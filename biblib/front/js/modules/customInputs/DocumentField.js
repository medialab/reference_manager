;(function() {
  'use strict';
  mlab.pkg('blf.modules.customInputs');

  // Loading Handlebars templates:
  var _templates = {
        main: {
          path: 'templates/DocumentField.handlebars'
        },
        line: {
          path: 'templates/DocumentField.line.handlebars'
        }
      };

  for (var k in _templates)
    (function(obj) {
      blf.utils.addTemplate(obj.path, function(data) {
        obj.template = data;
      });
    })(_templates[k]);

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

    var _dom = $(_templates.main.template({
          label: obj.label || obj.labels[blf.assets.lang]
        })),
        _ul = $('ul', _dom).first(),
        _lineID = 1,
        _self = this,
        _linesHash = {},
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
          li = $(_templates.line.template({
            id: id,
            type_fields: obj.type_fields
          }));

      if (data.rec_type) {
        $('select.select-field', li).first().val(data.rec_type);

        _linesHash[id] = blf.modules.createPanel.generateForm(blf.control, _fields[data.rec_type]);
        $('.custom-container', li).first().empty().append(_linesHash[id].map(function(o) {
          return o.dom;
        }));

        _linesHash[id].forEach(function(comp) {
          if (comp.fill)
            comp.fill(data.document[comp.property], data.document);
          else
            blf.modules.createPanel.defaultMethods.fill.call(
              comp,
              data.document[comp.property],
              data.document
            );
        });
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
        delete _linesHash[id];

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

        _linesHash[id] = blf.modules.createPanel.generateForm(blf.control, _fields[value]);
        container.empty().append(_linesHash[id].map(function(o) {
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
          invalid = 0;

      $('.message', _dom).first().empty();

      if (obj.required && (!data || !data.length)) {
        $('.message', _dom).first().text(i18n.t('customInputs:IdentifierField.errors.exactly_one'));
        return false;
      }

      for (k in _linesHash)
        _linesHash[k].forEach(function(comp) {
          var isValid =
            comp.validate ?
              comp.validate() :
              blf.modules.createPanel.defaultMethods.validate.call(comp);

          if (!isValid)
            invalid++;
        });

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
      ((data || {}).children || []).forEach(addDocument);
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
            id = li.data('id');

        documents.push({
          rec_type: $('select.select-field', li).first().val(),
          document: _linesHash[id].reduce(function(res, comp) {
            value = comp.getData ?
              comp.getData() :
              blf.modules.createPanel.defaultMethods.getData.call(comp);

            res[comp.property] = value;
            return res;
          }, {})
        });
      });

      return documents.length ? {
        children: documents
      } : undefined;
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
