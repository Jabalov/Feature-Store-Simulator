import os
import redis
from dotenv import load_dotenv

load_dotenv()
OFFLINE_STORE_BASE = str(os.getenv("OFFLINE_STORE_BASE"))


redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    db=0,
    decode_responses=True
)
