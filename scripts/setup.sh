#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python 3."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip is not installed. Please install pip for Python 3."
    exit 1
fi

# Create a virtual environment
echo "Creating a virtual environment..."
python3 -m venv venv

# Activate the virtual environment
echo "Activating the virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install development dependencies
echo "Installing development dependencies..."
pip install -r requirements.txt

# Install pre-commit hooks
echo "Setting up pre-commit hooks..."
pre-commit install

# Display success message
echo "Development environment setup complete!"
echo "To activate the virtual environment, run 'source venv/bin/activate'."
