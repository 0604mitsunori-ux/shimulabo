# -*- coding: utf-8 -*-
"""index.html へ 妊活3本(ninkatsu)＋結婚式3本(wedding)のカード＋ランキング＋本数(562→568)を挿入（冪等）。"""
import os, io, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')

GRAD = {'ninkatsu':'linear-gradient(135deg,#fff1f2,#fce7f3)', 'wedding':'linear-gradient(135deg,#fff1f2,#fdf2f8)'}
LABEL = {'ninkatsu':'妊娠・出産・妊活', 'wedding':'結婚式・ブライダル'}
DATA = [
  ('sankyu-ikukyu','ninkatsu','🗓️'),('jintsuu-kankaku','ninkatsu','⏱️'),('shussan-hiyou','ninkatsu','💰'),
  ('yubiwa-yosan','wedding','💍'),('nijikai-kaihi','wedding','🥂'),('honeymoon-hiyou','wedding','✈️'),
]
CARD = {
  'sankyu-ikukyu':('産休・育休の期間計算機','産休はいつから？育休いつまで？'),
  'jintsuu-kankaku':('陣痛間隔タイマー','タップで間隔を計測・病院連絡の目安'),
  'shussan-hiyou':('出産費用シミュレーター','一時金を引いた自己負担はいくら？'),
  'yubiwa-yosan':('結婚指輪・婚約指輪の予算','相場とお給料からの目安'),
  'nijikai-kaihi':('二次会の会費シミュレーター','赤字にならない会費はいくら？'),
  'honeymoon-hiyou':('ハネムーン費用シミュレーター','行き先・日数から新婚旅行の予算'),
}
SCORE = {'sankyu-ikukyu':72,'jintsuu-kankaku':70,'shussan-hiyou':69,'yubiwa-yosan':72,'nijikai-kaihi':67,'honeymoon-hiyou':65}

with io.open(IDX, encoding='utf-8') as f: html = f.read()
assert 'sims/sankyu-ikukyu/index.html' not in html, '既に挿入済み（中止）'

cards=[]
for sid,slug,emoji in DATA:
    h3,desc=CARD[sid]
    cards.append(f'''    <a class="sim-card" data-cat="{slug}" href="sims/{sid}/index.html">
      <div class="thumb" style="background:{GRAD[slug]}"><span class="emoji">{emoji}</span></div>
      <div class="body"><div class="cat">{LABEL[slug]}</div><h3>{h3}</h3><p>{desc}</p><span class="go">触ってみる →</span></div>
    </a>
''')
marker='    <a class="req-card" href="request/index.html">'
assert marker in html
html=html.replace(marker, ('\n'.join(cards)+'\n')+marker, 1)

rank=[]
for sid,slug,emoji in DATA:
    h3,_=CARD[sid]
    rank.append(f"    {{ href: 'sims/{sid}/index.html', emoji: '{emoji}', title: '{h3}', cat: '{LABEL[slug]}', score: {SCORE[sid]} }}")
idx=html.index('\n  ];')
before=html[:idx].rstrip()
if not before.endswith(','): before+=','
html=before+'\n'+',\n'.join(rank)+html[idx:]

assert '<b>562</b>本 公開中' in html
html=html.replace('<b>562</b>本 公開中','<b>568</b>本 公開中',1)
with io.open(IDX,'w',encoding='utf-8') as f: f.write(html)
print(f'patched index.html: +{len(DATA)} cards, +{len(DATA)} ranking, count=568')
