import redis
from flask import current_app


def get_redis_connection()-> redis.Redis:
    return redis.Redis(
        host=current_app.config['REDIS_HOST'],
        port=current_app.config['REDIS_PORT'],
        db=current_app.config['REDIS_DB']
    )
