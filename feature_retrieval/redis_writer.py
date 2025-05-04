from .config import redis_client
from typing import Dict
from datetime import datetime

def write_features_to_redis(entity_id: str, features: Dict[str, any]):
    for feature_name, value in features.items():
        key = f"{entity_id}:{feature_name}"
        redis_client.set(key, value)
        redis_client.set(f"{key}:timestamp", datetime.utcnow().isoformat())
        print(f"[✓] Redis Updated → {key} = {value}")