#!/usr/bin/env bash
# 使い方: scripts/new_video.sh 024 report-ai
set -euo pipefail
num=$(printf "%03d" "$((10#$1))"); name="$2"
dir="videos/${num}_${name}"
[ -e "$dir" ] && { echo "既に存在: $dir"; exit 1; }
mkdir -p "$dir"/{03_audio,04_raw,05_edit,06_thumb,08_analytics,09_shorts}
sed "s/{番号}/${num}/" templates/research.md > "$dir/01_research.md"
sed "s/{番号}/${num}/" templates/script.md   > "$dir/02_script.md"
sed "s/{番号}/${num}/" templates/checklist.md > "$dir/checklist.md"
sed "s/\"video\": \"\"/\"video\": \"${num}\"/" templates/meta.json > "$dir/07_meta.json"
echo "作成: $dir"
