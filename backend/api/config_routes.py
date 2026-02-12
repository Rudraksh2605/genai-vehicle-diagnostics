"""
Configuration API routes.
Serves the dynamic signal configuration for OTA feature adaptability.
"""

from fastapi import APIRouter
from typing import Any, Dict, List

from backend.services.data_store import DataStore

router = APIRouter(prefix="/config", tags=["Configuration"])


@router.get("/signals", summary="Get dynamic signal configuration")
async def get_signal_config() -> Dict[str, Any]:
    """
    Return the current signal configuration.
    Used by the Android app and backend for OTA feature adaptability.
    Adding a new signal to signals_config.json will automatically
    be reflected here.
    """
    store = DataStore()
    return {
        "signals": [cfg.model_dump() for cfg in store.signal_configs],
        "count": len(store.signal_configs),
    }
