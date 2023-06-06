from typing import Optional, Dict
from redis import Redis
from flask import current_app
from cache.redis_db import get_redis_connection


def cache_user_data(token, redis_data) -> None:
    redis_conn: Redis = get_redis_connection()
    redis_conn.hmset(token, redis_data)
    redis_conn.expire(token, current_app.config['REDIS_EXPIRATION'])


def get_cached_user_data(token: str) -> Optional[Dict[str, str]]:
    redis_conn: Redis = get_redis_connection()
    redis_data_in_bytes = redis_conn.hgetall(token)
    redis_data: Optional[Dict[str, str]] = {key.decode(): value.decode() for key, value in redis_data_in_bytes.items()}
    return redis_data


def set_done(token: str) -> None:
    redis_conn: Redis = get_redis_connection()
    redis_conn.hset(token, 'verified', 'True')

def is_verified(redis_data: Dict[str, str]) -> bool:
    if redis_data.get('verified') == 'True':
        return True
    return False 
