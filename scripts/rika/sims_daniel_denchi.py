# -*- coding: utf-8 -*-
"""理科の授業向けシミュ（2026-11-18）ダニエル電池
   daniel-denchi … 中3「化学変化とイオン」（第1分野（6）ア（イ）化学変化と電池 ㋐金属イオン ㋑化学変化と電池）"""
from common import canvas, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

MEXT_CHU = "https://www.mext.go.jp/a_menu/shotou/new-cs/1387016.htm"
def A(url, label): return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, label)

JS = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const FF='"Hiragino Sans","Hiragino Kaku Gothic ProN","Noto Sans JP","Yu Gothic UI","Yu Gothic",Meiryo,sans-serif';
  function tx(s,x,y,size,col,align,bold){ ctx.font=(bold?'bold ':'')+size+'px '+FF; ctx.fillStyle=col; ctx.textAlign=align||'left'; ctx.fillText(s,x,y); ctx.textAlign='left'; }
  function tw(s,size,bold){ ctx.font=(bold?'bold ':'')+size+'px '+FF; return ctx.measureText(s).width; }
  function rr(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
  function tag(s,x,y,size,col,bg,align){ const w=tw(s,size,true), x0=align==='right'?x-w:align==='center'?x-w/2:x; ctx.fillStyle=bg||'rgba(255,255,255,0.94)'; rr(x0-5,y-size-2,w+10,size+8,6); ctx.fill(); tx(s,x0,y,size,col,'left',true); }
  function arrow(x1,y1,x2,y2,col,w,s){ const dx=x2-x1, dy=y2-y1, l=Math.hypot(dx,dy); if(l<2) return; const ux=dx/l, uy=dy/l; ctx.strokeStyle=col; ctx.lineWidth=w; ctx.lineCap='round'; ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2-ux*s*1.3,y2-uy*s*1.3); ctx.stroke(); ctx.lineCap='butt';
    ctx.fillStyle=col; ctx.beginPath(); ctx.moveTo(x2,y2); ctx.lineTo(x2-ux*s*1.7-uy*s,y2-uy*s*1.7+ux*s); ctx.lineTo(x2-ux*s*1.7+uy*s,y2-uy*s*1.7-ux*s); ctx.closePath(); ctx.fill(); }
  // 金属：rank が大きいほどイオンになりやすい（中学の実験で調べる順 Mg＞Zn＞Cu）
  const M={zn:{nm:'亜鉛',s:'Zn',col:'#9ca3af',ion:'#64748b',sol:'硫酸亜鉛水溶液',solc:null,rank:2},
           cu:{nm:'銅',s:'Cu',col:'#c2703d',ion:'#2563eb',sol:'硫酸銅水溶液',solc:[96,165,250],rank:1},
           mg:{nm:'マグネシウム',s:'Mg',col:'#d4d4d8',ion:'#a855f7',sol:'硫酸マグネシウム水溶液',solc:null,rank:3}};
  // 組み合わせ：左＝イオンになりやすい方。V＝標準電極電位の差（理論値）
  const PAIR={'zn-cu':['zn','cu',1.10],'mg-cu':['mg','cu',2.71],'mg-zn':['mg','zn',1.61],'zn-zn':['zn','zn',0],'cu-cu':['cu','cu',0]};
  const XL=150, XR=490, MX=320, LT=176, LB=400, PT=96, PB=372, BOXL=58, BOXR=582, WY=44, VX=232, PX=410;
  let pair='zn-cu', A_, B_, V0, mem=true, run=false, speed=1, ions=[], wA, wB, nd=0, ndep=0, ndir=0, spots=[], elec=0, prop=0, tEv=0, I=0, Vnow=0, lastT=0, done=false, tNow=0, flash=[];
  const W0=26, CU0=12;
  function mk(t,side){ const x=side<0?rnd(BOXL+14,MX-14):rnd(MX+14,BOXR-14); return {t:t,x:x,y:rnd(LT+14,LB-14),vx:rnd(-30,30),vy:rnd(-30,30),tg:null,cross:false}; }
  function reset(){ const p=PAIR[pair]; A_=M[p[0]]; B_=M[p[1]]; V0=p[2]; ions=[]; nd=0; ndep=0; ndir=0; spots=[]; flash=[]; done=false; wA=W0; wB=W0*0.55; tEv=0; elec=0;
    for(let i=0;i<7;i++){ ions.push(mk('A',-1)); ions.push(mk('S',-1)); }
    for(let i=0;i<CU0;i++){ ions.push(mk('B',1)); ions.push(mk('S',1)); }
    syncUI(); }
  function plateRect(side){ const w=side<0?wA:wB, x=side<0?XL:XR; return [x-w/2,PT,w,PB-PT]; }
  function onPlate(o,side,pad){ const r=plateRect(side); return o.x>r[0]-pad&&o.x<r[0]+r[2]+pad&&o.y>LT&&o.y<r[1]+r[3]+pad; }
  const cntB=()=>ions.filter(o=>o.t==='B'&&o.x>MX).length, cntBall=()=>ions.filter(o=>o.t==='B').length;
  function event(){ // −極で金属が溶け、＋極で金属イオンが金属になる
    const tgt=ions.filter(o=>o.t==='B'&&!o.tg&&o.x>MX); if(!tgt.length){ return; }
    let best=tgt[0]; tgt.forEach(o=>{ if(Math.abs(o.x-XR)<Math.abs(best.x-XR)) best=o; });
    best.tg='dep';
    const y=rnd(LT+20,PB-20), z={t:'A',x:XL+wA/2+10,y:y,vx:rnd(20,50),vy:rnd(-20,20),tg:null,cross:false}; ions.push(z); flash.push({x:XL+wA/2,y:y,t:0,c:A_.ion}); nd++; wA=Math.max(8,wA-0.9);
    // 電気のつり合い：硫酸イオンが1個、セロハンを通って左へ（ときどき金属イオンが右へ）
    if(Math.random()<0.75){ const ss=ions.filter(o=>o.t==='S'&&o.x>MX&&!o.tg); if(ss.length){ const s=ss[Math.floor(Math.random()*ss.length)]; s.tg='left'; } }
    else { const aa=ions.filter(o=>o.t==='A'&&o.x<MX&&!o.tg); if(aa.length){ aa[0].tg='right'; } }
    elec+=2; }
  function step(dt){
    const same=V0===0;
    // 電流の大きさ（0〜1）：セロハンなしだと、＋極側のイオンが−極に直接ついて電子が導線を通らなくなる
    const rem=cntB(); I=(!run||same||done)?0:(rem>0?Math.max(0,1-(mem?0:ndir/5)):0);
    Vnow=(same||done||(rem===0&&nd>0))?0:V0*(mem?1:Math.max(0.05,1-ndir/6));
    if(run&&!same&&!done){ tEv+=dt*speed*I; const iv=1.1; while(tEv>iv){ tEv-=iv; event(); } }
    prop+=I*dt*speed*14;
    ions.forEach(o=>{
      if(o.tg==='dep'){ const tx_=XR+wB/2+8, d=Math.hypot(tx_-o.x,(o.ty||(o.ty=clamp(o.y,PT+20,PB-20)))-o.y); const sp=90*speed; o.x+=(tx_-o.x)/Math.max(d,1)*Math.min(d,sp*dt); o.y+=(o.ty-o.y)/Math.max(d,1)*Math.min(d,sp*dt); if(d<3){ o.dead=1; ndep++; wB=Math.min(46,wB+0.95); flash.push({x:XR+wB/2,y:o.y,t:0,c:B_.col}); } return; }
      if(o.tg==='left'||o.tg==='right'){ const goal=o.tg==='left'?MX-40:MX+40; o.vx=(goal>o.x?1:-1)*55*speed; o.vy*=0.9; if(Math.abs(o.x-goal)<6){ o.tg=null; } }
      else { o.vx+=rnd(-60,60)*dt; o.vy+=rnd(-60,60)*dt; o.vx=clamp(o.vx,-32,32); o.vy=clamp(o.vy,-32,32); }
      const k=run?speed:0.35; o.x+=o.vx*dt*k; o.y+=o.vy*dt*k;
      const r=10, free=!mem||o.tg==='left'||o.tg==='right';
      let lo=BOXL+r, hi=BOXR-r; if(!free){ if(o.x<MX){ hi=MX-r; } else { lo=MX+r; } }
      if(o.x<lo){ o.x=lo; o.vx=Math.abs(o.vx); } if(o.x>hi){ o.x=hi; o.vx=-Math.abs(o.vx); }
      if(o.y<LT+r){ o.y=LT+r; o.vy=Math.abs(o.vy); } if(o.y>LB-r){ o.y=LB-r; o.vy=-Math.abs(o.vy); }
      // 極板とぶつかる
      [-1,1].forEach(sd=>{ const pr=plateRect(sd); if(o.x>pr[0]-r&&o.x<pr[0]+pr[2]+r&&o.y<pr[1]+pr[3]+r){
        // セロハンなし：＋極側の金属イオンが−極の板にふれると、そこで金属になる（直接の反応）
        if(sd<0&&o.t==='B'&&!mem&&run&&V0>0){ o.dead=1; ndir++; spots.push({y:clamp(o.y,PT+8,PB-8),s:o.x<XL?-1:1}); ions.push({t:'A',x:o.x<XL?pr[0]-12:pr[0]+pr[2]+12,y:o.y,vx:rnd(-20,20),vy:rnd(-20,20),tg:null}); wA=Math.max(8,wA-0.9); nd++; flash.push({x:XL,y:o.y,t:0,c:B_.col}); return; }
        const c=pr[0]+pr[2]/2; if(o.x<c){ o.x=pr[0]-r; o.vx=-Math.abs(o.vx); } else { o.x=pr[0]+pr[2]+r; o.vx=Math.abs(o.vx); } } });
    });
    ions=ions.filter(o=>!o.dead);
    flash.forEach(f=>f.t+=dt); flash=flash.filter(f=>f.t<0.6);
    if(run&&!same&&!done&&cntBall()===0&&!ions.some(o=>o.tg==='dep')){ done=true; run=false; syncUI(); }
  }
  function ion(o){ const t=o.t, col=t==='A'?A_.ion:t==='B'?B_.ion:'#ea580c', lab=t==='A'?A_.s+'²⁺':t==='B'?B_.s+'²⁺':'SO₄²⁻', r=t==='S'?11:10;
    ctx.fillStyle=col; ctx.beginPath(); ctx.arc(o.x,o.y,r,0,6.2832); ctx.fill(); ctx.strokeStyle='rgba(255,255,255,.9)'; ctx.lineWidth=1.2; ctx.stroke();
    tx(lab,o.x,o.y+3.5,t==='S'?7.5:8.5,'#fff','center',true); }
  function plate(side,m,w){ const x=side<0?XL:XR; ctx.fillStyle=m.col; ctx.strokeStyle='rgba(0,0,0,.35)'; ctx.lineWidth=1.2;
    ctx.beginPath(); ctx.rect(x-w/2,PT,w,PB-PT); ctx.fill(); ctx.stroke();
    ctx.fillStyle='rgba(255,255,255,.28)'; ctx.fillRect(x-w/2+2,PT+2,Math.max(2,w*0.25),PB-PT-4);
    if(side>0&&ndep>0){ ctx.fillStyle='#9a4a1c'; for(let i=0;i<ndep*6;i++){ const yy=PT+40+((i*53)%(PB-PT-46)), sd=i%2?1:-1; ctx.beginPath(); ctx.arc(x+sd*(w/2),yy,2.2+(i%3),0,6.28); ctx.fill(); } }
    if(side<0) spots.forEach(s=>{ ctx.fillStyle='#9a4a1c'; ctx.beginPath(); ctx.arc(x+s.s*w/2,s.y,6.5,0,6.28); ctx.fill(); });
    tx(m.s,x,PT+18,12,'#111827','center',true); }
  function draw(){
    ctx.clearRect(0,0,W,H); ctx.fillStyle='#f8fafc'; ctx.fillRect(0,0,W,H);
    // 液
    const bAll=cntBall(), bR=cntB();
    const colSide=(m,frac)=>m.solc?'rgba('+m.solc.join(',')+','+(0.08+0.42*frac)+')':'rgba(226,232,240,.55)';
    const fracR=B_.solc?bR/CU0:0, fracL=A_.solc?1:0;
    if(mem){ ctx.fillStyle=colSide(A_,fracL); ctx.fillRect(BOXL,LT,MX-BOXL,LB-LT); ctx.fillStyle=colSide(B_,fracR); ctx.fillRect(MX,LT,BOXR-MX,LB-LT); }
    else { const g=ctx.createLinearGradient(BOXL,0,BOXR,0); g.addColorStop(0,colSide(A_,A_.solc?1:Math.min(1,ions.filter(o=>o.t==='B'&&o.x<MX).length/CU0*1.5))); g.addColorStop(1,colSide(B_,B_.solc?bR/CU0:0)); ctx.fillStyle=g; ctx.fillRect(BOXL,LT,BOXR-BOXL,LB-LT); }
    // 容器
    ctx.strokeStyle='#475569'; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(BOXL-2,LT-30); ctx.lineTo(BOXL-2,LB+2); ctx.lineTo(BOXR+2,LB+2); ctx.lineTo(BOXR+2,LT-30); ctx.stroke();
    if(mem){ ctx.setLineDash([6,5]); ctx.strokeStyle='#0891b2'; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(MX,LT-26); ctx.lineTo(MX,LB); ctx.stroke(); ctx.setLineDash([]); tag('セロハン（小さな穴）',MX,LT-30,11,'#0e7490',null,'center'); }
    else tag('セロハンなし（液がまざる）',MX,LT-30,11,'#b91c1c',null,'center');
    // 極板
    plate(-1,A_,wA); plate(1,B_,wB);
    // 導線
    const wy=WY, yA=PT;
    ctx.strokeStyle='#334155'; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(XL,yA); ctx.lineTo(XL,wy); ctx.lineTo(XR,wy); ctx.lineTo(XR,yA); ctx.stroke();
    // 電子（導線の中を −極 → ＋極）
    const len=(yA-wy)*2+(XR-XL); if(I>0){ const off=(tNow*90*speed*I)%30; for(let s=off;s<len;s+=30){ let x,y; if(s<yA-wy){ x=XL; y=yA-s; } else if(s<yA-wy+XR-XL){ x=XL+(s-(yA-wy)); y=wy; } else { x=XR; y=wy+(s-(yA-wy)-(XR-XL)); }
      if(Math.abs(x-VX)<30&&y===wy||Math.abs(x-PX)<26&&y===wy) continue; ctx.fillStyle='#facc15'; ctx.beginPath(); ctx.arc(x,y,4.5,0,6.28); ctx.fill(); ctx.strokeStyle='#a16207'; ctx.lineWidth=1; ctx.stroke(); } }
    // 電圧計
    ctx.fillStyle='#fff'; ctx.strokeStyle='#334155'; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(VX,wy,26,0,6.28); ctx.fill(); ctx.stroke();
    ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1; ctx.beginPath(); ctx.arc(VX,wy+6,18,Math.PI*1.15,Math.PI*1.85); ctx.stroke();
    const ang=Math.PI*1.15+Math.PI*0.7*clamp(Vnow/3,0,1); ctx.strokeStyle='#dc2626'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(VX,wy+6); ctx.lineTo(VX+Math.cos(ang)*18,wy+6+Math.sin(ang)*18); ctx.stroke();
    tx('V',VX,wy+20,10,'#334155','center',true); tag(Vnow.toFixed(2)+' V',VX,wy+46,12,'#b91c1c',null,'center');
    // モーターとプロペラ
    ctx.fillStyle='#e2e8f0'; ctx.strokeStyle='#334155'; ctx.lineWidth=2; rr(PX-18,wy-12,36,24,5); ctx.fill(); ctx.stroke(); tx('M',PX,wy+5,12,'#334155','center',true);
    ctx.strokeStyle='#334155'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(PX,wy-12); ctx.lineTo(PX,wy-22); ctx.stroke();
    ctx.save(); ctx.translate(PX,wy-24); ctx.scale(1,0.35); ctx.rotate(prop); ctx.fillStyle='#16a34a'; for(let k=0;k<3;k++){ ctx.rotate(2.094); ctx.beginPath(); ctx.ellipse(13,0,13,5,0,0,6.28); ctx.fill(); } ctx.restore();
    tx('光電池用モーター',PX+24,wy-12,10,'#64748b','left',true);
    // 電子と電流の向き
    if(V0>0){ arrow(274,wy-14,374,wy-14,'#ca8a04',2.5,5); tx('電子 e⁻ の流れ →',274,wy-20,10.5,'#a16207','left',true);
      arrow(374,wy+14,274,wy+14,'#dc2626',2.5,5); tx('← 電流の向き（電子と逆）',274,wy+30,10.5,'#dc2626','left',true); }
    // 極のラベル
    const neg=V0>0;
    tag(neg?'−極':'極にならない',XL,PT-8,13,neg?'#1d4ed8':'#64748b',null,'center'); tag(neg?'＋極':'極にならない',XR,PT-8,13,neg?'#b91c1c':'#64748b',null,'center');
    tx(A_.nm+'板',XL+wA/2+6,PT+44,11.5,'#334155','left',true); tx(B_.nm+'板',XR-wB/2-6,PT+44,11.5,'#334155','right',true);
    tag(A_.sol,(XL+MX)/2+8,LB-8,10.5,'#475569',null,'center'); tag(B_.sol,(MX+XR)/2-8,LB-8,10.5,B_.solc?'#1e3a8a':'#475569',null,'center');
    // イオン
    ions.forEach(ion);
    flash.forEach(f=>{ ctx.strokeStyle=f.c; ctx.globalAlpha=1-f.t/0.6; ctx.lineWidth=2.5; ctx.beginPath(); ctx.arc(f.x,f.y,6+f.t*30,0,6.28); ctx.stroke(); ctx.globalAlpha=1; });
    // 反応式
    const y0=432; ctx.fillStyle='#fff'; ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1.2; rr(10,y0-16,W-20,78,10); ctx.fill(); ctx.stroke();
    if(V0>0){ tx('−極（'+A_.nm+'）',22,y0+4,12,'#1d4ed8','left',true); tx(A_.s+' → '+A_.s+'²⁺ ＋ 2e⁻　（とけてイオンになる）',150,y0+4,12.5,'#0f172a','left',true);
      tx('＋極（'+B_.nm+'）',22,y0+24,12,'#b91c1c','left',true); tx(B_.s+'²⁺ ＋ 2e⁻ → '+B_.s+'　（イオンが金属になって付く）',150,y0+24,12.5,'#0f172a','left',true);
      tx('全体',22,y0+44,12,'#475569','left',true); tx(A_.s+' ＋ '+B_.s+'²⁺ → '+A_.s+'²⁺ ＋ '+B_.s,150,y0+44,12.5,'#0f172a','left',true); }
    else { tx('同じ金属どうしでは、イオンへのなりやすさに差がないので、電子が流れない（電圧 0 V）。',22,y0+14,12.5,'#0f172a','left',true); tx('電池にするには、イオンへのなりやすさがちがう2種類の金属が必要。',22,y0+38,12,'#475569','left',true); }
    if(!run&&!done&&nd===0&&V0>0) tag('▶「スタート」か、図をタップ',W/2,LT+40,14,'#0e7490',null,'center');
    if(done) tag(B_.s+'²⁺ がなくなり、電流が止まった',W/2,LT+40,13,'#b45309',null,'center');
    if(!mem&&ndir>0&&!done) tag(B_.s+'²⁺ が −極に直接ついた → 電流が弱くなる',W/2,LT+64,12,'#b91c1c',null,'center');
  }
  function syncUI(){ $('go').textContent=run?'⏸ 一時停止':(done?'⏮ もう一度':'▶ スタート'); $('mem').textContent=mem?'🧻 セロハン：あり':'🚫 セロハン：なし';
    setStat('sV',(V0>0?V0.toFixed(2):'0')+' V');
    setStat('sNeg',V0>0?A_.nm+'（'+A_.s+'）':'なし');
    setStat('sPos',V0>0?B_.nm+'（'+B_.s+'）':'なし');
    setStat('sCnt',V0>0?A_.s+' −'+nd+'個／'+B_.s+' ＋'+ndep+'個':'変化なし');
    setShare(V0>0?'【ダニエル電池】'+A_.nm+'が−極でとけて'+A_.s+'²⁺に、'+B_.nm+'が＋極に付く。電圧は約'+V0.toFixed(2)+' V（理論値）｜シミュラボ':'【ダニエル電池】同じ金属どうしでは電流が流れない（0 V）｜シミュラボ'); }
  let lastStat=0;
  function loop(t){ const dt=Math.min(0.05,(t-(lastT||t))/1000); lastT=t; tNow+=dt; step(dt); draw(); if(t-lastStat>300){ lastStat=t; syncUI(); } requestAnimationFrame(loop); }
  $('go').addEventListener('click',()=>{ if(done){ reset(); run=true; } else run=!run; syncUI(); });
  $('reset').addEventListener('click',()=>{ run=false; reset(); });
  $('mem').addEventListener('click',()=>{ mem=!mem; run=false; reset(); });
  $('pair').addEventListener('change',e=>{ pair=e.target.value; run=false; reset(); });
  $('spd').addEventListener('change',e=>{ speed=+e.target.value; });
  cv.addEventListener('pointerdown',()=>{ if(done){ reset(); run=true; } else run=!run; syncUI(); });
  reset(); requestAnimationFrame(loop);
  window.__dn={get nd(){return nd;},get ndep(){return ndep;},get I(){return I;},start(){run=true;syncUI();},setMem(v){mem=v;reset();},setPair(p){pair=p;reset();},setSpeed(v){speed=v;}};
'''

ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
<p>亜鉛板を硫酸亜鉛水溶液に、銅板を硫酸銅水溶液に入れ、2つの液をセロハンで仕切ってつなぐと、電池（ダニエル電池）になります。このシミュレーションでは、<b>−極の亜鉛がとけて亜鉛イオン Zn²⁺ になり、そのとき出た電子が導線を通って＋極へ流れ、＋極で銅イオン Cu²⁺ が電子を受け取って銅になって付く</b>ようすを、イオンと電子の動きで確かめます。中学校3年 第1分野（6）「化学変化とイオン」の「化学変化と電池」の単元です。</p>
<p>時間がたつと、亜鉛板はやせ、銅板には銅が付いて太り、硫酸銅水溶液の青色がうすくなります。セロハンを外したときや、金属の組み合わせを変えたときと比べられます。</p>

<h2>授業での使い方</h2>
<ul>
<li><b>導入</b>：前の時間の「金属のイオンへのなりやすさ」（硫酸銅水溶液に亜鉛を入れると銅が付く）を思い出し、「この反応で電子が移るなら、導線を通して取り出せないか」と問いかけます。</li>
<li><b>展開</b>：実験のあと、このシミュレーションでイオンと電子の動きを見て、−極・＋極で起きていることを電子 e⁻ を使った式で書きます。</li>
<li><b>まとめ</b>：「セロハンなし」「同じ金属どうし」と比べ、電池になる条件を言葉でまとめます。</li>
</ul>
<p>生徒への問いの例</p>
<ol>
<li>電子は導線の中をどちら向きに流れていますか。電流の向きと同じですか。</li>
<li>しばらく電流を流すと、硫酸銅水溶液の青色がうすくなるのはなぜですか。</li>
<li>セロハンを外すと、なぜプロペラの回り方が弱くなっていくのでしょうか。</li>
</ol>

<h2>しくみ・解説</h2>
<p><b>−極（亜鉛板）</b>：亜鉛原子が電子を2個失って亜鉛イオンになり、水溶液中にとけ出します。</p>
<p style="text-align:center;font-weight:700">Zn → Zn²⁺ ＋ 2e⁻</p>
<p><b>＋極（銅板）</b>：水溶液中の銅イオンが、導線から流れてきた電子を2個受け取って銅原子になり、銅板に付きます。</p>
<p style="text-align:center;font-weight:700">Cu²⁺ ＋ 2e⁻ → Cu</p>
<p>亜鉛は銅よりイオンになりやすいので、亜鉛が電子を出す側（−極）になります。電子は導線の中を−極から＋極へ流れ、<b>電流の向きはその逆（＋極から−極）</b>です。</p>
<p><b>セロハン（素焼きの板）の役目</b>：2つの水溶液がすぐにまざらないようにしながら、小さな穴を通してイオンが少しずつ移動できるようにしています。−極側では陽イオン（Zn²⁺）が増え、＋極側では陽イオン（Cu²⁺）が減るので、そのままでは電気のかたよりが生じます。硫酸イオン SO₄²⁻ が＋極側から−極側へ、Zn²⁺ が−極側から＋極側へセロハンを通って移動することで、電気のかたよりが打ち消され、電流が流れ続けます。</p>
<p>セロハンがないと、銅イオンが亜鉛板に直接ふれて、亜鉛板の上で銅が付く反応が起こります。このとき電子は導線を通らずに移るので、電流として取り出せる量が減ってしまいます。</p>
''' + T([["亜鉛と銅（ダニエル電池）", "亜鉛", "銅", "約1.1 V"],
          ["マグネシウムと銅", "マグネシウム", "銅", "約2.7 V（理論値）"],
          ["マグネシウムと亜鉛", "マグネシウム", "亜鉛", "約1.6 V（理論値）"],
          ["亜鉛と亜鉛／銅と銅", "—", "—", "0 V（電流は流れない）"]],
         ["金属の組み合わせ", "−極", "＋極", "電圧（目安）"]) + N(
    "電圧は、それぞれの金属の標準電極電位の差から求めた理論値（25℃・濃さ1 mol/L のとき）です。実際の実験では、水溶液の濃さや金属の表面の状態（マグネシウムの表面の酸化など）によって、これより小さくなることがあります。図のイオンや原子の数・大きさは、見やすくするために実際とは大きく変えています。") + P(
    "2種類の金属のうち、<b>イオンになりやすい方が−極</b>になります（中学校で調べる順：マグネシウム＞亜鉛＞銅）。") + '''

<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「中学校学習指導要領（平成29年告示）解説 理科編」第1分野（6）化学変化とイオン ア（イ）化学変化と電池（''' + A(MEXT_CHU, "中学校学習指導要領解説") + '''）</li>
<li>中学校理科の教科書（第3学年「化学変化とイオン」の単元：金属のイオンへのなりやすさ、ダニエル電池）</li>
<li>日本化学会 編「化学便覧 基礎編」標準電極電位（Zn²⁺/Zn −0.76 V、Cu²⁺/Cu ＋0.34 V、Mg²⁺/Mg −2.37 V）</li>
</ul>
'''

sim(slug="daniel-denchi", cat="rika", emoji="🔋", score=80,
    title="ダニエル電池のシミュレーター（亜鉛と銅・イオンと電子の動き）",
    title_tag="ダニエル電池のしくみシミュレーター｜−極・＋極の反応式とイオン・電子の動き、セロハンの役目（中3理科）",
    meta_desc="亜鉛板が亜鉛イオンになってとけ、電子が導線を流れ、銅板に銅が付く。ダニエル電池のイオンと電子の動き、電流の向き、セロハンの役目をアニメーションで確かめる中3理科の無料シミュレーター。マグネシウムとの組み合わせや同じ金属どうし、セロハンなしとの比較つき。",
    og_title="ダニエル電池のシミュレーター（亜鉛と銅・イオンと電子の動き）",
    og_desc="亜鉛がとけてZn²⁺に、電子は導線を通って銅板へ、Cu²⁺が銅になって付く。セロハンを通るイオン、プロペラと電圧計の動きまでアニメで。",
    card_desc="亜鉛がとけてZn²⁺に、電子が導線を流れ、銅板に銅が付く。セロハンの役目と−極・＋極の反応式まで動きで。",
    lead="亜鉛板（硫酸亜鉛水溶液）と銅板（硫酸銅水溶液）をセロハンで仕切った「ダニエル電池」です。スタートすると、亜鉛がとけて亜鉛イオンになり、電子が導線を流れてプロペラが回り、銅板に銅が付いていきます。セロハンを通るイオンの動き、電流の向き、−極・＋極の反応式を同時に確かめられます。金属の組み合わせやセロハンのあり・なしも変えられます。",
    model="中3 化学変化と電池（ダニエル電池）",
    level="中学3年",
    unit="中学校 第1分野（6）化学変化とイオン ア（イ）化学変化と電池",
    canvas=canvas(640, 500, light=True),
    controls=select("pair", "金属の組み合わせ（左＝−極側）", [("zn-cu", "亜鉛と銅（ダニエル電池）"), ("mg-cu", "マグネシウムと銅"), ("mg-zn", "マグネシウムと亜鉛"), ("zn-zn", "亜鉛と亜鉛"), ("cu-cu", "銅と銅")])
           + select("spd", "速さ", [("1", "ふつう"), ("2", "速い"), ("0.5", "ゆっくり")]),
    buttons=btn("go", "▶ スタート", True) + btn("mem", "🧻 セロハン：あり") + btn("reset", "⏮ はじめから"),
    stats=stats([("sV", "電圧（理論値）", True), ("sNeg", "−極（とける金属）", False), ("sPos", "＋極（付く金属）", False), ("sCnt", "変化した数", False)]),
    legend="上＝導線（黄色のつぶ＝電子 e⁻、電圧計 V、光電池用モーター M とプロペラ）。下＝容器（点線＝セロハン）。灰色 Zn²⁺ 亜鉛イオン、青 Cu²⁺ 銅イオン、紫 Mg²⁺ マグネシウムイオン、オレンジ SO₄²⁻ 硫酸イオン。硫酸銅水溶液の青色は、銅イオンが減るとうすくなります。図をタップしてもスタート・一時停止できます。",
    article=ARTICLE,
    faqs=[("ダニエル電池の−極と＋極はどちらですか？", "亜鉛板が−極、銅板が＋極です。亜鉛は銅よりイオンになりやすいので、亜鉛が電子を出してとけ（Zn → Zn²⁺ ＋ 2e⁻）、その電子が導線を通って銅板へ流れ、銅イオンが電子を受け取って銅になります（Cu²⁺ ＋ 2e⁻ → Cu）。"),
          ("電子の流れと電流の向きは同じですか？", "逆です。電子は導線の中を−極（亜鉛板）から＋極（銅板）へ流れます。電流の向きは、＋極から−極へと決められているので、電子の流れと反対になります。"),
          ("セロハン（素焼きの板）は何のためにありますか？", "2つの水溶液がすぐにまざらないようにしながら、イオンが少しずつ通れるようにするためです。硫酸イオンなどが移動して電気のかたよりを打ち消すので、電流が流れ続けます。セロハンがないと、銅イオンが亜鉛板に直接ふれて銅が付き、電流として取り出せなくなっていきます。"),
          ("しばらく使うと、亜鉛板・銅板・水溶液はどうなりますか？", "亜鉛板はとけてうすくなり（質量が減る）、銅板には銅が付いて質量が増えます。硫酸銅水溶液は銅イオンが減るので、青色がうすくなります。"),
          ("同じ金属を2枚使うと電池になりますか？", "なりません。同じ金属どうしではイオンへのなりやすさに差がないので、電子が流れず、電圧は0 Vです。電池にするには、イオンへのなりやすさがちがう2種類の金属を使います。"),
          ("ダニエル電池の電圧はどれくらいですか？", "亜鉛と銅のダニエル電池では約1.1 Vです。マグネシウムと銅にするとより大きな電圧になりますが、実験では表面の状態などにより理論値（約2.7 V）より小さくなることがあります。")],
    rel=[("chuwa-ion", "⚗️", "酸・アルカリと中和のシミュレーター"), ("kagaku-shitsuryou", "🧪", "化学変化と質量シミュレーター"),
         ("denki-kairo", "🔌", "電気回路シミュレーター"), ("shuukihyou", "🧪", "さわれる周期表"), ("denryu-jikai", "🧲", "電流と磁界シミュレーター")],
    js=JS)
