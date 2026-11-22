#!/usr/bin/env bash
# 声の整音 → 無音カット → 字幕生成
# 使い方: scripts/edit.sh videos/024_report-ai/04_raw/main.mp4
#   整音を飛ばす: NO_CLEAN=1 scripts/edit.sh ...（整音の設定は config/voice.json）
set -euo pipefail
in="$1"
here="$(dirname "$0")"
vdir="$(dirname "$(dirname "$in")")"
base="$(basename "${in%.*}")"
mkdir -p "$vdir/05_edit"
src="$in"
if [ "${NO_CLEAN:-0}" != "1" ]; then
  src="$vdir/05_edit/${base}_clean.mp4"
  python3 "$here/voice_clean.py" "$in" "$src"
fi
out="$vdir/05_edit/${base}_cut.mp4"
# 無音部分を詰める（前後0.2秒は残す）。詰めすぎなら margin を増やす
auto-editor "$src" --margin 0.2sec --output "$out"
python3 "$here/subtitles.py" "$out" "$vdir/05_edit/${base}_cut.srt"
echo "出力: $out と .srt（字幕はDaVinci Resolveで確認・修正）"
