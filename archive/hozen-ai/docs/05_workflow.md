# 05 制作フロー

| 工程 | 担当 | ツール | 人の時間 |
|---|---|---|---|
| 1 調査 | AI → 人が選ぶ | Claude（Web検索） | 10分 |
| 2 台本 | AI → 人が承認 | /script | 20分 |
| 3 ナレーション | 人（冒頭と要所） | 自分の声。補助にVOICEVOX（規約・クレジット要確認） | 15分 |
| 4 撮影 | 人 | OBS Studio、スマホ | 30分 |
| 5 編集 | AI → 人が仕上げ | auto-editor、faster-whisper、DaVinci Resolve | 20分 |
| 6 サムネ | AI → 人が選ぶ | scripts/thumbnail.py | 5分 |
| 7 投稿 | 人 | YouTube Studio（API自動化は第3段階） | 5分 |
| 8 分析 | AI | Studioから出したCSV → /weekly-review | 10分 |
| 9 Shorts化 | AI | scripts/shorts.sh | 5分 |

## 導入の段階
1. 第1段階（1〜3週）：手作業＋Claudeで作る。工程ごとの時間を記録
2. 第2段階（4週〜）：編集・サムネ・Shortsをスクリプト化
3. 第3段階（12週〜）：YouTube Data API／Analytics APIで投稿と集計を自動化

## 再利用（Shorts・TikTok・Reels）
- 1本の長尺から3本：フックの場面／失敗シーン／まとめ3ポイント
- 9:16、字幕大きめ、冒頭1秒で結論、最後に長尺へ誘導
- TikTok・Reels用は透かしのない元ファイルから書き出す
