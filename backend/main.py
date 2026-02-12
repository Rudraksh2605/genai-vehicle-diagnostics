"""
GenAI-Assisted Vehicle Health & Diagnostics — Backend Entry Point.

FastAPI application that serves:
- Vehicle telemetry REST APIs
- Data simulation control
- Health analytics & alerts
- OTA signal configuration
- Development traceability mapping
"""

import logging
import json
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.vehicle_routes import router as vehicle_router
from backend.api.simulation_routes import router as simulation_router
from backend.api.traceability_routes import router as traceability_router
from backend.api.config_routes import router as config_router

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-8s │ %(name)-30s │ %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ── FastAPI App ──────────────────────────────────────────────────────────────
app = FastAPI(
    title="Vehicle Health & Diagnostics API",
    description=(
        "GenAI-Assisted Development of Vehicle Health & Diagnostics "
        "for Software Defined Vehicles. Provides real-time vehicle "
        "telemetry, health analytics, alerts, and simulation control."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ──────────────────────────────────────────────────────────────────
app.include_router(vehicle_router)
app.include_router(simulation_router)
app.include_router(traceability_router)
app.include_router(config_router)


# ── Root & Health ────────────────────────────────────────────────────────────
@app.get("/", tags=["System"])
async def root():
    """API root — returns service info."""
    return {
        "service": "Vehicle Health & Diagnostics API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
        "endpoints": {
            "vehicle": "/vehicle/all",
            "speed": "/vehicle/speed",
            "battery": "/vehicle/battery",
            "tire_pressure": "/vehicle/tire-pressure",
            "alerts": "/vehicle/alerts",
            "simulate_start": "/vehicle/simulate/start",
            "simulate_stop": "/vehicle/simulate/stop",
            "simulate_status": "/vehicle/simulate/status",
            "traceability": "/traceability/map",
            "config": "/config/signals",
        },
    }


@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# ── Startup Event ────────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("=" * 60)
    logger.info("Vehicle Health & Diagnostics API starting up")
    logger.info("=" * 60)

    # Pre-initialize the data store (loads config)
    from backend.services.data_store import DataStore
    store = DataStore()
    logger.info(f"Loaded {len(store.signal_configs)} signal configurations")
    logger.info("API documentation available at /docs")
    logger.info("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown."""
    logger.info("Shutting down — stopping simulator if running")
    from backend.simulator.vehicle_simulator import get_simulator
    simulator = get_simulator()
    if simulator.is_running:
        await simulator.stop()
    logger.info("Shutdown complete")
