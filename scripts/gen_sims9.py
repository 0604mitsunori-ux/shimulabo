# -*- coding: utf-8 -*-
"""シミュラボ：少数カテゴリ補充（マーケ3／お金・時間3／恋愛・婚活3＝計9本）。"""
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

MKT='マーケティング'; MONEY='お金・時間'; LOVE='恋愛・婚活'
SIMS=[]

# ========== マーケティング ==========

# 1. バズ偏差値メーター
SIMS.append(dict(id='buzz', cat=MKT, emoji='📊',
  title='バズ偏差値メーター｜あなたの投稿、偏差値いくつ？｜シミュラボ',
  desc='フォロワー数・いいね・保存（リポスト）数から、SNS投稿のエンゲージメント率と「バズ偏差値」を判定する無料シミュレーター。',
  ogtitle='バズ偏差値メーター｜あなたの投稿、偏差値いくつ？', ogdesc='いいね・保存とフォロワー数から、投稿のバズ偏差値を判定。',
  h1='バズ偏差値メーター',
  lead='その投稿、伸びてる？それとも普通？フォロワー数に対する反応の大きさ（エンゲージメント率）から、投稿の「バズ偏差値」を出します。',
  inputs='''    <h2>📊 投稿の数字を入れる</h2>
    <div class="row"><div class="field"><label>フォロワー数 <span class="hint">（人）</span></label><input type="number" id="fol" value="1000" min="1" inputmode="numeric"></div>
    <div class="field"><label>いいね数</label><input type="number" id="like" value="50" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>保存・リポスト数 <span class="hint">（合計・分からなければ0）</span></label><input type="number" id="save" value="10" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">バズ偏差値を出す</button>''',
  result='''      <div class="label">あなたの投稿の バズ偏差値は</div>
      <div class="big"><span id="big">0</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">エンゲージ率</div><div class="v accent" id="er">—</div></div>
      <div class="stat"><div class="k">推定リーチ</div><div class="v" id="reach">—</div></div>
      <div class="stat"><div class="k">判定</div><div class="v" id="judge">—</div></div></div>''',
  article='''    <h2>計算の考え方</h2>
    <div class="note"><strong>計算式</strong><br>エンゲージ率 ＝（いいね＋保存・リポスト）÷ フォロワー数 ×100<br>これを一般的な水準（約3%）と比べ、偏差値に換算しています。</div>
    <p>フォロワーが多いほど「いいね数」は伸びますが、本当に伸びている投稿かは<strong>率</strong>で見るのが基本。保存・リポストは強いシグナルで、ここが多い投稿はおすすめに乗りやすくなります。</p>
    <h2>よくある質問</h2>'''+faq([('偏差値はどう出していますか？','エンゲージ率を一般的な水準と比較した簡易換算です。プラットフォームやジャンルで基準は変わります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const f=Math.max(1,+$('fol').value||1), l=Math.max(0,+$('like').value||0), s=Math.max(0,+$('save').value||0);
    const er=(l+s)/f*100;
    let h=50+12*Math.log10((er+0.2)/3); h=Math.max(30,Math.min(99,h));
    const reach=Math.round((l+s)*(8+Math.min(20,er)));
    let j; if(h>=70)j='大バズり🔥'; else if(h>=58)j='かなり好調'; else if(h>=45)j='平均的'; else j='これからの伸びしろ大';
    $('sub').textContent=`いいね${l}＋保存${s} ÷ フォロワー${num(f)}`;
    $('er').textContent=er.toFixed(1)+'%'; $('reach').textContent=num(reach)+'人'; $('judge').textContent=j;
    SHARE=`私の投稿のバズ偏差値は${Math.round(h)}でした📊（エンゲージ率${er.toFixed(1)}%）\\nあなたの投稿は？👇`;
    show(); anim($('big'),0,h,900);
  }'''))

# 2. 松竹梅の法則
SIMS.append(dict(id='kakaku-matsu', cat=MKT, emoji='🍣',
  title='松竹梅の法則シミュレーター｜真ん中はどれだけ選ばれる？｜シミュラボ',
  desc='3段階の価格（松・竹・梅）を入れると、おとり効果で「真ん中」がどれだけ選ばれやすくなるか、推定選択率と平均客単価を試算する無料シミュレーター。',
  ogtitle='松竹梅の法則シミュレーター｜真ん中はどれだけ選ばれる？', ogdesc='3段階価格を入れると、真ん中が選ばれる率と平均客単価を試算。',
  h1='松竹梅の法則シミュレーター',
  lead='メニューを「松・竹・梅」の3段階にすると、人は真ん中を選びやすくなる。価格を入れると、各プランの推定選択率と平均客単価を出します。',
  inputs='''    <h2>🍣 3段階の価格を入れる</h2>
    <div class="field"><label>梅（安いプラン） <span class="hint">（円）</span></label><input type="number" id="ume" value="2000" min="0" inputmode="numeric"></div>
    <div class="field"><label>竹（真ん中プラン） <span class="hint">（円）</span></label><input type="number" id="take" value="3500" min="0" inputmode="numeric"></div>
    <div class="field"><label>松（高いプラン） <span class="hint">（円）</span></label><input type="number" id="matsu" value="6000" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">選ばれ方を試算する</button>''',
  result='''      <div class="label">真ん中（竹）が選ばれる率</div>
      <div class="big"><span id="big">0</span><span class="unit">%</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">平均客単価</div><div class="v accent" id="avg">—</div></div>
      <div class="stat"><div class="k">松が選ばれる率</div><div class="v" id="pm">—</div></div>
      <div class="stat"><div class="k">梅が選ばれる率</div><div class="v" id="pu">—</div></div></div>''',
  article='''    <h2>松竹梅の法則とは</h2>
    <p>選択肢が3つあると、人は両端を避けて「真ん中」を選びやすくなります（極端の回避）。一番売りたい価格を真ん中に置くのが定石です。</p>
    <div class="note"><strong>計算の考え方</strong><br>基準を「梅30%・竹50%・松20%」とし、松と竹の価格差が大きいほど竹に集まる傾向を反映。平均客単価＝各価格×推定選択率の合計。あくまで傾向の目安です。</div>
    <h2>よくある質問</h2>'''+faq([('実際の比率と同じですか？','いいえ。商品・客層で変わります。本ツールは「真ん中効果」を体感するための簡易モデルです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const u=Math.max(0,+$('ume').value||0), t=Math.max(0,+$('take').value||0), m=Math.max(0,+$('matsu').value||0);
    let pu=30, pt=50, pm=20;
    const gap = (m>0&&t>0)? m/t : 1.5;
    if(gap>=1.6){ pt+=8; pm-=6; pu-=2; } else if(gap<=1.3){ pm+=6; pt-=4; pu-=2; }
    pu=Math.max(5,pu); pt=Math.max(5,pt); pm=Math.max(5,pm);
    const sum=pu+pt+pm; pu=pu/sum*100; pt=pt/sum*100; pm=pm/sum*100;
    const avg=(u*pu+t*pt+m*pm)/100;
    $('sub').textContent=`梅${num(u)}円／竹${num(t)}円／松${num(m)}円`;
    $('avg').textContent=yen(avg); $('pm').textContent=Math.round(pm)+'%'; $('pu').textContent=Math.round(pu)+'%';
    SHARE=`松竹梅シミュ：真ん中の「竹」が約${Math.round(pt)}%に選ばれ、平均客単価は${yen(avg)}🍣\\n価格設計、真ん中が主役。👇`;
    show(); anim($('big'),0,pt,900);
  }'''))

# 3. ネーミングバズ度診断
SIMS.append(dict(id='naming-buzz', cat=MKT, emoji='🏷️',
  title='ネーミングバズ度診断｜その商品名、バズる名前？｜シミュラボ',
  desc='商品名・サービス名を入れるだけで、文字数・カタカナ率・リズムなどから「覚えやすさ／バズりやすさ」を点数化するエンタメ診断シミュレーター。',
  ogtitle='ネーミングバズ度診断｜その商品名、バズる名前？', ogdesc='商品名を入れると、覚えやすさ・バズりやすさを点数化。',
  h1='ネーミングバズ度診断',
  lead='良い商品名は、それだけで広がります。商品・サービス名を入れると、文字数やリズムから「覚えやすさ・バズりやすさ」を点数化します（エンタメ診断）。',
  inputs='''    <h2>🏷️ 名前を入れる</h2>
    <div class="field"><label>商品・サービス名</label><input type="text" id="nm" value="モグモグ" maxlength="30" placeholder="例：シャキッと野菜"></div>
    <button class="btn btn-primary" id="calcBtn">バズ度を診断する</button>''',
  result='''      <div class="label">この名前のバズ度は</div>
      <div class="big"><span id="big">0</span><span class="unit">点</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:18px;">—</div>''',
  article='''    <h2>覚えやすい名前の条件</h2>
    <p>一般に、①短い（3〜6文字）②声に出しやすいリズム③繰り返しの音（モグモグ等）④数字や具体性、があると記憶に残りやすいと言われます。本診断はそれを簡易点数化したエンタメです。</p>
    <div class="note">💡 迷ったら「声に出して3回言ってみる」。スッと言えて、すぐ思い出せる名前が強い名前です。</div>
    <h2>よくある質問</h2>'''+faq([('点数は正確ですか？','エンタメ診断です。実際の良し悪しは商品との相性・ターゲットで変わります。'),('入力した名前は送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const nm=($('nm').value||'').trim();
    if(!nm){ alert('商品名を入力してね'); return; }
    const len=[...nm].length;
    const kata=(nm.match(/[\\u30A0-\\u30FF]/g)||[]).length;
    const digit=(nm.match(/[0-9０-９]/g)||[]).length;
    const rep=/(.)\\1/.test(nm)?1:0;
    let sc=48;
    if(len>=3&&len<=6) sc+=18; else if(len<=8) sc+=8; else sc-=10;
    sc+=Math.min(14,kata*4);
    if(digit>0) sc+=8;
    if(rep) sc+=12;
    sc=Math.max(20,Math.min(99,sc));
    let a; if(sc>=80)a='覚えやすくて拡散向き。SNSでも一度で覚えてもらえそう🔥';
    else if(sc>=60)a='良いバランス。あと一歩、短く・声に出しやすくするとさらに強い名前に。';
    else if(sc>=45)a='悪くないけど、もう少し短くするか、リズムのある音を足すと印象に残りやすく。';
    else a='少し長め・覚えにくいかも。3〜6文字で、声に出して言いやすい候補も試してみよう。';
    $('sub').textContent=`「${nm}」／${len}文字`;
    $('adv').textContent='🏷️ '+a;
    SHARE=`「${nm}」のネーミングバズ度は${sc}点でした🏷️\\nあなたの商品名は何点？👇`;
    show(); anim($('big'),0,sc,900);
  }'''))

# ========== お金・時間 ==========

# 4. ガチャ天井シミュレーター
SIMS.append(dict(id='gacha', cat=MONEY, emoji='🎴',
  title='ガチャ天井シミュレーター｜推しを引くのに平均いくら？｜シミュラボ',
  desc='排出確率・1回の価格・天井回数から、狙ったキャラ／アイテムを引くまでの「期待課金額」と天井までの最大額を試算する無料シミュレーター。',
  ogtitle='ガチャ天井シミュレーター｜推しを引くのに平均いくら？', ogdesc='排出率と価格から、当てるまでの期待課金額・天井までの最大額を試算。',
  h1='ガチャ天井シミュレーター',
  lead='その1点を引くまでに、平均でいくら溶ける？排出率・1回の価格・天井から、期待課金額と「最悪いくらまで」を冷静に見える化します。',
  inputs='''    <h2>🎴 条件を入れる</h2>
    <div class="row"><div class="field"><label>排出確率 <span class="hint">（％）</span></label><input type="number" id="rate" value="3" min="0.01" max="100" step="0.1" inputmode="decimal"></div>
    <div class="field"><label>1回の価格 <span class="hint">（円）</span></label><input type="number" id="price" value="300" min="1" inputmode="numeric"></div></div>
    <div class="field"><label>天井 <span class="hint">（◯回で確定／無いなら0）</span></label><input type="number" id="ceil" value="200" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">期待課金額を見る</button>''',
  result='''      <div class="label">1点引くまでの 期待課金額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">平均で引ける回数</div><div class="v" id="exp">—</div></div>
      <div class="stat"><div class="k">半分の人が引ける回数</div><div class="v" id="med">—</div></div>
      <div class="stat"><div class="k">天井までの最大</div><div class="v accent" id="ceilyen">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>期待回数 ＝ 1 ÷ 排出率／期待課金 ＝ 期待回数 × 1回の価格<br>半分の人が引ける回数（中央値）＝ log(0.5) ÷ log(1−排出率)</div>
    <p>「3%なら33回くらいで出る」が平均ですが、確率なので<strong>もっと引けない人も多数</strong>います。だから天井（上限）が安心材料になります。遊ぶ前に上限額を決めておくのがおすすめです。</p>
    <h2>よくある質問</h2>'''+faq([('必ずこの金額で引けますか？','いいえ。あくまで確率上の平均です。実際は大きくブレます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const p=Math.max(0.01,Math.min(100,+$('rate').value||1))/100;
    const price=Math.max(1,+$('price').value||300);
    const ceil=Math.max(0,+$('ceil').value||0);
    const exp=1/p, expYen=exp*price;
    const med=Math.log(0.5)/Math.log(1-p);
    const ceilYen=ceil>0?ceil*price:0;
    $('sub').textContent=`排出率${(p*100).toFixed(2)}％・1回${num(price)}円`;
    $('exp').textContent=num(exp)+'回'; $('med').textContent=num(med)+'回';
    $('ceilyen').textContent=ceil>0?yen(ceilYen):'天井なし';
    SHARE=`推しを1点引くのに、平均${yen(expYen)}…🎴（排出率${(p*100).toFixed(2)}％）\\n${ceil>0?'天井まで回すと最大'+yen(ceilYen):'天井がないと青天井…'}\\n計画的に課金しよ。👇`;
    show(); anim($('big'),0,expYen,900);
  }'''))

# 5. 格安SIM乗り換えメーター
SIMS.append(dict(id='kakuyasu-sim', cat=MONEY, emoji='📱',
  title='格安SIM乗り換えメーター｜乗り換えで生涯いくら浮く？｜シミュラボ',
  desc='今のスマホ月額と乗り換え後の月額から、年間・10年・残りの利用年数でどれだけ通信費が浮くかを試算する無料シミュレーター。',
  ogtitle='格安SIM乗り換えメーター｜生涯でいくら浮く？', ogdesc='今の月額と乗り換え後の月額から、浮く通信費を試算。',
  h1='格安SIM乗り換えメーター',
  lead='スマホ代、見直すだけで効いてくる固定費No.1。今の月額と乗り換え後の月額から、年間・残りの人生で浮く金額を出します。',
  inputs='''    <h2>📱 条件を入れる</h2>
    <div class="row"><div class="field"><label>今のスマホ月額 <span class="hint">（円）</span></label><input type="number" id="now" value="8000" min="0" inputmode="numeric"></div>
    <div class="field"><label>乗り換え後の月額 <span class="hint">（円）</span></label><input type="number" id="aft" value="2000" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>あと何年使う <span class="hint">（年）</span></label><input type="number" id="yr" value="30" min="1" max="80" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">浮く金額を見る</button>''',
  result='''      <div class="label" id="lab">残りの人生で 浮く通信費</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">月の差</div><div class="v" id="md">—</div></div>
      <div class="stat"><div class="k">1年で</div><div class="v accent" id="yr1">—</div></div>
      <div class="stat"><div class="k">10年で</div><div class="v" id="yr10">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>浮く金額 ＝（今の月額 − 乗り換え後の月額）× 12 × 年数</div>
    <p>通信費は「毎月・自動で」出ていく固定費。一度見直せば、あとは何もしなくても差が積み上がります。データ量・通話の使い方に合うプランを選ぶのがコツです。</p>
    <h2>よくある質問</h2>'''+faq([('乗り換えの手間や端末代は？','本ツールは月額差のみの概算です。事務手数料・端末代は別途ご確認ください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const now=Math.max(0,+$('now').value||0), aft=Math.max(0,+$('aft').value||0), yr=Math.max(1,+$('yr').value||1);
    const md=now-aft, total=md*12*yr;
    $('lab').textContent= total>=0?'残りの人生で 浮く通信費':'残りの人生で 増える通信費';
    $('sub').textContent=`月${num(now)}円 → ${num(aft)}円・${yr}年で`;
    $('md').textContent=num(Math.abs(md))+'円'; $('yr1').textContent=yen(Math.abs(md)*12); $('yr10').textContent=yen(Math.abs(md)*12*10);
    SHARE= md>=0?`スマホを格安SIMに乗り換えると、残り${yr}年で約${yen(Math.abs(total))}も浮く計算だった📱\\n固定費の見直し、効くなぁ。👇`:`今の見直し案だと逆に約${yen(Math.abs(total))}増える計算…📱要再検討👇`;
    show(); anim($('big'),0,Math.abs(total),900);
  }'''))

# 6. 自販機損失メーター
SIMS.append(dict(id='jihanki', cat=MONEY, emoji='🥤',
  title='自販機 損失メーター｜まとめ買いと比べていくら損してる？｜シミュラボ',
  desc='1日に買う本数と、自販機価格・まとめ買い時の1本価格から、1年・10年・生涯でどれだけ多く払っているかを試算する無料シミュレーター。',
  ogtitle='自販機 損失メーター｜まとめ買いといくら差がつく？', ogdesc='毎日の自販機ドリンク、まとめ買いと比べた差額を試算。',
  h1='自販機 損失メーター',
  lead='毎日の1本、自販機で買うかまとめ買いするかで、長い目で見ると大きな差に。1日の本数と価格差から、積み上がる差額を出します。',
  inputs='''    <h2>🥤 条件を入れる</h2>
    <div class="field"><label>1日に買う本数 <span class="hint">（本・小数OK）</span></label><input type="number" id="cnt" value="1" min="0" step="0.1" inputmode="decimal"></div>
    <div class="row"><div class="field"><label>自販機の価格 <span class="hint">（円）</span></label><input type="number" id="vend" value="160" min="0" inputmode="numeric"></div>
    <div class="field"><label>まとめ買いの1本価格 <span class="hint">（円）</span></label><input type="number" id="buy" value="80" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">差額を見る</button>''',
  result='''      <div class="label">1年で 多く払っている額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1ヶ月で</div><div class="v" id="m">—</div></div>
      <div class="stat"><div class="k">10年で</div><div class="v accent" id="y10">—</div></div>
      <div class="stat"><div class="k">30年で</div><div class="v" id="y30">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>1年の差額 ＝（自販機価格 − まとめ買い価格）× 1日の本数 × 365</div>
    <p>1本80円の差でも、毎日なら年に約29,000円。自販機が悪いわけではなく「便利さに払っている額」を知っておくと、使いどころを選べます。</p>
    <h2>よくある質問</h2>'''+faq([('全部やめるべき？','いいえ。便利さの価値もあります。額を知ったうえで、自分なりの使い方を決めるのがおすすめです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const cnt=Math.max(0,+$('cnt').value||0), vend=Math.max(0,+$('vend').value||0), buy=Math.max(0,+$('buy').value||0);
    const diff=Math.max(0,vend-buy), y1=diff*cnt*365;
    $('sub').textContent=`1本あたり差${num(diff)}円 × ${cnt}本/日 × 365日`;
    $('m').textContent=yen(y1/12); $('y10').textContent=yen(y1*10); $('y30').textContent=yen(y1*30);
    SHARE=`自販機ドリンク、まとめ買いより年で約${yen(y1)}多く払ってた🥤\\n10年で${yen(y1*10)}…ちりつもこわい。👇`;
    show(); anim($('big'),0,y1,900);
  }'''))

# ========== 恋愛・婚活 ==========

# 7. 記念日カウンター
SIMS.append(dict(id='kinenbi', cat=LOVE, emoji='💑',
  title='記念日カウンター｜付き合って何日？次の記念日まであと何日？｜シミュラボ',
  desc='付き合い始めた日を入れるだけで、今日までの日数・何年何ヶ月か・次の記念日（100日／1年など）まであと何日かが分かる無料カウンター。',
  ogtitle='記念日カウンター｜付き合って何日？次の記念日は？', ogdesc='付き合った日から、今日までの日数と次の記念日までを計算。',
  h1='記念日カウンター',
  lead='ふたりが一緒にいる時間を、数字にして大切に。付き合い始めた日を入れると、今日までの日数と、次の記念日まであと何日かを表示します。',
  inputs='''    <h2>💑 付き合い始めた日</h2>
    <div class="field"><label>記念日（付き合った日・結婚した日など）</label><input type="date" id="d1" value="2024-06-20"></div>
    <button class="btn btn-primary" id="calcBtn">数えてみる</button>''',
  result='''      <div class="label">付き合って（一緒にいて）</div>
      <div class="big"><span id="big">0</span><span class="unit">日</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">期間にすると</div><div class="v accent" id="ym">—</div></div>
      <div class="stat"><div class="k">次の記念日</div><div class="v" id="next">—</div></div>
      <div class="stat"><div class="k">そこまであと</div><div class="v" id="left">—</div></div></div>''',
  article='''    <h2>使い方</h2>
    <p>付き合った日でも、結婚記念日でも、友達と出会った日でもOK。次の節目（100日・1年・1000日など）を逃さないように、カレンダーに登録しておきましょう。</p>
    <div class="note">💡 100日・500日・1000日・1年・3年・5年…と、節目はたくさん。小さな「おめでとう」を増やすと、毎日がちょっと楽しくなります。</div>
    <h2>よくある質問</h2>'''+faq([('入力した日付は送信されますか？','いいえ。計算はすべてブラウザ内（あなたの端末の中）で完結します。'),('未来の日付を入れたら？','まだ来ていない記念日として「あと何日」を表示します。')]),
  js='''  function calc(){
    const v=$('d1').value; if(!v){ alert('日付を選んでね'); return; }
    const start=new Date(v); const today=new Date(); today.setHours(0,0,0,0); start.setHours(0,0,0,0);
    const days=Math.round((today-start)/86400000);
    if(isNaN(days)){ alert('正しい日付を入れてね'); return; }
    const ad=Math.abs(days);
    if(days<0){
      $('sub').textContent=`記念日まであと${ad}日`; $('ym').textContent='これから';
      $('next').textContent='当日'; $('left').textContent=ad+'日';
      SHARE=`記念日まであと${ad}日、楽しみ💑👇`;
      show(); anim($('big'),0,ad,900); return;
    }
    // カレンダーベースの「◯年◯ヶ月」
    let yy=today.getFullYear()-start.getFullYear(), mm=today.getMonth()-start.getMonth(), dd=today.getDate()-start.getDate();
    if(dd<0) mm--; if(mm<0){ yy--; mm+=12; }
    // 次の記念日＝日数の節目 と 次の周年 の早いほう
    const miles=[100,200,300,500,700,1000,1500,2000,2500,3000,3650,5000,7300,10000];
    const nextDay=miles.find(m=>m>days);
    const anniv=new Date(start); anniv.setFullYear(start.getFullYear()+yy+1);
    const annivDays=Math.round((anniv-start)/86400000);
    let next, lbl;
    if(nextDay && nextDay<annivDays){ next=nextDay; lbl=num(nextDay)+'日'; }
    else { next=annivDays; lbl=(yy+1)+'年'; }
    const left=next-days;
    $('sub').textContent=`${start.getFullYear()}年${start.getMonth()+1}月${start.getDate()}日から`;
    $('ym').textContent=`${yy}年${mm}ヶ月`;
    $('next').textContent=lbl+'記念日';
    $('left').textContent=num(left)+'日';
    SHARE=`記念日カウンター：今日でちょうど${num(days)}日💑\\n次の${lbl}記念日まであと${num(left)}日。\\nあなたは何日目？👇`;
    show(); anim($('big'),0,days,900);
  }'''))

# 8. 遠距離恋愛シミュレーター
SIMS.append(dict(id='enkyori', cat=LOVE, emoji='🚄',
  title='遠距離恋愛シミュレーター｜年間の交通費・会える回数は？｜シミュラボ',
  desc='片道の交通費・会う頻度・片道の所要時間から、遠距離恋愛で1年にかかる交通費・会える回数・移動時間を見える化する無料シミュレーター。',
  ogtitle='遠距離恋愛シミュレーター｜年間の交通費と会える回数', ogdesc='片道交通費と会う頻度から、年間の交通費・会える回数を試算。',
  h1='遠距離恋愛シミュレーター',
  lead='会いに行くたびにかかる時間とお金を、ちゃんと見える化。片道の交通費と会う頻度から、1年でかかる費用・会える回数・移動時間を出します。',
  inputs='''    <h2>🚄 条件を入れる</h2>
    <div class="row"><div class="field"><label>片道の交通費 <span class="hint">（円）</span></label><input type="number" id="fare" value="8000" min="0" inputmode="numeric"></div>
    <div class="field"><label>会う頻度 <span class="hint">（月に何回）</span></label><input type="number" id="freq" value="2" min="0" step="0.5" inputmode="decimal"></div></div>
    <div class="field"><label>片道の所要時間 <span class="hint">（時間）</span></label><input type="number" id="hours" value="2" min="0" step="0.5" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">年間コストを見る</button>''',
  result='''      <div class="label">1年でかかる 交通費</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">年に会える回数</div><div class="v accent" id="trips">—</div></div>
      <div class="stat"><div class="k">年間の移動時間</div><div class="v" id="hrs">—</div></div>
      <div class="stat"><div class="k">1回（往復）あたり</div><div class="v" id="per">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>年間の会う回数 ＝ 月の頻度 × 12<br>年間の交通費 ＝ 片道交通費 × 2 × 年間の会う回数</div>
    <p>遠距離は「お金と時間」をふたりでどう分担するかが続けるコツ。交通費を折半する、真ん中の街で会う、閑散期の割引を使う…工夫しだいで負担はぐっと軽くなります。</p>
    <h2>よくある質問</h2>'''+faq([('宿泊費は含まれますか？','いいえ。本ツールは交通費のみの概算です。宿泊や食事は別途見込んでください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const fare=Math.max(0,+$('fare').value||0), freq=Math.max(0,+$('freq').value||0), hours=Math.max(0,+$('hours').value||0);
    const trips=freq*12, yearFare=fare*2*trips, yearHours=hours*2*trips;
    $('sub').textContent=`片道${num(fare)}円・月${freq}回・片道${hours}時間`;
    $('trips').textContent=num(trips)+'回'; $('hrs').textContent=num(yearHours)+'時間'; $('per').textContent=yen(fare*2);
    SHARE=`遠距離恋愛シミュ：1年の交通費は約${yen(yearFare)}、移動は年${num(yearHours)}時間🚄\\n会いに行くその時間も、ふたりの思い出。👇`;
    show(); anim($('big'),0,yearFare,900);
  }'''))

# 9. 星座の相性占い
SIMS.append(dict(id='aishou-seiza', cat=LOVE, emoji='⭐',
  title='星座の相性占い｜12星座、ふたりの相性は？｜シミュラボ',
  desc='自分と相手の星座を選ぶだけ。火・地・風・水の4エレメントから、ふたりの相性とひとことアドバイスを占う無料の相性占いシミュレーター。',
  ogtitle='星座の相性占い｜12星座、ふたりの相性は？', ogdesc='自分と相手の星座から、4エレメントで相性を占います。',
  h1='星座の相性占い',
  lead='恋人・友達・気になるあの人。ふたりの星座を選ぶと、火・地・風・水のエレメントから相性を占います。盛り上がる定番のエンタメ占いです。',
  inputs='''    <h2>⭐ ふたりの星座を選ぶ</h2>
    <div class="row"><div class="field"><label>あなたの星座</label><select id="s1">
      <option value="火">牡羊座（おひつじ）</option><option value="地">牡牛座（おうし）</option><option value="風">双子座（ふたご）</option>
      <option value="水">蟹座（かに）</option><option value="火">獅子座（しし）</option><option value="地">乙女座（おとめ）</option>
      <option value="風">天秤座（てんびん）</option><option value="水">蠍座（さそり）</option><option value="火">射手座（いて）</option>
      <option value="地">山羊座（やぎ）</option><option value="風">水瓶座（みずがめ）</option><option value="水">魚座（うお）</option></select></div>
    <div class="field"><label>相手の星座</label><select id="s2">
      <option value="火">牡羊座（おひつじ）</option><option value="地">牡牛座（おうし）</option><option value="風">双子座（ふたご）</option>
      <option value="水" selected>蟹座（かに）</option><option value="火">獅子座（しし）</option><option value="地">乙女座（おとめ）</option>
      <option value="風">天秤座（てんびん）</option><option value="水">蠍座（さそり）</option><option value="火">射手座（いて）</option>
      <option value="地">山羊座（やぎ）</option><option value="風">水瓶座（みずがめ）</option><option value="水">魚座（うお）</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">相性を占う</button>''',
  result='''      <div class="label">ふたりの相性は</div>
      <div class="big"><span id="big">0</span><span class="unit">%</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:18px;">—</div>''',
  article='''    <h2>4つのエレメントとは</h2>
    <p>西洋占星術では12星座を「火（情熱）・地（堅実）・風（知性）・水（感情）」の4グループに分けます。同じ・相性の良いエレメント同士はテンポが合いやすいと言われます。</p>
    <div class="note">💡 相性はあくまでエンタメ。数字が低くても、違いを面白がれる相手とは長く続きます。会話のきっかけに使ってみてください。</div>
    <h2>よくある質問</h2>'''+faq([('相性％はどう決まる？','選んだ星座のエレメントの組み合わせから算出した、占いの目安です。'),('入力内容は送信されますか？','いいえ。占いはすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const a=$('s1').value, b=$('s2').value;
    const M={'火火':92,'地地':86,'風風':88,'水水':90,'火風':89,'風火':89,'地水':87,'水地':87,'火地':62,'地火':62,'火水':55,'水火':55,'風地':60,'地風':60,'風水':58,'水風':58};
    const sc=M[a+b]||70;
    const cm={'火':'情熱','地':'堅実','風':'知性','水':'感情'};
    let a2; if(sc>=85)a2='息ぴったりの黄金コンビ。一緒にいるとテンポよく盛り上がれる関係です✨';
    else if(sc>=70)a2='良い相性。お互いの「らしさ」を尊重すれば、心地よい関係を築けます。';
    else a2='違いが多めだからこそ学び合える二人。相手のペースを面白がると、ぐっと近づけます。';
    $('sub').textContent=`あなた(${cm[a]})×相手(${cm[b]})／${sel('s1').text.replace(/（.*/,'')}×${sel('s2').text.replace(/（.*/,'')}`;
    $('adv').textContent='⭐ '+a2;
    SHARE=`星座の相性占い、ふたりの相性は${sc}%でした⭐\\n${sc>=70?'いい感じ…！':'違いを楽しむ二人。'}\\nあなたたちは何%？👇`;
    show(); anim($('big'),0,sc,900);
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
