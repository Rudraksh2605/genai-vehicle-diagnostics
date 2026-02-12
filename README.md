# GenAI-Assisted Development of Vehicle Health & Diagnostics for Software Defined Vehicles

## Problem Statement

Modern Software Defined Vehicles (SDVs) rely heavily on software to monitor and analyze vehicle health parameters such as speed, battery condition, tire pressure, and driving behavior.

Currently, converting a simple vehicle diagnostics requirement into backend services, APIs, simulation data, analytics logic, and Android dashboards is a **manual, time-consuming, and error-prone process**. This problem becomes more severe when OTA (Over-The-Air) updates introduce new vehicle signals, requiring repeated updates across multiple system layers.

This project provides a **GenAI-assisted development framework** that automatically converts a natural language vehicle diagnostics requirement into:
- Working backend services (FastAPI)
- Simulated data streams (async Python)
- Health analytics & early warning engine
- Real-time Android dashboard (Kotlin + Jetpack Compose)

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Natural Language Requirement                  │
│  "Monitor speed, battery SoC, and tire pressure with alerts"    │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│   GenAI Requirement Interpreter     │
│   (Rule-based NLP / LLM stub)      │
│   Extracts: Signals, Services,     │
│   UI Widgets, Alert Types           │
└─────────────────┬───────────────────┘
                  │ JSON Blueprint
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FastAPI Backend                              │
│  ┌──────────┐  ┌──────────────┐  ┌───────────────────────────┐ │
│  │ REST API │  │  Simulator   │  │  Health Analytics Engine  │ │
│  │ Endpoints│  │  (async)     │  │  (Rule-based alerts)      │ │
│  └──────────┘  └──────────────┘  └───────────────────────────┘ │
│  ┌──────────────────┐  ┌─────────────────────────────────────┐ │
│  │  Traceability    │  │  OTA Config (signals_config.json)   │ │
│  │  Mapper          │  │  Dynamic signal definitions         │ │
│  └──────────────────┘  └─────────────────────────────────────┘ │
└─────────────────┬───────────────────────────────────────────────┘
                  │ REST APIs (JSON)
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│              Android App (Kotlin + Jetpack Compose)             │
│  ┌────────────┐  ┌────────────────┐  ┌──────────────────────┐  │
│  │ Dashboard  │  │ Alerts Screen  │  │ MVVM + Retrofit      │  │
│  │ SpeedGauge │  │ Alert Banners  │  │ Coroutines + Flow    │  │
│  │ BatteryBar │  │                │  │                      │  │
│  │ TireCards  │  │                │  │                      │  │
│  └────────────┘  └────────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
genai-vehicle-diagnostics/
│
├── backend/
│   ├── main.py                    # FastAPI entry point
│   ├── api/
│   │   ├── vehicle_routes.py      # Telemetry endpoints
│   │   ├── simulation_routes.py   # Simulation control
│   │   ├── traceability_routes.py # Traceability mapping
│   │   └── config_routes.py       # OTA signal config
│   ├── models/
│   │   └── telemetry.py           # Pydantic data models
│   ├── services/
│   │   └── data_store.py          # In-memory data store
│   ├── simulator/
│   │   └── vehicle_simulator.py   # Async data simulator
│   ├── analytics/
│   │   └── health_analyzer.py     # Rule-based alert engine
│   └── traceability/
│       └── mapper.py              # Requirement→API→UI mapping
│
├── genai_interpreter/
│   └── requirement_parser.py      # NLP requirement parser
│
├── android-app/                   # Kotlin + Jetpack Compose app
│   ├── app/src/main/
│   │   ├── java/com/vehiclediag/app/
│   │   │   ├── MainActivity.kt
│   │   │   ├── data/models/       # Data classes
│   │   │   ├── network/           # Retrofit API client
│   │   │   ├── viewmodel/         # MVVM ViewModels
│   │   │   └── ui/
│   │   │       ├── screens/       # Dashboard, Alerts
│   │   │       ├── components/    # Reusable composables
│   │   │       └── theme/         # Material3 theme
│   │   └── AndroidManifest.xml
│   └── build.gradle.kts
│
├── config/
│   └── signals_config.json        # OTA dynamic signal config
│
├── tests/
│   ├── test_interpreter.py        # Interpreter unit tests
│   ├── test_analytics.py          # Analytics rule tests
│   └── test_api.py                # API integration tests
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── run_backend.bat
└── README.md
```

---

## Setup Instructions

### Prerequisites
- **Python 3.10+**
- **pip** (Python package manager)
- **Android Studio** (for the Android app)
- **Docker** (optional, for containerized deployment)

### Backend Setup

```bash
# 1. Navigate to project directory
cd genai-vehicle-diagnostics

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Start the backend server
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# OR use the convenience script (Windows)
run_backend.bat
```

The API will be available at `http://localhost:8000`.
Interactive docs at `http://localhost:8000/docs`.

### Start Simulation

```bash
# Start vehicle data simulation (generates live telemetry)
curl -X POST http://localhost:8000/vehicle/simulate/start

# Check live data
curl http://localhost:8000/vehicle/all

# View alerts
curl http://localhost:8000/vehicle/alerts

# Stop simulation
curl -X POST http://localhost:8000/vehicle/simulate/stop
```

### Run Tests

```bash
cd genai-vehicle-diagnostics
python -m pytest tests/ -v
```

### Android App Setup

1. Open `android-app/` in **Android Studio**
2. Sync Gradle dependencies
3. Update `BASE_URL` in `RetrofitClient.kt` if not using emulator default
4. Run on emulator or physical device
5. Ensure backend is running on `http://localhost:8000`

### Docker Deployment

```bash
docker-compose up --build
```

---

## API Documentation

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/vehicle/speed` | Current vehicle speed (km/h) |
| `GET`  | `/vehicle/battery` | Battery SoC, voltage, temperature |
| `GET`  | `/vehicle/tire-pressure` | All 4 tire pressures (PSI) |
| `GET`  | `/vehicle/all` | Complete telemetry snapshot |
| `GET`  | `/vehicle/alerts` | Active alerts & warnings |
| `POST` | `/vehicle/simulate/start` | Start data simulation |
| `POST` | `/vehicle/simulate/stop` | Stop data simulation |
| `GET`  | `/vehicle/simulate/status` | Simulation status |
| `GET`  | `/traceability/map` | Requirement→Signal→API→UI mapping |
| `GET`  | `/config/signals` | Dynamic signal configuration |
| `GET`  | `/health` | Health check |
| `GET`  | `/docs` | Swagger UI (interactive) |
| `GET`  | `/redoc` | ReDoc documentation |

### Sample API Responses

**GET /vehicle/all**
```json
{
  "timestamp": "2026-02-12T11:30:00",
  "speed": 72.5,
  "battery": {
    "soc": 82.3,
    "voltage": 391.2,
    "temperature": 27.5,
    "health_status": "Good"
  },
  "tires": {
    "front_left": 31.8,
    "front_right": 32.1,
    "rear_left": 31.5,
    "rear_right": 32.0
  },
  "odometer": 15245.3,
  "engine_status": "running"
}
```

**GET /vehicle/alerts**
```json
[
  {
    "id": "a1b2c3d4-...",
    "alert_type": "tire_pressure_low",
    "severity": "critical",
    "message": "Possible Tire Failure: Front Left tire pressure at 22.3 PSI",
    "signal": "tire_pressure_fl",
    "value": 22.3,
    "threshold": "< 25 PSI",
    "timestamp": "2026-02-12T11:29:55",
    "acknowledged": false
  }
]
```

---

## GenAI Requirement Interpreter

### Sample Input
```
"Monitor vehicle speed, battery SoC, and tire pressure and generate alerts on abnormal behavior."
```

### Generated Blueprint Output
```json
{
  "signals": ["speed", "battery_soc", "tire_pressure"],
  "services": ["health_monitoring", "alert_service"],
  "ui_components": ["speed_gauge", "battery_indicator", "tire_pressure_card"],
  "alerts": ["high_speed_stress", "battery_degradation", "low_battery", "tire_pressure_drop", "tire_failure"],
  "raw_requirement": "Monitor vehicle speed, battery SoC, and tire pressure and generate alerts on abnormal behavior."
}
```

### Usage
```python
from genai_interpreter.requirement_parser import parse_requirement

blueprint = parse_requirement(
    "Monitor vehicle speed, battery SoC, and tire pressure "
    "and generate alerts on abnormal behavior."
)
print(blueprint)
```

---

## Health Analytics Rules

| Rule | Condition | Severity | Alert |
|------|-----------|----------|-------|
| Tire Pressure | Any tire < 25 PSI | Critical | Possible Tire Failure |
| Battery Drop | SoC drops > 5% in 30s window | Critical | Battery Degradation Alert |
| High Speed | Speed > 100 km/h for 10+ seconds | Warning | High Speed Stress Warning |

---

## OTA Feature Adaptability

The system is designed for seamless OTA extensibility through `config/signals_config.json`:

### Adding a New Signal (e.g., Engine Temperature)

1. **Add to `signals_config.json`**:
```json
{
  "id": "engine_temp",
  "name": "Engine Temperature",
  "unit": "°C",
  "min": 0,
  "max": 150,
  "normal_range": [60, 100],
  "ui_widget": "engine_temp_gauge",
  "analytics_rules": [
    {
      "condition": "value > 110",
      "alert_id": "engine_overheating",
      "severity": "critical",
      "message": "Engine Overheating: Temperature exceeds safe limit"
    }
  ]
}
```

2. **Backend** automatically loads the new signal config via `GET /config/signals`
3. **Simulator** can be extended to generate data for the new signal
4. **Analytics** automatically creates rule placeholder from config
5. **Android App** fetches updated config and dynamically renders a new UI card

This architecture ensures that OTA updates to `signals_config.json` propagate across all system layers without code changes.

---

## Screenshots

> **Dashboard Screen** — Real-time vehicle health gauges
> ![Dashboard Screenshot Placeholder]

> **Alerts Screen** — Active warnings and anomaly alerts
> ![Alerts Screenshot Placeholder]

> **Swagger API Docs** — Available at `/docs`
> ![Swagger UI Screenshot Placeholder]

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3.11 + FastAPI |
| Simulation | Async Python (asyncio) |
| Analytics | Rule-based explainable AI |
| Mobile App | Kotlin + Jetpack Compose |
| Architecture | MVVM + Clean Architecture |
| Data | In-memory store (mock fallback) |
| Communication | REST APIs + JSON |
| Containerization | Docker + Docker Compose |

---

## Future Enhancements

- **LLM Integration**: Replace rule-based NLP with actual LLM (GPT/PaLM) for requirement parsing
- **WebSocket Support**: Real-time push updates instead of polling
- **SQLite/PostgreSQL**: Persistent storage for telemetry and alerts
- **Predictive Analytics**: ML-based failure prediction
- **V2X Communication**: Vehicle-to-everything data integration
- **Multi-vehicle Fleet Dashboard**: Monitor multiple vehicles simultaneously
- **CI/CD Pipeline**: Automated testing, building, and deployment

---

## License

This project is developed for educational and demonstration purposes.
