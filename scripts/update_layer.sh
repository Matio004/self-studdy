#!/usr/bin/env bash

set -euo pipefail

LAYER_NAME="${1:?Layer name required}"

TERRAFORM_DIR="terraform"
# get function names - terraform
FUNCTIONS=$(
	terraform -chdir="$TERRAFORM_DIR" output --json lambda_functions
)
#
# build layer
LAYER_ZIP_FILE=$(./scripts/build_layer.sh "$LAYER_NAME")
#
#publish layer
LAYER_ARN=$(./scripts/deploy_layer.sh "$LAYER_NAME" "$LAYER_ZIP_FILE")
# get current layers
echo "$FUNCTIONS" | jq -r ".[]" |
while read -r FUNCTION_NAME; do
	echo "Updating layer $LAYER_NAME for $FUNCTION_NAME"
CURRENT_LAYERS=$(
	aws lambda get-function-configuration \
	--function-name "$FUNCTION_NAME" \
	--query "Layers[].Arn" \
	--output json
)

if [[ "$CURRENT_LAYERS" != *":layer:$LAYER_NAME:"* ]]; then
    echo "Layer not attached, skipping"
    continue
fi
	UPDATED_LAYERS=$(
	jq \
	--arg layer_name "$LAYER_NAME" \
	--arg new_arn "$LAYER_ARN" \
	'
	map(
		if test(":layer:" + $layer_name + ":[0-9]+$")
		then $new_arn
		else .
		end
	)
	' <<< "$CURRENT_LAYERS"
)
		aws lambda update-function-configuration \
	--function-name "$FUNCTION_NAME" \
	--layers $(jq -r '.[]' <<< "$UPDATED_LAYERS") > /dev/null
done
# change layer verion
#
# update

