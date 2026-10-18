"""風とゴムの力の働き（kaze-gomu・小3）の授業用の図。
数値はシミュ（scripts/rika/sims_sho3_a.py の rub_dist・wind_dist・fmtd）と同じ式をそのまま使う：
  ゴム：進むきょり＝0.9 m×本数×(のばす長さ÷5cm)^1.5、
  風：帆が受ける力＝½×1.2×1.2×0.04×(風の速さ−車の速さ)²、まさつ係数0.04・車100 g（送風きの口で 弱3・中4・強5 m/秒）。"""
from figlib import *

# --- シミュ（sims_sho3_a.py）と同じ式・同じ定数
G_, MASS, MU, AS, CDR, RHO = 9.8, 0.1, 0.04, 0.04, 1.2, 1.2
D0, CORE = 0.3, 0.6
WV = {1: 3.0, 2: 4.0, 3: 5.0}


def wind_dist(V0, mu=MU, dt=0.002):
    k = 0.5 * RHO * CDR * AS; s = u = t = 0.0
    while t < 60:
        d = s + D0; vw = V0 * (1 if d < CORE else CORE / d); rel = vw - u
        F = k * rel * abs(rel); fr = mu * MASS * G_
        if u <= 1e-6 and F <= fr and t > 0.05: break
        a = (F - fr) / MASS if (u > 1e-6 or F > fr) else 0
        u = max(0.0, u + a * dt); s += u * dt; t += dt
    return s


def rub_dist(n, x): return 0.9 * n * (x / 5) ** 1.5


def fmtd(d):
    cm = int(round(d * 100)); m_, c_ = divmod(cm, 100)
    return ("%dm%02dcm" % (m_, c_)) if m_ else "%dcm" % c_


WD = {k: wind_dist(v) for k, v in WV.items()}


def car(x, y, sail=False):
    """車（x＝後ろのはし、y＝地面）。長さ100"""
    b = []
    if sail:
        mx = x + 30
        b.append(line(mx, y - 18, mx, y - 130, "#7a5a2a", 3))
        b.append(f'<path d="M{mx},{y - 128} Q{mx + 50},{y - 78} {mx},{y - 36}Z" fill="{GOLD_L}" stroke="{GOLD}" stroke-width="2"/>')
    b.append(rect(x, y - 34, 100, 18, SKY, TEAL_D, 5, 1.6))
    for wx in (x + 20, x + 80):
        b.append(circle(wx, y - 9, 9, INK2, INK2, 0) + circle(wx, y - 9, 2.5, "#fff", "#fff", 0))
    return "".join(b)


def fig1():
    b = []
    # ---- 上：風の力
    G1 = 318
    b.append(text(60, 136, "風の力", 22, TEAL, 700))
    b.append(line(60, G1, 600, G1, MUTED, 2))
    fx, fy = 120, 236
    b.append(f'<rect x="{fx - 4}" y="{fy}" width="8" height="{G1 - fy}" fill="{MUTED}"/>' + rect(fx - 26, G1 - 7, 52, 7, INK2, INK2, 3, 0))
    b.append(circle(fx, fy, 42, "#e9e6df", INK2, 2) + circle(fx, fy, 28, "none", MUTED, 1) + circle(fx, fy, 5, INK2, INK2, 0))
    b.append(text(fx, G1 + 26, "送風き", 15, INK2, 700, "middle"))
    for yy in (200, 222, 244, 266):
        b.append(arrow(178, yy, 340, yy, "teal", 2.6))
    b.append(text(259, 188, "風", 17, TEAL, 700, "middle"))
    cx0 = 320
    b.append(car(cx0, G1, True))
    b.append(arrow(cx0 + 64, 242, cx0 + 150, 242, "acc", 4))
    b.append(text(cx0 + 68, 228, "風が「ほ」をおす力", 15, ACC, 700))
    b.append(text(cx0 + 160, G1 - 14, "→ 車が進む", 16, INK, 700))
    X = 650
    b.append(rect(X, 112, 500, 206, CARD, LINE, 10))
    b.append(text(X + 22, 158, "風が強いほど、おす力が大きい", 21, TEAL_D, 700))
    b.append(text(X + 22, 200, "→ 車は遠くまで進む", 19, INK, 700))
    b.append(text(X + 22, 248, "風の強さをかえるには：", 16, INK2))
    b.append(text(X + 22, 278, "送風きの風を「弱」→「強」にする", 17, INK2, 700))

    b.append(line(48, 352, 1152, 352, LINE, 1.6))
    # ---- 下：ゴムの力
    G2 = 590
    b.append(text(60, 392, "ゴムの力", 22, GOLD, 700))
    b.append(line(60, G2, 600, G2, MUTED, 2))
    sx = 340                                           # スタートの台（ゴムをかける所）
    b.append(f'<rect x="{sx - 5}" y="{G2 - 74}" width="10" height="74" fill="#8a6a3a"/>' + rect(sx - 18, G2 - 6, 36, 6, "#6b4f27", "#6b4f27", 2, 0))
    pull = 92                                          # のばす長さ（大きくかいた）
    cx1 = sx - pull - 100
    hx, hy = cx1 + 100, G2 - 26
    b.append(line(sx, G2 - 66, hx, hy, "#b4703a", 3) + line(sx, G2 - 10, hx, hy, "#b4703a", 3))
    b.append(car(cx1, G2))
    b.append(circle(hx, hy, 4, INK, INK, 0))
    b.append(text(sx + 12, G2 - 52, "スタートの台", 14, MUTED, 700))
    b.append(arrow(hx + 6, G2 - 92, hx + 112, G2 - 92, "acc", 4))
    b.append(text(hx - 60, G2 - 112, "ゴムがもとにもどろうとする力", 15, ACC, 700))
    b.append(line(hx, G2 + 14, sx, G2 + 14, INK2, 1.4) + line(hx, G2 + 6, hx, G2 + 22, INK2, 1.4) + line(sx, G2 + 6, sx, G2 + 22, INK2, 1.4))
    b.append(text(sx + 12, G2 + 20, "← のばす長さ", 15, INK2, 700))
    b.append(text(sx + 70, G2 - 14, "はなすと、車が進む →", 16, INK, 700))
    b.append(rect(X, 372, 500, 238, CARD, LINE, 10))
    b.append(text(X + 22, 418, "ゴムを長くのばすほど、", 21, GOLD, 700))
    b.append(text(X + 22, 452, "ゴムの本数をふやすほど、", 21, GOLD, 700))
    b.append(text(X + 22, 486, "もとにもどろうとする力が大きい", 21, GOLD, 700))
    b.append(text(X + 22, 528, "→ 車は遠くまで進む", 19, INK, 700))
    b.append(text(X + 22, 576, "ゴムを強く引っぱりすぎない。人に向けない。", 15.5, ACC))
    return svg("".join(b), "風の力・ゴムの力で、車が動くしくみ",
               "車・送風き・スタートの台は大きくかいている（大きさ・きょりは実際とちがう）。")


def fig2():
    b = []
    y0, PM = 506, 33                                   # 1 m＝33px（0〜10 m）

    def yaxis(x0, x1):
        out = []
        for m in range(0, 11, 2):
            yy = y0 - m * PM
            out.append(line(x0, yy, x1, yy, LINE, 1) + text(x0 - 8, yy + 5, f"{m}m" if m else "0", 14, INK2, anchor="end"))
        out.append(line(x0, y0 - 10.4 * PM, x0, y0, INK, 1.6) + line(x0, y0, x1, y0, INK, 1.6))
        return "".join(out)

    # 左：ゴム
    gx0, gx1 = 120, 640
    b.append(text(gx0 - 50, 128, "ゴムの力（のばす長さ・本数）", 19, GOLD, 700))
    b.append(yaxis(gx0, gx1))
    for gi, cm in enumerate((5, 10, 15)):
        gc = gx0 + 95 + gi * 165
        for n, dx, fill, edge in ((1, -33, GOLD_L, GOLD), (2, 33, "#d9b46a", GOLD)):
            d = rub_dist(n, cm)
            h = d * PM
            b.append(rect(gc + dx - 23, y0 - h, 46, h, fill, edge, 3, 1.6))
            b.append(text(gc + dx, y0 - h - 8, fmtd(d), 14.5, INK, 700, "middle"))
            b.append(text(gc + dx, y0 + 22, f"{n}本", 15, INK, 700, "middle"))
        b.append(text(gc, y0 + 48, f"{cm}cmのばす", 16, GOLD, 700, "middle"))
    # 右：風
    wx0, wx1 = 760, 1150
    b.append(text(wx0 - 50, 128, "風の力（送風きの風の強さ）", 19, TEAL, 700))
    b.append(yaxis(wx0, wx1))
    for i, (k, nm) in enumerate(((1, "弱い風"), (2, "中くらいの風"), (3, "強い風"))):
        c = wx0 + 70 + i * 125
        d = WD[k]
        h = d * PM
        b.append(rect(c - 30, y0 - h, 60, h, TEAL_L, TEAL, 3, 1.6))
        b.append(text(c, y0 - h - 8, fmtd(d), 15, INK, 700, "middle"))
        b.append(text(c, y0 + 22, nm, 15, TEAL_D, 700, "middle"))
        b.append(text(c, y0 + 44, f"（約{WV[k]:.0f} m/秒）", 14, MUTED, anchor="middle"))
    b.append(text(600, 598, "同じやり方でも、1回ごとに少しちがう（ばらつく）。3回くらいためして「だいたい」でくらべよう。", 16, INK2, anchor="middle"))
    return svg("".join(b), "力の大きさと、車が進むきょり（めやす）",
               "シミュレーションで計算しためやす（ばらつきなし）。車の重さ100 g。風の速さは送風きの口での速さ。")


FIGS = [
    dict(svg=fig1, alt="風とゴムの力の働きのしくみの図。送風きの風が車の「ほ」をおす力で車が進むこと、のばしたゴムがもとにもどろうとする力で車が進むことを示し、風が強いほど、ゴムを長くのばすほど・本数をふやすほど、力が大きく車は遠くまで進むことをまとめている（小3理科）。",
         caption="風の力とゴムの力で車が動くしくみ。力が大きいほど、車は遠くまで進む。"),
    dict(svg=fig2, alt="ゴムをのばす長さ（5cm・10cm・15cm）と本数（1本・2本）、送風きの風の強さ（弱い風・中くらいの風・強い風）で、車が進むきょりのめやすをくらべたぼうグラフ。ゴム1本5cmで約90cm、10cmで約2m55cm、15cmで約4m68cm、風は弱い風で約2m10cm、強い風で約4m89cm。",
         caption="力の大きさと車が進むきょりのめやす。ゴムを長く・多く、風を強くするほど遠くまで進む。"),
]
