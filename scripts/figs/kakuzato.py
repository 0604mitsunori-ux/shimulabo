"""角砂糖（kakuzato）の図。換算はページと同じ：角砂糖1個＝約4g、砂糖1g＝約4kcal、1年＝1日の量×365。WHO の目安（約25g＝角砂糖6個分）もページの本文どおり。
※ページの飲み物の砂糖の量（JS の値）は1本分として使うと少なすぎる疑いがあるため、図には飲み物ごとの数値を入れない（報告済み）。"""
from decimal import Decimal, ROUND_HALF_UP
from figlib import *

ANCHOR = r"毎日の習慣は見直しのきっかけに。</p>\n"
CUBE_G, KCAL_G = 4, 4
ROWS = [4, 10, 20, 25, 40, 60, 80]       # 砂糖の量（g）


def num(x):
    s = f"{x:.2f}".rstrip("0").rstrip(".")
    return s


def cubes(x, y, n, size=18, pitch=25, d=4):
    """角砂糖を n 個ならべる（端数は横に切った1個）。前の面＋上の面＋横の面の立方体"""
    out, i = [], 0
    while n - i > 1e-9:
        f = min(1, n - i); cx = x + i * pitch; w = size * f
        out.append(f'<path d="M{cx},{y + d} L{cx + d},{y} H{cx + w + d} L{cx + w},{y + d}Z" fill="#f4f1ea" stroke="{MUTED}" stroke-width="1.1" stroke-linejoin="round"/>')
        out.append(f'<path d="M{cx + w},{y + d} L{cx + w + d},{y} V{y + size} L{cx + w},{y + size + d}Z" fill="#e2ddd0" stroke="{MUTED}" stroke-width="1.1" stroke-linejoin="round"/>')
        out.append(f'<rect x="{cx}" y="{y + d}" width="{w}" height="{size}" fill="#ffffff" stroke="{MUTED}" stroke-width="1.3"/>')
        i += 1
    return "".join(out)


def fig1():
    b = []
    b.append(rect(48, 100, 1104, 50, TEAL_L, TEAL_L, 10))
    b.append(text(600, 133, "角砂糖の数＝砂糖(g)÷4　／　カロリー＝砂糖(g)×4kcal　／　1年分＝1日の量×365", 19, TEAL_D, 700, "middle"))
    X = [60, 196, 760, 880, 1010]          # 列：砂糖の量／角砂糖の絵／個数／カロリー／毎日1年
    hy = 184
    for x, t, anc in [(X[0] + 60, "1日の砂糖", "middle"), (X[1], "角砂糖（1個＝約4g）", "start"), (X[2] + 50, "個数", "middle"),
                      (X[3] + 60, "カロリー", "middle"), (X[4] + 70, "毎日なら1年で", "middle")]:
        b.append(text(x, hy, t, 16, INK2, 700, anc))
    b.append(line(48, hy + 12, 1152, hy + 12, INK, 1.2))
    rh = 56
    for i, g in enumerate(ROWS):
        y = hy + 16 + i * rh; n = g / CUBE_G
        who = (g == 25)
        if who:
            b.append(rect(52, y + 2, 1096, rh - 4, ACC_L, ACC, 8, 1.6))
        elif i % 2 == 1:
            b.append(f'<rect x="52" y="{y + 2}" width="1096" height="{rh - 4}" rx="6" fill="#f2efe7"/>')
        b.append(text(X[0] + 60, y + 36, f"{g}g", 22, ACC if who else INK, 700, "middle"))
        b.append(cubes(X[1], y + 16, n))
        lab = f"約{round(n)}個" if who else f"{num(n)}個"
        b.append(text(X[2] + 50, y + 36, lab, 21, ACC if who else INK, 700, "middle"))
        b.append(text(X[3] + 60, y + 36, f"{g * KCAL_G}kcal", 19, INK, anchor="middle"))
        kg = (Decimal(g * 365) / 1000).quantize(Decimal("0.1"), ROUND_HALF_UP)      # 3.65kg → 3.7kg（10進で四捨五入）
        b.append(text(X[4] + 70, y + 36, f"約{kg}kg", 19, INK, anchor="middle"))
        if who:
            b.append(text(X[1] + 7 * 25 + 14, y + 34, "← WHOがすすめる1日の目安", 16, ACC, 700))
    return svg("".join(b), "砂糖の量を角砂糖で数える（角砂糖1個＝約4g）",
               "WHOは1日の糖類を約25g（角砂糖6個分）以下にとすすめている。飲み物の糖分は気づかないうちにとりすぎやすい。")


FIGS = [
    dict(svg=fig1, alt="砂糖の量を角砂糖の個数に換算した早見表。角砂糖1個＝約4gとして、4g・10g・20g・25g・40g・60g・80gの砂糖が角砂糖何個分か、何kcalか、毎日とると1年で何kgになるかを角砂糖の絵で示し、WHOがすすめる1日約25g（角砂糖6個分）の目安を強調している。",
         caption="砂糖の量と角砂糖の個数の早見表。角砂糖1個＝約4g、砂糖1g＝約4kcal。"),
]
