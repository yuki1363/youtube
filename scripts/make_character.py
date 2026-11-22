#!/usr/bin/env python3
"""案内役キャラクター（オリジナル）の3案 × 表情4種を SVG で生成する。
使い方: python3 scripts/make_character.py  → assets/character/<案>/<表情>.svg と preview.html
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "character"
EXPRS = ["normal", "talk", "smile", "surprise"]
EXPR_JA = {"normal": "通常", "talk": "話す", "smile": "笑顔", "surprise": "驚き"}


def face(cx, cy, expr, eye="#2B2B2B", mouth="#2B2B2B", cheek=True, dx=32):
    s = []
    if expr == "smile":
        for x in (cx - dx, cx + dx):
            s.append(f'<path d="M{x-10} {cy+2} Q{x} {cy-12} {x+10} {cy+2}" stroke="{eye}" stroke-width="5" fill="none" stroke-linecap="round"/>')
    elif expr == "surprise":
        for x in (cx - dx, cx + dx):
            s.append(f'<circle cx="{x}" cy="{cy-2}" r="11" fill="{eye}"/><circle cx="{x+3}" cy="{cy-6}" r="3.5" fill="#fff"/>')
    else:
        for x in (cx - dx, cx + dx):
            s.append(f'<ellipse cx="{x}" cy="{cy}" rx="7" ry="10" fill="{eye}"/><circle cx="{x+2}" cy="{cy-4}" r="2.5" fill="#fff"/>')
    my = cy + 32
    if expr == "normal":
        s.append(f'<path d="M{cx-12} {my} Q{cx} {my+9} {cx+12} {my}" stroke="{mouth}" stroke-width="4" fill="none" stroke-linecap="round"/>')
    elif expr == "talk":
        s.append(f'<ellipse cx="{cx}" cy="{my+3}" rx="13" ry="10" fill="#7A2E2E"/><ellipse cx="{cx}" cy="{my+8}" rx="7" ry="4" fill="#E57373"/>')
    elif expr == "smile":
        s.append(f'<path d="M{cx-18} {my-3} Q{cx} {my+20} {cx+18} {my-3} Z" fill="#7A2E2E"/>')
    else:
        s.append(f'<ellipse cx="{cx}" cy="{my+3}" rx="7" ry="9" fill="#7A2E2E"/>')
        s.append(f'<path d="M{cx+70} {cy-40} q8 14 0 20 q-8 -6 0 -20 Z" fill="#7EC8F0"/>')
    if cheek:
        s.append(f'<ellipse cx="{cx-dx-20}" cy="{cy+20}" rx="11" ry="7" fill="#F48FB1" opacity=".55"/>')
        s.append(f'<ellipse cx="{cx+dx+20}" cy="{cy+20}" rx="11" ry="7" fill="#F48FB1" opacity=".55"/>')
    return "".join(s)


def char_a(expr):  # 若手保全マン（人）
    return (
        '<path d="M90 400 Q100 300 200 295 Q300 300 310 400 Z" fill="#3B6FB6"/>'
        '<path d="M168 300 L200 338 L232 300 Z" fill="#E8EEF6"/>'
        '<rect x="232" y="335" width="34" height="26" rx="4" fill="#2C548F"/>'
        '<rect x="186" y="262" width="28" height="40" fill="#F6D2B5"/>'
        '<circle cx="117" cy="212" r="15" fill="#F2C4A2"/><circle cx="283" cy="212" r="15" fill="#F2C4A2"/>'
        '<circle cx="200" cy="205" r="85" fill="#F6D2B5"/>'
        '<path d="M115 190 Q118 228 128 236 L128 190 Z M285 190 Q282 228 272 236 L272 190 Z" fill="#3A2A20"/>'
        '<path d="M108 192 A92 92 0 0 1 292 192 Z" fill="#F5C518"/>'
        '<rect x="192" y="104" width="16" height="86" rx="8" fill="#FFD84D"/>'
        '<rect x="94" y="184" width="212" height="18" rx="9" fill="#D9A800"/>'
        '<polygon points="214,128 188,160 204,160 194,184 224,148 207,148" fill="#2C548F"/>'
        + face(200, 232, expr)
    )


def char_b(expr):  # ブレーカーのマスコット
    return (
        '<rect x="178" y="34" width="44" height="74" rx="14" fill="#E53935"/>'
        '<rect x="158" y="84" width="84" height="56" rx="12" fill="#4A5563"/>'
        '<ellipse cx="102" cy="262" rx="20" ry="28" fill="#EEF1F4" stroke="#9AA5B1" stroke-width="6"/>'
        '<ellipse cx="298" cy="262" rx="20" ry="28" fill="#EEF1F4" stroke="#9AA5B1" stroke-width="6"/>'
        '<ellipse cx="160" cy="362" rx="30" ry="14" fill="#7D8894"/><ellipse cx="240" cy="362" rx="30" ry="14" fill="#7D8894"/>'
        '<rect x="110" y="120" width="180" height="235" rx="30" fill="#EEF1F4" stroke="#9AA5B1" stroke-width="6"/>'
        '<rect x="142" y="300" width="116" height="10" rx="5" fill="#2E7D32"/>'
        '<circle cx="152" cy="330" r="8" fill="#C0C8D0"/><circle cx="200" cy="330" r="8" fill="#C0C8D0"/><circle cx="248" cy="330" r="8" fill="#C0C8D0"/>'
        + face(200, 205, expr, dx=30)
    )


def char_c(expr):  # AIロボット
    return (
        '<line x1="200" y1="62" x2="200" y2="104" stroke="#5C6B7A" stroke-width="6"/>'
        '<circle cx="200" cy="56" r="11" fill="#F5C518"/>'
        '<rect x="108" y="270" width="30" height="70" rx="15" fill="#9FD3E8" stroke="#5C8FA8" stroke-width="5"/>'
        '<rect x="262" y="270" width="30" height="70" rx="15" fill="#9FD3E8" stroke="#5C8FA8" stroke-width="5"/>'
        '<rect x="140" y="258" width="120" height="110" rx="26" fill="#9FD3E8" stroke="#5C8FA8" stroke-width="6"/>'
        '<circle cx="200" cy="308" r="24" fill="#fff" stroke="#5C8FA8" stroke-width="4"/>'
        '<path d="M184 312 A18 18 0 0 1 216 312" stroke="#C0C8D0" stroke-width="3" fill="none"/>'
        '<line x1="200" y1="312" x2="212" y2="296" stroke="#E53935" stroke-width="4" stroke-linecap="round"/>'
        '<rect x="110" y="102" width="180" height="152" rx="42" fill="#9FD3E8" stroke="#5C8FA8" stroke-width="6"/>'
        '<path d="M113 150 Q113 105 160 105 L240 105 Q287 105 287 150 Z" fill="#F5C518"/>'
        '<rect x="136" y="148" width="128" height="88" rx="24" fill="#1F2D3A"/>'
        + face(200, 180, expr, eye="#6FF2FF", mouth="#6FF2FF", cheek=False, dx=28)
    )


CHARS = {
    "a_hozen": ("A 若手保全マン", char_a),
    "b_breaker": ("B ブレーカーのマスコット", char_b),
    "c_robot": ("C AIロボット", char_c),
}


def svg(body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">{body}</svg>\n'


def main():
    cells = []
    for key, (name, fn) in CHARS.items():
        d = OUT / key
        d.mkdir(parents=True, exist_ok=True)
        row = []
        for e in EXPRS:
            s = svg(fn(e))
            (d / f"{e}.svg").write_text(s, encoding="utf-8")
            row.append(f'<figure>{s}<figcaption>{EXPR_JA[e]}</figcaption></figure>')
        cells.append(f'<section><h2>{name}</h2><div class="row">{"".join(row)}</div></section>')
    html = ('<!doctype html><meta charset="utf-8"><style>'
            'body{margin:0;padding:24px;background:#F7F8FA;font-family:"Noto Sans CJK JP",sans-serif}'
            'h2{margin:8px 0;font-size:26px}.row{display:flex;gap:12px}'
            'figure{margin:0;background:#fff;border-radius:12px;padding:6px;text-align:center}'
            'svg{width:220px;height:220px}figcaption{font-size:18px;color:#555}</style>'
            + "".join(cells))
    (OUT / "preview.html").write_text(html, encoding="utf-8")
    print("出力:", OUT)


if __name__ == "__main__":
    main()
