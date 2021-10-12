import os
import numpy as np
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, select, Column, Integer, String, DateTime, LargeBinary
from sqlalchemy.orm import declarative_base, Session
import psycopg2

load_dotenv()
#credentials
user = os.environ['PSQL_USER']
pwd = os.environ['PSWD']
port = os.environ['PORT']
host = os.environ['HOST'] 
db = os.environ['DB']

engine = create_engine(f'postgresql://{user}:{pwd}@{host}:{port}/{db}', echo=True)
print(engine.connect())
Base = declarative_base()


def MySession():
	with Session(engine) as session:
		return session


class RefuelingDB(Base):
	__tablename__ = 'core_configuration'
	id = Column(Integer, primary_key=True)
	refueling_name = Column(String(100))
	description = Column(String(300))
	date = Column(DateTime())
	burnup_data = Column(LargeBinary(length=500))
	

	# def __init__(self, name='', description='', date=datetime.now(), data=np.array([0.0, 0.0])):
	def __init__(self, *args, **kwargs):
		self.refueling_name = kwargs['name']
		self.description = kwargs['description']
		self.date = kwargs['date']
		self.burnup_data = kwargs['data']
		# self.burnup_data = bytes(data, 'utf-8')
		self.session = MySession()

	def __repr__(self):
		return f'{self.__class__.__name__}(id={self.id}, name={self.refueling_name}, date={self.date}, data={self.burnup_data})'

	def add(self):
		self.session.add(self)
		self.session.flush()
		return self.session.commit()


def query(): #* query testing 
	session = MySession()
	response = session.query(RefuelingDB.id).all()
	print(response)
	response = session.query(RefuelingDB).filter(RefuelingDB.id == 3).all()
	print(response)
	for i in response:
		configuration = i.burnup_data
		print(i.description)
		arr = np.frombuffer(configuration)
		arr = arr.reshape((6,4))
		print(arr)
	return 


if __name__ == '__main__':
	# test = Refueling('refueling #118', '2 new 6-th tube in cells: 4-6, 6-6', 'here is a data').add()
	# print(Refueling(name='refueling #118', data=np.array([0,0]), date=datetime.now(), description=''))
	print(query())
	# print(select(Refueling))
	# Base.metadata.create_all(engine)

