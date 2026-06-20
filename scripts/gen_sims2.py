# -*- coding: utf-8 -*-
"""シミュラボ：追加シミュ第2弾をまとめて生成（gen_sims.pyと同じ枠）。"""
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

SIMS = []

# 1. 転職 年収if
SIMS.append(dict(id='tenshoku', cat='お金・時間', emoji='🔀',
  title='転職 年収ifシミュレーター｜転職すると生涯年収はどう変わる？｜シミュラボ',
  desc='今の年収と転職後の想定年収・昇給率・残り勤続年数から、転職した場合としなかった場合の生涯年収の差を計算する無料シミュレーター。',
  ogtitle='転職 年収ifシミュレーター｜生涯年収はどう変わる？', ogdesc='転職した場合としない場合の生涯年収の差を、昇給率込みで試算。',
  h1='転職 年収ifシミュレーター',
  lead='「あの時、転職していたら…」。今の年収と転職後の想定から、残りの働く年数でどれだけ生涯年収が変わるかを、昇給率込みで試算します。',
  inputs='''    <h2>🔀 条件を入れる</h2>
    <div class="row"><div class="field"><label>今の年収 <span class="hint">（万円）</span></label><input type="number" id="cur" value="400" min="0" inputmode="numeric"></div>
    <div class="field"><label>転職後の想定年収 <span class="hint">（万円）</span></label><input type="number" id="nw" value="500" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>現職の昇給率 <span class="hint">（％/年）</span></label><input type="number" id="rc" value="1" min="0" max="20" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>転職後の昇給率 <span class="hint">（％/年）</span></label><input type="number" id="rn" value="2.5" min="0" max="20" step="0.5" inputmode="decimal"></div></div>
    <div class="field"><label>あと何年働く <span class="hint">（年）</span></label><input type="number" id="years" value="20" min="1" max="50" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">生涯年収の差を見る</button>''',
  result='''      <div class="label" id="lab">転職すると、生涯年収が</div>
      <div class="big"><span id="big">0</span><span class="unit" id="unit">万円 増</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">現職のまま</div><div class="v" id="a">—</div></div>
      <div class="stat"><div class="k">転職した場合</div><div class="v accent" id="b">—</div></div>
      <div class="stat"><div class="k">残り勤続</div><div class="v" id="y">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>各年の年収を昇給率で複利計算し、残り勤続年数ぶん合計します。<br>差 ＝ 転職後の生涯年収 − 現職のままの生涯年収</div>
    <p>年収の差だけでなく「昇給率の差」が長期では大きく効きます。目先の額面だけでなく、伸びしろも含めて比較するのがポイントです。</p>
    <h2>よくある質問</h2>''' + faq([('退職金やボーナスは含まれますか？','いいえ。本ツールは年収ベースの概算です。退職金・賞与・福利厚生は別途考慮してください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const cur=Math.max(0,+$('cur').value||0)*10000, nw=Math.max(0,+$('nw').value||0)*10000;
    const rc=(+$('rc').value||0)/100, rn=(+$('rn').value||0)/100, y=Math.max(1,+$('years').value||1);
    let A=0,B=0; for(let t=0;t<y;t++){ A+=cur*Math.pow(1+rc,t); B+=nw*Math.pow(1+rn,t); }
    const diff=(B-A), up=diff>=0;
    $('unit').textContent= up?'万円 増':'万円 減';
    $('sub').textContent=`現職${(cur/10000)}万→転職${(nw/10000)}万・${y}年・昇給${(rc*100)}%/${(rn*100)}%`;
    $('a').textContent=num(A/10000)+'万円'; $('b').textContent=num(B/10000)+'万円'; $('y').textContent=y+'年';
    SHARE= up?`転職すると生涯年収が約${num(Math.abs(diff)/10000)}万円も増える計算だった🔀\\n\\nあなたは？👇`:`転職すると生涯年収が約${num(Math.abs(diff)/10000)}万円減る計算…慎重に🔀\\n👇`;
    show(); anim($('big'),0,Math.abs(diff)/10000,900);
  }'''))

# 2. FIRE
SIMS.append(dict(id='fire', cat='お金・時間', emoji='🔥',
  title='FIRE達成シミュレーター｜何年で経済的自由になれる？｜シミュラボ',
  desc='毎月の投資額・現在の資産・年間支出・想定利回りから、FIRE（経済的自立・早期リタイア）を達成できるまでの年数を計算する無料シミュレーター。',
  ogtitle='FIRE達成シミュレーター｜何年で経済的自由になれる？', ogdesc='毎月の投資額と利回りから、FIRE達成までの年数を試算。',
  h1='FIRE達成シミュレーター',
  lead='働かなくても資産の運用益で暮らせる状態＝FIRE。毎月の投資額と利回りから、あなたが何年でFIREに到達できるかを試算します。',
  inputs='''    <h2>🔥 条件を入れる</h2>
    <div class="row"><div class="field"><label>毎月の投資額 <span class="hint">（円）</span></label><input type="number" id="m" value="50000" min="0" inputmode="numeric"></div>
    <div class="field"><label>現在の資産 <span class="hint">（円）</span></label><input type="number" id="now" value="1000000" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>1年の生活費 <span class="hint">（円）</span></label><input type="number" id="cost" value="3000000" min="0" inputmode="numeric"></div>
    <div class="field"><label>想定利回り <span class="hint">（％/年）</span></label><input type="number" id="r" value="4" min="0" max="20" step="0.5" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">FIRE達成年数を見る</button>''',
  result='''      <div class="label">FIRE達成まで、あと</div>
      <div class="big"><span id="big">0</span><span class="unit">年</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">必要資産(年間支出×25)</div><div class="v accent" id="target">—</div></div>
      <div class="stat"><div class="k">年間の投資額</div><div class="v" id="ann">—</div></div>
      <div class="stat"><div class="k">達成時の年齢目安</div><div class="v" id="note2">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>必要資産 ＝ 年間支出 × 25（4%ルール）<br>毎年：資産 ＝ 資産 ×(1＋利回り) ＋ 年間投資額　を繰り返し、必要資産に届く年数を数える</div>
    <p>「4%ルール」は、資産の4%以内で生活すれば理論上 資産が尽きにくいとされる目安。だから必要資産は年間支出の25倍になります。利回りと積立額が大きいほど到達は早まります。</p>
    <h2>よくある質問</h2>''' + faq([('必ずこの年数で達成できますか？','いいえ。利回りは変動し、税・インフレもあります。あくまで一定利回りを仮定した概算です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const m=Math.max(0,+$('m').value||0), now=Math.max(0,+$('now').value||0), cost=Math.max(0,+$('cost').value||0), r=(+$('r').value||0)/100;
    const target=cost*25, ann=m*12; let a=now, y=0;
    while(a<target && y<100){ a=a*(1+r)+ann; y++; }
    $('sub').textContent=`月${num(m)}円積立・利回り${(r*100)}%・生活費${num(cost)}円`;
    $('target').textContent=yen(target); $('ann').textContent=yen(ann); $('note2').textContent=(y>=100?'100年超':'+'+y+'年後');
    SHARE= y>=100?`今の条件だとFIREは100年以上…条件を見直そう🔥\\n👇`:`私のFIRE達成まで、あと約${y}年らしい🔥（必要資産${yen(target)}）\\n\\nあなたは？👇`;
    show(); anim($('big'),0,Math.min(y,100),900);
  }'''))

# 3. あと何回給料日
SIMS.append(dict(id='kyuryobi', cat='お金・時間', emoji='📆',
  title='あと何回給料日シミュレーター｜定年まで残りの給料日は？｜シミュラボ',
  desc='今の年齢と定年から、定年までに受け取る給料日の残り回数を計算。働く時間の有限さを実感できる無料シミュレーター。',
  ogtitle='あと何回給料日シミュレーター｜定年まで残りの給料日は？', ogdesc='定年までに受け取る給料日の残り回数を計算。',
  h1='あと何回給料日シミュレーター',
  lead='毎月当たり前にやってくる給料日。でも定年までの回数は、実は数えられます。残りの給料日の回数を計算します。',
  inputs='''    <h2>📆 条件を入れる</h2>
    <div class="row"><div class="field"><label>今の年齢 <span class="hint">（歳）</span></label><input type="number" id="age" value="30" min="15" max="80" inputmode="numeric"></div>
    <div class="field"><label>定年の年齢 <span class="hint">（歳）</span></label><input type="number" id="ret" value="65" min="40" max="90" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">残りの給料日を見る</button>''',
  result='''      <div class="label">定年まで、給料日はあと</div>
      <div class="big"><span id="big">0</span><span class="unit">回</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">残りの年数</div><div class="v accent" id="y">—</div></div>
      <div class="stat"><div class="k">ボーナス(年2回)</div><div class="v" id="bonus">—</div></div>
      <div class="stat"><div class="k">残り月数</div><div class="v" id="mo">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>残りの給料日 ＝（定年 − 今の年齢）× 12回</div>
    <p>「まだまだ先」と思いがちな定年も、給料日の回数にすると有限だと実感できます。一回一回の使い方を、少し意識するきっかけに。</p>
    <h2>よくある質問</h2>''' + faq([('定年後の再雇用は？','本ツールは定年までの概算です。再雇用や年金は別途考慮してください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const age=Math.max(0,+$('age').value||0), ret=Math.max(0,+$('ret').value||0);
    const y=Math.max(0,ret-age), pays=y*12, bonus=y*2;
    $('sub').textContent=`${age}歳 → 定年${ret}歳`;
    $('y').textContent=y+'年'; $('bonus').textContent=bonus+'回'; $('mo').textContent=pays+'ヶ月';
    SHARE=`定年まで給料日はあと約${pays}回らしい📆\\n一回一回、大事にしよう。\\nあなたは？👇`;
    show(); anim($('big'),0,pays,900);
  }'''))

# 4. コーヒー一生分
SIMS.append(dict(id='coffee-life', cat='お金・時間', emoji='☕',
  title='コーヒー一生分シミュレーター｜生涯のコーヒー代とカフェイン量｜シミュラボ',
  desc='1日のコーヒー杯数・1杯の値段・続ける年数から、一生で飲むコーヒーの杯数・総額・カフェイン総量を計算する無料シミュレーター。',
  ogtitle='コーヒー一生分シミュレーター｜生涯のコーヒー代は？', ogdesc='一生で飲むコーヒーの杯数・総額・カフェイン量を計算。',
  h1='コーヒー一生分シミュレーター',
  lead='毎日の一杯のコーヒー。一生分にすると、どれだけの杯数とお金、そしてカフェインになるのでしょう。',
  inputs='''    <h2>☕ 条件を入れる</h2>
    <div class="row"><div class="field"><label>1日の杯数 <span class="hint">（杯）</span></label><input type="number" id="cups" value="2" min="0" max="30" inputmode="numeric"></div>
    <div class="field"><label>1杯の値段 <span class="hint">（円・店なら300〜、自宅なら30〜）</span></label><input type="number" id="price" value="200" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>続ける年数 <span class="hint">（年）</span></label><input type="number" id="years" value="40" min="1" max="90" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">一生分を見る</button>''',
  result='''      <div class="label">一生で飲むコーヒー代</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">総杯数</div><div class="v accent" id="cup">—</div></div>
      <div class="stat"><div class="k">カフェイン総量</div><div class="v" id="caf">—</div></div>
      <div class="stat"><div class="k">浴槽(200L)で</div><div class="v" id="bath">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>総額 ＝ 杯数 × 値段 × 365 × 年数<br>カフェイン ＝ 杯数 × 80mg × 365 × 年数</div>
    <p>1日2杯・40年でも、総額は数百万円・総杯数は約3万杯に。何気ない習慣も、一生分にするとスケールが見えてきます。</p>
    <h2>よくある質問</h2>''' + faq([('健康に悪いということですか？','いいえ。適量のコーヒーには良い面もあります。本ツールは習慣のスケールを可視化するお遊びです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const c=Math.max(0,+$('cups').value||0), p=Math.max(0,+$('price').value||0), y=Math.max(1,+$('years').value||1);
    const cups=c*365*y, total=cups*p, caf=c*80*365*y/1000;
    const liters=cups*0.15;
    $('sub').textContent=`1日${c}杯 × ${num(p)}円 × ${y}年`;
    $('cup').textContent=num(cups)+'杯'; $('caf').textContent=num(caf/1000)+'kg'; $('bath').textContent=(liters/200).toFixed(1)+'杯分';
    SHARE=`一生で飲むコーヒー、約${num(cups)}杯・${yen(total)}・カフェイン${num(caf/1000)}kg分らしい☕\\n\\nあなたは？👇`;
    show(); anim($('big'),0,total,900);
  }'''))

# 5. 酔いがさめるまで
SIMS.append(dict(id='yoi', cat='人生・自分ごと', emoji='🍺',
  title='酔いがさめるまでシミュレーター｜お酒は何時間で抜ける？｜シミュラボ',
  desc='飲んだお酒の量と体重から、アルコールが体から抜けるまでのおおよその時間を計算。翌朝の運転前チェックにも使える無料シミュレーター。',
  ogtitle='酔いがさめるまでシミュレーター｜お酒は何時間で抜ける？', ogdesc='飲んだ量と体重から、アルコールが抜けるまでの時間を概算。',
  h1='酔いがさめるまでシミュレーター',
  lead='飲んだお酒が体から抜けるまで、どれくらいかかるのか。飲んだ量と体重から、おおよその時間を計算します。翌朝の予定の目安に。',
  inputs='''    <h2>🍺 条件を入れる</h2>
    <div class="row"><div class="field"><label>ビール(中ジョッキ500ml)換算で何杯 <span class="hint">（杯）</span></label><input type="number" id="cups" value="3" min="0" max="50" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>体重 <span class="hint">（kg）</span></label><input type="number" id="kg" value="60" min="30" max="150" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">抜けるまでの時間を見る</button>''',
  result='''      <div class="label">アルコールが抜けるまで、約</div>
      <div class="big"><span id="big">0</span><span class="unit">時間</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">純アルコール量</div><div class="v accent" id="alc">—</div></div>
      <div class="stat"><div class="k">分解の目安速度</div><div class="v" id="rate">—</div></div>
      <div class="stat"><div class="k">体重</div><div class="v" id="w">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>純アルコール量(g) ＝ 杯数 × 500ml × 5% × 0.8<br>分解時間(h) ＝ 純アルコール量 ÷（体重kg × 0.1）<br><span style="font-size:13px">※1時間に体重×約0.1gのアルコールを分解すると仮定</span></div>
    <p>ビール3杯（純アルコール約60g）を体重60kgの人が飲むと、抜けるまで約10時間。意外と長く、翌朝まで残ることも。飲酒後の運転は、時間が経っていても絶対に避けてください。</p>
    <h2>よくある質問</h2>''' + faq([('これで運転して大丈夫か判断できますか？','いいえ。分解速度には大きな個人差があり、本ツールはあくまで概算です。少しでも不安があれば運転は控えてください。飲酒運転は法律で禁止されています。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const c=Math.max(0,+$('cups').value||0), kg=Math.max(1,+$('kg').value||1);
    const alc=c*500*0.05*0.8, hours=alc/(kg*0.1);
    $('sub').textContent=`ビール${c}杯・体重${kg}kg`;
    $('alc').textContent=Math.round(alc)+'g'; $('rate').textContent=(kg*0.1).toFixed(1)+'g/時'; $('w').textContent=kg+'kg';
    SHARE=`飲んだお酒が抜けるまで約${hours.toFixed(1)}時間かかるらしい…🍺（ビール${c}杯）\\n翌朝の運転は絶対NG。\\nあなたは？👇`;
    show(); anim($('big'),0,hours,900,1);
  }'''))

# 6. 半年後の体重
SIMS.append(dict(id='taiju', cat='人生・自分ごと', emoji='⚖️',
  title='半年後の体重シミュレーター｜今のカロリー収支だと何kg？｜シミュラボ',
  desc='今の体重と1日のカロリー収支（摂取−消費）から、半年後・1年後の体重を予測する無料シミュレーター。',
  ogtitle='半年後の体重シミュレーター｜今のカロリー収支だと何kg？', ogdesc='1日のカロリー収支から半年後・1年後の体重を予測。',
  h1='半年後の体重シミュレーター',
  lead='毎日のちょっとした食べ過ぎ・運動不足は、体重にじわじわ効いてきます。今のカロリー収支のままだと、半年後・1年後に何kgになるかを予測します。',
  inputs='''    <h2>⚖️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>今の体重 <span class="hint">（kg）</span></label><input type="number" id="kg" value="65" min="20" max="200" step="0.1" inputmode="decimal"></div>
    <div class="field"><label>1日のカロリー収支 <span class="hint">（摂取−消費 kcal・食べ過ぎは＋）</span></label><input type="number" id="bal" value="200" min="-2000" max="2000" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">半年後を予測する</button>''',
  result='''      <div class="label">このままだと半年後</div>
      <div class="big"><span id="big">0</span><span class="unit">kg</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1ヶ月の変化</div><div class="v accent" id="mo">—</div></div>
      <div class="stat"><div class="k">1年後</div><div class="v" id="y1">—</div></div>
      <div class="stat"><div class="k">変化量(半年)</div><div class="v" id="d">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>体脂肪1kg ≒ 約7,200kcal<br>体重変化 ＝ 1日のカロリー収支 × 日数 ÷ 7,200</div>
    <p>1日たった+200kcal（おにぎり1個ぶん）でも、半年で約5kg増える計算。逆にマイナス収支なら同じペースで減ります。小さな差の積み重ねが体重を作ります。</p>
    <h2>よくある質問</h2>''' + faq([('この通りに増減しますか？','いいえ。実際は代謝の変化や水分などで単純には進みません。あくまで収支の目安としてお使いください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const kg=Math.max(0,+$('kg').value||0), bal=+$('bal').value||0;
    const half=bal*182/7200, year=bal*365/7200, mo=bal*30/7200;
    const after=kg+half;
    $('sub').textContent=`今${kg}kg・1日 ${bal>=0?'+':''}${bal}kcal`;
    $('mo').textContent=(mo>=0?'+':'')+mo.toFixed(1)+'kg'; $('y1').textContent=(kg+year).toFixed(1)+'kg'; $('d').textContent=(half>=0?'+':'')+half.toFixed(1)+'kg';
    SHARE=`今のカロリー収支のままだと、半年後 約${after.toFixed(1)}kg（${half>=0?'+':''}${half.toFixed(1)}kg）になる予測…⚖️\\nあなたは？👇`;
    show(); anim($('big'),0,after,900,1);
  }'''))

# 7. 運命の人に出会う確率
SIMS.append(dict(id='unmei', cat='人生・自分ごと', emoji='💘',
  title='運命の人に出会う確率シミュレーター｜あなたの理想の相手は何人いる？｜シミュラボ',
  desc='地域の人口・年齢・独身率・価値観の一致度から、あなたの「運命の人」候補が何人いて、出会う確率がどれくらいかを計算する無料シミュレーター。',
  ogtitle='運命の人に出会う確率シミュレーター｜理想の相手は何人いる？', ogdesc='人口・条件から、あなたの運命の人候補と出会う確率を試算。',
  h1='運命の人に出会う確率',
  lead='広い世界に、あなたの「運命の人」は何人いるのでしょう。地域の人口と条件から、候補者数と出会う確率を（半分まじめに）計算します。',
  inputs='''    <h2>💘 条件を入れる</h2>
    <div class="row"><div class="field"><label>住んでいる地域の人口 <span class="hint">（万人）</span></label><input type="number" id="pop" value="50" min="1" max="5000" inputmode="numeric"></div>
    <div class="field"><label>年齢が合う割合 <span class="hint">（％）</span></label><input type="number" id="age" value="20" min="0" max="100" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>独身の割合 <span class="hint">（％）</span></label><input type="number" id="single" value="35" min="0" max="100" inputmode="numeric"></div>
    <div class="field"><label>価値観・好みが合う割合 <span class="hint">（％）</span></label><input type="number" id="pref" value="8" min="0" max="100" step="0.5" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">運命の人を数える</button>''',
  result='''      <div class="label">あなたの「運命の人」候補は</div>
      <div class="big"><span id="big">0</span><span class="unit">人</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">街でrandom遭遇する確率</div><div class="v accent" id="prob">—</div></div>
      <div class="stat"><div class="k">対象人口</div><div class="v" id="base">—</div></div>
      <div class="stat"><div class="k">難易度</div><div class="v" id="lv" style="font-size:16px;">—</div></div></div>''',
  article='''    <h2>計算方法（半分まじめ）</h2>
    <div class="note"><strong>計算式</strong><br>候補者 ＝ 人口 × 性別50% × 年齢が合う割合 × 独身率 × 価値観の一致率</div>
    <p>有名な「ドレイク方程式（宇宙人がいる数の推定式）」を恋愛に当てはめた遊びです。条件を厳しくするほど候補は一気に減ります。だからこそ、出会えたら奇跡なのかもしれません。</p>
    <h2>よくある質問</h2>''' + faq([('これは本当の確率ですか？','いいえ、あくまでお遊びの試算です。実際の出会いは確率では測れません。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const pop=Math.max(0,+$('pop').value||0)*10000, age=(+$('age').value||0)/100, single=(+$('single').value||0)/100, pref=(+$('pref').value||0)/100;
    const cand=pop*0.5*age*single*pref;
    const prob= cand>0? pop/cand : Infinity;
    let lv= cand>=1000?'イージー':cand>=100?'ノーマル':cand>=10?'ハード':cand>=1?'ベリーハード':'奇跡レベル';
    $('sub').textContent=`人口${num(pop)}人・年齢${(age*100)}%・独身${(single*100)}%・好み${(pref*100)}%`;
    $('prob').textContent= isFinite(prob)?('約 1/'+num(prob)+'人'):'—'; $('base').textContent=num(pop)+'人'; $('lv').textContent=lv;
    SHARE=`私の街に「運命の人」候補は約${num(cand)}人らしい💘（難易度：${lv}）\\n\\nあなたは？👇`;
    show(); anim($('big'),0,cand,900);
  }'''))

# 8. 精神年齢診断
SIMS.append(dict(id='mental-age', cat='人生・自分ごと', emoji='🧠',
  title='精神年齢診断｜あなたのおじさん・おばさん度は？｜シミュラボ',
  desc='5つの質問に答えるだけで、あなたの精神年齢と「おじさん・おばさん度」を診断するくだらない無料シミュレーター。',
  ogtitle='精神年齢診断｜あなたのおじさん・おばさん度は？', ogdesc='5つの質問で、あなたの精神年齢とおじさん度を診断。',
  h1='精神年齢診断',
  lead='実年齢と、心の年齢は別もの。5つの質問に答えるだけで、あなたの「精神年齢」と、ちょっと気になる「おじさん・おばさん度」を診断します。',
  inputs='''    <h2>🧠 5つの質問に答える</h2>
    <div class="field"><label>① メッセージの最後に「。」を付ける？</label><select id="q1"><option value="8">きっちり付ける</option><option value="3" selected>気分しだい</option><option value="0">ほぼ付けない</option></select></div>
    <div class="field"><label>② LINEで絵文字・スタンプを使う？</label><select id="q2"><option value="-5">たくさん使う</option><option value="2" selected>ほどほど</option><option value="6">ほぼ使わない</option></select></div>
    <div class="field"><label>③ 休日の理想は？</label><select id="q3"><option value="-4">外でアクティブに</option><option value="2" selected>予定を少し入れる</option><option value="5">家でのんびり</option></select></div>
    <div class="field"><label>④ 新しいアプリ・SNSが出たら？</label><select id="q4"><option value="-6">すぐ試す</option><option value="3" selected>様子を見る</option><option value="9">特に興味ない</option></select></div>
    <div class="field"><label>⑤ 飲み会の二次会は？</label><select id="q5"><option value="-3">まだまだ行きたい</option><option value="4" selected>そろそろ解散したい</option><option value="7">一次会で十分</option></select></div>
    <button class="btn btn-primary" id="calcBtn">精神年齢を診断する</button>''',
  result='''      <div class="label">あなたの精神年齢は</div>
      <div class="big"><span id="big">0</span><span class="unit">歳</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">おじ・おば度</div><div class="v accent" id="ojisan">—</div></div>
      <div class="stat"><div class="k">タイプ</div><div class="v" id="type" style="font-size:16px;">—</div></div></div>''',
  article='''    <h2>この診断について</h2>
    <p>普段の何気ない振る舞いから、心の年齢を推定するお遊び診断です。実年齢とのギャップを楽しんでください（結果に深い意味はありません）。</p>
    <h2>よくある質問</h2>''' + faq([('当たっていますか？','あくまでエンタメ診断です。当たっても当たらなくても、笑って楽しんでください。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    let s=20; for(const q of ['q1','q2','q3','q4','q5']) s+=(+$(q).value||0);
    s=Math.max(12,Math.min(75,s));
    const oj=Math.max(0,Math.min(100,Math.round((s-18)/0.45)));
    let t= s<25?'永遠の若者タイプ':s<38?'等身大タイプ':s<52?'ちょい大人タイプ':'達観・老成タイプ';
    $('sub').textContent='普段の振る舞いから推定';
    $('ojisan').textContent=oj+'%'; $('type').textContent=t;
    SHARE=`精神年齢診断、私は${s}歳（おじ・おば度${oj}%・${t}）でした🧠\\n\\nあなたは？👇`;
    show(); anim($('big'),0,s,900);
  }'''))

# 9. 異世界転生チート度
SIMS.append(dict(id='isekai', cat='人生・自分ごと', emoji='🗡️',
  title='異世界転生チート度診断｜あなたは異世界でどれだけ無双できる？｜シミュラボ',
  desc='現代のスキルや知識から、もし異世界に転生したらどれだけ「チート」になれるかを診断するくだらない無料シミュレーター。',
  ogtitle='異世界転生チート度診断｜あなたは異世界で無双できる？', ogdesc='現代のスキルから、異世界転生したときのチート度を診断。',
  h1='異世界転生チート度診断',
  lead='もし今のあなたが異世界に転生したら、どれだけ無双できる？現代の知識とスキルを、異世界の戦闘力に換算して診断します。',
  inputs='''    <h2>🗡️ あなたのスペックを選ぶ</h2>
    <div class="field"><label>① 職業・専門は？</label><select id="q1"><option value="30">エンジニア・技術職</option><option value="26">医療・看護</option><option value="22">研究・専門職</option><option value="18" selected>事務・営業</option><option value="20">職人・ものづくり</option><option value="12">学生</option></select></div>
    <div class="field"><label>② いちばんの特技は？</label><select id="q2"><option value="20">ものづくり・DIY</option><option value="18">体力・運動</option><option value="15">交渉・話術</option><option value="12">語学</option><option value="6" selected>特になし</option></select></div>
    <div class="field"><label>③ 現代知識のレベルは？</label><select id="q3"><option value="25">理系の知識が豊富</option><option value="18">雑学・歴史に強い</option><option value="10" selected>人並み</option></select></div>
    <div class="field"><label>④ メンタルの強さは？</label><select id="q4"><option value="15">何があっても図太い</option><option value="8" selected>普通</option><option value="3">豆腐メンタル</option></select></div>
    <button class="btn btn-primary" id="calcBtn">チート度を診断する</button>''',
  result='''      <div class="label">あなたの異世界チート度</div>
      <div class="big"><span id="big">0</span><span class="unit">/100</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">異世界での称号</div><div class="v accent" id="title" style="font-size:16px;">—</div></div>
      <div class="stat"><div class="k">推定生存率</div><div class="v" id="surv">—</div></div></div>''',
  article='''    <h2>この診断について</h2>
    <p>現代のスキルや知識は、文明レベルの低い異世界では「チート」になり得る…という妄想を数値化したお遊びです。結果はネタとしてお楽しみください。</p>
    <h2>よくある質問</h2>''' + faq([('本当に異世界で通用しますか？','異世界はまだ発見されていないため検証不能です。あくまでエンタメ診断としてお楽しみください。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    let s=0; for(const q of ['q1','q2','q3','q4']) s+=(+$(q).value||0); s=Math.max(0,Math.min(100,s));
    let t= s>=85?'魔王級チート':s>=70?'伝説の勇者':s>=50?'一流の冒険者':s>=30?'街の便利屋':'村人A';
    const surv=Math.min(99,40+s*0.6);
    $('sub').textContent='現代スキルを異世界戦闘力に換算';
    $('title').textContent=t; $('surv').textContent=Math.round(surv)+'%';
    SHARE=`異世界転生したら、私のチート度は${s}/100（称号：${t}）でした🗡️\\n\\nあなたは？👇`;
    show(); anim($('big'),0,s,900);
  }'''))

# 10. 値上げ客数シミュ
SIMS.append(dict(id='neage', cat='マーケティング', emoji='🏷️',
  title='値上げ客数シミュレーター｜価格を上げたら売上はどう動く？｜シミュラボ',
  desc='現在の価格・客数と値上げ後の価格、価格弾力性から、値上げによる客数の変化と売上への影響を試算する無料シミュレーター。お店の値付けの参考に。',
  ogtitle='値上げ客数シミュレーター｜価格を上げたら売上はどう動く？', ogdesc='値上げで客数はどれだけ減る？売上はプラス？価格弾力性から試算。',
  h1='値上げ客数シミュレーター',
  lead='値上げしたいけど、お客さんが減るのが怖い——。価格を上げたとき、客数と売上がどう動くかを「価格弾力性」から試算します。',
  inputs='''    <h2>🏷️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>今の価格 <span class="hint">（円）</span></label><input type="number" id="p0" value="1000" min="0" inputmode="numeric"></div>
    <div class="field"><label>値上げ後の価格 <span class="hint">（円）</span></label><input type="number" id="p1" value="1100" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>今の客数 <span class="hint">（月・人）</span></label><input type="number" id="q" value="500" min="0" inputmode="numeric"></div>
    <div class="field"><label>価格への敏感さ（弾力性）</label><select id="e"><option value="-0.5">低い（こだわり・常連が多い）</option><option value="-1.0" selected>普通</option><option value="-1.6">高い（価格で選ばれている）</option></select></div>
    <button class="btn btn-primary" id="calcBtn">売上への影響を見る</button>''',
  result='''      <div class="label" id="lab">値上げで月の売上は</div>
      <div class="big"><span id="big">0</span><span class="unit" id="unit">円 増</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">値上げ後の客数</div><div class="v accent" id="q1">—</div></div>
      <div class="stat"><div class="k">値上げ前の売上</div><div class="v" id="s0">—</div></div>
      <div class="stat"><div class="k">値上げ後の売上</div><div class="v" id="s1">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>客数の変化率 ＝ 価格弾力性 × 価格の変化率<br>値上げ後の客数 ＝ 今の客数 ×（1＋客数の変化率）<br>売上 ＝ 価格 × 客数</div>
    <p>「価格弾力性」は、価格が1%上がると客数が何%減るかを表す指標。こだわりや常連が多い店ほど客離れは小さく、値上げが売上増につながりやすくなります。</p>
    <h2>値上げ前にやっておきたいこと</h2>
    <ul><li><strong>価値を伝える</strong> ― 質や体験を発信すると、価格への敏感さが下がります。</li><li><strong>口コミ・MEOで「選ばれる理由」をつくる</strong> ― 価格以外で選ばれると値上げに強くなります。</li></ul>
    <div class="note">「価格で選ばれない店」をつくるMEO・口コミ運用のご相談は <a href="../../contact/index.html">こちら</a>。</div>
    <h2>よくある質問</h2>''' + faq([('弾力性はどう選べばいい？','常連・固定客が中心なら「低い」、価格比較されやすい商品なら「高い」が目安です。実際は商品ごとに異なります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const p0=Math.max(0,+$('p0').value||0), p1=Math.max(0,+$('p1').value||0), q0=Math.max(0,+$('q').value||0), e=+$('e').value||-1;
    const dp= p0>0? (p1-p0)/p0 : 0;
    const q1=Math.max(0, q0*(1+e*dp));
    const s0=p0*q0, s1=p1*q1, diff=s1-s0, up=diff>=0;
    $('unit').textContent= up?'円 増':'円 減';
    $('sub').textContent=`${num(p0)}→${num(p1)}円（${(dp*100).toFixed(0)}%値上げ）・弾力性${e}`;
    $('q1').textContent=num(q1)+'人'; $('s0').textContent=yen(s0); $('s1').textContent=yen(s1);
    SHARE= up?`${(dp*100).toFixed(0)}%の値上げで、客数は${num(q1)}人に減るけど売上は約${yen(Math.abs(diff))}増える試算🏷️\\nあなたのお店は？👇`:`${(dp*100).toFixed(0)}%値上げすると売上は約${yen(Math.abs(diff))}減る試算…慎重に🏷️\\n👇`;
    show(); anim($('big'),0,Math.abs(diff),900);
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
    print('created sims/' + s['id'])
print(f'done. {len(SIMS)} sims.')
