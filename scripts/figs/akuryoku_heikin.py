"""握力の平均（akuryoku-heikin）の図。値はページの JS（AV）・早見表と同じ（スポーツ庁「体力・運動能力調査」をもとにした丸めた目安）。"""
from figlib import *

ANCHOR = r'<div class="note" style="border-left:4px solid var\(--teal\)">.*?</div>\n'
AGES = [("13", "中学生"), ("16", "高校生"), ("20", "20代"), ("30", "30代"), ("40", "40代"), ("50", "50代"), ("60", "60代"), ("70", "70代")]
AV = {"m": {13: 30, 16: 41, 20: 46, 30: 47, 40: 46, 50: 44, 60: 40, 70: 35},
      "f": {13: 24, 16: 26, 20: 28, 30: 28, 40: 28, 50: 26, 60: 24, 70: 22}}


def fig1():
    b = []
    x0, y0, w, h, YM = 110, 560, 780, 430, 50
    n = len(AGES)
    cx = lambda i: x0 + (i + 0.5) * w / n
    py = lambda v: y0 - v * h / YM
    b.append(axes(x0, y0, w, h, "", "握力（kg）", [], [(v * h / YM, f"{v}") for v in range(0, 51, 10)], 15))
    for i, (_, lab) in enumerate(AGES):
        b.append(line(cx(i), y0, cx(i), y0 + 6, INK, 1.4) + text(cx(i), y0 + 28, lab, 16, INK, 700, "middle"))
    m = [AV["m"][int(k)] for k, _ in AGES]
    f = [AV["f"][int(k)] for k, _ in AGES]
    b.append(poly([(cx(i), py(v)) for i, v in enumerate(m)], TEAL, 3.4))
    b.append(poly([(cx(i), py(v)) for i, v in enumerate(f)], ACC, 3.4, dash="9 5"))
    pk = m.index(max(m))
    for i, v in enumerate(m):
        b.append(circle(cx(i), py(v), 7, TEAL, "#fff", 2) + text(cx(i), py(v) - (22 if i == pk else 16), f"{v}", 18, TEAL_D, 700, "middle"))
    for i, v in enumerate(f):
        b.append(f'<rect x="{cx(i) - 7:.1f}" y="{py(v) - 7:.1f}" width="14" height="14" fill="{ACC}" stroke="#fff" stroke-width="2"/>'
                 + text(cx(i), py(v) + 30, f"{v}", 18, ACC, 700, "middle"))
    b.append(circle(cx(pk), py(m[pk]), 12, "none", INK, 1.6))
    b.append(text(cx(pk), py(m[pk]) - 44, "ピーク", 15, INK, 700, "middle"))
    b.append(text(cx(n - 1) + 18, py(m[-1]) + 6, "男性", 17, TEAL_D, 700))
    b.append(text(cx(n - 1) + 18, py(f[-1]) + 6, "女性", 17, ACC, 700))
    # 右：まとめ
    rx = 950
    b.append(rect(rx, 110, 202, 470, CARD, LINE, 12))
    b.append(text(rx + 18, 144, "読みかた", 18, INK, 700))
    b.append(line(rx + 14, 176, rx + 42, 176, TEAL, 3) + circle(rx + 28, 176, 7, TEAL, "#fff", 2) + text(rx + 52, 182, "男性（kg）", 16, INK))
    b.append(line(rx + 14, 210, rx + 42, 210, ACC, 3, "9 5") + f'<rect x="{rx + 21}" y="203" width="14" height="14" fill="{ACC}" stroke="#fff" stroke-width="2"/>'
             + text(rx + 52, 216, "女性（kg）", 16, INK))
    b.append(line(rx + 16, 240, rx + 186, 240, LINE, 1.2))
    b.append(lines(rx + 18, 270, ["男性のピークは30代", f"（約{m[pk]}kg）"], 16, INK, 1.5, weight=700))
    b.append(lines(rx + 18, 336, ["女性は20〜40代で", f"約{max(f)}kg"], 16, INK, 1.5, weight=700))
    b.append(lines(rx + 18, 402, ["その後はゆるやかに", "下がり、70代で", f"男性 約{m[-1]}kg", f"女性 約{f[-1]}kg"], 16, INK2, 1.5))
    b.append(lines(rx + 18, 530, ["左右の平均か", "利き手の記録で比べる"], 14, MUTED, 1.45))
    return svg("".join(b), "握力の平均（年代別・男女別・目安）",
               "スポーツ庁「体力・運動能力調査」の結果をもとにした丸めた目安（kg）。")


FIGS = [
    dict(svg=fig1, alt="握力の平均を年代別・男女別に示した折れ線グラフ。男性は中学生約30kg、高校生約41kg、20代約46kg、30代約47kgでピーク、70代約35kg。女性は中学生約24kg、20〜40代約28kg、70代約22kg（スポーツ庁の調査をもとにした目安）。",
         caption="握力の平均（目安）。男性は30代の約47kg、女性は20〜40代の約28kgが最も高い。"),
]
