"""模試判定シミュレーター（moshi-hantei）の図。
式・区切りはページの JS と同じ：偏差値 h = 50 + 10×(得点−平均)÷標準偏差、d = h − 志望校偏差値、
A: d≥3 / B: d≥0 / C: d≥−3 / D: d≥−6 / E: それ未満。例はシミュの初期値（62点・平均55・標準偏差15・志望校58）。"""
from figlib import *

ANCHOR = r'<div class="note"><strong>計算式</strong>.*?</div>\s*<p>.*?</p>\n'
SCORE, MEAN, SD, GOAL = 62, 55, 15, 58
CUTS = [("A", 3), ("B", 0), ("C", -3), ("D", -6)]       # 差がこの値以上ならその判定


def hensa(score, mean=MEAN, sd=SD):
    return 50 + 10 * (score - mean) / sd


def judge(h, goal=GOAL):
    d = h - goal
    for r, c in CUTS:
        if d >= c:
            return r
    return "E"


def score_of(h, mean=MEAN, sd=SD):
    """偏差値 h になる得点"""
    return mean + sd * (h - 50) / 10


def num(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


ZONE_FILL = {"A": "#d6e6ee", "B": "#eef3f6", "C": "#f6eedc", "D": "#fbeae6", "E": "#f2d6cf"}


def fig1():
    b = []
    h = hensa(SCORE); r = judge(h)
    # ①
    b.append(rect(48, 100, 1104, 122, CARD, LINE, 10))
    b.append(badge(78, 136, "1", TEAL, "#fff", 17) + text(106, 143, "偏差値を出す", 19, INK, 700))
    b.append(text(290, 143, "偏差値 ＝ 50 ＋ 10 ×（得点 − 平均点）÷ 標準偏差", 20, INK, 700))
    b.append(text(106, 195, f"例）{SCORE}点・平均{MEAN}点・標準偏差{SD} → 50 ＋ 10 × {SCORE - MEAN} ÷ {SD} ＝", 18, INK2))
    b.append(text(600, 197, f"偏差値 {h:.1f}", 26, TEAL, 700))
    # ②
    b.append(badge(78, 268, "2", TEAL, "#fff", 17) + text(106, 275, f"志望校の偏差値との差で判定する（志望校が偏差値{GOAL}のとき）", 19, INK, 700))
    lo, hi, x0, x1 = GOAL - 12, GOAL + 8, 90, 1110
    px = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)
    edges = [lo, GOAL - 6, GOAL - 3, GOAL, GOAL + 3, hi]
    names = ["E", "D", "C", "B", "A"]
    zy, zh = 366, 80
    for i, nm in enumerate(names):
        a, c = px(edges[i]), px(edges[i + 1])
        b.append(f'<rect x="{a:.1f}" y="{zy}" width="{c - a:.1f}" height="{zh}" fill="{ZONE_FILL[nm]}" stroke="{CARD}" stroke-width="2"/>')
        b.append(text((a + c) / 2, zy + 54, nm, 36, INK, 700, "middle"))
    for v in edges[1:-1]:
        d = v - GOAL
        b.append(line(px(v), zy - 10, px(v), zy + zh + 4, INK, 2))
        b.append(text(px(v), zy - 44, f"偏差値{v}", 16, INK2, anchor="middle"))
        b.append(text(px(v), zy - 18, "差 0（志望校）" if d == 0 else f"差 {d:+d}".replace("-", "−"), 16, INK, 700, "middle"))
    b.append(text(px(lo) + 4, zy + zh + 30, "← 低い", 15, MUTED))
    b.append(text(px(hi) - 4, zy + zh + 30, "高い →", 15, MUTED, anchor="end"))
    # あなたの位置
    mx = px(h)
    b.append(line(mx, zy + 4, mx, zy + zh, ACC, 3, "5 4"))
    b.append(f'<path d="M{mx:.1f},{zy + zh + 2} l-12,24 h24z" fill="{ACC}"/>')
    b.append(text(mx, zy + zh + 62, f"{SCORE}点 → 偏差値{h:.1f}（差 {h - GOAL:.1f}）→ {r}判定".replace("-", "−"), 19, ACC, 700, "middle"))
    # 一言
    step = SD * 3 / 10
    b.append(rect(48, 548, 1104, 58, TEAL_L, TEAL_L, 10))
    b.append(text(70, 584, f"判定1段階の幅は偏差値3 ＝ 標準偏差{SD}のテストなら {num(step)}点ぶん（標準偏差 × 0.3 点）。"
                  f"{SCORE}点の人は あと{num(score_of(GOAL - 3) - SCORE)}点で C判定。", 17, INK, 700))
    return svg("".join(b), "模試判定のしくみ（偏差値と志望校の差で決まる）",
               "このシミュは、偏差値と志望校の偏差値の差だけで A〜E を出す目安です。")


def fig2():
    b = []
    b.append(text(55, 126, f"例：志望校の偏差値{GOAL}、テストの平均{MEAN}点・標準偏差{SD}（シミュの初期値）", 18, INK, 700))
    adv = {"A": "ケアレスミス対策", "B": "得点を安定させる", "C": "苦手分野を集中的に", "D": "基礎固めから着実に", "E": "計画的に積み上げる"}
    rows = []
    bounds = [None, 3, 0, -3, -6, None]          # 上の境目, 下の境目（差）
    for i, r in enumerate("ABCDE"):
        top, bot = bounds[i], bounds[i + 1]
        if top is None:
            diff, hs, sc = f"+{bot}以上", f"{GOAL + bot}以上", f"{num(score_of(GOAL + bot))}点以上"
        elif bot is None:
            diff, hs, sc = f"{top}より下", f"{GOAL + top}未満", f"{num(score_of(GOAL + top))}点未満"
        else:
            diff = f"{bot:+d}〜{top:+d}未満".replace("+0", "0")
            hs = f"{GOAL + bot}〜{GOAL + top}未満"
            sc = f"{num(score_of(GOAL + bot))}〜{num(score_of(GOAL + top))}点未満"
        rows.append([r, diff.replace("-", "−"), hs, sc, adv[r]])
    cw = [100, 230, 230, 250, 280]
    b.append(table(55, 146, ["判定", "志望校との差", f"偏差値（志望校{GOAL}）", "得点の目安", "今やること"], rows, cw, 58, 18))
    # 判定の列に色
    for i, r in enumerate("ABCDE"):
        b.append(f'<rect x="57" y="{146 + 58 * (i + 1) + 1}" width="{cw[0] - 2}" height="56" fill="{ZONE_FILL[r]}"/>'
                 + text(55 + cw[0] / 2, 146 + 58 * (i + 1) + 38, r, 24, INK, 700, "middle"))
    b.append(text(55, 540, "判定の区切りと合格可能性の％は模試の会社によってちがう。", 16, INK2))
    b.append(text(55, 600, f"得点の目安 ＝ 平均 ＋ 標準偏差 ×（偏差値 − 50）÷ 10　例）偏差値61 → {MEAN} ＋ {SD} × 11 ÷ 10 ＝ {num(score_of(61))}点", 16, INK, 700))
    return svg("".join(b), "A〜E判定の目安（早見表）",
               "A判定でも油断は禁物、E判定でもあきらめる必要はない。判定は「今の位置」。")


FIGS = [
    dict(svg=fig1,
         alt="模試判定のしくみの図。偏差値＝50＋10×（得点−平均点）÷標準偏差で偏差値を出し（62点・平均55点・標準偏差15で54.7）、志望校の偏差値58との差が＋3以上ならA、0以上B、−3以上C、−6以上D、それより下がE判定になることを数直線で示す。",
         caption="模試判定のしくみ。偏差値を出して、志望校の偏差値との差（+3・0・−3・−6）でA〜Eに分ける。"),
    dict(svg=fig2,
         alt="模試のA〜E判定の早見表。志望校の偏差値58・平均55点・標準偏差15のとき、各判定になる志望校との差・偏差値・得点の目安と、今やることをまとめた表。",
         caption="A〜E判定の早見表（志望校の偏差値58の例）。判定の区切りと合格可能性の％は模試の会社によってちがう。"),
]
