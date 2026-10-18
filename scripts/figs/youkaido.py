"""物の溶け方と溶解度（youkaido）の授業用の図
数値はシミュ（scripts/rika/sims_youkai_nenshou.py の SOL と JS_YOUKAI）と同じ：
  溶解度［g/水100 g］0〜80℃・10℃ごと、間は直線で結ぶ（sol()）。溶ける限度＝溶解度×水の量÷100（小数第1位に四捨五入）。
  粒子のモデルの粒の数＝水100 gあたりの量×1.5（KP）。"""
import math
import random
from figlib import *

# シミュの SOL と同じ値
SOL = {"alum": ("ミョウバン", [5.7, 7.6, 11.4, 16.6, 23.8, 36.4, 57.4, 110.5, 321.6]),
       "salt": ("食塩", [35.7, 35.7, 35.8, 36.1, 36.3, 36.7, 37.1, 37.5, 38.0]),
       "kno3": ("硝酸カリウム", [13.3, 22.0, 31.6, 45.6, 63.9, 85.2, 109.2, 138.0, 168.8]),
       "boric": ("ホウ酸", [2.8, 3.6, 4.9, 6.8, 8.9, 11.4, 14.9, 18.7, 23.5])}
KP = 1.5


def r1(v):
    return math.floor(v * 10 + 1e-7 + 0.5) / 10


def sol(k, t):
    S = SOL[k][1]; t = max(0, min(80, t)); i = min(7, int(t // 10))
    return S[i] + (S[i + 1] - S[i]) * (t / 10 - i)


def state(k, wa, tt, m):
    """シミュの calc() と同じ：溶ける限度・溶けている量・溶け残り・粒の数"""
    S1 = r1(sol(k, tt)); lim = r1(S1 * wa / 100); dis = r1(min(m, lim)); res = r1(m - dis)
    nT = round(m / wa * 100 * KP); nD = min(nT, round(dis / wa * 100 * KP))
    return dict(S1=S1, lim=lim, dis=dis, res=res, tot=r1(wa + m), nT=nT, nD=nD)


def scatter(n, x0, y0, x1, y1, seed):
    """溶けた粒：水の中に均一に（すきまのある格子＋少しずらす）"""
    rnd = random.Random(seed)
    cols = max(1, round(math.sqrt(n * (x1 - x0) / (y1 - y0))))
    rows = math.ceil(n / cols)
    cells = [(c, r) for r in range(rows) for c in range(cols)]
    rnd.shuffle(cells); cells = sorted(cells[:n], key=lambda q: (q[1], q[0]))
    cw, ch = (x1 - x0) / cols, (y1 - y0) / rows
    return [(x0 + (c + 0.5) * cw + rnd.uniform(-0.28, 0.28) * cw, y0 + (r + 0.5) * ch + rnd.uniform(-0.28, 0.28) * ch) for c, r in cells]


def pile(n, cx, by, d=11):
    """溶け残り・結晶：底に集まった粒"""
    pts, row, left = [], 0, n
    widths = [5, 4, 3, 1, 1]
    while left > 0:
        k = min(widths[min(row, 4)], left)
        for i in range(k): pts.append((cx + (i - (k - 1) / 2) * d, by - row * (d - 1.5)))
        left -= k; row += 1
    return pts


def fig1():
    b = []
    K, WA, M = "alum", 50, 10
    stages = [("① 20℃の水50 gに入れる", "ミョウバン10 gを入れてかき混ぜる", 20, "溶け残り"),
              ("② 40℃にあたためる", "かき混ぜると、溶け残りが溶ける", 40, None),
              ("③ もう一度 20℃に冷やす", "溶けきれない分が出てくる", 20, "出てきた結晶")]
    pw = 336
    for s, (head, sub, T, pl) in enumerate(stages):
        x0 = 48 + s * (pw + 48); st = state(K, WA, T, M)
        b.append(rect(x0, 100, pw, 494, CARD, LINE, 12))
        b.append(text(x0 + 18, 132, head, 18, INK, 700))
        b.append(text(x0 + 18, 156, sub, 15, INK2))
        cx = x0 + 146; L, R, top, wl, bot = cx - 96, cx + 96, 188, 232, 404
        # 水
        b.append(f'<rect x="{L + 2}" y="{wl}" width="{R - L - 4}" height="{bot - wl - 2}" fill="#e3eef4"/>')
        b.append(line(L + 2, wl, R - 2, wl, SKY, 1.6))
        b.append(text(L + 10, wl + 20, "水 50 g", 14, TEAL_D, 700))
        # 粒（溶けている粒＝水全体に、溶け残り＝底に）
        nS = st["nT"] - st["nD"]
        for (px, py) in scatter(st["nD"], L + 14, wl + 30, R - 14, bot - (44 if nS else 14), seed=7 if T == 20 else 11):
            b.append(circle(px, py, 5.2, PURPLE, PURPLE, 0))
        for (px, py) in pile(nS, cx + 54, bot - 8):
            b.append(circle(px, py, 5.2, PURPLE, INK, 1.1))
        if pl:      # 底の帯（溶けた粒をおかない所）に名前
            b.append(text(cx + 4, bot - 13, pl, 15, ACC, 700, "end") + arrow(cx + 8, bot - 18, cx + 24, bot - 18, "acc", 2))
        # ビーカー
        b.append(f'<path d="M{L - 8},{top} L{L},{top + 6} L{L},{bot - 8} Q{L},{bot} {L + 8},{bot} L{R - 8},{bot} Q{R},{bot} {R},{bot - 8} L{R},{top + 6} L{R + 8},{top}" fill="none" stroke="{INK2}" stroke-width="2.6"/>')
        # 温度計
        tx0 = x0 + 300; ty0, ty1 = 196, 392
        b.append(rect(tx0 - 5, ty0, 10, ty1 - ty0, "#fff", MUTED, 5, 1.2))
        hy = ty1 - 8 - T / 80 * (ty1 - ty0 - 16)
        b.append(f'<rect x="{tx0 - 2.5}" y="{hy:.1f}" width="5" height="{ty1 - hy + 2:.1f}" fill="{ACC}"/>' + circle(tx0, ty1 + 6, 8, ACC, ACC, 0))
        b.append(text(tx0, ty0 - 10, f"{T}℃", 17, ACC, 700, "middle"))
        # 電子てんびん
        b.append(rect(cx - 100, bot + 6, 200, 46, "#e9e5db", "#cfc9ba", 8) + rect(cx - 70, bot + 13, 140, 32, INK, INK, 5, 0)
                 + text(cx + 62, bot + 37, f"{st['tot']:.1f} g", 20, "#fff", 700, "end"))
        # 計算
        y = 496
        if s == 0:
            rows = [(f"溶ける限度　{SOL[K][1][2]} × 50 ÷ 100 ＝ {st['lim']} g", INK),
                    (f"溶け残り　{M} − {st['lim']} ＝ {st['res']} g", ACC)]
        elif s == 1:
            rows = [(f"溶ける限度　{SOL[K][1][4]} × 50 ÷ 100 ＝ {st['lim']} g", INK),
                    (f"{M} gは全部溶ける（溶け残り 0 g）", TEAL_D)]
        else:
            rows = [(f"溶ける限度　{st['lim']} g（20℃にもどる）", INK),
                    (f"出てくる結晶　{M} − {st['lim']} ＝ {st['res']} g", ACC)]
        for i, (t, c) in enumerate(rows):
            b.append(text(x0 + 18, y + i * 30, t, 16, c, 700 if i else 400))
        b.append(text(x0 + 18, y + 72, f"重さ：水50 g＋ミョウバン10 g＝{st['tot']:.1f} g", 15, INK2))
        if s < 2:
            b.append(arrow(x0 + pw + 6, 300, x0 + pw + 42, 300, "ink", 2.6))
    b.append(circle(58, 610, 5.2, PURPLE, PURPLE, 0))
    b.append(text(70, 615, "＝溶けている粒　", 15, INK2))
    b.append(circle(194, 610, 5.2, PURPLE, INK, 1.1))
    b.append(text(206, 615, "＝溶け残り・結晶の粒（粒の数は溶けている量に合わせた模式図。水の粒はかいていない）", 15, INK2))
    return svg("".join(b), "物が水に溶けるしくみ（ミョウバンの例）",
               "溶けた物は見えない小さな粒になり、水全体に均一に広がる。溶けても重さは変わらない。")


def fig2():
    b = []
    x0, y0, w, h, YM = 104, 572, 560, 412, 180
    gx = lambda t: x0 + t / 80 * w
    gy = lambda v: y0 - v / YM * h
    b.append(text(48, y0 - h - 22, "水100 gに溶ける量［g］", 15, INK))
    b.append(axes(x0, y0, w, h, "", "", [(gx(t) - x0, str(t)) for t in range(10, 81, 10)],
                  [(y0 - gy(v), str(v)) for v in range(20, YM + 1, 20)], 15))
    b.append(text(x0 - 10, y0 + 24, "0", 15, INK2, anchor="end"))
    b.append(text(x0 + w, y0 + 44, "水温［℃］", 15, INK, anchor="end"))
    sty = {"kno3": (ACC, None, 3.2), "alum": (PURPLE, None, 3.2), "salt": (INK2, "10 6", 3), "boric": (TEAL, "3 5", 3.2)}
    for k in ("salt", "boric", "alum", "kno3"):
        col, dash, wd = sty[k]; pts = []
        for i in range(0, 161):
            t = i * 0.5; v = sol(k, t)
            if v > YM:
                t0 = 70 + (YM - sol(k, 70)) / (sol(k, 80) - sol(k, 70)) * 10   # グラフの上の端と交わる点
                pts.append((gx(t0), gy(YM))); break
            pts.append((gx(t), gy(v)))
        b.append(poly(pts, col, wd, dash=dash))
    # 曲線の名前
    b.append(text(gx(62), gy(140), "硝酸カリウム", 17, ACC, 700, "end"))
    b.append(line(gx(62) + 4, gy(140) - 5, gx(66.5), gy(sol("kno3", 66.5)) + 2, ACC, 1.4))
    b.append(text(gx(71.5), gy(168), "ミョウバン", 17, PURPLE, 700, "end"))
    b.append(text(gx(71.5), gy(168) + 22, "（80℃では321.6 g）", 14, PURPLE, anchor="end"))
    b.append(text(gx(44), gy(43), "食塩", 17, INK2, 700))
    b.append(text(gx(79), gy(6), "ホウ酸", 17, TEAL, 700, "end"))
    # 再結晶：硝酸カリウム 60℃→20℃
    v60, v20 = sol("kno3", 60), sol("kno3", 20)
    b.append(circle(gx(60), gy(v60), 6, ACC, "#fff", 1.5))
    b.append(f'<line x1="{gx(60) - 8:.1f}" y1="{gy(v60):.1f}" x2="{gx(20) + 4:.1f}" y2="{gy(v60):.1f}" stroke="{INK}" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#ah-ink)"/>')
    b.append(text(gx(40), gy(v60) - 10, "60℃ → 20℃に冷やす", 15, INK, 700, "middle"))
    b.append(line(gx(20), gy(v60), gx(20), gy(v20), ACC, 4))
    b.append(circle(gx(20), gy(v20), 6, ACC, "#fff", 1.5))
    my = gy((v60 + v20) / 2)
    b.append(text(gx(20) - 10, my - 12, "出てくる結晶", 15, ACC, 700, "end"))
    b.append(text(gx(20) - 10, my + 12, f"{r1(v60 - v20):.1f} g", 18, ACC, 700, "end"))
    b.append(text(gx(20) - 10, my + 34, f"（{v60:.1f}−{v20:.1f}）", 14, ACC, anchor="end"))
    # 右：読み方と早見表
    X = 712
    b.append(text(X, 128, "溶解度曲線の読み方", 18, INK, 700))
    b.append(lines(X, 158, ["・曲線の上の点＝水100 gに溶ける限度（飽和）",
                            "・曲線より下の点は全部溶ける。上の点は溶け残る",
                            "・水50 gなら、溶ける量はグラフの値の半分",
                            "・冷やして出てくる結晶＝溶けていた量−冷やした",
                            "　温度で溶ける限度"], 15.5, INK2, 1.6))
    b.append(text(X, 318, "水100 gの飽和水溶液を60℃→20℃に冷やすと", 16, INK, 700))
    rows = []
    for k in ("kno3", "alum", "boric", "salt"):
        a, c = sol(k, 60), sol(k, 20)
        rows.append([SOL[k][0], f"{a:.1f} g", f"{c:.1f} g", f"{r1(a - c):.1f} g"])
    b.append(table(X, 332, ["", "60℃", "20℃", "出てくる結晶"], rows, [130, 92, 92, 126], 42, 16))
    b.append(lines(X, 566, ["食塩は温度で溶ける量がほとんど変わらないので、",
                            "冷やしても少ししか出てこない → 水を蒸発させて取り出す"], 15, INK2, 1.5))
    return svg("".join(b), "溶解度曲線と再結晶（まとめ）",
               "溶解度は理科年表・教科書で一般的な値（ミョウバンは結晶の質量で表した値）。教科書によって少しちがうことがある。")


FIGS = [
    dict(svg=fig1, alt="20℃の水50 gにミョウバン10 gを入れると5.7 gまで溶けて4.3 gが溶け残り、40℃にあたためると全部溶け、20℃に冷やすと4.3 gの結晶が出てくるようすを、ビーカーの中の粒子のモデルと温度計・電子てんびん（どれも60.0 g）でかいた図。溶けた粒は水全体に均一に広がる。",
         caption="物が水に溶けるしくみ。溶ける量には限度があり、あたためると多く溶け、冷やすと溶けきれない分が結晶として出てくる。重さは変わらない。"),
    dict(svg=fig2, alt="食塩・ミョウバン・硝酸カリウム・ホウ酸の溶解度曲線（水100 gに溶ける量と水温0〜80℃）。硝酸カリウムの飽和水溶液を60℃から20℃に冷やすと109.2−31.6＝77.6 gの結晶が出てくることと、4つの物質を60℃から20℃に冷やしたときに出てくる結晶の量の早見表。",
         caption="溶解度曲線の読み方と再結晶。温度で溶ける量が大きく変わる物は冷やして、食塩は水を蒸発させて取り出す。"),
]
