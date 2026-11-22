"""完成動画の自動チェック（編集・内容精度・パッケージ部門）。
使い方: python3 scripts/qa.py videos/NNN_xxx
結果: 05_edit/qa.json と 05_edit/contact.png（全場面の縮小一覧。図解部門が目で確認する）
問題があれば終了コード2。
"""
import json, os, re, subprocess, sys
from PIL import Image

vdir = sys.argv[1].rstrip("/")
edit = os.path.join(vdir, "05_edit")
mp4 = os.path.join(edit, "final.mp4")
problems, info = [], {}

def probe(entries):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", entries, "-of", "json", mp4], capture_output=True, text=True)
    return json.loads(r.stdout)

# 映像の形式・長さ
p = probe("format=duration:stream=codec_type,width,height")
dur = float(p["format"]["duration"]); info["秒"] = round(dur, 1)
v = [s for s in p["streams"] if s["codec_type"] == "video"][0]
if (v["width"], v["height"]) != (1080, 1920): problems.append(f"解像度が {v['width']}x{v['height']}")
if dur > 60: problems.append(f"{dur:.1f}秒で60秒を超えている")

# 音量
r = subprocess.run(["ffmpeg", "-i", mp4, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
I = float(r.stderr.split("Integrated loudness:")[-1].split("I:")[1].split("LUFS")[0]); info["LUFS"] = I
if not -15.5 <= I <= -12.5: problems.append(f"音量 {I} LUFS（目安 -14 前後）")

# 読み・遅さ（render_short.py が書いた readings.txt）
rd = open(os.path.join(edit, "readings.txt"), encoding="utf-8").read()
if "★要修正" in rd: problems.append("合成音声が急に遅くなる文がある（readings.txt の★）")

# 台本の未確認・未実測
sc = open(os.path.join(vdir, "02_script.md"), encoding="utf-8").read()
body = sc.split("# 5.")[0]
for tag in ("[要確認]", "[要実測]"):
    if tag in body: problems.append(f"台本の本文に {tag} が残っている")

# パッケージ
meta = json.load(open(os.path.join(vdir, "07_meta.json"), encoding="utf-8"))
if len(meta.get("title", "")) == 0 or len(meta["title"]) > 30: problems.append(f"タイトルが空か30字超（{len(meta.get('title',''))}字）")
if "出典" not in meta.get("description", ""): problems.append("説明欄に出典がない")
if "クレジット" not in meta.get("description", ""): problems.append("説明欄にクレジットがない")

# 全場面の縮小一覧（2秒ごと）
frames, t = [], 0.3
tmp = os.path.join(edit, "work"); os.makedirs(tmp, exist_ok=True)
while t < dur:
    f = os.path.join(tmp, f"qa_{len(frames):02}.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", mp4, "-frames:v", "1", "-vf", "scale=216:-1", f], check=True)
    frames.append(Image.open(f)); t += 2.0
cols = 8
sheet = Image.new("RGB", (226 * cols, 394 * ((len(frames) + cols - 1) // cols)), (90, 90, 90))
for i, im in enumerate(frames):
    sheet.paste(im, ((i % cols) * 226, (i // cols) * 394))
sheet.save(os.path.join(edit, "contact.png"))

json.dump({"info": info, "problems": problems}, open(os.path.join(edit, "qa.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(json.dumps(info, ensure_ascii=False))
if problems:
    print("見つけた問題:\n- " + "\n- ".join(problems)); sys.exit(2)
print("見つけた問題: なし（形式・長さ・音量・読み・台本の未確認・タイトル・出典・クレジット）")
