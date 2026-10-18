# -*- coding: utf-8 -*-
"""理科の授業向けシミュを生成・登録する（冪等）。

  python scripts/rika/build_sims.py --module sims_tenmon   … そのモジュールのページだけ生成（作成中の確認用。トップ等は触らない）
  python scripts/rika/build_sims.py                        … 全モジュールを生成し、OGP・トップのカード/ランキング/本数・
                                                              カテゴリ「理科の授業向け」・サイトマップ・share.js ALLOW まで反映

  シミュ1本 = dict。必須キーは AGENT_SPEC.md。モジュールは MODULES に足す。
  ※ seo_internal.py はサイトマップを作り直すときにここのシミュを含まないので、実行後は本スクリプトも再実行すること。
"""
import importlib, io, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
ROOT = os.path.dirname(SCRIPTS)
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8")
from common import render, G, CATJP, BASE, TODAY

MODULES = ["sims_tenmon", "sims_denki_hikari", "sims_kishou_jishin", "sims_chikara", "sims_ryushi_iden",   # 第1弾
           "sims_tentai", "sims_chisou", "sims_kishou2", "sims_denki_kagaku", "sims_karada_gijutsu", "sims_kinsei",   # 第2弾
           "sims_hikari_bane", "sims_youkai_nenshou", "sims_suiyoueki_kuuki", "sims_undou_shigoto", "sims_shokubutsu", "sims_saibou_fuyuu",   # 第3弾
           "sims_kou_butsuri", "sims_kou_kagaku_seibutsu", "sims_kou_chigaku"]   # 第4弾（高校）
REQUIRED = ["slug", "cat", "title", "title_tag", "meta_desc", "og_title", "og_desc", "lead", "model", "level", "unit",
            "emoji", "card_desc", "score", "article", "faqs", "rel", "js"]


def rd(p): return io.open(p, encoding="utf-8").read()
def wr(p, s): io.open(p, "w", encoding="utf-8").write(s)


def load(names):
    sims = []
    for n in names:
        if not os.path.exists(os.path.join(HERE, n + ".py")):
            print(f"（{n}.py はまだ無いのでスキップ）"); continue
        sims += importlib.import_module(n).SIMS
    for s in sims:
        miss = [k for k in REQUIRED if k not in s]
        assert not miss, f'{s.get("slug")}: 必須キーが足りません {miss}'
        assert s["cat"] == "rika", f'{s["slug"]}: cat は "rika"'
        assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", s["slug"]), s["slug"]
    slugs = [s["slug"] for s in sims]
    assert len(slugs) == len(set(slugs)), "slug重複"
    # 同時に作った担当どうしの rel は名前・絵文字が仮のことがあるので、実際の定義にそろえる（--module のときは全モジュールから引く）
    every = {x["slug"]: x for x in sims}
    for n in MODULES:
        if os.path.exists(os.path.join(HERE, n + ".py")):
            for x in importlib.import_module(n).SIMS: every.setdefault(x["slug"], x)
    for s in sims:
        s["rel"] = [(sl, every[sl]["emoji"], every[sl]["title"]) if sl in every else (sl, e, t) for sl, e, t in s["rel"]]
    return sims


def write_pages(sims):
    for s in sims:
        d = os.path.join(ROOT, "sims", s["slug"]); os.makedirs(d, exist_ok=True)
        wr(os.path.join(d, "index.html"), render(s))
    print("生成:", ", ".join(s["slug"] for s in sims))


args = sys.argv[1:]
if "--module" in args:
    write_pages(load([args[args.index("--module") + 1]]))
    sys.exit(0)

SIMS = load(MODULES)
write_pages(SIMS)
existing = {d for d in os.listdir(os.path.join(ROOT, "sims"))}

# ---- OGP ----
gen_path = os.path.join(SCRIPTS, "gen_images.py")
ns = {"__file__": gen_path}
exec(compile(rd(gen_path).split("\nSIMS = [")[0], gen_path, "exec"), ns)
for s in SIMS:
    p = os.path.join(ROOT, "ogp", s["slug"] + ".png")
    if not os.path.exists(p): ns["make_ogp"](p, s["title"], "理科の授業向け")

# ---- トップ: カテゴリ「理科の授業向け」 ----
IDX = os.path.join(ROOT, "index.html"); html = rd(IDX)
if "['rika','理科の授業向け','🔬']" not in html:
    html = html.replace("    ['cost','コスト・費用','🧾'],", "    ['cost','コスト・費用','🧾'],\n    ['rika','理科の授業向け','🔬'],", 1)
html = re.sub(r"\{ key: 'learn',\s*cats: \[(?!'rika')", "{ key: 'learn',  cats: ['rika', ", html, count=1)
if 'id="rika-cat-style"' not in html:
    html = html.replace("</head>", '<style id="rika-cat-style">.sim-card[data-cat="rika"]::before{background:linear-gradient(90deg,#0e7490,#22d3ee);}</style>\n</head>', 1)
assert "['rika','理科の授業向け','🔬']" in html and "cats: ['rika'," in html

# ---- トップ: カード・ランキング・本数（まだ無いものだけ） ----
new = [s for s in SIMS if f'href="sims/{s["slug"]}/"' not in html]
if new:
    cards = "".join(f'''    <a class="sim-card" data-cat="rika" href="sims/{s["slug"]}/">
      <div class="thumb" style="background:{G["rika"]}"><span class="emoji">{s["emoji"]}</span></div>
      <div class="body"><div class="cat">理科の授業向け</div><h3>{s["title"]}</h3><p>{s["card_desc"]}</p><span class="go">触ってみる →</span></div>
    </a>
''' for s in new)
    marker = '    <a class="req-card" href="request/">'
    assert marker in html
    html = html.replace(marker, cards + marker, 1)
    ranks = [f"    {{ href: 'sims/{s['slug']}/', emoji: '{s['emoji']}', title: '{s['title']}', cat: '理科の授業向け', score: {int(s['score'])} }}" for s in new]
    i = html.index("\n  ];")
    before = html[:i].rstrip()
    if not before.endswith(","): before += ","
    html = before + "\n" + ",\n".join(ranks) + html[i:]
    m = re.search(r"<b>(\d+)</b>本 公開中", html); cnt = int(m.group(1))
    html = html.replace(f"<b>{cnt}</b>本 公開中", f"<b>{cnt + len(new)}</b>本 公開中", 1)
    print(f"トップ: +{len(new)}本（計{cnt + len(new)}本）")
wr(IDX, html)

# ---- サイトマップ ----
SM = os.path.join(ROOT, "sitemap.xml"); sm = rd(SM)
add = "".join(f"  <url><loc>{BASE}/sims/{s['slug']}/</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>\n"
              for s in SIMS if f"/sims/{s['slug']}/</loc>" not in sm)
if add:
    sm = sm.replace("</urlset>", add + "</urlset>"); wr(SM, sm); print(f"sitemap +{add.count('<url>')}")

# ---- share.js ALLOW ----
sh = os.path.join(ROOT, "api", "share.js"); s = rd(sh)
head, rest = s.split("const ALLOW = new Set([", 1); body, tail = rest.split("]);", 1)
allow = set(re.findall(r"'([a-z0-9\-]+)'", body))
miss = [x["slug"] for x in SIMS if x["slug"] not in allow]
if miss:
    body = body.rstrip() + "\n  // rika\n  " + ", ".join(f"'{x}'" for x in miss) + ",\n"
    wr(sh, head + "const ALLOW = new Set([" + body + "]);" + tail); print(f"ALLOW +{len(miss)}")
print("完了")
