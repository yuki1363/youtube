#!/usr/bin/env bash
# WSL(Ubuntu)用セットアップ。一度だけ実行する
set -euo pipefail
sudo apt-get update
sudo apt-get install -y ffmpeg fonts-noto-cjk python3-venv
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install auto-editor faster-whisper pillow
echo "完了。以後は 'source .venv/bin/activate' してから使う"
