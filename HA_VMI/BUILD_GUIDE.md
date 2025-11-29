# Guide de Build et Publication - HA VMI Addon

## 📋 Vue d'ensemble

Ce guide explique comment construire et publier l'addon HA VMI sur GitHub Container Registry (GHCR).

## 🔧 Prérequis

- Docker installé et configuré
- Docker Buildx (pour les builds multi-architecture)
- Accès à GitHub Container Registry (GHCR)
- Git avec accès au dépôt

### Installation de Docker Buildx

```bash
# Sur Linux
docker buildx create --name mybuilder
docker buildx use mybuilder

# Vérifier l'installation
docker buildx ls
```

## 🏗️ Build Local

### Build simple (architecture locale)

```bash
./build.sh --local
```

Cela créera une image Docker locale :
```
fortinric88/ha_vmi:latest
```

### Build multi-architecture

```bash
# Nécessite Docker Buildx configuré
./build.sh
```

Cela construira les images pour :
- `amd64` (Intel/AMD 64-bit)
- `armv7` (ARM 32-bit - Raspberry Pi)
- `aarch64` (ARM 64-bit)

## 📤 Publication sur GHCR

### 1. Configuration de l'authentification

```bash
# Via token personnalisé
docker login ghcr.io
# Utilisateur: <votre_username>
# Password: <votre_personal_access_token>

# Ou via gh CLI
gh auth login
gh auth status
```

**Créer un Personal Access Token** :
1. Allez sur https://github.com/settings/tokens
2. Cliquez "Generate new token (classic)"
3. Sélectionnez le scope `write:packages`
4. Copiez le token

### 2. Build et push automatique

```bash
./build.sh --push
```

Cela va :
1. Construire les images pour toutes les architectures
2. Pousser vers `ghcr.io/fortinric88/ha_vmi-{arch}`

### 3. Vérification

```bash
# Lister les images publiées
docker image ls | grep ha_vmi

# Ou sur GitHub
# Settings → Packages and registries → Containers
```

## 🤖 Build Automatique (GitHub Actions)

Les workflows GitHub Actions construisent et publient automatiquement les images lors d'un push sur `main` :

### Workflows disponibles

| Workflow | Déclencheur | Action |
|----------|------------|--------|
| `build.yml` | Push sur `main` ou PR | Construit et pousse les images |
| `validate.yml` | Changement de manifest | Valide les fichiers JSON |

### Statut des builds

Consultez l'onglet **Actions** de votre dépôt GitHub pour voir :
- L'état des builds
- Les logs de compilation
- Les images publiées

## 📦 Structure des images publiées

Les images sont publiées sous :
```
ghcr.io/fortinric88/ha_vmi-{arch}:latest
ghcr.io/fortinric88/ha_vmi-{arch}:v1.0.0
ghcr.io/fortinric88/ha_vmi-{arch}:sha-<commit>
```

Exemple :
```
ghcr.io/fortinric88/ha_vmi-amd64:latest
ghcr.io/fortinric88/ha_vmi-armv7:latest
ghcr.io/fortinric88/ha_vmi-aarch64:latest
```

## 🐛 Troubleshooting

### Erreur: "Unknown flag: --push"

```bash
# Vérifiez que buildx est configuré
docker buildx ls

# Si absent, installez-le
docker buildx create --use
```

### Erreur: "denied: access denied"

```bash
# Vérifiez l'authentification
docker logout ghcr.io
docker login ghcr.io

# Utilisez un Personal Access Token valide avec scope "write:packages"
```

### Erreur: "No such file: Dockerfile"

```bash
# Vérifiez que vous êtes dans le bon répertoire
cd /workspaces/VMI
ls HA_VMI/Dockerfile
```

## 🔄 Mise à jour de version

Pour augmenter la version :

1. Modifiez `HA_VMI/manifest.json` :
```json
{
  "version": "1.0.1"
}
```

2. Modifiez `repository.json` :
```json
{
  "ha_vmi": {
    "version": "1.0.1"
  }
}
```

3. Committez et poussez :
```bash
git add HA_VMI/manifest.json repository.json
git commit -m "chore: bump version to 1.0.1"
git push
```

Les images seront automatiquement construites et publiées avec le nouveau tag de version.

## 📚 Ressources

- [Home Assistant Add-on Development](https://developers.home-assistant.io/docs/add_ons)
- [Docker Buildx Documentation](https://docs.docker.com/build/buildx/)
- [GitHub Container Registry](https://docs.github.com/packages/guides/about-github-container-registry)
- [Manifests Add-on](https://developers.home-assistant.io/docs/add_ons/manifest/)

## ✅ Checklist avant publication

- [ ] Les fichiers manifests sont validés (pas d'erreurs de syntaxe JSON)
- [ ] Les architectures sont correctes (amd64, armv7, aarch64)
- [ ] Le numéro de version est à jour
- [ ] Les dépendances Python sont à jour dans `requirements.txt`
- [ ] Le Dockerfile construis correctement
- [ ] Les tests passent (s'il y en a)
- [ ] La documentation est à jour

