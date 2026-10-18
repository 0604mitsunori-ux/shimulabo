"""ISSはいまどこ？（iss-doko）の図。ISSの軌道（高度約400km・約90分で1周）／ISSが見えるしくみと、距離ごとの見上げる高さ。
数値：地球の半径 6,371km・GM 398,600km³/s² から、高度400km の円軌道で 速さ 7.67km/s（時速約2万7,600km）・周期 92.4分・
1日に15.6周・1周のあいだに地球が 23.2° 自転（恒星日 86,164秒）。東京〜大阪 約400km はページ本文と同じ。
見上げる高さ：ページの距離 d＝√(地上の距離²＋高度²) を逆算し、球面の幾何で仰角を計算（高度400〜420km で 500km→51〜55°、
1,000km→19〜20°、1,500km→約9°、2,000km→約2〜3°）。ライブの位置には依存しない。"""
import math
from figlib import *

R, GM, H = 6371.0, 398600.4418, 400.0
A = R + H
V = math.sqrt(GM / A)                      # km/s
T = 2 * math.pi * math.sqrt(A ** 3 / GM)   # 秒
SHIFT = 360 * T / 86164.1                  # 1周のあいだに地球が回る角度


def elev(dist, h=H):
    """ページの距離（√(地上の距離²＋高度²)）から、見上げる高さ（仰角°）"""
    g = math.sqrt(max(0.0, dist * dist - h * h))
    if g == 0:
        return 90.0
    th = g / R
    return math.degrees(math.atan2(math.cos(th) - R / (R + h), math.sin(th)))


def man(n):
    """27600 → 2万7,600"""
    return f"{n // 10000}万{n % 10000:,}" if n >= 10000 else f"{n:,}"


def iss_icon(x, y, s=1.0, col=INK):
    return (rect(x - 5 * s, y - 4 * s, 10 * s, 8 * s, col, "none", 1, 0)
            + rect(x - 22 * s, y - 9 * s, 13 * s, 18 * s, "#4a78a8", col, 1, 1)
            + rect(x + 9 * s, y - 9 * s, 13 * s, 18 * s, "#4a78a8", col, 1, 1))


def fig1():
    b = []
    cx, cy, rE = 300, 372, 232
    k = rE / R
    rO = A * k
    b.append(circle(cx, cy, rE, "#cfe0c4", "#7d9a6c", 2))
    b.append(circle(cx, cy, rO, "none", ACC, 2.4))
    b.append(text(cx, cy - 10, "地球", 24, "#3f5a33", 700, "middle"))
    b.append(text(cx, cy + 20, "半径 約6,400km", 16, "#3f5a33", anchor="middle"))
    ang = math.radians(48)
    ix, iy = cx + rO * math.cos(ang), cy - rO * math.sin(ang)
    b.append(iss_icon(ix, iy, 0.9))
    a0, a1 = math.radians(30), math.radians(42)
    p0 = (cx + (rO + 16) * math.cos(a0), cy - (rO + 16) * math.sin(a0)); p1 = (cx + (rO + 16) * math.cos(a1), cy - (rO + 16) * math.sin(a1))
    b.append(f'<path d="M{p0[0]:.1f},{p0[1]:.1f} A{rO + 16:.1f},{rO + 16:.1f} 0 0 0 {p1[0]:.1f},{p1[1]:.1f}" fill="none" stroke="{ACC}" stroke-width="2.4" marker-end="url(#ah-acc)"/>')
    b.append(text(ix + 30, iy - 22, "ISS（印は大きくかいている）", 15, INK, 700))
    q = (cx + rO * math.cos(math.radians(140)), cy - rO * math.sin(math.radians(140)))
    b.append(line(q[0], q[1], 92, 140, ACC, 1.4))
    b.append(text(56, 128, "ISSの通り道（高度 約400km）", 15, ACC, 700))
    b.append(text(cx, cy + 70, "地球とISSの高さの比は", 15, "#3f5a33", anchor="middle"))
    b.append(text(cx, cy + 92, "実際と同じ", 15, "#3f5a33", anchor="middle"))
    # まん中：400km のものさし
    X, g0, top = 620, 560, 200                 # 1px＝(g0-top)/400 km
    sc = (g0 - top) / H
    b.append(text(X - 14, 128, "地上から400kmを拡大すると", 17, INK, 700))
    b.append(f'<rect x="{X}" y="{top - 6}" width="70" height="{g0 - top + 6}" fill="#eef3f6"/>')
    b.append(rect(X - 6, g0, 82, 16, "#cfe0c4", "#7d9a6c", 0, 1.2))
    b.append(line(X - 6, top, X + 80, top, ACC, 2, "6 4"))
    b.append(iss_icon(X + 35, top - 2, 0.8))
    b.append(line(X - 12, g0, X - 12, top + 4, INK, 1.6, arrow="ink") + line(X - 12, top, X - 12, g0 - 4, INK, 1.6, arrow="ink"))
    b.append(text(X + 35, (g0 + top) / 2 + 6, "400km", 17, INK, 700, "middle"))
    b.append(text(X + 92, top + 6, "ISS 約400km", 16, ACC, 700))
    for km, lab in [(10, "飛行機 約10km"), (3.776, "富士山 3.8km")]:
        y = g0 - km * sc
        b.append(line(X, y, X + 70, y, INK2, 1.4))
    b.append(text(X + 92, g0 - 10 * sc - 4, "飛行機 約10km", 15, INK))
    b.append(text(X + 92, g0 - 10 * sc + 16, "富士山 3.8km", 15, INK))
    # 東京〜大阪を横に
    b.append(text(X + 92, 330, "東京〜大阪の", 15, INK2))
    b.append(text(X + 92, 352, "直線距離（約400km）", 15, INK2))
    b.append(text(X + 92, 374, "と同じくらいの高さ", 15, INK2))
    # 右：数字
    XR = 868
    rows = [("高さ", "約400km", "地上から"),
            ("速さ", f"秒速 約{V:.1f}km", f"時速 約{man(int(round(V * 3600, -2)))}km"),
            ("1周", f"約{T / 60:.0f}分", "（約90分）"),
            ("1日に", f"約{86400 / T:.1f}周", "ISSでは1日に16回ほど日の出"),
            ("1周ごとに", f"西へ約{SHIFT:.0f}°ずれる", "その間に地球が自転するため")]
    y = 112
    for k_, v, sub in rows:
        b.append(rect(XR, y, 284, 92, CARD, LINE, 10))
        b.append(text(XR + 16, y + 28, k_, 15, INK2, 700))
        b.append(text(XR + 16, y + 60, v, 23, ACC, 700))
        b.append(text(XR + 16, y + 82, sub, 14, INK2))
        y += 100
    return svg("".join(b), "ISSの軌道（高度 約400km・約90分で地球1周）",
               f"高度400kmの円軌道として計算（実際の高度は日によって少し変わる）。東京〜大阪を約{400 / V:.0f}秒で飛ぶ速さ。")


def fig2():
    b = []
    cx, cy, r = 340, 342, 160
    rO = 222                                       # 見やすくするため高さを大きくかいている
    pos = lambda rr, deg: (cx + rr * math.cos(math.radians(deg)), cy - rr * math.sin(math.radians(deg)))
    # 太陽の光と地球の影（北極の上から見て反時計回りに自転：上が日の出、下が日の入りの側）
    b.append(text(56, 124, "太陽の光", 16, GOLD, 700))
    for y in range(150, 620, 52):
        b.append(arrow(52, y, 112, y, "gold", 2.2))
    b.append(f'<rect x="{cx}" y="{cy - r}" width="{650 - cx}" height="{2 * r}" fill="#3a4656" opacity=".16"/>')
    b.append(text(600, cy - 60, "地球の影", 16, INK2, 700, "middle"))
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{rO}" fill="none" stroke="{MUTED}" stroke-width="1.4" stroke-dasharray="6 5"/>')
    b.append(circle(cx, cy, r, "#d3e6f1", "#5f8fae", 1.8))
    b.append(f'<path d="M{cx},{cy - r} A{r},{r} 0 0 1 {cx},{cy + r}Z" fill="#33495e"/>')
    b.append(text(cx - 64, cy + 6, "昼", 20, TEAL_D, 700, "middle"))
    b.append(text(cx + 64, cy + 6, "夜", 20, "#fff", 700, "middle"))
    p0, p1 = pos(r - 26, 120), pos(r - 26, 150)
    b.append(f'<path d="M{p0[0]:.1f},{p0[1]:.1f} A{r - 26},{r - 26} 0 0 0 {p1[0]:.1f},{p1[1]:.1f}" fill="none" stroke="{INK}" stroke-width="2.2" marker-end="url(#ah-ink)"/>')
    b.append(text(cx - 60, cy - 70, "自転", 15, INK, 700, "middle"))
    b.append(text(cx - 8, cy - r + 30, "日の出のころ", 14, TEAL_D, 700, "end"))
    b.append(text(cx - 8, cy + r - 18, "日の入りのころ", 14, TEAL_D, 700, "end"))
    # 日没後の人と、日の当たるISS
    ox, oy = pos(r, 284)
    ix, iy = pos(rO, 262)
    b.append(line(ox, oy, ix, iy, ACC, 1.8, "5 4"))
    b.append(circle(ox, oy, 6, INK, "#fff", 1.4))
    b.append(circle(ix, iy, 28, "none", SUN, 3))
    b.append(iss_icon(ix, iy, 0.8))
    b.append(text(ix - 36, iy + 6, "日が当たって光るISS", 15, ACC, 700, "end"))
    b.append(text(ox + 14, oy - 8, "日没後の人", 15, INK, 700))
    b.append(text(ox + 14, oy + 12, "（空は暗い）", 14, INK))
    # 夜おそく：影の中
    jx, jy = pos(rO, 338)
    b.append(iss_icon(jx, jy, 0.8, MUTED))
    b.append(text(jx + 26, jy - 14, "夜おそくは", 15, INK2, 700))
    b.append(text(jx + 26, jy + 6, "影の中で見えない", 15, INK2, 700))
    b.append(text(cx + 40, 616, "北極の上から見た模式図（ISSの高さは大きくかいている）", 14, MUTED, anchor="middle"))
    # 右：距離と見上げる高さ
    X = 700
    b.append(text(X, 128, "ページの距離と、見上げる高さ（目安）", 18, INK, 700))
    rows = []
    for d in (500, 1000, 1500, 2000):
        e = elev(d)
        e5 = 5 * round(e / 5)
        rows.append([f"{d:,}km", "ほぼ地平線" if e < 5 else f"約{e5:.0f}°", "高い空" if e >= 40 else "見やすい" if e >= 15 else "建物や山にかくれやすい" if e >= 5 else "見えにくい"])
    b.append(table(X, 146, ["ISSまでの距離", "見上げる高さ", "見え方"], rows, [140, 120, 192], 48, 16))
    b.append(lines(X, 420, ["見えるのは、日の出前・日没後の暗い空で、", "ISSに太陽の光が当たっているとき。", "飛行機より速く、数分かけて空を横切る。"], 16, INK, 1.55))
    b.append(text(X, 534, "見上げる高さ＝地平線から何度の高さか（真上＝90°）", 14, INK2))
    b.append(text(X, 558, "見える日時はJAXA「#きぼうを見よう」で調べられる", 14, INK2))
    return svg("".join(b), "ISSが見えるしくみと、見上げる高さ",
               "距離はこのページの表示（ISSまでの直線距離）。高度400kmとして計算した目安で、天気や明るさでも変わる。")


FIGS = [
    dict(svg=fig1, alt="ISS（国際宇宙ステーション）の軌道の図。半径約6,400kmの地球と高度約400kmのISSの通り道を同じ縮尺で描き、400kmは東京〜大阪の直線距離と同じくらいであること、秒速約7.7km（時速約2万7,600km）、約92分（約90分）で地球を1周し、1日に約15.6周、1周ごとに通る場所が西へ約23°ずれることをまとめている。",
         caption="ISSの軌道。高度約400kmを秒速約7.7kmで飛び、約90分で地球を1周する。"),
    dict(svg=fig2, alt="ISSが見えるしくみの図。日没後や日の出前、地上の人は暗い空の下にいるが、上空のISSには太陽の光が当たっているため明るく光って見える。真夜中はISSも地球の影に入るので見えない。ページに出るISSまでの距離（500km・1,000km・1,500km・2,000km）ごとの見上げる高さの目安の表もつけている。",
         caption="ISSが見えるしくみ。日没後・日の出前の暗い空で、ISSに日が当たっているときに見える。"),
]
