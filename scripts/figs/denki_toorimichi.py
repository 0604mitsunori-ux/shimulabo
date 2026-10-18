"""電気の通り道（denki-toorimichi・小3）の授業用の図。
明かりがつく・つかないの判定は、ページのシミュの ev() と本文の「つなぎ方の早見表」「電気を通す物・通さない物の早見表」と同じ。
小3では電流の向きは扱わない（第4学年）ので、通り道は向きのない黄色の粒でかく（シミュと同じ）。"""
import math
from figlib import *

BAT, WIRE_P, WIRE_M, PATH, DOT = "#2f5f86", "#c4442b", "#3d434b", "#f4d35e", "#d99a06"


def battery(x, top, bot, w, label=True, size=1.0):
    """たて置きのかん電池（上が＋きょく＝出っぱっている方）"""
    bw = w * 0.34
    out = rect(x - bw / 2, top - 14 * size, bw, 15 * size, "#c9c4b8", MUTED, 3, 1.2)
    out += rect(x - w / 2, top, w, bot - top, BAT, BAT, 8 * size, 0) + f'<rect x="{x - w / 2:.1f}" y="{bot - 9 * size:.1f}" width="{w:.1f}" height="{9 * size:.1f}" fill="#c9c4b8"/>'
    out += text(x, top + 28 * size, "＋", 22 * size, "#fff", 700, "middle") + text(x, bot - 16 * size, "－", 22 * size, "#fff", 700, "middle")
    if label:
        out += text(x, (top + bot) / 2 - 2, "かん", 16, "#fff", 700, "middle") + text(x, (top + bot) / 2 + 18, "電池", 16, "#fff", 700, "middle")
    return out


def bulb(x, y, r, lit=True, sock=True):
    """豆電球（ガラスの中心 x,y）とソケット。もどり値＝(SVG, 左のねじ, 右のねじ)"""
    out = ""
    if lit:
        out += f'<circle cx="{x}" cy="{y}" r="{r * 1.9:.1f}" fill="{SUN}" opacity=".28"/>'
    out += circle(x, y, r, "#fff3b0" if lit else CARD, MUTED, 1.6)
    fy = y - r * 0.05
    out += poly([(x - r * 0.3, y + r * 0.8), (x - r * 0.3, fy)], MUTED, 1.4) + poly([(x + r * 0.3, y + r * 0.8), (x + r * 0.3, fy)], MUTED, 1.4)
    out += poly([(x - r * 0.3 + i * r * 0.1, fy + (r * 0.14 if i % 2 else -r * 0.14)) for i in range(7)], ACC if lit else INK2, 2)
    out += rect(x - r * 0.5, y + r * 0.82, r, r * 0.55, "#cfc9bb", MUTED, 2, 1.2)
    if not sock:
        return out, None, None
    sy = y + r * 1.3
    out += rect(x - r * 1.05, sy, r * 2.1, r * 0.95, "#ece8de", MUTED, 6, 1.2)
    lt, rt = (x - r * 0.78, sy + r * 0.6), (x + r * 0.78, sy + r * 0.6)
    out += circle(*lt, r * 0.13, "#bdb6a6", MUTED, 1) + circle(*rt, r * 0.13, "#bdb6a6", MUTED, 1)
    return out, lt, rt


def path_len(P):
    return sum(math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]) for i in range(1, len(P)))


def dots(P, gap=26, r=4.2):
    out, L, acc, i = [], path_len(P), gap / 2, 1
    segs = [(P[k - 1], P[k], math.hypot(P[k][0] - P[k - 1][0], P[k][1] - P[k - 1][1])) for k in range(1, len(P))]
    s = gap / 2
    while s < L:
        t = s
        for a, c, l in segs:
            if t <= l:
                out.append(circle(a[0] + (c[0] - a[0]) * t / l, a[1] + (c[1] - a[1]) * t / l, r, PATH, DOT, 1.2)); break
            t -= l
        s += gap
    return "".join(out)


def wire(P, col, w=5):
    return poly(P, col, w)


def fig1():
    b = []
    # ===== 左：明かりがつく回路 =====
    b.append(rect(48, 100, 650, 512, CARD, LINE, 12))
    b.append(text(70, 136, "明かりがつくつなぎ方", 21, INK, 700) + text(292, 136, "○", 22, GREEN, 700))
    bx, top, bot, gx = 236, 252, 470, 524
    gb, lt, rt = bulb(gx, 206, 40)
    red = [(bx, top - 14), (bx, 176), (gx - 96, 176), (gx - 96, lt[1]), lt]
    blk = [(bx, bot), (bx, 548), (644, 548), (644, rt[1]), rt]
    b.append(poly([lt, (gx - 12, 246), (gx + 12, 246), rt], PATH, 16) + poly(red, PATH, 18) + poly(blk, PATH, 18) + poly([(bx, top), (bx, bot)], PATH, 18))
    b.append(wire(red, WIRE_P) + wire(blk, WIRE_M))
    b.append(battery(bx, top, bot, 84))
    b.append(gb)
    b.append(dots(red) + dots(blk))
    b.append(text(bx - 52, top - 8, "＋きょく", 18, INK, 700, "end") + text(bx - 52, top + 16, "出っぱっている方", 15, INK2, anchor="end"))
    b.append(text(bx - 52, bot - 10, "－きょく", 18, INK, 700, "end") + text(bx - 52, bot + 14, "平らな方", 15, INK2, anchor="end"))
    b.append(text(gx + 60, 176, "豆電球", 18, INK, 700) + text(gx, 322, "ソケット", 15, INK2, anchor="middle"))
    b.append(text(332, 166, "どう線", 16, INK2, anchor="middle") + text(440, 538, "どう線", 16, INK2, anchor="middle"))
    b.append(lines(304, 380, ["＋きょく → 豆電球 → －きょく が、", "どう線で 1つの「わ」に", "なると、明かりがつく。"], 18, INK, 1.55))
    b.append(text(304, 474, "この電気の通り道を「回路」という。", 16, TEAL_D, 700))
    b.append(circle(70, 594, 7, PATH, DOT, 1.2) + text(84, 600, "黄色の粒＝電気が通っている所（シミュと同じ表し方）", 15, INK2))
    # ===== 右：豆電球の中の通り道 =====
    x0 = 722
    b.append(rect(x0, 100, 430, 512, CARD, LINE, 12))
    b.append(text(x0 + 22, 136, "豆電球の中の通り道", 21, INK, 700))
    cx, cy, R = 900, 262, 96
    b.append(circle(cx, cy, R, "#fffbe6", MUTED, 2))
    fy = cy - 12
    path = [(cx - 50, 380), (cx - 34, 366), (cx - 26, fy), (cx + 26, fy), (cx + 26, 360), (cx, 400), (cx, 468)]
    b.append(poly(path, PATH, 16))
    b.append(rect(cx - 50, 348, 100, 78, "#d3cdbf", MUTED, 4, 1.4))
    for k in range(4):
        b.append(line(cx - 50, 360 + k * 18, cx + 50, 368 + k * 18, "#a8a090", 1.4))
    b.append(rect(cx - 30, 426, 60, 22, "#3b3f46", "#3b3f46", 3, 0) + rect(cx - 14, 448, 28, 16, "#bdb6a6", MUTED, 4, 1.2))
    b.append(poly([(cx - 26, fy), (cx - 26, 366), (cx - 50, 384)], INK2, 2.4) + poly([(cx + 26, fy), (cx + 26, 360), (cx, 402), (cx, 456)], INK2, 2.4))
    b.append(poly([(cx - 26 + i * 52 / 8, fy + (7 if i % 2 else -7)) for i in range(9)], ACC, 3))
    b.append(dots(path, 24, 3.6))
    b.append(line(cx + 34, fy - 8, 1030, 196, MUTED, 1.2) + text(1034, 200, "フィラメント", 16, INK, 700))
    b.append(text(1034, 222, "（光る細い線）", 14, INK2))
    b.append(line(cx - 52, 386, 790, 478, MUTED, 1.2) + text(744, 500, "口金（くちがね）の横", 16, INK, 700))
    b.append(line(cx + 16, 458, 1000, 470, MUTED, 1.2) + text(1004, 466, "おしりの", 16, INK, 700) + text(1004, 488, "出っぱり", 16, INK, 700))
    b.append(lines(x0 + 22, 534, ["口金の横 → フィラメント → おしりの出っぱり", "とつながっている。ソケットがないときは、", "この2か所にどう線を1本ずつつなぐ。"], 16, INK, 1.5))
    return svg("".join(b), "電気の通り道（回路）のしくみ",
               "かん電池の＋きょく・豆電球・－きょくが1つのわにつながると、電気が通って明かりがつく。")


def mini(bx, by, kind):
    """つなぎ方の小さな絵。カード左上 (bx,by)"""
    out = []
    x, top, bot = bx + 44, by + 74, by + 146
    gb, lt, rt = bulb(bx + 122, by + 64, 17, lit=(kind == "ok"))
    plus, minus, side = (x, top - 8), (x, bot), (x + 15, (top + bot) / 2)
    yt, yb = by + 44, by + 162
    if kind == "short":
        x = bx + 87
        out.append(f'<path d="M{x},{top - 8} C{x - 64},{top - 44} {x - 68},{bot + 44} {x},{bot}" fill="none" stroke="{ACC}" stroke-width="6" stroke-linecap="round"/>')
        out.append(battery(x, top, bot, 34, False, 0.7))
        for k in range(3):
            out.append(f'<path d="M{x + 30 + k * 12},{top + 50} q-5,-8 0,-16 q5,-8 0,-16 q-5,-8 0,-16" fill="none" stroke="{ACC}" stroke-width="2.4"/>')
        out.append(text(x + 42, top - 22, "あつい！", 15, ACC, 700, "middle"))
        return "".join(out)
    pw = [(x, top - 8), (x, yt), (lt[0] - 10, yt), (lt[0] - 10, lt[1]), lt]
    end2 = {"ok": minus, "same": plus, "one": None, "side": side, "cut": minus}[kind]
    if kind == "same":
        mw = [(rt[0] + 12, rt[1]), (rt[0] + 12, yt - 12), (x + 4, yt - 12), (x + 4, top - 8)]
        out.append(wire(pw, WIRE_P, 4) + wire([rt] + mw, WIRE_M, 4))
    elif kind == "one":
        out.append(wire(pw, WIRE_P, 4) + wire([rt, (rt[0] + 10, rt[1] + 30), (rt[0] - 8, yb - 4)], WIRE_M, 4))
        out.append(circle(rt[0] - 8, yb - 4, 5, "#d9a35a", "#d9a35a", 0))
    elif kind == "side":
        out.append(wire(pw, WIRE_P, 4) + wire([rt, (rt[0] + 12, rt[1]), (rt[0] + 12, side[1]), side], WIRE_M, 4))
    else:
        mw = [rt, (rt[0] + 12, rt[1]), (rt[0] + 12, yb), (x, yb), minus]
        if kind == "cut":
            n = (rt[0] + 12 + x) / 2
            out.append(wire(pw, WIRE_P, 4) + wire(mw[:3] + [(n + 8, yb)], WIRE_M, 4) + wire([(n - 8, yb), (x, yb), minus], WIRE_M, 4))
            out.append(text(n, yb - 10, "✂", 16, ACC, 700, "middle"))
        else:
            out.append(poly(pw, PATH, 12) + poly(mw, PATH, 12))
            out.append(wire(pw, WIRE_P, 4) + wire(mw, WIRE_M, 4))
    out.append(battery(x, top, bot, 34, False, 0.7))
    out.append(gb)
    return "".join(out)


def fig2():
    b = []
    cases = [("ok", "つく", "○", GREEN, ["＋きょくと－きょく", "わになっている"]),
             ("same", "つかない", "×", MUTED, ["両方とも＋きょく", "わになっていない"]),
             ("one", "つかない", "×", MUTED, ["片方しか", "つないでいない"]),
             ("side", "つかない", "×", MUTED, ["かん電池の横に", "つないでいる"]),
             ("cut", "つかない", "×", MUTED, ["どう線が", "とちゅうで切れている"]),
             ("short", "やってはいけない", "⚠", ACC, ["＋と－をどう線だけで", "つなぐ（ショート回路）"])]
    b.append(text(48, 122, "つなぎ方と明かり", 19, INK, 700))
    for i, (k, res, mk, col, cap) in enumerate(cases):
        bx, by, w = 48 + i * 186, 134, 174
        danger = k == "short"
        b.append(rect(bx, by, w, 272, ACC_L if danger else CARD, ACC if danger else LINE, 10, 2 if danger else 1.2))
        b.append(mini(bx, by, k))
        b.append(text(bx + w / 2, by + 200, f"{mk} {res}", 17 if not danger else 15.5, col, 700, "middle"))
        b.append(text(bx + w / 2, by + 228, cap[0], 14.5, INK, anchor="middle") + text(bx + w / 2, by + 250, cap[1], 14.5, INK, anchor="middle"))
    b.append(text(1150, 122, "ショート回路は、どう線とかん電池が熱くなって あぶない。ぜったいにしない。", 15, ACC, 700, "end"))
    # 下：電気を通す物・通さない物
    y = 424
    b.append(rect(48, y, 540, 190, "#eef5ef", LINE, 12) + rect(612, y, 540, 190, "#f1efe9", LINE, 12))
    b.append(text(68, y + 34, "○ 電気を通す物（金ぞく）", 19, GREEN, 700) + text(632, y + 34, "× 電気を通さない物", 19, INK2, 700))
    for i, s in enumerate(["鉄のくぎ・クリップ（鉄）", "アルミニウムはく（アルミニウム）", "10円玉（どう）", "空きかんの けずった所"]):
        b.append(text(76, y + 72 + i * 32, "・" + s, 16.5, INK))
    for i, s in enumerate(["紙", "プラスチックのじょうぎ", "木のわりばし"]):
        b.append(text(640, y + 72 + i * 32, "・" + s, 16.5, INK))
    for i, s in enumerate(["ガラスのコップ", "消しゴム・わゴム", "空きかんの ぬってある所"]):
        b.append(text(890, y + 72 + i * 32, "・" + s, 16.5, INK))
    b.append(text(640, y + 172, "空きかんは、ぬってある所をけずると電気を通す。", 15, INK2))
    return svg("".join(b), "つなぎ方と電気を通す物（まとめ）",
               "テスター（回路にすき間を作った物）のすき間に物をはさんで、明かりがつけば電気を通す物。")


FIGS = [
    dict(svg=fig1, alt="かん電池の＋きょく、豆電球、－きょくがどう線で1つのわ（回路）につながって明かりがつくようすと、豆電球の中で口金の横からフィラメントを通っておしりの出っぱりまでつながっている電気の通り道を、黄色の粒で示した小3理科「電気の通り道」の図。",
         caption="電気の通り道（回路）。＋きょく・豆電球・－きょくが1つのわになると明かりがつく。"),
    dict(svg=fig2, alt="豆電球に明かりがつくつなぎ方（＋きょくと－きょく）と、つかないつなぎ方（両方とも＋きょく・片方だけ・かん電池の横・どう線が切れている）、やってはいけないショート回路を並べた早見表と、電気を通す物（鉄・アルミニウム・どうなどの金ぞく）と通さない物（紙・プラスチック・木・ガラス・ゴム）のまとめ。",
         caption="つなぎ方と電気を通す物のまとめ。ショート回路はあぶないので、ぜったいにしない。"),
]
