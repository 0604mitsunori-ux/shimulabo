"""高速 vs 下道（kousoku-shita）の図。値はページの JS と同じ式：所要時間＝距離÷平均速度、短縮時間＝下道−高速、時短1時間あたりの費用＝高速料金÷短縮時間"""
import math
from figlib import *

ANCHOR = r"近場・のんびりなら下道と使い分けを。</p>\n"
DIST, TOLL, VH, VL = 300, 6000, 80, 35          # ページの初期値


def jr(x):
    return math.floor(x + 0.5)                  # JS の Math.round


def hm(h):
    """JS の hm() と同じ（分に丸めてから 時間・分）。1時間未満は「○分」"""
    m = jr(h * 60)
    return f"{m // 60}時間{m % 60}分" if m >= 60 else f"{m}分"


def mins_hm(m):
    m = jr(m)
    return f"{m // 60}時間{m % 60}分" if m >= 60 else f"{m}分"


def fig1():
    th, tl = DIST / VH, DIST / VL; save = (tl - th) * 60; per = TOLL / (save / 60)
    b = []
    x0, px = 210, 100                           # 1時間＝100px
    # 時間の目盛り
    for h in range(0, 10):
        x = x0 + h * px
        b.append(line(x, 132, x, 388, LINE, 1))
        b.append(text(x, 412, f"{h}", 15, INK2, anchor="middle"))
    b.append(text(x0 + 9 * px + 14, 412, "時間", 15, INK2))
    b.append(line(x0, 392, x0 + 9 * px, 392, INK, 1.6))
    # 高速
    y = 150
    b.append(text(60, y + 28, "高速", 22, TEAL_D, 700) + text(60, y + 52, f"平均{VH}km/h", 15, INK2))
    b.append(rect(x0, y, th * px, 56, TEAL, TEAL, 6))
    b.append(text(x0 + th * px / 2, y + 36, hm(th), 20, "#fff", 700, "middle"))
    b.append(text(x0 + th * px + 16, y + 24, f"高速料金 {TOLL:,}円", 19, ACC, 700))
    b.append(text(x0 + th * px + 16, y + 48, f"{DIST}km ÷ {VH}km/h", 15, MUTED))
    # 下道
    y = 250
    b.append(text(60, y + 28, "下道", 22, GOLD, 700) + text(60, y + 52, f"平均{VL}km/h", 15, INK2))
    b.append(rect(x0, y, tl * px, 56, GOLD, GOLD, 6))
    b.append(text(x0 + th * px / 2, y + 36, hm(tl) + "（料金0円）", 20, "#fff", 700, "middle"))
    # 短縮時間
    xs, xe = x0 + th * px, x0 + tl * px
    b.append(line(xs, 214, xs, 360, ACC, 2, "6 5"))
    b.append(line(xs, 346, xe, 346, ACC, 2.2) + line(xs, 336, xs, 356, ACC, 2.2) + line(xe, 336, xe, 356, ACC, 2.2))
    b.append(rect((xs + xe) / 2 - 170, 322, 340, 32, BG, BG, 4))
    b.append(text((xs + xe) / 2, 345, f"短縮できる時間 {mins_hm(save)}（{jr(save)}分）", 18, ACC, 700, "middle"))
    # 下：時短1時間あたりの費用
    y = 446
    b.append(rect(60, y, 230, 84, CARD, LINE, 10) + text(175, y + 30, "高速料金", 15, INK2, anchor="middle") + text(175, y + 66, f"{TOLL:,}円", 26, INK, 700, "middle"))
    b.append(text(320, y + 56, "÷", 30, INK2, 700, "middle"))
    b.append(rect(350, y, 270, 84, CARD, LINE, 10) + text(485, y + 30, "短縮できる時間", 15, INK2, anchor="middle") + text(485, y + 66, f"{save / 60:.2f}時間", 26, INK, 700, "middle"))
    b.append(text(650, y + 56, "＝", 30, INK2, 700, "middle"))
    b.append(rect(680, y, 270, 84, ACC_L, ACC, 10) + text(815, y + 30, "時短1時間あたりの費用", 15, INK2, anchor="middle") + text(815, y + 66, f"約{jr(per):,}円", 26, ACC, 700, "middle"))
    b.append(lines(972, y + 30, ["これが自分の時給より", "安いと感じれば", "高速がお得"], 16, INK, 1.45))
    b.append(text(60, 586, "所要時間＝距離÷平均速度　／　短縮時間＝下道の時間−高速の時間", 16, INK2))
    return svg("".join(b), f"高速と下道のくらべ方（{DIST}km・高速料金{TOLL:,}円の例）",
               "ガソリン代の差は含めない（一般に高速のほうが燃費は良い傾向）。平均速度は休けい・渋滞で変わる。")


def fig2():
    dists = [50, 100, 200, 300, 500]; wages = [1000, 2000, 3000]
    rows = []
    for d in dists:
        th, tl = d / VH, d / VL
        save_m = jr(tl * 60) - jr(th * 60)               # 表示上の所要時間の差（＝JS の短縮分と同じ値になる）
        assert save_m == jr((tl - th) * 60)
        rows.append([f"{d}km", hm(th), hm(tl), mins_hm(save_m)] + [f"約{jr(w * (tl - th) / 100) * 100:,}円" for w in wages])
    cols = ["距離", "高速の所要", "下道の所要", "短縮できる時間"] + [f"時給{w:,}円の人" for w in wages]
    cw = [110, 150, 150, 170, 166, 166, 166]
    x0, y0, rh = 60, 168, 60
    b = []
    gx = x0 + sum(cw[:4])
    b.append(rect(gx, 120, sum(cw[4:]), 40, ACC_L, ACC_L, 8))
    b.append(text(gx + sum(cw[4:]) / 2, 147, "この料金までなら高速のほうが得", 18, ACC, 700, "middle"))
    b.append(table(x0, y0, cols, rows, cw, rh, 18))
    b.append(lines(60, 556, [f"高速の平均{VH}km/h・下道の平均{VL}km/h（シミュの初期値）で計算。100円単位で四捨五入。",
                             "料金が表の額より安ければ「時短1時間あたりの費用」が時給より安い＝高速のほうが得。"], 16, INK2, 1.6))
    return svg("".join(b), "何kmなら高速？ 距離ごとの時短と料金の目安",
               "例：300kmで高速料金6,000円なら、時短1時間あたり約1,244円。時給がこれより高い人には高速が得。")


FIGS = [
    dict(svg=fig1, alt="高速と下道の比較の図。300kmを高速（平均80km/h）なら3時間45分・料金6,000円、下道（平均35km/h）なら8時間34分で、高速で4時間49分短縮でき、時短1時間あたりの費用は約1,244円になる計算を示す。",
         caption="高速と下道のくらべ方。高速料金を短縮できる時間で割った「時短1時間あたりの費用」を、自分の時給とくらべる。"),
    dict(svg=fig2, alt="距離50km・100km・200km・300km・500kmごとの高速と下道の所要時間、短縮できる時間と、時給1,000円・2,000円・3,000円の人にとって高速のほうが得になる高速料金の上限の早見表。",
         caption="距離ごとの時短と、高速を使ったほうが得になる料金の目安（高速80km/h・下道35km/hの場合）。"),
]
