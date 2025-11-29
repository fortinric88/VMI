#!/usr/bin/env python3
"""
MQTT Discovery helper for Home Assistant HA VMI Addon
Generates Home Assistant MQTT Discovery messages for VMI entities
"""

import json
import logging

logger = logging.getLogger("ha_vmi_discovery")

# Entity mappings for Home Assistant MQTT Discovery
DISCOVERY_MAPPINGS = {
    # Sensors
    "TEMP0::value": {
        "name": "Température soufflage",
        "type": "sensor",
        "device_class": "temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "value_template": "{{ value }}"
    },
    "TEMP1::value": {
        "name": "Température reprise",
        "type": "sensor",
        "device_class": "temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "value_template": "{{ value }}"
    },
    "TEMP2::value": {
        "name": "Température bypass",
        "type": "sensor",
        "device_class": "temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "value_template": "{{ value }}"
    },
    "IEFIL::value": {
        "name": "État filtre",
        "type": "sensor",
        "unit": "%",
        "icon": "mdi:air-filter",
        "value_template": "{{ value }}"
    },
    "CVITM::raw_value": {
        "name": "Vitesse moteur",
        "type": "sensor",
        "unit": "%",
        "icon": "mdi:fan",
        "value_template": "{{ value }}"
    },
    # Binary Sensors
    "BOOS::raw_value": {
        "name": "Boost actif",
        "type": "binary_sensor",
        "device_class": "running",
        "payload_on": 1,
        "payload_off": 0,
        "value_template": "{{ value }}"
    },
    "VAC::raw_value": {
        "name": "Mode vacances",
        "type": "binary_sensor",
        "device_class": "presence",
        "payload_on": 1,
        "payload_off": 0,
        "value_template": "{{ value }}"
    },
    "SURV::raw_value": {
        "name": "Surventilation",
        "type": "binary_sensor",
        "device_class": "power",
        "payload_on": 1,
        "payload_off": 0,
        "value_template": "{{ value }}"
    },
    # Switches
    "BOOS_SWITCH": {
        "name": "Boost (15 min)",
        "type": "switch",
        "icon": "mdi:rocket",
        "command_topic": "home/vmi/vmi/command/BOOST",
        "state_topic": "home/vmi/vmi/data/BOOS::raw_value",
        "payload_on": "1",
        "payload_off": "0"
    },
    "VAC_SWITCH": {
        "name": "Vacances",
        "type": "switch",
        "icon": "mdi:beach",
        "command_topic": "home/vmi/vmi/command/VAC",
        "state_topic": "home/vmi/vmi/data/VAC::raw_value",
        "payload_on": "1",
        "payload_off": "0"
    },
}


def generate_discovery_message(entity_key: str, vmi_name: str = "Ventilairsec") -> dict:
    """Generate MQTT Discovery message for an entity"""
    
    if entity_key not in DISCOVERY_MAPPINGS:
        logger.warning(f"No discovery mapping for {entity_key}")
        return None
    
    mapping = DISCOVERY_MAPPINGS[entity_key]
    entity_type = mapping.get("type", "sensor")
    entity_name = mapping.get("name", entity_key)
    
    # Build unique ID
    unique_id = f"ha_vmi_{vmi_name.lower()}_{entity_key}".replace("::", "_").replace(" ", "_")
    
    # Build topic
    topic = f"homeassistant/{entity_type}/{vmi_name.lower().replace(' ', '_')}/{entity_key.replace('::', '_')}/config"
    
    # Build payload
    payload = {
        "name": entity_name,
        "unique_id": unique_id,
        "device": {
            "identifiers": [f"ha_vmi_{vmi_name.lower().replace(' ', '_')}"],
            "name": vmi_name,
            "model": "Purevent",
            "manufacturer": "Ventilairsec",
            "sw_version": "1.0.0"
        }
    }
    
    # Add common fields
    if "device_class" in mapping:
        payload["device_class"] = mapping["device_class"]
    if "unit" in mapping:
        payload["unit_of_measurement"] = mapping["unit"]
    if "icon" in mapping:
        payload["icon"] = mapping["icon"]
    
    # Add type-specific fields
    if entity_type == "sensor":
        payload["state_topic"] = f"home/vmi/vmi/data/{entity_key}"
        if "value_template" in mapping:
            payload["value_template"] = mapping["value_template"]
    elif entity_type == "binary_sensor":
        payload["state_topic"] = f"home/vmi/vmi/data/{entity_key}"
        if "payload_on" in mapping:
            payload["payload_on"] = mapping["payload_on"]
        if "payload_off" in mapping:
            payload["payload_off"] = mapping["payload_off"]
    elif entity_type == "switch":
        payload["state_topic"] = mapping.get("state_topic", "")
        payload["command_topic"] = mapping.get("command_topic", "")
        payload["payload_on"] = mapping.get("payload_on", "ON")
        payload["payload_off"] = mapping.get("payload_off", "OFF")
    
    return {
        "topic": topic,
        "payload": payload
    }


def publish_all_discovery_messages(mqtt_client, vmi_name: str = "Ventilairsec"):
    """Publish all discovery messages"""
    logger.info(f"Publishing MQTT Discovery messages for {vmi_name}")
    
    for entity_key in DISCOVERY_MAPPINGS.keys():
        message = generate_discovery_message(entity_key, vmi_name)
        if message:
            try:
                mqtt_client.publish(
                    message["topic"],
                    json.dumps(message["payload"]),
                    retain=True
                )
                logger.debug(f"Published discovery for {entity_key}")
            except Exception as e:
                logger.error(f"Error publishing discovery for {entity_key}: {e}")
