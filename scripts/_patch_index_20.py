# -*- coding: utf-8 -*-
"""index.html へ住まい/グルメ 計20本のカード＋ランキング＋本数(180)を一括挿入（1回限り）。"""
import os, io
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')

GRAD = {
  'home': 'linear-gradient(135deg,#ecfdf5,#d1fae5)',
  'food': 'linear-gradient(135deg,#fff7ed,#ffe4e6)',
}
LABEL = {'home':'住まい・暮らし','food':'グルメ・食'}

# (id, slug, emoji, h3, desc, score)
DATA = [
 ('yachin-tekisei','home','🏠','適正家賃チェック','手取りからいくらの家賃が無理ない？',67),
 ('hikkoshi-hiyou','home','🚚','引っ越し費用','荷物量・距離・時期で費用を試算。',62),
 ('chintai-mochiie','home','🔑','賃貸 vs 持ち家','生涯コストはどっちが得？',64),
 ('denki-setsuyaku','home','💡','電気代 節約','ちょっとの工夫で年いくら浮く？',60),
 ('hitorigurashi','home','📦','ひとり暮らし初期費用','引っ越しに最初いくら必要？',63),
 ('kounetsu','home','🧾','光熱費の平均','うちの光熱費、高い？普通？',58),
 ('net-hikari','home','📶','ネット代見直し','乗り換えで生涯いくら浮く？',56),
 ('kaji-jikan','home','🧹','家事の生涯時間','一生で家事に何日使ってる？',57),
 ('kagu-tsumitate','home','🛋️','家具・家電 買い替え積立','毎月いくら貯めれば慌てない？',54),
 ('tatami-henkan','home','📐','部屋の広さ換算','畳・㎡・坪と坪単価をすぐ計算。',59),
 ('ramen-roudou','food','🍜','ラーメン1杯の労働時間','何分働けば一杯食べられる？',66),
 ('gaishoku-jisui','food','🍳','外食 vs 自炊','自炊すると年いくら浮く？',63),
 ('issho-tabemono','food','🍚','一生で食べる量','一生で食べるお米は何kg？',62),
 ('conveni-super','food','🛒','コンビニ vs スーパー','多用で年いくら損してる？',60),
 ('karori-undou','food','🏃','食べ物のカロリー消費','この一品、運動で消すと何分？',64),
 ('cafe-nenkan','food','☕','カフェ代 年間','カフェ通い、年いくら使ってる？',61),
 ('obento-lunch','food','🍱','お弁当 vs 外食ランチ','お弁当にすると年いくら浮く？',59),
 ('tabehoudai','food','🍽️','食べ放題の元取り','あと何皿で元が取れる？',65),
 ('uber-jisui','food','🛵','デリバリー vs 自炊','デリバリー、年いくら高い？',58),
 ('nomikai-nenkan','food','🍻','飲み会の年間予算','飲み会、年いくら使ってる？',57),
]

with io.open(IDX, encoding='utf-8') as f:
    html = f.read()

assert 'sims/yachin-tekisei/index.html' not in html, '既に挿入済みのようです（中止）'

# 1) ギャラリーカード（req-card の直前に挿入）
cards = []
for sid, slug, emoji, h3, desc, score in DATA:
    cards.append(
f'''    <a class="sim-card" data-cat="{slug}" href="sims/{sid}/index.html">
      <div class="thumb" style="background:{GRAD[slug]}"><span class="emoji">{emoji}</span></div>
      <div class="body"><div class="cat">{LABEL[slug]}</div><h3>{h3}</h3><p>{desc}</p><span class="go">触ってみる →</span></div>
    </a>
''')
cards_block = '\n'.join(cards) + '\n'
marker = '    <a class="req-card" href="request/index.html">'
assert marker in html
html = html.replace(marker, cards_block + marker, 1)

# 2) ランキング（`  ];` の前に挿入）
rank = []
for sid, slug, emoji, h3, desc, score in DATA:
    rank.append(f"    {{ href: 'sims/{sid}/index.html', emoji: '{emoji}', title: '{h3}', cat: '{LABEL[slug]}', score: {score} }}")
idx = html.index('\n  ];')
before = html[:idx].rstrip()
if not before.endswith(','):
    before += ','
html = before + '\n' + ',\n'.join(rank) + html[idx:]

# 3) 本数 160 -> 180
html = html.replace('<b>160</b>本 公開中', '<b>180</b>本 公開中', 1)

with io.open(IDX, 'w', encoding='utf-8') as f:
    f.write(html)
print('patched index.html: +20 cards, +20 ranking, count=180')
