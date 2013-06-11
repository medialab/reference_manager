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
    shortcutPrefix: '::',
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
        _id: 'object',
        rec_type: 'string',
        rec_class: 'string',
        rec_metajson: 'number',
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
      {
        value: [],
        id: 'resultsList',
        type: 'array',
        triggers: 'updateResultsList',
        dispatch: 'resultsListUpdated',
        description: 'The results list.'
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
          this.request('field', {
            field: e.data.field
          });
        }
      },
      {
        triggers: 'validateEntry',
        description: 'What happens when an entry is validated from the form.',
        method: function(e) {
          this.dispatchEvent('displayEntry', {
            entry: e.data.entry,
            field: 'Book'
          });
        }
      },
      {
        triggers: 'search',
        description: 'Search for entries matching the specified query.',
        method: function(e) {
          this.request('search', {
            query: e.data.query
          });
        }
      },
      {
        triggers: ['resultsListUpdated'],
        description: 'Updates the mode to "list" when results are loaded.',
        method: function(e) {
          this.dispatchEvent('updateMode', {
            mode: 'list'
          });
        }
      }
    ],
    services: [
      // Test services (on static JSONS):
      {
        id: 'loadCreatorRoles',
        url: 'assets/creator-roles.json',
        setter: 'creatorRoles',
        path: 'children',
        description: 'Loads the list of the available creator roles.'
      },

      // RPC services:
      {
        id: 'echo',
        url: 'http://localhost\:8080',
        description: 'Just a test service to check if RPC works.',
        type: mlab.rpc.type,
        error: mlab.rpc.error,
        expect: mlab.rpc.expect,
        contentType: mlab.rpc.contentType,
        data: function(input) {
          return JSON.stringify({
            id: 1,
            jsonrpc: '2.0',
            method: 'echo',
            params: [
              input.message
            ]
          });
        },
        success: function(data) {
          this.log('ECHO FROM RPC', data.result);
        }
      },
      {
        id: 'search',
        url: 'http://localhost\:8080',
        description: 'A service to search on existing entries.',
        type: mlab.rpc.type,
        error: mlab.rpc.error,
        expect: mlab.rpc.expect,
        contentType: mlab.rpc.contentType,
        data: function(input) {
          return JSON.stringify({
            id: 1,
            jsonrpc: '2.0',
            method: 'search',
            params: [
              //input.query
              { rec_type: 'Book'} // /!\ HARD-CODED
            ]
          });
        },
        success: function(data) {
          var results = JSON.parse(data.result);
          this.log('SEARCH FROM RPC', results);

          this.update('resultsList', results);
        }
      },
      {
        id: 'type',
        url: 'http://localhost\:8080',
        description: 'Loads the dependance tree of the fields.',
        type: mlab.rpc.type,
        error: mlab.rpc.error,
        expect: mlab.rpc.expect,
        contentType: mlab.rpc.contentType,
        data: JSON.stringify({
          id: 1,
          jsonrpc: '2.0',
          method: 'type',
          params: [
            'document_type',
            'fr'
          ]
        }),
        success: function(data) {
          var results = JSON.parse(data.result);
          this.update('fieldsTree', results);
        }
      },
      {
        id: 'field',
        url: 'http://localhost\:8080',
        description: 'Loads one field specification.',
        type: mlab.rpc.type,
        error: mlab.rpc.error,
        expect: mlab.rpc.expect,
        contentType: mlab.rpc.contentType,
        data: function(input) {
          return JSON.stringify({
            id: 1,
            jsonrpc: '2.0',
            method: 'uifields',
            params: [
              input.field,
              'fr'
            ]
          });
        },
        success: function(data) {
          var result = JSON.parse(data.result),
              fields = this.get('fields');

          fields[result.rec_type] = result;
          this.update('fields', fields)
        }
      }
    ]
  });

  // Layout initialization:
  blf.layout = blf.control.addModule(blf.modules.layout);

  // Data initialization:
  blf.control.request(['type', 'loadCreatorRoles']);
});
