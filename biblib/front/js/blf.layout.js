;(function() {
  'use strict';

  mlab.pkg('blf.modules');

  blf.modules.layout = function() {
    domino.module.call(this);

    var _self = this,
        _html = $('#layout'),
        _buttons = $('#nav', _html),
        _panels = $('#panels', _html),
        _modules = [];

    // Bind actions:
    $('button[data-action]', _buttons).click(function() {
      _self.dispatchEvent('updateMode', {
        mode: $(this).data('action')
      });
    });

    // Initialize other modules:
    _modules.push(blf.control.addModule(
      blf.modules.createPanel,
      [ $('[data-panel="create"]', _panels) ]
    ));

    _modules.push(blf.control.addModule(
      blf.modules.searchPanel,
      [ $('[data-panel="search"]', _panels) ]
    ));

    _modules.push(blf.control.addModule(
      blf.modules.listPanel,
      [ $('[data-panel="list"]', _panels) ]
    ));

    // Listen to the controller:
    this.triggers.events.modeUpdated = function(d) {
      var mode = d.get('mode');
      $('[data-panel]:not([data-panel="' + mode + '"])', _panels).attr('hidden', 'true');
      $('[data-panel="' + mode + '"]', _panels).attr('hidden', null);
    };
  };
})();
