var mongoose = require("mongoose");

var Schema = mongoose.Schema;
var FacultySchema = new Schema({
    'code': {type:String, unique:true},  
    'title': String,
    'office_location': String, 
    'courses': [{type: mongoose.Schema.Types.ObjectId, ref: 'Course'}]
});

Faculty = mongoose.model('Faculty', FacultySchema);
exports.Faculty = Faculty;