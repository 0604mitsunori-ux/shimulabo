"""振り子の波（pendulum-wave）の図。
本文の設計：一番長い振り子が60秒間に51回、…、一番短い振り子が65回往復（周期＝60÷回数）。
周期 T＝2π√(L/g) から長さ L＝g·T²÷(4π²)（g＝9.8m/s²）。模様は各おもりのふれ＝cos(2π×回数×t÷60) で計算する。"""
import math
from figlib import *

G, CYC, NS = 9.8, 60, list(range(51, 66))


def length_cm(n):
    T = CYC / n
    return G * T * T / (4 * math.pi ** 2) * 100


def fig1():
    b = []
    x0, dx, top = 96, 40, 150
    k = 360 / length_cm(51)                       # 1cmあたりpx（一番長い振り子＝360px）
    b.append(line(x0 - 30, top, x0 + dx * 14 + 30, top, INK, 6))
    for i, n in enumerate(NS):
        x = x0 + dx * i; L = length_cm(n); yb = top + L * k
        b.append(line(x, top, x, yb, MUTED, 1.4))
        b.append(circle(x, yb, 11, TEAL if i in (0, 14) else TEAL_L, TEAL, 1.6))
        b.append(text(x, 606, f"{n}", 15, INK, 700, "middle"))
    for i in (0, 7, 14):
        n = NS[i]; x = x0 + dx * i; yb = top + length_cm(n) * k
        b.append(text(x, yb + 34, f"{length_cm(n):.1f}cm", 15, ACC, 700, "middle"))
    b.append(text(x0 - 30, 580, "60秒間に往復する回数", 15, INK2))
    b.append(text(x0 - 30, 128, "長い（ゆっくり）", 15, INK2))
    b.append(text(x0 + dx * 14 + 30, 128, "短い（速い）", 15, INK2, anchor="end"))
    # 右：きまり
    X = 724
    b.append(rect(X, 112, 428, 168, TEAL_L, TEAL, 10, 1.2))
    b.append(text(X + 20, 146, "1往復する時間（周期）は長さで決まる", 17, TEAL_D, 700))
    b.append(text(X + 214, 192, "T ＝ 2π√(L ÷ g)", 26, INK, 700, "middle", font_family=SERIF))
    b.append(lines(X + 20, 228, ["T：周期（秒）　L：長さ（m）　g＝9.8 m/s²", "おもりの重さやふれはばでは変わらない"], 15, INK2, 1.55))
    b.append(text(X, 318, "長さを4倍にすると、周期は2倍になる", 17, INK, 700))
    b.append(table(X, 336, ["", "回数（60秒）", "1往復", "長さ"],
                   [["一番長い", "51回", f"{CYC / 51:.2f}秒", f"{length_cm(51):.1f}cm"],
                    ["まん中", "58回", f"{CYC / 58:.2f}秒", f"{length_cm(58):.1f}cm"],
                    ["一番短い", "65回", f"{CYC / 65:.2f}秒", f"{length_cm(65):.1f}cm"]], [104, 120, 96, 108], 44, 16))
    b.append(lines(X, 548, [f"長さの比は (51÷65)² ＝ {(51 / 65) ** 2:.3f}。一番長い糸を", f"1mにすると、一番短い糸は約{(51 / 65) ** 2 * 100:.1f}cm。"], 15.5, INK2, 1.55))
    return svg("".join(b), "振り子の長さと、1往復する時間",
               "長さは本文の装置（60秒でそろう・g＝9.8m/s²）で計算。長い振り子ほど1往復に時間がかかる。")


PANELS = [(0, "出発", "全員そろってスタート"),
          (7.5, "7.5秒後", "8個で1つの波（となりと1/8往復ずれる）"),
          (15, "15秒後", "4個で1つの波"),
          (20, "20秒後", "3個ごとに同じ位置（3つのグループ）"),
          (30, "30秒後", "1つおきに逆側（2つのグループ）"),
          (60, "60秒後", "またぴったりそろう")]


def fig2():
    b = [text(48, 124, "15個のおもりのふれ（その時刻の位置）。左が一番長い振り子（51回）、右が一番短い振り子（65回）。", 15.5, INK2)]
    W_, H_ = 352, 232
    for j, (t, ttl, desc) in enumerate(PANELS):
        px0 = 48 + (j % 3) * (W_ + 24); py0 = 142 + (j // 3) * (H_ + 12)
        b.append(rect(px0, py0, W_, H_, CARD, LINE, 10))
        b.append(text(px0 + 16, py0 + 28, ttl, 18, ACC if t in (0, 60) else INK, 700))
        cy = py0 + 108; A = 52
        b.append(line(px0 + 16, cy, px0 + W_ - 16, cy, LINE, 1.2, "4 4"))
        for i, n in enumerate(NS):
            x = px0 + 30 + i * (W_ - 60) / 14
            y = cy - A * math.cos(2 * math.pi * n * t / CYC)
            b.append(line(x, cy, x, y, LINE, 1))
            b.append(circle(x, y, 7.5, TEAL, TEAL_D, 1))
        b.append(text(px0 + W_ / 2, py0 + H_ - 22, desc, 15, INK, anchor="middle"))
    return svg("".join(b), "時間とともに変わる振り子の波の模様",
               "となりどうしのずれが一定の割合でふえるので、波やグループの模様が順に現れ、60秒でまたそろう。")


FIGS = [
    dict(svg=fig1, alt="振り子の波の15個の振り子の長さを同じ縮尺で並べた図。60秒間に51回往復する一番長い振り子（34.4cm）から65回往復する一番短い振り子（21.2cm）まで、周期T＝2π√(L/g)で長さが決まり、長い振り子ほど1往復に時間がかかることを示す。",
         caption="振り子の長さと1往復する時間。周期は長さだけで決まり、長いほどゆっくり往復する。"),
    dict(svg=fig2, alt="振り子の波の模様が時間とともに変わる様子の図。出発・7.5秒後・15秒後・20秒後・30秒後・60秒後の15個のおもりの位置を並べ、波の形、3つのグループ、1つおきに逆側、60秒後に再びそろう様子を示す。",
         caption="時間とともに変わる模様。となりどうしのずれが積み重なって波になり、60秒でまたそろう。"),
]
