import os
import numpy as np
from . import db
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import SelectField
from sqlalchemy.sql import func
from functools import wraps


class RefuelingDB(db.Model):
	__tablename__ = 'reactor_refuel'
	id = db.Column(db.Integer, primary_key=True)
	refueling_name = db.Column(db.String(100))
	initial_configuration = db.Column(db.LargeBinary())
	initial_burnup_data = db.Column(db.LargeBinary(length=500))
	date = db.Column(db.DateTime(), default=func.now()) # the same data for every reactor refueling
	acts = db.relationship('RefuelingActs', backref='refuel')

	def __repr__(self):
		return f'{self.__class__.__name__}(id={self.id}, name={self.refueling_name})'

class RefuelingActs(db.Model):
	__tablename__ = 'refuel_acts'
	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.String(300))
	current_configuration = db.Column(db.LargeBinary())
	burnup_data = db.Column(db.LargeBinary(length=500))
	refuel_id = db.Column(db.Integer, db.ForeignKey('reactor_refuel.id'))

	def __repr__(self):
		return f'{self.__class__.__name__}(id={self.id}, description={self.description})'

class RefuelList(FlaskForm):
	add_existing = SelectField('dbnames', choices=[])