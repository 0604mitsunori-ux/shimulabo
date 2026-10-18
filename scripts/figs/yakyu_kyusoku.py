"""球速→反応時間シミュレーター（yakyu-kyusoku）の図。
ページの JS と同じ式：秒速 ＝ 時速(km/h) ÷ 3.6、到達時間 ＝ 距離 ÷ 秒速（距離の初期値 18.44m＝投手板から本塁まで）。
人の反応時間 約0.2秒 は本文の値。"""
from figlib import *

ANCHOR = r"スポーツの奥深さ。</p>\s*"

DIST, REACT = 18.44, 0.2


def t_of(kmh, dist=DIST):
    return dist / (kmh / 3.6)


def fig1():
    kmh = 140; v = kmh / 3.6; T = t_of(kmh)
    x0, x1, gy = 110, 1090, 300
    k = (x1 - x0) / DIST
    b = [line(x0 - 40, gy, x1 + 40, gy, "#c9bfa6", 3)]
    # 投手板と本塁
    b.append(rect(x0 - 22, gy - 4, 44, 8, CARD, INK, 2, 1.6) + text(x0, gy + 34, "投手板", 16, INK, 700, "middle"))
    b.append(f'<path d="M{x1 - 18},{gy - 6} h36 v8 l-18,10 l-18,-10z" fill="{CARD}" stroke="{INK}" stroke-width="1.6"/>' + text(x1, gy + 40, "本塁（打者）", 16, INK, 700, "middle"))
    b.append(line(x0, gy + 58, x1, gy + 58, INK2, 1.4) + line(x0, gy + 50, x0, gy + 66, INK2, 1.4) + line(x1, gy + 50, x1, gy + 66, INK2, 1.4))
    b.append(text((x0 + x1) / 2, gy + 84, f"{DIST}m", 18, INK, 700, "middle"))
    # 0.1秒ごとのボールの位置
    t = 0.0; i = 0
    while t < T - 1e-9:
        x = x0 + v * t * k
        b.append(circle(x, gy - 46, 9, CARD, ACC, 2))
        b.append(line(x, gy - 34, x, gy - 6, LINE, 1.2))
        b.append(text(x, gy - 68, f"{t:.1f}秒", 16, INK, 700 if i == 0 else 400, "middle"))
        b.append(text(x, gy + 22 if 0 < i else gy + 22, "" if i == 0 else f"{v * t:.1f}m", 14, MUTED, anchor="middle"))
        i += 1; t = round(t + 0.1, 10)
    b.append(circle(x1, gy - 46, 9, ACC, ACC, 0))
    b.append(text(x1, gy - 68, f"{T:.2f}秒", 18, ACC, 700, "middle"))
    b.append(text(x1, gy - 92, "到着", 16, ACC, 700, "middle"))
    b.append(text(x0, 128, f"時速{kmh}kmの球（0.1秒ごとの位置）", 18, INK, 700))
    # 下：時間の帯
    by = 456
    xr = x0 + (T - REACT) / T * (x1 - x0)
    b.append(text(x0, by - 24, f"投げてから届くまでの {T:.2f}秒", 17, INK, 700))
    b.append(rect(x0, by, xr - x0, 40, TEAL_L, TEAL, 4, 1.4))
    b.append(rect(xr, by, x1 - xr, 40, ACC_L, ACC, 4, 1.4))
    b.append(text((x0 + xr) / 2, by + 26, f"判断に使える時間 約{T - REACT:.2f}秒", 16, TEAL_D, 700, "middle"))
    b.append(text((xr + x1) / 2, by + 26, f"反応 約{REACT}秒", 16, ACC, 700, "middle"))
    b.append(lines(x0, by + 76, [f"人は見てから体が動き出すまでに約{REACT}秒かかる。投げてから約{T - REACT:.2f}秒（球が残り約{v * REACT:.1f}m）までに",
                                 "打つかどうかを決めないと、体が動き出す前にボールが届いてしまう。だから打者は「予測」して振る。"], 16, INK2, 1.6))
    b.append(rect(760, 108, 392, 76, GOLD_L, GOLD, 10, 1.2))
    b.append(text(778, 138, f"秒速 ＝ {kmh} ÷ 3.6 ＝ {v:.1f} m/s", 17, INK, 700))
    b.append(text(778, 168, f"到達時間 ＝ {DIST} ÷ {v:.1f} ＝ {T:.2f}秒", 17, INK, 700))
    return svg("".join(b), "時速140kmの球が本塁に届くまで",
               "変化球や、投手がボールを離す位置（投手板より前）は考えない単純計算。シミュの計算と同じ。")


def fig2():
    speeds = [100, 110, 120, 130, 140, 150, 160, 165]
    X = [48, 208, 368, 528]
    y0, hh, rh = 112, 44, 54
    bx0, bx1, tmax = 560, 1110, 0.7
    k = (bx1 - bx0) / tmax
    b = [rect(48, y0, 1104, hh + rh * len(speeds), CARD, LINE, 8),
         f'<rect x="48" y="{y0}" width="1104" height="{hh}" rx="8" fill="{TEAL_L}"/>']
    for (x, w), h in zip([(48, 160), (208, 160), (368, 160)], ["球速", "秒速", "到達時間"]):
        b.append(text(x + w / 2, y0 + 29, h, 16, INK, 700, "middle"))
    b.append(text(bx0, y0 + 29, "本塁に届くまでの時間", 16, INK, 700))
    b.append(line(bx1 - 152, y0 + 23, bx1 - 124, y0 + 23, ACC, 1.8, "6 5"))
    b.append(text(bx1 + 30, y0 + 29, f"人の反応時間 約{REACT}秒", 15, ACC, 700, "end"))
    for i, s in enumerate(speeds):
        y = y0 + hh + rh * i; t = t_of(s); v = s / 3.6
        if i % 2: b.append(f'<rect x="49" y="{y}" width="1102" height="{rh}" fill="#f7f5ef"/>')
        b.append(line(48, y, 1152, y, LINE, 1))
        hl = s == 140
        b.append(text(128, y + 34, f"時速{s}km", 17, ACC if hl else INK, 700, "middle"))
        b.append(text(288, y + 34, f"{v:.1f} m/s", 17, INK, 400, "middle"))
        b.append(text(448, y + 34, f"{t:.2f}秒", 18, ACC if hl else INK, 700, "middle"))
        b.append(f'<rect x="{bx0}" y="{y + 15}" width="{t * k:.1f}" height="24" rx="3" fill="{ACC_L if hl else TEAL_L}" stroke="{ACC if hl else TEAL}" stroke-width="1.2"/>')
        b.append(text(bx0 + t * k + 8, y + 33, f"{t * 1000:.0f}ms", 15, INK2))
    yb = y0 + hh + rh * len(speeds)
    for tt in (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7):
        b.append(line(bx0 + tt * k, yb, bx0 + tt * k, yb + 6, INK2, 1.2) + text(bx0 + tt * k, yb + 22, f"{tt:g}", 14, MUTED, anchor="middle"))
    b.append(text(bx1 + 30, yb + 22, "秒", 14, MUTED, anchor="end"))
    xr = bx0 + REACT * k
    b.append(line(xr, y0 + hh - 4, xr, yb, ACC, 1.8, "6 5"))
    return svg("".join(b), f"球速と、本塁に届くまでの時間（早見表・{DIST}m）",
               "到達時間＝18.44m ÷（時速÷3.6）。時速10km速くなるごとに、約0.03〜0.06秒短くなる。")


FIGS = [
    dict(svg=fig1, alt="時速140kmの球が投手板から本塁までの18.44mを進む様子を0.1秒ごとの位置で示した図。秒速は140÷3.6＝38.9m/s、到達時間は18.44÷38.9＝0.47秒で、人の反応時間約0.2秒を引くと判断に使える時間は約0.27秒しかないことを示す。",
         caption="時速140kmの球は0.47秒で本塁に届く。反応に約0.2秒かかるので、判断に使えるのは約0.27秒。"),
    dict(svg=fig2, alt="球速（時速100kmから165km）ごとの秒速と、投手板から本塁まで18.44mを進む到達時間の早見表。時速100kmで0.66秒、140kmで0.47秒、165kmで0.40秒になることを棒グラフと人の反応時間約0.2秒の線で示す。",
         caption="球速と本塁に届くまでの時間の早見表。時速100kmで0.66秒、165kmでは0.40秒。"),
]
