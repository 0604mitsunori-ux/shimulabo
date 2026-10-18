"""コリオリの力と大気の大循環（coriolis-henseifu）の授業用の図
   ページの JS（scripts/rika/sims_kou_chigaku.py）と同じ式：
   回る円盤（半径1 m）：外から見て等速直線運動する玉を、円盤とともに回る座標に直す rot(x, y, −ωt)。1分間に10回転・秒速1 m → 1秒で60°。
   f＝2Ω sinφ（Ω＝7.29×10⁻⁵ rad/s）。大循環：ハドレー（0〜30°）・フェレル（30〜60°）・極循環（60〜90°）、
   地上の風の向き uvw(la)＝(−sin(6|la|), −0.45 sin(6la))（東向き・北向き）。"""
import math
from figlib import *

OM = 7.29e-5
RPM, VB = 10, 1.0
W = RPM * 2 * math.pi / 60                          # 円盤の角速度 rad/s（反時計回り＝北半球）


def fpar(p): return 2 * OM * math.sin(math.radians(p))


def sci(v, d=2):
    if abs(v) < 1e-15: return "0"
    e = math.floor(math.log10(abs(v))); m = v / 10 ** e
    if round(abs(m), d) >= 10: e += 1; m /= 10
    sup = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
    return f"{m:.{d}f}×10" + str(e).translate(sup)


def throw(n=200):
    """中心から上（90°）へ投げた玉の位置：外から見た (x, y) と円盤から見た (x, y)。単位は半径＝1"""
    T = 1 / VB; out = []
    for i in range(n + 1):
        t = T * i / n; d = VB * t; xi, yi = 0.0, d
        a = -W * t; xr, yr = xi * math.cos(a) - yi * math.sin(a), xi * math.sin(a) + yi * math.cos(a)
        out.append((xi, yi, xr, yr))
    return out


def disk(cx, cy, R, rot_deg, path, who_ang, title, sub, sub_col, outside):
    b = [circle(cx, cy, R, "#fef3c7", "#b45309", 2)]
    for i in range(8):
        a = math.radians(rot_deg + i * 45)
        b.append(line(cx, cy, cx + R * math.cos(a), cy - R * math.sin(a), "#e6c58a", 1))
    b.append(circle(cx, cy, R / 2, "none", "#e6c58a", 1))
    if outside:                                                  # 回転の向き（反時計回り）
        for a0 in (200, 290):
            a1 = a0 + 50; rr_ = R + 14
            p0 = (cx + rr_ * math.cos(math.radians(a0)), cy - rr_ * math.sin(math.radians(a0)))
            p1 = (cx + rr_ * math.cos(math.radians(a1)), cy - rr_ * math.sin(math.radians(a1)))
            b.append(f'<path d="M{p0[0]:.1f},{p0[1]:.1f} A{rr_},{rr_} 0 0 0 {p1[0]:.1f},{p1[1]:.1f}" fill="none" stroke="#b45309" stroke-width="2.6" marker-end="url(#ah-gold)"/>')
    pts = [(cx + p[0] * R, cy - p[1] * R) for p in path]
    b.append(poly(pts, ACC, 3.4))
    b.append(circle(pts[-1][0], pts[-1][1], 8, "#fff", INK, 2))
    b.append(circle(cx, cy, 8, GREEN, "#fff", 2) + text(cx, cy + 26, "投げる人", 15, GREEN, 700, "middle"))
    for ang, dash in who_ang:
        qx, qy = cx + R * math.cos(math.radians(ang)), cy - R * math.sin(math.radians(ang))
        b.append(circle(qx, qy, 9, "#2563eb" if not dash else "#fff", "#2563eb", 2))
    b.append(text(cx, 168, title, 17, INK, 700, "middle") + text(cx, 192, sub, 15, sub_col, 700, "middle"))
    return "".join(b)


def fig1():
    b = []
    path = throw()
    R = 124
    # 左：外から見た円盤（玉はまっすぐ。受ける人は60°回って先へ行く）
    cx1, cy = 196, 368
    out_path = [(p[0], p[1]) for p in path]
    b.append(disk(cx1, cy, R, W * 1 / VB * 180 / math.pi, out_path, [(90, True), (90 + math.degrees(W / VB), False)],
                  "外（止まっている所）から見る", "玉はまっすぐ進む", INK2, True))
    a_end = 90 + math.degrees(W / VB)
    qx, qy = cx1 + R * math.cos(math.radians(a_end)), cy - R * math.sin(math.radians(a_end))
    b.append(line(qx - 4, qy - 8, 74, 240, "#1d4ed8", 1.2) + text(48, 234, "受ける人（1秒後）", 15, "#1d4ed8", 700))
    b.append(text(cx1 + 14, cy - R - 10, "受ける人（投げたとき）", 14, "#1d4ed8"))
    # 右：円盤の上から見た（右へ曲がって見える）
    cx2 = 516
    rot_path = [(p[2], p[3]) for p in path]
    b.append(disk(cx2, cy, R, 0, rot_path, [(90, False)], "円盤の上（いっしょに回る人）から見る", "玉は進む向きの右へ曲がって見える", PURPLE, False))
    b.append(line(cx2, cy, cx2, cy - R, INK2, 1.4, "5 4"))
    dev = math.degrees(math.atan2(rot_path[-1][1], rot_path[-1][0]))
    rr_ = R * 0.68; a0, a1 = math.radians(90), math.radians(dev)
    b.append(f'<path d="M{cx2 + rr_ * math.cos(a0):.1f},{cy - rr_ * math.sin(a0):.1f} A{rr_},{rr_} 0 0 1 {cx2 + rr_ * math.cos(a1):.1f},{cy - rr_ * math.sin(a1):.1f}" fill="none" stroke="{PURPLE}" stroke-width="2.4"/>')
    am = math.radians((90 + dev) / 2)
    b.append(text(cx2 + R * 0.84 * math.cos(am) + 6, cy - R * 0.84 * math.sin(am) + 6, f"{90 - dev:.0f}°", 17, PURPLE, 700, "middle"))
    b.append(text(cx2, cy - R - 12, "受ける人", 15, "#1d4ed8", 700, "middle"))
    b.append(lines(48, 548, [f"1分間に{RPM}回転（反時計回り）の円盤（半径1 m）の中心から、秒速{VB:.0f} mで玉を投げる。",
                             f"ふちに届くまで{1 / VB:.0f}秒 → その間に円盤は {math.degrees(W / VB):.0f}° 回る → 円盤の上からは右へ{math.degrees(W / VB):.0f}°それて見える。"], 15, INK, gap=1.55))
    b.append(text(48, 612, "円盤の上で見える見かけの力＝コリオリの力（転向力）。", 15, PURPLE, 700))
    # 右：地球では
    x0 = 700
    b.append(rect(x0, 116, 452, 186, TEAL_L, TEAL, 10, 1.4))
    b.append(text(x0 + 16, 144, "地球の上では", 17, TEAL_D, 700))
    b.append(lines(x0 + 16, 172, ["・北半球：進む向きの右へ曲げる", "・南半球：進む向きの左へ曲げる", "・赤道：0　極：いちばん大きい"], 16, INK, gap=1.55))
    b.append(text(x0 + 16, 278, "C ＝ 2mΩv sinφ ＝ m f v", 17, INK, 700))
    b.append(text(x0, 334, "f ＝ 2Ω sinφ（Ω ＝ 7.29×10⁻⁵ rad/s）", 16, INK, 700))
    rows = [[f"{p}°" if p else "0°（赤道）", f"{math.sin(math.radians(p)):.3f}", sci(fpar(p)) + " /s"] for p in (0, 30, 35, 45, 90)]
    rows[-1][0] = "90°（極）"
    b.append(table(x0, 348, ["緯度φ", "sinφ", "f"], rows, [150, 110, 192], 38, 15.5))
    return svg("".join(b), "コリオリの力のしくみ（回る円盤）",
               "回る円盤や自転する地球の上から見ると、まっすぐ進むものが曲がって見える。北半球では右、南半球では左へ。")


def uvw(la):
    return -math.sin(math.radians(6 * abs(la))), -0.45 * math.sin(math.radians(6 * la))


def fig2():
    b = []
    C = (60, 372); RE, HA = 160, 56
    cs = lambda la, h: (C[0] + (RE + h) * math.cos(math.radians(la)), C[1] - (RE + h) * math.sin(math.radians(la)))
    b.append(text(48, 128, "地球の断面（大気の厚さは誇張）", 17, INK, 700))
    # 大気と地球
    pa = cs(90, HA); pb = cs(-90, HA)
    b.append(f'<path d="M{C[0]},{pa[1]:.1f} A{RE + HA},{RE + HA} 0 0 1 {C[0]},{pb[1]:.1f}Z" fill="#e0f2fe"/>')
    b.append(f'<path d="M{C[0]},{C[1] - RE} A{RE},{RE} 0 0 1 {C[0]},{C[1] + RE}Z" fill="#3b6ea5"/>')
    for la in (-60, -30, 0, 30, 60):
        p, q = cs(la, 0), cs(la, HA + 6); b.append(line(p[0], p[1], q[0], q[1], MUTED, 1, "3 3"))
    cols = ["#d9622b", GREEN, "#0e7aa8"]
    cells = [(15, 12, -1, "ハドレー"), (45, 12, 1, "フェレル"), (75, 12, -1, "極循環")]
    for hs in (1, -1):
        for ci, (c0, c1, dr, nm) in enumerate(cells):
            pt = lambda t: cs(hs * (c0 + c1 * math.cos(t)), HA * (0.44 + 0.30 * math.sin(t)))
            ring = [pt(i / 60 * 2 * math.pi) for i in range(61)]
            b.append(poly(ring, cols[ci], 2.4))
            for t in (math.pi / 2, 3 * math.pi / 2, 0, math.pi):
                q, q2 = pt(t), pt(t + dr * 0.25)
                ang = math.atan2(q2[1] - q[1], q2[0] - q[0])
                b.append(f'<path d="M{q2[0] + 5 * math.cos(ang):.1f},{q2[1] + 5 * math.sin(ang):.1f} L{q2[0] - 6 * math.cos(ang - 0.5):.1f},{q2[1] - 6 * math.sin(ang - 0.5):.1f} L{q2[0] - 6 * math.cos(ang + 0.5):.1f},{q2[1] - 6 * math.sin(ang + 0.5):.1f}Z" fill="{cols[ci]}"/>')
    for la, t1, t2 in ((0, "赤道低圧帯", "（上昇）"), (30, "亜熱帯高圧帯", "（下降）"), (60, "亜寒帯低圧帯", "（上昇）"),
                       (-30, "亜熱帯高圧帯", "（下降）"), (-60, "亜寒帯低圧帯", "（上昇）")):
        p = cs(la, HA + 10)
        b.append(text(p[0] + 4, p[1] + (6 if la >= 0 else 14), t1, 14, INK2, 700) + text(p[0] + 4, p[1] + (24 if la >= 0 else 32), t2, 14, INK2))
    b.append(text(C[0] + 8, C[1] - RE - HA - 6, "北極", 14, INK2, 700) + text(C[0] + 8, C[1] + RE + HA + 2, "南極", 14, INK2, 700))
    b.append(text(C[0] + 60, C[1] + 6, "地球", 18, "#fff", 700))
    lx, ly = 440, 300
    b.append(text(lx, ly - 30, "循環（矢印は空気の流れ）", 15, INK, 700))
    for ci, nm in enumerate(["ハドレー循環（0〜30°）", "フェレル循環（30〜60°）", "極循環（60〜90°）"]):
        b.append(line(lx, ly + ci * 30 - 5, lx + 30, ly + ci * 30 - 5, cols[ci], 3.4) + text(lx + 40, ly + ci * 30, nm, 15, cols[ci], 700))
    b.append(lines(lx, ly + 112, ["上昇する所は低圧帯、", "下降する所は高圧帯になる。"], 14.5, INK2, gap=1.5))
    # 右：地上の風（地図）
    MX0, MX1 = 712, 960
    MY = lambda la: 372 - la * 2.48
    b.append(text(MX0 - 60, 128, "地上の風（年平均のモデル・上が北）", 17, INK, 700))
    for la0, la1, c in ((90, 60, "#e0f2fe"), (60, 30, "#dcfce7"), (30, 0, "#ffedd5"), (0, -30, "#ffedd5"), (-30, -60, "#dcfce7"), (-60, -90, "#e0f2fe")):
        b.append(f'<rect x="{MX0}" y="{MY(la0):.1f}" width="{MX1 - MX0}" height="{MY(la1) - MY(la0):.1f}" fill="{c}"/>')
    for la in (60, 30, 0, -30, -60):
        b.append(line(MX0, MY(la), MX1, MY(la), INK2 if la == 0 else "#b8c2cc", 1.4 if la == 0 else 1))
        b.append(text(MX0 - 8, MY(la) + 5, "赤道" if la == 0 else ("北" if la > 0 else "南") + f"{abs(la)}°", 14, INK2, anchor="end"))
    b.append(f'<rect x="{MX0}" y="{MY(90)}" width="{MX1 - MX0}" height="{MY(-90) - MY(90)}" fill="none" stroke="{MUTED}"/>')
    b.append(text(MX1 - 6, MY(90) + 18, "東 →", 14, INK2, 700, "end") + text(MX0 + 6, MY(90) + 18, "← 西", 14, INK2, 700))
    names = [(75, "極偏東風", "北東の風"), (45, "偏西風", "南西の風"), (15, "北東貿易風", "北東の風"),
             (-15, "南東貿易風", "南東の風"), (-45, "偏西風", "北西の風"), (-75, "極偏東風", "南東の風")]
    for la, nm, sub in names:
        u, v = uvw(la); L = math.hypot(u, v); u, v = u / L * 22, v / L * 22
        y = MY(la)
        for cx in (MX0 + 44, (MX0 + MX1) / 2, MX1 - 44):
            b.append(arrow(cx - u, y + v, cx + u, y - v, "ink", 2.8))
        b.append(text(MX1 + 12, y - 2, nm, 16, INK, 700) + text(MX1 + 12, y + 18, f"（{sub}）", 14, INK2))
    b.append(text(1152, 614, "南北に動く空気がコリオリの力で曲げられ、東寄り・西寄りの風になる。", 14, MUTED, anchor="end"))
    return svg("".join(b), "大気の大循環と地上の風",
               "赤道であたためられた空気は上昇し、緯度30°付近で下降する（ハドレー循環）。地上の風はコリオリの力で曲げられる。")


FIGS = [
    dict(svg=fig1, alt="コリオリの力のしくみの図。1分間に10回転する半径1 mの円盤の中心から秒速1 mで玉を投げると、外から見るとまっすぐ進むが、円盤の上から見ると進む向きの右へ60°曲がって見える。地球では北半球で右、南半球で左に曲げられ、コリオリパラメータ f＝2Ωsinφ は赤道で0、極で最大（緯度ごとの早見表つき）。",
         caption="回る円盤で見るコリオリの力。円盤が回っている間に、玉は右へそれて見える。"),
    dict(svg=fig2, alt="大気の大循環の図。地球の断面にハドレー循環・フェレル循環・極循環と赤道低圧帯・亜熱帯高圧帯・亜寒帯低圧帯を示し、地上の風として北東貿易風・南東貿易風・偏西風（北半球は南西の風、南半球は北西の風）・極偏東風の向きを地図上の矢印で示している。",
         caption="大気の大循環と地上の風。貿易風と偏西風は、南北の空気の流れがコリオリの力で曲げられたもの。"),
]
