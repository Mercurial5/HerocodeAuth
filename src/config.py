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


class TokenConfig:
    SECRET_KEY = environ.get('SECRET_KEY')
    SECURITY_PASSWORD_SALT = environ.get('SECURITY_PASSWORD_SALT')
    

class EmailConfig:
    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_PORT = int(environ.get('MAIL_PORT'))
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = environ.get('MAIL_DEFAULT_SENDER')
