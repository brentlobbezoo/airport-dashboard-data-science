const gulp = require('gulp');
const rename = require('gulp-rename');
const sass = require('gulp-sass')(require('sass'));
const cleanCSS = require('gulp-clean-css');

const buildpath = './../assets/'
const styles = [
    './scss/global.scss'
]
const scripts = [
    './js/*.js'
]

function compileSass() {
    return gulp.src(styles)
        .pipe(sass().on('error', sass.logError))
        .pipe(cleanCSS())
        .pipe(rename('main.css'))
        .pipe(gulp.dest(buildpath));
}

exports.styles = compileSass;