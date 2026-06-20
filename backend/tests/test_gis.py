import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from app.main import app
from app.db.session import get_db

client = TestClient(app)

def test_get_gis_layer_success():
    # Mock the DB session
    mock_db = MagicMock()
    
    # Mock the query chain: db.query().filter().all()
    mock_query = MagicMock()
    mock_filter = MagicMock()
    
    # Create mock database objects
    class MockFeature:
        def __init__(self, properties, geom_json):
            self.properties = properties
            self.geom_json = geom_json
            
    mock_feature = MockFeature(
        properties={"risk_level": "high", "name": "Mock Area"},
        geom_json='{"type": "Point", "coordinates": [105.0, 21.0]}'
    )
    
    mock_filter.all.return_value = [mock_feature]
    mock_query.filter.return_value = mock_filter
    mock_db.query.return_value = mock_query

    # Override dependency
    app.dependency_overrides[get_db] = lambda: mock_db

    response = client.get("/api/v1/gis/lsm")
    assert response.status_code == 200
    
    data = response.json()
    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) == 1
    assert data["features"][0]["properties"]["risk_level"] == "high"
    assert data["features"][0]["geometry"]["type"] == "Point"

    # Clean up override
    app.dependency_overrides.clear()
