"""理科の授業向けシミュの「授業で使える図」共通部品（2026-10-18）。
1枚＝1200×675（16:9）の SVG 文字列。サイトの配色（生成り・墨・藍・朱）と同じ。外部の画像・フォントは使わない。
使い方は scripts/rika/FIG_SPEC.md。"""
import html as _h
import math

W, H = 1200, 675
INK, INK2, MUTED, LINE, BG, CARD = "#14181d", "#3d434b", "#6b6f76", "#e2ded4", "#faf8f3", "#ffffff"
TEAL, TEAL_D, TEAL_L, ACC, ACC_L, GOLD, GOLD_L = "#2c6b86", "#1b4a63", "#eef3f6", "#c4442b", "#fbeae6", "#a97a24", "#f6eedc"
SKY, SUN, MOON_D, GREEN, PURPLE = "#7fb3d5", "#f4d35e", "#3b3f46", "#3f8a5a", "#6a5c82"
FONT = "'Hiragino Sans','Hiragino Kaku Gothic ProN','Noto Sans JP','Noto Sans CJK JP','Yu Gothic','Meiryo',sans-serif"
SERIF = "'Hiragino Mincho ProN','Noto Serif JP','Noto Serif CJK JP','Yu Mincho',serif"


def esc(s):
    return _h.escape(str(s), quote=False)


def svg(body, title, note="", defs=""):
    """枠：左上に見出し（明朝）と罫線、左下に一言（note）、右下にサイト名。本文は y=100〜620 に描く。"""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">'
            f'<defs>{ARROW_DEFS}{defs}</defs>'
            f'<rect width="{W}" height="{H}" fill="{BG}"/>'
            f'<text x="48" y="62" font-family="{SERIF}" font-size="32" font-weight="700" fill="{INK}">{esc(title)}</text>'
            f'<line x1="48" y1="82" x2="1152" y2="82" stroke="{INK}" stroke-width="1.5"/>'
            f'{body}'
            f'<text x="48" y="650" font-size="15" fill="{MUTED}">{esc(note)}</text>'
            f'<text x="1152" y="650" font-size="15" fill="{MUTED}" text-anchor="end">シミュラボ shimulabo.com</text>'
            f'</svg>')


ARROW_DEFS = "".join(
    f'<marker id="ah-{n}" markerWidth="10" markerHeight="10" refX="7" refY="5" orient="auto" markerUnits="userSpaceOnUse">'
    f'<path d="M0,0 L10,5 L0,10z" fill="{c}"/></marker>'
    for n, c in [("ink", INK), ("teal", TEAL), ("acc", ACC), ("gold", GOLD), ("muted", MUTED), ("green", GREEN)])


def text(x, y, s, size=17, fill=INK, weight=400, anchor="start", **kw):
    extra = "".join(f' {k.replace("_", "-")}="{v}"' for k, v in kw.items())
    w = ' font-weight="700"' if weight >= 700 else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}"{w}{extra}>{esc(s)}</text>'


def lines(x, y, rows, size=16, fill=INK, gap=1.55, **kw):
    """複数行のテキスト（rows は文字列のリスト）"""
    return "".join(text(x, y + i * size * gap, r, size, fill, **kw) for i, r in enumerate(rows))


def line(x1, y1, x2, y2, stroke=INK, width=2, dash=None, arrow=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    m = f' marker-end="url(#ah-{arrow})"' if arrow else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{width}"{d}{m}/>'


def arrow(x1, y1, x2, y2, color="ink", width=2.4):
    """矢印。color は ink / teal / acc / gold / muted / green"""
    c = {"ink": INK, "teal": TEAL, "acc": ACC, "gold": GOLD, "muted": MUTED, "green": GREEN}[color]
    return line(x1, y1, x2, y2, c, width, arrow=color)


def poly(pts, stroke=INK, width=2.4, fill="none", dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round"{d}/>'


def rect(x, y, w, h, fill=CARD, stroke=LINE, r=10, width=1.2):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'


def circle(cx, cy, r, fill=CARD, stroke=INK, width=1.6):
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'


def badge(x, y, s, fill=TEAL, color="#fff", size=15):
    """丸数字や番号の札"""
    return circle(x, y, size * 0.85, fill, fill, 0) + text(x, y + size * 0.36, s, size, color, 700, "middle")


def table(x, y, cols, rows, col_w, row_h=40, size=16, head_fill=TEAL_L, zebra=True):
    """早見表。cols＝見出しのリスト、rows＝行（文字列のリスト）のリスト、col_w＝列幅のリスト"""
    out, tw = [], sum(col_w)
    out.append(rect(x, y, tw, row_h * (len(rows) + 1), CARD, LINE, 8))
    out.append(f'<rect x="{x}" y="{y}" width="{tw}" height="{row_h}" rx="8" fill="{head_fill}"/>')
    cx = x
    for c, w in zip(cols, col_w):
        out.append(text(cx + w / 2, y + row_h * 0.64, c, size, INK, 700, "middle")); cx += w
    for i, r in enumerate(rows):
        yy = y + row_h * (i + 1)
        if zebra and i % 2 == 1:
            out.append(f'<rect x="{x + 1}" y="{yy}" width="{tw - 2}" height="{row_h}" fill="#f7f5ef"/>')
        out.append(line(x, yy, x + tw, yy, LINE, 1))
        cx = x
        for c, w in zip(r, col_w):
            out.append(text(cx + w / 2, yy + row_h * 0.64, c, size, INK, 400, "middle")); cx += w
    return "".join(out)


def axes(x0, y0, w, h, xlabel="", ylabel="", xticks=(), yticks=(), size=14):
    """グラフの軸。原点＝(x0, y0)（左下）。xticks/yticks は (位置px, ラベル) のリスト（原点からの距離）"""
    out = [arrow(x0, y0, x0 + w + 14, y0, "ink", 1.8), arrow(x0, y0, x0, y0 - h - 14, "ink", 1.8)]
    for px, lab in xticks:
        out.append(line(x0 + px, y0, x0 + px, y0 + 6, INK, 1.4)); out.append(text(x0 + px, y0 + 24, lab, size, INK2, anchor="middle"))
        out.append(line(x0 + px, y0, x0 + px, y0 - h, LINE, 1))
    for py, lab in yticks:
        out.append(line(x0 - 6, y0 - py, x0, y0 - py, INK, 1.4)); out.append(text(x0 - 10, y0 - py + 5, lab, size, INK2, anchor="end"))
        out.append(line(x0, y0 - py, x0 + w, y0 - py, LINE, 1))
    if xlabel: out.append(text(x0 + w + 18, y0 + 6, xlabel, size, INK))
    if ylabel: out.append(text(x0, y0 - h - 24, ylabel, size, INK, anchor="middle"))
    return "".join(out)


def moon_look(cx, cy, r, theta):
    """地球（北半球）から見た月の形。theta＝新月からの角度（0〜360、反時計回り）。満ちていく間は右側が光る。"""
    t = math.radians(theta)
    out = circle(cx, cy, r, MOON_D, MOON_D, 0)
    k = math.cos(t)
    if abs(theta % 360) < 1e-6:
        return out + f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{MUTED}" stroke-dasharray="3 3"/>'
    if abs(theta - 180) < 1e-6:
        return out + circle(cx, cy, r, SUN, SUN, 0)
    rx = abs(k) * r
    top, bot = f"{cx:.1f},{cy - r:.1f}", f"{cx:.1f},{cy + r:.1f}"
    if theta < 180:
        d = f"M{top} A{r},{r} 0 0 1 {bot} A{rx:.2f},{r} 0 0 {0 if k > 0 else 1} {top}Z"
    else:
        d = f"M{top} A{r},{r} 0 0 0 {bot} A{rx:.2f},{r} 0 0 {1 if k > 0 else 0} {top}Z"
    return out + f'<path d="{d}" fill="{SUN}"/>'
