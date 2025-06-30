import redis
import json
from datetime import datetime

# Making the Redis Connection
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

CACHE_FILE = "redis_cache_log.txt"

def log_to_file(key: str, value: list):
    """Append cached data to a local file for backup/debug."""
    try:
        with open(CACHE_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n[{datetime.utcnow().isoformat()}] CACHED KEY: {key}")
            f.write(json.dumps(value, indent=2))
            f.write("\n" + "="*60 + "\n")
    except Exception as e:
        print(f"⚠️ Failed to log cache to file: {e}")

def get_reviews_from_cache(book_id: int):
    key = f"book:{book_id}:reviews"
    try:
        data = r.get(key)
        if data:
            return json.loads(data)
    except redis.exceptions.RedisError:
        pass
    return None

def set_reviews_in_cache(book_id: int, reviews: list):
    key = f"book:{book_id}:reviews"

    try:
        # Convert datetime to string for JSON
        def serializer(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Type {type(obj)} not serializable")

        json_data = json.dumps(reviews, default=serializer)
        r.setex(key, 60 * 5, json_data)

        #Save to local log
        log_to_file(key, reviews)

    except redis.exceptions.RedisError:
        #Save to log anyway even if Redis fails
        log_to_file(key, reviews)
