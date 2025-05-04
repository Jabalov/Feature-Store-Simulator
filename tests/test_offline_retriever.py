import pytest
from feature_retrieval.offline import get_offline_features

def test_get_offline_features_existing_id():
    entity_id = "7590-VHVEG"
    result = get_offline_features(entity_id, ["tenure_months"])
    assert "tenure_months" in result
    assert isinstance(result["tenure_months"], (int, float))
    