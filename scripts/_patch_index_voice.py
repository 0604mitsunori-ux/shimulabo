# -*- coding: utf-8 -*-
"""index.html へ 音声入力・時短 10本のカード＋ランキング＋本数(373)を一括挿入（1回限り）。"""
import os, io, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')

import gen_sims_voice
GRAD = 'linear-gradient(135deg,#eef2ff,#f5f3ff)'
SLUG = 'voice'

sims = gen_sims_voice.SIMS
assert len(sims) == 10, len(sims)

with io.open(IDX, encoding='utf-8') as f:
    html = f.read()
assert 'sims/input-jitan/index.html' not in html, '既に挿入済み（中止）'

cards = []; ranks = []
for i, s in enumerate(sims):
    cat = s['cat']; desc = s.get('ogdesc', s.get('desc', ''))[:46]
    score = 60 - (i % 10)
    cards.append(
f'''    <a class="sim-card" data-cat="{SLUG}" href="sims/{s['id']}/index.html">
      <div class="thumb" style="background:{GRAD}"><span class="emoji">{s['emoji']}</span></div>
      <div class="body"><div class="cat">{cat}</div><h3>{s['h1']}</h3><p>{desc}</p><span class="go">触ってみる →</span></div>
    </a>
''')
    ranks.append(f"    {{ href: 'sims/{s['id']}/index.html', emoji: '{s['emoji']}', title: '{s['h1']}', cat: '{cat}', score: {score} }}")

marker = '    <a class="req-card" href="request/index.html">'
assert marker in html
html = html.replace(marker, '\n'.join(cards) + '\n' + marker, 1)

idx = html.index('\n  ];')
before = html[:idx].rstrip()
if not before.endswith(','): before += ','
html = before + '\n' + ',\n'.join(ranks) + html[idx:]

with io.open(IDX, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'patched index.html: +{len(sims)} cards/ranking (voice)')
