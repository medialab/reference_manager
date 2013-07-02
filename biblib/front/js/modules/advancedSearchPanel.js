;(function() {
  'use strict';

  mlab.pkg('blf.modules');

  // Loading Handlebars templates:
  var _templates = {
        main: {
          path: 'templates/advancedSearchPanel.handlebars'
        },
        index: {
          path: 'templates/advancedSearchPanel.index.handlebars'
        },
        filter: {
          path: 'templates/advancedSearchPanel.filter.handlebars'
        }
      };

  for (var k in _templates)
    (function(obj) {
      blf.utils.addTemplate(obj.path, function(data) {
        obj.template = data;
      });
    })(_templates[k]);

  /**
   * The advanced search panel.
   */
  blf.modules.advancedSearchPanel = function(html, controller) {
    domino.module.call(this);

    var _self = this,
        _html = html,
        _index,
        _filter,
        _filtersComponents;

    _html.append($(_templates.main.template()));

    // Try to get the list:
    // AAARGH: How am I supposed to do when I add a module that needs to
    //         dispatch an event when bindings are actually not existing yet?
    //         So... here is one dirty solution, waiting for something cleaner:
    //
    //         => https://github.com/jacomyal/domino.js/issues/35
    window.setTimeout(function() {
      [
        _index.property_source_index,
        _index.property_source_operator
      ].forEach(function(v) {
        if (v)
          _self.dispatchEvent('loadList', {
            list: v
          });
      });
    }, 0);

    // Bind DOM events:
    _html.on('click', '.add-index', function() {
      _index.indexesArray = getIndexesArray().concat({
        index: _index.indexes[0].type_id,
        query: '',
        operator: _index.default_operator
      });
      generateIndex();
    }).on('click', '.remove-index', function(e) {
      _index.indexesArray.splice(
        $(e.target).closest('.index').index(),
        1
      );
      generateIndex();
    });

    reset();

    function getIndexesArray() {
      var res = [];
      $('.index', _html).each(function() {
        var self = $(this);
        res.push({
          index: $('[data-type="index"]', self).val(),
          query: $('[data-type="query"]', self).val(),
          operator: $('[data-type="operator"]', self).val()
        });
      });

      return res;
    }

    // Generate index DOM:
    function generateIndex() {
      var dom = $('.index-container', _html).empty();

      if (_index)
        dom.append($(_templates.index.template(_index)));
    }

    // Regenerate everything blabla:
    function reset() {
      var config = blf.utils.translateLabels(
        controller.get('config').advancedSearchPanel || {}
      );

      _index = config.index;
      _index.indexesArray = _index.default_index.map(function(v) {
        return typeof v === 'string' ?
          {
            index: v,
            query: '',
            operator: _index.default_operator
          } :
          v;
      });
      _filter = config.filters;

      if (_filtersComponents) {
        // TODO
        // Kill existing modules
      }
      _filtersComponents = blf.modules.createPanel.generateForm(
        blf.control,
        _filter
      );
      $('.filter-container', _html).empty().append(_filtersComponents.map(function(o) {
        return o.dom;
      }));

      generateIndex();
    }

    this.triggers.events.listsUpdated = function(controller) {
      if (_index) {
        var indexes = controller.get('lists')[_index.property_source_index],
            operators = controller.get('lists')[_index.property_source_operator];

        if (!_index.indexes && indexes) {
          _index.indexes = indexes;
          generateIndex();
        }

        if (!_index.operators && operators) {
          _index.operators = operators;
          generateIndex();
        }
      }
    };
  };
})();
