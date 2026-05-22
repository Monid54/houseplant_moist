# houseplant_moist
Houseplant Moisture Monitor
=============================
A fully automated IoT plant monitoring system built with:
- ESP32-C3 soil moisture sensor
- Raspberry Pi backend (FastAPI + SQLite)
- Automated daily JSON exports to GitHub
- PlantCare web dashboard (HTML/CSS/JS + Chart.js)

This repository contains firmware, backend code, frontend, and generated datasets.

--------------------------------------------------
Architecture
--------------------------------------------------
ESP32 Sensor -> HTTP POST -> Raspberry Pi (FastAPI)
                                  |
                               SQLite
                                  |
                    Daily JSON export -> GitHub
                                  |
                        PlantCare Web Dashboard

--------------------------------------------------
Live Data
--------------------------------------------------
Latest measurements (last 14 days) in hourly buckets:
exports/latest.json

Daily snapshots:
exports/daily/YYYY-MM-DD.json

These files are automatically updated every night.

--------------------------------------------------
Repository Structure
--------------------------------------------------
backend/        FastAPI backend (app.py, plant.db)
esp32/          ESP32 firmware (sensor_1.ino)
frontend/       PlantCare web dashboard
scripts/        Export and automation scripts
exports/        Generated sensor data (JSON)

--------------------------------------------------
Hardware
--------------------------------------------------
- ESP32-C3 Super Mini
- Capacitive soil moisture sensor V2.0
- USB powered

Sampling interval: 15 minutes

--------------------------------------------------
Backend API
--------------------------------------------------
Health check
GET /health

Ingest sensor data
POST /ingest
Content-Type: application/json

Example payload:
{
  "sensor_id": "plant1",
  "raw": 512,
  "moisture": 42,
  "rssi": -55
}

All readings for a sensor
GET /readings?sensor_id=plant1&limit=100

Latest reading
GET /latest?sensor_id=plant1

--------------------------------------------------
Data Format
--------------------------------------------------
Example entry:
{
  "sensor_id": "plant1",
  "ts": "2026-02-22T18:34:20Z",
  "raw": 446,
  "moisture": 32,
  "vcc": null,
  "rssi": -61
}

Fields:
sensor_id   Sensor identifier
ts          ISO8601 timestamp (UTC)
raw         Raw ADC value (0–4095)
moisture    Calibrated percentage (0–100)
vcc         Supply voltage (unused, null)
rssi        WiFi signal strength (dBm)

--------------------------------------------------
Automation
--------------------------------------------------
A systemd timer on the Raspberry Pi:
- Exports database to JSON
- Commits changes
- Pushes to GitHub daily

Default execution time: 02:30 CET

--------------------------------------------------
Security
--------------------------------------------------
Sensitive data excluded from repository:
- WiFi credentials (secrets.h)
- SQLite database (plant.db)
- Environment files

--------------------------------------------------
Use Cases
--------------------------------------------------
- Plant watering alerts
- Long-term soil moisture monitoring
- IoT experimentation
- Web dashboard visualisation
- Data analysis of plant hydration

--------------------------------------------------
Development
--------------------------------------------------
Requirements:
- ESP32 Arduino framework
- Python 3.11+
- FastAPI
- SQLite

--------------------------------------------------
Roadmap
--------------------------------------------------
- Dynamic multi-sensor dashboard (FR-10b)
- Backend authentication (FR-11)
- Sensor inactivity notifications (FR-12)
- Battery-powered nodes with deep sleep
- Cloud synchronisation

--------------------------------------------------
License
--------------------------------------------------
MIT (recommended for educational and open hardware projects)

--------------------------------------------------
Authors
--------------------------------------------------
ZHAW – Software Engineering and Design Patterns, May 2026

Simon Schmid – Project Lead / Backend / Architecture
Cédric Müller – Backend ↔ Frontend Integration
Michael Ogar – Frontend / UI
Alex Filo – Software Design / UML / QA
