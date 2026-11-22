# yt-ops：身近なモノの仕組みチャンネル 運用システム（Claude Code用）

## セットアップ（WSL / Ubuntu）
1. このフォルダを好きな場所に展開し、git init する
2. `bash scripts/setup.sh`（ffmpeg・日本語フォント・auto-editor・faster-whisper・Pillow）
3. `source .venv/bin/activate`
4. フォルダ内で `claude` を起動。CLAUDE.md が自動で読み込まれる

## 1本の流れ
```
/new-video           → ネタ候補3つ → 調査メモ（あなたが採用判定）
/script              → 台本＋内容精度チェック（あなたが approved にする）  ← 関門1
  図解を生成 → 07_figures/
  声を収録（スマホ可）→ 03_audio/ に置く
/edit                → 無音カット＋字幕、図解とBGMを合わせて縦型に
/publish-prep        → メタデータ（出典・BGMクレジット）＋チェック  ← 関門2
  Studioで公開（あなた）
/weekly-review       → 毎週1回
```

## 構成
- CLAUDE.md：前提・ルール・禁止事項
- docs/：戦略・12部門・動画の型・動画案
- archive/hozen-ai/：旧企画（保全×AI）。使わない
- plan/90days.md：90日計画（チェックボックス）
- templates/：調査・台本・メタデータ・チェックリスト・台本例
- scripts/：自動化スクリプト
- .claude/skills/：スラッシュコマンド
- analytics/：動画ごとの指標とA/Bテストの記録

## 注意
- 収益化条件・YouTubeの仕様・VOICEVOXの規約は変わることがある。使う前に公式で確認する
- YouTube API（投稿・分析の自動化）は第12週に実装予定。今は Studio から手動で CSV を出す
- 勤務先の副業規定を第1週に確認する
