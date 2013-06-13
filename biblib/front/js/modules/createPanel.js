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
        _fields = {},
        _defaultMethods = {};

    // Bind DOM events:
    $('.select-field', _html).click(function(e) {
      var dom = $(e.target);

      // Check if it is a field anchor:
      if (dom.is('a[data-field]')) {
        var field = dom.attr('data-field');

        if (_fields[field]) {
          _field = _fields[field]
          generateForm();
        } else {
          _waitingField = field;
          _self.dispatchEvent('loadField', {
            field: _waitingField
          });
        }

        e.stopPropagation();
        return false;
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
                propertyObject: obj,
                property: obj.property,
                dom: $(
                  '<fieldset class="CharField">' +
                    '<div class="message"></div>' +
                    '<label for="' + obj.property + '"">' +
                      (obj.label || obj.labels[blf.assets.lang]) + ' :' +
                    '</label>' +
                    '<input class="col-6" name="' + obj.property + '" type="text" />' +
                  '</fieldset>'
                )
              });
              break;
            case 'DateField':
              _components.push({
                propertyObject: obj,
                property: obj.property,
                dom: $(
                  '<fieldset class="DateField">' +
                    '<div class="message"></div>' +
                    '<label for="' + obj.property + '"">' +
                      (obj.label || obj.labels[blf.assets.lang]) + ' :' +
                    '</label>' +
                    '<input class="col-6" name="' + obj.property + '" type="date" />' +
                  '</fieldset>'
                )
              });
              break;
            case 'IntegerField':
              _components.push({
                propertyObject: obj,
                property: obj.property,
                dom: $(
                  '<fieldset class="IntegerField">' +
                    '<div class="message"></div>' +
                    '<label for="' + obj.property + '"">' +
                      (obj.label || obj.labels[blf.assets.lang]) + ' :' +
                    '</label>' +
                    '<input class="col-6" name="' + obj.property + '" type="number" />' +
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

      $('<button class="validate-button">Validate</button>').click(validate).appendTo($('.create-form', _html));
    }

    function restart() {
      $('.create-form', _html).empty().attr('hidden', 'true');
      $('.select-field', _html).attr('hidden', null);
    }

    /**
     * This method checks if values entered in inputs by the user are valid. If
     * so, then an event will be dspatched containing the well-formed data.
     */
    function validate() {
      var invalid = 0;

      _components.some(function(comp) {
        var isValid =
          comp.validate ?
            comp.validate() :
            _defaultMethods.validate.call(comp);

        if (!isValid)
          invalid++;
      });

      if (invalid === 0)
        _self.dispatchEvent('validateEntry', {
          entry: getData()
        });
    }

    /**
     * This method returns the entry entered by the user in the form, according
     * to the scheme described by the "_field" object.
     * @return {object} The entry.
     */
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
          _defaultMethods.getData.call(component);

        if (value !== undefined)
        data[component.property] = value;
      }

      return data;
    }

    /**
     * This method fills the inputs in the form to represent an entry.
     */
    function fill(entry) {
      var i,
          l,
          component;

      for (i = 0, l = _components.length; i < l; i++) {
        component = _components[i];

        if (component.fill)
          component.fill(entry[component.property], entry);
        else
          _defaultMethods.fill.call(
            component,
            entry[component.property],
            entry
          );
      }
    }

    /**
     * DEFAULT INPUT METHODS:
     * **********************
     */
    /**
     * The default "getData" method.
     * @return {*} The data to insert in the new entry.
     */
    _defaultMethods.getData = function() {
      var value = $('input', this.dom).val();

      // Check empty strings:
      if (value === '')
        value = undefined;

      return value;
    }

    /**
     * The default "fill" method.
     * @param  {*} value The value to set in the input.
     */
    _defaultMethods.fill = function(value) {
      $('input', this.dom).val(value);
    }

    /**
     * The default "validate" method.
     * @return {boolean} "true" if valid, "false" else.
     */
    _defaultMethods.validate = function() {
      var isValid;

      if (this.propertyObject.required)
        isValid = (this.getData ?
          this.getData() :
          _defaultMethods.getData.call(this)) !== undefined;
      else
        isValid = true;

      // Display a short message if there is no value and the property is
      // required:
      if (!isValid)
        $('.message', this.dom).text('This field has to be specified.');
      else
        $('.message', this.dom).empty();

      return isValid;
    }

    /**
     * DOMINO BINDINGS:
     * ****************
     */
    // Listen to the controller:
    this.triggers.events.modeUpdated = function(d) {
      if (d.get('mode') === 'create')
        restart();
    };

    this.triggers.events.displayEntry = function(d, e) {
      var entry = e.data.entry;

      _field = _fields[e.data.field];

      restart();
      generateForm();
      fill(entry);
    };

    this.triggers.events.fieldsTreeUpdated = function(d) {
      var dom,
          tree = d.get('fieldsTree');

      // Generate the HTML to select which field to use:
      dom = (function recursiveParse(node, depth) {
        var header =
          (node.label && !node.bundle && !node.deprecated) ?
            '<a href="#" data-field="' + node.type_id + '">' +
              node.label +
            '</a>' :
            node.label ?
              '<span>' + node.label + '</span>' :
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
      _fields = d.get('fields');

      if (_waitingField && _fields[_waitingField]) {
        _field = _fields[_waitingField];
        generateForm();
        _waitingField = null;
      }
    };
  };
})();
