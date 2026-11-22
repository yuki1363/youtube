---
name: auto-video
description: ネタ選びから完成動画・部門報告までを自動で作り、完成品レビューで止まる。「自動で作って」「次の動画を自動で」「3本まとめて作って」で使う。本数を指定できる（既定1本）。
---
# 動画を自動で作る（全12部門）

人の関門は「完成品レビュー」と「公開」だけ。途中ではユーザーに質問しない（判断に迷ったら、安全で控えめな方を選び、報告に書く）。
本数の指定があれば、その本数を順番に作る。1本ずつ全工程を終えてから次へ進む。

## 0. 準備
- `scripts/setup_cloud.sh`（道具が入っていなければ入れる）
- 読む：CLAUDE.md、docs/01_strategy.md、docs/02_departments.md、docs/03_format.md、docs/video-ideas.md、plan/ideas-inbox.md、analytics/log.csv、studio/README.md
- **スマホのレビューページ（studio/README.md のURL）を確認する**：Artifact の read で一度読み、ArtifactData で
  - `settings/main` の `voice` と `voiceOptions` → 選ばれた声の `openjtalk` 設定（model・speed・fm など）を plan.json の voice にそのまま入れ、`credit` を説明欄のクレジットに書く
  - `videos` の `status: "redo"` → **新作より先に**その動画を `note` の指示どおりに直す（直したら status を review に戻し、note は残す）
  - `status: "posted"` → analytics/log.csv に行がなければ追加（公開日＝postedAt、数値は空欄）
- 次の番号 = videos/ の最大番号＋1

## 1. ① SNS収集部門 → ⑪ 統括がネタを決める
- docs/video-ideas.md の未着手（videos/ にない）★から、Web検索で関心の高さを確かめて1つ選ぶ
- 選ばない条件：出典が見つからない／危険な分解が必要／勤務先が特定される
- `bash scripts/new_video.sh <番号> <英小文字の短い名前>`

## 2. ② 情報調達部門 → 01_research.md
- 出典は公的機関・メーカー・特許・論文を優先。個人ブログだけを根拠にしない。URLと取得日を書く
- 出典が2件そろわなければ、そのネタはやめて次の★へ（報告に理由を書く）

## 3. ③ 作成部門 → ④ 内容精度部門 → 02_script.md
- templates/script.md の6項目。約220字・話し言葉。フック型は直前の動画と変える
- 内容精度：文ごとに ○／△／× と出典。×は削除、△は言い換え。数字は出典があるものだけ
- 本文に [要確認] [要実測] を残さない（残るなら、その文を削る）
- status は draft のまま（完成品レビューでユーザーが approved にする）

## 4. ⑫ 図解画像生成部門 → 07_figures/src/*.html
- `scripts/figures/kit.js` の部品で4〜6枚描く（見本：videos/001_coin-check/07_figures/src/）
- 画面の決まり：タイトルは上（y 120〜420）、絵は y 420〜1440、**y 1480より下は空ける**（字幕とShortsのボタン）
- ナビゲーター「ビリ太」（mascot）は1本に2〜3枚まで。表情は q／wow／point
- 足りない部品は kit.js に足す（実在のロゴ・キャラクターに似せない）
- 実測していないグラフ・波形には「イメージ」と書く

## 5. ⑦ ナレーション・⑤ 編集・⑥ BGM部門 → 05_edit/plan.json
- 形は templates/plan.json。1文ごとに figure（どの図か）と focus（注目させる座標）を決める
- 同じ図は続けて2文まで（画面を2〜3秒ごとに変えるため）
- 読み間違えそうな語は say に読みを書く（例：返却口 → 返却ぐち）

## 6. 組み立てと自動チェック
- `scripts/build_video.sh videos/NNN_xxx`
- 失敗したら readings.txt／qa.json の問題を直して、もう一度。直せない問題は報告に書く
- **05_edit/contact.png を必ず見る**（図解部門の合格基準①〜⑤）。重なり・はみ出し・読めない文字があれば直して作り直す

## 7. ⑧ パッケージ・⑨ 法務 → 07_meta.json・checklist.md
- タイトル3案（30字以内）、説明欄に出典とクレジット（音声合成・BGM）
- checklist.md はAIが確認できた項目だけチェック。人の項目（音声確認・副業規定・AI開示）は空けておく

## 8. ⑪ 統括 → report.md
- videos/001_coin-check/report.md と同じ形で、部門ごとに「確認したこと／見つけた問題→対応／判定」
- 最後に「人に見てほしい所」を3つ以内で書く

## 9. スマホのレビューページに載せる
- poster：`ffmpeg -i 07_figures/fig1*.png -vf scale=540:-1 06_thumb/poster.jpg`
- Artifact（publish, url=レビューページ, asset:true, file_paths=[final.mp4, poster.jpg]）で上げ、返った url を使う
- ArtifactData で `videos/<番号>` を set（形は studio/README.md）。status は "review"
- 作り直した動画は update（新しい videoUrl・duration・lufs・autoCheck・updatedAt、status:"review"）。古い動画アセットは消してよい

## 10. 止まる（完成品レビュー）
- ユーザーはスマホのレビューページで、見て聞いて「承認」か「作り直し（指示つき）」を押す
- 承認された台本は次の実行で 02_script.md を approved にする
- 公開はユーザーが YouTube アプリで行う。AIは公開しない
- 変更はブランチ claude/festive-gauss-cbxiq3 にコミットしてpushする
- 最後に、作った本数・タイトル・人に見てほしい所を短くまとめる（定期実行ではこれが通知になる）
