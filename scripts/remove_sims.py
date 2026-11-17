"""scripts/removed_sims.txt に書いたシミュを削除し、サイト内の参照を掃除する（2026-11-17・AdSense再審査）。
何度実行しても同じ結果。gen_sims*.py を再実行して消したページが復活したら、もう一度これを実行する。
  1) sims/<slug>/ を削除（git rm）
  2) 残りの HTML から、消したページへの <a>…</a>（トップのカード・関連リンク・ラボ一覧など）を取り除く
  3) トップの JS 一覧（{ href: 'sims/<slug>/…' … },）の行を取り除く
  4) assets/sim-counts.json から消す
  5) サイトマップと llms.txt を作り直す
使い方: python scripts/remove_sims.py"""
import glob, io, json, os, re, shutil, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
GONE = [l.strip() for l in io.open(os.path.join(HERE, "removed_sims.txt"), encoding="utf-8") if l.strip() and not l.startswith("#")]
S = "|".join(map(re.escape, sorted(GONE, key=len, reverse=True)))

# 1) ディレクトリ削除
rm = 0
for s in GONE:
    d = os.path.join(ROOT, "sims", s)
    if os.path.isdir(d):
        r = subprocess.run(["git", "rm", "-r", "-q", "--", f"sims/{s}"], cwd=ROOT, capture_output=True, text=True)
        if os.path.isdir(d): shutil.rmtree(d)
        rm += 1

# 2)(3) 参照の掃除
HREF = rf'''href=["'](?:\.\./|\./|/|https://shimulabo\.com/)*(?:sims/)?(?:{S})/(?:index\.html)?["']'''
A_RX = re.compile(rf'[ \t]*<a\b[^>]*{HREF}[^>]*>.*?</a>[ \t]*(?:\r?\n(?=[ \t]*\r?\n))?', re.S)
JS_RX = re.compile(rf"^[ \t]*\{{\s*href:\s*'(?:sims/)?(?:{S})/[^']*'[^\n]*\}},?[ \t]*\r?\n", re.M)
SKIP = ("scripts", "node_modules", ".git", "SEO", "note記事", "api")
changed = 0; left = []
for p in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    rel = os.path.relpath(p, ROOT)
    if rel.split(os.sep)[0] in SKIP: continue
    h = io.open(p, encoding="utf-8").read(); h0 = h
    h = A_RX.sub("", h)
    h = JS_RX.sub("", h)
    if h != h0:
        io.open(p, "w", encoding="utf-8", newline="").write(h); changed += 1
    if re.search(rf"sims/(?:{S})/", h) or re.search(rf'href="\.\./(?:{S})/"', h):
        left.append(rel)

# 4) 回数カウンター
cp = os.path.join(ROOT, "assets", "sim-counts.json")
J = json.load(io.open(cp, encoding="utf-8")); c = J["c"]; n0 = len(c)
for s in GONE: c.pop(s, None)
if len(c) != n0:
    io.open(cp, "w", encoding="utf-8").write(json.dumps(J, ensure_ascii=False, separators=(",", ":")))

# noindex_thin.txt から消したページを外す（noindex_thin.py の存在チェックで落ちないように）
np_ = os.path.join(HERE, "noindex_thin.txt")
lines = io.open(np_, encoding="utf-8").read().splitlines(True)
keep = [l for l in lines if l.strip() not in set(GONE)]
if len(keep) != len(lines): io.open(np_, "w", encoding="utf-8", newline="").write("".join(keep))

print(f"noindexリストから -{len(lines)-len(keep)}")
print(f"削除 {rm} 本（リスト {len(GONE)} 本）／参照を掃除したファイル {changed}／カウンター -{n0 - len(c)}")
if left: print("⚠ まだ参照が残っているファイル:", left[:20])

# 5) サイトマップ・llms.txt
sys.path.insert(0, HERE)
import build_sitemap; build_sitemap.main()
import runpy; runpy.run_path(os.path.join(HERE, "build_llms_txt.py"), run_name="__main__")
