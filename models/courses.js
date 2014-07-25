var mongoose = require("mongoose");

var Schema = mongoose.Schema;
var CourseSchema = new Schema({
    'course_code': {type:String, unique:true},  
    'course_number': Number,
    'course_subject': String,
    'title': String,
    'faculty': [String],
    'year_level': Number,
    'credit_count': [Number],
    'term_years_offered': [Number],
    'instructors': [String],
    'description': String,

});

Course = mongoose.model('Course', CourseSchema);
exports.Course = Course;