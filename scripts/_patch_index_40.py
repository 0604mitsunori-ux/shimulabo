# -*- coding: utf-8 -*-
"""index.html へ新40本のカード＋ランキング＋本数(160)を一括挿入（1回限り実行）。"""
import os, io
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')

GRAD = {
  'health': 'linear-gradient(135deg,#fef2f2,#fee2e2)',
  'uranai': 'linear-gradient(135deg,#faf5ff,#f3e8ff)',
  'car':    'linear-gradient(135deg,#eff6ff,#e0e7ff)',
  'travel': 'linear-gradient(135deg,#cffafe,#a5f3fc)',
}
LABEL = {'health':'健康・カラダ','uranai':'占い・診断','car':'クルマ・乗り物','travel':'旅行・おでかけ'}

# (id, slug, emoji, h3, desc, score)
DATA = [
 ('bmi','health','⚖️','BMI・適正体重チェック','身長と体重でBMIと適正体重をすぐ計算。',69),
 ('kiso-taisha','health','🔥','基礎代謝＆必要カロリー','1日に必要なカロリーを体格から計算。',64),
 ('tainai-nenrei','health','🫀','体内年齢診断','生活習慣5問でカラダの若さを診断。',67),
 ('suibun','health','💧','1日の水分必要量','体重と活動量で必要な水分量を計算。',58),
 ('taishibo','health','📏','体脂肪率ざっくり推定','体組成計なしで体脂肪率の目安を。',60),
 ('hosu-karori','health','🚶','歩数の消費カロリー','今日の歩数で何kcal燃えた？',61),
 ('sake-karori','health','🍺','お酒のカロリー','飲み会は何kcal？ごはん何杯分？',62),
 ('suimin-cycle','health','😴','快眠の起床時刻','何時に寝ればスッキリ起きられる？',65),
 ('suwari','health','🪑','座りすぎメーター','1年でどれだけ座ってる？',56),
 ('mizu-body','health','💦','体の水分量','カラダの何kgが水？おもしろ雑学。',54),
 ('tanjyobi-uranai','uranai','🔢','誕生日でわかる運命数','数秘術であなたの本質を占う。',70),
 ('zensei','uranai','🔮','前世診断','あなたの前世は何者だった？',71),
 ('kotoshi-unsei','uranai','🎍','今年の運勢占い','総合運・金運・恋愛運・仕事運を占う。',68),
 ('namae-uranai','uranai','📛','名前占い','名前に秘められた運勢と性格。',60),
 ('soul-color','uranai','🎨','ソウルカラー診断','あなたの魂の色は何色？',62),
 ('doubutsu-uranai','uranai','🐾','誕生月の動物キャラ占い','あなたは何の動物タイプ？',64),
 ('ketsueki-aishou','uranai','🩸','血液型相性占い','あの人との相性は何％？',66),
 ('lucky-today','uranai','🍀','今日の運勢＆ラッキー','毎日変わる今日の運気とアイテム。',63),
 ('kyusei','uranai','⭐','九星気学 本命星占い','生まれ年であなたの星を占う。',58),
 ('tarot-today','uranai','🃏','今日の一枚タロット','今日のあなたへのメッセージ。',65),
 ('nenpi-gas','car','⛽','年間ガソリン代','車のガソリン代、年いくら？',62),
 ('ev-vs-gas','car','🔌','EV vs ガソリン燃料費','電気とガソリン、どっちが得？',64),
 ('kuruma-yosan','car','🚗','車購入予算','年収でいくらの車が買える？',61),
 ('kousoku-shita','car','🛣️','高速 vs 下道','時間を取る？お金を取る？',57),
 ('shaken-tsumitate','car','🔧','車の維持費 毎月積立','車検・税金、毎月いくら貯める？',56),
 ('souko-kyori','car','🌍','生涯走行距離','あなたの車、地球を何周する？',59),
 ('chuko-nedan','car','📉','中古車 値落ち','何年後にいくらになる？',55),
 ('drive-yosan','car','🚙','ドライブ費用','日帰りドライブ、1人いくら？',58),
 ('tsukin-car','car','🚉','車通勤 vs 電車通勤','どっちが安い？',54),
 ('kuruma-hoyuu','car','🅿️','マイカー vs カーシェア','持つ？持たない？損益分岐。',53),
 ('ryohi','travel','✈️','旅行費用 総額','その旅行、ぜんぶでいくら？',66),
 ('mile-tamaru','travel','🎫','マイル特典航空券','カード払いで何ヶ月で旅に？',60),
 ('jisa-boke','travel','🕐','時差ボケ回復','現地に慣れるまで何日？',57),
 ('kaigai-iju','travel','🌏','海外移住の生活費','あの国で暮らすと月いくら？',63),
 ('tabi-tsumitate','travel','🐷','旅行貯金','あの旅まで毎月いくら貯める？',56),
 ('lcc-shinkansen','travel','🚄','LCC vs 新幹線','安さと速さ、どっちを取る？',61),
 ('gasolin-doko','travel','🛻','満タンでどこまで','満タンで走れる距離は？',58),
 ('onsen-seiha','travel','♨️','全国制覇まで何年？','47都道府県・温泉めぐり。',59),
 ('sekai-isshu','travel','🗺️','世界一周','夢の世界一周、いくらかかる？',62),
 ('theme-park','travel','🎢','テーマパーク1日予算','1日遊ぶと1人いくら？',64),
]

with io.open(IDX, encoding='utf-8') as f:
    html = f.read()

assert 'sims/bmi/index.html' not in html, '既に挿入済みのようです（中止）'

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

# 2) ランキング（最後の要素の直後、`  ];` の前に挿入）
rank = []
for sid, slug, emoji, h3, desc, score in DATA:
    rank.append(f"    {{ href: 'sims/{sid}/index.html', emoji: '{emoji}', title: '{h3}', cat: '{LABEL[slug]}', score: {score} }}")
# 直近の閉じ括弧 "  ];" を探し、その直前の最後のエントリにカンマを追加して挿入
anchor = "       score: 63 }\n  ];"  # aishou-seiza か repeat-rieki 行に依存しないため別手段
# よりロバスト：'  ];' の最初の出現を使い、その前にカンマ付きで差し込む
idx = html.index('\n  ];')
# idx の直前行末（最後のランキング要素）に ',' を付ける
before = html[:idx]
after = html[idx:]
before = before.rstrip()
if not before.endswith(','):
    before = before + ','
html = before + '\n' + ',\n'.join(rank) + after

# 3) 本数 120 -> 160
html = html.replace('<b>120</b>本 公開中', '<b>160</b>本 公開中', 1)

with io.open(IDX, 'w', encoding='utf-8') as f:
    f.write(html)
print('patched index.html: +40 cards, +40 ranking, count=160')
