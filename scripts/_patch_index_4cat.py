# -*- coding: utf-8 -*-
"""index.html へ 美容/スポーツ/推し活/メンタル 計40本のカード＋ランキング＋本数(235)を一括挿入（1回限り）。"""
import os, io
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')

GRAD = {
  'beauty': 'linear-gradient(135deg,#fff1f2,#fce7f3)',
  'sports': 'linear-gradient(135deg,#ecfdf5,#d1fae5)',
  'oshi':   'linear-gradient(135deg,#faf5ff,#fae8ff)',
  'mental': 'linear-gradient(135deg,#eff6ff,#e0e7ff)',
}
LABEL = {'beauty':'美容・ファッション','sports':'スポーツ・運動','oshi':'推し活・エンタメ','mental':'メンタル・自己分析'}

# (id, slug, emoji, h3, desc, score)
DATA = [
 ('datsumo-sougaku','beauty','🪒','脱毛の総額','全身脱毛、結局いくらかかる？',67),
 ('cosme-nenkan','beauty','💄','コスメ代 年間','美容にかけてるお金、年いくら？',62),
 ('fuku-shogai','beauty','👗','服の生涯コスト','一生で服にいくら使う？',61),
 ('biyoin-nenkan','beauty','💇','美容院 年間費用','髪にかけるお金、年いくら？',58),
 ('diet-mokuhyou','beauty','🥗','ダイエット目標カロリー','1日何kcal減らせばいい？',64),
 ('nail-matsu','beauty','💅','ネイル・まつエク 年間','指先と目元の維持費は？',56),
 ('hada-nenrei','beauty','✨','肌年齢診断','あなたの肌、実年齢より若い？',66),
 ('wardrobe','beauty','👚','クローゼット稼働率','持ってる服、ちゃんと着てる？',59),
 ('kami-nobiru','beauty','✂️','髪が伸びるまで','目標の長さまであと何ヶ月？',57),
 ('depacos','beauty','💋','デパコス vs プチプラ','生涯でどれだけ差がつく？',60),
 ('marathon-yosoku','sports','🏃','フルマラソン完走予測','今の走力でフルは何時間？',68),
 ('run-pace','sports','👟','ランニング目標ペース','目標タイムには1km何分？',62),
 ('kintore-1rm','sports','🏋️','1RM計算機','あなたのMAXは何kg？',63),
 ('tairyoku-nenrei','sports','💪','体力年齢診断','体力、実年齢より若い？',66),
 ('shomou-undou','sports','🔥','運動の消費カロリー','その運動、何kcal燃える？',61),
 ('golf-handi','sports','⛳','ゴルフ ハンデ目安','あなたのハンデはどのくらい？',55),
 ('swim-pace','sports','🏊','水泳ペース換算','100mあたり何秒？',54),
 ('jitensha','sports','🚴','サイクリング所要＆消費','その距離、何分で何kcal？',57),
 ('taishibo-otoshi','sports','📉','体脂肪を落とす運動量','何時間運動すればいい？',60),
 ('shinpaku-zone','sports','❤️','心拍ゾーン計算','脂肪燃焼に効く心拍数は？',58),
 ('oshi-nenkan','oshi','💸','推し活 年間費用','推しにかけてるお金、年いくら？',70),
 ('live-ensei','oshi','🚄','ライブ遠征費','遠征、年でいくら使ってる？',64),
 ('subsc-motodori','oshi','📺','動画サブスク 元取り','月何本観れば元が取れる？',63),
 ('tsumige','oshi','🎮','積みゲー消化','全部クリアに何年かかる？',67),
 ('eiga-shougai','oshi','🎬','一生で観る映画','あと何本観られる？',62),
 ('manga-otomegai','oshi','📚','漫画 大人買い','全巻そろえると総額は？',61),
 ('oshi-jikan','oshi','⏰','推しに使う時間','一生で何日、推しと過ごす？',65),
 ('ticket-tousen','oshi','🎫','チケット当選確率','何口応募すれば当たる？',66),
 ('live-sankai','oshi','🎤','一生で行けるライブ回数','あと何回参戦できる？',60),
 ('goods-shuunou','oshi','📦','推しグッズ収納','うちのグッズ、何箱分？',59),
 ('stress-do','mental','😣','ストレス度診断','今のストレスはどのくらい？',69),
 ('seikaku-type','mental','🧭','性格タイプ診断','あなたはどんなタイプ？',71),
 ('moeotsuki-do','mental','😮‍💨','燃え尽き度チェック','頑張りすぎていませんか？',66),
 ('jiko-koutei','mental','🌱','自己肯定感チェック','自己肯定感はどのくらい？',67),
 ('komyu-type','mental','💬','コミュ力タイプ診断','あなたの対人スタイルは？',65),
 ('kachikan','mental','🧩','価値観診断','本当に大事にしているものは？',64),
 ('chrono','mental','🌙','朝型・夜型診断','あなたの最適な時間帯は？',63),
 ('ketsudan','mental','🔀','決断スタイル診断','直感型？熟考型？',62),
 ('resilience','mental','🛟','レジリエンス診断','あなたの立ち直る力は？',61),
 ('kokoro-yoyuu','mental','🍃','心の余裕度チェック','今のあなたに、ゆとりはある？',64),
]

with io.open(IDX, encoding='utf-8') as f:
    html = f.read()

assert 'sims/datsumo-sougaku/index.html' not in html, '既に挿入済みのようです（中止）'

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

rank = []
for sid, slug, emoji, h3, desc, score in DATA:
    rank.append(f"    {{ href: 'sims/{sid}/index.html', emoji: '{emoji}', title: '{h3}', cat: '{LABEL[slug]}', score: {score} }}")
idx = html.index('\n  ];')
before = html[:idx].rstrip()
if not before.endswith(','):
    before += ','
html = before + '\n' + ',\n'.join(rank) + html[idx:]

html = html.replace('<b>195</b>本 公開中', '<b>235</b>本 公開中', 1)

with io.open(IDX, 'w', encoding='utf-8') as f:
    f.write(html)
print('patched index.html: +40 cards, +40 ranking, count=235')
