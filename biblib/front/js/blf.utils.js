;(function() {
  'use strict';

  // Handlebars helpers:
  Handlebars.registerHelper('t', function(i18n_key) {
    var result = i18n.t(i18n_key);
    return new Handlebars.SafeString(result);
  });

  Handlebars.registerHelper('ifCond', function(v1, operator, v2, options) {
    switch (operator) {
      case '==':
        return (v1 == v2) ? options.fn(this) : options.inverse(this);
      case '===':
        return (v1 === v2) ? options.fn(this) : options.inverse(this);
      case '<':
        return (v1 < v2) ? options.fn(this) : options.inverse(this);
      case '<=':
        return (v1 <= v2) ? options.fn(this) : options.inverse(this);
      case '>':
        return (v1 > v2) ? options.fn(this) : options.inverse(this);
      case '>=':
        return (v1 >= v2) ? options.fn(this) : options.inverse(this);
      default:
        return options.inverse(this);
    }
  });

  // Some specific utils:
  mlab.pkg('blf.utils');
  mlab.pkg('blf.templates');
  (function() {
    var _templates = {};

    function loadTemplate(path, callback) {
      if (!_templates[path])
        $.ajax({
          url: 'templates/' + path + '.handlebars',
          success: function(data) {
            _templates[path] = Handlebars.compile(data);
            if (callback)
              callback(_templates[path]);
          }
        });
      else if (callback)
        callback(_templates[path]);
    };

    blf.templates.require = function(v, callback) {
      if (typeof v === 'string')
        loadTemplate(v, callback);
      else
        for (var k in v)
          loadTemplate(v[k]);
    };

    blf.templates.get = function(path) {
      return _templates[path];
    };
  })();

  blf.utils.translateLabels = function(obj) {
    var k,
        i,
        l,
        res = {};

    obj = obj;
    if (domino.struct.check('object', obj))
      for (k in obj) {
        if (k === 'labels')
          res.label = obj[k][blf.config.lang];
        else if (domino.struct.check('array', obj[k]))
          res[k] = obj[k].map(blf.utils.translateLabels);
        else if (domino.struct.check('object', obj[k]))
          res[k] = blf.utils.translateLabels(obj[k]);
        else
          res[k] = obj[k];
      }
    else if (domino.struct.check('array', obj))
      res = obj.map(blf.utils.translateLabels);
    else
      res = obj;

    return res;
  };
})();
