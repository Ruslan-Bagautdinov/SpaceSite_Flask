from os import getenv, path

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SECRET_KEY = getenv('SECRET_KEY', 'secret-key')

ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 15))
REFRESH_TOKEN_EXPIRE_MINUTES = int(getenv('REFRESH_TOKEN_EXPIRE_MINUTES', 10080))

MYSQL_HOST = getenv('MYSQL_HOST', 'localhost')
MYSQL_PORT = getenv('MYSQL_PORT', '3306')
MYSQL_USER = getenv('MYSQL_USER', 'user')
MYSQL_PASSWORD = getenv('MYSQL_PASSWORD', 'password')
MYSQL_ROOT_PASSWORD = getenv('MYSQL_ROOT_PASSWORD', 'password')
MYSQL_DATABASE = getenv('MYSQL_DATABASE', 'database')

DATABASE_URL = (f"mysql+pymysql"
                f"://{MYSQL_USER}"
                f":{MYSQL_PASSWORD}"
                f"@{MYSQL_HOST}"
                f"/{MYSQL_DATABASE}")

UNSPLASH_ACCESS_KEY = getenv('UNSPLASH_ACCESS_KEY', 'unsplash-access-key')

BASE_DIR = path.abspath(path.dirname(__file__))
IMAGE_DIR = path.join(BASE_DIR, 'photo')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
