#!/bin/bash

# Home Assistant VMI Addon Dockerfile

ARG BUILD_FROM=ghcr.io/home-assistant/base:latest
FROM $BUILD_FROM

# Install dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    gcc \
    musl-dev \
    linux-headers \
    libudev-zero-dev

# Set working directory
WORKDIR /addon

# Copy addon files
COPY requirements.txt .
COPY run.py .
COPY run.sh .
COPY ha_vmi_service.py .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make run.sh executable
RUN chmod +x run.sh

# Run the addon
CMD ["/addon/run.sh"]
