"""地層のでき方と柱状図（chisou）の授業用の図
   断面図と柱状図はページの JS（scripts/rika/sims_chisou.py）の「はじめの例」と同じ計算：
   地層（下から）れき3・砂5・泥6・火山灰1・泥5・砂7・れき4・砂6・泥10 m、隆起の傾き 東へ100mで4m低い（k＝−0.04）、
   地表の標高は HP の点をカトマル–ロム曲線でつないだ形、地層の底 U＝ceil(max(地表−地層の厚さ−k(x−200))＋4)、
   A〜D は西から 50・150・250・350 m、ボーリングは 35 m。→ 鍵層（火山灰）の上面の標高 A50・B46・C42・D38 m（例題1と同じ）。"""
import math
from figlib import *

HP = [57, 60, 66, 70, 64, 55, 59, 65, 62]
SCRIPT = [("g", 3), ("s", 5), ("m", 6), ("a", 1), ("m", 5), ("s", 7), ("g", 4), ("s", 6), ("m", 10)]
K = -0.04
BD = 35
XS = [("A", 50), ("B", 150), ("C", 250), ("D", 350)]
TY = {"g": ("れき", "#f2d3a7", "#9a5b13"), "s": ("砂", "#fbecb2", "#a16207"), "m": ("泥", "#cbd5e1", "#475569"),
      "a": ("火山灰", "#fdeef5", "#be185d"), "b": ("古い岩石", "#a8a29e", "#78716c")}
ROCK = {"g": "れき岩", "s": "砂岩", "m": "泥岩", "a": "凝灰岩"}


def Hx(x):
    x = max(0, min(400, x)); i = min(7, int(x // 50)); t = (x - i * 50) / 50
    p0, p1, p2, p3 = HP[max(0, i - 1)], HP[i], HP[i + 1], HP[min(8, i + 2)]
    return 0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3)


BOT = [0]
for _, th in SCRIPT: BOT.append(BOT[-1] + th)
TT = BOT[-1]
U = math.ceil(max(Hx(x) - TT - K * (x - 200) for x in range(0, 401)) + 4)


def base(x): return U + K * (x - 200)
def G(x): return min(Hx(x), base(x) + TT - 0.3)


def column(x):
    """地表から 35 m の区間（上から順に (種類, 上の標高, 下の標高)）"""
    g = G(x); lo = g - BD; out = []
    b0 = base(x)
    if b0 > lo: out.append(("b", min(b0, g), lo))
    for i, (t, th) in enumerate(SCRIPT):
        top, bot = min(b0 + BOT[i + 1], g), max(b0 + BOT[i], lo)
        if top > bot + 1e-6: out.append((t, top, bot))
    return g, sorted(out, key=lambda v: -v[1])


IA = [t for t, _ in SCRIPT].index("a")
def ash_top(x): return base(x) + BOT[IA + 1]


def patterns(prefix):
    """柱状図の記号（教科書と同じ：れき＝丸、砂＝点、泥＝横線、火山灰＝V、古い岩石＝ななめ線）"""
    p = []
    c, d = TY["g"][1], TY["g"][2]
    p.append(f'<pattern id="{prefix}g" width="22" height="18" patternUnits="userSpaceOnUse"><rect width="22" height="18" fill="{c}"/>'
             + "".join(f'<circle cx="{a}" cy="{b_}" r="{r}" fill="none" stroke="{d}" stroke-width="0.9"/>' for a, b_, r in ((5, 5, 2.8), (14, 5, 1.8), (18, 13, 2.5), (9, 13, 1.7), (2, 15, 1.2))) + '</pattern>')
    c, d = TY["s"][1], TY["s"][2]
    p.append(f'<pattern id="{prefix}s" width="14" height="10" patternUnits="userSpaceOnUse"><rect width="14" height="10" fill="{c}"/>'
             + "".join(f'<circle cx="{a}" cy="{b_}" r="0.9" fill="{d}"/>' for a, b_ in ((2, 2), (7, 4), (11, 1.5), (4, 7), (10, 8), (13, 5.5), (1, 9))) + '</pattern>')
    c, d = TY["m"][1], TY["m"][2]
    p.append(f'<pattern id="{prefix}m" width="14" height="10" patternUnits="userSpaceOnUse"><rect width="14" height="10" fill="{c}"/>'
             f'<path d="M1,3 H6 M8,8 H13" stroke="{d}" stroke-width="1"/></pattern>')
    c, d = TY["a"][1], TY["a"][2]
    p.append(f'<pattern id="{prefix}a" width="14" height="10" patternUnits="userSpaceOnUse"><rect width="14" height="10" fill="{c}"/>'
             f'<path d="M2,2 L4,6 L6,2 M9,5 L11,9 L13,5" fill="none" stroke="{d}" stroke-width="1"/></pattern>')
    c, d = TY["b"][1], TY["b"][2]
    p.append(f'<pattern id="{prefix}b" width="12" height="12" patternUnits="userSpaceOnUse"><rect width="12" height="12" fill="{c}"/>'
             f'<path d="M0,12 L12,0 M-6,6 L6,-6 M6,18 L18,6" stroke="{d}" stroke-width="1"/></pattern>')
    return "".join(p)


def swatch(x, y, t, w=30, h=18, pre="cs"):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{pre}{t})" stroke="{INK2}" stroke-width="0.8"/>'


def fig1():
    b = []
    # ---- 左：海岸から沖まで ----
    b.append(text(48, 128, "川が運んだ土砂の積もり方（海岸から沖まで）", 18, INK, 700))
    X0, X1, Y0, WL = 48, 560, 150, 214
    shore = 176
    yf = lambda x: WL + 14 + 0.21 * (x - shore)               # 海底（沖ほど深い）
    b.append(f'<rect x="{X0}" y="{Y0}" width="{X1 - X0}" height="250" rx="10" fill="#eef5fa"/>')
    b.append(f'<path d="M{shore},{WL} L{X1},{WL} L{X1},{yf(X1):.1f} L{shore},{yf(shore):.1f}Z" fill="#9cc7e4" opacity=".75"/>')
    land = f'M{X0},{WL - 40} L{shore},{WL} L{shore},{yf(shore):.1f} L{X1},{yf(X1):.1f} L{X1},{Y0 + 250} L{X0},{Y0 + 250}Z'
    b.append(f'<path d="{land}" fill="#e7dcc8"/>')
    b.append(line(X0, WL - 40, shore, WL, GREEN, 4))
    b.append(line(shore, WL, X1, WL, TEAL, 1.6) + text(X1 - 8, WL - 8, "海面", 14, TEAL, anchor="end"))
    b.append(text(64, WL + 36, "陸", 18, GREEN, 700))
    b.append(arrow(70, WL - 46, shore + 34, WL - 6, "teal", 2.6) + text(shore + 46, WL - 14, "川が土砂を運ぶ", 15, TEAL, 700))
    zones = [("g", shore, shore + 104), ("s", shore + 104, shore + 230), ("m", shore + 230, X1)]
    for t, xa, xb in zones:
        b.append(f'<path d="M{xa},{yf(xa):.1f} L{xb},{yf(xb):.1f} L{xb},{yf(xb) + 16:.1f} L{xa},{yf(xa) + 16:.1f}Z" fill="url(#cs{t})" stroke="{INK2}" stroke-width="0.8"/>')
        xm = (xa + xb) / 2
        b.append(text(xm, yf(xm) + 42, TY[t][0], 18, INK, 700, "middle"))
    for xa, xb, n, r in ((shore + 12, shore + 96, 5, 3.2), (shore + 116, shore + 222, 8, 1.8), (shore + 242, X1 - 10, 12, 1.1)):
        for j in range(n):
            px = xa + (xb - xa) * (j + 0.5) / n; py = WL + 10 + ((j * 37) % 19)
            if py < yf(px) - 6: b.append(circle(px, py, r, TY["g"][2] if r > 3 else TY["s"][2] if r > 1.5 else TY["m"][2], "none", 0))
    b.append(text(shore + 4, Y0 + 238, "← 岸の近く（浅い）", 14, INK2) + text(X1 - 10, Y0 + 238, "沖（深い）→", 14, INK2, anchor="end"))
    b.append(text(48, 428, "粒が大きく重いものほど早くしずみ、岸の近くに積もる。", 15.5, INK))
    rows = [["れき", "直径2mm以上", "れき岩"], ["砂", "2mm〜約0.06mm", "砂岩"], ["泥", "約0.06mm以下", "泥岩"], ["火山灰", "噴火でふき出された粒", "凝灰岩"]]
    b.append(table(48, 444, ["粒", "大きさ", "固まった岩石"], rows, [110, 250, 152], 34, 15.5))
    # ---- 右：隆起したあとの断面（シミュの「はじめの例」）----
    SX0, SX1, ZT, ZB, SY0 = 640, 1140, 80, 18, 168
    PXM = (SX1 - SX0) / 400; PZ = PXM * 2.5                      # 高さは横の2.5倍
    xp = lambda x: SX0 + x * PXM; zp = lambda z: SY0 + (ZT - z) * PZ
    SY1 = zp(ZB)
    b.append(text(600, 128, "隆起して陸になった地層の断面（例）", 18, INK, 700))
    clip = f'<clipPath id="cs-sec"><path d="M{SX0},{SY1} ' + " ".join(f"L{xp(x):.1f},{zp(G(x)):.1f}" for x in range(0, 401, 2)) + f' L{SX1},{SY1}Z"/></clipPath>'
    g = [f'<g clip-path="url(#cs-sec)">']
    band = lambda lo, hi, f: f'<path d="M{xp(-4):.1f},{zp(hi(-4)):.1f} ' + " ".join(f"L{xp(x):.1f},{zp(hi(x)):.1f}" for x in range(0, 405, 5)) + " " + " ".join(f"L{xp(x):.1f},{zp(lo(x)):.1f}" for x in range(404, -5, -5)) + f'Z" fill="{f}"/>'
    g.append(band(lambda x: ZB - 30, base, "url(#csb)"))
    for i, (t, th) in enumerate(SCRIPT):
        g.append(band(lambda x, i=i: base(x) + BOT[i], lambda x, i=i: base(x) + BOT[i + 1], f"url(#cs{t})"))
    for i in range(len(SCRIPT) + 1):
        g.append(poly([(xp(x), zp(base(x) + BOT[i])) for x in range(0, 401, 10)], "rgba(30,41,59,.55)", 0.9))
    g.append("</g>")
    b.append("".join(g))
    b.append(poly([(xp(x), zp(G(x))) for x in range(0, 401, 2)], GREEN, 3.4))
    b.append(f'<rect x="{SX0}" y="{zp(ZT)}" width="{SX1 - SX0}" height="{SY1 - zp(ZT)}" fill="none" stroke="{MUTED}" stroke-width="1"/>')
    for z in range(20, 81, 10):
        b.append(line(SX0 - 5, zp(z), SX0, zp(z), INK2, 1.2) + text(SX0 - 8, zp(z) + 5, f"{z}m", 14, INK2, anchor="end"))
    b.append(text(SX0 - 8, zp(ZT) - 10, "標高", 14, INK2, anchor="end"))
    for x in (0, 100, 200, 300, 400):
        b.append(line(xp(x), SY1, xp(x), SY1 + 5, INK2, 1.2) + text(xp(x), SY1 + 22, f"{x}m", 14, INK2, anchor="middle"))
    b.append(text(SX0, SY1 + 44, "西", 16, INK, 700) + text(SX1, SY1 + 44, "東", 16, INK, 700, "end"))
    # ボーリング
    for nm, x in XS:
        gx = G(x); X = xp(x)
        b.append(f'<rect x="{X - 3:.1f}" y="{zp(gx):.1f}" width="6" height="{BD * PZ:.1f}" fill="#fff" fill-opacity=".65" stroke="{INK}" stroke-width="1.2"/>')
        b.append(text(X, zp(gx) - 10, nm, 18, INK, 700, "middle"))
    # 鍵層のラベル
    xl = 22; zt = ash_top(xl)
    b.append(line(xp(xl), zp(zt) - 2, xp(xl), zp(74) + 4, "#9d174d", 1.4) + circle(xp(xl), zp(zt), 3, "#9d174d", "#9d174d", 0))
    b.append(text(xp(xl) - 6, zp(74), "火山灰の層（鍵層）", 15, "#9d174d", 700))
    # 古い・新しい
    ax = SX1 + 0
    b.append(lines(600, SY1 + 72, ["地層は下ほど古く、上ほど新しい。隆起のときに東へかたむいた。",
                                   "A〜D：ボーリング（地表から35m）。柱状図は次の図。",
                                   "高さは横の約2.5倍に強調してかいている。"], 15, INK2, gap=1.5))
    b.append(rect(600, 506, 552, 108, TEAL_L, TEAL, 10, 1.2))
    b.append(text(616, 532, "地層からわかること", 16, TEAL_D, 700))
    b.append(lines(616, 558, ["・下から「れき→砂→泥」と粒が小さい → 海がだんだん深くなった",
                              "・火山灰の層は広い範囲にほぼ同時に積もる",
                              "　→ はなれた地点の地層を比べる手がかり（鍵層）"], 15, INK, gap=1.5))
    return svg("".join(b), "地層のでき方",
               "海の深さで積もる粒が変わり、地層は下から積み重なる。陸で見られるのは、大地が隆起したから。",
               patterns("cs") + clip)


def fig2():
    b = []
    cols = [(nm, x) + column(x) for nm, x in XS]
    zt = math.ceil(max(c[2] for c in cols) / 5) * 5; zb = math.floor(min(c[2] - BD for c in cols) / 5) * 5
    Y0, Y1 = 196, 566
    yz = lambda z: Y0 + (zt - z) / (zt - zb) * (Y1 - Y0)
    CX = [176, 300, 424, 548]; CW = 56
    b.append(text(48, 128, "A〜D の柱状図（標高をそろえて、西から東へ）", 18, INK, 700))
    for v in range(zb, zt + 1, 5):
        b.append(line(92, yz(v), 96, yz(v), INK2, 1.2) + text(88, yz(v) + 5, f"{v}m", 14, INK2, anchor="end"))
        b.append(line(96, yz(v), 590, yz(v), "#ece8de", 1))
    b.append(line(96, Y0, 96, Y1, INK2, 1.2) + text(60, Y0 - 16, "標高", 14, INK2))
    ash = []
    for (nm, x, g, iv), cx in zip(cols, CX):
        x0 = cx - CW / 2
        b.append(text(cx, 162, nm, 20, INK, 700, "middle") + text(cx, 182, f"標高{g:.0f}m", 14, INK2, anchor="middle"))
        for t, top, bot in iv:
            b.append(f'<rect x="{x0}" y="{yz(top):.1f}" width="{CW}" height="{yz(bot) - yz(top):.1f}" fill="url(#cf{t})" stroke="rgba(30,41,59,.7)" stroke-width="0.8"/>')
        b.append(f'<rect x="{x0}" y="{yz(g):.1f}" width="{CW}" height="{BD * (Y1 - Y0) / (zt - zb):.1f}" fill="none" stroke="{INK}" stroke-width="1.4"/>')
        a = ash_top(x); ash.append((cx, yz(a)))
        b.append(text(cx, Y1 + 24, f"深さ{g - a:.0f}m", 15, "#9d174d", 700, "middle"))
    for (x1, y1), (x2, y2) in zip(ash, ash[1:]):
        b.append(line(x1 + CW / 2, y1, x2 - CW / 2, y2, "#db2777", 2.2, "6 4"))
    b.append(text(48, Y1 + 24, "鍵層まで", 14, "#9d174d", 700))
    b.append(text(48, Y1 + 48, "赤い点線＝火山灰の層（鍵層）の上面。東へ100mずつはなれた4地点。", 14, MUTED))
    # 右：計算と記号
    x0 = 640
    b.append(rect(x0, 112, 512, 70, TEAL_L, TEAL, 10, 1.4))
    b.append(text(x0 + 16, 140, "鍵層の上面の標高", 17, TEAL_D, 700))
    b.append(text(x0 + 16, 168, "＝ 地表の標高 − 地表から鍵層の上面までの深さ", 16, INK))
    rows = []
    for nm, x, g, iv in cols:
        a = ash_top(x); rows.append([nm, f"{g:.0f}m", f"{g - a:.0f}m", f"{g:.0f} − {g - a:.0f} ＝ {a:.0f}m"])
    b.append(table(x0, 196, ["地点", "地表の標高", "鍵層の深さ", "鍵層の上面の標高"], rows, [70, 130, 130, 182], 40, 16))
    d100 = ash_top(150) - ash_top(50)
    b.append(text(x0, 430, f"→ 東へ100mごとに{abs(d100):.0f}mずつ低い。", 18, ACC, 700))
    b.append(text(x0, 456, "地層は東に低くなるように傾いている。", 16, INK))
    b.append(text(x0, 498, "柱状図の記号", 16, INK, 700))
    for i, t in enumerate(("g", "s", "m", "a", "b")):
        xx = x0 + (i % 3) * 172; yy = 512 + (i // 3) * 34
        b.append(swatch(xx, yy, t, pre="cf") + text(xx + 38, yy + 15, TY[t][0] + (f"（{ROCK[t]}）" if t in ROCK else ""), 15, INK))
    return svg("".join(b), "柱状図の読み方（鍵層で地層の傾きを読む）",
               "離れた地点は、深さではなく標高をそろえて比べる。火山灰の層は広い範囲にほぼ同時に積もるので、手がかりになる。",
               patterns("cf"))


FIGS = [
    dict(svg=fig1, alt="地層のでき方の図。川が運んだ土砂のうち、れきは岸の近く、砂は少しはなれた所、泥は沖の深い所に積もることを示す海岸の断面と、粒の大きさと岩石（れき岩・砂岩・泥岩・凝灰岩）の表、隆起して東へ傾いた地層の断面にA〜Dの4地点のボーリングを示す。",
         caption="地層のでき方。粒の大きさで積もる場所が変わり、地層は下から積み重なる。"),
    dict(svg=fig2, alt="A〜Dの4地点の柱状図を標高をそろえて並べ、火山灰の層（鍵層）の上面を点線でつないだ図。鍵層の上面の標高を「地表の標高−深さ」で求めると50m・46m・42m・38mで、東へ100mごとに4m低く、地層が東に傾いていることを読み取る。",
         caption="柱状図の読み方。鍵層の標高をそろえて比べると、地層の傾きがわかる。"),
]
