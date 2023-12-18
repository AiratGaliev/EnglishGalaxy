#!/bin/bash

if [ ! -d "venv" ]; then
    echo "Creating venv..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing dependencies..."
    pip install --upgrade pip setuptools wheel
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error happens. Deleting venv..."
        rm -rf venv
        exit 1
    fi
else
    source venv/bin/activate
fi
python3 start_cli.py
deactivate