# -*- coding: utf-8 -*-
"""全シミュの index.html に result-fx.js を読み込む<script>を注入（冪等）。"""
import os, glob, io
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAG = '<script src="../../assets/result-fx.js"></script>'
n = 0
for path in glob.glob(os.path.join(ROOT, 'sims', '*', 'index.html')):
    with io.open(path, encoding='utf-8') as f:
        html = f.read()
    if 'result-fx.js' in html:
        continue
    if '</body>' not in html:
        continue
    html = html.replace('</body>', TAG + '\n</body>', 1)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    n += 1
print(f'patched {n} files with result-fx.js')
