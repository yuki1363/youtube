"""VOICEVOX で補助音声を作る（自分の声の補助。主役にしない）。
VOICEVOX（エディタかエンジン）を起動しておくこと。設定は config/voice.json の voicevox。

台本の書き方: 02_script.md で補助音声にしたい行の先頭に [VV] を付ける
  [VV] 「確認済みの事実と推定を分けて書いて」
  [3:30] [VV] 「ここまで約[要実測]分です」   ← [要実測] が残っている行は止める

使い方:
  python3 scripts/voicevox_tts.py videos/024_x            # [VV]行を 03_audio/vv_01.wav… に書き出す
  python3 scripts/voicevox_tts.py videos/024_x --dry-run  # 読み替え後の文と割合だけ確認（エンジン不要）
  python3 scripts/voicevox_tts.py --list-speakers         # 話者IDの一覧
  python3 scripts/voicevox_tts.py --try "PLCのERRランプを見ます" --speed 1.0,1.1,1.2
      → 聞き比べ用に条件違いを scratch_voice/ に書き出す（--speaker 3,2 のように話者も並べられる）
"""
import argparse, json, os, re, subprocess, sys, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VV_LINE = re.compile(r"^(?:\s*\[(\d+:\d{2})\])?.*?\[VV\]\s*(.+)$")
QUOTE = re.compile(r"「([^」]*)」")


def load_cfg():
    with open(os.path.join(ROOT, "config", "voice.json"), encoding="utf-8") as f:
        cfg = json.load(f)
    return cfg["voicevox"], cfg["own_voice"]


def apply_readings(text, readings):
    for k in sorted(readings, key=len, reverse=True):  # 長い語から置換（GX Works2 を先に）
        text = text.replace(k, readings[k])
    return text


def strip_quotes(s):
    q = QUOTE.findall(s)
    return "".join(q) if q else s.strip()


def extract(script_path):
    with open(script_path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    # 割合は「9. 完全台本」以降のセリフで数える（見出しがなければ全体）
    start = next((i for i, l in enumerate(lines) if re.match(r"#\s*9[.．]", l)), 0)
    body = lines[start:]
    total = sum(len(t) for l in body for t in QUOTE.findall(l))
    items = []
    for l in lines:
        m = VV_LINE.match(l)
        if m:
            items.append({"time": m.group(1) or "", "text": strip_quotes(m.group(2))})
    vv = sum(len(i["text"]) for i in items)
    return items, vv, total


def api(base, path, params=None, body=None):
    url = f"{base}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = json.dumps(body).encode() if body is not None else (b"" if path != "/speakers" else None)
    req = urllib.request.Request(url, data=data, method="GET" if data is None else "POST",
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read()
    except OSError as e:
        sys.exit(f"VOICEVOXに接続できません（{base}）。VOICEVOXを起動してください: {e}")


def synth(c, text, out, speaker=None, speed=None):
    spk = c["speaker"] if speaker is None else speaker
    q = json.loads(api(c["engine_url"], "/audio_query", {"text": text, "speaker": spk}))
    q.update({
        "speedScale": c["speed"] if speed is None else speed,
        "pitchScale": c["pitch"],
        "intonationScale": c["intonation"],
        "volumeScale": c["volume"],
        "prePhonemeLength": c["pre_silence_sec"],
        "postPhonemeLength": c["post_silence_sec"],
        "outputSamplingRate": 48000,
        "outputStereo": False,
    })
    wav = api(c["engine_url"], "/synthesis", {"speaker": spk}, q)
    with open(out, "wb") as f:
        f.write(wav)


def normalize(path, own):
    """自分の声と同じラウドネスにそろえる（短い音声なので1パス）"""
    tmp = path + ".tmp.wav"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", path,
                    "-af", f"loudnorm=I={own['target_lufs']}:TP={own['true_peak_db']}:LRA={own['lra']},aresample=48000",
                    tmp], check=True)
    os.replace(tmp, path)


def floats(s, cast=float):
    return [cast(x) for x in s.split(",")] if s else [None]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("video_dir", nargs="?")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--list-speakers", action="store_true")
    p.add_argument("--try", dest="try_text")
    p.add_argument("--speed", help="例 1.0,1.1,1.2")
    p.add_argument("--speaker", help="例 3,2")
    a = p.parse_args()
    c, own = load_cfg()

    if a.list_speakers:
        for s in json.loads(api(c["engine_url"], "/speakers")):
            for st in s["styles"]:
                print(f"{st['id']:>4}  {s['name']}（{st['name']}）")
        return

    if a.try_text:
        out_dir = os.path.join(ROOT, "scratch_voice")
        os.makedirs(out_dir, exist_ok=True)
        text = apply_readings(a.try_text, c["readings"])
        print("読み替え後:", text)
        for spk in floats(a.speaker, int):
            for sp in floats(a.speed):
                name = f"try_spk{spk if spk is not None else c['speaker']}_speed{sp if sp is not None else c['speed']}.wav"
                out = os.path.join(out_dir, name)
                synth(c, text, out, spk, sp)
                normalize(out, own)
                print("出力:", out)
        print("気に入った値を config/voice.json に書き戻す")
        return

    if not a.video_dir:
        p.error("動画フォルダを指定してください（例 videos/024_report-ai）")
    script = os.path.join(a.video_dir, "02_script.md")
    with open(script, encoding="utf-8") as f:
        if not re.search(r"^status:\s*approved", f.read(), re.M) and not a.dry_run:
            sys.exit("台本が approved ではありません。承認後に実行します（--dry-run なら確認だけできる）")
    items, vv, total = extract(script)
    if not items:
        sys.exit("[VV] の行がありません")
    share = vv / total if total else 0
    print(f"補助音声の割合: {share:.0%}（{vv}/{total}字、上限の目安 {c['max_share']:.0%}）")
    if share > c["max_share"]:
        print("警告: 補助音声が多すぎます。自分の声の部分を増やす（審査の『不誠実なコンテンツ』対策）")
    bad = [i for i in items if "[要実測]" in i["text"]]
    if bad:
        for i in bad:
            print("  [要実測] が残っている:", i["text"])
        if not a.dry_run:
            sys.exit("実測値に差し替えてから実行してください")

    out_dir = os.path.join(a.video_dir, "03_audio")
    os.makedirs(out_dir, exist_ok=True)
    rows = ["| ファイル | 台本の時刻 | 読ませた文 |", "|---|---|---|"]
    for n, it in enumerate(items, 1):
        text = apply_readings(it["text"], c["readings"])
        name = f"vv_{n:02}.wav"
        rows.append(f"| {name} | {it['time']} | {text} |")
        if a.dry_run:
            print(f"{name} [{it['time']}] {text}")
            continue
        synth(c, text, os.path.join(out_dir, name))
        normalize(os.path.join(out_dir, name), own)
        print("出力:", os.path.join(out_dir, name))
    if not a.dry_run:
        with open(os.path.join(out_dir, "vv_list.md"), "w", encoding="utf-8") as f:
            f.write(f"# 補助音声一覧（クレジット: {c['credit']}）\n\n" + "\n".join(rows) + "\n")
        print(f"一覧: {out_dir}/vv_list.md")
        print(f"概要欄にクレジット「{c['credit']}」を入れる（07_meta.json の voicevox_credit）")


if __name__ == "__main__":
    main()
