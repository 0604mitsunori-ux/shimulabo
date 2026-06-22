# -*- coding: utf-8 -*-
"""全HTMLの <head> に Google AdSense 審査コードを注入（冪等）。
   使い方: python scripts/add_adsense.py
   ※ generator再生成で消えるTPLがあるため、再生成後はこのスクリプトを再実行すること。"""
import os, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = "<!-- adsense -->"
CLIENT = "ca-pub-4521532459480990"

def snippet():
    return (f'    {MARK}\n'
            f'    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={CLIENT}"\n'
            f'         crossorigin="anonymous"></script>')

patched = 0
for path in glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    if MARK in html or "</head>" not in html:
        continue
    html = html.replace("</head>", snippet() + "\n</head>", 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    patched += 1
    print("adsense:", os.path.relpath(path, ROOT))

print(f"done. {patched} files. client={CLIENT}")
