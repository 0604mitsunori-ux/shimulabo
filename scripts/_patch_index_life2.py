# -*- coding: utf-8 -*-
"""index.html へ 浮気・調査10本(tantei)＋子ども学習10本(kidedu)のカード＋ランキング＋本数(479→499)を挿入（冪等）。"""
import os, io, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_sims_tantei, gen_sims_kidedu
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'index.html')

GRAD = {'tantei':'linear-gradient(135deg,#f1f5f9,#e2e8f0)', 'kidedu':'linear-gradient(135deg,#eff6ff,#ecfeff)'}
LABEL = {'tantei':'浮気・調査・離婚', 'kidedu':'子どもの学習・英語'}
CARD = {
  'uwaki-do':('浮気度チェック','相手の浮気の可能性を診断'),
  'uwaki-sign':('浮気のサイン診断','どのタイプのサインが出てる？'),
  'isharyo-furin':('不倫・浮気の慰謝料シミュ','慰謝料の相場の目安はいくら？'),
  'tantei-hiyou':('浮気調査・探偵費用シミュ','調査費用の目安はいくら？'),
  'youikuhi':('養育費シミュレーター','毎月いくら？相場の目安'),
  'zaisan-bunyo':('財産分与シミュレーター','離婚でいくら分ける？原則1/2'),
  'shouko-check':('浮気の証拠 充足度チェック','証拠は足りてる？調査すべき？'),
  'shinrai-do':('パートナー信頼度診断','二人の信頼関係は何点？'),
  'kentaiki':('倦怠期度診断','二人の倦怠期はどれくらい？'),
  'uwaki-nayami':('浮気の悩み どうすべき診断','問い詰める？証拠？相談？'),
  'kid-eigo-type':('子どもの英語学習タイプ診断','わが子に合う英語の学び方は？'),
  'kid-eigo-itsukara':('子どもの英語いつから？診断','わが家の英語の始めどきは'),
  'kid-tablet-muki':('タブレット学習 向いてる？診断','わが子の適性をチェック'),
  'kid-gakushu-type':('子どもの学習タイプ診断','合う勉強のさせ方は？'),
  'kid-yaruki':('子どもの勉強やる気診断','わが子のやる気は何点？'),
  'kid-kyozai-hiyou':('子どもの通信教育 費用比較シミュ','月いくら？タブレット/英会話/塾'),
  'kid-eigomimi':('子どもの英語耳 育て度チェック','わが子の英語耳は育ってる？'),
  'kid-jitaku':('子どもの自宅学習 習慣度診断','家庭学習は身についてる？'),
  'kid-gakushu-jikan':('家庭学習時間の目安シミュ','学年別に1日どれくらい？'),
  'kid-naraigoto':('子どもに合う習い事診断','わが子にぴったりの習い事は？'),
}
SCORE = {'uwaki-do':70,'uwaki-sign':66,'isharyo-furin':72,'tantei-hiyou':70,'youikuhi':69,'zaisan-bunyo':65,
  'shouko-check':64,'shinrai-do':63,'kentaiki':64,'uwaki-nayami':62,
  'kid-eigo-type':70,'kid-eigo-itsukara':66,'kid-tablet-muki':71,'kid-gakushu-type':65,'kid-yaruki':66,
  'kid-kyozai-hiyou':67,'kid-eigomimi':63,'kid-jitaku':62,'kid-gakushu-jikan':65,'kid-naraigoto':64}

DATA=[]
for s in gen_sims_tantei.SIMS: DATA.append((s['id'],'tantei',s['emoji']))
for s in gen_sims_kidedu.SIMS: DATA.append((s['id'],'kidedu',s['emoji']))

with io.open(IDX, encoding='utf-8') as f: html = f.read()
assert 'sims/uwaki-do/index.html' not in html, '既に挿入済み（中止）'

cards=[]
for sid,slug,emoji in DATA:
    h3,desc=CARD[sid]
    cards.append(f'''    <a class="sim-card" data-cat="{slug}" href="sims/{sid}/index.html">
      <div class="thumb" style="background:{GRAD[slug]}"><span class="emoji">{emoji}</span></div>
      <div class="body"><div class="cat">{LABEL[slug]}</div><h3>{h3}</h3><p>{desc}</p><span class="go">触ってみる →</span></div>
    </a>
''')
marker='    <a class="req-card" href="request/index.html">'
assert marker in html
html=html.replace(marker, ('\n'.join(cards)+'\n')+marker, 1)

rank=[]
for sid,slug,emoji in DATA:
    h3,_=CARD[sid]
    rank.append(f"    {{ href: 'sims/{sid}/index.html', emoji: '{emoji}', title: '{h3}', cat: '{LABEL[slug]}', score: {SCORE[sid]} }}")
idx=html.index('\n  ];')
before=html[:idx].rstrip()
if not before.endswith(','): before+=','
html=before+'\n'+',\n'.join(rank)+html[idx:]

assert '<b>479</b>本 公開中' in html
html=html.replace('<b>479</b>本 公開中','<b>499</b>本 公開中',1)
with io.open(IDX,'w',encoding='utf-8') as f: f.write(html)
print(f'patched index.html: +{len(DATA)} cards, +{len(DATA)} ranking, count=499')
