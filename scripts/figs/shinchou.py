"""子どもの身長予測（shinchou）の図。式はページの JS・本文と同じ：
男の子＝(父＋母＋13)÷2、女の子＝(父＋母−13)÷2、目安の範囲＝予測±9cm（表示は Math.round）。"""
import math
from figlib import *

ANCHOR = r'<h2>計算方法</h2>\s*<div class="note">.*?</div>\s*<p>.*?</p>\n'


def pred(dad, mom, boy=True):
    return (dad + mom + (13 if boy else -13)) / 2


def jsround(x):
    return math.floor(x + 0.5)


def cm(v):
    return f"{v:g}"


def fig1():
    b = []
    dad, mom = 172, 158                     # ページの初期値
    avg = (dad + mom) / 2
    pb, pg = pred(dad, mom, True), pred(dad, mom, False)
    assert pb == avg + 6.5 and pg == avg - 6.5
    # 上：式
    for i, (lab, f, col) in enumerate([("男の子", "（ 父の身長 ＋ 母の身長 ＋ 13 ）÷ 2", TEAL), ("女の子", "（ 父の身長 ＋ 母の身長 − 13 ）÷ 2", ACC)]):
        y = 104 + i * 66
        b.append(rect(48, y, 700, 56, CARD, col, 10, 1.8))
        b.append(text(72, y + 37, lab, 21, col, 700) + text(170, y + 37, f, 21, INK, 700))
    b.append(rect(770, 104, 382, 122, TEAL_L, TEAL_L, 10))
    b.append(lines(790, 136, ["＝ 両親の平均 ＋ 6.5cm（男の子）", "＝ 両親の平均 − 6.5cm（女の子）", "13cm＝大人の男女の身長差の目安"], 17, INK, 1.6))
    # 下：数直線（例）
    lo, hi, X0, X1 = 145, 185, 150, 1100
    px = lambda v: X0 + (v - lo) * (X1 - X0) / (hi - lo)
    b.append(text(48, 266, f"例：父 {dad}cm・母 {mom}cm のとき（ツールの初期値）", 18, INK, 700))
    ay = 590
    b.append(line(X0, ay, X1, ay, INK, 1.6))
    for v in range(lo, hi + 1, 5):
        b.append(line(px(v), ay, px(v), ay + 8, INK, 1.4) + text(px(v), ay + 26, f"{v}", 14, INK2, anchor="middle"))
        b.append(line(px(v), 286, px(v), ay, LINE, 1))
    b.append(text(X1 + 24, ay + 26, "cm", 14, INK2))
    # 両親
    ry = 330
    b.append(text(48, ry + 6, "両親", 18, INK, 700))
    for v, lab, col in [(mom, f"母 {mom}", ACC), (dad, f"父 {dad}", TEAL)]:
        b.append(circle(px(v), ry, 8, col, "#fff", 2) + text(px(v), ry - 16, lab, 16, col, 700, "middle"))
    b.append(f'<rect x="{px(avg) - 7:.1f}" y="{ry - 7}" width="14" height="14" fill="{INK}" transform="rotate(45 {px(avg):.1f} {ry})"/>')
    b.append(text(px(avg), ry + 30, f"平均 {cm(avg)}", 16, INK, 700, "middle"))
    b.append(line(px(avg), ry + 38, px(avg), ay, INK2, 1.6, "5 5"))
    # 男の子・女の子
    for y, lab, p, col, ac, d in [(430, "男の子", pb, TEAL, "teal", +1), (520, "女の子", pg, ACC, "acc", -1)]:
        a, e = p - 9, p + 9
        b.append(text(48, y + 6, lab, 18, col, 700))
        b.append(f'<rect x="{px(a):.1f}" y="{y - 11}" width="{px(e) - px(a):.1f}" height="22" rx="11" fill="{TEAL_L if d > 0 else ACC_L}" stroke="{col}" stroke-width="1.6"/>')
        b.append(circle(px(p), y, 9, col, "#fff", 2))
        b.append(text(px(p), y - 20, f"予測 {cm(p)}cm", 18, col, 700, "middle"))
        b.append(text(px(e) + 10, y + 6, f"目安 {jsround(a)}〜{jsround(e)}cm", 15, INK2))
        b.append(arrow(px(avg), y + 24, px(p), y + 24, ac, 2))
        b.append(text((px(avg) + px(p)) / 2, y + 44, f"{'＋' if d > 0 else '−'}6.5cm", 14, col, 700, "middle"))
    return svg("".join(b), "子どもの身長予測のしくみ（両親の身長から・目安）",
               "あくまで目安。実際の身長は睡眠・栄養・運動でも変わり、±9cmほどの幅がある。")


def fig2():
    b = []
    dads = [160, 165, 170, 175, 180]
    moms = [150, 155, 160, 165]
    for k, (boy, col, lab, x0) in enumerate([(True, TEAL, "男の子の予測身長（cm）", 60), (False, ACC, "女の子の予測身長（cm）", 630)]):
        b.append(text(x0, 128, lab, 20, col, 700))
        rows = [[f"父 {d}"] + [cm(pred(d, m, boy)) for m in moms] for d in dads]
        b.append(table(x0, 146, ["父＼母"] + [f"母 {m}" for m in moms], rows, [110] + [100] * 4, 60, 18,
                       head_fill=TEAL_L if boy else ACC_L))
    b.append(lines(60, 548, ["男の子＝（父＋母＋13）÷2　女の子＝（父＋母−13）÷2", "実際は予測から±9cmほどの幅がある目安。睡眠・栄養・運動でも変わる。"], 17, INK2, 1.7))
    return svg("".join(b), "両親の身長から見る 子どもの予測身長 早見表（目安）",
               "身長の単位はcm。表は計算ツールと同じ式で出した予測値。")


FIGS = [
    dict(svg=fig1, alt="子どもの身長予測のしくみの図。男の子は（父の身長＋母の身長＋13）÷2、女の子は（父＋母−13）÷2で、両親の平均身長から男の子は6.5cm高く、女の子は6.5cm低くなる。父172cm・母158cmなら男の子171.5cm・女の子158.5cmで、それぞれ±9cmの目安の幅を数直線で示す。",
         caption="子どもの身長予測のしくみ（目安）。両親の平均に男の子は＋6.5cm、女の子は−6.5cm。"),
    dict(svg=fig2, alt="両親の身長から子どもの予測身長を読む早見表。父160〜180cm・母150〜165cmの組み合わせごとに、男の子と女の子の予測身長（目安）を並べている。",
         caption="両親の身長別の予測身長 早見表（目安）。実際は±9cmほどの幅がある。"),
]
