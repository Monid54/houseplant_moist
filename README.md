# houseplant_moist
Houseplant Moisture Monitor
=============================

A fully automated IoT plant monitoring system built with:
- ESP32-C3 soil moisture sensor
- Raspberry Pi backend (FastAPI + SQLite)
- Automated daily JSON exports to GitHub

This repository contains firmware, backend code, and generated datasets.

--------------------------------------------------
Architecture
--------------------------------------------------
ESP32 Sensor -> HTTP POST -> Raspberry Pi (FastAPI)
                                  |
                               SQLite
                                  |
                    Daily JSON export -> GitHub

--------------------------------------------------
Live Data
--------------------------------------------------
Latest measurements (last 14 days) in hourly buckets, and older measurements in 6-houre buckets:
exports/latest.json

Daily snapshots:
exports/daily/YYYY-MM-DD.json

These files are automatically updated every night.

--------------------------------------------------
Repository Structure
--------------------------------------------------
backend/        FastAPI backend
esp32/          ESP32 firmware
scripts/        Export and automation scripts
exports/        Generated sensor data (JSON)

--------------------------------------------------
Hardware
--------------------------------------------------
- ESP32-C3 Super Mini
- Capacitive soil moisture sensor
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
raw         Raw ADC value
moisture    Calibrated percentage
vcc         Supply voltage (for battery)
rssi        WiFi signal strength

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
Sensitive data excluded:
- WiFi credentials (secrets.h)
- SQLite database
- Environment files

--------------------------------------------------
Use Cases
--------------------------------------------------
- Plant watering alerts
- Long-term soil monitoring
- IoT experimentation
- Web dashboards
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
- Multi-sensor support
- Web dashboard
- Plant health scoring
- Cloud synchronization
- Battery-powered nodes

--------------------------------------------------
License
--------------------------------------------------
MIT (recommended for educational and open hardware projects)

--------------------------------------------------
Author
--------------------------------------------------
Built as an IoT plant monitoring project using ESP32 and Raspberry Pi.
