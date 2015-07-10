#!flask/bin/python

import os
from flask import Flask
from flask_restful import Api
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.migrate import Migrate

app = Flask(__name__)


appType = os.getenv('APP_TYPE', 'DEBUG')

if appType == 'DEBUG':
	app.config.from_object('config.BaseConfig')
else:
	app.config.from_object('config.ProductionConfig')

# Database
db = SQLAlchemy(app)
migrate = Migrate (app, db)

# Restful
api = Api(app)

# Bcrypt
bcrypt = Bcrypt(app)

# --- Views
from app import views

@app.route('/')
def hello():
	return 'Hello World'