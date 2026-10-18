"""光合成と呼吸（kougousei）の授業用の図。数値は scripts/rika/sims_shokubutsu.py（ページのJS）と同じ式。"""
import math
from figlib import *

# ---- シミュと同じモデル（相対値）
PMAX, KL, R0 = 4.0, 40.0, 1.0
def Pf(L): return PMAX * (1 - math.exp(-L / KL))          # 光合成量（呼吸量は R0=1 で一定）
LC = -KL * math.log(1 - R0 / PMAX)                         # 出入りがつり合う光の強さ（約11.5）
def f1(v): return "%.1f" % (round(v * 10) / 10)
def sg(v): return ("＋" if v > 0.05 else ("−" if v < -0.05 else "±")) + f1(abs(v))
# 蒸散（光の強さ100・6時間）mL：葉の表0.2・裏0.6 mL/時、茎 0.4/6 mL/時
JF, JB, JS = 0.2 * 6, 0.6 * 6, 0.4
JA, JBB, JC, JD = JF + JB + JS, JB + JS, JF + JS, JS

PCOL, RCOL = GREEN, ACC        # 光合成＝緑、呼吸＝朱（文字でも区別する）


def fat(x1, y1, x2, y2, w, color):
    """太さ w の矢印（多角形）"""
    dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L; nx, ny = -uy, ux
    hl, hw = max(16, w * 1.7), max(10, w * 1.25)
    bx, by = x2 - ux * hl, y2 - uy * hl
    pts = [(x1 + nx * w / 2, y1 + ny * w / 2), (bx + nx * w / 2, by + ny * w / 2), (bx + nx * hw, by + ny * hw), (x2, y2),
           (bx - nx * hw, by - ny * hw), (bx - nx * w / 2, by - ny * w / 2), (x1 - nx * w / 2, y1 - ny * w / 2)]
    return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{color}"/>'


def leaf(cx, cy, w=124, h=64, fill="#5fa877", edge="#2f6b45"):
    a, b = w / 2, h
    d = (f"M{cx - a:.1f},{cy:.1f} C{cx - a / 2:.1f},{cy - b:.1f} {cx + a / 2:.1f},{cy - b * 0.72:.1f} {cx + a:.1f},{cy:.1f} "
         f"C{cx + a / 2:.1f},{cy + b * 0.72:.1f} {cx - a / 2:.1f},{cy + b:.1f} {cx - a:.1f},{cy:.1f}Z")
    out = f'<path d="{d}" fill="{fill}" stroke="{edge}" stroke-width="2"/>'
    out += line(cx - a - 14, cy, cx + a - 6, cy, edge, 1.6)
    for k in (1, 2, 3, 4):
        x = cx - a + k * w / 5
        out += line(x, cy, x + w / 10, cy - h * 0.3, edge, 1.1) + line(x, cy, x + w / 10, cy + h * 0.3, edge, 1.1)
    return out


def sun(cx, cy, L):
    if L <= 0:
        return (f'<circle cx="{cx}" cy="{cy}" r="13" fill="{LINE}" stroke="{MUTED}" stroke-width="1.4" stroke-dasharray="3 3"/>'
                + text(cx + 24, cy + 6, "光が当たらない", 15, MUTED, 700))
    out, n, ln_ = [], 12, 5 + 12 * L / 100            # 光が強いほど光線を長く
    for k in range(n):
        q = 2 * math.pi * k / n
        out.append(line(cx + math.cos(q) * 17, cy + math.sin(q) * 17, cx + math.cos(q) * (17 + ln_), cy + math.sin(q) * (17 + ln_), GOLD, 2.2))
    out.append(circle(cx, cy, 13, SUN, GOLD, 1.6))
    return "".join(out)


def card(x, y, no, name, L, bg):
    w, h = 352, 350
    cx, cy = x + w / 2, y + 190
    P, R = Pf(L), R0; n = P - R
    b = [rect(x, y, w, h, bg, LINE, 12)]
    b.append(badge(x + 26, y + 30, no, INK, "#fff", 16) + text(x + 46, y + 37, name, 20, INK, 700))
    b.append(text(x + w - 16, y + 37, "光の強さ " + ("約%.1f" % L if abs(L - round(L)) > 1e-6 else "%d" % L), 16, INK2, anchor="end"))
    b.append(sun(cx - (52 if L <= 0 else 0), y + 84, L))
    b.append(leaf(cx, cy))
    b.append(text(cx, cy + 6, "葉", 17, "#fff", 700, "middle"))
    top, bot = y + 134, y + 248
    # 光合成（左）：二酸化炭素を取り入れ、酸素を出す
    if P > 0.02:
        wP = 3 + 3 * P
        b.append(fat(x + 22, top, cx - 70, cy - 12, wP, PCOL) + fat(cx - 70, cy + 12, x + 22, bot, wP, PCOL))
        b.append(text(x + 16, top - 12, f"二酸化炭素 {f1(P)}", 15, PCOL, 700) + text(x + 16, bot + 26, f"酸素 {f1(P)}", 15, PCOL, 700))
        b.append(text(x + 16, cy + 6, "光合成", 17, PCOL, 700))
    else:
        b.append(line(x + 22, top, cx - 70, cy - 12, MUTED, 2, "6 5") + line(cx - 70, cy + 12, x + 22, bot, MUTED, 2, "6 5"))
        b.append(text(x + 16, cy - 4, "光合成", 15, MUTED, 700) + text(x + 16, cy + 16, "なし", 15, MUTED, 700))
    # 呼吸（右）：酸素を取り入れ、二酸化炭素を出す（いつも同じ量）
    wR = 3 + 3 * R
    b.append(fat(x + w - 22, top, cx + 70, cy - 12, wR, RCOL) + fat(cx + 70, cy + 12, x + w - 22, bot, wR, RCOL))
    b.append(text(x + w - 16, top - 12, f"酸素 {f1(R)}", 15, RCOL, 700, "end") + text(x + w - 16, bot + 26, f"二酸化炭素 {f1(R)}", 15, RCOL, 700, "end"))
    b.append(text(x + w - 16, cy + 6, "呼吸", 17, RCOL, 700, "end"))
    # 差し引き
    word = "酸素を出す" if n > 0.05 else ("二酸化炭素を出す" if n < -0.05 else "出入りがつり合う")
    col = TEAL_D if n > 0.05 else (ACC if n < -0.05 else INK)
    b.append(line(x + 14, y + 288, x + w - 14, y + 288, LINE, 1.4))
    b.append(text(cx, y + 313, f"光合成 {f1(P)} − 呼吸 {f1(R)} ＝ {sg(n)}", 17, INK, 400, "middle"))
    b.append(text(cx, y + 339, "葉全体では → " + word, 19, col, 700, "middle"))
    return "".join(b)


def fig1():
    b = [card(48, 100, "1", "暗いとき（夜）", 0, "#eceef1"),
         card(424, 100, "2", "つり合うとき", LC, "#f6f3ea"),
         card(800, 100, "3", "明るいとき（昼）", 100, "#fbf3df")]
    y0 = 466
    b.append(rect(48, y0, 1104, 150, CARD, LINE, 12))
    b.append(text(72, y0 + 40, "光合成", 20, PCOL, 700) + text(160, y0 + 40, "二酸化炭素 ＋ 水 → デンプンなど ＋ 酸素", 21, INK, 700)
             + text(1128, y0 + 40, "葉緑体で・光のエネルギーを使う（光が当たるときだけ）", 15.5, INK2, anchor="end"))
    b.append(text(72, y0 + 84, "呼吸", 20, RCOL, 700) + text(160, y0 + 84, "デンプンなど ＋ 酸素 → 二酸化炭素 ＋ 水", 21, INK, 700)
             + text(1128, y0 + 84, "すべての細胞で・生きるエネルギーを取り出す（昼も夜も）", 15.5, INK2, anchor="end"))
    b.append(line(72, y0 + 104, 1128, y0 + 104, LINE, 1))
    b.append(text(72, y0 + 132, f"取り入れる気体と出す気体が逆。光の強さが 約{LC:.1f} より強いと、光合成のほうが多くなる（このシミュレーションの値）。", 16, INK2))
    return svg("".join(b), "光合成と呼吸の気体の出入り（光の強さで変わる）",
               "数値はシミュレーションと同じ式の相対値。矢印が太いほど多い。気体は主に葉の気孔から出入りする。")


def sw(col):
    return lambda x, y: circle(x, y, 9, col, INK2, 1.2)


def wbar(v, vmax):
    return lambda x, y: f'<rect x="{x + 16:.1f}" y="{y + 12:.1f}" width="{max(2, 88 * v / vmax):.1f}" height="9" rx="2" fill="{SKY}"/>'


def exp_card(x, y, title, sub, rows, concl):
    w, h = 352, 470
    b = [rect(x, y, w, h, CARD, LINE, 12)]
    b.append(text(x + 18, y + 34, title, 19, INK, 700))
    b.append(text(x + 18, y + 60, sub, 14.5, MUTED))
    yy = y + 78
    for lab, c1, c2, res, mark, tx in rows:
        b.append(line(x + 12, yy, x + w - 12, yy, LINE, 1))
        b.append(badge(x + 30, yy + 30, lab, INK2, "#fff", 15))
        b.append(text(x + 52, yy + 24, c1, 15, INK) + text(x + 52, yy + 46, c2, 15, INK2))
        b.append(mark(x + 236, yy + 29))
        b.append(text(x + tx, yy + 35, res, 16, INK, 700))
        yy += 58
    b.append(line(x + 12, yy, x + w - 12, yy, LINE, 1))
    b.append(rect(x + 12, y + 330, w - 24, 128, TEAL_L, TEAL_L, 8))
    b.append(lines(x + 24, y + 358, concl, 15.5, INK, 1.62))
    return "".join(b)


def fig2():
    b = [text(48, 118, "対照実験：調べたい条件だけを変え、ほかの条件はすべて同じにして、結果をくらべる。", 17, INK2)]
    BLUE, YEL, GRN, PUR, IOD = "#3f6fb5", "#e3c13b", "#4f9a5e", "#4b2a6b", "#d9b97c"
    rows = [("A", "オオカナダモ あり", "光：当てる", "青色", sw(BLUE), 252),
            ("B", "オオカナダモ あり", "光：当てない（はく）", "黄色", sw(YEL), 252),
            ("C", "オオカナダモ なし", "光：当てる", "緑色のまま", sw(GRN), 252),
            ("D", "オオカナダモ なし", "光：当てない（はく）", "緑色のまま", sw(GRN), 252)]
    b.append(exp_card(48, 134, "BTB溶液とオオカナダモ", "息をふきこんで緑色にした液を4本に分ける", rows,
                      ["A と C：ちがうのはオオカナダモだけ", "→ 色の変化はオオカナダモのはたらき", "A と B：ちがうのは光だけ",
                       "→ 光が当たると光合成で二酸化炭素が減る"]))
    rows = [("a", "緑色の部分", "光：当たる", "青紫色", sw(PUR), 252),
            ("b", "ふ（白い部分）", "光：当たる", "変化なし", sw(IOD), 252),
            ("c", "緑色の部分", "光：当たらない（はく）", "変化なし", sw(IOD), 252),
            ("d", "ふ（白い部分）", "光：当たらない（はく）", "変化なし", sw(IOD), 252)]
    b.append(exp_card(424, 134, "ヨウ素液でデンプンを調べる", "ふ入りの葉の一部をアルミはくでおおう", rows,
                      ["a と c：ちがうのは光だけ", "→ デンプンをつくるには光が必要", "a と b：ちがうのは葉緑体があるかだけ",
                       "→ デンプンは緑色の部分でできる"]))
    mx = JA
    rows = [("A", "何もぬらない", "表＋裏＋茎から", f1(JA) + "mL", wbar(JA, mx), 252),
            ("B", "葉の表にワセリン", "裏＋茎から", f1(JBB) + "mL", wbar(JBB, mx), 252),
            ("C", "葉の裏にワセリン", "表＋茎から", f1(JC) + "mL", wbar(JC, mx), 252),
            ("D", "葉をとる", "茎だけから", f1(JD) + "mL", wbar(JD, mx), 252)]
    b.append(exp_card(800, 134, "蒸散（ワセリンでふさぐ）", "減った水の量（光の強さ100・6時間）", rows,
                      [f"葉の裏から ＝ B − D ＝ {f1(JB)}mL", f"葉の表から ＝ C − D ＝ {f1(JF)}mL",
                       "→ 葉の裏からの蒸散が多い", "（気孔は葉の裏側に多い）"]))
    return svg("".join(b), "光合成・蒸散の対照実験（まとめ）",
               "BTB溶液：二酸化炭素が多いと黄色、少ないと青色。ヨウ素液：デンプンがあると青紫色。蒸散の量はシミュレーションの目安。")


FIGS = [
    dict(svg=fig1, alt="光合成と呼吸の気体の出入りを、暗いとき・つり合うとき・明るいときの3枚の葉でくらべた図。光合成は二酸化炭素と水からデンプンと酸素をつくり、呼吸は酸素を取り入れて二酸化炭素を出す。光の強さ0では呼吸だけで二酸化炭素を出し、約11.5でつり合い、100では光合成が多く酸素を出す。",
         caption="光の強さと気体の出入り。光合成と呼吸は気体の出入りが逆で、明るいと光合成のほうが多くなる。"),
    dict(svg=fig2, alt="光合成と蒸散の対照実験のまとめ。BTB溶液とオオカナダモの試験管A〜Dの色、ふ入りの葉をヨウ素液で調べた結果a〜d、ワセリンを使った蒸散の実験A〜Dの減った水の量と、くらべると分かることを並べた表。",
         caption="対照実験のまとめ。ちがう条件が1つだけの2つをくらべると、その条件のはたらきが分かる。"),
]
