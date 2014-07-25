var express = require('express');
var routes = require('./routes');
var course = require('./routes/course');
var http = require('http');
var path = require('path');
var reload = require('reload');
var mongoose = require("mongoose");

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

//app.use(express.favicon());
app.use(express.logger('dev'));
app.use(express.json());
app.use(express.urlencoded());
app.use(express.methodOverride());
app.use(express.cookieParser('a_secret_key'));
app.use(express.session());
app.use(app.router);
app.use(express.favicon(__dirname + '/favicon.ico'));

// development only
if ('development' == app.get('env')) {
  app.use(express.errorHandler());
}

app.get('/', routes.index);
app.get('/courses', course.list);
app.post('/courses', course.add_course);

http.createServer(app).listen(app.get('port'), function(){
  console.log('Express server listening on port ' + app.get('port'));
}); 
