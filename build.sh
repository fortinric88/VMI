#!/bin/bash
# Script de construction Docker pour l'addon HA VMI
# Usage: ./build.sh [--push] [--local]

set -e

ADDON_NAME="ha_vmi"
ADDON_PATH="./HA_VMI"
REGISTRY="ghcr.io"
OWNER="fortinric88"
PUSH_IMAGES=false
LOCAL_BUILD=false

# Parse les arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --push)
            PUSH_IMAGES=true
            shift
            ;;
        --local)
            LOCAL_BUILD=true
            shift
            ;;
        *)
            echo "Usage: $0 [--push] [--local]"
            exit 1
            ;;
    esac
done

# Architectures supportées
ARCHS=("amd64" "armv7" "aarch64")

echo "🔨 Construction de l'addon HA VMI..."
echo "Path: $ADDON_PATH"
echo "Registry: $REGISTRY"
echo "Owner: $OWNER"

cd "$ADDON_PATH" || exit 1

if [ "$LOCAL_BUILD" = true ]; then
    echo "🐳 Construction locale..."
    docker build -t "${OWNER}/${ADDON_NAME}:latest" .
    echo "✅ Image locale créée: ${OWNER}/${ADDON_NAME}:latest"
else
    for arch in "${ARCHS[@]}"; do
        IMAGE="${REGISTRY}/${OWNER}/${ADDON_NAME}-${arch}:latest"
        echo ""
        echo "🏗️  Construction pour architecture: $arch"
        echo "Image: $IMAGE"
        
        docker buildx build \
            --platform "linux/${arch}" \
            -t "$IMAGE" \
            --build-arg "BUILD_FROM=ghcr.io/home-assistant/base:latest" \
            .
        
        if [ "$PUSH_IMAGES" = true ]; then
            echo "📤 Push de l'image vers le registre..."
            docker push "$IMAGE"
        fi
    done
fi

cd - > /dev/null

echo ""
echo "✅ Construction terminée avec succès!"
echo ""
echo "📝 Pour pusher les images:"
echo "  ./build.sh --push"
echo ""
echo "🐳 Pour un build local rapide:"
echo "  ./build.sh --local"
