#!/usr/bin/env bash
# 横長動画の一部を縦型(1080x1920)Shortsにする。画面収録が切れないよう、全体を縮小して上下に余白を入れる
# 使い方: scripts/shorts.sh 入力.mp4 字幕.srt 開始 終了 出力.mp4
#   例: scripts/shorts.sh 05_edit/main_cut.mp4 05_edit/main_cut.srt 00:00:00 00:00:40 09_shorts/short1.mp4
# 字幕は元動画の時刻のまま使える（出力側で切り出すため）
set -euo pipefail
in="$1"; srt="$2"; start="$3"; end="$4"; out="$5"
tmp_srt="$(mktemp --suffix=.srt)"; cp "$srt" "$tmp_srt"
style="FontName=Noto Sans CJK JP,FontSize=20,Outline=2,MarginV=60"
ffmpeg -y -i "$in" -ss "$start" -to "$end" \
  -vf "scale=1080:-2,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,subtitles=${tmp_srt}:force_style='${style}'" \
  -c:v libx264 -crf 20 -preset medium -c:a aac -b:a 160k "$out"
rm -f "$tmp_srt"
echo "出力: $out（60秒以内を推奨。TikTok/Reels用もこのファイルから書き出す）"
