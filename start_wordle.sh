#!/bin/bash

# Terminal-based Wordle Game Launcher for Linux/macOS
echo "Starting Wordle Terminal Game..."

# Check if Python is installed
if command -v python3 &>/dev/null; then
    # Check if colorama is installed
    if python3 -c "import colorama" &>/dev/null; then
        # Run the game
        python3 wordle.py
    else
        echo "Colorama package is required but not installed."
        echo "Installing colorama..."
        pip3 install colorama
        echo "Launching the game..."
        python3 wordle.py
    fi
else
    echo "Python 3 is required to run this game but is not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi