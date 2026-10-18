"""ニュートンのゆりかご（newtons-cradle）の図。
ページの JS と同じ動き（玉5個・左から k 個を持ち上げて離す → 右から k 個が同じ振れ幅で跳ねる・真ん中は動かない）と、
本文の「運動量保存」「運動エネルギー保存」の2つを同時に満たすのは同じ数・同じ速さだけ、を図にする。"""
import math
from figlib import *

ANCHOR = r"パイプ役で、自分はほとんど動きません。</p>\s*"

BALL, BALL_S = "#d9dce1", "#5b6068"


def cradle(cx, top, kl=0, kr=0, ang=45, r=17, L=108, hl=None):
    """玉5個のゆりかご。kl＝左から持ち上げた数、kr＝右から跳ね上がった数。hl＝色をつける玉の番号の集合"""
    n = 5; d = 2 * r
    xs = [cx + (i - 2) * d for i in range(n)]
    hl = hl or set()
    out = [line(xs[0] - r - 26, top, xs[-1] + r + 26, top, INK, 5)]
    for i, x in enumerate(xs):
        a = -ang if i < kl else ang if i >= n - kr else 0
        bx, by = x + L * math.sin(math.radians(a)), top + L * math.cos(math.radians(a))
        out.append(line(x, top, bx, by, MUTED, 1.4))
        on = i in hl
        out.append(circle(bx, by, r, TEAL_L if on else BALL, TEAL if on else BALL_S, 2.2 if on else 1.6))
    return "".join(out), xs


def fig1():
    b = []
    cols = [370, 677, 985]
    heads = ["① 持ち上げて離す", "② ぶつかる", "③ 反対側が跳ね上がる"]
    for x, h in zip(cols, heads):
        b.append(text(x, 124, h, 18, INK, 700, "middle"))
    L, r, ang = 108, 17, 45
    rise = L - L * math.cos(math.radians(ang))
    for row, (k, top) in enumerate([(1, 152), (2, 352)]):
        yb = top + L
        b.append(rect(48, top - 12, 124, 156, TEAL_L, LINE, 10))
        b.append(text(110, top + 50, f"{k}個", 34, TEAL_D, 700, "middle"))
        b.append(text(110, top + 86, "持ち上げると", 15, INK2, anchor="middle"))
        b.append(text(110, top + 110, f"→ {k}個が跳ねる", 15, INK2, 700, "middle"))
        moving_l = set(range(k)); moving_r = set(range(5 - k, 5))
        # ①
        g, xs = cradle(cols[0], top, kl=k, hl=moving_l)
        b.append(g)
        lx = xs[0] - L * math.sin(math.radians(ang))
        b.append(line(lx - 30, yb - rise, xs[-1] + r + 8, yb - rise, GOLD, 1.4, "5 4"))
        b.append(text(xs[-1] + r + 12, yb - rise + 5, "この高さから", 15, GOLD, 700))
        b.append(f'<path d="M{lx - 4:.1f},{yb - rise + 26:.1f} Q{lx + 10:.1f},{yb + 18:.1f} {xs[0] - r - 6:.1f},{yb + 22:.1f}" fill="none" stroke="{TEAL}" stroke-width="2.4" marker-end="url(#ah-teal)"/>')
        # ②
        g, xs = cradle(cols[1], top, hl=moving_l)
        b.append(g)
        b.append(arrow(xs[0] - r, yb + 34, xs[-1] + r, yb + 34, "acc", 2.6))
        b.append(text(cols[1], yb + 60, "玉から玉へ、次々に伝わる", 15, ACC, 700, "middle"))
        # ③
        g, xs = cradle(cols[2], top, kr=k, hl=moving_r)
        b.append(g)
        rx = xs[-1] + L * math.sin(math.radians(ang))
        b.append(line(xs[0] - r - 8, yb - rise, rx + 22, yb - rise, GOLD, 1.4, "5 4"))
        b.append(text(xs[0] - r - 12, yb - rise + 5, "同じ高さまで", 15, GOLD, 700, anchor="end"))
        b.append(f'<path d="M{xs[-1] + r + 6:.1f},{yb + 22:.1f} Q{rx - 10:.1f},{yb + 18:.1f} {rx + 4:.1f},{yb - rise + 26:.1f}" fill="none" stroke="{TEAL}" stroke-width="2.4" marker-end="url(#ah-teal)"/>')
        for x in cols[:2]:
            b.append(arrow(x + 122, top + 30, x + 186, top + 30, "muted", 2))
    b.append(rect(48, 552, 1104, 62, GOLD_L, GOLD, 10, 1.2))
    b.append(text(68, 578, "ぶつけた数と同じ数の玉が、同じ速さで飛び出す（同じ高さまで上がる）。", 17, INK, 700))
    b.append(text(68, 602, "真ん中の玉は、ぶつかった勢いをとなりへ伝えるだけで、ほとんど動かない。", 16, INK2))
    return svg("".join(b), "ニュートンのゆりかご：ぶつけた数だけ反対側が跳ねる",
               "空気抵抗や音などでエネルギーが少しずつ失われるので、実物はやがて止まる。")


def balls_row(x, y, k, speed, r=11):
    out = [circle(x + i * 2 * r, y, r, TEAL_L, TEAL, 1.8) for i in range(k)]
    xe = x + (k - 1) * 2 * r + r + 4
    out.append(arrow(xe, y, xe + 30 * speed, y, "acc", 2.6))
    return "".join(out)


def fig2():
    b = [text(48, 126, "2個をぶつけたとき、反対側の玉はどう跳ねる？", 19, INK, 700),
         text(48, 154, "玉1個の質量を1、ぶつける速さを1とする。運動量とエネルギーの合計が、ぶつける前と同じになるものだけが起こる。", 15, INK2)]
    X = [48, 290, 520, 840, 1152]
    y0, hh, rh = 172, 54, 66
    b.append(rect(X[0], y0, X[-1] - X[0], hh + rh * 5, CARD, LINE, 8))
    b.append(f'<rect x="{X[0]}" y="{y0}" width="{X[-1] - X[0]}" height="{hh}" rx="8" fill="{TEAL_L}"/>')
    heads = [("飛び出す玉", ""), ("運動量の合計", "（質量×速さ）"), ("運動エネルギーの合計", "（½×質量×速さ²）"), ("起こる？", "")]
    for i, (h1, h2) in enumerate(heads):
        cx = (X[i] + X[i + 1]) / 2
        if h2:
            b.append(text(cx, y0 + 24, h1, 16, INK, 700, "middle") + text(cx, y0 + 44, h2, 14, INK2, anchor="middle"))
        else:
            b.append(text(cx, y0 + 34, h1, 16, INK, 700, "middle"))
    from fractions import Fraction as F
    rows = [("前", 2, F(1)), ("案", 1, F(2)), ("正", 2, F(1)), ("案", 3, F(2, 3)), ("案", 4, F(1, 2))]

    def fs(q):
        return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"
    p0 = 2 * F(1); e0 = 2 * F(1, 2) * F(1) ** 2
    for i, (kind, k, v) in enumerate(rows):
        y = y0 + hh + rh * i
        if kind == "前":
            b.append(f'<rect x="{X[0] + 1}" y="{y}" width="{X[-1] - X[0] - 2}" height="{rh}" fill="{GOLD_L}"/>')
        elif kind == "正":
            b.append(f'<rect x="{X[0] + 1}" y="{y}" width="{X[-1] - X[0] - 2}" height="{rh}" fill="#e3eef3"/>')
        b.append(line(X[0], y, X[-1], y, LINE, 1))
        yc = y + rh / 2
        b.append(balls_row(X[0] + 26, yc - 8, k, float(v)))
        lab = f"ぶつける前：{k}個が速さ{fs(v)}" if kind == "前" else f"{k}個が速さ{fs(v)}"
        b.append(text(X[0] + 26 - 11, yc + 24, lab, 14.5, INK, 700 if kind != "案" else 400))
        p = k * v; e = k * F(1, 2) * v * v
        ps = f"{k}×{fs(v)}＝{fs(p)}" if k > 1 else f"1×{fs(v)}＝{fs(p)}"
        es = f"{k}×½×({fs(v)})²＝{fs(e)}" if v.denominator > 1 else f"{k}×½×{fs(v)}²＝{fs(e)}"
        okp, oke = p == p0, e == e0
        mk = lambda ok: "○" if ok else "×"
        if kind == "前":
            b.append(text((X[1] + X[2]) / 2, yc + 7, ps, 17, INK, 700, "middle"))
            b.append(text((X[2] + X[3]) / 2, yc + 7, es, 17, INK, 700, "middle"))
            b.append(text((X[3] + X[4]) / 2, yc + 7, "これと同じになればよい", 15, INK2, anchor="middle"))
            continue
        b.append(text((X[1] + X[2]) / 2, yc + 7, f"{ps}　{mk(okp)}", 17, INK, 400, "middle"))
        b.append(text((X[2] + X[3]) / 2, yc + 7, f"{es}　{mk(oke)}", 17, ACC if not oke else INK, 700 if not oke else 400, "middle"))
        if okp and oke:
            res, col = "起こる（両方とも同じ）", TEAL_D
        else:
            res, col = ("起こらない（エネルギーがふえる）" if e > e0 else "起こらない（エネルギーがへる）"), MUTED
        b.append(text((X[3] + X[4]) / 2, yc + 7, res, 16, col, 700, "middle"))
    for xx in X[1:-1]:
        b.append(line(xx, y0, xx, y0 + hh + rh * 5, LINE, 1))
    b.append(text(48, 612, "運動量だけならどれも同じ。エネルギーも同じになるのは「同じ数・同じ速さ」だけ。", 17, INK, 700))
    return svg("".join(b), "なぜ同じ数だけ跳ねるのか（2つの保存則）",
               "○＝ぶつける前と同じ　×＝ちがう。玉どうしの衝突でエネルギーがほとんど失われない（弾性衝突）とした場合。")


FIGS = [
    dict(svg=fig1, alt="ニュートンのゆりかごの図。5個の玉のうち端の1個（または2個）を高さhまで持ち上げて離すと、ぶつかった勢いが玉から玉へ伝わり、反対側の端から同じ数の玉が同じ高さhまで跳ね上がり、真ん中の玉はほとんど動かないことを示す。",
         caption="ぶつけた数と同じ数の玉が、反対側から同じ高さまで跳ね上がる。真ん中の玉はほとんど動かない。"),
    dict(svg=fig2, alt="ニュートンのゆりかごで2個をぶつけたとき、反対側から1個が速さ2で・2個が速さ1で・3個が速さ3分の2で・4個が速さ2分の1で飛び出す場合の運動量の合計と運動エネルギーの合計を比べた表。運動量はどれも同じだが、運動エネルギーも保存されるのは2個が同じ速さで飛び出す場合だけであることを示す。",
         caption="運動量保存と運動エネルギー保存を両方満たすのは「同じ数・同じ速さ」だけ。"),
]
