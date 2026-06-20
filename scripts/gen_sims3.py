# -*- coding: utf-8 -*-
"""シミュラボ：婚活シリーズ3本を生成（やさしい設計・点数で値踏みしない）。"""
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
  $('shareBtn').addEventListener('click', () => window.open('https://twitter.com/intent/tweet?text='+encodeURIComponent(SHARE)+'&url='+encodeURIComponent(location.href)+'&hashtags='+encodeURIComponent('シミュラボ,婚活'),'_blank','noopener'));
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

# 1. 婚活マッチ診断
SIMS.append(dict(id='konkatsu-match', cat='人生・自分ごと', emoji='💍',
  title='婚活マッチ診断｜年齢とスペックから、釣り合う相手像を試算｜シミュラボ',
  desc='年齢・年収・重視する条件から、婚活で釣り合いやすい相手の年齢・年収レンジやタイプの傾向、向いている出会い方を試算。人を点数化しない、やさしい婚活シミュレーターです。',
  ogtitle='婚活マッチ診断｜釣り合う相手像を試算', ogdesc='年齢とスペックから、釣り合いやすい相手のレンジと向いてる出会い方を試算。',
  h1='婚活マッチ診断',
  lead='年齢や条件から、婚活で「釣り合いやすい相手の傾向」を範囲（レンジ）で試算します。<strong>人を点数で値踏みするものではなく</strong>、現実的な目安と出会い方のヒントを得るためのものです。',
  inputs='''    <h2>💍 あなたのことを教えてください</h2>
    <div class="row"><div class="field"><label>あなたの性別</label><select id="sex"><option value="m">男性</option><option value="f">女性</option></select></div>
    <div class="field"><label>年齢 <span class="hint">（歳）</span></label><input type="number" id="age" value="30" min="18" max="80" inputmode="numeric"></div></div>
    <div class="field"><label>年収 <span class="hint">（万円）</span></label><input type="number" id="inc" value="400" min="0" inputmode="numeric"></div>
    <div class="field"><label>相手にいちばん重視すること</label><select id="pri">
      <option value="value">価値観・性格</option><option value="age">年齢・ライフステージ</option><option value="income">経済力</option><option value="look">外見・清潔感</option><option value="hobby">趣味の相性</option></select></div>
    <div class="field"><label>希望する相手の年齢</label><select id="apref"><option value="same" selected>同年代がいい</option><option value="older">年上がいい</option><option value="younger">年下がいい</option></select></div>
    <button class="btn btn-primary" id="calcBtn">釣り合う相手像を見る</button>''',
  result='''      <div class="label">釣り合いやすい相手の年齢</div>
      <div class="big"><span id="big">—</span><span class="unit">歳</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline">
        <div class="stat"><div class="k">相手の年収レンジ(目安)</div><div class="v accent" id="incr" style="font-size:16px;">—</div></div>
        <div class="stat"><div class="k">相性が良さそうなタイプ</div><div class="v" id="type" style="font-size:14px;">—</div></div>
        <div class="stat"><div class="k">向いてる出会い方</div><div class="v" id="way" style="font-size:14px;">—</div></div>
      </div>
      <div class="alert good" id="tip" style="text-align:left;margin-top:20px;">—</div>''',
  article='''    <h2>この診断の考え方</h2>
    <p>婚活では「年齢・生活水準が近い人同士」がマッチしやすい傾向があります。本診断は、その一般的な傾向をもとに、釣り合いやすい相手の<strong>範囲（レンジ）</strong>と出会い方の目安を示すものです。当たり外れを決めつけるものではありません。</p>
    <div class="note">⚠️ 大前提：人の魅力はスペックで決まりません。これはあくまで現実的な目安を知り、選択肢を広げるための<strong>参考・エンタメ</strong>です。</div>
    <h2>うまくいく人の共通点</h2>
    <ul><li><strong>条件を絞りすぎない</strong> ― チェックリストが多いほど候補は激減します。</li><li><strong>"一緒にいて楽"を最優先に</strong> ― スペックは入り口、続くかは相性。</li><li><strong>出会いの母数を増やす</strong> ― 手段を1つに絞らない。</li></ul>
    <h2>よくある質問</h2>''' + faq([('当たりますか？','一般的な傾向にもとづく目安です。実際の相性は会ってみないと分かりません。気楽にお使いください。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const sex=$('sex').value, age=Math.max(18,+$('age').value||18), inc=Math.max(0,+$('inc').value||0), pri=$('pri').value, ap=$('apref').value;
    let lo,hi; if(ap==='younger'){lo=age-7;hi=age-1;} else if(ap==='older'){lo=age+1;hi=age+7;} else {lo=age-3;hi=age+3;}
    lo=Math.max(18,lo); hi=Math.max(lo+1,hi);
    const ilo=Math.round(inc*0.7/10)*10, ihi=Math.round(inc*1.4/10)*10;
    const types={value:'価値観・生活リズムが合う人',age:'ライフステージが近い人',income:'堅実で金銭感覚が合う人',look:'清潔感・身だしなみを大切にする人',hobby:'趣味を一緒に楽しめる人'};
    let way; if(age<=32) way='マッチングアプリ（母数が多い）'; else if(age<=40) way='結婚相談所＋アプリ併用'; else way='結婚相談所・婚活パーティー';
    if(pri==='value'||pri==='hobby') way+='／趣味コミュ・紹介も◎';
    $('big').textContent=lo+'〜'+hi;
    $('sub').textContent=`${sex==='m'?'男性':'女性'}・${age}歳・年収${inc}万・重視：${sel('pri').text}`;
    $('incr').textContent=(inc>0?(`${ilo}〜${ihi}万円`):'こだわらないのも手');
    $('type').textContent=types[pri]; $('way').textContent=way;
    $('tip').innerHTML='💡 <strong>相手の年収などの条件を1つ緩めるだけで、候補は2〜3倍に広がります。</strong>スペックは入り口、最後は「一緒にいて楽か」が決め手です。';
    show();
    SHARE=`婚活マッチ診断やってみた💍 釣り合う相手は ${lo}〜${hi}歳／年収${ilo}〜${ihi}万・「${types[pri]}」タイプらしい。\\nでも結局スペックは入り口だよね。\\nあなたは？👇`;
  }'''))

# 2. 婚活 条件マッチ診断
SIMS.append(dict(id='konkatsu-jouken', cat='人生・自分ごと', emoji='💕',
  title='婚活 条件マッチ診断｜理想の条件、満たす人は何人いる？｜シミュラボ',
  desc='相手に求める年収・年齢・価値観などの条件から、その全部を満たす人がどれくらいいるか、条件を1つ緩めると候補が何倍に増えるかを試算する無料シミュレーター。',
  ogtitle='婚活 条件マッチ診断｜理想の条件、満たす人は何人いる？', ogdesc='理想の条件を全部満たす人は何人？1つ緩めると候補は何倍に？',
  h1='婚活 条件マッチ診断',
  lead='相手に求める条件、全部そろった人は実は何人いるのでしょう。条件をかけ合わせると候補は一気に減り、<strong>1つ緩めるだけで激増</strong>します。理想と現実のバランスを見てみましょう。',
  inputs='''    <h2>💕 相手への希望条件</h2>
    <div class="field"><label>あなたの活動エリア</label><select id="area"><option value="2000000">大都市（東京・大阪など）</option><option value="400000" selected>地方都市</option><option value="80000">地方・郊外</option></select></div>
    <div class="field"><label>相手の年収 下限 <span class="hint">（万円・こだわらないなら0）</span></label><input type="number" id="inc" value="500" min="0" inputmode="numeric"></div>
    <div class="field"><label>相手の年齢の範囲は？</label><select id="age"><option value="1">こだわらない</option><option value="0.45" selected>±5歳くらい</option><option value="0.25">±3歳くらい</option></select></div>
    <div class="field"><label>外見・身長へのこだわりは？</label><select id="look"><option value="0.9">あまりこだわらない</option><option value="0.6" selected>ある程度</option><option value="0.35">強く希望がある</option></select></div>
    <div class="field"><label>価値観・趣味の一致は？</label><select id="val"><option value="0.8">合えば嬉しい</option><option value="0.5" selected>ある程度重視</option><option value="0.3">とても重視</option></select></div>
    <button class="btn btn-primary" id="calcBtn">条件に合う人数を見る</button>''',
  result='''      <div class="label">あなたの条件、全部を満たす人は</div>
      <div class="big"><span id="big">0</span><span class="unit">人</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline">
        <div class="stat"><div class="k">エリアの独身(対象)</div><div class="v" id="base">—</div></div>
        <div class="stat"><div class="k">年収条件を100万下げると</div><div class="v accent" id="loosen">—</div></div>
        <div class="stat"><div class="k">難易度</div><div class="v" id="lv" style="font-size:16px;">—</div></div>
      </div>
      <div class="alert good" id="tip" style="text-align:left;margin-top:20px;">—</div>''',
  article='''    <h2>計算の考え方</h2>
    <div class="note"><strong>計算式</strong><br>候補者 ＝ エリアの独身人口 × 各条件の通過率の掛け算</div>
    <p>条件は「掛け算」で効きます。1つ1つは緩く見えても、3つ4つ重なると候補は一気に数人〜ゼロに。逆に、いちばん厳しい条件を1つ緩めるだけで候補は何倍にもなります。</p>
    <div class="note">⚠️ これは選択肢の広さを知るための<strong>参考・エンタメ</strong>です。人を条件で選別することを推奨するものではありません。</div>
    <h2>よくある質問</h2>''' + faq([('正確な人数ですか？','一般的な割合を用いた概算です。実際の出会いは人数だけでは決まりません。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const base=+$('area').value, incLo=Math.max(0,+$('inc').value||0), ageF=+$('age').value, lookF=+$('look').value, valF=+$('val').value;
    const singles=base*0.30; // 対象性別の独身概算
    const incPass=(x)=>Math.max(0.02, 0.9*Math.exp(-Math.max(0,x-300)/400));
    const cand=singles*incPass(incLo)*ageF*lookF*valF;
    const loose=singles*incPass(Math.max(0,incLo-100))*ageF*lookF*valF;
    const ratio= cand>0? loose/cand : 0;
    let lv= cand>=1000?'イージー':cand>=100?'ノーマル':cand>=10?'ハード':cand>=1?'ベリーハード':'ほぼ奇跡';
    $('sub').textContent=`${sel('area').text}・年収${incLo}万↑・${sel('age').text}`;
    $('base').textContent=num(singles)+'人'; $('loosen').textContent='約'+num(loose)+'人(×'+ratio.toFixed(1)+')'; $('lv').textContent=lv;
    $('tip').innerHTML=`💡 <strong>年収条件を100万下げるだけで候補は約${ratio.toFixed(1)}倍に。</strong>条件を全部そろえるより、"これだけは"を1〜2個に絞るのが成功のコツです。`;
    show(); anim($('big'),0,cand,900);
  }'''))

# 3. 婚活 相性タイプ診断
SIMS.append(dict(id='konkatsu-type', cat='人生・自分ごと', emoji='🫶',
  title='婚活 相性タイプ診断｜あなたに合う相手のタイプは？｜シミュラボ',
  desc='5つの質問に答えるだけで、あなたの恋愛・結婚の価値観タイプと、相性が良さそうな相手のタイプ、向いている婚活の方法を診断する無料シミュレーター。',
  ogtitle='婚活 相性タイプ診断｜あなたに合う相手のタイプは？', ogdesc='5つの質問で、あなたの価値観タイプと相性の良い相手・婚活法を診断。',
  h1='婚活 相性タイプ診断',
  lead='恋愛・結婚で大事にするものは人それぞれ。5つの質問から、あなたの価値観タイプと、相性が良さそうな相手・向いている婚活の方法を診断します。',
  inputs='''    <h2>🫶 5つの質問に答える</h2>
    <div class="field"><label>① 理想のデートは？</label><select id="q1"><option value="a">家でまったり過ごす</option><option value="b" selected>定番スポットに出かける</option><option value="c">行ったことない所を冒険</option></select></div>
    <div class="field"><label>② 将来、大事にしたいのは？</label><select id="q2"><option value="a">安定した毎日</option><option value="b" selected>二人の成長</option><option value="c">刺激と変化</option></select></div>
    <div class="field"><label>③ 休日は二人で？それぞれ？</label><select id="q3"><option value="a">できるだけ一緒に</option><option value="b" selected>ほどよくバランス</option><option value="c">お互い自由に</option></select></div>
    <div class="field"><label>④ お金の使い方は？</label><select id="q4"><option value="a">コツコツ貯める</option><option value="b" selected>メリハリ重視</option><option value="c">経験にどんどん使う</option></select></div>
    <div class="field"><label>⑤ ケンカしたら？</label><select id="q5"><option value="a">すぐ話し合って解決</option><option value="b" selected>少し時間を置く</option><option value="c">気にせず引きずらない</option></select></div>
    <button class="btn btn-primary" id="calcBtn">相性タイプを診断する</button>''',
  result='''      <div class="label">あなたの婚活タイプは</div>
      <div class="big" style="font-size:clamp(26px,6vw,40px)"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline">
        <div class="stat"><div class="k">相性が良さそうな相手</div><div class="v" id="match" style="font-size:14px;">—</div></div>
        <div class="stat"><div class="k">向いてる婚活の方法</div><div class="v" id="way" style="font-size:14px;">—</div></div>
      </div>''',
  article='''    <h2>この診断について</h2>
    <p>恋愛・結婚の価値観を「安定⇔刺激」「一緒に過ごす⇔お互い自立」の2軸でとらえ、4タイプに分類します。相性のヒントとしてお楽しみください（結果がすべてではありません）。</p>
    <h2>よくある質問</h2>''' + faq([('当たりますか？','エンタメ診断です。タイプはあくまで傾向で、相性は実際の関係づくりで育つものです。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    // A: 安定(-)〜刺激(+)  /  B: 一緒(-)〜自立(+)
    const mapA={a:-1,b:0,c:1}, mapB={a:-1,b:0,c:1};
    let A=0,B=0;
    A+=mapA[$('q1').value]; A+=mapA[$('q2').value]; A+=mapA[$('q4').value]; A+=mapA[$('q5').value]*0.5;
    B+=mapB[$('q3').value]; B+=mapB[$('q1').value]*0.5; B+=mapB[$('q5').value]*0.5;
    const stim=A>=0, indep=B>=0;
    let t,m,w;
    if(!stim && !indep){ t='ぬくもり家庭型'; m='同じく家庭的で安定志向の人。一緒に過ごす時間を大切にできる相手'; w='結婚相談所・友人紹介（誠実な出会い）'; }
    else if(!stim && indep){ t='堅実パートナー型'; m='価値観が近く、お互いの時間も尊重できる自立した人'; w='結婚相談所・マッチングアプリ（条件で絞り込み）'; }
    else if(stim && !indep){ t='情熱ホーム型'; m='一緒に楽しみつつ家庭も大切にできる、表現豊かな人'; w='趣味コミュニティ・婚活パーティー'; }
    else { t='自由冒険型'; m='新しいことを一緒に楽しめる、束縛しない行動派の人'; w='マッチングアプリ・趣味イベント'; }
    $('big').textContent=t; $('sub').textContent='価値観を2軸で分析';
    $('match').textContent=m; $('way').textContent=w;
    SHARE=`婚活 相性タイプ診断、私は「${t}」でした🫶 相性◎なのは『${m}』らしい。\\nあなたは？👇`;
    show();
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
