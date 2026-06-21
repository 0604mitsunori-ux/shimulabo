# -*- coding: utf-8 -*-
"""index.html へ シニア/税金/受験/季節 計40本のカード＋ランキング＋本数(363)を一括挿入（1回限り）。"""
import os, io, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')

import gen_sims27, gen_sims28, gen_sims29, gen_sims30
GRAD = {
  'シニア・終活・介護': 'linear-gradient(135deg,#ecfdf5,#d1fae5)',
  '税金・確定申告': 'linear-gradient(135deg,#fffbeb,#fef3c7)',
  '受験・進学': 'linear-gradient(135deg,#fff1f2,#ffe4e6)',
  '季節・行事': 'linear-gradient(135deg,#fff7ed,#fce7f3)',
}
SLUG = {'シニア・終活・介護': 'senior', '税金・確定申告': 'tax', '受験・進学': 'juken', '季節・行事': 'season'}

sims = []
for m in (gen_sims27, gen_sims28, gen_sims29, gen_sims30):
    sims += m.SIMS
assert len(sims) == 40, len(sims)

with io.open(IDX, encoding='utf-8') as f:
    html = f.read()
assert 'sims/shukatsu-sougaku/index.html' not in html, '既に挿入済み（中止）'

cards = []; ranks = []
for i, s in enumerate(sims):
    cat = s['cat']; slug = SLUG[cat]; grad = GRAD[cat]
    desc = s.get('ogdesc', s.get('desc', ''))[:46]
    score = 58 - (i % 12)
    cards.append(
f'''    <a class="sim-card" data-cat="{slug}" href="sims/{s['id']}/index.html">
      <div class="thumb" style="background:{grad}"><span class="emoji">{s['emoji']}</span></div>
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

html = html.replace('<b>323</b>本 公開中', '<b>363</b>本 公開中', 1)

with io.open(IDX, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'patched index.html: +{len(sims)} cards/ranking, count=363')
