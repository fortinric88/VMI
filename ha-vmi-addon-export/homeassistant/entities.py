"""
Home Assistant Entities for VMI Ventilairsec
"""

import logging
from dataclasses import dataclass, field
from typing import Optional, Any

LOGGER = logging.getLogger(__name__)


@dataclass
class VMIEntityConfig:
    """Configuration for a VMI entity"""
    key: str
    name: str
    entity_type: str  # sensor, binary_sensor, select, switch, number
    unit: Optional[str] = None
    icon: Optional[str] = None
    device_class: Optional[str] = None
    options: Optional[list] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    step: Optional[float] = None
    unique_id_suffix: str = ""


# Sensors - Temperature, Humidity, CO2, etc.
VMI_SENSORS = [
    VMIEntityConfig(
        key="TEMP0::value",
        name="Température soufflage",
        entity_type="sensor",
        unit="°C",
        icon="mdi:thermometer",
        device_class="temperature"
    ),
    VMIEntityConfig(
        key="TEMP1::value",
        name="Température reprise",
        entity_type="sensor",
        unit="°C",
        icon="mdi:thermometer",
        device_class="temperature"
    ),
    VMIEntityConfig(
        key="TEMP2::value",
        name="Température bypass",
        entity_type="sensor",
        unit="°C",
        icon="mdi:thermometer",
        device_class="temperature"
    ),
    VMIEntityConfig(
        key="TEMPCELEC::value",
        name="Température consigne électrique",
        entity_type="sensor",
        unit="°C",
        icon="mdi:thermometer",
        device_class="temperature"
    ),
    VMIEntityConfig(
        key="TEMPMSOUFFL::value",
        name="Température min soufflage",
        entity_type="sensor",
        unit="°C",
        icon="mdi:thermometer",
        device_class="temperature"
    ),
    VMIEntityConfig(
        key="TEMPCHYDROR::value",
        name="Température consigne Hydro'R",
        entity_type="sensor",
        unit="°C",
        icon="mdi:thermometer",
        device_class="temperature"
    ),
    VMIEntityConfig(
        key="TEMPCSOLAR::value",
        name="Température consigne Solar'R",
        entity_type="sensor",
        unit="°C",
        icon="mdi:thermometer",
        device_class="temperature"
    ),
    VMIEntityConfig(
        key="HUMINTERNE::value",
        name="Humidité interne",
        entity_type="sensor",
        unit="%",
        icon="mdi:water-percent",
        device_class="humidity"
    ),
    VMIEntityConfig(
        key="CVITM::raw_value",
        name="Vitesse moteur",
        entity_type="sensor",
        unit="%",
        icon="mdi:fan"
    ),
    VMIEntityConfig(
        key="IEFIL::value",
        name="État filtre",
        entity_type="sensor",
        unit="%",
        icon="mdi:air-filter"
    ),
    VMIEntityConfig(
        key="PCHAUFF::value",
        name="Puissance chauffage",
        entity_type="sensor",
        unit="%",
        icon="mdi:radiator"
    ),
    VMIEntityConfig(
        key="OUVHYDR::value",
        name="Ouverture Hydro'R",
        entity_type="sensor",
        unit="%",
        icon="mdi:valve"
    ),
    VMIEntityConfig(
        key="OUVBY1::value",
        name="Ouverture Bypass",
        entity_type="sensor",
        unit="%",
        icon="mdi:valve"
    ),
]

# Binary Sensors - On/Off states
VMI_BINARY_SENSORS = [
    VMIEntityConfig(
        key="DEBF::raw_value",
        name="Débit fixe",
        entity_type="binary_sensor",
        device_class="running",
        icon="mdi:speedometer"
    ),
    VMIEntityConfig(
        key="SURV::raw_value",
        name="Surventilation",
        entity_type="binary_sensor",
        device_class="power",
        icon="mdi:fan-speed-3"
    ),
    VMIEntityConfig(
        key="VAC::raw_value",
        name="Mode vacances",
        entity_type="binary_sensor",
        device_class="presence",
        icon="mdi:beach"
    ),
    VMIEntityConfig(
        key="BOOS::raw_value",
        name="Boost actif",
        entity_type="binary_sensor",
        device_class="power",
        icon="mdi:rocket"
    ),
    VMIEntityConfig(
        key="HYDROR::raw_value",
        name="Hydro'R actif",
        entity_type="binary_sensor",
        device_class="power",
        icon="mdi:water-boiler"
    ),
    VMIEntityConfig(
        key="SOLARR::raw_value",
        name="Solar'R actif",
        entity_type="binary_sensor",
        device_class="power",
        icon="mdi:white-balance-sunny"
    ),
]

# Select - Mode selection
VMI_SELECTS = [
    VMIEntityConfig(
        key="MF::raw_value",
        name="Mode fonctionnement",
        entity_type="select",
        icon="mdi:fan",
        options=["Off", "Normal", "Réduit", "Ralenti", "Silence"]
    ),
    VMIEntityConfig(
        key="BYP::raw_value",
        name="Mode Bypass",
        entity_type="select",
        icon="mdi:pipe",
        options=["Auto", "Ouvert", "Fermé"]
    ),
]

# Switches - Controllable on/off
VMI_SWITCHES = [
    VMIEntityConfig(
        key="BOOS",
        name="Boost (15 min)",
        entity_type="switch",
        icon="mdi:rocket"
    ),
    VMIEntityConfig(
        key="VAC",
        name="Vacances",
        entity_type="switch",
        icon="mdi:beach"
    ),
    VMIEntityConfig(
        key="SURV",
        name="Surventilation",
        entity_type="switch",
        icon="mdi:fan-speed-3"
    ),
]

# Status & Error sensors
VMI_STATUS_SENSORS = [
    VMIEntityConfig(
        key="IDMACH::value",
        name="Identifiant machine",
        entity_type="sensor",
        icon="mdi:identifier"
    ),
    VMIEntityConfig(
        key="VELEC::value",
        name="Version électronique",
        entity_type="sensor",
        icon="mdi:microchip"
    ),
    VMIEntityConfig(
        key="VLOG::value",
        name="Version logiciel",
        entity_type="sensor",
        icon="mdi:microchip"
    ),
    VMIEntityConfig(
        key="CERR1::value",
        name="Code erreur 1",
        entity_type="sensor",
        icon="mdi:alert"
    ),
    VMIEntityConfig(
        key="CERR2::value",
        name="Code erreur 2",
        entity_type="sensor",
        icon="mdi:alert"
    ),
    VMIEntityConfig(
        key="TYPCAI::value",
        name="Type caisson",
        entity_type="sensor",
        icon="mdi:information"
    ),
]


def get_all_vmi_entities():
    """Get all VMI entity configurations"""
    return {
        'sensors': VMI_SENSORS,
        'binary_sensors': VMI_BINARY_SENSORS,
        'selects': VMI_SELECTS,
        'switches': VMI_SWITCHES,
        'status': VMI_STATUS_SENSORS
    }


def get_entity_by_key(key: str) -> Optional[VMIEntityConfig]:
    """Find entity configuration by key"""
    all_entities = get_all_vmi_entities()
    
    for entity_type, entities in all_entities.items():
        for entity in entities:
            if entity.key == key:
                return entity
    
    return None


# Error descriptions (from Jeedom plugin)
ERROR_CODES = {
    '01': 'Panne résistance',
    '02': 'Trop froid pour chauffage',
    '10': 'Panne moteur',
    '20': 'Filtre à changer',
    '30': 'Panne d\'un capteur QAI',
    '31': 'Panne capteur QAI n°1',
    '32': 'Panne capteur QAI n°2',
    '33': 'Panne capteur QAI n°3',
    '34': 'Panne capteur QAI n°4',
    '35': 'Panne capteur QAI n°5',
    '36': 'Panne capteur QAI n°6',
    '37': 'Panne capteur QAI n°7',
    '38': 'Panne capteur QAI n°8',
    '39': 'Panne capteur QAI n°9',
    '3A': 'Problème sur plusieurs capteurs QAI',
    '3B': 'Problème d\'appairage d\'un capteur QAI',
    '40': 'Problème inconnu sur l\'assistant',
    '41': 'Erreur de température de l\'assistant',
    '42': 'Perte de communication de l\'assistant',
    '43': 'Piles faibles de l\'assistant',
    '44': 'Plusieurs pannes sur l\'assistant',
    '51': 'Panne sur la sonde en sortie des résistances',
    '52': 'Panne sur la sonde en entrée de VMI',
    '53': 'Panne sur la sonde en sortie de HydroR',
    '55': 'Panne sur la sonde en sortie du Bypass',
    '56': 'Panne sur la sonde côté air extérieur du Bypass',
    '57': 'Panne sur la sonde côté comble du Bypass',
    '5F': 'Plusieurs pannes sondes',
    '61': 'Erreur sur le Bypass',
    '65': 'Erreur téléchargement logiciel',
    '70': 'Multiples erreurs',
    '81': 'Problème de communication ByPass',
    '82': 'Problème de communication ByPass',
    '83': 'Volet du ByPass bloqué'
}
