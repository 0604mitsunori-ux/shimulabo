# -*- coding: utf-8 -*-
"""index.html へ 光熱費10本(hikari)＋冠婚葬祭10本(manner)のカード＋ランキング＋本数(499→519)を挿入（冪等）。"""
import os, io, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_sims_hikari, gen_sims_manner
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')

GRAD = {'hikari':'linear-gradient(135deg,#fffbeb,#fef3c7)', 'manner':'linear-gradient(135deg,#fdf4ff,#fae8ff)'}
LABEL = {'hikari':'光熱費・節約', 'manner':'冠婚葬祭・贈り物'}
CARD = {
  'gasolinedai':('ガソリン代計算機','走行距離・燃費からガソリン代を計算'),
  'aircon-denki':('エアコンの電気代計算','畳数・時間から1日・1ヶ月いくら？'),
  'denkidai-keisan':('電気代計算機','消費電力(W)と時間から計算'),
  'kaden-denki':('家電別 電気代早見','冷蔵庫・ドライヤー等の電気代'),
  'suidoudai':('水道代の平均・目安','世帯人数別に月いくら？'),
  'gasudai':('ガス代の平均・目安','世帯人数・都市/プロパン別'),
  'led-setsuyaku':('LED電球の節約シミュ','白熱から替えるといくら得？'),
  'danbou-hikaku':('暖房の電気代比較','エアコン・こたつ・ストーブどれが安い？'),
  'ev-vs-gasoline':('EV vs ガソリン車 燃料費比較','どっちが安い？'),
  'kounetsuhi-shindan':('光熱費 高すぎ？診断','わが家は平均より高い？'),
  'koden-souba':('香典の相場早見','関係・年代別にいくら包む？'),
  'shukugi-souba':('ご祝儀の相場早見','結婚式でいくら包む？'),
  'otoshidama-souba':('お年玉の相場早見','年齢・学年別にいくら渡す？'),
  'shussan-iwai-souba':('出産祝いの相場早見','関係別にいくら贈る？'),
  'kekkon-iwai-souba':('結婚祝いの相場早見','出席しない場合・品物でいくら？'),
  'uchiiwai-keisan':('内祝い・お返しの金額計算','半返し・三分の一をすぐ計算'),
  'nyugaku-iwai-souba':('入学・卒業祝いの相場早見','関係・学齢別にいくら？'),
  'mochu-checker':('喪中の範囲チェッカー','この続柄は喪中？はがきはいつ？'),
  'kanchu-mimai':('寒中・暑中見舞いの時期','いつ出す？'),
  'chouju-iwai':('長寿祝い早見','還暦・古希・喜寿…何歳が何のお祝い？'),
}
SCORE = {'gasolinedai':72,'aircon-denki':71,'denkidai-keisan':68,'kaden-denki':66,'suidoudai':67,'gasudai':65,
  'led-setsuyaku':64,'danbou-hikaku':66,'ev-vs-gasoline':65,'kounetsuhi-shindan':67,
  'koden-souba':72,'shukugi-souba':71,'otoshidama-souba':69,'shussan-iwai-souba':70,'kekkon-iwai-souba':66,
  'uchiiwai-keisan':65,'nyugaku-iwai-souba':64,'mochu-checker':68,'kanchu-mimai':64,'chouju-iwai':67}

DATA=[]
for s in gen_sims_hikari.SIMS: DATA.append((s['id'],'hikari',s['emoji']))
for s in gen_sims_manner.SIMS: DATA.append((s['id'],'manner',s['emoji']))

with io.open(IDX, encoding='utf-8') as f: html = f.read()
assert 'sims/gasolinedai/index.html' not in html, '既に挿入済み（中止）'

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

assert '<b>499</b>本 公開中' in html
html=html.replace('<b>499</b>本 公開中','<b>519</b>本 公開中',1)
with io.open(IDX,'w',encoding='utf-8') as f: f.write(html)
print(f'patched index.html: +{len(DATA)} cards, +{len(DATA)} ranking, count=519')
