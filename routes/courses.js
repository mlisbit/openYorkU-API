var course_model = require('../models/courses.js');

var Course = course_model.Course;

//get
exports.list = function(req, res, next){
	var limit = 0,
		offset = 0,
		args = {},
		q = req.query
	var fields = {_id: 0, terms_offered: 0, instructors: 0, description: 0, term_year: 0, faculty: 0, __v: 0}

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
				console.log('ive been hit', arguement_list, key);
				var in_query = {}
				in_query.$in = arguement_list.map(function(item) {
					return parseInt(item, 10) || item
				});
				args[key] = in_query
		} //switch
	} //for

	Course.find(args, fields, { limit : limit , skip: offset},function (err, courses) {
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

exports.show_course = function(req, res, next){
	
}