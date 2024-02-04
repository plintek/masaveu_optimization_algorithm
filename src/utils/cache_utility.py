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
    """
    Utility class for caching data.
    """

    @staticmethod
    def write_cache(key, value, type):
        """
        Writes data to the cache.

        Args:
            key (str): The cache key.
            value (Any): The data to be cached.
            type (str): The type of data being cached.

        Returns:
            None
        """
        if type == "routes":
            key = json.dumps(key)

        try:
            here_cache.set(key, pickle.dumps(value), ex=expiration_time)
        except:
            print("Error writing cache")

    @staticmethod
    def read_cache(key, type):
        """
        Reads data from the cache.

        Args:
            key (str): The cache key.
            type (str): The type of data being read.

        Returns:
            Any: The cached data, or None if not found.
        """
        try:
            if type == "routes":
                key = json.dumps(key)

            result = here_cache.get(key)
            here_cache.expire(key, expiration_time)
            if result:
                return pickle.loads(result)
        except:
            return None

        return None
