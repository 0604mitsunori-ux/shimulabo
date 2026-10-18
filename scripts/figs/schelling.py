"""街の分断（schelling）の図。ルールはページの JS と同じ：40×40マス・青45%／オレンジ45%／空き地10%、
まわり8マスの「住人」のうち同じ仲間の割合が満足ライン以上なら満足（空き地は数えない・まわりに住人がいなければ満足・端はつながらない）、
不満な人は空き地のどこかへ引っ越す（1回のくり返しで左上から順に全員を見る）。"""
import random
from figlib import *

N = 40
ORANGE = GOLD
SEED = 1


def person(x, y, t, r=17):
    """t=1 青（丸）／t=2 オレンジ（四角）"""
    if t == 1:
        return circle(x, y, r, TEAL, TEAL, 0)
    return f'<rect x="{x - r * 0.9:.1f}" y="{y - r * 0.9:.1f}" width="{r * 1.8:.1f}" height="{r * 1.8:.1f}" rx="3" fill="{ORANGE}"/>'


class Town:
    def __init__(self, seed=SEED):
        self.rnd = random.Random(seed)
        self.g = [[0] * N for _ in range(N)]
        for i in range(N):
            for j in range(N):
                r = self.rnd.random(); self.g[i][j] = 1 if r < 0.45 else (2 if r < 0.9 else 0)

    def counts(self, i, j):
        t = self.g[i][j]; same = tot = 0
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                if di or dj:
                    a, b = i + di, j + dj
                    if 0 <= a < N and 0 <= b < N and self.g[a][b]:
                        tot += 1; same += self.g[a][b] == t
        return same, tot

    def happy(self, i, j, tol):
        if not self.g[i][j]: return True
        same, tot = self.counts(i, j)
        return True if tot == 0 else same / tot >= tol

    def step(self, tol):
        g = self.g
        empt = [(i, j) for i in range(N) for j in range(N) if not g[i][j]]
        moved = 0
        for i in range(N):
            for j in range(N):
                if g[i][j] and not self.happy(i, j, tol) and empt:
                    k = int(self.rnd.random() * len(empt)); a, b = empt[k]
                    g[a][b] = g[i][j]; g[i][j] = 0; empt[k] = (i, j); moved += 1
        return moved

    def same_share(self):
        s = n = 0
        for i in range(N):
            for j in range(N):
                if self.g[i][j]:
                    same, tot = self.counts(i, j)
                    if tot: s += same / tot; n += 1
        return s / n


def run(tol, max_steps=2000):
    t = Town()
    for st in range(1, max_steps + 1):
        if t.step(tol) == 0:
            return t, st - 1          # 引っ越しが起きた最後のくり返し
    return t, None


def town_svg(x, y, g, cs):
    """仲間ごとに、横につながった帯を1本の path で描く（ファイルを小さくするため）"""
    d = {1: [], 2: []}
    for i in range(N):
        j = 0
        while j < N:
            t = g[i][j]; k = j
            while k < N and g[i][k] == t: k += 1
            if t:
                w = (k - j) * cs
                d[t].append(f"M{x + j * cs:.1f} {y + i * cs:.1f}h{w:.1f}v{cs}h-{w:.1f}z")
            j = k
    return (rect(x - 1, y - 1, N * cs + 2, N * cs + 2, CARD, INK2, 2, 1)
            + "".join(f'<path d="{"".join(d[t])}" fill="{TEAL if t == 1 else ORANGE}" shape-rendering="crispEdges"/>' for t in (1, 2)))


EX = [  # まわり8マス（左上から右回り、真ん中は除く）。1=青 2=オレンジ 0=空き地
    ("満足", [1, 2, 2, 0, 1, 2, 1, 2]),
    ("不満", [2, 2, 1, 0, 2, 1, 2, 2]),
]
POS = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0)]


def fig1():
    b = []
    tol = 0.35
    for k, (nm, nb) in enumerate(EX):
        same = nb.count(1); tot = sum(1 for v in nb if v)
        ok = same / tot >= tol
        assert ok == (nm == "満足")
        y0 = 104 + k * 258
        b.append(rect(48, y0, 640, 246, CARD, LINE, 12))
        cs = 58; gx, gy = 76, y0 + 36
        for (r, c), v in zip(POS, nb):
            b.append(rect(gx + c * cs, gy + r * cs, cs, cs, CARD, LINE, 0, 1))
            if v: b.append(person(gx + c * cs + cs / 2, gy + r * cs + cs / 2, v))
        b.append(rect(gx + cs, gy + cs, cs, cs, ACC_L, ACC, 0, 3) + person(gx + cs * 1.5, gy + cs * 1.5, 1))
        b.append(text(gx + cs * 1.5, gy + 3 * cs + 24, "真ん中の人（青）", 14, INK2, anchor="middle"))
        tx = 300
        b.append(text(tx, y0 + 50, f"例{k + 1}", 18, MUTED, 700))
        b.append(text(tx, y0 + 88, f"同じ仲間 {same}人 ÷ まわりの住人 {tot}人", 18, INK))
        b.append(text(tx, y0 + 124, f"＝ {same / tot * 100:.0f}%", 26, INK, 700))
        b.append(text(tx + 120, y0 + 124, f"{'≧' if ok else '＜'} 満足ライン {tol * 100:.0f}%", 20, INK2, 700))
        if ok:
            b.append(rect(tx, y0 + 150, 350, 58, TEAL_L, TEAL, 10, 1.6) + text(tx + 175, y0 + 186, "満足 → そのまま住む", 20, TEAL_D, 700, "middle"))
        else:
            b.append(rect(tx, y0 + 150, 350, 58, ACC_L, ACC, 10, 1.6) + text(tx + 175, y0 + 186, "不満 → 空き地へ引っ越す", 20, ACC, 700, "middle"))
    # 右：連鎖
    x0 = 712
    b.append(text(x0, 128, "引っ越しが連鎖するしくみ", 19, INK, 700))
    steps = [["不満な人が、空き地のどこかへ", "引っ越す（行き先はランダム）"],
             ["元の場所と引っ越し先のまわりで、", "近所の割合が変わる"],
             ["そのせいで、別の人が", "新しく不満になる"],
             ["くり返すうちに、同じ仲間", "どうしで固まって落ち着く"]]
    for i, rows in enumerate(steps):
        y = 150 + i * 112
        b.append(rect(x0, y, 440, 84, CARD, LINE, 10) + badge(x0 + 30, y + 42, str(i + 1), TEAL if i < 3 else ACC, "#fff", 16))
        b.append(lines(x0 + 58, y + 36, rows, 16.5, INK, 1.5))
        if i < 3: b.append(arrow(x0 + 220, y + 86, x0 + 220, y + 108, "ink", 2.2))
    b.append(person(712 + 12, 617 - 6, 1, 8) + text(712 + 28, 617, "青", 15, INK2)
             + person(712 + 72, 617 - 6, 2, 8) + text(712 + 88, 617, "オレンジ", 15, INK2)
             + f'<rect x="{712 + 168}" y="{617 - 14}" width="16" height="16" fill="{CARD}" stroke="{LINE}"/>' + text(712 + 192, 617, "空き地（数えない）", 15, INK2))
    return svg("".join(b), "街の分断（シェリングの分居モデル）のしくみ",
               "満足ライン＝シミュの「満足する同類の割合」（初期値35%）。まわりに住人がいなければ満足。")


_CACHE = {}


def results():
    if "r" not in _CACHE:
        t0 = Town(); base = t0.same_share()
        out = []
        for tol in (0.20, 0.35, 0.50, 0.70):
            t, n = run(tol); out.append((tol, t.g, t.same_share(), n))
        _CACHE["r"] = (t0.g, base, out)
    return _CACHE["r"]


def fig2():
    g0, base, res = results()
    b = [text(48, 124, "同じスタート（40×40マス・青45%・オレンジ45%・空き地10%）から、満足ラインだけを変えて引っ越しが止まるまで動かした結果", 16, INK2)]
    cs, gap = 4.8, 36
    cols = [("はじめ（ランダム）", g0, base, None, None)] + [(f"満足ライン {int(t * 100)}%", g, s, n, t) for t, g, s, n in res]
    for k, (lab, g, s, n, tol) in enumerate(cols):
        x = 48 + k * (N * cs + gap); y = 176
        b.append(text(x + N * cs / 2, y - 14, lab, 17, INK if k else MUTED, 700, "middle"))
        b.append(town_svg(x, y, g, cs))
        b.append(text(x + N * cs / 2, y + N * cs + 34, f"同じ仲間 {s * 100:.0f}%", 21, INK if k == 0 else ACC, 700, "middle"))
        b.append(text(x + N * cs / 2, y + N * cs + 60, "近所の平均" if k == 0 else f"くり返し{n}回で落ち着く", 14.5, INK2, anchor="middle"))
        if k == 0:
            b.append(arrow(x + N * cs + 6, y + N * cs / 2, x + N * cs + gap - 6, y + N * cs / 2, "muted", 2))
    # 下：好み（満足ライン）と結果（同じ仲間の割合）の比べ
    y0 = 462
    b.append(text(48, y0, "好みは弱くても、結果は強く分かれる", 18, INK, 700))
    bx, bw = 290, 820
    for i, (tol, g, s, n) in enumerate(res):
        y = y0 + 20 + i * 33
        b.append(text(bx - 14, y + 20, f"満足ライン {int(tol * 100)}%", 15, INK2, anchor="end"))
        b.append(f'<rect x="{bx}" y="{y + 4}" width="{bw * tol:.1f}" height="11" fill="{LINE}" stroke="{MUTED}" stroke-width=".8"/>')
        b.append(text(bx + bw * tol + 8, y + 14, f"{int(tol * 100)}%", 14, MUTED))
        b.append(f'<rect x="{bx}" y="{y + 15}" width="{bw * s:.1f}" height="14" fill="{ACC}"/>')
        b.append(text(bx + bw * s + 8, y + 28, f"{s * 100:.0f}%", 15, ACC, 700))
    b.append(f'<rect x="{bx + 560}" y="{y0 - 14}" width="22" height="11" fill="{LINE}" stroke="{MUTED}" stroke-width=".8"/>' + text(bx + 588, y0 - 4, "好み（満足ライン）", 14, INK2)
             + f'<rect x="{bx + 720}" y="{y0 - 16}" width="22" height="14" fill="{ACC}"/>' + text(bx + 748, y0 - 4, "結果（同じ仲間）", 14, INK2))
    return svg("".join(b), "満足ラインと街の分かれ方（シミュの一例）",
               "「同じ仲間」＝住人ごとの、まわりの住人のうち同じ仲間の割合の平均。乱数を使うので、毎回少しずつちがう。")


FIGS = [
    dict(svg=fig1, alt="シェリングの分居モデルのしくみの図。真ん中の住人のまわり8マスで、同じ仲間の割合が満足ライン35%以上なら満足（例：3人÷7人＝43%）、未満なら不満で空き地へ引っ越す（例：2人÷7人＝29%）ことと、引っ越しが別の人の不満を生んで連鎖することを示している。",
         caption="街の分断のしくみ。近所の同じ仲間の割合が満足ラインに届かない人だけが引っ越し、それが連鎖する。"),
    dict(svg=fig2, alt="シェリングの分居モデルを同じスタートから満足ライン20%・35%・50%・70%で動かした結果の比較。はじめは近所の同じ仲間の割合が約50%だが、満足ライン35%でも約8割、70%ではほぼ全員が同じ仲間に囲まれるほど街が分かれる。",
         caption="満足ラインと分かれ方の比較（シミュと同じ計算の一例）。「3割ほどでいい」という弱い好みでも、街ははっきり分かれる。"),
]
