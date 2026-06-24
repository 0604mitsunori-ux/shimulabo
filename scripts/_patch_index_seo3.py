# -*- coding: utf-8 -*-
"""index.html へ SEO新規3本（年齢計算/出産予定日/割引計算機）のカード＋ランキング＋本数(376)を挿入（1回限り）。"""
import os, io, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')

import gen_sims_seo3
GRAD = {
  '人生・自分ごと': 'linear-gradient(135deg,#ecfeff,#cffafe)',
  '子ども・育児': 'linear-gradient(135deg,#fff7ed,#ffedd5)',
  'お金・時間': 'linear-gradient(135deg,#fff1f2,#ffe4e6)',
}
SLUG = {'人生・自分ごと': 'life', '子ども・育児': 'kids', 'お金・時間': 'money'}

sims = gen_sims_seo3.SIMS
assert len(sims) == 3, len(sims)

with io.open(IDX, encoding='utf-8') as f:
    html = f.read()
assert 'sims/nenrei-keisan/index.html' not in html, '既に挿入済み（中止）'

cards = []; ranks = []
for s in sims:
    cat = s['cat']; slug = SLUG[cat]; grad = GRAD[cat]
    desc = s.get('ogdesc', s.get('desc', ''))[:46]
    score = 61  # 新着は上位に
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

html = html.replace('<b>373</b>本 公開中', '<b>376</b>本 公開中', 1)

with io.open(IDX, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'patched index.html: +{len(sims)} cards/ranking, count=376')
