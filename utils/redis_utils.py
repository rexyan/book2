# encoding=utf8

import redis
import settings

pool = redis.ConnectionPool(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


def get_redis_conn():
    return redis.Redis(connection_pool=pool)


def redis_set(key, value, time=None):
    con = get_redis_conn()
    result = None
    if time:
        result = con.set(key, value)
        con.expire(key, time)
    else:
        result = con.set(key, value)
    return result


def redis_get(key):
    con = get_redis_conn()
    return con.get(key)


def redis_delete(key):
    con = get_redis_conn()
    con.delete(key)
