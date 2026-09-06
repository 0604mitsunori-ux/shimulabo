# -*- coding: utf-8 -*-
"""Fable20 シリーズ投入（冪等）: sims生成 → OGP → index.html（カード/ランキング/本数/ラボ棚） → /lab/ ハブ → sitemap → api/share.js ALLOW
   使い方: python scripts/fable20/build.py
"""
import os, io, re, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
ROOT = os.path.dirname(SCRIPTS)
sys.path.insert(0, HERE); sys.path.insert(0, SCRIPTS)
from common import render, G, CATJP, BASE, TODAY
import sims_a, sims_b, sims_c, sims_d

SIMS = sims_a.SIMS + sims_b.SIMS + sims_c.SIMS + sims_d.SIMS
assert len(SIMS) == 20, len(SIMS)
slugs = [s["slug"] for s in SIMS]
assert len(set(slugs)) == 20, "slug重複"

def rd(p): return io.open(p, encoding='utf-8').read()
def wr(p, s): io.open(p, 'w', encoding='utf-8').write(s)

# ---- sims ----
for s in SIMS:
    dst = os.path.join(ROOT, "sims", s["slug"])
    os.makedirs(dst, exist_ok=True)
    wr(os.path.join(dst, "index.html"), render(s))
print("generated %d sims" % len(SIMS))

# ---- OGP ----
gen_path = os.path.join(SCRIPTS, "gen_images.py")
gen_src = rd(gen_path)
ns = {"__file__": gen_path}
exec(compile(gen_src.split("\nSIMS = [")[0], gen_path, "exec"), ns)
for s in SIMS:
    p = os.path.join(ROOT, "ogp", s["slug"] + ".png")
    if not os.path.exists(p):
        ns["make_ogp"](p, s["title"], CATJP[s["cat"]])
if not os.path.exists(os.path.join(ROOT, "ogp", "lab.png")):
    ns["make_ogp"](os.path.join(ROOT, "ogp", "lab.png"), "シミュレーション・ラボ", "科学モデルで動く20本")
print("ogp ok")

# ---- index.html ----
IDX = os.path.join(ROOT, "index.html"); html = rd(IDX)
if "sims/%s/" % slugs[0] not in html:
    cards, ranks = [], []
    for s in SIMS:
        cards.append(
"""    <a class="sim-card" data-cat="%s" href="sims/%s/">
      <div class="thumb" style="background:%s"><span class="emoji">%s</span></div>
      <div class="body"><div class="cat">%s</div><h3>%s</h3><p>%s</p><span class="go">触ってみる →</span></div>
    </a>
""" % (s["cat"], s["slug"], G[s["cat"]], s["emoji"], CATJP[s["cat"]], s["title"], s["card_desc"]))
        ranks.append("    { href: 'sims/%s/', emoji: '%s', title: '%s', cat: '%s', score: %d }" % (s["slug"], s["emoji"], s["title"], CATJP[s["cat"]], s["score"]))
    marker = '    <a class="req-card" href="request/">'
    html = html.replace(marker, "".join(cards) + marker, 1)
    idx2 = html.index("\n  ];")
    before = html[:idx2].rstrip()
    if not before.endswith(","): before += ","
    html = before + "\n" + ",\n".join(ranks) + html[idx2:]
    m = re.search(r"<b>(\d+)</b>本 公開中", html); cnt = int(m.group(1))
    html = html.replace("<b>%d</b>本 公開中" % cnt, "<b>%d</b>本 公開中" % (cnt + len(SIMS)), 1)
    # ラボ棚（ライブ棚の直後）
    shelf_items = "".join('<a class="related-card" href="sims/%s/"><span class="e">%s</span><span>%s</span></a>' % (s["slug"], s["emoji"], s["title"]) for s in SIMS[:8])
    shelf = """  <section class="rank-wrap" id="labShelf">
    <div class="rank-head">
      <h2>🧪 シミュレーション・ラボ</h2>
      <span class="note">科学モデル・アルゴリズムで動く</span>
    </div>
    <div class="related-grid">%s</div>
    <div style="margin-top:10px;text-align:right;"><a href="lab/" style="font-weight:800;font-size:13px;">🧪 ラボの20本を全部見る →</a></div>
  </section>
""" % shelf_items
    a = html.index('<section class="rank-wrap" id="liveShelf">')
    a = html.index("</section>", a) + len("</section>\n")
    html = html[:a] + shelf + html[a:]
    wr(IDX, html); print("patched index.html: count=%d" % (cnt + len(SIMS)))
else:
    print("index.html: already patched")

# ---- /lab/ ハブ ----
LAB = os.path.join(ROOT, "lab"); os.makedirs(LAB, exist_ok=True)
groups = [
    ("🏙️ 社会はなぜそう動くのか（エージェントモデル）", ["lotka-volterra", "shinrai-shinka", "uwasa-kakusan", "echo-chamber", "ryukou-curve", "tasuketsu-wana", "bank-run", "kansen-agent"]),
    ("🚶 行列・混雑・待ち時間（待ち行列・群衆）", ["queue-docchi", "elevator-sim", "manin-densha", "jisa-shukkin", "heya-chirakaru"]),
    ("🌊 物理で解く身近な現象（数値シミュレーション）", ["coffee-milk", "building-quake", "tsunami-kishi"]),
    ("🤖 AI・アルゴリズムのしくみ（機械学習・探索）", ["neural-play", "ga-route", "maze-ai", "markov-bunsho"]),
]
by = {s["slug"]: s for s in SIMS}
assert sorted(sum([g[1] for g in groups], [])) == sorted(slugs)
def card(s):
    return ('<a class="sim-card" href="../sims/%s/"><div class="thumb" style="background:%s"><span class="emoji">%s</span></div>'
            '<div class="body"><div class="cat">%s</div><h3>%s</h3><p>%s</p><span class="go">触ってみる →</span></div></a>'
            % (s["slug"], G[s["cat"]], s["emoji"], s["model"], s["title"], s["card_desc"]))
grid = "".join('\n  <h2 class="lab-h2">%s</h2>\n  <div class="lab-grid">%s\n  </div>\n' % (h, "".join("\n    " + card(by[x]) for x in xs)) for h, xs in groups)
model_rows = "".join("<tr><td><a href=\"../sims/%s/\">%s</a></td><td>%s</td><td>%s</td></tr>" % (s["slug"], s["title"], s["model"], s["model_note"]) for s in SIMS)
lab_faqs = [
 ("「シミュレーション・ラボ」は他のシミュレーターと何が違う？", "ここに並ぶ20本は、単純な計算式ではなく、社会科学・物理学・計算機科学で実際に研究に使われている数理モデルやアルゴリズム（ロトカ・ヴォルテラ方程式、待ち行列、反復囚人のジレンマ、浅水波方程式、ニューラルネットワークなど）をブラウザ内で丸ごと動かしています。"),
 ("結果は毎回同じ？", "乱数を使うモデル（エージェントモデル・遺伝的アルゴリズムなど）は実行のたびに少しずつ違う結果になります。それ自体が「同じルールでも結果はばらつく」というモデルの性質です。"),
 ("授業や記事で使っていい？", "はい。出典（シミュラボ＋ページURL）を明記いただければ、授業・ブログ・ニュース記事・社内資料への引用を歓迎します。"),
 ("入力したデータは送信される？", "いいえ。すべての計算はブラウザ内で完結し、サーバーには何も送られません。"),
]
ld_faq = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in lab_faqs]}, ensure_ascii=False)
ld_col = json.dumps({"@context": "https://schema.org", "@type": "CollectionPage", "name": "シミュレーション・ラボ", "url": BASE + "/lab/",
    "description": "社会科学・物理学・AIの数理モデルをブラウザで動かす体験型シミュレーター20本。", "inLanguage": "ja",
    "hasPart": [{"@type": "WebApplication", "name": s["title"], "url": "%s/sims/%s/" % (BASE, s["slug"])} for s in SIMS]}, ensure_ascii=False)
ld_bread = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "ホーム", "item": BASE + "/"}, {"@type": "ListItem", "position": 2, "name": "シミュレーション・ラボ", "item": BASE + "/lab/"}]}, ensure_ascii=False)
from common import LOGO
lab_html = '''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" type="image/svg+xml" href="../favicon.svg">
    <link rel="icon" type="image/png" sizes="32x32" href="../favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="../favicon-16x16.png">
    <link rel="apple-touch-icon" href="../apple-touch-icon.png">
    <meta property="og:site_name" content="シミュラボ">
    <meta property="og:url" content="%(base)s/lab/">
<title>シミュレーション・ラボ｜社会・物理・AIの数理モデルで動く体験型シミュレーター20選｜シミュラボ</title>
<meta name="description" content="キツネとウサギの増減、行列の待ち時間、信頼の進化、流体、津波、ニューラルネットワーク——研究で使われる数理モデルやアルゴリズムをブラウザでそのまま動かせる無料シミュレーター20本。授業・記事への引用歓迎。">
<meta property="og:title" content="シミュレーション・ラボ｜数理モデルで動く体験型シミュレーター20選">
<meta property="og:description" content="社会・物理・AIの本物のモデルをブラウザで動かす20本。">
<meta property="og:type" content="website">
    <meta property="og:image" content="%(base)s/ogp/lab.png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="%(base)s/ogp/lab.png">
<link rel="stylesheet" href="../assets/style.css?v=4">
    <link rel="canonical" href="%(base)s/lab/">
    <meta property="og:locale" content="ja_JP">
    <meta name="robots" content="index,follow">
    <script type="application/ld+json">%(ld_col)s</script>
    <script type="application/ld+json">%(ld_bread)s</script>
    <script type="application/ld+json">%(ld_faq)s</script>
    <!-- ga4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-R72MT9H7PT"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-R72MT9H7PT");</script>
    <!-- adsense -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4521532459480990"
         crossorigin="anonymous"></script>
<style>
.lab-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px;margin:14px 0 6px;}
.lab-h2{margin:34px 0 4px;font-size:20px;}
.src-table{width:100%%;border-collapse:collapse;font-size:13px;margin:12px 0;}
.src-table th,.src-table td{padding:8px 10px;border-bottom:1px solid rgba(127,127,127,.25);text-align:left;vertical-align:top;}
.src-table th{font-size:12px;opacity:.75;white-space:nowrap;}
.lab-badge{display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:800;padding:4px 12px;border-radius:999px;background:rgba(44,107,134,.10);color:var(--teal-d);}
</style>
</head>
<body>

<header class="site-header">
  <div class="inner">
    <a class="brand" href="../">
      %(logo)s
      <span class="name">シミュ<b>ラボ</b></span>
    </a>
    <span class="spacer"></span>
    <a class="back" href="../">← 一覧へ</a>
  </div>
</header>

<main class="wrap">
  <nav class="breadcrumb" aria-label="breadcrumb"><a href="../">ホーム</a><span>›</span><span class="cur">シミュレーション・ラボ</span></nav>

  <div class="sim-head">
    <span class="lab-badge">🧪 SIMULATION LAB</span>
    <h1>シミュレーション・ラボ</h1>
    <p class="lead">研究の現場で使われている「本物のモデル」を、そのままブラウザで動かせる20本。キツネとウサギの増減、行列の待ち時間、信頼の進化、流体、津波、ニューラルネットワーク——スライダーを動かすと、社会や自然が“なぜそうなるのか”が数字と動きで見えてきます。</p>
  </div>
%(grid)s
  <article class="article">
    <h2>このラボについて</h2>
    <p>シミュラボの多くのページは「入力→計算→結果」の計算機ですが、このラボの20本は<b>時間とともに状態が変化していく“動くモデル”</b>です。1体1体の住人・客・車・粒子・ニューロンが単純なルールで動き、その積み重ねとして、渋滞や分断や流行やパニックといった全体の現象が“勝手に”立ち上がります。これを<b>創発</b>と呼び、複雑系科学・計算社会科学・計算物理の中心的なテーマです。</p>
    <p>各ページの本文では、使っているモデルの式や出典、現実世界でそのモデルがどう使われているかを解説しています。授業・記事・資料でご活用ください。</p>
    <h2>使っているモデル・アルゴリズム一覧</h2>
    <div class="tbl-scroll"><table class="src-table"><tr><th>シミュレーター</th><th>モデル</th><th>出典・分野</th></tr>%(rows)s</table></div>
    <h2>引用・転載について</h2>
    <p>本ラボの各シミュレーターの結果・画面は、<b>出典を明記いただければ</b>授業・ブログ・記事・社内資料への引用を歓迎します。事前連絡は不要です。</p>
    <div class="note">推奨クレジット表記：<code>出典：シミュラボ「（シミュレーター名）」 %(base)s/sims/（slug）/</code></div>
    <h2>よくある質問</h2><dl class="faq">%(faq)s</dl>
  </article>

  <section class="req-banner">
    <h2>💡 動かしてみたいモデル、ありますか？</h2>
    <p>「このモデルを見てみたい」「この現象を再現してほしい」を送ってください。投票で人気の案から実際に作ります。</p>
    <a class="btn btn-primary" style="width:auto;display:inline-flex;padding:14px 30px;" href="../request/">リクエストする →</a>
    <div style="margin-top:12px;"><a href="../board/" style="font-size:13px;font-weight:800;">🗳️ みんなのリクエストに投票する →</a></div>
  </section>
</main>

<footer class="site-footer">
  <div class="inner">
    <p><a href="../">← シミュラボ トップへ戻る</a>　<a href="../live/">⚡ ライブデータラボ</a></p>
    <p style="margin-top:10px;opacity:.7">© 2026 シミュラボ</p>
  </div>
</footer>
<script src="../assets/lang-toggle.js?v=4"></script>
</body>
</html>
''' % dict(base=BASE, ld_col=ld_col, ld_bread=ld_bread, ld_faq=ld_faq, logo=LOGO, grid=grid, rows=model_rows,
           faq="".join("<dt>%s</dt><dd>%s</dd>" % (q, a) for q, a in lab_faqs))
wr(os.path.join(LAB, "index.html"), lab_html); print("lab/index.html written")

# ---- sitemap ----
SM = os.path.join(ROOT, "sitemap.xml"); sm = rd(SM)
add = ""
if "/lab/</loc>" not in sm:
    add += "  <url><loc>%s/lab/</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>\n" % (BASE, TODAY)
for s in SIMS:
    if "/sims/%s/</loc>" % s["slug"] not in sm:
        add += "  <url><loc>%s/sims/%s/</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>\n" % (BASE, s["slug"], TODAY)
if add:
    sm = sm.replace("</urlset>", add + "</urlset>"); wr(SM, sm); print("sitemap +%d" % add.count("<url>"))

# ---- ALLOW ----
sh = os.path.join(ROOT, "api", "share.js"); s = rd(sh)
head, rest = s.split("const ALLOW = new Set([", 1); body, tail = rest.split("]);", 1)
allow = set(re.findall(r"'([a-z0-9\-]+)'", body))
miss = [x for x in slugs if x not in allow]
if miss:
    body = body.rstrip() + "\n  // fable20\n  " + ", ".join("'%s'" % x for x in miss) + ",\n"
    wr(sh, head + "const ALLOW = new Set([" + body + "]);" + tail); print("ALLOW +%d" % len(miss))
print("ALL DONE")
