import fakeredis
from feature_retrieval.online import get_online_features

def test_get_online_features():
    r = fakeredis.FakeStrictRedis()
    r.set("7590-VHVEG:monthly_charges", "75.3")

    from feature_retrieval.config import redis_client
    redis_client = r  

    result = get_online_features("7590-VHVEG", ["monthly_charges"])
    assert result["monthly_charges"] == "75.3"
