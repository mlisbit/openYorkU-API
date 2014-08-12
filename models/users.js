var mongoose = require("mongoose");

var Schema = mongoose.Schema;

var UserSchema = new Schema({
    first_name: String,
    last_name: String,
    email: String,
    password: String,
    date_joined: Date,
    term_year: Number,
    profile: {
    	image_url: String,
    	links: {
    		facebook: String,
    		github: String,
    		personal: String,
    		steam: String,
    		email: String,
    	},
    	major: String,
    	about: String
    }
});

var APIKeySchema = new Schema({
    user: {type: mongoose.Schema.Types.ObjectId, ref: 'User'},
    key: String,
    max_requests: Number,
    experation_date: Date,
    permissions: {
    	get: {
    		courses: Boolean,
    		faculties: Boolean,
    		places: Boolean,
    		subjects: Boolean,
    		users: Boolean
    	},
    	put: {
    		courses: Boolean,
    		faculties: Boolean,
    		places: Boolean,
    		subjects: Boolean,
    		users: Boolean
    	},
    	del: {
    		courses: Boolean,
    		faculties: Boolean,
    		places: Boolean,
    		subjects: Boolean,
    		users: Boolean
    	}
    }
});

var RestaurantRatingSchema = new Schema({
})

var CourseRatingSchema = new Schema({
})


User = mongoose.model('User', UserSchema);
API = mongoose.model('API', APIKeySchema);

exports.User = User;
exports.API = API;
