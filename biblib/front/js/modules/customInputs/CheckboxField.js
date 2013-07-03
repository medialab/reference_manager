;(function() {
  'use strict';
  mlab.pkg('blf.modules.customInputs');

  // Loading Handlebars templates:
  var _templates = {
        main: {
          path: 'templates/CheckboxField.handlebars'
        }
      };

  for (var k in _templates)
    (function(obj) {
      blf.utils.addTemplate(obj.path, function(data) {
        obj.template = data;
      });
    })(_templates[k]);

  /**
   * This custom input is used to represent a multiply selectable list.
   *
   * Data sample:
   * ************
   *
   *  > {
   *  >   label: "Document types"
   *  >   multiple: true,
   *  >   property: "filter_types",
   *  >   type_source: "document_type",
   *  >   type_ui: "CheckboxField"
   *  > }
   */
  blf.modules.customInputs.CheckboxField = function(obj, controller) {
    domino.module.call(this);

    var _dom,
        _values = controller.get('lists')[obj.type_source] || [],
        _self = this;

    generate();

    // Try to get the list:
    // AAARGH: How am I supposed to do when I add a module that needs to
    //         dispatch an event when bindings are actually not existing yet?
    //         So... here is one dirty solution, waiting for something cleaner:
    //
    //         => https://github.com/jacomyal/domino.js/issues/35
    window.setTimeout(function() {
      if (!_values.length)
        _self.dispatchEvent('loadList', {
          list: obj.type_source
        });
    }, 0);

    function generate() {
      var dom = $(_templates.main.template({
            label: obj.label,
            values: _values
          }));

      if (_dom)
        _dom.replaceWith(dom);

      _dom = dom;
    }

    function _fill(data, fullData) {
      var index = mlab.array.index(data, null);
      $('[type="checkbox"]', _dom).each(function() {
        var t = $(this);
        t.attr('checked', index[t.attr('id')] ? 'checked' : null);
      });
    }

    function _getData() {
      return Array.prototype.map.call($('[type="checkbox"]:checked', _dom), function() {
        return $(this).attr('id');
      });
    }

    function _validate() {
      // TODO
      return true;
    }

    this.getComponent = function() {
      return {
        dom: _dom,
        fill: _fill,
        getData: _getData,
        validate: _validate,
        propertyObject: obj,
        property: obj.property
      };
    };

    this.triggers.events.listsUpdated = function(controller) {
      if (!_values.length && controller.get('lists')[obj.type_source]) {
        _values = controller.get('lists')[obj.type_source];
        generate();
      }
    };
  };
})();
