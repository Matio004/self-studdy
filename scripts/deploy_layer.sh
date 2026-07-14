#!/usr/bin/env bash

set -euo pipefail

LAYER_NAME="${1:?Layer name required}"
ZIP_FILE="${2:?Zip file required}"
RUNTIME="${3:-python3.12}"

LAYER_ARN=$(
  aws lambda publish-layer-version \
    --layer-name "$LAYER_NAME" \
    --zip-file "fileb://${ZIP_FILE}" \
    --compatible-runtimes "$RUNTIME" \
    --query LayerVersionArn \
    --output text
)

echo "$LAYER_ARN"
