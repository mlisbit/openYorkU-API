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

app = Flask(__name__.split('.')[-1])

logger = logging.getLogger(__name__)


coloredlogs.install(level=logging.INFO, show_timestamps=False, show_hostname=False, show_name=False)

@app.route('/', methods = ['GET'])
def get_faulties():
	pass
	
if __name__ == '__main__':

	app.run(debug = True)