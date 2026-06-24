# -*- coding: utf-8 -*-
"""シミュラボ：便利ツール・変換計算カテゴリ 10本（SEO高TPの計算/変換ツール）。
新カテゴリ slug=tool「便利ツール」。gen_sims11方式のTPL（try無し・calcは関数スコープ直置き＝バインド確実）。

import安全（SIMSを定義するだけ。書き込みは __main__ ガード内）。
seo_internal.py / gen_images.py のauto-importに 'gen_sims_tool' を追加して使う。
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
        <button class="btn btn-x" id="shareBtn">𝕏 でシェア</button>
        <button class="btn btn-ghost" id="copyBtn">結果をコピー</button>
      </div>
    </div>
  </section>

  <article class="article">
__ARTICLE__
  </article>

  <section class="req-banner">
    <h2>💡 こんなツールも欲しい？</h2>
    <p>あなたの「これ計算したい」を送ってください。投票で人気の案から実際に作ります。</p>
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
  const num = (n) => (Math.round(n*100)/100).toLocaleString('ja-JP');
  const yen = (n) => '¥' + Math.round(n).toLocaleString('ja-JP');
  const sel = (id) => { const e=$(id); return e.options[e.selectedIndex]; };
  const clamp = (v,a,b) => Math.max(a,Math.min(b,v));
  let SHARE = '', raf = 0;
  function show(){ $('resultPanel').style.display=''; $('resultPanel').scrollIntoView({behavior:'smooth',block:'start'}); }
__JS__
  const cb=$('calcBtn'); if(cb) cb.addEventListener('click', calc);
  const sb=$('shareBtn'); if(sb) sb.addEventListener('click', () => window.open('https://twitter.com/intent/tweet?text='+encodeURIComponent(SHARE)+'&url='+encodeURIComponent(location.href)+'&hashtags='+encodeURIComponent('シミュラボ'),'_blank','noopener'));
  const cp=$('copyBtn'); if(cp) cp.addEventListener('click', async () => { try{ await navigator.clipboard.writeText(SHARE+'\\n'+location.href); $('copyBtn').textContent='コピーしました ✓'; setTimeout(()=>$('copyBtn').textContent='結果をコピー',1600);}catch{alert(SHARE);} });
})();
</script>
<script src="../../assets/result-fx.js"></script>
<script src="../../assets/share-counter.js"></script>
<script>ShareCounter.initSim({ simId:'__ID__', badgeEl:document.getElementById('shareCount'), shareBtnIds:['shareBtn'] });</script>
</body>
</html>
'''

CAT = '便利ツール'
def viz(w=480,h=120,mx=500):
    return (f'<canvas id="viz" width="{w}" height="{h}" style="width:100%;max-width:{mx}px;height:auto;'
            f'display:block;margin:0 auto;background:#0b1530;border-radius:12px;"></canvas>')

SIMS=[]
def add(**k):
    k.setdefault('visual','')
    SIMS.append(k)

# ============================================================
# 1. パーセント計算機（パーセント 計算 3800/KD0/TP23000）
# ============================================================
add(id='percent-keisan', emoji='％', cat=CAT,
  title='パーセント計算機｜割合・何％・増減率を一発計算（無料）｜シミュラボ',
  desc='「AはBの何％？」「Bの○％はいくら？」「AからBへの増減は何％？」を一度に計算できる無料のパーセント計算機。割合・歩合・増減率がすぐ分かります。',
  ogtitle='パーセント計算機｜割合・何％・増減率を計算', ogdesc='AはBの何％、Bの○％、増減率を一発計算。無料のパーセント計算機。',
  h1='パーセント計算機',
  lead='2つの数字を入れるだけで、「AはBの何％か」「Bの○％はいくらか」「AからBへの増減率」を同時に計算します。割引・テストの得点率・増減の計算に。',
  inputs='''    <h2>％ 数字を2つ入れる</h2>
    <div class="row"><div class="field"><label>A の値</label><input type="number" id="a" value="30" step="any" inputmode="decimal"></div>
    <div class="field"><label>B の値</label><input type="number" id="b" value="120" step="any" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">計算する</button>''',
  result='''      <div class="label">A は B の</div>
      <div class="big"><span id="big">0</span><span class="unit">％</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">B の A ％</div><div class="v accent" id="pof">—</div></div>
      <div class="stat"><div class="k">A→B の増減</div><div class="v" id="chg">—</div></div>
      <div class="stat"><div class="k">A の B ％</div><div class="v" id="aof">—</div></div></div>''',
  visual=viz(480,70,500),
  article='''    <div class="note"><strong>計算式</strong><br>AはBの何％ ＝ A ÷ B × 100／Bの A％ ＝ B × A ÷ 100／増減率 ＝ (B − A) ÷ A × 100</div>
    <h2>パーセント（％）の計算方法</h2>
    <p>パーセントは「全体を100としたときの割合」です。テストの得点率、割引率、売上の増減など、日常のあらゆる場面で使います。「割合が分からなくなった」ときは、まず「何を全体（100％）にするか」を決めるのがコツです。</p>
    <h2>よくある質問</h2>'''+faq([
      ('「30は120の何％？」は？','30÷120×100＝25％です。上の計算機にA=30, B=120と入れると出ます。'),
      ('増減率がマイナスになるのは？','BがAより小さいときです。減少した割合を表します。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const a=+$('a').value||0,b=+$('b').value||0;
    const pct=b!==0?a/b*100:0, pof=b*a/100, chg=a!==0?(b-a)/a*100:0, aof=a*b/100;
    $('sub').textContent=`A=${num(a)} / B=${num(b)}`;
    $('pof').textContent=num(pof);$('chg').textContent=(chg>=0?'+':'')+num(chg)+'％';$('aof').textContent=num(aof);
    SHARE=`パーセント計算機：${num(a)}は${num(b)}の${num(pct)}％でした％`;show();anim(pct);drawBar(clamp(pct,0,100));}
  function anim(pct){const el=$('big'),t0=performance.now();(function s(n){const p=Math.min(1,(n-t0)/700),e=1-Math.pow(1-p,3);el.textContent=num(pct*e);if(p<1)requestAnimationFrame(s);})(performance.now());}
  function drawBar(pct){const c=$('viz'),x=c.getContext('2d'),W=c.width,H=c.height,bx=16,bw=W-32,by=H/2-12;cancelAnimationFrame(raf);
    const t0=performance.now();function f(n){const p=Math.min(1,(n-t0)/700);x.fillStyle='#0b1530';x.fillRect(0,0,W,H);
      x.fillStyle='rgba(255,255,255,.1)';x.fillRect(bx,by,bw,24);
      const g=x.createLinearGradient(bx,0,bx+bw,0);g.addColorStop(0,'#0fb5c4');g.addColorStop(1,'#6366f1');
      x.fillStyle=g;x.fillRect(bx,by,bw*pct/100*p,24);
      x.fillStyle='#fff';x.font='bold 13px sans-serif';x.textAlign='center';x.fillText(num(pct*p)+'%',W/2,by+42);
      if(p<1)raf=requestAnimationFrame(f);}raf=requestAnimationFrame(f);}''')

# ============================================================
# 2. 分数計算機（分数 計算 2000/KD1/TP49000）
# ============================================================
add(id='bunsuu-keisan', emoji='½', cat=CAT,
  title='分数計算機｜分数の足し算・引き算・かけ算・割り算（約分つき）｜シミュラボ',
  desc='2つの分数の足し算・引き算・かけ算・割り算を、約分・通分まで自動で行う無料の分数計算機。小数への変換結果も表示します。宿題や確認に。',
  ogtitle='分数計算機｜足し算・引き算・かけ算・割り算', ogdesc='2つの分数を約分・通分つきで計算。小数変換も。無料の分数計算機。',
  h1='分数計算機',
  lead='2つの分数と記号（＋−×÷）を選ぶだけで、答えを約分まで自動で計算します。通分や約分が面倒なときに。小数にした値も表示します。',
  inputs='''    <h2>½ 分数を入れる</h2>
    <div class="row"><div class="field"><label>分子1</label><input type="number" id="a" value="1" inputmode="numeric"></div>
    <div class="field"><label>分母1</label><input type="number" id="b" value="2" inputmode="numeric"></div></div>
    <div class="field"><label>計算記号</label><select id="op"><option value="+">＋ 足す</option><option value="-">− 引く</option><option value="*">× かける</option><option value="/">÷ 割る</option></select></div>
    <div class="row"><div class="field"><label>分子2</label><input type="number" id="c" value="1" inputmode="numeric"></div>
    <div class="field"><label>分母2</label><input type="number" id="d" value="3" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">計算する</button>''',
  result='''      <div class="label">答え（約分済み）</div>
      <div class="big" style="font-size:38px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">小数にすると</div><div class="v accent" id="dec">—</div></div>
      <div class="stat"><div class="k">仮分数→帯分数</div><div class="v" id="mixed">—</div></div></div>''',
  article='''    <div class="note"><strong>分数の計算ルール</strong><br>足し算・引き算は通分してから分子を計算／かけ算は分子どうし・分母どうし／割り算は逆数をかける。最後に最大公約数で約分します。</div>
    <h2>分数の計算のしかた</h2>
    <p>分数の足し算・引き算は、分母をそろえる「通分」が必要です。かけ算は分子どうし・分母どうしをかけ、割り算は2つ目の分数をひっくり返して（逆数にして）かけます。答えは必ず「これ以上割り切れない形」まで約分します。この計算機はそれを自動で行います。</p>
    <h2>よくある質問</h2>'''+faq([
      ('帯分数も計算できる？','分子・分母に直して入力してください（例：1と1/2なら 3/2）。'),
      ('約分はどうやってる？','分子と分母の最大公約数（ユークリッドの互除法）で割っています。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function gcd(x,y){x=Math.abs(x);y=Math.abs(y);while(y){[x,y]=[y,x%y];}return x||1;}
  function calc(){let a=Math.trunc(+$('a').value||0),b=Math.trunc(+$('b').value||1),c=Math.trunc(+$('c').value||0),d=Math.trunc(+$('d').value||1),op=$('op').value;
    if(b===0||d===0){$('big').textContent='分母に0は不可';$('sub').textContent='—';$('dec').textContent='—';$('mixed').textContent='—';show();return;}
    let n,m;
    if(op==='+'){n=a*d+c*b;m=b*d;}else if(op==='-'){n=a*d-c*b;m=b*d;}else if(op==='*'){n=a*c;m=b*d;}else{n=a*d;m=b*c;}
    if(m===0){$('big').textContent='計算できません';show();return;}
    if(m<0){n=-n;m=-m;}const g=gcd(n,m);n/=g;m/=g;
    const opl={'+':'＋','-':'−','*':'×','/':'÷'}[op];
    $('big').textContent=(m===1?String(n):n+' / '+m);
    $('sub').textContent=`${a}/${b} ${opl} ${c}/${d}`;
    $('dec').textContent=num(n/m);
    if(m!==1&&Math.abs(n)>=m){const w=Math.trunc(n/m),r=Math.abs(n%m);$('mixed').textContent=(w+' と '+r+'/'+m);}else{$('mixed').textContent='—';}
    SHARE=`分数計算機：${a}/${b} ${opl} ${c}/${d} ＝ ${m===1?n:n+'/'+m} でした`;show();}''')

# ============================================================
# 3. 時間計算機（時間 計算 1800/KD4/TP24000）
# ============================================================
add(id='jikan-keisan', emoji='⏱️', cat=CAT,
  title='時間計算機｜2つの時刻の差・経過時間を計算（日またぎ対応）｜シミュラボ',
  desc='開始時刻と終了時刻から経過時間を計算する無料の時間計算機。日をまたぐ夜勤やイベント時間にも対応。合計分・時給換算も表示します。',
  ogtitle='時間計算機｜2つの時刻の差・経過時間を計算', ogdesc='開始と終了の時刻から経過時間を計算。日またぎ対応の時間計算機。',
  h1='時間計算機（経過時間）',
  lead='開始時刻と終了時刻を入れるだけで、経過時間を「○時間○分」で計算します。日をまたぐ夜勤やイベントにも対応。合計分や時給換算も出ます。',
  inputs='''    <h2>⏱️ 時刻を入れる</h2>
    <div class="row"><div class="field"><label>開始時刻</label><input type="time" id="s" value="09:00"></div>
    <div class="field"><label>終了時刻</label><input type="time" id="e" value="17:30"></div></div>
    <div class="field"><label>時給（任意・換算用） <span class="hint">（円）</span></label><input type="number" id="wage" value="0" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">経過時間を計算</button>''',
  result='''      <div class="label">経過時間</div>
      <div class="big" style="font-size:34px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">合計（分）</div><div class="v accent" id="min">—</div></div>
      <div class="stat"><div class="k">合計（時間）</div><div class="v" id="hour">—</div></div>
      <div class="stat"><div class="k">時給換算</div><div class="v" id="money">—</div></div></div>''',
  article='''    <div class="note"><strong>計算方法</strong><br>経過分 ＝ 終了時刻 − 開始時刻。終了が開始より早い場合は「日またぎ」とみなし、24時間を足して計算します。</div>
    <h2>時間の計算のしかた</h2>
    <p>時間の引き算は「60進法」なので、分が足りないと繰り下げが必要でミスしがち。この計算機は時刻を一度「分」に直して計算するので正確です。勤務時間の集計、夜勤の実働、イベントの所要時間などに使えます。</p>
    <h2>よくある質問</h2>'''+faq([
      ('夜勤（22:00→翌6:00）は？','終了が開始より早いので自動で日またぎ計算し、8時間と表示します。'),
      ('休憩を引きたい','経過時間から休憩分を手で引いてください（休憩入力は今後対応予定）。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const s=$('s').value||'00:00',e=$('e').value||'00:00',w=+$('wage').value||0;
    const [sh,sm]=s.split(':').map(Number),[eh,em]=e.split(':').map(Number);
    let mins=(eh*60+em)-(sh*60+sm);if(mins<0)mins+=1440;
    const h=Math.floor(mins/60),m=mins%60;
    $('big').textContent=`${h}時間${m}分`;$('sub').textContent=`${s} → ${e}`;
    $('min').textContent=num(mins)+'分';$('hour').textContent=num(mins/60)+'時間';$('money').textContent=w>0?yen(mins/60*w):'—';
    SHARE=`時間計算機：${s}〜${e}は ${h}時間${m}分 でした⏱️`;show();}''')

# ============================================================
# 4. 進数変換（16進数 変換 8200/KD2/TP30000）
# ============================================================
add(id='shinsu-henkan', emoji='🔢', cat=CAT,
  title='進数変換ツール｜2進数・8進数・10進数・16進数を相互変換｜シミュラボ',
  desc='2進数・8進数・10進数・16進数を相互に変換できる無料ツール。入力した数値を一度にすべての進数で表示。ビット表示つきでプログラミング学習にも。',
  ogtitle='進数変換ツール｜2進数・10進数・16進数を相互変換', ogdesc='2/8/10/16進数を一度に相互変換。ビット表示つきの進数変換ツール。',
  h1='進数変換ツール（2進・8進・10進・16進）',
  lead='数値と「入力した進数」を選ぶだけで、2進数・8進数・10進数・16進数に一度に変換します。プログラミングやネットワークの学習に。',
  inputs='''    <h2>🔢 数値を入れる</h2>
    <div class="row"><div class="field"><label>数値</label><input type="text" id="v" value="255" inputmode="text" autocomplete="off"></div>
    <div class="field"><label>入力した進数</label><select id="from"><option value="10" selected>10進数</option><option value="2">2進数</option><option value="8">8進数</option><option value="16">16進数</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">変換する</button>''',
  result='''      <div class="label">10進数</div>
      <div class="big" style="font-size:34px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">2進数</div><div class="v accent" id="bin" style="font-size:14px;word-break:break-all;">—</div></div>
      <div class="stat"><div class="k">8進数</div><div class="v" id="oct">—</div></div>
      <div class="stat"><div class="k">16進数</div><div class="v" id="hex">—</div></div></div>''',
  visual=viz(480,70,500),
  article='''    <div class="note"><strong>進数とは</strong><br>2進数は0と1だけ、16進数は0〜9とA〜Fで数を表します。コンピュータは内部で2進数を使い、色コード（#FF0000）などは16進数です。</div>
    <h2>進数変換の使い方</h2>
    <p>「255を16進数にすると？」のような変換が一瞬でできます。10進数255は16進数でFF、2進数で11111111。プログラミング、ネットワーク（IPアドレス・サブネット）、Webの色指定などで進数変換は頻出します。</p>
    <h2>よくある質問</h2>'''+faq([
      ('16進数のアルファベットは大文字？小文字？','本ツールは大文字（FF）で表示します。意味は同じです。'),
      ('負の数や小数は？','本ツールは0以上の整数に対応しています。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const raw=($('v').value||'').trim().replace(/^0[xob]/i,''),fb=+$('from').value;
    const dec=parseInt(raw,fb);
    if(isNaN(dec)||dec<0){$('big').textContent='入力エラー';$('sub').textContent='その進数で使えない文字が含まれています';$('bin').textContent='—';$('oct').textContent='—';$('hex').textContent='—';show();return;}
    const bin=dec.toString(2),oct=dec.toString(8),hex=dec.toString(16).toUpperCase();
    $('big').textContent=num(dec);$('sub').textContent=`入力：${raw}（${fb}進数）`;
    $('bin').textContent=bin;$('oct').textContent=oct;$('hex').textContent=hex;
    SHARE=`進数変換：10進${dec} ＝ 2進${bin} ＝ 16進${hex} でした🔢`;show();drawBits(bin);}
  function drawBits(bin){const c=$('viz'),x=c.getContext('2d'),W=c.width,H=c.height;cancelAnimationFrame(raf);
    const bits=bin.padStart(Math.ceil(bin.length/4)*4,'0').slice(-32).split('');
    const n=bits.length,bw=Math.min(26,(W-20)/n),sx=(W-n*bw)/2,by=H/2-bw/2,t0=performance.now();
    function f(t){const p=Math.min(1,(t-t0)/600);x.fillStyle='#0b1530';x.fillRect(0,0,W,H);
      bits.forEach((b,i)=>{const on=b==='1',show=i<n*p;x.fillStyle=show?(on?'#34d399':'rgba(255,255,255,.12)'):'rgba(255,255,255,.04)';
        x.fillRect(sx+i*bw,by,bw-2,bw-2);if(show){x.fillStyle=on?'#06281f':'rgba(255,255,255,.5)';x.font='bold 12px monospace';x.textAlign='center';x.textBaseline='middle';x.fillText(b,sx+i*bw+(bw-2)/2,by+(bw-2)/2);}});
      if(p<1)raf=requestAnimationFrame(f);}raf=requestAnimationFrame(f);}''')

# ============================================================
# 5. 西暦・和暦・年齢変換（西暦 和暦 変換 / 令和何年 TP819000）
# ============================================================
add(id='wareki-henkan', emoji='📅', cat=CAT,
  title='西暦・和暦変換＆年齢計算｜令和・平成・昭和は何年？｜シミュラボ',
  desc='西暦を入れると令和・平成・昭和などの和暦、その年生まれの今年の年齢、干支（えと）をまとめて表示する無料の西暦和暦変換ツール。',
  ogtitle='西暦・和暦変換＆年齢計算｜令和・平成は何年？', ogdesc='西暦から和暦・年齢・干支を一発変換。令和何年がすぐ分かる。',
  h1='西暦・和暦変換＆年齢計算',
  lead='西暦（年）を入れるだけで、令和・平成・昭和などの和暦、その年生まれの人の今年の年齢、干支（えと）をまとめて表示します。「令和○年は西暦何年？」の逆引きにも。',
  inputs='''    <h2>📅 西暦（年）を入れる</h2>
    <div class="field"><label>西暦 <span class="hint">（例：2000）</span></label><input type="number" id="y" value="2000" min="1868" max="2100" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">和暦・年齢を見る</button>''',
  result='''      <div class="label">和暦</div>
      <div class="big" style="font-size:34px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">その年生まれの今年の年齢</div><div class="v accent" id="age">—</div></div>
      <div class="stat"><div class="k">干支（えと）</div><div class="v" id="eto">—</div></div>
      <div class="stat"><div class="k">西暦</div><div class="v" id="seireki">—</div></div></div>''',
  article='''    <div class="note"><strong>和暦の区切り（改元）</strong><br>令和：2019年5月〜／平成：1989〜2019／昭和：1926〜1989／大正：1912〜1926／明治：1868〜1912</div>
    <h2>西暦と和暦の変換</h2>
    <p>「令和○年は西暦何年？」「平成○年生まれは今いくつ？」と迷ったときに。改元のあった年は2つの元号にまたがるため、月によって和暦が変わる点に注意してください（本ツールは年単位での目安です）。干支は12年周期で、西暦を12で割った余りから求めます。</p>
    <h2>よくある質問</h2>'''+faq([
      ('令和7年は西暦何年？','2025年です。令和は2019年が元年（令和1年）なので、令和○年＝2018＋○年です。'),
      ('年齢は満年齢？','その年に生まれた人が今年迎える満年齢の目安です（誕生日前なら−1歳）。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const y=Math.trunc(+$('y').value||0);
    if(y<1868||y>2100){$('big').textContent='1868〜2100で入力';show();return;}
    let g,gy;if(y>=2019){g='令和';gy=y-2018;}else if(y>=1989){g='平成';gy=y-1988;}else if(y>=1926){g='昭和';gy=y-1925;}else if(y>=1912){g='大正';gy=y-1911;}else{g='明治';gy=y-1867;}
    const now=new Date().getFullYear()||2026;const age=now-y;
    const ETO=['申','酉','戌','亥','子','丑','寅','卯','辰','巳','午','未'];const eto=ETO[y%12];
    $('big').textContent=`${g}${gy===1?'元':gy}年`;$('sub').textContent=`西暦 ${y} 年`;
    $('age').textContent=age+'歳';$('eto').textContent=eto+'年';$('seireki').textContent=y+'年';
    SHARE=`西暦${y}年は ${g}${gy===1?'元':gy}年（${eto}年）でした📅`;show();}''')

# ============================================================
# 6. 日数計算機（日数計算 35000/KD39/TP74000）
# ============================================================
add(id='nissu-keisan', emoji='🗓️', cat=CAT,
  title='日数計算機｜2つの日付の間は何日？あと何日かを計算｜シミュラボ',
  desc='開始日と終了日を入れるだけで、その間の日数・週数・おおよその月数を計算する無料の日数計算機。記念日や締め切りまでの「あと何日」にも使えます。',
  ogtitle='日数計算機｜2つの日付の間は何日？', ogdesc='開始日と終了日から日数・週数・月数を計算。あと何日もすぐ分かる。',
  h1='日数計算機（日付の差）',
  lead='2つの日付を入れるだけで、その間が何日あるかを計算します。週数・おおよその月数も表示。記念日からの経過日数や、締め切り・イベントまでの「あと何日」に。',
  inputs='''    <h2>🗓️ 日付を2つ入れる</h2>
    <div class="row"><div class="field"><label>開始日</label><input type="date" id="d1" value="2026-01-01"></div>
    <div class="field"><label>終了日</label><input type="date" id="d2" value="2026-12-31"></div></div>
    <button class="btn btn-primary" id="calcBtn">日数を計算</button>''',
  result='''      <div class="label">2つの日付の間は</div>
      <div class="big"><span id="big">0</span><span class="unit">日</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">週にすると</div><div class="v accent" id="wk">—</div></div>
      <div class="stat"><div class="k">およそ何ヶ月</div><div class="v" id="mo">—</div></div>
      <div class="stat"><div class="k">時間にすると</div><div class="v" id="hr">—</div></div></div>''',
  article='''    <div class="note"><strong>計算方法</strong><br>日数 ＝ (終了日 − 開始日) ÷ 1日。終了日が開始日より前なら、マイナス（過去）として表示します。</div>
    <h2>日数の計算のしかた</h2>
    <p>「ある日からある日まで何日あるか」は、カレンダーを数えると間違えがち。この計算機は日付を内部で計算するので正確です。記念日からの経過日数、締め切りまでの残り日数、契約・保証期間の確認などに使えます。</p>
    <h2>よくある質問</h2>'''+faq([
      ('当日を含む？含まない？','本ツールは「2つの日付の差」です。当日を含めたい場合は＋1日してください。'),
      ('未来の日付でも？','はい。終了日を未来にすれば「あと何日」が分かります。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const a=$('d1').value,b=$('d2').value;if(!a||!b){$('big').textContent='0';show();return;}
    const d1=new Date(a+'T00:00:00'),d2=new Date(b+'T00:00:00');
    const days=Math.round((d2-d1)/86400000);
    $('sub').textContent=`${a} → ${b}`;
    $('wk').textContent=num(days/7)+'週';$('mo').textContent=num(days/30.4)+'ヶ月';$('hr').textContent=num(days*24)+'時間';
    SHARE=`日数計算機：${a}〜${b}は ${num(days)}日 でした🗓️`;show();animN(days);}
  function animN(v){const el=$('big'),t0=performance.now();(function s(n){const p=Math.min(1,(n-t0)/700),e=1-Math.pow(1-p,3);el.textContent=Math.round(v*e).toLocaleString('ja-JP');if(p<1)requestAnimationFrame(s);})(performance.now());}''')

# ============================================================
# 7. 確率計算機（確率 計算 1200/KD2/TP11000）
# ============================================================
add(id='kakuritsu-keisan', emoji='🎲', cat=CAT,
  title='確率計算機｜○％を何回引けば当たる？ガチャの当選確率を計算｜シミュラボ',
  desc='排出率（％）と試行回数から、「1回以上当たる確率」を計算する無料の確率計算機。ガチャ・くじ・抽選の当たりやすさが分かります。50％・90％に必要な回数も。',
  ogtitle='確率計算機｜○％を何回引けば当たる？', ogdesc='排出率と回数から1回以上当たる確率を計算。ガチャの当選確率に。',
  h1='確率計算機（1回以上当たる確率）',
  lead='排出率（％）と引く回数を入れると、「1回以上当たる確率」を計算します。ガチャ・くじ・抽選で「これだけ引けばどれくらい当たるか」が分かります。',
  inputs='''    <h2>🎲 条件を入れる</h2>
    <div class="row"><div class="field"><label>1回の当たる確率 <span class="hint">（％）</span></label><input type="number" id="p" value="3" step="any" min="0" max="100" inputmode="decimal"></div>
    <div class="field"><label>引く回数 <span class="hint">（回）</span></label><input type="number" id="n" value="30" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">当たる確率を計算</button>''',
  result='''      <div class="label">1回以上 当たる確率</div>
      <div class="big"><span id="big">0</span><span class="unit">％</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">50％に必要な回数</div><div class="v accent" id="half">—</div></div>
      <div class="stat"><div class="k">90％に必要な回数</div><div class="v" id="n90">—</div></div>
      <div class="stat"><div class="k">期待される当たり数</div><div class="v" id="exp">—</div></div></div>''',
  visual=viz(480,70,500),
  article='''    <div class="note"><strong>計算式</strong><br>1回以上当たる確率 ＝ 1 −（1 − 当たる確率）^回数。「1回も当たらない確率」を1から引いて求めます。</div>
    <h2>ガチャの確率の考え方</h2>
    <p>「3％を30回引けば当たるはず」と思いがちですが、実際は1回以上当たる確率は約60％。何回引いても「絶対に当たる」わけではありません（独立試行）。50％・90％に達する回数も出すので、天井のないガチャの“引き際”の参考に。</p>
    <h2>よくある質問</h2>'''+faq([
      ('3％を33回で100％？','いいえ。約63％です。試行は独立なので確率は100％になりません。'),
      ('期待される当たり数とは？','確率×回数の平均値です。0.9個なら「平均1個未満」を意味します。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const p=clamp(+$('p').value||0,0,100)/100,n=Math.max(0,Math.trunc(+$('n').value||0));
    const atLeast=p>0?(1-Math.pow(1-p,n))*100:0,exp=p*n;
    const need=(t)=>p>0&&p<1?Math.ceil(Math.log(1-t)/Math.log(1-p)):(p>=1?1:'∞');
    $('sub').textContent=`1回${num(p*100)}％ × ${n}回`;
    $('half').textContent=need(0.5)+'回';$('n90').textContent=need(0.9)+'回';$('exp').textContent=num(exp)+'個';
    SHARE=`確率計算機：${num(p*100)}％を${n}回引くと1回以上当たる確率は${num(atLeast)}％でした🎲`;show();animP(atLeast);drawBar(clamp(atLeast,0,100));}
  function animP(v){const el=$('big'),t0=performance.now();(function s(n){const p=Math.min(1,(n-t0)/700),e=1-Math.pow(1-p,3);el.textContent=num(v*e);if(p<1)requestAnimationFrame(s);})(performance.now());}
  function drawBar(pct){const c=$('viz'),x=c.getContext('2d'),W=c.width,H=c.height,bx=16,bw=W-32,by=H/2-12;cancelAnimationFrame(raf);
    const t0=performance.now();function f(n){const p=Math.min(1,(n-t0)/700);x.fillStyle='#0b1530';x.fillRect(0,0,W,H);
      x.fillStyle='rgba(255,255,255,.1)';x.fillRect(bx,by,bw,24);const g=x.createLinearGradient(bx,0,bx+bw,0);g.addColorStop(0,'#f59e0b');g.addColorStop(1,'#f43f5e');
      x.fillStyle=g;x.fillRect(bx,by,bw*pct/100*p,24);x.fillStyle='#fff';x.font='bold 13px sans-serif';x.textAlign='center';x.fillText(num(pct*p)+'%',W/2,by+42);
      if(p<1)raf=requestAnimationFrame(f);}raf=requestAnimationFrame(f);}''')

# ============================================================
# 8. 単位変換（単位変換 3100/KD4）
# ============================================================
add(id='tani-henkan', emoji='📐', cat=CAT,
  title='単位変換ツール｜長さ・重さ・面積・容量をまとめて換算｜シミュラボ',
  desc='長さ（cm・m・inch等）・重さ（g・kg・lb等）・面積（㎡・坪・畳）・容量（mL・L・合）を相互に換算できる無料の単位変換ツール。',
  ogtitle='単位変換ツール｜長さ・重さ・面積・容量を換算', ogdesc='cm⇔inch、kg⇔lb、㎡⇔坪⇔畳などをまとめて換算。無料の単位変換。',
  h1='単位変換ツール',
  lead='種類を選んで数値を入れるだけ。長さ・重さ・面積・容量の単位を相互に換算します。「坪は何㎡？」「インチは何cm？」がすぐ分かります。',
  inputs='''    <h2>📐 換算する</h2>
    <div class="field"><label>種類</label><select id="cat"><option value="length">長さ</option><option value="weight">重さ</option><option value="area">面積</option><option value="volume">容量</option></select></div>
    <div class="row"><div class="field"><label>数値</label><input type="number" id="v" value="1" step="any" inputmode="decimal"></div>
    <div class="field"><label>変換元</label><select id="from"></select></div></div>
    <div class="field"><label>変換先</label><select id="to"></select></div>
    <button class="btn btn-primary" id="calcBtn">換算する</button>''',
  result='''      <div class="label">換算結果</div>
      <div class="big" style="font-size:34px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">逆向き（1単位）</div><div class="v accent" id="rev">—</div></div></div>''',
  article='''    <div class="note"><strong>よく使う換算</strong><br>1インチ＝2.54cm／1フィート＝30.48cm／1ポンド＝453.6g／1坪＝約3.31㎡＝2畳／1合＝180mL</div>
    <h2>単位変換の使い方</h2>
    <p>海外サイトの「インチ表記」、レシピの「ポンド・カップ」、不動産の「坪・畳」など、ふだん使わない単位に出会ったときに。種類を選んで数値と単位を指定するだけで換算できます。</p>
    <h2>よくある質問</h2>'''+faq([
      ('畳の広さは地域で違う？','本ツールは1畳＝1.6562㎡（中京間に近い目安）で計算しています。地域・物件で多少差があります。'),
      ('温度の変換は？','本ツールは長さ・重さ・面積・容量に対応。温度は今後追加予定です。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  const U={length:{'mm':1,'cm':10,'m':1000,'km':1000000,'inch':25.4,'feet':304.8,'yard':914.4,'mile':1609344},
    weight:{'mg':1,'g':1000,'kg':1000000,'t':1000000000,'oz':28349.5,'lb':453592},
    area:{'cm2':1,'m2':10000,'km2':10000000000,'坪':33057.85,'畳':16562,'ha':100000000},
    volume:{'mL':1,'L':1000,'cc':1,'合':180.39,'升':1803.9,'cup':200,'gallon':3785.41}};
  function fill(){const cat=$('cat').value,ks=Object.keys(U[cat]);
    const o=ks.map(k=>'<option>'+k+'</option>').join('');$('from').innerHTML=o;$('to').innerHTML=o;$('to').selectedIndex=Math.min(1,ks.length-1);}
  $('cat').addEventListener('change',fill);
  function calc(){const cat=$('cat').value,v=+$('v').value||0,fu=$('from').value,tu=$('to').value;
    const r=v*U[cat][fu]/U[cat][tu],rev=U[cat][tu]/U[cat][fu];
    $('big').textContent=num(r)+' '+tu;$('sub').textContent=`${num(v)} ${fu} =`;
    $('rev').textContent=`1 ${tu} = ${num(rev)} ${fu}`;
    SHARE=`単位変換：${num(v)}${fu} = ${num(r)}${tu} でした📐`;show();}
  fill();''')

# ============================================================
# 9. 速さ・距離・時間（速さ 計算）
# ============================================================
add(id='hayasa-keisan', emoji='🚗', cat=CAT,
  title='速さ・距離・時間の計算機（はじき）｜2つ入れて1つを計算｜シミュラボ',
  desc='速さ・距離・時間のうち2つを入れると残り1つを計算する無料ツール（「はじき」の計算）。km/h・分・kmで時速や所要時間、移動距離が分かります。',
  ogtitle='速さ・距離・時間の計算機（はじき）', ogdesc='速さ・距離・時間の2つから残りを計算。時速や所要時間がすぐ出る。',
  h1='速さ・距離・時間の計算機',
  lead='「はじき」の計算を自動化。求めたいものを選び、残り2つを入れるだけ。時速、所要時間、移動距離をサッと計算できます。',
  inputs='''    <h2>🚗 求めたいものを選ぶ</h2>
    <div class="field"><label>計算するもの</label><select id="mode"><option value="speed">速さ（km/h）</option><option value="dist">距離（km）</option><option value="time">時間（分）</option></select></div>
    <div class="row"><div class="field"><label>距離 <span class="hint">（km）</span></label><input type="number" id="d" value="60" step="any" inputmode="decimal"></div>
    <div class="field"><label>時間 <span class="hint">（分）</span></label><input type="number" id="t" value="90" step="any" inputmode="decimal"></div></div>
    <div class="field"><label>速さ <span class="hint">（km/h）</span></label><input type="number" id="s" value="40" step="any" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">計算する</button>''',
  result='''      <div class="label">計算結果</div>
      <div class="big" style="font-size:34px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">参考：分速</div><div class="v accent" id="mps">—</div></div>
      <div class="stat"><div class="k">参考：秒速</div><div class="v" id="sps">—</div></div></div>''',
  article='''    <div class="note"><strong>3つの関係（はじき）</strong><br>速さ ＝ 距離 ÷ 時間／距離 ＝ 速さ × 時間／時間 ＝ 距離 ÷ 速さ<br>※本ツールは距離km・時間分・速さkm/h で計算します。</div>
    <h2>速さ・距離・時間の計算</h2>
    <p>「時速40kmで60km走ると何分？」のような計算を自動化します。求めたいもの（速さ・距離・時間）を選び、残りの2つを入れてください。通勤・ドライブ・ランニングの計画に。</p>
    <h2>よくある質問</h2>'''+faq([
      ('単位は固定？','距離km・時間分・速さkm/hです。分は内部で時間に直して計算します。'),
      ('時速を分速・秒速にも？','はい。結果の下に分速（m/分）・秒速（m/秒）も表示します。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const m=$('mode').value,d=+$('d').value||0,t=+$('t').value||0,s=+$('s').value||0;let r,unit,label,kmh;
    if(m==='speed'){kmh=t>0?d/(t/60):0;r=num(kmh);unit='km/h';label='速さ';$('sub').textContent=`${num(d)}km を ${num(t)}分で`;}
    else if(m==='dist'){const dist=s*(t/60);kmh=s;r=num(dist);unit='km';label='距離';$('sub').textContent=`時速${num(s)}km で ${num(t)}分`;}
    else{const min=s>0?d/s*60:0;kmh=s;r=num(min);unit='分';label='時間';$('sub').textContent=`${num(d)}km を 時速${num(s)}km で`;}
    $('big').textContent=r+' '+unit;
    $('mps').textContent=num(kmh*1000/60)+' m/分';$('sps').textContent=num(kmh*1000/3600)+' m/秒';
    SHARE=`速さ・距離・時間の計算機：${label}は ${r}${unit} でした🚗`;show();}''')

# ============================================================
# 10. 文字数カウント（文字数カウント 1130000/KD42/TP1650000）★本丸
# ============================================================
add(id='moji-count', emoji='✍️', cat=CAT,
  title='文字数カウントツール｜文字数・原稿用紙・ツイート数を即カウント｜シミュラボ',
  desc='文章を貼り付けるだけで、文字数（空白あり/なし）・行数・段落数・原稿用紙の枚数・X(Twitter)の投稿可否・読了時間をリアルタイムでカウントする無料ツール。',
  ogtitle='文字数カウントツール｜文字数・原稿用紙を即カウント', ogdesc='貼り付けるだけで文字数・原稿用紙・ツイート数・読了時間をカウント。',
  h1='文字数カウントツール',
  lead='文章を貼り付けるだけで、文字数（空白あり・なし）、行数、段落数、原稿用紙の枚数、X(旧Twitter)に収まるか、読むのにかかる時間をリアルタイムで表示します。',
  inputs='''    <h2>✍️ 文章を貼り付ける</h2>
    <textarea id="txt" rows="7" placeholder="ここに文章を入力・貼り付け" style="width:100%;font-size:15px;padding:12px;border:1.5px solid var(--line);border-radius:10px;line-height:1.7;"></textarea>
    <button class="btn btn-primary" id="calcBtn" style="margin-top:10px;">カウントする</button>''',
  result='''      <div class="label">文字数（空白含む）</div>
      <div class="big"><span id="big">0</span><span class="unit">字</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">空白・改行なし</div><div class="v accent" id="nospace">—</div></div>
      <div class="stat"><div class="k">行数 / 段落</div><div class="v" id="lines">—</div></div>
      <div class="stat"><div class="k">原稿用紙(400字)</div><div class="v" id="genko">—</div></div>
      <div class="stat"><div class="k">X(140字)</div><div class="v" id="tw">—</div></div>
      <div class="stat"><div class="k">読了時間(400字/分)</div><div class="v" id="read">—</div></div></div>''',
  article='''    <div class="note"><strong>こんなときに</strong><br>レポート・小論文の字数チェック、ブログ・記事の文字数、X(Twitter)の投稿可否、原稿用紙の枚数換算などに。入力中もリアルタイムで更新されます。</div>
    <h2>文字数カウントの使い方</h2>
    <p>テキストエリアに文章を貼り付けるだけ。空白・改行を含む文字数と、含まない文字数の両方を表示します。「400字以内」「2000字以上」といった指定のある課題や、SNS投稿の字数管理に便利です。入力はすべて手元のブラウザ内で処理され、外部に送信されません。</p>
    <h2>よくある質問</h2>'''+faq([
      ('全角・半角は区別する？','文字数は1文字＝1としてカウントします（全角半角の重み付けはしません）。'),
      ('入力した文章は保存される？','いいえ。すべてブラウザ内で処理され、どこにも送信・保存されません。'),
      ('Xの文字数は？','本ツールは日本語の目安として140字で判定します。')]),
  js=r'''  function calc(){const t=$('txt').value||'';
    const all=Array.from(t).length;
    const nospace=Array.from(t.replace(/\s/g,'')).length;
    const lines=t===''?0:t.split(/\n/).length;
    const paras=t.trim()===''?0:t.trim().split(/\n\s*\n/).length;
    $('big').textContent=num(all);$('sub').textContent=all===0?'文章を入力してください':'リアルタイムで更新されます';
    $('nospace').textContent=num(nospace)+'字';$('lines').textContent=lines+' / '+paras;
    $('genko').textContent=num(Math.ceil(all/400))+'枚';
    $('tw').textContent=all<=140?('OK（あと'+(140-all)+'）'):('超過 '+(all-140));
    $('read').textContent=num(Math.ceil(all/400))+'分';
    SHARE=`文字数カウント：${num(all)}字（空白なし${num(nospace)}字）でした✍️`;
    if($('resultPanel').style.display==='none')show();}
  $('txt').addEventListener('input',calc);''')

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
    print(f'tool done. {len(SIMS)} sims.')
