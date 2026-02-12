"""
Integration tests for Backend FastAPI endpoints.
Uses TestClient to test all vehicle, simulation, traceability, and config endpoints.
"""

import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from backend.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    with TestClient(app) as c:
        yield c


class TestRootEndpoints:
    """Tests for root and health endpoints."""

    def test_root(self, client):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "Vehicle Health & Diagnostics API"
        assert "endpoints" in data

    def test_health_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestVehicleEndpoints:
    """Tests for vehicle telemetry endpoints."""

    def test_get_speed(self, client):
        response = client.get("/vehicle/speed")
        assert response.status_code == 200
        data = response.json()
        assert "speed" in data
        assert "unit" in data
        assert data["unit"] == "km/h"
        assert isinstance(data["speed"], (int, float))

    def test_get_battery(self, client):
        response = client.get("/vehicle/battery")
        assert response.status_code == 200
        data = response.json()
        assert "soc" in data
        assert "voltage" in data
        assert "temperature" in data
        assert "health_status" in data
        assert 0 <= data["soc"] <= 100

    def test_get_tire_pressure(self, client):
        response = client.get("/vehicle/tire-pressure")
        assert response.status_code == 200
        data = response.json()
        assert "front_left" in data
        assert "front_right" in data
        assert "rear_left" in data
        assert "rear_right" in data
        for key in ["front_left", "front_right", "rear_left", "rear_right"]:
            assert isinstance(data[key], (int, float))

    def test_get_all_telemetry(self, client):
        response = client.get("/vehicle/all")
        assert response.status_code == 200
        data = response.json()
        assert "speed" in data
        assert "battery" in data
        assert "tires" in data
        assert "timestamp" in data
        assert "odometer" in data
        assert "engine_status" in data

    def test_get_alerts_empty(self, client):
        response = client.get("/vehicle/alerts")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_alerts_with_limit(self, client):
        response = client.get("/vehicle/alerts?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 5


class TestSimulationEndpoints:
    """Tests for simulation control endpoints."""

    def test_get_simulation_status(self, client):
        response = client.get("/vehicle/simulate/status")
        assert response.status_code == 200
        data = response.json()
        assert "running" in data
        assert "tick_count" in data
        assert "message" in data

    def test_start_simulation(self, client):
        response = client.post("/vehicle/simulate/start")
        assert response.status_code == 200
        data = response.json()
        assert data["running"] is True
        assert "start_time" in data

        # Stop to clean up
        client.post("/vehicle/simulate/stop")

    def test_stop_simulation(self, client):
        # Start first
        client.post("/vehicle/simulate/start")

        response = client.post("/vehicle/simulate/stop")
        assert response.status_code == 200
        data = response.json()
        assert data["running"] is False

    def test_stop_when_not_running(self, client):
        # Ensure stopped
        client.post("/vehicle/simulate/stop")

        response = client.post("/vehicle/simulate/stop")
        assert response.status_code == 200
        data = response.json()
        assert data["running"] is False
        assert "not running" in data["message"].lower()


class TestTraceabilityEndpoints:
    """Tests for traceability mapping endpoint."""

    def test_get_traceability_map(self, client):
        response = client.get("/traceability/map")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

        # Check the default mapping structure
        first = data[0]
        assert "requirement" in first
        assert "extracted_signals" in first
        assert "generated_apis" in first
        assert "ui_components" in first


class TestConfigEndpoints:
    """Tests for signal configuration endpoint."""

    def test_get_signal_config(self, client):
        response = client.get("/config/signals")
        assert response.status_code == 200
        data = response.json()
        assert "signals" in data
        assert "count" in data
        assert isinstance(data["signals"], list)
        assert data["count"] == len(data["signals"])

    def test_signal_config_structure(self, client):
        response = client.get("/config/signals")
        data = response.json()
        if data["count"] > 0:
            signal = data["signals"][0]
            assert "id" in signal
            assert "name" in signal
            assert "unit" in signal
            assert "min" in signal
            assert "max" in signal
            assert "ui_widget" in signal


class TestOpenAPIDoc:
    """Tests for API documentation availability."""

    def test_docs_available(self, client):
        response = client.get("/docs")
        assert response.status_code == 200

    def test_openapi_json(self, client):
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "paths" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
