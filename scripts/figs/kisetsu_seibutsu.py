"""季節と生き物（kisetsu-seibutsu・小4）の授業用の図。気温（気象庁 東京の平年値）と生き物のようすは scripts/rika/sims_sho34_seibutsu.py（ページのJS）と同じデータ。"""
from figlib import *

MN = ["4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月", "1月", "2月", "3月"]
TEMP = [14.3, 18.8, 21.9, 25.7, 26.9, 23.3, 18.0, 12.5, 7.7, 5.4, 6.1, 9.4]   # 気象庁 東京 平年値（1991〜2020年）4月〜3月
SEAS = ["春", "春", "夏", "夏", "夏", "秋", "秋", "秋", "冬", "冬", "冬", "春"]
# 生き物ごとの月のようす（活動のさかんさ0〜3, 短い説明）。シミュの ORG と同じ（月は4月=0 … 3月=11）
def _M(lst):
    o = [None] * 12
    for (a, b), lv, sh, stt in lst:
        for i in range(a, b + 1): o[i] = (lv, sh, stt)
    assert all(o), lst
    return o
ORG = [
 ("ツバメ", "a", _M([((0, 0), 2, "巣をつくる", "nest"), ((1, 1), 3, "ひなを育てる", "hina"), ((2, 2), 3, "ひなが巣立つ", "hina"),
                    ((3, 3), 3, "さかんにとぶ", "fly"), ((4, 4), 2, "群れで集まる", "flock"), ((5, 5), 1, "南へわたる", "leave"),
                    ((6, 10), 0, "いない", "gone"), ((11, 11), 1, "やってくる", "fly")])),
 ("カエル", "a", _M([((0, 0), 1, "冬眠から目覚める", "wake"), ((1, 1), 3, "鳴いてたまごを産む", "eggs"), ((2, 2), 3, "おたまじゃくし", "tad"),
                    ((3, 3), 3, "子ガエルになる", "young"), ((4, 4), 3, "さかんに活動", "active"), ((5, 5), 2, "活動", "active"),
                    ((6, 6), 1, "動きがにぶい", "slow"), ((7, 7), 0, "冬眠を始める", "sleep"), ((8, 10), 0, "冬眠", "sleep"), ((11, 11), 0, "冬眠", "sleep")])),
 ("テントウムシ", "a", _M([((0, 0), 3, "たまごを産む", "eggs"), ((1, 1), 3, "よう虫・さなぎ", "larva"), ((2, 2), 2, "新しい成虫", "adult"),
                    ((3, 4), 2, "活動", "adult"), ((5, 6), 2, "活動", "adult"), ((7, 7), 1, "冬ごしの場所へ", "group"),
                    ((8, 10), 0, "成虫で冬ごし", "group"), ((11, 11), 1, "出てくる", "adult")])),
 ("カマキリ", "a", _M([((0, 0), 0, "たまごのまま", "ootheca"), ((1, 1), 1, "よう虫が出てくる", "hatch"), ((2, 2), 2, "小さなよう虫", "nymph"),
                    ((3, 3), 3, "よう虫が育つ", "nymph"), ((4, 4), 3, "成虫になる", "adult"), ((5, 5), 3, "成虫", "adult"),
                    ((6, 6), 2, "たまごを産む", "lay"), ((7, 7), 0, "たまごで冬ごし", "ootheca"), ((8, 11), 0, "たまごで冬ごし", "ootheca")])),
 ("モンシロチョウ", "a", _M([((0, 0), 3, "成虫がとぶ", "adult"), ((1, 1), 3, "たまご・よう虫", "larva"), ((2, 2), 3, "さかんにとぶ", "adult"),
                    ((3, 4), 2, "活動", "adult"), ((5, 5), 3, "さかんにとぶ", "adult"), ((6, 6), 2, "活動", "larva"),
                    ((7, 7), 1, "さなぎになる", "pupa"), ((8, 10), 0, "さなぎで冬ごし", "pupa"), ((11, 11), 1, "成虫が出てくる", "adult")])),
 ("サクラ", "p", _M([((0, 0), 2, "花がちり葉が出る", "hazakura"), ((1, 3), 3, "葉がしげる", "leaf"), ((4, 4), 2, "葉がしげる", "leaf"),
                    ((5, 5), 1, "葉の色が変わり始める", "leafy"), ((6, 6), 1, "葉が赤や黄色に", "koyo"), ((7, 7), 0, "葉が落ちる", "fall"),
                    ((8, 10), 0, "芽で冬ごし", "bare"), ((11, 11), 2, "花がさく", "flower")])),
 ("ヘチマ", "p", _M([((0, 0), 1, "たねをまく", "seed"), ((1, 1), 2, "芽が出る", "sprout"), ((2, 2), 3, "くきがのびる", "vine1"),
                    ((3, 3), 3, "ぐんぐんのびる・花", "flower"), ((4, 4), 3, "実が大きくなる", "fruit"), ((5, 5), 2, "のびがゆっくり", "fruit"),
                    ((6, 6), 1, "かれ始める", "wither"), ((7, 7), 0, "かれる", "dead"), ((8, 10), 0, "たねで冬ごし", "seedwinter"),
                    ((11, 11), 0, "たねで冬ごし", "seedwinter")])),
 ("タンポポ", "p", _M([((0, 0), 3, "花がさく", "flower"), ((1, 1), 3, "わた毛がとぶ", "fluff"), ((2, 2), 3, "葉がしげる", "leaf"),
                    ((3, 4), 2, "葉がしげる", "leaf"), ((5, 5), 2, "また花がさく", "flower"), ((6, 6), 1, "葉が地面に広がる", "rosette"),
                    ((7, 10), 0, "ロゼットで冬ごし", "rosette"), ((11, 11), 2, "花がさき始める", "flower")])),
]
ANI = [o for o in ORG if o[1] == "a"]; PLA = [o for o in ORG if o[1] == "p"]
ACTIVE = [sum(1 for o in ANI if o[2][i][0] >= 1) for i in range(12)]          # 活動している（見られる）動物の数
PGROW = [sum(o[2][i][0] for o in PLA) / len(PLA) for i in range(12)]
def pword(v): return "よく育つ" if v >= 2.3 else ("育つ" if v >= 1.5 else ("ゆっくり" if v >= 0.7 else "ほとんど育たない"))
SCOL = {"春": "#f6dfe6", "夏": "#fbe3d6", "秋": "#f3e7cc", "冬": "#dde9f3"}
STXT = {"春": "#a8456a", "夏": ACC, "秋": GOLD, "冬": TEAL_D}


def _hx(c): return [int(c[i:i + 2], 16) for i in (1, 3, 5)]
def mix(a, b, t):
    t = max(0.0, min(1.0, t)); A, B = _hx(a), _hx(b)
    return "#" + "".join("%02x" % round(A[i] + (B[i] - A[i]) * t) for i in range(3))
def tcol(t):
    return mix("#bcd6ee", "#8fbbe0", t / 10) if t < 10 else (mix("#c9e3b0", "#f1d27a", (t - 10) / 10) if t < 20 else mix("#f4b27e", "#e06a4f", (t - 20) / 8))


def fig1():
    b = []
    x0, bw, y0, k = 132, 82, 392, 8.0            # 1℃ = 8px
    xe = x0 + 12 * bw
    b.append(text(48, 117, "棒＝月の平均気温（℃）：東京の平年値（気象庁・1991〜2020年）", 16, INK, 700))
    b.append(text(700, 117, "色：", 15, INK2) + "".join(f'<rect x="{732 + q * 22}" y="104" width="18" height="14" rx="3" fill="{tcol(t)}"/>' for q, t in enumerate((5, 12, 18, 23, 27)))
             + text(732 + 5 * 22 + 4, 117, "寒い → あたたかい", 15, INK2))
    for v in (0, 10, 20, 30):
        y = y0 - v * k
        b.append(line(x0, y, xe, y, INK if v == 0 else LINE, 1.6 if v == 0 else 1) + text(x0 - 10, y + 5, f"{v}℃", 14, INK2, anchor="end"))
    for i, t in enumerate(TEMP):
        x = x0 + i * bw; h = t * k
        b.append(rect(x + 12, y0 - h, bw - 24, h, tcol(t), tcol(t), 4, 0))
        b.append(text(x + bw / 2, y0 - h - 8, f"{t:.1f}", 15, INK, 700, "middle"))
    # 月と季節
    for i, m in enumerate(MN):
        x = x0 + i * bw
        b.append(text(x + bw / 2, y0 + 22, m, 16, INK, 700, "middle"))
    sy = y0 + 32
    i = 0
    while i < 12:
        j = i
        while j + 1 < 12 and SEAS[j + 1] == SEAS[i]: j += 1
        s = SEAS[i]
        b.append(rect(x0 + i * bw + 2, sy, (j - i + 1) * bw - 4, 24, SCOL[s], SCOL[s], 6, 0) + text(x0 + (i + j + 1) * bw / 2, sy + 18, s, 15, STXT[s], 700, "middle"))
        i = j + 1
    # 動物：活動している数（5種類中）
    ay = sy + 38
    b.append(text(48, ay + 30, "動物", 17, ACC, 700) + text(48, ay + 50, "（5種類中）", 13.5, MUTED))
    for i, n in enumerate(ACTIVE):
        cx = x0 + i * bw + bw / 2
        b.append(rect(x0 + i * bw + 3, ay, bw - 6, 58, "#fdf1ec" if n else "#f1f0ec", LINE, 6, 1))
        for q in range(5):
            b.append(circle(cx - 24 + q * 12, ay + 16, 4.6, ACC if q < n else CARD, ACC if q < n else "#c9c4b8", 1.2))
        b.append(text(cx, ay + 46, f"{n}種類", 15, ACC if n else MUTED, 700, "middle"))
    # 植物：育ち方
    py = ay + 66
    b.append(text(48, py + 30, "植物", 17, GREEN, 700) + text(48, py + 50, "（3種類）", 13.5, MUTED))
    for i, v in enumerate(PGROW):
        x = x0 + i * bw; w = pword(v)
        b.append(rect(x + 3, py, bw - 6, 58, mix("#f3f2ee", "#bfe0c8", v / 3), LINE, 6, 1))
        if len(w) > 5:
            b.append(text(x + bw / 2, py + 25, w[:4], 14.5, INK2, 700, "middle") + text(x + bw / 2, py + 45, w[4:], 14.5, INK2, 700, "middle"))
        else:
            b.append(text(x + bw / 2, py + 35, w, 14.5, GREEN if v >= 1.5 else INK2, 700, "middle"))
    b.append(text(48, py + 88, "あたたかい月ほど、活動する動物が多く、植物がよく育つ。寒い12〜2月は、5種類とも活動していない（ツバメは南の国へ、ほかは冬ごし）。", 16, INK))
    return svg("".join(b), "季節と気温と生き物のようす（1年）",
               "動物＝ツバメ・カエル・テントウムシ・カマキリ・モンシロチョウ、植物＝サクラ・ヘチマ・タンポポ。関東の平地の目安。")


def fig2():
    b = []
    cols = [0, 3, 6, 9]
    X = [48, 92, 236]; CW = 229
    y, hh, rh = 104, 58, 50
    tw = X[2] - 48 + CW * 4
    b.append(rect(48, y, tw, hh + rh * 8, CARD, LINE, 10))
    b.append(text((X[1] + X[2]) / 2, y + 36, "生き物", 17, INK, 700, "middle"))
    for c, m in enumerate(cols):
        x = X[2] + c * CW; s = SEAS[m]
        b.append(rect(x + 3, y + 3, CW - 6, hh - 6, SCOL[s], SCOL[s], 8, 0))
        b.append(text(x + CW / 2, y + 27, f"{MN[m]}（{s}）", 18, STXT[s], 700, "middle"))
        b.append(text(x + CW / 2, y + 48, f"平均気温 {TEMP[m]:.1f}℃" + ("・冬ごし" if s == "冬" else ""), 14.5, INK2, anchor="middle"))
    for r, (nm, kind, M) in enumerate(ORG):
        yy = y + hh + r * rh
        b.append(line(X[1], yy, 48 + tw, yy, LINE, 1))
        if r == 5: b.append(line(48, yy, 48 + tw, yy, INK2, 2))
        b.append(text(X[1] + 14, yy + 32, nm, 17, INK, 700))
        for c, m in enumerate(cols):
            x = X[2] + c * CW; lv, sh, stt = M[m]
            if nm == "ツバメ" and stt == "gone": sh = "いない（南の国）"
            if SEAS[m] == "冬": b.append(f'<rect x="{x + 1}" y="{yy + 1}" width="{CW - 2}" height="{rh - 2}" fill="#f2f6f9"/>')
            b.append(text(x + 14, yy + 32, sh, 16, INK if lv else INK2))
            dc = ACC if kind == "a" else GREEN
            for q in range(3):
                b.append(circle(x + CW - 44 + q * 13, yy + 26, 4.6, dc if q < lv else CARD, dc if q < lv else "#c9c4b8", 1.2))
    for r0, r1, t, col in [(0, 5, "動物", ACC), (5, 8, "植物", GREEN)]:
        ya, yb = y + hh + r0 * rh, y + hh + r1 * rh
        b.append(rect(52, ya + 4, 34, yb - ya - 8, ACC_L if t == "動物" else "#e4f1e8", "none", 6, 0))
        b.append(text(69, (ya + yb) / 2 - 4, t[0], 17, col, 700, "middle") + text(69, (ya + yb) / 2 + 18, t[1], 17, col, 700, "middle"))
    b.append(text(48, 608, "●の数＝活動のさかんさ（植物は育ち方）の目安。ヘチマはツルレイシ（ゴーヤ）でも同じ。", 15.5, INK2))
    return svg("".join(b), "季節ごとの生き物のようすと冬ごし（早見表）",
               "関東の平地の目安（地域や年でちがう）。カエル＝アマガエル、カマキリ＝オオカマキリ、サクラ＝ソメイヨシノの例。")


FIGS = [
    dict(svg=fig1, alt="東京の月ごとの平均気温（気象庁の平年値）の棒グラフと、4月から3月までの各月に活動している動物の数（5種類中）と植物の育ち方を並べた図。気温が高い5月〜9月は5種類とも活動し、12月〜2月は活動している動物がいない。",
         caption="季節と気温と生き物のようす。あたたかい季節ほど動物の活動がさかんで、植物がよく育つ。"),
    dict(svg=fig2, alt="ツバメ・カエル・テントウムシ・カマキリ・モンシロチョウ・サクラ・ヘチマ・タンポポの、4月（春）・7月（夏）・10月（秋）・1月（冬）のようすと冬ごしのすがた（冬眠・成虫・たまご・さなぎ・芽・たね・ロゼット）をまとめた早見表。",
         caption="季節ごとの生き物のようすと冬ごし。冬ごしのすがたは生き物によってちがう。"),
]
