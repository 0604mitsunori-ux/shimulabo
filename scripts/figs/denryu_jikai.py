"""電流と磁界（denryu-jikai）の授業用の図。
向きはページのシミュ・本文と同じきまりで描く：
  右ねじの法則（上向きの電流→上から見て反時計回りの磁界）、コイルは右手の4本の指＝電流・親指＝N極、
  フレミングの左手の法則（中指＝電流・人差し指＝磁界・親指＝力。F＝I×B）、
  電磁誘導（近づくN極をしりぞけるように、コイルの磁石側のはしがN極になる）。
図の向きは scripts/figs 内の check で外積を計算して確かめた（下の _check）。"""
import math
from figlib import *

FLD, CUR, FRC = TEAL, ACC, GREEN      # 磁界＝藍、電流＝朱、力＝緑（文字でも区別する）


def head(x, y, dx, dy, col, s=8):
    l = math.hypot(dx, dy) or 1; ux, uy = dx / l, dy / l
    bx, by = x - ux * s * 1.6, y - uy * s * 1.6
    return (f'<path d="M{x:.1f},{y:.1f} L{bx - uy * s * 0.8:.1f},{by + ux * s * 0.8:.1f} '
            f'L{bx + uy * s * 0.8:.1f},{by - ux * s * 0.8:.1f}Z" fill="{col}"/>')


def compass(x, y, ang):
    """方位磁針。ang＝N極の向き（画面の角度・ラジアン、右＝0、下＝＋）"""
    c, s = math.cos(ang), math.sin(ang); L, w = 14, 4.6
    n = f"{x + c * L:.1f},{y + s * L:.1f} {x - s * w:.1f},{y + c * w:.1f} {x + s * w:.1f},{y - c * w:.1f}"
    so = f"{x - c * L:.1f},{y - s * L:.1f} {x - s * w:.1f},{y + c * w:.1f} {x + s * w:.1f},{y - c * w:.1f}"
    return (circle(x, y, 18, CARD, MUTED, 1.4) + f'<polygon points="{n}" fill="{ACC}"/>'
            + f'<polygon points="{so}" fill="#d6d0c2" stroke="{MUTED}" stroke-width="0.8"/>' + circle(x, y, 2.4, INK, INK, 0))


def dot_out(x, y, r=17, col=CUR):
    """⊙：電流が手前（見ている人の方）へ"""
    return circle(x, y, r, CARD, col, 2.6) + circle(x, y, 4.5, col, col, 0)


def cross_in(x, y, r=17, col=CUR):
    """⊗：電流が向こう（紙の裏）へ"""
    d = r * 0.62
    return (circle(x, y, r, CARD, col, 2.6) + line(x - d, y - d, x + d, y + d, col, 2.6) + line(x + d, y - d, x - d, y + d, col, 2.6))


def solenoid(x0, x1, cy, ry, n, col_cur=True):
    """コイル（輪を横に並べた形）。実線＝手前の半分、点線＝向こう側の半分。
    手前の半分を流れる電流を上向き（矢印）にかく → 右手の親指は左を向き、左はしがN極。"""
    out = []
    p = (x1 - x0) / (n - 1)
    for k in range(n):
        x = x0 + k * p
        out.append(f'<path d="M{x:.1f},{cy - ry} A9,{ry} 0 0 0 {x:.1f},{cy + ry}" fill="none" stroke="{MUTED}" stroke-width="1.6" stroke-dasharray="4 3"/>')
        out.append(f'<path d="M{x:.1f},{cy + ry} A9,{ry} 0 0 0 {x:.1f},{cy - ry}" fill="none" stroke="#9a6a1c" stroke-width="3.6"/>')
        if col_cur and k % 2 == 0:
            out.append(head(x + 9, cy - 4, 0, -1, CUR, 6.5))
    return "".join(out)


def card(x, y, w, h, no, title, sub):
    return (rect(x, y, w, h, CARD, LINE, 12) + badge(x + 28, y + 32, no, TEAL, "#fff", 17)
            + text(x + 52, y + 39, title, 19, INK, 700) + text(x + 20, y + 70, sub, 16, TEAL_D, 700))


def fig1():
    b = []
    # ① 電流がつくる磁界（上から見た図）
    x, w = 48, 352
    b.append(card(x, 100, w, 512, "1", "電流がつくる磁界", "右ねじの法則"))
    cx, cy = x + w / 2, 330
    b.append(text(cx, 204, "上から見た図", 15, MUTED, anchor="middle"))
    for r in (42, 78, 112):
        b.append(circle(cx, cy, r, "none", FLD, 2))
        for t in (math.radians(35), math.radians(215)):        # 反時計回り（画面では y が下向きなので sin を引く）
            px, py = cx + r * math.cos(t), cy - r * math.sin(t)
            b.append(head(px, py, -math.sin(t), -math.cos(t), FLD, 6.5))
    for t in (0, 90, 180, 270):
        tr = math.radians(t); r = 78
        px, py = cx + r * math.cos(tr), cy - r * math.sin(tr)
        b.append(compass(px, py, math.atan2(-math.cos(tr), -math.sin(tr))))
    b.append(dot_out(cx, cy))
    b.append(text(cx + 140, cy + 96, "磁界", 16, FLD, 700, "end"))
    b.append(lines(x + 20, 476, ["⊙＝電流が上向き（見ている人の方へ）", "→ 磁界は上から見て反時計回り", "右ねじを電流の向きに進めるとき、", "ねじを回す向き＝磁界の向き"], 15.5, INK, 1.55))
    # ② 磁界の中の電流が受ける力
    x = 424
    b.append(card(x, 100, w, 512, "2", "電流が磁界から受ける力", "フレミングの左手の法則"))
    cy = 288
    b.append(rect(x + 20, cy - 58, 54, 116, ACC_L, ACC, 4, 2) + text(x + 47, cy + 9, "N", 26, ACC, 700, "middle"))
    b.append(rect(x + w - 74, cy - 58, 54, 116, TEAL_L, TEAL, 4, 2) + text(x + w - 47, cy + 9, "S", 26, TEAL, 700, "middle"))
    for yy in (cy - 38, cy + 38):
        b.append(arrow(x + 82, yy, x + w - 84, yy, "teal", 2.2))
    b.append(arrow(x + 82, cy, x + w / 2 - 26, cy, "teal", 2.2) + arrow(x + w / 2 + 22, cy, x + w - 84, cy, "teal", 2.2))
    b.append(cross_in(x + w / 2, cy))
    b.append(arrow(x + w / 2, cy + 22, x + w / 2, cy + 100, "green", 4))
    b.append(text(x + w / 2 + 14, cy + 94, "力", 20, FRC, 700))
    b.append(text(x + w / 2, cy - 72, "磁界（N極 → S極）", 15, FLD, 700, "middle"))
    b.append(text(x + 20, cy + 82, "⊗＝電流が", 15, CUR, 700) + text(x + 20, cy + 104, "紙の裏へ", 15, CUR, 700))
    b.append(text(x + 20, 440, "左手の3本の指を直角に開くと", 15.5, INK))
    for i, (k, v, c) in enumerate([("中指", "電流", CUR), ("人差し指", "磁界", FLD), ("親指", "力", FRC)]):
        b.append(text(x + 36, 466 + i * 25, f"{k} ＝ {v}", 16, c, 700))
    b.append(text(x + 130, 516, "（中指から「電・磁・力」）", 15, INK2))
    b.append(lines(x + 20, 562, ["電流か磁界の一方を反対にすると、", "力も反対の向きになる。"], 15.5, INK2, 1.55))
    # ③ 電磁誘導
    x = 800
    b.append(card(x, 100, w, 512, "3", "電磁誘導", "磁界が変わると電流が流れる"))
    cy = 262
    b.append(rect(x + 18, cy - 17, 42, 34, TEAL_L, TEAL, 3, 1.8) + rect(x + 60, cy - 17, 42, 34, ACC_L, ACC, 3, 1.8))
    b.append(text(x + 39, cy + 7, "S", 19, TEAL, 700, "middle") + text(x + 81, cy + 7, "N", 19, ACC, 700, "middle"))
    b.append(arrow(x + 28, cy - 40, x + 100, cy - 40, "ink", 2.6) + text(x + 22, cy - 52, "N極を近づける", 15, INK, 700))
    c0, c1 = x + 150, x + 300
    b.append(solenoid(c0, c1, cy, 44, 8))
    b.append(text(c0 - 4, cy - 56, "N", 22, ACC, 700, "middle") + text(c1 + 8, cy - 56, "S", 22, TEAL, 700, "middle"))
    b.append(arrow(c0 + 110, cy, c0 + 30, cy, "teal", 2.2))
    # 検流計
    gx, gy = x + 226, 400
    b.append(poly([(c0, cy + 44), (c0, gy), (gx - 46, gy)], INK, 2) + poly([(c1, cy + 44), (c1, gy), (gx + 46, gy)], INK, 2))
    b.append(rect(gx - 46, gy - 30, 92, 56, CARD, INK2, 8, 1.6))
    b.append(f'<path d="M{gx - 30},{gy + 8} A34,34 0 0 1 {gx + 30},{gy + 8}" fill="none" stroke="{MUTED}" stroke-width="1.4"/>')
    a = math.radians(-90 + 40)
    b.append(line(gx, gy + 18, gx + 30 * math.cos(a), gy + 18 + 30 * math.sin(a), ACC, 2.6) + circle(gx, gy + 18, 3.5, INK, INK, 0))
    b.append(text(gx, gy + 50, "検流計（針がふれる）", 15, INK, 700, "middle"))
    b.append(lines(x + 20, 476, ["コイルの左はしがN極になり、", "近づくN極をしりぞける", "向きに誘導電流が流れる。", "磁石を止めると電流は流れない。"], 15.5, INK, 1.55))
    return svg("".join(b), "電流と磁界のしくみ（3つの関係）",
               "朱＝電流、藍＝磁界（磁力線）、緑＝力。方位磁針は色のついた方がN極。")


def fig2():
    b = []
    # 左上：コイルのまわりの磁界
    b.append(rect(48, 100, 540, 264, CARD, LINE, 12))
    b.append(text(68, 134, "コイルのまわりの磁界（電磁石）", 19, INK, 700))
    cy, c0, c1 = 232, 210, 410
    for k, s in [(1, 1), (1, -1), (2, 1), (2, -1)]:          # 外側の磁力線（N極から出てS極へ）
        hh = 62 + 16 * k
        d = f"M{c0 - 18},{cy - s * 12} C{c0 - 90 - 20 * k},{cy - s * hh} {c1 + 90 + 20 * k},{cy - s * hh} {c1 + 18},{cy - s * 12}"
        b.append(f'<path d="{d}" fill="none" stroke="{FLD}" stroke-width="1.8" opacity=".75"/>')
        b.append(head((c0 + c1) / 2 + 6, cy - s * (hh * 0.75 + 3), 1, 0, FLD, 6))
    b.append(solenoid(c0, c1, cy, 40, 9))
    b.append(arrow(c1 - 30, cy, c0 + 30, cy, "teal", 2.6))
    b.append(text(c0 - 30, cy + 8, "N", 26, ACC, 700, "end") + text(c1 + 30, cy + 8, "S", 26, TEAL, 700))
    b.append(lines(68, 326, ["右手の4本の指を電流の向きに合わせてにぎると、親指の側がN極。", "（朱の矢印＝手前側の導線を流れる電流の向き）"], 15.5, INK, 1.45))
    # 右上：力の向き
    b.append(text(612, 126, "電流が受ける力の向き（電気ぶらんこ・モーター）", 18, INK, 700))
    b.append(table(612, 140, ["電流の向き", "磁界の向き", "力の向き"],
                   [["もとのまま", "もとのまま", "もとの向き"], ["反対", "もとのまま", "反対の向き"],
                    ["もとのまま", "反対", "反対の向き"], ["反対", "反対", "もとの向き"]], [180, 180, 180], 42, 16))
    # 左下：電磁誘導
    b.append(text(48, 392, "電磁誘導（コイルに磁石を出し入れする）", 18, INK, 700))
    b.append(table(48, 406, ["操作", "検流計の針", "コイルの左はし"],
                   [["N極を入れる", "右にふれる", "N極"], ["N極を出す", "左にふれる", "S極"], ["S極を入れる", "左にふれる", "S極"],
                    ["S極を出す", "右にふれる", "N極"], ["磁石を止める", "ふれない", "—"]], [170, 180, 190], 34, 15.5))
    # 右下：強くするには
    b.append(rect(612, 362, 540, 252, GOLD_L, LINE, 12))
    b.append(text(632, 394, "強くする・大きくするには", 18, INK, 700))
    for i, (k, v) in enumerate([("電磁石", "電流を大きく・巻き数をふやす・鉄しんを入れる"), ("力", "電流を大きく・磁石を強く"),
                                ("誘導電流", "磁石を速く動かす・強い磁石・巻き数をふやす")]):
        yy = 428 + i * 32
        b.append(text(632, yy, k, 16, TEAL_D, 700) + text(724, yy, v, 16, INK))
    b.append(line(632, 512, 1132, 512, LINE, 1.2))
    b.append(lines(632, 540, ["モーター：整流子で半回転ごとに電流の向きを切りかえ、", "　　　　　同じ向きに回り続ける。",
                              "発電機：回し続けると向きが変わる電流（交流）ができる。"], 15.5, INK2, 1.5))
    return svg("".join(b), "電流と磁界のまとめ（向きのきまりと強さ）",
               "検流計は、N極を入れたときに右へふれるようにつないだ場合（シミュの図と同じ）。")


def _check():
    """向きの確かめ（x 右・y 上・z 手前の右手系）"""
    def cx(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
    assert cx((0, 0, -1), (1, 0, 0)) == (0, -1, 0)          # ⊗電流×右向き磁界＝下向きの力
    assert cx((-1, 0, 0), (0, 0, 1)) == (0, 1, 0)           # 親指が左（N極が左）のとき、手前の導線の電流は上向き


_check()

FIGS = [
    dict(svg=fig1, alt="電流と磁界の3つの関係を示す図。①上向きの電流のまわりに上から見て反時計回りの同心円状の磁界ができ方位磁針がその向きを指す（右ねじの法則）、②N極からS極への磁界の中で紙の裏へ流れる電流が下向きの力を受ける（フレミングの左手の法則：中指＝電流・人差し指＝磁界・親指＝力）、③コイルに磁石のN極を近づけるとコイルの左はしがN極になる向きに誘導電流が流れ検流計の針がふれる（電磁誘導）。",
         caption="電流と磁界の3つの関係。電流は磁界をつくり、磁界の中の電流は力を受け、磁界が変わると電流が流れる。"),
    dict(svg=fig2, alt="電流と磁界のまとめ。コイルのまわりの磁界（右手の4本の指を電流の向きに合わせると親指の側がN極）、電流や磁界の向きを反対にしたときの力の向きの表、磁石のN極・S極を入れる・出す・止めるときの検流計の針とコイルの極の表、電磁石・力・誘導電流を強くする方法とモーター・発電機のしくみ。",
         caption="向きのきまりの早見表。電流か磁界の一方を反対にすると力も反対、両方反対にするともとと同じ向き。"),
]
