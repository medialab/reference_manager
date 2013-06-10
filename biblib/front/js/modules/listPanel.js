;(function() {
  'use strict';

  mlab.pkg('blf.modules');

  /**
   * The list panel, to display a list of entries abstracts.
   */
  blf.modules.listPanel = function(html) {
    domino.module.call(this);

    var _list,
        _self = this,
        _html = html;

    function restart() {
      $('> ul', _html).empty();
    }

    function fill() {
      restart();

      var ul = $('> ul', _html);
      _list.forEach(function(o) {
        ul.append(
          '<li data-id="' + o._id.$oid + '">' +
            '[' + o.rec_type + '] ' + o.title +
          '</li>'
        );
      });
    }

    /**
     * DOMINO BINDINGS:
     * ****************
     */
    // Listen to the controller:
    this.triggers.events.modeUpdated = function(d) {
      if (d.get('mode') !== 'list')
        restart();
    };

    // Display a list of abstracts:
    this.triggers.events.resultsListUpdated = function(d) {
      _list = d.get('resultsList');
      fill();
    };
  };
})();
