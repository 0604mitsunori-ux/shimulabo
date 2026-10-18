"""DNA二重らせん（dna）の図。数値はページの本文と同じ（直径 約2nm・1回転 約3.4nm＝塩基対10個・A–T／G–C・右巻き）。
らせんの縦横比（3.4÷2＝1.7）と1回転10塩基対は実際と同じ比で描く。"""
import math
from figlib import *

BASE_COL = {"A": ACC, "T": GOLD, "G": TEAL, "C": PURPLE}
NAME = {"A": "アデニン", "T": "チミン", "G": "グアニン", "C": "シトシン"}
PAIR = {"A": "T", "T": "A", "G": "C", "C": "G"}
HB = {"A": 2, "T": 2, "G": 3, "C": 3}          # 水素結合の数（A–T 2本、G–C 3本）
SEQ = "ATGCGTACCGATTGCAAGTC"                    # 20塩基対＝2回転


def base_box(x, y, ch, w=34, h=30, size=18):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" rx="4" fill="{BASE_COL[ch]}"/>'
            + text(x + w / 2, y + h / 2 + size * 0.36, ch, size, "#fff", 700, "middle"))


def helix(cx, ybot, R, P, seq):
    """右巻きのらせん。θ は下から上へ増える。x＝cx＋R·cosθ、手前＝sinθ＜0（手前の鎖は左下→右上に見える）"""
    out_back, out_rung, out_front = [], [], []
    turns = len(seq) / 10
    ytop = ybot - turns * P
    for s, ph in ((0, 0.0), (1, math.pi)):
        seg, front_prev = [], None
        n = int((ybot - ytop) / 2)
        for i in range(n + 1):
            y = ybot - i * 2
            th = 2 * math.pi * (ybot - y) / P + ph + 0.35
            x = cx + R * math.cos(th); front = math.sin(th) < 0
            if front_prev is not None and front != front_prev:
                (out_front if front_prev else out_back).append(seg); seg = [seg[-1]]
            seg.append((x, y)); front_prev = front
        (out_front if front_prev else out_back).append(seg)
    back = "".join(poly(sg, "#b7bec5", 8) for sg in out_back)
    front = "".join(poly(sg, INK2, 10) for sg in out_front)
    for k, ch in enumerate(seq):
        y = ybot - (k + 0.5) * P / 10
        th = 2 * math.pi * (ybot - y) / P + 0.35
        x1, x2 = cx + R * math.cos(th), cx + R * math.cos(th + math.pi)
        xm = (x1 + x2) / 2
        out_rung.append(line(x1, y, xm, y, BASE_COL[ch], 7) + line(xm, y, x2, y, BASE_COL[PAIR[ch]], 7))
    return back + "".join(out_rung) + front, ytop


def fig1():
    b = []
    cx, R, P, ybot = 262, 65, 221, 590          # 直径130px：1回転221px＝2nm：3.4nm
    hx, ytop = helix(cx, ybot, R, P, SEQ)
    b.append(hx)
    # 直径
    yd = ytop - 18
    b.append(line(cx - R, yd, cx + R, yd, INK, 1.6) + line(cx - R, yd - 7, cx - R, yd + 7, INK, 1.6) + line(cx + R, yd - 7, cx + R, yd + 7, INK, 1.6))
    b.append(text(cx, yd - 10, "直径 約2nm", 16, INK, 700, "middle"))
    # 1回転
    xb = cx - R - 34
    b.append(line(xb, ybot, xb, ybot - P, INK, 1.6) + line(xb - 7, ybot, xb + 7, ybot, INK, 1.6) + line(xb - 7, ybot - P, xb + 7, ybot - P, INK, 1.6))
    b.append(lines(xb - 12, ybot - P / 2 - 14, ["1回転", "約3.4nm", "塩基対10個分"], 16, INK, 1.5, anchor="end"))
    # 右のラベル
    lx = 370
    ys = ybot - P * (1.5 - 0.35 / (2 * math.pi))      # 2本目の鎖がらせんの右端に来る高さ
    b.append(line(lx - 6, ys - 6, cx + R + 6, ys, MUTED, 1.2) + lines(lx, ys - 10, ["糖とリン酸の", "鎖（2本）"], 16, INK, 1.4, weight=700))
    k = 9; yk = ybot - (k + 0.5) * P / 10                  # 横に長く見えている塩基対
    assert abs(math.cos(2 * math.pi * (k + 0.5) / 10 + 0.35)) > 0.99
    b.append(line(lx - 6, yk + 2, cx + 36, yk, MUTED, 1.2) + lines(lx, yk + 8, ["塩基対", "（A–T、G–C）"], 16, INK, 1.4, weight=700))
    b.append(lines(lx, 492, ["右巻きの", "二重らせん"], 16, INK, 1.4, weight=700))
    b.append(text(cx, ybot + 26, "（模式図）", 14, MUTED, anchor="middle"))
    # 右：塩基の組み方
    x0 = 588
    b.append(text(x0, 126, "塩基は決まった相手とだけ組む", 19, INK, 700))
    b.append(line(x0 + 16, 150, x0 + 16, 386, INK2, 8) + line(x0 + 296, 150, x0 + 296, 386, INK2, 8))
    for i, ch in enumerate("AGTC"):
        y = 160 + i * 58
        b.append(base_box(x0 + 22, y, ch, 96, 40, 22))
        b.append(base_box(x0 + 194, y, PAIR[ch], 96, 40, 22))
        n = HB[ch]
        for j in range(n):
            yy = y + 20 + (j - (n - 1) / 2) * 10
            b.append(line(x0 + 124, yy, x0 + 188, yy, INK, 1.8, "4 3"))
        b.append(text(x0 + 322, y + 27, f"水素結合 {n}本", 16, INK2))
    b.append(text(x0, 416, "破線＝塩基どうしをつなぐ水素結合（形と本数が合う組だけがつながる）", 14, MUTED))
    b.append(table(x0, 432, ["塩基", "組む相手", "つなぐ水素結合"],
                   [["A（アデニン）", "T（チミン）", "2本"], ["G（グアニン）", "C（シトシン）", "3本"]], [200, 200, 164], 46, 17))
    b.append(text(x0, 600, "※ RNAでは T（チミン）のかわりに U（ウラシル）を使う。", 15, INK2))
    return svg("".join(b), "DNAの二重らせんのつくり",
               "2本の鎖を、塩基のペア（A–T、G–C）が橋のようにつなぎ、全体が右巻きにねじれている。")


def fig2():
    b = []
    # ① 相補性
    top = "ATGCGTACCA"
    bot = "".join(PAIR[c] for c in top)
    b.append(text(48, 126, "① 片方の鎖の並びが分かれば、もう片方は自動的に決まる（相補性）", 19, INK, 700))
    x0, w = 210, 74
    b.append(text(x0 - 20, 176, "わかっている鎖", 16, INK2, anchor="end"))
    b.append(text(x0 - 20, 264, "相手の鎖", 16, INK2, anchor="end"))
    for i, (c1, c2) in enumerate(zip(top, bot)):
        x = x0 + i * w
        b.append(base_box(x, 152, c1, 50, 36, 20))
        for j in range(HB[c1]):
            xx = x + 25 + (j - (HB[c1] - 1) / 2) * 9
            b.append(line(xx, 192, xx, 236, INK, 1.6, "4 3"))
        b.append(base_box(x, 240, c2, 50, 36, 20))
    b.append(line(x0 - 10, 150, x0 + 10 * w - 14, 150, INK2, 4) + line(x0 - 10, 278, x0 + 10 * w - 14, 278, INK2, 4))
    # ② 複製
    b.append(text(48, 338, "② 細胞が分かれる前のDNAのコピー（複製）", 19, INK, 700))
    seq = "ATGCGA"
    rh = 36

    def ladder(x, y, s, left_new=False, right_new=False, gap=0):
        out = []
        for side, new, xs in ((0, left_new, x), (1, right_new, x + 88 + gap)):
            col = TEAL if new else INK2
            out.append(line(xs + (0 if side == 0 else 38), y - 6, xs + (0 if side == 0 else 38), y + len(s) * rh, col, 6))
        for i, ch in enumerate(s):
            yy = y + i * rh
            out.append(base_box(x + 4, yy, ch, 30, 28, 15))
            out.append(base_box(x + 92 + gap, yy, PAIR[ch], 30, 28, 15))
            if gap == 0:
                out.append(line(x + 36, yy + 14, x + 90, yy + 14, INK, 1.4, "4 3"))
        return "".join(out)
    y = 384
    b.append(text(120, y - 14, "もとのDNA", 16, INK, 700, "middle"))
    b.append(ladder(60, y, seq))
    b.append(arrow(210, y + 105, 270, y + 105, "ink", 2.4))
    b.append(text(450, y - 14, "2本の鎖がほどける", 16, INK, 700, "middle"))
    b.append(ladder(330, y, seq, gap=110))
    b.append(arrow(612, y + 105, 672, y + 105, "ink", 2.4))
    b.append(text(870, y - 14, "それぞれを型に、新しい鎖ができる", 16, INK, 700, "middle"))
    b.append(ladder(712, y, seq, right_new=True))
    b.append(ladder(902, y, "".join(PAIR[c] for c in seq), right_new=True))
    b.append(text(1040, y + 70, "＝同じDNAが", 15, INK2) + text(1040, y + 94, "2つできる", 15, INK2))
    b.append(line(1040, y + 150, 1070, y + 150, INK2, 6) + text(1078, y + 156, "もとの鎖", 14, INK2))
    b.append(line(1040, y + 176, 1070, y + 176, TEAL, 6) + text(1078, y + 182, "新しい鎖", 14, TEAL_D))
    return svg("".join(b), "塩基のペアの決まり（相補性）とDNAのコピー",
               "A はT と、G はC とだけ組む。だから鎖が1本あれば、もう1本を正確に作り直せる。")


FIGS = [
    dict(svg=fig1, alt="DNAの二重らせんのつくりを示す図。糖とリン酸でできた2本の鎖を塩基対（A–T、G–C）がつなぎ、右巻きにねじれている。直径は約2nm、1回転は約3.4nmで塩基対10個分。A（アデニン）はT（チミン）と水素結合2本で、G（グアニン）はC（シトシン）と水素結合3本で組む。",
         caption="DNAの二重らせん。2本の鎖を塩基のペアがつなぎ、10ペアで1回転する右巻きのらせん。"),
    dict(svg=fig2, alt="DNAの相補性と複製の図。片方の鎖がATGCGTACCAなら相手の鎖はTACGCATGGTに決まることと、2本の鎖がほどけてそれぞれを型に新しい鎖ができ、同じDNAが2つできるようすを示している。",
         caption="相補性とDNAのコピー。AはT、GはCとだけ組むので、鎖が1本あればもう1本が決まる。"),
]
