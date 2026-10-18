"""模様が生まれる（turing）の図。計算はページの JS と同じ（グレイ・スコット模型・120×120マス・Du=0.16・Dv=0.08・dt=1・
はじめは u=1、真ん中の16×16マスだけ v=1・いちばん外側のマスは計算しない。模様ごとの F・k も JS の値）。
JS と同じく Float32 に保存しながら、同じ順番で足し算をする。"""
from figlib import *

N = 120
DU, DV = 0.16, 0.08
PATTERNS = [("spots", "水玉・ヒョウ柄", 0.035, 0.065), ("stripes", "しま模様", 0.055, 0.062), ("maze", "迷路", 0.029, 0.057)]
SNAP = (1000, 4000, 8000, 16000)
_CACHE = {}


def simulate(key, f, k):
    """ページの JS の init()/step() と同じ計算。SNAP のステップ数ごとに U・V を記録する。"""
    if key in _CACHE: return _CACHE[key]
    import numpy as np
    U = np.ones((N, N), np.float32); V = np.zeros((N, N), np.float32)
    V[N // 2 - 8:N // 2 + 8, N // 2 - 8:N // 2 + 8] = 1
    c = (slice(1, N - 1), slice(1, N - 1))
    out = {}
    for s in range(1, max(SNAP) + 1):
        u = U.astype(np.float64); v = V.astype(np.float64)
        lu = u[1:-1, :-2] + u[1:-1, 2:] + u[:-2, 1:-1] + u[2:, 1:-1] - 4 * u[c]
        lv = v[1:-1, :-2] + v[1:-1, 2:] + v[:-2, 1:-1] + v[2:, 1:-1] - 4 * v[c]
        uvv = u[c] * v[c] * v[c]
        U2 = U.copy(); V2 = V.copy()
        U2[c] = u[c] + (DU * lu - uvv + f * (1 - u[c])) * 1
        V2[c] = v[c] + (DV * lv + uvv - (k + f) * v[c]) * 1
        U, V = U2, V2
        if s in SNAP: out[s] = (U.copy(), V.copy())
    _CACHE[key] = out
    return out


def pattern_svg(x, y, V, cs, thr=0.2):
    """v が thr より多いマスを、横につながった帯ごとに1本の path で描く（ファイルを小さくするため）"""
    d = []
    for i in range(N):
        j = 0
        while j < N:
            if V[i, j] > thr:
                k = j
                while k < N and V[i, k] > thr: k += 1
                w = (k - j) * cs
                d.append(f"M{x + j * cs:.1f} {y + i * cs:.1f}h{w:.1f}v{cs}h-{w:.1f}z")
                j = k
            else:
                j += 1
    return (f'<rect x="{x}" y="{y}" width="{N * cs}" height="{N * cs}" fill="{TEAL_L}" stroke="{INK2}" stroke-width="1"/>'
            f'<path d="{"".join(d)}" fill="{TEAL_D}" shape-rendering="crispEdges"/>')


def fig1():
    b = []
    # 左：2つの物質
    cards = [("v", "ふえる物質", ACC, ACC_L, ["u を使って、自分をふやす（式の uv²）", f"ゆっくり広がる（Dᵥ＝{DV}）", "少しずつ取りのぞかれる（除去率 k）"]),
             ("u", "材料", TEAL, TEAL_L, ["外から少しずつ補給される（補給率 F）", f"速く広がる（Dᵤ＝{DU}・v の2倍）", "v がふえる所で使われて減る"])]
    for i, (sym, nm, col, bg, rows) in enumerate(cards):
        y = 104 + i * 130
        b.append(rect(48, y, 476, 122, bg, col, 10, 1.6))
        b.append(text(72, y + 36, sym, 30, col, 700) + text(104, y + 34, nm, 20, INK, 700))
        b.append(lines(72, y + 64, rows, 15.5, INK2, 1.4))
    b.append(rect(48, 366, 476, 94, CARD, LINE, 10))
    b.append(lines(68, 394, ["一般には「活性因子（自分をふやす）」と「抑制因子", "（それをおさえる・速く広がる）」の組で説明される。", "この式では v が活性因子、速く広がる u の不足が抑えの役。"], 15, INK2, 1.45))
    # 右：水玉の断面（シミュと同じ計算）
    U, V = simulate("spots", 0.035, 0.065)[16000]
    row, j0, j1 = 16, 10, 110
    gx, gy, gw, gh = 600, 430, 520, 228
    b.append(text(560, 126, "水玉模様を横に切った断面（16,000ステップ後）", 17, INK, 700))
    b.append(axes(gx, gy, gw, gh, "位置", "", [], [(v * gh, f"{v:.1f}") for v in (0, 0.5, 1.0)], 14))
    b.append(text(gx - 12, gy - gh - 18, "濃さ", 14, INK, anchor="end"))
    b.append(line(820, 160, 856, 160, ACC, 3.2) + text(864, 166, "v（ふえる物質）", 15, ACC, 700)
             + line(1000, 160, 1036, 160, TEAL, 2.6, "7 5") + text(1044, 166, "u（材料）", 15, TEAL_D, 700))
    sx = gw / (j1 - j0 - 1)
    b.append(poly([(gx + (j - j0) * sx, gy - float(U[row, j]) * gh) for j in range(j0, j1)], TEAL, 2.6, dash="7 5"))
    b.append(poly([(gx + (j - j0) * sx, gy - float(V[row, j]) * gh) for j in range(j0, j1)], ACC, 3.2))
    b.append(text(gx + gw / 2, gy + 24, "← 横1列のマスの位置 →", 14, MUTED, anchor="middle"))
    # 下：しくみの流れ
    steps = [["v が少しふえた所で、", "まわりの u がどんどん使われる"],
             ["u は速く広がるので、", "まわりの広い範囲で u が足りなくなる"],
             ["すぐとなりでは v がふえられず、", "少しはなれた所に次の v の山ができる"]]
    for i, rows in enumerate(steps):
        x = 48 + i * 376
        b.append(rect(x, 478, 352, 86, CARD, LINE, 10) + badge(x + 28, 521, str(i + 1), ACC if i == 2 else TEAL, "#fff", 16))
        b.append(lines(x + 54, 512, rows, 15.5, INK, 1.5))
        if i < 2: b.append(arrow(x + 354, 521, x + 372, 521, "ink", 2.2))
    b.append(text(600, 600, "→ 近くでふえ、はなれた所ではおさえられる。これがくり返されて、間かくのそろった模様になる。", 16, INK, 700, "middle"))
    return svg("".join(b), "模様が生まれるしくみ（反応拡散）",
               "式：∂u/∂t＝Dᵤ∇²u − uv² ＋ F(1−u)、∂v/∂t＝Dᵥ∇²v ＋ uv² − (F＋k)v（グレイ・スコット模型）")


def fig2():
    b = [text(48, 124, "シミュと同じ式・同じ F と k で計算した模様の育ち方（濃い色＝v が多い所）", 17, INK, 700)]
    cs = 1.2
    xs = [330, 540, 750, 960]
    for c, s in enumerate(SNAP):
        b.append(text(xs[c] + N * cs / 2, 160, f"{s:,}ステップ後", 16, INK2, 700, "middle"))
    for r, (key, nm, f, k) in enumerate(PATTERNS):
        snaps = simulate(key, f, k)
        y = 170 + r * 150
        b.append(text(48, y + 58, nm, 21, INK, 700))
        b.append(text(48, y + 90, f"F＝{f}　k＝{k}", 17, INK2))
        for c, s in enumerate(SNAP):
            b.append(pattern_svg(xs[c], y, snaps[s][1], cs))
    return svg("".join(b), "F と k で変わる模様（シミュの計算結果）",
               "1ステップ＝式を1回計算。シミュは1コマに8ステップ進む。はじめは真ん中の小さな四角だけに v を置いている。")


FIGS = [
    dict(svg=fig1, alt="反応拡散で模様が生まれるしくみの図。ふえる物質 v はゆっくり広がり、材料 u は速く広がる。水玉模様の断面のグラフでは、v の山の所で u が大きく減っている。v がふえるとまわりの u が足りなくなり、少しはなれた所に次の山ができることを3つの段階で示している。",
         caption="反応拡散（チューリングパターン）のしくみ。近くでふえ、はなれた所ではおさえられることで、間かくのそろった模様になる。"),
    dict(svg=fig2, alt="グレイ・スコット模型で、水玉・ヒョウ柄（F=0.035、k=0.065）、しま模様（F=0.055、k=0.062）、迷路（F=0.029、k=0.057）の3つの設定ごとに、1,000・4,000・8,000・16,000ステップ後の模様の育ち方を並べた図。",
         caption="F と k による模様のちがい（シミュと同じ計算）。真ん中の小さな四角から、設定ごとにちがう模様が広がる。"),
]
