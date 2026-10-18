"""月食・日食（gesshoku-nisshoku）の授業用の図
   数値はページの JS（scripts/rika/sims_tenmon.py）と同じ式：
   - 影の大きさ（地球半径単位）：本影 0.7403−u、半影 1.2848+u、月の半径 0.2725（Meeus 54章。月までの距離が平均のとき u＝0.0059）
   - 食が起こる「ずれ」：月食 皆既(0.4678−u)・部分(1.0128−u)・半影(1.5573+u)、日食 中心食 0.9972・部分(1.5433+u) に
     月の地平視差 π＝asin(6378.14/384400) をかけた角度"""
import math
from figlib import *

# ---- ページの JS と同じ定数（平均距離）----
KM = 0.2725                                     # 月の半径（地球半径単位）
U = 0.0059                                      # 本影円錐の半径（平均距離）
PI_DEG = math.degrees(math.asin(6378.14 / 384400))   # 月の地平視差（度）
UMB = 0.7403 - U                                # 月の位置での地球の本影の半径
PEN = 1.2848 + U                                # 同じく半影の半径
LIM = dict(total_l=(0.4678 - U) * PI_DEG, part_l=(1.0128 - U) * PI_DEG, pen_l=(1.5573 + U) * PI_DEG,
           part_s=(1.5433 + U) * PI_DEG, cen_s=0.9972 * PI_DEG)
INC = 5.145                                     # 月の通り道の傾き


def tw(s, size):
    """文字列のおよその幅（全角1字＝size、半角0.56字）"""
    return sum(size * (0.56 if ord(c) < 0x2000 else 1.0) for c in s)


def earth(cx, cy, r, label=True):
    """地球：太陽（左）側が昼"""
    return (circle(cx, cy, r, "#2f4f6b", "#2f4f6b", 0)
            + f'<path d="M{cx:.1f},{cy - r:.1f} A{r},{r} 0 0 0 {cx:.1f},{cy + r:.1f}Z" fill="{SKY}"/>'
            + (text(cx, cy + 6, "地球", 17, "#fff", 700, "middle") if label else ""))


def half_lit(cx, cy, r, dark=MOON_D):
    """左（太陽側）半分が光った球"""
    return (circle(cx, cy, r, dark, dark, 0)
            + f'<path d="M{cx:.1f},{cy - r:.1f} A{r},{r} 0 0 0 {cx:.1f},{cy + r:.1f}Z" fill="{SUN}"/>')


def info(x, y, w, rows, title=None):
    h = 22 + len(rows) * 28 + (30 if title else 0)
    out = [rect(x, y, w, h, CARD, LINE, 10)]
    yy = y + 30
    if title:
        out.append(text(x + 14, yy, title, 17, INK, 700)); yy += 30
    for r, c in rows:
        out.append(text(x + 14, yy, r, 16 if c != MUTED else 14.5, c)); yy += 28
    return "".join(out)


SUN_DEFS = '<clipPath id="gn-body"><rect x="0" y="96" width="1200" height="528"/></clipPath>'


def big_sun():
    return (f'<g clip-path="url(#gn-body)"><circle cx="-250" cy="365" r="322" fill="{SUN}" stroke="{GOLD}" stroke-width="2"/></g>'
            + text(14, 372, "太陽", 20, "#7a5a10", 700))


def fig1():
    b = [big_sun()]
    ER, MR = 46, 46 * KM
    # ---------- 上：月食 ----------
    cy = 236; ex, mx, xe = 430, 730, 820
    b.append(text(104, 130, "月食（満月のころ）", 20, ACC, 700))
    for dy in (-38, 0, 38):
        b.append(arrow(84, cy + dy, 168, cy + dy, "gold", 2.4))
    pr = lambda xx: ER + (PEN - 1) * ER * (xx - ex) / (mx - ex)      # 半影の半径（月の位置で PEN×地球半径）
    um = lambda xx: ER - (1 - UMB) * ER * (xx - ex) / (mx - ex)      # 本影の半径（月の位置で UMB×地球半径）
    b.append(f'<path d="M{ex},{cy - ER} L{xe},{cy - pr(xe):.1f} L{xe},{cy + pr(xe):.1f} L{ex},{cy + ER}Z" fill="#c9ccd2" opacity=".55"/>')
    b.append(f'<path d="M{ex},{cy - ER} L{xe},{cy - um(xe):.1f} L{xe},{cy + um(xe):.1f} L{ex},{cy + ER}Z" fill="#3b3f46" opacity=".88"/>')
    b.append(earth(ex, cy, ER))
    b.append(circle(mx, cy, MR, "#9a3b22", "#f0c9b8", 1.4))
    b.append(text(590, cy + 6, "地球の本影（こい影）", 15, "#fff", 700, "middle"))
    b.append(line(790, cy - pr(790) + 2, 806, cy - 82, MUTED, 1.2) + text(806, cy - 88, "半影（うすい影）", 15, INK2, anchor="middle"))
    b.append(line(mx, cy + MR + 2, mx + 6, cy + 74, MUTED, 1.2) + text(mx + 6, cy + 92, "月（赤黒く見える）", 15, INK, 700, "middle"))
    b.append(info(862, 112, 290, [("並び方　太陽－地球－月", INK), ("月の形　満月", INK), ("月が地球の影に入る", INK),
                                  ("月が出ていればどこでも見られる", INK), (f"本影は月の直径の約{UMB / KM:.1f}倍", MUTED)]))
    # ---------- 下：日食 ----------
    cy = 472; mx, ex = 470, 730
    b.append(text(104, 364, "日食（新月のころ）", 20, TEAL_D, 700))
    for dy in (-38, 0, 38):
        b.append(arrow(84, cy + dy, 168, cy + dy, "gold", 2.4))
    ps = 0.5461 + U                                   # 地球の位置での月の半影の半径（地球半径単位）
    b.append(f'<path d="M{mx},{cy - MR:.1f} L{ex},{cy - ps * ER:.1f} L{ex},{cy + ps * ER:.1f} L{mx},{cy + MR:.1f}Z" fill="#c9ccd2" opacity=".6"/>')
    tip = ex - ER
    b.append(f'<path d="M{mx},{cy - MR:.1f} L{tip},{cy} L{mx},{cy + MR:.1f}Z" fill="#3b3f46" opacity=".9"/>')
    b.append(earth(ex, cy, ER, False) + text(ex + 18, cy + 6, "地球", 17, "#fff", 700, "middle"))
    b.append(f'<ellipse cx="{tip + 6}" cy="{cy}" rx="7" ry="{ps * ER - 2:.1f}" fill="#3b3f46" opacity=".45"/>' + circle(tip + 3, cy, 4.5, "#14181d", "#14181d", 0))
    b.append(half_lit(mx, cy, MR))
    b.append(text(mx, cy - 26, "月（新月）", 15, INK, 700, "middle"))
    b.append(line(tip + 2, cy + 6, 640, cy + 66, INK2, 1.2) + text(640, cy + 84, "こい影（本影）が届く所 → 皆既日食", 15, INK, 700, "end"))
    b.append(line(tip + 4, cy + ps * ER - 4, 650, cy + 102, INK2, 1.2) + text(640, cy + 110, "うすい影（半影）の所 → 部分日食", 15, INK2, anchor="end"))
    b.append(info(862, 380, 290, [("並び方　太陽－月－地球", INK), ("月の形　新月", INK), ("月の影が地球に落ちる", INK),
                                  ("影が通る、限られた所だけ", INK), ("太陽を直接見てはいけない", MUTED)]))
    b.append(line(96, 344, 1152, 344, LINE, 1.2))
    b.append(text(1152, 612, "大きさの比はほぼ実際どおり。きょりは実際とちがう（月までは地球の直径の約30倍）", 14, MUTED, anchor="end"))
    return svg("".join(b), "月食と日食が起こる位置関係",
               "太陽・地球・月が一直線に並ぶと食が起こる。月食は満月のころ、日食は新月のころ。", SUN_DEFS)


def fig2():
    b = []
    sx, sy, RO, KD = 360, 352, 246, 0.317                 # 太陽の位置、地球の公転の半径、奥行きのちぢめ方
    CZ = math.sqrt(1 - KD * KD)
    P = lambda x3, y3, z3: (sx + x3, sy - y3 * KD - z3 * CZ)   # 宇宙をななめ上から見た図
    b.append(text(48, 130, "宇宙からななめに見た図（地球の公転を1年分）", 18, INK, 700))
    b.append(f'<ellipse cx="{sx}" cy="{sy}" rx="{RO + 70}" ry="{(RO + 70) * KD:.1f}" fill="{TEAL_L}" stroke="{LINE}"/>')
    b.append(text(sx + RO + 64, sy + (RO + 70) * KD - 6, "地球の公転面", 14, TEAL, anchor="end"))
    b.append(f'<ellipse cx="{sx}" cy="{sy}" rx="{RO}" ry="{RO * KD:.1f}" fill="none" stroke="{MUTED}" stroke-dasharray="5 5" stroke-width="1.4"/>')
    b.append(circle(sx, sy, 30, SUN, GOLD, 2) + text(sx, sy + 6, "太陽", 15, "#7a5a10", 700, "middle"))
    RM, I = 64, math.radians(15)                           # 月の通り道（傾きは大きくかく）
    # 交点を結ぶ線は奥行きの向き（地球が手前・奥のとき、満月・新月が交点に来る）
    def moon3(a):
        return (RM * math.cos(a) * math.cos(I), RM * math.sin(a), RM * math.cos(a) * math.sin(I))
    pos = [("L", -RO, 0), ("R", RO, 0), ("F", 0, -RO), ("B", 0, RO)]
    for key, ex3, ey3 in pos:
        E = P(ex3, ey3, 0)
        # 地球の影（太陽と反対側へ、公転面にそって）
        d = (ex3 / RO, ey3 / RO)
        sh_end = P(ex3 + d[0] * (RM + 22), ey3 + d[1] * (RM + 22), 0)
        b.append(line(E[0], E[1], sh_end[0], sh_end[1], "#3b3f46", 9) .replace('/>', ' stroke-linecap="round" opacity=".35"/>'))
        pts = [moon3(math.radians(t)) for t in range(0, 361, 4)]
        up = [P(ex3 + q[0], ey3 + q[1], q[2]) if q[2] >= -1e-9 else None for q in pts]
        dn = [P(ex3 + q[0], ey3 + q[1], q[2]) if q[2] <= 1e-9 else None for q in pts]
        for seq, dash in ((dn, "4 4"), (up, None)):
            run = []
            for p in seq + [None]:
                if p is None:
                    if len(run) > 1: b.append(poly(run, TEAL, 1.8, dash=dash))
                    run = []
                else:
                    run.append(p)
        b.append(circle(E[0], E[1], 10, "#2f4f6b", "#fff", 1.5))
        # 新月（太陽の側）と満月（反対側）
        to_sun = math.atan2(-ey3, -ex3)                      # 地球から見た太陽の向き（公転面上の角）
        def on_orbit(phi):                                   # 公転面への写りが向き phi になる月の位置
            best = min(range(0, 360), key=lambda t: abs(((math.degrees(math.atan2(moon3(math.radians(t))[1], moon3(math.radians(t))[0])) - math.degrees(phi)) + 180) % 360 - 180))
            q = moon3(math.radians(best)); return P(ex3 + q[0], ey3 + q[1], q[2]), q[2]
        nm, zn = on_orbit(to_sun); fm, zf = on_orbit(to_sun + math.pi)
        b.append(circle(nm[0], nm[1], 7, MOON_D, "#fff", 1.2))
        b.append(circle(fm[0], fm[1], 7, SUN, GOLD, 1.2))
    # ラベル
    lab = [(P(-RO, 0, 0), "起こらない", "満月・新月が公転面の上か下", "middle", 46, -66),
           (P(RO, 0, 0), "起こらない", "満月・新月が公転面の上か下", "middle", -46, -66),
           (P(0, -RO, 0), "食が起こる", "満月・新月が交点の近く", "middle", 0, 66),
           (P(0, RO, 0), "食が起こる", "満月・新月が交点の近く", "middle", 0, -96)]
    for (x0, y0), t1, t2, anc, dx, dy in lab:
        col = ACC if t1 == "食が起こる" else INK2
        b.append(text(x0 + dx, y0 + dy, t1, 16, col, 700, anc) + text(x0 + dx, y0 + dy + 20, t2, 14, INK2, anchor=anc))
    b.append(circle(58, 562, 7, SUN, GOLD, 1.2) + text(72, 567, "満月", 14, INK2) + circle(128, 562, 7, MOON_D, "#fff", 1.2) + text(142, 567, "新月", 14, INK2)
             + line(194, 562, 224, 562, TEAL, 1.8) + text(230, 567, "月の通り道（公転面より上）", 14, INK2)
             + line(428, 562, 458, 562, TEAL, 1.8, "4 4") + text(464, 567, "（公転面より下）", 14, INK2))
    b.append(lines(48, 592, ["交点＝月の通り道が地球の公転面と交わる所。", f"通り道のかたむき（実際は約{INC:.1f}°）は大きくかいた。大きさ・きょりは実際とちがう。"], 14, MUTED, gap=1.45))
    # ---------- 右：起こる条件の表 ----------
    x0 = 752
    b.append(text(x0, 130, "満月・新月のときの上下のずれと食", 18, INK, 700))
    rows = [["皆既月食", f"約{LIM['total_l']:.2f}°以内"], ["部分月食", f"約{LIM['part_l']:.2f}°以内"],
            ["半影月食（ほぼ気づかない）", f"約{LIM['pen_l']:.2f}°以内"], ["日食（どこかで部分日食）", f"約{LIM['part_s']:.2f}°以内"],
            ["皆既・金環日食（どこかで）", f"約{LIM['cen_s']:.2f}°以内"], ["食は起きない", f"それより大きい"]]
    b.append(table(x0, 146, ["起こる食", "ずれ"], rows, [250, 150], 42, 15.5))
    b.append(lines(x0, 468, ["ずれは、地球の中心から見た月の上下のはなれ", f"（月までの距離が平均のとき。最大で約{INC:.1f}°）。"], 14, MUTED))
    b.append(lines(x0, 524, ["・月の見かけの直径は約0.5°。ずれが月3個分", "　より大きいと、食は起きない。",
                             "・交点の近くで満月・新月になるのは約半年ごと", "　→ 食は年に2回ほどの時期にまとまって起こる。"], 15, INK, gap=1.45))
    return svg("".join(b), "なぜ毎月は起きない？（月の通り道のかたむき）",
               "ふだんの満月・新月は、太陽と地球を結ぶ線の上か下を通るので、食は起きない。")


FIGS = [
    dict(svg=fig1, alt="月食と日食が起こる位置関係の図。月食は満月のころ太陽・地球・月の順に並び、月が地球の本影に入って赤黒く見える。日食は新月のころ太陽・月・地球の順に並び、月の本影が届く所で皆既日食、半影の所で部分日食になる。",
         caption="月食と日食の位置関係。月食は月が地球の影に入り、日食は月の影が地球に落ちる。"),
    dict(svg=fig2, alt="月の通り道が地球の公転面に対して約5°かたむいているため、ふだんの満月・新月は公転面の上か下を通って食が起きず、交点の近くで満月・新月になるときだけ月食・日食が起こることを示す図と、皆既月食・部分月食・日食が起こるずれの大きさの早見表。",
         caption="毎月は食が起きない理由。月の通り道がかたむいているので、交点の近くで満月・新月になるときだけ食が起こる。"),
]
