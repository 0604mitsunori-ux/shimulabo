# -*- coding: utf-8 -*-
"""理科の授業向け：粒子（状態変化）と遺伝（メンデルの交配実験）
   joutai-henka … 小4「金属，水，空気と温度」／中1「状態変化」（第1分野（2）身の回りの物質）
   mendel-iden  … 中3「遺伝の規則性と遺伝子」（第2分野（5）生命の連続性）"""
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

def NW(t): return '<span style="white-space:nowrap">%s</span>' % t   # 表の短い列を折り返さない

MEXT = ('<a href="https://www.mext.go.jp/a_menu/shotou/new-cs/1384661.htm" target="_blank" rel="noopener">'
        '文部科学省「平成29・30・31年改訂学習指導要領（本文、解説）」</a>')

# ============================================================ 1 状態変化と粒子
JOUTAI_ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
<p>物質は温度によって<b>固体・液体・気体</b>とすがたを変えます（状態変化）。このとき変わるのは<b>粒子の並び方・間隔・動き</b>で、粒子の数（＝質量）は変わりません。純粋な物質は、とけている間（融点）と沸騰している間（沸点）は、加熱を続けても温度が一定になります。水は例外で、氷になると体積が約1.1倍に増えます。</p>
''' + N('<b>対応する単元</b>：小学4年「金属，水，空気と温度」（水は温度によって水蒸気や氷に変わること、水が氷になると体積が増えること）／中学1年 第1分野（2）身の回りの物質「状態変化」（状態変化と熱、物質の融点と沸点）。中学校の学習指導要領では、状態変化を粒子のモデルと関連付けて扱い、粒子の運動にも触れることとされています。') + '''
<h2>授業での使い方</h2>
<h3>導入：グラフの形を予想する</h3>
<p>物質を「水」にして「⏮ 固体にもどす」を押し、−40℃の氷から始めます。「同じ火力で温め続けると、温度はどう変わる？」とグラフの形を予想させてから「🔥 加熱する」を押し、0℃と100℃で平らになる様子を確かめます。</p>
<h3>展開：粒子のモデルで説明する</h3>
<p>右のグラフを指でなぞると、その時点の粒子のようすが左に出ます。固体・液体・気体のそれぞれで、粒子の並び方・間隔・動きを、ノートにかいた粒子のモデルと比べさせます。物質をエタノールや窒素に変えて、融点・沸点が物質ごとに決まっていることも確かめます。</p>
<h3>まとめ：体積と質量</h3>
<p>粒子の数（48個）は最後まで変わらないこと、体積（統計欄の「体積（相対）」）は大きく変わることを確認し、「状態変化では体積は変わるが質量は変わらない」とまとめます。小学4年では、水を0℃より下げると氷がピストンを少し押し上げ、体積が増えることを確かめます。</p>
<h3>児童・生徒への問いの例</h3>
<ol>
<li>氷がとけている間は、加熱を続けているのに温度が0℃のまま上がらない。加えた熱は何に使われているのだろう？</li>
<li>エタノールを入れたポリエチレンの袋に熱い湯をかけると、袋が大きくふくらむ。袋の中の粒子の数は増えたのだろうか？質量はどうなる？</li>
<li>水が氷になると体積が増える。冬の寒い日に、水道管が破裂することがあるのはなぜだろう？</li>
</ol>
<h2>しくみ・解説</h2>
<h3>固体・液体・気体と粒子のモデル</h3>
''' + T([[NW("固体"), "規則正しく並んでいる", "その場で細かくふるえている（振動）", "せまい。形も体積も変わりにくい"],
          [NW("液体"), "並び方がくずれ、寄り集まっている", "たがいの位置を入れかえながら動き回る", "固体とあまり変わらない。形は入れ物に合わせて変わる"],
          [NW("気体"), "ばらばらに離れている", "空間を自由に飛び回る", "とても広い。体積は液体の数百〜数千倍（水では約1,700倍）"]],
         [NW("状態"), "粒子の並び方", "粒子の動き", "粒子の間隔と体積"]) + '''
<p>温度が高いほど、粒子の運動は激しくなります。粒子どうしは引き合っていますが、運動が激しくなると結びつきから離れやすくなり、固体→液体→気体と変化します。</p>
<h3>融点・沸点と加熱のグラフ</h3>
<p>純粋な物質を一定の火力で加熱すると、とけ始めてから全部とけ終わるまで（融点）と、沸騰し始めてから全部が気体になるまで（沸点）は、加熱を続けても温度が上がりません。加えた熱が、粒子どうしの結びつきを切って状態を変えることに使われるからです。融点・沸点は物質の種類によって決まっていて、物質の量には関係しません（量が多いと、平らな部分が長くなるだけです）。</p>
''' + T([["水", "0℃", "100℃", "液体"], ["エタノール", "−115℃", "78℃", "液体"], ["窒素", "−210℃", "−196℃", "気体"],
          ["酸素", "−218℃", "−183℃", "気体"], ["水銀", "−39℃", "357℃", "液体"]],
         ["物質", "融点", "沸点", "20℃での状態"]) + '''
<p>中学校の実験でよく使うパルミチン酸の融点は約63℃です（このシミュレーターには入れていません）。水とエタノールのような混合物は、沸騰している間も温度が少しずつ変わり、平らな部分がはっきりしません。この沸点のちがいを使って、みりんや赤ワインからエタノールを取り出すのが蒸留です。</p>
''' + P('グラフの横軸（時間）は、見やすさのために模式的にしています。実際に水1 gを同じ火力で温めると、0℃の氷をとかすのに約334 J、0℃から100℃まで温めるのに約418 J、100℃で全部を水蒸気にするのに約2,257 Jの熱が必要です。沸騰の平らな部分は、0℃→100℃の部分の約5.4倍の長さになります（熱量の計算は高校の物理基礎で学びます）。') + '''
<h3>体積の変化（計算の例）</h3>
<p>水18 g（体積は約18 cm³）を100℃・1気圧の水蒸気にすると、約30.6 L（約30,600 cm³）になります。30,600÷18 ≒ 1,700 なので、<b>水が水蒸気になると体積は約1,700倍</b>です。統計欄の「体積（相対）」は、液体のときの体積を1として、気体の部分は1気圧の気体として計算しています。</p>
''' + T([["水", "約1,700倍（100℃）", "—（液体）"], ["エタノール", "約490倍（78℃）", "—（液体）"], ["窒素", "約180倍（−196℃）", "約690倍"],
          ["酸素", "約260倍（−183℃）", "約860倍"], ["水銀", "約3,500倍（357℃）", "—（液体）"]],
         ["物質", "沸点で気体になったとき（液体を1）", "20℃の気体（液体を1）"]) + '''
<h3>水の例外：氷は体積が増える</h3>
<p>水が氷になると、水の粒子がすき間の多い並び方で結びつくため、体積が約1.1倍（正確には約1.09倍）に増えます。同じ質量で体積が大きいので、氷は水に浮きます。ほかの多くの物質は、固体になると体積が数％〜十数％小さくなり、固体は液体に沈みます（例：ろう）。このシミュレーターでも、水を0℃にすると氷が水の上に浮き、ほかの物質では固体が底に沈みます。</p>
<h3>模式的にしている点</h3>
<ul>
<li>粒子の数（48個）と大きさは模式的です。実際の粒子はとても小さく、数もけた違いに多くあります。固体の粒子をつなぐ線は、粒子どうしが結びついていることを表す模式です。</li>
<li>気体の体積は、図では液体の数倍に縮めて描いています。実際の値は統計欄の「体積（相対）」を見てください。気体になったあとは、絶対温度に比例して体積が増えるように描いています（ピストンの中は1気圧のまま）。</li>
<li>水以外の固体の体積は、一律に液体の約0.9倍として表示しています（実際の割合は物質によってちがいます）。液体の体積は、水だけ温度による変化（0℃→100℃で約4％増）を入れ、ほかの物質は一定にしています。</li>
<li>アニメの動きの速さは見やすく調整しています。統計欄の「粒子の動き（相対）」は、0℃のときを1とした粒子の運動の激しさの目安で、絶対温度（℃の値＋273）に比例します。</li>
<li>沸点より低い温度でも、液体の表面からは少しずつ蒸発が起きていますが、このシミュレーターでは省略しています。</li>
</ul>
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「小学校学習指導要領（平成29年告示）」理科 第4学年 A（2）金属，水，空気と温度</li>
<li>文部科学省「中学校学習指導要領（平成29年告示）」理科 第1分野（2）身の回りの物質（ウ）状態変化／「中学校学習指導要領（平成29年告示）解説 理科編」</li>
<li>''' + MEXT + '''</li>
<li>中学校理科の教科書（第1学年）「物質の融点と沸点」の表（融点・沸点の値）</li>
<li>M. Tanaka ほか（2001）Metrologia 38, 301–309（水の密度の式。液体の水の体積の計算に使用）</li>
</ul>
'''

JOUTAI_JS = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const SUBS={
    water:{n:'水',mp:0,bp:100,lo:-40,hi:140,t0:20,c:'#3b82f6',d:'#1e3a8a',ice:true,rho:999.84,M:18.015},
    ethanol:{n:'エタノール',mp:-115,bp:78,lo:-150,hi:120,t0:20,c:'#a855f7',d:'#581c87',ice:false,rho:789.3,M:46.07},
    nitrogen:{n:'窒素',mp:-210,bp:-196,lo:-230,hi:-150,t0:-200,c:'#10b981',d:'#065f46',ice:false,rho:807,M:28.013},
    oxygen:{n:'酸素',mp:-218,bp:-183,lo:-240,hi:-140,t0:-200,c:'#f43f5e',d:'#881337',ice:false,rho:1141,M:31.999},
    mercury:{n:'水銀',mp:-39,bp:357,lo:-80,hi:420,t0:20,c:'#94a3b8',d:'#334155',ice:false,rho:13546,M:200.59}
  };
  // 粒子・容器（座標は W×H=640×420）
  const NP=48, C=12, PR=7, PD=14, X0=96, WC=C*PD+PR, X1=X0+WC, FY=372, YTOP=82, WALLTOP=60, AL=220;
  const ROWN=PD*Math.sqrt(3)/2;            // ふつうの固体（すき間なく並ぶ）
  const ROWI=(1.09*NP*AL/WC-PD)/3;         // 氷：液体の約1.09倍の体積になる行間
  const GX0=356, GX1=628, GY0=52, GY1=350, RUNSEC=24;
  const TX=50, TY0=98, TY1=346;
  let S=SUBS.water, rowH=ROWI, B=[0,0.2,0.4,0.6,0.8,1], prog=0, run=0, traceA=null, last=0, acc=0, simT=0, drag=false;
  let pistY=FY, cur=null, G=null, ns=NP, nl=0, ng=0, lastT=null;
  const PS=[];
  for(let i=0;i<NP;i++){ PS.push({x:X0+PR,y:FY-PR,vx:0,vy:0,ph:'s',out:false,w1:rnd(5,9),w2:rnd(5,9),f1:rnd(0,6.28),f2:rnd(0,6.28),gr:0}); }
  const ord=[]; for(let i=0;i<NP;i++) ord.push(i);
  for(let i=NP-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); const tmp=ord[i]; ord[i]=ord[j]; ord[j]=tmp; }
  ord.forEach(function(pi,r){ PS[pi].gr=r; });
  function fmtT(v){ return String(v).replace('-','−'); }
  function hexA(h,a){ const n=parseInt(h.slice(1),16); return 'rgba('+(n>>16)+','+((n>>8)&255)+','+(n&255)+','+a+')'; }
  // グラフの横軸（模式）：融解0.16・沸騰0.26、残りを温度幅の平方根で配分
  function segs(){ const a=Math.sqrt(S.mp-S.lo), b=Math.sqrt(S.bp-S.mp), c=Math.sqrt(S.hi-S.bp), k=0.58/(a+b+c);
    const w=[a*k,0.16,b*k,0.26,c*k], r=[0]; w.forEach(function(v){ r.push(r[r.length-1]+v); }); r[5]=1; return r; }
  function st(q){ const b=B; let T, m=0, g=0, k;
    if(q<b[1]){ T=S.lo+(S.mp-S.lo)*q/b[1]; k=0; }
    else if(q<b[2]){ T=S.mp; m=(q-b[1])/(b[2]-b[1]); k=1; }
    else if(q<b[3]){ T=S.mp+(S.bp-S.mp)*(q-b[2])/(b[3]-b[2]); m=1; k=2; }
    else if(q<b[4]){ T=S.bp; m=1; g=(q-b[3])/(b[4]-b[3]); k=3; }
    else { T=S.bp+(S.hi-S.bp)*Math.min(1,(q-b[4])/(b[5]-b[4])); m=1; g=1; k=4; }
    return {T:T,m:m,g:g,k:k}; }
  function progOf(T){ const b=B;
    if(T<S.mp) return b[1]*(T-S.lo)/(S.mp-S.lo);
    if(T===S.mp) return (b[1]+b[2])/2;
    if(T<S.bp) return b[2]+(b[3]-b[2])*(T-S.mp)/(S.bp-S.mp);
    if(T===S.bp) return (b[3]+b[4])/2;
    return b[4]+(b[5]-b[4])*(T-S.bp)/(S.hi-S.bp); }
  // 容器の中の積み重なり（固体の行・液体の層・気体の層）
  function geo(T){ const Rf=Math.floor(ns/C), p=ns%C, mm=nl+p;
    const hb=Rf>0?(Rf-1)*rowH+PD:0, hm=mm>0?Math.max(PD,mm*AL/WC):0;
    let lt, lb, bt;
    if(S.ice){ lb=FY; lt=FY-hm; bt=lt-hb; } else { bt=FY-hb; lb=bt; lt=lb-hm; }
    const top=S.ice?bt:lt;
    const full=(FY-YTOP)*(T+273.15)/(S.hi+273.15);
    const hg=ng>0?full*Math.sqrt(ng/NP):0;
    return {lt:lt,lb:lb,bt:bt,top:top,pist:top-hg-(ng>0?0:2)}; }
  function site(k){ const row=Math.floor(k/C), col=k%C; const x=X0+PR+col*PD+(row%2?PR:0);
    const y=S.ice?G.bt+PR+row*rowH:FY-PR-row*rowH; return [x,y]; }
  function vLiq(T){ if(!S.ice) return 1; const t=clamp(T,0,100); const rho=999.97495*(1-(t-3.983035)*(t-3.983035)*(t+301.797)/(522528.9*(t+69.34881))); return 999.84/rho; }
  function vGas(T){ const rg=101325*S.M/1000/(8.314462*(T+273.15)); return S.rho/rg; }
  function vol(s){ const vs=S.ice?1.0907:0.9;
    if(s.k===0) return vs; if(s.k===1) return (1-s.m)*vs+s.m*vLiq(S.mp); if(s.k===2) return vLiq(s.T);
    if(s.k===3) return (1-s.g)*vLiq(S.bp)+s.g*vGas(S.bp); return vGas(s.T); }
  function fmtV(v){ if(v<10) return v.toFixed(2)+'倍'; const e=Math.pow(10,Math.floor(Math.log10(v))-1); return '約'+num(Math.round(v/e)*e)+'倍'; }
  function update(){ cur=st(prog); ns=Math.round((1-cur.m)*NP); ng=Math.round(cur.g*NP); nl=NP-ns-ng; G=geo(cur.T); }
  function place(){ let li=0;
    for(let i=0;i<NP;i++){ const p=PS[i]; p.ph=i<ns?'s':(p.gr<ng?'g':'l'); p.vx=0; p.vy=0;
      if(p.ph==='s'){ const s=site(i); p.x=s[0]; p.y=s[1]; }
      else if(p.ph==='l'){ const r=Math.floor(li/C), c=li%C; p.x=X0+PR+c*PD+(r%2?PR*0.5:0); p.y=G.lb-PR-r*PD*0.95; li++; }
      else { p.x=rnd(X0+PR,X1-PR); p.y=rnd(G.pist+PR,G.top-PR); const a=rnd(0,6.28); p.vx=Math.cos(a)*2; p.vy=Math.sin(a)*2; } }
    pistY=G.pist; }
  function step(){
    simT+=1/60; const T=cur.T;
    const sf=clamp((T-S.lo)/(S.mp-S.lo),0,1), lf=clamp((T-S.mp)/(S.bp-S.mp),0,1), gf=clamp((T-S.bp)/(S.hi-S.bp),0,1);
    const A=0.4+1.6*sf, kick=0.6+0.8*lf, vg=2.1+1.5*gf;
    pistY+=(G.pist-pistY)*0.12;
    for(let i=0;i<NP;i++){ const p=PS[i]; const nph=i<ns?'s':(p.gr<ng?'g':'l');
      if(nph!==p.ph){ if(nph==='g'){ p.vx=rnd(-1,1); p.vy=-rnd(1.6,2.6); } else { p.vx*=0.2; p.vy*=0.2; } p.ph=nph; } }
    for(let i=0;i<NP;i++){ const p=PS[i];
      if(p.ph==='s'){ const s=site(i); const tx=s[0]+A*Math.sin(simT*p.w1+p.f1), ty=s[1]+A*Math.sin(simT*p.w2+p.f2); p.x+=(tx-p.x)*0.3; p.y+=(ty-p.y)*0.3; }
      else if(p.ph==='l'){ p.vx+=(Math.random()-0.5)*kick; p.vy+=(Math.random()-0.5)*kick+0.05; p.vx*=0.86; p.vy*=0.86; p.x+=p.vx; p.y+=p.vy; }
      else { const sp=Math.hypot(p.vx,p.vy)||1, f=1+(vg/sp-1)*0.08; p.vx*=f; p.vy*=f;
        const a=(Math.random()-0.5)*0.2, ca=Math.cos(a), sa=Math.sin(a), vx=p.vx*ca-p.vy*sa; p.vy=p.vx*sa+p.vy*ca; p.vx=vx; p.x+=p.vx; p.y+=p.vy; } }
    for(let i=0;i<NP;i++){ const a=PS[i]; for(let j=i+1;j<NP;j++){ const b=PS[j];
      if(a.ph!=='l'&&b.ph!=='l') continue;
      const dx=b.x-a.x, dy=b.y-a.y, d2=dx*dx+dy*dy; if(d2>=PD*PD) continue;
      const d=Math.sqrt(d2)||0.01, ov=PD-d, nx=dx/d, ny=dy/d;
      if(a.ph==='l'&&b.ph==='l'){ a.x-=nx*ov*0.4; a.y-=ny*ov*0.4; b.x+=nx*ov*0.4; b.y+=ny*ov*0.4;
        const rv=(b.vx-a.vx)*nx+(b.vy-a.vy)*ny; if(rv<0){ a.vx+=rv*nx*0.5; a.vy+=rv*ny*0.5; b.vx-=rv*nx*0.5; b.vy-=rv*ny*0.5; } }
      else if(a.ph==='l'){ if(!(a.out&&b.ph==='s')){ a.x-=nx*ov*0.8; a.y-=ny*ov*0.8; } }
      else { if(!(b.out&&a.ph==='s')){ b.x+=nx*ov*0.8; b.y+=ny*ov*0.8; } } } }
    for(let i=0;i<NP;i++){ const p=PS[i]; if(p.ph==='s') continue;
      if(p.x<X0+PR){ p.x=X0+PR; p.vx=Math.abs(p.vx); } if(p.x>X1-PR){ p.x=X1-PR; p.vx=-Math.abs(p.vx); }
      if(p.ph==='l'){
        p.out=(p.y<G.lt+PR-6)||(p.y>G.lb-PR+6);   // 層の外にいる液体の粒子は、固体をすり抜けて層へもどる
        const bp=G.lb-PR; if(p.y>bp){ const dd=p.y-bp; if(dd>4) p.y-=dd*0.3; else p.y=bp; p.vy=-Math.abs(p.vy)*0.5; }
        const tp=G.lt+PR; if(p.y<tp){ const dd=tp-p.y; if(dd>8){ p.y+=dd*0.12; p.vy=Math.max(p.vy,0); } else { p.vy+=dd*0.2; if(dd>3) p.y=tp-3; } } }
      else { if(p.y<pistY+PR){ p.y=pistY+PR; p.vy=Math.abs(p.vy); }
        const sy=G.top-PR; if(p.y>sy){ if(p.vy>0&&p.y-p.vy<=sy+0.5){ p.y=sy; p.vy=-Math.abs(p.vy); } else { p.vy=Math.min(p.vy,-1.2); } }
        if(p.y>FY-PR){ p.y=FY-PR; p.vy=-Math.abs(p.vy); } } }
  }
  function longLabel(s){ const pm=Math.round(s.m*100), pg=Math.round(s.g*100);
    if(s.k===0) return S.ice?'固体（氷）':'固体';
    if(s.k===1) return run<0?(S.ice?'こおる途中（凝固）':'固体になる途中（凝固）')+' 液体'+pm+'%':'とけている途中（融解） 液体'+pm+'%';
    if(s.k===2) return S.ice?'液体（水）':'液体';
    if(s.k===3) return run<0?'液体にもどる途中（凝縮） 気体'+pg+'%':'ふっとうしている（沸騰） 気体'+pg+'%';
    return S.ice?'気体（水蒸気）':'気体'; }
  const SHORT=['固体','固体＋液体','液体','液体＋気体','気体'], SCOL=['#1d4ed8','#6d28d9','#0e7490','#b45309','#c2410c'];
  function gx(q){ return GX0+q*(GX1-GX0); }
  function gy(T){ return GY1-(T-S.lo)/(S.hi-S.lo)*(GY1-GY0); }
  function pathQ(q0,q1){ const qs=[q0]; for(let i=1;i<5;i++){ if(B[i]>q0&&B[i]<q1) qs.push(B[i]); } qs.push(q1);
    ctx.beginPath(); qs.forEach(function(q,i){ const x=gx(q), y=gy(st(q).T); if(i) ctx.lineTo(x,y); else ctx.moveTo(x,y); }); }
  function thermo(T){ const ty=function(v){ return TY1-(v-S.lo)/(S.hi-S.lo)*(TY1-TY0); };
    ctx.fillStyle='#fff'; ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.rect(TX-5,TY0-4,10,TY1-TY0+12); ctx.fill(); ctx.stroke();
    ctx.fillStyle='#dc2626'; const yT=ty(T); ctx.fillRect(TX-2.5,yT,5,TY1+8-yT); ctx.beginPath(); ctx.arc(TX,TY1+16,9,0,6.283); ctx.fill();
    [[S.mp,'融点'],[S.bp,'沸点']].forEach(function(a){ const y=ty(a[0]); ctx.strokeStyle='#475569'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(TX+5,y); ctx.lineTo(TX+10,y); ctx.stroke();
      ctx.fillStyle='#475569'; ctx.font='11px sans-serif'; ctx.textAlign='right'; ctx.fillText(fmtT(a[0])+'℃',TX-8,y+4); ctx.textAlign='left'; ctx.fillText(a[1],TX+12,y+4); }); }
  function flame(){ const fx=X0+WC/2, fy=FY+8;
    if(run>0){ const fl=1+0.12*Math.sin(simT*20);
      ctx.fillStyle='#f97316'; ctx.beginPath(); ctx.moveTo(fx-15,fy+32); ctx.quadraticCurveTo(fx-17,fy+10,fx,fy-4*fl); ctx.quadraticCurveTo(fx+17,fy+10,fx+15,fy+32); ctx.closePath(); ctx.fill();
      ctx.fillStyle='#fde047'; ctx.beginPath(); ctx.moveTo(fx-7,fy+32); ctx.quadraticCurveTo(fx-8,fy+18,fx,fy+8*fl); ctx.quadraticCurveTo(fx+8,fy+18,fx+7,fy+32); ctx.closePath(); ctx.fill();
      ctx.fillStyle='#c2410c'; ctx.font='bold 12px sans-serif'; ctx.textAlign='left'; ctx.fillText('加熱中',fx+24,fy+24); }
    else if(run<0){ ctx.strokeStyle='#0284c7'; ctx.lineWidth=2.2; const cy=fy+16;
      for(let i=0;i<3;i++){ const a=i*Math.PI/3; ctx.beginPath(); ctx.moveTo(fx-Math.cos(a)*12,cy-Math.sin(a)*12); ctx.lineTo(fx+Math.cos(a)*12,cy+Math.sin(a)*12); ctx.stroke(); }
      ctx.fillStyle='#0369a1'; ctx.font='bold 12px sans-serif'; ctx.textAlign='left'; ctx.fillText('冷却中',fx+24,fy+24); } }
  function drawGraph(){
    ctx.textAlign='left'; ctx.fillStyle='#14181d'; ctx.font='bold 14px sans-serif'; ctx.fillText('加熱したときの温度変化',316,20);
    const tw=ctx.measureText('加熱したときの温度変化').width; ctx.font='11px sans-serif'; ctx.fillStyle='#59616c'; ctx.fillText('（一定の火力・横軸は模式的）',316+tw+4,20);
    const bc=['rgba(59,130,246,.10)','rgba(139,92,246,.09)','rgba(14,165,233,.10)','rgba(245,158,11,.11)','rgba(249,115,22,.12)'];
    for(let i=0;i<5;i++){ ctx.fillStyle=bc[i]; ctx.fillRect(gx(B[i]),GY0,gx(B[i+1])-gx(B[i]),GY1-GY0); }
    const rg=S.hi-S.lo; const stp=[5,10,20,50,100,200].find(function(v){ return v>=rg/9; })||200;
    ctx.font='11px sans-serif'; ctx.textAlign='right';
    for(let v=Math.ceil(S.lo/stp)*stp; v<=S.hi; v+=stp){ const y=gy(v); ctx.strokeStyle='rgba(20,24,29,.08)'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(GX0,y); ctx.lineTo(GX1,y); ctx.stroke(); ctx.fillStyle='#59616c'; ctx.fillText(fmtT(v),GX0-5,y+4); }
    ctx.textAlign='left'; ctx.fillText('温度（℃）',318,42);
    ctx.setLineDash([4,4]); ctx.strokeStyle='#64748b'; ctx.lineWidth=1;
    [S.mp,S.bp].forEach(function(v){ const y=gy(v); ctx.beginPath(); ctx.moveTo(GX0,y); ctx.lineTo(GX1,y); ctx.stroke(); }); ctx.setLineDash([]);
    ctx.font='bold 11px sans-serif'; ctx.fillStyle='#1b4a63'; ctx.fillText('融点 '+fmtT(S.mp)+'℃',GX0+4,gy(S.mp)-5); ctx.fillText('沸点 '+fmtT(S.bp)+'℃',GX0+4,gy(S.bp)-5);
    ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1.2; ctx.beginPath(); ctx.moveTo(GX0,GY0); ctx.lineTo(GX0,GY1); ctx.lineTo(GX1,GY1); ctx.stroke();
    pathQ(0,1); ctx.strokeStyle='#334155'; ctx.lineWidth=2.2; ctx.stroke();
    if(traceA!==null&&Math.abs(traceA-prog)>1e-4){ pathQ(Math.min(traceA,prog),Math.max(traceA,prog)); ctx.strokeStyle='rgba(196,68,43,.85)'; ctx.lineWidth=5; ctx.lineCap='round'; ctx.stroke(); ctx.lineCap='butt'; }
    const mx=gx(prog), my=gy(cur.T); ctx.beginPath(); ctx.arc(mx,my,7,0,6.283); ctx.fillStyle='#c4442b'; ctx.fill(); ctx.lineWidth=2.5; ctx.strokeStyle='#fff'; ctx.stroke();
    const BL=[['固体'],['固体と','液体'],['液体'],['液体と','気体'],['気体']];
    ctx.textAlign='center'; ctx.font='bold 11px sans-serif';
    for(let i=0;i<5;i++){ const x=(gx(B[i])+gx(B[i+1]))/2; ctx.fillStyle=SCOL[i]; BL[i].forEach(function(t,j){ ctx.fillText(t,x,GY1+15+j*13); }); }
    ctx.textAlign='right'; ctx.font='11px sans-serif'; ctx.fillStyle='#59616c'; ctx.fillText('加熱時間 →（グラフを指でなぞれます）',GX1,GY1+46); ctx.textAlign='left'; }
  function draw(){
    ctx.fillStyle='#fff'; ctx.fillRect(0,0,W,H);
    ctx.fillStyle='#f6f8fb'; ctx.fillRect(X0,WALLTOP,WC,FY-WALLTOP);
    if(ng>0){ ctx.fillStyle=hexA(S.c,0.05); ctx.fillRect(X0,pistY,WC,G.top-pistY); }
    if(nl>0){ ctx.fillStyle=hexA(S.c,0.13); ctx.fillRect(X0,G.lt,WC,G.lb-G.lt); }
    for(let i=0;i<NP;i++){ const p=PS[i]; ctx.beginPath(); ctx.arc(p.x,p.y,PR-0.5,0,6.283); ctx.fillStyle=S.c; ctx.fill(); ctx.lineWidth=1; ctx.strokeStyle=S.d; ctx.stroke();
      ctx.fillStyle='rgba(255,255,255,.55)'; ctx.beginPath(); ctx.arc(p.x-2.2,p.y-2.2,1.9,0,6.283); ctx.fill(); }
    // 固体の粒子どうしの結びつき（となりの粒子の中心を線でつなぐ・模式）
    if(ns>1){ ctx.strokeStyle=hexA(S.d,0.6); ctx.lineWidth=1.6; ctx.beginPath();
      for(let k=0;k<ns;k++){ const r=Math.floor(k/C), c=k%C, a=PS[k], nb=[];
        if(c<C-1) nb.push(k+1);
        const c1=(r%2)?c:c-1, c2=(r%2)?c+1:c; if(c1>=0) nb.push((r+1)*C+c1); if(c2<C) nb.push((r+1)*C+c2);
        nb.forEach(function(j){ if(j<ns){ const b=PS[j]; if(Math.hypot(b.x-a.x,b.y-a.y)<PD*1.6){ ctx.moveTo(a.x,a.y); ctx.lineTo(b.x,b.y); } } }); }
      ctx.stroke(); }
    const cx=X0+WC/2;
    ctx.fillStyle='#cbd5e1'; ctx.fillRect(X0,pistY-10,WC,10); ctx.strokeStyle='#64748b'; ctx.lineWidth=1; ctx.strokeRect(X0+0.5,pistY-9.5,WC-1,9);
    ctx.fillStyle='#94a3b8'; ctx.fillRect(cx-3,pistY-24,6,14); ctx.fillStyle='#64748b'; ctx.fillRect(cx-13,pistY-29,26,5);
    ctx.strokeStyle='#64748b'; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(X0-1.5,WALLTOP); ctx.lineTo(X0-1.5,FY+1.5); ctx.lineTo(X1+1.5,FY+1.5); ctx.lineTo(X1+1.5,WALLTOP); ctx.stroke();
    thermo(cur.T); flame();
    ctx.textAlign='left'; ctx.fillStyle='#14181d'; ctx.font='bold 19px sans-serif'; ctx.fillText(S.n+'　'+fmtT(Math.round(cur.T))+'℃',8,24);
    ctx.font='bold 14px sans-serif'; ctx.fillStyle=SCOL[cur.k]; ctx.fillText(longLabel(cur),8,46);
    drawGraph(); }
  let lastKey='';
  function showStats(){ const s=cur, T=Math.round(s.T), sh=SHORT[s.k];
    const mv=((s.T+273.15)/273.15).toFixed(2)+'倍', vv=(s.k===0&&!S.ice)?'約0.9倍':fmtV(vol(s)), key=S.n+T+sh+mv+vv;
    if(key===lastKey) return; lastKey=key;
    setStat('sT',fmtT(T)+'℃'); setStat('sState',sh); setStat('sMove',mv); setStat('sVol',vv);
    setShare('【状態変化】'+S.n+'の融点は'+fmtT(S.mp)+'℃、沸点は'+fmtT(S.bp)+'℃。'+fmtT(T)+'℃では'+sh+'。気体になると体積は液体の'+fmtV(vGas(S.bp))+'に（粒子の数は変わらない）｜シミュラボ'); }
  function syncT(){ const v=Math.round(cur.T); if(v!==lastT){ lastT=v; $('t').value=v; $('tL').textContent=fmtT(v)+'℃'; } }
  function setSub(key){ S=SUBS[key]; rowH=S.ice?ROWI:ROWN; B=segs(); const t=$('t'); t.min=S.lo; t.max=S.hi; t.value=S.t0; lastT=null; run=0; traceA=null; prog=progOf(S.t0); update(); place(); syncT(); }
  function frame(ts){ const dt=last?Math.min(0.05,(ts-last)/1000):1/60; last=ts;
    if(run!==0&&!drag){ prog=clamp(prog+run*dt/RUNSEC,0,1); if((run>0&&prog>=1)||(run<0&&prog<=0)) run=0; }
    update(); syncT();
    acc+=dt; let n=0; while(acc>=1/60&&n<4){ step(); acc-=1/60; n++; } if(n>=4) acc=0;
    draw(); showStats(); requestAnimationFrame(frame); }
  function toProg(e){ const p=cpos(cv,e); return clamp((p[0]/dpr-GX0)/(GX1-GX0),0,1); }
  function inGraph(e){ const p=cpos(cv,e), x=p[0]/dpr, y=p[1]/dpr; return x>=GX0-14&&x<=GX1+10&&y>=GY0-14&&y<=GY1+36; }
  cv.addEventListener('pointerdown',function(e){ if(!inGraph(e)) return; drag=true; run=0; traceA=null; prog=toProg(e); try{ cv.setPointerCapture(e.pointerId); }catch(err){} });
  cv.addEventListener('pointermove',function(e){ if(drag) prog=toProg(e); });
  const endDrag=function(){ drag=false; };
  cv.addEventListener('pointerup',endDrag); cv.addEventListener('pointercancel',endDrag);
  $('t').addEventListener('input',function(){ run=0; traceA=null; prog=progOf(+$('t').value); lastT=null; });
  $('sub').addEventListener('change',function(){ setSub($('sub').value); });
  $('heat').addEventListener('click',function(){ if(prog>=0.999) prog=0; traceA=prog; run=1; });
  $('cool').addEventListener('click',function(){ if(prog<=0.001) prog=1; traceA=prog; run=-1; });
  $('stop').addEventListener('click',function(){ run=0; });
  $('reset').addEventListener('click',function(){ run=0; traceA=null; prog=0; });
  setSub($('sub').value); for(let i=0;i<30;i++) step(); draw(); showStats();
  requestAnimationFrame(frame);
'''

sim(slug="joutai-henka", cat="rika", emoji="🧊", score=82,
    title="状態変化と粒子のシミュレーター（固体・液体・気体）",
    title_tag="状態変化のシミュレーター｜固体・液体・気体の粒子のモデルと融点・沸点のグラフ（小4・中1理科）",
    meta_desc="温度を変えると、粒子の並び方・動き・間隔がどう変わるかを粒子のモデルで表示。水・エタノールなどを加熱したときの、融点・沸点で温度が一定になるグラフも描けます。小4「金属，水，空気と温度」、中1「状態変化」の授業向けの無料シミュレーター。",
    og_title="状態変化と粒子のシミュレーター（固体・液体・気体）",
    og_desc="温度スライダーで固体→液体→気体。粒子の動きと体積の変化、融点・沸点で平らになる加熱のグラフを一画面で確かめられます。",
    card_desc="温度で粒子の並び方と動きが変わる。融点・沸点で温度が一定になる加熱のグラフも描ける。",
    lead="温度を上げ下げすると、粒子の並び方・間隔・動きが変わり、物質は固体・液体・気体とすがたを変えます。「🔥 加熱する」を押すと、融点・沸点で温度が一定になるグラフが描かれます。物質を変えて、融点・沸点のちがいや、水だけが氷になると体積が増えることも確かめられます。",
    model="小4 金属，水，空気と温度／中1 状態変化",
    level="小学4年、中学1年",
    unit="小学校 第4学年 A（2）金属，水，空気と温度／中学校 第1分野（2）身の回りの物質",
    canvas=canvas(640, 420, light=True),
    controls=select("sub", "物質", [("water", "水（融点0℃・沸点100℃）"), ("ethanol", "エタノール（融点−115℃・沸点78℃）"),
                                    ("nitrogen", "窒素（融点−210℃・沸点−196℃）"), ("oxygen", "酸素（融点−218℃・沸点−183℃）"),
                                    ("mercury", "水銀（融点−39℃・沸点357℃）")])
             + slider("t", "温度", -40, 140, 20, 1, "{v}℃"),
    buttons=btn("heat", "🔥 加熱する", True) + btn("cool", "❄️ 冷やす") + btn("stop", "⏸ 止める") + btn("reset", "⏮ 固体にもどす"),
    stats=stats([("sT", "温度", True), ("sState", "状態", False), ("sMove", "粒子の動き（相対）", False), ("sVol", "体積（相対）", False)]),
    legend="左：ピストン付きの容器に入れた物質の粒子（48個・模式図）。線でつながっている粒子が固体です。右：一定の火力で加熱したときの温度変化。グラフを指でなぞると、その時点の粒子のようすが見られます。粒子の動き＝0℃のときを1とした運動の激しさ。体積＝液体を1とした値（気体の体積は、図では縮めて描いています）。",
    article=JOUTAI_ARTICLE,
    faqs=[("融点や沸点で温度が一定になるのはなぜ？", "加えた熱が、粒子どうしの結びつきを切って状態を変えることに使われるからです。全部とけ終わる（全部が気体になる）までは温度が上がらず、状態が変わり終わると再び温度が上がり始めます。これは純粋な物質の性質で、混合物でははっきり一定になりません。"),
          ("水が氷になると体積が増えるのはなぜ？", "氷では、水の粒子がすき間の多い並び方で結びつくため、同じ質量でも体積が約1.1倍になります。そのため氷は水に浮きます。多くの物質は逆に、固体になると体積が小さくなります。"),
          ("状態変化で質量は変わる？", "変わりません。状態が変わっても粒子の数は同じで、変わるのは粒子の並び方と間隔です。体積は変わって質量は変わらないので、密度（1 cm³あたりの質量）は変わります。"),
          ("湯気は気体？", "湯気は気体ではなく、水蒸気が冷やされてできた小さな水の粒（液体）です。水蒸気（気体）は目に見えません。やかんの口のすぐ近くが透明に見えるのは、そこがまだ水蒸気のままだからです。"),
          ("蒸発と沸騰のちがいは？", "蒸発は、沸点より低い温度でも液体の表面から気体になる変化です。沸騰は、沸点で液体の内部からも気体になる変化で、泡がさかんに出ます。水を沸騰させたときの泡の正体は水蒸気です。"),
          ("物質の量を増やすと沸点は変わる？", "変わりません。量を増やすと、沸騰が終わるまでの時間（グラフの平らな部分の長さ）が長くなるだけで、温度は同じです。融点も同じです。そのため、融点や沸点を調べると物質の種類を見分ける手がかりになります。")],
    rel=[("diffusion", "🫧", "拡散シミュレーター"), ("coffee-milk", "☕", "コーヒーにミルクを落とすと"),
         ("sentaku-kawaku", "👕", "洗濯物 乾く時間メーター")],
    js=JOUTAI_JS)


# ============================================================ 2 遺伝の規則性（メンデル）
MENDEL_ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
<p>丸い種子をつくる純系のエンドウ（AA）と、しわのある種子をつくる純系のエンドウ（aa）をかけ合わせると、子（Aa）はすべて丸い種子になります。子どうしをかけ合わせて（自家受粉）できる孫では、丸としわが<b>およそ3：1</b>の割合で現れます。この比は、調べる数が少ないと大きくばらつき、数を増やすほど3：1に近づきます。</p>
''' + N('<b>対応する単元</b>：中学3年 第2分野（5）生命の連続性「遺伝の規則性と遺伝子」。学習指導要領では、交配実験の結果などに基づいて遺伝の規則性を見いだすこととされ、分離の法則を扱います。解説では、コインやカードを使った交配のモデル実験を行い、試行回数と得られる結果との関係に気付かせる例が示されています。') + '''
<h2>授業での使い方</h2>
<h3>導入：しわの種子はどこへ消えた？</h3>
<p>親→子→孫の流れ（キャンバスの左上）を見せ、「子ではしわの種子が1つもないのに、孫で再び現れるのはなぜか」を問いかけます。</p>
<h3>展開：モデル実験とくらべる</h3>
<p>班ごとにコインやカードで交配のモデル実験（例：20回）を行い、結果を記録します。次に、このシミュレーターで孫の数を20個にして「🔁 10回くり返す」を押し、班ごとに結果がばらつくのは当たり前であることを確かめます。そのあと数を100、1,000、10,000と増やし、比が3：1に近づいていく様子をグラフで見ます。</p>
<h3>まとめ：かけ合わせの表で説明する</h3>
<p>かけ合わせの表を使って、AA：Aa：aa＝1：2：1、丸：しわ＝3：1になる理由を説明させます。種子をタップすると遺伝子の組み合わせが見られるので、「見た目が丸でもAAとAaがある」ことも確かめられます。表のマスをタップすると、その組み合わせの種子だけが表示されます。</p>
<h3>生徒への問いの例</h3>
<ol>
<li>子（Aa）はすべて丸なのに、孫にしわの種子が現れるのはなぜだろう？</li>
<li>孫を20個だけ調べたら、丸が18個、しわが2個だった。3：1にならなかったのは、実験の失敗だろうか？</li>
<li>孫の丸い種子のうち、遺伝子の組み合わせがAaのものは、およそ何％だろう？</li>
</ol>
<h2>しくみ・解説</h2>
<h3>用語</h3>
<ul>
<li><b>形質・対立形質</b>：生物の形や性質の特徴を形質といいます。種子の形の「丸」と「しわ」のように、どちらか一方しか現れない形質どうしを対立形質といいます。</li>
<li><b>顕性の形質・潜性の形質</b>：対立形質をもつ純系どうしをかけ合わせたとき、子に現れる形質を顕性の形質（丸）、子に現れない形質を潜性の形質（しわ）といいます。以前は「優性」「劣性」と呼んでいましたが、形質が優れている・劣っているという意味ではないため、日本遺伝学会が2017年に言いかえを提案し、今の教科書では「顕性」「潜性」が使われています。</li>
<li><b>純系</b>：自家受粉をくり返しても、親・子・孫と同じ形質が現れ続ける系統（AA や aa）です。</li>
<li><b>分離の法則</b>：対になっている遺伝子は、生殖細胞（卵細胞・精細胞）がつくられるとき（減数分裂）に分かれて、別々の生殖細胞に入ります。</li>
</ul>
<h3>かけ合わせの表（子 Aa × 子 Aa → 孫）</h3>
''' + T([["A", "AA（丸）", "Aa（丸）"], ["a", "Aa（丸）", "aa（しわ）"]], ["卵細胞＼精細胞", "A", "a"]) + '''
<p>卵細胞も精細胞も、Aをもつものとaをもつものが1：1の割合でつくられるので、4つのマスはどれも同じ確率（1/4）で起こります。そのため AA：Aa：aa＝1：2：1。Aが1つでもあれば丸になるので、丸：しわ＝（1＋2）：1＝<b>3：1</b>です。丸い種子のうちAaは2/3（約67％）、AAは1/3です。</p>
<p><b>計算の例</b>：孫の種子が800個できたとき、しわはおよそ800×1/4＝200個、丸はおよそ600個です。丸600個のうち、AAはおよそ200個、Aaはおよそ400個です。</p>
<h3>数が少ないと、なぜずれるのか</h3>
<p>1つ1つの孫がどの組み合わせになるかは、コインを投げたときの表・裏のように偶然で決まります。そのため、調べる数が少ないと3：1から大きくずれることがあります。孫の数ごとに、しわの数がおよそ95％の確率で入る範囲を計算すると、次のようになります。</p>
''' + T([["20個", "5個", "2〜9個", "1.2：1 〜 9：1"], ["100個", "25個", "17〜34個", "1.9：1 〜 4.9：1"],
          ["1,000個", "250個", "223〜277個", "2.6：1 〜 3.5：1"], ["10,000個", "2,500個", "2,415〜2,585個", "2.9：1 〜 3.1：1"]],
         ["孫の数", "しわの数（理論上）", "しわの数（およそ95％の範囲）", "丸：しわ の範囲"]) + '''
<h3>メンデルの実験の結果</h3>
<p>メンデルは1865年にエンドウの交配実験の結果を発表し、翌年に論文として出版しました。7つの対立形質について、孫の代で次のような結果を得ています。</p>
''' + T([["種子の形", "丸", "しわ", "5,474：1,850", "2.96：1"], ["子葉の色", "黄色", "緑色", "6,022：2,001", "3.01：1"],
          ["種皮の色", "有色", "白色", "705：224", "3.15：1"], ["さやの形", "ふくれ", "くびれ", "882：299", "2.95：1"],
          ["さやの色", "緑色", "黄色", "428：152", "2.82：1"], ["花のつき方", "葉のつけ根", "茎の先端", "651：207", "3.14：1"],
          ["茎の高さ", "高い", "低い", "787：277", "2.84：1"]],
         ["形質", "顕性の形質", "潜性の形質", "孫の数（顕性：潜性）", "比"]) + '''
<p>どの形質もほぼ3：1です。種子の形では、7,324個を調べて丸5,474個・しわ1,850個（2.96：1）でした。このシミュレーターの「📗 メンデルと同じ7,324個」で、同じ数の交配を試せます。グラフの★がメンデルの結果です。</p>
''' + P('卵細胞と精細胞がAとaのどちらをもつかは、それぞれ1/2の確率（乱数）で決めています。ほかの遺伝子の影響や、種子が育たない場合などは考えていません。種子の絵は模式的です。') + '''
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「中学校学習指導要領（平成29年告示）」理科 第2分野（5）生命の連続性（イ）遺伝の規則性と遺伝子／「中学校学習指導要領（平成29年告示）解説 理科編」（交配のモデル実験）</li>
<li>''' + MEXT + '''</li>
<li>日本遺伝学会『遺伝単（遺伝学用語集 対訳付き）』（2017年。顕性・潜性への言いかえ）</li>
<li>G. Mendel（1866）Versuche über Pflanzen-Hybriden（エンドウの交配実験の論文）</li>
<li>中学校理科の教科書（第3学年）「遺伝の規則性と遺伝子」</li>
</ul>
'''

MENDEL_JS = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const NICE=[]; [10,100,1000].forEach(function(d){ [1,1.2,1.5,2,2.5,3,4,5,6,7,8,9].forEach(function(m){ NICE.push(Math.round(d*m)); }); }); NICE.push(10000);
  const SEEDN=64, YMAX=6, ANIM=1.4;
  const CX0=300, CW=160, RY0=72, RH=78, GX0=262, GX1=612, GY0=290, GY1=486, SX0=24, SY0=338, SP=21;
  const GT=['AA','Aa','Aa','aa'];
  let NN=NICE[+$('n').value], trials=[], cur=null, animT=1, last=0, showG=false, hl=null, tip=null, dirty=true, press=false;
  // 孫の代：卵細胞・精細胞がそれぞれ A / a を 1/2 で受けつぐ（c: 0=AA 1=卵A×精a 2=卵a×精A 3=aa）
  function trial(n){ let AA=0, Aa=0, aA=0, aa=0, next=1; const seeds=[], pts=[];
    for(let k=1;k<=n;k++){ const e=Math.random()<0.5, p=Math.random()<0.5; let c;
      if(e&&p){ AA++; c=0; } else if(e){ Aa++; c=1; } else if(p){ aA++; c=2; } else { aa++; c=3; }
      if(seeds.length<SEEDN) seeds.push(c);
      if(k>=next||k===n){ pts.push([k,AA,Aa,aA,aa]); next=k<40?k+1:Math.ceil(k*1.03); } }
    return {n:n,pts:pts,seeds:seeds}; }
  function shownK(t,a){ return a>=1?t.n:Math.max(1,Math.round(Math.pow(t.n,a))); }
  function ptAt(t,k){ let lo=0, hi=t.pts.length-1; while(lo<hi){ const mid=(lo+hi+1)>>1; if(t.pts[mid][0]<=k) lo=mid; else hi=mid-1; } return t.pts[lo]; }
  function seedShape(x,y,r,round,ph){ ctx.beginPath();
    if(round){ ctx.arc(x,y,r,0,6.283); }
    else { for(let i=0;i<=28;i++){ const a=i/28*6.283, rr=r*(0.88+0.12*Math.sin(a*6+ph)), px=x+Math.cos(a)*rr, py=y+Math.sin(a)*rr; if(i) ctx.lineTo(px,py); else ctx.moveTo(px,py); } ctx.closePath(); } }
  function seed(x,y,r,round,ph,alpha){ ctx.save(); ctx.globalAlpha=(alpha==null?1:alpha); seedShape(x,y,r,round,ph||0);
    ctx.fillStyle=round?'#d4e05c':'#b9bf5a'; ctx.fill(); ctx.lineWidth=Math.max(1,r/8); ctx.strokeStyle=round?'#71801c':'#5f6420'; ctx.stroke();
    if(round){ ctx.fillStyle='rgba(255,255,255,.55)'; ctx.beginPath(); ctx.ellipse(x-r*0.35,y-r*0.38,r*0.3,r*0.2,-0.6,0,6.283); ctx.fill(); }
    else { ctx.strokeStyle='rgba(80,84,24,.8)'; ctx.lineWidth=Math.max(0.9,r/11); ctx.beginPath(); ctx.arc(x-r*0.25,y+r*0.05,r*0.45,-1.0,0.9); ctx.stroke(); ctx.beginPath(); ctx.arc(x+r*0.3,y-r*0.1,r*0.35,2.2,4.0); ctx.stroke(); }
    ctx.restore(); }
  function arrow(x,y0,y1,label){ ctx.strokeStyle='#59616c'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(x,y0); ctx.lineTo(x,y1-6); ctx.stroke();
    ctx.fillStyle='#59616c'; ctx.beginPath(); ctx.moveTo(x-6,y1-8); ctx.lineTo(x+6,y1-8); ctx.lineTo(x,y1); ctx.closePath(); ctx.fill();
    ctx.font='11px sans-serif'; ctx.textAlign='left'; ctx.fillText(label,x+10,(y0+y1)/2+4); }
  function lineage(){
    ctx.textAlign='left'; ctx.fillStyle='#14181d'; ctx.font='bold 13px sans-serif'; ctx.fillText('親（純系）',8,20);
    seed(56,48,15,true,0); seed(150,48,15,false,1);
    ctx.font='bold 18px sans-serif'; ctx.textAlign='center'; ctx.fillStyle='#59616c'; ctx.fillText('×',103,54);
    ctx.font='bold 12px sans-serif'; ctx.fillStyle='#14181d'; ctx.fillText('AA（丸）',56,80); ctx.fillText('aa（しわ）',150,80);
    arrow(103,88,116,'受粉');
    ctx.textAlign='left'; ctx.fillStyle='#14181d'; ctx.font='bold 13px sans-serif'; ctx.fillText('子',8,136);
    seed(103,138,15,true,0); ctx.font='bold 12px sans-serif'; ctx.textAlign='center'; ctx.fillText('Aa',103,170);
    ctx.textAlign='left'; ctx.font='12px sans-serif'; ctx.fillStyle='#59616c'; ctx.fillText('すべて丸',126,143);
    arrow(103,178,206,'自家受粉');
    ctx.fillStyle='#14181d'; ctx.font='bold 13px sans-serif'; ctx.textAlign='left'; ctx.fillText('孫',8,226);
    [['AA',true],['Aa',true],['Aa',true],['aa',false]].forEach(function(v,i){ const x=46+i*38; seed(x,236,12,v[1],i); ctx.fillStyle='#14181d'; ctx.font='bold 11px sans-serif'; ctx.textAlign='center'; ctx.fillText(v[0],x,262); });
    ctx.font='bold 13px sans-serif'; ctx.fillStyle='#c4442b'; ctx.textAlign='center'; ctx.fillText('丸：しわ＝3：1（理論）',103,288); ctx.textAlign='left'; }
  function punnett(cnt,k){
    ctx.textAlign='left'; ctx.fillStyle='#14181d'; ctx.font='bold 13px sans-serif'; ctx.fillText('かけ合わせの表（子 Aa × 子 Aa → 孫）',222,20);
    ctx.font='11px sans-serif'; ctx.fillStyle='#59616c'; ctx.textAlign='center'; ctx.fillText('精細胞（花粉）の遺伝子 →',CX0+CW,40);
    ctx.textAlign='left'; ctx.fillText('卵細胞の',228,58); ctx.fillText('遺伝子 ↓',228,70);
    ctx.font='bold 18px sans-serif'; ctx.fillStyle='#14181d'; ctx.textAlign='center';
    ctx.fillText('A',CX0+CW*0.5,66); ctx.fillText('a',CX0+CW*1.5,66); ctx.fillText('A',261,RY0+RH*0.5+6); ctx.fillText('a',261,RY0+RH*1.5+6);
    const tot=k||1;
    for(let r=0;r<2;r++) for(let c=0;c<2;c++){ const code=r*2+c, x=CX0+c*CW, y=RY0+r*RH, g=GT[code], rd=code!==3;
      ctx.fillStyle=(hl===g)?'#fef3c7':'#ffffff'; ctx.fillRect(x,y,CW,RH); ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1; ctx.strokeRect(x+0.5,y+0.5,CW-1,RH-1);
      seed(x+30,y+RH/2,15,rd,code);
      ctx.textAlign='left'; ctx.fillStyle='#14181d'; ctx.font='bold 20px sans-serif'; ctx.fillText(g,x+54,y+34); const gw=ctx.measureText(g).width;
      ctx.font='13px sans-serif'; ctx.fillStyle='#59616c'; ctx.fillText(rd?'（丸）':'（しわ）',x+56+gw,y+34);
      ctx.font='12px sans-serif'; ctx.fillStyle='#1b4a63'; ctx.fillText(num(cnt[code])+'個（'+(cnt[code]/tot*100).toFixed(1)+'%）',x+54,y+58); }
    ctx.textAlign='left'; ctx.font='bold 12px sans-serif'; ctx.fillStyle='#14181d'; ctx.fillText('AA：Aa：aa＝1：2：1　→　丸：しわ＝3：1',222,RY0+2*RH+20); }
  function grid(t,k){ const n=Math.min(SEEDN,k);
    ctx.textAlign='left'; ctx.fillStyle='#14181d'; ctx.font='bold 12px sans-serif';
    ctx.fillText(t.n>SEEDN?'孫の種子（最初の64個）':'孫の種子（'+t.n+'個）',8,322);
    for(let i=0;i<n;i++){ const c=t.seeds[i], x=SX0+(i%8)*SP, y=SY0+Math.floor(i/8)*SP, g=GT[c], a=(hl&&hl!==g)?0.18:1;
      seed(x,y,8,c!==3,i,a);
      if(showG&&a===1){ ctx.fillStyle='#1f2937'; ctx.font='bold 9px sans-serif'; ctx.textAlign='center'; ctx.fillText(g,x,y+3); ctx.textAlign='left'; } }
    ctx.font='11px sans-serif'; ctx.fillStyle='#59616c';
    ctx.fillText(hl?hl+'だけ表示中（マスをもう一度タップで解除）':'種子をタップすると遺伝子が見られます',8,512); }
  function lx(k){ return GX0+Math.log10(k)/4*(GX1-GX0); }
  function ly(r){ return GY1-Math.min(r,YMAX+0.3)/YMAX*(GY1-GY0); }
  function ratio(p){ const R=p[1]+p[2]+p[3], w=p[4]; return w?R/w:YMAX+1; }
  function line(t,ks,col,lw){ ctx.beginPath(); let first=true;
    for(const p of t.pts){ if(p[0]>ks) break; const x=lx(p[0]), y=ly(ratio(p)); if(first){ ctx.moveTo(x,y); first=false; } else ctx.lineTo(x,y); }
    ctx.strokeStyle=col; ctx.lineWidth=lw; ctx.lineJoin='round'; ctx.stroke(); }
  function star(x,y,r,col){ ctx.beginPath(); for(let i=0;i<10;i++){ const a=-Math.PI/2+i*Math.PI/5, rr=(i%2)?r*0.45:r; ctx.lineTo(x+Math.cos(a)*rr,y+Math.sin(a)*rr); } ctx.closePath(); ctx.fillStyle=col; ctx.fill(); }
  function graph(ks){
    ctx.textAlign='left'; ctx.fillStyle='#14181d'; ctx.font='bold 13px sans-serif'; ctx.fillText('孫の数と「丸：しわ」の比',222,274);
    const tw=ctx.measureText('孫の数と「丸：しわ」の比').width; ctx.font='11px sans-serif'; ctx.fillStyle='#59616c'; ctx.fillText('（しわを1としたときの丸）',222+tw+4,274);
    ctx.font='11px sans-serif';
    for(let v=0;v<=YMAX;v++){ const y=ly(v); ctx.strokeStyle=v===0?'#94a3b8':'rgba(20,24,29,.08)'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(GX0,y); ctx.lineTo(GX1,y); ctx.stroke();
      ctx.textAlign='right'; if(v===3){ ctx.fillStyle='#c4442b'; ctx.font='bold 12px sans-serif'; ctx.fillText('3：1',GX0-6,y+4); ctx.font='11px sans-serif'; } else { ctx.fillStyle='#59616c'; ctx.fillText(String(v),GX0-6,y+4); } }
    ctx.textAlign='center'; ['1','10','100','1,000','10,000'].forEach(function(s,i){ const x=GX0+i/4*(GX1-GX0); ctx.strokeStyle='rgba(20,24,29,.08)'; ctx.beginPath(); ctx.moveTo(x,GY0); ctx.lineTo(x,GY1); ctx.stroke(); ctx.fillStyle='#59616c'; ctx.fillText(s,x,GY1+14); });
    ctx.textAlign='right'; ctx.fillText('孫の数（個）→ 目もりは10倍ずつ',GX1+20,GY1+29);
    ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1.2; ctx.beginPath(); ctx.moveTo(GX0,GY0); ctx.lineTo(GX0,GY1); ctx.stroke();
    ctx.setLineDash([6,4]); ctx.strokeStyle='#c4442b'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.moveTo(GX0,ly(3)); ctx.lineTo(GX1,ly(3)); ctx.stroke(); ctx.setLineDash([]);
    ctx.save(); ctx.beginPath(); ctx.rect(GX0,GY0-4,GX1-GX0+2,GY1-GY0+4); ctx.clip();
    trials.forEach(function(t){ if(t!==cur) line(t,t.n,'rgba(100,116,139,.45)',1.3); });
    if(cur) line(cur,ks,'#c4442b',2.4);
    ctx.restore();
    star(lx(7324),ly(5474/1850),7,'#a97a24');
    // 凡例（右上・線と重ならない位置）
    ctx.font='11px sans-serif'; const l2='メンデルの結果 2.96：1（7,324個）', lw2=ctx.measureText(l2).width, LW=Math.max(lw2+26,170), LX=GX1-LW-2, LY=GY0+4;
    ctx.fillStyle='rgba(255,255,255,.92)'; ctx.fillRect(LX-4,LY,LW+6,38);
    ctx.lineWidth=2.4; ctx.strokeStyle='#c4442b'; ctx.beginPath(); ctx.moveTo(LX,LY+10); ctx.lineTo(LX+16,LY+10); ctx.stroke();
    ctx.textAlign='left'; ctx.fillStyle='#14181d'; ctx.fillText('今回',LX+20,LY+14);
    ctx.lineWidth=1.3; ctx.strokeStyle='rgba(100,116,139,.7)'; ctx.beginPath(); ctx.moveTo(LX+56,LY+10); ctx.lineTo(LX+72,LY+10); ctx.stroke();
    ctx.fillText('これまで '+(Math.max(0,trials.length-1))+'回',LX+76,LY+14);
    star(LX+8,LY+28,6,'#a97a24'); ctx.fillStyle='#8a6418'; ctx.fillText(l2,LX+20,LY+32);
    if(cur){ const p=ptAt(cur,ks), r=ratio(p), x=lx(p[0]), y=Math.max(GY0,ly(r)); ctx.beginPath(); ctx.arc(x,y,4,0,6.283); ctx.fillStyle='#c4442b'; ctx.fill();
      const s=p[4]?(r.toFixed(2)+'：1'):'しわ0個'; ctx.font='bold 12px sans-serif'; const right=x>GX1-70; ctx.textAlign=right?'right':'left';
      const tx=right?x-8:x+8, ty=Math.max(GY0+26,Math.min(GY1-6,y-8)); ctx.lineWidth=3; ctx.strokeStyle='#fff'; ctx.strokeText(s,tx,ty); ctx.fillStyle='#c4442b'; ctx.fillText(s,tx,ty); }
    ctx.textAlign='left'; }
  function drawTip(k){ if(!tip||!cur) return; const age=performance.now()-tip.t; if(age>2600){ tip=null; return; }
    const i=tip.i; if(i>=Math.min(SEEDN,k)) return;
    const c=cur.seeds[i], x=SX0+(i%8)*SP, y=SY0+Math.floor(i/8)*SP, g=GT[c], egg=(c<2)?'A':'a', pol=(c===0||c===2)?'A':'a';
    const t1=g+'（'+(c===3?'しわ':'丸')+'）', t2='卵細胞 '+egg+' ＋ 精細胞 '+pol;
    ctx.font='11px sans-serif'; const w2=ctx.measureText(t2).width; ctx.font='bold 13px sans-serif'; const w1=ctx.measureText(t1).width;
    const bw=Math.max(w1,w2)+16, bh=40; let bx=x+12, by=y-48; if(bx+bw>W-4) bx=x-12-bw; if(by<4) by=y+12;
    ctx.globalAlpha=Math.min(1,(2600-age)/400); ctx.fillStyle='rgba(20,24,29,.92)'; ctx.fillRect(bx,by,bw,bh);
    ctx.fillStyle='#fff'; ctx.textAlign='left'; ctx.fillText(t1,bx+8,by+17); ctx.font='11px sans-serif'; ctx.fillText(t2,bx+8,by+33);
    ctx.strokeStyle='#c4442b'; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(x,y,10,0,6.283); ctx.stroke(); ctx.globalAlpha=1; }
  function showStats(p){ const k=p[0], R=p[1]+p[2]+p[3], w=p[4], rs=w?(R/w).toFixed(2)+'：1':num(R)+'：0';
    const gs=num(p[1])+'：'+num(p[2]+p[3])+'：'+num(p[4]);
    setStat('sR',num(R)+'個'); setStat('sW',num(w)+'個'); setStat('sRatio',rs); setStat('sG',gs); $('sG').style.fontSize=gs.length>12?'13px':'16px';
    setShare('【遺伝の規則性】エンドウの孫を'+num(k)+'個つくったら 丸'+num(R)+'個：しわ'+num(w)+'個＝'+rs+'（理論は3：1）。数を増やすほど3：1に近づく｜シミュラボ'); }
  function draw(){ ctx.fillStyle='#fff'; ctx.fillRect(0,0,W,H);
    const ks=cur?shownK(cur,animT):1, p=cur?ptAt(cur,ks):[0,0,0,0,0], k=p[0];
    lineage(); punnett([p[1],p[2],p[3],p[4]],k); if(cur) grid(cur,k); graph(ks); drawTip(k); showStats(p); }
  function frame(ts){ const dt=last?Math.min(0.1,(ts-last)/1000):0; last=ts; let need=dirty; dirty=false;
    if(animT<1){ animT=Math.min(1,animT+dt/ANIM); need=true; } if(tip) need=true;
    if(need) draw(); requestAnimationFrame(frame); }
  function setN(v){ NN=v; $('nL').textContent=num(NN)+'個'; }
  function go(){ cur=trial(NN); trials.push(cur); if(trials.length>12) trials.shift(); animT=0; tip=null; dirty=true; }
  $('n').addEventListener('input',function(){ setN(NICE[+$('n').value]); });
  $('n').addEventListener('change',function(){ setN(NICE[+$('n').value]); go(); });
  $('go').addEventListener('click',go);
  $('ten').addEventListener('click',function(){ for(let i=0;i<10;i++){ cur=trial(NN); trials.push(cur); } while(trials.length>12) trials.shift(); animT=1; tip=null; dirty=true; });
  $('mendel').addEventListener('click',function(){ $('n').value=NICE.indexOf(7000); setN(7324); go(); });
  $('gene').addEventListener('click',function(){ showG=!showG; $('gene').textContent=showG?'🔍 遺伝子をかくす':'🔍 遺伝子を表示'; dirty=true; });
  $('clear').addEventListener('click',function(){ trials=cur?[cur]:[]; dirty=true; });
  function hit(e){ const q=cpos(cv,e), x=q[0]/dpr, y=q[1]/dpr;
    if(cur&&x>=SX0-11&&x<=SX0+7*SP+11&&y>=SY0-11&&y<=SY0+7*SP+11){ const c=Math.round((x-SX0)/SP), r=Math.round((y-SY0)/SP), i=r*8+c;
      if(c>=0&&c<8&&r>=0&&r<8&&i<Math.min(SEEDN,ptAt(cur,shownK(cur,animT))[0])){ tip={i:i,t:performance.now()}; dirty=true; } return null; }
    if(x>=CX0&&x<CX0+2*CW&&y>=RY0&&y<RY0+2*RH){ return Math.min(1,Math.floor((y-RY0)/RH))*2+Math.min(1,Math.floor((x-CX0)/CW)); }
    return null; }
  cv.addEventListener('pointerdown',function(e){ press=true; const code=hit(e); if(code!==null){ const g=GT[code]; hl=(hl===g)?null:g; dirty=true; } });
  cv.addEventListener('pointermove',function(e){ if(press) hit(e); });
  const up=function(){ press=false; };
  cv.addEventListener('pointerup',up); cv.addEventListener('pointercancel',up); cv.addEventListener('pointerleave',up);
  setN(NN); cur=trial(NN); trials=[cur]; animT=1; draw();
  requestAnimationFrame(frame);
'''

sim(slug="mendel-iden", cat="rika", emoji="🌱", score=80,
    title="遺伝の規則性シミュレーター（メンデルの交配実験）",
    title_tag="メンデルの法則・遺伝の規則性シミュレーター｜エンドウの交配で丸：しわ＝3：1を確かめる（分離の法則）",
    meta_desc="エンドウの種子の形（丸＝顕性、しわ＝潜性）で、親AA×aa→子Aa→孫の交配を最大1万回シミュレーション。孫の丸・しわの数と比、AA：Aa：aaを表示し、数を増やすほど3：1に近づく様子をグラフで確かめられます。中3「遺伝の規則性と遺伝子」向け。",
    og_title="遺伝の規則性シミュレーター（メンデルの交配実験）",
    og_desc="エンドウの丸×しわを交配。孫を10〜10,000個つくり、丸：しわが3：1に近づく様子をグラフで確かめられます。かけ合わせの表つき。",
    card_desc="丸×しわのエンドウを交配。孫の数を増やすほど丸：しわが3：1に近づく様子をグラフで確かめる。",
    lead="丸い種子（AA）としわのある種子（aa）のエンドウをかけ合わせると、子はすべて丸。その子どうしから生まれる孫では、しわが再び現れます。孫の数を変えて何度も交配し、丸：しわの比が3：1に近づいていく様子を確かめてください。",
    model="中3 遺伝の規則性と遺伝子",
    level="中学3年",
    unit="中学校 第2分野（5）生命の連続性",
    canvas=canvas(640, 520, light=True),
    controls=slider("n", "交配する数（孫の種子の数）", 0, 36, 12, 1),
    buttons=btn("go", "🌱 交配する（孫をつくる）", True) + btn("ten", "🔁 10回くり返す") + btn("mendel", "📗 メンデルと同じ7,324個")
            + btn("gene", "🔍 遺伝子を表示") + btn("clear", "グラフを消す"),
    stats=stats([("sR", "丸の数", False), ("sW", "しわの数", False), ("sRatio", "丸：しわ の比", True), ("sG", "AA：Aa：aa", False)]),
    legend="左上：親→子→孫の流れ。右上：かけ合わせの表（マスをタップすると、その組み合わせの種子だけを表示）。左下：できた孫の種子（タップすると遺伝子が見られます）。右下：孫の数（横軸は10倍ずつ）と丸：しわの比。赤い線が今回、灰色の線がこれまでの結果です。",
    article=MENDEL_ARTICLE,
    faqs=[("「優性・劣性」と「顕性・潜性」は同じ意味？", "同じ意味です。「優性」は優れている、「劣性」は劣っているという誤解を生みやすいため、日本遺伝学会が2017年に「顕性」「潜性」への言いかえを提案しました。今の中学校の教科書は「顕性」「潜性」を使っています。"),
          ("実験の結果がぴったり3：1にならないのはなぜ？", "どの遺伝子の組み合わせになるかは偶然で決まるため、数が少ないとずれます。孫が100個なら、丸：しわが2：1や4：1くらいになるのは珍しくありません。数を増やすほど3：1に近づきます。メンデルも7,324個の種子を調べて2.96：1という結果を得ています。"),
          ("子（Aa）がすべて丸になるのはなぜ？しわの遺伝子はなくなったの？", "Aとaの両方をもつと、顕性の形質（丸）だけが現れるからです。しわの遺伝子aはなくなったわけではなく、子の中に受けつがれています。そのため子どうしをかけ合わせると、aaの組み合わせになった孫でしわが再び現れます。"),
          ("孫の丸い種子がAAかAaかを見分けるには？", "見た目では区別できません。しわの種子（aa）をつくる個体とかけ合わせ、できる種子がすべて丸ならAA、丸としわがおよそ1：1ならAaと分かります。"),
          ("分離の法則とは？", "対になっている遺伝子が、減数分裂で生殖細胞がつくられるときに分かれて、別々の生殖細胞に入ることです。Aaの親からは、Aをもつ生殖細胞とaをもつ生殖細胞が1：1の割合でつくられます。"),
          ("人の血液型も同じしくみ？", "ABO式血液型も遺伝子の組み合わせで決まります。ただし、AとBの遺伝子はどちらも現れ（AB型）、Oの遺伝子は潜性です。エンドウの種子の形より少し複雑で、「血液型 遺伝 判定」で組み合わせを確かめられます。")],
    rel=[("ketsueki-iden", "🩸", "血液型 遺伝 判定"), ("dna", "🧬", "DNA二重らせん"), ("shinka-sim", "🧬", "進化シミュレーター")],
    js=MENDEL_JS)
