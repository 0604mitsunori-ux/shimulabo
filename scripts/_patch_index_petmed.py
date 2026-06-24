# -*- coding: utf-8 -*-
"""index.html へ ペット予防薬費用シミュ1本のカード＋ランキング＋本数(446→447)を挿入（冪等）。"""
import os, io
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')
GRAD = 'linear-gradient(135deg,#ecfdf5,#d1fae5)'
DATA = [('pet-yobou-hiyou','🐾','ペット予防薬の年間費用','犬・猫のフィラリア・ノミダニ予防はいくら？費用の目安を計算。',60)]

with io.open(IDX, encoding='utf-8') as f:
    html = f.read()
assert 'sims/pet-yobou-hiyou/index.html' not in html, '既に挿入済み（中止）'

cards=[]
for sid,emoji,h3,desc,score in DATA:
    cards.append(f'''    <a class="sim-card" data-cat="pet" href="sims/{sid}/index.html">
      <div class="thumb" style="background:{GRAD}"><span class="emoji">{emoji}</span></div>
      <div class="body"><div class="cat">ペット</div><h3>{h3}</h3><p>{desc}</p><span class="go">触ってみる →</span></div>
    </a>
''')
marker='    <a class="req-card" href="request/index.html">'
assert marker in html
html=html.replace(marker, ('\n'.join(cards)+'\n')+marker, 1)

rank=[]
for sid,emoji,h3,desc,score in DATA:
    rank.append(f"    {{ href: 'sims/{sid}/index.html', emoji: '{emoji}', title: '{h3}', cat: 'ペット', score: {score} }}")
idx=html.index('\n  ];')
before=html[:idx].rstrip()
if not before.endswith(','): before+=','
html=before+'\n'+',\n'.join(rank)+html[idx:]

assert '<b>446</b>本 公開中' in html
html=html.replace('<b>446</b>本 公開中','<b>447</b>本 公開中',1)
with io.open(IDX,'w',encoding='utf-8') as f: f.write(html)
print('patched index.html: +1 card, +1 ranking, count=447')
