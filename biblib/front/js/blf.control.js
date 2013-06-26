$(document).ready(function() {
  'use strict';

  // Package "blf": BibLib Front
  mlab.pkg('blf');

  // Global vars:
  mlab.pkg('blf.global.rpc');

  blf.global.API_URL = 'http://localhost:8080/';
  blf.global.rpc.type = 'POST';
  blf.global.rpc.contentType = 'application/x-www-form-urlencoded';
  blf.global.rpc.expect = function(data) {
    return data !== null &&
      typeof data === 'object' &&
      !('error' in data);
  };
  blf.global.rpc.error = function(data) {
    this.log('Error:' + data);
  };
  blf.global.rpc.buildData = function(method, params) {
    return JSON.stringify({
      id: 1,
      jsonrpc: '2.0',
      method: method,
      params: params
    });
  };

  // Domino global settings:
  domino.settings({
    shortcutPrefix: '::',
    displayTime: true,
    verbose: true,
    strict: true
  });

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

  // Load dictionary:
  i18n.init({
    lng: 'fr',
    fallbackLng: 'en',
    ns: {
      namespaces: ['translation', 'customInputs'],
      defaultNs: 'translation'
    }
  }, function(t) {
    $('body').i18n();
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
      includes: true,
      struct: {
        fr: '?string',
        en: '?string'
      }
    });

  if (!domino.struct.isValid('blf.Property'))
    domino.struct.add({
      id: 'blf.Property',
      includes: true,
      struct: {
        multiple: '?boolean',
        property: 'string',
        required: 'boolean',
        type_data: '?string',
        type_ui: 'string',
        labels: '?blf.Dict',
        label: '?string'
      }
    });

  if (!domino.struct.isValid('blf.Field'))
    domino.struct.add({
      id: 'blf.Field',
      includes: true,
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
      includes: true,
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
        description: 'The list of fields that are already loaded.'
      },
      {
        value: {},
        id: 'availableFields',
        type: 'object',
        dispatch: 'availableFieldsUpdated',
        description: 'The list of existing and editable fields.'
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
      {
        value: {},
        id: 'lists',
        type: 'object',
        triggers: 'updateLists',
        dispatch: 'listsUpdated',
        description: 'The miscellaneous lists.'
      },

      // INTERFACE related properties
      {
        value: null,
        id: 'waitingEntry',
        type: '?object',
        triggers: 'updateWaitingEntry',
        dispatch: 'waitingEntryUpdated',
        description: 'An entry to edit, waiting for the field specifications to be loaded.'
      },
      {
        value: null,
        id: 'waitingField',
        type: '?string',
        triggers: 'updateWaitingField',
        dispatch: 'waitingFieldUpdated',
        description: 'A field that is being loaded.'
      },
      {
        value: 'home',
        id: 'mode',
        type: 'string',
        triggers: 'updateMode',
        dispatch: 'modeUpdated',
        description: 'The layout mode (home, search, create).'
      }
    ],
    hacks: [
      {
        triggers: 'validateEntry',
        description: 'What happens when an entry is validated from the form.',
        method: function(e) {
          this.dispatchEvent('displayForm', {
            entry: e.data.entry,
            field: e.data.entry.rec_type
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
        triggers: 'resultsListUpdated',
        description: 'Updates the mode to "list" when results are loaded.',
        method: function(e) {
          this.dispatchEvent('updateMode', {
            mode: 'list'
          });
        }
      },
      {
        triggers: 'loadList',
        description: 'Loads a specific list.',
        method: function(e) {
          this.request('type', {
            typeName: e.data.list
          });
        }
      },
      {
        triggers: 'loadField',
        description: 'Loads a specific field.',
        method: function(e) {
          this.request('field', {
            field: e.data.field
          });
        }
      },
      {
        triggers: 'editEntry',
        description: 'Loads the good field definition if needed and opens the edition panel for the related entry.',
        method: function(e) {
          var entry = e.data.entry,
              fields = this.get('fields');

          if (fields[entry.rec_type])
            this.dispatchEvent('displayForm', {
              entry: entry,
              field: entry.rec_type
            }).update('mode', 'create');
          else
            this.request('field', {
              field: entry.rec_type
            }).update('waitingEntry', entry);
        }
      },
      {
        triggers: 'fieldsUpdated',
        description: 'Check if there is a waiting entry when a field is loaded, and display it is the related field is loaded.',
        method: function(e) {
          var entry = this.get('waitingEntry'),
              field = this.get('waitingField'),
              fields = this.get('fields');

          if (entry && fields[entry.rec_type])
            this.dispatchEvent('displayForm', {
              entry: entry,
              field: entry.rec_type
            }).update({
              mode: 'create',
              waitingEntry: null
            });
          else if (field && fields[field])
            this.dispatchEvent('displayForm', {
              field: field
            }).update({
              mode: 'create',
              waitingField: null
            });
        }
      },
      {
        triggers: 'deleteEntry',
        description: 'Deletes the related entry.',
        method: function(e) {
          // TODO
        }
      },
      {
        triggers: 'clickField',
        description: 'Display the panel to create a new entry, with the related field.',
        method: function(e) {
          var field = e.data.field,
              fields = this.get('fields');

          this.update('mode', 'create');
          if (fields[field])
            this.dispatchEvent('displayForm', {
              field: field
            });
          else {
            this.update('waitingField', e.data.field);
            this.request('field', {
              field: e.data.field
            });
          }
        }
      }
    ],
    services: [
      // RPC services:
      {
        id: 'search',
        url: blf.global.API_URL,
        description: 'A service to search on existing entries.',
        type: blf.global.rpc.type,
        error: blf.global.rpc.error,
        expect: blf.global.rpc.expect,
        contentType: blf.global.rpc.contentType,
        data: function(input) {
          return blf.global.rpc.buildData('search', [ input.query ]);
        },
        success: function(data) {
          var results = JSON.parse(data.result);
          this.update('resultsList', results.records || []);
        }
      },
      {
        id: 'type',
        url: blf.global.API_URL,
        description: 'Loads the list of specified type.',
        type: blf.global.rpc.type,
        error: blf.global.rpc.error,
        expect: blf.global.rpc.expect,
        contentType: blf.global.rpc.contentType,
        data: function(input) {
          return blf.global.rpc.buildData('type', [ input.typeName, 'fr' ]);
        },
        success: function(data, input) {
          var results = JSON.parse(data.result);
          switch (input.typeName) {
            case 'document_type':
              // Find the list of available fields as well:
              var availableFields = {};
              (function recursiveParse(node, depth) {
                if (!node.bundle && !node.deprecated)
                  availableFields[node.type_id] = 1;

                if ((node.children || []).length)
                  node.children.forEach(recursiveParse);
              })(results);

              // Update:
              this.update({
                fieldsTree: results,
                availableFields: availableFields
              });
              break;
            default:
              var lists = this.get('lists');
              lists[input.typeName] = results.children || [];
              this.update('lists', lists);
              break;
          }
        }
      },
      {
        id: 'field',
        url: blf.global.API_URL,
        description: 'Loads one field specification.',
        type: blf.global.rpc.type,
        error: blf.global.rpc.error,
        expect: blf.global.rpc.expect,
        contentType: blf.global.rpc.contentType,
        data: function(input) {
          return blf.global.rpc.buildData('uifields', [ input.field, 'fr' ]);
        },
        success: function(data) {
          var result = JSON.parse(data.result),
              fields = this.get('fields');

          fields[result.rec_type] = result;
          this.update('fields', fields);
        }
      },
      {
        id: 'save',
        url: blf.global.API_URL,
        description: 'Loads one field specification.',
        type: blf.global.rpc.type,
        error: blf.global.rpc.error,
        expect: blf.global.rpc.expect,
        contentType: blf.global.rpc.contentType,
        data: function(input) {
          return blf.global.rpc.buildData('save', [ input.field, 'fr' ]);
        },
        success: function(data) {
          var result = JSON.parse(data.result),
              fields = this.get('fields');

          fields[result.rec_type] = result;
          this.update('fields', fields);
        }
      }
    ]
  });

  // Layout initialization:
  blf.layout = blf.control.addModule(blf.modules.layout);

  // Data initialization:
  blf.control.request([
    {
      service: 'type',
      typeName: 'creator_role'
    },
    {
      service: 'type',
      typeName: 'document_type'
    }
  ]);
});
