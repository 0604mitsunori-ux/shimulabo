"""水圧と浮力（suiatsu-fuyuu）の授業用の図。
数値はシミュ（scripts/rika/sims_saibou_fuyuu.py の SUIATSU_JS）と同じ式：
  水圧 pr(z)＝0.01×深さ〔N/cm²〕、物体は底面5cm×5cm（S＝25cm²）、重力＝質量÷100〔N〕、
  浮力 Fb＝水中にある部分の高さ×25×0.01、ばねばかり＝重力−浮力。
しくみ図はシミュの最初の設定（中 100cm³・300g・底面の深さ6cm）。"""
from figlib import *

S = 25            # 底面積 cm²
WATER = "#dcebf3"
BLOCK = "#c9ced6"


def pr(z):        # 水圧 N/cm²（シミュの pr）
    return max(0.0, z) * 0.01


def phys(d, h=4, m=300):
    """シミュの phys(d) と同じ（浮かない場合）。d＝底面の深さ cm"""
    V, Wt = S * h, m / 100
    sub = min(max(d, 0), h)
    Fb = sub * S * 0.01
    return dict(V=V, Wt=Wt, Fb=Fb, rd=max(0.0, Wt - Fb), top=d - h, bot=d)


def f2(v):
    return f"{v:.2f}"


def fig1():
    c = phys(6)                       # 中 100cm³・300g を底面の深さ6cmまで沈めた状態（シミュの初期値）
    PX, SY = 30, 250                  # 1cm＝30px、水面の y
    TL, TR, TB = 100, 470, SY + 9 * PX
    OX, OW = 285, 5 * PX              # 物体の中心 x と幅（5cm）
    top, bot = SY + c["top"] * PX, SY + c["bot"] * PX
    AL = 12                           # 水圧の矢印：深さ1cmあたり 12px（強調）
    b = []
    # 水そう
    b.append(f'<rect x="{TL}" y="{SY}" width="{TR - TL}" height="{TB - SY}" fill="{WATER}"/>')
    b.append(poly([(TL, SY - 50), (TL, TB), (TR, TB), (TR, SY - 50)], INK2, 3))
    b.append(line(TL, SY, TR, SY, TEAL, 2))
    b.append(text(TR - 8, SY - 8, "水面", 15, TEAL, 700, "end"))
    for cm in range(0, 10):
        y = SY + cm * PX
        b.append(line(TL - 10, y, TL, y, INK2, 1.4))
        if cm % 2 == 0 and cm:
            b.append(text(TL - 14, y + 5, f"{cm}cm", 14, INK2, anchor="end"))
    b.append(text(TL - 14, SY + 5, "0", 14, INK2, anchor="end"))
    b.append(text(TL - 14, SY - 14, "深さ", 14, INK2, 700, "end"))
    # ばねばかり
    b.append(line(OX - 70, 108, OX + 70, 108, INK2, 5))
    b.append(line(OX, 108, OX, 120, INK2, 2))
    b.append(rect(OX - 18, 120, 36, 82, CARD, INK2, 6, 1.6))
    for i in range(6):
        b.append(line(OX + 4, 130 + i * 12, OX + 14, 130 + i * 12, MUTED, 1.2))
    b.append(line(OX - 12, 172, OX + 12, 172, ACC, 3))
    b.append(line(OX, 202, OX, top, INK, 1.8))
    b.append(text(OX + 32, 146, "ばねばかり", 15, INK2, 700))
    b.append(text(OX + 32, 176, f"{f2(c['rd'])} N", 22, INK, 700))
    b.append(text(OX + 32, 200, f"（空気中では {f2(c['Wt'])} N）", 14, MUTED))
    # 物体
    b.append(rect(OX - OW / 2, top, OW, bot - top, BLOCK, INK, 2, 2))
    b.append(text(OX, (top + bot) / 2 - 4, f"{c['V']} cm³", 17, INK, 700, "middle"))
    b.append(text(OX, (top + bot) / 2 + 20, "300 g", 17, INK, 700, "middle"))
    # 水圧の矢印（長さ＝深さに比例）
    xs = [OX - 52, OX - 18, OX + 18, OX + 52]           # まん中は糸があるのでよける
    for x in xs:
        L = AL * c["top"]
        b.append(arrow(x, top - L - 2, x, top - 2, "teal", 2.6))
        L = AL * c["bot"]
        b.append(arrow(x, bot + L + 2, x, bot + 2, "teal", 2.6))
    for z in (c["top"] + 1, c["top"] + 2, c["top"] + 3):
        y, L = SY + z * PX, AL * z
        b.append(arrow(OX - OW / 2 - L - 2, y, OX - OW / 2 - 2, y, "teal", 2.6))
        b.append(arrow(OX + OW / 2 + L + 2, y, OX + OW / 2 + 2, y, "teal", 2.6))
    b.append(text(OX + OW / 2 + 8, top - 10, "上の面", 15, TEAL, 700))
    b.append(text(OX + 62, bot + 44, "下の面", 15, TEAL, 700))
    b.append(text((TL + TR) / 2, TB + 30, "青い矢印＝水圧（深いほど大きい）", 15, TEAL, 700, "middle"))

    # 右：水圧の差 → 浮力
    X = 620
    pt, pb = pr(c["top"]), pr(c["bot"])
    Ft, Fbm = pt * S, pb * S
    b.append(text(X, 122, "水圧の差が、浮力になる", 20, INK, 700))
    b.append(text(X, 160, f"上の面（深さ{c['top']:.0f}cm）を押す力：下向き", 16, INK2))
    b.append(text(X + 24, 188, f"{f2(pt)} N/cm² × {S} cm² ＝ {f2(Ft)} N", 18, INK, 700))
    b.append(text(X, 226, f"下の面（深さ{c['bot']:.0f}cm）を押す力：上向き", 16, INK2))
    b.append(text(X + 24, 254, f"{f2(pb)} N/cm² × {S} cm² ＝ {f2(Fbm)} N", 18, INK, 700))
    b.append(rect(X, 274, 520, 46, ACC_L, ACC_L, 8))
    b.append(text(X + 14, 305, f"浮力 ＝ {f2(Fbm)} N － {f2(Ft)} N ＝ {f2(Fbm - Ft)} N（上向き）", 19, ACC, 700))
    b.append(text(X, 350, "横から押す力は、左右で同じ大きさ → 打ち消し合う", 16, INK2))
    # 力のつり合い（帯グラフ）
    y0, K = 400, 120                  # 1N＝120px
    b.append(text(X, y0, "力のつり合い（物体は止まっている）", 18, INK, 700))
    bx = X + 110
    b.append(text(X, y0 + 44, "下向きの力", 15, INK2, 700))
    b.append(rect(bx, y0 + 18, c["Wt"] * K, 40, "#e7e3da", INK2, 4, 1.4))
    b.append(text(bx + c["Wt"] * K / 2, y0 + 44, f"重力 {f2(c['Wt'])} N", 17, INK, 700, "middle"))
    b.append(text(X, y0 + 100, "上向きの力", 15, INK2, 700))
    b.append(rect(bx, y0 + 74, c["Fb"] * K, 40, ACC_L, ACC, 4, 1.4))
    b.append(text(bx + c["Fb"] * K / 2, y0 + 100, f"浮力 {f2(c['Fb'])} N", 16, ACC, 700, "middle"))
    b.append(rect(bx + c["Fb"] * K, y0 + 74, c["rd"] * K, 40, TEAL_L, TEAL, 4, 1.4))
    b.append(text(bx + c["Fb"] * K + c["rd"] * K / 2, y0 + 100, f"ばねばかりが引く力 {f2(c['rd'])} N", 16, TEAL_D, 700, "middle"))
    b.append(text(X, y0 + 150, f"浮力 ＝ 空気中の値 － 水中の値 ＝ {f2(c['Wt'])} － {f2(c['rd'])} ＝ {f2(c['Fb'])} N", 17, INK, 700))
    b.append(text(X, y0 + 180, "（水圧の差から求めた値と同じになる）", 15, MUTED))
    return svg("".join(b), "水中の物体に働く力（水圧と浮力のしくみ）",
               "物体は底面5cm×5cm・高さ4cm。100 gの物体に働く重力を1 Nとして計算。矢印は見やすく強調。")


def fig2():
    b = []
    x0, y0, w, h = 130, 555, 500, 350
    XM, YM = 15, 3.0
    sx, sy = w / XM, 330 / YM
    xt = [(d * sx, f"{d}") for d in range(0, 16, 3)]
    yt = [(v * sy, f"{v:.1f}") for v in (0.5, 1.0, 1.5, 2.0, 2.5, 3.0)]
    b.append(axes(x0, y0, w, h, "", "", xt, yt, 15))
    b.append(text(x0 + w / 2, y0 + 50, "物体の底面の深さ（cm）", 16, INK, 700, "middle"))
    b.append(text(x0 - 14, y0 - h - 22, "力の大きさ（N）", 15, INK, 700))
    b.append(text(x0 - 10, y0 + 5, "0", 15, INK2, anchor="end"))
    dfull = 4
    X = lambda d: x0 + d * sx
    Y = lambda v: y0 - v * sy
    b.append(line(X(dfull), y0, X(dfull), Y(YM), MUTED, 1.6, "6 5"))
    b.append(text(X(dfull) + 8, Y(YM) + 2, "全部しずんだ（深さ4cm）", 15, MUTED, 700))
    ds = [i / 10 for i in range(0, 151)]
    b.append(poly([(X(d), Y(phys(d)["rd"])) for d in ds], TEAL, 3.2))
    b.append(poly([(X(d), Y(phys(d)["Fb"])) for d in ds], ACC, 3.2))
    for d in (0, 4, 10):
        b.append(circle(X(d), Y(phys(d)["rd"]), 5.5, TEAL, TEAL, 0) + circle(X(d), Y(phys(d)["Fb"]), 5.5, ACC, ACC, 0))
    b.append(text(X(0) + 12, Y(3.0) - 10, "空気中 3.00 N", 15, TEAL_D, 700))
    b.append(text(X(10), Y(2.0) - 14, "ばねばかりの値 2.00 N", 17, TEAL_D, 700, "middle"))
    b.append(text(X(10), Y(1.0) - 14, "浮力 1.00 N", 17, ACC, 700, "middle"))
    b.append(lines(X(0.25), Y(1.62), ["沈めるほど", "ふえる"], 15, ACC, 1.35, font_weight=700))
    b.append(text(X(0.25), Y(1.62) + 42, "（1cmで0.25 N）", 14, ACC))
    b.append(text(X(10), Y(1.0) + 30, "全部しずむと、深くしても一定", 15, ACC, 700, "middle"))
    b.append(text(x0, 118, "100 cm³・300 gの物体を少しずつ沈めたとき", 17, INK, 700))

    # 右：大きさと浮力の表＋まとめ
    RX = 700
    b.append(text(RX, 140, "物体の大きさと浮力（全部沈めたとき）", 18, INK, 700))
    rows = []
    for nm, hh in (("小（高さ2cm）", 2), ("中（高さ4cm）", 4), ("大（高さ8cm）", 8)):
        p = phys(20, hh, 300)
        rows.append([nm, f"{p['V']} cm³", f"{f2(p['Fb'])} N"])
    b.append(table(RX, 158, ["物体（底面5cm×5cm）", "体積", "浮力"], rows, [200, 120, 120], 46, 16.5))
    pts = ["浮力は、水中にある部分の体積で決まる。",
           "物体の質量（重さ）や材質には関係しない。",
           "浮力 ＝ 空気中の値 － 水中の値",
           "物体の密度が水（1 g/cm³）より小さいと、",
           "　全部沈む前に浮力と重力がつり合って浮く。"]
    yy = 410
    for i, s in enumerate(pts):
        if not s.startswith("　"):
            b.append(circle(RX + 8, yy - 6, 4, TEAL, TEAL, 0))
        b.append(text(RX + 22, yy, s, 16.5, INK if i != 2 else ACC, 700 if i == 2 else 400))
        yy += 34
    return svg("".join(b), "沈めた深さと浮力・ばねばかりの値",
               "底面の深さ＝水面から物体の底面までの深さ。物体は底面5cm×5cm。100 gに働く重力を1 Nとして計算。")


FIGS = [
    dict(svg=fig1, alt="水圧と浮力のしくみの図。ばねばかりにつるした体積100cm³・300gの物体を水中に沈めると、水圧が深いほど大きくあらゆる向きから働き、下の面を押す力1.50Nと上の面を押す力0.50Nの差1.00Nが浮力になり、ばねばかりの値が3.00Nから2.00Nに減ることを示す。",
         caption="水圧の差が浮力になるしくみ。重力3.00 N＝浮力1.00 N＋ばねばかり2.00 Nでつり合う。"),
    dict(svg=fig2, alt="物体を沈めた深さと浮力・ばねばかりの値のグラフ。全部沈むまでは浮力が深さに比例してふえ、全部沈んだあとは深さによらず一定になる。物体の大きさ（体積50・100・200cm³）と全部沈めたときの浮力（0.50・1.00・2.00N）の表つき。",
         caption="沈めた深さと浮力のグラフ。浮力は水中にある部分の体積で決まり、全部沈むと一定になる。"),
]
