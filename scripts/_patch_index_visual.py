# -*- coding: utf-8 -*-
"""index.html へ ビジュアル系10本のカード＋ランキング＋本数(376→386)を一括挿入（1回限り・冪等チェック付き）。"""
import os, io, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims_visual import SIMS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')

GRAD = {
  'wonder': 'linear-gradient(135deg,#eef2ff,#e0e7ff)',
  'play':   'linear-gradient(135deg,#ecfeff,#ede9fe)',
}
LABEL = {'wonder': 'ふしぎ・現象', 'play': 'あそぶ・実験'}

# (id, slug, emoji, h3, desc, score)
DATA = [(s['id'], s['slug'], s['emoji'], s['short'], s['carddesc'], s['score']) for s in SIMS]

with io.open(IDX, encoding='utf-8') as f:
    html = f.read()

assert 'sims/snowflake/index.html' not in html, '既に挿入済みのようです（中止）'

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
assert marker in html, 'req-card マーカーが見つかりません'
html = html.replace(marker, cards_block + marker, 1)

# 2) ランキング（最初の `\n  ];` の前に挿入）
rank = []
for sid, slug, emoji, h3, desc, score in DATA:
    rank.append(f"    {{ href: 'sims/{sid}/index.html', emoji: '{emoji}', title: '{h3}', cat: '{LABEL[slug]}', score: {score} }}")
idx = html.index('\n  ];')
before = html[:idx].rstrip()
if not before.endswith(','):
    before += ','
html = before + '\n' + ',\n'.join(rank) + html[idx:]

# 3) 本数 376 -> 386
assert '<b>376</b>本 公開中' in html, '本数マーカー(376)が見つかりません'
html = html.replace('<b>376</b>本 公開中', '<b>386</b>本 公開中', 1)

with io.open(IDX, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'patched index.html: +{len(DATA)} cards, +{len(DATA)} ranking, count=386')
