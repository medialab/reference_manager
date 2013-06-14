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
      var li = $(
        '<li>' +
          '<select class="col-1 select-type">' +
            // TODO:
            // Set this in assets, find it automatically as well.
            '<option value="person">Person</option>' +
            '<option value="orgunit">Orgunit</option>' +
            '<option value="event">Event</option>' +
          '</select>' +
          '<input class="col-3" type="text" placeholder="Type something..." />' +
          '<select class="col-2 select-role">' +
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
        $('> select.select-role', li).val(data.role);

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
  };
})();
