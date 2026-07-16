#!/usr/bin/env bash

set -euo pipefail

LAYER_NAME="${1:?Layer name required}"
BUILD_DIR=".build"
LAYER_BUILD_DIR="${BUILD_DIR}/${LAYER_NAME}"
PYTHON_DIR="${LAYER_BUILD_DIR}/python"
ZIP_FILE="${BUILD_DIR}/${LAYER_NAME}-layer.zip"

LAYER_DIR="src/${LAYER_NAME}"

rm -rf "$LAYER_BUILD_DIR"
rm -f "$ZIP_FILE"

mkdir -p "$PYTHON_DIR"

cp -r "$LAYER_DIR" "$PYTHON_DIR/"

(
  cd "$LAYER_BUILD_DIR"
  zip -r "../${LAYER_NAME}-layer.zip" python > /dev/null
)

echo "$ZIP_FILE"

