"""scripts/noindex_thin.txt に書いたシミュに <meta name="robots" content="noindex,follow"> を入れる（2026-10-18）。
リストから消したページの noindex は外す。何度実行しても同じ結果。最後にサイトマップと llms.txt を作り直す。
生成元（gen_sims*.py）を再実行したページは meta が消えるので、このスクリプトをもう一度実行する。
使い方: python scripts/noindex_thin.py"""
import glob, io, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
TAG = '<meta name="robots" content="noindex,follow"><!-- noindex-thin -->'
want = {l.strip() for l in io.open(os.path.join(HERE, "noindex_thin.txt"), encoding="utf-8") if l.strip() and not l.startswith("#")}
add = rm = 0
for p in glob.glob(os.path.join(ROOT, "sims", "*", "index.html")):
    slug = os.path.basename(os.path.dirname(p))
    h = io.open(p, encoding="utf-8").read(); h0 = h
    if slug in want and TAG not in h:
        h = re.sub(r"(<meta charset=[^>]*>)", r"\1\n" + TAG, h, count=1)
        assert TAG in h, slug
        add += 1
    elif slug not in want and TAG in h:
        h = h.replace("\n" + TAG, "").replace(TAG, ""); rm += 1
    if h != h0:
        io.open(p, "w", encoding="utf-8", newline="").write(h)
missing = [s for s in want if not os.path.exists(os.path.join(ROOT, "sims", s, "index.html"))]
assert not missing, missing
print(f"noindex: 対象{len(want)}本（今回 +{add} / -{rm}）")
sys.path.insert(0, HERE)
import build_sitemap; build_sitemap.main()
import runpy; runpy.run_path(os.path.join(HERE, "build_llms_txt.py"), run_name="__main__")
