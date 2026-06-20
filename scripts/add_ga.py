# -*- coding: utf-8 -*-
"""全HTMLの <head> に GA4(gtag.js) を注入（冪等）。
   使い方: python scripts/add_ga.py G-XXXXXXXXXX
"""
import os, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = "<!-- ga4 -->"

if len(sys.argv) < 2 or not sys.argv[1].upper().startswith("G-"):
    print("使い方: python scripts/add_ga.py G-XXXXXXXXXX"); sys.exit(1)
GA = sys.argv[1]

def snippet(ga):
    return (f'    {MARK}\n'
            f'    <script async src="https://www.googletagmanager.com/gtag/js?id={ga}"></script>\n'
            f'    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","{ga}");</script>')

patched = 0
for path in glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    if MARK in html or "</head>" not in html:
        continue
    html = html.replace("</head>", snippet(GA) + "\n</head>", 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    patched += 1
    print("ga4:", os.path.relpath(path, ROOT))

print(f"done. {patched} files. id={GA}")
