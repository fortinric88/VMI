# Guide complet d'intégration Home Assistant - HA VMI

## 📋 Vue d'ensemble

L'addon **HA VMI** offre une intégration complète de votre **VMI Purevent** et de vos capteurs **EnOcean** dans Home Assistant via MQTT.

## 🚀 Installation rapide

### Étape 1 : Ajouter le Repository (optionnel si l'addon est déjà disponible)

1. Allez dans **Settings → Addons → Addon Store**
2. Cliquez sur **⋮ (Menu)** → **Repositories**
3. Ajoutez : `https://github.com/fortinric88/VMI`
4. Cliquez sur **Create**

### Étape 2 : Installer l'addon

1. Allez dans **Settings → Addons → Addon Store**
2. Cherchez **"HA VMI"**
3. Cliquez sur **Install**

### Étape 3 : Configurer l'addon

1. Allez dans **Settings → Addons → HA VMI**
2. Cliquez sur **Configuration**
3. Remplissez les champs :

```json
{
  "device": "auto",
  "log_level": "info",
  "mqtt_broker": "localhost",
  "mqtt_port": 1883,
  "mqtt_user": "",
  "mqtt_password": "",
  "vmi_name": "Ventilairsec"
}
```

4. Cliquez sur **Save**

### Étape 4 : Démarrer l'addon

1. Cliquez sur **Start**
2. Allez dans **Logs** pour vérifier le démarrage
3. Vous devriez voir: `All services started successfully`

## 🔧 Détails de configuration

### Paramètre : device
Adresse du dongle EnOcean

| Valeur | Usage |
|--------|-------|
| `auto` | Détection automatique (recommandé) |
| `/dev/ttyUSB0` | Dongle USB (port 0) |
| `/dev/ttyUSB1` | Dongle USB (port 1) |
| `/dev/ttyAMA0` | GPIO serie (Raspberry Pi) |

**Comment trouver le bon port :**
```bash
# Terminal Home Assistant
ls /dev/ttyUSB*
ls /dev/ttyAMA*
dmesg | grep tty
```

### Paramètre : mqtt_broker & mqtt_port

Si vous utilisez l'addon **Mosquitto MQTT** en local :
```json
{
  "mqtt_broker": "localhost",
  "mqtt_port": 1883
}
```

Si vous utilisez un broker distant :
```json
{
  "mqtt_broker": "192.168.1.50",
  "mqtt_port": 1883
}
```

### Paramètre : mqtt_user & mqtt_password

Pour un broker sécurisé :
```json
{
  "mqtt_user": "homeassistant",
  "mqtt_password": "votre_mot_de_passe_secure"
}
```

## 📊 Entités créées automatiquement

### Capteurs principaux

| Entité | Topic MQTT | Unité |
|--------|-----------|-------|
| Température soufflage | `home/vmi/vmi/data/TEMP0::value` | °C |
| Température reprise | `home/vmi/vmi/data/TEMP1::value` | °C |
| Vitesse moteur | `home/vmi/vmi/data/CVITM::raw_value` | % |
| État filtre | `home/vmi/vmi/data/IEFIL::value` | % |
| Puissance chauffage | `home/vmi/vmi/data/PCHAUFF::value` | % |
| Ouverture Bypass | `home/vmi/vmi/data/OUVBY1::value` | % |

### Interrupteurs

| Interrupteur | Topic Commande |
|--------------|----------------|
| Boost (15 min) | `home/vmi/vmi/command/BOOST` |
| Mode vacances | `home/vmi/vmi/command/VAC` |
| Surventilation | `home/vmi/vmi/command/SURV` |

### Sélecteurs

| Sélecteur | Topic | Options |
|-----------|-------|---------|
| Mode fonctionnement | `home/vmi/vmi/data/MF::value` | Normal, Réduit, Ralenti, Silence |
| Mode Bypass | `home/vmi/vmi/data/BYP::value` | Auto, Ouvert, Fermé |

## 🏠 Automatisations Home Assistant

### Exemple 1 : Alerte filtre sale

```yaml
automation:
  - alias: Alerte filtre VMI
    trigger:
      platform: numeric_state
      entity_id: sensor.ventilairsec_etat_filtre
      above: 80
    action:
      service: notify.notify
      data:
        message: "⚠️ Le filtre de la VMI est encrassé à {{ states('sensor.ventilairsec_etat_filtre') }}%"
```

### Exemple 2 : Activation Boost manuel

```yaml
automation:
  - alias: Boost VMI simple
    trigger:
      platform: state
      entity_id: input_boolean.vmi_boost
      to: "on"
    action:
      - service: mqtt.publish
        data:
          topic: "home/vmi/vmi/command/BOOST"
          payload: "1"
      - delay: "00:15:00"
      - service: mqtt.publish
        data:
          topic: "home/vmi/vmi/command/BOOST"
          payload: "0"
```

### Exemple 3 : Mode vacances automatique

```yaml
automation:
  - alias: VMI Vacances - Départ
    trigger:
      platform: state
      entity_id: group.presence
      to: "not_home"
      for: "00:30:00"
    action:
      service: mqtt.publish
      data:
        topic: "home/vmi/vmi/command/VAC"
        payload: "1"

  - alias: VMI Vacances - Retour
    trigger:
      platform: state
      entity_id: group.presence
      to: "home"
    action:
      service: mqtt.publish
      data:
        topic: "home/vmi/vmi/command/VAC"
        payload: "0"
```

## 📱 Cartes Lovelace

### Carte de contrôle simple

```yaml
type: entities
title: VMI Ventilairsec
entities:
  - entity: sensor.ventilairsec_temperature_soufflage
    icon: mdi:thermometer
  - entity: sensor.ventilairsec_temperature_reprise
    icon: mdi:thermometer
  - entity: sensor.ventilairsec_vitesse_moteur
  - entity: sensor.ventilairsec_etat_filtre
  - entity: switch.ventilairsec_boost
  - entity: switch.ventilairsec_vacances
  - entity: select.ventilairsec_mode_fonctionnement
```

### Carte personnalisée (si apexcharts installé)

```yaml
type: custom:apexcharts-card
graph_span: 1d
title: Historique VMI
series:
  - entity: sensor.ventilairsec_temperature_soufflage
    name: Température soufflage
    color: "#FF6B6B"
  - entity: sensor.ventilairsec_vitesse_moteur
    name: Vitesse moteur (%)
    color: "#4ECDC4"
```

## 🐛 Troubleshooting

### L'addon ne démarre pas

**Logs à vérifier :**
```
Settings → Addons → HA VMI → Logs
```

**Solutions courantes :**

1. **Broker MQTT indisponible**
   - Vérifiez l'addon Mosquitto est bien started
   - Vérifiez l'adresse et le port

2. **Dongle EnOcean non détecté**
   - Vérifiez que le dongle est bien branché
   - Testez manuellement : `ls /dev/ttyUSB*`
   - Remplacez `device: auto` par le chemin exact

3. **Permissions GPIO**
   - Si utilisation de GPIO : `chmod 666 /dev/ttyAMA0`

### Pas de données en MQTT

**Testez la connexion MQTT :**

```bash
# Terminal Home Assistant
mosquitto_sub -h localhost -p 1883 -t "home/vmi/#" -v
```

Vous devriez voir les messages MQTT arriver.

### Entités non créées dans Home Assistant

Home Assistant crée les entités automatiquement avec MQTT Discovery :

1. Vérifiez que le broker MQTT est configuré dans Home Assistant
2. Redémarrez Home Assistant
3. Vérifiez les logs : `Settings → System → Logs`

## 📡 Topics MQTT

### Publication (données VMI)
```
home/vmi/vmi/status              # online/offline
home/vmi/vmi/name                # Nom de la VMI
home/vmi/vmi/data/{COMMAND_ID}   # Données individuelles
```

### Souscription (commandes)
```
home/vmi/vmi/command/BOOST       # Activation boost
home/vmi/vmi/command/VAC         # Mode vacances
home/vmi/vmi/command/SURV        # Surventilation
home/vmi/vmi/command/MF          # Mode fonctionnement
```

## 📚 Ressources

- [Home Assistant MQTT](https://www.home-assistant.io/integrations/mqtt/)
- [EnOcean Protocol](https://en.wikipedia.org/wiki/EnOcean)
- [VMI Ventilairsec Documentation](https://www.ventilairsec.com)

## 💡 Conseils d'utilisation

1. **Stockage des données** : Activez l'historique Home Assistant pour conserver les données (par défaut 10 jours)
2. **Performance** : Utilisez `log_level: info` en production (debug ralentit l'addon)
3. **Fiabilité** : Redémarrez l'addon tous les mois via une automation
4. **Sécurité** : Utilisez toujours un mot de passe MQTT fort

## 🤝 Support

- **Issues** : https://github.com/fortinric88/VMI/issues
- **Discussions** : https://github.com/fortinric88/VMI/discussions
