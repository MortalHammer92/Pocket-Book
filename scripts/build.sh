#!/usr/bin/env bash
# Builds Pocket Book on macOS or Linux (Python 3.10+ with Tkinter required).
# The easiest way is still to download the ready-made version from GitHub Releases.
set -euo pipefail
cd "$(dirname "$0")/.."

python3 -c "import tkinter" || {
  echo "Tkinter is missing."
  echo "  Debian/Ubuntu: sudo apt install python3-tk"
  echo "  Fedora:        sudo dnf install python3-tkinter"
  echo "  macOS:         brew install python-tk   (or Python from python.org)"
  exit 1
}
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip pyinstaller pillow
mkdir -p release

if [[ "$(uname)" == "Darwin" ]]; then
  .venv/bin/python -m PyInstaller --noconfirm --clean --windowed --name "Pocket Book" \
    --icon assets/pocketbook.png --add-data "assets/pocketbook.png:." \
    --osx-bundle-identifier io.github.mortalhammer92.pocketbook pocket_book.py
  ditto -c -k --keepParent "dist/Pocket Book.app" "release/PocketBook-macOS.zip"
  echo "Done: release/PocketBook-macOS.zip"
else
  .venv/bin/python -m PyInstaller --noconfirm --clean --onefile --windowed --name pocket-book \
    --add-data "assets/pocketbook.png:." pocket_book.py
  mkdir -p release/PocketBook-Linux
  cp dist/pocket-book README.md LICENSE release/PocketBook-Linux/
  tar -C release -czf release/PocketBook-Linux.tar.gz PocketBook-Linux
  echo "Done: release/PocketBook-Linux.tar.gz"
fi
