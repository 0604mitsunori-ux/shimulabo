"""電気回路（denki-kairo）の授業用の図。回路図記号は JIS C 0617（教科書の電気用図記号）。
数値はページのシミュと同じ式：直列 R＝R1＋R2・I＝V÷R、並列 1/R＝1/R1＋1/R2・I1＝V÷R1（電源6 V・R1＝10 Ω・R2＝20 Ω＝本文の計算例）。
小4：かん電池1個1.5 V、豆電球・モーター7.5 Ω、内部抵抗0（シミュの RL・E1 と同じ）。"""
from figlib import *

V0, R1, R2 = 6.0, 10.0, 20.0
RS = R1 + R2; IS = V0 / RS; VS1, VS2 = IS * R1, IS * R2                 # 直列
RP = R1 * R2 / (R1 + R2); IP1, IP2 = V0 / R1, V0 / R2; IP = IP1 + IP2    # 並列
E1, RL = 1.5, 7.5
I_ONE, I_SER, I_PAR = E1 / RL, 2 * E1 / RL, E1 / RL                      # 小4（へい列は1個あたり半分）


def g(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return s


# ---------- 電気用図記号（JIS C 0617） ----------
def cell_v(x, cy, plus_up=True):
    """電池・直流電源（縦の導線上）。長い細い線＝＋極、短い太い線＝－極"""
    yp, ym = (cy - 7, cy + 7) if plus_up else (cy + 7, cy - 7)
    return (f'<line x1="{x - 24}" y1="{yp}" x2="{x + 24}" y2="{yp}" stroke="{INK}" stroke-width="2.6"/>'
            f'<line x1="{x - 12}" y1="{ym}" x2="{x + 12}" y2="{ym}" stroke="{INK}" stroke-width="7"/>')


def cell_h(cx, y, plus_left=True):
    xp, xm = (cx - 6, cx + 6) if plus_left else (cx + 6, cx - 6)
    return (f'<line x1="{xp}" y1="{y - 18}" x2="{xp}" y2="{y + 18}" stroke="{INK}" stroke-width="2.4"/>'
            f'<line x1="{xm}" y1="{y - 9}" x2="{xm}" y2="{y + 9}" stroke="{INK}" stroke-width="6"/>')


def resistor(cx, cy, w=64, h=24, vertical=False):
    if vertical: w, h = h, w
    return rect(cx - w / 2, cy - h / 2, w, h, CARD, INK, 0, 2.4)


def meter(cx, cy, ch, r=19):
    return circle(cx, cy, r, CARD, INK, 2.2) + text(cx, cy + 7, ch, 19, INK, 700, "middle")


def jdot(x, y):
    return circle(x, y, 4.6, INK, INK, 0)


def wire(pts):
    return poly(pts, INK, 2.4)


def cur(x1, y1, x2, y2):
    return arrow(x1, y1, x2, y2, "acc", 3.4)


def fig1():
    b = []
    # ===== 左：直列回路 =====
    b.append(rect(48, 100, 540, 456, CARD, LINE, 12))
    b.append(text(70, 136, "直列回路", 22, INK, 700) + text(178, 136, "電流の通り道が1本", 16, INK2))
    L, R, T, B, cy = 112, 520, 215, 440, 330
    xr1, xr2, vy = 250, 410, 282
    b.append(wire([(L, cy - 7), (L, T), (R, T), (R, B), (L, B), (L, cy + 7)]))
    b.append(cell_v(L, cy))
    b.append(text(96, 316, "電源", 15, INK2, anchor="end") + text(96, 343, f"{g(V0)} V", 20, INK, 700, "end"))
    b.append(text(L + 30, cy - 6, "＋", 17, INK, 700, "middle") + text(L + 30, cy + 22, "－", 17, INK, 700, "middle"))
    for xr, nm, rv, vv in [(xr1, "R₁", R1, VS1), (xr2, "R₂", R2, VS2)]:
        b.append(resistor(xr, T) + text(xr, T - 22, f"{nm} {g(rv)} Ω", 16, INK, 700, "middle"))
        b.append(wire([(xr - 44, T), (xr - 44, vy), (xr - 19, vy)]) + wire([(xr + 19, vy), (xr + 44, vy), (xr + 44, T)]))
        b.append(jdot(xr - 44, T) + jdot(xr + 44, T) + meter(xr, vy, "V"))
        b.append(text(xr, vy + 46, f"{g(vv)} V", 20, INK, 700, "middle"))
    b.append(meter(316, B, "A") + text(316, B - 30, f"{g(IS)} A", 20, ACC, 700, "middle"))
    for a in [(94, 290, 94, 240), (132, 197, 180, 197), (300, 197, 348, 197), (538, 290, 538, 345), (480, 458, 430, 458), (210, 458, 160, 458)]:
        b.append(cur(*a))
    b.append(text(500, 345, f"{g(IS)} A", 18, ACC, 700, "end"))
    b.append(lines(70, 492, [f"電流：どこでも同じ　{g(IS)} A", f"電圧：{g(VS1)} V ＋ {g(VS2)} V ＝ {g(V0)} V（電源の電圧）",
                             f"全体の抵抗：{g(R1)} ＋ {g(R2)} ＝ {g(RS)} Ω"], 16, INK, 1.6))

    # ===== 右：並列回路 =====
    b.append(rect(612, 100, 540, 456, CARD, LINE, 12))
    b.append(text(634, 136, "並列回路", 22, INK, 700) + text(742, 136, "電流の通り道が枝分かれ", 16, INK2))
    L, R, T, B, M, P = 676, 1080, 215, 440, 320, 770
    xr = 925
    b.append(wire([(L, cy - 7), (L, T), (R, T), (R, B), (L, B), (L, cy + 7)]))
    b.append(wire([(P, T), (P, M), (R, M)]))
    b.append(jdot(P, T) + jdot(R, M))
    b.append(cell_v(L, cy))
    b.append(text(660, 316, "電源", 15, INK2, anchor="end") + text(660, 343, f"{g(V0)} V", 20, INK, 700, "end"))
    b.append(text(L + 30, cy - 6, "＋", 17, INK, 700, "middle") + text(L + 30, cy + 22, "－", 17, INK, 700, "middle"))
    # R1（上の枝）・R2（下の枝）と電圧計
    b.append(resistor(xr, T) + text(xr, T - 22, f"R₁ {g(R1)} Ω", 16, INK, 700, "middle"))
    b.append(wire([(xr - 46, T), (xr - 46, 266), (xr - 19, 266)]) + wire([(xr + 19, 266), (xr + 46, 266), (xr + 46, T)]))
    b.append(jdot(xr - 46, T) + jdot(xr + 46, T) + meter(xr, 266, "V") + text(xr + 58, 273, f"{g(V0)} V", 20, INK, 700))
    b.append(resistor(xr, M) + text(xr, M + 33, f"R₂ {g(R2)} Ω", 15, INK, 700, "middle"))
    b.append(wire([(xr - 46, M), (xr - 46, 390), (xr - 19, 390)]) + wire([(xr + 19, 390), (xr + 46, 390), (xr + 46, M)]))
    b.append(jdot(xr - 46, M) + jdot(xr + 46, M) + meter(xr, 390, "V") + text(xr + 58, 397, f"{g(V0)} V", 20, INK, 700))
    b.append(meter(770, B, "A") + text(770, B - 30, f"{g(IP)} A", 20, ACC, 700, "middle"))
    for a in [(658, 290, 658, 240), (690, 197, 738, 197), (990, 197, 1040, 197), (1098, 240, 1098, 290),
              (990, 338, 1040, 338), (1098, 360, 1098, 410), (1010, 458, 960, 458)]:
        b.append(cur(*a))
    b.append(text(1015, 184, f"{g(IP1)} A", 18, ACC, 700, "middle"))
    b.append(text(1015, 366, f"{g(IP2)} A", 18, ACC, 700, "middle"))
    b.append(lines(634, 492, [f"電流：{g(IP1)} A ＋ {g(IP2)} A ＝ {g(IP)} A（枝分かれした電流の和）", f"電圧：どの抵抗にも電源と同じ {g(V0)} V",
                              f"全体の抵抗：{g(V0)} ÷ {g(IP)} ＝ 約{RP:.1f} Ω"], 16, INK, 1.6))

    # ===== 下：記号と矢印の見方 =====
    y = 594
    b.append(rect(48, 568, 1104, 50, "#f4f1e8", LINE, 10))
    b.append(cell_h(78, y) + line(56, y, 72, y, INK, 2.4) + line(84, y, 100, y, INK, 2.4) + text(108, y + 6, "電源（長い線が＋極）", 15, INK))
    b.append(line(282, y, 292, y, INK, 2.4) + resistor(316, y, 48, 18) + line(340, y, 350, y, INK, 2.4) + text(358, y + 6, "抵抗", 15, INK))
    b.append(meter(434, y, "A", 15) + text(456, y + 6, "電流計（直列につなぐ）", 15, INK))
    b.append(meter(648, y, "V", 15) + text(670, y + 6, "電圧計（並列につなぐ）", 15, INK))
    b.append(cur(860, y, 904, y) + text(912, y + 6, "電流", 15, ACC, 700))
    b.append(f'<line x1="1010" y1="{y}" x2="966" y2="{y}" stroke="{TEAL}" stroke-width="3" stroke-dasharray="6 4" marker-end="url(#ah-teal)"/>'
             + text(1018, y + 6, "電子の流れ", 15, TEAL, 700))
    return svg("".join(b), "直列回路と並列回路の電流と電圧（電源6 V・10 Ωと20 Ωの例）",
               "電流は電源の＋極から出て－極へ流れる。電子は－極から＋極へ動く（電流と逆向き）。")


def fig2():
    b = []
    # ===== 左：電圧と電流のグラフ =====
    b.append(text(60, 124, "電圧と電流の関係（オームの法則）", 19, INK, 700))
    x0, y0, w, h, VM, IM = 120, 548, 380, 350, 12, 1.2
    X = lambda v: x0 + v / VM * w
    Y = lambda i: y0 - i / IM * h
    b.append(axes(x0, y0, w, h, "電圧［V］", "電流［A］",
                  [(v / VM * w, str(v)) for v in range(0, 13, 3)], [(i / 10 / IM * h, g(i / 10)) for i in range(0, 13, 2)], 15))
    for rv, col, lab, dash in [(R1, ACC, f"{g(R1)} Ω（R₁）", None), (R2, TEAL, f"{g(R2)} Ω（R₂）", None), (RS, INK2, f"{g(RS)} Ω（直列の全体）", "8 6")]:
        ve = min(VM, IM * rv)
        b.append(line(X(0), Y(0), X(ve), Y(ve / rv), col, 3, dash))
        b.append(circle(X(V0), Y(V0 / rv), 6, col, CARD, 2))
    b.append(text(X(11) - 14, Y(1.1), "10 Ω", 16, ACC, 700, "end"))
    b.append(text(X(12) + 4, Y(0.6) - 10, "20 Ω", 16, TEAL, 700, "end"))
    b.append(text(X(12) + 4, Y(0.4) + 24, "30 Ω", 16, INK2, 700, "end"))
    b.append(line(X(V0), Y(0), X(V0), Y(IP1), MUTED, 1.4, "4 4"))
    HALO = dict(stroke=BG, stroke_width=5, paint_order="stroke")
    b.append(text(X(V0) - 12, Y(IP1) + 5, f"{g(IP1)} A", 15, ACC, 700, "end", **HALO))
    b.append(text(X(V0) - 12, Y(IP2) + 1, f"{g(IP2)} A", 15, TEAL, 700, "end", **HALO))
    b.append(text(X(V0) + 12, Y(IS) + 24, f"{g(IS)} A", 15, INK2, 700, **HALO))
    b.append(text(60, 612, "原点を通る直線（比例）。抵抗が大きいほど、かたむきはゆるやか。", 15, INK2))

    # ===== 右上：オームの法則 =====
    b.append(rect(600, 102, 552, 84, TEAL_L, LINE, 12))
    b.append(text(624, 156, "V ＝ R × I", 30, TEAL_D, 700))
    b.append(text(800, 136, "電圧［V］＝ 抵抗［Ω］× 電流［A］", 17, INK))
    b.append(text(800, 168, "I ＝ V ÷ R　　R ＝ V ÷ I", 17, INK))

    # ===== 右中：直列・並列のきまり =====
    tx0, ty0, cw = 600, 200, [150, 201, 201]
    heads = ["", "直列回路", "並列回路"]
    rows = [["電流", "どこでも同じ", "I ＝ I₁ ＋ I₂"],
            ["電圧", "V ＝ V₁ ＋ V₂", "どこも同じ"],
            ["全体の抵抗", "R ＝ R₁ ＋ R₂", "1/R ＝ 1/R₁ ＋ 1/R₂"],
            ["", "どちらの抵抗より大きい", "どちらの抵抗より小さい"],
            ["6 V・10 Ω・20 Ω", f"{g(RS)} Ω・{g(IS)} A", f"約{RP:.1f} Ω・{g(IP)} A"]]
    b.append(table(tx0, ty0, heads, rows, cw, 42, 16))
    # ===== 右下：小4 かん電池のつなぎ方 =====
    yb = 482
    b.append(text(600, yb, "かん電池のつなぎ方（小4・豆電球1個）", 17, INK, 700))
    for i, (nm, iv, note) in enumerate([("1個", I_ONE, "もとにする"), ("2個の直列つなぎ", I_SER, "明るい（2倍）"), ("2個のへい列つなぎ", I_PAR, "1個と同じ・長持ち")]):
        bx = 600 + i * 186
        b.append(rect(bx, yb + 12, 176, 92, CARD, LINE, 10))
        b.append(text(bx + 88, yb + 40, nm, 15, INK, 700, "middle"))
        b.append(text(bx + 88, yb + 68, f"{g(iv)} A", 20, ACC, 700, "middle"))
        b.append(text(bx + 88, yb + 92, note, 14, INK2, anchor="middle"))
    return svg("".join(b), "オームの法則と直列・並列のきまり（まとめ）",
               "電流計は直列、電圧計は並列につなぐ。かん電池は1個1.5 V、豆電球は7.5 Ωの一定の抵抗とした目安。")


FIGS = [
    dict(svg=fig1, alt="電気用図記号でかいた直列回路と並列回路の回路図。電源6 V、抵抗10 Ωと20 Ωのとき、直列回路では電流がどこでも0.2 Aで電圧が2 Vと4 Vに分かれ、並列回路では電流が0.6 Aと0.3 Aに分かれて合計0.9 A、どの抵抗にも6 Vが加わることを、電流の向き（＋極から－極）の矢印とともに示す図。",
         caption="直列回路と並列回路の電流と電圧（電源6 V・10 Ω・20 Ω）。電流は＋極から出て－極へ流れる。"),
    dict(svg=fig2, alt="オームの法則（V＝R×I）のまとめ。10 Ω・20 Ω・30 Ωの抵抗の電圧と電流のグラフ（原点を通る直線）と、直列回路・並列回路の電流・電圧・全体の抵抗のきまりの表、小4のかん電池の直列つなぎ・へい列つなぎの電流の比較。",
         caption="オームの法則と直列・並列のきまり。抵抗が大きいほどグラフのかたむきはゆるやかになる。"),
]
