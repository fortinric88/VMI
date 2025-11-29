# 📚 Documentation Index - HA VMI

Bienvenue dans la documentation complète de l'addon **HA VMI** pour Home Assistant !

---

## 🎯 Commencer ici

### 1️⃣ Je suis nouveau
→ **[README.md](README.md)**
- ✅ Vue d'ensemble de l'addon
- ✅ Installation en 3 étapes
- ✅ Dépannage rapide

### 2️⃣ Je veux installer rapidement
→ **[QUICKSTART.sh](QUICKSTART.sh)**
- ✅ Checklist complète d'installation
- ✅ Vérification pas à pas

### 3️⃣ Je viens de Jeedom
→ **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)**
- ✅ Comparaison Jeedom ↔ Home Assistant
- ✅ Ce qui change, ce qui reste
- ✅ Avantages de la migration

---

## 🔧 Configuration

### Configuration détaillée
→ **[CONFIGURATION.md](CONFIGURATION.md)**
- ✅ Tous les paramètres disponibles
- ✅ Exemples pour chaque scénario
- ✅ Troubleshooting des problèmes config

### Paramètres rapides
| Paramètre | Type | Défaut | Doc |
|-----------|------|--------|-----|
| `device` | string | auto | CONFIGURATION.md |
| `log_level` | enum | info | CONFIGURATION.md |
| `mqtt_broker` | string | localhost | CONFIGURATION.md |
| `mqtt_port` | port | 1883 | CONFIGURATION.md |
| `mqtt_user` | string | (none) | CONFIGURATION.md |
| `mqtt_password` | password | (none) | CONFIGURATION.md |
| `vmi_name` | string | Ventilairsec | CONFIGURATION.md |

---

## 🏠 Intégration Home Assistant

### Guide complet
→ **[HOMEASSISTANT_INTEGRATION.md](HOMEASSISTANT_INTEGRATION.md)**
- ✅ Installation détaillée
- ✅ Entités créées automatiquement
- ✅ 20+ exemples d'automatisations
- ✅ Cartes Lovelace
- ✅ Troubleshooting avancé

### Points clés

#### 📊 Entités créées
- 50+ capteurs (température, humidité, etc)
- 10+ interrupteurs (boost, vacances, etc)
- 5+ sélecteurs (mode, bypass, etc)

#### 🎛️ Commandes possibles
```bash
# Activer Boost 15 minutes
mosquitto_pub -t "home/vmi/vmi/command/BOOST" -m "1"

# Mode vacances
mosquitto_pub -t "home/vmi/vmi/command/VAC" -m "1"

# Mode Normal
mosquitto_pub -t "home/vmi/vmi/command/MF" -m "1"
```

#### 🔄 Automatisations
- Alerte filtre sale
- Activation boost manuel
- Mode vacances automatique
- Historique et statistiques

---

## 📡 Architecture MQTT

### Structure complète des topics
→ **[MQTT_ARCHITECTURE.md](MQTT_ARCHITECTURE.md)**
- ✅ Schéma d'architecture complète
- ✅ Tous les topics détaillés
- ✅ Payload JSON
- ✅ Codes d'erreur
- ✅ Sécurité MQTT

### Topics principaux

**Publication (données)**
```
home/vmi/vmi/status              # online/offline
home/vmi/vmi/data/TEMP0::value   # Température
home/vmi/vmi/data/CVITM::raw_value  # Vitesse moteur
home/vmi/vmi/data/IEFIL::value   # État filtre
... 50+ topics de données
```

**Souscription (commandes)**
```
home/vmi/vmi/command/BOOST       # Activation boost
home/vmi/vmi/command/VAC         # Vacances
home/vmi/vmi/command/SURV        # Surventilation
home/vmi/vmi/command/MF          # Mode fonctionnement
```

---

## 🧑‍💻 Développement

### Pour les développeurs
→ **[CONTRIBUTING.md](CONTRIBUTING.md)**
- ✅ Comment contribuer
- ✅ Signaler des bugs
- ✅ Soumettre des améliorations
- ✅ Guidelines de code
- ✅ Pull request process

### Code Source
| Fichier | Purpose | Lignes |
|---------|---------|--------|
| `run.py` | Point d'entrée | 100 |
| `ha_vmi_service.py` | Services (EnOcean, MQTT, VMI) | 400 |
| `mqtt_discovery.py` | MQTT Discovery auto | 150 |
| `homeassistant/entities.py` | Défini les entités | 250 |
| `homeassistant/const.py` | Constantes | 30 |

---

## 🚀 Guides spécifiques

### Par niveau d'expérience

**Débutant** 👶
1. README.md
2. CONFIGURATION.md (section simple)
3. HOMEASSISTANT_INTEGRATION.md (exemples basiques)

**Intermédiaire** 👨‍💻
1. HOMEASSISTANT_INTEGRATION.md (complet)
2. MQTT_ARCHITECTURE.md
3. Créer automatisations personnalisées

**Avancé** 🚀
1. MQTT_ARCHITECTURE.md
2. CONTRIBUTING.md
3. Modifier le code source
4. Créer des extensions

### Par cas d'usage

**J'ai juste besoin que ça marche**
→ README.md + QUICKSTART.sh

**Je veux personnaliser**
→ CONFIGURATION.md + HOMEASSISTANT_INTEGRATION.md

**Je veux comprendre la technique**
→ MQTT_ARCHITECTURE.md

**Je veux développer**
→ CONTRIBUTING.md

**Je viens de Jeedom**
→ MIGRATION_GUIDE.md

---

## 🔍 Recherche rapide

### Par mot-clé

**Installation**
- README.md - Installation en 3 étapes
- QUICKSTART.sh - Checklist détaillée
- HOMEASSISTANT_INTEGRATION.md - Installation complète

**Configuration**
- CONFIGURATION.md - Tous les paramètres
- README.md - Configuration par défaut

**MQTT**
- MQTT_ARCHITECTURE.md - Structure complète
- HOMEASSISTANT_INTEGRATION.md - Topics utiles

**Troubleshooting**
- README.md - Problèmes courants
- CONFIGURATION.md - Problèmes config
- HOMEASSISTANT_INTEGRATION.md - Problèmes HA

**Automatisations**
- HOMEASSISTANT_INTEGRATION.md - 20+ exemples

**Développement**
- CONTRIBUTING.md - Guide complet

---

## 📊 Fichiers de documentation

```
HA_VMI/
├── 📄 README.md                        # Guide principal
├── 📄 CONFIGURATION.md                 # Options config
├── 📄 HOMEASSISTANT_INTEGRATION.md    # Intégration HA
├── 📄 MQTT_ARCHITECTURE.md            # Structure MQTT
├── 📄 MIGRATION_GUIDE.md              # Depuis Jeedom
├── 📄 CONTRIBUTING.md                 # Développement
├── 📄 INDEX.md                        # Ce fichier
├── 📄 QUICKSTART.sh                   # Checklist rapide
│
├── 📁 config/
│   └── d1079-01-00.json              # Config VMI
│
└── 📁 homeassistant/
    ├── config.json                    # Config HA
    ├── const.py                       # Constantes
    └── entities.py                    # Entités
```

---

## 🎓 Apprentissage progressif

### Chemin d'apprentissage recommandé

```
1. README.md (5 min)
   ↓
2. CONFIGURATION.md (10 min)
   ↓
3. QUICKSTART.sh (15 min) 🚀 INSTALLER
   ↓
4. HOMEASSISTANT_INTEGRATION.md (30 min)
   ↓
5. Créer votre première automatisation
   ↓
6. MQTT_ARCHITECTURE.md (optionnel, 20 min)
   ↓
7. CONTRIBUTING.md (si développement)
```

**Temps total** : ~2h pour être opérationnel

---

## 💡 Conseils utiles

### Lecture rapide ⚡
- Parcourez les **TABLE OF CONTENTS** au début
- Utilisez **Find** (Ctrl+F) pour chercher des mots-clés
- Consultez les **Examples** pour des cas d'usage concrets

### Pour les problèmes 🔧
1. Vérifiez **Troubleshooting** au début du README
2. Cherchez votre problème dans les docs avec Ctrl+F
3. Consultez les **logs** : Settings → Addons → HA_VMI → Logs
4. Ouvrez une **issue GitHub**

### Pour les améliorations 💡
1. Vérifiez CONTRIBUTING.md
2. Consultez les **areas d'amélioration**
3. Commencez petit
4. Testez localement
5. Créez une PR

---

## 🔗 Ressources externes

### Home Assistant
- [Home Assistant Official](https://www.home-assistant.io/)
- [HA Community Forum](https://community.home-assistant.io/)
- [HA Integrations](https://www.home-assistant.io/integrations/)

### MQTT
- [MQTT.org](https://mqtt.org/)
- [MQTT Explorer](https://mqtt-explorer.com/)
- [MQTT Documentation](https://mosquitto.org/documentation/)

### EnOcean
- [EnOcean Alliance](https://www.enocean.com/)
- [EnOcean Python Library](https://github.com/kpeu3i/enocean)
- [EnOcean Profiles](https://www.enocean.com/en/knowledge-base-item/eep/)

### Ventilairsec / Purevent
- [Ventilairsec Official](https://www.ventilairsec.com/)
- [VMI Purevent Documentation](https://www.ventilairsec.com/en/products/purevent/)

---

## 📞 Support & Contact

### Besoin d'aide ?

1. **Consulter la documentation** → Commencez ici
2. **Vérifier les logs** → Settings → Addons → HA_VMI → Logs
3. **Chercher dans GitHub Issues** → https://github.com/fortinric88/VMI/issues
4. **Ouvrir une discussion** → https://github.com/fortinric88/VMI/discussions
5. **Créer une issue** → Si bug confirmé

### Partager un feedback

- ⭐ Star le repository si vous aimez
- 💬 Ouvrez une discussion pour vos idées
- 🐛 Reportez les bugs avec logs

---

## 📈 Feuille de route

### Version 1.0.0 (Actuelle) ✅
- ✅ Communication EnOcean
- ✅ Gestion VMI Purevent
- ✅ MQTT Discovery
- ✅ Documentation complète

### Version 1.1.0 (Prévue)
- 🔄 Support capteurs additionnels
- 🔄 Amélioration stabilité
- 🔄 Plus de tests

### Version 2.0.0 (Long terme)
- 📋 UI de configuration graphique
- 📋 Support d'autres marques VMI
- 📋 Intégration avancée HA

---

## 📝 Changelog

**Version 1.0.0** - Initial Release
- Addon Home Assistant complet
- Communication EnOcean
- Gestion VMI Purevent
- 50+ entités
- MQTT Discovery
- Documentation complète

---

**Dernière mise à jour** : 2025-01-15
**Versions documentées** : 1.0.0+
**Langue** : Français 🇫🇷

---

## 🎉 Bienvenue !

Merci d'utiliser **HA_VMI** ! Nous espérons que cette documentation vous sera utile.

**Bon automatisation ! 🚀**

---

*Cette page d'index aide à naviguer la documentation. Pour plus d'informations, consultez le README principal.*
