var course_model = require('../models/courses.js');

var Course = course_model.Course;

//get
exports.list = function(req, res, next){
	var limit = 0,
		offset = 0,
		args = {},
		q = req.query
	var fields = {_id: 0, terms_offered: 0, instructors: 0, description: 0, term_year: 0, faculty: 0, __v: 0}

	/////////
	for (var key in q) {
		switch (key) {
			case 'q':
				var query = {'$regex': '(?i)'}
				for (i in q[key].split(',')) {
					console.log(q[key].split(',')[i])
					query['$regex'] = query['$regex']+'.*'+q[key].split(',')[i]
				}
				args['title'] = query;
				break;
			case 'limit':
				limit = parseInt(q[key])
			case 'offset':
				offset = parseInt(q[key])
			/*
				limit = int(arg) if arg.isdigit() else arg
			elif key == 'offset':
				offset = int(arg) if arg.isdigit() else arg
			elif key == 'fields':
				#only show these fields in the response.
				field_args = arg.split(',')
				fields = {'_id': 0}
				for field_arg in field_args:
					fields[field_arg]=1
			elif key == 'unhide-fields':
				#show the hidden fields of a typical response
				field_args = arg.split(',')
				for field_arg in field_args:
					try:
						del fields[field_arg]
					except:
						logger.warn('attempted to remove field that was not already remove (possibly doesnt exist)')
			else:
				in_query = {}
				in_options = arg.split(',')
				in_query['$in'] = [int(i) if i.isdigit() else i for i in in_options]
				args[key] = in_query
				*/
		} //switch
	} //for
	
	/////////

	Course.find(args, fields, { limit : limit , skip: offset},function (err, courses) {
        res.status(200).send(courses)
    }).limit(5);
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