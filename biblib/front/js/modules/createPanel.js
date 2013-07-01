;(function() {
  'use strict';
  mlab.pkg('blf.modules.customInputs');

  // Loading Handlebars templates:
  var _templates = {
        CharField: {
          path: 'templates/CharField.handlebars'
        },
        DateField: {
          path: 'templates/DateField.handlebars'
        },
        IntegerField: {
          path: 'templates/IntegerField.handlebars'
        },
        validate: {
          path: 'templates/createPanel.validate.handlebars'
        }
      };

  for (var k in _templates)
    (function(obj) {
      blf.utils.addTemplate(obj.path, function(data) {
        obj.template = data;
      });
    })(_templates[k]);

  // Module constructor:
  blf.modules.createPanel = function(html) {
    domino.module.call(this);

    var _self = this,
        _html = html,
        _waitingField,
        _field,
        _toKeep = [
          'rec_source',
          'rec_type',
          'rec_id',
          'nonce',
          '_id'
        ],
        _currentToKeep = {},
        _propertiesToAdd = {
          rec_class: 'Document',
          rec_metajson: 1
        },
        _components = [],
        _fields = {};

    /**
     * This method checks if values entered in inputs by the user are valid. If
     * so, then an event will be dspatched containing the well-formed data.
     */
    function validate() {
      var invalid = 0;

      blf.control.log('Form validation:');
      _components.forEach(function(comp) {
        var isValid =
          comp.validate ?
            comp.validate() :
            blf.modules.createPanel.defaultMethods.validate.call(comp);

        if (!isValid)
          invalid++;

        if (!isValid)
          blf.control.log('  - Invalid component:', comp.property);
      });

      if (invalid === 0) {
        var data = getData();
        blf.control.log('Everything is valid - data:', domino.utils.clone(data));
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
          k,
          component,
          value,
          data = domino.utils.clone(_currentToKeep);

      for (k in _propertiesToAdd)
        data[k] = _propertiesToAdd[k];

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
          component,
          parsed = {};

      // Store data to keep:
      _currentToKeep = _toKeep.reduce(function(o, k) {
        o[k] = domino.utils.clone(entry[k]);
        return o;
      }, {});

      // Parse components
      for (i = 0, l = _components.length; i < l; i++) {
        component = _components[i];

        if (parsed[component.property])
          blf.control.log('Hum, the property "' + component.property + '" has already been given to a component...');

        parsed[component.property] = 1;

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

      for (i in entry)
        if (!parsed[i])
          blf.control.log('Property not parsed:', i, 'value:', entry[i]);
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

      $(_templates.validate.template()).click(validate).appendTo($('.create-form', _html));

      fill(entry || { rec_type: e.data.field });
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
      } else if (_templates[obj.type_ui])
        components.push({
          propertyObject: obj,
          property: obj.property,
          dom: $(_templates[obj.type_ui].template({
            label: obj.label || obj.labels[blf.assets.lang],
            property: obj.property
          }))
        });

      // If not recognized at all:
      else
        d.warn('Data type "' + obj.type_ui + '" not recognized.');
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

    if (this.propertyObject.multiple)
      value = [value];

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
      $('.message', this.dom).text(i18n.t('customInputs:TypeField.errors.at_least_one'));
    else
      $('.message', this.dom).empty();

    return isValid;
  };
})();
