---
name: shorts
description: 長尺動画から縦型動画を3本切り出す（YouTube Shorts・TikTok 共通）。「Shortsを作って」「TikTokを作って」で使う。
---
# 縦型3本（YouTube Shorts・TikTok 共通。docs/07_sns.md を読む）

1. 05_edit の .srt と 02_script.md から、次の3区間（各60秒以内）を選んで提示する
   - フックの場面／失敗シーン／まとめ3ポイント（02_script.md の 8b を優先）
   - 長尺の「結論だけ」を見せ、手順の続きは長尺に残す
2. ユーザーの確認後、`scripts/shorts.sh <動画> <srt> <開始> <終了> <動画フォルダ>/09_shorts/shortN.mp4` を3回実行
3. 07_meta.json の shorts に作り分けて書く
   - YouTube：youtube_title、related_video
   - TikTok：tiktok_caption、tiktok_hashtags（3〜5個）、tiktok_pinned_comment（「続きは YouTube で『チャンネル名』と検索」）
4. 投稿はユーザーが行う。同じファイルを両方に投稿し、TikTok からダウンロードした動画を YouTube に上げないよう伝える
5. 関連動画（長尺本編）の設定を案内する
