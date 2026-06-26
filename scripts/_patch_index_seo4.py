# -*- coding: utf-8 -*-
"""index.html へ SEO新規3本（厄年/失業保険/借入可能額）のカード＋ランキング＋本数(571)を挿入（1回限り）。"""
import os, io, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')

import gen_sims_seo4
GRAD = {
  '冠婚葬祭・贈り物': 'linear-gradient(135deg,#fdf4ff,#fae8ff)',
  '仕事・働き方': 'linear-gradient(135deg,#eff6ff,#dbeafe)',
  'マネー・保険・不動産': 'linear-gradient(135deg,#f0fdf4,#dcfce7)',
}
SLUG = {'冠婚葬祭・贈り物': 'manner', '仕事・働き方': 'work', 'マネー・保険・不動産': 'finance'}

sims = gen_sims_seo4.SIMS
assert len(sims) == 3, len(sims)

with io.open(IDX, encoding='utf-8') as f:
    html = f.read()
assert 'sims/yakudoshi/index.html' not in html, '既に挿入済み（中止）'

cards = []; ranks = []
for s in sims:
    cat = s['cat']; slug = SLUG[cat]; grad = GRAD[cat]
    desc = s.get('ogdesc', s.get('desc', ''))[:46]
    score = 62  # 新着は上位
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

html = html.replace('<b>568</b>本 公開中', '<b>571</b>本 公開中', 1)

with io.open(IDX, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'patched index.html: +{len(sims)} cards/ranking, count=571')
