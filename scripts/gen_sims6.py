# -*- coding: utf-8 -*-
"""シミュラボ：新カテゴリ4種に3本ずつ追加（計12本）。"""
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
SIMS.append(dict(id='bep', cat=BIZ, emoji='⚖️',
  title='損益分岐点シミュレーター｜あと何人来れば黒字？｜シミュラボ',
  desc='月の固定費・粗利率・客単価から、お店が黒字になる損益分岐点の売上と、必要な客数（月・1日）を計算する無料シミュレーター。',
  ogtitle='損益分岐点シミュレーター｜あと何人来れば黒字？', ogdesc='固定費と粗利率から、黒字に必要な売上と客数を計算。',
  h1='損益分岐点シミュレーター',
  lead='お店が赤字を抜けて黒字になるのは、月いくら売れたとき？固定費と粗利率から、損益分岐点の売上と必要な客数を計算します。',
  inputs='''    <h2>⚖️ 条件</h2>
    <div class="row"><div class="field"><label>月の固定費 <span class="hint">（家賃・人件費など・円）</span></label><input type="number" id="fc" value="800000" min="0" inputmode="numeric"></div>
    <div class="field"><label>粗利率 <span class="hint">（％）</span></label><input type="number" id="gp" value="40" min="1" max="100" inputmode="numeric"></div></div>
    <div class="field"><label>客単価 <span class="hint">（円）</span></label><input type="number" id="aov" value="3000" min="1" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">損益分岐点を計算する</button>''',
  result='''      <div class="label">黒字になる月商（損益分岐点）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">必要な客数（月）</div><div class="v accent" id="cust">—</div></div>
      <div class="stat"><div class="k">1日あたり(26日)</div><div class="v" id="day">—</div></div>
      <div class="stat"><div class="k">粗利率</div><div class="v" id="gp2">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>損益分岐売上＝固定費÷粗利率<br>必要客数＝損益分岐売上÷客単価</div>
    <p>固定費を粗利でまかなえる売上が損益分岐点。これを「1日あたりの客数」に落とすと、目標が一気に身近になります。</p>
    <h2>よくある質問</h2>'''+faq([('変動費は？','本ツールは粗利率に変動費を織り込んだ簡易版です。より精密には変動費・固定費を分けて計算します。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const fc=Math.max(0,+$('fc').value||0), gp=(+$('gp').value||1)/100, aov=Math.max(1,+$('aov').value||1);
    const bep=fc/gp, cust=bep/aov;
    $('sub').textContent=`固定費${num(fc)}円・粗利${(gp*100)}%・客単価${num(aov)}円`;
    $('cust').textContent=num(cust)+'人'; $('day').textContent=num(cust/26)+'人/日'; $('gp2').textContent=(gp*100)+'%';
    SHARE=`うちの損益分岐点は月商${yen(bep)}・客数${num(cust)}人だった⚖️（1日約${num(cust/26)}人）\\nあなたのお店は？👇`;
    show(); anim($('big'),0,bep,900);
  }'''))

SIMS.append(dict(id='noshow', cat=BIZ, emoji='🚫',
  title='ノーショー損失シミュレーター｜無断キャンセルでいくら損してる？｜シミュラボ',
  desc='月の予約件数・キャンセル率・客単価から、予約の無断キャンセル（ノーショー）で失っている金額を月・年で試算する無料シミュレーター。',
  ogtitle='ノーショー損失シミュレーター｜無断キャンセルの損失', ogdesc='予約の無断キャンセルで失う金額を月・年で試算。',
  h1='ノーショー損失シミュレーター',
  lead='予約の無断キャンセル（ノーショー）。1件ずつは小さくても、積み重なると大きな損失です。あなたのお店の損失額を試算します。',
  inputs='''    <h2>🚫 条件</h2>
    <div class="row"><div class="field"><label>月の予約件数 <span class="hint">（件）</span></label><input type="number" id="rsv" value="200" min="0" inputmode="numeric"></div>
    <div class="field"><label>キャンセル・無断率 <span class="hint">（％）</span></label><input type="number" id="rate" value="8" min="0" max="100" step="0.5" inputmode="decimal"></div></div>
    <div class="row"><div class="field"><label>1件の平均客単価 <span class="hint">（円）</span></label><input type="number" id="aov" value="4000" min="0" inputmode="numeric"></div>
    <div class="field"><label>席を埋め直せる率 <span class="hint">（％）</span></label><input type="number" id="refill" value="30" min="0" max="100" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">損失額を見る</button>''',
  result='''      <div class="label">ノーショーによる月の損失</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">年間の損失</div><div class="v accent" id="yr">—</div></div>
      <div class="stat"><div class="k">月のキャンセル件数</div><div class="v" id="cnt">—</div></div>
      <div class="stat"><div class="k">埋め直せる率</div><div class="v" id="rf">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>損失＝予約件数×キャンセル率×客単価×(1−埋め直せる率)</div>
    <p>ノーショー対策には、事前決済・リマインド連絡・キャンセルポリシーの明示が効果的です。数字にすると、対策する価値が見えてきます。</p>
    <h2>よくある質問</h2>'''+faq([('当日キャンセルも含む？','「埋め直せる率」で当日穴埋めの可能性を反映しています。状況に合わせて調整してください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const rsv=Math.max(0,+$('rsv').value||0), rate=(+$('rate').value||0)/100, aov=Math.max(0,+$('aov').value||0), rf=(+$('refill').value||0)/100;
    const cnt=rsv*rate, loss=cnt*aov*(1-rf);
    $('sub').textContent=`予約${rsv}件・キャンセル${(rate*100)}%・単価${num(aov)}円`;
    $('yr').textContent=yen(loss*12); $('cnt').textContent=num(cnt)+'件'; $('rf').textContent=(rf*100)+'%';
    SHARE=`無断キャンセルの損失、うちは月${yen(loss)}・年${yen(loss*12)}だった🚫\\n対策する価値あり。あなたのお店は？👇`;
    show(); anim($('big'),0,loss,900);
  }'''))

SIMS.append(dict(id='jinkenhi', cat=BIZ, emoji='👥',
  title='人件費率診断シミュレーター｜うちの人件費、高すぎ？適正？｜シミュラボ',
  desc='月商と人件費から人件費率を計算し、業種別の目安と比べて高い・適正かを診断する無料シミュレーター。お店・会社の経営チェックに。',
  ogtitle='人件費率診断｜うちの人件費、高すぎ？適正？', ogdesc='月商と人件費から人件費率を計算、業種別目安と比較。',
  h1='人件費率診断シミュレーター',
  lead='売上に対する人件費の割合（人件費率）は、経営の健康診断のひとつ。あなたのお店の人件費率を、業種の目安と比べて診断します。',
  inputs='''    <h2>👥 条件</h2>
    <div class="row"><div class="field"><label>月商（売上） <span class="hint">（円）</span></label><input type="number" id="sales" value="3000000" min="1" inputmode="numeric"></div>
    <div class="field"><label>月の人件費 <span class="hint">（円・社保込み）</span></label><input type="number" id="labor" value="900000" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>業種（目安比較用）</label><select id="biz"><option value="30">飲食店（目安30%）</option><option value="15">小売・物販（目安15%）</option><option value="40">サービス・美容（目安40%）</option><option value="25">その他（目安25%）</option></select></div>
    <button class="btn btn-primary" id="calcBtn">人件費率を診断する</button>''',
  result='''      <div class="label">あなたのお店の人件費率</div>
      <div class="big"><span id="big">0</span><span class="unit">%</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">業種の目安</div><div class="v" id="std">—</div></div>
      <div class="stat"><div class="k">目安との差</div><div class="v accent" id="diff">—</div></div>
      <div class="stat"><div class="k">判定</div><div class="v" id="judge" style="font-size:16px;">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>人件費率＝人件費÷月商×100</div>
    <p>人件費率は低ければ良いわけではなく、低すぎると人手不足・サービス低下のサインにも。業種の目安と比べてバランスを見るのが大切です。</p>
    <h2>よくある質問</h2>'''+faq([('目安は絶対？','業態・立地で適正値は変わります。あくまで一般的な目安としてお使いください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const sales=Math.max(1,+$('sales').value||1), labor=Math.max(0,+$('labor').value||0), std=+$('biz').value;
    const rate=labor/sales*100, diff=rate-std;
    let j= diff>8?'やや高め':diff<-8?'やや低め':'おおむね適正';
    $('sub').textContent=`月商${num(sales)}円・人件費${num(labor)}円`;
    $('std').textContent=std+'%'; $('diff').textContent=(diff>=0?'+':'')+diff.toFixed(1)+'pt'; $('judge').textContent=j;
    SHARE=`うちの人件費率は${rate.toFixed(1)}%、業種目安${std}%に対して「${j}」だった👥\\nあなたのお店は？👇`;
    show(); anim($('big'),0,rate,900,1);
  }'''))

# ===== マネー・保険・不動産 =====
SIMS.append(dict(id='nisa', cat=FIN, emoji='📈',
  title='NISA積立シミュレーター｜毎月の積立、何年でいくらになる？｜シミュラボ',
  desc='毎月の積立額・想定利回り・年数から、将来の資産額と運用益を複利で計算する無料の積立投資（NISA）シミュレーター。',
  ogtitle='NISA積立シミュレーター｜将来いくらになる？', ogdesc='毎月の積立と利回りから、将来資産と運用益を複利で計算。',
  h1='NISA積立シミュレーター',
  lead='毎月コツコツ積み立てると、複利の力で資産はどこまで育つ？積立額・利回り・年数から、将来の資産と運用益を計算します。',
  inputs='''    <h2>📈 条件</h2>
    <div class="row"><div class="field"><label>毎月の積立額 <span class="hint">（円）</span></label><input type="number" id="m" value="30000" min="0" inputmode="numeric"></div>
    <div class="field"><label>想定利回り <span class="hint">（％/年）</span></label><input type="number" id="r" value="5" min="0" max="20" step="0.5" inputmode="decimal"></div></div>
    <div class="field"><label>積立年数 <span class="hint">（年）</span></label><input type="number" id="y" value="20" min="1" max="60" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">将来資産を計算する</button>''',
  result='''      <div class="label" id="lab">◯年後の資産</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">積み立てた元本</div><div class="v" id="moto">—</div></div>
      <div class="stat"><div class="k">運用益</div><div class="v accent" id="eki">—</div></div>
      <div class="stat"><div class="k">元本に対して</div><div class="v" id="x">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>毎月の積立を、想定利回りで毎月複利運用した場合の将来価値（積立額×{(1+月利)^回数−1}÷月利）</div>
    <p>同じ積立額でも、期間が長いほど「運用益」の割合がぐんと増えます。これが複利の力。早く始めるほど有利になります（投資には元本割れリスクがあります）。</p>
    <h2>よくある質問</h2>'''+faq([('元本割れは？','本ツールは一定利回りを仮定した試算で、実際の相場は変動します。リスクを理解して始めましょう。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const m=Math.max(0,+$('m').value||0), r=(+$('r').value||0)/100/12, y=Math.max(1,+$('y').value||1), n=y*12;
    const fv = r>0 ? m*((Math.pow(1+r,n)-1)/r) : m*n;
    const moto=m*n, eki=fv-moto;
    $('lab').textContent=y+'年後の資産';
    $('sub').textContent=`毎月${num(m)}円・利回り${(+$('r').value)}%・${y}年`;
    $('moto').textContent=yen(moto); $('eki').textContent=yen(eki); $('x').textContent='約'+(fv/moto).toFixed(2)+'倍';
    SHARE=`NISA積立シミュ：毎月${num(m)}円を${y}年で${yen(fv)}に（運用益${yen(eki)}）📈\\nあなたは？👇`;
    show(); anim($('big'),0,fv,900);
  }'''))

SIMS.append(dict(id='kuruma-iji', cat=FIN, emoji='🚙',
  title='車の維持費シミュレーター｜年間・生涯でいくらかかる？｜シミュラボ',
  desc='ガソリン代・保険・車検・駐車場・税金から、車の年間維持費と保有期間の総額を計算する無料シミュレーター。',
  ogtitle='車の維持費シミュレーター｜年間・生涯でいくら？', ogdesc='ガソリン・保険・車検・駐車場・税金から年間維持費と総額を計算。',
  h1='車の維持費シミュレーター',
  lead='車は買ったあとも、ガソリン・保険・車検…とお金がかかります。あなたの車の年間維持費と、保有期間の総額を計算します。',
  inputs='''    <h2>🚙 年間でかかる費用</h2>
    <div class="row"><div class="field"><label>ガソリン代 <span class="hint">（円/年）</span></label><input type="number" id="gas" value="120000" min="0" inputmode="numeric"></div>
    <div class="field"><label>任意保険 <span class="hint">（円/年）</span></label><input type="number" id="ins" value="60000" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>車検・整備（年あたり） <span class="hint">（円/年）</span></label><input type="number" id="shaken" value="80000" min="0" inputmode="numeric"></div>
    <div class="field"><label>自動車税 <span class="hint">（円/年）</span></label><input type="number" id="tax" value="34500" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>駐車場 <span class="hint">（円/月）</span></label><input type="number" id="park" value="10000" min="0" inputmode="numeric"></div>
    <div class="field"><label>何年乗る？ <span class="hint">（年）</span></label><input type="number" id="years" value="10" min="1" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">維持費を計算する</button>''',
  result='''      <div class="label">年間の維持費</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">月あたり</div><div class="v" id="mo">—</div></div>
      <div class="stat"><div class="k" id="ylab">保有期間の総額</div><div class="v accent" id="total">—</div></div>
      <div class="stat"><div class="k">いちばん高い費目</div><div class="v" id="top" style="font-size:15px;">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>年間維持費＝ガソリン＋保険＋車検＋税金＋駐車場×12<br>総額＝年間維持費×保有年数</div>
    <p>車両本体価格とは別に、維持費だけで年間数十万円。カーシェアや公共交通と比べる判断材料にどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([('車両ローンは含む？','本ツールは維持費のみ。ローンや車両価格は別途加算してください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const gas=+$('gas').value||0,ins=+$('ins').value||0,sh=+$('shaken').value||0,tax=+$('tax').value||0,park=(+$('park').value||0)*12,y=Math.max(1,+$('years').value||1);
    const year=gas+ins+sh+tax+park, total=year*y;
    const items=[['ガソリン',gas],['任意保険',ins],['車検・整備',sh],['自動車税',tax],['駐車場',park]].sort((a,b)=>b[1]-a[1]);
    $('sub').textContent='年間の合計維持費';
    $('mo').textContent=yen(year/12); $('ylab').textContent=y+'年の総額'; $('total').textContent=yen(total); $('top').textContent=items[0][0]+'('+yen(items[0][1])+')';
    SHARE=`車の維持費、年${yen(year)}・${y}年で${yen(total)}だった🚙\\nあなたの車は？👇`;
    show(); anim($('big'),0,year,900);
  }'''))

SIMS.append(dict(id='furusato', cat=FIN, emoji='🎁',
  title='ふるさと納税 上限額シミュレーター｜いくらまでお得？｜シミュラボ',
  desc='年収と家族構成から、ふるさと納税で自己負担2,000円に収まる寄付の上限額の目安を試算する無料シミュレーター。',
  ogtitle='ふるさと納税 上限額シミュレーター｜いくらまでお得？', ogdesc='年収と家族構成から、ふるさと納税の上限額の目安を試算。',
  h1='ふるさと納税 上限額シミュレーター',
  lead='ふるさと納税は、上限額までなら自己負担2,000円で返礼品がもらえるお得な制度。あなたの上限額の目安を年収から試算します。',
  inputs='''    <h2>🎁 条件</h2>
    <div class="field"><label>年収（額面） <span class="hint">（万円）</span></label><input type="number" id="income" value="500" min="100" max="5000" inputmode="numeric"></div>
    <div class="field"><label>家族構成</label><select id="fam">
      <option value="1.0">独身 または 共働き（扶養なし）</option>
      <option value="0.86">夫婦（配偶者を扶養）</option>
      <option value="0.78">夫婦＋子1人（高校生）</option>
      <option value="0.70">夫婦＋子2人</option></select></div>
    <button class="btn btn-primary" id="calcBtn">上限額の目安を見る</button>''',
  result='''      <div class="label">ふるさと納税 上限額の目安</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">実質負担</div><div class="v" id="cost">2,000円</div></div>
      <div class="stat"><div class="k">月あたり</div><div class="v accent" id="mo">—</div></div></div>''',
  article='''    <h2>この試算について</h2>
    <div class="note">独身・共働きの方の目安表をもとに、家族構成で調整した<strong>概算</strong>です。実際の上限は、社会保険料・各種控除・他の控除の有無で変わります。</div>
    <p>上限を超えた分は自己負担になります。正確な上限は、各ふるさと納税サイトの「詳細シミュレーション」や源泉徴収票でご確認ください。</p>
    <h2>よくある質問</h2>'''+faq([('正確ですか？','あくまで目安です。住宅ローン控除や医療費控除がある方は上限が下がることがあります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const inc=Math.max(100,+$('income').value||100), f=+$('fam').value;
    // 独身・共働きの上限目安(年収万→円)を線形補間
    const pts=[[300,28000],[400,43000],[500,61000],[600,77000],[700,108000],[800,129000],[900,152000],[1000,180000],[1500,395000],[2000,570000],[3000,1075000]];
    let base; if(inc<=pts[0][0])base=pts[0][1]*inc/pts[0][0]; else if(inc>=pts[pts.length-1][0])base=pts[pts.length-1][1]; else { for(let i=0;i<pts.length-1;i++){ if(inc>=pts[i][0]&&inc<=pts[i+1][0]){ const [x0,y0]=pts[i],[x1,y1]=pts[i+1]; base=y0+(y1-y0)*(inc-x0)/(x1-x0); break; } } }
    const limit=base*f;
    $('sub').textContent=`年収${inc}万・${sel('fam').text}`;
    $('mo').textContent=yen(limit/12);
    SHARE=`ふるさと納税の上限額、私は約${yen(limit)}だった🎁（年収${inc}万）\\n実質2000円でこの分お得。あなたは？👇`;
    show(); anim($('big'),0,limit,900);
  }'''))

# ===== 仕事・働き方 =====
SIMS.append(dict(id='jikkou-jikyu', cat=WORK, emoji='⏱️',
  title='実質時給シミュレーター｜残業込み、あなたの本当の時給は？｜シミュラボ',
  desc='月給・所定労働時間・残業時間から、サービス残業も含めた「実質時給」を計算する無料シミュレーター。働き方を見直すきっかけに。',
  ogtitle='実質時給シミュレーター｜あなたの本当の時給は？', ogdesc='残業込みで、月給を実際の労働時間で割った実質時給を計算。',
  h1='実質時給シミュレーター',
  lead='月給を「実際に働いた時間」で割ると、本当の時給が見えてきます。残業（とくにサービス残業）を含めた、あなたの実質時給を計算します。',
  inputs='''    <h2>⏱️ 条件</h2>
    <div class="row"><div class="field"><label>月給（手取り前） <span class="hint">（万円）</span></label><input type="number" id="pay" value="25" min="0" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>所定労働時間 <span class="hint">（時間/月）</span></label><input type="number" id="base" value="160" min="1" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>月の残業時間 <span class="hint">（時間）</span></label><input type="number" id="ot" value="30" min="0" inputmode="numeric"></div>
    <div class="field"><label>残業代は出る？</label><select id="paid"><option value="1">出る（割増25%）</option><option value="0" selected>ほぼ出ない</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">実質時給を見る</button>''',
  result='''      <div class="label">あなたの実質時給</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">額面の時給（所定のみ）</div><div class="v" id="face">—</div></div>
      <div class="stat"><div class="k">実際の総労働時間</div><div class="v" id="tot">—</div></div>
      <div class="stat"><div class="k">残業代</div><div class="v accent" id="ot2">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>総労働時間＝所定＋残業<br>総支給＝月給(＋残業代が出るなら加算)<br>実質時給＝総支給÷総労働時間</div>
    <p>残業代が出ないのに残業が多いと、実質時給はどんどん下がります。数字で見ると、働き方を見直すきっかけになります。</p>
    <h2>よくある質問</h2>'''+faq([('手取りで計算した方がいい？','手取りで入れれば「手取りベースの実質時給」になります。比較したい基準で入れてください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const pay=Math.max(0,+$('pay').value||0)*10000, base=Math.max(1,+$('base').value||1), ot=Math.max(0,+$('ot').value||0), paid=+$('paid').value;
    const faceHourly=pay/base; const otpay= paid? faceHourly*1.25*ot : 0;
    const totalPay=pay+otpay, totalH=base+ot, real=totalPay/totalH;
    $('sub').textContent=`月給${num(pay/10000)}万・所定${base}h・残業${ot}h・${sel('paid').text}`;
    $('face').textContent=yen(faceHourly); $('tot').textContent=totalH+'時間'; $('ot2').textContent=yen(otpay);
    SHARE=`私の実質時給、残業込みで${yen(real)}だった⏱️（額面時給${yen(faceHourly)}）\\nあなたは？👇`;
    show(); anim($('big'),0,real,900);
  }'''))

SIMS.append(dict(id='fukugyo-zei', cat=WORK, emoji='💸',
  title='副業の税金・手取りシミュレーター｜確定申告は必要？｜シミュラボ',
  desc='副業の年間所得から、確定申告が必要かどうか（20万円ライン）と、追加でかかる税金・手取りの目安を試算する無料シミュレーター。',
  ogtitle='副業の税金・手取りシミュレーター｜確定申告は必要？', ogdesc='副業所得から、確定申告の要否と追加の税金・手取りを試算。',
  h1='副業の税金・手取りシミュレーター',
  lead='副業で稼いだお金、税金を引くといくら残る？確定申告が必要かどうかも含めて、副業の手取りの目安を試算します。',
  inputs='''    <h2>💸 条件</h2>
    <div class="field"><label>副業の年間所得 <span class="hint">（収入−経費・万円）</span></label><input type="number" id="inc" value="30" min="0" inputmode="numeric"></div>
    <div class="field"><label>本業の年収帯（税率の目安）</label><select id="band"><option value="0.15">〜年収400万（税率15%）</option><option value="0.20" selected>〜年収600万（20%）</option><option value="0.30">〜年収900万（30%）</option><option value="0.33">900万超（33%〜）</option></select></div>
    <button class="btn btn-primary" id="calcBtn">手取りと申告要否を見る</button>''',
  result='''      <div class="label">副業の手取り（税引き後）</div>
      <div class="big"><span id="big">0</span><span class="unit">万円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">かかる税金の目安</div><div class="v accent" id="tax">—</div></div>
      <div class="stat"><div class="k">確定申告</div><div class="v" id="kakutei" style="font-size:15px;">—</div></div></div>
      <div class="alert" id="note2" style="text-align:left;margin-top:18px;">—</div>''',
  article='''    <h2>確定申告の「20万円ライン」</h2>
    <div class="note">給与所得者の場合、副業の所得が<strong>年20万円を超えると確定申告が必要</strong>です（所得＝収入−経費）。20万円以下でも、住民税の申告は必要な点に注意。</div>
    <p>税金は「本業の所得に上乗せ」されて計算されるため、本業の年収が高いほど副業分の税率も上がります。</p>
    <h2>よくある質問</h2>'''+faq([('20万円は収入？所得？','「所得（収入−経費）」で判定します。本ツールも所得で入力してください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const inc=Math.max(0,+$('inc').value||0), band=+$('band').value;
    const tax=inc*(band+0.10); // 所得税(概算限界税率)＋住民税10%
    const take=inc-tax;
    const need= inc>20;
    $('sub').textContent=`副業所得${inc}万・本業税率${(band*100)}%＋住民税10%`;
    $('tax').textContent=num(tax)+'万円'; $('kakutei').textContent= need?'必要（20万超）':'原則不要';
    $('note2').className='alert '+(need?'bad':'good');
    $('note2').innerHTML= need?'⚠️ 副業所得が20万円超のため<strong>確定申告が必要</strong>です。':'✅ 20万円以下なので所得税の確定申告は原則不要（住民税の申告は必要）。';
    SHARE=`副業所得${inc}万の手取りは約${num(take)}万円（税${num(tax)}万）💸 確定申告は${need?'必要':'原則不要'}\\nあなたは？👇`;
    show(); anim($('big'),0,take,900);
  }'''))

SIMS.append(dict(id='shouyo-tedori', cat=WORK, emoji='💰',
  title='ボーナス手取りシミュレーター｜額面からいくら引かれる？｜シミュラボ',
  desc='ボーナスの額面と年齢から、社会保険料・所得税を引いた手取り額の目安を試算する無料シミュレーター。',
  ogtitle='ボーナス手取りシミュレーター｜額面からいくら引かれる？', ogdesc='ボーナス額面から社会保険・税を引いた手取りを試算。',
  h1='ボーナス手取りシミュレーター',
  lead='楽しみなボーナス。でも額面どおりはもらえません。社会保険料や税金を引いた「手取り」の目安を試算します。',
  inputs='''    <h2>💰 条件</h2>
    <div class="row"><div class="field"><label>ボーナス額面 <span class="hint">（万円）</span></label><input type="number" id="bonus" value="50" min="0" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>年齢</label><select id="age"><option value="0">40歳未満</option><option value="1">40歳以上（介護保険あり）</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">手取りを計算する</button>''',
  result='''      <div class="label">ボーナスの手取り目安</div>
      <div class="big"><span id="big">0</span><span class="unit">万円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">社会保険料</div><div class="v" id="shaho">—</div></div>
      <div class="stat"><div class="k">所得税(概算)</div><div class="v" id="tax">—</div></div>
      <div class="stat"><div class="k">引かれる割合</div><div class="v accent" id="rate">—</div></div></div>''',
  article='''    <h2>計算方法（概算）</h2>
    <div class="note">健康保険・厚生年金・雇用保険でおよそ15%前後、さらに所得税が引かれます（40歳以上は介護保険が加わり少し増えます）。所得税率は前月給与で決まるため、ここでは概算としています。</div>
    <p>ボーナスは額面の約8割が手取りの目安。額面で使い道を考えると足が出るので注意。</p>
    <h2>よくある質問</h2>'''+faq([('正確ですか？','保険料率は加入先や都道府県で異なるため概算です。給与明細でご確認ください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const b=Math.max(0,+$('bonus').value||0), old=+$('age').value;
    const shahoRate= old? 0.159 : 0.150; // 介護保険込み概算
    const taxRate=0.0612; // 所得税概算
    const shaho=b*shahoRate, tax=b*taxRate, take=b-shaho-tax, rate=(shaho+tax)/b*100;
    $('sub').textContent=`額面${b}万・${sel('age').text}`;
    $('shaho').textContent=num(shaho*10000)+'円'; $('tax').textContent=num(tax*10000)+'円'; $('rate').textContent= b>0?rate.toFixed(0)+'%':'—';
    SHARE=`ボーナス額面${b}万の手取りは約${num(take)}万円だった💰（${(b>0?rate.toFixed(0):0)}%引かれる…）\\nあなたは？👇`;
    show(); anim($('big'),0,take,900);
  }'''))

# ===== 学生・勉強 =====
SIMS.append(dict(id='tango', cat=STUDY, emoji='📖',
  title='英単語マスター日数シミュレーター｜何日で全部覚えられる？｜シミュラボ',
  desc='覚えたい英単語の数と1日に覚える数・復習の負担から、全部覚え終わるまでの日数と完了予定日を計算する無料シミュレーター。',
  ogtitle='英単語マスター日数｜何日で全部覚えられる？', ogdesc='単語数と1日の数から、覚え終わる日数と完了予定日を計算。',
  h1='英単語マスター日数シミュレーター',
  lead='単語帳、全部覚えるのにあと何日かかる？覚えたい単語数と1日のペースから、完了までの日数と予定日を計算します。',
  inputs='''    <h2>📖 条件</h2>
    <div class="row"><div class="field"><label>覚えたい単語数 <span class="hint">（個）</span></label><input type="number" id="total" value="1500" min="1" inputmode="numeric"></div>
    <div class="field"><label>1日に覚える数 <span class="hint">（個）</span></label><input type="number" id="perday" value="20" min="1" inputmode="numeric"></div></div>
    <div class="field"><label>復習の負担</label><select id="rev"><option value="1.0">新規だけ（復習なし）</option><option value="1.3" selected>ほどよく復習</option><option value="1.6">しっかり復習</option></select></div>
    <button class="btn btn-primary" id="calcBtn">何日で覚えられるか見る</button>''',
  result='''      <div class="label">全部覚え終わるまで</div>
      <div class="big"><span id="big">0</span><span class="unit">日</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">完了予定日</div><div class="v accent" id="date" style="font-size:16px;">—</div></div>
      <div class="stat"><div class="k">1日のペース</div><div class="v" id="pace">—</div></div>
      <div class="stat"><div class="k">あと1日5個増やすと</div><div class="v" id="plus">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>必要日数＝単語数÷1日の数×復習係数</div>
    <p>新しく覚えるだけでなく、復習に時間を使うほど定着します。本ツールは復習の負担を係数で反映しています。コツコツが結局いちばんの近道。</p>
    <h2>よくある質問</h2>'''+faq([('1日20個は多い？','人それぞれですが、復習込みで無理のないペースが続けるコツです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const t=Math.max(1,+$('total').value||1), pd=Math.max(1,+$('perday').value||1), rev=+$('rev').value;
    const days=Math.ceil(t/pd*rev);
    const d=new Date(); d.setDate(d.getDate()+days);
    const plus=Math.ceil(t/(pd+5)*rev);
    $('sub').textContent=`${t}個 ÷ 1日${pd}個 × 復習${rev}`;
    $('date').textContent=(d.getMonth()+1)+'月'+d.getDate()+'日ごろ'; $('pace').textContent=pd+'個/日'; $('plus').textContent=plus+'日';
    SHARE=`単語帳${t}個、1日${pd}個ペースだと約${days}日で覚え終わる計算📖\\nコツコツやるぞ。あなたは？👇`;
    show(); anim($('big'),0,days,900);
  }'''))

SIMS.append(dict(id='shogakukin', cat=STUDY, emoji='🎓',
  title='奨学金返済シミュレーター｜毎月いくら？何年で返す？｜シミュラボ',
  desc='奨学金の借入総額・利率・返済年数から、毎月の返済額・総返済額・総利息を計算する無料シミュレーター。進学前・就職前のチェックに。',
  ogtitle='奨学金返済シミュレーター｜毎月いくら？何年で返す？', ogdesc='奨学金の借入額から、毎月の返済額・総返済額を計算。',
  h1='奨学金返済シミュレーター',
  lead='奨学金は「借金」。卒業後、毎月いくら・何年返すのか、先に知っておきましょう。借入総額から返済額を計算します。',
  inputs='''    <h2>🎓 条件</h2>
    <div class="field"><label>借入総額 <span class="hint">（万円・例: 月5万×4年=240）</span></label><input type="number" id="p" value="240" min="0" inputmode="numeric"></div>
    <div class="row"><div class="field"><label>利率 <span class="hint">（％/年・無利子なら0）</span></label><input type="number" id="r" value="0.3" min="0" max="10" step="0.05" inputmode="decimal"></div>
    <div class="field"><label>返済年数 <span class="hint">（年）</span></label><input type="number" id="y" value="15" min="1" max="30" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">返済額を計算する</button>''',
  result='''      <div class="label">毎月の返済額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">総返済額</div><div class="v" id="total">—</div></div>
      <div class="stat"><div class="k">総利息</div><div class="v accent" id="int">—</div></div>
      <div class="stat"><div class="k">返済完了まで</div><div class="v" id="y2">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式（元利均等）</strong><br>月返済＝借入×月利÷(1−(1+月利)^−回数)（無利子なら借入÷回数）</div>
    <p>社会人になってから十数年つきあう返済です。無理のない金額か、利子はいくらか、進学前に把握しておくと安心です。</p>
    <h2>よくある質問</h2>'''+faq([('第一種・第二種の違いは？','第一種は無利子（利率0）、第二種は有利子です。利率欄で切り替えて試せます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const P=Math.max(0,+$('p').value||0)*10000, ry=(+$('r').value||0)/100, y=Math.max(1,+$('y').value||1);
    const r=ry/12, n=y*12; const m= r>0 ? P*r/(1-Math.pow(1+r,-n)) : P/n;
    const total=m*n, int=total-P;
    $('sub').textContent=`借入${num(P/10000)}万・利率${(ry*100).toFixed(2)}%・${y}年`;
    $('total').textContent=yen(total); $('int').textContent=yen(int); $('y2').textContent=y+'年';
    SHARE=`奨学金${num(P/10000)}万、毎月${yen(m)}を${y}年返済（総利息${yen(int)}）🎓\\n返済は計画的に。あなたは？👇`;
    show(); anim($('big'),0,m,900);
  }'''))

SIMS.append(dict(id='benkyo-target', cat=STUDY, emoji='🎯',
  title='目標点までの勉強量シミュレーター｜1日何時間やればいい？｜シミュラボ',
  desc='目標点・今の点数・テストまでの日数から、目標達成に必要な総勉強時間と1日あたりの勉強時間を試算する無料シミュレーター。',
  ogtitle='目標点までの勉強量｜1日何時間やればいい？', ogdesc='目標点と残り日数から、1日に必要な勉強時間を試算。',
  h1='目標点までの勉強量シミュレーター',
  lead='テストの目標点まで、1日どれくらい勉強すればいい？目標点・今の点数・残り日数から、必要な勉強量を逆算します。',
  inputs='''    <h2>🎯 条件</h2>
    <div class="row"><div class="field"><label>目標点 <span class="hint">（点）</span></label><input type="number" id="goal" value="80" min="0" max="100" inputmode="numeric"></div>
    <div class="field"><label>今の点数 <span class="hint">（点）</span></label><input type="number" id="now" value="55" min="0" max="100" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>テストまでの日数 <span class="hint">（日）</span></label><input type="number" id="days" value="30" min="1" inputmode="numeric"></div>
    <div class="field"><label>1点上げるのに必要な時間 <span class="hint">（時間・目安）</span></label><input type="number" id="perpt" value="3" min="0.5" step="0.5" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">必要な勉強量を見る</button>''',
  result='''      <div class="label">1日に必要な勉強時間</div>
      <div class="big"><span id="big">0</span><span class="unit">時間</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">必要な総勉強時間</div><div class="v accent" id="tot">—</div></div>
      <div class="stat"><div class="k">あと何点</div><div class="v" id="gap">—</div></div>
      <div class="stat"><div class="k">残り日数</div><div class="v" id="d">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>必要総時間＝(目標点−今の点数)×1点あたりの時間<br>1日あたり＝必要総時間÷残り日数</div>
    <p>「あと25点」と言われると遠く感じますが、「1日◯時間」に分解すると一気に現実的になります。逆算して、毎日の計画に落とし込みましょう。</p>
    <h2>よくある質問</h2>'''+faq([('1点3時間って本当？','科目や現在地で変わる目安です。自分の感覚に合わせて調整してください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const goal=+$('goal').value||0, now=+$('now').value||0, days=Math.max(1,+$('days').value||1), pp=Math.max(0.1,+$('perpt').value||0.1);
    const gap=Math.max(0,goal-now), tot=gap*pp, perDay=tot/days;
    $('sub').textContent=`${now}点 → 目標${goal}点・あと${days}日`;
    $('tot').textContent=num(tot)+'時間'; $('gap').textContent=gap+'点'; $('d').textContent=days+'日';
    SHARE=`目標${goal}点まで、1日${perDay.toFixed(1)}時間の勉強が必要だった🎯（あと${gap}点/${days}日）\\nやるしかない。あなたは？👇`;
    show(); anim($('big'),0,perDay,900,1);
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
