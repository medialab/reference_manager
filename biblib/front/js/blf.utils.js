;(function() {
  'use strict';

  // Some prestart hooks:
  Handlebars.registerHelper('t', function(i18n_key) {
    var result = i18n.t(i18n_key);
    return new Handlebars.SafeString(result);
  });

  // Some specific utils:
  mlab.pkg('blf.utils');
  blf.utils.addTemplate = function(path, callback) {
    $.ajax({
      url: path,
      success: function(data) {
        callback(Handlebars.compile(data));
      }
    });
  };
})();
