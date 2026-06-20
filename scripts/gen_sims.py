# -*- coding: utf-8 -*-
"""シミュラボ：シミュレーターHTMLをまとめて生成（共通の枠を統一）。
   ※ head の seo-head / seo-internal / breadcrumb / related は後段スクリプトが付与。
"""
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
      <span class="name">シミュ<b>ラボ</b></span><span class="tag">BETA</span>
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

SIMS = []

# 2. カフェイン残量
SIMS.append(dict(
  id='caffeine', cat='人生・自分ごと', emoji='☕',
  title='カフェイン残量シミュレーター｜寝る時、体に何mg残ってる？｜シミュラボ',
  desc='飲んだコーヒーの杯数と就寝までの時間から、就寝時に体内へ残るカフェイン量を半減期で計算。なかなか眠れない原因をチェックできる無料シミュレーター。',
  ogtitle='カフェイン残量シミュレーター｜寝る時、体に何mg残ってる？',
  ogdesc='コーヒーの杯数と就寝までの時間から、寝るときに体に残るカフェインを計算。',
  h1='カフェイン残量シミュレーター',
  lead='夜なかなか眠れないのは、コーヒーのカフェインがまだ体に残っているからかも。飲んだ量と就寝までの時間から、寝るときに体内に残るカフェイン量を計算します。',
  inputs='''    <h2>☕ 条件を入れる</h2>
    <div class="row">
      <div class="field"><label>飲んだ杯数 <span class="hint">（コーヒー換算・1杯約80mg）</span></label><input type="number" id="cups" value="3" min="0" max="30" inputmode="numeric"></div>
      <div class="field"><label>最後の1杯から就寝まで <span class="hint">（時間）</span></label><input type="number" id="hours" value="4" min="0" max="24" step="0.5" inputmode="decimal"></div>
    </div>
    <button class="btn btn-primary" id="calcBtn">就寝時の残量を見る</button>''',
  result='''      <div class="label">就寝時、体内に残るカフェイン</div>
      <div class="big"><span id="big">0</span><span class="unit">mg</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline">
        <div class="stat"><div class="k">摂取量</div><div class="v" id="intake">—</div></div>
        <div class="stat"><div class="k">半減期</div><div class="v">5時間</div></div>
        <div class="stat"><div class="k">睡眠への影響</div><div class="v accent" id="judge" style="font-size:16px;">—</div></div>
      </div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>摂取量 ＝ 杯数 × 80mg<br>就寝時の残量 ＝ 摂取量 × 0.5 ^（就寝までの時間 ÷ 5）<br><span style="font-size:13px">※カフェインの半減期を約5時間として概算</span></div>
    <p>カフェインは半減期が約5時間と長く、夕方に飲んだ1杯が就寝時にもかなり残ります。一般に就寝時に50mg以上残っていると、寝つきや睡眠の質に影響する可能性があるとされています。</p>
    <h2>ぐっすり眠るコツ</h2>
    <ul><li><strong>就寝6〜8時間前以降はカフェインを控える</strong></li><li><strong>午後はカフェインレスに切り替える</strong></li><li><strong>エナジードリンクは1本でコーヒー1〜2杯分のことも</strong></li></ul>
    <h2>よくある質問</h2>''' + faq([
    ('この数値は正確ですか？','体質・体重・代謝で個人差があります。一般的な半減期5時間での概算としてお使いください。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const cups=Math.max(0,+$('cups').value||0), h=Math.max(0,+$('hours').value||0);
    const intake=cups*80, rem=intake*Math.pow(0.5,h/5);
    const j = rem>=100?'強く残存':rem>=50?'眠り浅いかも':'おおむねOK';
    $('sub').textContent=`${cups}杯(${intake}mg)を ${h}時間前に摂取`;
    $('intake').textContent=intake+'mg'; $('judge').textContent=j;
    SHARE=`寝るとき体内にカフェインが約${Math.round(rem)}mgも残ってるらしい…☕（${cups}杯/就寝${h}時間前）\\n\\nあなたの残量は？👇`;
    show(); anim($('big'),0,rem,900);
  }'''))

# 3. 睡眠負債
SIMS.append(dict(
  id='sleep-debt', cat='人生・自分ごと', emoji='😴',
  title='睡眠負債シミュレーター｜あなたの寝不足、1年でどれだけ溜まる？｜シミュラボ',
  desc='平日の睡眠時間と必要睡眠から、借金のように積み上がる睡眠負債を計算。1年でどれだけ眠りが足りていないかを可視化する無料シミュレーター。',
  ogtitle='睡眠負債シミュレーター｜あなたの寝不足、1年でどれだけ溜まる？',
  ogdesc='平日の睡眠から、1年で積み上がる睡眠負債を計算。借金のように溜まる寝不足を可視化。',
  h1='睡眠負債シミュレーター',
  lead='毎日のちょっとした寝不足は、借金のように積み上がります。これが「睡眠負債」。あなたの平日の睡眠から、1年でどれだけ負債が溜まるかを計算します。',
  inputs='''    <h2>😴 条件を入れる</h2>
    <div class="row">
      <div class="field"><label>平日の平均睡眠時間 <span class="hint">（時間）</span></label><input type="number" id="sleep" value="6" min="0" max="12" step="0.5" inputmode="decimal"></div>
      <div class="field"><label>あなたに必要な睡眠 <span class="hint">（時間・標準7.5）</span></label><input type="number" id="need" value="7.5" min="4" max="12" step="0.5" inputmode="decimal"></div>
    </div>
    <button class="btn btn-primary" id="calcBtn">睡眠負債を見る</button>''',
  result='''      <div class="label">1年で積み上がる睡眠負債</div>
      <div class="big"><span id="big">0</span><span class="unit">時間</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline">
        <div class="stat"><div class="k">1日あたり</div><div class="v accent" id="day">—</div></div>
        <div class="stat"><div class="k">1ヶ月で</div><div class="v" id="month">—</div></div>
        <div class="stat"><div class="k">＝ まる何日分の睡眠</div><div class="v" id="days">—</div></div>
      </div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>1日の不足 ＝ 必要睡眠 − 平日睡眠<br>1年の負債 ＝ 1日の不足 × 5日 × 52週</div>
    <p>1日30分の不足でも、平日に積み重なると1年で約130時間。これは「まる5日以上ずっと眠っていないと返せない」量です。睡眠負債は週末の寝だめだけでは完全には返せないとも言われます。</p>
    <h2>負債を減らすには</h2>
    <ul><li><strong>就寝時刻を15分だけ早める</strong></li><li><strong>寝る前のスマホを減らす</strong></li><li><strong>休日も起きる時間はなるべく一定に</strong></li></ul>
    <h2>よくある質問</h2>''' + faq([
    ('週末に寝だめすれば返せますか？','ある程度は回復しますが、慢性的な負債は寝だめだけでは返しきれないとされます。平日の睡眠を増やすのが基本です。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const s=Math.max(0,+$('sleep').value||0), need=Math.max(0,+$('need').value||0);
    const d=Math.max(0,need-s), year=d*5*52, month=d*5*4.3;
    $('sub').textContent=`必要${need}h − 平日${s}h = 1日${d.toFixed(1)}h 不足`;
    $('day').textContent=d.toFixed(1)+'時間'; $('month').textContent=Math.round(month)+'時間';
    $('days').textContent=(year/need).toFixed(1)+'日分';
    SHARE=`私の睡眠負債、1年で約${Math.round(year)}時間…（まる${(year/need).toFixed(1)}日分の睡眠）😴\\n\\nあなたは？👇`;
    show(); anim($('big'),0,year,900);
  }'''))

# 4. 割り勘の不公平
SIMS.append(dict(
  id='warikan', cat='お金・時間', emoji='🍻',
  title='割り勘の不公平シミュレーター｜飲まない人、いくら損してる？｜シミュラボ',
  desc='飲み会の総額・人数・自分の杯数から、割り勘でいくら損（または得）しているかを計算。あまり飲まない人の「割り勘の理不尽」を数字にする無料シミュレーター。',
  ogtitle='割り勘の不公平シミュレーター｜飲まない人、いくら損してる？',
  ogdesc='飲み会の割り勘、あなたは損してる？得してる？飲んだ量から不公平を数字に。',
  h1='割り勘の不公平シミュレーター',
  lead='「自分はそんなに飲んでないのに、割り勘だと損した気がする」。その感覚、数字で確かめましょう。飲み会での割り勘の損得を計算します。',
  inputs='''    <h2>🍻 条件を入れる</h2>
    <div class="row">
      <div class="field"><label>飲み会の総額 <span class="hint">（円）</span></label><input type="number" id="total" value="20000" min="0" inputmode="numeric"></div>
      <div class="field"><label>参加人数 <span class="hint">（人）</span></label><input type="number" id="people" value="5" min="1" inputmode="numeric"></div>
    </div>
    <div class="row">
      <div class="field"><label>あなたの飲んだ杯数 <span class="hint">（杯）</span></label><input type="number" id="you" value="2" min="0" inputmode="numeric"></div>
      <div class="field"><label>1人あたり平均の杯数 <span class="hint">（杯）</span></label><input type="number" id="avg" value="5" min="1" inputmode="numeric"></div>
    </div>
    <button class="btn btn-primary" id="calcBtn">損得を見る</button>''',
  result='''      <div class="label" id="lab">割り勘で あなたは</div>
      <div class="big"><span id="big">0</span><span class="unit" id="unit">円 損</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline">
        <div class="stat"><div class="k">割り勘の支払い</div><div class="v" id="pay">—</div></div>
        <div class="stat"><div class="k">実際に飲んだ分</div><div class="v" id="real">—</div></div>
        <div class="stat"><div class="k">判定</div><div class="v accent" id="judge" style="font-size:16px;">—</div></div>
      </div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>割り勘の支払い ＝ 総額 ÷ 人数<br>実際に飲んだ分 ＝ 総額 × あなたの杯数 ÷（平均杯数 × 人数）<br>損得 ＝ 割り勘 − 飲んだ分</div>
    <p>飲む量に差がある飲み会では、割り勘はあまり飲まない人が「飲む人の分まで負担する」構造になります。可視化すると、その額の大きさに驚くかもしれません。</p>
    <h2>もやもやしない工夫</h2>
    <ul><li><strong>飲む人と飲まない人で会費を分ける</strong></li><li><strong>ソフトドリンクの人は割引にする</strong></li><li><strong>多めに飲んだ人が少し色をつける</strong></li></ul>
    <h2>よくある質問</h2>''' + faq([
    ('飲む人にも使えますか？','はい。よく飲む人は「得してる」と出ます。お互いの納得感づくりにどうぞ。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const total=Math.max(0,+$('total').value||0), people=Math.max(1,+$('people').value||1), you=Math.max(0,+$('you').value||0), avg=Math.max(1,+$('avg').value||1);
    const pay=total/people, real=total*you/(avg*people), loss=pay-real;
    const isLoss=loss>=0;
    $('unit').textContent= isLoss?'円 損':'円 得';
    $('judge').textContent= isLoss?'損してる😢':'得してる😋';
    $('sub').textContent=`総額${num(total)}円・${people}人・あなた${you}杯/平均${avg}杯`;
    $('pay').textContent=yen(pay); $('real').textContent=yen(real);
    SHARE= isLoss
      ? `この飲み会、割り勘だと私 約${yen(Math.abs(loss))}も損してるらしい…🍻\\n\\nあなたの飲み会は？👇`
      : `この飲み会、割り勘で私 約${yen(Math.abs(loss))}お得だった😋🍻\\n\\nあなたは？👇`;
    show(); anim($('big'),0,Math.abs(loss),900);
  }'''))

# 5. 宝くじ皮算用
SIMS.append(dict(
  id='takarakuji', cat='お金・時間', emoji='🎰',
  title='宝くじ買い続けたらシミュレーター｜期待値の残酷な現実｜シミュラボ',
  desc='宝くじを毎年いくら・何年買い続けるかを入れると、使う総額・期待される回収額・実質損失、さらに同じ額を運用していた場合との差を計算する無料シミュレーター。',
  ogtitle='宝くじ買い続けたらシミュレーター｜期待値の残酷な現実',
  ogdesc='宝くじを買い続けると、総額・期待回収・実質損失はいくら？運用との差も。',
  h1='宝くじ買い続けたらシミュレーター',
  lead='「夢を買う」宝くじ。でも買い続けると、トータルでいくら使い、いくら戻ってくるのでしょう。期待値の現実を、同額を運用した場合と並べて見てみます。',
  inputs='''    <h2>🎰 条件を入れる</h2>
    <div class="row">
      <div class="field"><label>1回いくら買う <span class="hint">（円）</span></label><input type="number" id="amt" value="3000" min="0" inputmode="numeric"></div>
      <div class="field"><label>年に何回 <span class="hint">（回）</span></label><input type="number" id="times" value="10" min="0" inputmode="numeric"></div>
    </div>
    <div class="field"><label>続ける年数 <span class="hint">（年）</span></label><input type="number" id="years" value="30" min="1" max="80" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">買い続けた結果を見る</button>''',
  result='''      <div class="label">買い続けて使う総額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline">
        <div class="stat"><div class="k">期待される回収(約47%)</div><div class="v" id="back">—</div></div>
        <div class="stat"><div class="k">実質の損失</div><div class="v accent" id="loss">—</div></div>
        <div class="stat"><div class="k">同額を年3%運用なら</div><div class="v" id="inv">—</div></div>
      </div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>総額 ＝ 1回の額 × 年の回数 × 年数<br>期待回収 ＝ 総額 × 47%（宝くじの還元率の目安）<br>運用比較 ＝ 毎年の購入額を年利3%で積立運用した場合の将来価値</div>
    <p>宝くじの還元率は約47%とされ、長く買い続けるほど期待値では半分以上が手元に戻りません。同じお金を堅実に積立運用していたら…という比較も並べました（あくまで概算で、当選の夢を否定するものではありません）。</p>
    <h2>よくある質問</h2>''' + faq([
    ('夢を買うのも無駄ですか？','いいえ。期待値は低くても、ワクワクへの対価と割り切るのは個人の自由です。本ツールは「もし運用していたら」という比較を示すだけです。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const amt=Math.max(0,+$('amt').value||0), times=Math.max(0,+$('times').value||0), years=Math.max(1,+$('years').value||1);
    const annual=amt*times, total=annual*years, back=total*0.47, loss=total-back;
    let fv=0; for(let i=0;i<years;i++){ fv=(fv+annual)*1.03; }
    $('sub').textContent=`1回${num(amt)}円 × 年${times}回 × ${years}年`;
    $('back').textContent=yen(back); $('loss').textContent=yen(loss); $('inv').textContent=yen(fv);
    SHARE=`宝くじを${years}年買い続けると総額${yen(total)}、期待回収は${yen(back)}…実質${yen(loss)}の損らしい🎰\\n同額を運用してたら${yen(fv)}だって…👇`;
    show(); anim($('big'),0,total,900);
  }'''))

# 6. あと何回、親に会えるか
SIMS.append(dict(
  id='oyako', cat='人生・自分ごと', emoji='👨‍👩‍👧',
  title='あと何回、親に会えるかシミュレーター｜残り回数を可視化｜シミュラボ',
  desc='親の年齢・年に会う回数・想定寿命から、これからあと何回 親に会えるかを計算。当たり前の時間の有限さに気づく無料シミュレーター。',
  ogtitle='あと何回、親に会えるかシミュレーター',
  ogdesc='親の年齢と年に会う回数から、これからあと何回会えるかを計算。',
  h1='あと何回、親に会えるか',
  lead='実家を出ると、親に会うのは年に数回。当たり前に思える時間にも、実は限りがあります。これからあと何回 親に会えるかを計算します。',
  inputs='''    <h2>👨‍👩‍👧 条件を入れる</h2>
    <div class="row">
      <div class="field"><label>親の年齢 <span class="hint">（歳）</span></label><input type="number" id="age" value="60" min="1" max="120" inputmode="numeric"></div>
      <div class="field"><label>年に会う回数 <span class="hint">（回）</span></label><input type="number" id="freq" value="5" min="0" max="365" inputmode="numeric"></div>
    </div>
    <div class="field"><label>親の想定寿命 <span class="hint">（歳・平均は男81/女87前後）</span></label><input type="number" id="life" value="85" min="1" max="120" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">残り回数を見る</button>''',
  result='''      <div class="label">これから親に会えるのは、あと</div>
      <div class="big"><span id="big">0</span><span class="unit">回</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline">
        <div class="stat"><div class="k">残りの年数</div><div class="v accent" id="years">—</div></div>
        <div class="stat"><div class="k">年に会う回数</div><div class="v" id="f">—</div></div>
        <div class="stat"><div class="k">日数にすると</div><div class="v" id="days">—</div></div>
      </div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>残り回数 ＝（想定寿命 − 今の年齢）× 年に会う回数</div>
    <p>たとえば親が60歳・年に5回会う・想定寿命85歳なら、残りは約125回。「まだまだ」と思っていた時間が、意外と数えられる回数だと気づきます。会える時間を、少しだけ大切にするきっかけになれば。</p>
    <h2>よくある質問</h2>''' + faq([
    ('縁起でもないと感じます。','残りを脅すためではなく、今ある時間を大切にするためのツールです。気が向いたときにそっとお使いください。'),
    ('データは送信されますか？','いいえ。入力した年齢などは外部に送信されません。')]),
  js='''  function calc(){
    const age=Math.max(0,+$('age').value||0), freq=Math.max(0,+$('freq').value||0), life=Math.max(0,+$('life').value||0);
    const ry=Math.max(0,life-age), times=ry*freq;
    $('sub').textContent=`${age}歳・年${freq}回・想定寿命${life}歳`;
    $('years').textContent=ry+'年'; $('f').textContent=freq+'回'; $('days').textContent=Math.round(times)+'日';
    SHARE=`親にこれから会えるのは、あと約${Math.round(times)}回らしい…👨‍👩‍👧\\n当たり前の時間にも限りがある。\\nあなたは？👇`;
    show(); anim($('big'),0,times,900);
  }'''))

# 7. 物価2倍まで何年
SIMS.append(dict(
  id='infure', cat='お金・時間', emoji='📉',
  title='インフレ・物価2倍シミュレーター｜今の1万円、何年で半分の価値？｜シミュラボ',
  desc='想定インフレ率を入れるだけで、物価が2倍になるまでの年数と、今のお金が将来どれだけ目減りするかを計算する無料シミュレーター。',
  ogtitle='インフレ・物価2倍シミュレーター｜今の1万円、何年で半分の価値？',
  ogdesc='インフレ率から、物価が2倍になるまでの年数と、お金の目減りを可視化。',
  h1='物価2倍まで何年？シミュレーター',
  lead='インフレが続くと、同じ金額で買えるものは少しずつ減っていきます。「タンス預金」が静かに目減りする様子を、年数とともに可視化します。',
  inputs='''    <h2>📉 条件を入れる</h2>
    <div class="row">
      <div class="field"><label>想定インフレ率 <span class="hint">（％／年）</span></label><input type="number" id="rate" value="2" min="0.1" max="30" step="0.1" inputmode="decimal"></div>
      <div class="field"><label>いまの金額 <span class="hint">（円・目減りの確認用）</span></label><input type="number" id="amount" value="1000000" min="0" inputmode="numeric"></div>
    </div>
    <button class="btn btn-primary" id="calcBtn">何年で2倍か見る</button>''',
  result='''      <div class="label">物価が2倍になるまで</div>
      <div class="big"><span id="big">0</span><span class="unit">年</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline">
        <div class="stat"><div class="k">10年後の実質価値</div><div class="v" id="y10">—</div></div>
        <div class="stat"><div class="k">20年後</div><div class="v" id="y20">—</div></div>
        <div class="stat"><div class="k">30年後</div><div class="v accent" id="y30">—</div></div>
      </div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>2倍になる年数 ＝ log(2) ÷ log(1 + インフレ率)<br>N年後の実質価値 ＝ 今の金額 ÷ (1 + インフレ率)^N</div>
    <p>年2%のインフレでも、物価は約35年で2倍に。逆に言えば、現金のまま持っている100万円の「買う力」は35年で半分になります。インフレ下では、現金だけで持つことにもリスクがあると言われる理由です。</p>
    <h2>よくある質問</h2>''' + faq([
    ('これは投資の勧誘ですか？','いいえ。インフレによるお金の目減りを体感するための教育的なツールで、特定の投資を勧めるものではありません。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const r=Math.max(0.001,(+$('rate').value||0)/100), amt=Math.max(0,+$('amount').value||0);
    const yrs=Math.log(2)/Math.log(1+r);
    const val=(n)=>amt/Math.pow(1+r,n);
    $('sub').textContent=`年${(r*100).toFixed(1)}%のインフレが続いた場合`;
    $('y10').textContent=yen(val(10)); $('y20').textContent=yen(val(20)); $('y30').textContent=yen(val(30));
    SHARE=`年${(r*100).toFixed(1)}%のインフレだと、物価は約${yrs.toFixed(1)}年で2倍に📉\\n今の${yen(amt)}は30年後に実質${yen(val(30))}の価値…\\n👇`;
    show(); anim($('big'),0,yrs,900,1);
  }'''))

# 8. もしあなたが会社だったら
SIMS.append(dict(
  id='if-company', cat='マーケティング', emoji='🏢',
  title='もしあなたが会社だったらシミュレーター｜あなたの時価総額は？｜シミュラボ',
  desc='年収・年間支出・貯金を入れると、あなたを「会社」に見立てて営業利益・利益率・時価総額・格付けを算出するくだらない無料シミュレーター。',
  ogtitle='もしあなたが会社だったらシミュレーター｜あなたの時価総額は？',
  ogdesc='年収・支出・貯金から、あなたを会社に見立てて時価総額と格付けを算出。',
  h1='もしあなたが会社だったら',
  lead='あなたを「1つの会社」に見立てたら、業績はどうなる？年収を売上、支出をコストとして、営業利益・利益率・時価総額・格付けをはじき出します（半分ネタです）。',
  inputs='''    <h2>🏢 あなたの“決算”を入れる</h2>
    <div class="row">
      <div class="field"><label>年収（＝売上） <span class="hint">（円）</span></label><input type="number" id="rev" value="5000000" min="0" inputmode="numeric"></div>
      <div class="field"><label>年間支出（＝コスト） <span class="hint">（円）</span></label><input type="number" id="cost" value="3500000" min="0" inputmode="numeric"></div>
    </div>
    <div class="field"><label>貯金（＝内部留保） <span class="hint">（円）</span></label><input type="number" id="save" value="2000000" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">あなたの会社を査定する</button>''',
  result='''      <div class="label">あなたの「時価総額」（ネタ）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline">
        <div class="stat"><div class="k">営業利益</div><div class="v" id="profit">—</div></div>
        <div class="stat"><div class="k">利益率</div><div class="v accent" id="margin">—</div></div>
        <div class="stat"><div class="k">格付け</div><div class="v" id="rank" style="font-size:17px;">—</div></div>
      </div>''',
  article='''    <h2>計算方法（ネタ）</h2>
    <div class="note"><strong>計算式</strong><br>営業利益 ＝ 年収 − 年間支出<br>時価総額 ＝ 営業利益 × 15（PER見立て）＋ 貯金</div>
    <p>会社の価値づけによく使われる「利益×PER」を、あなたの家計にあてはめた遊びです。利益率（=どれだけ手元に残せているか）や格付けで、自分という“事業体”の健全性をちょっと客観視できます。</p>
    <h2>よくある質問</h2>''' + faq([
    ('本当の価値ですか？','いいえ、あくまでお遊びの試算です。人の価値はお金で測れません。家計を見直すきっかけにどうぞ。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const rev=Math.max(0,+$('rev').value||0), cost=Math.max(0,+$('cost').value||0), save=Math.max(0,+$('save').value||0);
    const profit=rev-cost, margin=rev>0?profit/rev*100:0, cap=Math.max(0,profit)*15+save;
    let rank='C（再建中）'; if(margin>=40)rank='S（超優良）'; else if(margin>=25)rank='A（優良）'; else if(margin>=10)rank='B（健全）'; else if(margin>=0)rank='C（堅実）'; else rank='D（赤字）';
    $('sub').textContent=`売上${num(rev)}・コスト${num(cost)}・内部留保${num(save)}`;
    $('profit').textContent=yen(profit); $('margin').textContent=margin.toFixed(1)+'%'; $('rank').textContent=rank;
    SHARE=`私を会社に見立てると、時価総額 約${yen(cap)}・利益率${margin.toFixed(1)}%・格付け${rank}だった🏢\\n\\nあなたの会社は？👇`;
    show(); anim($('big'),0,cap,900);
  }'''))

# 9. 二度寝損失
SIMS.append(dict(
  id='nidone', cat='人生・自分ごと', emoji='🛌',
  title='二度寝損失シミュレーター｜今年、二度寝に溶かす時間は？｜シミュラボ',
  desc='二度寝の頻度と1回の長さから、1年で二度寝に費やす時間を計算。映画何本分・何日分かで体感できるくだらない無料シミュレーター。',
  ogtitle='二度寝損失シミュレーター｜今年、二度寝に溶かす時間は？',
  ogdesc='二度寝の頻度と長さから、1年で溶かす時間を映画何本分かで可視化。',
  h1='二度寝損失シミュレーター',
  lead='あの至福の二度寝。でも積み重ねると、けっこうな時間になっています。あなたが1年で二度寝に溶かす時間を計算します（罪悪感はほどほどに）。',
  inputs='''    <h2>🛌 条件を入れる</h2>
    <div class="row">
      <div class="field"><label>二度寝する頻度 <span class="hint">（週に何回）</span></label><input type="number" id="freq" value="4" min="0" max="21" inputmode="numeric"></div>
      <div class="field"><label>1回の長さ <span class="hint">（分）</span></label><input type="number" id="min" value="30" min="0" max="240" inputmode="numeric"></div>
    </div>
    <button class="btn btn-primary" id="calcBtn">溶かした時間を見る</button>''',
  result='''      <div class="label">1年で二度寝に溶かす時間</div>
      <div class="big"><span id="big">0</span><span class="unit">時間</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline">
        <div class="stat"><div class="k">映画(2時間)にすると</div><div class="v accent" id="movie">—</div></div>
        <div class="stat"><div class="k">まる何日分</div><div class="v" id="days">—</div></div>
        <div class="stat"><div class="k">1回の長さ</div><div class="v" id="one">—</div></div>
      </div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>1年の二度寝時間 ＝ 週の頻度 × 52週 × 1回の長さ</div>
    <p>週4回・30分の二度寝なら、1年で約104時間。映画にして50本以上、まる4日以上を二度寝に使っている計算です。とはいえ、二度寝の幸福度はプライスレス。ほどほどに楽しみましょう。</p>
    <h2>よくある質問</h2>''' + faq([
    ('二度寝は悪ですか？','いいえ。リラックス効果もあります。本ツールは罪悪感をあおるのではなく、時間の使い方を“見える化”するお遊びです。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const f=Math.max(0,+$('freq').value||0), m=Math.max(0,+$('min').value||0);
    const yMin=f*52*m, yH=yMin/60;
    $('sub').textContent=`週${f}回 × ${m}分 × 52週`;
    $('movie').textContent=Math.round(yMin/120)+'本'; $('days').textContent=(yMin/1440).toFixed(1)+'日'; $('one').textContent=m+'分';
    SHARE=`今年、二度寝に約${Math.round(yH)}時間（映画${Math.round(yMin/120)}本分）溶かす計算らしい…🛌\\n\\nあなたは？👇`;
    show(); anim($('big'),0,yH,900);
  }'''))

# 10. 塵も積もれば
SIMS.append(dict(
  id='chiritsumo', cat='お金・時間', emoji='🪙',
  title='塵も積もればシミュレーター｜毎日の小さな出費、10年でいくら？｜シミュラボ',
  desc='毎日の何気ない出費（缶コーヒーなど）と年数から、塵も積もった総額と、もし運用していた場合の金額を計算する無料シミュレーター。',
  ogtitle='塵も積もればシミュレーター｜毎日の小さな出費、10年でいくら？',
  ogdesc='毎日の小さな出費が、10年でいくらになる？運用していた場合との差も。',
  h1='塵も積もればシミュレーター',
  lead='毎日の缶コーヒー、コンビニのお菓子。1回は小さくても、積み重なると驚きの金額に。あなたの「塵」がどれだけ積もるかを計算します。',
  inputs='''    <h2>🪙 条件を入れる</h2>
    <div class="row">
      <div class="field"><label>毎日の何気ない出費 <span class="hint">（円・例: 缶コーヒー150）</span></label><input type="number" id="daily" value="300" min="0" inputmode="numeric"></div>
      <div class="field"><label>続ける年数 <span class="hint">（年）</span></label><input type="number" id="years" value="10" min="1" max="80" inputmode="numeric"></div>
    </div>
    <button class="btn btn-primary" id="calcBtn">積もった額を見る</button>''',
  result='''      <div class="label" id="lab">塵も積もって</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline">
        <div class="stat"><div class="k">1年あたり</div><div class="v" id="year">—</div></div>
        <div class="stat"><div class="k">年3%運用してたら</div><div class="v accent" id="inv">—</div></div>
        <div class="stat"><div class="k">買えるもの</div><div class="v" id="buy" style="font-size:15px;">—</div></div>
      </div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>総額 ＝ 1日の出費 × 365日 × 年数<br>運用比較 ＝ 毎年の出費額を年利3%で積立運用した場合の将来価値</div>
    <p>1日300円でも10年で約110万円。もし同じお金を年3%で積み立てていたら、さらに増えていた計算になります。やめる必要はありませんが、「何にいくら使っているか」を知るのは大事です。</p>
    <h2>よくある質問</h2>''' + faq([
    ('節約を強制するツールですか？','いいえ。出費の大きさを“見える化”するだけです。使う・使わないはあなたの自由です。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const d=Math.max(0,+$('daily').value||0), years=Math.max(1,+$('years').value||1);
    const annual=d*365, total=annual*years;
    let fv=0; for(let i=0;i<years;i++){ fv=(fv+annual)*1.03; }
    const buy = total>=2000000?'新車':total>=1000000?'高級腕時計':total>=300000?'海外旅行':total>=50000?'いい家電':'プチ贅沢';
    $('sub').textContent=`1日${num(d)}円 × 365日 × ${years}年`;
    $('year').textContent=yen(annual); $('inv').textContent=yen(fv); $('buy').textContent=buy;
    SHARE=`毎日${num(d)}円の出費、${years}年で約${yen(total)}…🪙（運用してたら${yen(fv)}）\\n塵も積もれば、ですね。\\nあなたは？👇`;
    show(); anim($('big'),0,total,900);
  }'''))

for s in SIMS:
    d = os.path.join(ROOT, 'sims', s['id'])
    os.makedirs(d, exist_ok=True)
    html = (TPL.replace('__TITLE__', s['title']).replace('__DESC__', s['desc'])
            .replace('__OGTITLE__', s['ogtitle']).replace('__OGDESC__', s['ogdesc'])
            .replace('__CAT__', s['cat']).replace('__H1__', s['h1']).replace('__LEAD__', s['lead'])
            .replace('__INPUTS__', s['inputs']).replace('__RESULT__', s['result'])
            .replace('__ARTICLE__', s['article']).replace('__JS__', s['js']).replace('__ID__', s['id']))
    with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print('created sims/' + s['id'] + '/index.html')
print(f'done. {len(SIMS)} sims.')
