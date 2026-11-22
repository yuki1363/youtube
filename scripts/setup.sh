#!/usr/bin/env bash
# WSL(Ubuntu)用セットアップ。一度だけ実行する
set -euo pipefail
sudo apt-get update
sudo apt-get install -y ffmpeg fonts-noto-cjk python3-venv open-jtalk open-jtalk-mecab-naist-jdic hts-voice-nitech-jp-atr503-m001
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install auto-editor faster-whisper pillow numpy
echo "完了。以後は 'source .venv/bin/activate' してから使う"
