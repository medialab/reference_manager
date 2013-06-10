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
        '<label>' + obj.labels[blf.assets.lang] + ' :</label>' +
        '<div class="creators-container">' +
          '<ul class="creators-list"></ul>' +
          '<button class="add-creator">+</button>' +
        '</div>' +
      '</fieldset>'
    );

    // Bind events:
    $('button.add-creator', _dom).click(function() {
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
              return '<option value="' + o.type_id + '">' + o.labels[blf.assets.lang] + '</option>';
            }).join() +
          '</select>' +
          '<button class="remove-creator">-</button>' +
          '<button class="moveup-creator">↑</button>' +
          '<button class="movedown-creator">↓</button>' +
        '</li>'
      );

      li.click(function(e) {
        var dom = $(e.target);

        // Check if it is a field button:
        if (dom.is('button.remove-creator')) {
          li.remove();
        } else if (dom.is('button.moveup-creator')) {
          if (!li.is(':first-child'))
            li.prev().before(li);
        } else if (dom.is('button.movedown-creator')) {
          if (!li.is(':last-child'))
            li.next().after(li);
        }
      });

      $('ul.creators-list', _dom).append(li);
    });

    this.triggers.events.creatorRolesUpdated = function(d) {
      _creatorRoles = d.get('creatorRoles') || [];

      $('select.select-role', dom).html(
        _creatorRoles.map(function(o) {
          return '<option value="' + o.type_id + '">' + o.labels[blf.assets.lang] + '</option>';
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
      // TODO: Check empty lines and required.
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
      (data || []).forEach(function(creator) {
        li = $(
          '<li>' +
            '<input class="col-4" type="text" placeholder="Type something..." />' +
            '<select class="col-2" class="select-role">' +
              // Find the roles through the global controler:
              _creatorRoles.map(function(o) {
                return '<option value="' + o.type_id + '">' + o.labels[blf.assets.lang] + '</option>';
              }).join() +
            '</select>' +
            '<button class="remove-creator">-</button>' +
            '<button class="moveup-creator">↑</button>' +
            '<button class="movedown-creator">↓</button>' +
          '</li>'
        ).appendTo(ul);

        $('> select', li).val(creator.role);
        // TODO
      });
    }

    /**
     * Returns the well-formed data described by the component.
     *
     * @return {*} The data.
     */
    function _get() {
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
        getData: _get,
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
        '<label>' + obj.labels[blf.assets.lang] + ' :</label>' +
        '<div class="languages-container">' +
          '<ul class="languages-list"></ul>' +
          '<button class="add-language">+</button>' +
        '</div>' +
      '</fieldset>'
    );

    // Bind events:
    $('button.add-language', _dom).click(function() {
      if ($('ul.languages-list > li', _dom).length >= _languages.length)
        return;

      var isAlreadySelected = false,
          li = $(
            '<li>' +
              '<select>' +
                _languages.map(function(o) {
                  var selected = '';

                  if (!isAlreadySelected && !_selected[o.id]) {
                    selected = ' selected="true"'
                    isAlreadySelected = true;
                  }

                  return (
                    '<option value="' + o.id + '"' + selected + '>' +
                      o.labels[blf.assets.lang] +
                    '</option>'
                  );
                }).join() +
              '</select>' +
              '<button class="remove-language">-</button>' +
              '<textarea class="col-6"></textarea>' +
            '</li>'
          );

      $('button.remove-language', li).click(function() {
        li.remove();
        checkLanguagesCount();
        checkLanguagesDups();
      });

      $('select', li).change(checkLanguagesDups);

      $('ul.languages-list', _dom).append(li);
      checkLanguagesCount();
      checkLanguagesDups();
    });

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
      // TODO: Check empty lines and required.
      return true;
    }

    /**
     * Fill the component with existing data.
     *
     * @param  {object} data The data to display in the component.
     * @param  {object} full The full entry (sometimes might be needed).
     */
    function _fill(data) {
      // TODO
    }

    /**
     * Returns the well-formed data described by the component.
     *
     * @return {*} The data.
     */
    function _get() {
      // TODO
    }

    this.getComponent = function() {
      return {
        dom: _dom,
        fill: _fill,
        getData: _get,
        validate: _validate,
        propertyObject: obj,
        property: obj.property
      };
    };
  };
})();
