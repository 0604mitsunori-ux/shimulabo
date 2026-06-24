# -*- coding: utf-8 -*-
"""index.html の data-cat="tantei" シミュ全てに、探偵社CTAを挿入（冪等）。"""
import os, io, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tantei_cta import CTA_HTML
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with io.open(os.path.join(ROOT,'index.html'), encoding='utf-8') as f: idx = f.read()
ids = list(dict.fromkeys(re.findall(r'data-cat="tantei" href="sims/([a-z0-9-]+)/', idx)))
print('tantei sims:', len(ids))
MARKER='<!-- tantei-cta -->'; ANCHOR='  <section class="req-banner">'; ins=0
for sid in ids:
    p=os.path.join(ROOT,'sims',sid,'index.html')
    if not os.path.exists(p): print('  skip(nf):',sid); continue
    with io.open(p,encoding='utf-8') as f: html=f.read()
    if MARKER in html: continue
    if ANCHOR not in html: print('  skip(no anchor):',sid); continue
    html=html.replace(ANCHOR, CTA_HTML+'\n'+ANCHOR, 1)
    with io.open(p,'w',encoding='utf-8') as f: f.write(html)
    ins+=1; print('  cta:',sid)
print(f'done. inserted into {ins} sims.')
