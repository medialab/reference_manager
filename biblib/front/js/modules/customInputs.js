;(function() {
  'use strict';

  mlab.pkg('blf.modules.customInputs');

  /**
   * This custom input represents the creators of an entry. It is possible to
   * add several creators. Each creator is categorized by a name (string), a
   * role (huge external list) and a class ("Person", "Orgunit" or "Event").
   *
   * Data sample:
   * ************
   *
   *  > {
   *  >   labels: {
   *  >       en: "Creators",
   *  >       fr: "Créateurs"
   *  >   },
   *  >   multiple: true,
   *  >   property: "creators",
   *  >   required: true,
   *  >   type_data: "Creator",
   *  >   type_ui: "CreatorField"
   *  > }
   */
  blf.modules.customInputs.CreatorField = function(obj, d) {
    domino.module.call(this);

    var _dom,
        _creatorRoles = d.get('creatorRoles') || [];

    _dom = $(
      '<fieldset class="CreatorField">' +
        '<div class="message"></div>' +
        '<label>' +
          (obj.label || obj.labels[blf.assets.lang]) + ' :' +
        '</label>' +
        '<div class="creators-container">' +
          '<ul class="creators-list"></ul>' +
          '<button class="add-creator">+</button>' +
        '</div>' +
      '</fieldset>'
    );

    // Add a line. The line is empty (ie to be filled by the user) if data is
    // not specified.
    function addCreator(data) {
      data = data || {};
      var li = $(
        '<li>' +
          '<select class="col-1" class="select-type">' +
            // TODO:
            // Set this in assets, find it automatically as well.
            '<option value="person">Person</option>' +
            '<option value="orgunit">Orgunit</option>' +
            '<option value="event">Event</option>' +
          '</select>' +
          '<input class="col-3" type="text" placeholder="Type something..." />' +
          '<select class="col-2" class="select-role">' +
            // Find the roles through the global controler:
            _creatorRoles.map(function(o) {
              return '<option value="' + o.type_id + '">' + (o.label || o.labels[blf.assets.lang]) + '</option>';
            }).join() +
          '</select>' +
          '<button class="remove-creator">-</button>' +
          '<button class="moveup-creator">↑</button>' +
          '<button class="movedown-creator">↓</button>' +
        '</li>'
      );

      // TODO:
      // Fill every inputs
      if (data.role)
        $('> select', li).val(data.role);

      $('ul.creators-list', _dom).append(li);
    }

    // Bind events:
    _dom.click(function(e) {
      var target = $(e.target),
          li = target.parents('ul.creators-list > li');

      // Check if it is a field button:
      if (li.length && target.is('button.remove-creator')) {
        li.remove();
      } else if (li.length && target.is('button.moveup-creator')) {
        if (!li.is(':first-child'))
          li.prev().before(li);
      } else if (li.length && target.is('button.movedown-creator')) {
        if (!li.is(':last-child'))
          li.next().after(li);
      }
    });

    $('button.add-creator', _dom).click(function() {
      addCreator();
    });

    this.triggers.events.creatorRolesUpdated = function(d) {
      _creatorRoles = d.get('creatorRoles') || [];

      $('select.select-role', dom).html(
        _creatorRoles.map(function(o) {
          return '<option value="' + o.type_id + '">' + (o.label || o.labels[blf.assets.lang]) + '</option>';
        }).join()
      );
    };

    /**
     *  Check if the content of the component is valid. Returns true if valid,
     *  and false if not.
     *
     * @return {string} Returns true if the content id valid, and false else.
     */
    function _validate() {
      var data = _getData();

      if (obj.required && (!data || !data.length)) {
        $('.message', this.dom).text('At least one creator has to be specified.');
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
          ul = $('ul.creators-list', _dom).empty();

      // Parse data and create lines:
      (data || []).forEach(addCreator);
    }

    /**
     * Returns the well-formed data described by the component.
     *
     * @return {*} The data.
     */
    function _getData() {
      var creators = [];

      // Parse line and form data:
      $('ul.creators-list > li', _dom).each(function() {
        var li = $(this);

        creators.push({
          role: $('> select', li).val(),
          agents: {
            name_family: 'Power',   // TODO
            name_given: 'Michael',  // TODO
            rec_class: 'Person',    // TODO
            rec_metajson: 1
          }
        });
      });

      return creators.length ? creators : undefined;
    }

    /**
     * This method returns the component object.
     *
     * @return {objext} The component object.
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
  };

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
      '<fieldset class="LanguageValueField">' +
        '<div class="message"></div>' +
        '<label>' +
          (obj.label || obj.labels[blf.assets.lang]) + ' :' +
        '</label>' +
        '<div class="languages-container">' +
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

  /**
   * This custom input can be used to add parents entries. It can of course
   * a bit of madness when recursive parenting are used...
   *
   * Data sample:
   * ************
   *
   *  > // TODO
   */
  blf.modules.customInputs.IsPartOfField = function(obj) {
    domino.module.call(this);

    var _dom,
        _self = this;

    function _fill() {
      // TODO
    }

    function _getData() {
      // TODO
    }

    function _validate() {
      // TODO
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
