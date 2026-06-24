# -*- coding: utf-8 -*-
"""シミュラボ：16タイプ性格診断カテゴリ 10本（相性＋テーマ別、リッチアニメ）。
新カテゴリ slug=type16「16タイプ性格診断」。エンタメ診断（商標配慮で“MBTI公式”は名乗らない）。

import安全（SIMSを定義するだけ。書き込みは __main__ ガード内）。
seo_internal.py / gen_images.py のauto-importに 'gen_sims_type16' を追加して使う。
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
      <div class="viz-wrap" style="margin-top:16px;">__VISUAL__</div>
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
    <h2>💡 こんな診断も見てみたい？</h2>
    <p>あなたの「これ診断してみたい」を送ってください。投票で人気の案から実際に作ります。</p>
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
  const sel = (id) => { const e=$(id); return e.options[e.selectedIndex]; };
  const clamp = (v,a,b) => Math.max(a,Math.min(b,v));
  let SHARE = '', raf = 0;
  function show(){ $('resultPanel').style.display=''; $('resultPanel').scrollIntoView({behavior:'smooth',block:'start'}); }
  try {
__JS__
  } catch(e){ console.error('sim error', e); }
  const sb=$('shareBtn'); if(sb) sb.addEventListener('click', () => window.open('https://twitter.com/intent/tweet?text='+encodeURIComponent(SHARE)+'&url='+encodeURIComponent(location.href)+'&hashtags='+encodeURIComponent('シミュラボ,性格診断'),'_blank','noopener'));
  const cp=$('copyBtn'); if(cp) cp.addEventListener('click', async () => { try{ await navigator.clipboard.writeText(SHARE+'\\n'+location.href); $('copyBtn').textContent='コピーしました ✓'; setTimeout(()=>$('copyBtn').textContent='結果をコピー',1600);}catch{alert(SHARE);} });
})();
</script>
<script src="../../assets/result-fx.js"></script>
<script src="../../assets/share-counter.js"></script>
<script>ShareCounter.initSim({ simId:'__ID__', badgeEl:document.getElementById('shareCount'), shareBtnIds:['shareBtn'] });</script>
</body>
</html>
'''

CAT = '16タイプ性格診断'
VIZ = ('<canvas id="viz" width="500" height="210" style="width:100%;max-width:520px;height:auto;display:block;'
       'margin:0 auto;background:#0b1530;border-radius:14px;"></canvas>')

# 16タイプ（順序固定）とニックネーム
T16 = ['INTJ','INTP','ENTJ','ENTP','INFJ','INFP','ENFJ','ENFP','ISTJ','ISFJ','ESTJ','ESFJ','ISTP','ISFP','ESTP','ESFP']
NICK = {'INTJ':'戦略家','INTP':'探究者','ENTJ':'指揮官','ENTP':'討論家','INFJ':'提唱者','INFP':'夢想家',
        'ENFJ':'主人公','ENFP':'冒険者','ISTJ':'堅実家','ISFJ':'守り手','ESTJ':'統率者','ESFJ':'世話役',
        'ISTP':'職人','ISFP':'芸術家','ESTP':'挑戦者','ESFP':'人気者'}

# 12問（4軸×3問）。各選択肢→そのポール
QUIZ_DATA = [
  ('休日はどっちで充電する？','EI','友達とワイワイ外出','E','家でひとりまったり','I'),
  ('初対面の場では？','EI','自分から話しかける','E','相手が来るのを待つ','I'),
  ('元気が出るのは？','EI','大勢でいる時','E','ひとりの時間','I'),
  ('物事を見るとき重視するのは？','SN','事実・具体','S','可能性・ひらめき','N'),
  ('よく話すのは？','SN','現実的な話','S','アイデアや空想','N'),
  ('新しいことは？','SN','手順どおり確実に','S','とりあえずやってみる','N'),
  ('決めるときの基準は？','TF','論理と正しさ','T','気持ちと人間関係','F'),
  ('相談されたら？','TF','解決策を出す','T','まず共感する','F'),
  ('ほめられて嬉しいのは？','TF','能力・成果','T','人柄・優しさ','F'),
  ('旅行のスタイルは？','JP','計画をしっかり立てる','J','行き当たりばったり','P'),
  ('締め切りは？','JP','早めに終わらせたい','J','ギリギリで燃える','P'),
  ('部屋はどっち？','JP','いつも整理整頓','J','わりと散らかりがち','P'),
]

def quiz_js():
    qd = json.dumps([[q,ax,a,ap,b,bp] for (q,ax,a,ap,b,bp) in QUIZ_DATA], ensure_ascii=False)
    nick = json.dumps(NICK, ensure_ascii=False)
    # calc は window/DOM/IIFEスコープのみ参照（try块内constに依存しない＝確実に動く）
    return '''
  window.__NICK=''' + nick + ''';
  (function(){
    const QDATA=''' + qd + ''';
    const wrap=document.getElementById('quiz');
    QDATA.forEach((q,i)=>{const d=document.createElement('div');d.className='q';
      d.innerHTML='<p class="qt"><b>Q'+(i+1)+'.</b> '+q[0]+'</p><div class="opts">'+
        '<button type="button" class="opt" data-q="'+i+'" data-v="'+q[3]+'">'+q[2]+'</button>'+
        '<button type="button" class="opt" data-q="'+i+'" data-v="'+q[5]+'">'+q[4]+'</button></div>';
      wrap.appendChild(d);});
    wrap.addEventListener('click',e=>{const b=e.target.closest('.opt');if(!b)return;const qi=b.dataset.q;
      wrap.querySelectorAll('.opt[data-q="'+qi+'"]').forEach(o=>o.classList.toggle('on',o===b));
      const p=document.getElementById('prog');if(p)p.textContent=document.querySelectorAll('#quiz .opt.on').length+' / '+QDATA.length+' 問';});
  })();
  function calc(){
    const _n=performance.now();if(window.__lc&&_n-window.__lc<250)return;window.__lc=_n;
    const total=document.querySelectorAll('#quiz .q').length;
    const on=document.querySelectorAll('#quiz .opt.on');
    if(on.length<total){alert('あと'+(total-on.length)+'問！全部の質問に答えてね');
      const qs=document.querySelectorAll('#quiz .q');for(let j=0;j<qs.length;j++){if(!qs[j].querySelector('.opt.on')){qs[j].scrollIntoView({behavior:'smooth',block:'center'});break;}}return;}
    const c={E:0,I:0,S:0,N:0,T:0,F:0,J:0,P:0};on.forEach(b=>c[b.dataset.v]++);
    const code=(c.E>=c.I?'E':'I')+(c.S>=c.N?'S':'N')+(c.T>=c.F?'T':'F')+(c.J>=c.P?'J':'P');
    const sc={EI:c.E/(c.E+c.I),SN:c.S/(c.S+c.N),TF:c.T/(c.T+c.F),JP:c.J/(c.J+c.P)};
    const Q=window.__Q,N=window.__NICK,r=Q.THEME[code]||Q.THEME['ENFP'];
    $('emoji').textContent=r[0];$('big').textContent=r[1];$('code').textContent=code+'（'+N[code]+'タイプ）';
    $('desc').textContent='✨ '+r[2];
    const ar=Q.THEME[r[3]]||Q.THEME['ENFP'];$('aisho').textContent=ar[0]+' '+ar[1];$('aishosub').textContent=Q.META;
    SHARE=Q.SHARE.replace('{name}',r[1]).replace('{code}',code);
    show();window.__viz(sc);
  }
  window.__viz=function(sc){const c=$('viz'),x=c.getContext('2d'),W=c.width,H=c.height;cancelAnimationFrame(raf);
    const axes=[['外向 E','内向 I',sc.EI,'#5dd6ff'],['現実 S','直感 N',sc.SN,'#a78bfa'],['論理 T','情緒 F',sc.TF,'#34d399'],['計画 J','柔軟 P',sc.JP,'#fbbf24']];
    const t0=performance.now(),DUR=1100,bx=86,bw=W-172;
    function frame(n){const p=Math.min(1,(n-t0)/DUR);x.fillStyle='#0b1530';x.fillRect(0,0,W,H);
      axes.forEach((a,i)=>{const y=30+i*((H-44)/4),mid=bx+bw/2;
        x.fillStyle='rgba(255,255,255,.10)';x.fillRect(bx,y,bw,12);
        const target=bx+bw*(1-a[2]),cur=mid+(target-mid)*p;
        x.fillStyle=a[3];x.fillRect(Math.min(mid,cur),y,Math.abs(cur-mid),12);
        x.beginPath();x.arc(cur,y+6,9,0,7);x.fill();
        x.fillStyle='#fff';x.font='11px sans-serif';x.textAlign='right';x.fillText(a[0],bx-8,y+10);
        x.textAlign='left';x.fillText(a[1],bx+bw+8,y+10);});
      if(p<1)raf=requestAnimationFrame(frame);}
    raf=requestAnimationFrame(frame);};
  (function(){var __cb=document.getElementById('calcBtn');if(__cb)__cb.addEventListener('click',calc);})();
'''

QUIZ_INPUTS = ('''    <h2>🧩 12の質問に答えてね</h2>
    <p style="color:var(--ink-2);font-size:13px;margin:-4px 0 6px;">直感でサクサク選んでOK。<span id="prog" style="font-weight:800;color:var(--teal-d);">0 / 12 問</span></p>
    <div id="quiz" class="quiz"></div>
    <button class="btn btn-primary" id="calcBtn" style="margin-top:8px;">結果を見る</button>''')

QUIZ_RESULT = ('''      <div class="label">__RESULTLABEL__</div>
      <div id="emoji" style="font-size:72px;line-height:1.1;">❓</div>
      <div class="big" style="font-size:30px;"><span id="big">—</span></div>
      <div class="sub" id="code">—</div>
      <div class="alert good" id="desc" style="text-align:left;margin-top:14px;">—</div>
      <div class="statline"><div class="stat"><div class="k" id="aishosub">相性が良いのは</div><div class="v accent" id="aisho">—</div></div></div>''')

SIMS = []

def themed(id, emoji, title, h1, lead, ogtitle, ogdesc, resultlabel, metalabel, sharetpl, theme, article):
    js = ('  window.__Q={THEME:' + json.dumps(theme, ensure_ascii=False)
          + ',META:' + json.dumps(metalabel, ensure_ascii=False)
          + ',SHARE:' + json.dumps(sharetpl, ensure_ascii=False) + '};\n'
          + quiz_js())
    SIMS.append(dict(id=id, emoji=emoji, cat=CAT, kind='quiz',
        title=title, desc=lead, ogtitle=ogtitle, ogdesc=ogdesc, h1=h1, lead=lead,
        inputs=QUIZ_INPUTS, result=QUIZ_RESULT.replace('__RESULTLABEL__', resultlabel),
        visual=VIZ, article=article, js=js))

def common_article(intro, what, faqs):
    return ('    <div class="note" style="border-left:4px solid var(--teal)"><strong>これは何？</strong>：'
            + intro + '<br>12問の質問から、性格を4つの軸（外向/内向・現実/直感・論理/情緒・計画/柔軟）で測り、16タイプに分類。さらに各タイプを' + what
            + 'に当てはめます。<b>※当たるも八卦のエンタメ診断です。人を値踏みするものではありません。</b></div>\n'
            '    <h2>4つの軸と16タイプ</h2>\n'
            '    <p>性格を E/I（外向・内向）、S/N（現実・直感）、T/F（論理・情緒）、J/P（計画・柔軟）の4軸で見て、その組み合わせで16タイプに分けます。誰にでも当てはまる万能タイプはなく、どのタイプにも良さがあります。気軽に楽しんでください。</p>\n'
            '    <h2>よくある質問</h2>' + faq(faqs))

# ============================================================
# 2. 動物に例えると診断（動物に例えると 3400/KD0/TP7000）
# ============================================================
themed('doubutsu-type', '🦊',
  '動物に例えると診断｜あなたを動物に例えると？16タイプ性格診断｜シミュラボ',
  'あなたを動物に例えると診断',
  'あなたを動物に例えると、どの動物？12の質問であなたの性格を16タイプに分類し、ぴったりの動物キャラに当てはめます。相性の良い動物も分かります。',
  'あなたを動物に例えると診断｜16タイプ', 'あなたを動物に例えると？16タイプ性格診断。相性の動物も。',
  'あなたを動物に例えると', '相性が良い動物は', 'あなたを動物に例えると「{name}」でした🦊 16タイプ性格診断（{code}）。あなたは何の動物？',
  {'INTJ':('🦉','フクロウ','静かに全体を見渡す戦略家。ひとりで深く考える賢者タイプ。','ESFP'),
   'INTP':('🐈‍⬛','黒猫','気まぐれで探究心のかたまり。自分の興味に正直な研究者。','ENFJ'),
   'ENTJ':('🦁','ライオン','群れを率いる生まれながらのリーダー。決断が速い。','INFP'),
   'ENTP':('🦊','キツネ','機転と口の回る発想家。退屈が大の苦手。','ISFJ'),
   'INFJ':('🐺','オオカミ','物静かだが芯が強い理想家。仲間思いの一匹狼。','ENFP'),
   'INFP':('🦌','シカ','繊細でやさしい夢見がち。自分の世界を大切にする。','ENTJ'),
   'ENFJ':('🐬','イルカ','みんなを笑顔にする人気者リーダー。共感力の塊。','INTP'),
   'ENFP':('🐿️','リス','好奇心いっぱいのムードメーカー。じっとしてられない。','INTJ'),
   'ISTJ':('🐢','カメ','コツコツ堅実、約束は必ず守る。地味だが最強。','ESFP'),
   'ISFJ':('🐑','ヒツジ','献身的でやさしい縁の下の力持ち。','ENTP'),
   'ESTJ':('🐕','イヌ','面倒見が良く規律正しいまとめ役。','ISFP'),
   'ESFJ':('🐰','ウサギ','気配り上手で愛されキャラ。みんなの世話役。','ISTP'),
   'ISTP':('🐈','ネコ','クールで器用な一匹狼。困った時に頼れる。','ESFJ'),
   'ISFP':('🦋','チョウ','感性ゆたかなマイペース芸術家。','ESTJ'),
   'ESTP':('🐆','チーター','スリル大好きな行動派。瞬発力No.1。','INFJ'),
   'ESFP':('🐬','イルカ(陽)','その場を盛り上げる天性のエンタメ役。','INTJ')},
  common_article('あなたの性格をぴったりの動物に例える、エンタメ16タイプ診断です。', '動物',
    [('当たりますか？','エンタメ診断です。話のタネとして楽しんでください。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]))

# ============================================================
# 3. あなたに合うペット診断（ペット相性／犬種・猫診断）
# ============================================================
themed('pet-aisho-type', '🐾',
  'あなたに合うペット診断｜性格でわかる相性ぴったりの犬・猫｜シミュラボ',
  'あなたに合うペット診断',
  '12の質問であなたの性格を16タイプに分類し、相性ぴったりのペット（犬種・猫など）を診断します。これから飼う人のヒントにも。',
  'あなたに合うペット診断｜性格で相性チェック', '性格でわかる、あなたに相性ぴったりのペット（犬・猫）。',
  'あなたに合うペットは', '飼い主タイプの相性は', 'あなたに合うペットは「{name}」でした🐾 16タイプ性格診断（{code}）。あなたは？',
  {'INTJ':('🐈','ロシアンブルー','静かで賢い猫。お互いの距離感を尊重できる相棒。','ESFP'),
   'INTP':('🦎','エキゾチックな小動物','手はかかるが観察が楽しい。探究心を満たす相棒。','ENFJ'),
   'ENTJ':('🐕‍🦺','ジャーマンシェパード','賢く忠実な働き者。主従の信頼でぐんと伸びる。','INFP'),
   'ENTP':('🦜','インコ・オウム','おしゃべりで賢い。退屈させない刺激的な相棒。','ISFJ'),
   'INFJ':('🐩','トイプードル','賢く感受性ゆたか。心を通わせる理想の相棒。','ENFP'),
   'INFP':('🐇','うさぎ','繊細でやさしい。静かに寄り添う癒やしの存在。','ENTJ'),
   'ENFJ':('🐕','ゴールデンレトリバー','人懐っこく愛情深い。家族みんなの人気者。','INTP'),
   'ENFP':('🐶','柴犬(やんちゃ)','好奇心いっぱいで一緒に遊ぶと最高に楽しい。','INTJ'),
   'ISTJ':('🐈','日本猫','手堅く長く付き合える。安定の関係が築ける。','ESFP'),
   'ISFJ':('🐹','ハムスター','小さな世話が好きな人に。けなげで癒やし系。','ENTP'),
   'ESTJ':('🐕','ラブラドール','しつけが入りやすい優等生。頼れる相棒。','ISFP'),
   'ESFJ':('🐱','スコティッシュフォールド','甘え上手で愛されキャラ。世話のしがいあり。','ISTP'),
   'ISTP':('🐍','爬虫類・アクアリウム','手間より観察。クールに愛でる距離感が合う。','ESFJ'),
   'ISFP':('🐈','三毛猫','マイペース同士で心地よい。感性が通じ合う。','ESTJ'),
   'ESTP':('🐕','ボーダーコリー','一緒に走れる運動派。アクティブな毎日に。','INFJ'),
   'ESFP':('🐩','華やかな小型犬','一緒にお出かけが映える。毎日がにぎやか。','INTJ')},
  common_article('あなたの性格から、相性の良いペットを提案するエンタメ診断です。', '相性の良いペット（犬種・猫など）',
    [('飼う前の参考になる？','相性のヒントになりますが、実際の飼育は性格・住環境・時間も含めて検討を。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]))

# ============================================================
# 4. 戦国武将タイプ診断（戦国武将 診断 200/KD0）
# ============================================================
themed('sengoku-busho', '⚔️',
  '戦国武将タイプ診断｜あなたはどの武将？16タイプ性格診断｜シミュラボ',
  '戦国武将タイプ診断',
  '12の質問であなたの性格を16タイプに分類し、似ている戦国武将を診断します。あなたは信長型？家康型？相性の良い武将も分かります。',
  '戦国武将タイプ診断｜あなたはどの武将？', 'あなたに似た戦国武将は？16タイプ性格診断。相性の武将も。',
  'あなたに似た戦国武将は', '相性が良い武将は', 'あなたに似た戦国武将は「{name}」でした⚔️ 16タイプ性格診断（{code}）。あなたは？',
  {'INTJ':('🏯','徳川家康','耐えて好機を待ち天下を取る、長期戦略の達人。','ESFP'),
   'INTP':('📜','黒田官兵衛','冷静沈着な軍師。先を読む知略タイプ。','ENFJ'),
   'ENTJ':('🔥','織田信長','常識を壊す革新のカリスマ。決断と実行の人。','INFP'),
   'ENTP':('🌟','豊臣秀吉','機転と人たらしで成り上がる発想の天才。','ISFJ'),
   'INFJ':('🎋','上杉謙信','義を重んじる理想の武将。信念で動く。','ENFP'),
   'INFP':('🌸','石田三成','義理堅く一途。理想に殉じる純粋タイプ。','ENTJ'),
   'ENFJ':('🤝','前田利家','人望で結ぶ調整役。みんなに好かれる名将。','INTP'),
   'ENFP':('🐉','伊達政宗','派手で行動的な独眼竜。場を沸かせる革新児。','INTJ'),
   'ISTJ':('🛡️','北条氏康','守りを固める堅実派。地盤を盤石にする。','ESFP'),
   'ISFJ':('🌾','直江兼続','主君に尽くす誠実な補佐役。','ENTP'),
   'ESTJ':('⚙️','武田信玄','規律と組織で勝つ統率の名将。','ISFP'),
   'ESFJ':('🏵️','今川義元','格式と人脈を重んじる名門の当主。','ISTP'),
   'ISTP':('🗡️','本多忠勝','寡黙で最強の戦巧者。実力で語る職人武将。','ESFJ'),
   'ISFP':('🎭','古田織部','美を追う数寄者。独自の感性を貫く。','ESTJ'),
   'ESTP':('⚡','真田幸村','果敢に突撃する戦の華。スリルに強い猛将。','INFJ'),
   'ESFP':('🎏','加藤清正','豪快で人気者の勇将。みんなを盛り上げる。','INTJ')},
  common_article('あなたの性格に似た戦国武将を当てはめるエンタメ診断です。', '似ている戦国武将',
    [('史実に基づく？','武将像は通説・イメージに基づくエンタメです。諸説あります。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]))

# ============================================================
# 5. 三国志武将タイプ診断（三国志 診断 KD1）
# ============================================================
themed('sangokushi-type', '🐉',
  '三国志 武将タイプ診断｜あなたはどの英雄？16タイプ性格診断｜シミュラボ',
  '三国志 武将タイプ診断',
  '12の質問であなたの性格を16タイプに分類し、似ている三国志の英雄を診断します。あなたは諸葛亮型？曹操型？相性の良い武将も。',
  '三国志 武将タイプ診断｜あなたはどの英雄？', 'あなたに似た三国志の英雄は？16タイプ性格診断。',
  'あなたに似た三国志の英雄は', '相性が良い英雄は', 'あなたに似た三国志の英雄は「{name}」でした🐉 16タイプ性格診断（{code}）。あなたは？',
  {'INTJ':('🪶','諸葛亮','天下三分を描く知略の軍師。冷静沈着な戦略家。','ESFP'),
   'INTP':('📖','司馬懿','機を待ち最後に勝つ忍耐の知将。','ENFJ'),
   'ENTJ':('🗡️','曹操','乱世の奸雄、圧倒的な決断と実行のカリスマ。','INFP'),
   'ENTP':('🎯','周瑜','才気あふれる若き名将。発想と弁舌の人。','ISFJ'),
   'INFJ':('🤲','劉備','徳で人を集める理想のリーダー。','ENFP'),
   'INFP':('🍑','魯粛','和を尊ぶ誠実な調整役。理想を信じる。','ENTJ'),
   'ENFJ':('🔥','孫策','人望と勢いで国を興す若き覇王。','INTP'),
   'ENFP':('🌪️','馬超','勇猛果敢で情熱的な西涼の錦馬超。','INTJ'),
   'ISTJ':('🛡️','趙雲','忠義と堅実さを兼ねた完璧な武将。','ESFP'),
   'ISFJ':('🌿','黄忠','老いてなお誠実、堅実な老将。','ENTP'),
   'ESTJ':('⚙️','孫権','組織を固め国を治める統治の人。','ISFP'),
   'ESFJ':('🤝','魯粛(和)','人の和を重んじる外交の名手。','ISTP'),
   'ISTP':('🏹','呂布','最強の武力を誇る孤高の猛将。','ESFJ'),
   'ISFP':('🎶','姜維','信念を貫く一途な後継者。','ESTJ'),
   'ESTP':('🐯','張飛','豪快で猪突猛進、戦場の暴れ虎。','INFJ'),
   'ESFP':('🍶','関羽','義に厚く人気絶大の豪傑。','INTJ')},
  common_article('あなたの性格に似た三国志の英雄を当てはめるエンタメ診断です。', '似ている三国志の英雄',
    [('史実に基づく？','人物像は『三国志演義』等のイメージに基づくエンタメです。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]))

# ============================================================
# 6. お酒タイプ診断（お酒 性格診断 30/KD0/TP8500）
# ============================================================
themed('osake-type', '🍶',
  'お酒タイプ診断｜あなたをお酒に例えると？16タイプ性格診断｜シミュラボ',
  'あなたをお酒に例えると診断',
  '12の質問であなたの性格を16タイプに分類し、ぴったりのお酒に例えます。あなたはシャンパン型？日本酒型？相性の良いお酒も分かります。',
  'あなたをお酒に例えると診断｜16タイプ', 'あなたを お酒に例えると？性格でわかる16タイプ診断。',
  'あなたをお酒に例えると', '相性が良いお酒は', 'あなたをお酒に例えると「{name}」でした🍶 16タイプ性格診断（{code}）。あなたは？',
  {'INTJ':('🥃','シングルモルト','奥深く一本筋の通った通好み。静かな存在感。','ESFP'),
   'INTP':('🧪','クラフトジン','独創的で個性派。香りに探究心がにじむ。','ENFJ'),
   'ENTJ':('🍷','フルボディの赤ワイン','力強く重厚。リーダーの貫禄。','INFP'),
   'ENTP':('🍸','カクテル','自在に変化する発想型。話題の中心。','ISFJ'),
   'INFJ':('🍶','純米大吟醸','繊細で奥ゆかしい理想派。','ENFP'),
   'INFP':('🍑','梅酒','やさしく甘い癒やし系。マイペース。','ENTJ'),
   'ENFJ':('🍾','シャンパン','場を華やかにする祝福の人気者。','INTP'),
   'ENFP':('🍹','トロピカルカクテル','陽気で楽しい盛り上げ役。','INTJ'),
   'ISTJ':('🍺','ラガービール','王道で安定、誰からも信頼される定番。','ESFP'),
   'ISFJ':('🍵','甘酒','体にやさしいほっこり系。献身的。','ENTP'),
   'ESTJ':('🥂','スパークリング(辛口)','きりっと締まる統率派。','ISFP'),
   'ESFJ':('🍯','はちみつ酒','まろやかで愛され系。みんなに優しい。','ISTP'),
   'ISTP':('🍶','本格焼酎','飾らず実直、奥が深い職人肌。','ESFJ'),
   'ISFP':('🍇','自然派ワイン','個性と感性を大切にする芸術派。','ESTJ'),
   'ESTP':('🥃','テキーラ','勢いとスリルの行動派。場を沸かす。','INFJ'),
   'ESFP':('🍻','生ビールで乾杯','とにかく明るい宴会の主役。','INTJ')},
  common_article('あなたの性格をお酒に例えるエンタメ診断です（飲酒は20歳から・適量で）。', 'ぴったりのお酒',
    [('お酒が飲めなくても？','イメージを楽しむ診断なので大丈夫です。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]))

# ============================================================
# 7. 色に例えると診断（色 性格診断 150/KD0）
# ============================================================
themed('iro-type', '🎨',
  'あなたを色に例えると診断｜性格でわかるパーソナルカラー｜シミュラボ',
  'あなたを色に例えると診断',
  '12の質問であなたの性格を16タイプに分類し、ぴったりの色（パーソナルカラー）に例えます。あなたの色は何色？相性の色も分かります。',
  'あなたを色に例えると診断｜16タイプ', 'あなたを 色に例えると？性格でわかる16タイプ診断。',
  'あなたを色に例えると', '相性が良い色は', 'あなたを色に例えると「{name}」でした🎨 16タイプ性格診断（{code}）。あなたは何色？',
  {'INTJ':('🟦','ネイビー','知的で落ち着いた信頼の色。芯のある人。','🟧'),
   'INTP':('🟪','バイオレット','独創的でミステリアス。探究の色。','🟨'),
   'ENTJ':('🟥','クリムゾンレッド','情熱と決断のリーダーカラー。','🟩'),
   'ENTP':('🟧','オレンジ','活発で発想ゆたか。会話が弾む色。','🟦'),
   'INFJ':('🟦','インディゴ','深く静かな理想の色。','🟧'),
   'INFP':('🩵','ラベンダー','やさしく繊細な癒やしの色。','🟥'),
   'ENFJ':('🩷','コーラルピンク','あたたかく人を惹きつける色。','🟪'),
   'ENFP':('🟨','サンイエロー','明るく好奇心いっぱいの色。','🟦'),
   'ISTJ':('🟫','ブラウン','堅実で安定、地に足のついた色。','🩷'),
   'ISFJ':('🤍','アイボリー','やわらかく献身的な包容の色。','🟧'),
   'ESTJ':('⬛','チャコール','規律と統率の頼れる色。','🩵'),
   'ESFJ':('🩷','ローズピンク','愛され上手なあたたかい色。','🩶'),
   'ISTP':('🩶','スチールグレー','クールで実用的な職人の色。','🩷'),
   'ISFP':('🟩','セージグリーン','感性ゆたかで穏やかな色。','⬛'),
   'ESTP':('🟥','ビビッドレッド','勢いと行動力の刺激的な色。','🟦'),
   'ESFP':('🌈','レインボー','華やかで楽しい主役の色。','🟦')},
  common_article('あなたの性格を色（パーソナルカラー）に例えるエンタメ診断です。', 'ぴったりの色',
    [('似合う服の色とは違う？','こちらは性格イメージの色です。骨格・肌診断とは別物です。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]))

# ============================================================
# 8. 花に例えると診断（花 診断 250/KD0）
# ============================================================
themed('hana-type', '🌸',
  'あなたを花に例えると診断｜性格でわかるあなたの花｜シミュラボ',
  'あなたを花に例えると診断',
  '12の質問であなたの性格を16タイプに分類し、ぴったりの花に例えます。あなたを花に例えると何の花？花言葉と相性の花も分かります。',
  'あなたを花に例えると診断｜16タイプ', 'あなたを 花に例えると？性格でわかる16タイプ診断。',
  'あなたを花に例えると', '相性が良い花は', 'あなたを花に例えると「{name}」でした🌸 16タイプ性格診断（{code}）。あなたは何の花？',
  {'INTJ':('🌙','月下美人','静かに咲く神秘の花。気高く独自の世界。','🌻'),
   'INTP':('🌿','アザミ','独特の魅力をもつ探究の花。','🌼'),
   'ENTJ':('🌹','バラ','気高く堂々、リーダーの花。','🌷'),
   'ENTP':('🌻','ヒマワリ(発想)','明るく活発、好奇心の花。','🪻'),
   'INFJ':('🪷','ハス','清らかで芯の強い理想の花。','🌸'),
   'INFP':('🌷','スズラン','繊細でやさしい純粋の花。','🌹'),
   'ENFJ':('🌸','サクラ','人を惹きつけるあたたかな花。','🌿'),
   'ENFP':('🌼','コスモス','風に揺れる自由で陽気な花。','🌙'),
   'ISTJ':('🎍','松','堅実で長持ち、信頼の常緑。','🌻'),
   'ISFJ':('🌾','カスミソウ','主役を引き立てる献身の花。','🌻'),
   'ESTJ':('🌵','サボテン(統率)','どんな環境でも揺るがない強さ。','🌷'),
   'ESFJ':('🌺','ハイビスカス','あたたかく愛される人気の花。','🪻'),
   'ISTP':('🍀','クローバー','飾らず実用的、幸運を呼ぶ草花。','🌺'),
   'ISFP':('🪻','ラベンダー','感性ゆたかで穏やかな癒やしの花。','🌵'),
   'ESTP':('🌶️','ブーゲンビリア','情熱的で勢いのある花。','🪷'),
   'ESFP':('🌻','ヒマワリ','太陽みたいに明るい主役の花。','🌙')},
  common_article('あなたの性格を花に例えるエンタメ診断です。', 'ぴったりの花',
    [('花言葉も分かる？','タイプの花のイメージを楽しむ診断です。花言葉は諸説あります。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]))

# ============================================================
# 9. 四字熟語であらわすあなた診断（四字熟語 診断 100/KD0）
# ============================================================
themed('yoji-jukugo-type', '🀄',
  '四字熟語であらわすあなた診断｜性格を四字熟語で｜16タイプ｜シミュラボ',
  '四字熟語であらわすあなた診断',
  '12の質問であなたの性格を16タイプに分類し、あなたをあらわす四字熟語を診断します。あなたの座右の銘になるかも。相性の四字熟語も。',
  '四字熟語であらわすあなた診断｜16タイプ', 'あなたを四字熟語であらわすと？性格でわかる16タイプ診断。',
  'あなたをあらわす四字熟語は', '相性が良いのは', 'あなたをあらわす四字熟語は「{name}」でした🀄 16タイプ性格診断（{code}）。あなたは？',
  {'INTJ':('♟️','深謀遠慮','先の先まで読み抜く戦略家。','🎉'),
   'INTP':('🔬','独立独歩','人に流されず我が道を究める。','🤝'),
   'ENTJ':('👑','勇往邁進','迷わず突き進むリーダー。','🌱'),
   'ENTP':('💡','臨機応変','どんな場面も発想で切り抜ける。','🛡️'),
   'INFJ':('🕊️','初志貫徹','理想を最後まで貫く信念の人。','🎈'),
   'INFP':('🌷','純真無垢','まっすぐで澄んだ心の持ち主。','👑'),
   'ENFJ':('🤝','和衷協同','みんなの心を一つにまとめる。','🔬'),
   'ENFP':('🎈','自由奔放','枠にとらわれず楽しむ冒険者。','♟️'),
   'ISTJ':('🧱','質実剛健','飾らず堅実、ぶれない芯。','🎉'),
   'ISFJ':('🌾','一生懸命','誰かのため黙々と尽くす。','💡'),
   'ESTJ':('⚙️','率先垂範','自ら手本を示す統率者。','🌷'),
   'ESFJ':('💞','温故知新','人を大切に和を育む。','🛠️'),
   'ISTP':('🛠️','一意専心','一つのことを極める職人。','💞'),
   'ISFP':('🎨','天真爛漫','感性のまま自然体で輝く。','⚙️'),
   'ESTP':('⚡','電光石火','スピードと勢いで勝負。','🕊️'),
   'ESFP':('🎉','明朗快活','明るく場を照らすムードメーカー。','♟️')},
  common_article('あなたの性格をあらわす四字熟語を選ぶエンタメ診断です。', 'あなたをあらわす四字熟語',
    [('座右の銘にできる？','気に入ったらぜひ。エンタメ診断ですが背中を押す言葉になれば。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]))

# ============================================================
# 10. 天職・向いてる仕事診断（mbti 仕事 450/KD0/TP1500）
# ============================================================
themed('tenshoku-type', '💼',
  '天職・向いてる仕事診断｜性格でわかる適職｜16タイプ｜シミュラボ',
  '天職・向いてる仕事診断',
  '12の質問であなたの性格を16タイプに分類し、向いてる仕事の方向性（天職タイプ）を診断します。強みと相性の良いタイプも分かります。',
  '天職・向いてる仕事診断｜16タイプの適職', '性格でわかる、あなたに向いてる仕事の方向性。16タイプ診断。',
  'あなたに向いてる仕事は', '一緒に働くと良いのは', 'あなたの天職タイプは「{name}」でした💼 16タイプ性格診断（{code}）。あなたは？',
  {'INTJ':('🧭','戦略・企画タイプ','長期で構想を練る仕事が天職。コンサル・経営企画など。','🎤'),
   'INTP':('🔬','研究・分析タイプ','深く突き詰める仕事に強い。研究・エンジニア・分析など。','🤝'),
   'ENTJ':('🚀','経営・推進タイプ','人と組織を動かすリーダー職。経営・事業責任者など。','🎨'),
   'ENTP':('💡','起業・発明タイプ','ゼロから生み出す仕事が向く。起業・新規事業・企画。','🛡️'),
   'INFJ':('🌱','支援・育成タイプ','人の成長を支える仕事。カウンセラー・人事・教育など。','🎉'),
   'INFP':('✍️','創作・表現タイプ','想いを形にする仕事。ライター・クリエイター・デザイン。','🚀'),
   'ENFJ':('🎤','教育・リーダータイプ','人を導き巻き込む仕事。講師・マネージャー・広報。','🔬'),
   'ENFP':('🎨','企画・PRタイプ','アイデアと発信が武器。マーケ・PR・プランナー。','🧭'),
   'ISTJ':('📊','管理・実務タイプ','正確で堅実な仕事が天職。経理・法務・品質管理など。','🎉'),
   'ISFJ':('🤲','サポート・ケアタイプ','人を支える仕事。事務・看護・接客・総務など。','💡'),
   'ESTJ':('🏗️','運営・マネジメントタイプ','組織を回す仕事に強い。管理職・運営・現場長など。','🎨'),
   'ESFJ':('🤝','接客・調整タイプ','人と関わる仕事が天職。営業・接客・人事・販売など。','🛠️'),
   'ISTP':('🛠️','技術・職人タイプ','手を動かし極める仕事。エンジニア・整備・技術職。','🤝'),
   'ISFP':('🎨','デザイン・感性タイプ','美と感性を活かす仕事。デザイナー・美容・調理など。','🏗️'),
   'ESTP':('📈','営業・現場タイプ','スピードと交渉が武器。営業・トレーダー・現場職。','🌱'),
   'ESFP':('🎉','接客・エンタメタイプ','人を楽しませる仕事が天職。販売・接客・イベント。','🧭')},
  common_article('あなたの性格から向いてる仕事の方向性を提案するエンタメ診断です。', '向いてる仕事（天職タイプ）',
    [('転職の参考になる？','方向性のヒントとして。実際は経験・希望・市場も含めて検討を。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]))

# ============================================================
# 1. 16タイプ相性診断（mbti 相性 118000/KD0）★ — 2タイプ選択式
# ============================================================
def compat_options():
    return ''.join(f'<option value="{c}">{c}（{NICK[c]}）</option>' for c in T16)

NICK_JS = json.dumps(NICK, ensure_ascii=False)
EMOJI16 = {'INTJ':'🦉','INTP':'🐈‍⬛','ENTJ':'🦁','ENTP':'🦊','INFJ':'🐺','INFP':'🦌','ENFJ':'🐬','ENFP':'🐿️',
           'ISTJ':'🐢','ISFJ':'🐑','ESTJ':'🐕','ESFJ':'🐰','ISTP':'🐈','ISFP':'🦋','ESTP':'🐆','ESFP':'🎉'}

SIMS.append(dict(id='aisho-16type', emoji='💞', cat=CAT, kind='compat',
  title='16タイプ相性診断｜性格タイプの相性をチェック（MBTIタイプ対応）｜シミュラボ',
  desc='自分と相手の性格タイプ（16タイプ・MBTI対応）を選ぶだけで、相性の良さを%とコメントで診断する無料ツール。恋愛・友達・仕事の相性チェックに。',
  ogtitle='16タイプ相性診断｜性格タイプの相性チェック', ogdesc='自分と相手の16タイプを選ぶだけで相性を%で診断。恋愛・友達・仕事に。',
  h1='16タイプ相性診断',
  lead='自分と相手の性格タイプ（16タイプ／MBTI対応）を選ぶだけ。相性の良さを％とコメントで診断します。恋愛・友達・職場の相性チェックに。タイプが分からない人は他の診断で調べてから戻ってきてね。',
  inputs='''    <h2>💞 2人のタイプを選ぶ</h2>
    <div class="row"><div class="field"><label>あなたのタイプ</label><select id="me">''' + compat_options() + '''</select></div>
    <div class="field"><label>相手のタイプ</label><select id="you">''' + compat_options() + '''</select></div></div>
    <p style="color:var(--ink-2);font-size:13px;">タイプが分からない？　<a href="../doubutsu-type/index.html" style="font-weight:800;">▶ 動物に例えると診断</a> で調べられます。</p>
    <button class="btn btn-primary" id="calcBtn">相性を見る</button>''',
  result='''      <div class="label">2人の相性は</div>
      <div class="big"><span id="big">0</span><span class="unit">％</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="desc" style="text-align:left;margin-top:14px;">—</div>
      <div class="statline"><div class="stat"><div class="k">関係のヒント</div><div class="v accent" id="rel" style="font-size:15px;">—</div></div></div>''',
  visual=('<canvas id="viz" width="500" height="180" style="width:100%;max-width:520px;height:auto;display:block;'
          'margin:0 auto;background:#0b1530;border-radius:14px;"></canvas>'),
  article='''    <div class="note" style="border-left:4px solid var(--teal)"><strong>これは何？</strong>：自分と相手の性格タイプ（16タイプ／MBTI対応）から、相性の目安を％で出すエンタメ診断です。4つの軸（外向/内向・現実/直感・論理/情緒・計画/柔軟）の組み合わせから、噛み合いやすさ・補い合いやすさを計算します。<b>※相性に正解はありません。話のタネとして楽しんでください。</b></div>
    <h2>相性の考え方</h2>
    <p>一般に、価値観の土台（現実派か直感派か＝S/N）が近いと話が通じやすく、判断軸（論理か情緒か＝T/F）は似ても補い合っても良い関係になります。外向/内向（E/I）は違うほどバランスが取れることも。あくまで傾向で、実際の相性は一人ひとり違います。</p>
    <h2>タイプが分からないときは</h2>
    <p>自分や相手のタイプが分からないときは、<a href="../doubutsu-type/index.html">動物に例えると診断</a>や<a href="../tenshoku-type/index.html">天職診断</a>など、当サイトの16タイプ診断で先に調べてください。結果のアルファベット4文字（例：ENFP）がそのままタイプです。</p>
    <h2>よくある質問</h2>''' + faq([
      ('恋愛だけの相性？','恋愛・友情・仕事すべての“噛み合いやすさ”の目安です。'),
      ('相性が低いとダメ？','いいえ。違いは伸びしろ。理解し合えば良い関係になれます。'),
      ('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  js=('  window.__NICK=' + NICK_JS + ';\n  window.__EM=' + json.dumps(EMOJI16, ensure_ascii=False) + ''';
  window.__score=function(a,b){
    let s=50;const ax=[[0,'E','I'],[1,'S','N'],[2,'T','F'],[3,'J','P']];
    // S/N（世界観）が同じ＝大きく加点、違うと減点
    s += (a[1]===b[1]) ? 16 : -10;
    // T/F（判断軸）は同じでも違っても可。違いは補完として小さく加点
    s += (a[2]===b[2]) ? 8 : 6;
    // E/I（活力）は違うとバランス＝加点
    s += (a[0]!==b[0]) ? 9 : 4;
    // J/P（生活）は同じだと噛み合う
    s += (a[3]===b[3]) ? 9 : 2;
    // 同一タイプはやや加点、相補(全反転)もロマン加点
    if(a===b) s+=6;
    let rev=''; for(let i=0;i<4;i++) rev += (a[i]===ax[i][1]?ax[i][2]:ax[i][1]);
    if(b===rev) s+=8;
    // 決定論的なゆらぎ
    let h=0; const t=a+b; for(let i=0;i<t.length;i++){h=(h*31+t.charCodeAt(i))>>>0;}
    s += (h%9)-4;
    return clamp(Math.round(s),28,99);
  }
  function calc(){var _n=performance.now();if(window.__lc&&_n-window.__lc<250)return;window.__lc=_n;
    const a=$('me').value,b=$('you').value,sv=window.__score(a,b),NICK=window.__NICK;
    $('sub').textContent=a+'（'+NICK[a]+'）× '+b+'（'+NICK[b]+'）';
    let msg,rel;
    if(sv>=85){msg='最高クラスの相性！一緒にいるほど自然体でいられる名コンビ。';rel='ベストパートナー';}
    else if(sv>=70){msg='とても good な相性。違いも楽しめる心地よい関係です。';rel='good な関係';}
    else if(sv>=55){msg='バランス型。お互いを少し歩み寄ると、ぐっと深まります。';rel='伸びしろ大';}
    else if(sv>=42){msg='違いが多めの刺激的な関係。理解し合えれば最強の補完に。';rel='補い合う関係';}
    else{msg='正反対だからこそ学べることが多い関係。違いを面白がって。';rel='ないものを補う';}
    $('desc').textContent='💞 '+msg;$('rel').textContent=rel;$('big').textContent=sv;
    SHARE='16タイプ相性診断、'+a+'×'+b+'の相性は'+sv+'%（'+rel+'）でした💞 あなたたちは何%？';
    show();window.__cviz(a,b,sv);}
  window.__cviz=function(a,b,sv){const c=$('viz'),x=c.getContext('2d'),W=c.width,H=c.height;cancelAnimationFrame(raf);
    const t0=performance.now(),DUR=1300,lx=W*0.22,rx=W*0.78,cy=H*0.42;
    const hearts=[];for(let i=0;i<14;i++)hearts.push({t:Math.random(),sp:0.3+Math.random()*0.6,off:(Math.random()-0.5)*60});
    function frame(n){const p=Math.min(1,(n-t0)/DUR);x.fillStyle='#0b1530';x.fillRect(0,0,W,H);
      // two emblems moving slightly together
      const ax=lx+(W*0.5-lx)*0.12*p, bx2=rx-(rx-W*0.5)*0.12*p;
      x.font='44px sans-serif';x.textAlign='center';x.textBaseline='middle';
      x.fillText(window.__EM[a]||'🙂',ax,cy);x.fillText(window.__EM[b]||'🙂',bx2,cy);
      x.font='12px sans-serif';x.fillStyle='#cbd5e1';x.fillText(a,ax,cy+38);x.fillText(b,bx2,cy+38);
      // link line + rising hearts
      x.strokeStyle='rgba(255,120,160,'+(0.3+0.5*p)+')';x.lineWidth=2;x.beginPath();x.moveTo(ax+22,cy);x.lineTo(bx2-22,cy);x.stroke();
      hearts.forEach(h=>{const hp=(h.t+n*0.0004*h.sp)%1;const hx=(ax+bx2)/2+h.off*(1-hp);const hy=cy-hp*70;
        x.globalAlpha=(1-hp)*p;x.font=(10+hp*10)+'px sans-serif';x.fillText('💗',hx,hy);x.globalAlpha=1;});
      // score meter
      const by=H-26,bw=W-120,bxx=60;x.fillStyle='rgba(255,255,255,.1)';x.fillRect(bxx,by,bw,12);
      const grad=x.createLinearGradient(bxx,0,bxx+bw,0);grad.addColorStop(0,'#fb7185');grad.addColorStop(1,'#6366f1');
      x.fillStyle=grad;x.fillRect(bxx,by,bw*(sv/100)*p,12);
      x.fillStyle='#fff';x.font='bold 13px sans-serif';x.textAlign='center';x.fillText('相性 '+Math.round(sv*p)+'%',W/2,by-8);
      if(p<1)raf=requestAnimationFrame(frame);}
    raf=requestAnimationFrame(frame);};
  (function(){var __cb=document.getElementById('calcBtn');if(__cb)__cb.addEventListener('click',calc);})();
''')))

# ============================================================
def render():
    for s in SIMS:
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
    print(f'type16 done. {len(SIMS)} sims.')
