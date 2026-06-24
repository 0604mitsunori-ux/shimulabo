# -*- coding: utf-8 -*-
"""シミュラボ：Typeless訴求の「リッチアニメ×バズ」音声入力シミュ 10本。
結果欄にcanvasアニメ＋Typelessアフィリ CTA。slug=voice（音声入力・時短）。

import安全（SIMSを定義するだけ。書き込みは __main__ ガード内）。
seo_internal.py / gen_images.py のauto-importに 'gen_sims_typeless' を追加して使う。
"""
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

CTA = '''      <a class="cta-box" href="https://www.typeless.com/?via=44144c" target="_blank" rel="nofollow sponsored noopener" style="display:block;text-decoration:none;text-align:left;margin-top:20px;background:linear-gradient(135deg,#eef2ff,#f5f3ff);border:1.5px solid #a5b4fc;border-radius:14px;padding:18px;">
        <div style="font-weight:900;color:#4f46e5;font-size:15px;">🎙️ その時間、「話すだけ」で取り戻せます。</div>
        <div style="font-size:13px;color:var(--ink-2);margin-top:6px;line-height:1.7;">打つのをやめて話す時代。中でも<strong>今いちばんおすすめなのが「Typeless」</strong>です。AIが「えーと」などの言い淀みも自動でカット・整文し、議事録・メール・記事・日記まで一気に仕上げます。タイピングに戻れなくなる人が続出。</div>
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
      <div class="viz-wrap" style="margin-top:16px;">__VISUAL__</div>
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
  const clamp = (v,a,b) => Math.max(a,Math.min(b,v));
  let SHARE = '';
  function anim(el, from, to, dur, dec){ const t0=performance.now(); (function s(n){const p=Math.min(1,(n-t0)/dur);const e=1-Math.pow(1-p,3);const v=from+(to-from)*e;el.textContent=(dec!=null?v.toFixed(dec):Math.round(v).toLocaleString('ja-JP'));if(p<1)requestAnimationFrame(s);})(performance.now()); }
  function show(){ $('resultPanel').style.display=''; $('resultPanel').scrollIntoView({behavior:'smooth',block:'start'}); }
  try {
__JS__
  } catch(e){ console.error('sim error', e); }
  const cb=$('calcBtn'); if(cb) cb.addEventListener('click', calc);
  const sb=$('shareBtn'); if(sb) sb.addEventListener('click', () => window.open('https://twitter.com/intent/tweet?text='+encodeURIComponent(SHARE)+'&url='+encodeURIComponent(location.href)+'&hashtags='+encodeURIComponent('シミュラボ,音声入力'),'_blank','noopener'));
  const cp=$('copyBtn'); if(cp) cp.addEventListener('click', async () => { try{ await navigator.clipboard.writeText(SHARE+'\\n'+location.href); $('copyBtn').textContent='コピーしました ✓'; setTimeout(()=>$('copyBtn').textContent='結果をコピー',1600);}catch{alert(SHARE);} });
})();
</script>
<script src="../../assets/result-fx.js"></script>
<script src="../../assets/share-counter.js"></script>
<script>ShareCounter.initSim({ simId:'__ID__', badgeEl:document.getElementById('shareCount'), shareBtnIds:['shareBtn'] });</script>
</body>
</html>
'''

V = '音声入力・時短'
TYPELESS = '<div class="note" style="margin-top:14px;"><strong>結論：今いちばんおすすめの音声入力ツールは「Typeless」</strong><br>音声入力ツールは数あれど、精度・整文（言い淀みの自動カット）・日本語の自然さで頭ひとつ抜けているのがTypelessです。上の試算ぶんの時間を、現実に取り戻せます。</div>'

def viz(w=520,h=210,mx=540,id='viz',xtra=''):
    return (f'<canvas id="{id}" width="{w}" height="{h}" style="width:100%;max-width:{mx}px;height:auto;'
            f'display:block;margin:0 auto;background:#0b1530;border-radius:14px;{xtra}"></canvas>')

SIMS=[]
def add(**k): SIMS.append(k)

# ============================================================
# 1. ボイスメモ文字起こし時短（ボイスメモ 文字起こし 19000/KD0）
# ============================================================
add(id='voice-memo', cat=V, emoji='🎙️',
  title='ボイスメモ文字起こし時短シミュレーター｜手作業と音声入力どっちが速い？｜シミュラボ',
  desc='スマホのボイスメモ（録音）を手で文字起こしすると何時間かかるか、AI音声入力ならどれだけ速いかを比較する無料シミュレーター。録音時間を入れるだけで、聞き返し＋打ち込みの時間と削減額が分かります。',
  ogtitle='ボイスメモ文字起こし時短シミュ｜手作業 vs 音声入力', ogdesc='録音を手で文字起こしする時間とAI音声入力の差を可視化。',
  h1='ボイスメモ文字起こし時短シミュレーター',
  lead='スマホに溜まったボイスメモ、手で文字起こしすると何時間かかると思いますか？録音時間を入れると、聞き返し＋打ち込みの「手作業の時間」と、AI音声入力での時間を比べて可視化します。',
  inputs='''    <h2>🎙️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>録音時間 <span class="hint">（分）</span></label><input type="number" id="rec" value="60" min="0" inputmode="numeric"></div>
    <div class="field"><label>あなたの時給 <span class="hint">（円）</span></label><input type="number" id="wage" value="2500" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">手作業の時間を見る</button>''',
  result='''      <div class="label">手で文字起こしすると</div>
      <div class="big"><span id="big">0</span><span class="unit">時間</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">AI音声入力なら</div><div class="v accent" id="ai">—</div></div>
      <div class="stat"><div class="k">短縮できる時間</div><div class="v" id="save">—</div></div>
      <div class="stat"><div class="k">時給換算で</div><div class="v" id="money">—</div></div></div>''',
  visual=viz(520,200,540),
  article='''    <div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：録音を手で文字起こしすると、ふつう<b>録音時間の約4〜5倍</b>かかります（聞き返し・一時停止・打ち込みのため）。AI音声入力なら<b>録音とほぼ同じ時間＋軽い修正</b>で完了。録音が長いほど差は開きます。</div>
    <h2>ボイスメモを文字起こしする方法</h2>
    <p>会議・取材・授業・思いつき…スマホのボイスメモは便利ですが、「あとで文字にする」のが大変。手作業だと、再生→止める→打つ→巻き戻す、の繰り返しで録音時間の何倍もかかります。AI音声認識（自動文字起こし）を使えば、録音を読み込むだけで一気にテキスト化できます。</p>
    <h2>聞き返す時間こそ、人生のムダ</h2>
    <p>録音は「録った」だけでは使えません。文字にして初めて検索でき、引用でき、資料になります。その「文字にする時間」を手作業で払い続けるのは、もったいない。話した内容がそのままテキストになるなら、聞き返す時間はまるごと不要になります。</p>'''+TYPELESS+'''
    <h2>よくある質問</h2>'''+faq([
      ('手作業だと本当に4〜5倍かかる？','一般に「音声1分＝文字起こし4〜5分」が業界の目安です。専門用語や複数人の会話だとさらに増えます。'),
      ('精度は大丈夫？','近年のAIは高精度で、固有名詞だけ直せばOKなレベル。Typelessは言い淀みの自動カットや整文にも対応します。'),
      ('データは送信されますか？','いいえ。本シミュレーターの計算はすべてブラウザ内で完結します。')]),
  js=r'''  let raf=0;
  function calc(){const rec=Math.max(0,+$('rec').value||0),w=Math.max(0,+$('wage').value||0);
    const manualMin=rec*4.5, aiMin=rec*1.2, saveMin=Math.max(0,manualMin-aiMin), money=saveMin/60*w;
    $('sub').textContent=`録音${num(rec)}分・時給${num(w)}円`;
    $('ai').textContent=num(aiMin)+'分';$('save').textContent=num(saveMin)+'分';$('money').textContent=yen(money);
    SHARE=`ボイスメモ文字起こしシミュ、録音${num(rec)}分を手作業だと約${(manualMin/60).toFixed(1)}時間…音声入力なら${num(aiMin)}分でした🎙️`;
    show();anim($('big'),0,manualMin/60,900,1);startViz(manualMin,aiMin);}
  function startViz(manualMin,aiMin){const c=$('viz'),x=c.getContext('2d'),W=c.width,H=c.height;cancelAnimationFrame(raf);
    const maxT=Math.max(manualMin,1),t0=performance.now(),DUR=2600;
    function frame(n){const p=Math.min(1,(n-t0)/DUR);x.fillStyle='#0b1530';x.fillRect(0,0,W,H);
      // waveform top
      x.strokeStyle='rgba(125,233,255,.5)';x.lineWidth=2;x.beginPath();
      for(let i=0;i<W;i+=4){const a=Math.sin(i*0.08+n*0.006)*Math.sin(i*0.021+1)*22*(0.4+0.6*Math.abs(Math.sin(i*0.03)));x.lineTo(i,40+a);}x.stroke();
      x.fillStyle='rgba(255,255,255,.85)';x.font='bold 12px sans-serif';x.textAlign='left';x.fillText('🎙️ 録音',12,18);
      // two race bars
      const bx=20,bw=W-40,y1=92,y2=150,bh=30;
      function bar(y,label,frac,col,tmin){x.fillStyle='rgba(255,255,255,.08)';x.fillRect(bx,y,bw,bh);
        x.fillStyle=col;x.fillRect(bx,y,bw*frac,bh);
        x.fillStyle='#fff';x.font='bold 12px sans-serif';x.textAlign='left';x.fillText(label,bx+8,y-6);
        x.textAlign='right';x.fillText(num(tmin*frac)+'分',bx+bw-8,y+20);}
      const manFrac=Math.min(1,p*1.0), aiFrac=Math.min(1,p*maxT/Math.max(aiMin,1));
      bar(y1,'✋ 手作業',manFrac,'#f43f5e',manualMin);
      bar(y2,'🎙️ 音声入力(AI)',aiFrac,'#6366f1',aiMin);
      if(aiFrac>=1){x.fillStyle='#34d399';x.font='bold 13px sans-serif';x.textAlign='right';x.fillText('✓ 完了',bx+bw-8,y2-6);}
      if(p<1)raf=requestAnimationFrame(frame);}
    raf=requestAnimationFrame(frame);}''')

# ============================================================
# 2. 続く音声日記＝生涯の自分史（日記 続かない 150/KD0）
# ============================================================
add(id='voice-diary', cat=V, emoji='📖',
  title='音声日記シミュレーター｜1日1分の記録が生涯で何冊の自分史になる？｜シミュラボ',
  desc='日記が続かない人へ。1日たった1分の音声日記を続けたら、生涯で文庫本何冊分の「自分史」が残るかを可視化する無料シミュレーター。話すだけなら日記は続きます。',
  ogtitle='音声日記シミュレーター｜生涯で何冊の自分史になる？', ogdesc='1日1分の音声日記が生涯で文庫本何冊分の自分史になるか可視化。',
  h1='音声日記シミュレーター｜生涯の自分史',
  lead='日記が続かないのは「書くのが面倒」だから。でも、話すだけなら続きます。1日たった数分の音声日記を続けたら、生涯で文庫本何冊分の「自分史」が残るのか、本棚にして見てみましょう。',
  inputs='''    <h2>📖 条件を入れる</h2>
    <div class="row"><div class="field"><label>1日に話す時間 <span class="hint">（分）</span></label><input type="number" id="min" value="3" min="0" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>これからの年数 <span class="hint">（年）</span></label><input type="number" id="years" value="30" min="1" max="80" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">残る自分史を見る</button>''',
  result='''      <div class="label">生涯で残る自分史</div>
      <div class="big"><span id="big">0</span><span class="unit">冊分</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">総文字数</div><div class="v accent" id="chars">—</div></div>
      <div class="stat"><div class="k">記録する日数</div><div class="v" id="days">—</div></div>
      <div class="stat"><div class="k">1年で</div><div class="v" id="peryear">—</div></div></div>''',
  visual=viz(480,240,500),
  article='''    <div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：話す速さは約300字/分。1日3分の音声日記でも1年で約<b>32万字</b>、文庫本にして数冊分。これを何十年と積めば、<b>あなたにしか書けない一生分の自分史</b>になります。書くより圧倒的に続けやすいのが音声日記です。</div>
    <h2>日記が続かない本当の理由</h2>
    <p>「三日坊主」になるのは意志が弱いからではありません。手で書くのが面倒で、ハードルが高いからです。寝る前にノートを開き、ペンを持ち、文章を考えて書く——この一連の動作が、疲れた日には重すぎる。話すだけなら、布団の中でも、歩きながらでも続けられます。</p>
    <h2>記録のない毎日は、流れて消える</h2>
    <p>今日あった出来事も、感じたことも、記録しなければ数日で忘れます。10年後に読み返せる「自分の歴史」は、毎日のほんの数分からしか生まれません。1日1分話すだけで、人生がまるごと残る。これ以上の「時間の投資」はそうありません。</p>'''+TYPELESS+'''
    <h2>よくある質問</h2>'''+faq([
      ('文庫本1冊は何文字？','一般に約8〜10万字です。本シミュは8万字で換算しています。'),
      ('話した日記は読み返せる？','テキスト化されるので検索も引用も可能。「あの日のこと」を一瞬で探せます。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  let raf=0;
  function calc(){const mi=Math.max(0,+$('min').value||0),y=Math.max(1,+$('years').value||1);
    const chars=mi*300*365*y, books=chars/80000, days=365*y;
    $('sub').textContent=`1日${mi}分 × ${y}年`;
    $('chars').textContent=num(chars)+'字';$('days').textContent=num(days)+'日';$('peryear').textContent=(mi*300*365/80000).toFixed(1)+'冊';
    SHARE=`音声日記シミュ、1日${mi}分でも${y}年で文庫本 約${Math.round(books)}冊分の自分史が残る計算でした📖 話すだけなら続く。`;
    show();anim($('big'),0,books,1000);startViz(books);}
  function startViz(books){const c=$('viz'),x=c.getContext('2d'),W=c.width,H=c.height;cancelAnimationFrame(raf);
    const total=Math.round(books),shown=Math.min(total,48),cols=12,bw=30,bh=42,gap=4,baseY=H-24;
    const cols2=Math.min(cols,shown||1);
    const hues=[265,210,180,330,30,150];const t0=performance.now(),DUR=1600;
    function frame(n){const p=Math.min(1,(n-t0)/DUR);x.fillStyle='#0b1530';x.fillRect(0,0,W,H);
      // shelf
      const appear=Math.floor(shown*p);
      const startX=(W-(cols2*(bw+gap)))/2;
      for(let i=0;i<appear;i++){const r=Math.floor(i/cols2),col=i%cols2;const bxp=startX+col*(bw+gap);
        const yy=baseY-(r+1)*(bh+gap)+ (1-Math.min(1,(p*shown-i)))*8;
        x.fillStyle=`hsl(${hues[i%hues.length]},65%,${56-r*3}%)`;x.fillRect(bxp,yy,bw,bh);
        x.fillStyle='rgba(255,255,255,.25)';x.fillRect(bxp,yy,bw,4);
        x.strokeStyle='rgba(0,0,0,.2)';x.strokeRect(bxp+0.5,yy+0.5,bw,bh);}
      x.fillStyle='#fff';x.font='bold 14px sans-serif';x.textAlign='center';
      x.fillText('📚 あなたの自分史：'+num(total)+'冊',W/2,26);
      if(total>shown)x.fillText('（表示は'+shown+'冊・実際は'+num(total)+'冊）',W/2,H-6);
      if(p<1)raf=requestAnimationFrame(frame);}
    raf=requestAnimationFrame(frame);}''')

# ============================================================
# 3. 卒論・レポート執筆時間（卒論 進まない 50/KD0）
# ============================================================
add(id='sotsuron-jitan', cat=V, emoji='🎓',
  title='卒論・レポート執筆時間シミュレーター｜音声入力なら何日早く終わる？｜シミュラボ',
  desc='卒論やレポートの文字数から、タイピングで書く場合と音声入力で口述する場合の執筆時間・必要日数を比較する無料シミュレーター。締切まで間に合うかも分かります。',
  ogtitle='卒論・レポート執筆時間シミュ｜音声で何日早い？', ogdesc='文字数から、打つ場合と話す場合の執筆日数を比較。締切に間に合う？',
  h1='卒論・レポート執筆時間シミュレーター',
  lead='卒論が進まない…。原因は「書くのが遅い」こと。目標の文字数を入れると、タイピングで書く場合と、音声で口述する場合の執筆時間を比べ、締切に間に合うかを可視化します。',
  inputs='''    <h2>🎓 条件を入れる</h2>
    <div class="row"><div class="field"><label>目標の文字数 <span class="hint">（字）</span></label><input type="number" id="chars" value="20000" min="0" inputmode="numeric"></div>
    <div class="field"><label>1日に使える時間 <span class="hint">（時間）</span></label><input type="number" id="hpd" value="2" min="0" step="0.5" inputmode="decimal"></div></div>
    <div class="field"><label>タイピング速度 <span class="hint">（字/分）</span></label><input type="number" id="speed" value="55" min="10" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">執筆日数を見る</button>''',
  result='''      <div class="label">音声入力なら早く終わる</div>
      <div class="big"><span id="big">0</span><span class="unit">日</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">タイピングだと</div><div class="v" id="type">—</div></div>
      <div class="stat"><div class="k">音声入力だと</div><div class="v accent" id="voice">—</div></div>
      <div class="stat"><div class="k">短縮できる時間</div><div class="v" id="saveh">—</div></div></div>''',
  visual=viz(520,180,540),
  article='''    <div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：文章は「考えながら打つ」と手が止まり、想像以上に時間がかかります。音声で口述すれば思考が止まらず、下書きは<b>約半分の時間</b>で完成。締切前の徹夜を回避できます。</div>
    <h2>卒論・レポートが進まない理由</h2>
    <p>多くの人が「書けない」と感じるのは、頭の中の考えを「文字に変換する」作業が遅いから。タイピングは思考の速度に追いつけず、書いては消し、を繰り返して時間が溶けます。話すなら、考えがそのまま言葉になり、手が止まりません。</p>
    <h2>口述ドラフトという書き方</h2>
    <p>骨子（見出し）だけ先に決め、各セクションを声で一気に話す。AIが整文してくれるので、あとは推敲するだけ。「真っ白な画面とにらめっこ」する時間が消え、提出までの日数が一気に縮みます。締切に追われる学生ほど効果は絶大です。</p>'''+TYPELESS+'''
    <h2>よくある質問</h2>'''+faq([
      ('話し言葉のままにならない？','AIが書き言葉・論文調に整えます。引用や数式は後から手で足せばOK。'),
      ('参考文献の調査時間は別？','本シミュは執筆そのものの時間です。調べる時間は別途見込んでください。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  let raf=0;
  function calc(){const ch=Math.max(0,+$('chars').value||0),hpd=Math.max(0.1,+$('hpd').value||0.1),sp=Math.max(10,+$('speed').value||10);
    const typeH=ch/sp/60*2.0, voiceH=typeH*0.5, saveH=typeH-voiceH;
    const typeD=typeH/hpd, voiceD=voiceH/hpd, saveD=typeD-voiceD;
    $('sub').textContent=`${num(ch)}字・1日${hpd}時間・${sp}字/分`;
    $('type').textContent=typeD.toFixed(1)+'日';$('voice').textContent=voiceD.toFixed(1)+'日';$('saveh').textContent=num(saveH)+'時間';
    SHARE=`卒論執筆シミュ、${num(ch)}字をタイピングだと約${typeD.toFixed(1)}日…音声入力なら約${voiceD.toFixed(1)}日で、${saveD.toFixed(1)}日も早く終わる計算でした🎓`;
    show();anim($('big'),0,saveD,900,1);startViz(typeH,voiceH);}
  function startViz(typeH,voiceH){const c=$('viz'),x=c.getContext('2d'),W=c.width,H=c.height;cancelAnimationFrame(raf);
    const maxH=Math.max(typeH,0.1),t0=performance.now(),DUR=2400;
    function frame(n){const p=Math.min(1,(n-t0)/DUR);x.fillStyle='#0b1530';x.fillRect(0,0,W,H);
      const bx=24,bw=W-48,y1=64,y2=120,bh=34;
      function lane(y,label,h,col){x.fillStyle='rgba(255,255,255,.08)';x.fillRect(bx,y,bw,bh);
        const frac=Math.min(1,p*maxH/Math.max(h,0.01));x.fillStyle=col;x.fillRect(bx,y,bw*frac,bh);
        // pen icon at tip
        x.fillStyle='#fff';x.font='15px sans-serif';x.textAlign='left';x.fillText(frac<1?'✍️':'✅',bx+bw*frac-4,y+24);
        x.font='bold 12px sans-serif';x.fillText(label,bx,y-6);x.textAlign='right';x.fillText(h.toFixed(1)+'時間',bx+bw,y-6);}
      lane(y1,'⌨️ タイピングで執筆',typeH,'#f43f5e');
      lane(y2,'🎙️ 音声で口述',voiceH,'#6366f1');
      x.fillStyle='#fff';x.font='bold 13px sans-serif';x.textAlign='center';x.fillText('同じ卒論を書き上げるまで',W/2,24);
      if(p<1)raf=requestAnimationFrame(frame);}
    raf=requestAnimationFrame(frame);}''')

# ============================================================
# 4. スマホ入力の生涯時間（フリック入力）
# ============================================================
add(id='sumaho-input', cat=V, emoji='📱',
  title='スマホ入力 生涯時間シミュレーター｜フリック入力に一生で何日使う？｜シミュラボ',
  desc='1日のスマホ文字入力（フリック入力）の時間から、生涯でスマホを打つだけに費やす総時間を計算し、音声入力で取り戻せる日数を可視化する無料シミュレーター。',
  ogtitle='スマホ入力 生涯時間シミュ｜一生で何日打つ？', ogdesc='フリック入力に生涯で費やす時間と、音声で取り戻せる日数を可視化。',
  h1='スマホ入力 生涯時間シミュレーター',
  lead='LINE、SNS、検索、メモ…1日のうちスマホで「打っている」時間、合計するとけっこうなもの。生涯で何日分をフリック入力に使うのか、そして音声入力で何日取り戻せるかを計算します。',
  inputs='''    <h2>📱 条件を入れる</h2>
    <div class="row"><div class="field"><label>1日のスマホ入力時間 <span class="hint">（分）</span></label><input type="number" id="min" value="50" min="0" inputmode="numeric"></div>
    <div class="field"><label>これからの年数 <span class="hint">（年）</span></label><input type="number" id="years" value="40" min="1" max="80" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">生涯の入力時間を見る</button>''',
  result='''      <div class="label">生涯でフリック入力する時間</div>
      <div class="big"><span id="big">0</span><span class="unit">日分</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">総時間</div><div class="v" id="hh">—</div></div>
      <div class="stat"><div class="k">音声で取り戻す</div><div class="v accent" id="back">—</div></div>
      <div class="stat"><div class="k">推定タップ数</div><div class="v" id="taps">—</div></div></div>''',
  visual=viz(480,230,500),
  article='''    <div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：1日のスマホ入力が50分なら、40年で約<b>500日分（昼夜問わず丸1年以上）</b>を「親指で打つ」だけに使う計算。音声入力に切り替えれば、その大半を取り戻せます。</div>
    <h2>フリック入力は意外と時間を食う</h2>
    <p>フリック入力は速い人でも1分あたり数十文字。1通のメッセージは数十秒でも、1日に何十回も繰り返せば積み上がります。下のマスは「あなたの残りの人生の週」。赤く埋まるのが、スマホを打つだけに消える時間です。</p>
    <h2>スマホでこそ音声入力</h2>
    <p>歩きながら、家事をしながら、布団の中で。スマホの音声入力なら、親指を動かさずに話すだけ。LINEもメモもSNSも一瞬です。小さな積み重ねを取り戻すと、人生の時間がまとまって返ってきます。</p>'''+TYPELESS+'''
    <h2>よくある質問</h2>'''+faq([
      ('外で声を出しづらい','イヤホンマイクや小声入力に対応するツールも。自宅・移動中だけでも効果は大きいです。'),
      ('絵文字や記号は？','「ハートマーク」などと話して入力できるツールもあります。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  let raf=0;
  function calc(){const mi=Math.max(0,+$('min').value||0),y=Math.max(1,+$('years').value||1);
    const totalH=mi*365*y/60, days=totalH/24, back=days*2/3, taps=mi*60*365*y/2;
    $('sub').textContent=`1日${mi}分 × ${y}年`;
    $('hh').textContent=num(totalH)+'時間';$('back').textContent=num(back)+'日';$('taps').textContent=num(taps)+'回';
    SHARE=`スマホ入力 生涯時間シミュ、フリック入力に一生で約${num(days)}日分も使う計算でした📱 音声入力なら約${num(back)}日取り戻せる。`;
    show();anim($('big'),0,days,1000);startViz(y,mi);}
  function startViz(years,mi){const c=$('viz'),x=c.getContext('2d'),W=c.width,H=c.height;cancelAnimationFrame(raf);
    const cols=26,rows=Math.min(20,Math.max(4,Math.round(years/2))),cell=Math.min(14,(W-40)/cols),gap=2;
    const frac=clamp(mi/(16*60),0,1); // 起きてる時間に占める入力割合
    const totalCells=cols*rows, redCells=Math.round(totalCells*frac);
    const ox=(W-cols*(cell+gap))/2, oy=46, t0=performance.now(),DUR=1800;
    function frame(n){const p=Math.min(1,(n-t0)/DUR);x.fillStyle='#0b1530';x.fillRect(0,0,W,H);
      const reveal=Math.floor(totalCells*p);let red=0;
      for(let i=0;i<totalCells;i++){const r=Math.floor(i/cols),col=i%cols;const xx=ox+col*(cell+gap),yy=oy+r*(cell+gap);
        let fill='rgba(255,255,255,.10)';
        if(i<reveal){ if(red<Math.round(redCells*p)){fill='#f43f5e';red++;} else fill='rgba(160,200,255,.22)'; }
        x.fillStyle=fill;x.fillRect(xx,yy,cell,cell);}
      x.fillStyle='#fff';x.font='bold 13px sans-serif';x.textAlign='center';x.fillText('🟥 ＝ スマホを打つだけに消える時間',W/2,26);
      x.font='11px sans-serif';x.fillStyle='rgba(255,255,255,.7)';x.fillText('マス＝これからの人生の週',W/2,H-8);
      if(p<1)raf=requestAnimationFrame(frame);}
    raf=requestAnimationFrame(frame);}''')

# ============================================================
# 5. AI文章作成 時短（ai 文章作成 6600/KD21）
# ============================================================
add(id='ai-bunsho', cat=V, emoji='🤖',
  title='AI文章作成 時短シミュレーター｜話して作ると年間どれだけ速い？｜シミュラボ',
  desc='月の文章作成本数と1本の作成時間から、AI＋音声入力で文章を作った場合に年間でどれだけ時間が浮き、何本多く作れるかを計算する無料シミュレーター。',
  ogtitle='AI文章作成 時短シミュ｜年間どれだけ速い？', ogdesc='AI＋音声で文章を作ると年間どれだけ時短し何本多く作れるか計算。',
  h1='AI文章作成 時短シミュレーター',
  lead='AIに文章を作らせるのは速い。でも「プロンプトを打つ」のも手間です。最短は、話すだけ。月の作成本数と1本の時間から、AI＋音声入力で浮く年間の時間を計算します。',
  inputs='''    <h2>🤖 条件を入れる</h2>
    <div class="row"><div class="field"><label>月の文章作成本数 <span class="hint">（本）</span></label><input type="number" id="n" value="20" min="0" inputmode="numeric"></div>
    <div class="field"><label>1本の作成時間 <span class="hint">（分）</span></label><input type="number" id="min" value="30" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>時給（時間価値） <span class="hint">（円）</span></label><input type="number" id="wage" value="2500" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">年間の時短を見る</button>''',
  result='''      <div class="label">年間で浮く時間</div>
      <div class="big"><span id="big">0</span><span class="unit">時間</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">年間の削減額</div><div class="v accent" id="money">—</div></div>
      <div class="stat"><div class="k">浮いた時間で</div><div class="v" id="extra">—</div></div>
      <div class="stat"><div class="k">1本</div><div class="v" id="per">—</div></div></div>''',
  visual=viz(520,200,540),
  article='''    <div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：AI文章作成の時短効果は大きいですが、入力が「タイピング」のままでは半減します。<b>話して指示・口述</b>すれば、考えるそばから文章になり、作成時間は<b>3分の1ほど</b>に。浮いた時間で、もっと多くを生み出せます。</div>
    <h2>AIに「打って指示」も、実はムダ</h2>
    <p>AI文章作成ツールは便利ですが、長いプロンプトや下書きをキーボードで打つのは結局時間がかかります。思考の速度に手が追いつかないのは、AIを使っても同じ。入力そのものを「話す」に変えると、ボトルネックが消えます。</p>
    <h2>話す→AIが整える、が最速ワークフロー</h2>
    <p>頭の中のアイデアを声で吐き出し、AIが整文・要約・体裁を整える。推敲だけ手で行う。この流れなら、1本にかかる時間が激減し、同じ時間でより多くの記事・提案・投稿を量産できます。発信量＝チャンスの数です。</p>'''+TYPELESS+'''
    <h2>よくある質問</h2>'''+faq([
      ('AIだけで十分では？','AIの出力品質は「入力の質と量」で決まります。話して多くの素材を渡せるほど良くなります。'),
      ('音声とAIはどう組み合わせる？','音声入力で素材・指示を一気に渡し、AIに整えさせるのが効率的。Typelessは整文まで自動です。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  let raf=0;
  function calc(){const n=Math.max(0,+$('n').value||0),mi=Math.max(0,+$('min').value||0),w=Math.max(0,+$('wage').value||0);
    const aiMin=mi*0.35, saveYearH=(mi-aiMin)*n*12/60, money=saveYearH*w, extra=aiMin>0?(mi-aiMin)*n*12/aiMin:0;
    $('sub').textContent=`月${n}本・1本${mi}分・時給${num(w)}円`;
    $('money').textContent=yen(money);$('extra').textContent=num(extra)+'本多く';$('per').textContent=num(mi)+'分→'+num(aiMin)+'分';
    SHARE=`AI文章作成 時短シミュ、話して作ると年間 約${num(saveYearH)}時間（約${yen(money)}）浮いて、${num(extra)}本も多く作れる計算でした🤖`;
    show();anim($('big'),0,saveYearH,900);startViz(mi,aiMin);}
  function startViz(mi,aiMin){const c=$('viz'),x=c.getContext('2d'),W=c.width,H=c.height;cancelAnimationFrame(raf);
    const t0=performance.now(),DUR=2200,maxM=Math.max(mi,1);
    function doc(dx,frac,col,label,tmin){const dw=150,dh=120,dy=64;
      x.fillStyle='#11203a';x.fillRect(dx,dy,dw,dh);x.strokeStyle=col;x.lineWidth=2;x.strokeRect(dx,dy,dw,dh);
      const lines=Math.floor(10*frac);x.fillStyle=col;
      for(let i=0;i<lines;i++){const lw=(i%3===2?0.6:0.9)*(dw-20);x.fillRect(dx+10,dy+10+i*11,lw,5);}
      x.fillStyle='#fff';x.font='bold 12px sans-serif';x.textAlign='center';x.fillText(label,dx+dw/2,dy-8);
      x.fillText(num(tmin)+'分',dx+dw/2,dy+dh+18);}
    function frame(n){const p=Math.min(1,(n-t0)/DUR);x.fillStyle='#0b1530';x.fillRect(0,0,W,H);
      const fA=Math.min(1,p*maxM/maxM), fB=Math.min(1,p*maxM/Math.max(aiMin,0.1));
      doc(W*0.5-170,fA,'#f43f5e','⌨️ 打って作る',mi);
      doc(W*0.5+20,fB,'#6366f1','🎙️ 話して作る',aiMin);
      x.fillStyle='#fff';x.font='bold 13px sans-serif';x.textAlign='center';x.fillText('同じ1本ができるまで',W/2,24);
      if(p<1)raf=requestAnimationFrame(frame);}
    raf=requestAnimationFrame(frame);}''')

# ============================================================
# 6. Webライター実質時給（webライター 文字単価）
# ============================================================
add(id='writer-jikyu', cat=V, emoji='💰',
  title='Webライター実質時給シミュレーター｜音声入力で時給は何倍になる？｜シミュラボ',
  desc='文字単価・1記事の文字数・執筆時間から、Webライターの実質時給を計算し、音声入力で執筆を速くすると時給が何倍になるかを可視化する無料シミュレーター。',
  ogtitle='Webライター実質時給シミュ｜音声で時給は何倍？', ogdesc='文字単価と執筆速度から実質時給を計算。音声入力で何倍になる？',
  h1='Webライター実質時給シミュレーター',
  lead='Webライターの収入は「文字単価×速さ」で決まります。文字単価・記事の文字数・執筆時間から実質時給を計算し、音声入力で執筆を速くすると時給が何倍になるかを見てみましょう。',
  inputs='''    <h2>💰 条件を入れる</h2>
    <div class="row"><div class="field"><label>文字単価 <span class="hint">（円/字）</span></label><input type="number" id="tanka" value="1.0" min="0" step="0.1" inputmode="decimal"></div>
    <div class="field"><label>1記事の文字数 <span class="hint">（字）</span></label><input type="number" id="chars" value="3000" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>1記事の執筆時間 <span class="hint">（分）</span></label><input type="number" id="min" value="120" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">実質時給を見る</button>''',
  result='''      <div class="label">音声入力にした実質時給</div>
      <div class="big"><span id="big">0</span><span class="unit">円/時</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">今の実質時給</div><div class="v" id="now">—</div></div>
      <div class="stat"><div class="k">時給アップ</div><div class="v accent" id="ratio">—</div></div>
      <div class="stat"><div class="k">月20本で増収</div><div class="v" id="month">—</div></div></div>''',
  visual=viz(480,220,500),
  article='''    <div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：ライターの実質時給は「記事の報酬 ÷ かかった時間」。報酬が同じなら、<b>執筆が速いほど時給は上がります</b>。音声で下書きを口述すれば執筆時間は約半分。同じ単価でも<b>実質時給は約2倍</b>になります。</div>
    <h2>「遅さ」は、そのまま時給の損</h2>
    <p>文字単価1円の3,000字の記事も、30分で書けば時給6,000円、3時間かかれば時給1,000円。単価交渉より先に、まず「速さ」を上げるのが収入アップの近道です。手が止まる時間は、1円も生みません。</p>
    <h2>口述で書けば、時給も本数も増える</h2>
    <p>構成を決めて声で一気に下書き→AIが整文→推敲だけ。この流れに変えるだけで、1本の時間が縮み、同じ稼働で本数を増やせます。時給アップと増収のダブル効果。副業ライターほどインパクトが大きい改善です。</p>'''+TYPELESS+'''
    <h2>よくある質問</h2>'''+faq([
      ('品質は落ちない？','構成と推敲は人が行うので品質は保てます。むしろ手が止まらず筆が乗ります。'),
      ('音声で書くと単価が下がる？','成果物は同じテキスト。読者にもクライアントにも違いは分かりません。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  let raf=0;
  function calc(){const t=Math.max(0,+$('tanka').value||0),ch=Math.max(0,+$('chars').value||0),mi=Math.max(1,+$('min').value||1);
    const pay=t*ch, nowHourly=pay/(mi/60), voiceMin=mi*0.5, voiceHourly=pay/(voiceMin/60), ratio=nowHourly>0?voiceHourly/nowHourly:0;
    const monthGain=(voiceHourly-nowHourly)*(voiceMin/60)*20;
    $('sub').textContent=`単価${t}円 × ${num(ch)}字 ÷ ${num(mi)}分`;
    $('now').textContent=yen(nowHourly);$('ratio').textContent='約'+ratio.toFixed(1)+'倍';$('month').textContent=yen((voiceHourly-nowHourly)*(voiceMin/60)*20);
    SHARE=`Webライター実質時給シミュ、音声入力で執筆を速くすると時給が約${ratio.toFixed(1)}倍（${yen(nowHourly)}→${yen(voiceHourly)}）になる計算でした💰`;
    show();anim($('big'),0,voiceHourly,900);startViz(nowHourly,voiceHourly);}
  function startViz(nowH,voiceH){const c=$('viz'),x=c.getContext('2d'),W=c.width,H=c.height;cancelAnimationFrame(raf);
    const cx=W/2,cy=H-24,R=Math.min(W,H*1.6)/2-30,maxV=Math.max(voiceH,1),t0=performance.now(),DUR=1600;
    function frame(n){const p=Math.min(1,(n-t0)/DUR);x.fillStyle='#0b1530';x.fillRect(0,0,W,H);
      // gauge arc
      x.lineWidth=14;x.strokeStyle='rgba(255,255,255,.1)';x.beginPath();x.arc(cx,cy,R,Math.PI,2*Math.PI);x.stroke();
      const cur=nowH+(voiceH-nowH)*p, frac=clamp(cur/(maxV*1.1),0,1);
      const grad=x.createLinearGradient(cx-R,0,cx+R,0);grad.addColorStop(0,'#f59e0b');grad.addColorStop(1,'#6366f1');
      x.strokeStyle=grad;x.beginPath();x.arc(cx,cy,R,Math.PI,Math.PI+Math.PI*frac);x.stroke();
      // needle
      const ang=Math.PI+Math.PI*frac;x.strokeStyle='#fff';x.lineWidth=3;x.beginPath();x.moveTo(cx,cy);x.lineTo(cx+Math.cos(ang)*R*0.86,cy+Math.sin(ang)*R*0.86);x.stroke();
      x.fillStyle='#fff';x.beginPath();x.arc(cx,cy,6,0,7);x.fill();
      x.font='bold 22px sans-serif';x.textAlign='center';x.fillText(yen(cur)+'/時',cx,cy-R*0.35);
      x.font='12px sans-serif';x.fillStyle='rgba(255,255,255,.7)';x.fillText('🪙 実質時給メーター',cx,28);
      // coins
      for(let i=0;i<Math.floor(8*p);i++){const yy=(40+(i*40+n*0.1)%(H-60));x.fillStyle='#fbbf24';x.beginPath();x.arc(40+((i*53)%(W-80)),yy,5,0,7);x.fill();}
      if(p<1)raf=requestAnimationFrame(frame);}
    raf=requestAnimationFrame(frame);}''')

# ============================================================
# 7. 読書メモ・学びの蓄積（読書 アウトプット）
# ============================================================
add(id='dokusho-memo', cat=V, emoji='🧠',
  title='読書メモ蓄積シミュレーター｜話してアウトプットすると学びはどれだけ残る？｜シミュラボ',
  desc='年間の読書冊数から、感想やメモを音声でアウトプットすると、何文字・文庫本何冊分の「知識資産」が残るかを可視化する無料シミュレーター。読みっぱなしを防ぎます。',
  ogtitle='読書メモ蓄積シミュ｜話すと学びはどれだけ残る？', ogdesc='年間読書数から、話してメモすると残る知識資産を可視化。',
  h1='読書メモ蓄積シミュレーター',
  lead='本は読んだだけでは、内容の多くを忘れてしまいます。読後に少し話して残すだけで、学びは「知識資産」に変わる。年間の読書冊数から、音声アウトプットで蓄積される知識量を可視化します。',
  inputs='''    <h2>🧠 条件を入れる</h2>
    <div class="row"><div class="field"><label>年間の読書冊数 <span class="hint">（冊）</span></label><input type="number" id="books" value="24" min="0" inputmode="numeric"></div>
    <div class="field"><label>1冊で話す感想 <span class="hint">（分）</span></label><input type="number" id="min" value="5" min="0" step="0.5" inputmode="decimal"></div></div>
    <div class="field"><label>続ける年数 <span class="hint">（年）</span></label><input type="number" id="years" value="10" min="1" max="60" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">残る知識資産を見る</button>''',
  result='''      <div class="label">蓄積される知識資産</div>
      <div class="big"><span id="big">0</span><span class="unit">文字</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">文庫本にすると</div><div class="v accent" id="books2">—</div></div>
      <div class="stat"><div class="k">アウトプットする冊数</div><div class="v" id="cnt">—</div></div>
      <div class="stat"><div class="k">手で書くなら</div><div class="v" id="hand">—</div></div></div>''',
  visual=viz(480,210,500),
  article='''    <div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：人は読んだ内容の多くを数日で忘れます。読後に<b>話してアウトプット</b>すれば記憶に定着し、テキストとして検索・再利用できる「知識資産」になります。話す速さは約300字/分なので、ほんの数分で1冊分の学びを残せます。</div>
    <h2>読みっぱなしは、学びを捨てている</h2>
    <p>どんなに良い本も、アウトプットしなければ「読んだ気」で終わります。学びを定着させる最強の方法は「自分の言葉で説明する」こと。でも、毎回ノートに書くのは続きません。話すだけなら、本を閉じた直後に1〜2分で残せます。</p>
    <h2>話す→テキスト化で、知識が積み上がる</h2>
    <p>音声で感想・要点を話し、AIが整文。検索できる読書メモが自動でたまっていきます。1年後には、自分専用の知識データベース。仕事のアイデアも、SNS発信のネタも、そこから引き出せます。インプットを資産に変える習慣です。</p>'''+TYPELESS+'''
    <h2>よくある質問</h2>'''+faq([
      ('何を話せばいい？','「一番の学び」「使えそうな点」「印象的な一文」の3つだけでも十分です。'),
      ('記憶に本当に残る？','自分の言葉で再構成（アウトプット）すると定着しやすいことが知られています。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  let raf=0;
  function calc(){const b=Math.max(0,+$('books').value||0),mi=Math.max(0,+$('min').value||0),y=Math.max(1,+$('years').value||1);
    const chars=b*mi*300*y, books2=chars/80000, cnt=b*y, handMin=b*mi*3*y;
    $('sub').textContent=`年${b}冊・1冊${mi}分 × ${y}年`;
    $('books2').textContent=books2.toFixed(1)+'冊';$('cnt').textContent=num(cnt)+'冊';$('hand').textContent=num(handMin/60)+'時間';
    SHARE=`読書メモ蓄積シミュ、話してアウトプットすると${y}年で約${num(chars)}文字（文庫${books2.toFixed(1)}冊分）の知識資産が残る計算でした🧠`;
    show();anim($('big'),0,chars,1000);startViz(Math.min(60,Math.round(cnt)));}
  function startViz(cnt){const c=$('viz'),x=c.getContext('2d'),W=c.width,H=c.height;cancelAnimationFrame(raf);
    const cx=W/2,cy=H/2+6,t0=performance.now(),DUR=2200;
    const parts=[];for(let i=0;i<cnt;i++)parts.push({a:Math.random()*6.28,r:60+Math.random()*70,sp:0.4+Math.random()*0.6,delay:i/Math.max(cnt,1)});
    function brain(level){x.strokeStyle='rgba(167,139,250,'+(0.4+0.6*level)+')';x.lineWidth=2.5;
      x.beginPath();x.arc(cx,cy,46,0,7);x.stroke();
      x.beginPath();for(let a=0;a<6.28;a+=0.5){const rr=46+Math.sin(a*3)*6;x.lineTo(cx+Math.cos(a)*rr,cy+Math.sin(a)*rr);}x.closePath();x.stroke();
      x.fillStyle='rgba(99,102,241,'+(0.15+0.5*level)+')';x.beginPath();x.arc(cx,cy,46,0,7);x.fill();}
    function frame(n){const p=Math.min(1,(n-t0)/DUR);x.fillStyle='#0b1530';x.fillRect(0,0,W,H);
      let landed=0;
      for(const q of parts){const lp=clamp((p-q.delay)*2.2,0,1);if(lp>=1)landed++;
        const rr=q.r*(1-lp);const xx=cx+Math.cos(q.a)*rr,yy=cy+Math.sin(q.a)*rr-(1-lp)*0;
        x.fillStyle='hsla('+(255+q.a*8)+',80%,70%,'+(0.4+0.6*lp)+')';x.beginPath();x.arc(xx,yy,3.5,0,7);x.fill();}
      brain(landed/Math.max(cnt,1));
      x.fillStyle='#fff';x.font='bold 13px sans-serif';x.textAlign='center';x.fillText('📚→🧠 学びが知識資産に',W/2,24);
      if(p<1)raf=requestAnimationFrame(frame);}
    raf=requestAnimationFrame(frame);}''')

# ============================================================
# 8. 話せば何倍速？診断（インタラクティブ・タイピング測定）
# ============================================================
add(id='input-baisoku', cat=V, emoji='⚡',
  title='タイピング速度 vs 音声入力 診断｜あなたは話せば何倍速？｜シミュラボ',
  desc='表示された文章を実際にタイピングして速度を測定し、音声入力（約300字/分）と比べてあなたが「話せば何倍速か」を判定する無料の体験型シミュレーター。',
  ogtitle='あなたは話せば何倍速？｜タイピング vs 音声入力 診断', ogdesc='実際に打って速度測定→音声入力と比較。あなたは話せば何倍速？',
  h1='タイピング速度 vs 音声入力 診断',
  lead='あなたのタイピング、話すのと比べて何倍遅い？下の文章を実際に打ってみてください。打ち終わると速度を測定し、音声入力（約300字/分）と比較して「話せば何倍速か」を判定します。',
  inputs='''    <h2>⚡ この文章を打ってみよう</h2>
    <p id="sample" style="font-weight:800;font-size:16px;line-height:1.8;background:#f6f8fb;border:1px solid var(--line);border-radius:10px;padding:14px;">音声入力なら話すだけで文章があっという間に完成します</p>
    <input type="text" id="typein" placeholder="ここに上の文章を打つとスタート" autocomplete="off" style="width:100%;font-size:16px;padding:12px;border:1.5px solid var(--line);border-radius:10px;">
    <div style="margin-top:12px;">''' + viz(520,90,540,'race','background:#0b1530;') + '''</div>
    <button class="btn btn-ghost" id="calcBtn" style="margin-top:12px;">やり直す</button>''',
  result='''      <div class="label">音声入力は あなたの</div>
      <div class="big"><span id="big">0</span><span class="unit">倍速</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">あなたのタイピング</div><div class="v" id="cpm">—</div></div>
      <div class="stat"><div class="k">音声入力</div><div class="v accent" id="vcpm">約300字/分</div></div>
      <div class="stat"><div class="k">同じ文章を音声なら</div><div class="v" id="vsec">—</div></div></div>''',
  visual='',
  article='''    <div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：日本語のタイピングは速い人でも1分あたり<b>60〜120字</b>ほど。話す速さは約<b>300字/分</b>です。つまり多くの人にとって、音声入力は<b>タイピングの2〜4倍速</b>。打つのをやめて話すだけで、入力の時間は何分の一にもなります。</div>
    <h2>なぜ話すほうが速いのか</h2>
    <p>タイピングは「考える→指で打つ→画面を確認する」の3ステップ。話すのは「考える→声に出す」だけ。手の動きという物理的な制約がない分、思考の速度に近いスピードで文字にできます。脳の負担も小さく、長時間でも疲れにくいのが特長です。</p>
    <h2>あなたの「打つ速度」が、人生の上限になっている</h2>
    <p>メールも資料も日記も、あなたの「打つ速さ」が作業の上限を決めています。その上限を音声入力で2〜4倍に引き上げれば、同じ時間でできることが何倍にもなります。まずは上の診断で、自分の伸びしろを見てください。</p>'''+TYPELESS+'''
    <h2>よくある質問</h2>'''+faq([
      ('測定はどう行われる？','最初の入力から打ち終わりまでの時間で1分あたりの文字数を計算します。'),
      ('音声入力は本当に300字/分？','話す速さの目安です。整文の手直しを含めても、多くの場面でタイピングを上回ります。'),
      ('データは送信されますか？','いいえ。測定も計算もすべてブラウザ内で完結します。')]),
  js=r'''  const SAMPLE='音声入力なら話すだけで文章があっという間に完成します';
  const ta=$('typein'); let t0=null,raf=0,doneFlag=false;
  function calc(){ta.value='';t0=null;doneFlag=false;ta.disabled=false;ta.focus();drawRace(0,0);}
  ta.addEventListener('input',()=>{ if(doneFlag) return;
    if(t0===null && ta.value.length>0){t0=performance.now();loop();}
    if(ta.value.length>=SAMPLE.length){finish();}});
  function finish(){doneFlag=true;ta.disabled=true;cancelAnimationFrame(raf);
    const sec=Math.max(0.3,(performance.now()-t0)/1000);const cpm=SAMPLE.length/(sec/60);
    const vcpm=300, ratio=Math.max(0.5,vcpm/cpm), vsec=SAMPLE.length/(vcpm/60);
    $('sub').textContent=`あなた：${num(cpm)}字/分（この文章を${sec.toFixed(1)}秒で入力）`;
    $('cpm').textContent=num(cpm)+'字/分';$('vsec').textContent=vsec.toFixed(1)+'秒';
    SHARE=`タイピング vs 音声入力 診断、私のタイピングは${num(cpm)}字/分…音声入力なら約${ratio.toFixed(1)}倍速でした⚡ あなたは何倍速？`;
    show();anim($('big'),0,ratio,900,1);drawRace(1,1);}
  function drawRace(userFrac,voiceFrac){const c=$('race'),x=c.getContext('2d'),W=c.width,H=c.height;
    x.fillStyle='#0b1530';x.fillRect(0,0,W,H);const bx=70,bw=W-90;
    function lane(y,label,frac,col,emoji){x.fillStyle='rgba(255,255,255,.08)';x.fillRect(bx,y,bw,16);
      x.fillStyle=col;x.fillRect(bx,y,bw*clamp(frac,0,1),16);
      x.fillStyle='#fff';x.font='bold 11px sans-serif';x.textAlign='right';x.fillText(label,bx-6,y+13);
      x.font='15px sans-serif';x.textAlign='left';x.fillText(emoji,bx+bw*clamp(frac,0,1)-6,y+15);}
    lane(22,'⌨️あなた',userFrac,'#f43f5e','🏃');
    lane(56,'🎙️音声',voiceFrac,'#6366f1','🚀');}
  function loop(){const userFrac=ta.value.length/SAMPLE.length;
    const elapsed=(performance.now()-t0)/1000; const voiceFrac=elapsed/(SAMPLE.length/(300/60));
    drawRace(userFrac,voiceFrac);if(!doneFlag)raf=requestAnimationFrame(loop);}
  drawRace(0,0);''')

# ============================================================
# 9. 頭の中の棚卸し（頭の中 整理 / 書けない）
# ============================================================
add(id='atama-tana', cat=V, emoji='💭',
  title='頭の中の棚卸しシミュレーター｜書き出せずに失う時間はどれだけ？｜シミュラボ',
  desc='頭の中にあるのに書き出せない…そのモヤモヤや、考えがまとまらず手が止まる時間が、1年でどれだけになるかを可視化する無料シミュレーター。話せば一瞬で外に出せます。',
  ogtitle='頭の中の棚卸しシミュ｜書き出せずに失う時間は？', ogdesc='考えがまとまらず手が止まる時間が年でどれだけになるか可視化。',
  h1='頭の中の棚卸しシミュレーター',
  lead='頭の中にはあるのに、文字にしようとすると手が止まる。その「書き出せない時間」、1年に換算するとかなりのもの。話すだけなら、モヤモヤは一瞬で外に出せます。',
  inputs='''    <h2>💭 条件を入れる</h2>
    <div class="row"><div class="field"><label>1日に「手が止まる」時間 <span class="hint">（分）</span></label><input type="number" id="min" value="30" min="0" inputmode="numeric"></div>
    <div class="field"><label>これからの年数 <span class="hint">（年）</span></label><input type="number" id="years" value="10" min="1" max="60" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">失っている時間を見る</button>''',
  result='''      <div class="label">書き出せずに失う時間</div>
      <div class="big"><span id="big">0</span><span class="unit">時間/年</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">日数にすると(年)</div><div class="v accent" id="days">—</div></div>
      <div class="stat"><div class="k">これからの年数で</div><div class="v" id="total">—</div></div>
      <div class="stat"><div class="k">話せば</div><div class="v" id="voice">一瞬で整理</div></div></div>''',
  visual=viz(480,230,500),
  article='''    <div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：「書けない」のは能力の問題ではありません。<b>頭の中の考えを文字に変換する作業</b>が重いのです。話すなら、その変換がいらない。思いついた順に声に出せば、AIが整理してくれます。手が止まる時間が、まるごと消えます。</div>
    <h2>出せなければ、無かったのと同じ</h2>
    <p>素晴らしいアイデアも、伝えたい気持ちも、頭の中にあるだけでは何も生みません。書き出せずに消えていく思考は、あなたの才能と時間の損失です。下のアニメは、頭の中で渦巻くモヤモヤ。話すことで、ひとつずつ外に出て、整理されていきます。</p>
    <h2>「話す」は、思考の最速の出口</h2>
    <p>真っ白な画面とにらめっこせず、まず声に出す。順番がバラバラでも、AIが整文・構造化してくれます。完璧な文章を最初から打とうとするより、話してから整える方がずっと速い。書けずに固まる時間から、自由になれます。</p>'''+TYPELESS+'''
    <h2>よくある質問</h2>'''+faq([
      ('まとまっていなくても話していい？','むしろ、まとまらないまま話すのがコツ。AIが後から整理します。'),
      ('発達特性で書くのが苦手でも？','「話す」は書くより負担が小さい入力方法です。合う人は多くいます（医療的判断は専門家へ）。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  let raf=0;
  function calc(){const mi=Math.max(0,+$('min').value||0),y=Math.max(1,+$('years').value||1);
    const yearH=mi*365/60, days=yearH/24, totalD=days*y;
    $('sub').textContent=`1日${mi}分 × 365日`;
    $('days').textContent=days.toFixed(1)+'日';$('total').textContent=num(totalD)+'日分';
    SHARE=`頭の中の棚卸しシミュ、書き出せずに失う時間は年間 約${num(yearH)}時間（${days.toFixed(1)}日分）でした💭 話せば一瞬で整理できる。`;
    show();anim($('big'),0,yearH,900);startViz();}
  function startViz(){const c=$('viz'),x=c.getContext('2d'),W=c.width,H=c.height;cancelAnimationFrame(raf);
    const hx=W*0.32,hy=H/2; const words=['アイデア','やること','モヤモヤ','言いたいこと','悩み','企画','感想','タスク','ひらめき','不安'];
    const bub=words.map((w,i)=>({w:w,a:Math.random()*6.28,r:24+Math.random()*48,ph:Math.random()*6.28,out:0,ty:60+i*0}));
    const listX=W*0.62,t0=performance.now(),DUR=3600;
    function head(){x.strokeStyle='rgba(167,139,250,.8)';x.lineWidth=2.5;x.beginPath();
      x.arc(hx,hy,58,0,7);x.stroke();x.fillStyle='rgba(99,102,241,.10)';x.fill();}
    function frame(n){const p=Math.min(1,(n-t0)/DUR);x.fillStyle='#0b1530';x.fillRect(0,0,W,H);
      head();let outc=0;
      bub.forEach((b,i)=>{const trig=i/bub.length;const op=clamp((p-trig)*3,0,1);
        if(op<=0){const xx=hx+Math.cos(b.a+n*0.0008*b.r*0.02)*b.r, yy=hy+Math.sin(b.a*1.3+n*0.001)*b.r;
          x.fillStyle='rgba(199,210,254,.9)';x.font='11px sans-serif';x.textAlign='center';x.fillText(b.w,xx,yy);}
        else{outc++;const tx=hx+(listX-hx)*op, ty=hy-50+i*20*op;
          x.fillStyle='#6366f1';x.fillRect(listX-6,ty-9,3,12);
          x.fillStyle='rgba(255,255,255,'+(0.4+0.6*op)+')';x.font='12px sans-serif';x.textAlign=op>0.5?'left':'center';x.fillText(b.w,op>0.5?listX+4:tx,ty);} });
      x.fillStyle='#fff';x.font='bold 13px sans-serif';x.textAlign='center';x.fillText('🗣️ 話すと…',W/2,24);
      x.font='11px sans-serif';x.fillStyle='rgba(255,255,255,.7)';x.textAlign='center';x.fillText('頭の中 → 整理されたリストへ',W/2,H-8);
      if(p<1)raf=requestAnimationFrame(frame);}
    raf=requestAnimationFrame(frame);}''')

# ============================================================
# 10. 人生の"入力"総決算（生涯 入力時間）＝フラッグシップ Life Grid
# ============================================================
add(id='jinsei-input', cat=V, emoji='⌛',
  title='人生の入力総決算シミュレーター｜一生でキーボードに何年費やす？｜シミュラボ',
  desc='メール・チャット・資料・SNSなど、1日の合計入力時間から、これからの人生でキーボードを打つだけに費やす日数（人生の何％か）と、音声入力で取り戻せる時間を可視化する無料シミュレーター。',
  ogtitle='人生の入力総決算｜一生でキーボードに何年費やす？', ogdesc='1日の入力時間から人生の何％を入力に費やすか可視化。音声で取り戻す。',
  h1='人生の入力総決算シミュレーター',
  lead='メール、チャット、資料、SNS…1日に「文字を打っている」時間を全部足すと、人生でどれだけになるでしょう。残りの人生をマス目にして、入力に消える時間を見える化します。音声入力で取り戻せる時間も。',
  inputs='''    <h2>⌛ 条件を入れる</h2>
    <div class="row"><div class="field"><label>1日の合計入力時間 <span class="hint">（時間・仕事＋プライベート）</span></label><input type="number" id="h" value="3" min="0" max="16" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>これからの年数 <span class="hint">（年）</span></label><input type="number" id="years" value="40" min="1" max="80" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">人生の総決算を見る</button>''',
  result='''      <div class="label">起きている時間のうち 入力に費やす割合</div>
      <div class="big"><span id="big">0</span><span class="unit">％</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">入力に費やす日数</div><div class="v" id="days">—</div></div>
      <div class="stat"><div class="k">音声で取り戻す</div><div class="v accent" id="back">—</div></div>
      <div class="stat"><div class="k">総時間</div><div class="v" id="hh">—</div></div></div>''',
  visual=viz(500,260,520),
  article='''    <div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：1日の入力が3時間なら、起きている時間の約<b>19％</b>を「打つ」ことに使っている計算。40年では<b>180日（昼夜なしで半年以上）</b>に達します。音声入力に切り替えれば、その大半を人生に取り戻せます。</div>
    <h2>あなたの人生を、マス目で見る</h2>
    <p>下のグリッドは「これからの人生の週」です。赤く染まるのが、文字を打つだけに費やす時間。1日数時間の入力でも、生涯では驚くほどの面積を占めます。時間は、お金より取り戻しにくい唯一の資産です。</p>
    <h2>取り戻した時間で、何をする？</h2>
    <p>打つのをやめて話すだけで、入力時間は何分の一にもなります。浮いた時間は、家族と過ごす時間に、学びに、休息に。下の緑のマスが、音声入力で取り戻せる人生の時間です。「打つだけの人生」を、少しでも減らしませんか。</p>'''+TYPELESS+'''
    <h2>よくある質問</h2>'''+faq([
      ('入力時間ってそんなに長い？','仕事のメール・資料に加え、スマホのチャットやSNSを足すと、多くの人が1日2〜4時間に達します。'),
      ('全部を音声化できる？','コードや細かな編集は手入力向きですが、文章の大半は音声化できます。本シミュは2/3を音声化と仮定。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  let raf=0;
  function calc(){const h=Math.max(0,+$('h').value||0),y=Math.max(1,+$('years').value||1);
    const totalH=h*365*y, awakeH=16*365*y, pct=awakeH>0?totalH/awakeH*100:0, days=totalH/24, back=days*2/3;
    $('sub').textContent=`1日${h}時間 × ${y}年`;
    $('days').textContent=num(days)+'日';$('back').textContent=num(back)+'日';$('hh').textContent=num(totalH)+'時間';
    SHARE=`人生の入力総決算シミュ、起きてる時間の約${pct.toFixed(1)}%＝一生で${num(days)}日分も入力に費やす計算でした⌛ 音声入力なら約${num(back)}日取り戻せる。`;
    show();anim($('big'),0,pct,1000,1);startViz(y,h);}
  function startViz(years,h){const c=$('viz'),x=c.getContext('2d'),W=c.width,H=c.height;cancelAnimationFrame(raf);
    const cols=26,rows=clamp(Math.round(years*52/cols),4,24),cell=Math.min(13,(W-40)/cols),gap=2;
    const inputFrac=clamp(h/16,0,1); const total=cols*rows, redN=Math.round(total*inputFrac), greenN=Math.round(redN*2/3);
    const ox=(W-cols*(cell+gap))/2, oy=50, t0=performance.now(),DUR=2600;
    function frame(n){const p=Math.min(1,(n-t0)/DUR);x.fillStyle='#0b1530';x.fillRect(0,0,W,H);
      const phase1=clamp(p*1.7,0,1), phase2=clamp((p-0.6)/0.4,0,1);
      let red=0;
      for(let i=0;i<total;i++){const r=Math.floor(i/cols),col=i%cols;const xx=ox+col*(cell+gap),yy=oy+r*(cell+gap);
        let fill='rgba(160,200,255,.12)';
        if(i<Math.round(redN*phase1)){ red++;
          // later, first greenN of the red turn green (reclaimed)
          if(red<=greenN && phase2>0 && Math.random()<1){ fill = (i < Math.round(greenN*phase2)) ? '#34d399' : '#f43f5e'; }
          else fill='#f43f5e';
          if(i<Math.round(greenN*phase2)) fill='#34d399';
        }
        x.fillStyle=fill;x.fillRect(xx,yy,cell,cell);}
      x.fillStyle='#fff';x.font='bold 13px sans-serif';x.textAlign='center';x.fillText('あなたの残りの人生（マス＝1週間）',W/2,26);
      x.font='11px sans-serif';
      x.fillStyle='#f43f5e';x.textAlign='left';x.fillText('🟥 入力に消える',ox,H-10);
      x.fillStyle='#34d399';x.textAlign='right';x.fillText('🟩 音声で取り戻す',ox+cols*(cell+gap),H-10);
      if(p<1)raf=requestAnimationFrame(frame);}
    raf=requestAnimationFrame(frame);}''')

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
    print(f'typeless done. {len(SIMS)} sims.')
