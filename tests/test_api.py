"""
Tests for the Structural Engineering Analyzer API.
"""

from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_root_endpoint():
    """Test that the API root endpoint is working."""

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"


def test_health_endpoint():
    """Test the API health endpoint."""

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


def test_beam_calculation_endpoint():
    """Test the beam calculation API endpoint."""

    response = client.post(
        "/calculate/beam",
        json={
            "beam_width": 300,
            "overall_depth": 500,
            "concrete_cover": 25,
            "main_bar_diameter": 16,
            "dead_load": 10,
            "live_load": 5,
            "span": 5,
            "concrete_strength": 25,
            "steel_strength": 500,
            "link_diameter": 8
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)


def test_column_calculation_endpoint():
    """Test the column calculation API endpoint."""

    response = client.post(
        "/calculate/column",
        json={
            "column_width": 300,
            "column_depth": 300,
            "dead_load": 100,
            "live_load": 50,
            "concrete_strength": 25,
            "steel_strength": 500,
            "preferred_bar_diameter": 16
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)


def test_invalid_beam_input():
    """Test that invalid beam input is rejected."""

    response = client.post(
        "/calculate/beam",
        json={
            "beam_width": 0,
            "overall_depth": 500,
            "concrete_cover": 25,
            "main_bar_diameter": 16,
            "dead_load": 10,
            "live_load": 5,
            "span": 5
        }
    )

    assert response.status_code == 422


def test_invalid_column_input():
    """Test that invalid column input is rejected."""

    response = client.post(
        "/calculate/column",
        json={
            "column_width": 0,
            "column_depth": 300,
            "dead_load": 100,
            "live_load": 50
        }
    )

    assert response.status_code == 422
