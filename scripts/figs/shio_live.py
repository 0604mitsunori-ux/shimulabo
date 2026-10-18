"""今日の潮、いつ満ちる？（shio-live）の図。満潮・干潮のしくみ／大潮・小潮（月と太陽の並び方）。
言い方の正：気象庁「潮汐の仕組み」「潮汐・海面水位の用語集」
（起潮力＝月の引力＋地球が月との共通重心のまわりを回る慣性力、多くの場所で1日2回、満潮・干潮は毎日約50分ずつ遅れる、
新月・満月のころ大潮、上弦・下弦のころ小潮、新月から次の新月までにほぼ2回ずつ、日潮不等）。
数値：主太陰半日周潮 M2 の周期 12.4206時間＝12時間25分（半分 6時間12分、2回で24時間50分＝1日約50分遅れ）、
太陽の起潮力／月の起潮力＝(M☉/d☉³)/(M☾/d☾³)＝0.46。ライブのデータには依存しない。"""
import math
from figlib import *

WATER, WATER_D, EARTH = "#bcd8ea", "#5f97bb", "#cfdcc4"
M2 = 12.4206012                      # 時間


def hm(h):
    m = round(h * 60)
    return f"{m // 60}時間{m % 60}分"


def earth_tide(cx, cy, r, ax, ay, ang=0):
    """地球と、海面のふくらみ（ax：ふくらむ向きの半径、ay：直角の向きの半径、ang：ふくらむ向き°）"""
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{ax}" ry="{ay}" transform="rotate({ang} {cx} {cy})" fill="{WATER}" stroke="{WATER_D}" stroke-width="2"/>'
            + circle(cx, cy, r, EARTH, "#7d9a6c", 1.8))


def fig1():
    b = []
    cx, cy, r = 300, 372, 104
    b.append(earth_tide(cx, cy, r, 178, 124))
    b.append(text(cx, cy + 7, "地球", 20, "#3f5a33", 700, "middle"))
    mx = 640
    b.append(circle(mx, cy, 30, "#e9e4d6", INK2, 1.6) + text(mx, cy + 58, "月", 19, INK, 700, "middle"))
    b.append(arrow(cx + 196, cy, mx - 42, cy, "muted", 1.8))
    b.append(text((cx + 196 + mx - 42) / 2, cy - 12, "月の引力", 15, INK2, anchor="middle"))
    # 満潮・干潮の場所
    for x, y, t, anc in [(cx + 178 - 4, cy + 34, "満潮", "end"), (cx - 178 + 4, cy + 34, "満潮", "start"),
                         (cx, cy - 124 - 14, "干潮", "middle"), (cx, cy + 124 + 30, "干潮", "middle")]:
        b.append(text(x, y, t, 19, ACC if t == "満潮" else TEAL_D, 700, anc))
    # 自転の向き（北極の上から見て反時計回り）
    R2 = 150
    a0, a1 = math.radians(120), math.radians(150)
    p0 = (cx + R2 * math.cos(a0), cy - R2 * math.sin(a0)); p1 = (cx + R2 * math.cos(a1), cy - R2 * math.sin(a1))
    b.append(f'<path d="M{p0[0]:.1f},{p0[1]:.1f} A{R2},{R2} 0 0 0 {p1[0]:.1f},{p1[1]:.1f}" fill="none" stroke="{INK}" stroke-width="2.4" marker-end="url(#ah-ink)"/>')
    b.append(text(cx - 150, cy - 150, "地球の自転", 15, INK, 700, "middle"))
    b.append(lines(56, 128, ["月の側と、その反対側の2か所で海面が盛り上がる。", "地球が1回自転するあいだに、多くの場所で", "満潮と干潮が2回ずつ来る。"], 16, INK, 1.5))
    b.append(text(cx + 60, 600, "北極の上から見た図（大きさ・きょり・ふくらみは実際とちがう）", 14, MUTED, anchor="middle"))
    # 右：1日の潮位の変化（満潮からの時間）
    X0, Y0, Wd, Hd = 744, 452, 370, 224
    px = lambda h: X0 + 20 + h / 26 * (Wd - 24)
    py = lambda v: Y0 - 126 - v * 74
    b.append(text(X0 - 20, 128, "潮の高さの変わり方（目安）", 18, INK, 700))
    b.append(line(X0, Y0, X0 + Wd + 10, Y0, INK, 1.8, arrow="ink"))
    b.append(line(X0, Y0, X0, Y0 - Hd - 10, INK, 1.8, arrow="ink"))
    b.append(text(X0 + Wd / 2, Y0 + 50, "満潮からの時間", 14, INK2, anchor="middle"))
    b.append(text(X0 - 8, Y0 - Hd + 6, "潮位", 14, INK2, anchor="end"))
    pts = [(px(h / 10), py(math.cos(2 * math.pi * (h / 10) / M2))) for h in range(0, 261)]
    b.append(poly(pts, TEAL, 3))
    marks = [(0, "満潮"), (M2 / 2, "干潮"), (M2, "満潮"), (1.5 * M2, "干潮"), (2 * M2, "満潮")]
    for h, t in marks:
        v = math.cos(2 * math.pi * h / M2)
        b.append(circle(px(h), py(v), 5, ACC if t == "満潮" else TEAL_D, "#fff", 1.4))
        b.append(text(px(h), py(v) + (-14 if t == "満潮" else 28), t, 15, ACC if t == "満潮" else TEAL_D, 700, "middle"))
        b.append(line(px(h), Y0, px(h), Y0 + 6, INK, 1.4))
    b.append(text(px(0), Y0 + 24, "0", 14, INK2, anchor="middle"))
    b.append(text(px(M2), Y0 + 24, hm(M2), 14, INK2, anchor="middle"))
    b.append(text(px(2 * M2), Y0 + 24, hm(2 * M2), 14, INK2, anchor="middle"))
    b.append(lines(X0 - 20, 546, [f"満潮 → 干潮 → 満潮が約{hm(M2)}ごと。", f"次の日の同じ満潮は約{round((2 * M2 - 24) * 60)}分おそくなる。"], 16, INK, 1.5))
    b.append(text(X0 - 20, 604, "（月が1日に約50分おくれて南に来るため）", 14, INK2))
    return svg("".join(b), "満潮・干潮のしくみ",
               "起潮力＝月の引力と、地球が月と回ることで生まれる慣性力を合わせた力。実際は1日2回の満潮の高さがちがうことが多い。")


def fig2():
    b = []
    k = 0.46
    # 左：大潮
    for (X, ttl, sub, col) in [(48, "大潮（新月・満月のころ）", "月と太陽の力の向きが重なる → 干満の差が大きい", ACC),
                               (612, "小潮（上弦・下弦のころ）", "力の向きが直角にずれ、打ち消し合う → 差が小さい", TEAL)]:
        b.append(rect(X, 104, 540, 350, CARD, col, 12, 1.6))
        b.append(text(X + 18, 136, ttl, 20, col, 700))
        b.append(text(X + 18, 162, sub, 15, INK))
        # 太陽
        b.append(f'<path d="M{X},{250} A70,70 0 0 1 {X},{390}Z" fill="{SUN}" stroke="{GOLD}" stroke-width="1.5"/>')
        b.append(text(X + 30, 326, "太陽", 16, "#7a5512", 700, "middle"))
    ex, ey, r = 48 + 300, 320, 50
    b.append(earth_tide(ex, ey, r, 50 + 70 * (1 + k) * 0.62, 50 + 8))     # 大潮：横に大きくふくらむ
    b.append(text(ex, ey + 6, "地球", 15, "#3f5a33", 700, "middle"))
    for mx, nm in [(ex - 152, "新月"), (ex + 166, "満月")]:
        b.append(circle(mx, ey, 18, "#e9e4d6", INK2, 1.4) + text(mx, ey + 42, nm, 15, INK, 700, "middle"))
    b.append(text(ex + 166, ey + 62, "（どちらの位置でも）", 14, INK2, anchor="middle"))
    ex2 = 612 + 300
    b.append(earth_tide(ex2, ey, r, 50 + 70 * (1 - k) * 0.62 + 8, 50 + 14, 90))   # 小潮：月の向きに小さくふくらむ
    b.append(text(ex2, ey + 6, "地球", 15, "#3f5a33", 700, "middle"))
    for my, nm in [(ey + 108, "上弦"), (ey - 108, "下弦")]:      # 北極の上から見て反時計回り：太陽が左なら上弦は下側
        b.append(circle(ex2, my, 17, "#e9e4d6", INK2, 1.4) + text(ex2 + 28, my + 6, nm, 15, INK, 700))
    b.append(text(612 + 18, 440, "（大きさ・きょりは実際とちがう）", 14, MUTED))
    b.append(text(48 + 270, 438, "太陽の起潮力は月の約0.46倍", 15, INK, 700, "middle"))
    # 下：月齢と大潮・小潮
    X0, X1, yb = 120, 1080, 546
    P = 29.530588853
    px = lambda a: X0 + a / P * (X1 - X0)
    b.append(text(48, 484, "月齢と大潮・小潮（約15日ごとにくり返す）", 17, INK, 700))
    pts = []
    for i in range(0, 296):
        a = i / 10
        amp = abs(complex(1, 0) + k * complex(math.cos(4 * math.pi * a / P), math.sin(4 * math.pi * a / P)))
        pts.append((px(a), yb + 46 - amp * 30))
    b.append(poly(pts, TEAL, 2.6))
    b.append(text(48, yb + 10, "干満の差", 14, TEAL, 700))
    b.append(text(48, yb + 28, "（目安）", 14, TEAL))
    for a, nm, t in [(0, "新月", "大潮"), (P / 4, "上弦", "小潮"), (P / 2, "満月", "大潮"), (3 * P / 4, "下弦", "小潮"), (P, "新月", "大潮")]:
        b.append(moon_look(px(a), yb - 22, 15, 360 * a / P))
        b.append(text(px(a) + 22, yb - 16, nm, 14, INK2))
        b.append(text(px(a), yb + 66, t, 16, ACC if t == "大潮" else TEAL_D, 700, "middle"))
    return svg("".join(b), "大潮と小潮（月と太陽の並び方）",
               "大潮・小潮は「ころ」の目安。干満の差がいちばん大きくなるのは、新月・満月より少しおくれることが多い。")


FIGS = [
    dict(svg=fig1, alt="満潮と干潮のしくみの図。北極の上から見た地球で、月の側とその反対側の2か所の海面が盛り上がって満潮になり、その間が干潮になる。地球の自転で多くの場所では1日に満潮と干潮が2回ずつ来て、満潮から次の満潮まで約12時間25分、次の日は約50分おそくなることを潮位のグラフで示している。",
         caption="満潮・干潮のしくみ。月の側と反対側の海面が盛り上がり、地球の自転で1日に2回ずつ満潮と干潮が来る。"),
    dict(svg=fig2, alt="大潮と小潮の図。新月・満月のころは月と太陽と地球が一直線に並び、起潮力の向きが重なって干満の差が大きい大潮になる。上弦・下弦のころは月と太陽の向きが直角にずれて打ち消し合い、差が小さい小潮になる。月齢と大潮・小潮のくり返し（約15日ごと）も示す。",
         caption="大潮と小潮。新月・満月のころは干満の差が大きい大潮、上弦・下弦のころは差が小さい小潮。"),
]
