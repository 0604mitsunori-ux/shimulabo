"""エラトステネスの方法（eratosthenes）の授業用の図
   ページ（scripts/rika/sims_kou_chigaku.py）と同じ計算：地球一周 L＝d×360÷θ（925 km×360÷7.2＝46,250 km）、
   影の長さ＝100 cm×tanθ、日本の2都市は都道府県庁の緯度経度（同じ値）から、GRS80 の子午線弧長（シンプソン則）と
   Vincenty の式で南北の距離・2地点間の距離を計算。実際の子午線の一周 40,008 km（4×子午線弧長(90°)）。"""
import math
from figlib import *

GA, GF = 6378137.0, 1 / 298.257222101
GB, GE2 = GA * (1 - GF), GF * (2 - GF)


def merid(p, n=4000):
    h = math.radians(p) / n; s = 0.0
    for i in range(n + 1):
        q = h * i; w = 1 if i in (0, n) else (4 if i % 2 else 2)
        s += w * GA * (1 - GE2) / (1 - GE2 * math.sin(q) ** 2) ** 1.5
    return s * h / 3


def vincenty(l1, o1, l2, o2):
    L = math.radians(o2 - o1); U1 = math.atan((1 - GF) * math.tan(math.radians(l1))); U2 = math.atan((1 - GF) * math.tan(math.radians(l2)))
    lam = L
    for _ in range(200):
        sl, cl = math.sin(lam), math.cos(lam)
        ss = math.hypot(math.cos(U2) * sl, math.cos(U1) * math.sin(U2) - math.sin(U1) * math.cos(U2) * cl)
        cs = math.sin(U1) * math.sin(U2) + math.cos(U1) * math.cos(U2) * cl
        sg = math.atan2(ss, cs); sa = math.cos(U1) * math.cos(U2) * sl / ss; c2a = 1 - sa * sa
        c2m = cs - 2 * math.sin(U1) * math.sin(U2) / c2a
        C = GF / 16 * c2a * (4 + GF * (4 - 3 * c2a)); lp = lam
        lam = L + (1 - C) * GF * sa * (sg + C * ss * (c2m + C * cs * (-1 + 2 * c2m * c2m)))
        if abs(lam - lp) < 1e-13: break
    u2 = c2a * (GA * GA - GB * GB) / (GB * GB)
    Aa = 1 + u2 / 16384 * (4096 + u2 * (-768 + u2 * (320 - 175 * u2))); Bb = u2 / 1024 * (256 + u2 * (-128 + u2 * (74 - 47 * u2)))
    ds = Bb * ss * (c2m + Bb / 4 * (cs * (-1 + 2 * c2m * c2m) - Bb / 6 * c2m * (-3 + 4 * ss * ss) * (-3 + 4 * c2m * c2m)))
    return GB * Aa * (sg - ds)


MERID_CIRC = 4 * merid(90) / 1000
CITY = {"札幌": (43.0643, 141.3469), "青森": (40.8246, 140.7405), "仙台": (38.2686, 140.8721), "水戸": (36.3417, 140.4468),
        "新潟": (37.9025, 139.0232), "前橋": (36.3907, 139.0605), "福岡": (33.6064, 130.4180), "鹿児島": (31.5602, 130.5580),
        "松江": (35.4723, 133.0505), "高知": (33.5597, 133.5311), "那覇": (26.2124, 127.6809)}
PAIR_KEYS = [("青森", "仙台"), ("青森", "水戸"), ("札幌", "水戸"), ("新潟", "前橋"), ("福岡", "鹿児島"), ("松江", "高知"), ("札幌", "那覇")]
TH, DK = 7.2, 925


def pairs():
    out = []
    for a, b_ in PAIR_KEYS:
        (l1, o1), (l2, o2) = CITY[a], CITY[b_]
        ns = round(abs(merid(l1) - merid(l2)) / 1000, 1); geo = round(vincenty(l1, o1, l2, o2) / 1000, 1)
        out.append((a, b_, l1 - l2, abs(o1 - o2), ns, geo))
    return out


def comma(v): return "{:,}".format(int(round(v)))


def fig1():
    b = []
    O = (120, 520); R = 400; TD = 24                          # 中心角は見やすく大きくかく（実際は7.2°）
    P = lambda a, r=R: (O[0] + r * math.cos(math.radians(a)), O[1] - r * math.sin(math.radians(a)))
    b.append(text(48, 128, "地球の断面（夏至の日の正午）", 18, INK, 700))
    a0, a1 = -6, 52
    p0, p1 = P(a0), P(a1)
    b.append(f'<path d="M{O[0]},{O[1]} L{p0[0]:.1f},{p0[1]:.1f} A{R},{R} 0 0 0 {p1[0]:.1f},{p1[1]:.1f}Z" fill="#dbeafe" stroke="{TEAL}" stroke-width="2"/>')
    S, A = P(0), P(TD)
    # 太陽の光（平行）
    for y in (236, 400, 450, 486, S[1]):
        xs = O[0] + math.sqrt(R * R - (y - O[1]) ** 2)
        b.append(arrow(800, y, (S[0] + 70) if y == S[1] else xs + 6, y, "gold", 2))
    b.append(text(800, 220, "太陽の光（平行）", 15, GOLD, 700, "end"))
    # 中心から2地点へ
    b.append(line(O[0], O[1], S[0] + 70, S[1], INK2, 1.4, "6 4"))
    T = P(TD, R + 64)
    b.append(line(O[0], O[1], T[0], T[1], INK2, 1.4, "6 4"))
    rr_ = 70
    b.append(f'<path d="M{O[0] + rr_},{O[1]} A{rr_},{rr_} 0 0 0 {P(TD, rr_)[0]:.1f},{P(TD, rr_)[1]:.1f}" fill="none" stroke="{ACC}" stroke-width="2.4"/>')
    b.append(text(O[0] + 84, O[1] - 14, "θ", 20, ACC, 700) + text(O[0] + 20, O[1] + 30, "地球の中心", 15, INK2))
    b.append(circle(O[0], O[1], 4, INK, INK, 0))
    # 2地点の間の弧
    b.append(f'<path d="M{S[0]:.1f},{S[1]:.1f} A{R},{R} 0 0 0 {A[0]:.1f},{A[1]:.1f}" fill="none" stroke="{ACC}" stroke-width="5"/>')
    M = P(TD / 2, R - 18); b.append(text(M[0] - 6, M[1] + 6, f"{DK} km", 17, ACC, 700, "end"))
    # シエネ：棒は太陽の方を向く（影なし）、井戸
    b.append(line(S[0], S[1], S[0] + 64, S[1], "#2563eb", 4) + circle(S[0], S[1], 4, "#2563eb", "#2563eb", 0))
    b.append(text(S[0] + 6, S[1] + 30, "シエネ", 17, "#2563eb", 700) + text(S[0] + 6, S[1] + 50, "影ができない", 14, "#2563eb"))
    # アレクサンドリア：棒と影
    Tp = P(TD, R + 64)
    b.append(line(A[0], A[1], Tp[0], Tp[1], ACC, 4) + circle(A[0], A[1], 4, ACC, ACC, 0))
    # 棒の先を通る光と影の先
    yT = Tp[1]; xsh = O[0] + math.sqrt(R * R - (yT - O[1]) ** 2)
    b.append(arrow(800, yT, Tp[0] + 2, yT, "gold", 2.4) + line(Tp[0], yT, xsh, yT, GOLD, 2, "4 3"))
    b.append(line(A[0], A[1], xsh, yT, INK, 5))
    r2 = 34; d1 = math.radians(180 + TD)                         # 棒の先での角（棒の向き → 光の向き）
    b.append(f'<path d="M{Tp[0] + r2 * math.cos(d1):.1f},{Tp[1] - r2 * math.sin(d1):.1f} A{r2},{r2} 0 0 0 {Tp[0] - r2:.1f},{Tp[1]:.1f}" fill="none" stroke="{ACC}" stroke-width="2.4"/>')
    b.append(text(Tp[0] - 52, Tp[1] - 8, "θ", 20, ACC, 700, "middle"))
    b.append(text(Tp[0] + 8, Tp[1] - 40, "アレクサンドリア", 17, ACC, 700) + text(Tp[0] + 8, Tp[1] - 20, "棒の影ができる", 14, ACC))
    b.append(lines(48, 588, ["光は平行なので、棒と光の角θ（錯角）＝ 地球の中心角θ。", f"角度は大きくかいた（実際は{TH}°）。棒の長さも誇張。"], 14.5, INK2, gap=1.45))
    # 右：拡大図と式
    x0 = 840
    def zoom(y0, name, z, col, well):
        out = [rect(x0, y0, 312, 150, CARD, LINE, 10)]
        gy, rx, Hr = y0 + 128, x0 + 236, 84
        out.append(line(x0 + 10, gy, x0 + 302, gy, "#78716c", 2))
        if well:
            out.append(f'<rect x="{rx - 52}" y="{gy}" width="20" height="16" fill="#1e3a8a"/>' + line(rx - 42, y0 + 34, rx - 42, gy + 12, GOLD, 1.6))
        for k in (-1, 1, 2):
            ex = rx + k * 26; L = (gy - (y0 + 30)) / math.cos(math.radians(z))
            out.append(arrow(ex + math.sin(math.radians(z)) * L, gy - math.cos(math.radians(z)) * L, ex, gy, "gold", 1.4))   # 光は右上から（ページの拡大図と同じ向き）
        sh = Hr * math.tan(math.radians(z))
        if sh > 0.5: out.append(line(rx, gy, rx - sh, gy, INK, 5))
        out.append(line(rx, gy, rx, gy - Hr, col, 4))
        if z > 0.3:
            out.append(line(rx, gy - Hr, rx, gy - Hr - 34, col, 1.2, "3 3"))
            a_ = math.radians(90 - z); r3 = 30                     # 棒をのばした線と、太陽の方向（右上）の間の角
            tl = (gy - Hr - (y0 + 30)) / math.cos(math.radians(z))
            out.append(line(rx, gy - Hr, rx + math.sin(math.radians(z)) * tl, y0 + 30, GOLD, 1.6, "4 3"))
            out.append(f'<path d="M{rx},{gy - Hr - r3} A{r3},{r3} 0 0 1 {rx + r3 * math.cos(a_):.1f},{gy - Hr - r3 * math.sin(a_):.1f}" fill="none" stroke="{ACC}" stroke-width="2"/>')
            out.append(text(rx + 16, gy - Hr - 30, f"{z}°", 16, ACC, 700))
        out.append(text(x0 + 12, y0 + 26, name, 16, col, 700))
        return "".join(out)
    b.append(zoom(112, "シエネ：太陽が真上", 0, "#2563eb", True))
    b.append(text(x0 + 12, 112 + 50, "井戸の底まで光が届く", 14, INK2) + text(x0 + 12, 112 + 70, "影ができない", 14, INK2))
    b.append(zoom(274, "アレクサンドリア", TH, ACC, False))
    b.append(text(x0 + 12, 274 + 50, f"高さ1 mの棒の影", 14, INK2) + text(x0 + 12, 274 + 70, f"＝ {100 * math.tan(math.radians(TH)):.1f} cm", 14, INK2))
    b.append(text(x0 + 12, 274 + 92, f"tan θ ＝ {math.tan(math.radians(TH)):.3f}", 14, INK2))
    L = DK * 360 / TH
    b.append(rect(x0, 438, 312, 176, TEAL_L, TEAL, 10, 1.4))
    b.append(text(x0 + 14, 466, f"360° : {TH}° ＝ 地球一周 : {DK} km", 16, INK, 700))
    b.append(text(x0 + 14, 496, f"地球一周 ＝ {DK} × 360 ÷ {TH}", 16, INK))
    b.append(text(x0 + 14, 534, f"＝ {comma(L)} km", 26, TEAL_D, 700))
    b.append(text(x0 + 14, 566, f"実際（子午線の一周）{comma(MERID_CIRC)} km", 14.5, INK2))
    b.append(text(x0 + 14, 588, f"との差 +{(L / MERID_CIRC - 1) * 100:.0f}%（925 kmは5,000スタディア）", 14, INK2))
    return svg("".join(b), "エラトステネスの方法（地球の大きさの求め方）",
               "太陽の光は平行なので、影から測った角度が地球の中心角になる。2地点の距離から地球一周がわかる。")


def fig2():
    b = []
    # 式
    b.append(rect(48, 112, 560, 128, TEAL_L, TEAL, 10, 1.4))
    b.append(text(64, 140, "地球一周を求める式", 17, TEAL_D, 700))
    b.append(text(64, 172, "360° : θ ＝ 地球一周 L : 2地点の距離 d", 18, INK, 700))
    b.append(text(64, 202, "L ＝ d × 360° ÷ θ　　地球の半径 ＝ L ÷ 2π", 17, INK))
    b.append(text(64, 228, "θ：影の角度（棒と光の角）＝ 2地点の緯度の差", 15, INK2))
    b.append(rect(624, 112, 528, 128, CARD, LINE, 10))
    b.append(text(640, 140, "影の長さから角度を求める", 17, INK, 700))
    b.append(text(640, 172, "tan θ ＝ 影の長さ ÷ 棒の高さ", 18, INK, 700))
    b.append(text(640, 202, f"例：1 mの棒の影が{100 * math.tan(math.radians(TH)):.1f} cm → tanθ＝{math.tan(math.radians(TH)):.3f}", 16, INK))
    b.append(text(640, 228, f"→ θ ≒ {TH}°（下の表で読む）", 16, INK))
    # tan の早見表（横長）
    degs = (5, 7.2, 10, 20, 30, 35, 40, 45)
    fmt = lambda d: ("%.1f" % d if d != int(d) else "%d" % d) + "°"
    b.append(table(48, 256, ["棒と光の角θ"] + [fmt(d) for d in degs],
                   [["tan θ"] + ["%.3f" % math.tan(math.radians(d)) for d in degs],
                    ["1 mの棒の影"] + ["%.1f cm" % (100 * math.tan(math.radians(d))) for d in degs]],
                   [160] + [118] * 8, 33, 15.5))
    # 日本の2都市
    b.append(text(48, 384, "日本の2都市（都道府県庁）で計算した地球一周", 17, INK, 700))
    rows = []
    for a, b_, dphi, dlon, ns, geo in pairs():
        rows.append([f"{a}—{b_}", "%.3f°" % dphi, "%.2f°" % dlon, "%.1f km" % ns, "%.1f km" % geo,
                     comma(ns * 360 / dphi) + " km", comma(geo * 360 / dphi) + " km"])
    b.append(table(48, 394, ["2地点", "緯度の差", "経度の差", "南北の距離", "2地点間の距離", "一周（南北の距離で）", "一周（2地点間で）"],
                   rows, [150, 120, 110, 150, 160, 210, 204], 28, 15))
    return svg("".join(b), "地球一周の求め方と日本の2都市での計算",
               "南北の距離（子午線にそった長さ）を使うと約40,000 km。東西にずれた2地点の直線距離を使うと大きく出る。")


FIGS = [
    dict(svg=fig1, alt="エラトステネスの方法の図。夏至の日の正午、シエネでは太陽が真上で影ができず、アレクサンドリアでは棒と光の角が7.2°。太陽の光は平行なので、この角は地球の中心角に等しく、360°:7.2°＝地球一周:925 kmから地球一周46,250 kmが求められる。",
         caption="エラトステネスの方法。影から測った角度が、地球の中心角になる。"),
    dict(svg=fig2, alt="地球一周を求める式（360°:θ＝L:d、L＝d×360÷θ）と、影の長さから角度を求める tan の早見表、日本の2都市（都道府県庁）の緯度の差・南北の距離・2地点間の距離から計算した地球一周の表（南北の距離では約40,000 km）。",
         caption="地球一周の求め方の早見表。南北の距離を使うと、どの組み合わせでも約40,000 kmになる。"),
]
