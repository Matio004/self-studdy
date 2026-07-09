#!/usr/bin/env bash

rm -r layer

mkdir -p "layer/python"


uv sync

uv export --no-dev --format requirements.txt > requirements.txt

uv pip --managed-python install \
    --target layer/python \
    -r requirements.txt
