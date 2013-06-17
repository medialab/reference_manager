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
        _lineID = 1,
        _linesHash = {},
        _classTemplates,
        _creatorRoles = d.get('lists').creator_role || [];

    _dom = $(
      '<fieldset class="customInput CreatorField">' +
        '<div class="message"></div>' +
        '<label>' +
          (obj.label || obj.labels[blf.assets.lang]) + ' :' +
        '</label>' +
        '<div class="creators-container container">' +
          '<ul class="creators-list"></ul>' +
          '<button class="add-creator">+</button>' +
        '</div>' +
      '</fieldset>'
    );

    // Add a line. The line is empty (ie to be filled by the user) if data is
    // not specified.
    function addCreator(data) {
      data = data || {};
      var id = _lineID++,
          li = $(
            '<li data-id="' + id + '">' +
              '<select class="col-3 select-type">' +
                // TODO:
                // Set this in assets, find it automatically as well.
                '<option value="Person">Person</option>' +
                '<option value="Orgunit">Orgunit</option>' +
                '<option value="Event">Event</option>' +
              '</select>' +
              '<select class="col-3 select-role">' +
                // Find the roles through the global controler:
                _creatorRoles.map(function(o) {
                  return '<option value="' + o.type_id + '">' + (o.label || o.labels[blf.assets.lang]) + '</option>';
                }).join() +
              '</select>' +
              '<button class="remove-creator">-</button>' +
              '<button class="moveup-creator">↑</button>' +
              '<button class="movedown-creator">↓</button>' +
              '<div class="col-6 custom-container">' +
              '</div>' +
            '</li>'
          );

      var agent = data.agent || {};
      if (data.role)
        $('> select.select-role', li).val(data.role);

      _linesHash[id] = _classTemplates(agent.rec_class || 'Person');
      $('.custom-container', li).append(_linesHash[id].dom);

      if (agent.rec_class) {
        $('> select.select-type', li).val(agent.rec_class);
        _linesHash[id].fill(data, _linesHash[id]);
      }

      $('ul.creators-list', _dom).append(li);
    }

    // Class templates:
    _classTemplates = function(c) {
      var o = {
        Person: {
          dom: $(
            '<fieldset>' +
              '<label class="col-3">Nom :</label>' +
              '<input data-attribute="name_family" class="col-3" type="text" />' +
            '</fieldset>' +
            '<fieldset>' +
              '<label class="col-3">Prénom :</label>' +
              '<input data-attribute="name_given" class="col-3" type="text" />' +
            '</fieldset>' +
            '<fieldset>' +
              '<label class="col-3">Année de naissance :</label>' +
              '<input data-attribute="date_birth" class="col-3" type="year" />' +
            '</fieldset>' +
            '<fieldset>' +
              '<label class="col-3">Année de décès :</label>' +
              '<input data-attribute="date_death" class="col-3" type="year" />' +
            '</fieldset>' +
            '<fieldset>' +
              '<label class="col-3">Affiliation :</label>' +
              '<input data-attribute="affiliation" class="col-3" type="text" />' +
            '</fieldset>'
          ),
          fill: function(data, obj) {
            $('input[data-attribute="name_family"]', obj.dom).val(data.agent.name_family);
            $('input[data-attribute="name_given"]', obj.dom).val(data.agent.name_given);
            $('input[data-attribute="date_birth"]', obj.dom).val(data.agent.date_birth);
            $('input[data-attribute="date_death"]', obj.dom).val(data.agent.date_death);

            $('input[data-attribute="affiliation"]', obj.dom).val((data.affiliation || {}).name);
            return this;
          },
          getData: function(data, obj) {
            data.agent = data.agent || {
              rec_class: 'Person',
              rec_metajson: 1
            };

            data.agent.name_family = $('input[data-attribute="name_family"]', obj.dom).val();
            data.agent.name_given = $('input[data-attribute="name_given"]', obj.dom).val();
            data.agent.date_birth = $('input[data-attribute="date_birth"]', obj.dom).val();
            data.agent.date_death = $('input[data-attribute="date_death"]', obj.dom).val();

            var aff = $('input[data-attribute="affiliation"]', obj.dom).val();
            if (aff)
              data.affiliation = {
                rec_class: 'Orgunit',
                rec_metajson: 1,
                name: aff
              };

            return data;
          }
        },
        Orgunit: {
          dom: $(
            '<fieldset>' +
              '<label class="col-3">Nom :</label>' +
              '<input data-attribute="name" class="col-3" type="text" />' +
            '</fieldset>'
          ),
          fill: function(data, obj) {
            $('input[data-attribute="name"]', obj.dom).val(data.agent.name);
            return this;
          },
          getData: function(data, obj) {
            data.agent = data.agent || {
              rec_class: 'Orgunit',
              rec_metajson: 1
            };

            data.agent.name = $('input[data-attribute="name"]', obj.dom).val();

            return data;
          }
        },
        Event: {
          dom: $(
            '<fieldset>' +
              '<label class="col-3">Titre :</label>' +
              '<input data-attribute="title" class="col-3" type="text" />' +
            '</fieldset>' +
            '<fieldset>' +
              '<label class="col-3">Numéro :</label>' +
              '<input data-attribute="number" class="col-3" type="number" />' +
            '</fieldset>' +
            '<fieldset>' +
              '<label class="col-3">International :</label>' +
              '<input data-attribute="international" class="col-3" type="checkbox" />' +
            '</fieldset>' +
            '<fieldset>' +
              '<label class="col-3">Ville :</label>' +
              '<input data-attribute="place" class="col-3" type="text" />' +
            '</fieldset>' +
            '<fieldset>' +
              '<label class="col-3">Pays :</label>' +
              '<input data-attribute="country" class="col-3" type="text" />' +
            '</fieldset>' +
            '<fieldset>' +
              '<label class="col-3">Date de début :</label>' +
              '<input data-attribute="date_start" class="col-3" type="date" />' +
            '</fieldset>' +
            '<fieldset>' +
              '<label class="col-3">Date de fin :</label>' +
              '<input data-attribute="date_end" class="col-3" type="date" />' +
            '</fieldset>'
          ),
          fill: function(data, obj) {
             ('input[data-attribute="title"]', obj.dom).val(data.agent.title);
             ('input[data-attribute="number"]', obj.dom).val(data.agent.number);
             ('input[data-attribute="place"]', obj.dom).val(data.agent.place);
             ('input[data-attribute="country"]', obj.dom).val(data.agent.country);
             ('input[data-attribute="date_start"]', obj.dom).val(data.agent.date_start);
             ('input[data-attribute="date_end"]', obj.dom).val(data.agent.date_end);
             ('input[data-attribute="international"]', obj.dom).attr('checked', data.agent.international ? 'checked' : null);
             return this;
          },
          getData: function(data, obj) {
            data.agent = data.agent || {
              rec_class: 'Event',
              rec_metajson: 1
            };

            data.agent.title = $('input[data-attribute="title"]', obj.dom).val();
            data.agent.number = $('input[data-attribute="number"]', obj.dom).val();
            data.agent.place = $('input[data-attribute="place"]', obj.dom).val();
            data.agent.country = $('input[data-attribute="country"]', obj.dom).val();
            data.agent.date_start = $('input[data-attribute="date_start"]', obj.dom).val();
            data.agent.date_end = $('input[data-attribute="date_end"]', obj.dom).val();
            data.agent.international = !!$('input[data-attribute="international"]', obj.dom).is(':checked');

            return data;
          }
        }
      };

      return o[c];
    };

    // Bind events:
    $('button.add-creator', _dom).click(function() {
      addCreator();
    });

    _dom.click(function(e) {
      var target = $(e.target),
          li = target.parents('ul.creators-list > li');

      // Check if it is a field button:
      if (li.length && target.is('button.remove-creator')) {
        var id = li.data('id');
        li.remove();
        delete _linesHash[id];
      } else if (li.length && target.is('button.moveup-creator')) {
        if (!li.is(':first-child'))
          li.prev().before(li);
      } else if (li.length && target.is('button.movedown-creator')) {
        if (!li.is(':last-child'))
          li.next().after(li);
      }
    }).change(function(e) {
      var target = $(e.target),
          li = target.parents('ul.creators-list > li');

      // Check which select it is:
      if (li.length && target.is('select.select-type')) {
        var id = li.data('id'),
            value = target.val(),
            container = $('.custom-container', li);

        _linesHash[id] = _classTemplates(value);
        container.empty().append(_linesHash[id].dom);
      }
    });

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
        var li = $(this),
            id = li.data('id');

        creators.push(_linesHash[id].getData({
          role: $('> select', li).val(),
          agents: {}
        }), _linesHash[id]);
      });

      return creators.length ? creators : undefined;
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
    this.triggers.events.creatorRolesUpdated = function(d) {
      _creatorRoles = d.get('creatorRoles') || [];

      $('select.select-role', dom).html(
        _creatorRoles.map(function(o) {
          return '<option value="' + o.type_id + '">' + (o.label || o.labels[blf.assets.lang]) + '</option>';
        }).join()
      );
    };
  };
})();
