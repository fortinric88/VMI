"""
EnOcean and MQTT Services for Home Assistant VMI Addon
"""

import logging
import json
import threading
import time
import os
import sys
import queue
from abc import ABC, abstractmethod
from datetime import datetime

try:
    import paho.mqtt.client as mqtt
except ImportError:
    mqtt = None

logger = logging.getLogger("ha_vmi")

# Try to import enocean library, will be installed via requirements.txt
try:
    from enocean.communicators.serialcommunicator import SerialCommunicator
    from enocean.communicators.arubacommunicator import ArubaCommunicator
    from enocean.protocol.packet import RadioPacket
    from enocean.protocol.constants import PACKET, RORG
    ENOCEAN_AVAILABLE = True
except ImportError:
    ENOCEAN_AVAILABLE = False
    logger.warning("EnOcean library not available, install via pip")


class MQTTService:
    """MQTT service for publishing VMI data"""
    
    def __init__(self, config):
        self.config = config
        self.client = None
        self.connected = False
        self.topic_prefix = "home/vmi"
        self.message_queue = queue.Queue()
        self.running = False
        
    def start(self):
        """Start MQTT service"""
        if not mqtt:
            logger.warning("paho-mqtt not available, MQTT disabled")
            return
            
        self.running = True
        self.client = mqtt.Client(client_id="ha_vmi_addon")
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message
        
        try:
            broker = self.config.get("broker", "localhost")
            port = self.config.get("port", 1883)
            user = self.config.get("user", "")
            password = self.config.get("password", "")
            
            if user and password:
                self.client.username_pw_set(user, password)
            
            self.client.connect(broker, port, keepalive=60)
            self.client.loop_start()
            
            logger.info(f"MQTT connection initiated to {broker}:{port}")
            
            # Start message publishing thread
            threading.Thread(target=self._publish_loop, daemon=True).start()
            
        except Exception as e:
            logger.error(f"Failed to connect to MQTT: {e}")
    
    def _on_connect(self, client, userdata, flags, rc):
        """MQTT connection callback"""
        if rc == 0:
            self.connected = True
            logger.info("MQTT connected successfully")
            # Subscribe to command topics
            client.subscribe(f"{self.topic_prefix}/command/#")
        else:
            logger.error(f"MQTT connection failed with code {rc}")
    
    def _on_disconnect(self, client, userdata, rc):
        """MQTT disconnection callback"""
        self.connected = False
        if rc != 0:
            logger.warning(f"MQTT disconnected with code {rc}")
    
    def _on_message(self, client, userdata, msg):
        """MQTT message callback"""
        logger.debug(f"MQTT message received: {msg.topic} = {msg.payload.decode()}")
    
    def _publish_loop(self):
        """Publish queued messages to MQTT"""
        while self.running:
            try:
                topic, payload = self.message_queue.get(timeout=1)
                if self.connected and self.client:
                    self.client.publish(topic, payload)
                    logger.debug(f"Published to {topic}: {payload}")
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error publishing MQTT message: {e}")
    
    def publish(self, topic_suffix, payload):
        """Queue message for publication"""
        full_topic = f"{self.topic_prefix}/{topic_suffix}"
        if isinstance(payload, dict):
            payload = json.dumps(payload)
        self.message_queue.put((full_topic, str(payload)))
    
    def stop(self):
        """Stop MQTT service"""
        self.running = False
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
        logger.info("MQTT service stopped")


class EnOceanService:
    """EnOcean communication service"""
    
    def __init__(self, config, mqtt_service):
        self.config = config
        self.mqtt_service = mqtt_service
        self.communicator = None
        self.running = False
        self.devices = {}  # Known devices
        self.packet_queue = queue.Queue()
        
    def start(self):
        """Start EnOcean service"""
        if not ENOCEAN_AVAILABLE:
            logger.warning("EnOcean library not available")
            return
        
        self.running = True
        
        try:
            device = self.config.get("device", "auto")
            if device == "auto":
                device = self._find_device()
            
            if not device:
                logger.error("No EnOcean device found")
                return
            
            logger.info(f"Using EnOcean device: {device}")
            self.communicator = SerialCommunicator(port=device)
            self.communicator.start()
            
            if self.communicator.base_id:
                base_id_str = ':'.join(f'{b:02X}' for b in self.communicator.base_id)
                logger.info(f"EnOcean Base ID: {base_id_str}")
                self.mqtt_service.publish("enocean/base_id", base_id_str)
            
            # Start listening thread
            threading.Thread(target=self._listen_loop, daemon=True).start()
            logger.info("EnOcean service started")
            
        except Exception as e:
            logger.error(f"Failed to start EnOcean service: {e}")
    
    def _find_device(self):
        """Find EnOcean USB device"""
        try:
            import serial.tools.list_ports
            ports = serial.tools.list_ports.comports()
            for port in ports:
                if '0403' in port.hwid or '6001' in port.hwid or 'EnOcean' in port.description:
                    logger.info(f"Found EnOcean device at {port.device}")
                    return port.device
        except Exception as e:
            logger.debug(f"Error finding device: {e}")
        return None
    
    def _listen_loop(self):
        """Listen for EnOcean packets"""
        while self.running:
            try:
                if self.communicator and self.communicator.is_alive():
                    packet = self.communicator.receive.get(block=True, timeout=1)
                    if packet:
                        self._process_packet(packet)
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error in EnOcean listen loop: {e}")
                time.sleep(1)
    
    def _process_packet(self, packet):
        """Process received EnOcean packet"""
        try:
            if hasattr(packet, 'sender_int'):
                sender_id = packet.sender_int
                sender_hex = f"{sender_id:08X}"
                
                logger.debug(f"EnOcean packet from {sender_hex}: {packet}")
                
                # Store device info
                if sender_hex not in self.devices:
                    self.devices[sender_hex] = {
                        'id': sender_hex,
                        'last_update': datetime.now().isoformat()
                    }
                
                # Publish to MQTT
                self.mqtt_service.publish(
                    f"enocean/devices/{sender_hex}/raw",
                    json.dumps({
                        'id': sender_hex,
                        'timestamp': datetime.now().isoformat(),
                        'data': str(packet.data.hex()) if hasattr(packet, 'data') else ''
                    })
                )
        except Exception as e:
            logger.error(f"Error processing packet: {e}")
    
    def send_packet(self, packet):
        """Send EnOcean packet"""
        try:
            if self.communicator and self.communicator.is_alive():
                self.communicator.send(packet)
                logger.debug(f"EnOcean packet sent: {packet}")
                return True
        except Exception as e:
            logger.error(f"Error sending packet: {e}")
        return False
    
    def stop(self):
        """Stop EnOcean service"""
        self.running = False
        if self.communicator:
            try:
                self.communicator.stop()
            except:
                pass
        logger.info("EnOcean service stopped")


class VMIService:
    """VMI Ventilairsec Service"""
    
    def __init__(self, config, enocean_service, mqtt_service):
        self.config = config
        self.enocean_service = enocean_service
        self.mqtt_service = mqtt_service
        self.running = False
        self.vmi_data = {}
        self.device_id = config.get("device_id", "d1079-01-00")
        self.vmi_name = config.get("name", "Ventilairsec")
        
        # Load VMI command definitions
        self.commands = self._load_commands()
    
    def _load_commands(self):
        """Load VMI command definitions from Jeedom config"""
        commands = {}
        try:
            config_path = Path(__file__).parent / "config" / "d1079-01-00.json"
            if config_path.exists():
                with open(config_path, 'r') as f:
                    data = json.load(f)
                    if self.device_id in data:
                        cmds = data[self.device_id].get("commands", [])
                        for cmd in cmds:
                            commands[cmd['logicalId']] = cmd
            else:
                logger.warning(f"Config file not found: {config_path}")
        except Exception as e:
            logger.error(f"Error loading commands: {e}")
        return commands
    
    def start(self):
        """Start VMI service"""
        self.running = True
        logger.info(f"VMI Service started for {self.vmi_name}")
        
        # Publish initial VMI availability
        self.mqtt_service.publish("vmi/status", "online")
        self.mqtt_service.publish("vmi/name", self.vmi_name)
    
    def update_vmi_data(self, command_id, value):
        """Update VMI data and publish via MQTT"""
        try:
            self.vmi_data[command_id] = {
                'value': value,
                'timestamp': datetime.now().isoformat()
            }
            
            # Find command name
            cmd_name = command_id
            if command_id in self.commands:
                cmd_name = self.commands[command_id].get('name', command_id)
            
            # Publish to MQTT
            self.mqtt_service.publish(
                f"vmi/data/{command_id}",
                json.dumps({
                    'name': cmd_name,
                    'value': value,
                    'timestamp': datetime.now().isoformat()
                })
            )
            
            logger.debug(f"VMI data updated: {command_id} = {value}")
        except Exception as e:
            logger.error(f"Error updating VMI data: {e}")
    
    def stop(self):
        """Stop VMI service"""
        self.running = False
        self.mqtt_service.publish("vmi/status", "offline")
        logger.info("VMI service stopped")
