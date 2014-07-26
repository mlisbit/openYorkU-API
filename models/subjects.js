var mongoose = require("mongoose");

var Schema = mongoose.Schema;
var SubjectSchema = new Schema({
    'code': {type:String, unique:true},  
    'title': String, 
    'courses': [{type: mongoose.Schema.Types.ObjectId, ref: 'Course'}]
});

Subject = mongoose.model('Subject', SubjectSchema);
exports.Subject = Subject;