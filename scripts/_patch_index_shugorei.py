# -*- coding: utf-8 -*-
"""index.html へ 守護霊クラスタ6本(uranai)＋出席率クラスタ4本(teacher)のカード＋ランキング＋本数(686)を一括挿入（1回限り）。"""
import os, io, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')
import gen_sims_uranai2 as U
import gen_sims_teacher as T

# (id, data-cat, label, gradient)
URA_GRAD = 'linear-gradient(135deg,#f5f3ff,#ede9fe)'
TCH_GRAD = 'linear-gradient(135deg,#fff7ed,#ffedd5)'
NEW = (
    [(sid, 'uranai', '占い・診断', URA_GRAD) for sid in ['shugoshin','shugo-tenshi','aura-color','reikan','soulmate','ryujin']] +
    [(sid, 'teacher', '教員・先生', TCH_GRAD) for sid in ['hisho-nissu','kaikin-hantei','shinkyu-hantei','chiko-soutai']]
)
byid = {}
byid.update({s['id']: s for s in U.SIMS})
byid.update({s['id']: s for s in T.SIMS})

with io.open(IDX, encoding='utf-8') as f:
    html = f.read()
assert 'sims/shugoshin/index.html' not in html, '既に挿入済み（中止）'

cards = []; ranks = []
for i, (sid, dcat, label, grad) in enumerate(NEW):
    s = byid[sid]
    desc = s.get('ogdesc', s.get('desc', ''))[:46]
    score = 68 - i  # クラスタ強化のため上位寄り
    cards.append(
f'''    <a class="sim-card" data-cat="{dcat}" href="sims/{sid}/index.html">
      <div class="thumb" style="background:{grad}"><span class="emoji">{s['emoji']}</span></div>
      <div class="body"><div class="cat">{label}</div><h3>{s['h1']}</h3><p>{desc}</p><span class="go">触ってみる →</span></div>
    </a>
''')
    ranks.append(f"    {{ href: 'sims/{sid}/index.html', emoji: '{s['emoji']}', title: '{s['h1']}', cat: '{label}', score: {score} }}")

marker = '    <a class="req-card" href="request/index.html">'
assert marker in html
html = html.replace(marker, '\n'.join(cards) + '\n' + marker, 1)

idx = html.index('\n  ];')
before = html[:idx].rstrip()
if not before.endswith(','): before += ','
html = before + '\n' + ',\n'.join(ranks) + html[idx:]

html = html.replace('<b>676</b>本 公開中', '<b>686</b>本 公開中', 1)

with io.open(IDX, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'patched index.html: +{len(NEW)} cards/ranking, count=686')
