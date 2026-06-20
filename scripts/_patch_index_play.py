# -*- coding: utf-8 -*-
"""index.html へ あそぶ・実験 15本のカード＋ランキング＋本数(195)を一括挿入（1回限り）。"""
import os, io
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')

GRAD = 'linear-gradient(135deg,#ecfeff,#ede9fe)'
LABEL = 'あそぶ・実験'

# (id, emoji, h3, desc, score)
DATA = [
 ('lorenz','🦋','ローレンツ・アトラクタ','カオスの蝶を回転描画。ずっと見られる。',74),
 ('pendulum-wave','🎐','振り子の波','波→らせん→整列をくり返す催眠演出。',72),
 ('solar-system','🪐','太陽系シミュレーター','8惑星がそれぞれの速さで公転。',70),
 ('gravity','🌌','重力シミュレーター','クリックで星を放つと軌道が生まれる。',73),
 ('fireworks','🎆','花火シミュレーター','タップで打ち上がる花火。音は出ない。',71),
 ('fractal-tree','🌳','フラクタルの木','角度を変えて自分だけの木を育てる。',66),
 ('mandelbrot','🌀','マンデルブロ集合','クリックでどこまでもズーム。無限の模様。',69),
 ('starfield','🌟','ワープ星空','星の中を飛ぶ。スピードで光の筋に。',65),
 ('gears','⚙️','歯車シミュレーター','歯数を変えて回転比を体感。',60),
 ('dna','🧬','DNA二重らせん','くるくる回る生命の設計図。',64),
 ('reaction-test','⚡','反応速度テスト','緑になった瞬間にクリック。何ミリ秒？',68),
 ('typing-test','⌨️','タイピング速度測定','何打/分？正確率も判定。',63),
 ('memory-test','🧠','記憶力テスト','光る順番を何個まで覚えられる？',67),
 ('spirograph','✏️','スピログラフ','歯車で描く無限の幾何学模様。',62),
 ('ripple','🌊','波紋シミュレーター','水面をタップ。波の干渉が見える。',61),
]

with io.open(IDX, encoding='utf-8') as f:
    html = f.read()

assert 'sims/lorenz/index.html' not in html, '既に挿入済みのようです（中止）'

cards = []
for sid, emoji, h3, desc, score in DATA:
    cards.append(
f'''    <a class="sim-card" data-cat="play" href="sims/{sid}/index.html">
      <div class="thumb" style="background:{GRAD}"><span class="emoji">{emoji}</span></div>
      <div class="body"><div class="cat">{LABEL}</div><h3>{h3}</h3><p>{desc}</p><span class="go">触ってみる →</span></div>
    </a>
''')
cards_block = '\n'.join(cards) + '\n'
marker = '    <a class="req-card" href="request/index.html">'
assert marker in html
html = html.replace(marker, cards_block + marker, 1)

rank = []
for sid, emoji, h3, desc, score in DATA:
    rank.append(f"    {{ href: 'sims/{sid}/index.html', emoji: '{emoji}', title: '{h3}', cat: '{LABEL}', score: {score} }}")
idx = html.index('\n  ];')
before = html[:idx].rstrip()
if not before.endswith(','):
    before += ','
html = before + '\n' + ',\n'.join(rank) + html[idx:]

html = html.replace('<b>180</b>本 公開中', '<b>195</b>本 公開中', 1)

with io.open(IDX, 'w', encoding='utf-8') as f:
    f.write(html)
print('patched index.html: +15 cards, +15 ranking, count=195')
