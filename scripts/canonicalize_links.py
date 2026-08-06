# -*- coding: utf-8 -*-
"""内部リンクを canonical 形（ディレクトリ形式）に統一し、CSS/JSにバージョンを付与する。

背景:
  canonical と sitemap は https://shimulabo.com/sims/<slug>/ 形式なのに、
  トップの763本を含む内部リンクは <slug>/index.html を指しており、
  「内部リンクが全部 canonical と別URL」という状態だった。
  クロール効率・リンク評価の集約の面で損なので、ディレクトリ形式へ統一する。

  あわせて style.css / result-fx.js 等に ?v= を付ける。
  （付けないと、デザイン刷新が既存訪問者のブラウザキャッシュで反映されないため）

冪等。何度実行しても同じ結果になる。
"""
import os, io, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSET_VER = sys.argv[1] if len(sys.argv) > 1 else '3'

# バージョンを付けるアセット
ASSETS = ('style.css', 'result-fx.js', 'lang-toggle.js', 'share-counter.js', 'vote.js')

# index.html を落としてディレクトリ形式にする対象ディレクトリ
DIRS = ('sims', 'request', 'board', 'contact', 'privacy', 'terms', 'en')

link_pat = re.compile(r'(href=")([^"]*?)(index\.html)(")')


def fix_links(html):
    """href の末尾 index.html を落とす（外部URL・アンカー付きは対象外）"""
    def rep(m):
        pre, path, _idx, post = m.group(1), m.group(2), m.group(3), m.group(4)
        if path.startswith(('http://', 'https://', '//', 'mailto:')):
            return m.group(0)
        # 末尾が index.html で終わるものだけ（?や#付きは触らない）
        return pre + path + post
    return link_pat.sub(rep, html)


def fix_assets(html):
    """assets/xxx.css → assets/xxx.css?v=N （既存の ?v= は付け替え）"""
    for a in ASSETS:
        name, ext = a.rsplit('.', 1)
        # 既存バージョンを一旦除去してから付け直す（冪等性の担保）
        html = re.sub(r'(assets/' + re.escape(name) + r'\.' + ext + r')\?v=[^"\'\s>]*', r'\1', html)
        html = re.sub(r'(assets/' + re.escape(name) + r'\.' + ext + r')(?=["\'])', r'\1?v=' + ASSET_VER, html)
    return html


def targets():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        skip = ('.git', 'scripts', 'ogp', 'node_modules', 'SEO', 'note記事')
        if any(('/' + s) in dirpath.replace('\\', '/') or dirpath.replace('\\', '/').endswith('/' + s) for s in skip):
            continue
        for fn in filenames:
            if fn.endswith('.html'):
                yield os.path.join(dirpath, fn)


def main():
    n_files = n_links = 0
    for p in targets():
        html = io.open(p, encoding='utf-8').read()
        before = html
        before_links = len(link_pat.findall(html))
        html = fix_links(html)
        html = fix_assets(html)
        if html != before:
            io.open(p, 'w', encoding='utf-8').write(html)
            n_files += 1
            n_links += before_links
    print('rewrote %d files / %d index.html links canonicalized / asset ver=%s' % (n_files, n_links, ASSET_VER))


if __name__ == '__main__':
    main()
