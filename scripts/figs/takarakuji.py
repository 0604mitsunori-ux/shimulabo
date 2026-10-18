"""宝くじ買い続けたらシミュレーター（takarakuji）の図。
式はページの JS と同じ：総額＝1回の額×年の回数×年数、期待回収＝総額×47%、運用比較＝毎年の購入額を年3%で積立（fv=(fv+年額)×1.03 を年数回）。"""
from figlib import *

ANCHOR = r'<div class="note"><strong>計算式</strong>.*?</div>\s*<p>.*?</p>\n'
RET, RATE = 0.47, 0.03


def fv(annual, years):
    """ページの JS：for(i<years){ fv=(fv+annual)*1.03 }"""
    f = 0.0
    for _ in range(years):
        f = (f + annual) * (1 + RATE)
    return f


def man(v):
    """円 → ◯万円（小数1けた、.0 は省く）"""
    s = f"{v / 10000:.1f}".rstrip("0").rstrip(".")
    return f"{s}万円"


def yen(v):
    return f"{round(v):,}円"


def fig1():
    b = []
    # 左：お金のゆくえ
    x0, bw = 60, 500
    b.append(text(x0, 128, "買ったお金のゆくえ（還元率 約47%）", 19, INK, 700))
    w1 = bw * RET
    b.append(f'<rect x="{x0}" y="148" width="{w1:.1f}" height="66" rx="8" fill="{TEAL}"/>')
    b.append(f'<rect x="{x0 + w1:.1f}" y="148" width="{bw - w1:.1f}" height="66" rx="8" fill="#cfc9bb"/>')
    b.append(text(x0 + w1 / 2, 176, "当せん金として", 16, "#fff", 700, "middle") + text(x0 + w1 / 2, 202, "戻る 47%", 18, "#fff", 700, "middle"))
    b.append(text(x0 + w1 + (bw - w1) / 2, 176, "戻らない", 16, INK, 700, "middle") + text(x0 + w1 + (bw - w1) / 2, 202, "53%", 18, INK, 700, "middle"))
    b.append(text(x0 + bw, 240, "（経費や、発売元の自治体の収益金など）", 15, MUTED, anchor="end"))
    amt = 3000
    b.append(text(x0, 290, f"1回{amt:,}円買うと…", 18, INK, 700))
    b.append(rect(x0, 304, 240, 94, TEAL_L, TEAL, 10, 1.4) + text(x0 + 120, 336, "平均して戻る（期待値）", 15, TEAL_D, 700, "middle")
             + text(x0 + 120, 378, yen(amt * RET), 28, TEAL, 700, "middle"))
    b.append(rect(x0 + 260, 304, 240, 94, ACC_L, ACC, 10, 1.4) + text(x0 + 380, 336, "期待値で戻らない", 15, ACC, 700, "middle")
             + text(x0 + 380, 378, yen(amt * (1 - RET)), 28, ACC, 700, "middle"))
    b.append(rect(x0, 424, bw, 170, CARD, LINE, 10))
    b.append(text(x0 + 20, 456, "期待値とは？", 17, INK, 700))
    b.append(lines(x0 + 20, 488, ["とても多くの人が買ったときの、1人あたりの平均の戻り。",
                                   "実際は、ほとんどの人は期待値より少なく、",
                                   "ごく一部の人が大きく当たる。"], 16, INK2, 1.6))
    b.append(text(x0 + 20, 578, "長く買うほど、平均では使った額の約53%が戻らない。", 16, ACC, 700))
    # 右：30年続けたら
    rx = 610
    b.append(text(rx, 128, "30年買い続けたら（年額別）", 19, INK, 700))
    rows = []
    for a in (10000, 30000, 60000, 120000):
        t = a * 30
        rows.append([f"年{man(a)}", man(t), man(t * RET), man(t - t * RET)])
    b.append(table(rx, 146, ["年額", "30年の総額", "期待回収（47%）", "実質の損失"], rows, [118, 136, 160, 126], 52, 17))
    b.append(text(rx, 446, "例：年3万円 ＝ 1回3,000円 × 年10回（シミュの初期値）", 15.5, INK2))
    b.append(rect(rx, 470, 540, 116, TEAL_L, TEAL_L, 10))
    b.append(lines(rx + 20, 504, ["総額 ＝ 1回の額 × 年の回数 × 年数",
                                   "期待回収 ＝ 総額 × 47%",
                                   "実質の損失 ＝ 総額 − 期待回収"], 17, INK, 1.6, font_weight="700"))
    return svg("".join(b), "宝くじの還元率と期待値のしくみ",
               "還元率47%はシミュで使う目安。くじの種類や回によって少しちがう。")


def fig2():
    b = []
    annual, years = 3000 * 10, 30
    gx, gy, gw, gh, ymax = 130, 566, 780, 370, 1600000
    px = lambda yr: gx + yr / years * gw
    py = lambda v: gy - v / ymax * gh
    b.append(text(60, 124, "1回3,000円 × 年10回（年3万円）を買い続けた場合（シミュの初期値）", 18, INK, 700))
    b.append(axes(gx, gy, gw, gh, "年", "金額",
                  [(yr / years * gw, f"{yr}年") for yr in (0, 5, 10, 15, 20, 25, 30)],
                  [(v / ymax * gh, (f"{v // 10000}万円" if v else "0")) for v in (0, 400000, 800000, 1200000, 1600000)], 14))
    tot = [(px(y), py(annual * y)) for y in range(years + 1)]
    back = [(px(y), py(annual * y * RET)) for y in range(years + 1)]
    inv = [(px(y), py(fv(annual, y))) for y in range(years + 1)]
    area = " ".join(f"{x:.1f},{y:.1f}" for x, y in tot + back[::-1])
    b.append(f'<polygon points="{area}" fill="{ACC_L}" stroke="none"/>')
    b.append(poly(inv, GOLD, 3.2, dash="9 6"))
    b.append(poly(tot, INK, 3.2))
    b.append(poly(back, TEAL, 3.2))
    yr = 24
    mid = (annual * yr + annual * yr * RET) / 2
    b.append(text(px(yr), py(mid) + 6, "期待値で戻らないお金", 16, ACC, 700, "middle"))
    t30, b30, f30 = annual * years, annual * years * RET, fv(annual, years)
    for v, c, nm, val in [(f30, GOLD, "同額を年3%で積立運用", "約" + man(round(f30, -3))),
                          (t30, INK, "使った総額", man(t30)),
                          (b30, TEAL, "期待される回収", man(b30))]:
        y = py(v)
        b.append(circle(px(years), y, 5, c, c, 0))
        b.append(text(px(years) + 16, y - 4, nm, 16, c, 700) + text(px(years) + 16, y + 20, val, 20, c, 700))
    b.append(text(px(years) + 16, py((t30 + b30) / 2) + 12, f"差 {man(t30 - b30)}", 17, ACC, 700))
    return svg("".join(b), "宝くじを30年買い続けたら（使った額・回収・運用の比較）",
               "運用は毎年の購入額を年3%で積み立てた概算（実際の運用成績は変動する）。当選の夢を否定するものではありません。")


FIGS = [
    dict(svg=fig1,
         alt="宝くじの還元率と期待値のしくみの図。買ったお金のうち当せん金として戻るのは約47%で53%は戻らないこと、1回3,000円買うと期待値は1,410円であること、年1万円・3万円・6万円・12万円を30年買い続けたときの総額・期待回収・実質の損失の早見表。",
         caption="還元率と期待値のしくみ。期待回収＝買った総額×47%（還元率の目安）。"),
    dict(svg=fig2,
         alt="宝くじを1回3,000円・年10回、30年買い続けたときのグラフ。使った総額は90万円、期待される回収は42.3万円で差は47.7万円、同じ額を年3%で積み立て運用した場合は約147万円になることを示す。",
         caption="30年買い続けたときの使った額・期待される回収・同額を年3%で運用した場合の比較（年3万円の例）。"),
]
