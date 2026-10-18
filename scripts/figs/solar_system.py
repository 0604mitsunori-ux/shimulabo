"""太陽系シミュレーター（solar-system）の図。
大きさ：理科年表（国立天文台）の赤道半径から直径を出す。きょり・公転周期：ページの表とシミュの JS（周期 0.24〜165年）と同じ値。"""
from figlib import *

# 名前, 赤道半径(km・理科年表), 太陽からの平均きょり(天文単位・ページの表), 公転周期(ページの表), 色
PL = [("水星", 2439.7, 0.39, "88日", "#a9a9a9"),
      ("金星", 6051.8, 0.72, "225日", "#d9a35a"),
      ("地球", 6378.1, 1.00, "365日", "#4a86c8"),
      ("火星", 3396.2, 1.52, "687日", "#c8563a"),
      ("木星", 71492, 5.20, "11.9年", "#c89a6a"),
      ("土星", 60268, 9.54, "29.5年", "#d8bf86"),
      ("天王星", 25559, 19.2, "84年", "#8cc4d6"),
      ("海王星", 24764, 30.1, "165年", "#4f6fc8")]
SUN_R = 696000          # 太陽の半径(km)
AU_KM = 1.496e8         # 1天文単位(km)


def ratio(r):
    v = r / PL[2][1]
    return "1" if abs(v - 1) < 1e-9 else (f"{v:.2f}" if v < 2 else f"{v:.1f}")


def comma(n):
    return f"{n:,}"


def fig1():
    b = []
    E = 20.0                                  # 地球の直径(px)
    s = E / (2 * PL[2][1])                    # 1kmあたりpx
    cy = 330
    sun_r = SUN_R * s
    clip = '<clipPath id="sunclip"><rect x="48" y="120" width="200" height="390"/></clipPath>'
    b.append(f'<circle cx="{116 - sun_r:.1f}" cy="{cy}" r="{sun_r:.1f}" fill="{SUN}" stroke="{GOLD}" stroke-width="2" clip-path="url(#sunclip)"/>')
    b.append(lines(54, 286, ["太陽", "直径は", "地球の", f"約{SUN_R / PL[2][1]:.0f}倍"], 14.5, INK, 1.45, font_weight="700"))
    gaps = [44, 56, 50, 52, 40, 40, 36, 32]
    x = 168
    for (nm, r, au, per, col), g in zip(PL, gaps):
        d = 2 * r * s
        x += g
        cx = x + d / 2
        b.append(circle(cx, cy, d / 2, col, INK2, 1))
        if nm == "土星":
            b.append(text(cx, cy + 5, "（環はのぞく）", 14, INK, anchor="middle"))
        ty = 470 if d > 60 else 400
        b.append(line(cx, cy + d / 2 + 6, cx, ty - 24, LINE, 1.2))
        b.append(text(cx, ty, nm, 17, INK, 700, "middle"))
        b.append(text(cx, ty + 24, f"{ratio(r)}倍", 16, ACC, 700, "middle"))
        x += d
    b.append(text(1152, 128, "地球の直径を1としたときの大きさ（直径）", 16, INK2, anchor="end"))
    # 下：表
    cols = ["", "水星", "金星", "地球", "火星", "木星", "土星", "天王星", "海王星"]
    tb = [["直径（km）"] + [f"{comma(round(2 * r))}" for nm, r, *_ in PL],
          ["地球を1として"] + [ratio(r) for nm, r, *_ in PL]]
    b.append(table(48, 516, cols, tb, [168] + [117] * 8, 34, 15.5))
    return svg("".join(b), "惑星の大きさくらべ（地球＝1）",
               "直径は赤道の直径（km・理科年表の赤道半径の2倍）。大きさの比は正しく、ならべた間かくは実際とちがう。", clip)


def fig2():
    b = []
    # 上：0〜31天文単位のものさし
    x0, x1, y = 96, 1120, 196
    k = (x1 - x0) / 31
    b.append(text(48, 126, "太陽からのきょり（同じ縮尺。点の大きさは実際とちがう）", 17, INK, 700))
    b.append(line(x0, y, x1, y, INK2, 2))
    for t in range(0, 31, 5):
        b.append(line(x0 + t * k, y - 6, x0 + t * k, y + 6, INK2, 1.4) + text(x0 + t * k, y + 28, f"{t}", 14, MUTED, anchor="middle"))
    b.append(text(x1, y + 50, "（天文単位）", 14, MUTED, anchor="end"))
    b.append(circle(x0, y, 9, SUN, GOLD, 1.5) + text(x0, y - 18, "太陽", 15, INK, 700, "middle"))
    for i, (nm, r, au, per, col) in enumerate(PL):
        cx = x0 + au * k
        b.append(circle(cx, y, 6 if i < 4 else 8, col, INK2, 1))
        if i >= 4:
            b.append(text(cx, y - 18, nm, 15, INK, 700, "middle"))
    b.append(arrow(x0 + 0.9 * k, y + 50, x0 + 0.9 * k, y + 14, "muted", 1.6))
    b.append(text(x0 + 0.9 * k + 10, y + 56, "水星・金星・地球・火星は、太陽のすぐ近く（下に拡大）", 14.5, INK2))
    # 中：太陽のまわりを拡大
    y2, z0, z1 = 340, 96, 720
    kz = (z1 - z0) / 1.6
    b.append(text(48, 290, "太陽の近くを拡大（0〜1.6天文単位）", 17, INK, 700))
    b.append(line(z0, y2, z1, y2, INK2, 2))
    for t in (0, 0.5, 1.0, 1.5):
        b.append(line(z0 + t * kz, y2 - 6, z0 + t * kz, y2 + 6, INK2, 1.4) + text(z0 + t * kz, y2 + 28, f"{t:g}", 14, MUTED, anchor="middle"))
    b.append(circle(z0, y2, 9, SUN, GOLD, 1.5) + text(z0, y2 - 18, "太陽", 15, INK, 700, "middle"))
    for nm, r, au, per, col in PL[:4]:
        cx = z0 + au * kz
        b.append(circle(cx, y2, 8, col, INK2, 1) + text(cx, y2 - 18, nm, 15, INK, 700, "middle"))
    b.append(lines(760, 318, ["1天文単位＝太陽と地球のきょり", "（約1億5,000万km。光でも約8分20秒）"], 15.5, INK2, 1.55))
    # 下：表
    cols = ["", "水星", "金星", "地球", "火星", "木星", "土星", "天王星", "海王星"]
    tb = [["きょり（天文単位）"] + [f"{au:g}" if au >= 10 else f"{au:.2f}" for nm, r, au, per, col in PL],
          ["きょり（億km）"] + [f"{au * AU_KM / 1e8:.1f}" if au * AU_KM / 1e8 >= 10 else f"{au * AU_KM / 1e8:.2f}" for nm, r, au, per, col in PL],
          ["公転周期（1周）"] + [per for nm, r, au, per, col in PL]]
    b.append(table(48, 418, cols, tb, [184] + [115] * 8, 40, 15.5))
    return svg("".join(b), "太陽からのきょりと公転周期",
               "遠い惑星ほど1周に時間がかかる（周期の2乗はきょりの3乗に比例）。海王星は地球の約30倍遠い。")


FIGS = [
    dict(svg=fig1, alt="太陽系の8つの惑星の大きさくらべの図。水星・金星・地球・火星・木星・土星・天王星・海王星を直径の比が正しくなるように並べ、地球の直径を1としたときの倍率（木星は約11.2倍）と直径（km）、太陽の直径が地球の約109倍であることを示す。",
         caption="惑星の大きさくらべ（地球＝1）。木星は地球の約11倍、太陽は約109倍。"),
    dict(svg=fig2, alt="太陽から8つの惑星までのきょりを同じ縮尺のものさしで示した図と、水星から火星までの拡大図、各惑星のきょり（天文単位・億km）と公転周期（水星88日〜海王星165年）の早見表。",
         caption="太陽からのきょりと公転周期。内側の4つは太陽の近くにかたまり、遠い惑星ほど1周に時間がかかる。"),
]
