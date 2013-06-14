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

    // Bind events:
    $('button.add-identifier', _dom).click(function() {
      addLine();
    });

    _dom.click(function(e) {
      var target = $(e.target),
          li = target.parents('ul.identifiers-list > li');

      // Check if it is a field button:
      if (li.length && target.is('button.remove-identifier')) {
        li.remove();
        checkValuesCount();
      }
    });

    // Init:
    if (obj.required) {
      $('button.add-identifier', _dom).click();
      $('ul.identifiers-list > li:first-child button.remove-identifier', _dom).attr('hidden', true);
    }

    // Check that all values are not added yet:
    function checkValuesCount() {
      if (obj.multiple && obj.only_one && $('ul.identifiers-list > li', _dom).length)
        $('button.add-identifier', _dom).attr('hidden', 'true');
      else
        $('button.add-identifier', _dom).attr('hidden', null);
    }

    function addLine(o) {
      var li = $(
        '<li>' +
          '<input type="text" class="col-4" value="' + (o ? o.value : '') + '" />' +
          '<button class="remove-identifier">-</button>' +
        '</li>'
      );

      checkValuesCount();
      $('ul.identifiers-list', _dom).append(li);
    }

    function _fill(data, fullData) {
      $('ul.identifiers-list', _dom).empty();

      (data || []).forEach(addLine);
    }

    function _getData() {
      var lis = $('ul.identifiers-list > li', _dom),
          res;

      if (obj.multiple) {
        res = [];
        lis.each(function() {
          res.push({
            type: obj.id_type,
            value: $(this).find('input').val()
          });
        });
      } else {
        res = lis.length ?
          {
            type: obj.id_type,
            value: $('ul.identifiers-list > li:first-child > input', _dom).val()
          } :
          null;
      }

      return res;
    }

    function _validate() {
      var data = _getData();

      // Check !multiple && required:
      if (
        (!obj.multiple && obj.required && !data) ||
        (obj.multiple && obj.required && obj.only_one && !data)
      ) {
        $('.message', this.dom).text('Exactly one identifier has to be added.');
        return false;
      }

      // Check multiple && required:
      if (obj.multiple && obj.required && data.length < 1) {
        $('.message', this.dom).text('At least one identifier has to be added.');
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
