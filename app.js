var express = require('express');
var routes = require('./routes');
var http = require('http');
var path = require('path');
var reload = require('reload');
var mongoose = require("mongoose");
var mongo = require("mongodb")
var docs = require("express-mongoose-docs");

var errors = require("./errors/errors");

var my_middleware = require("./middleware");

/* ROUTES */
var courses = require('./routes/courses');
var faculties = require('./routes/faculties');
var subjects = require('./routes/subjects');
var places = require('./routes/places');
var index = require('./routes/index');

var db_connection = 'mongodb://localhost/openyorku'

//include winston
//include underscore

var my_conf = require('./config.json');

var app = express();
// all environments
app.set('port', process.env.PORT || my_conf.server_options.port);
app.configure(function() {
	app.use(express.favicon(__dirname + '/public/favicon.ico'));
	app.use(express.logger('dev'));
	app.use(express.json());
	app.use(express.urlencoded());
	app.use(express.methodOverride());
	app.use(express.cookieParser(my_conf.server_options.cookie_parser_secret));
	app.use(express.session());
	app.use(app.router);
	app.use(my_middleware.permissions);
	app.use(my_middleware.counter);
	app.use(my_middleware.api_ify);
})

app.configure('test', function() {
	//connect to different db during tests
	//remove all existing data in the document so there's no conflicts.

	//WHY MUST YOU MAKE ME DO THIS MONGO!!!!!!!!!!!!!!!
	var count = 0;
	console.log('TESTING')
	
	function clearDB(total, fn) {
		for (i in mongoose.connection.collections) {
			removeDoc(i, total, fn)
		}
	}

	function removeDoc(i, total, fn) {
		mongoose.connection.collections[i].remove({}, function() {
			count++;
			console.log('removed all entries for ' + i + ' in db.')
			if (count === total) {
				fn()
			}
		}) //mongoose drop
	}

	mongoose.connect('mongodb://localhost/openyorku-testing', function(err) {
		var total_dbs = Object.keys(mongoose.connection.collections).length;
		clearDB(total_dbs, function() {
			console.log('cleared all dbs!')
		});
	});
})

app.configure('development', function() {
	console.log('DEVELOPMENT')

	if (process.env.DATABASE_URL) {
		console.log("database URL set : " + process.env.DATABASE_URL)
		db_connection = process.env.DATABASE_URL
	}

	mongoose.connect(process.env.DATABASE_URL, function(err) {
		if (!err) { console.log("connected to mongodb") } else { throw err; }
	});
});

app.configure('production', function() {
	console.log("PRODUCTION");
});
//create a proper error middleware, 
//create a logger middleware,
//create a user authentication middleware, including API keys

docs(app, mongoose);

/* HOME */
app.get('/', index.index);
app.get('/help', index.index);
app.get('/env', index.env);
app.get('/err', index.provoke_error('duplicate'));
app.get('/add_key', index.add_api_key);
app.get('/time', index.time)
app.get('/list_keys', index.list_api_keys);

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
app.get('/places', places.list('Place'));
app.get('/places/buildings', places.list('Building'));
app.get('/places/restaurants', places.list('Restaurant'));

app.get('/places/buildings/del', places.clear_db('Building'));
app.get('/places/restaurants/del', places.clear_db('Restaurant'));

app.get('/places/del', places.clear_db());
app.post('/places/restaurants', places.add_restaurant);
app.post('/places/buildings', places.add_building);

/* USERS */


http.createServer(app).listen(app.get('port'), function(){
  console.log('Express server listening on port ' + app.get('port'));
}); 
