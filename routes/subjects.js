var subject_model = require('../models/subjects.js');
var course_model = require('../models/courses.js');

var Course = course_model.Course;
var Subject = subject_model.Subject;

exports.list = function(req, res, next){
	var limit 		= 0
		, offset 	= 0
		, args 		= {}
		, q 		= req.query
		, fields 	= {_id: 0, __v: 0, courses: 0}
	for (var key in q) {
		var arguement_list = q[key].split(',');
		switch (key) {
			case 'q':
				var query = {'$regex': '(?i)'}
				for (i in arguement_list) {
					query['$regex'] = query['$regex']+'.*'+arguement_list[i]
				}
				args['title'] = query;
				break;
			case 'limit':
				limit = parseInt(q[key])
				break;
			case 'offset':
				offset = parseInt(q[key])
				break;
			case 'fields':
				//only show these fields in the response.
				fields = {'_id': 0}
				for (i in arguement_list) {
					fields[arguement_list[i]]=1
				}
				break;
			case 'show':
				//show the hidden fields of a typical response
				for (i in arguement_list) {
					delete fields[arguement_list]
				}
				break;
			default:
				//handles queries with parameters
				var in_query = {}
				in_query.$in = arguement_list.map(function(item) {
					return parseInt(item, 10) || item
				});
				args[key] = in_query
		} //switch
	} //for

	Subject
		.find(args, fields, { limit : limit , skip: offset})
		.populate('courses', 'title -_id')
		.exec(function (err, subjects) {
			if (err) {
				next(err)
			}
        	res.status(200).send(subjects)
    	});
};
exports.collect_courses = function(req, res, next){
	Course.find({}, {}, {limit: 0}, function (err, courses) {
		for (i in courses) {
			Subject.update(
				{code: courses[i].course_subject}, 
				{$addToSet: {courses: courses[i]}}, 
				function(err) {
					if (err) { next(err); }
					console.log('added a course to ',courses[i].course_subject)
				} //function()
			); //update()
		} //for
	}).exec(
		res.send("collected all the subjects from courses document.")
	)
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
};
exports.show_subject = function(req, res, next){
	Subject
		.findOne({code: req.params.code.toUpperCase()})
		.populate('courses', 'title -_id')
		.exec(function (err, subject) {
			if (err) {
				next(err)
			}
        	res.status(200).send(subject)
    	});
}