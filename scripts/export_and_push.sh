#!/usr/bin/env bash
set -euo pipefail

cd /home/pi/houseplant_moist

python3 scripts/export_db.py

git add exports/latest.json exports/daily/*.json

# Nur committen, wenn sich was geändert hat
if git diff --cached --quiet; then
  echo "No changes to commit."
  exit 0
fi

git commit -m "Daily export $(date -u +%F)"
git push
