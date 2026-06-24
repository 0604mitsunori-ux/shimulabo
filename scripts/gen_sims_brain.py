# -*- coding: utf-8 -*-
"""シミュラボ：脳トレ・診断テストカテゴリ 10本（診断クイズ7＋ミニゲーム3）。
新カテゴリ slug=brain「脳トレ・診断テスト」。gen_sims11方式TPL（try無し・calcは関数スコープ直置き）。
全てエンタメ／セルフチェック（医療診断ではない旨を明記）。

seo_internal.py / gen_images.py のauto-importに 'gen_sims_brain' を追加して使う。
"""
import os, sys, json
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
      <div class="viz-wrap" style="margin-top:14px;">__VISUAL__</div>
      <div style="text-align:center;margin-top:12px;"><span id="shareCount" class="share-count" style="display:none"></span></div>
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
    <h2>💡 こんな診断も見てみたい？</h2>
    <p>あなたの「これ診断・テストしてみたい」を送ってください。投票で人気の案から実際に作ります。</p>
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
  const clamp = (v,a,b) => Math.max(a,Math.min(b,v));
  let SHARE = '', raf = 0;
  function show(){ $('resultPanel').style.display=''; $('resultPanel').scrollIntoView({behavior:'smooth',block:'start'}); }
  function gauge(score,max,col){const c=$('viz');if(!c)return;const x=c.getContext('2d'),W=c.width,H=c.height,bx=20,bw=W-40,by=H/2-10;cancelAnimationFrame(raf);
    const frac=clamp(score/max,0,1),t0=performance.now();
    function f(n){const p=Math.min(1,(n-t0)/800);x.fillStyle='#0b1530';x.fillRect(0,0,W,H);
      x.fillStyle='rgba(255,255,255,.1)';x.fillRect(bx,by,bw,20);
      x.fillStyle=col||'#6366f1';x.fillRect(bx,by,bw*frac*p,20);
      x.fillStyle='#fff';x.font='bold 13px sans-serif';x.textAlign='center';x.fillText(num(score*p)+' / '+max,W/2,by+40);
      if(p<1)raf=requestAnimationFrame(f);}raf=requestAnimationFrame(f);}
__JS__
  const cb=$('calcBtn'); if(cb) cb.addEventListener('click', calc);
  const sb=$('shareBtn'); if(sb) sb.addEventListener('click', () => window.open('https://twitter.com/intent/tweet?text='+encodeURIComponent(SHARE)+'&url='+encodeURIComponent(location.href)+'&hashtags='+encodeURIComponent('シミュラボ,診断'),'_blank','noopener'));
  const cp=$('copyBtn'); if(cp) cp.addEventListener('click', async () => { try{ await navigator.clipboard.writeText(SHARE+'\\n'+location.href); $('copyBtn').textContent='コピーしました ✓'; setTimeout(()=>$('copyBtn').textContent='結果をコピー',1600);}catch{alert(SHARE);} });
})();
</script>
<script src="../../assets/result-fx.js"></script>
<script src="../../assets/share-counter.js"></script>
<script>ShareCounter.initSim({ simId:'__ID__', badgeEl:document.getElementById('shareCount'), shareBtnIds:['shareBtn'] });</script>
</body>
</html>
'''

CAT = '脳トレ・診断テスト'
def viz(w=480,h=90,mx=500):
    return (f'<canvas id="viz" width="{w}" height="{h}" style="width:100%;max-width:{mx}px;height:auto;'
            f'display:block;margin:0 auto;background:#0b1530;border-radius:12px;"></canvas>')

SIMS=[]

# ---------- 診断クイズ共通 ----------
QUIZ_INPUTS = '''    <h2>__QHEAD__</h2>
    <p style="color:var(--ink-2);font-size:13px;margin:-4px 0 6px;">直感で選んでOK。<span id="prog" style="font-weight:800;color:var(--teal-d);">0 / __QN__ 問</span></p>
    <div id="quiz" class="quiz"></div>
    <button class="btn btn-primary" id="calcBtn" style="margin-top:8px;">結果を見る</button>'''

QUIZ_RESULT = '''      <div class="label">__RLABEL__</div>
      <div id="emoji" style="font-size:64px;line-height:1.1;">❓</div>
      <div class="big" style="font-size:26px;"><span id="big">—</span></div>
      <div class="sub" id="score">—</div>
      <div class="alert good" id="advice" style="text-align:left;margin-top:14px;">—</div>'''

def quiz_sim(id, emoji, title, desc, ogtitle, ogdesc, h1, lead, qhead, questions, bands, rlabel, sharetpl, article, gaugecol='#6366f1'):
    # questions: [ [qtext, [[opt,pts],...]], ... ]   bands: [ [maxScore, emoji, label, advice], ... ] 昇順
    qn = len(questions)
    maxscore = sum(max(p for _,p in opts) for _,opts in questions)
    js = ('  const Q=' + json.dumps(questions, ensure_ascii=False) + ';\n'
          '  const BANDS=' + json.dumps(bands, ensure_ascii=False) + ';\n'
          '  const MAXS=' + str(maxscore) + ', RLABEL=' + json.dumps(rlabel, ensure_ascii=False) + ';\n'
          '  const SHARETPL=' + json.dumps(sharetpl, ensure_ascii=False) + ';\n'
          '  const GCOL=' + json.dumps(gaugecol, ensure_ascii=False) + ';\n'
          + r'''  const wrap=$('quiz');
  Q.forEach((q,i)=>{const d=document.createElement('div');d.className='q';
    let h='<p class="qt"><b>Q'+(i+1)+'.</b> '+q[0]+'</p><div class="opts" style="grid-template-columns:1fr;">';
    q[1].forEach((o,j)=>{h+='<button type="button" class="opt" data-q="'+i+'" data-p="'+o[1]+'">'+o[0]+'</button>';});
    d.innerHTML=h+'</div>';wrap.appendChild(d);});
  wrap.addEventListener('click',e=>{const b=e.target.closest('.opt');if(!b)return;const qi=b.dataset.q;
    wrap.querySelectorAll('.opt[data-q="'+qi+'"]').forEach(o=>o.classList.toggle('on',o===b));
    const p=$('prog');if(p)p.textContent=document.querySelectorAll('#quiz .opt.on').length+' / '+Q.length+' 問';});
  function calc(){const on=document.querySelectorAll('#quiz .opt.on');
    if(on.length<Q.length){alert('あと'+(Q.length-on.length)+'問！全部の質問に答えてね');
      const qs=document.querySelectorAll('#quiz .q');for(let j=0;j<qs.length;j++){if(!qs[j].querySelector('.opt.on')){qs[j].scrollIntoView({behavior:'smooth',block:'center'});break;}}return;}
    let s=0;on.forEach(b=>s+=(+b.dataset.p||0));
    let band=BANDS[BANDS.length-1];for(const bd of BANDS){if(s<=bd[0]){band=bd;break;}}
    $('emoji').textContent=band[1];$('big').textContent=band[2];$('score').textContent='スコア '+s+' / '+MAXS;
    $('advice').textContent='💡 '+band[3];
    SHARE=SHARETPL.replace('{label}',band[2]).replace('{score}',s);
    show();gauge(s,MAXS,GCOL);}
''')
    SIMS.append(dict(id=id, emoji=emoji, cat=CAT,
        title=title, desc=desc, ogtitle=ogtitle, ogdesc=ogdesc, h1=h1, lead=lead,
        inputs=QUIZ_INPUTS.replace('__QHEAD__',qhead).replace('__QN__',str(qn)),
        result=QUIZ_RESULT.replace('__RLABEL__',rlabel), visual=viz(), article=article, js=js))

def quiz_article(intro, faqs):
    return ('    <div class="note"><strong>これは何？</strong>：' + intro
            + '<br><b>※医療的な診断ではなく、セルフチェックのエンタメ診断です。</b>気になる症状が続く場合は専門家にご相談ください。</div>\n'
            '    <h2>使い方</h2>\n    <p>各質問に直感で答えるだけ。最後に「結果を見る」を押すと、スコアからあなたの傾向を判定します。当てはまりすぎても、当たらなくても、自分を見つめるきっかけにどうぞ。</p>\n'
            '    <h2>よくある質問</h2>' + faq(faqs))

# 4点スケール共通選択肢
S4 = [['とても当てはまる',3],['まあ当てはまる',2],['あまり当てはまらない',1],['全く当てはまらない',0]]
def q(text): return [text, [list(o) for o in S4]]

# ============================================================
# 1. 簡易ストレスチェック（ストレスチェック 23000/KD26/TP44000）
# ============================================================
quiz_sim('stress-check','😣',
  'ストレスチェック（簡易）｜今のストレス度を10問でセルフ診断｜シミュラボ',
  '今のストレス度を10問でセルフチェックできる無料の簡易ストレスチェック。仕事や生活の疲れ・イライラ・眠れなさから、ストレスのたまり具合と対処のヒントが分かります（エンタメ診断）。',
  'ストレスチェック（簡易）｜今のストレス度を診断', '10問で今のストレス度をセルフチェック。対処のヒントも。',
  'ストレスチェック（簡易セルフ診断）',
  '最近のあなたのストレス、たまっていませんか？10問でストレス度をセルフチェックし、今の状態と対処のヒントを表示します。',
  '😣 最近2週間の状態に答えてね',
  [q('些細なことでもイライラしやすい'),q('夜なかなか眠れない・眠りが浅い'),q('疲れが抜けず、朝がつらい'),
   q('仕事や家事に集中できない'),q('食欲が落ちた、または食べすぎる'),q('気分が落ち込み、楽しめない'),
   q('頭痛・肩こり・胃の不調がある'),q('人と会うのが面倒に感じる'),q('将来や物事を悲観しがち'),q('リラックスできる時間がない')],
  [[7,'😌','ストレス低め','今は良い状態。この調子で休息と気分転換を続けて。'],
   [15,'🙂','ストレスやや軽め','大きな問題はなさそう。早めの休息でさらに整います。'],
   [22,'😣','ストレス中くらい','疲れがたまり気味。睡眠・運動・人に話す、で意識的にケアを。'],
   [30,'😵','ストレス高め','かなりお疲れの様子。無理せず休み、つらさが続くなら専門家に相談を。']],
  'あなたのストレス度は',
  'ストレスチェック（簡易）、私の結果は「{label}」（スコア{score}）でした😣 あなたは？',
  quiz_article('最近2週間の心身の状態から、今のストレスのたまり具合をセルフチェックする簡易テストです。',
    [('正式なストレスチェックですか？','いいえ。手軽なセルフチェックのエンタメ版です。職場の正式な検査とは異なります。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  gaugecol='#f43f5e')

# ============================================================
# 2. HSP診断（繊細さん）
# ============================================================
quiz_sim('hsp-shindan','🌿',
  'HSP診断（繊細さん）｜あなたの繊細さレベルを12問でチェック｜シミュラボ',
  '生まれつき敏感で繊細な気質「HSP（繊細さん）」の傾向を12問でセルフチェックできる無料診断。音・光・人の感情に敏感、共感しやすい…あなたの繊細さレベルが分かります（エンタメ診断）。',
  'HSP診断（繊細さん）｜繊細さレベルをチェック', '12問であなたのHSP（繊細さん）傾向をセルフチェック。',
  'HSP診断（繊細さん度）',
  '人の気持ちや音・光に敏感で、気疲れしやすい…そんな「繊細さん（HSP）」の傾向を12問でセルフチェックします。あなたの繊細さレベルは？',
  '🌿 当てはまる度合いで答えてね',
  [q('大きな音や強い光が苦手だ'),q('人の機嫌や場の空気にすぐ気づく'),q('他人の感情に強く影響される'),
   q('一度にたくさんのことを頼まれると混乱する'),q('些細なことが気になって眠れないことがある'),q('暴力的な映画やニュースが苦手'),
   q('美しい音楽や芸術に深く感動する'),q('短時間でも人混みに行くとどっと疲れる'),q('カフェインや空腹に敏感だ'),
   q('ミスを指摘されると人一倍落ち込む'),q('一人になれる時間がないとつらい'),q('細かい変化（家具の位置など）によく気づく')],
  [[12,'😎','たくましいタイプ','繊細さは控えめ。ストレスに強く、おおらかに過ごせるタイプ。'],
   [22,'🙂','ふつう寄り','場面によって敏感さが出るバランス型。'],
   [30,'🌿','やや繊細さん','HSP傾向あり。刺激を減らし、一人時間で回復を。'],
   [36,'🍃','しっかり繊細さん','強いHSP傾向。あなたの感受性は才能。無理せず自分を守って。']],
  'あなたの繊細さレベルは',
  'HSP診断（繊細さん）、私は「{label}」（スコア{score}）でした🌿 あなたは？',
  quiz_article('HSP（Highly Sensitive Person＝とても敏感な人）の傾向を、刺激や感情への反応からセルフチェックします。',
    [('HSPは病気？','いいえ。生まれ持った気質の一つとされ、病気や障害ではありません。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  gaugecol='#34d399')

# ============================================================
# 3. EQ診断（心の知能指数）
# ============================================================
quiz_sim('eq-shindan','💗',
  'EQ診断｜心の知能指数（こころの賢さ）を10問でチェック｜シミュラボ',
  '感情を理解し、うまく付き合う力「EQ（心の知能指数）」を10問でセルフチェックできる無料診断。自分や相手の感情への気づき、共感力、感情コントロール力が分かります（エンタメ診断）。',
  'EQ診断｜心の知能指数をチェック', '10問であなたのEQ（心の知能指数）をセルフチェック。共感力・感情コントロール。',
  'EQ診断（心の知能指数）',
  'IQが頭の良さなら、EQは「心の賢さ」。自分や相手の感情を理解し、うまく付き合う力を10問でセルフチェックします。',
  '💗 当てはまる度合いで答えてね',
  [q('自分が今どんな感情かを言葉にできる'),q('イライラしても衝動的に行動しないでいられる'),q('相手の表情や声から気持ちを察せる'),
   q('落ち込んでも自分なりに立ち直る方法を持っている'),q('意見の違う相手とも冷静に話せる'),q('人の長所に目を向けられる'),
   q('プレッシャーの中でも平常心を保てる'),q('自分の弱みを認められる'),q('困っている人につい手を貸したくなる'),q('感謝の気持ちを言葉で伝えられる')],
  [[10,'🌱','EQ伸びしろ大','今はこれから。感情に名前をつける習慣で、ぐんと伸びます。'],
   [18,'🙂','EQ標準','バランス良好。共感と冷静さを意識するとさらに◎。'],
   [25,'💗','EQ高め','感情の扱いが上手。人から信頼されるタイプ。'],
   [30,'👑','EQマスター','とても高いEQ。リーダーや相談役にぴったり。']],
  'あなたのEQは',
  'EQ診断、私の心の知能指数は「{label}」（スコア{score}）でした💗 あなたは？',
  quiz_article('EQ（Emotional Intelligence Quotient＝心の知能指数）を、感情への気づき・共感・自己コントロールの面からセルフチェックします。',
    [('EQは上げられる？','はい。IQと違い、意識と練習で伸ばせるとされています。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  gaugecol='#ec4899')

# ============================================================
# 4. 怒りやすさ診断（アンガー）
# ============================================================
quiz_sim('anger-type','🔥',
  '怒りやすさ診断（アンガー）｜あなたの“沸点”を10問でチェック｜シミュラボ',
  'カッとなりやすさ・怒りのコントロール力を10問でセルフチェックできる無料の怒りやすさ診断。あなたの“沸点”の低さと、アンガーマネジメントのヒントが分かります（エンタメ診断）。',
  '怒りやすさ診断（アンガー）｜あなたの沸点は？', '10問であなたの怒りやすさ・沸点をセルフチェック。',
  '怒りやすさ診断（アンガー）',
  'ついカッとなって後悔する…そんな「怒りやすさ」を10問でセルフチェック。あなたの“沸点”の低さと、上手な付き合い方のヒントを表示します。',
  '🔥 当てはまる度合いで答えてね',
  [q('順番待ちや渋滞でイライラする'),q('思い通りにならないと態度に出る'),q('一度怒ると引きずりやすい'),
   q('「普通こうでしょ」と思うことが多い'),q('人のミスが許せないことがある'),q('カッとなって言い過ぎてしまう'),
   q('SNSの投稿にイラッとする'),q('店員や家族につい強い口調になる'),q('怒った後で後悔することが多い'),q('自分は正しいと思うと譲れない')],
  [[8,'🧊','仏のように穏やか','沸点が高く、めったに怒らないタイプ。周りも安心。'],
   [16,'🙂','穏やかめ','基本は冷静。たまにイラッとするくらいで健全。'],
   [24,'🔥','やや沸点低め','カッとなりやすい傾向。6秒待つだけで衝動は和らぎます。'],
   [30,'🌋','沸点かなり低め','怒りが強めに出やすいかも。深呼吸とその場を離れる習慣を。']],
  'あなたの怒りやすさは',
  '怒りやすさ診断、私の沸点は「{label}」（スコア{score}）でした🔥 あなたは？',
  quiz_article('日常のイライラ場面への反応から、怒りやすさ（沸点の低さ）とコントロール力をセルフチェックします。',
    [('怒りっぽいのは直せる？','アンガーマネジメント（6秒待つ等）で和らげられるとされています。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  gaugecol='#f59e0b')

# ============================================================
# 5. 完璧主義度診断
# ============================================================
quiz_sim('kanpeki-do','📏',
  '完璧主義度診断｜あなたのこだわりの強さを10問でチェック｜シミュラボ',
  '何事もきっちりやらないと気が済まない「完璧主義」の強さを10問でセルフチェックできる無料診断。完璧主義の良い面・しんどい面と、ラクになるヒントが分かります（エンタメ診断）。',
  '完璧主義度診断｜こだわりの強さをチェック', '10問であなたの完璧主義度をセルフチェック。',
  '完璧主義度診断',
  '何事もきっちりしないと気が済まない…その「完璧主義」の強さを10問でセルフチェック。長所にも、しんどさにもなるこだわりを見える化します。',
  '📏 当てはまる度合いで答えてね',
  [q('やるなら完璧にやりたい'),q('細かいミスがどうしても気になる'),q('人に任せるより自分でやりたい'),
   q('80点では満足できない'),q('準備に時間をかけすぎてしまう'),q('「だいたいでいい」が苦手'),
   q('人の評価がとても気になる'),q('できなかった点ばかり思い出す'),q('計画通りに進まないと不安'),q('自分にも他人にも厳しい')],
  [[8,'🍃','おおらかタイプ','良い意味で力が抜けている。完璧より「まあいっか」が上手。'],
   [16,'🙂','バランス型','こだわるところと流すところのメリハリが◎。'],
   [24,'📏','しっかり完璧主義','高い基準が強み。でも8割で十分な場面も多いですよ。'],
   [30,'🎯','ストイック完璧主義','こだわりが強め。自分を追い込みすぎないよう、合格点を下げる練習を。']],
  'あなたの完璧主義度は',
  '完璧主義度診断、私は「{label}」（スコア{score}）でした📏 あなたは？',
  quiz_article('物事へのこだわり方から、完璧主義の強さをセルフチェックします。完璧主義は長所にも、しんどさにもなります。',
    [('完璧主義は悪いこと？','いいえ。高い成果につながる長所です。ただ強すぎると疲れやすい面も。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  gaugecol='#6366f1')

# ============================================================
# 6. 気疲れ・人疲れ度診断
# ============================================================
quiz_sim('kizukare','🫠',
  '気疲れ・人疲れ度診断｜人といると疲れるあなたへ｜10問チェック｜シミュラボ',
  '人といると気を使って疲れてしまう「気疲れ・人疲れ」の度合いを10問でセルフチェックできる無料診断。気疲れしやすさと、ラクに過ごすヒントが分かります（エンタメ診断）。',
  '気疲れ・人疲れ度診断｜10問チェック', '10問であなたの気疲れ・人疲れ度をセルフチェック。',
  '気疲れ・人疲れ度診断',
  '人といると、つい気を使ってどっと疲れる…その「気疲れ度」を10問でセルフチェック。あなたの人疲れしやすさと、ラクに過ごすヒントを表示します。',
  '🫠 当てはまる度合いで答えてね',
  [q('人に会った後はどっと疲れる'),q('相手に合わせて自分を抑えがち'),q('沈黙が気まずくて気を使う'),
   q('嫌われないか気にしてしまう'),q('断るのが苦手でつい引き受ける'),q('人の機嫌が気になって仕方ない'),
   q('一人になるとホッとする'),q('LINEの返信に気を使いすぎる'),q('集まりの後に「あの言動大丈夫だったかな」と振り返る'),q('本音より建前で話しがち')],
  [[8,'😎','マイペース','人に振り回されにくく、自然体で過ごせるタイプ。'],
   [16,'🙂','ほどほど','気を使いつつも自分を保てるバランス型。'],
   [24,'🫠','気疲れしやすい','人に合わせがちで消耗気味。一人時間で意識的に回復を。'],
   [30,'😮‍💨','かなり人疲れ','気の使いすぎでヘトヘトかも。「断る・頼る」の練習でぐっとラクに。']],
  'あなたの気疲れ度は',
  '気疲れ・人疲れ度診断、私は「{label}」（スコア{score}）でした🫠 あなたは？',
  quiz_article('人付き合いでの気の使い方から、気疲れ・人疲れのしやすさをセルフチェックします。',
    [('気疲れしやすいのは性格？','繊細さや優しさの裏返しでもあります。自分を責めず、休む工夫を。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  gaugecol='#a78bfa')

# ============================================================
# 7. 心配性度診断
# ============================================================
quiz_sim('shinpaisei','😟',
  '心配性度診断｜あなたの不安の強さを10問でチェック｜シミュラボ',
  '先のことや小さなことをつい心配してしまう「心配性」の強さを10問でセルフチェックできる無料診断。不安の強さと、考えすぎをやわらげるヒントが分かります（エンタメ診断）。',
  '心配性度診断｜不安の強さをチェック', '10問であなたの心配性度・不安の強さをセルフチェック。',
  '心配性度診断',
  '起きてもいないことをつい心配してしまう…その「心配性」の強さを10問でセルフチェック。あなたの不安の強さと、考えすぎをやわらげるヒントを表示します。',
  '😟 当てはまる度合いで答えてね',
  [q('まだ起きていないことを心配しがち'),q('最悪のケースを想像してしまう'),q('外出後に戸締まりや火を気にする'),
   q('小さな体調の変化が気になる'),q('決断する前に何度も確認したくなる'),q('人の何気ない一言を引きずる'),
   q('予定が決まらないと落ち着かない'),q('「大丈夫かな」が口ぐせ'),q('考えすぎて眠れないことがある'),q('リスクを取るのが怖い')],
  [[8,'😌','楽天家','「なんとかなる」と思えるおおらかタイプ。'],
   [16,'🙂','ほどほど慎重','適度に備えつつ前に進める健全なタイプ。'],
   [24,'😟','心配性','先回りして不安になりがち。慎重さは強みでもあります。'],
   [30,'😰','かなり心配性','考えすぎてしまう傾向。「今できること」に絞ると軽くなります。']],
  'あなたの心配性度は',
  '心配性度診断、私は「{label}」（スコア{score}）でした😟 あなたは？',
  quiz_article('先のことや小さなことへの不安の出やすさから、心配性の強さをセルフチェックします。',
    [('心配性は短所？','慎重で備えが上手という長所でもあります。強すぎると疲れる面も。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  gaugecol='#0ea5e9')

# ============================================================
# 8. 脳年齢テスト（計算スピード）★ミニゲーム
# ============================================================
SIMS.append(dict(id='nou-nenrei', emoji='🧠', cat=CAT,
  title='脳年齢テスト｜計算スピードで脳の若さをチェック（無料）｜シミュラボ',
  desc='10問の簡単な計算をどれだけ速く正確に解けるかで、あなたの「脳年齢」をチェックする無料の脳トレテスト。スキマ時間の脳の活性化チェックに（エンタメ）。',
  ogtitle='脳年齢テスト｜計算スピードで脳の若さをチェック', ogdesc='10問の計算スピードであなたの脳年齢をチェック。無料の脳トレ。',
  h1='脳年齢テスト（計算スピード）',
  lead='かんたんな計算を10問、どれだけ速く正確に解けるかで「脳年齢」をチェックします。スタートを押すと問題が出ます。スピード勝負！（エンタメテストです）',
  inputs='''    <h2>🧠 計算で脳年齢チェック</h2>
    <div id="game" style="display:none;text-align:center;background:var(--bg-2,#f6f8fb);border:1px solid var(--line);border-radius:14px;padding:22px;margin-bottom:12px;">
      <div id="q" style="font-size:30px;font-weight:900;letter-spacing:1px;">—</div>
      <input type="number" id="ans" inputmode="numeric" autocomplete="off" style="font-size:22px;text-align:center;width:140px;padding:10px;margin-top:14px;border:1.5px solid var(--line);border-radius:10px;">
      <div style="margin-top:12px;"><button class="btn btn-primary" id="submit" style="width:auto;padding:10px 26px;">答える</button></div>
      <div id="prog" style="margin-top:10px;color:var(--ink-2);font-weight:800;font-size:13px;">—</div>
    </div>
    <button class="btn btn-primary" id="calcBtn">▶ スタート</button>''',
  result='''      <div class="label">あなたの脳年齢は</div>
      <div class="big"><span id="big">—</span><span class="unit">歳</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">かかった時間</div><div class="v accent" id="time">—</div></div>
      <div class="stat"><div class="k">正解数</div><div class="v" id="correct">—</div></div>
      <div class="stat"><div class="k">1問あたり</div><div class="v" id="per">—</div></div></div>''',
  visual='',
  article='''    <div class="note"><strong>遊び方</strong><br>「スタート」を押すと計算問題が10問出ます。答えを入力して「答える」（またはEnter）。速く正確に解けるほど脳年齢が若く出ます。</div>
    <h2>脳年齢テストとは</h2>
    <p>簡単な計算を素早く解く「単純計算」は、脳の前頭前野を活性化させる脳トレとして知られています。本テストは計算の速さと正確さから脳年齢の目安を出すエンタメです。毎日のスキマ時間にどうぞ。<b>※医学的な検査ではありません。</b></p>
    <h2>よくある質問</h2>'''+faq([
      ('何回でもできる？','はい。「もう一回」で再挑戦できます。慣れると速くなります。'),
      ('スマホでもできる？','できます。数字キーボードで入力してください。'),
      ('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  js=r'''  let probs=[],idx=0,t0=0,correct=0,running=false;
  function gen(){probs=[];for(let i=0;i<10;i++){const op=['+','-','×'][Math.floor(Math.random()*3)];let a,b;
    if(op==='×'){a=2+Math.floor(Math.random()*8);b=2+Math.floor(Math.random()*8);}
    else{a=5+Math.floor(Math.random()*45);b=2+Math.floor(Math.random()*Math.min(a-1,40));}
    const ans=op==='+'?a+b:op==='-'?a-b:a*b;probs.push([a,op,b,ans]);}}
  function showP(){const p=probs[idx];$('q').textContent=p[0]+' '+p[1]+' '+p[2]+' = ?';$('prog').textContent=(idx+1)+' / 10 問';$('ans').value='';$('ans').focus();}
  function start(){gen();idx=0;correct=0;running=true;$('game').style.display='';$('resultPanel').style.display='none';$('calcBtn').textContent='▶ もう一回';t0=performance.now();showP();}
  function submit(){if(!running)return;const p=probs[idx];if(Math.trunc(+$('ans').value)===p[3])correct++;idx++;if(idx>=10)finish();else showP();}
  function finish(){running=false;const sec=(performance.now()-t0)/1000,wrong=10-correct;
    let age=Math.round(18+sec*1.1+wrong*6);age=clamp(age,18,90);
    $('big').textContent=age;$('sub').textContent=(age<=30?'素晴らしい反応速度！':age<=50?'平均的な脳年齢です':'ゆっくりペース。脳トレで若返りを');
    $('time').textContent=sec.toFixed(1)+'秒';$('correct').textContent=correct+' / 10';$('per').textContent=(sec/10).toFixed(2)+'秒';
    SHARE='脳年齢テスト、私の脳年齢は'+age+'歳でした🧠（10問'+sec.toFixed(1)+'秒・正解'+correct+'）あなたは？';
    $('game').style.display='none';show();}
  $('submit').addEventListener('click',submit);
  $('ans').addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();submit();}});
  function calc(){start();}'''))

# ============================================================
# 9. 数字記憶テスト（digit span）★ミニゲーム
# ============================================================
SIMS.append(dict(id='suuji-kioku', emoji='🔢', cat=CAT,
  title='数字記憶テスト｜何桁まで覚えられる？記憶力チェック（無料）｜シミュラボ',
  desc='画面に表示される数字を覚えて入力し、何桁まで覚えられるかを測る無料の数字記憶テスト（数唱・ワーキングメモリ）。脳トレ・記憶力チェックに（エンタメ）。',
  ogtitle='数字記憶テスト｜何桁まで覚えられる？', ogdesc='表示される数字を記憶。何桁まで覚えられるか測る記憶力テスト。',
  h1='数字記憶テスト（何桁まで覚えられる？）',
  lead='画面に数字が一瞬表示されます。消えたら同じ数字を入力。正解すると桁数が1つ増えます。あなたは何桁まで覚えられる？（ワーキングメモリの脳トレ）',
  inputs='''    <h2>🔢 数字を記憶しよう</h2>
    <div id="game" style="display:none;text-align:center;background:var(--bg-2,#f6f8fb);border:1px solid var(--line);border-radius:14px;padding:22px;margin-bottom:12px;">
      <div id="show" style="font-size:36px;font-weight:900;letter-spacing:6px;min-height:46px;">—</div>
      <input type="number" id="ans" inputmode="numeric" autocomplete="off" style="font-size:22px;text-align:center;width:200px;padding:10px;margin-top:14px;border:1.5px solid var(--line);border-radius:10px;display:none;">
      <div style="margin-top:12px;"><button class="btn btn-primary" id="submit" style="width:auto;padding:10px 26px;display:none;">これだ！</button></div>
      <div id="lvl" style="margin-top:10px;color:var(--ink-2);font-weight:800;font-size:13px;">—</div>
    </div>
    <button class="btn btn-primary" id="calcBtn">▶ スタート</button>''',
  result='''      <div class="label">覚えられた桁数</div>
      <div class="big"><span id="big">—</span><span class="unit">桁</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">判定</div><div class="v accent" id="judge">—</div></div>
      <div class="stat"><div class="k">平均の目安</div><div class="v" id="avg">7桁前後</div></div></div>''',
  visual='',
  article='''    <div class="note"><strong>遊び方</strong><br>数字が約1.5秒表示→消えたら入力→「これだ！」。正解で桁数アップ、間違えると終了。表示中は覚えることに集中！</div>
    <h2>数字記憶テスト（数唱）とは</h2>
    <p>短い間だけ情報を保持する力を「ワーキングメモリ」と呼びます。人が一度に覚えられる数字は平均7桁前後（マジカルナンバー7）と言われます。塊（チャンク）にして覚えると桁数を伸ばせます。<b>※エンタメの脳トレです。</b></p>
    <h2>よくある質問</h2>'''+faq([
      ('平均は何桁？','一般に7桁前後とされます。9桁以上覚えられたらかなり優秀です。'),
      ('コツは？','3桁ずつ区切る、声に出す、リズムをつけると覚えやすくなります。'),
      ('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  js=r'''  let cur='',level=3,running=false;
  function makeNum(d){let s='';for(let i=0;i<d;i++)s+=Math.floor(Math.random()*10);if(s[0]==='0')s='1'+s.slice(1);return s;}
  function round(){cur=makeNum(level);$('lvl').textContent='レベル '+level+'桁　覚えて！';
    $('show').textContent=cur;$('ans').style.display='none';$('submit').style.display='none';
    setTimeout(()=>{$('show').textContent='？？？';$('ans').style.display='';$('submit').style.display='';$('ans').value='';$('ans').focus();},900+level*200);}
  function start(){level=3;running=true;$('game').style.display='';$('resultPanel').style.display='none';$('calcBtn').textContent='▶ もう一回';round();}
  function submit(){if(!running)return;if($('ans').value===cur){level++;round();}else{finish();}}
  function finish(){running=false;const best=level-1;$('big').textContent=best;
    const j=best>=9?'天才級🧠':best>=7?'優秀！':best>=5?'平均的':'伸びしろあり';
    $('sub').textContent='正解は「'+cur+'」でした';$('judge').textContent=j;
    SHARE='数字記憶テスト、私は'+best+'桁まで覚えられました🔢（'+j+'）あなたは何桁？';
    $('game').style.display='none';show();}
  $('submit').addEventListener('click',submit);
  $('ans').addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();submit();}});
  function calc(){start();}'''))

# ============================================================
# 10. ストループテスト ★ミニゲーム
# ============================================================
SIMS.append(dict(id='stroop-test', emoji='🎨', cat=CAT,
  title='ストループテスト｜文字でなく“色”を答える脳トレ（無料）｜シミュラボ',
  desc='「あか」と書かれた青い文字…文字の意味ではなく“インクの色”を答える、脳の切り替え力を測るストループテスト。20問の正解数とスピードで脳の柔軟さをチェック（無料・エンタメ）。',
  ogtitle='ストループテスト｜文字でなく色を答える脳トレ', ogdesc='文字の意味ではなくインクの色を答える脳トレ。脳の切り替え力チェック。',
  h1='ストループテスト（色を答える脳トレ）',
  lead='「あか」と書かれているのに文字の色は青…そんなとき、文字の意味ではなく“インクの色”をすばやく答えるテストです。20問の正解数とスピードで、脳の切り替え力をチェック！',
  inputs='''    <h2>🎨 文字の「色」を答えてね</h2>
    <div id="game" style="display:none;text-align:center;background:var(--bg-2,#f6f8fb);border:1px solid var(--line);border-radius:14px;padding:22px;margin-bottom:12px;">
      <div id="word" style="font-size:46px;font-weight:900;min-height:56px;">—</div>
      <div id="btns" style="display:grid;grid-template-columns:1fr 1fr;gap:10px;max-width:320px;margin:16px auto 0;"></div>
      <div id="prog" style="margin-top:12px;color:var(--ink-2);font-weight:800;font-size:13px;">—</div>
    </div>
    <button class="btn btn-primary" id="calcBtn">▶ スタート</button>''',
  result='''      <div class="label">脳の切り替え力</div>
      <div class="big" style="font-size:30px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">正解数</div><div class="v accent" id="correct">—</div></div>
      <div class="stat"><div class="k">かかった時間</div><div class="v" id="time">—</div></div>
      <div class="stat"><div class="k">1問あたり</div><div class="v" id="per">—</div></div></div>''',
  visual='',
  article='''    <div class="note"><strong>遊び方</strong><br>表示された文字の「インクの色」のボタンを押します（文字の意味につられないよう注意！）。全20問の正解数とスピードで判定します。</div>
    <h2>ストループ効果とは</h2>
    <p>「あか」という文字が青色で書かれていると、つい「あか」と答えたくなる——文字の意味と色の情報がぶつかって反応が遅れる現象を「ストループ効果」といいます。この“ついやってしまう”を抑えて正しく答えるには、脳の切り替え（実行機能）が必要。脳トレや集中力チェックに使われます。<b>※エンタメテストです。</b></p>
    <h2>よくある質問</h2>'''+faq([
      ('どこを答えるの？','文字の意味ではなく「文字の色」です。「あお」と赤色で書いてあれば“赤”が正解。'),
      ('速さも関係ある？','正解数を最優先に、同点なら速いほど高評価です。'),
      ('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  js=r'''  const COLS=[['あか','#e23b3b'],['あお','#2f6bff'],['みどり','#19a34a'],['きいろ','#e0a500']];
  let idx=0,correct=0,t0=0,running=false,cur=null;
  function build(){const g=$('btns');g.innerHTML='';COLS.forEach(c=>{const b=document.createElement('button');
    b.className='opt';b.textContent=c[0];b.dataset.col=c[1];b.style.padding='14px';b.style.fontWeight='800';
    g.appendChild(b);});}
  function next(){const wi=Math.floor(Math.random()*4);let ci=Math.floor(Math.random()*4);
    cur=COLS[ci][1];$('word').textContent=COLS[wi][0];$('word').style.color=cur;$('prog').textContent=(idx+1)+' / 20 問　正解 '+correct;}
  function pick(col){if(!running)return;if(col===cur)correct++;idx++;if(idx>=20)finish();else next();}
  function start(){idx=0;correct=0;running=true;$('game').style.display='';$('resultPanel').style.display='none';$('calcBtn').textContent='▶ もう一回';build();t0=performance.now();next();}
  function finish(){running=false;const sec=(performance.now()-t0)/1000;
    const j=correct>=19?'達人級🧠':correct>=16?'とても柔軟！':correct>=12?'平均的':'つられやすいかも';
    $('big').textContent=j;$('sub').textContent='全20問の結果';
    $('correct').textContent=correct+' / 20';$('time').textContent=sec.toFixed(1)+'秒';$('per').textContent=(sec/20).toFixed(2)+'秒';
    SHARE='ストループテスト、私の脳の切り替え力は「'+j+'」でした🎨（20問中'+correct+'正解）あなたは？';
    $('game').style.display='none';show();}
  $('btns').addEventListener('click',e=>{const b=e.target.closest('.opt');if(b)pick(b.dataset.col);});
  function calc(){start();}'''))

# ============================================================
def render():
    for s in SIMS:
        s.setdefault('visual','')
        d=os.path.join(ROOT,'sims',s['id']); os.makedirs(d,exist_ok=True)
        html=(TPL.replace('__TITLE__',s['title']).replace('__DESC__',s['desc'])
              .replace('__OGTITLE__',s['ogtitle']).replace('__OGDESC__',s['ogdesc'])
              .replace('__CAT__',s['cat']).replace('__H1__',s['h1']).replace('__LEAD__',s['lead'])
              .replace('__INPUTS__',s['inputs']).replace('__RESULT__',s['result'])
              .replace('__VISUAL__',s['visual']).replace('__ARTICLE__',s['article'])
              .replace('__JS__',s['js']).replace('__ID__',s['id']))
        with open(os.path.join(d,'index.html'),'w',encoding='utf-8') as f: f.write(html)
        print('created sims/'+s['id'])

if __name__=='__main__':
    render()
    print(f'brain done. {len(SIMS)} sims.')
