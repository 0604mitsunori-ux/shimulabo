# -*- coding: utf-8 -*-
"""index.html へ 便利ツール10(tool)＋脳トレ10(brain)＋テスト10(brain)のカード＋ランキング＋本数(519→549)を挿入（冪等）。"""
import os, io, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_sims_tool3, gen_sims_brain3, gen_sims_test3
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')

GRAD = {'tool':'linear-gradient(135deg,#eff6ff,#e0f2fe)', 'brain':'linear-gradient(135deg,#f0fdfa,#ccfbf1)'}
LABEL = {'tool':'便利ツール', 'brain':'脳トレ・診断テスト'}
CARD = {
  'zeikomi-keisan':('消費税計算機','税込・税抜・消費税額をすぐ計算'),
  'waribiki-keisan':('割引計算機','○％OFF・二重割引の価格を計算'),
  'hensachi-keisan':('偏差値計算機','点数・平均・標準偏差から偏差値'),
  'hiritsu-keisan':('比率計算機','A:B＝C:X の X をすぐ計算'),
  'nenrei-keisan':('年齢計算機','満年齢・数え年・干支を計算'),
  'roma-suji':('ローマ数字変換','数字⇔ローマ数字を相互変換'),
  'hyojun-hensa':('標準偏差計算機','平均・分散・標準偏差を計算'),
  'taiseki-keisan':('体積計算機','立方体・円柱・球などの体積'),
  'yakubun-keisan':('約分計算機','分数を約分・帯分数・小数に'),
  'junretsu-keisan':('順列・組み合わせ計算','nPr・nCr・階乗をすぐ計算'),
  'machigai-sagashi':('間違い探しゲーム','60秒で違う絵文字を何問見つける？'),
  'shinkei-suijaku':('神経衰弱ゲーム','1人で遊べる記憶力ゲーム'),
  'shunkan-kioku':('瞬間記憶テスト','一瞬の数字を何桁覚えられる？'),
  'simon-game':('順番記憶ゲーム','光る順番を覚えて再現（サイモン）'),
  'gyakushou-kioku':('逆唱テスト','数字を逆から言えるか？'),
  'mental-rotation':('図形回転テスト','同じ向き？それとも鏡文字？'),
  'nakama-hazure':('仲間はずれ探しクイズ','1つだけ違うものはどれ？'),
  'ichi-kioku':('位置記憶テスト','光ったマスの場所を覚えて再現'),
  'tango-kioku':('単語記憶テスト','いくつ覚えられる？記憶力チェック'),
  'schulte':('数字探し（シュルテ）','1〜25を順に速くタップ'),
  'mosquito-on':('モスキート音テスト','何歳まで聞こえる？聴力年齢チェック'),
  'hansha-shinkei':('反射神経テスト','緑になった瞬間にタップ！反応速度'),
  'click-cps':('クリック連打速度（CPS）','10秒で何回クリックできる？'),
  'shiryoku-test':('視力テスト','ランドルト環の切れ目はどっち？'),
  'shikikaku-test':('色の識別テスト','1つだけ違う色を探せ'),
  'iq-test':('IQテスト（簡易版）','10問で論理思考力をチェック'),
  'typing-sokudo':('タイピング速度テスト','CPM・正確性を測定'),
  'rhythm-test':('リズム感テスト','ビートに合わせてタップ'),
  'mato-tap':('的当て反応テスト','30秒で何個タップできる？'),
  'gonogo-test':('集中力テスト（Go/No-Go）','青はタップ・赤は我慢！'),
}
SCORE = {
  'zeikomi-keisan':74,'waribiki-keisan':70,'hensachi-keisan':72,'hiritsu-keisan':70,'nenrei-keisan':69,
  'roma-suji':67,'hyojun-hensa':65,'taiseki-keisan':64,'yakubun-keisan':63,'junretsu-keisan':62,
  'machigai-sagashi':73,'shinkei-suijaku':70,'shunkan-kioku':66,'simon-game':65,'gyakushou-kioku':64,
  'mental-rotation':64,'nakama-hazure':66,'ichi-kioku':63,'tango-kioku':63,'schulte':68,
  'mosquito-on':73,'hansha-shinkei':70,'click-cps':69,'shiryoku-test':71,'shikikaku-test':65,
  'iq-test':72,'typing-sokudo':67,'rhythm-test':64,'mato-tap':66,'gonogo-test':64,
}

DATA=[]
for s in gen_sims_tool3.SIMS: DATA.append((s['id'],'tool',s['emoji']))
for s in gen_sims_brain3.SIMS: DATA.append((s['id'],'brain',s['emoji']))
for s in gen_sims_test3.SIMS: DATA.append((s['id'],'brain',s['emoji']))

with io.open(IDX, encoding='utf-8') as f: html = f.read()
assert 'sims/zeikomi-keisan/index.html' not in html, '既に挿入済み（中止）'

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

assert '<b>519</b>本 公開中' in html
html=html.replace('<b>519</b>本 公開中','<b>549</b>本 公開中',1)
with io.open(IDX,'w',encoding='utf-8') as f: f.write(html)
print(f'patched index.html: +{len(DATA)} cards, +{len(DATA)} ranking, count=549')
