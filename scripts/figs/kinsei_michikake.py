"""金星の満ち欠けと見え方（kinsei-michikake）の授業用の図
   数値はページの JS（scripts/rika/sims_kinsei.py）の円軌道モデルと同じ式：
   金星 0.723 天文単位・224.701日、地球 1 天文単位・365.256日。geo()：離角・位相角 i・光っている部分 k＝(1＋cos i)/2・
   距離 d・見かけの大きさ＝1.723÷d（外合のころ＝1）。内合の30日前・後は、30日×(360/224.701−360/365.256)° ずらした位置。"""
import math
from figlib import *

AV = 0.723
NV, NE = 360 / 224.701, 360 / 365.256
SUP = 1 + AV
REL30 = 30 * (NV - NE)                               # 30日で金星が地球より先に進む角度（太陽から見て）
PSI_MAX = math.degrees(math.acos(AV))                # 最大離角のときの太陽から見た角
ELONG_MAX = math.degrees(math.asin(AV))              # 最大離角


def geo(tv):
    """地球を (0,−1) に置き、金星を太陽から見た角度 tv（度・反時計回り）に置いたときの値"""
    V = (AV * math.cos(math.radians(tv)), AV * math.sin(math.radians(tv))); E = (0.0, -1.0)
    g = (V[0] - E[0], V[1] - E[1]); s = (-E[0], -E[1]); d = math.hypot(*g)
    el = math.degrees(math.acos(max(-1, min(1, (g[0] * s[0] + g[1] * s[1]) / (d * math.hypot(*s))))))
    if s[0] * g[1] - s[1] * g[0] < 0: el = -el
    ci = (V[0] * g[0] + V[1] * g[1]) / (AV * d)
    return dict(el=el, i=math.degrees(math.acos(max(-1, min(1, ci)))), k=(1 + ci) / 2, d=d, size=SUP / d, V=V)


POS = [("①", "外合", 90), ("②", "東方最大離角", 270 - PSI_MAX), ("③", "内合の約30日前", 270 - REL30),
       ("④", "内合", 270), ("⑤", "内合の約30日後", 270 + REL30), ("⑥", "西方最大離角", 270 + PSI_MAX)]


def venus_look(cx, cy, r, g):
    """地球から見た金星の形（夕方＝太陽の東側は右側が光る、明け方は左側）"""
    if g["k"] < 0.005:
        return circle(cx, cy, r, MOON_D, MUTED, 1).replace('stroke-width="1"', 'stroke-width="1" stroke-dasharray="3 3"')
    th = 180 - g["i"] if g["el"] >= 0 else 180 + g["i"]
    return moon_look(cx, cy, r, th)


def half_lit_toward(cx, cy, r, sx, sy):
    """宇宙から見た金星：太陽 (sx, sy) の側の半分が光る"""
    a = math.atan2(sy - cy, sx - cx); px, py = -math.sin(a), math.cos(a)
    p1 = (cx + r * px, cy + r * py); p2 = (cx - r * px, cy - r * py)
    return (circle(cx, cy, r, MOON_D, MOON_D, 0)
            + f'<path d="M{p1[0]:.1f},{p1[1]:.1f} A{r},{r} 0 0 0 {p2[0]:.1f},{p2[1]:.1f}Z" fill="{SUN}"/>')


def fig1():
    b = []
    sx, sy, RE = 300, 328, 200
    RV = RE * AV
    E = (sx, sy + RE)
    b.append(text(48, 128, "北極の上から見た太陽・金星・地球", 18, INK, 700))
    b.append(f'<path d="M{sx - RE * 0.62:.1f},{sy + RE * 0.785:.1f} A{RE},{RE} 0 0 0 {sx + RE * 0.62:.1f},{sy + RE * 0.785:.1f}" fill="none" stroke="{MUTED}" stroke-width="1.4" stroke-dasharray="5 5"/>')
    b.append(text(sx - 120, sy + math.sqrt(RE * RE - 120 * 120) + 22, "地球の軌道", 14, MUTED, anchor="middle"))
    b.append(circle(sx, sy, RV, "none", TEAL, 1.6) + text(sx - RV * 0.72 - 6, sy - RV * 0.72 - 6, "金星の軌道", 14, TEAL, 700, "end"))
    # 最大離角の接線（地球から金星の軌道に引いた線）
    tips = []
    for sgn in (-1, 1):
        g = geo(270 + sgn * PSI_MAX); vx, vy = sx + g["V"][0] * RE, sy - g["V"][1] * RE
        ex, ey = vx + (vx - E[0]) * 0.55, vy + (vy - E[1]) * 0.55
        b.append(line(E[0], E[1], ex, ey, MUTED, 1.3, "6 4")); tips.append((ex, ey))
    b.append(line(E[0], E[1], sx, sy + 34, GOLD, 1.3, "6 4"))
    rr_ = 112; a0 = -math.pi / 2; a1 = a0 - math.radians(ELONG_MAX)
    b.append(f'<path d="M{E[0] + rr_ * math.cos(a0):.1f},{E[1] + rr_ * math.sin(a0):.1f} A{rr_},{rr_} 0 0 0 {E[0] + rr_ * math.cos(a1):.1f},{E[1] + rr_ * math.sin(a1):.1f}" fill="none" stroke="{ACC}" stroke-width="2"/>')
    am = (a0 + a1) / 2
    b.append(text(E[0] + 136 * math.cos(am) + 4, E[1] + 136 * math.sin(am) + 4, f"{ELONG_MAX:.0f}°", 16, ACC, 700, "middle"))
    b.append(circle(sx, sy, 28, SUN, GOLD, 2) + text(sx, sy + 6, "太陽", 15, "#7a5a10", 700, "middle"))
    b.append(circle(E[0], E[1], 13, "#2f4f6b", "#fff", 1.5) + f'<path d="M{E[0] - 13},{E[1]} A13,13 0 0 1 {E[0] + 13},{E[1]}Z" fill="{SKY}"/>'
             + text(E[0] + 20, E[1] + 6, "地球", 16, INK, 700))
    for no, nm, tv in POS:
        g = geo(tv); vx, vy = sx + g["V"][0] * RE, sy - g["V"][1] * RE
        b.append(half_lit_toward(vx, vy, 10, sx, sy))
        ux, uy = (vx - sx) / RV, (vy - sy) / RV
        k = 24 if no in ("①", "②", "⑥") else 22
        lx, ly = vx - ux * k, vy - uy * k + 7                     # 軌道の内側（太陽の側）に番号
        if no == "④": lx, ly = vx - 22, vy - 8
        if no == "③": lx, ly = vx - 8, vy - 22
        if no == "⑤": lx, ly = vx + 8, vy - 22
        b.append(text(lx, ly, no, 19, INK, 700, "middle"))
    b.append(text(48, 470, "太陽の東側", 16, ACC, 700) + text(48, 492, "→ 夕方に見える", 15, INK2))
    b.append(text(552, 470, "太陽の西側", 16, TEAL, 700, "end") + text(552, 492, "明け方に見える ←", 15, INK2, anchor="end"))
    b.append(lines(48, 578, [f"点線＝地球から金星の軌道に引いた接線（最大離角 約{ELONG_MAX:.0f}°）。",
                             "金星（約225日）も地球（約365日）も反時計回りに公転。大きさは誇張。",
                             "右の距離は天文単位（太陽と地球のきょり＝1）、大きさは①を1とした倍率。"], 14, MUTED, gap=1.3))
    # 右：地球から見た形と大きさ
    x0, y0 = 600, 112
    b.append(text(x0, y0 + 16, "地球から見た金星の形と大きさ（同じ倍率）", 18, INK, 700))
    cw, ch = 182, 236
    for j, (no, nm, tv) in enumerate(POS):
        g = geo(tv); col, row = j % 3, j // 3
        bx, by = x0 + col * (cw + 4), y0 + 30 + row * (ch + 6)
        b.append(rect(bx, by, cw, ch))
        b.append(text(bx + 12, by + 26, no, 19, INK, 700) + text(bx + 36, by + 26, nm, 15.5 if len(nm) <= 6 else 14.5, INK, 700))
        r = 7 * g["size"]
        b.append(venus_look(bx + cw / 2, by + 96, r, g))
        if g["k"] < 0.005:
            b.append(text(bx + cw / 2, by + 102, "見えない", 15, "#fff", 700, "middle"))
        sz = "1倍" if j == 0 else f"約{g['size']:.1f}倍"
        vis = "夕方の西の空" if g["el"] > 10 else "明け方の東の空" if g["el"] < -10 else "太陽と同じ方向"
        vcol = ACC if g["el"] > 10 else TEAL if g["el"] < -10 else MUTED
        b.append(text(bx + cw / 2, by + 160, f"距離 約{g['d']:.2f}", 14.5, INK2, anchor="middle"))
        b.append(text(bx + cw / 2, by + 181, f"大きさ {sz}", 14.5, INK2, anchor="middle"))
        b.append(text(bx + cw / 2, by + 202, f"光っている部分 {round(g['k'] * 100):d}%", 14.5, INK2, anchor="middle"))
        b.append(text(bx + cw / 2, by + 226, vis, 15, vcol, 700, "middle"))
    return svg("".join(b), "金星の満ち欠けのしくみ",
               "金星はいつも太陽の側の半分が光っている。地球に近いほど大きく、細く欠けて見える。")


def fig2():
    b = []
    # ---- 左：見える時刻（地上の観察者と地平線）----
    cx, cy, r = 280, 392, 84
    b.append(text(48, 128, "金星が見える時刻と、真夜中に見えないわけ", 18, INK, 700))
    b.append(arrow(cx, cy - r - 8, cx, 172, "gold", 2.4) + text(cx, 162, "太陽の方向", 15, GOLD, 700, "middle"))
    for sgn, col, nm, ox in ((1, ACC, "よいの明星", cx - r), (-1, TEAL, "明けの明星", cx + r)):
        a = math.radians(90 + sgn * ELONG_MAX); L = 150
        tx, ty = ox + L * math.cos(a), cy - L * math.sin(a)
        b.append(line(ox, cy, tx, ty, col, 2, "6 4"))
        b.append(circle(tx, ty, 9, SUN, col, 2))
        lx, anc = (48, "start") if sgn > 0 else (545, "end")
        b.append(text(lx, ty - 36, f"金星（{nm}）", 15, col, 700, anc) + text(lx, ty - 16, f"太陽から{'東' if sgn > 0 else '西'}へ最大約{ELONG_MAX:.0f}°", 14, col, anchor=anc))
    # 地球（上が昼）
    b.append(circle(cx, cy, r, "#2f4f6b", "#2f4f6b", 0) + f'<path d="M{cx - r},{cy} A{r},{r} 0 0 1 {cx + r},{cy}Z" fill="{SKY}"/>')
    b.append(text(cx, cy - 30, "昼", 18, "#14385a", 700, "middle") + text(cx, cy + 50, "夜", 18, "#fff", 700, "middle"))
    a0, a1, rr_ = math.radians(205), math.radians(245), 58
    b.append(f'<path d="M{cx + rr_ * math.cos(a0):.1f},{cy - rr_ * math.sin(a0):.1f} A{rr_},{rr_} 0 0 0 {cx + rr_ * math.cos(a1):.1f},{cy - rr_ * math.sin(a1):.1f}" fill="none" stroke="#fff" stroke-width="2.2"/>')
    hx, hy = cx + rr_ * math.cos(a1), cy - rr_ * math.sin(a1); tx_, ty_ = -math.sin(a1), -math.cos(a1)   # 反時計回りの向き（画面）
    b.append(f'<path d="M{hx + tx_ * 9:.1f},{hy + ty_ * 9:.1f} L{hx - ty_ * 5:.1f},{hy + tx_ * 5:.1f} L{hx + ty_ * 5:.1f},{hy - tx_ * 5:.1f}Z" fill="#fff"/>')
    b.append(text(cx - 6, cy + 24, "自転", 14, "#fff", 700, "end"))
    # 観察者と地平線
    for (ox, oy), (dx, dy), nm, sub, anc, lx, ly in (((cx - r, cy), (0, 1), "夕方", "西の空に見える", "end", cx - r - 12, cy + 30),
                                                     ((cx + r, cy), (0, 1), "明け方", "東の空に見える", "start", cx + r + 12, cy + 30),
                                                     ((cx, cy + r), (1, 0), "真夜中", "金星は地平線の下（見えない）", "middle", cx, cy + r + 34)):
        b.append(line(ox - dx * 104, oy - dy * 104, ox + dx * 104, oy + dy * 104, INK, 2.2))
        b.append(circle(ox, oy, 6, ACC, "#fff", 1.5))
        b.append(text(lx, ly, nm, 17, INK, 700, anc) + text(lx, ly + 22, sub, 15, INK2, anchor=anc))
    b.append(lines(48, 596, ["黒い線＝それぞれの時刻の観察者の地平線（地球の外側が空）。", "北極の上から見た図。大きさは誇張。"], 14, MUTED, gap=1.4))
    # ---- 右：早見表 ----
    x0 = 560
    b.append(text(x0, 128, "金星の位置と見え方（円軌道で計算）", 18, INK, 700))
    rows = []
    for no, nm, tv in POS:
        g = geo(tv)
        shape = "丸い" if g["k"] > 0.97 else "半月形" if abs(g["k"] - 0.5) < 0.03 else "見えない" if g["k"] < 0.01 else "三日月形"
        sky = "見えない（太陽の方向）" if abs(g["el"]) < 10 else ("よいの明星（夕方・西）" if g["el"] > 0 else "明けの明星（明け方・東）")
        rows.append([f"{no} {nm}", f"約{g['d']:.2f}", f"{shape}（{round(g['k'] * 100)}%）", "1倍" if no == "①" else f"約{g['size']:.1f}倍", sky])
    b.append(table(x0, 144, ["位置", "距離", "形（光る部分）", "大きさ", "見え方"], rows, [146, 60, 128, 70, 188], 46, 14.5))
    b.append(lines(x0, 488, [f"・地球から見ると、金星は太陽から最大でも約{ELONG_MAX:.0f}°しかはなれない",
                             "　→ 夕方の西の空か、明け方の東の空にしか見えない。",
                             f"・①→②→④→⑥→①と一周するのに約{360 / (NV - NE):.0f}日（約1年7か月）。",
                             "・距離は天文単位、大きさは①（外合のころ）を1とした倍率。"], 15, INK, gap=1.5))
    return svg("".join(b), "金星の見え方の早見表",
               "金星は地球より内側を回るので、真夜中には見えない。地球に近いほど大きく、細く欠けて見える。")


FIGS = [
    dict(svg=fig1, alt="北極の上から見た太陽・金星・地球の位置関係と、外合・東方最大離角・内合の約30日前・内合・内合の約30日後・西方最大離角の6つの位置で地球から見た金星の形と見かけの大きさを並べた金星の満ち欠けのしくみ図。最大離角は約46°。",
         caption="金星の満ち欠けのしくみ。地球に近づくほど大きく、細く欠けて見える。"),
    dict(svg=fig2, alt="夕方・明け方・真夜中の観察者の地平線と金星の方向から、金星がよいの明星（夕方の西の空）・明けの明星（明け方の東の空）として見え、真夜中には見えないことを示す図と、金星の位置ごとの地球からの距離・形・見かけの大きさ・見える時刻と方角の早見表。",
         caption="金星の見え方の早見表。太陽の東側にあると夕方の西の空、西側にあると明け方の東の空に見える。"),
]
