"""光と音のせいしつ（hikari-oto・小3）の授業用の図。数値はページのシミュと同じ式：
  かがみ：日光は左上から同じ向き SD＝(0.55,1)、はね返りは鏡の法線で計算（シミュの aim/refl と同じ）。まと18℃＋光1まい5℃（T0・DT）。
  虫めがね：直径 D＝6 cm、光が集まるきょり F＝15 cm、明るい部分の直径＝D|F−d|/F＋d×0.00931、明るさ＝0.9×(D÷直径)²。
  音：ふるえの大きさ＝たたく強さ×exp(−t/τ)（トライアングル τ＝1.5秒）、手でおさえると τ＝0.05秒で止まる。"""
import math
from figlib import *

T0, DT = 18, 5
D, F, TH, TRN = 6.0, 15.0, 0.00931, 0.9
TAU, FV = 1.5, 9


def spot(d): return D * abs(F - d) / F + d * TH          # cm
def conc(d): return TRN * (D / spot(d)) ** 2


def fmt_d(s): return f"約{s * 10:.1f} mm" if s < 1 else f"約{s:.1f} cm"


def fmt_c(c):
    if c < 10: return f"約{c:.1f}倍"
    if c < 100: return f"約{round(c)}倍"
    if c < 1000: return f"約{round(c / 10) * 10}倍"
    return f"約{round(c / 100) * 100:,}倍"


def sun(x, y, r=24):
    out = [f'<circle cx="{x}" cy="{y}" r="{r * 1.9}" fill="{SUN}" opacity=".3"/>', circle(x, y, r, SUN, GOLD, 1.6)]
    for k in range(8):
        a = k * math.pi / 4
        out.append(line(x + math.cos(a) * (r + 6), y + math.sin(a) * (r + 6), x + math.cos(a) * (r + 16), y + math.sin(a) * (r + 16), GOLD, 2.4))
    return "".join(out)


def unit(v):
    l = math.hypot(*v); return (v[0] / l, v[1] / l)


def fig1():
    b = []
    # ===== 左：かがみで日光をはね返す =====
    X0, X1, Y0, GY = 48, 700, 100, 560
    b.append(f'<g clip-path="url(#sky)"><rect x="{X0}" y="{Y0}" width="{X1 - X0}" height="{GY - Y0}" fill="#e9f2f7"/>'
             f'<rect x="{X0}" y="{GY}" width="{X1 - X0}" height="{52}" fill="#d8cfb8"/>')
    SD = unit((0.55, 1.0))
    for k in range(-6, 14):                           # 日光（平行な光）
        x = 40 + k * 52
        b.append(line(x, Y0, x + SD[0] / SD[1] * (GY - Y0), GY, "#e7c65a", 1.2))
    WX = 610; TGT = (WX, 300)
    b.append(rect(WX, 168, 50, GY - 168, "#8b939b", "#6b737b", 0, 1) + f'<rect x="{WX}" y="168" width="6" height="{GY - 168}" fill="#6b737b"/>')
    beams, mirrors = [], []
    for i, mx in enumerate((190, 300, 410)):
        m = (mx, 506)
        r = unit((TGT[0] - m[0], TGT[1] - m[1]))
        n = unit((r[0] - SD[0], r[1] - SD[1]))
        t = (-n[1], n[0])
        p0, p1 = (m[0] - t[0] * 30, m[1] - t[1] * 30), (m[0] + t[0] * 30, m[1] + t[1] * 30)
        L = 600
        beams.append(f'<polygon points="{p0[0] - SD[0] * L:.1f},{p0[1] - SD[1] * L:.1f} {p0[0]:.1f},{p0[1]:.1f} {p1[0]:.1f},{p1[1]:.1f} {p1[0] - SD[0] * L:.1f},{p1[1] - SD[1] * L:.1f}" fill="{SUN}" opacity=".28"/>')
        h0 = (WX, p0[1] + r[1] / r[0] * (WX - p0[0])); h1 = (WX, p1[1] + r[1] / r[0] * (WX - p1[0]))
        beams.append(f'<polygon points="{p0[0]:.1f},{p0[1]:.1f} {h0[0]:.1f},{h0[1]:.1f} {h1[0]:.1f},{h1[1]:.1f} {p1[0]:.1f},{p1[1]:.1f}" fill="{SUN}" opacity=".45"/>')
        s = (m[0] - SD[0] * 260, m[1] - SD[1] * 260)
        beams.append(arrow(s[0], s[1], m[0] - SD[0] * 70, m[1] - SD[1] * 70, "gold", 2.6) + line(m[0] - SD[0] * 70, m[1] - SD[1] * 70, m[0], m[1], GOLD, 2.6))
        q = (m[0] + r[0] * 130, m[1] + r[1] * 130)
        beams.append(arrow(m[0], m[1], q[0], q[1], "gold", 2.6) + line(q[0], q[1], TGT[0], TGT[1], GOLD, 2.6))
        mirrors.append(line(m[0], m[1] + 4, m[0], GY, "#78716c", 3) + line(p0[0] - n[0] * 4, p0[1] - n[1] * 4, p1[0] - n[0] * 4, p1[1] - n[1] * 4, "#3b3f46", 7)
                       + line(p0[0], p0[1], p1[0], p1[1], "#cfe3ef", 4.5) + text(m[0], GY + 30, "①②③"[i], 20, INK, 700, "middle"))
    b += beams + mirrors
    b.append(f'<ellipse cx="{WX + 3}" cy="{TGT[1]}" rx="12" ry="40" fill="#fffbd0" opacity=".95"/>')
    b.append(circle(WX + 8, TGT[1], 26, "none", ACC, 3) + circle(WX + 8, TGT[1], 13, "none", ACC, 3))
    b.append('</g>')
    b.append(rect(X0, Y0, X1 - X0, 512, "none", LINE, 12))
    b.append(sun(100, 152))
    b.append(text(70, 214, "日光は まっすぐ進む", 17, INK, 700, stroke="#e9f2f7", stroke_width=5, paint_order="stroke"))
    b.append(text(WX - 8, 210, "日かげのかべ", 16, INK, 700, "end", stroke="#e9f2f7", stroke_width=5, paint_order="stroke"))
    b.append(text(WX - 40, 254, "まと", 18, ACC, 700, "end", stroke="#e9f2f7", stroke_width=5, paint_order="stroke"))
    b.append(text(452, 420, "かがみで", 16, INK, 700, stroke="#e9f2f7", stroke_width=5, paint_order="stroke")
             + text(452, 442, "はね返した光", 16, INK, 700, stroke="#e9f2f7", stroke_width=5, paint_order="stroke"))
    b.append(text(68, 596, "かがみ", 16, INK, 700))
    b.append(rect(236, 114, 300, 64, "#ffffff", ACC, 8, 1.6))
    b.append(text(250, 140, "3まい分の光が まとで重なる", 16, INK, 700) + text(250, 164, f"→ とても明るく、あたたかい（約{T0 + 3 * DT}℃）", 15, ACC, 700))
    # ===== 右：糸電話 =====
    x0 = 724
    b.append(rect(x0, 100, 428, 512, CARD, LINE, 12))
    b.append(text(x0 + 22, 136, "音は ふるえで つたわる（糸電話）", 19, INK, 700))
    cy = 250
    b.append(f'<polygon points="780,{cy - 36} 850,{cy - 18} 850,{cy + 18} 780,{cy + 36}" fill="#f4efe2" stroke="{INK2}" stroke-width="2"/>')
    b.append(f'<polygon points="1096,{cy - 36} 1026,{cy - 18} 1026,{cy + 18} 1096,{cy + 36}" fill="#f4efe2" stroke="{INK2}" stroke-width="2"/>')
    b.append(line(850, cy, 1026, cy, INK2, 2))
    b.append(poly([(850 + k * 4, cy + (5 if k % 2 else -5)) for k in range(45)], TEAL, 1.6))
    for k in range(3):                                # 音の波（右へ進む）
        for xx in (730 + k * 12, 1100 + k * 12):
            b.append(f'<path d="M{xx},{cy - 20} A20,20 0 0 1 {xx},{cy + 20}" fill="none" stroke="{TEAL}" stroke-width="2.2"/>')
    for xx in (851, 1025):
        b.append(line(xx, cy - 24, xx, cy + 24, ACC, 3, "4 3"))
    b.append(text(800, cy - 50, "話す人", 16, INK, 700, "middle") + text(1076, cy - 50, "聞く人", 16, INK, 700, "middle"))
    b.append(text(938, cy - 16, "糸がふるえる", 15, TEAL, 700, "middle"))
    b.append(text(938, cy + 50, "（糸はピンとはる）", 14, INK2, anchor="middle"))
    steps = ["声で、コップのそこが ふるえる", "ふるえが 糸を つたわる", "聞く人のコップが ふるえる", "耳にとどいて 聞こえる"]
    for i, s in enumerate(steps):
        yy = 344 + i * 46
        b.append(badge(x0 + 40, yy - 6, str(i + 1), TEAL, "#fff", 15) + text(x0 + 62, yy, s, 17, INK))
        if i < 3: b.append(arrow(x0 + 40, yy + 9, x0 + 40, yy + 28, "teal", 2))
    b.append(rect(x0 + 20, 528, 388, 64, ACC_L, ACC, 8, 1.4))
    b.append(text(x0 + 36, 554, "糸をつまむと、そこで ふるえが止まり、", 16, INK, 700) + text(x0 + 36, 578, "聞く人には 聞こえない。", 16, INK, 700))
    return svg("".join(b), "光と音のせいしつ（しくみ）",
               "太陽を直せつ見ない。はね返した日光を人の顔に当てない。（大きさ・きょりは実際とちがう）",
               defs=f'<clipPath id="sky"><rect x="{X0}" y="{Y0}" width="{X1 - X0}" height="512" rx="12"/></clipPath>')


def wave(x0, y0, w, h, pw, damp=None):
    pts = []
    for k in range(0, 601):
        t = 2.5 * k / 600
        a = pw * math.exp(-t / TAU)
        if damp is not None and t > damp: a *= math.exp(-(t - damp) / 0.05)
        pts.append((x0 + w * k / 600, y0 - a / 5 * (h / 2 - 3) * math.sin(2 * math.pi * FV * t)))
    return poly(pts, TEAL, 1.8)


def fig2():
    b = []
    cols = [(48, "1", "かがみの数と まと"), (424, "2", "虫めがねで 日光を集める"), (800, "3", "音の大きさと ふるえ")]
    for x, no, t in cols:
        b.append(rect(x, 100, 352, 512, CARD, LINE, 12) + badge(x + 28, 132, no, TEAL, "#fff", 17) + text(x + 52, 139, t, 19, INK, 700))
    # ① かがみ
    x = 48
    b.append(text(x + 20, 182, "まとに当てた光", 15, INK2) + text(x + 332, 182, "温度（3分後のめやす）", 15, INK2, anchor="end"))
    words = ["いちばん暗い", "明るい", "もっと明るい", "とても明るい"]
    for k in range(4):
        yy = 204 + k * 74
        v = T0 + DT * k
        b.append(text(x + 20, yy + 26, f"{k}まい", 20, INK, 700))
        bw = 170 * (v - 10) / 30
        b.append(rect(x + 92, yy + 6, 170, 30, "#f1eee6", LINE, 4, 1) + rect(x + 92, yy + 6, bw, 30, "#f2c14e" if k else "#d6d0c2", "none", 4, 0))
        b.append(text(x + 332, yy + 30, f"約{v}℃", 20, ACC if k else INK2, 700, "end"))
        b.append(text(x + 92, yy + 58, words[k] + ("（日かげのまま）" if k == 0 else ""), 15, INK2))
    b.append(lines(x + 20, 520, ["光を重ねるほど、まとは", "明るく、あたたかくなる。"], 17, INK, 1.5))
    # ② 虫めがね
    x = 424
    b.append(text(x + 20, 178, "紙までのきょりを変えると…", 15, INK2))
    sc = 20
    for k, d in enumerate((7, 13, 15)):
        yy = 196 + k * 104
        s, c = spot(d), conc(d)
        b.append(rect(x + 20, yy, 96, 92, "#2b2f35", "none", 6, 0))
        rr = max(1.6, s * sc / 2)
        col = "#cdbb6a" if c < 5 else ("#fff0a0" if c < 200 else "#ffffff")
        if c >= 30: b.append(f'<circle cx="{x + 68}" cy="{yy + 46}" r="{rr + 7:.1f}" fill="{SUN}" opacity=".35"/>')
        b.append(circle(x + 68, yy + 46, rr, col, "none", 0))
        state = "あたたかい" if c < 5 else ("とても あつい" if c < 30 else ("黒い紙はこげる" if c < 200 else "白い紙もこげる"))
        b.append(text(x + 132, yy + 24, f"{d} cm：明るい部分 {fmt_d(s)}", 15.5, INK, 700))
        b.append(text(x + 132, yy + 50, f"明るさ 日光の{fmt_c(c)}", 15.5, INK))
        b.append(text(x + 132, yy + 76, state, 15.5, ACC if c >= 30 else INK2, 700))
    b.append(lines(x + 20, 532, ["明るい部分が小さいほど、", "明るく、あつくなる。"], 17, INK, 1.5))
    b.append(text(x + 20, 594, "集めた光を人や服に当てない", 15, ACC, 700))
    # ③ 音
    x = 800
    rows = [("よわく たたく", 2, None, "ふるえ 小さい → 音 小さい"), ("強く たたく", 5, None, "ふるえ 大きい → 音 大きい"),
            ("強くたたいて 手でおさえる", 5, 0.6, "ふるえが止まる → 音も止まる")]
    for k, (nm, pw, dmp, res) in enumerate(rows):
        yy = 168 + k * 124
        b.append(text(x + 20, yy + 6, nm, 16, INK, 700))
        b.append(rect(x + 20, yy + 14, 312, 62, "#f4f7f9", LINE, 6, 1) + line(x + 26, yy + 45, x + 326, yy + 45, LINE, 1))
        b.append(wave(x + 26, yy + 45, 300, 58, pw, dmp))
        b.append(text(x + 20, yy + 98, res, 15.5, TEAL_D if k < 2 else ACC, 700))
    b.append(text(x + 20, 558, "音が出ている物は ふるえている。", 17, INK, 700))
    b.append(text(x + 20, 594, "トライアングルの例（ゆっくりにした図）", 14, INK2))
    return svg("".join(b), "光と音のせいしつ（まとめ）",
               "温度は日かげのまと18℃に光を当てたときのめやす。虫めがねは直径6 cm・光が集まるきょり15 cm。")


FIGS = [
    dict(svg=fig1, alt="小3理科「光と音の性質」のしくみ図。太陽の光がまっすぐ進み、3まいのかがみではね返した日光を日かげのかべのまとに重ねると明るくあたたかくなるようすと、糸電話で声によるコップのふるえが糸をつたわって聞く人に届き、糸をつまむと聞こえなくなることを示す。",
         caption="日光はまっすぐ進み、かがみではね返せる。音は物のふるえでつたわる。"),
    dict(svg=fig2, alt="光と音の性質のまとめ。かがみの数（0〜3まい）とまとの明るさ・温度のめやす（約18℃〜約33℃）、虫めがねと紙のきょり（7 cm・13 cm・15 cm）ごとの明るい部分の大きさと明るさ（黒い紙がこげる）、よわくたたいた・強くたたいた・手でおさえたときの音のふるえのグラフ。",
         caption="光を重ねる・集めるほど明るく、あたたかい。音が大きいほど物のふるえは大きい。"),
]
