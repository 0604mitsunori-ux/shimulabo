# -*- coding: utf-8 -*-
"""理科の授業向けシミュ（高校 生物：酵素）— シミュラボのリクエスト（2026-11-23 受付 e5c88d5372・96f1b9569e／伊藤さん）から
   kouso-hannou-sokudo … 酵素濃度・基質濃度と反応速度（時間と生成物量のグラフ、初速度のグラフ）
   kouso-sogai         … 競争的阻害と非競争的阻害（基質濃度と初速度の3条件比較・Km/Vmax は発展表示）
   生物（2）生命現象と物質 ア（ｱ）細胞と分子 ㋑生命現象とタンパク質（酵素）
   2本とも同じ粒子モデル（ENGINE）で動く。数値の確かめは __test（ページ内）から。"""
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

MEXT_KOU = "https://www.mext.go.jp/a_menu/shotou/new-cs/1407074.htm"
def A(url, label): return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, label)

HELP = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const FF='"Hiragino Sans","Hiragino Kaku Gothic ProN","Noto Sans JP","Yu Gothic UI","Yu Gothic",Meiryo,sans-serif';
  function tx(s,x,y,size,col,align,bold){ ctx.font=(bold?'bold ':'')+size+'px '+FF; ctx.fillStyle=col; ctx.textAlign=align||'left'; ctx.fillText(s,x,y); ctx.textAlign='left'; }
  function tw(s,size,bold){ ctx.font=(bold?'bold ':'')+size+'px '+FF; return ctx.measureText(s).width; }
  function rr(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
  function pill(s,x,y,size,col,bg){ const w=tw(s,size,true)+16; rr(x-w/2,y-size-2,w,size+12,8); ctx.fillStyle=bg||'rgba(255,255,255,.92)'; ctx.fill(); tx(s,x,y+2,size,col,'center',true); }
'''

# ---------------------------------------------------------------- 粒子モデル（2本共通）
ENGINE = r'''
  // ===== 粒子モデル =====
  // 酵素は基質とぶつかると結合し（酵素基質複合体）、TAU 秒ほどで生成物に変えて放す。酵素はくり返し使われる。
  // 阻害剤：comp＝活性部位に結合（基質と取り合い）／non＝別の場所に結合（基質は結合できるが、生成物ができない）。どちらも時間がたつと離れる（可逆）。
  const RE=16, RC=23, TAU=1.2, TI=1.2, OPEN=1.0, VH=300;
  function mkWorld(o){
    const w={t:0,P:0,E:[],S:[],I:[],Pr:[],fx:[],o:o};
    function put(arr,n,sp,ex){ for(let i=0;i<n;i++){ arr.push(Object.assign({x:rnd(24,o.W-24),y:rnd(24,o.H-24),a:rnd(0,6.283),sp:sp,th:rnd(0,6.283),w:rnd(-1.5,1.5)},ex||{})); } }
    function mv(p,dt,R){ p.a+=randn()*Math.sqrt(dt)*1.5; p.x+=Math.cos(p.a)*p.sp*dt; p.y+=Math.sin(p.a)*p.sp*dt; p.th+=p.w*dt;
      if(p.x<R){p.x=R;p.a=Math.PI-p.a;} if(p.x>o.W-R){p.x=o.W-R;p.a=Math.PI-p.a;} if(p.y<R){p.y=R;p.a=-p.a;} if(p.y>o.H-R){p.y=o.H-R;p.a=-p.a;} }
    for(let i=0;i<o.nE;i++){ w.E.push({x:rnd(30,o.W-30),y:rnd(30,o.H-30),a:rnd(0,6.283),sp:13,th:rnd(0,6.283),w:rnd(-.35,.35),st:0,tc:0,tc0:1,inh:false,ti:0,cool:0,op:OPEN,bk:0}); }
    put(w.I,o.nI||0,130);
    w.step=function(dt){
      w.t+=dt;
      const E=w.E,S=w.S,I=w.I,non=o.mode==='non',comp=o.mode==='comp';
      for(const e of E){
        mv(e,dt,RE+3);
        if(e.cool>0) e.cool-=dt;
        if(e.inh){ e.ti-=dt; if(e.ti<=0){ e.inh=false; const d=comp?e.th:e.th+Math.PI; I.push({x:e.x+Math.cos(d)*(RE+9),y:e.y+Math.sin(d)*(RE+9),a:d+rnd(-.5,.5),sp:130,th:d,w:rnd(-1.5,1.5)}); e.cool=Math.max(e.cool,.25); } }
        if(e.st===1 && !(non&&e.inh)){ e.tc-=dt; if(e.tc<=0){ e.st=0; e.cool=.18; w.P++; const d=e.th+rnd(-.3,.3);
            w.Pr.push({x:e.x+Math.cos(e.th)*(RE+6),y:e.y+Math.sin(e.th)*(RE+6),a:d,sp:55,th:e.th,w:rnd(-1.5,1.5)});
            if(o.fx) w.fx.push({x:e.x+Math.cos(e.th)*RE,y:e.y+Math.sin(e.th)*RE,t:w.t}); } }
      }
      for(let i=S.length-1;i>=0;i--){ const s=S[i]; mv(s,dt,9);
        for(const e of E){ if(e.st!==0||e.cool>0||(comp&&e.inh)) continue; const dx=s.x-e.x,dy=s.y-e.y; if(dx*dx+dy*dy<RC*RC){ e.st=1; e.tc0=e.tc=rnd(TAU-.2,TAU+.2); e.bk=0; S.splice(i,1); break; } } }
      for(let i=I.length-1;i>=0;i--){ const s=I[i]; mv(s,dt,9);
        for(const e of E){ if(e.inh||e.cool>0) continue; if(comp&&e.st!==0) continue; const dx=s.x-e.x,dy=s.y-e.y; if(dx*dx+dy*dy<RC*RC){ e.inh=true; e.ti=-Math.log(1-Math.random())*TI; e.bk=0; I.splice(i,1); break; } } }
      for(const p of w.Pr) mv(p,dt,9);
      if(o.fx&&w.fx.length&&w.t-w.fx[0].t>.7) w.fx.shift();
    };
    // 阻害剤は、基質を入れる前に酵素とまぜておく（結合と解離がつり合った状態から始める）
    if(o.nI>0&&o.mode!=='none'){ for(let k=0;k<480;k++) w.step(1/60); w.t=0; w.fx.length=0; }
    put(w.S,o.nS,95);
    w.bound=function(){ let n=0; for(const e of w.E) if(e.st===1) n++; return n; };
    w.inhib=function(){ let n=0; for(const e of w.E) if(e.inh) n++; return n; };
    return w;
  }
  // 反応開始直後の反応速度（個/秒）。T0〜T1 秒にできた生成物の数から求める。trials 回の平均。
  const T0=1.4, T1=3.9;
  function measure(nE,nS,nI,mode,trials){ let v=0; for(let k=0;k<trials;k++){ const w=mkWorld({nE:nE,nS:nS,nI:nI,mode:mode,W:W,H:VH,fx:false}); let p0=0,got=false;
      while(w.t<T1){ w.step(1/60); if(!got&&w.t>=T0){p0=w.P;got=true;} } v+=(w.P-p0)/(T1-T0); } return v/trials; }

  // ===== 描く =====
  function wedge(x,y,r,rot,open){ ctx.beginPath(); ctx.moveTo(x,y); ctx.arc(x,y,r,rot-open/2,rot+open/2); ctx.closePath(); }
  function dSub(x,y,rot,k,sc){ // k=0 基質 → 1 生成物（2つに分かれた形）
    const r=13*(sc||1);
    if(k<.5){ wedge(x,y,r,rot,OPEN-.1); ctx.fillStyle='#f59e0b'; ctx.fill(); ctx.strokeStyle='#b45309'; ctx.lineWidth=1.2; ctx.stroke();
      if(k>0){ ctx.strokeStyle='rgba(120,53,15,'+(k*2)+')'; ctx.lineWidth=1.4; ctx.beginPath(); ctx.moveTo(x,y); ctx.lineTo(x+Math.cos(rot)*r,y+Math.sin(rot)*r); ctx.stroke(); } }
    else { const g=(k-.5)*2*3.2+1.2, h=(OPEN-.1)/2; for(const sgn of [-1,1]){ const rr2=rot+sgn*h/2, ox=Math.cos(rot+sgn*1.57)*g, oy=Math.sin(rot+sgn*1.57)*g;
        wedge(x+ox,y+oy,r,rr2,h-.04); ctx.fillStyle='#22c55e'; ctx.fill(); ctx.strokeStyle='#15803d'; ctx.lineWidth=1.2; ctx.stroke(); } }
  }
  function dProd(p){ const ax=p.x-Math.cos(p.th)*7, ay=p.y-Math.sin(p.th)*7; dSub(ax,ay,p.th,1,.92); }
  function dFreeSub(p){ dSub(p.x-Math.cos(p.th)*7,p.y-Math.sin(p.th)*7,p.th,0,.92); }
  function dInhC(x,y,rot,sc){ const r=13*(sc||1); wedge(x,y,r,rot,OPEN-.1); ctx.fillStyle='#a855f7'; ctx.fill(); ctx.strokeStyle='#6b21a8'; ctx.lineWidth=1.2; ctx.stroke();
    ctx.beginPath(); ctx.arc(x+Math.cos(rot)*r,y+Math.sin(rot)*r,4.2,0,7); ctx.fillStyle='#6b21a8'; ctx.fill(); }
  function dInhN(x,y,rot){ ctx.beginPath(); for(let i=0;i<6;i++){ const a=rot+i*Math.PI/3; ctx.lineTo(x+Math.cos(a)*8,y+Math.sin(a)*8); } ctx.closePath(); ctx.fillStyle='#a855f7'; ctx.fill(); ctx.strokeStyle='#6b21a8'; ctx.lineWidth=1.3; ctx.stroke(); }
  function dFreeInh(p,mode){ if(mode==='comp') dInhC(p.x-Math.cos(p.th)*7,p.y-Math.sin(p.th)*7,p.th,.92); else dInhN(p.x,p.y,p.th); }
  function dEnz(e,mode,t){
    const non=mode==='non', comp=mode==='comp';
    const tgt=(non&&e.inh)?.5:OPEN; e.op+=(tgt-e.op)*.18; e.bk=Math.min(1,e.bk+.09);
    const act=e.st===1&&!(non&&e.inh), blocked=e.inh;
    ctx.save();
    if(act){ ctx.shadowColor='rgba(245,158,11,.9)'; ctx.shadowBlur=10+6*Math.sin(t*9); }
    ctx.beginPath(); ctx.arc(e.x,e.y,RE,e.th+e.op/2,e.th-e.op/2+Math.PI*2); ctx.lineTo(e.x+Math.cos(e.th)*2,e.y+Math.sin(e.th)*2); ctx.closePath();
    const g=ctx.createRadialGradient(e.x-5,e.y-6,2,e.x,e.y,RE+2);
    if(blocked){ g.addColorStop(0,'#e2e8f0'); g.addColorStop(1,'#94a3b8'); } else { g.addColorStop(0,'#93c5fd'); g.addColorStop(1,'#2563eb'); }
    ctx.fillStyle=g; ctx.fill(); ctx.restore();
    ctx.strokeStyle=blocked?'#475569':'#1e3a8a'; ctx.lineWidth=1.6; ctx.stroke();
    if(e.st===1){ const k=act?Math.max(0,Math.min(.49,(1-e.tc/e.tc0)*.5)):0, sc=.55+.45*e.bk;
      ctx.save(); if(e.op<OPEN-.05){ ctx.globalAlpha=.75; } dSub(e.x+Math.cos(e.th)*(1-e.bk)*10,e.y+Math.sin(e.th)*(1-e.bk)*10,e.th,k,sc*(e.op<OPEN-.05?.8:1)); ctx.restore();
      if(act){ ctx.strokeStyle='#f59e0b'; ctx.lineWidth=2.5; ctx.beginPath(); ctx.arc(e.x,e.y,RE+4,-1.57,-1.57+(1-e.tc/e.tc0)*6.283); ctx.stroke(); } }
    if(e.inh){ if(comp) dInhC(e.x+Math.cos(e.th)*(1-e.bk)*10,e.y+Math.sin(e.th)*(1-e.bk)*10,e.th,.55+.45*e.bk);
      else { const d=e.th+Math.PI, q=RE+6+(1-e.bk)*8; dInhN(e.x+Math.cos(d)*q,e.y+Math.sin(d)*q,d);
        if(e.st===1){ ctx.strokeStyle='#dc2626'; ctx.lineWidth=2.2; const cx=e.x+Math.cos(e.th)*8,cy=e.y+Math.sin(e.th)*8; ctx.beginPath(); ctx.moveTo(cx-4,cy-4); ctx.lineTo(cx+4,cy+4); ctx.moveTo(cx+4,cy-4); ctx.lineTo(cx-4,cy+4); ctx.stroke(); } } }
  }
  function dVessel(w,mode){
    const g=ctx.createLinearGradient(0,0,0,VH); g.addColorStop(0,'#f0f9ff'); g.addColorStop(1,'#dbeafe'); ctx.fillStyle=g; ctx.fillRect(0,0,W,VH);
    for(const p of w.Pr) dProd(p);
    for(const p of w.S) dFreeSub(p);
    for(const p of w.I) dFreeInh(p,mode);
    for(const e of w.E) dEnz(e,mode,w.t);
    for(const f of w.fx){ const k=(w.t-f.t)/.7; if(k<0||k>1) continue; ctx.strokeStyle='rgba(34,197,94,'+(1-k)+')'; ctx.lineWidth=3*(1-k)+.5; ctx.beginPath(); ctx.arc(f.x,f.y,6+k*26,0,7); ctx.stroke();
      for(let i=0;i<6;i++){ const a=i*1.047+f.t*7, r1=10+k*24; ctx.fillStyle='rgba(250,204,21,'+(1-k)+')'; ctx.beginPath(); ctx.arc(f.x+Math.cos(a)*r1,f.y+Math.sin(a)*r1,2.2*(1-k)+.4,0,7); ctx.fill(); } }
    ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1; ctx.strokeRect(.5,.5,W-1,VH-1);
  }
  function dLegend(items){ // [[kind,label],...]
    let x=10; const y=10, h=26; let wsum=10; for(const it of items) wsum+=30+tw(it[1],12,true)+10;
    rr(6,6,wsum,h+2,8); ctx.fillStyle='rgba(255,255,255,.9)'; ctx.fill(); ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1; ctx.stroke(); x=14;
    for(const it of items){ const cy=y+h/2-1;
      if(it[0]==='E'){ ctx.beginPath(); ctx.arc(x+10,cy,9,.5,-.5+6.283); ctx.lineTo(x+11,cy); ctx.closePath(); ctx.fillStyle='#3b82f6'; ctx.fill(); ctx.strokeStyle='#1e3a8a'; ctx.lineWidth=1.2; ctx.stroke(); }
      if(it[0]==='S') dSub(x+3,cy,0,0,.95);
      if(it[0]==='P') dSub(x+3,cy,0,1,.95);
      if(it[0]==='IC') dInhC(x+3,cy,0,.9);
      if(it[0]==='IN') dInhN(x+10,cy,0);
      tx(it[1],x+24,cy+4,12,'#0f172a','left',true); x+=30+tw(it[1],12,true)+10; }
  }
  // グラフの枠。戻り値は座標変換
  function frame(x,y,w,h,xmax,ymax,xl,yl,xt,yt){
    rr(x,y,w,h,10); ctx.fillStyle='#fff'; ctx.fill(); ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; ctx.stroke();
    const L=x+42,R=x+w-14,Tp=y+28,B=y+h-34; const X=v=>L+v/xmax*(R-L), Y=v=>B-v/ymax*(B-Tp);
    ctx.strokeStyle='#eef2f7'; ctx.lineWidth=1; for(let i=1;i<=4;i++){ const yy=B-(B-Tp)*i/4; ctx.beginPath(); ctx.moveTo(L,yy); ctx.lineTo(R,yy); ctx.stroke(); }
    ctx.strokeStyle='#334155'; ctx.lineWidth=1.4; ctx.beginPath(); ctx.moveTo(L,Tp-4); ctx.lineTo(L,B); ctx.lineTo(R+2,B); ctx.stroke();
    for(let i=0;i<=4;i++){ const v=ymax*i/4; tx(yt?yt(v):(ymax<10?v.toFixed(1):String(Math.round(v))),L-5,B-(B-Tp)*i/4+4,11,'#475569','right'); }
    for(let i=0;i<=4;i++){ const v=xmax*i/4; tx(xt?xt(v):String(Math.round(v)),L+(R-L)*i/4,B+14,11,'#475569','center'); }
    tx(xl,(L+R)/2,y+h-4,12,'#0f172a','center',true); tx(yl,x+8,y+16,12,'#0f172a','left',true);
    return {X:X,Y:Y,L:L,R:R,T:Tp,B:B};
  }
  function nice(v){ const p=Math.pow(10,Math.floor(Math.log10(v))); const m=v/p; return (m<=1?1:m<=1.2?1.2:m<=1.6?1.6:m<=2?2:m<=2.4?2.4:m<=3.2?3.2:m<=4?4:m<=6?6:m<=8?8:10)*p; }
'''

# ============================================================ 1 酵素の反応速度
SOKUDO_JS = HELP + ENGINE + r'''
  const COLS=['#db2777','#7c3aed','#d97706','#0891b2','#65a30d'];
  let world, paused=false, data=[], runs=[], ptsS=[], ptsE=[], rec=0, p0=0, queue=[], fcount=0, doneMsg=false, sweeping='';
  function cond(){ return {nE:+$('nE').value,nS:+$('nS').value}; }
  function start(){ const c=cond(); world=mkWorld({nE:c.nE,nS:c.nS,nI:0,mode:'none',W:W,H:VH,fx:true}); data=[[0,0]]; rec=0; p0=0; paused=false; doneMsg=false; $('pause').textContent='⏸ 一時停止'; }
  function addPt(list,p){ for(let i=list.length-1;i>=0;i--) if(list[i].x===p.x&&list[i].k===p.k) list.splice(i,1); p.born=performance.now(); list.push(p); }
  function rateNow(){ if(data.length<3) return 0; const b=data[data.length-1]; let a=data[0]; for(let i=data.length-1;i>=0;i--){ if(b[0]-data[i][0]>=1.5){a=data[i];break;} } return b[0]>a[0]?(b[1]-a[1])/(b[0]-a[0]):0; }
  function tick(dt){
    world.step(dt);
    const last=data[data.length-1]; if(world.t-last[0]>=.2) data.push([world.t,world.P]);
    if(rec===0&&world.t>=T0){ p0=world.P; rec=1; }
    if(rec===1&&world.t>=T1){ rec=2; const v=(world.P-p0)/(T1-T0), c=world.o; addPt(ptsS,{x:c.nS,k:c.nE,v:v}); addPt(ptsE,{x:c.nE,k:c.nS,v:v}); }
    if(!doneMsg&&world.S.length===0&&world.bound()===0){ doneMsg=true; data.push([world.t,world.P]); }
  }
  function series(list){ const ks=[]; for(const p of list) if(ks.indexOf(p.k)<0) ks.push(p.k); return ks; }
  function drawTime(){
    let tmax=20, pmax=20; const all=runs.concat([{data:data,nS:world.o.nS}]);
    for(const r of all){ tmax=Math.max(tmax,r.data[r.data.length-1][0]); pmax=Math.max(pmax,r.nS); }
    tmax=Math.ceil(tmax/20)*20; pmax=nice(pmax);
    const f=frame(6,VH+10,312,H-VH-16,tmax,pmax,'時間（秒）','生成物の量（個）');
    function line(d,col,lw){ ctx.strokeStyle=col; ctx.lineWidth=lw; ctx.lineJoin='round'; ctx.beginPath(); d.forEach((q,i)=>{ const x=f.X(q[0]),y=f.Y(q[1]); i?ctx.lineTo(x,y):ctx.moveTo(x,y); }); ctx.stroke(); }
    runs.forEach((r,i)=>{ line(r.data,r.col,1.8); const q=r.data[r.data.length-1]; tx(r.label,Math.min(f.R-2,f.X(q[0])),f.Y(q[1])-5-(i%2)*11,10.5,r.col,'right',true); });
    line(data,'#0d9488',3);
    const q=data[data.length-1], v=rateNow(), x=f.X(q[0]), y=f.Y(q[1]);
    if(data.length>3){ const sx=(f.R-f.L)/tmax, sy=(f.B-f.T)/pmax, dx=34, dy=v*dx/sx*sy; const n=Math.hypot(dx,dy)/34; ctx.strokeStyle='#ef4444'; ctx.lineWidth=2; ctx.setLineDash([5,3]); ctx.beginPath(); ctx.moveTo(x-dx/n,y+dy/n); ctx.lineTo(x+dx/n,y-dy/n); ctx.stroke(); ctx.setLineDash([]); }
    ctx.fillStyle='#0d9488'; ctx.beginPath(); ctx.arc(x,y,4.5,0,7); ctx.fill(); ctx.strokeStyle='#fff'; ctx.lineWidth=1.5; ctx.stroke();
    tx('赤い点線の傾き＝いまの反応速度 '+v.toFixed(1)+' 個/秒',f.L+8,f.T+4,10.5,'#dc2626','left',true);
    if(doneMsg){ ctx.strokeStyle='#94a3b8'; ctx.setLineDash([3,3]); ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(f.L,f.Y(world.P)); ctx.lineTo(f.R,f.Y(world.P)); ctx.stroke(); ctx.setLineDash([]); }
  }
  function drawV0(){
    const isS=$('gsel').value==='S', list=isS?ptsS:ptsE, xmax=isS?160:20;
    let vmax=4; for(const p of list) vmax=Math.max(vmax,p.v*1.15); vmax=nice(vmax);
    const f=frame(322,VH+10,312,H-VH-16,xmax,vmax,isS?'はじめの基質の数（基質濃度）':'酵素の数（酵素濃度）','反応開始直後の反応速度（個/秒）');
    const ks=series(list), now=performance.now(), c=cond();
    ks.forEach((k,i)=>{ const col=COLS[i%COLS.length], pts=list.filter(p=>p.k===k).sort((a,b)=>a.x-b.x);
      if(pts.length>=3){ ctx.strokeStyle=col; ctx.lineWidth=2; ctx.globalAlpha=.75; ctx.beginPath(); ctx.moveTo(f.X(0),f.Y(0)); pts.forEach(p=>ctx.lineTo(f.X(p.x),f.Y(p.v))); ctx.stroke(); ctx.globalAlpha=1; }
      pts.forEach(p=>{ const a=Math.min(1,(now-p.born)/350), r=4.5+(1-a)*9; ctx.fillStyle=col; ctx.globalAlpha=.35+.65*a; ctx.beginPath(); ctx.arc(f.X(p.x),f.Y(p.v),r,0,7); ctx.fill(); ctx.globalAlpha=1; ctx.strokeStyle='#fff'; ctx.lineWidth=1.2; ctx.stroke(); });
      const lp=pts[pts.length-1]; tx(isS?('酵素'+k+'個'):('基質'+k+'個'),Math.min(f.R,f.X(lp.x)+4),f.Y(lp.v)-8,10.5,col,'right',true); });
    const cx=f.X(isS?c.nS:c.nE); ctx.strokeStyle='#0d9488'; ctx.setLineDash([3,3]); ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(cx,f.T); ctx.lineTo(cx,f.B); ctx.stroke(); ctx.setLineDash([]);
    if(!list.length) tx('反応を始めて約4秒たつと、点が1つ入ります',(f.L+f.R)/2,(f.T+f.B)/2,11.5,'#64748b','center');
    if(sweeping) pill('自動で測定中… '+sweeping,(f.L+f.R)/2,f.T+14,11,'#0f172a','rgba(254,243,199,.95)');
  }
  function draw(){
    ctx.clearRect(0,0,W,H); ctx.fillStyle='#f8fafc'; ctx.fillRect(0,0,W,H);
    dVessel(world,'none');
    dLegend([['E','酵素'],['S','基質'],['P','生成物']]);
    const b=world.bound(), n=world.E.length, gw=150, gx=W-gw-12, gy=VH-26;
    rr(gx-8,gy-18,gw+16,38,8); ctx.fillStyle='rgba(255,255,255,.9)'; ctx.fill();
    tx('基質と結合している酵素 '+b+'/'+n,gx,gy-4,11,'#0f172a','left',true);
    rr(gx,gy+2,gw,9,4); ctx.fillStyle='#e2e8f0'; ctx.fill(); if(b>0){ rr(gx,gy+2,Math.max(9,gw*b/n),9,4); ctx.fillStyle='#f59e0b'; ctx.fill(); }
    if(doneMsg) pill('基質を使い切りました（生成物 '+world.P+' 個）',W/2,VH/2,14,'#0f172a','rgba(255,255,255,.95)');
    else if(paused) pill('一時停止中',W/2,VH/2,14,'#0f172a','rgba(255,255,255,.95)');
    drawTime(); drawV0();
    const v=rateNow();
    setStat('sT',world.t.toFixed(1)+' 秒'); setStat('sP',world.P+' 個'); setStat('sS',(world.S.length+b)+' 個'); setStat('sV',v.toFixed(1)+' 個/秒'); setStat('sB',b+' / '+n);
    setShare('【酵素の反応速度】酵素'+world.o.nE+'個・基質'+world.o.nS+'個で反応させると、'+world.t.toFixed(0)+'秒で生成物が'+world.P+'個できた｜シミュラボ');
  }
  function loop(){
    fcount++;
    if(!paused&&!doneMsg){ const sp=+$('spd').value; const n=Math.max(1,Math.round(sp*2)); for(let i=0;i<n;i++) tick(1/120); }
    if(queue.length&&fcount%5===0){ queue.shift()(); if(!queue.length) sweeping=''; }
    draw(); requestAnimationFrame(loop);
  }
  $('go').addEventListener('click',start);
  $('pause').addEventListener('click',()=>{ paused=!paused; $('pause').textContent=paused?'▶ 再開':'⏸ 一時停止'; });
  $('keep').addEventListener('click',()=>{ if(data.length<5) return; if(runs.length>=5) runs.shift(); const c=world.o; runs.push({label:'酵素'+c.nE+'・基質'+c.nS,col:COLS[runs.length%COLS.length],data:data.slice(),nS:c.nS}); runs.forEach((r,i)=>r.col=COLS[i%COLS.length]); });
  $('sweep').addEventListener('click',()=>{ if(queue.length) return; const c=cond();
    if($('gsel').value==='S'){ [5,10,20,35,50,75,100,125,150].forEach(s=>queue.push(()=>{ sweeping='基質'+s+'個'; addPt(ptsS,{x:s,k:c.nE,v:measure(c.nE,s,0,'none',14)}); })); }
    else { [1,2,4,6,8,10,13,16,20].forEach(e=>queue.push(()=>{ sweeping='酵素'+e+'個'; addPt(ptsE,{x:e,k:150,v:measure(e,150,0,'none',14)}); })); } });
  $('clr').addEventListener('click',()=>{ runs=[]; ptsS=[]; ptsE=[]; });
  $('nE').addEventListener('change',start); $('nS').addEventListener('change',start);
  window.__test={measure:measure,mk:mkWorld,get world(){return world;},tick:function(n){ for(let i=0;i<n;i++) tick(1/60); while(queue.length) queue.shift()(); sweeping=''; draw(); }};
  start(); loop();
'''

SOKUDO_ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
<p>酵素は、基質と結合して<b>酵素基質複合体</b>をつくり、基質を生成物に変えて放します。酵素そのものは変化しないので、くり返し働きます。このシミュレーターでは、酵素と基質の数を変えて、粒子の動きと「時間と生成物の量」のグラフ、「濃度と反応開始直後の反応速度」のグラフを同時に見ることができます。</p>
''' + N('<b>対応する単元</b>：高等学校「生物」（2）生命現象と物質 ア（ｱ）細胞と分子「㋑生命現象とタンパク質」。学習指導要領解説では、タンパク質が生命現象を支えている例として、生体触媒である酵素を取り上げることが示されています。「生物基礎」（1）の「生物とエネルギー」（酵素の基質特異性）の発展としても使えます。') + '''
<h2>授業での使い方</h2>
<h3>導入：グラフの傾きは何を表すか</h3>
<p>まず酵素6個・基質60個で反応を始め、左のグラフを見ます。生成物ははじめ速く増え、基質が減るにつれて増え方がゆるやかになり、基質を使い切ると水平になります。赤い点線（接線）の傾きが、その時点の<b>反応速度</b>です。「グラフが水平になった＝反応速度が0になった」であり、「生成物がなくなった」ではないことを確かめます。</p>
<h3>展開1：酵素を増やすと何が変わるか</h3>
<p>「📌 この結果を残す」を押してから、基質の数はそのままで酵素を12個に増やして、もう一度反応させます。生成物は速く増えますが、最後の量は同じです。生成物の最終量を決めているのは基質の量だからです。次に、酵素はそのままで基質を120個に増やすと、最終量が2倍になります。</p>
<h3>展開2：反応速度が頭打ちになる理由</h3>
<p>右のグラフを「基質濃度と反応速度」にして「⚡ 自動で測定」を押すと、基質の数を変えたときの反応開始直後の反応速度が次々に点で入ります。基質が少ないうちは基質を増やすほど速くなりますが、やがて頭打ちになります。このとき基質を150個にして反応させ、画面右下の「基質と結合している酵素」を見ると、ほとんどの酵素が基質と結合しています。酵素が1回の反応にかける時間は決まっているので、すべての酵素がふさがると、それ以上は速くなりません。</p>
<p>右のグラフを「酵素濃度と反応速度」にして自動で測定すると、基質が十分にあるとき（150個）、反応速度は酵素の数にほぼ比例します。</p>
<h3>生徒への問いの例</h3>
<ol>
<li>酵素を2倍にすると、反応が終わるまでの時間と、最後にできる生成物の量はそれぞれどうなるだろう？</li>
<li>時間と生成物の量のグラフが水平になったとき、反応液の中では何が起きているだろう？</li>
<li>基質をどんどん増やしても、反応速度がそれ以上大きくならなくなるのはなぜだろう？そのとき酵素はどんな状態だろう？</li>
</ol>
<h2>しくみ・解説</h2>
<h3>用語</h3>
<ul>
<li><b>酵素</b>とは、生体内の化学反応を速める触媒としてはたらくタンパク質です。反応の前後で酵素自身は変化しません。</li>
<li><b>基質</b>とは、酵素が作用する相手の物質です。酵素は特定の基質にだけ作用します（<b>基質特異性</b>）。</li>
<li><b>活性部位</b>とは、酵素の中で基質が結合し、反応が起こる部分です。</li>
<li><b>酵素基質複合体</b>とは、酵素の活性部位に基質が結合したものです。</li>
<li><b>反応速度</b>とは、単位時間あたりにできる生成物の量（または減る基質の量）です。時間と生成物の量のグラフでは、接線の傾きにあたります。</li>
</ul>
<h3>条件を変えたときのまとめ</h3>
''' + T([["酵素濃度を2倍（基質濃度は同じ）", "ほぼ2倍（基質が十分なとき）", "変わらない", "短くなる"],
          ["基質濃度を2倍（酵素濃度は同じ）", "大きくなるが、やがて頭打ち", "2倍になる", "長くなる"]],
         ["変えた条件", "反応開始直後の反応速度", "生成物の最終量", "反応が終わるまでの時間"]) + '''
<h3>反応速度が頭打ちになる理由</h3>
<p>反応は「酵素＋基質 → 酵素基質複合体 → 酵素＋生成物」の順に進みます。基質濃度が低いときは、酵素が基質と出会うまでの待ち時間が長く、基質を増やすと出会いが増えて反応速度が上がります。基質濃度が十分に高いと、酵素は生成物を放すとすぐ次の基質と結合するので、ほぼすべての酵素が酵素基質複合体になっています。この状態の反応速度が<b>最大反応速度</b>で、酵素の数と、酵素が1回の反応にかける時間で決まります。</p>
''' + P('生成物の<b>量</b>と反応<b>速度</b>を区別することが大切です。酵素を増やすと「速く」なりますが、基質の量が同じなら、できる生成物の「量」は変わりません。') + '''
<h3>このシミュレーターのモデル</h3>
<p>一定の広さ（体積）の容器の中を、酵素と基質がランダムに動きます。基質が空いている酵素にぶつかると結合し、約1.2秒後に生成物になって放されます。温度とpHは一定で、生成物から基質にもどる逆向きの反応や、生成物による阻害は考えていません。粒子の数が少ないため、同じ条件でも結果は毎回少しずつちがいます。自動で測定した点は、14回の平均です。分子の大きさ・形・数は、見やすいように大きく単純にしてあります。</p>
<h2>参考</h2>
<ul>
<li>''' + A(MEXT_KOU, "文部科学省 高等学校学習指導要領（平成30年告示）解説 理科編") + '''（生物（2）生命現象と物質）</li>
<li>高等学校「生物」「生物基礎」の教科書（酵素の性質、酵素反応の速度）</li>
</ul>
'''

sim(slug="kouso-hannou-sokudo", cat="rika", emoji="⚗️", score=80,
    title="酵素の反応速度シミュレーター（酵素濃度・基質濃度と反応速度のグラフ）",
    title_tag="酵素の反応速度シミュレーター｜酵素濃度・基質濃度と反応速度、時間と生成物量のグラフ（高校生物）",
    meta_desc="酵素と基質の数を変えると、酵素基質複合体ができて生成物が増えていく様子と、時間と生成物量のグラフが同時に動くシミュレーター。酵素を増やすと速くなるが最終量は同じ、基質を増やすと反応速度が頭打ちになることを、粒子の動きとグラフで確かめられます。",
    og_title="酵素の反応速度シミュレーター（酵素濃度・基質濃度と反応速度のグラフ）",
    og_desc="酵素が基質をつかまえて、生成物に変えて放す。酵素を増やすと速くなるのに最終量は同じ。基質を増やすと反応速度は頭打ち。粒子の動きとグラフが同時に動くので、グラフがその形になる理由が見える。",
    card_desc="酵素と基質の数を変えて、生成物が増えるグラフと反応速度の頭打ちを、粒子の動きといっしょに確かめる。",
    lead="青い丸が酵素、オレンジのくさび形が基質、緑が生成物です。基質が酵素の活性部位（切れこみ）にはまると酵素基質複合体になり、しばらくすると生成物になって離れ、酵素はまた次の基質と反応します。酵素と基質の数を変えて、生成物の増え方と反応速度がどう変わるかを、粒子の動きとグラフで比べてみましょう。",
    model="生物 細胞と分子（酵素：酵素濃度・基質濃度と反応速度）",
    level="高校（生物）、生物基礎の発展",
    unit="高等学校 生物（2）生命現象と物質 ア（ｱ）細胞と分子 ㋑生命現象とタンパク質",
    canvas=canvas(640, 590, light=True),
    controls=slider("nE", "酵素の数（酵素濃度）", 1, 20, 6, 1, "{v} 個")
             + slider("nS", "基質の数（基質濃度）", 10, 150, 60, 5, "{v} 個")
             + select("gsel", "右のグラフ", [("S", "基質濃度と反応速度"), ("E", "酵素濃度と反応速度（基質は150個）")])
             + select("spd", "速さ", [("1", "×1"), ("2", "×2"), ("4", "×4"), ("0.5", "×0.5（ゆっくり）")]),
    buttons=btn("go", "▶ 反応を始める（はじめから）", True) + btn("pause", "⏸ 一時停止") + btn("keep", "📌 この結果を残す") + btn("sweep", "⚡ 自動で測定") + btn("clr", "🧹 グラフを消す"),
    stats=stats([("sT", "時間", False), ("sP", "生成物", True), ("sS", "残りの基質", False), ("sV", "いまの反応速度", True), ("sB", "基質と結合している酵素", False)]),
    legend="青＝酵素（切れこみが活性部位）、オレンジ＝基質、緑＝生成物。酵素のまわりの光と輪は、反応が進んでいるしるしです。左のグラフは時間と生成物の量、右のグラフは反応開始直後（1.4〜3.9秒）の反応速度。スライダーを動かすと、新しい条件ではじめから反応します。",
    article=SOKUDO_ARTICLE,
    faqs=[("酵素を増やすと、できる生成物の量も増えるの？", "増えません。酵素を増やすと反応は速くなりますが、基質の量が同じなら、基質を使い切ったときの生成物の量は同じです。酵素は反応の前後で変化せず、くり返し使われる触媒だからです。生成物の最終量は基質の量で決まります。"),
          ("基質濃度を高くしても反応速度が頭打ちになるのはなぜ？", "基質濃度が十分に高いと、ほぼすべての酵素が基質と結合して酵素基質複合体になっています。酵素が1回の反応にかける時間は決まっているので、空いている酵素がない状態では、基質をそれ以上増やしても反応速度は大きくなりません。このときの速度を最大反応速度といいます。"),
          ("時間と生成物の量のグラフが水平になるのはどういう意味？", "基質がすべて生成物に変わり、反応が終わったことを表します。グラフの傾きは反応速度なので、水平は反応速度が0という意味です。酵素がこわれたわけではなく、基質を加えればまた反応が進みます。"),
          ("反応速度はグラフのどこから読み取るの？", "時間と生成物の量のグラフの傾きが反応速度です。反応開始直後は基質がまだ多く、傾きがほぼ一定なので、この部分の傾きを「反応開始直後の反応速度（初速度）」として、酵素濃度や基質濃度との関係を調べます。"),
          ("酵素濃度と反応速度が比例するのはどんなとき？", "基質が十分にあるときです。どの酵素もすぐに次の基質と結合できるので、酵素の数が2倍になれば、単位時間にできる生成物も2倍になります。基質が少ないと、基質がすぐに減ってしまい、比例からはずれます。"),
          ("同じ条件なのに結果が毎回少しちがうのはなぜ？", "このシミュレーターは粒子1個1個のランダムな動きを計算しており、粒子の数が実際の反応液よりはるかに少ないためです。実際の実験では分子の数が非常に多いので、ばらつきは平均されて見えなくなります。")],
    rel=[("kouso-sogai", "🔒", "酵素の阻害シミュレーター"), ("maku-yuso", "🚪", "膜輸送のシミュレーター"),
         ("rinshishitsu-maku", "🧼", "リン脂質と細胞膜のでき方シミュレーター"), ("kouso-shikkatsu", "🌡️", "酵素の失活シミュレーター"), ("diffusion", "🫧", "拡散シミュレーター")],
    js=SOKUDO_JS)


# ============================================================ 2 酵素の阻害
SOGAI_JS = HELP + ENGINE + r'''
  const MC={none:'#2563eb',comp:'#db2777',non:'#7c3aed'}, MN={none:'阻害剤なし',comp:'競争的阻害',non:'非競争的阻害'};
  const SV=[5,10,20,35,50,75,100,125,150];
  let world, paused=false, data=[], kept={}, pts=[], queue=[], fcount=0, doneMsg=false, sweeping='', names=true, showKm=false, note='';
  function cond(){ return {nE:+$('nE').value,nS:+$('nS').value,nI:+$('nI').value,mode:$('mode').value}; }
  function start(){ const c=cond(); if(world&&data.length>8) kept[world.o.mode]={data:data.slice(),nS:world.o.nS};
    world=mkWorld({nE:c.nE,nS:c.nS,nI:c.mode==='none'?0:c.nI,mode:c.mode,W:W,H:VH,fx:true}); data=[[0,0]]; paused=false; doneMsg=false; $('pause').textContent='⏸ 一時停止'; }
  function addPt(p){ for(let i=pts.length-1;i>=0;i--) if(pts[i].x===p.x&&pts[i].k===p.k) pts.splice(i,1); p.born=performance.now(); pts.push(p); }
  function rateNow(){ if(data.length<3) return 0; const b=data[data.length-1]; let a=data[0]; for(let i=data.length-1;i>=0;i--){ if(b[0]-data[i][0]>=1.5){a=data[i];break;} } return b[0]>a[0]?(b[1]-a[1])/(b[0]-a[0]):0; }
  function tick(dt){ world.step(dt); const last=data[data.length-1]; if(world.t-last[0]>=.2) data.push([world.t,world.P]);
    if(!doneMsg&&world.S.length===0&&world.bound()===0){ doneMsg=true; data.push([world.t,world.P]); } }
  // v = Vmax・S/(Km+S) に合わせる（発展表示用）
  function fit(ps){ let best=null; for(let km=2;km<=400;km+=2){ let a=0,b=0; for(const p of ps){ const f=p.x/(km+p.x); a+=p.v*f; b+=f*f; } const vm=a/b; let e=0; for(const p of ps){ const d=p.v-vm*p.x/(km+p.x); e+=d*d; } if(!best||e<best.e) best={km:km,vm:vm,e:e}; } return best; }
  function drawTime(){
    let tmax=20, pmax=20; const all=[{data:data,nS:world.o.nS}]; for(const k in kept) if(k!==world.o.mode) all.push(kept[k]);
    for(const r of all){ tmax=Math.max(tmax,Math.min(120,r.data[r.data.length-1][0])); pmax=Math.max(pmax,r.nS); }
    tmax=Math.ceil(tmax/20)*20; pmax=nice(pmax);
    const f=frame(6,VH+10,312,H-VH-16,tmax,pmax,'時間（秒）','生成物の量（個）');
    function line(d,col,lw){ ctx.save(); ctx.beginPath(); ctx.rect(f.L,f.T-6,f.R-f.L+2,f.B-f.T+8); ctx.clip(); ctx.strokeStyle=col; ctx.lineWidth=lw; ctx.lineJoin='round'; ctx.beginPath(); d.forEach((q,i)=>{ const x=f.X(q[0]),y=f.Y(q[1]); i?ctx.lineTo(x,y):ctx.moveTo(x,y); }); ctx.stroke(); ctx.restore(); }
    for(const k in kept){ if(k===world.o.mode) continue; line(kept[k].data,MC[k],1.8); }
    line(data,MC[world.o.mode],3);
    const q=data[data.length-1]; ctx.fillStyle=MC[world.o.mode]; ctx.beginPath(); ctx.arc(Math.min(f.R,f.X(q[0])),f.Y(q[1]),4.5,0,7); ctx.fill(); ctx.strokeStyle='#fff'; ctx.lineWidth=1.5; ctx.stroke();
    let ly=f.B-8; ['non','comp','none'].forEach(k=>{ if(k===world.o.mode||kept[k]){ ctx.fillStyle=MC[k]; ctx.fillRect(f.R-88,ly-8,14,3.5); tx(MN[k],f.R-70,ly-2,10.5,MC[k],'left',true); ly-=14; } });
  }
  function drawV0(){
    let vmax=4; for(const p of pts) vmax=Math.max(vmax,p.v*1.2); vmax=nice(vmax);
    const f=frame(322,VH+10,312,H-VH-16,160,vmax,'はじめの基質の数（基質濃度）','反応開始直後の反応速度（個/秒）');
    const now=performance.now(); let ly=f.B-8;
    ['none','comp','non'].forEach(k=>{ const col=MC[k], ps=pts.filter(p=>p.k===k).sort((a,b)=>a.x-b.x); if(!ps.length) return;
      const ft=(showKm&&ps.length>=6)?fit(ps):null;
      if(ft){ ctx.strokeStyle=col; ctx.lineWidth=2; ctx.beginPath(); for(let s=0;s<=160;s+=4){ const y=f.Y(ft.vm*s/(ft.km+s)); s?ctx.lineTo(f.X(s),y):ctx.moveTo(f.X(s),y); } ctx.stroke();
        ctx.setLineDash([4,3]); ctx.lineWidth=1.2; if(ft.vm<vmax){ ctx.beginPath(); ctx.moveTo(f.L,f.Y(ft.vm)); ctx.lineTo(f.R,f.Y(ft.vm)); ctx.stroke(); tx('Vmax '+ft.vm.toFixed(1),f.R-2,f.Y(ft.vm)+(k==='comp'?12:-4),10,col,'right',true); }
        if(ft.km<160){ ctx.beginPath(); ctx.moveTo(f.X(ft.km),f.Y(ft.vm/2)); ctx.lineTo(f.X(ft.km),f.B); ctx.stroke(); ctx.beginPath(); ctx.moveTo(f.L,f.Y(ft.vm/2)); ctx.lineTo(f.X(ft.km),f.Y(ft.vm/2)); ctx.stroke(); tx('Km '+ft.km,f.X(ft.km)+3,f.B-4-(k==='comp'?11:k==='non'?22:0),10,col,'left',true); } ctx.setLineDash([]); }
      else if(ps.length>=3){ ctx.strokeStyle=col; ctx.lineWidth=2; ctx.globalAlpha=.8; ctx.beginPath(); ctx.moveTo(f.X(0),f.Y(0)); ps.forEach(p=>ctx.lineTo(f.X(p.x),f.Y(p.v))); ctx.stroke(); ctx.globalAlpha=1; }
      ps.forEach(p=>{ const a=Math.min(1,(now-p.born)/350), r=4+(1-a)*9; ctx.fillStyle=col; ctx.globalAlpha=.35+.65*a; ctx.beginPath(); ctx.arc(f.X(p.x),f.Y(p.v),r,0,7); ctx.fill(); ctx.globalAlpha=1; ctx.strokeStyle='#fff'; ctx.lineWidth=1.2; ctx.stroke(); }); });
    ['non','comp','none'].forEach(k=>{ if(pts.some(p=>p.k===k)){ ctx.fillStyle=MC[k]; ctx.beginPath(); ctx.arc(f.R-82,ly-6,4,0,7); ctx.fill(); tx(MN[k],f.R-74,ly-2,10.5,MC[k],'left',true); ly-=14; } });
    if(!pts.length){ tx('「📈 3つの条件を自動で測定」を押すと、',(f.L+f.R)/2,(f.T+f.B)/2-8,11.5,'#64748b','center'); tx('3本の曲線が入ります',(f.L+f.R)/2,(f.T+f.B)/2+8,11.5,'#64748b','center'); }
    if(note) tx(note,(f.L+f.R)/2,f.T+2,10.5,'#b45309','center',true);
    if(sweeping) pill('自動で測定中… '+sweeping,(f.L+f.R)/2,f.T+22,11,'#0f172a','rgba(254,243,199,.95)');
  }
  function draw(){
    ctx.clearRect(0,0,W,H); ctx.fillStyle='#f8fafc'; ctx.fillRect(0,0,W,H);
    const m=world.o.mode; dVessel(world,m);
    if(names){ const it=[['E','酵素'],['S','基質'],['P','生成物']]; if(m==='comp') it.push(['IC','阻害剤（活性部位に結合）']); if(m==='non') it.push(['IN','阻害剤（別の場所に結合）']); dLegend(it); }
    const b=world.bound(), ih=world.inhib(), n=world.E.length, gw=170, gx=W-gw-12, gy=VH-44;
    rr(gx-8,gy-18,gw+16,56,8); ctx.fillStyle='rgba(255,255,255,.9)'; ctx.fill();
    tx('基質と結合 '+b+'/'+n,gx,gy-4,11,'#0f172a','left',true); rr(gx,gy+1,gw,7,3.5); ctx.fillStyle='#e2e8f0'; ctx.fill(); if(b>0){ rr(gx,gy+1,Math.max(7,gw*b/n),7,3.5); ctx.fillStyle='#f59e0b'; ctx.fill(); }
    tx('阻害剤と結合 '+ih+'/'+n,gx,gy+21,11,'#0f172a','left',true); rr(gx,gy+26,gw,7,3.5); ctx.fillStyle='#e2e8f0'; ctx.fill(); if(ih>0){ rr(gx,gy+26,Math.max(7,gw*ih/n),7,3.5); ctx.fillStyle='#a855f7'; ctx.fill(); }
    pill(MN[m],W-70,22,13,'#fff',MC[m]);
    if(doneMsg) pill('基質を使い切りました（生成物 '+world.P+' 個）',W/2,VH/2,14,'#0f172a','rgba(255,255,255,.95)');
    else if(paused) pill('一時停止中',W/2,VH/2,14,'#0f172a','rgba(255,255,255,.95)');
    drawTime(); drawV0();
    const v=rateNow();
    setStat('sT',world.t.toFixed(1)+' 秒'); setStat('sP',world.P+' 個'); setStat('sV',v.toFixed(1)+' 個/秒'); setStat('sB',b+' / '+n); setStat('sI',ih+' / '+n);
    setShare('【酵素の阻害】'+MN[m]+'：酵素'+world.o.nE+'個・基質'+world.o.nS+'個'+(m==='none'?'':'・阻害剤'+world.o.nI+'個')+'で、'+world.t.toFixed(0)+'秒で生成物が'+world.P+'個できた｜シミュラボ');
  }
  function loop(){ fcount++;
    if(!paused&&!doneMsg){ const sp=+$('spd').value; const n=Math.max(1,Math.round(sp*2)); for(let i=0;i<n;i++) tick(1/120); }
    if(queue.length&&fcount%4===0){ queue.shift()(); if(!queue.length) sweeping=''; }
    draw(); requestAnimationFrame(loop); }
  function resetPts(){ if(pts.length){ pts=[]; queue=[]; sweeping=''; note='数を変えたので、測定をやり直してください'; } kept={}; }
  $('go').addEventListener('click',start);
  $('mode').addEventListener('change',()=>{ const f=$('nI').closest('.field'); if(f) f.style.opacity=$('mode').value==='none'?.4:1; start(); });
  $('nS').addEventListener('change',start);
  $('nE').addEventListener('change',()=>{ resetPts(); start(); }); $('nI').addEventListener('change',()=>{ resetPts(); start(); });
  $('pause').addEventListener('click',()=>{ paused=!paused; $('pause').textContent=paused?'▶ 再開':'⏸ 一時停止'; });
  $('sweep').addEventListener('click',()=>{ if(queue.length) return; const c=cond(); note=''; pts=[];
    ['none','comp','non'].forEach(k=>SV.forEach(s=>queue.push(()=>{ sweeping=MN[k]+'・基質'+s+'個'; addPt({x:s,k:k,v:measure(c.nE,s,k==='none'?0:c.nI,k,14)}); }))); });
  $('names').addEventListener('click',()=>{ names=!names; $('names').textContent=names?'🏷 名前をかくす':'🏷 名前を表示'; });
  $('km').addEventListener('click',()=>{ showKm=!showKm; $('km').textContent=showKm?'Km・Vmaxをかくす':'Km・Vmaxを表示（発展）'; });
  window.__test={measure:measure,fit:fit,get world(){return world;},get pts(){return pts;},tick:function(n){ for(let i=0;i<n;i++) tick(1/60); while(queue.length) queue.shift()(); sweeping=''; draw(); }};
  $('nI').closest('.field').style.opacity=.4;
  start(); loop();
'''

SOGAI_ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
<p>酵素のはたらきを弱める物質を<b>阻害剤</b>（阻害物質）といいます。阻害剤が酵素のどこに結合するかによって、基質濃度を高くしたときの反応速度の変わり方がちがいます。このシミュレーターでは、「阻害剤なし」「競争的阻害」「非競争的阻害」の3つの条件で、酵素・基質・阻害剤が結合したり離れたりする様子と、基質濃度と反応速度のグラフを比べることができます。</p>
''' + N('<b>対応する単元</b>：高等学校「生物」（2）生命現象と物質 ア（ｱ）細胞と分子「㋑生命現象とタンパク質」（酵素の機能とタンパク質の立体構造との関連）。競争的阻害・非競争的阻害は教科書で発展的に扱われる内容です。') + '''
<h2>授業での使い方</h2>
<h3>導入：阻害剤を加えると何が変わるか</h3>
<p>まず「阻害剤なし」で反応させ、次に「競争的阻害」に切り替えます。紫のくさび形の阻害剤は基質と形が似ていて、酵素の活性部位にはまります。阻害剤がはまっている酵素（灰色）には基質が結合できません。左のグラフに前の条件の線が残るので、生成物の増え方がおそくなったことがわかります。</p>
<h3>展開：基質を増やせば反応速度はもどるか</h3>
<p>「基質を増やせば、反応速度は阻害剤がないときと同じになるだろうか」と予想させてから、「📈 3つの条件を自動で測定」を押します。競争的阻害（ピンク）は、基質濃度が低いところでは阻害剤なし（青）より大きく下がりますが、基質濃度を高くすると青の曲線に近づいていきます。基質が多いと、空いた活性部位に基質が先に結合することが増えるからです。</p>
<p>非競争的阻害（紫）では、六角形の阻害剤が活性部位とは別の場所に結合し、酵素の形が変わって、基質が結合していても生成物ができません（赤い×印）。基質を増やしても、阻害剤が結合している酵素ははたらけないので、曲線は青より低いところで頭打ちになります。</p>
<h3>発展：阻害剤の数を変える・Km と Vmax</h3>
<p>阻害剤の数を変えて測定し直すと、競争的阻害では曲線の立ち上がりがゆるやかになり、非競争的阻害では頭打ちの高さが下がることがわかります。「Km・Vmaxを表示（発展）」を押すと、測定した点に合う曲線と、最大反応速度 Vmax、ミカエリス定数 Km（反応速度が Vmax の半分になる基質濃度）が表示されます。</p>
<h3>生徒への問いの例</h3>
<ol>
<li>競争的阻害では、基質を増やすと阻害の影響が小さくなるのはなぜだろう？酵素の活性部位で何が起きているだろう？</li>
<li>非競争的阻害では、基質をいくら増やしても最大反応速度が元にもどらないのはなぜだろう？</li>
<li>阻害剤が結合する場所のちがいは、グラフのどこのちがいとして現れているだろう？</li>
</ol>
<h2>しくみ・解説</h2>
<h3>用語</h3>
<ul>
<li><b>阻害剤（阻害物質）</b>とは、酵素に結合して、酵素のはたらきを弱める物質です。</li>
<li><b>競争的阻害</b>とは、基質とよく似た構造の阻害剤が、基質と活性部位を取り合うことで起こる阻害です。</li>
<li><b>非競争的阻害</b>とは、阻害剤が活性部位とは別の場所に結合して酵素の立体構造を変え、酵素のはたらきを弱める阻害です。</li>
<li><b>最大反応速度（Vmax）</b>とは、基質濃度を十分に高くしたときの反応速度です。</li>
<li><b>ミカエリス定数（Km）</b>とは、反応速度が最大反応速度の半分になるときの基質濃度です。酵素と基質の結合しやすさの目安になります（発展）。</li>
</ul>
<h3>2つの阻害の比較</h3>
''' + T([["阻害剤が結合する場所", "活性部位", "活性部位とは別の場所"],
          ["阻害剤が結合した酵素", "基質が結合できない", "基質は結合できるが、生成物ができない"],
          ["基質濃度を高くすると", "阻害の影響が小さくなる", "阻害の影響は変わらない"],
          ["最大反応速度（Vmax）", "変わらない", "小さくなる"],
          ["ミカエリス定数（Km）※発展", "大きくなる", "変わらない"]],
         ["", "競争的阻害", "非競争的阻害"]) + '''
''' + P('見分け方は「基質濃度を十分に高くしたとき、反応速度が阻害剤なしの場合に近づくかどうか」です。近づけば競争的阻害、低いまま頭打ちになれば非競争的阻害です。') + '''
<h3>体の中での阻害</h3>
<p>阻害は、細胞が反応の進み方を調節するしくみとしても使われています。一連の反応の最終産物が、はじめの反応を進める酵素の活性部位とは別の場所（アロステリック部位）に結合して、その酵素のはたらきを弱めることを<b>フィードバック調節</b>といいます。薬の中にも、特定の酵素の阻害剤としてはたらくものが多くあります。</p>
<h3>このシミュレーターのモデル</h3>
<p>温度とpHは一定で、阻害剤は酵素に結合したり離れたりします（可逆的な阻害）。阻害剤は、基質を入れる前に酵素とまぜてあり、結合と解離がつり合った状態から反応を始めます。非競争的阻害は、阻害剤が「基質と結合していない酵素」と「酵素基質複合体」の両方に同じように結合する、純粋な非競争的阻害のモデルです。粒子の数が少ないため、測定値にはばらつきがあります（自動測定は14回の平均）。Km と Vmax は、測定した点に v = Vmax × [S] ÷ (Km ＋ [S]) の式を合わせて求めた値で、測定のたびに少し変わります。競争的阻害では、表示している基質濃度の範囲では Vmax に届かないため、Vmax が少し小さめに出ることがあります。</p>
<h2>参考</h2>
<ul>
<li>''' + A(MEXT_KOU, "文部科学省 高等学校学習指導要領（平成30年告示）解説 理科編") + '''（生物（2）生命現象と物質）</li>
<li>高等学校「生物」の教科書（酵素反応の調節、競争的阻害・非競争的阻害、フィードバック調節）</li>
</ul>
'''

sim(slug="kouso-sogai", cat="rika", emoji="🔒", score=79,
    title="酵素の阻害シミュレーター（競争的阻害と非競争的阻害のちがい）",
    title_tag="競争的阻害と非競争的阻害のシミュレーター｜阻害剤の結合場所と基質濃度・反応速度のグラフ（高校生物）",
    meta_desc="酵素・基質・阻害剤が結合したり離れたりする様子と、基質濃度と反応速度のグラフを、阻害剤なし・競争的阻害・非競争的阻害の3条件で比べられるシミュレーター。基質を増やすと競争的阻害では最大反応速度に近づき、非競争的阻害では届かないことを確かめられます。",
    og_title="酵素の阻害シミュレーター（競争的阻害と非競争的阻害のちがい）",
    og_desc="阻害剤が活性部位に結合する競争的阻害と、別の場所に結合する非競争的阻害。基質を増やすと反応速度は回復する？粒子の動きと3本の曲線で、結合する場所のちがいがグラフのちがいになる理由が見える。",
    card_desc="阻害剤なし・競争的阻害・非競争的阻害の3条件で、分子の動きと基質濃度―反応速度の曲線を比べる。",
    lead="青い丸が酵素、オレンジが基質、緑が生成物、紫が阻害剤です。「競争的阻害」では阻害剤が活性部位に結合して基質と取り合いになり、「非競争的阻害」では阻害剤が別の場所に結合して、基質が結合していても生成物ができなくなります。基質を増やすと反応速度がどうなるか、3つの条件で比べてみましょう。",
    model="生物 細胞と分子（酵素：競争的阻害・非競争的阻害）",
    level="高校（生物）",
    unit="高等学校 生物（2）生命現象と物質 ア（ｱ）細胞と分子 ㋑生命現象とタンパク質",
    canvas=canvas(640, 590, light=True),
    controls=select("mode", "条件", [("none", "阻害剤なし"), ("comp", "競争的阻害"), ("non", "非競争的阻害")])
             + slider("nS", "基質の数（基質濃度）", 10, 150, 50, 5, "{v} 個")
             + slider("nI", "阻害剤の数", 0, 40, 20, 2, "{v} 個")
             + slider("nE", "酵素の数", 2, 12, 6, 1, "{v} 個")
             + select("spd", "速さ", [("1", "×1"), ("2", "×2"), ("4", "×4"), ("0.5", "×0.5（ゆっくり）")]),
    buttons=btn("go", "▶ 反応を始める（はじめから）", True) + btn("pause", "⏸ 一時停止") + btn("sweep", "📈 3つの条件を自動で測定") + btn("names", "🏷 名前をかくす") + btn("km", "Km・Vmaxを表示（発展）"),
    stats=stats([("sT", "時間", False), ("sP", "生成物", True), ("sV", "いまの反応速度", True), ("sB", "基質と結合している酵素", False), ("sI", "阻害剤と結合している酵素", False)]),
    legend="青＝酵素（灰色は阻害剤が結合中）、オレンジ＝基質、緑＝生成物、紫のくさび形＝競争的阻害の阻害剤（活性部位に結合）、紫の六角形＝非競争的阻害の阻害剤（別の場所に結合）。赤い×＝基質が結合していても生成物ができない状態。条件を切り替えると、前の条件の線が左のグラフに残ります。",
    article=SOGAI_ARTICLE,
    faqs=[("競争的阻害と非競争的阻害のちがいは？", "阻害剤が結合する場所がちがいます。競争的阻害では、基質と似た構造の阻害剤が酵素の活性部位に結合し、基質と活性部位を取り合います。非競争的阻害では、阻害剤が活性部位とは別の場所に結合して酵素の立体構造を変え、基質が結合していても反応が進まなくなります。"),
          ("競争的阻害で、基質濃度を高くすると阻害の影響が小さくなるのはなぜ？", "基質と阻害剤が同じ活性部位を取り合っているからです。基質の数が阻害剤よりずっと多くなると、空いた活性部位には基質が結合することがほとんどになり、阻害剤が結合する機会が減ります。そのため、反応速度は阻害剤がないときの最大反応速度に近づきます。"),
          ("非競争的阻害で、基質を増やしても最大反応速度がもどらないのはなぜ？", "阻害剤は活性部位とは別の場所に結合するので、基質をいくら増やしても阻害剤の結合をじゃまできません。阻害剤が結合している酵素は生成物をつくれないので、はたらける酵素の数が減ったのと同じことになり、最大反応速度が小さくなります。"),
          ("グラフから2つの阻害を見分けるには？", "基質濃度と反応速度のグラフで、基質濃度を高くしたときの曲線を見ます。阻害剤なしの曲線に近づいていけば競争的阻害、低い値で頭打ちになれば非競争的阻害です。"),
          ("Km（ミカエリス定数）とは？", "反応速度が最大反応速度（Vmax）の半分になるときの基質濃度です。値が小さいほど、低い基質濃度でも酵素が基質と結合しやすいことを表します。競争的阻害では Km が大きくなり Vmax は変わらず、純粋な非競争的阻害では Km は変わらず Vmax が小さくなります。高校では発展的な内容です。"),
          ("阻害は体の中で役に立っているの？", "役に立っています。たとえば、一連の反応の最終産物が、はじめの反応を進める酵素に結合してはたらきを弱めるフィードバック調節は、必要な量だけ物質をつくるためのしくみです。また、多くの薬は、特定の酵素の阻害剤としてはたらきます。")],
    rel=[("kouso-hannou-sokudo", "⚗️", "酵素の反応速度シミュレーター"), ("maku-yuso", "🚪", "膜輸送のシミュレーター"),
         ("rinshishitsu-maku", "🧼", "リン脂質と細胞膜のでき方シミュレーター"), ("kouso-shikkatsu", "🌡️", "酵素の失活シミュレーター"), ("diffusion", "🫧", "拡散シミュレーター")],
    js=SOGAI_JS)
