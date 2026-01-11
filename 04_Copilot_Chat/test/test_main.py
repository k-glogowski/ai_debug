import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app

client = TestClient(app)


def test_read_root():
    """Test the root endpoint returns correct response."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_read_root_response_structure():
    """Test the root endpoint response structure."""
    response = client.get("/")
    data = response.json()
    assert "Hello" in data
    assert isinstance(data["Hello"], str)


def test_read_root_headers():
    """Test the root endpoint returns JSON content type."""
    response = client.get("/")
    assert response.headers["content-type"] == "application/json"
