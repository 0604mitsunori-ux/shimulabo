"""磁力線シミュレーター（magnet）の図。
磁力線と方位磁針の向きは、ページの JS と同じモデル（棒磁石の両はしにN極（＋1）とS極（−1）を置き、
各点の磁界 ＝ Σ 極 × (dx, dy) ÷ r³、r＝距離＋10（JSの単位。図では磁石の長さに合わせて拡大））で計算する。"""
import math
from figlib import *

N_COL, S_COL = ACC, TEAL          # 学校の棒磁石と同じく N＝赤、S＝青（文字でも区別）

CX, CY, D = 392, 372, 140          # 磁石の中心と、中心から極までのきょり（px）
SOFT = 10 * D / 64                 # JS（d=64, +10）と同じ比率


def field(x, y):
    fx = fy = 0.0
    for px, q in ((CX - D, 1), (CX + D, -1)):
        dx, dy = x - px, y - CY
        r = math.hypot(dx, dy) + SOFT
        fx += q * dx / r ** 3; fy += q * dy / r ** 3
    return fx, fy


def trace(a0, box=(48, 100, 740, 624)):
    """N極のすぐそばの角度 a0（度）から、磁界の向きに線をたどる"""
    x, y = CX - D + 6 * math.cos(math.radians(a0)), CY + 6 * math.sin(math.radians(a0))
    pts = [(x, y)]
    for _ in range(6000):
        fx, fy = field(x, y); m = math.hypot(fx, fy)
        if m == 0: break
        x += 2 * fx / m; y += 2 * fy / m
        pts.append((x, y))
        if math.hypot(x - (CX + D), y - CY) < 5: break
        if not (box[0] - 400 < x < box[2] + 400 and box[1] - 400 < y < box[3] + 400): break
    return pts


def needle(x, y, ang, r=17):
    """方位磁針。ang＝N極（色つき）の向き（ラジアン）"""
    c, s = math.cos(ang), math.sin(ang)
    w = r * 0.32
    tip = (x + c * (r - 3), y + s * (r - 3)); tail = (x - c * (r - 3), y - s * (r - 3))
    l = (x - s * w, y + c * w); rr = (x + s * w, y - c * w)
    out = circle(x, y, r, CARD, INK2, 1.4)
    out += f'<path d="M{tip[0]:.1f},{tip[1]:.1f} L{l[0]:.1f},{l[1]:.1f} L{rr[0]:.1f},{rr[1]:.1f}Z" fill="{N_COL}"/>'
    out += f'<path d="M{tail[0]:.1f},{tail[1]:.1f} L{l[0]:.1f},{l[1]:.1f} L{rr[0]:.1f},{rr[1]:.1f}Z" fill="{CARD}" stroke="{INK2}" stroke-width="1"/>'
    return out


def bar(cx, cy, d, h, ang=0.0, letters=True):
    t = f' transform="rotate({ang:.2f} {cx:.1f} {cy:.1f})"' if ang else ""
    return (f'<g{t}><rect x="{cx - d:.1f}" y="{cy - h / 2:.1f}" width="{d:.1f}" height="{h:.1f}" fill="{N_COL}"/>'
            f'<rect x="{cx:.1f}" y="{cy - h / 2:.1f}" width="{d:.1f}" height="{h:.1f}" fill="{S_COL}"/>'
            f'<rect x="{cx - d:.1f}" y="{cy - h / 2:.1f}" width="{2 * d:.1f}" height="{h:.1f}" fill="none" stroke="{INK}" stroke-width="1.6"/>'
            + ("" if not letters else f'<text x="{cx - d / 2:.1f}" y="{cy + h * 0.3:.1f}" font-size="{h * 0.8:.0f}" fill="#fff" font-weight="700" text-anchor="middle">N</text>'
            f'<text x="{cx + d / 2:.1f}" y="{cy + h * 0.3:.1f}" font-size="{h * 0.8:.0f}" fill="#fff" font-weight="700" text-anchor="middle">S</text>') + '</g>')


def runs_inside(pts, box):
    """枠の中に入っている、ひと続きの部分ごとに分ける"""
    out, cur = [], []
    for p in pts:
        if box[0] < p[0] < box[2] and box[1] < p[1] < box[3]: cur.append(p)
        elif cur: out.append(cur); cur = []
    if cur: out.append(cur)
    return out


def mid_arrow(pts, frac=0.5, fdir=None):
    """線の途中に向きの矢印。fdir があれば、その点の磁界の向き（計算）で矢印を向ける"""
    i = max(1, min(len(pts) - 2, int(len(pts) * frac)))
    (x0, y0), (x1, y1) = pts[i - 1], pts[i + 1]
    x, y = pts[i]
    a = math.atan2(*fdir(x, y)[::-1]) if fdir else math.atan2(y1 - y0, x1 - x0)
    c, s = math.cos(a), math.sin(a)
    p1 = (x + 8 * c, y + 8 * s); p2 = (x - 6 * c - 6 * s, y - 6 * s + 6 * c); p3 = (x - 6 * c + 6 * s, y - 6 * s - 6 * c)
    return f'<path d="M{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} L{p3[0]:.1f},{p3[1]:.1f}Z" fill="{INK2}"/>'


def fig1():
    clip = '<clipPath id="mclip"><rect x="48" y="100" width="692" height="524"/></clipPath>'
    b = ['<g clip-path="url(#mclip)">']
    arrows = []
    for i in range(18):
        a0 = 360 / 18 * (i + 0.5)
        if abs(((a0 + 180) % 360) - 180) < 25: continue        # 磁石の中を通る線は描かない
        pts = trace(a0)
        b.append(poly(pts, INK2, 1.5))
        rs = runs_inside(pts, (60, 112, 728, 612))
        if rs:
            run = max(rs, key=len)
            if len(run) > 20: arrows.append(mid_arrow(run, 0.5, field))
    b.append("".join(arrows) + "</g>")
    b.append(bar(CX, CY, D, 40))
    # 方位磁針（その場所の磁界の向きにN極を向ける）
    for x, y in [(160, CY), (624, CY), (CX, 222), (CX, 522), (228, 210), (556, 210), (228, 534), (556, 534), (CX, 140), (CX, 604)]:
        fx, fy = field(x, y)
        b.append(needle(x, y, math.atan2(fy, fx)))
    # 番号（右のきまりと対応）
    b.append(badge(CX + 34, 176, "1", ACC))
    b.append(badge(118, 252, "2", ACC))
    b.append(badge(CX - D - 34, CY - 50, "3", ACC))
    X = 770
    b.append(text(X, 128, "磁力線の3つのきまり", 19, INK, 700))
    rules = [("1", "N極から出て、S極に入る", ["矢印の向き＝その場所の磁界の向き。", "方位磁針の色のついたN極がさす向き。"]),
             ("2", "とちゅうで交わらない", ["1つの場所の磁界の向きは1つに", "決まるので、線は交わらない。"]),
             ("3", "こみ合うところほど強い", ["線が密な両はし（極）の近くほど", "磁力が強い。"])]
    yy = 172
    for no, h, rows in rules:
        b.append(badge(X + 14, yy - 6, no, ACC))
        b.append(text(X + 38, yy, h, 17.5, INK, 700))
        b.append(lines(X + 38, yy + 30, rows, 15.5, INK2, 1.5))
        yy += 124
    b.append(needle(X + 20, 560, 0.0) + text(X + 46, 566, "方位磁針：色のついた方がN極", 15, INK2))
    return svg("".join(b), "棒磁石のまわりの磁力線と方位磁針",
               "方位磁針は、置いた場所の磁力線の向きにN極を向ける。磁石の中では、磁力線はS極からN極へ向かう。", clip)


def fig2():
    ex, ey, R = 330, 372, 112
    tilt = 10                                                    # 磁石のかたむき（度・目安）
    clip = '<clipPath id="eclip"><rect x="48" y="100" width="640" height="524"/></clipPath>'
    b = ['<g clip-path="url(#eclip)">']
    # 磁軸（地理の北に近い向き）の単位ベクトル。画面は y が下向き
    ux, uy = math.sin(math.radians(tilt)), -math.cos(math.radians(tilt))
    vx, vy = -uy, ux                                             # 磁軸に垂直
    arrows = []
    for Lm in (1.45, 2.0, 2.8):
        for side in (1, -1):
            pts = []
            for k in range(1, 180):
                th = math.radians(k)                               # 磁気の北（S極側）からの角度
                r = Lm * R * math.sin(th) ** 2
                if r < R:
                    if pts: break
                    continue
                pts.append((ex + r * (math.cos(th) * ux + side * math.sin(th) * vx), ey + r * (math.cos(th) * uy + side * math.sin(th) * vy)))
            pts = pts[::-1]                                       # 南側から北側へ（磁力線の向き）
            b.append(poly(pts, INK2, 1.5))
            rs = runs_inside(pts, (60, 112, 676, 612))
            if rs:
                run = max(rs, key=len)
                if len(run) > 10: arrows.append(mid_arrow(run, 0.5))
    b.append("".join(arrows) + "</g>")
    b.append(circle(ex, ey, R, "#dbe9f2", TEAL, 2))
    b.append(line(ex, ey - R - 34, ex, ey + R + 34, MUTED, 1.4, "6 5"))
    b.append(text(ex, ey - R - 44, "北極（地理）", 16, INK, 700, "middle"))
    b.append(text(ex, ey + R + 58, "南極（地理）", 16, INK, 700, "middle"))
    b.append(bar(ex, ey, 64, 30, ang=-90 + tilt, letters=False))
    for sgn, t in ((1, "S"), (-1, "N")):
        lx, ly = ex + sgn * 34 * ux, ey + sgn * 34 * uy
        b.append(text(lx, ly + 8, t, 22, "#fff", 700, "middle"))
    # 日本あたり（北緯35°）の方位磁針：地面にそって北をさす
    lat = math.radians(35)
    jx, jy = ex + R * math.cos(lat), ey - R * math.sin(lat)
    b.append(needle(jx + 26 * math.cos(lat), jy - 26 * math.sin(lat), math.atan2(-math.cos(lat), -math.sin(lat)), 18))
    b.append(line(jx + 40, jy - 44, jx + 62, jy - 70, MUTED, 1.2))
    b.append(text(jx + 66, jy - 96, "日本の方位磁針", 15, INK, 700))
    b.append(text(jx + 66, jy - 74, "N極は北をさす", 15, ACC, 700))
    X = 720
    b.append(text(X, 132, "地球は大きな磁石", 19, INK, 700))
    b.append(lines(X, 172, ["方位磁針のN極が北をさすのは、", "地球の北極の近くに、磁石としての", "S極があるから（N極とS極は引き合う）。"], 16, INK, 1.55))
    b.append(rect(X, 270, 432, 166, CARD, LINE, 10))
    b.append(lines(X + 18, 304, ["・磁石の向きは、地軸から少しかたむいている。",
                                 "・日本では、方位磁針の北が真北から",
                                 "　西へ約7〜9°ずれる（偏角）。",
                                 "・磁極は毎年少しずつ動き、数十万年",
                                 "　ごとに南北が入れかわることもある。"], 15.5, INK2, 1.65))
    b.append(lines(X, 478, ["地球のまわりの磁力線も、", "南極側（磁石のN極）から出て、", "北極側（磁石のS極）に入る。"], 15.5, INK, 1.55))
    return svg("".join(b), "地球は大きな磁石（北極側がS極）",
               "地球の中の棒磁石は、磁界の向きを表す模式図（大きさ・かたむきは実際とちがう）。", clip)


FIGS = [
    dict(svg=fig1, alt="棒磁石のまわりの磁力線と方位磁針の図。磁力線はN極から出てS極に入り、とちゅうで交わらず、両はしの極の近くほど線がこみ合って磁力が強いという磁力線の3つのきまりと、各場所の方位磁針のN極が磁力線の向きをさすことを示す。",
         caption="棒磁石のまわりの磁力線。N極から出てS極に入り、交わらず、極の近くほどこみ合う。"),
    dict(svg=fig2, alt="地球は大きな磁石であることを示す図。地球の中に北極側がS極、南極側がN極の棒磁石があるとみなせ、地球のまわりの磁力線が南極側から北極側へ向かうことと、日本の方位磁針のN極が北をさすこと、偏角（西へ約7〜9°）を説明している。",
         caption="地球は大きな磁石。北極の近くに磁石のS極があるので、方位磁針のN極は北をさす。"),
]
