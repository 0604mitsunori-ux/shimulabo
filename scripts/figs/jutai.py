"""渋滞は勝手に生まれる（jutai）の図。
ページの JS と同じモデル（最適速度モデル：N=42台・A=1.0・DT=0.10・SUB=2・Vopt(h)=tanh(h-2)+tanh(2)、
均等配置＋同じゆらぎ）を Python で動かして描く。色分けのしきい値も JS と同じ（最高速度の33%未満＝渋滞、66%未満＝減速）。"""
import math
from figlib import *

ANCHOR = r"シンプルなルール.*?</p>\s*"

N, A, DT, SUB = 42, 1.0, 0.10, 2
VMAX = math.tanh(8 - 2) + math.tanh(2)


def vopt(h):
    return math.tanh(h - 2) + math.tanh(2)


def init(L):
    gap = L / N
    # JS の (Math.sin(i*12.9898)*43758.5453 % 1)*0.6（JS の % は割られる数の符号）
    return [{"x": math.fmod(i * gap + math.fmod(math.sin(i * 12.9898) * 43758.5453, 1) * 0.6, L), "v": VMAX} for i in range(N)]


def step(cars, L):
    cars.sort(key=lambda c: c["x"])
    for _ in range(SUB):
        for i in range(N):
            h = cars[(i + 1) % N]["x"] - cars[i]["x"]
            if h <= 0: h += L
            cars[i]["a"] = A * (vopt(h) - cars[i]["v"])
        for c in cars:
            c["v"] = max(0.0, c["v"] + c["a"] * DT)
            c["x"] = math.fmod(c["x"] + c["v"] * DT, L)


def mark(x, y, v):
    """車1台。渋滞＝朱の四角、減速中＝金の丸、スムーズ＝藍の白抜き丸（形でも区別）"""
    r = v / VMAX
    if r < 0.33:
        return f'<rect x="{x - 5.5:.1f}" y="{y - 5.5:.1f}" width="11" height="11" fill="{ACC}"/>'
    if r < 0.66:
        return circle(x, y, 4.6, GOLD, GOLD, 0)
    return circle(x, y, 4.6, CARD, TEAL, 1.8)


L0 = 83          # ページの初期値（スライダー value=82 は step=2 の都合で 83 になる）
ROWS = list(range(0, 601, 50))


def snapshots(L=L0):
    cars = init(L); snap = {0: [(c["x"], c["v"]) for c in cars]}
    for f in range(1, ROWS[-1] + 1):
        step(cars, L)
        if f in ROWS: snap[f] = [(c["x"], c["v"]) for c in cars]
    return snap


def jam_runs(row):
    """渋滞（33%未満）の車のかたまり → [(はじめのx, おわりのx, 台数)]（リングのつなぎ目をまたぐものは除く）"""
    cs = sorted(row); out, cur = [], []
    for x, v in cs:
        if v < VMAX * 0.33: cur.append(x)
        elif cur: out.append(cur); cur = []
    if cur: out.append(cur)
    return [(c[0], c[-1], len(c)) for c in out]


def fig1():
    snap = snapshots()
    x0, x1, y0, dy = 92, 700, 186, 33
    px = lambda x: x0 + (x1 - x0) * x / L0
    b = [text(x0, 124, "道路のようす（リングを1本にのばした図・42台）", 17, INK, 700)]
    b.append(arrow(x1 - 128, 152, x1 - 4, 152, "teal", 2.4) + text(x1 - 136, 157, "車の進む向き", 15, TEAL, anchor="end"))
    b.append(mark(x0 + 8, 152, VMAX) + text(x0 + 22, 157, "スムーズ", 15, INK2))
    b.append(mark(x0 + 112, 152, VMAX * 0.5) + text(x0 + 126, 157, "減速中", 15, INK2))
    b.append(mark(x0 + 202, 152, 0) + text(x0 + 216, 157, "渋滞（ほぼ止まる）", 15, INK2))
    track = []
    for k, f in enumerate(ROWS):
        y = y0 + k * dy
        b.append(line(x0, y, x1, y, LINE, 1.2))
        b.append(text(x0 - 12, y + 5, "出発" if f == 0 else f"{f}", 14, MUTED, anchor="end"))
        for x, v in snap[f]:
            b.append(mark(px(x), y, v))
        # 追いかける渋滞：150コマ目に x≒50 にあるかたまりを、1つ前の位置から一番近いもので追う
        if f >= 150:
            runs = jam_runs(snap[f]); prev = track[-1][0] if track else 51
            if runs:
                r = min(runs, key=lambda r: abs((r[0] + r[1]) / 2 - prev))
                c = (r[0] + r[1]) / 2
                if abs(c - prev) < 8: track.append((c, y))
    b.append(text(48, y0 - 30, "時間", 14, MUTED, anchor="middle"))
    b.append(arrow(48, y0 - 18, 48, y0 + 12 * dy, "muted", 2))
    if len(track) >= 2:
        d = "M" + " L".join(f"{px(c) + 15:.1f},{y:.1f}" for c, y in track)
        b.append(f'<path d="{d}" fill="none" stroke="{ACC}" stroke-width="2.6" stroke-dasharray="7 5" marker-end="url(#ah-acc)"/>')
        xe = px(track[-1][0]) + 15
        b.append(text(xe - 6, y0 + 12 * dy + 30, "渋滞の波は後ろへ進む（車の進む向きと逆）", 16, ACC, 700, "middle"))
    # 右：しくみ
    X = 748
    b.append(rect(X, 108, 404, 100, TEAL_L, TEAL, 10, 1.2))
    b.append(text(X + 18, 138, "どの車も同じルールで走る", 17, TEAL_D, 700))
    b.append(lines(X + 18, 168, ["前との車間がせまい → ゆるめる", "前との車間が広い → 加速する"], 16, INK, 1.5))
    steps = [("1", ["ほんの少し車間がつまった車が、", "少しだけブレーキをかける"]),
             ("2", ["後ろの車は、前が減速してから減速", "する。反応がおくれる分、強めにふむ"]),
             ("3", ["ブレーキが後ろへ次々と大きくなって", "伝わり、止まりかけの車がかたまる"]),
             ("4", ["先頭の車は前があいて抜け出し、", "後ろに車が加わる → 渋滞は後ろへ進む"])]
    for i, (no, rows) in enumerate(steps):
        yy = 252 + i * 92
        b.append(badge(X + 16, yy - 6, no, ACC if i >= 2 else TEAL))
        b.append(lines(X + 40, yy, rows, 16, INK, 1.45))
    return svg("".join(b), "自然渋滞のしくみ（ブレーキの波が後ろへ伝わる）",
               "シミュのはじめの設定で走らせたときの計算。左の数字は経過したコマ数。事故も工事もないのに渋滞の波が生まれる。")


def sweep(frames=4000, keep=1000):
    out = []
    for L in range(63, 140, 2):                 # スライダー（min63・step2）で選べる値
        cars = init(L); acc = 0.0; jam = 0
        for f in range(1, frames + 1):
            step(cars, L)
            if f > frames - keep:
                acc += sum(c["v"] for c in cars) / N
        jam = sum(1 for c in cars if c["v"] < VMAX * 0.33)
        out.append((L, acc / keep / VMAX * 100, jam))
    return out


def word(l):     # JS の densityWord と同じ区切り
    return "かなりゆとり" if l >= 125 else "ゆとりがある" if l >= 110 else "ふつう" if l >= 95 else "やや混雑" if l >= 80 else "過密"


def fig2():
    data = sweep()
    gx0, gy0, gw, gh = 120, 520, 640, 360          # 原点（左下）
    lo, hi = 62, 140
    px = lambda l: gx0 + gw * (l - lo) / (hi - lo)
    py = lambda s: gy0 - gh * s / 100
    b = [axes(gx0, gy0, gw, gh, "", "平均速度（%）", [], [(gh * s / 100, f"{s}") for s in (0, 20, 40, 60, 80, 100)], 15)]
    # スライダーの言葉の帯
    bands = [(lo, 80, "過密"), (80, 95, "やや混雑"), (95, 110, "ふつう"), (110, 125, "ゆとりがある"), (125, hi, "かなりゆとり")]
    for i, (a_, z, t) in enumerate(bands):
        b.append(f'<rect x="{px(a_):.1f}" y="{gy0 + 8}" width="{px(z) - px(a_):.1f}" height="30" fill="{"#efece4" if i % 2 else "#f6f3ec"}"/>')
        b.append(text((px(a_) + px(z)) / 2, gy0 + 29, t, 14.5, INK2, 700, "middle"))
    b.append(text(gx0 + gw / 2, gy0 + 68, "スライダー「混雑度（車の間隔）」の位置　　せまい ← → 広い", 15, INK, anchor="middle"))
    jam_last = max(l for l, s, j in data if j > 0)
    clear_first = min(l for l, s, j in data if j == 0)
    xb = (px(jam_last) + px(clear_first)) / 2
    b.append(f'<rect x="{gx0}" y="{gy0 - gh}" width="{xb - gx0:.1f}" height="{gh}" fill="{ACC_L}" opacity=".55"/>')
    b.append(line(xb, gy0 - gh, xb, gy0, ACC, 1.6, "6 5"))
    b.append(text(gx0 + 14, gy0 - gh + 26, "渋滞の波ができる", 17, ACC, 700))
    pts = [(px(l), py(s)) for l, s, j in data]
    b.append(poly([p for p, (l, s, j) in zip(pts, data) if j > 0], ACC, 2.2))
    b.append(poly([p for p, (l, s, j) in zip(pts, data) if j == 0], TEAL, 2.2))
    for (x, y), (l, s, j) in zip(pts, data):
        b.append(f'<rect x="{x - 4.5:.1f}" y="{y - 4.5:.1f}" width="9" height="9" fill="{ACC}"/>' if j > 0 else circle(x, y, 4.6, CARD, TEAL, 1.8))
    d = {l: (s, j) for l, s, j in data}
    s1, j1 = d[jam_last]; s2, j2 = d[clear_first]; s0, j0 = d[L0]
    b.append(line(px(jam_last) - 4, py(s1) + 8, px(jam_last) - 56, py(s1) + 78, MUTED, 1.2))
    b.append(lines(px(jam_last) - 196, py(s1) + 100, ["渋滞する一番広い間隔", f"平均{s1:.0f}%・渋滞中の車{j1}台"], 15, INK2))
    b.append(text(xb + 14, py(s2) + 46, "渋滞しない", 17, TEAL_D, 700))
    b.append(lines(xb + 14, py(s2) + 74, ["少し広げただけで", f"平均{s2:.0f}%・渋滞中の車0台"], 15, INK2))
    b.append(line(px(L0), py(s0) + 8, px(L0) + 16, py(s0) + 44, MUTED, 1.2))
    b.append(text(px(L0) + 20, py(s0) + 60, f"はじめの設定：平均{s0:.0f}%", 15, INK2))
    # 右：防ぐコツ
    X = 830
    b.append(rect(X, 108, 322, 300, CARD, LINE, 10))
    b.append(text(X + 18, 140, "自然渋滞を防ぐコツ", 18, INK, 700))
    tips = [("車間距離を広めにとる", ["ブレーキの連鎖を吸収できる"]),
            ("一定の速度を保つ", ["加減速が少ないほど", "後ろへ伝わる波が小さい"]),
            ("合流はゆずり合う", ["つめすぎない方が", "全体の流れは速くなる"])]
    yy = 180
    for i, (h, rows) in enumerate(tips):
        b.append(badge(X + 28, yy - 6, str(i + 1), TEAL))
        b.append(text(X + 50, yy, h, 16.5, INK, 700))
        b.append(lines(X + 50, yy + 26, rows, 15, INK2, 1.5))
        yy += 34 + 23 * len(rows) + 12
    b.append(rect(X, 424, 322, 104, GOLD_L, GOLD, 10, 1.2))
    b.append(lines(X + 18, 456, ["実際の高速道路では、1車線あたり", "1kmに約25台（車間およそ40m）を", "こえると起きやすいとされる。"], 15, INK, 1.55))
    return svg("".join(b), "混雑度と平均速度（シミュの結果）",
               "平均速度は最高速度に対する%（シミュの表示と同じ）。十分に走らせたあとの平均。帯の言葉はスライダー横の表示。")


FIGS = [
    dict(svg=fig1, alt="自然渋滞のしくみの図。リング道路を走る42台の車のようすを時間ごとに並べ、ほぼ等間隔で走っていた車の中から、わずかなゆらぎで止まりかけの車のかたまり（渋滞）が生まれ、その渋滞の波が車の進む向きとは逆の後ろへ進んでいくことを示す。前との車間でブレーキと加速を決める同じルールと、ブレーキが後ろへ伝わる4つの段階の説明つき。",
         caption="自然渋滞のしくみ。少しのブレーキが後ろの車へ大きくなって伝わり、渋滞の波は後ろへ進む（シミュと同じ計算）。"),
    dict(svg=fig2, alt="渋滞シミュレーターで混雑度（車の間隔）を変えたときの平均速度のグラフ。車間がせまいと渋滞の波ができて平均速度が下がり、ある間隔より広いと渋滞しなくなる境目を示し、車間距離を広めにとる・一定の速度を保つ・合流はゆずり合うという自然渋滞を防ぐコツをまとめた図。",
         caption="混雑度と平均速度。車間がある広さより狭いと渋滞の波が生まれ、平均速度ががくんと下がる。"),
]
