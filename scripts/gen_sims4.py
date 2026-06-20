# -*- coding: utf-8 -*-
"""シミュラボ：恋愛・婚活カテゴリ 新作5本（学生向け含む・すべて健全/エンタメ）。"""
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
  const num = (n) => Math.round(n).toLocaleString('ja-JP');
  const sel = (id) => { const e=$(id); return e.options[e.selectedIndex]; };
  let SHARE = '';
  function anim(el, from, to, dur, dec){ const t0=performance.now(); (function s(n){const p=Math.min(1,(n-t0)/dur);const e=1-Math.pow(1-p,3);const v=from+(to-from)*e;el.textContent=(dec!=null?v.toFixed(dec):Math.round(v).toLocaleString('ja-JP'));if(p<1)requestAnimationFrame(s);})(performance.now()); }
  function show(){ $('resultPanel').style.display=''; $('resultPanel').scrollIntoView({behavior:'smooth',block:'start'}); }
__JS__
  $('calcBtn').addEventListener('click', calc);
  $('shareBtn').addEventListener('click', () => window.open('https://twitter.com/intent/tweet?text='+encodeURIComponent(SHARE)+'&url='+encodeURIComponent(location.href)+'&hashtags='+encodeURIComponent('シミュラボ,恋愛'),'_blank','noopener'));
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

CAT='恋愛・婚活'
SIMS=[]

# 1. 告白成功率
SIMS.append(dict(id='kokuhaku', cat=CAT, emoji='💌',
  title='告白成功率シミュレーター｜あなたの告白、成功する確率は？｜シミュラボ',
  desc='相手との関係・連絡頻度・脈ありサインから、告白が成功する確率の目安を診断。背中を押してくれる無料の恋愛シミュレーターです。',
  ogtitle='告白成功率シミュレーター｜あなたの告白、成功する確率は？', ogdesc='相手との関係や脈ありサインから、告白の成功率を診断。',
  h1='告白成功率シミュレーター',
  lead='告白しようか迷っているあなたへ。相手との関係や脈ありサインから、成功率の目安を診断します。最後に背中を押すアドバイスつき。',
  inputs='''    <h2>💌 今の状況を選んでください</h2>
    <div class="field"><label>相手との関係は？</label><select id="rel"><option value="30">よく話す友達</option><option value="18" selected>クラス・職場が同じ</option><option value="10">たまに話す</option><option value="3">あいさつ程度</option></select></div>
    <div class="field"><label>連絡（LINEなど）の頻度は？</label><select id="freq"><option value="25">毎日のように</option><option value="15" selected>数日に1回</option><option value="6">たまに</option><option value="0">ほとんどない</option></select></div>
    <div class="field"><label>脈ありサイン（目が合う・よく笑う・相手から話しかける等）は？</label><select id="sign"><option value="25">3つ以上ある</option><option value="12" selected>1〜2つある</option><option value="0">よく分からない</option></select></div>
    <div class="field"><label>告白のタイミングは？</label><select id="time"><option value="10">二人きりで落ち着いた時</option><option value="3" selected>普通</option><option value="-5">ちょっと微妙かも</option></select></div>
    <button class="btn btn-primary" id="calcBtn">成功率を診断する</button>''',
  result='''      <div class="label">あなたの告白 成功率は</div>
      <div class="big"><span id="big">0</span><span class="unit">%</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:18px;">—</div>''',
  article='''    <h2>この診断について</h2>
    <p>相手との距離感や脈ありサインから、告白成功率の目安を出すエンタメ診断です。数字はあくまで参考。大事なのは、勇気を出して気持ちを伝えることです。</p>
    <div class="note">💡 成功率を上げるコツ：①まずは会話・連絡を増やす ②相手の好きなものを知る ③落ち着いた二人の時間を選ぶ。</div>
    <h2>よくある質問</h2>''' + faq([('当たりますか？','エンタメ診断です。低くても諦める理由にはなりません。関係を育てればきっと変わります。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    let s=10; for(const id of ['rel','freq','sign','time']) s+=(+$(id).value||0);
    s=Math.max(3,Math.min(95,s));
    let a; if(s>=70)a='かなり脈あり！自信を持って、二人の時間に素直な気持ちを伝えてみよう💪';
    else if(s>=45)a='チャンスは十分。もう少し会話や連絡を重ねてから告白すると◎';
    else if(s>=25)a='まずは仲良くなるところから。共通の話題を増やして距離を縮めよう。';
    else a='今は土台づくりの時期。焦らず、まずは「話せる関係」を目指そう。低い数字でも、これからいくらでも上げられる！';
    $('sub').textContent=`関係:${sel('rel').text}／連絡:${sel('freq').text}`;
    $('adv').textContent='💌 '+a;
    SHARE=`告白成功率シミュ、私は${s}%でした💌\\n${s>=45?'いける気がしてきた…！':'まずは距離を縮めるぞ'}\\nあなたは？👇`;
    show(); anim($('big'),0,s,900);
  }'''))

# 2. 両思い度診断
SIMS.append(dict(id='ryomoi', cat=CAT, emoji='💞',
  title='両思い度診断｜あの人とあなた、両思いの可能性は？｜シミュラボ',
  desc='相手の言動についての5つの質問から、両思いの可能性を診断する無料の恋愛シミュレーター。学生にもおすすめのエンタメ診断です。',
  ogtitle='両思い度診断｜あの人と両思いの可能性は？', ogdesc='相手の言動から、両思いの可能性を5つの質問で診断。',
  h1='両思い度診断',
  lead='「もしかして両思い…？」その予感、確かめてみましょう。相手の言動についての5つの質問から、両思い度を診断します。',
  inputs='''    <h2>💞 あの人について教えて</h2>
    <div class="field"><label>① 目が合うと？</label><select id="q1"><option value="20">よく目が合う・そらさない</option><option value="10" selected>たまに合う</option><option value="0">あまり合わない</option></select></div>
    <div class="field"><label>② 相手から話しかけてくる？</label><select id="q2"><option value="20">よくある</option><option value="10" selected>たまに</option><option value="0">自分からが多い</option></select></div>
    <div class="field"><label>③ LINE・連絡の返信は？</label><select id="q3"><option value="20">早い・会話が続く</option><option value="10" selected>普通</option><option value="0">そっけない/遅い</option></select></div>
    <div class="field"><label>④ 二人の時、笑顔が多い？</label><select id="q4"><option value="20">すごく楽しそう</option><option value="10" selected>まあまあ</option><option value="0">分からない</option></select></div>
    <div class="field"><label>⑤ あなたの変化に気づく？</label><select id="q5"><option value="20">髪型などよく気づく</option><option value="8" selected>たまに</option><option value="0">気づかない</option></select></div>
    <button class="btn btn-primary" id="calcBtn">両思い度を診断する</button>''',
  result='''      <div class="label">あの人との両思い度は</div>
      <div class="big"><span id="big">0</span><span class="unit">%</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:18px;">—</div>''',
  article='''    <h2>この診断について</h2>
    <p>相手の言動から両思いの可能性を占うエンタメ診断です。当たっても外れても、最後は勇気を出して関わってみることが大切です。</p>
    <h2>よくある質問</h2>''' + faq([('信じていい？','お楽しみ診断です。脈ありサインは人それぞれなので、参考程度に。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    let s=0; for(const id of ['q1','q2','q3','q4','q5']) s+=(+$(id).value||0); s=Math.min(100,s);
    let a; if(s>=80)a='かなり脈あり！両思いの可能性大。あと一歩、勇気を出してみて💕';
    else if(s>=55)a='いい感じ。相手もあなたを意識しているかも。会話を増やそう！';
    else if(s>=30)a='これからのアプローチしだい。まずは仲良くなることから。';
    else a='今はまだこれから。焦らず、自然に関わる時間を増やしてみよう。';
    $('sub').textContent='相手の言動から推定';
    $('adv').textContent='💞 '+a;
    SHARE=`両思い度診断、あの人との両思い度は${s}%でした💞\\nあなたも気になる人で試してみて👇`;
    show(); anim($('big'),0,s,900);
  }'''))

# 3. 名前で相性占い
SIMS.append(dict(id='aisho-name', cat=CAT, emoji='💘',
  title='名前で相性占い｜二人の名前で相性をチェック｜シミュラボ',
  desc='あなたと気になる人の名前を入れるだけで、二人の相性を占う無料シミュレーター。学校でもSNSでも盛り上がる定番の相性占いです。',
  ogtitle='名前で相性占い｜二人の名前で相性をチェック', ogdesc='二人の名前を入れるだけで相性を占う、定番の相性占い。',
  h1='名前で相性占い',
  lead='あなたと、気になるあの人。名前を入れるだけで、二人の相性を占います。友達同士でも、推しとでも、気軽にどうぞ。',
  inputs='''    <h2>💘 二人の名前を入れて</h2>
    <div class="row"><div class="field"><label>あなたの名前 <span class="hint">（ニックネームでOK）</span></label><input type="text" id="a" value="" placeholder="例：はると" maxlength="20"></div>
    <div class="field"><label>相手の名前 <span class="hint">（ニックネームでOK）</span></label><input type="text" id="b" value="" placeholder="例：ひなた" maxlength="20"></div></div>
    <button class="btn btn-primary" id="calcBtn">相性を占う</button>''',
  result='''      <div class="label" id="lab">二人の相性は</div>
      <div class="big"><span id="big">0</span><span class="unit">%</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:18px;">—</div>''',
  article='''    <h2>この占いについて</h2>
    <p>二人の名前から相性を占う、昔ながらの相性占いです。同じ名前の組み合わせなら何度占っても同じ結果になります。お遊びとしてお楽しみください。</p>
    <h2>よくある質問</h2>''' + faq([('本名じゃないとダメ？','いいえ。ニックネームでもOK。同じ入力なら結果は変わりません。'),('データは送信されますか？','いいえ。占いはすべてブラウザ内で完結し、名前は外部に送信されません。')]),
  js='''  function calc(){
    const a=($('a').value||'').trim(), b=($('b').value||'').trim();
    if(!a||!b){ $('sub').textContent='⚠️ 二人の名前を入れてね'; $('adv').textContent=''; $('big').textContent='0'; show(); return; }
    const s=a+'♥'+b; let h=0; for(let i=0;i<s.length;i++){ h=(h*131+s.codePointAt(i))%1000003; }
    const score=30+h%71;
    let c; if(score>=85)c='最高の相性！運命級かも。大切にしてね💖';
    else if(score>=65)c='とても good な相性。一緒にいて楽しい二人になれそう。';
    else if(score>=45)c='悪くない相性。お互いを知るほど深まるタイプ。';
    else c='今は伸びしろの相性。違いを楽しめると◎';
    $('lab').textContent=`${a} ＆ ${b} の相性は`;
    $('sub').textContent='二人の名前から占いました';
    $('adv').textContent='💘 '+c;
    SHARE=`「${a}」と「${b}」の名前相性は ${score}% でした💘\\nあなたも気になる人と占ってみて👇`;
    show(); anim($('big'),0,score,900);
  }'''))

# 4. 同じクラスになる確率（中学生向け）
SIMS.append(dict(id='same-class', cat=CAT, emoji='🏫',
  title='好きな人と同じクラスになる確率｜中学生・高校生向け｜シミュラボ',
  desc='クラスの数と在学年数から、好きな人と同じクラスになる確率を計算。中学生・高校生向けの、ドキドキする確率シミュレーターです。',
  ogtitle='好きな人と同じクラスになる確率｜中学生・高校生向け', ogdesc='クラス数から、好きな人と同じクラスになる確率を計算。',
  h1='好きな人と同じクラスになる確率',
  lead='新学期、好きな人や友達と同じクラスになれるかドキドキ…。クラスの数から、その確率を計算してみましょう。',
  inputs='''    <h2>🏫 学校のことを入れて</h2>
    <div class="row"><div class="field"><label>学年のクラス数 <span class="hint">（組の数）</span></label><input type="number" id="c" value="4" min="1" max="30" inputmode="numeric"></div>
    <div class="field"><label>残りの在学年数 <span class="hint">（年・中学なら最大3）</span></label><input type="number" id="n" value="3" min="1" max="6" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">確率を計算する</button>''',
  result='''      <div class="label">在学中に一度でも同じクラスになる確率</div>
      <div class="big"><span id="big">0</span><span class="unit">%</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline">
        <div class="stat"><div class="k">毎年の確率</div><div class="v accent" id="one">—</div></div>
        <div class="stat"><div class="k">ずっと同じクラス</div><div class="v" id="all">—</div></div>
        <div class="stat"><div class="k">一度も同じにならない</div><div class="v" id="never">—</div></div>
      </div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>毎年の確率 ＝ 1 ÷ クラス数<br>一度でも同じ ＝ 1 −（1 − 1/クラス数）の(在学年数)乗</div>
    <p>クラスがランダムに分けられると仮定した計算です。クラス数が少ないほど、年数が多いほど、同じクラスになる確率は上がります。新学期のドキドキの参考にどうぞ。</p>
    <h2>よくある質問</h2>''' + faq([('本当にこの確率？','クラス分けが完全にランダムと仮定した計算です。実際は成績や人数調整などもあるため、あくまで目安です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const c=Math.max(1,+$('c').value||1), n=Math.max(1,+$('n').value||1);
    const one=1/c, all=Math.pow(1/c,n), atLeast=1-Math.pow(1-1/c,n), never=Math.pow(1-1/c,n);
    $('sub').textContent=`${c}クラス・残り${n}年で計算`;
    $('one').textContent=(one*100).toFixed(0)+'%'; $('all').textContent=(all*100).toFixed(1)+'%'; $('never').textContent=(never*100).toFixed(0)+'%';
    SHARE=`好きな人と同じクラスになる確率、${c}クラスだと在学中に約${(atLeast*100).toFixed(0)}%だった🏫\\n新学期、ドキドキ…！\\nあなたの学校は？👇`;
    show(); anim($('big'),0,atLeast*100,900);
  }'''))

# 5. モテ期はいつ来る？
SIMS.append(dict(id='moteki', cat=CAT, emoji='🌟',
  title='モテ期はいつ来る？診断｜次のモテ期を占う｜シミュラボ',
  desc='年齢と最近の調子から、次の「モテ期」がいつ来るかを占う無料の恋愛診断シミュレーター。学生から大人まで楽しめます。',
  ogtitle='モテ期はいつ来る？診断｜次のモテ期を占う', ogdesc='年齢と調子から、次のモテ期がいつ来るかを占う恋愛診断。',
  h1='モテ期はいつ来る？診断',
  lead='人生に3回あると言われる「モテ期」。あなたの次のモテ期がいつ来るのか、占ってみましょう。',
  inputs='''    <h2>🌟 あなたのことを教えて</h2>
    <div class="row"><div class="field"><label>今の年齢 <span class="hint">（歳）</span></label><input type="number" id="age" value="20" min="10" max="90" inputmode="numeric"></div>
    <div class="field"><label>最近の恋愛運は？</label><select id="luck"><option value="good">なんだか好調</option><option value="normal" selected>ふつう</option><option value="bad">ちょっと低調</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">モテ期を占う</button>''',
  result='''      <div class="label">次のモテ期まで、あと</div>
      <div class="big"><span id="big">0</span><span class="unit">年</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline">
        <div class="stat"><div class="k">次のモテ期は</div><div class="v accent" id="at">—</div></div>
        <div class="stat"><div class="k">モテ期の強さ</div><div class="v" id="pow">—</div></div>
        <div class="stat"><div class="k">タイプ</div><div class="v" id="type" style="font-size:15px;">—</div></div>
      </div>''',
  article='''    <h2>この診断について</h2>
    <p>「モテ期は人生に3回」という言い伝えをもとにした、占い・エンタメ診断です。結果は気軽に楽しんでください。モテ期は、自分磨きと前向きさで引き寄せられるとも言われます。</p>
    <h2>よくある質問</h2>''' + faq([('本当に当たる？','占い・エンタメです。当たらなくても、笑って前向きに過ごすのが一番のモテ期の作り方かも。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const age=Math.max(10,+$('age').value||10), luck=$('luck').value;
    const ss='m'+age+luck; let h=0; for(let i=0;i<ss.length;i++) h=(h*131+ss.codePointAt(i))%99991;
    let yrs=1+(h%6); if(luck==='good')yrs=Math.max(1,yrs-2); if(luck==='bad')yrs=yrs+2;
    const at=age+yrs; const pow=['★★★☆☆','★★★★☆','★★★★★'][h%3];
    const types=['出会い運上昇型','内面が輝く型','まわりが放っておかない型','急にモテだす型'];
    const t=types[h%types.length];
    $('sub').textContent=`${age}歳・恋愛運：${sel('luck').text}`;
    $('at').textContent=at+'歳ごろ'; $('pow').textContent=pow; $('type').textContent=t;
    SHARE=`モテ期診断、私の次のモテ期は${at}歳ごろ（あと${yrs}年）でした🌟 タイプは「${t}」\\nあなたのモテ期はいつ？👇`;
    show(); anim($('big'),0,yrs,900);
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
