"""鳥の群れ（boids）の図。数値はページの JS と同じ（見える範囲 半径40・近すぎる範囲 d²<260＝約16・
整列0.05・結合0.0008・分離0.02・ゆらぎ±0.05・最高速度2.6・画面520×360で端は反対側とつながる）。"""
import math
import random
from figlib import *

ANCHOR = r"<h2>3つのルール</h2>\s*<ul>.*?</ul>\n"
W0, H0 = 520, 360                       # シミュの画面
R_VIEW, SEP2 = 40, 260                  # 見える範囲の半径・分離の距離²
A_W, C_W, S_W, VMAX = 0.05, 0.0008, 0.02, 2.6


def bird(x, y, ang, size=15, fill=TEAL, stroke="none"):
    """進む向き ang（度・画面の右が0、時計回りが正）を向いた三角"""
    a = math.radians(ang); ca, sa = math.cos(a), math.sin(a)
    pts = [(size, 0), (-0.65 * size, 0.5 * size), (-0.65 * size, -0.5 * size)]
    p = " ".join(f"{x + px * ca - py * sa:.1f},{y + px * sa + py * ca:.1f}" for px, py in pts)
    return f'<polygon points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>'


def dcircle(cx, cy, r, color, dash="6 5", width=1.8, fill="none"):
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{color}" stroke-width="{width}" stroke-dasharray="{dash}"/>'


def fig1():
    b = []
    S = 2.6                                   # シミュの長さ1 → 図の2.6px
    pw, gap = 352, 24
    sep_r = math.sqrt(SEP2)
    panels = []
    # 1 分離：近すぎる範囲（約16）の中の仲間から離れる。JS：sx -= dx, sy -= dy
    nb1 = [(10, -8, 0), (-4, 12, 0)]
    for dx, dy, _ in nb1: assert dx * dx + dy * dy < SEP2
    sx, sy = -sum(d[0] for d in nb1), -sum(d[1] for d in nb1)
    panels.append(("分離", "近づきすぎたら離れる", nb1, (sx, sy), "離れる向き",
                   [f"約{sep_r:.0f}より近い仲間がいると、", "その仲間と反対の向きに押される", f"（強さ {S_W}）"]))
    # 2 整列：見える範囲の仲間の平均の速度に近づける
    nb2 = [(-26, -14, -40), (4, -33, -55), (-6, 28, -35), (26, 18, -48), (-30, 12, -42)]
    for dx, dy, _ in nb2: assert SEP2 < dx * dx + dy * dy < R_VIEW ** 2
    avg = math.degrees(math.atan2(sum(math.sin(math.radians(a)) for *_, a in nb2), sum(math.cos(math.radians(a)) for *_, a in nb2)))
    panels.append(("整列", "まわりと進む向きを合わせる", nb2, None, "", [f"見える範囲（半径{R_VIEW}）の仲間の", "平均の速度に、1コマごとに", f"{A_W * 100:.0f}%ずつ近づける"]))
    # 3 結合：見える範囲の仲間の重心へ寄る
    nb3 = [(-34, -18, 10), (-34, 18, -5), (-20, -30, 20), (-20, 30, 0)]
    for dx, dy, _ in nb3: assert SEP2 < dx * dx + dy * dy < R_VIEW ** 2
    gx3, gy3 = sum(d[0] for d in nb3) / 4, sum(d[1] for d in nb3) / 4
    panels.append(("結合", "群れの中心へ寄っていく", nb3, (gx3, gy3), "重心へ",
                   ["見える範囲の仲間の重心（平均の", "位置）へ向かう。強さは", f"重心までの距離×{C_W}"]))
    for k, (nm, sub, nbs, force, flabel, desc) in enumerate(panels):
        px = 48 + k * (pw + gap); cx, cy = px + pw / 2, 104 + 196
        b.append(rect(px, 104, pw, 424, CARD, LINE, 12))
        b.append(badge(px + 32, 140, str(k + 1), TEAL, "#fff", 16) + text(px + 56, 149, nm, 25, INK, 700)
                 + text(px + 116, 148, sub, 16, INK2))
        b.append(dcircle(cx, cy, R_VIEW * S, MUTED))
        b.append(text(cx, cy - R_VIEW * S - 12, f"見える範囲（半径{R_VIEW}）", 14, MUTED, anchor="middle"))
        if nm == "分離":
            b.append(dcircle(cx, cy, sep_r * S, ACC, "4 4", 1.8, ACC_L))
            b.append(text(cx, cy - sep_r * S - 8, f"近すぎる範囲（約{sep_r:.0f}）", 14, ACC, anchor="middle"))
        for dx, dy, ang in nbs:
            b.append(bird(cx + dx * S, cy + dy * S, ang, 14, TEAL))
        b.append(bird(cx, cy, -90 if nm == "結合" else 0, 17, ACC))
        if nm == "整列":
            ar = math.radians(avg)
            b.append(arrow(cx + 4, cy, cx + 74, cy, "muted", 2))
            b.append(text(cx + 12, cy + 26, "いまの向き", 14, MUTED))
            tx, ty = cx + 72 * math.cos(ar), cy + 72 * math.sin(ar)
            b.append(arrow(cx, cy, tx, ty, "acc", 3.4))
            b.append(lines(tx + 10, ty - 6, ["仲間の", "平均の向き"], 15, ACC, 1.3, weight=700,
                           stroke="#fff", stroke_width=5, paint_order="stroke"))
        else:
            fx, fy = force; L = math.hypot(fx, fy)
            ex, ey = cx + fx / L * 70, cy + fy / L * 70
            if nm == "結合":
                gx, gy = cx + fx * S, cy + fy * S
                b.append(line(gx - 7, gy - 7, gx + 7, gy + 7, INK, 3) + line(gx - 7, gy + 7, gx + 7, gy - 7, INK, 3))
                b.append(text(gx, gy + 28, "重心", 15, INK, 700, "middle"))
                ex, ey = cx + fx * S * 0.8, cy + fy * S * 0.8
                b.append(arrow(cx, cy, ex, ey, "acc", 3.4))
                b.append(text((cx + ex) / 2, cy - 14, "重心へ寄る", 15, ACC, 700, "middle"))
            else:
                b.append(arrow(cx, cy, ex, ey, "acc", 3.4))
                b.append(text(ex - 6, ey + 26, flabel, 15, ACC, 700, "end"))
        b.append(lines(px + 24, 446, desc, 16, INK2, 1.5))
    # 1コマの計算
    b.append(rect(48, 542, 1104, 74, TEAL_L, TEAL_L, 10))
    b.append(text(70, 572, "1コマごとの計算", 16, TEAL_D, 700))
    b.append(text(70, 601, "速度に「整列＋結合＋分離＋小さなゆらぎ」を足す → 速さは最大2.6まで → その速度で位置を動かす", 17, INK))
    return svg("".join(b), "鳥の群れ（ボイド）の3つのルール",
               "距離・速さはシミュの画面（520×360）の単位。どの鳥も、見える範囲の仲間だけを見て動いている。（大きさは見やすく拡大）")


def simulate(seed=1, n=90, frames=1200, every=15):
    """ページの JS の init()/step() と同じ計算（乱数だけ Python の固定シード）。向きのそろい具合と位置を記録する。"""
    rnd = random.Random(seed)
    b = [[rnd.random() * W0, rnd.random() * H0, rnd.random() * 2 - 1, rnd.random() * 2 - 1] for _ in range(n)]
    R2 = R_VIEW * R_VIEW
    rec, snaps = [], {}

    def order():
        sx = sum(p[2] / math.hypot(p[2], p[3]) for p in b); sy = sum(p[3] / math.hypot(p[2], p[3]) for p in b)
        return math.hypot(sx, sy) / n
    for f in range(frames + 1):
        if f % every == 0:
            rec.append((f, order())); snaps[f] = [tuple(p) for p in b]
        if f == frames: break
        for p in b:
            ax = ay = cx = cy = sx = sy = 0.0; cnt = 0
            for q in b:
                if q is p: continue
                dx, dy = q[0] - p[0], q[1] - p[1]; d2 = dx * dx + dy * dy
                if 0 < d2 < R2:
                    ax += q[2]; ay += q[3]; cx += q[0]; cy += q[1]; cnt += 1
                    if d2 < SEP2: sx -= dx; sy -= dy
            if cnt:
                ax /= cnt; ay /= cnt; cx /= cnt; cy /= cnt
                p[2] += (ax - p[2]) * A_W + (cx - p[0]) * C_W + sx * S_W
                p[3] += (ay - p[3]) * A_W + (cy - p[1]) * C_W + sy * S_W
            p[2] += (rnd.random() - .5) * 0.1; p[3] += (rnd.random() - .5) * 0.1
            sp = math.hypot(p[2], p[3])
            if sp > VMAX: p[2] = p[2] / sp * VMAX; p[3] = p[3] / sp * VMAX
            p[0] = (p[0] + p[2] + W0) % W0; p[1] = (p[1] + p[3] + H0) % H0
    return rec, snaps


_CACHE = {}


def fig2():
    if "sim" not in _CACHE: _CACHE["sim"] = simulate()
    rec, snaps = _CACHE["sim"]
    od = dict(rec)
    b = [text(48, 124, "シミュと同じ計算で90羽を動かした一例（1秒＝60コマとして）", 18, INK, 700)]
    sc, gap = 0.48, 34
    for k, (f, lab) in enumerate([(0, "はじめ"), (120, "約2秒後"), (300, "約5秒後"), (600, "約10秒後")]):
        x0 = 48 + 2 + k * (W0 * sc + gap); y0 = 168
        b.append(text(x0, y0 - 12, lab, 17, INK, 700))
        b.append(rect(x0, y0, W0 * sc, H0 * sc, CARD, INK2, 4, 1.2))
        b.append(f'<svg x="{x0:.1f}" y="{y0:.1f}" width="{W0 * sc:.1f}" height="{H0 * sc:.1f}">')   # はみ出しを切る
        for (x, y, vx, vy) in snaps[f]:
            b.append(bird(x * sc, y * sc, math.degrees(math.atan2(vy, vx)), 6.5, TEAL))
        b.append('</svg>')
        b.append(text(x0 + W0 * sc / 2, y0 + H0 * sc + 30, f"向きのそろい具合 {od[f]:.2f}", 17, ACC if k == 3 else INK2, 700, "middle"))
    # 下：向きのそろい具合のグラフ
    gx, gy, gw, gh = 150, 588, 900, 150
    secs = [0, 5, 10, 15, 20]
    b.append(axes(gx, gy, gw, gh, "時間", "", [(s * 60 / 1200 * gw, f"{s}秒") for s in secs],
                  [(v * gh, f"{v:.1f}") for v in (0, 0.5, 1.0)], 14))
    b.append(text(gx - 12, gy - gh - 22, "向きのそろい具合", 15, INK, anchor="start"))
    b.append(poly([(gx + f / 1200 * gw, gy - v * gh) for f, v in rec], ACC, 2.6))
    for f in (0, 120, 300, 600):
        b.append(circle(gx + f / 1200 * gw, gy - od[f] * gh, 4.5, ACC, ACC, 0))
    return svg("".join(b), "だれも指揮していないのに群れになる（シミュの一例）",
               "向きのそろい具合＝全員の向きの平均（0＝ばらばら、1＝全員が同じ向き）。乱数を使うので、毎回少しずつちがう。")


FIGS = [
    dict(svg=fig1, alt="ボイド（鳥の群れ）の3つのルールの図。近すぎる範囲（約16）の仲間から離れる分離、見える範囲（半径40）の仲間の平均の速度に5%ずつ近づける整列、仲間の重心へ寄る結合を、真ん中の1羽と仲間の位置・矢印で示している。",
         caption="群れの3つのルール。1羽ずつが「見える範囲の仲間」だけを見て、分離・整列・結合の3つを足して進む。"),
    dict(svg=fig2, alt="ボイドのシミュレーションで90羽がはじめはばらばらの向きから、約2秒後・約5秒後・約10秒後と群れになっていくようすと、向きのそろい具合が0.1前後から約0.9まで上がるグラフ。",
         caption="群れができていくようす（シミュと同じ計算の一例）。まわりに合わせるだけで、全体の向きがそろっていく。"),
]
