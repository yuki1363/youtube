"""図解画像生成部門の共通部品。縦型 1080x1920 の図をPillowで描く。
色は3色まで（背景・主色・強調色）。文字は1枚10字以内を目安にする。
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
BG = (250, 248, 242)      # 背景
INK = (30, 34, 44)        # 線・文字
ACCENT = (230, 70, 40)    # 強調（1枚に1か所まで）
SUB = (40, 110, 190)      # 補助（磁界・矢印など）

FONT_PATHS = {
    "bold": [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/mnt/c/Windows/Fonts/meiryob.ttc",
    ],
    "regular": [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/mnt/c/Windows/Fonts/meiryo.ttc",
    ],
}


def font(size, weight="bold"):
    for path in FONT_PATHS[weight]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    raise SystemExit("日本語フォントが見つかりません（setup.sh で fonts-noto-cjk を入れる）")


def canvas():
    img = Image.new("RGB", (W, H), BG)
    return img, ImageDraw.Draw(img)


def title(d, text, y=180, size=96, fill=INK):
    """上部の大きい見出し。10字を超えたら警告する。"""
    if len(text) > 10:
        print(f"警告: 見出しが10字を超えています: {text}")
    f = font(size)
    w = d.textbbox((0, 0), text, font=f)[2]
    d.text(((W - w) // 2, y), text, font=f, fill=fill)


def label(d, xy, text, size=56, fill=INK, anchor="mm"):
    d.text(xy, text, font=font(size), fill=fill, anchor=anchor)


def arrow(d, start, end, fill=INK, width=12, head=36):
    """直線の矢印（start→end）。"""
    import math
    d.line([start, end], fill=fill, width=width)
    ang = math.atan2(end[1] - start[1], end[0] - start[0])
    left = (end[0] - head * math.cos(ang - 0.45), end[1] - head * math.sin(ang - 0.45))
    right = (end[0] - head * math.cos(ang + 0.45), end[1] - head * math.sin(ang + 0.45))
    d.polygon([end, left, right], fill=fill)


def coin(d, center, r=90, fill=(205, 170, 90), text=None):
    x, y = center
    d.ellipse([x - r, y - r, x + r, y + r], fill=fill, outline=INK, width=8)
    d.ellipse([x - r + 18, y - r + 18, x + r - 18, y + r - 18], outline=INK, width=4)
    if text:
        label(d, center, text, size=int(r * 0.7))


def save(img, out_dir, name):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, name)
    img.save(path)
    print("出力:", path)
    return path
