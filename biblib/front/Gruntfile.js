var findit = require('findit');
module.exports = function(grunt) {
  var jsFiles = [
    './js/ext/jquery.min.js',
    './js/ext/domino.min.js',
    './js/ext/i18next.min.js',
    './js/ext/handlebars.min.js',
    './js/ext/mlab.utils.js',
    './js/blf.utils.js',
    './js/blf.layout.js',
    './js/blf.control.js'
  ].concat(findit.sync('./js/modules/').filter(function(s) {
    return s.match(/\.js$/);
  }));

  // Project configuration.
  grunt.initConfig({
    uglify: {
      options: {
        banner: '/* BibLib Web front-end */\n'
      },
      prod: {
        files: {
          'build/blf.min.js': jsFiles
        }
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-uglify');

  // By default, will check lint, test and minify:
  grunt.registerTask('default', ['uglify']);
};
