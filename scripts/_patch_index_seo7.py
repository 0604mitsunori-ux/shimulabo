# -*- coding: utf-8 -*-
"""index.html へ 診断15本（メンタル/恋愛/美容 各5）のカード＋ランキング＋本数(646)を挿入（1回限り）。"""
import os, io, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')

import gen_sims_seo7
GRAD = {
  'メンタル・自己分析':'linear-gradient(135deg,#eff6ff,#e0e7ff)',
  '恋愛・婚活':'linear-gradient(135deg,#ecfeff,#cffafe)',
  '美容・ファッション':'linear-gradient(135deg,#fff1f2,#fce7f3)',
}
SLUG = {'メンタル・自己分析':'mental','恋愛・婚活':'love','美容・ファッション':'beauty'}

sims = gen_sims_seo7.SIMS
assert len(sims) == 15, len(sims)

with io.open(IDX, encoding='utf-8') as f:
    html = f.read()
assert 'sims/kanpeki-shugi/index.html' not in html, '既に挿入済み（中止）'

cards = []; ranks = []
for i, s in enumerate(sims):
    cat = s['cat']; slug = SLUG[cat]; grad = GRAD[cat]
    desc = s.get('ogdesc', s.get('desc', ''))[:46]
    score = 62 - (i % 6)
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

html = html.replace('<b>631</b>本 公開中', '<b>646</b>本 公開中', 1)

with io.open(IDX, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'patched index.html: +{len(sims)} cards/ranking, count=646')
