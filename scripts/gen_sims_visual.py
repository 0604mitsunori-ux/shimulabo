# -*- coding: utf-8 -*-
"""シミュラボ：SEO狙いのリッチアニメ系canvasシミュ 10本を生成。

KW（jp実測 vol/KD）:
 雪の結晶26000/3, 三体問題8700/0, ドップラー効果7400/0, ニュートンのゆりかご2100/0,
 バブルソート1100/0, ボロノイ図1000/0, パーリンノイズ500/0, コッホ曲線400/0,
 モンテカルロ法 円周率250/0, ダブルスリット実験(TP5100)/2

import安全（SIMSを定義するだけ。書き込みは __main__ ガード内）。
seo_internal.py / gen_images.py の取り込みループに 'gen_sims_visual' を追加して使う。
"""
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

CV = '<canvas id="cv" width="__W__" height="__H__" style="width:100%;max-width:__MX__px;height:auto;background:#fff;border:1px solid var(--line);border-radius:12px;__XTRA__"></canvas>'

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
    <div style="display:grid;place-items:center;gap:16px;">
      __CANVAS__
      <div style="width:100%;max-width:560px;">__CONTROLS__</div>
    </div>
    <p style="text-align:center;color:var(--ink-2);font-size:13px;margin-top:14px;">__LEGEND__</p>
    <div style="text-align:center;"><span id="shareCount" class="share-count" style="display:none"></span></div>
    <div class="share-row"><button class="btn btn-x" id="shareBtn">𝕏 でシェア</button></div>
  </section>

  <article class="article">
__ARTICLE__
  </article>

  <section class="req-banner">
    <h2>💡 こんなシミュも見てみたい？</h2>
    <p>あなたの「これ見てみたい」を送ってください。投票で人気の案から実際に作ります。</p>
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
  const SHARE = '__SHARE__';
  try {
__JS__
  } catch(e) { console.error(e); }
  const sb=$('shareBtn'); if(sb) sb.addEventListener('click',()=>window.open('https://twitter.com/intent/tweet?text='+encodeURIComponent(SHARE)+'&url='+encodeURIComponent(location.href)+'&hashtags='+encodeURIComponent('シミュラボ'),'_blank','noopener'));
})();
</script>
<script src="../../assets/share-counter.js"></script>
<script>ShareCounter.initSim({ simId:'__ID__', badgeEl:document.getElementById('shareCount'), shareBtnIds:['shareBtn'] });</script>
</body>
</html>
'''

def faq(qa):
    return '<dl class="faq">' + ''.join(f'<dt>{q}</dt><dd>{a}</dd>' for q,a in qa) + '</dl>'

def refs(items):
    return '<h2>参考</h2><ul class="seo-refs">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'

def canvas(w,h,mx,xtra=''):
    return CV.replace('__W__',str(w)).replace('__H__',str(h)).replace('__MX__',str(mx)).replace('__XTRA__',xtra)

def btn(id,label,primary=False):
    cls='btn btn-primary' if primary else 'btn btn-ghost'
    return f'<button class="{cls}" id="{id}" style="padding:11px 18px;font-size:14px;">{label}</button>'

def row(*items):
    return '<div class="share-row" style="margin-top:0;flex-wrap:wrap;">'+''.join(items)+'</div>'

def slider(id,label,mn,mx,val,step='1'):
    return (f'<div class="field" style="margin-bottom:10px;"><div class="slider-head"><label style="margin:0;">{label}</label>'
            f'<span class="val" id="{id}L">{val}</span></div>'
            f'<input type="range" id="{id}" min="{mn}" max="{mx}" value="{val}" step="{step}" style="width:100%;"></div>')

def select(id,label,opts):
    o=''.join(f'<option value="{v}">{t}</option>' for v,t in opts)
    return f'<div class="field" style="margin-bottom:10px;"><label>{label}</label><select id="{id}">{o}</select></div>'

def readout(id,text='—'):
    return (f'<div id="{id}" style="text-align:center;font-weight:800;font-size:15px;color:var(--ink);'
            f'background:var(--bg-2,#f6f8fb);border:1px solid var(--line);border-radius:10px;padding:10px;margin-bottom:10px;">{text}</div>')

WONDER='ふしぎ・現象'; PLAY='あそぶ・実験'
SIMS=[]

# ============================================================
# 1. 雪の結晶ジェネレーター（雪の結晶 26000/3）
# ============================================================
SIMS.append(dict(id='snowflake', emoji='❄️', cat=WONDER, slug='wonder', score=72,
  short='雪の結晶ジェネレーター', carddesc='ボタンを押すたび、世界に一つだけの六角形の雪の結晶が育つ。',
  title='雪の結晶ジェネレーター｜世界に一つの結晶を作る無料シミュレーター｜シミュラボ',
  desc='ボタンを押すたびに、二度と同じものができない六角形の雪の結晶が枝を伸ばして育つ無料シミュレーター。雪の結晶がなぜ六角形で左右対称になるのか、その仕組みも解説します。',
  ogtitle='雪の結晶ジェネレーター｜世界に一つの結晶を作る', ogdesc='ボタンを押すたびに二度と同じものができない六角形の雪の結晶が育つ。',
  h1='雪の結晶ジェネレーター',
  lead='雪の結晶は、ひとつとして同じものがありません。ボタンを押すたびに、六角形の対称をもった「あなただけの雪の結晶」が枝を伸ばして育ちます。気に入った結晶はスクショして残してください。',
  canvas=canvas(420,420,440,'background:#0b1530;cursor:pointer;'),
  controls=slider('cplx','枝の複雑さ','3','9','6')+row(btn('again','❄️ 新しい結晶を作る',True)),
  legend='ボタンを押すたびに別の結晶が生まれます。スライダーで枝の複雑さを変えられます。',
  article='''    <div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：雪の結晶が六角形になるのは、水の分子が水素結合で<b>120度</b>＝六方対称に並ぶから。枝の細かい形は落ちてくる間の<b>気温と湿度</b>で決まり、同じ環境を二度と通らないため「同じ結晶は二つとない」と言われます。</div>
    <h2>雪の結晶はなぜ六角形なのか</h2>
    <p>雪の結晶（雪結晶）は、上空で水蒸気が氷の粒に直接くっついて成長したものです。水分子は酸素1個と水素2個が約104.5度の角度で結びついており、氷になるとこの分子が規則正しく並びます。その並び方が正六角形を基本とするため、結晶も六方対称（6回対称）になります。</p>
    <h2>同じ結晶が二つとないのはなぜ？</h2>
    <p>結晶は落下しながら、気温や湿度の違う層を次々に通過します。枝が伸びる速さや枝分かれのしかたは、その瞬間の環境で変わります。6本の腕はほぼ同時に同じ環境を通るので互いによく似ますが、別の結晶が同じ落下経路をたどることはまずありません。これが「世界に一つだけ」と言われる理由です。本シミュレーターも、生成のたびに乱数の種を変えて二度と同じ形を作りません。</p>
    <table class="seo-table">
      <tr><th>気温</th><th>できやすい形</th></tr>
      <tr><td>0〜-4℃</td><td>六角板・薄い板状</td></tr>
      <tr><td>-4〜-10℃</td><td>針状・柱状</td></tr>
      <tr><td>-10〜-22℃</td><td>樹枝状（よく見る星型）</td></tr>
      <tr><td>-22℃以下</td><td>厚い板・柱状</td></tr>
    </table>
    <h2>よくある質問</h2>'''+faq([
      ('雪の結晶は本当に全部ちがう形ですか？','枝の細部まで完全に一致することは現実にはほぼ起こらないとされます。一方で、ごく単純な六角板どうしならよく似ることもあります。'),
      ('なぜ6本の腕がそっくりなの？','6本はほぼ同時に同じ気温・湿度を経験するため、同じように成長するからです。'),
      ('保存できますか？','スクリーンショットで保存してください。計算はすべてブラウザ内で完結し、データは送信されません。')])
    +refs([
      'ナカヤ（中谷宇吉郎）の研究：気温・過飽和度と結晶形の関係（中谷ダイヤグラム）',
      'Libbrecht, K. G. "The physics of snow crystals" (Reports on Progress in Physics, 2005)',
      '気象庁「雪結晶の観察」']),
  share='ボタンを押すたび、世界に一つだけの雪の結晶が育つ❄️ あなたの結晶はどんな形？',
  js='''  const c=$('cv'),x=c.getContext('2d'),W=c.width,H=c.height,cx=W/2,cy=H/2;
  let seed=1,P=null,grow=0,raf=0;
  function rng(s){let z=s>>>0;return ()=>{z=(z*1664525+1013904223)>>>0;return z/4294967296;};}
  function build(){const r=rng(seed),cp=+$('cplx').value;$('cplxL').textContent=cp;
    const len=140+r()*40, n=2+(cp*0.7|0), br=[];
    for(let i=0;i<n;i++){const pos=len*(0.18+0.72*(i+1)/(n+1));
      br.push({pos:pos,len:len*(0.22+r()*0.28), ang:0.45+r()*0.45, tip:r()<0.5});}
    P={len:len, w:1.4+r()*1.6, br:br, plate:0.10+r()*0.10};}
  function arm(g){const L=P.len*g;
    x.beginPath();x.moveTo(0,0);x.lineTo(0,-L);x.stroke();
    if(L>P.len*P.plate){const s=P.len*P.plate;x.save();x.translate(0,-s);x.beginPath();
      for(let k=0;k<6;k++){const a=k*Math.PI/3-Math.PI/2,rr=P.len*0.06;x.lineTo(Math.cos(a)*rr,Math.sin(a)*rr);}x.closePath();x.stroke();x.restore();}
    for(const b of P.br){if(L>b.pos){const bl=Math.min(L-b.pos,b.len);
      for(const sgn of [-1,1]){x.save();x.translate(0,-b.pos);x.rotate(sgn*b.ang);
        x.beginPath();x.moveTo(0,0);x.lineTo(0,-bl);x.stroke();
        if(b.tip&&bl>b.len*0.6){x.save();x.translate(0,-bl);x.rotate(sgn*0.5);x.beginPath();x.moveTo(0,0);x.lineTo(0,-b.len*0.3);x.stroke();x.restore();}
        x.restore();}}}}
  function draw(){x.clearRect(0,0,W,H);x.save();x.translate(cx,cy);
    x.shadowColor='#9fe8ff';x.shadowBlur=12;x.strokeStyle='#eaffff';x.lineWidth=P.w;x.lineCap='round';
    for(let i=0;i<6;i++){x.save();x.rotate(i*Math.PI/3);arm(grow);x.restore();}
    x.restore();}
  function start(){seed=(Math.random()*1e9)>>>0;build();grow=0;cancelAnimationFrame(raf);loop();}
  function loop(){grow=Math.min(1,grow+0.022);draw();if(grow<1)raf=requestAnimationFrame(loop);}
  $('again').addEventListener('click',start);
  $('cplx').addEventListener('input',()=>{$('cplxL').textContent=$('cplx').value;build();grow=0;cancelAnimationFrame(raf);loop();});
  build();start();'''))

# ============================================================
# 2. 三体問題シミュレーター（三体問題 8700/0, TP18000）
# ============================================================
SIMS.append(dict(id='three-body', emoji='🌌', cat=WONDER, slug='wonder', score=70,
  short='三体問題シミュレーター', carddesc='3つの星が引き合うだけで予測不能のカオス軌道に。',
  title='三体問題シミュレーター｜3つの星のカオスを体感する無料ツール｜シミュラボ',
  desc='3つの星がお互いの重力で引き合うだけなのに、軌道がぐちゃぐちゃに乱れて二度と同じにならない「三体問題」のカオスをブラウザで体感できる無料シミュレーター。なぜ未来が計算できないのかも解説。',
  ogtitle='三体問題シミュレーター｜3つの星のカオスを体感', ogdesc='3つの星が引き合うだけで予測不能のカオス軌道に。三体問題を体感。',
  h1='三体問題シミュレーター',
  lead='星が2つなら軌道はきれいな楕円。ところが3つになると、お互いの重力で引き合うだけで動きは予測不能のカオスに。これが300年解かれていない「三体問題」です。リセットするたびに、まったく違う運命が生まれます。',
  canvas=canvas(480,400,520,'background:#05060f;'),
  controls=slider('spd','時間の速さ','1','6','3')+row(btn('reset','🌌 別の初期配置で始める',True),btn('clr','軌跡を消す')),
  legend='3つの星と、それぞれが描く軌跡。少しでも初期位置が違うと、その後は完全に別の運命になります。',
  article='''    <div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：2つの天体の運動は数式できれいに解けますが（二体問題）、<b>3つになった瞬間、一般には解の公式が存在しない</b>ことが証明されています。わずかな初期条件の差が時間とともに爆発的に拡大する「カオス」のため、長期の未来は原理的に計算しきれません。</div>
    <h2>三体問題とは</h2>
    <p>三体問題とは、互いに重力をおよぼし合う3つの天体が、この先どう動くかを求める問題です。太陽・地球・月のような身近な組み合わせでもあります。ニュートン以来、多くの数学者が挑みましたが、19世紀末にポアンカレが「一般には解析的な解（きれいな数式の答え）は存在しない」ことを示しました。</p>
    <h2>なぜ未来が計算できないのか（カオス）</h2>
    <p>三体問題は「決まった物理法則」で動くので、本来ランダムではありません。それでも、初期位置をほんの少し変えただけで、数ステップ後にはまったく違う軌道になります。この<strong>初期値鋭敏性（バタフライ効果）</strong>がカオスの正体です。コンピュータで数値計算はできますが、ごく小さな誤差が拡大するため、遠い未来ほど予測の信頼性は落ちます。</p>
    <h2>身のまわりの三体問題</h2>
    <p>SF小説『三体』で広く知られるようになりましたが、現実の天文学でも重要です。人工衛星の軌道設計、連星まわりの惑星の安定性、ラグランジュ点（重力が釣り合う点）の計算など、応用は多岐にわたります。</p>
    <h2>よくある質問</h2>'''+faq([
      ('三体問題は解けたのですか？','一般解（どんな初期条件にも効く数式の答え）は存在しないと証明済みです。特殊な初期条件での周期解（8の字解など）や、数値計算による近似は可能です。'),
      ('ランダムに動かしているの？','いいえ。万有引力の法則どおりに計算しています。それでも予測が難しいのがカオスの面白さです。'),
      ('星が画面外へ飛んでいくのは？','三体ではしばしば1つが弾き飛ばされます。実際の三体系でも起こる現象で、その時は新しい配置で再スタートします。')])
    +refs([
      'Poincaré, H. 「天体力学の新しい方法」（三体問題とカオスの先駆的研究）',
      'Newton, I. 『プリンキピア』万有引力の法則',
      '国立天文台「ラグランジュ点」解説']),
  share='3つの星が引き合うだけで、軌道は予測不能のカオスに🌌 300年解けてない三体問題、見てると止まらない。',
  js='''  const c=$('cv'),x=c.getContext('2d'),W=c.width,H=c.height;
  const COL=['#5dd6ff','#ff7a9c','#ffd166'];
  let B=[];
  function reset(){const cx=W/2,cy=H/2,R=90;B=[];
    for(let i=0;i<3;i++){const a=i*2.094+Math.random()*0.4;
      B.push({x:cx+Math.cos(a)*R*(0.8+Math.random()*0.4),y:cy+Math.sin(a)*R*(0.8+Math.random()*0.4),
        vx:-Math.sin(a)*0.5+(Math.random()-0.5)*0.3,vy:Math.cos(a)*0.5+(Math.random()-0.5)*0.3,
        m:9+Math.random()*4,tr:[],col:COL[i]});}
    x.fillStyle='#05060f';x.fillRect(0,0,W,H);}
  function offscreen(p){return p.x<-200||p.x>W+200||p.y<-200||p.y>H+200;}
  function stepOne(dt){const G=0.55,soft=140;
    for(const p of B){let ax=0,ay=0;for(const q of B){if(q===p)continue;const dx=q.x-p.x,dy=q.y-p.y,d2=dx*dx+dy*dy+soft,d=Math.sqrt(d2);const f=G*q.m/d2;ax+=f*dx/d;ay+=f*dy/d;}p.ax=ax;p.ay=ay;}
    for(const p of B){p.vx+=p.ax*dt;p.vy+=p.ay*dt;p.x+=p.vx*dt;p.y+=p.vy*dt;p.tr.push([p.x,p.y]);if(p.tr.length>180)p.tr.shift();}}
  function draw(){x.fillStyle='rgba(5,6,15,0.16)';x.fillRect(0,0,W,H);
    for(const p of B){x.strokeStyle=p.col;x.globalAlpha=0.55;x.lineWidth=1.4;x.beginPath();p.tr.forEach((t,i)=>i?x.lineTo(t[0],t[1]):x.moveTo(t[0],t[1]));x.stroke();x.globalAlpha=1;
      x.shadowColor=p.col;x.shadowBlur=16;x.fillStyle=p.col;x.beginPath();x.arc(p.x,p.y,p.m*0.5,0,7);x.fill();x.shadowBlur=0;}}
  function loop(){const sp=+$('spd').value;$('spdL').textContent=sp;for(let k=0;k<sp;k++)stepOne(0.6);
    if(B.some(offscreen))reset();draw();requestAnimationFrame(loop);}
  $('reset').addEventListener('click',reset);
  $('clr').addEventListener('click',()=>{B.forEach(p=>p.tr=[]);x.fillStyle='#05060f';x.fillRect(0,0,W,H);});
  $('spd').addEventListener('input',()=>$('spdL').textContent=$('spd').value);
  reset();loop();'''))

# ============================================================
# 3. ドップラー効果シミュレーター（ドップラー効果 7400/0）
# ============================================================
SIMS.append(dict(id='doppler', emoji='🚑', cat=WONDER, slug='wonder', score=68,
  short='ドップラー効果シミュレーター', carddesc='救急車が近づくと高い音、過ぎると低い音。波の圧縮を可視化。',
  title='ドップラー効果シミュレーター｜救急車の音が変わる理由を可視化｜シミュラボ',
  desc='動く音源から出る波が、進む前方では詰まって（高い音）、後方では伸びる（低い音）様子を可視化する無料シミュレーター。救急車のサイレンが通り過ぎると音が下がるドップラー効果を、波面の動きで直感的に理解できます。',
  ogtitle='ドップラー効果シミュレーター｜音が変わる理由を可視化', ogdesc='動く音源の前は音が詰まり後ろは伸びる。ドップラー効果を波で可視化。',
  h1='ドップラー効果シミュレーター',
  lead='救急車が近づくときは高く、通り過ぎると低く聞こえる。あの「ドップラー効果」を、音源から広がる波の動きで可視化します。速さを上げると、前方の波がぎゅっと詰まっていく様子が見えます。',
  canvas=canvas(520,300,540,'background:#0b1530;'),
  controls=slider('vel','音源の速さ（音速＝100%）','0','130','55')+row(btn('toggle','⏸ 一時停止')),
  legend='○＝音源　△＝観測者。進行方向（前）は波が詰まって高い音、後ろは伸びて低い音になります。',
  article='''    <div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：音源が動くと、進む<b>前方では波が詰まって波長が短く＝高い音</b>に、<b>後方では波が伸びて波長が長く＝低い音</b>になります。これがドップラー効果。音源が観測者を通り過ぎる瞬間に、音の高さがストンと下がって聞こえます。</div>
    <h2>ドップラー効果とは</h2>
    <p>ドップラー効果（ドップラーこうか）とは、音源や観測者が動くことで、聞こえる音の高さ（振動数）が変化する現象です。1842年に物理学者クリスティアン・ドップラーが提唱しました。救急車・パトカーのサイレン、通過する電車の音などで日常的に体験できます。</p>
    <h2>なぜ音の高さが変わるのか</h2>
    <p>音は1秒間に決まった回数の波を出しています。音源が前に進むと、次の波を出すときには少し前に移動しているため、前方では波と波の間隔（波長）が縮みます。波長が短い＝1秒あたりに届く波の数（振動数）が増える＝高い音。逆に後方では波長が伸び、低い音になります。光でも同じことが起き、遠ざかる銀河の光が赤くずれる「赤方偏移」もドップラー効果の一種です。</p>
    <div class="note"><strong>音速を超えると</strong>：音源の速さを音速（100%）以上にすると、波がV字に重なった「衝撃波（ソニックブーム）」の形になります。超音速ジェットがドンと衝撃音を出すのはこのためです。</div>
    <h2>よくある質問</h2>'''+faq([
      ('救急車の音が「下がる」のはいつ？','救急車が自分の前を通り過ぎる瞬間です。近づく間は高め、遠ざかると低めで一定になります。'),
      ('光でもドップラー効果は起きますか？','起きます。近づく光源は青く、遠ざかる光源は赤くずれます（青方偏移・赤方偏移）。'),
      ('音は鳴りますか？','本シミュレーターは波の動きを目で見る可視化です。音は鳴りません。')])
    +refs([
      'Doppler, C. (1842) 二重星の色についての論文（ドップラー効果の原典）',
      '日本物理学会／高校物理「ドップラー効果」',
      'NASA「Doppler effect and redshift」解説']),
  share='救急車が近づくと高い音、過ぎると低い音…ドップラー効果を波で見ると一発で分かる🚑',
  js='''  const c=$('cv'),x=c.getContext('2d'),W=c.width,H=c.height,oy=H/2;
  const cWave=1.1; let sx=60,t=0,waves=[],run=true,emitT=0;
  function reset(){sx=60;waves=[];}
  function step(){const v=(+$('vel').value)/100*cWave;$('velL').textContent=$('vel').value+'%';
    sx+=v;if(sx>W-40){sx=60;waves=[];}
    emitT++;if(emitT>=12){emitT=0;waves.push({x:sx,y:oy,r:0});}
    for(const w of waves)w.r+=cWave*0.9*4;
    waves=waves.filter(w=>w.x-w.r<W+50&&w.r<900);}
  function draw(){x.fillStyle='#0b1530';x.fillRect(0,0,W,H);
    for(const w of waves){const hue=w.x<sx?'rgba(120,180,255,':'rgba(255,140,150,';
      x.strokeStyle=hue+Math.max(0,0.7-w.r/600).toFixed(2)+')';x.lineWidth=1.6;x.beginPath();x.arc(w.x,w.y,w.r,0,7);x.stroke();}
    x.fillStyle='#ffd166';x.shadowColor='#ffd166';x.shadowBlur=14;x.beginPath();x.arc(sx,oy,9,0,7);x.fill();x.shadowBlur=0;
    x.fillStyle='#9fe8ff';x.beginPath();x.moveTo(W-30,oy-12);x.lineTo(W-14,oy);x.lineTo(W-30,oy+12);x.closePath();x.fill();
    x.fillStyle='rgba(255,255,255,.85)';x.font='12px sans-serif';x.textAlign='center';
    x.fillText('← 後ろ：低い音',110,28);x.fillText('前：高い音 →',W-110,28);}
  function loop(){if(run)step();draw();requestAnimationFrame(loop);}
  $('toggle').addEventListener('click',()=>{run=!run;$('toggle').textContent=run?'⏸ 一時停止':'▶ 再生';});
  $('vel').addEventListener('input',()=>$('velL').textContent=$('vel').value+'%');
  reset();loop();'''))

# ============================================================
# 4. ニュートンのゆりかご（ニュートンのゆりかご 2100/0）
# ============================================================
SIMS.append(dict(id='newtons-cradle', emoji='🟤', cat=WONDER, slug='wonder', score=67,
  short='ニュートンのゆりかご', carddesc='端の玉を離すと反対側だけが跳ねる。運動量保存を体感。',
  title='ニュートンのゆりかごシミュレーター｜運動量保存を体感する無料ツール｜シミュラボ',
  desc='端の玉を持ち上げて離すと、反対側の玉だけが同じ数だけ跳ね上がる「ニュートンのゆりかご」をブラウザで再現する無料シミュレーター。なぜ真ん中の玉は動かないのか、運動量保存とエネルギー保存の仕組みも解説します。',
  ogtitle='ニュートンのゆりかご｜運動量保存を体感', ogdesc='端の玉を離すと反対側だけが跳ねる、運動量保存のシミュレーター。',
  h1='ニュートンのゆりかごシミュレーター',
  lead='端の玉を持ち上げて離すと、反対側の玉だけが同じ数だけ跳ねる――あの不思議な置物「ニュートンのゆりかご」。持ち上げる数を変えて、運動量とエネルギーが玉から玉へ伝わる様子を体感してください。',
  canvas=canvas(480,340,520,'background:#0e1626;'),
  controls=slider('lift','持ち上げる玉の数','1','4','1')+row(btn('go','▶ 離す',True)),
  legend='左端から指定した数の玉を持ち上げて離します。反対側から同じ数の玉が跳ね上がります。',
  article='''    <div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：1個ぶつけたら1個、2個なら2個だけが反対側で跳ねます。これは<b>運動量保存則</b>と<b>運動エネルギー保存則</b>の<b>両方</b>を同時に満たす答えが「同じ個数・同じ速さで跳ねる」だけだから。真ん中の玉は衝撃を一瞬で伝えるだけで、ほとんど動きません。</div>
    <h2>ニュートンのゆりかごとは</h2>
    <p>ニュートンのゆりかご（Newton's cradle）は、同じ重さの金属球を糸で吊るして一列に並べた装置です。端の球を引いて離すと、反対端の球だけが同じ勢いで跳ね上がります。物理学者アイザック・ニュートンにちなんで名付けられ、運動量とエネルギーの保存をわかりやすく示す教材として有名です。</p>
    <h2>なぜ反対側だけが同じ数跳ねるのか</h2>
    <p>玉どうしの衝突では、ほぼエネルギーが失われない「弾性衝突」が起こります。このとき成り立つのが次の2つです。</p>
    <div class="note"><strong>2つの保存則</strong><br>運動量保存：質量×速度の合計は衝突の前後で変わらない<br>エネルギー保存：（½×質量×速度²）の合計も変わらない</div>
    <p>この2つを同時に満たす組み合わせは、「ぶつけた数と同じ数の玉が、同じ速さで反対側から飛び出す」場合だけです。だから1個なら1個、2個なら2個。真ん中の玉は、力を瞬間的に隣へ伝えるパイプ役で、自分はほとんど動きません。</p>
    <h2>よくある質問</h2>'''+faq([
      ('2個ぶつけたら、なぜ1個が倍の速さで飛ばないの？','その場合は運動量は保存できてもエネルギーが保存できません。2つの保存則を両立できるのは「同じ数・同じ速さ」だけです。'),
      ('いつか止まるのはなぜ？','空気抵抗や、玉のわずかな変形・音による微小なエネルギー損失があるためです。理想状態なら止まりません。'),
      ('真ん中の玉は本当に動いていないの？','厳密にはごくわずかに動きますが、衝撃を伝えるだけでほぼ静止して見えます。')])
    +refs([
      'Newton, I. 運動の三法則（運動量保存の基礎）',
      'Hutzler, S. et al. "Rocking Newton’s cradle" (American Journal of Physics, 2004)',
      '高校物理「弾性衝突と運動量保存」']),
  share='端の玉を離すと、反対側だけが同じ数跳ねる。ニュートンのゆりかご、運動量保存の傑作🟤',
  js='''  const c=$('cv'),x=c.getContext('2d'),W=c.width,H=c.height;
  const N=5,R=22,pivY=46,L=210,gapX=R*2+2,startX=W/2-gapX*2;
  const G=0.0006,A0=0.9;
  let ang=new Array(N).fill(0),vel=new Array(N).fill(0),swing=null;
  function px(i){return startX+i*gapX;}
  function release(){const k=Math.min(4,Math.max(1,+$('lift').value));$('liftL').textContent=k;
    swing={side:'L',k:k,a:-A0,w:0};ang.fill(0);}
  function physics(){if(!swing)return;
    swing.w+=-G*1000*Math.sin(swing.a);swing.a+=swing.w;
    const k=swing.k;
    if(swing.side==='L'&&swing.a>=0){swing.a=0;swing.side='R';}
    else if(swing.side==='R'&&swing.a<=0){swing.a=0;swing.side='L';}
    // amplitude grows on outer side only
    if(swing.side==='L'){for(let i=0;i<N;i++)ang[i]=i<k?swing.a:0;}
    else{for(let i=0;i<N;i++)ang[i]=i>=N-k?swing.a:0;}}
  function draw(){x.fillStyle='#0e1626';x.fillRect(0,0,W,H);
    x.strokeStyle='#33405c';x.lineWidth=3;x.beginPath();x.moveTo(startX-R,pivY);x.lineTo(px(N-1)+R,pivY);x.stroke();
    for(let i=0;i<N;i++){const a=ang[i];const bx=px(i)+Math.sin(a)*L,by=pivY+Math.cos(a)*L;
      x.strokeStyle='#7b8aa8';x.lineWidth=1.5;x.beginPath();x.moveTo(px(i),pivY);x.lineTo(bx,by);x.stroke();
      const g=x.createRadialGradient(bx-7,by-7,2,bx,by,R);g.addColorStop(0,'#dfe8ff');g.addColorStop(1,'#8aa0d8');
      x.fillStyle=g;x.beginPath();x.arc(bx,by,R,0,7);x.fill();x.strokeStyle='#4a5a82';x.lineWidth=1.5;x.stroke();}}
  function loop(){physics();draw();requestAnimationFrame(loop);}
  $('go').addEventListener('click',release);
  $('lift').addEventListener('input',()=>$('liftL').textContent=$('lift').value);
  draw();loop();'''))

# ============================================================
# 5. ソートアルゴリズム可視化（バブルソート 1100/0, ソートアルゴリズム 600/1）
# ============================================================
SIMS.append(dict(id='sort-visualizer', emoji='📊', cat=PLAY, slug='play', score=66,
  short='ソートアルゴリズム可視化', carddesc='バブル・クイック等の並べ替えを棒グラフで動かして比較。',
  title='ソートアルゴリズム可視化｜バブルソートなど5種の動きを比較｜シミュラボ',
  desc='バブルソート・選択ソート・挿入ソート・クイックソート・マージソートが、棒グラフを並べ替えていく様子をアニメーションで比較できる無料シミュレーター。どのアルゴリズムが速いのか、計算量とあわせて直感的に分かります。',
  ogtitle='ソートアルゴリズム可視化｜5種の動きを比較', ogdesc='バブル・選択・挿入・クイック・マージソートを棒グラフで可視化・比較。',
  h1='ソートアルゴリズム可視化',
  lead='バラバラの棒を小さい順に並べ替える――その手順がアルゴリズムによってこんなに違います。バブルソートから高速なクイックソートまで、並べ替えの動きを目で見て比べてください。',
  canvas=canvas(520,300,540,'background:#0e1626;'),
  controls=select('algo','アルゴリズム',[('bubble','バブルソート'),('selection','選択ソート'),('insertion','挿入ソート'),('quick','クイックソート'),('merge','マージソート')])
    +slider('cnt','棒の本数','12','80','40')+slider('spd','速さ','1','60','18')
    +row(btn('go','▶ スタート',True),btn('shuf','シャッフル')),
  legend='黄＝比較中　赤＝入れ替え　緑＝確定。アルゴリズムを変えて並べ替えの効率を見比べてください。',
  article='''    <div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：バブル・選択・挿入ソートは仕組みが単純ですが遅く（計算量 O(n²)）、クイックソート・マージソートは平均 <b>O(n log n)</b> で大きなデータに強い。本数を増やすほど、速いアルゴリズムとの差がはっきり見えます。</div>
    <h2>ソートアルゴリズムとは</h2>
    <p>ソートアルゴリズムとは、データを一定の順序（小さい順・大きい順など）に並べ替える手順のことです。プログラミングの基礎であり、検索の高速化やデータ処理の前段としてあらゆる場面で使われます。同じ「並べ替え」でも、手順しだいで速さが大きく変わります。</p>
    <h2>5つのアルゴリズムの違い</h2>
    <table class="seo-table">
      <tr><th>アルゴリズム</th><th>平均計算量</th><th>特徴</th></tr>
      <tr><td>バブルソート</td><td>O(n²)</td><td>隣どうしを比べて交換。仕組みが最も簡単だが遅い。</td></tr>
      <tr><td>選択ソート</td><td>O(n²)</td><td>最小値を選んで前に置く。交換回数は少なめ。</td></tr>
      <tr><td>挿入ソート</td><td>O(n²)</td><td>ほぼ整列済みのデータには速い。トランプの整列に近い。</td></tr>
      <tr><td>クイックソート</td><td>O(n log n)</td><td>基準値で分割。実用上もっとも速い部類。</td></tr>
      <tr><td>マージソート</td><td>O(n log n)</td><td>半分に分けて併合。安定で計算量が安定。</td></tr>
    </table>
    <p>「O(n²)」は、データが10倍になると手間が約100倍に増えるという意味。「O(n log n)」なら増え方がゆるやかで、大量データほど差が開きます。</p>
    <h2>よくある質問</h2>'''+faq([
      ('一番速いソートはどれ？','一般にはクイックソートが高速ですが、データの状態によります。ほぼ整列済みなら挿入ソートが有利な場面もあります。'),
      ('バブルソートはなぜ習うの？','仕組みが直感的で、ソートの考え方を学ぶのに最適だからです。実務では遅いためあまり使われません。'),
      ('計算はどこで行われますか？','すべてあなたのブラウザ内で完結します。データは送信されません。')])
    +refs([
      'Knuth, D. 『The Art of Computer Programming Vol.3 Sorting and Searching』',
      'Cormen ほか『アルゴリズムイントロダクション』ソート章',
      '情報処理推進機構（IPA）基本情報技術者 アルゴリズム']),
  share='バブルソートとクイックソート、並べ替えの速さがこんなに違う📊 見比べると面白い。',
  js='''  const c=$('cv'),x=c.getContext('2d'),W=c.width,H=c.height;
  let a=[],ops=[],pi=0,playing=false,cur={c:[],s:[],done:-1};
  function shuffle(){const n=+$('cnt').value;$('cntL').textContent=n;a=[];for(let i=0;i<n;i++)a.push(0.08+Math.random()*0.9);ops=[];pi=0;playing=false;cur={c:[],s:[],done:-1};draw();}
  function rec(t,i,j){ops.push([t,i,j]);}
  function build(){const arr=a.slice(),n=arr.length;ops=[];const algo=$('algo').value;
    const sw=(i,j)=>{rec('s',i,j);const t=arr[i];arr[i]=arr[j];arr[j]=t;};
    if(algo==='bubble'){for(let i=0;i<n;i++){for(let j=0;j<n-1-i;j++){rec('c',j,j+1);if(arr[j]>arr[j+1])sw(j,j+1);}rec('d',n-1-i,-1);}}
    else if(algo==='selection'){for(let i=0;i<n;i++){let m=i;for(let j=i+1;j<n;j++){rec('c',m,j);if(arr[j]<arr[m])m=j;}if(m!==i)sw(i,m);rec('d',i,-1);}}
    else if(algo==='insertion'){rec('d',0,-1);for(let i=1;i<n;i++){let j=i;while(j>0){rec('c',j-1,j);if(arr[j-1]>arr[j]){sw(j-1,j);j--;}else break;}rec('d',i,-1);}}
    else if(algo==='quick'){const qs=(lo,hi)=>{if(lo>=hi){if(lo===hi)rec('d',lo,-1);return;}const p=arr[hi];let i=lo;for(let j=lo;j<hi;j++){rec('c',j,hi);if(arr[j]<p){sw(i,j);i++;}}sw(i,hi);rec('d',i,-1);qs(lo,i-1);qs(i+1,hi);};qs(0,n-1);}
    else if(algo==='merge'){const tmp=arr.slice();const ms=(lo,hi)=>{if(hi-lo<1)return;const mid=(lo+hi)>>1;ms(lo,mid);ms(mid+1,hi);let i=lo,j=mid+1,k=lo;for(let t=lo;t<=hi;t++)tmp[t]=arr[t];while(i<=mid&&j<=hi){rec('c',i,j);if(tmp[i]<=tmp[j])arr[k++]=tmp[i++];else arr[k++]=tmp[j++];rec('w',-1,-1);}while(i<=mid){arr[k++]=tmp[i++];rec('w',-1,-1);}while(j<=hi){arr[k++]=tmp[j++];rec('w',-1,-1);}for(let t=lo;t<=hi;t++)rec('hi',t,hi);};ms(0,n-1);for(let i=0;i<n;i++)rec('d',i,-1);}
    pi=0;}
  function apply(op){const [t,i,j]=op;cur.c=[];
    if(t==='s'){const tmp=a[i];a[i]=a[j];a[j]=tmp;cur.s=[i,j];}
    else if(t==='c'){cur.c=[i,j];cur.s=[];}
    else if(t==='d'){cur.done=Math.max(cur.done,i);cur.s=[];}
    else if(t==='hi'){cur.c=[i];}}
  function draw(){x.fillStyle='#0e1626';x.fillRect(0,0,W,H);const n=a.length,bw=W/n;
    for(let i=0;i<n;i++){const h=a[i]*(H-10);let col='#5b6b8c';
      if(i<=cur.done)col='#34d399';if(cur.c.includes(i))col='#fbbf24';if(cur.s.includes(i))col='#f43f5e';
      x.fillStyle=col;x.fillRect(i*bw+0.5,H-h,bw-1,h);}}
  function loop(){if(playing){const sp=+$('spd').value;$('spdL').textContent=sp;
    for(let k=0;k<sp&&pi<ops.length;k++)apply(ops[pi++]);
    if(pi>=ops.length){playing=false;cur.done=a.length-1;cur.c=[];cur.s=[];}}
    draw();requestAnimationFrame(loop);}
  $('go').addEventListener('click',()=>{if(pi>=ops.length||ops.length===0){build();}playing=true;});
  $('shuf').addEventListener('click',shuffle);
  $('algo').addEventListener('change',()=>{ops=[];pi=0;playing=false;cur={c:[],s:[],done:-1};draw();});
  $('cnt').addEventListener('input',shuffle);
  $('spd').addEventListener('input',()=>$('spdL').textContent=$('spd').value);
  shuffle();loop();'''))

# ============================================================
# 6. ボロノイ図ジェネレーター（ボロノイ図 1000/0）
# ============================================================
SIMS.append(dict(id='voronoi', emoji='🔷', cat=PLAY, slug='play', score=63,
  short='ボロノイ図ジェネレーター', carddesc='母点に一番近い領域で平面を分割。動かすとセルが踊る。',
  title='ボロノイ図ジェネレーター｜母点で平面を分割する無料シミュレーター｜シミュラボ',
  desc='いくつかの点（母点）に対して「どの点に一番近いか」で平面を塗り分ける、ボロノイ図をリアルタイムで生成する無料シミュレーター。点をクリックで追加したり、動かしてセルが変化する様子を体感できます。',
  ogtitle='ボロノイ図ジェネレーター｜母点で平面を分割', ogdesc='一番近い母点で平面を塗り分けるボロノイ図をリアルタイム生成。',
  h1='ボロノイ図ジェネレーター',
  lead='たくさんの点に対して「どの点が一番近いか」で色を塗ると、平面が多角形のタイルに分かれます。これがボロノイ図。点をクリックで足したり、動く点が作るセルの変化を眺めてください。',
  canvas=canvas(460,360,500,'cursor:crosshair;'),
  controls=slider('np','母点の数','3','24','10')+row(btn('reset','リセット'),btn('toggle','⏸ 動きを止める')),
  legend='同じ色の領域＝その色の点が最も近い場所。キャンバスをクリックで母点を追加できます。',
  article='''    <div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：ボロノイ図は「平面上の各場所を、最も近い母点ごとに縄張り分けした図」です。隣り合う母点の<b>垂直二等分線</b>が境界になり、領域は必ず凸多角形になります。最寄り店の商圏、携帯基地局のエリア分けなど応用は多彩です。</div>
    <h2>ボロノイ図とは</h2>
    <p>ボロノイ図（Voronoi diagram）は、平面にいくつかの母点（種となる点）を置いたとき、それぞれの場所を「一番近い母点」ごとに塗り分けてできる図形です。数学者ゲオルギー・ボロノイにちなみます。生まれる境界線は、隣り合う2つの母点を結ぶ線の垂直二等分線でできています。</p>
    <h2>どこで使われている？</h2>
    <ul>
      <li><strong>商圏・立地分析</strong>：最寄りの店舗・施設の担当エリアを求める</li>
      <li><strong>通信</strong>：携帯電話の基地局がカバーするエリア分け</li>
      <li><strong>地理・気象</strong>：観測点ごとの代表エリア（ティーセン多角形）</li>
      <li><strong>CG・ゲーム</strong>：自然な地形や模様、ひび割れの生成</li>
    </ul>
    <p>身近な例では「キリンの模様」「乾いた泥のひび割れ」もボロノイ図に近い構造をしています。</p>
    <h2>よくある質問</h2>'''+faq([
      ('ドロネー三角形分割との関係は？','ボロノイ図と表裏一体の関係にあり、母点どうしを結んでできる三角形分割がドロネー図です。'),
      ('境界線はどうやって決まるの？','隣り合う母点を結んだ線分の垂直二等分線が境界になります。だから領域は凸多角形になります。'),
      ('点はいくつまで増やせますか？','スライダーで増やせるほか、クリックでも追加できます。多いほど細かいタイルになります。')])
    +refs([
      'Voronoi, G. (1908) 二次形式に関する研究（ボロノイ図の起源）',
      'Aurenhammer, F. "Voronoi Diagrams" (ACM Computing Surveys, 1991)',
      'Thiessen, A. ティーセン多角形（気象観測への応用）']),
  share='一番近い点で平面を塗り分けるとタイルになる…ボロノイ図、動かすとセルが踊って気持ちいい🔷',
  js='''  const c=$('cv'),x=c.getContext('2d'),W=c.width,H=c.height,S=4;
  const gw=Math.ceil(W/S),gh=Math.ceil(H/S),img=x.createImageData(gw,gh);
  let pts=[],run=true;
  function hsl(h){h=((h%360)+360)%360;const s=0.55,l=0.56;const k=n=>(n+h/30)%12;const f=n=>l-s*Math.min(l,1-l)*Math.max(-1,Math.min(k(n)-3,9-k(n),1));return [f(0)*255,f(8)*255,f(4)*255];}
  function reset(){const n=+$('np').value;$('npL').textContent=n;pts=[];for(let i=0;i<n;i++)pts.push({x:20+Math.random()*(W-40),y:20+Math.random()*(H-40),vx:(Math.random()-.5)*1.4,vy:(Math.random()-.5)*1.4,col:hsl(i*360/n)});}
  function step(){if(!run)return;for(const p of pts){p.x+=p.vx;p.y+=p.vy;if(p.x<8||p.x>W-8)p.vx*=-1;if(p.y<8||p.y>H-8)p.vy*=-1;}}
  function draw(){const d=img.data;
    for(let gy=0;gy<gh;gy++)for(let gx=0;gx<gw;gx++){const px=gx*S,py=gy*S;let bd=1e9,bi=0;
      for(let i=0;i<pts.length;i++){const dx=px-pts[i].x,dy=py-pts[i].y,dd=dx*dx+dy*dy;if(dd<bd){bd=dd;bi=i;}}
      const col=pts[bi].col,id=(gy*gw+gx)*4,edge=bd<60?0.6:1;d[id]=col[0]*edge;d[id+1]=col[1]*edge;d[id+2]=col[2]*edge;d[id+3]=255;}
    x.putImageData(img,0,0);x.imageSmoothingEnabled=false;x.drawImage(c,0,0,gw,gh,0,0,W,H);
    for(const p of pts){x.fillStyle='#fff';x.beginPath();x.arc(p.x,p.y,3,0,7);x.fill();x.strokeStyle='#0e1626';x.lineWidth=1;x.stroke();}}
  function loop(){step();draw();requestAnimationFrame(loop);}
  $('reset').addEventListener('click',reset);
  $('np').addEventListener('input',reset);
  $('toggle').addEventListener('click',()=>{run=!run;$('toggle').textContent=run?'⏸ 動きを止める':'▶ 動かす';});
  c.addEventListener('click',e=>{const r=c.getBoundingClientRect();pts.push({x:(e.clientX-r.left)/r.width*W,y:(e.clientY-r.top)/r.height*H,vx:(Math.random()-.5)*1.4,vy:(Math.random()-.5)*1.4,col:hsl(pts.length*47)});});
  reset();loop();'''))

# ============================================================
# 7. フローフィールド（パーリンノイズ 500/0）
# ============================================================
SIMS.append(dict(id='flow-field', emoji='🌬️', cat=PLAY, slug='play', score=61,
  short='パーリンノイズ・フローフィールド', carddesc='ノイズが作る見えない流れに沿って粒子が線を描く生成アート。',
  title='パーリンノイズ フローフィールド｜流れる生成アートの無料シミュレーター｜シミュラボ',
  desc='パーリンノイズ（なめらかな乱数）が作る見えない「流れの場」に沿って、無数の粒子が線を描いていく生成アートのシミュレーター。ノイズの細かさを変えると、模様がガラリと変わります。',
  ogtitle='パーリンノイズ フローフィールド｜流れる生成アート', ogdesc='なめらかな乱数が作る流れに沿って粒子が線を描く生成アート。',
  h1='パーリンノイズ・フローフィールド',
  lead='パーリンノイズという「なめらかな乱数」を使うと、目に見えない風のような流れが生まれます。その流れに沿って無数の粒子を走らせると、川や煙のような美しい模様に。眺めるだけのデジタルアートです。',
  canvas=canvas(520,360,540,'background:#0a0a12;'),
  controls=slider('scl','流れの細かさ','3','30','10')+row(btn('palette','🎨 配色を変える'),btn('reset','リセット')),
  legend='見えないベクトルの流れに沿って粒子が線を描きます。細かさを変えると模様が変化します。',
  article='''    <div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：パーリンノイズは、点と点が急に飛ばずに<b>なめらかに変化する乱数</b>です。各地点の値を「矢印の向き」に変換すると、自然な流れの地図（フローフィールド）ができ、そこに粒子を流すと有機的な模様＝<b>ジェネラティブアート</b>が生まれます。</div>
    <h2>パーリンノイズとは</h2>
    <p>パーリンノイズ（Perlin noise）は、1983年に映画『トロン』のために、ケン・パーリンが考案したなめらかな乱数の作り方です。ふつうの乱数は隣り合う値がバラバラですが、パーリンノイズは隣どうしがゆるやかにつながるため、雲・炎・地形・水面など「自然なゆらぎ」の表現に欠かせません。CG・ゲーム・VFXで広く使われ、パーリンはこの功績でアカデミー科学技術賞を受賞しました。</p>
    <h2>フローフィールドの仕組み</h2>
    <p>画面の各場所でノイズの値を求め、それを角度に変換すると「矢印が並んだ流れの地図」ができます。粒子はその場所の矢印の向きへ少しずつ進み、軌跡を薄く重ねていきます。流れの細かさ（ノイズの拡大率）を変えると、大きくうねる模様にも、細かく入り組んだ模様にも変化します。</p>
    <h2>よくある質問</h2>'''+faq([
      ('ジェネラティブアートとは？','人が直接1本ずつ描くのではなく、ルールやアルゴリズムに沿ってコンピュータが模様を生成する作品のことです。'),
      ('毎回ちがう模様になりますか？','はい。リセットや配色変更で異なる流れと色になります。気に入った絵はスクショで保存してください。'),
      ('重くないですか？','負荷を抑えた軽量版です。古い端末では粒子数を控えめにしています。')])
    +refs([
      'Perlin, K. (1985) "An Image Synthesizer" (SIGGRAPH) パーリンノイズの原典',
      'Perlin, K. (2002) "Improving Noise" 改良版ノイズ',
      'The Nature of Code（Daniel Shiffman）フローフィールドの解説']),
  share='なめらかな乱数「パーリンノイズ」で粒子を流すと、川や煙みたいな模様が生まれる🌬️ 生成アート。',
  js='''  const c=$('cv'),x=c.getContext('2d'),W=c.width,H=c.height;
  const G=14;let grid=[],parts=[],z=0,pal=0,frame=0;
  const PALS=[[190,255],[20,60],[270,330],[90,160]];
  function noiseGrid(){grid=[];for(let i=0;i<=G;i++){grid[i]=[];for(let j=0;j<=G;j++)grid[i][j]=Math.random()*6.283;}}
  function smooth(gx,gy){const i=Math.floor(gx),j=Math.floor(gy),fx=gx-i,fy=gy-j;
    const a=grid[i%G][j%G],b=grid[(i+1)%G][j%G],cc=grid[i%G][(j+1)%G],d=grid[(i+1)%G][(j+1)%G];
    const u=fx*fx*(3-2*fx),v=fy*fy*(3-2*fy);
    const top=a+(b-a)*u,bot=cc+(d-cc)*u;return top+(bot-top)*v;}
  function reset(){noiseGrid();parts=[];for(let i=0;i<700;i++)parts.push({x:Math.random()*W,y:Math.random()*H});x.fillStyle='#0a0a12';x.fillRect(0,0,W,H);}
  function step(){const scl=(+$('scl').value)/200;$('sclL').textContent=$('scl').value;z+=0.0007;
    const [h0,h1]=PALS[pal];
    for(const p of parts){const gx=(p.x*scl)%G,gy=(p.y*scl)%G;const ang=smooth((gx+G)%G,(gy+G)%G)*3+z*40;
      const nx=p.x+Math.cos(ang)*1.4,ny=p.y+Math.sin(ang)*1.4;
      const hue=h0+(h1-h0)*(p.y/H);x.strokeStyle='hsla('+hue+',80%,62%,0.10)';x.lineWidth=1;
      x.beginPath();x.moveTo(p.x,p.y);x.lineTo(nx,ny);x.stroke();
      p.x=nx;p.y=ny;if(p.x<0||p.x>W||p.y<0||p.y>H){p.x=Math.random()*W;p.y=Math.random()*H;}}}
  function loop(){frame++;if(frame%600===0){x.fillStyle='rgba(10,10,18,0.10)';x.fillRect(0,0,W,H);}step();requestAnimationFrame(loop);}
  $('palette').addEventListener('click',()=>{pal=(pal+1)%PALS.length;});
  $('reset').addEventListener('click',reset);
  $('scl').addEventListener('input',()=>$('sclL').textContent=$('scl').value);
  reset();loop();'''))

# ============================================================
# 8. フラクタル図形ジェネレーター（コッホ曲線 400/0）
# ============================================================
SIMS.append(dict(id='koch', emoji='🔺', cat=PLAY, slug='play', score=60,
  short='コッホ雪片・フラクタル図形', carddesc='コッホ雪片やドラゴン曲線を反復で描く。自己相似の不思議。',
  title='コッホ雪片 フラクタル図形ジェネレーター｜反復で描く無料シミュレーター｜シミュラボ',
  desc='コッホ曲線・コッホ雪片・シェルピンスキー・ドラゴン曲線などのフラクタル図形を、反復回数を変えながらアニメーションで描く無料シミュレーター。拡大しても同じ形が現れる「自己相似」を体感できます。',
  ogtitle='コッホ雪片 フラクタル図形ジェネレーター', ogdesc='コッホ曲線・雪片・ドラゴン曲線を反復で描くフラクタル生成器。',
  h1='コッホ雪片・フラクタル図形ジェネレーター',
  lead='直線を折り曲げる操作を何度もくり返すと、雪の結晶のような複雑な図形「コッホ雪片」が現れます。反復回数を上げると、どこを拡大しても同じ形が出てくる「フラクタル」の不思議が見えてきます。',
  canvas=canvas(460,380,500,'background:#0b1530;'),
  controls=select('shape','図形',[('snow','コッホ雪片'),('koch','コッホ曲線'),('sier','シェルピンスキー'),('dragon','ドラゴン曲線')])
    +slider('iter','反復回数','0','6','3')+row(btn('redraw','▶ 描き直す',True)),
  legend='反復回数を上げるほど細かくなります。一部を拡大すると全体と同じ形が現れます（自己相似）。',
  article='''    <div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：フラクタルとは、<b>一部を拡大すると全体とそっくりな形が現れる「自己相似」</b>な図形のこと。コッホ雪片は、線を折り曲げる単純な操作のくり返しだけで、無限に入り組んだ縁を持つ図形になります。</div>
    <h2>コッホ曲線・コッホ雪片とは</h2>
    <p>コッホ曲線は、1904年に数学者ヘルゲ・フォン・コッホが考えた図形です。1本の線分を3等分し、真ん中の区間を山型（正三角形の2辺）に置きかえます。この操作を各線分にくり返すと、ギザギザがどんどん細かくなります。正三角形の3辺すべてにこれを行ったものが「コッホ雪片」で、雪の結晶のような輪郭になります。</p>
    <div class="note"><strong>不思議な性質</strong><br>コッホ雪片は、<b>面積は有限</b>なのに<b>周の長さは無限</b>に伸びていきます。反復のたびに辺の数が4/3倍に増えるためです。</div>
    <h2>いろいろなフラクタル</h2>
    <ul>
      <li><strong>シェルピンスキー</strong>：三角形から中央の三角形をくり抜き続ける図形</li>
      <li><strong>ドラゴン曲線</strong>：紙を半分に折り続けたときの折り目が作る曲線</li>
    </ul>
    <p>フラクタルは数学の世界だけのものではありません。海岸線・樹木の枝・雲・血管の分かれ方など、自然界のいたるところに自己相似の構造が見られます。</p>
    <h2>よくある質問</h2>'''+faq([
      ('フラクタルの「次元」って何ですか？','直線は1次元、面は2次元ですが、フラクタルはその中間の「1.26次元」のような分数の次元（フラクタル次元）を持ちます。'),
      ('どこまで反復できますか？','画面では6回までにしています。理論上は無限にくり返せ、いくら拡大しても新しいギザギザが現れます。'),
      ('自然界のどこにありますか？','海岸線、シダの葉、樹木、雷の枝分かれ、雲の輪郭などが代表例です。')])
    +refs([
      'von Koch, H. (1904) コッホ曲線の原論文',
      'Mandelbrot, B. 『フラクタル幾何学』（フラクタルの概念を確立）',
      'Mandelbrot, B. (1967) "How Long Is the Coast of Britain?" (Science)']),
  share='線を折り曲げ続けるだけで、雪の結晶みたいなコッホ雪片に🔺 拡大しても同じ形が出るフラクタルの不思議。',
  js='''  const c=$('cv'),x=c.getContext('2d'),W=c.width,H=c.height;
  let pts=[],drawn=0,raf=0;
  function lsys(axiom,rules,it){let s=axiom;for(let k=0;k<it;k++){let n='';for(const ch of s)n+=rules[ch]||ch;s=n;}return s;}
  function turtle(s,ang,start){const st=[];let px=start.x,py=start.y,a=start.a;const pts=[[px,py]];
    for(const ch of s){if(ch==='F'||ch==='A'||ch==='B'){px+=Math.cos(a);py+=Math.sin(a);pts.push([px,py]);}
      else if(ch==='+')a+=ang;else if(ch==='-')a-=ang;}return pts;}
  function build(){const it=+$('iter').value;$('iterL').textContent=it;const sh=$('shape').value;let raw,ang,ax,start;
    if(sh==='koch'){raw=lsys('F',{F:'F+F--F+F'},it);ang=Math.PI/3;start={x:0,y:0,a:0};}
    else if(sh==='snow'){raw=lsys('F--F--F',{F:'F+F--F+F'},it);ang=Math.PI/3;start={x:0,y:0,a:0};}
    else if(sh==='sier'){raw=lsys('A',{A:'B-A-B',B:'A+B+A'},it);ang=Math.PI/3;start={x:0,y:0,a:0};}
    else{raw=lsys('FX',{X:'X+YF+',Y:'-FX-Y'},it);ang=Math.PI/2;start={x:0,y:0,a:0};}
    let p=turtle(raw,ang,start);
    let minx=1e9,miny=1e9,maxx=-1e9,maxy=-1e9;for(const q of p){minx=Math.min(minx,q[0]);maxx=Math.max(maxx,q[0]);miny=Math.min(miny,q[1]);maxy=Math.max(maxy,q[1]);}
    const pw=maxx-minx||1,ph=maxy-miny||1,pad=30,sc=Math.min((W-pad*2)/pw,(H-pad*2)/ph);
    pts=p.map(q=>[(q[0]-minx)*sc+(W-pw*sc)/2,(q[1]-miny)*sc+(H-ph*sc)/2]);drawn=0;}
  function loop(){x.fillStyle='#0b1530';x.fillRect(0,0,W,H);
    drawn=Math.min(pts.length,drawn+Math.max(2,pts.length/60|0));
    x.strokeStyle='#7fe9ff';x.lineWidth=1.4;x.shadowColor='#3aa0ff';x.shadowBlur=6;x.beginPath();
    for(let i=0;i<drawn;i++){const q=pts[i];i?x.lineTo(q[0],q[1]):x.moveTo(q[0],q[1]);}x.stroke();x.shadowBlur=0;
    if(drawn<pts.length)raf=requestAnimationFrame(loop);}
  function start(){cancelAnimationFrame(raf);build();loop();}
  $('redraw').addEventListener('click',start);
  $('shape').addEventListener('change',start);
  $('iter').addEventListener('input',start);
  start();'''))

# ============================================================
# 9. モンテカルロ法で円周率（モンテカルロ法 円周率 250/0）
# ============================================================
SIMS.append(dict(id='montecarlo-pi', emoji='🎯', cat=WONDER, slug='wonder', score=62,
  short='モンテカルロ法で円周率', carddesc='ランダムに点を打つだけで円周率πが浮かび上がる。',
  title='モンテカルロ法で円周率を求めるシミュレーター｜πが点で現れる｜シミュラボ',
  desc='正方形の中にランダムな点を打ち、円の中に入った割合からπ（円周率）を求める「モンテカルロ法」を可視化する無料シミュレーター。点を増やすほど推定値が3.14…に近づく様子をリアルタイムで体感できます。',
  ogtitle='モンテカルロ法で円周率を求める｜πが点で現れる', ogdesc='ランダムに点を打つだけで円周率πが求まるモンテカルロ法を可視化。',
  h1='モンテカルロ法で円周率を求めるシミュレーター',
  lead='正方形にランダムな点をばらまき、円の内側に入った割合を数える――ただそれだけで円周率π＝3.14…が浮かび上がります。点が増えるほど精度が上がる「モンテカルロ法」をその目で確かめてください。',
  canvas=canvas(360,360,400,'background:#0b1530;'),
  controls=readout('out','πの推定値：—')+slider('rate','1秒あたりの点の数','50','3000','600')+row(btn('reset','リセット')),
  legend='青＝円の内側に入った点　赤＝外側。内側の割合×4が円周率πの推定値になります。',
  article='''    <div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：正方形に点をランダムに打つと、円の中に入る確率は「円の面積 ÷ 正方形の面積 ＝ π/4」。だから<b>（円内の点 ÷ 全部の点）× 4</b> がπの推定値になります。点が増えるほど 3.14159… に近づきます。</div>
    <h2>モンテカルロ法とは</h2>
    <p>モンテカルロ法とは、乱数（ランダムな数）を大量に使って、答えを近似的に求める計算手法です。カジノで有名な都市モンテカルロにちなんで名付けられました。複雑で式では解きにくい問題でも、「たくさん試して割合を見る」ことで答えに迫れるのが強みです。</p>
    <h2>なぜ点を打つと円周率が分かるのか</h2>
    <p>1辺の長さが2の正方形（面積4）の中に、半径1の円（面積π）を描きます。正方形の中にランダムに点を打つと、点が円の内側に入る確率は面積の比、つまり π/4 になります。</p>
    <div class="note"><strong>計算式</strong><br>π ≒ （円の内側に入った点の数 ÷ 打った点の総数）× 4</div>
    <p>はじめは値が大きくぶれますが、点を増やすほど安定して 3.14159… に近づきます。これは「大数の法則」――試行回数を増やすほど、実際の割合が理論値に近づくという性質によるものです。</p>
    <h2>よくある質問</h2>'''+faq([
      ('正確なπが出ないのはなぜ？','ランダムなので必ず誤差が残ります。点を10倍に増やすと誤差はおよそ1/3になり、ゆっくり精度が上がります。'),
      ('モンテカルロ法は何の役に立つの？','金融のリスク試算、物理シミュレーション、AIの探索など、式で解けない問題の近似計算に幅広く使われます。'),
      ('点はどこで計算していますか？','すべてブラウザ内で生成しています。データは送信されません。')])
    +refs([
      'Metropolis, N. & Ulam, S. (1949) "The Monte Carlo Method" (JASA)',
      '大数の法則（確率論の基本定理）',
      'Buffonの針（乱数で円周率を求める古典的問題）']),
  share='正方形にランダムに点を打つだけで、円周率π＝3.14…が現れる🎯 モンテカルロ法、不思議すぎる。',
  js='''  const c=$('cv'),x=c.getContext('2d'),W=c.width,H=c.height,R=Math.min(W,H)/2-6,cx=W/2,cy=H/2;
  let inside=0,total=0;
  function bg(){x.fillStyle='#0b1530';x.fillRect(0,0,W,H);
    x.strokeStyle='rgba(255,255,255,.35)';x.lineWidth=1.5;x.strokeRect(cx-R,cy-R,R*2,R*2);
    x.beginPath();x.arc(cx,cy,R,0,7);x.stroke();}
  function reset(){inside=0;total=0;bg();$('out').textContent='πの推定値：—';}
  function step(){const n=Math.max(1,(+$('rate').value)/60|0);$('rateL').textContent=$('rate').value;
    for(let k=0;k<n;k++){const rx=Math.random()*2-1,ry=Math.random()*2-1;const isin=rx*rx+ry*ry<=1;if(isin)inside++;total++;
      const px=cx+rx*R,py=cy+ry*R;x.fillStyle=isin?'#5dd6ff':'#ff7a9c';x.fillRect(px,py,2,2);}
    if(total>0){const pi=4*inside/total;$('out').textContent='πの推定値：'+pi.toFixed(5)+'　（点 '+total.toLocaleString()+'　誤差 '+(Math.abs(pi-Math.PI)).toFixed(5)+'）';}}
  function loop(){step();requestAnimationFrame(loop);}
  $('reset').addEventListener('click',reset);
  $('rate').addEventListener('input',()=>$('rateL').textContent=$('rate').value);
  reset();loop();'''))

# ============================================================
# 10. ダブルスリット実験（ダブルスリット実験 TP5100/2）
# ============================================================
SIMS.append(dict(id='double-slit', emoji='⚛️', cat=WONDER, slug='wonder', score=64,
  short='ダブルスリット実験', carddesc='粒を1個ずつ撃つだけで、なぜか縞模様が浮かぶ量子の謎。',
  title='ダブルスリット実験シミュレーター｜1個ずつでも縞ができる謎｜シミュラボ',
  desc='2つのスリットに向けて粒子を1個ずつ撃つと、1個1個はランダムに当たるのに、積み重なると干渉縞（しま模様）が現れる「ダブルスリット実験（二重スリット実験）」を再現する無料シミュレーター。量子力学の不思議を体感できます。',
  ogtitle='ダブルスリット実験｜1個ずつでも縞ができる謎', ogdesc='粒子を1個ずつ撃つだけで干渉縞が現れる二重スリット実験を再現。',
  h1='ダブルスリット実験シミュレーター',
  lead='2つの細いすき間（スリット）に向けて、粒を1個ずつ撃ち込みます。1個1個はランダムに当たるのに、積み重なると不思議なしま模様＝干渉縞が現れます。「世界一美しい実験」とも呼ばれる量子の謎を体感してください。',
  canvas=canvas(460,400,500,'background:#05060f;'),
  controls=slider('gap','スリットの間隔','20','120','60')
    +select('mode','スリット',[('two','両方ひらく'),('one','片方を閉じる')])
    +row(btn('reset','リセット'),btn('fast','⏩ 一気に当てる')),
  legend='上から粒子を発射、下のスクリーンに当たって積もります。両方ひらくと縞模様が現れます。',
  article='''    <div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：粒子を1個ずつ撃っても、両方のスリットを開けておくと、当たった点が積み重なって<b>縞模様（干渉縞）</b>になります。まるで1個の粒が「両方のすき間を同時に通った波」のように振る舞う――これが量子力学の最大の謎です。片方を閉じると縞は消えます。</div>
    <h2>ダブルスリット実験とは</h2>
    <p>ダブルスリット実験（二重スリット実験）は、2本の細いすき間に向けて光や電子を当て、その先のスクリーンにできる模様を見る実験です。19世紀にトマス・ヤングが光で行い、光が波であることを示しました。20世紀には電子1個ずつでも同じ縞ができることが確かめられ、量子力学を象徴する実験になりました。</p>
    <h2>なぜ1個ずつなのに縞ができるのか</h2>
    <p>粒子を1個だけ撃つと、スクリーンには1点だけ記録されます。どこに当たるかはランダムです。ところが何千個も積み重ねると、当たりやすい場所と当たらない場所が縞状に分かれます。これは、1個の粒子が「両方のスリットを通る波」として広がり、自分自身と干渉して、当たる確率に濃淡ができるためと説明されます。</p>
    <div class="note"><strong>もっと不思議なこと</strong><br>「どちらのスリットを通ったか」を観測しようとすると、とたんに縞模様は消え、ただの2本の帯になります。見るか見ないかで結果が変わる――これが「観測問題」と呼ばれる謎です。</div>
    <h2>よくある質問</h2>'''+faq([
      ('粒子なのに波って、どういうこと？','量子の世界では、電子や光は「粒」と「波」の両方の性質を持ちます（波と粒子の二重性）。状況によってどちらの顔を見せるかが変わります。'),
      ('片方を閉じると縞が消えるのはなぜ？','干渉は2つの経路の波が重なって初めて起こります。経路が1つになると重ね合わせがなくなり、縞も消えます。'),
      ('これは本物の物理ですか？','干渉縞の現れ方を確率モデルで再現した可視化です。考え方は実際の二重スリット実験に基づいています。')])
    +refs([
      'Young, T. (1804) 光の干渉実験（ヤングの実験）',
      'Feynman, R. 『ファインマン物理学』二重スリットの章',
      'Tonomura, A. ほか (1989) 電子1個ずつの二重スリット実験（日立）']),
  share='粒を1個ずつ撃つだけなのに、積もると縞模様が現れる…ダブルスリット実験、量子の最大の謎⚛️',
  js='''  const c=$('cv'),x=c.getContext('2d'),W=c.width,H=c.height;
  const slitY=120,screenY=H-26,NB=120;
  let bins=new Float32Array(NB),maxb=1;
  function intensity(xpix){const gap=+$('gap').value;
    const cx=W/2,d=(xpix-cx);
    const sigma=W*0.30,envlp=Math.exp(-(d*d)/(2*sigma*sigma));
    if($('mode').value==='one'){const w=gap*1.3;return Math.exp(-(d*d)/(2*w*w));}
    const fr=Math.cos(d*Math.PI*gap/2600);
    return fr*fr*envlp;}
  function sample(){const cx=W/2;for(let tries=0;tries<60;tries++){const xp=Math.random()*W;const p=intensity(xp);if(Math.random()<p)return xp;}return cx+(Math.random()-0.5)*W*0.5;}
  function bg(){x.fillStyle='#05060f';x.fillRect(0,0,W,H);
    x.fillStyle='#2a3350';x.fillRect(0,slitY-4,W,8);
    const gap=+$('gap').value,cx=W/2,sw=10;
    x.clearRect(cx-gap/2-sw/2,slitY-4,sw,8);
    if($('mode').value==='two')x.clearRect(cx+gap/2-sw/2,slitY-4,sw,8);
    x.fillStyle='#05060f';x.fillRect(cx-gap/2-sw/2,slitY-4,sw,8);if($('mode').value==='two')x.fillRect(cx+gap/2-sw/2,slitY-4,sw,8);
    x.fillStyle='#1a2238';x.fillRect(0,screenY,W,4);}
  function fire(n){for(let i=0;i<n;i++){const xp=sample();const b=Math.min(NB-1,Math.max(0,(xp/W*NB)|0));bins[b]++;maxb=Math.max(maxb,bins[b]);
    const px=(b+0.5)/NB*W,py=screenY-2-Math.random()*1;x.fillStyle='rgba(120,200,255,0.9)';x.fillRect(xp-1,slitY+8+Math.random()*4,2,2);}
    drawScreen();}
  function drawScreen(){x.clearRect(0,screenY-150,W,150);
    for(let b=0;b<NB;b++){const h=bins[b]/maxb*140;const px=b/NB*W;
      const g=Math.round(120+120*bins[b]/maxb);x.fillStyle='rgba('+g+',200,255,0.9)';x.fillRect(px,screenY-h,W/NB+0.6,h);}}
  function reset(){bins=new Float32Array(NB);maxb=1;bg();}
  let auto=false;
  function loop(){fire(auto?40:6);requestAnimationFrame(loop);}
  $('reset').addEventListener('click',reset);
  $('fast').addEventListener('click',()=>{auto=!auto;$('fast').textContent=auto?'⏸ ゆっくり':'⏩ 一気に当てる';});
  $('gap').addEventListener('input',()=>{$('gapL').textContent=$('gap').value;reset();});
  $('mode').addEventListener('change',reset);
  reset();loop();'''))

# ============================================================
def write_all():
    for s in SIMS:
        d=os.path.join(ROOT,'sims',s['id']); os.makedirs(d,exist_ok=True)
        html=(TPL.replace('__TITLE__',s['title']).replace('__DESC__',s['desc'])
              .replace('__OGTITLE__',s['ogtitle']).replace('__OGDESC__',s['ogdesc'])
              .replace('__CAT__',s['cat']).replace('__H1__',s['h1']).replace('__LEAD__',s['lead'])
              .replace('__CANVAS__',s['canvas']).replace('__CONTROLS__',s['controls'])
              .replace('__LEGEND__',s['legend']).replace('__ARTICLE__',s['article'])
              .replace('__SHARE__',s['share']).replace('__JS__',s['js']).replace('__ID__',s['id']))
        with open(os.path.join(d,'index.html'),'w',encoding='utf-8') as f: f.write(html)
        print('created sims/'+s['id'])

if __name__=='__main__':
    write_all()
    print(f'visual done. {len(SIMS)} sims.')
