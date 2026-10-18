"""今週末、晴れる？（shuumatsu-hare）の図。降水確率の意味／おでかけ日和度の決め方。
言い方の正：気象庁「降水確率予報って何ですか？」「天気予報（予報用語）」
（30%の予報を100回発表したら約30回は1mm以上の雨や雪、府県予報は6時間ごと・週間予報は1日ごと、10%きざみ（間は四捨五入）、確率が高くても雨量が多いとは限らない、
発表区域内のどこでも同じ確率）。ページの数値の決め方：Open-Meteo の precipitation_probability_max（1時間に0.1mm以上の確率の、その日の最大）。
おでかけ日和度：ページの JS  round((100 − 降水確率) × 係数)、係数＝天気コード≦3（快晴〜くもり）1／≦48（霧）0.8／それ以外（雨・雪・雷雨など）0.45、
判定 75以上 おでかけ日和！／50以上 まずまず／30以上 傘と相談／それ未満 インドア推奨…。"""
import math
from figlib import *

RAINY = [2, 7, 11, 16, 23, 25, 31, 38, 40, 44, 49, 52, 57, 60, 64, 66, 71, 73, 78, 81, 83, 86, 90, 92, 95, 97, 13, 34, 55, 68]  # 30個（ばらばらに並べる）


def drop(cx, cy, s, fill):
    return (f'<path d="M{cx:.1f},{cy - s:.1f} C{cx + s * 0.15:.1f},{cy - s * 0.55:.1f} {cx + s * 0.75:.1f},{cy - s * 0.05:.1f} {cx + s * 0.75:.1f},{cy + s * 0.35:.1f} '
            f'A{s * 0.75:.1f},{s * 0.75:.1f} 0 0 1 {cx - s * 0.75:.1f},{cy + s * 0.35:.1f} C{cx - s * 0.75:.1f},{cy - s * 0.05:.1f} {cx - s * 0.15:.1f},{cy - s * 0.55:.1f} {cx:.1f},{cy - s:.1f}Z" fill="{fill}"/>')


STYLE = {"sun": (TEAL, None), "fog": (GOLD, "10 6"), "rain": (ACC, "3 5")}


def outing(p, code_class):
    k = {"sun": 1, "fog": 0.8, "rain": 0.45}[code_class]
    return max(0, math.floor((100 - p) * k + 0.5))


def fig1():
    assert len(set(RAINY)) == 30 and all(0 <= i < 100 for i in RAINY)
    b = [text(48, 126, "降水確率30%の予報が100回出たら…", 19, INK, 700)]
    x0, y0, c = 64, 146, 38
    for i in range(100):
        cx, cy = x0 + (i % 10) * c + c / 2, y0 + (i // 10) * c + c / 2
        if i in RAINY:
            b.append(drop(cx, cy + 2, 15, TEAL))
        else:
            b.append(circle(cx, cy, 6, "#e3ded2", "none", 0))
    b.append(drop(x0 + 14, y0 + 10 * c + 26, 12, TEAL))
    b.append(text(x0 + 32, y0 + 10 * c + 32, "＝ 1mm以上の雨か雪が降った（約30回）", 16, INK, 700))
    b.append(circle(x0 + 14, y0 + 10 * c + 56, 6, "#e3ded2", "none", 0))
    b.append(text(x0 + 32, y0 + 10 * c + 62, "＝ 降らなかった（1mm未満の小雨をふくむ）", 16, INK))
    # 右：勘ちがいしやすい点
    X = 520
    b.append(text(X, 126, "降水確率は「降るかどうか」の確率", 19, TEAL, 700))
    rows = [("×", "雨の量や強さ", ["確率が高くても小雨のことがある。", "低くても、短い時間に強く降る雨（夕立）もある"]),
            ("×", "その時間のうち雨が降る長さ", ["30%でも「時間の3割が雨」ではない"]),
            ("×", "地域のうち雨が降る広さ", ["発表した区域の中なら、どこでも同じ確率"]),
            ("○", "10%きざみ・四捨五入", ["0%は「5%未満」。1mm未満の雨は数えないので、", "0%でも小雨が降ることはある"])]
    y = 150
    for mk, head, body in rows:
        h = 34 + 24 * len(body)
        col = ACC if mk == "×" else TEAL
        b.append(rect(X, y, 632, h, CARD, LINE, 8))
        b.append(badge(X + 24, y + 22, mk, col, "#fff", 18))
        b.append(text(X + 48, y + 28, ("ではない：" if mk == "×" else "") + head, 17, col, 700))
        b.append(lines(X + 48, y + 54, body, 15.5, INK, 1.5))
        y += h + 10
    b.append(lines(X, y + 20, ["このページの降水確率は気象モデル（Open-Meteo）の、", "1時間ごとの確率（0.1mm以上）のうちその日いちばん高い値。",
                                "気象庁の予報と数字がちがうことがある。"], 14.5, INK2, 1.5))
    return svg("".join(b), "降水確率の意味（気象庁の定義）",
               "気象庁は、決まった時間に1mm以上の雨か雪が降る確率を10%きざみで発表（今日・明日は6時間ごと、週間予報は1日ごと）。")


def fig2():
    b = []
    X0, Y0, Wd, Hd = 100, 560, 560, 400
    px = lambda p: X0 + p / 100 * Wd
    py = lambda s: Y0 - s / 100 * Hd
    bands = [(75, 100, "おでかけ日和！", "#dfeee6"), (50, 75, "まずまず", "#eef3f6"), (30, 50, "傘と相談", "#f6eedc"), (0, 30, "インドア推奨…", "#f7ebe6")]
    for s0, s1, lab, col in bands:
        b.append(f'<rect x="{X0}" y="{py(s1):.1f}" width="{Wd}" height="{py(s0) - py(s1):.1f}" fill="{col}"/>')
        b.append(text(X0 + Wd - 10, py(s1) + 24, lab, 15, INK2, 700, "end"))
    b.append(axes(X0, Y0, Wd, Hd, "", "", [(px(p) - X0, f"{p}%") for p in range(0, 101, 20)],
                  [(Hd * s / 100, str(s)) for s in (0, 30, 50, 75, 100)], 14))
    b.append(text(X0 + Wd / 2, Y0 + 50, "降水確率", 15, INK, 700, "middle"))
    b.append(text(X0 - 10, Y0 - Hd - 26, "おでかけ日和度（点）", 15, INK, 700))
    for cls in STYLE:
        col, dash = STYLE[cls]
        kk = {"sun": 1, "fog": 0.8, "rain": 0.45}[cls]
        b.append(poly([(px(0), py(100 * kk)), (px(100), py(0))], col, 3.4, dash=dash))   # 四捨五入する前の直線
    b.append(text(px(1.5), py(100) - 8, "晴れ・くもり ×1", 15, TEAL, 700))
    b.append(text(px(1.5), py(80) - 10, "霧 ×0.8", 15, GOLD, 700))
    b.append(text(px(1.5), py(45) - 10, "雨・雪など ×0.45", 15, ACC, 700))
    # 右：式と例
    X = 720
    b.append(text(X, 128, "おでかけ日和度の決め方", 19, INK, 700))
    b.append(rect(X, 144, 432, 64, TEAL_L, "none", 8, 0))
    b.append(text(X + 216, 184, "（100 − 降水確率）× 天気の係数", 19, TEAL_D, 700, "middle"))
    b.append(table(X, 222, ["", "その日の天気", "係数"],
                   [["", "快晴・晴れ・くもり", "×1"], ["", "霧", "×0.8"], ["", "霧雨・雨・雪・雷雨など", "×0.45"]], [70, 262, 100], 42, 16))
    for i, cls in enumerate(("sun", "fog", "rain")):
        col, dash = STYLE[cls]
        b.append(line(X + 14, 222 + 42 * (i + 1) + 21, X + 56, 222 + 42 * (i + 1) + 21, col, 3.4, dash))
    b.append(text(X, 424, "例", 16, INK, 700))
    ex = [("くもり・降水確率20%", outing(20, "sun")), ("雨・降水確率60%", outing(60, "rain"))]
    for i, (t, sc) in enumerate(ex):
        lab = "おでかけ日和！" if sc >= 75 else "まずまず" if sc >= 50 else "傘と相談" if sc >= 30 else "インドア推奨…"
        b.append(text(X, 452 + i * 28, f"{t} → {sc}点（{lab}）", 16, INK))
    b.append(lines(X, 530, ["土曜と日曜のうち、点の高いほうが", "今週末の点数。高いほうの日を", "「おすすめ」に表示する。"], 16, INK, 1.5))
    return svg("".join(b), "おでかけ日和度の決め方（このページの判定）",
               "雨・雪の予報の日は、降水確率が0%でも45点まで。週の前半に見た週末予報は、前日にもう一度確かめる。")


FIGS = [
    dict(svg=fig1, alt="降水確率の意味を示す図。降水確率30%の予報が100回出たら、そのうち約30回は1mm以上の雨か雪が降るという意味を100個の印で表し、降水確率は雨の量や強さ・降る時間の長さ・降る範囲の広さではないこと、10%きざみで0%は5%未満であることをまとめている。",
         caption="降水確率30%は「同じ予報が100回出たら約30回は1mm以上の雨か雪が降る」という意味。雨の量や強さではない。"),
    dict(svg=fig2, alt="今週末のおでかけ日和度の決め方。おでかけ日和度＝（100−降水確率）×天気の係数（快晴・晴れ・くもり×1、霧×0.8、雨・雪・雷雨など×0.45）で、降水確率ごとの点数と判定（75点以上おでかけ日和・50点以上まずまず・30点以上傘と相談・それ未満インドア推奨）をグラフで示す。",
         caption="おでかけ日和度の決め方。降水確率が低く、天気が晴れ〜くもりの日ほど点が高い。"),
]
