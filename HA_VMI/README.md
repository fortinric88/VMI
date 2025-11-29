# HA VMI - Home Assistant Addon pour VMI Ventilairsec & EnOcean

## Description

Cet addon Home Assistant intègre votre VMI Purevent et le module EnOcean pour une gestion complète de votre ventilation.

**Fonctionnalités :**
- Communication EnOcean via GPIO/USB
- Lecture des données VMI Ventilairsec en temps réel
- Publication MQTT pour intégration avec Home Assistant
- Support de la programmation et du contrôle de la VMI
- Historique et alertes

## Installation

### Prérequis

- Home Assistant avec support des addons
- Broker MQTT configuré (ex: Mosquitto addon)
- Module EnOcean USB ou GPIO connecté au serveur

### Étapes d'installation

1. **Ajouter le repository** (si nécessaire)
   - Accédez à Settings → Addons → Addon Store
   - Cliquez sur les trois points → Repositories
   - Ajoutez: `https://github.com/fortinric88/VMI`

2. **Installer l'addon**
   - Cherchez "HA VMI" dans l'Addon Store
   - Cliquez sur "Install"

3. **Configurer l'addon**
   - Allez à Settings → Addons → HA VMI
   - Remplissez les paramètres:
     - **device** : Chemin du périphérique EnOcean (auto = détection automatique)
     - **log_level** : Niveau de log (debug, info, warning, error)
     - **mqtt_broker** : Adresse du broker MQTT (localhost si local)
     - **mqtt_port** : Port MQTT (1883 par défaut)
     - **mqtt_user** : Utilisateur MQTT (optionnel)
     - **mqtt_password** : Mot de passe MQTT (optionnel)
     - **vmi_name** : Nom de votre VMI

4. **Démarrer l'addon**
   - Cliquez sur "Start"
   - Vérifiez les logs pour confirmer le démarrage

## Configuration MQTT

Les données sont publiées sur les topics MQTT suivants:

```
home/vmi/enocean/base_id         # ID de base EnOcean
home/vmi/enocean/devices/{ID}/raw # Paquets bruts EnOcean
home/vmi/vmi/status              # État du service VMI
home/vmi/vmi/name                # Nom de la VMI
home/vmi/vmi/data/{COMMAND_ID}   # Données VMI individuelles
```

## Entités Home Assistant

Les entités suivantes sont créées automatiquement:

### Capteurs
- **Température soufflage** (°C)
- **Température reprise** (°C)
- **Humidité relative** (%)
- **Qualité air** (ppm CO2)
- **Vitesse moteur** (%)
- **Taux filtre** (%)

### Sélecteurs
- **Mode fonctionnement** (Normal, Réduit, Ralenti, Silence, Vacances)
- **Mode Bypass** (Auto, Ouvert, Fermé)

### Interrupteurs
- **Surventilation**
- **Débit fixe**
- **Boost** (15 minutes)
- **Vacances**
- **Chauffage appoint**

### Alarmes
- **État filtre**
- **État sondes**
- **Erreurs VMI**

## Troubleshooting

### L'addon ne démarre pas
- Vérifiez que le broker MQTT est disponible
- Vérifiez les logs: Settings → Addons → HA VMI → Logs

### Pas de communication EnOcean
- Vérifiez que le périphérique est connecté
- Essayez un autre port USB
- Vérifiez les permissions GPIO si connecté en GPIO

### Données MQTT non publiées
- Vérifiez la connexion MQTT dans les logs
- Testez avec un client MQTT (ex: MQTT Explorer)

## Support

Pour les problèmes ou suggestions:
- GitHub Issues: https://github.com/fortinric88/VMI/issues
- Discussions: https://github.com/fortinric88/VMI/discussions

## License

AGPL-3.0 - Voir LICENSE
