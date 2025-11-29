# 📚 Guide de création du dépôt séparé ha-vmi

## 🎯 Objectif

Créer un dépôt GitHub séparé `ha-vmi` contenant uniquement l'addon Home Assistant, sans les autres projets (Jeedom, etc.).

## 📋 Étapes à suivre

### Étape 1: Créer le dépôt GitHub

1. Allez sur https://github.com/new
2. **Repository name**: `ha-vmi`
3. **Description**: `Home Assistant addon for VMI Purevent and EnOcean sensors`
4. **Visibility**: Public ✅
5. **.gitignore**: Python
6. **License**: MIT
7. Cliquez **Create repository**

### Étape 2: Préparer les fichiers localement

```bash
cd /workspaces/VMI

# Exécutez le script de préparation
bash prepare-addon.sh
```

Cela créera un dossier `ha-vmi-addon-export` avec tous les fichiers nécessaires.

### Étape 3: Initialiser le dépôt local

```bash
# Créer un dossier temporaire de travail
mkdir -p ~/ha-vmi-work
cd ~/ha-vmi-work

# Copier tous les fichiers du dossier export
cp -r /workspaces/VMI/ha-vmi-addon-export/* .

# Initialiser git
git init
git add .
git commit -m "initial: setup home assistant addon for vmi purevent and enocean"

# Ajouter le remote et pousser
git remote add origin https://github.com/fortinric88/ha-vmi.git
git branch -M main
git push -u origin main
```

### Étape 4: Vérifier la structure

Le dépôt doit ressembler à ceci:

```
ha-vmi/
├── manifest.json          ✅ À la racine
├── Dockerfile             ✅ À la racine
├── requirements.txt
├── run.sh
├── ha_vmi_service.py
├── mqtt_discovery.py
├── README.md
├── LICENSE
├── .gitignore
├── .github/
│   └── workflows/
│       ├── build.yml
│       └── validate.yml
├── config/
├── homeassistant/
└── rootfs/
```

### Étape 5: Ajouter à Home Assistant

1. **Settings → Addons → Addon Store**
2. Cliquez sur **⋮ (Menu)** → **Repositories**
3. Ajoutez: `https://github.com/fortinric88/ha-vmi`
4. Cliquez **Create**

L'addon devrait maintenant apparaître dans le store! 🎉

## 🔄 Mise à jour future

Quand vous ferez des mises à jour:

1. Modifiez les fichiers dans le dépôt `ha-vmi`
2. Augmentez la version dans `manifest.json`
3. Committez et poussez
4. Les workflows GitHub Actions construiront et publieront automatiquement

## 🔗 Liens importants

- **Nouveau dépôt**: https://github.com/fortinric88/ha-vmi
- **Original (VMI)**: https://github.com/fortinric88/VMI
- **Home Assistant Docs**: https://developers.home-assistant.io/docs/add_ons

## ⚠️ Important

- Le dépôt `ha-vmi` doit être **public** pour Home Assistant
- Le fichier `manifest.json` doit être à la **racine** du dépôt
- Les images Docker seront publiées sur GHCR automatiquement
