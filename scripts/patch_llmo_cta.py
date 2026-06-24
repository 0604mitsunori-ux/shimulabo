# -*- coding: utf-8 -*-
"""index.html の data-cat="marketing" シミュ全てに、AIMA5（実行型LLMOサービス）CTAを挿入（冪等）。
記事の下・リクエストバナーの直前に差し込む。既に <!-- llmo-cta --> があるページはスキップ。
追加コンテンツを作ったら index 反映後に再実行すればよい。"""
import os, io, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from llmo_cta import CTA_HTML

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')

with io.open(IDX, encoding='utf-8') as f:
    idx_html = f.read()

ids = re.findall(r'data-cat="marketing" href="sims/([a-z0-9-]+)/', idx_html)
ids = list(dict.fromkeys(ids))  # 重複除去・順序維持
print(f'marketing sims found: {len(ids)}')

MARKER = '<!-- llmo-cta -->'
ANCHOR = '  <section class="req-banner">'
inserted = 0
for sid in ids:
    p = os.path.join(ROOT, 'sims', sid, 'index.html')
    if not os.path.exists(p):
        print('  skip (not found):', sid); continue
    with io.open(p, encoding='utf-8') as f:
        html = f.read()
    if MARKER in html:
        continue
    if ANCHOR not in html:
        print('  skip (no anchor):', sid); continue
    html = html.replace(ANCHOR, CTA_HTML + '\n' + ANCHOR, 1)
    with io.open(p, 'w', encoding='utf-8') as f:
        f.write(html)
    inserted += 1
    print('  cta:', sid)

print(f'done. inserted into {inserted} sims.')
