# -*- coding: utf-8 -*-
"""十人十脳と連動するテスト 第2弾（1回限り・2026-11-05）
   - 新規3本（aphantasia-test / naigen-test / mimi-nenrei）：トップのカード＋ランキング＋公開本数、share.js の ALLOW、sitemap
   - 作り直し1本（shikikaku-test）：トップのカードの題と説明を新しい中身に、sitemap の更新日を今日に
   - シェア画像は プロジェクト/YouTube脳科学チャンネル/クリエイティブ/診断ページOGP/ で作ったものを ogp/ に写す
   ページ本体は scripts/gen_nou_pages.py で作る
"""
import io, os, re, shutil

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPTS)
OGP_SRC = r"C:\Users\pc\Desktop\Nsawa\プロジェクト\YouTube脳科学チャンネル\クリエイティブ\診断ページOGP"
TODAY = "2026-11-05"
GRAD = "linear-gradient(135deg,#f0fdfa,#ccfbf1)"

NEW = [  # (slug, emoji, タイトル, カード説明, score)
    ("aphantasia-test", "🍎", "アファンタジア テスト（頭の中の映像）", "目を閉じて、りんごは見える？頭の中に映像が浮かばない人は、およそ25人に1人。", 54),
    ("naigen-test", "💬", "頭の中の声テスト", "考えるとき、頭の中で声はしていますか？ずっとしゃべる人から、まったくない人まで。", 53),
    ("mimi-nenrei", "👂", "耳年齢テスト（モスキート音）", "この音、聞こえますか？少しずつ高くなる音で、どこまで聞こえるかを試す。", 55),
]

for slug in ["shikikaku-test"] + [n[0] for n in NEW]:
    shutil.copyfile(os.path.join(OGP_SRC, slug + ".png"), os.path.join(ROOT, "ogp", slug + ".png"))
    assert os.path.isfile(os.path.join(ROOT, "sims", slug, "index.html")), slug

IDX = os.path.join(ROOT, "index.html")
html = io.open(IDX, encoding="utf-8").read()
assert "sims/aphantasia-test/" not in html, "既に挿入済み（中止）"

# 作り直した色覚テストのカード
old = '<h3>色の識別テスト</h3><p>1つだけ違う色を探せ</p>'
assert html.count(old) == 1
html = html.replace(old, '<h3>色覚テスト（あなたの目は何色型？）</h3><p>16枚の中から1枚だけちがう色を探す。赤〜緑・青〜黄、どこまで見分けられる？</p>')

cards = "".join("""    <a class="sim-card" data-cat="brain" href="sims/%s/">
      <div class="thumb" style="background:%s"><span class="emoji">%s</span></div>
      <div class="body"><div class="cat">脳トレ・診断テスト</div><h3>%s</h3><p>%s</p><span class="go">触ってみる →</span></div>
    </a>
""" % (s, GRAD, e, t, d) for s, e, t, d, _ in NEW)
marker = '    <a class="req-card" href="request/">'
assert marker in html
html = html.replace(marker, cards + marker, 1)

idx = html.index("\n  ];")
before = html[:idx].rstrip()
if not before.endswith(","):
    before += ","
html = before + "\n" + ",\n".join("    { href: 'sims/%s/', emoji: '%s', title: '%s', cat: '脳トレ・診断テスト', score: %d }" % (s, e, t, sc) for s, e, t, _, sc in NEW) + html[idx:]

m = re.search(r"<b>(\d+)</b>本 公開中", html); cnt = int(m.group(1))
html = html.replace("<b>%d</b>本 公開中" % cnt, "<b>%d</b>本 公開中" % (cnt + len(NEW)), 1)
io.open(IDX, "w", encoding="utf-8").write(html)
print("index.html: +%d cards, count=%d" % (len(NEW), cnt + len(NEW)))

SH = os.path.join(ROOT, "api", "share.js")
js = io.open(SH, encoding="utf-8").read()
for s, *_ in NEW:
    if "'%s'" % s not in js:
        js = js.replace("'hsp-shindan'", "'hsp-shindan', '%s'" % s, 1)
io.open(SH, "w", encoding="utf-8").write(js)

SM = os.path.join(ROOT, "sitemap.xml")
sm = io.open(SM, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in sm else "\n"
sm = re.sub(r"(<loc>https://shimulabo.com/sims/shikikaku-test/</loc><lastmod>)[\d-]+", r"\g<1>" + TODAY, sm)
sm = sm.replace("</urlset>", "".join("  <url><loc>https://shimulabo.com/sims/%s/</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>%s" % (s, TODAY, nl) for s, *_ in NEW) + "</urlset>")
io.open(SM, "w", encoding="utf-8", newline="").write(sm)
print("share.js / sitemap.xml updated")
