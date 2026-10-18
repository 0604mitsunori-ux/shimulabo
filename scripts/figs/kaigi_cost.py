"""会議コスト（kaigi-cost）の図。値はページの JS と同じ式：1人1時間＝年収÷1,900時間、会議1回＝1人1時間×人数×時間、年間＝1回×回数"""
import math
from figlib import *

ANCHOR = r"年間では <strong>80万円以上</strong> に達します。.*?</p>\n"
HOURS = 1900                                   # ページの JS の ANNUAL_HOURS
FREQ = {"毎週": 52, "毎営業日": 251, "毎月": 12}  # ページの JS の開催ペース


def jr(x):
    return math.floor(x + 0.5)                 # JS の Math.round と同じ


def yen(x):
    return f"{jr(x):,}円"


def cost(salary_man, people, minutes):
    return salary_man * 10000 / HOURS * people * minutes / 60


def box(x, y, w, h, label, value, fill=CARD, stroke=LINE, vcol=INK, vsize=26):
    return (rect(x, y, w, h, fill, stroke, 10, 1.6) + text(x + w / 2, y + 30, label, 15, INK2, anchor="middle")
            + text(x + w / 2, y + 66, value, vsize, vcol, 700, "middle"))


def op(x, y, s):
    return text(x, y, s, 30, INK2, 700, "middle")


def fig1():
    sal, ppl, mins = 500, 6, 60
    ph = sal * 10000 / HOURS; once = ph * ppl * mins / 60; year = once * FREQ["毎週"]
    b = []
    X = [96, 371, 646, 921]; BW, BH = 215, 84          # 4列（列のあいだに演算子）
    rows = [(122, "① 1人1時間あたりの人件費"), (264, "② 会議1回のコスト"), (406, "③ 1年間のコスト（毎週開く場合）")]
    for (y, cap), no in zip(rows, "123"):
        b.append(text(X[0], y, cap, 17, INK, 700))
    # ①
    y = 134
    b.append(box(X[0], y, BW, BH, "平均年収", f"{sal}万円"))
    b.append(op(X[0] + BW + 30, y + 54, "÷"))
    b.append(box(X[1], y, BW, BH, "年間の労働時間", f"約{HOURS:,}時間"))
    b.append(op(X[1] + BW + 30, y + 54, "＝"))
    b.append(box(X[2], y, BW, BH, "1人1時間あたり", f"約{yen(ph)}", TEAL_L, TEAL, TEAL_D))
    b.append(lines(X[3] + 4, y + 30, ["1日約7.5時間×月20日", "×12か月＝1,800〜1,900時間", "という一般的な目安"], 14, MUTED, 1.5))
    # ②
    y = 276
    b.append(box(X[0], y, BW, BH, "①の答え（1人1時間）", f"約{yen(ph)}", TEAL_L, TEAL, TEAL_D))
    b.append(op(X[0] + BW + 30, y + 54, "×"))
    b.append(box(X[1], y, BW, BH, "参加人数", f"{ppl}人"))
    b.append(op(X[1] + BW + 30, y + 54, "×"))
    b.append(box(X[2], y, BW, BH, "会議の時間", f"{mins // 60}時間（{mins}分）"))
    b.append(op(X[2] + BW + 30, y + 54, "＝"))
    b.append(box(X[3], y, BW, BH, "会議1回の人件費", yen(once), ACC_L, ACC, ACC))
    # ③
    y = 418
    b.append(box(X[0], y, BW, BH, "②の答え（会議1回）", yen(once), ACC_L, ACC, ACC))
    b.append(op(X[0] + BW + 30, y + 54, "×"))
    b.append(box(X[1], y, BW, BH, "開く回数", f"毎週＝年{FREQ['毎週']}回"))
    b.append(op(X[1] + BW + 30, y + 54, "＝"))
    b.append(box(X[2], y, BW, BH, "1年間の人件費", yen(year), ACC_L, ACC, ACC))
    b.append(lines(X[3] + 4, y + 30, [f"1分あたり 約{yen(once / mins)}", f"1秒あたり 約{once / mins / 60:.1f}円"], 17, INK, 1.6))
    # 下：減らし方
    b.append(rect(48, 534, 1104, 76, GOLD_L, "#e8d9b5", 10))
    b.append(text(72, 564, "コストは人数と時間に比例する", 17, INK, 700))
    b.append(text(72, 592, f"60分→45分にすると25%減（{yen(once * 0.75)}）、6人→4人にすると約33%減（{yen(cost(sal, 4, mins))}）。", 16, INK2))
    return svg("".join(b), "会議コストの計算のしくみ（年収500万円・6人・60分の例）",
               "社会保険料・オフィス代などは含まない概算。実際のコストはこれより高い（最低ラインの目安）。")


def fig2():
    sals = [350, 500, 650, 800, 1000]; ppls = [3, 6, 10, 20]
    rows = [[f"{p}人"] + [yen(cost(s, p, 60)) for s in sals] for p in ppls]
    cols = ["参加人数"] + [f"年収{s:,}万円" if i == 0 else f"{s:,}万円" for i, s in enumerate(sals)]
    b = [text(60, 124, "会議1回（60分）の人件費　※平均年収は参加者の平均", 17, INK, 700)]
    x0, y0, rh, cw = 60, 140, 58, [160, 184, 184, 184, 184, 184]
    b.append(table(x0, y0, cols, rows, cw, rh, 19))
    # シミュの初期値（6人・500万円）を囲む
    r, c = ppls.index(6) + 1, sals.index(500) + 1
    b.append(f'<rect x="{x0 + sum(cw[:c]) + 3}" y="{y0 + rh * r + 3}" width="{cw[c] - 6}" height="{rh - 6}" rx="6" fill="none" stroke="{ACC}" stroke-width="2.6"/>')
    b.append(text(1140, 124, "赤わく＝シミュの初期値（6人・年収500万円）", 15, ACC, 700, "end"))
    once = cost(500, 6, 60)
    cards = [("時間をかえると", ["30分なら半分、45分なら3/4。", "90分なら1.5倍。"]),
             ("毎週開くと（年52回）", ["上の金額×52。", f"6人・500万円なら {yen(once * 52)}"]),
             ("毎営業日だと（年251回）", ["上の金額×251。", f"6人・500万円なら {yen(once * 251)}"])]
    for i, (h, ls) in enumerate(cards):
        x = 60 + i * 364
        b.append(rect(x, 464, 352, 140, CARD, LINE, 10))
        b.append(text(x + 20, 498, h, 18, TEAL_D, 700))
        b.append(lines(x + 20, 534, ls, 17, INK, 1.6))
    return svg("".join(b), "会議コストの早見表（人数×平均年収）",
               "1人1時間＝年収÷1,900時間で計算（シミュと同じ式）。社会保険料などを含めると、実際はもっと高い。")


FIGS = [
    dict(svg=fig1, alt="会議コストの計算式を図にしたもの。平均年収500万円÷年間労働時間1,900時間＝1人1時間約2,632円、×6人×1時間＝会議1回15,789円、毎週開くと×52回で年間821,053円になる計算の流れを示す図。",
         caption="会議コストの計算のしくみ。年収÷1,900時間で1人1時間の人件費を出し、人数と時間をかける。"),
    dict(svg=fig2, alt="会議1回（60分）の人件費の早見表。参加人数3人・6人・10人・20人と平均年収350万〜1,000万円の組み合わせごとの金額と、時間を変えたとき・毎週や毎営業日開いたときの年間コストの目安。",
         caption="会議1回（60分）の人件費の早見表。人数と平均年収から、その会議の「値段」がすぐわかる。"),
]
