"""計量カップ換算（cup-kanzan）の図。値はページの JS と同じ：容量＝カップ数×カップの大きさ（200/180/240ml）、重さ＝容量×比重、大さじ＝容量÷15"""
import math
from figlib import *

ANCHOR = r"砂糖1カップ≒170g）。</p>\n"
CUPS = [("計量カップ（日本）", 200, "200ml"), ("米用カップ（1合）", 180, "180ml"), ("米国カップ", 240, "約240ml")]
FILL = [("水・牛乳", 1), ("小麦粉", 0.55), ("砂糖", 0.85), ("米", 0.83), ("油", 0.92)]   # ページの JS と同じ


def jr(x):
    return math.floor(x + 0.5)                 # JS の Math.round


def cup(cx, base, ml, col, tick_lab=True):
    k = 1.1; h = ml * k; w0, w1 = 150, 176      # 少し上が広い形
    top = base - h
    out = [f'<path d="M{cx - w0 / 2},{base} L{cx - w1 / 2},{top} L{cx + w1 / 2},{top} L{cx + w0 / 2},{base}Z" fill="{col}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>']
    hx = cx + w1 / 2 - (w1 - w0) / 2 * 0.3
    out.append(f'<path d="M{hx},{top + 30} q46,8 40,60 q-4,40 -46,48" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')  # 取っ手
    for v in range(50, ml, 50):                 # 50mlごとの目盛り（ふちの線とは重ねない）
        y = base - v * k; xw = cx - (w0 + (w1 - w0) * v / ml) / 2      # その高さの左の壁
        out.append(line(xw, y, xw + 26, y, INK, 1.6))
        if tick_lab: out.append(text(xw + 32, y + 5, f"{v}", 14, INK2))
    return "".join(out)


def fig1():
    b = []
    base = 470
    for (nm, ml, lab), cx, col in zip(CUPS, [200, 600, 1000], [TEAL_L, GOLD_L, "#efe9f3"]):
        top = base - ml * 1.1
        b.append(text(cx, top - 50, nm, 19, INK, 700, "middle"))
        b.append(text(cx, top - 14, lab, 30, TEAL_D if ml == 200 else INK, 700, "middle"))
        b.append(cup(cx, base, ml, col))
        o = ml / 15
        b.append(text(cx, base + 36, f"大さじ{o:.1f}杯分".replace(".0杯", "杯"), 18, INK2, anchor="middle"))
    b.append(line(80, base, 1120, base, MUTED, 1.4))
    b.append(rect(48, 534, 1104, 76, GOLD_L, "#e8d9b5", 10))
    b.append(text(72, 564, "日本のレシピの「1カップ」は200ml（1/2カップ＝100ml、1/4カップ＝50ml）", 18, INK, 700))
    b.append(text(72, 594, "お米の「1合」は180ml、アメリカのレシピの「1 cup」は約240ml。同じ「1カップ」でも量がちがう。", 16, INK2))
    return svg("".join(b), "1カップは何ml？ 計量カップの種類と容量",
               "カップの高さは容量に合わせた。目盛りは50mlごと。大さじ1＝15mlで換算。")


def fig2():
    b = []
    cols = [("1/2カップ", 100), ("1カップ", 200), ("2カップ", 400), ("米用カップ1杯", 180), ("米国カップ1杯", 240)]
    rows = [[nm] + [f"{jr(ml * d):,}g" for _, ml in cols] for nm, d in FILL]
    cw = [170, 180, 180, 180, 185, 185]
    x0, y0, rh = 60, 140, 64
    gx = x0 + cw[0]
    b.append(rect(gx, 104, sum(cw[1:4]), 30, TEAL_L, TEAL_L, 6) + text(gx + sum(cw[1:4]) / 2, 125, "計量カップ（200ml）", 16, TEAL_D, 700, "middle"))
    b.append(table(x0, y0, [""] * 6, rows, cw, rh, 20))
    b.append(text(x0 + cw[0] / 2, y0 + 41, "中身", 18, INK, 700, "middle"))
    cx = gx
    for (a, ml), w in zip(cols, cw[1:]):
        b.append(text(cx + w / 2, y0 + 28, a, 18, INK, 700, "middle") + text(cx + w / 2, y0 + 52, f"（{ml}ml）", 15, INK2, anchor="middle"))
        cx += w
    b.append(lines(60, 568, ["重さ＝容量（ml）×比重（水・牛乳1、小麦粉0.55、砂糖0.85、米0.83、油0.92）で計算した目安。",
                             "粉や砂糖は、詰め方で重さが変わる。正確さが必要なときは、はかりで量る。"], 16, INK2, 1.55))
    return svg("".join(b), "1カップは何グラム？ 中身別の早見表",
               "米用カップ1杯＝米1合（180ml）。米1合はおよそ150gになる。")


FIGS = [
    dict(svg=fig1, alt="計量カップの種類と容量の図。日本の計量カップは1カップ200ml（大さじ13.3杯分）、米用カップは1合180ml（大さじ12杯分）、米国カップは約240ml（大さじ16杯分）で、容量に合わせた高さのカップで比べている。",
         caption="1カップは何ml？ 日本の計量カップは200ml、米用カップ（1合）は180ml、米国カップは約240ml。"),
    dict(svg=fig2, alt="水・牛乳、小麦粉、砂糖、米、油を、計量カップ1/2・1・2カップ、米用カップ1杯（180ml）、米国カップ1杯（240ml）ではかったときの重さ（グラム）の早見表。小麦粉1カップ110g、砂糖1カップ170gなど。",
         caption="1カップは何グラム？ 中身によって重さが変わる（小麦粉1カップ≒110g、砂糖1カップ≒170g）。"),
]
