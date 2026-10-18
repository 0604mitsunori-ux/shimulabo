"""原子の構造と電子配置（denshi-haichi）の授業用の図（化学基礎）
数値はシミュ（scripts/rika/sims_kou_kagaku_seibutsu.py の DENSHI_JS）と同じ：
  conf(z)：1〜18番は K＝min(z,2)、L＝z−2（0〜8）、M＝z−10（0〜8）。19番 K2 L8 M8 N1、20番 K2 L8 M8 N2。
  族 group(z)・周期 period(z)・価電子 valence(z)（貴ガスは0）・イオン ION（Na⁺ は電子1個を失う、Cl⁻ は1個受け取る）。"""
import math
import re
from figlib import *

SYM = ["", "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca"]
NAME = {11: "ナトリウム", 17: "塩素", 10: "ネオン", 18: "アルゴン"}
SHN = ["K", "L", "M", "N"]
NOBLE = {2: "He", 10: "Ne", 18: "Ar"}
ION = {11: ("Na^+", "ナトリウムイオン", -1), 17: ("Cl^-", "塩化物イオン", 1)}
ISO_A = {11: 23, 17: 35}          # 代表的な質量数（シミュの ISO の先頭）
EC, VC, SC = TEAL, GOLD, GREEN    # 電子・価電子・安定な最外殻


def conf(z):
    if z <= 18: return [min(z, 2), max(0, min(z - 2, 8)), max(0, min(z - 10, 8)), 0]
    return {19: [2, 8, 8, 1], 20: [2, 8, 8, 2]}[z]


def group(z):
    if z == 1: return 1
    if z == 2: return 18
    if z <= 10: return z - 2 if z <= 4 else z + 8
    if z <= 18: return z - 10 if z <= 12 else z
    return z - 18


def period(z): return 1 if z <= 2 else 2 if z <= 10 else 3 if z <= 18 else 4
def outer(c): return max(i for i in range(4) if c[i] > 0)
def valence(z):
    g = group(z); return 0 if g == 18 else (g if g <= 2 else g - 10)
def cs(c): return " ".join(f"{SHN[i]}{c[i]}" for i in range(4) if c[i] > 0)


def chem(x, y, s, size=20, fill=INK, weight=400, anchor="start"):
    """化学式。_2 / _{2} は下付き、^+ / ^{2} は上付き（tspan の dy でずらす）"""
    sub = max(14, round(size * 0.7)); cur = 0.0; out = []
    for t in re.findall(r"_\{[^}]*\}|_\d+|\^\{[^}]*\}|\^[+\-−]|[^_^]+", s):
        if t[0] in "_^":
            body = (t[2:-1] if t[1] == "{" else t[1:]).replace("-", "−")
            tgt = size * 0.28 if t[0] == "_" else -size * 0.42
            out.append(f'<tspan dy="{tgt - cur:.1f}" font-size="{sub}">{esc(body)}</tspan>'); cur = tgt
        else:
            out.append(f'<tspan dy="{-cur:.1f}">{esc(t)}</tspan>' if cur else esc(t)); cur = 0.0
    w = ' font-weight="700"' if weight >= 700 else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}"{w}>{"".join(out)}</text>'


def bohr(cx, cy, c, radii, er, stable=False, val_col=VC, nuc=None, start=90, stagger=0):
    """ボーア模型（模式図）。c＝各殻の電子の数。stable＝最外殻が貴ガスと同じ（緑）"""
    out = []; o = outer(c)
    for i in range(4):
        if c[i] == 0: continue
        isO = i == o
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{radii[i]}" fill="none" stroke="{SC if (isO and stable) else "#a9b0b8"}" stroke-width="{2.2 if (isO and stable) else 1.3}"/>')
    out.append(nuc if nuc is not None else circle(cx, cy, max(4, radii[0] * 0.42), ACC, ACC, 0))
    for i in range(4):
        n = c[i]
        for j in range(n):
            a = math.radians(start + (stagger if i >= 2 else 0) - j * 360 / n)
            col = (SC if stable else val_col) if i == o else EC
            out.append(circle(cx + radii[i] * math.cos(a), cy - radii[i] * math.sin(a), er, col, INK, 0.8))
    return "".join(out)


def nucleus(cx, cy, z, a, rn=7):
    """陽子 z こと中性子 a−z こをひまわり状に並べる（シミュと同じ並べ方・並び順は模式的）"""
    tp = [1 if i < z else 0 for i in range(a)]
    sd = z * 131 + a * 7
    def r():
        nonlocal sd
        sd = (sd * 16807) % 2147483647; return sd / 2147483647
    for i in range(a - 1, 0, -1):
        j = int(r() * (i + 1)); tp[i], tp[j] = tp[j], tp[i]
    Rn = rn * math.sqrt(a / 0.82)
    pts = [(cx + Rn * math.sqrt((k + 0.5) / a) * 0.92 * math.cos(k * 2.39996), cy + Rn * math.sqrt((k + 0.5) / a) * 0.92 * math.sin(k * 2.39996), t) for k, t in enumerate(tp)]
    return "".join(circle(x, y, rn, ACC if t else "#c3c8cf", INK, 0.7) for x, y, t in reversed(pts))


def nuc_label(cx, cy, z, r=14):
    return circle(cx, cy, r, ACC, ACC, 0) + text(cx, cy + 5, f"{z}+", 14, "#fff", 700, "middle")


def prescript(x, y, a, z, sym, size=26):
    """左上に質量数、左下に原子番号をつけた元素記号（x＝元素記号の左端）"""
    return (text(x - 2, y - size * 0.62, str(a), 16, INK, 700, "end") + text(x - 2, y + 4, str(z), 16, INK, 700, "end")
            + text(x, y, sym, size, INK, 700))


def fig1():
    b = []
    # ---------- 左：ナトリウム原子のつくり ----------
    b.append(rect(48, 100, 520, 516, CARD, LINE, 12))
    b.append(text(68, 136, "ナトリウム原子のつくり", 19, INK, 700))
    b.append(prescript(316, 138, 23, 11, "Na"))
    b.append(text(360, 136, "質量数23・原子番号11", 15, INK2))
    lg = [(ACC, "陽子"), ("#c3c8cf", "中性子"), (EC, "電子"), (VC, "価電子")]
    x = 72
    for col, nm in lg:
        b.append(circle(x, 163, 7, col, INK, 0.8) + text(x + 12, 168, nm, 15, INK)); x += 26 + len(nm) * 15 + 18
    cx, cy = 252, 352; radii = [62, 104, 146]
    c = conf(11)
    b.append(bohr(cx, cy, c, radii + [190], 9.5, False, VC, nucleus(cx, cy, 11, 23), start=90))
    for i, (nm, ag) in enumerate([("K殻", -135), ("L殻", -112.5), ("M殻", -112.5)]):     # 電子と重ならない角度
        a = math.radians(ag); lx, ly = cx + radii[i] * math.cos(a), cy - radii[i] * math.sin(a)
        b.append(rect(lx - 21, ly - 12, 42, 22, CARD, CARD, 4, 0) + text(lx, ly + 5, nm, 15, INK2, 700, "middle"))
    vx, vy = cx + radii[2] * math.cos(math.radians(90)), cy - radii[2] * math.sin(math.radians(90))
    b.append(line(vx + 12, vy + 2, vx + 64, vy + 16, INK, 1.2) + text(vx + 68, vy + 22, "価電子（いちばん外側）", 15, "#7d5a18", 700))
    b.append(line(cx + 34, cy + 16, cx + 156, cy + 68, INK, 1.2) + text(cx + 160, cy + 84, "原子核", 15, ACC, 700))
    b.append(lines(68, 540, ["原子核：陽子 11個 ＋ 中性子 12個（23−11）",
                             "電子：11個（K殻2・L殻8・M殻1）＝陽子の数と同じ",
                             "価電子：1個（いちばん外側のM殻の電子）"], 16, INK, 1.6))
    # ---------- 右：イオンになるしくみ ----------
    X0 = 592
    b.append(rect(X0, 100, 560, 516, CARD, LINE, 12))
    b.append(text(X0 + 20, 136, "イオンになるしくみ（貴ガスと同じ電子配置に）", 19, INK, 700))
    mr = [16, 30, 44, 58]
    for k, (z, yc) in enumerate([(11, 228), (17, 386)]):
        lb, nm, d = ION[z]; ca = conf(z); ci = ca[:]; ci[outer(ca)] += d
        tgt = NOBLE[sum(ci)]
        ax, ix = 670, 866
        b.append(bohr(ax, yc, ca, mr, 4.8, False, VC, nuc_label(ax, yc, z)))
        b.append(bohr(ix, yc, ci, mr, 4.8, True, VC, nuc_label(ix, yc, z)))
        b.append(arrow(726, yc, 806, yc, "ink", 2.6))
        b.append(text(766, yc - 34, "電子を1個", 15, INK, 700, "middle"))
        b.append(text(766, yc - 16, "失う" if d < 0 else "受け取る", 15, INK, 700, "middle"))
        b.append(chem(ax, yc + 72, f"{SYM[z]}　{cs(ca)}", 16, INK, 700, "middle"))
        b.append(chem(ix, yc + 72, f"{lb}　{cs(ci)}", 16, INK, 700, "middle"))
        tx = 944
        b.append(chem(tx, yc - 22, lb, 26, ACC if d < 0 else TEAL_D, 700))
        b.append(text(tx + 52, yc - 22, nm, 15, INK2))
        eq = f"{SYM[z]} → {lb} ＋ e^-" if d < 0 else f"{SYM[z]} ＋ e^- → {lb}"
        b.append(chem(tx, yc + 8, eq, 18, INK, 700))
        b.append(text(tx, yc + 36, f"{tgt}（{NAME[sum(ci)]}）と", 15, INK))
        b.append(text(tx, yc + 58, "同じ電子配置", 15, SC, 700))
    b.append(rect(X0 + 18, 496, 524, 106, "#fbfaf6", LINE, 10))
    b.append(text(X0 + 34, 524, "原子番号 ＝ 陽子の数 ＝ 電子の数（原子のとき）", 16, INK, 700))
    b.append(text(X0 + 34, 553, "質量数 ＝ 陽子の数 ＋ 中性子の数", 16, INK, 700))
    b.append(chem(X0 + 34, 584, "電子殻の最大の電子の数 2n^{2}（K殻2・L殻8・M殻18・N殻32）", 16, INK, 700))
    return svg("".join(b), "原子のつくりとイオンのでき方（ボーア模型）",
               "模式図。実際の原子核は原子の約10万分の1の大きさで、電子は決まった円の上を回っているわけではない。")


def fig2():
    b = []
    LX, CW, TY, CH = 118, (1152 - 118) / 8, 130, 112
    cols = {1: 0, 2: 1, 13: 2, 14: 3, 15: 4, 16: 5, 17: 6, 18: 7}
    for g, j in cols.items():
        b.append(text(LX + j * CW + CW / 2, 122, f"{g}族", 15, INK2, 700, "middle"))
    for p in range(1, 5):
        y = TY + (p - 1) * CH
        b.append(text(78, y + 50, str(p), 26, INK, 700, "middle"))
        b.append(text(78, y + 76, f"（{SHN[p - 1]}殻）", 14, MUTED, anchor="middle"))
    b.append(text(78, 122, "周期", 15, INK2, 700, "middle"))
    for z in range(1, 21):
        j = cols[group(z)]; p = period(z); x, y = LX + j * CW, TY + (p - 1) * CH
        c = conf(z); v = valence(z)
        fill = "#fbeae6" if (group(z) == 1 and z > 1) else "#f6eedc" if group(z) == 2 else "#e6f0e8" if group(z) == 17 else "#ebe6f2" if v == 0 else CARD
        b.append(rect(x + 3, y + 3, CW - 6, CH - 6, fill, LINE, 8))
        b.append(text(x + 13, y + 26, str(z), 14, MUTED))
        b.append(text(x + 13, y + 54, SYM[z], 24, INK, 700))
        b.append(bohr(x + 85, y + 49, c, [12, 21, 30, 39], 3.3, v == 0, VC, circle(x + 85, y + 49, 5, ACC, ACC, 0), stagger=22.5))
        b.append(text(x + CW / 2, y + 102, cs(c), 14, INK, 700 if False else 400, "middle"))
    # あいている所：凡例と読み方
    gx0 = LX + CW + 16
    b.append(circle(gx0 + 6, 155, 5, EC, INK, 0.8) + text(gx0 + 16, 160, "電子", 15, INK))
    b.append(circle(gx0 + 70, 155, 5, VC, INK, 0.8) + text(gx0 + 80, 160, "価電子（いちばん外側の電子）", 15, INK))
    b.append(circle(gx0 + 316, 155, 5, SC, INK, 0.8) + text(gx0 + 326, 160, "貴ガスの安定な最外殻（価電子は0とする）", 15, INK))
    b.append(text(gx0, 186, "・同じ族（たての列）は価電子の数が同じ → 化学的な性質が似る", 15, INK2))
    b.append(text(gx0, 210, "・周期の番号 ＝ 電子が入っている最も外側の電子殻（1＝K殻、2＝L殻、3＝M殻、4＝N殻）", 15, INK2))
    lx = gx0
    for col, nm in [("#fbeae6", "アルカリ金属"), ("#f6eedc", "アルカリ土類金属"), ("#e6f0e8", "ハロゲン"), ("#ebe6f2", "貴ガス")]:
        b.append(rect(lx, 220, 16, 14, col, "#a9b0b8", 3, 1) + text(lx + 22, 232, nm, 14, INK2)); lx += 40 + len(nm) * 14
    b.append(text(LX + 2 * CW + 3 * CW, TY + 3 * CH + 52, "19番 K・20番 Ca は、M殻が8個のところで次の N殻に入る", 15, INK2, anchor="middle"))
    b.append(text(LX + 2 * CW + 3 * CW, TY + 3 * CH + 76, "（21番以降の遷移元素は「発展」）", 14, MUTED, anchor="middle"))
    # いちばん下：価電子の数
    b.append(text(112, 604, "価電子", 16, "#7d5a18", 700, "end"))
    for g, j in cols.items():
        b.append(text(LX + j * CW + CW / 2, 605, str(0 if g == 18 else (g if g <= 2 else g - 10)), 20, "#7d5a18", 700, "middle"))
    return svg("".join(b), "原子番号1〜20の電子配置（周期表の形）",
               "K殻に2個、L殻に8個、M殻に8個まで入ると次の殻へ。いちばん下の数＝価電子の数（族と対応する）。")


FIGS = [
    dict(svg=fig1, alt="ナトリウム原子（質量数23・原子番号11）のボーア模型。原子核（陽子11個・中性子12個）のまわりのK殻に2個、L殻に8個、M殻に1個（価電子）の電子が入っている。右は、ナトリウム原子が電子を1個失ってネオンと同じ電子配置のNa⁺に、塩素原子が電子を1個受け取ってアルゴンと同じ電子配置のCl⁻になるしくみと、原子番号・質量数・電子殻の最大数2n²の式。",
         caption="原子のつくりとイオンのでき方。イオンになるときは電子を失ったり受け取ったりして、近い貴ガスと同じ電子配置になる。"),
    dict(svg=fig2, alt="原子番号1〜20（水素〜カルシウム）の電子配置を周期表の形に並べた図。それぞれの元素のボーア模型で電子殻（K殻・L殻・M殻・N殻）の電子の数と価電子を示し、族ごとの価電子の数（1・2・3・4・5・6・7・0）をいちばん下にまとめている。",
         caption="原子番号1〜20の電子配置。同じ族は価電子の数が同じで、周期の番号は電子が入っている最も外側の電子殻の番号と同じ。"),
]
