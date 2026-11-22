---
name: edit
description: （旧方式）収録素材の無音カットと日本語字幕生成を行う。自動作成（/render）では使わない。収録素材がある場合だけ使う。
---
# 編集（無音カット＋字幕）

前提：02_script.md が `status: approved`、04_raw/ に素材があること。

1. `.venv` を有効化する（なければ scripts/setup.sh の実行を案内）
2. `scripts/edit.sh <04_raw内の動画>` を実行する
3. 生成された .srt を 02_script.md の台本と照合し、明らかな誤変換を直す
   - よく出る誤変換は scripts/subtitles.py の FIXES に追記する
4. 無音カットが詰まりすぎ・残りすぎなら margin の調整を提案する
5. 最終の仕上げ（BGM・画面の強調）はDaVinci Resolveでユーザーが行う旨を伝える
