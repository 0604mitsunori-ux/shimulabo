"""ご飯のカロリー（gohan-cal）の図。式はページの JS と同じ：kcal＝重さ(g)×1.68、糖質＝重さ×0.37、角砂糖＝kcal÷16（1個16kcal）。
盛りの重さもページの選択肢と同じ（小盛100g・茶碗1杯150g・大盛200g・丼250g）。"""
from decimal import Decimal, ROUND_HALF_UP
from figlib import *

ANCHOR = r'<div class="note" style="border-left:4px solid var\(--teal\)">.*?</div>\n'
SIZES = [("小盛", 100), ("茶碗1杯", 150), ("大盛", 200), ("丼", 250)]


def to_fixed(v, n):
    """JS の toFixed と同じ四捨五入（2進で正確に表せる .5 は切り上げ）"""
    return str(Decimal(v).quantize(Decimal(1).scaleb(-n), rounding=ROUND_HALF_UP))


def calc(g):
    kcal = g * 1.68
    return kcal, g * 0.37, kcal / 16


def fig1():
    b = []
    b.append(rect(48, 102, 1104, 100, CARD, LINE, 12))
    b.append(text(76, 144, "ご飯 100g ＝ 約168kcal・糖質 約37g", 26, INK, 700))
    b.append(text(76, 182, "カロリー（kcal）＝ ご飯の重さ（g）× 1.68　　糖質（g）＝ ご飯の重さ（g）× 0.37", 17, INK2))
    bx, kmax, bw = 300, 420, 520
    pxk = lambda k: bx + k * bw / kmax
    top, pitch = 268, 82
    b.append(text(60, 244, "盛り（ご飯の重さ）", 16, MUTED, 700) + text(bx, 244, "カロリー", 16, MUTED, 700)
             + text(1000, 244, "糖質", 16, MUTED, 700, "middle") + text(1098, 244, "角砂糖", 16, MUTED, 700, "middle"))
    ybot = top + pitch * len(SIZES) - 18
    for k in range(0, 401, 100):
        b.append(line(pxk(k), top - 4, pxk(k), ybot, LINE, 1) + text(pxk(k), ybot + 22, f"{k}", 14, MUTED, anchor="middle"))
    b.append(text(pxk(400) + 26, ybot + 22, "kcal", 14, MUTED))
    for i, (nm, g) in enumerate(SIZES):
        kcal, tou, kaku = calc(g)
        y = top + pitch * i
        hi = g == 150
        b.append(text(60, y + 30, nm, 21, INK, 700) + text(250, y + 30, f"{g}g", 19, INK2, anchor="end"))
        b.append(rect(bx, y + 2, pxk(kcal) - bx, 40, TEAL if hi else TEAL_L, TEAL, 6, 1.4))
        b.append(text(pxk(kcal) + 12, y + 31, f"約{kcal:.0f}kcal", 22, TEAL_D if not hi else INK, 700))
        b.append(text(1000, y + 30, f"約{to_fixed(tou, 1).rstrip('0').rstrip('.')}g", 19, INK, 700, "middle"))
        b.append(text(1098, y + 30, f"{to_fixed(kaku, 1)}個分", 19, INK, 700, "middle"))
    return svg("".join(b), "ご飯のカロリー早見（茶碗の量とカロリー・糖質）",
               "日本食品標準成分表（ごはん）をもとにした目安。角砂糖は1個16kcalとしてカロリーを置きかえた数。")


FIGS = [
    dict(svg=fig1, alt="ご飯のカロリーの早見図。ご飯100gで約168kcal・糖質約37g。小盛100gは約168kcal、茶碗1杯150gは約252kcal、大盛200gは約336kcal、丼250gは約420kcalで、糖質と角砂糖に換算した量を横棒グラフで比べている。",
         caption="ご飯のカロリー早見。茶碗1杯（150g）で約252kcal・糖質約55.5g。"),
]
