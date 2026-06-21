# -*- coding: utf-8 -*-
"""JA音声入力10ページの<head>にhreflang(ja/en/x-default)を注入（冪等）。
   英語版が存在するidのみ。canonicalの直後に差し込む。"""
import os, io
import gen_sims_voice_en as EN
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://shimulabo.com"

ids = [s['id'] for s in EN.SIMS]
n = 0
for sid in ids:
    path = os.path.join(ROOT, 'sims', sid, 'index.html')
    if not os.path.exists(path):
        print('skip(missing)', sid); continue
    with io.open(path, encoding='utf-8') as f:
        html = f.read()
    if 'hreflang="en"' in html:
        continue
    block = (
        f'    <link rel="alternate" hreflang="ja" href="{BASE}/sims/{sid}/">\n'
        f'    <link rel="alternate" hreflang="en" href="{BASE}/en/sims/{sid}/">\n'
        f'    <link rel="alternate" hreflang="x-default" href="{BASE}/sims/{sid}/">\n'
    )
    anchor = f'<link rel="canonical" href="{BASE}/sims/{sid}/">'
    if anchor in html:
        html = html.replace(anchor, anchor + '\n' + block.rstrip('\n'), 1)
    elif '</head>' in html:
        html = html.replace('</head>', block + '</head>', 1)
    else:
        print('skip(no head)', sid); continue
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    n += 1
    print('hreflang ja:', sid)
print(f'done. {n} JA pages got hreflang.')
