"""うちの海抜チェッカー（kaibatsu-check）の図。海抜と標高の違い／海抜の目安とハザードマップの浸水深の色。
数値の正：ページの JS（海抜の4区分 0m未満・5m未満・20m未満・20m以上）と、国土交通省「水害ハザードマップ作成の手引き」
（令和8年5月版 図3-3：浸水深 0.5m・3m・5m・10m・20m の6段階と標準RGB、0.5m＝1階床高・3m＝2階床下・5m＝2階が水没）。"""
from figlib import *

ANCHOR = r"海抜とは？標高との違い</h2>.*?</table></div>\n"

GROUND, GROUND_D, SEA, SEA_D = "#e3d8bf", "#b9a983", "#d6e8f1", "#7fb3d5"
# 浸水深の標準色（手引き 図3-3）
D_COL = {"20": "rgb(220,122,220)", "10": "rgb(242,133,201)", "5": "rgb(255,145,145)",
         "3": "rgb(255,183,183)", "0.5": "rgb(255,216,192)", "0": "rgb(247,245,169)"}


def house(x, base, w=44, h=34, fill=CARD):
    """小さい家（x＝左端、base＝地面のy）"""
    return (rect(x, base - h, w, h, fill, INK, 0, 1.6)
            + f'<path d="M{x - 5},{base - h} L{x + w / 2},{base - h - 22} L{x + w + 5},{base - h}Z" fill="{fill}" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>'
            + rect(x + w / 2 - 6, base - 18, 12, 18, "#d9d2c3", INK, 0, 1.2))


def dbl(x, y1, y2, color="acc", width=2.4):
    """両向き矢印（y1→y2 と y2→y1）"""
    c = {"acc": ACC, "teal": TEAL, "ink": INK}[color]
    return line(x, y1, x, y2, c, width, arrow=color) + line(x, y2, x, y1, c, width, arrow=color)


def fig1():
    y0, k = 500, 7.4                      # 東京湾平均海面（0m）の y と 1m あたりの px（高さは強調した模式図）
    hw, lw = y0 - 22, y0 + 22             # 満潮・干潮の海面（模式）
    plat = y0 - 15 * k                    # 例：海抜15m の台地
    low = 512                             # 海抜ゼロメートル地帯の地面（0m より低い）
    b = []
    # 海
    b.append(f'<rect x="48" y="{hw}" width="300" height="{620 - hw}" fill="{SEA}"/>')
    wave = " ".join(f"{48 + i * 12},{hw + (3 if i % 2 else -3)}" for i in range(0, 26))
    b.append(f'<polyline points="{wave}" fill="none" stroke="{TEAL}" stroke-width="2"/>')
    b.append(line(48, lw, 300, lw, TEAL, 1.6, "6 5"))
    b.append(text(58, hw - 12, "満潮のときの海面", 15, TEAL_D, 700))
    b.append(text(58, lw + 24, "干潮のときの海面", 15, TEAL_D, 700))
    # 地面（堤防 → ゼロメートル地帯 → 坂 → 台地）
    pts = [(300, 620), (322, 440), (352, 440), (374, low), (520, low), (604, plat), (1152, plat), (1152, 620)]
    b.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{GROUND}" stroke="{GROUND_D}" stroke-width="2" stroke-linejoin="round"/>')
    b.append(text(337, 430, "堤防", 15, INK, 700, "middle"))
    # 基準面（0m）
    b.append(line(48, y0, 1152, y0, INK, 2, "10 6"))
    b.append(text(1146, y0 + 26, "東京湾平均海面（T.P.）＝ 0m", 17, INK, 700, "end"))
    # ゼロメートル地帯の家
    for x in (392, 452):
        b.append(house(x, low))
    b.append(rect(380, 300, 226, 78, CARD, ACC, 8, 1.6))
    b.append(text(392, 326, "海抜ゼロメートル地帯", 17, ACC, 700))
    b.append(lines(392, 350, ["満潮の海面より低い土地。", "堤防で守られている"], 15, INK2))
    b.append(line(470, 378, 470, 450, ACC, 1.6, arrow="acc"))
    # 台地の家：海抜＝標高
    b.append(house(644, plat, 52, 40))
    b.append(dbl(626, y0, plat + 2, "acc"))
    b.append(text(640, plat + 40, "海抜 15m", 18, ACC, 700))
    b.append(text(640, plat + 64, "＝ 標高 15m", 18, ACC, 700))
    b.append(text(640, plat + 86, "（例）", 14, INK2))
    # ビル：高さ（比高）
    top = plat - 30 * k
    b.append(rect(850, top, 74, plat - top, "#eef0f2", INK, 0, 1.8))
    for r in range(8):
        for c in range(3):
            b.append(rect(860 + c * 20, top + 14 + r * 26, 12, 14, "#c9d6df", "none", 0, 0))
    b.append(dbl(944, plat, top + 2, "teal"))
    b.append(text(958, top + 92, "高さ（比高）30m", 18, TEAL, 700))
    b.append(text(958, top + 116, "地面からてっぺんまで", 15, INK2))
    b.append(text(958, top + 140, "（例）", 14, INK2))
    b.append(text(958, top + 18, "てっぺんの標高は", 15, INK2))
    b.append(text(958, top + 40, "15m＋30m＝45m", 16, INK, 700))
    # 説明の枠
    b.append(rect(48, 104, 296, 160, CARD, TEAL, 10, 1.6))
    b.append(text(64, 134, "海抜と標高は同じ高さ", 19, TEAL, 700))
    b.append(lines(64, 164, ["日本ではどちらも、東京湾の", "平均海面（T.P.）を0mとして測る。", "地図・登山では「標高」、", "海辺の看板や防災では「海抜」"], 15.5, INK, 1.6))
    return svg("".join(b), "海抜・標高・高さのちがい（断面図）",
               "模式図（高さ・きょりは実際とちがう／数字は例）。海抜は「土地の高さ」で、浸水の危険そのものではない。")


def fig2():
    b = []
    # 左：海抜の目安（ページの4区分）
    b.append(text(48, 124, "土地の高さ（海抜）ごとの目安", 20, INK, 700))
    b.append(text(48, 148, "海抜だけで安全かどうかは決まらない", 15, ACC, 700))
    rows = [("20m以上", ["津波・高潮の影響は受けにくい高さ。", "ただし、がけ崩れ・土石流の区域は", "高い所に多い"], "→「土砂災害」を確認"),
            ("5〜20m", ["海抜だけでは安全とも危険とも", "言えない。近くの川があふれるか、", "水が集まる地形かどうか"], "→「洪水」の浸水の深さを確認"),
            ("0〜5m", ["海や川に近いと、高潮・津波・洪水の", "想定区域に入っていることがある"], "→ 浸水の深さを確認"),
            ("0m未満", ["海抜ゼロメートル地帯の可能性。", "大雨や高潮のとき水が引きにくい"], "→ 浸水の深さと避難先を必ず確認")]
    y = 162
    for i, (rng, ls, chk) in enumerate(rows):
        h = 108
        b.append(rect(48, y, 548, h, CARD, LINE, 10))
        b.append(f'<rect x="48" y="{y}" width="124" height="{h}" rx="10" fill="{TEAL_L}"/>')
        b.append(text(110, y + h / 2 + 8, rng, 21, TEAL_D, 700, "middle"))
        b.append(lines(186, y + 26, ls, 15.5, INK, 1.4))
        b.append(text(186, y + 26 + len(ls) * 15.5 * 1.4 + 2, chk, 15.5, TEAL, 700))
        y += h + 6
    # 右：浸水深の色（国の標準）と2階建ての家
    X0, X1, g, k = 630, 1152, 590, 67.0
    yd = lambda m: g - m * k
    b.append(text(X0, 124, "浸水の深さ（地面から水面まで）の色", 20, INK, 700))
    b.append(text(X0, 148, "ハザードマップの国の標準の色分け", 15, MUTED))
    # 10m・20m（家の図には入らない深さ）
    b.append(text(X0, 181, "さらに深い区分：", 15.5, INK2))
    for j, (key, lab) in enumerate([("10", "10〜20m"), ("20", "20m以上")]):
        xx = X0 + 134 + j * 170
        b.append(rect(xx, 162, 34, 26, D_COL[key], "#9a8f8f", 4, 1))
        b.append(text(xx + 44, 181, lab, 16, INK, 700))
    bands = [("0", 0, 0.5), ("0.5", 0.5, 3), ("3", 3, 5), ("5", 5, 5.85)]
    for key, m0, m1 in bands:
        b.append(f'<rect x="{X0}" y="{yd(m1):.1f}" width="{X1 - X0}" height="{yd(m0) - yd(m1):.1f}" fill="{D_COL[key]}"/>')
    for m in (0.5, 3, 5):
        b.append(line(X0, yd(m), X1, yd(m), INK2, 1.4, "6 4"))
        b.append(text(X1 - 6, yd(m) - 6, f"{m:g}m", 15, INK, 700, "end"))
    b.append(line(X0, g, X1, g, INK, 2.4))
    b.append(text(X1 - 6, g + 22, "地面（0m）", 14, INK2, anchor="end"))
    # 2階建ての家（1階の床0.5m・2階の床3m・2階の軒5m）
    hx0, hx1 = 664, 800
    b.append(rect(hx0 + 6, yd(0.5), hx1 - hx0 - 12, yd(0) - yd(0.5), "#b8b1a4", INK, 0, 1.4))
    b.append(f'<rect x="{hx0}" y="{yd(5):.1f}" width="{hx1 - hx0}" height="{yd(0.5) - yd(5):.1f}" fill="none" stroke="{INK}" stroke-width="2.4"/>')
    b.append(line(hx0, yd(3), hx1, yd(3), INK, 4))
    b.append(line(hx0, yd(0.5), hx1, yd(0.5), INK, 4))
    b.append(f'<path d="M{hx0 - 12},{yd(5):.1f} L{(hx0 + hx1) / 2},{yd(5.8):.1f} L{hx1 + 12},{yd(5):.1f}Z" fill="none" stroke="{INK}" stroke-width="2.4" stroke-linejoin="round"/>')
    for fl in (0.5, 3):
        b.append(rect(hx0 + 16, yd(fl + 1.7), 36, 40, "none", INK, 0, 1.6))
        b.append(rect(hx1 - 52, yd(fl + 1.7), 36, 40, "none", INK, 0, 1.6))
    b.append(text((hx0 + hx1) / 2, yd(0.5) - 10, "1階の床", 14, INK, 700, "middle"))
    b.append(text((hx0 + hx1) / 2, yd(3) - 10, "2階の床", 14, INK, 700, "middle"))
    # 区分の説明
    tx = 826
    b.append(text(tx, yd(5) - 14, "5〜10m：2階が水没する深さ", 16, INK, 700))
    b.append(text(tx, yd(4) + 2, "3〜5m", 18, INK, 700))
    b.append(text(tx, yd(4) + 26, "2階の床より上まで", 16, INK))
    b.append(text(tx, yd(1.75) - 4, "0.5〜3m", 18, INK, 700))
    b.append(text(tx, yd(1.75) + 20, "1階の床より上まで", 16, INK))
    b.append(text(tx, yd(1.75) + 42, "（床上浸水）", 16, INK))
    b.append(text(tx, yd(0.25) + 6, "0.5m未満：床下浸水ていど", 15.5, INK, 700))
    return svg("".join(b), "海抜の目安と、ハザードマップの浸水の色",
               "浸水の色は国土交通省「水害ハザードマップ作成の手引き」の標準。家の高さは一般的な2階建ての目安。")


FIGS = [
    dict(svg=fig1, alt="海抜と標高の違いを示す断面図。海抜と標高はどちらも東京湾平均海面（T.P.）を0mとして測る同じ高さで、高さ（比高）は地面から建物のてっぺんまでの高さ。満潮の海面より低い海抜ゼロメートル地帯が堤防で守られている様子も描いている。",
         caption="海抜・標高・高さのちがい。海抜と標高はどちらも東京湾の平均海面を0mとした「土地の高さ」。"),
    dict(svg=fig2, alt="海抜の目安（20m以上・5〜20m・0〜5m・0m未満）ごとにハザードマップで確認すべきこと（土砂災害・洪水・浸水の深さ・避難先）と、ハザードマップの浸水深の色分け（0.5m未満・0.5〜3m・3〜5m・5〜10m・10〜20m・20m以上）を2階建ての家の高さと比べた図。",
         caption="海抜の目安と浸水の深さの色。0.5mで1階の床、3mで2階の床に届き、5mで2階が水没する。"),
]
