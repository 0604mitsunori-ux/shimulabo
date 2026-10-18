"""何代前？計算（sedai-sakanobori）の図。式・時代の区切りはページの JS と同じ：
何年前＝2026−西暦、何代前＝Math.round(何年前÷1世代の年数)、その代の人数＝2^何代前。"""
import math
from figlib import *

ANCHOR = r'<div class="note" style="border-left:4px solid var\(--teal\)">.*?</div>\n'
NOW = 2026
# ページの JS の判定（y>=1989 平成・令和 … y>=794 平安）と同じ区切り
ERAS = [("平安", 794, 1184), ("鎌倉", 1185, 1335), ("室町", 1336, 1466), ("戦国", 1467, 1572), ("安土桃山", 1573, 1602),
        ("江戸", 1603, 1867), ("明治", 1868, 1911), ("大正", 1912, 1925), ("昭和", 1926, 1988), ("平成・令和", 1989, NOW)]


def jsround(x):
    return math.floor(x + 0.5)


def gen_of(y, g=30):
    return max(0, jsround(max(0, NOW - y) / g))


def jidai(y):
    for nm, a, b in ERAS:
        if a <= y <= b:
            return nm
    return "それ以前"


def jp_people(n):
    if n < 100000:
        return f"{n:,}"
    if n < 10 ** 8:
        return f"約{n // 10 ** 4:,}万"
    if n < 10 ** 12:
        return f"約{n / 10 ** 8:.1f}億"
    return f"約{n / 10 ** 12:.1f}兆"


def fig1():
    b = []
    Y0, Y1, X0, X1 = 1100, NOW, 90, 1110
    px = lambda y: X0 + (y - Y0) * (X1 - X0) / (Y1 - Y0)
    # 上：式と例
    b.append(rect(48, 100, 1104, 112, CARD, LINE, 12))
    b.append(text(76, 142, "何代前", 24, INK, 700) + text(160, 142, "≒（ 2026 − 西暦 ）÷ 1世代の年数（25〜30年）", 24, INK, 700))
    y = 1700; yrs = NOW - y; g = gen_of(y)
    b.append(text(76, 186, f"例：西暦{y}年 → {yrs}年前 ÷ 30年 ≒ {yrs / 30:.1f} → 約{g}代前（{jidai(y)}時代）。その代の直系のご先祖は 2の{g}乗＝{2 ** g:,}人。", 17, INK2))
    # 年の目盛り
    ay = 268
    b.append(line(X0, ay, X1, ay, INK, 1.6))
    for yy in range(1100, 2001, 100):
        b.append(line(px(yy), ay - 6, px(yy), ay, INK, 1.4) + text(px(yy), ay - 12, f"{yy}年", 14, INK2, anchor="middle"))
    b.append(text(X1 + 8, ay + 6, "今", 16, ACC, 700) + line(X1, ay - 6, X1, ay + 54, ACC, 2))
    # 時代の帯
    by, bh = 276, 46
    for i, (nm, a, e) in enumerate(ERAS):
        x0, x1 = px(max(a, Y0)), px(min(e + 1, NOW))
        if x1 <= x0:
            continue
        b.append(f'<rect x="{x0:.1f}" y="{by}" width="{x1 - x0:.1f}" height="{bh}" fill="{[TEAL_L, GOLD_L][i % 2]}" stroke="#fff" stroke-width="1"/>')
        w = len(nm) * 16
        if x1 - x0 > w + 6:
            b.append(text((x0 + x1) / 2, by + 29, nm, 16, INK, 700, "middle"))
        else:
            cx = (x0 + x1) / 2
            lx = {"安土桃山": cx, "大正": cx - 12, "平成・令和": cx + 2}[nm]
            b.append(line(cx, by + bh, lx, by + bh + 12, MUTED, 1) + text(lx, by + bh + 28, nm, 14, INK2, 700, "middle"))
    b.append(text(X0, by + bh + 28, "← 昔", 14, MUTED))
    # 世代の目盛り（30年・25年）
    for row, (g, gy, col, ac, note) in enumerate([(30, 412, TEAL, "teal", "1世代30年のとき（ツールの初期値）"),
                                                  (25, 540, GOLD, "gold", "1世代25年のとき")]):
        b.append(text(X0, gy - 34, note, 16, col, 700))
        b.append(line(X0, gy, X1, gy, col, 2.4))
        n = 0
        while NOW - g * n >= Y0:
            x = px(NOW - g * n)
            big = n % 5 == 0
            b.append(line(x, gy - (10 if big else 5), x, gy + (10 if big else 5), col, 2 if big else 1.2))
            if big and n:
                b.append(text(x, gy + 30, f"{n}代前", 16, INK, 700, "middle") + text(x, gy + 50, f"{NOW - g * n}年", 14, INK2, anchor="middle"))
            n += 1
        b.append(text(X1, gy + 30, "あなた", 15, INK, 700, "middle"))
    return svg("".join(b), "何代前？ 年数と世代・時代の対応（しくみ）",
               "小さい目盛り＝1世代。時代の区切りはツールの判定と同じ。1世代の年数の取り方で何代前かは前後する（目安）。")


def fig2():
    b = []
    rows = []
    for nm, a, e in ERAS[::-1]:
        if nm == "平成・令和":
            continue
        g_new, g_old = gen_of(e), gen_of(a)
        rows.append((nm, f"{a}〜{e}年", f"{NOW - e}〜{NOW - a}年前", f"約{g_new}〜{g_old}代前",
                     f"{jp_people(2 ** g_new)}〜{jp_people(2 ** g_old)}人"))
    x0, y0, hh, rh = 50, 100, 46, 48
    cw = [150, 230, 220, 230, 270]
    heads = ["時代", "西暦", "何年前（2026年から）", "何代前（30年）", "その代のご先祖"]
    tw_ = sum(cw)
    b.append(rect(x0, y0, tw_, hh + rh * len(rows), CARD, LINE, 10))
    b.append(f'<rect x="{x0}" y="{y0}" width="{tw_}" height="{hh}" rx="10" fill="{TEAL_L}"/>')
    cx = x0
    for c, w in zip(heads, cw):
        b.append(text(cx + w / 2, y0 + 30, c, 17, INK, 700, "middle")); cx += w
    for i, r in enumerate(rows):
        yy = y0 + hh + rh * i
        if r[0] == "江戸":
            b.append(f'<rect x="{x0 + 1}" y="{yy}" width="{tw_ - 2}" height="{rh}" fill="{GOLD_L}"/>')
        elif i % 2 == 1:
            b.append(f'<rect x="{x0 + 1}" y="{yy}" width="{tw_ - 2}" height="{rh}" fill="#f7f5ef"/>')
        b.append(line(x0, yy, x0 + tw_, yy, LINE, 1))
        cx = x0
        for j, (c, w) in enumerate(zip(r, cw)):
            if j == 0:
                b.append(text(cx + w / 2, yy + 32, c, 19, INK, 700, "middle"))
            elif j == 3:
                b.append(text(cx + w / 2, yy + 32, c, 20, ACC, 700, "middle"))
            else:
                b.append(text(cx + w / 2, yy + 31, c, 16.5, INK, 400, "middle"))
            cx += w
    b.append(text(x0, y0 + hh + rh * len(rows) + 34,
                  "人数は理論上の数（2の「何代前」乗）。同じ人が何度もご先祖として登場するため、実際はもっと少ない。", 15.5, INK2))
    return svg("".join(b), "時代ごとの「何代前？」早見表（1世代30年）",
               "時代の区切り・計算はツールと同じ（何代前＝何年前÷30を四捨五入）。1世代25年なら何代前は2割ほど多くなる。")


FIGS = [
    dict(svg=fig1, alt="西暦1100年から2026年までの時代区分（平安・鎌倉・室町・戦国・安土桃山・江戸・明治・大正・昭和・平成・令和）の帯と、1世代30年・25年のときに何代前がどの年にあたるかを示した目盛りの図。何代前＝（2026−西暦）÷1世代の年数で計算する。",
         caption="年数と世代・時代の対応。1世代30年なら10代前は1726年ごろ（江戸中期）、20代前は1426年ごろ（室町）。"),
    dict(svg=fig2, alt="時代ごとに、ご先祖が何代前にあたるかの早見表。江戸時代は約5〜14代前、戦国時代は約15〜19代前、鎌倉時代は約23〜28代前など、西暦・何年前・その代の直系のご先祖の人数（理論上）を並べている。",
         caption="時代ごとの何代前の早見表。江戸時代のご先祖はおよそ5〜14代前。"),
]
