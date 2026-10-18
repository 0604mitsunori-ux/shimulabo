"""犬・猫の年齢 人間換算（pet-age）の図。換算式はページの JS と同じ：
1歳まで 15×年齢、2歳まで 15＋(年齢−1)×9、それ以降 24＋(年齢−2)×4（小〜中型犬・猫）／×7（大型犬）。
ライフステージの区切りも JS と同じ（13歳未満 子ども／20未満 青年／45未満 働き盛り／60未満 中年／75未満 シニア／それ以上 長寿）。"""
from figlib import *

ANCHOR = r'<h2>換算の考え方</h2>\s*<div class="note">.*?</div>\s*<p>.*?</p>\n'
STAGES = [(0, 13, "子ども"), (13, 20, "青年"), (20, 45, "働き盛り"), (45, 60, "中年"), (60, 75, "シニア"), (75, 125, "長寿")]


def human(y, large=False):
    if y <= 1:
        return 15 * y
    if y <= 2:
        return 15 + (y - 1) * 9
    return 24 + (y - 2) * (7 if large else 4)


def fig1():
    b = []
    x0, y0, w, h = 110, 568, 700, 440
    XM, YM = 20, 120
    px = lambda v: x0 + v * w / XM
    py = lambda v: y0 - v * h / YM
    # ライフステージの帯
    for i, (a, e, nm) in enumerate(STAGES):
        e = min(e, YM)
        b.append(f'<rect x="{x0}" y="{py(e):.1f}" width="{w}" height="{py(a) - py(e):.1f}" fill="{[GOLD_L, "#f3f1ea"][i % 2]}"/>')
        b.append(text(x0 + w + 10, (py(a) + py(e)) / 2 + 5, nm, 14, INK2, 700))
    b.append(text(x0 + w + 10, py(YM) - 10, "ライフステージ", 13, MUTED))
    b.append(axes(x0, y0, w, h, "", "人間の年齢（歳）",
                  [(v * w / XM, f"{v}") for v in range(0, 21, 2)], [(v * h / YM, f"{v}") for v in range(0, 121, 20)], 14))
    b.append(text(x0 + w / 2, y0 + 48, "ペットの年齢（歳）", 15, INK, 700, "middle"))
    sm = [(v / 4, human(v / 4)) for v in range(0, 81)]
    lg = [(v / 4, human(v / 4, True)) for v in range(0, 61)]
    b.append(poly([(px(a), py(c)) for a, c in lg], ACC, 3.2, dash="9 5"))
    b.append(poly([(px(a), py(c)) for a, c in sm], TEAL, 3.2))
    for yv in (5, 10, 15, 20):
        hv = human(yv)
        lx, anc = (px(yv) - 8, "end") if yv == 20 else (px(yv) + 4, "middle")
        b.append(circle(px(yv), py(hv), 5.5, TEAL, "#fff", 1.6) + text(lx, py(hv) + (40 if yv == 20 else 24), f"{hv}歳", 15, TEAL_D, 700, anc))
    for yv in (5, 10, 15):
        hv = human(yv, True)
        b.append(f'<rect x="{px(yv) - 5.5:.1f}" y="{py(hv) - 5.5:.1f}" width="11" height="11" fill="{ACC}" stroke="#fff" stroke-width="1.6"/>'
                 + text(px(yv) - 10, py(hv) - 8, f"{hv}歳", 15, ACC, 700, "end"))
    for yv in (1, 2):
        hv = human(yv)
        b.append(circle(px(yv), py(hv), 5.5, INK, "#fff", 1.6) + text(px(yv) + 10, py(hv) + 22, f"{yv}歳→{hv}歳", 15, INK, 700))
    b.append(text(px(15) + 12, py(human(15, True)) + 4, "大型犬", 17, ACC, 700))
    b.append(text(px(20) - 6, py(human(20)) - 14, "小〜中型犬・猫", 17, TEAL_D, 700, "end"))
    # 右：ルール
    rx = 930
    b.append(rect(rx, 110, 222, 470, CARD, LINE, 12))
    b.append(text(rx + 18, 144, "換算のルール", 18, INK, 700))
    b.append(badge(rx + 30, 186, "1", INK, "#fff", 15) + lines(rx + 52, 182, ["最初の1年で", "約15歳"], 16, INK, 1.4))
    b.append(badge(rx + 30, 262, "2", INK, "#fff", 15) + lines(rx + 52, 258, ["2年で", "約24歳"], 16, INK, 1.4))
    b.append(badge(rx + 30, 338, "3", INK, "#fff", 15) + lines(rx + 52, 334, ["そのあとは", "1年ごとに"], 16, INK, 1.4))
    b.append(line(rx + 30, 392, rx + 62, 392, TEAL, 3.2) + text(rx + 70, 397, "小〜中型犬・猫", 15, TEAL_D, 700))
    b.append(text(rx + 70, 424, "＋約4歳", 20, TEAL_D, 700))
    b.append(line(rx + 30, 466, rx + 62, 466, ACC, 3.2, "9 5") + text(rx + 70, 471, "大型犬", 15, ACC, 700))
    b.append(text(rx + 70, 498, "＋約7歳", 20, ACC, 700))
    b.append(lines(rx + 18, 540, ["体格・犬種で差がある", "一般的な目安"], 14, MUTED, 1.4))
    return svg("".join(b), "犬・猫の年齢を人間に換算するしくみ（目安）",
               "背景の帯は人間の年齢でのライフステージ（ツールの判定と同じ区切り）。大型犬ほど早く歳をとる。")


def fig2():
    b = []
    cw = [120, 220, 170]
    heads = ["ペットの年齢", "小〜中型犬・猫", "大型犬"]
    for k, (xs, ages) in enumerate([(60, range(1, 11)), (630, range(11, 21))]):
        rows = []
        for a in ages:
            rows.append([f"{a}歳", f"{human(a)}歳", f"{human(a, True)}歳" if a <= 15 else "—"])
        b.append(table(xs, 104, heads, rows, cw, 42, 17))
    b.append(text(60, 604, "人間の年齢に換算した目安。大型犬の16歳以上は省略（一般に小型犬より寿命が短め）。", 15.5, INK2))
    return svg("".join(b), "犬・猫の年齢 早見表（人間でいうと何歳？）",
               "最初の2年で約24歳、その後は小〜中型犬・猫が1年に約4歳、大型犬が約7歳ずつ（一般的な目安）。")


FIGS = [
    dict(svg=fig1, alt="犬・猫の年齢を人間の年齢に換算するグラフ。最初の1年で約15歳、2年で約24歳になり、その後は小型・中型犬と猫が1年に約4歳、大型犬が約7歳ずつ年をとる。犬・猫の10歳は人間の約56歳（大型犬は約80歳）。子ども・青年・働き盛り・中年・シニア・長寿のライフステージの帯つき。",
         caption="犬・猫の年齢換算のしくみ（目安）。2歳で約24歳、その後は1年に約4歳（大型犬は約7歳）。"),
    dict(svg=fig2, alt="犬・猫の年齢の人間換算 早見表。1歳から20歳まで、小型・中型犬と猫、大型犬それぞれが人間でいうと何歳かの一覧（例：犬・猫の5歳は約36歳、10歳は約56歳、15歳は約76歳。大型犬の10歳は約80歳）。",
         caption="犬・猫の年齢 早見表。小〜中型犬・猫の10歳は人間の約56歳、大型犬は約80歳。"),
]
