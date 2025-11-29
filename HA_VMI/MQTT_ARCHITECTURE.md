# Architecture MQTT - HA VMI

## 📐 Schéma d'architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Home Assistant                         │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐   │
│  │   MQTT      │  │  Automations │  │   Lovelace │   │
│  │ Integration │  │   & Scripts  │  │     UI     │   │
│  └──────┬──────┘  └──────┬───────┘  └──────┬─────┘   │
│         │                │                 │           │
│         └────────────────┼─────────────────┘           │
│                          │                             │
│                   TCP 1883 (MQTT)                      │
│                          │                             │
└──────────────────────────┼─────────────────────────────┘
                           │
                   ┌───────▼────────┐
                   │ Mosquitto MQTT │
                   │ (localhost:1883)
                   └───────┬────────┘
                           │
       ┌───────────────────┼──────────────────┐
       │                   │                  │
┌──────▼──────┐    ┌───────▼────────┐  ┌────▼────────┐
│  HA VMI     │    │ Other Addons / │  │   External  │
│  Addon      │    │   Services     │  │    MQTT     │
│             │    │                │  │  Clients    │
└──────┬──────┘    └────────────────┘  └─────────────┘
       │
       │  Serial/GPIO (USB or UART)
       │
┌──────▼──────────────────┐
│   EnOcean Dongle/GPIO   │
│   (d1079-01-00)         │
│   VMI Purevent          │
└─────────────────────────┘
```

## 📡 Structure des Topics MQTT

### Hiérarchie générale
```
home/vmi/
├── enocean/              # Données EnOcean
│   ├── base_id          # ID de base du contrôleur
│   └── devices/         # Appareils EnOcean individuels
│       └── {DEVICE_ID}/
│           └── raw      # Données brutes
│
└── vmi/                  # Données VMI Ventilairsec
    ├── status           # État du service (online/offline)
    ├── name             # Nom de la VMI
    ├── data/            # Données temps réel
    │   ├── TEMP0::value
    │   ├── TEMP1::value
    │   ├── CVITM::raw_value
    │   ├── IEFIL::value
    │   └── ...
    └── command/         # Commandes entrantes
        ├── BOOST
        ├── VAC
        ├── SURV
        └── ...
```

## 📊 Topics détaillés

### 1. Status et Information

#### `home/vmi/vmi/status`
- **Type** : String
- **Valeurs** : `online`, `offline`
- **Fréquence** : À la connexion/déconnexion
- **Exemple** : `online`

#### `home/vmi/vmi/name`
- **Type** : String
- **Valeurs** : Nom configuré
- **Fréquence** : À la démarrage
- **Exemple** : `Ventilairsec`

### 2. Capteurs de Température

#### `home/vmi/vmi/data/TEMP0::value`
- **Nom** : Température soufflage
- **Type** : Float
- **Unité** : °C
- **Plage** : -10 à +60
- **Fréquence** : Toutes les 30 secondes
- **Exemple** : `21.5`

#### `home/vmi/vmi/data/TEMP1::value`
- **Nom** : Température reprise
- **Type** : Float
- **Unité** : °C
- **Plage** : -10 à +60
- **Exemple** : `20.2`

#### `home/vmi/vmi/data/TEMP2::value`
- **Nom** : Température bypass (si disponible)
- **Type** : Float
- **Unité** : °C
- **Exemple** : `18.8`

### 3. Capteurs d'État

#### `home/vmi/vmi/data/CVITM::raw_value`
- **Nom** : Vitesse moteur
- **Type** : Integer
- **Unité** : % (0-255, converti en %)
- **Exemple** : `150` → ~59%

#### `home/vmi/vmi/data/IEFIL::value`
- **Nom** : État du filtre
- **Type** : Integer
- **Unité** : % (0-100)
- **Exemple** : `45`

#### `home/vmi/vmi/data/PCHAUFF::value`
- **Nom** : Puissance chauffage
- **Type** : Integer
- **Unité** : % (0-100)
- **Exemple** : `75`

#### `home/vmi/vmi/data/OUVBY1::value`
- **Nom** : Ouverture Bypass
- **Type** : Integer
- **Unité** : % (0-100)
- **Exemple** : `100`

### 4. Modes et États binaires

#### `home/vmi/vmi/data/MF::value`
- **Nom** : Mode fonctionnement
- **Type** : String
- **Valeurs** : `Off`, `Normal`, `Réduit`, `Ralenti`, `Silence`
- **Exemple** : `Normal`

#### `home/vmi/vmi/data/BYP::value`
- **Nom** : Mode Bypass
- **Type** : String
- **Valeurs** : `Auto`, `Ouvert`, `Fermé`
- **Exemple** : `Auto`

#### `home/vmi/vmi/data/BOOS::raw_value`
- **Nom** : Boost actif
- **Type** : Integer (0 ou 1)
- **Valeurs** : `0` (off), `1` (on)
- **Exemple** : `0`

#### `home/vmi/vmi/data/VAC::raw_value`
- **Nom** : Mode vacances
- **Type** : Integer (0 ou 1)
- **Exemple** : `0`

#### `home/vmi/vmi/data/SURV::raw_value`
- **Nom** : Surventilation
- **Type** : Integer (0 ou 1)
- **Exemple** : `0`

### 5. Erreurs et Diagnostique

#### `home/vmi/vmi/data/CERR1::value`
- **Nom** : Code erreur 1
- **Type** : Integer (0-255)
- **Exemple** : `255` (pas d'erreur)
- **Note** : Voir la table des codes d'erreur ci-dessous

#### `home/vmi/vmi/data/CERR2::value`
- **Nom** : Code erreur 2
- **Type** : Integer (0-255)
- **Exemple** : `255`

## 🎛️ Topics de Commande

Les commandes se publient sur `home/vmi/vmi/command/{COMMAND_ID}` avec les valeurs suivantes :

### Boost

**Topic** : `home/vmi/vmi/command/BOOST`
- **Payload** : `1` (activation) ou `0` (désactivation)
- **Durée** : 15 minutes
- **Exemple** : Publier `1` pour activer

```bash
mosquitto_pub -h localhost -p 1883 -t "home/vmi/vmi/command/BOOST" -m "1"
```

### Mode Vacances

**Topic** : `home/vmi/vmi/command/VAC`
- **Payload** : `1` (vacances on) ou `0` (vacances off)
- **Exemple** : Publier `1` pour mode vacances

### Surventilation

**Topic** : `home/vmi/vmi/command/SURV`
- **Payload** : `1` (on) ou `0` (off)

### Mode Fonctionnement

**Topic** : `home/vmi/vmi/command/MF`
- **Payload** : `0` (Off), `1` (Normal), `2` (Réduit), `3` (Ralenti)
- **Exemple** : Publier `1` pour mode Normal

## 🔴 Codes d'Erreur VMI

| Code | Hex | Signification |
|------|-----|---------------|
| 1 | 01 | Panne résistance |
| 2 | 02 | Trop froid pour chauffage |
| 16 | 10 | Panne moteur |
| 32 | 20 | Filtre à changer |
| 48 | 30 | Panne d'un capteur QAI |
| 49-57 | 31-39 | Panne capteur QAI n°1-9 |
| 58 | 3A | Problème sur plusieurs capteurs |
| 59 | 3B | Problème d'appairage capteur |
| 64 | 40 | Problème inconnu sur l'assistant |
| 255 | FF | Pas d'erreur |

## 📝 Exemples de requêtes

### Test de connexion MQTT

```bash
# S'abonner à tous les messages VMI
mosquitto_sub -h localhost -p 1883 -t "home/vmi/vmi/#" -v

# S'abonner à toutes les données
mosquitto_sub -h localhost -p 1883 -t "home/vmi/vmi/data/#" -v
```

### Activer le Boost

```bash
mosquitto_pub -h localhost -p 1883 \
  -t "home/vmi/vmi/command/BOOST" \
  -m "1"
```

### Basculer en mode vacances

```bash
mosquitto_pub -h localhost -p 1883 \
  -t "home/vmi/vmi/command/VAC" \
  -m "1"
```

### Changer le mode fonctionnement

```bash
mosquitto_pub -h localhost -p 1883 \
  -t "home/vmi/vmi/command/MF" \
  -m "1"  # 1 = Normal
```

## 📊 Payload JSON

Les données complexes sont envoyées en JSON :

```json
{
  "name": "Température soufflage",
  "value": 21.5,
  "timestamp": "2025-01-15T10:30:45.123456",
  "unit": "°C"
}
```

## 🔐 Sécurité MQTT

Pour sécuriser votre connexion MQTT :

1. **Authentification** : Utilisez `mqtt_user` et `mqtt_password`
2. **TLS** : Utilisez `mqtt_port: 8883` avec certificats
3. **Topic Access Control** : Restreignez les topics par utilisateur

### Configuration sécurisée exemple

```json
{
  "mqtt_broker": "mqtt.example.com",
  "mqtt_port": 8883,
  "mqtt_user": "homeassistant",
  "mqtt_password": "securite_maximale_42_caracteres"
}
```
