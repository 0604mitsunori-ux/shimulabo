"""物と重さ（mono-omosa・小3）の授業用の図。
数値はシミュ（scripts/rika/sims_sho3_a.py の JS_OMOSA・BLOCKS）と同じ：
  ねん土 100 g（細かく分けたかけら 24・20・18・15・13・10 g）、アルミはく 8.9 g、
  1辺3cmの立方体（27 cm³）の重さ＝1 cm³あたりの重さ×27（小数第1位まで）。
  自動上皿はかりは、はり1回り500 g。"""
import math
from figlib import *

CLAY, CLAY_E = "#e8b88a", "#b4703a"
V = 27
BLOCKS = [("木", 0.5), ("プラスチック", 1.19), ("ゴム", 1.3), ("ガラス", 2.5), ("アルミニウム", 2.70), ("鉄", 7.87), ("どう", 8.96)]
BW = {n: round(r * V, 1) for n, r in BLOCKS}
PCS = [24, 20, 18, 15, 13, 10]
TAU = 2 * math.pi


def dial_scale(cx, py, g):
    """自動上皿はかり（1回り500 g）。py＝皿の上面"""
    b = [rect(cx - 85, py + 20, 170, 150, "#e9e6df", INK2, 12, 1.6),
         f'<rect x="{cx - 8}" y="{py + 7}" width="16" height="14" fill="{MUTED}"/>',
         rect(cx - 75, py, 150, 8, "#d9d5cc", INK2, 3, 1.4)]
    dc, R = py + 95, 58
    b.append(circle(cx, dc, R, CARD, INK, 2))
    for k in range(50):
        gg = k * 10
        a = -math.pi / 2 + TAU * gg / 500
        L = 10 if gg % 100 == 0 else (7 if gg % 50 == 0 else 4)
        b.append(line(cx + (R - 2) * math.cos(a), dc + (R - 2) * math.sin(a), cx + (R - 2 - L) * math.cos(a), dc + (R - 2 - L) * math.sin(a),
                      INK if gg % 100 == 0 else MUTED, 1.6 if gg % 100 == 0 else 1))
    a = -math.pi / 2 + TAU * g / 500
    b.append(line(cx - 8 * math.cos(a), dc - 8 * math.sin(a), cx + (R - 6) * math.cos(a), dc + (R - 6) * math.sin(a), ACC, 3))
    b.append(circle(cx, dc, 4.5, INK2, INK2, 0))
    for gg in range(0, 500, 100):      # 目もりの数字（はりの上でも読めるようにふちどり）
        a = -math.pi / 2 + TAU * gg / 500
        b.append(text(cx + (R - 25) * math.cos(a), dc + (R - 25) * math.sin(a) + 5, str(gg), 14, INK, 700, "middle",
                      stroke="#fff", stroke_width=4, paint_order="stroke"))
    return "".join(b)


def ball(x, cy, r):
    return f'<ellipse cx="{x:.1f}" cy="{cy:.1f}" rx="{r * 1.03:.1f}" ry="{r * 0.96:.1f}" fill="{CLAY}" stroke="{CLAY_E}" stroke-width="1.4"/>'


def clay(kind, cx, by):
    if kind == "maru":
        return ball(cx, by - 31, 32)
    if kind == "taira":
        return f'<rect x="{cx - 72}" y="{by - 15}" width="144" height="15" rx="7.5" fill="{CLAY}" stroke="{CLAY_E}" stroke-width="1.4"/>'
    if kind == "himo":
        pts = [(cx + x, by - 7 - 3 * math.sin(x / 11)) for x in range(-82, 83, 4)]
        return (poly(pts, CLAY_E, 14).replace('stroke-linejoin="round"', 'stroke-linejoin="round" stroke-linecap="round"')
                + poly(pts, CLAY, 10.5).replace('stroke-linejoin="round"', 'stroke-linejoin="round" stroke-linecap="round"'))
    pos = [(-52, 0), (-17, 0), (17, 0), (51, 0), (-34, 1), (34, 1)]       # シミュの CPOS
    out = []
    for (dx, row), g in zip(pos, PCS):
        r = 30 * (g / 100) ** (1 / 3)
        cy = by - 0.96 * r if row == 0 else by - 30 - 0.71 * r
        out.append((row, ball(cx + dx, cy, r)))
    return "".join(s for _, s in sorted(out, key=lambda t: -t[0]))


def fig1():
    b = []
    kinds = [("maru", "丸めた"), ("taira", "平らにした"), ("himo", "ほそ長くした"), ("bara", "細かく分けた")]
    py = 296
    for i, (k, nm) in enumerate(kinds):
        cx = 165 + i * 290
        b.append(text(cx, 205, nm, 21, INK, 700, "middle"))
        b.append(dial_scale(cx, py, 100))
        b.append(clay(k, cx, py))
        b.append(text(cx, 500, "100 g", 28, TEAL_D, 700, "middle"))
        if i < 3:
            b.append(arrow(cx + 92, 198, cx + 196, 198, "muted", 2))
    b.append(text(165 + 145, 182, "形をかえる", 14, MUTED, anchor="middle"))
    b.append(text(60, 130, "ねん土を自動上皿はかりにのせて、重さをはかる", 18, INK2, 700))
    b.append(rect(48, 526, 1104, 94, TEAL_L, LINE, 10))
    b.append(text(600, 562, "どの形でも 100 g。物は、形をかえても重さはかわらない。", 22, TEAL_D, 700, "middle"))
    b.append(text(600, 598, "細かく分けたときは、かけらを全部のせてはかろう（1こでも外に出すと、軽くなったように見える）。", 16.5, INK2, anchor="middle"))
    return svg("".join(b), "形をかえても、重さはかわらない（ねん土 100 g）",
               "自動上皿はかり（はり1回り500 g）ではかった。アルミはく（30cm×1m）も、広げても丸めても 8.9 g のまま。")


def fig2():
    b = []
    # 左上：立方体
    b.append(text(60, 130, "どれも同じ大きさ", 18, INK, 700))
    x, y, s, d = 110, 175, 86, 26
    b.append(f'<path d="M{x},{y} l{d},{-d} h{s} l{-d},{d}z" fill="#efe9dc" stroke="{INK2}" stroke-width="1.6"/>')
    b.append(f'<path d="M{x + s},{y} l{d},{-d} v{s} l{-d},{d}z" fill="#ddd5c4" stroke="{INK2}" stroke-width="1.6"/>')
    b.append(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="#f6f1e6" stroke="{INK2}" stroke-width="1.6"/>')
    b.append(text(x + s / 2, y + s + 24, "3cm", 16, INK, 700, "middle"))
    b.append(text(x - 10, y + s / 2 + 6, "3cm", 16, INK, 700, "end"))
    b.append(text(x + s + d + 10, y - d / 2 + 22, "3cm", 16, INK, 700))
    b.append(text(60, 318, "1辺3cmの立方体", 16, INK2))
    # 左下：てんびん（シミュと同じかたむき 0.16×tanh(重さの差÷4)）
    th = 0.16 * math.tanh((BW["鉄"] - BW["木"]) / 4)
    cx, py, L = 205, 470, 118
    b.append(text(60, 360, "てんびんでくらべる", 18, INK, 700))
    b.append(f'<rect x="{cx - 80}" y="{py + 66}" width="160" height="10" rx="4" fill="{INK2}"/>' + f'<rect x="{cx - 6}" y="{py}" width="12" height="{66}" fill="{MUTED}"/>')
    lx, ly = cx - L * math.cos(th), py - L * math.sin(th)
    rx, ry = cx + L * math.cos(th), py + L * math.sin(th)
    b.append(line(lx, ly, rx, ry, INK, 7))
    for ex, ey, nm, fill in [(lx, ly, "木", "#e7c08a"), (rx, ry, "鉄", "#8a9099")]:
        b.append(f'<rect x="{ex - 3}" y="{ey - 22}" width="6" height="22" fill="{MUTED}"/>' + rect(ex - 42, ey - 28, 84, 7, "#d9d5cc", INK2, 3, 1.2))
        b.append(rect(ex - 22, ey - 72, 44, 44, fill, INK2, 3, 1.4) + text(ex, ey - 43, nm, 17, INK if nm == "木" else "#fff", 700, "middle"))
    b.append(circle(cx, py, 5, INK, INK, 0))
    b.append(text(60, 588, "鉄の方が下がる → 鉄の方が重い", 17, ACC, 700))
    # 右：ぼうグラフ（重いじゅん）
    X0, LX = 600, 588
    b.append(text(430, 130, "1辺3cmの立方体の重さ（重いじゅん）", 18, INK, 700))
    order = sorted(BW.items(), key=lambda t: -t[1])
    k = 1.8                                          # 1 g＝1.8px
    y0 = 150
    for i, (nm, g) in enumerate(order):
        yy = y0 + i * 50
        b.append(text(LX, yy + 27, nm, 17, INK, 700, "end"))
        b.append(rect(X0, yy + 6, g * k, 30, TEAL_L, TEAL, 4, 1.4))
        b.append(text(X0 + g * k + 10, yy + 28, f"{g} g", 17, INK, 700))
    ya = y0 + 7 * 50 + 4
    b.append(line(X0, y0, X0, ya, INK, 1.6) + line(X0, ya, X0 + 250 * k + 10, ya, INK, 1.6))
    for g in range(0, 251, 50):
        b.append(line(X0 + g * k, ya, X0 + g * k, ya + 6, INK, 1.4) + text(X0 + g * k, ya + 24, f"{g}", 14, INK2, anchor="middle"))
    b.append(text(X0 + 250 * k + 16, ya + 24, "g", 14, INK2))
    b.append(text(430, 570, f"どうは木の約{round(BW['どう'] / BW['木'])}倍、鉄は木の約{round(BW['鉄'] / BW['木'])}倍の重さ。", 17, ACC, 700))
    b.append(text(430, 600, "プラスチックとゴム、ガラスとアルミニウムは手で持つとわかりにくい → てんびんやはかりで。", 15.5, INK2))
    return svg("".join(b), "同じ大きさでも、物によって重さはちがう",
               "重さは、1cm³あたりの重さ（理科年表など）から計算しためやす。木は種類によってちがう（ここでは0.5 g）。")


FIGS = [
    dict(svg=fig1, alt="物と重さの図。100 gのねん土を丸めた・平らにした・ほそ長くした・細かく分けた4つの形で自動上皿はかりにのせると、どれも100 gで、物は形をかえても重さはかわらないことを示す（小3理科）。",
         caption="ねん土の形をかえて重さをはかる。どの形でも100 gで、形をかえても重さはかわらない。"),
    dict(svg=fig2, alt="同じ大きさ（1辺3cmの立方体）の木・プラスチック・ゴム・ガラス・アルミニウム・鉄・どうの重さを重いじゅんにならべたぼうグラフ（どう241.9 g、鉄212.5 g、アルミニウム72.9 g、木13.5 gなど）と、木と鉄をてんびんでくらべた図。",
         caption="同じ大きさでも、物によって重さはちがう。てんびんやはかりでくらべる。"),
]
