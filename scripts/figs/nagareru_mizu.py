"""流れる水の働き（nagareru-mizu・小5）の授業用の図。
川の形・曲がり方・流れの速さ・石の大きさは、シミュと同じ式（scripts/rika/sims_kishou2.py の _CPT・_ub・_vel・_dmm・_rnd ほか）で計算する。
値はシミュの初期設定（土地のかたむき「ふつう」・水の量「ふつう」）。"""
import os, sys
from figlib import *

_R = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rika")
if _R not in sys.path:
    sys.path.append(_R)
import sims_kishou2 as Z                      # noqa: E402


def river_points():
    """JS と同じ中心線（Catmull-Rom → 長さ2.5ごとの点）と、接線・法線（左岸側が＋）・曲がり K"""
    def crp(a, b, c, d, u):
        u2 = u * u; u3 = u2 * u
        return [0.5 * (2 * b[k] + (-a[k] + c[k]) * u + (2 * a[k] - 5 * b[k] + 4 * c[k] - d[k]) * u2 + (-a[k] + 3 * b[k] - 3 * c[k] + d[k]) * u3) for k in (0, 1)]
    C = Z._CPT; dn = []
    for k in range(len(C) - 1):
        a = C[max(0, k - 1)]; b = C[k]; c = C[k + 1]; d = C[min(len(C) - 1, k + 2)]
        for j in range(16): dn.append(crp(a, b, c, d, j / 16))
    dn.append(C[-1])
    cum = [0.0]
    for k in range(1, len(dn)): cum.append(cum[-1] + math.hypot(dn[k][0] - dn[k - 1][0], dn[k][1] - dn[k - 1][1]))
    L = cum[-1]; DS = 2.5; ns = int(math.floor(L / DS)) + 1; P = []; j = 0
    for i in range(ns):
        s = min(L, i * DS)
        while j < len(dn) - 2 and cum[j + 1] < s: j += 1
        q = (s - cum[j]) / ((cum[j + 1] - cum[j]) or 1)
        P.append([dn[j][0] + (dn[j + 1][0] - dn[j][0]) * q, dn[j][1] + (dn[j + 1][1] - dn[j][1]) * q])
    out = []
    for i in range(ns):
        a = P[max(0, i - 1)]; b = P[min(ns - 1, i + 1)]; l = math.hypot(b[0] - a[0], b[1] - a[1]) or 1
        tx, ty = (b[0] - a[0]) / l, (b[1] - a[1]) / l
        u = i / (ns - 1)
        out.append(dict(x=P[i][0], y=P[i][1], tx=tx, ty=ty, nx=ty, ny=-tx, u=u, K=Z._K[i], w0=3.6 + 12 * u))
    assert ns == Z._NS
    return out


RP = river_points()
NS = len(RP)
IB = Z._IB                                     # 中流でいちばん曲がっている所（シミュの「曲がった所」）
F = 0.6 + 0.4 * (1 - 0.758) / (1.466 - 0.758)  # JS の fW()（水の量「ふつう」：Qf＝1）
V_OUT, V_IN = Z._V_OUT, Z._V_IN
PL = Z._PL
def vel(i): return Z._vel(i / (NS - 1), Z._K[i], 0)


def water_edges(p):
    """JS の geomAll()（f≤1）：水のある所の左岸側 eL・右岸側 eR（曲がった所では内側が川原になる）"""
    Wc = 2 * p["w0"]; kk = min(1, abs(p["K"]))
    dry = min(0.62, (1 - F) * (1 + 0.9 * kk)) * Wc; a = 0.5 + 0.5 * min(1, kk * 1.3); di = dry * a; dout = dry - di
    if p["K"] >= 0: return p["w0"] - di, -(p["w0"] - dout)
    return p["w0"] - dout, -(p["w0"] - di)


def f1(v): return Z._f1(v)


def fig1():
    b = []
    S, OX, OY, MT, MB = 1.1, 48, 104, 44, 298
    X = lambda x: OX + x * S
    Y = lambda y: OY + (y - MT) * S
    coast = lambda y: 606 + 5 * math.sin(y * 0.06)
    W1 = X(640)
    defs = f'<clipPath id="nm-map"><rect x="{OX}" y="{OY}" width="{W1 - OX:.1f}" height="{(MB - MT) * S:.1f}" rx="8"/></clipPath>'
    m = [f'<rect x="{OX}" y="{OY}" width="{W1 - OX:.1f}" height="{(MB - MT) * S:.1f}" fill="#e6efd8"/>']
    # 山（左の方）
    rs = [((k * 0.618) % 1, (k * 0.377 + 0.1) % 1) for k in range(1, 90)]
    for fx, fy in rs:
        x, y = fx * 250 - 6, MT + 4 + fy * (MB - MT - 8)
        if x > 215 + (y - MT) * 0.15 or min(math.hypot(p["x"] - x, p["y"] - y) for p in RP[::3]) < 26: continue
        s = 11 + 12 * (1 - max(0, x) / 320)
        m.append(f'<path d="M{X(x - s):.1f},{Y(y + s * 0.5):.1f} L{X(x):.1f},{Y(y - s * 0.62):.1f} L{X(x + s):.1f},{Y(y + s * 0.5):.1f}Z" fill="#9db27c" stroke="#6d8550" stroke-width="1"/>')
    # 海
    sea = [(X(coast(y)), Y(y)) for y in range(MT, MB + 1, 4)]
    m.append(f'<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in sea) + f' L{W1:.1f},{Y(MB):.1f} L{W1:.1f},{Y(MT):.1f}Z" fill="#a9cdea"/>')
    # 川原（川の両岸の間）と水
    def band(fa, fb, fill, stroke=None):
        pts = [(X(p["x"] + p["nx"] * fa(p)), Y(p["y"] + p["ny"] * fa(p))) for p in RP] + \
              [(X(p["x"] + p["nx"] * fb(p)), Y(p["y"] + p["ny"] * fb(p))) for p in RP[::-1]]
        st = f' stroke="{stroke}" stroke-width="1.2"' if stroke else ""
        return f'<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f'Z" fill="{fill}"{st}/>'
    m.append(band(lambda p: p["w0"], lambda p: -p["w0"], "#e8dab8", "#a08a5c"))
    m.append(band(lambda p: water_edges(p)[0], lambda p: water_edges(p)[1], "#5b9bd5"))
    b.append(f'<g clip-path="url(#nm-map)">{"".join(m)}</g>')
    b.append(rect(OX, OY, W1 - OX, (MB - MT) * S, "none", LINE, 8))
    # 地名（白いふちどり）
    H = dict(stroke="#fff", stroke_width="4", paint_order="stroke")
    pu = RP[PL[0][1]]; pd = RP[PL[3][1]]
    b.append(text(X(36), Y(MT + 22), "山", 18, "#3f6212", 700, "middle", **H))
    b.append(text(X(pu["x"]), Y(pu["y"]) + 38, "上流", 18, INK, 700, "middle", **H))
    b.append(text(X(pd["x"]) + 26, Y(pd["y"]) + 6, "下流", 18, INK, 700, **H))
    b.append(text(X(430), Y(MB - 12), "平地", 16, "#4d7c0f", 700, "middle", **H))
    b.append(text(X(coast(120) + 16), Y(MT + 64), "海", 18, TEAL_D, 700, "middle"))
    b.append(f'<rect x="{X(470)}" y="114" width="16" height="12" fill="#5b9bd5"/>' + text(X(470) + 22, 125, "水", 14, INK2, **H))
    b.append(f'<rect x="{X(470) + 50}" y="114" width="16" height="12" fill="#e8dab8" stroke="#a08a5c"/>' + text(X(470) + 72, 125, "川原", 14, INK2, **H))
    # 曲がった所：外側と内側
    p = RP[IB]; sg = 1 if p["K"] >= 0 else -1                 # K>0：左へ曲がる＝外側は右岸（n が−の側）
    no, ni = -sg * (p["w0"] + 13), sg * (p["w0"] + 12)
    xo, yo = X(p["x"] + p["nx"] * no), Y(p["y"] + p["ny"] * no)
    xi, yi = X(p["x"] + p["nx"] * ni), Y(p["y"] + p["ny"] * ni)
    b.append(badge(xo, yo, "外", ACC, "#fff", 16) + badge(xi, yi, "内", TEAL, "#fff", 16))
    b.append(text(X(p["x"]), Y(p["y"]) + 62, "中流（曲がった所）", 17, INK, 700, "middle", **H))
    # 流れの向き
    for k in (60, 200, 290):
        q = RP[k]; x0, y0 = X(q["x"]), Y(q["y"])
        b.append(arrow(x0 - q["tx"] * 10, y0 - q["ty"] * 10, x0 + q["tx"] * 12, y0 + q["ty"] * 12, "ink", 2.2))
    # 右：曲がった所の断面（JS の drawXsec と同じ形）
    u = p["u"]; a = max(0.0, min(1.0, (abs(p["K"]) - 0.12) * 1.4)); outR = p["K"] > 0
    al, be = (0.8 + 0.6 * a, 0.8 - 0.45 * a) if outR else (0.8 - 0.45 * a, 0.8 + 0.6 * a)
    qm = al / (al + be); gm = qm ** al * (1 - qm) ** be; Dp = 30 + 22 * (1 - u); mx = Dp * (1 + 0.3 * a)
    dep = lambda q: mx * max(0, min(1, q)) ** al * max(0, min(1, 1 - q)) ** be / gm
    L0, R0, T0, B0 = 790, 1152, 150, 382
    sx, sz = 1.6, 1.9
    cx, gy = (L0 + R0) / 2, T0 + 60
    half = p["w0"] * 46 / math.sqrt(2 * p["w0"]) * sx
    xl, xr = cx - half, cx + half
    ys = gy + mx * sz * (1 - max(0, min(1, (F - 0.4) / 0.6)))
    b.append(text(L0, 122, "曲がった所の川の断面", 18, INK, 700))
    b.append(text(L0, 142, "（下流の方を向いて見た図）", 14, MUTED))
    sec = [f'<rect x="{L0}" y="{T0}" width="{R0 - L0}" height="{B0 - T0}" fill="#f0f6fb"/>',
           f'<rect x="{L0}" y="{ys:.1f}" width="{R0 - L0}" height="{B0 - ys:.1f}" fill="#5b9bd5"/>']
    gp = [(L0 - 2, gy - (xl - L0 + 2) * 0.05), (xl, gy)] + [(xl + (xr - xl) * k / 60, gy + dep(k / 60) * sz) for k in range(1, 60)] + [(xr, gy), (R0 + 2, gy - (R0 + 2 - xr) * 0.05), (R0 + 2, B0 + 2), (L0 - 2, B0 + 2)]
    sec.append(f'<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in gp) + f'Z" fill="#b08d5b" stroke="#6b4f2a" stroke-width="1.6"/>')
    defs += f'<clipPath id="nm-sec"><rect x="{L0}" y="{T0}" width="{R0 - L0}" height="{B0 - T0}"/></clipPath>'
    b.append(f'<g clip-path="url(#nm-sec)">{"".join(sec)}</g>' + rect(L0, T0, R0 - L0, B0 - T0, "none", LINE, 0, 1))
    def edge(q0, q1):                                   # 川底が水面と交わる所（二分法）
        f0 = gy + dep(q0) * sz - ys
        for _ in range(40):
            qm_ = (q0 + q1) / 2
            if (gy + dep(qm_) * sz - ys > 0) == (f0 > 0): q0 = qm_
            else: q1 = qm_
        return xl + (xr - xl) * (q0 + q1) / 2
    qd = max([k / 200 for k in range(201)], key=dep)
    b.append(line(edge(0.0, qd), ys, edge(1.0, qd), ys, TEAL_D, 1.8))
    # 川原（内側の水の外の部分）に小石
    qs = [k / 60 for k in range(61)]
    wet = [q for q in qs if gy + dep(q) * sz > ys]
    qa, qb = wet[0], wet[-1]
    xin = (xl + (xl + (xr - xl) * qa)) / 2 if outR else (xr + (xl + (xr - xl) * qb)) / 2
    xout = xr if outR else xl
    xin_lbl, xout_lbl = (L0 + 92, R0 - 92) if outR else (R0 - 92, L0 + 92)
    for k in range(9):
        qq = (qa * (k + 0.5) / 9) if outR else (qb + (1 - qb) * (k + 0.5) / 9)
        xx = xl + (xr - xl) * qq; yy = gy + dep(qq) * sz - 4
        b.append(f'<ellipse cx="{xx:.1f}" cy="{yy:.1f}" rx="5" ry="3.5" fill="#d6c7a1" stroke="#8b7550" stroke-width="1"/>')
    deep_q = max(qs, key=dep); xd = xl + (xr - xl) * deep_q
    b.append(text(xd, gy + dep(deep_q) * sz - 10, "深い", 16, "#fff", 700, "middle"))
    for xx, nm, col, w1, w2 in ((xout_lbl, "外", ACC, "外側：がけ・深い", f"流れが速い（秒速{f1(V_OUT)} m）"),
                                (xin_lbl, "内", TEAL, "内側：川原・浅い", f"流れがおそい（秒速{f1(V_IN)} m）")):
        b.append(badge(xx - 72, T0 + 22, nm, col, "#fff", 14) + text(xx - 56, T0 + 28, w1, 16, col if col == ACC else TEAL_D, 700))
        b.append(text(xx, T0 + 50, w2, 14, INK2, anchor="middle"))
    b.append(text(cx - 20, ys + 22, "水", 16, "#fff", 700, "middle"))
    # 下：3つのはたらき
    boxes = [("けずる", "しん食", "地面や川岸・川底をけずる。", "流れが速い所（上流・曲がった所の外側）", ACC),
             ("運ぶ", "運ぱん", "けずった土や石を下流へ運ぶ。", "流れが速いほど、大きな石まで運ばれる", GOLD),
             ("積もらせる", "たい積", "運んできた土や石を積もらせる。", "流れがおそい所（下流・曲がった所の内側）", TEAL)]
    for k, (w, nm, d1, d2, col) in enumerate(boxes):
        x = 48 + k * 372
        b.append(rect(x, 404, 360, 160, CARD, col, 10, 2))
        b.append(f'<rect x="{x}" y="404" width="360" height="46" rx="10" fill="{col}"/><rect x="{x}" y="430" width="360" height="20" fill="{col}"/>')
        b.append(text(x + 18, 435, f"{w}（{nm}）", 20, "#fff", 700))
        b.append(text(x + 18, 482, d1, 16.5, INK, 700))
        b.append(text(x + 18, 516, "よく見られる所", 14, MUTED))
        b.append(text(x + 18, 542, d2, 15.5, INK2))
    b.append(text(600, 598, "流れが速いほど、けずる・運ぶはたらきが大きく、流れがおそくなると積もる。", 17, INK, 700, "middle"))
    return svg("".join(b), "流れる水のはたらき（しん食・運ぱん・たい積）",
               "川の形・速さは、しくみがわかるように作ったモデルの値（目安）。水の量がふえると、流れは速くなる。", defs)


def stone(cx, cy, size, rnd, seed):
    """石の絵。rnd＝丸さ（0 角ばっている〜1 丸い）。size＝横の長さ px"""
    r = size / 2
    if rnd >= 0.65:
        return f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{r:.1f}" ry="{r * 0.72:.1f}" fill="#b9b2a6" stroke="#6b6359" stroke-width="1.6"/>'
    n = 7 if rnd < 0.3 else 11
    pts = []
    for k in range(n):
        a = (k + 0.35 * math.sin(seed * 7.1 + k * 2.3)) / n * 2 * math.pi
        rr = r * (0.82 + 0.18 * math.sin(seed * 3.3 + k * 1.7))
        pts.append((cx + rr * math.cos(a), cy + rr * 0.7 * math.sin(a)))
    if rnd < 0.3:
        return f'<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f'Z" fill="#9b958c" stroke="#57534e" stroke-width="1.8" stroke-linejoin="round"/>'
    d = "M" + " ".join(f"{(pts[k][0] + pts[(k + 1) % n][0]) / 2:.1f},{(pts[k][1] + pts[(k + 1) % n][1]) / 2:.1f} Q{pts[(k + 1) % n][0]:.1f},{pts[(k + 1) % n][1]:.1f}" for k in range(n))
    return f'<path d="{d} {(pts[0][0] + pts[1][0]) / 2:.1f},{(pts[0][1] + pts[1][1]) / 2:.1f}Z" fill="#aaa398" stroke="#615a51" stroke-width="1.6"/>'


def fig2():
    b = []
    CX = [330, 650, 970]; CW = 300
    places = [("上流（山の中）", PL[0][1]), ("中流", IB), ("下流（平地）", PL[3][1])]
    # 上：川の高さのようす（JS の drawProf：base−Hk·(1−u)^2.2）
    xa, xb, base = 180, 1120, 220
    Hk = 8 + 5.5 * 3
    zx = lambda uu: base - 4 - Hk * (1 - uu) ** 2.2 * 3.4
    X = lambda uu: xa + (xb - xa) * uu
    prof = [(X(k / 100), zx(k / 100)) for k in range(101)]
    b.append(f'<path d="M{xa},{base + 14} ' + " ".join(f"L{x:.1f},{y:.1f}" for x, y in prof) + f' L{xb},{base + 14}Z" fill="#c9b48a"/>')
    b.append(poly(prof, "#5b9bd5", 4))
    b.append(f'<rect x="{xb}" y="{base - 4}" width="32" height="18" fill="#a9cdea"/>' + text(xb + 16, base - 10, "海", 15, TEAL_D, 700, "middle"))
    b.append(text(48, 150, "川の高さのようす", 16, INK, 700) + text(48, 172, "（横から見た図）", 14, MUTED))
    b.append(text(X(0.06), zx(0.06) - 12, "山", 16, "#3f6212", 700))
    b.append(text(X(0.5), 128, "土地のかたむき：急 → ゆるやか", 16, INK2, anchor="middle"))
    # 列の見出し
    for (nm, i), cx in zip(places, CX):
        b.append(f'<rect x="{cx - CW / 2 + 4}" y="236" width="{CW - 8}" height="38" rx="8" fill="{TEAL_L}"/>' + text(cx, 262, nm, 18, INK, 700, "middle"))
    heads = [("川原の石", 292, 112), ("石の大きさ", 404, 54), ("石の形", 458, 40), ("流れの速さ", 498, 54), ("多いはたらき", 552, 54)]
    for k, (h, y, hh) in enumerate(heads):
        if k % 2 == 0: b.append(f'<rect x="48" y="{y}" width="1104" height="{hh}" fill="#f3f0e8"/>')
        b.append(text(60, y + hh / 2 + (0 if k == 0 else 6), h, 16, INK, 700))
    b.append(text(60, 378, "（3つとも同じ", 14, MUTED) + text(60, 396, "　割合でかいた絵）", 14, MUTED))
    # 石の絵（1 cm＝4.2 px）
    PXCM = 4.2
    for k, ((nm, i), cx) in enumerate(zip(places, CX)):
        uu = i / (NS - 1); d = Z._dmm(uu); rr = Z._rnd(uu); w = d / 10 * PXCM
        if w > 40:
            b.append(stone(cx, 348, w, rr, k + 1))
        elif w > 14:
            for j, (dx, dy) in enumerate([(-40, -12), (0, 8), (40, -10), (-20, 30), (24, 32)]):
                b.append(stone(cx + dx, 346 + dy, w * (0.85 + 0.1 * (j % 3)), rr, k * 5 + j + 2))
        else:
            for j in range(18):
                dx = ((j * 37) % 90) - 45; dy = ((j * 53) % 50) - 20
                b.append(stone(cx + dx, 346 + dy, max(w, 6), 1.0, 0))
    b.append(line(1040, 392, 1040 + 10 * PXCM, 392, INK, 2) + line(1040, 386, 1040, 398, INK, 2) + line(1040 + 10 * PXCM, 386, 1040 + 10 * PXCM, 398, INK, 2)
             + text(1040 + 5 * PXCM + 34, 397, "10 cm", 14, INK2))
    for k, ((nm, i), cx) in enumerate(zip(places, CX)):
        uu = i / (NS - 1); d = Z._dmm(uu)
        b.append(text(cx, 426, Z._size(d), 18, INK, 700, "middle") + text(cx, 448, f"（{Z._sizew(d)}）", 14, INK2, anchor="middle"))
        b.append(text(cx, 484, Z._shapew(Z._rnd(uu)), 17, INK, 700, "middle"))
    b.append(text(CX[0], 532, f"秒速{f1(vel(PL[0][1]))} m（速い）", 17, INK, 700, "middle"))
    b.append(text(CX[1], 522, f"外側 秒速{f1(V_OUT)} m", 16, ACC, 700, "middle") + text(CX[1], 543, f"内側 秒速{f1(V_IN)} m", 16, TEAL_D, 700, "middle"))
    b.append(text(CX[2], 532, f"秒速{f1(vel(PL[3][1]))} m（おそい）", 17, INK, 700, "middle"))
    b.append(text(CX[0], 585, "けずる・運ぶ", 17, ACC, 700, "middle"))
    b.append(text(CX[1], 576, "外側でけずり、", 16, INK, 700, "middle") + text(CX[1], 597, "内側で積もらせる", 16, INK, 700, "middle"))
    b.append(text(CX[2], 585, "積もらせる", 17, TEAL_D, 700, "middle"))
    for x in (CX[0] + CW / 2, CX[1] + CW / 2):
        b.append(line(x, 236, x, 606, LINE, 1.2))
    return svg("".join(b), "上流・中流・下流のちがい（まとめ）",
               f"シミュの初期設定（かたむき・水の量「ふつう」）の値。河口の近くはすなつぶ（{Z._size(Z._dmm(PL[4][1] / (NS - 1)))}）が多い。")


FIGS = [
    dict(svg=fig1,
         alt=f"山から海へ流れる川を上から見た図。曲がって流れている所の外側は流れが速く（秒速{f1(V_OUT)} m）、岸がけずられてがけになり、内側は流れがおそく（秒速{f1(V_IN)} m）、石やすなが積もって川原になる。曲がった所の川の断面と、流れる水のしん食・運ぱん・たい積の3つのはたらきもまとめている。",
         caption="流れる水のはたらき。曲がった所の外側はけずられ、内側には石やすなが積もる。"),
    dict(svg=fig2,
         alt="上流・中流・下流の川原の石の大きさ（約24 cm・約8.1 cm・約1.5 cm）と形（角ばっている・少し丸い・丸い）、流れの速さ、多いはたらき（けずる・積もらせる）を比べたまとめの図。川の高さのようすも横から見た図で示している。",
         caption="上流・中流・下流のちがい。下流ほど土地のかたむきがゆるやかで、流れはおそく、石は小さく丸くなる。"),
]
