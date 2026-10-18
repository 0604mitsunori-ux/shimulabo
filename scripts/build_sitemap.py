"""sitemap.xml を作り直す（2026-10-18）。何度実行しても同じ結果。
  - URL はファイルから拾う（/ ・ /sims/*/ ・ /rika/ /lab/ /live/ などの直下ページ・ /en/）。
    以前の seo_internal.py は自分の SIMS 一覧だけで作っていたため、/rika/ /lab/ /live/ やラボ・API系・理科シミュが落ちていた。
  - <lastmod> は git の最終コミット日（作業ツリーで変更中のファイルは今日）。
    以前はファイルの更新時刻だったため、git で取り出した日付（8/6 など）のまま、改善したページも更新日が動かなかった。
  - noindex のページは載せない。
使い方: python scripts/build_sitemap.py   （seo_internal.py の最後からも呼ばれる）
"""
import os, re, subprocess, sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://shimulabo.com"
SKIP_DIRS = {"sims", "en", "scripts", "api", "assets", "ogp", "SEO", "note記事", "node_modules", ".git", ".vercel", ".claude"}


def git(*args):
    return subprocess.run(["git", "-c", "core.quotepath=false", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8").stdout


def commit_dates():
    """パス → 最終コミット日（YYYY-MM-DD）。履歴を新しい順に1回なめて最初に出た日付を採る。"""
    out, cur = {}, None
    for line in git("log", "--format=@%cs", "--name-only").splitlines():
        if line.startswith("@"):
            cur = line[1:]
        elif line and line not in out:
            out[line] = cur
    return out


def dirty():
    s = set()
    for line in git("status", "--porcelain", "--untracked-files=all").splitlines():
        p = line[3:].strip().strip('"')
        if " -> " in p: p = p.split(" -> ")[1]
        s.add(p)
    return s


def pages():
    """(URLパス, リポジトリ内の相対パス)"""
    out = [("/", "index.html")]
    for d in sorted(os.listdir(ROOT)):
        if d in SKIP_DIRS or d.startswith("."): continue
        if os.path.isfile(os.path.join(ROOT, d, "index.html")):
            out.append((f"/{d}/", f"{d}/index.html"))
    for sid in sorted(os.listdir(os.path.join(ROOT, "sims"))):
        if os.path.isfile(os.path.join(ROOT, "sims", sid, "index.html")):
            out.append((f"/sims/{sid}/", f"sims/{sid}/index.html"))
    return out


def en_pages():
    out = []
    if os.path.isfile(os.path.join(ROOT, "en", "index.html")):
        out.append(("/en/", "en/index.html"))
    d = os.path.join(ROOT, "en", "sims")
    if os.path.isdir(d):
        for sid in sorted(os.listdir(d)):
            if os.path.isfile(os.path.join(d, sid, "index.html")):
                out.append((f"/en/sims/{sid}/", f"en/sims/{sid}/index.html"))
    return out


def noindex(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        head = f.read(6000)
    return re.search(r'<meta[^>]+name="robots"[^>]+noindex', head) is not None


def images(u):
    """ページの図（scripts/build_figs.py が作る sims/<slug>/<slug>-<n>.png）を画像サイトマップに載せる（2026-10-18）"""
    if not u.startswith("/sims/"): return ""
    slug = u.split("/")[2]; d = os.path.join(ROOT, "sims", slug)
    pngs = sorted((f for f in os.listdir(d) if re.fullmatch(re.escape(slug) + r"-\d+\.png", f)), key=lambda f: int(f[len(slug) + 1:-4]))
    return "".join(f"<image:image><image:loc>{BASE}{u}{f}</image:loc></image:image>" for f in pngs)


def alt(ja, en):
    return (f'<xhtml:link rel="alternate" hreflang="ja" href="{BASE}{ja}"/>'
            f'<xhtml:link rel="alternate" hreflang="en" href="{BASE}{en}"/>'
            f'<xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{ja}"/>')


def main():
    dates, changed, today = commit_dates(), dirty(), date.today().isoformat()
    lm = lambda rel: today if rel in changed else dates.get(rel, today)
    ja, en = pages(), en_pages()
    en_set = {u for u, _ in en}
    rows = []
    for u, rel in ja:
        if noindex(rel): continue
        pr = "1.0" if u == "/" else "0.9" if u in ("/rika/", "/lab/", "/live/") else "0.8" if u.startswith("/sims/") else "0.5"
        a = ""
        if u == "/" and "/en/" in en_set: a = alt("/", "/en/")
        elif u.startswith("/sims/") and "/en" + u in en_set: a = alt(u, "/en" + u)
        rows.append(f"  <url><loc>{BASE}{u}</loc><lastmod>{lm(rel)}</lastmod>{a}{images(u)}<changefreq>weekly</changefreq><priority>{pr}</priority></url>")
    for u, rel in en:
        if noindex(rel): continue
        ja_u = "/" if u == "/en/" else u[3:]
        rows.append(f"  <url><loc>{BASE}{u}</loc><lastmod>{lm(rel)}</lastmod>{alt(ja_u, u)}<changefreq>weekly</changefreq><priority>{'0.9' if u == '/en/' else '0.8'}</priority></url>")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
           + "\n".join(rows) + "\n</urlset>\n")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
        f.write(xml)
    print(f"sitemap.xml: {len(rows)} URL")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
