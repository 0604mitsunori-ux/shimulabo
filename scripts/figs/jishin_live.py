"""今日の地震・最新の地震情報（jishin-live）の図。震度とマグニチュードの違い／震度階級の目安（気象庁の10階級）。
数値・言い方の正：ページ本文（M1でエネルギー約32倍・M2で約1000倍＝10^1.5・10^3）と、
気象庁「震度階級関連解説表」（人の体感・行動／屋内の状況）を短く要約。震度は日付に依存しない目安として描く。"""
from figlib import *

ANCHOR = r"震度とマグニチュードの違い</h2>.*?</table>\n"

# 震度の札の色（弱い→強い）。色だけでなく文字でも区別する
SC = {"0": ("#eef1f3", INK), "1": ("#e3ebf0", INK), "2": ("#d3e2ea", INK), "3": ("#bcd3df", INK),
      "4": ("#f3e3b5", INK), "5弱": ("#f2c98f", INK), "5強": ("#eaa76b", INK),
      "6弱": ("#d9744c", "#fff"), "6強": ("#c4442b", "#fff"), "7": ("#8e2a1a", "#fff")}


def tag(cx, cy, s, size=19, w=None):
    f, c = SC[s]
    w = w or (size * (len(s) + 2.2))
    return rect(cx - w / 2, cy - size * 0.95, w, size * 1.7, f, "#b9b2a3", 8, 1) + \
        text(cx, cy + size * 0.36, "震度" + s if size >= 17 else s, size, c, 700, "middle")


def star(cx, cy, r1, r2, fill):
    import math
    pts = []
    for i in range(10):
        r = r1 if i % 2 == 0 else r2
        a = math.radians(-90 + 36 * i)
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="#fff" stroke-width="1.5"/>'


def house(x, base, w=40, h=30):
    return (rect(x, base - h, w, h, CARD, INK, 0, 1.6)
            + f'<path d="M{x - 5},{base - h} L{x + w / 2},{base - h - 20} L{x + w + 5},{base - h}Z" fill="{CARD}" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>')


def fig1():
    gy, ex, ey = 318, 190, 560          # 地面の y、震源の位置
    b = [f'<defs><clipPath id="under"><rect x="48" y="{gy}" width="650" height="{620 - gy}"/></clipPath></defs>']
    b.append(f'<rect x="48" y="{gy}" width="650" height="{612 - gy}" fill="#efe7d6"/>')
    b.append(line(48, gy, 698, gy, INK, 2.4))
    for r in (120, 215, 310, 405, 500):
        b.append(f'<circle cx="{ex}" cy="{ey}" r="{r}" fill="none" stroke="{GOLD}" stroke-width="2" stroke-dasharray="8 7" opacity=".75" clip-path="url(#under)"/>')
    b.append(line(ex, ey - 16, ex, gy, INK2, 1.6, "4 4"))
    b.append(f'<path d="M{ex - 9},{gy} l9,-14 l9,14z" fill="{INK}"/>')
    b.append(text(ex - 14, gy + 24, "震央", 15, INK, 700, "end"))
    b.append(text(ex - 12, (gy + ey) / 2 + 6, "深さ", 15, INK2, anchor="end"))
    b.append(star(ex, ey, 22, 9, ACC))
    b.append(f'<rect x="{ex + 28}" y="{ey - 28}" width="372" height="58" rx="6" fill="#efe7d6" opacity=".92"/>')
    b.append(text(ex + 34, ey - 6, "震源（岩盤がずれ始めた所）", 16, INK, 700))
    b.append(text(ex + 34, ey + 20, "マグニチュード M6.8（例）は、この地震に1つ", 16, ACC, 700))
    # 町ごとの震度
    for x, s, lab in [(268, "6弱", "震源に近い町"), (458, "4", "少しはなれた町"), (640, "2", "遠い町")]:
        b.append(house(x - 20, gy))
        b.append(tag(x, 236, s, 19, 116))
        b.append(text(x, 196, lab, 15, INK2, anchor="middle"))
    b.append(text(48, 126, "震度＝その場所の揺れの強さ。1つの地震でも場所ごとにちがう", 17, TEAL_D, 700))
    b.append(text(48, 152, "震源から遠いほど小さくなり、地盤がやわらかい所は大きくなりやすい", 15, INK2))
    # 右：比べるカード
    X = 730
    b.append(rect(X, 104, 422, 300, CARD, ACC, 12, 1.6))
    b.append(text(X + 18, 136, "マグニチュード（M）", 21, ACC, 700))
    b.append(lines(X + 18, 166, ["地震そのものの規模（エネルギーの大きさ）。", "1つの地震に、値は1つだけ。"], 16, INK, 1.5))
    b.append(text(X + 18, 228, "M が 1 大きい → エネルギー約32倍", 17, INK, 700))
    b.append(text(X + 18, 256, "M が 2 大きい → 約1000倍", 17, INK, 700))
    s0, gx0, gy0 = 15, X + 22, 280
    for i in range(32):
        c, r = i % 8, i // 8
        b.append(rect(gx0 + c * (s0 + 3), gy0 + r * (s0 + 3), s0, s0, ACC_L, ACC, 2, 1))
    b.append(text(gx0 + 8 * (s0 + 3) + 14, gy0 + 22, "M7の1回分 ＝", 16, INK, 700))
    b.append(text(gx0 + 8 * (s0 + 3) + 14, gy0 + 46, "M6の約32回分", 16, INK, 700))
    b.append(text(gx0, gy0 + 4 * (s0 + 3) + 22, "（M5なら約1000回分）", 15, INK2))
    b.append(rect(X, 418, 422, 196, CARD, TEAL, 12, 1.6))
    b.append(text(X + 18, 450, "震度", 21, TEAL, 700))
    b.append(lines(X + 18, 480, ["その場所がどれだけ揺れたか。", "同じ地震でも、場所ごとにちがう。", "気象庁は10階級で発表："], 16, INK, 1.5))
    cx = X + 20
    for s in ["0", "1", "2", "3", "4", "5弱", "5強", "6弱", "6強", "7"]:
        w = 27 if len(s) == 1 else 41
        b.append(tag(cx + w / 2, 574, s, 14.5, w)); cx += w + 4
    assert cx < X + 422 - 10
    return svg("".join(b), "震度とマグニチュードのちがい",
               "震度の数字は例。実際の震度は、震源の深さ・距離・地盤によって変わる。")


ROWS = [("0", "人は揺れを感じない（地震計には記録される）", "—"),
        ("1", "屋内で静かにしている人の中に、わずかに感じる人がいる", "—"),
        ("2", "屋内で静かにしている人の大半が感じる", "電灯などのつり下げ物がわずかに揺れる"),
        ("3", "屋内にいる人のほとんどが感じる。眠っている人の大半が目を覚ます", "棚の食器類が音を立てることがある"),
        ("4", "ほとんどの人が驚く。眠っている人のほとんどが目を覚ます", "つり下げ物が大きく揺れる。座りの悪い置物が倒れることがある"),
        ("5弱", "大半の人が恐怖を覚え、物につかまりたいと感じる", "食器や本が落ちることがある。固定していない家具が動くことがある"),
        ("5強", "物につかまらないと歩くことが難しい", "落ちる食器や本が多くなる。固定していない家具が倒れることがある"),
        ("6弱", "立っていることが困難になる", "固定していない家具の大半が動き、倒れるものもある。ドアが開かなくなることがある"),
        ("6強", "立っていられず、はわないと動けない。飛ばされることもある", "固定していない家具のほとんどが動き、倒れるものが多くなる"),
        ("7", "（6強と同じ）", "固定していない家具のほとんどが動いたり倒れたりし、飛ぶこともある")]


def wrap(s, n):
    """n 文字ずつで折り返す（句読点で切れるところを優先）"""
    if len(s) <= n:
        return [s]
    cut = max((i + 1 for i, ch in enumerate(s[:n]) if ch in "、。）"), default=n)
    if cut < n * 0.55:
        cut = n
    return [s[:cut]] + wrap(s[cut:], n)


def fig2():
    x0, y0, hh, rh = 48, 100, 38, 48.4
    cw = [92, 486, 526]
    b = [rect(x0, y0, sum(cw), hh + rh * len(ROWS), CARD, LINE, 8)]
    b.append(f'<rect x="{x0}" y="{y0}" width="{sum(cw)}" height="{hh}" rx="8" fill="{TEAL_L}"/>')
    for i, h in enumerate(["震度", "人の感じ方・行動", "屋内のようす"]):
        cx = x0 + sum(cw[:i])
        b.append(text(cx + (cw[i] / 2 if i == 0 else 14), y0 + 25, h, 16, INK, 700, "middle" if i == 0 else "start"))
    for i, (s, p, r) in enumerate(ROWS):
        y = y0 + hh + rh * i
        if i % 2 == 1:
            b.append(f'<rect x="{x0 + 1}" y="{y:.1f}" width="{sum(cw) - 2}" height="{rh:.1f}" fill="#f7f5ef"/>')
        b.append(line(x0, y, x0 + sum(cw), y, LINE, 1))
        b.append(tag(x0 + cw[0] / 2, y + rh / 2 + 1, s, 16, 66))
        for j, (t, n) in enumerate([(p, 29), (r, 31)]):
            ls = wrap(t, n)
            tx = x0 + sum(cw[:j + 1]) + 14
            ty = y + rh / 2 + 5.5 - (len(ls) - 1) * 9.5
            b.append(lines(tx, ty, ls, 15, INK, 1.27))
    b.append(line(x0 + cw[0], y0, x0 + cw[0], y0 + hh + rh * len(ROWS), LINE, 1))
    b.append(line(x0 + cw[0] + cw[1], y0, x0 + cw[0] + cw[1], y0 + hh + rh * len(ROWS), LINE, 1))
    return svg("".join(b), "震度階級の目安（気象庁の10階級）",
               "気象庁「震度階級関連解説表」を短くまとめたもの。表の現象がすべて起きるわけではない。")


FIGS = [
    dict(svg=fig1, alt="震度とマグニチュードの違いを示す図。震源で起きた1つの地震（マグニチュードは1つ）でも、震源に近い町・少しはなれた町・遠い町で震度が6弱・4・2のように場所ごとに違う例と、マグニチュードが1大きいとエネルギーが約32倍、2大きいと約1000倍になること、気象庁の震度は0〜7の10階級であることをまとめている。",
         caption="震度はその場所の揺れの強さ、マグニチュードは地震そのものの規模。1つの地震でマグニチュードは1つ、震度は場所ごとにちがう。"),
    dict(svg=fig2, alt="気象庁の震度階級（震度0・1・2・3・4・5弱・5強・6弱・6強・7の10階級）ごとに、人の感じ方・行動と屋内のようす（つり下げ物・食器・家具など）の目安をまとめた早見表。",
         caption="震度階級の目安。震度5弱から家具が動き始め、6弱では立っていることが困難になる。"),
]
