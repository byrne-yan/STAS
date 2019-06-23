import os
from flask import Flask
from flask_pymongo import PyMongo
 
def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__,instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY='dev',
		#DATABASE=os.path.join(app.instance_path,'stas.sqlite'),
	)
	# if test_config is None:
		# app.config.from_pyfile('config.py',silent=True)
	# else:
		# app.config.from_mapping(test_config)
		
	# try:
		# os.makedirs(app.instance_path)
	# except OSError:
		# pass
	app.config.update(
		MONGO_URI='mongodb://localhost:27017/stas',
		MONGO_USERNAME='admin',
		MONGO_PASSWORD='312517'
	)
	
	
	from . import db
	db.init_app(app)
	
	# @app.route('/hello')
	# def hello():
		# return 'Hello World!'
		
	from . import auth
	app.register_blueprint(auth.bp)
	
	from . import stock
	app.register_blueprint(stock.bp)
	#app.add_url_rule('/', endpoint='index')
	
	return app