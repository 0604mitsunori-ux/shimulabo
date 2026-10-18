"""細胞分裂（saibou-bunretsu・中3）の授業用の図。
図1の細胞・染色体は、ページのシミュ（scripts/rika/sims_saibou_fuyuu.py の SAIBOU_JS の drawTai）の各段階（p＝0〜6）と同じ座標・形を 0.75倍で描く。
染色体は4本（長い2本・短い2本、赤＝朱・青＝藍）。数は 体細胞分裂 4本→4本、減数分裂 4本→2本→受精で4本、ヒト 46→23→46。"""
import math
from figlib import *

CW, CH = 300, 184                                  # シミュの細胞の大きさ
CHR = [(36, ACC), (36, TEAL), (22, ACC), (22, TEAL)]
SC = [(-26, -18, 0.6), (22, -22, -0.9), (-18, 24, 1.9), (26, 16, 0.3)]
YY = [-58, 20, -20, 58]
CELL_F = "#f2f8ec"                                 # 細胞の中（GREEN のうすい色）


def prng(seed):
    a = [seed & 0xFFFFFFFF]

    def r():
        a[0] = (a[0] + 0x6D2B79F5) & 0xFFFFFFFF; t = a[0]
        t = ((t ^ (t >> 15)) * (t | 1)) & 0xFFFFFFFF
        t ^= (t + (((t ^ (t >> 7)) * (t | 61)) & 0xFFFFFFFF)) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return r


def _threads():
    r = prng(7); out = []
    for i in range(4):
        pts = []; a = r() * 6.28; rad = 0.3 + 0.35 * r()
        for j in range(9):
            a += 0.5 + r() * 0.9; rad = min(0.78, max(0.15, rad + (r() - 0.5) * 0.35)); pts.append((math.cos(a) * rad, math.sin(a) * rad))
        out.append(pts)
    return out


THR = _threads()


class Cell:
    """シミュの座標（細胞の中心＝0,0）を、図の座標へ s 倍して描く"""
    def __init__(self, cx, cy, s): self.cx, self.cy, self.s = cx, cy, s
    def P(self, x, y): return self.cx + x * self.s, self.cy + y * self.s

    def box(self, x0, x1):
        X0, Y0 = self.P(x0, -CH / 2); X1, Y1 = self.P(x1, CH / 2)
        return rect(X0, Y0, X1 - X0, Y1 - Y0, CELL_F, GREEN, 14 * self.s, 2.4)

    def nucleus(self, x, y, r, a=1.0):
        X, Y = self.P(x, y)
        return f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{r * self.s:.1f}" fill="#e3e8ee" stroke="{MUTED}" stroke-width="1.6" opacity="{a}"/>'

    def threads(self, x, y, r):
        out = []
        for i, pts in enumerate(THR):
            q = lambda p: self.P(x + p[0] * r, y + p[1] * r)
            d = "M%.1f,%.1f" % q(pts[0])
            for j in range(1, len(pts) - 1):
                c = q(pts[j]); m = q(((pts[j][0] + pts[j + 1][0]) / 2, (pts[j][1] + pts[j + 1][1]) / 2))
                d += " Q%.1f,%.1f %.1f,%.1f" % (c[0], c[1], m[0], m[1])
            out.append(f'<path d="{d}" fill="none" stroke="{CHR[i][1]}" stroke-width="1.5" stroke-opacity=".85" stroke-linecap="round"/>')
        return "".join(out)

    def chromatid(self, x, y, ln, rot, bend, col, w=6):
        l = ln / 2; sx, cy = math.sin(bend) * l, math.cos(bend) * l
        c, s = math.cos(rot), math.sin(rot)
        pts = [self.P(x + px * c - py * s, y + px * s + py * c) for px, py in [(sx, -cy), (0, 0), (sx, cy)]]
        return (f'<polyline points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="none" stroke="{col}" '
                f'stroke-width="{w * self.s:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')

    def xchrom(self, x, y, ln, rot, col):
        g, c, s = 3.4, math.cos(rot), math.sin(rot)
        X, Y = self.P(x, y)
        return (self.chromatid(x - g * c, y - g * s, ln, rot, -0.35, col) + self.chromatid(x + g * c, y + g * s, ln, rot, 0.35, col)
                + circle(X, Y, 2.4 * self.s, INK2, INK2, 0))

    def plate(self, hl):
        X0, Y0 = self.P(0, -hl); X1, Y1 = self.P(0, hl)
        return line(X0, Y0, X1, Y1, GREEN, 3)

    def tag(self, x, y, s="4本"):
        X, Y = self.P(x, y)
        return rect(X - 22, Y - 12, 44, 24, "#fff", TEAL, 12, 1.2) + text(X, Y + 5, s, 14, TEAL, 700, "middle")


def stage(c, k):
    """シミュの drawTai(p) を p＝k（⑦は p＝6）で描いたものと同じ"""
    b = []
    T = -CH / 2
    if k < 5:
        b.append(c.box(-CW / 2, CW / 2))
        if k == 4: b.append(c.plate(0.6 * CH / 2))
    else:
        wd = CW / 2 if k == 5 else CW * 0.92
        b.append(c.box(-wd, 0) + c.box(0, wd))
    if k == 0: b.append(c.nucleus(0, 0, 62) + c.threads(0, 0, 62))
    if k == 4: b.append(c.nucleus(-75, 0, 44, 0.7) + c.nucleus(75, 0, 44, 0.7))
    if k >= 5:
        wd, r = (CW / 2, 44) if k == 5 else (CW * 0.92, 52)
        for x in (-wd / 2, wd / 2): b.append(c.nucleus(x, 0, r) + c.threads(x, 0, r))
    for i, (ln, col) in enumerate(CHR):
        if k == 1: b.append(c.xchrom(SC[i][0], SC[i][1], ln, SC[i][2], col))
        elif k == 2:
            for s in (0, 1):
                d = 1 if s else -1
                b.append(c.chromatid(d * 3.4, YY[i], ln, math.pi if s else 0, -0.35, col))
            X, Y = c.P(0, YY[i]); b.append(circle(X, Y, 2.4 * c.s, INK2, INK2, 0))
        elif k in (3, 4):
            for s in (0, 1):
                d = 1 if s else -1
                x, y, bb = (d * 100, YY[i] * 0.75, 0.9) if k == 3 else (d * 75, YY[i] * 0.45, 0.5)
                b.append(c.chromatid(x, y, ln, math.pi if s else 0, bb, col))
    if k in (3, 4, 5): b.append(c.tag(-75, T + 18) + c.tag(75, T + 18))
    elif k == 6: b.append(c.tag(-CW * 0.46, T + 18) + c.tag(CW * 0.46, T + 18))
    else: b.append(c.tag(-CW / 2 + 34, T + 20))
    return "".join(b)


STAGES = [("①", ["分裂前の細胞"], "間期"), ("②", ["核の中に染色体が", "見えるようになる"], "前期"), ("③", ["染色体が細胞の", "中央に並ぶ"], "中期"),
          ("④", ["染色体が分かれて", "両端へ移動する"], "後期"), ("⑤", ["中央に仕切りが", "でき始める"], "終期"), ("⑥", ["2つの細胞に分かれる"], "間期にもどる"),
          ("⑦", ["それぞれの細胞が大きくなる"], "間期")]


def fig1():
    b = []; s = 0.75; PW, GAP = 252, 32
    slots = [(0, 0, 1), (1, 0, 1), (2, 0, 1), (3, 0, 1), (0, 1, 1), (1, 1, 1), (2, 1, 2)]
    for k, ((col, row, span), (no, nm, hi)) in enumerate(zip(slots, STAGES)):
        x = 48 + col * (PW + GAP); y = 100 + row * 266; w = PW * span + GAP * (span - 1)
        b.append(rect(x, y, w, 252, CARD, LINE, 10))
        b.append(badge(x + 22, y + 24, str(k + 1), TEAL, "#fff", 16))
        b.append(text(x + w - 14, y + 30, "高校：" + hi, 14, MUTED, anchor="end"))
        b.append(stage(Cell(x + w / 2, y + 112, s), k))
        for j, t in enumerate(nm):
            b.append(text(x + w / 2, y + 210 + j * 22, t, 16, INK, 700, "middle"))
        if k == 6:
            b.append(text(x + w / 2, y + 236, "（染色体は見やすいように4本にして色分けしている）", 14, MUTED, anchor="middle"))
        if col < 3 and span == 1 and k != 3:
            b.append(arrow(x + PW + 5, y + 112, x + PW + GAP - 5, y + 112, "teal", 2.4))
    return svg("".join(b), "体細胞分裂の順序（タマネギの根の先端の細胞）",
               "染色体は分裂の前に複製され、2つの細胞に同じ数ずつ分けられる。4本の細胞 → 4本の細胞が2つ（数は変わらない）。")


def rods(cx, cy, cols, scale=1.0, gap=14):
    """染色体を棒で（長さ：長い36・短い22 をそろえた比で）。cols＝[(長さ, 色), ...]"""
    out = []; n = len(cols); x0 = cx - (n - 1) * gap / 2
    for i, (ln, c) in enumerate(cols):
        h = ln * scale
        out.append(line(x0 + i * gap, cy - h / 2, x0 + i * gap, cy + h / 2, c, 6))
    return "".join(out)


def fig2():
    b = []
    L, S_ = 36, 22
    full = [(L, ACC), (L, TEAL), (S_, ACC), (S_, TEAL)]
    # 左：体細胞分裂
    b.append(text(48, 124, "体細胞分裂", 19, TEAL, 700) + text(160, 124, "（体の細胞をふやす）", 15, MUTED))
    b.append(circle(130, 222, 54, CELL_F, GREEN, 2.4) + rods(130, 222, full, 1.2))
    b.append(text(130, 302, "4本", 17, INK, 700, "middle"))
    b.append(arrow(196, 222, 276, 222, "teal", 2.6) + text(236, 208, "1回", 15, TEAL, 700, "middle"))
    for x in (350, 470):
        b.append(circle(x, 222, 54, CELL_F, GREEN, 2.4) + rods(x, 222, full, 1.2) + text(x, 302, "4本", 17, INK, 700, "middle"))
    b.append(text(410, 330, "数は変わらない", 16, TEAL, 700, "middle"))
    # 右：減数分裂と受精
    b.append(line(570, 106, 570, 330, LINE, 1.4))
    b.append(text(600, 124, "減数分裂と受精", 19, ACC, 700) + text(744, 124, "（生殖細胞をつくる）", 15, MUTED))
    b.append(circle(650, 222, 46, CELL_F, GREEN, 2.4) + rods(650, 222, full, 1.0, 13))
    b.append(text(650, 302, "4本", 17, INK, 700, "middle"))
    b.append(arrow(704, 222, 760, 222, "acc", 2.6) + text(732, 208, "2回", 15, ACC, 700, "middle"))
    gam = [[(L, ACC), (S_, TEAL)], [(L, ACC), (S_, TEAL)], [(L, TEAL), (S_, ACC)], [(L, TEAL), (S_, ACC)]]
    for i, cs in enumerate(gam):
        x, y = 794 + (i % 2) * 58, 192 + (i // 2) * 62
        b.append(circle(x, y, 26, CELL_F, GREEN, 2) + rods(x, y, cs, 0.9, 12))
    b.append(text(823, 302, "2本ずつ（半分）", 17, INK, 700, "middle"))
    b.append(arrow(890, 222, 1010, 222, "acc", 2.6))
    b.append(text(950, 208, "受精", 15, ACC, 700, "middle"))
    b.append(text(950, 250, "＋精子 2本", 15, GOLD, 700, "middle"))
    b.append(circle(1080, 222, 54, CELL_F, GREEN, 2.4) + rods(1080, 222, [(L, ACC), (S_, TEAL), (L, GOLD), (S_, GOLD)], 1.2))
    b.append(text(1080, 302, "受精卵 4本", 17, INK, 700, "middle"))
    b.append(text(1080, 330, "卵 2本＋精子 2本", 15, INK2, anchor="middle"))
    b.append(text(1152, 124, "金色＝もう一方の親から", 15, GOLD, 700, "end"))
    # 下：くらべる表
    rows = [["何のための分裂か", "体の細胞をふやす（成長・無性生殖）", "生殖細胞（卵・精子）をつくる"],
            ["どこで起こるか", "根やくきの先端（成長点）など体のいろいろな部分", "動物は卵巣・精巣、植物は胚珠・やく"],
            ["分裂の回数", "1回", "続けて2回"],
            ["できる細胞の数", "2つ", "4つ"],
            ["染色体の数（この図）", "4本 → 4本（変わらない）", "4本 → 2本（半分）→ 受精で4本"],
            ["染色体の数（ヒト）", "46本 → 46本", "46本 → 23本 → 受精で46本"]]
    b.append(table(48, 352, ["", "体細胞分裂", "減数分裂"], rows, [204, 450, 450], 38, 16))
    return svg("".join(b), "体細胞分裂と減数分裂のちがい",
               "受精卵の染色体は、半分が卵（母親）から、半分が精子（父親）から受けついだもの。")


FIGS = [
    dict(svg=fig1, alt="体細胞分裂の順序を7段階で示す図。①分裂前の細胞（間期）②核の中に染色体が見えるようになる（前期）③染色体が細胞の中央に並ぶ（中期）④染色体が分かれて両端へ移動する（後期）⑤中央に仕切りができ始める（終期）⑥2つの細胞に分かれる⑦それぞれの細胞が大きくなる。どの段階でも1つの細胞の染色体は4本で、数は変わらない。",
         caption="体細胞分裂の順序（タマネギの根の先端）。染色体は複製されてから2つの細胞に等しく分けられ、数は変わらない。"),
    dict(svg=fig2, alt="体細胞分裂と減数分裂をくらべたまとめ図。体細胞分裂では4本の細胞から4本の細胞が2つでき、減数分裂では2回の分裂で2本ずつ（半分）の生殖細胞が4つでき、受精で4本にもどる。目的・起こる場所・分裂の回数・できる細胞の数・染色体の数（ヒトは46本→23本→受精で46本）の比較表つき。",
         caption="体細胞分裂と減数分裂のちがい。減数分裂で染色体は半分になり、受精でもとの数にもどる。"),
]
