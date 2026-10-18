"""火山の形と火成岩（kazan-kaseigan）の授業用の図
   ページの JS（scripts/rika/sims_chisou.py の kazan-kaseigan）と同じ値：
   火山の形 PRF＝たて状 R262・H46・e1.8／成層 R186・H122・e0.72／溶岩ドーム R72・H84・e2.6（高さ＝H(1−u^e)、u＝中心からの距離÷R。
   溶岩ドームは 18(1−d/128)^1.3 のすそ野つき）。岩石の色 rockC、鉱物の割合 COMP（3区分の中央の値を直線でつなぎ、両はしは一定）。"""
import math, random
from figlib import *

PRF = [(262, 46, 1.8), (186, 122, 0.72), (72, 84, 2.6)]
ROCKC = [(62, 60, 60), (136, 128, 121), (222, 215, 204)]
MIN = ["カンラン石", "キ石", "カクセン石", "クロウンモ", "チョウ石", "セキエイ"]
MCOL = ["#a3c23f", "#3d6b4a", "#26302b", "#6b4428", "#f3ece0", "#cfd8e3"]
COMP = [[12, 36, 2, 0, 50, 0], [0, 8, 20, 4, 60, 8], [0, 0, 2, 8, 60, 30]]
VR, PR = ["玄武岩", "安山岩", "流紋岩"], ["斑れい岩", "閃緑岩", "花こう岩"]


def comp(q):
    q = max(1 / 6, min(5 / 6, q)); lo = q <= 0.5
    a, b = (COMP[0], COMP[1]) if lo else (COMP[1], COMP[2]); t = (q - 1 / 6) * 3 if lo else (q - 0.5) * 3
    return [x + (y - x) * t for x, y in zip(a, b)]


def rgb(c): return "rgb(%d,%d,%d)" % c


def vh(dx, k):
    R, H, e = PRF[k]; u = abs(dx) / R; h = H * (1 - u ** e) if u < 1 else 0
    if k == 2:
        ap = abs(dx) / 128
        if ap < 1: h = max(h, 18 * (1 - ap) ** 1.3)
    return h


def fig1():
    b = []
    names = ["たて状火山", "成層火山", "溶岩ドーム"]
    shapes = ["傾斜がゆるやかな形", "円すい形", "ドーム状（おわんをふせた形）"]
    col_w = [168, 312, 312, 312]; x0 = 48
    cxs = [x0 + col_w[0] + col_w[1] / 2, x0 + col_w[0] + col_w[1] + col_w[2] / 2, x0 + sum(col_w[:3]) + col_w[3] / 2]
    GY = 300; S = 0.52                                   # シミュの形を 0.52 倍
    b.append(text(48, 128, "マグマのねばりけと火山の形（断面）", 18, INK, 700))
    for k, cx in enumerate(cxs):
        R = PRF[k][0] * S * 1.05 + (40 if k == 2 else 0)
        pts = [(cx + dx * S, GY - vh(dx, k) * S * 1.25) for dx in range(-int(PRF[k][0] + 130), int(PRF[k][0] + 131), 3)]
        pts = [p for p in pts if abs(p[0] - cx) <= col_w[k + 1] / 2 - 8]
        b.append(f'<path d="M{pts[0][0]:.1f},{GY} ' + " ".join(f"L{x:.1f},{y:.1f}" for x, y in pts) + f' L{pts[-1][0]:.1f},{GY}Z" fill="{rgb(ROCKC[k])}" stroke="{INK}" stroke-width="1.6"/>')
        # 火道とマグマ
        b.append(line(cx, GY - vh(0, k) * S * 1.25 + 4, cx, GY + 14, ACC, 5))
        b.append(f'<ellipse cx="{cx}" cy="{GY + 24}" rx="34" ry="11" fill="{ACC}" opacity=".85"/>')
        b.append(text(cx, 162, names[k], 19, INK, 700, "middle"))
        b.append(text(cx, 184, shapes[k], 15, INK2, anchor="middle"))
    b.append(line(x0 + col_w[0], GY, 1152, GY, INK2, 1.4))
    b.append(text(x0 + col_w[0] + 8, GY + 34, "マグマ", 14, ACC, 700))
    rows = [["噴火のようす", "おだやか（溶岩が流れ出す）", "爆発的な噴火と溶岩の流出", "激しい（爆発的・火砕流も）"],
            ["溶岩・岩石の色", "黒っぽい", "灰色っぽい（中間）", "白っぽい"],
            ["火山の例", "マウナロア・キラウエア（ハワイ）", "桜島・浅間山・富士山", "昭和新山・雲仙普賢岳（平成新山）"]]
    b.append(table(x0, 352, ["マグマのねばりけ", "弱い", "中くらい", "強い"], rows, col_w, 50, 15.5))
    b.append(text(x0, 612, "火山の大きさ・高さは実際の比率ではない（形のちがいを表したもの）。", 14, MUTED))
    return svg("".join(b), "マグマのねばりけと火山の形・噴火・色",
               "ねばりけが強いマグマほど、もり上がった形になり、噴火は激しく、溶岩や岩石は白っぽい。", "")


def voronoi(sites, box):
    """ボロノイ図（各点の領域を半平面で切り出す）"""
    cells = []
    for i, (px, py) in enumerate(sites):
        poly_ = [(box[0], box[1]), (box[2], box[1]), (box[2], box[3]), (box[0], box[3])]
        for j, (qx, qy) in enumerate(sites):
            if i == j or abs(qx - px) > 80 or abs(qy - py) > 80: continue
            mx, my = (px + qx) / 2, (py + qy) / 2; nx, ny = qx - px, qy - py
            side = lambda p: (p[0] - mx) * nx + (p[1] - my) * ny
            out = []
            for k in range(len(poly_)):
                a, c = poly_[k], poly_[(k + 1) % len(poly_)]; sa, sc = side(a), side(c)
                if sa <= 0: out.append(a)
                if sa * sc < 0:
                    t = sa / (sa - sc); out.append((a[0] + (c[0] - a[0]) * t, a[1] + (c[1] - a[1]) * t))
            poly_ = out
            if not poly_: break
        cells.append(poly_)
    return cells


def pick(u, c):
    s = 0
    for i in range(6):
        s += c[i]
        if u * 100 < s: return i
    return 4


def texture(cx, cy, r, kind, cid):
    rnd = random.Random(7 if kind == "por" else 11)
    out = [f'<clipPath id="{cid}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>', f'<g clip-path="url(#{cid})">']
    if kind == "por":                                    # 斑状組織（安山岩の例）：石基＋斑晶
        out.append(circle(cx, cy, r, "#8d877f", "none", 0))
        for _ in range(420):
            a, d = rnd.random() * 2 * math.pi, r * math.sqrt(rnd.random())
            col = rnd.choice(["#6f6a63", "#a29c94", "#b8b2aa", "#5d5852"])
            out.append(f'<rect x="{cx + d * math.cos(a):.1f}" y="{cy + d * math.sin(a):.1f}" width="2.4" height="1.6" fill="{col}"/>')
        c = comp(0.5)
        for _ in range(11):
            a, d = rnd.random() * 2 * math.pi, (r - 16) * math.sqrt(rnd.random())
            x, y = cx + d * math.cos(a), cy + d * math.sin(a); m = pick(rnd.random(), c)
            w, h, rot = (rnd.uniform(16, 26), rnd.uniform(7, 11), rnd.uniform(0, 180)) if m == 4 else (rnd.uniform(9, 14), rnd.uniform(8, 12), rnd.uniform(0, 180))
            out.append(f'<rect x="{x - w / 2:.1f}" y="{y - h / 2:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{MCOL[m]}" stroke="#3d3a36" stroke-width="0.8" transform="rotate({rot:.0f} {x:.1f} {y:.1f})"/>')
    else:                                                # 等粒状組織（花こう岩の例）
        c = comp(5 / 6); sites = []
        step = 15
        for gy in range(int(cy - r - step), int(cy + r + step), step):
            for gx in range(int(cx - r - step), int(cx + r + step), step):
                sites.append((gx + rnd.uniform(-5, 5), gy + rnd.uniform(-5, 5)))
        for cell in voronoi(sites, (cx - r - 20, cy - r - 20, cx + r + 20, cy + r + 20)):
            if len(cell) < 3: continue
            m = pick(rnd.random(), c); col = MCOL[m] if m != 4 else rnd.choice(["#f3ece0", "#efd9cf"])
            out.append(f'<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in cell) + f'Z" fill="{col}" stroke="#55504a" stroke-width="0.7"/>')
    out.append("</g>")
    out.append(circle(cx, cy, r, "none", INK, 1.8))
    return "".join(out)


def fig2():
    b = []
    # ---- 左：組織 ----
    cx, r = 150, 80
    b.append(text(48, 128, "冷え方とつくり（組織）", 18, INK, 700))
    b.append(texture(cx, 226, r, "por", "kz-c1"))
    b.append(line(cx + 32, 210, 268, 176, INK, 1.2) + text(272, 176, "斑晶", 15, INK, 700) + text(272, 194, "（大きな結晶）", 14, INK2))
    b.append(line(cx + 58, 252, 268, 262, INK, 1.2) + text(272, 260, "石基", 15, INK, 700) + text(272, 278, "（細かい粒・ガラス）", 14, INK2))
    b.append(text(48, 330, "斑状組織 ＝ 火山岩", 17, ACC, 700))
    b.append(text(48, 352, "地表や地表付近で急に冷えた", 15, INK2))
    b.append(texture(cx, 456, r, "eq", "kz-c2"))
    b.append(line(cx + 50, 430, 268, 420, INK, 1.2) + text(272, 418, "同じくらいの", 14, INK2) + text(272, 436, "大きさの結晶", 14, INK2))
    b.append(text(48, 562, "等粒状組織 ＝ 深成岩", 17, TEAL_D, 700))
    b.append(text(48, 584, "地下深くでゆっくり冷えた", 15, INK2))
    b.append(text(48, 612, "円は岩石をルーペで見たようす（例）", 14, MUTED))
    # ---- 右：分類表 ----
    x0 = 420; cw = [184, 182, 182, 182]
    b.append(text(x0, 128, "火成岩の分類と、ふくまれる鉱物", 18, INK, 700))
    rows = [["火山岩（斑状組織）"] + VR, ["深成岩（等粒状組織）"] + PR,
            ["有色鉱物の割合"] + ["約%d％" % (round(sum(comp(q)[:4]) / 10) * 10) for q in (1 / 6, 0.5, 5 / 6)]]
    b.append(table(x0, 144, ["岩石の色", "黒っぽい", "中間（灰色っぽい）", "白っぽい"], rows, cw, 42, 15.5))
    # 鉱物の割合のグラフ（積み上げ）
    gx0, gx1 = x0 + cw[0], x0 + sum(cw); gy0, gy1 = 336, 590
    b.append(text(x0, gy0 + 16, "鉱物の割合", 15, INK, 700) + text(x0, gy0 + 36, "（体積の％・目安）", 14, INK2))
    qs = [i / 60 for i in range(61)]
    acc = [[0] * len(qs)]
    for m in range(6):
        acc.append([acc[-1][j] + comp(q)[m] for j, q in enumerate(qs)])
    X = lambda q: gx0 + q * (gx1 - gx0); Y = lambda v: gy1 - v / 100 * (gy1 - gy0)
    for m in range(6):
        lo, hi = acc[m], acc[m + 1]
        d = "M" + " L".join(f"{X(q):.1f},{Y(hi[j]):.1f}" for j, q in enumerate(qs)) + " L" + " L".join(f"{X(q):.1f},{Y(lo[j]):.1f}" for j, q in reversed(list(enumerate(qs)))) + "Z"
        b.append(f'<path d="{d}" fill="{MCOL[m]}" stroke="#55504a" stroke-width="0.6"/>')
    b.append(poly([(X(q), Y(acc[4][j])) for j, q in enumerate(qs)], ACC, 3))          # 有色鉱物と無色鉱物の境
    b.append(f'<rect x="{gx0}" y="{gy0}" width="{gx1 - gx0}" height="{gy1 - gy0}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    for v in (0, 50, 100):
        b.append(line(gx0 - 5, Y(v), gx0, Y(v), INK, 1.2) + text(gx0 - 8, Y(v) + 5, f"{v}％", 14, INK2, anchor="end"))
    # 鉱物名（帯の中、太さが足りる所に）
    lab = [(0, 1 / 6, "#fff"), (1, 0.25, "#fff"), (2, 0.5, "#fff"), (3, 0.86, "#fff"), (4, 0.5, INK), (5, 0.85, INK)]
    for m, q, col in lab:
        j = round(q * 60); mid = (acc[m][j] + acc[m + 1][j]) / 2
        b.append(text(X(q), Y(mid) + 5, MIN[m], 14.5, col, 700, "middle"))
    # 有色・無色の目じるし
    b.append(text(x0, Y(22) + 5, "▼ 有色鉱物", 15, INK, 700) + text(x0, Y(22) + 25, "（黒っぽい鉱物）", 14, INK2))
    b.append(text(x0, Y(62) + 5, "▲ 無色鉱物", 15, INK, 700) + text(x0, Y(62) + 25, "（白っぽい鉱物）", 14, INK2))
    b.append(text(x0, Y(44) + 5, "赤線が境目", 14, ACC, 700))
    b.append(text(1152, 612, "鉱物の割合はおおよその例（同じ岩石でも試料でちがう）。", 14, MUTED, anchor="end"))
    return svg("".join(b), "火成岩の分類（組織と色）",
               "冷え方で組織が、ふくまれる鉱物の割合で色が決まる。有色鉱物が多いほど黒っぽい。")


FIGS = [
    dict(svg=fig1, alt="マグマのねばりけと火山の形の図。ねばりけが弱いと傾斜がゆるやかなたて状火山（マウナロア・キラウエア）、中くらいだと円すい形の成層火山（桜島・浅間山・富士山）、強いとドーム状の溶岩ドーム（昭和新山・雲仙普賢岳の平成新山）になり、噴火のようすと溶岩・岩石の色（黒っぽい〜白っぽい）も変わることを示す。",
         caption="マグマのねばりけと火山の形・噴火・色。ねばりけが強いほど、もり上がった形で、噴火が激しく、白っぽい。"),
    dict(svg=fig2, alt="火成岩の分類の図。斑晶と石基からなる斑状組織（火山岩）と、同じくらいの大きさの結晶が組み合わさった等粒状組織（深成岩）のようす、玄武岩・安山岩・流紋岩と斑れい岩・閃緑岩・花こう岩の分類表、有色鉱物の割合（約50％・約30％・約10％）、カンラン石・キ石・カクセン石・クロウンモ・チョウ石・セキエイの割合のグラフ。",
         caption="火成岩の分類。組織で火山岩と深成岩に、色（有色鉱物の割合）で3つに分ける。"),
]
