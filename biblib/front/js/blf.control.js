$(document).ready(function() {
  'use strict';

  // Package "blf": BibLib Front
  mlab.pkg('blf');

  // Initialize lang and other global assets:
  mlab.pkg('blf.assets');
  blf.assets.lang = 'en';
  blf.assets.languages = [
    {
      id: 'fr',
      labels: {
        fr: 'Français',
        en: 'French'
      }
    },
    {
      id: 'en',
      labels: {
        fr: 'Anglais',
        en: 'English'
      }
    }
  ];

  // Domino global settings:
  domino.settings({
    displayTime: true,
    verbose: true,
    strict: true
  });

  /**
   * First, let's describe our data here. To add a new type, just use:
   *
   *  > if (!domino.struct.isValid('blf.typeTest'))
   *  >   domino.struct.add({
   *  >     id: 'blf.typeTest',
   *  >     struct: {
   *  >       key1: 'string',
   *  >       key2: '?number'
   *  >     }
   *  >   });
   */
  if (!domino.struct.isValid('blf.Dict'))
    domino.struct.add({
      id: 'blf.Dict',
      struct: {
        fr: '?string',
        en: '?string'
      }
    });

  if (!domino.struct.isValid('blf.Property'))
    domino.struct.add({
      id: 'blf.Property',
      struct: {
        multiple: '?boolean',
        property: 'string',
        required: 'boolean',
        type_data: 'string',
        type_ui: 'string',
        labels: '?blf.Dict'
      }
    });

  if (!domino.struct.isValid('blf.Field'))
    domino.struct.add({
      id: 'blf.Field',
      struct: {
        rec_class: 'string',
        rec_type: 'string',
        children: [ 'blf.Property' ]
      }
    });

  if (!domino.struct.isValid('blf.FieldsIndex'))
    domino.struct.add({
      id: 'blf.FieldsIndex',
      struct: function(o) {
        var k, test;

        if (!domino.struct.check('object', o))
          return false;

        for (k in o)
          if (!domino.struct.check('blf.Field', o[k]))
            return false;

        return true;
      }
    });

  /**
   * Controler:
   */
  blf.control = new domino({
    name: 'blf.control',
    properties: [
      // DATA related properties
      {
        value: {},
        id: 'fields',
        type: 'blf.FieldsIndex',
        dispatch: 'fieldsUpdated',
        description: 'The field templates.'
      },
      {
        value: {},
        id: 'fieldsTree',
        type: 'object',
        dispatch: 'fieldsTreeUpdated',
        description: 'The fields tree.'
      },
      {
        value: [],
        id: 'creatorRoles',
        type: 'array',
        dispatch: 'creatorRolesUpdated',
        description: 'The creator roles list.'
      },

      // INTERFACE related properties
      {
        value: 'home',
        id: 'mode',
        force: true,
        type: 'string',
        description: 'The layout mode (home, search, create).'
      }
    ],
    hacks: [
      {
        // This hack is just useful to make the modules able to log, warn and
        // die trough domino:
        triggers: ['log', 'warn', 'die'],
        method: function(e) {
          this[e.type]((e.data || {}).message);
        }
      },
      {
        triggers: 'updateMode',
        description: 'Update the mode. Hack necessary because of domino.js issue #27.',
        method: function(e) {
          this.update('mode', e.data.mode);
          this.dispatchEvent('modeUpdated');
        }
      },
      {
        triggers: 'loadField',
        description: 'Loading the template of a specific field.',
        method: function(e) {
          this.request('loadField', {
            field: e.data.field
          });
        }
      },
      {
        triggers: 'validateEntry',
        description: 'What happens when an entry is validated from the form.',
        method: function(e) {
          console.log(e.data.entry);
        }
      }
    ],
    services: [
      {
        id: 'loadField',
        description: 'Loads the template of a specified field.',
        url: function(input) {
          return 'templates/' + input.field + '.json';
        },
        success: function(data) {
          var fields = this.get('fields');
          fields[data.rec_type] = data;
          this.update('fields', fields)
        }
      },
      {
        id: 'loadFieldsTree',
        url: 'assets/templates-tree_sample.json',
        setter: 'fieldsTree',
        description: 'Loads the dependance tree of the fields.'
      },
      {
        id: 'loadCreatorRoles',
        url: 'assets/creator-roles.json',
        setter: 'creatorRoles',
        path: 'children',
        description: 'Loads the list of the available creator roles.'
      }
    ]
  });

  // Layout initialization:
  blf.layout = blf.control.addModule(blf.modules.layout);

  // Data initialization:
  blf.control.request(['loadFieldsTree', 'loadCreatorRoles']);
});
