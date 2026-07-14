#!/usr/bin/env bash

set -euo pipefail

BUILD_DIR=".build"

LAYER_BUILD_DIR="${BUILD_DIR}/dependencies"
PYTHON_DIR="${LAYER_BUILD_DIR}/python"

ZIP_FILE="${BUILD_DIR}/dependencies-layer.zip"
REQ_FILE="${BUILD_DIR}/requirements.txt"

rm -rf "$LAYER_BUILD_DIR"
rm -f "$ZIP_FILE"
rm -f "$REQ_FILE"

mkdir -p "$PYTHON_DIR"

uv sync
uv export --no-dev --format requirements.txt > "$REQ_FILE"

uv pip --managed-python install \
  --target "$PYTHON_DIR" \
  -r "$REQ_FILE"

(
  cd "$LAYER_BUILD_DIR"
  zip -r ../dependencies-layer.zip python > /dev/null
)

echo "$ZIP_FILE"

