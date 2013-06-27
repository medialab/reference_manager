;(function() {
  'use strict';

  mlab.pkg('blf.modules');

  /**
   * The search panel, with two different modes (simple and advanced).
   */
  blf.modules.searchPanel = function(html) {
    domino.module.call(this);

    var _self = this,
        _html = html;

    $('input.advanced-search', _html).change(function() {
      if ($(this).is(':checked')) {
        $('.advanced-search-panel', _html).css('display', '');
        $('.normal-search', _html).attr('disabled', 'true');
      } else {
        $('.advanced-search-panel', _html).css('display', 'none');
        $('.normal-search', _html).attr('disabled', null);
      }
    });

    // TODO: Fix / remove this:
    $('input.advanced-search', _html).hide();
    $('label[for="use-advanced-search"]', _html).hide();

    $('button.validate', _html).click(search);

    function restart() {
      // Disable advanced search:
      var advCheckbox = $('input.advanced-search', _html);
      if (advCheckbox.is(':checked'))
        advCheckbox.attr('checked', null).change();

      // Reinitialize inputs:
      $('input', _html).val(null);
    }

    function search() {
      _self.dispatchEvent('search', {
        query: {
          'creators.agent.title': $('input.normal-search', _html).val()
        }
      });
    }

    /**
     * DOMINO BINDINGS:
     * ****************
     */
    // Listen to the controller:
    this.triggers.events.modeUpdated = function(d) {
      if (d.get('mode') === 'search')
        restart();
    };
  };
})();
