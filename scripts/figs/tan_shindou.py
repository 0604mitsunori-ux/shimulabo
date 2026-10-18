"""単振動（tan-shindou）の授業用の図。
数値はシミュ（scripts/rika/sims_kou_butsuri.py の TAN_JS）と同じ式：
  ω＝√(k/m)、T＝2π/ω、x＝A cos ωt（端からはなす）、v＝−Aω sin ωt、a＝−ω²x、単振り子 T₀＝2π√(L/g)（g＝9.8）。
例の値はシミュの初期設定（k＝20 N/m・m＝0.50 kg・A＝10 cm、L＝1.00 m）。"""
import math
from figlib import *

G = 9.8
K0, M0, A0, L0 = 20, 0.50, 0.10, 1.00
W0 = math.sqrt(K0 / M0)
T0 = 2 * math.pi / W0
TP = 2 * math.pi * math.sqrt(L0 / G)


PDEFS = (f'<marker id="ah-purple" markerWidth="10" markerHeight="10" refX="7" refY="5" orient="auto" markerUnits="userSpaceOnUse">'
         f'<path d="M0,0 L10,5 L0,10z" fill="{PURPLE}"/></marker>')


def parrow(x1, y1, x2, y2, width=2.8):
    """紫の矢印（速度）"""
    return line(x1, y1, x2, y2, PURPLE, width) .replace("/>", ' marker-end="url(#ah-purple)"/>')


def spring(x1, x2, y, n=14, amp=9):
    pts = [(x1, y), (x1 + 8, y)]
    a, b = x1 + 8, x2 - 6
    for i in range(n):
        pts.append((a + (b - a) * (i + 0.5) / n, y + (amp if i % 2 else -amp)))
    pts += [(b, y), (x2, y)]
    return poly(pts, INK2, 2)


def fig1():
    CX, CY, R, th = 300, 290, 130, math.radians(50)
    px, py = CX + R * math.cos(th), CY - R * math.sin(th)
    LV, LA = 100, 80                                  # 矢印の長さ（見やすさ優先）
    b = []
    b.append(text(60, 128, "等速円運動", 17, TEAL, 700))
    b.append(text(60, 152, "（半径 A・角速度 ω）", 15, TEAL, 700))
    b.append(circle(CX, CY, R, "none", TEAL, 2))
    b.append(line(CX - R - 24, CY, CX + R + 24, CY, MUTED, 1.2, "5 5"))
    a0 = 30
    b.append(f'<path d="M{CX + a0},{CY} A{a0},{a0} 0 0 0 {CX + a0 * math.cos(th):.1f},{CY - a0 * math.sin(th):.1f}" fill="none" stroke="{TEAL}" stroke-width="2"/>')
    b.append(text(CX + 48 * math.cos(th / 2), CY - 48 * math.sin(th / 2) + 6, "ωt", 17, TEAL, 700, "middle"))
    b.append(line(CX, CY, px, py, TEAL, 2))
    b.append(circle(CX, CY, 3.5, INK, INK, 0))
    b.append(text(CX - 8, CY + 22, "O", 15, INK2, 700, "end"))
    # 円運動の速度（接線）と向心加速度
    vx, vy = -math.sin(th), -math.cos(th)
    b.append(parrow(px, py, px + LV * vx, py + LV * vy))
    b.append(text(px + LV * vx + 14, py + LV * vy + 2, "速度（大きさ Aω）", 15, PURPLE, 700))
    ax, ay = -math.cos(th), math.sin(th)
    b.append(arrow(px, py, px + LA * ax, py + LA * ay, "acc", 2.8))
    b.append(lines(px + LA * ax - 14, py + LA * ay - 24, ["向心加速度", "（大きさ Aω²）"], 15, ACC, 1.35, anchor="end", font_weight=700))
    b.append(circle(px, py, 7, TEAL, TEAL, 0) + text(px + 12, py - 8, "P", 18, TEAL, 700))
    # 正射影（真下の影）
    FY = 560
    b.append(line(px, py + 8, px, FY - 50, TEAL, 1.6, "6 5"))
    b.append(text(px + 10, 440, "真下への影", 15, TEAL, 700))
    b.append(text(px + 10, 460, "（正射影）", 15, TEAL, 700))
    # ばね・おもり
    b.append(f'<rect x="56" y="{FY - 66}" width="12" height="66" fill="{LINE}" stroke="{INK2}" stroke-width="1.2"/>')
    b.append(line(56, FY, 470, FY, INK2, 2.4))
    b.append(spring(68, px - 30, FY - 23))
    b.append(rect(px - 30, FY - 46, 60, 46, TEAL, TEAL_D, 6, 1.4) + text(px, FY - 16, "m", 18, "#fff", 700, "middle"))
    b.append(parrow(px, FY - 66, px + LV * vx, FY - 66))
    b.append(text(px + LV * vx - 8, FY - 60, "v", 18, PURPLE, 700, "end"))
    b.append(arrow(px, FY - 90, px + LA * ax, FY - 90, "acc", 2.8))
    b.append(text(px + LA * ax - 8, FY - 84, "a", 18, ACC, 700, "end"))
    for x, t in [(CX - R, "−A"), (CX, "O"), (CX + R, "+A")]:
        b.append(line(x, FY, x, FY + 8, INK2, 1.6) + text(x, FY + 28, t, 16, INK2, 700, "middle"))
    b.append(line(CX, FY - 60, CX, FY, MUTED, 1.2, "3 4"))

    # 右：式の流れ
    X = 610
    b.append(text(X, 128, "円運動を真下に写すと、単振動になる", 20, INK, 700))
    rows = [("1", "おもりの位置 x ＝ 点Pの影", "x ＝ A cos ωt", TEAL),
            ("2", "速度 v ＝ 円運動の速度の影", "v ＝ −Aω sin ωt　（速さの最大値 Aω）", PURPLE),
            ("3", "加速度 a ＝ 向心加速度の影", "a ＝ −Aω² cos ωt ＝ −ω²x", ACC),
            ("4", "運動方程式 ma ＝ −kx とくらべると", "ω ＝ √(k/m)　→　T ＝ 2π/ω ＝ 2π√(m/k)", INK)]
    y = 172
    for no, t1, t2, col in rows:
        b.append(badge(X + 12, y - 6, no, col, "#fff", 15))
        b.append(text(X + 34, y, t1, 16.5, INK2))
        b.append(text(X + 34, y + 30, t2, 19, col, 700))
        y += 76
    b.append(rect(X, 470, 540, 140, TEAL_L, LINE, 10))
    b.append(text(X + 18, 500, "例（シミュの最初の設定）k＝20 N/m、m＝0.50 kg、A＝0.10 m", 15.5, INK2, 700))
    b.append(text(X + 18, 534, f"ω ＝ √(20÷0.50) ＝ {W0:.2f} rad/s　　T ＝ {T0:.3f} s", 18, INK, 700))
    b.append(text(X + 18, 566, f"速さの最大値 Aω ＝ {A0 * W0:.3f} m/s", 17, PURPLE, 700))
    b.append(text(X + 18, 596, f"加速度の大きさの最大値 Aω² ＝ {A0 * W0 * W0:.2f} m/s²", 17, ACC, 700))
    return svg("".join(b), "単振動のしくみ（等速円運動の正射影）",
               "x＝A cos ωt は、時刻0に端（x＝＋A）ではなしたとき（シミュの動き）。矢印の長さは見やすくかいた。", PDEFS)


def fig2():
    GX0, GX1 = 170, 650
    b = []
    rows = [("変位 x", "A", lambda p: math.cos(p), TEAL, 178),
            ("速度 v", "Aω", lambda p: -math.sin(p), PURPLE, 318),
            ("加速度 a", "Aω²", lambda p: -math.cos(p), ACC, 458)]
    HH, AMP = 50, 44
    for nm, mx, fn, col, cy in rows:
        b.append(f'<rect x="{GX0}" y="{cy - HH}" width="{GX1 - GX0}" height="{2 * HH}" fill="{CARD}" stroke="{LINE}"/>')
        for j in range(5):
            x = GX0 + (GX1 - GX0) * j / 4
            b.append(line(x, cy - HH, x, cy + HH, LINE, 1.2, None if j % 2 == 0 else "4 4"))
        b.append(line(GX0, cy, GX1, cy, MUTED, 1.2))
        b.append(text(GX0 - 10, cy - AMP + 5, "+" + mx, 14, INK2, anchor="end"))
        b.append(text(GX0 - 10, cy + 5, "0", 14, INK2, anchor="end"))
        b.append(text(GX0 - 10, cy + AMP + 5, "−" + mx, 14, INK2, anchor="end"))
        b.append(text(56, cy + 6, nm, 18, col, 700))
        pts = [(GX0 + (GX1 - GX0) * i / 200, cy - AMP * fn(2 * math.pi * i / 200)) for i in range(201)]
        b.append(poly(pts, col, 3))
    for j, s in enumerate(["0（端）", "T/4（中心）", "T/2（端）", "3T/4（中心）", "T（端）"]):
        x = GX0 + (GX1 - GX0) * j / 4
        b.append(text(x, 534, s, 15, INK2, 700, "start" if j == 0 else ("end" if j == 4 else "middle")))
    b.append(text(60, 534, "時間 t →", 15, INK2, 700))
    b.append(text(60, 572, "・v は x より 1/4 周期進む（山が 1/4 周期早く来る）", 16, INK))
    b.append(text(60, 600, "・a は x と逆向き（逆位相）：a ＝ −ω²x", 16, INK))

    X, Wd = 700, 450
    b.append(rect(X, 108, Wd, 120, CARD, LINE, 10))
    b.append(text(X + 18, 140, "つり合いの位置（x＝0）", 18, INK, 700))
    b.append(text(X + 18, 172, "速さ：最大（Aω）", 17, PURPLE, 700))
    b.append(text(X + 18, 204, "加速度・復元力：0", 17, ACC, 700))
    b.append(rect(X, 240, Wd, 150, CARD, LINE, 10))
    b.append(text(X + 18, 272, "振動の端（x＝±A）", 18, INK, 700))
    b.append(text(X + 18, 304, "速さ：0", 17, PURPLE, 700))
    b.append(text(X + 18, 336, "加速度の大きさ：最大（Aω²）", 17, ACC, 700))
    b.append(text(X + 18, 368, "復元力の大きさ：最大（kA）", 17, ACC, 700))
    b.append(rect(X, 402, Wd, 210, TEAL_L, LINE, 10))
    b.append(text(X + 18, 434, "周期は振幅によらない", 18, INK, 700))
    b.append(text(X + 18, 470, "ばね振り子　T ＝ 2π√(m/k)", 19, TEAL_D, 700))
    b.append(text(X + 34, 498, f"例 k＝20 N/m、m＝0.50 kg → T＝{T0:.3f} s", 15.5, INK2))
    b.append(text(X + 18, 540, "単振り子　T ＝ 2π√(L/g)", 19, TEAL_D, 700))
    b.append(text(X + 34, 568, "（振れ角が小さいとき）", 14.5, MUTED))
    b.append(text(X + 34, 594, f"例 L＝1.00 m、g＝9.8 m/s² → T＝{TP:.2f} s", 15.5, INK2))
    return svg("".join(b), "単振動の x・v・a のグラフと周期（まとめ）",
               "グラフは時刻0に端（x＝＋A）ではなしたとき。縦の目もりは、それぞれの量の最大値に合わせた。")


FIGS = [
    dict(svg=fig1, alt="単振動のしくみの図。半径A・角速度ωで等速円運動する点Pを真下に正射影すると、ばね振り子のおもりの位置 x＝A cos ωt になり、円運動の速度（大きさAω）と向心加速度（大きさAω²）の影が単振動の速度vと加速度a＝−ω²xになること、ma＝−kxから周期T＝2π√(m/k)が導かれることを示す。",
         caption="等速円運動の正射影としての単振動。速度・加速度も円運動の速度・向心加速度の影になる。"),
    dict(svg=fig2, alt="単振動の変位x・速度v・加速度aの時間変化のグラフ（1周期分、1/4周期ごとの目もり）。vはxより1/4周期進み、aはxと逆位相。つり合いの位置と振動の端での速さ・加速度・復元力のまとめと、ばね振り子の周期T＝2π√(m/k)・単振り子の周期T＝2π√(L/g)の式と計算例。",
         caption="x・v・aのグラフと周期の式のまとめ。周期は振幅によらない。"),
]
