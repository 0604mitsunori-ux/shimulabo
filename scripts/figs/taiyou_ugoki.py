"""太陽の1日の動きと季節（taiyou-ugoki）の授業用の図
   数値はページの JS（scripts/rika/sims_tentai.py の CORE1）と同じ式：
   赤緯＝asin(sin23.4°×sin黄経)（黄経は2026年の春分3/20・夏至6/21・秋分9/23・冬至12/22の正午に0・90・180・270°となるよう直線でつなぐ）、
   均時差は USNO の近似式、日の出入りは太陽の上のふち（−0.8333°）、透明半球はななめ上（南南東）から見た図（シミュと同じ投影）。"""
import math
from figlib import *

R = math.pi / 180
EPS, H0 = 23.4, -0.8333
LOC = {"tokyo": ("東京", 35.6581, 139.7414), "sapporo": ("札幌", 43.0667, 141.35), "naha": ("那覇", 26.2167, 127.6667)}
SEAS = [(79, "春分"), (172, "夏至"), (266, "秋分"), (356, "冬至")]
ANC = [(79.5, 0), (172.5, 90), (266.5, 180), (356.5, 270), (444.5, 360)]


def lam_of(t):
    if t < ANC[0][0]: t += 365
    for i in range(4):
        a, b = ANC[i], ANC[i + 1]
        if t <= b[0]: return a[1] + (b[1] - a[1]) * (t - a[0]) / (b[0] - a[0])
    return 0


def dec_of(n): return math.asin(math.sin(EPS * R) * math.sin(lam_of(n + 0.5) * R)) / R


def eot_of(n):
    d = (n - 1) + 3 / 24 + 2461041.5 - 2451545            # Date.UTC(2026,0,n,3) の JD − J2000
    g = (357.529 + 0.98560028 * d) * R; q = 280.459 + 0.98564736 * d
    L = (q + 1.915 * math.sin(g) + 0.020 * math.sin(2 * g)) * R; e = (23.439 - 0.00000036 * d) * R
    return ((q - math.atan2(math.cos(e) * math.sin(L), math.cos(L)) / R + 180) % 360 + 360) % 360 - 180


def sun_day(n, lat, lon):
    d = dec_of(n); E = eot_of(n); noon = 12 - (lon - 135) / 15 - E / 15
    sl, cl, sd, cd = math.sin(lat * R), math.cos(lat * R), math.sin(d * R), math.cos(d * R)
    c = (math.sin(H0 * R) - sl * sd) / (cl * cd); h0 = 180 if c <= -1 else 0 if c >= 1 else math.acos(c) / R
    top = 90 - lat + d
    return dict(d=d, noon=noon, len=2 * h0 / 15, rise=noon - h0 / 15, set=noon + h0 / 15, top=top, shift=math.asin(sd / cl) / R)


def sun_at(n, lat, lon, t):
    """高度・方位（南から西回り）"""
    d = dec_of(n) * R; Hd = 15 * (t - 12) + (lon - 135) + eot_of(n); Hr = Hd * R; la = lat * R
    h = math.asin(math.sin(la) * math.sin(d) + math.cos(la) * math.cos(d) * math.cos(Hr))
    return h / R, math.atan2(math.sin(Hr), math.cos(Hr) * math.sin(la) - math.tan(d) * math.cos(la)) / R


def tw(s, size):
    return sum(size * (0.56 if ord(c) < 0x2000 else 1.0) for c in s)


def hm(h):
    m = round(h * 60); return f"{m // 60}時間{m % 60:02d}分"


# 透明半球（シミュと同じ：ななめ上の南南東から見た図、東が右手前）
CP, SP, SLV, CLV = math.cos(28 * R), math.sin(28 * R), math.sin(24 * R), math.cos(24 * R)
CX, CY, RD = 356, 448, 262


def P3(e, n, z): return (CX + (e * CP + n * SP) * RD, CY - ((n * CP - e * SP) * SLV + z * CLV) * RD)


def PS(h, A, k=1.0):
    c = math.cos(h * R) * k
    return P3(-math.sin(A * R) * c, -math.cos(A * R) * c, math.sin(h * R) * k)


def path(n, lat, lon):
    pts, pv = [], None
    for i in range(0, 289):
        t = i / 12; sv = sun_at(n, lat, lon, t)
        if pv is not None and (pv[0] < 0) != (sv[0] < 0):       # 地平線との交わり
            f = pv[0] / (pv[0] - sv[0]); q = sun_at(n, lat, lon, t - (1 - f) / 12); pts.append(PS(0, q[1]))
        if sv[0] >= 0: pts.append(PS(sv[0], sv[1]))
        pv = sv
    return pts


TK = LOC["tokyo"]


def fig1():
    b = []
    lat, lon = TK[1], TK[2]
    # 台紙と方位の線
    b.append(f'<ellipse cx="{CX}" cy="{CY}" rx="{RD}" ry="{RD * SLV:.1f}" fill="#efe9da" stroke="{INK2}" stroke-width="1.4"/>')
    for a, c in [((1, 0, 0), (-1, 0, 0)), ((0, 1, 0), (0, -1, 0))]:
        p, q = P3(*a), P3(*c); b.append(line(p[0], p[1], q[0], q[1], MUTED, 1.2, "4 4"))
    # 透明半球
    b.append(f'<path d="M{CX - RD},{CY} A{RD},{RD} 0 0 1 {CX + RD},{CY}" fill="#ffffff" fill-opacity=".45" stroke="{TEAL}" stroke-width="1.8"/>')
    mer = [PS(t, 0) if t <= 90 else PS(180 - t, 180) for t in range(0, 181, 5)]
    b.append(poly(mer, MUTED, 1.2, dash="2 5"))
    cols = {172: (ACC, "夏至"), 79: (GOLD, "春分・秋分"), 356: (TEAL, "冬至")}
    for n in (356, 79, 172):
        col, nm = cols[n]
        pts = path(n, lat, lon)
        b.append(poly(pts, "#fff", 7) + poly(pts, col, 3.4))
        for k in range(24):
            sv = sun_at(n, lat, lon, k)
            if sv[0] < 0.5: continue
            q = PS(sv[0], sv[1]); b.append(circle(q[0], q[1], 4.2, "#fff", col, 2))
        s = sun_day(n, lat, lon)
        # 日の出・日の入りの位置
        for A in (-90 - s["shift"], 90 + s["shift"]):
            q = PS(0, A); b.append(circle(q[0], q[1], 5.5, col, "#fff", 1.5))
    # 時刻の目もり（春分・秋分の道すじに）
    HALO = dict(stroke=BG, stroke_width=5, paint_order="stroke")
    for k, dx, dy, anc in ((9, -12, 20, "end"), (12, 4, 26, "middle"), (15, -12, 22, "end")):
        sv = sun_at(79, lat, lon, k); q = PS(sv[0], sv[1])
        b.append(text(q[0] + dx, q[1] + dy, f"{k}時", 15, "#7a5a10", 700, anc, **HALO))
    # 南中の位置（子午線との交点）に小さな印
    for n in (172, 79, 356):
        col, nm = cols[n]; s = sun_day(n, lat, lon); q = PS(s["top"], 0)
        b.append(f'<rect x="{q[0] - 5:.1f}" y="{q[1] - 5:.1f}" width="10" height="10" fill="{col}" stroke="#fff" stroke-width="1.5" transform="rotate(45 {q[0]:.1f} {q[1]:.1f})"/>')
    # 凡例（下の空いている所）
    lx = 48
    for n in (172, 79, 356):
        col, nm = cols[n]; s = sun_day(n, lat, lon); t = f"{nm} 南中{s['top']:.1f}°"
        b.append(line(lx, 584, lx + 30, 584, col, 4) + text(lx + 38, 590, t, 16, col, 700)); lx += 38 + tw(t, 16) + 22
    b.append(f'<rect x="{lx}" y="579" width="10" height="10" fill="{INK2}" transform="rotate(45 {lx + 5} 584)"/>' + text(lx + 16, 590, "＝南中（真南）", 15, INK2))
    O = P3(0, 0, 0); b.append(circle(O[0], O[1], 4, ACC, ACC, 0) + text(O[0] - 10, O[1] + 24, "観測者 O", 14, INK2, anchor="end", **HALO))
    for nm, e, n in (("東", 1, 0), ("西", -1, 0), ("南", 0, -1), ("北", 0, 1)):
        q = P3(e * 1.1, n * 1.1, 0); b.append(text(q[0], q[1] + 8, nm, 22, INK, 700, "middle"))
    b.append(text(48, 128, "透明半球に記録した太陽の通り道（東京・北緯35.7°）", 18, INK, 700))
    b.append(text(48, 614, "○は1時間ごとの位置、●は日の出・日の入りの位置。", 14.5, INK2))
    # 右：早見表
    x0 = 676
    b.append(text(x0, 128, "季節による違い（東京・2026年）", 18, INK, 700))
    rows = []
    for n, nm in ((172, "夏至"), (79, "春分"), (266, "秋分"), (356, "冬至")):
        s = sun_day(n, lat, lon); sh = round(abs(s["shift"]))
        rows.append([nm, f"{s['top']:.1f}°", hm(s["len"]), "真東・真西" if sh == 0 else ("北" if s["shift"] > 0 else "南") + f"へ約{sh}°"])
    b.append(table(x0, 144, ["季節", "南中高度", "昼の長さ", "日の出・日の入り"], rows, [76, 104, 140, 156], 44, 16))
    b.append(text(x0, 384, "日の出・日の入りの方位は、真東・真西からのずれ。", 14, MUTED))
    b.append(lines(x0, 424, ["・太陽は東からのぼり、南を通って西へしずむ。",
                             "　1時間ごとの印の間隔は同じ（1時間に約15°）。",
                             "・夏至は北寄りからのぼり、南中高度が高く、昼が長い。",
                             "　冬至は南寄りからのぼり、低く、昼が短い。",
                             "・地軸が23.4°かたむいたまま公転しているため。"], 15.5, INK, gap=1.55))
    return svg("".join(b), "季節による太陽の通り道（透明半球）",
               "透明半球をななめ上（南南東）から見た図。季節によって通り道が南北に平行に移る。")


def fig2():
    b = []
    # ---- 左：地球の断面（春分・秋分の日の正午）----
    ex, ey, er, phi = 262, 392, 128, TK[1]
    b.append(text(48, 128, "地球の断面で考える（春分・秋分の日）", 17, INK, 700))
    ox, oy = ex - er * math.cos(phi * R), ey - er * math.sin(phi * R)
    for y in (222, 256, oy, 430, 474, 518):
        if abs(y - ey) < er - 6:
            xs = ex - math.sqrt(er * er - (y - ey) ** 2)
            b.append(arrow(48, y, xs - 4, y, "gold", 2.4 if y == oy else 2))
    b.append(text(52, 502, "太陽の光", 15, GOLD, 700))
    b.append(circle(ex, ey, er, "#dbe8f1", TEAL, 2))
    b.append(line(ex, ey - er - 26, ex, ey + er + 14, INK2, 1.4, "5 4") + text(ex + 8, ey - er - 14, "北極", 15, INK2, 700))
    b.append(line(ex - er, ey, ex + er, ey, INK2, 1.4, "5 4") + text(ex + er - 4, ey - 8, "赤道", 15, INK2, 700, "end"))
    b.append(line(ex, ey, ox, oy, INK2, 1.4))
    tx, ty = -math.sin(phi * R), math.cos(phi * R)                 # 南向きの地平線（画面座標）
    b.append(line(ox - tx * 70, oy - ty * 70, ox + tx * 92, oy + ty * 92, ACC, 2.6))
    b.append(text(ox + tx * 92 - 4, oy + ty * 92 + 20, "地平線（南）", 14, ACC, 700, "middle"))
    zx, zy = -math.cos(phi * R), -math.sin(phi * R)
    b.append(line(ox, oy, ox + zx * 60, oy + zy * 60, INK2, 1.4, "3 3") + text(ox + zx * 60 - 6, oy + zy * 60 + 6, "真上", 14, INK2, anchor="end"))
    a0, a1 = math.atan2(ty, tx), math.pi                           # 南の地平線 → 太陽の向き
    rr = 46
    b.append(f'<path d="M{ox + rr * math.cos(a0):.1f},{oy + rr * math.sin(a0):.1f} A{rr},{rr} 0 0 1 {ox + rr * math.cos(a1):.1f},{oy + rr * math.sin(a1):.1f}" fill="none" stroke="{ACC}" stroke-width="2.2"/>')
    am = (a0 + a1) / 2
    b.append(text(ox + 62 * math.cos(am), oy + 62 * math.sin(am) + 12, f"90°−緯度", 15, ACC, 700, "end"))
    b.append(circle(ox, oy, 5, ACC, "#fff", 1.5))
    r2 = 40; c0, c1 = math.pi, math.pi + phi * R
    b.append(f'<path d="M{ex + r2 * math.cos(c0):.1f},{ey + r2 * math.sin(c0):.1f} A{r2},{r2} 0 0 1 {ex + r2 * math.cos(c1):.1f},{ey + r2 * math.sin(c1):.1f}" fill="none" stroke="{TEAL}" stroke-width="2"/>')
    b.append(text(ex - 50, ey - 10, "緯度", 15, TEAL, 700, "end"))
    b.append(lines(48, 556, ["夏至：北極側が太陽の方へ23.4°かたむく → ＋23.4°",
                             "冬至：南極側が太陽の方へ23.4°かたむく → −23.4°"], 14.5, INK2, gap=1.5))
    # ---- 中：東京の南中高度（真南を向いて横から見た図）----
    O = (650, 404); Rr = 196
    b.append(text(430, 128, "東京（北緯35.7°）の南中高度", 17, INK, 700))
    b.append(line(442, O[1], 820, O[1], INK, 2.2))
    b.append(text(452, O[1] + 26, "南", 18, INK, 700) + text(808, O[1] + 26, "北", 18, INK, 700, "end"))
    b.append(line(O[0], O[1], O[0], O[1] - Rr - 10, MUTED, 1.2, "3 4") + text(O[0] + 6, O[1] - Rr - 2, "天頂", 14, MUTED))
    cols = [(172, ACC, "夏至"), (79, GOLD, "春分・秋分"), (356, TEAL, "冬至")]
    for i, (n, col, nm) in enumerate(cols):
        s = sun_day(n, TK[1], TK[2]); t = s["top"] if n != 79 else 90 - TK[1]
        tt = round(t, 1)
        px, py = O[0] - Rr * math.cos(t * R), O[1] - Rr * math.sin(t * R)
        b.append(line(O[0], O[1], px, py, col, 2.2))
        ra = 52 + i * 26
        b.append(f'<path d="M{O[0] - ra},{O[1]} A{ra},{ra} 0 0 1 {O[0] - ra * math.cos(t * R):.1f},{O[1] - ra * math.sin(t * R):.1f}" fill="none" stroke="{col}" stroke-width="2"/>')
        b.append(circle(px, py, 15, SUN, col, 2.4))
        b.append(text(px - 22, py - 8, nm, 16, col, 700, "end") + text(px - 22, py + 12, f"{tt:.1f}°", 18, col, 700, "end"))
    b.append(circle(O[0], O[1], 4.5, INK, INK, 0))
    bx, by = 430, 444
    b.append(rect(bx, by, 380, 150, TEAL_L, TEAL, 10, 1.4))
    b.append(text(bx + 16, by + 30, "南中高度の求め方（北緯◯°の地点）", 16, TEAL_D, 700))
    for i, (nm, f) in enumerate([("春分・秋分", "90° − 緯度"), ("夏至", "90° − 緯度 ＋ 23.4°"), ("冬至", "90° − 緯度 − 23.4°")]):
        b.append(text(bx + 16, by + 66 + i * 30, nm, 17, INK, 700) + text(bx + 130, by + 66 + i * 30, f, 18, INK))
    # ---- 右：地点ごとの早見表 ----
    x0 = 836
    b.append(text(x0, 128, "地点ごとの南中高度", 17, INK, 700))
    rows = []
    for key in ("sapporo", "tokyo", "naha"):
        nm, la, lo = LOC[key]
        rows.append([f"{nm} {la:.1f}°", f"{90 - la:.1f}°", f"{90 - la + EPS:.1f}°", f"{90 - la - EPS:.1f}°"])
    rows.append(["赤道 0°", "90°", f"{180 - (90 + EPS):.1f}°北", f"{90 - EPS:.1f}°"])
    b.append(table(x0, 144, ["地点・緯度", "春秋分", "夏至", "冬至"], rows, [110, 70, 68, 68], 44, 15))
    b.append(text(x0, 384, "赤道の夏至は北の空に南中する", 14, MUTED))
    b.append(text(x0, 404, "（90°をこえたら 180° − その値）。", 14, MUTED))
    b.append(text(x0, 444, "例題", 16, TEAL_D, 700))
    b.append(lines(x0, 472, ["北緯34.0°の地点の冬至の日の", "南中高度は？",
                             f"90° − 34.0° − 23.4° ＝ {90 - 34.0 - 23.4:.1f}°"], 15.5, INK, gap=1.55))
    b.append(lines(x0, 566, ["春分の日の南中高度が50.0°の", f"地点の緯度は？ → 北緯{90 - 50.0:.1f}°"], 15.5, INK, gap=1.55))
    return svg("".join(b), "南中高度の求め方と季節による違い",
               "地軸の傾きは教科書どおり23.4°とした計算値（国立天文台の暦では2026年の夏至の東京は77.8°）。")


FIGS = [
    dict(svg=fig1, alt="透明半球に記録した東京の太陽の通り道の図。夏至・春分秋分・冬至の通り道と1時間ごとの位置、日の出・日の入りの位置を示し、季節ごとの南中高度（夏至77.7°・春分秋分54.3°・冬至30.9°）、昼の長さ、日の出・日の入りの方位の早見表を並べている。",
         caption="季節による太陽の通り道（東京）。通り道は南北に平行に移り、南中高度・昼の長さ・日の出の方位が変わる。"),
    dict(svg=fig2, alt="南中高度の求め方の図。地球の断面で春分・秋分の日の南中高度が90°−緯度になる理由と、東京の夏至・春分秋分・冬至の南中高度、求め方の式（夏至は＋23.4°、冬至は−23.4°）、札幌・東京・那覇・赤道の南中高度の早見表と例題。",
         caption="南中高度の求め方。春分・秋分は90°−緯度、夏至は23.4°高く、冬至は23.4°低い。"),
]
