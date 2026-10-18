"""雨水のゆくえと地面のようす（amamizu-yukue・小4）の授業用の図。
①の地面の形・水の流れ・しみこみ、②のカップのしみこみ方は、シミュの JS（scripts/rika/sims_sho4_a.py の JS_AMA）と同じ式で計算する。
①はシミュの初期設定（地面の形「校庭の例」・校庭の土・雨の強さ 1時間に30 mm）で、雨がふりはじめて30分後のようす。"""
from figlib import *

# ---------------- ① 地面のかたむきと水の流れ（JS の preset('ex')・stepFlow と同じ）
N = 128
SOIL_F = {"suna": 150, "kotei": 10, "nendo": 2, "asph": 0}     # しみこむ力（mm/時の目安）


def ground():
    h = []
    for i in range(N):
        x = i / (N - 1)
        v = 30 - 17 * x + 6 * math.sin(2 * math.pi * x * 1.45 + 1.6) + 1.5 * math.cos(x * 37) * (1 - 0.7 * x)
        h.append(max(1.0, min(48.0, v)))
    return h


def rain_run(R=30, soil="kotei", minutes=30, sub=0.5):
    h = ground(); w = [0.0] * N; F = [0.0] * N; tot = dict(r=0.0, i=0.0, o=0.0)
    for _ in range(int(round(minutes * 60 / sub))):
        rn = R / 36000 * sub; fc = SOIL_F[soil] / 36000 * sub
        for i in range(N):
            w[i] += rn; tot["r"] += rn; q = min(w[i], fc); w[i] -= q; tot["i"] += q
        for i in range(N - 1):
            q = 0.24 * ((h[i] + w[i]) - (h[i + 1] + w[i + 1]))
            F[i] = min(q, w[i] * 0.5) if q > 0 else max(q, -w[i + 1] * 0.5)
        for i in range(N - 1):
            w[i] -= F[i]; w[i + 1] += F[i]
        d = w[N - 1] * 0.5; w[N - 1] -= d; tot["o"] += d
    return h, w, tot


def puddles(w):
    out, i = [], 0
    while i < N:
        if w[i] > 0.3:
            j, md, mi = i, 0.0, i
            while j < N and w[j] > 0.3:
                if w[j] > md: md, mi = w[j], j
                j += 1
            out.append(dict(a=i, b=j - 1, d=md, m=mi)); i = j
        else:
            i += 1
    return out


MIN = 30
H, Wt, TOT = rain_run(minutes=MIN)
PUD = puddles(Wt)
P_IN, P_OUT = TOT["i"] / TOT["r"], TOT["o"] / TOT["r"]
P_REST = max(0.0, 1 - P_IN - P_OUT)
MM = TOT["r"] / N * 10
assert abs(MM - 15) < 0.05 and len(PUD) == 1

# ---------------- ② 土のつぶとしみこみ方（JS の CUP と同じ）
CUP = [dict(nm="すな", sub="つぶが大きい", r=10, Rt=22, tau=3, gs=6.5, c="#e8d09a", d="#b9944f", lc=GOLD),
       dict(nm="校庭の土", sub="つぶが中くらい", r=1.0, Rt=35, tau=12, gs=3.4, c="#b8915f", d="#7a5a36", lc=ACC),
       dict(nm="ねん土っぽい土", sub="つぶがとても小さい", r=0.12, Rt=45, tau=40, gs=1.3, c="#a07f68", d="#5b4334", lc=PURPLE)]
V0, TMAX, DT = 100, 900, 0.1
for c in CUP:
    o, O = 0.0, []
    for k in range(int(round(TMAX / DT)) + 1):
        I = min(V0, c["r"] * k * DT); E = max(0.0, I - c["Rt"]); o += (E - o) * DT / c["tau"]; O.append(o)
    c["O"] = O; c["Ts"] = V0 / c["r"]


def fmtT(s):                                   # JS の fmtT
    s = max(0, s)
    if s >= 600: return "約%d分" % math.floor(s / 60 + 0.5)
    if s < 60: return "%d秒" % math.floor(s)
    m, r = int(s // 60), int(s % 60)
    return "%d分%02d秒" % (m, r)


def fr(v): return v - math.floor(v)
def hs1(k): return fr(math.sin(k * 12.9898) * 43758.5453)
def hs2(k): return fr(math.sin(k * 78.233) * 12345.678)


def fig1():
    b = []
    GX0, GX1, BY = 70, 1010, 540
    CW = (GX1 - GX0) / N
    PXH = CW / (2000 / N) * 14                 # 横20 m を GX0〜GX1 に。高さは横の14倍
    X = lambda i: GX0 + (i + 0.5) * CW
    Y = lambda v: BY - v * PXH
    # 空と雨
    b.append(rect(48, 100, 1104, 452, "#eef3f6", LINE, 10))
    for cx, cy in [(150, 132), (420, 124), (700, 134), (930, 126)]:
        b.append(circle(cx, cy, 24, "#b3bcc7", "#b3bcc7", 0) + circle(cx + 28, cy + 6, 20, "#b3bcc7", "#b3bcc7", 0) + circle(cx - 28, cy + 8, 18, "#b3bcc7", "#b3bcc7", 0))
    p = PUD[0]
    keep = [(X(2) - 10, Y(H[2]) - 50, 140, 60), (X(20) - 10, Y(H[20]) - 66, 220, 36), (X(p["m"]) - 150, Y(H[p["m"]] + Wt[p["m"]]) - 72, 300, 60),
            (X(104) - 160, Y(H[104]) - 100, 320, 40)]                       # ことばの所には雨をかかない
    for k in range(70):
        x = GX0 + hs1(k + 1) * (GX1 - GX0); i = max(0, min(N - 1, int((x - GX0) / CW)))
        top = Y(H[i] + Wt[i]); y = 160 + hs2(k + 1) * (top - 190)
        if y + 14 >= top - 30: continue
        if any(kx <= x <= kx + kw and ky <= y + 14 and y <= ky + kh for kx, ky, kw, kh in keep): continue
        b.append(line(x, y, x - 2, y + 14, "#5b8fc9", 1.8))
    # 地面
    pts = [(GX0 - 21, Y(H[0]))] + [(X(i), Y(H[i])) for i in range(N)] + [(GX1, Y(H[-1]))]
    b.append(f'<path d="M{GX0 - 21},{BY + 12} L' + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f' L{GX1},{BY + 12}Z" fill="#c9a777"/>')
    for k in range(150):
        x = GX0 + hs1(k + 300) * (GX1 - GX0); i = max(0, min(N - 1, int((x - GX0) / CW)))
        y = Y(H[i]) + 6 + hs2(k + 300) * max(0, BY + 6 - Y(H[i]) - 8)
        b.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="2.4" height="2.4" fill="#8a6a43"/>')
    # 水（地面の上の水）：つながった所ごとに1つの形でかく
    i = 0
    while i < N:
        if Wt[i] > 0.03:
            j = i
            while j < N and Wt[j] > 0.03: j += 1
            top = [(X(k) - CW / 2 if k == i else X(k), Y(H[k] + Wt[k])) for k in range(i, j)] + [(X(j - 1) + CW / 2, Y(H[j - 1] + Wt[j - 1]))]
            bot = [(X(k), Y(H[k])) for k in range(j - 1, i - 1, -1)]
            b.append(f'<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in top + bot) + '" fill="#4b8fe0"/>')
            i = j
        else:
            i += 1
    b.append(poly(pts, "#7a5a36", 2.2))
    # みぞ
    gy = Y(H[-1])
    b.append(f'<rect x="{GX1}" y="{gy - 2:.1f}" width="40" height="44" fill="#9ca3af"/><rect x="{GX1 + 6}" y="{gy:.1f}" width="28" height="36" fill="#334155"/>'
             f'<rect x="{GX1 + 6}" y="{gy + 22:.1f}" width="28" height="14" fill="#3b82f6"/>')
    b.append(text(GX1 + 20, gy - 12, "みぞ", 17, INK, 700, "middle"))
    b.append(arrow(GX1 + 52, gy + 30, GX1 + 120, gy + 30, "teal", 3) + text(GX1 + 86, gy + 58, "川へ", 15, TEAL_D, 700, "middle"))
    # 水の流れる向き（JS と同じきまり：水がうすい所で、高い方から低い方へ）
    for i in range(5, N - 5, 8):
        if Wt[i] < 0.002 or Wt[i] > 0.3: continue
        sl = (H[i + 3] + Wt[i + 3]) - (H[i - 3] + Wt[i - 3])
        if abs(sl) < 0.2: continue
        d = -1 if sl > 0 else 1; j0, j1 = i - d * 3, i + d * 3
        b.append(arrow(X(j0), Y(H[j0] + Wt[j0]) - 16, X(j1), Y(H[j1] + Wt[j1]) - 16, "acc", 3))
    # しみこむ
    for i in (10, 22, 95, 110):
        x = X(i); y = Y(H[i]) + 14
        b.append(arrow(x, y, x, y + 34, "teal", 2.4))
    b.append(text(X(10) + 12, Y(H[10]) + 44, "しみこむ", 16, TEAL_D, 700))
    # ことば
    b.append(text(X(2), Y(H[2]) - 26, "高い所", 18, INK, 700))
    b.append(text(X(p["m"]), Y(H[p["m"]] + Wt[p["m"]]) - 46, "低い所に集まる", 18, TEAL_D, 700, "middle"))
    b.append(text(X(p["m"]), Y(H[p["m"]] + Wt[p["m"]]) - 24, f"水たまり（深さ {p['d']:.1f} cm）", 16, TEAL_D, anchor="middle"))
    b.append(text(X(104), Y(H[104]) - 72, "高い所から低い所へ流れる", 16, ACC, 700, "middle"))
    b.append(text(X(20) + 4, Y(H[20]) - 40, "高い所から低い所へ", 16, ACC, 700))
    b.append(text(1140, 124, "高さは横の約14倍に強調", 14, MUTED, anchor="end"))
    # 下：ふった雨のゆくえ
    y0 = 572
    b.append(text(48, y0 + 18, f"ふった雨（{MM:.0f} mm）のゆくえ", 17, INK, 700))
    segs = [(P_IN, "#8a6a43", "しみこんだ"), (P_OUT, "#2563eb", "みぞへ流れた"), (P_REST, "#93c5fd", "地面に残る（水たまりなど）")]
    bx0, bw, xx = 290, 470, 290
    for v, col, nm in segs:
        ww = bw * v
        b.append(f'<rect x="{xx:.1f}" y="{y0}" width="{ww:.1f}" height="26" fill="{col}"/>')
        b.append(text(xx + ww / 2, y0 + 19, f"{round(v * 100)}%", 16, "#fff" if col != "#93c5fd" else INK, 700, "middle"))
        xx += ww
    lx = 786
    for v, col, nm in segs:
        b.append(f'<rect x="{lx}" y="{y0 + 2}" width="14" height="14" fill="{col}"/>')
        lx += 20
        b.append(text(lx, y0 + 15, nm if col != "#93c5fd" else "地面に残る", 14, INK2))
        lx += 14 * (len(nm if col != "#93c5fd" else "地面に残る")) + 12
    return svg("".join(b), "雨水のゆくえ（高い所から低い所へ流れて集まる）",
               f"校庭の土の地面に、1時間に30 mmの雨が{MIN}分ふったときのようす（シミュの初期設定）。数値は目安。")


def fig2():
    b = []
    # 左：3つの土
    for k, c in enumerate(CUP):
        cx = 150 + k * 200
        b.append(text(cx, 126, c["nm"], 19, INK, 700, "middle"))
        # 虫めがねで見たつぶ
        mx, my, R = cx, 200, 50
        cid = f"am-l{k}"
        dots = "".join(f'<circle cx="{mx - 54 + hs1(j + k * 97) * 108:.1f}" cy="{my - 54 + hs2(j + k * 97) * 108:.1f}" r="{c["gs"] * 2 * (0.7 + hs1(j * 3 + k) * 0.6):.1f}" fill="{c["c"]}" stroke="{c["d"]}" stroke-width="1.2"/>' for j in range(70 if k == 0 else 160 if k == 1 else 420))
        b.append(f'<clipPath id="{cid}"><circle cx="{mx}" cy="{my}" r="{R}"/></clipPath>')
        b.append(f'<circle cx="{mx}" cy="{my}" r="{R}" fill="#fefce8"/><g clip-path="url(#{cid})">{dots}</g>')
        b.append(circle(mx, my, R, "none", "#475569", 4) + line(mx + 36, my + 36, mx + 58, my + 58, "#475569", 7))
        rows = [("つぶ", ["大きい", "中くらい", "とても小さい"][k]), ("すき間", ["大きい", "小さい", "とても小さい"][k])]
        for j, (a, v) in enumerate(rows):
            b.append(text(cx, 290 + j * 26, f"{a}：{v}", 16, INK, anchor="middle"))
        b.append(rect(cx - 90, 336, 180, 78, CARD, c["lc"], 10, 2))
        b.append(text(cx, 360, "水100 mLが", 14, INK2, anchor="middle") + text(cx, 378, "全部しみこむまで", 14, INK2, anchor="middle"))
        b.append(text(cx, 403, ("約" if c["Ts"] < 600 else "") + fmtT(c["Ts"]), 20, c["lc"], 700, "middle"))
    b.append(arrow(70, 452, 600, 452, "ink", 2.4))
    b.append(text(70, 444, "つぶが大きい", 15, INK2) + text(600, 444, "つぶが小さい", 15, INK2, anchor="end"))
    b.append(text(335, 482, "つぶが大きいほど、水は速くしみこむ", 18, INK, 700, "middle"))
    b.append(text(335, 508, "（つぶが大きいと、つぶとつぶのすき間も大きい）", 15, INK2, anchor="middle"))
    # 右：下に出た水の量のグラフ
    X0, Y0, GW, GH = 720, 520, 400, 300
    tx = lambda t: X0 + t / TMAX * GW
    ty = lambda v: Y0 - v / V0 * GH
    b.append(text(660, 124, "カップの下に出た水の量", 18, INK, 700))
    b.append(text(660, 146, "（同じ量の土に水100 mLを注いだとき・数は目安）", 14, MUTED))
    b.append(axes(X0, Y0, GW, GH, "", "", [(t / TMAX * GW, f"{t // 60}分") for t in range(0, TMAX + 1, 180)],
                  [(v / V0 * GH, str(v)) for v in range(25, 101, 25)], 14))
    b.append(text(X0 - 10, Y0 + 6, "0", 14, INK2, anchor="end"))
    b.append(text(X0 - 50, 196, "［mL］", 14, INK2))
    b.append(text(X0 + GW, Y0 + 48, "注いでからの時間", 14, INK2, anchor="end"))
    for c in CUP:
        pts = [(tx(k * 1.0), ty(c["O"][int(k * 1.0 / DT)])) for k in range(0, TMAX + 1, 3)]
        b.append(poly(pts, c["lc"], 3.4))
        fin = c["O"][-1]
        b.append(text(tx(TMAX) - 4, ty(fin) - 10, f"{c['nm']}", 15, c["lc"], 700, "end"))
    b.append(text(tx(30) + 4, ty(78) + 28, "すぐに出てくる", 14, GOLD, 700))
    return svg("".join(b), "土のつぶの大きさと水のしみこみ方",
               "カップ・土の量・水の量をそろえてくらべる。土の中に残る水があるので、下に出る水は100 mLより少ない。")


FIGS = [
    dict(svg=fig1,
         alt=f"校庭の地面を横から切った図。雨水が高い所から低い所へ流れて、へこんだ低い所に集まって水たまり（深さ約{PUD[0]['d']:.0f} cm）ができ、一部は地面にしみこみ、一部はみぞから川へ流れていく。ふった雨{MM:.0f} mmのうち、しみこんだ水{round(P_IN * 100)}%・みぞへ流れた水{round(P_OUT * 100)}%・地面に残る水{round(P_REST * 100)}%を帯グラフで示している。",
         caption="雨水のゆくえ。水は高い所から低い所へ流れて集まり、地面にしみこんだり、みぞから川へ流れたりする。"),
    dict(svg=fig2,
         alt="すな・校庭の土・ねん土っぽい土のつぶを虫めがねで見た様子と、水100 mLが全部しみこむまでの時間（すな約10秒・校庭の土約1分40秒・ねん土っぽい土約14分）、カップの下に出た水の量の時間変化のグラフ。つぶが大きいほど水が速くしみこむことをまとめている。",
         caption="土のつぶの大きさとしみこみ方。つぶが大きいほど、すき間が大きく、水が速くしみこむ。"),
]
