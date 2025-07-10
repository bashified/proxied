#!/bin/bash

set -e

echo "[*] Starting installation..."

if ! command -v python3 &> /dev/null; then
    echo "[!] Python3 not found. Please install it first."
    exit 1
fi

echo "[*] Installing required Python packages..."
pip install -r requirements.txt

echo "[✔] Installation complete."