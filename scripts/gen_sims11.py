# -*- coding: utf-8 -*-
"""シミュラボ：新4カテゴリ 各10本（健康/占い/クルマ/旅行＝計40本）。"""
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
  const hash = (s) => { let h=2166136261; for(let i=0;i<s.length;i++){ h^=s.charCodeAt(i); h=Math.imul(h,16777619); } return (h>>>0); };
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

HEALTH='健康・カラダ'; URANAI='占い・診断'; CAR='クルマ・乗り物'; TRAVEL='旅行・おでかけ'
SIMS=[]

# ============ 健康・カラダ ============

SIMS.append(dict(id='bmi', cat=HEALTH, emoji='⚖️',
  title='BMI・適正体重シミュレーター｜あなたの適正体重は何kg？｜シミュラボ',
  desc='身長と体重からBMIと適正体重（BMI22）を計算し、今の体重との差や判定の目安を表示する無料シミュレーター。',
  ogtitle='BMI・適正体重シミュレーター｜適正体重は何kg？', ogdesc='身長・体重からBMIと適正体重、今との差を計算。',
  h1='BMI・適正体重シミュレーター',
  lead='身長と体重を入れるだけ。BMIと、もっとも病気になりにくいとされるBMI22の適正体重、今との差を計算します（健康判断は専門家にご相談を）。',
  inputs='''    <h2>⚖️ 身長・体重を入れる</h2>
    <div class="row"><div class="field"><label>身長 <span class="hint">（cm）</span></label><input type="number" id="h" value="170" min="100" max="230" inputmode="numeric"></div>
    <div class="field"><label>体重 <span class="hint">（kg）</span></label><input type="number" id="w" value="65" min="20" max="250" step="0.1" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">BMIを計算する</button>''',
  result='''      <div class="label">あなたのBMIは</div>
      <div class="big"><span id="big">0</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">適正体重(BMI22)</div><div class="v accent" id="ideal">—</div></div>
      <div class="stat"><div class="k">今との差</div><div class="v" id="diff">—</div></div>
      <div class="stat"><div class="k">判定</div><div class="v" id="judge">—</div></div></div>''',
  article='''    <h2>BMIの見方</h2>
    <div class="note"><strong>計算式</strong><br>BMI ＝ 体重(kg) ÷ 身長(m)²／適正体重 ＝ 22 × 身長(m)²<br>日本肥満学会の目安：18.5未満=低体重／18.5〜25=普通／25以上=肥満</div>
    <p>BMIは体格の目安で、筋肉量や体脂肪までは分かりません。数字は参考として、体調や見た目とあわせて判断しましょう。</p>
    <h2>よくある質問</h2>'''+faq([('BMIが普通なら健康ですか？','BMIはあくまで体格指数です。体脂肪率や生活習慣も含めて総合的に見てください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const h=Math.max(1,+$('h').value||1)/100, w=Math.max(0,+$('w').value||0);
    const bmi=w/(h*h), ideal=22*h*h, diff=w-ideal;
    let j; if(bmi<18.5)j='低体重'; else if(bmi<25)j='普通体重'; else if(bmi<30)j='肥満(1度)'; else j='肥満(2度〜)';
    $('sub').textContent=`身長${(h*100)}cm・体重${w}kg`;
    $('ideal').textContent=ideal.toFixed(1)+'kg'; $('diff').textContent=(diff>=0?'+':'')+diff.toFixed(1)+'kg'; $('judge').textContent=j;
    SHARE=`BMI計算したら${bmi.toFixed(1)}（${j}）でした⚖️\\n適正体重まであと${Math.abs(diff).toFixed(1)}kg。あなたは？👇`;
    show(); anim($('big'),0,bmi,900,1);
  }'''))

SIMS.append(dict(id='kiso-taisha', cat=HEALTH, emoji='🔥',
  title='基礎代謝＆必要カロリー計算｜1日に必要なカロリーは？｜シミュラボ',
  desc='性別・年齢・身長・体重・活動量から、基礎代謝量と1日に必要なカロリー（推定エネルギー必要量）を計算する無料シミュレーター。',
  ogtitle='基礎代謝＆必要カロリー計算｜1日に必要なのは何kcal？', ogdesc='性別・年齢・体格・活動量から基礎代謝と必要カロリーを計算。',
  h1='基礎代謝＆必要カロリー計算',
  lead='何もしなくても消費する「基礎代謝」と、1日に必要なカロリーを計算します。ダイエットや増量の目安づくりに（医学的判断は専門家へ）。',
  inputs='''    <h2>🔥 条件を入れる</h2>
    <div class="row"><div class="field"><label>性別</label><select id="sex"><option value="m">男性</option><option value="f">女性</option></select></div>
    <div class="field"><label>年齢 <span class="hint">（歳）</span></label><input type="number" id="age" value="30" min="10" max="100" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>身長 <span class="hint">（cm）</span></label><input type="number" id="h" value="170" min="100" max="230" inputmode="numeric"></div>
    <div class="field"><label>体重 <span class="hint">（kg）</span></label><input type="number" id="w" value="65" min="20" max="250" step="0.1" inputmode="decimal"></div></div>
    <div class="field"><label>活動量</label><select id="act"><option value="1.2">ほぼ運動しない</option><option value="1.375" selected>軽い運動(週1〜3)</option><option value="1.55">中程度(週3〜5)</option><option value="1.725">よく動く(週6〜7)</option></select></div>
    <button class="btn btn-primary" id="calcBtn">必要カロリーを計算する</button>''',
  result='''      <div class="label">1日に必要なカロリー</div>
      <div class="big"><span id="big">0</span><span class="unit">kcal</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">基礎代謝</div><div class="v" id="bmr">—</div></div>
      <div class="stat"><div class="k">減量の目安(-500)</div><div class="v accent" id="diet">—</div></div>
      <div class="stat"><div class="k">活動レベル</div><div class="v" id="lv">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式（ミフリン・サンジョール式）</strong><br>基礎代謝 ＝ 10×体重 ＋ 6.25×身長 − 5×年齢 ＋（男性+5／女性−161）<br>必要カロリー ＝ 基礎代謝 × 活動係数</div>
    <p>必要カロリーより摂取が少なければ減量、多ければ増量の方向です。1日−500kcalで月約2kgが目安ですが、無理な制限は禁物です。</p>
    <h2>よくある質問</h2>'''+faq([('正確な値ですか？','推定式による目安です。実際の代謝には個人差があります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const sex=$('sex').value, age=Math.max(1,+$('age').value||1), h=Math.max(1,+$('h').value||1), w=Math.max(0,+$('w').value||0), act=+$('act').value||1.2;
    const bmr=10*w+6.25*h-5*age+(sex==='m'?5:-161), need=bmr*act;
    $('sub').textContent=`${sex==='m'?'男性':'女性'}・${age}歳・${h}cm・${w}kg`;
    $('bmr').textContent=num(bmr)+'kcal'; $('diet').textContent=num(need-500)+'kcal'; $('lv').textContent=sel('act').text;
    SHARE=`1日の必要カロリー、私は約${num(need)}kcalでした🔥（基礎代謝${num(bmr)}）\\n食べすぎ注意…！あなたは？👇`;
    show(); anim($('big'),0,need,900);
  }'''))

SIMS.append(dict(id='tainai-nenrei', cat=HEALTH, emoji='🫀',
  title='体内年齢診断｜あなたのカラダ、実年齢より若い？老けてる？｜シミュラボ',
  desc='運動・睡眠・食生活・喫煙・ストレスの5つの生活習慣から、実年齢に対する「体内年齢」の目安を診断するエンタメシミュレーター。',
  ogtitle='体内年齢診断｜カラダは実年齢より若い？', ogdesc='5つの生活習慣から体内年齢の目安を診断。',
  h1='体内年齢診断',
  lead='同じ年齢でも、生活習慣でカラダの若さは変わります。5つの質問から、あなたの「体内年齢」の目安を診断します（エンタメ診断です）。',
  inputs='''    <h2>🫀 生活習慣を選ぶ</h2>
    <div class="field"><label>実年齢 <span class="hint">（歳）</span></label><input type="number" id="age" value="35" min="10" max="100" inputmode="numeric"></div>
    <div class="field"><label>運動の習慣</label><select id="q1"><option value="-4">週3以上しっかり</option><option value="-1" selected>たまに動く</option><option value="3">ほぼ運動しない</option></select></div>
    <div class="field"><label>睡眠</label><select id="q2"><option value="-3">毎日ぐっすり7時間</option><option value="0" selected>まあまあ</option><option value="3">不足・不規則</option></select></div>
    <div class="field"><label>食生活</label><select id="q3"><option value="-3">バランス良い</option><option value="0" selected>普通</option><option value="3">外食・脂っこい中心</option></select></div>
    <div class="field"><label>喫煙</label><select id="q4"><option value="0">吸わない</option><option value="2" selected>たまに</option><option value="5">毎日吸う</option></select></div>
    <div class="field"><label>ストレス</label><select id="q5"><option value="-2">うまく発散できてる</option><option value="1" selected>普通</option><option value="4">かなり多い</option></select></div>
    <button class="btn btn-primary" id="calcBtn">体内年齢を診断する</button>''',
  result='''      <div class="label">あなたの体内年齢は</div>
      <div class="big"><span id="big">0</span><span class="unit">歳</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:18px;">—</div>''',
  article='''    <h2>体内年齢とは</h2>
    <p>運動・睡眠・食事・喫煙・ストレスは、カラダの老化スピードに影響すると言われます。本診断はそれを簡易点数化したエンタメです。生活を見直すきっかけにどうぞ。</p>
    <div class="note">💡 いちばん効くのは「運動」と「睡眠」。週に少し体を動かし、7時間眠るだけでも体内年齢は変わってきます。</div>
    <h2>よくある質問</h2>'''+faq([('医学的な数値ですか？','いいえ。生活習慣から目安を出すエンタメ診断です。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const age=Math.max(10,+$('age').value||10);
    let d=0; for(const id of ['q1','q2','q3','q4','q5']) d+=(+$(id).value||0);
    const inner=Math.max(15,Math.round(age+d));
    const gap=inner-age;
    let a; if(gap<=-3)a='素晴らしい！実年齢よりぐっと若いカラダ。今の習慣を続けましょう✨';
    else if(gap<=1)a='実年齢相応。運動か睡眠をもう少し足すと、さらに若返りが狙えます。';
    else a='少し老化が進み気味かも。まずは「週2の運動」と「7時間睡眠」から見直してみて。';
    $('sub').textContent=`実年齢${age}歳 → 体内年齢${inner}歳（${gap>=0?'+':''}${gap}歳）`;
    $('adv').textContent='🫀 '+a;
    SHARE=`体内年齢診断、実年齢${age}歳に対して体内年齢は${inner}歳でした🫀\\n${gap<=0?'若い…！':'生活見直そ…'}あなたは？👇`;
    show(); anim($('big'),0,inner,900);
  }'''))

SIMS.append(dict(id='suibun', cat=HEALTH, emoji='💧',
  title='1日の水分必要量シミュレーター｜あなたは1日何リットル？｜シミュラボ',
  desc='体重と活動量から、1日に必要な水分量の目安とコップ何杯分かを計算する無料シミュレーター。',
  ogtitle='1日の水分必要量シミュレーター｜1日に何リットル？', ogdesc='体重と活動量から、1日に必要な水分量とコップ杯数を計算。',
  h1='1日の水分必要量シミュレーター',
  lead='水分不足は不調のもと。体重と活動量から、1日に必要な水分量の目安と、コップ何杯ぶんかを計算します。',
  inputs='''    <h2>💧 条件を入れる</h2>
    <div class="field"><label>体重 <span class="hint">（kg）</span></label><input type="number" id="w" value="60" min="20" max="200" step="0.1" inputmode="decimal"></div>
    <div class="field"><label>活動量・季節</label><select id="act"><option value="1">ふつう</option><option value="1.15" selected>よく動く・暑い日</option><option value="1.3">運動・猛暑</option></select></div>
    <button class="btn btn-primary" id="calcBtn">必要な水分量を見る</button>''',
  result='''      <div class="label">1日に必要な水分量</div>
      <div class="big"><span id="big">0</span><span class="unit">ml</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">リットル</div><div class="v accent" id="l">—</div></div>
      <div class="stat"><div class="k">コップ(200ml)</div><div class="v" id="cup">—</div></div>
      <div class="stat"><div class="k">ペットボトル(500ml)</div><div class="v" id="pet">—</div></div></div>''',
  article='''    <h2>計算の考え方</h2>
    <div class="note"><strong>計算式</strong><br>必要水分量 ＝ 体重(kg) × 35ml × 活動係数<br>※食事に含まれる水分も含む、ざっくりの目安です。</div>
    <p>のどが渇く前にこまめに飲むのがコツ。一気飲みより、コップ1杯をこまめにが吸収に良いとされます。持病のある方は主治医の指示を優先してください。</p>
    <h2>よくある質問</h2>'''+faq([('全部を飲み水で？','いいえ。食事やお茶も含む総量の目安です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const w=Math.max(0,+$('w').value||0), act=+$('act').value||1;
    const ml=w*35*act;
    $('sub').textContent=`体重${w}kg × 35ml × ${act}`;
    $('l').textContent=(ml/1000).toFixed(1)+'L'; $('cup').textContent=num(ml/200)+'杯'; $('pet').textContent=num(ml/500)+'本';
    SHARE=`1日に必要な水分量、私は約${(ml/1000).toFixed(1)}L（コップ${num(ml/200)}杯）でした💧\\nちゃんと飲めてる？👇`;
    show(); anim($('big'),0,ml,900);
  }'''))

SIMS.append(dict(id='taishibo', cat=HEALTH, emoji='📏',
  title='体脂肪率ざっくり推定｜身長・体重・年齢から体脂肪率を推定｜シミュラボ',
  desc='性別・年齢・身長・体重から、BMIをもとに体脂肪率の目安をざっくり推定する無料シミュレーター（体組成計の代わりの簡易版）。',
  ogtitle='体脂肪率ざっくり推定｜身長・体重から体脂肪率を推定', ogdesc='BMIをもとに体脂肪率の目安をざっくり推定。',
  h1='体脂肪率ざっくり推定',
  lead='体組成計がなくても、身長・体重・年齢から体脂肪率の目安をざっくり推定します（あくまで概算。正確には体組成計で）。',
  inputs='''    <h2>📏 条件を入れる</h2>
    <div class="row"><div class="field"><label>性別</label><select id="sex"><option value="m">男性</option><option value="f">女性</option></select></div>
    <div class="field"><label>年齢 <span class="hint">（歳）</span></label><input type="number" id="age" value="30" min="15" max="100" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>身長 <span class="hint">（cm）</span></label><input type="number" id="h" value="170" min="100" max="230" inputmode="numeric"></div>
    <div class="field"><label>体重 <span class="hint">（kg）</span></label><input type="number" id="w" value="65" min="20" max="250" step="0.1" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">体脂肪率を推定する</button>''',
  result='''      <div class="label">推定体脂肪率</div>
      <div class="big"><span id="big">0</span><span class="unit">%</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">BMI</div><div class="v" id="bmi">—</div></div>
      <div class="stat"><div class="k">判定の目安</div><div class="v accent" id="judge">—</div></div>
      <div class="stat"><div class="k">推定体脂肪量</div><div class="v" id="fat">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式（BMIベースの推定）</strong><br>体脂肪率 ＝ 1.2×BMI ＋ 0.23×年齢 − 10.8×性別(男1/女0) − 5.4</div>
    <p>あくまで統計的な推定式で、筋肉質な人ほどズレやすい点に注意。目安：男性10〜20%／女性20〜30%が標準的とされます。</p>
    <h2>よくある質問</h2>'''+faq([('体組成計と違うのはなぜ？','本ツールはBMIからの推定です。実測とは差が出ます。傾向把握に使ってください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const sex=$('sex').value, age=Math.max(15,+$('age').value||15), h=Math.max(1,+$('h').value||1)/100, w=Math.max(0,+$('w').value||0);
    const bmi=w/(h*h);
    let bf=1.2*bmi+0.23*age-10.8*(sex==='m'?1:0)-5.4; bf=Math.max(3,Math.min(55,bf));
    const std = sex==='m' ? (bf<10?'やや低い':bf<20?'標準':bf<25?'やや高い':'高め') : (bf<20?'やや低い':bf<30?'標準':bf<35?'やや高い':'高め');
    $('sub').textContent=`${sex==='m'?'男性':'女性'}・${age}歳・BMI${bmi.toFixed(1)}`;
    $('bmi').textContent=bmi.toFixed(1); $('judge').textContent=std; $('fat').textContent=(w*bf/100).toFixed(1)+'kg';
    SHARE=`体脂肪率をざっくり推定したら約${bf.toFixed(1)}%（${std}）でした📏\\nあなたは？👇`;
    show(); anim($('big'),0,bf,900,1);
  }'''))

SIMS.append(dict(id='hosu-karori', cat=HEALTH, emoji='🚶',
  title='歩数の消費カロリー計算｜1日◯歩で何kcal燃える？｜シミュラボ',
  desc='1日の歩数と体重から、消費カロリー・燃える脂肪量・歩いた距離、脂肪1kgを減らすのに何日かかるかを計算する無料シミュレーター。',
  ogtitle='歩数の消費カロリー計算｜◯歩で何kcal燃える？', ogdesc='歩数と体重から消費カロリー・脂肪量・距離を計算。',
  h1='歩数の消費カロリー計算',
  lead='今日の歩数、何kcal燃えた？歩数と体重から、消費カロリー・燃える脂肪・歩いた距離を計算します。',
  inputs='''    <h2>🚶 条件を入れる</h2>
    <div class="row"><div class="field"><label>1日の歩数 <span class="hint">（歩）</span></label><input type="number" id="steps" value="8000" min="0" inputmode="numeric"></div>
    <div class="field"><label>体重 <span class="hint">（kg）</span></label><input type="number" id="w" value="60" min="20" max="200" step="0.1" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">消費カロリーを見る</button>''',
  result='''      <div class="label">この歩数の消費カロリー</div>
      <div class="big"><span id="big">0</span><span class="unit">kcal</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">燃える脂肪</div><div class="v accent" id="fat">—</div></div>
      <div class="stat"><div class="k">歩いた距離</div><div class="v" id="dist">—</div></div>
      <div class="stat"><div class="k">脂肪1kg減らすに</div><div class="v" id="days">—</div></div></div>''',
  article='''    <h2>計算の考え方</h2>
    <div class="note"><strong>計算式（概算）</strong><br>消費カロリー ＝ 歩数 × 体重(kg) × 0.0005<br>脂肪 ＝ カロリー ÷ 7.2（脂肪1g≒7.2kcal）／距離 ＝ 歩数 × 0.7m</div>
    <p>歩くだけでもしっかりカロリーは消費します。早歩きや坂道だと消費はさらにアップ。毎日の積み重ねが効いてきます。</p>
    <h2>よくある質問</h2>'''+faq([('正確な値ですか？','歩幅・速度で変わる概算です。傾向の目安として使ってください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const steps=Math.max(0,+$('steps').value||0), w=Math.max(0,+$('w').value||0);
    const kcal=steps*w*0.0005, fat=kcal/7.2, dist=steps*0.7/1000, days=kcal>0?7200/kcal:0;
    $('sub').textContent=`${num(steps)}歩 × ${w}kg`;
    $('fat').textContent=num(fat)+'g'; $('dist').textContent=dist.toFixed(2)+'km'; $('days').textContent=days>0?num(days)+'日':'—';
    SHARE=`今日の${num(steps)}歩で約${num(kcal)}kcal・脂肪${num(fat)}g燃えてた🚶\\n歩くって偉い。あなたは何歩？👇`;
    show(); anim($('big'),0,kcal,900);
  }'''))

SIMS.append(dict(id='sake-karori', cat=HEALTH, emoji='🍺',
  title='お酒のカロリー計算｜飲み会で何kcal？ごはん何杯分？｜シミュラボ',
  desc='お酒の種類と杯数から、合計カロリーとごはん何杯分・ウォーキング何分で消費できるかを計算する無料シミュレーター。',
  ogtitle='お酒のカロリー計算｜飲み会で何kcal？', ogdesc='お酒の種類と杯数から合計カロリーとごはん換算を計算。',
  h1='お酒のカロリー計算',
  lead='その飲み会、何kcal？お酒の種類と杯数から、合計カロリーと「ごはん何杯分」「歩いて消費するには何分」かを計算します。',
  inputs='''    <h2>🍺 条件を入れる</h2>
    <div class="field"><label>お酒の種類</label><select id="type"><option value="140">ビール(中ジョッキ)</option><option value="100">ハイボール</option><option value="200">日本酒(1合)</option><option value="90">ワイン(グラス)</option><option value="100">焼酎(ロック)</option><option value="200">酎ハイ・サワー</option></select></div>
    <div class="field"><label>杯数 <span class="hint">（杯）</span></label><input type="number" id="n" value="3" min="0" max="50" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">カロリーを計算する</button>''',
  result='''      <div class="label">お酒の合計カロリー</div>
      <div class="big"><span id="big">0</span><span class="unit">kcal</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">ごはん換算</div><div class="v accent" id="rice">—</div></div>
      <div class="stat"><div class="k">ウォーキング</div><div class="v" id="walk">—</div></div>
      <div class="stat"><div class="k">1杯あたり</div><div class="v" id="per">—</div></div></div>''',
  article='''    <h2>計算の考え方</h2>
    <div class="note"><strong>計算式</strong><br>合計カロリー ＝ 1杯のカロリー × 杯数<br>ごはん1杯≒252kcal／ウォーキングは体重60kgで約4kcal/分として換算。</div>
    <p>お酒のカロリーに加えて、おつまみも要注意。飲みすぎた翌日は軽めの食事と運動でリセットを。適量を楽しみましょう。</p>
    <h2>よくある質問</h2>'''+faq([('糖質はわかりますか？','本ツールはカロリーのみの概算です。種類により糖質量は異なります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const c=+$('type').value||0, n=Math.max(0,+$('n').value||0);
    const total=c*n;
    $('sub').textContent=`${sel('type').text} × ${n}杯`;
    $('rice').textContent=(total/252).toFixed(1)+'杯'; $('walk').textContent=num(total/4)+'分'; $('per').textContent=num(c)+'kcal';
    SHARE=`今日の飲み会、お酒だけで約${num(total)}kcal（ごはん${(total/252).toFixed(1)}杯分）🍺\\nおつまみ込みだともっと…！👇`;
    show(); anim($('big'),0,total,900);
  }'''))

SIMS.append(dict(id='suimin-cycle', cat=HEALTH, emoji='😴',
  title='快眠の起床時刻シミュレーター｜何時に寝ればスッキリ起きられる？｜シミュラボ',
  desc='起きたい時刻を入れると、睡眠サイクル（約90分）にあわせてスッキリ起きやすい就寝時刻を逆算する無料シミュレーター。',
  ogtitle='快眠の起床時刻シミュレーター｜何時に寝ればスッキリ？', ogdesc='起きたい時刻から、90分サイクルでベストな就寝時刻を逆算。',
  h1='快眠の起床時刻シミュレーター',
  lead='睡眠は約90分サイクル。サイクルの切れ目で起きると目覚めスッキリ。起きたい時刻から、おすすめの就寝時刻を逆算します。',
  inputs='''    <h2>😴 起きたい時刻を入れる</h2>
    <div class="field"><label>起床したい時刻</label><input type="time" id="wake" value="07:00"></div>
    <button class="btn btn-primary" id="calcBtn">就寝時刻を逆算する</button>''',
  result='''      <div class="label">おすすめの睡眠時間</div>
      <div class="big"><span id="big">0</span><span class="unit">時間</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">ベスト就寝(5サイクル)</div><div class="v accent" id="b5">—</div></div>
      <div class="stat"><div class="k">しっかり寝る(6サイクル)</div><div class="v" id="b6">—</div></div>
      <div class="stat"><div class="k">短め(4サイクル)</div><div class="v" id="b4">—</div></div></div>''',
  article='''    <h2>睡眠サイクルとは</h2>
    <div class="note"><strong>考え方</strong><br>睡眠は浅い→深い→浅いを約90分でくり返します。サイクルの切れ目（90分の倍数）で起きると目覚めが良いとされます。寝つきに約15分を加味して逆算しています。</div>
    <p>5サイクル＝約7.5時間が多くの大人にちょうど良い目安。ただし最適な睡眠時間には個人差があります。</p>
    <h2>よくある質問</h2>'''+faq([('必ずスッキリ起きられますか？','個人差があります。あくまで目安としてお使いください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const v=$('wake').value||'07:00'; const [wh,wm]=v.split(':').map(Number);
    const wake=wh*60+wm;
    function fmt(mins){ mins=((mins%1440)+1440)%1440; const h=Math.floor(mins/60), m=mins%60; return `${h}:${('0'+m).slice(-2)}`; }
    const fall=15;
    const b5=wake-(5*90+fall), b6=wake-(6*90+fall), b4=wake-(4*90+fall);
    $('sub').textContent=`起床 ${v} に合わせた就寝時刻`;
    $('b5').textContent=fmt(b5); $('b6').textContent=fmt(b6); $('b4').textContent=fmt(b4);
    SHARE=`${v}に起きるなら、${fmt(b5)}に寝ると5サイクル(約7.5時間)でスッキリ😴\\n試してみて。👇`;
    show(); anim($('big'),0,7.5,900,1);
  }'''))

SIMS.append(dict(id='suwari', cat=HEALTH, emoji='🪑',
  title='座りすぎメーター｜あなたは1年でどれだけ座ってる？｜シミュラボ',
  desc='1日の座っている時間から、1週間・1年でどれだけ座っているか、起きている時間に占める割合を可視化するエンタメシミュレーター。',
  ogtitle='座りすぎメーター｜1年でどれだけ座ってる？', ogdesc='1日の座位時間から、年間の座っている時間と割合を可視化。',
  h1='座りすぎメーター',
  lead='デスクワーク中心だと、人は驚くほど座っています。1日の座位時間から、1年でどれだけ座っているかを可視化します（健康への影響は専門家へ）。',
  inputs='''    <h2>🪑 条件を入れる</h2>
    <div class="field"><label>1日に座っている時間 <span class="hint">（時間・仕事/食事/スマホ等の合計）</span></label><input type="number" id="hpd" value="9" min="0" max="20" step="0.5" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">座りすぎ度を見る</button>''',
  result='''      <div class="label">1年で座っている時間</div>
      <div class="big"><span id="big">0</span><span class="unit">日分</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1週間で</div><div class="v" id="wk">—</div></div>
      <div class="stat"><div class="k">起きてる時間の</div><div class="v accent" id="ratio">—</div></div>
      <div class="stat"><div class="k">1年の合計</div><div class="v" id="yr">—</div></div></div>''',
  article='''    <h2>座りすぎに注意</h2>
    <div class="note"><strong>計算式</strong><br>年間の座位時間 ＝ 1日の座位時間 × 365／割合は起床16時間に対する比率</div>
    <p>長時間座りっぱなしは健康リスクと言われます。30〜60分に一度立つ・歩く・伸びをするだけでも違います。「立って会議」「1駅歩く」もおすすめ。</p>
    <h2>よくある質問</h2>'''+faq([('何時間までならOK？','明確な基準はありませんが、こまめに中断するのが良いとされます。気になる方は専門家へ。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const h=Math.max(0,Math.min(20,+$('hpd').value||0));
    const yrH=h*365, days=yrH/24, wk=h*7, ratio=Math.min(100,h/16*100);
    $('sub').textContent=`1日${h}時間 × 365日`;
    $('wk').textContent=num(wk)+'時間'; $('ratio').textContent=Math.round(ratio)+'%'; $('yr').textContent=num(yrH)+'時間';
    SHARE=`座りすぎメーター：私は1年で約${num(days)}日分も座ってた🪑（起きてる時間の${Math.round(ratio)}%）\\nちょっと立とう…！👇`;
    show(); anim($('big'),0,days,900);
  }'''))

SIMS.append(dict(id='mizu-body', cat=HEALTH, emoji='💦',
  title='体の水分量シミュレーター｜あなたのカラダ、何kgが水？｜シミュラボ',
  desc='体重とタイプ（成人・子ども・高齢者）から、体に含まれる水分の量とペットボトル何本分かを計算するエンタメシミュレーター。',
  ogtitle='体の水分量シミュレーター｜カラダの何kgが水？', ogdesc='体重とタイプから、体に含まれる水分量を計算。',
  h1='体の水分量シミュレーター',
  lead='人のカラダの大半は水でできています。体重とタイプから、あなたのカラダに含まれる水分量を計算します（おもしろ雑学）。',
  inputs='''    <h2>💦 条件を入れる</h2>
    <div class="field"><label>体重 <span class="hint">（kg）</span></label><input type="number" id="w" value="60" min="5" max="200" step="0.1" inputmode="decimal"></div>
    <div class="field"><label>タイプ</label><select id="type"><option value="0.6">成人男性(約60%)</option><option value="0.55" selected>成人女性(約55%)</option><option value="0.7">子ども(約70%)</option><option value="0.5">高齢者(約50%)</option></select></div>
    <button class="btn btn-primary" id="calcBtn">水分量を見る</button>''',
  result='''      <div class="label">あなたのカラダの水分量</div>
      <div class="big"><span id="big">0</span><span class="unit">kg</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">割合</div><div class="v" id="pct">—</div></div>
      <div class="stat"><div class="k">ペットボトル(500ml)</div><div class="v accent" id="pet">—</div></div>
      <div class="stat"><div class="k">水以外</div><div class="v" id="rest">—</div></div></div>''',
  article='''    <h2>体の水分のはなし</h2>
    <div class="note"><strong>計算式</strong><br>体内の水分量 ＝ 体重 × タイプ別の水分割合<br>赤ちゃんは約75%、成人は約60%、高齢になるほど割合は下がります。</div>
    <p>たった2%の水分が失われるだけで、のどの渇きや集中力低下が起きると言われます。こまめな水分補給を。</p>
    <h2>よくある質問</h2>'''+faq([('正確ですか？','体組成で個人差があります。雑学レベルの目安です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const w=Math.max(0,+$('w').value||0), r=+$('type').value||0.6;
    const water=w*r;
    $('sub').textContent=`体重${w}kg × ${Math.round(r*100)}%`;
    $('pct').textContent=Math.round(r*100)+'%'; $('pet').textContent=num(water/0.5)+'本'; $('rest').textContent=(w-water).toFixed(1)+'kg';
    SHARE=`体の水分量を計算したら約${water.toFixed(1)}kg（ペットボトル${num(water/0.5)}本分）が水だった💦\\nカラダってほぼ水。👇`;
    show(); anim($('big'),0,water,900,1);
  }'''))

# （占い・クルマ・旅行は後続スクリプトで追記）
def write_all(sims):
    for s in sims:
        d=os.path.join(ROOT,'sims',s['id']); os.makedirs(d,exist_ok=True)
        html=(TPL.replace('__TITLE__',s['title']).replace('__DESC__',s['desc'])
              .replace('__OGTITLE__',s['ogtitle']).replace('__OGDESC__',s['ogdesc'])
              .replace('__CAT__',s['cat']).replace('__H1__',s['h1']).replace('__LEAD__',s['lead'])
              .replace('__INPUTS__',s['inputs']).replace('__RESULT__',s['result'])
              .replace('__ARTICLE__',s['article']).replace('__JS__',s['js']).replace('__ID__',s['id']))
        with open(os.path.join(d,'index.html'),'w',encoding='utf-8') as f: f.write(html)
        print('created sims/'+s['id'])

if __name__=='__main__':
    write_all(SIMS)
    print(f'health done. {len(SIMS)} sims.')
