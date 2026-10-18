"""こん虫の育ち方と体のつくり（konchu-sodachi・小3）の授業用の図。日数・体のつくりは scripts/rika/sims_sho34_seibutsu.py（ページのJS）と同じ。"""
import math
from figlib import *

# ---- シミュと同じ日数（目安）
BF_ST = [("たまご", 0, 7), ("よう虫", 7, 24), ("さなぎ", 24, 34), ("成虫", 34, 60)]
GH_ST = [("たまご", 0, 14), ("よう虫", 14, 49), ("成虫", 49, 60)]
BF_MOLT = [10, 13, 16, 20]          # よう虫が皮をぬぐ日（4回）。24日目に5回目でさなぎ
GH_MOLT = [21, 28, 35, 42]          # 49日目に5回目の皮をぬいで成虫
def bf_len(d): return 3 * 10 ** ((d - 7) / 17)          # よう虫の体長 mm（3mm→30mm）
def gh_len(d): return 7 * (40 / 7) ** ((d - 14) / 35)   # よう虫の体長 mm（7mm→40mm）
DMAX, X0, X1 = 60, 230, 1130
def dx(d): return X0 + d * (X1 - X0) / DMAX
SFILL = {"たまご": GOLD_L, "よう虫": "#e4f1e8", "さなぎ": "#efe3cf", "成虫": TEAL_L}
SEDGE = {"たまご": GOLD, "よう虫": GREEN, "さなぎ": "#9a6b2f", "成虫": TEAL}


def ell(x, y, rx, ry, rot=0, fill="none", stroke="none", w=1.2, op=None):
    o = f' opacity="{op}"' if op is not None else ""
    return (f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{max(0.1, rx):.1f}" ry="{max(0.1, ry):.1f}" transform="rotate({math.degrees(rot):.1f} {x:.1f} {y:.1f})"'
            f' fill="{fill}" stroke="{stroke}" stroke-width="{w}"{o}/>')


def ln(x1, y1, x2, y2, w, c):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w:.1f}" stroke-linecap="round"/>'


# ---- 生き物の絵（JS の描き方を SVG に移したもの）
def caterpillar(x, y, Lp):
    n = 11; sp = Lp / (n - 1); r = max(1.4, sp * 0.78); out = []
    for i in range(n - 1, -1, -1):
        px = x - Lp / 2 + i * sp
        out.append(circle(px, y + r * 0.7, max(0.6, r * 0.22), "#3f6212", "#3f6212", 0))
        out.append(circle(px, y, r, "#4d7c0f" if i == 0 else "#84cc16", "#4d7c0f", 0.8))
    out.append(circle(x - Lp / 2 - r * 0.3, y - r * 0.2, r * 0.2, "#1f2937", "#1f2937", 0))
    return "".join(out)


def butterfly(x, y, s):
    out = []
    for sd in (-1, 1):
        g = f'<g transform="translate({x:.1f},{y:.1f}) scale({sd * s:.2f},{s:.2f})">'
        g += '<path d="M0,2 C30,0 38,18 26,30 C14,36 4,20 0,8Z" fill="#f4f6f8" stroke="#8b96a5" stroke-width="1.3" vector-effect="non-scaling-stroke"/>'
        g += '<path d="M0,-4 C10,-30 40,-36 46,-26 C44,-10 26,0 0,2Z" fill="#fbfcfd" stroke="#8b96a5" stroke-width="1.3" vector-effect="non-scaling-stroke"/>'
        g += '<circle cx="27" cy="-13" r="4.2" fill="#475569"/><circle cx="41" cy="-26" r="4.5" fill="#475569"/></g>'
        out.append(g)
    out.append(ell(x, y + 4 * s, 3 * s, 15 * s, 0, "#334155"))
    out.append(circle(x, y - 12 * s, 3.6 * s, "#1f2937", "#1f2937", 0))
    for sd in (-1, 1):
        out.append(ln(x + sd * 1.5 * s, y - 14 * s, x + sd * 10 * s, y - 30 * s, 1.4, "#334155") + circle(x + sd * 10 * s, y - 30 * s, 1.8 * s, "#334155", "#334155", 0))
    return "".join(out)


def pupa(x, y, s):
    out = [ln(x - 16 * s, y - 42 * s, x - 16 * s, y + 38 * s, 5, "#a16207")]
    out.append(f'<path d="M{x:.1f},{y - 36 * s:.1f} C{x + 16 * s:.1f},{y - 20 * s:.1f} {x + 14 * s:.1f},{y + 8 * s:.1f} {x + 3 * s:.1f},{y + 32 * s:.1f} '
               f'C{x - 8 * s:.1f},{y + 14 * s:.1f} {x - 12 * s:.1f},{y - 6 * s:.1f} {x - 10 * s:.1f},{y - 14 * s:.1f}Z" fill="#a3c46c" stroke="#4d7c0f" stroke-width="1.6"/>')
    out.append(ln(x - 16 * s, y - 4 * s, x + 8 * s, y - 8 * s, 1, "#9aa5b4") + ln(x - 16 * s, y + 4 * s, x + 8 * s, y - 8 * s, 1, "#9aa5b4"))
    return "".join(out)


def grasshopper(x, y, L, wf, nymph):
    col, dk = ("#84cc16" if nymph else "#65a30d"), "#3f6212"; lw = max(1.4, 0.02 * L); o = []
    o.append(ln(x - 0.28 * L, y + 0.06 * L, x - 0.32 * L, y + 0.15 * L, lw, dk) + ln(x - 0.32 * L, y + 0.15 * L, x - 0.37 * L, y + 0.23 * L, lw, dk))
    o.append(ln(x - 0.15 * L, y + 0.07 * L, x - 0.12 * L, y + 0.15 * L, lw, dk) + ln(x - 0.12 * L, y + 0.15 * L, x - 0.09 * L, y + 0.23 * L, lw, dk))
    o.append(ell(x + 0.16 * L, y, 0.32 * L, 0.085 * L, 0, col, dk, 1.2))
    for k in range(1, 6):
        xx = x - 0.1 * L + k * 0.09 * L; o.append(ln(xx, y - 0.06 * L, xx, y + 0.06 * L, 0.8, "#6f8f3a"))
    o.append(f'<rect x="{x - 0.33 * L:.1f}" y="{y - 0.105 * L:.1f}" width="{0.23 * L:.1f}" height="{0.19 * L:.1f}" rx="{0.05 * L:.1f}" fill="{col}" stroke="{dk}" stroke-width="1.2"/>')
    hr = (0.13 if nymph else 0.1) * L
    o.append(ell(x - 0.4 * L, y - 0.01 * L, hr * 0.9, hr, 0.2, col, dk, 1.2) + circle(x - 0.44 * L, y - 0.045 * L, hr * 0.36, "#713f12", "#713f12", 0))
    o.append(ln(x - 0.44 * L, y - 0.09 * L, x - 0.62 * L, y - 0.32 * L, max(1, 0.012 * L), dk))
    if wf > 0.5: o.append(ell(x + 0.2 * L, y - 0.075 * L, 0.42 * L * wf, 0.065 * L, 0.03, "#4d7c0f", dk, 1, 0.92))
    elif wf > 0: o.append(ell(x - 0.06 * L, y - 0.08 * L, 0.12 * L * wf * 2.2, 0.05 * L, 0.25, "#65a30d", dk, 1))
    o.append(ln(x - 0.08 * L, y + 0.02 * L, x + 0.3 * L, y - 0.13 * L, max(3, 0.07 * L), dk) + ln(x - 0.08 * L, y + 0.02 * L, x + 0.3 * L, y - 0.13 * L, max(2, 0.05 * L), col))
    o.append(ln(x + 0.3 * L, y - 0.13 * L, x + 0.17 * L, y + 0.23 * L, max(1.2, 0.022 * L), dk) + ln(x + 0.17 * L, y + 0.23 * L, x + 0.26 * L, y + 0.24 * L, max(1, 0.015 * L), dk))
    return "".join(o)


def row(y0, name, sub, tag, tagc, S, M, icons, desc):
    b = [text(48, y0 + 44, name, 22, INK, 700)]
    if sub: b.append(text(48, y0 + 70, sub, 14.5, MUTED))
    tw = len(tag) * 16 + 22
    b.append(rect(48, y0 + 86, tw, 30, tagc, tagc, 15, 0) + text(48 + tw / 2, y0 + 107, tag, 16, "#fff", 700, "middle"))
    b.append(icons)
    by = y0 + 124
    for n, a, z in S:
        x0, x1 = dx(a), dx(z)
        b.append(rect(x0 + 1, by, x1 - x0 - 2, 34, SFILL[n], SEDGE[n], 6, 1.4))
        b.append(text((x0 + x1) / 2, by + 24, n, 18, INK, 700, "middle"))
        if a > 0: b.append(text(x0, by - 6, f"{a}日", 14, MUTED, anchor="middle"))
    for m in M:
        x = dx(m); b.append(f'<path d="M{x - 7:.1f},{by + 37} L{x + 7:.1f},{by + 37} L{x:.1f},{by + 49}Z" fill="{GREEN}"/>')
    for (n, a, z), (l1, l2) in zip(S, desc):
        cx = (dx(a) + dx(z)) / 2
        b.append(text(cx, by + 72, l1, 15, INK, 400, "middle") + text(cx, by + 94, l2, 15, INK2, 400, "middle"))
    return "".join(b)


def fig1():
    b = []
    # モンシロチョウ
    y0 = 100; iy = y0 + 62
    ic = [ell(dx(3.5), iy + 6, 34, 16, -0.1, "#cdeccf", "#7fbf8a", 1.4), ell(dx(3.5), iy + 2, 5, 11, 0, "#facc15", "#a16207", 1.4)]
    ic.append(caterpillar(dx(10.5), iy + 8, 8 + bf_len(10) * 3.3))
    ic.append(arrow(dx(12.5), iy + 8, dx(16.5), iy + 8, "muted", 2) + text(dx(14.5), iy - 6, "大きくなる", 14, MUTED, anchor="middle"))
    ic.append(caterpillar(dx(20.5), iy + 8, 8 + bf_len(22) * 3.3))
    ic.append(pupa(dx(29) + 6, iy, 1.15))
    ic.append(butterfly(dx(47), iy + 4, 1.25))
    b.append(row(y0, "モンシロチョウ", "", "さなぎになる", TEAL, BF_ST, BF_MOLT, "".join(ic),
                 [("約1週間", "葉のうらに産む"), ("葉を食べ、皮をぬいで大きくなる", f"体長 約{bf_len(7):.0f}mm → 約{bf_len(24) / 10:.0f}cm"),
                  ("約10日", "何も食べず動かない"), ("花のみつをすう・はね4まい", "たまごを産む")]))
    # バッタ
    y0 = 330; iy = y0 + 62
    ic = [f'<rect x="{dx(1.5):.1f}" y="{iy - 16}" width="{dx(12.5) - dx(1.5):.1f}" height="58" rx="6" fill="#b58f62"/>',
          f'<g transform="translate({dx(7):.1f},{iy + 12}) rotate(-20)">' + ell(0, 0, 46, 15, 0, "#e7d3a8", "#92743f", 1.4)
          + "".join(ell(-34 + k * 8.5, 4 if k % 2 else -4, 4, 6, 0.3, "#f59e0b", "#92400e", 0.8) for k in range(9)) + "</g>"]
    ic.append(text(dx(1.5) + 8, iy + 2, "土の中", 14, "#fff", 700))
    ic.append(grasshopper(dx(19), iy + 14, 22 + gh_len(18) * 2.4, 0.1, True))
    ic.append(arrow(dx(23), iy + 10, dx(32), iy + 10, "muted", 2) + text(dx(27.5), iy - 4, "皮をぬいで大きくなる", 14, MUTED, anchor="middle"))
    ic.append(grasshopper(dx(41), iy + 14, 22 + gh_len(40) * 2.4, 0.1 + 0.12 * sum(1 for m in GH_MOLT if m <= 40), True))
    ic.append(grasshopper(dx(55), iy + 10, 118, 1, False))
    b.append(row(y0, "バッタ", "（トノサマバッタ）", "さなぎにならない", ACC, GH_ST, GH_MOLT, "".join(ic),
                 [("約2週間", "夏に産まれたたまご"), ("草を食べ、皮をぬいで大きくなる（成虫ににた形・はねは小さい）", f"体長 約{gh_len(14):.0f}mm → 約{gh_len(49) / 10:.0f}cm"),
                  ("はねがのびて", "とべる")]))
    # 日数の目もり
    ay = 572
    b.append(line(X0, ay, X1, ay, INK, 1.6))
    for d in range(0, DMAX + 1, 10):
        b.append(line(dx(d), ay, dx(d), ay + 6, INK, 1.4) + text(dx(d), ay + 26, f"{d}日", 15, INK2, anchor="middle"))
    b.append(text(48, ay + 6, "たまごからの日数", 16, INK, 700))
    b.append(f'<path d="M{X0 + 0:.1f},{ay + 40} l14,0 l-7,12z" fill="{GREEN}"/>')
    b.append(text(X0 + 22, ay + 52, "＝よう虫が皮をぬぐ日（4回）。5回目に皮をぬぐと、モンシロチョウはさなぎに、バッタは成虫になる。", 15, INK2))
    return svg("".join(b), "こん虫の育ち方（モンシロチョウとバッタ）",
               "日数はあたたかい季節（20〜25℃くらい）の目安。絵は形をわかりやすくした図で、大きさは実際とちがう。")


# ---- 体のつくり（JS のパズルの形を1.5倍にしたもの）
S, CX, OY = 1.5, 250, 146
def P(x, y): return CX + (x - 190) * S, OY + (y - 58) * S
LEGY = [166, 181, 196]; KNEE = [[46, 150], [58, 172], [52, 222]]; FOOT = [[62, 122], [86, 186], [76, 270]]


def insect():
    o, legs = [], []
    for k in range(3):                       # あし（むねから3対）
        for s in (-1, 1):
            a, kn, ft = P(190 + s * 16, LEGY[k]), P(190 + s * KNEE[k][0], KNEE[k][1]), P(190 + s * FOOT[k][0], FOOT[k][1])
            legs.append(poly([a, kn, ft], "#78350f", 6))
            legs.append(circle(ft[0], ft[1], 4, "#78350f", "#78350f", 0))
    hx, hy = P(190, 118)
    for s in (-1, 1):                        # しょっかく
        o.append(poly([P(190 + s * 6, 102), P(190 + s * 18, 76), P(190 + s * 30, 58)], "#7f1d1d", 3))
    bx, by = P(190, 288)
    o.append(ell(bx, by, 28 * S, 66 * S, 0, TEAL_L, TEAL, 2.4))
    for k in range(1, 7):
        yy = 288 - 66 + k * 132 / 7; hw = 28 * math.sqrt(max(0, 1 - ((yy - 288) / 66) ** 2))
        o.append(line(*P(190 - hw + 2, yy), *P(190 + hw - 2, yy), TEAL, 1.6))
    mx, my = P(190, 180)
    for s in (-1, 1):                        # はね（4まい・半とうめい）
        o.append(ell(*P(190 + s * 30, 180 + 44), 17 * S, 56 * S, -s * 0.28, "#dbeefa", "#3b9ad1", 1.5, 0.55))
        o.append(ell(*P(190 + s * 36, 180 + 56), 18 * S, 44 * S, -s * 0.5, "#dbeefa", "#3b9ad1", 1.5, 0.55))
    o += legs
    o.append(ell(mx, my, 20 * S, 28 * S, 0, "#e4f1e8", GREEN, 2.4))
    o.append(ell(hx, hy, 22 * S, 18 * S, 0, ACC_L, ACC, 2.4))
    for s in (-1, 1):
        o.append(ell(*P(190 + s * 14, 115), 7 * S, 9 * S, s * 0.3, "#1f2937"))
    o.append(ln(*P(185, 135), *P(182, 142), 3, "#7f1d1d") + ln(*P(195, 135), *P(198, 142), 3, "#7f1d1d"))
    return "".join(o)


def fig2():
    b = [text(48, 118, "こん虫の体のつくり（上から見た図）", 18, INK, 700), insect()]
    hx, hy = P(190, 118); mx, my = P(190, 180); bx, by = P(190, 288)
    LX = 452
    for (px, py), ly, nm, col, fill, d1 in [((hx + 34, hy), hy + 6, "頭", ACC, ACC_L, "目・しょっかく・口がある"),
                                          ((mx + 26, my + 14), my + 28, "むね", GREEN, "#e4f1e8", "あしが6本（3対）・はねがある"),
                                          ((bx + 43, by + 10), by + 2, "はら", TEAL, TEAL_L, "いくつかの「ふし」に分かれている")]:
        b.append(line(px, py, LX - 6, ly - 6, col, 1.8) + circle(px, py, 4, col, col, 0))
        b.append(rect(LX, ly - 34, 116, 40, fill, col, 8, 1.6) + text(LX + 58, ly - 6, nm, 22, col, 700, "middle"))
        b.append(text(LX, ly + 26, d1, 15.5, INK))
    ax, ay = P(190 - 30, 58); b.append(text(ax - 6, ay - 4, "しょっかく", 15, INK2, anchor="end"))
    fx, fy = P(190 - 86, 186); b.append(text(fx - 4, fy + 30, "あし", 15, INK2, 700, anchor="middle"))
    wx, wy = P(190 - 50, 262); b.append(line(wx, wy, wx - 34, wy + 36, MUTED, 1.4) + text(wx - 36, wy + 56, "はね", 15, INK2, 700, anchor="middle"))
    b.append(lines(LX, 580, ["あしも はねも、", "ぜんぶ「むね」から出ている。"], 16, ACC, 1.5, weight=700))
    # 右：こん虫かな？
    tx = 720
    b.append(text(tx, 118, "こん虫かな？（見分け方）", 18, INK, 700))
    rows = [("アリ", "3つ（頭・むね・はら）", "6本", 1), ("テントウムシ", "3つ（はらは はねの下）", "6本", 1), ("トンボ", "3つ", "6本", 1),
            ("クモ", "2つ（頭とむねが1つ）", "8本", 0), ("ダンゴムシ", "たくさんのふし", "14本", 0), ("ムカデ", "たくさんのふし", "30本以上", 0)]
    cw = [112, 170, 76, 74]; rh = 46; y = 132; tw = sum(cw)
    cw = [112, 170, 70, 80]
    tw = sum(cw)
    b.append(rect(tx, y, tw, rh * 7, CARD, LINE, 8))
    b.append(f'<rect x="{tx}" y="{y}" width="{tw}" height="{rh}" rx="8" fill="{TEAL_L}"/>')
    for i, h in enumerate(["生き物", "体の分かれ方", "あし", "こたえ"]):
        b.append(text(tx + sum(cw[:i]) + cw[i] / 2, y + 30, h, 16, INK, 700, "middle"))
    for r, (n, part, leg, ok) in enumerate(rows):
        yy = y + rh * (r + 1)
        if r % 2: b.append(f'<rect x="{tx + 1}" y="{yy}" width="{tw - 2}" height="{rh}" fill="#f7f5ef"/>')
        b.append(line(tx, yy, tx + tw, yy, LINE, 1))
        b.append(text(tx + cw[0] / 2, yy + 30, n, 15.5, INK, 700, "middle"))
        b.append(text(tx + cw[0] + cw[1] / 2, yy + 30, part, 14.5, INK, 400, "middle"))
        b.append(text(tx + sum(cw[:2]) + cw[2] / 2, yy + 30, leg, 15.5, INK, 700, "middle"))
        b.append(text(tx + sum(cw[:3]) + cw[3] / 2, yy + 30, "○" if ok else "×", 20, TEAL_D if ok else ACC, 700, "middle"))
    b.append(rect(tx, 470, tw, 142, GOLD_L, GOLD_L, 10))
    b.append(lines(tx + 16, 500, ["こん虫 ＝ 体が「頭・むね・はら」の3つに", "分かれていて、むねに あしが6本 ある。",
                                  "クモ・ダンゴムシ・ムカデは", "あしの数や体の分かれ方がちがう。"], 16, INK, 1.6))
    return svg("".join(b), "こん虫の体のつくりと見分け方",
               "体の図は、こん虫の体のつくりを表した図（特定の種類ではない）。○＝こん虫、×＝こん虫ではない。")


FIGS = [
    dict(svg=fig1, alt="モンシロチョウ（たまご→よう虫→さなぎ→成虫）とバッタ（たまご→よう虫→成虫、さなぎにならない）の育ち方を、たまごからの日数の帯でならべた図。よう虫は4回皮をぬいで大きくなり、モンシロチョウは24日目ごろさなぎ、34日目ごろ成虫、バッタは49日目ごろ成虫になる。",
         caption="こん虫の育ち方。モンシロチョウはさなぎになり、バッタはさなぎにならずに成虫になる。"),
    dict(svg=fig2, alt="こん虫の体のつくりの図。体が頭・むね・はらの3つに分かれ、頭に目・しょっかく・口、むねに6本のあしとはね、はらにふしがある。アリ・テントウムシ・トンボ・クモ・ダンゴムシ・ムカデがこん虫かどうかを、体の分かれ方とあしの数で見分ける表つき。",
         caption="こん虫の体のつくりと見分け方。体が頭・むね・はらの3つで、むねにあしが6本あるのがこん虫。"),
]
