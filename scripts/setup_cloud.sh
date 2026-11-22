#!/usr/bin/env bash
# クラウドの作業環境（定期実行の新しいセッション）で、動画制作に要る道具を入れる。何度実行してもよい
set -euo pipefail
need=""
for p in open-jtalk open-jtalk-mecab-naist-jdic hts-voice-nitech-jp-atr503-m001 fonts-noto-cjk ffmpeg; do
  dpkg -s "$p" >/dev/null 2>&1 || need="$need $p"
done
if [ -n "$need" ]; then
  (apt-get install -y -q $need >/dev/null 2>&1) || (apt-get update -q >/dev/null 2>&1 && apt-get install -y -q $need >/dev/null)
fi
python3 -c "import PIL, numpy" 2>/dev/null || pip install -q pillow numpy
node -e "require('playwright')" 2>/dev/null || { echo "playwright が見つかりません"; exit 1; }
echo "準備完了"
