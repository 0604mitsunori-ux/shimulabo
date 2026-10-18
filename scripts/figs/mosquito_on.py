"""モスキート音テスト（mosquito-on）の図。周波数と判定はページの JS と同じ：
FR＝8,10,12,14,15,16,17,18,19,20kHz（低い順に1回2秒）、「聞こえない」で終了し、最後に「聞こえた」音で AGEMAP の目安を出す。"""
from figlib import *

FR = [8000, 10000, 12000, 14000, 15000, 16000, 17000, 18000, 19000, 20000]
AGEMAP = ["60歳以上", "50代", "40代後半", "40代", "30代", "20代後半", "24歳以下", "24歳以下", "10代並み", "10代並み"]


def fig1():
    assert len(FR) == len(AGEMAP)
    b = []
    # 左：テストのしかた・耳と高い音・注意
    b.append(rect(48, 104, 500, 236, CARD, LINE, 12))
    b.append(text(70, 138, "このページのテストのしかた", 18, INK, 700))
    steps = [["8kHz から始めて、10→12→14→15→16", "→17→18→19→20kHz と高くしていく（1回2秒）"],
             ["聞こえたら「聞こえた」で次の音へ。", "聞こえなければ、そこで終わり"],
             ["最後に「聞こえた」音の高さで、", "聴力年齢の目安を出す（右の表）"]]
    for i, rows in enumerate(steps):
        y = 176 + i * 56
        b.append(badge(84, y - 6, str(i + 1), TEAL, "#fff", 15) + lines(106, y, rows, 15.5, INK, 1.4))
    b.append(rect(48, 354, 500, 104, TEAL_L, TEAL_L, 12))
    b.append(text(70, 386, "人の耳と高い音", 18, TEAL_D, 700))
    b.append(lines(70, 416, ["人が聞こえる音の高さは およそ20Hz〜20kHz。", "年齢とともに、高い音の側から聞こえにくくなる。"], 15.5, INK, 1.45))
    b.append(rect(48, 472, 500, 144, ACC_L, ACC, 12, 1.4))
    b.append(text(70, 504, "※ 医療の診断ではありません", 18, ACC, 700))
    b.append(lines(70, 534, ["あくまで簡易的な目安。聞こえに不安があるときは", "耳鼻咽喉科を受診する。音量は小さめから始める。",
                             "スピーカーは高い音が出にくいので、イヤホン推奨。"], 15.5, INK, 1.45))
    # 右：聞こえた最高の音と目安
    x0, kx, bx, bw = 590, 668, 680, 270
    b.append(text(x0, 126, "聞こえた最高の音 → 聴力年齢の目安", 18, INK, 700))
    rh = 44; y0 = 146
    for i, (f, age) in enumerate(reversed(list(zip(FR, AGEMAP)))):
        y = y0 + i * rh
        k = f / 1000
        if i % 2 == 0: b.append(f'<rect x="{x0}" y="{y}" width="{1152 - x0}" height="{rh}" fill="#f2efe7"/>')
        b.append(text(kx, y + rh / 2 + 6, f"{k:g} kHz", 17, INK, 700, "end"))
        w = k / 20 * bw
        b.append(f'<rect x="{bx}" y="{y + 11}" width="{w:.1f}" height="{rh - 22}" rx="3" fill="{TEAL}"/>')
        b.append(text(bx + bw + 18, y + rh / 2 + 7, age, 19, INK, 700))
    b.append(line(bx, y0, bx, y0 + rh * len(FR), INK2, 1.4))
    b.append(text(bx + bw, y0 + rh * len(FR) + 22, "棒の長さ＝音の高さ（0〜20kHz）", 14, MUTED, anchor="end"))
    return svg("".join(b), "モスキート音：聞こえた最高の音と聴力年齢の目安",
               "このシミュの判定表（簡易な目安）。聞こえ方はイヤホン・音量・まわりの音でも変わる。医療の診断ではない。")


FIGS = [
    dict(svg=fig1, alt="モスキート音テストで聞こえた最高の音の高さと聴力年齢の目安の早見表。20・19kHzは10代並み、18・17kHzは24歳以下、16kHzは20代後半、15kHzは30代、14kHzは40代、12kHzは40代後半、10kHzは50代、8kHzは60歳以上。テストのしかたと「医療の診断ではない目安」という注意も示している。",
         caption="聞こえた最高の音と聴力年齢の目安（このシミュの判定）。医療の診断ではなく、簡易的な目安。"),
]
