#!/bin/bash
# Home Assistant VMI Addon - Run script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Log level setup
LOG_LEVEL=$(jq -r '.log_level // "info"' /data/options.json)
DEVICE=$(jq -r '.device // "auto"' /data/options.json)

echo -e "${GREEN}Starting HA VMI Addon${NC}"
echo "Log Level: $LOG_LEVEL"
echo "Device: $DEVICE"

# Create necessary directories
mkdir -p /data/logs
mkdir -p /data/config

# Run Python addon
cd /addon
exec python3 -u run.py
