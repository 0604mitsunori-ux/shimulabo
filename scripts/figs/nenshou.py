"""ものの燃え方と空気（nenshou）の授業用の図（小6）
数値はシミュ（scripts/rika/sims_youkai_nenshou.py の JS_NENSHOU）と同じモデルで計算する：
  はじめの空気 窒素78.0・酸素21.0・二酸化炭素0.04・その他0.96（はじめの空気の量を100とした割合）。
  炎の大きさ f＝√((酸素−16.8)/4.2)（上限1.8）、f＜0.25 で火が消える。酸素の減り方 k×f、二酸化炭素の増え方 その r 倍。
  空気の入れかわり q：ふたなし＋すき間 0.8、ふたなし 0.27、ふた＋すき間 0.012、ふた 0（炎の熱で強まる）。"""
import math
from figlib import *

AIR = [78.0, 21.0, 0.04, 0.96]
FUEL = {"candle": (0.5, 0.66), "wood": (0.8, 1.0)}
OX, FMIN = 16.8, 0.25
CN, CO, CC, CX = "#b9bdc4", ACC, TEAL, "#ffffff"      # 窒素・酸素・二酸化炭素・その他


def run(lid, gap, fuel="candle", dt=1 / 60, T=120):
    """シミュの start()/step() と同じ計算。火が消えた時刻と、そのとき（燃え続けるときは T 秒後）の割合を返す"""
    comp = AIR[:]; lit = True; heat = 0.7; t = 0.0; k, r = FUEL[fuel]
    q0 = (0.012 if gap else 0.0) if lid else (0.8 if gap else 0.27)
    flame = lambda: min(1.8, math.sqrt(max(0.0, (comp[1] - OX) / (21 - OX))))
    while t < T:
        t += dt; f = 0.0
        if lit:
            f = flame()
            if f < FMIN: return t, comp[:]
        heat += ((min(1, f) if lit else 0) - heat) * min(1, dt / 0.5)
        q = q0 * (0.25 + 0.75 * heat)
        comp[1] = max(0.0, comp[1] - k * f * dt); comp[2] += k * f * r * dt
        for i in range(4): comp[i] += q * (AIR[i] - comp[i]) * dt
    return None, comp


def counts(v):
    """シミュの counts()：空気の粒100こに丸める"""
    n = [round(v[0]), round(v[1]), round(v[2])]; s = sum(n)
    while s > 100:
        i = n.index(max(n)); n[i] -= 1; s -= 1
    return n + [100 - s]


def f1(v): return f"{math.floor(v * 10 + 1e-7 + 0.5) / 10:.1f}"
def fc(v): return f"{math.floor(v * 100 + 1e-7 + 0.5) / 100:.2f}" if v < 0.995 else f1(v)


def grid(x0, y0, n, d=27, r=10):
    out, k = [], 0
    for g, cnt in enumerate(n):
        for _ in range(cnt):
            cx, cy = x0 + (k % 10) * d + r, y0 + (k // 10) * d + r
            if g == 2: out.append(rect(cx - r + 0.5, cy - r + 0.5, 2 * r - 1, 2 * r - 1, CC, INK, 4, 1))   # 二酸化炭素は四角
            else: out.append(circle(cx, cy, r, [CN, CO, CC, CX][g], INK if g == 3 else "none", 1))
            k += 1
    return "".join(out)


def legend_item(x, y, g, label):
    r = 9
    mark = (rect(x - r, y - r - 5, 2 * r, 2 * r, CC, INK, 4, 1) if g == 2
            else circle(x, y - 5, r, [CN, CO, CC, CX][g], INK if g == 3 else "none", 1))
    return mark + text(x + 16, y, label, 16, INK, 700 if g in (1, 2) else 400)


def jar(cx, top, bot, lid, gap, scale=1.0):
    """集気びん（ねんどの台の上）。top＝口、bot＝底"""
    nk, bw = 34 * scale, 74 * scale; sh = top + 26 * scale; bd = top + 54 * scale
    d = (f"M{cx - bw},{bot} L{cx - bw},{bd} Q{cx - bw},{sh} {cx - nk},{sh} L{cx - nk},{top} "
         f"M{cx + bw},{bot} L{cx + bw},{bd} Q{cx + bw},{sh} {cx + nk},{sh} L{cx + nk},{top}")
    out = [f'<path d="M{cx - bw},{bot} L{cx - bw},{bd} Q{cx - bw},{sh} {cx - nk},{sh} L{cx - nk},{top} L{cx + nk},{top} L{cx + nk},{sh} Q{cx + bw},{sh} {cx + bw},{bd} L{cx + bw},{bot}Z" fill="#eef5f8"/>',
           rect(cx - bw - 26, bot, 2 * bw + 52, 22, "#e2cfa8", "#c9b285", 5)]
    if gap:
        for gx in (cx - bw, cx + bw):
            out.append(f'<rect x="{gx - 12}" y="{bot - 1}" width="24" height="12" fill="{BG}" stroke="#c9b285" stroke-width="1"/>')
    out.append(f'<path d="{d}" fill="none" stroke="{INK2}" stroke-width="2.6"/>')
    if lid:
        out.append(rect(cx - nk - 14, top - 8, 2 * nk + 28, 8, "#cfe3ee", INK2, 1, 1.2))
    return "".join(out)


def candle(cx, bot, lit, big=1.0):
    out = [rect(cx - 9, bot - 70, 18, 70, "#fbf6e4", "#cfc6ad", 2, 1.2), line(cx, bot - 70, cx, bot - 78, INK, 2)]
    if lit:
        h, w = 30 * big, 9 * min(1.3, big)
        out.append(f'<path d="M{cx},{bot - 76 - h} C{cx + w},{bot - 76 - h * 0.45} {cx + w},{bot - 74} {cx},{bot - 74} C{cx - w},{bot - 74} {cx - w},{bot - 76 - h * 0.45} {cx},{bot - 76 - h}Z" fill="{SUN}" stroke="{GOLD}" stroke-width="1.2"/>')
    else:
        out.append(f'<path d="M{cx},{bot - 80} q-6,-10 0,-20 q6,-10 0,-20" fill="none" stroke="{MUTED}" stroke-width="1.8" stroke-dasharray="3 3"/>')
    return "".join(out)


def fig1():
    b = []
    tout, aft = run(True, False)
    nb, na = counts(AIR), counts(aft)
    # 左：燃やす前
    for x0, head, n, vals in [(64, "燃やす前の空気", nb, AIR), (868, "火が消えたあとの空気", na, aft)]:
        b.append(rect(x0 - 16, 100, 302, 420, CARD, LINE, 12))
        b.append(text(x0 + 135, 132, head, 19, INK, 700, "middle"))
        b.append(grid(x0, 150, n))
        rows = [(0, f"窒素 {n[0]}こ"), (1, f"酸素 {n[1]}こ"), (2, f"二酸化炭素 {n[2]}こ"), (3, f"その他 {n[3]}こ")]
        for i, (g, lab) in enumerate(rows):
            b.append(legend_item(x0 + 10 + (i % 2) * 168, 448 + (i // 2) * 32, g, lab))
        b.append(text(x0 + 135, 510, "（粒1こ＝約1%）", 14, MUTED, anchor="middle"))
    # まん中：集気びん
    cx = 600
    b.append(text(cx, 132, "ふたをした集気びんで", 17, INK, 700, "middle"))
    b.append(text(cx, 156, "ろうそくを燃やす", 17, INK, 700, "middle"))
    b.append(jar(cx, 210, 430, True, False))
    b.append(candle(cx, 430, True))
    b.append(arrow(372, 300, 506, 300, "ink", 3))
    b.append(arrow(694, 300, 846, 300, "ink", 3))
    b.append(text(cx, 478, f"約{tout:.1f}秒で火が消える", 17, ACC, 700, "middle"))
    b.append(text(cx, 502, "石灰水を入れてふると", 15, INK2, anchor="middle"))
    b.append(text(cx, 522, "白くにごる", 15, INK2, 700, "middle"))
    # 下：まとめ
    y = 540
    cells = [("窒素", f"約{f1(AIR[0])}% → 約{f1(aft[0])}%", "変わらない（燃えることに関係しない）", INK2),
             ("酸素", f"約{f1(AIR[1])}% → 約{f1(aft[1])}%", "燃えるときに使われて減る（0%にはならない）", ACC),
             ("二酸化炭素", f"約{fc(AIR[2])}% → 約{fc(aft[2])}%", "燃えるとできて増える", TEAL_D)]
    for i, (nm, v, why, col) in enumerate(cells):
        x = 48 + i * 372
        b.append(rect(x, y, 360, 76, CARD, col, 10, 1.6))
        b.append(text(x + 16, y + 30, nm, 18, col, 700) + text(x + 16 + len(nm) * 18 + 14, y + 30, v, 18, INK, 700))
        b.append(text(x + 16, y + 60, why, 15, INK2))
    return svg("".join(b), "ものが燃えるときの空気の変化（粒の図）",
               "数値はシミュの値（ふたをした集気びん・ろうそく）。木（わりばし）では二酸化炭素は約4.0%になる。")


def fig2():
    b = []
    conds = [(True, False, "ふたをする・すき間なし"), (True, True, "ふたをする・下にすき間あり"),
             (False, False, "ふたをしない・すき間なし"), (False, True, "ふたをしない・下にすき間あり")]
    pw, gp = 264, 16
    for i, (lid, gap, head) in enumerate(conds):
        x0 = 48 + i * (pw + gp); cx = x0 + pw / 2
        tout, comp = run(lid, gap)
        b.append(rect(x0, 100, pw, 470, CARD, LINE, 12))
        b.append(badge(x0 + 24, 128, str(i + 1), TEAL, "#fff", 16))
        b.append(text(x0 + 44, 134, head, 16 if len(head) <= 11 else 15, INK, 700))
        top, bot = 214, 430
        b.append(jar(cx, top, bot, lid, gap, 0.92))
        b.append(candle(cx, bot, tout is None, 1.0 if tout is None else 0))
        nk, bw = 34 * 0.92, 74 * 0.92
        if not lid and gap:       # 下のすき間から入り、上の口から出ていく
            for s_ in (-1, 1):
                b.append(f'<path d="M{cx + s_ * (bw + 46)},{bot - 34} L{cx + s_ * (bw + 2)},{bot + 4} Q{cx + s_ * 28},{bot - 2} {cx + s_ * 16},{bot - 100}" fill="none" stroke="{TEAL}" stroke-width="2.6" stroke-linejoin="round" marker-end="url(#ah-teal)"/>')
                b.append(text(cx + s_ * (bw + 46), bot - 44, "入る", 15, TEAL, 700, "middle"))
            b.append(arrow(cx, bot - 130, cx, top - 34, "acc", 2.8))
            b.append(text(cx, top - 46, "出ていく", 15, ACC, 700, "middle"))
        elif not lid:             # 上の口のふちから入り、まん中から出ていく
            for s_ in (-1, 1):
                b.append(f'<path d="M{cx + s_ * (nk + 24)},{top - 40} Q{cx + s_ * (nk - 6)},{top - 10} {cx + s_ * (nk - 10)},{top + 54}" fill="none" stroke="{TEAL}" stroke-width="2.6" marker-end="url(#ah-teal)"/>')
                b.append(text(cx + s_ * (nk + 30), top - 48, "入る", 15, TEAL, 700, "middle"))
            b.append(arrow(cx, bot - 130, cx, top - 34, "acc", 2.8))
            b.append(text(cx, top - 46, "出ていく", 15, ACC, 700, "middle"))
        else:
            b.append(text(cx, top - 26, "空気が入れかわらない" if not gap else "ほとんど入れかわらない", 15, MUTED, 700, "middle"))
        # 結果
        y = 488
        if tout is not None:
            b.append(text(cx, y, "火が消える", 19, INK, 700, "middle"))
            b.append(text(cx, y + 28, f"（約{tout:.1f}秒）", 16, INK2, anchor="middle"))
        else:
            b.append(text(cx, y, "よく燃え続ける" if gap else "燃え続ける", 19, ACC, 700, "middle"))
            b.append(text(cx, y + 28, f"（酸素 約{f1(comp[1])}%）", 16, INK2, anchor="middle"))
    b.append(arrow(56, 604, 92, 604, "teal", 2.6) + text(100, 610, "新しい空気が入る", 16, TEAL, 700))
    b.append(arrow(300, 614, 300, 590, "acc", 2.6) + text(312, 610, "あたためられた空気が出ていく", 16, ACC, 700))
    b.append(text(1152, 610, "空気が入れかわると、ものは燃え続ける", 18, INK, 700, "end"))
    return svg("".join(b), "集気びんの条件と燃え方（くらべる）",
               "線香のけむりを近づけると、空気の流れが分かる。秒数・酸素の割合はシミュの値（ろうそく）。")


FIGS = [
    dict(svg=fig1, alt="ふたをした集気びんでろうそくを燃やす前と、火が消えたあとの空気を、空気の粒100こ（窒素・酸素・二酸化炭素・その他）で表した図。酸素は約21%から約17%に減り、二酸化炭素は約0.04%から約2.6%に増え、窒素は約78%のまま変わらない。石灰水は白くにごる。",
         caption="ものが燃えるときの空気の変化。酸素の一部が使われて二酸化炭素ができる。火が消えても酸素は約17%残っている。"),
    dict(svg=fig2, alt="集気びんのふたと下のすき間の4つの条件（ふたあり・すき間なし、ふたあり・すき間あり、ふたなし・すき間なし、ふたなし・すき間あり）で、空気の流れとろうそくの燃え方（火が消える・燃え続ける）をくらべた図。",
         caption="集気びんの条件と燃え方。下のすき間から新しい空気が入り、上の口から出ていくと、よく燃え続ける。"),
]
