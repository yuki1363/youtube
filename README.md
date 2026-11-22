# yt-ops：製造業DX×AI YouTube運用システム（Claude Code用）

## セットアップ（WSL / Ubuntu）
1. このフォルダを好きな場所に展開し、git init する
2. `bash scripts/setup.sh`（ffmpeg・日本語フォント・auto-editor・faster-whisper・Pillow）
3. `source .venv/bin/activate`
4. フォルダ内で `claude` を起動。CLAUDE.md が自動で読み込まれる

## 1本の流れ
```
/new-video 24        → 調査メモ（あなたが採用判定）
/script              → 台本（あなたが approved にする）  ← 関門1
  収録（OBS・スマホ）→ 04_raw/ に置く
/edit                → 無音カット＋字幕
  DaVinci Resolveで仕上げ
/thumbnail           → 3案
/shorts              → 縦型3本（YouTube Shorts・TikTok 共通）
/publish-prep        → メタデータ＋チェック  ← 関門2
  YouTube Studio と TikTok で公開（あなた）
/weekly-review       → 毎週1回
```

## 構成
- CLAUDE.md：前提・ルール・禁止事項
- docs/：設計（全体・ニッチ・動画の型・指標・制作フロー・収益化・SNS）と動画案115本
- plan/90days.md：90日計画（チェックボックス）
- templates/：調査・台本・メタデータ・チェックリスト・台本例
- scripts/：自動化スクリプト
- .claude/skills/：スラッシュコマンド
- analytics/：動画ごとの指標とA/Bテストの記録

## 注意
- 収益化条件・YouTubeの仕様・VOICEVOXの規約は変わることがある。使う前に公式で確認する
- YouTube API（投稿・分析の自動化）は第12週に実装予定。今は Studio から手動で CSV を出す
- 勤務先の副業規定と撮影可否を第1週に確認する
