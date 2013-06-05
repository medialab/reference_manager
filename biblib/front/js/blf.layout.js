;(function() {
  'use strict';

  // Package "blf": BibLib Front
  mlab.pkg('blf.modules');

  blf.modules.layout = function() {
    domino.module.call(this);

    var _self = this,
        _html = $('#layout'),
        _buttons = $('#nav', _html),
        _panels = $('#panels', _html);

    // Bind actions:
    $('button[data-action]', _buttons).click(function() {
      _self.dispatchEvent('updateMode', {
        mode: $(this).data('action')
      });
    });

    // Listen to the controller:
    this.triggers.events.modeUpdated = function(d) {
      var mode = d.get('mode');
      $('[data-panel]:not([data-panel="' + mode + '"])', _panels).attr('hidden', 'true');
      $('[data-panel="' + mode + '"]', _panels).attr('hidden', null);
    };
  };
})();
