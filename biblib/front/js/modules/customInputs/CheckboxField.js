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
  blf.modules.customInputs.CheckboxField = function(obj) {
    domino.module.call(this);

    var _dom,
        _list = [],
        _self = this;

    generate();

    function generate() {
      _dom = $(_templates.main.template({
        label: obj.label,
        values: _list
      }));
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
      if (!_list && controller.get('lists')[obj.type_source]) {
        _list = controller.get('lists')[obj.type_source];
        generate();
      }
    };
  };
})();
