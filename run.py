from flask import Flask, g
from modules.courses import mod
from flask.ext.pymongo import PyMongo

app = Flask(__name__)

mongo = PyMongo(app)
app.register_blueprint(mod, url_prefix='/courses')
@app.before_request
def mark_current_user_online():
	g.mongo = mongo
	#with current_app.app_context():
	#	mongo = PyMongo.get_default_database()
@app.route('/')
def index():
	return "welcome to YorkU's unofficial API."

app.run(debug=True)
