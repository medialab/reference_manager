;(function() {
  'use strict';
  mlab.pkg('blf.modules.customInputs');
  /**
   * This custom input is basically a combo, whose options are dynamically
   * loaded.
   *
   * Data sample:
   * ************
   *
   *  > {
   *  >   label: "Pays de publication",
   *  >   multiple: true,
   *  >   property: "publication_countries",
   *  >   required: false,
   *  >   type_source: "country",
   *  >   type_ui: "TypeField"
   *  > }
   */
  blf.modules.customInputs.TypeField = function(obj) {
    domino.module.call(this);

    var _dom,
        _selected = {},
        _values = blf.control.get('lists')[obj.type_source] || [],
        _majorValues = _values.filter(function(o) {
          return o.major;
        }),
        _self = this;

    // Try to get the list:
    // AAARGH: How am I supposed to do when I add a module that needs to
    //         dispatch an event when bindings are actually not existing yet?
    //         So... here is one dirty solution:
    window.setTimeout(function() {
      if (!_values.length)
        _self.dispatchEvent('loadList', {
          list: obj.type_source
        });
    }, 0);

    _dom = $(
      '<fieldset class="customInput TypeField">' +
        '<div class="message"></div>' +
        '<label>' +
          (obj.label || obj.labels[blf.assets.lang]) + ' :' +
        '</label>' +
        '<div class="types-container container">' +
          '<ul class="values-list"></ul>' +
          (obj.only_one ? '' : '<button class="add-value">+</button>') +
        '</div>' +
      '</fieldset>'
    );

    // Bind events:
    $('button.add-value', _dom).click(function() {
      addLine();
    });

    _dom.click(function(e) {
      var target = $(e.target),
          li = target.parents('ul.values-list > li');

      // Check if it is a field button:
      if (li.length && target.is('button.remove-value')) {
        li.remove();
        checkValuesCount();
        checkValuesDups();
      }
    });

    function getLineContent(value) {
      return _majorValues.map(function(o) {
        return '<option value="' + o.type_id + '">' + o.label + '</option>';
      }).join();
    }

    // Check that all values are not added yet:
    function checkValuesCount() {
      if ($('ul.values-list > li', _dom).length >= _majorValues.length)
        $('button.add-value', _dom).attr('hidden', 'true');
      else
        $('button.add-value', _dom).attr('hidden', null);
    }

    // Deal with values deduplication:
    function checkValuesDups() {
      var list = $('ul.values-list > li > select', _dom);

      // Find selected values:
      _selected = {};
      list.each(function() {
        _selected[$(this).val()] = 1;
      });

      // Disable selected values:
      list.each(function() {
        var val = $(this).val();
        $(this).find('option').each(function() {
          var opt = $(this);
          if (opt.is(':selected') || !_selected[opt.val()])
            opt.attr('disabled', null);
          else
            opt.attr('disabled', 'true');
        });
      });
    }

    function addLine(s) {
      var li = $(
        '<li>' +
          '<select class="select-in-type col-3">' +
            getLineContent() +
          '</select>' +
          '<button class="remove-value">-</button>' +
        '</li>'
      );

      if (s)
        $('> select', li).val(s);

      // If the value is not specified, we use the first value that is
      // not used yet:
      else
        $('> select', li).val(_values.reduce(function(res, v) {
          return res !== null ?
            res :
            !$('select.select-in-type > option[value="' + v.type_id + '"]:selected', _dom).length ?
              v.type_id :
              null;
        }, null));

      $('select', li).change(checkValuesDups);
      $('ul.values-list', _dom).append(li);
      checkValuesCount();
      checkValuesDups();
    }

    function _fill() {
      // TODO
    }

    function _getData() {
      // TODO
    }

    function _validate() {
      // TODO
    }

    this.triggers.events.listsUpdated = function(d) {
      var list = d.get('lists')[obj.type_source] || [];

      if (!(_values || []).length && list.length) {
        _values = list;
        _majorValues = _values.filter(function(o) {
          return o.major;
        });
        $('select.select-in-type', _dom).empty().append(getLineContent());
      }
    };

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
  };
})();
