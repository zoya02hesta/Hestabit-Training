#!/bin/bash

SERVER="google.com"
LOG_DIR="$(dirname "$0")/../logs"
LOG_FILE="$LOG_DIR/health.log"

mkdir -p "$LOG_DIR"

ping -c 1 $SERVER > /dev/null 2>&1

if [ $? -ne 0 ]; then
  echo "$(date) ❌ Server DOWN" >> "$LOG_FILE"
else
  echo "$(date) ✅ Server UP" >> "$LOG_FILE"
fi
