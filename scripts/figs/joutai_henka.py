"""状態変化と粒子（joutai-henka・小4／中1）の授業用の図。
融点・沸点・体積の倍率・加熱グラフの形（横軸の区切り）は、シミュの JS（scripts/rika/sims_ryushi_iden.py の JOUTAI_JS）と同じ値・式。"""
from figlib import *

SUBS = [("水", 0, 100, -40, 140, 999.84, 18.015, "液体"), ("エタノール", -115, 78, -150, 120, 789.3, 46.07, "液体"),
        ("窒素", -210, -196, -230, -150, 807, 28.013, "気体"), ("酸素", -218, -183, -240, -140, 1141, 31.999, "気体"),
        ("水銀", -39, 357, -80, 420, 13546, 200.59, "液体")]
W_NM, W_MP, W_BP, W_LO, W_HI, W_RHO, W_M, _ = SUBS[0]


def v_gas(T, rho, M):                          # JS の vGas：1気圧の気体の体積（液体を1）
    rg = 101325 * M / 1000 / (8.314462 * (T + 273.15)); return rho / rg


def v_liq_water(T):                            # JS の vLiq（水だけ・温度で体積が少し変わる）
    t = max(0, min(100, T))
    rho = 999.97495 * (1 - (t - 3.983035) ** 2 * (t + 301.797) / (522528.9 * (t + 69.34881)))
    return 999.84 / rho


V_ICE = 1.0907                                 # JS：氷は液体の 1.0907 倍
V_STEAM = v_gas(W_BP, W_RHO, W_M)
assert round(V_STEAM, -2) == 1700 and abs(V_ICE / v_liq_water(0) - 1.09) < 0.01


def segs(mp, bp, lo, hi):                      # JS の segs()：加熱グラフの横軸（模式）
    a, b, c = math.sqrt(mp - lo), math.sqrt(bp - mp), math.sqrt(hi - bp); k = 0.58 / (a + b + c)
    w = [a * k, 0.16, b * k, 0.26, c * k]; r = [0.0]
    for v in w: r.append(r[-1] + v)
    r[5] = 1.0
    return r


def T_of(q, B, mp, bp, lo, hi):                # JS の st(q).T
    if q < B[1]: return lo + (mp - lo) * q / B[1]
    if q < B[2]: return mp
    if q < B[3]: return mp + (bp - mp) * (q - B[2]) / (B[3] - B[2])
    if q < B[4]: return bp
    return bp + (hi - bp) * min(1, (q - B[4]) / (B[5] - B[4]))


def mt(v): return str(v).replace("-", "−")


def fr(v): return v - math.floor(v)
def hs1(k): return fr(math.sin(k * 12.9898) * 43758.5453)
def hs2(k): return fr(math.sin(k * 78.233) * 12345.678)


NP = 18                                       # どの状態でも粒子の数は同じ


def particles(kind, x0, y0, w, h):
    out = []
    PR, PD = 13, 28
    if kind == "solid":
        RH = PD * math.sqrt(3) / 2
        pts = [(x0 + w / 2 - 2.5 * PD + c * PD + (PD / 2 if r % 2 else 0) - PD / 4, y0 + h - 20 - r * RH) for r in range(3) for c in range(6)]
        for x, y in pts:
            out.append(circle(x, y, PR, "#7fb3d5", TEAL_D, 1.4))
        for i, (ax, ay) in enumerate(pts):            # 粒子どうしの結びつき（模式）
            for bx, by in pts[i + 1:]:
                if math.hypot(bx - ax, by - ay) < PD * 1.05:
                    out.append(f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{TEAL_D}" stroke-width="1.8" stroke-opacity=".6"/>')
        for x, y in pts[-6::2]:                       # その場でふるえる
            out.append(f'<path d="M{x - 9:.1f},{y - 22:.1f} q-5,-4 0,-8 M{x + 9:.1f},{y - 22:.1f} q5,-4 0,-8" fill="none" stroke="{ACC}" stroke-width="2"/>')
    elif kind == "liquid":
        for k in range(NP):
            c, r = k % 6, k // 6
            x = x0 + w / 2 - 2.5 * PD + c * PD + (hs1(k + 5) - 0.5) * 6 + (PD / 3 if r == 1 else 0) - PD / 6
            y = y0 + h - 20 - r * 26 + (hs2(k + 5) - 0.5) * 5
            out.append(circle(x, y, PR, "#7fb3d5", TEAL_D, 1.4))
        for c in (1, 4):
            x = x0 + w / 2 - 2.5 * PD + c * PD; y = y0 + h - 20 - 3 * 26 + 10
            out.append(f'<path d="M{x - 14:.1f},{y:.1f} q14,-16 28,0" fill="none" stroke="{ACC}" stroke-width="2.2" marker-end="url(#ah-acc)"/>')
    else:
        cw, ch = (w - 40) / 6, (h - 40) / 3
        P = [(x0 + 20 + (k % 6 + 0.5) * cw + (hs1(k + 11) - 0.5) * 14, y0 + 20 + (k // 6 + 0.5) * ch + (hs2(k + 11) - 0.5) * 30) for k in range(NP)]
        for k, (x, y) in enumerate(P):
            if k % 2 == 0:                            # 動きの矢印：箱の中で、ほかの粒子にかからない向きをえらぶ
                a0 = hs1(k * 7 + 3) * 2 * math.pi
                for t in range(24):
                    a = a0 + t * math.pi / 12
                    seg = [(x + math.cos(a) * d, y + math.sin(a) * d) for d in (16, 26, 36)]
                    if all(x0 + 8 < sx < x0 + w - 8 and y0 + 8 < sy < y0 + h - 8 for sx, sy in seg) and                        all(math.hypot(sx - qx, sy - qy) > PR + 5 for sx, sy in seg for j, (qx, qy) in enumerate(P) if j != k):
                        break
                out.append(arrow(x + math.cos(a) * 16, y + math.sin(a) * 16, x + math.cos(a) * 36, y + math.sin(a) * 36, "acc", 2))
        for x, y in P:
            out.append(circle(x, y, PR, "#7fb3d5", TEAL_D, 1.4))
    return "".join(out)


def fig1():
    b = []
    BX = [60, 465, 870]; BW, BY0, BH = 270, 150, 238
    names = [("固体", "（氷）"), ("液体", "（水）"), ("気体", "（水蒸気）")]
    kinds = ["solid", "liquid", "gas"]
    for k in range(3):
        x = BX[k]
        b.append(text(x + BW / 2, 132, names[k][0], 22, INK, 700, "end") + text(x + BW / 2 + 4, 132, names[k][1], 16, INK2))
        b.append(rect(x, BY0, BW, BH, "#f4f8fb", LINE, 8))
        b.append(particles(kinds[k], x, BY0, BW, BH))
    # 状態の変化の矢印（上＝加熱、下＝冷却）
    for k, (up, dn) in enumerate([(("とける", "（融解）"), ("こおる", "（凝固）")), (("ふっとう・蒸発", ""), ("液体にもどる", "（凝縮）"))]):
        xa, xb = BX[k] + BW + 10, BX[k + 1] - 10; xm = (xa + xb) / 2
        b.append(arrow(xa, 236, xb, 236, "acc", 4))
        b.append(text(xm, 222, up[0], 16, ACC, 700, "middle") + (text(xm, 260, up[1], 14, ACC, anchor="middle") if up[1] else ""))
        b.append(arrow(xb, 318, xa, 318, "teal", 4))
        b.append(text(xm, 304, dn[0], 16, TEAL_D, 700, "middle") + text(xm, 342, dn[1], 14, TEAL_D, anchor="middle"))
    # 加熱・冷却の向き
    b.append(text(BX[0] + BW + 12, 176, "加熱 →", 15, ACC, 700) + text(BX[2] - 12, 176, "加熱 →", 15, ACC, 700, "end"))
    b.append(text(BX[0] + BW + 12, 378, "← 冷却", 15, TEAL_D, 700) + text(BX[2] - 12, 378, "← 冷却", 15, TEAL_D, 700, "end"))
    # 説明
    desc = [["規則正しく並ぶ", "その場でふるえる（振動）", "間隔はせまい"],
            ["並び方がくずれる", "位置を入れかえて動き回る", "間隔は固体とあまり変わらない"],
            ["ばらばらに離れる", "空間を自由に飛び回る", "間隔はとても広い"]]
    heads = ["並び方", "動き", "間隔"]
    for k in range(3):
        for j, s in enumerate(desc[k]):
            y = 420 + j * 30
            b.append(text(BX[k] + 4, y, heads[j], 14, MUTED, 700) + text(BX[k] + 54, y, s, 16, INK))
    b.append(text(BX[0] + 4, 512, f"水が氷になると体積は約{V_ICE:.1f}倍", 15, TEAL_D, 700))
    b.append(text(BX[1] + 4, 512, f"粒子の数はどれも{NP}個（同じ）", 15, INK, 700))
    b.append(text(BX[2] + 4, 512, f"水が水蒸気になると約{round(V_STEAM, -2):,.0f}倍（100℃）", 15, ACC, 700))
    b.append(rect(60, 538, 1080, 64, ACC_L, ACC_L, 10))
    b.append(text(600, 566, "状態が変わっても、粒子の数（＝質量）は変わらない。", 18, INK, 700, "middle"))
    b.append(text(600, 590, "変わるのは、粒子の並び方・間隔・動き。だから体積が変わる。", 16, INK2, anchor="middle"))
    return svg("".join(b), "状態変化と粒子のモデル（固体・液体・気体）",
               "粒子の大きさ・数は模式的。温度が高いほど粒子の動きは激しくなる。体積の倍率は液体の水を1としたとき。")


def fig2():
    b = []
    B = segs(W_MP, W_BP, W_LO, W_HI)
    GX0, GX1, GY0, GY1 = 120, 660, 172, 520
    gx = lambda q: GX0 + q * (GX1 - GX0)
    gy = lambda T: GY1 - (T - W_LO) / (W_HI - W_LO) * (GY1 - GY0)
    b.append(text(48, 122, "水を一定の火力で加熱したときの温度", 18, INK, 700))
    fills = ["#e6eff7", "#ece8f3", "#e3f0f3", "#f6eedc", "#fbeae6"]
    names = [["固体", "（氷）"], ["固体と", "液体"], ["液体", "（水）"], ["液体と", "気体"], ["気体", "（水蒸気）"]]
    for i in range(5):
        b.append(f'<rect x="{gx(B[i]):.1f}" y="{GY0}" width="{gx(B[i + 1]) - gx(B[i]):.1f}" height="{GY1 - GY0}" fill="{fills[i]}"/>')
        xm = (gx(B[i]) + gx(B[i + 1])) / 2
        b.append(lines(xm, GY1 + 24, names[i], 15, INK, 1.3, anchor="middle", weight=700))
    for T in range(-40, 141, 20):
        b.append(line(GX0, gy(T), GX1, gy(T), LINE, 1) + text(GX0 - 8, gy(T) + 5, mt(T), 14, INK2, anchor="end"))
    b.append(line(GX0, GY0 - 8, GX0, GY1, INK, 1.6) + line(GX0, GY1, GX1 + 8, GY1, INK, 1.6))
    b.append(text(GX0 - 8, GY0 - 16, "温度［℃］", 15, INK, anchor="start"))
    for T, nm in ((W_MP, "融点"), (W_BP, "沸点")):
        b.append(line(GX0, gy(T), GX1, gy(T), MUTED, 1.4, "5 4"))
    pts = [(gx(k / 400), gy(T_of(k / 400, B, W_MP, W_BP, W_LO, W_HI))) for k in range(401)]
    b.append(poly(pts, INK, 3.4))
    b.append(text(gx((B[1] + B[2]) / 2), gy(W_MP) - 12, f"融点 {mt(W_MP)}℃", 16, TEAL_D, 700, "middle"))
    b.append(text(gx((B[3] + B[4]) / 2), gy(W_BP) - 12, f"沸点 {mt(W_BP)}℃", 16, ACC, 700, "middle"))
    b.append(text(gx((B[1] + B[2]) / 2), gy(W_MP) + 26, "とけている間", 14, INK2, anchor="middle"))
    b.append(text(gx((B[3] + B[4]) / 2), gy(W_BP) + 26, "ふっとうしている間", 14, INK2, anchor="middle"))
    b.append(text(GX1, GY1 + 70, "加熱した時間 →（横軸は模式的）", 14, MUTED, anchor="end"))
    # 右：融点・沸点の表とポイント
    RX = 710
    b.append(text(RX, 122, "物質の融点と沸点（1気圧）", 18, INK, 700))
    rows = [[nm, mt(mp) + "℃", mt(bp) + "℃", st] for nm, mp, bp, lo, hi, rho, M, st in SUBS]
    b.append(table(RX, 138, ["物質", "融点", "沸点", "20℃では"], rows, [130, 104, 104, 104], 42, 16.5))
    pts2 = ["融点・沸点では、加熱しても温度が上がらない", "（熱が状態を変えるのに使われる）",
            "融点・沸点は物質によって決まっている", "（量が多いと、平らな部分が長くなるだけ）"]
    for k in range(2):
        y = 438 + k * 76
        b.append(rect(RX, y - 26, 442, 66, CARD, LINE, 8))
        b.append(badge(RX + 22, y - 2, str(k + 1), TEAL, "#fff", 15))
        b.append(text(RX + 44, y + 2, pts2[2 * k], 15.5, INK, 700) + text(RX + 44, y + 26, pts2[2 * k + 1], 14, INK2))
    return svg("".join(b), "加熱したときの温度変化と融点・沸点（まとめ）",
               "純粋な物質は、とけている間・ふっとうしている間は温度が一定になる。混合物では平らにならない。")


FIGS = [
    dict(svg=fig1,
         alt=f"固体（氷）・液体（水）・気体（水蒸気）の粒子のモデル図。固体は規則正しく並んでその場でふるえ、液体は並び方がくずれて動き回り、気体はばらばらに離れて飛び回る。加熱すると固体→液体（融解）→気体（沸騰・蒸発）、冷却するとその逆に変わる。粒子の数（質量）は変わらず、水が氷になると体積は約{V_ICE:.1f}倍、水蒸気になると約1,700倍になる。",
         caption="状態変化と粒子のモデル。変わるのは粒子の並び方・間隔・動きで、粒子の数（質量）は変わらない。"),
    dict(svg=fig2,
         alt="水を一定の火力で加熱したときの温度変化のグラフ。−40℃の氷から温めると、融点0℃と沸点100℃で温度が一定（平ら）になる。水・エタノール・窒素・酸素・水銀の融点と沸点の表もある。",
         caption="加熱したときの温度変化と融点・沸点。純粋な物質は、状態が変わっている間は温度が一定になる。"),
]
