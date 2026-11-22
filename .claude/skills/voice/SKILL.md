---
name: voice
description: 自分の声の整音とVOICEVOX補助音声の調整・生成を行う。「ボイス調整」「声を整えて」「補助音声を作って」で使う。
---
# ボイス調整（自分の声＋VOICEVOX補助音声）

原則：主役は自分の声。VOICEVOXは補助（短い読み上げ・引用・掛け合い程度）。
設定はすべて config/voice.json。決めた値はここに書き戻して残す（`_note` に決めた日と理由を一言）。

## A. 自分の声の整音（初回は必ず聞き比べる）
1. 収録素材（04_raw/）か 03_audio/ の声で、先頭30秒だけ試す
   `python3 scripts/voice_clean.py 入力 05_edit/preview.wav --preview 30`
2. ユーザーに元音声と聞き比べてもらい、症状から1つずつ調整する（同時に複数変えない）
   | 症状 | 調整する値 |
   |---|---|
   | 「サー」というノイズが残る | denoise_nf_db を -20 側へ（上げすぎると声が水っぽくなる） |
   | 声がこもる・ボワつく | highpass_hz を 100〜120 へ |
   | サ行が刺さる | deesser を 0.6〜0.8 へ |
   | 声が小さい所と大きい所の差が大きい | compressor.ratio を 4 へ |
   | 声が平板・息苦しい | compressor.ratio を 2 へ、threshold_db を -16 へ |
   | 工場の機械音が残る | ソフトでは限界がある。収録位置・マイクを見直す |
3. 決まったら `/edit` の中で自動適用される（scripts/edit.sh。飛ばすときは NO_CLEAN=1）
4. 公開前に完成動画を測る：`python3 scripts/voice_clean.py 完成.mp4 --measure`

## B. VOICEVOX補助音声
前提：VOICEVOXを起動していること（既定 http://127.0.0.1:50021）。
WSLからWindows側のVOICEVOXに繋がらない場合は engine_url をWindowsのIPにする、
またはWSLのネットワークをミラーモードにする（環境により異なる：不確か）。

1. 話者を選ぶ：`python3 scripts/voicevox_tts.py --list-speakers`
2. 聞き比べ：台本の実際のセリフ1文で、速度か話者を並べて作る
   `python3 scripts/voicevox_tts.py --try "GX Works2でERRを確認します" --speed 1.0,1.1,1.2`
   → scratch_voice/ に出る。選んだ値を config/voice.json の voicevox に書き戻す
3. 読み間違い（型番・略語）は voicevox.readings に追記する
4. 台本で補助音声にする行に `[VV]` を付ける（承認前でも `--dry-run` で確認できる）
   `python3 scripts/voicevox_tts.py videos/NNN_x --dry-run`
5. 台本が approved になったら生成：`python3 scripts/voicevox_tts.py videos/NNN_x`
   → 03_audio/vv_NN.wav と vv_list.md（台本の時刻つき）。DaVinci Resolveで配置はユーザー
6. 07_meta.json の voicevox_credit にクレジットを入れる

## 止まる条件
- 補助音声の割合が上限（max_share、初期30%）を超えたら、自分の声へ戻す案を出す
- [VV]行に [要実測] が残っていたら生成しない
- クレジット表記・商用利用の可否はキャラクターごとに規約が違う。使う話者の規約を公式で確認したかユーザーに聞く（未確認なら不確かと伝える）
