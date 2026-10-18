# -*- coding: utf-8 -*-
"""理科の授業向けシミュ（小学4年）
   tenki-kion    … 小4 B（4）天気の様子（天気と1日の気温／水の蒸発と結露）
   atatamarikata … 小4 A（2）金属，水，空気と温度（温まり方が主。温度と体積も切りかえで）"""
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

MEXT_SHO = "https://www.mext.go.jp/a_menu/shotou/new-cs/1387014.htm"
def A(url, label): return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, label)
def NW(t): return '<span style="white-space:nowrap">%s</span>' % t

# 2本で共通の描画ヘルパー（JS）
HELP = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const FF='"Hiragino Sans","Hiragino Kaku Gothic ProN","Noto Sans JP","Yu Gothic UI","Yu Gothic",Meiryo,sans-serif';
  function tx(s,x,y,size,col,align,bold){ ctx.font=(bold?'bold ':'')+size+'px '+FF; ctx.fillStyle=col; ctx.textAlign=align||'left'; ctx.fillText(s,x,y); ctx.textAlign='left'; }
  function tw(s,size,bold){ ctx.font=(bold?'bold ':'')+size+'px '+FF; return ctx.measureText(s).width; }
  function rr(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
  function panel(x,y,w,h){ ctx.fillStyle='#fff'; ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1.2; rr(x,y,w,h,10); ctx.fill(); ctx.stroke(); }
  function tag(s,x,y,size,col,align){ const w=tw(s,size,true), x0=align==='right'?x-w:align==='center'?x-w/2:x; ctx.fillStyle='rgba(255,255,255,0.94)'; rr(x0-4,y-size-1,w+8,size+6,5); ctx.fill(); tx(s,x0,y,size,col,'left',true); }
  function mix(a,b,t){ const p=h=>[1,3,5].map(i=>parseInt(h.substr(i,2),16)), A=p(a), B=p(b); return 'rgb('+A.map((x,i)=>Math.round(x+(B[i]-x)*clamp(t,0,1))).join(',')+')'; }
  function dot(x,y,r,fill,stroke){ ctx.fillStyle=fill; ctx.beginPath(); ctx.arc(x,y,r,0,6.2832); ctx.fill(); if(stroke){ ctx.strokeStyle=stroke; ctx.lineWidth=1; ctx.stroke(); } }
  function flame(x,y,s){ ctx.fillStyle='#f97316'; ctx.beginPath(); ctx.moveTo(x,y-1.9*s); ctx.bezierCurveTo(x+1.15*s,y-0.6*s,x+0.95*s,y+0.7*s,x,y+0.75*s); ctx.bezierCurveTo(x-0.95*s,y+0.7*s,x-1.15*s,y-0.6*s,x,y-1.9*s); ctx.fill();
    ctx.fillStyle='#fde047'; ctx.beginPath(); ctx.moveTo(x,y-0.9*s); ctx.bezierCurveTo(x+0.6*s,y-0.2*s,x+0.5*s,y+0.5*s,x,y+0.55*s); ctx.bezierCurveTo(x-0.5*s,y+0.5*s,x-0.6*s,y-0.2*s,x,y-0.9*s); ctx.fill(); }
  function sunIcon(x,y,r){ ctx.strokeStyle='#f59e0b'; ctx.lineWidth=2.2; for(let k=0;k<8;k++){ const a=k*Math.PI/4; ctx.beginPath(); ctx.moveTo(x+Math.cos(a)*(r+3),y+Math.sin(a)*(r+3)); ctx.lineTo(x+Math.cos(a)*(r+8),y+Math.sin(a)*(r+8)); ctx.stroke(); } dot(x,y,r,'#fbbf24','#f59e0b'); }
  function cloudIcon(x,y,s,col){ ctx.fillStyle=col; ctx.beginPath(); ctx.arc(x-s*0.55,y+s*0.1,s*0.42,0,6.2832); ctx.arc(x,y-s*0.18,s*0.55,0,6.2832); ctx.arc(x+s*0.6,y+s*0.12,s*0.4,0,6.2832); ctx.fill(); rr(x-s*0.95,y+s*0.05,s*1.9,s*0.47,s*0.2); ctx.fill(); }
  const K=id=>$(id).previousElementSibling;
  function sh(id,m,sub){ const e=$(id); if(e) e.innerHTML=m+(sub?'<span style="display:block;font-size:12px;font-weight:700;color:#59616c;margin-top:2px">'+sub+'</span>':''); }
  function show(id,on){ const e=$(id); if(e) e.style.display=on?'':'none'; }
  function showF(id,on){ const e=$(id), f=e?e.closest('.field'):null; if(f) f.style.display=on?'':'none'; }
  const Q=new URLSearchParams(location.search);
'''

# ============================================================ 1 天気の様子（天気と気温・水のゆくえ）
JS_TENKI = HELP + r'''
  const C={bg:'#f8fafc',ink:'#0f172a',sub:'#64748b',grid:'#e2e8f0'};
  // 1日の気温のモデル（春〜秋のおだやかな日の目安）：6時に最低、14時（午後2時）に最高。T＝最低＋上がり幅×f(t)
  const WX={hare:{nm:'晴れ',lo:12,amp:11,col:'#ea580c',sun:7,gnd:4,gn:1},kumori:{nm:'くもり',lo:14,amp:4,col:'#64748b',sun:1.5,gnd:1,gn:0.3},ame:{nm:'雨',lo:13.4,amp:1.5,col:'#2563eb',sun:0,gnd:0,gn:0}};
  const WK=['hare','kumori','ame'], PK=['hyou','hinata','jimen'], PN={hyou:'百葉箱',hinata:'日なた',jimen:'地面近く'};
  // 水のゆくえ：はじめの水の高さ 80 mm。ふたなしの入れ物は 日なた 4 mm／日、日かげ 1.5 mm／日 へる（目安）
  const LOC={hinata:{nm:'日なた（まどぎわ）',o:4,c:0.1},hikage:{nm:'日かげ（ろうか）',o:1.5,c:0.05}}, H0=80, DMAX=10;
  // 結ろ：部屋の気温 25℃。しつ度から水てきがつきはじめる温度（露点）を求める（Tetens の式）
  const ROOM={norm:{rh:60,nm:'ふつう'},dry:{rh:40,nm:'かわいている'},wet:{rh:80,nm:'しめっている'}}, TR=25;
  const fday=t=>t<=14?(1-Math.cos(Math.PI*(t-6)/8))/2:0.5+0.5*Math.cos(Math.PI*(t-14)/10);
  const temp=(w,t)=>WX[w].lo+WX[w].amp*fday(t);
  const sunI=t=>Math.max(0,Math.sin(Math.PI*(t-6)/12));
  function reading(w,t,p){ const q=WX[w], s=sunI(t), Tt=temp(w,t); return p==='hinata'?Tt+q.sun*s:(p==='jimen'?Tt+q.gnd*s-q.gn*(1-s):Tt); }
  const es=x=>6.1078*Math.pow(10,7.5*x/(x+237.3));
  function dew(rh){ const a=Math.log10(rh/100*es(TR)/6.1078); return 237.3*a/(7.5-a); }
  function hm(t){ const h=Math.floor(t+1e-6), m=Math.round((t-h)*60); if(h===12&&m===0) return '正午'; return (h<12?'午前':'午後')+(h<12?h:h-12)+'時'+(m?m+'分':''); }
  const r0=x=>Math.round(x);
  let md='kion', w='hare', tm=14, pl='hyou', cmp=true, play=false, day=3, loc='hinata', room='norm', cup=5, tc=180, last=0, tNow=0, vap=[], air=[], drag=null, lastSt=0;
  const DROPS=[]; for(let i=0;i<90;i++) DROPS.push({fx:rnd(-0.92,0.92),fy:rnd(0.04,0.97),th:Math.pow(Math.random(),0.8),r:rnd(1.8,3.6)});
  const WRAP=[]; for(let i=0;i<34;i++) WRAP.push({fx:rnd(0.06,0.94),th:Math.random(),r:rnd(1.6,3.2)});
  for(let i=0;i<46;i++) air.push({x:rnd(20,390),y:rnd(90,340),vx:0,vy:0});
  const hOpen=d=>Math.max(0,H0-LOC[loc].o*d), hCov=d=>H0-LOC[loc].c*d;
  const Td=()=>dew(ROOM[room].rh);
  function dropAmt(){ return clamp((Td()-cup)/6,0,1.25)*clamp(tc/240,0,1); }

  // ---------- ① 1日の気温 ----------
  const GX0=58, GX1=350, GY0=388, GY1=100, gx=t=>GX0+(GX1-GX0)*(t-6)/12, gy=v=>GY0-(GY0-GY1)*v/30;
  const WB=i=>[18+i*122,40,114,42];
  const PB=i=>[404+i*76,382,72,42];
  function wxIcon(k,x,y,s){ if(k==='hare') sunIcon(x,y,s*0.5); else if(k==='kumori') cloudIcon(x,y,s,'#94a3b8'); else { cloudIcon(x,y-3,s,'#64748b'); ctx.strokeStyle='#2563eb'; ctx.lineWidth=2; for(let j=-1;j<=1;j++){ ctx.beginPath(); ctx.moveTo(x+j*s*0.5,y+s*0.55); ctx.lineTo(x+j*s*0.5-3,y+s*0.95); ctx.stroke(); } } }
  function drawKionGraph(){ panel(8,8,382,424); tx('1日の気温の変わり方（目安）',18,28,13.5,C.ink,'left',true);
    WK.forEach((k,i)=>{ const b=WB(i), sel=k===w; ctx.fillStyle=sel?WX[k].col:'#fff'; ctx.strokeStyle=sel?WX[k].col:'#cbd5e1'; ctx.lineWidth=1.5; rr(b[0],b[1],b[2],b[3],10); ctx.fill(); ctx.stroke();
      if(sel){ ctx.fillStyle='rgba(255,255,255,.92)'; ctx.beginPath(); ctx.arc(b[0]+26,b[1]+21,15,0,6.2832); ctx.fill(); }
      wxIcon(k,b[0]+26,b[1]+21,22); tx(WX[k].nm,b[0]+48,b[1]+27,16,sel?'#fff':C.ink,'left',true); });
    ctx.strokeStyle=C.grid; ctx.lineWidth=1; for(let v=5;v<=30;v+=5){ ctx.beginPath(); ctx.moveTo(GX0,gy(v)); ctx.lineTo(GX1,gy(v)); ctx.stroke(); }
    for(let h=7;h<=18;h++){ ctx.beginPath(); ctx.moveTo(gx(h),GY0); ctx.lineTo(gx(h),GY1); ctx.stroke(); }
    for(let v=0;v<=30;v+=5) tx(String(v),GX0-7,gy(v)+4,11,C.sub,'right');
    for(let h=6;h<=18;h+=2) tx(String(h),gx(h),GY0+15,11,C.sub,'center',true);
    ctx.strokeStyle=C.ink; ctx.lineWidth=1.3; ctx.beginPath(); ctx.moveTo(GX0,GY1-4); ctx.lineTo(GX0,GY0); ctx.lineTo(GX1,GY0); ctx.stroke();
    tx('気温［℃］',18,GY1-8,11,C.sub,'left',true); tx('時こく［時］',GX1,GY0+31,11,C.sub,'right',true);
    tx('← 午前',gx(12)-6,GY0+31,10.5,C.sub,'right',true); tx('午後 →',gx(12)+6,GY0+31,10.5,C.sub,'left',true);
    ctx.setLineDash([3,3]); ctx.strokeStyle='#94a3b8'; ctx.beginPath(); ctx.moveTo(gx(12),GY0+3); ctx.lineTo(gx(12),GY0+22); ctx.stroke(); ctx.setLineDash([]);
    const line=(k,lw,al)=>{ ctx.globalAlpha=al; ctx.strokeStyle=WX[k].col; ctx.lineWidth=lw; ctx.beginPath(); for(let t=6;t<=18.001;t+=0.1){ const X=gx(t), Y=gy(temp(k,t)); if(t===6) ctx.moveTo(X,Y); else ctx.lineTo(X,Y); } ctx.stroke(); ctx.globalAlpha=1; };
    if(cmp) WK.forEach(k=>{ if(k===w) return; line(k,2,0.45); tx(WX[k].nm,GX1+5,gy(temp(k,18))+4,10.5,WX[k].col,'left',true); });
    line(w,3.4,1); tx(WX[w].nm,GX1+5,gy(temp(w,18))+4,10.5,WX[w].col,'left',true); for(let h=6;h<=18;h++) dot(gx(h),gy(temp(w,h)),3.6,'#fff',WX[w].col);
    const mx=temp(w,14); dot(gx(14),gy(mx),5,WX[w].col); tag('いちばん高い '+r0(mx)+'℃（午後2時ごろ）',gx(14),gy(mx)-12,11.5,WX[w].col,'center');
    ctx.setLineDash([5,4]); ctx.strokeStyle='#0f172a'; ctx.lineWidth=1.2; ctx.beginPath(); ctx.moveTo(gx(tm),GY0); ctx.lineTo(gx(tm),GY1); ctx.stroke(); ctx.setLineDash([]);
    const cy=gy(temp(w,tm)); ctx.fillStyle='#fff'; ctx.strokeStyle=C.ink; ctx.lineWidth=2.5; ctx.beginPath(); ctx.arc(gx(tm),cy,6.5,0,7); ctx.fill(); ctx.stroke();
    const lab=hm(tm)+' '+r0(temp(w,tm))+'℃', al=gx(tm)>300?'right':(gx(tm)<110?'left':'center'); tag(lab,gx(tm)+(al==='right'?-8:al==='left'?8:0),Math.min(GY0-10,cy+26),12,C.ink,al);
    if(!drag) tx('グラフを指でなぞると時こくが変わる',GX1,GY0-8,10.5,'#0e7490','right',true); }
  function drawMeasure(){ const x0=398; panel(x0,8,234,424); tx('気温のはかり方',x0+10,28,13.5,C.ink,'left',true);
    const gY=250; ctx.fillStyle='#e0f2fe'; ctx.fillRect(x0+6,36,166,gY-36); ctx.fillStyle='#86efac'; ctx.fillRect(x0+6,gY,166,12); ctx.fillStyle='#a16207'; ctx.fillRect(x0+6,gY+12,166,4);
    const s=sunI(tm), sx=x0+20+136*(tm-6)/12, sy=gY-26-150*s;
    if(w==='hare'){ if(s>0.02) sunIcon(sx,sy,11); } else { if(s>0.02&&w==='kumori'){ ctx.globalAlpha=0.5; sunIcon(sx,sy,10); ctx.globalAlpha=1; } cloudIcon(x0+70,62,30,w==='ame'?'#94a3b8':'#cbd5e1'); cloudIcon(x0+132,74,24,w==='ame'?'#94a3b8':'#cbd5e1');
      if(w==='ame'){ ctx.strokeStyle='rgba(37,99,235,.65)'; ctx.lineWidth=1.4; for(let i=0;i<14;i++){ const xx=x0+24+((i*37+tNow*60)%140), yy=92+((i*53+tNow*180)%140); ctx.beginPath(); ctx.moveTo(xx,yy); ctx.lineTo(xx-3,yy+9); ctx.stroke(); } } }
    // 百葉箱
    const bx=x0+58, bw=62, by=150, bh=52; ctx.strokeStyle='#94a3b8'; ctx.lineWidth=3; [bx+8,bx+bw-8].forEach(lx=>{ ctx.beginPath(); ctx.moveTo(lx,by+bh); ctx.lineTo(lx,gY); ctx.stroke(); });
    ctx.fillStyle='#fff'; ctx.strokeStyle='#64748b'; ctx.lineWidth=1.4; ctx.fillRect(bx,by,bw,bh); ctx.strokeRect(bx,by,bw,bh);
    ctx.beginPath(); ctx.moveTo(bx-6,by); ctx.lineTo(bx+bw/2,by-14); ctx.lineTo(bx+bw+6,by); ctx.closePath(); ctx.fillStyle='#f8fafc'; ctx.fill(); ctx.stroke();
    ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1; for(let yy=by+7;yy<by+bh;yy+=7){ ctx.beginPath(); ctx.moveTo(bx+4,yy); ctx.lineTo(bx+bw-4,yy-3); ctx.stroke(); }
    tx('百葉箱',bx+bw/2,by-18,10.5,C.sub,'center',true);
    // 高さの目もり
    ctx.strokeStyle='#0e7490'; ctx.lineWidth=1.4; ctx.beginPath(); ctx.moveTo(x0+30,gY); ctx.lineTo(x0+30,by+bh/2); ctx.stroke(); [gY,by+bh/2].forEach(yy=>{ ctx.beginPath(); ctx.moveTo(x0+24,yy); ctx.lineTo(x0+36,yy); ctx.stroke(); });
    ctx.save(); ctx.translate(x0+22,(gY+by+bh/2)/2); ctx.rotate(-Math.PI/2); tx('1.2〜1.5 m',0,0,10.5,'#0e7490','center',true); ctx.restore();
    // 温度計の場所
    const th=(x,y,hl)=>{ ctx.fillStyle='#fff'; ctx.strokeStyle='#475569'; ctx.lineWidth=1.2; rr(x-3,y-22,6,26,3); ctx.fill(); ctx.stroke(); dot(x,y+5,4,'#ef4444','#475569'); if(hl){ ctx.strokeStyle='#dc2626'; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(x,y-6,17,0,6.2832); ctx.stroke(); } };
    if(pl==='hyou'){ ctx.fillStyle='rgba(255,255,255,.85)'; ctx.fillRect(bx+22,by+8,18,bh-14); th(bx+31,by+30,true); }
    else if(pl==='hinata'){ const hx=x0+150, hy=206; ctx.strokeStyle='#94a3b8'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(hx,hy+8); ctx.lineTo(hx,gY); ctx.stroke(); th(hx,hy,true);
      if(w==='hare'&&s>0.05){ ctx.strokeStyle='rgba(245,158,11,.75)'; ctx.lineWidth=2; ctx.setLineDash([4,4]); ctx.beginPath(); ctx.moveTo(sx,sy); ctx.lineTo(hx,hy-10); ctx.stroke(); ctx.setLineDash([]); } }
    else { ctx.save(); ctx.translate(x0+150,gY-5); ctx.rotate(-Math.PI/2); th(0,0,false); ctx.restore(); ctx.strokeStyle='#dc2626'; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(x0+150,gY-5,17,0,6.2832); ctx.stroke(); }
    // 大きな温度計
    const R=reading(w,tm,pl), tX=x0+204, tT=50, tB=318, ty=v=>tB-(tB-tT)*v/40;
    ctx.fillStyle='#fff'; ctx.strokeStyle='#475569'; ctx.lineWidth=1.5; rr(tX-9,tT-10,18,tB-tT+20,9); ctx.fill(); ctx.stroke(); dot(tX,tB+18,12,'#ef4444','#475569');
    ctx.fillStyle='#ef4444'; ctx.fillRect(tX-3,ty(clamp(R,0,40)),6,tB+10-ty(clamp(R,0,40)));
    for(let v=0;v<=40;v++){ const yy=ty(v), L=v%10===0?11:(v%5===0?8:4); ctx.strokeStyle='#334155'; ctx.lineWidth=v%5===0?1.2:0.7; ctx.beginPath(); ctx.moveTo(tX-9,yy); ctx.lineTo(tX-9-L,yy); ctx.stroke(); if(v%10===0) tx(String(v),tX-22,yy+4,10,C.sub,'right',true); }
    tx('℃',tX-24,tT-14,10,C.sub,'left',true);
    // 文字
    tx(hm(tm),x0+12,284,13,C.ink,'left',true); tx('温度計の目もり',x0+12,304,11,C.sub,'left',true); tx(r0(R)+'℃',x0+12,336,28,pl==='hyou'?'#dc2626':'#9a3412','left',true);
    const d=R-temp(w,tm), msg=pl==='hyou'?['正しいはかり方','（気温）']:(Math.abs(d)<0.5?['気温とほぼ同じ',''] :[(d>0?'気温より '+r0(d)+'℃ 高い':'気温より '+r0(-d)+'℃ 低い'),'正しくはかれない']);
    tx(msg[0],x0+12,356,11.5,pl==='hyou'?'#15803d':'#b45309','left',true); if(msg[1]) tx(msg[1],x0+12,372,11,C.sub,'left',true);
    PK.forEach((k,i)=>{ const b=PB(i), sel=k===pl; ctx.fillStyle=sel?'#0e7490':'#fff'; ctx.strokeStyle=sel?'#0e7490':'#cbd5e1'; ctx.lineWidth=1.3; rr(b[0],b[1],b[2],b[3],9); ctx.fill(); ctx.stroke(); tx(PN[k],b[0]+b[2]/2,b[1]+26,12.5,sel?'#fff':C.ink,'center',true); }); }

  // ---------- ② 水のゆくえ ----------
  const CUPS=[[56,118],[236,118]], CB=360, MM=2.2;
  function drawEvap(){ panel(8,8,412,424); tx('水のゆくえ：ふたなし と ふたあり',18,28,13.5,C.ink,'left',true); tx(LOC[loc].nm+'に '+(day<0.05?'置いたところ':Math.floor(day+1e-6)+'日 置いた'),18,47,11.5,C.sub,'left',true);
    if(loc==='hinata') sunIcon(392,52,11); else { ctx.fillStyle='#e2e8f0'; rr(352,38,60,22,6); ctx.fill(); tx('日かげ',382,54,11,C.sub,'center',true); }
    const ho=hOpen(day), hc=hCov(day), wd=clamp(day*(loc==='hinata'?1.6:0.8),0,1);
    CUPS.forEach((c,k)=>{ const x=c[0], wdt=c[1], top=CB-H0*MM-56, hh=k?hc:ho, wy=CB-hh*MM;
      ctx.fillStyle='rgba(125,211,252,.45)'; ctx.fillRect(x,wy,wdt,CB-wy); ctx.strokeStyle='rgba(2,132,199,.7)'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.moveTo(x,wy); ctx.lineTo(x+wdt,wy); ctx.stroke();
      if(k&&wd>0){ ctx.fillStyle='rgba(148,163,184,'+(0.18*wd)+')'; ctx.fillRect(x+1,top+4,wdt-2,wy-top-4); }
      ctx.strokeStyle='#64748b'; ctx.lineWidth=2.5; ctx.beginPath(); ctx.moveTo(x,top); ctx.lineTo(x,CB); ctx.lineTo(x+wdt,CB); ctx.lineTo(x+wdt,top); ctx.stroke();
      ctx.setLineDash([6,4]); ctx.strokeStyle='#dc2626'; ctx.lineWidth=1.6; ctx.beginPath(); ctx.moveTo(x-4,CB-H0*MM); ctx.lineTo(x+wdt+4,CB-H0*MM); ctx.stroke(); ctx.setLineDash([]);
      for(let v=0;v<=100;v+=10){ const yy=CB-v*MM; if(yy<top) break; ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(x-1,yy); ctx.lineTo(x-(v%50?5:9),yy); ctx.stroke(); if(v%20===0) tx(String(v),x-11,yy+4,9.5,C.sub,'right'); }
      if(k){ ctx.strokeStyle='#94a3b8'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(x-8,top); ctx.quadraticCurveTo(x+wdt/2,top+7,x+wdt+8,top); ctx.stroke(); tx('ラップ',x+wdt+10,top+4,10.5,C.sub,'left',true);
        WRAP.forEach(d=>{ if(d.th<wd){ const dx=x+d.fx*wdt, dy=top+3.5+Math.sin(Math.PI*d.fx)*7*0.5+d.r; dot(dx,dy,d.r*(0.6+0.4*wd),'rgba(186,230,253,.95)','rgba(2,132,199,.6)'); } }); }
      tx(k?'ふたあり':'ふたなし',x+wdt/2,CB+22,14,k?'#2563eb':'#dc2626','center',true);
      tx(Math.round(hh)+' mm'+(H0-hh>=1?'（'+Math.round(H0-hh)+' mm へった）':(day>0.05?'（ほとんどへらない）':'')),x+wdt/2,CB+42,11.5,C.ink,'center',true); });
    tx('赤い点線＝はじめの水面の印',18,CB+62,10.5,'#dc2626','left',true);
    vap.forEach(p=>dot(p.x,p.y,2.2,'rgba(56,189,248,'+(0.75*p.a)+')'));
    if(vap.length) tx('水じょう気（目に見えない・イメージ）',CUPS[0][0]-6,CB-H0*MM-70,10.5,'#0369a1','left',true); }
  function drawEvapGraph(){ const x=428; panel(x,8,204,424); tx('水の高さの変わり方',x+10,28,13,C.ink,'left',true);
    const X0=x+34, X1=x+194, Y0=230, Y1=56, ex=d=>X0+(X1-X0)*d/DMAX, ey=v=>Y0-(Y0-Y1)*v/90;
    ctx.strokeStyle=C.grid; ctx.lineWidth=1; for(let v=20;v<=80;v+=20){ ctx.beginPath(); ctx.moveTo(X0,ey(v)); ctx.lineTo(X1,ey(v)); ctx.stroke(); } for(let d=2;d<=DMAX;d+=2){ ctx.beginPath(); ctx.moveTo(ex(d),Y0); ctx.lineTo(ex(d),Y1); ctx.stroke(); }
    for(let v=0;v<=80;v+=20) tx(String(v),X0-5,ey(v)+4,10,C.sub,'right'); for(let d=0;d<=DMAX;d+=2) tx(String(d),ex(d),Y0+14,10,C.sub,'center');
    ctx.strokeStyle=C.ink; ctx.lineWidth=1.2; ctx.beginPath(); ctx.moveTo(X0,Y1-4); ctx.lineTo(X0,Y0); ctx.lineTo(X1,Y0); ctx.stroke();
    tx('［mm］',x+8,Y1-8,10,C.sub,'left',true); tx('日数［日］',X1,Y0+29,10,C.sub,'right',true);
    [[hOpen,'#dc2626'],[hCov,'#2563eb']].forEach(q=>{ ctx.strokeStyle=q[1]; ctx.lineWidth=2.6; ctx.beginPath(); ctx.moveTo(ex(0),ey(q[0](0))); ctx.lineTo(ex(day),ey(q[0](day))); ctx.stroke(); dot(ex(day),ey(q[0](day)),4.5,'#fff',q[1]); });
    tx('ふたあり',ex(day)>X0+90?X0+6:X1-4,ey(hCov(day))-8,10.5,'#2563eb',ex(day)>X0+90?'left':'right',true); tx('ふたなし',X0+6,Y0-8,10.5,'#dc2626','left',true);
    const M=day<0.05?['同じ高さまで水を入れて、','印をつけた。','日がたつと、どうなる？','「▶ 日をすすめる」','をおしてみよう。']
      :['ふたなしの水はへった。','水は じょう発して','水じょう気になり、','空気中へ出ていった。','ふたありは、ほとんど','へらない。ラップの内側に','水てきがついている。'];
    M.forEach((s,i)=>tx(s,x+12,268+i*20,11.5,i<4?C.ink:'#1d4ed8','left',true)); }

  // ---------- ③ 結ろ ----------
  const CX=196, CT=120, CBt=345, CWt=64, CWb=52, cupX=(fy,fx)=>CX+fx*(CWt+(CWb-CWt)*fy), cupY=fy=>CT+(CBt-CT)*fy;
  function drawDew(){ panel(8,8,392,424); tx('冷たい水を入れたコップ',18,28,13.5,C.ink,'left',true); tx('部屋の気温 '+TR+'℃・空気が'+ROOM[room].nm,18,47,11.5,C.sub,'left',true);
    const d=dropAmt();
    air.forEach(p=>dot(p.x,p.y,2.2,'rgba(56,189,248,.6)'));
    dot(26,70,2.6,'rgba(56,189,248,.8)'); tx('＝水じょう気（目に見えない・イメージ）',32,74,10.5,'#0369a1','left',true);
    ctx.fillStyle='#d6d3d1'; ctx.fillRect(18,CBt+2,372,8);
    if(d>0.75) { ctx.fillStyle='rgba(125,211,252,.55)'; ctx.beginPath(); ctx.ellipse(CX,CBt+3,CWb+10+18*(d-0.75),5,0,0,6.2832); ctx.fill(); }
    const wy=CT+30, wc=mix('#bae6fd','#e0f2fe',clamp(cup/30,0,1));
    ctx.fillStyle=wc; ctx.beginPath(); ctx.moveTo(cupX(0.13,-1),wy); ctx.lineTo(cupX(0.13,1),wy); ctx.lineTo(cupX(1,1),CBt); ctx.lineTo(cupX(1,-1),CBt); ctx.closePath(); ctx.fill();
    if(cup<=5){ [[-30,wy+4],[4,wy+12],[20,wy-2]].forEach((q,i)=>{ ctx.fillStyle='rgba(255,255,255,.85)'; ctx.strokeStyle='#7dd3fc'; ctx.lineWidth=1.2; ctx.save(); ctx.translate(CX+q[0],q[1]); ctx.rotate(0.3*i-0.2); rr(-12,-12,24,24,5); ctx.fill(); ctx.stroke(); ctx.restore(); }); tag('氷水',CX-56,wy+44,11,'#0369a1','left'); }
    ctx.strokeStyle='#475569'; ctx.lineWidth=1.2; ctx.fillStyle='#fff'; rr(CX+30,CT-40,7,140,3.5); ctx.fill(); ctx.stroke(); dot(CX+33.5,CT+104,5,'#ef4444','#475569'); ctx.fillStyle='#ef4444'; ctx.fillRect(CX+32,CT+100-cup*2.6,3,cup*2.6+2);
    tag(cup+'℃',CX+42,CT-28,12.5,'#1d4ed8','left');
    ctx.strokeStyle='#64748b'; ctx.lineWidth=2.5; ctx.beginPath(); ctx.moveTo(cupX(0,-1),CT); ctx.lineTo(cupX(1,-1),CBt); ctx.lineTo(cupX(1,1),CBt); ctx.lineTo(cupX(0,1),CT); ctx.stroke();
    if(d>0.02){ ctx.fillStyle='rgba(148,163,184,'+(0.22*Math.min(1,d))+')'; ctx.beginPath(); ctx.moveTo(cupX(0.13,-1),wy); ctx.lineTo(cupX(0.13,1),wy); ctx.lineTo(cupX(1,1),CBt); ctx.lineTo(cupX(1,-1),CBt); ctx.closePath(); ctx.fill(); }
    DROPS.forEach(q=>{ if(q.fy<0.13||q.th>=d) return; const yy=cupY(q.fy)+(d>0.9&&q.th<0.25?(d-0.9)*60*q.fy:0), xx=cupX(q.fy,q.fx); const rr_=q.r*(0.55+0.45*Math.min(1,d)), yd=Math.min(CBt-3,yy); dot(xx,yd,rr_,'rgba(224,242,254,.95)','rgba(3,105,161,.9)'); dot(xx-rr_*0.35,yd-rr_*0.35,rr_*0.3,'#fff'); });
    if(d>0.02){ const ax=cupX(0.62,1), ay=cupY(0.62); ctx.strokeStyle='#0369a1'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.moveTo(ax+26,ay-14); ctx.lineTo(ax+4,ay); ctx.stroke(); tag('外側の水てき',ax+28,ay-14,11.5,'#0369a1','left'); }
    const m=d>0.02?['コップの外側に 水てき がついた！','空気中の水じょう気が冷やされて、','水にもどった（結ろ）。']:(cup<Td()?['まだ水てきは小さい。','少し待つと…']:['水てきはつかない。','コップがあまり冷たくないから。']);
    m.forEach((s,i)=>tx(s,18,384+i*17,i?11.5:12.5,i?C.ink:(d>0.02?'#0369a1':C.sub),'left',true)); }
  const BX=462, BT=66, BBt=360, by=v=>BBt-(BBt-BT)*v/30;
  function drawDewBar(){ const x=408; panel(x,8,224,424); tx('水てきがつく温度（目安）',x+10,28,13,C.ink,'left',true);
    const td=Td();
    ctx.fillStyle='rgba(125,211,252,.25)'; ctx.fillRect(BX-14,by(td),x+218-(BX-14),BBt-by(td));
    const g=ctx.createLinearGradient(0,BBt,0,BT); g.addColorStop(0,'#60a5fa'); g.addColorStop(0.55,'#e2e8f0'); g.addColorStop(1,'#fb923c'); ctx.fillStyle=g; rr(BX-8,BT,16,BBt-BT,8); ctx.fill(); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1; rr(BX-8,BT,16,BBt-BT,8); ctx.stroke();
    for(let v=0;v<=30;v+=5){ ctx.strokeStyle='#64748b'; ctx.beginPath(); ctx.moveTo(BX-14,by(v)); ctx.lineTo(BX-8,by(v)); ctx.stroke(); tx(String(v),BX-17,by(v)+4,10,C.sub,'right'); }
    tx('［℃］',x+8,BT-12,10,C.sub,'left',true);
    const L=[[by(TR),'部屋の気温 '+TR+'℃','#ea580c'],[by(td),'水てきがつきはじめる 約'+r0(td)+'℃','#0e7490'],[by(cup),'コップの水 '+cup+'℃','#1d4ed8']];
    ctx.setLineDash([5,4]); ctx.strokeStyle='#0e7490'; ctx.lineWidth=1.6; ctx.beginPath(); ctx.moveTo(BX-14,by(td)); ctx.lineTo(x+218,by(td)); ctx.stroke(); ctx.setLineDash([]);
    ctx.strokeStyle='#ea580c'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(BX-12,by(TR)); ctx.lineTo(BX+12,by(TR)); ctx.stroke();
    ctx.fillStyle='#1d4ed8'; ctx.beginPath(); ctx.moveTo(BX+10,by(cup)); ctx.lineTo(BX+22,by(cup)-7); ctx.lineTo(BX+22,by(cup)+7); ctx.closePath(); ctx.fill();
    const ys=L.map(q=>q[0]+4), ord=[0,1,2].sort((a,b)=>ys[a]-ys[b]); for(let k=1;k<3;k++){ const a=ord[k-1], b=ord[k]; if(ys[b]-ys[a]<17) ys[b]=ys[a]+17; }
    L.forEach((q,i)=>{ const s=q[1]; if(i===1){ const p=s.split(' '); tag(p[0],BX+26,ys[i],10.5,q[2],'left'); tag(p[1],BX+26,ys[i]+15,11,q[2],'left'); if(ys[2]>ys[1]&&ys[2]-ys[1]<32) ys[2]=ys[1]+32; } else tag(s,BX+26,ys[i],11,q[2],'left'); });
    tx('この温度より冷たいと',x+10,BBt+24,11,'#0e7490','left',true); tx('水てきがつく',x+10,BBt+40,11,'#0e7490','left',true);
    tx('コップの温度を指で上下に動かせる',x+10,BBt+60,10,C.sub,'left',true); }

  // ---------- 統計欄 ----------
  function stats(){ if(md==='kion'){ const q=WX[w], R=reading(w,tm,pl), mx=temp(w,14), mn=temp(w,6);
      K('sA').innerHTML='天気'; sh('sA',q.nm,'午前6時〜午後6時');
      K('sB').innerHTML='温度計の目もり'; sh('sB',r0(R)+'℃',hm(tm)+'・'+PN[pl]);
      K('sC').innerHTML='いちばん高い気温'; sh('sC',r0(mx)+'℃','午後2時ごろ');
      K('sD').innerHTML='1日の気温の差'; sh('sD',r0(mx-mn)+'℃','いちばん低い '+r0(mn)+'℃（朝）');
      setShare('【天気と気温】'+q.nm+'の日の気温は朝 約'+r0(mn)+'℃→午後2時ごろ 約'+r0(mx)+'℃（差 約'+r0(mx-mn)+'℃）。晴れの日は山の形、くもり・雨の日は変化が小さい｜シミュラボ'); }
    else if(md==='evap'){ const ho=hOpen(day), hc=hCov(day), dd=Math.floor(day+1e-6);
      K('sA').innerHTML='置いた日数'; sh('sA',dd+'日',LOC[loc].nm);
      K('sB').innerHTML='ふたなしの水'; sh('sB',Math.round(ho)+' mm',Math.round(H0-ho)+' mm へった');
      K('sC').innerHTML='ふたありの水'; sh('sC',Math.round(hc)+' mm',H0-hc<1?'ほとんどへらない':Math.round(H0-hc)+' mm へった');
      K('sD').innerHTML='へった水のゆくえ'; sh('sD','水じょう気','じょう発して空気中へ');
      setShare('【水のゆくえ】'+LOC[loc].nm+'に'+dd+'日置くと、ふたなしの水は'+(H0-ho).toFixed(0)+' mmへり、ふたありはほとんどへらない。水はじょう発して水じょう気になり、空気中へ出ていく｜シミュラボ'); }
    else { const td=Td(), d=dropAmt();
      K('sA').innerHTML='コップの水の温度'; sh('sA',cup+'℃',cup<=5?'氷水':(cup<20?'冷たい水':'あまり冷たくない'));
      K('sB').innerHTML='外側の水てき'; sh('sB',d>0.02?'つく':(cup<td?'つきはじめ':'つかない'),'置いてから '+Math.round(tc/60)+'分');
      K('sC').innerHTML='水てきがつく温度'; sh('sC','約'+r0(td)+'℃','先生向け：露点');
      K('sD').innerHTML='部屋の空気'; sh('sD',TR+'℃・'+ROOM[room].rh+'%','気温・しつ度');
      setShare('【結ろ】気温'+TR+'℃・しつ度'+ROOM[room].rh+'%の部屋では、コップの水が約'+r0(td)+'℃より冷たいと外側に水てきがつく（空気中の水じょう気が冷やされて水にもどる）｜シミュラボ'); } }
  function vis(){ const k=md==='kion', e=md==='evap', d=md==='dew'; showF('wx',k); showF('tm',k); showF('loc',e); showF('day',e); showF('room',d); showF('cup',d); show('cmp',k);
    $('play').textContent=k?(play?'⏸ 止める':'▶ 1日を早送り'):(e?(play?'⏸ 止める':'▶ 日をすすめる'):'🧊 コップを置きなおす');
    $('cmp').textContent=cmp?'📈 3つの天気をくらべる：ON':'📈 3つの天気をくらべる：OFF'; }
  function syncL(){ $('tm').value=tm; $('tmL').textContent=hm(tm); $('day').value=Math.floor(day+1e-6); $('dayL').textContent=Math.floor(day+1e-6)+'日'; $('cup').value=cup; $('cupL').textContent=cup+'℃'; $('wx').value=w; }
  function draw(){ ctx.fillStyle=C.bg; ctx.fillRect(0,0,W,H); if(md==='kion'){ drawKionGraph(); drawMeasure(); } else if(md==='evap'){ drawEvap(); drawEvapGraph(); } else { drawDew(); drawDewBar(); } }
  function stepVis(dt){ if(md==='evap'){ const ro=LOC[loc].o*(play?2.5:1);
      if(Math.random()<dt*ro*3) vap.push({x:CUPS[0][0]+rnd(6,CUPS[0][1]-6),y:CB-hOpen(day)*MM-2,a:1,k:0});
      if(Math.random()<dt*ro*2) vap.push({x:CUPS[1][0]+rnd(6,CUPS[1][1]-6),y:CB-hCov(day)*MM-2,a:1,k:1});
      const top=CB-H0*MM-56; vap.forEach(p=>{ p.y-=dt*(22+rnd(0,10)); p.x+=rnd(-1,1)*dt*30; if(p.k){ if(p.y<top+8){ p.y=top+8; p.a-=dt*1.5; } } else if(p.y<top) p.a-=dt*0.8; }); vap=vap.filter(p=>p.a>0&&p.y>20); }
    else if(md==='dew'){ const cold=cup<Td(); air.forEach(p=>{ p.vx+=randn()*60*dt; p.vy+=randn()*60*dt; p.vx*=0.95; p.vy*=0.95;
        if(cold){ const dx=CX-p.x, dy=(CT+CBt)/2-p.y, dd=Math.hypot(dx,dy); if(dd<150){ p.vx+=dx/dd*40*dt; p.vy+=dy/dd*40*dt; } if(Math.abs(dx)<CWt+4&&p.y>CT&&p.y<CBt){ p.x=rnd(20,390); p.y=rnd(90,130); p.vx=p.vy=0; } }
        p.x+=p.vx*dt; p.y+=p.vy*dt; if(p.x<20||p.x>390){ p.vx=-p.vx; p.x=clamp(p.x,20,390); } if(p.y<88||p.y>340){ p.vy=-p.vy; p.y=clamp(p.y,88,340); } }); } }

  // ---------- 操作 ----------
  [['mode','mode'],['wx','wx'],['loc','loc'],['room','room']].forEach(a=>{ if(!Q.has(a[1])) return; const el=$(a[0]), q=Q.get(a[1]); if([].some.call(el.options,o=>o.value===q)) el.value=q; });
  md=$('mode').value; w=$('wx').value; loc=$('loc').value; room=$('room').value;
  if(Q.has('t')) tm=clamp(Math.round((+Q.get('t')||14)*2)/2,6,18); if(Q.has('pl')&&PK.indexOf(Q.get('pl'))>=0) pl=Q.get('pl');
  if(Q.has('day')) day=clamp(+Q.get('day')||0,0,DMAX); if(Q.has('cup')) cup=clamp(Math.round(+Q.get('cup')),0,30); if(Q.get('cmp')==='0') cmp=false;
  $('mode').addEventListener('change',()=>{ md=$('mode').value; play=false; vis(); stats(); });
  $('wx').addEventListener('change',()=>{ w=$('wx').value; stats(); });
  $('loc').addEventListener('change',()=>{ loc=$('loc').value; vap=[]; stats(); });
  $('room').addEventListener('change',()=>{ room=$('room').value; stats(); });
  $('tm').addEventListener('input',()=>{ tm=+$('tm').value; play=false; vis(); syncL(); stats(); });
  $('day').addEventListener('input',()=>{ day=+$('day').value; play=false; vis(); syncL(); stats(); });
  $('cup').addEventListener('input',()=>{ cup=+$('cup').value; syncL(); stats(); });
  $('cmp').addEventListener('click',()=>{ cmp=!cmp; vis(); });
  $('play').addEventListener('click',()=>{ if(md==='dew'){ tc=0; play=true; stats(); return; } if(play){ play=false; } else { if(md==='kion'&&tm>=18) tm=6; if(md==='evap'&&day>=DMAX){ day=0; vap=[]; } play=true; } vis(); syncL(); stats(); });
  cv.addEventListener('pointerdown',e=>{ const p=cpos(cv,e), x=p[0]/dpr, y=p[1]/dpr;
    if(md==='kion'){ for(let i=0;i<3;i++){ const b=WB(i); if(x>=b[0]&&x<=b[0]+b[2]&&y>=b[1]&&y<=b[1]+b[3]){ w=WK[i]; syncL(); stats(); return; } }
      for(let i=0;i<3;i++){ const b=PB(i); if(x>=b[0]&&x<=b[0]+b[2]&&y>=b[1]&&y<=b[1]+b[3]){ pl=PK[i]; stats(); return; } }
      if(x>=GX0-10&&x<=GX1+30&&y>=GY1-10&&y<=GY0+20){ drag='t'; play=false; vis(); } }
    else if(md==='evap'){ if(x>=436&&y>=40&&y<=250){ drag='d'; play=false; vis(); } }
    else { if(x>=408){ drag='c'; } }
    if(drag){ try{ cv.setPointerCapture(e.pointerId); }catch(err){} mv(x,y); } });
  function mv(x,y){ if(drag==='t'){ tm=clamp(Math.round((6+12*(x-GX0)/(GX1-GX0))*2)/2,6,18); } else if(drag==='d'){ day=clamp(Math.round(DMAX*(x-462)/(622-462)),0,DMAX); } else if(drag==='c'){ cup=clamp(Math.round(30*(BBt-y)/(BBt-BT)),0,30); } syncL(); stats(); }
  cv.addEventListener('pointermove',e=>{ if(!drag) return; const p=cpos(cv,e); mv(p[0]/dpr,p[1]/dpr); });
  const up=()=>{ drag=null; }; cv.addEventListener('pointerup',up); cv.addEventListener('pointercancel',up);
  function frame(ts){ const dt=last?Math.min(0.05,(ts-last)/1000):0; last=ts; tNow+=dt;
    if(play&&md==='kion'){ tm=Math.min(18,tm+dt*1.5); if(tm>=18){ play=false; vis(); } syncL(); }
    if(play&&md==='evap'){ day=Math.min(DMAX,day+dt*1.0); if(day>=DMAX){ play=false; vis(); } syncL(); }
    if(md==='dew'&&tc<600){ tc=Math.min(600,tc+dt*60); }
    if(play&&(md!=='dew'||tc<600)){ if(ts-lastSt>120){ lastSt=ts; stats(); } } else if(md==='dew'&&ts-lastSt>500){ lastSt=ts; stats(); }
    stepVis(dt); draw(); requestAnimationFrame(frame); }
  for(let i=0;i<30;i++) stepVis(1/30);
  syncL(); vis(); stats(); draw(); requestAnimationFrame(frame);
'''

TENKI_ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
<p>晴れの日は、朝は気温が低く、昼すぎ（<b>午後2時ごろ</b>）にいちばん高くなります。グラフにすると<b>山の形</b>になります。くもりや雨の日は、太陽の光が雲でさえぎられるので、<b>1日の気温の変わり方が小さく</b>なります。気温は、<b>地面から1.2〜1.5 mの高さで、日光が直接当たらない、風通しのよい所</b>（百葉箱の中など）ではかります。また、入れ物の水は<b>じょう発</b>して<b>水じょう気</b>になって空気中へ出ていくこと、空気中の水じょう気は冷やされると<b>水てきになって現れる（結ろ）</b>ことも確かめられます。</p>
''' + N('<b>対応する単元</b>：小学4年 B（4）天気の様子「（ア）天気によって1日の気温の変化の仕方に違いがあること」「（イ）水は，水面や地面などから蒸発し，水蒸気になって空気中に含まれていくこと。また，空気中の水蒸気は，結露して再び水になって現れることがあること」。学習指導要領解説では、晴れた日は日中に気温が上がる山型のグラフ、曇りや雨の日は高低差の小さいグラフになること、気温は場所を決めて定点で観測すること（百葉箱の利用など）、算数科と関連付けてグラフに表し読み取ることが示されています。') + '''
<h2>授業での使い方</h2>
<h3>導入：天気と気温を予想する</h3>
<p>「晴れの日とくもりの日では、1日の気温の変わり方はちがうだろうか」と問いかけ、予想をノートにかかせてから「① 1日の気温（天気）」を開きます。はじめは「3つの天気をくらべる」をOFFにして晴れだけを見せ、グラフを指でなぞって時こくを動かすと、右の温度計の目もりが動きます。午前9時・正午・午後3時など、実際に観測する時こくの気温を読み取らせます。</p>
<h3>展開：気温の正しいはかり方・天気によるちがい</h3>
<p>右下の「日なた」「地面近く」をおすと、同じ時こくでも温度計の目もりが変わります。晴れた日の昼に日光が直接当たると気温より数℃高く出ることから、百葉箱を使う理由（日光が直接当たらない・風通しがよい・地面から1.2〜1.5 m）を考えさせます。次に「3つの天気をくらべる」をONにし、晴れ・くもり・雨のグラフの形のちがいを話し合います。</p>
<h3>まとめ・発展：水のゆくえ</h3>
<p>「② 水のゆくえ（じょう発）」で、ふたなしとふたあり（ラップ）の入れ物を何日か置いたときの水の高さを比べます。ふたなしの水だけがへること、ふたありはラップの内側に水てきがつくことから、水はじょう発して水じょう気になり、空気中へ出ていくことをまとめます。「③ 水てきがつく（結ろ）」では、氷水を入れたコップの外側に水てきがつく様子から、空気中に水じょう気があることを確かめます。</p>
<h3>児童への問いの例</h3>
<ol>
<li>晴れの日に、気温がいちばん高くなるのは何時ごろだろう？太陽がいちばん高くなる正午ではないのはなぜだろう？</li>
<li>温度計に日光が直接当たると、目もりはどうなるだろう？気温を正しくはかるには、どんな場所がよいだろう？</li>
<li>ふたをしなかった入れ物の水は、どこへいったのだろう？冷たい水を入れたコップの外側についた水てきは、どこから来たのだろう？</li>
</ol>
<h2>しくみ・解説</h2>
<h3>言葉の意味（1文で）</h3>
<ul>
<li><b>気温</b>とは、地面から1.2〜1.5 mくらいの高さではかった、日かげの風通しのよい所の空気の温度のことです。</li>
<li><b>百葉箱（ひゃくようばこ）</b>とは、気温を正しくはかるために、温度計を日光や雨から守り、風通しをよくした白い箱のことです。</li>
<li><b>じょう発</b>とは、水が水面や地面などから、目に見えない水じょう気になって空気中へ出ていくことです。</li>
<li><b>水じょう気</b>とは、水がすがたを変えた気体で、目には見えず、空気の中にふくまれています。</li>
<li><b>結ろ（けつろ）</b>とは、空気中の水じょう気が冷やされて、ふたたび水（水てき）になって現れることです。</li>
</ul>
<h3>天気と気温の早見表（このシミュレーターの目安）</h3>
''' + T([["晴れ", "12℃", "15℃", "21℃", "23℃", "23℃", "19℃", "約11℃", "山の形"],
          ["くもり", "14℃", "15℃", "17℃", "18℃", "18℃", "17℃", "約4℃", "なだらか"],
          ["雨", "13℃", "14℃", "15℃", "15℃", "15℃", "14℃", "約1〜2℃", "ほぼ平ら"]],
         ["天気", NW("午前6時"), NW("午前9時"), "正午", NW("午後2時"), NW("午後3時"), NW("午後6時"), "1日の差", "グラフの形"]) + '''
<p>春〜秋のおだやかな日をもとにした目安で、季節や場所、風によって実際の数値は変わります。どの天気でも同じ時こくに気温をはかってグラフに表すと、天気によって変わり方がちがうことがわかります。</p>
<h3>気温のはかり方の早見表</h3>
''' + T([["高さ", "地面から1.2〜1.5 m", "地面の近くは、昼は地面の熱で高く、朝は低くなりやすい"],
          ["日光", "直接当てない（日かげ・百葉箱の中）", "晴れた日の昼に日光が当たると、気温より数℃高く出る"],
          ["風通し", "風通しのよい所", "熱がこもると正しい気温にならない"],
          ["場所・時こく", "同じ場所で、決めた時こくにはかる", "くらべられるように（定点で観測）"],
          ["目もりの読み方", "液の先と目の高さを同じにして真横から読む", "目もりの間のときは近い方を読む"]],
         ["気をつけること", "正しいはかり方", "理由"]) + '''
<h3>先生向けの補足：最高気温が午後2時ごろになるわけ</h3>
<p>太陽の高さがいちばん高くなるのは正午ごろですが、太陽の光はまず地面をあたため、あたためられた地面が空気をあたためます。地面から空気へ熱が伝わるのに時間がかかり、また正午を過ぎても、しばらくは地面が受け取る熱の方が出ていく熱より多いため、気温は午後1〜2時ごろに最も高くなります。最低気温は、夜の間に地面から熱がにげ続けるため、日の出前後になります。このシミュレーターでは、午前6時に最低、午後2時に最高になるなめらかな曲線（目安）で表しています。</p>
<h3>水のゆくえ（じょう発）の早見表</h3>
''' + T([["日なた（まどぎわ）", "80 mm", "68 mm", "60 mm", "40 mm", "ほとんどへらない"],
          ["日かげ（ろうか）", "80 mm", "76 mm", "73 mm", "65 mm", "ほとんどへらない"]],
         ["置く場所", "はじめ", "3日後", "5日後", "10日後", "ふたあり（ラップ）"]) + '''
<p>ふたなしの入れ物は、日なたで1日に約4 mm、日かげで約1.5 mm 水面が下がるとした目安です。じょう発する量は、気温・日光・風・空気のしめり具合・水面の広さによって変わります。ふたをした入れ物では、じょう発した水じょう気が外に出られず、ラップの内側で冷やされて水てきにもどるので、水の量はほとんど変わりません。</p>
<h3>結ろ（水てきがつく）の早見表</h3>
''' + T([["かわいている（しつ度40%）", "約10℃", "氷水（約5℃）ならつく"],
          ["ふつう（しつ度60%）", "約17℃", "冷たい水（約15℃）でもつく"],
          ["しめっている（しつ度80%）", "約21℃", "水道の水（約20℃）でもつく"]],
         ["部屋の空気（気温25℃）", "水てきがつきはじめる温度", "コップの水の例"]) + '''
<p>コップの外側の水てきは、コップの水がしみ出したものではなく、まわりの空気中の水じょう気が冷やされて水になったものです。寒い日の窓ガラスの内側のくもりや、冷ぞう庫から出したペットボトルの水てきも同じしくみです。</p>
''' + N('先生向け：水てきがつきはじめる温度は露点（中学2年「気象とその変化」で学習）です。飽和水蒸気圧を Tetens の式 e(T)＝6.1078×10<sup>7.5T/(T+237.3)</sup> hPa で求め、気温25℃・湿度60％なら露点は約16.7℃になります（関連：<a href="../shitsudo-roten/">湿度と雲のでき方シミュレーター</a>）。') + '''
<h3>このシミュレーションで単純化していること</h3>
<ul>
<li>1日の気温は、天気ごとに決めたなめらかな曲線（目安）で、実際の観測値ではありません。実際には、雲の動きや風、前線の通過などで、雨の日に気温が下がり続けたり、夜に上がったりすることもあります。</li>
<li>「日なた」「地面近く」の温度計の目もりは、日光や地面の熱の影響を大まかに足した目安です。</li>
<li>じょう発の速さは一定としています。水じょう気の粒の図は、目に見えない水じょう気をイメージとしてかいたものです。</li>
<li>結ろでは、コップの水の温度は変わらないものとしています。実際には、時間がたつとコップの水はあたたまり、水てきもつかなくなっていきます。</li>
</ul>
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「小学校学習指導要領（平成29年告示）解説 理科編」第4学年 B（4）天気の様子（''' + A(MEXT_SHO, "小学校学習指導要領解説") + '''）</li>
<li>気象庁「気象観測の手引き」（気温は地上約1.5 mの高さで、日射や雨を防ぎ風通しをよくしてはかる）</li>
<li>小学校理科の教科書（第4学年「天気と気温」「自然の中の水のすがた」の単元）</li>
</ul>
'''

sim(slug="tenki-kion", cat="rika", emoji="🌡️", score=80,
    title="天気と1日の気温のシミュレーター",
    title_tag="天気と1日の気温のシミュレーター｜晴れ・くもり・雨のグラフ、気温のはかり方、水のじょう発と結ろ（小4理科 天気の様子）",
    meta_desc="晴れ・くもり・雨を選ぶと、1日の気温の変わり方を折れ線グラフで表示。晴れの日は午後2時ごろに最高の山の形、くもり・雨は変化が小さい。百葉箱での気温のはかり方、ふたあり・なしの水のじょう発、コップの結ろも確かめられる小4理科「天気の様子」の無料シミュレーター。",
    og_title="天気と1日の気温のシミュレーター（じょう発・結ろも）",
    og_desc="晴れの日は午後2時ごろに最高の山の形、くもり・雨は変化が小さい。百葉箱のはかり方、水のじょう発、コップの結ろまで小4理科をひとつで。",
    card_desc="晴れ・くもり・雨の1日の気温グラフと百葉箱の温度計。水のじょう発とコップの結ろも。",
    lead="晴れ・くもり・雨を選ぶと、1日の気温の変わり方がグラフになります。グラフを指でなぞると時こくが変わり、右の温度計の目もりが動きます。百葉箱・日なた・地面近くで、はかった気温がどうちがうかも比べられます。「水のゆくえ」「水てきがつく」に切りかえると、水のじょう発と結ろを確かめられます。",
    model="小4 天気の様子",
    level="小学4年",
    unit="小学校 第4学年 B（4）天気の様子",
    canvas=canvas(640, 440, light=True),
    controls=select("mode", "見るもの", [("kion", "① 1日の気温（天気）"), ("evap", "② 水のゆくえ（じょう発）"), ("dew", "③ 水てきがつく（結ろ）")])
           + select("wx", "天気", [("hare", "晴れ"), ("kumori", "くもり"), ("ame", "雨")])
           + slider("tm", "時こく", 6, 18, 14, 0.5)
           + select("loc", "置く場所", [("hinata", "日なた（まどぎわ）"), ("hikage", "日かげ（ろうか）")])
           + slider("day", "置いた日数", 0, 10, 3, 1)
           + select("room", "部屋の空気", [("norm", "ふつう（しつ度60%）"), ("dry", "かわいている（しつ度40%）"), ("wet", "しめっている（しつ度80%）")])
           + slider("cup", "コップの水の温度", 0, 30, 5, 1),
    buttons=btn("play", "▶ 1日を早送り", True) + btn("cmp", "📈 3つの天気をくらべる：ON"),
    stats=stats([("sA", "天気", False), ("sB", "温度計の目もり", True), ("sC", "いちばん高い気温", False), ("sD", "1日の気温の差", False)]),
    legend="①：左＝1日の気温のグラフ（太い線が選んだ天気、うすい線はほかの天気）。上の「晴れ・くもり・雨」をタップして切りかえ、グラフを指でなぞると時こくが変わります。右＝気温のはかり方（百葉箱・日なた・地面近くをタップ）。②：ふたなし・ふたありの入れ物の水の高さ（日なたで1日約4 mmへる目安）。③：気温25℃の部屋で、コップの水の温度を変えると水てきがつくか確かめられます。数値はすべて目安です。",
    article=TENKI_ARTICLE,
    faqs=[("晴れの日の1日の気温はどう変わりますか？", "朝（日の出のころ）がいちばん低く、昼すぎの午後2時ごろにいちばん高くなり、夕方にかけて下がります。グラフにすると山の形になります。春〜秋のおだやかな晴れの日では、1日の気温の差は10℃くらいになることがあります。"),
          ("くもりや雨の日の気温はどう変わりますか？", "太陽の光が雲でさえぎられるので、昼でも気温があまり上がらず、1日の気温の変わり方が小さくなります。グラフはなだらか、雨の日はほぼ平らになります。"),
          ("気温はどこではかればよいですか？", "地面から1.2〜1.5 mくらいの高さで、日光が直接当たらない、風通しのよい所ではかります。学校では百葉箱の中の温度計を使います。日光が直接当たると、実際の気温より高い目もりになります。"),
          ("気温がいちばん高くなるのが正午ではなく午後2時ごろなのはなぜですか？", "太陽の光はまず地面をあたため、その地面が空気をあたためるので、空気があたたまるまでに時間がかかるからです。正午を過ぎても、しばらくは気温が上がり続けます。"),
          ("ふたをしない入れ物の水がへるのはなぜですか？", "水が水面からじょう発して、目に見えない水じょう気になり、空気中へ出ていくからです。ふたをすると、水じょう気が外に出られず、ふたの内側で冷やされて水てきにもどるので、水はほとんどへりません。"),
          ("冷たい水を入れたコップの外側に水てきがつくのはなぜですか？", "まわりの空気中にふくまれている水じょう気が、冷たいコップで冷やされて水にもどるからです（結ろ）。コップの中の水がしみ出したものではありません。")],
    rel=[("shitsudo-roten", "☁️", "湿度と雲のでき方シミュレーター"), ("taiyou-ugoki", "🌞", "太陽の動き"), ("sentaku-kawaku", "👕", "洗濯物 乾く時間メーター"),
         ("amagumo-now", "🌧️", "いまの雨雲マップ"), ("atatamarikata", "🔥", "物のあたたまり方シミュレーター")],
    js=JS_TENKI)


# ============================================================ 2 物のあたたまり方（金属・水・空気）
JS_ATA = HELP + r'''
  const C={bg:'#f8fafc',ink:'#0f172a',sub:'#64748b',grid:'#e2e8f0'};
  // 金ぞく：熱伝導（熱拡散率 α［m²/s］、体積あたりの熱容量 ρc［J/(m³・K)］、1マス2.5 mm）。板（厚さ1 mm）に30 W、ぼう（直径5 mm）に12 W の熱が入る。空気へにげる熱は 0.6%／秒（ぼうは0.4%）
  const MET={cu:{nm:'銅',a:1.11e-4,rc:3.45e6,col:'#c8794a'},al:{nm:'アルミニウム',a:9.7e-5,rc:2.42e6,col:'#c3ccd6'},fe:{nm:'鉄',a:2.3e-5,rc:3.54e6,col:'#8b939e'}};
  // 水・空気：層のモデル（あたためられた水・空気が上へ動いて上にたまり、層が下へおし下げられる）。Q＝熱の入る速さ［℃・層／秒］、F＝上へ動く量［層／秒］
  const MD={plate:{k:'metal',nm:'金ぞくの板',spd:1,xm:60,gd:0.5},slit:{k:'metal',nm:'切れこみのある金ぞくの板',spd:1,xm:60,gd:0.5},rod:{k:'metal',nm:'金ぞくのぼう（かたむけたもの）',spd:1,xm:60,gd:0.5},
    tube:{k:'water',nm:'試験管の水（示温インク）',spd:1,xm:120,gd:1},beaker:{k:'water',nm:'ビーカーの水（示温インク）',spd:3,xm:360,gd:3},room:{k:'air',nm:'部屋の空気（だんぼう）',spd:10,xm:1200,gd:10},vol:{k:'vol',nm:'温度と体積'}};
  const PCOL=['#dc2626','#d97706','#2563eb'], TMX=500, WAX=55, DX=2.5e-3;
  const RC=[204,226], RA=-Math.PI/6, RW=6.6, RH=22;
  let mode='plate', NX=1, NY=1, CW=7, CH=7, OX=0, OY=0, Tm=new Float32Array(1), T2=new Float32Array(1), Mk=new Uint8Array(1), NB=[], melt=new Uint8Array(1);
  let L=new Float64Array(1), FP=null, plume=null, heat=[], hp=[0,0], PR=[[0],[0],[0]], PL=['ア','イ','ウ'], t=0, acc=0, on=true, fast=1, hist=[], nextH=0, first=[null,null,null], parts=[], act=0, tNow=0, last=0, lastSt=0, vT=20, vTo=null, REG=[], bub=[];
  const id=(x,y)=>y*NX+x, r0=x=>Math.round(x);
  const isM=()=>MD[mode].k==='metal', isF=()=>MD[mode].k==='water'||MD[mode].k==='air';
  // 色
  const TC=[[0,'#2563eb'],[0.3,'#06b6d4'],[0.5,'#84cc16'],[0.7,'#facc15'],[0.85,'#f97316'],[1,'#dc2626']], LUT=[];
  for(let i=0;i<=200;i++){ const f=i/200; let c=TC[TC.length-1][1]; for(let k=1;k<TC.length;k++) if(f<=TC[k][0]){ c=mix(TC[k-1][1],TC[k][1],(f-TC[k-1][0])/(TC[k][0]-TC[k-1][0])); break; } LUT.push(c); }
  const tcol=(v,lo,hi)=>LUT[Math.round(clamp((v-lo)/(hi-lo),0,1)*200)];
  const INK=[]; for(let i=0;i<=100;i++) INK.push(mix('#4f6bd8','#ec6fa6',(i-34)/10));
  const ink=v=>INK[Math.round(clamp(v,0,100))];
  function fmt(s){ s=Math.round(s); if(s<60) return s+'秒'; const m=Math.floor(s/60), r=s%60; return m+'分'+(r?r+'秒':''); }

  // ---------- 金ぞく（熱伝導） ----------
  function grid(nx,ny,cw,ch,ox,oy,ins){ NX=nx; NY=ny; CW=cw; CH=ch; OX=ox; OY=oy; const n=nx*ny; Tm=new Float32Array(n).fill(20); T2=new Float32Array(n); Mk=new Uint8Array(n); melt=new Uint8Array(n); NB=new Array(n);
    for(let y=0;y<ny;y++) for(let x=0;x<nx;x++) Mk[id(x,y)]=ins(x,y)?1:0;
    for(let i=0;i<n;i++){ const x=i%nx, y=(i/nx)|0, a=[]; if(Mk[i]) [[1,0],[-1,0],[0,1],[0,-1]].forEach(d=>{ const X=x+d[0], Y=y+d[1]; if(X>=0&&X<nx&&Y>=0&&Y<ny&&Mk[id(X,Y)]) a.push(id(X,Y)); }); NB[i]=a; } }
  function setHeat(c){ hp=c; heat=[]; if(mode==='rod'){ for(let x=c[0]-1;x<=c[0]+1;x++) if(x>=0&&x<NX) heat.push(x); }
    else for(let y=c[1]-2;y<=c[1]+2;y++) for(let x=c[0]-2;x<=c[0]+2;x++){ if(x<0||y<0||x>=NX||y>=NY) continue; if(Math.hypot(x-c[0],y-c[1])<=1.5&&Mk[id(x,y)]) heat.push(id(x,y)); } }
  function mstep(h){ const mt=MET[$('met').value], a=mt.a, r=a*h/(DX*DX), ls=(mode==='rod'?0.004:0.006)*h, rod=mode==='rod', dq=heat.length?(rod?12:30)/(heat.length*mt.rc*(rod?4.9e-8:6.25e-9))*h:0;
    for(let i=0;i<Tm.length;i++){ if(!Mk[i]){ T2[i]=Tm[i]; continue; } const nb=NB[i]; let s=0; for(let j=0;j<nb.length;j++) s+=Tm[nb[j]]-Tm[i]; T2[i]=Tm[i]+r*s-ls*(Tm[i]-20); }
    const q=Tm; Tm=T2; T2=q; if(on) for(const i of heat) Tm[i]=Math.min(TMX,Tm[i]+dq); for(let i=0;i<Tm.length;i++) if(Tm[i]>=WAX) melt[i]=1; }
  function cellXY(i){ if(mode==='rod'){ const lx=(i+0.5-NX/2)*RW; return [RC[0]+lx*Math.cos(RA),RC[1]+lx*Math.sin(RA)]; } return [OX+(i%NX+0.5)*CW,OY+(((i/NX)|0)+0.5)*CH]; }

  // ---------- 水・空気（層のモデル） ----------
  function fstep(h){ const P=FP, n=P.ny; let Tp=null, d=P.hL;
    if(on){ Tp=Math.min(P.tmax,L[P.hL]+P.Q/P.F); d=0; while(d<P.hL&&L[d]>Tp) d++; const s=P.F*h, N=L.slice(); for(let j=d;j<=P.hL;j++){ const up=j===d?Tp:L[j-1]; N[j]=L[j]+s*(up-L[j]); } L=N; }
    plume=on?{Tp:Tp,d:d}:null;
    for(let j=0;j<n;j++){ L[j]=Math.min(P.tmax,L[j]); L[j]+=(P.tenv-L[j])*P.loss*h; if(P.win&&j>=P.win[0]&&j<=P.win[1]) L[j]+=(P.tenv-L[j])*P.win[2]*h; }
    const D=L.slice(); for(let j=0;j<n;j++){ const u=j?L[j-1]:L[j], dd=j<n-1?L[j+1]:L[j]; D[j]=L[j]+P.vd*h*(u+dd-2*L[j]); } L=D;
    if(mode==='room'&&$('fan').value==='on'){ let s=0; for(let j=0;j<n;j++) s+=L[j]; const m=s/n, k=Math.min(1,0.3*h); for(let j=0;j<n;j++) L[j]+=(m-L[j])*k; }
    for(let it=0;it<n;it++){ let ch=false; for(let j=n-1;j>0;j--) if(L[j]>L[j-1]+1e-9){ const m=(L[j]+L[j-1])/2; L[j]=L[j-1]=m; ch=true; } if(!ch) break; } }
  function rows(){ return mode==='tube'?[175,235,66,8]:(mode==='beaker'?[79,339,150,10]:[24,384,72,9]); }
  function hx(){ return mode==='tube'?($('posT').value==='bot'?[185,225]:[175,195]):(mode==='beaker'?($('posB').value==='edge'?[89,119]:[189,229]):[42,96]); }

  // ---------- 共通 ----------
  function pv(k){ if(isM()){ const a=PR[k]; let s=0; for(const i of a) s+=Tm[i]; return s/a.length; } const j=PR[k], a=Math.max(0,j-1), b=Math.min(FP.ny-1,j+1); let s=0; for(let q=a;q<=b;q++) s+=L[q]; return s/(b-a+1); }
  const thr=()=>MD[mode].k==='air'?18:40;
  function rec(f){ const v=[pv(0),pv(1),pv(2)]; for(let k=0;k<3;k++) if(first[k]===null&&v[k]>=thr()) first[k]=t; if(f||t>=nextH-1e-9){ hist.push([t,v[0],v[1],v[2]]); nextH=t+MD[mode].gd; } }
  function hstep(){ return isM()?0.2*DX*DX/MET[$('met').value].a:FP.h; }
  function adv(dt){ const h=hstep(); acc+=dt; let n=0; while(acc>=h&&n<6000){ if(isM()) mstep(h); else fstep(h); acc-=h; t+=h; n++; rec(false); } }
  function order(){ const ks=[0,1,2].filter(k=>first[k]!==null).sort((a,b)=>first[a]-first[b]); if(!ks.length) return ''; const tol=Math.max(1,MD[mode].xm*0.02); let s=PL[ks[0]];
    for(let i=1;i<ks.length;i++) s+=(first[ks[i]]-first[ks[i-1]]<=tol?'・':'→')+PL[ks[i]]; return s; }
  function resetRun(){ t=0; acc=0; hist=[]; nextH=0; first=[null,null,null]; act=0; bub=[];
    if(isM()){ Tm.fill(20); melt.fill(0); } else { L=new Float64Array(FP.ny).fill(FP.t0); } rec(true); }
  function setup(){ mode=$('mode').value; on=true; parts=[]; plume=null;
    if(mode==='vol'){ vis(); stats(); return; }
    if(mode==='plate'||mode==='slit'){ grid(40,40,7,7,64,70,(x,y)=>!(mode==='slit'&&(x===19||x===20)&&y<28));
      PR=(mode==='plate'?[[8,8],[20,20],[32,32]]:[[9,9],[20,35],[30,9]]).map(q=>[id(q[0],q[1])]); PL=['ア','イ','ウ']; setHeat(mode==='plate'?[3,3]:[4,4]); }
    else if(mode==='rod'){ grid(47,1,RW,RH,0,0,()=>true); PR=[[7],[15],[39]]; PL=['ア','イ','ウ']; setHeat([23,0]); }
    else if(mode==='tube'){ const p=$('posT').value; NX=6; FP={ny:40,h:0.05,t0:20,tmax:100,tenv:20,loss:0.002,vd:0.3,hL:p==='bot'?39:(p==='mid'?21:5),Q:24,F:4.8};
      PR=[3,20,36]; PL=['上','真ん中','下']; REG=p==='bot'?[[175,205,66,386,-1],[205,235,66,386,1]]:[[175,235,66,66+(FP.hL+1)*8,1]]; }
    else if(mode==='beaker'){ NX=26; FP={ny:24,h:0.05,t0:20,tmax:100,tenv:20,loss:0.0015,vd:0.15,hL:23,Q:3.36,F:0.3}; PR=[1,11,21]; PL=['上','真ん中','下'];
      REG=$('posB').value==='edge'?[[79,339,150,390,1]]:[[79,209,150,390,-1],[209,339,150,390,1]]; }
    else { NX=40; FP={ny:26,h:0.25,t0:10,tmax:70,tenv:5,loss:0.0008,vd:0.02,hL:25,Q:1.2,F:0.15,win:[4,19,0.004]}; PR=[1,13,24]; PL=['天井近く','真ん中','床近く']; REG=[[24,384,72,306,1]]; }
    resetRun(); makeParts(); vis(); stats(); }

  // ---------- おがくず・けむり（見やすくするためのイメージ） ----------
  function bounds(){ return mode==='tube'?[178,232,70,382]:(mode==='beaker'?[82,336,154,386]:[28,380,76,302]); }
  function makeParts(){ parts=[]; if(!isF()) return; const n=mode==='room'?90:(mode==='tube'?34:70), b=bounds(); for(let i=0;i<n;i++){ const x=rnd(b[0],b[1]), y=rnd(b[2],b[3]); parts.push({x:x,y:y,px:x,py:y}); } }
  function vel(x,y){ let u=0,v=0; for(const R of REG){ if(x<R[0]||x>R[1]||y<R[2]||y>R[3]) continue; const Lx=R[1]-R[0], Ly=R[3]-R[2], A=Math.min(Lx,Ly)/Math.PI*R[4], ax=Math.PI*(x-R[0])/Lx, ay=Math.PI*(y-R[2])/Ly;
      u+=A*Math.sin(ax)*Math.cos(ay)*Math.PI/Ly; v-=A*Math.cos(ax)*Math.sin(ay)*Math.PI/Lx; } return [u,v]; }
  function moveParts(dt){ if(!isF()) return; const fan=mode==='room'&&$('fan').value==='on', S=(mode==='room'?55:42)*act+(fan?60:0), b=bounds(), j=(mode==='room'?14:6)*Math.sqrt(dt);
    for(const p of parts){ p.px=p.x; p.py=p.y; const q=vel(p.x,p.y); p.x+=q[0]*S*dt+randn()*j; p.y+=q[1]*S*dt+randn()*j; if(p.x<b[0]||p.x>b[1]||p.y<b[2]||p.y>b[3]){ p.x=clamp(p.x,b[0],b[1]); p.y=clamp(p.y,b[2],b[3]); p.px=p.x; p.py=p.y; } } }
  function updAct(dt){ if(!isF()) return; let tg=0; if(on&&plume){ let s=0; for(let j=0;j<FP.ny;j++) s+=L[j]; tg=clamp((plume.Tp-s/FP.ny)/8,0.25,1); if(FP.hL<10) tg=0.6; } act+=(tg-act)*Math.min(1,dt*1.5); }

  // ---------- 描画：金ぞく ----------
  function head(){ panel(8,8,392,424); tx(MD[mode].nm+(isM()?'（'+MET[$('met').value].nm+'）':''),18,28,13.5,C.ink,'left',true); tx((on?'熱しはじめて ':'止めた・')+fmt(t),390,28,12,on?'#b91c1c':C.sub,'right',true); }
  function drawMetal(){ const mt=MET[$('met').value], wax=$('look').value==='wax'; head();
    tx('指でタップした所を熱する',18,48,11.5,'#0e7490','left',true);
    const col=i=>wax?(melt[i]?mt.col:'#f8fafc'):tcol(Tm[i],20,100);
    if(mode==='rod'){ ctx.save(); ctx.translate(RC[0],RC[1]); ctx.rotate(RA); const x0=-NX*RW/2; for(let i=0;i<NX;i++){ ctx.fillStyle=col(i); ctx.fillRect(x0+i*RW,-RH/2,RW+0.6,RH); }
        ctx.strokeStyle='#334155'; ctx.lineWidth=1.6; ctx.strokeRect(x0,-RH/2,NX*RW,RH); ctx.restore();
        const e0=cellXY(0), e1=cellXY(NX-1); tx('下のはし',e0[0]-6,e0[1]+30,11,C.sub,'left',true); tx('上のはし',e1[0]+8,e1[1]-18,11,C.sub,'right',true); }
    else { for(let y=0;y<NY;y++) for(let x=0;x<NX;x++){ const i=id(x,y); if(!Mk[i]) continue; ctx.fillStyle=col(i); ctx.fillRect(OX+x*CW,OY+y*CH,CW+0.5,CH+0.5); }
      ctx.strokeStyle='#334155'; ctx.lineWidth=1.6; ctx.beginPath(); for(let y=0;y<NY;y++) for(let x=0;x<NX;x++){ if(!Mk[id(x,y)]) continue; const X=OX+x*CW, Y=OY+y*CH;
        if(x===0||!Mk[id(x-1,y)]){ ctx.moveTo(X,Y); ctx.lineTo(X,Y+CH); } if(x===NX-1||!Mk[id(x+1,y)]){ ctx.moveTo(X+CW,Y); ctx.lineTo(X+CW,Y+CH); }
        if(y===0||!Mk[id(x,y-1)]){ ctx.moveTo(X,Y); ctx.lineTo(X+CW,Y); } if(y===NY-1||!Mk[id(x,y+1)]){ ctx.moveTo(X,Y+CH); ctx.lineTo(X+CW,Y+CH); } } ctx.stroke(); }
    for(let k=0;k<3;k++){ const p=cellXY(PR[k][0]); dot(p[0],p[1],9,'rgba(255,255,255,.93)','#334155'); tx(PL[k],p[0],p[1]+4.5,11.5,PCOL[k],'center',true); }
    const hc=cellXY(mode==='rod'?hp[0]:id(hp[0],hp[1]));
    if(on){ const g=ctx.createRadialGradient(hc[0],hc[1],2,hc[0],hc[1],20); g.addColorStop(0,'rgba(249,115,22,.55)'); g.addColorStop(1,'rgba(249,115,22,0)'); ctx.fillStyle=g; ctx.beginPath(); ctx.arc(hc[0],hc[1],20,0,6.2832); ctx.fill(); flame(hc[0],hc[1]+4,8); }
    else dot(hc[0],hc[1],6,'#94a3b8');
    const ly=372;
    if(wax){ ctx.fillStyle='#f8fafc'; ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1; ctx.fillRect(18,ly,22,14); ctx.strokeRect(18,ly,22,14); tx('ろう（まだとけていない）',46,ly+12,11.5,C.ink,'left',true);
      ctx.fillStyle=mt.col; ctx.fillRect(18,ly+22,22,14); tx('ろうがとけた所（約55℃より高い）',46,ly+34,11.5,C.ink,'left',true); }
    else { const g=ctx.createLinearGradient(40,0,360,0); TC.forEach(s=>g.addColorStop(s[0],s[1])); ctx.fillStyle=g; rr(40,ly,320,14,7); ctx.fill();
      [[20,'20℃'],[60,'60℃'],[100,'100℃以上']].forEach(q=>tx(q[1],40+320*(q[0]-20)/80,ly+30,11,C.sub,q[0]===20?'left':(q[0]===100?'right':'center'),true));
      tx('温度の色（示温シールのイメージ）',200,ly+48,11,C.sub,'center',true); } }

  // ---------- 描画：水・空気 ----------
  function lampAt(x,yTip,s){ flame(x,yTip+1.9*s,s); ctx.fillStyle='#cbd5e1'; ctx.fillRect(x-1.5,yTip+2.6*s,3,5); ctx.fillStyle='rgba(219,234,254,.9)'; ctx.strokeStyle='#64748b'; ctx.lineWidth=1.2; rr(x-17,yTip+2.6*s+5,34,15,6); ctx.fill(); ctx.stroke(); }
  function sideFlame(x,y){ ctx.save(); ctx.translate(x,y); ctx.rotate(Math.PI/2); flame(0,0,8); ctx.restore(); }
  function cellsFluid(colf){ const R=rows(), P=plume, X=hx();
    for(let j=0;j<FP.ny;j++){ ctx.fillStyle=colf(L[j]); ctx.fillRect(R[0],R[2]+j*R[3],R[1]-R[0],R[3]+0.6); }
    if(P&&P.Tp!==null){ ctx.fillStyle=colf(P.Tp); ctx.globalAlpha=0.8; const y0=R[2]+P.d*R[3], y1=R[2]+(FP.hL+1)*R[3]; ctx.fillRect(X[0]+3,y0,X[1]-X[0]-6,y1-y0); ctx.globalAlpha=1; } }
  function drawParts(col,r,trail){ parts.forEach(p=>{ if(trail){ ctx.strokeStyle=col; ctx.lineWidth=r*1.4; ctx.lineCap='round'; ctx.beginPath(); ctx.moveTo(p.px,p.py); ctx.lineTo(p.x,p.y); ctx.stroke(); ctx.lineCap='butt'; } dot(p.x,p.y,r,col); }); }
  function probeTags(xs){ const R=rows(); for(let k=0;k<3;k++){ const y=R[2]+(PR[k]+0.5)*R[3]; ctx.strokeStyle=PCOL[k]; ctx.lineWidth=1.5; ctx.beginPath(); ctx.moveTo(xs[0],y); ctx.lineTo(xs[1],y); ctx.stroke(); dot(xs[0],y,3,PCOL[k]); tag(PL[k]+' '+r0(pv(k))+'℃',xs[1]+4,y+5,11.5,PCOL[k],'left'); } }
  function inkLegend(){ tx('示温インク：',18,48,11,C.sub,'left',true); [['約40℃より低い','#4f6bd8'],['約40℃より高い','#ec6fa6']].forEach((q,i)=>{ ctx.fillStyle=q[1]; rr(86+i*112,38,14,14,3); ctx.fill(); tx(q[0],104+i*112,50,11,C.ink,'left',true); }); }
  function drawTube(){ head(); const p=$('posT').value;
    ctx.save(); ctx.beginPath(); ctx.moveTo(175,66); ctx.lineTo(175,356); ctx.arc(205,356,30,Math.PI,0,true); ctx.lineTo(235,66); ctx.closePath(); ctx.clip(); cellsFluid(ink); drawParts('rgba(120,53,15,.85)',2.2,false);
    bub.forEach(b=>dot(b.x,b.y,b.r,'rgba(255,255,255,.9)','rgba(100,116,139,.6)')); ctx.restore();
    ctx.strokeStyle='#64748b'; ctx.lineWidth=2.5; ctx.beginPath(); ctx.moveTo(173,58); ctx.lineTo(173,356); ctx.arc(205,356,32,Math.PI,0,true); ctx.lineTo(237,58); ctx.stroke();
    ctx.strokeStyle='rgba(2,132,199,.6)'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.moveTo(175,66); ctx.lineTo(235,66); ctx.stroke();
    if(on){ if(p==='bot') lampAt(205,392,6.5); else { const y=66+(FP.hL-1)*8; sideFlame(156,y); tx('熱する',140,y+4,11,'#c2410c','right',true); } }
    probeTags([240,262]); inkLegend();
    tx('茶色のつぶ＝おがくず（水の動き）',18,402,10.5,C.sub,'left',true); tx('指でタップした高さを熱する',18,420,10.5,'#0e7490','left',true); }
  function drawBeaker(){ head(); const p=$('posB').value;
    ctx.save(); ctx.beginPath(); ctx.rect(79,150,260,240); ctx.clip(); cellsFluid(ink); drawParts('rgba(120,53,15,.85)',2.2,false); bub.forEach(b=>dot(b.x,b.y,b.r,'rgba(255,255,255,.9)','rgba(100,116,139,.6)')); ctx.restore();
    ctx.strokeStyle='#64748b'; ctx.lineWidth=2.5; ctx.beginPath(); ctx.moveTo(70,112); ctx.lineTo(77,118); ctx.lineTo(77,390); ctx.quadraticCurveTo(77,392,81,392); ctx.lineTo(337,392); ctx.quadraticCurveTo(341,392,341,388); ctx.lineTo(341,112); ctx.stroke();
    ctx.strokeStyle='rgba(2,132,199,.6)'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.moveTo(79,150); ctx.lineTo(339,150); ctx.stroke();
    ctx.strokeStyle='#9ca3af'; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(60,395); ctx.lineTo(358,395); ctx.stroke();
    if(on) lampAt(p==='edge'?104:209,396,6); probeTags(p==='edge'?[262,278]:[96,112]); inkLegend();
    tx('茶色のつぶ＝おがくず　金あみの下から熱する',18,72,10.5,C.sub,'left',true); }
  function drawRoom(){ head(); const fan=$('fan').value==='on';
    ctx.save(); ctx.beginPath(); ctx.rect(24,72,360,234); ctx.clip(); ctx.globalAlpha=0.62; cellsFluid(v=>tcol(v,5,35)); ctx.globalAlpha=1; ctx.restore();
    ctx.strokeStyle='#475569'; ctx.lineWidth=3; ctx.strokeRect(24,72,360,234); ctx.fillStyle='#a8763e'; ctx.fillRect(20,306,368,8);
    ctx.fillStyle='rgba(224,242,254,.95)'; ctx.fillRect(379,108,8,136); ctx.strokeStyle='#0369a1'; ctx.lineWidth=1.5; ctx.strokeRect(379,108,8,136); tag('まど（外は5℃）',372,262,10.5,'#0369a1','right');
    ctx.fillStyle='#374151'; rr(40,262,58,44,6); ctx.fill(); ctx.fillStyle=on?'#ef4444':'#6b7280'; for(let i=0;i<3;i++) ctx.fillRect(48,270+i*10,42,4); tag('ストーブ',69,256,11,'#b91c1c','center');
    if(fan){ const fx=232, fy=284, a=tNow*12; ctx.strokeStyle='#334155'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(fx,fy+10); ctx.lineTo(fx,306); ctx.stroke(); ctx.fillStyle='#94a3b8'; for(let k=0;k<3;k++){ ctx.beginPath(); ctx.ellipse(fx+Math.cos(a+k*2.09)*7,fy+Math.sin(a+k*2.09)*7,7,3.5,a+k*2.09,0,6.2832); ctx.fill(); } dot(fx,fy,3,'#334155'); tag('せんぷうき',fx,fy-16,10.5,'#334155','center'); }
    ctx.save(); ctx.beginPath(); ctx.rect(24,72,360,234); ctx.clip(); drawParts('rgba(71,85,105,.45)',2.6,true); ctx.restore();
    probeTags([300,306]);
    tx('灰色のすじ＝線香のけむり（空気の動き）　色＝温度',18,328,10.5,C.sub,'left',true);
    const g=ctx.createLinearGradient(40,0,360,0); TC.forEach(s=>g.addColorStop(s[0],s[1])); ctx.globalAlpha=0.62; ctx.fillStyle=g; rr(40,340,320,12,6); ctx.fill(); ctx.globalAlpha=1;
    [[5,'5℃'],[20,'20℃'],[35,'35℃']].forEach(q=>tx(q[1],40+320*(q[0]-5)/30,366,11,C.sub,q[0]===5?'left':(q[0]===35?'right':'center'),true));
    tx(fan?'せんぷうきで空気を回している':'あたためられた空気は上へ',200,392,12,fan?'#0e7490':'#b91c1c','center',true); tx('（部屋のたての断面図）',200,410,10.5,C.sub,'center',true); }

  // ---------- 描画：右のグラフ ----------
  function msgs(){ const fe=$('met').value==='fe';
    if(!on) return ['熱するのを止めた。','少しずつ温度が下がっていく。',''];
    if(mode==='plate') return ['熱した所から近いじゅんに','まわりへ広がるように','あたたまる。'+(fe?'（鉄はゆっくり）':'')];
    if(mode==='slit') return ['切れこみがあると、','金ぞくのある所を回って','じゅんに伝わる。'+(fe?'（鉄はゆっくり）':'')];
    if(mode==='rod') return ['かたむけても、熱した所から','上にも下にも同じように','じゅんにあたたまる。'];
    if(mode==='tube'){ const p=$('posT').value; return p==='bot'?['あたためられた水は上へ動き、','上の方からじゅんに','全体があたたまる。']:(p==='mid'?['熱した所より上はあたたまる','が、下の方の水は','なかなかあたたまらない。']:['上の方の水だけがあたたまる。','あたたかい水は上にたまり、','下の水はつめたいまま。']); }
    if(mode==='beaker') return ['あたためられた水は上へ動き、','上の方にたまって、上から','じゅんに下へあたたまる。'];
    return $('fan').value==='on'?['せんぷうきで空気を回すと、','上と下の温度のちがいが','小さくなる。']:['あたためられた空気は上へ動く。','天井近くはあたたかく、','足もとはつめたいまま。']; }
  function drawRight(){ const x=408, md=MD[mode], k=md.k; panel(x,8,224,424); tx('温度の変わり方（目安）',x+10,28,13,C.ink,'left',true);
    let xm=md.xm; while(t>xm*1.0001) xm*=2; const lo=k==='air'?0:20, hi=k==='air'?35:100, X0=x+34, X1=x+214, Y0=196, Y1=48, gx=s=>X0+(X1-X0)*s/xm, gy=v=>Y0-(Y0-Y1)*(clamp(v,lo,hi)-lo)/(hi-lo);
    const ys=k==='air'?5:20, xs=xm<=120?xm/4:(xm<=480?60:(xm<=1200?300:600));
    ctx.strokeStyle=C.grid; ctx.lineWidth=1; for(let v=lo+ys;v<=hi;v+=ys){ ctx.beginPath(); ctx.moveTo(X0,gy(v)); ctx.lineTo(X1,gy(v)); ctx.stroke(); } for(let s=xs;s<=xm+1e-6;s+=xs){ ctx.beginPath(); ctx.moveTo(gx(s),Y0); ctx.lineTo(gx(s),Y1); ctx.stroke(); }
    for(let v=lo;v<=hi;v+=(k==='air'?10:20)) tx(String(v),X0-5,gy(v)+4,10,C.sub,'right');
    for(let s=0;s<=xm+1e-6;s+=xs) tx(xm<=120?String(Math.round(s)):String(Math.round(s/60*10)/10),gx(s),Y0+14,10,C.sub,'center');
    ctx.strokeStyle=C.ink; ctx.lineWidth=1.2; ctx.beginPath(); ctx.moveTo(X0,Y1-4); ctx.lineTo(X0,Y0); ctx.lineTo(X1,Y0); ctx.stroke();
    tx('［℃］',x+6,Y1-8,10,C.sub,'left',true); tx('時間［'+(xm<=120?'秒':'分')+'］',X1,Y0+27,10,C.sub,'right',true);
    if(k!=='air'){ ctx.setLineDash([4,4]); ctx.strokeStyle='#94a3b8'; ctx.beginPath(); ctx.moveTo(X0,gy(40)); ctx.lineTo(X1,gy(40)); ctx.stroke(); ctx.setLineDash([]); }
    for(let q=2;q>=0;q--){ ctx.strokeStyle=PCOL[q]; ctx.lineWidth=2.4; ctx.beginPath(); hist.forEach((h,i)=>{ const X=gx(h[0]), Y=gy(h[q+1]); if(i) ctx.lineTo(X,Y); else ctx.moveTo(X,Y); }); ctx.stroke(); }
    const by=250; for(let q=0;q<3;q++){ const y=by+q*23; dot(x+16,y-5,5,PCOL[q]); tx(PL[q],x+26,y,12,C.ink,'left',true); tx(r0(pv(q))+'℃',x+212,y+1,17,PCOL[q],'right',true); }
    const o=order(); tx('あたたまった順（'+thr()+'℃）',x+10,320,11,C.sub,'left',true); tx(o||'まだ',x+10,338,o.length>9?12:14,C.ink,'left',true);
    msgs().forEach((s,i)=>tx(s,x+10,360+i*18,11.5,'#0f766e','left',true));
    tx(mode==='room'?'⚠ ストーブの近くに物を置かない':'⚠ 熱した物・湯にさわらない',x+10,424,10.5,'#b45309','left',true); }

  // ---------- 描画：温度と体積 ----------
  function rho(T_){ return 999.97495*(1-(T_-3.983035)*(T_-3.983035)*(T_+301.797)/(522528.9*(T_+69.34881))); }
  const vr=()=>({a:(273.15+vT)/293.15,w:rho(20)/rho(vT),m:1+36e-6*(vT-20)});
  const pct=(r,dg)=>((r-1)*100>=0?'+':'−')+Math.abs((r-1)*100).toFixed(dg)+'%';
  function drawVol(){ panel(8,8,624,424); tx('温度と体積：20℃のときとくらべる',18,28,13.5,C.ink,'left',true); tx('水そうの温度 '+Math.round(vT)+'℃',622,28,14,vT>=40?'#b91c1c':(vT<=10?'#1d4ed8':C.ink),'right',true);
    const R=vr(), bath=vT<20?mix('#93c5fd','#e0f2fe',vT/20):mix('#e0f2fe','#fca5a5',(vT-20)/80), bn=vT<=5?'氷水':(vT>=40?'湯':'水'), S=320, B=128;
    [[112,'空気',R.a],[322,'水',R.w]].forEach(c=>{ const cx=c[0], air=c[1]==='空気';
      ctx.fillStyle=bath; ctx.fillRect(cx-72,218,144,112); ctx.strokeStyle='#64748b'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(cx-72,206); ctx.lineTo(cx-72,330); ctx.lineTo(cx+72,330); ctx.lineTo(cx+72,206); ctx.stroke(); tx(bn,cx+64,322,11,C.sub,'right',true);
      if(vT>=60) for(let i=0;i<3;i++){ ctx.strokeStyle='rgba(148,163,184,.6)'; ctx.lineWidth=1.5; ctx.beginPath(); const sx=cx-50+i*22; ctx.moveTo(sx,212); ctx.quadraticCurveTo(sx+8,200,sx,190); ctx.stroke(); }
      ctx.fillStyle=air?'rgba(241,245,249,.9)':'rgba(125,211,252,.75)'; ctx.beginPath(); ctx.moveTo(cx-16,164); ctx.lineTo(cx-16,300); ctx.arc(cx,300,16,Math.PI,0,true); ctx.lineTo(cx+16,164); ctx.closePath(); ctx.fill();
      ctx.strokeStyle='#64748b'; ctx.lineWidth=2; ctx.stroke(); ctx.fillStyle='#57534e'; rr(cx-20,150,40,16,4); ctx.fill();
      ctx.fillStyle='rgba(255,255,255,.9)'; ctx.fillRect(cx-4,34,8,118); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1.2; ctx.strokeRect(cx-4,34,8,118);
      const y=B-(c[2]-1)*S;
      if(air){ ctx.fillStyle='#0ea5e9'; ctx.fillRect(cx-3,y-4,6,8); } else { ctx.fillStyle='rgba(56,189,248,.85)'; ctx.fillRect(cx-3,y,6,152-y); }
      ctx.strokeStyle='#dc2626'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.moveTo(cx-12,B); ctx.lineTo(cx-5,B); ctx.stroke(); tx('20℃の位置',cx-14,B+4,10,'#dc2626','right',true);
      if(Math.abs(y-B)>3){ ctx.strokeStyle='#0f172a'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.moveTo(cx+12,B); ctx.lineTo(cx+12,y); ctx.stroke(); ctx.beginPath(); ctx.moveTo(cx+8,y+(y<B?5:-5)); ctx.lineTo(cx+12,y); ctx.lineTo(cx+16,y+(y<B?5:-5)); ctx.stroke(); }
      tx(air?'ゼリー（水）のしるし':'水の先',cx+20,y+4,10.5,'#0369a1','left',true);
      tx(c[1],cx,354,15,C.ink,'center',true); tx(pct(c[2],1),cx,382,22,c[2]>=1?'#b91c1c':'#1d4ed8','center',true); tx('20℃の体積を100とすると '+(c[2]*100).toFixed(1),cx,402,10.5,C.sub,'center',true); });
    const cx=532; ctx.strokeStyle='#64748b'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(cx,40); ctx.lineTo(cx,108); ctx.stroke(); dot(cx,134,26,mix('#9ca3af','#f87171',(vT-20)/80),'#475569'); dot(cx-8,126,6,'rgba(255,255,255,.5)');
    ctx.strokeStyle='#475569'; ctx.lineWidth=5; ctx.beginPath(); ctx.ellipse(cx,200,30,8,0,0,6.2832); ctx.stroke(); ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(cx+30,200); ctx.lineTo(cx+58,200); ctx.lineTo(cx+58,240); ctx.stroke(); ctx.fillStyle='#475569'; ctx.fillRect(cx+34,238,48,5); tx('輪',cx-40,204,11,C.sub,'right',true);
    const dd=25*(1+12e-6*(vT-20)); tx('鉄の玉（20℃で直径25.00 mm）',cx,262,10.5,C.sub,'center',true); tx('いま '+dd.toFixed(2)+' mm',cx,280,12,C.ink,'center',true); tx('輪の内側 25.05 mm → 通る',cx,297,11,'#15803d','center',true);
    tx('湯くらいでは ほとんど変わらない。',cx,314,10,C.sub,'center',true); tx('ガスバーナーで強く熱すると通らなくなる',cx,328,10,C.sub,'center',true);
    tx('金ぞく（鉄）',cx,354,15,C.ink,'center',true); tx(pct(R.m,2),cx,382,22,R.m>=1?'#b91c1c':'#1d4ed8','center',true); tx('20℃の体積を100とすると '+(R.m*100).toFixed(2),cx,402,10.5,C.sub,'center',true);
    tx('空気と水の図は同じ倍率（試験管 20 mL・同じ太さのガラス管）。体積の変わり方は 空気 ＞ 水 ＞ 金ぞく。',320,424,10.5,C.sub,'center',true); }

  // ---------- 統計欄 ----------
  function stats(){ const md=MD[mode], k=md.k;
    if(k==='vol'){ const R=vr(); K('sA').innerHTML='水そうの温度'; sh('sA',Math.round(vT)+'℃','20℃のときとくらべる');
      K('sB').innerHTML='空気の体積'; sh('sB',pct(R.a,1),'いちばん大きく変わる'); K('sC').innerHTML='水の体積'; sh('sC',pct(R.w,1),'少し変わる'); K('sD').innerHTML='金ぞく（鉄）の体積'; sh('sD',pct(R.m,2),'ほんの少し変わる');
      setShare('【温度と体積】20℃→'+Math.round(vT)+'℃で、空気の体積は'+pct(R.a,1)+'、水は'+pct(R.w,1)+'、金ぞく（鉄）は'+pct(R.m,2)+'。温度による体積の変わり方は空気がいちばん大きい｜シミュラボ'); return; }
    const v=[pv(0),pv(1),pv(2)], o=order(), sp=md.spd*fast;
    K('sA').innerHTML=on?'熱しはじめて':'熱するのを止めた'; sh('sA',fmt(t),sp>1?'時間は'+sp+'倍の速さ':'実際の時間の目安');
    if(k==='metal'){ K('sB').innerHTML='ア・イ・ウの温度'; sh('sB',v.map(r0).join('/')+'℃'); }
    else { K('sB').innerHTML=PL[0]+'／'+PL[2]+'の温度'; sh('sB',r0(v[0])+'℃／'+r0(v[2])+'℃'); }
    K('sC').innerHTML='あたたまった順'; sh('sC',o||'まだ',thr()+'℃をこえた順');
    if(k==='metal'){ let a=0,n=0; for(let i=0;i<Tm.length;i++) if(Mk[i]){ n++; if(melt[i]) a++; } K('sD').innerHTML='ろうがとけた所'; sh('sD',Math.round(a/n*100)+'%','約55℃をこえた広さ'); }
    else if(k==='air'){ K('sD').innerHTML='天井近くと床近くの差'; sh('sD',r0(v[0]-v[2])+'℃',$('fan').value==='on'?'せんぷうきあり':'せんぷうきなし'); }
    else { let s=0; for(let j=0;j<FP.ny;j++) s+=L[j]; K('sD').innerHTML='水全体の平均'; sh('sD',r0(s/FP.ny)+'℃','約40℃でピンク'); }
    const mt=MET[$('met').value].nm;
    if(k==='metal') setShare('【物のあたたまり方】'+mt+'の'+(mode==='rod'?'ぼう':'板')+'を熱すると、熱した所から順にあたたまる（'+fmt(t)+'で ア'+r0(v[0])+'℃・イ'+r0(v[1])+'℃・ウ'+r0(v[2])+'℃'+(o?'、あたたまった順 '+o:'')+'）｜シミュラボ');
    else if(k==='water') setShare('【物のあたたまり方】'+(mode==='tube'?'試験管の水の'+{bot:'下',mid:'真ん中',top:'上'}[$('posT').value]:'ビーカーの水の底')+'を熱すると、'+fmt(t)+'で上'+r0(v[0])+'℃・下'+r0(v[2])+'℃。あたためられた水は上へ動く｜シミュラボ');
    else setShare('【空気のあたたまり方】ストーブで部屋をあたためると、'+fmt(t)+'で天井近く'+r0(v[0])+'℃・床近く'+r0(v[2])+'℃（差'+r0(v[0]-v[2])+'℃）。あたためられた空気は上へ動く｜シミュラボ'); }
  function vis(){ const k=MD[mode].k, m=k==='metal'; showF('met',m); showF('look',m); showF('posT',mode==='tube'); showF('posB',mode==='beaker'); showF('fan',mode==='room'); showF('vt',k==='vol');
    ['heat','reset','fast'].forEach(i=>show(i,k!=='vol')); ['hot','cold'].forEach(i=>show(i,k==='vol'));
    $('heat').textContent=on?'⏸ 熱するのを止める':'🔥 熱する'; $('fast').textContent=fast>1?'⏩ はやおくり：ON':'⏩ はやおくり'; }
  function draw(){ ctx.fillStyle=C.bg; ctx.fillRect(0,0,W,H); if(mode==='vol'){ drawVol(); return; } if(isM()) drawMetal(); else if(mode==='tube') drawTube(); else if(mode==='beaker') drawBeaker(); else drawRoom(); drawRight(); }
  function bubbles(dt){ if(!isF()||mode==='room') return; const R=rows(); for(let j=0;j<FP.ny;j++){ if(L[j]>=99.5&&Math.random()<dt*3){ bub.push({x:rnd(R[0]+6,R[1]-6),y:R[2]+(j+0.5)*R[3],r:rnd(1.5,3.2)}); } }
    bub.forEach(b=>{ b.y-=dt*60; }); bub=bub.filter(b=>b.y>R[2]+2).slice(-60); }

  // ---------- 操作 ----------
  [['mode','mode'],['met','met'],['look','look'],['posT','pos'],['posB','pos'],['fan','fan']].forEach(a=>{ if(!Q.has(a[1])) return; const el=$(a[0]), q=Q.get(a[1]); if([].some.call(el.options,o=>o.value===q)) el.value=q; });
  if(Q.has('vt')){ vT=clamp(Math.round(+Q.get('vt')),0,100); $('vt').value=vT; $('vtL').textContent=vT+'℃'; }
  setup();
  if(Q.has('hx')&&isM()){ const a=Q.get('hx').split(',').map(Number); setHeat(mode==='rod'?[clamp(a[0]|0,0,NX-1),0]:[clamp(a[0]|0,0,NX-1),clamp(a[1]|0,0,NY-1)]); resetRun(); }
  if(Q.get('heat')==='off'){ on=false; }
  if(Q.has('t')){ adv(clamp(+Q.get('t')||0,0,3600)); } else if(mode==='plate') adv(15);
  if(isF()){ updAct(1); updAct(1); }
  ['mode','met','posT','posB'].forEach(i=>$(i).addEventListener('change',()=>{ fast=1; setup(); }));
  $('look').addEventListener('change',()=>{ stats(); });
  $('fan').addEventListener('change',()=>{ stats(); });
  $('heat').addEventListener('click',()=>{ on=!on; vis(); stats(); });
  $('reset').addEventListener('click',()=>{ on=true; resetRun(); makeParts(); vis(); stats(); });
  $('fast').addEventListener('click',()=>{ fast=fast>1?1:4; vis(); stats(); });
  $('vt').addEventListener('input',()=>{ vT=+$('vt').value; vTo=null; $('vtL').textContent=vT+'℃'; stats(); });
  $('hot').addEventListener('click',()=>{ vTo=80; });
  $('cold').addEventListener('click',()=>{ vTo=0; });
  cv.addEventListener('pointerdown',e=>{ const p=cpos(cv,e), x=p[0]/dpr, y=p[1]/dpr; if(x>400||mode==='vol') return;
    if(mode==='rod'){ const dx=x-RC[0], dy=y-RC[1], lx=dx*Math.cos(RA)+dy*Math.sin(RA), ly=-dx*Math.sin(RA)+dy*Math.cos(RA); if(Math.abs(ly)<RH*1.6&&Math.abs(lx)<NX*RW/2+10){ on=true; setHeat([clamp(Math.floor(lx/RW+NX/2),0,NX-1),0]); resetRun(); vis(); stats(); } }
    else if(isM()){ let cx=Math.floor((x-OX)/CW), cy=Math.floor((y-OY)/CH); if(cx<-3||cy<-3||cx>NX+2||cy>NY+2) return; cx=clamp(cx,0,NX-1); cy=clamp(cy,0,NY-1);
      if(!Mk[id(cx,cy)]){ let b=null, bd=1e9; for(let yy=0;yy<NY;yy++) for(let xx=0;xx<NX;xx++) if(Mk[id(xx,yy)]){ const d=Math.hypot(xx-cx,yy-cy); if(d<bd){ bd=d; b=[xx,yy]; } } if(!b||bd>4) return; cx=b[0]; cy=b[1]; }
      on=true; setHeat([cx,cy]); resetRun(); vis(); stats(); }
    else if(mode==='tube'&&x>120&&x<300&&y>40){ $('posT').value=y<140?'top':(y<300?'mid':'bot'); setup(); }
    else if(mode==='beaker'&&x>60&&x<360&&y>110){ $('posB').value=Math.abs(x-209)<50?'center':'edge'; setup(); } });
  function frame(ts){ const dt=last?Math.min(0.05,(ts-last)/1000):0; last=ts; tNow+=dt;
    if(mode==='vol'){ if(vTo!==null){ const d=vTo-vT, s=Math.sign(d)*Math.min(Math.abs(d),dt*40); vT+=s; if(Math.abs(vTo-vT)<0.01){ vT=vTo; vTo=null; } $('vt').value=Math.round(vT); $('vtL').textContent=Math.round(vT)+'℃'; if(ts-lastSt>120){ lastSt=ts; stats(); } } }
    else { adv(dt*MD[mode].spd*fast); updAct(dt); moveParts(dt); bubbles(dt); if(ts-lastSt>200){ lastSt=ts; stats(); } }
    draw(); requestAnimationFrame(frame); }
  for(let i=0;i<20;i++) moveParts(1/30);
  vis(); stats(); draw(); requestAnimationFrame(frame);
'''

ATA_ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
<p><b>金ぞく</b>は、熱した所から近いじゅんに、まわりへ広がるようにあたたまります。ぼうをかたむけても、上にも下にも同じようにあたたまります。<b>水と空気</b>は、あたためられた部分が<b>上へ動き</b>、上の方からじゅんに全体があたたまります。そのため、試験管の水の上の方だけを熱すると、下の方の水はなかなかあたたまりません。部屋をストーブであたためると、天井近くはあたたかく、足もとはつめたいままになりやすいのも同じしくみです。切りかえで、温度による体積の変わり方（空気 ＞ 水 ＞ 金ぞく）も確かめられます。</p>
''' + N('<b>対応する単元</b>：小学4年 A（2）金属，水，空気と温度「（イ）金属は熱せられた部分から順に温まるが，水や空気は熱せられた部分が移動して全体が温まること」（主にこの内容）、「（ア）金属，水及び空気は，温めたり冷やしたりすると，それらの体積が変わるが，その程度には違いがあること」。学習指導要領解説では、水や空気は熱を加えられた部分が上方に移動して全体が温まること、物によって温まり方に違いがあること、空気の温度による体積の変化が最も大きいことを捉えるようにし、日常生活との関連として冷暖房時の空気循環の効果などを取り上げることが示されています。水が水蒸気や氷に変わる（ウ）は<a href="../joutai-henka/">状態変化と粒子のシミュレーター</a>で扱えます。') + '''
<h2>授業での使い方</h2>
<h3>導入：金ぞくはどのようにあたたまる？</h3>
<p>「金ぞくの板のかどを熱すると、どのようにあたたまっていくだろう」と問いかけ、あたたまっていく様子を予想して図にかかせます。「金ぞくの板」で熱する場所を指でタップし、ア・イ・ウのどこから先にあたたまるかを確かめます。「見え方」を「ろうをぬった板・ぼう」にすると、ろうがとけていく様子（教科書の実験と同じ見え方）になります。「切れこみあり」の板では、熱が金ぞくのある所を回って伝わることがわかります。</p>
<h3>展開：水と空気のあたたまり方</h3>
<p>「試験管の水」で、熱する場所を「下」「真ん中」「上」と変えて比べます（試験管の図をタップしても変えられます）。示温インクの色が、下を熱すると上の方から順にピンクに変わり、上を熱すると上の方だけが変わる（下は青のまま）ことから、あたためられた水は上へ動くことに気づかせます。「ビーカーの水」ではおがくずの動きで水の動きを見ます。「部屋の空気」では、線香のけむりの動きと、天井近く・床近くの温度のちがいを確かめ、せんぷうきで空気を回すとどうなるかを考えさせます。</p>
<h3>まとめ・発展：温度と体積</h3>
<p>「温度と体積」に切りかえ、湯（80℃）や氷水（0℃）につけたときの空気・水・金ぞくの体積の変わり方を比べます。体積の変わり方は空気がいちばん大きく、金ぞくはとても小さいことを、数値と図でまとめます。</p>
<h3>児童への問いの例</h3>
<ol>
<li>金ぞくのぼうをかたむけて真ん中を熱すると、上のはしと下のはしでは、どちらが先にあたたまるだろう？</li>
<li>試験管の水を早く全体あたためるには、試験管のどこを熱するとよいだろう？それはなぜだろう？</li>
<li>だんぼうをつけた部屋で、天井の近くと足もとでは、どちらがあたたかいだろう？せんぷうきやサーキュレーターを使うのはなぜだろう？</li>
</ol>
<h2>しくみ・解説</h2>
<h3>言葉の意味（1文で）</h3>
<ul>
<li><b>金ぞくのあたたまり方</b>とは、熱した所から近いじゅんに、金ぞくの中を熱が伝わってあたたまっていくことです。</li>
<li><b>水や空気のあたたまり方</b>とは、あたためられた水や空気が上へ動き、上の方からじゅんに全体があたたまっていくことです。</li>
<li><b>示温インク（しおんインク）</b>とは、温度によって色が変わるインクで、このシミュレーターでは約40℃で青色からピンク色に変わるものとしています。</li>
<li><b>示温テープ（示温シール）</b>とは、温度によって色が変わるテープで、金ぞくなどにはって、あたたまった所を色で見るために使います。</li>
<li><b>体積</b>とは、物がしめている場所の大きさのことで、空気・水・金ぞくは、あたためると体積が大きくなり、冷やすと小さくなります。</li>
</ul>
<h3>あたたまり方の早見表</h3>
''' + T([["金ぞく（板・ぼう）", "熱した所から近いじゅんに", "上・下・ななめに関係なく、まわりへ広がる", "ろうがとける・示温テープの色が変わる"],
          ["水", "あたためられた水が上へ動き、上からじゅんに全体へ", "上の方だけ熱すると、下はなかなかあたたまらない", "示温インクの色・おがくずの動き"],
          ["空気", "あたためられた空気が上へ動き、上からじゅんに全体へ", "部屋の天井近くはあたたかく、足もとはつめたい", "線香のけむりの動き・温度計"]],
         ["物", "あたたまり方", "こんなことが起きる", "調べ方"]) + '''
<h3>試験管の水：熱する場所によるちがい（このシミュレーターの目安）</h3>
''' + T([["下", "約31秒", "約35秒", "約39秒", "全体があたたまる（上からじゅんに）"],
          ["真ん中", "約18秒", "約22秒", "なかなかあたたまらない", "熱した所より上だけ（下は数分たっても40℃に届かない）"],
          ["上（水面の近く）", "約6秒", "なかなかあたたまらない", "なかなかあたたまらない", "上の方だけ。約30秒で上はふっとうしても、下はつめたいまま"]],
         ["熱する場所", "上が40℃に", "真ん中が40℃に", "下が40℃に", "結果"]) + '''
<p>水20 mL（はじめ20℃）を、アルコールランプでおよそ一定の強さで熱したときの目安です。実際の時間は、火の強さや試験管の太さ、熱する位置で変わります。</p>
<h3>温度と体積の早見表（20℃の体積を100とする）</h3>
''' + T([["0℃（氷水）", "93.2", "99.8", "99.93"], ["20℃", "100", "100", "100"], ["40℃", "106.8", "100.6", "100.07"],
          ["60℃", "113.6", "101.5", "100.14"], ["80℃（湯）", "120.5", "102.7", "100.22"], ["100℃", "127.3", "104.2", "100.29"]],
         ["温度", "空気", "水", "金ぞく（鉄）"]) + '''
<p>空気は、おさえつけていなければ、温度（℃）に273を足した値（絶対温度）に比例して体積が変わります（シャルルの法則・先生向け）。水は約4℃で体積がいちばん小さくなり、それより高くなると少しずつ大きくなります。鉄の体積は1℃につき約0.0036％大きくなります。同じ大きさの試験管と同じ太さのガラス管で比べると、空気のしるしは数cm、水の先は数mm動くくらいのちがいになります。</p>
<h3>先生向けの補足：伝導と対流</h3>
<p>金ぞくのあたたまり方は「熱伝導」、水や空気のあたたまり方は「対流」とよばれます（どちらの用語も小学校では扱わず、中学校以降で学びます）。金ぞくのモデルでは、板を2.5 mmのマスに分け、熱拡散率（銅 1.11×10⁻⁴、アルミニウム 9.7×10⁻⁵、鉄 2.3×10⁻⁵ m²/s）を使って熱の広がりを計算しています。鉄は銅の約5分の1の速さでしか熱が広がらないので、同じ場所でもあたたまるのに時間がかかります。水と空気は、熱した所であたためられた水（空気）が上へ動いて上にたまり、そのぶん全体が少しずつ下へおし下げられる「層のモデル」（フィリングボックスモデル）で計算しています。</p>
''' + N('安全のために：アルコールランプやガスこんろを使うときは、保護眼鏡をかけ、まわりに燃えやすい物を置かないようにします。熱した金ぞくや試験管、湯はしばらく熱いので、直接さわらないようにします。試験管の水を熱するときは、試験管の口を人に向けず、急にふっとうしないように少しずつ熱します（ふっとう石を入れます）。') + '''
<h3>このシミュレーションで単純化していること</h3>
<ul>
<li>金ぞくの熱した所は約300℃に保ち、まわりの空気へ少しずつ熱がにげるものとしています。板の大きさは約10 cm四方、ぼうの長さは約12 cmです。温度の色は示温シールのイメージで、実際の示温テープは決まった温度で色が変わります。</li>
<li>水と空気の温度は、同じ高さではどこも同じになるようにした「層のモデル」です。熱した所の上の色の帯は、上へ動くあたたかい水（空気）を表しています。おがくずや線香のけむりの動きは、水や空気の動きを見やすくするためのイメージです。</li>
<li>試験管の水は一定の強さで熱するものとし、100℃でふっとうしたあとはそれ以上上がらないものとしています。ビーカーは約3倍、部屋は約10倍の速さで時間が進みます。部屋は、外が5℃で、はじめ10℃の部屋をストーブであたためるものとしています。</li>
<li>温度と体積の図では、ガラス管の中の動きを同じ倍率でかいています。金ぞくの変化は小さすぎて、図では見えません。</li>
</ul>
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「小学校学習指導要領（平成29年告示）解説 理科編」第4学年 A（2）金属，水，空気と温度（''' + A(MEXT_SHO, "小学校学習指導要領解説") + '''）</li>
<li>小学校理科の教科書（第4学年「もののあたたまり方」「ものの温度と体積」の単元）</li>
<li>国立天文台 編『理科年表』（金属の熱伝導率・比熱・線膨張率、水の密度）</li>
<li>M. Tanaka ほか（2001）Metrologia 38, 301–309（水の密度の式。水の体積の計算に使用）</li>
</ul>
'''

sim(slug="atatamarikata", cat="rika", emoji="🔥", score=81,
    title="物のあたたまり方シミュレーター（金属・水・空気）",
    title_tag="物のあたたまり方シミュレーター｜金属は熱した所から順に、水・空気は動いて全体があたたまる（小4理科 金属，水，空気と温度）",
    meta_desc="金属の板・ぼうは熱した所から順に、水と空気はあたためられた部分が上へ動いて全体があたたまる。示温インク・ろう・おがくず・線香のけむりのイメージで確かめる小4理科「金属，水，空気と温度」の無料シミュレーター。温度と体積（空気＞水＞金属）の切りかえつき。",
    og_title="物のあたたまり方シミュレーター（金属・水・空気）",
    og_desc="金属は熱した所から順に、水と空気は上へ動いて全体があたたまる。熱する場所を指でえらんで確かめる小4理科。温度と体積の比較も。",
    card_desc="金属は熱した所から順に、水と空気は上へ動いて全体に。熱する場所を指でえらんで確かめる。",
    lead="金ぞくの板やぼうは、指でタップした所を熱すると、熱した所から順に色が広がっていきます。試験管やビーカーの水、部屋の空気では、あたためられた部分が上へ動き、上の方からあたたまる様子を示温インクの色と温度のグラフで確かめられます。「温度と体積」に切りかえると、空気・水・金ぞくの体積の変わり方も比べられます。",
    model="小4 金属，水，空気と温度",
    level="小学4年",
    unit="小学校 第4学年 A（2）金属，水，空気と温度",
    canvas=canvas(640, 440, light=True),
    controls=select("mode", "何をあたためる？", [("plate", "金ぞくの板"), ("slit", "金ぞくの板（切れこみあり）"), ("rod", "金ぞくのぼう（かたむけたもの）"),
                                                ("tube", "試験管の水"), ("beaker", "ビーカーの水"), ("room", "部屋の空気（だんぼう）"), ("vol", "温度と体積（空気・水・金ぞく）")])
           + select("met", "金ぞくの種類", [("cu", "銅"), ("al", "アルミニウム"), ("fe", "鉄")])
           + select("look", "見え方", [("color", "温度の色（示温シール）"), ("wax", "ろうをぬった板・ぼう")])
           + select("posT", "熱する場所", [("bot", "下"), ("mid", "真ん中"), ("top", "上（水面の近く）")])
           + select("posB", "熱する場所", [("edge", "底のはし"), ("center", "底の真ん中")])
           + select("fan", "せんぷうき", [("off", "なし"), ("on", "あり（空気を回す）")])
           + slider("vt", "水そうの温度", 0, 100, 20, 1, "{v}℃"),
    buttons=btn("heat", "⏸ 熱するのを止める", True) + btn("reset", "⏮ はじめから") + btn("fast", "⏩ はやおくり")
           + btn("hot", "🔥 湯（80℃）につける", True) + btn("cold", "🧊 氷水（0℃）につける"),
    stats=stats([("sA", "熱しはじめて", False), ("sB", "ア・イ・ウの温度", True), ("sC", "あたたまった順", False), ("sD", "ろうがとけた所", False)]),
    legend="金ぞく：指でタップした所を熱します（ア・イ・ウは温度をはかる所）。色は温度（青＝20℃ → 赤＝100℃以上）、「ろうをぬった板・ぼう」では白いろうが約55℃でとけていきます。水：示温インク（約40℃で青→ピンク）とおがくず。空気：部屋のたての断面で、色は温度、灰色のすじは線香のけむり。右：ア・イ・ウ（上・真ん中・下）の温度の変わり方。数値は目安です。",
    article=ATA_ARTICLE,
    faqs=[("金属はどのようにあたたまりますか？", "熱した所から近いじゅんに、まわりへ広がるようにあたたまります。金属のぼうをかたむけて真ん中を熱しても、上にも下にも同じようにあたたまります。"),
          ("水はどのようにあたたまりますか？", "熱せられてあたたかくなった水が上へ動き、上の方にたまって、上からじゅんに全体があたたまります。示温インクを入れると、上の方から色が変わっていく様子が見られます。"),
          ("試験管の水の上の方を熱すると、下の水はどうなりますか？", "あたたかい水は上にとどまるので、下の方の水はなかなかあたたまりません。上の方の水がふっとうしていても、下の方はつめたいままのことがあります。水全体を早くあたためるには、下の方を熱します。"),
          ("空気はどのようにあたたまりますか？", "水と同じように、あたためられた空気が上へ動き、上の方からあたたまります。だんぼうをつけた部屋では天井近くがあたたかく、足もとはつめたくなりやすいので、せんぷうきやサーキュレーターで空気を回すと、部屋全体があたたまりやすくなります。"),
          ("温度による体積の変わり方は、空気・水・金属でどうちがいますか？", "どれも、あたためると体積が大きくなり、冷やすと小さくなりますが、変わり方は空気がいちばん大きく、次に水、金属はとても小さいです。20℃から80℃にすると、空気は約20％、水は約3％、鉄は約0.2％体積が大きくなります。"),
          ("示温インクとは何ですか？", "温度によって色が変わるインクです。水に入れて熱すると、あたたまった所の色が変わるので、水のあたたまり方を目で見ることができます。教科書の実験では、約40℃で青色からピンク色に変わるものなどが使われます。")],
    rel=[("joutai-henka", "🧊", "状態変化と粒子のシミュレーター"), ("kuuki-mizu", "💉", "とじこめた空気と水のシミュレーター"), ("tenki-kion", "🌡️", "天気と1日の気温のシミュレーター"),
         ("diffusion", "🫧", "拡散シミュレーター"), ("shitsudo-roten", "☁️", "湿度と雲のでき方シミュレーター")],
    js=JS_ATA)
