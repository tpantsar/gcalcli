#!/bin/bash

# Detect OS
OS="$(uname -s)"

echo "🔍 Detecting OS..."
if [[ "$OS" == "Linux" ]]; then
    echo "✅ Linux detected. Setting up virtual environment..."
    
    # Create virtual environment
    python3 -m venv .venv
    source .venv/bin/activate

    # Install dependencies
    pip install .

    # Move gcalcli to /usr/local/bin
    if [[ -f ".venv/bin/gcalcli" ]]; then
        sudo cp .venv/bin/gcalcli /usr/local/bin/
        echo "✅ gcalcli copied to /usr/local/bin"
    else
        echo "⚠️ gcalcli not found in .venv/bin/"
    fi

elif [[ "$OS" == "MINGW"* || "$OS" == "CYGWIN"* || "$OS" == "MSYS"* ]]; then
    echo "✅ Windows detected. Setting up virtual environment..."

    # Create virtual environment
    python -m venv .venv
    source .venv/Scripts/activate

    # Install dependencies
    pip install .

    # Move gcalcli to $HOME/bin
    if [[ -f ".venv/Scripts/gcalcli" ]]; then
        POWERSHELL_CMD='[System.Environment]::SetEnvironmentVariable("Path", `$env:Path + ";$env:USERPROFILE\\bin", [System.EnvironmentVariableTarget]::User)'
        powershell.exe -Command "$POWERSHELL_CMD"
        echo "Added $HOME\\bin to PATH in Windows."

        cp .venv/Scripts/gcalcli $HOME/bin/
        echo "✅ gcalcli copied to $HOME\\bin"
    else
        echo "⚠️ gcalcli not found in .venv/Scripts/"
    fi

else
    echo "❌ Unsupported OS: $OS"
    exit 1
fi

echo "✅ Installation complete! Run 'gcalcli --help' to verify."
