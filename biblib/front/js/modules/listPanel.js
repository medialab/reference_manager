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

    _html.click(function(e) {
      var target = $(e.target),
          li = target.parents('ul > li');

      // Check if it is an openable post:
      if (li.length && target.is('a.entry-title')) {
        console.log('clicked openable result');
        e.stopPropagation();
        return false;
      }
    });

    function restart() {
      $('> ul', _html).empty();
    }

    function fill(d) {
      restart();

      var fields = d.get('availableFields'),
          ul = $('> ul', _html).empty();

      _list.forEach(function(o) {
        var editable = fields[o.rec_type];

        ul.append(
          '<li data-id="' + o._id.$oid + '">' +
            '<span class="entry-type">' + o.rec_type + '</span> - ' +
            (editable ? '<a href="#" class="entry-title">' : '<span class="entry-title">') +
              o.title +
            (editable ? '</a>' : '</span>') +
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
      fill(d);
    };
  };
})();
