"""カフェイン残量（caffeine）の図。計算はページの JS と同じ：摂取量＝杯数×80mg、残量＝摂取量×0.5^(時間÷5)、
判定は 100mg以上「強く残存」・50mg以上「眠り浅いかも」・それ未満「おおむねOK」。"""
from figlib import *

ANCHOR = r"<h2>計算方法</h2>.*?</p>\n"
MG, HALF = 80, 5


def remain(cups, h): return cups * MG * 0.5 ** (h / HALF)


def judge(r): return "強く残存" if r >= 100 else ("眠り浅いかも" if r >= 50 else "おおむねOK")


ZONE = {"おおむねOK": (TEAL_L, TEAL_D), "眠り浅いかも": (GOLD_L, GOLD), "強く残存": (ACC_L, ACC)}


def fig1():
    b = []
    gx, gy, gw, gh = 118, 572, 620, 420
    T, YM = 24, 250
    x = lambda h: gx + h / T * gw
    y = lambda mg: gy - mg / YM * gh
    # 判定の帯
    for lo, hi, nm in [(0, 50, "おおむねOK"), (50, 100, "眠り浅いかも"), (100, YM, "強く残存")]:
        b.append(f'<rect x="{gx}" y="{y(hi):.1f}" width="{gw}" height="{y(lo) - y(hi):.1f}" fill="{ZONE[nm][0]}"/>')
        b.append(text(gx + gw - 10, y(hi) + 22 if nm != "おおむねOK" else y(35), nm + ("（100mg以上）" if nm == "強く残存" else "（50〜100mg）" if nm == "眠り浅いかも" else "（50mg未満）"),
                      14.5, ZONE[nm][1], 700, "end"))
    b.append(text(gx + gw / 2, gy + 46, "飲んでからの時間（時間）", 15, INK, anchor="middle"))
    b.append(axes(gx, gy, gw, gh, "", "", [(x(h) - gx, f"{h}") for h in range(0, 25, 5)] + [(x(24) - gx, "24")],
                  [(gy - y(v), f"{v}") for v in (0, 50, 100, 150, 200, 250)], 14))
    b.append(text(gx - 8, gy - gh - 22, "体に残るカフェイン（mg）", 14, INK, anchor="start"))
    hs = [i * 0.25 for i in range(97)]
    for cups, col, dash in [(3, ACC, None), (2, GOLD, "9 5"), (1, TEAL, "3 4")]:
        b.append(poly([(x(h), y(remain(cups, h))) for h in hs], col, 3.2, dash=dash))
        b.append(text(x(0) + 10, y(cups * MG) - 8, f"{cups}杯（{cups * MG}mg）", 15, col, 700, stroke=BG, stroke_width=5, paint_order="stroke"))
    # 半減期の目印（2杯の線）
    for h in (5, 10, 15):
        r = remain(2, h)
        b.append(line(x(h), y(r), x(h), gy, MUTED, 1.2, "3 3") + circle(x(h), y(r), 5, INK, INK, 0))
        b.append(text(x(h) + 8, y(r) - 10, f"{h}時間後 {r:.0f}mg", 15, INK, 700, stroke=BG, stroke_width=5, paint_order="stroke"))
    # 右：ポイント
    px = 806
    b.append(rect(px, 104, 346, 148, GOLD_L, GOLD, 10, 1.4))
    b.append(text(px + 20, 136, "計算式（シミュと同じ）", 16, GOLD, 700))
    b.append(lines(px + 20, 168, ["摂取量 ＝ 杯数 × 80mg", "残量 ＝ 摂取量 × 0.5^（時間÷5）", "→ 5時間ごとに半分になる（半減期）"], 16, INK, 1.5))
    b.append(rect(px, 268, 346, 184, CARD, LINE, 10))
    b.append(text(px + 20, 302, "たとえば（寝るときの残量）", 16, INK, 700))
    ex = [(3, 4), (2, 6), (1, 8)]
    for i, (c, h) in enumerate(ex):
        r = remain(c, h)
        b.append(text(px + 20, 342 + i * 38, f"{c}杯を寝る{h}時間前", 16, INK))
        b.append(text(px + 326, 342 + i * 38, f"約{r:.0f}mg・{judge(r)}", 16, ZONE[judge(r)][1], 700, "end"))
    b.append(rect(px, 468, 346, 148, ACC_L, ACC, 10, 1.2))
    b.append(lines(px + 20, 508, ["※ 目安であり、医療の診断ではない。", "体質・体重・代謝などで個人差がある。", "1杯＝コーヒー約80mgとして計算。"], 15, INK, 1.5))
    return svg("".join(b), "カフェインが体に残る量と時間（半減期5時間）",
               "就寝時に50mg以上残っていると、寝つきや眠りの質に影響する可能性があるとされる（シミュの判定）。")


def fig2():
    b = []
    hours = [2, 4, 6, 8, 10, 12]
    x0, y0, cw0, cw, hh, rh = 48, 150, 176, 154, 54, 92
    b.append(text(48, 126, "最後の1杯から寝るまでの時間と、寝るときに残るカフェイン（mg）", 18, INK, 700))
    b.append(rect(x0, y0, cw0 + cw * len(hours), hh + rh * 4, CARD, LINE, 8))
    b.append(f'<rect x="{x0}" y="{y0}" width="{cw0 + cw * len(hours)}" height="{hh}" rx="8" fill="{TEAL_L}"/>')
    b.append(text(x0 + cw0 / 2, y0 + 34, "飲んだ量", 16, INK, 700, "middle"))
    for j, h in enumerate(hours):
        b.append(text(x0 + cw0 + cw * (j + 0.5), y0 + 34, f"寝る{h}時間前", 17, INK, 700, "middle"))
    for i, cups in enumerate([1, 2, 3, 4]):
        yy = y0 + hh + rh * i
        b.append(line(x0, yy, x0 + cw0 + cw * len(hours), yy, LINE, 1))
        b.append(text(x0 + cw0 / 2, yy + 42, f"{cups}杯", 21, INK, 700, "middle"))
        b.append(text(x0 + cw0 / 2, yy + 68, f"（{cups * MG}mg）", 15, INK2, anchor="middle"))
        for j, h in enumerate(hours):
            r = remain(cups, h); jd = judge(r); bg, fg = ZONE[jd]
            cx = x0 + cw0 + cw * j
            b.append(f'<rect x="{cx + 4}" y="{yy + 4}" width="{cw - 8}" height="{rh - 8}" rx="6" fill="{bg}"/>')
            b.append(text(cx + cw / 2, yy + 46, f"{r:.0f}mg", 24, fg, 700, "middle"))
            b.append(text(cx + cw / 2, yy + 74, jd, 15, INK2, anchor="middle"))
    b.append(text(48, 588, "判定（シミュと同じ）：100mg以上＝強く残存　50mg以上＝眠り浅いかも　50mg未満＝おおむねOK", 16, INK))
    b.append(text(48, 614, "※ 半減期5時間での概算。体質・体重・代謝で個人差がある目安で、医療の診断ではない。", 15, ACC, 700))
    return svg("".join(b), "寝るときのカフェイン残量（早見表）",
               "1杯＝コーヒー約80mg。エナジードリンクは1本でコーヒー1〜2杯分のこともある。")


FIGS = [
    dict(svg=fig1, alt="カフェインの体内残量が半減期5時間で減っていくグラフ。コーヒー1杯（80mg）・2杯（160mg）・3杯（240mg）を飲んでから24時間の残量を、50mg未満おおむねOK・50〜100mg眠り浅いかも・100mg以上強く残存の帯と重ねて示し、2杯なら5時間後80mg・10時間後40mg・15時間後20mgになる。",
         caption="カフェインは5時間ごとに半分に減る。夕方の1杯も寝るときまでかなり残る。"),
    dict(svg=fig2, alt="コーヒー1〜4杯を寝る2・4・6・8・10・12時間前に飲んだときの、寝るときに残るカフェイン量（mg）と睡眠への影響の判定の早見表。例：3杯を寝る4時間前なら約138mgで強く残存、1杯を寝る6時間前なら約35mgでおおむねOK。",
         caption="寝るときのカフェイン残量の早見表（半減期5時間での目安）。"),
]
