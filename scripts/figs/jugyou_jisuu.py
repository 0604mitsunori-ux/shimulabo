"""年間授業時数シミュレーター（jugyou-jisuu）の図。
式はページの JS と同じ：年間授業時数 = 週の授業時数 × 実施週数、過不足 = 年間 − 標準（≥0 で「確保できる見込み」）。
標準授業時数（学校教育法施行規則 別表第一・第二）：小1 850・小2 910・小3 980・小4〜6 1015・中1〜3 1015。
1単位時間：小45分・中50分。学習指導要領：年間35週（小1は34週）以上にわたって計画。"""
from figlib import *

ANCHOR = r'<div class="note"><strong>計算式</strong>.*?</div>\s*<p>.*?</p>\n'
STD = [("小1", 850, 34), ("小2", 910, 35), ("小3", 980, 35), ("小4", 1015, 35), ("小5", 1015, 35), ("小6", 1015, 35),
       ("中1", 1015, 35), ("中2", 1015, 35), ("中3", 1015, 35)]


def fig1():
    b = []
    b.append(text(48, 124, "1年間の総授業時数（単位時間）と、週あたりのコマ数", 19, INK, 700))
    base, top, vmax = 508, 196, 1015
    bw, gap, x0 = 62, 50, 176
    py = lambda v: base - v / vmax * (base - top)
    b.append(line(150, base, 1140, base, INK, 1.8))
    for v in (250, 500, 750, 1000):
        b.append(line(150, py(v), 1140, py(v), LINE, 1) + text(140, py(v) + 5, str(v), 14, INK2, anchor="end"))
    b.append(text(140, base + 5, "0", 14, INK2, anchor="end"))
    for i, (g, v, w) in enumerate(STD):
        x = x0 + i * (bw + gap)
        c = TEAL if g.startswith("小") else TEAL_D
        b.append(f'<rect x="{x}" y="{py(v):.1f}" width="{bw}" height="{base - py(v):.1f}" rx="3" fill="{c}"/>')
        b.append(text(x + bw / 2, py(v) - 10, str(v), 18, INK, 700, "middle"))
        b.append(text(x + bw / 2, base + 30, g, 18, INK, 700, "middle"))
        b.append(text(x + bw / 2, base + 60, f"{v // w}コマ", 17, INK2, anchor="middle"))
    b.append(text(48, base + 30, "学年", 16, INK, 700))
    b.append(text(48, base + 60, "週あたり※", 16, INK, 700))
    # 小学校／中学校のくくり
    xs0, xs1 = x0, x0 + 5 * (bw + gap) + bw
    xm0, xm1 = x0 + 6 * (bw + gap), x0 + 8 * (bw + gap) + bw
    for a, c, s, col in [(xs0, xs1, "小学校：1コマ＝45分", TEAL), (xm0, xm1, "中学校：1コマ＝50分", TEAL_D)]:
        b.append(f'<path d="M{a},{base + 72} v8 H{c} v-8" fill="none" stroke="{col}" stroke-width="2"/>'
                 + text((a + c) / 2, base + 104, s, 17, col, 700, "middle"))
    b.append(text(1140, 160, "小4〜中3はすべて 1015", 17, TEAL_D, 700, "end"))
    return svg("".join(b), "学年ごとの標準授業時数（小1〜中3）",
               "※週あたり＝標準授業時数÷35週（小1は34週）。学校教育法施行規則の別表、学習指導要領による。")


def fig2():
    b = []
    std = 1015
    b.append(text(48, 126, "年間授業時数 ＝ 週の授業時数 × 実施週数", 20, INK, 700))
    b.append(text(560, 126, "例）29 × 35 ＝ 1015（ちょうど標準）", 18, INK2))
    weeks = [33, 34, 35, 36, 37]
    per = [27, 28, 29, 30, 31]
    x0, y0, hw, cw, hh, ch = 96, 150, 150, 176, 48, 70
    b.append(rect(x0, y0, hw + cw * len(weeks), hh + ch * len(per), CARD, LINE, 8))
    b.append(f'<rect x="{x0}" y="{y0}" width="{hw + cw * len(weeks)}" height="{hh}" rx="8" fill="{TEAL_L}"/>')
    b.append(text(x0 + hw / 2, y0 + 31, "週 ＼ 実施週数", 16, INK, 700, "middle"))
    for j, w in enumerate(weeks):
        b.append(text(x0 + hw + cw * j + cw / 2, y0 + 31, f"{w}週", 18, INK, 700, "middle"))
    for i, p in enumerate(per):
        yy = y0 + hh + ch * i
        b.append(line(x0, yy, x0 + hw + cw * len(weeks), yy, LINE, 1))
        b.append(text(x0 + hw / 2, yy + 43, f"週{p}コマ", 18, INK, 700, "middle"))
        for j, w in enumerate(weeks):
            t = p * w; d = t - std
            ok = d >= 0
            cx = x0 + hw + cw * j
            b.append(f'<rect x="{cx + 3}" y="{yy + 3}" width="{cw - 6}" height="{ch - 6}" rx="6" fill="{TEAL_L if ok else ACC_L}"/>')
            b.append(text(cx + cw / 2, yy + 32, f"{t}", 20, INK, 700, "middle"))
            b.append(text(cx + cw / 2, yy + 56, ("±0" if d == 0 else f"{d:+d}".replace("-", "−")) + ("　✓" if ok else "　不足"), 15, TEAL_D if ok else ACC, 700, "middle"))
    # 標準ちょうどのセルに枠
    i, j = per.index(29), weeks.index(35)
    b.append(rect(x0 + hw + cw * j + 2, y0 + hh + ch * i + 2, cw - 4, ch - 4, "none", TEAL_D, 6, 3))
    ly = y0 + hh + ch * len(per) + 34
    b.append(rect(x0, ly - 16, 22, 22, TEAL_L, TEAL, 4) + text(x0 + 32, ly, "標準1015以上（確保できる見込み）", 16, INK2))
    b.append(rect(x0 + 380, ly - 16, 22, 22, ACC_L, ACC, 4) + text(x0 + 412, ly, "標準に足りない（不足の可能性）", 16, INK2))
    return svg("".join(b), "週の授業時数×実施週数の早見表（標準1015コマ：小4〜中3）",
               "行事や休校で1週減ると、週29コマなら29コマ減る。教科ごとの時数管理もあわせて行う。")


FIGS = [
    dict(svg=fig1,
         alt="学年ごとの標準授業時数の棒グラフ。小1は850、小2は910、小3は980、小4〜小6と中1〜中3は1015単位時間で、週あたりは小1が25コマ（34週）、小2が26コマ、小3が28コマ、小4〜中3が29コマ（35週）。1コマは小学校45分・中学校50分。",
         caption="学年ごとの標準授業時数。小4〜中3は年間1015コマ（35週なら週29コマ）が標準。"),
    dict(svg=fig2,
         alt="年間授業時数の早見表。週の授業時数27〜31コマと実施週数33〜37週の組み合わせごとに、年間授業時数と標準授業時数1015との過不足（確保できる見込みか不足の可能性か）を示した表。",
         caption="週の授業時数×実施週数の早見表（標準1015コマの学年）。週29コマなら35週でちょうど標準。"),
]
