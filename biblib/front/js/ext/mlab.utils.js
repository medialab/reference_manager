;(function() {
  'use strict';
  window.mlab = window.mlab || {};

  /**
   * A useful function to deeply check whether a "namespace" exists yet, and
   * that creates it is not.
   *
   * Use case:
   * *********
   *
   *  > mlab.pkg('a.b.c');
   *  > // Is equivalent to:
   *  > window.a = window.a || {};
   *  > a.b = a.b || {}
   *  > a.b.c = a.b.c || {}
   *
   * @param  {string} str The path of the namespace, with "." to separe the
   *                      different parts of the path.
   * @return {object} Returns the related object.
   */
  mlab.pkg = function(str) {
    return str.split('.').reduce(function(o, s) {
      o[s] = o[s] || {};
      return o[s];
    }, window);
  };

  /**
   * Indexes an array on a specific key ("id", by default).
   *
   * Use case:
   * *********
   *
   *  > var o = mlab.array.index([
   *  >   {
   *  >     id: '1',
   *  >     content: 'abc'
   *  >   },
   *  >   {
   *  >     id: '2',
   *  >     content: 'def'
   *  >   }
   *  > ]);
   *  > // will return the following object:
   *  > // {
   *  > //   '1': {
   *  > //     id: '1'
   *  > //     content: 'abc'
   *  > //   },
   *  > //   '2': {
   *  > //     id: '2',
   *  > //     content: 'def'
   *  > //   }
   *  > // }
   *
   * @param  {array}   arr The array to index.
   * @param  {?string} key The key that will be used as index. If not
   *                       specified,
   * @return {object} Returns the object index.
   */
  mlab.pkg('mlab.array');
  mlab.array.index = function(arr, key) {
    arr = arr || [];
    key = key || 'id';

    return arr.reduce(function(res, obj) {
      res[obj[key]] = obj;
      return res
    }, {});
  };

  /**
   * The package mlab.rpc contains some recurring functions and constants to
   * facilitate RPC management with domino.js:
   */
  mlab.pkg('mlab.rpc');
  mlab.rpc.type = 'POST';
  mlab.rpc.contentType = 'application/x-www-form-urlencoded';
  mlab.rpc.expect = function(data) {
    return data !== null &&
      typeof data === 'object' &&
      !('error' in data);
  };
  mlab.rpc.error = function(data) {
    this.log('Error:' + data);
  };
})();
