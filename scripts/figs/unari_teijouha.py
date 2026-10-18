"""うなりと定常波（unari-teijouha・高校物理基礎）の授業用の図。式はページのシミュ（UNARI_JS）・本文と同じ：
  うなり y＝sin2πf₁t＋sin2πf₂t（包絡線 2|cos π(f₁−f₂)t|）、うなりの回数 |f₁−f₂|。
  定常波（固定端）：入射波 sin(ωt−kx)、反射波 −sin(ωt−k(2L−x))、節の間隔 λ/2（シミュの初期値 λ＝40 cm・長さ1.2 m）。
  弦 fₙ＝nv/2L（v＝√(S/ρ)、L＝0.50 m・S＝40 N・ρ＝1.0 g/m）、閉管 f＝(2n−1)V/4L、開管 f＝nV/2L、V＝331.5＋0.6t（20℃・L＝0.50 m）。"""
import math
from figlib import *

TAU = 2 * math.pi
F1, F2 = 20, 23                      # うなりの図：見やすい低い振動数（|f₁−f₂|＝3 回/秒）
LAM, LW = 0.40, 1.20                 # 定常波：波長 40 cm、長さ 1.2 m、固定端
LS, S, RHO = 0.50, 40.0, 1.0e-3      # 弦
VS = math.sqrt(S / RHO)
TC, LP = 20, 0.50                    # 気柱
V = 331.5 + 0.6 * TC


def hz(f):
    return f"{f:.1f} Hz".replace(".0 Hz", " Hz") if abs(f * 10 - round(f * 10)) < 1e-9 else f"約{f:.0f} Hz"


def curve(fn, x0, x1, n=600):
    return [(x0 + (x1 - x0) * k / n, fn(k / n)) for k in range(n + 1)]


def strip_bg(x0, y, w, h):
    return rect(x0, y - h / 2, w, h, "#f4f7f9", LINE, 4, 1) + line(x0, y, x0 + w, y, LINE, 1)


def fig1():
    b = []
    # ===== 左：うなり =====
    b.append(rect(48, 100, 540, 512, CARD, LINE, 12))
    b.append(badge(76, 132, "1", TEAL, "#fff", 17) + text(100, 139, "うなり（2つの音の重ね合わせ）", 19, INK, 700))
    x0, w = 120, 440
    rows = [(198, 56, f"f₁＝{F1} Hz", lambda t: math.sin(TAU * F1 * t), 1, TEAL),
            (272, 56, f"f₂＝{F2} Hz", lambda t: math.sin(TAU * F2 * t), 1, GOLD),
            (400, 132, "合成波", lambda t: math.sin(TAU * F1 * t) + math.sin(TAU * F2 * t), 2, INK)]
    for yc, h, lab, fn, amp, col in rows:
        b.append(strip_bg(x0, yc, w, h))
        b.append(poly([(x, yc - fn(t) / amp * (h / 2 - 4)) for x, t in curve(lambda u: u, x0, x0 + w)], col, 1.6))
        b.append(text(x0 - 10, yc + 6, lab, 15, col if col != GOLD else "#8a6216", 700, "end"))
    yc, h = 400, 132
    env = lambda t: abs(math.cos(math.pi * (F1 - F2) * t))       # 2|cos|/2（合成波の振幅の半分で正規化）
    for sg in (1, -1):
        b.append(poly([(x0 + w * t, yc - sg * env(t) * (h / 2 - 4)) for t in [k / 300 for k in range(301)]], ACC, 2.2, dash="7 5"))
    nb = abs(F1 - F2)
    for k in range(nb + 1):
        xx = x0 + w * k / nb
        b.append(line(xx, yc + h / 2, xx, yc + h / 2 + 8, INK, 1.4) + text(xx, yc + h / 2 + 26, ["0", "1/3", "2/3", "1"][k] + (" 秒" if k == nb else ""), 14, INK2, anchor="middle"))
        if k: b.append(badge(xx, yc - h / 2 - 2, str(k), ACC, "#fff", 13))
    b.append(lines(70, 526, ["赤の点線＝振幅（音の大きさ）。大きくなる回数は", f"1秒間に |f₁−f₂|＝|{F1}−{F2}|＝{nb} 回（うなり）。", "440 Hz と 443 Hz でも 3 回/秒になる。", "（図は見やすいように振動数を小さくしてある）"], 16, INK, 1.42))
    # ===== 右：定常波 =====
    b.append(rect(612, 100, 540, 512, CARD, LINE, 12))
    b.append(badge(640, 132, "2", TEAL, "#fff", 17) + text(664, 139, "定常波（固定端で反射）", 19, INK, 700))
    X0, Wd = 670, 440
    sx = Wd / LW
    k = TAU / LAM
    ph = math.pi / 4                                         # 時刻 t＝T/8
    yi = lambda x: math.sin(ph - k * x)
    yr = lambda x: -math.sin(ph - k * (2 * LW - x))
    rows = [(198, 56, "入射波 →", yi, 1, TEAL), (272, 56, "反射波 ←", yr, 1, GOLD), (400, 132, "合成波", lambda x: yi(x) + yr(x), 2, INK)]
    for yc, h, lab, fn, amp, col in rows:
        b.append(strip_bg(X0, yc, Wd, h))
        b.append(poly([(X0 + x * sx, yc - fn(x) / amp * (h / 2 - 4)) for x in [LW * q / 600 for q in range(601)]], col, 2.2))
        parts = lab.split(" ")
        for q, ptxt in enumerate(parts):
            b.append(text(X0 - 10, yc + 6 + (q - (len(parts) - 1) / 2) * 20, ptxt, 15, col if col != GOLD else "#8a6216", 700, "end"))
    yc, h = 400, 132
    for sg in (1, -1):
        b.append(poly([(X0 + x * sx, yc - sg * abs(math.sin(k * (LW - x))) * (h / 2 - 4)) for x in [LW * q / 600 for q in range(601)]], ACC, 1.8, dash="6 5"))
    b.append(rect(X0 + Wd, 160, 10, 310, "#c9c4b8", MUTED, 0, 1) + text(X0 + Wd + 5, 154, "固定端", 14, INK2, anchor="middle"))
    nm = round(LW / (LAM / 2))
    nodes = [LW - m * LAM / 2 for m in range(nm + 1)]
    anti = [LW - LAM / 4 - m * LAM / 2 for m in range(nm)]
    for xn in nodes:
        b.append(circle(X0 + xn * sx, yc, 5, PURPLE, CARD, 1.5) + text(X0 + xn * sx, yc + h / 2 + 24, "節", 15, PURPLE, 700, "middle"))
    for xa in anti:
        b.append(text(X0 + xa * sx, yc + h / 2 + 24, "腹", 15, ACC, 700, "middle"))
    xa_, xb_ = X0 + nodes[-1] * sx, X0 + nodes[-2] * sx
    b.append(line(xa_, 324, xb_, 324, INK, 1.4) + line(xa_, 318, xa_, 330, INK, 1.4) + line(xb_, 318, xb_, 330, INK, 1.4) + text((xa_ + xb_) / 2, 318, "λ/2", 15, INK, 700, "middle"))
    b.append(lines(634, 530, [f"節の間隔＝λ/2（λ＝{LAM * 100:.0f} cm なら {LAM * 50:.0f} cm）、腹と節＝λ/4。", "固定端は節、自由端は腹になる。", "波形は左右に進まず、その場で振動する。"], 16, INK, 1.5))
    return svg("".join(b), "うなりと定常波のしくみ（重ね合わせ）",
               "合成波の各点の変位は、2つの波の変位の和（重ね合わせの原理）。定常波の図は時刻 t＝T/8 のようす。")


def cell(x, y, w, kind, n):
    """固有振動の小さな図。kind＝'str'/'closed'/'open'、n＝何番目か"""
    out = []
    xa, xb, yc, A = x + 26, x + w - 26, y + 62, 34
    L = xb - xa
    if kind == "str":
        u = lambda s: math.sin(n * math.pi * s)
        nodes = [j / n for j in range(n + 1)]
        anti = [(j + 0.5) / n for j in range(n)]
        out.append(line(xa - 10, yc, xb + 10, yc, LINE, 1))
        for X in (xa, xb):
            out.append(f'<path d="M{X},{yc} l-8,14 h16z" fill="{MUTED}"/>')
    else:
        h = 2 * n - 1 if kind == "closed" else n
        lam = 4 / h if kind == "closed" else 2 / n         # 管の長さ 1 に対する波長
        kk = TAU / lam
        u = (lambda s: math.sin(kk * s)) if kind == "closed" else (lambda s: math.cos(kk * s))
        nodes = [j * lam / 2 for j in range(10) if j * lam / 2 <= 1 + 1e-9] if kind == "closed" else [lam / 4 + j * lam / 2 for j in range(10) if lam / 4 + j * lam / 2 <= 1 + 1e-9]
        anti = [lam / 4 + j * lam / 2 for j in range(10) if lam / 4 + j * lam / 2 <= 1 + 1e-9] if kind == "closed" else [j * lam / 2 for j in range(10) if j * lam / 2 <= 1 + 1e-9]
        out.append(f'<rect x="{xa}" y="{yc - A - 8}" width="{L}" height="{2 * A + 16}" fill="#eef3f6"/>')
        out.append(line(xa, yc - A - 8, xb, yc - A - 8, INK2, 3) + line(xa, yc + A + 8, xb, yc + A + 8, INK2, 3))
        if kind == "closed":
            out.append(rect(xa - 9, yc - A - 10, 9, 2 * A + 20, INK2, INK2, 0, 0))
    for sg in (1, -1):
        out.append(poly([(xa + L * s, yc - sg * A * u(s)) for s in [q / 200 for q in range(201)]], TEAL, 2.4))
    for s in nodes:
        out.append(circle(xa + L * s, yc, 4.5, PURPLE, CARD, 1.4))
    for s in anti:
        out.append(circle(xa + L * s, yc, 4.5, CARD, ACC, 2))
    return "".join(out)


def fig2():
    b = []
    heads = ["1番目（基本振動）", "2番目", "3番目"]
    for j, hd in enumerate(heads):
        b.append(text(278 + j * 292 + 138, 120, hd, 16, INK, 700, "middle"))
    rows = [("弦（両端を固定）", "fₙ ＝ nv / 2L", "両端が節", "str", [k * VS / (2 * LS) for k in (1, 2, 3)], ["基本振動", "2倍振動", "3倍振動"]),
            ("閉管（片方が閉じた管）", "f ＝ (2n−1)V / 4L", "閉じた端が節・開いた端が腹", "closed", [k * V / (4 * LP) for k in (1, 3, 5)], ["基本振動", "3倍振動", "5倍振動"]),
            ("開管（両方が開いた管）", "f ＝ nV / 2L", "両端が腹", "open", [k * V / (2 * LP) for k in (1, 2, 3)], ["基本振動", "2倍振動", "3倍振動"])]
    for i, (nm, fml, end, kind, fs, nms) in enumerate(rows):
        y = 134 + i * 160
        b.append(rect(48, y, 218, 150, TEAL_L, LINE, 10))
        b.append(text(62, y + 34, nm, 16, INK, 700) + text(62, y + 74, fml, 19, TEAL_D, 700) + text(62, y + 112, end, 14.5, INK2))
        if kind == "closed": b.append(text(62, y + 134, "奇数倍だけ現れる", 14.5, ACC, 700))
        else: b.append(text(62, y + 134, "整数倍すべて現れる", 14.5, INK2))
        for j in range(3):
            x = 278 + j * 292
            b.append(rect(x, y, 276, 150, CARD, LINE, 10))
            b.append(cell(x, y, 276, kind, j + 1))
            b.append(text(x + 138, y + 138, f"{nms[j]}　{hz(fs[j])}", 16, INK, 700, "middle"))
    b.append(circle(56, 622, 5, PURPLE, CARD, 1.4) + text(66, 627, "節", 14, PURPLE, 700) + circle(100, 622, 5, CARD, ACC, 2) + text(110, 627, "腹", 14, ACC, 700))
    b.append(text(146, 627, f"弦：L＝{LS:.2f} m・S＝{S:.0f} N・ρ＝1.0 g/m（v＝{VS:.0f} m/s）　管：L＝{LP:.2f} m・{TC}℃（V＝{V:.1f} m/s）・開口端補正なし", 14, INK2))
    return svg("".join(b), "弦と気柱の固有振動（まとめ）",
               "気柱の図は空気の変位（縦波）を縦向きにかいたもの。閉じた端は変位の節、開いた端は腹。", )


FIGS = [
    dict(svg=fig1, alt="うなりと定常波のしくみの図。振動数が少しちがう2つの音（20 Hzと23 Hz）を重ねると合成波の振幅が1秒間に3回（|f₁−f₂|回）大きくなるうなりと、右向きの入射波と固定端で反射した左向きの反射波を重ねてできる定常波（節の間隔λ/2、固定端が節）を示す。",
         caption="うなりと定常波。うなりの回数は |f₁−f₂| 回/秒、定常波の節の間隔は λ/2。"),
    dict(svg=fig2, alt="弦（両端固定）・閉管・開管の固有振動のまとめ。基本振動から3番目までの定常波の形と節・腹の位置、固有振動数の式（fₙ＝nv/2L、f＝(2n−1)V/4L、f＝nV/2L）と、長さ0.50 mの例の振動数（弦200・400・600 Hz、閉管約172・515・859 Hz、開管343.5・687・1030.5 Hz）。",
         caption="弦・閉管・開管の固有振動。閉管だけは基本振動の奇数倍しか現れない。"),
]
