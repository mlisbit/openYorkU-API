var mongoose = require("mongoose");

var Schema = mongoose.Schema;

var CourseSchema = new Schema({
    course_id: String
});

CourseSchema.statics.newCourse = function (course, fn) {
	
}

Course = mongoose.model('Course', CourseSchema);
exports.Course = Course;