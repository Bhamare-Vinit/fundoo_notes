from django.conf import settings
from django.core.cache import cache
import json
from loguru import logger

class RedisUtils:
    """
    Utility class for interacting with Redis cache.

    Attributes:
        cache (object): An instance of a Redis cache client.
    """
    def __init__(self):
        self.cache = cache
    def save(self,key,value,ex=None):
        """
        Saves a value to the cache with a specified key.

        Args:
            key (str): The key under which the value is stored.
            value (any): The value to be cached.
            ex (int, optional): The expiration time in seconds. Defaults to None.
        """
        serialized_value = json.dumps(value)
        self.cache.set(key,serialized_value, ex)
        logger.info(f"Saved to cache: {key} -> {serialized_value}")
    def get(self,key):
        """
        Retrieves a value from the cache by its key.

        Args:
            key (str): The key for the value to be retrieved.

        Returns:
            any: The deserialized value if found, otherwise None.
        """
        value = self.cache.get(key) 
        if value:
            deserialized_value = json.loads(value)
            logger.info(f"Fetched from cache: {key} -> {deserialized_value}")
            return deserialized_value
        logger.info(f"Cache miss for key: {key}")
        return None
    def delete(self,key):
        """
        Deletes a value from the cache by its key.

        Args:
            key (str): The key of the value to be deleted.
        """
        self.cache.delete(key)
