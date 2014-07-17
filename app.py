#!ve/bin/python
from flask import Flask, jsonify
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)
version = '/v1/'


@app.route('/')
def index():
	return "welcome to YorkU's unofficial API."

@app.route('/courses/', methods = ['GET'])
def get_tasks():
	return jsonify( { 'courses': {} } )

if __name__ == '__main__':
	app.run(debug = True)