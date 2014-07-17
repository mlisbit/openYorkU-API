#!ve/bin/python
import sys
import json
import logging
import coloredlogs
from flask import Flask, jsonify, request, abort
from bson.json_util import dumps
from flask.ext.pymongo import PyMongo

#http://api.mongodb.org/python/current/api/bson/json_util.html

app = Flask(__name__)
mongo = PyMongo(app)
version = '/v1/'
logger = logging.getLogger(__name__)


coloredlogs.install(level=logging.INFO, show_timestamps=False, show_hostname=False, show_name=False)

@app.route('/')
def index():
	return "welcome to YorkU's unofficial API."

@app.route('/courses/del', methods = ['GET'])
def delete_courses():
	print request.args.getlist('help')
	all_courses_dict = list(mongo.db['courses'].find({}, {'_id': 0}))
	return  dumps(all_courses_dict)

@app.route('/courses/', methods = ['GET'])
def get_courses():
	print request.args.getlist('help')
	all_courses_dict = list(mongo.db['courses'].find({}, {'_id': 0}))
	return  dumps(all_courses_dict)

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