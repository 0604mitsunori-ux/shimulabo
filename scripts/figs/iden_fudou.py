"""遺伝的浮動とハーディー・ワインベルグの法則（iden-fudou・高校生物）の授業用の図。
図1の折れ線は、ページのシミュ（scripts/rika/sims_kou_kagaku_seibutsu.py の FUDOU_JS）と同じ乱数（mulberry32）・
同じ二項分布の取り出し方（ライト・フィッシャーのモデル）をそのまま Python に写して計算している。
「乱数：固定 No.1」・p₀＝0.5・100世代・選択なし・びん首なしで、N＝10 と N＝1000 の最初の8集団と一致する（node で照合済み）。"""
import math
from figlib import *

M32 = 0xFFFFFFFF


def _imul(a, b): return (a * b) & M32


def mulberry(a):
    st = [a & M32]

    def r():
        a = (st[0] + 0x6D2B79F5) & M32; st[0] = a
        t = _imul(a ^ (a >> 15), 1 | a)
        t = ((t + _imul(t ^ (t >> 7), 61 | t)) & M32) ^ t
        return ((t ^ (t >> 14)) & M32) / 4294967296
    return r


def run_drift(seed, N, p0=0.5, G=100, s=0.0, K=8):
    """シミュの runDrift と同じ（びん首なし）。戻り値：[(各世代の p のリスト, 固定・消失した世代 or -1), ...]"""
    R = mulberry(seed * 1000003 + 1)

    def gauss():
        u = 0
        while not u: u = R()
        v = 0
        while not v: v = R()
        return math.sqrt(-2 * math.log(u)) * math.cos(2 * math.pi * v)

    def binom(n, p):
        if p <= 0: return 0
        if p >= 1: return n
        if p > 0.5: return n - binom(n, 1 - p)
        if n * p < 25:
            lq = math.log(1 - p); x = i = 0
            while True:
                i += math.floor(math.log(1 - R()) / lq) + 1
                if i > n: return x
                x += 1
        m = n * p
        return max(0, min(n, math.floor(m + math.sqrt(m * (1 - p)) * gauss() + 0.5)))   # Math.round と同じ
    pops = []
    for _ in range(K):
        p = p0; a = [p]; ab = -1
        for g in range(1, G + 1):
            ps = p * (1 + s) / (1 + p * s); p = binom(2 * N, ps) / (2 * N); a.append(p)
            if ab < 0 and p in (0, 1): ab = g
        pops.append((a, ab))
    return pops


LINE_COLS = [TEAL, ACC, GOLD, GREEN, PURPLE, SKY, TEAL_D, INK2]


def gene(x, y, g, r=12):
    c = ACC if g == "A" else TEAL
    return circle(x, y, r, c, c, 0) + text(x, y + 5, g, 15, "#fff", 700, "middle")


def drift_graph(N, top, bot, x0=520, x1=1120, G=100):
    pops = run_drift(1, N, 0.5, G, 0, 8)
    gx = lambda g: x0 + g / G * (x1 - x0)
    py = lambda p: bot - p * (bot - top)
    b = []
    fx = sum(1 for a, ab in pops if ab >= 0 and a[ab] == 1); ls = sum(1 for a, ab in pops if ab >= 0 and a[ab] == 0)
    b.append(text(x0, top - 14, f"N＝{N:,}個体（遺伝子 2N＝{2 * N:,}個）", 17, INK, 700))
    b.append(text(x1, top - 14, f"Aが固定 {fx}・消失 {ls}・両方残る {len(pops) - fx - ls}（8集団）", 15, INK2, anchor="end"))
    b.append(rect(x0, top, x1 - x0, bot - top, CARD, LINE, 0, 1))
    for v, lab in [(1, "1 固定"), (0.5, "0.5"), (0, "0 消失")]:
        b.append(line(x0, py(v), x1, py(v), LINE if v == 0.5 else INK2, 1 if v == 0.5 else 1.3))
        b.append(text(x0 - 8, py(v) + 5, lab, 14, INK2, 700 if v != 0.5 else 400, "end"))
    b.append(line(x0, py(0.5), x1, py(0.5), MUTED, 1.2, "5 4"))
    for g in range(0, G + 1, 20):
        b.append(line(gx(g), bot, gx(g), bot + 5, INK, 1.2))
        b.append(text(gx(g), bot + 21, f"{g}世代" if g == G else str(g), 14, INK2, anchor="middle"))
    for k, (a, ab) in enumerate(pops):
        end = ab if ab >= 0 else G
        b.append(poly([(gx(g), py(a[g])) for g in range(end + 1)], LINE_COLS[k], 2, "none"))
        if ab >= 0: b.append(circle(gx(ab), py(a[ab]), 4.5, LINE_COLS[k], "#fff", 1.4))
    return "".join(b)


def fig1():
    b = [text(48, 118, "遺伝子頻度が偶然で変わるしくみ", 18, INK, 700)]
    # 親の世代 → 子の世代（N＝10・2色のコインのモデル実験と同じ操作）
    par = "AaAaaAaAAaAaAaaAAaaA"            # A 10・a 10
    kid = "AAaAAaAaAAaAAaaAAaAa"            # A 12・a 8（例）
    for y0, title, gs in [(134, "親の世代", par), (304, "子の世代（例）", kid)]:
        nA = gs.count("A")
        b.append(rect(48, y0, 400, 104, CARD, LINE, 10))
        b.append(text(64, y0 + 26, f"{title}　A {nA}個・a {20 - nA}個（p＝{nA / 20:.2f}）", 16, INK, 700))
        for i, g in enumerate(gs):
            b.append(gene(78 + (i % 10) * 36, y0 + 52 + (i // 10) * 30, g))
    b.append(arrow(96, 242, 96, 298, "ink", 2.4))
    b.append(text(116, 264, "20個を無作為に選び直す", 16, INK, 700))
    b.append(text(116, 288, "（どの遺伝子が残るかは偶然）", 15, MUTED))
    sd10, sd1000 = math.sqrt(0.25 / 20), math.sqrt(0.25 / 2000)
    t10 = 4 * 10 * math.log(2)
    b.append(lines(48, 444, ["・集団が小さいほど、1世代のゆれが大きい。",
                             f"　ゆれ √(pq/2N)：N＝10で約{sd10:.2f}、",
                             f"　N＝1000で約{sd1000:.3f}（p＝0.5のとき）",
                             "・やがて固定（p＝1）か消失（p＝0）する。",
                             f"　平均 約2.8N世代（N＝10なら約{t10:.0f}世代）",
                             "・中立なら、Aがいずれ固定する確率＝最初のp"], 16, INK2, 1.5))
    b.append(drift_graph(10, 134, 296))
    b.append(drift_graph(1000, 378, 540))
    return svg("".join(b), "遺伝的浮動のしくみ（集団の大きさと遺伝子頻度の変化）",
               "シミュで p₀＝0.5・100世代・選択なし・乱数「固定 No.1」にしたときの最初の8集団と同じ線（●＝固定・消失した世代）。")


def fig2():
    b = [text(48, 120, "(p＋q)²＝p²＋2pq＋q²＝1", 22, INK, 700)]
    p = 0.6; q = 1 - p
    X, Y, S = 124, 186, 300
    a, c = S * p, S * q
    b.append(text(X + S / 2, 150, "精子の遺伝子 →", 15, MUTED, 700, "middle"))
    b.append(text(X + a / 2, 176, f"A（p＝{p:.1f}）", 16, ACC, 700, "middle") + text(X + a + c / 2, 176, f"a（q＝{q:.1f}）", 16, TEAL, 700, "middle"))
    b.append(text(48, 158, "卵の", 15, MUTED, 700) + text(48, 178, "遺伝子 ↓", 15, MUTED, 700))
    b.append(text(X - 10, Y + a / 2 - 2, "A", 18, ACC, 700, "end") + text(X - 10, Y + a / 2 + 20, f"p＝{p:.1f}", 14, ACC, 700, "end"))
    b.append(text(X - 10, Y + a + c / 2 - 2, "a", 18, TEAL, 700, "end") + text(X - 10, Y + a + c / 2 + 20, f"q＝{q:.1f}", 14, TEAL, 700, "end"))
    cells = [(X, Y, a, a, "AA", f"p²＝{p * p:.2f}", ACC_L), (X + a, Y, c, a, "Aa", f"pq＝{p * q:.2f}", GOLD_L),
             (X, Y + a, a, c, "Aa", f"pq＝{p * q:.2f}", GOLD_L), (X + a, Y + a, c, c, "aa", f"q²＝{q * q:.2f}", TEAL_L)]
    for x, y, w, h, g, v, f in cells:
        b.append(rect(x, y, w, h, f, INK2, 0, 1.4))
        b.append(text(x + w / 2, y + h / 2 - 4, g, 24, INK, 700, "middle"))
        b.append(text(x + w / 2, y + h / 2 + 22, v, 16, INK2, 700, "middle"))
    b.append(text(X + S + 18, Y + 24, "面積が", 15, MUTED) + text(X + S + 18, Y + 44, "その組み合わせ", 15, MUTED) + text(X + S + 18, Y + 64, "の割合", 15, MUTED))
    b.append(text(48, 522, "AA：Aa：aa＝p²：2pq：q²", 18, INK, 700))
    b.append(text(48, 550, f"＝{p * p * 100:.0f}%：{2 * p * q * 100:.0f}%：{q * q * 100:.0f}%（p＝{p:.1f} のとき）", 18, ACC, 700))
    b.append(text(48, 584, "次の世代のAの頻度＝p²＋pq＝p(p＋q)＝p", 16, INK2))
    b.append(text(48, 608, "→ 遺伝子頻度は世代をこえて変わらない", 16, INK2, 700))
    # 右：条件・早見表・計算の例
    x0 = 600
    b.append(rect(x0, 100, 552, 152, CARD, LINE, 10))
    b.append(f'<rect x="{x0}" y="100" width="6" height="152" rx="3" fill="{TEAL}"/>')
    b.append(text(x0 + 22, 128, "法則が成り立つ5つの条件", 18, INK, 700))
    b.append(lines(x0 + 22, 156, ["① 集団が十分に大きい（遺伝的浮動が無視できる）", "② 自由に交配が行われる",
                                  "③ 突然変異が起こらない　④ 移入や移出がない", "⑤ 自然選択がはたらかない"], 16, INK2, 1.5))
    b.append(text(x0, 290, "早見表：遺伝子頻度と遺伝子型頻度", 17, INK, 700))
    rows = []
    for pp in [0.9, 0.8, 0.7, 0.6, 0.5, 0.99]:
        qq = round(1 - pp, 10); d = 4 if pp == 0.99 else 2
        rows.append([f"{pp:g}", f"{qq:g}", f"{pp * pp:.{d}f}", f"{2 * pp * qq:.{d}f}", f"{qq * qq:.{d}f}"])
    b.append(table(x0, 304, ["p（A）", "q（a）", "AA（p²）", "Aa（2pq）", "aa（q²）"], rows, [100, 100, 116, 120, 116], 33, 16))
    b.append(lines(x0, 572, ["計算の例：aa が16%なら q²＝0.16 → q＝0.4、p＝0.6、", "Aa＝2×0.6×0.4＝0.48（顕性の形質の個体84%のうち約57%）"], 15, INK2, 1.5))
    return svg("".join(b), "ハーディー・ワインベルグの法則（まとめ）",
               "親の遺伝子型の割合がどうであっても、遺伝子頻度が p・q なら1世代の自由な交配で p²：2pq：q² になる。")


FIGS = [
    dict(svg=fig1, alt="遺伝的浮動のしくみの図。親の世代の遺伝子プール（A 10個・a 10個）から20個を無作為に選び直すと子の世代の遺伝子頻度が偶然で変わることと、集団の大きさN＝10とN＝1000で、8つの集団の対立遺伝子Aの頻度pが100世代でどう変化するかをくらべた折れ線グラフ。小さい集団ほど早く固定・消失する。",
         caption="遺伝的浮動のしくみ。集団が小さいほど遺伝子頻度が偶然で大きくゆれ、早く固定・消失する。"),
    dict(svg=fig2, alt="ハーディー・ワインベルグの法則のまとめ図。配偶子の組み合わせを面積で表した表（p＝0.6のとき AA p²＝0.36・Aa 2pq＝0.48・aa q²＝0.16）、法則が成り立つ5つの条件、遺伝子頻度pと遺伝子型頻度の早見表、潜性ホモ接合体の割合から遺伝子頻度を求める計算の例。",
         caption="ハーディー・ワインベルグの法則。遺伝子型頻度は p²：2pq：q² になり、条件が成り立てば遺伝子頻度は変わらない。"),
]
