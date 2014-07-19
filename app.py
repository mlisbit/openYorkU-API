#!ve/bin/python
import sys
import logging
import pprint
import coloredlogs

from flask import Flask, jsonify, request, abort, Response, json
from bson import json_util
from bson.json_util import dumps
from flask.ext.pymongo import PyMongo

#http://api.mongodb.org/python/current/api/bson/json_util.html

app = Flask(__name__)
mongo = PyMongo(app)
version = '/v1/'
logger = logging.getLogger(__name__)
#mongo.db['courses'].ensureIndex( { "course_code": 1 }, { unique: true } )


coloredlogs.install(level=logging.INFO, show_timestamps=False, show_hostname=False, show_name=False)

@app.route('/')
def index():
	return "welcome to YorkU's unofficial API."

@app.route('/courses/del', methods = ['GET'])
def delete_courses():
	mongo.db['courses'].remove()
	doc = list(mongo.db['courses'].find({}, {'_id': 0}))
	return  Response(json.dumps(doc, indent=4, default=json_util.default), mimetype='application/json')

@app.route('/courses/', methods = ['GET'])
def get_courses():
	#print request.args.getlist('help')
	args = {}
	fields = {'_id': 0}

	#if a param is anumber, convert it.
	for key in request.args.to_dict():
		if key == 'fields':
			fields[request.args.get(key)] = 1
		elif request.args.get(key).isdigit():
			args[key] = int(request.args.get(key))
		else:
			args[key] = request.args.get(key)
	
	doc = list(mongo.db['courses'].find(args, fields))
	return Response(json.dumps(doc, indent=4, default=json_util.default), mimetype='application/json')
	

@app.route('/courses/<coursecode>', methods = ['GET'])
def get_course(coursecode):
	all_courses_dict = list(mongo.db['courses'].find({}, {'_id': 0}))
	logger.warn(coursecode)
	logger.error(all_courses_dict)
	return  dumps(all_courses_dict)

@app.route('/courses/', methods = ['POST'])
def create_course():
	print mongo.db.collection_names()
	if not request.data:
		logger.warn("post request sent, but no data")
		abort(400, 'No data received')
	try:
		mongo.db['courses'].save(json.loads(request.data))
	except TypeError as ee:
		logger.error(ee)
		abort(400, "error")
	except:
		logger.error(sys.exc_info()[0])
	return "post successful"
	
if __name__ == '__main__':

	app.run(debug = True)