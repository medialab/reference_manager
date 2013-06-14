;(function() {
  'use strict';
  mlab.pkg('blf.modules.customInputs');

  /**
   * This custom input is used to represent identifier-like properties.
   *
   * Data sample:
   * ************
   *
   *  > {
   *  >   id_type: "isbn",
   *  >   label: "ISBN",
   *  >   multiple: true,
   *  >   only_one: true,
   *  >   property: "identifiers",
   *  >   required: false,
   *  >   type_ui: "IdentifierField"
   *  > }
   */
  blf.modules.customInputs.IdentifierField = function(obj) {
    domino.module.call(this);

    var _dom,
        _self = this;

    _dom = $(
      '<fieldset class="customInput IdentifierField">' +
        '<div class="message"></div>' +
        '<label>' +
          (obj.label || obj.labels[blf.assets.lang]) + ' :' +
        '</label>' +
        '<div class="identifier-container container">' +
          '<ul class="identifiers-list"></ul>' +
          '<button class="add-identifier">+</button>' +
        '</div>' +
      '</fieldset>'
    );

    function _addLine(value) {
      // TODO
    }

    function _fill() {
      // TODO
    }

    function _getData() {
      if (obj.multiple)
        return ;
      else
        return ;
    }

    function _validate() {
      var data = _getData();

      // Check multiple && required:
      if (obj.multiple && obj.required && data.length < 1) {
        $('.message', this.dom).text('At least one identifier has to be added.');
        return false;
      }

      // Check !multiple && required:
      if (!obj.multiple && obj.required && !data) {
        $('.message', this.dom).text('Exactly one identifier has to be added.');
        return false;
      }

      $('.message', this.dom).empty();
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
