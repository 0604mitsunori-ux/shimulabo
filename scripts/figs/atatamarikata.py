"""物のあたたまり方（atatamarikata）の授業用の図。
数値・色分けは、ページの JS（scripts/rika/sims_sho4_b.py の JS_ATA）と同じモデルをそのまま Python に移して計算する。
  金ぞく：熱伝導（2.5 mmマス・熱拡散率・板30 W／ぼう12 W・空気へにげる熱）、ろうは約55℃でとける
  水・空気：層のモデル（あたためられた水・空気が上へ動いて上にたまる）
  体積：空気＝(273.15+T)/293.15、水＝ρ(20)/ρ(T)（Tanaka ほか 2001）、鉄＝1+36e-6×(T−20)"""
import math
import numpy as np
from figlib import *

# ================= ページの JS と同じモデル =================
MET = {"cu": (1.11e-4, 3.45e6), "al": (9.7e-5, 2.42e6), "fe": (2.3e-5, 3.54e6)}   # 熱拡散率, 体積あたりの熱容量
DX, TMX, WAX = 2.5e-3, 500, 55


def plate_run(times, met="cu", heat_c=(3, 3)):
    """金ぞくの板（40×40マス・かどの(3,3)を熱する）。times の各時刻で「ろうがとけた所」（約55℃をこえた所）を返す"""
    a, rc = MET[met]; h = 0.2 * DX * DX / a; r = a * h / (DX * DX); ls = 0.006 * h
    n = 40; Tm = np.full((n, n), 20.0)
    heat = [(y, x) for y in range(heat_c[1] - 2, heat_c[1] + 3) for x in range(heat_c[0] - 2, heat_c[0] + 3)
            if 0 <= x < n and 0 <= y < n and math.hypot(x - heat_c[0], y - heat_c[1]) <= 1.5]
    hy = np.array([p[0] for p in heat]); hx = np.array([p[1] for p in heat])
    dq = 30 / (len(heat) * rc * 6.25e-9) * h
    melt = np.zeros((n, n), bool); t = 0.0; out = {}; rt = sorted(times); first = {}
    probes = {"ア": (8, 8), "イ": (20, 20), "ウ": (32, 32)}
    while rt:
        s = np.zeros_like(Tm)
        d = Tm[:, 1:] - Tm[:, :-1]; s[:, :-1] += d; s[:, 1:] -= d
        d = Tm[1:, :] - Tm[:-1, :]; s[:-1, :] += d; s[1:, :] -= d
        Tm = Tm + r * s - ls * (Tm - 20)
        Tm[hy, hx] = np.minimum(TMX, Tm[hy, hx] + dq)
        melt |= Tm >= WAX; t += h
        for k, (x, y) in probes.items():
            if k not in first and Tm[y, x] >= WAX: first[k] = t
        while rt and t >= rt[0] - 1e-12:
            out[rt.pop(0)] = melt.copy()
    return out, first


def rod_run(T, met="cu"):
    """金ぞくのぼう（47マス・真ん中の3マスを熱する）"""
    a, rc = MET[met]; h = 0.2 * DX * DX / a; r = a * h / (DX * DX); ls = 0.004 * h
    n = 47; Tm = np.full(n, 20.0); heat = np.arange(22, 25); dq = 12 / (3 * rc * 4.9e-8) * h
    melt = np.zeros(n, bool); t = 0.0
    while t < T - 1e-12:
        s = np.zeros(n); d = Tm[1:] - Tm[:-1]; s[:-1] += d; s[1:] -= d
        Tm = Tm + r * s - ls * (Tm - 20); Tm[heat] = np.minimum(TMX, Tm[heat] + dq); melt |= Tm >= WAX; t += h
    return melt


def fluid(P, T, fan=False):
    """水・空気の層のモデル（JS の fstep をそのまま）。T 秒後の層の温度（上が0）と、上・真ん中・下（PR）の温度、40℃（空気は18℃）をこえた時刻"""
    n = P["ny"]; L = [float(P["t0"])] * n; h = P["h"]; t = 0.0; first = [None] * 3
    def pv(k):
        j = P["PR"][k]; a, b = max(0, j - 1), min(n - 1, j + 1); return sum(L[a:b + 1]) / (b - a + 1)
    for _ in range(int(round(T / h))):
        Tp = min(P["tmax"], L[P["hL"]] + P["Q"] / P["F"]); d = 0
        while d < P["hL"] and L[d] > Tp: d += 1
        s = P["F"] * h; N = L[:]
        for j in range(d, P["hL"] + 1):
            up = Tp if j == d else L[j - 1]; N[j] = L[j] + s * (up - L[j])
        L = N
        for j in range(n):
            L[j] = min(P["tmax"], L[j]); L[j] += (P["tenv"] - L[j]) * P["loss"] * h
            if P.get("win") and P["win"][0] <= j <= P["win"][1]: L[j] += (P["tenv"] - L[j]) * P["win"][2] * h
        D = L[:]
        for j in range(n):
            u = L[j - 1] if j else L[j]; dd = L[j + 1] if j < n - 1 else L[j]; D[j] = L[j] + P["vd"] * h * (u + dd - 2 * L[j])
        L = D
        if fan:
            m = sum(L) / n; k = min(1, 0.3 * h); L = [x + (m - x) * k for x in L]
        for _it in range(n):
            ch = False
            for j in range(n - 1, 0, -1):
                if L[j] > L[j - 1] + 1e-9:
                    m = (L[j] + L[j - 1]) / 2; L[j] = L[j - 1] = m; ch = True
            if not ch: break
        t += h
        for k in range(3):
            if first[k] is None and pv(k) >= P["thr"]: first[k] = t
    return L, [pv(k) for k in range(3)], first


def TUBE(pos):
    return dict(ny=40, h=0.05, t0=20, tmax=100, tenv=20, loss=0.002, vd=0.3, hL={"bot": 39, "mid": 21, "top": 5}[pos], Q=24, F=4.8, PR=[3, 20, 36], thr=40)


BEAKER = dict(ny=24, h=0.05, t0=20, tmax=100, tenv=20, loss=0.0015, vd=0.15, hL=23, Q=3.36, F=0.3, PR=[1, 11, 21], thr=40)
ROOM = dict(ny=26, h=0.25, t0=10, tmax=70, tenv=5, loss=0.0008, vd=0.02, hL=25, Q=1.2, F=0.15, win=[4, 19, 0.004], PR=[1, 13, 24], thr=18)


def rho(T):
    return 999.97495 * (1 - (T - 3.983035) ** 2 * (T + 301.797) / (522528.9 * (T + 69.34881)))


def vols(T):
    return (273.15 + T) / 293.15, rho(20) / rho(T), 1 + 36e-6 * (T - 20)


def r0(x):                                 # JS の Math.round と同じ
    return int(math.floor(x + 0.5))


def hexmix(a, b, t):
    t = max(0.0, min(1.0, t)); pa = [int(a[i:i + 2], 16) for i in (1, 3, 5)]; pb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(pa, pb))


def ink(v):                                # しおんインク：約40℃で青→ピンク（JS の ink と同じ）
    return hexmix("#4f6bd8", "#ec6fa6", (v - 34) / 10)


def roomcol(v):                            # 空気の温度の色（つめたい→あたたかい）
    return hexmix("#cfe2ee", "#f1ad97", (v - 12) / 12)


# ================= 部品 =================
CU1, CU2, CU3 = "#a9582e", "#d1916a", "#efcdb5"          # ろうがとけた所（早い→おそい）


def flame(x, y, s):
    """炎。(x, y)＝炎の根元"""
    o = (f'M{x},{y - 2.6 * s:.1f} C{x + 1.2 * s:.1f},{y - 1.3 * s:.1f} {x + 1.0 * s:.1f},{y:.1f} {x},{y:.1f} '
         f'C{x - 1.0 * s:.1f},{y:.1f} {x - 1.2 * s:.1f},{y - 1.3 * s:.1f} {x},{y - 2.6 * s:.1f}Z')
    i = (f'M{x},{y - 1.5 * s:.1f} C{x + 0.6 * s:.1f},{y - 0.8 * s:.1f} {x + 0.5 * s:.1f},{y - 0.15 * s:.1f} {x},{y - 0.15 * s:.1f} '
         f'C{x - 0.5 * s:.1f},{y - 0.15 * s:.1f} {x - 0.6 * s:.1f},{y - 0.8 * s:.1f} {x},{y - 1.5 * s:.1f}Z')
    return f'<path d="{o}" fill="{ACC}"/><path d="{i}" fill="{SUN}"/>'


def lamp(x, ytip, s=7):
    """アルコールランプ（炎の先＝ytip）"""
    base = ytip + 2.6 * s
    return (flame(x, base, s) + rect(x - 2, base, 4, 7, MUTED, MUTED, 1, 0)
            + rect(x - 20, base + 7, 40, 18, "#e8eef2", INK2, 7, 1.4))


def runs(mask, x0, y0, cw, color):
    """True のマスを行ごとにつなげた四角でぬる"""
    out = []
    for y in range(mask.shape[0]):
        x = 0
        while x < mask.shape[1]:
            if mask[y, x]:
                s = x
                while x < mask.shape[1] and mask[y, x]: x += 1
                out.append(f'<rect x="{x0 + s * cw:.1f}" y="{y0 + y * cw:.1f}" width="{(x - s) * cw + 0.4:.1f}" height="{cw + 0.4:.1f}" fill="{color}"/>')
            else:
                x += 1
    return "".join(out)


def tagc(x, y, s, color, size=15, anchor="middle"):
    w = sum(size * (0.6 if ord(c) < 128 else 1.0) for c in s)
    x0 = x - w / 2 if anchor == "middle" else (x - w if anchor == "end" else x)
    return rect(x0 - 5, y - size - 1, w + 10, size + 9, "#ffffff", color, 5, 1.2) + text(x, y + 1, s, size, color, 700, anchor)


# ================= 図1：しくみ図 =================
def fig1():
    b = []
    # ---------- 金ぞく ----------
    P0, P1 = 48, 438
    b.append(rect(P0, 98, P1 - P0, 524, CARD, LINE, 12))
    b.append(text(P0 + 18, 130, "金ぞく", 21, INK, 700) + text(P0 + 96, 130, "熱した所から近いじゅんに", 17, ACC, 700))
    T1, T2, T3 = 10, 25, 40
    melt, first = plate_run((T1, T2, T3, 90))         # 90秒まで計算して、ア・イ・ウがとけた時刻も求める
    cw, ox, oy = 5.5, P0 + 22, 172
    b.append(rect(ox - 2, oy - 2, 40 * cw + 4, 40 * cw + 4, "#fbfaf6", INK2, 2, 1.6))
    for T, c in [(T3, CU3), (T2, CU2), (T1, CU1)]:
        b.append(runs(melt[T], ox, oy, cw, c))
    hx_, hy_ = ox + 3.5 * cw, oy + 3.5 * cw
    b.append(circle(hx_, hy_, 13, "#fff3c4", ACC, 1.6) + flame(hx_, hy_ + 9, 6.5))
    for k, (x, y) in {"ア": (8, 8), "イ": (20, 20), "ウ": (32, 32)}.items():
        cx, cy = ox + (x + 0.5) * cw, oy + (y + 0.5) * cw
        b.append(circle(cx, cy, 12, "#ffffff", INK, 1.6) + text(cx, cy + 5.5, k, 15, INK, 700, "middle"))
    b.append(text(ox, oy - 9, "かどを熱する", 14, ACC, 700))
    lx = ox + 40 * cw + 20
    b.append(text(lx, 178, "ろうがとけた所", 15, INK, 700))
    for i, (T, c) in enumerate([(T1, CU1), (T2, CU2), (T3, CU3)]):
        yy = 196 + i * 30
        b.append(rect(lx, yy, 24, 20, c, c, 3, 0) + text(lx + 32, yy + 16, f"{T}秒後", 15, INK, 700))
    b.append(rect(lx, 286, 24, 20, "#fbfaf6", INK2, 3, 1.2) + text(lx + 32, 302, "まだ", 15, INK, 700))
    order = sorted(first, key=first.get)
    b.append(text(lx, 340, "とけた順", 15, INK2, 700))
    for i, k in enumerate(order):
        b.append(text(lx, 364 + i * 22, k, 16, ACC, 700) + text(lx + 24, 364 + i * 22, f"約{r0(first[k])}秒", 15, INK, 700))
    b.append(text(ox, 416, "どうの板（約10 cm四方）", 14, MUTED))
    # かたむけたぼう
    b.append(line(P0 + 16, 432, P1 - 16, 432, LINE, 1.2))
    b.append(text(P0 + 18, 458, "かたむけたぼう（20秒後）", 16, INK, 700))
    mr = rod_run(20)
    rw, rh, ang = 4.6, 18, -30
    cxr, cyr = 250, 522
    L = 47 * rw
    g = [f'<g transform="translate({cxr},{cyr}) rotate({ang})">',
         f'<rect x="{-L / 2:.1f}" y="{-rh / 2}" width="{L:.1f}" height="{rh}" fill="#fbfaf6"/>']
    i = 0
    while i < 47:
        if mr[i]:
            s = i
            while i < 47 and mr[i]: i += 1
            g.append(f'<rect x="{-L / 2 + s * rw:.1f}" y="{-rh / 2}" width="{(i - s) * rw:.1f}" height="{rh}" fill="{CU1}"/>')
        else:
            i += 1
    g.append(f'<rect x="{-L / 2:.1f}" y="{-rh / 2}" width="{L:.1f}" height="{rh}" fill="none" stroke="{INK2}" stroke-width="1.6"/>')
    # 上へ・下へ の矢印（ぼうにそって）
    g.append(line(30, -rh / 2 - 12, 78, -rh / 2 - 12, ACC, 2.4, arrow="acc") + line(-30, -rh / 2 - 12, -78, -rh / 2 - 12, ACC, 2.4, arrow="acc"))
    g.append("</g>")
    b.append("".join(g))
    b.append(flame(cxr, cyr + 34, 7))
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    e0 = (cxr - L / 2 * ca, cyr - L / 2 * sa); e1 = (cxr + L / 2 * ca, cyr + L / 2 * sa)
    b.append(text(e0[0] - 12, e0[1] + 6, "下のはし", 15, INK2, 700, "end"))
    b.append(text(e1[0] + 12, e1[1] + 6, "上のはし", 15, INK2, 700))
    b.append(text(P0 + 18, 606, "上にも下にも、同じようにあたたまる", 16, INK, 700))

    # ---------- 水 ----------
    Q0, Q1 = 450, 798
    b.append(rect(Q0, 98, Q1 - Q0, 524, CARD, LINE, 12))
    b.append(text(Q0 + 18, 130, "水", 21, INK, 700) + text(Q0 + 50, 130, "あたためられた水が上へ動く", 17, ACC, 700))
    TB = 150
    Lb, pvb, _ = fluid(BEAKER, TB)
    bx0, bx1, wy0, wy1 = Q0 + 30, Q0 + 230, 190, 410
    nh = (wy1 - wy0) / BEAKER["ny"]
    for j, v in enumerate(Lb):
        b.append(f'<rect x="{bx0}" y="{wy0 + j * nh:.1f}" width="{bx1 - bx0}" height="{nh + 0.5:.1f}" fill="{ink(v)}"/>')
    b.append(poly([(bx0 - 6, wy0 - 30), (bx0, wy0 - 24), (bx0, wy1 + 2), (bx1, wy1 + 2), (bx1, wy0 - 30)], INK2, 2.6))
    b.append(line(bx0 - 22, wy1 + 8, bx1 + 22, wy1 + 8, MUTED, 3))
    fx = bx0 + (bx1 - bx0) * (104 - 79) / 260                # JS：底のはし（x=104）を熱する
    b.append(lamp(fx, wy1 + 12, 6.5))
    # 水の動き（JS の流れの向きと同じ：熱した側で上へ→上を横へ→反対側で下へ→底を戻る）
    m = 22
    loop = (f'M{fx:.1f},{wy1 - m} L{fx:.1f},{wy0 + m + 14} Q{fx:.1f},{wy0 + m} {fx + 14:.1f},{wy0 + m} '
            f'L{bx1 - m - 14:.1f},{wy0 + m} Q{bx1 - m:.1f},{wy0 + m} {bx1 - m:.1f},{wy0 + m + 14} '
            f'L{bx1 - m:.1f},{wy1 - m - 14} Q{bx1 - m:.1f},{wy1 - m} {bx1 - m - 14:.1f},{wy1 - m} L{fx + 30:.1f},{wy1 - m}')
    b.append(f'<path d="{loop}" fill="none" stroke="#ffffff" stroke-width="7" stroke-linejoin="round" opacity=".8"/>')
    b.append(f'<path d="{loop}" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linejoin="round" stroke-dasharray="10 6"/>')
    for (x1, y1, x2, y2) in [(fx, wy0 + 150, fx, wy0 + 110), ((bx0 + bx1) / 2, wy0 + m, (bx0 + bx1) / 2 + 30, wy0 + m),
                             (bx1 - m, wy0 + 100, bx1 - m, wy0 + 140), ((bx0 + bx1) / 2 + 30, wy1 - m, (bx0 + bx1) / 2, wy1 - m)]:
        b.append(arrow(x1, y1, x2, y2, "ink", 2.6))
    for k, nm in enumerate(["上", "真ん中", "下"]):
        y = wy0 + (BEAKER["PR"][k] + 0.5) * nh
        b.append(line(bx1 + 2, y, bx1 + 12, y, INK2, 1.4) + text(bx1 + 16, y + 6, f"{nm} {r0(pvb[k])}℃", 15, INK, 700))
    b.append(text(Q0 + 18, 508, "しおんインク：", 15, INK2, 700))
    for i, (s, c) in enumerate([("約40℃より低い", "#4f6bd8"), ("約40℃より高い", "#ec6fa6")]):
        b.append(rect(Q0 + 120, 494 + i * 24, 18, 16, c, c, 3, 0) + text(Q0 + 144, 508 + i * 24, s, 15, INK, 700))
    b.append(text(Q0 + 18, 562, f"ビーカーの底のはしを熱して{TB // 60}分{TB % 60}秒後", 15, MUTED))
    b.append(text(Q0 + 18, 584, "上の方からじゅんに、", 16, INK, 700) + text(Q0 + 18, 606, "全体があたたまる", 16, INK, 700))

    # ---------- 空気 ----------
    R0, R1 = 810, 1152
    b.append(rect(R0, 98, R1 - R0, 524, CARD, LINE, 12))
    b.append(text(R0 + 18, 130, "空気", 21, INK, 700) + text(R0 + 70, 130, "あたためられた空気が上へ", 17, ACC, 700))
    TR_ = 900
    Lr, pvr, _ = fluid(ROOM, TR_)
    _, pvf, _ = fluid(ROOM, TR_, fan=True)
    rx0, rx1, ry0, ry1 = R0 + 22, R1 - 30, 168, 432
    nh = (ry1 - ry0) / ROOM["ny"]
    for j, v in enumerate(Lr):
        b.append(f'<rect x="{rx0}" y="{ry0 + j * nh:.1f}" width="{rx1 - rx0}" height="{nh + 0.5:.1f}" fill="{roomcol(v)}"/>')
    b.append(rect(rx0, ry0, rx1 - rx0, ry1 - ry0, "none", INK2, 0, 3) + rect(rx0 - 4, ry1, rx1 - rx0 + 8, 9, GOLD, GOLD, 0, 0))
    wy_a, wy_b = ry0 + (ry1 - ry0) * 36 / 234, ry0 + (ry1 - ry0) * 172 / 234          # JS：まど（y=108〜244）
    b.append(rect(rx1 - 5, wy_a, 10, wy_b - wy_a, "#e6f2f8", TEAL, 0, 1.6))
    b.append(text(rx1 + 8, ry1 + 34, "右のかべ＝まど（外は5℃）", 14, TEAL_D, 700, "end"))
    sx0 = rx0 + 18
    b.append(rect(sx0, ry1 - 48, 62, 48, "#3d434b", "#3d434b", 6, 0))
    for i in range(3):
        b.append(rect(sx0 + 8, ry1 - 40 + i * 12, 46, 5, ACC, ACC, 1, 0))
    b.append(text(sx0 + 31, ry1 - 56, "ストーブ", 15, ACC, 700, "middle"))
    m = 26; sxc = sx0 + 31
    loop = (f'M{sxc:.1f},{ry1 - 82} L{sxc:.1f},{ry0 + m + 16} Q{sxc:.1f},{ry0 + m} {sxc + 16:.1f},{ry0 + m} '
            f'L{rx1 - m - 30:.1f},{ry0 + m} Q{rx1 - m - 14:.1f},{ry0 + m} {rx1 - m - 14:.1f},{ry0 + m + 16} '
            f'L{rx1 - m - 14:.1f},{ry1 - m - 16} Q{rx1 - m - 14:.1f},{ry1 - m} {rx1 - m - 30:.1f},{ry1 - m} L{sx0 + 80:.1f},{ry1 - m}')
    b.append(f'<path d="{loop}" fill="none" stroke="#ffffff" stroke-width="7" stroke-linejoin="round" opacity=".8"/>')
    b.append(f'<path d="{loop}" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linejoin="round" stroke-dasharray="10 6"/>')
    mx = (rx0 + rx1) / 2
    for (x1, y1, x2, y2) in [(sxc, ry0 + 140, sxc, ry0 + 100), (mx - 10, ry0 + m, mx + 20, ry0 + m),
                             (rx1 - m - 14, ry0 + 110, rx1 - m - 14, ry0 + 150), (mx + 40, ry1 - m, mx + 10, ry1 - m)]:
        b.append(arrow(x1, y1, x2, y2, "ink", 2.6))
    for k, nm in enumerate(["天井近く", "真ん中", "ゆか近く"]):
        y = ry0 + (ROOM["PR"][k] + 0.5) * nh
        y = min(max(y, ry0 + 58), ry1 - 46) if k != 1 else y
        b.append(tagc(mx + 34, y + 6, f"{nm} {r0(pvr[k])}℃", INK, 15))
    b.append(text(R0 + 18, 494, f"ストーブをつけて{TR_ // 60}分後（たての断面図）", 15, MUTED))
    b.append(text(R0 + 18, 520, f"天井近くとゆか近くの差 約{r0(pvr[0] - pvr[2])}℃", 16, INK, 700))
    b.append(text(R0 + 18, 548, f"せんぷうきで回すと 約{r0(pvf[0] - pvf[2])}℃", 16, TEAL_D, 700))
    b.append(text(R0 + 18, 584, "天井近くからあたたまり、", 16, INK, 700) + text(R0 + 18, 606, "足もとはつめたいまま", 16, INK, 700))
    return svg("".join(b), "物のあたたまり方のしくみ（金ぞく・水・空気）",
               "金ぞくは熱した所から近いじゅんに、水と空気はあたためられた部分が上へ動いて全体があたたまる。")


# ================= 図2：まとめ図 =================
def fig2():
    b = []
    # ---------- 左：試験管の水 ----------
    b.append(text(48, 124, "試験管の水：熱する場所でくらべる", 19, INK, 700))
    TT = 40
    b.append(text(48, 150, f"熱しはじめて{TT}秒後のようす（水20 mL・はじめ20℃）", 15, MUTED))
    b.append(text(48, 178, "しおんインク：", 15, INK2, 700))
    for i, (s, c) in enumerate([("約40℃より低い", "#4f6bd8"), ("約40℃より高い", "#ec6fa6")]):
        b.append(rect(152 + i * 150, 164, 18, 16, c, c, 3, 0) + text(176 + i * 150, 178, s, 15, INK, 700))
    ty0, ty1, tw, rr_ = 238, 420, 46, 23                 # 水面・底（丸い所の下）
    cols = [("bot", "下を熱する", 140), ("mid", "真ん中を熱する", 330), ("top", "上を熱する", 520)]
    res = {}
    for pos, nm, cx in cols:
        _, _, first = fluid(TUBE(pos), 120)               # 2分まで見る
        Lt40, pv40, _ = fluid(TUBE(pos), TT)
        res[pos] = first
        nh = (ty1 - ty0) / 40
        cid = f"tube_{pos}"
        b.append(f'<clipPath id="{cid}"><path d="M{cx - tw / 2},{ty0} L{cx - tw / 2},{ty1 - rr_} A{rr_},{rr_} 0 0 0 {cx + tw / 2},{ty1 - rr_} L{cx + tw / 2},{ty0}Z"/></clipPath>')
        g = [f'<g clip-path="url(#{cid})">']
        for j, v in enumerate(Lt40):
            g.append(f'<rect x="{cx - tw / 2}" y="{ty0 + j * nh:.1f}" width="{tw}" height="{nh + 0.5:.1f}" fill="{ink(v)}"/>')
        g.append("</g>")
        b.append("".join(g))
        b.append(f'<path d="M{cx - tw / 2 - 2},{ty0 - 16} L{cx - tw / 2 - 2},{ty1 - rr_} A{rr_ + 2},{rr_ + 2} 0 0 0 {cx + tw / 2 + 2},{ty1 - rr_} L{cx + tw / 2 + 2},{ty0 - 16}" fill="none" stroke="{INK2}" stroke-width="2.6"/>')
        hL = TUBE(pos)["hL"]
        if pos == "bot":
            b.append(lamp(cx, ty1 + 6, 6.5))
        else:
            fy = ty0 + (hL - 0.5) * nh
            b.append(f'<g transform="translate({cx - tw / 2 - 8},{fy:.1f}) rotate(90)">{flame(0, 0, 7)}</g>')
        for k in range(3):
            y = ty0 + (TUBE(pos)["PR"][k] + 0.5) * nh
            b.append(line(cx + tw / 2 + 3, y, cx + tw / 2 + 12, y, INK2, 1.4) + text(cx + tw / 2 + 15, y + 5, f"{r0(pv40[k])}℃", 15, INK, 700))
            if k == 0 and pv40[0] >= 99.5:
                b.append(text(cx + tw / 2 + 15, y + 24, "ふっとう", 14, ACC, 700))
        b.append(text(cx, 208, nm, 16, INK, 700, "middle"))
    for k, nmk in enumerate(["上", "真ん中", "下"]):
        y = ty0 + (TUBE("bot")["PR"][k] + 0.5) * (ty1 - ty0) / 40
        b.append(text(140 - tw / 2 - 10, y + 5, nmk, 14, INK2, 700, "end"))
    # 40℃になるまでの時間（表）
    def tt(x):
        return f"約{r0(x)}秒" if x is not None else "なかなか…"
    rows = [["上が40℃に"] + [tt(res[p][0]) for p, _, _ in cols],
            ["真ん中が40℃に"] + [tt(res[p][1]) for p, _, _ in cols],
            ["下が40℃に"] + [tt(res[p][2]) for p, _, _ in cols]]
    b.append(table(48, 478, ["40℃になるまで", "下を熱する", "真ん中を熱する", "上を熱する"], rows, [150, 146, 150, 146], 28, 15))
    # ---------- 右：温度と体積 ----------
    X0 = 666
    b.append(text(X0, 124, "温度と体積", 19, INK, 700))
    b.append(text(X0, 150, "20℃のときの体積を100とすると", 15, MUTED))
    trs = []
    for T, nm in [(0, "0℃（氷水）"), (20, "20℃"), (40, "40℃"), (60, "60℃"), (80, "80℃（湯）"), (100, "100℃")]:
        a, w, m = vols(T)
        trs.append([nm, f"{a * 100:.1f}", f"{w * 100:.1f}", f"{m * 100:.2f}"])
    b.append(table(X0, 164, ["温度", "空気", "水", "金ぞく（鉄）"], trs, [136, 104, 104, 142], 38, 16))
    a80, w80, m80 = vols(80)
    yb = 164 + 38 * 7 + 40
    b.append(text(X0, yb, "体積の変わり方", 17, INK, 700) + text(X0 + 136, yb, "空気 ＞ 水 ＞ 金ぞく", 20, ACC, 700))
    b.append(text(X0, yb + 30, "あたためると体積が大きくなり、冷やすと小さくなる。", 15, INK))
    b.append(text(X0, yb + 54, f"20℃→80℃で、空気は約{r0((a80 - 1) * 100)}%、水は約{r0((w80 - 1) * 100)}%、鉄は約{(m80 - 1) * 100:.1f}%", 15, INK))
    b.append(text(X0, yb + 76, "大きくなる。", 15, INK))
    b.append(text(X0, yb + 102, "左の表の「なかなか…」＝2分たっても40℃にならない", 14, MUTED))
    # ---------- 安全 ----------
    b.append(rect(48, 600, 1104, 30, ACC_L, ACC, 6, 1.2))
    b.append(text(60, 621, "注意：熱した金ぞく・試験管・湯は、しばらく熱いのでさわらない。試験管の口を人に向けない。まわりにもえやすい物を置かない。", 15, ACC, 700))
    return svg("".join(b), "試験管の水のあたたまり方と、温度と体積",
               "試験管の水全体を早くあたためるには、下の方を熱する。時間・体積はこのシミュレーターの目安。")


FIGS = [
    dict(svg=fig1, alt="物のあたたまり方のしくみの図。金ぞくの板はかどを熱すると近いじゅんにろうがとけ（ア→イ→ウ）、かたむけたぼうは上にも下にも同じようにあたたまる。水はビーカーの底のはしを熱すると、あたためられた水が上へ動いて上の方からあたたまり（しおんインクの色）、空気はストーブであたためられた空気が上へ動いて天井近くがあたたかく、足もとはつめたいことを示す。",
         caption="物のあたたまり方のしくみ。金ぞくは熱した所から近いじゅんに、水と空気はあたためられた部分が上へ動いて全体があたたまる。"),
    dict(svg=fig2, alt="試験管の水の下・真ん中・上を熱したときのあたたまり方を、しおんインクの色と40℃になるまでの時間でくらべた図と、0℃〜100℃での空気・水・金ぞく（鉄）の体積（20℃を100とする）の早見表。体積の変わり方は空気＞水＞金ぞく。火や熱湯をあつかうときの注意つき。",
         caption="試験管の水は熱する場所であたたまり方が変わる。温度による体積の変わり方は空気がいちばん大きい。"),
]
