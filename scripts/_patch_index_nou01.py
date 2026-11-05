# -*- coding: utf-8 -*-
"""脳のちがい診断 第1弾：共感覚テスト（kyokankaku-test）を投入（1回限り）。
   sims/kyokankaku-test/index.html は作成済み（og:image も設定済み）なので、
   1) OGP画像を生成（gen_images.py の関数を再利用）
   2) index.html にカード＋ランキング＋公開本数を挿入
   3) api/share.js の ALLOW に id を追加
   sitemap.xml はこのあと scripts/build_sitemap.py で作り直す（ファイルから自動で拾う）
"""
import os, io, re

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPTS)
TODAY = "2026-11-05"

# (slug, data-cat, カテゴリ表示名, グラデ, emoji, タイトル, カード説明, score)
NEW = [
    ("kyokankaku-test", "brain", "脳トレ・診断テスト", "linear-gradient(135deg,#f0fdfa,#ccfbf1)", "🎨", "共感覚テスト（文字に色が見える？）",
     "あなたの「あ」は何色？文字に色が見える人は100人に1〜2人。約2分のセルフテスト。", 55),
]

IDX = os.path.join(ROOT, "index.html")
with io.open(IDX, encoding="utf-8") as f:
    html = f.read()
assert "sims/kyokankaku-test/" not in html, "既に挿入済み（中止）"
for slug, *_ in NEW:
    assert os.path.isfile(os.path.join(ROOT, "sims", slug, "index.html")), "ページが無い: " + slug

# ---------- 1) OGP画像生成（gen_images.py の定義部だけ実行して再利用） ----------
gen_src = io.open(os.path.join(SCRIPTS, "gen_images.py"), encoding="utf-8").read()
defs_only = gen_src.split("\nSIMS = [")[0]
ns = {"__file__": os.path.join(SCRIPTS, "gen_images.py")}
exec(compile(defs_only, "gen_images_defs", "exec"), ns)
for slug, _cat, catjp, _g, _e, title, _d, _s in NEW:
    ns["make_ogp"](os.path.join(ROOT, "ogp", slug + ".png"), "文字に色が見える？共感覚テスト", catjp)  # 仮。公開版は 案A（プロジェクト/YouTube脳科学チャンネル/クリエイティブ/共感覚/ogp_A.html）で差し替え

# ---------- 2) index.html: カード＋ランキング＋本数 ----------
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

# ---------- 3) api/share.js の ALLOW ----------
SH = os.path.join(ROOT, "api", "share.js")
with io.open(SH, encoding="utf-8") as f:
    js = f.read()
for slug, *_ in NEW:
    if "'%s'" % slug in js:
        continue
    assert "'hsp-shindan'" in js
    js = js.replace("'hsp-shindan'", "'hsp-shindan', '%s'" % slug, 1)
with io.open(SH, "w", encoding="utf-8") as f:
    f.write(js)
print("patched api/share.js ALLOW")
print("ALL DONE")
