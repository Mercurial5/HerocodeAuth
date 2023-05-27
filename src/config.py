from os import environ
from dotenv import load_dotenv

load_dotenv()

class PostgreSQLConfig:
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class RedisConfig:
    REDIS_HOST = environ.get('REDIS_HOST')
    REDIS_PORT = int(environ.get('REDIS_PORT'))
    REDIS_DB = int(environ.get('REDIS_DB'))
    REDIS_EXPIRATION = int(environ.get('REDIS_EXPIRATION'))