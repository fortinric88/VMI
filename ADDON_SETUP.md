# 🎯 Mise en place complète - Addon HA VMI

## ✅ Ce qui a été créé/mis à jour

### 1. **repository.json** ✅ (RÉNOVÉ)
- Structure correcte pour Home Assistant
- Contient toutes les métadonnées nécessaires
- Références Docker correctes pour multi-architecture

**Location**: `/workspaces/VMI/repository.json`

### 2. **build.sh** - Script de construction Docker ✅ (CRÉÉ)
- Build local rapide (`--local`)
- Build multi-architecture (`--push`)
- Support pour amd64, armv7, aarch64

**Location**: `/workspaces/VMI/build.sh`

**Usage**:
```bash
./build.sh --local        # Build local
./build.sh --push         # Build et push vers GHCR
```

### 3. **GitHub Actions Workflows** ✅ (CRÉÉS)

#### `.github/workflows/build.yml`
- Construction automatique des images Docker
- Push vers GHCR après chaque commit sur `main`
- Support multi-architecture

#### `.github/workflows/validate.yml`
- Validation JSON des manifests
- Vérification de la structure du repository
- Exécuté à chaque changement

### 4. **BUILD_GUIDE.md** ✅ (CRÉÉ)
Guide complet pour :
- Comprendre le process de build
- Configuration locale
- Authentification GHCR
- Troubleshooting
- Mise à jour des versions

**Location**: `/workspaces/VMI/HA_VMI/BUILD_GUIDE.md`

### 5. **.dockerignore** ✅ (CRÉÉ)
Optimisation du build Docker :
- Exclut les fichiers inutiles
- Réduit la taille des images
- Accélère le build

**Location**: `/workspaces/VMI/HA_VMI/.dockerignore`

### 6. **validate-addon.sh** ✅ (CRÉÉ)
Script de validation :
- Vérifie tous les fichiers essentiels
- Valide la syntaxe JSON
- Checklist avant publication

**Location**: `/workspaces/VMI/validate-addon.sh`

## 🚀 Comment utiliser maintenant

### **Étape 1 : Commitez les changements**

```bash
cd /workspaces/VMI
git add .
git commit -m "feat: setup addon dockerfile and ci/cd pipelines"
git push
```

### **Étape 2 : Ajoutez le dépôt à Home Assistant**

1. **Settings → Addons → Addon Store**
2. Cliquez sur **⋮ (Menu)** → **Repositories**
3. Ajoutez : `https://github.com/fortinric88/VMI`
4. Cliquez sur **Create**

L'addon devrait maintenant apparaître ! ✅

### **Étape 3 : Vérifiez les builds automatiques**

- Allez sur votre dépôt GitHub
- Onglet **Actions**
- Vous verrez les workflows `build.yml` et `validate.yml` en action

### **Étape 4 : Configurez GHCR (optionnel)**

Pour que les images Docker se construisent automatiquement :

1. Vérifiez que votre dépôt est **public** (Settings → Visibility)
2. GitHub Actions a besoin du scope `write:packages`
3. Les images seront disponibles sous : `ghcr.io/fortinric88/ha_vmi-{arch}`

## 📊 Architecture de publication

```
Repository GitHub (fortinric88/VMI)
    ├── HA_VMI/
    │   ├── Dockerfile (construit l'image)
    │   ├── manifest.json (métadonnées addon)
    │   ├── requirements.txt
    │   ├── run.sh
    │   └── BUILD_GUIDE.md
    ├── repository.json (pointe vers l'addon)
    ├── build.sh (script de build local)
    └── .github/workflows/
        ├── build.yml (CI: build images)
        └── validate.yml (CI: valide manifests)
            ↓
    Publie vers GHCR
            ↓
    Disponible dans Home Assistant
```

## 📋 Checklist avant de partager

- [ ] Commitez et poussez tous les changements
- [ ] Vérifiez que GitHub Actions passe ✅
- [ ] Testez l'ajout du dépôt dans Home Assistant
- [ ] Vérifiez que l'addon apparaît dans le store
- [ ] Testez l'installation de l'addon

## 🔗 Ressources

- **Repository**: https://github.com/fortinric88/VMI
- **Guide d'intégration**: `HA_VMI/HOMEASSISTANT_INTEGRATION.md`
- **Guide de build**: `HA_VMI/BUILD_GUIDE.md`
- **Home Assistant Docs**: https://developers.home-assistant.io/

## ❓ Questions fréquentes

**Q: L'addon n'apparaît pas?**
A: Assurez-vous que `repository.json` est valide et que les workflows GitHub Actions se sont exécutés.

**Q: Comment tester localement?**
A: Utilisez `./build.sh --local` pour créer une image Docker locale.

**Q: Comment augmenter la version?**
A: Modifiez `HA_VMI/manifest.json` et `repository.json`, puis commitez.

---

**Setup complété le**: 29 novembre 2025 ✅
