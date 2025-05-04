from .offline import get_offline_features
from .online import get_online_features

def retrieve_features(entity_id: str, feature_names: list, source="offline", date=None):
    if source == "online":
        return get_online_features(entity_id, feature_names)
    else:
        return get_offline_features(entity_id, feature_names, date)
