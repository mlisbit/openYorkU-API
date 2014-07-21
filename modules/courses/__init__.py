#!ve/bin/python
import sys
import logging
import pprint
import coloredlogs

from flask import Blueprint, Flask, jsonify, request, abort, Response, json, g, current_app, _app_ctx_stack
from bson import json_util
from bson.json_util import dumps

from pprint import pprint
from flask.ext.pymongo import PyMongo


#http://api.mongodb.org/python/current/api/bson/json_util.html
mod = Blueprint('courses', __name__.split('.')[-1])

#app = current_app._get_current_object()

logger = logging.getLogger(__name__)
#mongo.db['courses'].ensureIndex( { "course_code": 1 }, { unique: true } )

coloredlogs.install(level=logging.INFO, show_timestamps=False, show_hostname=False, show_name=False)

@mod.route('/del', methods = ['GET'])
def delete_courses():
	mongo = g.mongo
	mongo.db['courses'].remove()
	doc = list(mongo.db['courses'].find({}, {'_id': 0}))
	return  Response(json.dumps(doc, indent=4, default=json_util.default), mimetype='application/json')

@mod.route('/', methods = ['GET'])
def get_courses():
	mongo = g.mongo
	limit = 0
	offset = 0
	args = {}
	fields = {'_id': 0, 'terms_offered': 0, 'instructors': 0, 'description': 0, 'term_year': 0, "faculty": 0}

	try:
		for key in request.args.to_dict():
			arg = request.args.get(key)
			if key == 'q':
				query = {'$regex': '(?i)'}
				for i in arg.split(' '):
					print arg
					query['$regex'] = str(query['$regex']+'.*'+i)
				print query
				args['title'] = query
			elif key == 'limit':
				limit = int(arg) if arg.isdigit() else arg
			elif key == 'offset':
				offset = int(arg) if arg.isdigit() else arg
			elif key == 'fields':
				#only show these fields in the response.
				field_args = arg.split(',')
				fields = {'_id': 0}
				for field_arg in field_args:
					fields[field_arg]=1
			elif key == 'unhide-fields':
				#show the hidden fields of a typical response
				field_args = arg.split(',')
				for field_arg in field_args:
					try:
						del fields[field_arg]
					except:
						logger.warn('attempted to remove field that was not already remove (possibly doesnt exist)')
			else:
				in_query = {}
				in_options = arg.split(',')
				in_query['$in'] = [int(i) if i.isdigit() else i for i in in_options]
				args[key] = in_query
	except:
		abort(404)
	doc = list(mongo.db['courses'].find(args, fields).limit(limit).skip(offset))
	return Response(json.dumps(doc, indent=4, default=json_util.default), mimetype='application/json')
	

@mod.route('/<coursecode>', methods = ['GET'])
def get_course(coursecode):
	args = {'course_code':coursecode}
	fields = {'_id': 0}

	for key in request.args.to_dict():
		arg = request.args.get(key)
		if key == 'fields':
			#only show these fields in the response.
			field_args = arg.split(',')
			fields = {'_id': 0}
			for field_arg in field_args:
				fields[field_arg]=1

	doc = list(mongo.db['courses'].find(args, fields))
	return Response(json.dumps(doc, indent=4, default=json_util.default), mimetype='application/json')

@mod.route('/', methods = ['POST'])
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

	mod.run(debug = True)