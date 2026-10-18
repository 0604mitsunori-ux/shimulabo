"""ばねののびと力（bane-nobi・中1 力の働き）の授業用の図
数値はシミュ（scripts/rika/sims_hikari_bane.py の BANE_JS／BANE_TABLE）と同じ：
力〔N〕＝質量〔g〕÷100（月面は÷6）、のび〔cm〕＝1Nあたりののび×力（弾性の限界＝のび16cmまで）。ばねA＝1Nで5cm、ばねB＝1Nで2.5cm。"""
import math
from figlib import *

KA, KB, XL = 5, 2.5, 16          # ばねA・Bの強さ（1Nで何cm）、弾性の限界（のび16cm）


def r1(v): return math.floor(v * 10 + 0.5) / 10


def fN(v):
    s = "%.2f" % (math.floor(v * 100 + 0.5) / 100)
    return s.rstrip("0").rstrip(".")


def nobi(k, f):
    x = k * f
    assert x <= XL + 1e-9           # 図ではすべて弾性の限界の内側
    return x


def coil(x, y0, y1, n=22, w=13, color=INK2, width=2):
    pts = [(x, y0), (x, y0 + 8)]
    L = (y1 - 8) - (y0 + 8)
    for i in range(1, n):
        pts.append((x + (w if i % 2 else -w), y0 + 8 + L * i / n))
    pts += [(x, y1 - 8), (x, y1)]
    return poly(pts, color, width)


def fig1():
    b = []
    # ---- 左：おもりをふやすとのびる（ばねA・20gのおもり）
    m = 20; f1 = m / 100                      # 20gのおもり1個＝0.2N
    TOP, NAT, S = 134, 150, 26                # ばねの上の端、元の長さ（px）、1cm＝26px
    xs = [130, 230, 330, 430]
    b.append(rect(80, 122, 420, 12, "#cfc9bb", "#cfc9bb", 3))
    b.append(line(84, TOP + NAT, 480, TOP + NAT, MUTED, 1.3, "6 5"))
    b.append(text(486, TOP + NAT + 5, "元の長さ", 15, MUTED))
    for row, (y, lab) in enumerate([(486, "おもり"), (512, "力"), (538, "のび")]):
        b.append(text(48, y, lab, 15, MUTED))
    for n, x in enumerate(xs):
        F = n * f1; X = nobi(KA, F); yb = TOP + NAT + X * S
        b.append(coil(x, TOP, yb))
        if n:
            b.append(line(x, yb, x, yb + 8, INK2, 2))
        for i in range(n):
            b.append(rect(x - 22, yb + 8 + i * 15, 44, 13, "#9aa0a8", "#6b6f76", 2, 1))
        if n:
            b.append(line(x - 26, TOP + NAT, x - 26, yb, TEAL, 5))
        if n == 1:
            b.append(text(x - 34, TOP + NAT + 20, "のび", 14, TEAL, 700, "end"))
        b.append(text(x, 486, f"{n}個", 17, INK, 700, "middle"))
        b.append(text(x, 512, f"{fN(F)}N", 16, ACC, 700, "middle"))
        b.append(text(x, 538, f"{r1(X):.1f}cm" if n else "0cm", 16, TEAL, 700, "middle"))
    # 2力のつり合い（3個のとき）
    x = xs[3]; F = 3 * f1; yb = TOP + NAT + nobi(KA, F) * S
    Lf = F / f1 * 20                                              # 矢印の長さは力に比例（0.2Nで20px）
    hook, mid = yb + 8, yb + 8 + 3 * 15 / 2
    b.append(arrow(x, hook, x, hook - Lf, "green", 4) + arrow(x, mid, x, mid + Lf, "acc", 4))
    b.append(text(x + 18, hook - Lf + 14, "ばねが引く力", 15, GREEN, 700) + text(x + 18, hook - Lf + 34, f"{fN(F)}N（上向き）", 15, GREEN, 700))
    b.append(text(x + 18, mid + Lf - 14, "重力", 15, ACC, 700) + text(x + 18, mid + Lf + 6, f"{fN(F)}N（下向き）", 15, ACC, 700))
    b.append(rect(48, 556, 500, 58, CARD, LINE, 8))
    b.append(text(298, 580, f"ばねA（1Nで{KA}cmのびる）に、{m}gのおもりを1個ずつ", 15, INK2, anchor="middle"))
    b.append(text(298, 604, f"おもり1個（{fN(f1)}N）ごとに {r1(KA * f1):.1f}cm ずつのびる", 17, INK, 700, "middle"))
    # ---- 右：力の大きさとのびのグラフ
    x0, y0, w, h, Fm, Xm = 680, 530, 420, 340, 2.0, 10
    sx, sy = w / Fm, h / Xm
    b.append(text(612, 122, "力の大きさとばねののびのグラフ", 19, INK, 700))
    b.append(axes(x0, y0, w, h, "", "ばねののび（cm）",
                  [(v * sx, fN(v)) for v in (0, 0.5, 1.0, 1.5, 2.0)], [(v * sy, str(v)) for v in range(0, 11, 2)], 15))
    b.append(text(x0 + w / 2, y0 + 50, "力の大きさ（N）", 16, INK, anchor="middle"))
    for k, col, nm in [(KA, TEAL, "A"), (KB, ACC, "B")]:
        b.append(line(x0, y0, x0 + Fm * sx, y0 - k * Fm * sy, col, 2.4))
        for n in range(1, 11):
            F = n * f1; X = nobi(k, F); px, py = x0 + F * sx, y0 - X * sy
            b.append(circle(px, py, 6, col, "#fff", 1.2) if nm == "A" else f'<rect x="{px - 5.5:.1f}" y="{py - 5.5:.1f}" width="11" height="11" fill="{col}" stroke="#fff" stroke-width="1.2"/>')
        b.append(badge(x0 + Fm * sx + 22, y0 - k * Fm * sy, nm, col, "#fff", 15))
    # 左の図の「3個」の点
    F = 3 * f1; X = nobi(KA, F); px, py = x0 + F * sx, y0 - X * sy
    b.append(line(px, y0, px, py, TEAL, 1.2, "4 3") + line(x0, py, px, py, TEAL, 1.2, "4 3"))
    b.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="11" fill="none" stroke="{TEAL}" stroke-width="2"/>')
    b.append(text(px + 10, y0 - 12, f"左の図の3個：{fN(F)}Nで{r1(X):.1f}cm", 15, TEAL_D, 700))
    b.append(rect(700, 176, 262, 104, CARD, LINE, 8))
    b.append(circle(718, 200, 6, TEAL, TEAL, 0) + text(732, 206, f"ばねA：1Nで{KA}cmのびる", 15, INK, 700))
    b.append(f'<rect x="712.5" y="222.5" width="11" height="11" fill="{ACC}"/>' + text(732, 234, f"ばねB：1Nで{KB}cmのびる", 15, INK, 700))
    b.append(text(714, 266, "原点を通る直線 → のびは力に比例", 15, TEAL_D, 700))
    return svg("".join(b), "ばねののびと力の大きさのしくみ（フックの法則）",
               "質量100gの物体にはたらく重力を1Nとする（20gで0.2N）。おもりにはたらく2力は、大きさが等しく向きが反対で一直線上。")


def fig2():
    b = []
    rows = [[f"{m} g", f"{fN(m / 100)} N", f"{r1(KA * m / 100):.1f} cm", f"{r1(KB * m / 100):.1f} cm", f"約{fN(m / 100 / 6)} N"]
            for m in (20, 40, 60, 80, 100, 200, 300)]
    b.append(table(70, 104, ["おもりの質量", "重さ（地球）", f"ばねA（1Nで{KA}cm）ののび", f"ばねB（1Nで{KB}cm）ののび", "月面での重さ"],
                   rows, [180, 180, 250, 250, 200], 40, 17))
    cards = [(60, ACC, ACC_L, "重さ", "物体にはたらく重力の大きさ",
              ["・単位：N（ニュートン）", "・ばねばかりではかる", "・場所で変わる（月面では約6分の1）", "・質量100gの物体で約1N"]),
             (610, TEAL, TEAL_L, "質量", "物体そのものの量",
              ["・単位：g、kg", "・上皿てんびん・電子てんびんではかる", "・どこでも変わらない（月面でも同じ）", "・例：60gのおもりは月面でも60g"])]
    for x, col, bg, nm, sub, items in cards:
        b.append(rect(x, 446, 530, 170, bg, col, 10, 1.4))
        b.append(text(x + 24, 482, nm, 24, col, 700) + text(x + 84, 481, "＝" + sub, 17, INK, 700))
        b.append(lines(x + 24, 514, items, 16, INK2, 1.68))
    return svg("".join(b), "おもりの質量・重さ・ばねののび（早見表）と、重さと質量のちがい",
               "100gの物体にはたらく重力を1Nとして計算（正確には約0.98N）。月面の重力は地球の約6分の1。のびは弾性の限界の内側。")


FIGS = [
    dict(svg=fig1, alt="ばねののびと力の大きさのしくみの図。1Nで5cmのびるばねAに20g（0.2N）のおもりを0〜3個つるすと、のびが0・1.0・2.0・3.0cmと力に比例してふえ、おもりにはたらく重力とばねが引く力（どちらも0.6N）がつり合う。ばねA（1Nで5cm）とばねB（1Nで2.5cm）の力とのびのグラフは原点を通る直線になる（フックの法則）。",
         caption="ばねののびは、ばねを引く力の大きさに比例する（フックの法則）。グラフは原点を通る直線。"),
    dict(svg=fig2, alt="おもりの質量（20g〜300g）ごとの重さ（N）、ばねA（1Nで5cm）とばねB（1Nで2.5cm）ののび、月面での重さ（約6分の1）の早見表と、重さ（重力の大きさ・N・ばねばかり・場所で変わる）と質量（物体そのものの量・g・てんびん・変わらない）のちがいのまとめ。",
         caption="質量・重さ・ばねののびの早見表と、重さと質量のちがい。月面では重さは約6分の1、質量は同じ。"),
]
