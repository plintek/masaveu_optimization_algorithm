import json
import redis
import pickle

types = ["routes", "here"]
is_in_local = True

host = "localhost" if is_in_local else "cache"
here_cache = redis.Redis(host=host, port=6379, db=0)
routes_cache = redis.Redis(host=host, port=6379, db=1)

expiration_time = 600000


class CacheUtility:
    @staticmethod
    def write_cache(key, value, type):
        if type == "routes":
            key = json.dumps(key)

        here_cache.set(key, pickle.dumps(value), ex=expiration_time)

    @staticmethod
    def read_cache(key, type):
        if type == "routes":
            key = json.dumps(key)

        result = here_cache.get(key)
        here_cache.expire(key, expiration_time)
        if result:
            return pickle.loads(result)

        return None
