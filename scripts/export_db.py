#!/usr/bin/env python3
import json, sqlite3
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = Path("/home/pi/plant-backend/plant.db")
EXPORTS = ROOT / "exports"
DAILY = EXPORTS / "daily"
LATEST_DAYS = 7

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

if __name__ == "__main__":
    main()
