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
    key: {type: String, unique: true},
    max_requests: Number,
    experation_date: Date,
    permissions: {
    	get: {
    		courses: {type: Boolean, default: true},
    		faculties: {type: Boolean, default: true},
    		places: {type: Boolean, default: true},
    		subjects: {type: Boolean, default: true},
    		users: {type: Boolean, default: true},
    	},
    	put: {
    		courses: {type: Boolean, default: false},
    		faculties: {type: Boolean, default: false},
    		places: {type: Boolean, default: false},
    		subjects: {type: Boolean, default: false},
    		users: {type: Boolean, default: false},
    	},
    	del: {
    		courses: {type: Boolean, default: false},
    		faculties: {type: Boolean, default: false},
    		places: {type: Boolean, default: false},
    		subjects: {type: Boolean, default: false},
    		users: {type: Boolean, default: false},
    	}
    }
});

var RestaurantRatingSchema = new Schema({
})

var CourseRatingSchema = new Schema({
})


User = mongoose.model('User', UserSchema);
API_Key = mongoose.model('API_Key', APIKeySchema);

exports.User = User;
exports.API_Key = API_Key;
