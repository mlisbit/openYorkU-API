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
	//console.log(req.body);
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

exports.modify_course = function(req, res, next){
	var update_fields= {
		credit_count: req.body.credit_count, 
		term_years_offered: req.body.term_years_offered,
		faculty: req.body.faculty,
		instructors: req.body.instructors
	}
	if (!req.body.credit_count) {delete update_fields.credit_count};
	if (!req.body.term_years_offered) {delete update_fields.term_years_offered};
	if (!req.body.faculty) {delete update_fields.faculty};
	if (!req.body.instructors) {delete update_fields.instructors};

	Course.update({course_code: req.body.course_code
	}, {$addToSet: update_fields}, function(err) {
		if (err) { next(err); }
		res.status(200).send("Successfully changed document")
	});
}