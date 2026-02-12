"""
Unit tests for the Health Analytics & Early Warning Engine.
Tests tire pressure, battery degradation, and high speed rules.
"""

import pytest
import sys
import os
from datetime import datetime
from unittest.mock import MagicMock

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.analytics.health_analyzer import HealthAnalyzer
from backend.models.telemetry import (
    VehicleTelemetry,
    BatteryHealth,
    TireStatus,
    AlertSeverity,
)


class MockStore:
    """Mock data store for analytics tests."""

    def __init__(self):
        self.battery_history = []
        self.speed_history = []


class TestHealthAnalyzer:
    """Tests for the HealthAnalyzer class."""

    def setup_method(self):
        self.analyzer = HealthAnalyzer()
        self.store = MockStore()

    def _make_telemetry(
        self,
        speed=60.0,
        battery_soc=85.0,
        tire_fl=32.0,
        tire_fr=31.5,
        tire_rl=31.8,
        tire_rr=32.2,
    ) -> VehicleTelemetry:
        """Helper to create telemetry with custom values."""
        return VehicleTelemetry(
            timestamp=datetime.utcnow().isoformat(),
            speed=speed,
            battery=BatteryHealth(soc=battery_soc),
            tires=TireStatus(
                front_left=tire_fl,
                front_right=tire_fr,
                rear_left=tire_rl,
                rear_right=tire_rr,
            ),
        )

    # ── Tire pressure tests ──────────────────────────────────────────────

    def test_normal_tire_pressure_no_alert(self):
        telemetry = self._make_telemetry(tire_fl=32, tire_fr=31, tire_rl=30, tire_rr=31)
        alerts = self.analyzer.analyze(telemetry, self.store)
        tire_alerts = [a for a in alerts if a.alert_type == "tire_pressure_low"]
        assert len(tire_alerts) == 0

    def test_low_tire_pressure_front_left(self):
        telemetry = self._make_telemetry(tire_fl=22.0)
        alerts = self.analyzer.analyze(telemetry, self.store)
        tire_alerts = [a for a in alerts if a.alert_type == "tire_pressure_low"]
        assert len(tire_alerts) >= 1
        assert tire_alerts[0].severity == AlertSeverity.CRITICAL
        assert "Front Left" in tire_alerts[0].message

    def test_low_tire_pressure_rear_right(self):
        telemetry = self._make_telemetry(tire_rr=20.0)
        alerts = self.analyzer.analyze(telemetry, self.store)
        tire_alerts = [a for a in alerts if "tire_pressure_rr" in a.signal]
        assert len(tire_alerts) == 1
        assert tire_alerts[0].severity == AlertSeverity.CRITICAL

    def test_multiple_low_tires(self):
        telemetry = self._make_telemetry(
            tire_fl=20.0, tire_fr=22.0, tire_rl=30.0, tire_rr=18.0
        )
        alerts = self.analyzer.analyze(telemetry, self.store)
        tire_alerts = [a for a in alerts if a.alert_type == "tire_pressure_low"]
        assert len(tire_alerts) == 3  # fl, fr, rr below threshold

    def test_borderline_tire_pressure(self):
        telemetry = self._make_telemetry(tire_fl=25.0)
        alerts = self.analyzer.analyze(telemetry, self.store)
        tire_alerts = [a for a in alerts if a.alert_type == "tire_pressure_low"]
        assert len(tire_alerts) == 0  # 25.0 is NOT < 25

    # ── Battery degradation tests ────────────────────────────────────────

    def test_no_battery_alert_when_stable(self):
        self.store.battery_history = [
            {"timestamp": datetime.utcnow().timestamp() - 20, "soc": 85.0},
            {"timestamp": datetime.utcnow().timestamp() - 10, "soc": 84.5},
        ]
        telemetry = self._make_telemetry(battery_soc=84.0)
        alerts = self.analyzer.analyze(telemetry, self.store)
        battery_alerts = [a for a in alerts if a.alert_type == "battery_degradation"]
        assert len(battery_alerts) == 0

    def test_battery_rapid_drop_alert(self):
        self.store.battery_history = [
            {"timestamp": datetime.utcnow().timestamp() - 25, "soc": 90.0},
            {"timestamp": datetime.utcnow().timestamp() - 15, "soc": 87.0},
        ]
        telemetry = self._make_telemetry(battery_soc=83.0)
        alerts = self.analyzer.analyze(telemetry, self.store)
        battery_alerts = [a for a in alerts if a.alert_type == "battery_degradation"]
        assert len(battery_alerts) == 1
        assert battery_alerts[0].severity == AlertSeverity.CRITICAL

    def test_no_battery_alert_with_empty_history(self):
        self.store.battery_history = []
        telemetry = self._make_telemetry(battery_soc=50.0)
        alerts = self.analyzer.analyze(telemetry, self.store)
        battery_alerts = [a for a in alerts if a.alert_type == "battery_degradation"]
        assert len(battery_alerts) == 0

    # ── High speed tests ─────────────────────────────────────────────────

    def test_no_speed_alert_at_normal_speed(self):
        now = datetime.utcnow().timestamp()
        self.store.speed_history = [
            {"timestamp": now - i, "speed": 80.0} for i in range(15, 0, -1)
        ]
        telemetry = self._make_telemetry(speed=80.0)
        alerts = self.analyzer.analyze(telemetry, self.store)
        speed_alerts = [a for a in alerts if a.alert_type == "high_speed_stress"]
        assert len(speed_alerts) == 0

    def test_high_speed_sustained_alert(self):
        now = datetime.utcnow().timestamp()
        self.store.speed_history = [
            {"timestamp": now - i, "speed": 110.0} for i in range(15, 0, -1)
        ]
        telemetry = self._make_telemetry(speed=115.0)
        alerts = self.analyzer.analyze(telemetry, self.store)
        speed_alerts = [a for a in alerts if a.alert_type == "high_speed_stress"]
        assert len(speed_alerts) == 1
        assert speed_alerts[0].severity == AlertSeverity.WARNING

    def test_no_speed_alert_with_intermittent_high(self):
        now = datetime.utcnow().timestamp()
        # Mix of high and low speeds
        self.store.speed_history = [
            {"timestamp": now - 10, "speed": 110.0},
            {"timestamp": now - 9, "speed": 105.0},
            {"timestamp": now - 8, "speed": 90.0},  # below threshold
            {"timestamp": now - 7, "speed": 110.0},
            {"timestamp": now - 6, "speed": 105.0},
            {"timestamp": now - 5, "speed": 115.0},
            {"timestamp": now - 4, "speed": 108.0},
            {"timestamp": now - 3, "speed": 112.0},
            {"timestamp": now - 2, "speed": 110.0},
            {"timestamp": now - 1, "speed": 105.0},
        ]
        telemetry = self._make_telemetry(speed=110.0)
        alerts = self.analyzer.analyze(telemetry, self.store)
        speed_alerts = [a for a in alerts if a.alert_type == "high_speed_stress"]
        assert len(speed_alerts) == 0  # not ALL above 100

    def test_no_speed_alert_with_insufficient_history(self):
        now = datetime.utcnow().timestamp()
        self.store.speed_history = [
            {"timestamp": now - 2, "speed": 120.0},
            {"timestamp": now - 1, "speed": 115.0},
        ]
        telemetry = self._make_telemetry(speed=120.0)
        alerts = self.analyzer.analyze(telemetry, self.store)
        speed_alerts = [a for a in alerts if a.alert_type == "high_speed_stress"]
        assert len(speed_alerts) == 0  # less than 10 history entries

    # ── Combined scenarios ───────────────────────────────────────────────

    def test_multiple_alerts_simultaneously(self):
        now = datetime.utcnow().timestamp()
        self.store.speed_history = [
            {"timestamp": now - i, "speed": 120.0} for i in range(15, 0, -1)
        ]
        self.store.battery_history = [
            {"timestamp": now - 25, "soc": 80.0},
            {"timestamp": now - 10, "soc": 76.0},
        ]
        telemetry = self._make_telemetry(
            speed=120.0, battery_soc=70.0, tire_fl=20.0
        )
        alerts = self.analyzer.analyze(telemetry, self.store)
        # Should get at least tire + battery + speed alerts
        alert_types = {a.alert_type for a in alerts}
        assert "tire_pressure_low" in alert_types
        assert "battery_degradation" in alert_types
        assert "high_speed_stress" in alert_types
        assert len(alerts) >= 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
