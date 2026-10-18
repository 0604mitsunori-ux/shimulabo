"""ml⇔グラム換算（ml-gram）の図。比重はページの表（食材別の比重）と同じ。g＝ml×比重、ml＝g÷比重。
小さじ5ml・大さじ15ml・1カップ200ml・1合180ml（計量の一般的な値）。"""
import math
from decimal import Decimal, ROUND_HALF_UP
from figlib import *

ANCHOR = r"<tr><td>小麦粉</td><td>0\.55g</td></tr></table>\n"
# ページの表の6食材（JS にある砂糖0.85はページの表にないので入れない）
FOODS = [("水", "1"), ("牛乳", "1.03"), ("サラダ油", "0.92"), ("醤油", "1.15"), ("はちみつ", "1.4"), ("小麦粉", "0.55")]


def rnd(x, nd=0):
    """10進で四捨五入（浮動小数の誤差を避ける）"""
    q = Decimal(1).scaleb(-nd)
    return Decimal(x).quantize(q, ROUND_HALF_UP)


def grams(ml, d):
    return Decimal(ml) * Decimal(d)


def fig1():
    b = []
    order = sorted(FOODS, key=lambda f: -float(f[1]))
    b.append(rect(48, 100, 1104, 50, TEAL_L, TEAL_L, 10))
    b.append(text(600, 133, "g（重さ）＝ ml（かさ）× 比重　　／　　ml ＝ g ÷ 比重", 20, TEAL_D, 700, "middle"))
    x0, sc = 220, 340                                  # 1g/ml＝340px
    top, rh = 178, 60
    for v in (0, 0.5, 1.0, 1.5):
        x = x0 + v * sc
        b.append(line(x, top - 8, x, top + rh * 6 - 8, LINE, 1))
        b.append(text(x, top + rh * 6 + 16, f"{v:g}g", 15, INK2, anchor="middle"))
    b.append(text(x0 + 1.5 * sc + 26, top + rh * 6 + 16, "（1mlあたり）", 14, MUTED))
    b.append(text(1040, top - 16, "100gは何ml？", 17, INK, 700, "middle"))
    for i, (nm, d) in enumerate(order):
        y = top + i * rh; dv = float(d)
        col = GOLD if dv < 1 else (INK2 if dv == 1 else TEAL)
        b.append(text(x0 - 18, y + 30, nm, 20, INK, 700, "end"))
        b.append(rect(x0, y + 4, dv * sc, 38, col, col, 4))
        lx = x0 + dv * sc + 12
        if lx < x0 + sc + 12 and lx + 140 > x0 + sc - 6:    # 水の線（1g）にかかるときは線の右へ
            lx = x0 + sc + 12
        b.append(text(lx, y + 32, f"1ml＝{d}g", 20, col, 700))
        ml100 = Decimal(100) / Decimal(d)
        s = f"{rnd(ml100)}ml" if ml100 == ml100.to_integral() else f"約{rnd(ml100)}ml"
        b.append(text(1040, y + 32, s, 20, INK, anchor="middle"))
    xw = x0 + 1.0 * sc
    b.append(line(xw, top - 8, xw, top + rh * 6 - 8, ACC, 2, "6 5"))
    b.append(text(xw - 10, top + rh * 6 + 40, "← 水より軽い", 15, GOLD, 700, "end"))
    b.append(text(xw + 10, top + rh * 6 + 40, "水より重い →", 15, TEAL_D, 700))
    return svg("".join(b), "1mlは何g？ 食材ごとの重さのちがい（比重）",
               "水は1ml＝1g。粉ものは、ふるい方や詰め方で同じかさでも重さが1〜2割変わる（目安）。")


def fig2():
    b = []
    cols_ml = [(5, "小さじ1", "5ml"), (15, "大さじ1", "15ml"), (100, "", "100ml"), (180, "1合", "180ml"), (200, "1カップ", "200ml"), (500, "", "500ml")]
    rows = []
    for nm, d in FOODS:
        r = [nm]
        for ml, _, _ in cols_ml:
            g = grams(ml, d)
            if ml < 100:                                   # 小さじ・大さじは整数に丸めた目安
                r.append(f"{rnd(g)}g" if g == g.to_integral() else f"約{rnd(g)}g")
            else:                                          # ページの早見表と同じ（整数に四捨五入）
                r.append(f"{rnd(g)}g")
        rows.append(r)
    cw = [170, 150, 150, 150, 150, 160, 150]
    x0, y0, rh = 60, 112, 62
    b.append(table(x0, y0, [""] * 7, rows, cw, rh, 20))
    cx = x0 + cw[0]
    b.append(text(x0 + cw[0] / 2, y0 + 39, "食材", 18, INK, 700, "middle"))
    for (ml, a, u), w in zip(cols_ml, cw[1:]):
        if a:
            b.append(text(cx + w / 2, y0 + 27, a, 18, INK, 700, "middle") + text(cx + w / 2, y0 + 50, f"（{u}）", 15, INK2, anchor="middle"))
        else:
            b.append(text(cx + w / 2, y0 + 39, u, 18, INK, 700, "middle"))
        cx += w
    b.append(lines(60, 576, ["重さ＝ml×比重（水1・牛乳1.03・サラダ油0.92・醤油1.15・はちみつ1.4・小麦粉0.55）で計算。",
                             "小さじ・大さじは1g単位に丸めた目安。お菓子づくりなど正確さが必要なときは、はかりで量る。"], 16, INK2, 1.55))
    return svg("".join(b), "小さじ・大さじ・カップは何g？（ml→g早見表）",
               "小さじ1＝5ml、大さじ1＝15ml、1カップ＝200ml、米1合＝180ml。")


FIGS = [
    dict(svg=fig1, alt="1mlは何gかを食材ごとに比べた棒グラフ。水1g、牛乳1.03g、サラダ油0.92g、醤油1.15g、はちみつ1.4g、小麦粉0.55gで、水より重いもの・軽いものと、100gが約何mlになるかを示す。",
         caption="1mlは何g？ 水は1ml＝1gだが、はちみつは1.4g、油は0.92g、小麦粉は0.55gと食材で変わる。"),
    dict(svg=fig2, alt="水・牛乳・サラダ油・醤油・はちみつ・小麦粉について、小さじ1（5ml）・大さじ1（15ml）・100ml・180ml（1合）・200ml（1カップ）・500mlが何グラムになるかの早見表。",
         caption="ml→gの早見表。小さじ・大さじ・1カップ（200ml）が何グラムかがひと目でわかる。"),
]
