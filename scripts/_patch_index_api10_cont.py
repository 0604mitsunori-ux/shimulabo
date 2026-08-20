# -*- coding: utf-8 -*-
"""_patch_index_api10.py の続き（OGP生成→index.html→sitemap.xml）。コピーとheadパッチは完了済み前提。"""
import os, io, re

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPTS)
TODAY = "2026-08-20"

NEW = [
    ("renkyuu-maker",  "work",   "仕事・働き方",     "linear-gradient(135deg,#eff6ff,#dbeafe)", "🏖️", "9連休メーカー",
     "有休を「どこに置くか」で連休は倍変わる。最新の祝日データから最大連休を自動発見。", 71),
    ("kaibatsu-check", "home",   "住まい・暮らし",   "linear-gradient(135deg,#ecfdf5,#d1fae5)", "⛰️", "うちの海抜チェッカー",
     "自分の家の海抜、言えますか？住所を入れるだけで国土地理院データから即計算。", 70),
    ("hiyake-timer",   "beauty", "美容・ファッション", "linear-gradient(135deg,#fff1f2,#fce7f3)", "☀️", "日焼けタイマー",
     "今日のUV指数をリアルタイム取得。あなたの肌だと何分で焼け始めるかを計算。", 69),
    ("enyasu-taikan",  "money",  "お金・時間",       "linear-gradient(135deg,#fff1f2,#ffe4e6)", "💱", "円安体感メーター",
     "そのiPhone、超円高の2011年なら9万円だった。最新レートで「あの頃」と比較。", 68),
    ("jishin-live",    "wonder", "ふしぎ・現象",     "linear-gradient(135deg,#eef2ff,#e0e7ff)", "🗾", "日本はいまも揺れている",
     "直近24時間に日本で起きた地震をリアルタイム集計。思ったより多くて驚くやつ。", 67),
    ("sakura-kaisu",     "life",  "人生・自分ごと", "linear-gradient(135deg,#fefce8,#fef9c3)", "🌸", "桜をあと何回見られるか",
     "桜が咲くのは年に一度、ほんの2週間。人生であと何回見られるかを数える。", 58),
    ("shuumatsu-nokori", "life",  "人生・自分ごと", "linear-gradient(135deg,#fefce8,#fef9c3)", "📅", "人生に残された週末カウンター",
     "「また今度の週末でいいか」——その週末、人生にあと何回ある？", 57),
    ("sofubo-jikan",     "life",  "人生・自分ごと", "linear-gradient(135deg,#fefce8,#fef9c3)", "👵", "祖父母と過ごせる残り時間",
     "おじいちゃん・おばあちゃんに会えるのはあと何回か、会う頻度から計算。", 56),
    ("tomodachi-kaisu",  "life",  "人生・自分ごと", "linear-gradient(135deg,#fefce8,#fef9c3)", "🤝", "友達とあと何回会えるか",
     "「また今度ね」のあの友達。今のペースだと、人生であと何回会える？", 55),
    ("yasumeru-kaisu",   "study", "学生・勉強",     "linear-gradient(135deg,#f5f3ff,#ede9fe)", "🏫", "あと何回休めるか計算",
     "授業の全回数と必要な出席率から、単位を落とさず「あと何回休めるか」を計算。", 54),
]

IDX = os.path.join(ROOT, "index.html")
with io.open(IDX, encoding="utf-8") as f:
    html = f.read()
assert "sims/renkyuu-maker/" not in html, "既に挿入済み（中止）"

# ---------- 3) OGP画像生成 ----------
gen_path = os.path.join(SCRIPTS, "gen_images.py")
gen_src = io.open(gen_path, encoding="utf-8").read()
defs_only = gen_src.split("\nSIMS = [")[0]
ns = {"__file__": gen_path}
exec(compile(defs_only, gen_path, "exec"), ns)
for slug, _cat, catjp, _g, _e, title, _d, _s in NEW:
    ns["make_ogp"](os.path.join(ROOT, "ogp", slug + ".png"), title, catjp)

# ---------- 4) index.html ----------
cards, ranks = [], []
for slug, cat, catjp, grad, emoji, title, desc, score in NEW:
    cards.append(
"""    <a class="sim-card" data-cat="%s" href="sims/%s/">
      <div class="thumb" style="background:%s"><span class="emoji">%s</span></div>
      <div class="body"><div class="cat">%s</div><h3>%s</h3><p>%s</p><span class="go">触ってみる →</span></div>
    </a>
""" % (cat, slug, grad, emoji, catjp, title, desc))
    ranks.append("    { href: 'sims/%s/', emoji: '%s', title: '%s', cat: '%s', score: %d }" % (slug, emoji, title, catjp, score))

marker = '    <a class="req-card" href="request/">'
assert marker in html
html = html.replace(marker, "".join(cards) + marker, 1)

idx = html.index("\n  ];")
before = html[:idx].rstrip()
if not before.endswith(","):
    before += ","
html = before + "\n" + ",\n".join(ranks) + html[idx:]

m = re.search(r"<b>(\d+)</b>本 公開中", html)
assert m, "公開本数カウンタが見つからない"
cnt = int(m.group(1))
html = html.replace("<b>%d</b>本 公開中" % cnt, "<b>%d</b>本 公開中" % (cnt + len(NEW)), 1)

with io.open(IDX, "w", encoding="utf-8") as f:
    f.write(html)
print("patched index.html: +%d cards/ranking, count=%d" % (len(NEW), cnt + len(NEW)))

# ---------- 5) sitemap.xml ----------
SM = os.path.join(ROOT, "sitemap.xml")
with io.open(SM, encoding="utf-8") as f:
    sm = f.read()
assert "sims/renkyuu-maker/" not in sm, "sitemap既に挿入済み"
entries = "".join(
    "  <url><loc>https://shimulabo.com/sims/%s/</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>\n" % (slug, TODAY)
    for slug, *_ in NEW)
sm = sm.replace("</urlset>", entries + "</urlset>")
with io.open(SM, "w", encoding="utf-8") as f:
    f.write(sm)
print("patched sitemap.xml: +%d urls" % len(NEW))
print("ALL DONE")
