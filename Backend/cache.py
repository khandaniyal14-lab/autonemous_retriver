import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

def get_cache(query):
    key = f"query:{query}"
    if r.exists(key):
        return json.loads(r.get(key))
    return None

def set_cache(query, results):
    key = f"query:{query}"
    r.setex(key, 3600, json.dumps(results))