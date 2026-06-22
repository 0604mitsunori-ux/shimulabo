# -*- coding: utf-8 -*-
"""シミュラボ：音声入力・時短カテゴリ 10本。結果ページにTypelessアフィリCTA入り。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGO = '''<span class="mark">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M9 3h6M10 3v5.2L5.4 16.4A2.4 2.4 0 0 0 7.5 20h9a2.4 2.4 0 0 0 2.1-3.6L14 8.2V3" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M7.7 14.5h8.6" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/>
          <circle cx="10.3" cy="16.7" r="1" fill="#fff"/>
          <circle cx="13.4" cy="17.4" r=".7" fill="#fff"/>
        </svg>
      </span>'''

# Typeless（音声入力AI）への訴求CTA（結果欄に表示）
CTA = '''      <a class="cta-box" href="https://www.typeless.com/?via=44144c" target="_blank" rel="noopener" style="display:block;text-decoration:none;text-align:left;margin-top:20px;background:linear-gradient(135deg,#eef2ff,#f5f3ff);border:1.5px solid #a5b4fc;border-radius:14px;padding:18px;">
        <div style="font-weight:900;color:#4f46e5;font-size:15px;">🎙️ その時短、「音声入力」で本当に実現できます。</div>
        <div style="font-size:13px;color:var(--ink-2);margin-top:6px;line-height:1.7;">話すだけで文章が完成する時代。中でも<strong>今いちばんおすすめなのが「Typeless」</strong>です。AIが「えーと」などの言い淀みも自動で整え、議事録・メール・記事を一気に仕上げます。タイピングに戻れなくなる人が続出。</div>
        <div style="margin-top:12px;display:inline-flex;align-items:center;gap:8px;background:#4f46e5;color:#fff;font-weight:800;font-size:14px;padding:11px 22px;border-radius:999px;">Typeless を無料で試す →</div>
      </a>'''

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
<!-- adsense -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4521532459480990"
     crossorigin="anonymous"></script>
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
''' + CTA + '''
      <div style="text-align:center;margin-top:14px;"><span id="shareCount" class="share-count" style="display:none"></span></div>
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
  $('shareBtn').addEventListener('click', () => window.open('https://twitter.com/intent/tweet?text='+encodeURIComponent(SHARE)+'&url='+encodeURIComponent(location.href)+'&hashtags='+encodeURIComponent('シミュラボ,音声入力'),'_blank','noopener'));
  $('copyBtn').addEventListener('click', async () => { try{ await navigator.clipboard.writeText(SHARE+'\\n'+location.href); $('copyBtn').textContent='コピーしました ✓'; setTimeout(()=>$('copyBtn').textContent='結果をコピー',1600);}catch{alert(SHARE);} });
})();
</script>
<script src="../../assets/result-fx.js"></script>
<script src="../../assets/share-counter.js"></script>
<script>ShareCounter.initSim({ simId:'__ID__', badgeEl:document.getElementById('shareCount'), shareBtnIds:['shareBtn'] });</script>
</body>
</html>
'''

V = '音声入力・時短'
TYPELESS = '<div class="note" style="margin-top:14px;"><strong>結論：今いちばんおすすめの音声入力ツールは「Typeless」</strong><br>音声入力ツールは数あれど、精度・整文（言い淀みの自動カット）・日本語の自然さで頭ひとつ抜けているのがTypelessです。上の試算ぶんの時短を、現実のものにしてくれます。</div>'
SIMS = []
def add(**k): SIMS.append(k)

add(id='input-jitan', cat=V, emoji='🎙️',
  title='音声入力 時短シミュレーター｜タイピングを音声にすると年いくら得？｜シミュラボ',
  desc='1日の文字入力量・タイピング速度・あなたの時給から、音声入力に切り替えた場合の年間の時短時間と削減できる金額を計算する無料シミュレーター。',
  ogtitle='音声入力 時短シミュレーター｜年いくら得する？', ogdesc='タイピングを音声入力にした時の年間の時短と節約額を計算。',
  h1='音声入力 時短シミュレーター',
  lead='文章を「打つ」のをやめて「話す」だけにしたら、年間でどれだけ得する？1日の入力量・タイピング速度・時給から、時短時間と削減できる金額を計算します。',
  inputs='''    <h2>🎙️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>1日の文字入力量 <span class="hint">（文字）</span></label><input type="number" id="chars" value="5000" min="0" inputmode="numeric"></div>
    <div class="field"><label>タイピング速度 <span class="hint">（文字/分）</span></label><input type="number" id="speed" value="70" min="10" inputmode="numeric"></div></div>
    <div class="field"><label>あなたの時給（時間価値） <span class="hint">（円）</span></label><input type="number" id="wage" value="2500" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">年間の節約額を見る</button>''',
  result='''      <div class="label">音声入力で 年間の削減額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1日の時短</div><div class="v accent" id="day">—</div></div>
      <div class="stat"><div class="k">年間の時短時間</div><div class="v" id="hours">—</div></div>
      <div class="stat"><div class="k">10年の削減額</div><div class="v" id="y10">—</div></div></div>''',
  article='''    <h2>音声入力はどれくらい速い？</h2>
    <div class="note"><strong>計算式</strong><br>音声入力は約3倍速（話す約300字/分 ＞ 打つ約80〜120字/分）<br>1日の時短 ＝ 入力量 ÷ 速度 ×（1 − 1/3）／削減額 ＝ 時短時間 × 時給</div>
    <p>人は「打つ」より「話す」ほうが圧倒的に速い。毎日の入力を音声に変えるだけで、年単位では大きな時間とお金が浮きます。その時間を本来やるべき仕事や休息に回せます。</p>'''+TYPELESS+'''
    <h2>よくある質問</h2>'''+faq([('誤変換の修正時間は？','最新のAI音声入力は精度が高く、整文まで自動。修正の手間も大幅に減ります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const c=Math.max(0,+$('chars').value||0),sp=Math.max(1,+$('speed').value||1),w=Math.max(0,+$('wage').value||0);
    const typeMin=c/sp, voiceMin=c/(sp*3), saveDay=typeMin-voiceMin, yearH=saveDay*365/60, money=yearH*w;
    $('sub').textContent=`1日${num(c)}字・${sp}字/分・時給${num(w)}円`;$('day').textContent=num(saveDay)+'分';$('hours').textContent=num(yearH)+'時間';$('y10').textContent=yen(money*10);
    SHARE=`音声入力 時短シミュ、タイピングを音声にすると年間 約${yen(money)}（${num(yearH)}時間）も得する計算でした🎙️`;show();anim($('big'),0,money,900);}''')

add(id='gijiroku-jitan', cat=V, emoji='📝',
  title='議事録 音声入力シミュレーター｜文字起こしで年間いくら削減？｜シミュラボ',
  desc='週の会議数と1回の議事録作成時間・時給から、音声入力（自動文字起こし）で削減できる年間の作業時間と人件費を計算する無料シミュレーター。',
  ogtitle='議事録 音声入力シミュレーター｜年間いくら削減？', ogdesc='音声入力で議事録づくりの作業時間と人件費をどれだけ削減できるか計算。',
  h1='議事録 音声入力シミュレーター',
  lead='会議のたびに発生する議事録づくり。音声入力（自動文字起こし）にすると、年間でどれだけの作業時間と人件費が浮くかを計算します。',
  inputs='''    <h2>📝 条件を入れる</h2>
    <div class="row"><div class="field"><label>週の会議数 <span class="hint">（回）</span></label><input type="number" id="n" value="5" min="0" inputmode="numeric"></div>
    <div class="field"><label>1回の議事録作成時間 <span class="hint">（分）</span></label><input type="number" id="min" value="40" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>時給（作成者の時間価値） <span class="hint">（円）</span></label><input type="number" id="wage" value="3000" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">削減額を見る</button>''',
  result='''      <div class="label">議事録の年間 人件費削減</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">年間の時短</div><div class="v accent" id="hours">—</div></div>
      <div class="stat"><div class="k">1回あたり時短</div><div class="v" id="per">—</div></div>
      <div class="stat"><div class="k">年間の会議数</div><div class="v" id="cnt">—</div></div></div>''',
  article='''    <h2>議事録の自動化効果</h2>
    <div class="note"><strong>計算式</strong><br>音声入力で作成時間は約1/3に短縮<br>年間削減 ＝ 1回の作成時間 × 2/3 × 週の会議数 × 52週 × 時給</div>
    <p>会議を録って話すだけで議事録の下書きが完成すれば、要点整理だけで済みます。組織全体だと削減効果は莫大。会議が多い職場ほど効果絶大です。</p>'''+TYPELESS+'''
    <h2>よくある質問</h2>'''+faq([('精度は大丈夫？','最新のAIは専門用語も学習し高精度。固有名詞だけ直せばOKなレベルです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const n=Math.max(0,+$('n').value||0),mi=Math.max(0,+$('min').value||0),w=Math.max(0,+$('wage').value||0);
    const perSave=mi*2/3, yearH=perSave*n*52/60, money=yearH*w;
    $('sub').textContent=`週${n}回・1回${mi}分・時給${num(w)}円`;$('hours').textContent=num(yearH)+'時間';$('per').textContent=num(perSave)+'分';$('cnt').textContent=num(n*52)+'回';
    SHARE=`議事録 音声入力シミュ、自動文字起こしで年間 約${yen(money)}（${num(yearH)}時間）削減できる計算でした📝`;show();anim($('big'),0,money,900);}''')

add(id='mail-jitan', cat=V, emoji='✉️',
  title='メール作成 音声入力シミュレーター｜メールを話すと年いくら得？｜シミュラボ',
  desc='1日のメール作成数と1通の作成時間・時給から、音声入力でメール作成を時短した場合の年間削減時間と金額を計算する無料シミュレーター。',
  ogtitle='メール作成 音声入力｜年いくら得する？', ogdesc='メール作成を音声入力にした時の年間の時短と節約額を計算。',
  h1='メール作成 音声入力シミュレーター',
  lead='1日に何通も書くメール、話して書いたら？1日のメール数・1通の作成時間から、音声入力で浮く年間の時間とお金を計算します。',
  inputs='''    <h2>✉️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>1日のメール作成数 <span class="hint">（通）</span></label><input type="number" id="n" value="15" min="0" inputmode="numeric"></div>
    <div class="field"><label>1通の作成時間 <span class="hint">（分）</span></label><input type="number" id="min" value="4" min="0" step="0.5" inputmode="decimal"></div></div>
    <div class="field"><label>時給 <span class="hint">（円）</span></label><input type="number" id="wage" value="2500" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">節約額を見る</button>''',
  result='''      <div class="label">メールの年間 削減額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1日の時短</div><div class="v accent" id="day">—</div></div>
      <div class="stat"><div class="k">年間の時短時間</div><div class="v" id="hours">—</div></div>
      <div class="stat"><div class="k">年間のメール数</div><div class="v" id="cnt">—</div></div></div>''',
  article='''    <h2>メールこそ音声入力</h2>
    <div class="note"><strong>計算式</strong><br>音声入力で作成時間は約1/3に<br>年間削減 ＝ 1通の時間 × 2/3 × 1日の通数 × 240営業日 × 時給</div>
    <p>定型的なメールほど、話すだけで一瞬。AIが敬語や体裁も整えてくれるので、推敲の時間も激減します。1日のメールが多い人ほど効果大。</p>'''+TYPELESS+'''
    <h2>よくある質問</h2>'''+faq([('敬語も大丈夫？','AIが自然なビジネス文体に整えてくれます。話し言葉のままになりません。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const n=Math.max(0,+$('n').value||0),mi=Math.max(0,+$('min').value||0),w=Math.max(0,+$('wage').value||0);
    const saveDay=n*mi*2/3, yearH=saveDay*240/60, money=yearH*w;
    $('sub').textContent=`1日${n}通・1通${mi}分・時給${num(w)}円`;$('day').textContent=num(saveDay)+'分';$('hours').textContent=num(yearH)+'時間';$('cnt').textContent=num(n*240)+'通';
    SHARE=`メール作成 音声入力シミュ、年間 約${yen(money)}（${num(yearH)}時間）の節約になる計算でした✉️`;show();anim($('big'),0,money,900);}''')

add(id='blog-shippitsu', cat=V, emoji='✍️',
  title='記事・ブログ執筆 音声入力シミュレーター｜執筆を話すと年いくら？｜シミュラボ',
  desc='月の執筆本数と1本の執筆時間・時間単価から、音声入力で記事・ブログ執筆を時短した場合の年間の削減時間と金額（外注換算）を計算する無料シミュレーター。',
  ogtitle='記事・ブログ執筆 音声入力｜年いくら得？', ogdesc='執筆を音声入力にした時の年間の時短と金額換算を計算。',
  h1='記事・ブログ執筆 音声入力シミュレーター',
  lead='記事やブログの執筆、口述で一気に下書きしたら？月の本数・1本の執筆時間から、音声入力で浮く年間の時間とその価値を計算します。ライター・発信者に。',
  inputs='''    <h2>✍️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>月の執筆本数 <span class="hint">（本）</span></label><input type="number" id="n" value="8" min="0" inputmode="numeric"></div>
    <div class="field"><label>1本の執筆時間 <span class="hint">（分）</span></label><input type="number" id="min" value="120" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>時間単価 <span class="hint">（円・自分の時給 or 外注単価）</span></label><input type="number" id="wage" value="3000" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">年間の効果を見る</button>''',
  result='''      <div class="label">執筆の年間 削減額（価値）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">年間の時短</div><div class="v accent" id="hours">—</div></div>
      <div class="stat"><div class="k">浮いた時間で書ける本数</div><div class="v" id="extra">—</div></div>
      <div class="stat"><div class="k">年間の執筆本数</div><div class="v" id="cnt">—</div></div></div>''',
  article='''    <h2>口述ドラフトの威力</h2>
    <div class="note"><strong>計算式</strong><br>音声で下書き時間は約半分に（構成は頭の中、肉付けを口述）<br>年間削減 ＝ 1本の時間 × 0.5 × 月の本数 × 12 × 時間単価</div>
    <p>「書く」より「話す」ほうが思考が止まりません。骨子だけ決めて一気に口述→AIが整文、の流れで執筆スピードが激変。浮いた時間でさらに本数を増やせば、発信量＝チャンスも倍増します。</p>'''+TYPELESS+'''
    <h2>よくある質問</h2>'''+faq([('文章が話し言葉っぽくならない？','AIが書き言葉に整えてくれるので、自然な記事になります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const n=Math.max(0,+$('n').value||0),mi=Math.max(0,+$('min').value||0),w=Math.max(0,+$('wage').value||0);
    const saveYearMin=mi*0.5*n*12, yearH=saveYearMin/60, money=yearH*w, extra=mi>0?saveYearMin/(mi*0.5):0;
    $('sub').textContent=`月${n}本・1本${mi}分・単価${num(w)}円`;$('hours').textContent=num(yearH)+'時間';$('extra').textContent=num(extra)+'本';$('cnt').textContent=num(n*12)+'本';
    SHARE=`記事執筆 音声入力シミュ、年間 約${yen(money)}（${num(yearH)}時間）ぶんの効率化になる計算でした✍️`;show();anim($('big'),0,money,900);}''')

add(id='moji-okoshi', cat=V, emoji='🔊',
  title='文字起こし外注費 削減シミュレーター｜自動化で年いくら浮く？｜シミュラボ',
  desc='月の録音時間と文字起こしの外注単価から、AI音声認識（自動文字起こし）に切り替えて削減できる年間の外注費を計算する無料シミュレーター。',
  ogtitle='文字起こし外注費 削減｜自動化で年いくら浮く？', ogdesc='外注の文字起こしをAI自動化した時の年間削減額を計算。',
  h1='文字起こし外注費 削減シミュレーター',
  lead='インタビューや会議の文字起こし、外注すると分単位で費用がかかります。AI自動文字起こしに切り替えると、年間でいくら浮くかを計算します。',
  inputs='''    <h2>🔊 条件を入れる</h2>
    <div class="row"><div class="field"><label>月の録音時間 <span class="hint">（分）</span></label><input type="number" id="min" value="180" min="0" inputmode="numeric"></div>
    <div class="field"><label>外注単価 <span class="hint">（円/分・相場100〜200）</span></label><input type="number" id="tanka" value="150" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>AIツールの月額 <span class="hint">（円・差引用）</span></label><input type="number" id="tool" value="2000" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">削減額を見る</button>''',
  result='''      <div class="label">文字起こしの年間 削減額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">外注なら年間</div><div class="v" id="gai">—</div></div>
      <div class="stat"><div class="k">AIツール年額</div><div class="v" id="toolv">—</div></div>
      <div class="stat"><div class="k">削減率</div><div class="v accent" id="rate">—</div></div></div>''',
  article='''    <h2>外注 vs 自動文字起こし</h2>
    <div class="note"><strong>計算式</strong><br>外注費（年）＝ 録音分数 × 外注単価 × 12<br>削減額 ＝ 外注費（年）− AIツールの年額</div>
    <p>外注の文字起こしは「録音1分＝100〜200円」が相場。AI自動文字起こしなら月額数千円で使い放題のことも多く、量が多いほど圧倒的にお得。スピードも段違いです。</p>'''+TYPELESS+'''
    <h2>よくある質問</h2>'''+faq([('精度は外注に劣らない？','近年のAIは高精度。話者分離や用語学習に対応するツールもあります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const mi=Math.max(0,+$('min').value||0),t=Math.max(0,+$('tanka').value||0),tool=Math.max(0,+$('tool').value||0);
    const gai=mi*t*12, toolY=tool*12, save=Math.max(0,gai-toolY), rate=gai>0?save/gai*100:0;
    $('sub').textContent=`月${num(mi)}分・外注${num(t)}円/分`;$('gai').textContent=yen(gai);$('toolv').textContent=yen(toolY);$('rate').textContent=Math.round(rate)+'%';
    SHARE=`文字起こし外注費 削減シミュ、AI自動化で年間 約${yen(save)}（削減率${Math.round(rate)}%）浮く計算でした🔊`;show();anim($('big'),0,save,900);}''')

add(id='shorui-jitan', cat=V, emoji='📄',
  title='書類・レポート作成 音声入力シミュレーター｜年間いくら時短？｜シミュラボ',
  desc='週の書類・レポート作成時間と時給から、音声入力で文書作成を時短した場合の年間の削減時間と金額を計算する無料シミュレーター。',
  ogtitle='書類・レポート 音声入力｜年間いくら時短？', ogdesc='文書作成を音声入力にした時の年間の時短と金額を計算。',
  h1='書類・レポート作成 音声入力シミュレーター',
  lead='報告書・日報・提案書…文書作成に取られる時間、音声入力で短くできます。週の作成時間と時給から、年間の削減効果を計算します。',
  inputs='''    <h2>📄 条件を入れる</h2>
    <div class="row"><div class="field"><label>週の文書作成時間 <span class="hint">（時間）</span></label><input type="number" id="hours" value="5" min="0" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>時給 <span class="hint">（円）</span></label><input type="number" id="wage" value="2800" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">削減額を見る</button>''',
  result='''      <div class="label">文書作成の年間 削減額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">年間の時短</div><div class="v accent" id="hh">—</div></div>
      <div class="stat"><div class="k">1週間の時短</div><div class="v" id="wk">—</div></div>
      <div class="stat"><div class="k">10年で</div><div class="v" id="y10">—</div></div></div>''',
  article='''    <h2>文書作成の時短</h2>
    <div class="note"><strong>計算式</strong><br>音声入力で作成時間は約40%短縮（思考を含むため控えめに見積もり）<br>年間削減 ＝ 週の作成時間 × 40% × 52週 × 時給</div>
    <p>文章を「考えながら打つ」のは脳に負荷大。話しながらだとアイデアが流れるように出て、作成が速くなります。AIが整形・要約もしてくれるので、清書の手間も削減。</p>'''+TYPELESS+'''
    <h2>よくある質問</h2>'''+faq([('表や数字が多い書類は？','文章部分の作成が速くなります。テンプレと併用が効果的です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const h=Math.max(0,+$('hours').value||0),w=Math.max(0,+$('wage').value||0);
    const wk=h*0.4, yearH=wk*52, money=yearH*w;
    $('sub').textContent=`週${h}時間・時給${num(w)}円`;$('hh').textContent=num(yearH)+'時間';$('wk').textContent=wk.toFixed(1)+'時間';$('y10').textContent=yen(money*10);
    SHARE=`書類作成 音声入力シミュ、年間 約${yen(money)}（${num(yearH)}時間）の時短になる計算でした📄`;show();anim($('big'),0,money,900);}''')

add(id='chat-jitan', cat=V, emoji='💬',
  title='チャット・SNS 音声入力シミュレーター｜返信を話すと年いくら？｜シミュラボ',
  desc='1日のチャット・SNS入力時間と時間価値から、音声入力に切り替えた場合の年間の時短時間と価値を計算する無料シミュレーター。',
  ogtitle='チャット・SNS 音声入力｜年いくら時短？', ogdesc='チャット返信を音声入力にした時の年間の時短を計算。',
  h1='チャット・SNS 音声入力シミュレーター',
  lead='Slackやチャット、SNSの返信、地味に時間を取られていませんか。1日の入力時間から、音声入力で浮く年間の時間とその価値を計算します。',
  inputs='''    <h2>💬 条件を入れる</h2>
    <div class="row"><div class="field"><label>1日のチャット入力時間 <span class="hint">（分）</span></label><input type="number" id="min" value="40" min="0" inputmode="numeric"></div>
    <div class="field"><label>時間価値 <span class="hint">（円/時）</span></label><input type="number" id="wage" value="2000" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">年間の効果を見る</button>''',
  result='''      <div class="label">チャットの年間 時短価値</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1日の時短</div><div class="v accent" id="day">—</div></div>
      <div class="stat"><div class="k">年間の時短時間</div><div class="v" id="hours">—</div></div>
      <div class="stat"><div class="k">映画(2h)にすると</div><div class="v" id="movie">—</div></div></div>''',
  article='''    <h2>スキマ入力こそ音声</h2>
    <div class="note"><strong>計算式</strong><br>音声入力で入力時間は約半分に<br>年間 ＝ 1日の入力時間 × 50% × 365 × 時間価値</div>
    <p>短文の返信は、フリック入力でも意外と時間がかかるもの。音声ならスマホに話すだけ。塵も積もれば、1年でまとまった時間に。スキマ時間を取り戻せます。</p>'''+TYPELESS+'''
    <h2>よくある質問</h2>'''+faq([('外で使いづらい？','イヤホンマイクや小声入力に対応するツールも。自宅・移動中だけでも効果的です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const mi=Math.max(0,+$('min').value||0),w=Math.max(0,+$('wage').value||0);
    const saveDay=mi*0.5, yearH=saveDay*365/60, money=yearH*w;
    $('sub').textContent=`1日${mi}分・時間価値${num(w)}円`;$('day').textContent=num(saveDay)+'分';$('hours').textContent=num(yearH)+'時間';$('movie').textContent=num(yearH/2)+'本';
    SHARE=`チャット 音声入力シミュ、年間 約${yen(money)}（${num(yearH)}時間）の時短になる計算でした💬`;show();anim($('big'),0,money,900);}''')

add(id='memo-jitan', cat=V, emoji='🗒️',
  title='メモ・記録 音声入力シミュレーター｜記録を話すと年いくら時短？｜シミュラボ',
  desc='1日のメモ・記録・日記などの入力時間から、音声入力に切り替えた場合の年間の時短時間と価値を計算する無料シミュレーター。',
  ogtitle='メモ・記録 音声入力｜年いくら時短？', ogdesc='メモや記録を音声入力にした時の年間の時短を計算。',
  h1='メモ・記録 音声入力シミュレーター',
  lead='アイデアメモ、日報、日記、読書記録…日々の「書き留める」作業も音声で。1日の記録時間から、年間で浮く時間とその価値を計算します。',
  inputs='''    <h2>🗒️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>1日のメモ・記録時間 <span class="hint">（分）</span></label><input type="number" id="min" value="25" min="0" inputmode="numeric"></div>
    <div class="field"><label>時間価値 <span class="hint">（円/時）</span></label><input type="number" id="wage" value="2000" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">年間の効果を見る</button>''',
  result='''      <div class="label">メモ・記録の年間 時短価値</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1日の時短</div><div class="v accent" id="day">—</div></div>
      <div class="stat"><div class="k">年間の時短時間</div><div class="v" id="hours">—</div></div>
      <div class="stat"><div class="k">10年の価値</div><div class="v" id="y10">—</div></div></div>''',
  article='''    <h2>思いついた瞬間を逃さない</h2>
    <div class="note"><strong>計算式</strong><br>音声入力で記録時間は約1/3に<br>年間 ＝ 1日の記録時間 × 2/3 × 365 × 時間価値</div>
    <p>アイデアは書こうとした瞬間に消えるもの。話すだけなら一瞬で残せます。時短だけでなく「記録する習慣」自体が続きやすくなるのも音声入力のメリットです。</p>'''+TYPELESS+'''
    <h2>よくある質問</h2>'''+faq([('箇条書きもできる？','「箇条書きで」と話せば整形してくれるツールもあります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const mi=Math.max(0,+$('min').value||0),w=Math.max(0,+$('wage').value||0);
    const saveDay=mi*2/3, yearH=saveDay*365/60, money=yearH*w;
    $('sub').textContent=`1日${mi}分・時間価値${num(w)}円`;$('day').textContent=num(saveDay)+'分';$('hours').textContent=num(yearH)+'時間';$('y10').textContent=yen(money*10);
    SHARE=`メモ・記録 音声入力シミュ、年間 約${yen(money)}（${num(yearH)}時間）の時短になる計算でした🗒️`;show();anim($('big'),0,money,900);}''')

add(id='shogai-typing', cat=V, emoji='⌨️',
  title='生涯タイピング時間シミュレーター｜音声入力で人生何日取り戻せる？｜シミュラボ',
  desc='1日のタイピング時間とこれからの年数から、生涯でキーボードを打つ総時間と、音声入力で取り戻せる人生の時間を計算するエンタメシミュレーター。',
  ogtitle='生涯タイピング時間｜音声で何日取り戻せる？', ogdesc='生涯のタイピング時間と音声入力で取り戻せる時間を計算。',
  h1='生涯タイピング時間シミュレーター',
  lead='あなたが一生でキーボードを打つ時間は何日分？1日のタイピング時間から生涯の総時間を出し、音声入力に切り替えたら人生の何日を取り戻せるかを計算します。',
  inputs='''    <h2>⌨️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>1日のタイピング時間 <span class="hint">（時間）</span></label><input type="number" id="h" value="4" min="0" max="16" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>これからの年数 <span class="hint">（年）</span></label><input type="number" id="years" value="40" min="1" max="70" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">取り戻せる時間を見る</button>''',
  result='''      <div class="label">音声入力で取り戻せる時間</div>
      <div class="big"><span id="big">0</span><span class="unit">日分</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">生涯のタイピング</div><div class="v" id="total">—</div></div>
      <div class="stat"><div class="k">取り戻せる時間</div><div class="v accent" id="back">—</div></div>
      <div class="stat"><div class="k">1日あたり</div><div class="v" id="day">—</div></div></div>''',
  article='''    <h2>人生の時間を取り戻す</h2>
    <div class="note"><strong>計算式</strong><br>生涯のタイピング時間 ＝ 1日の時間 × 365 × 年数<br>取り戻せる時間 ＝ 生涯のタイピング × 2/3（音声で約3倍速）</div>
    <p>毎日のキーボード入力は、積み重ねると人生の何日分にもなります。その3分の2を音声入力で取り戻せたら——その時間で何ができるでしょう。時間は何より貴重な資産です。</p>'''+TYPELESS+'''
    <h2>よくある質問</h2>'''+faq([('全部音声にできる？','コードや細かい編集は手入力が向きますが、文章の大半は音声化できます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const h=Math.max(0,+$('h').value||0),y=Math.max(1,+$('years').value||1);
    const totalH=h*365*y, backH=totalH*2/3, backDays=backH/24;
    $('sub').textContent=`1日${h}時間 × ${y}年`;$('total').textContent=num(totalH)+'時間';$('back').textContent=num(backH)+'時間';$('day').textContent=num(h*2/3*60)+'分';
    SHARE=`生涯タイピング時間シミュ、音声入力に変えると人生で約${num(backDays)}日分も取り戻せる計算でした⌨️`;show();anim($('big'),0,backDays,900);}''')

add(id='kenshouen', cat=V, emoji='🩹',
  title='タイピングの手の負担シミュレーター｜音声入力で負担はどれだけ減る？｜シミュラボ',
  desc='1日のタイピング時間から、年間の推定打鍵数と手・指への負担を可視化し、音声入力に切り替えた場合の負担軽減を計算する無料シミュレーター。',
  ogtitle='タイピングの手の負担｜音声入力でどれだけ減る？', ogdesc='年間の打鍵数と手の負担を、音声入力で軽減する効果を計算。',
  h1='タイピングの手の負担シミュレーター',
  lead='毎日のタイピング、手や指への負担は相当なもの。1日のタイピング時間から年間の打鍵数を推定し、音声入力に置き換えると負担がどれだけ減るかを可視化します。',
  inputs='''    <h2>🩹 条件を入れる</h2>
    <div class="row"><div class="field"><label>1日のタイピング時間 <span class="hint">（時間）</span></label><input type="number" id="h" value="5" min="0" max="16" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>音声入力に置き換える割合 <span class="hint">（％）</span></label><input type="number" id="rate" value="60" min="0" max="100" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">負担軽減を見る</button>''',
  result='''      <div class="label">年間で減らせる打鍵数</div>
      <div class="big"><span id="big">0</span><span class="unit">回</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">年間の打鍵数</div><div class="v" id="total">—</div></div>
      <div class="stat"><div class="k">手を休められる時間(年)</div><div class="v accent" id="rest">—</div></div>
      <div class="stat"><div class="k">指の移動距離(年)</div><div class="v" id="dist">—</div></div></div>''',
  article='''    <h2>手の負担を数字で見る</h2>
    <div class="note"><strong>目安</strong><br>タイピングは1分あたり約250打鍵。1日5時間で約7.5万打鍵/日。<br>音声入力に置き換えた割合ぶん、打鍵と指の移動が減ります（1打鍵≒指2cm移動で概算）。</div>
    <p>長時間のタイピングは腱鞘炎・肩こり・眼精疲労の原因にも。音声入力で打鍵を減らせば、手への負担を大きく軽減できます。健康はお金には代えられない資産。体をいたわる選択を。</p>'''+TYPELESS+'''
    <h2>よくある質問</h2>'''+faq([('医学的な効果は？','負担軽減の目安です。痛みがある場合は医療機関にご相談ください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const h=Math.max(0,+$('h').value||0),r=Math.max(0,Math.min(100,+$('rate').value||0))/100;
    const perDay=h*60*250, yearTotal=perDay*240, reduced=yearTotal*r;
    const restH=h*r*240, distKm=reduced*0.02/1000;
    $('sub').textContent=`1日${h}時間・音声化${Math.round(r*100)}%`;$('total').textContent=num(yearTotal)+'回';$('rest').textContent=num(restH)+'時間';$('dist').textContent=num(distKm)+'km';
    SHARE=`タイピングの手の負担シミュ、音声入力で年間 約${num(reduced)}回の打鍵を減らせる計算でした🩹 手をいたわろう。`;show();anim($('big'),0,reduced,900);}''')

def render():
    for s in SIMS:
        d=os.path.join(ROOT,'sims',s['id']); os.makedirs(d,exist_ok=True)
        html=(TPL.replace('__TITLE__',s['title']).replace('__DESC__',s['desc'])
              .replace('__OGTITLE__',s['ogtitle']).replace('__OGDESC__',s['ogdesc'])
              .replace('__CAT__',s['cat']).replace('__H1__',s['h1']).replace('__LEAD__',s['lead'])
              .replace('__INPUTS__',s['inputs']).replace('__RESULT__',s['result'])
              .replace('__ARTICLE__',s['article']).replace('__JS__',s['js']).replace('__ID__',s['id']))
        with open(os.path.join(d,'index.html'),'w',encoding='utf-8') as f: f.write(html)
        print('created sims/'+s['id'])

if __name__=='__main__':
    render()
    print(f'voice done. {len(SIMS)} sims.')
