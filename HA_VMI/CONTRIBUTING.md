# Contribuer à HA_VMI

Merci de votre intérêt pour contribuer à HA_VMI ! 🎉

## 🐛 Signaler un bug

Si vous trouvez un bug, créez une issue GitHub :

1. Allez sur https://github.com/fortinric88/VMI/issues
2. Cliquez sur "New issue"
3. Décrivez le problème :
   - Version de l'addon
   - Étapes pour reproduire
   - Comportement attendu vs réel
   - Logs (Settings → Add-ons → HA_VMI → Logs)

### Template de bug report

```markdown
**Describe the bug**
[Décrivez le problème ici]

**To Reproduce**
1. [Étape 1]
2. [Étape 2]
3. [Étape 3]

**Expected behavior**
[Ce qui devrait se passer]

**Actual behavior**
[Ce qui se passe réellement]

**Environment**
- Home Assistant version: [e.g. 2025.1.0]
- HA_VMI version: [e.g. 1.0.0]
- Device: [Raspberry Pi / x86 / etc]
- Logs: [Copier les logs pertinents]
```

## 💡 Proposer une amélioration

Vous avez une idée pour améliorer HA_VMI ?

1. Ouvrez une issue GitHub avec le label `enhancement`
2. Décrivez :
   - Quel est le problème/limitation actuelle
   - Votre proposition de solution
   - Cas d'usage

## 🔧 Développement

### Installation locale

```bash
# Clone le repository
git clone https://github.com/fortinric88/VMI.git
cd VMI/HA_VMI

# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Installer les dépendances de développement
pip install black flake8 pytest
```

### Structure du code

```
HA_VMI/
├── run.py                  # Point d'entrée principal
├── ha_vmi_service.py      # Services (EnOcean, MQTT, VMI)
├── mqtt_discovery.py      # MQTT Discovery generator
├── homeassistant/
│   ├── const.py          # Constantes
│   └── entities.py       # Définitions des entités
└── tests/                # Tests unitaires
```

### Conventions de code

- **Python** : PEP 8 avec `black` et `flake8`
- **Logging** : Utiliser le logger standard Python
- **Documentation** : Docstrings pour chaque classe/fonction
- **Type hints** : Recommandé pour les nouvelles fonctions

### Exemple de code

```python
def example_function(param1: str, param2: int) -> dict:
    """
    Description courte.
    
    Paramètres:
        param1: Description du paramètre 1
        param2: Description du paramètre 2
    
    Returns:
        dict: Description du retour
    
    Raises:
        ValueError: Si param2 est négatif
    """
    logger.debug(f"Processing {param1} with {param2}")
    
    if param2 < 0:
        raise ValueError("param2 must be positive")
    
    return {"result": param1 * param2}
```

### Linting

```bash
# Vérifier le style de code
flake8 ha_vmi_service.py --max-line-length=100

# Formater automatiquement
black ha_vmi_service.py
```

### Tests

```bash
# Lancer les tests
pytest tests/ -v

# Avec couverture
pytest tests/ --cov=. --cov-report=html
```

### Building du Docker

```bash
# Build l'image
docker build -t ha_vmi:latest .

# Tester localement
docker run -it -v $(pwd):/addon ha_vmi:latest
```

## 📝 Pull Request Process

1. **Fork** le repository
2. **Créez une branche** : `git checkout -b feature/votre-feature`
3. **Committez vos changements** : `git commit -m "Add votre feature"`
4. **Poussez vers GitHub** : `git push origin feature/votre-feature`
5. **Ouvrez une Pull Request**

### Checklist pour PR

- [ ] Votre code suit PEP 8
- [ ] Tests unitaires ajoutés/modifiés
- [ ] Documentation mise à jour
- [ ] Aucun secret/mot de passe dans le code
- [ ] Messages de commit clairs et concis
- [ ] Référence les issues associées

### Template de PR

```markdown
## Description
[Description brève des changements]

## Type de changement
- [ ] Bug fix (non-breaking change)
- [ ] Nouvelle fonctionnalité (non-breaking change)
- [ ] Breaking change
- [ ] Documentation

## Testing
Décrivez comment vous avez testé:
- [x] Test A
- [x] Test B

## Checklist
- [x] Suivis les guidelines
- [x] Code commenté/documenté
- [x] Tests ajoutés
- [x] Documentation mise à jour
```

## 🏆 Areas d'amélioration

### Priorité haute
- [ ] Support pour capteurs EnOcean additionnels
- [ ] Gestion avancée des erreurs
- [ ] Tests de stress/performance
- [ ] Documentation en plusieurs langues

### Priorité moyenne
- [ ] UI de configuration graphique
- [ ] Intégration Influx DB
- [ ] Support Home Assistant Cloud
- [ ] Automatisations pré-définies

### Priorité basse
- [ ] Dashboard Grafana template
- [ ] Support pour autres marques VMI
- [ ] API REST supplémentaire
- [ ] Support Zigbee

## 📚 Documentation

### Ajouter une fonctionnalité = Ajouter de la doc

Pour chaque nouvelle fonction:
1. Docstring complète dans le code
2. Exemple dans les docs
3. Test unitaire
4. Mise à jour du README

### Fichiers de documentation

- **README.md** : Vue d'ensemble, démarrage rapide
- **CONFIGURATION.md** : Options de configuration
- **HOMEASSISTANT_INTEGRATION.md** : Intégration HA
- **MQTT_ARCHITECTURE.md** : Structure MQTT
- **MIGRATION_GUIDE.md** : Historique/comparaisons

## 🔐 Security

### Signaler une vulnérabilité

**Ne créez PAS une issue publique** pour les vulnérabilités.

Contactez : [email de sécurité à définir]

## 🤝 Code of Conduct

Soyez respectueux, constructif, et inclusif. Nous accueillons tous les niveaux de compétence.

## 📊 Git Workflow

```bash
# Mettre à jour depuis master
git fetch origin
git rebase origin/main

# Avant de faire un commit
black .
flake8 .
pytest

# Ajouter les changements
git add .
git commit -m "Descriptive message"

# Push vers votre fork
git push origin feature/votre-feature
```

## 📞 Questions ?

- 📖 Consultez la documentation
- 🐛 Cherchez des issues similaires
- 💬 Ouvrez une discussion : https://github.com/fortinric88/VMI/discussions

## 🎉 Merci !

Chaque contribution, même petite, compte. Merci d'améliorer HA_VMI ! 🚀
