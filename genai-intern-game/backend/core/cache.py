import redis
import os

# Loading Redis connection details from the environment file
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# This creates a connection to the Redis server
cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

# This function stores a result in the cache
def cache_guess_verdict(session_id: str, guess: str, result: str):
    key = f"{session_id}:{guess}"                                          # Unique key for each session+guess
    cache.set(key, result, ex=86400)                                       # Store it for 24 hours

# This function retrieves a cached result if it exists
def get_cached_verdict(session_id: str, guess: str) -> str:
    key = f"{session_id}:{guess}"
    return cache.get(key)   

