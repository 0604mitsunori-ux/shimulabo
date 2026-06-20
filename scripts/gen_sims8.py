# -*- coding: utf-8 -*-
"""シミュラボ：子ども・育児／ペット の2カテゴリ 各10本（計20本）。"""
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

KIDS='子ども・育児'; PET='ペット'
SIMS=[]

# ===== 子ども・育児 =====
SIMS.append(dict(id='kosodate-hiyou', cat=KIDS, emoji='👶',
  title='子育て費用 総額シミュレーター｜子ども1人にいくらかかる？｜シミュラボ',
  desc='進路と子どもの人数から、誕生から大学卒業までにかかる「養育費＋教育費」の総額の目安を試算する無料シミュレーター。',
  ogtitle='子育て費用 総額シミュレーター｜子ども1人にいくら？', ogdesc='進路と人数から、子育てにかかる総額（養育費＋教育費）を試算。',
  h1='子育て費用 総額シミュレーター',
  lead='子ども1人を育てるのに、トータルでいくらかかる？誕生から大学卒業までの「養育費＋教育費」の目安を、進路から試算します。',
  inputs='''    <h2>👶 条件</h2>
    <div class="field"><label>進路のイメージ</label><select id="course">
      <option value="800">すべて公立＋国公立大</option>
      <option value="1100" selected>高校・大学は私立（文系）</option>
      <option value="1300">中学から私立＋私立大文系</option>
      <option value="1600">私立大 理系コース</option>
      <option value="3000">私立 医歯薬系</option></select></div>
    <div class="field"><label>子どもの人数 <span class="hint">（人）</span></label><input type="number" id="n" value="1" min="1" max="10" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">総額を計算する</button>''',
  result='''      <div class="label" id="lab">子ども1人を育てる総額</div>
      <div class="big"><span id="big">0</span><span class="unit">万円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">養育費（食費・衣服・医療等）</div><div class="v" id="you">—</div></div>
      <div class="stat"><div class="k">教育費</div><div class="v" id="edu">—</div></div>
      <div class="stat"><div class="k">毎月いくら備える(22年)</div><div class="v accent" id="mo">—</div></div></div>''',
  article='''    <h2>この試算について</h2>
    <div class="note">養育費（教育費以外の生活費）を約1,640万円とし、進路別の教育費を加えた概算です（各種調査の目安より）。実際は家庭・地域で大きく変わります。</div>
    <p>「総額」は大きく見えますが、22年かけて少しずつ。早めに月いくら備えればよいかを知ると、計画的に準備できます。</p>
    <h2>よくある質問</h2>'''+faq([('習い事や塾は？','教育費の目安に含めていますが、家庭差が大きい部分です。余裕をもって見積もるのがおすすめです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const edu=+$('course').value, you=1640, n=Math.max(1,+$('n').value||1);
    const per=edu+you, total=per*n;
    $('lab').textContent= n>1?(n+'人を育てる総額'):'子ども1人を育てる総額';
    $('sub').textContent=`${sel('course').text}・子ども${n}人`;
    $('you').textContent=num(you*n)+'万円'; $('edu').textContent=num(edu*n)+'万円'; $('mo').textContent=num(per/(22*12)*10000)+'円';
    SHARE=`子育て総額シミュ：子ども${n}人で約${num(total)}万円という試算だった👶（${sel('course').text}）\\nあなたは？👇`;
    show(); anim($('big'),0,total,900);
  }'''))

SIMS.append(dict(id='kodomo-jikan', cat=KIDS, emoji='🧸',
  title='子どもと過ごせる残り時間シミュレーター｜巣立ちまであと何日？｜シミュラボ',
  desc='子どもの今の年齢から、18歳で巣立つまでに一緒に過ごせる残りの日数を計算する無料シミュレーター。今ある時間の大切さに気づくきっかけに。',
  ogtitle='子どもと過ごせる残り時間｜巣立ちまであと何日？', ogdesc='子どもの年齢から、巣立ちまでに一緒に過ごせる残り日数を計算。',
  h1='子どもと過ごせる残り時間',
  lead='子どもと一緒に暮らせるのは、意外と短い時間です。今の年齢から、18歳で巣立つまでに一緒に過ごせる残りの日数を計算します。',
  inputs='''    <h2>🧸 条件</h2>
    <div class="field"><label>お子さんの今の年齢 <span class="hint">（歳）</span></label><input type="number" id="age" value="3" min="0" max="18" inputmode="numeric"></div>
    <div class="field"><label>巣立つ年齢 <span class="hint">（歳・進学や就職で家を出る目安）</span></label><input type="number" id="leave" value="18" min="1" max="25" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">残りの時間を見る</button>''',
  result='''      <div class="label">巣立ちまで、一緒に過ごせるのは あと</div>
      <div class="big"><span id="big">0</span><span class="unit">日</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">残りの年数</div><div class="v accent" id="years">—</div></div>
      <div class="stat"><div class="k">残りの夏休み</div><div class="v" id="natsu">—</div></div>
      <div class="stat"><div class="k">すでに過ごした割合</div><div class="v" id="done">—</div></div></div>''',
  article='''    <h2>この計算について</h2>
    <p>子どもが家で過ごす時間の多くは、18歳までに集中していると言われます。残りの日数や「あと何回の夏休み」を知ると、今ある時間がいっそう大切に感じられます。</p>
    <div class="note">数字で脅すためではなく、今日の「いってらっしゃい」を大切にするためのツールです。</div>
    <h2>よくある質問</h2>'''+faq([('巣立ちの年齢は？','進学・就職などご家庭の想定で変えてください。一緒に暮らす期間の目安です。'),('データは送信されますか？','いいえ。入力した年齢などは外部に送信されません。')]),
  js='''  function calc(){
    const age=Math.max(0,+$('age').value||0), leave=Math.max(0,+$('leave').value||0);
    const ry=Math.max(0,leave-age), days=ry*365, natsu=ry;
    $('sub').textContent=`今${age}歳・${leave}歳で巣立つ想定`;
    $('years').textContent=ry+'年'; $('natsu').textContent=natsu+'回'; $('done').textContent= leave>0?Math.round(age/leave*100)+'%':'—';
    SHARE=`子どもと一緒に過ごせるのは、巣立ちまであと約${num(days)}日（夏休みあと${natsu}回）だった🧸\\n一日一日を大切に。あなたは？👇`;
    show(); anim($('big'),0,days,900);
  }'''))

SIMS.append(dict(id='ikukyu', cat=KIDS, emoji='🍼',
  title='育休手当シミュレーター｜育児休業給付金はいくらもらえる？｜シミュラボ',
  desc='月給と育休の取得月数から、育児休業給付金（最初6か月67%・以降50%）の総額の目安を試算する無料シミュレーター。',
  ogtitle='育休手当シミュレーター｜育児休業給付金はいくら？', ogdesc='月給と育休月数から、育児休業給付金の総額を試算。',
  h1='育休手当シミュレーター',
  lead='育児休業中にもらえる「育児休業給付金」。最初の半年は給料の約67%、その後は50%が目安です。あなたの育休手当の総額を試算します。',
  inputs='''    <h2>🍼 条件</h2>
    <div class="row"><div class="field"><label>休む前の月給 <span class="hint">（万円・額面）</span></label><input type="number" id="pay" value="25" min="0" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>育休の取得月数 <span class="hint">（月）</span></label><input type="number" id="months" value="12" min="0" max="36" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">育休手当を計算する</button>''',
  result='''      <div class="label">育休手当の総額（目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">最初6か月(67%)</div><div class="v" id="first">—</div></div>
      <div class="stat"><div class="k">7か月目以降(50%)</div><div class="v" id="after">—</div></div>
      <div class="stat"><div class="k">月あたりの目安</div><div class="v accent" id="mo">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>育児休業給付金</strong><br>最初の180日：休業前賃金の約67%／181日目以降：約50%<br>（上限あり・社会保険料は免除される点も実質プラス）</div>
    <p>育休中は給付金に加えて社会保険料が免除されるため、手取りの実質は数字以上に守られます。制度を知って、安心して育休を取りましょう。</p>
    <h2>よくある質問</h2>'''+faq([('上限はある？','給付には上限額があります。高収入の方は実際の額が本ツールより低くなる場合があります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const pay=Math.max(0,+$('pay').value||0)*10000, m=Math.max(0,+$('months').value||0);
    const m1=Math.min(6,m), m2=Math.max(0,m-6);
    const first=pay*0.67*m1, after=pay*0.50*m2, total=first+after;
    $('sub').textContent=`月給${num(pay/10000)}万・育休${m}か月`;
    $('first').textContent=yen(first); $('after').textContent=yen(after); $('mo').textContent= m>0?yen(total/m):'—';
    SHARE=`育休手当シミュ：${m}か月の育休で総額 約${yen(total)}もらえる試算だった🍼\\n社会保険料も免除。あなたは？👇`;
    show(); anim($('big'),0,total,900);
  }'''))

SIMS.append(dict(id='jidou-teate', cat=KIDS, emoji='🎒',
  title='児童手当 総額シミュレーター｜18歳までにいくらもらえる？｜シミュラボ',
  desc='子どもの今の年齢と第何子かから、児童手当を18歳（高校卒業）まで受け取った場合の総額を試算する無料シミュレーター（拡充後の制度に対応）。',
  ogtitle='児童手当 総額シミュレーター｜18歳までにいくら？', ogdesc='子どもの年齢から、児童手当を18歳まで受け取る総額を試算。',
  h1='児童手当 総額シミュレーター',
  lead='毎月もらえる児童手当、18歳（高校卒業）まで合計するといくら？子どもの年齢から総額を試算します（拡充後の制度に対応）。',
  inputs='''    <h2>🎒 条件</h2>
    <div class="row"><div class="field"><label>子どもの今の年齢 <span class="hint">（歳）</span></label><input type="number" id="age" value="0" min="0" max="18" inputmode="numeric"></div>
    <div class="field"><label>第何子？</label><select id="order"><option value="1" selected>第1子・第2子</option><option value="3">第3子以降</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">総額を計算する</button>''',
  result='''      <div class="label">18歳までにもらえる児童手当 総額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">残り受給期間</div><div class="v accent" id="years">—</div></div>
      <div class="stat"><div class="k">月あたり(現在)</div><div class="v" id="now">—</div></div></div>''',
  article='''    <h2>この試算について</h2>
    <div class="note"><strong>支給額（拡充後の目安）</strong><br>0〜3歳：月15,000円／3歳〜18歳：月10,000円<br>第3子以降：一律 月30,000円<br>※所得制限は撤廃されています。</div>
    <p>制度は改定されることがあります。最新の支給額・条件はお住まいの自治体でご確認ください。</p>
    <h2>よくある質問</h2>'''+faq([('もう受け取った分は？','本ツールは「今の年齢から18歳まで」の残りの総額です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const age=Math.max(0,Math.min(18,+$('age').value||0)), order=+$('order').value;
    let total, nowM;
    if(order===3){ total=30000*12*(18-age); nowM=30000; }
    else { const y03=Math.max(0,3-age), y318=18-Math.max(age,3); total=15000*12*y03+10000*12*y318; nowM= age<3?15000:10000; }
    $('sub').textContent=`今${age}歳・${sel('order').text}`;
    $('years').textContent=(18-age)+'年'; $('now').textContent=yen(nowM);
    SHARE=`児童手当、うちは18歳まで総額 約${yen(total)}もらえる試算だった🎒\\n（${sel('order').text}・今${age}歳）あなたは？👇`;
    show(); anim($('big'),0,total,900);
  }'''))

SIMS.append(dict(id='hoiku-youchi', cat=KIDS, emoji='🏫',
  title='保育園 vs 幼稚園 コストシミュレーター｜総額でどっちが安い？｜シミュラボ',
  desc='保育園と幼稚園（＋預かり保育）の月額と通う年数から、卒園までにかかる費用の総額を比較する無料シミュレーター。',
  ogtitle='保育園 vs 幼稚園 コスト｜総額でどっちが安い？', ogdesc='保育園と幼稚園の月額から、卒園までの総額を比較。',
  h1='保育園 vs 幼稚園 コストシミュレーター',
  lead='保育園と幼稚園、トータルでかかるお金はどう違う？それぞれの月額と通う年数から、卒園までの費用を比べてみましょう。',
  inputs='''    <h2>🏫 条件</h2>
    <div class="row"><div class="field"><label>保育園の月額 <span class="hint">（円・給食費等含む実質）</span></label><input type="number" id="a" value="40000" min="0" inputmode="numeric"></div>
    <div class="field"><label>幼稚園＋預かりの月額 <span class="hint">（円）</span></label><input type="number" id="b" value="30000" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>通う年数 <span class="hint">（年）</span></label><input type="number" id="y" value="3" min="1" max="6" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">総額を比べる</button>''',
  result='''      <div class="label" id="lab">総額で安いのは</div>
      <div class="big" style="font-size:clamp(30px,7vw,50px)"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">保育園 総額</div><div class="v" id="ta">—</div></div>
      <div class="stat"><div class="k">幼稚園 総額</div><div class="v" id="tb">—</div></div>
      <div class="stat"><div class="k">差</div><div class="v accent" id="diff">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>総額＝月額×12×通う年数</div>
    <p>3〜5歳は幼児教育・保育の無償化の対象ですが、給食費・行事費・預かり保育などで差が出ます。実質の月額で比べるのがポイントです。</p>
    <h2>よくある質問</h2>'''+faq([('無償化は反映される？','無償化後の「実質の月額」を入力して比べてください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const a=Math.max(0,+$('a').value||0), b=Math.max(0,+$('b').value||0), y=Math.max(1,+$('y').value||1);
    const ta=a*12*y, tb=b*12*y, diff=Math.abs(ta-tb), win= ta<=tb?'保育園':'幼稚園';
    $('big').textContent=win; $('sub').textContent=`${y}年で比較`;
    $('ta').textContent=yen(ta); $('tb').textContent=yen(tb); $('diff').textContent=yen(diff);
    SHARE=`保育園 vs 幼稚園、${y}年の総額は保育園${yen(ta)}／幼稚園${yen(tb)}。安いのは「${win}」🏫\\nあなたは？👇`;
    show();
  }'''))

SIMS.append(dict(id='omutsu', cat=KIDS, emoji='🧷',
  title='おむつ 総数・費用シミュレーター｜卒業まで何枚・いくら？｜シミュラボ',
  desc='1日のおむつ枚数・おむつ卒業の年齢・1枚の値段から、おむつが外れるまでに使う総枚数と費用を計算する無料シミュレーター。',
  ogtitle='おむつ 総数・費用シミュレーター｜卒業まで何枚？', ogdesc='1日の枚数と卒業年齢から、おむつの総枚数と費用を計算。',
  h1='おむつ 総数・費用シミュレーター',
  lead='毎日替えるおむつ、卒業までに何枚使う？費用はいくら？1日の枚数から、おむつ卒業までの総枚数と総額を計算します。',
  inputs='''    <h2>🧷 条件</h2>
    <div class="row"><div class="field"><label>1日のおむつ枚数 <span class="hint">（枚）</span></label><input type="number" id="perday" value="6" min="1" inputmode="numeric"></div>
    <div class="field"><label>おむつ卒業の年齢 <span class="hint">（歳）</span></label><input type="number" id="age" value="3" min="1" max="6" step="0.5" inputmode="decimal"></div></div>
    <div class="field"><label>おむつ1枚の値段 <span class="hint">（円）</span></label><input type="number" id="price" value="20" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">総数・費用を見る</button>''',
  result='''      <div class="label">卒業までに使うおむつの総枚数</div>
      <div class="big"><span id="big">0</span><span class="unit">枚</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">総費用</div><div class="v accent" id="cost">—</div></div>
      <div class="stat"><div class="k">1日の枚数</div><div class="v" id="pd">—</div></div>
      <div class="stat"><div class="k">替えにかかる生涯時間</div><div class="v" id="time">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>総枚数＝1日の枚数×365×卒業年齢<br>総費用＝総枚数×1枚の値段</div>
    <p>毎日のことなので積み重なると驚きの枚数に。新生児期は1日10枚以上替えることも。今だけの大変さ、お疲れさまです。</p>
    <h2>よくある質問</h2>'''+faq([('替えの時間って？','1回3分として、総枚数×3分で概算しています。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const pd=Math.max(1,+$('perday').value||1), age=Math.max(0,+$('age').value||0), price=Math.max(0,+$('price').value||0);
    const total=pd*365*age, cost=total*price, hours=total*3/60;
    $('sub').textContent=`1日${pd}枚 × 365日 × ${age}歳`;
    $('cost').textContent=yen(cost); $('pd').textContent=pd+'枚'; $('time').textContent=num(hours)+'時間';
    SHARE=`おむつ卒業まで、総数 約${num(total)}枚・費用${yen(cost)}という試算だった🧷\\n毎日の育児、お疲れさまです。あなたは？👇`;
    show(); anim($('big'),0,total,900);
  }'''))

SIMS.append(dict(id='shinchou', cat=KIDS, emoji='📏',
  title='子どもの身長予測シミュレーター｜両親の身長から予測｜シミュラボ',
  desc='お父さんとお母さんの身長から、子どもの大人になったときの予測身長を計算する無料シミュレーター（一般的な予測式を使用）。',
  ogtitle='子どもの身長予測シミュレーター｜両親の身長から', ogdesc='両親の身長から、子どもの大人になった時の予測身長を計算。',
  h1='子どもの身長予測シミュレーター',
  lead='お子さんは将来どれくらい背が伸びる？お父さん・お母さんの身長から、大人になったときの予測身長を計算します（あくまで目安）。',
  inputs='''    <h2>📏 条件</h2>
    <div class="field"><label>お子さんの性別</label><select id="sex"><option value="m">男の子</option><option value="f">女の子</option></select></div>
    <div class="row"><div class="field"><label>お父さんの身長 <span class="hint">（cm）</span></label><input type="number" id="dad" value="172" min="100" max="220" inputmode="numeric"></div>
    <div class="field"><label>お母さんの身長 <span class="hint">（cm）</span></label><input type="number" id="mom" value="158" min="100" max="220" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">予測身長を見る</button>''',
  result='''      <div class="label">大人になったときの予測身長</div>
      <div class="big"><span id="big">0</span><span class="unit">cm</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">目安の範囲</div><div class="v accent" id="range" style="font-size:16px;">—</div></div>
      <div class="stat"><div class="k">両親の平均</div><div class="v" id="avg">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>予測式（一般的な目安）</strong><br>男の子：(父＋母＋13)÷2<br>女の子：(父＋母−13)÷2</div>
    <p>身長は遺伝だけでなく、睡眠・栄養・運動でも変わります。あくまで目安として、±9cmほどの幅をもって楽しんでください。</p>
    <h2>よくある質問</h2>'''+faq([('絶対この身長になる？','いいえ。生活習慣などで大きく変わります。エンタメ・参考としてお使いください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const sex=$('sex').value, dad=+$('dad').value||0, mom=+$('mom').value||0;
    const pred = sex==='m' ? (dad+mom+13)/2 : (dad+mom-13)/2;
    $('sub').textContent=`${sex==='m'?'男の子':'女の子'}・父${dad}cm・母${mom}cm`;
    $('range').textContent=Math.round(pred-9)+'〜'+Math.round(pred+9)+'cm'; $('avg').textContent=((dad+mom)/2).toFixed(1)+'cm';
    SHARE=`子どもの身長予測、大人になると約${Math.round(pred)}cmだった📏（父${dad}・母${mom}）\\nあなたのお子さんは？👇`;
    show(); anim($('big'),0,pred,900);
  }'''))

SIMS.append(dict(id='nezukashi', cat=KIDS, emoji='🌙',
  title='寝かしつけ 生涯時間シミュレーター｜トータルで何時間？｜シミュラボ',
  desc='1日の寝かしつけ時間と何歳まで続けるかから、子育てで寝かしつけに使う生涯の総時間を計算する無料シミュレーター。',
  ogtitle='寝かしつけ 生涯時間シミュレーター｜何時間？', ogdesc='1日の寝かしつけ時間から、生涯の総時間を計算。',
  h1='寝かしつけ 生涯時間シミュレーター',
  lead='毎晩の寝かしつけ、トータルにすると何時間になるのでしょう。大変な毎日も、振り返ればかけがえのない時間。生涯の寝かしつけ時間を計算します。',
  inputs='''    <h2>🌙 条件</h2>
    <div class="row"><div class="field"><label>1日の寝かしつけ時間 <span class="hint">（分）</span></label><input type="number" id="min" value="30" min="0" inputmode="numeric"></div>
    <div class="field"><label>何歳まで <span class="hint">（歳）</span></label><input type="number" id="age" value="5" min="0" max="12" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">生涯時間を見る</button>''',
  result='''      <div class="label">寝かしつけに使う生涯時間</div>
      <div class="big"><span id="big">0</span><span class="unit">時間</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">まる何日分</div><div class="v accent" id="days">—</div></div>
      <div class="stat"><div class="k">絵本にすると</div><div class="v" id="ehon">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>生涯時間＝1日の寝かしつけ時間×365×続ける年数</div>
    <p>毎晩30分でも、5年で約900時間。大変だけれど、子どもが「寝かしつけてほしい」と思うのも今だけ。いつか懐かしくなる時間です。</p>
    <h2>よくある質問</h2>'''+faq([('絵本換算って？','寝かしつけの定番、絵本1冊5分として何冊分かを表示しています。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const m=Math.max(0,+$('min').value||0), age=Math.max(0,+$('age').value||0);
    const totMin=m*365*age, h=totMin/60;
    $('sub').textContent=`1日${m}分 × 365日 × ${age}年`;
    $('days').textContent=(h/24).toFixed(1)+'日'; $('ehon').textContent=num(totMin/5)+'冊分';
    SHARE=`寝かしつけ、生涯で約${num(h)}時間（まる${(h/24).toFixed(1)}日）かけてた…🌙\\n大変だけど今だけ。あなたは？👇`;
    show(); anim($('big'),0,h,900);
  }'''))

SIMS.append(dict(id='gakushi', cat=KIDS, emoji='🐷',
  title='学資 積立シミュレーター｜大学費用、毎月いくら貯める？｜シミュラボ',
  desc='大学費用の目標額・今の子どもの年齢・想定利回りから、18歳までに貯めるための毎月の積立額を逆算する無料シミュレーター。',
  ogtitle='学資 積立シミュレーター｜大学費用、毎月いくら？', ogdesc='大学費用の目標から、18歳までの毎月の積立額を逆算。',
  h1='学資 積立シミュレーター',
  lead='大学入学までに「○○万円」を用意するには、毎月いくら積み立てればいい？今の子どもの年齢から逆算します。',
  inputs='''    <h2>🐷 条件</h2>
    <div class="field"><label>大学費用の目標額 <span class="hint">（万円）</span></label><input type="number" id="goal" value="400" min="0" inputmode="numeric"></div>
    <div class="row"><div class="field"><label>今の子どもの年齢 <span class="hint">（歳）</span></label><input type="number" id="age" value="0" min="0" max="17" inputmode="numeric"></div>
    <div class="field"><label>想定利回り <span class="hint">（％/年・貯金なら0）</span></label><input type="number" id="r" value="1" min="0" max="20" step="0.5" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">毎月の積立額を見る</button>''',
  result='''      <div class="label">毎月の積立額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">積立できる期間</div><div class="v accent" id="years">—</div></div>
      <div class="stat"><div class="k">積み立てる元本</div><div class="v" id="moto">—</div></div>
      <div class="stat"><div class="k">目標額</div><div class="v" id="g2">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>18歳までの月数で、目標額を積み立て（利回りがあれば複利で割引）。</div>
    <p>早く始めるほど、毎月の負担は軽くなります。0歳から始めれば18年。今からコツコツが、いちばんラクな準備です。</p>
    <h2>よくある質問</h2>'''+faq([('学資保険とどっちがいい？','確実性なら保険・預金、増やしたいなら積立投資（元本割れリスクあり）。本ツールは積立額の目安です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const goal=Math.max(0,+$('goal').value||0)*10000, age=Math.max(0,Math.min(17,+$('age').value||0)), ry=(+$('r').value||0)/100;
    const y=18-age, r=ry/12, n=y*12; const m= r>0 ? goal*r/(Math.pow(1+r,n)-1) : goal/n;
    $('sub').textContent=`目標${num(goal/10000)}万・今${age}歳・利回り${(+$('r').value)}%`;
    $('years').textContent=y+'年'; $('moto').textContent=yen(m*n); $('g2').textContent=yen(goal);
    SHARE=`学資積立シミュ：18歳までに${num(goal/10000)}万なら、毎月${yen(m)}の積立が必要だった🐷（今${age}歳）\\nあなたは？👇`;
    show(); anim($('big'),0,m,900);
  }'''))

SIMS.append(dict(id='okozukai', cat=KIDS, emoji='💴',
  title='おこづかい 生涯総額シミュレーター｜子に渡すお金は総額いくら？｜シミュラボ',
  desc='毎月のおこづかいと渡す年数から、子どもに渡すおこづかいの生涯総額を計算する無料シミュレーター。',
  ogtitle='おこづかい 生涯総額シミュレーター｜総額いくら？', ogdesc='毎月のおこづかいと年数から、生涯の総額を計算。',
  h1='おこづかい 生涯総額シミュレーター',
  lead='毎月のおこづかい、子どもが独立するまでに渡す総額はいくら？金額と年数から、生涯のおこづかい総額を計算します。',
  inputs='''    <h2>💴 条件</h2>
    <div class="row"><div class="field"><label>毎月のおこづかい <span class="hint">（円）</span></label><input type="number" id="amt" value="3000" min="0" inputmode="numeric"></div>
    <div class="field"><label>渡す年数 <span class="hint">（年・例: 小4〜高3で9年）</span></label><input type="number" id="years" value="9" min="1" max="20" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">総額を計算する</button>''',
  result='''      <div class="label">おこづかいの生涯総額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1年あたり</div><div class="v" id="yr">—</div></div>
      <div class="stat"><div class="k">渡す回数</div><div class="v accent" id="cnt">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>総額＝毎月のおこづかい×12×渡す年数</div>
    <p>毎月の額は小さくても、長く渡すと大きな金額に。おこづかいは「お金との付き合い方を学ぶ機会」。総額を知ると、渡し方を考えるきっかけにも。</p>
    <h2>よくある質問</h2>'''+faq([('お年玉は？','本ツールは毎月のおこづかいのみの概算です。お年玉や臨時の支出は別途加算してください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const a=Math.max(0,+$('amt').value||0), y=Math.max(1,+$('years').value||1);
    const total=a*12*y;
    $('sub').textContent=`毎月${num(a)}円 × ${y}年`;
    $('yr').textContent=yen(a*12); $('cnt').textContent=(12*y)+'回';
    SHARE=`子に渡すおこづかい、生涯総額で約${yen(total)}という試算だった💴（毎月${num(a)}円×${y}年）\\nあなたは？👇`;
    show(); anim($('big'),0,total,900);
  }'''))

# ===== ペット =====
SIMS.append(dict(id='pet-age', cat=PET, emoji='🐾',
  title='犬・猫の年齢を人間に換算シミュレーター｜うちの子は何歳？｜シミュラボ',
  desc='犬（小型・大型）や猫の年齢を、人間でいう何歳かに換算する無料シミュレーター。うちの子の本当の年齢を知ろう。',
  ogtitle='犬・猫の年齢を人間に換算｜うちの子は何歳？', ogdesc='犬・猫の年齢を人間年齢に換算。うちの子は何歳？',
  h1='犬・猫の年齢 人間換算シミュレーター',
  lead='うちの子、人間でいうと何歳？犬（小型・大型）や猫の年齢を、人間の年齢に換算します。意外と大人かも？',
  inputs='''    <h2>🐾 条件</h2>
    <div class="field"><label>種類</label><select id="type"><option value="small">犬（小〜中型）</option><option value="large">犬（大型）</option><option value="cat">猫</option></select></div>
    <div class="field"><label>今の年齢 <span class="hint">（歳）</span></label><input type="number" id="age" value="3" min="0" max="30" step="0.5" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">人間年齢に換算する</button>''',
  result='''      <div class="label">人間でいうと</div>
      <div class="big"><span id="big">0</span><span class="unit">歳</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">ライフステージ</div><div class="v accent" id="stage" style="font-size:16px;">—</div></div>
      <div class="stat"><div class="k">1年で歳をとる速さ</div><div class="v" id="speed">—</div></div></div>''',
  article='''    <h2>換算の考え方</h2>
    <div class="note">最初の1年で約15歳、2年で約24歳まで一気に成長し、その後は小型犬・猫で1年に約4歳、大型犬で約7歳ずつ年をとる、という一般的な目安で換算しています。</div>
    <p>大型犬ほど歳をとるのが速め。だからこそ、一緒の時間を大切に。健康診断は人間の年齢感覚で考えると分かりやすいです。</p>
    <h2>よくある質問</h2>'''+faq([('犬種で違う？','体格で差があります。本ツールは小〜中型／大型／猫の代表的な目安です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const t=$('type').value, y=Math.max(0,+$('age').value||0);
    let h; if(y<=1) h=15*y; else if(y<=2) h=15+(y-1)*9; else h=24+(y-2)*(t==='large'?7:4);
    const speed= t==='large'?'約7歳/年':'約4歳/年';
    let st= h<13?'子ども':h<20?'青年':h<45?'働き盛り':h<60?'中年':h<75?'シニア':'長寿・大ベテラン';
    $('sub').textContent=`${sel('type').text}・${y}歳`;
    $('stage').textContent=st; $('speed').textContent=speed;
    SHARE=`うちの子（${sel('type').text}・${y}歳）、人間でいうと約${Math.round(h)}歳だった🐾（${st}）\\nあなたの子は？👇`;
    show(); anim($('big'),0,h,900);
  }'''))

SIMS.append(dict(id='pet-hiyou', cat=PET, emoji='🐕',
  title='ペットの生涯費用シミュレーター｜一生でいくらかかる？｜シミュラボ',
  desc='フード・医療・トリミングなどの費用と想定寿命から、ペットを一生育てるのにかかる総額を試算する無料シミュレーター。',
  ogtitle='ペットの生涯費用シミュレーター｜一生でいくら？', ogdesc='フード・医療・トリミング費用から、ペットの生涯費用を試算。',
  h1='ペットの生涯費用シミュレーター',
  lead='ペットを家族に迎えると、一生でどれくらいのお金がかかる？フードや医療費から、生涯の総額を試算します。お迎え前の心づもりに。',
  inputs='''    <h2>🐕 条件</h2>
    <div class="row"><div class="field"><label>月のフード代 <span class="hint">（円）</span></label><input type="number" id="food" value="5000" min="0" inputmode="numeric"></div>
    <div class="field"><label>年の医療費 <span class="hint">（円・ワクチン等込み）</span></label><input type="number" id="med" value="30000" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>年のトリミング・その他 <span class="hint">（円）</span></label><input type="number" id="other" value="40000" min="0" inputmode="numeric"></div>
    <div class="field"><label>想定寿命 <span class="hint">（年）</span></label><input type="number" id="life" value="15" min="1" max="30" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">生涯費用を計算する</button>''',
  result='''      <div class="label">ペットの生涯費用（目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">年あたり</div><div class="v" id="yr">—</div></div>
      <div class="stat"><div class="k">月あたり</div><div class="v accent" id="mo">—</div></div>
      <div class="stat"><div class="k">フード総額</div><div class="v" id="food2">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>生涯費用＝(フード×12＋医療＋トリミング等)×想定寿命</div>
    <p>ペットの生涯費用は数百万円になることも。とくにシニア期は医療費が増えがち。ペット保険や貯蓄で備えておくと安心です。</p>
    <h2>よくある質問</h2>'''+faq([('初期費用は？','お迎え費用やケージ等は別途。本ツールは毎年かかる費用の総額です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const food=Math.max(0,+$('food').value||0), med=Math.max(0,+$('med').value||0), other=Math.max(0,+$('other').value||0), life=Math.max(1,+$('life').value||1);
    const year=food*12+med+other, total=year*life;
    $('sub').textContent=`想定寿命${life}年で計算`;
    $('yr').textContent=yen(year); $('mo').textContent=yen(year/12); $('food2').textContent=yen(food*12*life);
    SHARE=`ペットの生涯費用、約${yen(total)}という試算だった🐕（寿命${life}年）\\n備えて安心。あなたの子は？👇`;
    show(); anim($('big'),0,total,900);
  }'''))

SIMS.append(dict(id='pet-jikan', cat=PET, emoji='🐈',
  title='ペットと過ごせる残り時間シミュレーター｜あと何日一緒にいられる？｜シミュラボ',
  desc='ペットの今の年齢と想定寿命から、これから一緒に過ごせる残りの日数を計算する無料シミュレーター。今ある時間を大切にするきっかけに。',
  ogtitle='ペットと過ごせる残り時間｜あと何日一緒に？', ogdesc='ペットの年齢と寿命から、一緒に過ごせる残り日数を計算。',
  h1='ペットと過ごせる残り時間',
  lead='大切な家族であるペットと、これからどれくらい一緒にいられる？今の年齢と想定寿命から、残りの日数を計算します。今日のなでなでを、いつもより少し大切に。',
  inputs='''    <h2>🐈 条件</h2>
    <div class="row"><div class="field"><label>ペットの今の年齢 <span class="hint">（歳）</span></label><input type="number" id="age" value="5" min="0" max="30" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>想定寿命 <span class="hint">（年・犬猫は15前後）</span></label><input type="number" id="life" value="15" min="1" max="30" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">残りの時間を見る</button>''',
  result='''      <div class="label">これから一緒に過ごせるのは あと</div>
      <div class="big"><span id="big">0</span><span class="unit">日</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">残りの年数</div><div class="v accent" id="years">—</div></div>
      <div class="stat"><div class="k">残りの散歩・遊び</div><div class="v" id="play">—</div></div>
      <div class="stat"><div class="k">一緒に過ごした割合</div><div class="v" id="done">—</div></div></div>''',
  article='''    <h2>この計算について</h2>
    <p>ペットの一生は、人間よりずっと短いもの。残りの日数を知ることで、今ある時間がよりかけがえなく感じられます。数字に一喜一憂せず、今日を大切に過ごしてください。</p>
    <div class="note">想定寿命はあくまで目安です。健康管理で、その日が一日でも先になりますように。</div>
    <h2>よくある質問</h2>'''+faq([('寿命の目安は？','犬猫はおおよそ15年前後ですが、犬種・体格・個体差で大きく変わります。'),('データは送信されますか？','いいえ。入力した年齢などは外部に送信されません。')]),
  js='''  function calc(){
    const age=Math.max(0,+$('age').value||0), life=Math.max(0,+$('life').value||0);
    const ry=Math.max(0,life-age), days=ry*365;
    $('sub').textContent=`今${age}歳・想定寿命${life}年`;
    $('years').textContent=ry.toFixed(1)+'年'; $('play').textContent='約'+num(days)+'回'; $('done').textContent= life>0?Math.round(age/life*100)+'%':'—';
    SHARE=`ペットと一緒に過ごせるのは、あと約${num(days)}日だった🐈\\n今日のなでなでを大切に。あなたの子は？👇`;
    show(); anim($('big'),0,days,900);
  }'''))

SIMS.append(dict(id='pet-hoken', cat=PET, emoji='🏥',
  title='ペット保険 元が取れる？シミュレーター｜入る価値ある？｜シミュラボ',
  desc='月々の保険料・加入年数・想定する生涯医療費・補償割合から、ペット保険で元が取れるか（損得）を試算する無料シミュレーター。',
  ogtitle='ペット保険 元が取れる？｜入る価値ある？', ogdesc='保険料と想定医療費から、ペット保険の損得を試算。',
  h1='ペット保険 元が取れる？シミュレーター',
  lead='ペット保険、入ったほうがいい？月々の保険料と、想定する医療費から、元が取れるか（損得）を試算します。安心料と考えるかどうかの判断材料に。',
  inputs='''    <h2>🏥 条件</h2>
    <div class="row"><div class="field"><label>月々の保険料 <span class="hint">（円）</span></label><input type="number" id="prem" value="3000" min="0" inputmode="numeric"></div>
    <div class="field"><label>加入する年数 <span class="hint">（年）</span></label><input type="number" id="years" value="15" min="1" max="30" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>生涯にかかる医療費の想定 <span class="hint">（円）</span></label><input type="number" id="med" value="600000" min="0" inputmode="numeric"></div>
    <div class="field"><label>保険の補償割合 <span class="hint">（％・50/70が一般的）</span></label><input type="number" id="cover" value="70" min="0" max="100" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">損得を試算する</button>''',
  result='''      <div class="label" id="lab">保険に入ると</div>
      <div class="big"><span id="big">0</span><span class="unit" id="unit">円 おトク</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">支払う保険料 総額</div><div class="v" id="prem2">—</div></div>
      <div class="stat"><div class="k">保険でカバーされる額</div><div class="v accent" id="cov">—</div></div></div>
      <div class="note" style="text-align:left;margin-top:18px;">⚠️ 大きな手術・入院が重なると医療費はもっと膨らむことも。保険は「もしもの高額出費に備える安心料」という面もあります。</div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>保険料総額＝月々の保険料×12×年数<br>カバー額＝想定医療費×補償割合<br>損得＝カバー額−保険料総額</div>
    <p>「元が取れるか」だけでなく、高額医療が突然来ても払える安心も保険の価値です。貯蓄で備えられるなら、それも一つの選択。</p>
    <h2>よくある質問</h2>'''+faq([('医療費の想定はどれくらい？','生涯で数十万〜100万円超とさまざま。シニア期に増えやすい点も考慮を。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const prem=Math.max(0,+$('prem').value||0), y=Math.max(1,+$('years').value||1), med=Math.max(0,+$('med').value||0), cv=(+$('cover').value||0)/100;
    const premTotal=prem*12*y, cover=med*cv, diff=cover-premTotal, plus=diff>=0;
    $('unit').textContent= plus?'円 おトク':'円 払い超過';
    $('sub').textContent=`月${num(prem)}円×${y}年・医療費${num(med)}円・補償${(cv*100)}%`;
    $('prem2').textContent=yen(premTotal); $('cov').textContent=yen(cover);
    SHARE= plus?`ペット保険、この想定だと約${yen(Math.abs(diff))}おトクの試算だった🏥\\nあなたの子は？👇`:`ペット保険、この想定だと約${yen(Math.abs(diff))}の払い超過。でも"もしも"の安心料かも🏥\\n👇`;
    show(); anim($('big'),0,Math.abs(diff),900);
  }'''))

SIMS.append(dict(id='sanpo', cat=PET, emoji='🦮',
  title='犬の散歩 生涯距離シミュレーター｜一生で何km歩く？｜シミュラボ',
  desc='1日の散歩距離と散歩する年数から、犬と一緒に歩く生涯の総距離を計算する無料シミュレーター。地球何周分かも分かります。',
  ogtitle='犬の散歩 生涯距離シミュレーター｜一生で何km？', ogdesc='1日の散歩距離から、犬と歩く生涯の総距離を計算。地球何周分？',
  h1='犬の散歩 生涯距離シミュレーター',
  lead='毎日の散歩、ワンちゃんと一緒に歩く距離を一生分にすると…？1日の距離から、生涯の総距離を計算します。地球何周分になるかな？',
  inputs='''    <h2>🦮 条件</h2>
    <div class="row"><div class="field"><label>1日の散歩距離 <span class="hint">（km・往復合計）</span></label><input type="number" id="km" value="2" min="0" step="0.1" inputmode="decimal"></div>
    <div class="field"><label>散歩する年数 <span class="hint">（年）</span></label><input type="number" id="years" value="12" min="0" max="25" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">生涯距離を見る</button>''',
  result='''      <div class="label">一生で一緒に歩く距離</div>
      <div class="big"><span id="big">0</span><span class="unit">km</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">地球（4万km）</div><div class="v accent" id="earth">—</div></div>
      <div class="stat"><div class="k">1年で</div><div class="v" id="yr">—</div></div>
      <div class="stat"><div class="k">歩いた歩数(概算)</div><div class="v" id="steps">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>生涯距離＝1日の散歩距離×365×散歩する年数</div>
    <p>毎日2kmでも、12年で約8,760km。日本列島を縦断するどころか、地球を何分の一も歩く距離に。散歩は健康にも、絆を深めるのにも大切な時間です。</p>
    <h2>よくある質問</h2>'''+faq([('歩数の計算は？','1km＝約1,300歩として概算しています。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const km=Math.max(0,+$('km').value||0), y=Math.max(0,+$('years').value||0);
    const total=km*365*y;
    $('sub').textContent=`1日${km}km × 365日 × ${y}年`;
    $('earth').textContent=(total/40000).toFixed(2)+'周'; $('yr').textContent=num(km*365)+'km'; $('steps').textContent=num(total*1300)+'歩';
    SHARE=`愛犬との散歩、一生で約${num(total)}km（地球${(total/40000).toFixed(2)}周分）歩く計算だった🦮\\nあなたの子は？👇`;
    show(); anim($('big'),0,total,900);
  }'''))

SIMS.append(dict(id='neko-nemuri', cat=PET, emoji='😺',
  title='猫が寝てる時間シミュレーター｜一生でどれだけ寝てる？｜シミュラボ',
  desc='1日の睡眠時間と想定寿命から、猫が一生のうちで寝て過ごす総時間を計算する無料シミュレーター。猫はやっぱり寝てばかり？',
  ogtitle='猫が寝てる時間シミュレーター｜一生でどれだけ寝てる？', ogdesc='1日の睡眠時間から、猫が生涯で寝て過ごす時間を計算。',
  h1='猫が寝てる時間シミュレーター',
  lead='よく寝る猫。一生のうち、どれくらいの時間を寝て過ごすのでしょう？1日の睡眠時間から、生涯の睡眠時間を計算します。',
  inputs='''    <h2>😺 条件</h2>
    <div class="row"><div class="field"><label>1日の睡眠時間 <span class="hint">（時間・猫は14〜16が目安）</span></label><input type="number" id="hours" value="16" min="0" max="24" inputmode="numeric"></div>
    <div class="field"><label>想定寿命 <span class="hint">（年）</span></label><input type="number" id="life" value="15" min="1" max="30" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">寝てる時間を見る</button>''',
  result='''      <div class="label">一生で寝て過ごす時間</div>
      <div class="big"><span id="big">0</span><span class="unit">時間</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">まる何日分</div><div class="v accent" id="days">—</div></div>
      <div class="stat"><div class="k">起きている時間</div><div class="v" id="awake">—</div></div>
      <div class="stat"><div class="k">人生に占める割合</div><div class="v" id="rate">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>生涯睡眠時間＝1日の睡眠時間×365×想定寿命</div>
    <p>猫は1日の3分の2近くを寝て過ごす動物。狩りに備えてエネルギーを温存する習性のなごりと言われます。気持ちよさそうに寝ている姿、見ているだけで癒されますね。</p>
    <h2>よくある質問</h2>'''+faq([('猫は本当にそんなに寝るの？','成猫で14〜16時間、子猫やシニアはさらに長く寝ることもあります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const h=Math.max(0,Math.min(24,+$('hours').value||0)), life=Math.max(1,+$('life').value||1);
    const totH=h*365*life, awakeH=(24-h)*365*life;
    $('sub').textContent=`1日${h}時間 × 365日 × ${life}年`;
    $('days').textContent=num(totH/24)+'日'; $('awake').textContent=num(awakeH)+'時間'; $('rate').textContent=Math.round(h/24*100)+'%';
    SHARE=`うちの猫、一生で約${num(totH)}時間（まる${num(totH/24)}日）寝てる計算だった😺（人生の${Math.round(h/24*100)}%！）\\nあなたの子は？👇`;
    show(); anim($('big'),0,totH,900);
  }'''))

SIMS.append(dict(id='food-ryou', cat=PET, emoji='🥣',
  title='ペットの適正フード量シミュレーター｜体重から1日のごはん量｜シミュラボ',
  desc='犬・猫の体重から、1日に必要なカロリーと、ドライフードのおおよその給餌量を計算する無料シミュレーター。',
  ogtitle='ペットの適正フード量｜体重から1日のごはん量', ogdesc='犬・猫の体重から、1日の必要カロリーとフード量を計算。',
  h1='ペットの適正フード量シミュレーター',
  lead='うちの子、ごはんの量は合ってる？体重から、1日に必要なカロリーと、ドライフードのおおよその量を計算します。',
  inputs='''    <h2>🥣 条件</h2>
    <div class="field"><label>種類・状態</label><select id="type"><option value="1.6">成犬（避妊・去勢なし）</option><option value="1.4" selected>成犬（避妊・去勢済み）</option><option value="1.2">成猫（避妊・去勢済み）</option><option value="1.4b">成猫（避妊・去勢なし）</option></select></div>
    <div class="row"><div class="field"><label>体重 <span class="hint">（kg）</span></label><input type="number" id="kg" value="4" min="0.1" step="0.1" inputmode="decimal"></div>
    <div class="field"><label>フードのカロリー <span class="hint">（kcal/100g・袋に記載）</span></label><input type="number" id="kcal" value="350" min="100" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">適正量を計算する</button>''',
  result='''      <div class="label">1日に必要なフード量（目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">g</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1日の必要カロリー</div><div class="v accent" id="der">—</div></div>
      <div class="stat"><div class="k">安静時の必要量(RER)</div><div class="v" id="rer">—</div></div>
      <div class="stat"><div class="k">1回(2回食)</div><div class="v" id="once">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>RER（安静時）＝70×体重^0.75<br>DER（1日必要）＝RER×活動係数<br>フード量＝DER÷フードのカロリー</div>
    <p>あくまで一般的な目安です。年齢・運動量・体質で変わります。体型（あばらが触れるか等）を見ながら、かかりつけの先生とも相談して調整してください。</p>
    <h2>よくある質問</h2>'''+faq([('おやつは？','おやつのぶんは1日のカロリーから差し引いて調整しましょう。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const f=$('type').value, kg=Math.max(0.1,+$('kg').value||0.1), kcal=Math.max(1,+$('kcal').value||1);
    const factor= f==='1.4b'?1.4:parseFloat(f);
    const rer=70*Math.pow(kg,0.75), der=rer*factor, grams=der/kcal*100;
    $('sub').textContent=`${sel('type').text}・体重${kg}kg・フード${kcal}kcal/100g`;
    $('der').textContent=Math.round(der)+'kcal'; $('rer').textContent=Math.round(rer)+'kcal'; $('once').textContent=Math.round(grams/2)+'g';
    SHARE=`うちの子（${kg}kg）の1日の適正フード量、約${Math.round(grams)}g（${Math.round(der)}kcal）だった🥣\\nあなたの子は？👇`;
    show(); anim($('big'),0,grams,900);
  }'''))

SIMS.append(dict(id='tatou', cat=PET, emoji='🐾',
  title='多頭飼い 費用シミュレーター｜何匹で生涯いくら？｜シミュラボ',
  desc='1匹あたりの年間費用と頭数・残りの年数から、多頭飼いにかかる生涯費用の合計を試算する無料シミュレーター。',
  ogtitle='多頭飼い 費用シミュレーター｜何匹で生涯いくら？', ogdesc='1匹の年間費用と頭数から、多頭飼いの生涯費用を試算。',
  h1='多頭飼い 費用シミュレーター',
  lead='2匹、3匹…と増えると、費用はどれくらいになる？1匹あたりの年間費用と頭数から、多頭飼いの生涯費用を試算します。',
  inputs='''    <h2>🐾 条件</h2>
    <div class="row"><div class="field"><label>1匹あたりの年間費用 <span class="hint">（円・フード+医療等）</span></label><input type="number" id="per" value="300000" min="0" inputmode="numeric"></div>
    <div class="field"><label>頭数 <span class="hint">（匹）</span></label><input type="number" id="n" value="3" min="1" max="20" inputmode="numeric"></div></div>
    <div class="field"><label>これからの年数 <span class="hint">（年）</span></label><input type="number" id="years" value="12" min="1" max="30" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">生涯費用を計算する</button>''',
  result='''      <div class="label">多頭飼いの生涯費用（合計）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">年あたり合計</div><div class="v accent" id="yr">—</div></div>
      <div class="stat"><div class="k">月あたり合計</div><div class="v" id="mo">—</div></div>
      <div class="stat"><div class="k">1匹あたり生涯</div><div class="v" id="one">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>生涯費用＝1匹の年間費用×頭数×これからの年数</div>
    <p>頭数が増えると費用はもちろん、お世話の手間や医療リスクも増えます。みんなが幸せに暮らせる頭数か、費用面からも考えてみましょう。</p>
    <h2>よくある質問</h2>'''+faq([('多頭割引は？','フードのまとめ買いなどで多少安くなることも。本ツールは単純な合計の目安です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const per=Math.max(0,+$('per').value||0), n=Math.max(1,+$('n').value||1), y=Math.max(1,+$('years').value||1);
    const yr=per*n, total=yr*y;
    $('sub').textContent=`1匹 年${num(per)}円 × ${n}匹 × ${y}年`;
    $('yr').textContent=yen(yr); $('mo').textContent=yen(yr/12); $('one').textContent=yen(per*y);
    SHARE=`${n}匹の多頭飼い、生涯費用は約${yen(total)}という試算だった🐾\\nみんな幸せに。あなたは？👇`;
    show(); anim($('big'),0,total,900);
  }'''))

SIMS.append(dict(id='pet-taiju', cat=PET, emoji='⚖️',
  title='ペットの肥満度シミュレーター｜うちの子、太りすぎ？｜シミュラボ',
  desc='今の体重と適正体重を入れると、ペットの体重オーバー率（肥満度）を計算して判定する無料シミュレーター。健康管理のチェックに。',
  ogtitle='ペットの肥満度シミュレーター｜うちの子、太りすぎ？', ogdesc='今の体重と適正体重から、ペットの肥満度を計算・判定。',
  h1='ペットの肥満度シミュレーター',
  lead='うちの子、ちょっとぽっちゃり？今の体重と適正体重から、体重オーバーの割合（肥満度）を計算して判定します。',
  inputs='''    <h2>⚖️ 条件</h2>
    <div class="row"><div class="field"><label>今の体重 <span class="hint">（kg）</span></label><input type="number" id="now" value="5" min="0.1" step="0.1" inputmode="decimal"></div>
    <div class="field"><label>適正体重 <span class="hint">（kg・かかりつけの目安）</span></label><input type="number" id="ideal" value="4" min="0.1" step="0.1" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">肥満度を見る</button>''',
  result='''      <div class="label" id="lab">適正体重より</div>
      <div class="big"><span id="big">0</span><span class="unit">%</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">判定</div><div class="v accent" id="judge" style="font-size:16px;">—</div></div>
      <div class="stat"><div class="k">体重の差</div><div class="v" id="diff">—</div></div></div>''',
  article='''    <h2>判定の目安</h2>
    <div class="note">適正体重＋10〜15%で「やや肥満」、＋15〜20%以上で「肥満」とされるのが一般的です（犬猫）。体型（あばらが触れるか・くびれがあるか）と合わせて見ましょう。</div>
    <p>肥満は関節・心臓・糖尿病などのリスクを高めます。気になったら、フード量の見直しや、かかりつけの先生への相談を。</p>
    <h2>よくある質問</h2>'''+faq([('適正体重が分からない','子犬・子猫の頃の体重や、かかりつけの先生の目安が参考になります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const now=Math.max(0.1,+$('now').value||0.1), ideal=Math.max(0.1,+$('ideal').value||0.1);
    const over=(now-ideal)/ideal*100;
    let j= over>=20?'肥満ぎみ':over>=10?'やや肥満':over>=-10?'適正':'やせぎみ';
    $('lab').textContent= over>=0?'適正体重より':'適正体重より（軽い）';
    $('sub').textContent=`今${now}kg・適正${ideal}kg`;
    $('judge').textContent=j; $('diff').textContent=(over>=0?'+':'')+(now-ideal).toFixed(1)+'kg';
    SHARE=`うちの子の肥満度、適正より${over>=0?'+':''}${over.toFixed(0)}%（${j}）だった⚖️\\n健康のためにチェック。あなたの子は？👇`;
    show(); anim($('big'),0,Math.abs(over),900);
  }'''))

SIMS.append(dict(id='pet-gohan-life', cat=PET, emoji='🍖',
  title='ペットが一生で食べるフード量シミュレーター｜総量は何kg？｜シミュラボ',
  desc='1日のフード量と想定寿命から、ペットが一生のうちに食べるフードの総量（kg・袋数）を計算する無料シミュレーター。',
  ogtitle='ペットが一生で食べるフード量｜総量は何kg？', ogdesc='1日のフード量から、一生で食べるフードの総量を計算。',
  h1='ペットが一生で食べるフード量シミュレーター',
  lead='毎日のごはん、一生分にするとどれくらいの量になる？1日のフード量と想定寿命から、生涯で食べるフードの総量を計算します。',
  inputs='''    <h2>🍖 条件</h2>
    <div class="row"><div class="field"><label>1日のフード量 <span class="hint">（g）</span></label><input type="number" id="g" value="80" min="0" inputmode="numeric"></div>
    <div class="field"><label>想定寿命 <span class="hint">（年）</span></label><input type="number" id="life" value="15" min="1" max="30" inputmode="numeric"></div></div>
    <div class="field"><label>フード1袋の容量 <span class="hint">（kg）</span></label><input type="number" id="bag" value="2" min="0.1" step="0.1" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">一生分を見る</button>''',
  result='''      <div class="label">一生で食べるフードの総量</div>
      <div class="big"><span id="big">0</span><span class="unit">kg</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">袋数にすると</div><div class="v accent" id="bags">—</div></div>
      <div class="stat"><div class="k">1年で</div><div class="v" id="yr">—</div></div>
      <div class="stat"><div class="k">うちの子の体重 何匹分</div><div class="v" id="x">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>生涯フード量＝1日のフード量×365×想定寿命</div>
    <p>1日80gでも、15年で約438kg。毎日のごはんが、健やかな体をつくります。年齢や体調に合わせてフードを選んであげましょう。</p>
    <h2>よくある質問</h2>'''+faq([('体重何匹分って？','生涯フード量が、体重4kgのペット何匹分かを表示しています（イメージ用）。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const g=Math.max(0,+$('g').value||0), life=Math.max(1,+$('life').value||1), bag=Math.max(0.1,+$('bag').value||0.1);
    const kg=g*365*life/1000;
    $('sub').textContent=`1日${g}g × 365日 × ${life}年`;
    $('bags').textContent=num(kg/bag)+'袋'; $('yr').textContent=num(g*365/1000)+'kg'; $('x').textContent=num(kg/4)+'匹分';
    SHARE=`うちの子が一生で食べるフード、約${num(kg)}kg（${num(kg/bag)}袋分）だった🍖\\nたくさん食べて長生きしてね。あなたの子は？👇`;
    show(); anim($('big'),0,kg,900);
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
