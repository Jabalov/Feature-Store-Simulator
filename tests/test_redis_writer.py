import fakeredis
from feature_retrieval.redis_writer import write_features_to_redis

def test_write_features_to_redis():
    r = fakeredis.FakeStrictRedis()
    from feature_retrieval.config import redis_client
    redis_client = r  
    features = {"tenure_months": 30}
    write_features_to_redis("0001-XYZ", features)

    assert r.get("0001-XYZ:tenure_months") == b"30"
    assert r.get("0001-XYZ:monthly_charges") is None  
    assert r.get("0001-XYZ:tenure_months") == b"30" 