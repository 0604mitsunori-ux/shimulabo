"""人の体のつくりと働き（hito-karada・小6／中2）の授業用の図。
図1：血液の循環。ページのシミュ（scripts/rika/sims_karada_gijutsu.py の KARADA_JS ①）と同じく「体の正面から見た図（図の左が体の右）」で、
  右心房・右心室を図の左、左心房・左心室を図の右にかく。肺循環＝右心室→肺動脈→肺→肺静脈→左心房、体循環＝左心室→大動脈→全身→大静脈→右心房。
  動脈血（酸素が多い）＝朱、静脈血（二酸化炭素が多い）＝藍（シミュの赤・青と同じ割り当て）。肺動脈には静脈血、肺静脈には動脈血。
図2：呼吸・消化と吸収・心臓が送り出す血液の量。数値はページの記事と同じ式（HR0×SV0 など）で計算する。"""
import math
from figlib import *

HR0, SV0, HR1, SV1 = 70, 70, 130, 100       # 安静時・運動中の目安（sims_karada_gijutsu.py と同じ）
BR0, TV0 = 15, 500


def flow(pts, col, w=12, heads=True):
    """血管（太い線）＋流れの向きの三角。長さ40px以上の区間のまん中に三角を置く"""
    out = [poly(pts, col, w)]
    if heads:
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            L = math.hypot(x1 - x0, y1 - y0)
            if L < 40: continue
            ux, uy = (x1 - x0) / L, (y1 - y0) / L; mx, my = (x0 + x1) / 2, (y0 + y1) / 2
            a, h = 9, 7
            p = [(mx + ux * a, my + uy * a), (mx - ux * a - uy * h, my - uy * a + ux * h), (mx - ux * a + uy * h, my - uy * a - ux * h)]
            out.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in p)}" fill="#fff"/>')
    return "".join(out)


def meander(x0, x1, y, amp, grad, n=7):
    """毛細血管（波線）。x0→x1 へ n 回うねる"""
    d = f"M{x0},{y}"
    for i in range(n * 8 + 1):
        t = i / (n * 8); x = x0 + (x1 - x0) * t
        d += f" L{x:.1f},{y - amp * math.sin(t * n * 2 * math.pi):.1f}"
    return f'<path d="{d}" fill="none" stroke="url(#{grad})" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>'


def fig1():
    defs = (f'<linearGradient id="hk-lung" gradientUnits="userSpaceOnUse" x1="270" y1="0" x2="550" y2="0"><stop offset="0" stop-color="{TEAL}"/><stop offset="1" stop-color="{ACC}"/></linearGradient>'
            f'<linearGradient id="hk-body" gradientUnits="userSpaceOnUse" x1="170" y1="0" x2="590" y2="0"><stop offset="0" stop-color="{TEAL}"/><stop offset="1" stop-color="{ACC}"/></linearGradient>')
    b = []
    # 肺
    b.append(rect(230, 100, 360, 96, "#f8eeee", "#d7a9a9", 30, 1.6))
    b.append(text(254, 134, "肺", 22, INK, 700) + text(290, 134, "二酸化炭素を出し、酸素を受けとる", 15, INK2))
    b.append(poly([(260, 196), (260, 166), (270, 166)], TEAL, 7) + meander(270, 550, 166, 10, "hk-lung", 6) + poly([(550, 166), (560, 166), (560, 196)], ACC, 7))
    # 心臓（体の正面から見た図：図の左が体の右）
    b.append(rect(278, 278, 254, 186, CARD, INK2, 26, 1.6))
    ch = [(290, 290, 88, 60, "右心房", TEAL_L, TEAL, 2), (290, 360, 110, 92, "右心室", TEAL_L, TEAL, 2.4),
          (422, 290, 98, 60, "左心房", ACC_L, ACC, 2), (410, 360, 110, 92, "左心室", ACC_L, ACC, 4.5)]
    for x, y, w, h, nm, f, s, sw in ch:
        b.append(rect(x, y, w, h, f, s, 10, sw))
    # 血管（体循環：大動脈・大静脈／肺循環：肺動脈・肺静脈）
    b.append(flow([(130, 592), (130, 320), (290, 320)], TEAL))                       # 大静脈 → 右心房
    b.append(flow([(393, 362), (393, 258), (260, 258), (260, 196)], TEAL))           # 右心室 → 肺動脈 → 肺
    b.append(flow([(560, 196), (560, 236), (470, 236), (470, 290)], ACC))            # 肺 → 肺静脈 → 左心房
    b.append(flow([(520, 405), (650, 405), (650, 592), (600, 592)], ACC))            # 左心室 → 大動脈 → 全身
    b.append(flow([(160, 592), (130, 592)], TEAL, 12, False))
    # 部屋の中の流れ（心房 → 心室）と部屋の名前
    b.append(arrow(330, 334, 330, 384, "ink", 2.2) + arrow(470, 334, 470, 384, "ink", 2.2))
    for x, y, w, h, nm, f, s, sw in ch:
        b.append(text(x + w / 2, y + h / 2 + 6, nm, 17, TEAL_D if "右" in nm else "#9c3320", 700, "middle"))
    # 全身
    b.append(rect(160, 534, 440, 82, "#f4f1ea", "#cfc6b4", 16, 1.6))
    b.append(text(178, 562, "全身", 20, INK, 700) + text(226, 562, "酸素・養分をわたし、二酸化炭素などを受けとる", 15, INK2))
    b.append(meander(170, 590, 594, 9, "hk-body", 9))
    # ラベル
    b.append(text(405, 224, "肺循環", 20, INK, 700, "middle"))
    b.append(text(405, 518, "体循環", 20, INK, 700, "middle"))
    b.append(text(405, 488, "心臓（体の正面から見た図：図の左が体の右）", 15, MUTED, anchor="middle"))
    b.append(text(248, 230, "肺動脈", 17, TEAL_D, 700, "end") + text(248, 250, "静脈血", 15, TEAL_D, anchor="end"))
    b.append(text(574, 226, "肺静脈", 17, "#9c3320", 700) + text(574, 246, "動脈血", 15, "#9c3320"))
    b.append(text(142, 470, "大静脈", 17, TEAL_D, 700) + text(142, 490, "静脈血", 15, TEAL_D))
    b.append(text(664, 470, "大動脈", 17, "#9c3320", 700) + text(664, 490, "動脈血", 15, "#9c3320"))
    # 右：まとめ
    x0 = 790
    b.append(line(x0, 116, x0 + 34, 116, ACC, 10) + text(x0 + 44, 122, "動脈血（酸素が多い血液）", 16, INK, 700))
    b.append(line(x0, 146, x0 + 34, 146, TEAL, 10) + text(x0 + 44, 152, "静脈血（二酸化炭素が多い血液）", 16, INK, 700))
    b.append(table(x0, 172, ["部屋", "つながる血管", "血液"],
                   [["右心房", "大静脈（全身から）", "静脈血"], ["右心室", "肺動脈（肺へ）", "静脈血"],
                    ["左心房", "肺静脈（肺から）", "動脈血"], ["左心室", "大動脈（全身へ）", "動脈血"]], [78, 178, 106], 34, 15))
    b.append(text(x0, 370, "肺循環：右心室→肺動脈→肺→肺静脈→左心房", 15, INK, 700))
    b.append(text(x0, 396, "体循環：左心室→大動脈→全身→大静脈→右心房", 15, INK, 700))
    b.append(rect(x0, 414, 362, 104, GOLD_L, "#e3d3ad", 10))
    b.append(lines(x0 + 14, 442, ["名前は、心臓から出る血管＝動脈、", "心臓にもどる血管＝静脈。だから", "肺動脈には静脈血、肺静脈には動脈血。"], 16, INK, 1.5))
    b.append(lines(x0, 548, ["左心室は全身へ血液を送り出すので、", "かべの筋肉がいちばん厚い。", "部屋の出口や静脈には、逆流を防ぐ弁がある。"], 15, INK2, 1.55))
    return svg("".join(b), "血液の循環（肺循環と体循環）",
               "模式図（大きさ・位置は実際とちがう）。見やすいように動脈血を赤、静脈血を青でかいた（実際の静脈血は暗い赤色）。", defs)


def panel(x, y, w, h, title, col):
    return (rect(x, y, w, h, CARD, LINE, 10) + f'<rect x="{x}" y="{y}" width="{w}" height="6" rx="3" fill="{col}"/>'
            + text(x + 18, y + 38, title, 19, INK, 700))


def fig2():
    b = []
    W_, Y0, H_ = 352, 100, 516
    xs = [48, 424, 800]
    # ① 呼吸
    x = xs[0]; b.append(panel(x, Y0, W_, H_, "① 呼吸（肺）", TEAL))
    b.append(lines(x + 18, Y0 + 70, ["肺胞で、酸素が血液にとりこまれ、", "二酸化炭素が肺胞に出される。"], 15, INK2, 1.5))
    sc = 210 / 21                                           # 1% あたりの長さ
    for i, (nm, o2, co2) in enumerate([("吸う空気", 21, 0.04), ("はいた空気", 17, 4)]):
        y = Y0 + 150 + i * 112
        b.append(text(x + 18, y, nm, 17, INK, 700))
        b.append(f'<rect x="{x + 18}" y="{y + 12}" width="{o2 * sc:.1f}" height="20" rx="3" fill="{GOLD}"/>')
        b.append(text(x + 26 + o2 * sc, y + 28, f"酸素 約{o2}%", 15, GOLD, 700))
        b.append(f'<rect x="{x + 18}" y="{y + 40}" width="{max(2.5, co2 * sc):.1f}" height="20" rx="2" fill="{INK2}"/>')
        b.append(text(x + 26 + max(2.5, co2 * sc), y + 56, f"二酸化炭素 約{co2:g}%", 15, INK2, 700))
    b.append(text(x + 18, Y0 + 368, "残りはおもにちっ素（約78%）", 15, MUTED))
    V0 = BR0 * TV0
    b.append(line(x + 18, Y0 + 392, x + W_ - 18, Y0 + 392, LINE, 1.2))
    b.append(lines(x + 18, Y0 + 422, ["1分間に出入りする空気（安静時）", f"{BR0}回 × {TV0}mL ＝ {V0 / 1000:.1f}L",
                                      f"とりこむ酸素：{V0 / 1000:.1f}L ×（21%−17%）", f"　＝ 約{V0 * 0.04:.0f}mL"], 15, INK, 1.5))
    # ② 消化と吸収
    x = xs[1]; b.append(panel(x, Y0, W_, H_, "② 消化と吸収", GOLD))
    b.append(text(x + 18, Y0 + 72, "口→食道→胃→小腸→大腸→こう門", 16, INK, 700))
    rows = [("デンプン → ブドウ糖", "だ液・すい液のアミラーゼ、小腸の壁"),
            ("タンパク質 → アミノ酸", "胃液のペプシン、すい液のトリプシン、小腸の壁"),
            ("脂肪 → 脂肪酸とモノグリセリド", "胆汁が細かくし、すい液のリパーゼが分解")]
    for i, (a, c) in enumerate(rows):
        y = Y0 + 112 + i * 62
        b.append(rect(x + 14, y - 22, W_ - 28, 54, "#f7f5ef", "none", 8, 0))
        b.append(text(x + 24, y, a, 16, INK, 700) + text(x + 24, y + 22, c, 14, INK2))
    b.append(text(x + 18, Y0 + 316, "小腸の柔毛から吸収する", 16, INK, 700))
    b.append(lines(x + 18, Y0 + 344, ["・ブドウ糖・アミノ酸 → 毛細血管", "　→ 肝臓を通って全身へ", "・脂肪酸とモノグリセリド → 柔毛の中で", "　再び脂肪になり、リンパ管へ", "・水分はおもに小腸で吸収（大腸でも）"], 15, INK2, 1.5))
    # ③ 心臓が送り出す血液の量
    x = xs[2]; b.append(panel(x, Y0, W_, H_, "③ 心臓が送り出す血液の量", ACC))
    Q0, Q1 = HR0 * SV0, HR1 * SV1
    b.append(lines(x + 18, Y0 + 72, ["1分間に送り出す量", "＝ 心拍数 × 1回に送り出す量"], 15, INK2, 1.5))
    b.append(text(x + 18, Y0 + 138, "安静時（おとなの目安）", 16, INK, 700))
    b.append(text(x + 18, Y0 + 168, f"{HR0}回 × {SV0}mL ＝ {Q0:,}mL", 19, INK, 700))
    b.append(text(x + 18, Y0 + 204, f"≒ 約{Q0 / 1000:.1f}L（1分間）", 24, ACC, 700))
    b.append(text(x + 18, Y0 + 248, "運動中（ジョギングくらい）", 16, INK, 700))
    b.append(text(x + 18, Y0 + 276, f"{HR1}回 × {SV1}mL ＝ 約{Q1 / 1000:.0f}L", 19, INK, 700))
    day = Q0 * 1440 / 1000
    b.append(line(x + 18, Y0 + 300, x + W_ - 18, Y0 + 300, LINE, 1.2))
    b.append(lines(x + 18, Y0 + 330, [f"1日では 約{day:,.0f}L（安静時）", f"＝ 200Lのドラム缶 約{int(day / 200)}本分",
                                      "体の血液は約5Lなので、安静時は", "約1分で、体の血液と同じくらいの", "量が心臓から送り出されている。",
                                      "心臓が1回ちぢむと、手首の脈が1回ふれる。"], 15, INK2, 1.5))
    return svg("".join(b), "呼吸・消化と吸収・心臓の働き（まとめ）",
               "数値はおとなの目安（年齢・体格・体調で変わる）。学習用で、医療的な判断には使えない。")


FIGS = [
    dict(svg=fig1, alt="血液の循環（肺循環と体循環）の図。体の正面から見た心臓の4つの部屋（図の左が右心房・右心室、右が左心房・左心室）と、右心室→肺動脈→肺→肺静脈→左心房の肺循環、左心室→大動脈→全身→大静脈→右心房の体循環を、動脈血（酸素が多い）を赤、静脈血（二酸化炭素が多い）を青で示す。肺動脈には静脈血、肺静脈には動脈血が流れる。",
         caption="血液の循環。心臓は体の正面から見た図なので、図の左が体の右（右心房・右心室）。肺動脈には静脈血、肺静脈には動脈血が流れる。"),
    dict(svg=fig2, alt="人の体のつくりと働きのまとめ図。①呼吸：吸う空気（酸素約21%・二酸化炭素約0.04%）とはいた空気（酸素約17%・二酸化炭素約4%）の比較、②消化と吸収：消化管の順番と、デンプン→ブドウ糖・タンパク質→アミノ酸・脂肪→脂肪酸とモノグリセリドの消化酵素、柔毛での吸収、③心臓が1分間に送り出す血液の量（70回×70mL＝約4.9L）。",
         caption="呼吸・消化と吸収・心臓の働きのまとめ。数値はおとなの目安。"),
]
