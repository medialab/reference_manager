;(function() {
  'use strict';
  mlab.pkg('blf.modules.customInputs');

  // Loading Handlebars templates:
  var _templates = {
        main: {
          path: 'templates/LanguageValueField.handlebars'
        },
        line: {
          path: 'templates/LanguageValueField.line.handlebars'
        }
      };

  (function() {
    for (var k in _templates)
      (function(obj) {
        blf.utils.addTemplate(obj.path, function(data) {
          obj.template = data;
        });
      })(_templates[k]);
  })();

  /**
   * This custom input can be used to add several entries for different
   * languages.
   *
   * Data sample:
   * ************
   *
   *  > {
   *  >   labels: {
   *  >       en: "Abstracts",
   *  >       fr: "Resumés"
   *  >   },
   *  >   multiple: true,
   *  >   property: "descriptions",
   *  >   required: false,
   *  >   type_data: "LanguageValue",
   *  >   type_ui: "LanguageValueField"
   *  > }
   */
  blf.modules.customInputs.LanguageValueField = function(obj) {
    domino.module.call(this);

    var _dom,
        _selected = {},
        _languages = blf.assets.languages;

    _dom = $(_templates.main.template({
      label: obj.label || obj.labels[blf.assets.lang]
    }));

    // Bind events:
    $('button.add-language', _dom).click(function() {
      addLanguage();
    });

    // Bind events:
    _dom.click(function(e) {
      var target = $(e.target),
          li = target.parents('li');

      // Check if it is a field button:
      if (li.length && target.is('button.remove-language')) {
        li.remove();
        checkLanguagesCount();
        checkLanguagesDups();
      }
    });

    // Add a line. The line is empty (ie to be filled by the user) if data is
    // not specified.
    function addLanguage(data) {
      data = data || {};
      var li = $(_templates.line.template({
        languages: _languages.map(function(o) {
          return {
            id: o.id,
            label: o.label || o.labels[blf.assets.lang]
          };
        })
      }));

      if (data.language)
        $('select.select-language', li).val(data.language);

      // If the language is not specified, we use the first language that is
      // not used yet:
      else
        _languages.some(function(lang) {
          if (!$('option[value="' + lang.id + '"]:selected', _dom).length)
            return $('select.select-language', li).val(lang.id);
        }, null);


      if (data.value)
        $('textarea', li).val(data.value);

      $('select.select-language', li).change(checkLanguagesDups);
      $('ul.languages-list', _dom).append(li);
      checkLanguagesCount();
      checkLanguagesDups();
    }

    // Check that all languages are not added yet:
    function checkLanguagesCount() {
      if ($('li', _dom).length >= _languages.length)
        $('button.add-language', _dom).attr('hidden', 'true');
      else
        $('button.add-language', _dom).attr('hidden', null);
    }

    // Deal with languages deduplication:
    function checkLanguagesDups() {
      var list = $('select.select-language', _dom);

      // Find selected languages:
      _selected = {};
      list.each(function() {
        _selected[$(this).val()] = 1;
      });

      // Disable selected languages:
      list.each(function() {
        var val = $(this).val();
        $(this).find('option').each(function() {
          var opt = $(this);
          if (opt.is(':selected') || !_selected[opt.val()])
            opt.attr('disabled', null);
          else
            opt.attr('disabled', 'true');
        });
      });
    }

    /**
     * Check if the content of the component is valid. Returns true if valid,
     * and false if not.
     *
     * @return {string} Returns true if the content id valid, and false else.
     */
    function _validate() {
      var data = _getData();

      if (obj.required && (!data || !data.length)) {
        $('.message', this.dom).text(i18n.t('customInputs:LanguageValueField.errors.at_least_one'));
        return false;
      }

      $('.message', this.dom).empty();
      return true;
    }

    /**
     * Fill the component with existing data.
     *
     * @param  {object} data The data to display in the component.
     * @param  {object} full The full entry (sometimes might be needed).
     */
    function _fill(data) {
      var li,
          ul = $('ul.languages-list', _dom).empty();

      // Parse data and create lines:
      (data || []).forEach(addLanguage);
    }

    /**
     * Returns the well-formed data described by the component.
     *
     * @return {*} The data.
     */
    function _getData() {
      var languages = [];

      // Parse line and form data:
      $('ul.languages-list > li', _dom).each(function() {
        var li = $(this);

        languages.push({
          language: $('> select', li).val(),
          value: $('> textarea', li).val()
        });
      });

      return languages.length ? languages : undefined;
    }

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
  };
})();
