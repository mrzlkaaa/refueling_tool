import os, sys
import io
import redis
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

new_template_folder = os.path.join(os.getcwd().split()[0], "templates")
new_static_folder = os.path.join(os.getcwd().split()[0], "static")
# print(new_template_folder)

load_dotenv()
#credentials 
user = os.environ['PSQL_USER']
pwd = os.environ['PSWD']
port = os.environ['PORT']
host = os.environ['HOST'] 
database = os.environ['DB']

r = redis.Redis(host="redis", port = "6379", db=0)
db = SQLAlchemy()
migrate = Migrate()

UPLOAD_FOLDER = 'input/'

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI = f'postgresql+pg8000://{user}:{pwd}@{host}:{port}/{database}',
        SECRET_KEY = "DEV",
        UPLOAD_FOLDER = UPLOAD_FOLDER,
        DOWNLOAD_FOLDER = 'output/'
    )
    app.template_folder = new_template_folder
    app._static_folder = new_static_folder
    db.init_app(app)
    migrate.init_app(app, db)

    from .views import view
    app.register_blueprint(view, prefix="/")

    return app