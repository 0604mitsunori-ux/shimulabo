"""遺伝の規則性（mendel-iden・中3）の授業用の図。
数値はページ（scripts/rika/sims_ryushi_iden.py）と同じ：卵細胞・精細胞が A／a を 1/2 ずつ受けつぐ → AA：Aa：aa＝1：2：1、丸：しわ＝3：1。
数が少ないときのずれは、しわの数（二項分布 n, 1/4）がおよそ95％で入る範囲を下で計算する。メンデルの結果は 丸5,474・しわ1,850。"""
import math
from figlib import *

PEA, PEA_D, PEA_W, PEA_WD = "#d4e05c", "#71801c", "#b9bf5a", "#5f6420"   # シミュの種子の色（丸・しわ）


def seed(x, y, r, rnd, ph=0.0):
    """シミュと同じ形の種子。rnd=True が丸、False がしわ（ふちが波打つ）"""
    if rnd:
        return (circle(x, y, r, PEA, PEA_D, max(1.6, r / 8))
                + f'<ellipse cx="{x - r * 0.35:.1f}" cy="{y - r * 0.38:.1f}" rx="{r * 0.3:.1f}" ry="{r * 0.2:.1f}" transform="rotate(-34 {x - r * 0.35:.1f} {y - r * 0.38:.1f})" fill="#fff" fill-opacity=".55"/>')
    pts = []
    for i in range(28):
        a = i / 28 * 2 * math.pi
        rr = r * (0.88 + 0.12 * math.sin(a * 6 + ph))
        pts.append(f"{x + math.cos(a) * rr:.1f},{y + math.sin(a) * rr:.1f}")
    out = f'<polygon points="{" ".join(pts)}" fill="{PEA_W}" stroke="{PEA_WD}" stroke-width="{max(1.6, r / 8):.1f}" stroke-linejoin="round"/>'

    def arc(cx, cy, R, a0, a1):
        x0, y0, x1, y1 = cx + R * math.cos(a0), cy + R * math.sin(a0), cx + R * math.cos(a1), cy + R * math.sin(a1)
        return f'<path d="M{x0:.1f},{y0:.1f} A{R:.1f},{R:.1f} 0 0 1 {x1:.1f},{y1:.1f}" fill="none" stroke="#505418" stroke-opacity=".8" stroke-width="{max(1.2, r / 11):.1f}"/>'
    return out + arc(x - r * 0.25, y + r * 0.05, r * 0.45, -1.0, 0.9) + arc(x + r * 0.3, y - r * 0.1, r * 0.35, 2.2, 4.0)


def gamete(x, y, g, r=18):
    """生殖細胞（遺伝子を1つもつ）。A＝朱、a＝藍"""
    c, f = (ACC, ACC_L) if g == "A" else (TEAL, TEAL_L)
    return circle(x, y, r, f, c, 2) + text(x, y + 7, g, 20, c, 700, "middle")


def binom_range(n, p=0.25, lo_q=0.025, hi_q=0.975):
    """しわの数（二項分布）がおよそ95％で入る範囲（ページの表と同じ）"""
    lg = math.lgamma
    pmf = lambda i: math.exp(lg(n + 1) - lg(i + 1) - lg(n - i + 1) + i * math.log(p) + (n - i) * math.log(1 - p))
    acc, cdf = 0.0, []
    for i in range(n + 1):
        acc += pmf(i); cdf.append(acc)
        if acc > hi_q: break
    lo = next(i for i, v in enumerate(cdf) if v >= lo_q)       # P(X≦lo)≧2.5% となる最小
    hi = next(i for i, v in enumerate(cdf) if v >= hi_q)       # P(X≦hi)≧97.5% となる最小（20個→2〜9個）
    return lo, hi


def fig1():
    b = []
    # 左の行ラベル
    for y, t, s in [(140, "親（純系）", ""), (228, "生殖細胞", "（減数分裂）"), (318, "子", ""), (410, "生殖細胞", "（減数分裂）"), (512, "孫", "")]:
        b.append(text(60, y + 6, t, 18, INK, 700))
        if s: b.append(text(60, y + 28, s, 14, MUTED))
    b.append(line(186, 104, 186, 592, LINE, 1.4))
    # 親
    b.append(seed(300, 140, 26, True) + text(338, 137, "AA", 24, INK, 700) + text(338, 161, "丸い種子", 16, INK2))
    b.append(text(452, 151, "×", 30, MUTED, 700, "middle"))
    b.append(seed(540, 140, 26, False, 1) + text(578, 137, "aa", 24, INK, 700) + text(578, 161, "しわのある種子", 16, INK2))
    # 生殖細胞（親）
    b.append(arrow(300, 170, 300, 206, "muted", 2) + arrow(540, 170, 540, 206, "muted", 2))
    b.append(gamete(300, 228, "A") + gamete(540, 228, "a"))
    # 受精 → 子
    b.append(arrow(312, 244, 396, 296, "muted", 2) + arrow(528, 244, 438, 296, "muted", 2))
    b.append(text(420, 268, "受精", 15, MUTED, 700, "middle"))
    b.append(seed(418, 318, 26, True) + text(456, 314, "Aa", 24, INK, 700) + text(456, 338, "すべて丸（顕性の形質）", 16, INK2))
    # 生殖細胞（子）
    b.append(arrow(404, 346, 368, 390, "muted", 2) + arrow(432, 346, 468, 390, "muted", 2))
    b.append(gamete(358, 410, "A") + gamete(478, 410, "a"))
    b.append(text(512, 406, "A：a＝1：1", 18, ACC, 700) + text(512, 430, "Aとaが分かれて入る", 15, INK2))
    # 孫
    b.append(arrow(418, 434, 418, 474, "muted", 2))
    b.append(text(406, 462, "自家受粉（子どうし）", 15, MUTED, 700, "end"))
    xs = [283, 373, 463, 553]
    for x, g, rd, ph in zip(xs, ["AA", "Aa", "Aa", "aa"], [True, True, True, False], [0, 1, 2, 3]):
        b.append(seed(x, 512, 24, rd, ph))
        b.append(text(x, 560, g, 19, INK, 700, "middle"))
        b.append(text(x, 584, "丸" if rd else "しわ", 16, INK2 if rd else ACC, 700 if not rd else 400, "middle"))
    b.append(text(598, 506, "丸：しわ", 17, INK, 700) + text(598, 540, "＝3：1", 28, ACC, 700))
    b.append(text(230, 614, "4つの組み合わせは、どれも同じ確率（1/4ずつ）で起こる", 15, MUTED))
    # 右：ことばのまとめ
    x0, w = 740, 412
    boxes = [("顕性の形質と潜性の形質", ["純系どうしをかけ合わせたとき、", "子に現れる形質（丸）＝顕性の形質", "子に現れない形質（しわ）＝潜性の形質", "Aは丸の遺伝子、aはしわの遺伝子。"]),
             ("分離の法則", ["対になっている遺伝子（Aとa）は、", "生殖細胞がつくられるとき（減数分裂）", "に分かれて、別々の生殖細胞に入る。"]),
             ("しわの遺伝子は消えていない", ["子（Aa）の中に、aは受けつがれている。", "aをもつ生殖細胞どうしが受精した孫", "（aa）で、しわが再び現れる。"])]
    y = 104
    for i, (t, rows) in enumerate(boxes):
        h = 52 + len(rows) * 25
        b.append(rect(x0, y, w, h, CARD, LINE, 10))
        b.append(f'<rect x="{x0}" y="{y}" width="6" height="{h}" rx="3" fill="{[TEAL, ACC, GOLD][i]}"/>')
        b.append(text(x0 + 22, y + 32, t, 18, INK, 700))
        b.append(lines(x0 + 22, y + 60, rows, 16, INK2, 1.55))
        y += h + 14
    return svg("".join(b), "エンドウの種子の形の遺伝（分離の法則）",
               "A＝丸（顕性）の遺伝子、a＝しわ（潜性）の遺伝子。種子の絵は模式図。")


def fig2():
    b = []
    # 左：かけ合わせの表
    gx, gy, cw, ch = 160, 196, 170, 118
    b.append(text(48, 124, "子（Aa）× 子（Aa）→ 孫", 19, INK, 700))
    b.append(text(gx + cw, 148, "精細胞（花粉）の遺伝子 →", 15, MUTED, 700, "middle"))
    b.append(gamete(gx + cw / 2, 174, "A", 16) + gamete(gx + cw * 1.5, 174, "a", 16))
    b.append(text(48, 206, "卵細胞の", 15, MUTED, 700) + text(48, 228, "遺伝子 ↓", 15, MUTED, 700))
    b.append(gamete(130, gy + ch / 2, "A", 16) + gamete(130, gy + ch * 1.5, "a", 16))
    GT = [["AA", "Aa"], ["Aa", "aa"]]
    for r in range(2):
        for c in range(2):
            x, y, g = gx + c * cw, gy + r * ch, GT[r][c]
            rd = g != "aa"
            b.append(rect(x, y, cw, ch, CARD if rd else ACC_L, LINE, 0, 1.4))
            b.append(seed(x + 42, y + 52, 22, rd, r * 2 + c))
            b.append(text(x + 76, y + 50, g, 24, INK, 700))
            b.append(text(x + 76, y + 76, "（丸）" if rd else "（しわ）", 16, INK2 if rd else ACC, 700 if not rd else 400))
            b.append(text(x + cw - 12, y + ch - 12, "1/4", 15, MUTED, anchor="end"))
    b.append(rect(gx, gy, cw * 2, ch * 2, "none", INK2, 0, 1.6))
    b.append(text(48, 476, "AA：Aa：aa＝1：2：1", 20, INK, 700))
    b.append(text(48, 512, "丸：しわ＝（1＋2）：1＝3：1", 22, ACC, 700))
    b.append(text(48, 544, "丸い種子のうち、AAは1/3、Aaは2/3（約67%）。", 16, INK2))
    b.append(lines(48, 576, ["例：孫が800個なら、しわは約200個、丸は約600個", "　　（丸のうち AA 約200個・Aa 約400個）"], 16, INK2, 1.45))
    # 右：数とずれ
    X0, U = 716, 26                      # 比 0 の位置と 1 あたりの長さ
    rx = lambda v: X0 + v * U
    b.append(text(600, 124, "数が少ないと、3：1からずれる", 19, INK, 700))
    b.append(text(600, 148, "しわの数がおよそ95%の確率で入る範囲（丸：しわ の比）", 15, MUTED))
    rows_y = [204, 260, 316, 372]
    top, bot = 184, 454
    for v in range(0, 11):
        b.append(line(rx(v), top, rx(v), bot, LINE, 1))
        b.append(text(rx(v), bot + 22, str(v), 14, INK2, anchor="middle"))
    b.append(line(rx(3), top - 6, rx(3), bot, ACC, 2, "6 4"))
    b.append(text(rx(3), top - 10, "3：1", 15, ACC, 700, "middle"))
    fr = lambda v: f"{v:.1f}".rstrip("0").rstrip(".")
    b.append(line(X0, bot, rx(10), bot, INK, 1.4))
    b.append(text(rx(5), bot + 46, "しわを1としたときの丸の数", 14, MUTED, anchor="middle"))
    for y, n in zip(rows_y, [20, 100, 1000, 10000]):
        lo, hi = binom_range(n)
        r0, r1 = (n - hi) / hi, (n - lo) / lo
        b.append(text(600, y + 6, f"孫 {n:,}個", 17, INK, 700))
        b.append(f'<rect x="{rx(r0):.1f}" y="{y - 9}" width="{max(3, rx(r1) - rx(r0)):.1f}" height="18" rx="4" fill="{TEAL_L}" stroke="{TEAL}" stroke-width="1.6"/>')
        b.append(circle(rx(3), y, 4.5, ACC, ACC, 0))
        b.append(text(990, y - 2, f"しわ {lo:,}〜{hi:,}個", 15, INK, 700))
        b.append(text(990, y + 18, f"{fr(r0)}：1 〜 {fr(r1)}：1", 14, INK2))
    # メンデルの結果
    y = 428; R, Wr = 5474, 1850; m = R / Wr
    st = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5; rr = 11 if i % 2 == 0 else 5
        st.append(f"{rx(m) + math.cos(a) * rr:.1f},{y + math.sin(a) * rr:.1f}")
    b.append(text(600, y + 6, f"メンデル", 17, GOLD, 700))
    b.append(f'<polygon points="{" ".join(st)}" fill="{GOLD}"/>')
    b.append(text(990, y - 2, f"{R + Wr:,}個", 15, GOLD, 700))
    b.append(text(990, y + 18, f"{m:.2f}：1", 14, GOLD, 700))
    b.append(text(600, 540, "・数を増やすほど、範囲がせまくなり 3：1 に近づく。", 16, INK2))
    b.append(text(600, 568, f"・メンデルは丸 {R:,}個・しわ {Wr:,}個（{m:.2f}：1）を得た。", 16, INK2))
    b.append(text(600, 596, "・少ない数で3：1にならなくても、失敗ではない。", 16, INK2))
    return svg("".join(b), "かけ合わせの表と「3：1」になる理由",
               "卵細胞も精細胞も、Aとaが1：1でつくられる。だから4つのマスは同じ確率（1/4）で起こる。")


FIGS = [
    dict(svg=fig1, alt="エンドウの種子の形の遺伝を示す図。丸い種子（AA）としわのある種子（aa）の純系をかけ合わせると子（Aa）はすべて丸（顕性の形質）になり、子の生殖細胞ではAとaが分かれ（分離の法則）、自家受粉でできた孫は AA・Aa・Aa・aa となって丸：しわ＝3：1になることを、顕性・潜性・分離の法則の説明とともに示している。",
         caption="親→子→孫で遺伝子がどう受けつがれるか。対になった遺伝子は生殖細胞に分かれて入り（分離の法則）、孫で丸：しわ＝3：1になる。"),
    dict(svg=fig2, alt="子（Aa）どうしのかけ合わせの表（AA・Aa・Aa・aa、AA：Aa：aa＝1：2：1、丸：しわ＝3：1）と、孫の数が20個・100個・1,000個・10,000個のときに丸：しわの比がおよそ95%の確率で入る範囲をくらべたグラフ。メンデルの結果（7,324個で2.96：1）も示している。",
         caption="かけ合わせの表で3：1になる理由と、調べる数によるずれ。数を増やすほど3：1に近づく。"),
]
