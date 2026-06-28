# -*- coding: utf-8 -*-
"""index.html へ 追加10本のカード＋ランキング＋本数(656)を挿入（1回限り）。"""
import os, io, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')

import gen_sims_seo8
GRAD = {
  '仕事・働き方':'linear-gradient(135deg,#eff6ff,#dbeafe)','店舗・ビジネス':'linear-gradient(135deg,#fff7ed,#ffedd5)',
  'お金・時間':'linear-gradient(135deg,#fff1f2,#ffe4e6)','マネー・保険・不動産':'linear-gradient(135deg,#f0fdf4,#dcfce7)',
  'メンタル・自己分析':'linear-gradient(135deg,#eff6ff,#e0e7ff)','推し活・エンタメ':'linear-gradient(135deg,#faf5ff,#fae8ff)',
  'スポーツ・運動':'linear-gradient(135deg,#ecfdf5,#d1fae5)',
}
SLUG = {
  '仕事・働き方':'work','店舗・ビジネス':'biz','お金・時間':'money','マネー・保険・不動産':'finance',
  'メンタル・自己分析':'mental','推し活・エンタメ':'oshi','スポーツ・運動':'sports',
}

sims = gen_sims_seo8.SIMS
assert len(sims) == 10, len(sims)

with io.open(IDX, encoding='utf-8') as f:
    html = f.read()
assert 'sims/kyuryo-tedori/index.html' not in html, '既に挿入済み（中止）'

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

html = html.replace('<b>646</b>本 公開中', '<b>656</b>本 公開中', 1)

with io.open(IDX, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'patched index.html: +{len(sims)} cards/ranking, count=656')
