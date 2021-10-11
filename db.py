import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import psycopg2

#credentials
user = os.environ['USER']
pwd = os.environ['PWD']
port = os.environ['PORT']
host = os.environ['HOST'] 
db = os.environ['DB']

engine = create_engine('postgresql+psycopg2://:{user}@{host}:{port}/mydatabase')

load_dotenv()
print()