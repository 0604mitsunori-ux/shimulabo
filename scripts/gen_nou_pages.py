# -*- coding: utf-8 -*-
"""十人十脳（YouTube）と連動する「頭の中のちがい」テストのページを作る。
   ページごとの中身は scripts/nou_pages/<slug>.py の PAGE（辞書）に書き、ここは共通の枠だけ。
   使い方: python scripts/gen_nou_pages.py [slug ...]   （省略すると nou_pages/ の全部）
   - 動画が公開されたら、各ページの PAGE["video_id"] に本編のIDを入れて作り直す
   - 共感覚テスト（sims/kyokankaku-test）は手書きの第1号なので、この仕組みでは作らない
"""
import html, importlib.util, io, json, os, sys

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPTS)
PDIR = os.path.join(SCRIPTS, "nou_pages")
BASE = "https://shimulabo.com"
CAT = "脳トレ・診断テスト"

CSS = """
/* テストの画面だけ、動画のチャンネル（十人十脳）と同じ「深い青緑」にする */
.syn-stage{background:radial-gradient(ellipse 90% 70% at 50% 30%,#16303A 0%,#0D1417 78%);border-radius:var(--radius);padding:18px 16px 20px;color:#EEEAE3;}
.syn-top{display:flex;justify-content:space-between;align-items:center;font-size:13px;color:#8D9BA1;gap:10px;}
.syn-bar{height:6px;background:#2A3C43;border-radius:3px;overflow:hidden;margin:8px 0 6px;}
.syn-bar i{display:block;height:100%;width:0;background:#4FC6B4;transition:width .2s;}
.syn-ask{text-align:center;font-size:15px;color:#cfd6d8;margin:10px 0;line-height:1.7;}
.syn-big{font-size:96px;font-weight:900;text-align:center;line-height:1.15;margin:4px 0 12px;}
.syn-btns{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;}
.syn-btns.c1{grid-template-columns:1fr;}
.syn-btns.c5{grid-template-columns:repeat(5,1fr);}
.syn-btns button{border:1px solid #2A3C43;border-radius:10px;background:#111c20;color:#EEEAE3;font:inherit;font-size:15px;padding:12px 6px;cursor:pointer;line-height:1.4;}
.syn-btns button:hover{border-color:#4FC6B4;}
.syn-btns button small{display:block;font-size:11px;color:#8D9BA1;margin-top:2px;}
.syn-go{display:block;width:100%;margin-top:12px;border:0;border-radius:10px;background:#4FC6B4;color:#0D1417;font:inherit;font-weight:800;font-size:16px;padding:13px;cursor:pointer;}
.syn-note{font-size:12px;color:#8D9BA1;margin-top:10px;line-height:1.6;}
.syn-rows{margin:14px 0 4px;font-size:14px;text-align:left;}
.syn-rows div{display:flex;align-items:center;gap:10px;padding:6px 4px;border-bottom:1px solid var(--line);}
.syn-rows .k{flex:1;}
.syn-rows .v{font-weight:800;color:var(--teal-d);}
.syn-meter{height:10px;border-radius:5px;background:var(--line-2);overflow:hidden;flex:0 0 120px;}
.syn-meter i{display:block;height:100%;background:var(--teal);}
.syn-video{position:relative;padding-top:56.25%;border-radius:var(--radius);overflow:hidden;background:#0D1417;margin:10px 0;}
.syn-video iframe{position:absolute;inset:0;width:100%;height:100%;border:0;}
#qPanel,#resultPanel{scroll-margin-top:72px;}
[hidden]{display:none !important;}
"""

# どのページでも同じ：結果の表示・1080×1080の結果画像・保存と共有・動画の枠
COMMON_JS = r"""
const NOU = (() => {
  const $ = (id) => document.getElementById(id);
  let SHARE = '', cardBlob = null;
  if (CONF.video_id) {
    $('video').hidden = false;
    $('videoFrame').src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(CONF.video_id);
    $('videoBtn').hidden = false; $('commentHint').hidden = false;
  }
  function wrap(x, text, max) {            // 1行に入らない文を折り返す
    const out = []; let line = '';
    for (const ch of text) { if (x.measureText(line + ch).width > max && line) { out.push(line); line = ch; } else line += ch; }
    if (line) out.push(line); return out;
  }
  function card(r) {
    const W = 1080, c = document.createElement('canvas'); c.width = c.height = W;
    const x = c.getContext('2d'), F = '"Noto Sans JP","Hiragino Sans","Yu Gothic",sans-serif';
    const bg = x.createRadialGradient(W / 2, 300, 60, W / 2, 420, 820);
    bg.addColorStop(0, '#1d3d49'); bg.addColorStop(.55, '#11232a'); bg.addColorStop(1, '#0D1417');
    x.fillStyle = bg; x.fillRect(0, 0, W, W); x.textAlign = 'center'; x.textBaseline = 'alphabetic';
    x.fillStyle = '#4FC6B4'; x.font = '800 30px ' + F; x.fillText(CONF.card_label, W / 2, 92);
    x.fillStyle = '#EEEAE3'; x.font = '900 60px ' + F; x.fillText(r.cardTitle, W / 2, 172);
    if (r.draw) { x.save(); r.draw(x, { x: 70, y: 220, w: W - 140, h: 560, F }); x.restore(); }
    x.textAlign = 'center'; x.fillStyle = '#EEEAE3'; x.font = '800 44px ' + F;
    wrap(x, r.cardLine, W - 140).slice(0, 2).forEach((l, i, a) => x.fillText(l, W / 2, 848 - (a.length - 1 - i) * 54));
    x.font = '900 40px ' + F; const label = r.emoji + ' ' + r.typeName, lw = x.measureText(label).width + 64;
    x.fillStyle = '#4FC6B4'; x.beginPath(); x.roundRect(W / 2 - lw / 2, 878, lw, 64, 32); x.fill();
    x.fillStyle = '#0D1417'; x.fillText(label, W / 2, 924);
    x.fillStyle = '#8D9BA1'; x.font = '700 26px ' + F; x.fillText(CONF.card_footer, W / 2, 1030);
    $('cardImg').src = c.toDataURL('image/png');
    cardBlob = null; c.toBlob(b => {
      cardBlob = b; const f = new File([b], CONF.slug + '.png', { type: 'image/png' });
      $('shareImgBtn').hidden = !(navigator.canShare && navigator.canShare({ files: [f] }));
    }, 'image/png');
  }
  function finish(r) {
    $('qPanel').hidden = true; $('resultPanel').hidden = false;
    $('rLabel').textContent = r.label; $('big').textContent = r.big; $('bigUnit').textContent = r.unit || '';
    $('typeName').textContent = r.emoji + ' ' + r.typeName; $('advice').textContent = '💡 ' + r.advice;
    $('extra').innerHTML = r.extraHTML || ''; $('extra').hidden = !r.extraHTML;
    SHARE = r.share; card(r);
    $('resultPanel').scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  function startPanels() {
    $('startPanel').hidden = $('resultPanel').hidden = true; $('qPanel').hidden = false;
    $('qPanel').scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  $('saveImgBtn').addEventListener('click', () => { const a = document.createElement('a'); a.href = $('cardImg').src; a.download = CONF.slug + '.png'; document.body.appendChild(a); a.click(); a.remove(); });
  $('shareImgBtn').addEventListener('click', async () => { if (!cardBlob) return; try { await navigator.share({ files: [new File([cardBlob], CONF.slug + '.png', { type: 'image/png' })], text: SHARE + ' #' + CONF.tag + ' ' + location.href }); } catch (e) {} });
  $('shareBtn').addEventListener('click', () => window.open('https://twitter.com/intent/tweet?text=' + encodeURIComponent(SHARE) + '&url=' + encodeURIComponent(location.href) + '&hashtags=' + encodeURIComponent(CONF.tag + ',シミュラボ'), '_blank', 'noopener'));
  $('copyBtn').addEventListener('click', async () => { try { await navigator.clipboard.writeText(SHARE + '\n' + location.href); $('copyBtn').textContent = 'コピーしました ✓'; setTimeout(() => $('copyBtn').textContent = '結果をコピー', 1600); } catch { alert(SHARE); } });
  return { finish, startPanels, $ };
})();
"""

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

FOOTER = """<section class="req-banner">
    <h2>💡 こんな診断も見てみたい？</h2>
    <p>あなたの「これ診断・テストしてみたい」を送ってください。投票で人気の案から実際に作ります。</p>
    <a class="btn btn-primary" style="width:auto;display:inline-flex;padding:14px 30px;" href="../../request/">リクエストする →</a>
    <div style="margin-top:12px;"><a href="../../board/" style="font-size:13px;font-weight:800;">🗳️ みんなのリクエストに投票する →</a></div>
  </section>

</main>

<footer class="site-footer">
  <div class="inner">
    <p><a href="../../">← シミュラボ トップへ戻る</a></p>
    <p style="margin-top:10px;opacity:.7">© 2026 シミュラボ</p>
  </div>
</footer>"""


def esc(s):
    return html.escape(s, quote=True)


def build(P):
    slug = P["slug"]; url = "%s/sims/%s/" % (BASE, slug)
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": _strip(a)}} for q, a in P["faq"]]}
    app_ld = {"@context": "https://schema.org", "@type": "WebApplication", "name": P["ld_name"], "url": url, "description": P["desc"],
              "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any", "inLanguage": "ja", "isAccessibleForFree": True,
              "offers": {"@type": "Offer", "price": "0", "priceCurrency": "JPY"}, "publisher": {"@type": "Organization", "name": "シミュラボ", "url": BASE + "/"}}
    bc_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "ホーム", "item": BASE + "/"}, {"@type": "ListItem", "position": 2, "name": P["ld_name"], "item": url}]}
    conf = {"slug": slug, "video_id": P.get("video_id", ""), "tag": P["tag"], "card_label": P["card_label"], "card_footer": P["card_footer"]}
    faq_html = "".join("<dt>%s</dt><dd>%s</dd>" % (esc(q), a) for q, a in P["faq"])
    refs_html = "".join("<li>%s</li>" % r for r in P["refs"])
    rel_html = "".join('<a class="related-card" href="../%s/"><span class="e">%s</span><span>%s</span></a>' % (s, e, esc(t)) for s, e, t in P["related"])
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
    <meta property="og:image" content="{BASE}/ogp/{slug}.png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="{BASE}/ogp/{slug}.png">
<title>{esc(P['title'])}</title>
<meta name="description" content="{esc(P['desc'])}">
<meta property="og:title" content="{esc(P['og_title'])}">
<meta property="og:description" content="{esc(P['og_desc'])}">
<meta property="og:type" content="website">
<link rel="stylesheet" href="../../assets/style.css?v=4">
<!-- adsense -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4521532459480990"
     crossorigin="anonymous"></script>
    <!-- seo-internal -->
    <link rel="canonical" href="{url}">
    <meta property="og:locale" content="ja_JP">
    <meta name="robots" content="index,follow">
    <script type="application/ld+json">{json.dumps(app_ld, ensure_ascii=False)}</script>
    <script type="application/ld+json">{json.dumps(bc_ld, ensure_ascii=False)}</script>
    <script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
    <!-- ga4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-R72MT9H7PT"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","G-R72MT9H7PT");</script>
<style>{CSS}{P.get('css', '')}</style>
</head>
<body>

{HEADER}

<main class="wrap">

  <nav class="breadcrumb" aria-label="breadcrumb"><a href="../../">ホーム</a><span>›</span>{CAT}<span>›</span><span class="cur">{esc(P['ld_name'])}</span></nav>

  <div class="sim-head">
    <div class="cat">{CAT}</div>
    <h1>{esc(P['h1'])}</h1>
    <p class="lead">{P['lead']}</p>
  </div>

  <section class="panel" id="startPanel">
    <h2>{P['start_h2']}</h2>
    <p style="color:var(--ink-2);font-size:14px;margin:-4px 0 12px;">{P['start_text']}</p>
    {P.get('start_extra', '')}
    <button class="btn btn-primary" id="startBtn">{P.get('start_btn', 'はじめる')}</button>
    <p style="color:var(--ink-3);font-size:12px;margin-top:10px;">※ 遊びのためのセルフテストで、検査や診断ではありません。答えは送信も保存もしません。</p>
  </section>

  <section class="panel" id="qPanel" hidden>
    <div class="syn-stage">{P['stage_html']}</div>
  </section>

  <section class="panel" id="resultPanel" hidden>
    <div class="result">
      <div class="label" id="rLabel">—</div>
      <div class="big" style="font-size:48px;"><span id="big">—</span><small style="font-size:20px;" id="bigUnit"></small></div>
      <div class="sub" id="typeName" style="font-size:20px;font-weight:800;color:var(--teal-d);">—</div>
      <div class="alert good" id="advice" style="text-align:left;margin-top:14px;">—</div>
      <div id="extra" style="text-align:left;margin-top:10px;" hidden></div>
      <h3 style="font-size:16px;margin:18px 0 8px;">🖼️ 結果を1枚の画像に</h3>
      <img id="cardImg" alt="結果の画像" style="width:100%;max-width:460px;border-radius:12px;display:block;margin:0 auto;box-shadow:var(--shadow);">
      <p style="font-size:12px;color:var(--ink-3);margin-top:6px;">スマホは画像を長押しでも保存できます。画像はこの画面の中で作っていて、どこにも送っていません。</p>
      <div class="share-row">
        <button class="btn btn-primary" id="saveImgBtn">画像を保存</button>
        <button class="btn btn-ghost" id="shareImgBtn" hidden>画像でシェア</button>
      </div>
      <div style="text-align:center;margin-top:12px;"><span id="shareCount" class="share-count" style="display:none"></span></div>
      <div class="share-row">
        <button class="btn btn-x" id="shareBtn">𝕏 で結果をシェア</button>
        <button class="btn btn-ghost" id="copyBtn">結果をコピー</button>
      </div>
      <p id="commentHint" style="font-size:13px;color:var(--ink-2);margin-top:10px;" hidden>コピーした結果は、動画のコメント欄にそのまま貼れます。ほかの人の結果と比べてみてください。</p>
      <a class="btn btn-primary" id="videoBtn" href="#video" style="margin-top:10px;" hidden>▶ 動画で答え合わせをする</a>
      <button class="btn btn-ghost" id="againBtn" style="margin-top:10px;">もう一度</button>
    </div>
  </section>

  <article class="article">
    <div class="note"><strong>これは何？</strong>：{P['note']}<br><b>※遊びのためのもので、検査や診断ではありません。</b>答えはこの画面の中だけで使い、送信も保存もしません。</div>

    <section id="video" hidden>
      <h2>動画で答え合わせ</h2>
      <p>このテストの答え合わせと、研究の話を動画にしました。</p>
      <div class="syn-video"><iframe id="videoFrame" title="{esc(P['ld_name'])}の解説動画" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>
    </section>

{P['article']}

    <h2>よくある質問</h2>
    <dl class="faq">{faq_html}</dl>

    <h2>参考にした研究・資料</h2>
    <ul class="seo-refs">{refs_html}</ul>
  </article>

  <nav class="related" aria-label="related">
    <h2>ほかの「頭の中のちがい」テスト</h2>
    <div class="related-grid">{rel_html}</div>
  </nav>

  {FOOTER}

<script>
const CONF = {json.dumps(conf, ensure_ascii=False)};
{COMMON_JS}
(() => {{
{P['js']}
}})();
</script>
<script src="../../assets/result-fx.js?v=4"></script>
<script src="../../assets/share-counter.js?v=4"></script>
<script>ShareCounter.initSim({{ simId:'{slug}', badgeEl:document.getElementById('shareCount'), shareBtnIds:['shareBtn'] }});</script>
<script src="../../assets/lang-toggle.js?v=4"></script>
</body>
</html>
"""


def _strip(a):
    import re
    return re.sub(r"<[^>]+>", "", a)


def load(slug_file):
    spec = importlib.util.spec_from_file_location("p", os.path.join(PDIR, slug_file))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m.PAGE


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    files = sorted(f for f in os.listdir(PDIR) if f.endswith(".py"))
    want = sys.argv[1:]
    for f in files:
        P = load(f)
        if want and P["slug"] not in want:
            continue
        out = os.path.join(ROOT, "sims", P["slug"], "index.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with io.open(out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(build(P))
        print("wrote", out)
