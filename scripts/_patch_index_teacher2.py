# -*- coding: utf-8 -*-
"""index.html へ 教員SEO追加7本のカード＋ランキング＋本数(323)を一括挿入（1回限り）。"""
import os, io, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')
import gen_sims_teacher as M

NEW = ['hyoutei-heikin', 'gpa', 'jugyou-jisuu', 'kekka-tani', 'kyoin-kyuryo', 'kyosai-bairitsu', 'gakkyu-hensei']
byid = {s['id']: s for s in M.SIMS}
GRAD = 'linear-gradient(135deg,#fff7ed,#ffedd5)'
LABEL = '教員・先生'

with io.open(IDX, encoding='utf-8') as f:
    html = f.read()
assert 'sims/hyoutei-heikin/index.html' not in html, '既に挿入済み（中止）'

cards = []; ranks = []
for i, sid in enumerate(NEW):
    s = byid[sid]
    desc = s.get('ogdesc', s.get('desc', ''))[:46]
    score = 66 - i  # SEO狙いなので上位寄り
    cards.append(
f'''    <a class="sim-card" data-cat="teacher" href="sims/{sid}/index.html">
      <div class="thumb" style="background:{GRAD}"><span class="emoji">{s['emoji']}</span></div>
      <div class="body"><div class="cat">{LABEL}</div><h3>{s['h1']}</h3><p>{desc}</p><span class="go">触ってみる →</span></div>
    </a>
''')
    ranks.append(f"    {{ href: 'sims/{sid}/index.html', emoji: '{s['emoji']}', title: '{s['h1']}', cat: '{LABEL}', score: {score} }}")

marker = '    <a class="req-card" href="request/index.html">'
assert marker in html
html = html.replace(marker, '\n'.join(cards) + '\n' + marker, 1)

idx = html.index('\n  ];')
before = html[:idx].rstrip()
if not before.endswith(','): before += ','
html = before + '\n' + ',\n'.join(ranks) + html[idx:]

html = html.replace('<b>316</b>本 公開中', '<b>323</b>本 公開中', 1)

with io.open(IDX, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'patched index.html: +{len(NEW)} cards/ranking, count=323')
