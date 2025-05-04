from fastapi.testclient import TestClient
from feature_serving.main import app

client = TestClient(app)

def test_get_offline_route():
    response = client.get("/features/offline", params={
        "entity_id": "7590-VHVEG", "features": ["monthly_charges"]
    })
    assert response.status_code == 200
    assert "monthly_charges" in response.json()["features"]
    assert isinstance(response.json()["features"]["monthly_charges"], (int, float))