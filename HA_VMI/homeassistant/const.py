"""
Home Assistant Integration for HA VMI Addon
"""

import logging
from typing import Final

DOMAIN: Final = "ha_vmi"
VERSION: Final = "1.0.0"
ISSUE_URL: Final = "https://github.com/fortinric88/VMI/issues"

LOGGER = logging.getLogger(__name__)

CONF_DEVICE: Final = "device"
CONF_LOG_LEVEL: Final = "log_level"
CONF_MQTT_BROKER: Final = "mqtt_broker"
CONF_MQTT_PORT: Final = "mqtt_port"
CONF_MQTT_USER: Final = "mqtt_user"
CONF_MQTT_PASSWORD: Final = "mqtt_password"
CONF_VMI_NAME: Final = "vmi_name"

# Entity IDs and attributes
VMI_ENTITY_PREFIX: Final = "vmi"
ENOCEAN_ENTITY_PREFIX: Final = "enocean"

# MQTT Topics
MQTT_TOPIC_PREFIX: Final = "home/vmi"
MQTT_TOPIC_VMI: Final = "vmi"
MQTT_TOPIC_ENOCEAN: Final = "enocean"
