"""滑車と仕事の原理（kassha-shigoto・中3 仕事とエネルギー）の授業用の図
数値はシミュ（scripts/rika/sims_undou_shigoto.py の KASSHA_JS の FD() と WAYS_TABLE／POWER_TABLE）と同じ：
1000g（重力10N・100gで1N）を50cm持ち上げる。直接・定滑車＝10N×0.5m、動滑車・定滑車＋動滑車＝5N×1m、動滑車2個＝2.5N×2m、
斜面（長さ100cm）＝重力×高さ÷長さ＝5N×1m、てこ（2:1）＝5N×1m。仕事率＝仕事÷時間。"""
import math
from figlib import *

MASS0, H0 = 1000, 50
Wt, h = MASS0 / 100, H0 / 100          # 10N、0.5m


def n_(v):
    """シミュの nf()／記事の _n()：小数第2位で丸め、ずれれば「約」"""
    r = math.floor(v * 100 + 0.5) / 100
    s = ("%.2f" % r).rstrip("0").rstrip(".")
    return ("約" if abs(v - r) > 1e-9 else "") + s


def FD(mid, Lc=100, k=2):
    """シミュの FD()：[必要な力N, 動かす距離m]"""
    if mid in ("move", "combo"): return Wt / 2, 2 * h
    if mid == "move2": return Wt / 4, 4 * h
    if mid == "slope": return Wt * h / (Lc / 100), Lc / 100
    if mid == "lever": return Wt / k, k * h
    return Wt, h


WAYS = [("direct", "直接持ち上げる"), ("fixed", "定滑車"), ("move", "動滑車"), ("combo", "定滑車＋動滑車"),
        ("move2", "動滑車2個（＋定滑車）"), ("slope", "斜面（長さ100cm）"), ("lever", "てこ（支点からのきょり2:1）")]

ROPE = "#8a5a1c"


def pulley(x, y, r, fill):
    return circle(x, y, r, fill, INK2, 2) + circle(x, y, r - 7, "none", MUTED, 1) + circle(x, y, 3.5, INK2, INK2, 0)


def obj(cx, top, dashed=False):
    w, hh = 76, 52
    if dashed:
        return f'<rect x="{cx - w / 2:.1f}" y="{top:.1f}" width="{w}" height="{hh}" rx="6" fill="none" stroke="{TEAL}" stroke-width="1.6" stroke-dasharray="5 4"/>'
    return (rect(cx - w / 2, top, w, hh, TEAL, TEAL, 6) + text(cx, top + 23, f"{MASS0}g", 15, "#fff", 700, "middle")
            + text(cx, top + 43, f"{n_(Wt)}N", 14, "#d6ecf3", 400, "middle"))


def ceiling(x0, x1, y=152):
    out = [f'<rect x="{x0}" y="{y}" width="{x1 - x0}" height="9" fill="#cfc9bb"/>']
    for x in range(int(x0) + 4, int(x1), 11):
        out.append(line(x, y, x + 7, y - 7, "#a8a294", 1.2))
    return "".join(out)


def vdim(x, y1, y2, color, rows, side="right", size=15):
    """縦の寸法線（両向き矢印）。color は figlib の矢印の色名、rows はラベルの行"""
    c = PALETTE[color]; mid = (y1 + y2) / 2
    out = [line(x - 7, y1, x + 7, y1, c, 1.6), line(x - 7, y2, x + 7, y2, c, 1.6),
           arrow(x, mid, x, y1, color, 2), arrow(x, mid, x, y2, color, 2)]
    tx = x + 12 if side == "right" else x - 12
    out.append(lines(tx, mid - (len(rows) - 1) * size * 0.75 + 5, rows, size, c, 1.5,
                     anchor="start" if side == "right" else "end", weight=700))
    return "".join(out)


PALETTE = {"teal": TEAL, "acc": ACC, "ink": INK, "muted": MUTED, "gold": GOLD, "green": GREEN}


def hand(x, y, dashed=False):
    if dashed:
        return f'<circle cx="{x}" cy="{y}" r="9" fill="none" stroke="{GOLD}" stroke-width="1.5" stroke-dasharray="3 3"/>'
    return circle(x, y, 9, "#f6d48a", GOLD, 1.5)


def fig1():
    s = 80 / h                     # 0.5m を 80px
    FLOOR = 540
    b = []
    pan = [("direct", "直接持ち上げる"), ("fixed", "定滑車"), ("move", "動滑車")]
    for i, (mid, ttl) in enumerate(pan):
        px = 48 + i * 376
        F, d = FD(mid)
        Wk = F * d
        assert abs(Wk - Wt * h) < 1e-9
        b.append(rect(px, 96, 352, 524, CARD, LINE, 10))
        b.append(text(px + 176, 128, ttl, 21, INK, 700, "middle"))
        b.append(line(px + 16, FLOOR, px + 336, FLOOR, "#9a958a", 3))
        up = h * s; Lf = F * 8                                     # 力の矢印は 1N＝8px
        if mid == "direct":
            cx = px + 150
            top0, top1 = FLOOR - 52, FLOOR - 52 - up
            b.append(obj(cx, top0, True) + obj(cx, top1))
            b.append(arrow(cx, top1, cx, top1 - Lf, "acc", 3.6) + hand(cx, top1 - 2))
            b.append(text(cx + 14, top1 - Lf + 18, f"{n_(F)}N", 20, ACC, 700))
            b.append(vdim(cx - 62, FLOOR, FLOOR - up, "teal", ["上がる", f"高さ {n_(h)}m"], "left"))
            b.append(vdim(cx + 66, top0, top1, "acc", ["手を動かす", f"距離 {n_(d)}m"], "right"))
            note = "力も距離もそのまま"
        elif mid == "fixed":
            pxc, py, r = px + 188, 214, 26
            ox = pxc - r
            top0, top1 = FLOOR - 52, FLOOR - 52 - up
            hy0 = 330; hy1 = hy0 + d * s
            b.append(ceiling(pxc - 50, pxc + 50) + line(pxc, 161, pxc, py - r + 2, INK2, 3))
            b.append(pulley(pxc, py, r, "#e6e3dc"))
            b.append(f'<path d="M{pxc - r},{py} A{r},{r} 0 0 1 {pxc + r},{py}" fill="none" stroke="{ROPE}" stroke-width="2.6"/>')
            b.append(line(ox, py, ox, top1, ROPE, 2.6) + line(pxc + r, py, pxc + r, hy1, ROPE, 2.6))
            b.append(obj(ox, top0, True) + obj(ox, top1))
            b.append(hand(pxc + r, hy0, True) + arrow(pxc + r, hy1, pxc + r, hy1 + Lf, "acc", 3.6) + hand(pxc + r, hy1))
            b.append(text(pxc + r + 14, hy1 + Lf - 4, f"{n_(F)}N", 20, ACC, 700))
            b.append(text(pxc - r - 8, py - 4, "定滑車", 16, INK2, 700, "end"))
            b.append(vdim(ox - 52, FLOOR, FLOOR - up, "teal", ["上がる", f"高さ {n_(h)}m"], "left"))
            b.append(vdim(pxc + r + 42, hy0, hy1, "acc", ["手を動かす", f"距離 {n_(d)}m"], "right"))
            note = "力の向きを変えられる（下に引ける）"
        else:
            cx, r = px + 166, 26
            top0, top1 = FLOOR - 52, FLOOR - 52 - up
            py0, py1 = top0 - 30, top1 - 30
            hy0 = 350; hy1 = hy0 - d * s
            # ひもの長さが変わらないことを確かめる（左のひも＋右のひも）
            assert abs(((py0 - 161) + (py0 - hy0)) - ((py1 - 161) + (py1 - hy1))) < 1e-9
            b.append(ceiling(cx - r - 46, cx - r + 22))
            b.append(obj(cx, top0, True) + line(cx, py1, cx, top1, INK2, 3) + obj(cx, top1))
            b.append(pulley(cx, py1, r, "#f3e2b8"))
            b.append(f'<path d="M{cx - r},{py1} A{r},{r} 0 0 0 {cx + r},{py1}" fill="none" stroke="{ROPE}" stroke-width="2.6"/>')
            b.append(line(cx - r, 161, cx - r, py1, ROPE, 2.6) + line(cx + r, py1, cx + r, hy1, ROPE, 2.6))
            b.append(hand(cx + r, hy0, True) + arrow(cx + r, hy1, cx + r, hy1 - Lf, "acc", 3.6) + hand(cx + r, hy1))
            b.append(text(cx + r + 14, hy1 - Lf + 18, f"{n_(F)}N", 20, ACC, 700))
            b.append(text(cx - r - 10, py1 + 6, "動滑車", 16, GOLD, 700, "end"))
            b.append(lines(cx - r - 10, 262, ["2本のひもで", "支えるので", "1本は半分の力"], 14.5, INK2, 1.45, anchor="end"))
            b.append(vdim(cx - 72, FLOOR, FLOOR - up, "teal", ["上がる", f"高さ {n_(h)}m"], "left", 14))
            b.append(vdim(cx + r + 40, hy0, hy1, "acc", ["手を動かす", f"距離 {n_(d)}m"], "right", 14))
            note = "力は半分、手を動かす距離は2倍"
        b.append(text(px + 176, 576, f"仕事 ＝ {n_(F)}N × {n_(d)}m ＝ {n_(Wk)}J", 19, TEAL_D, 700, "middle"))
        b.append(text(px + 176, 603, note, 15, INK2, anchor="middle"))
    return svg("".join(b), "滑車と仕事の原理のしくみ（1000gの物体を0.5m持ち上げる）",
               "点線は持ち上げる前。滑車・ひもの重さと摩擦は考えない。100gの物体にはたらく重力を1Nとする。")


def fig2():
    b = []
    # ---- 左：力×距離の長方形
    x0, y0, w, hgt = 100, 560, 380, 380
    dmax, fmax = 2.0, 10.0
    sx, sy = w / dmax, hgt / fmax
    b.append(text(60, 122, "力×距離の長方形（面積＝仕事）", 19, INK, 700))
    b.append(axes(x0, y0, w, hgt, "", "力（N）", [(v * sx, n_(v)) for v in (0, 0.5, 1.0, 1.5, 2.0)],
                  [(v * sy, n_(v)) for v in (0, 2.5, 5, 7.5, 10)], 15))
    b.append(text(x0 + w / 2, y0 + 50, "力を加えて動かす距離（m）", 15, INK, anchor="middle"))
    rects = [(FD("move2"), GOLD, GOLD_L, "動滑車2個", None),
             (FD("move"), TEAL, TEAL_L, "動滑車・斜面・てこ", None),
             (FD("direct"), INK2, "#e9e6df", "直接・定滑車", None)]
    for (F, d), col, fill, nm, _ in rects:
        b.append(f'<rect x="{x0}" y="{y0 - F * sy:.1f}" width="{d * sx:.1f}" height="{F * sy:.1f}" fill="{fill}" fill-opacity=".55" stroke="{col}" stroke-width="2.2"/>')
    (F1, d1), (F2, d2), (F3, d3) = FD("direct"), FD("move"), FD("move2")
    b.append(text(x0 + d1 * sx / 2, y0 - F1 * sy + 26, "直接・", 14.5, INK, 700, "middle") + text(x0 + d1 * sx / 2, y0 - F1 * sy + 46, "定滑車", 14.5, INK, 700, "middle"))
    b.append(text(x0 + d1 * sx / 2, y0 - F1 * sy + 72, f"{n_(F1)}N×{n_(d1)}m", 14, INK2, anchor="middle"))
    b.append(text(x0 + (d1 + d2) * sx / 2, y0 - F2 * sy + 26, "動滑車など", 14.5, TEAL_D, 700, "middle"))
    b.append(text(x0 + (d1 + d2) * sx / 2, y0 - F2 * sy + 48, f"{n_(F2)}N×{n_(d2)}m", 14, TEAL_D, anchor="middle"))
    b.append(text(x0 + (d2 + d3) * sx / 2, y0 - F3 * sy + 26, "動滑車2個", 14.5, GOLD, 700, "middle"))
    b.append(text(x0 + (d2 + d3) * sx / 2, y0 - F3 * sy + 46, f"{n_(F3)}N×{n_(d3)}m", 14, GOLD, anchor="middle"))
    b.append(text(340, 232, f"3つの長方形の面積は、どれも {n_(F1 * d1)}J", 17, TEAL_D, 700, "middle"))
    b.append(text(340, 260, "力が半分なら距離は2倍、1/4なら4倍", 15, INK2, anchor="middle"))
    # ---- 右：早見表
    b.append(text(606, 122, f"{MASS0}g（{n_(Wt)}N）を{H0}cm持ち上げるとき", 19, INK, 700))
    rows = []
    for mid, nm in WAYS:
        F, d = FD(mid)
        rows.append([nm, f"{n_(F)} N", f"{n_(d)} m", f"{n_(F * d)} J"])
    b.append(table(606, 138, ["持ち上げ方", "必要な力", "動かす距離", "仕事"], rows, [236, 104, 104, 102], 40, 15.5))
    # 仕事率
    b.append(text(606, 494, f"仕事率（仕事 ÷ かかった時間）：{n_(Wt * h)}Jの仕事なら", 17, INK, 700))
    secs = (1, 2, 5, 10, 20)
    b.append(table(606, 508, ["時間"] + [f"{s_}秒" for s_ in secs], [["仕事率"] + [f"{n_(Wt * h / s_)} W" for s_ in secs]],
                   [106, 88, 88, 88, 88, 88], 40, 15.5))
    return svg("".join(b), "道具ごとの力・距離・仕事（仕事の原理のまとめ）",
               "どの方法でも仕事は同じ（仕事の原理）。滑車・ひも・棒の重さと摩擦は考えない。100gの物体にはたらく重力＝1N。")


FIGS = [
    dict(svg=fig1, alt="滑車と仕事の原理のしくみの図。1000g（10N）の物体を0.5m持ち上げるとき、直接持ち上げると10Nで0.5m、定滑車は10Nで手を下に0.5m引き、動滑車は2本のひもで支えるので5Nで手を1.0m引く。仕事（力×距離）はどれも5Jで同じ。",
         caption="定滑車・動滑車のしくみ。動滑車では力は半分になるが、ひもを引く距離が2倍になり、仕事は変わらない。"),
    dict(svg=fig2, alt="仕事の原理のまとめ図。力×距離の長方形（10N×0.5m、5N×1m、2.5N×2m）の面積がどれも5Jになることと、直接・定滑車・動滑車・定滑車＋動滑車・動滑車2個・斜面・てこで1000gの物体を50cm持ち上げるときの力・距離・仕事の早見表、5Jの仕事の仕事率（1秒で5W〜20秒で0.25W）。",
         caption="道具ごとの力・距離・仕事の早見表。どの道具でも仕事は5Jで同じ（仕事の原理）。"),
]
