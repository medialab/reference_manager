;(function() {
  'use strict';

  // Package "blf": BibLib Front
  mlab.pkg('blf.modules.formComponents');

  blf.modules.formGenerator = function(control) {
    domino.modules.call(this);

    var _self = this,
        _html = $('#layout');

    function generateForm(field) {
      var i,
          l,
          obj,
          component;

      // Parse children:
      for (i = 0, l = field.children.length; i++; i < l) {
        obj = field.children[i];
        component = blf.modules.formComponents[obj.type_data];

        if (component) {

        } else {
          switch (obj.type_data) {
            case 'text':
              // TODO
              break;
            case 'date':
              // TODO
              break;
            case 'number':
              // TODO
              break;
            default:
              control.warn('Data type "' + obj.type_data + '" not recognized.');
              break;
          }
        }
      }
    }
  };

  // Basic components for forms generation:
  blf.modules.formComponents.text = {
    dom: '<input type="text">',
    validate: function(dom) {
      return dom.attr('value');
    }
  };

  blf.modules.formComponents.date = {
    dom: '<input type="date">',
    validate: function(dom) {
      return dom.attr('value');
    }
  };

  blf.modules.formComponents.number = {
    dom: '<input type="number">',
    validate: function(dom) {
      return dom.attr('value');
    }
  };

  // Components to develop:
  //  - text:
  //    "<input type="text">"
  //  - date
  //    "<input type="date">"
  //  - number
  //    "<input type="number">"
  //  - Creator
  //  - LanguageValue
})();
