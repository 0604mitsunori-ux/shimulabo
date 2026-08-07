# -*- coding: utf-8 -*-
"""index.html へ SEO流入10本（10カテゴリ分散）のカード＋ランキング＋本数(768→778)を挿入（1回限り）。"""
import os, io, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')

import gen_sims_fable10 as M

# id -> (data-cat slug, gradient)
MAP = {
    'yukyu-fuyo':       ('work',   'linear-gradient(135deg,#eff6ff,#dbeafe)'),
    'bonus-heikin':     ('money',  'linear-gradient(135deg,#fff1f2,#ffe4e6)'),
    'nyuen-nenrei':     ('kids',   'linear-gradient(135deg,#fffbeb,#fef3c7)'),
    'koreisha-itsu':    ('senior', 'linear-gradient(135deg,#ecfdf5,#d1fae5)'),
    'junior-seat':      ('car',    'linear-gradient(135deg,#eff6ff,#e0e7ff)'),
    'dokushin-zei':     ('tax',    'linear-gradient(135deg,#fffbeb,#fef3c7)'),
    'bust-size':        ('beauty', 'linear-gradient(135deg,#fff1f2,#fce7f3)'),
    'myakuhaku-heikin': ('health', 'linear-gradient(135deg,#fef2f2,#fee2e2)'),
    'akuryoku-heikin':  ('sports', 'linear-gradient(135deg,#ecfdf5,#d1fae5)'),
    'arasa-hantei':     ('life',   'linear-gradient(135deg,#fefce8,#fef9c3)'),
}
sims = M.SIMS
assert len(sims) == 10, len(sims)

with io.open(IDX, encoding='utf-8') as f:
    html = f.read()
assert 'sims/yukyu-fuyo/' not in html, '既に挿入済み（中止）'

cards = []; ranks = []
for i, s in enumerate(sims):
    slug, grad = MAP[s['id']]
    cat = s['cat']; desc = s.get('ogdesc', s.get('desc', ''))[:46]
    score = 66 - i
    cards.append(
f'''    <a class="sim-card" data-cat="{slug}" href="sims/{s['id']}/">
      <div class="thumb" style="background:{grad}"><span class="emoji">{s['emoji']}</span></div>
      <div class="body"><div class="cat">{cat}</div><h3>{s['h1']}</h3><p>{desc}</p><span class="go">触ってみる →</span></div>
    </a>
''')
    ranks.append(f"    {{ href: 'sims/{s['id']}/', emoji: '{s['emoji']}', title: '{s['h1']}', cat: '{cat}', score: {score} }}")

marker = '    <a class="req-card" href="request/">'
assert marker in html
html = html.replace(marker, '\n'.join(cards) + '\n' + marker, 1)

idx = html.index('\n  ];')
before = html[:idx].rstrip()
if not before.endswith(','): before += ','
html = before + '\n' + ',\n'.join(ranks) + html[idx:]

html = html.replace('<b>768</b>本 公開中', '<b>778</b>本 公開中', 1)

with io.open(IDX, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'patched index.html: +{len(sims)} cards/ranking, count=778')
