# -*- coding: utf-8 -*-
"""index.html へ Webマーケ計算10＋LLMO診断1のカード＋ランキング＋本数(447→458)を挿入（冪等）。
既存カテゴリ marketing に追加。"""
import os, io, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_sims_webmkt
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')
GRAD = 'linear-gradient(135deg,#fff7ed,#fce7f3)'  # 既存マーケと同系
LABEL = 'マーケティング'

CARD = {
  'cvr-keisan':('コンバージョン率(CVR)計算機','CV数とアクセスからCVRを一発計算。',69),
  'cpa-keisan':('CPA計算機','広告費とCV数から顧客獲得単価を計算。',66),
  'cpc-keisan':('CPC計算機','広告費とクリック数からクリック単価を計算。',64),
  'cpm-keisan':('CPM計算機','広告費と表示回数から1000回表示単価を計算。',63),
  'churn-keisan':('解約率(チャーンレート)計算機','継続率・平均継続月数も。サブスクに。',68),
  'kyakutanka-keisan':('客単価計算機','売上と客数から客単価を計算（目標逆算も）。',67),
  'listing-hiyou':('リスティング広告 費用シミュ','月額予算とCV数・CPAの目安を試算。',70),
  'funnel-cv':('集客ファネル試算','アクセス→CV→売上とCVR改善の効果。',65),
  'meo-raiten':('MEO来店効果シミュ','地図検索からの来店数を試算。',66),
  'kokoku-yosan':('広告予算シミュレーター','予算からCV・売上・ROASを試算。',68),
  'llmo-check':('店舗のLLMO対応度診断','AIに選ばれる店か8問でチェック。',72),
}
DATA = [(s['id'], s['emoji'], CARD[s['id']][0], CARD[s['id']][1], CARD[s['id']][2]) for s in gen_sims_webmkt.SIMS]

with io.open(IDX, encoding='utf-8') as f:
    html = f.read()
assert 'sims/cvr-keisan/index.html' not in html, '既に挿入済み（中止）'

cards=[]
for sid,emoji,h3,desc,score in DATA:
    cards.append(f'''    <a class="sim-card" data-cat="marketing" href="sims/{sid}/index.html">
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

assert '<b>447</b>本 公開中' in html
html=html.replace('<b>447</b>本 公開中','<b>458</b>本 公開中',1)
with io.open(IDX,'w',encoding='utf-8') as f: f.write(html)
print(f'patched index.html: +{len(DATA)} cards, +{len(DATA)} ranking, count=458')
