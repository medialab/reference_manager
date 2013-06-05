$(document).ready(function() {
  'use strict';

  // Package "blf": BibLib Front
  mlab.pkg('blf');

  // Domino global settings:
  domino.settings({
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
  
  blf.controller = new domino({
    name: 'blf',
    properties: [
      {
        value: [],
        id: 'fields',
        type: ['blf.Field'],
        triggers: 'fieldsUpdated'
      }
    ],
    services: [
      {
        id: 'field',
        url: function(input) {
          return 'templates/' + input.field + '.json';
        },
        success: function(data) {
          var k,
              arr = this.get('fields');

          // If the "rec_type" already exists, it overrides the old one:
          if (mlab.array.index(this.get('fields'), 'rec_type')[data.rec_type])
            arr = arr.map(function(o) {
              return o.rec_type === data.rec_type ?
                data :
                o;
            });

          // If not, we just push it in our existing fields array:
          else
            arr.push(data);

          // Finally, we update:
          this.update('fields', arr);
        }
      }
    ]
  });

  // Initialization:
  blf.controller.request('field', {
    field: 'Book'
  });
});
