# -*- coding: utf-8 -*-
"""理科の授業向けシミュ（高校 生物：酵素の失活）— シミュラボのリクエスト（2026-11-23 受付 1599585fdd／伊藤さん）から
   kouso-shikkatsu … 熱・pHによるタンパク質の立体構造の変化と酵素の失活（変性）
   生物（2）生命現象と物質 ア（ｱ）細胞と分子 ㋑生命現象とタンパク質（酵素の働きとタンパク質の立体構造）
   モデル：1本のポリペプチド鎖（ビーズ）を、折りたたまれた形 ⇄ ほどけた形のあいだで動かす。鎖は切れない。
   数値の確かめは __test（ページ内）から。"""
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []

# スマホ縦向きでは図が小さくなるので、横向きをすすめる一言（幅560px以下・縦向きのときだけ表示）
PH = ('<span class="ph-note">📱 スマホでは、画面を横向きにすると図の中の文字が読みやすくなります。</span>'
      '<style>.ph-note{display:none}@media (max-width:560px) and (orientation:portrait){.ph-note{display:block;font-weight:800;color:#b45309;margin-bottom:6px}}</style>')
def sim(**kw): SIMS.append(kw)

MEXT_KOU = "https://www.mext.go.jp/a_menu/shotou/new-cs/1407074.htm"
def A(url, label): return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, label)

JS = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const FF='"Hiragino Sans","Hiragino Kaku Gothic ProN","Noto Sans JP","Yu Gothic UI","Yu Gothic",Meiryo,sans-serif';
  function tx(s,x,y,size,col,align,bold){ ctx.font=(bold?'bold ':'')+size+'px '+FF; ctx.fillStyle=col; ctx.textAlign=align||'left'; ctx.fillText(s,x,y); ctx.textAlign='left'; }
  function tw(s,size,bold){ ctx.font=(bold?'bold ':'')+size+'px '+FF; return ctx.measureText(s).width; }
  function rr(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
  function pill(s,x,y,size,col,bg){ const w=tw(s,size,true)+16; rr(x-w/2,y-size-2,w,size+12,8); ctx.fillStyle=bg||'rgba(255,255,255,.92)'; ctx.fill(); tx(s,x,y+2,size,col,'center',true); }
  const sm=v=>{ v=clamp(v,0,1); return v*v*(3-2*v); };
  const mix=(a,b,k)=>'rgb('+a.map((v,i)=>Math.round(v+(b[i]-v)*k)).join(',')+')';

  // ===== モデルの数値 =====
  // 反応の速さ：10℃上がると約2倍。変性：41℃をこえると起こり始め、温度が高いほど急に速くなる。pH 3 未満・11 をこえると変性する。
  // 活性部位の2つのアミノ酸：1つは H⁺ を放した状態（−）、もう1つは H⁺ を受け取った状態（＋）のときだけ反応が進む。
  const LO=3, HI=11, PKA_A=4.0, PKA_B=10.5, PKC_A=5.5, PKC_B=8.5;
  const q=T=>Math.pow(2,(T-37)/10);
  const kdT=T=>T>41?.5*Math.exp((T-50)/1.5):0;
  const kdP=p=>{ const o=Math.max(LO-p,p-HI,0); return o>0?.3*(Math.exp(o/.4)-1):0; };
  const fA=(p,pk)=>1/(1+Math.pow(10,pk-p)), fB=(p,pk)=>1/(1+Math.pow(10,p-pk));
  const bell0=p=>fA(p,PKC_A)*fB(p,PKC_B), B7=bell0(7), bell=p=>bell0(p)/B7;
  const refT=T=>q(T)*Math.exp(-kdT(T)*10);
  let AMAX=0; for(let x=0;x<=90;x+=.5) AMAX=Math.max(AMAX,refT(x));

  // ===== 鎖（折りたたまれた形） =====
  const PW=462, PH=360, C={x:205,y:182}, SP=20, RG=92, MOUTH={x:C.x+62,y:C.y}, SITE={x:C.x+31,y:C.y};
  const B=[];
  for(let r=0;r<9;r++){ const y=-80+20*r, n=Math.floor(Math.sqrt(RG*RG-y*y)/SP); let xs=[];
    for(let k=-n;k<=n;k++){ const x=k*SP; if(Math.abs(y)===20&&x>20) continue; if(y===0&&x>0) continue; xs.push(x); }
    if(r%2) xs.reverse(); xs.forEach(x=>B.push({rx:x,ry:y,nx:C.x+x,ny:C.y+y,cx:0,cy:0,x:0,y:0,u:0,type:'p',ch:true,ion:0,cat:0,off:0,f1:0,f2:0,p1:0,p2:0})); }
  const NB=B.length; let seed=11; const lr=()=>(seed=(seed*16807)%2147483647)/2147483647;
  B.forEach(b=>{ b.off=.1+lr()*.34; b.f1=5+lr()*5; b.f2=5+lr()*5; b.p1=lr()*6.28; b.p2=lr()*6.28; b.r=Math.hypot(b.rx,b.ry); });
  const at=(x,y)=>B.findIndex(b=>b.rx===x&&b.ry===y);
  const CA=at(20,-20), CB=at(20,20), BACK=at(0,0);
  B[CA].type='a'; B[CA].cat=1; B[CA].ion=1; B[CB].type='b'; B[CB].cat=1; B[CB].ion=1; [CA,CB,BACK,at(0,-20),at(0,20)].forEach(i=>B[i].off=.04);
  B.forEach(b=>{ if(!b.cat&&b.r<=45) b.type='h'; });
  const used=new Set([CA,CB]); let pairs=[];
  for(let i=0;i<NB;i++) for(let j=i+3;j<NB;j++){ if(Math.hypot(B[i].nx-B[j].nx,B[i].ny-B[j].ny)<21) pairs.push([i,j,lr()]); }
  pairs.sort((a,b)=>a[2]-b[2]);
  const ION=[], HB=[]; let SS=null;
  for(const p of pairs){ if(ION.length>=4) break; const a=B[p[0]],b=B[p[1]]; if(a.r>55&&b.r>55&&!used.has(p[0])&&!used.has(p[1])){ ION.push({i:p[0],j:p[1],th:.2+lr()*.25}); used.add(p[0]); used.add(p[1]); a.type='a'; a.ion=1; b.type='b'; b.ion=1; } }
  { let best=null; for(const p of pairs){ const a=B[p[0]],b=B[p[1]]; if(used.has(p[0])||used.has(p[1])||a.type==='h'||b.type==='h') continue; if(!best||p[1]-p[0]>best[1]-best[0]) best=p; }
    SS=[best[0],best[1]]; used.add(best[0]); used.add(best[1]); B[best[0]].type='c'; B[best[1]].type='c'; }
  for(const p of pairs){ if(HB.length>=10) break; if(used.has(p[0])||used.has(p[1])) continue; HB.push({i:p[0],j:p[1],th:.08+lr()*.2,k:lr()*20}); used.add(p[0]); used.add(p[1]); }
  function mkCoil(){ let x=0,y=0,a=rnd(0,6.28); const p=[];
    for(let i=0;i<NB;i++){ p.push([x,y]); a+=rnd(-.95,.95); x+=Math.cos(a)*17; y+=Math.sin(a)*17; if(Math.hypot(x,y)>140) a=Math.atan2(-y,-x)+rnd(-.7,.7); }
    const sa=SS[0],sb=SS[1], dx=p[sb][0]-p[sa][0]-16, dy=p[sb][1]-p[sa][1]; for(let k=sa+1;k<NB;k++){ const f=k<=sb?(k-sa)/(sb-sa):1; p[k][0]-=dx*f; p[k][1]-=dy*f; }
    let x0=1e9,x1=-1e9,y0=1e9,y1=-1e9; p.forEach(v=>{ x0=Math.min(x0,v[0]); x1=Math.max(x1,v[0]); y0=Math.min(y0,v[1]); y1=Math.max(y1,v[1]); });
    const s=Math.min(1.15,(PW-70)/(x1-x0),(PH-80)/(y1-y0)); B.forEach((b,i)=>{ b.cx=PW/2+(p[i][0]-(x0+x1)/2)*s; b.cy=PH/2+8+(p[i][1]-(y0+y1)/2)*s; }); }

  // ===== 状態 =====
  let t=0, T=37, pH=7, D=0, cause='', loose=0, paused=false, zoom=false, names=true, times=[], subs=[], fx=[], site={s:null,k:0,prog:0,bad:0}, trT=[], trP=[], trc=0, nProd=0;
  function spawn(edge){ const a=rnd(0,6.28); let x=rnd(20,PW-20), y=rnd(20,PH-20); if(edge){ if(Math.random()<.5){ x=PW-14; } else { y=Math.random()<.5?14:PH-14; x=rnd(PW*.45,PW-20); } } else { while(Math.hypot(x-C.x,y-C.y)<RG+24){ x=rnd(20,PW-20); y=rnd(20,PH-20); } }
    return {x:x,y:y,a:a,th:rnd(0,6.28),st:0,cool:0,life:0}; }
  function fresh(){ D=0; cause=''; loose=0; site={s:null,k:0,prog:0,bad:0}; subs=[]; for(let i=0;i<16;i++) subs.push(spawn(false)); times=[]; fx=[]; trT=[]; trP=[]; nProd=0; B.forEach(b=>{ b.ch=true; }); mkCoil(); }
  const pocketOK=()=>B[CA].u<.3&&B[CB].u<.3&&B[BACK].u<.3;
  const catOK=()=>B[CA].ch&&B[CB].ch;
  function act(){ return q(T)*bell(pH)*(1-sm((D-.08)/.3))/AMAX; }
  function ionBroken(){ let n=0; for(const b of ION) if(!(B[b.i].ch&&B[b.j].ch)) n++; return n/ION.length; }
  function structure(){ return (1-D)*(1-.15*loose); }
  function step(dt){
    t+=dt; T=+$('temp').value; pH=+$('ph').value;
    const kT=kdT(T), kP=kdP(pH);
    if(kT+kP>0){ const d0=D; D=Math.min(1,D+(kT+kP)*dt*(1.02-D)); if(d0<.5&&D>=.5) cause=kT>=kP?'heat':'ph'; }
    for(const b of B){ if(!b.ion) continue; if(Math.random()<dt*3){ const f=b.type==='a'?fA(pH,b.cat?PKC_A:PKA_A):fB(pH,b.cat?PKC_B:PKA_B); b.ch=Math.random()<f; } }
    loose+=(ionBroken()-loose)*Math.min(1,dt*2);
    const amp=.8+T/90*3.4, fq=.3+T/45;
    for(const b of B){ const u=sm((D*1.45-b.off)/.55); b.u=u; const j=amp*(1+1.5*u), sw=loose*5*(1-u)*b.r/RG;
      b.x=b.nx+(b.cx-b.nx)*u+Math.sin(t*fq*b.f1+b.p1)*j+b.rx/(b.r||1)*sw; b.y=b.ny+(b.cy-b.ny)*u+Math.cos(t*fq*b.f2+b.p2)*j+b.ry/(b.r||1)*sw; }
    const v=22+T*1.25, ok=pocketOK(), folded=D<.45;
    for(let i=subs.length-1;i>=0;i--){ const s=subs[i]; s.a+=randn()*Math.sqrt(dt)*1.5; s.th+=dt*1.2; if(s.cool>0) s.cool-=dt;
      s.x+=Math.cos(s.a)*v*dt; s.y+=Math.sin(s.a)*v*dt;
      if(s.x<10){s.x=10;s.a=Math.PI-s.a;} if(s.x>PW-10){s.x=PW-10;s.a=Math.PI-s.a;} if(s.y<10){s.y=10;s.a=-s.a;} if(s.y>PH-10){s.y=PH-10;s.a=-s.a;}
      if(folded){ const dx=s.x-C.x, dy=s.y-C.y, d=Math.hypot(dx,dy); const inMouth=dx>18&&Math.abs(dy)<24; if(d<RG+13&&!inMouth){ s.x=C.x+dx/d*(RG+13); s.y=C.y+dy/d*(RG+13); s.a=Math.atan2(dy,dx)+rnd(-1,1); } if(inMouth&&dx<44){ s.x=C.x+44; s.a=rnd(-1,1); } }
      if(s.st===1){ s.life+=dt; if(s.life>4.5){ subs[i]=spawn(true); } continue; }
      const mx=s.x-C.x, my=s.y-C.y;
      if(!site.s&&s.cool<=0&&folded&&ok&&mx>0){ let da=Math.atan2(MOUTH.y-s.y,MOUTH.x+30-s.x)-s.a; while(da>Math.PI) da-=6.283; while(da<-Math.PI) da+=6.283; s.a+=da*Math.min(1,dt*1.3); }
      if(!site.s&&s.cool<=0&&folded&&mx>40&&mx<112&&Math.abs(my)<27){
        if(ok){ site.s=s; site.k=0; site.prog=0; site.bad=0; site.x0=s.x; site.y0=s.y; subs.splice(i,1); }
        else { s.a=rnd(-.9,.9); s.cool=1.2; fx.push({x:MOUTH.x-8,y:MOUTH.y,t:t,type:'x'}); } }
    }
    if(site.s){ site.k=Math.min(1,site.k+dt*3.5); const tau=clamp(2.2/q(T),.4,10);
      if(!pocketOK()){ const s=site.s; s.x=MOUTH.x+6; s.y=MOUTH.y; s.a=rnd(-.8,.8); s.cool=1.5; subs.push(s); site.s=null; }
      else if(site.k<1){ } else if(catOK()){ site.prog+=dt/tau; if(site.prog>=1){ const s=site.s; s.st=1; s.life=0; s.x=MOUTH.x+4; s.y=MOUTH.y; s.a=rnd(-.7,.7); subs.push(s); site.s=null; times.push(t); nProd++; fx.push({x:MOUTH.x-14,y:MOUTH.y,t:t,type:'p'}); } }
      else { site.bad+=dt; if(site.bad>1.6){ const s=site.s; s.x=MOUTH.x+6; s.y=MOUTH.y; s.a=rnd(-.8,.8); s.cool=1.5; subs.push(s); site.s=null; fx.push({x:MOUTH.x-8,y:MOUTH.y,t:t,type:'x'}); } } }
    while(times.length&&t-times[0]>10) times.shift();
    while(fx.length&&t-fx[0].t>.8) fx.shift();
    trc+=dt; if(trc>.25){ trc=0; const a=act(); trT.push([T,a]); trP.push([pH,a]); if(trT.length>240){ trT.shift(); trP.shift(); } }
  }

  // ===== 描く =====
  const COL={p:'#94a3b8',h:'#facc15',a:'#ef4444',b:'#3b82f6',c:'#a3e635'};
  function show(k){ const f=$('bond').value; return f==='all'||f===k; }
  function dSub(x,y,th,k,sc){ const r=10*(sc||1);
    if(k<1){ ctx.beginPath(); ctx.arc(x,y,r,0,7); ctx.fillStyle='#f59e0b'; ctx.fill(); ctx.strokeStyle='#b45309'; ctx.lineWidth=1.3; ctx.stroke();
      if(k>0){ ctx.strokeStyle='rgba(120,53,15,'+k+')'; ctx.lineWidth=1.6; ctx.beginPath(); ctx.moveTo(x+Math.cos(th)*r,y+Math.sin(th)*r); ctx.lineTo(x-Math.cos(th)*r,y-Math.sin(th)*r); ctx.stroke(); } }
    else { for(const sg of [-1,1]){ const ox=Math.cos(th+1.57)*3*sg, oy=Math.sin(th+1.57)*3*sg; ctx.beginPath(); ctx.arc(x+ox,y+oy,r,th+(sg>0?0:Math.PI),th+(sg>0?Math.PI:Math.PI*2)); ctx.closePath(); ctx.fillStyle='#22c55e'; ctx.fill(); ctx.strokeStyle='#15803d'; ctx.lineWidth=1.3; ctx.stroke(); } } }
  function dProtein(){
    // 背景（温度で色が変わる）とイオン
    ctx.fillStyle=mix([239,246,255],[255,241,224],clamp(T/90,0,1)); ctx.fillRect(0,0,PW,PH);
    const nI=Math.round(Math.abs(7-pH)*5), acid=pH<7;
    for(let k=0;k<nI;k++){ const hx=Math.abs(Math.sin(k*12.9898)*43758.5)%1, hy=Math.abs(Math.sin(k*78.233)*12543.1)%1; const x=((hx*PW+t*(8+k%5*3)*(k%2?1:-1))%PW+PW)%PW, y=((hy*PH+Math.sin(t*.6+k)*14)%PH+PH)%PH;
      tx(acid?'H⁺':'OH⁻',x,y,11,acid?'rgba(220,38,38,.5)':'rgba(37,99,235,.5)','center',true); }
    // 疎水性相互作用（内側に集まった疎水性のアミノ酸）
    if(show('hyd')){ for(const b of B){ if(b.type!=='h') continue; const a=.3*(1-b.u); if(a<=.01) continue; ctx.fillStyle='rgba(250,204,21,'+a+')'; ctx.beginPath(); ctx.arc(b.x,b.y,15,0,7); ctx.fill(); } }
    // 主鎖
    ctx.lineJoin='round'; ctx.lineCap='round';
    for(const pass of [0,1]){ ctx.beginPath(); B.forEach((b,i)=>{ if(!i){ ctx.moveTo(b.x,b.y); return; } const p=B[i-1]; ctx.quadraticCurveTo(p.x,p.y,(p.x+b.x)/2,(p.y+b.y)/2); if(i===NB-1) ctx.lineTo(b.x,b.y); });
      ctx.strokeStyle=pass?'#cbd5e1':'#64748b'; ctx.lineWidth=pass?5.5:8; ctx.stroke(); }
    // 相互作用
    if(show('hb')){ for(const h of HB){ const a=B[h.i],b=B[h.j]; const fl=Math.sin(t*(3+T/12)+h.k)>1-2*clamp((T-25)/130,0,.42); if(Math.max(a.u,b.u)>h.th||fl) continue; ctx.strokeStyle='#0891b2'; ctx.lineWidth=3; ctx.setLineDash([2.5,2.5]); ctx.beginPath(); ctx.moveTo(a.x,a.y); ctx.lineTo(b.x,b.y); ctx.stroke(); ctx.setLineDash([]); } }
    if(show('ion')){ for(const h of ION){ const a=B[h.i],b=B[h.j]; if(Math.max(a.u,b.u)>h.th||!(a.ch&&b.ch)) continue; ctx.strokeStyle='#c026d3'; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(a.x,a.y); ctx.lineTo(b.x,b.y); ctx.stroke(); } }
    if(show('ss')){ const a=B[SS[0]],b=B[SS[1]]; ctx.strokeStyle='#4d7c0f'; ctx.lineWidth=4.5; ctx.beginPath(); ctx.moveTo(a.x,a.y); ctx.lineTo(b.x,b.y); ctx.stroke(); }
    // アミノ酸
    for(const b of B){ let col=COL[b.type]; const neutral=b.ion&&!b.ch; ctx.beginPath(); ctx.arc(b.x,b.y,b.cat?8:6.4,0,7); ctx.fillStyle=neutral?'#e2e8f0':col; ctx.fill(); ctx.strokeStyle=b.cat?'#111827':(neutral?col:'rgba(15,23,42,.45)'); ctx.lineWidth=b.cat?2.4:1.2; ctx.stroke();
      if(b.ion) tx(b.ch?(b.type==='a'?'−':'＋'):(b.type==='a'?'H':''),b.x,b.y+4,b.ch?12:9.5,b.ch?'#fff':col,'center',true);
      if(b.type==='c') tx('S',b.x,b.y+3.5,9.5,'#365314','center',true); }
    // 結合している基質
    if(site.s){ const k=sm(site.k), x=site.x0+(SITE.x-site.x0)*k+(B[BACK].x-B[BACK].nx)*.5*k, y=site.y0+(SITE.y-site.y0)*k+(B[BACK].y-B[BACK].ny)*.5*k; const good=catOK();
      if(good){ ctx.save(); ctx.shadowColor='rgba(245,158,11,.9)'; ctx.shadowBlur=10+5*Math.sin(t*9); dSub(x,y,1.57,Math.min(.99,site.prog),1); ctx.restore(); ctx.strokeStyle='#f59e0b'; ctx.lineWidth=2.5; ctx.beginPath(); ctx.arc(x,y,14,-1.57,-1.57+site.prog*6.283); ctx.stroke(); }
      else { dSub(x,y,1.57,0,1); ctx.strokeStyle='#dc2626'; ctx.lineWidth=2.2; ctx.beginPath(); ctx.moveTo(x-5,y-5); ctx.lineTo(x+5,y+5); ctx.moveTo(x+5,y-5); ctx.lineTo(x-5,y+5); ctx.stroke(); } }
    for(const s of subs) dSub(s.x,s.y,s.th,s.st,.9);
    for(const f of fx){ const k=(t-f.t)/.8; if(f.type==='p'){ ctx.strokeStyle='rgba(34,197,94,'+(1-k)+')'; ctx.lineWidth=3*(1-k)+.5; ctx.beginPath(); ctx.arc(f.x+20,f.y,6+k*26,0,7); ctx.stroke(); }
      else { ctx.strokeStyle='rgba(220,38,38,'+(1-k)+')'; ctx.lineWidth=2.5; const r=6+k*5, x=f.x+26, y=f.y-22-k*10; ctx.beginPath(); ctx.moveTo(x-r,y-r); ctx.lineTo(x+r,y+r); ctx.moveTo(x+r,y-r); ctx.lineTo(x-r,y+r); ctx.stroke(); } }
    if(names&&D<.3){ const y=B[CA].y-26; tx('活性部位',MOUTH.x+34,y-2,12,'#0f172a','center',true); ctx.strokeStyle='#0f172a'; ctx.lineWidth=1.2; ctx.beginPath(); ctx.moveTo(MOUTH.x+20,y+2); ctx.lineTo(SITE.x+8,C.y-12); ctx.stroke(); }
  }
  function dKey(){ if(!names) return; const it=[['hb','水素結合'],['ion','イオン結合'],['hyd','疎水性相互作用'],['ss','ジスルフィド結合']]; let x=10; const y=PH-14;
    rr(4,PH-30,PW-8,25,7); ctx.fillStyle='rgba(255,255,255,.9)'; ctx.fill();
    for(const [k,l] of it){ const on=show(k); ctx.globalAlpha=on?1:.3;
      if(k==='hb'){ ctx.strokeStyle='#0891b2'; ctx.lineWidth=2.4; ctx.setLineDash([2.5,3.5]); ctx.beginPath(); ctx.moveTo(x,y-4); ctx.lineTo(x+20,y-4); ctx.stroke(); ctx.setLineDash([]); }
      if(k==='ion'){ ctx.strokeStyle='#c026d3'; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(x,y-4); ctx.lineTo(x+20,y-4); ctx.stroke(); }
      if(k==='hyd'){ ctx.fillStyle='rgba(250,204,21,.55)'; ctx.beginPath(); ctx.arc(x+10,y-4,8,0,7); ctx.fill(); }
      if(k==='ss'){ ctx.strokeStyle='#4d7c0f'; ctx.lineWidth=4.5; ctx.beginPath(); ctx.moveTo(x,y-4); ctx.lineTo(x+20,y-4); ctx.stroke(); }
      tx(l,x+24,y,10.5,'#0f172a','left',true); ctx.globalAlpha=1; x+=24+tw(l,10.5,true)+12; }
    rr(4,4,214,24,7); ctx.fillStyle='rgba(255,255,255,.9)'; ctx.fill(); dSub(18,16,0,0,.8); tx('基質',30,20,11,'#0f172a','left',true); dSub(72,16,0,1,.8); tx('生成物',86,20,11,'#0f172a','left',true);
    ctx.beginPath(); ctx.arc(140,16,7,0,7); ctx.fillStyle='#e2e8f0'; ctx.fill(); ctx.strokeStyle='#111827'; ctx.lineWidth=2.2; ctx.stroke(); tx('反応に必要',151,20,11,'#0f172a','left',true); }
  function status(){
    if(D>.5) return cause==='ph'?['#b91c1c','極端なpHで立体構造が','くずれた（変性・失活）。','条件をもどしても形はもどらない']:['#b91c1c','熱で立体構造がくずれた','（変性・失活）。温度を','下げても形はもどらない'];
    if(D>.08) return ['#c2410c','立体構造がくずれ始めている。','活性部位の形が変わり、','基質が結合しにくい'];
    if(bell(pH)<.6) return ['#7c3aed','形はほぼ保たれているが、','活性部位の電荷が変わり、','反応が進みにくい'];
    if(T<20) return ['#1d4ed8','形は保たれている。','低温で分子の動きがおそく、','反応がおそい（失活ではない）'];
    return ['#047857','立体構造が保たれ、','基質が活性部位に結合して','生成物ができている'];
  }
  function dPanel(){
    const x0=PW+6, w=W-PW-12; rr(x0,6,w,PH-12,10); ctx.fillStyle='#fff'; ctx.fill(); ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; ctx.stroke();
    // 温度計
    const tx0=x0+34, ty0=34, th=150; tx('温度',tx0,24,11.5,'#0f172a','center',true);
    rr(tx0-7,ty0,14,th,7); ctx.fillStyle='#e2e8f0'; ctx.fill(); const fh=Math.max(6,th*T/90), tc='hsl('+(220-T/90*220)+',85%,50%)'; rr(tx0-7,ty0+th-fh,14,fh,7); ctx.fillStyle=tc; ctx.fill();
    ctx.beginPath(); ctx.arc(tx0,ty0+th+6,12,0,7); ctx.fillStyle=tc; ctx.fill(); tx(T+'℃',tx0,ty0+th+38,14,'#0f172a','center',true);
    [0,30,60,90].forEach(v=>tx(String(v),tx0-12,ty0+th-th*v/90+4,9.5,'#64748b','right'));
    // pH
    const px=x0+w-46; tx('pH',px,24,11.5,'#0f172a','center',true); const g=ctx.createLinearGradient(0,ty0+th,0,ty0);
    g.addColorStop(0,'#dc2626'); g.addColorStop(.25,'#f97316'); g.addColorStop(.5,'#22c55e'); g.addColorStop(.75,'#3b82f6'); g.addColorStop(1,'#7c3aed'); rr(px-7,ty0,14,th,7); ctx.fillStyle=g; ctx.fill();
    const my=ty0+th-th*(pH-1)/12; ctx.fillStyle='#0f172a'; ctx.beginPath(); ctx.moveTo(px+9,my); ctx.lineTo(px+19,my-6); ctx.lineTo(px+19,my+6); ctx.closePath(); ctx.fill();
    tx('酸性',px-12,ty0+th-2,9.5,'#64748b','right'); tx('中性',px-12,ty0+th/2+4,9.5,'#64748b','right'); tx('アルカリ性',px-12,ty0+9,9.5,'#64748b','right');
    tx('pH '+pH.toFixed(1),px,ty0+th+38,14,'#0f172a','center',true);
    // ゲージ
    const gx=x0+12, gw=w-24; let gy=246; const S=structure(), a=act();
    tx('立体構造の保たれ具合 '+Math.round(S*100)+'%',gx,gy,11,'#0f172a','left',true); rr(gx,gy+5,gw,8,4); ctx.fillStyle='#e2e8f0'; ctx.fill(); if(S>.02){ rr(gx,gy+5,Math.max(8,gw*S),8,4); ctx.fillStyle='#0ea5e9'; ctx.fill(); }
    gy+=32; tx('酵素活性 '+Math.round(a*100)+'（最適を100）',gx,gy,11,'#0f172a','left',true); rr(gx,gy+5,gw,8,4); ctx.fillStyle='#e2e8f0'; ctx.fill(); if(a>.02){ rr(gx,gy+5,Math.max(8,gw*Math.min(1,a/1.2)),8,4); ctx.fillStyle='#f59e0b'; ctx.fill(); }
    const st=status(); rr(gx-4,gy+22,gw+8,54,8); ctx.fillStyle='#f8fafc'; ctx.fill(); for(let i=1;i<st.length;i++) tx(st[i],gx+gw/2,gy+38+(i-1)*15,10.5,st[0],'center',true);
  }
  function frame(x,y,w,h,xmin,xmax,ymax,xl,yl){
    rr(x,y,w,h,10); ctx.fillStyle='#fff'; ctx.fill(); ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; ctx.stroke();
    const L=x+38,R=x+w-14,Tp=y+28,Bt=y+h-34; const X=v=>L+(v-xmin)/(xmax-xmin)*(R-L), Y=v=>Bt-Math.min(v,ymax*1.04)/ymax*(Bt-Tp);
    ctx.strokeStyle='#eef2f7'; ctx.lineWidth=1; for(let i=1;i<=4;i++){ const yy=Bt-(Bt-Tp)*i/4; ctx.beginPath(); ctx.moveTo(L,yy); ctx.lineTo(R,yy); ctx.stroke(); }
    ctx.strokeStyle='#334155'; ctx.lineWidth=1.4; ctx.beginPath(); ctx.moveTo(L,Tp-4); ctx.lineTo(L,Bt); ctx.lineTo(R+2,Bt); ctx.stroke();
    for(let i=0;i<=4;i++) tx(String(Math.round(ymax*i/4*100)),L-5,Bt-(Bt-Tp)*i/4+4,11,'#475569','right');
    tx(xl,(L+R)/2,y+h-4,12,'#0f172a','center',true); tx(yl,x+8,y+16,12,'#0f172a','left',true);
    return {X:X,Y:Y,L:L,R:R,T:Tp,B:Bt};
  }
  function dGraphs(){
    const gy=PH+8, gh=H-PH-14, a=act();
    // 温度と酵素活性
    let f=frame(6,gy,312,gh,0,90,1.2,'温度（℃）','酵素活性（最適を100）');
    [0,15,30,45,60,75,90].forEach(v=>tx(String(v),f.X(v),f.B+14,11,'#475569','center'));
    const bp=bell(pH); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=2; ctx.setLineDash([5,4]); ctx.beginPath(); for(let x=0;x<=90;x+=1){ const y=f.Y(refT(x)/AMAX*bp); x?ctx.lineTo(f.X(x),y):ctx.moveTo(f.X(x),y); } ctx.stroke(); ctx.setLineDash([]);
    trT.forEach((p,i)=>{ ctx.fillStyle='rgba(13,148,136,'+(.15+.6*i/trT.length)+')'; ctx.beginPath(); ctx.arc(f.X(p[0]),f.Y(p[1]),2.6,0,7); ctx.fill(); });
    ctx.strokeStyle='#0d9488'; ctx.lineWidth=1; ctx.setLineDash([3,3]); ctx.beginPath(); ctx.moveTo(f.X(T),f.T); ctx.lineTo(f.X(T),f.B); ctx.stroke(); ctx.setLineDash([]);
    ctx.fillStyle='#f59e0b'; ctx.beginPath(); ctx.arc(f.X(T),f.Y(a),6,0,7); ctx.fill(); ctx.strokeStyle='#fff'; ctx.lineWidth=2; ctx.stroke();
    tx('点線＝10秒おいたときのめやす',f.R,f.T-12,9.5,'#64748b','right');
    // pHと酵素活性
    f=frame(322,gy,312,gh,1,13,1.2,'pH','酵素活性（最適を100）');
    [1,3,5,7,9,11,13].forEach(v=>tx(String(v),f.X(v),f.B+14,11,'#475569','center'));
    const tf=refT(T)/AMAX; ctx.strokeStyle='#94a3b8'; ctx.lineWidth=2; ctx.setLineDash([5,4]); ctx.beginPath(); for(let x=1;x<=13.01;x+=.1){ const y=f.Y(bell(x)*Math.exp(-kdP(x)*10)*tf); x>1?ctx.lineTo(f.X(x),y):ctx.moveTo(f.X(x),y); } ctx.stroke(); ctx.setLineDash([]);
    trP.forEach((p,i)=>{ ctx.fillStyle='rgba(13,148,136,'+(.15+.6*i/trP.length)+')'; ctx.beginPath(); ctx.arc(f.X(p[0]),f.Y(p[1]),2.6,0,7); ctx.fill(); });
    ctx.strokeStyle='#0d9488'; ctx.lineWidth=1; ctx.setLineDash([3,3]); ctx.beginPath(); ctx.moveTo(f.X(pH),f.T); ctx.lineTo(f.X(pH),f.B); ctx.stroke(); ctx.setLineDash([]);
    ctx.fillStyle='#f59e0b'; ctx.beginPath(); ctx.arc(f.X(pH),f.Y(a),6,0,7); ctx.fill(); ctx.strokeStyle='#fff'; ctx.lineWidth=2; ctx.stroke();
    tx('●＝いまの酵素の活性',f.R,f.T-12,9.5,'#b45309','right',true);
  }
  function draw(){
    ctx.clearRect(0,0,W,H); ctx.fillStyle='#f8fafc'; ctx.fillRect(0,0,W,H);
    ctx.save(); rr(0,0,PW,PH,10); ctx.clip();
    if(zoom){ const z=2.1; ctx.save(); ctx.translate(PW/2,PH/2); ctx.scale(z,z); ctx.translate(-(C.x+34),-C.y); dProtein(); ctx.restore(); } else dProtein();
    dKey();
    if(zoom) pill('活性部位を拡大中',PW-70,48,11,'#0f172a','rgba(254,243,199,.95)');
    if(paused) pill('一時停止中',PW/2,54,13,'#0f172a','rgba(255,255,255,.95)');
    ctx.restore(); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1; rr(.5,.5,PW-1,PH-1,10); ctx.stroke();
    dPanel(); dGraphs();
    const a=act(), st=status();
    setStat('sS',Math.round(structure()*100)+' %'); setStat('sA',String(Math.round(a*100))); setStat('sP',times.length+' 個'); setStat('sC',D>.5?'変性（失活）':D>.08?'変性し始め':bell(pH)<.6?'電荷の変化':T<20?'低温でおそい':'はたらいている');
    setShare('【酵素の失活】'+T+'℃・pH'+pH.toFixed(1)+'で、立体構造の保たれ具合は'+Math.round(structure()*100)+'%、酵素活性は'+Math.round(a*100)+'（最適を100）｜シミュラボ');
  }
  function loop(){ if(!paused){ const sp=+$('spd').value, n=Math.max(1,Math.round(sp*2)); for(let i=0;i<n;i++) step(1/120); } draw(); requestAnimationFrame(loop); }
  $('pause').addEventListener('click',()=>{ paused=!paused; $('pause').textContent=paused?'▶ 再開':'⏸ 一時停止'; });
  $('stepb').addEventListener('click',()=>{ paused=true; $('pause').textContent='▶ 再開'; for(let i=0;i<12;i++) step(1/120); });
  $('fresh').addEventListener('click',fresh);
  $('best').addEventListener('click',()=>{ $('temp').value=37; $('ph').value=7; $('temp').dispatchEvent(new Event('input')); $('ph').dispatchEvent(new Event('input')); });
  $('zoom').addEventListener('click',()=>{ zoom=!zoom; $('zoom').textContent=zoom?'🔍 全体を表示':'🔍 活性部位を拡大'; });
  $('names').addEventListener('click',()=>{ names=!names; $('names').textContent=names?'🏷 名前をかくす':'🏷 名前を表示'; });
  window.__test={step:function(s){ const n=Math.round(s*60); for(let i=0;i<n;i++) step(1/60); draw(); },get s(){ return {T:T,pH:pH,D:+D.toFixed(3),act:+act().toFixed(3),str:+structure().toFixed(3),prod:nProd,cause:cause,loose:+loose.toFixed(2),NB:NB,ION:ION.length,HB:HB.length,SS:SS,AMAX:+AMAX.toFixed(3)}; },refT:refT,bell:bell,kdT:kdT,kdP:kdP,q:q};
  fresh(); step(1/60); loop();
'''

ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
<p>酵素はタンパク質でできていて、1本のポリペプチド鎖が決まった形に折りたたまれることで、基質がちょうどはまる<b>活性部位</b>ができています。このシミュレーターでは、温度とpHを変えると、立体構造を支えている相互作用と、タンパク質全体の形、活性部位の形・電荷がどう変わり、それが酵素のはたらきにどうつながるかを見ることができます。</p>
''' + N('<b>対応する単元</b>：高等学校「生物」（2）生命現象と物質 ア（ｱ）細胞と分子「㋑生命現象とタンパク質」。学習指導要領では、酵素について「その働きとタンパク質の立体構造との関連」を扱うこととされ、解説ではタンパク質の立体構造や熱による変性の資料を使うことが例に挙げられています。「生物基礎」の酵素（最適温度・最適pH）の発展としても使えます。') + '''
<h2>授業での使い方</h2>
<h3>導入：立体構造は何で支えられているか</h3>
<p>37℃・pH 7 の状態で、「表示する相互作用」を1つずつ切り替えます。水素結合（青緑の点線）、＋と−の電荷をもつ側鎖どうしのイオン結合（紫の線）、内側に集まった疎水性のアミノ酸（黄色）、ジスルフィド結合（緑の太い線）によって、鎖が折りたたまれた形に保たれています。基質（オレンジ）は活性部位にはまり、生成物（緑）になって出ていきます。</p>
<h3>展開1：温度を変える</h3>
<p>温度を5℃に下げると、分子の動きがおそくなり、基質が結合してから生成物になるまでの時間が長くなります。形は保たれているので、温度を37℃にもどせば元どおりにはたらきます。次に温度を少しずつ上げると、40℃すぎまでは反応が速くなりますが、45℃をこえると水素結合などが切れ始め、50℃では数秒で鎖がほどけて活性部位がなくなります。「↺ 最適条件にもどす」を押しても形はもどりません。左下のグラフには通った点が残るので、「上げるとき」と「下げるとき」で活性がちがうことがわかります。</p>
<h3>展開2：pHを変える</h3>
<p>「🧪 新しい酵素に取りかえる」を押し、pHを5や9に変えます。全体の形はほとんど変わりませんが、活性部位の2つのアミノ酸（黒いふちの丸）の電荷が変わり、基質が結合しても反応が進まないこと（赤い×）が増えます。pHを7にもどすと、活性ももどります。pHを3より小さく、または11より大きくすると、側鎖の電荷が大きく変わってイオン結合が切れ、立体構造そのものがくずれます。</p>
<h3>生徒への問いの例</h3>
<ol>
<li>5℃で反応がおそい状態と、70℃で反応しなくなった状態は、何がちがうだろう？それぞれ37℃にもどすとどうなるだろう？</li>
<li>変性したとき、ポリペプチド鎖は切れているだろうか？アミノ酸の並び順（一次構造）は変わっているだろうか？</li>
<li>pH 5 では形がほとんど変わっていないのに、活性が下がるのはなぜだろう？</li>
</ol>
<h2>しくみ・解説</h2>
<h3>用語</h3>
<ul>
<li><b>立体構造</b>とは、ポリペプチド鎖が折りたたまれてできる、タンパク質ごとに決まった形です。アミノ酸の並び順を一次構造、部分的な規則的な構造（αヘリックス・βシート）を二次構造、鎖全体の立体的な形を三次構造といいます。</li>
<li><b>変性</b>とは、熱や酸・アルカリなどによって、タンパク質の立体構造がくずれることです。アミノ酸どうしをつなぐペプチド結合は切れず、一次構造は変わりません。</li>
<li><b>失活</b>とは、酵素などのタンパク質が、はたらきを失うことです。</li>
<li><b>最適温度・最適pH</b>とは、酵素の反応速度が最も大きくなる温度・pHです。</li>
</ul>
<h3>立体構造を支える相互作用</h3>
''' + T([["水素結合", "主鎖や側鎖の −NH と C=O などのあいだ", "弱い。熱運動が激しくなると切れやすい"],
          ["イオン結合（静電的な相互作用）", "＋の電荷をもつ側鎖と −の電荷をもつ側鎖のあいだ", "pHが変わって電荷がなくなると失われる"],
          ["疎水性相互作用", "疎水性の側鎖が水をさけて内側に集まる", "形がくずれると疎水性の部分が外に出る"],
          ["ジスルフィド結合（S−S結合）", "システインの側鎖の −SH どうし", "共有結合で強い。熱やpHだけではふつう切れない"]],
         ["相互作用", "どこにできるか", "特徴"]) + '''
<h3>温度と酵素活性</h3>
<p>温度が上がると、酵素と基質の分子の動きが激しくなり、反応は速くなります（このモデルでは10℃で約2倍）。一方、温度が高くなりすぎると、立体構造を支える弱い相互作用が保てなくなり、変性して失活します。この2つのかね合いで、反応速度が最大になる最適温度が決まります。低温で反応がおそいのは分子の動きがおそいためで、立体構造は保たれているので、温度を上げれば再びはたらきます。熱で変性した酵素は、多くの場合、温度を下げても元の立体構造にはもどりません。</p>
<h3>pHと酵素活性</h3>
<p>アミノ酸の側鎖には、まわりの H⁺ の濃度によって H⁺ を受け取ったり放したりするものがあります（−COOH ⇄ −COO⁻、−NH₃⁺ ⇄ −NH₂ など）。pHが変わると側鎖の電荷が変わるため、①活性部位で基質の結合や反応に必要な電荷の状態がくずれる、②側鎖どうしの引き合い・反発が変わって立体構造がくずれる、という2つのことが起こります。最適pHから少しはずれたときは主に①が起こり、pHをもどせば活性ももどります。極端なpHでは②によって変性します。</p>
''' + P('最適pHは酵素によってちがいます。だ液アミラーゼは約7、胃ではたらくペプシンは約2、すい液のトリプシンは約8です。このシミュレーターは最適pHが7付近、最適温度が40℃すぎの酵素をモデルにしています。') + '''
<h3>このシミュレーターのモデル</h3>
<p>ポリペプチド鎖をアミノ酸59個のビーズとして、平面の上に描いた模式的なモデルです。実際のタンパク質は立体的で、数百個のアミノ酸からなり、相互作用の数もはるかに多くあります。変性が始まる温度・pHや、変性の進む速さは、授業時間内に変化が見えるように決めた値で、特定の酵素の実測値ではありません。グラフの点線は「その条件に10秒おいたとき」のめやすで、置く時間が長いほど、高温側の活性はさらに低くなります。極端なpHによる変性も、このモデルでは元にもどらないものとしています。</p>
<h2>参考</h2>
<ul>
<li>''' + A(MEXT_KOU, "文部科学省 高等学校学習指導要領（平成30年告示）解説 理科編") + '''（生物（2）生命現象と物質）</li>
<li>高等学校「生物」「生物基礎」の教科書（タンパク質の立体構造、変性と失活、酵素の最適温度・最適pH）</li>
</ul>
'''

sim(slug="kouso-shikkatsu", cat="rika", emoji="🌡️", score=80,
    title="酵素の失活シミュレーター（熱・pHによるタンパク質の変性と立体構造）",
    title_tag="酵素の失活・タンパク質の変性シミュレーター｜熱とpHで立体構造と活性部位がどう変わるか（高校生物）",
    meta_desc="温度とpHを変えると、タンパク質の立体構造を支える水素結合・イオン結合・疎水性相互作用・ジスルフィド結合と、活性部位の形・電荷がどう変わり、酵素が失活するかを観察できるシミュレーター。温度と酵素活性、pHと酵素活性のグラフが分子の動きと連動します。",
    og_title="酵素の失活シミュレーター（熱・pHによるタンパク質の変性と立体構造）",
    og_desc="温度を上げると鎖がほどけて活性部位がなくなる。低温はおそいだけで、もどせばはたらく。pHを変えると側鎖の電荷が変わる。変性しても鎖は切れない。構造が変わるとはたらきが変わる理由が見える。",
    card_desc="温度とpHを変えて、タンパク質の立体構造を支える相互作用と活性部位がどう変わり、酵素が失活するかを見る。",
    lead="折りたたまれた1本の鎖が酵素（タンパク質）、右のくぼみが活性部位です。温度とpHのスライダーを動かすと、立体構造を支えている相互作用が切れたり、側鎖の電荷が変わったりして、基質の結合や反応に影響が出ます。低温で反応がおそい状態、高温で変性した状態、pHで活性部位の電荷が変わった状態を比べてみましょう。",
    model="生物 細胞と分子（酵素の働きとタンパク質の立体構造：変性と失活）",
    level="高校（生物）、生物基礎の発展",
    unit="高等学校 生物（2）生命現象と物質 ア（ｱ）細胞と分子 ㋑生命現象とタンパク質",
    canvas=canvas(640, 590, light=True),
    controls=slider("temp", "温度", 0, 90, 37, 1, "{v} ℃")
             + slider("ph", "pH", 1, 13, 7, 0.5, "pH {v}")
             + select("bond", "表示する相互作用", [("all", "すべて"), ("hb", "水素結合"), ("ion", "イオン結合（静電的な相互作用）"), ("hyd", "疎水性相互作用"), ("ss", "ジスルフィド結合"), ("none", "表示しない")])
             + select("spd", "速さ", [("1", "×1"), ("2", "×2"), ("0.5", "×0.5（ゆっくり）")]),
    buttons=btn("pause", "⏸ 一時停止", True) + btn("stepb", "⏭ コマ送り") + btn("best", "↺ 最適条件にもどす") + btn("fresh", "🧪 新しい酵素に取りかえる") + btn("zoom", "🔍 活性部位を拡大") + btn("names", "🏷 名前をかくす"),
    stats=stats([("sS", "立体構造の保たれ具合", False), ("sA", "酵素活性（最適を100）", True), ("sP", "生成物（直近10秒）", True), ("sC", "酵素の状態", False)]),
    legend=PH + "丸1個がアミノ酸（赤＝−の電荷をもつ側鎖、青＝＋の電荷をもつ側鎖、黄＝疎水性、緑のS＝システイン、灰色＝その他）。電荷を失った側鎖は白くなります。黒いふちの2つは、反応に必要な活性部位のアミノ酸。オレンジ＝基質、緑＝生成物、赤い×＝基質が結合できない、または結合しても反応が進まないこと。背景の H⁺・OH⁻ はpHのめやすです。",
    article=ARTICLE,
    faqs=[("変性と失活のちがいは？", "変性は、熱や酸・アルカリなどによってタンパク質の立体構造がくずれることです。失活は、酵素などがはたらきを失うことです。酵素は変性すると活性部位の形が変わるので失活しますが、立体構造がほとんど変わらなくても、活性部位の電荷が変わるだけで活性が下がることもあります。"),
          ("変性すると、ポリペプチド鎖は切れるの？", "切れません。変性でくずれるのは、水素結合などの弱い相互作用で支えられている立体構造です。アミノ酸どうしをつなぐペプチド結合は切れないので、アミノ酸の並び順（一次構造）は変わりません。ペプチド結合が切れてアミノ酸や短いペプチドになるのは、消化などの「分解」です。"),
          ("低温で酵素がはたらかないのも失活？", "ちがいます。低温では分子の動きがおそくなり、酵素と基質が出会う回数や、反応が進む速さが小さくなるだけで、立体構造は保たれています。温度を上げれば再びはたらきます。高温で変性した酵素は、多くの場合、温度を下げても元にもどりません。"),
          ("最適温度をこえると反応速度が急に下がるのはなぜ？", "温度が高いほど反応そのものは速くなりますが、ある温度をこえると、立体構造を支える水素結合などの弱い相互作用が熱運動で保てなくなり、変性する酵素が急に増えるからです。変性した酵素は基質と結合できないので、全体の反応速度は急に下がります。"),
          ("pHが変わると酵素のはたらきが変わるのはなぜ？", "アミノ酸の側鎖には、pHによって H⁺ を受け取ったり放したりして電荷が変わるものがあります。活性部位のアミノ酸の電荷が変わると、基質の結合や反応が進みにくくなります。さらに極端なpHでは、側鎖どうしの引き合いや反発が変わり、立体構造そのものがくずれて変性します。"),
          ("どの酵素も同じ温度・pHで失活するの？", "酵素によってちがいます。胃ではたらくペプシンの最適pHは約2、すい液のトリプシンは約8です。また、温泉などにすむ好熱菌の酵素には、90℃以上でもはたらくものがあり、PCR法で使われるDNAポリメラーゼはその例です。")],
    rel=[("kouso-hannou-sokudo", "⚗️", "酵素の反応速度シミュレーター"), ("kouso-sogai", "🔒", "酵素の阻害シミュレーター"),
         ("maku-yuso", "🚪", "膜輸送のシミュレーター"), ("rinshishitsu-maku", "🧼", "リン脂質と細胞膜のでき方シミュレーター"), ("joutai-henka", "🧊", "状態変化と粒子のシミュレーター")],
    js=JS)
