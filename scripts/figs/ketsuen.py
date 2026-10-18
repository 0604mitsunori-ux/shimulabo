"""血のつながり（血縁度）計算（ketsuen）の図。血縁度はページの JS・早見表と同じ（親子・きょうだい1/2、祖父母と孫・おじ甥・異母きょうだい1/4、
いとこ・曾祖父母1/8、いとこの子1/16、はとこ1/32、二重いとこ1/4）。親等は民法726条の数え方（共通の先祖までさかのぼって相手まで下る世代の数）。"""
from fractions import Fraction as F
from figlib import *

ANCHOR = r'<div class="note" style="border-left:4px solid var\(--teal\)">.*?</div>\n'


def r_of(paths):
    """共通の先祖ごとの「1/2をかける回数」から血縁度を計算（各道 (1/2)^回数 の和）"""
    return sum(F(1, 2) ** n for n in paths)


def pct(fr):
    v = float(fr) * 100
    return f"{v:g}%"


# 続柄：(名前, 血縁度, 親等)。血縁度は道の数え方で計算し、ページの値と assert で照合
REL = {
    "父母": (r_of([1]), 1), "子": (r_of([1]), 1), "きょうだい": (r_of([2, 2]), 2),
    "祖父母": (r_of([2]), 2), "おじ・おば": (r_of([3, 3]), 3), "甥・姪": (r_of([3, 3]), 3),
    "曾祖父母": (r_of([3]), 3), "いとこ": (r_of([4, 4]), 4), "いとこの子": (r_of([5, 5]), 5),
    "はとこ": (r_of([6, 6]), 6),
}
PAGE = {"父母": "1/2", "子": "1/2", "きょうだい": "1/2", "祖父母": "1/4", "おじ・おば": "1/4", "甥・姪": "1/4",
        "曾祖父母": "1/8", "いとこ": "1/8", "いとこの子": "1/16", "はとこ": "1/32"}
for k, v in PAGE.items():
    assert str(REL[k][0]) == v, (k, REL[k][0], v)
assert r_of([2]) == F(1, 4) and r_of([4] * 4) == F(1, 4)      # 異母きょうだい・二重いとこ


def box(cx, cy, name, w=190, h=62, kind="rel", sub=None):
    x, y = cx - w / 2, cy - h / 2
    if kind == "me":
        return rect(x, y, w, h, INK, INK, 10) + text(cx, cy + 8, name, 22, "#fff", 700, "middle")
    if kind == "via":
        o = f'<rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" rx="10" fill="{BG}" stroke="{MUTED}" stroke-width="1.4" stroke-dasharray="5 4"/>'
        o += text(cx, cy - 4 if sub else cy + 6, name, 16, INK2, 700, "middle")
        if sub:
            o += text(cx, cy + 18, sub, 14, MUTED, anchor="middle")
        return o
    fr, sh = REL[name]
    hi = kind == "hi"
    o = rect(x, y, w, h, ACC_L if hi else CARD, ACC if hi else TEAL, 10, 2.4 if hi else 1.6)
    o += text(cx, cy - 6, name, 18, INK, 700, "middle")
    o += text(cx, cy + 20, f"{fr}（{pct(fr)}）・{sh}親等", 15.5, ACC if hi else TEAL_D, 700, "middle")
    return o


def fig1():
    b = []
    X = [150, 372, 594, 816]
    Y = [140, 243, 346, 449, 552]
    h = 62
    top, bot = lambda r: Y[r] - h / 2, lambda r: Y[r] + h / 2

    def fork(px, r, kids):
        """親の箱（列px・段r）から、子ども（列のリスト）へ線を引く"""
        ym = (bot(r) + top(r + 1)) / 2
        o = line(px, bot(r), px, ym, INK2, 2)
        xs = [px] + kids
        o += line(min(xs), ym, max(xs), ym, INK2, 2)
        for k in kids:
            o += line(k, ym, k, top(r + 1), INK2, 2)
        return o

    b.append(fork(X[0], 0, [X[0], X[3]]))       # 曾祖父母 → 祖父母・祖父母のきょうだい
    b.append(fork(X[0], 1, [X[0], X[2]]))       # 祖父母 → 父母・おじおば
    b.append(fork(X[3], 1, [X[3]]))             # 祖父母のきょうだい → 親のいとこ
    b.append(fork(X[0], 2, [X[0], X[1]]))       # 父母 → あなた・きょうだい
    b.append(fork(X[2], 2, [X[2]]))             # おじおば → いとこ
    b.append(fork(X[3], 2, [X[3]]))             # 親のいとこ → はとこ
    b.append(fork(X[0], 3, [X[0]]))             # あなた → 子
    b.append(fork(X[1], 3, [X[1]]))             # きょうだい → 甥・姪
    b.append(fork(X[2], 3, [X[2]]))             # いとこ → いとこの子
    b.append(box(X[0], Y[0], "曾祖父母"))
    b.append(box(X[0], Y[1], "祖父母"))
    b.append(box(X[3], Y[1], "祖父母のきょうだい", kind="via", sub="（大おじ・大おば）"))
    b.append(box(X[0], Y[2], "父母"))
    b.append(box(X[2], Y[2], "おじ・おば"))
    b.append(box(X[3], Y[2], "親のいとこ", kind="via"))
    b.append(box(X[0], Y[3], "あなた", kind="me"))
    b.append(box(X[1], Y[3], "きょうだい"))
    b.append(box(X[2], Y[3], "いとこ", kind="hi"))
    b.append(box(X[3], Y[3], "はとこ"))
    b.append(box(X[0], Y[4], "子"))
    b.append(box(X[1], Y[4], "甥・姪"))
    b.append(box(X[2], Y[4], "いとこの子"))
    # 右：見かた
    x0 = 942
    b.append(rect(x0, 108, 210, 506, CARD, LINE, 12))
    b.append(text(x0 + 18, 140, "見かた", 17, INK, 700))
    b.append(text(x0 + 18, 172, "1/8（12.5%）", 17, TEAL_D, 700))
    b.append(lines(x0 + 18, 196, ["＝血縁度（同じ遺伝子を", "　受けつぐ割合の平均）"], 14.5, INK2, 1.45))
    b.append(text(x0 + 18, 252, "4親等", 17, TEAL_D, 700))
    b.append(lines(x0 + 18, 276, ["＝共通の先祖までさかの", "　ぼって相手まで下る", "　世代の数"], 14.5, INK2, 1.45))
    b.append(line(x0 + 16, 344, x0 + 194, 344, LINE, 1.2))
    b.append(lines(x0 + 18, 372, ["1世代はなれるごとに", "血縁度は1/2になる"], 15.5, INK, 1.5, weight=700))
    b.append(line(x0 + 16, 420, x0 + 194, 420, LINE, 1.2))
    b.append(text(x0 + 18, 448, "ほかの続柄", 15.5, INK, 700))
    b.append(lines(x0 + 18, 474, ["異母・異父きょうだい", "　1/4（25%）・2親等", "二重いとこ", "　1/4（25%）・4親等"], 14.5, INK2, 1.5))
    b.append(text(x0 + 18, 600, "点線の箱は通り道", 14, MUTED))
    return svg("".join(b), "血のつながり（血縁度）と親等の関係図",
               "父方・母方とも同じ割合。「父母」「祖父母」の箱は2人分をまとめて表す。孫・ひ孫は祖父母・曾祖父母と同じ割合。")


def chain(cx, apex, col, ac):
    """共通の先祖1人から、あなた・いとこへの道（1/2が4回）"""
    o = []
    ya, ym, yb = 160, 248, 324
    pts = {"top": (cx, ya), "L1": (cx - 92, ym), "R1": (cx + 92, ym), "L2": (cx - 92, yb), "R2": (cx + 92, yb)}
    w, hh = 112, 38
    for a, b_ in [("top", "L1"), ("L1", "L2"), ("top", "R1"), ("R1", "R2")]:
        (x1, y1), (x2, y2) = pts[a], pts[b_]
        if x1 != x2:
            sx, sy = x1 + (-1 if x2 < x1 else 1) * 30, y1 + hh / 2
            ex, ey = x2 + (1 if x2 < x1 else -1) * 12, y2 - hh / 2 - 4
        else:
            sx, sy, ex, ey = x1, y1 + hh / 2, x2, y2 - hh / 2 - 4
        o.append(arrow(sx, sy, ex, ey, ac, 2.6))
        mx, my = (sx + ex) / 2, (sy + ey) / 2
        dx = -1 if (x2 < x1 or (x1 == x2 and x1 < cx)) else 1
        if x1 != x2:            # 斜めの線：線から外側（上）へずらす
            L = ((ex - sx) ** 2 + (ey - sy) ** 2) ** 0.5
            nx, ny = (ey - sy) / L, -(ex - sx) / L
            if ny > 0: nx, ny = -nx, -ny
            o.append(text(mx + nx * 16, my + ny * 16, "1/2", 15, col, 700, "end" if dx < 0 else "start"))
        else:
            o.append(text(mx + dx * 14, my + 6, "1/2", 15, col, 700, "end" if dx < 0 else "start"))
    for k, nm in [("top", apex), ("L1", "親"), ("R1", "おじ・おば"), ("L2", "あなた"), ("R2", "いとこ")]:
        x, y = pts[k]
        if k == "top":
            o.append(rect(x - 46, y - hh / 2, 92, hh, col, col, 8) + text(x, y + 6, nm, 17, "#fff", 700, "middle"))
        elif k == "L2":
            o.append(rect(x - w / 2, y - hh / 2, w, hh, INK, INK, 8) + text(x, y + 6, nm, 17, "#fff", 700, "middle"))
        else:
            o.append(rect(x - w / 2, y - hh / 2, w, hh, CARD, col, 8, 1.8) + text(x, y + 6, nm, 16, INK, 700, "middle"))
    o.append(text(cx, 372, "1/2×1/2×1/2×1/2 ＝ 1/16", 18, col, 700, "middle"))
    return "".join(o)


def fig2():
    b = []
    b.append(text(190, 122, "祖父を通る道", 17, TEAL, 700, "middle"))
    b.append(chain(190, "祖父", TEAL, "teal"))
    b.append(text(368, 262, "＋", 34, INK, 700, "middle"))
    b.append(text(546, 122, "祖母を通る道", 17, ACC, 700, "middle"))
    b.append(chain(546, "祖母", ACC, "acc"))
    b.append(text(718, 262, "＝", 34, INK, 700, "middle"))
    cous = r_of([4, 4])
    b.append(rect(752, 152, 400, 220, CARD, LINE, 12))
    b.append(text(952, 200, "1/16 ＋ 1/16", 22, INK2, 700, "middle"))
    b.append(text(952, 268, f"＝ {cous}", 48, ACC, 700, "middle"))
    b.append(text(952, 310, f"いとこの血縁度 {pct(cous)}", 20, INK, 700, "middle"))
    b.append(text(952, 346, "共通の先祖が2人いるので2本の道を足す", 14.5, INK2, anchor="middle"))
    # 下：ほかの続柄も同じ数え方
    rows = [("きょうだい", "父と母（2人）", 2, 2), ("おじ・おば／甥・姪", "祖父と祖母（2人）", 2, 3), ("いとこ", "祖父と祖母（2人）", 2, 4),
            ("はとこ", "曾祖父と曾祖母（2人）", 2, 6), ("異母・異父きょうだい", "父か母（1人）", 1, 2)]
    tr = []
    for nm, anc, k, n in rows:
        one = F(1, 2) ** n
        val = r_of([n] * k)
        calc = f"{one} ＋ {one}" if k == 2 else f"{one}"
        tr.append([nm, anc, f"{n}回", calc, f"{val}（{pct(val)}）"])
    b.append(table(48, 392, ["続柄", "共通の先祖", "1本の道で1/2をかける回数", "計算", "血縁度"], tr,
                   [230, 230, 260, 170, 214], 37, 16))
    return svg("".join(b), "いとこの血のつながりが12.5%（1/8）になる理由",
               "血縁度＝共通の先祖を通る道ごとに「1/2をかける回数」分かけて、全部の道を足したもの。")


FIGS = [
    dict(svg=fig1, alt="血のつながり（血縁度）と親等の関係図。あなたから見て、父母・子・きょうだいは1/2（50%）、祖父母・おじおば・甥姪は1/4（25%）、曾祖父母といとこは1/8（12.5%）、いとこの子は1/16（6.25%）、はとこは1/32（3.125%）で、それぞれの親等（1〜6親等）も示した家系図。",
         caption="続柄ごとの血縁度と親等。いとこは1/8（12.5%）・4親等、はとこは1/32（3.125%）・6親等。"),
    dict(svg=fig2, alt="いとこの血の繋がりの割合が12.5%（8分の1）になる理由を示す図。共通の祖父を通る道と祖母を通る道でそれぞれ1/2を4回かけて1/16、2本を足して1/8になる。きょうだい・おじおば・はとこ・異母きょうだいの計算も表にまとめている。",
         caption="いとこが1/8になる理由。祖父・祖母を通る2本の道（各1/16）を足す。"),
]
