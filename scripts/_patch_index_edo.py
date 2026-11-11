# -*- coding: utf-8 -*-
"""リクエストボードの8案目「もし江戸時代に生まれてたら」（edo-umare）を公開する（1回限り・2026-11-11）
   トップのカード＋ランキング＋公開本数、share.js の ALLOW、sitemap、OGP画像
"""
import io, os, re

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPTS)
TODAY = "2026-11-11"
SLUG, EMOJI, TITLE, DESC = "edo-umare", "🏯", "もし江戸時代に生まれてたら診断", "生まれ年と7問で、江戸のあなたの職業・身分ガチャ・年号・推定寿命を診断。"
GRAD = "linear-gradient(135deg,#faf5ff,#f3e8ff)"

assert os.path.isfile(os.path.join(ROOT, "sims", SLUG, "index.html"))

# OGP（gen_images.py の make_ogp を再利用）
ns = {"__file__": os.path.join(SCRIPTS, "gen_images.py"), "__name__": "gen_images_lib"}
src = io.open(os.path.join(SCRIPTS, "gen_images.py"), encoding="utf-8").read()
src = src.split("# --- 全カテゴリ3本ずつ補充分")[0]   # 定義だけ（全ページの作り直しはしない）
assert "make_ogp(os.path.join(OGP_DIR" not in src
exec(compile(src, "gen_images.py", "exec"), ns)
ns["make_ogp"](os.path.join(ROOT, "ogp", SLUG + ".png"), TITLE, "占い・診断")
ns["make_ogp"](os.path.join(ROOT, "ogp", "board.png"), "みんなの「作ってほしい」と進み具合", "REQUEST BOARD")
print("ogp ok")

IDX = os.path.join(ROOT, "index.html")
html = io.open(IDX, encoding="utf-8").read()
assert "sims/%s/" % SLUG not in html, "既に挿入済み（中止）"
card = """    <a class="sim-card" data-cat="uranai" href="sims/%s/">
      <div class="thumb" style="background:%s"><span class="emoji">%s</span></div>
      <div class="body"><div class="cat">占い・診断</div><h3>%s</h3><p>%s</p><span class="go">触ってみる →</span></div>
    </a>
""" % (SLUG, GRAD, EMOJI, TITLE, DESC)
marker = '    <a class="req-card" href="request/">'
assert marker in html
html = html.replace(marker, card + marker, 1)

idx = html.index("\n  ];")
before = html[:idx].rstrip()
if not before.endswith(","):
    before += ","
html = before + "\n    { href: 'sims/%s/', emoji: '%s', title: '%s', cat: '占い・診断', score: 60 }" % (SLUG, EMOJI, TITLE) + html[idx:]

m = re.search(r"<b>(\d+)</b>本 公開中", html); cnt = int(m.group(1))
html = html.replace("<b>%d</b>本 公開中" % cnt, "<b>%d</b>本 公開中" % (cnt + 1), 1)
io.open(IDX, "w", encoding="utf-8").write(html)
print("index.html: count=%d" % (cnt + 1))

SH = os.path.join(ROOT, "api", "share.js")
js = io.open(SH, encoding="utf-8").read()
if "'%s'" % SLUG not in js:
    js = js.replace("'hsp-shindan'", "'hsp-shindan', '%s'" % SLUG, 1)
io.open(SH, "w", encoding="utf-8").write(js)

SM = os.path.join(ROOT, "sitemap.xml")
sm = io.open(SM, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in sm else "\n"
if SLUG not in sm:
    sm = sm.replace("</urlset>", "  <url><loc>https://shimulabo.com/sims/%s/</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>%s</urlset>" % (SLUG, TODAY, nl))
io.open(SM, "w", encoding="utf-8", newline="").write(sm)
print("share.js / sitemap.xml updated")
