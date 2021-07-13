import os
from os.path import dirname, join

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

# SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
SECRET_KEY = os.environ.get("SECRET_KEY")
FLASK_ENV = os.environ.get("FLASK_ENV")
FLASK_APP = os.environ.get("FLASK_APP")
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
