"""前線と天気の変化（zensen-tenki）の授業用の図。
前線の位置・雲や雨の範囲・観測記録は、シミュと同じ式（scripts/rika/sims_kishou2.py の _xwf/_xcf/_zrun ほか）を読み込んで計算する。
初期設定＝観測地点は低気圧の中心の南300 km・時速40 km・気温の日変化あり（ページの例題の表と同じ記録）。"""
import os, sys
from figlib import *

_R = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rika")
if _R not in sys.path:
    sys.path.append(_R)
import sims_kishou2 as Z                      # noqa: E402

YS, U = 300, 40                               # 観測地点（中心の南 km）・低気圧の速さ（km/時）
XW, XC = Z._xwf(YS), Z._xcf(YS)               # 観測地点の緯度での温暖前線・寒冷前線の位置（中心から東へ km）
RW = 320 - 0.25 * YS                          # 温暖前線の雨の範囲（前線の東側 km）
TSNAP = 24                                    # 図1の時刻：2日目0時（観測地点は暖域）
XOBS = XW + U * (Z._ZTWF - TSNAP)             # そのときの観測地点の位置（中心から東へ km）
assert XC < XOBS < XW


def _wgroup(d):
    return "N" if "北" in d else ("S" if d in ("南", "南南西", "南西", "西南西") else "E")


def wind_bands():
    """1時間ごとの風向を「東寄り・南寄り・北寄り」に分けた区間（境目は変わった前後の中間）"""
    seq = [(h, Z._ZO(h)["d"]) for h in range(49)]
    bands, start = [], 0
    for i in range(1, len(seq) + 1):
        if i == len(seq) or _wgroup(seq[i][1]) != _wgroup(seq[start][1]):
            ds = [d for _, d in seq[start:i]]
            bands.append((start - (0.5 if start else 0), (i - 0.5) if i < len(seq) else 48, max(set(ds), key=ds.count), _wgroup(ds[0])))
            start = i
    return bands


# ---------------- 部品
def front_symbols(pts, kind, step=40, size=7.5, color=ACC):
    """前線の記号。pts＝前線の線（中心から外へ）。進む向き（東側）に半円（温暖）／三角（寒冷）をつける"""
    out, acc, nxt = [], 0.0, 22.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        seg = math.hypot(x1 - x0, y1 - y0)
        if seg < 1e-9: continue
        tx, ty = (x1 - x0) / seg, (y1 - y0) / seg; nx, ny = ty, -tx       # (ty,−tx)＝東側
        while acc + seg >= nxt:
            q = (nxt - acc) / seg; cx, cy = x0 + (x1 - x0) * q, y0 + (y1 - y0) * q
            ax, ay, bx, by = cx - tx * size, cy - ty * size, cx + tx * size, cy + ty * size
            if kind == "warm":
                sweep = 1 if (tx * ny - ty * nx) < 0 else 0
                out.append(f'<path d="M{ax:.1f},{ay:.1f} A{size},{size} 0 0 {sweep} {bx:.1f},{by:.1f}Z" fill="{color}"/>')
            else:
                out.append(f'<path d="M{ax:.1f},{ay:.1f} L{cx + nx * size * 1.5:.1f},{cy + ny * size * 1.5:.1f} L{bx:.1f},{by:.1f}Z" fill="{color}"/>')
            nxt += step
        acc += seg
    return "".join(out)


def front_sample(x, y, kind):
    col = ACC if kind == "warm" else TEAL
    pts = [(x, y), (x + 64, y)]
    return poly(pts, col, 3) + front_symbols(pts, kind, 32, 7, col)


def wx_symbol(x, y, wx, r=8):
    """天気図記号（快晴○・晴れ（○に縦線）・くもり◎・雨●・強い雨は大きい●）"""
    if wx == -1: return circle(x, y, r, CARD, INK, 1.8)
    if wx == 0: return circle(x, y, r, CARD, INK, 1.8) + line(x, y - r, x, y + r, INK, 1.8)
    if wx == 1: return circle(x, y, r, CARD, INK, 1.8) + circle(x, y, r * 0.45, CARD, INK, 1.6)
    return circle(x, y, r * (1.3 if wx == 3 else 1), INK, INK, 0)


# ---------------- 図1：上から見た図＋断面図
def fig1():
    b = []
    # 左：上から見た図
    MXL, MXR, MYT, MYB, sc, cx0, cy0 = 48, 468, 136, 456, 0.3, 215, 190
    PX = lambda xkm: cx0 + xkm * sc
    PY = lambda skm: cy0 + skm * sc
    b.append(text(MXL, 122, "上から見た図（天気図）", 18, INK, 700))
    b.append(rect(MXL, MYT, MXR - MXL, MYB - MYT, CARD, LINE, 8))
    defs = f'<clipPath id="zt-map"><rect x="{MXL}" y="{MYT}" width="{MXR - MXL}" height="{MYB - MYT}" rx="8"/></clipPath>'
    m = []
    wf = [(PX(Z._xwf(s)), PY(s)) for s in range(0, 741, 10)]
    cf = [(PX(Z._xcf(s)), PY(s)) for s in range(0, 941, 10)]
    # 暖域（2つの前線の間）をうすく
    m.append(f'<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in wf + [(wf[-1][0], MYB + 60), (cf[-1][0], MYB + 60)] + cf[::-1]) + f'Z" fill="{ACC_L}"/>')
    m.append(poly(wf, ACC, 3) + front_symbols(wf, "warm", 40, 7.5, ACC))
    m.append(poly(cf, TEAL, 3) + front_symbols(cf, "cold", 40, 7.5, TEAL))
    ys = PY(YS)
    m.append(line(MXL, ys, MXR, ys, INK2, 1.6, "7 5"))
    b.append(f'<g clip-path="url(#zt-map)">{"".join(m)}</g>')
    b.append(text(MXL + 8, ys - 8, "西", 15, INK2, 700) + text(MXR - 8, ys - 8, "東", 15, INK2, 700, "end"))
    b.append(text(PX(XC) + 12, ys + 22, "断面図の線（右の図）", 14, INK2))
    ox = PX(XOBS)
    b.append(f'<path d="M{ox:.1f},{ys - 2:.1f} l-8,-14 h16z" fill="{INK}"/>')
    b.append(text(ox + 4, ys - 20, "観測地点", 14, INK, 700, "middle"))
    b.append(line(cx0 - 7, cy0 - 7, cx0 + 7, cy0 + 7, ACC, 3) + line(cx0 - 7, cy0 + 7, cx0 + 7, cy0 - 7, ACC, 3))
    b.append(text(cx0 - 14, cy0 - 10, "低", 26, ACC, 700, "end"))
    b.append(text(PX(110), PY(560), "暖気", 18, ACC, 700, "middle"))
    b.append(text(PX(-420), PY(150), "寒気", 18, TEAL_D, 700, "middle"))
    b.append(text(PX(640), PY(130), "寒気", 18, TEAL_D, 700, "middle"))
    b.append(text(300, 160, "西から東へ進む", 14, INK2) + arrow(300, 172, 398, 172, "ink", 2))
    b.append(line(310, 438, 310 + 500 * sc, 438, INK, 2) + line(310, 432, 310, 444, INK, 2) + line(310 + 500 * sc, 432, 310 + 500 * sc, 444, INK, 2)
             + text(310 + 250 * sc, 428, "500 km", 14, INK, anchor="middle"))
    b.append(front_sample(56, 490, "warm") + text(132, 496, "温暖前線（南東にのびる）", 16, ACC, 700))
    b.append(front_sample(56, 524, "cold") + text(132, 530, "寒冷前線（南西にのびる）", 16, TEAL_D, 700))
    b.append(lines(56, 566, ["記号は前線が進む向き（東）の側につく。", "低気圧と前線は西から東へ進む。"], 15, INK2))
    # 右：断面図（観測地点を通る西→東）
    SL, SR, L, R, G, EX = 506, 1152, -460, 1000, 556, 75
    kx = (SR - SL) / (R - L); kz = EX * kx
    X = lambda xkm: SL + (xkm - L) * kx
    Zy = lambda zkm: G - zkm * kz
    zc = lambda p: max(0.0, min(10.6, (XC - p) / 60))
    zw = lambda p: max(0.0, min(10.6, (p - XW) / 180))
    b.append(text(SL, 122, "断面図（観測地点を通る西→東・2日目0時ごろ）", 18, INK, 700))
    b.append(text(SL, 144, f"高さは横の約{EX}倍に強調（大きさ・きょりは実際とちがう）", 14, MUTED))
    top = Zy(10.6)
    s = [f'<rect x="{SL}" y="{top:.1f}" width="{SR - SL}" height="{G - top:.1f}" fill="{ACC_L}"/>']
    cold_l = [(X(L), G)] + [(X(p), Zy(zc(p))) for p in range(int(XC), L - 1, -10)] + [(X(L), Zy(zc(L)))]
    cold_r = [(X(XW), G)] + [(X(p), Zy(zw(p))) for p in range(int(XW), R + 1, 10)] + [(X(R), G)]
    for pts in (cold_l, cold_r):
        s.append(f'<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f'Z" fill="#dce8ef"/>')

    def puffs(cs, fill, stroke):
        """だ円を重ねた雲（ふちだけ線）"""
        e = "".join(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx:.1f}" ry="{ry:.1f}"/>' for x, y, rx, ry in cs)
        return f'<g fill="{fill}" stroke="{stroke}" stroke-width="4">{e}</g><g fill="{fill}">{e}</g>'
    # 巻層雲・巻雲（前線から遠い高い所）
    a3, b3 = XW + RW + 110, XW + RW + 330
    for k in range(3):
        yy = Zy(7.7 + k * 0.45); xa, xb = X(a3 + k * 30), X(min(b3 - k * 40, R))
        s.append(f'<path d="M{xa:.1f},{yy:.1f} Q{(xa + xb) / 2:.1f},{yy - 8:.1f} {xb:.1f},{yy + 2:.1f}" fill="none" stroke="#c9ccd1" stroke-width="6" stroke-linecap="round"/>'
                 f'<path d="M{xa:.1f},{yy:.1f} Q{(xa + xb) / 2:.1f},{yy - 8:.1f} {xb:.1f},{yy + 2:.1f}" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/>')
    # 高層雲（中くらいの高さ・うすい層）
    a2, b2 = XW + RW * 0.55, XW + RW + 200
    s.append(puffs([(X(p), Zy(5.85 - 0.5 * (p - a2) / (b2 - a2)), 22, 9) for p in frange(a2 + 20, b2 - 20, 26)], "#eceef1", "#a3a8b0"))
    # 乱層雲（温暖前線の前に広がる厚い雲）：下のふちは前線面の少し上、上は約5 km
    b1 = XW + RW
    cs = []
    for p in frange(XW + 14, b1 - 6, 22):
        lo, hi = zw(p) + 0.45, 5.3 - 0.9 * (p - XW) / (b1 - XW)
        hi = min(hi, lo + 0.9 + (p - XW) * 0.04)
        cs.append((X(p), Zy((lo + hi) / 2), 20, (hi - lo) / 2 * kz + 4))
    s.append(puffs(cs, "#a7adb5", "#6b7280"))
    # 雨（温暖前線：前線の東側 RW km の広い範囲、寒冷前線：前線の西55 km〜東12 km のせまい範囲）
    for p in frange(XW + 6, b1 - 4, 10):
        x = X(p); y0 = Zy(zw(p) + 0.45) + 6
        for k in range(int((G - y0) / 20)):
            yy = y0 + 4 + k * 20 + (p * 3.7) % 10
            if yy + 8 < G: s.append(line(x, yy, x - 2, yy + 9, "#4a7fa5", 1.6))
    for p in frange(XC - 52, XC + 10, 8.5):
        x = X(p); y0 = Zy(1.25)
        for k in range(int((G - y0) / 13)):
            yy = y0 + 4 + k * 13 + (p * 5.3) % 6
            if yy + 10 < G: s.append(line(x, yy, x - 3, yy + 10, TEAL_D, 2))
    # 積乱雲（寒冷前線のすぐ後ろで、おし上げられた暖気がたてにのびる）
    cx = X(XC - 15)
    tower = [(cx + 10 * math.sin(k * 1.9), 1.7 + k * 0.5, 25 - k * 0.4, 25 - k * 0.4) for k in range(15)]
    tower += [(cx + 26, 9.7, 84, 13)] + [(cx - 40 + k * 22, 9.95, 12, 12) for k in range(6)]
    s.append(puffs([(x, Zy(z), rx, ry) for x, z, rx, ry in tower], "#fff", "#8a919b"))
    # 前線面
    s.append(line(X(XC), G, X(L), Zy(zc(L)), TEAL, 3.4) + line(X(XW), G, X(R), Zy(zw(R)), ACC, 3.4))
    defs += f'<clipPath id="zt-sec"><rect x="{SL}" y="{top:.1f}" width="{SR - SL}" height="{G - top + 1:.1f}"/></clipPath>'
    b.append(f'<g clip-path="url(#zt-sec)">{"".join(s)}</g>')
    b.append(rect(SL, top, SR - SL, G - top, "none", LINE, 0, 1))
    b.append(f'<rect x="{SL}" y="{G}" width="{SR - SL}" height="10" fill="#c9bfa6"/>')
    for zz in (5, 10):
        b.append(line(SR - 8, Zy(zz), SR, Zy(zz), INK2, 1.4) + text(SR - 12, Zy(zz) + 5, f"{zz} km", 14, INK2, anchor="end"))
    # 空気の動き
    b.append(arrow(X(XC - 200), Zy(0.55), X(XC - 62), Zy(0.55), "teal", 3.4))
    b.append(arrow(X(XC + 80), Zy(0.6), X(XC + 12), Zy(4.0), "acc", 3.4))
    b.append(arrow(X(XW - 150), Zy(0.9), X(XW + 200), Zy(zw(XW + 200) + 1.2), "acc", 3.4))
    # ラベル
    b.append(text(X(-375), Zy(1.5), "寒気", 18, TEAL_D, 700, "middle"))
    b.append(text(X(890), Zy(0.4), "寒気", 18, TEAL_D, 700, "middle"))
    b.append(text(X(160), Zy(6.2), "暖気", 18, ACC, 700, "middle"))
    b.append(text(cx + 36, Zy(7.2), "積乱雲", 16, INK, 700))
    b.append(text(X(XW + 150), Zy(3.2), "乱層雲", 16, "#fff", 700, "middle"))
    b.append(text(X((a2 + b2) / 2), Zy(6.75), "高層雲", 15, INK2, 700, "middle"))
    b.append(text(X(a3 + 110), Zy(9.25), "巻層雲・巻雲", 15, INK2, 700, "middle"))
    b.append(text(SL + 10, Zy(zc(L)) - 34, "寒冷前線面", 15, TEAL_D, 700))
    b.append(text(SL + 10, Zy(zc(L)) - 14, "（傾きが急）", 14, TEAL_D))
    ang = -math.degrees(math.atan(kz / 180 / kx))
    lx = X(XW + 252); ly = Zy(zw(XW + 252)) + 22
    b.append(f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="15" fill="{ACC}" font-weight="700" transform="rotate({ang:.1f} {lx:.1f} {ly:.1f})">温暖前線面（ゆるやか）</text>')
    # 地上
    xo = X(XOBS)
    b.append(line(xo, G, xo, G - 22, INK, 2) + f'<path d="M{xo:.1f},{G - 22} l13,4 l-13,4z" fill="{INK}"/>')
    b.append(text(xo, G + 32, "観測地点", 15, INK, 700, "middle"))
    b.append(text(X(XC), G + 32, "寒冷前線", 16, TEAL_D, 700, "middle"))
    b.append(text(X(XW), G + 32, "温暖前線", 16, ACC, 700, "middle"))
    b.append(text(X(XC), G + 54, "せまい範囲に強い雨", 14, TEAL_D, anchor="middle"))
    b.append(text(X(XW + RW / 2), G + 54, "広い範囲におだやかな雨", 14, "#3f6f91", anchor="middle"))
    b.append(text(SR, 168, "前線は西から東（右）へ進む", 14, INK2, anchor="end") + arrow(SR - 196, 182, SR - 6, 182, "ink", 2))
    return svg("".join(b), "寒冷前線と温暖前線のしくみ（天気図と断面図）",
               "寒冷前線は寒気が暖気の下にもぐりこみ、温暖前線は暖気が寒気の上をはい上がる。", defs)


def frange(a, b, st):
    out, v = [], a
    if st > 0:
        while v <= b + 1e-9: out.append(v); v += st
    else:
        while v >= b - 1e-9: out.append(v); v += st
    return out


# ---------------- 図2：観測記録の読み取り＋ちがいの表
def fig2():
    b = []
    GL, GR = 152, 650
    gx = lambda h: GL + h / 48 * (GR - GL)
    TOP, BOT = 132, 556
    # 前線の通過（3時間ごとの記録で「〜時から〜時の間」）
    ROWS = Z._ZROWS
    kw = next(k for k in range(16) if ROWS[k]["wx"] >= 2 and ROWS[k + 1]["wx"] <= 1)
    kc = next(k for k in range(kw + 1, 16) if ROWS[k]["wx"] >= 2 and ROWS[k + 1]["wx"] <= 1)
    assert (kw, kc) == (5, 10)
    for k, col, nm in ((kw, ACC, "温暖前線の通過"), (kc, TEAL, "寒冷前線の通過")):
        x0, x1 = gx(3 * k), gx(3 * k + 3)
        b.append(f'<rect x="{x0:.1f}" y="{TOP}" width="{x1 - x0:.1f}" height="{BOT - TOP}" fill="{col}" opacity=".13"/>')
        b.append(text((x0 + x1) / 2, TOP - 8, nm, 15, col if col == ACC else TEAL_D, 700, "middle"))
    # 天気（3時間ごと）
    b.append(text(48, 161, "天気", 15, INK, 700))
    for k, o in enumerate(ROWS):
        b.append(wx_symbol(gx(3 * k), 156, o["wx"], 7.5))
    # 風向（向きのまとまり）
    b.append(text(48, 196, "風向", 15, INK, 700))
    for h0, h1, d, g in wind_bands():
        x0, x1 = gx(h0), gx(h1)
        fill = {"E": GOLD_L, "S": ACC_L, "N": TEAL_L}[g]
        b.append(f'<rect x="{x0 + 1:.1f}" y="178" width="{x1 - x0 - 2:.1f}" height="26" rx="5" fill="{fill}" stroke="{LINE}"/>')
        if x1 - x0 > 60: b.append(text((x0 + x1) / 2, 196, f"{d}の風", 15, INK, 700, "middle"))
    # 降水量（1時間ごと・mm）
    py0, pk = 290, 3.6
    b.append(text(48, py0 - 38, "降水量", 15, INK, 700) + text(48, py0 - 18, "［mm］", 14, INK2))
    for v in (0, 10, 20):
        b.append(line(GL, py0 - v * pk, GR, py0 - v * pk, LINE, 1) + text(GL - 6, py0 - v * pk + 5, str(v), 14, INK2, anchor="end"))
    for h in range(48):
        r = Z._HR[h]
        if r >= 0.05:
            b.append(f'<rect x="{gx(h) + 1:.1f}" y="{py0 - r * pk:.1f}" width="{gx(1) - gx(0) - 2:.1f}" height="{r * pk:.1f}" fill="#5b8fb3"/>')
    b.append(text(gx(13), py0 - 20, f"約{len(Z._WR)}時間おだやかに", 14, "#3f6f91", anchor="middle"))
    b.append(text(gx(30.5) - 14, py0 - 54, f"約{len(Z._CR)}時間・強い雨", 14, TEAL_D, 700, "end"))
    # 気温
    ty0, tlo, thi = 410, 8, 22
    tk = 100 / (thi - tlo)
    ty = lambda T: ty0 - (T - tlo) * tk
    b.append(text(48, ty(15) - 4, "気温", 15, INK, 700) + text(48, ty(15) + 16, "［℃］", 14, INK2))
    for v in (10, 15, 20):
        b.append(line(GL, ty(v), GR, ty(v), LINE, 1) + text(GL - 6, ty(v) + 5, str(v), 14, INK2, anchor="end"))
    b.append(poly([(gx(q / 4), ty(Z._ZO(q / 4)["T"])) for q in range(0, 193)], ACC, 2.8))
    t30, t33 = ROWS[kc]["T"], ROWS[kc + 1]["T"]
    b.append(text(gx(33) + 8, ty(t33) + 22, f"急に下がる（{Z._f1(t30)}→{Z._f1(t33)}℃）", 14, ACC, 700))
    b.append(text(gx(18) + 6, ty(ROWS[kw + 1]["T"]) - 10, "上がる", 14, ACC, 700))
    # 気圧
    py1, plo, phi = 530, 988, 1018
    pkk = 100 / (phi - plo)
    pyy = lambda P: py1 - (P - plo) * pkk
    b.append(text(48, pyy(1005) - 4, "気圧", 15, INK, 700) + text(48, pyy(1005) + 16, "［hPa］", 14, INK2))
    for v in (995, 1005, 1015):
        b.append(line(GL, pyy(v), GR, pyy(v), LINE, 1) + text(GL - 6, pyy(v) + 5, str(v), 14, INK2, anchor="end"))
    pts = [(q / 4, Z._ZO(q / 4)["P"]) for q in range(0, 193)]
    b.append(poly([(gx(h), pyy(P)) for h, P in pts], TEAL_D, 2.8))
    hmin, pmin = min(pts, key=lambda a: a[1])
    b.append(circle(gx(hmin), pyy(pmin), 4.5, TEAL_D, TEAL_D, 0) + text(gx(hmin), pyy(pmin) + 24, "いちばん低い→上がる", 14, TEAL_D, 700, "middle"))
    # 横軸
    b.append(line(GL, BOT, GR, BOT, INK, 1.6))
    for h in range(0, 49, 6):
        b.append(line(gx(h), BOT, gx(h), BOT + 6, INK, 1.4) + text(gx(h), BOT + 24, f"{h % 24}時", 14, INK2, anchor="middle"))
    for d in range(3):
        b.append(text(gx(24 * d), BOT + 44, f"{d + 1}日目", 14, INK, 700, "middle"))
    b.append(text(GR, BOT + 64, "天気記号：○ 快晴　⦶ 晴れ　◎ くもり　● 雨", 14, MUTED, anchor="end"))
    # 右：ちがいの表
    TX, TW = 690, 462
    cw = [118, 172, 172]
    b.append(text(TX, 122, "寒冷前線と温暖前線のちがい", 18, INK, 700))
    rows = [("前線面の傾き", ["急"], ["ゆるやか"]),
            ("できる雲", ["積乱雲"], ["乱層雲など"]),
            ("雨の降り方", ["せまい範囲に", "短時間の強い雨"], ["広い範囲に", "長時間のおだやかな雨"]),
            ("通過後の気温", ["急に下がる"], ["上がる"]),
            ("風向の変化", ["南寄り → 北寄り"], ["東寄り → 南寄り"]),
            ("天気図の記号", None, None)]
    hh, y = 44, 136
    b.append(rect(TX, y, TW, hh + sum(64 if r[1] and len(r[1]) > 1 else 50 for r in rows), CARD, LINE, 8))
    b.append(f'<rect x="{TX}" y="{y}" width="{TW}" height="{hh}" rx="8" fill="{TEAL_L}"/>')
    b.append(text(TX + cw[0] + cw[1] / 2, y + 29, "寒冷前線", 17, TEAL_D, 700, "middle") + text(TX + cw[0] + cw[1] + cw[2] / 2, y + 29, "温暖前線", 17, ACC, 700, "middle"))
    y += hh
    for i, (lab, c1, c2) in enumerate(rows):
        rh = 64 if c1 and len(c1) > 1 else 50
        if i % 2: b.append(f'<rect x="{TX + 1}" y="{y}" width="{TW - 2}" height="{rh}" fill="#f7f5ef"/>')
        b.append(line(TX, y, TX + TW, y, LINE, 1))
        b.append(text(TX + 12, y + rh / 2 + 6, lab, 15, INK, 700))
        if c1 is None:
            b.append(front_sample(TX + cw[0] + cw[1] / 2 - 32, y + rh / 2, "cold") + front_sample(TX + cw[0] + cw[1] + cw[2] / 2 - 32, y + rh / 2, "warm"))
        else:
            for j, c in enumerate((c1, c2)):
                xc = TX + cw[0] + sum(cw[1:1 + j]) + cw[1 + j] / 2
                y0 = y + rh / 2 + 6 - (len(c) - 1) * 11
                b.append(lines(xc, y0, c, 15, INK, 1.45, anchor="middle"))
        y += rh
    b.append(lines(TX, y + 26, ["夜は前線と関係なく気温が下がるので、", "風向・気圧・雨も合わせて読み取る。"], 15, INK2))
    return svg("".join(b), "前線の通過と天気の変化（観測記録の読み取り）",
               f"観測地点は低気圧の中心の南{YS} km・時速{U} kmで通過するときのモデルの記録（実際の観測値ではない）。")


FIGS = [
    dict(svg=fig1,
         alt="温帯低気圧の天気図ふうの図と、観測地点を通る西から東への断面図。寒冷前線では寒気が暖気の下にもぐりこんで暖気をおし上げ、積乱雲ができてせまい範囲に強い雨が降る。温暖前線では暖気が寒気の上をゆるやかにはい上がり、乱層雲・高層雲・巻層雲が広がって広い範囲におだやかな雨が降る。",
         caption="寒冷前線と温暖前線のしくみ。断面図は高さを約50倍に強調している。"),
    dict(svg=fig2,
         alt="前線が通過した2日間の観測記録（天気・風向・降水量・気温・気圧）のグラフと、寒冷前線と温暖前線のちがい（前線面の傾き・雲・雨の降り方・通過後の気温・風向の変化・記号）をまとめた表。温暖前線は1日目15時から18時の間、寒冷前線は2日目6時から9時の間に通過している。",
         caption="前線の通過と天気の変化の読み取り。寒冷前線は気温の急な低下と北寄りの風への変化でわかる。"),
]
