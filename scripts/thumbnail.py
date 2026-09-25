"""サムネイル3案(1280x720)を作る。変える要素は配色だけ（A/Bテストで1要素ずつ比べるため）。
使い方:
  python3 thumbnail.py --text "5分" --sub "故障報告書" \
      --left before.png --right after.png --out videos/024_x/06_thumb
--left/--right は省略可（省略時は文字だけ）。
"""
import argparse, os
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
FONT_CANDIDATES = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/mnt/c/Windows/Fonts/meiryob.ttc",
]
VARIANTS = {
    "A": {"bg": (20, 24, 32), "main": (255, 214, 0), "sub": (255, 255, 255)},
    "B": {"bg": (245, 245, 245), "main": (220, 30, 30), "sub": (20, 20, 20)},
    "C": {"bg": (0, 70, 140), "main": (255, 255, 255), "sub": (255, 214, 0)},
}

def font(size):
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    raise SystemExit("日本語フォントが見つかりません（setup.shでfonts-noto-cjkを入れる）")

def paste_fit(canvas, path, box):
    img = Image.open(path).convert("RGB")
    img.thumbnail((box[2] - box[0], box[3] - box[1]))
    x = box[0] + (box[2] - box[0] - img.width) // 2
    y = box[1] + (box[3] - box[1] - img.height) // 2
    canvas.paste(img, (x, y))

def centered(draw, text, fnt, y, fill):
    w = draw.textbbox((0, 0), text, font=fnt)[2]
    draw.text(((W - w) // 2, y), text, font=fnt, fill=fill,
              stroke_width=6, stroke_fill=(0, 0, 0))

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--text", required=True, help="大きい文字（10字以内推奨）")
    p.add_argument("--sub", default="", help="小さい文字")
    p.add_argument("--left"); p.add_argument("--right")
    p.add_argument("--out", required=True)
    a = p.parse_args()
    if len(a.text) > 10:
        print("警告: 大きい文字が10字を超えています")
    os.makedirs(a.out, exist_ok=True)
    for key, c in VARIANTS.items():
        im = Image.new("RGB", (W, H), c["bg"])
        d = ImageDraw.Draw(im)
        if a.left:
            paste_fit(im, a.left, (30, 150, 600, 690))
        if a.right:
            paste_fit(im, a.right, (680, 150, 1250, 690))
        if a.left and a.right:
            d.polygon([(610, 380), (670, 420), (610, 460)], fill=c["main"])
        if a.sub:
            centered(d, a.sub, font(70), 30, c["sub"])
        size = 220 if (a.left or a.right) else 260
        centered(d, a.text, font(size), H // 2 - size // 2, c["main"])
        path = os.path.join(a.out, f"thumb_{key}.png")
        im.save(path)
        print("作成:", path)

if __name__ == "__main__":
    main()
