"""天気と1日の気温（tenki-kion）の授業用の図。数値はページの JS（scripts/rika/sims_sho4_b.py の JS_TENKI）と同じ式で計算する。"""
import math
from figlib import *

# ---- ページの JS と同じモデル（JS_TENKI） ----
WX = {"hare": dict(nm="晴れ", lo=12, amp=11, sun=7, gnd=4, gn=1),
      "kumori": dict(nm="くもり", lo=14, amp=4, sun=1.5, gnd=1, gn=0.3),
      "ame": dict(nm="雨", lo=13.4, amp=1.5, sun=0, gnd=0, gn=0)}
H0 = 80                                   # 水のゆくえ：はじめの水の高さ [mm]
LOC = {"hinata": dict(o=4, c=0.1), "hikage": dict(o=1.5, c=0.05)}
TR = 25                                   # 結ろ：部屋の気温 [℃]


def fday(t):
    return (1 - math.cos(math.pi * (t - 6) / 8)) / 2 if t <= 14 else 0.5 + 0.5 * math.cos(math.pi * (t - 14) / 10)


def temp(w, t):
    return WX[w]["lo"] + WX[w]["amp"] * fday(t)


def sunI(t):
    return max(0.0, math.sin(math.pi * (t - 6) / 12))


def reading(w, t, p):
    q, s, T = WX[w], sunI(t), temp(w, t)
    return T + q["sun"] * s if p == "hinata" else (T + q["gnd"] * s - q["gn"] * (1 - s) if p == "jimen" else T)


def es(x):
    return 6.1078 * 10 ** (7.5 * x / (x + 237.3))


def dew(rh):
    a = math.log10(rh / 100 * es(TR) / 6.1078)
    return 237.3 * a / (7.5 - a)


def r0(x):                                 # JS の Math.round と同じ（.5 は切り上げ）
    return int(math.floor(x + 0.5))


# ---- 部品 ----
GROUND, GROUND_D, CLOUD, VAP = "#d8cfb8", "#b9a983", "#c9ced4", "#7fb3d5"


def sun_icon(cx, cy, r):
    out = []
    for k in range(8):
        a = k * math.pi / 4
        out.append(line(cx + (r + 6) * math.cos(a), cy + (r + 6) * math.sin(a), cx + (r + 15) * math.cos(a), cy + (r + 15) * math.sin(a), GOLD, 3))
    return "".join(out) + circle(cx, cy, r, SUN, GOLD, 2)


def cloud(cx, cy, s, fill=CLOUD):
    return (f'<g fill="{fill}"><circle cx="{cx - s * 0.55:.1f}" cy="{cy + s * 0.1:.1f}" r="{s * 0.42:.1f}"/>'
            f'<circle cx="{cx:.1f}" cy="{cy - s * 0.18:.1f}" r="{s * 0.55:.1f}"/>'
            f'<circle cx="{cx + s * 0.6:.1f}" cy="{cy + s * 0.12:.1f}" r="{s * 0.4:.1f}"/>'
            f'<rect x="{cx - s * 0.95:.1f}" y="{cy + s * 0.05:.1f}" width="{s * 1.9:.1f}" height="{s * 0.47:.1f}" rx="{s * 0.2:.1f}"/></g>')


def wavy_up(x, y0, y1, amp=5, color=ACC):
    """下から上へのゆらゆらした矢印（あたためられた空気）"""
    n, pts = 24, []
    for i in range(n + 1):
        y = y0 + (y1 - y0) * i / n
        pts.append((x + amp * math.sin(i / n * 2 * math.pi * 1.5), y))
    d = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.6" marker-end="url(#ah-acc)"/>'


def dot(x, y, r=4.2, fill=VAP):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" opacity=".9"/>'


def drop(x, y, r=5):
    """水てき（しずく形）"""
    return (f'<path d="M{x:.1f},{y - r * 1.7:.1f} C{x + r * 0.4:.1f},{y - r * 0.9:.1f} {x + r:.1f},{y - r * 0.3:.1f} {x + r:.1f},{y + r * 0.2:.1f} '
            f'A{r},{r} 0 0 1 {x - r:.1f},{y + r * 0.2:.1f} C{x - r:.1f},{y - r * 0.3:.1f} {x - r * 0.4:.1f},{y - r * 0.9:.1f} {x:.1f},{y - r * 1.7:.1f}Z" '
            f'fill="#dbeef8" stroke="{TEAL}" stroke-width="1.4"/>')


# ---- 図1：しくみ図 ----
def fig1():
    b = []
    # ===== 左：気温が変わるしくみ =====
    b.append(rect(48, 98, 548, 524, CARD, LINE, 12))
    b.append(text(66, 128, "気温が変わるしくみ", 20, INK, 700))
    # 晴れの日
    ax0, ax1, sy0, gy = 64, 324, 144, 330
    b.append(rect(ax0, sy0, ax1 - ax0, gy - sy0, TEAL_L, TEAL_L, 0) + rect(ax0, gy, ax1 - ax0, 38, GROUND, GROUND, 0))
    b.append(text(ax1 - 12, sy0 + 26, "晴れの日", 18, INK, 700, "end"))
    b.append(sun_icon(102, 184, 20))
    for ex in (135, 195, 255):
        b.append(arrow(102 + 26 * (ex - 102) / math.hypot(ex - 102, gy - 184), 184 + 26 * (gy - 184) / math.hypot(ex - 102, gy - 184), ex, gy - 4, "gold", 2.6))
    for wx in (166, 226, 292):
        b.append(wavy_up(wx, gy - 6, gy - 66, 4))
    b.append(text(ax0 + 10, gy + 25, "① 日光が地面をあたためる", 15, INK, 700))
    b.append(text(ax1 - 10, gy - 98, "② 地面が空気を", 15, ACC, 700, "end") + text(ax1 - 10, gy - 79, "あたためる", 15, ACC, 700, "end"))
    # くもり・雨の日
    bx0, bx1 = 340, 580
    b.append(rect(bx0, sy0, bx1 - bx0, gy - sy0, "#e9ecef", "#e9ecef", 0) + rect(bx0, gy, bx1 - bx0, 38, GROUND, GROUND, 0))
    b.append(f'<g opacity=".45">{sun_icon(380, 184, 20)}</g>')
    for ex in (404, 428):
        b.append(arrow(380 + 24 * (ex - 380) / math.hypot(ex - 380, 40), 184 + 24 * 40 / math.hypot(ex - 380, 40), ex, 220, "gold", 2.4))
    b.append(cloud(440, 226, 46) + cloud(520, 214, 40))
    for i in range(7):
        x = 418 + i * 22
        b.append(line(x, 262, x - 5, 280, TEAL, 2))
    b.append(text(bx1 - 12, sy0 + 26, "くもり・雨の日", 18, INK, 700, "end"))
    b.append(text(bx0 + 12, gy - 18, "雲が日光をさえぎる", 15, INK, 700))
    b.append(text(bx0 + 10, gy + 25, "地面があまりあたたまらない", 15, INK, 700))
    # 下の一言（差）
    dh = temp("hare", 14) - temp("hare", 6); dk = temp("kumori", 14) - temp("kumori", 6); da = temp("ame", 14) - temp("ame", 6)
    b.append(text((ax0 + ax1) / 2, 396, "1日の気温の差が大きい", 16, INK, 700, "middle"))
    b.append(text((ax0 + ax1) / 2, 418, f"晴れ　約{r0(dh)}℃（山の形）", 16, ACC, 700, "middle"))
    b.append(text((bx0 + bx1) / 2, 396, "1日の気温の差が小さい", 16, INK, 700, "middle"))
    b.append(text((bx0 + bx1) / 2, 418, f"くもり 約{r0(dk)}℃・雨 約1〜2℃", 16, TEAL_D, 700, "middle"))
    # 太陽の高さと気温（晴れの日）
    b.append(line(64, 436, 580, 436, LINE, 1.2))
    b.append(text(66, 462, "太陽の高さと気温（晴れの日）", 16, INK, 700))
    cx0, cx1, cy0, ch = 92, 560, 584, 92
    gx = lambda t: cx0 + (cx1 - cx0) * (t - 6) / 12
    b.append(line(cx0, cy0, cx1, cy0, INK, 1.6))
    sp = [(gx(t / 10), cy0 - ch * sunI(t / 10)) for t in range(60, 181)]
    tp = [(gx(t / 10), cy0 - ch * fday(t / 10)) for t in range(60, 181)]
    b.append(poly(sp, GOLD, 2.6, dash="7 5"))
    b.append(poly(tp, ACC, 3.2))
    for t, lab, c in [(12, "正午", GOLD), (14, "午後2時", ACC)]:
        b.append(line(gx(t), cy0, gx(t), cy0 - ch - 6, c, 1.4, "3 4"))
        b.append(circle(gx(t), cy0 - ch, 5, c, c, 0))
    b.append(text(gx(12) - 8, cy0 - ch - 10, "太陽がいちばん高い", 15, GOLD, 700, "end"))
    b.append(text(gx(14) + 8, cy0 - ch - 10, "気温がいちばん高い", 15, ACC, 700))
    b.append(text(gx(6), cy0 + 22, "午前6時", 14, INK2, anchor="middle") + text(gx(12), cy0 + 22, "正午", 14, INK2, anchor="middle")
             + text(gx(14), cy0 + 22, "午後2時", 14, INK2, anchor="middle") + text(gx(18), cy0 + 22, "午後6時", 14, INK2, anchor="middle"))
    b.append(line(350, 457, 382, 457, GOLD, 2.6, "7 5") + text(388, 462, "太陽の高さ", 14, GOLD, 700))
    b.append(line(474, 457, 506, 457, ACC, 3.2) + text(512, 462, "気温", 14, ACC, 700))

    # ===== 右：水のゆくえ =====
    X0 = 612
    b.append(rect(X0, 98, 540, 524, CARD, LINE, 12))
    b.append(text(X0 + 18, 128, "水のゆくえ（じょう発と結ろ）", 20, INK, 700))
    tb = 440                                            # 台の上面
    b.append(rect(X0 + 16, 144, 508, tb - 144, "#f3f7f9", "#f3f7f9", 0) + rect(X0 + 16, tb, 508, 12, GROUND_D, GROUND_D, 0))
    # 空気中の水じょう気
    b.append(dot(X0 + 30, 167, 5) + text(X0 + 42, 173, "＝空気中の水じょう気（目に見えない・イメージ）", 15, TEAL_D, 700))
    for x, y in [(700, 214), (742, 236), (790, 205), (850, 246), (905, 214), (950, 192), (1000, 228), (1060, 204), (1110, 240), (668, 262), (1120, 290)]:
        b.append(dot(x, y))
    mm = 1.0                                             # 1 mm → 1 px
    # 1) ふたなし（日なたに3日）
    c1x, cw, cb = 650, 96, tb
    ho = max(0, H0 - LOC["hinata"]["o"] * 3); hc = H0 - LOC["hinata"]["c"] * 3
    top = cb - 110
    b.append(f'<rect x="{c1x}" y="{cb - ho * mm:.1f}" width="{cw}" height="{ho * mm:.1f}" fill="#cfe5f1"/>')
    b.append(line(c1x - 6, cb - H0 * mm, c1x + cw + 6, cb - H0 * mm, ACC, 1.8, "6 4"))
    b.append(text(c1x + cw + 8, cb - H0 * mm + 5, "はじめ", 14, ACC, 700))
    b.append(poly([(c1x, top), (c1x, cb), (c1x + cw, cb), (c1x + cw, top)], INK2, 2.6))
    for x, y in [(c1x + 22, cb - ho - 22), (c1x + 52, cb - ho - 40), (c1x + 76, cb - ho - 18), (c1x + 34, cb - ho - 62), (c1x + 66, cb - ho - 80)]:
        b.append(dot(x, y))
    b.append(arrow(c1x + cw / 2, top - 6, c1x + cw / 2, top - 74, "teal", 2.6))
    b.append(text(c1x + cw / 2 + 10, top - 50, "じょう発", 16, TEAL_D, 700))
    # 2) ふたあり（ラップ）
    c2x = 812
    b.append(f'<rect x="{c2x}" y="{cb - hc * mm:.1f}" width="{cw}" height="{hc * mm:.1f}" fill="#cfe5f1"/>')
    b.append(line(c2x - 6, cb - H0 * mm, c2x + cw + 6, cb - H0 * mm, ACC, 1.8, "6 4"))
    b.append(poly([(c2x, top), (c2x, cb), (c2x + cw, cb), (c2x + cw, top)], INK2, 2.6))
    b.append(f'<path d="M{c2x - 8},{top} Q{c2x + cw / 2},{top + 10} {c2x + cw + 8},{top}" fill="none" stroke="{MUTED}" stroke-width="2.4"/>')
    for i in range(6):
        fx = c2x + 10 + i * 15.2
        b.append(drop(fx, top + 6 + 4 * math.sin(math.pi * (fx - c2x) / cw) + 6, 4))
    b.append(text(c2x + cw / 2, top - 14, "ラップ", 15, INK2, 700, "middle"))
    # 3) 冷たい水のコップ
    k0, kt, kb2 = 1010, 316, tb                         # 中心・上・下
    wt, wb = 46, 38
    b.append(f'<path d="M{k0 - wt},{kt + 26} L{k0 + wt},{kt + 26} L{k0 + wb},{kb2} L{k0 - wb},{kb2}Z" fill="#d6ebf6"/>')
    for dx, dy, a in [(-18, kt + 44, -12), (12, kt + 56, 14), (-6, kt + 82, 4)]:
        b.append(f'<rect x="{k0 + dx - 12}" y="{dy - 12}" width="24" height="24" rx="5" fill="#fff" stroke="{SKY}" stroke-width="1.6" transform="rotate({a} {k0 + dx} {dy})"/>')
    b.append(poly([(k0 - wt, kt), (k0 - wb, kb2), (k0 + wb, kb2), (k0 + wt, kt)], INK2, 2.6))
    for fy in (0.25, 0.45, 0.65, 0.85):
        for side in (-1, 1):
            yy = kt + (kb2 - kt) * fy
            xx = k0 + side * (wt + (wb - wt) * fy + 6)
            b.append(drop(xx, yy, 4.6))
    for x0_, y0_ in [(1100, 300), (1112, 380), (928, 302)]:
        b.append(dot(x0_, y0_))
        b.append(arrow(x0_ + (-14 if x0_ > k0 else 14), y0_ + 6, k0 + (wt + 16 if x0_ > k0 else -wt - 16), y0_ + 22, "teal", 2))
    b.append(text(k0, kt - 14, "氷水", 15, INK2, 700, "middle"))
    # 下のラベル
    for x, l1, l2 in [(c1x + cw / 2, "ふたなし", f"3日で {H0}→{r0(ho)} mm"), (c2x + cw / 2, "ふたあり", "ほとんどへらない"),
                      (k0, "冷たい水のコップ", "外側に水てき")]:
        b.append(text(x, tb + 38, l1, 16, INK, 700, "middle") + text(x, tb + 60, l2, 15, TEAL_D, 700, "middle"))
    b.append(text(X0 + 18, 534, "じょう発：水が水面や地面から水じょう気になって、空気中へ出ていくこと", 15, INK))
    b.append(text(X0 + 18, 558, "結ろ：空気中の水じょう気が冷やされて、水てきになってあらわれること", 15, INK))
    b.append(text(X0 + 18, 586, "ふたなし・ふたありは、日なたに置いたときの目安。", 14, MUTED))
    b.append(text(X0 + 18, 607, f"気温{TR}℃・しつ度60%の部屋では、コップが約{r0(dew(60))}℃より冷たいと水てきがつく。", 14, MUTED))
    return svg("".join(b), "天気と気温・水のゆくえのしくみ",
               "日光が地面をあたため、地面が空気をあたためる。水はじょう発して空気中に入り、冷やされると水にもどる。")


# ---- 図2：まとめ図 ----
def fig2():
    b = []
    # ===== 左：1日の気温のグラフ =====
    b.append(text(48, 124, "天気と1日の気温の変わり方（目安）", 19, INK, 700))
    x0, y0, pxh = 118, 552, 38                          # 原点（0℃）と1時間の幅
    y10, pxd = 518, 22                                  # 10℃の位置と1℃の高さ
    gx = lambda t: x0 + pxh * (t - 6)
    gy = lambda v: y10 - pxd * (v - 10)
    w = pxh * 12
    for v in range(10, 26):
        b.append(line(x0, gy(v), x0 + w, gy(v), LINE if v % 5 else "#cfc9bb", 1 if v % 5 else 1.3))
    for h in range(7, 19):
        b.append(line(gx(h), y10, gx(h), gy(25), LINE, 1))
    b.append(line(x0, y0, x0 + w + 10, y0, INK, 1.8, arrow="ink") + line(x0, y0, x0, gy(25) - 18, INK, 1.8, arrow="ink"))
    # 波線（0〜10℃を省略）
    b.append(f'<path d="M{x0 - 9},{y0 - 14} q4,-5 9,0 t9,0 M{x0 - 9},{y0 - 22} q4,-5 9,0 t9,0" fill="none" stroke="{INK}" stroke-width="1.6"/>')
    b.append(f'<rect x="{x0 - 2}" y="{y0 - 23}" width="4" height="9" fill="{BG}"/>')
    for v in (10, 15, 20, 25):
        b.append(text(x0 - 10, gy(v) + 5, str(v), 15, INK2, anchor="end"))
    b.append(text(x0 - 10, y0 + 5, "0", 15, INK2, anchor="end"))
    b.append(text(x0 + 10, gy(25) - 8, "（℃）", 15, INK2))
    for h in range(6, 19):
        b.append(line(gx(h), y0, gx(h), y0 + 6, INK, 1.4))
        lab = "正午" if h == 12 else str(h if h < 12 else h - 12)
        b.append(text(gx(h), y0 + 24, lab, 15, INK2, anchor="middle"))
    b.append(text(gx(8.5), y0 + 48, "午前", 15, INK2, 700, "middle") + text(gx(15.5), y0 + 48, "午後", 15, INK2, 700, "middle"))
    b.append(text(x0 + w + 4, y0 + 48, "（時）", 15, INK2, anchor="end"))
    sty = {"hare": (ACC, 3.6, None), "kumori": (INK2, 3, "9 6"), "ame": (TEAL, 3, "3 5")}
    for k in ("ame", "kumori", "hare"):
        c, wd, ds = sty[k]
        b.append(poly([(gx(t / 10), gy(temp(k, t / 10))) for t in range(60, 181)], c, wd, dash=ds))
        for h in range(6, 19):
            X, Y = gx(h), gy(temp(k, h))
            if k == "hare": b.append(circle(X, Y, 5, CARD, c, 2.4))
            elif k == "kumori": b.append(f'<rect x="{X - 4.5:.1f}" y="{Y - 4.5:.1f}" width="9" height="9" fill="{CARD}" stroke="{c}" stroke-width="2.2"/>')
            else: b.append(f'<path d="M{X:.1f},{Y - 5.5:.1f} L{X + 5.5:.1f},{Y + 4:.1f} L{X - 5.5:.1f},{Y + 4:.1f}Z" fill="{CARD}" stroke="{c}" stroke-width="2.2"/>')
    ex = gx(18) + 14
    for k, nm, lab in [("hare", "晴れ", "山の形"), ("kumori", "くもり", "なだらか"), ("ame", "雨", "ほぼ平ら")]:
        c = sty[k][0]; Y = gy(temp(k, 18))
        b.append(text(ex, Y + 1, nm, 17, c, 700) + text(ex, Y + 21, lab, 15, c, 700))
    mx = temp("hare", 14)
    b.append(text(gx(14), gy(mx) - 16, f"いちばん高い {r0(mx)}℃（午後2時ごろ）", 16, ACC, 700, "middle"))
    mn = temp("hare", 6)
    b.append(text(gx(6) + 14, gy(mn) + 28, f"朝がいちばん低い {r0(mn)}℃", 15, ACC, 700))
    dk, da = temp("kumori", 14) - temp("kumori", 6), temp("ame", 14) - temp("ame", 6)
    bx_, by_ = 590, 160
    b.append(rect(bx_, by_, 136, 116, CARD, LINE, 8))
    b.append(text(bx_ + 68, by_ + 26, "1日の気温の差", 16, INK, 700, "middle"))
    for i, (nm, v, c) in enumerate([("晴れ", f"約{r0(mx - mn)}℃", ACC), ("くもり", f"約{r0(dk)}℃", INK2), ("雨", "約1〜2℃", TEAL)]):
        b.append(text(bx_ + 10, by_ + 54 + i * 22, nm, 15, c, 700) + text(bx_ + 128, by_ + 54 + i * 22, v, 15, c, 700, "end"))

    # ===== 右：気温の正しいはかり方 =====
    X0 = 742
    b.append(rect(X0, 98, 410, 524, CARD, LINE, 12))
    b.append(text(X0 + 18, 128, "気温の正しいはかり方", 19, INK, 700))
    gY = 396                                            # 地面
    b.append(rect(X0 + 14, gY, 382, 10, "#b9d4a6", "#b9d4a6", 0))
    bx, bw, by, bh = X0 + 70, 96, 192, 82               # 百葉箱
    for lx in (bx + 14, bx + bw - 14):
        b.append(line(lx, by + bh, lx, gY, MUTED, 4))
    b.append(f'<path d="M{bx - 10},{by} L{bx + bw / 2},{by - 22} L{bx + bw + 10},{by}Z" fill="{CARD}" stroke="{INK2}" stroke-width="1.8"/>')
    b.append(rect(bx, by, bw, bh, CARD, INK2, 2, 1.8))
    for yy in range(by + 9, by + bh - 4, 9):
        b.append(line(bx + 6, yy, bx + bw - 6, yy - 4, "#c9c3b5", 1.4))
    b.append(rect(bx + bw / 2 - 12, by + 8, 24, bh - 16, "#ffffff", "#ffffff", 3, 0))
    b.append(f'<rect x="{bx + bw / 2 - 3}" y="{by + 14}" width="6" height="{bh - 34}" rx="3" fill="#fff" stroke="{INK2}" stroke-width="1.2"/>'
             + circle(bx + bw / 2, by + bh - 16, 5, ACC, INK2, 1.2) + line(bx + bw / 2, by + 36, bx + bw / 2, by + bh - 18, ACC, 3))
    b.append(text(bx + bw / 2, by - 30, "百葉箱", 16, INK, 700, "middle"))
    # 高さ
    hx = X0 + 40; hy = by + bh - 16
    b.append(line(hx, gY, hx, hy, TEAL, 2) + line(hx - 7, gY, hx + 7, gY, TEAL, 2) + line(hx - 7, hy, hx + 7, hy, TEAL, 2)
             + line(hx + 7, hy, bx + bw / 2 - 14, hy, TEAL, 1, "3 3"))
    b.append(f'<text x="{hx - 10}" y="{(gY + hy) / 2}" font-size="15" fill="{TEAL_D}" font-weight="700" text-anchor="middle" transform="rotate(-90 {hx - 10} {(gY + hy) / 2})">1.2〜1.5 m</text>')
    # ポイント
    px = bx + bw + 26
    pts = [("1", ["地面から", "1.2〜1.5 m の高さ"]), ("2", ["温度計に日光が", "当たらない（日かげ）"]), ("3", ["風通しがよい", "（すき間のある板）"]), ("4", ["同じ場所で、決めた", "時こくにはかる"])]
    for i, (n, rows) in enumerate(pts):
        yy = 168 + i * 56
        b.append(badge(px + 10, yy - 5, n, TEAL, "#fff", 14) + lines(px + 26, yy, rows, 15, INK, 1.3))
    # 同じ時こくでも、場所で目もりが変わる
    t = 14
    vals = [("百葉箱の中", reading("hare", t, "hyou"), "正しい気温"), ("日なた", reading("hare", t, "hinata"), "高く出る"), ("地面の近く", reading("hare", t, "jimen"), "高く出る")]
    b.append(text(X0 + 18, 440, "晴れの日の午後2時、温度計の目もりは…", 16, INK, 700))
    for i, (nm, v, note) in enumerate(vals):
        cx = X0 + 18 + i * 128
        ok = i == 0
        b.append(rect(cx, 454, 118, 108, TEAL_L if ok else ACC_L, TEAL if ok else ACC, 8, 1.4))
        b.append(text(cx + 59, 480, nm, 15, INK, 700, "middle"))
        b.append(text(cx + 59, 522, f"{r0(v)}℃", 30, TEAL_D if ok else ACC, 700, "middle"))
        b.append(text(cx + 59, 549, note, 15, TEAL_D if ok else ACC, 700, "middle"))
    b.append(text(X0 + 18, 586, "目もりは、液の先と目の高さを同じにして真横から読む。", 14, INK2))
    b.append(text(X0 + 18, 608, "注意：太陽をちょくせつ見ない（目をいためる）。", 14, ACC, 700))
    return svg("".join(b), "天気と1日の気温のグラフ・気温のはかり方",
               "グラフはこのシミュレーターの目安（春〜秋のおだやかな日）。季節や場所で実際の数値は変わる。")


FIGS = [
    dict(svg=fig1, alt="天気と気温のしくみの図。晴れの日は日光が地面をあたため、地面が空気をあたためるので1日の気温の差が大きく（約11℃）、くもり・雨の日は雲が日光をさえぎるので差が小さいこと、太陽がいちばん高い正午より少しおくれて午後2時ごろに気温がいちばん高くなることを示す。右は、ふたなしの入れ物の水がじょう発して水じょう気になり、ふたありのラップの内側や氷水のコップの外側で水てきにもどる（結ろ）ようすの図。",
         caption="天気と気温・水のゆくえのしくみ。晴れの日は地面から空気があたたまり、水はじょう発して空気中に入り、冷やされると水てきにもどる。"),
    dict(svg=fig2, alt="晴れ・くもり・雨の日の1日の気温の変わり方を折れ線グラフにした図（晴れは午後2時ごろに約23℃でいちばん高い山の形、くもりはなだらか、雨はほぼ平ら）と、百葉箱を使った気温の正しいはかり方（地面から1.2〜1.5 m・日かげ・風通しがよい所）のまとめ。晴れの日の午後2時に百葉箱・日なた・地面の近くではかった温度計の目もりのちがいもくらべている。",
         caption="天気と1日の気温のグラフと、気温の正しいはかり方。晴れの日は山の形、くもり・雨の日は変わり方が小さい。"),
]
