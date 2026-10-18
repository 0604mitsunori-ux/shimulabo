"""歯車シミュレーター（gears）の図。
ページの JS と同じ関係：従動車の回転数 = 原動車の回転数 × 原動車の歯数 ÷ 従動車の歯数、速度伝達比 = 従動車の歯数 ÷ 原動車の歯数、
かみ合う歯車は逆向きに回る（JS では左の角度 +a、右の角度 -a×t1/t2）。"""
import math
from figlib import *

ANCHOR = r"<h2>ギア比のしくみ</h2>\s*<p>.*?</p>\s*"


def gear(cx, cy, n, r, rot, fill, stroke, deco=False):
    """歯数 n・ピッチ円の半径 r の歯車（モジュール m＝2r/n、歯先＋m、歯底－1.25m）。rot＝1枚目の歯の中心の角度（ラジアン）"""
    m = 2 * r / n; ra, rr = r + m, r - 1.25 * m; p = 2 * math.pi / n
    pts = []
    for i in range(n):
        a = rot + p * i
        for da, rad in ((-0.30, rr), (-0.15, ra), (0.15, ra), (0.30, rr)):
            pts.append((cx + rad * math.cos(a + da * p), cy + rad * math.sin(a + da * p)))
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z"
    out = f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="2" stroke-linejoin="round"/>'
    if deco:
        out += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r * 0.62:.1f}" fill="none" stroke="{stroke}" stroke-width="1" stroke-dasharray="4 5" opacity=".6"/>'
    out += circle(cx, cy, max(7, r * 0.12), BG, stroke, 2)
    return out


def turn(cx, cy, R, a0, a1, color="ink", cw=True):
    """歯車のまわりの回る向きの矢印（角度は度・画面の時計回りが正）"""
    c = {"ink": INK, "teal": TEAL, "acc": ACC, "gold": GOLD}[color]
    x0, y0 = cx + R * math.cos(math.radians(a0)), cy + R * math.sin(math.radians(a0))
    x1, y1 = cx + R * math.cos(math.radians(a1)), cy + R * math.sin(math.radians(a1))
    large = 1 if abs(a1 - a0) > 180 else 0
    return (f'<path d="M{x0:.1f},{y0:.1f} A{R},{R} 0 {large} {1 if cw else 0} {x1:.1f},{y1:.1f}" fill="none" '
            f'stroke="{c}" stroke-width="3" marker-end="url(#ah-{color})"/>')


def mesh_rot(rot_a, n_a, phi, n_b):
    """歯車A（rot_a・n_a歯）と、Aの中心から角度 phi の向きにかみ合う歯車B（n_b歯）の rot。Aの歯の所にBのすきまが来るように合わせる"""
    s = (phi - rot_a) / (2 * math.pi / n_a)
    sb = 0.5 - s
    return phi + math.pi - (2 * math.pi / n_b) * sb


def pair(x1, cy, n1, n2, k):
    """左（n1歯）と右（n2歯）をかみ合わせて描く。k＝1歯あたりのピッチ円の半径(px)。右の中心のxを返す"""
    r1, r2 = n1 * k, n2 * k
    x2 = x1 + r1 + r2
    g = gear(x1, cy, n1, r1, 0.0, TEAL_L, TEAL)                      # 左：歯の中心が右（かみ合う所）を向く
    g += gear(x2, cy, n2, r2, mesh_rot(0.0, n1, 0.0, n2), GOLD_L, GOLD)  # 右：かみ合う所に歯のすきま
    return g, x2


def fig1():
    n1, n2, rpm = 24, 12, 60
    rpm2 = rpm * n1 / n2; ratio = n2 / n1
    k = 5.4; cy = 372; x1 = 205
    r1, r2 = n1 * k, n2 * k; m = 2 * k
    g, x2 = pair(x1, cy, n1, n2, k)
    b = [g]
    R1, R2 = r1 + m + 20, r2 + m + 20
    b.append(turn(x1, cy, R1, 200, 290, "teal", cw=True))
    b.append(turn(x2, cy, R2, 330, 230, "gold", cw=False))
    b.append(text(x1, cy - R1 - 34, "原動車（回す側）", 18, TEAL_D, 700, "middle"))
    b.append(text(x1, cy - R1 - 10, f"{n1}歯・時計回り", 16, INK, anchor="middle"))
    b.append(text(x2 + 20, cy - R2 - 34, "従動車（回される側）", 18, GOLD, 700, "middle"))
    b.append(text(x2 + 20, cy - R2 - 10, f"{n2}歯・反時計回り", 16, INK, anchor="middle"))
    b.append(text(x1, cy + 52, f"{rpm}rpm", 22, TEAL_D, 700, "middle"))
    b.append(text(x2, cy + 34, f"{rpm2:.0f}rpm", 17, GOLD, 700, "middle"))
    cxp = x1 + r1
    b.append(line(cxp, cy + 18, cxp + 40, cy + 150, MUTED, 1.4, "4 4"))
    b.append(lines(cxp + 44, cy + 156, ["かみ合う所では、", "両方の歯が同じ数ずつ進む"], 15, INK2))
    # 右：計算のしかた
    X = 640
    b.append(rect(X, 112, 512, 112, CARD, LINE, 10))
    b.append(badge(X + 28, 146, "1", TEAL))
    b.append(text(X + 52, 152, "回る向き", 18, INK, 700))
    b.append(text(X + 52, 186, "かみ合う歯車は、たがいに反対向きに回る。", 16, INK2))
    b.append(text(X + 52, 210, "（3つつなぐと、3つ目は1つ目と同じ向き）", 15, MUTED))
    b.append(rect(X, 238, 512, 112, CARD, LINE, 10))
    b.append(badge(X + 28, 272, "2", TEAL))
    b.append(text(X + 52, 278, "回転数は、歯数の逆の比", 18, INK, 700))
    b.append(text(X + 52, 312, f"原動車が1回転＝{n1}歯ぶん進む", 16, INK2))
    b.append(text(X + 52, 336, f"→ {n2}歯の従動車は {n1}÷{n2}＝{n1 // n2}回転", 16, INK2))
    b.append(rect(X, 364, 512, 232, GOLD_L, GOLD, 10, 1.4))
    b.append(badge(X + 28, 398, "3", GOLD))
    b.append(text(X + 52, 404, "計算のしかた（中学校 技術）", 18, INK, 700))
    b.append(lines(X + 24, 440, ["速度伝達比 ＝ 従動車の歯数 ÷ 原動車の歯数",
                                 "　　　　　 ＝ 原動車の回転数 ÷ 従動車の回転数"], 16.5, INK, 1.5))
    b.append(lines(X + 24, 502, ["従動車の回転数",
                                 "＝ 原動車の回転数 × 原動車の歯数 ÷ 従動車の歯数"], 16.5, INK, 1.5))
    b.append(text(X + 24, 572, f"例：{rpm} × {n1} ÷ {n2} ＝ {rpm2:.0f}rpm（速度伝達比 {n2}÷{n1}＝{ratio:g}）", 17, ACC, 700))
    return svg("".join(b), "かみ合う歯車の回る向きと回転数",
               "rpm＝1分間に回る回数。歯数が半分の歯車は2倍の速さで、反対向きに回る。")


def fig2():
    n1, n2, n3, rpm = 12, 18, 24, 60
    k = 4.2; cy = 250; x1 = 108
    r1, r2, r3 = n1 * k, n2 * k, n3 * k; m = 2 * k
    x2 = x1 + r1 + r2; x3 = x2 + r2 + r3
    rot2 = mesh_rot(0.0, n1, 0.0, n2); rot3 = mesh_rot(rot2, n2, 0.0, n3)
    b = [gear(x1, cy, n1, r1, 0.0, TEAL_L, TEAL, False), gear(x2, cy, n2, r2, rot2, CARD, MUTED, False), gear(x3, cy, n3, r3, rot3, GOLD_L, GOLD, False)]
    for x, r, cw, col, a0, a1 in [(x1, r1, True, "teal", 200, 290), (x2, r2, False, "ink", 300, 240), (x3, r3, True, "gold", 200, 290)]:
        b.append(turn(x, cy, r + m + 14, a0, a1, col, cw=cw))
    rpm2 = rpm * n1 / n2; rpm3 = rpm * n1 / n3
    for x, nm, n, col in [(x1, "原動車", n1, TEAL_D), (x2, "まん中", n2, INK2), (x3, "従動車", n3, GOLD)]:
        b.append(text(x, cy - 16, nm, 15, col, 700, "middle"))
        b.append(text(x, cy + 30, f"{n}歯", 15, INK, anchor="middle"))
    for x, r, s_ in [(x1, r1, f"{rpm}rpm"), (x2, r2, f"{rpm2:.0f}rpm"), (x3, r3, f"{rpm3:.0f}rpm")]:
        b.append(text(x, 392, s_, 17, INK, 700, "middle"))
    X = 580
    b.append(text(X, 128, "歯車を3つつなぐと", 19, INK, 700))
    b.append(lines(X, 166, ["・まん中の歯車（アイドラー）は、回る向きを変えるだけ。",
                            "・右はしの回転数は、両はしの歯数だけで決まる。",
                            f"　{rpm} × {n1} ÷ {n3} ＝ {rpm3:.0f}rpm（まん中の歯数を変えても同じ）",
                            "・1つ目と3つ目は同じ向き（時計回り）、",
                            "　まん中だけ反対向き（反時計回り）に回る。"], 16, INK2, 1.6))
    b.append(text(48, 436, "速度伝達比と、回る速さ・回す力の関係", 19, INK, 700))
    rows = [["1より小さい（例 0.5）", "速くなる", "小さくなる", "24歯 → 12歯：60rpm → 120rpm"],
            ["1（歯数が同じ）", "同じ", "同じ", "24歯 → 24歯：60rpm → 60rpm"],
            ["1より大きい（例 2）", "ゆっくりになる", "大きくなる", "20歯 → 40歯：60rpm → 30rpm"]]
    b.append(table(48, 452, ["速度伝達比", "従動車の回り方", "回す力（トルク）", "例（原動車の歯数 → 従動車の歯数）"], rows,
                   [250, 200, 200, 454], 41, 16))
    return svg("".join(b), "歯車を3つつなぐとき／速度伝達比の早見表",
               "回す力は摩擦を無視した場合。回転をゆっくりにするほど、回す力は大きくなる。")


FIGS = [
    dict(svg=fig1, alt="かみ合う歯車のしくみの図。24歯の原動車が時計回りに60rpmで回ると、12歯の従動車は反対向きの反時計回りに120rpmで回ることと、速度伝達比＝従動車の歯数÷原動車の歯数、従動車の回転数＝原動車の回転数×原動車の歯数÷従動車の歯数の計算式を示す。",
         caption="かみ合う歯車は反対向きに回り、回転数は歯数の逆の比になる（24歯→12歯なら2倍の速さ）。"),
    dict(svg=fig2, alt="12歯・18歯・24歯の歯車を3つつないだ図で、まん中の歯車は回る向きを変えるだけで、右はしの回転数は両はしの歯数で決まる（60rpm→30rpm）ことを示し、速度伝達比が1より小さい・1・1より大きいときの回る速さと回す力（トルク）の変化をまとめた早見表。",
         caption="歯車を3つつなぐとき、まん中の歯車は向きを変えるだけ。速度伝達比が大きいほどゆっくり・力強く回る。"),
]
