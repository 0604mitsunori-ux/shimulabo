# -*- coding: utf-8 -*-
"""index.html へ ショーケース5本（ふしぎ・現象）のカード＋ランキング＋本数(763→768)を挿入（1回限り）。"""
import os, io, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')

GRAD = 'linear-gradient(135deg,#eef2ff,#e0e7ff)'
CAT = 'ふしぎ・現象'
NEW = [
    ('galaxy-collision', '🌌', '銀河衝突シミュレーター',     '4,000個の星が重力で踊る。潮汐で伸びる星の尾を数十億年分早送りで。'),
    ('black-hole',       '🕳️', 'ブラックホール 光の曲がり', '光の束がねじ曲がり、巻き付き、吸い込まれる。指で狙って撃てる。'),
    ('element-sandbox',  '🏖️', '粉と水のサンドボックス',     '砂・水・火・草を指で描くと、物理法則で動き出す落下砂の箱庭。'),
    ('shinka-sim',       '🧬', '進化シミュレーター',         '食べて、増えて、突然変異。生き物の「速さ」が勝手に進化していく。'),
    ('hinan-crowd',      '🚪', '群衆避難シミュレーター',     '焦るほど遅くなる？130人の避難タイムを実測して確かめる実験室。'),
]

with io.open(IDX, encoding='utf-8') as f:
    html = f.read()
assert 'sims/galaxy-collision/' not in html, '既に挿入済み（中止）'

cards = []; ranks = []
for i, (sid, emoji, h1, desc) in enumerate(NEW):
    score = 72 - i   # ショーケースなのでランキング上位に
    cards.append(
f'''    <a class="sim-card" data-cat="wonder" href="sims/{sid}/">
      <div class="thumb" style="background:{GRAD}"><span class="emoji">{emoji}</span></div>
      <div class="body"><div class="cat">{CAT}</div><h3>{h1}</h3><p>{desc}</p><span class="go">触ってみる →</span></div>
    </a>
''')
    ranks.append(f"    {{ href: 'sims/{sid}/', emoji: '{emoji}', title: '{h1}', cat: '{CAT}', score: {score} }}")

marker = '    <a class="req-card" href="request/">'
assert marker in html
html = html.replace(marker, '\n'.join(cards) + '\n' + marker, 1)

idx = html.index('\n  ];')
before = html[:idx].rstrip()
if not before.endswith(','): before += ','
html = before + '\n' + ',\n'.join(ranks) + html[idx:]

html = html.replace('<b>763</b>本 公開中', '<b>768</b>本 公開中', 1)

with io.open(IDX, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'patched index.html: +{len(NEW)} cards/ranking, count=768')
