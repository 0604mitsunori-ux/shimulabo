"""大学4年間の費用（daigaku-4nen）の図。値はページの本文（国公立 約240〜250万円・私立文系 約400万円・私立理系 約540万円・医歯薬系はさらに高額、
自宅外は4年で300〜500万円上乗せ）と JS の初期値（入学金25万円・学費100万円×4年・教科書30万円・通学40万円・交際40万円）と同じ。"""
from figlib import *

INIT = [("入学金", 250000, GOLD), ("学費（年100万円×4年）", 1000000 * 4, TEAL), ("教科書・PC・学用品", 300000, PURPLE),
        ("通学定期・交通費", 400000, SKY), ("サークル・交際費・その他", 400000, ACC)]     # ページの JS の初期値


def fig1():
    b = []
    x0, sc = 230, 1.25                 # 1万円＝1.25px
    top, rh = 128, 82
    for v in range(0, 701, 100):
        x = x0 + v * sc
        b.append(line(x, top - 6, x, top + rh * 4, LINE, 1))
        b.append(text(x, top + rh * 4 + 22, f"{v}万円" if v else "0", 14, INK2, anchor="middle"))
    rows = [("国公立", 240, 250, TEAL, "約240〜250万円", ""),
            ("私立 文系", 400, 400, GOLD, "約400万円", "国公立より約150万円高い"),
            ("私立 理系", 540, 540, ACC, "約540万円", "国公立より約300万円高い"),
            ("医歯薬系", None, None, PURPLE, "さらに高額", "大学・学部による")]
    for i, (nm, lo, hi, col, lab, sub) in enumerate(rows):
        y = top + i * rh + 12
        b.append(text(x0 - 18, y + 36, nm, 21, INK, 700, "end"))
        if lo is None:                 # 医歯薬系：数値はページにないので「さらに高額」と矢印だけ
            w = 700 * sc
            b.append(f'<defs><linearGradient id="fade4" x1="0" x2="1"><stop offset="0" stop-color="{col}"/><stop offset="0.75" stop-color="{col}" stop-opacity="0.55"/><stop offset="1" stop-color="{col}" stop-opacity="0.05"/></linearGradient></defs>')
            b.append(f'<rect x="{x0}" y="{y}" width="{w}" height="50" rx="6" fill="url(#fade4)"/>')
            b.append(arrow(x0 + w - 30, y + 25, x0 + w + 36, y + 25, "ink", 2.6))
            b.append(text(x0 + 20, y + 33, lab + "（" + sub + "）", 19, "#fff", 700))
            continue
        b.append(rect(x0, y, lo * sc, 50, col, col, 6))
        if hi > lo:
            b.append(f'<rect x="{x0 + lo * sc}" y="{y}" width="{(hi - lo) * sc}" height="50" fill="{col}" opacity=".45"/>')
        b.append(text(x0 + hi * sc + 14, y + (24 if sub else 33), lab, 22, col, 700, paint_order="stroke", stroke=BG, stroke_width=6))
        if sub:
            b.append(text(x0 + hi * sc + 14, y + 46, sub, 15, INK2, paint_order="stroke", stroke=BG, stroke_width=6))
    b.append(text(x0, top - 16, "入学金＋授業料など（4年分）の目安", 16, INK2, 700))
    # 下：このほかにかかるお金
    y = 512
    b.append(text(60, y + 4, "このほかにかかるお金", 17, INK, 700))
    other = sum(v for _, v, _ in INIT[2:])
    for i, (h, s) in enumerate([("＋ 教科書・PC・通学費・交際費など", f"シミュの初期値では4年で{other // 10000}万円"),
                                ("＋ 自宅外通学なら 家賃・生活費", "4年で300〜500万円ほど上乗せが多い")]):
        x = 60 + i * 548
        b.append(rect(x, y + 16, 532, 80, GOLD_L if i else CARD, "#e8d9b5" if i else LINE, 10))
        b.append(text(x + 20, y + 48, h, 18, INK, 700))
        b.append(text(x + 20, y + 78, s, 17, INK2))
    return svg("".join(b), "大学4年間の学費の目安（国公立・私立）",
               "学費は大学・学部で大きく異なる目安。奨学金・教育ローン・授業料減免などの制度もある。")


def fig2():
    b = []
    tot = sum(v for _, v, _ in INIT)
    b.append(rect(48, 100, 1104, 50, TEAL_L, TEAL_L, 10))
    b.append(text(600, 133, "4年間の費用 ＝ 入学金 ＋ 年間の学費×4年 ＋ 教科書・PC ＋ 通学費 ＋ 交際費など", 19, TEAL_D, 700, "middle"))
    x0, W, y = 60, 1080, 196
    b.append(text(x0, y - 12, "シミュの初期値の例", 16, INK2, 700))
    b.append(text(x0 + W, y - 12, f"合計 {tot:,}円（{tot // 10000}万円）", 20, INK, 700, "end"))
    x = x0
    for nm, v, col in INIT:
        w = W * v / tot
        b.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="64" fill="{col}" stroke="#fff" stroke-width="2"/>')
        if w > 300:
            b.append(text(x + w / 2, y + 41, f"{nm} {v // 10000}万円", 20, "#fff", 700, "middle"))
        x += w
    # 内訳の表
    ty, rh = 300, 46
    b.append(text(120, ty, "費目", 15, INK2, 700) + text(760, ty, "金額", 15, INK2, 700, "end") + text(900, ty, "割合", 15, INK2, 700, "end"))
    b.append(line(80, ty + 10, 940, ty + 10, INK, 1.2))
    for i, (nm, v, col) in enumerate(INIT):
        yy = ty + 10 + i * rh
        b.append(rect(86, yy + 13, 22, 22, col, col, 4))
        b.append(text(120, yy + 31, nm, 18, INK))
        b.append(text(760, yy + 31, f"{v:,}円", 18, INK, anchor="end"))
        b.append(text(900, yy + 31, f"{v / tot * 100:.1f}%", 18, INK, anchor="end"))
        b.append(line(80, yy + rh + 2, 940, yy + rh + 2, LINE, 1))
    yy = ty + 10 + len(INIT) * rh
    b.append(text(120, yy + 32, "合計", 18, INK, 700) + text(760, yy + 32, f"{tot:,}円", 18, INK, 700, "end") + text(900, yy + 32, "100%", 18, INK, 700, "end"))
    gak = INIT[0][1] + INIT[1][1]
    b.append(rect(966, 310, 186, 270, ACC_L, ACC, 10))
    b.append(lines(984, 344, ["入学金と学費で", f"{gak // 10000}万円"], 18, INK, 1.5))
    b.append(text(1059, 432, f"{gak / tot * 100:.0f}%", 40, ACC, 700, "middle"))
    b.append(lines(984, 476, ["総額の約8割が", "入学金と学費。", "まずはここを", "大学ごとに確認。"], 15, INK2, 1.45))
    return svg("".join(b), "大学4年間の費用の内訳（シミュの初期値の例）",
               "自宅外通学の家賃・生活費は含まない（4年で300〜500万円ほど上乗せが多い）。金額は目安。")


FIGS = [
    dict(svg=fig1, alt="大学4年間の学費（入学金と授業料など）の目安を比べた横棒グラフ。国公立は約240〜250万円、私立文系は約400万円（国公立より約150万円高い）、私立理系は約540万円（約300万円高い）、医歯薬系はさらに高額。ほかに教科書・通学費・交際費や、自宅外なら家賃・生活費が4年で300〜500万円かかる。",
         caption="大学4年間の学費の目安。国公立と私立で大きく違い、私立理系は国公立の2倍以上になる。"),
    dict(svg=fig2, alt="大学4年間の費用の内訳を帯グラフと表で示した図。入学金25万円、学費100万円×4年＝400万円、教科書・PC・学用品30万円、通学定期・交通費40万円、サークル・交際費40万円で合計535万円になり、入学金と学費が約8割を占める。",
         caption="4年間の費用の内訳（シミュの初期値の例）。総額の約8割を入学金と学費が占める。"),
]
