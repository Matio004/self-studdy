#!/usr/bin/env bash

set -euo pipefail

TERRAFORM_DIR="terraform"
RUNTIME="python3.12"

COMMON_LAYER_NAME=$(
  terraform -chdir="$TERRAFORM_DIR" output -raw common_layer_name
)

DEPENDENCIES_LAYER_NAME=$(
  terraform -chdir="$TERRAFORM_DIR" output -raw dependencies_layer_name
)

echo "Building common layer..."
COMMON_ZIP=$(./scripts/build_common_layer.sh)

echo "Publishing common layer..."
COMMON_LAYER_ARN=$(
  ./scripts/deploy_layer.sh "$COMMON_LAYER_NAME" "$COMMON_ZIP" "$RUNTIME"
)

echo "Common layer ARN:"
echo "$COMMON_LAYER_ARN"

echo "Building dependencies layer..."
DEPENDENCIES_ZIP=$(./scripts/build_dependencies_layer.sh)

echo "Publishing dependencies layer..."
DEPENDENCIES_LAYER_ARN=$(
  ./scripts/deploy_layer.sh "$DEPENDENCIES_LAYER_NAME" "$DEPENDENCIES_ZIP" "$RUNTIME"
)

echo "Dependencies layer ARN:"
echo "$DEPENDENCIES_LAYER_ARN"

echo "Updating Lambda configurations with layers..."

LAMBDA_FUNCTIONS_JSON=$(
  terraform -chdir="$TERRAFORM_DIR" output -json lambda_functions
)

echo "$LAMBDA_FUNCTIONS_JSON" | jq -r 'to_entries[] | "\(.key) \(.value)"' |
while read -r FUNCTION_KEY FUNCTION_NAME; do
  echo "Updating layers for: $FUNCTION_KEY -> $FUNCTION_NAME"

  aws lambda update-function-configuration \
    --function-name "$FUNCTION_NAME" \
    --layers "$COMMON_LAYER_ARN" "$DEPENDENCIES_LAYER_ARN" > /dev/null

  echo "Waiting for configuration update..."
  aws lambda wait function-updated \
    --function-name "$FUNCTION_NAME"

  echo "Deploying code for: $FUNCTION_KEY"
  ./scripts/deploy_function.sh "$FUNCTION_KEY" "$FUNCTION_NAME"
done

echo "Deploy completed."
