# -*- coding: utf-8 -*-
"""理科の授業向けシミュ：食物連鎖ピラミッド（2026-11-18）
   shokumotsu-rensa … 中3「自然界のつり合い」（生産者・消費者・分解者／数量関係のピラミッド／一時的な増減とつり合いの回復）
   モデル：植物p・草食h・肉食c を基準の数（1,000・100・10）で割った値。分解者の働きNが土の養分（植物の上限）を決める。
     p' = p(1 - p/k) - 0.5ph,  k = 0.3 + 1.7N
     h' = 0.9ph - 0.5h - 0.4hc
     c' = 0.6hc - 0.4c - 0.2c²
     N' = 0.25(目標 - N)  目標＝分解者あり 1 / なし 0.05
   基準(1,1,1)で安定なつり合い。肉食0 → 植物0.56・草食1.44 の新しいつり合い（Pythonで数値計算して確認）。"""
from common import T, N, P, slider, btn, stats

MEXT_CHU = "https://www.mext.go.jp/a_menu/shotou/new-cs/1387016.htm"
def A(url, label): return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, label)

SIMS = []

STAGE = r'''
<style>@media (max-width:560px){.lab-btns .btn{flex:1 1 44%;padding:10px 8px;font-size:13px;}}</style>
<canvas id="cv" class="lab" width="640" height="400" aria-label="食物連鎖のピラミッド（植物・草食動物・肉食動物の数と、分解者による養分の行き来）"></canvas>
<canvas id="gr" class="lab light" width="640" height="210" aria-label="個体数の時間変化のグラフ（基準の数を100%として）"></canvas>
'''

ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
<p>植物（生産者）・草食動物・肉食動物（消費者）の数は、ふつう<strong>植物がいちばん多く、肉食動物ほど少ない</strong>ピラミッドの形になっています。どれかの数が一時的に増えたり減ったりしても、食べる・食べられるの関係を通して、やがて<strong>もとのつり合いにもどる</strong>ことを、ピラミッドの形とグラフの動きで確かめられます。また、ある生物がいなくなったり、分解者が働かなくなったりすると、全体のつり合いが変わったり崩れたりすることもわかります。中学3年「自然と人間」（自然界のつり合い）の学習に使えます。</p>

<h2>授業での使い方</h2>
<ul>
<li><strong>導入</strong>：「▶ 再生」で何も変えずに動かし、数がほとんど変わらない＝つり合っている状態を確認します。ピラミッドの形（植物が多く、肉食動物が少ない）に注目させます。</li>
<li><strong>展開</strong>：「草食動物を半分に」を押す前に、植物と肉食動物の数がどう変わるか予想させ、グラフで確かめます。続けて「肉食動物を0に」「分解者を止める」を試し、もとにもどる場合ともどらない場合を比べます。</li>
<li><strong>まとめ</strong>：グラフの山と谷の順番（草食動物が増える→少し遅れて肉食動物が増える→草食動物が減る…）を言葉で説明させます。人間の活動（外来生物・乱獲・開発など）とつなげて話し合います。</li>
</ul>
<p>生徒への問いの例：</p>
<ol>
<li>草食動物が急に半分になると、植物と肉食動物の数は、そのあとそれぞれどう変わるでしょう。</li>
<li>肉食動物がいなくなると、草食動物は増え続けるでしょうか。植物はどうなるでしょう。</li>
<li>分解者（菌類・細菌類など）がいなくなると、なぜ植物も動物も減ってしまうのでしょう。</li>
</ol>

<h2>しくみ・解説</h2>
<p><strong>食物連鎖と食物網</strong>：生物どうしの「食べる・食べられる」の関係のつながりを<strong>食物連鎖</strong>といいます。実際の自然では、1種類の動物が何種類もの生物を食べるので、つながりは網の目のようになっていて、これを<strong>食物網</strong>といいます。このシミュレーションでは、わかりやすくするために、植物・草食動物・肉食動物の3つのグループにまとめています。</p>
<p><strong>生産者・消費者・分解者</strong>：</p>
''' + T([
    ["生産者", "植物（緑色の植物・植物プランクトン）", "光合成で、無機物（二酸化炭素・水）から有機物（デンプンなど）をつくる"],
    ["消費者", "草食動物・肉食動物", "ほかの生物を食べて、有機物をとり入れる"],
    ["分解者", "菌類（カビ・キノコ）・細菌類、ミミズ・ダンゴムシなどの土の中の小動物", "死がいやふんなどの有機物を、無機物に分解する（分解者も消費者の一部）"],
], ["役割", "おもな生物", "はたらき"]) + '''
<p><strong>数量のピラミッド</strong>：食べられる側の生物は、食べる側よりも数が多いのがふつうです。そのため、生物の数（または量）を積み上げると、植物を底辺とするピラミッドの形になります。このシミュレーションでは、つり合っているときの数を、植物1,000・草食動物100・肉食動物10として表示しています（数は説明のための目安です）。</p>
<p><strong>つり合いがもどるしくみ</strong>：たとえば草食動物が減ると、①食べられる植物は増え、②えさが減った肉食動物は減ります。③すると草食動物は、えさが多く・天敵が少ない状態になるので増えはじめ、④やがて植物は減り、肉食動物は増えて、もとの数の近くにもどります。グラフでは、数が上下にゆれながら、だんだんもとの線（100%）に近づいていきます。</p>
''' + P("つり合いがもどるのは、一時的な増減の場合です。ある生物が完全にいなくなる・外から別の生物が入ってくる・土の養分がなくなるなど、大きな変化があると、もとの数にはもどらず、新しいつり合いになったり、全体が崩れたりします。") + '''
<p><strong>分解者と物質の循環</strong>：分解者は、死がいやふんにふくまれる有機物を、二酸化炭素や水、窒素をふくむ物質などの無機物に分解します。植物はそれを根から吸収したり、光合成に使ったりします。画面の下の土の部分では、死がい・ふんが土に落ち（茶色のつぶ）、分解者のはたらきで養分になって植物にもどる（緑のつぶ）ようすを表しています。「分解者を止める」と養分がもどらなくなり、植物が育つ上限が下がって、植物を食べる動物から順に減っていきます。</p>
''' + T([
    ["草食動物を半分に", "植物が増え、肉食動物が減る → 草食動物が増えもどる", "ゆれながら、もとのつり合いにもどる"],
    ["草食動物を2倍に", "植物が減り、肉食動物が増える → 草食動物が減る", "ゆれながら、もとのつり合いにもどる"],
    ["植物を半分に（日照り）", "草食動物が減り、そのあと肉食動物が減る", "もとのつり合いにもどる"],
    ["肉食動物を0に", "草食動物が増え、植物が減る", "もとにはもどらない（草食動物が約1.4倍・植物が約0.6倍の新しいつり合い）"],
    ["草食動物を0に", "えさがなくなった肉食動物もいなくなる。植物は増える", "崩れる（動物がいなくなる）"],
    ["分解者を止める", "養分が減って植物が減り、草食動物・肉食動物も減る", "崩れる"],
], ["操作", "そのあとの変化", "結果"]) + N("このシミュレーションは、生物の数の増え方・減り方を簡単な式（ロトカ・ヴォルテラ型の式に、植物の育つ上限と肉食動物どうしの競争を加えたもの）で計算した模型です。実際の自然では、季節・天気・病気・生物の移動などが重なるので、グラフのようにきれいにはもどりません。1目盛りの「年」も目安です。") + '''

<h2>参考</h2>
<ul class="seo-refs">
<li>''' + A(MEXT_CHU, "文部科学省「中学校学習指導要領（平成29年告示）解説 理科編」") + ''' 第2分野（7）自然と人間 ア（ｱ）生物と環境「自然界のつり合い」</li>
<li>中学校理科の教科書（3年）「自然界のつり合い」「生物どうしのつながり」「微生物のはたらき」の単元</li>
<li>国立環境研究所「侵入生物データベース」（外来生物が生態系に与える影響の例）</li>
</ul>
'''

FAQS = [
    ("食物連鎖のピラミッドで、上の生物ほど数が少ないのはなぜですか？",
     "食べる動物は、生きていくために自分よりたくさんの量の生物を食べる必要があり、食べた有機物の多くは呼吸などで使われて、体をつくるのに回るのは一部だけだからです。そのため、食べられる側（下の段）の生物ほど数や量が多くなり、ピラミッドの形になります。"),
    ("草食動物が急に減ると、植物と肉食動物はどうなりますか？",
     "食べられる量が減った植物は一時的に増え、えさが減った肉食動物は少し遅れて減ります。すると草食動物は増えやすくなるので、しだいに数がもどり、植物と肉食動物の数も、もとのつり合いの近くにもどっていきます。"),
    ("肉食動物がいなくなると、草食動物はずっと増え続けますか？",
     "増え続けることはありません。草食動物が増えると、えさの植物が減って、草食動物も増えにくくなるからです。このシミュレーションでは、草食動物が約1.4倍、植物が約0.6倍のところで新しいつり合いになります。実際の自然では、植物を食べつくして草食動物が大きく減ってしまうこともあります。"),
    ("分解者がいないとどうなりますか？",
     "死がいやふんなどの有機物が分解されず、植物が使う無機物（養分）が土にもどらなくなります。植物が育ちにくくなり、植物を食べる草食動物、さらに肉食動物も減って、生態系全体のつり合いが崩れます。"),
    ("分解者にはどんな生物がいますか？",
     "カビやキノコなどの菌類、乳酸菌や大腸菌などの細菌類が代表です。ミミズやダンゴムシ、トビムシなど、落ち葉や死がいを食べる土の中の小動物も、分解者のはたらきをしています（これらは消費者でもあります）。"),
]

JS = r'''
const cv=$('cv'), gr=$('gr');
const dpr=Math.min(2,window.devicePixelRatio||1);
const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
const GW=gr.width,GH=gr.height; gr.width=GW*dpr; gr.height=GH*dpr; const g=gr.getContext('2d'); g.setTransform(dpr,0,0,dpr,0,0);
const BASE=[1000,100,10], NAMES=['植物','草食動物','肉食動物'], COL=['#16a34a','#ea580c','#dc2626'], EM=['🌿','🐇','🦊'];
const F='"Hiragino Kaku Gothic ProN","Yu Gothic","Meiryo",sans-serif';
let s, hist, events, playing=true, flash=0, lastEv='', parts=[];
function reset(){ s={p:1,h:1,c:1,N:1,dec:true,t:0}; hist=[{t:0,p:1,h:1,c:1}]; events=[]; lastEv=''; flash=0; parts=[]; upd(); }
function step(dt){
  const tgt=s.dec?1:0.05; s.N+=(tgt-s.N)*0.25*dt;
  const k=0.3+1.7*s.N, p=s.p,h=s.h,c=s.c;
  const dp=p*(1-p/k)-0.5*p*h, dh=0.9*p*h-0.5*h-0.4*h*c, dc=0.6*h*c-0.4*c-0.2*c*c;
  s.p=Math.max(0,p+dp*dt); s.h=Math.max(0,h+dh*dt); s.c=Math.max(0,c+dc*dt); s.t+=dt;
  if(s.c*10<0.3) s.c=0; if(s.h*100<0.3) s.h=0; if(s.p*1000<0.5) s.p=0;   // 1匹（1本）を切ったらいなくなる
}
function ev(label, fn){ fn(); events.push({t:s.t,label}); lastEv=label; flash=1; if(!playing){ playing=true; $('play').textContent='⏸ 一時停止'; } upd(); }
$('hHalf').addEventListener('click',()=>ev('草食動物を半分に',()=>{s.h*=0.5;}));
$('hDouble').addEventListener('click',()=>ev('草食動物を2倍に',()=>{s.h=Math.max(s.h*2,0.05);}));
$('pHalf').addEventListener('click',()=>ev('植物を半分に（日照り）',()=>{s.p*=0.5;}));
$('cZero').addEventListener('click',()=>ev('肉食動物を0に',()=>{s.c=0;}));
$('hZero').addEventListener('click',()=>ev('草食動物を0に',()=>{s.h=0;}));
$('dec').addEventListener('click',()=>ev(s.dec?'分解者を止める':'分解者をもどす',()=>{s.dec=!s.dec; $('dec').textContent=s.dec?'🍄 分解者を止める':'🍄 分解者をもどす';}));
$('play').addEventListener('click',()=>{ playing=!playing; $('play').textContent=playing?'⏸ 一時停止':'▶ 再生'; });
$('reset').addEventListener('click',()=>{ reset(); $('dec').textContent='🍄 分解者を止める'; });
function state(){
  const ext=[]; if(s.p===0)ext.push('植物'); if(s.h===0)ext.push('草食動物'); if(s.c===0)ext.push('肉食動物');
  const r=hist.slice(-40), sp=r.length<2?0:Math.max(...['p','h','c'].map(k=>Math.max(...r.map(o=>o[k]))-Math.min(...r.map(o=>o[k]))));
  if(!s.dec && s.N<0.5) return ['崩れていく（養分がもどらない）','bad'];
  if(ext.length>=2 || (ext.length===1 && ext[0]!=='肉食動物')) return ['崩れた（'+ext.join('・')+'がいない）','bad'];
  if(sp>0.03) return ['ゆらいでいる','mid'];
  if(Math.abs(s.p-1)<0.03&&Math.abs(s.h-1)<0.03&&Math.abs(s.c-1)<0.03) return ['もとのつり合い','ok'];
  return ['新しいつり合い'+(ext.length?'（'+ext[0]+'なし）':''),'mid'];
}
function upd(){
  setStat('sP',num(s.p*1000)); setStat('sH',num(s.h*100)); setStat('sC',num(s.c*10));
  setStat('sT',Math.floor(s.t)+' 年'); const st=state(); setStat('sSt',st[0]);
  const f=v=>(v).toFixed(1)+'倍';
  setShare(lastEv ? '【食物連鎖】「'+lastEv+'」→ '+Math.floor(s.t)+'年後、植物'+f(s.p)+'・草食動物'+f(s.h)+'・肉食動物'+f(s.c)+'（'+st[0]+'）｜シミュラボ'
                  : '【食物連鎖】植物1,000・草食動物100・肉食動物10の数のピラミッドが、食べる・食べられるの関係でつり合っている｜シミュラボ');
}
// ---- 描画：ピラミッド ----
function rr(c,x,y,w,h,r){ c.beginPath(); if(c.roundRect) c.roundRect(x,y,w,h,r); else c.rect(x,y,w,h); }
const EQW=[360,230,110], TH=62, CX=230, GROUND=300;
function tierX(i,v){ const w=Math.max(4,EQW[i]*Math.min(v,1.9)); return [CX-w/2,w]; }
function draw(time){
  const T=time/1000;
  // 空と土
  const sky=ctx.createLinearGradient(0,0,0,GROUND); sky.addColorStop(0,'#bae6fd'); sky.addColorStop(1,'#f0f9ff'); ctx.fillStyle=sky; ctx.fillRect(0,0,W,GROUND);
  const soilA=0.35+0.65*s.N; ctx.fillStyle='rgb('+Math.round(120-30*soilA)+','+Math.round(85+15*soilA)+','+Math.round(50)+')'; ctx.fillRect(0,GROUND,W,H-GROUND);
  ctx.fillStyle='rgba(255,255,255,.75)'; ctx.font='800 12px '+F; ctx.textAlign='left'; ctx.fillText('土（養分 '+Math.round(s.N*100)+'%）',10,GROUND+18);
  // 分解者
  const decA=s.dec?1:Math.max(0.15,s.N);
  ctx.globalAlpha=decA; ctx.font='22px '+F; ['🍄','🦠','🪱','🍄','🦠'].forEach((e,i)=>{ ctx.fillText(e,30+i*80+Math.sin(T*1.5+i)*3,GROUND+60+ (i%2)*18); }); ctx.globalAlpha=1;
  ctx.font='700 11px '+F; ctx.fillStyle='#fef3c7'; ctx.fillText(s.dec?'分解者（菌類・細菌類・ミミズなど）が働いている':'分解者が働いていない（死がい・ふんが分解されない）',10,H-10);
  // 養分のつぶ
  if(playing && Math.random()<0.5){
    const lvl=Math.floor(Math.random()*3), v=[s.p,s.h,s.c][lvl];
    if(v>0.02){ const [x,w]=tierX(lvl,v); parts.push({x:x+Math.random()*w,y:GROUND-lvl*TH-TH/2,vy:1.2,k:'down',life:1}); }
    if(s.N>0.2 && s.dec && Math.random()<0.7) parts.push({x:20+Math.random()*400,y:H-30,vy:-1.1,k:'up',life:1});
  }
  parts.forEach(q=>{ q.y+=q.vy*(q.k==='down'?1.4:1); if(q.k==='down'&&q.y>GROUND+40) q.life=0; if(q.k==='up'&&q.y<GROUND-8) q.life=0;
    ctx.fillStyle=q.k==='down'?'rgba(120,53,15,.85)':'rgba(74,222,128,.95)'; ctx.beginPath(); ctx.arc(q.x,q.y,q.k==='down'?2.6:2.2,0,7); ctx.fill(); });
  parts=parts.filter(q=>q.life>0).slice(-160);
  // ピラミッド
  [s.p,s.h,s.c].forEach((v,i)=>{
    const y=GROUND-(i+1)*TH, [x,w]=tierX(i,v);
    ctx.save(); if(flash>0) ctx.translate(Math.sin(time/30)*4*flash,0);
    // 基準の枠
    const [bx,bw]=tierX(i,1); ctx.setLineDash([5,4]); ctx.strokeStyle='rgba(15,23,42,.35)'; ctx.lineWidth=1.2; rr(ctx,bx,y+3,bw,TH-6,8); ctx.stroke(); ctx.setLineDash([]);
    if(v>0){ rr(ctx,x,y+3,w,TH-6,8); ctx.fillStyle=COL[i]+(v>1.05||v<0.95?'':'')+''; ctx.globalAlpha=.88; ctx.fill(); ctx.globalAlpha=1;
      const n=Math.max(1,Math.round(Math.min(v,1.9)*[9,6,3][i])); ctx.font=(i===0?20:24)+'px '+F; ctx.textAlign='center';
      for(let j=0;j<n;j++){ const ex=x+w*(j+.5)/n, ey=y+TH/2+9+Math.sin(T*2+j+i)*2; if(w/n>14) ctx.fillText(EM[i],ex,ey); } }
    else { ctx.font='800 13px '+F; ctx.textAlign='center'; ctx.fillStyle='#475569'; ctx.fillText(NAMES[i]+'がいない',CX,y+TH/2+5); }
    ctx.restore();
  });
  // 右の説明
  const RX=470; ctx.textAlign='left';
  [2,1,0].forEach((i,k)=>{ const y=GROUND-(i+1)*TH+TH/2; const v=[s.p,s.h,s.c][i];
    ctx.font='800 13px '+F; ctx.fillStyle=COL[i]; ctx.fillText(EM[i]+' '+NAMES[i],RX,y-6);
    ctx.font='900 18px '+F; ctx.fillStyle='#0f172a'; ctx.fillText(num(v*BASE[i]),RX,y+15);
    ctx.font='700 11px '+F; ctx.fillStyle=v===0?'#475569':v>1.03?'#b91c1c':v<0.97?'#1d4ed8':'#475569'; ctx.fillText(v===0?'いなくなった':v>1.03?'▲ 増えている':v<0.97?'▼ 減っている':'つり合いの数',RX+64,y+14);
    if(i>0){ ctx.strokeStyle='#64748b'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.moveTo(RX-12,y+TH-12); ctx.lineTo(RX-12,y+12); ctx.stroke(); ctx.beginPath(); ctx.moveTo(RX-16,y+18); ctx.lineTo(RX-12,y+10); ctx.lineTo(RX-8,y+18); ctx.stroke(); } });
  ctx.font='700 10.5px '+F; ctx.fillStyle='#475569'; ctx.fillText('↑ 食べられる → 食べる',RX-18,20);
  ctx.fillStyle='#0f172a'; ctx.font='800 13px '+F; ctx.fillText(Math.floor(s.t)+' 年目',10,22);
  const st=state(); ctx.font='800 13px '+F; ctx.fillStyle=st[1]==='ok'?'#15803d':st[1]==='bad'?'#b91c1c':'#b45309'; ctx.fillText(st[0],10,42);
  ctx.font='700 10.5px '+F; ctx.fillStyle='#64748b'; ctx.fillText('点線の枠＝つり合いのときの数',10,60);
  flash=Math.max(0,flash-0.03);
}
function drawGraph(){
  g.clearRect(0,0,GW,GH); const L=44,R=GW-12,TOP=14,B=GH-26, span=60, t1=Math.max(span,s.t), t0=t1-span;
  const X=t=>L+(t-t0)/span*(R-L), Y=v=>B-Math.min(v,2)/2*(B-TOP);
  g.strokeStyle='#e2e8f0'; g.lineWidth=1; g.font='700 10px '+F; g.fillStyle='#64748b'; g.textAlign='right';
  [0,0.5,1,1.5,2].forEach(v=>{ g.beginPath(); g.moveTo(L,Y(v)); g.lineTo(R,Y(v)); g.stroke(); g.fillText(Math.round(v*100)+'%',L-4,Y(v)+3); });
  g.setLineDash([5,4]); g.strokeStyle='#94a3b8'; g.beginPath(); g.moveTo(L,Y(1)); g.lineTo(R,Y(1)); g.stroke(); g.setLineDash([]);
  g.textAlign='center'; for(let t=Math.ceil(t0/10)*10;t<=t1;t+=10) g.fillText(t+'年',X(t),GH-10);
  events.forEach(e=>{ if(e.t<t0) return; g.strokeStyle='rgba(15,23,42,.35)'; g.beginPath(); g.moveTo(X(e.t),TOP); g.lineTo(X(e.t),B); g.stroke(); g.fillStyle='#334155'; g.textAlign='left'; g.font='700 10px '+F; g.fillText(e.label,Math.min(X(e.t)+3,R-110),TOP+10); });
  ['p','h','c'].forEach((k,i)=>{ g.strokeStyle=COL[i]; g.lineWidth=2.4; g.beginPath(); let on=false; hist.forEach(o=>{ if(o.t<t0) return; const x=X(o.t),y=Y(o[k]); on?g.lineTo(x,y):g.moveTo(x,y); on=true; }); g.stroke(); });
  g.textAlign='left'; g.font='800 11px '+F; NAMES.forEach((n,i)=>{ g.fillStyle=COL[i]; g.fillRect(L+8+i*96,TOP+20,12,3); g.fillText(n,L+24+i*96,TOP+25); });
  g.fillStyle='#64748b'; g.font='700 10px '+F; g.textAlign='right'; g.fillText('つり合いの数＝100%',R,TOP+25);
}
let prev=performance.now(), acc=0;
function loop(now){
  const dtR=Math.min(0.05,(now-prev)/1000); prev=now;
  if(playing){ const sp=+$('speed').value; acc+=dtR*sp; while(acc>0.02){ step(0.02); acc-=0.02; if(s.t-hist[hist.length-1].t>=0.25) hist.push({t:s.t,p:s.p,h:s.h,c:s.c}); } if(hist.length>2000) hist=hist.slice(-1200); }
  draw(now); drawGraph(); if(Math.floor(now/250)!==Math.floor((now-dtR*1000)/250)) upd();
  requestAnimationFrame(loop);
}
reset(); requestAnimationFrame(loop);
'''

SIMS.append(dict(
    slug="shokumotsu-rensa", cat="rika", emoji="🐇", score=80,
    title="食物連鎖ピラミッドのシミュレーター（自然界のつり合い・生産者・消費者・分解者）",
    title_tag="食物連鎖のピラミッド シミュレーター｜草食動物が減ると？自然界のつり合いと分解者（中3理科）",
    meta_desc="植物・草食動物・肉食動物の数のピラミッドが、食べる・食べられるの関係で増えたり減ったりするシミュレーター。草食動物を半分にする・肉食動物をいなくする・分解者を止めると、数がゆれながらもとのつり合いにもどるのか、崩れるのかをグラフで確かめられる。中学3年「自然界のつり合い」向け。",
    og_title="食物連鎖ピラミッドのシミュレーター｜草食動物が減ると、植物と肉食動物は？",
    og_desc="草食動物を半分にすると、植物が増え肉食動物が減り、ゆれながらもとのつり合いへ。肉食動物を0にすると新しいつり合いに。分解者を止めると全体が崩れる。",
    card_desc="草食動物を半分に、肉食動物を0に。数のピラミッドがゆれて、もとにもどるか崩れるかをグラフで見る。",
    lead="植物・草食動物・肉食動物の数が、食べる・食べられるの関係で増えたり減ったりします。下のボタンで「草食動物を半分に」「肉食動物を0に」「分解者を止める」などの出来事を起こすと、ピラミッドの形がゆがみ、グラフで数がゆれながら、もとのつり合いにもどるのか、新しいつり合いになるのか、崩れるのかを確かめられます。",
    model="中3 自然界のつり合い（食物連鎖・生産者・消費者・分解者）",
    level="中学3年（小学6年「生物と環境」の発展にも）",
    unit="中学校 第2分野（7）自然と人間 ア（ｱ）生物と環境 ㋐自然界のつり合い",
    canvas=STAGE,
    controls=slider("speed", "進む速さ", 1, 8, 3, 1, "{v} 年/秒"),
    buttons=(btn("hHalf", "🐇 草食動物を半分に") + btn("hDouble", "🐇 草食動物を2倍に") + btn("pHalf", "🌿 植物を半分に（日照り）")
             + btn("cZero", "🦊 肉食動物を0に") + btn("hZero", "🐇 草食動物を0に") + btn("dec", "🍄 分解者を止める")
             + btn("play", "⏸ 一時停止", True) + btn("reset", "↺ 最初から")),
    stats=stats([("sP", "🌿 植物", False), ("sH", "🐇 草食動物", False), ("sC", "🦊 肉食動物", False), ("sT", "経過", False), ("sSt", "いまの状態", True)]),
    legend="数は、つり合っているときを植物1,000・草食動物100・肉食動物10とした目安です。土の中の茶色のつぶ＝死がい・ふん、緑のつぶ＝分解者がつくった養分。グラフはつり合いのときの数を100%として表しています。",
    article=ARTICLE, faqs=FAQS,
    rel=[("lotka-volterra", "🐰", "キツネとウサギ 増減シミュレーター"),
         ("shinka-sim", "🧬", "進化シミュレーター"),
         ("kougousei", "🍃", "光合成と呼吸のシミュレーター（気体の出入り・BTB溶液・ヨウ素液・蒸散）"),
         ("diffusion", "🫧", "拡散シミュレーター")],
    js=JS,
))
