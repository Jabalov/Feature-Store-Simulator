import os
import redis
from dotenv import load_dotenv

OFFLINE_STORE_BASE = "data/processed/offline_store/telco"
load_dotenv()

redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    db=0,
    decode_responses=True
)
