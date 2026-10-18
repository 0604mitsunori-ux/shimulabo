"""記録タイマーと台車の運動（kiroku-timer・中3 運動の規則性）の授業用の図
数値はシミュ（scripts/rika/sims_undou_shigoto.py の KIROKU_JS の calc()）と同じ：a＝9.8×sinθ、x(t)＝v0·t＋a·t²/2、
1秒間に50回打点、0.1秒ごとのテープ、斜面の長さ2.0m・最長1.0秒で記録終了。"""
import math
from figlib import *

G, TMAX, LTR = 9.8, 1.0, 2.0


def calc(th, v0=0.0, hz=50):
    """シミュの calc() と同じ（長さは m）"""
    a = G * math.sin(math.radians(th))
    X = lambda t: v0 * t + a * t * t / 2
    tEnd = TMAX
    if X(TMAX) > LTR:
        tEnd = (-v0 + math.sqrt(v0 * v0 + 2 * a * LTR)) / a if a > 1e-9 else LTR / v0
    nd = math.floor(tEnd * hz + 1e-9)
    dots = [X(k / hz) for k in range(nd + 1)]
    np_ = math.floor(tEnd * 10 + 1e-9)
    pcs = [(X(j / 10), X((j + 1) / 10) - X(j / 10)) for j in range(np_)]
    return dict(a=a, v0=v0, X=X, tEnd=tEnd, dots=dots, pcs=pcs, hz=hz)


def f2(v): return "%.2f" % (math.floor(v * 100 + 0.5) / 100)      # JS (Math.round(v*100)/100).toFixed(2)


CIR = "①②③④⑤⑥⑦⑧⑨⑩"
PCF, PCS = [GOLD_L, TEAL_L], [GOLD, TEAL]


def tape_graph(x0, y0, slot, bw, sc, c, h, nums=True, numsize=14):
    """テープグラフ（0.1秒ごとのテープを左から順にならべる）。sc＝1cmあたりのpx"""
    out, tops = [], []
    for j, (_, L) in enumerate(c["pcs"]):
        hh = L * 100 * sc
        x = x0 + j * slot + (slot - bw) / 2
        out.append(rect(x, y0 - hh, bw, hh, PCF[j % 2], PCS[j % 2], 1.5, 1.2))
        tops.append((x + bw / 2, y0 - hh))
        if nums:
            out.append(text(x + bw / 2, y0 + 20, CIR[j], numsize, PCS[j % 2], 700, "middle"))
    if len(tops) >= 2:
        out.append(poly(tops, ACC, 2, dash="6 4"))
    return "".join(out)


def fig1():
    c = calc(15)
    b = []
    # ---- 左上：斜面と記録タイマー（模式図）
    th = math.radians(15)
    X0, Y0, run = 82, 150, 320
    X1, Y1 = X0 + run, Y0 + run * math.tan(th)
    b.append(f'<path d="M{X0},{Y0 + 3} L{X1:.1f},{Y1 + 3:.1f} L{X0},{Y1 + 3:.1f}Z" fill="#e7e3d8"/>')
    b.append(line(X0, Y0, X1, Y1, "#9a958a", 4) + line(56, Y1 + 3, 420, Y1 + 3, "#9a958a", 3))
    ra = 52
    b.append(f'<path d="M{X1 - ra:.1f},{Y1 + 3:.1f} A{ra},{ra} 0 0 1 {X1 - ra * math.cos(th):.1f},{Y1 + 3 - ra * math.sin(th):.1f}" fill="none" stroke="{ACC}" stroke-width="2"/>')
    b.append(text(X1 - ra - 10, Y1 - 4, "15°", 16, ACC, 700, "end"))
    co, si = math.cos(th), math.sin(th)
    # 記録タイマー（斜面の上の端）
    tx, ty = X0 + 18 * co + si * 16, Y0 + 18 * si - co * 16
    b.append(f'<g transform="translate({tx:.1f},{ty:.1f}) rotate(15)"><rect x="-22" y="-13" width="44" height="26" rx="4" fill="{INK2}"/><rect x="14" y="-4" width="8" height="8" fill="{ACC}"/></g>')
    b.append(text(60, 116, "記録タイマー（1秒間に50回、点を打つ）", 15, INK, 700))
    # 台車
    u = 120
    px, py = X0 + u * co, Y0 + u * si
    b.append(f'<g transform="translate({px:.1f},{py:.1f}) rotate(15)"><rect x="0" y="-30" width="62" height="20" rx="4" fill="{TEAL}"/>'
             f'<circle cx="13" cy="-6" r="6" fill="{MOON_D}"/><circle cx="49" cy="-6" r="6" fill="{MOON_D}"/></g>')
    # テープ（タイマー → 台車の後ろ）
    b.append(line(tx + 22 * co, ty + 22 * si, px + si * 20, py - co * 20, "#e3b341", 4))
    t0x, t0y, t1x, t1y = tx + 22 * co, ty + 22 * si, px + si * 20, py - co * 20
    mx, my = (t0x + t1x) / 2 + si * 12, (t0y + t1y) / 2 - co * 12
    b.append(text(mx, my, "記録テープ", 14, GOLD, 700, "middle", transform=f"rotate(15 {mx:.1f} {my:.1f})"))
    # 斜面に沿った力（台車の前に向きだけ示す）
    s0, s1 = u + 66, u + 126
    ax0, ay0 = X0 + s0 * co + si * 20, Y0 + s0 * si - co * 20
    ax1, ay1 = X0 + s1 * co + si * 20, Y0 + s1 * si - co * 20
    b.append(arrow(ax0, ay0, ax1, ay1, "acc", 3.4))
    lx, ly = X0 + (u + 92) * co + si * 36, Y0 + (u + 92) * si - co * 36
    b.append(text(lx, ly, "斜面に沿った力（一定）", 14, ACC, 700, "middle", transform=f"rotate(15 {lx:.1f} {ly:.1f})"))
    # ---- 右上：記録テープ（はじめの0.4秒）
    x0, yt, S = 462, 178, 33                     # 1cm＝33px
    n4 = 4; L4 = c["pcs"][n4 - 1][0] + c["pcs"][n4 - 1][1]
    b.append(text(456, 132, "記録テープ（はじめの0.4秒）：5打点＝0.1秒ごとに色分け", 16, INK, 700))
    for j in range(n4):
        s0, L = c["pcs"][j]
        b.append(f'<rect x="{x0 + s0 * 100 * S:.1f}" y="{yt}" width="{L * 100 * S:.1f}" height="34" fill="{PCF[j % 2]}" stroke="{PCS[j % 2]}" stroke-width="1"/>')
        cx = x0 + (s0 + L / 2) * 100 * S
        b.append(text(cx, yt - 8, "0.1秒", 14, INK2, anchor="middle"))
        b.append(text(cx, yt + 58, CIR[j], 17, PCS[j % 2], 700, "middle"))
        b.append(text(cx, yt + 80, f"{f2(L * 100)}cm", 15, INK, 700, "middle"))
    for k in range(5 * n4 + 1):
        b.append(circle(x0 + c["dots"][k] * 100 * S, yt + 17, 2.8, INK, INK, 0))
    b.append(text(462, 284, "← 打ち始め（点の間かくがせまい）", 14, MUTED))
    b.append(text(x0 + L4 * 100 * S, 284, "点の間かくが広くなる → 速くなっている", 14, MUTED, anchor="end"))
    # ---- 左下：テープグラフ
    gx0, gy0, slot, sc = 110, 570, 46, 9
    b.append(text(60, 314, "テープグラフ（0.1秒ごとに切って、左から順にならべる）", 17, INK, 700))
    b.append(axes(gx0, gy0, 10 * slot, 230, "", "", [], [(v * sc, str(v)) for v in range(0, 26, 5)], 14))
    b.append(text(gx0 + 12, 340, "テープの長さ（cm）", 14, INK2))
    b.append(tape_graph(gx0, gy0, slot, 38, sc, c, 230))
    for j, lab in [(0, "0"), (5, "0.5"), (10, "1.0秒")]:
        b.append(text(gx0 + j * slot, gy0 + 42, lab, 14, INK2, anchor="middle"))
    b.append(text(gx0 + 18, 372, "点線：テープの上の端をつないだ線", 14, ACC, 700))
    # ---- 右下：読み方
    a_cm = c["a"]                                   # 1本ごとに a×0.1²[m]＝a[cm] 長くなる
    L3 = c["pcs"][2][1] * 100
    items = [("テープ1本の長さ ＝ 0.1秒間に進んだ距離", "→ テープの長さは速さに比例する"),
             ("0.1秒間の平均の速さ ＝ テープの長さ ÷ 0.1秒", f"例：③ {f2(L3)}cm ÷ 0.1秒 ≒ {round(L3 * 10)}cm/s"),
             (f"1本ごとに {f2(a_cm)}cm ずつ長くなる", "→ 速さが一定の割合で増える運動"),
             ("上の端をつなぐと、速さ－時間のグラフと同じ形", "斜面を下る台車は右上がりの直線になる")]
    for i, (h, s) in enumerate(items):
        y = 346 + i * 68
        b.append(badge(668, y - 6, str(i + 1), TEAL, "#fff", 15))
        b.append(text(690, y, h, 17, INK, 700) + text(690, y + 25, s, 15.5, INK2))
    return svg("".join(b), "記録タイマーとテープグラフのしくみ（斜面を下る台車）",
               "斜面の角度15°・1秒間に50回打点の記録（シミュレーションのはじめの設定）。摩擦と空気の抵抗は考えない。斜面の図は模式図。")


def fig2():
    b = []
    cases = [(0, 0.5, "水平（0°）で押す", "等速直線運動（50cm/s）"),
             (15, 0.0, "斜面 15°", "だんだん速くなる"),
             (30, 0.0, "斜面 30°", "だんだん速くなる"),
             (90, 0.0, "90°（自由落下）", "速さの増え方がいちばん大きい")]
    sc, slot = 4.8, 20                               # 4つのグラフは同じ目もり（1cm＝4.8px）
    for i, (th, v0, ttl, sub) in enumerate(cases):
        c = calc(th, v0)
        px = 48 + i * 280
        b.append(rect(px, 96, 264, 522, CARD, LINE, 10))
        b.append(f'<rect x="{px}" y="96" width="264" height="62" rx="10" fill="{TEAL_L}"/>')
        b.append(text(px + 132, 123, ttl, 18, INK, 700, "middle"))
        b.append(text(px + 132, 147, sub, 14.5, INK2, anchor="middle"))
        x0, y0 = px + 42, 452
        b.append(axes(x0, y0, 10 * slot, 266, "", "", [], [(v * sc, str(v)) for v in range(0, 51, 10)], 14))
        b.append(text(x0 + 8, 186, "（cm）", 14, INK2))
        b.append(tape_graph(x0, y0, slot, 15, sc, c, 266, nums=False))
        for j, lab in [(0, "0"), (5, "0.5"), (10, "1.0秒")]:
            b.append(text(x0 + j * slot, y0 + 20, lab, 14, INK2, anchor="middle"))
        inc = f2(c["a"]) + "cm" if th else "0cm"
        v05 = round((c["v0"] + c["a"] * 0.5) * 100)          # シミュの「0.5秒後の速さ」
        b.append(text(px + 68, 498, "1本ごとの増え", 14, MUTED, anchor="middle") + text(px + 196, 498, "0.5秒後の速さ", 14, MUTED, anchor="middle"))
        b.append(text(px + 68, 528, inc, 21, ACC, 700, "middle") + text(px + 196, 528, f"{v05}cm/s", 21, TEAL_D, 700, "middle"))
        if th == 0:
            note = "力がはたらかない（慣性）"
        elif th == 90:
            note = "a ＝ 9.8m/s²"
        else:
            note = f"a ＝ 9.8×sin{th}° ≒ {f2(c['a'])}m/s²"
        b.append(line(px + 16, 548, px + 248, 548, LINE, 1))
        b.append(text(px + 132, 574, note, 15, INK2, anchor="middle"))
        end = "1.0秒で記録終了" if c["tEnd"] >= TMAX else f"{f2(c['tEnd'])}秒で2.0m{'落ちて' if th == 90 else '進み'}記録終了"
        b.append(text(px + 132, 600, end, 14, MUTED, anchor="middle"))
    return svg("".join(b), "斜面の角度とテープグラフ（まとめ）",
               "4つのグラフは同じ目もり。角度が大きいほど、テープの長さの増え方（速さの増え方）が大きい。摩擦なし。")


FIGS = [
    dict(svg=fig1, alt="記録タイマーとテープグラフのしくみの図。15°の斜面を下る台車の記録テープ（1秒間に50回打点、5打点＝0.1秒ごとに1.27・3.80・6.34・8.88cm）と、0.1秒ごとに切ってならべたテープグラフ。テープは1本ごとに2.54cmずつ長くなり、上の端をつなぐと速さ－時間のグラフと同じ右上がりの直線になる。",
         caption="記録タイマーの打点とテープグラフ。0.1秒ごとのテープの長さが速さを表し、斜面では一定の割合で長くなる。"),
    dict(svg=fig2, alt="斜面の角度ごとのテープグラフのまとめ図。水平で押すと等速直線運動（テープはどれも5.00cm）、15°・30°・90°（自由落下）ではテープが1本ごとに2.54cm・4.90cm・9.80cmずつ長くなり、0.5秒後の速さは50・127・245・490cm/s。",
         caption="斜面の角度とテープグラフ。角度が大きいほど速さの増え方が大きく、90°で自由落下になる。"),
]
