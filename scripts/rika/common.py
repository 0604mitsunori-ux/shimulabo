# -*- coding: utf-8 -*-
"""理科の授業向けシミュ 共通：ページ骨格・部品ヘルパー（fable20/common.py を元に作成）。
   /rika/（理科の授業向け）配下のシミュとしてパンくず・戻りリンクを設定。
   各シミュは dict で定義し render(s) でHTMLにする。必須キーは AGENT_SPEC.md を参照。"""
import json, re

BASE = "https://shimulabo.com"
TODAY = "2026-10-04"

G = dict(wonder="linear-gradient(135deg,#eef2ff,#e0e7ff)", play="linear-gradient(135deg,#fdf4ff,#fae8ff)",
         marketing="linear-gradient(135deg,#fff7ed,#ffedd5)", life="linear-gradient(135deg,#fefce8,#fef9c3)",
         work="linear-gradient(135deg,#eff6ff,#dbeafe)", home="linear-gradient(135deg,#ecfdf5,#d1fae5)",
         finance="linear-gradient(135deg,#fff1f2,#ffe4e6)", health="linear-gradient(135deg,#fef2f2,#fee2e2)",
         mental="linear-gradient(135deg,#f5f3ff,#ede9fe)",
         rika="linear-gradient(135deg,#ecfeff,#cffafe)")
CATJP = dict(wonder="ふしぎ・現象", play="あそぶ・実験", marketing="マーケティング", life="人生・自分ごと",
             work="仕事・働き方", home="住まい・暮らし", finance="マネー・保険・不動産", health="健康・カラダ",
             mental="メンタル・自己分析", rika="理科の授業向け")

LOGO = '''<span class="mark">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M9 3h6M10 3v5.2L5.4 16.4A2.4 2.4 0 0 0 7.5 20h9a2.4 2.4 0 0 0 2.1-3.6L14 8.2V3" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M7.7 14.5h8.6" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/>
          <circle cx="10.3" cy="16.7" r="1" fill="#fff"/>
          <circle cx="13.4" cy="17.4" r=".7" fill="#fff"/>
        </svg>
      </span>'''

SKELETON = '''<!DOCTYPE html>
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
    <meta property="og:url" content="@@BASE@@/sims/@@SLUG@@/">
<title>@@TITLE_TAG@@｜シミュラボ</title>
<meta name="description" content="@@META_DESC@@">
<meta property="og:title" content="@@OG_TITLE@@">
<meta property="og:description" content="@@OG_DESC@@">
<meta property="og:type" content="website">
    <meta property="og:image" content="@@BASE@@/ogp/@@SLUG@@.png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="@@BASE@@/ogp/@@SLUG@@.png">
<link rel="stylesheet" href="../../assets/style.css?v=4">
    <!-- seo-internal -->
    <link rel="canonical" href="@@BASE@@/sims/@@SLUG@@/">
    <meta property="og:locale" content="ja_JP">
    <meta name="robots" content="index,follow">
    <script type="application/ld+json">@@LD_APP@@</script>
    <script type="application/ld+json">@@LD_BREAD@@</script>
    <script type="application/ld+json">@@LD_FAQ@@</script>
    <!-- ga4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-R72MT9H7PT"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-R72MT9H7PT");</script>
    <!-- adsense -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4521532459480990"
         crossorigin="anonymous"></script>
<style>
.lab-ctl{width:100%;max-width:640px;display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:8px 18px;}
.lab-ctl .field{margin-bottom:6px;}
.lab-ctl>*,.lab-stats>*{min-width:0;}
.lab-ctl .slider-head{display:flex;justify-content:space-between;align-items:center;}
.lab-ctl .slider-head label{margin:0;font-size:13px;}
.lab-ctl .val{font-weight:800;color:var(--teal-d);font-size:13px;}
.lab-ctl input[type=range]{width:100%;}
.lab-ctl select{width:100%;padding:8px;border:1px solid var(--line);border-radius:8px;font-size:14px;background:#fff;}
.lab-btns{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-top:6px;}
.lab-btns .btn{padding:11px 18px;font-size:14px;width:auto;}
.lab-stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:8px;width:100%;max-width:640px;margin-top:4px;}
.lab-stats .stat{background:var(--teal-l);border-radius:10px;padding:10px 12px;text-align:center;}
.lab-stats .k{font-size:11px;color:var(--ink-2);}
.lab-stats .v{font-size:20px;font-weight:800;color:var(--ink);font-feature-settings:"tnum";}
.lab-stats .v.accent{color:var(--accent);}
.lab-legend{text-align:center;color:var(--ink-2);font-size:13px;margin-top:12px;}
.lab-badge{display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:800;padding:4px 12px;border-radius:999px;background:rgba(44,107,134,.10);color:var(--teal-d);margin-bottom:8px;}
canvas.lab{width:100%;max-width:640px;height:auto;border:1px solid var(--line);border-radius:12px;background:#0b1020;touch-action:none;}
canvas.lab.light{background:#fff;}
.panel:fullscreen,.panel:-webkit-full-screen{overflow:auto;padding:24px;background:var(--bg,#faf8f3);}
.panel:fullscreen canvas.lab{max-width:min(96vw,1100px);}
.panel:fullscreen .lab-ctl,.panel:fullscreen .lab-stats{max-width:min(96vw,1100px);}
</style>
</head>
<body>

<header class="site-header">
  <div class="inner">
    <a class="brand" href="../../">
      ''' + LOGO + '''
      <span class="name">シミュ<b>ラボ</b></span>
    </a>
    <span class="spacer"></span>
    <a class="back" href="../../rika/">🔬 理科の授業向け</a>
  </div>
</header>

<main class="wrap">

  <nav class="breadcrumb" aria-label="breadcrumb"><a href="../../">ホーム</a><span>›</span><a href="../../rika/">理科の授業向け</a><span>›</span><span class="cur">@@H1@@</span></nav>

  <div class="sim-head">
    <div class="cat">@@CATJP@@</div>
    <h1>@@H1@@</h1>
    <p class="lead">@@LEAD@@</p>
  </div>

  <section class="panel">
    <div style="display:grid;grid-template-columns:minmax(0,1fr);justify-items:center;gap:14px;">
      <span class="lab-badge">🔬 @@MODEL@@</span>
      @@CANVAS@@
      <div class="lab-ctl">@@CONTROLS@@</div>
      <div class="lab-btns">@@BUTTONS@@</div>
      <div class="lab-stats">@@STATS@@</div>
    </div>
    <p class="lab-legend">@@LEGEND@@</p>
    <div style="text-align:center;"><span id="shareCount" class="share-count" style="display:none"></span></div>
    <div class="share-row">
      <button class="btn btn-ghost" id="fsBtn" hidden>⛶ 全画面で表示</button>
      <button class="btn btn-x" id="shareBtn">𝕏 で結果をシェア</button>
      <button class="btn btn-ghost" id="copyBtn">結果をコピー</button>
    </div>
  </section>

  <article class="article">
@@ARTICLE@@
    <h2>引用・転載について</h2>
    <p>本ページのシミュレーション結果・数値は、<b>出典を明記いただければ</b>ブログ・ニュース記事・SNS・授業や社内資料への引用を歓迎します。事前連絡は不要です。</p>
    <div class="note">推奨クレジット表記：<code>出典：シミュラボ「@@H1@@」 @@BASE@@/sims/@@SLUG@@/</code></div>
    <h2>よくある質問</h2><dl class="faq">@@FAQ_DL@@</dl>
  </article>

  <nav class="related" aria-label="related">
    <h2>ほかのシミュレーション</h2>
    <div class="related-grid">@@RELATED@@</div>
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
    <p><a href="../../">← シミュラボ トップへ戻る</a>　<a href="../../rika/">🔬 理科の授業向けシミュレーター</a></p>
    <p style="margin-top:10px;opacity:.7">© 2026 シミュラボ</p>
  </div>
</footer>

<script>
(() => {
  const $ = (id) => document.getElementById(id);
  const num = (n) => Math.round(n).toLocaleString('ja-JP');
  const clamp = (v,a,b) => Math.max(a, Math.min(b, v));
  const rnd = (a,b) => a + Math.random()*(b-a);
  const randn = () => { let u=0,v=0; while(!u)u=Math.random(); while(!v)v=Math.random(); return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v); };
  let SHARE = '';
  function setShare(t){ SHARE = t; }
  function syncSliders(){ document.querySelectorAll('input[type=range]').forEach(s=>{ const l=$(s.id+'L'); if(l){ const u=()=>{ l.textContent = (s.dataset.fmt ? s.dataset.fmt.replace('{v}', s.value) : s.value); }; s.addEventListener('input',u); u(); } }); }
  function cpos(cv,e){ const r=cv.getBoundingClientRect(); const t=(e.touches&&e.touches[0])?e.touches[0]:e; return [(t.clientX-r.left)*cv.width/r.width,(t.clientY-r.top)*cv.height/r.height]; }
  function setStat(id, v){ const e=$(id); if(e) e.textContent = v; }
  try {
    syncSliders();
@@JS@@
  } catch(e) { console.error(e); }
  (function(){ const fs=$('fsBtn'), panel=document.querySelector('.panel');
    const req = panel && (panel.requestFullscreen || panel.webkitRequestFullscreen);
    if (fs && req) { fs.hidden = false; fs.addEventListener('click', () => {
      const cur = document.fullscreenElement || document.webkitFullscreenElement;
      if (cur) { (document.exitFullscreen || document.webkitExitFullscreen).call(document); }
      else { req.call(panel); } }); }
  })();
  $('shareBtn').addEventListener('click', () => window.open('https://twitter.com/intent/tweet?text='+encodeURIComponent(SHARE || document.title)+'&url='+encodeURIComponent(location.href)+'&hashtags='+encodeURIComponent('シミュラボ'),'_blank','noopener'));
  $('copyBtn').addEventListener('click', async () => { try{ await navigator.clipboard.writeText((SHARE||document.title)+'\\n'+location.href); $('copyBtn').textContent='コピーしました ✓'; setTimeout(()=>$('copyBtn').textContent='結果をコピー',1600);}catch{alert(SHARE);} });
})();
</script>
<script src="../../assets/share-counter.js?v=4"></script>
<script>ShareCounter.initSim({ simId:'@@SLUG@@', badgeEl:document.getElementById('shareCount'), shareBtnIds:['shareBtn'] });</script>
<script src="../../assets/lang-toggle.js?v=4"></script>
</body>
</html>
'''

# ---------- 部品 ----------
def canvas(w=640, h=400, light=False):
    return '<canvas id="cv" class="lab%s" width="%d" height="%d"></canvas>' % (' light' if light else '', w, h)

def slider(id, label, mn, mx, val, step=1, fmt=None):
    f = ' data-fmt="%s"' % fmt if fmt else ''
    return ('<div class="field"><div class="slider-head"><label for="%s">%s</label><span class="val" id="%sL"></span></div>'
            '<input type="range" id="%s" min="%s" max="%s" value="%s" step="%s"%s></div>' % (id, label, id, id, mn, mx, val, step, f))

def select(id, label, opts):
    return ('<div class="field"><div class="slider-head"><label for="%s">%s</label></div><select id="%s">' % (id, label, id)
            + ''.join('<option value="%s"%s>%s</option>' % (v, ' selected' if i == 0 else '', t) for i, (v, t) in enumerate(opts)) + '</select></div>')

def btn(id, label, primary=False):
    return '<button class="btn %s" id="%s">%s</button>' % ('btn-primary' if primary else 'btn-ghost', id, label)

def stats(items):
    return ''.join('<div class="stat"><div class="k">%s</div><div class="v%s" id="%s">—</div></div>' % (k, ' accent' if acc else '', id) for id, k, acc in items)

def T(rows, head):
    return ('<div class="tbl-scroll"><table class="seo-table"><tr>' + ''.join('<th>%s</th>' % h for h in head) + '</tr>'
            + ''.join('<tr>' + ''.join('<td>%s</td>' % c for c in r) + '</tr>' for r in rows) + '</table></div>')

def N(t): return '<div class="note">' + t + '</div>'
def P(t): return '<div class="note" style="border-left:4px solid var(--teal)"><strong>ポイント</strong>：' + t + '</div>'

def faq_dl(faqs): return "".join("<dt>%s</dt><dd>%s</dd>" % (q, a) for q, a in faqs)
def faq_ld(faqs):
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in faqs]}, ensure_ascii=False)
def related(items):
    return "".join('<a class="related-card" href="../%s/"><span class="e">%s</span><span>%s</span></a>' % (s, e, t) for s, e, t in items)

def render(s):
    # 2026-10-18: 教材として読まれるよう LearningResource を併記（単元＝学習指導要領への対応・対象＝先生と児童生徒）
    ld_app = json.dumps({"@context": "https://schema.org", "@type": ["WebApplication", "LearningResource"], "name": s["title"],
        "url": "%s/sims/%s/" % (BASE, s["slug"]), "description": s["og_desc"],
        "applicationCategory": "EducationalApplication", "operatingSystem": "Any", "inLanguage": "ja",
        "isAccessibleForFree": True, "educationalLevel": s.get("level", ""), "learningResourceType": "シミュレーション",
        "teaches": s["model"], "educationalUse": ["授業", "自習"],
        "audience": {"@type": "EducationalAudience", "educationalRole": ["teacher", "student"]},
        "educationalAlignment": {"@type": "AlignmentObject", "alignmentType": "educationalSubject",
                                 "educationalFramework": "学習指導要領（平成29・30年告示）", "targetName": s["unit"]},
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "JPY"},
        "publisher": {"@type": "Organization", "name": "シミュラボ", "url": BASE + "/"}}, ensure_ascii=False)
    ld_bread = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "ホーム", "item": BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": "理科の授業向け", "item": BASE + "/rika/"},
        {"@type": "ListItem", "position": 3, "name": s["title"], "item": "%s/sims/%s/" % (BASE, s["slug"])}]}, ensure_ascii=False)
    page = SKELETON
    for k, v in [("@@BASE@@", BASE), ("@@SLUG@@", s["slug"]), ("@@TITLE_TAG@@", s["title_tag"]), ("@@META_DESC@@", s["meta_desc"]),
                 ("@@OG_TITLE@@", s["og_title"]), ("@@OG_DESC@@", s["og_desc"]), ("@@LD_APP@@", ld_app), ("@@LD_BREAD@@", ld_bread),
                 ("@@LD_FAQ@@", faq_ld(s["faqs"])), ("@@CATJP@@", CATJP[s["cat"]]), ("@@H1@@", s["title"]), ("@@LEAD@@", s["lead"]),
                 ("@@MODEL@@", s["model"]), ("@@CANVAS@@", s.get("canvas", "")), ("@@CONTROLS@@", s.get("controls", "")),
                 ("@@BUTTONS@@", s.get("buttons", "")), ("@@STATS@@", s.get("stats", "")), ("@@LEGEND@@", s.get("legend", "")),
                 ("@@ARTICLE@@", s["article"]), ("@@FAQ_DL@@", faq_dl(s["faqs"])), ("@@RELATED@@", related(s["rel"])), ("@@JS@@", s["js"])]:
        page = page.replace(k, v)
    assert "@@" not in page, [m for m in re.findall(r"@@\w+@@", page)]
    return page
