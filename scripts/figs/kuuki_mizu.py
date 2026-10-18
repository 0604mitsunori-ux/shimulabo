"""とじこめた空気と水（kuuki-mizu・小4）の授業用の図。
体積と手ごたえは、シミュの JS（scripts/rika/sims_suiyoueki_kuuki.py の JS_KUUKI）と同じ式：
大気圧がピストンをおす力 F0＝101325 Pa×6 cm²÷9.80665（≒6.2 kg重）、おす力 F のとき 空気の体積＝もとの体積×F0÷(F0＋F)。"""
from figlib import *

F0 = 101325 * 6e-4 / 9.80665
MD = {"air": (40, 0), "water": (0, 40), "half": (20, 20)}     # （空気 mL, 水 mL）
FMAX = 12


def vol(m, f):
    a, w = MD[m]; return a * F0 / (F0 + f) + w


def f_of_v(v):                                 # 空気だけ：体積 v にするのに必要な力
    return F0 * (40 / v - 1)


FP = F0                                        # 図1でおす力（空気の体積がちょうど半分になる力）
assert abs(vol("air", FP) - 20) < 1e-9 and abs(vol("half", FP) - 30) < 1e-9 and abs(vol("water", FP) - 40) < 1e-9


def fr(v): return v - math.floor(v)
def hs1(k): return fr(math.sin(k * 12.9898) * 43758.5453)
def hs2(k): return fr(math.sin(k * 78.233) * 12345.678)


def syringe(cx, yb, m, f, px, seed, show_force):
    """注しゃ器（先をゴム板におしつけた形）。yb＝0 mL の目もりの高さ、px＝1 mL あたりの px"""
    a, wv = MD[m]; va = a * F0 / (F0 + f); vt = va + wv
    BW = 64; xl, xr = cx - BW / 2, cx + BW / 2
    out = []
    ytop = yb - vt * px; yw = yb - wv * px
    if wv > 0: out.append(f'<rect x="{xl}" y="{yw:.1f}" width="{BW}" height="{yb - yw:.1f}" fill="{TEAL_L}"/>')
    if va > 0: out.append(f'<rect x="{xl}" y="{ytop:.1f}" width="{BW}" height="{yw - ytop:.1f}" fill="#e6f0f8"/>')
    # 水のつぶ（すき間なく並ぶ）
    if wv > 0:
        j = 0
        while True:
            y = yb - 5.5 - j * 9.5
            if y < yw + 4: break
            x = xl + 6 + (5.5 if j % 2 else 0)
            while x <= xr - 5.5:
                out.append(circle(x, y, 4.6, "#5eead4", "#0f766e", 1)); x += 11
            j += 1
    # 空気のつぶ（数は同じ・間がつまる）
    if a > 0:
        n = 30 if m == "air" else 16
        for k in range(n):
            x = xl + 7 + hs1(k + seed) * (BW - 14); y = ytop + 7 + hs2(k + seed) * (yw - ytop - 14)
            out.append(circle(x, y, 4.2, "#60a5fa", "#1d4ed8", 1))
    # つつ・目もり
    out.append(poly([(xl - 1.5, yb - 52 * px), (xl - 1.5, yb + 1.5), (xr + 1.5, yb + 1.5), (xr + 1.5, yb - 52 * px)], "#64748b", 3))
    out.append(f'<rect x="{xl - 16}" y="{yb - 52 * px - 7:.1f}" width="{BW + 32}" height="7" rx="3" fill="#94a3b8"/>')
    out.append(f'<rect x="{cx - 5}" y="{yb + 2}" width="10" height="9" fill="#cbd5e1" stroke="#64748b"/><rect x="{cx - 40}" y="{yb + 11}" width="80" height="9" rx="3" fill="#334155"/>')
    for ml in range(0, 51, 10):
        yy = yb - ml * px
        out.append(line(xr + 1, yy, xr + 10, yy, "#64748b", 1.2) + text(xr + 14, yy + 5, str(ml), 14, INK2))
    # ピストン・おしぼう
    out.append(f'<rect x="{xl + 1}" y="{ytop - 12:.1f}" width="{BW - 2}" height="12" rx="3" fill="#1f2937"/>')
    rod = 66
    out.append(f'<rect x="{cx - 5}" y="{ytop - 12 - rod:.1f}" width="10" height="{rod}" fill="#e2e8f0" stroke="#64748b"/>')
    out.append(f'<rect x="{cx - 20}" y="{ytop - 20 - rod:.1f}" width="40" height="8" rx="3" fill="#94a3b8"/>')
    if show_force:
        out.append(arrow(cx, ytop - 84 - rod, cx, ytop - 24 - rod, "acc", 4.4))
    return "".join(out), ytop


def fig1():
    b = []
    YB, PX = 478, 5.0
    cols = [("① 空気だけ", "air"), ("② 水だけ", "water"), ("③ 空気と水（半分ずつ）", "half")]
    res = [("40 mL → 20 mL", "体積が小さくなる（つぶの間がつまる）", ACC), ("40 mL → 40 mL", "体積は変わらない（ピストンは動かない）", TEAL_D),
           ("40 mL → 30 mL", "空気の部分だけちぢむ（水は20 mLのまま）", PURPLE)]
    for k, ((ttl, m), (r1, r2, col)) in enumerate(zip(cols, res)):
        cx = 232 + k * 368
        if k: b.append(line(cx - 184, 110, cx - 184, 610, LINE, 1.2))
        b.append(text(cx, 124, ttl, 19, INK, 700, "middle"))
        s0, y0 = syringe(cx - 82, YB, m, 0, PX, 1 + k * 40, False)
        s1, y1 = syringe(cx + 70, YB, m, FP, PX, 1 + k * 40, True)
        b.append(s0 + s1)
        b.append(text(cx - 82, YB + 44, "おす前", 15, INK2, anchor="middle") + text(cx + 70, YB + 44, "おしたとき", 15, INK2, anchor="middle"))
        b.append(arrow(cx - 30, YB - 46 * PX, cx + 14, YB - 46 * PX, "ink", 2.6))
        b.append(text(cx, YB + 76, r1, 18, INK, 700, "middle"))
        b.append(text(cx, YB + 102, r2, 16, col, 700, "middle"))
    return svg("".join(b), "とじこめた空気と水をおすと（つぶのモデル）",
               f"赤い矢印＝おす力（どれも約{FP:.0f} kg）。青いつぶ＝空気、緑のつぶ＝水（つぶの数は少なくかいている）。")


def fig2():
    b = []
    X0, Y0, GW, GH = 130, 548, 520, 380
    gx = lambda v: X0 + v / 50 * GW
    gy = lambda f: Y0 - f / FMAX * GH
    b.append(axes(X0, Y0, GW, GH, "", "", [(v / 50 * GW, str(v)) for v in range(0, 51, 10)], [(f / FMAX * GH, str(f)) for f in range(2, FMAX + 1, 2)], 15))
    b.append(text(X0 - 12, Y0 + 6, "0", 15, INK2, anchor="end"))
    b.append(text(48, 132, "手ごたえ（おし返す力）［kg］", 16, INK, 700))
    b.append(text(X0 + GW, Y0 + 48, "中の体積（注しゃ器の目もり）［mL］", 15, INK, anchor="end"))
    b.append(line(gx(40), Y0, gx(40), gy(FMAX), MUTED, 1.4, "5 4") + text(gx(40) - 6, gy(FMAX) + 18, "もとの体積", 14, MUTED, anchor="end"))
    curves = [("air", ACC, "空気だけ"), ("half", PURPLE, "空気と水"), ("water", TEAL_D, "水だけ")]
    for m, col, nm in curves:
        pts = [(gx(vol(m, f / 20)), gy(f / 20)) for f in range(0, FMAX * 20 + 1)]
        b.append(poly(pts, col, 3.6))
    b.append(text(gx(vol("air", 11)) + 10, gy(11) + 6, "空気だけ", 16, ACC, 700))
    b.append(text(gx(vol("half", 9)) - 10, gy(9), "空気と水", 16, PURPLE, 700, "end"))
    b.append(text(gx(40) + 10, gy(6), "水だけ", 16, TEAL_D, 700))
    b.append(text(gx(40) + 10, gy(6) + 20, "（体積が変わらない）", 14, TEAL_D))
    for v in (35, 30, 25, 20, 15):
        b.append(circle(gx(v), gy(f_of_v(v)), 5, "#fff", ACC, 2.4))
    # 右：早見表とまとめ
    RX = 700
    rows = [[f"{v} mL" + ("（もと）" if v == 40 else "（半分）" if v == 20 else ""), "0 kg" if v == 40 else f"約{f_of_v(v):.1f} kg"] for v in (40, 35, 30, 25, 20, 15)]
    b.append(text(RX, 122, "空気だけ（40 mL）のときの早見表", 18, INK, 700))
    b.append(table(RX, 138, ["空気の体積", "手ごたえ（おす力）"], rows, [220, 232], 40, 16.5))
    pts = [("空気", "おしちぢめられる。ちぢめるほど、手ごたえが大きい。", ACC),
           ("水", "おしちぢめられない。体積は変わらない。", TEAL_D),
           ("つぶ", "空気のつぶの数は変わらず、つぶの間がつまる。", "#1d4ed8")]
    for k, (h, t, col) in enumerate(pts):
        y = 478 + k * 56
        b.append(rect(RX, y - 26, 452, 48, CARD, LINE, 8) + text(RX + 14, y + 4, h, 17, col, 700) + text(RX + 66, y + 4, t, 15.5, INK))
    return svg("".join(b), "体積と手ごたえのグラフ（まとめ）",
               "手ごたえ＝その重さのものを持ち上げるくらいの力。注しゃ器の中身40 mL・ピストンの面積6 cm²のときの値。")


FIGS = [
    dict(svg=fig1,
         alt=f"注しゃ器にとじこめた空気・水・空気と水（半分ずつ）を、約{FP:.0f} kgの力でおしたときのつぶのモデルの図。空気だけは40 mLから20 mLに体積が小さくなり、水だけは40 mLのまま変わらず、空気と水では空気の部分だけがちぢんで30 mLになる。",
         caption="とじこめた空気と水をおすと。空気はおしちぢめられるが、水はおしちぢめられない。"),
    dict(svg=fig2,
         alt="注しゃ器の中の体積と手ごたえ（おし返す力）のグラフ。空気だけは体積が小さくなるほど手ごたえが大きくなり、水だけは体積が40 mLのまま変わらない。空気の体積と手ごたえの早見表（20 mLで約6.2 kg、15 mLで約10.3 kg）と、空気と水の性質のまとめもある。",
         caption="体積と手ごたえのグラフ。空気はおしちぢめるほど手ごたえが大きくなり、水はおしちぢめられない。"),
]
