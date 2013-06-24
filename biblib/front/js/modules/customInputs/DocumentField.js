;(function() {
  'use strict';
  mlab.pkg('blf.modules.customInputs');

  /**
   * This custom input can be used to add parents entries. It can of course
   * a bit of madness when recursive parenting are used...
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

    var _dom = $(
          '<fieldset class="customInput DocumentField">' +
            '<div class="message"></div>' +
            '<label>' +
              (obj.label || obj.labels[blf.assets.lang]) + ' :' +
            '</label>' +
            '<div class="documents-container container">' +
              '<ul class="documents-list"></ul>' +
              '<button class="add-document">+</button>' +
            '</div>' +
          '</fieldset>'
        ),
        _ul = $('> div > ul', _dom),
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
          li = $(
            '<li data-id="' + id + '">' +
              '<select class="col-3 select-field">' +
                // Find the field through the global controler:
                obj.type_fields.map(function(o) {
                  return '<option value="' + o + '">' + o + '</option>';
                }).join() +
              '</select>' +
              '<button class="remove-document">-</button>' +
              '<div class="col-6 custom-container">' +
              '</div>' +
            '</li>'
          );

      if (data.rec_type) {
        $('> select.select-field', li).val(data.rec_type);

        _linesHash[id] = blf.modules.createPanel.generateForm(blf.control, _fields[data.rec_type]);
        $('> .custom-container', li).empty().append(_linesHash[id].map(function(o) {
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
      if (obj.only_one && $('> li', _ul).length >= 1)
        $('.add-document', _dom).attr('hidden', 'true');
      else
        $('.add-document', _dom).attr('hidden', null);

      // Trigger event if only one type available:
      if (!data.rec_type && obj.type_fields.length <= 1)
        $('> select.select-field', li).change();
    }

    // Bind events:
    $('button.add-document', _dom).click(function() {
      addDocument();
    });

    _dom.click(function(e) {
      var target = $(e.target),
          li = target.parents('ul.documents-list > li').first();

      // Check if it is a field button:
      if (li.length && target.is('button.remove-document')) {
        var id = li.data('id');
        li.remove();
        delete _linesHash[id];

        // Trigger event if only one type available:
        if (obj.type_fields.length <= 1)
          $('> select.select-field', li).change();

        // Check count:
        if (obj.only_one && $('> div > ul > li', _dom).length >= 1)
          $('.add-document', _dom).attr('hidden', 'true');
        else
          $('.add-document', _dom).attr('hidden', null);
      }
    }).change(function(e) {
      var target = $(e.target),
          li = target.parents('ul.documents-list > li').first();

      // Check which select it is:
      if (li.length && target.is($('> div > ul > li > select.select-field', _dom))) {
        var id = li.data('id'),
            value = target.val(),
            container = $('> .custom-container', li);

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

      $('.message', _dom).empty();

      if (obj.required && (!data || !data.length)) {
        $('.message', _dom).text('At least one document has to be specified.');
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
      $('> li', _ul).each(function() {
        var value,
            li = $(this),
            id = li.data('id');

        documents.push({
          rec_type: $('> select.select-field', li).val(),
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
      _fields = d.get('fields') || [];

      $('> li > select.select-field', _ul).html(
        obj.type_fields.filter(function(s) {
          return _fields[s];
        }).map(function(s) {
          var o = _fields[s];
          return '<option value="' + o.rec_type + '">' + o.rec_type + '</option>';
        }).join()
      );
    };
  };
})();
