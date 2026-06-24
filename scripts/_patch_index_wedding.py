# -*- coding: utf-8 -*-
"""index.html へ 結婚式・ブライダル6本のカード＋ランキング＋本数(458→464)を挿入（冪等）。"""
import os, io, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_sims_wedding
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')
GRAD = 'linear-gradient(135deg,#fff1f2,#fdf2f8)'
LABEL = '結婚式・ブライダル'

CARD = {
  'wedding-style':('結婚式スタイル診断','ふたりに合う挙式は？教会式・神前式・人前式。',71),
  'venue-type':('結婚式場タイプ診断','ホテル・専門式場・ゲストハウス・レストラン。',70),
  'enshutsu-type':('結婚式の演出タイプ診断','感動派？盛り上げ派？ふたりに合う演出。',68),
  'wedding-theme':('結婚式テーマ診断','ナチュラル？エレガント？ふたりのテーマ。',66),
  'kekkon-jikofutan':('結婚式の自己負担額シミュ','ご祝儀を引いた持ち出しはいくら？',69),
  'kekkon-junbi':('結婚式 準備スケジュール診断','いつから始める？間に合う？を診断。',65),
}
DATA = [(s['id'], s['emoji'], CARD[s['id']][0], CARD[s['id']][1], CARD[s['id']][2]) for s in gen_sims_wedding.SIMS]

with io.open(IDX, encoding='utf-8') as f:
    html = f.read()
assert 'sims/wedding-style/index.html' not in html, '既に挿入済み（中止）'

cards=[]
for sid,emoji,h3,desc,score in DATA:
    cards.append(f'''    <a class="sim-card" data-cat="wedding" href="sims/{sid}/index.html">
      <div class="thumb" style="background:{GRAD}"><span class="emoji">{emoji}</span></div>
      <div class="body"><div class="cat">{LABEL}</div><h3>{h3}</h3><p>{desc}</p><span class="go">触ってみる →</span></div>
    </a>
''')
marker='    <a class="req-card" href="request/index.html">'
assert marker in html
html=html.replace(marker, ('\n'.join(cards)+'\n')+marker, 1)

rank=[]
for sid,emoji,h3,desc,score in DATA:
    rank.append(f"    {{ href: 'sims/{sid}/index.html', emoji: '{emoji}', title: '{h3}', cat: '{LABEL}', score: {score} }}")
idx=html.index('\n  ];')
before=html[:idx].rstrip()
if not before.endswith(','): before+=','
html=before+'\n'+',\n'.join(rank)+html[idx:]

assert '<b>458</b>本 公開中' in html
html=html.replace('<b>458</b>本 公開中','<b>464</b>本 公開中',1)
with io.open(IDX,'w',encoding='utf-8') as f: f.write(html)
print(f'patched index.html: +{len(DATA)} cards, +{len(DATA)} ranking, count=464')
