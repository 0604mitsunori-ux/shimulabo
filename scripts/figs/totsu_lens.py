"""凸レンズの像（totsu-lens）の授業用の図"""
from figlib import *


def ray(pts, c=ACC):
    return poly(pts, c, 2.6)


def fig1():
    ay, lx, f = 392, 600, 150
    a = 3 * f; ox = lx - a; oh = 120                         # 物体：焦点距離の3倍（2倍より遠い）
    bd = a * f / (a - f); ix = lx + bd; ih = -oh * bd / a     # レンズの式 1/a+1/b=1/f で像の位置と大きさ
    ty, iy = ay - oh, ay - ih
    b = [line(60, ay, 1140, ay, MUTED, 1.4), text(1140, ay - 10, "光軸", 14, MUTED, anchor="end")]
    b.append(f'<ellipse cx="{lx}" cy="{ay}" rx="16" ry="150" fill="{TEAL_L}" stroke="{TEAL}" stroke-width="2"/>'
             + line(lx, ay - 150, lx, ay + 150, TEAL, 1, "4 4") + text(lx, ay - 160, "凸レンズ", 17, TEAL, 700, "middle"))
    for x, t in [(lx - f, "焦点"), (lx + f, "焦点"), (lx - 2 * f, "焦点距離の2倍"), (lx + 2 * f, "焦点距離の2倍")]:
        b.append(circle(x, ay, 5, INK, INK, 0) + text(x, ay + 30, t, 14, INK, anchor="middle"))
    s1 = (ay - ty) / f
    b.append(ray([(ox, ty), (lx, ty), (990, ty + s1 * (990 - lx))]))
    s2 = (ay - ty) / (lx - ox)
    b.append(ray([(ox, ty), (1100, ty + s2 * (1100 - ox))]))
    s3 = (ay - ty) / (lx - f - ox); yl = ty + s3 * (lx - ox)
    b.append(ray([(ox, ty), (lx, yl), (1100, yl)]))
    b.append(text(lx - 190, ty - 12, "① 光軸に平行な光", 14, ACC))
    b.append(text(lx - 250, ty + 36, "② 中心を通る光", 14, ACC))
    b.append(text(lx - 205, yl + 30, "③ 焦点を通る光", 14, ACC))
    b.append(line(ox, ay, ox, ty + 8, INK, 5) + f'<path d="M{ox},{ty} l-11,16 h22z" fill="{INK}"/>' + text(ox, ty - 14, "物体", 17, INK, 700, "middle"))
    b.append(line(ix, ay, ix, iy - 8, TEAL, 5) + f'<path d="M{ix:.1f},{iy:.1f} l-11,-16 h22z" fill="{TEAL}"/>'
             + text(ix + 16, iy + 34, "実像（上下逆・物体より小さい）", 17, TEAL, 700))
    b.append(text(60, 126, f"物体の位置：焦点距離の{a / f:.0f}倍　→　像の位置：焦点距離の{bd / f:.1f}倍（焦点と焦点距離の2倍の間）・大きさ {abs(ih) / oh:.1f}倍", 16, INK))
    return svg("".join(b), "凸レンズでできる像の作図（物体が焦点距離の2倍より遠いとき）",
               "3本の光のうち2本をかけば、交わった所に像ができる。光はレンズの中心の線で1回曲げてかく（教科書の約束）。")


def fig2():
    b = []
    # 上：物体の位置のものさし
    y = 150; lx = 980; f = 150
    b.append(line(80, y, 1100, y, MUTED, 1.4))
    b.append(f'<ellipse cx="{lx}" cy="{y}" rx="9" ry="40" fill="{TEAL_L}" stroke="{TEAL}" stroke-width="2"/>' + text(lx, y - 50, "凸レンズ", 15, TEAL, 700, "middle"))
    zones = [(80, lx - 2 * f, "A", "#f6eedc"), (lx - 2 * f, lx - f, "C", "#eef3f6"), (lx - f, lx, "E", "#fbeae6")]
    for x0, x1, t, c in zones:
        b.append(f'<rect x="{x0}" y="{y - 22}" width="{x1 - x0}" height="44" fill="{c}" opacity=".9"/>' + text((x0 + x1) / 2, y + 7, t, 20, INK, 700, "middle"))
    for x, t, k in [(lx - 2 * f, "焦点距離の2倍", "B"), (lx - f, "焦点", "D")]:
        b.append(line(x, y - 30, x, y + 30, INK, 2) + badge(x, y + 48, k, INK, "#fff", 15) + text(x, y - 36, t, 14, INK, anchor="middle"))
    b.append(text(80, y - 36, "← 物体をおく位置（レンズの左側）", 14, MUTED))
    # 下：早見表
    rows = [["A", "焦点距離の2倍より遠い", "実像", "上下左右が逆", "物体より小さい", "カメラ"],
            ["B", "焦点距離の2倍", "実像", "上下左右が逆", "物体と同じ", "—"],
            ["C", "焦点と焦点距離の2倍の間", "実像", "上下左右が逆", "物体より大きい", "プロジェクター"],
            ["D", "焦点", "像はできない", "—", "—", "—"],
            ["E", "焦点より近い", "虚像", "物体と同じ向き", "物体より大きい", "虫めがね"]]
    b.append(table(60, 236, ["", "物体の位置", "像", "向き", "大きさ", "使われ方"], rows, [50, 290, 150, 190, 190, 210], 54, 16.5))
    return svg("".join(b), "物体の位置と凸レンズの像（早見表）",
               "実像はスクリーンにうつる像、虚像はレンズをのぞくと見える像（スクリーンにはうつらない）。")


FIGS = [
    dict(svg=fig1, alt="凸レンズの作図。物体を焦点距離の2倍より遠く（3倍）に置いたとき、光軸に平行な光・レンズの中心を通る光・焦点を通る光の3本が交わり、焦点と焦点距離の2倍の位置の間に上下逆で小さい実像ができることを示す図。",
         caption="作図のしかた（物体が焦点距離の2倍より遠いとき）。3本の光のうち2本で像の位置が決まる。"),
    dict(svg=fig2, alt="物体を置く位置（焦点距離の2倍より遠い・2倍・焦点と2倍の間・焦点・焦点より近い）ごとに、できる像（実像・虚像）、向き、大きさ、使われ方（カメラ・プロジェクター・虫めがね）をまとめた早見表。",
         caption="物体の位置と像の早見表。物体を近づけるほど、実像は大きくレンズから遠くにできる。"),
]
