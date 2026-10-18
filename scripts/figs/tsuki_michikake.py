"""月の満ち欠けの仕組み（tsuki-michikake）の授業用の図"""
import math
from figlib import *

NAMES = [("①", "新月", "0"), ("②", "三日月", "約3"), ("③", "上弦の月", "約7"), ("④", "満月の前", "約11"),
         ("⑤", "満月", "約15"), ("⑥", "満月の後", "約18"), ("⑦", "下弦の月", "約22"), ("⑧", "二十六夜の月", "約26")]


def fig1():
    cx, cy, R, er, mr = 395, 368, 190, 46, 20
    b = []
    for y in range(126, 616, 46):
        b.append(arrow(56, y, 138, y, "gold", 2.4))
    b.append(text(58, 114, "太陽の光", 17, GOLD, 700))
    b.append(circle(cx, cy, R, "none", LINE, 2))
    a0, a1 = math.radians(300), math.radians(330); RR = R + 34
    p0 = (cx + RR * math.cos(a0), cy - RR * math.sin(a0)); p1 = (cx + RR * math.cos(a1), cy - RR * math.sin(a1))
    b.append(f'<path d="M{p0[0]:.1f},{p0[1]:.1f} A{RR},{RR} 0 0 0 {p1[0]:.1f},{p1[1]:.1f}" fill="none" stroke="{TEAL}" stroke-width="2.4" marker-end="url(#ah-teal)"/>')
    b.append(text(p0[0] + 40, p0[1] + 30, "月の公転の向き", 15, TEAL, anchor="middle"))
    b.append(circle(cx, cy, er, "#2f4f6b", "#2f4f6b", 0) + f'<path d="M{cx},{cy - er} A{er},{er} 0 0 0 {cx},{cy + er}Z" fill="{SKY}"/>'
             + text(cx, cy + 6, "地球", 17, "#fff", 700, "middle"))
    for i, (no, nm, age) in enumerate(NAMES):
        phi = math.radians(180 + 45 * i)            # 新月＝太陽の側（左）から反時計回りに45°ずつ
        mx, my = cx + R * math.cos(phi), cy - R * math.sin(phi)
        b.append(circle(mx, my, mr, MOON_D, MOON_D, 0) + f'<path d="M{mx:.1f},{my - mr:.1f} A{mr},{mr} 0 0 0 {mx:.1f},{my + mr:.1f}Z" fill="{SUN}"/>')
        lx, ly = cx + (R - 46) * math.cos(phi), cy - (R - 46) * math.sin(phi)
        b.append(text(lx, ly + 7, no, 20, INK, 700, "middle"))
    b.append(text(cx, cy + R + 64, "北極の上から見た図（大きさ・きょりは実際とちがう）", 14, MUTED, anchor="middle"))
    x0, y0 = 700, 108
    b.append(text(x0, y0 + 10, "地球（日本）から見た月の形", 19, INK, 700))
    for i, (no, nm, age) in enumerate(NAMES):
        col, row = i % 4, i // 4
        bx, by = x0 + col * 113, y0 + 34 + row * 236
        b.append(rect(bx, by, 103, 220))
        b.append(text(bx + 51.5, by + 30, no, 20, INK, 700, "middle"))
        b.append(moon_look(bx + 51.5, by + 92, 34, 45 * i))
        b.append(text(bx + 51.5, by + 162, nm, 15 if len(nm) <= 5 else 12.5, INK, 700, "middle"))
        b.append(text(bx + 51.5, by + 188, f"月齢 {age}", 13, MUTED, anchor="middle"))
    return svg("".join(b), "月の満ち欠けのしくみ",
               "月はいつも太陽の側の半分が光っている。地球から見える「光った部分」の形が、月の位置で変わる。")


def fig2():
    b = []
    # 左：夕方6時ごろ、南を向いて見た空
    x0, x1, hy = 60, 600, 520
    b.append(rect(x0, 104, x1 - x0, 470, "#eef3f6", LINE, 12))
    b.append(f'<path d="M{x0 + 40},{hy} A{(x1 - x0 - 80) / 2},{300} 0 0 1 {x1 - 40},{hy}" fill="none" stroke="{MUTED}" stroke-dasharray="5 6" stroke-width="1.6"/>')
    b.append(f'<rect x="{x0}" y="{hy}" width="{x1 - x0}" height="54" fill="#d8cfb8"/>')
    for x, t in [(x0 + 40, "東"), ((x0 + x1) / 2, "南"), (x1 - 40, "西")]:
        b.append(text(x, hy + 36, t, 20, INK, 700, "middle"))
    b.append(text(x0 + 20, 138, "夕方6時ごろ、南を向いて見た空", 18, INK, 700))
    for x, y, th, nm, lx, ly, anc in [(x0 + 78, hy - 46, 180, "満月（東からのぼってくる）", x0 + 112, hy - 40, "start"),
                                      ((x0 + x1) / 2, 228, 90, "上弦の月（南の空）", (x0 + x1) / 2, 278, "middle"),
                                      (x1 - 80, hy - 70, 40, "三日月（西の空の低い所）", x1 - 80, hy - 20, "middle")]:
        b.append(moon_look(x, y, 26, th))
        b.append(text(lx, ly, nm, 14.5, INK, 700, anc))
    b.append(text((x0 + x1) / 2, hy - 120, "← 東からのぼり、南を通って、西へしずむ →", 14, MUTED, anchor="middle"))
    # 右：早見表
    b.append(text(640, 138, "形ごとの見えやすい時刻と方角（目安）", 18, INK, 700))
    b.append(table(640, 156, ["形", "南の空に来る時刻", "見えやすい時間"],
                   [["三日月", "午後3時ごろ", "夕方の西の空"],
                    ["上弦の月", "夕方6時ごろ", "夕方〜真夜中"],
                    ["満月", "真夜中0時ごろ", "一晩中"],
                    ["下弦の月", "明け方6時ごろ", "真夜中〜朝"]],
                   [120, 190, 202], 52, 16))
    b.append(lines(640, 452, ["・新月は正午ごろ南の空に来る。そこから1日に約50分ずつおそくなる。", "・どの月も、東からのぼって南を通り、西へしずむ", "　（太陽と同じ動き方）。"], 15.5, INK2))
    return svg("".join(b), "月の形と見える時刻・方角",
               "時刻は東京あたりの目安。季節や場所で少しずれる。")


FIGS = [
    dict(svg=fig1, alt="月の満ち欠けのしくみの図。太陽の光が左から当たり、地球のまわりを回る月の8つの位置（新月・三日月・上弦の月・満月・下弦の月など）と、それぞれの位置で地球（日本）から見た月の形と月齢を並べている。",
         caption="月の位置と見え方。月はいつも太陽の側の半分が光り、地球から見える光った部分の形が変わる。"),
    dict(svg=fig2, alt="夕方6時ごろ南を向いて見た空に、東の満月・南の上弦の月・西の低い所の三日月を描いた図と、三日月・上弦の月・満月・下弦の月の南中時刻と見えやすい時間の早見表。",
         caption="月の形と見える時刻・方角（目安）。夕方に見える位置から月の形がわかる。"),
]
