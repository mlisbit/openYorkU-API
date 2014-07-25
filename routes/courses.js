var course_model = require('../models/courses.js');

var Course = course_model.Course;

//get
exports.list = function(req, res, next){
	Course.find({}, function (err, courses) {
        res.status(200).send(courses)
    });
};

//post
exports.add_course = function(req, res, next){
	var instance = new Course(req.body);
	instance.save(function(err) {
		if (err) {
			next(err);
		}
		res.send("add a course!");	
	});
}

exports.clear_db = function(req, res, next){
	Course.remove(function(err) {
		res.send("removed database successfully.")
	});
}