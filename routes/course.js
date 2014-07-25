var course_model = require('../models/courses.js');

var Course = course_model.Course;


exports.list = function(req, res){
  	res.send("these are all the courses! yay!");
};

exports.add_course = function(){
	res.send("add a course!")
}