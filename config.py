from os import getenv, path

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SECRET_KEY = getenv('SECRET_KEY')

ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
REFRESH_TOKEN_EXPIRE_MINUTES = int(getenv('REFRESH_TOKEN_EXPIRE_MINUTES'))

UNSPLASH_ACCESS_KEY = getenv('UNSPLASH_ACCESS_KEY')

BASE_DIR = path.abspath(path.dirname(__file__))
IMAGE_DIR = path.join(BASE_DIR, 'photo')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
