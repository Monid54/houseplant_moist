#!/usr/bin/env bash

'''
This script exports the sensor readings from the SQLite database into JSON files and pushes them to a Git repository. It performs the following steps:
1. Navigates to the project directory.
2. Runs the export_db.py script to generate the latest.json and daily/YYYY-MM-DD.json files.
3. Stages the generated JSON files for commit.
4. Commits the changes with a message containing the current date.
5. Pushes the commit to the remote Git repository.
'''

# Exit immediately if a command exits with a non-zero status, if an undefined variable is used, or if any command in a pipeline fails.
set -euo pipefail

# Navigate to the project directory where the export_db.py script is located.
cd /home/pi/houseplant_moist

# Run the export_db.py script to generate the JSON exports.
python3 scripts/export_db.py

# Stage the generated JSON files for commit. This includes the latest.json file and all daily exports in the daily directory.
git add exports/latest.json exports/daily/*.json

# Only commit if there are changes to avoid unnecessary commits when there is no new data.
if git diff --cached --quiet; then
  echo "No changes to commit."
  exit 0
fi

# Commit the changes with a message that includes the current date in UTC. The date is formatted as YYYY-MM-DD.
git commit -m "Daily export $(date -u +%F)"
# Push the commit to the remote Git repository. This will update the repository with the new JSON exports.
git push
