"""faster-whisperで日本語字幕(.srt)を作る。
使い方: python3 subtitles.py 入力.mp4 出力.srt [--model small]
初回はモデルをダウンロードする（ネット接続が必要）。
"""
import argparse
from faster_whisper import WhisperModel

# 誤変換しやすい用語の置換表（運用しながら追記する）
FIXES = {
    "ジーエックスワークス": "GX Works",
    "ピーエルシー": "PLC",
    "ラダ図": "ラダー図",
}

def ts(sec: float) -> str:
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--model", default="small")
    a = p.parse_args()
    model = WhisperModel(a.model, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(a.input, language="ja", vad_filter=True)
    with open(a.output, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, 1):
            text = seg.text.strip()
            for k, v in FIXES.items():
                text = text.replace(k, v)
            f.write(f"{i}\n{ts(seg.start)} --> {ts(seg.end)}\n{text}\n\n")
    print("字幕:", a.output)

if __name__ == "__main__":
    main()
