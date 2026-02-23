#!/usr/bin/env python3
import json, sqlite3
from pathlib import Path
from datetime import datetime, timezone, timedelta

"""
This script exports the sensor readings from the SQLite database into JSON files.
It creates two types of exports:
1. latest.json: Contains the latest readings from the last 14 days, aggregated into hourly buckets for recent data and 6-hourly buckets for older data.
2. daily/YYYY-MM-DD.json: Contains all readings for the current day.
The exports are saved in the "exports" directory, with daily exports in a "daily" subdirectory.
"""

# Define paths and constants
ROOT = Path(__file__).resolve().parents[1]
DB_PATH = Path("/home/pi/plant-backend/plant.db")
EXPORTS = ROOT / "exports"
DAILY = EXPORTS / "daily"
LATEST_DAYS = 14

# The main function performs the export process.
def main():
    if not DB_PATH.exists():
        raise SystemExit(f"DB not found: {DB_PATH}")

    EXPORTS.mkdir(parents=True, exist_ok=True)
    DAILY.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    now = datetime.now(timezone.utc)
    cutoff = (now - timedelta(days=LATEST_DAYS)).isoformat()

    latest = conn.execute(
        "SELECT sensor_id, ts, raw, moisture, vcc, rssi FROM readings "
        "WHERE ts >= ? ORDER BY ts ASC",
        (cutoff,),
    ).fetchall()

    # Aggregate data: hourly for last 14 days, 6-hourly for older data
    aggregated = {}
    for row in latest:
        row_dict = dict(row)
        ts = datetime.fromisoformat(row_dict['ts'])
        
        if ts >= (now - timedelta(days=LATEST_DAYS)):
            # Hourly buckets for recent data
            bucket = ts.replace(minute=0, second=0, microsecond=0).isoformat()
        else:
            # 6-hourly buckets for older data
            hour_bucket = (ts.hour // 6) * 6
            bucket = ts.replace(hour=hour_bucket, minute=0, second=0, microsecond=0).isoformat()
        
        key = (row_dict['sensor_id'], bucket)
        if key not in aggregated:
            aggregated[key] = []
        aggregated[key].append(row_dict)
    
    # Average values per bucket
    latest = []
    for (sensor_id, bucket), rows in aggregated.items():
        avg = {
            'sensor_id': sensor_id,
            'ts': bucket,
            'raw': sum(r['raw'] for r in rows) / len(rows),
            'moisture': sum(r['moisture'] for r in rows) / len(rows),
            'vcc': sum(r['vcc'] for r in rows) / len(rows),
            'rssi': sum(r['rssi'] for r in rows) / len(rows),
        }
        latest.append(avg)

    (EXPORTS / "latest.json").write_text(json.dumps({
        "meta": {"generated_at": now.isoformat(), "latest_days": LATEST_DAYS, "count": len(latest)},
        "readings": [dict(r) for r in latest],
    }, ensure_ascii=False, indent=2))

    day = now.strftime("%Y-%m-%d")
    day_start = f"{day}T00:00:00+00:00"
    day_end   = f"{day}T23:59:59.999999+00:00"

    daily = conn.execute(
        "SELECT sensor_id, ts, raw, moisture, vcc, rssi FROM readings "
        "WHERE ts >= ? AND ts <= ? ORDER BY ts ASC",
        (day_start, day_end),
    ).fetchall()

    (DAILY / f"{day}.json").write_text(json.dumps({
        "meta": {"generated_at": now.isoformat(), "day": day, "count": len(daily)},
        "readings": [dict(r) for r in daily],
    }, ensure_ascii=False, indent=2))

    print(f"Exported latest={len(latest)} daily={len(daily)}")
# The init_db function initializes the database by creating the readings table if it doesn't exist and adding an index for efficient querying.
if __name__ == "__main__":
    main()
