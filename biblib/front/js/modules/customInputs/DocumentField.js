;(function() {
  'use strict';
  mlab.pkg('blf.modules.customInputs');

  /**
   * This custom input can be used to add parents entries. It can of course
   * a bit of madness when recursive parenting are used...
   *
   * Data sample:
   * ************
   *
   *  > // TODO
   */
  blf.modules.customInputs.DocumentField = function(obj) {
    domino.module.call(this);

    var _dom,
        _self = this;

    _dom = $(
      '<fieldset class="customInput DocumentField">' +
        '<div class="message"></div>' +
        '<label>' +
          (obj.label || obj.labels[blf.assets.lang]) + ' :' +
        '</label>' +
        '<div class="documents-container container">' +
          '<span>(component not working yet)</span>' +
          // '<ul class="documents-list"></ul>' +
          // '<button class="add-document">+</button>' +
        '</div>' +
      '</fieldset>'
    );

    function _fill() {
      // TODO
    }

    function _getData() {
      // TODO
    }

    function _validate() {
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
