"""動画001「自販機は偽物の硬貨をどうやって見破っている？」の図解3枚。
使い方: python3 scripts/figures/v001_coin_check.py videos/001_coin-check/07_figures
台本の内容精度判定（02_script.md 5章）に合わせ、出典で確認できた範囲だけを描く。
- 描く：大きさ・厚みの検出／コイルの磁界で材質を見る（電子式）／返却口への振り分け
- 描かない：判定にかかる時間（出典なしで削除済み）、特定メーカーの構造
"""
import sys
from common import (W, H, INK, ACCENT, SUB, canvas, title, label, arrow, coin, save)

out = sys.argv[1] if len(sys.argv) > 1 else "07_figures"


def fig1_question():
    """1枚目：疑問。硬貨が返却口から戻ってくる。"""
    img, d = canvas()
    title(d, "なぜ戻ってくる？", y=220, size=110, fill=ACCENT)
    # 自販機の外形（ロゴ・メーカー要素なし）
    d.rounded_rectangle([240, 520, 840, 1640], radius=30, outline=INK, width=12)
    d.rectangle([300, 600, 780, 1000], outline=INK, width=8)  # 商品見本の窓
    for i in range(3):
        x = 340 + i * 150
        d.rounded_rectangle([x, 660, x + 110, 940], radius=20, outline=INK, width=6)
    d.rectangle([640, 1080, 760, 1110], fill=INK)              # 投入口
    d.rounded_rectangle([600, 1320, 800, 1440], radius=16, outline=INK, width=8)  # 返却口
    label(d, (700, 1480), "返却口", size=48)
    coin(d, (700, 1380), r=46)
    arrow(d, (930, 1060), (780, 1300), fill=ACCENT, width=14)
    label(d, (540, 1760), "入れたのに…", size=72)
    return save(img, out, "fig1_question.png")


def fig2_size():
    """2枚目：大きさと厚みを測る。"""
    img, d = canvas()
    title(d, "まず大きさ・厚み", y=220)
    # 坂道（レール）：y = 760 + (x-120)*500/840
    d.line([(120, 760), (960, 1260)], fill=INK, width=16)
    cx, r = 520, 110
    rail_y = 760 + (cx - 120) * 500 / 840
    cy = int(rail_y - r - 10)          # レールの上に乗せる
    coin(d, (cx, cy), r=r)
    # 直径の寸法線（硬貨の上端〜下端に合わせる）
    x = cx - r - 70
    d.line([(x - 20, cy - r), (x + 20, cy - r)], fill=SUB, width=6)
    d.line([(x - 20, cy + r), (x + 20, cy + r)], fill=SUB, width=6)
    arrow(d, (x, cy), (x, cy - r), fill=SUB, width=6, head=24)
    arrow(d, (x, cy), (x, cy + r), fill=SUB, width=6, head=24)
    label(d, (x - 90, cy), "直径", size=60, fill=SUB)
    # 厚み（横から見た図）
    d.rectangle([640, 1420, 700, 1700], fill=(205, 170, 90), outline=INK, width=6)
    arrow(d, (580, 1380), (640, 1380), fill=SUB, width=6, head=22)
    arrow(d, (760, 1380), (700, 1380), fill=SUB, width=6, head=22)
    label(d, (670, 1320), "厚み", size=60, fill=SUB)
    label(d, (330, 1560), "横から見ると", size=48)
    return save(img, out, "fig2_size.png")


def fig3_coil():
    """3枚目：コイルの磁界で材質を見る（電子式の選別装置）。"""
    img, d = canvas()
    title(d, "磁界で材質を見る", y=220)
    # コイル（巻き線を楕円で表現）
    cx, cy = 540, 900
    for i in range(6):
        y = cy - 150 + i * 60
        d.ellipse([cx - 220, y - 22, cx + 220, y + 22], outline=INK, width=8)
    label(d, (cx + 330, cy), "コイル", size=56)
    # 磁界の線（コイルの上下に回り込む）
    for r in (300, 380, 460):
        d.arc([cx - r, cy - r * 1.25, cx + r, cy + r * 1.25], start=200, end=340, fill=SUB, width=6)
        d.arc([cx - r, cy - r * 1.25, cx + r, cy + r * 1.25], start=20, end=160, fill=SUB, width=6)
    label(d, (cx + 330, cy - 470), "磁界", size=56, fill=SUB)
    # 磁界の中を通過する硬貨
    coin(d, (cx, cy + 430), r=80)
    arrow(d, (cx - 380, cy + 430), (cx - 110, cy + 430), fill=INK, width=10)
    arrow(d, (cx + 110, cy + 430), (cx + 380, cy + 430), fill=INK, width=10)
    label(d, (cx, 1660), "金属で変化が違う", size=64, fill=ACCENT)
    label(d, (cx, 1760), "（電子式の選別装置の例）", size=46)
    return save(img, out, "fig3_coil.png")


def fig4_sort():
    """4枚目：基準内は金庫へ、基準外は返却口へ。"""
    img, d = canvas()
    title(d, "基準外は返却口へ", y=220)
    coin(d, (540, 560), r=80)
    arrow(d, (540, 660), (540, 860), width=14)
    d.rounded_rectangle([300, 880, 780, 1060], radius=24, outline=INK, width=10)
    label(d, (540, 970), "判定", size=72)
    arrow(d, (440, 1070), (260, 1340), width=14)
    arrow(d, (640, 1070), (820, 1340), fill=ACCENT, width=14)
    d.rounded_rectangle([90, 1360, 430, 1540], radius=24, outline=INK, width=10)
    label(d, (260, 1450), "受け入れ", size=60)
    d.rounded_rectangle([650, 1360, 990, 1540], radius=24, outline=ACCENT, width=10)
    label(d, (820, 1450), "返却口", size=60, fill=ACCENT)
    label(d, (260, 1610), "基準内", size=48)
    label(d, (820, 1610), "基準外", size=48, fill=ACCENT)
    return save(img, out, "fig4_sort.png")


if __name__ == "__main__":
    for f in (fig1_question, fig2_size, fig3_coil, fig4_sort):
        f()
