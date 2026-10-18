"""ライフゲーム（life）の図。ルールはページの JS と同じ（まわり8マス・誕生＝ちょうど3・生存＝2か3・端は反対側とつながる）。"""
from figlib import *

ANCHOR = r"<h2>3つのルール</h2>\s*<ul>.*?</ul>\n"


def step(cells, rows, cols):
    """ページの JS の step() と同じ：まわり8マスを数え、(生 かつ 2か3) または (死 かつ 3) なら次も生。端は反対側とつながる。"""
    nxt = set()
    for i in range(rows):
        for j in range(cols):
            s = sum(((i + di) % rows, (j + dj) % cols) in cells for di in (-1, 0, 1) for dj in (-1, 0, 1) if di or dj)
            alive = (i, j) in cells
            if (alive and s in (2, 3)) or (not alive and s == 3):
                nxt.add((i, j))
    return nxt


def grid(x, y, cs, n_rows, n_cols, live, ghost=(), stroke=LINE):
    out = [rect(x, y, cs * n_cols, cs * n_rows, CARD, stroke, 2, 1.2)]
    for (r, c) in ghost:
        out.append(f'<rect x="{x + c * cs + 3:.1f}" y="{y + r * cs + 3:.1f}" width="{cs - 6}" height="{cs - 6}" fill="none" '
                   f'stroke="{MUTED}" stroke-width="1.6" stroke-dasharray="3 3"/>')
    for (r, c) in live:
        out.append(f'<rect x="{x + c * cs + 1.5:.1f}" y="{y + r * cs + 1.5:.1f}" width="{cs - 3}" height="{cs - 3}" rx="2" fill="{TEAL}"/>')
    for k in range(1, n_cols):
        out.append(line(x + k * cs, y, x + k * cs, y + n_rows * cs, LINE, 1))
    for k in range(1, n_rows):
        out.append(line(x, y + k * cs, x + n_cols * cs, y + k * cs, LINE, 1))
    return "".join(out)


RULES = [  # 名前, 真ん中が生きているか, まわりの生きているマス, 説明2行, 結果(生/死), 結果の言葉
    ("誕生", False, [(0, 0), (0, 2), (2, 1)], ["死んでいるマスのまわりに", "生きているマスが ちょうど3つ"], True, "生まれる"),
    ("生存", True, [(0, 1), (2, 2)], ["生きているマスのまわりに", "生きているマスが 2つか3つ"], True, "生き残る"),
    ("過疎", True, [(1, 0)], ["生きているマスのまわりが", "0か1つ（さみしすぎる）"], False, "死ぬ"),
    ("過密", True, [(0, 0), (0, 1), (1, 2), (2, 0)], ["生きているマスのまわりが", "4つ以上（混みすぎ）"], False, "死ぬ"),
]


def fig1():
    b = []
    pw, gap = 264, 16
    for k, (nm, center, nb, desc, res, word) in enumerate(RULES):
        # 例の配置が本当にそのルールになるか、JS と同じ step() で確かめる
        cells = set((r + 1, c + 1) for r, c in nb) | ({(2, 2)} if center else set())
        assert ((2, 2) in step(cells, 5, 5)) == res, nm
        px = 48 + k * (pw + gap); cxp = px + pw / 2
        b.append(rect(px, 104, pw, 486, CARD, LINE, 12))
        b.append(badge(px + 34, 142, str(k + 1), TEAL if res else ACC, "#fff", 17))
        b.append(text(px + 60, 152, nm, 26, INK, 700))
        b.append(lines(px + 22, 194, desc, 16, INK2, 1.5))
        cs = 50; gx, gy = cxp - 1.5 * cs, 246
        b.append(grid(gx, gy, cs, 3, 3, set(nb) | ({(1, 1)} if center else set())))
        for n, (r, c) in enumerate(nb, 1):
            b.append(text(gx + c * cs + cs / 2, gy + r * cs + cs / 2 + 7, str(n), 19, "#fff", 700, "middle"))
        b.append(f'<rect x="{gx + cs + 1:.1f}" y="{gy + cs + 1:.1f}" width="{cs - 2}" height="{cs - 2}" fill="none" stroke="{ACC}" stroke-width="3.5"/>')
        b.append(text(cxp, gy + 3 * cs + 26, f"まわりの生きているマス：{len(nb)}つ", 15, INK2, anchor="middle"))
        b.append(arrow(cxp, gy + 3 * cs + 40, cxp, gy + 3 * cs + 74, "ink", 2.4))
        b.append(text(cxp + 12, gy + 3 * cs + 62, "次の世代", 14, MUTED))
        ry = gy + 3 * cs + 84; rx = cxp - 92
        if res:
            b.append(f'<rect x="{rx}" y="{ry}" width="{cs}" height="{cs}" rx="3" fill="{TEAL}" stroke="{ACC}" stroke-width="3.5"/>')
        else:
            b.append(f'<rect x="{rx}" y="{ry}" width="{cs}" height="{cs}" rx="3" fill="{CARD}" stroke="{ACC}" stroke-width="3.5"/>'
                     + line(rx + 12, ry + 12, rx + cs - 12, ry + cs - 12, MUTED, 2.4) + line(rx + cs - 12, ry + 12, rx + 12, ry + cs - 12, MUTED, 2.4))
        b.append(text(rx + cs + 18, ry + cs / 2 + 9, word, 24, TEAL_D if res else ACC, 700))
    b.append(f'<rect x="48" y="603" width="18" height="18" rx="2" fill="{TEAL}"/>' + text(74, 618, "生きているマス", 15, INK2))
    b.append(f'<rect x="210" y="603" width="18" height="18" rx="2" fill="{CARD}" stroke="{LINE}" stroke-width="1.5"/>' + text(236, 618, "死んでいるマス", 15, INK2))
    b.append(f'<rect x="372" y="603" width="18" height="18" fill="none" stroke="{ACC}" stroke-width="3"/>' + text(398, 618, "注目するマス（数字は数えた順）", 15, INK2))
    b.append(text(1152, 618, "まわり＝となりの8マス（たて・よこ・ななめ）", 15, INK2, anchor="end"))
    return svg("".join(b), "ライフゲームのルール（誕生・生存・過疎・過密）",
               "全部のマスを同時に次の世代へ進める。このシミュでは、画面の端は反対側の端とつながっている。")


def frames(start, n, off=3, size=14):
    """表示用の座標で置いた形を、端の影響が出ない広さ（14×14）で n 世代すすめる"""
    cur = {(r + off, c + off) for r, c in start}; out = [set(start)]
    for _ in range(n):
        cur = step(cur, size, size)
        out.append({(r - off, c - off) for r, c in cur})
    return out


def fig2():
    b = []
    block = frames({(1, 1), (1, 2), (2, 1), (2, 2)}, 1)
    blink = frames({(2, 1), (2, 2), (2, 3)}, 2)
    glider = frames({(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)}, 4)
    assert block[1] == block[0] and blink[2] == blink[0] and blink[1] != blink[0]
    assert glider[4] == {(r + 1, c + 1) for r, c in glider[0]}          # 4世代で右下へ1マス
    cs = 19
    rows = [("ブロック", ["2×2の正方形", "ずっと変わらない（固定物）"], block, 4),
            ("ブリンカー", ["横3つ ⇄ たて3つ", "2世代でもとにもどる（振動子）"], blink, 5),
            ("グライダー", ["5マスのかたまり", "4世代でななめに1マス進む（移動体）", "点線の□＝第0世代の位置"], glider, 6)]
    y, h = 104, 172
    for nm, desc, fr, n in rows:
        b.append(rect(48, y, 1104, h - 8, CARD, LINE, 12))
        b.append(text(72, y + 46, nm, 24, INK, 700))
        b.append(lines(72, y + 82, desc, 16, INK2, 1.55))
        gx = 360; gy = y + (h - 8 - n * cs) / 2 + 10
        for g, cells in enumerate(fr):
            ghost = glider[0] if (nm == "グライダー" and g == 4) else ()
            b.append(text(gx + n * cs / 2, gy - 10, f"第{g}世代", 15, INK2, anchor="middle"))
            assert all(0 <= r < n and 0 <= c < n for r, c in cells)
            b.append(grid(gx, gy, cs, n, n, cells, ghost))
            if g < len(fr) - 1:
                b.append(arrow(gx + n * cs + 10, gy + n * cs / 2, gx + n * cs + 34, gy + n * cs / 2, "muted", 2))
            gx += n * cs + 46
        if nm == "ブロック":
            b.append(text(gx - 6, gy + n * cs / 2 + 6, "→ 何世代たっても同じ形", 17, TEAL_D, 700))
        if nm == "ブリンカー":
            b.append(text(gx - 6, gy + n * cs / 2 + 6, "→ 第0世代と第2世代が同じ", 17, TEAL_D, 700))
        assert gx - 46 <= 1130, gx
        y += h
    return svg("".join(b), "ライフゲームの有名なパターン（世代ごとの変化）",
               "どのパターンも図1の4つのルールだけで動く。「クリア」してから同じ形をクリックで置くと、シミュでも同じ動きになる。")


FIGS = [
    dict(svg=fig1, alt="ライフゲームの4つのルールの図。死んでいるマスのまわり8マスに生きているマスがちょうど3つなら誕生、生きているマスのまわりが2つか3つなら生存、0か1つなら過疎で死、4つ以上なら過密で死になることを3×3のマスで示している。",
         caption="ライフゲームのルール。まわり8マスの「生きているマスの数」だけで、次の世代の生死が決まる。"),
    dict(svg=fig2, alt="ライフゲームの有名なパターンの世代ごとの変化。ブロック（2×2で変わらない固定物）、ブリンカー（横3つとたて3つを2世代でくり返す振動子）、グライダー（4世代でななめに1マス進む移動体）を第0世代から順に並べた図。",
         caption="有名なパターンの動き。固定物・振動子・移動体が、同じルールから生まれる。"),
]
