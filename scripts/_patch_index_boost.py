# -*- coding: utf-8 -*-
"""index.html へ 横展開12本（teacher3/uranai3/car3/life3）のカード＋ランキング＋本数(701→713)を挿入（1回限り）。既存カテゴリに追加。"""
import os, io, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')

import gen_sims_boost

# id -> (data-cat slug, gradient)
MAP = {
    'daigaku-shusseki': ('teacher', 'linear-gradient(135deg,#fff7ed,#ffedd5)'),
    'sotsugyo-tani':    ('teacher', 'linear-gradient(135deg,#fff7ed,#ffedd5)'),
    'ryunen-tani':      ('teacher', 'linear-gradient(135deg,#fff7ed,#ffedd5)'),
    'shugo-animal':     ('uranai',  'linear-gradient(135deg,#f5f3ff,#ede9fe)'),
    'shugorei-level':   ('uranai',  'linear-gradient(135deg,#f5f3ff,#ede9fe)'),
    'power-stone':      ('uranai',  'linear-gradient(135deg,#f5f3ff,#ede9fe)'),
    'shinkansen-car':   ('car',     'linear-gradient(135deg,#eff6ff,#e0e7ff)'),
    'teiki-kaisu':      ('car',     'linear-gradient(135deg,#eff6ff,#e0e7ff)'),
    'taxi-densha':      ('car',     'linear-gradient(135deg,#eff6ff,#e0e7ff)'),
    'ojisan-do':        ('life',    'linear-gradient(135deg,#ecfeff,#cffafe)'),
    'obasan-do':        ('life',    'linear-gradient(135deg,#ecfeff,#cffafe)'),
    'wakamono-do':      ('life',    'linear-gradient(135deg,#ecfeff,#cffafe)'),
}
sims = gen_sims_boost.SIMS
assert len(sims) == 12, len(sims)

with io.open(IDX, encoding='utf-8') as f:
    html = f.read()
assert 'sims/daigaku-shusseki/index.html' not in html, '既に挿入済み（中止）'

cards = []; ranks = []
for i, s in enumerate(sims):
    slug, grad = MAP[s['id']]
    cat = s['cat']; desc = s.get('ogdesc', s.get('desc', ''))[:46]
    score = 65 - i
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

html = html.replace('<b>701</b>本 公開中', '<b>713</b>本 公開中', 1)

with io.open(IDX, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'patched index.html: +{len(sims)} cards/ranking, count=713')
