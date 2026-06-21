# -*- coding: utf-8 -*-
"""全ページ（/en/配下を除く）に lang-toggle.js を注入（冪等・相対パス深さ自動）。
   /en/ 配下は gen_sims_voice_en.py のTPLに直書き済みなので対象外。"""
import os, glob, io
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def prefix_for(path):
    rel = os.path.relpath(path, ROOT).replace('\\', '/')
    depth = rel.count('/')  # index.html=0, sims/x/index.html=2, contact/index.html=1
    return '../' * depth

n = 0
for path in glob.glob(os.path.join(ROOT, '**', 'index.html'), recursive=True):
    rel = os.path.relpath(path, ROOT).replace('\\', '/')
    if rel.startswith('en/'):
        continue
    with io.open(path, encoding='utf-8') as f:
        html = f.read()
    if 'lang-toggle.js' in html or '</body>' not in html:
        continue
    tag = f'<script src="{prefix_for(path)}assets/lang-toggle.js"></script>'
    html = html.replace('</body>', tag + '\n</body>', 1)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    n += 1
print(f'patched {n} files with lang-toggle.js')
