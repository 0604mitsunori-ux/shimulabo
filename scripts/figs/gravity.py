"""重力シミュレーター（gravity）の図。
ページの JS と同じ式：太陽が星を引く加速度 = G·M ÷ r²（距離の2乗に反比例）。クリックしたときの初速 = √(GM/r) × 0.9（円軌道の速さの0.9倍・横向き）。
軌道の形は、同じ場所から横向きに打ち出したときの円錐曲線（円・楕円・放物線・双曲線）を式で計算して描く。"""
import math
from figlib import *

ANCHOR = r"万有引力（距離の2乗に反比例）で計算しています。</p>\s*"


def fig1():
    b = []
    # 左：2つの物体が引き合う
    Mx, mx, y = 150, 470, 238
    b.append(circle(Mx, y, 54, SUN, GOLD, 2) + text(Mx, y + 7, "M", 24, INK, 700, "middle"))
    b.append(circle(mx, y, 20, SKY, TEAL, 2) + text(mx, y + 6, "m", 18, INK, 700, "middle"))
    b.append(arrow(mx - 24, y, mx - 104, y, "acc", 3.2) + text(mx - 64, y - 14, "F", 19, ACC, 700, "middle"))
    b.append(arrow(Mx + 58, y, Mx + 138, y, "acc", 3.2) + text(Mx + 98, y - 14, "F", 19, ACC, 700, "middle"))
    b.append(line(Mx, y + 76, mx, y + 76, INK2, 1.4) + line(Mx, y + 66, Mx, y + 86, INK2, 1.4) + line(mx, y + 66, mx, y + 86, INK2, 1.4))
    b.append(text((Mx + mx) / 2, y + 102, "r（中心どうしのきょり）", 16, INK, anchor="middle"))
    b.append(text(48, 128, "2つの物体は、同じ大きさの力で引き合う", 17, INK, 700))
    b.append(rect(48, 378, 500, 210, GOLD_L, GOLD, 10, 1.4))
    b.append(text(298, 432, "F ＝ G × M × m ÷ r²", 30, INK, 700, "middle", font_family=SERIF))
    b.append(lines(72, 478, ["F：引き合う力（万有引力）", "G：万有引力定数（どこでも同じ数）",
                             "M・m：2つの物体の質量", "r：2つの物体の中心どうしのきょり"], 16, INK2, 1.5))
    # 右：きょりと力のグラフ
    gx0, gy0, gw, gh = 660, 560, 440, 400
    k = gw / 4.4
    b.append(axes(gx0, gy0, gw, gh, "", "引き合う力（r＝1のときを1）",
                  [(k * r, f"{r}") for r in (1, 2, 3, 4)], [(gh * v, f"{v:g}") for v in (0, 0.25, 0.5, 0.75, 1)], 15))
    b.append(text(gx0 + gw + 2, gy0 + 46, "きょり r", 15, INK, anchor="end"))
    pts = [(gx0 + k * r, gy0 - gh / (r * r)) for r in [1 + i * 0.02 for i in range(171)]]
    b.append(poly(pts, TEAL, 2.4))
    for r, lab in [(1, "1"), (2, "1/4"), (3, "1/9"), (4, "1/16")]:
        x, yy = gx0 + k * r, gy0 - gh / (r * r)
        b.append(f'<rect x="{x - 14:.1f}" y="{yy:.1f}" width="28" height="{gy0 - yy:.1f}" fill="{TEAL_L}" stroke="{TEAL}" stroke-width="1"/>')
        b.append(circle(x, yy, 5, TEAL, TEAL, 0))
        b.append(text(x + 18, yy - 8, lab, 20, ACC, 700))
    b.append(lines(gx0 + 170, gy0 - gh + 60, ["きょりが2倍 → 力は 1/4", "きょりが3倍 → 力は 1/9", "（きょりの2乗に反比例）"], 16, INK, 1.55))
    return svg("".join(b), "万有引力の式と、きょりによる力の変わり方",
               "このシミュは、太陽が星を引く力をこの式で毎回計算している（星どうしの引き合いは無視）。")


SX, SY, R0, SUN_R = 372, 362, 108, 15


def conic(kk):
    """太陽から R0 の点で、円軌道の速さの kk 倍で横向き（画面の下向き）に打ち出したときの軌道の点列"""
    pts = []
    if abs(kk - 1) < 1e-9:
        return [(SX + R0 * math.cos(math.radians(a)), SY + R0 * math.sin(math.radians(a))) for a in range(0, 361, 3)]
    p = R0 * kk * kk
    if kk > 1:
        e = kk * kk - 1
        lim = math.degrees(math.acos(-1 / e)) - 0.5 if e > 1 else 179.5
        for s in (-1, 1):
            seg = []
            a = 0.0
            while a <= lim:
                r = p / (1 + e * math.cos(math.radians(a)))
                seg.append((SX + r * math.cos(math.radians(s * a)), SY + r * math.sin(math.radians(s * a))))
                if r > 2000: break
                a += 0.5
            pts.append(seg[::-1] if s < 0 else seg)
        return pts[0] + pts[1]
    e = 1 - kk * kk
    for a10 in range(0, 3601, 5):
        a = a10 / 10
        r = p / (1 - e * math.cos(math.radians(a)))
        if r <= SUN_R:
            pts.append((SX + SUN_R * math.cos(math.radians(a)), SY + SUN_R * math.sin(math.radians(a))))
            break
        pts.append((SX + r * math.cos(math.radians(a)), SY + r * math.sin(math.radians(a))))
    return pts


ORB = [  # 速さの倍率, 名前, 色, 線の種類, ラベル位置(角度・度), ラベルのずれ
    (0.4, "落ちる", MUTED, None),
    (0.9, "楕円", GOLD, None),
    (1.0, "円", TEAL, None),
    (1.2, "楕円", INK, "8 6"),
    (math.sqrt(2), "放物線", ACC, "3 5"),
    (1.7, "双曲線", ACC, None),
]


def fig2():
    clip = '<clipPath id="gclip"><rect x="48" y="100" width="640" height="524"/></clipPath>'
    b = ['<g clip-path="url(#gclip)">']
    for kk, nm, col, dash in ORB:
        b.append(poly(conic(kk), col, 2.6 if kk != 1.0 else 3, dash=dash))
    b.append('</g>')
    b.append(circle(SX, SY, SUN_R, SUN, GOLD, 2))
    b.append(text(SX - 22, SY + 6, "太陽", 15, INK, 700, "end"))
    px_, py_ = SX + R0, SY
    b.append(circle(px_, py_, 7, INK, INK, 0))
    b.append(arrow(px_ + 16, py_ - 34, px_ + 16, py_ + 40, "ink", 2.6))
    b.append(lines(px_ + 26, py_ - 24, ["ここから横向きに", "打ち出す"], 15, INK, 1.4, font_weight="700"))
    # ラベル（曲線の上の点に）
    def at(kk, a):
        if abs(kk - 1) < 1e-9: r = R0
        elif kk > 1: r = R0 * kk * kk / (1 + (kk * kk - 1) * math.cos(math.radians(a)))
        else: r = R0 * kk * kk / (1 - (1 - kk * kk) * math.cos(math.radians(a)))
        return SX + r * math.cos(math.radians(a)), SY + r * math.sin(math.radians(a))
    labs = [(1.0, 270, "円（1倍）", 0, -12, "middle", TEAL),
            (1.2, 205, "楕円（1.2倍）", -8, -10, "end", INK),
            (math.sqrt(2), 265, "放物線（√2倍）", -12, 4, "end", ACC),
            (1.7, 60, "双曲線（1.7倍）", 12, 4, "start", ACC)]
    for kk, a, s, dx, dy, anc, col in labs:
        x, y = at(kk, a)
        b.append(text(x + dx, y + dy, s, 15.5, col, 700, anc))
    b.append(text(389, 304, "楕円（0.9倍）", 15.5, GOLD, 700, "middle"))
    b.append(text(392, 420, "落ちる（0.4倍）", 15.5, MUTED, 700, "middle"))
    # 右：まとめ
    X = 716
    b.append(text(X, 128, "打ち出す速さ（円軌道の速さを1倍とする）", 17, INK, 700))
    rows = [("0.4倍", "太陽に落ちる"), ("0.9倍", "楕円（このシミュでクリックしたとき）"), ("1倍", "円"),
            ("1.2倍", "細長い楕円（戻ってくる）"), ("√2倍（約1.41倍）", "放物線（ぎりぎり戻らない）"), ("1.7倍", "双曲線（飛び去る）")]
    for i, ((kk, nm, col, dash), (sp, desc)) in enumerate(zip(ORB, rows)):
        yy = 166 + i * 38
        b.append(line(X, yy - 5, X + 40, yy - 5, col, 3, dash))
        b.append(text(X + 52, yy, sp, 16, INK, 700))
        b.append(text(X + 196, yy, desc, 15.5, INK2))
    b.append(rect(X, 404, 436, 178, GOLD_L, GOLD, 10, 1.4))
    b.append(text(X + 18, 436, "円軌道の速さ　v ＝ √(GM ÷ r)", 18, INK, 700))
    b.append(lines(X + 18, 470, ["地球の表面すれすれなら 約7.9 km/s", "（第一宇宙速度）",
                                 "その√2倍の 約11.2 km/s で地球から", "飛び去る（第二宇宙速度）"], 15.5, INK2, 1.5))
    return svg("".join(b), "打ち出す速さと軌道の形（円・楕円・放物線・双曲線）",
               "どれも同じ点から横向きに打ち出し、万有引力の式で計算した軌道。速さだけで形が決まる。", clip)


FIGS = [
    dict(svg=fig1, alt="万有引力の法則の図。質量Mとmの2つの物体が同じ大きさの力Fで引き合い、F＝G×M×m÷r²で表されることと、きょりrが2倍になると力は4分の1、3倍で9分の1になる（きょりの2乗に反比例する）ことを示すグラフ。",
         caption="万有引力の式。引き合う力はきょりの2乗に反比例し、きょりが2倍なら力は1/4になる。"),
    dict(svg=fig2, alt="太陽のまわりで同じ点から横向きに打ち出した星の軌道の図。打ち出す速さが円軌道の速さの0.4倍だと太陽に落ち、0.9倍と1.2倍は楕円、1倍は円、√2倍は放物線、1.7倍は双曲線になることと、第一宇宙速度約7.9km/s・第二宇宙速度約11.2km/sを示す。",
         caption="打ち出す速さと軌道の形。速さが円軌道の√2倍をこえると、星は戻ってこない。"),
]
