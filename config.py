import os
from os.path import dirname, join

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
DATABASE_URl = os.environ.get("DATABASE_URL")

# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = DATABASE_URl
