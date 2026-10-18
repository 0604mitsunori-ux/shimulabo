"""先祖の人数 計算（senzo-ninzu）の図。式はページの JS と同じ：n代前＝2^n 人、1〜n代前の合計＝2^(n+1)−2 人、何年前＝n×30年。"""
from figlib import *

ANCHOR = r'<div class="note" style="border-left:4px solid var\(--teal\)">.*?</div>\n'
YEAR = 2026      # ページの JS と同じ基準年
GEN_Y = 30       # 1世代の年数（ページの初期値）


def jp_big(n):
    """1,048,576 → 約104万 のような切り捨て（ページの早見表と同じ書き方）"""
    if n < 100000:
        return f"{n:,}"
    if n < 10 ** 8:
        return f"約{n // 10 ** 4:,}万"          # 104.8万→約104万（ページの早見表と同じ）
    return f"約{n / 10 ** 8:.1f}億"


def supt(x, y, parts, size, fill=INK, weight=700, anchor="start"):
    """上付き文字入りの1行。parts＝[(文字, 上付きか)]"""
    w = ' font-weight="700"' if weight >= 700 else ""
    out, up = [], False
    for s, sup in parts:
        if sup and not up:
            out.append(f'<tspan dy="{-size * 0.42:.1f}" font-size="{size * 0.62:.1f}">{esc(s)}</tspan>'); up = True
        elif not sup and up:
            out.append(f'<tspan dy="{size * 0.42:.1f}" font-size="{size}">{esc(s)}</tspan>'); up = False
        elif sup:
            out.append(f'<tspan font-size="{size * 0.62:.1f}">{esc(s)}</tspan>')
        else:
            out.append(f'<tspan>{esc(s)}</tspan>')
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}"{w}>{"".join(out)}</text>'


def node(x, y, male, s=24, label=None):
    """家系図の人：男性＝四角（藍）、女性＝丸（朱）"""
    if male:
        o = f'<rect x="{x - s / 2:.1f}" y="{y - s / 2:.1f}" width="{s}" height="{s}" rx="3" fill="{TEAL}"/>'
    else:
        o = circle(x, y, s / 2, ACC, ACC, 0)
    if label:
        o += text(x, y + s * 0.2, label, int(s * 0.5), "#fff", 700, "middle")
    return o


def fig1():
    b = []
    cx, sp4 = 565, 38                      # 4代前の16人の間隔
    ys = [568, 462, 356, 250, 146]         # あなた・1代前・2代前・3代前・4代前
    sizes = [0, 40, 30, 24, 22]
    xs = {0: [cx]}
    for k in range(1, 5):
        sp = sp4 * 2 ** (4 - k)
        xs[k] = [cx + (i - (2 ** k - 1) / 2) * sp for i in range(2 ** k)]
    # 線（子 → 両親）
    for k in range(0, 4):
        h0 = 34 if k == 0 else sizes[k] / 2
        h1 = sizes[k + 1] / 2
        ym = (ys[k] - h0 + ys[k + 1] + h1) / 2
        for i, x in enumerate(xs[k]):
            fx, mx = xs[k + 1][2 * i], xs[k + 1][2 * i + 1]
            b.append(line(x, ys[k] - h0, x, ym, INK2, 1.6))
            b.append(line(fx, ym, mx, ym, INK2, 1.6))
            b.append(line(fx, ym, fx, ys[k + 1] + h1, INK2, 1.6) + line(mx, ym, mx, ys[k + 1] + h1, INK2, 1.6))
    # さらに上へ続く（点線）
    for x in xs[4]:
        b.append(line(x, ys[4] - 11, x, ys[4] - 24, MUTED, 1.4, "3 3"))
    # 人
    b.append(rect(cx - 62, ys[0] - 34, 124, 68, INK, INK, 12) + text(cx, ys[0] + 8, "あなた", 22, "#fff", 700, "middle"))
    for k in range(1, 5):
        for i, x in enumerate(xs[k]):
            lab = ("父" if i == 0 else "母") if k == 1 else ("祖父" if i % 2 == 0 else "祖母") if k == 2 else None
            b.append(node(x, ys[k], i % 2 == 0, sizes[k], lab if k == 1 else None))
            if k == 2:
                b.append(text(x + (-24 if i % 2 == 0 else 24), ys[k] + 6, lab, 15, INK2, 700, "end" if i % 2 == 0 else "start"))
    # 左の段ラベル
    rows = [("あなた", "1人"), ("1代前（父・母）", "2人"), ("2代前（祖父母）", "4人"),
            ("3代前（曾祖父母）", "8人"), ("4代前（高祖父母）", "16人")]
    for k, (nm, n) in enumerate(rows):
        b.append(text(48, ys[k] - 4, nm, 16, INK2, 700))
        b.append(text(48, ys[k] + 24, n, 24, ACC if k else INK, 700))
    b.append(text(cx, 110, "↑ さらにさかのぼると、1代ごとに2倍に増えていく", 15, MUTED, anchor="middle"))
    # 右：式
    x0 = 880
    b.append(rect(x0, 104, 272, 492, CARD, LINE, 12))
    b.append(text(x0 + 22, 140, "n代前のご先祖", 17, INK2, 700))
    b.append(supt(x0 + 22, 190, [("＝ 2", False), ("n", True), (" 人", False)], 38, ACC))
    b.append(text(x0 + 22, 220, "（2をn回かけた数）", 15, MUTED))
    b.append(line(x0 + 20, 244, x0 + 252, 244, LINE, 1.4))
    b.append(text(x0 + 22, 276, "1代前〜n代前の合計", 17, INK2, 700))
    b.append(supt(x0 + 22, 320, [("＝ 2", False), ("n+1", True), (" − 2 人", False)], 30, TEAL))
    b.append(line(x0 + 20, 346, x0 + 252, 346, LINE, 1.4))
    n = 10
    b.append(text(x0 + 22, 380, f"例：{n}代前（約{n * GEN_Y}年前）", 17, INK, 700))
    b.append(text(x0 + 22, 418, "その代", 16, INK2) + text(x0 + 250, 418, f"{2 ** n:,}人", 22, ACC, 700, "end"))
    b.append(text(x0 + 22, 454, "1〜10代前の合計", 16, INK2) + text(x0 + 250, 454, f"{2 ** (n + 1) - 2:,}人", 22, TEAL, 700, "end"))
    b.append(text(x0 + 22, 490, "あなたを入れると", 16, INK2) + text(x0 + 250, 490, f"{2 ** (n + 1) - 1:,}人", 22, INK, 700, "end"))
    b.append(line(x0 + 20, 514, x0 + 252, 514, LINE, 1.4))
    b.append(text(x0 + 22, 544, f"20代前 → {jp_big(2 ** 20)}人", 17, INK, 700))
    b.append(text(x0 + 22, 576, f"30代前 → {jp_big(2 ** 30)}人", 17, INK, 700))
    b.append(node(700, 566, True, 16) + text(714, 571, "男性", 14, INK2))
    b.append(node(770, 566, False, 16) + text(784, 571, "女性", 14, INK2))
    return svg("".join(b), "先祖の人数のしくみ（1代さかのぼるごとに2倍）",
               "理論上の数。実際は同じ人が何度も登場する（祖先の共有）ため、ご先祖はもっと少なくなる。")


def fig2():
    b = []
    labels = {5: "幕末〜明治", 10: "江戸中期", 15: "戦国", 20: "室町", 25: "鎌倉", 30: "平安"}   # ページの早見表と同じ
    x0, y0, hh, rh = 50, 104, 48, 70
    cw = [140, 290, 250, 270, 150]
    heads = ["世代", "その代のご先祖", "1代前からの合計", "何年前（1世代30年）", "時代の目安"]
    tw_ = sum(cw)
    b.append(rect(x0, y0, tw_, hh + rh * 6, CARD, LINE, 10))
    b.append(f'<rect x="{x0}" y="{y0}" width="{tw_}" height="{hh}" rx="10" fill="{TEAL_L}"/>')
    cx = x0
    for c, w in zip(heads, cw):
        b.append(text(cx + w / 2, y0 + 31, c, 17, INK, 700, "middle")); cx += w
    for i, n in enumerate([5, 10, 15, 20, 25, 30]):
        yy = y0 + hh + rh * i
        if i % 2 == 1:
            b.append(f'<rect x="{x0 + 1}" y="{yy}" width="{tw_ - 2}" height="{rh}" fill="#f7f5ef"/>')
        b.append(line(x0, yy, x0 + tw_, yy, LINE, 1))
        gen, tot, yrs = 2 ** n, 2 ** (n + 1) - 2, n * GEN_Y
        mid = yy + rh / 2
        c = [x0 + sum(cw[:j]) + cw[j] / 2 for j in range(5)]
        b.append(text(c[0], mid + 8, f"{n}代前", 22, INK, 700, "middle"))
        if gen < 100000:
            b.append(text(c[1], mid + 9, f"{gen:,}人", 26, ACC, 700, "middle"))
        else:
            b.append(text(c[1], mid + 2, f"{jp_big(gen)}人", 26, ACC, 700, "middle"))
            b.append(text(c[1], mid + 25, f"（{gen:,}人）", 14, MUTED, anchor="middle"))
        if tot < 100000:
            b.append(text(c[2], mid + 8, f"{tot:,}人", 20, TEAL, 700, "middle"))
        else:
            b.append(text(c[2], mid + 2, f"{jp_big(tot)}人", 20, TEAL, 700, "middle"))
            b.append(text(c[2], mid + 25, f"（{tot:,}人）", 14, MUTED, anchor="middle"))
        b.append(text(c[3], mid + 2, f"約{yrs}年前", 19, INK, 700, "middle"))
        b.append(text(c[3], mid + 25, f"（西暦{YEAR - yrs}年ごろ）", 15, INK2, anchor="middle"))
        b.append(text(c[4], mid + 8, labels[n], 19, INK, 700, "middle"))
    b.append(text(x0, y0 + hh + rh * 6 + 36, "さかのぼるほど当時の人口を超えるのは、同じ人が何度もご先祖として登場する（祖先の共有）ため。", 16, INK2))
    return svg("".join(b), "ご先祖の人数 早見表（5代前〜30代前）",
               "その代＝2のn乗。合計＝1代前からその代までの全員。年数は1世代30年の目安（25年なら少し近くなる）。")


FIGS = [
    dict(svg=fig1, alt="先祖の人数のしくみを示す家系図。あなたから1代前の父母2人、2代前の祖父母4人、3代前の曾祖父母8人、4代前の高祖父母16人と、1代さかのぼるごとにご先祖が2倍になり、n代前のご先祖は2のn乗人（10代前で1,024人）になることを示す。",
         caption="先祖の人数のしくみ。n代前のご先祖は2のn乗人、1代前からの合計は2のn+1乗−2人。"),
    dict(svg=fig2, alt="5代前から30代前までのご先祖の人数の早見表。5代前32人、10代前1,024人、15代前32,768人、20代前約104万人、25代前約3,355万人、30代前約10.7億人と、それぞれの合計人数・何年前か・時代の目安を並べている。",
         caption="ご先祖の人数 早見表。10代前（約300年前・江戸中期）で1,024人、20代前で約104万人。"),
]
