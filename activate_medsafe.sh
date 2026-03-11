#!/bin/bash
# MedSafe AI Virtual Environment Activation Script
# Usage: source activate_medsafe.sh

if [ -f "medsafe_env/bin/activate" ]; then
    source medsafe_env/bin/activate
    echo "✓ MedSafe AI virtual environment activated"
    echo "  Python: $(python --version)"
    echo "  Location: $(which python)"
else
    echo "✗ Error: Virtual environment not found"
    echo "  Please ensure you're in the MedSafe project directory"
    exit 1
fi
