#!/bin/bash
# Script de validation pour l'addon HA VMI

set -e

echo "🔍 Validation de l'addon HA VMI..."
echo ""

# Vérifier les fichiers essentiels
echo "📋 Vérification des fichiers essentiels..."
required_files=(
    "HA_VMI/manifest.json"
    "HA_VMI/Dockerfile"
    "HA_VMI/requirements.txt"
    "HA_VMI/run.sh"
    "HA_VMI/ha_vmi_service.py"
    "repository.json"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ MANQUANT: $file"
        exit 1
    fi
done

echo ""
echo "📝 Validation des fichiers JSON..."

# Vérifier la syntaxe JSON
if command -v python3 &> /dev/null; then
    echo "  - Validation de manifest.json..."
    python3 -m json.tool HA_VMI/manifest.json > /dev/null && echo "    ✅ Syntaxe valide"
    
    echo "  - Validation de repository.json..."
    python3 -m json.tool repository.json > /dev/null && echo "    ✅ Syntaxe valide"
else
    echo "⚠️  Python3 non disponible, validation JSON skippée"
fi

echo ""
echo "🐳 Vérification du Dockerfile..."
if grep -q "FROM" HA_VMI/Dockerfile; then
    echo "✅ Dockerfile contient une instruction FROM"
fi

if grep -q "COPY requirements.txt" HA_VMI/Dockerfile; then
    echo "✅ Dockerfile copie requirements.txt"
fi

if grep -q "pip install" HA_VMI/Dockerfile; then
    echo "✅ Dockerfile installe les dépendances Python"
fi

echo ""
echo "🔧 Vérification du manifest.json..."
if grep -q '"name"' HA_VMI/manifest.json; then
    echo "✅ Contient le champ 'name'"
fi

if grep -q '"slug"' HA_VMI/manifest.json; then
    echo "✅ Contient le champ 'slug'"
fi

if grep -q '"version"' HA_VMI/manifest.json; then
    echo "✅ Contient le champ 'version'"
fi

if grep -q '"arch"' HA_VMI/manifest.json; then
    echo "✅ Contient le champ 'arch'"
fi

echo ""
echo "📦 Vérification du repository.json..."
if grep -q '"addons"' repository.json; then
    echo "✅ Contient la liste des addons"
fi

if grep -q '"ha_vmi"' repository.json; then
    echo "✅ Contient l'addon 'ha_vmi'"
fi

if grep -q '"image"' repository.json; then
    echo "✅ Contient les références d'image Docker"
fi

echo ""
echo "🚀 Vérification du script run.sh..."
if [ -x "HA_VMI/run.sh" ]; then
    echo "✅ run.sh est exécutable"
else
    echo "⚠️  run.sh n'est pas exécutable"
    chmod +x HA_VMI/run.sh
fi

echo ""
echo "📄 Vérification de la documentation..."
docs=(
    "HA_VMI/HOMEASSISTANT_INTEGRATION.md"
    "HA_VMI/BUILD_GUIDE.md"
    "HA_VMI/CONFIGURATION.md"
)

for doc in "${docs[@]}"; do
    if [ -f "$doc" ]; then
        echo "✅ $doc"
    else
        echo "⚠️  MANQUANT: $doc"
    fi
done

echo ""
echo "════════════════════════════════════════════"
echo "✅ Validation complète réussie!"
echo "════════════════════════════════════════════"
echo ""
echo "📝 Prochaines étapes:"
echo "  1. Commitez les changements: git add . && git commit -m 'chore: setup addon'"
echo "  2. Poussez vers GitHub: git push"
echo "  3. Vérifiez les workflows GitHub Actions"
echo "  4. Les images Docker seront automatiquement construites et publiées"
echo ""
