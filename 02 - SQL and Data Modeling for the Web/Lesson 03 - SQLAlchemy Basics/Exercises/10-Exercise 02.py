from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask("app")
app.config['SQLALCHEMY_DATABASE_URI'] = \
		'postgresql://student@localhost:5432/example'

db = SQLAlchemy(app)

