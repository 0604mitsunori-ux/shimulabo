"""種子の発芽と成長の条件（hatsuga-jouken・小5）の授業用の図。条件・判定・高さは scripts/rika/sims_shokubutsu.py（ページのJS）と同じ。"""
import math
from figlib import *

# ---- シミュと同じ決まり
GD = 3                                         # 水をあたえてから根が出る（発芽する）まで：3日（目安）
B0 = dict(w=1, a=1, t=1, s=1, f=0)            # 基本のカップ（肥料なしの土）
KEYS, NM = ["w", "a", "t", "s", "f"], ["水", "空気", "温度", "日光", "肥料"]
NEED = ["水", "空気", "適当な温度", "日光", "肥料"]
PRE = [("①", "水は必要？", "", [{}, {"w": 0}]),
       ("②", "空気は必要？", "水にしずめる", [{}, {"a": 0}]),
       ("③", "温度は関係する？", "冷蔵庫と箱", [{"s": 0}, {"t": 0, "s": 0}]),
       ("④", "まちがいやすい|比べ方", "（窓辺と冷蔵庫）", [{}, {"t": 0, "s": 0}]),
       ("⑤", "日光は発芽に必要？", "", [{}, {"s": 0}])]


def mk(o): c = dict(B0); c.update(o); return c
def germ(c): return bool(c["w"] and c["a"] and c["t"])          # 発芽に必要なのは水・空気・適当な温度


def hgt(s, f, g):
    """発芽してからの日数 g → 土の上の高さ(cm)（JS の hgt と同じ）"""
    if g < 2.5: return 0.0
    hm, tau = (28, 8) if (s and f) else ((16, 6) if s else (36, 7))
    return 2 + (hm - 2) * (1 - math.exp(-(g - 2.5) / tau))


def chip(c, j):
    if j == 0: return ("あり", 1) if c["w"] else ("なし", 0)
    if j == 1: return ("ふれる", 1) if c["a"] else ("しずめる", 0)
    if j == 2: return ("あたたかい", 1) if c["t"] else ("冷蔵庫", 0)
    if j == 3: return ("当てる", 1) if c["s"] else (("箱で暗く", 0) if c["t"] else ("暗い", 0))
    return ("あり", 1) if c["f"] else ("なし", 0)


def judge(A, B):
    """JS の comp() と同じ考え方で「わかること」を決める"""
    dif = [n for n, k in enumerate(KEYS) if A[k] != B[k]]
    ga, gb = germ(A), germ(B)
    if len(dif) >= 2:
        return ["ちがう条件が%dつ" % len(dif), "（%s）" % "・".join(NM[n] for n in dif), "→ 原因が分からない"], ACC, dif
    d0 = dif[0]
    if ga != gb: return ["発芽には", NEED[d0] + "が必要"], TEAL_D, dif
    if ga and gb: return ["発芽に" + NM[d0] + "は", "必要ない"], TEAL_D, dif
    return ["どちらも発芽しない", ""], INK, dif


def fig1():
    X = [48, 216, 260, 376, 492, 608, 724, 840, 956, 1152]     # 列の区切り
    b = []
    hy, hh = 104, 36
    b.append(rect(48, hy, 1104, hh, TEAL_L, TEAL_L, 8))
    for i, t in enumerate(["調べること", "カップ", "水", "空気", "温度", "日光", "肥料", "結果", "わかること"]):
        b.append(text((X[i] + X[i + 1]) / 2, hy + 24, t, 16, INK, 700, "middle"))
    y = hy + hh + 8; RH, GAP = 36, 10
    for k, (no, q, sub, pre) in enumerate(PRE):
        A, B = mk(pre[0]), mk(pre[1])
        concl, col, dif = judge(A, B)
        bad = len(dif) >= 2
        b.append(rect(48, y - 2, 1104, RH * 2 + 4, "#fdf3f0" if bad else CARD, LINE, 8))
        qs = q.split("|")
        if len(qs) == 2:
            b.append(text(58, y + 22, no + " " + qs[0], 16, ACC if bad else INK, 700) + text(82, y + 44, qs[1], 16, ACC if bad else INK, 700)
                     + text(82, y + 66, sub, 14, MUTED))
        else:
            b.append(text(58, y + (28 if sub else 42), no + " " + q, 16, ACC if bad else INK, 700))
            if sub: b.append(text(82, y + 54, sub, 14, MUTED))
        for r, (lab, c) in enumerate([("A", A), ("B", B)]):
            yy = y + r * RH
            b.append(badge((X[1] + X[2]) / 2, yy + RH / 2, lab, INK2, "#fff", 14))
            for j in range(5):
                s, ok = chip(c, j)
                x0, x1 = X[2 + j] + 6, X[3 + j] - 6
                b.append(rect(x0, yy + 4, x1 - x0, RH - 8, "#e4f1e8" if ok else ACC_L, "#9cc8a9" if ok else "#e6a99b", 6, 1))
                b.append(text((x0 + x1) / 2, yy + 24, s + (" ○" if ok else " ×"), 14.5, GREEN if ok else ACC, 700, "middle"))
            g = germ(c)
            b.append(text((X[7] + X[8]) / 2, yy + 24, "発芽する" if g else "発芽しない", 16, TEAL_D if g else ACC, 700, "middle"))
        for j in dif:                                           # ちがう条件の列を金のわくで囲む
            b.append(rect(X[2 + j] + 2, y, X[3 + j] - X[2 + j] - 4, RH * 2, "none", GOLD, 6, 3))
        if len(concl) == 3:
            b.append(lines(X[8] + 12, y + 20, concl, 15.5, col, 1.42, weight=700))
        else:
            b.append(text(X[8] + 12, y + 30, concl[0], 15.5, col, 700) + text(X[8] + 12, y + 54, concl[1], 15.5, col, 700))
        y += RH * 2 + GAP
    b.append(rect(48, y + 6, 26, 20, "none", GOLD, 5, 3) + text(84, y + 22, "＝くらべる2つでちがう条件。ちがう条件が1つだけなら、結果のちがいはその条件のせいだと分かる。", 16, INK))
    b.append(text(48, y + 52, "③：冷蔵庫の中は暗いので、部屋のカップにも箱をかぶせて暗くし、ちがう条件を温度だけにする（④は温度と日光の2つがちがう）。", 16, INK2))
    return svg("".join(b), "発芽の条件を調べる実験（変える条件は1つだけ）",
               "インゲンマメ・肥料をふくまない土の場合。部屋は約20〜25℃、冷蔵庫は約5℃。結果はシミュレーションと同じ決まり。")


def fig2():
    b = []
    # 左：早見表
    x, y, cw, rh = 48, 104, [150, 165, 165], 46
    rows = [("水", "必要", "必要"), ("空気", "必要", "必要"), ("適当な温度", "必要", "関係する"),
            ("日光", "必要ない", "必要"), ("肥料", "必要ない", "関係する")]
    fill = {"必要": "#e4f1e8", "必要ない": "#eeeeec", "関係する": GOLD_L}
    tc = {"必要": GREEN, "必要ない": MUTED, "関係する": GOLD}
    tw = sum(cw)
    b.append(rect(x, y, tw, rh * 6, CARD, LINE, 10))
    b.append(f'<rect x="{x}" y="{y}" width="{tw}" height="{rh}" rx="10" fill="{TEAL_L}"/>')
    for i, t in enumerate(["条件", "発芽", "成長"]):
        b.append(text(x + sum(cw[:i]) + cw[i] / 2, y + 30, t, 18, INK, 700, "middle"))
    for r, (c, g, s) in enumerate(rows):
        yy = y + rh * (r + 1)
        b.append(line(x, yy, x + tw, yy, LINE, 1))
        b.append(text(x + cw[0] / 2, yy + 30, c, 18, INK, 700, "middle"))
        for k, v in enumerate((g, s)):
            x0 = x + sum(cw[:k + 1]) + 8
            b.append(rect(x0, yy + 8, cw[k + 1] - 16, rh - 16, fill[v], fill[v], 6, 0))
            b.append(text(x0 + (cw[k + 1] - 16) / 2, yy + 30, v, 17, tc[v], 700, "middle"))
    b.append(text(x, y + rh * 6 + 30, "発芽に必要なのは「水・空気・適当な温度」の3つ。", 17, INK, 700))
    b.append(text(x, y + rh * 6 + 56, "日光と肥料は、発芽したあと、よく育つために必要。", 17, INK, 700))
    # 左下：子葉のでんぷん
    by = 448
    b.append(rect(x, by, tw, 162, "#f4eff8", "#d9cde6", 10))
    b.append(text(x + 16, by + 30, "発芽の養分は、子葉の中のでんぷん", 17, PURPLE, 700))
    for k, (cy, col, t1, t2) in enumerate([(by + 74, "#4b2a6b", "発芽する前の子葉", "ヨウ素液で青むらさき色（でんぷんがある）"),
                                           (by + 128, "#e8d9b4", "育ったあとの子葉（しぼんだもの）", "色がほとんど変わらない（でんぷんが使われた）")]):
        cx = x + 46
        b.append(f'<ellipse cx="{cx}" cy="{cy}" rx="24" ry="15" fill="{col}" stroke="#7a5a2a" stroke-width="1.4"/>'
                 + line(cx - 24, cy, cx + 24, cy, "#7a5a2a", 1.2))
        b.append(text(cx + 36, cy - 4, t1, 15, INK, 700) + text(cx + 36, cy + 18, "→ " + t2, 15, INK2))
    # 右：成長のグラフ
    gx, gy, gw, gh = 610, 512, 280, 350             # 0〜20日・0〜35cm
    px, py = gw / 20, gh / 35
    b.append(text(gx - 40, 120, "水をあたえてからの日数と、くきの高さ", 18, INK, 700))
    b.append(text(gx + 12, gy - gh - 2, "高さ（cm）", 15, INK))
    b.append(axes(gx, gy, gw, gh, "", "", [(d * px, f"{d}") for d in (0, 5, 10, 15, 20)],
                  [(h * py, f"{h}") for h in (10, 20, 30)], 15))
    b.append(text(gx + gw / 2, gy + 46, "水をあたえてからの日数（日）", 15, INK, anchor="middle"))
    b.append(line(gx + GD * px, gy, gx + GD * px, gy - gh, MUTED, 1.4, "4 4"))
    b.append(text(gx + GD * px + 6, gy - gh + 26, f"{GD}日目ごろ 発芽（根が出る）", 14.5, MUTED))
    CUR = [((1, 1), GREEN, None, "日光と肥料あり", "葉が多く大きい・こい緑色"),
           ((1, 0), TEAL, "8 5", "日光あり・肥料なし", "葉が少なく小さい"),
           ((0, 1), GOLD, "2 5", "日光なし", "ひょろ長く、葉が黄色っぽい")]
    for (s, f), col, dash, n1, n2 in CUR:
        pts = [(gx + (GD + g) * px, gy - hgt(s, f, g) * py) for g in [2.5 + i * 0.1 for i in range(int((20 - GD - 2.5) / 0.1) + 1)]]
        b.append(poly(pts, col, 3.6, dash=dash) + circle(pts[0][0], pts[0][1], 4, col, col, 0))
        h20 = hgt(s, f, 20 - GD); ey = gy - h20 * py
        b.append(circle(gx + gw, ey, 5, col, col, 0))
        b.append(text(gx + gw + 14, ey - 2, f"{n1} 約{round(h20)}cm", 16, col, 700) + text(gx + gw + 14, ey + 20, n2, 14.5, INK2))
    b.append(rect(gx - 40, 562, 582, 50, CARD, LINE, 8))
    b.append(text(gx - 28, 582, "日光なし：くきは長くのびるが、ひょろ長く弱い（よく育ったとはいえない）。", 14.5, INK2))
    b.append(text(gx - 28, 604, "肥料なし：日光が当たっても、葉の数が少なく小さい。", 14.5, INK2))
    return svg("".join(b), "発芽の条件と成長の条件（まとめ）",
               "高さは、あたたかい部屋で育てたときの目安（シミュレーションと同じ式）。5〜6日目ごろ、子葉が土の上に出る。")


FIGS = [
    dict(svg=fig1, alt="インゲンマメの発芽の条件を調べる5つの比べ方（水・空気・温度・まちがいやすい比べ方・日光）について、2つのカップの水・空気・温度・日光・肥料の条件と、発芽したかどうか、わかることを並べた表。ちがう条件は1つだけにし、冷蔵庫とくらべるカップには箱をかぶせる。",
         caption="条件のそろえ方。くらべる2つのカップでちがう条件を1つだけにすると、発芽に必要な条件が分かる。"),
    dict(svg=fig2, alt="発芽の条件と成長の条件の早見表（発芽に必要なのは水・空気・適当な温度、日光と肥料は成長に必要）と、日光と肥料あり・日光あり肥料なし・日光なしのインゲンマメの20日間のくきの高さのグラフ、子葉のでんぷんをヨウ素液で調べた結果。",
         caption="発芽の条件と成長の条件。発芽には水・空気・適当な温度、よく育つには日光と肥料が必要。"),
]
