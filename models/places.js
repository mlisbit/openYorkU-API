var mongoose = require("mongoose")
	, extend = require('mongoose-schema-extend');

var Schema = mongoose.Schema;

var PlaceSchema = new Schema({
	campus	: {type: String, default: 'Keele'},
	name 	: {type: String, unique: true},
	building: {type: mongoose.Schema.Types.ObjectId, ref: 'Building'},
	location: {
		lon: Number,
		lat: Number
	}
}, { collection : 'places', discriminatorKey : '_type' });

var LibrarySchema = PlaceSchema.extend({
	
});

var RoomSchema = PlaceSchema.extend({
	room_number: String,
	capacity: String
});

var StudyAreaSchema = PlaceSchema.extend({
	capacity: String
});

var BuildingSchema = PlaceSchema.extend({
	building_name: String,
	building_code: {type: String, unique: true},
	cover_polygon: [
		{
			lon: Number,
			lat: Number
		}
	],
	building_gps: {
		lon: Number,
		lat: Number
	},
	year_built: String,
	history: String,
	restaurants: [{type: mongoose.Schema.Types.ObjectId, ref: 'Restaurant'}],
	rooms: [{type: mongoose.Schema.Types.ObjectId, ref: 'Room'}],
	libraries: [{type: mongoose.Schema.Types.ObjectId, ref: 'Library'}],
	study_areas: [{type: mongoose.Schema.Types.ObjectId, ref: 'StudyArea'}],
	art_areas: [{type: mongoose.Schema.Types.ObjectId, ref: 'ArtArea'}],
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

var ParkingLotSchema = PlaceSchema.extend({
	is_reserved: Boolean,
	capacity: String,
	cover_polygon: [
		{
			lon: Number,
			lat: Number
		}
	]
});

var RecreationSchema = PlaceSchema.extend({
	intended_purpose: String
});

var ParkingGarageSchema = PlaceSchema.extend({
	capacity: String
});

var BusStopSchema = PlaceSchema.extend({
	bus_servicer: String
});

var ArtAreaSchema = PlaceSchema.extend({
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
