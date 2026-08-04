#!/usr/bin/env bash
set -euo pipefail

# Run this ON the Raspberry Pi (Raspberry Pi OS / Debian-based), as a user
# with sudo access. Installs the rpi-rgb-led-matrix C++ library + Python
# bindings, this project's Python dependencies, and a systemd service that
# starts the dashboard on boot.

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MATRIX_LIB_DIR="$HOME/rpi-rgb-led-matrix"

echo "==> Installing build dependencies"
sudo apt-get update
sudo apt-get install -y git python3-dev python3-pip python3-venv build-essential libjpeg-dev libpng-dev

if [ ! -d "$MATRIX_LIB_DIR" ]; then
  echo "==> Cloning hzeller/rpi-rgb-led-matrix"
  git clone https://github.com/hzeller/rpi-rgb-led-matrix.git "$MATRIX_LIB_DIR"
fi

echo "==> Building the matrix library + Python bindings"
cd "$MATRIX_LIB_DIR"
make build-python PYTHON="$(which python3)"
sudo make install-python PYTHON="$(which python3)"

echo "==> Setting up this project's virtualenv"
cd "$REPO_DIR"
# --system-site-packages so the venv can see the rgbmatrix bindings just
# installed above into the system Python.
python3 -m venv --system-site-packages .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

if [ ! -f .env ]; then
  cp .env.example .env
  echo "==> Created .env from .env.example - fill in your API keys before starting the service"
fi

echo "==> Installing systemd service"
sudo cp scripts/dashboard.service /etc/systemd/system/dashboard.service
sudo sed -i "s#__REPO_DIR__#$REPO_DIR#g" /etc/systemd/system/dashboard.service
sudo systemctl daemon-reload
sudo systemctl enable dashboard.service

echo
echo "Done."
echo "Next steps:"
echo "  1. Edit $REPO_DIR/.env with your OpenWeatherMap and Spotify API keys"
echo "  2. Run: .venv/bin/python scripts/spotify_auth.py   (one-time, adds SPOTIFY_REFRESH_TOKEN to .env)"
echo "  3. Run: sudo systemctl start dashboard"
