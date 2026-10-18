"""昼の長さメーター（hiruma-nagasa）の図。季節で昼の長さが変わるしくみ（地軸の傾き）／1年の昼の長さ（札幌・東京・那覇）。
数値：日の出・日の入り＝太陽の中心が高度 −0.833°（大気の屈折と太陽の半径の分）になる時刻、赤緯は NOAA の近似式で 2026年の日ごとに計算。
ページの Open-Meteo（daylight_duration）とは1〜2分ちがうことがある（10/18〜20 の東京で 1.6分短い）。
地点の緯度経度はページの PREFS（札幌 43.06・東京 35.69・那覇 26.21）。夏至 6/21・冬至 12/22・春分 3/20・秋分 9/23（2026年）。"""
import datetime
import math
from figlib import *

EPS = 23.44
CITIES = [("札幌", 43.06, GOLD, "10 6"), ("東京", 35.69, TEAL, None), ("那覇", 26.21, ACC, "3 5")]


def decl(doy):
    g = 2 * math.pi / 365 * (doy - 1)
    return (0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g) - 0.006758 * math.cos(2 * g)
            + 0.000907 * math.sin(2 * g) - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g))


def daylen(lat, doy):
    """昼の長さ（時間）"""
    d, p = decl(doy), math.radians(lat)
    c = (math.sin(math.radians(-0.833)) - math.sin(p) * math.sin(d)) / (math.cos(p) * math.cos(d))
    return 2 * math.degrees(math.acos(max(-1, min(1, c)))) / 15


def doy(m, d):
    return datetime.date(2026, m, d).timetuple().tm_yday


def hm5(h):
    """5分単位に丸めた「約○時間○分」"""
    m = int(5 * round(h * 60 / 5))
    return f"約{m // 60}時間" + (f"{m % 60}分" if m % 60 else "")


def earth(cx, cy, r, tilt, lat=35.69):
    """横から見た地球。tilt：北極が太陽（左）の側に傾く角度（夏至 +23.4、冬至 −23.4、春分・秋分 0）"""
    t = math.radians(tilt)
    a = (-math.sin(t), -math.cos(t))            # 北極の向き（単位ベクトル）
    u = (math.cos(t), -math.sin(t))             # 地軸に直角で、太陽と反対の側
    out = [circle(cx, cy, r, "#d3e6f1", "#5f8fae", 1.8),
           f'<path d="M{cx},{cy - r} A{r},{r} 0 0 1 {cx},{cy + r}Z" fill="#33495e"/>',
           circle(cx, cy, r, "none", "#5f8fae", 1.8)]
    # 地軸
    out.append(line(cx - a[0] * (r + 30), cy - a[1] * (r + 30), cx + a[0] * (r + 34), cy + a[1] * (r + 34), INK, 2))
    out.append(circle(cx + a[0] * r, cy + a[1] * r, 4, INK, INK, 0))
    out.append(text(cx + a[0] * (r + 46), cy + a[1] * (r + 46) + 5, "北極", 14, INK, 700, "middle"))
    # 緯線（赤道と東京の緯度）：t＝0 が真夜中。昼は x が太陽の側（左）になる t
    def ring(phi, day_col, night_col, w):
        p = math.radians(phi)
        cc = (cx + a[0] * r * math.sin(p), cy + a[1] * r * math.sin(p))
        rr, k = r * math.cos(p), 0.2
        pts = []
        for i in range(0, 361, 3):
            tt = math.radians(i)
            x = cc[0] + rr * math.cos(tt) * u[0]                 # 奥行きは縦にだけずらす（昼夜の境目が明暗の境目と一致する）
            y = cc[1] + rr * (math.cos(tt) * u[1] - k * math.sin(tt))
            day = (cc[0] - cx) + rr * math.cos(tt) * u[0] < 0
            pts.append((x, y, day))
        segs, cur = [], [pts[0]]
        for q in pts[1:]:
            if q[2] == cur[-1][2]:
                cur.append(q)
            else:
                cur.append(q); segs.append(cur); cur = [q]
        segs.append(cur)
        res = []
        for sg in segs:
            res.append(poly([(x, y) for x, y, _ in sg], day_col if sg[0][2] else night_col, w, dash=None if sg[0][2] else "5 4"))
        frac = sum(1 for x, y, d in pts[:-1] if d) / (len(pts) - 1)
        return "".join(res), frac
    eq, _ = ring(0, "#7b8f9e", "#8fa3b3", 1.4)
    tk, frac = ring(lat, GOLD, "#d9c690", 4)
    out.append(eq)
    out.append(tk)
    return "".join(out), frac


def fig1():
    b = [text(56, 122, "太陽の光", 16, GOLD, 700)]
    panels = [("夏至（6月21日ごろ）", 23.44, (6, 21), "北半球が太陽の側に傾く"),
              ("春分・秋分（3月20日・9月23日ごろ）", 0, (3, 20), "どちらにも傾かない"),
              ("冬至（12月22日ごろ）", -23.44, (12, 22), "北半球が太陽と反対に傾く")]
    for i, (ttl, tilt, md, sub) in enumerate(panels):
        x0 = 48 + i * 370
        cx, cy, r = x0 + 205, 352, 104
        for y in (300, 352, 404):
            b.append(arrow(x0 + 6, y, x0 + 64, y, "gold", 2.2))
        g, frac = earth(cx, cy, r, tilt)
        b.append(g)
        b.append(text(x0 + 184, 152, ttl, 17 if i != 1 else 15.5, INK, 700, "middle"))
        h = daylen(35.69, doy(*md))
        if i == 1:
            lab = "東京の昼 約12時間"
        else:
            lab = "東京の昼 " + hm5(h)
        b.append(text(x0 + 184, 520, lab, 19, TEAL_D, 700, "middle"))
        b.append(text(x0 + 184, 546, sub, 15, INK2, anchor="middle"))
        b.append(text(x0 + 184, 570, "昼と夜がほぼ同じ" if i == 1 else ("昼が長い" if tilt > 0 else "昼が短い"), 15, INK2, anchor="middle"))
        if i == 0:
            t = math.radians(tilt); ra = r + 30
            b.append(line(cx, cy - r - 44, cx, cy - r + 2, INK2, 1.4, "4 4"))
            b.append(f'<path d="M{cx},{cy - ra} A{ra},{ra} 0 0 0 {cx - ra * math.sin(t):.1f},{cy - ra * math.cos(t):.1f}" fill="none" stroke="{ACC}" stroke-width="2"/>')
            b.append(text(cx + 8, cy - r - 24, f"{EPS:.1f}°", 15, ACC, 700))
            b.append(text(cx + (r + 40) * math.sin(t) + 8, cy + (r + 40) * math.cos(t) + 4, "地軸", 14, INK, 700))
    # 凡例
    b.append(line(80, 604, 120, 604, GOLD, 4) + text(128, 609, "東京の緯度（北緯35.7°）を1日で回る道の、昼の部分", 15, INK))
    b.append(line(560, 604, 600, 604, "#d9c690", 4, "5 4") + text(608, 609, "夜の部分", 15, INK))
    b.append(f'<rect x="720" y="594" width="22" height="18" fill="#33495e"/>' + text(750, 609, "夜の側", 15, INK))
    b.append(f'<rect x="830" y="594" width="22" height="18" fill="#d3e6f1" stroke="#5f8fae"/>' + text(860, 609, "昼の側", 15, INK))
    return svg("".join(b), "季節で昼の長さが変わるしくみ（地軸の傾き）",
               "横から見た模式図。地軸が傾いたまま太陽のまわりを回るので、夏は北半球の昼の部分が長くなる。")


def fig2():
    b = []
    X0, Y0, Wd, Hd = 104, 560, 860, 400
    hmin, hmax = 8, 16
    px = lambda d: X0 + (d - 1) / 364 * Wd
    py = lambda h: Y0 - (h - hmin) / (hmax - hmin) * Hd
    months = [(doy(m, 1), f"{m}月") for m in range(1, 13)]
    b.append(axes(X0, Y0, Wd, Hd, "", "", [(px(d) - X0, lab) for d, lab in months],
                  [(Y0 - py(h), f"{h}時間") for h in range(hmin, hmax + 1)], 14))
    for nm, dd, lab in [("春分", doy(3, 20), "春分"), ("夏至", doy(6, 21), "夏至"), ("秋分", doy(9, 23), "秋分"), ("冬至", doy(12, 22), "冬至")]:
        b.append(line(px(dd), Y0, px(dd), Y0 - Hd, INK2, 1.4, "5 5"))
        b.append(text(px(dd), Y0 - Hd - 12, lab, 15, INK, 700, "middle"))
    for nm, lat, col, dash in CITIES:
        pts = [(px(d), py(daylen(lat, d))) for d in range(1, 366)]
        b.append(poly(pts, col, 3.6 if nm == "東京" else 2.8, dash=dash))
        b.append(text(X0 + Wd + 14, py(daylen(lat, 365)) + 6, nm, 17, col, 700))
    # 夏至・冬至の値（下地つきのラベル）
    def lab(x, y, s, col, anc="start", size=15):
        w = sum(size * (0.58 if ch.isascii() else 1.0) for ch in s) + 10
        x0 = x - 5 if anc == "start" else x - w + 5
        return f'<rect x="{x0:.1f}" y="{y - size - 2:.1f}" width="{w:.1f}" height="{size + 9}" rx="3" fill="{BG}" opacity=".92"/>' + text(x, y, s, size, col, 700, anc)
    ds, dw = doy(6, 21), doy(12, 22)
    ts, tw = daylen(35.69, ds), daylen(35.69, dw)
    sap, nah = daylen(43.06, ds), daylen(26.21, ds)
    for d, h, col in [(ds, sap, GOLD), (ds, ts, TEAL), (ds, nah, ACC), (dw, tw, TEAL)]:
        b.append(circle(px(d), py(h), 5, col, "#fff", 1.4))
    b.append(lab(px(ds) - 10, py(sap) - 10, "札幌 " + hm5(sap), "#7a5512", "end"))
    b.append(lab(px(ds) + 10, py(ts) + 26, "東京 " + hm5(ts), TEAL_D))
    b.append(lab(px(ds) - 10, py(nah) + 26, "那覇 " + hm5(nah), ACC, "end"))
    b.append(lab(px(dw) - 10, py(tw) + 28, "東京 " + hm5(tw), TEAL_D, "end"))
    # 変わる速さ（東京）
    rate = max(abs(daylen(35.69, d + 1) - daylen(35.69, d)) for d in range(1, 364)) * 60
    bx, by = 690, 172
    b.append(rect(bx, by, 292, 84, CARD, LINE, 8))
    b.append(text(bx + 16, by + 28, "春分・秋分のころは毎日大きく変わる", 15, INK, 700))
    b.append(text(bx + 16, by + 54, f"東京で1日に約{int(rate)}分{round((rate % 1) * 60):02d}秒", 15, INK))
    b.append(text(bx + 16, by + 74, "夏至・冬至のころはほとんど変わらない", 14, INK2))
    return svg("".join(b), "1年の昼の長さ（札幌・東京・那覇）",
               "昼の長さ＝日の出から日の入りまで。天文計算の目安で、このページ（Open-Meteo）の値と1〜2分ちがうことがある。")


FIGS = [
    dict(svg=fig1, alt="季節で昼の長さが変わるしくみの図。地軸が23.4°傾いたまま地球が太陽のまわりを回るため、夏至は北半球が太陽の側に傾いて東京の昼は約14時間35分、春分・秋分は約12時間、冬至は太陽と反対に傾いて約9時間45分になることを、横から見た地球と東京の緯度の昼と夜の部分で示している。",
         caption="季節で昼の長さが変わるしくみ。地軸の傾きで、夏は北半球の昼の部分が長く、冬は短くなる。"),
    dict(svg=fig2, alt="札幌・東京・那覇の1年間の昼の長さ（日の出から日の入りまで）のグラフ。夏至に最も長く（札幌約15時間20分・東京約14時間35分・那覇約13時間45分）、冬至に最も短い（東京約9時間45分）。春分・秋分のころは東京で1日に約2分ずつ変わる。",
         caption="1年の昼の長さ。北の地域ほど夏と冬の差が大きく、春分・秋分のころに毎日いちばん大きく変わる。"),
]
