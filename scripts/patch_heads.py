# -*- coding: utf-8 -*-
"""全HTMLの <head> に favicon と OGP/Twitter画像メタを挿入（冪等）。
   公開時は BASE を実ドメインに find/replace すること。
"""
import os, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://shimulabo.com"   # ★公開時に実ドメインへ置換（全ファイル一括）
VIEWPORT = '<meta name="viewport" content="width=device-width, initial-scale=1">'
MARKER = "<!-- seo-head -->"

SIM_IDS = {"kaigi-cost","jutai","scroll-distance","machi-jikan","catchcopy","influencer-soroban","kuchikomi-hakyu"}

def info(path):
    rel = os.path.relpath(path, ROOT).replace("\\", "/")
    parts = rel.split("/")
    depth = len(parts) - 1                  # index.html からルートまでの階層
    prefix = "../" * depth
    if rel == "index.html":
        ogid, url = "default", "/"
    elif parts[0] == "sims" and len(parts) == 3:
        ogid, url = parts[1], f"/sims/{parts[1]}/"
    elif parts[0] in ("contact","request","board"):
        ogid, url = parts[0], f"/{parts[0]}/"
    else:
        ogid, url = "default", f"/{parts[0]}/"
    return prefix, ogid, url

def block(prefix, ogid, url):
    img = f"{BASE}/ogp/{ogid}.png"
    return f"""    {MARKER}
    <link rel="icon" type="image/svg+xml" href="{prefix}favicon.svg">
    <link rel="icon" type="image/png" sizes="32x32" href="{prefix}favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="{prefix}favicon-16x16.png">
    <link rel="apple-touch-icon" href="{prefix}apple-touch-icon.png">
    <meta property="og:site_name" content="シミュラボ">
    <meta property="og:url" content="{BASE}{url}">
    <meta property="og:image" content="{img}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="{img}">"""

patched = 0
for path in glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    if MARKER in html:
        continue
    if VIEWPORT not in html:
        print("skip (no viewport):", os.path.relpath(path, ROOT)); continue
    prefix, ogid, url = info(path)
    html = html.replace(VIEWPORT, VIEWPORT + "\n" + block(prefix, ogid, url), 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    patched += 1
    print("patched:", os.path.relpath(path, ROOT), "->", ogid)

print(f"done. {patched} files patched.")
