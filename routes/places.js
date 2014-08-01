var place_model = require('../models/places.js');

var Place = place_model.Place;
var Restaurant = place_model.Restaurant;

//get
exports.list = function(req, res, next){
	Place.find({},function (err, places) {
        res.status(200).send(places)
    });
};

//GET (should be DEL)
exports.clear_db = function(req, res, next){
	Place.remove(function(err) {
		res.send("removed database successfully.")
	});
};

//post
exports.add_restaurant = function(req, res, next){
	var instance = new Restaurant(req.body);
	instance.save(function(err) {
		if (err) {
			next(err);
		}
		res.send("added a restaurant!");	
	});
};

//post
exports.add_building = function(req, res, next){
	var instance = new Restaurant(req.body);
	instance.save(function(err) {
		if (err) {
			next(err);
		}
		res.send("added a building!");	
	});
};