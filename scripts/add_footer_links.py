"""全ページのフッターに「運営者情報・プライバシーポリシー・お問い合わせ」のリンクを入れる（2026-11-17・冪等）。
gen_sims*.py で作り直したページは消えるので、もう一度実行する。使い方: python scripts/add_footer_links.py"""
import glob, io, os, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = "<!-- footer-links -->"
COPY = '<p style="margin-top:10px;opacity:.7">© 2026 シミュラボ</p>'
n = 0
for p in glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True):
    rel = os.path.relpath(p, ROOT)
    if rel.split(os.sep)[0] in ("scripts", "node_modules", ".git", "SEO", "note記事") or rel == "index.html": continue
    h = io.open(p, encoding="utf-8").read()
    if MARK in h or COPY not in h: continue
    up = "../" * (rel.count(os.sep))
    links = (f'<p style="margin-top:8px;font-size:.85em">{MARK}<a href="{up}about/">運営者情報</a>　'
             f'<a href="{up}privacy/">プライバシーポリシー</a>　<a href="{up}terms/">利用規約</a>　<a href="{up}contact/">お問い合わせ</a></p>\n    ')
    h = h.replace(COPY, links + COPY, 1)
    io.open(p, "w", encoding="utf-8", newline="").write(h); n += 1
# トップ
p = os.path.join(ROOT, "index.html"); h = io.open(p, encoding="utf-8").read()
if 'href="about/"' not in h:
    h = h.replace('      <a href="privacy/">プライバシーポリシー</a>\n', '      <a href="privacy/">プライバシーポリシー</a>\n      <a href="about/">運営者情報</a>\n', 1)
    assert 'href="about/"' in h
    io.open(p, "w", encoding="utf-8", newline="").write(h); n += 1
print("footer-links:", n)
