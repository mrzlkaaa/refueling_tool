import os
import numpy as np
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SelectField
from sqlalchemy.sql import func
import psycopg2

load_dotenv()
#credentials
user = os.environ['PSQL_USER']
pwd = os.environ['PSWD']
port = os.environ['PORT']
host = os.environ['HOST'] 
database = os.environ['DB']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{pwd}@{host}:{port}/{database}'
app.config['SECRET_KEY'] = 'dev'
db = SQLAlchemy(app)


class RefuelingDB(db.Model):
	__tablename__ = 'reactor_refuel'
	id = db.Column(db.Integer, primary_key=True)
	refueling_name = db.Column(db.String(100)) 
	date = db.Column(db.DateTime(), default=func.now()) # the same data for every reactor refueling
	activities = db.relationship('RefuelingActs', backref='refuel')
	
	def __init__(self, *args, **kwargs):
		self.refueling_name = kwargs['name']
		self.date = kwargs['date']

	def __repr__(self):
		return f'{self.__class__.__name__}(id={self.id}, name={self.refueling_name}, date={self.date})'

class RefuelingActs(db.Model):
	__tablename__ = 'refuel_acts'
	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.String(300))
	burnup_data = db.Column(db.LargeBinary(length=500))
	refuel_id = db.Column(db.Integer, db.ForeignKey('reactor_refuel.id'))

	def __init__(self, *args, **kwargs):
		self.description = kwargs['description']
		self.burnup_data = kwargs['data']


class RefuelList(FlaskForm):
    	names = SelectField('dbnames', choices=[(data.id, data.refueling_name) for data in RefuelingDB.query.all()])
		# names = SelectField('dbnames', choices=[('LA', 'California')])


if __name__ == '__main__':
	db.create_all()

