#!/bin/bash

if [ ! -d "venv" ]; then
    echo "Creating venv..."
    python -m venv venv
    source venv/bin/activate
    echo "Installing dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error happens. Deleting venv..."
        rm -rf venv
        exit 1
    fi
else
    source venv/bin/activate
fi
python main.py
deactivate