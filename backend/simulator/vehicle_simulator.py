"""
Vehicle Data Simulation Engine.
Generates realistic vehicle telemetry data every 1 second using asyncio.
Supports start/stop via API and pushes data to the in-memory data store.
"""

import asyncio
import random
import logging
import uuid
from datetime import datetime
from typing import Optional

from backend.models.telemetry import (
    VehicleTelemetry,
    BatteryHealth,
    TireStatus,
    SimulationStatus,
)
from backend.services.data_store import DataStore
from backend.analytics.health_analyzer import HealthAnalyzer

logger = logging.getLogger(__name__)


class VehicleSimulator:
    """
    Async vehicle data simulator.
    Generates realistic telemetry with:
    - Speed: 0-120 km/h dynamic variation with acceleration/deceleration
    - Battery SoC: slow gradual decline with occasional rapid drops
    - Tire pressure: normal range with occasional sudden drop events
    """

    def __init__(self) -> None:
        self.store = DataStore()
        self.analyzer = HealthAnalyzer()
        self._task: Optional[asyncio.Task] = None
        self._running = False
        self._tick_count = 0

        # Simulation state variables
        self._speed = 0.0
        self._battery_soc = 95.0
        self._battery_voltage = 400.0
        self._battery_temp = 25.0
        self._tire_fl = 32.0
        self._tire_fr = 31.5
        self._tire_rl = 31.8
        self._tire_rr = 32.2
        self._odometer = 15000.0
        self._speed_direction = 1  # 1 = accelerating, -1 = decelerating

    @property
    def is_running(self) -> bool:
        return self._running

    async def start(self) -> SimulationStatus:
        """Start the simulation background task."""
        if self._running:
            return SimulationStatus(
                running=True,
                tick_count=self._tick_count,
                start_time=self.store.simulation.start_time,
                message="Simulator already running",
            )

        self._running = True
        self._tick_count = 0
        start_time = datetime.utcnow().isoformat()

        self.store.simulation = SimulationStatus(
            running=True,
            tick_count=0,
            start_time=start_time,
            message="Simulator started",
        )

        self._task = asyncio.create_task(self._simulation_loop())
        logger.info("Vehicle simulator started")

        return self.store.simulation

    async def stop(self) -> SimulationStatus:
        """Stop the simulation background task."""
        if not self._running:
            return SimulationStatus(
                running=False,
                tick_count=self._tick_count,
                message="Simulator not running",
            )

        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None

        self.store.simulation = SimulationStatus(
            running=False,
            tick_count=self._tick_count,
            message=f"Simulator stopped after {self._tick_count} ticks",
        )

        logger.info(f"Vehicle simulator stopped after {self._tick_count} ticks")
        return self.store.simulation

    async def _simulation_loop(self) -> None:
        """Main simulation loop — generates data every 1 second."""
        logger.info("Simulation loop started")
        try:
            while self._running:
                self._tick_count += 1
                telemetry = self._generate_telemetry()

                # Update data store
                self.store.update_telemetry(telemetry)

                # Run analytics on the new telemetry
                new_alerts = self.analyzer.analyze(telemetry, self.store)
                for alert in new_alerts:
                    self.store.add_alert(alert)

                # Update simulation status
                self.store.simulation.tick_count = self._tick_count

                await asyncio.sleep(1)
        except asyncio.CancelledError:
            logger.info("Simulation loop cancelled")
            raise

    def _generate_telemetry(self) -> VehicleTelemetry:
        """Generate a single telemetry snapshot with realistic variations."""

        # --- Speed simulation ---
        # Change direction periodically
        if random.random() < 0.05:
            self._speed_direction *= -1

        speed_delta = random.uniform(1.0, 5.0) * self._speed_direction
        self._speed = max(0, min(140, self._speed + speed_delta))

        # Occasionally hold high speed for alert testing
        if self._tick_count % 50 < 15 and self._tick_count > 20:
            self._speed = random.uniform(105, 130)

        # --- Battery simulation ---
        # Slow gradual decline
        self._battery_soc -= random.uniform(0.05, 0.2)

        # Occasional rapid drop event (for alert testing)
        if random.random() < 0.02:
            self._battery_soc -= random.uniform(5.0, 8.0)
            logger.debug("Battery rapid drop event triggered")

        self._battery_soc = max(5.0, min(100.0, self._battery_soc))
        self._battery_voltage = 350 + (self._battery_soc / 100) * 50
        self._battery_temp = 25 + random.uniform(-2, 5)

        health_status = "Good"
        if self._battery_soc < 20:
            health_status = "Low"
        elif self._battery_soc < 50:
            health_status = "Fair"

        # --- Tire pressure simulation ---
        # Small random fluctuations
        self._tire_fl += random.uniform(-0.1, 0.1)
        self._tire_fr += random.uniform(-0.1, 0.1)
        self._tire_rl += random.uniform(-0.1, 0.1)
        self._tire_rr += random.uniform(-0.1, 0.1)

        # Occasional sudden drop event (for alert testing)
        if random.random() < 0.01:
            tire_choice = random.choice(["fl", "fr", "rl", "rr"])
            drop = random.uniform(8, 15)
            if tire_choice == "fl":
                self._tire_fl -= drop
            elif tire_choice == "fr":
                self._tire_fr -= drop
            elif tire_choice == "rl":
                self._tire_rl -= drop
            else:
                self._tire_rr -= drop
            logger.debug(f"Tire pressure sudden drop on {tire_choice}")

        # Clamp tire pressures
        self._tire_fl = max(15.0, min(40.0, self._tire_fl))
        self._tire_fr = max(15.0, min(40.0, self._tire_fr))
        self._tire_rl = max(15.0, min(40.0, self._tire_rl))
        self._tire_rr = max(15.0, min(40.0, self._tire_rr))

        # --- Odometer ---
        self._odometer += (self._speed / 3600)  # km per second

        return VehicleTelemetry(
            timestamp=datetime.utcnow().isoformat(),
            speed=round(self._speed, 1),
            battery=BatteryHealth(
                soc=round(self._battery_soc, 1),
                voltage=round(self._battery_voltage, 1),
                temperature=round(self._battery_temp, 1),
                health_status=health_status,
            ),
            tires=TireStatus(
                front_left=round(self._tire_fl, 1),
                front_right=round(self._tire_fr, 1),
                rear_left=round(self._tire_rl, 1),
                rear_right=round(self._tire_rr, 1),
            ),
            odometer=round(self._odometer, 1),
            engine_status="running",
        )


# Module-level singleton
_simulator: Optional[VehicleSimulator] = None


def get_simulator() -> VehicleSimulator:
    """Get or create the singleton simulator instance."""
    global _simulator
    if _simulator is None:
        _simulator = VehicleSimulator()
    return _simulator
