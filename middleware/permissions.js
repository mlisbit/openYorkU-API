var my_conf = require('../config.json');
var user_model = require('../models/users.js');

var API_Key = user_model.API_Key;


exports.permissions = function(data, req, res, next) {
	if (my_conf.development_options.ignore_api_key) {
		//skip over checking the api key, move to next middleware in stack.
		next(data)
	} else {
		var key = req.query['key'];
		API_Key.find({key: key}, function (err, api_user) {
        	if (err) {
        		next({err: err});
        	} 
        	else if (api_user.length === 0) {
        		next({err: new Error('invalid API Key')});
        	}
        	else {
        		next(data)
        	}
    	});
	}
}