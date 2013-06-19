;(function() {
  'use strict';

  mlab.pkg('blf.modules.customInputs');

  blf.modules.createPanel = function(html) {
    domino.module.call(this);

    var _self = this,
        _html = html,
        _waitingField,
        _field,
        _components = [],
        _fields = {};

    /**
     * This method checks if values entered in inputs by the user are valid. If
     * so, then an event will be dspatched containing the well-formed data.
     */
    function validate() {
      var invalid = 0;

      console.log('Form validation:');
      _components.forEach(function(comp) {
        var isValid =
          comp.validate ?
            comp.validate() :
            blf.modules.createPanel.defaultMethods.validate.call(comp);

        if (!isValid)
          invalid++;

        if (!isValid)
          console.log('  - Invalid component:', comp.property);
      });

      if (invalid === 0) {
        var data = getData();
        console.log('Data:', domino.utils.clone(data));
        _self.dispatchEvent('validateEntry', {
          entry: data
        });
      }
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
          blf.modules.createPanel.defaultMethods.getData.call(component);

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
            blf.modules.createPanel.defaultMethods.fill.call(
              component,
              entry[component.property],
              entry
            );
        }
      }
    }

    /**
     * DOMINO BINDINGS:
     * ****************
     */
    this.triggers.events.displayForm = function(d, e) {
      var entry = e.data.entry;

      _fields = d.get('fields');
      _field = _fields[e.data.field];

      _components = blf.modules.createPanel.generateForm(blf.control, _field);
      $('.create-form', _html).empty().append(_components.map(function(o) {
        return o.dom;
      }));

      $('<button class="validate-button">Validate</button>').click(validate).appendTo($('.create-form', _html));

      fill(entry);
    };
  };

  /**
   * FORM GENERATION STATIC HELPERS:
   * *******************************
   */
  mlab.pkg('blf.modules.createPanel.defaultMethods');
  blf.modules.createPanel.generateForm = function(d, field) {
    var i,
        l,
        obj,
        module,
        component,
        components = [];

    // Parse children:
    for (i = 0, l = field.children.length; i < l; i++) {
      obj = field.children[i];
      module = blf.modules.customInputs[obj.type_ui];

      // If a custom component is found:
      if (typeof module === 'function') {
        module = d.addModule(module, [obj]);
        components.push(module.getComponent());

      // Else, if a basic component is recognized:
      } else {
        switch (obj.type_ui) {
          case 'CharField':
            components.push({
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
            components.push({
              propertyObject: obj,
              property: obj.property,
              dom: $(
                '<fieldset class="DateField">' +
                  '<div class="message"></div>' +
                  '<label for="' + obj.property + '"">' +
                    (obj.label || obj.labels[blf.assets.lang]) + ' :' +
                  '</label>' +
                  '<input class="col-6" name="' + obj.property + '" type="year" />' +
                '</fieldset>'
              )
            });
            break;
          case 'IntegerField':
            components.push({
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
            d.warn('Data type "' + obj.type_ui + '" not recognized.');
            break;
        }
      }
    }

    return components;
  };

  /**
   * The default "getData" method.
   * @return {*} The data to insert in the new entry.
   */
  blf.modules.createPanel.defaultMethods.getData = function() {
    var value = $('input', this.dom).val();

    // Check empty strings:
    if (value === '')
      value = undefined;

    return value;
  };

  /**
   * The default "fill" method.
   * @param  {*} value The value to set in the input.
   */
  blf.modules.createPanel.defaultMethods.fill = function(value) {
    $('input', this.dom).val(value);
  };

  /**
   * The default "validate" method.
   * @return {boolean} "true" if valid, "false" else.
   */
  blf.modules.createPanel.defaultMethods.validate = function() {
    var isValid;

    if (this.propertyObject.required)
      isValid = (this.getData ?
        this.getData() :
        blf.modules.createPanel.defaultMethods.getData.call(this)) !== undefined;
    else
      isValid = true;

    // Display a short message if there is no value and the property is
    // required:
    if (!isValid)
      $('.message', this.dom).text('This field has to be specified.');
    else
      $('.message', this.dom).empty();

    return isValid;
  };
})();
