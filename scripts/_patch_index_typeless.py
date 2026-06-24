# -*- coding: utf-8 -*-
"""index.html へ Typeless訴求シミュ10本のカード＋ランキング＋本数(386→396)を一括挿入（冪等チェック付き）。"""
import os, io, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims_typeless import SIMS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')

GRAD = 'linear-gradient(135deg,#eef2ff,#f5f3ff)'  # voiceカードと同じ
LABEL = '音声入力・時短'

# カード用の短い見出し・説明・スコア
CARD = {
  'voice-memo':     ('ボイスメモ文字起こし時短', '録音を手作業 vs 音声入力。聞き返す時間のムダを可視化。', 66),
  'voice-diary':    ('音声日記＝生涯の自分史', '1日1分の音声日記が生涯で文庫本何冊分になる？', 64),
  'sotsuron-jitan': ('卒論・レポート執筆時間', '音声入力なら卒論は何日早く終わる？締切まで逆算。', 62),
  'sumaho-input':   ('スマホ入力 生涯時間', 'フリック入力に一生で何日使う？人生グリッドで可視化。', 63),
  'ai-bunsho':      ('AI文章作成 時短', '打つより話す。AI＋音声で年間どれだけ速い？', 61),
  'writer-jikyu':   ('Webライター実質時給', '音声入力で執筆を速くすると時給は何倍に？', 60),
  'dokusho-memo':   ('読書メモ蓄積', '話してアウトプットすると学びはどれだけ残る？', 59),
  'input-baisoku':  ('話せば何倍速？診断', '実際に打って測定→音声入力と速度を体験比較。', 67),
  'atama-tana':     ('頭の中の棚卸し', '書き出せずに失う時間は？話せば一瞬で整理。', 58),
  'jinsei-input':   ('人生の入力総決算', '一生でキーボードに何日費やす？音声で取り戻す。', 65),
}
# (id, emoji, h3, desc, score) — SIMSの順序を維持
DATA = [(s['id'], s['emoji'], CARD[s['id']][0], CARD[s['id']][1], CARD[s['id']][2]) for s in SIMS]

with io.open(IDX, encoding='utf-8') as f:
    html = f.read()

assert 'sims/voice-memo/index.html' not in html, '既に挿入済みのようです（中止）'

# 1) ギャラリーカード（req-card の直前に挿入）
cards = []
for sid, emoji, h3, desc, score in DATA:
    cards.append(
f'''    <a class="sim-card" data-cat="voice" href="sims/{sid}/index.html">
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

# 3) 本数 386 -> 396
assert '<b>386</b>本 公開中' in html, '本数マーカー(386)が見つかりません'
html = html.replace('<b>386</b>本 公開中', '<b>396</b>本 公開中', 1)

with io.open(IDX, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'patched index.html: +{len(DATA)} cards, +{len(DATA)} ranking, count=396')
