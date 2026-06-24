# -*- coding: utf-8 -*-
"""index.html へ 便利ツール10本＋脳トレ・診断テスト10本のカード＋ランキング＋本数(406→426)を一括挿入（冪等）。
CATS/GROUPSへの 'tool'/'brain' 追加は index.html 側で別途実施済み。"""
import os, io, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_sims_tool, gen_sims_brain

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')

GRAD = {'tool':'linear-gradient(135deg,#eff6ff,#e0f2fe)', 'brain':'linear-gradient(135deg,#f0fdfa,#ccfbf1)'}
LABEL = {'tool':'便利ツール', 'brain':'脳トレ・診断テスト'}

# 短い見出し・説明・スコア
CARD = {
  # 便利ツール
  'percent-keisan':  ('パーセント計算機','割合・何％・増減率を一発計算。',70),
  'bunsuu-keisan':   ('分数計算機','分数の＋−×÷を約分つきで計算。',66),
  'jikan-keisan':    ('時間計算機','2つの時刻の差・経過時間を計算（夜勤対応）。',64),
  'shinsu-henkan':   ('進数変換ツール','2進・8進・10進・16進を相互変換。',67),
  'wareki-henkan':   ('西暦・和暦変換','令和・平成は何年？年齢・干支も。',68),
  'nissu-keisan':    ('日数計算機','2つの日付の間は何日？あと何日も。',69),
  'kakuritsu-keisan':('確率計算機','○％を何回引けば当たる？ガチャの確率。',65),
  'tani-henkan':     ('単位変換ツール','長さ・重さ・面積・容量をまとめて換算。',63),
  'hayasa-keisan':   ('速さ・距離・時間','2つ入れると残り1つを計算（はじき）。',60),
  'moji-count':      ('文字数カウント','貼るだけで文字数・原稿用紙・読了時間。',72),
  # 脳トレ・診断テスト
  'stress-check':    ('ストレスチェック','10問で今のストレス度をセルフ診断。',72),
  'hsp-shindan':     ('HSP診断（繊細さん）','あなたの繊細さレベルを12問でチェック。',70),
  'eq-shindan':      ('EQ診断','心の知能指数を10問でチェック。',66),
  'anger-type':      ('怒りやすさ診断','あなたの“沸点”を10問でチェック。',65),
  'kanpeki-do':      ('完璧主義度診断','こだわりの強さを10問でチェック。',62),
  'kizukare':        ('気疲れ・人疲れ度診断','人といると疲れる度合いをチェック。',64),
  'shinpaisei':      ('心配性度診断','あなたの不安の強さを10問でチェック。',61),
  'nou-nenrei':      ('脳年齢テスト','計算スピードで脳の若さをチェック。',68),
  'suuji-kioku':     ('数字記憶テスト','何桁まで覚えられる？記憶力チェック。',67),
  'stroop-test':     ('ストループテスト','文字でなく“色”を答える脳トレ。',63),
}

DATA = []
for s in gen_sims_tool.SIMS:
    DATA.append((s['id'], 'tool', s['emoji'], CARD[s['id']][0], CARD[s['id']][1], CARD[s['id']][2]))
for s in gen_sims_brain.SIMS:
    DATA.append((s['id'], 'brain', s['emoji'], CARD[s['id']][0], CARD[s['id']][1], CARD[s['id']][2]))

with io.open(IDX, encoding='utf-8') as f:
    html = f.read()

assert 'sims/percent-keisan/index.html' not in html, '既に挿入済みのようです（中止）'

# 1) ギャラリーカード
cards = []
for sid, slug, emoji, h3, desc, score in DATA:
    cards.append(
f'''    <a class="sim-card" data-cat="{slug}" href="sims/{sid}/index.html">
      <div class="thumb" style="background:{GRAD[slug]}"><span class="emoji">{emoji}</span></div>
      <div class="body"><div class="cat">{LABEL[slug]}</div><h3>{h3}</h3><p>{desc}</p><span class="go">触ってみる →</span></div>
    </a>
''')
marker = '    <a class="req-card" href="request/index.html">'
assert marker in html
html = html.replace(marker, ('\n'.join(cards) + '\n') + marker, 1)

# 2) ランキング
rank = []
for sid, slug, emoji, h3, desc, score in DATA:
    rank.append(f"    {{ href: 'sims/{sid}/index.html', emoji: '{emoji}', title: '{h3}', cat: '{LABEL[slug]}', score: {score} }}")
idx = html.index('\n  ];')
before = html[:idx].rstrip()
if not before.endswith(','):
    before += ','
html = before + '\n' + ',\n'.join(rank) + html[idx:]

# 3) 本数 406 -> 426
assert '<b>406</b>本 公開中' in html, '本数マーカー(406)が見つかりません'
html = html.replace('<b>406</b>本 公開中', '<b>426</b>本 公開中', 1)

with io.open(IDX, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'patched index.html: +{len(DATA)} cards, +{len(DATA)} ranking, count=426')
