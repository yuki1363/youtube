"""縦型Shortsを1本組み立てる（ナレーション部門・編集部門・BGM部門）。
使い方: python3 scripts/render_short.py videos/001_coin-check/05_edit/plan.json

plan.json の形:
{
  "figures_dir": "videos/001_coin-check/07_figures",
  "out_dir": "videos/001_coin-check/05_edit",
  "voice": {"engine": "openjtalk", "speed": 1.1},
  "bgm": {"type": "synth", "gain_db": -26},
  "lines": [{"text": "字幕の文", "say": "読み方（省略可）", "figure": "fig1_question.png"}, ...]
}
- 合成音声は1文ずつ作るので、字幕の時刻は音声の長さから正確に決まる
- BGMはnumpyで自作した和音（権利の問題が出ない）。"type": "file" で外部の曲も使える
"""
import json, os, subprocess, sys, tempfile, wave
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "figures"))
from common import W, H, BG, INK, font  # noqa: E402

FPS = 30
GAP = 0.25              # 文と文の間（秒）
SR = 48000
FIG_SCALE = 0.74        # 図を縮めて、下に字幕の場所を空ける
SUB_TOP = 1470          # 字幕の上端。下の約330pxはShortsのボタン・タイトルに隠れるため空ける（推測）
SUB_CHARS = 14          # 字幕1行の最大文字数


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


# ---------- ナレーション ----------
def tts_openjtalk(text, path, speed):
    voice = "/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice"
    dic = "/var/lib/mecab/dic/open-jtalk/naist-jdic"
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(text)
    raw = path + ".raw.wav"
    run(["open_jtalk", "-x", dic, "-m", voice, "-r", str(speed), "-ow", raw, f.name])
    run(["ffmpeg", "-y", "-i", raw, "-ar", str(SR), "-ac", "1", path])
    os.remove(raw); os.remove(f.name)


def wav_seconds(path):
    with wave.open(path) as w:
        return w.getnframes() / w.getframerate()


# ---------- BGM ----------
def synth_bgm(seconds, path):
    """やわらかい和音の繰り返し（C→Am→F→G、1和音2秒）。自作なので権利表記は不要。"""
    t = np.arange(int(seconds * SR)) / SR
    chords = [[261.6, 329.6, 392.0], [220.0, 261.6, 329.6], [174.6, 220.0, 261.6], [196.0, 246.9, 293.7]]
    out = np.zeros_like(t)
    seg = 2.0
    for i in range(int(np.ceil(seconds / seg))):
        a, b = int(i * seg * SR), min(int((i + 1) * seg * SR), len(t))
        tt = t[a:b] - i * seg
        env = np.minimum(tt / 0.4, 1) * np.minimum((seg - tt) / 0.4, 1)   # 0.4秒で出入り
        for f in chords[i % 4]:
            out[a:b] += env * (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2 * f * tt))
    out = out / np.max(np.abs(out)) * 0.5
    fade = int(1.0 * SR)
    out[-fade:] *= np.linspace(1, 0, fade)
    with wave.open(path, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((out * 32767).astype(np.int16).tobytes())


# ---------- 画面 ----------
def wrap(text, n=SUB_CHARS):
    """句読点の後ろで優先して改行し、1行n文字以内にする。"""
    lines, cur = [], ""
    for ch in text:
        cur += ch
        if len(cur) >= n or (ch in "、。" and len(cur) >= n * 0.6):
            lines.append(cur); cur = ""
    if cur:
        lines.append(cur)
    # 句読点だけが次の行の先頭に来ないようにする
    for i in range(1, len(lines)):
        while lines[i] and lines[i][0] in "、。":
            lines[i - 1] += lines[i][0]; lines[i] = lines[i][1:]
    return [l for l in lines if l]


def chunks(text, max_chars=SUB_CHARS * 2):
    """長い文を「、」で区切り、1つの字幕が2行以内に収まるかたまりにする。"""
    parts, cur = [], ""
    for p in text.replace("、", "、|").split("|"):
        if cur and len(wrap((cur + p).rstrip("。"))) > 2:
            parts.append(cur); cur = p
        else:
            cur += p
    if cur:
        parts.append(cur)
    return parts


def frame(fig_path, text, out_path):
    img = Image.new("RGB", (W, H), BG)
    fig = Image.open(fig_path).convert("RGB")
    fw, fh = int(W * FIG_SCALE), int(H * FIG_SCALE)
    img.paste(fig.resize((fw, fh), Image.LANCZOS), ((W - fw) // 2, 20))
    d = ImageDraw.Draw(img)
    f = font(58)
    rows = wrap(text.rstrip("。"))
    lh = 80
    top = SUB_TOP
    box_h = lh * len(rows) + 40
    d.rounded_rectangle([60, top - 20, W - 60, top - 20 + box_h], radius=24, fill=(255, 255, 255), outline=INK, width=4)
    for i, r in enumerate(rows):
        d.text((W // 2, top + lh * i + lh // 2 - 10), r, font=f, fill=INK, anchor="mm")
    img.save(out_path)
    return len(rows)


def srt_time(s):
    ms = int(round(s * 1000))
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"


def main(plan_path):
    plan = json.load(open(plan_path, encoding="utf-8"))
    out_dir = plan["out_dir"]; os.makedirs(out_dir, exist_ok=True)
    work = os.path.join(out_dir, "work"); os.makedirs(work, exist_ok=True)
    speed = plan.get("voice", {}).get("speed", 1.0)

    segs, t = [], 0.0
    for i, line in enumerate(plan["lines"]):
        wav = os.path.join(work, f"v{i:02}.wav")
        tts_openjtalk(line.get("say", line["text"]), wav, speed)  # say：読み間違い対策の読み方
        dur = wav_seconds(wav) + GAP
        pieces = chunks(line["text"])
        voiced = wav_seconds(wav)
        n_chars = sum(len(p) for p in pieces)
        st = t
        for k, piece in enumerate(pieces):
            png = os.path.join(work, f"f{i:02}_{k}.png")
            rows = frame(os.path.join(plan["figures_dir"], line["figure"]), piece, png)
            if rows > 2:
                print(f"警告: 字幕が{rows}行になりました: {piece}")
            d = voiced * len(piece) / n_chars + (GAP if k == len(pieces) - 1 else 0)
            segs.append({"png": png, "start": st, "dur": d, "text": piece,
                         "wav": wav if k == 0 else None, "last": k == len(pieces) - 1})
            st += d
        t += dur
    total = t + 0.5

    # 字幕ファイル（YouTubeにアップロードする用。画面には焼き込み済み）
    with open(os.path.join(out_dir, "final.srt"), "w", encoding="utf-8") as f:
        for i, s in enumerate(segs, 1):
            end = s['start'] + s['dur'] - (GAP if s['last'] else 0)
            f.write(f"{i}\n{srt_time(s['start'])} --> {srt_time(end)}\n{s['text']}\n\n")

    # 映像：画像を時間どおりに並べる
    lst = os.path.join(work, "frames.txt")
    with open(lst, "w") as f:
        for s in segs:
            f.write(f"file '{os.path.abspath(s['png'])}'\nduration {s['dur']:.3f}\n")
        f.write(f"file '{os.path.abspath(segs[-1]['png'])}'\nduration 0.5\n")
        f.write(f"file '{os.path.abspath(segs[-1]['png'])}'\n")

    # 声：文ごとの音声の後ろに無音を足してつなぐ
    voice = os.path.join(work, "voice.wav")
    inputs, filt = [], ""
    voiced_segs = [s for s in segs if s["wav"]]
    for i, s in enumerate(voiced_segs):
        inputs += ["-i", s["wav"]]
        filt += f"[{i}]apad=pad_dur={GAP}[a{i}];"
    filt += "".join(f"[a{i}]" for i in range(len(voiced_segs))) + f"concat=n={len(voiced_segs)}:v=0:a=1,apad=pad_dur=0.5[out]"
    run(["ffmpeg", "-y", *inputs, "-filter_complex", filt, "-map", "[out]", "-ar", str(SR), voice])

    # BGM
    bgm_cfg = plan.get("bgm", {"type": "synth", "gain_db": -26})
    bgm = os.path.join(work, "bgm.wav")
    if bgm_cfg["type"] == "synth":
        synth_bgm(total, bgm)
    else:
        run(["ffmpeg", "-y", "-i", bgm_cfg["path"], "-t", f"{total:.2f}", "-ar", str(SR), "-ac", "1", bgm])

    out = os.path.join(out_dir, "final.mp4")
    g = bgm_cfg.get("gain_db", -26)
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-i", voice, "-i", bgm,
         "-filter_complex",
         f"[2]volume={g}dB[b];[1][b]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-13:TP=-1.5:LRA=11[a]",
         "-map", "0:v", "-map", "[a]", "-r", str(FPS), "-c:v", "libx264", "-pix_fmt", "yuv420p",
         "-crf", "20", "-c:a", "aac", "-b:a", "160k", "-shortest", out])
    print(f"出力: {out}（{total:.1f}秒）と final.srt")


if __name__ == "__main__":
    main(sys.argv[1])
