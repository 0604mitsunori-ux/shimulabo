# -*- coding: utf-8 -*-
"""診断系シミュの本文に「結果タイプ一覧」表を追加する（各ページ固有・冪等）。

背景:
  診断ページ457本の本文が300字未満と薄かった。
  ただし定型文を足すのは重複コンテンツになるだけで意味がない。
  これらのページは判定ロジックとして
      const B = [[しきい値, "タイプ名", "説明"], ...]
  を自分自身のJS内に持っているので、それを読み取って
  「この診断で判定される全タイプの一覧」を表にする。
  → 事実に基づき、ページごとに内容が異なる、ユーザーにも有用な追記になる。

使い方: python scripts/enrich_types_table.py [--dry]
"""
import os, io, re, sys, glob, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = '<!-- types-table -->'
DRY = '--dry' in sys.argv

# const B=[[4,"名前","説明"],...]  を拾う（変数名はB以外も許容）
BAND_RE = re.compile(r'(?:const|var|let)\s+(?:B|BANDS|RES)\s*=\s*(\[\s*\[.*?\]\s*\])\s*[;,]', re.S)


def parse_bands(js_array_text):
    """JSの配列リテラルをJSONとして読む。読めない形なら None"""
    try:
        data = json.loads(js_array_text)
    except Exception:
        return None
    rows = []
    for item in data:
        if not isinstance(item, list) or len(item) < 2:
            return None
        # 実在する3形式に対応する
        #   [しきい値, 名前, 説明]            … dq() 系
        #   [しきい値, 絵文字, 名前, 説明]    … anger-type 等
        #   [絵文字, 名前, 説明]              … 占い系（seed_sim）
        if isinstance(item[0], (int, float)):
            if len(item) >= 4:
                emoji, name, desc = str(item[1]), item[2], item[3]
            else:
                emoji, name, desc = '', item[1], (item[2] if len(item) > 2 else '')
        else:
            emoji = str(item[0])
            name = item[1] if len(item) > 1 else ''
            desc = item[2] if len(item) > 2 else ''
        if not isinstance(name, str) or not isinstance(desc, str):
            return None
        if not name.strip():
            return None
        rows.append((emoji, name.strip(), desc.strip()))
    # タイプが少なすぎ/多すぎるものは対象外
    if not (2 <= len(rows) <= 10):
        return None
    return rows


def build_table(rows, h1):
    n = len(rows)
    head = ('    ' + MARK + '\n'
            '    <h2>この診断で判定される{n}タイプ</h2>\n'
            '    <p>「{h1}」では、回答の内容におうじて次の{n}タイプのいずれかを判定します。'
            '自分がどのタイプになるか、また他にどんなタイプがあるのかを先に見ておくと、結果が読み取りやすくなります。</p>\n'
            ).format(n=n, h1=h1)
    body = ['    <div class="tbl-scroll">\n    <table class="seo-table">\n'
            '    <tr><th>タイプ</th><th>どんなタイプ？</th></tr>\n']
    for emoji, name, desc in rows:
        label = (emoji + ' ' + name).strip()
        body.append('    <tr><td>%s</td><td>%s</td></tr>\n' % (label, desc or '—'))
    body.append('    </table>\n    </div>\n')
    return head + ''.join(body)


def main():
    hit = skip_mark = skip_nob = 0
    changed = []
    for p in sorted(glob.glob(os.path.join(ROOT, 'sims', '*', 'index.html'))):
        slug = os.path.basename(os.path.dirname(p))
        html = io.open(p, encoding='utf-8').read()
        if MARK in html:
            skip_mark += 1
            continue
        m = BAND_RE.search(html)
        if not m:
            skip_nob += 1
            continue
        rows = parse_bands(m.group(1))
        if not rows:
            skip_nob += 1
            continue
        h1m = re.search(r'<h1>(.*?)</h1>', html, re.S)
        h1 = re.sub(r'<[^>]+>', '', h1m.group(1)).strip() if h1m else slug
        # 本文の「よくある質問」の直前に入れる（無ければ </article> の直前）
        table = build_table(rows, h1)
        anchor = '    <h2>よくある質問</h2>'
        if anchor in html:
            html = html.replace(anchor, table + anchor, 1)
        elif '<h2>よくある質問</h2>' in html:
            html = html.replace('<h2>よくある質問</h2>', table + '<h2>よくある質問</h2>', 1)
        elif '  </article>' in html:
            html = html.replace('  </article>', table + '  </article>', 1)
        else:
            skip_nob += 1
            continue
        hit += 1
        changed.append(slug)
        if not DRY:
            io.open(p, 'w', encoding='utf-8').write(html)
    print('対象 %d本に「結果タイプ一覧」を追加%s / 既適用 %d / 非対象 %d'
          % (hit, '（DRY RUN）' if DRY else '', skip_mark, skip_nob))
    print('例:', ', '.join(changed[:12]))


if __name__ == '__main__':
    main()
