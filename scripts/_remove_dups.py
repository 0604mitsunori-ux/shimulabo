# -*- coding: utf-8 -*-
"""重複7本を削除：sims/フォルダ削除＋index.htmlのカード/ランキング除去＋本数569→562＋share.js ALLOW除去。"""
import os, io, re, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUPS = ['inu-nenrei','neko-nenrei','taishibo-keisan','naishinten','saidai-shinpaku','kodomo-shincho','jidoshazei']

# 1) sims フォルダ削除
for sid in DUPS:
    d=os.path.join(ROOT,'sims',sid)
    if os.path.isdir(d): shutil.rmtree(d); print('removed dir:',sid)
    else: print('  (no dir):',sid)

# 2) index.html：カード（<a class="sim-card" ... href="sims/<id>/...">...</a>）とランキング行を除去
idx=os.path.join(ROOT,'index.html')
with io.open(idx,encoding='utf-8') as f: html=f.read()
for sid in DUPS:
    # カードブロック（<a class="sim-card" ... href="sims/SID/index.html"> ... </a>\n）
    pat=re.compile(r'\s*<a class="sim-card"[^>]*href="sims/'+re.escape(sid)+r'/index\.html">.*?</a>\n',re.S)
    html,n1=pat.subn('\n',html)
    # ランキング行（    { href: 'sims/SID/index.html', ... },?\n）
    pat2=re.compile(r'\s*\{ href: \047sims/'+re.escape(sid)+r'/index\.html\047,.*?\}(,?)\n',re.S)
    html,n2=pat2.subn('\n',html)
    print(f'index {sid}: card x{n1}, rank x{n2}')
# 本数 569→562
assert '<b>569</b>本 公開中' in html
html=html.replace('<b>569</b>本 公開中','<b>562</b>本 公開中',1)
# 連続空行を整理
html=re.sub(r'\n{3,}','\n\n',html)
with io.open(idx,'w',encoding='utf-8') as f: f.write(html)

# 3) share.js ALLOW から除去
sj=os.path.join(ROOT,'api','share.js')
with io.open(sj,encoding='utf-8') as f: js=f.read()
for sid in DUPS:
    js=js.replace("'"+sid+"', ", "").replace(", '"+sid+"'", "").replace("'"+sid+"'", "")
js=re.sub(r',\s*,',',',js)
with io.open(sj,'w',encoding='utf-8') as f: f.write(js)
print('share.js cleaned.')

# 確認
with io.open(idx,encoding='utf-8') as f: h=f.read()
left=[s for s in DUPS if ('sims/'+s+'/index.html') in h]
print('still in index:',left if left else 'none')
print('done. count=562')
