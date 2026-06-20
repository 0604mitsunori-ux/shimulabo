# -*- coding: utf-8 -*-
"""シミュラボ：新カテゴリ4種に さらに3本ずつ（計12本）。"""
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
SIMS=[]

# ===== 店舗・ビジネス =====
SIMS.append(dict(id='kaiten', cat=BIZ, emoji='🍽️',
  title='回転率シミュレーター｜飲食店の1日売上はいくら？｜シミュラボ',
  desc='席数・回転数・客単価・営業日数から、飲食店の1日と月の売上を試算する無料シミュレーター。回転率を上げると売上がどう変わるかが分かります。',
  ogtitle='回転率シミュレーター｜飲食店の1日売上は？', ogdesc='席数と回転数・客単価から、飲食店の1日・月の売上を試算。',
  h1='回転率シミュレーター',
  lead='飲食店の売上は「席数 × 回転数 × 客単価」で決まります。あなたのお店の1日・月の売上を試算して、回転率アップの効果を見てみましょう。',
  inputs='''    <h2>🍽️ 条件</h2>
    <div class="row"><div class="field"><label>席数 <span class="hint">（席）</span></label><input type="number" id="seats" value="30" min="1" inputmode="numeric"></div>
    <div class="field"><label>1日の回転数 <span class="hint">（回・1席が1日に何組）</span></label><input type="number" id="turn" value="2.5" min="0" step="0.1" inputmode="decimal"></div></div>
    <div class="row"><div class="field"><label>客単価 <span class="hint">（円）</span></label><input type="number" id="aov" value="1200" min="0" inputmode="numeric"></div>
    <div class="field"><label>月の営業日数 <span class="hint">（日）</span></label><input type="number" id="days" value="26" min="1" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">売上を試算する</button>''',
  result='''      <div class="label">1日の売上見込み</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">月商</div><div class="v accent" id="month">—</div></div>
      <div class="stat"><div class="k">1日の来客数</div><div class="v" id="cust">—</div></div>
      <div class="stat"><div class="k">回転0.5上げると月商</div><div class="v" id="up">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>1日売上＝席数×回転数×客単価<br>月商＝1日売上×営業日数</div>
    <p>回転率を0.5上げるだけでも、月商は大きく変わります。提供スピード・予約・席の使い方を工夫する価値が見えてきます。</p>
    <h2>よくある質問</h2>'''+faq([('回転数の目安は？','業態で大きく異なります。ランチ中心なら高く、ディナー・カフェは低めが一般的です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const s=Math.max(1,+$('seats').value||1),t=Math.max(0,+$('turn').value||0),a=Math.max(0,+$('aov').value||0),d=Math.max(1,+$('days').value||1);
    const day=s*t*a, month=day*d, cust=s*t, up=s*(t+0.5)*a*d;
    $('sub').textContent=`${s}席・回転${t}回・客単価${num(a)}円・月${d}日`;
    $('month').textContent=yen(month); $('cust').textContent=num(cust)+'組'; $('up').textContent=yen(up);
    SHARE=`回転率シミュ：うちの月商は約${yen(month)}（${s}席×回転${t}×${num(a)}円）🍽️\\nあなたのお店は？👇`;
    show(); anim($('big'),0,day,900);
  }'''))

SIMS.append(dict(id='line-cv', cat=BIZ, emoji='✉️',
  title='LINE・メルマガ配信効果シミュレーター｜1回の配信で売上いくら？｜シミュラボ',
  desc='配信数・開封率・クリック率・購入率・客単価から、LINEやメルマガ1回の配信で生まれる売上を試算する無料シミュレーター。',
  ogtitle='LINE・メルマガ配信効果シミュレーター｜1回でいくら？', ogdesc='配信数と開封率・購入率から、1回の配信の売上を試算。',
  h1='LINE・メルマガ配信効果シミュレーター',
  lead='お店のLINEやメルマガ、1回の配信でどれくらい売上になる？登録者数と反応率から、配信1回の効果を試算します。',
  inputs='''    <h2>✉️ 条件</h2>
    <div class="row"><div class="field"><label>配信数（登録者） <span class="hint">（人）</span></label><input type="number" id="n" value="1000" min="0" inputmode="numeric"></div>
    <div class="field"><label>開封率 <span class="hint">（％）</span></label><input type="number" id="open" value="40" min="0" max="100" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>クリック率 <span class="hint">（開封者のうち％）</span></label><input type="number" id="click" value="15" min="0" max="100" inputmode="numeric"></div>
    <div class="field"><label>来店・購入率 <span class="hint">（クリック者のうち％）</span></label><input type="number" id="cv" value="10" min="0" max="100" inputmode="numeric"></div></div>
    <div class="field"><label>客単価 <span class="hint">（円）</span></label><input type="number" id="aov" value="3000" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">配信の効果を見る</button>''',
  result='''      <div class="label">1回の配信で生まれる売上</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">開封した人</div><div class="v" id="op">—</div></div>
      <div class="stat"><div class="k">来店・購入</div><div class="v accent" id="cvn">—</div></div>
      <div class="stat"><div class="k">月4回配信なら</div><div class="v" id="m4">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>開封者＝配信数×開封率／クリック＝開封者×クリック率<br>購入＝クリック×購入率／売上＝購入×客単価</div>
    <p>登録者を増やすこと、開封したくなる件名にすること、両方が効きます。自社の「ハウスリスト」は、広告と違って何度でも無料で届けられる資産です。</p>
    <h2>よくある質問</h2>'''+faq([('開封率の目安は？','LINEは50%前後、メルマガは10〜30%が一般的な目安です（業種で差大）。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const n=Math.max(0,+$('n').value||0),o=(+$('open').value||0)/100,c=(+$('click').value||0)/100,cv=(+$('cv').value||0)/100,a=Math.max(0,+$('aov').value||0);
    const op=n*o, cvn=op*c*cv, rev=cvn*a;
    $('sub').textContent=`配信${num(n)}・開封${(o*100)}%・クリック${(c*100)}%・購入${(cv*100)}%`;
    $('op').textContent=num(op)+'人'; $('cvn').textContent=num(cvn)+'人'; $('m4').textContent=yen(rev*4);
    SHARE=`LINE/メルマガ1回の配信で売上${yen(rev)}の試算✉️（登録${num(n)}人）\\nリストは資産。あなたのお店は？👇`;
    show(); anim($('big'),0,rev,900);
  }'''))

SIMS.append(dict(id='zaiko', cat=BIZ, emoji='📦',
  title='在庫の持ちすぎコストシミュレーター｜眠る在庫、年いくら？｜シミュラボ',
  desc='平均在庫金額・保管コスト率・廃棄ロス率から、在庫を持ちすぎることで年間にかかるコストを試算する無料シミュレーター。',
  ogtitle='在庫の持ちすぎコスト｜眠る在庫、年いくら？', ogdesc='在庫金額と保管・廃棄率から、持ちすぎコストを年で試算。',
  h1='在庫の持ちすぎコストシミュレーター',
  lead='倉庫に眠る在庫は、ただ置いているだけでもお金がかかっています。保管・金利・廃棄ロスなど、在庫の持ちすぎコストを試算します。',
  inputs='''    <h2>📦 条件</h2>
    <div class="field"><label>平均の在庫金額 <span class="hint">（円・常にある在庫）</span></label><input type="number" id="stock" value="2000000" min="0" inputmode="numeric"></div>
    <div class="row"><div class="field"><label>年間の保管コスト率 <span class="hint">（％・保管+金利+劣化+機会損失）</span></label><input type="number" id="hold" value="20" min="0" max="100" inputmode="numeric"></div>
    <div class="field"><label>廃棄・値下げロス率 <span class="hint">（％/年）</span></label><input type="number" id="waste" value="3" min="0" max="100" step="0.5" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">在庫コストを見る</button>''',
  result='''      <div class="label">在庫の持ちすぎコスト（年）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">保管コスト</div><div class="v" id="hc">—</div></div>
      <div class="stat"><div class="k">廃棄・値下げロス</div><div class="v accent" id="wc">—</div></div>
      <div class="stat"><div class="k">月あたり</div><div class="v" id="mo">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>保管コスト＝在庫金額×保管コスト率<br>廃棄ロス＝在庫金額×廃棄率<br>合計＝保管＋廃棄</div>
    <p>在庫は「持っているだけでコスト」。一般に在庫の保管コストは年20〜30%とも言われます。適正在庫に近づけるほど、利益とキャッシュが改善します。</p>
    <h2>よくある質問</h2>'''+faq([('保管コスト20%は高すぎ？','倉庫代・金利・劣化・売れ残りリスク・機会損失を合わせると、一般に2〜3割になると言われます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const st=Math.max(0,+$('stock').value||0),h=(+$('hold').value||0)/100,w=(+$('waste').value||0)/100;
    const hc=st*h, wc=st*w, total=hc+wc;
    $('sub').textContent=`在庫${num(st)}円・保管${(h*100)}%・廃棄${(w*100)}%`;
    $('hc').textContent=yen(hc); $('wc').textContent=yen(wc); $('mo').textContent=yen(total/12);
    SHARE=`眠ってる在庫、持ちすぎコストが年${yen(total)}だった📦\\n在庫は置くだけでお金がかかる…あなたのお店は？👇`;
    show(); anim($('big'),0,total,900);
  }'''))

# ===== マネー・保険・不動産 =====
SIMS.append(dict(id='chochiku-mokuhyo', cat=FIN, emoji='🎯',
  title='目標金額までの積立シミュレーター｜毎月いくら貯めればいい？｜シミュラボ',
  desc='目標金額・想定利回り・積立年数から、目標達成に必要な毎月の積立額を逆算する無料シミュレーター。教育費・住宅頭金・老後資金の準備に。',
  ogtitle='目標金額までの積立｜毎月いくら貯めればいい？', ogdesc='目標額と利回り・年数から、必要な毎月の積立額を逆算。',
  h1='目標金額までの積立シミュレーター',
  lead='「○年後に○万円」を貯めるには、毎月いくら積み立てればいい？目標から逆算して、必要な積立額を計算します。',
  inputs='''    <h2>🎯 条件</h2>
    <div class="field"><label>目標金額 <span class="hint">（万円）</span></label><input type="number" id="goal" value="1000" min="1" inputmode="numeric"></div>
    <div class="row"><div class="field"><label>想定利回り <span class="hint">（％/年・貯金なら0）</span></label><input type="number" id="r" value="3" min="0" max="20" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>積立年数 <span class="hint">（年）</span></label><input type="number" id="y" value="15" min="1" max="60" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">必要な積立額を見る</button>''',
  result='''      <div class="label">毎月の積立額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">積み立てる元本</div><div class="v" id="moto">—</div></div>
      <div class="stat"><div class="k">運用益でカバー</div><div class="v accent" id="eki">—</div></div>
      <div class="stat"><div class="k">目標金額</div><div class="v" id="g2">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>毎月の積立＝目標額×月利÷((1+月利)^回数−1)（利回り0なら目標額÷回数）</div>
    <p>利回りがつくほど、毎月の負担は軽くなります。運用益が「目標のうちいくらをカバーしてくれるか」も表示しました（投資には元本割れリスクがあります）。</p>
    <h2>よくある質問</h2>'''+faq([('利回りは何%にすべき？','確実なのは0%（預金）。投資の場合は3〜5%が一つの目安ですが、変動・元本割れリスクがあります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const goal=Math.max(1,+$('goal').value||1)*10000, ry=(+$('r').value||0)/100, y=Math.max(1,+$('y').value||1);
    const r=ry/12, n=y*12; const m= r>0 ? goal*r/(Math.pow(1+r,n)-1) : goal/n;
    const moto=m*n, eki=goal-moto;
    $('sub').textContent=`目標${num(goal/10000)}万・利回り${(+$('r').value)}%・${y}年`;
    $('moto').textContent=yen(moto); $('eki').textContent=yen(Math.max(0,eki)); $('g2').textContent=yen(goal);
    SHARE=`${num(goal/10000)}万を${y}年で貯めるには、毎月${yen(m)}の積立が必要だった🎯（運用益${yen(Math.max(0,eki))}が手伝ってくれる）\\nあなたは？👇`;
    show(); anim($('big'),0,m,900);
  }'''))

SIMS.append(dict(id='reborisk', cat=FIN, emoji='💳',
  title='リボ払い 利息シミュレーター｜完済まで何年・利息いくら？｜シミュラボ',
  desc='リボ払いの残高・年率・毎月の返済額から、完済までの期間と支払う利息の総額を計算する無料シミュレーター。リボの怖さを数字で確認。',
  ogtitle='リボ払い 利息シミュレーター｜完済まで何年？', ogdesc='リボ残高と年率・返済額から、完済までの期間と総利息を計算。',
  h1='リボ払い 利息シミュレーター',
  lead='毎月の支払いが一定で安心に見えるリボ払い。でも実は高い利息がついています。完済までの期間と、支払う利息の総額を計算します。',
  inputs='''    <h2>💳 条件</h2>
    <div class="field"><label>リボ残高 <span class="hint">（円）</span></label><input type="number" id="bal" value="300000" min="0" inputmode="numeric"></div>
    <div class="row"><div class="field"><label>実質年率 <span class="hint">（％・多くは15%前後）</span></label><input type="number" id="r" value="15" min="0" max="30" step="0.1" inputmode="decimal"></div>
    <div class="field"><label>毎月の返済額 <span class="hint">（円）</span></label><input type="number" id="pay" value="10000" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">完済までを計算する</button>''',
  result='''      <div class="label">完済までに払う利息の総額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">完済まで</div><div class="v accent" id="months">—</div></div>
      <div class="stat"><div class="k">総支払額</div><div class="v" id="total">—</div></div>
      <div class="stat"><div class="k">毎月の返済</div><div class="v" id="pay2">—</div></div></div>
      <div class="alert" id="warn" style="text-align:left;margin-top:18px;display:none;"></div>''',
  article='''    <h2>リボ払いが危ない理由</h2>
    <div class="note">毎月の返済額が一定でも、その多くが利息に消えて元金が減りにくいのがリボ払い。年率15%は、100万円の残高で年15万円の利息がつく計算です。</div>
    <p>返済額が「毎月の利息」を下回ると、元金がほとんど減らず、いつまでも終わりません。早めに繰上返済・一括返済するのが鉄則です。</p>
    <h2>よくある質問</h2>'''+faq([('なぜ終わらないことがある？','毎月の返済額が利息より少ないと、元金が減らないためです。返済額を上げると一気に楽になります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const bal=Math.max(0,+$('bal').value||0), ry=(+$('r').value||0)/100, pay=Math.max(0,+$('pay').value||0);
    const r=ry/12; const firstInt=bal*r;
    $('sub').textContent=`残高${num(bal)}円・年率${(ry*100).toFixed(1)}%・毎月${num(pay)}円`;
    $('pay2').textContent=yen(pay);
    if(pay<=firstInt){ $('months').textContent='終わらない'; $('total').textContent='—';
      $('warn').style.display=''; $('warn').className='alert bad'; $('warn').innerHTML='⚠️ 毎月の返済額が利息（'+yen(firstInt)+'）以下のため、<strong>元金が減らず完済できません</strong>。返済額を増やしましょう。';
      show(); $('big').textContent='∞'; return; }
    let b=bal, paid=0, mo=0; while(b>0 && mo<1200){ const i=b*r; b=b+i-pay; paid+=pay; mo++; if(b<0){ paid+=b; b=0; } }
    const interest=paid-bal;
    $('months').textContent=Math.floor(mo/12)+'年'+(mo%12)+'ヶ月'; $('total').textContent=yen(paid);
    $('warn').style.display='';$('warn').className='alert bad';$('warn').innerHTML='💡 同じ残高でも、毎月の返済額を上げるほど利息は減ります。可能なら一括・繰上返済を。';
    SHARE=`リボ払い、完済まで${Math.floor(mo/12)}年${mo%12}ヶ月・利息は総額${yen(interest)}だった💳\\nリボは早めに返すのが鉄則。👇`;
    show(); anim($('big'),0,interest,900);
  }'''))

SIMS.append(dict(id='fukuri72', cat=FIN, emoji='✨',
  title='72の法則シミュレーター｜お金は何年で2倍になる？｜シミュラボ',
  desc='想定利回りを入れるだけで、お金が2倍になるまでの年数を「72の法則」で計算し、10年・20年・30年後に何倍になるかも分かる無料シミュレーター。',
  ogtitle='72の法則シミュレーター｜お金は何年で2倍になる？', ogdesc='利回りから、お金が2倍になる年数を72の法則で計算。',
  h1='72の法則シミュレーター',
  lead='「72÷金利＝お金が2倍になる年数」。これが有名な“72の法則”。利回りを入れて、複利でお金が育つスピードを体感しましょう。',
  inputs='''    <h2>✨ 条件</h2>
    <div class="field"><label>想定利回り <span class="hint">（％/年）</span></label><input type="number" id="r" value="5" min="0.1" max="30" step="0.1" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">2倍になる年数を見る</button>''',
  result='''      <div class="label">お金が2倍になるまで</div>
      <div class="big"><span id="big">0</span><span class="unit">年</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">10年後</div><div class="v" id="y10">—</div></div>
      <div class="stat"><div class="k">20年後</div><div class="v" id="y20">—</div></div>
      <div class="stat"><div class="k">30年後</div><div class="v accent" id="y30">—</div></div></div>''',
  article='''    <h2>72の法則とは</h2>
    <div class="note"><strong>計算式</strong><br>2倍になる年数 ≒ 72 ÷ 利回り(%)</div>
    <p>たとえば利回り6%なら約12年で2倍。複利では、時間が経つほど増え方が加速します（雪だるま式）。低金利の預金と、運用の差が時間とともに大きく開く理由がここにあります。</p>
    <h2>よくある質問</h2>'''+faq([('正確な式ではない？','近似式ですが、利回り数%なら十分な精度です。投資の利回りは変動・元本割れリスクがあります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const r=Math.max(0.1,+$('r').value||0.1);
    const yrs=72/r, g=(n)=>Math.pow(1+r/100,n);
    $('sub').textContent=`年利回り${r}%の複利で計算`;
    $('y10').textContent='約'+g(10).toFixed(2)+'倍'; $('y20').textContent='約'+g(20).toFixed(2)+'倍'; $('y30').textContent='約'+g(30).toFixed(2)+'倍';
    SHARE=`72の法則：年利${r}%だとお金が2倍になるまで約${yrs.toFixed(1)}年✨（30年で約${g(30).toFixed(1)}倍）\\n複利すごい。あなたは？👇`;
    show(); anim($('big'),0,yrs,900,1);
  }'''))

# ===== 仕事・働き方 =====
SIMS.append(dict(id='taishokukin', cat=WORK, emoji='🎁',
  title='退職金 手取りシミュレーター｜税金を引くといくら？｜シミュラボ',
  desc='退職金の額面と勤続年数から、退職所得控除・税金を引いた手取り額を試算する無料シミュレーター。退職金は税優遇が大きいのが特徴です。',
  ogtitle='退職金 手取りシミュレーター｜税金を引くといくら？', ogdesc='退職金の額面と勤続年数から、税引き後の手取りを試算。',
  h1='退職金 手取りシミュレーター',
  lead='退職金は、税金がとても優遇されています。額面と勤続年数から、退職所得控除を使ったあとの「手取り」を試算します。',
  inputs='''    <h2>🎁 条件</h2>
    <div class="row"><div class="field"><label>退職金の額面 <span class="hint">（万円）</span></label><input type="number" id="amt" value="2000" min="0" inputmode="numeric"></div>
    <div class="field"><label>勤続年数 <span class="hint">（年）</span></label><input type="number" id="y" value="35" min="1" max="50" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">手取りを試算する</button>''',
  result='''      <div class="label">退職金の手取り（目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">万円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">退職所得控除</div><div class="v" id="ctrl">—</div></div>
      <div class="stat"><div class="k">税金（所得税＋住民税）</div><div class="v accent" id="tax">—</div></div>
      <div class="stat"><div class="k">手取り率</div><div class="v" id="rate">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>退職所得控除</strong><br>勤続20年まで：40万円×年数（最低80万円）<br>20年超：800万円＋70万円×(勤続−20年)<br>課税退職所得＝(額面−控除)÷2 に課税（1/2課税）</div>
    <p>退職金は「控除が大きい」「1/2だけ課税」と二重に優遇されており、手取り率はかなり高くなります。勤続が長いほど控除も増えます。</p>
    <h2>よくある質問</h2>'''+faq([('一時金と年金受取どっちが得？','受け取り方で税が変わります。本ツールは一時金（退職所得）の概算です。詳細は専門家にご相談を。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const amt=Math.max(0,+$('amt').value||0), y=Math.max(1,+$('y').value||1);
    const ctrl = y<=20 ? Math.max(80,40*y) : 800+70*(y-20);
    const kazei=Math.max(0,(amt-ctrl)/2);
    const br=[[195,0.05],[330,0.10],[695,0.20],[900,0.23],[1800,0.33],[4000,0.40],[1e9,0.45]];
    let st=0,prev=0; for(const [cap,rate] of br){ if(kazei>prev){ st+=(Math.min(kazei,cap)-prev)*rate; prev=cap; } else break; }
    const juumin=kazei*0.10, tax=st+juumin, take=amt-tax;
    $('sub').textContent=`額面${num(amt)}万・勤続${y}年`;
    $('ctrl').textContent=num(ctrl)+'万円'; $('tax').textContent=num(tax)+'万円'; $('rate').textContent= amt>0?Math.round(take/amt*100)+'%':'—';
    SHARE=`退職金${num(amt)}万の手取りは約${num(take)}万円だった🎁（税金わずか${num(tax)}万・税優遇すごい）\\nあなたは？👇`;
    show(); anim($('big'),0,take,900);
  }'''))

SIMS.append(dict(id='nenkin-mikomi', cat=WORK, emoji='🧓',
  title='年金見込みシミュレーター｜将来もらえる年金はいくら？｜シミュラボ',
  desc='平均年収と厚生年金の加入年数から、将来受け取れる公的年金（老齢基礎＋厚生年金）の年額・月額の目安を試算する無料シミュレーター。',
  ogtitle='年金見込みシミュレーター｜将来もらえる年金は？', ogdesc='平均年収と加入年数から、将来の年金額の目安を試算。',
  h1='年金見込みシミュレーター',
  lead='将来、年金は月いくらもらえる？平均年収と厚生年金の加入年数から、受け取れる公的年金の目安を試算します（ざっくり概算）。',
  inputs='''    <h2>🧓 条件</h2>
    <div class="row"><div class="field"><label>平均年収 <span class="hint">（現役時代の平均・万円）</span></label><input type="number" id="inc" value="450" min="0" inputmode="numeric"></div>
    <div class="field"><label>厚生年金の加入年数 <span class="hint">（年）</span></label><input type="number" id="y" value="40" min="0" max="50" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">年金見込みを見る</button>''',
  result='''      <div class="label">年金の見込み（年額・目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">万円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">月あたり</div><div class="v accent" id="mo">—</div></div>
      <div class="stat"><div class="k">老齢基礎年金</div><div class="v" id="kiso">—</div></div>
      <div class="stat"><div class="k">厚生年金（報酬比例）</div><div class="v" id="kousei">—</div></div></div>''',
  article='''    <h2>計算方法（ざっくり概算）</h2>
    <div class="note"><strong>計算式</strong><br>老齢基礎年金 ≒ 満額約81万円 ×（加入年数÷40）<br>厚生年金 ≒ 平均年収 × 0.005481 × 加入年数</div>
    <p>会社員は「基礎年金＋厚生年金」の2階建て。年収が高く・長く加入するほど厚生年金が増えます。正確な額は「ねんきん定期便」やねんきんネットでご確認ください。</p>
    <h2>よくある質問</h2>'''+faq([('正確ですか？','制度改定や個別事情で変わるため、あくまで目安です。公式の「ねんきんネット」で必ずご確認ください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const inc=Math.max(0,+$('inc').value||0), y=Math.max(0,+$('y').value||0);
    const kiso=81*Math.min(40,y)/40, kousei=inc*0.005481*y, total=kiso+kousei;
    $('sub').textContent=`平均年収${inc}万・加入${y}年`;
    $('mo').textContent=num(total/12*10000)+'円'; $('kiso').textContent=num(kiso)+'万円'; $('kousei').textContent=num(kousei)+'万円';
    SHARE=`将来の年金見込み、年${num(total)}万円（月${num(total/12)}万）の試算だった🧓\\n足りる？早めに備えよう。あなたは？👇`;
    show(); anim($('big'),0,total,900);
  }'''))

SIMS.append(dict(id='zaitaku-setsuyaku', cat=WORK, emoji='🏠',
  title='在宅勤務 節約シミュレーター｜テレワークで年いくら浮く？｜シミュラボ',
  desc='昼食代の差・通勤時間・在宅日数から、在宅勤務（テレワーク）で年間に浮くお金と時間を試算する無料シミュレーター。',
  ogtitle='在宅勤務 節約シミュレーター｜年いくら浮く？', ogdesc='昼食代と通勤時間から、在宅勤務で浮くお金と時間を試算。',
  h1='在宅勤務 節約シミュレーター',
  lead='在宅勤務にすると、ランチ代や通勤時間が浮きます。あなたが在宅で年間どれだけのお金と時間を取り戻せるかを試算します。',
  inputs='''    <h2>🏠 条件</h2>
    <div class="row"><div class="field"><label>出社時の昼食代との差 <span class="hint">（円/日・外食−自炊）</span></label><input type="number" id="lunch" value="400" min="0" inputmode="numeric"></div>
    <div class="field"><label>片道の通勤時間 <span class="hint">（分）</span></label><input type="number" id="commute" value="45" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>週の在宅日数 <span class="hint">（日）</span></label><input type="number" id="wd" value="3" min="0" max="7" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">浮くお金と時間を見る</button>''',
  result='''      <div class="label">在宅で浮くお金（年）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">年で浮く時間</div><div class="v accent" id="time">—</div></div>
      <div class="stat"><div class="k">＝ まる何日分</div><div class="v" id="days">—</div></div>
      <div class="stat"><div class="k">月あたりの節約</div><div class="v" id="mo">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>浮くお金＝昼食差×在宅日数×52週<br>浮く時間＝通勤(往復)×在宅日数×52週</div>
    <p>毎日のランチ代や通勤時間も、年単位で見ると大きな差に。浮いた時間を学習・副業・睡眠にあてれば、節約以上の価値が生まれます。</p>
    <h2>よくある質問</h2>'''+faq([('光熱費の増加は？','在宅では自宅の光熱費が増える面もあります。差し引きで考えるとより正確です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const lunch=Math.max(0,+$('lunch').value||0), c=Math.max(0,+$('commute').value||0), wd=Math.max(0,+$('wd').value||0);
    const money=lunch*wd*52, timeMin=c*2*wd*52, timeH=timeMin/60;
    $('sub').textContent=`昼食差${num(lunch)}円・片道${c}分・週${wd}日 在宅`;
    $('time').textContent=num(timeH)+'時間'; $('days').textContent=(timeH/24).toFixed(1)+'日'; $('mo').textContent=yen(money/12);
    SHARE=`在宅勤務で、年${yen(money)}＋${num(timeH)}時間（まる${(timeH/24).toFixed(1)}日）も浮く計算だった🏠\\nあなたは？👇`;
    show(); anim($('big'),0,money,900);
  }'''))

# ===== 学生・勉強 =====
SIMS.append(dict(id='naishin', cat=STUDY, emoji='📋',
  title='内申点シミュレーター｜9教科の評定から内申点を計算｜シミュラボ',
  desc='主要5教科と実技4教科の評定（5段階）から、内申点の目安を計算する無料シミュレーター。実技2倍の地域にも対応。高校受験の目安に。',
  ogtitle='内申点シミュレーター｜9教科の評定から計算', ogdesc='5教科と実技4教科の評定から、内申点の目安を計算。',
  h1='内申点シミュレーター',
  lead='高校受験で大事な「内申点」。9教科の評定（5段階）から、あなたの内申点の目安を計算します。実技を2倍で計算する地域にも対応。',
  inputs='''    <h2>📋 評定（5段階）</h2>
    <div class="row"><div class="field"><label>主要5教科の合計 <span class="hint">（国・数・英・理・社／25点満点）</span></label><input type="number" id="main" value="20" min="5" max="25" inputmode="numeric"></div>
    <div class="field"><label>実技4教科の合計 <span class="hint">（音・美・体・技家／20点満点）</span></label><input type="number" id="sub" value="14" min="4" max="20" inputmode="numeric"></div></div>
    <div class="field"><label>計算方式（地域による）</label><select id="mode"><option value="1">通常（9教科×5＝45点満点）</option><option value="2">実技2倍（5教科＋実技×2）</option></select></div>
    <button class="btn btn-primary" id="calcBtn">内申点を計算する</button>''',
  result='''      <div class="label">あなたの内申点（目安）</div>
      <div class="big"><span id="big">0</span><span class="unit" id="unit">点</span></div>
      <div class="sub" id="sub2">—</div>
      <div class="statline"><div class="stat"><div class="k">満点</div><div class="v" id="max">—</div></div>
      <div class="stat"><div class="k">達成率</div><div class="v accent" id="rate">—</div></div>
      <div class="stat"><div class="k">評価</div><div class="v" id="rank" style="font-size:16px;">—</div></div></div>''',
  article='''    <h2>この計算について</h2>
    <p>内申点（調査書点）の計算方法は<strong>都道府県や学校で大きく異なります</strong>。本ツールは代表的な「9教科×5段階＝45点満点」と「実技2倍」の2方式に対応した目安です。志望校の正確な計算方法は学校や先生に確認してください。</p>
    <h2>よくある質問</h2>'''+faq([('学年の重みは？','地域により中1〜中3の比重が違います（中3のみ・全学年など）。本ツールはある時点の素点の目安です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const m=Math.max(0,+$('main').value||0), s=Math.max(0,+$('sub').value||0), mode=+$('mode').value;
    let score, max; if(mode===2){ score=m+s*2; max=25+40; } else { score=m+s; max=45; }
    const rate=score/max*100;
    let r= rate>=90?'トップ校ねらえる':rate>=78?'かなり良い':rate>=64?'平均より上':rate>=50?'平均的':'これから伸ばそう';
    $('sub2').textContent=`5教科${m}＋実技${s}・${sel('mode').text}`;
    $('max').textContent=max+'点'; $('rate').textContent=Math.round(rate)+'%'; $('rank').textContent=r;
    SHARE=`内申点シミュ、私は${score}/${max}点（${Math.round(rate)}%・${r}）でした📋\\nあなたは？👇`;
    show(); anim($('big'),0,score,900);
  }'''))

SIMS.append(dict(id='juken-hiyou', cat=STUDY, emoji='💰',
  title='受験費用シミュレーター｜受験にいくらかかる？｜シミュラボ',
  desc='受験する学校数・受験料・交通費・入学金から、受験にかかる総額の目安を試算する無料シミュレーター。受験前の資金計画に。',
  ogtitle='受験費用シミュレーター｜受験にいくらかかる？', ogdesc='受験校数・受験料・入学金から、受験にかかる総額を試算。',
  h1='受験費用シミュレーター',
  lead='受験は、受験料・交通費・入学金など、意外とお金がかかります。受験にかかる費用の総額を試算して、早めに準備しましょう。',
  inputs='''    <h2>💰 条件</h2>
    <div class="row"><div class="field"><label>受験する学校数 <span class="hint">（校・併願含む）</span></label><input type="number" id="schools" value="5" min="1" inputmode="numeric"></div>
    <div class="field"><label>1校の受験料 <span class="hint">（円・私立は1.5〜3万が目安）</span></label><input type="number" id="fee" value="15000" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>交通・宿泊費の合計 <span class="hint">（円）</span></label><input type="number" id="travel" value="20000" min="0" inputmode="numeric"></div>
    <div class="field"><label>進学先の入学金 <span class="hint">（円・私立20〜30万が目安）</span></label><input type="number" id="enroll" value="250000" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">受験費用を計算する</button>''',
  result='''      <div class="label">受験にかかる費用 総額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">受験料の合計</div><div class="v" id="fees">—</div></div>
      <div class="stat"><div class="k">入学金</div><div class="v accent" id="en">—</div></div>
      <div class="stat"><div class="k">交通・宿泊</div><div class="v" id="tr">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>総額＝受験料×受験校数＋交通・宿泊費＋進学先の入学金</div>
    <p>併願校を増やすほど受験料がかさみます。私立の入学金は、入学を辞退しても戻らないことが多い点にも注意。早めの資金計画が安心です。</p>
    <h2>よくある質問</h2>'''+faq([('滑り止めの入学金は？','第一志望の発表前に滑り止めの入学金が必要なケースもあります。日程と返金有無を要確認です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const sc=Math.max(1,+$('schools').value||1), fee=Math.max(0,+$('fee').value||0), tr=Math.max(0,+$('travel').value||0), en=Math.max(0,+$('enroll').value||0);
    const fees=sc*fee, total=fees+tr+en;
    $('sub').textContent=`${sc}校受験・受験料${num(fee)}円`;
    $('fees').textContent=yen(fees); $('en').textContent=yen(en); $('tr').textContent=yen(tr);
    SHARE=`受験費用、総額で約${yen(total)}かかる試算だった💰（${sc}校受験）\\n早めに準備を。あなたは？👇`;
    show(); anim($('big'),0,total,900);
  }'''))

SIMS.append(dict(id='natsuyasumi', cat=STUDY, emoji='🌻',
  title='夏休みの宿題シミュレーター｜1日何ページやれば終わる？｜シミュラボ',
  desc='残りの宿題の量と夏休みの残り日数から、1日にこなすべき量と、いまのペースで間に合うかを計算する無料シミュレーター。',
  ogtitle='夏休みの宿題シミュレーター｜1日何ページで終わる？', ogdesc='残りの宿題量と日数から、1日のノルマと間に合うかを計算。',
  h1='夏休みの宿題シミュレーター',
  lead='夏休みの宿題、あと何日で終わらせる？残りの量と日数から、1日にやるべき量と、いまのペースで間に合うかを計算します。',
  inputs='''    <h2>🌻 条件</h2>
    <div class="row"><div class="field"><label>残りの宿題 <span class="hint">（ページ・問題数など）</span></label><input type="number" id="pages" value="120" min="0" inputmode="numeric"></div>
    <div class="field"><label>夏休みの残り日数 <span class="hint">（日）</span></label><input type="number" id="days" value="30" min="1" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>1日に使える時間 <span class="hint">（時間）</span></label><input type="number" id="hours" value="1" min="0.5" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>1ページにかかる時間 <span class="hint">（分）</span></label><input type="number" id="permin" value="10" min="1" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">1日のノルマを見る</button>''',
  result='''      <div class="label">1日にやれば終わるページ数</div>
      <div class="big"><span id="big">0</span><span class="unit">ページ</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">終わるのに必要な総時間</div><div class="v" id="tot">—</div></div>
      <div class="stat"><div class="k">1日の所要時間</div><div class="v accent" id="need">—</div></div>
      <div class="stat"><div class="k">間に合う？</div><div class="v" id="ok" style="font-size:16px;">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>1日のノルマ＝残りページ÷残り日数<br>必要総時間＝残りページ×1ページの時間</div>
    <p>「あと120ページ」と聞くと大変そうでも、「1日4ページ」なら一気にラクに感じます。逆算して、毎日コツコツ片付けるのが、夏休みを楽しむコツ。</p>
    <h2>よくある質問</h2>'''+faq([('間に合わないと出たら？','1日の時間を増やすか、得意な宿題から効率よく進めましょう。早く始めるほどラクになります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const p=Math.max(0,+$('pages').value||0), d=Math.max(1,+$('days').value||1), h=Math.max(0.1,+$('hours').value||0.1), pm=Math.max(1,+$('permin').value||1);
    const perDay=Math.ceil(p/d), totMin=p*pm, needMin=perDay*pm, ok= needMin <= h*60;
    $('sub').textContent=`残り${p}ページ・あと${d}日・1ページ${pm}分`;
    $('tot').textContent=(totMin/60).toFixed(1)+'時間'; $('need').textContent=(needMin/60).toFixed(1)+'時間/日'; $('ok').textContent= ok?'間に合う！':'時間を増やそう';
    SHARE=`夏休みの宿題、1日${perDay}ページやれば終わる計算だった🌻（残り${p}ページ/${d}日）\\n早めに片付けよ。あなたは？👇`;
    show(); anim($('big'),0,perDay,900);
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
