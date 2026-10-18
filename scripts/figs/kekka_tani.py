"""欠課時数・単位シミュレーター（kekka-tani）の図。
式はページの JS と同じ：上限 = floor(年間授業時数 × 上限の割合)、あと休める = 上限 − これまでの欠課。
判定：あと<0 上限超過の可能性 / ≤2 危険ライン / ≤5 余裕少なめ / それ以上 まだ余裕あり。例はシミュの初期値（70コマ・欠課10・33%）。
1単位＝35単位時間（1単位時間50分）は高等学校学習指導要領の標準。"""
import math
from figlib import *

ANCHOR = r'<div class="note"><strong>計算式</strong>.*?</div>\s*<p>.*?</p>\n'
TOTAL, ABS, LIM = 70, 10, 33


def upper(total, lim=LIM):
    """JS：Math.floor(total*lim)（lim は ％÷100）"""
    return math.floor(total * (lim / 100))


def fig1():
    b = []
    mx = upper(TOTAL); left = mx - ABS
    b.append(text(60, 122, f"例：年間{TOTAL}コマの科目（2単位＝週2コマ）、これまでの欠課{ABS}コマ、上限{LIM}%（シミュの初期値）", 18, INK, 700))
    x0, x1, by, bh = 60, 1140, 180, 56
    cw = (x1 - x0) / TOTAL
    for i in range(TOTAL):
        if i < ABS: f, s = ACC, ACC
        elif i < mx: f, s = GOLD_L, GOLD
        else: f, s = TEAL_L, "#c9dbe4"
        b.append(f'<rect x="{x0 + i * cw + 1:.1f}" y="{by}" width="{cw - 2:.1f}" height="{bh}" rx="2" fill="{f}" stroke="{s}" stroke-width="1"/>')
    bx = x0 + mx * cw
    b.append(line(bx, by - 18, bx, by + bh + 8, INK, 3))
    b.append(text(bx, by - 26, f"欠課の上限 {mx}コマ", 17, INK, 700, "middle"))
    # かっこと説明
    for a, c, col, s1, s2 in [(0, ABS, ACC, f"これまでの欠課", f"{ABS}コマ"),
                              (ABS, mx, GOLD, "あと休める", f"{left}コマ"),
                              (mx, TOTAL, TEAL, "上限をこえないために出席が必要", f"{TOTAL - mx}コマ")]:
        xa, xc = x0 + a * cw + 2, x0 + c * cw - 2
        yb = by + bh + 14
        b.append(f'<path d="M{xa:.1f},{yb} v8 H{xc:.1f} v-8" fill="none" stroke="{col}" stroke-width="2"/>')
        b.append(text((xa + xc) / 2, yb + 34, s1, 16, col, 700, "middle") + text((xa + xc) / 2, yb + 60, s2, 20, col, 700, "middle"))
    # 式
    b.append(rect(60, 340, 1080, 104, CARD, LINE, 10))
    b.append(badge(88, 374, "1", TEAL, "#fff", 15) + text(112, 380, "欠課の上限 ＝ 年間授業時数 × 上限の割合（端数は切り捨て）", 18, INK, 700)
             + text(1118, 380, f"{TOTAL} × {LIM}% ＝ {TOTAL * LIM / 100:.1f} → {mx}コマ", 18, INK, 700, "end"))
    b.append(badge(88, 418, "2", TEAL, "#fff", 15) + text(112, 424, "あと休める回数 ＝ 欠課の上限 − これまでの欠課", 18, INK, 700)
             + text(1118, 424, f"{mx} − {ABS} ＝ {left}コマ", 18, ACC, 700, "end"))
    # 判定のめやす
    b.append(text(60, 488, "シミュの判定（あと休める回数）", 17, INK, 700))
    judges = [("6コマ以上", "まだ余裕あり", TEAL_L, TEAL), ("3〜5コマ", "余裕少なめ", GOLD_L, GOLD),
              ("0〜2コマ", "危険ライン！注意", ACC_L, ACC), ("マイナス", "上限超過の可能性（要相談）", "#f2d6cf", ACC)]
    w = [230, 230, 250, 340]; xx = 60
    for (k, v, f, s), ww in zip(judges, w):
        b.append(rect(xx, 502, ww - 12, 64, f, s, 8, 1.4) + text(xx + (ww - 12) / 2, 527, k, 15, INK2, anchor="middle")
                 + text(xx + (ww - 12) / 2, 554, v, 17, s, 700, "middle"))
        xx += ww
    b.append(text(60, 600, "遅刻・早退を「3回で1欠課」などと換算する学校もある。基準は校則・担任に確認を。", 15.5, INK2))
    return svg("".join(b), "あと何回休める？ 欠課時数の上限のしくみ",
               "1マス＝1コマ。欠課が上限をこえると単位が認められないことがある（基準は学校でちがう）。")


def fig2():
    b = []
    b.append(text(60, 124, "単位数ごとの欠課の上限（年間35週で計算）", 19, INK, 700))
    rows = []
    for u in range(1, 7):
        t = 35 * u; m = upper(t)
        rows.append([f"{u}単位", f"週{u}コマ", f"{t}コマ", f"{m}コマ", f"{t // 3}コマ", f"{m - 2}コマ〜", f"{m + 1}コマ"])
    cols = ["単位数", "週の授業", "年間授業時数", "上限（33%）", "上限（3分の1）", "危険ライン※", "上限をこえる欠課"]
    cw = [110, 120, 160, 160, 170, 160, 200]
    b.append(table(60, 142, cols, rows, cw, 52, 17.5))
    # 33% と 3分の1 で数がちがう所に印
    for i, u in enumerate(range(1, 7)):
        t = 35 * u
        if t // 3 != upper(t):
            cx = 60 + sum(cw[:4]) + cw[4] / 2 + 46
            b.append(text(cx, 142 + 52 * (i + 1) + 34, "◆", 15, ACC, anchor="middle"))
    b.append(lines(60, 548, ["※危険ライン＝あと休める回数が2コマ以下になる欠課数（上限33%で計算）。◆＝3分の1で数えると1コマ多い。",
                             "1単位は 1単位時間50分×35単位時間 が標準（高等学校学習指導要領）。週1コマ×35週＝1単位。"], 15.5, INK2, 1.75))
    return svg("".join(b), "欠課時数の上限 早見表（単位数別）",
               "上限の割合は学校の決まり（多くは3分の1）。シミュの初期値は33%。必ず校則・担任に確認を。")


FIGS = [
    dict(svg=fig1,
         alt="欠課時数の上限のしくみの図。年間70コマ（2単位）の科目で、欠課の上限は70×33%＝23コマ、これまでの欠課10コマなら、あと13コマ休めることを1マス1コマの帯で示し、あと休める回数による判定（まだ余裕あり・余裕少なめ・危険ライン・上限超過）をまとめている。",
         caption="欠課時数の上限のしくみ。上限＝年間授業時数×上限の割合（切り捨て）、あと休める＝上限−これまでの欠課。"),
    dict(svg=fig2,
         alt="高校の単位数（1〜6単位）ごとの欠課時数の早見表。週の授業コマ数、年間授業時数（35週）、欠課の上限（33%と3分の1）、危険ライン、上限をこえる欠課数をまとめた表。",
         caption="単位数別の欠課の上限（早見表）。2単位（年間70コマ）なら上限23コマ、24コマ欠課で上限をこえる。"),
]
