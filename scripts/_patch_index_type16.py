# -*- coding: utf-8 -*-
"""index.html へ 16タイプ性格診断10本のカード＋ランキング＋本数(396→406)を一括挿入（冪等チェック付き）。
新カテゴリ slug=type16（CATS/GROUPSへの追加は index.html 側で別途実施済み）。"""
import os, io, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims_type16 import SIMS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')

GRAD = 'linear-gradient(135deg,#fdf2f8,#ede9fe)'  # 診断＝ピンク×バイオレット
LABEL = '16タイプ性格診断'

CARD = {
  'aisho-16type':    ('16タイプ相性診断', '自分と相手のタイプを選ぶだけで相性を％診断。恋愛・友達・仕事に。', 72),
  'doubutsu-type':   ('動物に例えると診断', '12問であなたを動物に例える。相性の動物も分かる。', 70),
  'pet-aisho-type':  ('あなたに合うペット診断', '性格でわかる、相性ぴったりの犬・猫。', 66),
  'sengoku-busho':   ('戦国武将タイプ診断', 'あなたに似た戦国武将は？信長型？家康型？', 67),
  'sangokushi-type': ('三国志武将タイプ診断', 'あなたに似た三国志の英雄を診断。', 64),
  'osake-type':      ('お酒タイプ診断', 'あなたをお酒に例えると？相性のお酒も。', 65),
  'iro-type':        ('色に例えると診断', '性格でわかるあなたのパーソナルカラー。', 62),
  'hana-type':       ('花に例えると診断', 'あなたを花に例えると何の花？花言葉も。', 61),
  'yoji-jukugo-type':('四字熟語であらわす診断', 'あなたを四字熟語であらわすと？座右の銘に。', 60),
  'tenshoku-type':   ('天職・向いてる仕事診断', '性格でわかる、向いてる仕事の方向性。', 63),
}
DATA = [(s['id'], s['emoji'], CARD[s['id']][0], CARD[s['id']][1], CARD[s['id']][2]) for s in SIMS]

with io.open(IDX, encoding='utf-8') as f:
    html = f.read()

assert 'sims/aisho-16type/index.html' not in html, '既に挿入済みのようです（中止）'

# 1) ギャラリーカード（req-card の直前に挿入）
cards = []
for sid, emoji, h3, desc, score in DATA:
    cards.append(
f'''    <a class="sim-card" data-cat="type16" href="sims/{sid}/index.html">
      <div class="thumb" style="background:{GRAD}"><span class="emoji">{emoji}</span></div>
      <div class="body"><div class="cat">{LABEL}</div><h3>{h3}</h3><p>{desc}</p><span class="go">触ってみる →</span></div>
    </a>
''')
cards_block = '\n'.join(cards) + '\n'
marker = '    <a class="req-card" href="request/index.html">'
assert marker in html, 'req-card マーカーが見つかりません'
html = html.replace(marker, cards_block + marker, 1)

# 2) ランキング（最初の `\n  ];` の前に挿入）
rank = []
for sid, emoji, h3, desc, score in DATA:
    rank.append(f"    {{ href: 'sims/{sid}/index.html', emoji: '{emoji}', title: '{h3}', cat: '{LABEL}', score: {score} }}")
idx = html.index('\n  ];')
before = html[:idx].rstrip()
if not before.endswith(','):
    before += ','
html = before + '\n' + ',\n'.join(rank) + html[idx:]

# 3) 本数 396 -> 406
assert '<b>396</b>本 公開中' in html, '本数マーカー(396)が見つかりません'
html = html.replace('<b>396</b>本 公開中', '<b>406</b>本 公開中', 1)

with io.open(IDX, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'patched index.html: +{len(DATA)} cards, +{len(DATA)} ranking, count=406')
