"""偏差値計算シミュレーター（hensachi）の図。
式はページの JS と同じ：偏差値 = 50 + 10×(点数−平均)÷標準偏差、上位％ = (1 − Φ((偏差値−50)/10))×100（erf は JS と同じ近似式）、
100人なら順位 = max(1, round(上位％))。例はシミュの初期値（70点・平均60・標準偏差15）。"""
import math
from figlib import *

SQRT2 = math.sqrt(2)

ANCHOR = r'<div class="note"><strong>計算式</strong>.*?</div>\s*<p>.*?</p>\n'
SCORE, MEAN, SD = 70, 60, 15


def erf(t):
    """ページの JS と同じ近似（Abramowitz-Stegun 7.1.26）"""
    s = -1 if t < 0 else 1; t = abs(t)
    a1, a2, a3, a4, a5, p = 0.254829592, -0.284496736, 1.421413741, -1.453152027, 1.061405429, 0.3275911
    u = 1 / (1 + p * t)
    return s * (1 - (((((a5 * u + a4) * u) + a3) * u + a2) * u + a1) * u * math.exp(-t * t))


def hensa(x, m=MEAN, sd=SD):
    return 50 + 10 * (x - m) / sd


def top(h):
    """上位およそ何％（JS：(1-cdf)*100）"""
    z = (h - 50) / 10
    return (1 - 0.5 * (1 + erf(z / SQRT2))) * 100


def rank(h):
    return max(1, math.floor(top(h) + 0.5))      # JS の Math.round


def h_for_top(t):
    """上位 t％ に入る偏差値（top() の逆を二分法で）"""
    lo, hi = 0.0, 100.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if top(mid) > t: lo = mid
        else: hi = mid
    return (lo + hi) / 2


def score_of(h, m=MEAN, sd=SD):
    return m + sd * (h - 50) / 10


def num(v, d=1):
    return f"{v:.{d}f}".rstrip("0").rstrip(".")


def fig1():
    b = []
    h = hensa(SCORE)
    b.append(rect(48, 98, 1104, 92, TEAL_L, TEAL_L, 10))
    b.append(text(70, 134, "偏差値 ＝ 50 ＋ 10 ×（点数 − 平均点）÷ 標準偏差", 21, INK, 700))
    b.append(text(70, 172, f"例）{SCORE}点・平均{MEAN}点・標準偏差{SD} → 50 ＋ 10 × {SCORE - MEAN} ÷ {SD} ＝ 偏差値{h:.1f}（上位 約{top(h):.1f}%）", 18, INK2))
    # 正規分布
    x0, x1, base, peak = 150, 1070, 492, 236
    px = lambda v: x0 + (v - 20) / 60 * (x1 - x0)
    py = lambda v: base - (base - peak) * math.exp(-((v - 50) / 10) ** 2 / 2)
    fills = {(20, 30): "#f3efe6", (30, 40): "#e6eef2", (40, 50): "#d6e6ee", (50, 60): "#d6e6ee", (60, 70): "#e6eef2", (70, 80): "#f3efe6"}
    for (a, c), f in fills.items():
        pts = [(px(a), base)] + [(px(a + (c - a) * i / 40), py(a + (c - a) * i / 40)) for i in range(41)] + [(px(c), base)]
        b.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{f}" stroke="none"/>')
    curve = [(px(20 + 60 * i / 240), py(20 + 60 * i / 240)) for i in range(241)]
    b.append(poly(curve, TEAL_D, 3))
    for a in (30, 40, 60, 70):
        b.append(line(px(a), base, px(a), py(a), "#ffffff", 2))
    p1 = (erf(1 / SQRT2)) / 2 * 100                 # 50〜60 の割合
    p2 = (erf(2 / SQRT2) - erf(1 / SQRT2)) / 2 * 100
    for c, v in [(45, p1), (55, p1), (35, p2), (65, p2)]:
        b.append(text(px(c), base - 26, f"{v:.1f}%", 17, INK, 700, "middle"))
    b.append(line(x0 - 10, base, x1 + 10, base, INK, 1.8))
    for v in range(20, 81, 10):
        b.append(line(px(v), base, px(v), base + 7, INK, 1.4) + text(px(v), base + 28, str(v), 16, INK, 700 if v == 50 else 400, "middle"))
    b.append(text(56, base + 28, "偏差値", 16, INK, 700))
    b.append(text(56, base + 66, f"点数の例", 15, INK2) + text(56, base + 86, f"（平均{MEAN}・標準偏差{SD}）", 14, INK2))
    for v in range(30, 71, 10):
        b.append(text(px(v), base + 66, f"{num(score_of(v))}点", 16, INK2, anchor="middle"))
    # 目印：50・60・70
    b.append(line(px(50), peak - 4, px(50), peak - 18, INK, 1.4) + text(px(50), peak - 26, "平均 ＝ 偏差値50（上位50%）", 16, INK, 700, "middle"))
    for v, dy in [(60, -30), (70, -40)]:
        yy = py(v)
        b.append(f'<path d="M{px(v):.1f},{yy:.1f} L{px(v) + 40:.1f},{yy + dy:.1f} L{px(v) + 52:.1f},{yy + dy:.1f}" fill="none" stroke="{ACC}" stroke-width="1.6"/>')
        b.append(circle(px(v), yy, 4.5, ACC, ACC, 0))
        b.append(text(px(v) + 58, yy + dy - 2, f"偏差値{v}以上", 16, ACC, 700) + text(px(v) + 58, yy + dy + 24, f"上位 約{top(v):.1f}%", 20, ACC, 700))
    return svg("".join(b), "偏差値のしくみ（正規分布と上位％）",
               "上位％は、点数の分布を正規分布と考えた近似。実際のテストの分布によって多少ずれる。")


def fig2():
    b = []
    b.append(text(55, 126, "偏差値 → 上位およそ何％か", 19, INK, 700))
    rows = [[str(v), f"{top(v):.1f}%", f"{rank(v)}位くらい", f"{num(score_of(v))}点"] for v in (75, 70, 65, 60, 55, 50, 45, 40, 35)]
    b.append(table(55, 142, ["偏差値", "上位およそ", "100人なら", "点数の例※"], rows, [120, 160, 160, 160], 45, 17))
    rx = 680
    b.append(text(rx, 126, "上位◯％に入るには？", 19, INK, 700))
    rows2 = []
    for t in (1, 5, 10, 20, 30, 50):
        hv = h_for_top(t)
        rows2.append([f"上位{t}%", f"偏差値 {hv:.1f}", f"{score_of(hv):.1f}点"])
    b.append(table(rx, 142, ["目標", "必要な偏差値", "点数の例※"], rows2, [140, 170, 160], 45, 17))
    b.append(rect(rx, 486, 470, 106, CARD, LINE, 10))
    b.append(lines(rx + 18, 518, [f"※点数の例は 平均{MEAN}点・標準偏差{SD} のテスト。",
                                   "標準偏差が分からないときは 15前後 で概算。",
                                   "偏差値60で上位約16%、70で上位約2%。"], 15.5, INK2, 1.65))
    return svg("".join(b), "偏差値と上位％の早見表",
               "上位％は正規分布を仮定した近似（シミュと同じ計算）。100人なら順位＝上位％を四捨五入（最低1位）。")


FIGS = [
    dict(svg=fig1,
         alt="偏差値のしくみの図。偏差値＝50＋10×（点数−平均点）÷標準偏差の式（70点・平均60点・標準偏差15で偏差値56.7）と、正規分布の山に偏差値20〜80と点数の例を並べ、偏差値40〜60に約68%、偏差値60以上が上位約15.9%、70以上が上位約2.3%であることを示す。",
         caption="偏差値のしくみ。偏差値50が平均で、60以上は上位約16%、70以上は上位約2%（正規分布を仮定）。"),
    dict(svg=fig2,
         alt="偏差値と上位％の早見表。偏差値35〜75について上位およそ何％か・100人中の順位・平均60点標準偏差15のテストでの点数と、上位1%・5%・10%・20%・30%・50%に入るのに必要な偏差値と点数をまとめた表。",
         caption="偏差値と上位％の早見表。上位10%に入るには偏差値約62.8、上位1%なら約73.3が目安。"),
]
