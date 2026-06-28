# -*- coding: utf-8 -*-
"""index.html へ SEO新規30本＋Typeless10本のカード＋ランキング＋本数(631)を挿入（1回限り）。"""
import os, io, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')

import gen_sims_seo6, gen_sims_voice2
GRAD = {
  'マネー・保険・不動産':'linear-gradient(135deg,#f0fdf4,#dcfce7)','お金・時間':'linear-gradient(135deg,#fff1f2,#ffe4e6)',
  '税金・確定申告':'linear-gradient(135deg,#fffbeb,#fef3c7)','仕事・働き方':'linear-gradient(135deg,#eff6ff,#dbeafe)',
  '健康・カラダ':'linear-gradient(135deg,#fef2f2,#fee2e2)','クルマ・乗り物':'linear-gradient(135deg,#eff6ff,#e0e7ff)',
  '人生・自分ごと':'linear-gradient(135deg,#fefce8,#fef9c3)','冠婚葬祭・贈り物':'linear-gradient(135deg,#fdf4ff,#fae8ff)',
  '子ども・育児':'linear-gradient(135deg,#fffbeb,#fef3c7)','シニア・終活・介護':'linear-gradient(135deg,#ecfdf5,#d1fae5)',
  '店舗・ビジネス':'linear-gradient(135deg,#fff7ed,#ffedd5)','メンタル・自己分析':'linear-gradient(135deg,#eff6ff,#e0e7ff)',
  '美容・ファッション':'linear-gradient(135deg,#fff1f2,#fce7f3)','恋愛・婚活':'linear-gradient(135deg,#ecfeff,#cffafe)',
  '学生・勉強':'linear-gradient(135deg,#f5f3ff,#ede9fe)','音声入力・時短':'linear-gradient(135deg,#eef2ff,#f5f3ff)',
}
SLUG = {
  'マネー・保険・不動産':'finance','お金・時間':'money','税金・確定申告':'tax','仕事・働き方':'work',
  '健康・カラダ':'health','クルマ・乗り物':'car','人生・自分ごと':'life','冠婚葬祭・贈り物':'manner',
  '子ども・育児':'kids','シニア・終活・介護':'senior','店舗・ビジネス':'biz','メンタル・自己分析':'mental',
  '美容・ファッション':'beauty','恋愛・婚活':'love','学生・勉強':'study','音声入力・時短':'voice',
}

sims = list(gen_sims_seo6.SIMS) + [dict(s, cat='音声入力・時短') for s in gen_sims_voice2.SIMS]
assert len(sims) == 40, len(sims)

with io.open(IDX, encoding='utf-8') as f:
    html = f.read()
assert 'sims/tdee-keisan/index.html' not in html, '既に挿入済み（中止）'

cards = []; ranks = []
for i, s in enumerate(sims):
    cat = s['cat']; slug = SLUG[cat]; grad = GRAD[cat]
    desc = s.get('ogdesc', s.get('desc', ''))[:46]
    score = 63 - (i % 7)
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

html = html.replace('<b>591</b>本 公開中', '<b>631</b>本 公開中', 1)

with io.open(IDX, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'patched index.html: +{len(sims)} cards/ranking, count=631')
