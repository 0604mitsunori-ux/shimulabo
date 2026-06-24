# -*- coding: utf-8 -*-
"""index.html へ 便利ツール第2弾10＋脳トレ第2弾10のカード＋ランキング＋本数(426→446)を一括挿入（冪等）。
既存カテゴリ tool/brain に追加（CATS/GROUPS変更なし）。"""
import os, io, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_sims_tool2, gen_sims_brain2

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')

GRAD = {'tool':'linear-gradient(135deg,#eff6ff,#e0f2fe)', 'brain':'linear-gradient(135deg,#f0fdfa,#ccfbf1)'}
LABEL = {'tool':'便利ツール', 'brain':'脳トレ・診断テスト'}

CARD = {
  # 便利ツール2
  'soinsu-bunkai':   ('素因数分解ツール','数を素数の積に分解。約数の個数も。',68),
  'password-gen':    ('パスワード生成','安全で強いランダムパスワードを作成。',71),
  'koubaisu-yakusu': ('最小公倍数・最大公約数','2〜3つの数のLCM・GCDを計算。',64),
  'ondo-henkan':     ('温度変換','摂氏・華氏・ケルビンを相互変換。',66),
  'aspect-keisan':   ('アスペクト比計算','縦横比を求める・サイズを比から計算。',65),
  'romaji-henkan':   ('ローマ字変換','ひらがな・カタカナをローマ字に。',67),
  'heikin-keisan':   ('平均値計算','平均・合計・中央値をまとめて計算。',63),
  'jikyu-keisan':    ('時給計算機','時給から日給・月収・年収を計算。',69),
  'zenkaku-hankaku': ('全角・半角変換','英数字・記号・カナを一括変換。',62),
  'menseki-keisan':  ('面積計算ツール','円・三角形・台形などの面積を計算。',61),
  # 脳トレ2
  'naikou-gaikou':   ('内向型・外向型診断','あなたはどっち？12問でチェック。',70),
  'negative-shikou': ('ネガティブ思考度診断','考えすぎ・マイナス思考をチェック。',64),
  'smartphone-izon': ('スマホ依存度診断','あなたのスマホ依存をセルフチェック。',69),
  'rakkan-hikan':    ('楽観・悲観度診断','あなたはどっち寄り？10問チェック。',63),
  'kyoukan-ryoku':   ('共感力診断（エンパス度）','人の気持ちがわかる力をチェック。',65),
  'kichoumen-zubora':('几帳面・ズボラ度診断','きっちり？おおざっぱ？をチェック。',62),
  'ankan-flash':     ('フラッシュ暗算ゲーム','次々現れる数を足す脳トレ。何個まで？',72),
  'doutai-shiryoku': ('動体視力テスト','一瞬の数字を読み取れる？',67),
  'keisanryoku':     ('計算力テスト','1分間で何問解ける？暗算スピード。',66),
  'chuuiryoku':      ('注意力テスト','1から順にタッチ！集中力チェック。',64),
}

DATA = []
for s in gen_sims_tool2.SIMS:
    DATA.append((s['id'], 'tool', s['emoji'], CARD[s['id']][0], CARD[s['id']][1], CARD[s['id']][2]))
for s in gen_sims_brain2.SIMS:
    DATA.append((s['id'], 'brain', s['emoji'], CARD[s['id']][0], CARD[s['id']][1], CARD[s['id']][2]))

with io.open(IDX, encoding='utf-8') as f:
    html = f.read()

assert 'sims/soinsu-bunkai/index.html' not in html, '既に挿入済みのようです（中止）'

cards = []
for sid, slug, emoji, h3, desc, score in DATA:
    cards.append(
f'''    <a class="sim-card" data-cat="{slug}" href="sims/{sid}/index.html">
      <div class="thumb" style="background:{GRAD[slug]}"><span class="emoji">{emoji}</span></div>
      <div class="body"><div class="cat">{LABEL[slug]}</div><h3>{h3}</h3><p>{desc}</p><span class="go">触ってみる →</span></div>
    </a>
''')
marker = '    <a class="req-card" href="request/index.html">'
assert marker in html
html = html.replace(marker, ('\n'.join(cards) + '\n') + marker, 1)

rank = []
for sid, slug, emoji, h3, desc, score in DATA:
    rank.append(f"    {{ href: 'sims/{sid}/index.html', emoji: '{emoji}', title: '{h3}', cat: '{LABEL[slug]}', score: {score} }}")
idx = html.index('\n  ];')
before = html[:idx].rstrip()
if not before.endswith(','):
    before += ','
html = before + '\n' + ',\n'.join(rank) + html[idx:]

assert '<b>426</b>本 公開中' in html, '本数マーカー(426)が見つかりません'
html = html.replace('<b>426</b>本 公開中', '<b>446</b>本 公開中', 1)

with io.open(IDX, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'patched index.html: +{len(DATA)} cards, +{len(DATA)} ranking, count=446')
