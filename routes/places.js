var place_model = require('../models/places.js');

var Place = place_model.Place;
var Restaurant = place_model.Restaurant;
var Building = place_model.Building;

function getDateFromString(instance, is_closing) {
	//default stuff
	var minutes = 0;
	var hour = 24;
	var the_date = new Date();

	var colon_position = instance.indexOf(':')
	//if there's a colon, that meants minutes are included.
	if (colon_position >= 1) {
		minutes = parseInt(instance.slice(colon_position+1,colon_position+3))
		hour = parseInt(instance.slice(0, colon_position))
	}
	//otherwise no minutes. just parse the first two characters as ints. 
	else {
		hour = parseInt(instance.toUpperCase().slice(0, 2))
	}

	//if there's a PM in the time, add 12 to the hours to convert to 24hour base. 
	if (instance.toUpperCase().search('PM') > 0) {
		hour = hour + 12
	}

	//if there's an AM in the closing time, we know it closes the next day. So add a day to the closing time. 
	if (instance.toUpperCase().search('AM') > 0 && is_closing === true) {
		the_date.setDate(the_date.getDate() + 1)
	}

	//modify the current date with current hour and minutes.
	the_date.setHours(hour)
	the_date.setMinutes(minutes)
	return the_date;
}

function checkIfOpen(instance) {
	var current_date 	= new Date()
	//if the time right now is less than 2am, than get the hours for the previous date. 
	if (current_date.getHours() < 2 && instance.hours[getDayFromNumber(current_date.getDay())-1].toUpperCase().search('AM') > 0) {
		day = current_date.getDay() - 1
		if (day === -1) {
			day = 6
		}
		var current_day = getDayFromNumber(day)
	} else {
		var current_day = getDayFromNumber(current_date.getDay())
	}
	var open = getDateFromString(instance.hours[current_day].open)
	var close = getDateFromString(instance.hours[current_day].close, true)
	return (current_date > open && current_date < close)
}

function getDayFromNumber(day_number) {
	weekdays = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
	return weekdays[day_number]
}
//get
exports.list = function(type) {
	return function(req, res, next){
		var q 			= req.query
			, args 		= {}
			, fields 	= {}
			, limit 	= 0
			, offset 	= 0
			, fields 	= {_id: 0, __v: 0}
			, check_if_open = false

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
				case 'is_open':
					if (parseInt(q[key]) === 1) {
						check_if_open = true
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
			.where()
			.exec(function (err, results) {
				if (err) {
					next(err)
				} 
				if (check_if_open && type === 'Restaurant') {
					for (var i = 0 ; i < results.length ; i++) {
						if (!checkIfOpen(results[i])) {
							delete results[i]
						}
					}
					next({data: results.filter(function(e){return e})}) 
				} else {
					next({data: results}) 
				}
				 	
	    	}) // exec;
	} //return function
}

//GET (should be DEL)
exports.clear_db = function(type) {
	return function(req, res, next){
		place_model[type].remove(function(err) {
			next({message: "removed database successfully."})
		});
	};
};

//post
exports.add_restaurant = function(req, res, next){
	//first find the building this restaurant says its in.
	Building.findOne({building_code: req.body.building},function (err, building) {
		if (err) {
			next(err);
		}
		req.body.building = building
		var instance = new Restaurant(req.body);

        instance.save(function(err) {
			if (err) {
				next({err:err});
			}
			next({message: "added a restaurant!"});	
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
		next({message: "added a building!"});	
	});
};