# -*- coding: utf-8 -*-
"""IndexNow で、新しく作った・更新したページを Bing などにすぐ知らせる。

背景:
  検索流入の約75%が Bing（2026-10-03 GA4）。Bing はクロールを待つより、
  IndexNow で知らせたほうが新しいページの反映が早い。
  キーのファイル（サイト直下の <KEY>.txt）は公開されている前提（中身はキーそのもの）。

使い方（git push して Vercel のデプロイが終わってから実行する）:
  python scripts/indexnow.py              … 直前のコミットで変わったページだけ送る
  python scripts/indexnow.py --since REF  … REF 以降に変わったページを送る（例: --since HEAD~3）
  python scripts/indexnow.py --all        … サイトマップの全URLを送る（初回・大きく作り直したとき）
  python scripts/indexnow.py --dry-run    … 送らずに対象URLだけ表示
"""
import json, os, re, subprocess, sys, urllib.request, urllib.error

HOST = 'shimulabo.com'
KEY = '933a329ec8704289ac09bfb350ade738'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENDPOINT = 'https://api.indexnow.org/indexnow'
MEANING = {200: 'OK（受け付けました）', 202: '受け付けました（キーの確認待ち）', 400: 'リクエストの形式が不正',
           403: 'キーが確認できない（キーのファイルが公開されているか確認）', 422: 'URLがこのホストのものではない',
           429: '送りすぎ（時間をおいて再実行）'}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'indexnow-script'}), timeout=30) as r:
        return r.status, r.read().decode('utf-8', 'replace')


def changed_urls(since):
    out = subprocess.run(['git', '-C', ROOT, 'diff', '--name-only', since, 'HEAD'],
                         capture_output=True, text=True, encoding='utf-8', check=True).stdout
    urls = []
    for path in out.splitlines():
        path = path.strip().strip('"')
        if not path.endswith('index.html') or path.startswith(('scripts/', 'api/')):
            continue
        d = path[:-len('index.html')]
        urls.append(f'https://{HOST}/{d}')
    return sorted(set(urls))


def sitemap_urls():
    _, xml = get(f'https://{HOST}/sitemap.xml')
    return sorted(set(u.strip() for u in re.findall(r'<loc>(.*?)</loc>', xml)))


def main():
    args = sys.argv[1:]
    dry = '--dry-run' in args
    if '--all' in args:
        urls = sitemap_urls()
    else:
        since = args[args.index('--since') + 1] if '--since' in args else 'HEAD~1'
        urls = changed_urls(since)
    print(f'対象URL: {len(urls)}件')
    for u in urls[:10]: print('  ', u)
    if len(urls) > 10: print('   …')
    if not urls or dry:
        return
    # キーのファイルが本番で読めないと Bing 側で弾かれる（デプロイ前に実行していないかの確認）
    try:
        st, body = get(f'https://{HOST}/{KEY}.txt')
    except urllib.error.HTTPError as e:
        st, body = e.code, ''
    if st != 200 or body.strip() != KEY:
        sys.exit(f'キーのファイルが本番で確認できません（{st}）。デプロイが終わってから実行してください。')
    for i in range(0, len(urls), 10000):
        payload = json.dumps({'host': HOST, 'key': KEY, 'keyLocation': f'https://{HOST}/{KEY}.txt',
                              'urlList': urls[i:i + 10000]}).encode('utf-8')
        req = urllib.request.Request(ENDPOINT, data=payload, method='POST',
                                     headers={'Content-Type': 'application/json; charset=utf-8'})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                code = r.status
        except urllib.error.HTTPError as e:
            code = e.code
        print(f'送信 {len(urls[i:i + 10000])}件 → {code} {MEANING.get(code, "")}')


if __name__ == '__main__':
    main()
