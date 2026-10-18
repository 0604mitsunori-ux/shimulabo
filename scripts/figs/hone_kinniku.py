"""ほねときん肉（hone-kinniku・小4）の授業用の図。
図1のうで・図2の全身のほねは、ページのシミュ（scripts/rika/sims_sho4_a.py の JS_HONE の drawArm／drawSkel）と同じ座標・同じ式
（armG：ひじの角度 a から 下うでの向き f＝(sin(180°−a), cos(180°−a))、きん肉の太さ hwI・hwO）で描く。
曲げるとき＝内側のきん肉がちぢみ外側がゆるむ／のばすとき＝外側がちぢみ内側がゆるむ。小4の言葉で書く。"""
import math
from figlib import *

SKIN, SKIN_L, BONE, BONE_L, TEND, TEND_L = "#fde4cc", "#d9a877", "#fbf8ef", "#a8a29e", "#f5f5f4", "#a8a29e"   # シミュと同じ（はだ・ほね・けん）
RELAX = "#f3c2b8"                                   # ゆるんでいるきん肉（ACC のうすい色）
S, E, LF = (150, 86), (150, 254), 140              # かた・ひじ・下うでの長さ（シミュの座標）


def V(x, y): return (x, y)
def ad(p, d, k=1.0): return (p[0] + d[0] * k, p[1] + d[1] * k)
def dst(a, b): return math.hypot(a[0] - b[0], a[1] - b[1])


def mix(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]; b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(a, b))


def seg(a, b, col, w):
    return f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{col}" stroke-width="{w:.1f}" stroke-linecap="round"/>'


def bone(a, b, w, fill=BONE, ol=BONE_L):
    return (seg(a, b, ol, w + 2.4) + circle(a[0], a[1], w * 0.72 + 1.2, ol, ol, 0) + circle(b[0], b[1], w * 0.72 + 1.2, ol, ol, 0)
            + seg(a, b, fill, w) + circle(a[0], a[1], w * 0.72, fill, fill, 0) + circle(b[0], b[1], w * 0.72, fill, fill, 0))


def tendon(a, b): return seg(a, b, TEND_L, 5) + seg(a, b, TEND, 3)


def spindle(P1, P2, hw, col, t1, t2):
    """シミュの spindle：両はしにけん、まん中がふくらんだきん肉"""
    L = dst(P1, P2); d = ((P2[0] - P1[0]) / L, (P2[1] - P1[1]) / L); n = (-d[1], d[0])
    Q1, Q2 = ad(P1, d, t1), ad(P2, d, -t2); M = ((Q1[0] + Q2[0]) / 2, (Q1[1] + Q2[1]) / 2)
    out = []
    if t1 > 0: out.append(tendon(P1, ad(Q1, d, 6)))
    if t2 > 0: out.append(tendon(ad(Q2, d, -6), P2))
    c1, c2 = ad(M, n, hw * 2), ad(M, n, -hw * 2)
    out.append(f'<path d="M{Q1[0]:.1f},{Q1[1]:.1f} Q{c1[0]:.1f},{c1[1]:.1f} {Q2[0]:.1f},{Q2[1]:.1f} Q{c2[0]:.1f},{c2[1]:.1f} {Q1[0]:.1f},{Q1[1]:.1f}Z" fill="{col}" stroke="#7f1d1d" stroke-opacity=".55" stroke-width="1.3"/>')
    for k in (-1, 0, 1):
        c = ad(M, n, k * hw)
        out.append(f'<path d="M{Q1[0]:.1f},{Q1[1]:.1f} Q{c[0]:.1f},{c[1]:.1f} {Q2[0]:.1f},{Q2[1]:.1f}" fill="none" stroke="#fff" stroke-opacity=".4" stroke-width="1"/>')
    return "".join(out), M


def jring(P, r):
    return f'<circle cx="{P[0]:.1f}" cy="{P[1]:.1f}" r="{r}" fill="none" stroke="{GREEN}" stroke-width="2.4" stroke-dasharray="5 4"/>'


def arm(ang, bend):
    """シミュの drawArm（ang＝ひじの角度、bend＝曲げているとき True）。戻り値：(SVG, 目印の点の辞書)"""
    cin = 1.0 if bend else 0.0
    p = math.radians(180 - ang); f = (math.sin(p), math.cos(p)); n = (f[1], -f[0]); Wr = ad(E, f, LF); gb = (180 - ang) / 135
    o = []
    for c, ex in [(SKIN_L, 3), (SKIN, 0)]:
        o.append(f'<ellipse cx="{S[0] - 4}" cy="{S[1] - 24}" rx="{52 + ex / 2}" ry="{32 + ex / 2}" fill="{c}"/>')
        o.append(seg((S[0], S[1] - 14), E, c, 70 + ex) + seg(E, Wr, c, 56 + ex))
    rot = math.degrees(math.atan2(f[1], f[0]))
    o.append(f'<g transform="translate({Wr[0]:.1f},{Wr[1]:.1f}) rotate({rot:.1f})"><ellipse cx="30" cy="0" rx="30" ry="22" fill="{SKIN}" stroke="{SKIN_L}" stroke-width="2"/>'
             f'<ellipse cx="18" cy="-21" rx="13" ry="8" transform="rotate(-28.6 18 -21)" fill="{SKIN}" stroke="{SKIN_L}" stroke-width="2"/></g>')
    o.append(f'<polygon points="{S[0] - 38},{S[1] - 30} {S[0] - 8},{S[1] - 16} {S[0] - 32},{S[1] + 34}" fill="{BONE}" stroke="{BONE_L}" stroke-width="1.3"/>')
    o.append(bone((S[0], S[1] + 2), (E[0], E[1] - 8), 14))
    e1, w1 = ad(E, f, 10), ad(Wr, f, -2)
    o.append(bone(ad(e1, n, 4.5), ad(w1, n, 5), 7) + bone(ad(e1, n, -4.5), ad(w1, n, -5), 7))
    Oi = (S[0] + 16, S[1] + 20); Ii = ad(ad(E, f, 34), n, 9); Li = dst(Oi, Ii); Li0 = dst(Oi, (E[0] + 9, E[1] + 34))
    Oo = (S[0] - 17, S[1] + 20); Bo = (S[0] - 17, E[1] - 30 + gb * 10); Io = ad(ad(E, n, -12), f, -5)
    hwI = 7 + 7 * cin + (1 - Li / Li0) * 9; hwO = 7 + 7 * (1 - cin) - gb * 2
    so, Mo = spindle(Oo, Bo, hwO, mix(RELAX, ACC, 1 - cin), 10, 0)
    o.append(so + tendon(Bo, Io))
    si, Mi = spindle(Oi, Ii, hwI, mix(RELAX, ACC, cin), 10, 12)
    o.append(si)
    o.append(jring(E, 21) + jring(S, 17))
    tip = ad(Wr, f, 66); dr = 1 if bend else -1
    return "".join(o), dict(Mi=Mi, Mo=Mo, E=E, S=S, tip=tip, tip2=ad(tip, n, dr * 40), bone=(S[0], 150), fore=ad(E, f, 70))


def lab(x, y, w, rows, col, to):
    """シミュの lbl：白い札＋引き出し線。rows＝[(文字, 大きさ, 色, 太字)]"""
    h = 12 + len(rows) * 22
    o = [rect(x, y, w, h, "#fff", col, 7, 1.6)]
    sx = x + w if to[0] > x + w else (x if to[0] < x else x + w / 2)
    sy = y + h if to[1] > y + h else (y if to[1] < y else y + h / 2)
    o.append(line(sx, sy, to[0], to[1], col, 1.5) + circle(to[0], to[1], 3.2, col, col, 0))
    for i, (s, sz, c, bd) in enumerate(rows):
        o.append(text(x + 10, y + 26 + i * 22, s, sz, c, 700 if bd else 400))
    return "".join(o)


def fig1():
    b = []
    for k, (px, ang, bend, title) in enumerate([(48, 70, True, "うでを曲げるとき"), (440, 150, False, "うでをのばすとき")]):
        b.append(rect(px, 100, 372, 516, CARD, LINE, 12))
        b.append(text(px + 18, 134, title, 21, INK, 700))
        tx, ty = px + 20, 128
        T = lambda P: (tx + P[0], ty + P[1])
        g, pt = arm(ang, bend)
        b.append(f'<g transform="translate({tx},{ty})">{g}</g>')
        a0, a1 = T(pt["tip"]), T(pt["tip2"])
        b.append(arrow(a0[0], a0[1], a1[0], a1[1], "teal", 3.4))
        if bend:
            b.append(lab(px + 226, 150, 132, [("内側のきん肉", 15, INK, True), ("ちぢむ", 19, ACC, True)], ACC, T(pt["Mi"])))
            b.append(lab(px + 12, 300, 112, [("外側のきん肉", 15, INK, True), ("ゆるむ", 19, MUTED, True)], "#94a3b8", T(pt["Mo"])))
            b.append(lab(px + 12, 178, 84, [("ほね", 15, INK, True), ("かたい", 14, MUTED, False)], BONE_L, T(pt["bone"])))
            b.append(lab(px + 12, 420, 124, [("関節（ひじ）", 15, GREEN, True), ("曲がるところ", 14, MUTED, False)], GREEN, T((E[0] - 21, E[1] + 4))))
        else:
            b.append(lab(px + 238, 152, 120, [("内側のきん肉", 15, INK, True), ("ゆるむ", 19, MUTED, True)], "#94a3b8", T(pt["Mi"])))
            b.append(lab(px + 12, 300, 112, [("外側のきん肉", 15, INK, True), ("ちぢむ", 19, ACC, True)], ACC, T(pt["Mo"])))
            b.append(lab(px + 12, 420, 124, [("関節（ひじ）", 15, GREEN, True), ("曲がるところ", 14, MUTED, False)], GREEN, T((E[0] - 21, E[1] + 4))))
    # 右：まとめ
    x0 = 832
    b.append(text(x0, 134, "きん肉のようす", 19, INK, 700))
    b.append(table(x0, 148, ["うでの動き", "内側", "外側"], [["曲げる", "ちぢむ", "ゆるむ"], ["のばす", "ゆるむ", "ちぢむ"]], [112, 104, 104], 40, 17))
    b.append(lines(x0, 300, ["きん肉は、ちぢんでほねを", "引っぱり、体を動かす。", "きん肉は、ほねをおすことは", "できない。だから、曲げるときと", "のばすときで、はたらくきん肉が", "入れかわる。"], 16, INK, 1.5))
    for i, (sw, t) in enumerate([("c", "ちぢむ＝短く太くなる（かたい）"), ("r", "ゆるむ＝のばされる（やわらかい）"), ("j", "関節＝ほねとほねのつなぎ目")]):
        y = 476 + i * 34
        if sw == "c": b.append(f'<ellipse cx="{x0 + 14}" cy="{y - 6}" rx="14" ry="8" fill="{ACC}"/>')
        elif sw == "r": b.append(f'<ellipse cx="{x0 + 14}" cy="{y - 6}" rx="14" ry="5" fill="{RELAX}" stroke="#7f1d1d" stroke-opacity=".4"/>')
        else: b.append(f'<circle cx="{x0 + 14}" cy="{y - 6}" r="11" fill="none" stroke="{GREEN}" stroke-width="2.4" stroke-dasharray="5 4"/>')
        b.append(text(x0 + 38, y, t, 15, INK2))
    b.append(text(x0, 590, "きん肉のはしの白い部分＝けん", 15, MUTED))
    return svg("".join(b), "うでを曲げる・のばすときの、ほねときん肉",
               "曲げるときは内側、のばすときは外側のきん肉がちぢむ。図は、ほねときん肉を見やすくした模式図。")


J = dict(neck=(200, 106), waist=(200, 238), shL=(146, 126), shR=(254, 126), elL=(132, 204), elR=(268, 204), wrL=(124, 268), wrR=(276, 268),
         fiL=(119, 296), fiR=(281, 296), hiL=(181, 284), hiR=(219, 284), knL=(177, 368), knR=(223, 368), anL=(176, 436), anR=(224, 436))


def skeleton():
    """シミュの drawSkel と同じ座標"""
    o = []
    o.append(f'<ellipse cx="200" cy="56" rx="30" ry="34" fill="{BONE}" stroke="{BONE_L}" stroke-width="2"/>')
    o.append(f'<path d="M219,82 A19,13 0 0 1 181,82Z" fill="{BONE}" stroke="{BONE_L}" stroke-width="2"/>')
    o.append(circle(189, 56, 7, "#d6d3d1", "#d6d3d1", 0) + circle(211, 56, 7, "#d6d3d1", "#d6d3d1", 0) + '<polygon points="200,66 196,75 204,75" fill="#d6d3d1"/>')
    o.append(f'<path d="M194,250 C170,236 150,244 154,262 C158,280 172,290 184,296 L200,300 L216,296 C228,290 242,280 246,262 C250,244 230,236 206,250Z" fill="{BONE}" stroke="{BONE_L}" stroke-width="1.6"/>')
    o.append('<ellipse cx="188" cy="284" rx="6" ry="5" fill="#ece9e4"/><ellipse cx="212" cy="284" rx="6" ry="5" fill="#ece9e4"/>')
    o.append(f'<rect x="196" y="128" width="8" height="66" rx="3" fill="{BONE}" stroke="{BONE_L}" stroke-width="1.2"/>')
    for i, w in enumerate([28, 36, 41, 43, 42, 39, 34]):
        y = 132 + i * 11.5
        for s in (-1, 1):
            for sw, c in [(5.5, BONE_L), (3.5, BONE)]:
                o.append(f'<path d="M{200 + s * 6},{y} C{200 + s * (w + 8)},{y - 4} {200 + s * (w + 6)},{y + 18} {200 + s * 9},{y + 16}" fill="none" stroke="{c}" stroke-width="{sw}"/>')
    for y in range(96, 261, 9):
        o.append(f'<rect x="194" y="{y}" width="12" height="7" rx="2" fill="{BONE}" stroke="{BONE_L}" stroke-width="1.2"/>')
    o.append(bone((196, 121), (150, 119), 5) + bone((204, 121), (250, 119), 5))
    for s, oo in (("L", -1), ("R", 1)):
        sh, el, wr, fi = J["sh" + s], J["el" + s], J["wr" + s], J["fi" + s]
        o.append(bone(sh, el, 10))
        o.append(bone((el[0] - 3.5, el[1] + 6), (wr[0] - 3.5, wr[1] - 2), 4.5) + bone((el[0] + 3.5, el[1] + 6), (wr[0] + 3.5, wr[1] - 2), 4.5))
        for k in range(4):
            o.append(bone((wr[0] + (k - 1.5) * 3.4, wr[1] + 5), (fi[0] + (k - 1.5) * 5.2, fi[1] + 10), 2.4))
        o.append(bone((wr[0] - oo * 6, wr[1] + 5), (wr[0] - oo * 13, wr[1] + 19), 2.4))
        hi, kn, an = J["hi" + s], J["kn" + s], J["an" + s]
        o.append(bone(hi, kn, 12) + bone((kn[0], kn[1] + 8), an, 9) + bone((kn[0] + oo * 7, kn[1] + 12), (an[0] + oo * 7, an[1] - 4), 4))
        o.append(circle(kn[0], kn[1] - 2, 6.5, BONE, BONE_L, 1))
        o.append(bone((an[0], an[1] + 4), (an[0] + oo * 8, an[1] + 16), 6))
    for k, p in J.items():
        if k not in ("waist", "neck"):
            o.append(f'<circle cx="{p[0]}" cy="{p[1]}" r="7" fill="none" stroke="{GREEN}" stroke-width="2"/>')
    return "".join(o)


def fig2():
    b = []
    sc, tx, ty = 1.15, 100, 84
    T = lambda P: (tx + P[0] * sc, ty + P[1] * sc)
    b.append(f'<g transform="translate({tx},{ty}) scale({sc})">{skeleton()}</g>')
    G1, G2, G3 = GOLD, TEAL, GREEN
    for nm, wk, col, x, y, P in [("頭のほね", "のう（脳）を守る", G2, 470, 112, (229, 50)), ("むねのほね", "心ぞうや はい を守る", G2, 470, 228, (244, 158)),
                                 ("うでのほね", "うでを動かす", G3, 470, 330, (273, 236)), ("あしのほね", "体をささえる", G1, 470, 500, (226, 402)),
                                 ("せぼね", "体をささえる", G1, 48, 300, (193, 222)), ("こしのほね", "おなかの中を守る", G2, 48, 496, (162, 272))]:
        b.append(lab(x, y, 156 if x > 400 else 150, [(nm, 16, INK, True), (wk, 14, col, True)], BONE_L, T(P)))
    b.append(f'<circle cx="62" cy="600" r="8" fill="none" stroke="{GREEN}" stroke-width="2.3"/>' + text(78, 606, "＝関節（曲がるところ）", 16, GREEN, 700))
    # 右：はたらき・関節
    x0 = 676
    b.append(text(x0, 128, "ほねの3つのはたらき", 19, INK, 700) + text(1152, 128, "ほねは全身でおよそ200こ", 15, MUTED, anchor="end"))
    for i, (t, d, c) in enumerate([("1. 体をささえる", "せぼね・こしのほね・あしのほね", G1), ("2. 体の中を守る", "頭のほね→のう、むねのほね→心ぞう・はい", G2),
                                   ("3. 体を動かす", "きん肉に引っぱられて、関節で曲がる", G3)]):
        y = 142 + i * 66
        b.append(rect(x0, y, 476, 58, CARD, c, 8, 1.6))
        b.append(text(x0 + 14, y + 26, t, 17, c, 700) + text(x0 + 14, y + 49, d, 15, INK2))
    b.append(text(x0, 372, "体の曲がるところ（関節）", 19, INK, 700))
    b.append(table(x0, 384, ["曲がるところ", "つながっているほね"],
                   [["首・こし", "せぼね（小さなほねがたくさんつながる）"], ["かた", "うでのほねと、かたのほね"], ["ひじ", "うでのほね（上と下）"],
                    ["手首・ゆび", "手のほね（ゆびには関節がいくつもある）"], ["足のつけ根", "あしのほねと、こしのほね"], ["ひざ・足首", "あしのほね"]], [128, 348], 33, 15))
    return svg("".join(b), "体のほねと関節（ほねのはたらき）",
               "関節は、ほねとほねのつなぎ目にある。曲がらない所には、かたいほねが1本通っている。（図は模式図）")


FIGS = [
    dict(svg=fig1, alt="うでを曲げるときとのばすときの、ほねときん肉のようすをくらべた図。曲げるときはうでの内側のきん肉がちぢみ（太く、かたくなる）外側のきん肉がゆるみ、のばすときは外側のきん肉がちぢみ内側のきん肉がゆるむ。うでは、ほねとほねのつなぎ目の関節（ひじ）で曲がる。",
         caption="うでを曲げる・のばすときのきん肉。曲げるときは内側、のばすときは外側のきん肉がちぢんで、ほねを引っぱる。"),
    dict(svg=fig2, alt="人の全身のほねと関節の図。頭のほね（のうを守る）・むねのほね（心ぞうやはいを守る）・せぼね（体をささえる）・こしのほね・うでのほね・あしのほねと、かた・ひじ・手首・足のつけ根・ひざ・足首の関節を示し、ほねの3つのはたらき（ささえる・守る・動かす）と体の曲がるところの表をまとめている。",
         caption="体のほねと関節。ほねには、体をささえる・体の中を守る・体を動かすはたらきがある。"),
]
