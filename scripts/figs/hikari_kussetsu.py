"""光の反射と屈折（hikari-kussetsu）の授業用の図。
角度はページのシミュ・本文の早見表と同じ式：屈折率 空気1.00・水1.33・ガラス1.50、n1 sin i ＝ n2 sin r（スネルの法則）、
臨界角 sinθc＝1/n。表の丸めも本文と同じ（0.1°未満を四捨五入）。"""
import math
from figlib import *

NW, NGL = 1.33, 1.50
WATER = "#dceaf2"


def r1(v): return math.floor(v * 10 + 0.5) / 10
def deg(v): return "%.1f°" % r1(v)


def refr(n1, n2, a):
    s = n1 * math.sin(math.radians(a)) / n2
    return None if s > 1 else math.degrees(math.asin(s))


CRIT_W, CRIT_G = math.degrees(math.asin(1 / NW)), math.degrees(math.asin(1 / NGL))


def P(o, ang, L):
    """o から画面の角度 ang（度・右＝0・下向きが＋）へ L 進んだ点"""
    a = math.radians(ang)
    return (o[0] + L * math.cos(a), o[1] + L * math.sin(a))


def ray_in(s, o, col=ACC, op=1):
    m = ((s[0] + o[0]) / 2, (s[1] + o[1]) / 2)
    return (f'<g opacity="{op}">' + line(s[0], s[1], m[0], m[1], col, 3.2, arrow="acc") + line(m[0], m[1], o[0], o[1], col, 3.2) + "</g>")


def ray_out(o, e, col=ACC, op=1):
    m = (o[0] + (e[0] - o[0]) * 0.62, o[1] + (e[1] - o[1]) * 0.62)
    return (f'<g opacity="{op}">' + line(o[0], o[1], m[0], m[1], col, 3.2, arrow="acc") + line(m[0], m[1], e[0], e[1], col, 3.2) + "</g>")


def arc(o, r, a0, a1, col, lab, lr=None, size=15):
    """角度の弧（画面の角度 a0→a1）と、その外側のラベル"""
    a0, a1 = min(a0, a1), max(a0, a1)
    p0, p1 = P(o, a0, r), P(o, a1, r)
    big = 1 if a1 - a0 > 180 else 0
    out = f'<path d="M{p0[0]:.1f},{p0[1]:.1f} A{r},{r} 0 {big} 1 {p1[0]:.1f},{p1[1]:.1f}" fill="none" stroke="{col}" stroke-width="2.4"/>'
    q = P(o, (a0 + a1) / 2, lr or r + 26)
    hl = dict(stroke=CARD, stroke_width=4, paint_order="stroke")
    if isinstance(lab, (list, tuple)):        # 2行（角度の名前／値）
        return out + text(q[0], q[1] - 4, lab[0], size, col, 700, "middle", **hl) + text(q[0], q[1] + 15, lab[1], size, col, 700, "middle", **hl)
    return out + text(q[0], q[1] + 5, lab, size, col, 700, "middle", **hl)


def panel(x, no, title, n_up, n_dn, i, mode):
    """x＝カード左。mode＝'in'（上→下へ進む）/'out'（下→上へ進む）"""
    w, oy = 352, 330
    o = (x + w / 2, oy)
    b = [rect(x, 100, w, 512, CARD, LINE, 12)]
    b.append(f'<rect x="{x + 1}" y="{oy}" width="{w - 2}" height="{190}" fill="{WATER}"/>')
    b.append(badge(x + 28, 132, no, TEAL, "#fff", 17) + text(x + 52, 139, title, 19, INK, 700))
    b.append(line(x + 1, oy, x + w - 1, oy, INK2, 2))
    b.append(line(o[0], oy - 150, o[0], oy + 160, MUTED, 1.6, "6 5") + text(o[0], oy - 158, "法線", 14, MUTED, anchor="middle"))
    b.append(text(x + 18, 196, n_up, 18, INK, 700) + text(x + 18, oy + 34, n_dn, 18, INK, 700))
    L = 160
    if mode == "in":
        r = refr(1.0, NW, i)
        s = P(o, -90 - i, L); b.append(ray_in(s, o))
        b.append(ray_out(o, P(o, -90 + i, L), op=0.35))
        b.append(ray_out(o, P(o, 90 - r, L)))
        b.append(arc(o, 62, -90 - i, -90, ACC, ["入射角", f"{i:.0f}°"], 124))
        b.append(arc(o, 50, -90, -90 + i, PURPLE, ["反射角", f"{i:.0f}°"], 124))
        b.append(arc(o, 62, 90 - r, 90, TEAL, ["屈折角", deg(r)], 124))
    else:
        r = refr(NW, 1.0, i)
        s = P(o, 90 + i, L); b.append(ray_in(s, o))
        b.append(arc(o, 62, 90, 90 + i, ACC, ["入射角", f"{i:.0f}°"], 124))
        if r is None:
            b.append(ray_out(o, P(o, 90 - i, L)))
            b.append(arc(o, 50, 90 - i, 90, PURPLE, ["反射角", f"{i:.0f}°"], 124))
            b.append(text(o[0], oy - 60, "空気へ出ていく光はない", 16, INK2, 700, "middle", stroke=CARD, stroke_width=5, paint_order="stroke"))
        else:
            b.append(ray_out(o, P(o, 90 - i, L), op=0.35))
            b.append(ray_out(o, P(o, -90 + r, L)))
            b.append(arc(o, 62, -90, -90 + r, TEAL, ["屈折角", deg(r)], 124))
    return b


def fig1():
    b = []
    b += panel(48, "1", "空気 → 水", "空気", "水", 40, "in")
    b.append(lines(68, 548, ["入射角 ＞ 屈折角", "法線に近づくように曲がる"], 17, INK, 1.5))
    b += panel(424, "2", "水 → 空気", "空気", "水", 30, "out")
    b.append(lines(444, 548, ["入射角 ＜ 屈折角", "法線から遠ざかるように曲がる"], 17, INK, 1.5))
    b += panel(800, "3", "水 → 空気（全反射）", "空気", "水", 60, "out")
    b.append(lines(820, 548, [f"入射角が臨界角（約{CRIT_W:.1f}°）より", "大きいと、すべて反射する"], 17, INK, 1.5))
    return svg("".join(b), "光の反射・屈折・全反射のしくみ",
               "角度は境界面に垂直な線（法線）からはかる。うすい線は境界面で一部だけ反射した光。反射角＝入射角。")


def fig2():
    b = []
    b.append(text(60, 122, "入射角と屈折角の関係", 19, INK, 700))
    x0, y0, w, h = 112, 560, 400, 392
    X = lambda a: x0 + a / 90 * w
    Y = lambda a: y0 - a / 90 * h
    b.append(axes(x0, y0, w, h, "入射角", "屈折角", [(a / 90 * w, f"{a}°") for a in range(0, 91, 30)],
                  [(a / 90 * h, f"{a}°") for a in range(0, 91, 30)], 15))
    b.append(line(X(0), Y(0), X(90), Y(90), MUTED, 1.6, "3 5"))
    b.append(text(X(62), Y(62) + 24, "入射角＝屈折角", 14, MUTED, anchor="middle", transform=f"rotate(-44.4 {X(62):.1f} {Y(62) + 24:.1f})"))
    curves = [(1.0, NW, ACC, None), (1.0, NGL, ACC, "8 5"), (NW, 1.0, TEAL, None), (NGL, 1.0, TEAL, "8 5")]
    for n1, n2, col, dash in curves:
        pts, a = [], 0.0
        amax = 89.9 if n1 < n2 else math.degrees(math.asin(n2 / n1))
        while a <= amax + 1e-9:
            r = refr(n1, n2, a); pts.append((X(a), Y(r))); a += 0.5
        if n1 > n2: pts.append((X(amax), Y(90)))
        b.append(poly(pts, col, 3, dash=dash))
    for c, lab in [(CRIT_W, "水"), (CRIT_G, "ガラス")]:
        b.append(line(X(c), Y(90), X(c), y0, TEAL, 1.2, "2 4") + circle(X(c), Y(90), 5, TEAL, CARD, 2))
    b.append(text(X(CRIT_G) - 8, Y(90) - 10, f"{CRIT_G:.1f}°", 14, TEAL, 700, "end"))
    b.append(text(X(CRIT_W) + 8, Y(90) - 10, f"{CRIT_W:.1f}°", 14, TEAL, 700))
    b.append(text(X(54), Y(78), "ここから先は全反射", 15, TEAL_D, 700))
    lab = dict(stroke=BG, stroke_width=4, paint_order="stroke")
    b.append(text(X(23), Y(refr(NW, 1, 23)) - 10, "水→空気", 15, TEAL, 700, "end", **lab))
    b.append(text(X(26), Y(refr(NGL, 1, 26)) - 6, "ガラス→空気", 15, TEAL, 700, "end", **lab))
    b.append(text(X(88), Y(refr(1, NW, 88)) - 10, "空気→水", 15, ACC, 700, "end", **lab))
    b.append(text(X(88), Y(refr(1, NGL, 88)) + 24, "空気→ガラス", 15, ACC, 700, "end", **lab))
    b.append(text(60, 612, "点線の対角線より下＝屈折角が小さい（空気→水・ガラス）。上＝大きい（水・ガラス→空気）。", 14.5, INK2))
    # 右：早見表
    rows = []
    for a in (0, 10, 20, 30, 40, 45, 50, 60, 70, 80):
        o1, o2 = refr(NW, 1, a), refr(NGL, 1, a)
        rows.append([f"{a}°", deg(refr(1, NW, a)), deg(refr(1, NGL, a)), "全反射" if o1 is None else deg(o1), "全反射" if o2 is None else deg(o2)])
    b.append(table(612, 104, ["入射角", "空気→水", "空気→ガラス", "水→空気", "ガラス→空気"], rows, [80, 110, 120, 110, 120], 38, 15.5))
    b.append(text(612, 552, f"臨界角：水 約{CRIT_W:.1f}°・ガラス 約{CRIT_G:.1f}°", 16, INK, 700))
    b.append(text(612, 582, "n₁ sin i ＝ n₂ sin r（屈折率：空気1.00・水1.33・ガラス1.50）", 15, INK2))
    return svg("".join(b), "入射角と屈折角の早見表（グラフと表）",
               "数値は屈折率 水1.33・ガラス1.50 で計算（スネルの法則・高校の発展）。中学では入射角と屈折角の大小の関係をおさえる。")


FIGS = [
    dict(svg=fig1, alt="光の反射と屈折の図。空気から水へ入射角40°で進む光は屈折角28.9°で法線に近づくように曲がり、水から空気へ入射角30°で進む光は屈折角41.7°で法線から遠ざかるように曲がり、水から空気へ入射角60°で進む光は臨界角（約48.8°）より大きいので全反射することを、入射角・反射角・屈折角の弧とともに示す。",
         caption="反射・屈折・全反射。空気→水では入射角＞屈折角、水→空気では入射角＜屈折角になる。"),
    dict(svg=fig2, alt="入射角と屈折角の関係のグラフと早見表。空気→水・空気→ガラスでは屈折角が入射角より小さく、水→空気・ガラス→空気では大きくなり、臨界角（水 約48.8°・ガラス 約41.8°）より大きい入射角では全反射になる。入射角0°〜80°の屈折角の表つき。",
         caption="入射角と屈折角の早見表（屈折率 水1.33・ガラス1.50）。臨界角より大きいと全反射になる。"),
]
