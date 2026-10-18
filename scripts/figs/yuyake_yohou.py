"""今日の夕焼け予報（yuyake-yohou）の図。夕焼けが赤いしくみ（光の散乱）／焼け度の決まり（ページの判定）。
数値の正：ページの JS（日没時の雲量 ≦5→55点・≦15→70・≦40→88・≦65→74・≦85→40・それ以上→15、
ベスト観賞タイム＝日の入りの5〜20分後）。道のり約38倍＝地平線の太陽の大気路程（Kasten-Young 式で37.9）、
青は赤の約6倍＝レイリー散乱 (700/450)^4＝5.9。"""
import math
from figlib import *

BLUE = "#3f7fc0"
YAKE = [("0〜5%", "快晴", 55, "快晴。焼けるけど、ちょっと平凡かも"),
        ("6〜15%", "", 70, "きれいなグラデーション日和"),
        ("16〜40%", "", 88, "燃える空の予感！カメラの準備を"),
        ("41〜65%", "", 74, "雲の切れ間しだいで大当たりも"),
        ("66〜85%", "", 40, "雲多め。ドラマチック狙いならワンチャン"),
        ("86〜100%", "", 15, "今日は厚い雲の向こう…")]


def score(cloud):
    """ページの JS と同じ判定（雲量％→焼け度）"""
    return 55 if cloud <= 5 else 70 if cloud <= 15 else 88 if cloud <= 40 else 74 if cloud <= 65 else 40 if cloud <= 85 else 15


def person(x, y, nx, ny, color=INK):
    """地面の点 (x,y) に、法線 (nx,ny) の向きに立つ人"""
    hx, hy = x + nx * 26, y + ny * 26
    return line(x, y, hx, hy, color, 3) + circle(x + nx * 33, y + ny * 33, 7, color, color, 0)


def fig1():
    C, R, RA = (440, 680), 250, 315
    be = math.radians(25)
    s = (-math.cos(be), -math.sin(be))                 # 地球から太陽への向き
    d = (-s[0], -s[1])                                  # 光の進む向き
    n = (math.sin(be), -math.cos(be))                   # s に直角で上向き
    A = (C[0] + R * s[0], C[1] + R * s[1])              # ① 太陽が真上
    B = (C[0] + R * n[0], C[1] + R * n[1])              # ② 太陽が地平線
    b = ['<defs><clipPath id="body"><rect x="48" y="96" width="740" height="524"/></clipPath>'
         f'<linearGradient id="rayB" gradientUnits="userSpaceOnUse" x1="{B[0] - d[0] * 192:.1f}" y1="{B[1] - d[1] * 192:.1f}" x2="{B[0]:.1f}" y2="{B[1]:.1f}">'
         f'<stop offset="0" stop-color="{SUN}"/><stop offset=".55" stop-color="#ef9a3c"/><stop offset="1" stop-color="{ACC}"/></linearGradient></defs>']
    g = ['<g clip-path="url(#body)">']
    g.append(circle(*C, RA, "#e6f0f6", "#b9d3e2", 1.4))
    g.append(circle(*C, R, "#cfdcc4", "#8aa27a", 2))
    g.append('</g>')
    b += g
    b.append(text(C[0] + 246, C[1] - 136, "空気の層", 15, TEAL_D, 700, "middle"))
    # 太陽の光（平行な光）
    b.append(text(56, 122, "太陽の光", 17, GOLD, 700))
    sl = d[1] / d[0]
    for y in range(140, 470, 54):
        b.append(line(52, y, 108, y + 56 * sl, GOLD, 2.2, arrow="gold"))
    # ② 地平線から来る光：空気の中を長く通る
    tB = math.sqrt(RA ** 2 - R ** 2)
    eB = (B[0] - d[0] * tB, B[1] - d[1] * tB)
    x0 = 120; y0B = B[1] - (B[0] - x0) * sl
    b.append(line(x0, y0B, eB[0], eB[1], SUN, 4))
    b.append(f'<line x1="{eB[0]:.1f}" y1="{eB[1]:.1f}" x2="{B[0]:.1f}" y2="{B[1]:.1f}" stroke="url(#rayB)" stroke-width="6" stroke-linecap="round"/>')
    for k, f in enumerate((0.12, 0.32, 0.52, 0.72)):
        px, py = eB[0] + (B[0] - eB[0]) * f, eB[1] + (B[1] - eB[1]) * f
        ang = math.radians(-60 - 25 * (k % 2))
        b.append(line(px, py, px + 34 * math.cos(ang), py + 34 * math.sin(ang), BLUE, 2.2, arrow="teal"))
    # ① 真上から来る光：空気の中を短く通る
    tA = RA - R
    eA = (A[0] - d[0] * tA, A[1] - d[1] * tA)
    y0A = A[1] - (A[0] - x0) * sl
    b.append(line(x0, y0A, A[0] - d[0] * 8, A[1] - d[1] * 8, SUN, 4))
    for ang in (-150, -100, 170):
        a = math.radians(ang); px, py = eA[0] + (A[0] - eA[0]) * 0.5, eA[1] + (A[1] - eA[1]) * 0.5
        b.append(line(px, py, px + 30 * math.cos(a), py + 30 * math.sin(a), BLUE, 2.2, arrow="teal"))
    b.append(person(*A, *s))
    b.append(person(*B, *n))
    b.append(badge(A[0] + 34, A[1] + 30, "①", TEAL, "#fff", 18))
    b.append(badge(B[0] + 28, B[1] - 46, "②", ACC, "#fff", 18))
    b.append(text(eB[0] - 40, eB[1] - 66, "空気の中の道のりが長い", 15, ACC, 700, "middle"))
    b.append(text(A[0] + 58, A[1] + 36, "道のりが短い", 15, TEAL_D, 700))
    b.append(text(C[0], C[1] - 70, "地球", 18, "#4d6340", 700, "middle"))
    # 右：説明
    X = 812
    b.append(text(X, 128, "① 昼（太陽が高い）", 18, TEAL, 700))
    b.append(lines(X, 158, ["空気の中を通る道のりが短い。", "青い光が空いっぱいに散らばり、", "空が青く見える。"], 16, INK, 1.5))
    b.append(text(X, 270, "② 夕方（太陽が地平線の近く）", 18, ACC, 700))
    b.append(lines(X, 300, ["道のりは真上から来るときの約38倍。", "青い光は途中で散らばって減り、", "残った赤・オレンジの光が届く。"], 16, INK, 1.5))
    b.append(text(X, 424, "光の色と散らばりやすさ", 17, INK, 700))
    b.append('<defs><linearGradient id="spec" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#5b3fa8"/>'
             '<stop offset=".2" stop-color="#2f6fd0"/><stop offset=".45" stop-color="#3fa86a"/><stop offset=".65" stop-color="#e8d23a"/>'
             '<stop offset=".82" stop-color="#ef8a2c"/><stop offset="1" stop-color="#c8301e"/></linearGradient></defs>')
    b.append(f'<rect x="{X}" y="440" width="330" height="26" rx="4" fill="url(#spec)"/>')
    b.append(text(X, 490, "青（波長 約450nm）", 15, INK2))
    b.append(text(X + 330, 490, "赤（約700nm）", 15, INK2, anchor="end"))
    b.append(text(X, 524, "青い光は赤い光の約6倍", 17, BLUE, 700))
    b.append(text(X, 548, "散らばりやすい", 17, BLUE, 700))
    b.append(text(X, 576, "（波長の4乗に反比例＝レイリー散乱）", 14, INK2))
    return svg("".join(b), "夕焼けが赤いしくみ（光の散乱）",
               "模式図（大きさ・空気の厚さは実際とちがう）。散乱＝光が空気の分子に当たって、いろいろな向きに散らばること。")


def fig2():
    b = [text(48, 124, "日の入りのころの雲量と焼け度（このページの判定）", 18, INK, 700)]
    y, rh, bx, k = 146, 75, 214, 3.3
    for i, (rng, sub, sc, lab) in enumerate(YAKE):
        assert score(int(rng.split("〜")[1].rstrip("%"))) == sc      # 区分の上端がページの判定と同じか
        yy = y + rh * i
        if i % 2 == 0:
            b.append(f'<rect x="48" y="{yy}" width="560" height="{rh}" fill="#f2efe7"/>')
        b.append(text(60, yy + 32, rng, 18, INK, 700))
        if sub:
            b.append(text(60, yy + 56, sub, 14, INK2))
        t = sc / 88                       # 点が高いほど濃い朱
        col = "#%02x%02x%02x" % tuple(round(a + (c - a) * t) for a, c in zip((0xee, 0xdc, 0xbf), (0xc4, 0x44, 0x2b)))
        b.append(rect(bx, yy + 13, sc * k, 26, col, "none", 3, 0))
        b.append(text(bx + sc * k + 10, yy + 34, f"{sc}点", 19, INK, 700))
        b.append(text(bx, yy + 62, lab, 15, INK2))
    b.append(text(60, 140 + rh * 6 + 22, "雲量＝空のうち雲がおおっている割合", 14, MUTED))
    # 右上：雲がスクリーンになる
    X0, X1 = 648, 1152
    b.append(f'<defs><clipPath id="pane"><rect x="{X0}" y="100" width="{X1 - X0}" height="300"/></clipPath>'
             f'<linearGradient id="cb" x1="0" x2="0" y1="0" y2="1"><stop offset=".45" stop-color="#f3f1ec"/><stop offset="1" stop-color="#ef8a4a"/></linearGradient></defs>')
    b.append(rect(X0, 100, X1 - X0, 300, "#eef3f6", LINE, 10))
    Ec, Er = (850, 1110), 760
    top = Ec[1] - Er
    b.append(f'<circle cx="{Ec[0]}" cy="{Ec[1]}" r="{Er}" fill="#d8cfb8" stroke="#b9a983" clip-path="url(#pane)"/>')
    sun = (1110, 382)
    for cx, cy, rx in [(780, 196, 62), (930, 222, 70)]:
        b.append(f'<line x1="{sun[0]}" y1="{sun[1]}" x2="{cx + rx * 0.3:.1f}" y2="{cy + 20:.1f}" stroke="{ACC}" stroke-width="2" stroke-dasharray="6 5"/>')
    for cx, cy, rx in [(780, 196, 62), (930, 222, 70)]:
        b.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="22" fill="url(#cb)" stroke="#c9c3b6" stroke-width="1"/>')
    b.append(circle(*sun, 15, SUN, GOLD, 1.5))
    b.append(line(X0 + 10, top, X1 - 10, top, INK2, 1.4, "6 5"))
    b.append(person(Ec[0], top, 0, -1))
    b.append(text(X1 - 14, top - 10, "地平線", 14, INK2, anchor="end"))
    b.append(text(sun[0] - 22, sun[1] + 6, "太陽（地平線の下）", 14, INK, 700, "end"))
    b.append(text(X0 + 16, 128, "日没後、地平線の下の太陽の光が", 16, INK, 700))
    b.append(text(X0 + 16, 152, "雲の底を照らす＝雲がスクリーンになる", 16, INK, 700))
    # 右下：ベスト観賞タイム
    ty, tx0, pm = 506, 690, 18.0
    b.append(text(X0, 438, "ベスト観賞タイム（このページの表示）", 17, INK, 700))
    b.append(rect(tx0 + 5 * pm, ty - 26, 15 * pm, 52, ACC_L, ACC, 6, 1.4))
    b.append(text(tx0 + 12.5 * pm, ty + 6, "マジックアワー", 17, ACC, 700, "middle"))
    b.append(arrow(tx0 - 20, ty + 40, tx0 + 23 * pm, ty + 40, "ink", 2))
    for m, lab in [(0, "日の入り"), (5, "5分後"), (20, "20分後")]:
        b.append(line(tx0 + m * pm, ty + 32, tx0 + m * pm, ty + 48, INK, 2))
        b.append(text(tx0 + m * pm, ty + 70, lab, 15, INK, 700 if m == 0 else 400, "middle"))
    b.append(text(tx0 + 24 * pm, ty + 46, "時刻", 14, INK2))
    return svg("".join(b), "夕焼けになりやすい条件（焼け度の決まり）",
               "雲量は日の入りの時刻にいちばん近い1時間の予報（Open-Meteo）。雲の高さや厚さは見ていない。")


FIGS = [
    dict(svg=fig1, alt="夕焼けが赤い理由を示す図。太陽が高い昼は光が空気の中を通る道のりが短く、散らばりやすい青い光が空いっぱいに広がって空が青く見える。太陽が地平線の近くにある夕方は道のりが約38倍になり、青い光が途中で散乱して減り、赤・オレンジの光が届いて夕焼けになる。",
         caption="夕焼けが赤いしくみ。地平線近くの太陽の光は空気の中を長く通り、青い光が散らばって赤い光が残る。"),
    dict(svg=fig2, alt="今日の夕焼け予報の判定の決まり。日の入りのころの雲量が0〜5%なら55点、6〜15%は70点、16〜40%は88点、41〜65%は74点、66〜85%は40点、86%以上は15点。日没後に地平線の下の太陽が雲の底を照らす様子と、ベスト観賞タイム（日の入りの5〜20分後）も示す。",
         caption="焼け度の決まり。日の入りのころの雲量が16〜40%の日がいちばん高い88点。見ごろは日の入りの5〜20分後。"),
]
