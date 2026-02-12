"""
Health Analytics & Early Warning Engine.
Rule-based explainable analytics for vehicle health monitoring.
Detects anomalies in tire pressure, battery SoC, and speed.
"""

import uuid
import logging
from datetime import datetime
from typing import List

from backend.models.telemetry import (
    VehicleTelemetry,
    AlertModel,
    AlertSeverity,
)

logger = logging.getLogger(__name__)


class HealthAnalyzer:
    """
    Rule-based health analytics engine.

    Rules:
    1. Tire pressure < 25 PSI → "Possible Tire Failure" (critical)
    2. Battery SoC drops rapidly (>5% in 30 seconds) → "Battery Degradation" (critical)
    3. Speed > 100 km/h continuously for 10+ seconds → "High Speed Stress Warning" (warning)
    """

    def analyze(self, telemetry: VehicleTelemetry, store) -> List[AlertModel]:
        """
        Run all analytics rules against the current telemetry.
        Returns list of newly generated alerts.
        """
        alerts: List[AlertModel] = []

        # Rule 1: Tire pressure checks
        alerts.extend(self._check_tire_pressure(telemetry))

        # Rule 2: Battery rapid drop
        alert = self._check_battery_degradation(telemetry, store)
        if alert:
            alerts.append(alert)

        # Rule 3: Sustained high speed
        alert = self._check_high_speed(telemetry, store)
        if alert:
            alerts.append(alert)

        return alerts

    def _check_tire_pressure(self, telemetry: VehicleTelemetry) -> List[AlertModel]:
        """Check all four tire pressures against threshold."""
        alerts = []
        tire_map = {
            "tire_pressure_fl": ("Front Left", telemetry.tires.front_left),
            "tire_pressure_fr": ("Front Right", telemetry.tires.front_right),
            "tire_pressure_rl": ("Rear Left", telemetry.tires.rear_left),
            "tire_pressure_rr": ("Rear Right", telemetry.tires.rear_right),
        }

        for signal_id, (label, pressure) in tire_map.items():
            if pressure < 25.0:
                alerts.append(AlertModel(
                    id=str(uuid.uuid4()),
                    alert_type="tire_pressure_low",
                    severity=AlertSeverity.CRITICAL,
                    message=f"Possible Tire Failure: {label} tire pressure at {pressure:.1f} PSI (below 25 PSI threshold)",
                    signal=signal_id,
                    value=pressure,
                    threshold="< 25 PSI",
                    timestamp=telemetry.timestamp,
                ))

        return alerts

    def _check_battery_degradation(self, telemetry: VehicleTelemetry, store) -> AlertModel | None:
        """Check for rapid battery SoC drop (>5% within the tracked window)."""
        history = store.battery_history
        if len(history) < 2:
            return None

        # Compare current SoC with the oldest value in the window
        oldest_soc = history[0]["soc"]
        current_soc = telemetry.battery.soc
        drop = oldest_soc - current_soc

        if drop > 5.0:
            return AlertModel(
                id=str(uuid.uuid4()),
                alert_type="battery_degradation",
                severity=AlertSeverity.CRITICAL,
                message=f"Battery Degradation Alert: SoC dropped {drop:.1f}% (from {oldest_soc:.1f}% to {current_soc:.1f}%)",
                signal="battery_soc",
                value=current_soc,
                threshold="> 5% drop in monitoring window",
                timestamp=telemetry.timestamp,
            )
        return None

    def _check_high_speed(self, telemetry: VehicleTelemetry, store) -> AlertModel | None:
        """Check for sustained high speed (>100 km/h for 10+ consecutive seconds)."""
        history = store.speed_history
        if len(history) < 10:
            return None

        # Check if all entries in the last 10 seconds are above 100 km/h
        recent = history[-10:]
        all_high = all(h["speed"] > 100 for h in recent)

        if all_high:
            return AlertModel(
                id=str(uuid.uuid4()),
                alert_type="high_speed_stress",
                severity=AlertSeverity.WARNING,
                message=f"High Speed Stress Warning: Vehicle sustained speed above 100 km/h (current: {telemetry.speed:.1f} km/h)",
                signal="speed",
                value=telemetry.speed,
                threshold="> 100 km/h sustained for 10+ seconds",
                timestamp=telemetry.timestamp,
            )
        return None
