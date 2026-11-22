# ビリ太スタジオ（スマホのレビューページ）
URL: https://claude.ai/artifact/3qVLrULds3QcbP9D7129kn
ページの元ファイル: studio/review.html（変えたら同じURLに publish）

## データ（ArtifactData）
### videos/<番号>（例 videos/001）
| 項目 | 内容 |
|---|---|
| slug | 英小文字の短い名前 |
| title / titleAlts / description | 07_meta.json から |
| videoUrl / videoAssetId / posterUrl | アップロードした動画・画像（"/_blob/…"） |
| duration / lufs / autoCheck | qa.json から（autoCheck は「自動チェック：問題なし」など） |
| summary | 1〜2文の内容紹介 |
| humanChecks | 人が確認すること（配列） |
| status | review（確認待ち）→ approved（投稿待ち）→ posted（投稿済み）／ redo（作り直し） |
| note | 作り直しの指示（ユーザーが書く） |
| createdAt / updatedAt / postedAt | 日付 |

### settings/main
| 項目 | 内容 |
|---|---|
| voice | 選ばれた声のキー |
| voiceOptions | [{key, label, url, openjtalk:{speed, fm, alpha, jf}}] |
| schedule | 定期実行の予定（表示用） |
