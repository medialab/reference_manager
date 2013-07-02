;(function() {
  'use strict';
  mlab.pkg('blf.modules.customInputs');

  // Loading Handlebars templates:
  var _templates = {
        main: {
          path: 'templates/YearRangeField.handlebars'
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
   *  >   labels: "Year",
   *  >   property_start: "filter_date_start",
   *  >   property_end: "filter_date_end",
   *  >   type_ui: "YearRangeField"
   *  > }
   */
  blf.modules.customInputs.YearRangeField = function(obj) {
    domino.module.call(this);

    var _dom,
        _list = [],
        _self = this;

    generate();

    function generate() {
      _dom = $(_templates.main.template({
        label: obj.label
      }));
    }

    function _fill(data, fullData) {
      $('.date-from', _dom).val(data[obj.property_start]);
      $('.date-to', _dom).val(data[obj.property_end]);
    }

    function _getData(data) {
      data[obj.property_start] = $('.date-from', _dom).val();
      data[obj.property_end] = $('.date-to', _dom).val();
    }

    function _validate() {
      var data = {};
      _getData(data);

      if (+data[obj.property_start] > +data[obj.property_end]) {
        $('.message', _dom).text(i18n.t('customInputs:YearRangeField.errors.wrong_order'));
        return false;
      }

      $('.message', _dom).empty();
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
  };
})();
