# -*- coding: utf-8 -*-
"""index.html へ 全カテゴリ3本ずつ補充 計66本のカード＋ランキング＋本数(301)を一括挿入（1回限り）。"""
import os, io, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')

SLUG = {'お金・時間':'money','ふしぎ・現象':'wonder','人生・自分ごと':'life','マーケティング':'marketing',
 '恋愛・婚活':'love','店舗・ビジネス':'biz','マネー・保険・不動産':'finance','仕事・働き方':'work',
 '学生・勉強':'study','子ども・育児':'kids','ペット':'pet','健康・カラダ':'health','占い・診断':'uranai',
 'クルマ・乗り物':'car','旅行・おでかけ':'travel','住まい・暮らし':'home','グルメ・食':'food',
 'あそぶ・実験':'play','美容・ファッション':'beauty','スポーツ・運動':'sports','推し活・エンタメ':'oshi','メンタル・自己分析':'mental'}
GRAD = {'money':'linear-gradient(135deg,#fff1f2,#ffe4e6)','wonder':'linear-gradient(135deg,#eef2ff,#e0e7ff)',
 'life':'linear-gradient(135deg,#ecfeff,#cffafe)','marketing':'linear-gradient(135deg,#fff7ed,#fce7f3)',
 'love':'linear-gradient(135deg,#fff1f2,#ffe4e6)','biz':'linear-gradient(135deg,#fff7ed,#ffedd5)',
 'finance':'linear-gradient(135deg,#ecfdf5,#d1fae5)','work':'linear-gradient(135deg,#eff6ff,#dbeafe)',
 'study':'linear-gradient(135deg,#f5f3ff,#ede9fe)','kids':'linear-gradient(135deg,#fffbeb,#fef3c7)',
 'pet':'linear-gradient(135deg,#ecfdf5,#d1fae5)','health':'linear-gradient(135deg,#fef2f2,#fee2e2)',
 'uranai':'linear-gradient(135deg,#faf5ff,#f3e8ff)','car':'linear-gradient(135deg,#eff6ff,#e0e7ff)',
 'travel':'linear-gradient(135deg,#cffafe,#a5f3fc)','home':'linear-gradient(135deg,#ecfdf5,#d1fae5)',
 'food':'linear-gradient(135deg,#fff7ed,#ffe4e6)','play':'linear-gradient(135deg,#ecfeff,#ede9fe)',
 'beauty':'linear-gradient(135deg,#fff1f2,#fce7f3)','sports':'linear-gradient(135deg,#ecfdf5,#d1fae5)',
 'oshi':'linear-gradient(135deg,#faf5ff,#fae8ff)','mental':'linear-gradient(135deg,#eff6ff,#e0e7ff)'}

sims=[]
for m in ('gen_sims22','gen_sims23','gen_sims24','gen_sims25','gen_sims26'):
    mod=__import__(m)
    for s in mod.SIMS:
        sims.append(s)
assert len(sims)==66, len(sims)

with io.open(IDX, encoding='utf-8') as f:
    html=f.read()
assert 'sims/point-katsu/index.html' not in html, '既に挿入済み（中止）'

cards=[]; ranks=[]
for i,s in enumerate(sims):
    slug=SLUG[s['cat']]; grad=GRAD[slug]; emoji=s['emoji']; h3=s['h1']
    desc=s.get('ogdesc', s.get('desc',''))[:46]
    score=58-(i%10)
    cards.append(
f'''    <a class="sim-card" data-cat="{slug}" href="sims/{s['id']}/index.html">
      <div class="thumb" style="background:{grad}"><span class="emoji">{emoji}</span></div>
      <div class="body"><div class="cat">{s['cat']}</div><h3>{h3}</h3><p>{desc}</p><span class="go">触ってみる →</span></div>
    </a>
''')
    ranks.append(f"    {{ href: 'sims/{s['id']}/index.html', emoji: '{emoji}', title: '{h3}', cat: '{s['cat']}', score: {score} }}")

marker='    <a class="req-card" href="request/index.html">'
assert marker in html
html=html.replace(marker, '\n'.join(cards)+'\n'+marker, 1)

idx=html.index('\n  ];')
before=html[:idx].rstrip()
if not before.endswith(','): before+=','
html=before+'\n'+',\n'.join(ranks)+html[idx:]

html=html.replace('<b>235</b>本 公開中','<b>301</b>本 公開中',1)

with io.open(IDX,'w',encoding='utf-8') as f: f.write(html)
print(f'patched index.html: +{len(sims)} cards/ranking, count=301')
