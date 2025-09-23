#!/bin/bash

# Detect OS
OS="$(uname -s)"

echo "🔍 Detecting OS..."
if [[ "$OS" == "Linux" ]]; then
  echo "Linux detected. Setting up virtual environment..."

  REPO_PATH="$HOME/gcalcli"
  INSTALL_PATH="/usr/local/bin"

  sudo mkdir -p "$INSTALL_PATH"

  if [[ ! -d "$REPO_PATH" ]]; then
    echo "Cloning gcalcli repository to $REPO_PATH..."
    git clone https://github.com/tpantsar/gcalcli.git "$REPO_PATH"
    cd $REPO_PATH || {
      echo "Failed to enter gcalcli repository directory"
      exit 1
    }
  else
    echo "gcalcli repository already exists at $REPO_PATH. Pulling latest changes..."
    cd $REPO_PATH || {
      echo "Failed to enter gcalcli repository directory"
      exit 1
    }
    git checkout main
    git pull origin main
  fi

  # Create virtual environment
  if ! command -v python3 &>/dev/null; then
    echo "python3 is not installed. Please install Python 3 and try again."
    exit 1
  fi
  python3 -m venv .venv
  source .venv/bin/activate

  # Install dependencies
  pip install .
  deactivate

  # Copy gcalcli to install path
  if [[ -f ".venv/bin/gcalcli" ]]; then
    sudo cp .venv/bin/gcalcli $INSTALL_PATH
    echo "✅ gcalcli copied to $INSTALL_PATH"
  else
    echo "⚠️ gcalcli not found in .venv/bin/"
  fi

elif [[ "$OS" == "MINGW"* || "$OS" == "CYGWIN"* || "$OS" == "MSYS"* ]]; then
  echo "Windows detected. Setting up virtual environment..."

  REPO_PATH="$HOME/gcalcli"
  INSTALL_PATH="$HOME/bin"

  git clone https://github.com/tpantsar/gcalcli.git "$REPO_PATH"
  cd $REPO_PATH || {
    echo "Failed to enter gcalcli directory"
    exit 1
  }

  # Create virtual environment
  python -m venv .venv
  source .venv/Scripts/activate

  # Install dependencies
  pip install .
  deactivate

  # Copy gcalcli to install path
  if [[ -f ".venv/Scripts/gcalcli" ]]; then
    POWERSHELL_CMD='[System.Environment]::SetEnvironmentVariable("Path", `$env:Path + ";$env:USERPROFILE\\bin", [System.EnvironmentVariableTarget]::User)'
    powershell.exe -Command "$POWERSHELL_CMD"
    echo "Added $HOME\\bin to PATH in Windows."

    cp .venv/Scripts/gcalcli $INSTALL_PATH
    echo "✅ gcalcli copied to $INSTALL_PATH"
  else
    echo "⚠️ gcalcli not found in .venv/Scripts/"
  fi

else
  echo "❌ Unsupported OS: $OS"
  exit 1
fi

echo "✅ Installation complete! Run 'gcalcli init' to authenticate."
