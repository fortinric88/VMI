#!/bin/bash
# Script pour préparer les fichiers du nouvel addon séparé

set -e

OUTPUT_DIR="ha-vmi-addon-export"

# Créer le répertoire de sortie
mkdir -p "$OUTPUT_DIR"

echo "📦 Copie des fichiers essentiels..."

# Copier les fichiers principaux
cp /workspaces/VMI/HA_VMI/manifest.json "$OUTPUT_DIR/"
cp /workspaces/VMI/HA_VMI/Dockerfile "$OUTPUT_DIR/"
cp /workspaces/VMI/HA_VMI/requirements.txt "$OUTPUT_DIR/"
cp /workspaces/VMI/HA_VMI/run.sh "$OUTPUT_DIR/"
cp /workspaces/VMI/HA_VMI/ha_vmi_service.py "$OUTPUT_DIR/"
cp /workspaces/VMI/HA_VMI/mqtt_discovery.py "$OUTPUT_DIR/"
cp /workspaces/VMI/HA_VMI/README.md "$OUTPUT_DIR/"
cp /workspaces/VMI/HA_VMI/HOMEASSISTANT_INTEGRATION.md "$OUTPUT_DIR/"
cp /workspaces/VMI/HA_VMI/CONFIGURATION.md "$OUTPUT_DIR/"
cp /workspaces/VMI/HA_VMI/.dockerignore "$OUTPUT_DIR/"

echo "📁 Copie des répertoires..."

# Copier les répertoires
cp -r /workspaces/VMI/HA_VMI/config "$OUTPUT_DIR/" 2>/dev/null || true
cp -r /workspaces/VMI/HA_VMI/homeassistant "$OUTPUT_DIR/" 2>/dev/null || true
cp -r /workspaces/VMI/HA_VMI/rootfs "$OUTPUT_DIR/" 2>/dev/null || true

echo "📄 Création des fichiers supplémentaires..."

# Créer un README pour le nouveau dépôt
cat > "$OUTPUT_DIR/README.md" << 'EOF'
# HA VMI - Home Assistant Addon

Home Assistant addon for integrating VMI Purevent ventilation systems and EnOcean wireless sensors via MQTT.

## Features

- 🌬️ VMI Purevent ventilation system integration
- 📡 EnOcean wireless sensor support  
- 🏠 Native Home Assistant MQTT discovery
- 📊 Real-time sensor data and metrics
- 🔧 Easy configuration via addon UI

## Quick Start

1. Add this repository to Home Assistant:
   - Settings → Addons → Addon Store → Repositories
   - Add: `https://github.com/fortinric88/ha-vmi`

2. Install the addon from the store

3. Configure MQTT broker and device settings

4. Start the addon

## Documentation

- [Integration Guide](HOMEASSISTANT_INTEGRATION.md)
- [Configuration](CONFIGURATION.md)
- [Build Guide](BUILD_GUIDE.md)

## Support

For issues and feature requests, visit: https://github.com/fortinric88/ha-vmi

## License

See LICENSE file for details
EOF

# Créer un LICENSE
cat > "$OUTPUT_DIR/LICENSE" << 'EOF'
MIT License

Copyright (c) 2025 fortinric88

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
EOF

# Créer un .gitignore
cat > "$OUTPUT_DIR/.gitignore" << 'EOF'
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
.pytest_cache/
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
EOF

# Créer un .github/workflows pour le build
mkdir -p "$OUTPUT_DIR/.github/workflows"

cat > "$OUTPUT_DIR/.github/workflows/build.yml" << 'EOF'
name: Build and Push Addon Images

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  build:
    name: Build ${{ matrix.arch }}
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    strategy:
      matrix:
        include:
          - arch: amd64
            platform: linux/amd64
          - arch: armv7
            platform: linux/arm/v7
          - arch: aarch64
            platform: linux/arm64

    steps:
      - uses: actions/checkout@v3

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v2

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Log in to Container Registry
        uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: |
            ghcr.io/${{ github.repository_owner }}/ha-vmi-${{ matrix.arch }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=sha

      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          platforms: ${{ matrix.platform }}
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          build-args: |
            BUILD_FROM=ghcr.io/home-assistant/base:latest
EOF

cat > "$OUTPUT_DIR/.github/workflows/validate.yml" << 'EOF'
name: Validate Addon Manifest

on:
  push:
    branches:
      - main
    paths:
      - 'manifest.json'
  pull_request:
    branches:
      - main
    paths:
      - 'manifest.json'

jobs:
  validate:
    name: Validate Manifest
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Validate manifest.json syntax
        run: |
          python3 -m json.tool manifest.json > /dev/null
          echo "✅ manifest.json syntax valide"

      - name: Check required fields
        run: |
          python3 << 'PYEOF'
          import json
          
          required_fields = ['name', 'version', 'slug', 'description', 'arch', 'startup', 'boot']
          
          with open('manifest.json') as f:
              manifest = json.load(f)
          
          missing = [field for field in required_fields if field not in manifest]
          
          if missing:
              print(f"❌ Champs manquants: {', '.join(missing)}")
              exit(1)
          
          print("✅ Tous les champs requis sont présents")
          PYEOF
EOF

echo ""
echo "✅ Fichiers préparés dans: $OUTPUT_DIR"
echo ""
echo "📋 Fichiers inclus:"
ls -la "$OUTPUT_DIR" | grep -v "^total" | awk '{print "   " $9}'
echo ""
echo "📦 Prochaine étape:"
echo "   1. Créez un dépôt 'ha-vmi' sur GitHub"
echo "   2. Copiez le contenu de '$OUTPUT_DIR' dedans"
echo "   3. Committez et poussez"
echo "   4. Ajoutez https://github.com/fortinric88/ha-vmi à Home Assistant"
