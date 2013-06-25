;(function() {
  'use strict';
  mlab.pkg('blf.modules.customInputs');

  // Loading Handlebars templates:
  var _templates = {
        main: {
          path: 'templates/IdentifierField.handlebars'
        },
        line: {
          path: 'templates/IdentifierField.line.handlebars'
        }
      };

  for (var k in _templates)
    (function(obj) {
      blf.utils.addTemplate(obj.path, function(data) {
        obj.template = data;
      });
    })(_templates[k]);

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

    _dom = $(_templates.main.template({
      label: obj.label || obj.labels[blf.assets.lang]
    }));

    // Bind events:
    $('button.add-identifier', _dom).click(function() {
      addLine();
    });

    _dom.click(function(e) {
      var target = $(e.target),
          li = target.closest('li');

      // Check if it is a field button:
      if (li.length && target.is('button.remove-identifier')) {
        li.remove();
        checkValuesCount();
      }
    });

    // Init:
    if (obj.required) {
      $('button.add-identifier', _dom).click();
      $('li:first-child button.remove-identifier', _dom).attr('hidden', true);
    }

    // Check that all values are not added yet:
    function checkValuesCount() {
      if (obj.multiple && obj.only_one && $('li', _dom).length)
        $('button.add-identifier', _dom).attr('hidden', 'true');
      else
        $('button.add-identifier', _dom).attr('hidden', null);
    }

    function addLine(o) {
      var li = $(_templates.line.template({
            value: (o || {}).value || ''
          }));

      checkValuesCount();
      $('ul.identifiers-list', _dom).append(li);
    }

    function _fill(data, fullData) {
      $('ul.identifiers-list', _dom).empty();

      (data || []).forEach(addLine);
    }

    function _getData() {
      var lis = $('li', _dom),
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
            value: $('li:first-child input', _dom).val()
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
        $('.message', this.dom).text(i18n.t('customInputs:IdentifierField.errors.exactly_one'));
        return false;
      }

      // Check multiple && required:
      if (obj.multiple && obj.required && data.length < 1) {
        $('.message', this.dom).text(i18n.t('customInputs:IdentifierField.errors.at_least_one'));
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
