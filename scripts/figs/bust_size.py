"""バストサイズ計算（bust-size）の図。判定はページの JS と同じ：
差＝トップ−アンダー、カップ＝CUPS[Math.round((差−7.5)÷2.5)]（AA=7.5cm から2.5cmごと）、アンダー区分＝Math.round(アンダー÷5)×5（±2.5cm）。
人体は描かない（線と数値だけ）。"""
import math
from figlib import *

ANCHOR = r'<div class="note" style="border-left:4px solid var\(--teal\)">.*?</div>\n'
CUPS = ['AA', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
SHOW = CUPS[:8]                     # 早見はページの表と同じ AA〜G


def jsround(x):
    return math.floor(x + 0.5)


def cup_of(sa):
    return CUPS[max(0, min(len(CUPS) - 1, jsround((sa - 7.5) / 2.5)))]


def diff(c):
    return 7.5 + 2.5 * CUPS.index(c)


def num(v):
    return f"{v:g}"


# ページの JS と同じ判定になっているかの確かめ（境目は四捨五入で上のカップ）
assert cup_of(12.5) == "B" and cup_of(11.25) == "B" and cup_of(13.74) == "B" and cup_of(13.75) == "C" and cup_of(10) == "A"
assert jsround(72.4 / 5) * 5 == 70 and jsround(72.5 / 5) * 5 == 75 and jsround(67.5 / 5) * 5 == 70


def fig1():
    b = []
    # 上：式
    bx = [(60, 250, "トップバスト", "胸のいちばん高い位置"), (350, 250, "アンダーバスト", "胸のふくらみのすぐ下"),
          (640, 190, "差", "（cm）"), (900, 200, "カップ", "差で決まる")]
    for x, w, t, s in bx:
        b.append(rect(x, 104, w, 70, CARD, TEAL, 10, 1.8) + text(x + w / 2, 136, t, 21, INK, 700, "middle")
                 + text(x + w / 2, 162, s, 14, MUTED, anchor="middle"))
    b.append(line(319, 139, 341, 139, INK, 3.4) + text(620, 150, "＝", 30, INK, 700, "middle"))
    b.append(arrow(842, 139, 890, 139, "ink", 2.4))
    b.append(text(60, 214, "例：トップ82.5cm − アンダー70cm ＝ 差12.5cm → Bカップ → サイズ表記は「B70」（カップ＋アンダー）", 17, INK2))
    # 中：カップの目盛り（差）
    x0, x1, lo, hi = 100, 1000, 6.25, 26.25
    px = lambda v: x0 + (v - lo) * (x1 - x0) / (hi - lo)
    by, bh = 268, 66
    b.append(text(60, 254, "トップとアンダーの差（cm）とカップ", 17, INK, 700))
    for i, c in enumerate(SHOW):
        d = diff(c); a, e = px(d - 1.25), px(d + 1.25)
        hi_ = c == "B"
        b.append(f'<rect x="{a:.1f}" y="{by}" width="{e - a:.1f}" height="{bh}" fill="{ACC_L if hi_ else (TEAL_L if i % 2 == 0 else CARD)}" stroke="{LINE}" stroke-width="1"/>')
        b.append(text((a + e) / 2, by + 32, c, 26, ACC if hi_ else INK, 700, "middle"))
        b.append(text((a + e) / 2, by + 56, f"約{num(d)}", 15, INK2, anchor="middle"))
    b.append(f'<rect x="{x0}" y="{by}" width="{x1 - x0}" height="{bh}" fill="none" stroke="{INK}" stroke-width="1.6"/>')
    for i in range(len(SHOW) + 1):
        v = lo + 2.5 * i
        b.append(line(px(v), by + bh, px(v), by + bh + 8, INK, 1.4) + text(px(v), by + bh + 26, num(v), 14, MUTED, anchor="middle"))
    b.append(arrow(x1 + 10, by + bh / 2, x1 + 46, by + bh / 2, "muted", 2))
    b.append(lines(x1 + 54, by + 26, ["H・I・J・K…", "2.5cmごと"], 15, INK2))
    b.append(text(x0, by + bh + 52, "1カップ＝2.5cm。各カップは中心の値 ±1.25cm（例：B＝11.25cm以上13.75cm未満）。", 15.5, INK2))
    # 下：アンダー区分
    ux0, ulo, uhi = 100, 57.5, 92.5
    upx = lambda v: ux0 + (v - ulo) * (1000 - ux0) / (uhi - ulo)
    uy = 456
    b.append(text(60, uy - 14, "アンダーバスト（cm）の区分（サイズ表記の数字）", 17, INK, 700))
    for i, u in enumerate(range(60, 95, 5)):
        a, e = upx(u - 2.5), upx(u + 2.5)
        hi_ = u == 70
        b.append(f'<rect x="{a:.1f}" y="{uy}" width="{e - a:.1f}" height="54" fill="{ACC_L if hi_ else (GOLD_L if i % 2 == 0 else CARD)}" stroke="{LINE}" stroke-width="1"/>')
        b.append(text((a + e) / 2, uy + 35, str(u), 22, ACC if hi_ else INK, 700, "middle"))
    b.append(f'<rect x="{ux0}" y="{uy}" width="900" height="54" fill="none" stroke="{INK}" stroke-width="1.6"/>')
    for i in range(8):
        v = ulo + 5 * i
        b.append(line(upx(v), uy + 54, upx(v), uy + 62, INK, 1.4) + text(upx(v), uy + 80, num(v), 14, MUTED, anchor="middle"))
    b.append(lines(1010, uy + 20, ["5cmごと", "（±2.5cm）"], 15, INK2))
    return svg("".join(b), "カップ数のしくみ（トップとアンダーの差で決まる）",
               "カップ・アンダーの区分はJIS L4006の考え方にそった目安。同じ表記でもメーカーで着け心地は変わる。")


def fig2():
    b = []
    unders = list(range(60, 95, 5))
    x0, y0 = 60, 110
    cw0, cw, hh, rh = 170, 115, 64, 52
    tw_ = cw0 + cw * len(SHOW)
    b.append(rect(x0, y0, tw_, hh + rh * len(unders), CARD, LINE, 10))
    b.append(f'<rect x="{x0}" y="{y0}" width="{tw_}" height="{hh}" rx="10" fill="{TEAL_L}"/>')
    b.append(text(x0 + cw0 / 2, y0 + 28, "カップ →", 16, INK, 700, "middle") + text(x0 + cw0 / 2, y0 + 52, "アンダー ↓", 16, INK, 700, "middle"))
    for j, c in enumerate(SHOW):
        cx = x0 + cw0 + cw * j + cw / 2
        b.append(text(cx, y0 + 30, c, 22, INK, 700, "middle") + text(cx, y0 + 52, f"差{num(diff(c))}", 14, INK2, anchor="middle"))
    for i, u in enumerate(unders):
        yy = y0 + hh + rh * i
        if i % 2 == 1:
            b.append(f'<rect x="{x0 + 1}" y="{yy}" width="{tw_ - 2}" height="{rh}" fill="#f7f5ef"/>')
        b.append(line(x0, yy, x0 + tw_, yy, LINE, 1))
        b.append(text(x0 + cw0 / 2, yy + 33, f"{u}", 20, INK, 700, "middle"))
        for j, c in enumerate(SHOW):
            top = u + diff(c)
            assert cup_of(top - u) == c
            cx = x0 + cw0 + cw * j + cw / 2
            if u == 70 and c == "B":
                b.append(rect(cx - cw / 2 + 4, yy + 5, cw - 8, rh - 10, ACC_L, ACC, 6, 1.6))
                b.append(text(cx, yy + 33, num(top), 19, ACC, 700, "middle"))
            else:
                b.append(text(cx, yy + 33, num(top), 18, INK, 400, "middle"))
    b.append(line(x0 + cw0, y0, x0 + cw0, y0 + hh + rh * len(unders), LINE, 1.2))
    b.append(text(x0, y0 + hh + rh * len(unders) + 32,
                  "表の数字＝トップバストの目安（アンダー＋差）。例：アンダー70cm・トップ82.5cm → B70。", 16, INK2))
    return svg("".join(b), "ブラのサイズ早見表（トップバストの目安・cm）",
               "カップを1つ上げてアンダーを1つ下げると容量が近い「兄弟サイズ」（例：B70とA75）。")


FIGS = [
    dict(svg=fig1, alt="バストサイズのカップ数のしくみの図。トップバストからアンダーバストを引いた差でカップが決まり、差が約7.5cmでAA、約10cmでA、約12.5cmでB、以降2.5cmごとにC・D・E・F・Gと1カップずつ上がることと、アンダーバストが5cmごとの区分（65・70・75…）になることを、線と数値の目盛りで示す。",
         caption="カップ数のしくみ。差10cmでA、そこから2.5cmごとに1カップ上がる（JIS）。"),
    dict(svg=fig2, alt="ブラのサイズ早見表。アンダーバスト60〜90cmとカップAA〜Gの組み合わせごとに、トップバストの目安（例：B70ならトップ82.5cm、C75なら90cm）を一覧にした表。",
         caption="サイズ表記ごとのトップバストの目安。アンダーに差（カップ）を足した値。"),
]
