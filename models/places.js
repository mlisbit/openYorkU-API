var mongoose = require("mongoose")
	, extend = require('mongoose-schema-extend');

var Schema = mongoose.Schema;
var PlaceSchema = new Schema({
	name 	: String,
	building: String,
	location: {
		lon: Number,
		lat: Number
	}
});

var LibrarySchema = PlaceSchema.extend({
	
});

var RoomSchema = PlaceSchema.extend({
	
});

var BuildingSchema = PlaceSchema.extend({
	building_code: String
});

var RestaurantSchema = PlaceSchema.extend({
	tags	: [String],
	hours 	: {
		monday		: {open: String, close: String},
		tuesday		: {open: String, close: String},
		wednesday	: {open: String, close: String},
		thursday	: {open: String, close: String},
		friday		: {open: String, close: String},
		saturday	: {open: String, close: String},
		sunday		: {open: String, close: String}
	},
	logo_url: String,
	serves_booze: Boolean
});

var ArtSchema = PlaceSchema.extend({
	artist	: 	String
});

Place = mongoose.model('Place', PlaceSchema);
Library = mongoose.model('Library', LibrarySchema);
exports.Place = Place;

