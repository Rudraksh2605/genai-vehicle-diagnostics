"""
Vehicle API routes.
Endpoints for fetching vehicle telemetry data and alerts.
"""

from fastapi import APIRouter, Query
from typing import Optional

from backend.services.data_store import DataStore
from backend.models.telemetry import VehicleTelemetry, BatteryHealth, TireStatus, AlertModel

router = APIRouter(prefix="/vehicle", tags=["Vehicle Telemetry"])


@router.get("/speed", summary="Get current vehicle speed")
async def get_speed() -> dict:
    """Return the current vehicle speed in km/h."""
    store = DataStore()
    return {
        "speed": store.telemetry.speed,
        "unit": "km/h",
        "timestamp": store.telemetry.timestamp,
    }


@router.get("/battery", summary="Get battery health status")
async def get_battery() -> BatteryHealth:
    """Return the current battery state of charge and health."""
    store = DataStore()
    return store.telemetry.battery


@router.get("/tire-pressure", summary="Get tire pressure status")
async def get_tire_pressure() -> TireStatus:
    """Return the current tire pressure for all four tires."""
    store = DataStore()
    return store.telemetry.tires


@router.get("/all", summary="Get all vehicle telemetry")
async def get_all_telemetry() -> VehicleTelemetry:
    """Return the complete vehicle telemetry snapshot."""
    store = DataStore()
    return store.telemetry


@router.get("/alerts", summary="Get active vehicle alerts")
async def get_alerts(limit: Optional[int] = Query(50, ge=1, le=200)) -> list[AlertModel]:
    """Return the most recent vehicle alerts."""
    store = DataStore()
    return store.get_alerts(limit=limit)
