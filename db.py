import os
import numpy as np
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
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
db = SQLAlchemy(app)


class RefuelingDB(db.Model):
	__tablename__ = 'core_configuration'
	id = db.Column(db.Integer, primary_key=True)
	refueling_name = db.Column(db.String(100))
	description = db.Column(db.String(300))
	date = db.Column(db.DateTime())
	burnup_data = db.Column(db.LargeBinary(length=500))
	

	def __init__(self, *args, **kwargs):
		self.refueling_name = kwargs['name']
		self.description = kwargs['description']
		self.date = kwargs['date']
		self.burnup_data = kwargs['data']
		# self.burnup_data = bytes(data, 'utf-8')
		# self.session = MySession()

	def __repr__(self):
		return f'{self.__class__.__name__}(id={self.id}, name={self.refueling_name}, date={self.date}, data={self.burnup_data})'


# def query(): #* query testing 
# 	session = MySession()
# 	response = session.query(RefuelingDB.id).all()
# 	print(response)
# 	response = session.query(RefuelingDB).filter(RefuelingDB.id == 3).all()
# 	print(response)
# 	for i in response:
# 		configuration = i.burnup_data
# 		print(i.description)
# 		arr = np.frombuffer(configuration)
# 		arr = arr.reshape((6,4))
# 		print(arr)
# 	return 


# if __name__ == '__main__':

