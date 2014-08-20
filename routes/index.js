var course_model = require('../models/courses.js');
var user_model = require('../models/users.js');

var Course = course_model.Course;
var API_Key = user_model.API_Key;

exports.index = function(req, res, next){
	res.json("openyorku api")
};

exports.help = function(req, res, next){
	res.send("you will be able to find help here.")
};

exports.env = function(req, res, next){
	if (process.env.NODE_ENV) {
		res.json(process.env.NODE_ENV)
	} else {
		res.json("development")
	}
};

exports.provoke_error = function(type) {
	return function(req, res, next) {
		
		if (type === 'duplicate') {
			var course1 = new Course({'course_code': 'ABC123'});
			var course2 = new Course({'course_code': 'ABC123'});

			course1.save(function(err) {

				if (err) {
					next( {err:err} );
				}
				course2.save(function(err2) {
					if (err2) { next( {err:err2}); }
				});
			});
			
		} // if
		else {
			next({err: new Error('this is just a test.')})
		}
	}
}

exports.add_api_key = function(req, res, next) {
	var api_key_instance = new API_Key({key: "helloworld"});

	api_key_instance.save(function(err) {
		if (err) {
			next({err: err})
		}
	})
}

exports.list_api_keys = function(req, res, next) {
	API_Key.find({}, function (err, api_keys) {
		next({data: api_keys})
	})
}

exports.time = function(req, res, next) {
	next({data: new Date()})
}