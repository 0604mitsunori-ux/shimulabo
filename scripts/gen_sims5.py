# -*- coding: utf-8 -*-
"""シミュラボ：新カテゴリ4種（店舗・ビジネス／マネー保険不動産／仕事・働き方／学生・勉強）計16本。"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGO = '''<span class="mark">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M9 3h6M10 3v5.2L5.4 16.4A2.4 2.4 0 0 0 7.5 20h9a2.4 2.4 0 0 0 2.1-3.6L14 8.2V3" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M7.7 14.5h8.6" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/>
          <circle cx="10.3" cy="16.7" r="1" fill="#fff"/>
          <circle cx="13.4" cy="17.4" r=".7" fill="#fff"/>
        </svg>
      </span>'''

TPL = '''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<meta name="description" content="__DESC__">
<meta property="og:title" content="__OGTITLE__">
<meta property="og:description" content="__OGDESC__">
<meta property="og:type" content="website">
<link rel="stylesheet" href="../../assets/style.css">
</head>
<body>

<header class="site-header">
  <div class="inner">
    <a class="brand" href="../../index.html">
      ''' + LOGO + '''
      <span class="name">シミュ<b>ラボ</b></span>
    </a>
    <span class="spacer"></span>
    <a class="back" href="../../index.html">← 一覧へ</a>
  </div>
</header>

<main class="wrap">

  <div class="sim-head">
    <div class="cat">__CAT__</div>
    <h1>__H1__</h1>
    <p class="lead">__LEAD__</p>
  </div>

  <section class="panel">
__INPUTS__
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
__RESULT__
      <div style="text-align:center;"><span id="shareCount" class="share-count" style="display:none"></span></div>
      <div class="share-row">
        <button class="btn btn-x" id="shareBtn">𝕏 で結果をシェア</button>
        <button class="btn btn-ghost" id="copyBtn">結果をコピー</button>
      </div>
    </div>
  </section>

  <article class="article">
__ARTICLE__
  </article>

  <section class="req-banner">
    <h2>💡 こんなシミュも見てみたい？</h2>
    <p>あなたの「これ数字で見たい」を送ってください。投票で人気の案から実際に作ります。</p>
    <a class="btn btn-primary" style="width:auto;display:inline-flex;padding:14px 30px;" href="../../request/index.html">リクエストする →</a>
    <div style="margin-top:12px;"><a href="../../board/index.html" style="font-size:13px;font-weight:800;">🗳️ みんなのリクエストに投票する →</a></div>
  </section>

</main>

<footer class="site-footer">
  <div class="inner">
    <p><a href="../../index.html">← シミュラボ トップへ戻る</a></p>
    <p style="margin-top:10px;opacity:.7">© 2026 シミュラボ</p>
  </div>
</footer>

<script>
(() => {
  const $ = (id) => document.getElementById(id);
  const yen = (n) => '¥' + Math.round(n).toLocaleString('ja-JP');
  const num = (n) => Math.round(n).toLocaleString('ja-JP');
  const sel = (id) => { const e=$(id); return e.options[e.selectedIndex]; };
  let SHARE = '';
  function anim(el, from, to, dur, dec){ const t0=performance.now(); (function s(n){const p=Math.min(1,(n-t0)/dur);const e=1-Math.pow(1-p,3);const v=from+(to-from)*e;el.textContent=(dec!=null?v.toFixed(dec):Math.round(v).toLocaleString('ja-JP'));if(p<1)requestAnimationFrame(s);})(performance.now()); }
  function show(){ $('resultPanel').style.display=''; $('resultPanel').scrollIntoView({behavior:'smooth',block:'start'}); }
__JS__
  $('calcBtn').addEventListener('click', calc);
  $('shareBtn').addEventListener('click', () => window.open('https://twitter.com/intent/tweet?text='+encodeURIComponent(SHARE)+'&url='+encodeURIComponent(location.href)+'&hashtags='+encodeURIComponent('シミュラボ'),'_blank','noopener'));
  $('copyBtn').addEventListener('click', async () => { try{ await navigator.clipboard.writeText(SHARE+'\\n'+location.href); $('copyBtn').textContent='コピーしました ✓'; setTimeout(()=>$('copyBtn').textContent='結果をコピー',1600);}catch{alert(SHARE);} });
})();
</script>
<script src="../../assets/share-counter.js"></script>
<script>ShareCounter.initSim({ simId:'__ID__', badgeEl:document.getElementById('shareCount'), shareBtnIds:['shareBtn'] });</script>
</body>
</html>
'''

def faq(qa):
    return '<dl class="faq">' + ''.join(f'<dt>{q}</dt><dd>{a}</dd>' for q,a in qa) + '</dl>'

BIZ='店舗・ビジネス'; FIN='マネー・保険・不動産'; WORK='仕事・働き方'; STUDY='学生・勉強'
CTA='<div class="note">📣 集客やWeb広告の運用でお困りなら、<a href="../../contact/index.html">プロに相談</a>できます（MEO・広告運用・SEO代行）。</div>'
SIMS=[]

# ===== 店舗・ビジネス =====
SIMS.append(dict(id='ad-roas', cat=BIZ, emoji='📊',
  title='広告ROAS試算シミュレーター｜その広告、利益は出てる？｜シミュラボ',
  desc='広告費・クリック単価・CVR・客単価から、広告のROAS（費用対効果）と広告を差し引いた利益を試算する無料シミュレーター。お店・EC・サービスの広告判断に。',
  ogtitle='広告ROAS試算シミュレーター｜その広告、利益は出てる？', ogdesc='広告費とCVR・客単価からROASと差引利益を試算。',
  h1='広告ROAS試算シミュレーター',
  lead='出している広告、ちゃんと利益が出ていますか？広告費・クリック単価・成約率・客単価から、ROAS（費用対効果）と手元に残る利益を試算します。',
  inputs='''    <h2>📊 広告の条件</h2>
    <div class="row"><div class="field"><label>月の広告費 <span class="hint">（円）</span></label><input type="number" id="cost" value="100000" min="0" inputmode="numeric"></div>
    <div class="field"><label>クリック単価(CPC) <span class="hint">（円）</span></label><input type="number" id="cpc" value="50" min="1" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>成約率(CVR) <span class="hint">（％）</span></label><input type="number" id="cvr" value="2" min="0" step="0.1" inputmode="decimal"></div>
    <div class="field"><label>客単価 <span class="hint">（円）</span></label><input type="number" id="aov" value="5000" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>粗利率 <span class="hint">（％）</span></label><input type="number" id="margin" value="40" min="0" max="100" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">ROASを試算する</button>''',
  result='''      <div class="label">広告のROAS（費用対効果）</div>
      <div class="big"><span id="big">0</span><span class="unit">%</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">獲得客数</div><div class="v" id="cv">—</div></div>
      <div class="stat"><div class="k">売上</div><div class="v" id="rev">—</div></div>
      <div class="stat"><div class="k">広告差引利益</div><div class="v accent" id="profit">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>クリック数＝広告費÷CPC／獲得客数＝クリック×CVR<br>売上＝獲得客数×客単価／ROAS＝売上÷広告費×100<br>差引利益＝売上×粗利率−広告費</div>
    <p>ROASは「広告費1円が何円の売上を生んだか」。ただし大事なのは<strong>粗利で広告費を回収できているか</strong>。ROASが高くても粗利率が低いと赤字のこともあります。</p>
    '''+CTA+'''
    <h2>よくある質問</h2>'''+faq([('ROASは何%あればいい？','粗利率の逆数が損益分岐の目安。粗利40%なら売上の40%＞広告費、つまりROAS250%以上が黒字ラインです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const cost=Math.max(0,+$('cost').value||0),cpc=Math.max(1,+$('cpc').value||1),cvr=(+$('cvr').value||0)/100,aov=Math.max(0,+$('aov').value||0),m=(+$('margin').value||0)/100;
    const clicks=cost/cpc, cv=clicks*cvr, rev=cv*aov, roas=cost>0?rev/cost*100:0, profit=rev*m-cost;
    $('sub').textContent=`広告費${num(cost)}円・CPC${cpc}円・CVR${(cvr*100)}%・客単価${num(aov)}円`;
    $('cv').textContent=num(cv)+'人'; $('rev').textContent=yen(rev); $('profit').textContent=yen(profit);
    SHARE=`広告ROASを試算したら${Math.round(roas)}%、差引利益${yen(profit)}だった📊\\nあなたの広告は？👇`;
    show(); anim($('big'),0,roas,900);
  }'''))

SIMS.append(dict(id='ltv', cat=BIZ, emoji='🔁',
  title='LTV（顧客生涯価値）シミュレーター｜1人のお客さんはいくらの価値？｜シミュラボ',
  desc='客単価・来店頻度・継続年数・粗利率から、1人の顧客がもたらすLTV（生涯価値）と、新規獲得にかけられる上限を試算する無料シミュレーター。',
  ogtitle='LTVシミュレーター｜1人のお客さんはいくらの価値？', ogdesc='客単価と来店頻度・継続年数からLTVと獲得コスト上限を試算。',
  h1='LTVシミュレーター',
  lead='1人のお客さんは、生涯であなたのお店にいくら使ってくれる？このLTV（顧客生涯価値）が分かると、新規集客にいくらまでかけられるかが見えてきます。',
  inputs='''    <h2>🔁 条件</h2>
    <div class="row"><div class="field"><label>客単価 <span class="hint">（円）</span></label><input type="number" id="aov" value="3000" min="0" inputmode="numeric"></div>
    <div class="field"><label>月の来店回数 <span class="hint">（回）</span></label><input type="number" id="freq" value="1" min="0" step="0.1" inputmode="decimal"></div></div>
    <div class="row"><div class="field"><label>継続年数 <span class="hint">（年）</span></label><input type="number" id="years" value="2" min="0" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>粗利率 <span class="hint">（％）</span></label><input type="number" id="margin" value="40" min="0" max="100" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">LTVを試算する</button>''',
  result='''      <div class="label">1人あたりのLTV（売上ベース）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">粗利ベースのLTV</div><div class="v" id="gp">—</div></div>
      <div class="stat"><div class="k">新規獲得にかけられる上限</div><div class="v accent" id="cac">—</div></div>
      <div class="stat"><div class="k">年間の売上/人</div><div class="v" id="yr">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>LTV(売上)＝客単価×月の来店回数×12×継続年数<br>粗利LTV＝LTV×粗利率（＝新規獲得にかけられる上限の目安）</div>
    <p>新規のお客さん1人を獲得するのにかけてよい広告費の上限は、ざっくり「粗利LTV」まで。リピートを増やすほどLTVは伸び、集客にかけられる予算も増えます。</p>
    '''+CTA+'''
    <h2>よくある質問</h2>'''+faq([('リピートを増やすには？','口コミ・再来店の仕組み・MEOでの再発見が効きます。LTVが上がると広告も回しやすくなります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const aov=Math.max(0,+$('aov').value||0),f=Math.max(0,+$('freq').value||0),y=Math.max(0,+$('years').value||0),m=(+$('margin').value||0)/100;
    const ltv=aov*f*12*y, gp=ltv*m, yr=aov*f*12;
    $('sub').textContent=`客単価${num(aov)}円・月${f}回・${y}年・粗利${(m*100)}%`;
    $('gp').textContent=yen(gp); $('cac').textContent='〜'+yen(gp); $('yr').textContent=yen(yr);
    SHARE=`うちの顧客LTVは1人${yen(ltv)}（粗利${yen(gp)}）だった🔁\\n新規獲得はここまでかけてOK。\\nあなたのお店は？👇`;
    show(); anim($('big'),0,ltv,900);
  }'''))

SIMS.append(dict(id='coupon', cat=BIZ, emoji='🎟️',
  title='クーポン採算シミュレーター｜その割引、利益は残る？｜シミュラボ',
  desc='割引率・原価率・クーポンで増える来店数・リピート率から、クーポン施策の採算（初回＋リピートの想定利益）を試算する無料シミュレーター。',
  ogtitle='クーポン採算シミュレーター｜その割引、利益は残る？', ogdesc='割引と原価率・リピート率からクーポン施策の利益を試算。',
  h1='クーポン採算シミュレーター',
  lead='集客のためのクーポン。割引すると利益は減りますが、新規＆リピートで取り戻せれば成功です。クーポン施策の採算を試算します。',
  inputs='''    <h2>🎟️ 条件</h2>
    <div class="row"><div class="field"><label>通常の客単価 <span class="hint">（円）</span></label><input type="number" id="aov" value="3000" min="0" inputmode="numeric"></div>
    <div class="field"><label>割引率 <span class="hint">（％）</span></label><input type="number" id="disc" value="20" min="0" max="100" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>原価率 <span class="hint">（％）</span></label><input type="number" id="cost" value="30" min="0" max="100" inputmode="numeric"></div>
    <div class="field"><label>クーポンで増える来店 <span class="hint">（人）</span></label><input type="number" id="add" value="50" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>リピーターになる率 <span class="hint">（％・想定3回来店）</span></label><input type="number" id="rep" value="20" min="0" max="100" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">採算を試算する</button>''',
  result='''      <div class="label" id="lab">クーポンの想定利益</div>
      <div class="big"><span id="big">0</span><span class="unit" id="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">初回（割引時）の利益</div><div class="v" id="first">—</div></div>
      <div class="stat"><div class="k">リピートの利益</div><div class="v accent" id="rp">—</div></div>
      <div class="stat"><div class="k">1回(割引時)の利益</div><div class="v" id="per">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>割引時の単価＝客単価×(1−割引率)／原価＝客単価×原価率<br>1回の利益＝割引時単価−原価<br>初回利益＝1回の利益×増えた来店／リピート利益＝来店×リピート率×3回×(通常単価−原価)</div>
    <p>クーポンは「初回で多少利益が薄くても、リピートで回収」が基本戦略。リピートにつながらないと、ただ安売りで終わってしまいます。</p>
    '''+CTA+'''
    <h2>よくある質問</h2>'''+faq([('リピートにつなげるには？','次回使えるクーポン・LINE登録・良い体験＆口コミ依頼が効果的です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const aov=Math.max(0,+$('aov').value||0),disc=(+$('disc').value||0)/100,cr=(+$('cost').value||0)/100,add=Math.max(0,+$('add').value||0),rep=(+$('rep').value||0)/100;
    const dPrice=aov*(1-disc), cost=aov*cr, per=dPrice-cost;
    const first=per*add, rpProfit=add*rep*3*(aov-cost), total=first+rpProfit;
    $('unit').textContent= total>=0?'円':'円 赤字';
    $('sub').textContent=`割引${(disc*100)}%・原価${(cr*100)}%・+${add}人・リピート${(rep*100)}%`;
    $('first').textContent=yen(first); $('rp').textContent=yen(rpProfit); $('per').textContent=yen(per);
    SHARE=`クーポン採算を試算したら、想定利益${yen(total)}だった🎟️（初回${yen(first)}+リピート${yen(rpProfit)}）\\nあなたのお店は？👇`;
    show(); anim($('big'),0,Math.abs(total),900);
  }'''))

SIMS.append(dict(id='chirashi-web', cat=BIZ, emoji='📰',
  title='チラシ vs Web広告シミュレーター｜同じ予算でどっちが集客できる？｜シミュラボ',
  desc='同じ予算で、紙のチラシとWeb広告のどちらが多く集客できるかを、配布数・反応率・クリック単価・成約率から比較する無料シミュレーター。',
  ogtitle='チラシ vs Web広告｜同じ予算でどっちが集客できる？', ogdesc='同じ予算でチラシとWeb広告の集客数を比較。',
  h1='チラシ vs Web広告シミュレーター',
  lead='同じ予算をかけるなら、紙のチラシとWeb広告、どちらが多く集客できる？それぞれの条件を入れて比べてみましょう。',
  inputs='''    <h2>📰 条件</h2>
    <div class="field"><label>予算 <span class="hint">（円・共通）</span></label><input type="number" id="budget" value="100000" min="0" inputmode="numeric"></div>
    <div class="row"><div class="field"><label>チラシ単価 <span class="hint">（円/枚・印刷+配布）</span></label><input type="number" id="cprice" value="5" min="0.1" step="0.1" inputmode="decimal"></div>
    <div class="field"><label>チラシ反応率 <span class="hint">（％・0.1〜0.3が目安）</span></label><input type="number" id="cresp" value="0.3" min="0" step="0.01" inputmode="decimal"></div></div>
    <div class="row"><div class="field"><label>Web クリック単価 <span class="hint">（円）</span></label><input type="number" id="cpc" value="50" min="1" inputmode="numeric"></div>
    <div class="field"><label>Web 成約率 <span class="hint">（％）</span></label><input type="number" id="cvr" value="2" min="0" step="0.1" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">どっちが集客できるか見る</button>''',
  result='''      <div class="label" id="lab">集客数で勝つのは</div>
      <div class="big" style="font-size:clamp(30px,7vw,52px)"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">チラシの集客</div><div class="v" id="ch">—</div></div>
      <div class="stat"><div class="k">Web広告の集客</div><div class="v accent" id="we">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>チラシ：枚数＝予算÷単価／集客＝枚数×反応率<br>Web：クリック＝予算÷CPC／集客＝クリック×成約率</div>
    <p>チラシは地域に確実に届く・年配層に強い、Webは狙い撃ち＆効果測定ができるのが強み。どちらが良いかは商売や地域によります。両方を組み合わせるのも有効です。</p>
    '''+CTA+'''
    <h2>よくある質問</h2>'''+faq([('反応率やCVRの目安は？','チラシ反応率は0.1〜0.3%、Web成約率は1〜3%が一般的な目安です（業種で差大）。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const b=Math.max(0,+$('budget').value||0),cp=Math.max(0.1,+$('cprice').value||0.1),cr=(+$('cresp').value||0)/100,cpc=Math.max(1,+$('cpc').value||1),cvr=(+$('cvr').value||0)/100;
    const ch=(b/cp)*cr, we=(b/cpc)*cvr;
    const win= we>=ch?'Web広告':'チラシ';
    $('big').textContent=win; $('sub').textContent=`予算${num(b)}円で比較`;
    $('ch').textContent=num(ch)+'人'; $('we').textContent=num(we)+'人';
    SHARE=`同じ予算でチラシ${num(ch)}人 vs Web広告${num(we)}人、勝ったのは「${win}」📰\\nあなたのお店は？👇`;
    show();
  }'''))

# ===== マネー・保険・不動産 =====
SIMS.append(dict(id='jutaku-loan', cat=FIN, emoji='🏠',
  title='住宅ローン返済シミュレーター｜毎月いくら？総利息は？｜シミュラボ',
  desc='借入額・金利・返済年数から、住宅ローンの毎月の返済額・総返済額・総利息を計算する無料シミュレーター（元利均等返済）。',
  ogtitle='住宅ローン返済シミュレーター｜毎月いくら？総利息は？', ogdesc='借入額と金利・年数から毎月返済額・総利息を計算。',
  h1='住宅ローン返済シミュレーター',
  lead='マイホームの住宅ローン、毎月いくら返す？総額でいくら利息を払う？借入額・金利・年数から計算します（元利均等返済）。',
  inputs='''    <h2>🏠 条件</h2>
    <div class="field"><label>借入額 <span class="hint">（万円）</span></label><input type="number" id="p" value="3500" min="0" inputmode="numeric"></div>
    <div class="row"><div class="field"><label>金利 <span class="hint">（％/年）</span></label><input type="number" id="r" value="1.0" min="0" max="20" step="0.05" inputmode="decimal"></div>
    <div class="field"><label>返済年数 <span class="hint">（年）</span></label><input type="number" id="y" value="35" min="1" max="50" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">返済額を計算する</button>''',
  result='''      <div class="label">毎月の返済額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">総返済額</div><div class="v" id="total">—</div></div>
      <div class="stat"><div class="k">総利息</div><div class="v accent" id="int">—</div></div>
      <div class="stat"><div class="k">借入額</div><div class="v" id="p2">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式（元利均等）</strong><br>月返済＝借入×月利÷(1−(1+月利)^−回数)<br>月利＝年利÷12／回数＝年数×12</div>
    <p>金利が1%違うだけで、35年では総利息が数百万円変わります。借入前に「総利息」まで見ておくのが大切です。</p>
    <h2>よくある質問</h2>'''+faq([('ボーナス返済は？','本ツールは毎月返済のみの概算です。実際の審査・諸費用は金融機関にご確認ください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const P=Math.max(0,+$('p').value||0)*10000, ry=(+$('r').value||0)/100, y=Math.max(1,+$('y').value||1);
    const r=ry/12, n=y*12; const m = r>0 ? P*r/(1-Math.pow(1+r,-n)) : P/n;
    const total=m*n, int=total-P;
    $('sub').textContent=`借入${num(P/10000)}万・金利${(ry*100).toFixed(2)}%・${y}年`;
    $('total').textContent=yen(total); $('int').textContent=yen(int); $('p2').textContent=yen(P);
    SHARE=`住宅ローン試算：毎月${yen(m)}・総利息${yen(int)}だった🏠（${num(P/10000)}万/${(ry*100).toFixed(2)}%/${y}年）\\n👇`;
    show(); anim($('big'),0,m,900);
  }'''))

SIMS.append(dict(id='kuriage', cat=FIN, emoji='💴',
  title='繰上返済 効果シミュレーター｜利息はいくら減る？｜シミュラボ',
  desc='住宅ローンの残高・金利・残り年数と繰上返済額から、短縮できる期間と減らせる利息を試算する無料シミュレーター（期間短縮型）。',
  ogtitle='繰上返済 効果シミュレーター｜利息はいくら減る？', ogdesc='繰上返済で短縮できる期間と減る利息を試算。',
  h1='繰上返済 効果シミュレーター',
  lead='まとまったお金で繰上返済すると、どれだけ利息が減って、何年早く返し終わる？効果を試算します（期間短縮型）。',
  inputs='''    <h2>💴 条件</h2>
    <div class="field"><label>ローン残高 <span class="hint">（万円）</span></label><input type="number" id="p" value="3000" min="0" inputmode="numeric"></div>
    <div class="row"><div class="field"><label>金利 <span class="hint">（％/年）</span></label><input type="number" id="r" value="1.0" min="0.01" max="20" step="0.05" inputmode="decimal"></div>
    <div class="field"><label>残り年数 <span class="hint">（年）</span></label><input type="number" id="y" value="30" min="1" max="50" inputmode="numeric"></div></div>
    <div class="field"><label>繰上返済額 <span class="hint">（万円）</span></label><input type="number" id="extra" value="100" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">効果を試算する</button>''',
  result='''      <div class="label">減らせる利息（おトク額）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">短縮できる期間</div><div class="v accent" id="short">—</div></div>
      <div class="stat"><div class="k">繰上返済額</div><div class="v" id="ex">—</div></div>
      <div class="stat"><div class="k">繰上後の残高</div><div class="v" id="np">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>考え方（期間短縮型）</strong><br>毎月返済額はそのままに、元金を一括で減らすと、完済までの回数が短くなり、その分の利息が丸ごと不要になります。</div>
    <p>繰上返済は「早く・金利が高いほど」効果が大きくなります。一方、手元資金を残す安心とのバランスも大切です。</p>
    <h2>よくある質問</h2>'''+faq([('期間短縮型と返済額軽減型の違いは？','短縮型は利息軽減が大きく、軽減型は毎月の負担が下がります。本ツールは短縮型の概算です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const P=Math.max(0,+$('p').value||0)*10000, ry=(+$('r').value||0.01)/100, y=Math.max(1,+$('y').value||1), ex=Math.max(0,+$('extra').value||0)*10000;
    const r=ry/12, n=y*12; const m=P*r/(1-Math.pow(1+r,-n));
    const origInt=m*n-P;
    const np=Math.max(0,P-ex);
    // 新しい回数: np を 同じ月返済mで返すのに必要な回数
    let nn; if(np<=0){nn=0;} else { nn=Math.log(m/(m-np*r))/Math.log(1+r); }
    nn=Math.min(n, nn);
    const newInt=Math.max(0, m*nn-np);
    const saved=Math.max(0, origInt-newInt);
    const shortM=Math.round(n-nn);
    $('sub').textContent=`残高${num(P/10000)}万・金利${(ry*100).toFixed(2)}%・残${y}年・繰上${num(ex/10000)}万`;
    $('short').textContent=Math.floor(shortM/12)+'年'+(shortM%12)+'ヶ月'; $('ex').textContent=yen(ex); $('np').textContent=yen(np);
    SHARE=`繰上返済${num(ex/10000)}万で、利息が${yen(saved)}減って${Math.floor(shortM/12)}年${shortM%12}ヶ月早く完済できる試算💴\\n👇`;
    show(); anim($('big'),0,saved,900);
  }'''))

SIMS.append(dict(id='hosho', cat=FIN, emoji='🛡️',
  title='必要保障額シミュレーター｜生命保険、いくら必要？｜シミュラボ',
  desc='遺族の生活費・必要年数・貯蓄・公的遺族年金の見込みから、生命保険で備えるべき必要保障額の目安を試算する無料シミュレーター。',
  ogtitle='必要保障額シミュレーター｜生命保険いくら必要？', ogdesc='遺族の生活費と貯蓄・遺族年金から必要保障額を試算。',
  h1='必要保障額シミュレーター',
  lead='生命保険、いくら入ればいい？多すぎても保険料の無駄、少なすぎても不安。残された家族に必要な「保障額」の目安を試算します。',
  inputs='''    <h2>🛡️ 条件</h2>
    <div class="row"><div class="field"><label>遺族の年間生活費 <span class="hint">（万円）</span></label><input type="number" id="cost" value="300" min="0" inputmode="numeric"></div>
    <div class="field"><label>あと何年必要 <span class="hint">（年）</span></label><input type="number" id="years" value="20" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>今ある貯蓄 <span class="hint">（万円）</span></label><input type="number" id="save" value="500" min="0" inputmode="numeric"></div>
    <div class="field"><label>遺族年金など年額 <span class="hint">（万円・ざっくり）</span></label><input type="number" id="nenkin" value="100" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">必要保障額を見る</button>''',
  result='''      <div class="label">必要保障額の目安</div>
      <div class="big"><span id="big">0</span><span class="unit">万円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">総生活費</div><div class="v" id="tot">—</div></div>
      <div class="stat"><div class="k">貯蓄＋遺族年金でカバー</div><div class="v" id="cov">—</div></div>
      <div class="stat"><div class="k">不足（＝保険で備える）</div><div class="v accent" id="gap">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>必要保障額＝(年間生活費×必要年数)−貯蓄−(遺族年金×必要年数)</div>
    <p>必要以上の保険は家計を圧迫します。公的保障（遺族年金など）と貯蓄でまかなえる分を差し引いて、「足りない分だけ」保険で備えるのが基本です。</p>
    <h2>よくある質問</h2>'''+faq([('遺族年金はいくら？','家族構成で変わります。会社員世帯で年100〜150万円程度が一つの目安ですが、必ず公的資料でご確認ください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const c=Math.max(0,+$('cost').value||0),y=Math.max(0,+$('years').value||0),s=Math.max(0,+$('save').value||0),nk=Math.max(0,+$('nenkin').value||0);
    const tot=c*y, cov=s+nk*y, gap=Math.max(0,tot-cov);
    $('sub').textContent=`生活費${c}万×${y}年・貯蓄${s}万・遺族年金${nk}万/年`;
    $('tot').textContent=num(tot)+'万円'; $('cov').textContent=num(cov)+'万円'; $('gap').textContent=num(gap)+'万円';
    SHARE=`生命保険の必要保障額を試算したら約${num(gap)}万円だった🛡️\\n入りすぎ・入らなすぎ防止に。\\nあなたは？👇`;
    show(); anim($('big'),0,gap,900);
  }'''))

SIMS.append(dict(id='rougo', cat=FIN, emoji='👴',
  title='老後資金シミュレーター｜2000万円で足りる？不足額は？｜シミュラボ',
  desc='毎月の年金見込み・生活費・老後の年数から、老後に不足する資金の目安を試算する無料シミュレーター。「老後2000万円問題」を自分ごとに。',
  ogtitle='老後資金シミュレーター｜2000万円で足りる？', ogdesc='年金と生活費から、老後に不足する資金を試算。',
  h1='老後資金シミュレーター',
  lead='「老後2000万円問題」、自分の場合はどうなる？毎月の年金見込みと生活費から、老後に足りなくなる金額を試算します。',
  inputs='''    <h2>👴 条件</h2>
    <div class="row"><div class="field"><label>毎月の年金見込み <span class="hint">（万円）</span></label><input type="number" id="nenkin" value="15" min="0" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>毎月の生活費 <span class="hint">（万円）</span></label><input type="number" id="cost" value="25" min="0" step="0.5" inputmode="decimal"></div></div>
    <div class="field"><label>老後の年数 <span class="hint">（年・65歳から何年）</span></label><input type="number" id="years" value="30" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">不足額を見る</button>''',
  result='''      <div class="label" id="lab">老後に不足する資金</div>
      <div class="big"><span id="big">0</span><span class="unit">万円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">毎月の不足</div><div class="v accent" id="m">—</div></div>
      <div class="stat"><div class="k">老後の年数</div><div class="v" id="y">—</div></div>
      <div class="stat"><div class="k">毎月いくら積立てれば(20年)</div><div class="v" id="save">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>毎月の不足＝生活費−年金／総不足＝毎月の不足×12×老後の年数</div>
    <p>毎月5万円の不足でも、30年で1,800万円。これが「老後2000万円問題」の正体です。逆に、現役のうちから少しずつ積み立てれば十分備えられます。</p>
    <h2>よくある質問</h2>'''+faq([('年金見込みはどう調べる？','「ねんきん定期便」やねんきんネットで確認できます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const nk=Math.max(0,+$('nenkin').value||0),c=Math.max(0,+$('cost').value||0),y=Math.max(0,+$('years').value||0);
    const md=c-nk, total=Math.max(0,md*12*y);
    const saveM = total>0 ? total/ (20*12) : 0;
    $('lab').textContent= md<=0?'老後資金は足りる見込み':'老後に不足する資金';
    $('sub').textContent=`年金${nk}万・生活費${c}万・${y}年`;
    $('m').textContent=(md>=0?'':'＋')+num(Math.abs(md))+'万円'; $('y').textContent=y+'年'; $('save').textContent=(md<=0?'不要':num(saveM*10000)+'円/月');
    SHARE= md<=0?`老後資金シミュ、私は年金で足りる見込みでした👴\\nあなたは？👇`:`老後に不足する資金、私は約${num(total)}万円だった👴（毎月${num(md)}万不足）\\nあなたは？👇`;
    show(); anim($('big'),0,total,900);
  }'''))

# ===== 仕事・働き方 =====
SIMS.append(dict(id='zangyo', cat=WORK, emoji='🕒',
  title='残業代シミュレーター｜あなたの残業、いくらになる？｜シミュラボ',
  desc='月給と残業時間・割増率から、月と年の残業代を計算する無料シミュレーター。サービス残業の理論金額のチェックにも。',
  ogtitle='残業代シミュレーター｜あなたの残業、いくらになる？', ogdesc='月給と残業時間から、月・年の残業代を計算。',
  h1='残業代シミュレーター',
  lead='あなたの残業、お金にするといくら？月給と残業時間から、本来もらえる残業代を計算します。',
  inputs='''    <h2>🕒 条件</h2>
    <div class="row"><div class="field"><label>月給（基本給） <span class="hint">（万円）</span></label><input type="number" id="pay" value="25" min="0" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>月の残業時間 <span class="hint">（時間）</span></label><input type="number" id="hrs" value="30" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>割増率 <span class="hint">（％・通常25/深夜50）</span></label><input type="number" id="rate" value="25" min="0" max="100" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">残業代を計算する</button>''',
  result='''      <div class="label">1ヶ月の残業代</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">時給換算</div><div class="v" id="hw">—</div></div>
      <div class="stat"><div class="k">割増後の時給</div><div class="v" id="ow">—</div></div>
      <div class="stat"><div class="k">年間の残業代</div><div class="v accent" id="yr">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>時給＝月給÷160時間（目安）<br>残業代＝時給×(1+割増率)×残業時間</div>
    <p>法定時間外の割増は通常25%以上、深夜や休日はさらに上乗せされます。もし支払われていなければ、それは未払い残業代かもしれません。</p>
    <h2>よくある質問</h2>'''+faq([('正確な金額ですか？','所定労働時間や手当で変わるため概算です。正確な計算は給与規定をご確認ください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const pay=Math.max(0,+$('pay').value||0)*10000, hrs=Math.max(0,+$('hrs').value||0), rate=(+$('rate').value||0)/100;
    const hw=pay/160, ow=hw*(1+rate), m=ow*hrs;
    $('sub').textContent=`月給${num(pay/10000)}万・残業${hrs}h・割増${(rate*100)}%`;
    $('hw').textContent=yen(hw); $('ow').textContent=yen(ow); $('yr').textContent=yen(m*12);
    SHARE=`私の残業代、月${yen(m)}・年${yen(m*12)}になる計算だった🕒（残業${hrs}h/月）\\nあなたは？👇`;
    show(); anim($('big'),0,m,900);
  }'''))

SIMS.append(dict(id='yukyu', cat=WORK, emoji='🏖️',
  title='有給消化シミュレーター｜使わない有給、いくら捨ててる？｜シミュラボ',
  desc='残っている有給日数と月給から、有給の金額価値を計算。消化しないまま捨ててしまう有給を「お金」に換算する無料シミュレーター。',
  ogtitle='有給消化シミュレーター｜使わない有給、いくら捨ててる？', ogdesc='残っている有給を金額に換算。捨てると損する額は？',
  h1='有給消化シミュレーター',
  lead='使い切れずに消えていく有給休暇。実はけっこうな「お金」です。あなたの残り有給の金額価値を計算します。',
  inputs='''    <h2>🏖️ 条件</h2>
    <div class="row"><div class="field"><label>残っている有給 <span class="hint">（日）</span></label><input type="number" id="days" value="10" min="0" inputmode="numeric"></div>
    <div class="field"><label>月給 <span class="hint">（万円）</span></label><input type="number" id="pay" value="25" min="0" step="0.5" inputmode="decimal"></div></div>
    <div class="field"><label>1ヶ月の勤務日数 <span class="hint">（日）</span></label><input type="number" id="wd" value="20" min="1" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">有給の価値を見る</button>''',
  result='''      <div class="label">残っている有給の金額価値</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">日給換算</div><div class="v" id="dw">—</div></div>
      <div class="stat"><div class="k">残り日数</div><div class="v" id="d">—</div></div>
      <div class="stat"><div class="k">＝ 連休にすると</div><div class="v accent" id="wk">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>日給＝月給÷勤務日数／有給の価値＝日給×残り日数</div>
    <p>有給は「賃金が出る休み」。使わずに失効させると、その分を働いてタダで提供しているのと同じです。計画的に消化しましょう。</p>
    <h2>よくある質問</h2>'''+faq([('有給は買い取ってもらえる？','原則は買い取り不可（退職時など例外あり）。だからこそ「使う」のが基本です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const days=Math.max(0,+$('days').value||0), pay=Math.max(0,+$('pay').value||0)*10000, wd=Math.max(1,+$('wd').value||1);
    const dw=pay/wd, val=dw*days;
    $('sub').textContent=`月給${num(pay/10000)}万・勤務${wd}日／月`;
    $('dw').textContent=yen(dw); $('d').textContent=days+'日'; $('wk').textContent='約'+Math.round(days/5)+'週間の休み';
    SHARE=`残ってる有給、金額にすると${yen(val)}分だった🏖️（${days}日）\\n使わないと損！あなたは？👇`;
    show(); anim($('big'),0,val,900);
  }'''))

SIMS.append(dict(id='freelance', cat=WORK, emoji='🧑‍💻',
  title='フリーランス手取りシミュレーター｜税金・保険を引くといくら？｜シミュラボ',
  desc='年間売上と経費から、所得税・住民税・国民健康保険・国民年金をざっくり引いた、フリーランス・個人事業主の手取りの目安を試算する無料シミュレーター。',
  ogtitle='フリーランス手取りシミュレーター｜税・保険を引くと？', ogdesc='売上と経費から、税・社保を引いた手取りをざっくり試算。',
  h1='フリーランス手取りシミュレーター',
  lead='フリーランスの売上から、税金や保険を引くと手元にいくら残る？所得税・住民税・国保・年金をざっくり引いた手取りの目安を試算します。',
  inputs='''    <h2>🧑‍💻 条件</h2>
    <div class="row"><div class="field"><label>年間売上 <span class="hint">（万円）</span></label><input type="number" id="sales" value="600" min="0" inputmode="numeric"></div>
    <div class="field"><label>年間経費 <span class="hint">（万円）</span></label><input type="number" id="cost" value="100" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">手取りを試算する</button>''',
  result='''      <div class="label">ざっくり手取り（年）</div>
      <div class="big"><span id="big">0</span><span class="unit">万円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">所得</div><div class="v" id="inc">—</div></div>
      <div class="stat"><div class="k">税・社会保険 合計</div><div class="v accent" id="tax">—</div></div>
      <div class="stat"><div class="k">手取り率</div><div class="v" id="rate">—</div></div></div>''',
  article='''    <h2>計算方法（ざっくり概算）</h2>
    <div class="note"><strong>引くもの</strong><br>国民年金（年約20万）＋国民健康保険（所得の約10%）＋所得税（累進）＋住民税（課税所得の約10%）<br>※青色申告特別控除・基礎控除を簡易的に考慮した概算です。</div>
    <p>フリーランスは「売上＝手取り」ではありません。税・社会保険でおおよそ2〜3割が引かれます。請求額を決めるときの目安にどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([('正確ですか？','控除・扶養・自治体差で変わるため、あくまで概算です。正確には税理士や確定申告ソフトでご確認ください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const sales=Math.max(0,+$('sales').value||0), cost=Math.max(0,+$('cost').value||0);
    const inc=Math.max(0,sales-cost); // 所得(万円)
    const nenkin=20, kokuho=Math.min(inc*0.10,90);
    const kazei=Math.max(0,inc-48-nenkin-kokuho); // 基礎控除48万
    const br=[[195,0.05],[330,0.10],[695,0.20],[900,0.23],[1800,0.33],[4000,0.40],[1e9,0.45]];
    let st=0,prev=0; for(const [cap,rate] of br){ if(kazei>prev){ st+=(Math.min(kazei,cap)-prev)*rate; prev=cap; } else break; }
    const juumin=kazei*0.10;
    const totalTax=nenkin+kokuho+st+juumin;
    const take=inc-totalTax;
    $('sub').textContent=`売上${sales}万・経費${cost}万`;
    $('inc').textContent=num(inc)+'万円'; $('tax').textContent=num(totalTax)+'万円'; $('rate').textContent= inc>0?Math.round(take/inc*100)+'%':'—';
    SHARE=`フリーランス手取り試算：売上${sales}万→手取り約${num(take)}万円だった🧑‍💻（税・社保で${num(totalTax)}万）\\n👇`;
    show(); anim($('big'),0,take,900);
  }'''))

SIMS.append(dict(id='tsukin', cat=WORK, emoji='🚃',
  title='通勤時間の生涯コストシミュレーター｜人生で何日 通勤してる？｜シミュラボ',
  desc='片道の通勤時間・出勤日数・働く年数から、生涯で通勤に使う総時間を計算する無料シミュレーター。通勤時間の大きさを可視化します。',
  ogtitle='通勤時間の生涯コスト｜人生で何日 通勤してる？', ogdesc='片道の通勤時間から、生涯の通勤時間を日数換算で可視化。',
  h1='通勤時間の生涯コストシミュレーター',
  lead='毎日の通勤、生涯で合計するとどれだけの時間になる？片道の時間から、人生で通勤に使う総時間を計算します。',
  inputs='''    <h2>🚃 条件</h2>
    <div class="row"><div class="field"><label>片道の通勤時間 <span class="hint">（分）</span></label><input type="number" id="one" value="45" min="0" inputmode="numeric"></div>
    <div class="field"><label>週の出勤日数 <span class="hint">（日）</span></label><input type="number" id="wd" value="5" min="0" max="7" inputmode="numeric"></div></div>
    <div class="field"><label>あと働く年数 <span class="hint">（年）</span></label><input type="number" id="years" value="30" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">生涯の通勤時間を見る</button>''',
  result='''      <div class="label">生涯で通勤に使う時間</div>
      <div class="big"><span id="big">0</span><span class="unit">時間</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">まる何日分</div><div class="v accent" id="days">—</div></div>
      <div class="stat"><div class="k">1年あたり</div><div class="v" id="yr">—</div></div>
      <div class="stat"><div class="k">1日の往復</div><div class="v" id="rt">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>1日の往復＝片道×2／年間＝往復×週の出勤日数×52<br>生涯＝年間×働く年数</div>
    <p>片道45分でも、30年で約4,700時間＝まる195日分。通勤時間を学習や副業に変える、職住近接を選ぶなど、人生の使い方を考えるきっかけに。</p>
    <h2>よくある質問</h2>'''+faq([('在宅勤務だと？','出勤日数を減らして計算すれば、在宅で浮く時間が分かります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const one=Math.max(0,+$('one').value||0), wd=Math.max(0,+$('wd').value||0), y=Math.max(0,+$('years').value||0);
    const rt=one*2, yearMin=rt*wd*52, totalH=yearMin*y/60;
    $('sub').textContent=`片道${one}分・週${wd}日・${y}年`;
    $('days').textContent=(totalH/24).toFixed(0)+'日'; $('yr').textContent=Math.round(yearMin*y/y/60||yearMin/60)+'時間'; $('rt').textContent=rt+'分';
    SHARE=`生涯の通勤時間、約${num(totalH)}時間（まる${(totalH/24).toFixed(0)}日分）だった🚃\\nこの時間、何に使う？あなたは？👇`;
    show(); anim($('big'),0,totalH,900);
  }'''))

# ===== 学生・勉強 =====
SIMS.append(dict(id='goukaku', cat=STUDY, emoji='✏️',
  title='合格可能性シミュレーター｜偏差値で志望校の可能性をチェック｜シミュラボ',
  desc='自分の偏差値・志望校の偏差値・本気で勉強できる月数から、志望校の合格可能性の目安を診断する無料シミュレーター。受験のモチベーションづくりに。',
  ogtitle='合格可能性シミュレーター｜志望校の可能性は？', ogdesc='偏差値と残り期間から、志望校の合格可能性をざっくり診断。',
  h1='合格可能性シミュレーター',
  lead='今の偏差値と志望校の偏差値から、合格可能性の目安を診断します。これからの頑張りも反映。あくまで参考＆やる気アップのために。',
  inputs='''    <h2>✏️ 条件</h2>
    <div class="row"><div class="field"><label>今の自分の偏差値</label><input type="number" id="my" value="50" min="20" max="80" inputmode="numeric"></div>
    <div class="field"><label>志望校の偏差値</label><input type="number" id="goal" value="55" min="20" max="80" inputmode="numeric"></div></div>
    <div class="field"><label>本気で勉強できる残り月数 <span class="hint">（ヶ月）</span></label><input type="number" id="months" value="6" min="0" max="36" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">合格可能性を見る</button>''',
  result='''      <div class="label">志望校の合格可能性（目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">%</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:18px;">—</div>''',
  article='''    <h2>この診断について</h2>
    <p>偏差値の差と、これから勉強できる期間から合格可能性の目安を出すエンタメ診断です。実際の合否は当日の点数・倍率・科目バランスなど多くの要素で決まります。数字に振り回されず、やる気アップに使ってください。</p>
    <h2>よくある質問</h2>'''+faq([('信じていい？','参考程度に。判定が低くても、これからの努力で十分ひっくり返せます。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const my=+$('my').value||50, goal=+$('goal').value||50, mo=Math.max(0,+$('months').value||0);
    const diff=my-goal+mo*0.6; // 勉強でじわり上がる
    let p=1/(1+Math.exp(-diff/4))*100; p=Math.max(2,Math.min(97,p));
    let a; if(p>=70)a='合格圏内！この調子で苦手をつぶしていこう。油断は禁物💪';
    else if(p>=45)a='十分ねらえる！残り期間の伸びが勝負。計画的にいこう。';
    else if(p>=25)a='チャレンジ圏。基礎を固めて1点でも多く。逆転は十分ある！';
    else a='今は差があるけど、受験は伸びしろ勝負。毎日の積み重ねで可能性は上げられる！';
    $('sub').textContent=`偏差値 自分${my}／志望${goal}・あと${mo}ヶ月`;
    $('adv').textContent='✏️ '+a;
    SHARE=`合格可能性シミュ、志望校${goal}に対して私は${Math.round(p)}%だった✏️\\nここから上げてやる。あなたは？👇`;
    show(); anim($('big'),0,p,900);
  }'''))

SIMS.append(dict(id='benkyo-time', cat=STUDY, emoji='📚',
  title='勉強時間シミュレーター｜受験までの総勉強時間とライバル差｜シミュラボ',
  desc='1日の勉強時間と受験までの月数から、受験本番までの総勉強時間と、平均的なライバルとの差を可視化する無料シミュレーター。',
  ogtitle='勉強時間シミュレーター｜受験までの総時間とライバル差', ogdesc='1日の勉強時間から、受験までの総時間とライバル差を可視化。',
  h1='勉強時間シミュレーター',
  lead='受験本番まで、あと何時間 勉強できる？1日の勉強時間を入れると、総勉強時間と「ライバルとの差」が見えてきます。',
  inputs='''    <h2>📚 条件</h2>
    <div class="row"><div class="field"><label>1日の勉強時間 <span class="hint">（時間）</span></label><input type="number" id="h" value="2" min="0" max="18" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>受験まで <span class="hint">（ヶ月）</span></label><input type="number" id="m" value="6" min="0" max="48" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">総勉強時間を見る</button>''',
  result='''      <div class="label">受験までの総勉強時間</div>
      <div class="big"><span id="big">0</span><span class="unit">時間</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">ライバル平均(3h/日)</div><div class="v" id="rival">—</div></div>
      <div class="stat"><div class="k">差</div><div class="v accent" id="diff">—</div></div>
      <div class="stat"><div class="k">あと1h増やすと</div><div class="v" id="plus">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>総勉強時間＝1日の勉強時間×30日×残り月数</div>
    <p>「1日たった1時間の差」も、受験までの数ヶ月で数百時間の差になります。逆に言えば、今からの上積みでライバルを十分に追い越せます。</p>
    <h2>よくある質問</h2>'''+faq([('質と量どっちが大事？','どちらも大事ですが、まずは量を確保すると質も上がりやすくなります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const h=Math.max(0,+$('h').value||0), m=Math.max(0,+$('m').value||0);
    const tot=h*30*m, rival=3*30*m, diff=tot-rival, plus=(h+1)*30*m;
    $('sub').textContent=`1日${h}時間 × ${m}ヶ月`;
    $('rival').textContent=num(rival)+'時間'; $('diff').textContent=(diff>=0?'+':'')+num(diff)+'時間'; $('plus').textContent=num(plus)+'時間';
    SHARE=`受験までの総勉強時間、私は${num(tot)}時間になる計算📚（1日${h}h）\\nライバルと差をつけるぞ。あなたは？👇`;
    show(); anim($('big'),0,tot,900);
  }'''))

SIMS.append(dict(id='gakuhi', cat=STUDY, emoji='🎓',
  title='学費総額シミュレーター｜大学卒業まで教育費はいくら？｜シミュラボ',
  desc='進路（公立／私立・文系／理系）と自宅か下宿かから、大学卒業までにかかる教育費の総額の目安を試算する無料シミュレーター。',
  ogtitle='学費総額シミュレーター｜大学卒業まで教育費はいくら？', ogdesc='進路と下宿の有無から、大学卒業までの教育費総額を試算。',
  h1='学費総額シミュレーター',
  lead='子どもが大学を卒業するまで、教育費はトータルでいくらかかる？進路の選び方で大きく変わる学費の総額を試算します。',
  inputs='''    <h2>🎓 条件</h2>
    <div class="field"><label>進路（小〜大のイメージ）</label><select id="course">
      <option value="800">すべて公立＋国公立大</option>
      <option value="1100" selected>高校・大学は私立（文系）</option>
      <option value="1400">中学から私立＋私立大文系</option>
      <option value="1600">私立大 理系コース</option>
      <option value="3000">私立 医歯薬系</option></select></div>
    <div class="field"><label>大学で下宿する？</label><select id="lodge"><option value="0">自宅から通う</option><option value="400" selected>下宿・一人暮らし</option></select></div>
    <button class="btn btn-primary" id="calcBtn">教育費の総額を見る</button>''',
  result='''      <div class="label">大学卒業までの教育費 総額（目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">万円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">学費など</div><div class="v" id="base">—</div></div>
      <div class="stat"><div class="k">下宿の上乗せ</div><div class="v" id="lo">—</div></div>
      <div class="stat"><div class="k">毎月いくら積立（18年）</div><div class="v accent" id="save">—</div></div></div>''',
  article='''    <h2>この試算について</h2>
    <p>文部科学省などの調査をもとにした、進路別のざっくりした目安です。実際は学校・地域・習い事などで大きく変わります。早めに「総額」を知っておくと、計画的に準備できます。</p>
    <h2>よくある質問</h2>'''+faq([('習い事や塾は含む？','大まかに含んだ目安ですが、家庭により差が大きい部分です。余裕をもって見積もるのがおすすめです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const base=+$('course').value, lo=+$('lodge').value, total=base+lo;
    $('sub').textContent=`${sel('course').text}／${sel('lodge').text}`;
    $('base').textContent=num(base)+'万円'; $('lo').textContent=num(lo)+'万円'; $('save').textContent=num(total/(18*12)*10000)+'円/月';
    SHARE=`大学卒業までの教育費、約${num(total)}万円という試算だった🎓（${sel('course').text}）\\n計画的に備えよう。👇`;
    show(); anim($('big'),0,total,900);
  }'''))

SIMS.append(dict(id='bukatsu', cat=STUDY, emoji='🏃',
  title='部活引退カウントダウン｜引退まであと何日・あと何回練習？｜シミュラボ',
  desc='学年と引退の時期、週の練習日数から、部活を引退するまでの残り日数と残りの練習回数を計算する無料シミュレーター。中高生向け。',
  ogtitle='部活引退カウントダウン｜引退まであと何日？', ogdesc='学年と引退時期から、部活引退までの残り日数・練習回数を計算。',
  h1='部活引退カウントダウン',
  lead='大好きな部活も、いつかは引退。引退まであと何日、あと何回 練習できる？残りの時間を数えて、一日一日を大切に。',
  inputs='''    <h2>🏃 条件</h2>
    <div class="field"><label>今の学年</label><select id="grade">
      <option value="m1">中学1年</option><option value="m2">中学2年</option><option value="m3" selected>中学3年</option>
      <option value="h1">高校1年</option><option value="h2">高校2年</option><option value="h3">高校3年</option></select></div>
    <div class="field"><label>引退の時期</label><select id="when"><option value="7" selected>最終学年の夏（7月ごろ）</option><option value="10">最終学年の秋（10月ごろ）</option></select></div>
    <div class="field"><label>週の練習日数 <span class="hint">（日）</span></label><input type="number" id="wd" value="5" min="0" max="7" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">引退までを数える</button>''',
  result='''      <div class="label">引退まで、あと</div>
      <div class="big"><span id="big">0</span><span class="unit">日</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">あと何回の練習</div><div class="v accent" id="prac">—</div></div>
      <div class="stat"><div class="k">あと何ヶ月</div><div class="v" id="mo">—</div></div></div>''',
  article='''    <h2>この計算について</h2>
    <p>今日の日付と、最終学年の引退時期から、残りの日数と練習回数を計算します。卒業学年の人は引退が近いほど数字が小さくなります。残りの時間を大切に、悔いのないように。</p>
    <h2>よくある質問</h2>'''+faq([('もう引退した場合は？','残り0日と表示されます。お疲れさまでした！'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const g=$('grade').value, wm=+$('when').value, wd=Math.max(0,+$('wd').value||0);
    const now=new Date(); const y=now.getFullYear();
    // 最終学年になる年度を推定（学年→あと何年で最終学年か）
    const left={m1:2,m2:1,m3:0,h1:2,h2:1,h3:0}[g];
    // 年度の区切り(4月始まり)。今が1〜3月なら学年内。
    const fyBase = (now.getMonth()+1>=4)? y : y-1; // 現在の年度開始年
    const retYear = fyBase + left;
    let ret = new Date(retYear, wm-1, 15);
    let days = Math.ceil((ret-now)/86400000);
    if(days<0) days=0;
    const months=Math.max(0,(days/30));
    const prac=Math.round(days/7*wd);
    $('sub').textContent=`${sel('grade').text}・${sel('when').text}・週${wd}日`;
    $('prac').textContent=num(prac)+'回'; $('mo').textContent=months.toFixed(1)+'ヶ月';
    SHARE=`部活引退まであと${num(days)}日、練習あと約${num(prac)}回だった🏃\\n一日一日を大切に。あなたは？👇`;
    show(); anim($('big'),0,days,900);
  }'''))

for s in SIMS:
    d=os.path.join(ROOT,'sims',s['id']); os.makedirs(d,exist_ok=True)
    html=(TPL.replace('__TITLE__',s['title']).replace('__DESC__',s['desc'])
          .replace('__OGTITLE__',s['ogtitle']).replace('__OGDESC__',s['ogdesc'])
          .replace('__CAT__',s['cat']).replace('__H1__',s['h1']).replace('__LEAD__',s['lead'])
          .replace('__INPUTS__',s['inputs']).replace('__RESULT__',s['result'])
          .replace('__ARTICLE__',s['article']).replace('__JS__',s['js']).replace('__ID__',s['id']))
    with open(os.path.join(d,'index.html'),'w',encoding='utf-8') as f: f.write(html)
    print('created sims/'+s['id'])
print(f'done. {len(SIMS)} sims.')
