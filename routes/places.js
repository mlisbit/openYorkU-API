var place_model = require('../models/places.js');

var Place = place_model.Place;
var Restaurant = place_model.Restaurant;
var Building = place_model.Building;

//get
exports.list = function(type) {
	/*
		place_model[type].find({},function (err, places) {
        	res.status(200).send(places)
    	});
	};
	*/

	return function(req, res, next){
		var q 			= req.query
			, args 		= {}
			, fields 	= {}
			, limit 	= 0
			, offset 	= 0
			, fields 	= {_id: 0, __v: 0}

		for (var key in q) {
			var arguement_list = q[key].split(',');
			switch (key) {
				case 'q':
					var query = {'$regex': '(?i)'}
					for (i in arguement_list) {
						query['$regex'] = query['$regex']+'.*'+arguement_list[i]
					}
					args['name'] = query;
					break;
				case 'limit':
					limit = parseInt(q[key])
					break;
				case 'offset':
					offset = parseInt(q[key])
					break;
				case 'fields':
					//only show these fields in the response.
					fields = {'_id': 0}
					for (i in arguement_list) {
						fields[arguement_list[i]]=1
					}
					break;
				case 'show':
					//show the hidden fields of a typical response
					for (i in arguement_list) {
						delete fields[arguement_list]
					}
					break;
				default:
					//handles queries with parameters
					var in_query = {}
					in_query.$in = arguement_list.map(function(item) {
						return parseInt(item, 10) || item
					});
					args[key] = in_query
			} //switch
		} //for

		place_model[type]
			.find(args, fields, { limit : limit , skip: offset})
			.populate('building', 'name -_id')
			.exec(function (err, results) {
				if (err) {
					next(err)
				}
	        	res.status(200).send(results)
	    	});
	} //return function
}

//GET (should be DEL)
exports.clear_db = function(req, res, next){
	Place.remove();
	Building.remove(function(err) {
		res.send("removed database successfully.")
	});
};

//post
exports.add_restaurant = function(req, res, next){
	Building.findOne({building_code: req.body.building},function (err, building) {
		if (err) {
			next(err);
		}
		req.body.building = building
		var instance = new Restaurant(req.body);

        instance.save(function(err) {
			if (err) {
				next(err);
			}
			res.send("added a restaurant!");	
		});
    });
	
};

//post
exports.add_building = function(req, res, next){
	var instance = new Building(req.body);
	instance.save(function(err) {
		if (err) {
			next(err);
		}
		res.send("added a building!");	
	});
};