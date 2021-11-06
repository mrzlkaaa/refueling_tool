import os
import redis
import numpy as np
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SelectField
from sqlalchemy.sql import func
from sqlalchemy.orm import load_only
from functools import wraps

load_dotenv()
#credentials 
user = os.environ['PSQL_USER']
pwd = os.environ['PSWD']
port = os.environ['PORT']
host = os.environ['HOST'] 
database = os.environ['DB']

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+pg8000://{user}:{pwd}@{host}:{port}/{database}'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+pg8000://postgres:postgres@db/irt_refueling'
app.config['SECRET_KEY'] = 'dev'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

r = redis.Redis(host="in-memory", port = "6379", db=0)

class RefuelingDB(db.Model):
	__tablename__ = 'reactor_refuel'
	id = db.Column(db.Integer, primary_key=True)
	refueling_name = db.Column(db.String(100))
	initial_configuration = db.Column(db.LargeBinary())
	initial_burnup_data = db.Column(db.LargeBinary(length=500))
	date = db.Column(db.DateTime(), default=func.now()) # the same data for every reactor refueling
	acts = db.relationship('RefuelingActs', backref='refuel')

	def __repr__(self):
		return f'{self.__class__.__name__}(id={self.id}, name={self.refueling_name}, initial_configuration={self.initial_configuration[:10]}, initial_burnup_data={self.initial_burnup_data[:10]}, date={self.date}, acts={self.acts})'

class RefuelingActs(db.Model):
	__tablename__ = 'refuel_acts'
	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.String(300))
	current_configuration = db.Column(db.LargeBinary())
	burnup_data = db.Column(db.LargeBinary(length=500))
	refuel_id = db.Column(db.Integer, db.ForeignKey('reactor_refuel.id'))

	def __repr__(self):
		return f'{self.__class__.__name__}(id={self.id}, description={self.description}, current_configuration={self.current_configuration[:10]}, burnup_data={self.burnup_data[:10]}, refuel_id={self.refuel_id})'


class RefuelList(FlaskForm):
	add_existing = SelectField('dbnames', choices=[])


# if __name__ == '__main__':
# 	# db.create_all()
