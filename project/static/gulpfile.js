// requirements
var gulp = require('gulp');
var gulpBrowser = require("gulp-browser");
var reactify = require('reactify');
var del = require('del');
var size = require('gulp-size');
var react = require('gulp-react');
var babel = require('gulp-babel');

// tasks
gulp.task('transform', function () {
  var stream = gulp.src('scripts/jsx/*.js')
    .pipe(gulpBrowser.browserify({transform: ['reactify']}))
    .pipe(gulp.dest('scripts/js'))
    .pipe(size());
  return stream;
});

gulp.task('del', function () {
	return del(['./scripts/js/main.js']);
});

gulp.task('default', function() {
    devMode = true;
    return gulp.src("scripts/jsx/*.jsx").
        pipe(babel({
            plugins: ['transform-react-jsx']
        })).
        pipe(gulp.dest("scripts/js"));
});