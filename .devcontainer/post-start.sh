#!/bin/bash

echo "Running post-start.sh"

echo "Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh

echo "Installing Python dependencies"
uv sync --all-extras
