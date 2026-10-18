"""チケット当選確率シミュレーター（ticket-tousen）の図。
式はページの JS と同じ：1口の当選率 p = 1 ÷ 倍率、少なくとも1枚当たる確率 = 1 −（1 − p）^口数。"""
from fractions import Fraction
from figlib import *

ANCHOR = r'<div class="note"><strong>計算式</strong>.*?</div>\s*<p>.*?</p>\n'


def win(rate, n):
    """少なくとも1枚当たる確率（0〜1）。ページの JS：1-Math.pow(1-p,n)"""
    return 1 - (1 - 1 / rate) ** n


def need(rate, target):
    """少なくとも1枚当たる確率が target 以上になる最少の口数（分数で厳密に）"""
    p, n, t = Fraction(1, rate), 1, Fraction(target).limit_denominator(1000)
    while 1 - (1 - p) ** n < t:
        n += 1
    return n


def pct(v):
    return f"{v * 100:.1f}%"


def sup(x, y, base, s, size=18, fill=INK, weight=700):
    """右肩に小さい文字（べき乗）をつけたテキスト"""
    w = ' font-weight="700"' if weight >= 700 else ""
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}"{w}>{esc(base)}'
            f'<tspan dy="-9" font-size="{size * 0.78:.0f}">{esc(s)}</tspan></text>')


def fig1():
    b = []
    # 左：3ステップ
    x0, bw = 48, 520
    steps = [
        ("1", "1口の当選率 ＝ 1 ÷ 倍率", None, "例）倍率10倍 → 1 ÷ 10 ＝ 10%", pct(1 / 10)),
        ("2", "全部外れる確率 ＝（1 − 当選率）", "口数", "例）3口 → 0.9 × 0.9 × 0.9 ＝ 0.729", pct(0.9 ** 3)),
        ("3", "少なくとも1枚当たる ＝ 1 − 全部外れる確率", None, "例）1 − 0.729 ＝ 0.271", pct(win(10, 3))),
    ]
    y = 104
    for no, head, sp, ex, val in steps:
        last = no == "3"
        b.append(rect(x0, y, bw, 116, ACC_L if last else CARD, ACC if last else LINE, 10, 1.6 if last else 1.2))
        b.append(badge(x0 + 30, y + 34, no, ACC if last else TEAL, "#fff", 17))
        if sp:
            b.append(sup(x0 + 58, y + 41, head, sp, 19))
        else:
            b.append(text(x0 + 58, y + 41, head, 19, INK, 700))
        b.append(text(x0 + 58, y + 90, ex, 17, INK2))
        b.append(text(x0 + bw - 22, y + 92, val, 30 if last else 24, ACC if last else TEAL, 700, "end"))
        if not last:
            b.append(arrow(x0 + 30, y + 118, x0 + 30, y + 138, "muted", 2))
        y += 140
    b.append(text(x0, 552, "口数を10倍にしても、確率は10倍にならない", 17, INK, 700))
    b.append(text(x0, 584, f"倍率10倍で 1口＝{pct(win(10, 1))} → 10口＝{pct(win(10, 10))}（100%にはならない）", 16, INK2))

    # 右：口数と当選確率のグラフ
    gx, gy, gw, gh, nmax = 640, 540, 430, 360, 20
    px = lambda n: gx + n / nmax * gw
    py = lambda v: gy - v * gh
    b.append(text(610, 122, "口数と当選確率（倍率別）", 19, INK, 700))
    b.append(axes(gx, gy, gw, gh, "口数", "当選確率",
                  [(n / nmax * gw, f"{n}口" if n == 1 else str(n)) for n in (1, 5, 10, 15, 20)],
                  [(v / 100 * gh, f"{v}%") for v in (0, 25, 50, 75, 100)], 14))
    b.append(line(gx, py(0.5), gx + gw, py(0.5), ACC, 1.4, "6 5"))
    curves = [(5, TEAL, None), (10, ACC, None), (20, GOLD, "8 5"), (50, PURPLE, "3 4")]
    for rate, c, dash in curves:
        pts = [(px(n), py(win(rate, n))) for n in range(1, nmax + 1)]
        b.append(poly(pts, c, 3, dash=dash))
        b.append("".join(circle(x, yy, 3, c, c, 0) for x, yy in pts))
        n50 = need(rate, 0.5)
        if n50 <= nmax:
            b.append(circle(px(n50), py(win(rate, n50)), 7, CARD, c, 2.6))
        b.append(text(px(nmax) + 12, py(win(rate, nmax)) + 6, f"{rate}倍", 17, c, 700))
    b.append(text(610, 600, "◯＝50%に届く口数：" + "　".join(f"{r}倍→{need(r, 0.5)}口" for r in (5, 10, 20, 50)), 15, INK2))
    return svg("".join(b), "何口で当たる？ チケット当選確率のしくみ",
               "1口ごとに同じ確率で、別々に抽選されると考えた目安。名義の貸し借りや重複申し込みは公演のルールを確認。")


def fig2():
    b = []
    rates = [2, 3, 5, 10, 20, 30, 50, 100]
    rows = [[f"{r}倍", pct(1 / r), f"{need(r, 0.5)}口", f"{need(r, 0.8)}口", f"{need(r, 0.9)}口", pct(win(r, 10))] for r in rates]
    b.append(text(60, 128, "少なくとも1枚当たる確率が 50%・80%・90% に届く口数", 19, INK, 700))
    cols = ["倍率", "1口の当選率", "50%以上", "80%以上", "90%以上", "10口申し込むと"]
    cw = [150, 190, 170, 170, 170, 230]
    b.append(table(60, 142, cols, rows, cw, 47, 18))
    # 目標の列を色で示す（見出しの下に細い帯）
    xs = 60 + cw[0] + cw[1]
    b.append(f'<rect x="{xs}" y="185" width="{cw[2] + cw[3] + cw[4]}" height="4" fill="{ACC}"/>')
    b.append(text(60, 604, "目標の確率に届く口数 ＝ 1 −（1 − 1 ÷ 倍率）の口数乗 が、その確率以上になる いちばん少ない口数", 16, INK2))
    return svg("".join(b), "当選確率50%・80%・90%に必要な口数（早見表）",
               "倍率が2倍になると、必要な口数もほぼ2倍。1口ごとに同じ確率で抽選されると考えた目安。")


FIGS = [
    dict(svg=fig1,
         alt="チケット当選確率の計算のしくみの図。1口の当選率＝1÷倍率、全部外れる確率＝（1−当選率）の口数乗、少なくとも1枚当たる確率＝1−全部外れる確率（倍率10倍・3口で27.1%）の3ステップと、倍率5倍・10倍・20倍・50倍で口数1〜20口のときの当選確率のグラフ。",
         caption="当選確率の計算のしくみ。少なくとも1枚当たる確率＝1 −（1 − 1÷倍率）^口数。口数を増やしても確率は比例しては増えない。"),
    dict(svg=fig2,
         alt="当落シミュレーターの早見表。倍率2倍・3倍・5倍・10倍・20倍・30倍・50倍・100倍ごとに、1口の当選率と、少なくとも1枚当たる確率が50%・80%・90%に届く口数、10口申し込んだときの当選確率をまとめた表。",
         caption="何口申し込めば当たりやすいかの早見表。倍率10倍なら7口で50%、16口で80%、22口で90%を超える。"),
]
