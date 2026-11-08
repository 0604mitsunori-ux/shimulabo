# -*- coding: utf-8 -*-
"""3Dシリーズのページをトップ・サイトマップ・OGPに足す（2026-11-08〜）
   使い方: python -I scripts/_patch_index_3d.py 追加リスト.json
   リストの形: [{"slug","emoji","title","desc","cat":"wonder|rika","catname","score","ogp_title","ogp_cat"}]
   - OGP画像は gen_images.py の make_ogp（関数の定義部分だけ実行し、全画像の作り直しはしない）
   - トップ：req-card の前にカード、const SIMS にランキング、公開本数 +N
   - sitemap.xml に追記
"""
import io, json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
SCRIPTS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPTS)
TODAY = "2026-11-08"
GRAD = {"wonder": "linear-gradient(135deg,#eef2ff,#e0e7ff)", "rika": "linear-gradient(135deg,#ecfeff,#cffafe)", "home": "linear-gradient(135deg,#ecfdf5,#d1fae5)", "money": "linear-gradient(135deg,#fff1f2,#ffe4e6)"}

NEW = json.load(io.open(sys.argv[1], encoding="utf-8"))
for n in NEW:
    assert os.path.isfile(os.path.join(ROOT, "sims", n["slug"], "index.html")), n["slug"]

# ---- OGP ----
src = io.open(os.path.join(SCRIPTS, "gen_images.py"), encoding="utf-8").read()
cut = src.index("\nSIMS = [") if "\nSIMS = [" in src else src.index("\nfor _m in")
ns = {"__file__": os.path.join(SCRIPTS, "gen_images.py"), "__name__": "gen_images_partial"}
sys.path.insert(0, SCRIPTS)
exec(compile(src[:cut], "gen_images.py", "exec"), ns)
for n in NEW:
    ns["make_ogp"](os.path.join(ROOT, "ogp", n["slug"] + ".png"), n.get("ogp_title", n["title"]), n.get("ogp_cat", n["catname"]))
print("ogp: %d" % len(NEW))

# ---- トップ ----
IDX = os.path.join(ROOT, "index.html")
html = io.open(IDX, encoding="utf-8").read()
NEW = [n for n in NEW if 'href="sims/%s/"' % n["slug"] not in html]
if NEW:
    cards = "".join("""    <a class="sim-card" data-cat="%s" href="sims/%s/">
      <div class="thumb" style="background:%s"><span class="emoji">%s</span></div>
      <div class="body"><div class="cat">%s</div><h3>%s</h3><p>%s</p><span class="go">触ってみる →</span></div>
    </a>
""" % (n["cat"], n["slug"], GRAD.get(n["cat"], GRAD["wonder"]), n["emoji"], n["catname"], n["title"], n["desc"]) for n in NEW)
    marker = '    <a class="req-card" href="request/">'
    assert marker in html
    html = html.replace(marker, cards + marker, 1)
    idx = html.index("\n  ];")
    before = html[:idx].rstrip()
    if not before.endswith(","):
        before += ","
    html = before + "\n" + ",\n".join("    { href: 'sims/%s/', emoji: '%s', title: '%s', cat: '%s', score: %d }" % (n["slug"], n["emoji"], n["title"].replace("'", "’"), n["catname"], n.get("score", 60)) for n in NEW) + html[idx:]
    m = re.search(r"<b>(\d+)</b>本 公開中", html); cnt = int(m.group(1))
    html = html.replace("<b>%d</b>本 公開中" % cnt, "<b>%d</b>本 公開中" % (cnt + len(NEW)), 1)
    io.open(IDX, "w", encoding="utf-8").write(html)
    print("index.html: +%d cards, count=%d" % (len(NEW), cnt + len(NEW)))

    SM = os.path.join(ROOT, "sitemap.xml")
    sm = io.open(SM, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in sm else "\n"
    add = [n for n in NEW if "/sims/%s/<" % n["slug"] not in sm]
    sm = sm.replace("</urlset>", "".join("  <url><loc>https://shimulabo.com/sims/%s/</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>%s" % (n["slug"], TODAY, nl) for n in add) + "</urlset>")
    io.open(SM, "w", encoding="utf-8", newline="").write(sm)
    print("sitemap.xml: +%d" % len(add))
else:
    print("index.html: 追加済み（スキップ）")
