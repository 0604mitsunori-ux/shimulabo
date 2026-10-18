"""星の1日・1年の動き（hoshi-ugoki）の授業用の図
   数値はページの JS（scripts/rika/sims_tentai.py の CORE2）と同じ式：
   東京 北緯35.6581°・東経139.7414°、高度・方位は hor()（時角から計算）、太陽の黄経は sunOf()（2026年）。
   公転の図の星座の向き（黄経）は、ページと同じ星（SIMBAD・2026.5年に歳差補正）の重心から計算した値
   （オリオン座 83.8°・しし座 152.9°・さそり座 255.9°・ペガスス座 353.3°。sims_tentai.py の ORB_JS と同じ）。"""
import math
from figlib import *

R = math.pi / 180
LAT = 35.6581
SLA, CLA = math.sin(LAT * R), math.cos(LAT * R)
EPS = 23.4366
ML = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
JD0 = 2461041.5                                   # 2026-01-01 0時（世界時）
ORB = [("オリオン座", "冬", 83.8), ("しし座", "春", 152.9), ("さそり座", "夏", 255.9), ("ペガスス座", "秋", 353.3)]


def hor_h(H, dec):
    """時角 H（度）・赤緯 → 高度・方位（北から東回り）。ページの hor() と同じ式"""
    Hr, d = H * R, dec * R
    sh = SLA * math.sin(d) + CLA * math.cos(d) * math.cos(Hr)
    az = math.atan2(-math.cos(d) * math.sin(Hr), math.sin(d) * CLA - math.cos(d) * math.cos(Hr) * SLA) / R
    return math.asin(sh) / R, az % 360


def sun_lon(jd):
    n = jd - 2451545; g = (357.529 + 0.98560028 * n) * R; q = 280.459 + 0.98564736 * n
    return (q + 1.915 * math.sin(g) + 0.020 * math.sin(2 * g)) % 360


def md(n):
    m = 0
    while m < 11 and n > ML[m]: n -= ML[m]; m += 1
    return m + 1, n


def date_when_earth_at(lon):
    """地球の位置（太陽から見た黄経）が lon になる2026年の日（地球の黄経＝太陽の黄経＋180°）"""
    best = min(range(1, 366), key=lambda n: abs(((sun_lon(JD0 + n - 1 + 0.5) + 180 - lon) + 180) % 360 - 180))
    return md(best)


def season_word(m, d):
    return f"{m}月" + ("上旬" if d <= 10 else "中ごろ" if d <= 20 else "下旬")


def tw(s, size):
    return sum(size * (0.56 if ord(c) < 0x2000 else 1.0) for c in s)


# ---------- 図1：方位ごとの星の動き ----------
def vec(alt, az):
    ca = math.cos(alt * R); return (ca * math.sin(az * R), ca * math.cos(az * R), math.sin(alt * R))   # 東・北・上


def cam(az0, alt0):
    a, h = az0 * R, alt0 * R
    F = (math.sin(a) * math.cos(h), math.cos(a) * math.cos(h), math.sin(h))
    Rt = (math.cos(a), -math.sin(a), 0.0)
    U = (-math.sin(h) * math.sin(a), -math.sin(h) * math.cos(a), math.cos(h))
    return F, Rt, U


def stereo(c, alt, az):
    """立体射影（角度の形が保たれる）。見る向きの中心からの (x, y)、単位は半径1"""
    F, Rt, U = c; v = vec(alt, az)
    z = sum(p * q for p, q in zip(v, F)); X = sum(p * q for p, q in zip(v, Rt)); Y = sum(p * q for p, q in zip(v, U))
    return 2 * X / (1 + z), 2 * Y / (1 + z)


def gnomo(c, alt, az):
    F, Rt, U = c; v = vec(alt, az)
    z = sum(p * q for p, q in zip(v, F)); X = sum(p * q for p, q in zip(v, Rt)); Y = sum(p * q for p, q in zip(v, U))
    return (X / z, Y / z) if z > 0.15 else None


PW, PT, PH, GY = 258, 168, 380, 520          # パネルの幅・上端・下端（地平線 GY）
PX = [48, 330, 612, 894]


def inside(p, x0, m=4):
    return x0 + m <= p[0] <= x0 + PW - m and PT + m <= p[1] <= GY + 1


def track(pts, x0, col=TEAL):
    """パネルの中に入る部分だけ線をひき、終わりに矢印"""
    q = [p for p in pts if inside(p, x0)]
    if len(q) < 2: return ""
    (x1, y1), (x2, y2) = q[-3] if len(q) > 2 else q[-2], q[-1]
    return poly(q, col, 2.6) + arrow(x1, y1, x2, y2, "teal", 2.6)


def dots(pts, x0, col=TEAL):
    return "".join(circle(p[0], p[1], 4.5, "#fff", col, 2) for p in pts if inside(p, x0, 6) and p[1] < GY - 3)


def panel(i, title, sides, desc):
    x0 = PX[i]
    return (f'<rect x="{x0}" y="{PT}" width="{PW}" height="{GY - PT}" fill="#e9f0f5" />'
            + f'<rect x="{x0}" y="{GY}" width="{PW}" height="40" fill="#d8cfb8"/>'
            + text(x0 + PW / 2, GY + 28, title, 20, INK, 700, "middle")
            + text(x0 + 8, GY + 26, "← " + sides[0], 14.5, INK2, 700) + text(x0 + PW - 8, GY + 26, sides[1] + " →", 14.5, INK2, 700, "end")
            + lines(x0 + PW / 2, GY + 70, desc, 15.5, INK, anchor="middle"))


def fig1():
    b = []
    clip = "".join(f'<clipPath id="hs-p{i}"><rect x="{PX[i]}" y="{PT}" width="{PW}" height="{GY - PT}"/></clipPath>' for i in range(4))
    # 東・南・西：地平線上の真東・真南・真西を中心にした立体射影（地平線は直線、地平線での角度は実際どおり）
    # 北：天の北極を中心にした透視図（北極星のまわりの円は円のまま、地平線は直線）
    conf = [("東の空", 90, ("北", "南"), ["地平線から右ななめ上へ", "のぼっていく"]),
            ("南の空", 180, ("東", "西"), ["東（左）から西（右）へ", "弧をえがいて動く"]),
            ("西の空", 270, ("南", "北"), ["右ななめ下へ", "しずんでいく"]),
            ("北の空", 0, ("西", "東"), ["北極星を中心に", "反時計回りに回る"])]
    for i, (title, az0, sides, desc) in enumerate(conf):
        b.append(panel(i, title, sides, desc))
        x0 = PX[i]; cx = x0 + PW / 2
        g = [f'<g clip-path="url(#hs-p{i})">']
        if az0 != 0:
            c = cam(az0, 0); S = 150 if az0 != 180 else 120
            P = lambda alt, az, c=c, S=S, cx=cx: (cx + stereo(c, alt, az)[0] * S, GY - stereo(c, alt, az)[1] * S)
            for a in (30, 60):
                g.append(poly([P(a, az0 + k) for k in range(-80, 81, 4)], "#b9c9d6", 1, dash="3 5"))
            g.append("</g>")
            b.append("".join(g))
            decs = {90: (-30, -10, 10, 30), 270: (-30, -10, 10, 30), 180: (-20, -5, 10)}[az0]
            for dec in decs:
                H0 = math.acos(max(-1, min(1, -math.tan(LAT * R) * math.tan(dec * R)))) / R
                if az0 == 90: Hs = [-H0 + 15 * k for k in range(0, 7)]
                elif az0 == 270: Hs = [H0 - 15 * k for k in range(6, -1, -1)]
                else: Hs = [15 * k for k in range(-5, 6)]
                fine = [Hs[0] + j * 0.5 for j in range(0, int((Hs[-1] - Hs[0]) / 0.5) + 1)]
                pts = [P(*hor_h(H, dec)) for H in fine if hor_h(H, dec)[0] > -0.01]
                b.append(track(pts, x0) + dots([P(*hor_h(H, dec)) for H in Hs if hor_h(H, dec)[0] > 0.5], x0))
            # 高度の目安のラベル：道すじから最もはなれた所（左はし・右はし・中央）に置く
            allp = [p for dec in decs for p in [P(*hor_h(H, dec)) for H in range(-180, 181, 2)] if inside(p, x0)]
            for a in (30, 60):
                best = None
                for (k, xx, anc), dy in [(c_, d_) for c_ in ((-1, x0 + 6, "start"), (1, x0 + PW - 6, "end"), (0, cx, "middle")) for d_ in (-5, 19)]:
                    q = P(a, az0 + (k * (40 if az0 != 180 else 50)))
                    w = 62; rx0 = xx if anc == "start" else xx - w if anc == "end" else xx - w / 2
                    yy = (q[1] if k != 0 else P(a, az0)[1]) + dy
                    d = min((max(rx0 - px, 0, px - rx0 - w) ** 2 + max(yy - 15 - py, 0, py - yy - 2) ** 2) for px, py in allp)
                    if best is None or d > best[0]: best = (d, xx, yy, anc)
                b.append(text(best[1], best[2], f"高度{a}°", 14, MUTED, anchor=best[3], stroke="#e9f0f5", stroke_width=5, paint_order="stroke"))
        else:
            c = cam(0, LAT); S = 150
            pcy = GY - math.tan(LAT * R) * S                         # 地平線がちょうど GY にくる
            P = lambda alt, az, c=c, S=S, cx=cx, pcy=pcy: (cx + gnomo(c, alt, az)[0] * S, pcy - gnomo(c, alt, az)[1] * S)
            pc = P(LAT, 0)
            for dec in (80, 70, 60, 50):
                g.append(poly([P(*hor_h(H, dec)) for H in range(0, 361, 3) if gnomo(c, *hor_h(H, dec))], "#b9c9d6", 1, dash="3 5"))
            g.append("</g>")
            b.append("".join(g))
            for dec, Hs in ((50, [-45 + 15 * k for k in range(4)]), (70, [45 + 15 * k for k in range(4)]), (60, [-120 + 15 * k for k in range(4)])):
                fine = [Hs[0] + j * 0.5 for j in range(0, int((Hs[-1] - Hs[0]) / 0.5) + 1)]
                b.append(track([P(*hor_h(H, dec)) for H in fine], x0) + dots([P(*hor_h(H, dec)) for H in Hs], x0))
                if dec == 50:
                    q1, q2 = P(*hor_h(Hs[1], dec)), P(*hor_h(Hs[2], dec))
                    b.append(line(pc[0], pc[1], q1[0], q1[1], ACC, 1.4, "4 3") + line(pc[0], pc[1], q2[0], q2[1], ACC, 1.4, "4 3"))
                    m = ((q1[0] + q2[0]) / 2 - pc[0], (q1[1] + q2[1]) / 2 - pc[1]); L = math.hypot(*m)
                    b.append(text(pc[0] + m[0] / L * 70, pc[1] + m[1] / L * 70 + 6, "15°", 16, ACC, 700, "middle"))
            b.append(circle(pc[0], pc[1], 6, GOLD, INK, 1.5) + text(pc[0] + 10, pc[1] + 22, "北極星", 16, INK, 700))
            b.append(text(x0 + PW - 8, PT + 22, f"北極星の高度 約{LAT:.1f}°", 14, INK2, anchor="end"))
    b.append(text(48, 132, "東京で、それぞれの方位を向いて見た星の動き（○は1時間ごとの位置）", 18, INK, 700))
    b.append(text(48, 156, "どの方位でも、星は1時間に約15°（360°÷24時間）ずつ動く。", 15, INK2))
    return svg("".join(b), "星の1日の動き（日周運動）",
               "地球が西から東へ1日に1回自転しているので、星は東から西へ1時間に約15°動いて見える。", clip)


# ---------- 図2：年周運動と季節の星座 ----------
def fig2():
    b = []
    sx, sy, RO, RC = 280, 365, 104, 186
    TH0 = 186                                         # 画面の角度＝黄経＋186°（ページの公転の図と同じ向き：冬が下）
    ang = lambda lon: math.radians(lon + TH0)
    P = lambda r, lon: (sx + r * math.cos(ang(lon)), sy - r * math.sin(ang(lon)))
    b.append(text(48, 128, "北極の上から見た地球の公転と季節の星座", 18, INK, 700))
    b.append(circle(sx, sy, RO, "none", MUTED, 1.4).replace('stroke-width="1.4"', 'stroke-width="1.4" stroke-dasharray="5 5"'))
    a0, a1 = ang(300), ang(330); RR = RO + 16
    b.append(f'<path d="M{sx + RR * math.cos(a0):.1f},{sy - RR * math.sin(a0):.1f} A{RR},{RR} 0 0 0 {sx + RR * math.cos(a1):.1f},{sy - RR * math.sin(a1):.1f}" fill="none" stroke="{TEAL}" stroke-width="2.4" marker-end="url(#ah-teal)"/>')
    q = P(RR + 30, 322); b.append(text(q[0], q[1], "公転の向き", 14, TEAL, 700, "middle"))
    b.append(circle(sx, sy, 26, SUN, GOLD, 2) + text(sx, sy + 6, "太陽", 15, "#7a5a10", 700, "middle"))
    for nm, sea, lon in ORB:
        m, d = date_when_earth_at(lon)
        E = P(RO, lon); C = P(RC, lon)
        # 地球（太陽側が昼）
        th = ang(lon)
        ux, uy = math.cos(th), -math.sin(th)                       # 太陽から地球への向き（画面）
        b.append(circle(E[0], E[1], 13, "#2f4f6b", "#fff", 1.5))
        p1 = (E[0] + 13 * uy, E[1] - 13 * ux); p2 = (E[0] - 13 * uy, E[1] + 13 * ux)
        b.append(f'<path d="M{p1[0]:.1f},{p1[1]:.1f} A13,13 0 0 0 {p2[0]:.1f},{p2[1]:.1f}Z" fill="{SKY}"/>')
        b.append(arrow(E[0] + ux * 16, E[1] + uy * 16, C[0] - ux * 34, C[1] - uy * 34, "acc", 2))
        tx, ty = -math.sin(th), -math.cos(th)                    # 公転の道にそった向き（ラベルを地球の横に置く）
        if abs(tx) > 0.5: b.append(text(E[0] + tx * 22, E[1] + 6, season_word(m, d), 15, INK, 700, "start" if tx > 0 else "end"))
        else: b.append(text(E[0], E[1] + (34 if ty > 0 else -22), season_word(m, d), 15, INK, 700, "middle"))
        b.append(circle(C[0], C[1], 32, "#fff", GOLD, 1.6))
        b.append(text(C[0], C[1] - 2, nm.replace("座", ""), 14.5, INK, 700, "middle") + text(C[0], C[1] + 16, f"（{sea}）", 13.5 if False else 14, INK2, anchor="middle"))
    b.append(text(48, 610, "赤い矢印＝真夜中に南に見える向き。大きさ・きょりは実際とちがう。", 14, MUTED))
    # ---- 右：まとめ ----
    x0 = 572
    b.append(text(x0, 128, "動き方のまとめ", 18, INK, 700))
    rows = [["日周運動", "1時間に約15°、東から西へ", "地球の自転"],
            ["年周運動", "同じ時刻で1か月に約30°、東から西へ", "地球の公転"]]
    b.append(table(x0, 144, ["", "動き方", "原因"], rows, [124, 320, 136], 44, 15.5))
    b.append(lines(x0, 300, ["・南中する時刻は1日に約4分、1か月で約2時間早くなる。",
                             "　例：1月15日22時に南中した星は、2月15日には20時ごろ南中。",
                             "・北極星はほとんど動かない（高度＝その土地の緯度）。"], 15, INK, gap=1.5))
    b.append(text(x0, 384, "季節の星座（夜9時ごろの南の空）", 18, INK, 700))
    srows = [["春（4〜5月）", "しし座・おとめ座・うしかい座"], ["夏（7〜8月）", "さそり座・いて座・わし座"],
             ["秋（10〜11月）", "ペガスス座・アンドロメダ座"], ["冬（1〜2月）", "オリオン座・おうし座・おおいぬ座"]]
    b.append(table(x0, 400, ["季節", "南の空の主な星座"], srows, [150, 430], 40, 15.5))
    b.append(text(x0, 616, "太陽と同じ方向にある星座は、昼の空にあるので見えない。", 14.5, INK2))
    return svg("".join(b), "星の1年の動き（年周運動）と季節の星座",
               "地球が1年で太陽のまわりを1周するので、同じ時刻に見える星は1か月に約30°ずつ西へずれる。")


FIGS = [
    dict(svg=fig1, alt="東京で東・南・西・北の空を見たときの星の日周運動の図。東の空では右ななめ上へのぼり、南の空では東から西へ弧をえがき、西の空では右ななめ下へしずみ、北の空では北極星を中心に反時計回りに1時間に15°回る。1時間ごとの位置を点で示している。",
         caption="方位ごとの星の動き（日周運動）。星は1時間に約15°、東から西へ動いて見える。"),
    dict(svg=fig2, alt="北極の上から見た地球の公転と季節の星座（オリオン座・しし座・さそり座・ペガスス座）の図で、真夜中に南の空に見える星座が季節で変わることを示す。日周運動（1時間に15°）・年周運動（1か月に30°）・南中時刻のずれと、夜9時ごろの季節の星座の早見表。",
         caption="年周運動と季節の星座。真夜中に南に見えるのは、太陽と反対側にある星座。"),
]
