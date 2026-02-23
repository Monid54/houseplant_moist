from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
import sqlite3
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional
"""
This is the backend application for a plant sensor system.
It uses FastAPI to create a web API that allows clients to ingest sensor readings and retrieve them later.
The data is stored in a SQLite database.
"""

# Here we define the path to the SQLite database file.
# It will be located in the same directory as this script and named "plant.db".
DB_PATH = Path(__file__).with_name("plant.db")

# We create an instance of the FastAPI application, which will be used to define our API endpoints and handle incoming requests.
app = FastAPI(title="Plant Sensor Backend", version="0.1.0")

# This function establishes a connection to the SQLite database.
# It sets the row factory to sqlite3.Row, which allows us to access columns by name.
def db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# This function initializes the database by creating the "readings" table if it doesn't already exist.
def init_db() -> None:
    with db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS readings (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              sensor_id TEXT NOT NULL,
              ts TEXT NOT NULL,
              raw INTEGER,
              moisture INTEGER,
              vcc REAL,
              rssi INTEGER
            );
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_readings_sensor_ts ON readings(sensor_id, ts);"
        )

# The @app.on_event("startup") decorator registers the _startup function to be called when the application starts.
@app.on_event("startup")
def _startup():
    init_db()

# The ReadingIn class defines the expected structure of the incoming data for the /ingest endpoint.
class ReadingIn(BaseModel):
    sensor_id: str = Field(..., min_length=1, max_length=64)
    raw: Optional[int] = Field(None, ge=0, le=4095)
    moisture: Optional[int] = Field(None, ge=0, le=100)
    vcc: Optional[float] = None
    rssi: Optional[int] = None
    ts: Optional[str] = None

# The /health endpoint is a simple health check that returns a JSON response indicating that the service is running.
@app.get("/health")
def health():
    return {"ok": True}

# The /ingest endpoint accepts POST requests with a JSON body that matches the ReadingIn model.
@app.post("/ingest")
def ingest(r: ReadingIn):
    ts = r.ts or datetime.now(timezone.utc).isoformat()

    if r.raw is None and r.moisture is None:
        raise HTTPException(status_code=400, detail="raw oder moisture muss gesetzt sein")

    with db() as conn:
        conn.execute(
            "INSERT INTO readings(sensor_id, ts, raw, moisture, vcc, rssi) VALUES (?, ?, ?, ?, ?, ?)",
            (r.sensor_id, ts, r.raw, r.moisture, r.vcc, r.rssi),
        )
        conn.commit()

    return {"stored": True, "sensor_id": r.sensor_id, "ts": ts}

# The /readings endpoint allows clients to retrieve readings for a specific sensor_id, with an optional limit on the number of records returned.
@app.get("/readings")
def get_readings(sensor_id: str, limit: int = Query(100, ge=1, le=5000)):
    with db() as conn:
        rows = conn.execute(
            "SELECT sensor_id, ts, raw, moisture, vcc, rssi FROM readings WHERE sensor_id=? ORDER BY ts DESC LIMIT ?",
            (sensor_id, limit),
        ).fetchall()
    return [dict(row) for row in rows]

# The /latest endpoint retrieves the most recent reading for a given sensor_id.
@app.get("/latest")
def latest(sensor_id: str):
    with db() as conn:
        row = conn.execute(
            "SELECT sensor_id, ts, raw, moisture, vcc, rssi FROM readings WHERE sensor_id=? ORDER BY ts DESC LIMIT 1",
            (sensor_id,),
        ).fetchone()
    return dict(row) if row else None
