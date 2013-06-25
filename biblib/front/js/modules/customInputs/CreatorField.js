;(function() {
  'use strict';
  mlab.pkg('blf.modules.customInputs');

  // Loading Handlebars templates:
  var _templates = {
        main: {
          path: 'templates/CreatorField.handlebars'
        },
        line: {
          path: 'templates/CreatorField.line.handlebars'
        },
        roles: {
          path: 'templates/CreatorField.roles.handlebars'
        },
        person: {
          path: 'templates/CreatorField.Person.handlebars'
        },
        orgunit: {
          path: 'templates/CreatorField.Orgunit.handlebars'
        },
        event: {
          path: 'templates/CreatorField.Event.handlebars'
        }
      };

  for (var k in _templates)
    (function(obj) {
      blf.utils.addTemplate(obj.path, function(data) {
        obj.template = data;
      });
    })(_templates[k]);

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

    _dom = $(_templates.main.template({
      label: obj.label || obj.labels[blf.assets.lang]
    }));

    // Add a line. The line is empty (ie to be filled by the user) if data is
    // not specified.
    function addCreator(data) {
      data = data || {};
      var id = _lineID++,
          li = $(_templates.line.template({
            id: id,
            creators: _creatorRoles.map(function(o) {
              return {
                type_id: o.type_id,
                label: o.label || o.labels[blf.assets.lang]
              };
            })
          }));

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
          dom: $(_templates.person.template()),
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
          dom: $(_templates.orgunit.template()),
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
          dom: $(_templates.event.template()),
          fill: function(data, obj) {
             $('input[data-attribute="title"]', obj.dom).val(data.agent.title);
             $('input[data-attribute="number"]', obj.dom).val(data.agent.number);
             $('input[data-attribute="place"]', obj.dom).val(data.agent.place);
             $('input[data-attribute="country"]', obj.dom).val(data.agent.country);
             $('input[data-attribute="date_start"]', obj.dom).val(data.agent.date_start);
             $('input[data-attribute="date_end"]', obj.dom).val(data.agent.date_end);
             $('input[data-attribute="international"]', obj.dom).attr('checked', data.agent.international ? 'checked' : null);
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
        $('.message', this.dom).text(i18n.t('customInputs:CreatorField.errors.at_least_one'));
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
        }, _linesHash[id]));
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
          return _templates.roles.template({
            type_id: o.type_id,
            label: o.label
          });
        })
      );
    };
  };
})();
