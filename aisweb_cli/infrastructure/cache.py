import os

import redis

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

class Cache:
  def __init__(self) -> None:
    self.pool = redis.ConnectionPool(host=REDIS_HOST, port=6379, db=0)
    # Check if redis is reachable
    client = redis.Redis(connection_pool=self.pool)
    client.get("xxxx")
    client.close()


  def get(self, key):
    client = redis.Redis(connection_pool=self.pool)
    value = client.get(key)
    client.close()
    return value.decode('utf-8') if value else None

  def set(self, key, value):
    client = redis.Redis(connection_pool=self.pool)
    client.set(key, value)
    client.close()
