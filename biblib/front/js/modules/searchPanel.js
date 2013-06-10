;(function() {
  'use strict';

  mlab.pkg('blf.modules');

  blf.modules.searchPanel = function(html) {
    domino.module.call(this);

    var _self = this,
        _html = html;

    $('input.advanced-search', _html).change(function() {
      if ($(this).is(':checked')) {
        $('.advanced-search-panel', _html).attr('hidden', null);
        $('.normal-search', _html).attr('disabled', 'true');
      } else {
        $('.advanced-search-panel', _html).attr('hidden', 'true');
        $('.normal-search', _html).attr('disabled', null);
      }
    });
  };
})();
