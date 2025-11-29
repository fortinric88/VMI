# Configuration d'exemple pour HA VMI

```json
{
  "device": "auto",
  "log_level": "info",
  "mqtt_broker": "192.168.1.100",
  "mqtt_port": 1883,
  "mqtt_user": "homeassistant",
  "mqtt_password": "your_secure_password",
  "vmi_name": "Ventilairsec Salon"
}
```

## Paramètres disponibles

### device
- **Type** : string
- **Défaut** : "auto"
- **Description** : Chemin du périphérique EnOcean
  - `auto` : Détection automatique du premier dongle USB trouvé
  - `/dev/ttyUSB0` : Périphérique série spécifique
  - `/dev/ttyAMA0` : GPIO serial (Raspberry Pi)

### log_level
- **Type** : string (enum)
- **Valeurs** : debug, info, warning, error
- **Défaut** : info
- **Description** : Niveau de détail des logs

### mqtt_broker
- **Type** : string
- **Défaut** : localhost
- **Description** : Adresse IP ou hostname du broker MQTT
- **Exemple** : 192.168.1.100, mqtt.local, localhost

### mqtt_port
- **Type** : port
- **Défaut** : 1883
- **Description** : Port du broker MQTT
- **Note** : Utilisez 8883 pour MQTT sécurisé (TLS)

### mqtt_user
- **Type** : string (optionnel)
- **Description** : Utilisateur MQTT pour l'authentification

### mqtt_password
- **Type** : password (optionnel)
- **Description** : Mot de passe MQTT

### vmi_name
- **Type** : string
- **Défaut** : Ventilairsec
- **Description** : Nom de votre VMI pour les entités Home Assistant

## Configuration MQTT

### Broker MQTT local (Mosquitto addon)
```json
{
  "mqtt_broker": "localhost",
  "mqtt_port": 1883,
  "mqtt_user": "",
  "mqtt_password": ""
}
```

### Broker MQTT distant
```json
{
  "mqtt_broker": "mqtt.monserveur.com",
  "mqtt_port": 8883,
  "mqtt_user": "homeassistant",
  "mqtt_password": "motdepasse_securise"
}
```

## Dépannage

### Détection automatique ne trouve pas le dongle
1. Branchez le dongle EnOcean
2. Exécutez: `ls /dev/ttyUSB*`
3. Remplacez `device` par le chemin affiché

### Erreur de connexion MQTT
- Vérifiez que le broker MQTT est en cours d'exécution
- Testez la connexion: `mosquitto_pub -h localhost -p 1883 -t test -m "hello"`
- Vérifiez le nom d'utilisateur et le mot de passe

### Permissions GPIO
Si vous utilisez GPIO (`/dev/ttyAMA0`), l'addon a besoin des permissions :
```bash
chmod 666 /dev/ttyAMA0
```
