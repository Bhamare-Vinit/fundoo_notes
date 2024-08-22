from django.conf import settings
from django.core.cache import cache
import json
from loguru import logger

class RedisUtils:
    def __init__(self):
        self.cache = cache
    def save(self,key,value,ex=None):
        serialized_value = json.dumps(value)
        self.cache.set(key,serialized_value, ex)
        logger.info(f"Saved to cache: {key} -> {serialized_value}")
    def get(self,key):
        value = self.cache.get(key) 
        if value:
            deserialized_value = json.loads(value)
            logger.info(f"Fetched from cache: {key} -> {deserialized_value}")
            return deserialized_value
        logger.info(f"Cache miss for key: {key}")
        return None
    def delete(self,key):
        self.cache.delete(key)
