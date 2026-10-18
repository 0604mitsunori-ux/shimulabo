"""地震の伝わり方（jishin-ha）の授業用の図。
速さ・観測点・震源の深さはシミュの初期値（P波6 km/秒・S波3.5 km/秒・深さ10 km・震央(40,260)・観測点A〜E）と同じ。
震源距離は JS の model() と同じく三平方の定理、地震計の波形は JS の sig() と同じ式（見た目のためのモデル）。"""
from figlib import *

VP, VS, DEP = 6.0, 3.5, 10.0
EX, EY = 40, 260
ST = [("A", 99.0, 201.0), ("B", 66.1, 137.1), ("C", 204.0, 225.1), ("D", 157.3, 86.1), ("E", 251.2, 122.9)]
D = [math.sqrt((x - EX) ** 2 + (y - EY) ** 2 + DEP ** 2) for _, x, y in ST]
EPI = [math.hypot(x - EX, y - EY) for _, x, y in ST]
TP = [d / VP for d in D]
TS = [d / VS for d in D]
K = VP * VS / (VP - VS)                       # 大森公式の係数（8.4 km/秒）
PH = [[(((i + 1) * (k + 3) * 37) % 100) / 100 * math.pi * 2 for k in range(4)] for i in range(5)]
assert abs(K - 8.4) < 1e-9
assert [round(d) for d in D] == [84, 126, 168, 210, 252] and [round(ts - tp) for tp, ts in zip(TP, TS)] == [10, 15, 20, 25, 30]


def sig(i, tt):                               # JS の sig()
    tp, ts = TP[i], TS[i]
    if tt < tp: return 0.0
    ph = PH[i]; u = tt - tp
    eP = min(1, u / 0.5) * (1 if tt < ts else max(0.35, math.exp(-(tt - ts) / 3)))
    y = 0.28 * eP * (0.6 * math.sin(2 * math.pi * 2.6 * u + ph[0]) + 0.4 * math.sin(2 * math.pi * 4.1 * u + ph[1]))
    if tt >= ts:
        w = tt - ts; eS = min(1, w / 1.0) * math.exp(-w / (8 + D[i] / 25))
        y += eS * (0.62 * math.sin(2 * math.pi * 0.75 * w + ph[2]) + 0.38 * math.sin(2 * math.pi * 1.25 * w + ph[3]))
    return y


def surfR(R, d): return math.sqrt(R * R - d * d) if R > d else 0.0


def fig1():
    b = []
    T = 21.0                                  # B地点にP波が届いた瞬間（A地点は初期微動の最中）
    rP, rS = VP * T, VS * T
    # 左：地面の断面
    PL, PR, GY, sc = 48, 560, 214, 2.4
    ex = 96; hy = GY + DEP * sc
    b.append(text(PL, 122, f"地面の断面（地震が起きてから{T:.0f}秒後）", 18, INK, 700))
    b.append(text(PL, 144, "（大きさ・きょりは実際とちがう）", 14, MUTED))
    defs = f'<clipPath id="jh-g"><rect x="{PL}" y="{GY}" width="{PR - PL}" height="{600 - GY}"/></clipPath>'
    g = [f'<rect x="{PL}" y="{GY}" width="{PR - PL}" height="{600 - GY}" fill="{GOLD_L}"/>']
    g.append(f'<circle cx="{ex}" cy="{hy:.1f}" r="{rP * sc:.1f}" fill="{TEAL_L}" stroke="{TEAL}" stroke-width="3"/>')
    g.append(f'<circle cx="{ex}" cy="{hy:.1f}" r="{rS * sc:.1f}" fill="{ACC_L}" stroke="{ACC}" stroke-width="3"/>')
    b.append(f'<g clip-path="url(#jh-g)">{"".join(g)}</g>')
    b.append(line(PL, GY, PR, GY, INK, 2.2))
    b.append(text(PR - 4, GY - 10, "地表", 15, INK2, anchor="end"))
    # 地表での揺れの範囲
    sP, sS = surfR(rP, DEP) * sc, surfR(rS, DEP) * sc
    b.append(f'<rect x="{ex}" y="{GY - 7}" width="{sS:.1f}" height="7" fill="{ACC}"/>')
    b.append(f'<rect x="{ex + sS:.1f}" y="{GY - 7}" width="{sP - sS:.1f}" height="7" fill="{TEAL}"/>')
    # 震源・震央
    b.append(f'<path d="M{ex - 9},{hy - 9} l18,18 M{ex - 9},{hy + 9} l18,-18" stroke="{INK}" stroke-width="3.4"/>')
    b.append(text(ex + 16, hy + 30, "震源", 17, INK, 700))
    b.append(lines(ex + 16, hy + 52, ["（岩石が最初に", "ずれ動いた所）"], 14, INK2, 1.45))
    b.append(f'<path d="M{ex},{GY - 9} l-8,-14 h16z" fill="{INK}"/>')
    b.append(text(ex, GY - 30, "震央", 16, INK, 700, "middle") + text(ex + 20, GY - 30, "（震源の真上）", 14, INK2))
    # 観測点
    for i in (0, 1):
        xs = ex + EPI[i] * sc
        b.append(rect(xs - 13, GY - 24, 26, 17, CARD, INK, 3, 1.6) + poly([(xs - 9, GY - 15), (xs - 4, GY - 20), (xs, GY - 11), (xs + 4, GY - 19), (xs + 9, GY - 15)], INK, 1.4))
        b.append(text(xs, GY - 32, f"{ST[i][0]}地点", 16, INK, 700, "middle"))
    # 波の先頭に札
    for r, nm, col, ang in ((rP, "P波", TEAL, 33), (rS, "S波", ACC, 40)):
        a = math.radians(ang); x, y = ex + r * sc * math.cos(a), hy + r * sc * math.sin(a)
        b.append(rect(x - 24, y - 15, 48, 30, col, col, 15, 0) + text(x, y + 6, nm, 16, "#fff", 700, "middle"))
    LX, LY = 360, 486
    b.append(line(LX, LY - 6, LX + 28, LY - 6, TEAL, 3.4) + text(LX + 36, LY, f"P波の先頭（秒速{VP:g} km）", 15, TEAL_D, 700))
    b.append(text(LX + 36, LY + 20, "→ 初期微動（小さなゆれ）", 14, TEAL_D))
    b.append(line(LX, LY + 44, LX + 28, LY + 44, ACC, 3.4) + text(LX + 36, LY + 50, f"S波の先頭（秒速{VS:g} km）", 15, ACC, 700))
    b.append(text(LX + 36, LY + 70, "→ 主要動（大きなゆれ）", 14, ACC))
    # 地表の色の説明
    b.append(f'<rect x="{PL + 8}" y="584" width="22" height="8" fill="{ACC}"/>' + text(PL + 36, 592, "主要動", 14, ACC, 700))
    b.append(f'<rect x="{PL + 96}" y="584" width="22" height="8" fill="{TEAL}"/>' + text(PL + 124, 592, "初期微動", 14, TEAL_D, 700))
    b.append(text(PL + 186, 592, "が起きている地表（地表の色）", 14, INK2))
    # 右：地震計の記録
    X0, X1, TM = 668, 1140, 45.0
    tx = lambda t: X0 + t / TM * (X1 - X0)
    b.append(text(600, 122, "地震計の記録（地震が起きた時刻を0秒）", 18, INK, 700))
    for i, base in ((0, 226), (1, 414)):
        tp, ts = TP[i], TS[i]
        b.append(text(600, base + 6, f"{ST[i][0]}地点", 17, INK, 700))
        b.append(text(600, base + 26, f"震源距離", 14, INK2) + text(600, base + 44, f"{D[i]:.0f} km", 14, INK2))
        b.append(f'<rect x="{tx(tp):.1f}" y="{base - 78}" width="{tx(ts) - tx(tp):.1f}" height="136" fill="{TEAL}" opacity=".08"/>')
        b.append(line(X0, base, X1, base, LINE, 1))
        pts = [(tx(k * 0.02), base - 52 * sig(i, k * 0.02)) for k in range(int(TM / 0.02) + 1)]
        b.append(poly(pts, INK, 1.1))
        for t, col, nm in ((tp, TEAL, "P波が届く"), (ts, ACC, "S波が届く")):
            b.append(line(tx(t), base - 70, tx(t), base + 62, col, 2, "5 4"))
        b.append(text(tx(tp) - 4, base - 76, f"P波 {tp:.0f}秒", 14, TEAL_D, 700, "end"))
        b.append(text(tx(ts) + 4, base - 76, f"S波 {ts:.0f}秒", 14, ACC, 700))
        b.append(text((tx(tp) + tx(ts)) / 2, base - 36, "初期微動", 15, TEAL_D, 700, "middle"))
        b.append(text(tx(ts) + 50, base - 52, "主要動", 15, ACC, 700, "middle"))
        yb = base + 52
        b.append(line(tx(tp) + 3, yb, tx(ts) - 3, yb, INK, 1.6) + line(tx(tp), yb - 7, tx(tp), yb + 7, INK, 1.6) + line(tx(ts), yb - 7, tx(ts), yb + 7, INK, 1.6))
        b.append(text((tx(tp) + tx(ts)) / 2, yb + 22, f"初期微動継続時間 {ts - tp:.0f}秒", 15, INK, 700, "middle"))
    ay = 536
    b.append(line(X0, ay, X1, ay, INK, 1.6))
    for t in range(0, 46, 5):
        b.append(line(tx(t), ay, tx(t), ay + 6, INK, 1.4) + text(tx(t), ay + 24, str(t), 14, INK2, anchor="middle"))
    b.append(text(X1, ay + 44, "地震が起きてからの時間［秒］", 14, INK2, anchor="end"))
    b.append(text(600, 610, f"震源から遠いほど、初期微動継続時間は長い（{TS[0] - TP[0]:.0f}秒 → {TS[1] - TP[1]:.0f}秒）。", 16, INK, 700))
    return svg("".join(b), "P波・S波と初期微動継続時間のしくみ",
               f"P波（秒速{VP:g} km）とS波（秒速{VS:g} km）は震源から同時に出る。速いP波が先に届き、おそいS波があとから届く。", defs)


def fig2():
    b = []
    # 左：距離と到着時刻のグラフ（走時曲線）
    X0, Y0, kx, ky = 118, 560, 1.72, 4.6          # 1 km・1秒あたりの px
    DX, TY = 300, 80
    gx = lambda d: X0 + d * kx
    gy = lambda t: Y0 - t * ky
    b.append(text(48, 122, "震源からの距離と、波が届くまでの時間", 18, INK, 700))
    b.append(axes(X0, Y0, DX * kx, TY * ky, "", "", [(d * kx, str(d)) for d in range(0, DX + 1, 50)],
                  [(t * ky, str(t)) for t in range(10, TY + 1, 10)], 15))
    b.append(text(X0 - 8, Y0 - TY * ky - 24, "地震が起きてからの時間［秒］", 15, INK, anchor="start"))
    b.append(text(X0 + DX * kx, Y0 + 46, "震源からの距離（震源距離）［km］", 15, INK, anchor="end"))
    DM = DX * 0.97
    b.append(f'<path d="M{gx(0)},{gy(0)} L{gx(DM):.1f},{gy(DM / VS):.1f} L{gx(DM):.1f},{gy(DM / VP):.1f}Z" fill="{TEAL}" opacity=".10"/>')
    b.append(line(gx(0), gy(0), gx(DX), gy(DX / VP), TEAL, 3.2) + line(gx(0), gy(0), gx(DX * 0.97), gy(DX * 0.97 / VS), ACC, 3.2))
    b.append(line(gx(8), gy(76) - 6, gx(8) + 30, gy(76) - 6, ACC, 3.2) + text(gx(8) + 38, gy(76), f"S波が届く時刻（秒速{VS:g} km）", 16, ACC, 700))
    b.append(line(gx(8), gy(70) - 6, gx(8) + 30, gy(70) - 6, TEAL, 3.2) + text(gx(8) + 38, gy(70), f"P波が届く時刻（秒速{VP:g} km）", 16, TEAL_D, 700))
    for i in range(5):
        x = gx(D[i]); y1, y2 = gy(TP[i]), gy(TS[i])
        b.append(line(x, y1 - 4, x, y2 + 4, INK, 2) + f'<path d="M{x - 5:.1f},{y1 - 6:.1f} l5,8 l5,-8z M{x - 5:.1f},{y2 + 6:.1f} l5,-8 l5,8z" fill="{INK}"/>')
        b.append(circle(x, y1, 4.5, TEAL, "#fff", 1.4) + circle(x, y2, 4.5, ACC, "#fff", 1.4))
        b.append(text(x + 8, (y1 + y2) / 2 + 5, f"{TS[i] - TP[i]:.0f}秒", 15, INK, 700))
        b.append(text(x, Y0 - 10, ST[i][0], 15, INK2, 700, "middle"))
    b.append(text(gx(8), gy(62), "たての矢印の長さ＝初期微動継続時間", 15, INK2))
    b.append(text(gx(8), gy(57), "距離が2倍になると、2倍になる（比例）", 15, INK2))
    # 右：式と早見表
    RX = 700
    b.append(rect(RX, 104, 452, 196, CARD, LINE, 10))
    b.append(text(RX + 20, 136, "震源距離の求め方（大森公式）", 18, INK, 700))
    b.append(text(RX + 20, 172, "震源距離 ＝", 18, INK, 700))
    b.append(text(RX + 136, 172, "P波の速さ × S波の速さ", 16, INK, anchor="start"))
    b.append(line(RX + 132, 182, RX + 340, 182, INK, 1.4))
    b.append(text(RX + 236, 204, "P波の速さ − S波の速さ", 16, INK, anchor="middle"))
    b.append(text(RX + 350, 194, "× 初期微動", 16, INK))
    b.append(text(RX + 368, 214, "継続時間", 16, INK))
    b.append(text(RX + 20, 248, f"例：{VP:g} × {VS:g} ÷ （{VP:g} − {VS:g}）＝ {K:.1f}", 17, ACC, 700))
    b.append(text(RX + 20, 278, f"→ 震源距離 ＝ {K:.1f} × 初期微動継続時間", 17, ACC, 700))
    pairs = [(6, 3.5), (8, 4)]
    ks = [p * s / (p - s) for p, s in pairs]
    rows = [[f"{t}秒"] + [f"{k * t:.0f} km" for k in ks] for t in (5, 10, 15, 20, 25, 30)]
    b.append(text(RX, 334, "初期微動継続時間から震源距離を求める早見表", 16, INK, 700))
    b.append(table(RX, 348, ["初期微動継続時間", f"P{pairs[0][0]:g}・S{pairs[0][1]:g}（×{ks[0]:.1f}）", f"P{pairs[1][0]:g}・S{pairs[1][1]:g}（×{ks[1]:.0f}）"],
                   rows, [156, 148, 148], 36, 16))
    return svg("".join(b), "初期微動継続時間と震源距離（まとめ）",
               "表の「P6・S3.5」はP波6 km/秒・S波3.5 km/秒のこと（シミュの初期値。深さ10 kmでA〜E地点は約84〜252 km）。")


FIGS = [
    dict(svg=fig1,
         alt="地震のP波とS波のしくみの図。地下の震源から速いP波（秒速6 km）とおそいS波（秒速3.5 km）が同心円状に広がる断面と、震源距離84 kmのA地点・126 kmのB地点の地震計の記録を並べ、P波が届くと初期微動、S波が届くと主要動が始まり、その差の初期微動継続時間がA地点10秒・B地点15秒になることを示す。",
         caption="P波・S波と初期微動継続時間のしくみ。震源から遠いほど、P波とS波の届く時間の差が大きくなる。"),
    dict(svg=fig2,
         alt="震源からの距離とP波・S波が届くまでの時間のグラフ（A〜E地点の初期微動継続時間10〜30秒）と、震源距離＝P波の速さ×S波の速さ÷（P波の速さ−S波の速さ）×初期微動継続時間の式（係数8.4）、初期微動継続時間から震源距離を求める早見表。",
         caption="初期微動継続時間と震源距離のまとめ。初期微動継続時間は震源距離に比例する（大森公式）。"),
]
