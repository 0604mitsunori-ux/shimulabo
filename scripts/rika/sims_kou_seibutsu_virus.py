# -*- coding: utf-8 -*-
"""理科の授業向けシミュ（高校 生物：ウイルスのエンベロープと洗剤・エタノール）— シミュラボのリクエスト（2026-11-23 受付 4ed4e7da53／伊藤さん）から
   virus-sekken-alcohol … エンベロープをもつ／もたないウイルスに、界面活性剤・エタノールを加えたときの変化と感染性
   生物（2）ア（ｱ）細胞と分子（生体膜・タンパク質の立体構造）の身近な応用
   モデル：すべての分子の位置を「進み具合 p（0→1）」の関数として決める模式的なアニメーション（力の計算はしていない）。"""
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

MEXT_KOU = "https://www.mext.go.jp/a_menu/shotou/new-cs/1407074.htm"
def A(url, label): return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, label)

JS = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const FF='"Hiragino Sans","Hiragino Kaku Gothic ProN","Noto Sans JP","Yu Gothic UI","Yu Gothic",Meiryo,sans-serif';
  function tx(s,x,y,size,col,align,bold){ ctx.font=(bold?'bold ':'')+size+'px '+FF; ctx.fillStyle=col; ctx.textAlign=align||'left'; ctx.fillText(s,x,y); ctx.textAlign='left'; }
  function tw(s,size,bold){ ctx.font=(bold?'bold ':'')+size+'px '+FF; return ctx.measureText(s).width; }
  function rr(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
  function pill(s,x,y,size,col,bg){ const w=tw(s,size,true)+16; rr(x-w/2,y-size-2,w,size+12,8); ctx.fillStyle=bg||'rgba(255,255,255,.9)'; ctx.fill(); tx(s,x,y+2,size,col,'center',true); }
  const sm=v=>{ v=clamp(v,0,1); return v*v*(3-2*v); }, PI=Math.PI, TAU=PI*2;
  const hh=(i,k)=>{ const v=Math.sin(i*12.9898+k*78.233)*43758.5453; return v-Math.floor(v); };
  const angd=(a,b)=>{ let d=b-a; while(d>PI) d-=TAU; while(d<-PI) d+=TAU; return d; };
  const mixp=(a,b,k)=>[a[0]+(b[0]-a[0])*k,a[1]+(b[1]-a[1])*k,a[2]+angd(a[2],b[2])*k];
  const VW=640, VH=330, CY=336, CH=134, CAP=476;
  let t=0, p=0, cur='none', adding=false, paused=false, names=true, test=-1, testF=[true,true];

  // ===== 分子 =====
  function mol(q,sc,kind,al){ // q=[頭のx,頭のy,尾の向き]
    const th=q[2], cx=Math.cos(th), cy=Math.sin(th), px=-cy, py=cx, L=20*sc, x=q[0], y=q[1]; ctx.globalAlpha=al==null?1:al;
    const offs=kind==='L'?[-3.2*sc,3.2*sc]:[0];
    for(const pass of [0,1]){ ctx.strokeStyle=pass?'#facc15':'#a16207'; ctx.lineWidth=(pass?2.2:3.8)*Math.max(.55,sc); ctx.lineCap='round';
      for(const o of offs){ ctx.beginPath(); ctx.moveTo(x+cx*4*sc+px*o,y+cy*4*sc+py*o); const w=Math.sin(t*5+x*.3+o)*1.6*sc; ctx.quadraticCurveTo(x+cx*L*.6+px*(o+w),y+cy*L*.6+py*(o+w),x+cx*L+px*o,y+cy*L+py*o); ctx.stroke(); } }
    ctx.beginPath(); ctx.arc(x,y,(kind==='L'?5.4:5)*sc,0,7); ctx.fillStyle=kind==='L'?'#ef4444':'#2563eb'; ctx.fill(); ctx.strokeStyle=kind==='L'?'#7f1d1d':'#1e3a8a'; ctx.lineWidth=1; ctx.stroke(); ctx.globalAlpha=1; }
  function etoh(x,y,sc,al){ ctx.globalAlpha=al; ctx.beginPath(); ctx.arc(x,y,2.6*sc,0,7); ctx.fillStyle='#a855f7'; ctx.fill(); ctx.beginPath(); ctx.arc(x+2.6*sc,y-1.2*sc,1.7*sc,0,7); ctx.fillStyle='#e9d5ff'; ctx.fill(); ctx.globalAlpha=1; }
  function spike(x,y,ang,sc,d,tm){ // d=0 正常 → 1 変性
    ctx.save(); ctx.translate(x,y); ctx.rotate(ang+PI/2+d*Math.sin(x*7.1+y)*.7); const c=d>.02?'rgb('+[13+135*d,148+15*d,136+48*d].map(Math.round).join(',')+')':'#0d9488';
    ctx.strokeStyle=c; ctx.lineCap='round'; ctx.lineWidth=5*sc;
    if(tm){ ctx.beginPath(); ctx.moveTo(0,52*sc); ctx.lineTo(0,0); ctx.stroke(); ctx.beginPath(); ctx.arc(0,58*sc,6*sc,0,7); ctx.fillStyle=c; ctx.fill(); }
    ctx.beginPath(); ctx.moveTo(0,0); ctx.quadraticCurveTo(d*9*sc,-9*sc,d*5*sc,-(18-6*d)*sc); ctx.stroke();
    const hy=-(22-9*d)*sc, hx=d*7*sc; ctx.fillStyle=c; ctx.strokeStyle='rgba(15,23,42,.45)'; ctx.lineWidth=1;
    [[-5.5,0,5.6],[5.5,0,5.6],[0,-6,5.6]].forEach((o,i)=>{ const jx=d*(hh(i,x)-.5)*9, jy=d*(hh(i,y)+.2)*8; ctx.beginPath(); ctx.arc(hx+(o[0]*(1-.45*d)+jx)*sc,hy+(o[1]*(1-.6*d)+jy)*sc,o[2]*sc*(1-.18*d),0,7); ctx.fill(); ctx.stroke(); });
    ctx.restore(); }
  function genome(x,y,r,al){ ctx.globalAlpha=al==null?1:al; ctx.strokeStyle='#ea580c'; ctx.lineWidth=Math.max(1.6,r*.13); ctx.lineCap='round'; ctx.beginPath(); for(let u=0;u<=1.001;u+=.01){ const a=u*TAU*2.3+t*.3, rr2=r*(.25+.7*u)*(.88+.12*Math.sin(u*34)); const X=x+Math.cos(a)*rr2, Y=y+Math.sin(a)*rr2; u?ctx.lineTo(X,Y):ctx.moveTo(X,Y); } ctx.stroke(); ctx.globalAlpha=1; }
  function capsidRing(x,y,R,n,br,amp,knob){ for(let i=0;i<n;i++){ const a=i/n*TAU, jx=Math.sin(t*6+i*1.9)*amp, jy=Math.cos(t*5.2+i*2.7)*amp, bx=x+Math.cos(a)*R+jx, by=y+Math.sin(a)*R+jy;
      if(knob&&i%3===0){ ctx.strokeStyle='#0d9488'; ctx.lineWidth=3.2; ctx.lineCap='round'; ctx.beginPath(); ctx.moveTo(bx,by); ctx.lineTo(bx+Math.cos(a)*(br+7),by+Math.sin(a)*(br+7)); ctx.stroke(); ctx.beginPath(); ctx.arc(bx+Math.cos(a)*(br+8),by+Math.sin(a)*(br+8),3.6,0,7); ctx.fillStyle='#0d9488'; ctx.fill(); }
      ctx.beginPath(); ctx.arc(bx,by,br,0,7); ctx.fillStyle=i%2?'#8b5cf6':'#a78bfa'; ctx.fill(); ctx.strokeStyle='#5b21b6'; ctx.lineWidth=1.1; ctx.stroke(); } }

  // ===== 全体表示：エンベロープをもつウイルス =====
  const E={x:165,y:162,R:90}, NL=46, MIC=[]; for(let k=0;k<7;k++){ const a=k/7*TAU+.35; MIC.push([clamp(E.x+Math.cos(a)*128,28,296),clamp(E.y+Math.sin(a)*128,44,300)]); }
  const micSlot=(k,q)=>{ const b=q/20*TAU+k; return [MIC[k][0]+Math.cos(b)*17,MIC[k][1]+Math.sin(b)*17,b+PI]; };
  function lipW(j){ const leaf=j%2, a=Math.floor(j/2)/NL*TAU, r=leaf?E.R-9:E.R+9; const home=[E.x+Math.cos(a)*r,E.y+Math.sin(a)*r,leaf?a:a+PI], tau=.32+.4*hh(j,1);
    if(cur==='surf'){ const k=sm((p-tau)/.22); return [mixp(home,micSlot(j%7,Math.floor(j/7)),k),k]; }
    if(cur==='eth'){ if(hh(j,6)<.5){ const k=sm((p-tau)/.3); return [mixp(home,[18+hh(j,7)*284,44+hh(j,8)*262,hh(j,9)*TAU],k),k]; }
      const am=6*sm(p/.6); return [[home[0]+Math.sin(t*6+j)*am,home[1]+Math.cos(t*5+j*2)*am,home[2]+Math.sin(t*3+j)*.5*sm(p/.6)],0]; }
    return [[home[0]+Math.sin(t*5+j)*.6,home[1]+Math.cos(t*4+j*2)*.6,home[2]],0]; }
  function envLeft(){ if(cur==='none') return 1; let n=0; for(let j=0;j<NL*2;j++) if(lipW(j)[1]<.5) n++; return n/(NL*2); }
  function spk(q){ const a=(q+.5)/10*TAU; if(cur==='surf') return sm((p-(.45+.3*hh(q,11)))/.2); if(cur==='eth') return sm((p-.25-hh(q,12)*.2)/.35); return 0; }
  function protLeft(){ let s=0; for(let q=0;q<10;q++) s+=1-spk(q); return s/10; }
  const funcE=()=>cur==='none'||p<.4;
  function dEnveloped(){
    capsidRing(E.x,E.y,44,16,7.2,cur==='eth'?.8*sm(p):.4,false); genome(E.x,E.y,26);
    for(let j=0;j<NL*2;j++) mol(lipW(j)[0],.5,'L');
    if(cur==='surf'){ const al=sm(p/.05); for(let s=0;s<42;s++){ let sx=20+hh(s,2)*280, sy=44+hh(s,3)*262; const d=Math.hypot(sx-E.x,sy-E.y); if(d<122){ sx=E.x+(sx-E.x)/d*124; sy=E.y+(sy-E.y)/d*124; }
        const a=(s+.5)/42*TAU, st0=[sx+Math.sin(t*2+s)*4,sy+Math.cos(t*1.7+s)*4,hh(s,4)*TAU+t*.6], ins=[E.x+Math.cos(a)*(E.R+11),E.y+Math.sin(a)*(E.R+11),a+PI];
        let q=mixp(st0,ins,sm((p-.03-hh(s,4)*.12)/.15)); q=mixp(q,micSlot(s%7,14+Math.floor(s/7)),sm((p-(.4+.35*hh(s,5)))/.22)); mol(q,.5,'S',al); } }
    if(cur==='eth'){ const al=sm(p/.05); for(let e=0;e<60;e++){ const sx=14+hh(e,2)*290+Math.sin(t*1.5+e)*6, sy=44+hh(e,3)*262+Math.cos(t*1.3+e)*6; let q=[sx,sy];
        if(e<42){ const a=hh(e,4)*TAU+t*.25*(e%2?1:-1), r=E.R+(hh(e,5)-.5)*20, k=sm((p-.02-hh(e,6)*.25)/.2); q=[sx+(E.x+Math.cos(a)*r-sx)*k,sy+(E.y+Math.sin(a)*r-sy)*k]; } etoh(q[0],q[1],.8,al); } }
    for(let q=0;q<10;q++){ const a=(q+.5)/10*TAU, k=spk(q); let x=E.x+Math.cos(a)*(E.R+9), y=E.y+Math.sin(a)*(E.R+9), ang=a, d=0;
      if(cur==='surf'){ const m=MIC[q%7]; x+=(m[0]+Math.cos(a)*22-x)*k; y+=(m[1]+Math.sin(a)*22-y)*k; ang=a+k*(hh(q,13)-.5)*3; d=k*.35; } else if(cur==='eth') d=k;
      spike(x,y,ang,.62,d,false); }
  }
  // ===== 全体表示：エンベロープをもたないウイルス =====
  const NV={x:482,y:162,R:66};
  function dNaked(){ capsidRing(NV.x,NV.y,NV.R,24,8.6,cur==='eth'?1.3*sm(p):.4,true); genome(NV.x,NV.y,38);
    if(cur==='none') return; const al=sm(p/.05);
    if(cur==='surf') for(let s=0;s<30;s++){ const a=hh(s,21)*TAU+t*(.12+.2*hh(s,22))*(s%2?1:-1), r=NV.R+26+hh(s,23)*36+Math.sin(t*1.3+s)*7; mol([clamp(NV.x+Math.cos(a)*r,336,628),clamp(NV.y+Math.sin(a)*r,44,304),a+PI+Math.sin(t*2+s)*1.1],.5,'S',al); }
    else for(let e=0;e<46;e++){ const a=hh(e,24)*TAU+t*(.15+.25*hh(e,25))*(e%2?1:-1), r=NV.R+14+hh(e,26)*50+Math.sin(t*1.6+e)*8; etoh(clamp(NV.x+Math.cos(a)*r,334,630),clamp(NV.y+Math.sin(a)*r,42,306),.8,al); } }
  function dWhole(){
    const g=ctx.createLinearGradient(0,0,0,VH); g.addColorStop(0,'#eff6ff'); g.addColorStop(1,'#dbeafe'); ctx.fillStyle=g; ctx.fillRect(0,0,VW,VH);
    ctx.strokeStyle='#bfdbfe'; ctx.lineWidth=2; ctx.setLineDash([6,5]); ctx.beginPath(); ctx.moveTo(322,34); ctx.lineTo(322,VH-6); ctx.stroke(); ctx.setLineDash([]);
    dEnveloped(); dNaked();
    pill('エンベロープをもつウイルス',165,22,12.5,'#fff','#be123c'); pill('エンベロープをもたないウイルス',482,22,12.5,'#fff','#6d28d9');
    if(names){ const a=sm(1-p/.25); if(a>.02&&cur!=='x'){ ctx.globalAlpha=cur==='none'?1:a;
        pill('遺伝物質',E.x,E.y+3,10.5,'#9a3412'); pill('カプシド',E.x,E.y-56,10.5,'#5b21b6'); pill('エンベロープ（脂質二重層）',E.x,VH-22,11,'#9f1239'); pill('膜のタンパク質',62,58,11,'#115e59');
        ctx.strokeStyle='#115e59'; ctx.lineWidth=1.2; ctx.beginPath(); ctx.moveTo(74,64); ctx.lineTo(E.x+Math.cos(3.77)*(E.R+26),E.y+Math.sin(3.77)*(E.R+26)); ctx.stroke(); ctx.globalAlpha=1; }
      pill('遺伝物質',NV.x,NV.y+3,10.5,'#9a3412'); pill('カプシド（タンパク質の殻）',NV.x,VH-36,11,'#5b21b6');
      if(cur!=='none'){ let x=336; rr(x-6,VH-26,298,22,7); ctx.fillStyle='rgba(255,255,255,.92)'; ctx.fill(); if(cur==='surf'){ mol([x+6,VH-15,0],.5,'S'); tx('界面活性剤',x+22,VH-11,10.5,'#0f172a','left',true); mol([x+92,VH-15,0],.5,'L'); tx('エンベロープの脂質',x+108,VH-11,10.5,'#0f172a','left',true); } else { etoh(x+6,VH-15,.8,1); tx('エタノール',x+16,VH-11,10.5,'#0f172a','left',true); mol([x+92,VH-15,0],.5,'L'); tx('エンベロープの脂質',x+108,VH-11,10.5,'#0f172a','left',true); } }
    }
  }
  // ===== 拡大表示：エンベロープの断面 =====
  const ZL=[], MZ=[[80,72],[205,262],[335,70],[470,262],[575,78]], ZN=[0,0,0,0,0];
  for(let i=0;i<40;i++){ const x=20+15*i; if(Math.abs(x-320)<24) continue; for(const leaf of [0,1]){ const z=Math.min(4,Math.floor(x/128)); ZL.push({x:x,leaf:leaf,z:z,q:ZN[z]++}); } }
  const ZS=[]; for(let s=0;s<36;s++){ let x=27.5+15*Math.floor(s*39/36); if(Math.abs(x-320)<26) x+=45; const z=Math.min(4,Math.floor(x/128)); ZS.push({x:x,z:z,q:ZN[z]++}); }
  const mzSlot=(z,q)=>{ const b=q/ZN[z]*TAU; return [MZ[z][0]+Math.cos(b)*30,MZ[z][1]+Math.sin(b)*30,b+PI]; };
  function dZoom(){
    const el=envLeft(); ctx.fillStyle='#dbeafe'; ctx.fillRect(0,0,VW,VH); ctx.fillStyle='rgba(255,237,213,'+(.25+.75*el)+')'; ctx.fillRect(0,176,VW,VH-176);
    capsidRing(320,VH+250,280,96,9,.4,false);
    ZL.forEach((m,j)=>{ const home=[m.x,m.leaf?202:150,m.leaf?-PI/2:PI/2], tau=.45+.3*hh(j,31); let q;
      if(cur==='surf') q=mixp(home,mzSlot(m.z,m.q),sm((p-tau)/.22));
      else if(cur==='eth'){ if(hh(j,6)<.5) q=mixp(home,[m.x+(hh(j,32)-.5)*110,176+(hh(j,33)-.5)*230,home[2]+(hh(j,34)-.5)*5],sm((p-(.32+.4*hh(j,1)))/.3)); else { const am=8*sm(p/.6); q=[home[0]+Math.sin(t*6+j)*am,home[1]+Math.cos(t*5+j*2)*am*.6,home[2]+Math.sin(t*3+j)*.6*sm(p/.6)]; } }
      else q=[home[0]+Math.sin(t*5+j)*.8,home[1]+Math.cos(t*4+j*2)*.8,home[2]+Math.sin(t*3+j)*.06];
      mol(q,1,'L'); });
    if(cur==='surf'){ const al=sm(p/.05); ZS.forEach((m,s)=>{ const st0=[14+hh(s,2)*612+Math.sin(t*2+s)*6,34+hh(s,3)*66+Math.cos(t*1.7+s)*6,hh(s,4)*TAU+t*.6]; let q=mixp(st0,[m.x,150,PI/2],sm((p-.03-hh(s,4)*.14)/.16)); q=mixp(q,mzSlot(m.z,m.q),sm((p-(.45+.3*hh(s,5)))/.22)); mol(q,1,'S',al); }); }
    if(cur==='eth'){ const al=sm(p/.05); for(let e=0;e<74;e++){ const sx=10+hh(e,2)*620+Math.sin(t*1.5+e)*7, sy=34+hh(e,3)*90+Math.cos(t*1.3+e)*7; let x=sx,y=sy; if(e<52){ const k=sm((p-.02-hh(e,6)*.28)/.2); x=sx+(10+hh(e,7)*620-sx)*k+Math.sin(t*2+e)*3; y=sy+(140+hh(e,8)*72-sy)*k; } etoh(x,y,1.25,al); } }
    const k=cur==='surf'?sm((p-.6)/.25):0, d=cur==='eth'?sm((p-.3)/.4):k*.35; const sx=320+k*26, sy=150-k*40;
    ctx.save(); ctx.translate(sx,sy); ctx.rotate(k*.6); ctx.translate(-sx,-sy); spike(sx,sy,-PI/2,1.5,d,true);
    if(k>.3) for(let i=0;i<8;i++){ const sd=i%2?1:-1, yy=sy+12+Math.floor(i/2)*16; mol([sx+sd*22,yy,sd>0?PI:0],1,'S',sm((k-.3)/.4)); }
    ctx.restore();
    if(names){ pill('ウイルスの外側（水）',92,22,12,'#1e3a8a'); if(el>.5){ pill('ウイルスの内部',92,VH-58,12,'#9a3412'); pill('エンベロープ（脂質二重層）',520,176,12,'#9f1239'); } pill(d>.6?'変性した膜のタンパク質':k>.6?'膜からはずれたタンパク質':'膜のタンパク質',sx-112,sy-58,12,'#115e59'); pill('カプシド',320,VH-14,12,'#5b21b6');
      let x=380; rr(x-6,36,258,22,7); ctx.fillStyle='rgba(255,255,255,.92)'; ctx.fill(); ctx.beginPath(); ctx.arc(x+4,47,5,0,7); ctx.fillStyle='#ef4444'; ctx.fill(); tx('親水部',x+12,51,10.5,'#0f172a','left',true); ctx.strokeStyle='#a16207'; ctx.lineWidth=3.6; ctx.beginPath(); ctx.moveTo(x+56,47); ctx.lineTo(x+72,47); ctx.stroke(); tx('疎水部',x+76,51,10.5,'#0f172a','left',true);
      if(cur==='surf'){ ctx.beginPath(); ctx.arc(x+126,47,5,0,7); ctx.fillStyle='#2563eb'; ctx.fill(); tx('界面活性剤の親水部',x+134,51,10.5,'#0f172a','left',true); } if(cur==='eth'){ etoh(x+126,47,1.2,1); tx('エタノール',x+136,51,10.5,'#0f172a','left',true); } }
  }
  // ===== 細胞に近づける（感染できるか） =====
  function mini(x,y,kind,ok,al){ ctx.globalAlpha=al;
    if(kind===0){ if(ok||cur==='eth'){ ctx.strokeStyle=ok?'#ef4444':'#9ca3af'; ctx.lineWidth=3.2; if(!ok) ctx.setLineDash([5,5]); ctx.beginPath(); ctx.arc(x,y,17,0,7); ctx.stroke(); ctx.setLineDash([]);
        for(let i=0;i<8;i++){ const a=i/8*TAU+.4; ctx.strokeStyle=ok?'#0d9488':'#9ca3af'; ctx.lineWidth=2.6; ctx.lineCap='round'; ctx.beginPath(); ctx.moveTo(x+Math.cos(a)*18,y+Math.sin(a)*18); ctx.lineTo(x+Math.cos(a+(ok?0:.5))*(ok?25:22),y+Math.sin(a+(ok?0:.5))*(ok?25:22)); ctx.stroke(); } }
      ctx.beginPath(); for(let i=0;i<6;i++){ const a=i/6*TAU; ctx.lineTo(x+Math.cos(a)*10,y+Math.sin(a)*10); } ctx.closePath(); ctx.fillStyle='#a78bfa'; ctx.fill(); ctx.strokeStyle='#5b21b6'; ctx.lineWidth=1.2; ctx.stroke(); genome(x,y,6); ctx.globalAlpha=al; }
    else { ctx.beginPath(); for(let i=0;i<8;i++){ const a=i/8*TAU; ctx.lineTo(x+Math.cos(a)*15,y+Math.sin(a)*15); } ctx.closePath(); ctx.fillStyle='#a78bfa'; ctx.fill(); ctx.strokeStyle='#5b21b6'; ctx.lineWidth=1.4; ctx.stroke();
      for(let i=0;i<8;i++){ const a=i/8*TAU; ctx.beginPath(); ctx.arc(x+Math.cos(a)*19,y+Math.sin(a)*19,2.8,0,7); ctx.fillStyle='#0d9488'; ctx.fill(); } genome(x,y,8); }
    ctx.globalAlpha=1; }
  function dCell(){
    const my=CY+92; ctx.fillStyle='#e0f2fe'; ctx.fillRect(0,CY,VW,CH); ctx.fillStyle='#fef3c7'; ctx.fillRect(0,my,VW,CY+CH-my);
    ctx.strokeStyle='#fb7185'; ctx.lineWidth=7; ctx.beginPath(); ctx.moveTo(0,my); ctx.lineTo(VW,my); ctx.stroke(); ctx.strokeStyle='#fecdd3'; ctx.lineWidth=2.5; ctx.beginPath(); ctx.moveTo(0,my); ctx.lineTo(VW,my); ctx.stroke();
    [165,482].forEach((x,i)=>{ const glow=test>=.38&&testF[i]; ctx.strokeStyle=glow?'#f59e0b':'#4f46e5'; ctx.lineWidth=4; ctx.lineCap='round'; ctx.beginPath(); ctx.moveTo(x,my+6); ctx.lineTo(x,my-8); ctx.moveTo(x,my-8); ctx.lineTo(x-7,my-17); ctx.moveTo(x,my-8); ctx.lineTo(x+7,my-17); ctx.stroke(); });
    tx('細胞の中',12,CY+CH-10,11.5,'#92400e','left',true); tx('細胞膜',12,my-9,11,'#be123c','left',true); if(names) tx('受容体',150,my-10,11,'#3730a3','right',true);
    if(test<0){ pill('「🦠 細胞に近づける」を押すと、いまの状態で細胞に感染できるかを確かめます',VW/2,CY+34,12,'#0f172a','rgba(255,255,255,.92)'); return; }
    [165,482].forEach((x0,i)=>{ const ok=testF[i]; let x=x0, y, al=1, k1=sm(test/.38);
      if(ok){ y=CY+18+k1*(my-44-CY-18); const k2=sm((test-.58)/.42); y+=k2*52; al=1-k2*.85; mini(x,y,i,true,al); if(k2>0) genome(x,my+24,13,k2);
        if(test>.45) pill(test>.9?'感染する（遺伝物質が細胞に入った）':'受容体に結合',x,CY+14,11.5,'#fff','rgba(220,38,38,.92)'); }
      else { y=CY+18+k1*(my-50-CY-18); const k2=sm((test-.45)/.55); y-=Math.sin(k2*PI)*8; x+=k2*44; mini(x,y,i,false,1); if(test>.45){ pill('感染しない（結合・侵入できない）',x0,CY+14,11.5,'#fff','rgba(4,120,87,.92)'); if(test>.8&&i===0) tx('遺伝物質は残っている',x+34,y+4,11,'#92400e','left',true); } } });
  }
  function wrap(s,maxw,size){ const out=[]; let c=''; for(const ch of s){ if(tw(c+ch,size,false)>maxw){ out.push(c); c=ch; } else c+=ch; } if(c) out.push(c); return out; }
  function caption(){
    if(cur==='none') return 'エンベロープをもつウイルス（左）は、脂質二重層の膜（エンベロープ）で包まれ、膜のタンパク質が外につき出ています。エンベロープをもたないウイルス（右）は、タンパク質の殻（カプシド）がいちばん外側です。加える物質を選んで「▶ 加える」を押してください。';
    if(cur==='surf') return p<.4?'洗剤の界面活性剤の分子（青い頭）が、疎水部をエンベロープの脂質二重層にさしこんでいます。右のウイルスには、界面活性剤が入りこむ脂質の膜がありません。':'エンベロープは、脂質と界面活性剤がまざった小さな集まりに分かれてなくなりました。膜のタンパク質も失われ、遺伝物質が残っていても、細胞に結合・侵入できません。右のウイルスは形が保たれています（洗い流すことはできます）。';
    return p<.4?'エタノール（紫）が膜に入りこんで脂質の並びを乱し、タンパク質の立体構造にも影響しはじめています。':'エンベロープの脂質の並びがくずれ、膜のタンパク質は変性しました。遺伝物質が残っていても、細胞に結合・侵入できません。右のウイルスは、このモデルではエタノールの影響を受けにくいものとしています（ウイルスの種類や条件でちがいます）。'; }
  function draw(){
    ctx.clearRect(0,0,W,H); ctx.fillStyle='#f8fafc'; ctx.fillRect(0,0,W,H);
    ctx.save(); rr(0,0,VW,VH,10); ctx.clip(); if($('view').value==='zoom') dZoom(); else dWhole();
    if(paused) pill('一時停止中',VW/2,60,13,'#0f172a','rgba(255,255,255,.95)');
    if(cur!=='none'){ const w=110, x=14, y=VH-8; rr(x,y-7,w,6,3); ctx.fillStyle='rgba(15,23,42,.15)'; ctx.fill(); rr(x,y-7,Math.max(6,w*p),6,3); ctx.fillStyle=cur==='surf'?'#2563eb':'#a855f7'; ctx.fill(); }
    ctx.restore(); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1; rr(.5,.5,VW-1,VH-1,10); ctx.stroke();
    ctx.save(); rr(0,CY,VW,CH,10); ctx.clip(); dCell(); ctx.restore(); rr(.5,CY+.5,VW-1,CH-1,10); ctx.stroke();
    rr(0,CAP,W,H-CAP,10); ctx.fillStyle='#fff'; ctx.fill(); ctx.strokeStyle='#e2e8f0'; ctx.stroke(); wrap(caption(),W-28,12.5).slice(0,6).forEach((l,i)=>tx(l,14,CAP+22+i*18,12.5,'#0f172a','left',false));
    const el=envLeft(), pl=protLeft(), fe=funcE();
    setStat('sV1',fe?'あり':'なし'); setStat('sV2','あり'); setStat('sE',Math.round(el*100)+' %'); setStat('sP',Math.round(pl*100)+' %');
    setShare('【ウイルスと洗剤・アルコール】'+(cur==='none'?'エンベロープをもつウイルスともたないウイルスの構造を比べた':(cur==='surf'?'洗剤（界面活性剤）':'エタノール')+'を加えると、エンベロープの残りは'+Math.round(el*100)+'%、膜タンパク質のはたらきは'+Math.round(pl*100)+'%になった')+'｜シミュラボ');
  }
  function step(dt){ t+=dt; if(adding&&p<1) p=Math.min(1,p+dt/9); if(test>=0&&test<1) test=Math.min(1,test+dt/4.5); }
  function loop(){ if(!paused){ const sp=+$('spd').value, n=Math.max(1,Math.round(sp*2)); for(let i=0;i<n;i++) step(1/120); } draw(); requestAnimationFrame(loop); }
  function reset(){ p=0; cur='none'; adding=false; test=-1; $('add').textContent='▶ 加える'; }
  $('add').addEventListener('click',()=>{ if(cur==='none'){ cur=$('sub').value; p=0; adding=true; test=-1; $('add').textContent='（加えました）'; } });
  $('sub').addEventListener('change',reset);
  $('reset').addEventListener('click',reset);
  $('test').addEventListener('click',()=>{ testF=[funcE(),true]; test=0; });
  $('pause').addEventListener('click',()=>{ paused=!paused; $('pause').textContent=paused?'▶ 再開':'⏸ 一時停止'; });
  $('names').addEventListener('click',()=>{ names=!names; $('names').textContent=names?'🏷 名前をかくす':'🏷 名前を表示'; });
  window.__test={step:function(s){ const n=Math.round(s*60); for(let i=0;i<n;i++) step(1/60); draw(); },get s(){ return {cur:cur,p:+p.toFixed(2),env:+envLeft().toFixed(2),prot:+protLeft().toFixed(2),funcE:funcE(),test:+test.toFixed(2),testF:testF,ZL:ZL.length,ZN:ZN}; }};
  loop();
'''

ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
<p>ウイルスには、タンパク質の殻（カプシド）の外側を<b>エンベロープ</b>という脂質二重層の膜で包まれたものと、エンベロープをもたないものがあります。このシミュレーターでは、2種類のウイルスを並べて、洗剤の界面活性剤やエタノールを加えたときに、どの構造に何が起こり、なぜ感染できなくなるのかを見ることができます。</p>
''' + N('<b>対応する単元</b>：高等学校「生物」（2）生命現象と物質 ア（ｱ）細胞と分子「㋐生体物質と細胞」（生体膜とリン脂質）・「㋑生命現象とタンパク質」（タンパク質の立体構造と変性）の身近な応用。「生物基礎」の免疫・感染症、「保健」の感染症の予防と関連づけて使えます。') + '''
<h2>授業での使い方</h2>
<h3>導入：2つのウイルスの構造を比べる</h3>
<p>何も加えない状態で、左のウイルス（エンベロープあり）と右のウイルス（エンベロープなし）を比べます。左は外側から、膜のタンパク質、エンベロープ（脂質二重層）、カプシド、遺伝物質の順です。右はカプシドがいちばん外側です。「表示」を「エンベロープの断面を拡大」にすると、エンベロープがリン脂質二重層でできていて、膜のタンパク質がそれをつらぬいていることがわかります。ここで「洗剤を加えると、どの部分が変化するだろう」と予想させます。</p>
<h3>展開：洗剤とエタノールを加える</h3>
<p>「洗剤（界面活性剤）」を選んで「▶ 加える」を押すと、青い頭の界面活性剤が、疎水部をエンベロープにさしこみ、やがて膜は脂質と界面活性剤がまざった小さな集まりに分かれてなくなります。右のウイルスには脂質の膜がないので、界面活性剤は入りこめません。「↺ 新しいウイルスにもどす」を押してから「エタノール」を加えると、膜の脂質の並びが乱れ、膜のタンパク質の形が変わります（変性）。</p>
<h3>まとめ：構造の変化と感染性</h3>
<p>「🦠 細胞に近づける」を押すと、いまの状態のウイルスが細胞に感染できるかを確かめられます。正常なウイルスは受容体に結合して、遺伝物質が細胞に入ります。エンベロープや膜のタンパク質を失ったウイルスは、遺伝物質が残っていても、結合・侵入ができません。</p>
<h3>生徒への問いの例</h3>
<ol>
<li>界面活性剤は、エンベロープのどの部分に、分子のどちら側を向けて入りこむだろう？リン脂質の親水部・疎水部と関連づけて説明しよう。</li>
<li>遺伝物質がこわれていないのに、感染できなくなるのはなぜだろう？</li>
<li>エンベロープをもたないウイルスに、洗剤やアルコールが効きにくいのはなぜだろう？その場合、手洗いにはどんな意味があるだろう？</li>
</ol>
<h2>しくみ・解説</h2>
<h3>用語</h3>
<ul>
<li><b>ウイルス</b>とは、遺伝物質（DNAまたはRNA）がタンパク質の殻に包まれた粒子で、細胞に入りこんで増えます。</li>
<li><b>カプシド</b>とは、遺伝物質を包むタンパク質の殻です。</li>
<li><b>エンベロープ</b>とは、一部のウイルスがカプシドの外側にもつ脂質二重層の膜です。ウイルスが細胞から出るときに、細胞の膜をまとってできます。インフルエンザウイルスやコロナウイルスなどがもっています。</li>
<li><b>受容体</b>とは、細胞の表面にあり、特定の物質と結合するタンパク質です。ウイルスは表面のタンパク質で細胞の受容体に結合し、細胞に侵入します。</li>
<li><b>界面活性剤</b>とは、親水部と疎水部をもつ分子で、セッケンや洗剤の主成分です。</li>
</ul>
<h3>2種類のウイルスと、洗剤・エタノールの作用</h3>
''' + T([["いちばん外側", "エンベロープ（脂質二重層）と膜のタンパク質", "カプシド（タンパク質の殻）"],
          ["例", "インフルエンザウイルス、コロナウイルスなど", "ノロウイルス、ロタウイルス、アデノウイルスなど"],
          ["界面活性剤", "疎水部が脂質二重層に入りこみ、膜をこわす", "作用する脂質の膜がない"],
          ["エタノール", "膜の脂質の並びを乱し、タンパク質を変性させる", "一般に効きにくい（種類や条件による）"]],
         ["", "エンベロープをもつウイルス", "エンベロープをもたないウイルス"]) + '''
''' + P('感染に必要なのは、遺伝物質だけではありません。細胞に結合して侵入するための構造（エンベロープと膜のタンパク質など）がはたらかなくなると、遺伝物質が残っていても感染性を失います。') + '''
<h3>手洗いの2つのはたらき</h3>
<p>セッケンでの手洗いには、①界面活性剤がエンベロープをこわしてウイルスの感染性を失わせるはたらきと、②手についたウイルスや汚れを皮ふから引きはなして水で洗い流すはたらきがあります。②はエンベロープの有無に関係なくはたらくので、エンベロープをもたないウイルスに対しても、ていねいな手洗いは有効です。</p>
<h3>このシミュレーターのモデル</h3>
<p>分子の動きは、作用のしくみを見やすく示すための模式的なアニメーションで、分子どうしの力を計算したものではありません。分子の大きさや数、変化にかかる時間は実際とはちがいます。実際のエンベロープには多くの種類の脂質とタンパク質が含まれ、ウイルスの細胞への侵入のしかた（膜の融合、細胞に取りこまれるなど）も種類によってさまざまです。エタノールや洗剤の効き方は、濃度・作用させる時間・ウイルスの種類によって変わります。エンベロープをもたないウイルスは「影響を受けにくい代表的なモデル」として表しており、実際にはエタノールで感染性が下がるものもあります。消毒の具体的な方法は、厚生労働省など公的機関の情報を確認してください。</p>
<h2>参考</h2>
<ul>
<li>''' + A(MEXT_KOU, "文部科学省 高等学校学習指導要領（平成30年告示）解説 理科編") + '''（生物（2）生命現象と物質）</li>
<li>厚生労働省「新型コロナウイルスの消毒・除菌方法について」「ノロウイルスに関するQ&amp;A」</li>
<li>高等学校「生物」「生物基礎」の教科書（生体膜、タンパク質の構造と変性、ウイルス）</li>
</ul>
'''

sim(slug="virus-sekken-alcohol", cat="rika", emoji="🧴", score=79,
    title="ウイルスと洗剤・アルコールのシミュレーター（エンベロープと界面活性剤・エタノール）",
    title_tag="ウイルスのエンベロープと洗剤・アルコールのシミュレーター｜界面活性剤が膜をこわすしくみ（高校生物）",
    meta_desc="エンベロープをもつウイルスともたないウイルスを並べ、洗剤の界面活性剤やエタノールを加えたときに、脂質二重層と膜のタンパク質に何が起こり、なぜ感染できなくなるのかを観察できるシミュレーター。エンベロープの断面の拡大表示、細胞への結合・侵入の比較ができます。",
    og_title="ウイルスと洗剤・アルコールのシミュレーター（エンベロープと界面活性剤・エタノール）",
    og_desc="セッケンやアルコールは、ウイルスのどこに作用する？界面活性剤が脂質二重層に入りこんで膜がばらばらになる様子と、エンベロープをもたないウイルスとのちがいを、分子の動きで見る。",
    card_desc="エンベロープをもつ・もたないウイルスに洗剤やエタノールを加え、膜とタンパク質の変化と感染性を比べる。",
    lead="左がエンベロープ（脂質二重層の膜）をもつウイルス、右がもたないウイルスです。洗剤の界面活性剤やエタノールを加えると、膜の脂質や膜のタンパク質に何が起こるでしょうか。エンベロープの断面を拡大して分子の動きを見たり、細胞に近づけて感染できるかを確かめたりしながら、手洗いと消毒のしくみを分子から考えてみましょう。",
    model="生物 細胞と分子（生体膜・タンパク質の変性の応用：ウイルスと手洗い・消毒）",
    level="高校（生物・生物基礎）",
    unit="高等学校 生物（2）生命現象と物質 ア（ｱ）細胞と分子 ㋐生体物質と細胞",
    canvas=canvas(640, 590, light=True),
    controls=select("sub", "加える物質", [("surf", "洗剤（界面活性剤）"), ("eth", "エタノール")])
             + select("view", "表示", [("whole", "2つのウイルスの全体"), ("zoom", "エンベロープの断面を拡大")])
             + select("spd", "速さ", [("1", "×1"), ("2", "×2"), ("0.5", "×0.5（ゆっくり）")]),
    buttons=btn("add", "▶ 加える", True) + btn("test", "🦠 細胞に近づける") + btn("reset", "↺ 新しいウイルスにもどす") + btn("pause", "⏸ 一時停止") + btn("names", "🏷 名前をかくす"),
    stats=stats([("sV1", "感染性（エンベロープあり）", True), ("sV2", "感染性（エンベロープなし）", True), ("sE", "エンベロープの残り", False), ("sP", "膜のタンパク質のはたらき", False)]),
    legend="赤い頭＋黄色の尾2本＝エンベロープの脂質、青い頭＋黄色の尾1本＝界面活性剤、紫＝エタノール、青緑＝膜のタンパク質（細胞への結合に必要）、うす紫の丸＝カプシドのタンパク質、オレンジの線＝遺伝物質。下の段は細胞の表面で、Y字形が受容体です。",
    article=ARTICLE,
    faqs=[("セッケンや洗剤がウイルスに効くのはなぜ？", "セッケンや洗剤にふくまれる界面活性剤は、親水部と疎水部をもつ分子です。疎水部がウイルスのエンベロープ（脂質二重層）に入りこみ、膜を脂質と界面活性剤のまざった小さな集まりに分けてこわします。エンベロープと膜のタンパク質を失ったウイルスは、細胞に結合・侵入できなくなります。"),
          ("エンベロープとは何？", "一部のウイルスが、タンパク質の殻（カプシド）の外側にもつ脂質二重層の膜です。ウイルスが細胞から出るときに細胞の膜をまとってできるもので、細胞膜と同じくリン脂質が主成分です。膜には、細胞への結合に必要なウイルスのタンパク質がうまっています。"),
          ("エタノールはウイルスのどこに作用するの？", "エタノールは、エンベロープの脂質の並びを乱して膜をこわすとともに、タンパク質の立体構造を変えて（変性させて）はたらきを失わせます。そのため、エンベロープをもつウイルスにはよく効きます。効果は濃度や作用させる時間によって変わります。"),
          ("エンベロープをもたないウイルスには効かないの？", "エンベロープをもたないウイルスは、いちばん外側がタンパク質の殻（カプシド）で、界面活性剤が作用する脂質の膜がありません。エタノールも一般に効きにくいとされますが、ウイルスの種類や条件によってちがいます。ノロウイルスなどでは、流水とセッケンによるていねいな手洗いで洗い流すことや、次亜塩素酸ナトリウムによる消毒が勧められています。"),
          ("遺伝物質が残っているのに、なぜ感染しなくなるの？", "ウイルスが感染するには、細胞の受容体に結合し、細胞の中に遺伝物質を送りこむ必要があります。そのはたらきをしているのが、エンベロープや表面のタンパク質です。これらがこわれると、遺伝物質が無事でも細胞に入れないので、感染性を失います。"),
          ("手洗いには、ウイルスをこわす以外のはたらきもあるの？", "あります。界面活性剤は、手についたウイルスや油汚れを皮ふから引きはなし、水といっしょに洗い流します。このはたらきはエンベロープの有無に関係しないので、どのウイルスに対しても、ていねいな手洗いは大切です。")],
    rel=[("sekken-shabondama", "🫧", "セッケン・シャボン玉・細胞膜のシミュレーター"), ("rinshishitsu-maku", "🧼", "リン脂質と細胞膜のでき方シミュレーター"),
         ("kouso-shikkatsu", "🌡️", "酵素の失活シミュレーター"), ("kansen-agent", "🦠", "感染はこう広がる SIRシミュレーター"), ("maku-yuso", "🚪", "膜輸送のシミュレーター")],
    js=JS)
