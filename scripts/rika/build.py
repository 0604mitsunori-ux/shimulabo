# -*- coding: utf-8 -*-
"""「理科の授業向け」まとめページ /rika/ を作る（冪等）。
   単元表 units.json（学習指導要領の単元 → 使えるシミュ）だけを書き換えて再実行すれば更新できる。

   やること: ① /rika/index.html を生成 ② トップに「理科の授業で使える」棚を入れる（labShelf の直後）
             ③ sitemap.xml に /rika/ を追加 ④ OGP画像 ogp/rika.png（無ければ作る）
   使い方: python scripts/rika/build.py
"""
import html, io, json, os, re, sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
ROOT = os.path.dirname(SCRIPTS)
BASE = "https://shimulabo.com"
TODAY = date.today().isoformat()


def rd(p): return io.open(p, encoding="utf-8").read()
def wr(p, s): io.open(p, "w", encoding="utf-8").write(s)
def esc(s): return html.escape(s, quote=True)


U = json.load(io.open(os.path.join(HERE, "units.json"), encoding="utf-8"))

# ---- トップのカードから、シミュの絵文字・色・タイトルを拾う（見た目を一覧と揃える） ----
index_path = os.path.join(ROOT, "index.html")
idx = rd(index_path)
CARD = {}
for m in re.finditer(r'<a class="sim-card[^"]*" data-cat="[^"]+" href="sims/([^/"]+)/">(.*?)</a>', idx, re.S):
    sid, body = m.groups()
    bg = re.search(r'class="thumb" style="([^"]*)"', body)
    em = re.search(r'<span class="emoji">(.*?)</span>', body)
    t = re.search(r"<h3>(.*?)</h3>", body, re.S)
    CARD[sid] = {"bg": bg.group(1) if bg else "", "emoji": em.group(1) if em else "🔬",
                 "title": html.unescape(re.sub("<[^>]+>", "", t.group(1)).strip()) if t else sid}

missing = sorted({it["id"] for sec in U["sections"] for g in sec["groups"] for it in g["items"] if it["id"] not in CARD}
                 | {sid for sid in U["shelf"] if sid not in CARD})
assert not missing, f"トップの一覧に無いシミュIDがあります: {missing}"


def card(it):
    c = CARD[it["id"]]
    return (f'<a class="sim-card" href="../sims/{it["id"]}/"><div class="thumb" style="{c["bg"]}"><span class="emoji">{c["emoji"]}</span></div>'
            f'<div class="body"><div class="cat">{esc(it["unit"])}</div><h3>{esc(c["title"])}</h3>'
            f'<p>{esc(it["use"])}</p><span class="go">授業で使う →</span></div></a>')


# ---- ページ本体 ----
toc = "".join(f'<a class="rika-toc-item" href="#{s["id"]}">{s["icon"]} {esc(s["title"])}</a>' for s in U["sections"])
body = ""
part_ld = []
seen = set()
for s in U["sections"]:
    body += f'\n  <h2 class="lab-h2" id="{s["id"]}">{s["icon"]} {esc(s["title"])}</h2>'
    if s.get("note"): body += f'\n  <p class="rika-note">{esc(s["note"])}</p>'
    for g in s["groups"]:
        body += f'\n  <h3 class="rika-h3">{esc(g["title"])}</h3>\n  <div class="lab-grid">' + "".join(card(it) for it in g["items"]) + "</div>"
        for it in g["items"]:
            if it["id"] not in seen:
                seen.add(it["id"])
                part_ld.append({"@type": "WebApplication", "name": CARD[it["id"]]["title"], "url": f'{BASE}/sims/{it["id"]}/'})

src_rows = "".join(f'<tr><td>{esc(x["name"])}</td><td><a href="{esc(x["url"])}" rel="noopener" target="_blank">{esc(x["url"])}</a></td></tr>'
                   for x in U["sources"])
faq = U["faq"]
faq_html = "".join(f"<h3>{esc(q)}</h3><p>{esc(a)}</p>" for q, a in faq)
title = U["title"]; desc = U["description"]
ld_collection = {"@context": "https://schema.org", "@type": "CollectionPage", "name": U["h1"], "url": f"{BASE}/rika/",
                 "description": desc, "inLanguage": "ja", "educationalLevel": "小学校・中学校・高等学校", "hasPart": part_ld}
ld_crumb = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "シミュラボ", "item": f"{BASE}/"},
    {"@type": "ListItem", "position": 2, "name": U["h1"], "item": f"{BASE}/rika/"}]}
ld_faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
J = lambda o: json.dumps(o, ensure_ascii=False)

page = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" type="image/svg+xml" href="../favicon.svg">
    <link rel="icon" type="image/png" sizes="32x32" href="../favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="../favicon-16x16.png">
    <link rel="apple-touch-icon" href="../apple-touch-icon.png">
    <meta property="og:site_name" content="シミュラボ">
    <meta property="og:url" content="{BASE}/rika/">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta property="og:title" content="{esc(U["og_title"])}">
<meta property="og:description" content="{esc(U["og_description"])}">
<meta property="og:type" content="website">
    <meta property="og:image" content="{BASE}/ogp/rika.png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="{BASE}/ogp/rika.png">
<link rel="stylesheet" href="../assets/style.css?v=4">
    <link rel="canonical" href="{BASE}/rika/">
    <meta property="og:locale" content="ja_JP">
    <meta name="robots" content="index,follow">
    <script type="application/ld+json">{J(ld_collection)}</script>
    <script type="application/ld+json">{J(ld_crumb)}</script>
    <script type="application/ld+json">{J(ld_faq)}</script>
    <!-- ga4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-R72MT9H7PT"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","G-R72MT9H7PT");</script>
<style>
.lab-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px;margin:10px 0 6px;}}
.lab-h2{{margin:40px 0 4px;font-size:21px;scroll-margin-top:12px;}}
.rika-h3{{margin:22px 0 2px;font-size:15px;opacity:.85;}}
.rika-note{{font-size:13px;opacity:.75;margin:4px 0 0;}}
.lab-badge{{display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:800;padding:4px 12px;border-radius:999px;background:rgba(44,107,134,.10);color:var(--teal-d);}}
.rika-toc{{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0 6px;}}
.rika-toc-item{{display:inline-block;padding:8px 14px;border:1px solid rgba(127,127,127,.35);border-radius:8px;font-weight:700;font-size:14px;text-decoration:none;}}
.rika-tips{{margin:18px 0 0;padding:14px 16px;border:1px solid rgba(127,127,127,.3);border-radius:10px;font-size:14px;line-height:1.8;}}
.rika-tips ul{{margin:6px 0 0 1.2em;padding:0;}}
.src-table{{width:100%;border-collapse:collapse;font-size:13px;margin:12px 0;}}
.src-table th,.src-table td{{padding:8px 10px;border-bottom:1px solid rgba(127,127,127,.25);text-align:left;vertical-align:top;word-break:break-all;}}
.src-table th{{font-size:12px;opacity:.75;white-space:nowrap;}}
</style>
</head>
<body>
<header class="site-header">
  <div class="inner">
    <a class="brand" href="../">
      <span class="mark">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M9 3h6M10 3v5.2L5.4 16.4A2.4 2.4 0 0 0 7.5 20h9a2.4 2.4 0 0 0 2.1-3.6L14 8.2V3" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M7.7 14.5h8.6" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/>
          <circle cx="10.3" cy="16.7" r="1" fill="#fff"/><circle cx="13.4" cy="17.4" r=".7" fill="#fff"/>
        </svg>
      </span>
      <span class="name">シミュ<b>ラボ</b></span>
    </a>
    <span class="spacer"></span>
    <a class="back" href="../">← 一覧へ</a>
  </div>
</header>
<main class="wrap">
  <nav class="breadcrumb" aria-label="breadcrumb"><a href="../">ホーム</a><span>›</span><span class="cur">{esc(U["h1"])}</span></nav>
  <div class="sim-head">
    <span class="lab-badge">🔬 理科の授業向け</span>
    <h1>{esc(U["h1"])}</h1>
    <p class="lead">{esc(U["lead"])}</p>
  </div>
  <div class="rika-toc">{toc}</div>
  <div class="rika-tips"><strong>授業で使うときのヒント</strong><ul>{"".join(f"<li>{esc(t)}</li>" for t in U["tips"])}</ul></div>
{body}

  <h2 class="lab-h2" id="faq">よくある質問</h2>
  {faq_html}
  <h2 class="lab-h2" id="sources">単元名の出典</h2>
  <p class="rika-note">{esc(U["sources_note"])}</p>
  <table class="src-table"><thead><tr><th>資料</th><th>URL</th></tr></thead><tbody>{src_rows}</tbody></table>
  <div class="rika-tips"><strong>授業で使いたいシミュレーションはありますか？</strong><br>{esc(U["request_text"])} <a href="../request/" style="font-weight:800;">シミュレーションのリクエスト →</a></div>
</main>

<footer class="site-footer">
  <div class="inner">
    <p><a href="../">← シミュラボ トップへ戻る</a>　<a href="../lab/">🧪 シミュレーション・ラボ</a>　<a href="../live/">⚡ ライブデータラボ</a></p>
    <p style="margin-top:10px;opacity:.7">© 2026 シミュラボ</p>
  </div>
</footer>
<script src="../assets/lang-toggle.js?v=4"></script>
</body>
</html>
'''
os.makedirs(os.path.join(ROOT, "rika"), exist_ok=True)
wr(os.path.join(ROOT, "rika", "index.html"), page)
n_items = sum(len(g["items"]) for s in U["sections"] for g in s["groups"])
print(f"rika/index.html: {len(seen)}本（掲載 {n_items}か所）")

# ---- トップの棚（labShelf の直後。既にあれば置き換え） ----
cards = "".join(f'<a class="related-card" href="sims/{sid}/"><span class="e">{CARD[sid]["emoji"]}</span><span>{esc(CARD[sid]["title"])}</span></a>'
                for sid in U["shelf"])
shelf = (f'<section class="rank-wrap" id="rikaShelf">\n    <div class="rank-head">\n      <h2>🔬 理科の授業で使える</h2>\n'
         f'      <span class="note">小学校〜高校の単元別</span>\n    </div>\n    <div class="related-grid">{cards}</div>\n'
         f'    <div style="margin-top:10px;text-align:right;"><a href="rika/" style="font-weight:800;font-size:13px;">🔬 学年・単元別に{len(seen)}本を見る →</a></div>\n  </section>')
if 'id="rikaShelf"' in idx:
    idx = re.sub(r'<section class="rank-wrap" id="rikaShelf">.*?</section>', lambda m: shelf, idx, count=1, flags=re.S)
else:
    m = re.search(r'<section class="rank-wrap" id="labShelf">.*?</section>', idx, re.S)
    assert m, "トップに labShelf が見つかりません"
    idx = idx[:m.end()] + "\n  " + shelf + idx[m.end():]
wr(index_path, idx)
print("index.html: 棚を更新")

# ---- sitemap ----
sm_path = os.path.join(ROOT, "sitemap.xml"); sm = rd(sm_path)
entry = f"<url><loc>{BASE}/rika/</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>"
if f"<loc>{BASE}/rika/</loc>" in sm:
    sm = re.sub(r"<url><loc>" + re.escape(BASE) + r"/rika/</loc>.*?</url>", entry, sm, count=1)
else:
    sm = sm.replace("</urlset>", "  " + entry + "\n</urlset>")
wr(sm_path, sm)
print("sitemap.xml: /rika/")

# ---- OGP ----
ogp = os.path.join(ROOT, "ogp", "rika.png")
if not os.path.exists(ogp):
    gen_path = os.path.join(SCRIPTS, "gen_images.py")
    ns = {"__file__": gen_path}
    exec(compile(rd(gen_path).split("\nSIMS = [")[0], gen_path, "exec"), ns)
    ns["make_ogp"](ogp, "理科の授業で使えるシミュレーター", "小学校〜高校の単元別")
    print("ogp/rika.png を作成")
