var mongoose = require("mongoose");

var Schema = mongoose.Schema;

var PlaceSchema = new Schema({
	
}, { collection : 'places', discriminatorKey : '_type' });

var LibrarySchema = new Schema({
	
});

var RoomSchema = new Schema({
	room_number: String,
	capacity: String
});

var StudyAreaSchema = new Schema({
	capacity: String
});

var BuildingSchema = new Schema({
	name: String,
	campus	: {type: String, default: 'Keele'},
	location: {
		lon: Number,
		lat: Number
	},
	building_code: {type: String, unique: true},
	cover_polygon: [
		{
			lon: Number,
			lat: Number
		}
	],
	year_built: Number,
	history: String,
	restaurants: [{type: mongoose.Schema.Types.ObjectId, ref: 'Restaurant'}],
	rooms: [{type: mongoose.Schema.Types.ObjectId, ref: 'Room'}],
	libraries: [{type: mongoose.Schema.Types.ObjectId, ref: 'Library'}],
	study_areas: [{type: mongoose.Schema.Types.ObjectId, ref: 'StudyArea'}],
	art_areas: [{type: mongoose.Schema.Types.ObjectId, ref: 'ArtArea'}],
});

var RestaurantSchema = new Schema({
	name: String,
	campus	: {type: String, default: 'Keele'},
	location: {
		lon: Number,
		lat: Number
	},
	building: {type: mongoose.Schema.Types.ObjectId, ref: 'Building'},
	tags	: [String],
	hours 	: {
		sunday		: {open: String, close: String},
		monday		: {open: String, close: String},
		tuesday		: {open: String, close: String},
		wednesday	: {open: String, close: String},
		thursday	: {open: String, close: String},
		friday		: {open: String, close: String},
		saturday	: {open: String, close: String}
	},
	logo_url: String,
	serves_booze: Boolean
});

RestaurantSchema.static.findStillOpen = function (cb) {
	var current_date = new Date();
	cb(current_date.getHours())
}


var ParkingLotSchema = new Schema({
	is_reserved: Boolean,
	capacity: String,
	cover_polygon: [
		{
			lon: Number,
			lat: Number
		}
	]
});

var RecreationSchema = new Schema({
	intended_purpose: String
});

var ParkingGarageSchema = new Schema({
	capacity: String
});

var BusStopSchema = new Schema({
	bus_servicer: String
});

var ArtAreaSchema = new Schema({
	is_exhibit: Boolean,
	is_theater: Boolean,
	is_art_peice: Boolean,
	artist: String
});

Place = mongoose.model('Place', PlaceSchema);
Library = mongoose.model('Library', LibrarySchema);
Restaurant = mongoose.model('Restaurant', RestaurantSchema);
Room = mongoose.model('Room', RoomSchema);
StudyArea = mongoose.model('StudyArea', StudyAreaSchema);
ArtArea = mongoose.model('ArtArea', ArtAreaSchema);
Building = mongoose.model('Building', BuildingSchema);

exports.Place = Place;
exports.Restaurant = Restaurant;
exports.Library = Library;
exports.Room = Room;
exports.StudyArea = StudyArea;
exports.ArtArea = ArtArea;
exports.Building = Building;
