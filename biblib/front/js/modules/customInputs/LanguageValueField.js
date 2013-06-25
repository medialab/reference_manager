;(function() {
  'use strict';
  mlab.pkg('blf.modules.customInputs');

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

    _dom = $(
      '<fieldset class="customInput LanguageValueField">' +
        '<div class="message"></div>' +
        '<label>' +
          (obj.label || obj.labels[blf.assets.lang]) + ' :' +
        '</label>' +
        '<div class="languages-container container">' +
          '<ul class="languages-list"></ul>' +
          '<button class="add-language">+</button>' +
        '</div>' +
      '</fieldset>'
    );

    // Bind events:
    $('button.add-language', _dom).click(function() {
      addLanguage();
    });

    // Bind events:
    _dom.click(function(e) {
      var target = $(e.target),
          li = target.parents('ul.languages-list > li');

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
      var li = $(
        '<li>' +
          '<select class="select-language">' +
            _languages.map(function(o) {
              return (
                '<option value="' + o.id + '">' +
                  (o.label || o.labels[blf.assets.lang]) +
                '</option>'
              );
            }).join() +
          '</select>' +
          '<button class="remove-language">-</button>' +
          '<textarea class="col-6"></textarea>' +
        '</li>'
      );

      if (data.language)
        $('> select', li).val(data.language);

      // If the language is not specified, we use the first language that is
      // not used yet:
      else
        $('> select', li).val(_languages.reduce(function(res, lang) {
          return res !== null ?
            res :
            !$('select.select-language > option[value="' + lang.id + '"]:selected', _dom).length ?
              lang.id :
              null;
        }, null));


      if (data.value)
        $('> textarea', li).val(data.value);

      $('select', li).change(checkLanguagesDups);
      $('ul.languages-list', _dom).append(li);
      checkLanguagesCount();
      checkLanguagesDups();
    }

    // Check that all languages are not added yet:
    function checkLanguagesCount() {
      if ($('ul.languages-list > li', _dom).length >= _languages.length)
        $('button.add-language', _dom).attr('hidden', 'true');
      else
        $('button.add-language', _dom).attr('hidden', null);
    }

    // Deal with languages deduplication:
    function checkLanguagesDups() {
      var list = $('ul.languages-list > li > select', _dom);

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
        $('.message', this.dom).text('At least one language has to be added.');
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
