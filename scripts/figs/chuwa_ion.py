"""酸・アルカリと中和（chuwa-ion）の授業用の図
数値はシミュ（scripts/rika/sims_suiyoueki_kuuki.py の JS_CHUWA）と同じモデル：
  うすい塩酸10 cm³ に H⁺・Cl⁻ が各10こ。同じ濃さの水酸化ナトリウム水溶液 1 cm³ に Na⁺・OH⁻ が各1こ。
  cnt(v)：H⁺＝max(0,10−v)、Cl⁻＝10、Na⁺＝v、OH⁻＝max(0,v−10)、水＝min(10,v)。
  pH（参考）は塩酸・水酸化ナトリウム水溶液とも 0.1 mol/L として計算。BTB は pH 6.0 以下 黄色、7.6 以上 青色。"""
import math
import random
import re
from figlib import *

N0, CM = 10, 0.1
ION = {"H": ("H^+", ACC, "水素イオン"), "Cl": ("Cl^-", GREEN, "塩化物イオン"),
       "Na": ("Na^+", PURPLE, "ナトリウムイオン"), "OH": ("OH^-", TEAL, "水酸化物イオン")}
BTB = {"黄色": "#f7e7a1", "緑色": "#cfe6d3", "青色": "#cfdff0"}


def cnt(v, k=1):
    a = k * v
    return dict(H=max(0, N0 - a), Cl=N0, Na=a, OH=max(0, a - N0), W=min(N0, a))


def pH(v, k=1):
    d = (CM * N0 - k * CM * v) / (N0 + v); h = (d + math.sqrt(d * d + 4e-14)) / 2
    return -math.log10(h)


def btb_name(p):        # シミュの btbName
    return "黄色" if p < 6.5 else ("緑色" if p <= 7.4 else "青色")


def nature(c):
    return "酸性" if c["H"] > 0 else ("アルカリ性" if c["OH"] > 0 else "中性")


NATC = {"酸性": ACC, "中性": GREEN, "アルカリ性": TEAL_D}


def chem(x, y, s, size=20, fill=INK, weight=400, anchor="start", sub=None):
    """化学式。_2 / _{2} は下付き、^+ / ^{3} は上付き（tspan の dy でずらす）"""
    sub = sub or max(14, round(size * 0.7)); cur = 0.0; out = []
    for t in re.findall(r"_\{[^}]*\}|_\d+|\^\{[^}]*\}|\^[+\-−]|[^_^]+", s):
        if t[0] in "_^":
            body = (t[2:-1] if t[1] == "{" else t[1:]).replace("-", "−")
            tgt = size * 0.28 if t[0] == "_" else -size * 0.42
            out.append(f'<tspan dy="{tgt - cur:.1f}" font-size="{sub}">{esc(body)}</tspan>'); cur = tgt
        else:
            out.append(f'<tspan dy="{-cur:.1f}">{esc(t)}</tspan>' if cur else esc(t)); cur = 0.0
    w = ' font-weight="700"' if weight >= 700 else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}"{w}>{"".join(out)}</text>'


def ion(cx, cy, t, r=15.6):
    lb, col, _ = ION[t]
    return (circle(cx, cy, r, col, INK, 0.8)
            + chem(cx, cy + 5, lb, 14, "#fff", 700, "middle", sub=14).replace("<text ", '<text letter-spacing="-0.4" ', 1))


def water(cx, cy):
    return (circle(cx - 8, cy + 6, 5.5, "#fff", INK2, 1) + circle(cx + 8, cy + 6, 5.5, "#fff", INK2, 1)
            + circle(cx, cy - 1, 10, SKY, INK2, 1))


def fig1():
    b = []
    stages = [(0, "加える前（塩酸10 cm^{3}）"), (6, "6 cm^{3} 加えた"), (10, "10 cm^{3} 加えた"), (14, "14 cm^{3} 加えた")]
    pw, gp = 264, 16
    for i, (v, head) in enumerate(stages):
        x0 = 48 + i * (pw + gp); c = cnt(v); p = pH(v); nat = nature(c); bn = btb_name(p)
        b.append(rect(x0, 100, pw, 498, CARD, LINE, 12))
        b.append(badge(x0 + 22, 128, str(i + 1), INK2, "#fff", 15))
        b.append(chem(x0 + 40, 134, head, 17, INK, 700))
        b.append(chem(x0 + 40, 160, f"液の体積 {N0 + v} cm^{{3}}", 15, INK2))
        L, R, bot = x0 + 16, x0 + 248, 444
        top = bot - (N0 + v) * 11
        b.append(f'<rect x="{L}" y="{top}" width="{R - L}" height="{bot - top}" fill="{BTB[bn]}"/>')
        b.append(line(L, top, R, top, INK2, 1, "4 3"))
        # 粒をます目にばらばらに置く（並びは毎回同じ）
        cs = 32; cols = int((R - L - 8) // cs); rows = int((bot - top - 6) // cs)
        cells = [(cc, rr) for rr in range(rows) for cc in range(cols)]
        rnd = random.Random(100 + v); rnd.shuffle(cells)
        kinds = ["H"] * c["H"] + ["Cl"] * c["Cl"] + ["Na"] * c["Na"] + ["OH"] * c["OH"] + ["W"] * c["W"]
        rnd.shuffle(kinds)
        ox = L + (R - L - cols * cs) / 2
        for kd, (cc, rr) in zip(kinds, cells):
            px, py = ox + (cc + 0.5) * cs, bot - 3 - (rr + 0.5) * cs
            b.append(water(px, py) if kd == "W" else ion(px, py, kd))
        b.append(f'<path d="M{L - 8},172 L{L},178 L{L},{bot - 8} Q{L},{bot} {L + 8},{bot} L{R - 8},{bot} Q{R},{bot} {R},{bot - 8} L{R},178 L{R + 8},172" fill="none" stroke="{INK2}" stroke-width="2.6"/>')
        # 数
        y = 476
        for j, (t, n) in enumerate([("H", c["H"]), ("Cl", c["Cl"]), ("Na", c["Na"]), ("OH", c["OH"])]):
            xx, yy = x0 + 20 + (j % 2) * 124, y + (j // 2) * 28
            b.append(chem(xx, yy, ION[t][0], 17, ION[t][1], 700) + text(xx + 92, yy, f"{n}こ", 17, INK, 700, "end"))
        b.append(text(x0 + 20, y + 56, "水", 17, "#1b6f99", 700) + text(x0 + 112, y + 56, f"{c['W']}こ", 17, INK, 700, "end"))
        b.append(text(x0 + 20, y + 90, nat, 19, NATC[nat], 700))
        b.append(text(x0 + 20 + len(nat) * 19 + 8, y + 90, f"BTB溶液：{bn}", 15, INK2))
        if v == 6:
            b.append(text(x0 + 244, y + 56, "中和は起きている", 15, ACC, 700, "end"))
        if v == 10:
            b.append(text(x0 + 244, y + 56, "ちょうど中和", 15, GREEN, 700, "end"))
        if v == 14:
            b.append(chem(x0 + 244, y + 56, "OH^- が残る", 15, TEAL_D, 700, "end"))
    b.append(chem(48, 620, "中和：H^+ ＋ OH^- → H_2O（水）。Na^+ と Cl^- は塩（塩化ナトリウム）として液にとけたまま。", 17, INK, 700))
    return svg("".join(b), "中和のしくみ（イオンのモデル）",
               "うすい塩酸10 cm³に同じ濃さの水酸化ナトリウム水溶液を加えていく。イオンの数は数えやすくしたモデル。")


def fig2():
    b = []
    x0, y0, w, h, XM, YM = 104, 566, 480, 380, 20, 20
    gx = lambda a: x0 + a / XM * w
    gy = lambda n: y0 - n / YM * h
    b.append(text(48, 128, "加えた量とイオンの数", 19, INK, 700))
    b.append(chem(250, 128, "（塩酸10 cm^{3}・同じ濃さの水酸化ナトリウム水溶液）", 15, INK2))
    b.append(text(48, y0 - h - 26, "イオンの数［こ］", 15, INK))
    b.append(axes(x0, y0, w, h, "", "", [(gx(a) - x0, str(a)) for a in range(2, 21, 2)],
                  [(y0 - gy(n), str(n)) for n in range(5, 21, 5)], 15))
    b.append(text(x0 - 10, y0 + 24, "0", 15, INK2, anchor="end"))
    b.append(chem(x0 + w, y0 + 48, "加えた水酸化ナトリウム水溶液［cm^{3}］", 15, INK, anchor="end"))
    # 酸性・中性・アルカリ性
    b.append(line(gx(10), y0, gx(10), y0 - h, GREEN, 1.8, "6 5"))
    b.append(text(gx(5), y0 - h - 8, "酸性（BTB：黄色）", 15, ACC, 700, "middle"))
    b.append(text(gx(10), y0 - h - 30, "中性（緑色）", 15, GREEN, 700, "middle"))
    b.append(text(gx(15), y0 - h - 8, "アルカリ性（青色）", 15, TEAL_D, 700, "middle"))
    xs = [0, 10, 20]
    sty = {"H": None, "Cl": "8 5", "Na": None, "OH": "8 5"}
    for t in ("Cl", "Na", "OH", "H"):
        b.append(poly([(gx(a), gy(cnt(a)[t])) for a in xs], ION[t][1], 3.4, dash=sty[t]))
    # 線の名前（線のすぐそばに）
    b.append(chem(gx(2.8), gy(8.3), "H^+ 水素イオン", 16, ACC, 700))
    b.append(chem(gx(13.2), gy(10.6), "Cl^- 塩化物イオン", 16, GREEN, 700))
    ang = math.degrees(math.atan2(gy(0) - gy(1), gx(1) - gx(0)))      # Na⁺ の線の画面上の傾き
    nx, ny = gx(12.0) - 9 * math.sin(math.radians(ang)), gy(12.0) - 9 * math.cos(math.radians(ang))
    b.append(f'<g transform="rotate({-ang:.2f} {nx:.1f} {ny:.1f})">' + chem(nx, ny, "Na^+ ナトリウムイオン", 16, PURPLE, 700) + "</g>")
    b.append(chem(gx(19.8), gy(1.4), "OH^- 水酸化物イオン", 16, TEAL_D, 700, "end"))
    # 右：指示薬の早見表
    X = 640
    b.append(text(X, 128, "指示薬の色の早見表", 19, INK, 700))
    rows = [["青色リトマス紙", "赤色になる", "変化なし", "変化なし"],
            ["赤色リトマス紙", "変化なし", "変化なし", "青色になる"],
            ["BTB溶液", "　 黄色", "　 緑色", "　 青色"],
            ["フェノールフタレイン溶液", "無色", "無色", "赤色"],
            ["pH", "7より小さい", "7", "7より大きい"]]
    cw = [196, 104, 104, 108]; rh = 44
    b.append(table(X, 146, ["指示薬", "酸性", "中性", "アルカリ性"], rows, cw, rh, 15))
    yy = 146 + rh * 3
    for j, nm in enumerate(["黄色", "緑色", "青色"]):
        cx = X + cw[0] + sum(cw[1:1 + j]) + cw[1 + j] / 2
        b.append(rect(cx - 26, yy + 13, 18, 18, BTB[nm], INK2, 4, 1))
    # pH のものさし
    py = 446
    b.append(f'<rect x="{X}" y="{py}" width="512" height="16" rx="8" fill="url(#phbar)"/>')
    for v, lab in [(0, "0"), (7, "7"), (14, "14")]:
        xx = X + 512 * v / 14
        b.append(line(xx, py + 16, xx, py + 22, INK, 1.4) + text(xx, py + 40, lab, 15, INK2, anchor="middle" if v == 7 else ("start" if v == 0 else "end")))
    b.append(text(X + 28, py + 40, "← 酸性が強い", 15, ACC, 700))
    b.append(text(X + 484, py + 40, "アルカリ性が強い →", 15, TEAL_D, 700, "end"))
    b.append(rect(X, 510, 512, 92, CARD, LINE, 10))
    b.append(chem(X + 16, 540, "・中性にならなくても、H^+ と OH^- が結びつけば中和は起きている", 15, INK))
    b.append(text(X + 16, 568, "・中性の液を蒸発させると、塩化ナトリウム（塩）の結晶が残る", 15, INK))
    b.append(text(X + 16, 594, "・中和が起きると熱が出て、液の温度が少し上がる", 15, INK))
    defs = ('<linearGradient id="phbar" x1="0" x2="1" y1="0" y2="0">'
            '<stop offset="0" stop-color="#c4442b"/><stop offset=".22" stop-color="#e08a3c"/><stop offset=".4" stop-color="#e8c84e"/>'
            '<stop offset=".5" stop-color="#5aa36b"/><stop offset=".66" stop-color="#4f8fbf"/><stop offset=".84" stop-color="#2c6b86"/>'
            '<stop offset="1" stop-color="#6a5c82"/></linearGradient>')
    return svg("".join(b), "中和とイオンの数・指示薬の色（まとめ）",
               "グラフはシミュのモデル（塩酸10 cm³の中の水素イオン・塩化物イオンが各10こ）。中性になるのは10 cm³加えたとき。", defs)


FIGS = [
    dict(svg=fig1, alt="中和のしくみをイオンのモデルで表した図。うすい塩酸10 cm³（H⁺とCl⁻が10こずつ）に水酸化ナトリウム水溶液を0・6・10・14 cm³加えたときのビーカーの中のイオン（H⁺・Cl⁻・Na⁺・OH⁻）と水の分子の数と、液の性質（酸性・中性・アルカリ性）とBTB溶液の色（黄色・緑色・青色）を並べている。",
         caption="中和のしくみ。加えた OH⁻ は H⁺ と結びついて水になる。H⁺ が残れば酸性、過不足なく結びつくと中性、OH⁻ が残るとアルカリ性。"),
    dict(svg=fig2, alt="塩酸に水酸化ナトリウム水溶液を加えた量とイオンの数のグラフ（H⁺は減って10 cm³で0、Cl⁻は10こで変わらない、Na⁺は増え続ける、OH⁻は10 cm³をこえると増える）と、リトマス紙・BTB溶液・フェノールフタレイン溶液の色とpHを酸性・中性・アルカリ性でまとめた早見表。",
         caption="加えた量とイオンの数のグラフ、指示薬の色の早見表。中性にならなくても中和は起きている。"),
]
