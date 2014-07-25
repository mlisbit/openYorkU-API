var express = require('express');
var routes = require('./routes');
var courses = require('./routes/courses');
var http = require('http');
var path = require('path');
var reload = require('reload');
var mongoose = require("mongoose");
//include winston
//include underscore

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
	console.log('ERROR', err.name, err.err);
	res.status(400).send('ERROR', err.name, err.err)
})


app.get('/', routes.index);
app.get('/courses', courses.list);
//just for testing really.
app.get('/courses/del', courses.clear_db);
app.post('/courses', courses.add_course);
app.put('/courses', courses.modify_course);

http.createServer(app).listen(app.get('port'), function(){
  console.log('Express server listening on port ' + app.get('port'));
}); 
