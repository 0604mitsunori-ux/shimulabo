# -*- coding: utf-8 -*-
"""シミュラボ：追加10本（計算4＋診断6・重複なし）。write_all＋dq()ヘルパー。CTAなしカテゴリ。"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq, write_all

WORK='仕事・働き方'; BIZ='店舗・ビジネス'; MONEY='お金・時間'; FIN='マネー・保険・不動産'
MENTAL='メンタル・自己分析'; OSHI='推し活・エンタメ'; SPORTS='スポーツ・運動'
SIMS=[]
def add(**k): SIMS.append(k)
def C(t): return '<div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：'+t+'</div>'
def REF(items): return '<h2>参考</h2><ul class="seo-refs">'+''.join('<li>'+i+'</li>' for i in items)+'</ul>'
def J(s): return json.dumps(s, ensure_ascii=False)

def dq(id, cat, emoji, title, desc, ogt, ogd, h1, lead, qs, bands, intro, types_label, faqs, refs, share_pre):
    inp = '    <h2>'+emoji+' 質問に答えてね</h2>\n'
    for i,(q,opts) in enumerate(qs):
        o = ''.join('<option value="%d">%s</option>' % (s, l) for l,s in opts)
        inp += '    <div class="field"><label>%s</label><select id="q%d">%s</select></div>\n' % (q, i, o)
    inp += '    <button class="btn btn-primary" id="calcBtn">診断する</button>'
    res = ('      <div class="seo-anim ptag-stage" id="stg"><div class="pop-emoji" id="ico">'+emoji+'''</div></div>
      <div class="label">あなたのタイプは</div>
      <div class="big" style="font-size:30px"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:16px">—</div>''')
    bandjs = ','.join('[%d,%s,%s]' % (b[0], J(b[1]), J(b[2])) for b in bands)
    js = ('  const B=['+bandjs+'''];
  function calc(){let s=0; const n='''+str(len(qs))+'''; for(let i=0;i<n;i++)s+=(+$('q'+i).value||0);
    let t=B[B.length-1]; for(const b of B){ if(s<=b[0]){ t=b; break; } }
    $('big').textContent=t[1]; $('sub').textContent='スコア '+s+'点';
    $('adv').innerHTML='<strong>'+t[1]+'</strong><br>'+t[2];
    const ic=$('ico'); ic.classList.remove('on'); void ic.offsetWidth; ic.classList.add('on');
    show(); SHARE='''+J(share_pre)+'''+t[1]+'でした'+'''+J(emoji)+''';}''')
    article = (C(intro) + '\n    <h2>診断でわかるタイプ</h2>\n    <p>'+types_label+'</p>\n    <div class="note">回答を点数化して傾向を判定するエンタメ診断です。気軽に楽しんでください。</div>\n    <h2>よくある質問</h2>' + faq(faqs) + REF(refs))
    add(id=id, cat=cat, emoji=emoji, title=title, desc=desc, ogtitle=ogt, ogdesc=ogd, h1=h1, lead=lead, inputs=inp, result=res, article=article, js=js)

# ===================== 計算 4本 =====================

add(id='kyuryo-tedori', cat=WORK, emoji='💴',
  title='給料 手取り 計算｜月給からの手取りはいくら？｜シミュラボ',
  desc='額面の月給と年齢から、社会保険・税を引いた毎月の手取り額の目安を計算する無料シミュレーター。',
  ogtitle='給料 手取り 計算｜月給からの手取りは？', ogdesc='額面月給から手取り額・社会保険・税の目安を計算。',
  h1='給料 手取り 計算シミュレーター',
  lead='額面の月給から、実際にもらえる手取りはいくら？社会保険と税を引いた毎月の手取りの目安を計算します（独身・概算）。',
  inputs='''    <h2>💴 条件を入れる</h2>
    <div class="row"><div class="field"><label>額面の月給 <span class="hint">（万円）</span></label><input type="number" id="g" value="25" min="0" inputmode="numeric"></div>
    <div class="field"><label>年齢</label><select id="age"><option value="0" selected>40歳未満</option><option value="1">40〜64歳（介護あり）</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">手取りを計算する</button>''',
  result='''      <div class="label">毎月の手取り（目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">社会保険料</div><div class="v" id="sha">—</div></div>
      <div class="stat"><div class="k">税(概算)</div><div class="v" id="zei">—</div></div>
      <div class="stat"><div class="k">手取り率</div><div class="v accent" id="rate">—</div></div></div>''',
  article=C('手取りは額面の <b>約75〜85%</b>。社会保険料（約15%）と所得税・住民税が引かれます。月給が高いほど手取り率は下がります。')+'''
    <h2>給料の手取りの内訳</h2>
    <p>額面（総支給）から、健康保険・厚生年金・雇用保険（40歳以上は介護保険も）と、所得税・住民税が差し引かれた残りが「手取り」です。社会保険料だけで約15%引かれます。</p>
    <div class="note"><strong>概算の考え方</strong><br>社会保険料 ＝ 月給 × 約15%（40歳以上は＋約0.9%）<br>手取り ≒ 月給 ×（0.76〜0.83／月給帯で変動）</div>
    <h2>月給別の手取りの目安</h2>
    <table class="seo-table"><tr><th>額面月給</th><th>手取りの目安</th></tr>
    <tr><td>20万円</td><td>約16.4万円</td></tr><tr><td>25万円</td><td>約20.3万円</td></tr>
    <tr><td>30万円</td><td>約23.7万円</td></tr><tr><td>40万円</td><td>約31万円</td></tr></table>
    <h2>よくある質問</h2>'''+faq([('ボーナスの手取りは？','賞与も社会保険・税が引かれ、手取りは額面の約8割が目安です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['国税庁・日本年金機構 各種料率']),
  js='''  function calc(){const g=Math.max(0,+$('g').value||0)*10000,kaigo=$('age').value==='1';
    const sha=g*(0.15+(kaigo?0.009:0)); let r; if(g<250000)r=0.83;else if(g<350000)r=0.81;else if(g<500000)r=0.79;else r=0.76;
    const net=g*r, zei=Math.max(0,g-sha-net);
    $('sub').textContent=`額面月給${num(g/10000)}万円・${kaigo?'40〜64歳':'40歳未満'}`;
    $('sha').textContent=yen(sha);$('zei').textContent=yen(zei);$('rate').textContent=Math.round(r*100)+'%';
    show();anim($('big'),0,net,800);
    SHARE=`給料手取りシミュ、月給${num(g/10000)}万円→手取り 約${yen(net)}（${Math.round(r*100)}%）でした💴`;}''')

add(id='riekiritsu', cat=BIZ, emoji='📈',
  title='利益率 計算｜売価と原価から粗利率・原価率・値入率を計算｜シミュラボ',
  desc='売価と原価から、粗利益・利益率（粗利率）・原価率・値入率を一発で計算する無料ツール。物販・飲食の価格設定に。',
  ogtitle='利益率 計算｜粗利率・原価率は？', ogdesc='売価と原価から粗利率・原価率・値入率を計算。',
  h1='利益率 計算ツール',
  lead='売価と原価を入れるだけで、粗利益・利益率（粗利率）・原価率・値入率を一発計算。価格設定や仕入れ判断に。',
  inputs='''    <h2>📈 条件を入れる</h2>
    <div class="row"><div class="field"><label>売価（販売価格） <span class="hint">（円）</span></label><input type="number" id="p" value="1000" min="0" inputmode="numeric"></div>
    <div class="field"><label>原価（仕入れ） <span class="hint">（円）</span></label><input type="number" id="c" value="400" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">利益率を計算する</button>''',
  result='''      <div class="label">利益率（粗利率・対売価）</div>
      <div class="big"><span id="big">0</span><span class="unit">%</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">粗利益</div><div class="v accent" id="gross">—</div></div>
      <div class="stat"><div class="k">原価率</div><div class="v" id="genka">—</div></div>
      <div class="stat"><div class="k">値入率(対原価)</div><div class="v" id="neire">—</div></div></div>''',
  article=C('利益率（粗利率）＝ <b>粗利益 ÷ 売価 × 100</b>。原価率＝原価÷売価。値入率は原価に対する利益の割合で、利益率とは別物です。')+'''
    <h2>利益率・原価率・値入率の違い</h2>
    <p>同じ「もうけ」でも、何を基準にするかで率が変わります。利益率（粗利率）は売価基準、値入率は原価基準。混同すると価格設定を誤るので注意。</p>
    <div class="note"><strong>計算式</strong><br>粗利益 ＝ 売価 − 原価<br>利益率(粗利率) ＝ 粗利益 ÷ 売価 ×100<br>原価率 ＝ 原価 ÷ 売価 ×100<br>値入率 ＝ 粗利益 ÷ 原価 ×100</div>
    <h2>業種別の原価率の目安</h2>
    <table class="seo-table"><tr><th>業種</th><th>原価率の目安</th></tr>
    <tr><td>飲食店</td><td>30%前後</td></tr><tr><td>小売（物販）</td><td>50〜70%</td></tr><tr><td>カフェ・ドリンク</td><td>10〜20%</td></tr></table>
    <h2>よくある質問</h2>'''+faq([('利益率30%にするには？','売価の30%が粗利になる価格設定＝原価率70%。原価÷0.7が売価の目安です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['原価管理・価格設定の基礎']),
  js='''  function calc(){const p=Math.max(0,+$('p').value||0),c=Math.max(0,+$('c').value||0);
    const gross=p-c, rate=p>0?gross/p*100:0, genka=p>0?c/p*100:0, neire=c>0?gross/c*100:0;
    $('sub').textContent=`売価${num(p)}円・原価${num(c)}円`;
    $('gross').textContent=yen(gross);$('genka').textContent=genka.toFixed(1)+'%';$('neire').textContent=neire.toFixed(1)+'%';
    show();anim($('big'),0,rate,800,1);
    SHARE=`利益率シミュ、売価${num(p)}円・原価${num(c)}円→利益率${rate.toFixed(1)}%（粗利${yen(gross)}）でした📈`;}''')

add(id='kinmu-jikan', cat=WORK, emoji='⏰',
  title='勤務時間 計算｜出勤・退勤・休憩から実働時間を計算｜シミュラボ',
  desc='出勤時刻・退勤時刻・休憩時間から、実働時間と残業時間（8時間超）を計算する無料ツール。勤怠・タイムカードの確認に。',
  ogtitle='勤務時間 計算｜実働時間は何時間？', ogdesc='出勤・退勤・休憩から実働時間と残業を計算。',
  h1='勤務時間 計算ツール',
  lead='出勤・退勤・休憩を入れるだけで、その日の実働時間と残業（8時間超）を計算します。勤怠やタイムカードの確認に。',
  inputs='''    <h2>⏰ 条件を入れる</h2>
    <div class="row"><div class="field"><label>出勤時刻</label><input type="time" id="in" value="09:00"></div>
    <div class="field"><label>退勤時刻</label><input type="time" id="out" value="18:30"></div></div>
    <div class="field"><label>休憩 <span class="hint">（分）</span></label><input type="number" id="b" value="60" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">実働時間を計算する</button>''',
  result='''      <div class="label">実働時間</div>
      <div class="big"><span id="big">0</span><span class="unit">時間</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">拘束時間</div><div class="v" id="kousoku">—</div></div>
      <div class="stat"><div class="k">休憩</div><div class="v" id="bv">—</div></div>
      <div class="stat"><div class="k">残業(8h超)</div><div class="v accent" id="over">—</div></div></div>''',
  article=C('実働時間 ＝ <b>退勤 − 出勤 − 休憩</b>。1日8時間（週40時間）を超えると、原則 <b>割増賃金（残業代）</b> の対象です。')+'''
    <h2>勤務時間の数え方</h2>
    <p>給与計算の基礎になる「実働時間」は、拘束時間から休憩を除いた時間です。労働基準法では1日8時間・週40時間が法定労働時間で、これを超える分は時間外労働（残業）として割増賃金の対象になります。</p>
    <div class="note"><strong>計算式</strong><br>拘束時間 ＝ 退勤時刻 − 出勤時刻<br>実働時間 ＝ 拘束時間 − 休憩時間<br>残業時間 ＝ max(0, 実働 − 8時間)</div>
    <p>6時間超は45分以上、8時間超は60分以上の休憩が必要です。深夜（22時〜5時）はさらに割増になります。</p>
    <h2>よくある質問</h2>'''+faq([('休憩は何分必要？','労働6時間超で45分、8時間超で60分以上の休憩が義務付けられています。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['労働基準法 労働時間・休憩']),
  js='''  function toMin(v){if(!v)return 0;const p=v.split(':');return (+p[0])*60+(+p[1]);}
  function calc(){const s=toMin($('in').value),e=toMin($('out').value),b=Math.max(0,+$('b').value||0);
    let kou=e-s; if(kou<0)kou+=1440; const work=Math.max(0,kou-b), over=Math.max(0,work-480);
    $('sub').textContent=`${$('in').value}〜${$('out').value}・休憩${b}分`;
    $('kousoku').textContent=(kou/60).toFixed(1)+'時間';$('bv').textContent=b+'分';$('over').textContent=(over/60).toFixed(1)+'時間';
    show();anim($('big'),0,work/60,800,1);
    SHARE=`勤務時間シミュ、実働${(work/60).toFixed(1)}時間（残業${(over/60).toFixed(1)}時間）でした⏰`;}''')

add(id='kakeibo-wari', cat=MONEY, emoji='🥧',
  title='家計の黄金比 計算｜手取りから理想の支出割合は？｜シミュラボ',
  desc='手取り月収から、住居・食費・貯蓄など理想的な家計の支出割合（黄金比）に当てはめた金額の目安を計算する無料シミュレーター。',
  ogtitle='家計の黄金比｜理想の支出割合は？', ogdesc='手取りから理想の家計バランス(各費目の目安額)を計算。',
  h1='家計の黄金比 計算シミュレーター',
  lead='手取りから、理想の家計バランスは？住居・食費・貯蓄などの「黄金比」に当てはめて、各費目の目安額を計算します。',
  inputs='''    <h2>🥧 条件を入れる</h2>
    <div class="field"><label>手取りの月収 <span class="hint">（万円）</span></label><input type="number" id="m" value="25" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">理想の家計を見る</button>''',
  result='''      <div class="label">理想の貯蓄・投資（月）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">住居(25%)</div><div class="v accent" id="ie">—</div></div>
      <div class="stat"><div class="k">食費(15%)</div><div class="v" id="shoku">—</div></div>
      <div class="stat"><div class="k">自由に使える</div><div class="v" id="free">—</div></div></div>''',
  article=C('家計の黄金比は <b>住居25%・食費15%・貯蓄20%</b> が目安。手取りに対する割合で考えると、使いすぎを防げます。')+'''
    <h2>理想の家計バランス（黄金比）</h2>
    <p>収入が増えても支出も膨らむと貯まりません。手取りに対する費目ごとの「割合」で管理すると、ムダが見えやすくなります。下表は一般的な目安です（家族構成・地域で調整を）。</p>
    <table class="seo-table"><tr><th>費目</th><th>理想割合</th></tr>
    <tr><td>住居（家賃・ローン）</td><td>25%</td></tr><tr><td>食費</td><td>15%</td></tr>
    <tr><td>水道光熱</td><td>6%</td></tr><tr><td>通信</td><td>5%</td></tr>
    <tr><td>保険</td><td>4%</td></tr><tr><td>趣味・娯楽・交際</td><td>15%</td></tr>
    <tr><td>日用品・その他</td><td>10%</td></tr><tr><td>貯蓄・投資</td><td>20%</td></tr></table>
    <p>まず「貯蓄20%を先取り」してから残りで生活するのが貯まる家計のコツです。</p>
    <h2>よくある質問</h2>'''+faq([('貯蓄20%は難しい','まず10%からでもOK。固定費（住居・通信・保険）の見直しが効果的です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['家計管理の一般的な黄金比']),
  js='''  function calc(){const m=Math.max(0,+$('m').value||0)*10000;
    const chochiku=m*0.20, ie=m*0.25, shoku=m*0.15, free=m*0.15;
    $('sub').textContent=`手取り月収 ${num(m/10000)}万円`;
    $('ie').textContent=yen(ie);$('shoku').textContent=yen(shoku);$('free').textContent=yen(free);
    show();anim($('big'),0,chochiku,800);
    SHARE=`家計の黄金比シミュ、手取り${num(m/10000)}万円なら貯蓄は月${yen(chochiku)}・住居${yen(ie)}が目安でした🥧`;}''')

# ===================== 診断 6本 =====================

dq('tekishoku', WORK, '🧩', '適職診断｜あなたに向いてる仕事タイプは？｜シミュラボ',
  '仕事の好みや強みの質問から、あなたに向いている仕事タイプ（対人・分析・創造・堅実）を診断する無料エンタメ診断。',
  '適職診断｜向いてる仕事タイプは？','質問に答えて向いてる仕事タイプを診断。',
  '適職診断','仕事の好みや強みから、向いている仕事タイプを診断します（エンタメ診断）。転職・就活のヒントに。',
  [('得意なのは？',[('人と話す',0),('分析・計算',2),('企画・発想',4)]),
   ('働き方の理想は？',[('チームで',0),('黙々と',2),('自由に',4)]),
   ('評価されたいのは？',[('人を支えた',0),('正確さ',2),('新しさ',4)]),
   ('苦手なのは？',[('細かい作業',4),('臨機応変',0),('単調な繰り返し',2)])],
  [(4,'対人サポート型','人と関わる仕事が得意。営業・接客・人事・教育・医療系などが向くタイプ。'),
   (9,'分析・堅実型','正確さとコツコツが強み。事務・経理・エンジニア・専門職などが向くタイプ。'),
   (16,'クリエイティブ型','発想と自由度を活かすタイプ。企画・デザイン・マーケ・起業などが向くタイプ。')],
  '得意・働き方・評価軸から、向いている仕事タイプを判定します。','対人サポート型／分析・堅実型／クリエイティブ型に分かれます。',
  [('転職の参考になる？','方向性のヒントになります。エンタメ診断です。'),('データは送信される？','いいえ、ブラウザ内で完結します。')],
  ['職業適性の一般論'], '適職診断、私は')

dq('kinsen-kankaku', MONEY, '💸', '金銭感覚診断｜あなたのお金の使い方タイプは？｜シミュラボ',
  'お金の使い方の質問から、あなたの金銭感覚タイプ（浪費・バランス・倹約）を診断する無料エンタメ診断。',
  '金銭感覚診断｜お金の使い方タイプは？','質問に答えて金銭感覚タイプを診断。',
  '金銭感覚診断','お金の使い方のクセから、あなたの金銭感覚タイプを診断します（エンタメ診断）。',
  [('ほしい物があると？',[('じっくり検討',0),('そこそこ',2),('すぐ買う',4)]),
   ('セールを見ると？',[('必要な物だけ',0),('少し見る',2),('つい買う',4)]),
   ('家計の把握は？',[('しっかり管理',0),('ざっくり',2),('ノータッチ',4)])],
  [(3,'しっかり倹約型','計画的にお金を使える堅実タイプ。貯蓄上手。'),
   (8,'バランス型','使うときは使い、締めるときは締める健全タイプ。'),
   (12,'浪費・楽しむ型','今を楽しむ気前の良いタイプ。先取り貯蓄を取り入れると安心。')],
  'お金の使い方・セール・家計管理から金銭感覚タイプを判定します。','倹約型／バランス型／浪費型に分かれます。',
  [('当たってる？','エンタメ診断です。家計見直しのきっかけに。'),('データは送信される？','いいえ、ブラウザ内で完結します。')],
  ['家計・金銭感覚の一般論'], '金銭感覚診断、私は')

dq('chokin-type', FIN, '🐷', '貯金タイプ診断｜あなたに合う貯金法は？｜シミュラボ',
  '性格やお金への向き合い方の質問から、あなたに合う貯金タイプ・貯め方を診断する無料エンタメ診断。',
  '貯金タイプ診断｜合う貯金法は？','質問に答えて合う貯金タイプを診断。',
  '貯金タイプ診断','性格やお金への向き合い方から、あなたに合う貯金法を診断します（エンタメ診断）。',
  [('コツコツは？',[('得意',0),('普通',2),('苦手',4)]),
   ('お金の管理は？',[('細かく派',0),('ざっくり',2),('面倒',4)]),
   ('ごほうびは？',[('我慢できる',0),('時々',2),('ないと続かない',4)])],
  [(3,'コツコツ積立型','毎月一定額の積立が向くタイプ。自動積立で着実に増やせます。'),
   (8,'仕組み化型','先取り貯蓄＋ほどよいごほうびが向くタイプ。'),
   (12,'ゲーム感覚型','楽しさが必要なタイプ。目標貯金やアプリ、ポイント活用が続けやすい。')],
  'コツコツ度・管理スタイル・ごほうび欲求から合う貯金法を判定します。','積立型／仕組み化型／ゲーム感覚型に分かれます。',
  [('どれが一番貯まる？','自分が続けられる方法が一番です。先取り貯蓄はどのタイプにも有効。'),('データは送信される？','いいえ、ブラウザ内で完結します。')],
  ['貯蓄・行動経済の一般論'], '貯金タイプ診断、私は')

dq('hougen-shindan', MENTAL, '🗾', '似合う方言診断｜あなたにピッタリの方言は？｜シミュラボ',
  '性格や話し方の質問から、あなたに似合う方言（関西弁・博多弁・東北弁など）を診断する無料エンタメ診断。',
  '似合う方言診断｜あなたにピッタリの方言は？','質問に答えて似合う方言を診断。',
  '似合う方言診断','性格や話し方の雰囲気から、あなたに似合う方言を診断します（エンタメ診断）。',
  [('会話のテンションは？',[('落ち着いてる',0),('普通',2),('にぎやか',4)]),
   ('ノリは？',[('クール',0),('そこそこ',2),('ツッコミ大好き',4)]),
   ('印象は？',[('上品・おっとり',0),('素朴',2),('元気・愛嬌',4)])],
  [(3,'はんなり京都弁／標準語','落ち着いた上品な雰囲気。やわらかい言葉が似合うタイプ。'),
   (8,'素朴な東北・博多弁','親しみやすく和ませる雰囲気。あたたかい方言が似合うタイプ。'),
   (12,'にぎやか関西弁','明るくテンポの良いムードメーカー。関西弁がハマるタイプ。')],
  'テンション・ノリ・印象から似合う方言を判定します。','京都弁・標準語／東北・博多弁／関西弁に分かれます。',
  [('当たってる？','エンタメ診断です。'),('データは送信される？','いいえ、ブラウザ内で完結します。')],
  ['方言の印象の一般論'], '似合う方言診断、私は')

dq('otaku-do', OSHI, '🎮', 'オタク度診断｜あなたのオタク度は何％？｜シミュラボ',
  '趣味への熱中度の質問から、あなたの「オタク度」を診断する無料エンタメ診断。',
  'オタク度診断｜あなたのオタク度は？','質問に答えてオタク度を診断。',
  'オタク度診断','好きなものへの熱中度から、あなたのオタク度を診断します（エンタメ診断）。',
  [('好きな物には？',[('そこそこ',0),('まあ熱中',2),('全力で沼る',4)]),
   ('グッズや課金は？',[('しない',0),('たまに',2),('つい使う',4)]),
   ('語り出すと？',[('短め',0),('普通',2),('止まらない',4)])],
  [(3,'ライトファン','広く浅く楽しむバランスタイプ。'),
   (8,'なかなかオタク','好きを深く楽しむ立派な趣味人タイプ。'),
   (12,'ガチオタク','愛と知識が止まらない筋金入り。その熱量が魅力！')],
  '熱中度・課金・語り度からオタク度を判定します。','ライトファン／なかなか／ガチオタクに分かれます。',
  [('当たってる？','エンタメ診断です。'),('データは送信される？','いいえ、ブラウザ内で完結します。')],
  ['趣味への熱中度の一般論'], 'オタク度診断、私は')

dq('undou-shinkei', SPORTS, '🤸', '運動神経 自己診断｜あなたの運動神経レベルは？｜シミュラボ',
  '反射や球技・バランスなどの質問から、あなたの運動神経レベルをセルフ診断する無料エンタメ診断。',
  '運動神経 自己診断｜あなたのレベルは？','質問に答えて運動神経レベルをセルフ診断。',
  '運動神経 自己診断','反射・球技・バランス感覚などから、運動神経レベルをセルフ診断します（エンタメ診断）。',
  [('とっさの反応は？',[('遅め',0),('普通',2),('素早い',4)]),
   ('球技は？',[('苦手',0),('人並み',2),('得意',4)]),
   ('バランス感覚は？',[('ぐらつく',0),('普通',2),('安定',4)]),
   ('新しい動きの習得は？',[('時間かかる',0),('普通',2),('すぐできる',4)])],
  [(4,'のんびり運動タイプ','運動はマイペース派。ウォーキング等コツコツ系が向くタイプ。'),
   (10,'平均的運動神経','人並みにこなせるバランスタイプ。練習で伸びしろ大。'),
   (16,'運動神経バツグン','反射・球技・習得が早いアスリート気質タイプ。')],
  '反射・球技・バランス・習得の速さから運動神経レベルを判定します。','のんびり型／平均型／バツグン型に分かれます。',
  [('当たってる？','自己回答のエンタメ診断です。'),('データは送信される？','いいえ、ブラウザ内で完結します。')],
  ['運動能力・コーディネーションの一般論'], '運動神経 自己診断、私は')

if __name__=='__main__':
    write_all(SIMS)
    print(f'seo8 done. {len(SIMS)} sims.')
