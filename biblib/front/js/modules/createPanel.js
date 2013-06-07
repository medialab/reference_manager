;(function() {
  'use strict';

  mlab.pkg('blf.modules.customInputs');

  blf.modules.createPanel = function(html) {
    domino.module.call(this);

    var _self = this,
        _html = html,
        _waitingField,
        _field,
        _modules = [],
        _components = [],
        _fieldsIndex = {};

    // Bind DOM events:
    $('.select-field', _html).click(function(e) {
      var dom = $(e.target);

      // Check if it is a field button:
      if (dom.is('button[data-field]')) {
        var field = dom.attr('data-field');

        if (_fieldsIndex[field]) {
          _field = _fieldsIndex[field]
          generateForm();
        } else {
          _waitingField = field;
          _self.dispatchEvent('loadField', {
            field: _waitingField
          });
        }
      }
    });

    // The following method generates the form:
    function generateForm() {
      var i,
          l,
          obj,
          module,
          component;

      _modules = [];
      _components = [];

      // Parse children:
      for (i = 0, l = _field.children.length; i < l; i++) {
        obj = _field.children[i];
        module = blf.modules.customInputs[obj.type_ui];

        // If a custom component is found:
        if (typeof module === 'function') {
          module = blf.control.addModule(module, [obj]);
          _modules.push(module);
          _components.push(module.getComponent());

        // Else, if a basic component is recognized:
        } else {
          switch (obj.type_ui) {
            case 'CharField':
              _components.push({
                property: obj.property,
                dom: $(
                  '<fieldset class="CharField">' +
                    '<label for="' + obj.property + '"">' + obj.labels[blf.assets.lang] + ' :</label>' +
                    '<input class="col-3" name="' + obj.property + '" type="text" />' +
                  '</fieldset>'
                )
              });
              break;
            case 'DateField':
              _components.push({
                property: obj.property,
                dom: $(
                  '<fieldset class="DateField">' +
                    '<label for="' + obj.property + '"">' + obj.labels[blf.assets.lang] + ' :</label>' +
                    '<input class="col-3" name="' + obj.property + '" type="date" />' +
                  '</fieldset>'
                )
              });
              break;
            case 'IntegerField':
              _components.push({
                property: obj.property,
                dom: $(
                  '<fieldset class="IntegerField">' +
                    '<label for="' + obj.property + '"">' + obj.labels[blf.assets.lang] + ' :</label>' +
                    '<input class="col-3" name="' + obj.property + '" type="number" />' +
                  '</fieldset>'
                )
              });
              break;
            default:
              _self.dispatchEvent('warn', {
                message: 'Data type "' + obj.type_ui + '" not recognized.'
              });
              break;
          }
        }
      }

      $('.select-field', _html).attr('hidden', 'true');
      $('.create-form', _html).empty().attr('hidden', null).append(_components.map(function(o) {
        return o.dom;
      }));

      $('<button class="validate-button">Validate</button>').click(function() {
        if (_components.some(function(comp) {
          return comp.validate && !comp.validate();
        }))
          console.log('not valid');
        else
          console.log('Data:', getData());
      }).appendTo($('.create-form', _html));
    }

    function restart() {
      $('.create-form', _html).empty().attr('hidden', 'true');
      $('.select-field', _html).attr('hidden', null);
    }

    function getData() {
      var i,
          l,
          component,
          value,
          data = {};

      for (i = 0, l = _components.length; i < l; i++) {
        component = _components[i];
        value = component.getData ?
          component.getData() :
          getDataFromComponent.call(component);

        if (value !== undefined)
        data[component.property] = value;
      }

      return data;
    }

    /**
     * The default "getData" method
     * @return {[type]} [description]
     */
    function getDataFromComponent() {
      var value = $('input', this.dom).val();

      // Check empty strings:
      if (value === '')
        value = undefined;

      return value;
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
        var header =
          (node.name && !node.bundle) ?
            '<button data-field="' + node.name + '">' +
              node.name +
            '</button>' :
            node.name ?
              '<span>' + node.name + '</span>' :
              '';

        return header +
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
            '');
      })(tree, 0);

      // Add the HTML to the DOM:
      $('.select-field', _html).empty().append(dom);
    };

    this.triggers.events.fieldsUpdated = function(d) {
      _fieldsIndex = mlab.array.index(d.get('fields'), 'rec_type');

      if (_waitingField && _fieldsIndex[_waitingField]) {
        _field = _fieldsIndex[_waitingField];
        generateForm();
        _waitingField = null;
      }
    };
  };
})();
