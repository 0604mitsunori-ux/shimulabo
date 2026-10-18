"""出席率シミュレーター（shusseki-ritsu）の図。
式はページの JS・本文と同じ：出席率＝(授業日数−欠席日数)÷授業日数×100、年間で9割維持＝floor(年間日数×0.1)−欠席日数、
休める回数の上限＝floor(授業回数×(1−出席率))。例はシミュの初期値（120日・欠席5日・年間200日）。"""
import math
from fractions import Fraction
from figlib import *

ANCHOR = r'<div class="note"><strong>計算式</strong>.*?</div>\s*<p>.*?</p>\n'
TOTAL, ABS, YEAR = 120, 5, 200


def rate(t, a):
    return (t - a) / t * 100


def can_abs(n, r):
    """出席率 r（分数）以上を保てる欠席回数の上限（端数切り捨て）"""
    return math.floor(n * (1 - r))


def fig1():
    b = []
    b.append(rect(48, 98, 1104, 70, TEAL_L, TEAL_L, 10))
    b.append(text(600, 145, "出席率（%）＝（授業日数 − 欠席日数）÷ 授業日数 × 100", 24, INK, 700, "middle"))
    # 左：例
    x0 = 60
    r = rate(TOTAL, ABS); att = TOTAL - ABS
    b.append(text(x0, 212, f"例）授業日数{TOTAL}日・欠席{ABS}日（シミュの初期値）", 18, INK, 700))
    bw, by = 520, 232
    wa = bw * att / TOTAL
    b.append(f'<rect x="{x0}" y="{by}" width="{wa:.1f}" height="50" rx="6" fill="{TEAL}"/>'
             f'<rect x="{x0 + wa + 2:.1f}" y="{by}" width="{bw - wa - 2:.1f}" height="50" rx="3" fill="{ACC}"/>')
    b.append(text(x0 + wa / 2, by + 32, f"出席 {att}日", 18, "#fff", 700, "middle"))
    b.append(text(x0 + bw, by + 74, f"欠席 {ABS}日", 16, ACC, 700, "end"))
    b.append(text(x0, by + 74, f"授業日数 {TOTAL}日", 16, INK2))
    steps = [("1", f"出席日数 ＝ {TOTAL} − {ABS} ＝ {att}日", INK),
             ("2", f"出席率 ＝ {att} ÷ {TOTAL} × 100 ＝ 約{r:.1f}%", ACC)]
    y = 370
    for no, s, c in steps:
        b.append(badge(x0 + 16, y - 7, no, TEAL, "#fff", 15) + text(x0 + 40, y, s, 20, c, 700))
        y += 46
    keep = math.floor(YEAR * 0.1) - ABS
    b.append(rect(x0, 470, bw, 122, GOLD_L, GOLD_L, 10))
    b.append(text(x0 + 18, 502, f"年間{YEAR}日で 9割（90%）を保つには", 17, INK, 700))
    b.append(text(x0 + 18, 538, f"休めるのは {YEAR} × 10% ＝ {math.floor(YEAR * 0.1)}日まで", 17, INK2))
    b.append(text(x0 + 18, 574, f"いま欠席{ABS}日 → あと{keep}日まで", 20, GOLD, 700))
    # 右：早見表（年間200日）
    rx = 640
    b.append(text(rx, 212, f"出席率の早見表（年間{YEAR}日の場合）", 18, INK, 700))
    marks = {0: "皆勤", 5: "非常に良好", 10: "良好", 20: "ひとつの目安ライン", 40: "注意（要件に注意）", 60: "進級・単位に影響も"}
    rows = []
    for a, m in marks.items():
        v = rate(YEAR, a)
        rows.append([f"{a}日", ("100%" if a == 0 else f"{v:.1f}%"), m])
    b.append(table(rx, 228, ["欠席日数", "出席率", "目安"], rows, [130, 140, 242], 52, 17))
    return svg("".join(b), "出席率の計算方法（式と早見表）",
               "出席停止や忌引きは欠席に数えない扱いが一般的（学校で確認）。目安は在籍校の規定で変わる。")


def fig2():
    b = []
    b.append(rect(48, 98, 1104, 62, TEAL_L, TEAL_L, 10))
    b.append(text(600, 140, "休める回数の上限 ＝ 授業回数 ×（1 − 出席率）　※端数は切り捨て", 22, INK, 700, "middle"))
    targets = [("90%以上", Fraction(9, 10)), ("80%以上", Fraction(8, 10)), ("75%以上", Fraction(3, 4)), ("3分の2以上", Fraction(2, 3))]
    lessons = [(15, "回", "（大学の半期）"), (30, "回", "（大学の通年）"), (35, "回", "（高校の週1科目）"), (200, "日", "（年間の授業日数）")]
    rows = [[f"{n}{u}{d}"] + [f"{can_abs(n, r)}{u}まで" for _, r in targets] for n, u, d in lessons]
    b.append(table(80, 182, ["授業回数", *[t for t, _ in targets]], rows, [320, 190, 190, 190, 150], 54, 18.5))
    # 例：15回で3分の2以上
    n, keep = 15, can_abs(15, Fraction(2, 3))
    y = 512
    b.append(text(80, y - 14, f"例）大学の半期{n}回で「3分の2以上の出席」なら", 18, INK, 700))
    for i in range(n):
        cx = 100 + i * 46
        absent = i >= n - keep
        b.append(circle(cx, y + 30, 17, ACC_L if absent else TEAL, ACC if absent else TEAL, 2))
        b.append(text(cx, y + 36, "欠" if absent else "出", 15, ACC if absent else "#fff", 700, "middle"))
    b.append(text(100 + n * 46, y + 25, f"出席{n - keep}回以上", 18, TEAL, 700))
    b.append(text(100 + n * 46, y + 51, f"欠席{keep}回まで", 18, ACC, 700))
    b.append(text(80, 606, "遅刻・早退を欠席に数える学校や、「3分の1を超えて欠席すると不可」など境目の扱いがちがう学校もある。", 15.5, INK2))
    return svg("".join(b), "出席率◯%を保つには何回まで休める？（早見表）",
               "3分の2以上＝約66.7%以上。高校・大学の単位認定でよく使われる。最終的には在籍校の規定を確認。")


FIGS = [
    dict(svg=fig1,
         alt="出席率の計算方法の図。出席率（%）＝（授業日数−欠席日数）÷授業日数×100の式と、授業日数120日・欠席5日で出席率約95.8%になる計算例、年間200日で9割を保てる欠席は20日までであること、欠席0〜60日の出席率の早見表。",
         caption="出席率の計算方法。出席率＝（授業日数−欠席日数）÷授業日数×100。年間200日なら欠席20日で90%。"),
    dict(svg=fig2,
         alt="出席率90%・80%・75%・3分の2以上を保つために休める回数の早見表。授業15回（大学の半期）・30回（大学の通年）・35回（高校の週1科目）・年間200日ごとの欠席の上限と、15回で3分の2以上なら欠席5回までになる例。",
         caption="出席率を保てる欠席回数の早見表。欠席回数 ≦ 授業回数 ×（1 − 出席率）、端数は切り捨て。"),
]
