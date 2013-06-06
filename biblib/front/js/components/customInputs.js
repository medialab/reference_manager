;(function() {
  'use strict';

  mlab.pkg('blf.customInputs');

  /**
   * This custom input represents the creators of an entry. It is possible to
   * add several creators. Each creator is categorized by a name (string), a
   * role (huge external list) and a class ("Person", "Orgunit" or "Event").
   *
   * Use case:
   * *********
   *  > new blf.customInputs.Creator({
   *  >   labels: {
   *  >       en: "Creators",
   *  >       fr: "Créateurs"
   *  >   },
   *  >   multiple: true,
   *  >   property: "creators",
   *  >   required: true,
   *  >   type_data: "Creator",
   *  >   type_ui: "CreatorField"
   *  > });
   */
  blf.customInputs.Creator = function(obj) {
    var _dom,
        _validate;

    _dom = $(
      '<fieldset>' +
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
          '<input type="text" placeholder="Type something..." />' +
          '<select>' +
            '<option value="lorem">Lorem</option>' +
            '<option value="ipsum">Ipsum</option>' +
          '</select>' +
          '<button class="remove-creator">-</button>' +
        '</li>'
      );
      $('button.remove-creator', li).click(function() {
        li.remove();
      });

      $('ul.creators-list', _dom).append(li);
    });

    return {
      dom: _dom,
      validate: _validate
    };
  };

  /**
   * This custom input can be used to add several entries for different
   * languages.
   *
   * Use case:
   * *********
   *  > new blf.customInputs.LanguageValue({
   *  >   labels: {
   *  >       en: "Abstracts",
   *  >       fr: "Resumés"
   *  >   },
   *  >   multiple: true,
   *  >   property: "descriptions",
   *  >   required: false,
   *  >   type_data: "LanguageValue",
   *  >   type_ui: "LanguageValueField"
   *  > });
   */
  blf.customInputs.LanguageValue = function(obj) {
    var _dom,
        _validate,
        _selected = {},
        _languages = blf.assets.languages;

    _dom = $(
      '<fieldset>' +
        '<label>' + obj.labels[blf.assets.lang] + ' :</label>' +
        '<div class="languages-container">' +
          '<ul class="languages-list"></ul>' +
          '<button class="add-creator">+</button>' +
        '</div>' +
      '</fieldset>'
    );

    // Bind events:
    $('button.add-creator', _dom).click(function() {
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
              '<button class="remove-creator">-</button>' +
              '<textarea rows="3" cols="30"></textarea>' +
            '</li>'
          );

      $('button.remove-creator', li).click(function() {
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
        $('button.add-creator', _dom).attr('hidden', 'true');
      else
        $('button.add-creator', _dom).attr('hidden', null);
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

    return {
      dom: _dom,
      validate: _validate
    };
  };
})();
