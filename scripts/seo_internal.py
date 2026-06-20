# -*- coding: utf-8 -*-
"""シミュラボ 内部SEO一括適用（冪等）
   - canonical / og:locale / robots メタ
   - JSON-LD（WebSite+Organization / WebApplication / FAQPage / BreadcrumbList）
   - パンくず（表示） / 関連シミュ内部リンク
   - sitemap.xml / robots.txt 生成
   公開時は BASE を実ドメインへ find/replace すること。
"""
import os, re, glob, json, html as htmllib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://shimulabo.com"   # ★公開時に実ドメインへ置換

HEAD_MARK = "<!-- seo-internal -->"
BC_MARK   = 'class="breadcrumb"'
REL_MARK  = 'class="related"'

# シミュのメタ（id, タイトル, 絵文字, カテゴリ, 説明）
SIMS = [
    ("kaigi-cost",         "会議コストシミュレーター",             "🔥", "お金・時間",     "参加人数と年収から、会議中に溶けていく人件費をリアルタイム計算。"),
    ("kuchikomi-hakyu",    "口コミ波及シミュレーター",             "📈", "マーケティング", "店舗の口コミが集客にどれだけ波及するかを12か月でシミュレーション。"),
    ("jutai",              "渋滞は勝手に生まれる",                 "🚗", "ふしぎ・現象",   "事故ゼロでも渋滞の波が発生する自然渋滞をリング道路で再現。"),
    ("machi-jikan",        "人生の「待ち時間」シミュレーター",     "⏳", "人生・自分ごと", "信号・レジ・電車・読み込み…生涯で待つだけに使う時間を計算。"),
    ("scroll-distance",    "スクロール距離メーター",               "📱", "人生・自分ごと", "スマホ時間から、親指が1年でスクロールする距離をエベレスト換算。"),
    ("influencer-soroban", "インフルエンサー皮算用シミュレーター", "🦝", "マーケティング", "フォロワー数から皮算用の月収と脳内ランクを判定するジョークツール。"),
    ("catchcopy",          "うさんくさいキャッチコピー製造機",     "🪧", "マーケティング", "商品名を入れるだけでうさんくさい広告コピーを量産するジョークツール。"),
    ("subsc",              "サブスク墓場シミュレーター",           "💸", "お金・時間",     "使ってないサブスクに1年・10年で捨てている金額を計算。"),
    ("caffeine",           "カフェイン残量シミュレーター",         "☕", "人生・自分ごと", "就寝時に体内へ残るカフェイン量を半減期で計算。"),
    ("sleep-debt",         "睡眠負債シミュレーター",               "😴", "人生・自分ごと", "平日の睡眠から1年で積み上がる睡眠負債を計算。"),
    ("warikan",            "割り勘の不公平シミュレーター",         "🍻", "お金・時間",     "飲み会の割り勘で損得いくらかを飲んだ量から計算。"),
    ("takarakuji",         "宝くじ買い続けたらシミュレーター",     "🎰", "お金・時間",     "買い続けた総額・期待回収・運用との差を計算。"),
    ("oyako",              "あと何回、親に会えるか",               "👨‍👩‍👧", "人生・自分ごと", "親の年齢と会う回数から残りの回数を計算。"),
    ("infure",             "物価2倍まで何年？シミュレーター",       "📉", "お金・時間",     "インフレ率から物価2倍までの年数とお金の目減りを計算。"),
    ("if-company",         "もしあなたが会社だったら",             "🏢", "マーケティング", "年収・支出・貯金から時価総額と格付けを算出するジョーク。"),
    ("nidone",             "二度寝損失シミュレーター",             "🛌", "人生・自分ごと", "二度寝に1年で溶かす時間を映画何本分かで可視化。"),
    ("chiritsumo",         "塵も積もればシミュレーター",           "🪙", "お金・時間",     "毎日の小さな出費が積もる総額と運用との差を計算。"),
]
SIM_BY_ID = {s[0]: s for s in SIMS}

# サブページ（パンくず用ラベル）
SUBPAGES = {
    "contact": "広告掲載・タイアップ",
    "request": "リクエスト",
    "board":   "リクエストボード",
    "terms":   "利用規約",
    "privacy": "プライバシーポリシー",
}

def page_meta(path):
    rel = os.path.relpath(path, ROOT).replace("\\", "/")
    parts = rel.split("/")
    if rel == "index.html":
        return {"kind": "home", "url": "/", "prefix": ""}
    if parts[0] == "sims" and len(parts) == 3:
        return {"kind": "sim", "id": parts[1], "url": f"/sims/{parts[1]}/", "prefix": "../../"}
    if parts[0] in SUBPAGES:
        return {"kind": "sub", "id": parts[0], "url": f"/{parts[0]}/", "prefix": "../"}
    return {"kind": "other", "url": "/" + "/".join(parts[:-1]) + "/", "prefix": "../"}

def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + '</script>'

def extract_faq(htmltext):
    m = re.search(r'<dl class="faq">(.*?)</dl>', htmltext, re.S)
    if not m: return []
    block = m.group(1)
    dts = re.findall(r'<dt>(.*?)</dt>', block, re.S)
    dds = re.findall(r'<dd>(.*?)</dd>', block, re.S)
    out = []
    for q, a in zip(dts, dds):
        q = htmllib.unescape(re.sub(r'<[^>]+>', '', q)).strip()
        a = htmllib.unescape(re.sub(r'<[^>]+>', '', a)).strip()
        if q and a:
            out.append((q, a))
    return out

def head_block(meta, htmltext):
    url = BASE + meta["url"]
    lines = [
        HEAD_MARK,
        f'<link rel="canonical" href="{url}">',
        '<meta property="og:locale" content="ja_JP">',
        '<meta name="robots" content="index,follow">',
    ]
    blocks = []
    if meta["kind"] == "home":
        blocks.append(jsonld({
            "@context": "https://schema.org", "@type": "WebSite",
            "name": "シミュラボ", "url": BASE + "/", "inLanguage": "ja",
            "description": "身近なギモンや現象を、入力するだけで数字とアニメで体感できる無料シミュレーター集。"
        }))
        blocks.append(jsonld({
            "@context": "https://schema.org", "@type": "Organization",
            "name": "シミュラボ", "url": BASE + "/", "logo": BASE + "/apple-touch-icon.png"
        }))
    elif meta["kind"] == "sim":
        sid = meta["id"]; _, title, _, cat, desc = SIM_BY_ID[sid]
        blocks.append(jsonld({
            "@context": "https://schema.org", "@type": "WebApplication",
            "name": title, "url": url, "description": desc,
            "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any",
            "inLanguage": "ja", "isAccessibleForFree": True,
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "JPY"},
            "publisher": {"@type": "Organization", "name": "シミュラボ", "url": BASE + "/"}
        }))
        blocks.append(jsonld({
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "ホーム", "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": title, "item": url},
            ]
        }))
        faq = extract_faq(htmltext)
        if faq:
            blocks.append(jsonld({
                "@context": "https://schema.org", "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": q,
                     "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq
                ]
            }))
    elif meta["kind"] == "sub":
        label = SUBPAGES[meta["id"]]
        blocks.append(jsonld({
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "ホーム", "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": label, "item": url},
            ]
        }))
    return "\n".join("    " + l for l in lines) + "\n" + "\n".join("    " + b for b in blocks)

def breadcrumb_html(meta):
    home = meta["prefix"] + "index.html"
    if meta["kind"] == "sim":
        _, title, _, cat, _ = SIM_BY_ID[meta["id"]]
        mid = f'{htmllib.escape(cat)}<span>›</span>'
        cur = htmllib.escape(title)
    elif meta["kind"] == "sub":
        mid = ""; cur = htmllib.escape(SUBPAGES[meta["id"]])
    else:
        return None
    return (f'  <nav class="breadcrumb" aria-label="breadcrumb">'
            f'<a href="{home}">ホーム</a><span>›</span>{mid}'
            f'<span class="cur">{cur}</span></nav>\n')

def related_html(sid):
    cur = SIM_BY_ID[sid]
    same = [s for s in SIMS if s[0] != sid and s[3] == cur[3]]
    other = [s for s in SIMS if s[0] != sid and s[3] != cur[3]]
    picks = (same + other)[:3]
    cards = "".join(
        f'<a class="related-card" href="../{s[0]}/index.html"><span class="e">{s[2]}</span><span>{htmllib.escape(s[1])}</span></a>'
        for s in picks
    )
    return ('  <nav class="related" aria-label="related">\n'
            '    <h2>ほかのシミュレーション</h2>\n'
            f'    <div class="related-grid">{cards}</div>\n'
            '  </nav>\n\n')

# ---- 各ページ適用 ----
patched = 0
for path in glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    meta = page_meta(path)
    changed = False

    if HEAD_MARK not in html and "</head>" in html:
        html = html.replace("</head>", head_block(meta, html) + "\n</head>", 1)
        changed = True

    if BC_MARK not in html:
        bc = breadcrumb_html(meta)
        if bc and '<div class="sim-head">' in html:
            html = html.replace('  <div class="sim-head">', bc + '\n  <div class="sim-head">', 1)
            changed = True

    if meta["kind"] == "sim" and REL_MARK not in html:
        anchor = '  </article>\n\n  <section class="req-banner">'
        if anchor in html:
            html = html.replace(anchor, '  </article>\n\n' + related_html(meta["id"]) + '  <section class="req-banner">', 1)
            changed = True

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        patched += 1
        print("seo:", os.path.relpath(path, ROOT), "->", meta["kind"])

# ---- sitemap.xml ----
urls = ["/"] + [f"/sims/{s[0]}/" for s in SIMS] + [f"/{k}/" for k in SUBPAGES]
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in urls:
    pr = "1.0" if u == "/" else ("0.8" if u.startswith("/sims/") else "0.5")
    sm.append(f"  <url><loc>{BASE}{u}</loc><changefreq>weekly</changefreq><priority>{pr}</priority></url>")
sm.append("</urlset>")
with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write("\n".join(sm) + "\n")

# ---- robots.txt ----
with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
    f.write("User-agent: *\nAllow: /\n\nSitemap: " + BASE + "/sitemap.xml\n")

print(f"done. {patched} pages patched. sitemap.xml / robots.txt written.")
