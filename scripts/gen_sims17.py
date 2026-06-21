# -*- coding: utf-8 -*-
"""シミュラボ：あそぶ・実験カテゴリ canvas系15本（凝ったインタラクティブ）。"""
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

CV = '<canvas id="cv" width="__W__" height="__H__" style="width:100%;max-width:__MX__px;height:auto;background:#0b1020;border:1px solid var(--line);border-radius:12px;__XTRA__"></canvas>'

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
  let SHARE = '__SHARE__';
  function syncSliders(){ document.querySelectorAll('input[type=range]').forEach(s=>{const l=$(s.id+'L'); if(l){const u=()=>l.textContent=s.value; s.addEventListener('input',u); u();}}); }
  function cpos(cv,e){ const r=cv.getBoundingClientRect(); const t=(e.touches&&e.touches[0])?e.touches[0]:e; return [(t.clientX-r.left)*cv.width/r.width,(t.clientY-r.top)*cv.height/r.height]; }
  try {
    syncSliders();
__JS__
  } catch(e) { console.error(e); }
  const sb=$('shareBtn'); if(sb) sb.addEventListener('click',()=>window.open('https://twitter.com/intent/tweet?text='+encodeURIComponent(SHARE)+'&url='+encodeURIComponent(location.href)+'&hashtags='+encodeURIComponent('シミュラボ'),'_blank','noopener'));
})();
</script>
<script src="../../assets/result-fx.js"></script>
<script src="../../assets/share-counter.js"></script>
<script>ShareCounter.initSim({ simId:'__ID__', badgeEl:document.getElementById('shareCount'), shareBtnIds:['shareBtn'] });</script>
</body>
</html>
'''

CAT='あそぶ・実験'

def faq(qa):
    return '<dl class="faq">' + ''.join(f'<dt>{q}</dt><dd>{a}</dd>' for q,a in qa) + '</dl>'

def canvas(w,h,mx,xtra=''):
    return CV.replace('__W__',str(w)).replace('__H__',str(h)).replace('__MX__',str(mx)).replace('__XTRA__',xtra)

def btn(id,label,primary=False):
    cls='btn btn-primary' if primary else 'btn btn-ghost'
    return f'<button class="{cls}" id="{id}" style="padding:11px 18px;font-size:14px;">{label}</button>'

def row(*items):
    return '<div class="share-row" style="margin-top:0;flex-wrap:wrap;">'+''.join(items)+'</div>'

def slider(id,label,mn,mx,val,step='1'):
    return (f'<div class="field" style="margin-bottom:10px;"><div class="slider-head" style="display:flex;justify-content:space-between;"><label style="margin:0;">{label}</label>'
            f'<span class="val" id="{id}L" style="font-weight:800;color:var(--teal-d);">{val}</span></div>'
            f'<input type="range" id="{id}" min="{mn}" max="{mx}" value="{val}" step="{step}" style="width:100%;"></div>')

def resbox():
    return '<div id="res" style="display:none;text-align:center;margin-top:6px;padding:14px;border-radius:12px;background:var(--teal-l);font-weight:800;color:var(--ink);"></div>'

SIMS=[]

# 1. ローレンツ・アトラクタ
SIMS.append(dict(id='lorenz', emoji='🦋',
  title='ローレンツ・アトラクタ｜カオスの蝶を描くシミュレーター｜シミュラボ',
  desc='たった3つの方程式から生まれる「カオスの蝶」ローレンツ・アトラクタを、回転しながら描き続ける美しい無料シミュレーター。',
  ogtitle='ローレンツ・アトラクタ｜カオスの蝶', ogdesc='3つの式から生まれるカオスの蝶を回転描画。',
  h1='ローレンツ・アトラクタ',
  lead='たった3つの方程式から、二度と同じ軌道を通らない「カオスの蝶」が生まれます。回転しながら描かれる軌跡を眺めてみてください。',
  canvas=canvas(600,420,600,'cursor:default;'),
  controls=row(btn('reset','最初から',True))+slider('spd','スピード',1,12,5),
  legend='バタフライ効果の語源。初期値のごくわずかな差が、まったく違う未来になる「カオス」の象徴です。',
  article='''    <h2>カオスの蝶とは</h2>
    <p>気象学者ローレンツが大気の対流を3つの式で表したところ、初期値のほんの少しの違いが将来を大きく変えることを発見しました。これが「バタフライ効果」。軌跡は蝶のような形を描き、二度と同じ点を通りません。</p>
    <h2>よくある質問</h2>'''+faq([('同じ絵になりますか？','形は似ますが、軌道は毎回わずかに違います。それがカオスです。'),('データは送信されますか？','いいえ。すべてブラウザ内で動きます。')]),
  share='たった3つの式から"カオスの蝶"が生まれる…ローレンツ・アトラクタ、ずっと見てられる🦋',
  js='''
    const cv=$('cv'),x=cv.getContext('2d');const W=cv.width,H=cv.height;
    let px=0.1,py=0,pz=0;const s=10,r=28,b=8/3,dt=0.006;let pts=[],ang=0;
    function reset(){px=0.1;py=0;pz=0;pts=[];}
    $('reset').addEventListener('click',reset);
    function loop(){
      const it=+$('spd').value;
      for(let i=0;i<it*2;i++){const dx=s*(py-px),dy=px*(r-pz)-py,dz=px*py-b*pz;px+=dx*dt;py+=dy*dt;pz+=dz*dt;pts.push([px,py,pz]);}
      if(pts.length>5000)pts.splice(0,pts.length-5000);
      ang+=0.004; x.fillStyle='#0b1020';x.fillRect(0,0,W,H);
      const cx=W/2,cy=H/2+20,sc=8.5,ca=Math.cos(ang),sa=Math.sin(ang);
      for(let i=1;i<pts.length;i++){const a=pts[i-1],c=pts[i];
        const ax=a[0]*ca-a[1]*sa, cxx=c[0]*ca-c[1]*sa;
        x.strokeStyle='hsla('+((i/pts.length*200+190)%360)+',90%,62%,'+(0.25+0.6*i/pts.length)+')';x.lineWidth=1.2;
        x.beginPath();x.moveTo(cx+ax*sc,cy-(a[2]-25)*sc);x.lineTo(cx+cxx*sc,cy-(c[2]-25)*sc);x.stroke();}
      requestAnimationFrame(loop);
    } loop();
'''))

# 2. 振り子の波
SIMS.append(dict(id='pendulum-wave', emoji='🎐',
  title='振り子の波｜長さの違う振り子が作る波模様シミュレーター｜シミュラボ',
  desc='長さを少しずつ変えた15個の振り子が、ばらばらに揺れたり一直線にそろったりを繰り返す「振り子の波」を体感できる無料シミュレーター。',
  ogtitle='振り子の波｜長さの違う振り子が作る波模様', ogdesc='15個の振り子が波・らせん・整列をくり返す不思議。',
  h1='振り子の波',
  lead='長さをほんの少しずつ変えた15個の振り子。動かすと波になり、らせんになり、やがてピタッとそろう——その繰り返しに見入ってしまいます。',
  canvas=canvas(600,420,600),
  controls=row(btn('reset','スタート',True)),
  legend='各振り子の周期がわずかに違うため、ずれては重なるパターン（うなり）が生まれます。',
  article='''    <h2>なぜ波模様になる？</h2>
    <p>振り子の周期は「長さ」で決まります。一定時間にちょうど51回・52回・53回…と揺れるよう長さを調整すると、最初はそろっていた振り子が少しずつずれて波模様になり、一定時間ごとに再びそろいます。物理の美しさを体感できる定番デモです。</p>
    <h2>よくある質問</h2>'''+faq([('実際に作れる？','はい。科学館の展示でも人気です。長さの精密な調整がポイント。'),('データは送信されますか？','いいえ。すべてブラウザ内で動きます。')]),
  share='長さの違う15個の振り子が、波になってまた一直線にそろう…振り子の波、催眠術みたい🎐',
  js='''
    const cv=$('cv'),x=cv.getContext('2d');const W=cv.width,H=cv.height;const N=15;
    let t0=performance.now();
    $('reset').addEventListener('click',()=>t0=performance.now());
    const cycle=30, base=51;
    function loop(now){
      const t=(now-t0)/1000; x.fillStyle='#0b1020';x.fillRect(0,0,W,H);
      const topY=24,amp=0.55,maxLen=H-70;
      for(let i=0;i<N;i++){
        const osc=base+i, T=cycle/osc, ang=amp*Math.cos(2*Math.PI*t/T);
        const len=maxLen*(0.55+0.45*i/(N-1));
        const ax=W*(i+1)/(N+1), bx=ax+Math.sin(ang)*len, by=topY+Math.cos(ang)*len;
        x.strokeStyle='rgba(255,255,255,.18)';x.lineWidth=1;x.beginPath();x.moveTo(ax,topY);x.lineTo(bx,by);x.stroke();
        x.fillStyle='hsl('+(i/N*300)+',85%,63%)';x.beginPath();x.arc(bx,by,9,0,7);x.fill();
      }
      requestAnimationFrame(loop);
    } requestAnimationFrame(loop);
'''))

# 3. 太陽系
SIMS.append(dict(id='solar-system', emoji='🪐',
  title='太陽系シミュレーター｜惑星の公転を眺める無料シミュレーター｜シミュラボ',
  desc='水星から海王星まで8つの惑星が、それぞれの速さで太陽のまわりを回る様子を眺められる無料シミュレーター。スピードも変えられます。',
  ogtitle='太陽系シミュレーター｜惑星の公転を眺める', ogdesc='8惑星がそれぞれの速さで公転。スピード調整も。',
  h1='太陽系シミュレーター',
  lead='水星はせかせか、海王星はゆったり。8つの惑星が、それぞれの速さで太陽を回ります。内側ほど速い——その理由も体感できます。',
  canvas=canvas(560,560,560),
  controls=row(btn('pause','⏸ 一時停止',True))+slider('spd','スピード',1,40,12)+slider('orbit','軌道を表示',0,1,1),
  legend='内側の惑星ほど速く回ります（ケプラーの法則）。太陽の重力が強く働くためです。',
  article='''    <h2>内側ほど速いのはなぜ？</h2>
    <p>太陽に近い惑星ほど重力を強く受け、速く回らないと落ちてしまいます。だから水星の1年は88日、海王星は165年。実際の公転周期の比に合わせて回しています（距離は見やすく圧縮）。</p>
    <h2>よくある質問</h2>'''+faq([('距離は正確？','見やすさ優先で圧縮しています。周期の比は実際に近づけています。'),('データは送信されますか？','いいえ。すべてブラウザ内で動きます。')]),
  share='8つの惑星がそれぞれの速さで太陽を回る…太陽系シミュレーター、内側ほど速いのが分かる🪐',
  js='''
    const cv=$('cv'),x=cv.getContext('2d');const W=cv.width,H=cv.height,cx=W/2,cy=H/2;
    const P=[[44,2.6,'#b8b8b8',0.24],[66,4.2,'#e0a060',0.62],[88,4.6,'#4a90e2',1],[110,3.6,'#e0563a',1.88],[150,9,'#d9a066',11.9],[195,7.5,'#e6c98a',29.5],[230,6,'#9ad0e6',84],[260,6,'#5a7de0',165]];
    let ang=P.map(()=>Math.random()*7),playing=true;
    $('pause').addEventListener('click',()=>{playing=!playing;$('pause').textContent=playing?'⏸ 一時停止':'▶ 再生';});
    function loop(){
      const sp=+$('spd').value/2000; x.fillStyle='#05060f';x.fillRect(0,0,W,H);
      for(let i=0;i<200;i++){x.fillStyle='rgba(255,255,255,'+(Math.random()*0.4)+')';x.fillRect((i*97)%W,(i*53)%H,1,1);}
      if(+$('orbit').value>0){x.strokeStyle='rgba(255,255,255,.10)';for(const p of P){x.beginPath();x.arc(cx,cy,p[0],0,7);x.stroke();}}
      const g=x.createRadialGradient(cx,cy,2,cx,cy,26);g.addColorStop(0,'#fff3b0');g.addColorStop(1,'#f59e0b');x.fillStyle=g;x.beginPath();x.arc(cx,cy,15,0,7);x.fill();
      for(let i=0;i<P.length;i++){const p=P[i];if(playing)ang[i]+=sp/p[3];const x0=cx+Math.cos(ang[i])*p[0],y0=cy+Math.sin(ang[i])*p[0];x.fillStyle=p[2];x.beginPath();x.arc(x0,y0,p[1],0,7);x.fill();}
      requestAnimationFrame(loop);
    } loop();
'''))

# 4. 重力シミュレーター
SIMS.append(dict(id='gravity', emoji='🌌',
  title='重力シミュレーター｜クリックで惑星を放り込むと軌道が生まれる｜シミュラボ',
  desc='画面をクリックすると小さな星が生まれ、中心の星の重力で公転したり、引き合ったりする様子を観察できる無料の重力シミュレーター。',
  ogtitle='重力シミュレーター｜クリックで惑星を放り込む', ogdesc='クリックで星を放つと重力で軌道が生まれる。',
  h1='重力シミュレーター',
  lead='画面をクリック（タップ）すると、小さな星が生まれます。中心の太陽の重力に引かれて、公転したり、落ちたり、はじき飛ばされたり。あなただけの星系を作ってみてください。',
  canvas=canvas(640,440,640,'cursor:crosshair;'),
  controls=row(btn('clear','リセット',True)),
  legend='クリックで星を追加／重力で互いに引き合います。絶妙な速度だと安定した軌道に。',
  article='''    <h2>軌道が生まれるしくみ</h2>
    <p>星は中心の太陽に向かって落ちますが、横向きの速度があると「落ち続けながら回る」＝公転になります。速すぎると飛び去り、遅すぎると落下。地球が太陽を回るのも同じ原理です。万有引力（距離の2乗に反比例）で計算しています。</p>
    <h2>よくある質問</h2>'''+faq([('安定した軌道を作るコツは？','中心から少し離れた場所をクリックすると、自動でほどよい初速がつきます。'),('データは送信されますか？','いいえ。すべてブラウザ内で動きます。')]),
  share='クリックで星を放り込むと重力で軌道が生まれる…重力シミュレーター、自分だけの星系が作れる🌌',
  js='''
    const cv=$('cv'),x=cv.getContext('2d');const W=cv.width,H=cv.height;const G=0.9;
    let sun={x:W/2,y:H/2,m:1600},bodies=[];
    function add(px,py){const dx=px-sun.x,dy=py-sun.y,d=Math.hypot(dx,dy)||1;const v=Math.sqrt(G*sun.m/d)*0.9;bodies.push({x:px,y:py,vx:-dy/d*v,vy:dx/d*v,m:6,t:[],c:'hsl('+(Math.random()*360)+',85%,65%)'});}
    cv.addEventListener('click',e=>{const p=cpos(cv,e);add(p[0],p[1]);});
    cv.addEventListener('touchstart',e=>{e.preventDefault();const p=cpos(cv,e);add(p[0],p[1]);},{passive:false});
    $('clear').addEventListener('click',()=>bodies=[]);
    for(let i=0;i<3;i++)add(W/2+90+i*55,H/2);
    function loop(){
      x.fillStyle='rgba(5,6,15,.35)';x.fillRect(0,0,W,H);
      for(const bd of bodies){let ax=0,ay=0;const dx=sun.x-bd.x,dy=sun.y-bd.y,d=Math.hypot(dx,dy)||1;const f=G*sun.m/(d*d);ax+=dx/d*f;ay+=dy/d*f;
        bd.vx+=ax*0.12;bd.vy+=ay*0.12;bd.x+=bd.vx*0.12;bd.y+=bd.vy*0.12;bd.t.push([bd.x,bd.y]);if(bd.t.length>40)bd.t.shift();
        x.strokeStyle=bd.c;x.globalAlpha=.4;x.beginPath();for(let i=0;i<bd.t.length;i++){const p=bd.t[i];i?x.lineTo(p[0],p[1]):x.moveTo(p[0],p[1]);}x.stroke();x.globalAlpha=1;
        x.fillStyle=bd.c;x.beginPath();x.arc(bd.x,bd.y,bd.m*0.7,0,7);x.fill();}
      const g=x.createRadialGradient(sun.x,sun.y,2,sun.x,sun.y,34);g.addColorStop(0,'#fff3b0');g.addColorStop(1,'rgba(245,158,11,0)');x.fillStyle=g;x.beginPath();x.arc(sun.x,sun.y,34,0,7);x.fill();
      x.fillStyle='#ffd34d';x.beginPath();x.arc(sun.x,sun.y,13,0,7);x.fill();
      bodies=bodies.filter(b=>b.x>-200&&b.x<W+200&&b.y>-200&&b.y<H+200);
      requestAnimationFrame(loop);
    } loop();
'''))

# 5. 花火
SIMS.append(dict(id='fireworks', emoji='🎆',
  title='花火シミュレーター｜タップで打ち上がる花火｜シミュラボ',
  desc='画面をタップすると花火が打ち上がって夜空に咲く、癒やしの無料花火シミュレーター。色とりどりの火花が重力で散っていきます。',
  ogtitle='花火シミュレーター｜タップで打ち上がる花火', ogdesc='タップで花火を打ち上げ。夜空に色とりどりの花火。',
  h1='花火シミュレーター',
  lead='画面をタップすると、花火が打ち上がって夜空に咲きます。連打すれば豪華に。音は出ないので、いつでもどこでも夏気分を。',
  canvas=canvas(640,460,640,'cursor:pointer;'),
  controls=row(btn('auto','自動で打ち上げ',True)),
  legend='タップで打ち上げ／火花は重力で落ちながら消えていきます。',
  article='''    <h2>花火の動きの再現</h2>
    <p>打ち上げの玉が最高点で爆発し、数百個の火花が全方向へ飛び散ります。各火花には重力と空気抵抗、そして少しずつ消えていく明るさを与えています。シンプルな粒子（パーティクル）の集まりで、本物らしい動きが生まれます。</p>
    <h2>よくある質問</h2>'''+faq([('音は出ますか？','出ません。静かに楽しめます。'),('データは送信されますか？','いいえ。すべてブラウザ内で動きます。')]),
  share='タップで打ち上がる花火シミュレーター🎆 音が出ないからいつでも夏気分。連打すると豪華！',
  js='''
    const cv=$('cv'),x=cv.getContext('2d');const W=cv.width,H=cv.height;
    let rockets=[],sparks=[],auto=false;
    function launch(tx){const x0=tx!=null?tx:60+Math.random()*(W-120);rockets.push({x:x0,y:H,vy:-(7+Math.random()*2.5),ty:80+Math.random()*160,c:'hsl('+(Math.random()*360)+',90%,62%)'});}
    function burst(px,py,c){for(let i=0;i<90;i++){const a=Math.random()*7,s=Math.random()*4+1;sparks.push({x:px,y:py,vx:Math.cos(a)*s,vy:Math.sin(a)*s,life:1,c:c});}}
    cv.addEventListener('click',e=>{const p=cpos(cv,e);launch(p[0]);});
    cv.addEventListener('touchstart',e=>{e.preventDefault();const p=cpos(cv,e);launch(p[0]);},{passive:false});
    $('auto').addEventListener('click',()=>{auto=!auto;$('auto').textContent=auto?'■ 自動を止める':'自動で打ち上げ';});
    let f=0;
    function loop(){
      f++; if(auto&&f%28===0)launch();
      x.fillStyle='rgba(8,10,26,.28)';x.fillRect(0,0,W,H);
      for(const r of rockets){r.y+=r.vy;r.vy+=0.06;x.fillStyle=r.c;x.fillRect(r.x,r.y,3,3);if(r.y<=r.ty||r.vy>=0){burst(r.x,r.y,r.c);r.dead=1;}}
      rockets=rockets.filter(r=>!r.dead);
      for(const s of sparks){s.x+=s.vx;s.y+=s.vy;s.vy+=0.05;s.vx*=0.99;s.life-=0.012;x.globalAlpha=Math.max(0,s.life);x.fillStyle=s.c;x.fillRect(s.x,s.y,2.4,2.4);}
      x.globalAlpha=1;sparks=sparks.filter(s=>s.life>0);
      requestAnimationFrame(loop);
    } loop(); setTimeout(()=>launch(),400);
'''))

# 6. フラクタルの木
SIMS.append(dict(id='fractal-tree', emoji='🌳',
  title='フラクタルの木｜枝分かれの数式で育つ木シミュレーター｜シミュラボ',
  desc='枝が同じルールで分かれ続ける「フラクタルの木」を、角度や深さを変えながら描ける無料シミュレーター。風でゆれる演出つき。',
  ogtitle='フラクタルの木｜枝分かれの数式で育つ木', ogdesc='角度と深さのスライダーで自分だけの木を育てる。',
  h1='フラクタルの木',
  lead='「枝の先で2つに分かれる」を繰り返すだけ。それだけで本物の木のような形が生まれます。角度と深さを変えて、あなただけの木を育ててみてください（そよ風でゆれます）。',
  canvas=canvas(600,460,600),
  controls=slider('ang','枝の角度',10,50,26)+slider('depth','枝分かれの深さ',6,13,11)+slider('wind','風のつよさ',0,10,3),
  legend='全体が部分と同じ形（自己相似）になるのがフラクタル。木・血管・川・雷も同じ仲間です。',
  article='''    <h2>フラクタルとは</h2>
    <p>拡大しても全体と同じような形が現れる図形のこと。木の枝、川の支流、肺の血管、稲妻——自然界はフラクタルだらけです。単純な「分かれるルール」の繰り返しが、複雑で自然な形を生み出します。</p>
    <h2>よくある質問</h2>'''+faq([('深さを上げると重い？','枝の数が指数的に増えます。13くらいまでが快適です。'),('データは送信されますか？','いいえ。すべてブラウザ内で動きます。')]),
  share='角度を変えるだけで本物みたいな木が育つ…フラクタルの木🌳 自然界がフラクタルだらけって納得。',
  js='''
    const cv=$('cv'),x=cv.getContext('2d');const W=cv.width,H=cv.height;let t=0;
    function branch(px,py,len,ang,depth,sway){
      if(depth<=0||len<2)return;
      const ex=px+Math.cos(ang)*len, ey=py+Math.sin(ang)*len;
      x.strokeStyle='hsl('+(110-depth*6)+','+(40+depth*4)+'%,'+(28+depth*4)+'%)';x.lineWidth=depth*0.9;
      x.beginPath();x.moveTo(px,py);x.lineTo(ex,ey);x.stroke();
      const da=(+$('ang').value)*Math.PI/180;
      const w=sway*Math.sin(t*0.8+depth)*0.04;
      branch(ex,ey,len*0.74,ang-da+w,depth-1,sway);
      branch(ex,ey,len*0.74,ang+da+w,depth-1,sway);
    }
    function loop(){
      t+=0.03; x.fillStyle='#0b1020';x.fillRect(0,0,W,H);
      branch(W/2,H-10,H*0.22,-Math.PI/2,+$('depth').value,+$('wind').value);
      requestAnimationFrame(loop);
    } loop();
'''))

# 7. マンデルブロ集合
SIMS.append(dict(id='mandelbrot', emoji='🌀',
  title='マンデルブロ集合エクスプローラー｜無限に続く模様をズーム｜シミュラボ',
  desc='ひとつの式の繰り返しから生まれる、無限に複雑な模様「マンデルブロ集合」。クリックでどこまでもズームできる無料シミュレーター。',
  ogtitle='マンデルブロ集合｜無限に続く模様をズーム', ogdesc='クリックでどこまでもズームできる無限フラクタル。',
  h1='マンデルブロ集合エクスプローラー',
  lead='たったひとつの式「z = z² + c」を繰り返すだけ。なのに、ズームしてもズームしても新しい模様が現れ続けます。クリックでどこまでも潜ってみてください。',
  canvas=canvas(480,360,560,'cursor:zoom-in;'),
  controls=row(btn('reset','最初に戻る',True),btn('out','ズームアウト'))+'<p style="text-align:center;color:var(--ink-2);font-size:12px;margin:6px 0 0;">画面をクリックでズームイン</p>',
  legend='境界を拡大すると、全体とそっくりな小さなマンデルブロが無限に現れます。',
  article='''    <h2>無限に複雑な理由</h2>
    <p>各点について「z = z² + c」を繰り返し、無限大に飛んでいくか踏みとどまるかを色で表したものです。境界線は無限に入り組んでいて、拡大するたびに新しい渦や、全体と同じ小さなマンデルブロが現れます。たった1行の式が生む無限の世界です。</p>
    <h2>よくある質問</h2>'''+faq([('どこまでズームできる？','数値の精度の限界まで。本ツールでも数十段は潜れます。'),('データは送信されますか？','いいえ。すべてブラウザ内で計算します。')]),
  share='たった1行の式から無限に複雑な模様が生まれる…マンデルブロ集合、ズームが止まらない🌀',
  js='''
    const cv=$('cv'),x=cv.getContext('2d');const W=cv.width,H=cv.height;
    let cxx=-0.6,cyy=0,scale=3.2;
    function render(){
      const img=x.createImageData(W,H),d=img.data,maxI=140;
      for(let py=0;py<H;py++){const y0=cyy+(py/H-0.5)*scale*H/W;
        for(let px=0;px<W;px++){const x0=cxx+(px/W-0.5)*scale;
          let a=0,b=0,i=0;for(;i<maxI;i++){const a2=a*a-b*b+x0,b2=2*a*b+y0;a=a2;b=b2;if(a*a+b*b>4)break;}
          const k=(py*W+px)*4;
          if(i>=maxI){d[k]=8;d[k+1]=10;d[k+2]=26;}
          else{const t=i/maxI;d[k]=Math.floor(9+255*Math.pow(t,0.5)*Math.abs(Math.sin(t*7)));d[k+1]=Math.floor(20+180*t);d[k+2]=Math.floor(60+180*(1-t));}
          d[k+3]=255;}}
      x.putImageData(img,0,0);
    }
    cv.addEventListener('click',e=>{const p=cpos(cv,e);cxx=cxx+(p[0]/W-0.5)*scale;cyy=cyy+(p[1]/H-0.5)*scale*H/W;scale*=0.5;render();});
    $('reset').addEventListener('click',()=>{cxx=-0.6;cyy=0;scale=3.2;render();});
    $('out').addEventListener('click',()=>{scale*=2;render();});
    render();
'''))

# 8. ワープ星空
SIMS.append(dict(id='starfield', emoji='🌟',
  title='ワープ星空シミュレーター｜星の中を飛ぶ｜シミュラボ',
  desc='まるで宇宙船で星の中を飛んでいるような「ワープ星空」を体感できる無料シミュレーター。スピードを上げると光の筋に。',
  ogtitle='ワープ星空シミュレーター｜星の中を飛ぶ', ogdesc='星の中を飛ぶワープ体験。スピードで光の筋に。',
  h1='ワープ星空シミュレーター',
  lead='宇宙船で星の海を進むような映像を、ブラウザだけで。スピードを上げると、星が光の筋になってワープ感が増します。',
  canvas=canvas(640,440,640),
  controls=slider('spd','スピード',1,30,8),
  legend='手前に近づく星ほど速く・大きく見えます（遠近感）。スピードを上げると光跡に。',
  article='''    <h2>遠近感の作り方</h2>
    <p>星に奥行き（z座標）を持たせ、近づくほど画面の外側へ大きく速く動くように描いています。これだけで「自分が前進している」感覚が生まれます。古くからあるデモですが、何度見ても気持ちいい演出です。</p>
    <h2>よくある質問</h2>'''+faq([('酔いませんか？','スピードを下げるとゆったり眺められます。'),('データは送信されますか？','いいえ。すべてブラウザ内で動きます。')]),
  share='星の中を飛ぶワープ星空シミュレーター🌟 スピード上げると光の筋になって気持ちいい！',
  js='''
    const cv=$('cv'),x=cv.getContext('2d');const W=cv.width,H=cv.height,cx=W/2,cy=H/2;
    let st=[];for(let i=0;i<260;i++)st.push({x:(Math.random()-0.5)*W,y:(Math.random()-0.5)*H,z:Math.random()*W});
    function loop(){
      const sp=+$('spd').value; x.fillStyle='rgba(5,6,15,.35)';x.fillRect(0,0,W,H);
      for(const s of st){const oz=s.z;s.z-=sp;if(s.z<1){s.z=W;s.x=(Math.random()-0.5)*W;s.y=(Math.random()-0.5)*H;continue;}
        const k=128/s.z,sx=cx+s.x*k,sy=cy+s.y*k,ok=128/oz,ox=cx+s.x*ok,oy=cy+s.y*ok;
        const r=Math.max(0.5,(1-s.z/W)*2.6);x.strokeStyle='rgba(255,255,255,'+(1-s.z/W)+')';x.lineWidth=r;
        x.beginPath();x.moveTo(ox,oy);x.lineTo(sx,sy);x.stroke();}
      requestAnimationFrame(loop);
    } loop();
'''))

# 9. 歯車
SIMS.append(dict(id='gears', emoji='⚙️',
  title='歯車シミュレーター｜かみ合う歯車と回転比｜シミュラボ',
  desc='かみ合って回る歯車の歯数を変えると、回転の速さの比（ギア比）がどう変わるかを目と数字で確かめられる無料シミュレーター。',
  ogtitle='歯車シミュレーター｜かみ合う歯車と回転比', ogdesc='歯数を変えてギア比＝回転速度の比を体感。',
  h1='歯車シミュレーター',
  lead='大きい歯車はゆっくり、小さい歯車はくるくる。かみ合う歯車の歯数を変えて、回転の速さの比（ギア比）が変わる様子を見てみましょう。',
  canvas=canvas(600,420,600),
  controls=slider('t1','左の歯数',8,40,24)+slider('t2','右の歯数',8,40,12),
  legend='歯数の比が、そのまま回転数の逆比に。歯数が半分の歯車は2倍速く回ります。',
  article='''    <h2>ギア比のしくみ</h2>
    <p>かみ合う歯車は、歯のかみ合う数が同じになるよう回ります。だから歯数が半分の歯車は2倍の速さで回転。自転車の変速、車のミッション、時計の針——すべてこの原理です。</p>
    <h2>よくある質問</h2>'''+faq([('なぜ逆向きに回る？','かみ合う歯車は必ず反対方向に回ります。'),('データは送信されますか？','いいえ。すべてブラウザ内で動きます。')]),
  share='歯数を変えると回転速度の比が変わる…歯車シミュレーター⚙️ 自転車の変速もこれか！',
  js='''
    const cv=$('cv'),x=cv.getContext('2d');const W=cv.width,H=cv.height;let a=0;
    function gear(cx,cy,teeth,rot,col){
      const pr=teeth*4.2, ad=6; x.fillStyle=col;x.beginPath();
      for(let i=0;i<teeth;i++){const t0=rot+i/teeth*Math.PI*2,t1=rot+(i+0.5)/teeth*Math.PI*2;
        x.lineTo(cx+Math.cos(t0)*(pr+ad),cy+Math.sin(t0)*(pr+ad));
        x.lineTo(cx+Math.cos(t0+0.0001)*(pr+ad),cy+Math.sin(t0)*(pr+ad));
        const m0=rot+(i+0.25)/teeth*Math.PI*2;
        x.lineTo(cx+Math.cos(m0)*pr,cy+Math.sin(m0)*pr);
        x.lineTo(cx+Math.cos(t1)*pr,cy+Math.sin(t1)*pr);}
      x.closePath();x.fill();
      x.fillStyle='#0b1020';x.beginPath();x.arc(cx,cy,pr*0.35,0,7);x.fill();
      x.strokeStyle='#0b1020';x.lineWidth=3;x.beginPath();x.moveTo(cx,cy);x.lineTo(cx+Math.cos(rot)*pr*0.8,cy+Math.sin(rot)*pr*0.8);x.stroke();
    }
    function loop(){
      const t1=+$('t1').value,t2=+$('t2').value; x.fillStyle='#0b1020';x.fillRect(0,0,W,H);
      const r1=t1*4.2,r2=t2*4.2,gap=r1+r2+12; const cx1=W/2-gap/2+10,cx2=cx1+gap-0; const cy=H/2;
      a+=0.012; gear(cx1,cy,t1,a,'#5eead4'); gear(cx2,cy,t2,-a*t1/t2+Math.PI/t2,'#a78bfa');
      x.fillStyle='#fff';x.font='bold 15px sans-serif';x.textAlign='center';
      x.fillText('×'+(t1/t2).toFixed(2)+'倍速',W/2,H-14);
      requestAnimationFrame(loop);
    } loop();
'''))

# 10. DNAらせん
SIMS.append(dict(id='dna', emoji='🧬',
  title='DNA二重らせんシミュレーター｜回る生命の設計図｜シミュラボ',
  desc='くるくると回転するDNAの二重らせんを眺められる無料シミュレーター。塩基対のはしごが立体的に回ります。',
  ogtitle='DNA二重らせん｜回る生命の設計図', ogdesc='回転する立体的なDNA二重らせんを眺める。',
  h1='DNA二重らせんシミュレーター',
  lead='私たちの体の設計図、DNA。2本のひもがはしごのようにつながり、らせんを描いて回ります。立体的に回転する二重らせんを眺めてみてください。',
  canvas=canvas(440,560,440),
  controls=slider('spd','回転スピード',1,12,5),
  legend='4種類の塩基（A・T・G・C）の並びが、生き物すべての設計図になっています。',
  article='''    <h2>二重らせんとは</h2>
    <p>DNAは2本の鎖がねじれて結びついた「二重らせん」構造。鎖の間をつなぐ「塩基」はA-T、G-Cの組でペアになります。この4文字の並び順が、私たちの体をつくる遺伝情報そのもの。1953年にワトソンとクリックが構造を解明しました。</p>
    <h2>よくある質問</h2>'''+faq([('色の意味は？','塩基対をイメージした色分けです（A-T／G-C）。'),('データは送信されますか？','いいえ。すべてブラウザ内で動きます。')]),
  share='くるくる回るDNA二重らせん🧬 これが生命の設計図か…と眺めてしまう。',
  js='''
    const cv=$('cv'),x=cv.getContext('2d');const W=cv.width,H=cv.height,cx=W/2;let p=0;
    const cols=[['#f43f5e','#fb923c'],['#22d3ee','#60a5fa']];
    function loop(){
      p+=(+$('spd').value)*0.012; x.fillStyle='#0b1020';x.fillRect(0,0,W,H);
      const n=26,amp=W*0.32;
      for(let i=0;i<n;i++){const y=30+i*(H-60)/n,ph=p+i*0.5;
        const x1=cx+Math.sin(ph)*amp,x2=cx+Math.sin(ph+Math.PI)*amp;
        const z1=Math.cos(ph),z2=Math.cos(ph+Math.PI);
        const c=cols[i%2];
        x.strokeStyle='rgba(255,255,255,.5)';x.lineWidth=2;x.beginPath();x.moveTo(x1,y);x.lineTo(x2,y);x.stroke();
        const r1=4+z1*2.5,r2=4+z2*2.5;
        x.fillStyle=c[0];x.globalAlpha=0.5+0.5*(z1+1)/2;x.beginPath();x.arc(x1,y,Math.abs(r1)+3,0,7);x.fill();
        x.fillStyle=c[1];x.globalAlpha=0.5+0.5*(z2+1)/2;x.beginPath();x.arc(x2,y,Math.abs(r2)+3,0,7);x.fill();x.globalAlpha=1;}
      requestAnimationFrame(loop);
    } loop();
'''))

# 11. 反応速度テスト
SIMS.append(dict(id='reaction-test', emoji='⚡',
  title='反応速度テスト｜あなたの反射神経は何ミリ秒？｜シミュラボ',
  desc='画面が緑に変わった瞬間にクリック。あなたの反応速度（反射神経）を5回の平均で測定し、ランク判定するゲーム型シミュレーター。',
  ogtitle='反応速度テスト｜反射神経は何ミリ秒？', ogdesc='緑になった瞬間にクリック。反応速度を測定＆ランク判定。',
  h1='反応速度テスト',
  lead='赤い画面が緑に変わった瞬間に、できるだけ速くクリック（タップ）！5回の平均で、あなたの反射神経を測定します。早押しゲームに自信ある人、挑戦どうぞ。',
  canvas=canvas(600,360,600,'cursor:pointer;'),
  controls=row(btn('start','スタート',True))+resbox(),
  legend='人間の平均は約250ミリ秒。緑になる前に押すとフライング判定です。',
  article='''    <h2>反応速度のはなし</h2>
    <p>光を見てから手を動かすまでには、目→脳→手と信号が伝わる時間がかかります。一般的な平均は200〜250ミリ秒ほど。eスポーツ選手やアスリートはこれが速い傾向があります。寝不足や疲れでも遅くなるので、コンディションチェックにも。</p>
    <h2>よくある質問</h2>'''+faq([('スマホでもできる？','はい。タップで測定できます。'),('データは送信されますか？','いいえ。すべてブラウザ内で測定します。')]),
  share='反応速度テストやってみた⚡ 君の反射神経は何ミリ秒？',
  js='''
    const cv=$('cv'),x=cv.getContext('2d');const W=cv.width,H=cv.height;
    let state='idle',t0=0,times=[],to=null;
    function paint(col,line1,line2){x.fillStyle=col;x.fillRect(0,0,W,H);x.fillStyle='#fff';x.textAlign='center';x.font='bold 34px sans-serif';x.fillText(line1,W/2,H/2-6);if(line2){x.font='bold 20px sans-serif';x.fillText(line2,W/2,H/2+34);}}
    function ready(){state='wait';paint('#dc2626','まだ…','緑になったらクリック！');to=setTimeout(()=>{state='go';t0=performance.now();paint('#16a34a','今だ！クリック！');},900+Math.random()*2200);}
    function finish(){const avg=Math.round(times.reduce((a,b)=>a+b,0)/times.length);let rank;if(avg<200)rank='超人級！🦅';else if(avg<250)rank='かなり速い⚡';else if(avg<320)rank='平均的';else rank='ねむい？😴';
      $('res').style.display='';$('res').innerHTML='平均 <span style="font-size:26px;color:var(--accent-d)">'+avg+'</span> ミリ秒　'+rank+'<br><span style="font-weight:600;font-size:13px;">'+times.map(t=>t+'ms').join(' / ')+'</span>';
      SHARE='反応速度テスト、私の反射神経は平均'+avg+'ミリ秒（'+rank+'）でした⚡ 君は？';
      paint('#0b1020','結果が出たよ →','もう一度はスタート');state='idle';}
    cv.addEventListener('pointerdown',()=>{
      if(state==='wait'){clearTimeout(to);paint('#0b1020','フライング！','スタートからやり直し');state='idle';times=[];return;}
      if(state==='go'){const t=Math.round(performance.now()-t0);times.push(t);if(times.length>=5){finish();}else{paint('#0b1020',t+' ミリ秒',(times.length)+'/5回 完了 → クリックで次');state='between';}return;}
      if(state==='between'){ready();return;}
    });
    $('start').addEventListener('click',()=>{times=[];$('res').style.display='none';ready();});
    paint('#0b1020','スタートを押してね','緑になった瞬間にクリック');
'''))

# 12. タイピング速度
SIMS.append(dict(id='typing-test', emoji='⌨️',
  title='タイピング速度測定｜あなたのタイピングは何打/分？｜シミュラボ',
  desc='表示された文章を入力して、タイピングの速さ（1分あたりの文字数）と正確率を測定する無料のタイピングテスト。',
  ogtitle='タイピング速度測定｜何打/分？', ogdesc='文章を入力してタイピング速度と正確率を測定。',
  h1='タイピング速度測定',
  lead='表示された文章を、できるだけ速く正確に入力してください。1分あたりの入力文字数（CPM）と正確率、ランクを判定します。',
  canvas='',
  controls='<div id="target" style="background:var(--teal-l);border-radius:12px;padding:16px;font-size:18px;line-height:1.8;margin-bottom:12px;min-height:60px;">スタートを押すと文章が出ます。</div>'
          +'<textarea id="inp" rows="3" placeholder="ここに入力…" style="width:100%;padding:12px;border:1.5px solid var(--line);border-radius:12px;font-size:16px;" disabled></textarea>'
          +row(btn('start','スタート',True))+resbox(),
  legend='速さだけでなく正確さも大事。ミスタイプは正確率に反映されます。',
  article='''    <h2>CPMとは</h2>
    <p>CPM（Characters Per Minute）は1分あたりに打てる文字数のこと。日本語入力ならローマ字の打鍵数で変わりますが、目安として150CPMで「日常的に困らない」、300CPM超で「速い」と言われます。毎日少しずつで誰でも上達します。</p>
    <h2>よくある質問</h2>'''+faq([('日本語と英語どっち？','本テストはやさしい日本語（かな）の文章で測ります。'),('データは送信されますか？','いいえ。すべてブラウザ内で測定します。')]),
  share='タイピング速度を測ってみた⌨️ 君は何打/分？',
  js='''
    const texts=['すもももももももものうち','となりのきゃくはよくかきくうきゃくだ','はやおきはさんもんのとく','あしたはきっといいてんきになる','ねこはこたつでまるくなる','ちりもつもればやまとなる','いそがばまわれということわざ','あさごはんをしっかりたべよう'];
    const inp=$('inp');let cur='',st=0;
    $('start').addEventListener('click',()=>{cur=texts[Math.floor(Math.random()*texts.length)];$('target').textContent=cur;inp.disabled=false;inp.value='';inp.focus();st=0;$('res').style.display='none';});
    inp.addEventListener('input',()=>{
      if(!st)st=performance.now();
      const v=inp.value;
      if(v.length>=cur.length){
        const sec=(performance.now()-st)/1000; let ok=0;for(let i=0;i<cur.length;i++)if(v[i]===cur[i])ok++;
        const acc=Math.round(ok/cur.length*100); let cpm=Math.round(cur.length/sec*60); if(!isFinite(cpm)||cpm>2000)cpm=2000;
        let rank;if(cpm>=300&&acc>=95)rank='達人級！⌨️🔥';else if(cpm>=200)rank='速い！';else if(cpm>=120)rank='なかなか';else rank='これから伸びる';
        $('res').style.display='';$('res').innerHTML='<span style="font-size:24px;color:var(--accent-d)">'+cpm+'</span> 打/分　正確率 '+acc+'%　'+rank;
        SHARE='タイピング速度測定、私は'+cpm+'打/分・正確率'+acc+'%（'+rank+'）でした⌨️ 君は？';
        inp.disabled=true;
      }
    });
'''))

# 13. 記憶力テスト
SIMS.append(dict(id='memory-test', emoji='🧠',
  title='記憶力テスト｜光る順番を何個まで覚えられる？｜シミュラボ',
  desc='光るパネルの順番を覚えて同じ順にタップ。だんだん長くなる並びを何個まで覚えられるか挑戦する記憶力ゲーム型シミュレーター。',
  ogtitle='記憶力テスト｜光る順番を何個まで覚えられる？', ogdesc='光る順番を記憶して再現。何レベルまでいける？',
  h1='記憶力テスト',
  lead='4つのパネルが光る順番を覚えて、同じ順にタップ。正解するたびに1つ長くなります。あなたは何個まで覚えられる？（短期記憶のトレーニングにも）',
  canvas=canvas(420,420,420,'cursor:pointer;'),
  controls=row(btn('start','スタート',True))+resbox(),
  legend='人が一度に覚えられるのは7±2個と言われます（マジカルナンバー）。どこまでいける？',
  article='''    <h2>マジカルナンバー7</h2>
    <p>人間が短期記憶で一度に保持できる情報は「7±2個」が目安とされます（ミラーの法則）。電話番号がこのくらいの桁なのも偶然ではありません。塊（チャンク）にまとめると、もっと覚えられるようになります。</p>
    <h2>よくある質問</h2>'''+faq([('コツはある？','色だけでなく「位置」や「リズム」で覚えると伸びます。'),('データは送信されますか？','いいえ。すべてブラウザ内で動きます。')]),
  share='記憶力テスト、光る順番を覚えるやつ🧠 君は何個まで覚えられる？',
  js='''
    const cv=$('cv'),x=cv.getContext('2d');const W=cv.width,H=cv.height;
    const cols=['#ef4444','#22c55e','#3b82f6','#eab308'],lit=['#fca5a5','#86efac','#93c5fd','#fde68a'];
    let seq=[],input=[],flash=-1,playing=false,level=0;
    function box(i){return [i%2*W/2, Math.floor(i/2)*H/2, W/2, H/2];}
    function draw(){x.fillStyle='#0b1020';x.fillRect(0,0,W,H);for(let i=0;i<4;i++){const b=box(i);x.fillStyle=flash===i?lit[i]:cols[i];x.fillRect(b[0]+6,b[1]+6,b[2]-12,b[3]-12);}}
    function wait(ms){return new Promise(r=>setTimeout(r,ms));}
    async function play(){playing=true;await wait(500);for(const s of seq){flash=s;draw();await wait(420);flash=-1;draw();await wait(180);}playing=false;}
    function next(){seq.push(Math.floor(Math.random()*4));input=[];level=seq.length;play();}
    cv.addEventListener('pointerdown',async e=>{
      if(playing||seq.length===0)return;const p=cpos(cv,e);const i=(p[0]>W/2?1:0)+(p[1]>H/2?2:0);
      flash=i;draw();await wait(150);flash=-1;draw();input.push(i);
      const k=input.length-1;
      if(input[k]!==seq[k]){$('res').style.display='';$('res').innerHTML='ゲームオーバー！　覚えられたのは <span style="font-size:24px;color:var(--accent-d)">'+(seq.length-1)+'</span> 個';SHARE='記憶力テスト、私は'+(seq.length-1)+'個の順番まで覚えられた🧠 君は？';seq=[];return;}
      if(input.length===seq.length){$('res').style.display='';$('res').innerHTML='レベル '+seq.length+' クリア！次へ…';await wait(700);next();}
    });
    $('start').addEventListener('click',()=>{seq=[];input=[];$('res').style.display='none';next();});
    draw();
'''))

# 14. スピログラフ
SIMS.append(dict(id='spirograph', emoji='✏️',
  title='スピログラフ｜歯車で描く幾何学模様シミュレーター｜シミュラボ',
  desc='大きな円の中で小さな円を転がして描く、美しい幾何学模様「スピログラフ」をブラウザで。半径やペン位置を変えて無限の模様を作れる無料シミュレーター。',
  ogtitle='スピログラフ｜歯車で描く幾何学模様', ogdesc='半径やペン位置を変えて無限の幾何学模様を描く。',
  h1='スピログラフ',
  lead='あの定規みたいなおもちゃ「スピログラフ」を再現。円の大きさやペンの位置を変えるだけで、二度と同じものができない美しい模様が描けます。',
  canvas=canvas(520,520,520),
  controls=slider('R','外側の円',60,200,150)+slider('r','内側の円',20,120,52)+slider('d','ペンの位置',10,120,80)+row(btn('draw','この設定で描く',True),btn('rand','ランダム')),
  legend='外円と内円の半径の比で模様の形が決まります。整数比だときれいに閉じます。',
  article='''    <h2>スピログラフの数学</h2>
    <p>大きな円の内側で小さな円を転がし、小円の中の一点が描く軌跡を「ハイポトロコイド」と呼びます。半径の比が模様の対称性（花びらの数）を決め、ペンの位置で形が変わります。比が整数だと模様がぴったり閉じます。</p>
    <h2>よくある質問</h2>'''+faq([('保存できる？','スクリーンショットで保存できます。'),('データは送信されますか？','いいえ。すべてブラウザ内で描画します。')]),
  share='半径を変えるだけで無限の幾何学模様…スピログラフ✏️ ずっと描いてられる。',
  js='''
    const cv=$('cv'),x=cv.getContext('2d');const W=cv.width,H=cv.height,cx=W/2,cy=H/2;let anim=null;
    function draw(){
      if(anim)cancelAnimationFrame(anim);
      const R=+$('R').value,r=+$('r').value,d=+$('d').value;
      x.fillStyle='#0b1020';x.fillRect(0,0,W,H);
      let t=0;const dt=0.06,steps=Math.PI*2*(r/gcd(R,r))*6;let first=true;
      x.lineWidth=1.6;
      function step(){
        for(let k=0;k<40;k++){const px=cx+(R-r)*Math.cos(t)+d*Math.cos((R-r)/r*t);const py=cy+(R-r)*Math.sin(t)-d*Math.sin((R-r)/r*t);
          x.strokeStyle='hsl('+((t*40)%360)+',85%,62%)';if(first){x.beginPath();x.moveTo(px,py);first=false;}else x.lineTo(px,py);x.stroke();x.beginPath();x.moveTo(px,py);t+=dt;}
        if(t<steps)anim=requestAnimationFrame(step);
      } step();
    }
    function gcd(a,b){a=Math.round(a);b=Math.round(b);while(b){[a,b]=[b,a%b];}return a||1;}
    $('draw').addEventListener('click',draw);
    $('rand').addEventListener('click',()=>{$('R').value=80+Math.floor(Math.random()*120);$('r').value=20+Math.floor(Math.random()*90);$('d').value=20+Math.floor(Math.random()*90);syncSliders();draw();});
    draw();
'''))

# 15. 波紋
SIMS.append(dict(id='ripple', emoji='🌊',
  title='波紋シミュレーター｜水面をタップして波の干渉を見る｜シミュラボ',
  desc='水面をタップすると波紋が広がり、複数の波がぶつかって干渉する様子を観察できる無料の波紋シミュレーター。',
  ogtitle='波紋シミュレーター｜水面をタップして波の干渉', ogdesc='タップで波紋が広がり、ぶつかって干渉する様子を観察。',
  h1='波紋シミュレーター',
  lead='静かな水面をタップ（クリック）すると、波紋が広がります。2か所をたたくと、波と波がぶつかって強め合ったり打ち消し合ったり——「干渉」が目で見えます。',
  canvas=canvas(480,360,560,'cursor:pointer;'),
  controls=row(btn('drop','自動でしずくを落とす',True),btn('clear','静める'))+slider('damp','水の粘り',90,99,97),
  legend='波が重なると、山＋山は強く、山＋谷は打ち消し合います（波の干渉）。',
  article='''    <h2>波の干渉とは</h2>
    <p>2つの波が出会うと、高さが足し算されます。山と山が重なれば大きな山に（強め合い）、山と谷が重なれば平ら（打ち消し合い）。音・光・水面——あらゆる波で起きる現象で、ノイズキャンセリングや干渉縞もこの原理です。波動方程式を格子で計算しています。</p>
    <h2>よくある質問</h2>'''+faq([('重い場合は？','少しカクつくときはタップの数を減らしてみてください。'),('データは送信されますか？','いいえ。すべてブラウザ内で計算します。')]),
  share='水面をタップすると波紋が広がってぶつかる…波紋シミュレーター🌊 干渉が目で見える！',
  js='''
    const cv=$('cv'),x=cv.getContext('2d');const W=cv.width,H=cv.height;
    const GW=160,GH=120;let cur=new Float32Array(GW*GH),prev=new Float32Array(GW*GH);
    const off=document.createElement('canvas');off.width=GW;off.height=GH;const ox=off.getContext('2d');const img=ox.createImageData(GW,GH);
    let auto=false,f=0;
    function drop(gx,gy){gx=gx|0;gy=gy|0;for(let dy=-2;dy<=2;dy++)for(let dx=-2;dx<=2;dx++){const X=gx+dx,Y=gy+dy;if(X>0&&X<GW&&Y>0&&Y<GH)prev[Y*GW+X]+=260;}}
    cv.addEventListener('click',e=>{const p=cpos(cv,e);drop(p[0]/W*GW,p[1]/H*GH);});
    cv.addEventListener('touchstart',e=>{e.preventDefault();const p=cpos(cv,e);drop(p[0]/W*GW,p[1]/H*GH);},{passive:false});
    $('drop').addEventListener('click',()=>{auto=!auto;$('drop').textContent=auto?'■ 自動を止める':'自動でしずくを落とす';});
    $('clear').addEventListener('click',()=>{cur.fill(0);prev.fill(0);});
    function loop(){
      f++; if(auto&&f%40===0)drop(Math.random()*GW,Math.random()*GH);
      const damp=+$('damp').value/100;
      for(let y=1;y<GH-1;y++)for(let xx=1;xx<GW-1;xx++){const i=y*GW+xx;
        let v=(prev[i-1]+prev[i+1]+prev[i-GW]+prev[i+GW])/2-cur[i];v*=damp;cur[i]=v;}
      const t=cur;cur=prev;prev=t;
      const d=img.data;for(let i=0;i<GW*GH;i++){const v=prev[i];const c=128+v;d[i*4]=Math.max(0,Math.min(255,c*0.3));d[i*4+1]=Math.max(0,Math.min(255,c*0.6));d[i*4+2]=Math.max(0,Math.min(255,c));d[i*4+3]=255;}
      ox.putImageData(img,0,0);x.imageSmoothingEnabled=true;x.drawImage(off,0,0,W,H);
      requestAnimationFrame(loop);
    } loop(); setTimeout(()=>{drop(GW*0.4,GH*0.5);drop(GW*0.6,GH*0.5);},400);
'''))

def render():
    for s in SIMS:
        d=os.path.join(ROOT,'sims',s['id']); os.makedirs(d,exist_ok=True)
        html=(TPL.replace('__TITLE__',s['title']).replace('__DESC__',s['desc'])
              .replace('__OGTITLE__',s['ogtitle']).replace('__OGDESC__',s['ogdesc'])
              .replace('__CAT__',CAT).replace('__H1__',s['h1']).replace('__LEAD__',s['lead'])
              .replace('__CANVAS__',s.get('canvas','')).replace('__CONTROLS__',s['controls'])
              .replace('__LEGEND__',s['legend']).replace('__ARTICLE__',s['article'])
              .replace('__SHARE__',s['share']).replace('__JS__',s['js']).replace('__ID__',s['id']))
        with open(os.path.join(d,'index.html'),'w',encoding='utf-8') as f: f.write(html)
        print('created sims/'+s['id'])

if __name__=='__main__':
    render()
    print(f'play done. {len(SIMS)} sims.')
