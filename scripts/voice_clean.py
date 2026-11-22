"""自分の声を整える（低音カット → ノイズ除去 → 歯擦音の抑制 → コンプ → ラウドネス統一）。
設定は config/voice.json の own_voice。値は聞き比べて調整し、決めた値を残す。

使い方:
  python3 scripts/voice_clean.py 入力 出力              # 音声(.wav等)でも動画(.mp4)でも可
  python3 scripts/voice_clean.py 入力 --measure         # ラウドネスを測るだけ（公開前チェック用）
  python3 scripts/voice_clean.py 入力 出力 --preview 30 # 先頭30秒だけ処理して聞き比べる

動画を渡すと映像はそのままコピーし、音声だけ差し替える。
"""
import argparse, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEO_EXT = {".mp4", ".mov", ".mkv"}


def load_cfg():
    with open(os.path.join(ROOT, "config", "voice.json"), encoding="utf-8") as f:
        return json.load(f)["own_voice"]


def measure(path, pre_filters="", c=None, extra_in=()):
    """loudnorm の1パス目。測定値(dict)を返す"""
    c = c or load_cfg()
    ln = f"loudnorm=I={c['target_lufs']}:TP={c['true_peak_db']}:LRA={c['lra']}:print_format=json"
    af = f"{pre_filters},{ln}" if pre_filters else ln
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", *extra_in, "-i", path,
                        "-af", af, "-vn", "-f", "null", "-"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(r.stderr[-2000:])
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S)
    if not m:
        sys.exit("ラウドネスの測定結果を読めませんでした")
    return json.loads(m.group(0))


def chain(c):
    comp = c["compressor"]
    parts = [f"highpass=f={c['highpass_hz']}",
             f"afftdn=nf={c['denoise_nf_db']}"]
    if c.get("deesser"):
        parts.append(f"deesser=i={c['deesser']}")
    parts.append(f"acompressor=threshold={comp['threshold_db']}dB:ratio={comp['ratio']}"
                 f":attack={comp['attack_ms']}:release={comp['release_ms']}")
    return ",".join(parts)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("input")
    p.add_argument("output", nargs="?")
    p.add_argument("--measure", action="store_true")
    p.add_argument("--preview", type=float, help="先頭N秒だけ処理")
    a = p.parse_args()
    c = load_cfg()

    if a.measure:
        m = measure(a.input, c=c)
        print(f"ラウドネス {m['input_i']} LUFS / ピーク {m['input_tp']} dBTP / LRA {m['input_lra']}")
        print(f"目安 {c['target_lufs']} LUFS前後、ピーク {c['true_peak_db']} dBTP以下")
        return
    if not a.output:
        p.error("出力ファイルを指定してください")

    trim = ["-t", str(a.preview)] if a.preview else []
    pre = chain(c)
    m = measure(a.input, pre, c, extra_in=trim)  # 1パス目：処理後の音を測る
    ln = (f"loudnorm=I={c['target_lufs']}:TP={c['true_peak_db']}:LRA={c['lra']}"
          f":measured_I={m['input_i']}:measured_TP={m['input_tp']}"
          f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}"
          f":offset={m['target_offset']}:linear=true")
    af = f"{pre},{ln},aresample=48000"
    is_video = os.path.splitext(a.input)[1].lower() in VIDEO_EXT
    os.makedirs(os.path.dirname(os.path.abspath(a.output)), exist_ok=True)
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *trim, "-i", a.input, "-af", af]
    if is_video:
        cmd += ["-c:v", "copy", "-c:a", "aac", "-b:a", "192k"]
    cmd.append(a.output)
    subprocess.run(cmd, check=True)
    after = measure(a.output, c=c)
    print(f"出力: {a.output}")
    print(f"音量調整前 {m['input_i']} LUFS → 音量調整後 {after['input_i']} LUFS / ピーク {after['input_tp']} dBTP")


if __name__ == "__main__":
    main()
