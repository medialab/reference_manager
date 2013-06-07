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
        _validate;

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
          '<input class="col-2" type="text" placeholder="Type something..." />' +
          '<select class="col-1" class="select-role">' +
            // Find the roles through the global controler:
            (d.get('creatorRoles') || []).map(function(o) {
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
      $('select.select-role', dom).html(
        (d.get('creatorRoles') || []).map(function(o) {
          return '<option value="' + o.type_id + '">' + o.labels[blf.assets.lang] + '</option>';
        }).join()
      );
    };

    this.getComponent = function() {
      return {
        dom: _dom,
        validate: _validate
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
        _validate,
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
              '<textarea class="col-3"></textarea>' +
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

    this.getComponent = function() {
      return {
        dom: _dom,
        validate: _validate
      };
    };
  };
})();
