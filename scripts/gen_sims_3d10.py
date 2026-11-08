# -*- coding: utf-8 -*-
"""3Dシリーズ 第1弾 10本を作る（2026-11-08）
   ページの中身（説明・操作・記事）はこのファイル、3Dと計算のJSは scripts/3d_pages/<slug>.js
   使い方: python -I scripts/gen_sims_3d10.py   … sims/<slug>/index.html を書き出す
   共通の舞台は assets/three/sim3d.js / sim3d.css（地下神殿のページと同じ操作感）
"""
import html as H, io, json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSDIR = os.path.join(ROOT, "scripts", "3d_pages")

SERIES = [  # 3Dシリーズの一覧（どのページにも載せる）
    ("gaikaku-housuiro", "🌊", "地下神殿 3D水位"),
    ("kurobe-dam-3d", "🏞️", "黒部ダムの水圧 3D"),
    ("shinkai-suiatsu-3d", "🌌", "深海の水圧 3D"),
    ("bunshi-katachi-3d", "⚛️", "分子の形 3D"),
    ("tenkaizu-3d", "📦", "立体の展開図 3D"),
    ("chikyu-hiruyoru-3d", "🌍", "昼と夜の地球 3D"),
    ("jishin-chikyu-3d", "🌐", "世界の地震 3D"),
    ("takasa-kurabe-3d", "🗼", "高さ比べ 3D"),
    ("shinsui-fukasa-3d", "🏠", "浸水の深さ 3D"),
    ("tsuki-kyori-3d", "🌕", "地球と月の距離 3D"),
    ("satsutaba-3d", "💴", "札束 3D"),
]

HEADER = """<header class="site-header">
  <div class="inner">
    <a class="brand" href="../../">
      <span class="mark">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M9 3h6M10 3v5.2L5.4 16.4A2.4 2.4 0 0 0 7.5 20h9a2.4 2.4 0 0 0 2.1-3.6L14 8.2V3" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M7.7 14.5h8.6" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/>
          <circle cx="10.3" cy="16.7" r="1" fill="#fff"/>
          <circle cx="13.4" cy="17.4" r=".7" fill="#fff"/>
        </svg>
      </span>
      <span class="name">シミュ<b>ラボ</b></span>
    </a>
    <span class="spacer"></span>
    <a class="back" href="../../">← 一覧へ</a>
  </div>
</header>"""


def page(p):
    slug = p["slug"]; url = "https://shimulabo.com/sims/%s/" % slug
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]}
    app_ld = {"@context": "https://schema.org", "@type": "WebApplication", "name": p["name"], "url": url, "description": p["desc"], "applicationCategory": "EducationalApplication", "operatingSystem": "Any", "inLanguage": "ja", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "JPY"}, "publisher": {"@type": "Organization", "name": "シミュラボ", "url": "https://shimulabo.com/"}}
    bc_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "ホーム", "item": "https://shimulabo.com/"}, {"@type": "ListItem", "position": 2, "name": p["name"], "item": url}]}
    jd = lambda o: json.dumps(o, ensure_ascii=False)
    cams = "".join('<button data-v="%s"%s>%s</button>' % (k, ' class="on"' if i == 0 else "", t) for i, (k, t) in enumerate(p["cams"]))
    faq_html = "".join("<dt>%s</dt><dd>%s</dd>" % (H.escape(q), H.escape(a)) for q, a in p["faq"])
    rel = "".join('<a class="related-card" href="../%s/"><span class="e">%s</span><span>%s</span></a>' % r for r in p["related"])
    ser = "".join('<a class="related-card" href="../%s/"><span class="e">%s</span><span>%s</span></a>' % s for s in SERIES if s[0] != slug)
    yt = ""
    if p.get("yt"):
        vid, ch, ttl, txt = p["yt"]
        yt = '<div class="yt-box"><span style="font-size:30px">🎬</span><div class="t"><b>3Dで解説した動画</b><br>%s<br><a href="https://www.youtube.com/watch?v=%s" target="_blank" rel="noopener">YouTube「%s」%s →</a></div></div>' % (txt, vid, ch, ttl)
    js = io.open(os.path.join(JSDIR, slug + ".js"), encoding="utf-8").read()
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- seo-head -->
    <link rel="icon" type="image/svg+xml" href="../../favicon.svg">
    <link rel="icon" type="image/png" sizes="32x32" href="../../favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="../../favicon-16x16.png">
    <link rel="apple-touch-icon" href="../../apple-touch-icon.png">
    <meta property="og:site_name" content="シミュラボ">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="https://shimulabo.com/ogp/{slug}.png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="https://shimulabo.com/ogp/{slug}.png">
<title>{p['title']}｜シミュラボ</title>
<meta name="description" content="{H.escape(p['desc'])}">
<meta property="og:title" content="{H.escape(p['title'])}">
<meta property="og:description" content="{H.escape(p['ogd'])}">
<meta property="og:type" content="website">
<link rel="stylesheet" href="../../assets/style.css?v=4">
<link rel="stylesheet" href="../../assets/three/sim3d.css?v=1">
    <!-- seo-internal -->
    <link rel="canonical" href="{url}">
    <meta property="og:locale" content="ja_JP">
    <meta name="robots" content="index,follow">
    <script type="application/ld+json">{jd(app_ld)}</script>
    <script type="application/ld+json">{jd(bc_ld)}</script>
    <script type="application/ld+json">{jd(faq_ld)}</script>
    <!-- ga4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-R72MT9H7PT"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","G-R72MT9H7PT");</script>
    <!-- adsense -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4521532459480990"
         crossorigin="anonymous"></script>
{('<style>' + p['css'] + '</style>') if p.get('css') else ''}
</head>
<body>

{HEADER}

<main class="wrap">

  <nav class="breadcrumb" aria-label="breadcrumb"><a href="../../">ホーム</a><span>›</span>{p['catname']}<span>›</span><span class="cur">{p['name']}</span></nav>

  <div class="sim-head">
    <div class="cat">{p['catname']} ／ 3D</div>
    <h1>{p['name']}</h1>
    <p class="lead">{p['lead']}</p>
  </div>

  <section class="panel">
    <h2>🧊 {p.get('viewh', '3Dで見る（ドラッグで回転）')}</h2>
    {p.get('above', '')}
    <div class="view3d{' dark' if p.get('dark') else ''}" id="view">
      <div class="load">3D模型を読み込み中…</div>
      {p.get('hud', '')}
    </div>
    <div class="cam-row" id="camRow">{cams}</div>
    {p.get('below', '')}
  </section>

  <section class="panel">
    <h2>{p['ctlh']}</h2>
    {p['ctl']}
  </section>

  <section class="panel" id="resultPanel">
    <div class="result">
      <div class="label" id="resLabel">{p['reslabel']}</div>
      <div class="big"><span id="big">—</span><span class="unit" id="bigUnit">{p['unit']}</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline">{''.join('<div class="stat"><div class="k">%s</div><div class="v%s" id="%s">—</div></div>' % (k, ' accent' if i == 2 else '', sid) for i, (sid, k) in enumerate(p['stats']))}</div>
      <div class="note" id="resNote" style="margin-top:14px;text-align:left;"></div>
      <div style="text-align:center;"><span id="shareCount" class="share-count" style="display:none"></span></div>
      <div class="share-row">
        <button class="btn btn-x" id="shareBtn">𝕏 で結果をシェア</button>
        <button class="btn btn-ghost" id="copyBtn">結果をコピー</button>
      </div>
    </div>
  </section>

  {yt}

  <article class="article">
{p['article']}
    <h2>引用・転載について</h2>
    <p>本ページの計算結果・数値は、<b>出典を明記いただければ</b>ブログ・ニュース記事・SNS・授業資料への引用を歓迎します。</p>
    <div class="note">推奨クレジット表記：<code>出典：シミュラボ「{p['name']}」 {url}</code>{('<br>' + p['src']) if p.get('src') else ''}</div>
    <h2>よくある質問</h2><dl class="faq">{faq_html}</dl>
  </article>

  <section class="series3d" aria-label="3Dシリーズ">
    <h2>🧊 3Dで触れるシリーズ</h2>
    <div class="related-grid">{ser}</div>
  </section>

  <nav class="related" aria-label="related">
    <h2>ほかのシミュレーション</h2>
    <div class="related-grid">{rel}</div>
  </nav>

  <section class="req-banner">
    <h2>💡 こんなシミュも見てみたい？</h2>
    <p>あなたの「これ数字で見たい」を送ってください。投票で人気の案から実際に作ります。</p>
    <a class="btn btn-primary" style="width:auto;display:inline-flex;padding:14px 30px;" href="../../request/">リクエストする →</a>
    <div style="margin-top:12px;"><a href="../../board/" style="font-size:13px;font-weight:800;">🗳️ みんなのリクエストに投票する →</a></div>
  </section>

</main>

<footer class="site-footer">
  <div class="inner">
    <p><a href="../../">← シミュラボ トップへ戻る</a></p>
    <p style="margin-top:10px;opacity:.7">© 2026 シミュラボ</p>
  </div>
</footer>

<script>
window.SHARE = '';
document.getElementById('shareBtn').addEventListener('click', () => window.open('https://twitter.com/intent/tweet?text=' + encodeURIComponent(window.SHARE) + '&url=' + encodeURIComponent(location.href) + '&hashtags=' + encodeURIComponent('シミュラボ'), '_blank', 'noopener'));
document.getElementById('copyBtn').addEventListener('click', async () => {{ const b = document.getElementById('copyBtn'); try {{ await navigator.clipboard.writeText(window.SHARE + '\\n' + location.href); b.textContent = 'コピーしました ✓'; setTimeout(() => b.textContent = '結果をコピー', 1600); }} catch {{ alert(window.SHARE); }} }});
</script>
<script type="module">
{js}
</script>
<script src="../../assets/share-counter.js?v=4"></script>
<script>ShareCounter.initSim({{ simId:'{slug}', badgeEl:document.getElementById('shareCount'), shareBtnIds:['shareBtn'] }});</script>
<script src="../../assets/result-fx.js?v=4"></script>
<script src="../../assets/lang-toggle.js?v=4"></script>
</body>
</html>
"""


def rng(id_, label, mn, mx, step, val):
    return '<div class="field"><div class="slider-head"><label for="%s">%s</label><span class="val" id="%sL"></span></div><input type="range" id="%s" min="%s" max="%s" step="%s" value="%s"></div>' % (id_, label, id_, id_, mn, mx, step, val)


from pages_3d10 import PAGES  # noqa: E402  ページの中身

if __name__ == "__main__":
    only = sys.argv[1:]
    for p in PAGES:
        if only and p["slug"] not in only:
            continue
        d = os.path.join(ROOT, "sims", p["slug"]); os.makedirs(d, exist_ok=True)
        io.open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page(p))
        print("wrote", p["slug"])
