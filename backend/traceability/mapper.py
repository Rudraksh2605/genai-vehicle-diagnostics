"""
Development Traceability Mapping Engine.
Maps requirements → extracted signals → generated APIs → UI components.
"""

import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class TraceabilityMapper:
    """
    Stores and manages the traceability mapping from requirement
    to signals, APIs, and UI components.
    """

    def __init__(self) -> None:
        self._maps: List[Dict[str, Any]] = []
        # Pre-populate with the default system mapping
        self._add_default_mapping()

    def _add_default_mapping(self) -> None:
        """Add the default system traceability map."""
        self._maps.append({
            "requirement": "Monitor vehicle speed, battery SoC, and tire pressure and generate alerts on abnormal behavior.",
            "extracted_signals": [
                {
                    "signal": "speed",
                    "api_endpoint": "GET /vehicle/speed",
                    "ui_component": "SpeedGauge",
                    "analytics_rule": "speed > 100 km/h sustained → High Speed Stress Warning",
                },
                {
                    "signal": "battery_soc",
                    "api_endpoint": "GET /vehicle/battery",
                    "ui_component": "BatteryIndicator",
                    "analytics_rule": "SoC drop > 5% rapidly → Battery Degradation Alert",
                },
                {
                    "signal": "tire_pressure",
                    "api_endpoint": "GET /vehicle/tire-pressure",
                    "ui_component": "TirePressureCard",
                    "analytics_rule": "pressure < 25 PSI → Possible Tire Failure",
                },
            ],
            "generated_services": [
                "health_monitoring",
                "alert_service",
                "simulation_service",
            ],
            "generated_apis": [
                "GET /vehicle/speed",
                "GET /vehicle/battery",
                "GET /vehicle/tire-pressure",
                "GET /vehicle/all",
                "GET /vehicle/alerts",
                "POST /vehicle/simulate/start",
                "POST /vehicle/simulate/stop",
                "GET /traceability/map",
                "GET /config/signals",
            ],
            "ui_components": [
                "SpeedGauge",
                "BatteryIndicator",
                "TirePressureCard",
                "AlertBanner",
            ],
        })

    def add_mapping(self, requirement: str, blueprint: Dict[str, Any]) -> None:
        """Add a new traceability entry from a parsed requirement."""
        mapping = {
            "requirement": requirement,
            "extracted_signals": [],
            "generated_services": blueprint.get("services", []),
            "generated_apis": [],
            "ui_components": blueprint.get("ui_components", []),
        }

        for signal in blueprint.get("signals", []):
            entry = {
                "signal": signal,
                "api_endpoint": f"GET /vehicle/{signal.replace('_', '-')}",
                "ui_component": self._signal_to_widget(signal),
                "analytics_rule": f"Auto-generated rule for {signal}",
            }
            mapping["extracted_signals"].append(entry)
            mapping["generated_apis"].append(entry["api_endpoint"])

        self._maps.append(mapping)
        logger.info(f"Traceability mapping added for requirement: {requirement[:60]}...")

    def _signal_to_widget(self, signal: str) -> str:
        """Map a signal name to a UI widget name."""
        widget_map = {
            "speed": "SpeedGauge",
            "battery_soc": "BatteryIndicator",
            "tire_pressure": "TirePressureCard",
        }
        return widget_map.get(signal, f"{signal.title().replace('_', '')}Card")

    def get_map(self) -> List[Dict[str, Any]]:
        """Get the full traceability mapping."""
        return self._maps

    def get_latest(self) -> Dict[str, Any] | None:
        """Get the most recent traceability entry."""
        return self._maps[-1] if self._maps else None


# Module-level singleton
_mapper = TraceabilityMapper()


def get_mapper() -> TraceabilityMapper:
    """Get the singleton traceability mapper."""
    return _mapper
