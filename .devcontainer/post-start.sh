#!/bin/bash

echo "Running post-start.sh"

echo "Installing Poetry..."
pip install poetry==1.8.3

echo "Installing Python dependencies"
poetry install
