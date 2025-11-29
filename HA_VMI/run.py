#!/usr/bin/env python3
"""
Home Assistant Addon - VMI Ventilairsec & EnOcean Integration
"""

import logging
import json
import os
import sys
import time
import signal
import threading
from pathlib import Path

# Configuration
CONFIG_PATH = "/data/options.json"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

logger = logging.getLogger("ha_vmi")

def load_config():
    """Load addon configuration"""
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        return {}

def setup_logging(log_level):
    """Setup logging configuration"""
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    logging.basicConfig(
        format=LOG_FORMAT,
        level=numeric_level
    )

def main():
    """Main entry point"""
    config = load_config()
    log_level = config.get("log_level", "info")
    setup_logging(log_level)
    
    logger.info("Starting HA VMI Addon")
    logger.info(f"Configuration: {config}")
    
    # Import and start services
    try:
        from ha_vmi_service import EnOceanService, VMIService, MQTTService
        
        # Initialize MQTT service
        mqtt_config = {
            "broker": config.get("mqtt_broker", "localhost"),
            "port": config.get("mqtt_port", 1883),
            "user": config.get("mqtt_user", ""),
            "password": config.get("mqtt_password", "")
        }
        mqtt_service = MQTTService(mqtt_config)
        
        # Initialize EnOcean service
        enocean_config = {
            "device": config.get("device", "auto"),
            "log_level": log_level
        }
        enocean_service = EnOceanService(enocean_config, mqtt_service)
        
        # Initialize VMI service
        vmi_config = {
            "name": config.get("vmi_name", "Ventilairsec"),
            "device_id": "d1079-01-00"
        }
        vmi_service = VMIService(vmi_config, enocean_service, mqtt_service)
        
        # Start services
        mqtt_service.start()
        enocean_service.start()
        vmi_service.start()
        
        logger.info("All services started successfully")
        
        # Keep running
        signal.signal(signal.SIGTERM, lambda s, f: shutdown(mqtt_service, enocean_service, vmi_service))
        signal.signal(signal.SIGINT, lambda s, f: shutdown(mqtt_service, enocean_service, vmi_service))
        
        while True:
            time.sleep(1)
            
    except Exception as e:
        logger.error(f"Failed to start services: {e}", exc_info=True)
        sys.exit(1)

def shutdown(mqtt_service, enocean_service, vmi_service):
    """Shutdown services gracefully"""
    logger.info("Shutting down services...")
    try:
        vmi_service.stop()
        enocean_service.stop()
        mqtt_service.stop()
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")
    sys.exit(0)

if __name__ == "__main__":
    main()
