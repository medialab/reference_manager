;(function() {
  'use strict';
  mlab.pkg('blf.modules.customInputs');

  // Loading Handlebars templates:
  blf.templates.require([
    'DocumentField',
    'DocumentField.line'
  ]);

  /**
   * This custom input can be used to add parents entries. It can of course
   * a bit of madness when recursive parenting are used...
   *
   * Warning
   * *******
   *
   * Since this component includes other components (even eventually a similar
   * one), jQuery selectors are kind of strict, and you have to be very careful
   * if you modify them - or any related template.
   *
   * Data sample:
   * ************
   *
   *  > {
   *  >   label: "Collection",
   *  >   only_one: true,
   *  >   property: "seriess",
   *  >   required: false,
   *  >   type_fields: [
   *  >     "Series"
   *  >   ],
   *  >   type_ui: "DocumentField"
   *  > }
   */
  blf.modules.customInputs.DocumentField = function(obj, d) {
    domino.module.call(this);

    var _dom = $(blf.templates.get('DocumentField')({
          label: obj.label || obj.labels[blf.assets.lang]
        })),
        _ul = $('ul', _dom).first(),
        _lineID = 1,
        _self = this,
        _forms = {},
        _classTemplates,
        _fields = d.get('fields');

    // Try to get the list:
    // AAARGH: How am I supposed to do when I add a module that needs to
    //         dispatch an event when bindings are actually not existing yet?
    //         So... here is one dirty solution, waiting for something cleaner:
    //
    //         => https://github.com/jacomyal/domino.js/issues/35
    window.setTimeout(function() {
      obj.type_fields.forEach(function(v) {
        _self.dispatchEvent('loadField', {
          field: v
        });
      });
    }, 0);

    // Add a line. The line is empty (ie to be filled by the user) if data is
    // not specified.
    function addDocument(data) {
      data = data || {};
      var id = _lineID++,
          li = $(blf.templates.get('DocumentField.line')({
            id: id,
            type_fields: obj.type_fields
          }));

      if (data.rec_type) {
        $('select.select-field', li).first().val(data.rec_type);
        _forms[id] = blf.modules.createPanel.generateForm(blf.control, _fields[data.rec_type].children);

        $('.custom-container', li).first().empty().append(_forms[id].components.map(function(o) {
          return o.dom;
        }));

        _forms[id].fill(data);
      }

      _ul.append(li);
      // Check count:
      if (obj.only_one && _ul.children('li').length >= 1)
        $('.add-document', _dom).css('display', 'none');
      else
        $('.add-document', _dom).css('display', '');

      // Trigger event if only one type available:
      if (!data.rec_type && obj.type_fields.length <= 1)
        $('select.select-field', li).first().change();
    }

    // Bind events:
    $('button.add-document', _dom).click(function() {
      addDocument();
    });

    _dom.click(function(e) {
      var target = $(e.target),
          li = target.closest('li').first();

      // Check if it is a field button:
      if (li.length && target.is('button.remove-document')) {
        var id = li.data('id');
        li.remove();
        delete _forms[id];

        // Trigger event if only one type available:
        if (obj.type_fields.length <= 1)
          $('select.select-field', li).first().change();

        // Check count:
        if (obj.only_one && _ul.children('li').length >= 1)
          $('.add-document', _dom).css('display', 'none');
        else
          $('.add-document', _dom).css('display', '');
      }
    }).change(function(e) {
      var target = $(e.target),
          li = target.closest('li');

      // Check which select it is:
      if (li.length && target.is(_ul.children('li').children('select.select-field'))) {
        var id = li.data('id'),
            value = target.val(),
            container = $('.custom-container', li).first();

        _forms[id] = blf.modules.createPanel.generateForm(blf.control, _fields[value].children);
        container.empty().append(_forms[id].components.map(function(o) {
          return o.dom;
        }));
      }
    });

    /**
     *  Check if the content of the component is valid. Returns true if valid,
     *  and false if not.
     *
     * @return {string} Returns true if the content id valid, and false else.
     */
    function _validate() {
      var k,
          invalid = 0,
          data = _getData();

      $('.message', _dom).first().empty();
      if (obj.required && !(data || []).length) {
        $('.message', _dom).first().text(i18n.t('customInputs:DocumentField.errors.exactly_one'));
        return false;
      }

      for (k in _forms)
        if (!_forms[k].validate())
          invalid++;

      return invalid === 0;
    }

    /**
     * Fill the component with existing data.
     *
     * @param  {object} data The data to display in the component.
     * @param  {object} full The full entry (sometimes might be needed).
     */
    function _fill(data) {
      _ul.empty();

      // Parse data and create lines:
      (data || []).forEach(addDocument);
    }

    /**
     * Returns the well-formed data described by the component.
     *
     * @return {*} The data.
     */
    function _getData() {
      var documents = [];

      // Parse line and form data:
      _ul.children('li').each(function() {
        var value,
            li = $(this),
            id = li.data('id'),
            data = _forms[id].getData();

        data.rec_type = $('select.select-field', li).first().val();
        documents.push(data);
      });

      return documents.length ? documents : undefined;
    }

    /**
     * This method returns the component object.
     *
     * @return {object} The component object.
     */
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

    // Domino bindings:
    this.triggers.events.fieldsUpdated = function(d) {
      // If each related field has already been loaded, do nothing:
      if (obj.type_fields.every(function(o) {
        return _fields[o];
      }))
        return;

      // Else, let's regenerate the <select> contents:
      _fields = d.get('fields');

      _ul.children('li').each(function() {
        $(this).find('select.select-field').first().html(
          obj.type_fields.filter(function(s) {
            return _fields[s];
          }).map(function(s) {
            var o = _fields[s];
            return '<option value="' + o.rec_type + '">' + o.rec_type + '</option>';
          }).join()
        );
      });
    };
  };
})();
