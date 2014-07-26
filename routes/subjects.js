var subject_model = require('../models/subjects.js');
var course_model = require('../models/courses.js');

var Course = course_model.Course;
var Subject = subject_model.Subject;

exports.list = function(req, res, next){
	var limit 		= 0
		, offset 	= 0
		, args 		= {}
		, q 		= req.query
		, fields 	= {_id: 0, __v: 0}

	Subject.find(args, fields, { limit : limit , skip: offset},function (err, subjects) {
        res.status(200).send(subjects)
    });
};

exports.collect_courses = function(req, res, next){
	res.send("collected all the subjects from courses document.")
};

exports.clear_db = function(req, res, next){
	Subject.remove(function(err) {
		res.send("removed database successfully.")
	});
}

exports.add_subject = function(req, res, next){
	var instance = new Subject(req.body);
	instance.save(function(err) {
		if (err) {
			next(err);
		}
		res.send("added a subject!");	
	});
}
