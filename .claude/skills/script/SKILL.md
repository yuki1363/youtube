---
name: script
description: 調査メモと検証メモから台本(02_script.md)を作る。「台本を作って」で使う。承認は必ずユーザーが行う。
---
# 台本を作る

前提：01_research.md が「採用」になっていること。

1. 読む：docs/03_video-format.md、templates/example-script-024.md、対象フォルダの 01_research.md
2. analytics/log.csv で直前の動画の hook_type を確認し、**違う型**を選ぶ
3. 00_memo.md（現場メモ）を読む。なければユーザーに書いてもらうよう求めて止まる（現場メモのない動画は作らない）。メモにない結果は [要実測] とする
   - docs/03_video-format.md の構成の型4つから、直前の動画と違う型を選ぶ
4. 02_script.md の11項目をすべて埋める
   - 完全台本は1分あたり約300字、話し言葉
   - 検証メモにない結果・数値は書かない
   - 危険作業の手順、社名・設備番号は書かない
5. セルフレビュー：タイトルの約束を冒頭30秒で回収しているか／事実と推定が分かれているか／禁止事項に触れていないか
6. 03_scenes.json（シーンごとに narration・visual の種類〔diagram／slide／character／screen〕・図解の指定・強調する文字）を作る。docs/08_auto-production.md に従う
7. `status: draft` のまま止め、ユーザーに確認を依頼する。承認後にユーザーが approved に変える
