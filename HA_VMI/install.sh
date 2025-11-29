#!/bin/bash
# Installation script for Home Assistant VMI Addon

echo "Installing HA VMI Addon dependencies..."

# Update package lists
apt-get update

# Install system dependencies
apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    libusb-dev \
    libudev-dev \
    build-essential \
    git

# Install Python requirements
pip3 install --no-cache-dir \
    pyserial \
    paho-mqtt \
    enocean

echo "Installation completed!"
