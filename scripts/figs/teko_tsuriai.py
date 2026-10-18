"""てこのつり合い（teko-tsuriai・小6 てこの規則性）の授業用の図
数値はシミュ（scripts/rika/sims_chikara.py の teko-tsuriai の JS）と同じ：おもり1こ10g、目盛り1〜6、
てこをかたむけるはたらき＝重さ(g)×支点からのきょり(目盛り)、1つの目盛りに100g（10こ）まで。"""
from figlib import *

CAP = 10                      # 1つの目盛りに10こ（100g）まで（シミュの CAP）


def hataraki(a):
    """シミュの sum()：a[d]＝目盛り d につるした10gのおもりの数"""
    return sum(a[d] * 10 * d for d in range(1, 7))


def omori(x, y, n, fill, stroke, w=40, h=18, gap=3):
    """目盛りの下につるす10gのおもり n こ（上の端 y）"""
    out = [line(x, y, x, y + 8, INK2, 1.6)]
    for i in range(n):
        out.append(rect(x - w / 2, y + 8 + i * (h + gap), w, h, fill, stroke, 3, 1.4))
    return "".join(out)


def vdim_h(x1, x2, y, color, label, size=16):
    """横向きの寸法線（両はしに短い縦線）＋下にラベル"""
    return (line(x1, y, x2, y, color, 1.8) + line(x1, y - 7, x1, y + 7, color, 1.8) + line(x2, y - 7, x2, y + 7, color, 1.8)
            + text((x1 + x2) / 2, y + 24, label, size, color, 700, "middle"))


def fig1():
    CX, CY, SP = 600, 222, 72
    L = [0] * 7; R = [0] * 7
    L[4] = 3                   # シミュのはじめの状態：左の4の目盛りに30g
    R[6] = 2                   # 右の6の目盛りに20gをつるすとつり合う
    l, r = hataraki(L), hataraki(R)
    assert l == r == 120
    b = []
    # 台と支柱
    b.append(rect(CX - 90, 398, 180, 12, "#cfc9bb", "#cfc9bb", 4))
    b.append(f'<rect x="{CX - 6}" y="{CY}" width="12" height="{398 - CY}" fill="#d9d4c7"/>')
    # 棒と目盛り
    b.append(rect(CX - 6 * SP - 20, CY - 8, 12 * SP + 40, 16, "#eceae4", INK2, 5, 1.6))
    for d in range(1, 7):
        for s in (-1, 1):
            x = CX + s * d * SP
            b.append(line(x, CY - 8, x, CY + 8, INK2, 1.6))
            b.append(text(x, CY - 18, str(d), 19, INK, 700, "middle"))
            b.append(circle(x, CY + 13, 3.6, CARD, INK2, 1.4))
    b.append(circle(CX, CY, 9, INK, INK, 0) + circle(CX, CY, 3.5, "#fff", "#fff", 0))
    b.append(text(CX + 16, CY + 44, "支点", 18, INK, 700))
    b.append(text(CX - 6 * SP, CY - 50, "左のうで", 17, TEAL, 700, "middle"))
    b.append(text(CX + 6 * SP, CY - 50, "右のうで", 17, ACC, 700, "middle"))
    # おもり
    for s, a, fill, stroke, col in [(-1, L, TEAL_L, TEAL, TEAL), (1, R, ACC_L, ACC, ACC)]:
        for d in range(1, 7):
            if a[d]:
                x = CX + s * d * SP
                b.append(omori(x, CY + 17, a[d], fill, stroke))
                b.append(text(x, CY + 110, f"{a[d] * 10}g", 19, col, 700, "middle"))
    # 支点からのきょり
    b.append(vdim_h(CX - 4 * SP, CX, CY + 138, TEAL, "支点からのきょり 4"))
    b.append(vdim_h(CX, CX + 6 * SP, CY + 138, ACC, "支点からのきょり 6"))
    # 左右のはたらき
    b.append(rect(60, 424, 500, 96, TEAL_L, TEAL, 10, 1.4))
    b.append(text(310, 455, "左のうでをかたむけるはたらき", 17, TEAL_D, 700, "middle"))
    b.append(text(310, 500, f"30g × 4 ＝ {l}", 30, INK, 700, "middle"))
    b.append(rect(640, 424, 500, 96, ACC_L, ACC, 10, 1.4))
    b.append(text(890, 455, "右のうでをかたむけるはたらき", 17, ACC, 700, "middle"))
    b.append(text(890, 500, f"20g × 6 ＝ {r}", 30, INK, 700, "middle"))
    b.append(text(600, 486, "＝", 36, INK, 700, "middle"))
    # きまり
    b.append(rect(60, 540, 1080, 78, GOLD_L, GOLD, 10, 1.4))
    b.append(text(600, 573, "てこをかたむけるはたらき ＝ おもりの重さ × 支点からのきょり", 22, INK, 700, "middle"))
    b.append(text(600, 604, "左右のはたらきが等しいとき、てこは水平につり合う（左が大きいと左に、右が大きいと右にかたむく）", 16, INK2, anchor="middle"))
    return svg("".join(b), "てこのつり合いのしくみ（実験用てこ）",
               "おもりは1こ10g。棒の重さは左右で同じなので、計算に入れない（シミュレーションと同じ）。")


def fig2():
    b = []
    # ---- 左：はたらき120とつり合うおもり（反比例）
    k = hataraki([0, 0, 0, 0, 3, 0, 0])          # 左の4に30g ＝ 120
    x0, y0, sw, sc = 100, 530, 70, 2.6
    b.append(text(60, 122, f"左の4に30g（はたらき{k}）とつり合うのは？", 19, INK, 700))
    b.append(text(60, 148, "右の目盛りごとに、つり合うおもりの重さ", 16, INK2))
    b.append(axes(x0, y0, 6 * sw, 320, "", "重さ（g）",
                  [(sw * (d - 0.5), str(d)) for d in range(1, 7)],
                  [(v * sc, str(v)) for v in range(0, 121, 20)], 15))
    for d in range(1, 7):
        w = k / d                                   # 重さ×きょり＝120
        cx = x0 + sw * (d - 0.5); hgt = w * sc
        ok = (w <= CAP * 10) and abs(w / 10 - round(w / 10)) < 1e-9   # 10gのおもり・100gまでで作れるか
        if ok:
            b.append(rect(cx - 22, y0 - hgt, 44, hgt, ACC_L, ACC, 3, 1.6))
        else:
            b.append(f'<rect x="{cx - 22:.1f}" y="{y0 - hgt:.1f}" width="44" height="{hgt:.1f}" rx="3" fill="#faf1ee" stroke="{ACC}" stroke-width="1.6" stroke-dasharray="5 4"/>')
        b.append(text(cx, y0 - hgt - 9, f"{w:g}g", 17, ACC, 700, "middle"))
        b.append(text(cx, y0 + 48, f"{w:g}×{d}", 14, INK2, anchor="middle"))
    b.append(text(x0 + 3 * sw, y0 + 74, "右の目盛り（支点からのきょり）", 15, INK, anchor="middle"))
    b.append(text(395, 262, "きょりが2倍になると、", 17, INK, 700, "middle"))
    b.append(text(395, 288, "重さは半分になる", 17, INK, 700, "middle"))
    b.append(text(395, 316, f"重さ×きょり は、どれも{k}", 16, TEAL_D, 700, "middle"))
    b.append(lines(262, 352, ["点線：1の目盛りは100gをこえる。", "5の目盛りの24gは、10gの", "おもりでは作れない。"], 14, MUTED, 1.45))
    # ---- 右：身の回りのてこ
    b.append(text(606, 122, "身の回りのてこ（支点・力点・作用点）", 19, INK, 700))
    lx = 610
    b.append(f'<path d="M{lx + 8},{140} l-9,16 h18z" fill="{INK}"/>' + text(lx + 22, 154, "支点", 15, INK, 700))
    b.append(circle(lx + 92, 148, 8, ACC, ACC, 0) + text(lx + 106, 154, "力点（力を加える所）", 15, ACC, 700))
    b.append(f'<rect x="{lx + 270}" y="140" width="16" height="16" fill="{TEAL}"/>' + text(lx + 294, 154, "作用点（物に力がはたらく所）", 15, TEAL, 700))
    rows = [("支点が真ん中", "はさみ・くぎぬき", {"力": 640, "支": 820, "作": 880},
             ["力点を支点から遠くすると、", "小さな力で大きな力が出る"]),
            ("作用点が真ん中", "せんぬき", {"支": 640, "作": 705, "力": 880},
             ["力点を支点から遠くすると、", "小さな力で大きな力が出る"]),
            ("力点が真ん中", "ピンセット", {"支": 640, "力": 718, "作": 880},
             ["作用点にはたらく力が小さく", "なり、やさしくつまめる"])]
    for i, (nm, tools, P, note) in enumerate(rows):
        c = 236 + i * 132
        b.append(rect(600, c - 58, 552, 116, CARD, LINE, 10))
        b.append(rect(625, c - 11, 270, 10, "#d9d4c7", INK2, 4, 1.2))
        x = P["支"]; b.append(f'<path d="M{x},{c - 1} l-13,22 h26z" fill="{INK}"/>' + text(x, c + 44, "支点", 15, INK, 700, "middle"))
        x = P["力"]; b.append(circle(x, c - 6, 10, ACC, ACC, 0) + text(x, c + 44, "力点", 15, ACC, 700, "middle"))
        x = P["作"]; b.append(f'<rect x="{x - 9}" y="{c - 15}" width="18" height="18" fill="{TEAL}"/>' + text(x, c + 44, "作用点", 15, TEAL, 700, "middle"))
        b.append(text(918, c - 24, nm, 18, INK, 700))
        b.append(text(918, c + 1, tools, 16, INK))
        b.append(lines(918, c + 26, note, 14.5, INK2, 1.4))
    return svg("".join(b), "てこのきまりと身の回りのてこ（まとめ）",
               "つり合うとき：左の（重さ×きょり）＝右の（重さ×きょり）。きょりと重さは反比例の関係。")


FIGS = [
    dict(svg=fig1, alt="てこのつり合いのしくみの図。実験用てこの左の4の目盛りに30g、右の6の目盛りに20gのおもりをつるすと、左のうでをかたむけるはたらき30×4＝120と右のはたらき20×6＝120が等しくなり、水平につり合うことを示す。てこをかたむけるはたらき＝おもりの重さ×支点からのきょり。",
         caption="てこのつり合いのしくみ。左右の「おもりの重さ×支点からのきょり」が等しいとき、てこは水平につり合う。"),
    dict(svg=fig2, alt="てこのきまりのまとめ図。左の4に30g（はたらき120）とつり合う右のおもりは、目盛り1で120g・2で60g・3で40g・4で30g・5で24g・6で20gになる（きょりと重さは反比例）。はさみ・くぎぬき（支点が真ん中）、せんぬき（作用点が真ん中）、ピンセット（力点が真ん中）の支点・力点・作用点のならび方。",
         caption="てこのきまりのまとめ。きょりが2倍になると、つり合う重さは半分。身の回りの道具の支点・力点・作用点。"),
]
