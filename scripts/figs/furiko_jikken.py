"""振り子の実験（furiko-jikken・小5 振り子の運動）の授業用の図
時間はシミュ（scripts/rika/sims_chikara.py の FURIKO_JS）と同じ式：1往復 T＝2π√(L/g)（g＝9.8）、
10往復の時間＝Math.round(10T×100)/100、1往復の時間＝Math.round(10往復÷10×100)/100。おもりの重さ・振れ幅は式に入らない。"""
import math
from figlib import *

G = 9.8


def r2(v):
    return math.floor(v * 100 + 0.5) / 100          # JS の Math.round(v*100)/100 と同じ


def t10(cm):
    return r2(10 * 2 * math.pi * math.sqrt(cm / 100 / G))


def t1(cm):
    return r2(t10(cm) / 10)


def bob(x, y, r, faded=False):
    if faded:
        return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="none" stroke="{MUTED}" stroke-width="1.6" stroke-dasharray="4 3"/>'
    return circle(x, y, r, MOON_D, MOON_D, 0) + circle(x - r * 0.32, y - r * 0.32, r * 0.28, "#8a9099", "#8a9099", 0)


def pend(px, py, Lpx, deg, r, faded=False, string=INK2):
    t = math.radians(deg)
    bx, by = px + Lpx * math.sin(t), py + Lpx * math.cos(t)
    s = line(px, py, bx, by, MUTED if faded else string, 1.4 if faded else 2, "5 4" if faded else None)
    return s + bob(bx, by, r, faded), (bx, by)


def fig1():
    b = []
    PX, PY, L, A, R = 300, 134, 320, 20, 18
    # 支え
    b.append(rect(200, 120, 200, 12, "#cfc9bb", "#cfc9bb", 3))
    b.append(line(PX, PY, PX, PY + L + 46, MUTED, 1.4, "5 5"))
    # 振れる道すじ（ウ→イ→ア）
    ux, uy = PX - L * math.sin(math.radians(A)), PY + L * math.cos(math.radians(A))
    ax, ay = PX + L * math.sin(math.radians(A)), uy
    b.append(f'<path d="M{ux:.1f},{uy:.1f} A{L},{L} 0 0 0 {ax:.1f},{ay:.1f}" fill="none" stroke="{MUTED}" stroke-width="1.6" stroke-dasharray="5 5"/>')
    s, _ = pend(PX, PY, L, -A, R, faded=True); b.append(s)
    b.append(bob(PX, PY + L, R, faded=True))
    s, _ = pend(PX, PY, L, A, R); b.append(s)
    b.append(circle(PX, PY, 4, INK, INK, 0))
    # 振れ幅（角度）：アの側にかく
    ra = 82
    p0 = (PX, PY + ra); p1 = (PX + ra * math.sin(math.radians(A)), PY + ra * math.cos(math.radians(A)))
    b.append(f'<path d="M{p0[0]:.1f},{p0[1]:.1f} A{ra},{ra} 0 0 0 {p1[0]:.1f},{p1[1]:.1f}" fill="none" stroke="{ACC}" stroke-width="2.4"/>')
    b.append(text(PX + 40, PY + ra + 6, "振れ幅", 16, ACC, 700))
    # 振り子の長さ（ウの外側に寸法線）
    n = (-math.cos(math.radians(A)), -math.sin(math.radians(A)))     # ウの糸に直角・外向き
    off = 40
    s0 = (PX + n[0] * off, PY + n[1] * off); s1 = (ux + n[0] * off, uy + n[1] * off)
    b.append(line(PX, PY, s0[0] - n[0] * 4, s0[1] - n[1] * 4, TEAL, 1, "3 3") + line(ux, uy, s1[0] - n[0] * 4, s1[1] - n[1] * 4, TEAL, 1, "3 3"))
    mx, my = (s0[0] + s1[0]) / 2, (s0[1] + s1[1]) / 2
    b.append(arrow(mx, my, s0[0], s0[1], "teal", 2) + arrow(mx, my, s1[0], s1[1], "teal", 2))
    b.append(text(mx - 22, my - 14, "振り子の長さ", 18, TEAL, 700, "end"))
    b.append(lines(mx - 22, my + 12, ["（支点から", "おもりの中心まで）"], 15, TEAL, 1.45, anchor="end"))
    # ラベル
    b.append(line(PX + 104, 140, PX + 6, PY, INK2, 1))
    b.append(text(PX + 110, 146, "支点（糸をつるした所）", 16, INK, 700))
    b.append(text(PX + (L * 0.58) * math.sin(math.radians(A)) - 12, PY + L * 0.58 * math.cos(math.radians(A)) + 6, "糸", 16, INK, 700, "end"))
    b.append(text(ax + R + 10, ay + 6, "おもり", 16, INK, 700))
    b.append(badge(ax, ay + 44, "ア", ACC, "#fff", 16) + badge(PX, PY + L + 44, "イ", TEAL, "#fff", 16) + badge(ux, uy + 44, "ウ", TEAL, "#fff", 16))
    b.append(text(ax + 22, ay + 50, "手をはなす", 15, ACC, 700))
    # ---- 右：1往復とは
    b.append(text(660, 128, "1往復とは", 20, INK, 700))
    seq = [("ア", 25, ACC), ("イ", 0, TEAL), ("ウ", -25, TEAL), ("イ", 0, TEAL), ("ア", 25, ACC)]
    for i, (k, d, col) in enumerate(seq):
        cx = 690 + i * 100
        b.append(line(cx - 26, 150, cx + 26, 150, "#b9b3a5", 4))
        s, (bx, by) = pend(cx, 152, 92, d, 10); b.append(s)
        b.append(badge(cx, 282, k, col, "#fff", 15))
        if i < 4:
            b.append(arrow(cx + 20, 282, cx + 82, 282, "muted", 2))
    b.append(lines(660, 326, ["手をはなした所（ア）から反対側（ウ）まで行き、", "またアにもどってくるまでが「1往復」。"], 16, INK2, 1.5))
    # 1往復の時間の求め方
    b.append(text(660, 400, "1往復の時間の求め方", 20, INK, 700))
    b.append(rect(650, 414, 496, 200, CARD, LINE, 10))
    b.append(text(670, 450, "1往復の時間 ＝ 10往復の時間 ÷ 10", 21, ACC, 700))
    T10, T1 = t10(50), t1(50)
    b.append(text(670, 482, f"例（長さ50cm）：10往復が{T10:.2f}秒なら、", 16, INK))
    b.append(text(670, 507, f"{T10:.2f} ÷ 10 ＝ {T10 / 10:.3f} → 1往復は約{T1:.2f}秒", 16, INK, 700))
    b.append(lines(670, 545, ["1往復は短いので、10往復を計って10でわると、", "計るときのずれが10分の1になる。",
                              "同じ条件で3回計って平均をとると、より正しくなる。"], 16, INK2, 1.6))
    return svg("".join(b), "振り子の1往復と、振り子の長さ",
               "振り子の長さは、支点からおもりの中心まで。振れ幅は大きくしすぎないようにする。")


def fig2():
    b = []
    S = 2.6                                   # 1cm を 2.6px（3つのパネルで同じちぢめ方）
    panels = [("おもりの重さだけ変える", "変えない条件：長さ50cm・振れ幅20°",
               [(50, 20, 10), (50, 20, 30), (50, 20, 50)], lambda c: f"{c[2]}g", [62, 162, 262], False),
              ("振れ幅だけ変える", "変えない条件：長さ50cm・おもり10g",
               [(50, 10, 10), (50, 20, 10), (50, 30, 10)], lambda c: f"{c[1]}°", [62, 162, 262], False),
              ("振り子の長さだけ変える", "変えない条件：おもり10g・振れ幅20°",
               [(25, 20, 10), (50, 20, 10), (100, 20, 10)], lambda c: f"{c[0]}cm", [52, 146, 236], True)]
    for i, (ttl, sub, conds, lab, xs, changes) in enumerate(panels):
        px = 48 + i * 376
        b.append(rect(px, 96, 352, 522, CARD, LINE, 10))
        b.append(f'<rect x="{px}" y="96" width="352" height="64" rx="10" fill="{ACC_L if changes else TEAL_L}"/>')
        b.append(text(px + 176, 124, ttl, 19, INK, 700, "middle"))
        b.append(text(px + 176, 149, sub, 14.5, INK2, anchor="middle"))
        b.append(line(px + 18, 178, px + 334, 178, "#b9b3a5", 5))
        times = []
        for c, x in zip(conds, xs):
            Lcm, deg, w = c
            cx = px + x
            b.append(line(cx, 180, cx, 180 + Lcm * S + 16, LINE, 1.2, "4 4"))
            s, _ = pend(cx, 180, Lcm * S, deg, 9 * (w / 10) ** (1 / 3)); b.append(s)   # おもりの大きさはシミュと同じく重さの3乗根
            b.append(circle(cx, 180, 3, INK, INK, 0))
            b.append(text(cx, 466, lab(c), 19, INK, 700, "middle"))
            T10, T1 = t10(Lcm), t1(Lcm); times.append(T1)
            b.append(text(cx, 524, f"{T1:.2f}秒", 21, ACC if changes else TEAL_D, 700, "middle"))
            b.append(text(cx, 547, f"({T10:.2f}秒)", 14, MUTED, anchor="middle"))
        b.append(text(px + 176, 494, "↓ 1往復の時間（かっこは10往復）", 14.5, INK2, anchor="middle"))
        same = len(set(times)) == 1
        assert same != changes
        b.append(rect(px + 14, 562, 324, 44, ACC_L if changes else TEAL_L, ACC if changes else TEAL, 8, 1.4))
        b.append(text(px + 176, 591, "長いほど1往復の時間が長い" if changes else "1往復の時間は変わらない", 18, ACC if changes else TEAL_D, 700, "middle"))
    return svg("".join(b), "振り子の1往復の時間は何で変わる？（条件をそろえて比べる）",
               f"長さを4倍（25cm→100cm）にすると、1往復の時間は約2倍（{t1(25):.2f}秒→{t1(100):.2f}秒）になる。")


FIGS = [
    dict(svg=fig1, alt="振り子の実験のしくみの図。支点（糸をつるした所）、糸、おもり、振れ幅、振り子の長さ（支点からおもりの中心まで）を示し、手をはなした所アから反対側ウへ行ってアにもどるまでが1往復であること、1往復の時間＝10往復の時間÷10（長さ50cmで10往復14.19秒→約1.42秒）の求め方を示す。",
         caption="振り子の1往復と振り子の長さ。1往復の時間は、10往復の時間を計って10でわって求める。"),
    dict(svg=fig2, alt="振り子の1往復の時間を、条件を1つだけ変えて比べたまとめ図。おもりの重さ（10g・30g・50g）や振れ幅（10°・20°・30°）を変えても1往復は1.42秒で変わらず、振り子の長さを25cm・50cm・100cmにすると1.00秒・1.42秒・2.01秒と長くなる。",
         caption="条件を1つだけ変えて比べた結果。1往復の時間を変えるのは、振り子の長さだけ。"),
]
