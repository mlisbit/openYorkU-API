exports.index = function(req, res, next){
	res.json("openyorku api")
};

exports.help = function(req, res, next){
	res.send("you will be able to find help here.")
};

exports.env = function(req, res, next){
	if (process.env.NODE_ENV) {
		res.json(process.env.NODE_ENV)
	} else {
		res.json("development")
	}
};