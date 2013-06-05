;(function() {
  'use strict';

  // Package "blf": BibLib Front
  mlab.pkg('blf.customInputs');

  blf.modules.createPanel = function(html) {
    domino.module.call(this);

    var _self = this,
        _html = html,
        _waitingField,
        _fieldsIndex = {};

    // Bind DOM events:
    $('.select-field', _html).click(function(e) {
      var dom = $(e.target);

      // Check if it is a field button:
      if (dom.is('button[data-field]')) {
        var field = dom.attr('data-field');

        if (_fieldsIndex[field])
          generateForm(_fieldsIndex[field]);
        else {
          _waitingField = field;
          _self.dispatchEvent('loadField', {
            field: _waitingField
          });
        }
      }
    });

    // The following method generates the form:
    function generateForm(field) {
      var i,
          l,
          obj,
          component,
          components = [];

      // Parse children:
      for (i = 0, l = field.children.length; i < l; i++) {
        obj = field.children[i];
        component = blf.customInputs[obj.type_data];

        // If a custom component is found:
        if (typeof component === 'function') {
          components.push(new component(obj));

        // Else, if a basic component is recognized:
        } else {
          switch (obj.type_data) {
            case 'text':
              components.push({
                dom: $(
                  '<fieldset>' +
                    '<label for="' + obj.property + '"">' + obj.labels[blf.lang] + ' :</label>' +
                    '<input name="' + obj.property + '" type="text" />' +
                  '</fieldset>'
                )
              });
              break;
            case 'date':
              components.push({
                dom: $(
                  '<fieldset>' +
                    '<label for="' + obj.property + '"">' + obj.labels[blf.lang] + ' :</label>' +
                    '<input name="' + obj.property + '" type="date" />' +
                  '</fieldset>'
                )
              });
              break;
            case 'number':
              components.push({
                dom: $(
                  '<fieldset>' +
                    '<label for="' + obj.property + '"">' + obj.labels[blf.lang] + ' :</label>' +
                    '<input name="' + obj.property + '" type="number" />' +
                  '</fieldset>'
                )
              });
              break;
            default:
              _self.dispatchEvent('log', {
                message: 'Data type "' + obj.type_data + '" not recognized.'
              });
              break;
          }
        }
      }

      $('.select-field', _html).attr('hidden', 'true');
      $('.create-form', _html).empty().attr('hidden', null).append(components.map(function(o) {
        return o.dom;
      }));
    }

    function restart() {
      $('.create-form', _html).empty().attr('hidden', 'true');
      $('.select-field', _html).attr('hidden', null);
    }

    // Listen to the controller:
    this.triggers.events.modeUpdated = function(d) {
      if (d.get('mode') === 'create')
        restart();
    };

    this.triggers.events.fieldsTreeUpdated = function(d) {
      var dom,
          tree = d.get('fieldsTree');

      // Generate the HTML to select which field to use:
      dom = (function recursiveParse(node, depth) {
        return(
          (node.name ?
            '<button data-field="' + node.name + '">' +
              node.name +
            '</button>' :
            '') +
          ((node.children || []).length ?
            '<ul class="tree-depth-' + depth + '">' +
              node.children.map(function(obj) {
                return(
                  '<li>' +
                    recursiveParse(obj, depth + 1) +
                  '</li>'
                );
              }).join('') +
            '</ul>' :
            '')
        );
      })(tree, 0);

      // Add the HTML to the DOM:
      $('.select-field', _html).empty().append(dom);
    };

    this.triggers.events.fieldsUpdated = function(d) {
      _fieldsIndex = mlab.array.index(d.get('fields'), 'rec_type');

      if (_waitingField && _fieldsIndex[_waitingField]) {
        generateForm(_fieldsIndex[_waitingField]);
        _waitingField = null;
      }
    };
  };
})();
