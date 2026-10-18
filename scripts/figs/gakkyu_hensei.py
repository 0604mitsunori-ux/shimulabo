"""学級編成シミュレーター（gakkyu-hensei）の図。
式はページの JS と同じ：クラス数 = ceil(人数 ÷ 上限)、1クラス平均 = 人数 ÷ クラス数、あと何人で+1クラス = クラス数×上限 − 人数 + 1。
制度：公立小学校は2021〜2025年度に学年進行で35人へ（全学年35人）。公立中学校は義務標準法改正（2026年3月31日公布・4月1日施行）で
40人→35人、2026年度中1・2027年度中2・2028年度中3の順。特別支援学級は8人。"""
import math
from decimal import Decimal, ROUND_HALF_UP
from figlib import *

ANCHOR = r'<div class="note"><strong>計算式</strong>.*?</div>\s*<p>.*?</p>\n'
CAP = 35


def fix1(v):
    """JS の toFixed(1) と同じ（ちょうど半分は切り上げ）"""
    return str(Decimal(repr(v)).quantize(Decimal("0.1"), ROUND_HALF_UP))


def classes(n, cap=CAP):
    return math.ceil(n / cap)


def split(n, k):
    """n人を k クラスにできるだけ均等に分けた人数（多い順）"""
    q, r = divmod(n, k)
    return [q + 1] * r + [q] * (k - r)


def class_box(x, y, label, num, cap=CAP):
    """1クラス分の箱：席（7列×5段）のうち num 席に人が入っている"""
    out = [rect(x, y, 152, 132, CARD, LINE, 8)]
    out.append(text(x + 76, y + 24, label, 15, INK2, 700, "middle"))
    for i in range(cap):
        cx, cy = x + 22 + (i % 7) * 18, y + 44 + (i // 7) * 18
        out.append(circle(cx, cy, 6.5, TEAL if i < num else "none", TEAL if i < num else "#cfc9bb", 1.4))
    return "".join(out)


def fig1():
    b = []
    rows = [(70, 132), (71, 330)]
    for n, y in rows:
        k = classes(n); sp = split(n, k)
        b.append(text(60, y + 52, f"{n}人", 32, INK, 700))
        b.append(text(60, y + 88, f"→ {k}クラス", 19, TEAL, 700))
        b.append(text(60, y + 116, f"平均 {fix1(n / k)}人", 16, INK2))
        for j, m in enumerate(sp):
            b.append(class_box(200 + j * 170, y, f"{j + 1}組 {m}人", m))
    b.append(arrow(110, 268, 110, 316, "acc", 2.6) + text(124, 300, "＋1人", 18, ACC, 700))
    b.append(circle(208, 505, 6.5, TEAL, TEAL, 1.4) + text(222, 510, "＝児童生徒", 15, MUTED)
             + circle(324, 505, 6.5, "none", "#cfc9bb", 1.4) + text(338, 510, "＝空き（1クラス35人まで）", 15, MUTED))
    # 右：決まり方
    rx, rw = 750, 402
    b.append(rect(rx, 112, rw, 372, CARD, LINE, 10))
    b.append(text(rx + 20, 146, "クラス数の決まり方（35人学級）", 18, INK, 700))
    items = [("1", "クラス数 ＝ 人数 ÷ 35（切り上げ）", [f"70 ÷ 35 ＝ 2 → 2クラス", f"71 ÷ 35 ＝ {71 / 35:.2f}… → 3クラス"]),
             ("2", "1クラス平均 ＝ 人数 ÷ クラス数", [f"71 ÷ 3 ＝ {fix1(71 / 3)}人"]),
             ("3", "あと何人で＋1クラス", ["＝ クラス数 × 35 − 人数 ＋ 1", f"71人なら 3 × 35 − 71 ＋ 1 ＝ {3 * 35 - 71 + 1}人"])]
    y = 188
    for no, head, sub in items:
        b.append(badge(rx + 32, y - 6, no, TEAL, "#fff", 14) + text(rx + 54, y, head, 17, INK, 700))
        b.append(lines(rx + 54, y + 30, sub, 16, INK2, 1.6))
        y += 30 + len(sub) * 26 + 34
    b.append(rect(48, 548, 1104, 56, ACC_L, ACC_L, 10))
    b.append(text(600, 584, f"70人→71人の「1人の差」で、クラスが1つふえ、1クラスの人数は35人から約{71 / 3:.0f}人に。", 18, ACC, 700, "middle"))
    return svg("".join(b), "1人ふえるとクラスが変わる（学級編成のしくみ）",
               "公立小中学校の「学級編制の標準」（1学級35人）で計算した例。")


def fig2():
    b = []
    b.append(text(48, 124, "学年の人数 → クラス数と1クラス平均", 19, INK, 700))
    rows = []
    for k in range(1, 7):
        lo35, hi35, lo40, hi40 = 35 * (k - 1) + 1, 35 * k, 40 * (k - 1) + 1, 40 * k
        avg35 = "〜35人" if k == 1 else f"{fix1(lo35 / k)}〜35人"
        avg40 = "〜40人" if k == 1 else f"{fix1(lo40 / k)}〜40人"
        rows.append([f"{k}クラス", f"{lo35}〜{hi35}人", avg35, f"{lo40}〜{hi40}人", avg40])
    cw = [110, 150, 150, 150, 150]
    b.append(table(48, 142, ["クラス数", "35人学級", "1クラス平均", "40人学級", "1クラス平均"], rows, cw, 54, 17))
    b.append(f'<rect x="{48 + cw[0]}" y="186" width="{cw[1] + cw[2]}" height="4" fill="{TEAL}"/>'
             f'<rect x="{48 + sum(cw[:3])}" y="186" width="{cw[3] + cw[4]}" height="4" fill="{GOLD}"/>')
    b.append(text(48, 560, "あと何人で＋1クラス ＝ クラス数 × 上限 − 人数 ＋ 1", 17, INK, 700))
    b.append(text(48, 592, f"例）72人・35人学級 → {classes(72)}クラス（平均{fix1(72 / classes(72))}人）、あと{classes(72) * 35 - 72 + 1}人で4クラス", 16, INK2))
    # 右：制度
    rx, rw = 790, 362
    b.append(rect(rx, 104, rw, 420, TEAL_L, TEAL_L, 10))
    b.append(text(rx + 20, 140, "学級編制の標準（公立小中学校）", 18, TEAL_D, 700))
    blocks = [("小学校", "35人", ["2021年度から学年ごとに引き下げ、", "2025年度に全学年が35人に"]),
              ("中学校", "40人 → 35人", ["2026年度の中1から順に引き下げ、", "2028年度に全学年が35人に"]),
              ("特別支援学級", "8人", [])]
    y = 186
    for head, val, sub in blocks:
        b.append(text(rx + 20, y, head, 16, INK2, 700) + text(rx + rw - 20, y, val, 21, TEAL_D, 700, "end"))
        b.append(lines(rx + 20, y + 30, sub, 15.5, INK2, 1.6))
        y += 30 + len(sub) * 25 + 30
        b.append(line(rx + 20, y - 26, rx + rw - 20, y - 26, "#d3e1e8", 1))
    b.append(lines(rx + 20, y + 4, ["都道府県の基準で、標準より少ない", "人数で編制することもある。"], 15.5, INK2, 1.6))
    return svg("".join(b), "学年の人数とクラス数の早見表（35人学級・40人学級）",
               "1クラス平均の幅：その学級数になる人数のうち、いちばん少ないとき〜上限いっぱいのとき。")


FIGS = [
    dict(svg=fig1,
         alt="学級編成のしくみの図。35人学級で学年70人なら35人ずつ2クラス、71人になると3クラス（24人・24人・23人、平均23.7人）に分かれることを座席の丸で示し、クラス数＝人数÷35（切り上げ）、1クラス平均、あと何人で1クラス増えるかの計算をまとめている。",
         caption="学級編成のしくみ。クラス数＝人数÷35（端数は切り上げ）。1人の差でクラス数と1クラスの人数が大きく変わる。"),
    dict(svg=fig2,
         alt="学年の人数とクラス数の早見表。35人学級と40人学級で1〜6クラスになる学年の人数の範囲と1クラス平均の幅、公立小中学校の学級編制の標準（小学校35人、中学校は2026年度から段階的に40人から35人へ、特別支援学級8人）をまとめた図。",
         caption="学年の人数とクラス数の早見表。35人学級では36人・71人・106人…でクラスが1つ増える。"),
]
