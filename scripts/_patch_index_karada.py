# -*- coding: utf-8 -*-
"""index.html へ 健康/運動/美容/妊活/ペット/育児/ツール/受験/住居/車 計20本のカード＋ランキング＋本数(549→569)を挿入（冪等）。"""
import os, io, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_sims_karada, gen_sims_ninkatsu, gen_sims_petkids, gen_sims_keisan2
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')

# 各simのslug（カード data-cat とランキングcatラベル用）
SLUG = {
  'ketsuatsu-check':'health','taishibo-keisan':'health','ranning-calorie':'sports','saidai-shinpaku':'sports','biyo-taiju':'beauty',
  'hairan-keisan':'ninkatsu','ninshin-shusu':'ninkatsu','seiri-cycle':'ninkatsu','kiso-taion':'ninkatsu',
  'inu-nenrei':'pet','neko-nenrei':'pet','kodomo-shincho':'kids','kodomo-himan':'kids',
  'root-keisan':'tool','nijihoteishiki':'tool','en-menseki':'tool','naishinten':'juken',
  'hikkoshi-hiyou':'home','shoki-hiyou':'home','jidoshazei':'car',
}
GRAD = {'health':'linear-gradient(135deg,#fff1f2,#ffe4e6)','sports':'linear-gradient(135deg,#ecfeff,#cffafe)','beauty':'linear-gradient(135deg,#fdf2f8,#fce7f3)',
  'ninkatsu':'linear-gradient(135deg,#fff1f2,#fce7f3)','pet':'linear-gradient(135deg,#fefce8,#fef9c3)','kids':'linear-gradient(135deg,#eff6ff,#dbeafe)',
  'tool':'linear-gradient(135deg,#eff6ff,#e0f2fe)','juken':'linear-gradient(135deg,#f5f3ff,#ede9fe)','home':'linear-gradient(135deg,#f0fdf4,#dcfce7)','car':'linear-gradient(135deg,#f1f5f9,#e2e8f0)'}
LABEL = {'health':'健康・カラダ','sports':'スポーツ・運動','beauty':'美容・ファッション','ninkatsu':'妊娠・出産・妊活','pet':'ペット','kids':'子ども・育児',
  'tool':'便利ツール','juken':'受験・進学','home':'住まい・暮らし','car':'クルマ・乗り物'}
CARD = {
  'ketsuatsu-check':('血圧の判定チェッカー','上・下の数値であなたの血圧分類は？'),
  'taishibo-keisan':('体脂肪率の推定計算機','身長・体重・年齢から体脂肪率の目安'),
  'ranning-calorie':('ランニング消費カロリー計算','距離・体重から消費カロリー'),
  'saidai-shinpaku':('最大心拍数・心拍ゾーン計算','脂肪燃焼ゾーンは何拍？'),
  'biyo-taiju':('美容体重・モデル体重 計算','身長から理想体重の目安'),
  'hairan-keisan':('排卵日計算機','排卵日・妊娠しやすい時期を予測'),
  'ninshin-shusu':('妊娠週数計算機','今は妊娠何週？出産予定日も'),
  'seiri-cycle':('生理周期計算機','次の生理日・排卵日・今の時期'),
  'kiso-taion':('基礎体温 高温期・低温期 判定','今日は高温相？低温相？'),
  'inu-nenrei':('犬の年齢 人間換算','うちの子は人間で何歳？サイズ別'),
  'neko-nenrei':('猫の年齢 人間換算','うちの猫は人間で何歳？'),
  'kodomo-shincho':('子供の身長予測','両親の身長から将来の身長を予測'),
  'kodomo-himan':('子供の肥満度チェック','カウプ指数・ローレル指数で判定'),
  'root-keisan':('ルート計算機（平方根）','√の値を計算・簡単な形に変形'),
  'nijihoteishiki':('二次方程式の解の計算機','ax²+bx+c=0 を解の公式で'),
  'en-menseki':('円の面積・円周の計算機','半径や直径からすぐ計算'),
  'naishinten':('内申点計算機','9教科の評定から合計・換算'),
  'hikkoshi-hiyou':('引っ越し費用シミュレーター','人数・距離・時期から相場の目安'),
  'shoki-hiyou':('賃貸の初期費用シミュレーター','家賃から契約時の総額を計算'),
  'jidoshazei':('自動車税の早見・計算機','排気量から年間の税額'),
}
SCORE = {
  'ketsuatsu-check':74,'taishibo-keisan':73,'ranning-calorie':70,'saidai-shinpaku':66,'biyo-taiju':70,
  'hairan-keisan':71,'ninshin-shusu':72,'seiri-cycle':70,'kiso-taion':66,
  'inu-nenrei':72,'neko-nenrei':71,'kodomo-shincho':67,'kodomo-himan':66,
  'root-keisan':72,'nijihoteishiki':65,'en-menseki':73,'naishinten':68,
  'hikkoshi-hiyou':69,'shoki-hiyou':70,'jidoshazei':67,
}

DATA=[]
for mod in (gen_sims_karada, gen_sims_ninkatsu, gen_sims_petkids, gen_sims_keisan2):
    for s in mod.SIMS: DATA.append((s['id'], SLUG[s['id']], s['emoji']))

with io.open(IDX, encoding='utf-8') as f: html = f.read()
assert 'sims/ketsuatsu-check/index.html' not in html, '既に挿入済み（中止）'

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

assert '<b>549</b>本 公開中' in html
html=html.replace('<b>549</b>本 公開中','<b>569</b>本 公開中',1)
with io.open(IDX,'w',encoding='utf-8') as f: f.write(html)
print(f'patched index.html: +{len(DATA)} cards, +{len(DATA)} ranking, count=569')
