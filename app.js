var express = require('express');
var routes = require('./routes');
var http = require('http');
var path = require('path');
var reload = require('reload');
var mongoose = require("mongoose");
var docs = require("express-mongoose-docs");

/* ROUTES */
var courses = require('./routes/courses');
var faculties = require('./routes/faculties');
var subjects = require('./routes/subjects');
var places = require('./routes/places');

//include winston
//include underscore
//include mocha

mongoose.connect('mongodb://localhost/openyorku', function(err) {
	if (!err) {
		console.log("connected to mongodb");
	} else {
		throw err;
	}
});

var app = express();

// all environments
app.set('port', process.env.PORT || 1337);

app.use(express.favicon(__dirname + '/public/favicon.ico'));
app.use(express.logger('dev'));
app.use(express.json());
app.use(express.urlencoded());
app.use(express.methodOverride());
app.use(express.cookieParser('a_secret_key'));
app.use(express.session());
app.use(app.router);
app.use(function (err, req, res, next) {
	res.send('ERROR')
	console.log('ERROR', err.name, err.err);
})

docs(app, mongoose);

/* HOME */
app.get('/', routes.index);
app.get('/help', routes.index);

/* COURSES */
app.get('/courses', courses.list);
app.get('/courses/del', courses.clear_db);
app.put('/courses', courses.modify_course);
app.get('/courses/:code', courses.show_course);
app.post('/courses', courses.add_course);

/* FACULTIES */
app.get('/faculties', faculties.list);

/* SUBJECTS */
app.get('/subjects', subjects.list);
app.get('/subjects/collect', subjects.collect_courses);
app.get('/subjects/del', subjects.clear_db);
app.get('/subjects/:code', subjects.show_subject);
app.put('/subjects', subjects.modify_subject);
app.post('/subjects', subjects.add_subject);

/* PLACES */
app.get('/places', places.list);


http.createServer(app).listen(app.get('port'), function(){
  console.log('Express server listening on port ' + app.get('port'));
}); 
