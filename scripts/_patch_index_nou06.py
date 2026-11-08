# -*- coding: utf-8 -*-
"""十人十脳と連動するテスト 第10弾（1回限り・2026-11-08 用意・公開は長澤さんのOK後）
   - 新規3本：zukei-housoku（第20話）・matsu-chikara（第21話）・tsukaimichi-test（第22話）。作り直し2本（mental-rotation 第19話・stroop-test 第23話）はシェア画像の差し替えだけ。トップのカード＋ランキング＋公開本数、share.js の ALLOW、sitemap
   - シェア画像は プロジェクト/YouTube脳科学チャンネル/クリエイティブ/診断ページOGP/ で作ったものを ogp/ に写す
   ページ本体は scripts/gen_nou_pages.py で作る
"""
import io, os, re, shutil

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPTS)
OGP_SRC = r"C:\Users\pc\Desktop\Nsawa\プロジェクト\YouTube脳科学チャンネル\クリエイティブ\診断ページOGP"
TODAY = "2026-11-08"
GRAD = "linear-gradient(135deg,#f0fdfa,#ccfbf1)"

NEW = [  # (slug, emoji, タイトル, カード説明, score)
    ("zukei-housoku", "🔷", "図形の法則テスト（？に入る図形はどれ？）", "IQテストによく出る行列の図形8問。あなたは答えを組み立てる派？見比べる派？", 55),
    ("matsu-chikara", "⏳", "待つ力テスト（今もらう？あとで多く？）", "マシュマロの実験と同じ「今か、あとか」の10問。正解のない選び方のくせ。", 55),
    ("tsukaimichi-test", "📎", "使い道テスト（クリップの使い道、30秒でいくつ？）", "答えは1つじゃない。30秒×2回で分かる発想のタイプ。", 55),
]
for slug in ("mental-rotation", "stroop-test"):   # 作り直し：シェア画像だけ差し替え
    shutil.copyfile(os.path.join(OGP_SRC, slug + ".png"), os.path.join(ROOT, "ogp", slug + ".png"))

for slug, *_ in NEW:
    shutil.copyfile(os.path.join(OGP_SRC, slug + ".png"), os.path.join(ROOT, "ogp", slug + ".png"))
    assert os.path.isfile(os.path.join(ROOT, "sims", slug, "index.html")), slug

IDX = os.path.join(ROOT, "index.html")
html = io.open(IDX, encoding="utf-8").read()
assert "sims/zukei-housoku/" not in html, "既に挿入済み（中止）"

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
sm = sm.replace("</urlset>", "".join("  <url><loc>https://shimulabo.com/sims/%s/</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>%s" % (s, TODAY, nl) for s, *_ in NEW) + "</urlset>")
io.open(SM, "w", encoding="utf-8", newline="").write(sm)
print("share.js / sitemap.xml updated")
