
import os
from os import environ

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
# Enable debug mode.
DEBUG = True
# Connect to the database
SQLALCHEMY_DATABASE_URI = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/government_grant'
# SQLALCHEMY_DATABASE_URI = environ.get('dbURL') or 'mysql+mysqlconnector://admin:lZGENKSGyAK7RO6SnAv7@tap-db.cnfultx0d56f.us-east-1.rds.amazonaws.com:3306/football_competition'
# Turn off the Flask-SQLAlchemy event system and warning
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {'pool_recycle': 299}
