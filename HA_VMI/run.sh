#!/bin/bash

set -e

# Create necessary directories
mkdir -p /data/logs
mkdir -p /data/config

# Run the addon
cd /addon
exec python3 -u run.py
