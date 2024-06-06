from cachetools import TTLCache

cache = TTLCache(maxsize=100, ttl=300)  # Cache with a TTL of 5 minutes
