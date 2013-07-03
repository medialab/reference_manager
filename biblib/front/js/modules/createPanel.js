;(function() {
  'use strict';
  mlab.pkg('blf.modules.customInputs');

  // Loading Handlebars templates:
  blf.templates.require([
    'CharField',
    'DateField',
    'IntegerField',
    'createPanel.validate'
  ]);

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
      _components.forEach(function(component) {
        var isValid = blf.modules.createPanel.validate(component);

        if (!isValid)
          invalid++;

        if (!isValid)
          blf.control.log('  - Invalid component:', component.property);
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
        value = blf.modules.createPanel.getData(component, data);

        if (value !== undefined && component.property !== undefined)
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

        if (entry)
          blf.modules.createPanel.fill(component, entry);
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

      _components = blf.modules.createPanel.generateForm(blf.control, _field.children);
      $('.create-form', _html).empty().append(_components.map(function(o) {
        return o.dom;
      }));

      $(blf.templates.get('createPanel.validate')()).click(validate).appendTo($('.create-form', _html));

      fill(entry || { rec_type: e.data.field.children });
    };
  };

  /**
   * FORM GENERATION STATIC HELPERS:
   * *******************************
   */
  mlab.pkg('blf.modules.createPanel.defaultMethods');
  blf.modules.createPanel.generateForm = function(d, config) {
    var i,
        l,
        obj,
        module,
        component,
        components = [];

    // Parse children:
    for (i = 0, l = config.length; i < l; i++)
      components.push(blf.modules.createPanel.getComponent(d, config[i]));

    return components;
  };

  /**
   * Instanciates and returns the good component.
   * @return {*} The component instance.
   */
  blf.modules.createPanel.getComponent = function(d, obj) {
    var component,
        template,
        module = blf.modules.customInputs[obj.type_ui];

    // If a custom component is found:
    if (typeof module === 'function') {
      module = d.addModule(module, [obj]);
      component = module.getComponent();

    // Else, if a basic component is recognized:
    } else if (template = blf.templates.get(obj.type_ui))
      component = {
        propertyObject: obj,
        property: obj.property,
        dom: $(template({
          label: obj.label || obj.labels[blf.assets.lang],
          property: obj.property
        }))
      };

    // If not recognized at all:
    else
      d.warn('Data type "' + obj.type_ui + '" not recognized.');

    return component;
  };

  /**
   * Methods that work on every components:
   */
  blf.modules.createPanel.getData = function(component, data) {
    return component.getData ?
      component.getData(data) :
      blf.modules.createPanel.defaultMethods.getData.call(component);
  };

  blf.modules.createPanel.fill = function(component, entry) {
    if (component.fill)
      component.fill(component.property ? entry[component.property] : null, entry);
    else
      blf.modules.createPanel.defaultMethods.fill.call(
        component,
        entry[component.property],
        entry
      );
  };

  blf.modules.createPanel.validate = function(component) {
    return component.validate ?
      component.validate() :
      blf.modules.createPanel.defaultMethods.validate.call(component);
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
