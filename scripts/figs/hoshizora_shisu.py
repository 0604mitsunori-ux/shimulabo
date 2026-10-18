"""今夜の星空指数（hoshizora-shisu）の図。指数の決め方（雲量×月明かり）の早見表／月齢と月の光って見える割合。
数値の正：ページの JS
  illum = (1 − cos(2π・月齢/29.530588853)) / 2
  指数  = max(0, round((100 − 雲量の平均) × (1 − 0.55 × illum)))
  判定  = 80以上 満天チャンス／60以上 よく見えそう／40以上 明るい星なら見える／20以上 今夜は厳しめ／それ未満 今夜は絶望的
月の出ている時間は tsuki-michikake の図2と同じ目安（上弦＝真夜中に沈む・下弦＝真夜中にのぼる）。
実際の明るさ（半月は満月の約1/11）は、位相角による等級差 約2.6等（Allen の式）で別に確かめた。"""
import math
from figlib import *

P = 29.530588853


def illum(age):
    return (1 - math.cos(2 * math.pi * age / P)) / 2


def index(cloud, age):
    v = (100 - cloud) * (1 - 0.55 * illum(age))
    return max(0, math.floor(v + 0.5))          # JS の Math.round と同じ


LABELS = [(80, "満天チャンス"), (60, "よく見えそう"), (40, "明るい星なら見える"), (20, "今夜は厳しめ"), (0, "今夜は絶望的…")]
CELL = {80: (TEAL_D, "#fff"), 60: (TEAL, "#fff"), 40: ("#8fb5c7", INK), 20: ("#cddde5", INK), 0: ("#eef2f4", INK2)}


def fac(v):
    """月明かりの補正（指数にかける数）を小数2けたで（0.725→0.73）"""
    return f"{math.floor((1 - 0.55 * v) * 100 + 0.5) / 100:.2f}"


def band(s):
    return next(t for t, _ in LABELS if s >= t)


def fig1():
    b = []
    # 式
    y = 112
    b.append(rect(48, y, 1104, 76, CARD, LINE, 10))
    b.append(text(70, y + 47, "星空指数", 22, INK, 700))
    b.append(text(178, y + 47, "＝", 22, INK, 700))
    b.append(rect(214, y + 12, 268, 52, TEAL_L, "none", 8, 0))
    b.append(text(348, y + 36, "100 − 雲量（%）", 19, TEAL_D, 700, "middle"))
    b.append(text(348, y + 56, "雲のない割合", 14, INK2, anchor="middle"))
    b.append(text(500, y + 47, "×", 22, INK, 700, "middle"))
    b.append(rect(520, y + 12, 452, 52, GOLD_L, "none", 8, 0))
    b.append(text(746, y + 36, "1 − 0.55 × 月の光って見える割合", 19, "#7a5512", 700, "middle"))
    b.append(text(746, y + 56, "月明かりの補正（新月 1.00 〜 満月 0.45）", 14, INK2, anchor="middle"))
    b.append(text(992, y + 47, "→ 0〜100点", 19, INK, 700))
    # 早見表
    cols = [("新月", 0.0, "月齢0"), ("三日月", 3.0, "月齢3"), ("上弦の月", P / 4, "月齢7.4"), ("十三夜の月", 12.0, "月齢12"), ("満月", P / 2, "月齢14.8")]
    clouds = [0, 20, 40, 60, 80, 100]
    x0, y0, hw, cw, hh, rh = 48, 206, 150, 136, 104, 50
    b.append(text(x0 + hw / 2, y0 + 50, "今夜の雲量", 16, INK, 700, "middle"))
    b.append(text(x0 + hw / 2, y0 + 74, "↓　月の形 →", 15, INK2, anchor="middle"))
    for j, (nm, age, lab) in enumerate(cols):
        cx = x0 + hw + cw * j + cw / 2
        b.append(moon_look(cx, y0 + 30, 20, 360 * age / P))
        b.append(text(cx, y0 + 74, nm, 16, INK, 700, "middle"))
        b.append(text(cx, y0 + 95, f"{lab}・×{fac(illum(age))}", 14, INK2, anchor="middle"))
    for i, c in enumerate(clouds):
        yy = y0 + hh + rh * i
        b.append(text(x0 + hw - 24, yy + rh / 2 + 7, f"{c}%", 18, INK, 700, "end"))
        for j, (nm, age, lab) in enumerate(cols):
            s = index(c, age)
            f, tc = CELL[band(s)]
            xx = x0 + hw + cw * j
            b.append(rect(xx + 2, yy + 2, cw - 4, rh - 4, f, "none", 4, 0))
            b.append(text(xx + cw / 2, yy + rh / 2 + 7, str(s), 19, tc, 700, "middle"))
    # 判定の凡例
    lx, ly = 900, 312
    b.append(text(lx, ly - 12, "判定（このページの表示）", 16, INK, 700))
    for k, (t, lab) in enumerate(LABELS):
        f, tc = CELL[t]
        yy = ly + 8 + k * 52
        b.append(rect(lx, yy, 44, 36, f, "none", 4, 0))
        rng = f"{t}点以上" if t else "19点以下"
        b.append(text(lx + 56, yy + 16, rng, 14, INK2))
        b.append(text(lx + 56, yy + 35, lab, 16, INK, 700))
    return svg("".join(b), "星空指数の決め方（雲量×月明かり）",
               "雲量は今夜の数時間の予報の平均（Open-Meteo）。街明かりは入れていないので、暗い場所ほど実際は多く見える。")


def fig2():
    b = []
    X0, Y0, Wd, Hd = 110, 560, 520, 300          # グラフ：月齢 0〜29.5 × 割合 0〜100%
    px = lambda a: X0 + a / P * Wd
    py = lambda v: Y0 - v * Hd
    b.append(axes(X0, Y0, Wd, Hd, "", "",
                  [(px(a) - X0, f"{a:g}") for a in (0, 5, 10, 15, 20, 25)] + [(Wd, "29.5")],
                  [(Hd * v, f"{round(v * 100)}%") for v in (0, .25, .5, .75, 1)], 14))
    b.append(text(X0 - 60, Y0 - Hd - 30, "月の光って見える割合", 15, INK, 700))
    pts = [(px(a / 10), py(illum(a / 10))) for a in range(0, 296)]
    b.append(poly(pts, GOLD, 3.4))
    # 右の目盛：指数にかける数
    for v in (0, .5, 1):
        b.append(text(X0 + Wd + 30, py(v) + 5, f"×{fac(v)}", 15, ACC, 700))
    b.append(text(X0 + Wd + 30, Y0 - Hd - 30, "指数にかける数", 15, ACC, 700))
    b.append(text(X0 + Wd / 2, Y0 + 50, "月齢（新月からの日数）", 15, INK, 700, "middle"))
    # 月の形
    for a, nm in [(0, "新月"), (P / 4, "上弦"), (P / 2, "満月"), (3 * P / 4, "下弦")]:
        b.append(moon_look(px(a), 140, 17, 360 * a / P))
        b.append(text(px(a), 178, nm, 15, INK, 700, "middle"))
        b.append(line(px(a), 188, px(a), py(illum(a)) - 6, LINE, 1.4, "4 4"))
        b.append(circle(px(a), py(illum(a)), 5, GOLD, GOLD, 0))
    # 右：月が出ている時間
    X = 800
    b.append(text(X, 128, "月が空に出ている時間（目安）", 18, INK, 700))
    b.append(table(X, 144, ["月の形", "夜に出ている時間"],
                   [["新月", "夜は出ていない"], ["上弦の月", "夕方〜真夜中"], ["満月", "一晩中"], ["下弦の月", "真夜中〜明け方"]],
                   [118, 234], 46, 16))
    b.append(lines(X, 400, ["上弦のころは真夜中すぎ、", "下弦のころは真夜中まえに、", "月のない暗い空になる。"], 16, INK, 1.5))
    b.append(lines(X, 506, ["実際の明るさは、半月（上弦・下弦）でも", "満月の約10分の1。満月の前後に", "急に明るくなる。"], 14.5, INK2, 1.5))
    return svg("".join(b), "月齢と、月の光って見える割合",
               "このページは「光って見える割合」で月明かりを補正する（新月×1.00、上弦・下弦×0.73、満月×0.45）。")


FIGS = [
    dict(svg=fig1, alt="今夜の星空指数の決め方。星空指数＝（100−雲量）×（1−0.55×月の光って見える割合）で、雲量0〜100%と月の形（新月・三日月・上弦の月・十三夜の月・満月）ごとの指数の早見表。新月で雲量0%なら100点、満月で雲量0%なら45点。",
         caption="星空指数の決め方。雲が少なく、月が細いほど点が高い。満月の夜は雲がなくても45点まで。"),
    dict(svg=fig2, alt="月齢（0〜29.5日）と月の光って見える割合のグラフ。新月で0%、上弦・下弦で50%、満月で100%になり、星空指数にかける数は新月1.00・上弦0.73・満月0.45。新月・上弦・満月・下弦の月が夜空に出ている時間の目安の表もつけている。",
         caption="月齢と月の光って見える割合。満月に近いほど月明かりで淡い星が見えにくくなる。"),
]
