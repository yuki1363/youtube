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
FIG_SCALE = 1.0         # HTML版の図は字幕の場所（下部）を空けて描くので縮めない。Pillow版は0.74
SUB_TOP = 1520          # 字幕の上端。下の約330pxはShortsのボタン・タイトルに隠れるため空ける（推測）
SUB_CHARS = 14          # 字幕1行の最大文字数
SLOW_MS = 300           # 1音がこれより長いと「急に遅くなる」不具合とみなす（通常の最大は約185ms：実測）


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


# ---------- ナレーション ----------
def tts_openjtalk(text, path, speed, fm=0.0, alpha=None, jf=None):
    """fm：声の高さ（半音）、alpha：声質（小さいほど軽い声）、jf：抑揚の強さ。可愛い声は plan.json の voice で指定"""
    voice = "/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice"
    dic = "/var/lib/mecab/dic/open-jtalk/naist-jdic"
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(text)
    raw = path + ".raw.wav"
    trace = path + ".trace.txt"
    extra = ["-fm", str(fm)] + (["-a", str(alpha)] if alpha else []) + (["-jf", str(jf)] if jf else [])
    run(["open_jtalk", "-x", dic, "-m", voice, "-r", str(speed), *extra, "-ow", raw, "-ot", trace, f.name])
    run(["ffmpeg", "-y", "-i", raw, "-ar", str(SR), "-ac", "1", path])
    os.remove(raw); os.remove(f.name)
    return reading(trace)


def reading(trace):
    """open_jtalk の出力ラベルから音素列を取り出す（ナレーション部門の読み確認用）。| は息継ぎ"""
    import re
    lab = open(trace, encoding="utf-8", errors="ignore").read().split("[Output label]")[-1]
    lab = lab.split("\n[")[0]                     # 次の見出しまで（同じラベルが2回出るため）
    ph = re.findall(r"\^([a-zA-Z]+)-", lab)
    text = " ".join(ph).replace("sil", "").replace("pau", "|").replace("xx", "").strip()
    # 1音の長さ（ミリ秒）。Open JTalk は長い文の終わりで急に遅くなる不具合があるため検出する
    durs = []
    for row in lab.strip().splitlines():
        r = row.split()
        m = re.search(r"-([a-zA-Z]+)\+", r[2]) if len(r) >= 3 else None
        if m and m.group(1) not in ("sil", "pau"):
            durs.append((int(r[1]) - int(r[0])) / 1e4)
    return text, max(durs), sum(durs) / len(durs)


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
def _kind(ch):
    if "\u3041" <= ch <= "\u309f":
        return "hira"
    if "\u30a0" <= ch <= "\u30ff":
        return "kata"
    if "\u4e00" <= ch <= "\u9fff":
        return "kanji"
    return "other"


def wrap(text, n=SUB_CHARS):
    """1行n文字以内で、言葉の切れ目で改行する（最大2行を想定）。
    切れ目の優先度：「、」の後 ＞ ひらがな→漢字・カタカナに変わる所（助詞の後のことが多い）。同点なら中央に近い所"""
    if len(text) <= n:
        return [text]
    best, best_score = None, -1
    lo, hi = max(1, len(text) - n), min(n, len(text) - 1)
    for k in range(lo, hi + 1):
        a, b = text[k - 1], text[k]
        if b in "、。ーっゃゅょぁぃぅぇぉ":
            continue
        score = 3 if a == "、" else 2 if (_kind(a) == "hira" and _kind(b) in ("kanji", "kata")) else 0
        score -= abs(k - len(text) / 2) / 100
        if score > best_score:
            best, best_score = k, score
    if best is None:
        best = n
    return [text[:best]] + wrap(text[best:], n)


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


def subtitle_png(text, out_path):
    """字幕だけの透明PNG（図の上に重ねる）。戻り値は行数"""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = font(58)
    rows = wrap(text.rstrip("。"))
    lh = 80
    top = SUB_TOP
    box_h = lh * len(rows) + 40
    d.rounded_rectangle([60, top - 20, W - 60, top - 20 + box_h], radius=24, fill=(255, 255, 255, 255), outline=INK, width=4)
    for i, r in enumerate(rows):
        d.text((W // 2, top + lh * i + lh // 2 - 10), r, font=f, fill=INK, anchor="mm")
    img.save(out_path)
    return len(rows)


ZOOM = 0.06             # 1文の間に6%だけ寄る（または引く）。画面が止まって見えないようにする


def line_clip(fig_path, subs, dur, focus, zoom_in, out_path):
    """1文ぶんの映像：図をfocusに向けてゆっくりズームし、字幕を時刻どおりに重ねる"""
    frames = max(1, int(round(dur * FPS)))
    fx, fy = focus
    z = f"1+{ZOOM}*on/{frames}" if zoom_in else f"{1 + ZOOM}-{ZOOM}*on/{frames}"
    # 2倍に拡大してからズームすると、動きがガタつかない
    zp = (f"scale={W*2}:{H*2},zoompan=z='{z}':d={frames}:s={W}x{H}:fps={FPS}"
          f":x='max(0,min(iw-iw/zoom,{fx*2}-iw/zoom/2))':y='max(0,min(ih-ih/zoom,{fy*2}-ih/zoom/2))'")
    inputs = ["-loop", "1", "-t", f"{dur:.3f}", "-i", fig_path]
    chain = f"[0]{zp},format=yuv420p[v0]"
    for j, (png, a, b) in enumerate(subs, 1):
        inputs += ["-i", png]
        chain += f";[v{j-1}][{j}]overlay=0:0:enable='between(t,{a:.3f},{b:.3f})'[v{j}]"
    run(["ffmpeg", "-y", *inputs, "-filter_complex", chain, "-map", f"[v{len(subs)}]",
         "-frames:v", str(frames), "-r", str(FPS), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", out_path])


def srt_time(s):
    ms = int(round(s * 1000))
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"


def main(plan_path):
    plan = json.load(open(plan_path, encoding="utf-8"))
    out_dir = plan["out_dir"]; os.makedirs(out_dir, exist_ok=True)
    work = os.path.join(out_dir, "work"); os.makedirs(work, exist_ok=True)
    vc = plan.get("voice", {})
    speed = vc.get("speed", 1.0)
    vopt = {"fm": vc.get("fm", 0.0), "alpha": vc.get("alpha"), "jf": vc.get("jf")}

    segs, t, readings, problems, clips, wavs = [], 0.0, [], [], [], []
    for i, line in enumerate(plan["lines"]):
        wav = os.path.join(work, f"v{i:02}.wav")
        ph, mx, avg = tts_openjtalk(line.get("say", line["text"]), wav, speed, **vopt)  # say：読み間違い対策の読み方
        flag = ""
        if mx > SLOW_MS:
            flag = f"  ★要修正：1音が{mx:.0f}ms（平均{avg:.0f}ms）。急に遅くなっている。say で読点を足す"
            problems.append(f"{i+1}文目が遅くなる（最大{mx:.0f}ms）")
        readings.append(f"{i+1}. {line['text']}\n   読み: {ph}\n   1音の長さ: 平均{avg:.0f}ms／最大{mx:.0f}ms{flag}\n")
        dur = wav_seconds(wav) + GAP
        pieces = chunks(line["text"])
        voiced = wav_seconds(wav)
        n_chars = sum(len(p) for p in pieces)
        st, subs = 0.0, []
        for k, piece in enumerate(pieces):
            png = os.path.join(work, f"s{i:02}_{k}.png")
            rows = subtitle_png(piece, png)
            if rows > 2:
                problems.append(f"字幕が{rows}行: {piece}")
            d = voiced * len(piece) / n_chars + (GAP if k == len(pieces) - 1 else 0)
            last = k == len(pieces) - 1
            segs.append({"start": t + st, "dur": d, "text": piece, "last": last})
            subs.append((png, st, st + d + (1.0 if last else 0)))   # 最後の字幕は次の文まで出す
            st += d
        is_last_line = i == len(plan["lines"]) - 1
        clip_dur = dur + (0.5 if is_last_line else 0)
        clip = os.path.join(work, f"c{i:02}.mp4")
        focus = line.get("focus", [W // 2, H // 2 - 200])
        line_clip(os.path.join(plan["figures_dir"], line["figure"]), subs, clip_dur, focus, i % 2 == 0, clip)
        clips.append(clip)
        wavs.append(wav)
        t += dur
    total = t + 0.5

    # ナレーション部門の確認表：全文の読み（音素）。読み違いはここで探し、plan.json の say で直す
    with open(os.path.join(out_dir, "readings.txt"), "w", encoding="utf-8") as f:
        f.write("".join(readings))

    # 字幕ファイル（YouTubeにアップロードする用。画面には焼き込み済み）
    with open(os.path.join(out_dir, "final.srt"), "w", encoding="utf-8") as f:
        for i, s in enumerate(segs, 1):
            end = s['start'] + s['dur'] - (GAP if s['last'] else 0)
            f.write(f"{i}\n{srt_time(s['start'])} --> {srt_time(end)}\n{s['text']}\n\n")

    # 映像：文ごとのクリップをつなぐ
    lst = os.path.join(work, "clips.txt")
    with open(lst, "w") as f:
        for c in clips:
            f.write(f"file '{os.path.abspath(c)}'\n")

    # 声：文ごとの音声の後ろに無音を足してつなぐ
    voice = os.path.join(work, "voice.wav")
    inputs, filt = [], ""
    for i, w_ in enumerate(wavs):
        inputs += ["-i", w_]
        filt += f"[{i}]apad=pad_dur={GAP}[a{i}];"
    filt += "".join(f"[a{i}]" for i in range(len(wavs))) + f"concat=n={len(wavs)}:v=0:a=1,apad=pad_dur=0.5[out]"
    run(["ffmpeg", "-y", *inputs, "-filter_complex", filt, "-map", "[out]", "-ar", str(SR), voice])

    # BGM
    bgm_cfg = plan.get("bgm", {"type": "synth", "gain_db": -26})
    bgm = os.path.join(work, "bgm.wav")
    if bgm_cfg["type"] == "synth":
        synth_bgm(total, bgm)
    else:
        run(["ffmpeg", "-y", "-i", bgm_cfg["path"], "-t", f"{total:.2f}", "-ar", str(SR), "-ac", "1", bgm])

    # 声とBGMを混ぜ、2回測って -14 LUFS に合わせる（1回だけだと約1dB足りなかった：実測）
    g = bgm_cfg.get("gain_db", -26)
    mix = os.path.join(work, "mix.wav")
    run(["ffmpeg", "-y", "-i", voice, "-i", bgm, "-filter_complex",
         f"[1]volume={g}dB[b];[0][b]amix=inputs=2:duration=first:normalize=0[a]", "-map", "[a]", mix])
    # 声のピークが大きく、loudnorm だけでは -15 LUFS 止まりだった（実測）。
    # 測った値との差だけ音量を上げ、ピークはリミッターで -1.5dB に抑える
    r = subprocess.run(["ffmpeg", "-i", mix, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    measured = float(r.stderr.split("Integrated loudness:")[-1].split("I:")[1].split("LUFS")[0])
    gain = -14.0 - measured
    ln = f"volume={gain:.2f}dB,alimiter=limit=0.84:level=disabled"
    out = os.path.join(out_dir, "final.mp4")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-i", mix,
         "-filter_complex", f"[1]{ln},aresample={SR}[a]",
         "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", out])
    print(f"出力: {out}（{total:.1f}秒）と final.srt、readings.txt")
    if problems:
        print("見つけた問題:\n- " + "\n- ".join(problems))
        sys.exit(2)
    print("見つけた問題: なし（読み・遅さ・字幕の行数を確認）")


if __name__ == "__main__":
    main(sys.argv[1])
