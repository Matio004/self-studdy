#!/usr/bin/env bash

rm -r layer
mkdir -p "layer/python"

uv export --format requirements.txt > requirements.txt

uv pip install \
  --target layer/python \
  -r requirements.txt