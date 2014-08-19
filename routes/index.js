var course_model = require('../models/courses.js');
var Course = course_model.Course;

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
			console.log('hello?')
			var course1 = new Course({'course_code': 'ABC123'});
			var course2 = new Course({'course_code': 'ABC123'});
			console.log('nope')
			console.log(type)

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