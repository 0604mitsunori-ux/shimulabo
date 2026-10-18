"""回転率（kaiten）の図。値はページの JS と同じ式：1日売上＝席数×回転数×客単価、月商＝1日売上×営業日数"""
from figlib import *

ANCHOR = r"工夫する価値が見えてきます。</p>\n"
SEATS, TURN, AOV, DAYS = 30, 2.5, 1200, 26      # ページの初期値


def man(x):
    """円 → 「○万円」（小数1桁まで・末尾の .0 は省く）"""
    v = round(x / 10000, 1)
    return (f"{v:,.0f}" if v == int(v) else f"{v:,.1f}") + "万円"


def card(x, y, w, h, title, value, sub, fill=CARD, stroke=LINE, vcol=INK):
    return (rect(x, y, w, h, fill, stroke, 12, 1.6) + text(x + w / 2, y + 32, title, 17, INK2, 700, "middle")
            + text(x + w / 2, y + 80, value, 32, vcol, 700, "middle") + text(x + w / 2, y + h - 18, sub, 15, MUTED, anchor="middle"))


def fig1():
    day = SEATS * TURN * AOV; month = day * DAYS; up = SEATS * (TURN + 0.5) * AOV * DAYS
    b = []
    X, W, Y, H = [60, 340, 620, 900], 240, 112, 190
    b.append(card(X[0], Y, W, H, "席数", f"{SEATS}席", "お店の席の数"))
    for i in range(SEATS):                     # 席を30個ならべる
        cx, cy = X[0] + 33 + (i % 10) * 19.5, Y + 100 + (i // 10) * 16
        b.append(rect(cx, cy, 13, 12, TEAL_L, TEAL, 2, 1.2))
    b.append(text(X[0] + W + 20, Y + 98, "×", 30, INK2, 700, "middle"))
    b.append(card(X[1], Y, W, H, "回転数", f"{TURN}回", "1席に1日何組座るか"))
    for k in range(3):                         # 2.5回＝2回＋半分
        cx = X[1] + 72 + k * 48; frac = min(1, TURN - k)
        b.append(circle(cx, Y + 126, 16, CARD, LINE, 2))
        if frac >= 1:
            b.append(circle(cx, Y + 126, 16, "none", TEAL, 4))
        elif frac > 0:
            b.append(f'<path d="M{cx},{Y + 110} A16,16 0 0 1 {cx},{Y + 142}" fill="none" stroke="{TEAL}" stroke-width="4"/>')
    b.append(text(X[1] + W + 20, Y + 98, "×", 30, INK2, 700, "middle"))
    b.append(card(X[2], Y, W, H, "客単価", f"{AOV:,}円", "1人あたりの支払い"))
    b.append(text(X[2] + W / 2, Y + 130, "¥", 30, GOLD, 700, "middle"))
    b.append(text(X[2] + W + 20, Y + 98, "＝", 30, INK2, 700, "middle"))
    b.append(card(X[3], Y, W, H, "1日の売上", f"{day:,.0f}円", f"来客 のべ{SEATS * TURN:.0f}席分", TEAL_L, TEAL, TEAL_D))
    b.append(text(X[3] + W / 2, Y + 124, f"{SEATS}×{TURN}×{AOV:,}", 17, TEAL_D, anchor="middle"))
    # 月商
    y = 336
    b.append(arrow(X[3] + W / 2, Y + H + 4, X[3] + W / 2, y + 4, "teal", 2.4))
    b.append(rect(60, y + 8, 1080, 80, CARD, LINE, 12))
    b.append(text(90, y + 58, "月商 ＝ 1日の売上", 22, INK, 700))
    b.append(text(310, y + 58, f"{day:,.0f}円 × 月の営業日数 {DAYS}日 ＝", 22, INK))
    b.append(text(1110, y + 60, f"{month:,.0f}円（{man(month)}）", 28, ACC, 700, "end"))
    # 回転数を0.5上げると
    y = 458
    b.append(text(60, y, "回転数を0.5上げると（30席・客単価1,200円・月26日のまま）", 18, INK, 700))
    sc = 480 / 3000000                         # 300万円＝480px
    for i, (lab, v, col) in enumerate([(f"回転 {TURN}回", month, TEAL), (f"回転 {TURN + 0.5:.1f}回", up, ACC)]):
        yy = y + 18 + i * 62
        b.append(text(200, yy + 32, lab, 18, INK, 700, "end"))
        b.append(rect(220, yy, v * sc, 44, col, col, 6))
        b.append(text(220 + v * sc + 14, yy + 30, f"月商 {man(v)}", 20, col, 700))
    b.append(rect(880, y + 34, 260, 76, ACC_L, ACC, 10))
    b.append(text(1010, y + 64, "月商が2割ふえる", 17, INK2, anchor="middle"))
    b.append(text(1010, y + 96, f"＋{man(up - month)}", 26, ACC, 700, "middle"))
    return svg("".join(b), "飲食店の売上のしくみ（席数×回転数×客単価）",
               "回転数＝1つの席に1日に何組のお客さんが座るか（回転率）。提供スピード・予約・席の使い方で上がる。")


def fig2():
    turns = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5]; aovs = [800, 1200, 2000, 3000, 5000]
    rows = [[f"{t:.1f}回"] + [man(SEATS * t * a * DAYS) for a in aovs] for t in turns]
    cols = ["回転数＼客単価"] + [f"{a:,}円" for a in aovs]
    x0, y0, rh, cw = 60, 132, 58, [160, 140, 140, 140, 140, 140]
    b = [table(x0, y0, cols, rows, cw, rh, 19)]
    r, c = turns.index(TURN) + 1, aovs.index(AOV) + 1
    b.append(f'<rect x="{x0 + sum(cw[:c]) + 3}" y="{y0 + rh * r + 3}" width="{cw[c] - 6}" height="{rh - 6}" rx="6" fill="none" stroke="{ACC}" stroke-width="2.6"/>')
    tw = sum(cw)
    # 右：回転数の目安（ページの本文どおり、数値ではなく傾向）
    rx = x0 + tw + 36
    top, bot = y0 + rh + 8, y0 + rh * (len(turns) + 1) - 8
    b.append(arrow(rx, top, rx, bot, "teal", 2.6))          # 表は下へいくほど回転数が高い
    b.append(text(rx + 20, top + 16, "回転数が低め", 17, GOLD, 700))
    b.append(lines(rx + 20, top + 44, ["ディナー・カフェ", "（ゆっくり過ごす）"], 15, INK2, 1.5))
    b.append(text(rx + 20, bot - 96, "回転数が高め", 17, TEAL_D, 700))
    b.append(lines(rx + 20, bot - 68, ["ランチ中心の店", "（短い時間で", "　入れかわる）"], 15, INK2, 1.5))
    b.append(text(60, 568, f"赤わく＝シミュの初期値（{TURN}回・{AOV:,}円 → 月商{man(SEATS * TURN * AOV * DAYS)}）。", 16, ACC, 700))
    b.append(text(60, 596, "席数がちがうときは、表の値 × 席数 ÷ 30。営業日数がちがうときは、表の値 × 日数 ÷ 26。", 16, INK2))
    return svg("".join(b), f"月商の早見表（{SEATS}席・月{DAYS}日営業）",
               "回転数の目安は業態で大きく異なる。月商＝席数×回転数×客単価×営業日数（シミュと同じ式）。")


FIGS = [
    dict(svg=fig1, alt="飲食店の売上のしくみの図。30席×回転数2.5回×客単価1,200円＝1日の売上90,000円、×営業日数26日＝月商234万円になり、回転数を0.5上げて3.0回にすると月商が280.8万円（＋46.8万円）になることを示す。",
         caption="飲食店の売上のしくみ。回転数（回転率）を0.5上げるだけで、月商は2割ふえる。"),
    dict(svg=fig2, alt="30席・月26日営業の飲食店で、回転数1.0〜3.5回と客単価800円〜5,000円の組み合わせごとの月商の早見表。ランチ中心の店は回転数が高め、ディナー・カフェは低めという目安つき。",
         caption="月商の早見表（30席・月26日営業）。回転数と客単価から、月商の見当がつく。"),
]
