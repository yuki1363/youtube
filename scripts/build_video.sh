#!/usr/bin/env bash
# 1本を最後まで組み立てる：図解 → 声・字幕・BGM → 自動チェック
# 使い方: scripts/build_video.sh videos/001_coin-check
set -euo pipefail
v="${1%/}"
cd "$(dirname "$0")/.."
echo "== 図解画像生成部門"
rm -f "$v"/07_figures/*.png
node scripts/figures/render_html.js "$v/07_figures" "$v"/07_figures/src/*.html
echo "== ナレーション・編集・BGM部門"
rm -rf "$v/05_edit/work"
python3 scripts/render_short.py "$v/05_edit/plan.json"
echo "== 自動チェック"
python3 scripts/qa.py "$v"
echo "== 完了：$v/05_edit/final.mp4（全場面の一覧は 05_edit/contact.png）"
