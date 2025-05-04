from .config import redis_client
from typing import List

def get_online_features(entity_id: str, feature_names: List[str]):
    result = {}
    for feature in feature_names:
        key = f"{entity_id}:{feature}"
        value = redis_client.get(key)
        if value is not None:
            result[feature] = value
    return result
