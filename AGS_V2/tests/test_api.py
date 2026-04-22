import pytest
from fastapi.testclient import TestClient
from api import app
from core.db import create_db_and_tables

@pytest.fixture(autouse=True)
def setup_database():
    create_db_and_tables()
    yield

client = TestClient(app)

def test_stream_endpoint():
    with client.stream("GET", "/stream") as response:
        assert response.status_code == 200
        for line in response.iter_lines():
            if line:
                assert line.startswith("data:")
                break
