"""カムとベルト・プーリ（kamu-pulley）の授業用の図（中学 技術・家庭 技術分野「動力伝達の機構」）。
数値・形はシミュ（scripts/rika/sims_karada_gijutsu.py の KAMU_JS）と同じ式：
  速度伝達比 i＝従動プーリの直径÷原動プーリの直径、従動プーリの回転数＝原動プーリの回転数×d1÷d2、
  ベルトの形 beltPath（平行掛け／十字掛け）、カムの半径 camR（偏心40mm円板・卵形 R0＝30/rs＝12・ハート形 22mm＋差）、
  従動節の高さ＝camR(π−回転角)−最小半径。"""
import math
from figlib import *

TAU = 2 * math.pi


# ---------------- ベルトとプーリ
def belt_pts(AX, BX, PY, r1, r2, cross):
    """シミュの beltPath と同じ（y は下向き）"""
    d = BX - AX
    ph = math.acos(max(-1, min(1, ((r1 + r2) if cross else (r1 - r2)) / d)))
    pts = []

    def arc(cx, r, a0, a1, n=72):
        for k in range(n + 1):
            a = a0 + (a1 - a0) * k / n
            pts.append((cx + r * math.cos(a), PY + r * math.sin(a)))
    arc(AX, r1, ph, TAU - ph)
    if cross:
        arc(BX, r2, math.pi - ph, -math.pi + ph)
    else:
        arc(BX, r2, -ph, ph)
    pts.append(pts[0])
    return pts


def pulley(cx, cy, r, fill, edge):
    out = [circle(cx, cy, r, fill, edge, 2.4), circle(cx, cy, max(9, r * 0.62), "none", edge, 1).replace("<circle", '<circle opacity=".45"')]
    hub = min(9, r * 0.35)
    for k in range(4):
        a = -math.pi / 2 + k * math.pi / 2 + math.pi / 4
        out.append(line(cx + hub * math.cos(a), cy + hub * math.sin(a), cx + (r - 5) * math.cos(a), cy + (r - 5) * math.sin(a), edge, 3))
    mr = max(r * 0.68, r - 12)
    out.append(circle(cx, cy - mr, max(4, min(7, r * 0.13)), ACC, ACC, 0))     # 赤い●（回った数を数える印）
    out.append(circle(cx, cy, hub, INK2, INK2, 0) + circle(cx, cy, 2.5, "#fff", "#fff", 0))
    return "".join(out)


def rot_arrow(cx, cy, R, d0, d1, color, mk):
    """回る向きの矢印。d0→d1（度、y 下向きの角度）。d1＞d0 なら時計回り。ベルトが巻きついている側の外にかく"""
    a0, a1 = math.radians(d0), math.radians(d1)
    x0, y0 = cx + R * math.cos(a0), cy + R * math.sin(a0)
    x1, y1 = cx + R * math.cos(a1), cy + R * math.sin(a1)
    return (f'<path d="M{x0:.1f},{y0:.1f} A{R},{R} 0 0 {1 if d1 > d0 else 0} {x1:.1f},{y1:.1f}" fill="none" stroke="{color}" '
            f'stroke-width="2.6" marker-end="url(#ah-{mk})"/>')


def fig1():
    d1, d2, n1 = 20, 60, 1200
    i = d2 / d1
    n2 = n1 * d1 / d2                                  # シミュ：n2＝n1×d1÷d2
    AX, BX, PY, KS = 180, 540, 268, 3.6
    r1, r2 = d1 / 2 * KS, d2 / 2 * KS
    b = []
    b.append(text((AX + BX) / 2, 118, "平行掛け：どちらも時計回り（同じ向き）", 17, INK, 700, "middle"))
    b.append(pulley(AX, PY, r1, TEAL_L, TEAL) + pulley(BX, PY, r2, GOLD_L, GOLD))
    b.append(poly(belt_pts(AX, BX, PY, r1, r2, False), INK, 7))
    b.append(rot_arrow(AX, PY, r1 + 16, 140, 225, TEAL, "teal") + rot_arrow(BX, PY, r2 + 16, -45, 35, GOLD, "gold"))
    # ベルトの動く向き（上側は右へ）
    ty = PY - r1 - 52
    b.append(arrow(AX + 70, ty + 8, AX + 150, ty - 2, "ink", 2))
    b.append(text(AX + 70, ty - 14, "ベルト", 15, INK2, 700))
    ly = PY + r2 + 38
    for cx, col, nm, dd, nn in [(AX, TEAL_D, "原動プーリ", d1, n1), (BX, GOLD, "従動プーリ", d2, n2)]:
        b.append(text(cx, ly, nm, 19, col, 700, "middle"))
        b.append(text(cx, ly + 26, f"直径 {dd}mm", 17, INK, 700, "middle"))
        b.append(text(cx, ly + 52, f"1分間に {nn:,.0f}回転", 17, INK, 700, "middle"))
    b.append(text(AX, PY - r1 - 26, "（モーターで回す）", 14, TEAL_D, anchor="middle"))

    # 右：十字掛け
    X0 = 730
    b.append(rect(X0, 104, 422, 330, CARD, LINE, 10))
    b.append(text(X0 + 20, 136, "十字掛け（たすき掛け）", 18, INK, 700))
    cA, cB, cy, q1, q2 = X0 + 90, X0 + 300, 262, 22, 66
    b.append(pulley(cA, cy, q1, TEAL_L, TEAL) + pulley(cB, cy, q2, GOLD_L, GOLD))
    b.append(poly(belt_pts(cA, cB, cy, q1, q2, True), INK, 5))
    b.append(rot_arrow(cA, cy, q1 + 14, 140, 225, TEAL, "teal") + rot_arrow(cB, cy, q2 + 14, 40, -40, GOLD, "gold"))
    b.append(text(cA, cy + 62, "時計回り", 15, TEAL_D, 700, "middle"))
    b.append(text(cB, cy + 92, "反時計回り", 15, GOLD, 700, "middle"))
    b.append(text(X0 + 20, 400, "ベルトを交差させると、逆向きに回る", 17, ACC, 700))

    # 下：式
    b.append(rect(48, 474, 1104, 146, TEAL_L, LINE, 10))
    b.append(text(70, 506, f"速度伝達比 ＝ 従動プーリの直径 ÷ 原動プーリの直径 ＝ {d2} ÷ {d1} ＝ {i:g}", 20, INK, 700))
    b.append(text(70, 538, f"　　　　　 ＝ 原動プーリの回転数 ÷ 従動プーリの回転数 ＝ {n1:,} ÷ {n2:,.0f} ＝ {n1 / n2:g}", 20, INK, 700))
    b.append(text(70, 572, f"従動プーリの回転数 ＝ 原動プーリの回転数 ÷ 速度伝達比 ＝ {n1:,} ÷ {i:g} ＝ {n2:,.0f}回/分", 17, INK2, 700))
    b.append(text(70, 604, "わけ：ベルトはすべらないので、「直径 × 3.14 × 回転数」（ふちが1分間に進む長さ）がどちらのプーリでも同じ。", 16, INK2))
    return svg("".join(b), "ベルトとプーリのしくみ（速度伝達比と回転数）",
               "速度伝達比が1より大きいと、従動プーリはゆっくり回り、回す力（トルク）は大きくなる（損失を考えないとき約3倍）。")


# ---------------- カム機構
def camR(phi, sh, p):
    a = ((phi % TAU) + 3 * math.pi) % TAU - math.pi
    if sh == "ecc":
        R, e = 40, p
        return e * math.cos(a) + math.sqrt(R * R - e * e * math.sin(a) ** 2)
    if sh == "heart":
        return 22 + p * (1 - abs(a) / math.pi)
    R0, rs = 30, 12
    cc = R0 + p - rs
    al = math.acos((R0 - rs) / cc)
    be = math.atan2(rs * math.sin(al), cc + rs * math.cos(al))
    bb = abs(a)
    if bb >= al:
        return R0
    if bb >= be:
        return R0 / math.cos(bb - al)
    return cc * math.cos(bb) + math.sqrt(max(0, rs * rs - cc * cc * math.sin(bb) ** 2))


def egg_dwell(p):
    R0, rs = 30, 12
    return 1 - math.acos((R0 - rs) / (R0 + p - rs)) / math.pi


CAMS = [("ecc", 10, "円形（偏心カム）"), ("egg", 20, "卵形カム"), ("heart", 20, "ハート形カム")]   # シミュの初期値


def samples(sh, p):
    return [camR(math.pi - k / 720 * TAU, sh, p) for k in range(721)]


def fig2():
    b = []
    KC, OY = 1.55, 300
    for ci, (sh, p, nm) in enumerate(CAMS):
        cx = 220 + ci * 380
        S = samples(sh, p)
        rmin, rmax = min(S), max(S)
        stroke = rmax - rmin
        b.append(text(cx, 128, nm, 19, INK, 700, "middle"))
        # カム（回転角0の位置：いちばん短い半径が従動節の下）
        pts = []
        for k in range(241):
            ph = k / 240 * TAU
            r = camR(ph, sh, p) * KC
            ps = ph - 1.5 * math.pi
            pts.append((cx + r * math.cos(ps), OY + r * math.sin(ps)))
        b.append(poly(pts, INK2, 2.4, "#e7e3da"))
        if sh == "ecc":
            ey = OY + p * KC
            b.append(line(cx, OY, cx, ey, ACC, 1.6, "3 3") + line(cx - 7, ey, cx + 7, ey, ACC, 2.2) + line(cx, ey - 7, cx, ey + 7, ACC, 2.2))
        if sh == "egg":
            b.append(circle(cx, OY, 30 * KC, "none", MUTED, 1.2).replace("/>", ' stroke-dasharray="4 4"/>'))
        b.append(circle(cx, OY, 7, INK2, INK2, 0) + circle(cx, OY, 2.4, "#fff", "#fff", 0))
        R = rmax * KC + 12
        a0, a1 = math.pi * 0.82, math.pi * 1.18
        b.append(f'<path d="M{cx + R * math.cos(a0):.1f},{OY + R * math.sin(a0):.1f} A{R:.1f},{R:.1f} 0 0 1 {cx + R * math.cos(a1):.1f},{OY + R * math.sin(a1):.1f}" '
                 f'fill="none" stroke="{TEAL}" stroke-width="2.6" marker-end="url(#ah-teal)"/>')
        # 従動節
        tip = OY - rmin * KC
        b.append(line(cx, tip - 4, cx, tip - 100, MUTED, 9) + line(cx, tip - 4, cx, tip - 100, "#d7d3ca", 5))
        b.append(circle(cx, tip - 3, 4.5, INK2, INK2, 0))
        b.append(rect(cx - 26, tip - 70, 15, 16, LINE, MUTED, 3) + rect(cx + 11, tip - 70, 15, 16, LINE, MUTED, 3))
        b.append(text(cx + 32, tip - 76, "従動節", 15, INK, 700))
        b.append(text(cx - 60, OY - 70, "カム", 15, TEAL_D, 700, "end"))
        b.append(text(cx - 60, OY - 52, "（原動節）", 14, TEAL_D, 700, "end"))
        # グラフ
        gx0, gx1, gy0, H = cx - 130, cx + 150, 522, 84
        sy = H / 20
        b.append(f'<rect x="{gx0}" y="{gy0 - H}" width="{gx1 - gx0}" height="{H}" fill="{CARD}" stroke="{LINE}"/>')
        if sh == "egg":
            al_deg = math.degrees(math.acos(18 / (30 + p - 12)))
            for g0, g1 in [(0, 180 - al_deg), (180 + al_deg, 360)]:
                x0 = gx0 + g0 / 360 * (gx1 - gx0); x1 = gx0 + g1 / 360 * (gx1 - gx0)
                b.append(f'<rect x="{x0:.1f}" y="{gy0 - H}" width="{x1 - x0:.1f}" height="{H}" fill="{GOLD_L}"/>')
            b.append(text(gx0 + (180 - al_deg) / 720 * (gx1 - gx0), gy0 - H + 22, "止まる", 14, GOLD, 700, "middle"))
            b.append(text(gx1 - (180 - al_deg) / 720 * (gx1 - gx0), gy0 - H + 22, "止まる", 14, GOLD, 700, "middle"))
        for mm in (10, 20):
            b.append(line(gx0, gy0 - mm * sy, gx1, gy0 - mm * sy, LINE, 1))
        for dg in (90, 180, 270):
            b.append(line(gx0 + dg / 360 * (gx1 - gx0), gy0 - H, gx0 + dg / 360 * (gx1 - gx0), gy0, LINE, 1))
        b.append(poly([(gx0 + k / 720 * (gx1 - gx0), gy0 - (r - rmin) * sy) for k, r in enumerate(S)], TEAL, 3))
        b.append(line(gx0, gy0, gx1, gy0, INK, 1.6) + line(gx0, gy0 - H, gx0, gy0, INK, 1.6))
        for mm in (0, 10, 20):
            b.append(text(gx0 - 6, gy0 - mm * sy + 5, f"{mm}", 14, INK2, anchor="end"))
        b.append(text(gx0 - 30, gy0 - H - 12, "従動節の高さ（mm）", 14, INK2, 700))
        for dg in (0, 90, 180, 270, 360):
            b.append(text(gx0 + dg / 360 * (gx1 - gx0), gy0 + 20, f"{dg}°", 14, INK2, anchor="middle"))
        if sh == "ecc":
            d1, d2 = "なめらかに上下する", f"上下の幅 ＝ 中心のずれ{p}mm × 2 ＝ {stroke:.0f}mm"
        elif sh == "egg":
            d1, d2 = f"1回転の約{round(egg_dwell(p) * 100)}%は止まっている", "とがった部分が来たときだけ上下する"
        else:
            d1, d2 = "一定の速さで上がり、下がる", "グラフが直線（三角の形）になる"
        b.append(text(cx + 10, 572, d1, 16, INK, 700, "middle"))
        b.append(text(cx + 10, 598, d2, 15, INK2, anchor="middle"))
    return svg("".join(b), "カムの形と従動節の動き（3つのカムをくらべる）",
               "カムが時計回りに1回転すると、従動節は1回上下する（上下の幅はどれも20mm）。グラフの横軸はカムの回転角。")


FIGS = [
    dict(svg=fig1, alt="ベルトとプーリのしくみの図。直径20mmの原動プーリと直径60mmの従動プーリを平行掛けのベルトでつなぐと、速度伝達比は従動プーリの直径÷原動プーリの直径＝3で、原動プーリが1分間に1,200回転すると従動プーリは400回転する。十字掛けでは回る向きが逆になることも示す。",
         caption="ベルトとプーリの速度伝達比と回転数。速度伝達比＝従動プーリの直径÷原動プーリの直径＝原動の回転数÷従動の回転数。"),
    dict(svg=fig2, alt="カム機構で、円形（偏心カム）・卵形カム・ハート形カムの3つの形と、カムの回転角に対する従動節の高さのグラフをくらべた図。偏心カムはなめらかに上下し、卵形カムは1回転の約66%は止まっていて、ハート形カムは一定の速さで上がって下がる。",
         caption="カムの形と従動節の動きのくらべ。カム（原動節）の形で、従動節の上下の仕方が変わる。"),
]
