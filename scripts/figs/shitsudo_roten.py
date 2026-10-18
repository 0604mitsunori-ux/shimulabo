"""湿度と雲のでき方（shitsudo-roten）の授業用の図。
飽和水蒸気量はシミュと同じ表（scripts/rika/sims_kishou_jishin.py の SAT・25℃＝23.1 g/m³）を読み込み、
表と表の間はシミュの JS と同じく直線で結んで計算する。"""
import os, sys
from figlib import *

_R = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rika")
if _R not in sys.path:
    sys.path.append(_R)
from sims_kishou_jishin import SAT          # noqa: E402


def sat(t):                                  # JS の sat()
    t = max(0.0, min(40.0, t)); i = min(39, int(t)); return SAT[i] + (SAT[i + 1] - SAT[i]) * (t - i)


def dew(v):                                  # JS の dew()
    if v <= SAT[0]: return 0.0
    for i in range(40):
        if v <= SAT[i + 1] + 1e-9: return i + (v - SAT[i]) / (SAT[i + 1] - SAT[i])
    return 40.0


def r1(v): return math.floor(v * 10 + 0.5) / 10
def f1(v): return "%.1f" % r1(v)


# 例題1〜3（ページの例題と同じ）：25℃・12.8 g/m³ の空気を 10℃まで冷やす
T0, V0, TC = 25, 12.8, 10
S0, TD, SC = sat(T0), dew(V0), sat(TC)
RH0 = V0 / S0 * 100
WT = r1(V0 - SC)
# 例題4・5：28℃・湿度50％ → 露点16℃ → 1200 m
T4 = 28; V4 = r1(sat(T4) * 50 / 100); TD4 = dew(V4); HB4 = (T4 - TD4) * 100
assert abs(S0 - 23.1) < 1e-9 and abs(TD - 15) < 1e-9 and abs(SC - 9.4) < 1e-9 and abs(WT - 3.4) < 1e-9
assert abs(V4 - 13.6) < 1e-9 and abs(TD4 - 16) < 1e-9 and abs(HB4 - 1200) < 1e-6


def drop(x, y, r, fill=TEAL):
    """しずくの形（先が上）"""
    return (f'<path d="M{x:.1f},{y - r * 1.7:.1f} Q{x + r:.1f},{y - r * 0.3:.1f} {x + r:.1f},{y + r * 0.2:.1f} '
            f'A{r:.1f},{r:.1f} 0 0 1 {x - r:.1f},{y + r * 0.2:.1f} Q{x - r:.1f},{y - r * 0.3:.1f} {x:.1f},{y - r * 1.7:.1f}Z" fill="{fill}"/>')


def fig1():
    b = []
    X0, Y0, KX, KY = 112, 566, 12.4, 8.0        # グラフの原点・1℃・1 g/m³ あたりの px
    gx = lambda t: X0 + t * KX
    gy = lambda v: Y0 - v * KY
    # 曲線の下（湿度100％未満）をうすくぬる
    pts = [(gx(t / 4), gy(sat(t / 4))) for t in range(0, 161)]
    b.append(f'<path d="M{gx(0)},{gy(0)} ' + " ".join(f"L{x:.1f},{y:.1f}" for x, y in pts) + f' L{gx(40)},{gy(0)}Z" fill="{TEAL_L}"/>')
    b.append(axes(X0, Y0, 40 * KX, 52 * KY, "気温［℃］", "", [(t * KX, str(t)) for t in range(0, 41, 5)],
                  [(v * KY, str(v)) for v in range(10, 51, 10)], 15))
    b.append(text(X0 - 50, 116, "水蒸気量［g/m³］", 15, INK))
    b.append(poly(pts, TEAL, 3.4))
    b.append(text(gx(31.6), gy(sat(36)) - 4, "飽和水蒸気量", 17, TEAL_D, 700, "end"))
    b.append(text(gx(31.6), gy(sat(36)) + 17, "（1 m³にふくめる最大の量）", 14, TEAL_D, anchor="end"))
    b.append(lines(gx(1), gy(48), ["曲線より上に出る分は、", "水滴になる"], 15, MUTED))
    b.append(text(gx(38.5), gy(4), "湿度100％未満の空気", 15, TEAL_D, anchor="end"))
    xa, ya, xd, xc, yc = gx(T0), gy(V0), gx(TD), gx(TC), gy(SC)
    # 25℃の飽和水蒸気量まで（あと何 g ふくめるか）
    b.append(line(xa, ya, xa, gy(S0), ACC, 1.6, "5 4") + circle(xa, gy(S0), 4.5, ACC, ACC, 0))
    b.append(text(xa + 10, gy(S0) - 8, f"25℃の飽和水蒸気量 {f1(S0)} g", 15, ACC, 700))
    b.append(text(xa + 10, (ya + gy(S0)) / 2 + 6, f"あと {f1(S0 - V0)} g ふくめる", 15, ACC))
    # 冷やす：水平に左へ → 露点で曲線にぶつかる → 曲線にそって 10℃まで
    b.append(line(xd, ya, xd, Y0, MUTED, 1.4, "5 4"))
    b.append(arrow(xa - 12, ya, xd + 12, ya, "acc", 3))
    b.append(text(xd + 12, ya + 28, "冷やす", 17, ACC, 700))
    b.append(text(xd + 12, ya + 48, "水蒸気量は変わらない", 14, ACC))
    cur = [(gx(TD - k * 0.25), gy(sat(TD - k * 0.25))) for k in range(0, int((TD - TC) * 4) + 1)]
    b.append(poly(cur, ACC, 4))
    b.append(line(xc, ya, xc, yc, TEAL_D, 7) + line(xc - 10, ya, xc + 10, ya, TEAL_D, 1.6) + line(xc - 10, yc, xc + 10, yc, TEAL_D, 1.6))
    b.append(line(xc, ya, xd, ya, MUTED, 1.2, "3 3"))
    b.append(text(xc - 14, (ya + yc) / 2 - 2, f"水滴 {f1(WT)} g", 16, TEAL_D, 700, "end"))
    b.append(text(xc - 14, (ya + yc) / 2 + 18, f"（{f1(V0)}−{f1(SC)}）", 14, TEAL_D, anchor="end"))
    b.append(circle(xc, yc, 6, CARD, TEAL_D, 2.4))
    b.append(circle(xd, ya, 8, CARD, TEAL, 3))
    b.append(text(xd + 6, Y0 - 12, f"露点 {TD:.0f}℃", 17, TEAL_D, 700))
    b.append(circle(xa, ya, 9, ACC, "#fff", 2.4))
    b.append(text(xa + 14, ya + 6, "はじめの空気", 16, ACC, 700))
    b.append(text(xa + 14, ya + 28, f"{T0}℃・{f1(V0)} g/m³・湿度 {f1(RH0)}％", 14, ACC))
    # 右：コップのたとえ（空気1 m³）
    b.append(text(708, 122, "コップのたとえ（空気1 m³）", 18, INK, 700))
    b.append(rect(708, 138, 14, 14, "none", INK, 2, 1.8) + text(728, 151, "コップ＝飽和水蒸気量", 15, INK2))
    b.append(f'<rect x="908" y="138" width="14" height="14" fill="{SKY}"/>' + text(928, 151, "中の水＝水蒸気量", 15, INK2))
    K, BY, CW = 10.0, 520, 86
    cups = [(786, T0, S0, V0, 0.0, f"湿度 {f1(RH0)}％", INK), (930, TD, V0, V0, 0.0, "湿度 100％（露点）", TEAL_D),
            (1070, TC, SC, SC, WT, f"水滴 {f1(WT)} g", TEAL_D)]
    for cx, t, s, v, wt, lab, col in cups:
        xl, xr, top, wl = cx - CW / 2, cx + CW / 2, BY - s * K, BY - v * K
        if wt > 0:
            gt = BY - (v + wt) * K
            b.append(f'<rect x="{xl:.1f}" y="{gt:.1f}" width="{CW}" height="{top - gt:.1f}" fill="{SKY}" opacity=".28" stroke="{SKY}" stroke-dasharray="4 3"/>')
            b.append(text(cx, gt - 8, "入りきらない", 14, TEAL_D, anchor="middle"))
            for k in range(3):
                b.append(drop(xr + 12 + k * 10, top + 18 + k * 22, 5))
        b.append(f'<rect x="{xl:.1f}" y="{wl:.1f}" width="{CW}" height="{BY - wl:.1f}" fill="{SKY}"/>')
        b.append(poly([(xl, top - 4), (xl, BY), (xr, BY), (xr, top - 4)], INK, 2.6))
        b.append(text(cx, (wl + BY) / 2 + 6, f"{f1(v)} g", 17, "#fff", 700, "middle"))
        b.append(text(cx, BY + 28, f"{t:.0f}℃", 19, INK, 700, "middle"))
        b.append(text(cx, BY + 52, f"コップ {f1(s)} g", 15, INK2, anchor="middle"))
        b.append(text(cx, BY + 76, lab, 15.5, col, 700, "middle"))
    for xa_, xb_ in ((833, 881), (977, 1022)):
        b.append(arrow(xa_, 370, xb_, 370, "acc", 2.4) + text((xa_ + xb_) / 2, 358, "冷やす", 14, ACC, anchor="middle"))
    return svg("".join(b), "湿度と露点のしくみ（飽和水蒸気量のグラフ）",
               "空気を冷やしても水蒸気量は変わらない。飽和水蒸気量と等しくなる温度が露点で、それより下では水滴ができる。")


def fig2():
    b = []
    rows = [("湿度［％］＝ 水蒸気量 ÷ 飽和水蒸気量 × 100",
             f"例：25℃・水蒸気量 {f1(V0)} g/m³ → {f1(V0)} ÷ {f1(S0)} × 100 ≒ {RH0:.1f}％"),
            ("露点 ＝ 飽和水蒸気量が、水蒸気量と等しくなる温度",
             f"例：水蒸気量 {f1(V0)} g/m³ → 飽和水蒸気量が {f1(V0)} g になるのは {TD:.0f}℃"),
            ("水滴の量 ＝ 水蒸気量 − 冷やした温度の飽和水蒸気量",
             f"例：{TC}℃まで冷やす → {f1(V0)} − {f1(SC)} ＝ {f1(WT)} g（空気1 m³あたり）"),
            ("雲ができ始める高さ ＝（地上の気温 − 露点）× 100 m",
             f"例：{T4}℃・湿度50％ → 水蒸気量 {f1(sat(T4))}×0.5＝{f1(V4)} g → 露点 {TD4:.0f}℃ → {HB4:.0f} m")]
    for i, (fm, ex) in enumerate(rows):
        y = 104 + i * 88
        b.append(rect(48, y, 712, 78, CARD, LINE, 10))
        b.append(badge(78, y + 39, str(i + 1), TEAL, "#fff", 18))
        b.append(text(108, y + 33, fm, 19, INK, 700))
        b.append(text(108, y + 62, ex, 16, INK2))
    # 右：空気が上昇すると雲ができる
    gx0, gy0, hmax, kh = 860, 452, 2000, 0.148
    hy = lambda h: gy0 - h * kh
    b.append(text(800, 122, "上昇する空気と雲（例：④）", 18, INK, 700))
    b.append(f'<rect x="{gx0}" y="{hy(hmax):.1f}" width="290" height="{gy0 - hy(hmax):.1f}" fill="{TEAL_L}"/>')
    b.append(f'<rect x="{gx0}" y="{gy0}" width="290" height="10" fill="#d8cfb8"/>')
    b.append(line(gx0, hy(hmax) - 6, gx0, gy0, INK, 1.6))
    for h in range(0, hmax + 1, 500):
        b.append(line(gx0 - 6, hy(h), gx0, hy(h), INK, 1.4) + text(gx0 - 10, hy(h) + 5, f"{h} m", 14, INK2, anchor="end"))
    hb = HB4; yb = hy(hb); px = gx0 + 110
    # 雲（雲底＝露点に達した高さ）
    cl = [(px - 40, yb - 26, 30), (px - 4, yb - 44, 36), (px + 36, yb - 28, 30), (px + 66, yb - 20, 22), (px - 66, yb - 18, 20)]
    b.append(f'<g clip-path="url(#sr-cloud)">' + "".join(f'<circle cx="{x}" cy="{y:.1f}" r="{r}" fill="#fff" stroke="{MUTED}" stroke-width="2"/>' for x, y, r in cl)
             + "".join(f'<circle cx="{x}" cy="{y:.1f}" r="{r - 2}" fill="#fff"/>' for x, y, r in cl)
             + f'<rect x="{px - 70}" y="{yb - 24:.1f}" width="140" height="24" fill="#fff"/></g>')
    defs = f'<clipPath id="sr-cloud"><rect x="{gx0}" y="{hy(hmax):.1f}" width="290" height="{yb - hy(hmax):.1f}"/></clipPath>'
    b.append(text(px, yb - 34, "雲", 18, INK2, 700, "middle"))
    b.append(line(gx0, yb, gx0 + 290, yb, TEAL_D, 2, "7 5"))

    for h in (0, 600):
        t = T4 - h / 100
        b.append(circle(px, hy(h) - (14 if h == 0 else 0), 14, CARD, ACC, 2.4))
        b.append(text(px + 24, hy(h) - (14 if h == 0 else 0) + 6, f"{h} m：{t:.0f}℃", 15, ACC, 700))
    b.append(text(px + 14, yb + 22, f"{hb:.0f} m：{TD4:.0f}℃（露点）", 15, TEAL_D, 700))
    b.append(text(px + 14, yb + 42, "→ 雲ができ始める", 15, TEAL_D, 700))
    b.append(arrow(px, hy(0) - 32, px, hy(600) + 18, "acc", 2.4) + arrow(px, hy(600) - 18, px, yb + 4, "acc", 2.4))
    b.append(text(gx0 + 6, gy0 - 8, "地上", 14, INK2))
    b.append(text(800, 482 + 4, "100 m上がるごとに約1℃下がる", 15, ACC))
    # 下：飽和水蒸気量の表（5℃ごと）
    ts = list(range(0, 41, 5))
    b.append(table(48, 500, ["気温［℃］"] + [str(t) for t in ts], [["飽和水蒸気量［g/m³］"] + [f1(SAT[t]) for t in ts]],
                   [218] + [98] * 9, 46, 17))
    return svg("".join(b), "湿度・露点・雲のできる高さの求め方",
               "飽和水蒸気量は25℃＝23.1 g/m³の表の値（1℃ごとの表はページ下）。雲の中では下がり方が約0.5℃/100 mになる（発展）。", defs)


FIGS = [
    dict(svg=fig1,
         alt=f"飽和水蒸気量のグラフで、気温25℃・水蒸気量12.8 g/m³（湿度55.4％）の空気を冷やすと、露点15℃で飽和水蒸気量の曲線にぶつかり、10℃まで冷やすと1 m³あたり3.4 gの水滴ができることを示す図。飽和水蒸気量をコップ、水蒸気量を中の水にたとえた絵も並べている。",
         caption="湿度と露点のしくみ。冷やしても水蒸気量は変わらず、飽和水蒸気量と等しくなる温度（露点）から水滴ができる。"),
    dict(svg=fig2,
         alt="湿度・露点・水滴の量・雲ができ始める高さの4つの求め方を例題つきでまとめた図。気温28℃・湿度50％の空気が上昇すると露点16℃になる1200 mで雲ができ始める様子と、0〜40℃の5℃ごとの飽和水蒸気量の表もある。",
         caption="湿度・露点・雲のできる高さの求め方（まとめ）。100 m上がるごとに約1℃下がるとして計算する。"),
]
