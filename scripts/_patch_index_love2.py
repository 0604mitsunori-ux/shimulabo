# -*- coding: utf-8 -*-
"""index.html へ 占い5本(uranai)＋マッチング10本(match)のカード＋ランキング＋本数(464→479)を挿入（冪等）。"""
import os, io, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_sims_uranai2, gen_sims_match
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')

GRAD = {'uranai':'linear-gradient(135deg,#f5f3ff,#ede9fe)', 'match':'linear-gradient(135deg,#fff1f2,#ffe4e6)'}
LABEL = {'uranai':'占い・診断', 'match':'マッチング・恋活'}

CARD = {
  'twinray':('ツインレイ診断','あなたの魂の片割れのサインは？'),
  'unmei-hito':('運命の人占い','運命の人はどんな人？いつ出会う？'),
  'aite-kimochi':('相手の気持ち占い','あの人は今あなたをどう思ってる？'),
  'shugorei':('守護霊診断','あなたを守る守護霊はどんな存在？'),
  'deai-uranai':('出会い占い','次の素敵な出会いはいつ？どこで？'),
  'renai-shindan':('恋愛診断','あなたの恋愛傾向タイプは？'),
  'renai-type':('恋愛タイプ診断','肉食？草食？あなたの恋のスタンス。'),
  'renai-hensachi':('恋愛偏差値診断','あなたの恋愛偏差値は？数値で判定。'),
  'mote-do':('モテ度診断','あなたのモテ度は何％？'),
  'risou-aite':('理想の相手診断','あなたに合うパートナーは？'),
  'renai-kachikan':('恋愛価値観診断','恋で大切にするものは？'),
  'kakehiki-type':('恋の駆け引きタイプ診断','追う派？追われる派？'),
  'matchapp-aisho':('マッチングアプリ相性診断','合う使い方・相手タイプは？'),
  'kekkon-tekireiki':('結婚適齢期診断','あなたの結婚への準備度は？'),
  'koibito-itsu':('恋人ができるまで診断','次に恋人ができるのはいつ？'),
}
SCORE = {'twinray':70,'aite-kimochi':71,'unmei-hito':69,'deai-uranai':67,'shugorei':64,
  'renai-shindan':72,'renai-type':70,'renai-hensachi':68,'mote-do':69,'risou-aite':66,
  'renai-kachikan':64,'kakehiki-type':65,'matchapp-aisho':67,'kekkon-tekireiki':66,'koibito-itsu':65}

DATA=[]
for s in gen_sims_uranai2.SIMS: DATA.append((s['id'],'uranai',s['emoji']))
for s in gen_sims_match.SIMS: DATA.append((s['id'],'match',s['emoji']))

with io.open(IDX, encoding='utf-8') as f: html = f.read()
assert 'sims/twinray/index.html' not in html, '既に挿入済み（中止）'

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

assert '<b>464</b>本 公開中' in html
html=html.replace('<b>464</b>本 公開中','<b>479</b>本 公開中',1)
with io.open(IDX,'w',encoding='utf-8') as f: f.write(html)
print(f'patched index.html: +{len(DATA)} cards, +{len(DATA)} ranking, count=479')
