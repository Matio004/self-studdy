#!/usr/bin/env bash

set -euo pipefail

BUILD_DIR=".build"
LAYER_BUILD_DIR="${BUILD_DIR}/common"
PYTHON_DIR="${LAYER_BUILD_DIR}/python"
ZIP_FILE="${BUILD_DIR}/common-layer.zip"

rm -rf "$LAYER_BUILD_DIR"
rm -f "$ZIP_FILE"

mkdir -p "$PYTHON_DIR"

cp -r src/common "$PYTHON_DIR/"

(
  cd "$LAYER_BUILD_DIR"
  zip -r "../common-layer.zip" python > /dev/null
)

echo "$ZIP_FILE"
