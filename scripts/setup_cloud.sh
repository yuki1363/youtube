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
# 女性の声「Mei」（名古屋工業大学, CC BY 3.0）。npm の openjtalk パッケージに同梱されているものを使う
if [ ! -f /opt/voices/mei/mei_normal.htsvoice ]; then
  t=$(mktemp -d); (cd "$t" && npm pack openjtalk@0.1.6 --silent >/dev/null && tar xzf openjtalk-0.1.6.tgz)
  mkdir -p /opt/voices && cp -r "$t/package/voice/mei" /opt/voices/ && rm -rf "$t"
fi
python3 -c "import PIL, numpy" 2>/dev/null || pip install -q pillow numpy
node -e "require('playwright')" 2>/dev/null || { echo "playwright が見つかりません"; exit 1; }
echo "準備完了"
