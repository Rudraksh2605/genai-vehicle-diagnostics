"""
Unit tests for the GenAI Requirement Interpreter.
Tests signal extraction, service detection, UI widget mapping, and edge cases.
"""

import pytest
import json
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from genai_interpreter.requirement_parser import (
    RequirementParser,
    parse_requirement,
    parse_requirement_json,
)


class TestRequirementParser:
    """Tests for the RequirementParser class."""

    def setup_method(self):
        self.parser = RequirementParser()

    # ── Signal extraction ────────────────────────────────────────────────

    def test_extract_speed_signal(self):
        bp = self.parser.parse("Monitor vehicle speed")
        assert "speed" in bp["signals"]

    def test_extract_battery_signal(self):
        bp = self.parser.parse("Track battery SoC levels")
        assert "battery_soc" in bp["signals"]

    def test_extract_tire_pressure_signal(self):
        bp = self.parser.parse("Check tire pressure readings")
        assert "tire_pressure" in bp["signals"]

    def test_extract_multiple_signals(self):
        bp = self.parser.parse(
            "Monitor vehicle speed, battery SoC, and tire pressure"
        )
        assert "speed" in bp["signals"]
        assert "battery_soc" in bp["signals"]
        assert "tire_pressure" in bp["signals"]

    def test_extract_signals_case_insensitive(self):
        bp = self.parser.parse("MONITOR VEHICLE SPEED AND BATTERY SOC")
        assert "speed" in bp["signals"]
        assert "battery_soc" in bp["signals"]

    # ── Service extraction ───────────────────────────────────────────────

    def test_extract_monitoring_service(self):
        bp = self.parser.parse("Monitor vehicle health diagnostics")
        assert "health_monitoring" in bp["services"]

    def test_extract_alert_service(self):
        bp = self.parser.parse("Generate alerts on abnormal behavior")
        assert "alert_service" in bp["services"]

    def test_extract_multiple_services(self):
        bp = self.parser.parse(
            "Monitor health and generate alerts with logging"
        )
        assert "health_monitoring" in bp["services"]
        assert "alert_service" in bp["services"]
        assert "data_logging" in bp["services"]

    # ── UI component derivation ──────────────────────────────────────────

    def test_ui_components_for_speed(self):
        bp = self.parser.parse("Monitor speed")
        assert "speed_gauge" in bp["ui_components"]

    def test_ui_components_for_battery(self):
        bp = self.parser.parse("Track battery health")
        assert "battery_indicator" in bp["ui_components"]

    def test_ui_components_for_tire(self):
        bp = self.parser.parse("Check tire pressure")
        assert "tire_pressure_card" in bp["ui_components"]

    # ── Alert derivation ─────────────────────────────────────────────────

    def test_alerts_for_speed(self):
        bp = self.parser.parse("Monitor speed")
        assert "high_speed_stress" in bp["alerts"]

    def test_alerts_for_battery(self):
        bp = self.parser.parse("Track battery")
        assert "battery_degradation" in bp["alerts"]

    def test_alerts_for_tire(self):
        bp = self.parser.parse("Check tire pressure")
        assert "tire_pressure_drop" in bp["alerts"]

    # ── Full sample requirement ──────────────────────────────────────────

    def test_full_sample_requirement(self):
        req = (
            "Monitor vehicle speed, battery SoC, and tire pressure "
            "and generate alerts on abnormal behavior."
        )
        bp = self.parser.parse(req)

        assert len(bp["signals"]) == 3
        assert "speed" in bp["signals"]
        assert "battery_soc" in bp["signals"]
        assert "tire_pressure" in bp["signals"]

        assert "health_monitoring" in bp["services"]
        assert "alert_service" in bp["services"]

        assert "speed_gauge" in bp["ui_components"]
        assert "battery_indicator" in bp["ui_components"]
        assert "tire_pressure_card" in bp["ui_components"]

        assert len(bp["alerts"]) > 0

    # ── Edge cases ───────────────────────────────────────────────────────

    def test_empty_requirement(self):
        bp = self.parser.parse("")
        assert bp["signals"] == []
        assert bp["services"] == []

    def test_none_requirement(self):
        bp = self.parser.parse(None)
        assert bp["signals"] == []

    def test_no_matching_signals_defaults(self):
        bp = self.parser.parse("Run the general vehicle diagnostics system")
        # Should fallback to default signals
        assert len(bp["signals"]) > 0

    def test_raw_requirement_preserved(self):
        req = "Test requirement text"
        bp = self.parser.parse(req)
        assert bp["raw_requirement"] == req

    # ── Module-level functions ───────────────────────────────────────────

    def test_parse_requirement_function(self):
        bp = parse_requirement("Monitor speed")
        assert isinstance(bp, dict)
        assert "signals" in bp

    def test_parse_requirement_json_function(self):
        result = parse_requirement_json("Monitor speed")
        assert isinstance(result, str)
        parsed = json.loads(result)
        assert "signals" in parsed

    # ── LLM stub ─────────────────────────────────────────────────────────

    def test_llm_stub_fallback(self):
        bp = self.parser.parse_with_llm_stub("Monitor speed and battery")
        assert "speed" in bp["signals"]
        assert "battery_soc" in bp["signals"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
