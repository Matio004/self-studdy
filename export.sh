#!/usr/bin/env bash

rm -r layer
mkdir -p "layer/python"


uv sync

cp -r .venv/lib/python3.12/site-packages/* layer/python/
