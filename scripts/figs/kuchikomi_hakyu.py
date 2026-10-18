"""口コミ波及（kuchikomi-hakyu）の図。計算はページの JS と同じ：
すすめる確率 pPos(★)＝max(0, 0.10×(★−2.0))、止める確率 pNeg(★)＝max(0, 0.12×(3.5−★))、
増幅率 R＝来店率×話す人数×(pPos − 1.5×pNeg)、月の客 C＝max(0, 基礎＋R×前月)（はじめの前月＝基礎）、12か月。"""
from figlib import *

ANCHOR = r"<strong>計算の考え方</strong>.*?</div>\n"
BASE, TELLS, CONV = 100, 5, 0.10          # シミュの初期値


def p_pos(s): return max(0.0, 0.10 * (s - 2.0))
def p_neg(s): return max(0.0, 0.12 * (3.5 - s))


def model(s, base=BASE, tells=TELLS, conv=CONV):
    R = conv * tells * (p_pos(s) - 1.5 * p_neg(s))
    prev, tot = base, 0.0
    for _ in range(12):
        c = max(0.0, base + R * prev); tot += c; prev = c
    return R, tot - base * 12


def zero_star():
    """すすめる確率＝1.5×止める確率 になる★（0.1(s−2)＝0.18(3.5−s) → s＝0.83/0.28）"""
    lo, hi = 2.0, 3.5
    for _ in range(60):
        m = (lo + hi) / 2
        if p_pos(m) - 1.5 * p_neg(m) < 0: lo = m
        else: hi = m
    return (lo + hi) / 2


def box(x, y, w, h, rows, fill=CARD, stroke=LINE, size=16, color=INK, weight=400):
    out = rect(x, y, w, h, fill, stroke, 10, 1.4)
    n = len(rows); y0 = y + h / 2 - (n - 1) * size * 0.75 + size * 0.36
    for i, r in enumerate(rows):
        out += text(x + w / 2, y0 + i * size * 1.5, r, size, color, weight, "middle")
    return out


def fig1():
    b = []
    # 左：口コミの流れ
    b.append(text(48, 126, "1か月ごとの流れ", 18, INK, 700))
    b.append(box(48, 144, 250, 70, ["口コミ以外の新規客", "（広告・通りがかり など）"], TEAL_L, TEAL, 15))
    b.append(box(48, 254, 250, 60, ["今月のお客さん"], CARD, INK2, 18, INK, 700))
    b.append(arrow(173, 216, 173, 250, "teal", 2.4))
    b.append(box(338, 236, 222, 46, ["満足 → すすめる"], CARD, TEAL, 16, TEAL_D, 700))
    b.append(box(338, 290, 222, 46, ["不満 → 止める"], CARD, ACC, 16, ACC, 700))
    b.append(arrow(300, 276, 334, 262, "ink", 2) + arrow(300, 292, 334, 310, "ink", 2))
    b.append(box(48, 362, 512, 64, ["話を聞いた人（1人が○人に話す）× 来店率", "→ 来月のお客さんが ふえる／へる"], CARD, LINE, 15.5))
    b.append(arrow(449, 338, 449, 358, "ink", 2.2))
    b.append(f'<path d="M48,394 C28,394 28,284 44,284" fill="none" stroke="{MUTED}" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#ah-muted)"/>')
    b.append(text(48, 450, "↑ 毎月くり返す（複利のように積み重なる）", 14, MUTED))
    b.append(rect(48, 476, 512, 132, GOLD_L, GOLD, 10, 1.4))
    b.append(text(68, 504, "計算式（シミュと同じ）", 16, GOLD, 700))
    b.append(lines(68, 536, ["月の集客 ＝ 口コミ以外の新規客 ＋ 前月のお客さん × R",
                             "増幅率 R ＝ 来店率 × 話す人数", "　　　　　×（すすめる確率 − 1.5 × 止める確率）"], 15.5, INK, 1.55))
    # 右：満足度とすすめる・止める確率
    gx, gy, gw, gh = 680, 540, 440, 360
    x = lambda s: gx + (s - 1.0) / 4.0 * gw
    y = lambda v: gy - v / 0.45 * gh
    b.append(text(620, 126, "満足度（★）と口コミの向き", 18, INK, 700))
    z = zero_star()
    b.append(f'<rect x="{gx}" y="{gy - gh}" width="{x(z) - gx:.1f}" height="{gh}" fill="{ACC_L}"/>')
    b.append(f'<rect x="{x(z):.1f}" y="{gy - gh}" width="{gx + gw - x(z):.1f}" height="{gh}" fill="{TEAL_L}"/>')
    b.append(axes(gx, gy, gw, gh, "★", "", [(x(s) - gx, f"{s:.0f}") for s in (1, 2, 3, 4, 5)],
                  [(gy - y(v), f"{v * 100:.0f}%") for v in (0, 0.15, 0.30, 0.45)], 14))
    ss = [1 + i * 0.05 for i in range(81)]
    b.append(poly([(x(s), y(p_pos(s))) for s in ss], TEAL, 3.2))
    b.append(poly([(x(s), y(1.5 * p_neg(s))) for s in ss], ACC, 3.2, dash="8 5"))
    b.append(line(x(z), gy - gh, x(z), gy, INK, 1.6, "4 4"))
    b.append(text(x(z), gy - gh - 10, f"★約{z:.1f}が分かれ目", 15, INK, 700, "middle"))
    b.append(text(x(1.15), y(0.20), "止める力", 15, ACC, 700) + text(x(1.15), y(0.20) + 20, "（止める確率×1.5）", 14, ACC))
    b.append(text(x(4.95), y(0.28) - 14, "すすめる確率", 15, TEAL_D, 700, "end"))
    b.append(text(x(2.0), y(0.08), "逆波及（客がへる）", 15, ACC, 700, "middle"))
    b.append(text(x(4.2), y(0.40), "波及（客がふえる）", 15, TEAL_D, 700, "middle"))
    return svg("".join(b), "口コミ波及のしくみ（満足・不満の広がり方）",
               "不満のお客さんは、満足したお客さんの1.5倍強く広めると仮定している。口コミの広がりを単純化したモデル。")


def fig2():
    b = []
    stars = [1.0, 2.0, 2.5, 3.0, 3.5, 4.0, 4.2, 4.5, 5.0]
    rows = []
    vals = []
    for s in stars:
        R, gap = model(s)
        vals.append(gap)
        rows.append([f"★{s:.1f}" + ("（初期値）" if s == 4.2 else ""), f"{p_pos(s) * 100:.0f}%", f"{p_neg(s) * 100:.0f}%",
                     ("−" if R < 0 else "") + f"{abs(R):.3f}", ""])
    cw = [168, 136, 136, 140, 524]
    b.append(text(48, 124, f"条件：口コミ以外の新規客 月{BASE}人・1人が{TELLS}人に話す・来店率{CONV * 100:.0f}%（シミュの初期値）", 16, INK2))
    ty, rh = 138, 42
    b.append(table(48, ty, ["満足度", "すすめる確率", "止める確率", "増幅率 R", "1年の口コミ効果（口コミなしとの差）"], rows, cw, rh, 16.5))
    x0 = 48 + sum(cw[:4]); xc = x0 + cw[4] / 2; sc = 190 / 224
    b.append(line(xc, ty + rh + 4, xc, ty + rh * (len(rows) + 1) - 4, INK2, 1.4))
    for i, g in enumerate(vals):
        yy = ty + rh * (i + 1) + rh / 2
        wbar = abs(g) * sc
        if g < 0:
            b.append(f'<rect x="{xc - wbar:.1f}" y="{yy - 10}" width="{wbar:.1f}" height="20" fill="{ACC}"/>')
            b.append(text(xc - wbar - 8, yy + 6, f"−{abs(round(g)):,}人", 16, ACC, 700, "end"))
        else:
            b.append(f'<rect x="{xc:.1f}" y="{yy - 10}" width="{wbar:.1f}" height="20" fill="{TEAL}"/>')
            b.append(text(xc + wbar + 8, yy + 6, f"＋{round(g):,}人", 16, TEAL_D, 700))
    b.append(f'<rect x="49" y="{ty + rh * 7 + 1}" width="1102" height="{rh - 2}" fill="none" stroke="{GOLD}" stroke-width="2.4"/>')
    b.append(text(48, 600, "★3.0未満では不満の口コミが勝ち、口コミなしより客がへる（逆波及）。★を上げるほど、口コミで客がふえる。", 16, INK, 700))
    return svg("".join(b), "満足度ごとの口コミ効果（早見表）",
               "1年の口コミ効果＝12か月の客数の合計 −（口コミなしの月100人×12か月）。目安であり、業種・立地で変わる。")


FIGS = [
    dict(svg=fig1, alt="口コミ波及のしくみの図。来店したお客さんが満足すればすすめ、不満なら止める口コミが広がり、話を聞いた人×来店率で翌月の客数が変わることを毎月くり返す流れと計算式、満足度★ごとのすすめる確率と止める力のグラフで★約3.0が波及と逆波及の分かれ目になることを示している。",
         caption="口コミ波及のしくみ。満足度★約3.0を境に、口コミは客をふやす向きにもへらす向きにも働く。"),
    dict(svg=fig2, alt="満足度★1.0〜5.0ごとのすすめる確率・止める確率・増幅率と、1年間の口コミ効果の早見表。口コミ以外の新規客が月100人・1人が5人に話す・来店率10%の場合、★1.0で−224人、★3.0で＋6人、★4.2で＋147人、★5.0で＋209人。",
         caption="満足度ごとの口コミ効果の早見表（シミュの初期値の場合）。★3.0を下回ると逆波及になる。"),
]
