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

      $('.create-form', _html).empty().attr('hidden', null).append(_components.map(function(o) {
        return o.dom;
      }));

      $('<button class="validate-button">Validate</button>').click(validate).appendTo($('.create-form', _html));
    }

    /**
     * This method checks if values entered in inputs by the user are valid. If
     * so, then an event will be dspatched containing the well-formed data.
     */
    function validate() {
      var invalid = 0;

      console.log('Form validation:');
      _components.some(function(comp) {
        var isValid =
          comp.validate ?
            comp.validate() :
            _defaultMethods.validate.call(comp);

        if (!isValid)
          invalid++;

        if (!isValid)
          console.log('  - Invalid component:', comp.property);
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

        if (entry) {
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
    this.triggers.events.displayForm = function(d, e) {
      var entry = e.data.entry;

      _fields = d.get('fields');
      _field = _fields[e.data.field];

      $('.create-form', _html).empty()
      generateForm();
      fill(entry);
    };
  };
})();
