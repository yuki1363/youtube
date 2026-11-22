#!/usr/bin/env bash
# 無音カット＋字幕生成
# 使い方: scripts/edit.sh videos/024_report-ai/04_raw/main.mp4
set -euo pipefail
in="$1"
vdir="$(dirname "$(dirname "$in")")"
base="$(basename "${in%.*}")"
out="$vdir/05_edit/${base}_cut.mp4"
# 無音部分を詰める（前後0.2秒は残す）。詰めすぎなら margin を増やす
auto-editor "$in" --margin 0.2sec --output "$out"
python3 "$(dirname "$0")/subtitles.py" "$out" "$vdir/05_edit/${base}_cut.srt"
echo "出力: $out と .srt（字幕はDaVinci Resolveで確認・修正）"
