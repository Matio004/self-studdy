#!/usr/bin/env bash

set -euo pipefail

FUNCTION_KEY="${1:?Function key required}"
FUNCTION_NAME="${2:?Function name required}"
BUILD_DIR=".build"
LAMBDA_DIR="src/${FUNCTION_KEY}"
ZIP_FILE="${BUILD_DIR}/${FUNCTION_KEY}.zip"

if [ ! -d "$LAMBDA_DIR" ]; then
  echo "Lambda directory does not exist: $LAMBDA_DIR"
  exit 1
fi

rm -f "$ZIP_FILE"
mkdir -p "$BUILD_DIR"

(
  cd "$LAMBDA_DIR"
  zip -r "../../${ZIP_FILE}" . > /dev/null
)

aws lambda update-function-code \
  --function-name "$FUNCTION_NAME" \
  --zip-file "fileb://${ZIP_FILE}" > /dev/null

echo "Deployed function: $FUNCTION_KEY -> $FUNCTION_NAME"
