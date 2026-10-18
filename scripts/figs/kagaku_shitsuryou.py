"""化学変化と質量（kagaku-shitsuryou）の授業用の図
数値はシミュ（scripts/rika/sims_denki_kagaku.py の JS_KAGAKU）と同じ式で計算する：
  質量の比 銅：酸素＝4：1（r=0.25）、マグネシウム：酸素＝3：2（r=2/3）。1回の加熱で反応する割合 銅0.7・マグネシウム0.8。
  密閉した容器：反応前 82.46 g、二酸化炭素 0.52 g（炭酸水素ナトリウム1.00 g）。"""
import math
import re
from figlib import *

# シミュの MET / RX と同じ値
MET = {"cu": dict(nm="銅", r=0.25, a=4, b=1, p=0.7, lst=[0.4, 0.6, 0.8, 1.0, 1.2, 1.4]),
       "mg": dict(nm="マグネシウム", r=2 / 3, a=3, b=2, p=0.8, lst=[0.3, 0.6, 0.9, 1.2, 1.5])}
RX_M0, RX_GAS = 82.46, 0.52
CU, MG, OX, CC, NA, CL = GOLD, MUTED, ACC, INK, PURPLE, GREEN


def r2(v):      # シミュの r2（Math.round(v*100+1e-7)/100）
    return math.floor(v * 100 + 1e-7 + 0.5) / 100


def heat_reads(k, m):
    """加熱した回数ごとの電子てんびんの値（シミュの applyHeat と同じ。一定になったら止める）"""
    M = MET[k]; reads = [r2(m)]; n = 0
    while True:
        n += 1; f = 1 - (1 - M["p"]) ** n; rd = r2(m * (1 + M["r"] * f)); reads.append(rd)
        if n >= 2 and rd == reads[n - 1]: return reads


def oxy(k, m):      # シミュの batch()：結びついた酸素の質量
    return r2(r2(m * (1 + MET[k]["r"])) - r2(m))


def chem(x, y, s, size=20, fill=INK, weight=400, anchor="start"):
    """化学式。_2 / _{2} は下付き、^+ / ^{2+} は上付き（tspan の dy でずらす）"""
    sub = max(14, round(size * 0.7)); cur = 0.0; out = []
    for t in re.findall(r"_\{[^}]*\}|_\d+|\^\{[^}]*\}|\^[+\-−]|[^_^]+", s):
        if t[0] in "_^":
            body = (t[2:-1] if t[1] == "{" else t[1:]).replace("-", "−")
            tgt = size * 0.28 if t[0] == "_" else -size * 0.42
            out.append(f'<tspan dy="{tgt - cur:.1f}" font-size="{sub}">{esc(body)}</tspan>'); cur = tgt
        else:
            out.append(f'<tspan dy="{-cur:.1f}">{esc(t)}</tspan>' if cur else esc(t)); cur = 0.0
    w = ' font-weight="700"' if weight >= 700 else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}"{w}>{"".join(out)}</text>'


def atom(cx, cy, r, sym, fill, tc="#fff", size=None):
    return (circle(cx, cy, r, fill, INK, 1.2)
            + text(cx, cy + (size or max(14, r * 0.8)) * 0.36, sym, size or max(14, round(r * 0.8)), tc, 700, "middle"))


def bottle(cx, top, lid, liquid=TEAL_L):
    """密閉できる容器（首・肩・胴）。top＝首の上端"""
    nk, bw, sh, bot = 15, 46, top + 22, top + 98
    d = (f"M{cx - nk},{top} L{cx - nk},{top + 10} Q{cx - nk},{sh} {cx - bw},{sh + 12} L{cx - bw},{bot - 8} Q{cx - bw},{bot} {cx - bw + 8},{bot} "
         f"L{cx + bw - 8},{bot} Q{cx + bw},{bot} {cx + bw},{bot - 8} L{cx + bw},{sh + 12} Q{cx + nk},{sh} {cx + nk},{top + 10} L{cx + nk},{top}")
    out = [f'<path d="{d}" fill="#f4f8fa" stroke="{TEAL}" stroke-width="2"/>',
           f'<rect x="{cx - bw + 3}" y="{bot - 30}" width="{2 * bw - 6}" height="27" rx="6" fill="{liquid}"/>']
    if lid:
        out.append(rect(cx - nk - 4, top - 12, 2 * nk + 8, 13, TEAL, TEAL, 3, 0))
    return "".join(out), bot


def balance(cx, y, val):
    return (rect(cx - 74, y, 148, 44, "#e9e5db", "#cfc9ba", 8)
            + rect(cx - 52, y + 7, 104, 30, INK, INK, 5, 0)
            + text(cx + 44, y + 29, val, 19, "#fff", 700, "end"))


def co2(cx, cy, al=1.0):
    s = f'<g opacity="{al}">' + circle(cx - 11, cy, 6.5, OX, INK, 0.8) + circle(cx + 11, cy, 6.5, OX, INK, 0.8) + circle(cx, cy, 7, CC, INK, 0.8) + "</g>"
    return s


def fig1():
    b = []
    # ---------- 左：質量保存の法則 ----------
    L0, L1 = 48, 568; lc = (L0 + L1) / 2
    b.append(rect(L0, 100, L1 - L0, 516, CARD, LINE, 12))
    b.append(text(L0 + 20, 132, "① 質量保存の法則（密閉した容器の反応）", 19, INK, 700))
    b.append(chem(lc, 174, "NaHCO_3 ＋ HCl → NaCl ＋ H_2O ＋ CO_2", 22, INK, 700, "middle"))
    b.append(text(lc, 200, "炭酸水素ナトリウム＋塩酸 → 塩化ナトリウム＋水＋二酸化炭素", 14.5, INK2, anchor="middle"))
    b.append(table(L0 + 30, 214, ["原子の数", "Na", "H", "C", "O", "Cl"],
                   [["反応前", "1こ", "2こ", "1こ", "3こ", "1こ"], ["反応後", "1こ", "2こ", "1こ", "3こ", "1こ"]],
                   [130, 64, 64, 64, 64, 64], 32, 16))
    xs = [L0 + 100, L0 + 260, L0 + 420]; top = 368
    for i, (cx, lid, val) in enumerate([(xs[0], True, RX_M0), (xs[1], True, RX_M0), (xs[2], False, r2(RX_M0 - RX_GAS))]):
        s, bot = bottle(cx, top, lid, TEAL_L)
        b.append(s)
        if i == 0:      # 反応前：小さい試験管に塩酸、底に炭酸水素ナトリウム
            b.append(f'<rect x="{cx + 8}" y="{top + 30}" width="14" height="58" rx="6" fill="#fff" stroke="{TEAL}" stroke-width="1.4" transform="rotate(-12 {cx + 15} {top + 88})"/>')
            b.append(f'<ellipse cx="{cx - 18}" cy="{bot - 6}" rx="16" ry="5" fill="#fff" stroke="{MUTED}" stroke-width="1"/>')
        else:           # 反応後：あわ（二酸化炭素）
            for j in range(5):
                b.append(f'<circle cx="{cx - 24 + j * 12}" cy="{bot - 14 - (j % 2) * 7}" r="3" fill="#fff" stroke="{TEAL}" stroke-width="1"/>')
        if i == 1:      # 容器の中の二酸化炭素
            b.append(co2(cx - 10, top + 52) + co2(cx + 18, top + 40))
        b.append(balance(cx, bot, f"{val:.2f} g"))
        if i == 2:      # ふたを開けると出ていく（ふたは電子てんびんの上に置く）
            b.append(rect(cx + 50, bot - 10, 22, 10, TEAL, TEAL, 3, 0))
            b.append(co2(cx + 4, top - 16, 0.9) + co2(cx + 28, top - 38, 0.6))
            b.append(arrow(cx - 28, top + 4, cx - 28, top - 36, "muted", 2))
    b.append(arrow(xs[0] + 62, top + 60, xs[1] - 62, top + 60, "ink", 2.4))
    b.append(arrow(xs[1] + 62, top + 60, xs[2] - 62, top + 60, "ink", 2.4))
    ly = top + 98 + 44 + 24
    b.append(text(xs[0], ly, "反応前", 15, INK, 700, "middle"))
    b.append(text(xs[1], ly, "反応後", 15, INK, 700, "middle") + text(xs[1], ly + 20, "（ふたをしたまま）", 15, INK2, anchor="middle"))
    b.append(text(xs[2], ly, "ふたを開けたあと", 15, INK, 700, "middle"))
    b.append(chem(xs[2], ly + 20, f"CO_2 {RX_GAS:.2f} g が外へ", 15, ACC, 700, "middle"))
    b.append(text(lc, 600, "原子の種類と数は変わらない → 質量の総和は変わらない", 17, TEAL_D, 700, "middle"))

    # ---------- 右：金属の酸化と質量の比 ----------
    R0, R1 = 592, 1152
    b.append(rect(R0, 100, R1 - R0, 516, CARD, LINE, 12))
    b.append(text(R0 + 20, 132, "② 金属を加熱する（酸素と結びつく）", 19, INK, 700))
    rows = [("cu", "Cu", CU, 18, "2Cu ＋ O_2 → 2CuO", "（酸化銅・黒色）", "銅原子1この質量は、酸素原子1この約4倍"),
            ("mg", "Mg", MG, 17, "2Mg ＋ O_2 → 2MgO", "（酸化マグネシウム・白色）", "マグネシウム原子1この質量は、酸素原子1この約1.5倍")]
    for j, (k, sym, col, ra, eq, oxn, why) in enumerate(rows):
        y0 = 150 + j * 158; ay = y0 + 36; ro = 12
        b.append(rect(R0 + 14, y0, R1 - R0 - 28, 146, "#fbfaf6", LINE, 10))
        x = R0 + 30 + ra
        b.append(atom(x, ay, ra, sym, col, size=15) + atom(x + 2 * ra + 6, ay, ra, sym, col, size=15))
        x2 = x + 2 * ra + 6 + ra + 18
        b.append(text(x2, ay + 7, "＋", 20, INK, 700, "middle"))
        b.append(atom(x2 + 26, ay, ro, "O", OX, size=14) + atom(x2 + 26 + 2 * ro, ay, ro, "O", OX, size=14))
        x3 = x2 + 26 + 2 * ro + ro + 10
        b.append(arrow(x3, ay, x3 + 34, ay, "ink", 2.4))
        x4 = x3 + 46 + ra
        for q in range(2):
            px = x4 + q * (2 * ra + 2 * ro + 12)
            b.append(atom(px, ay, ra, sym, col, size=15) + atom(px + ra + ro, ay, ro, "O", OX, size=14))
        b.append(chem(R0 + 34, y0 + 102, eq, 20, INK, 700) + text(R0 + 214, y0 + 102, oxn, 15, INK2))
        b.append(text(R0 + 34, y0 + 132, why, 15, INK2))
        # 質量の比（■の数）
        M = MET[k]; xr = R1 - 32
        b.append(text(xr, y0 + 22, "結びつく質量の比", 14, MUTED, anchor="end"))
        u = 18; xx = xr - (M["a"] + M["b"]) * (u + 3) - 5
        for i in range(M["a"]): b.append(rect(xx + i * (u + 3), y0 + 32, u, u, col, col, 3, 0))
        xx2 = xx + M["a"] * (u + 3) + 8
        for i in range(M["b"]): b.append(rect(xx2 + i * (u + 3), y0 + 32, u, u, OX, OX, 3, 0))
        b.append(text(xr, y0 + 76, f"{M['nm']}：酸素＝{M['a']}：{M['b']}", 18, INK, 700, "end"))
    # 一定になるわけ（銅原子12こ）
    y0 = 470
    b.append(text(R0 + 20, y0 + 6, "加熱をくり返すと質量が一定になるわけ（銅原子12こ）", 16, INK, 700))
    for s, (nR, lab) in enumerate([(0, "加熱前"), (6, "加熱の途中"), (12, "全部結びついた")]):
        sx = R0 + 30 + s * 178
        b.append(text(sx + 74, y0 + 32, lab, 15, INK, 700, "middle"))
        for i in range(12):
            c, r = i % 6, i // 6
            ax, ay = sx + 12 + c * 25, y0 + 58 + r * 30
            if i < nR: b.append(circle(ax + 11, ay - 7, 6, OX, INK, 0.8))
            b.append(circle(ax, ay, 9.5, CU, INK, 0.8))
        if s < 2: b.append(arrow(sx + 156, y0 + 72, sx + 172, y0 + 72, "muted", 2))
    b.append(text(R0 + 20, 604, "全部の銅原子が酸素と結びつくと、それ以上は重くならない。", 15.5, TEAL_D, 700))
    return svg("".join(b), "化学変化と質量のしくみ（原子のモデル）",
               "化学変化では原子の組み合わせが変わるだけ。原子の大きさ・色は模式的。")


def fig2():
    b = []
    # ---------- 左のグラフ：加熱した回数と質量 ----------
    x0, y0, w, h = 116, 404, 380, 236
    lo, hi = 0.5, 1.1
    gx = lambda n: x0 + n / 6 * w
    gy = lambda v: y0 - (v - lo) / (hi - lo) * h
    b.append(text(60, 124, "加熱した回数と質量", 19, INK, 700))
    b.append(axes(x0, y0, w, h, "", "質量［g］", [(gx(n) - x0, str(n)) for n in range(0, 7)],
                  [(y0 - gy(v), f"{v:.1f}") for v in (0.6, 0.7, 0.8, 0.9, 1.0, 1.1)], 15))
    b.append(f'<path d="M{x0 - 7},{y0 - 10} l7,-4 l7,4" fill="none" stroke="{INK}" stroke-width="1.6"/>'
             f'<path d="M{x0 - 7},{y0 - 16} l7,-4 l7,4" fill="none" stroke="{INK}" stroke-width="1.6"/>')
    b.append(text(x0 + w, y0 + 48, "加熱した回数［回］", 15, INK, anchor="end"))
    b.append(line(x0, gy(1.0), x0 + w, gy(1.0), GREEN, 1.6, "6 5"))
    b.append(text(x0 + w - 4, gy(1.0) - 10, "一定になった（1.00 g）", 15, GREEN, 700, "end"))
    for k, m, col in [("mg", 0.6, MG), ("cu", 0.8, CU)]:
        rd = heat_reads(k, m)
        b.append(poly([(gx(n), gy(v)) for n, v in enumerate(rd)], col, 2.6))
        for n, v in enumerate(rd):
            if k == "cu": b.append(f'<rect x="{gx(n) - 6:.1f}" y="{gy(v) - 6:.1f}" width="12" height="12" fill="{col}" stroke="#fff" stroke-width="1.2"/>')
            else: b.append(circle(gx(n), gy(v), 6.5, col, "#fff", 1.2))
    lx, ly = gx(2.5), gy(0.80)      # 凡例（あいている右下に）
    b.append(f'<rect x="{lx - 6:.1f}" y="{ly - 11:.1f}" width="12" height="12" fill="{CU}"/>' + text(lx + 12, ly, "銅 0.80 g を加熱", 15, "#7d5a18", 700))
    b.append(circle(lx, gy(0.72) - 5, 6.5, MG, MG, 0) + text(lx + 12, gy(0.72), "マグネシウム 0.60 g を加熱", 15, INK2, 700))
    # ---------- 右のグラフ：金属の質量と結びつく酸素の質量 ----------
    X0, Y0, W2, H2, XM, YM = 676, 404, 420, 236, 1.6, 1.0
    px = lambda v: X0 + v / XM * W2
    py = lambda v: Y0 - v / YM * H2
    b.append(text(620, 124, "金属の質量と結びつく酸素の質量", 19, INK, 700))
    b.append(axes(X0, Y0, W2, H2, "", "酸素の質量［g］", [(px(v) - X0, f"{v:.1f}") for v in (0.4, 0.8, 1.2, 1.6)],
                  [(Y0 - py(v), f"{v:.1f}") for v in (0.2, 0.4, 0.6, 0.8, 1.0)], 15))
    b.append(text(X0 - 10, Y0 + 24, "0", 15, INK2, anchor="end"))
    b.append(text(X0 + W2, Y0 + 48, "金属の質量［g］", 15, INK, anchor="end"))
    for k, col in [("cu", CU), ("mg", MG)]:
        M = MET[k]; sl = M["b"] / M["a"]; xe = min(XM, YM / sl)
        b.append(line(px(0), py(0), px(xe), py(sl * xe), col, 2.2, "8 5"))
        for m in M["lst"]:
            o = oxy(k, m)
            if k == "cu": b.append(f'<rect x="{px(m) - 6:.1f}" y="{py(o) - 6:.1f}" width="12" height="12" fill="{col}" stroke="#fff" stroke-width="1.2"/>')
            else: b.append(circle(px(m), py(o), 6.5, col, "#fff", 1.2))
    b.append(text(px(1.30), py(0.98), "マグネシウム：酸素＝3：2", 16, INK2, 700, "end"))
    b.append(text(px(1.6), py(0.40) + 62, "銅：酸素＝4：1", 16, "#7d5a18", 700, "end"))
    b.append(text(X0 + 14, py(0.72), "原点を通る直線＝比例", 15, INK2))
    # ---------- 下：質量の比の表と計算のしかた ----------
    b.append(table(60, 476, ["質量の比", "金属", "酸素", "酸化物"],
                   [["銅 → 酸化銅", "4", "1", "5"], ["マグネシウム → 酸化マグネシウム", "3", "2", "5"]],
                   [290, 78, 78, 86], 44, 17))
    b.append(rect(620, 470, 532, 144, CARD, LINE, 10))
    b.append(text(638, 498, "計算のしかた（反応していない銅が残るとき）", 16, INK, 700))
    b.append(lines(638, 526, ["銅1.2 gを加熱したら、1.4 gになった。",
                              "① 結びついた酸素　1.4 − 1.2 ＝ 0.2 g",
                              "② 酸素と結びついた銅　0.2 × 4 ＝ 0.8 g",
                              "③ 反応していない銅　1.2 − 0.8 ＝ 0.4 g"], 16, INK2, 1.45))
    return svg("".join(b), "加熱のグラフと質量の比（まとめ）",
               "質量の比は教科書の値（銅：酸素＝4：1、マグネシウム：酸素＝3：2）。点はシミュの「まとめて実験」の値。")


FIGS = [
    dict(svg=fig1, alt="化学変化と質量のしくみの図。炭酸水素ナトリウムとうすい塩酸を密閉した容器で反応させても82.46 gのまま変わらず、ふたを開けると二酸化炭素0.52 gが出ていって81.94 gになることと、反応の前後で原子の種類と数が同じことを示す。銅とマグネシウムが酸素と結びつく原子のモデル（2Cu＋O₂→2CuO、2Mg＋O₂→2MgO）と、質量の比 銅：酸素＝4：1、マグネシウム：酸素＝3：2もかいている。",
         caption="質量保存の法則と、金属が酸素と結びつくしくみ。原子の種類と数が変わらないので質量の総和は変わらず、結びつく原子の質量の比から銅：酸素＝4：1、マグネシウム：酸素＝3：2になる。"),
    dict(svg=fig2, alt="銅0.80 gとマグネシウム0.60 gを加熱した回数と質量のグラフ（どちらも1.00 gで一定になる）と、金属の質量と結びつく酸素の質量の比例のグラフ。質量の比の表（銅：酸素：酸化銅＝4：1：5、マグネシウム：酸素：酸化マグネシウム＝3：2：5）と、反応していない銅の質量を求める計算のしかたをまとめた図。",
         caption="加熱のグラフと質量の比のまとめ。加熱をくり返すと質量は一定になり、金属の質量と結びつく酸素の質量は比例する。"),
]
