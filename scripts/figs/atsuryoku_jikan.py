"""圧力鍋の時短（atsuryoku-jikan）の図。加圧時間＝通常の時間×係数（ページの JS：肉の煮込み0.33・豆/玄米0.25・カレー/シチュー0.4・魚の骨まで0.3）。
水の沸点は IAPWS-IF97 の飽和温度の式（Region 4）で計算する。"""
import math
from figlib import *

ANCHOR = r"光熱費の節約にもつながります。</p>\n"
FOODS = [("肉の煮込み", 0.33), ("豆・玄米", 0.25), ("カレー・シチュー", 0.4), ("魚の骨まで", 0.3)]   # ページの JS と同じ
ATM = 0.101325   # MPa
_N = [0, 0.11670521452767e4, -0.72421316703206e6, -0.17073846940092e2, 0.12020824702470e5, -0.32325550322333e7,
      0.14915108613530e2, -0.48232657361591e4, 0.40511340542057e6, -0.23855557567849, 0.65017534844798e3]


def tsat(atm):
    """水の沸点（℃）。atm＝絶対圧（気圧）"""
    b = (atm * ATM) ** 0.25; n = _N
    E = b * b + n[3] * b + n[6]; F = n[1] * b * b + n[4] * b + n[7]; G = n[2] * b * b + n[5] * b + n[8]
    D = 2 * G / (-F - math.sqrt(F * F - 4 * E * G))
    return (n[10] + D - math.sqrt((n[10] + D) ** 2 - 4 * (n[9] + n[10] * D))) / 2 - 273.15


def jr(x):
    return math.floor(x + 0.5)       # JS の Math.round


def pot(cx, by, sealed):
    """鍋の断面。by＝鍋底の y"""
    w, h = 200, 150; x0, top = cx - w / 2, by - h
    out = [f'<rect x="{x0}" y="{top + 40}" width="{w}" height="{h - 40}" fill="{TEAL_L}"/>']          # 水
    for i in range(5):
        bx = x0 + 30 + i * 36
        out.append(circle(bx, top + 70 + (i % 2) * 22, 5, CARD, TEAL, 1.4))                              # 泡
    out.append(f'<path d="M{x0},{top} V{by} H{x0 + w} V{top}" fill="none" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
    out.append(line(x0 - 26, top + 30, x0, top + 30, INK, 6) + line(x0 + w, top + 30, x0 + w + 26, top + 30, INK, 6))   # 取っ手
    if sealed:
        out.append(rect(x0 - 10, top - 16, w + 20, 18, INK2, INK2, 4))                                        # ふた（密閉）
        out.append(rect(x0 - 14, top - 20, 16, 34, INK, INK, 3) + rect(x0 + w - 2, top - 20, 16, 34, INK, INK, 3))   # 留め金
        out.append(rect(cx - 8, top - 34, 16, 18, INK, INK, 3))                                               # おもり（圧力調整）
        for i in range(8):                                                                                   # 中にこもる蒸気
            out.append(circle(x0 + 22 + i * 22, top + 18 + (i % 2) * 10, 3.5, MUTED, MUTED, 0))
    else:
        out.append(f'<path d="M{x0 + 6},{top - 22} Q{cx},{top - 40} {x0 + w - 6},{top - 22}" fill="none" stroke="{INK2}" stroke-width="5"/>')   # ふた（すき間あり）
        for sx in (x0 + 4, x0 + w - 4):                                                                      # すき間から逃げる蒸気
            d = -1 if sx < cx else 1
            out.append(f'<path d="M{sx},{top - 14} q{d * 14},-14 {d * 6},-30 q{d * -8},-14 {d * 6},-30" fill="none" stroke="{MUTED}" stroke-width="2.4" stroke-linecap="round"/>')
    return "".join(out)


def fig1():
    b = []
    t1, t2 = tsat(1), tsat(2)
    # 左：2つの鍋
    for cx, sealed, name, p, t, sub in [(175, False, "ふつうの鍋", "鍋の中＝1気圧", f"沸点 {t1:.0f}℃", ["湯気がすき間から逃げる。", "100℃より熱くならない。"]),
                                        (455, True, "圧力鍋", "鍋の中＝約2気圧", f"沸点 約{jr(t2 / 5) * 5:.0f}℃", ["ふたを密閉して蒸気をとじこめ、", "圧力を上げる。"])]:
        b.append(text(cx, 130, name, 22, INK, 700, "middle"))
        b.append(pot(cx, 360, sealed))
        b.append(text(cx, 396, p, 17, INK2, anchor="middle"))
        b.append(text(cx, 430, t, 26, ACC if sealed else TEAL_D, 700, "middle"))
        b.append(lines(cx - 130, 466, sub, 15, INK2, 1.5))
    b.append(arrow(292, 290, 340, 290, "ink", 2.6))
    # 右：水の沸点と気圧のグラフ
    gx, gy, gw, gh = 690, 470, 400, 320
    px = lambda a: gx + (a - 0.5) / 2.0 * gw          # 0.5〜2.5気圧
    py = lambda t: gy - (t - 80) / 50 * gh            # 80〜130℃
    b.append(text(gx - 50, 124, "水の沸点と圧力", 18, INK, 700))
    b.append(axes(gx, gy, gw, gh, "気圧", "",
                  [(px(a) - gx, f"{a:g}") for a in (0.5, 1, 1.5, 2, 2.5)]))
    for t in range(80, 131, 10):
        y = py(t)
        b.append(line(gx - 6, y, gx, y, INK, 1.4) + text(gx - 10, y + 5, f"{t}℃", 14, INK2, anchor="end"))
        if t > 80: b.append(line(gx, y, gx + gw, y, LINE, 1))
    pts = [(px(a), py(tsat(a))) for a in [0.5 + i * 0.05 for i in range(41)]]
    b.append(poly(pts, TEAL, 3.2))
    for a, t, lab, col in [(1, t1, "ふつうの鍋 100℃", TEAL_D), (2, t2, f"圧力鍋 約{jr(t2 / 5) * 5:.0f}℃", ACC)]:
        x, y = px(a), py(t)
        b.append(line(x, gy, x, y, col, 1.6, "5 5") + line(gx, y, x, y, col, 1.6, "5 5"))
        b.append(circle(x, y, 7, col, "#fff", 2))
        b.append(text(x + 14, y + 26, lab, 16, col, 700) if a == 1 else text(x - 14, y - 18, lab, 16, col, 700, "end"))
    b.append(text(gx + gw / 2, gy + 52, "圧力が高いほど、水は高い温度でふっとうする", 15, INK2, anchor="middle"))
    # 下：結論
    b.append(rect(48, 548, 1104, 64, GOLD_L, "#e8d9b5", 10))
    b.append(text(72, 588, "温度が高いほど食材に早く火が通る　→　煮込み時間は約1/3〜1/4（加圧時間の目安）", 19, INK, 700))
    return svg("".join(b), "圧力鍋で早く煮えるしくみ（沸点と時間の関係）",
               "約2気圧・約120℃は高圧の目安で、製品によってちがう（大きさは実際とちがう模式図）。")


def fig2():
    b = []
    mins = [30, 60, 90, 120]
    cols = ["料理", "通常の時間を1としたとき", "時短率"] + [f"通常{m}分" for m in mins]
    cw = [180, 300, 110, 122, 122, 122, 122]
    rows = []
    for name, k in FOODS:
        rows.append([name, "", f"{jr((1 - k) * 100)}%"] + [f"約{jr(m * k)}分" for m in mins])
    x0, y0, rh = 60, 120, 76
    b.append(table(x0, y0, cols, rows, cw, rh, 18))
    bx, bw = x0 + cw[0] + 20, cw[1] - 40
    for i, (name, k) in enumerate(FOODS):
        y = y0 + rh * (i + 1) + 22
        b.append(rect(bx, y, bw, 30, "#e9e5da", "#e9e5da", 4))
        b.append(rect(bx, y, bw * k, 30, ACC, ACC, 4))
        b.append(text(bx + bw * k + 10, y + 22, f"×{k:g}", 16, ACC, 700))
    b.append(text(bx + bw, y0 + rh * 5 + 26, "灰色＝通常の時間、赤＝加圧時間", 14, MUTED, anchor="end"))
    b.append(rect(48, 548, 1104, 64, CARD, LINE, 10))
    b.append(lines(72, 574, ["表の時間は「加圧時間」。このほかに、加圧までの加熱と、火を止めたあとの自然放置（余熱）の時間がかかる。",
                             "仕上がりはレシピや製品の説明書の指示に合わせる。"], 16, INK2, 1.55))
    return svg("".join(b), "圧力鍋の加圧時間の早見表（目安）",
               "加圧時間＝通常の調理時間×係数（シミュと同じ）。一般的な目安で、食材の量や大きさで変わる。")


FIGS = [
    dict(svg=fig1, alt="圧力鍋の時短のしくみの図。ふつうの鍋は1気圧で水が100℃でふっとうするのに対し、ふたを密閉した圧力鍋は約2気圧になり沸点が約120℃に上がることを、水の沸点と圧力のグラフとともに示す。温度が高いので煮込み時間は約1/3〜1/4になる。",
         caption="圧力鍋で早く煮えるしくみ。圧力が上がると水の沸点が約120℃に上がり、早く火が通る。"),
    dict(svg=fig2, alt="圧力鍋の加圧時間の早見表。肉の煮込み・豆や玄米・カレーやシチュー・魚の骨まで、の4種類について、通常30分・60分・90分・120分の料理を圧力鍋にしたときの加圧時間の目安と時短率。",
         caption="圧力鍋の加圧時間の早見表（目安）。加圧のあとの自然放置（余熱）の時間は別にかかる。"),
]
