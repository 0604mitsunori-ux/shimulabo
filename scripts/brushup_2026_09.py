# -*- coding: utf-8 -*-
"""2026-09 ブラッシュアップ（冪等）
  1. fable10 系4ページの壊れた関連リンクを既存slugへ修正
  2. 初期3本(catchcopy / influencer-soroban / jutai) に FAQ + FAQPage 構造化データを追加
  3. api/share.js の ALLOW に未登録の sims を追加
  4. ふしぎ・現象／あそぶ・実験 31本の本文強化（enrich_wonder_play.py）
  ※ GA4 は add_ga.py G-R72MT9H7PT を別途実行
"""
import os, io, re, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def rd(p): return io.open(p, encoding='utf-8').read()
def wr(p, s): io.open(p, 'w', encoding='utf-8').write(s)

# 1. 壊れリンク
FIX = {
    'akuryoku-heikin': [('/sims/undo-calorie/', '/sims/shomou-undou/')],
    'bonus-heikin':    [('/sims/bonus-tsukaimichi/', '/sims/bonus-haibun/')],
    'dokushin-zei':    [('/sims/tedori/', '/sims/nenshu-tedori/')],
    'myakuhaku-heikin':[('/sims/shinpaku/', '/sims/shinpaku-zone/')],
}
for slug, pairs in FIX.items():
    p = os.path.join(ROOT, 'sims', slug, 'index.html'); s = rd(p); o = s
    for a, b in pairs:
        assert os.path.exists(os.path.join(ROOT, b.strip('/'), 'index.html')), b
        s = s.replace('href="' + a + '"', 'href="' + b + '"')
    if s != o: wr(p, s); print('link fixed:', slug)

# 2. 初期3本に FAQ
FAQS = {
 'catchcopy': [
   ('生成されたコピーを実際の広告に使っていい？', 'おすすめしません。本ツールは「盛りすぎ表現」をネタにしたジョークジェネレーターです。根拠のない最上級表現や効果の断定は、景品表示法・薬機法に抵触するおそれがあります。'),
   ('同じ商品名でも結果が変わるのはなぜ？', '型（テンプレート）と語彙の組み合わせをランダムに選んでいるためです。気に入った“うさんくささ”が出るまで何度でも生成できます。'),
   ('入力した商品名は送信される？', 'いいえ。生成はすべてブラウザ内で行われ、サーバーには何も送られません。')],
 'influencer-soroban': [
   ('フォロワー単価「約2.5円」の根拠は？', '国内のインフルエンサーマーケティングで慣習的に語られる「フォロワー数×2〜4円」の相場感を、わかりやすく1つの値に置いたものです。実際はジャンル・エンゲージメント率・投稿形式で数倍の幅があります。'),
   ('フォロワー1万人だと月収はいくら？', '本ツールの皮算用では1案件あたり約2.5万円。月2案件なら5万円、月5案件なら12.5万円です。「案件が継続的に来るか」が現実との最大の差になります。'),
   ('データは送信される？', 'いいえ。計算はすべてブラウザ内で完結します。')],
 'jutai': [
   ('自然渋滞はどのくらいの密度で起きる？', '高速道路では1車線あたり1kmに約25台（車間およそ40m）を超えたあたりから、わずかなブレーキが後方へ増幅して伝わり始めるとされます。本シミュレーターでも混雑度を上げるとこの状態が再現されます。'),
   ('渋滞の波はなぜ後ろへ動く？', '各車は「前の車が減速してから」減速するため、減速の起点が1台ずつ後ろへずれていきます。実際の高速道路でも渋滞の波は時速約20kmで後方へ進むことが観測されています。'),
   ('データは送信される？', 'いいえ。すべてブラウザ内で動作します。')],
}
for slug, faqs in FAQS.items():
    p = os.path.join(ROOT, 'sims', slug, 'index.html'); s = rd(p)
    if 'FAQPage' in s: continue
    dl = '<h2>よくある質問</h2><dl class="faq">' + ''.join('<dt>%s</dt><dd>%s</dd>' % (q, a) for q, a in faqs) + '</dl>\n  '
    i = s.index('</article>')
    s = s[:i] + dl + s[i:]
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}, ensure_ascii=False)
    s = s.replace('</head>', '    <script type="application/ld+json">' + ld + '</script>\n</head>', 1)
    wr(p, s); print('faq added:', slug)

# 3. ALLOW 同期
sh = os.path.join(ROOT, 'api', 'share.js'); s = rd(sh)
head, rest = s.split('const ALLOW = new Set([', 1)
body, tail = rest.split(']);', 1)
allow = set(re.findall(r"'([a-z0-9\-]+)'", body))
sims = sorted(d for d in os.listdir(os.path.join(ROOT, 'sims')) if os.path.exists(os.path.join(ROOT, 'sims', d, 'index.html')))
missing = [x for x in sims if x not in allow]
if missing:
    add = '\n  // 2026-09 同期追加\n' + '\n'.join('  ' + ', '.join("'%s'" % x for x in missing[i:i+6]) + ',' for i in range(0, len(missing), 6)) + '\n'
    s = head + 'const ALLOW = new Set([' + body.rstrip() + add + ']);' + tail
    wr(sh, s); print('ALLOW +%d' % len(missing))

# 4. 本文強化
import enrich_wonder_play
enrich_wonder_play.apply()
print('brushup done')
