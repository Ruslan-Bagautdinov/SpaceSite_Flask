import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SECRET_KEY = os.environ.get('SECRET_KEY')

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
