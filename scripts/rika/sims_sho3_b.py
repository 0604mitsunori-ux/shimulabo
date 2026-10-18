# -*- coding: utf-8 -*-
"""理科の授業向けシミュ（小学3年）：電気の通り道／光と音のせいしつ
   denki-toorimichi … 小3 A（5）電気の通り道（（ア）つなぎ方 （イ）電気を通す物・通さない物）
   hikari-oto       … 小3 A（3）光と音の性質（（ア）日光は直進し集めたり反射させたりできる （イ）明るさや暖かさ （ウ）音とふるえ）"""
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

MEXT_SHO = "https://www.mext.go.jp/a_menu/shotou/new-cs/1387014.htm"
def A(url, label): return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, label)

# 2本で共通の描画ヘルパー（JS）
HELP = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const FF='"Hiragino Sans","Hiragino Kaku Gothic ProN","Noto Sans JP","Yu Gothic UI","Yu Gothic",Meiryo,sans-serif';
  function tx(s,x,y,size,col,align,bold){ ctx.font=(bold?'bold ':'')+size+'px '+FF; ctx.fillStyle=col; ctx.textAlign=align||'left'; ctx.fillText(s,x,y); ctx.textAlign='left'; }
  function tw(s,size,bold){ ctx.font=(bold?'bold ':'')+size+'px '+FF; return ctx.measureText(s).width; }
  function rr(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
  function panel(x,y,w,h,fill){ ctx.fillStyle=fill||'#fff'; ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1.2; rr(x,y,w,h,10); ctx.fill(); ctx.stroke(); }
  function dot(x,y,r,fill,stroke){ ctx.fillStyle=fill; ctx.beginPath(); ctx.arc(x,y,r,0,6.2832); ctx.fill(); if(stroke){ ctx.strokeStyle=stroke; ctx.lineWidth=1; ctx.stroke(); } }
  function wrap(s,x,y,mw,size,col,lh,bold){ ctx.font=(bold?'bold ':'')+size+'px '+FF; let line='', yy=y; const NG='、。）」！？ー';
    for(const ch of s){ const t=line+ch; if(ctx.measureText(t).width>mw&&line&&NG.indexOf(ch)<0){ tx(line,x,yy,size,col,'left',bold); line=ch; yy+=lh; } else line=t; }
    if(line) tx(line,x,yy,size,col,'left',bold); return yy; }
  function warnTri(x,y,s){ ctx.fillStyle='#facc15'; ctx.strokeStyle='#b91c1c'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(x,y-s); ctx.lineTo(x+s*0.95,y+s*0.7); ctx.lineTo(x-s*0.95,y+s*0.7); ctx.closePath(); ctx.fill(); ctx.stroke(); tx('!',x,y+s*0.5,s*1.1,'#b91c1c','center',true); }
  const K=id=>$(id).previousElementSibling;
  function sh(id,m,sub){ const e=$(id); if(e) e.innerHTML=m+(sub?'<span style="display:block;font-size:12px;font-weight:700;color:#59616c;margin-top:2px">'+sub+'</span>':''); }
  function show(id,on){ const e=$(id); if(e) e.style.display=on?'':'none'; }
  function showF(id,on){ const e=$(id), f=e?e.closest('.field'):null; if(f) f.style.display=on?'':'none'; }
  const Q=new URLSearchParams(location.search);
'''

# ============================================================ 1 電気の通り道
JS_DENKI = HELP + r'''
  const C={bg:'#f8fafc',ink:'#0f172a',sub:'#64748b',ok:'#15803d',no:'#475569',red:'#dc2626',cu:'#d97706',teal:'#0e7490'};
  let mode='tsunagi', cut=false, loose=false, drag=null, danger=0, tNow=0, last=0, recs=[], seen={}, nLit=0, note='', obj=-1, tested=[0,0,0,0,0,0,0,0,0,0,0,0];
  // ---------- ① つなぎ方：かん電池（たて置き・上が＋きょく）、ソケットつき豆電球、どう線3本 ----------
  const BX=112, BT=152, BB=322;
  const TG={plus:{x:BX,y:BT-13,nm:'＋きょく'}, minus:{x:BX,y:BB+3,nm:'－きょく'}, side:{x:BX+31,y:248,nm:'かん電池の横'}};
  const NMS={plus:'＋きょく',minus:'－きょく',side:'横',none:'なし'}, SYM={plus:'＋',minus:'－',side:'横',none:'なし'};
  const SX=318, SG=82, LS=[{x:SX-9,y:SG+56},{x:SX+9,y:SG+56}], TRAY=[{x:56,y:410},{x:196,y:410}];
  let E=[];
  function home(){ E=[{x:TG.plus.x,y:TG.plus.y,at:'plus'},{x:250,y:376,at:null},{x:TRAY[0].x,y:TRAY[0].y,at:null},{x:TRAY[1].x,y:TRAY[1].y,at:null}]; cut=false; loose=false; }
  function put(i,k){ if(k){ E[i].at=k; E[i].x=TG[k].x; E[i].y=TG[k].y; } else { E[i].at=null; E[i].x=i===1?250:(i===0?300:TRAY[i-2].x); E[i].y=i<2?376:TRAY[i-2].y; } }
  function ev(){ const a=E[0].at, b=E[1].at, c=E[2].at, d=E[3].at;
    if((c==='plus'&&d==='minus')||(c==='minus'&&d==='plus')) return {k:'short',lit:false,ring:false,why:'かん電池の＋きょくと－きょくを、どう線だけでつないでいる（ショート回路）。'};
    const ring=(a==='plus'&&b==='minus')||(a==='minus'&&b==='plus');
    if(ring&&cut) return {k:'cut',lit:false,ring:false,why:'どう線がとちゅうで切れているので、わがつながっていない。'};
    if(ring&&loose) return {k:'loose',lit:false,ring:false,why:'豆電球がゆるんでいて、ソケットとつながっていない。'};
    if(ring) return {k:'ok',lit:true,ring:true,why:'＋きょく → 豆電球 → －きょくが、1つのわのようにつながっている。'};
    let why;
    if(!a&&!b) why='どう線がかん電池につながっていない。';
    else if(!a||!b) why='どう線が片方しかつながっていないので、わになっていない。';
    else if(a===b) why='どう線が両方とも'+TG[a].nm+'につながっている。';
    else why='かん電池の、きょくではない所（横）につないでいる。';
    if(cut) why+='（どう線も切れている）';
    return {k:'ng',lit:false,ring:false,why:why}; }
  function nmOf(k){ return NMS[k||'none']; }
  function record(){ const r=ev(); let lb, mk;
    if(r.k==='short'){ lb='ショート回路'; mk='!'; }
    else { lb=nmOf(E[0].at)+'・'+nmOf(E[1].at)+(cut?' 切れ':'')+(loose?' ゆるい':''); mk=r.lit?'o':'x'; }
    if(!seen[lb]){ seen[lb]=1; if(r.lit) nLit++; }
    if(!recs.length||recs[0].lb!==lb){ recs.unshift({lb:lb,mk:mk}); if(recs.length>6) recs.pop(); } }
  function after(){ const r=ev(); if(r.k==='short'&&danger<=0) danger=3.4; record(); stats(); }
  // どう線の形（ベジェ曲線）
  function bz(p0,p1,p2,p3,n){ const r=[]; for(let i=0;i<=n;i++){ const t=i/n, u=1-t; r.push([u*u*u*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t*t*t*p3[0], u*u*u*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t*t*t*p3[1]]); } return r; }
  const APP={plus:[0,-78],minus:[0,78],side:[78,0]}, APX={plus:[-78,-40],minus:[-78,40],side:[78,0]};
  function leadPts(i){ const s=LS[i], e=E[i], c2=e.at?[e.x+APP[e.at][0],e.y+APP[e.at][1]]:[e.x+(s.x-e.x)*0.2,e.y-50]; return bz([s.x,s.y],[s.x,s.y+90],c2,[e.x,e.y],48); }
  function extraPts(){ const a=E[2], b=E[3]; const c1=a.at?[a.x+APX[a.at][0],a.y+APX[a.at][1]]:[a.x+(b.x-a.x)*0.3,a.y-45], c2=b.at?[b.x+APX[b.at][0],b.y+APX[b.at][1]]:[b.x+(a.x-b.x)*0.3,b.y-45]; return bz([a.x,a.y],c1,c2,[b.x,b.y],48); }
  function poly(P,col,w){ ctx.strokeStyle=col; ctx.lineWidth=w; ctx.lineCap='round'; ctx.lineJoin='round'; ctx.beginPath(); P.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1])); ctx.stroke(); ctx.lineCap='butt'; }
  function wire(P,col,dark){ poly(P,dark,8.5); poly(P,col,5.5); }
  function tip(P,e,active){ const n=P.length-1; poly(P.slice(n-3),C.cu,4);
    if(!e.at){ ctx.setLineDash([4,3]); ctx.strokeStyle=active?C.red:C.teal; ctx.lineWidth=2; ctx.fillStyle='rgba(14,116,144,.12)'; ctx.beginPath(); ctx.arc(e.x,e.y,15,0,6.2832); ctx.fill(); ctx.stroke(); ctx.setLineDash([]); } }
  function pathLen(P){ let L=0; const cum=[0]; for(let i=1;i<P.length;i++){ L+=Math.hypot(P[i][0]-P[i-1][0],P[i][1]-P[i-1][1]); cum.push(L); } return {P:P,cum:cum,L:L}; }
  function at(pl,s){ const c=pl.cum; let i=1; while(i<c.length-1&&c[i]<s) i++; const f=(s-c[i-1])/Math.max(1e-6,c[i]-c[i-1]); return [pl.P[i-1][0]+(pl.P[i][0]-pl.P[i-1][0])*f, pl.P[i-1][1]+(pl.P[i][1]-pl.P[i-1][1])*f]; }
  function flow(P,n,sp){ const pl=pathLen(P); for(let k=0;k<n;k++){ const s=((k*pl.L/n)+tNow*sp)%pl.L; const p=at(pl,s); dot(p[0],p[1],3.4,'#fbbf24','#b45309'); } }

  function drawBattery(x,top,bot,w,small){ const g=ctx.createLinearGradient(x-w/2,0,x+w/2,0); g.addColorStop(0,'#1e3a8a'); g.addColorStop(0.45,'#3b82f6'); g.addColorStop(1,'#1e3a8a');
    ctx.fillStyle='#cbd5e1'; rr(x-w*0.15,top-12,w*0.3,14,3); ctx.fill(); ctx.strokeStyle='#64748b'; ctx.lineWidth=1; ctx.stroke();
    ctx.fillStyle=g; rr(x-w/2,top,w,bot-top,7); ctx.fill(); ctx.fillStyle='#e2e8f0'; ctx.fillRect(x-w/2,bot-8,w,8); ctx.strokeStyle='#64748b'; ctx.lineWidth=1.2; rr(x-w/2,top,w,bot-top,7); ctx.stroke();
    tx('＋',x,top+(small?20:28),small?16:22,'#fff','center',true); tx('－',x,bot-(small?12:18),small?16:22,'#fff','center',true);
    if(!small){ tx('かん',x,(top+bot)/2-4,13,'#fff','center',true); tx('電池',x,(top+bot)/2+13,13,'#fff','center',true); } }
  function drawBulb(x,gy,lit,lse,dim){ const off=lse?-9:0;
    if(lit){ const g=ctx.createRadialGradient(x,gy,6,x,gy,78); g.addColorStop(0,'rgba(253,224,71,.95)'); g.addColorStop(0.35,'rgba(253,224,71,.45)'); g.addColorStop(1,'rgba(253,224,71,0)'); ctx.fillStyle=g; ctx.beginPath(); ctx.arc(x,gy,78,0,6.2832); ctx.fill(); }
    // ソケット
    ctx.fillStyle='#e5e7eb'; ctx.strokeStyle='#64748b'; ctx.lineWidth=1.2; rr(x-21,gy+20,42,36,6); ctx.fill(); ctx.stroke();
    ctx.fillStyle='#94a3b8'; ctx.fillRect(x-21,gy+44,42,4);
    // 口金
    ctx.fillStyle='#cbd5e1'; ctx.fillRect(x-11,gy+12+off,22,14); ctx.strokeStyle='#94a3b8'; for(let i=0;i<3;i++){ ctx.beginPath(); ctx.moveTo(x-11,gy+15+i*4+off); ctx.lineTo(x+11,gy+17+i*4+off); ctx.stroke(); }
    // ガラス玉
    ctx.fillStyle=lit?'rgba(254,240,138,.95)':'rgba(226,232,240,.55)'; ctx.strokeStyle='#64748b'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.arc(x,gy-4+off,20,0,6.2832); ctx.fill(); ctx.stroke();
    ctx.strokeStyle=lit?'#b45309':'#78716c'; ctx.lineWidth=1.3; ctx.beginPath(); ctx.moveTo(x-6,gy+12+off); ctx.lineTo(x-6,gy-6+off); ctx.moveTo(x+6,gy+12+off); ctx.lineTo(x+6,gy-6+off); ctx.stroke();
    ctx.strokeStyle=lit?'#f97316':'#57534e'; ctx.lineWidth=lit?2.2:1.4; ctx.beginPath(); for(let i=0;i<=6;i++){ const xx=x-6+i*2, yy=gy-6+off+(i%2?-3:0); i?ctx.lineTo(xx,yy):ctx.moveTo(xx,yy); } ctx.stroke();
    if(lse) tx('ゆるんでいる',x+26,gy+22,11,C.red,'left',true); }

  function drawTsunagi(){ const r=ev();
    panel(8,8,422,424); tx('どう線の先を指で動かして、かん電池につなごう',18,28,13,C.ink,'left',true);
    // あまったどう線の置き場
    ctx.fillStyle='#f1f5f9'; rr(16,384,240,42,8); ctx.fill(); tx('あまったどう線',126,422,10.5,C.sub,'center',true);
    drawBattery(BX,BT,BB,60,false);
    tx('＋きょく',BX-38,BT-4,12,C.ink,'right',true); tx('－きょく',BX-38,BB+6,12,C.ink,'right',true);
    if(drag){ Object.keys(TG).forEach(k=>{ ctx.setLineDash([3,3]); ctx.strokeStyle='#0ea5e9'; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(TG[k].x,TG[k].y,13,0,6.2832); ctx.stroke(); ctx.setLineDash([]); });
      tx('横',TG.side.x+18,TG.side.y+4,11,'#0369a1','left',true); }
    drawBulb(SX,SG,r.lit,loose);
    tx('豆電球',SX+30,SG-12,12,C.ink,'left',true); tx('ソケット',SX+28,SG+44,11,C.sub,'left',true);
    // どう線（赤・黒）
    const P0=leadPts(0), P1=leadPts(1);
    wire(P0,'#ef4444','#991b1b');
    if(cut){ const m=Math.floor(P1.length*0.5); wire(P1.slice(0,m-3),'#334155','#0f172a'); wire(P1.slice(m+3),'#334155','#0f172a'); poly(P1.slice(m-5,m-2),C.cu,4); poly(P1.slice(m+3,m+6),C.cu,4); tx('✂ 切れている',P1[m][0]+12,P1[m][1]-8,11.5,C.red,'left',true); }
    else wire(P1,'#334155','#0f172a');
    tip(P0,E[0],drag&&drag.i===0); tip(P1,E[1],drag&&drag.i===1);
    // あまったどう線
    const PX=extraPts(); if(r.k==='short'){ poly(PX,'rgba(239,68,68,.35)',18); wire(PX,'#f97316','#b91c1c'); } else wire(PX,'#60a5fa','#1d4ed8');
    poly(PX.slice(0,3),C.cu,4); tip(PX,E[2],drag&&drag.i===2); tip(PX.slice().reverse(),E[3],drag&&drag.i===3);
    // 電気の通り道
    if(r.lit){ const pi=E[0].at==='plus'?0:1, mi=1-pi, Pp=leadPts(pi).reverse(), Pm=leadPts(mi);
      const mid=[[LS[pi].x,SG+30],[LS[pi].x,SG+6],[LS[mi].x,SG+6],[LS[mi].x,SG+30]];
      flow(Pp.concat(mid,Pm),26,70); }
    if(r.k==='short'){ warnTri(BX,BT+60,20); const ph=tNow*8; for(let i=0;i<3;i++){ ctx.strokeStyle='rgba(239,68,68,.7)'; ctx.lineWidth=2; ctx.beginPath(); for(let j=0;j<=10;j++){ const xx=40+i*12+Math.sin(ph+j)*3, yy=BT+40-j*6; j?ctx.lineTo(xx,yy):ctx.moveTo(xx,yy); } ctx.stroke(); }
      ctx.fillStyle='rgba(254,226,226,.97)'; ctx.strokeStyle=C.red; ctx.lineWidth=2.5; rr(150,190,272,96,10); ctx.fill(); ctx.stroke();
      tx('⚠ やってはいけない！',286,216,17,C.red,'center',true); wrap('ショート回路：どう線とかん電池が とても熱くなって あぶない。このどう線は外します。',162,240,250,12,'#7f1d1d',17,true); }
    if(note&&danger<=0) tx(note,262,398,11,C.red,'left',true); }
  function drawResult(){ const r=ev(), x=438, w=194; panel(x,8,w,424);
    if(r.k==='short'){ warnTri(x+24,42,14); tx('やってはいけない',x+44,48,15,C.red,'left',true); }
    else if(r.lit){ dot(x+22,40,12,'#fde047','#ca8a04'); tx('明かりがつく',x+42,47,16,C.ok,'left',true); }
    else { dot(x+22,40,12,'#e2e8f0','#94a3b8'); tx('明かりがつかない',x+42,47,15,C.no,'left',true); }
    const y1=wrap(r.why,x+12,76,w-22,12,C.ink,18,true);
    ctx.fillStyle=r.ring?'#dcfce7':'#f1f5f9'; rr(x+10,y1+12,w-20,46,8); ctx.fill();
    tx('電気の通り道（回路）',x+18,y1+30,11,C.sub,'left',true); tx(r.ring?'わになっている ○':'わになっていない ×',x+18,y1+50,13,r.ring?C.ok:C.no,'left',true);
    let yy=Math.max(y1+86,214); tx('ためしたつなぎ方',x+12,yy,12.5,C.ink,'left',true); tx('赤・黒',x+w-12,yy,10.5,C.sub,'right',true); yy+=8;
    if(!recs.length) tx('（まだない）',x+16,yy+18,11,'#94a3b8','left',true);
    recs.forEach((q,i)=>{ const y=yy+20+i*24; ctx.fillStyle=i===0?'#f0f9ff':'#fff'; rr(x+8,y-15,w-16,21,5); ctx.fill();
      tx(q.lb,x+14,y,11.5,C.ink,'left',true); const col=q.mk==='o'?C.ok:(q.mk==='!'?C.red:'#94a3b8'); tx(q.mk==='o'?'○ つく':(q.mk==='!'?'⚠ だめ':'× つかない'),x+w-12,y,11.5,col,'right',true); });
    tx('豆電球をタップすると、ゆるめる／しめる',x+12,422,10,C.sub,'left',true); }

  // ---------- ② 電気を通す物・通さない物（テスター） ----------
  const OB=[
    {nm:'鉄のくぎ',L:['鉄のくぎ'],sh:'鉄のくぎ',mat:'鉄',c:1,ic:'nail',hw:30},
    {nm:'紙',L:['紙'],sh:'紙',mat:'紙',c:0,ic:'paper',hw:24},
    {nm:'アルミニウムはく',L:['アルミニウム','はく'],sh:'アルミニウムはく',mat:'アルミニウム',c:1,ic:'foil',hw:28},
    {nm:'プラスチックのじょうぎ',L:['プラスチックの','じょうぎ'],sh:'プラスチック',mat:'プラスチック',c:0,ic:'ruler',hw:30},
    {nm:'10円玉',L:['10円玉'],sh:'10円玉',mat:'どう',c:1,ic:'coin',hw:16},
    {nm:'木のわりばし',L:['木のわりばし'],sh:'木のわりばし',mat:'木',c:0,ic:'wood',hw:30},
    {nm:'ガラスのコップ',L:['ガラスの','コップ'],sh:'ガラス',mat:'ガラス',c:0,ic:'glass',hw:18},
    {nm:'クリップ',L:['クリップ'],sh:'クリップ',mat:'鉄',c:1,ic:'clip',hw:24},
    {nm:'消しゴム',L:['消しゴム'],sh:'消しゴム',mat:'プラスチックなど',c:0,ic:'eraser',hw:20},
    {nm:'わゴム',L:['わゴム'],sh:'わゴム',mat:'ゴム',c:0,ic:'band',hw:24},
    {nm:'空きかん（ぬってある所）',L:['空きかん','（ぬってある所）'],sh:'かん（ぬってある所）',mat:'表面にぬってある物',c:0,ic:'can',hw:16},
    {nm:'空きかん（けずった所）',L:['空きかん','（けずった所）'],sh:'かん（けずった所）',mat:'鉄やアルミニウム',c:1,ic:'can2',hw:16}];
  function icon(k,x,y){ ctx.lineWidth=1.2;
    if(k==='nail'){ ctx.fillStyle='#94a3b8'; ctx.fillRect(x-26,y-2.5,46,5); ctx.fillRect(x-29,y-8,4,16); ctx.beginPath(); ctx.moveTo(x+20,y-2.5); ctx.lineTo(x+30,y); ctx.lineTo(x+20,y+2.5); ctx.fill(); }
    else if(k==='paper'){ ctx.fillStyle='#fff'; ctx.strokeStyle='#94a3b8'; ctx.fillRect(x-22,y-15,44,30); ctx.strokeRect(x-22,y-15,44,30); ctx.strokeStyle='#cbd5e1'; for(let i=0;i<3;i++){ ctx.beginPath(); ctx.moveTo(x-16,y-7+i*7); ctx.lineTo(x+16,y-7+i*7); ctx.stroke(); } }
    else if(k==='foil'){ const g=ctx.createLinearGradient(x-26,y-12,x+26,y+12); g.addColorStop(0,'#f1f5f9'); g.addColorStop(0.5,'#94a3b8'); g.addColorStop(1,'#e2e8f0'); ctx.fillStyle=g; ctx.strokeStyle='#64748b';
      ctx.beginPath(); ctx.moveTo(x-26,y-10); ctx.lineTo(x-10,y-14); ctx.lineTo(x+6,y-9); ctx.lineTo(x+26,y-12); ctx.lineTo(x+24,y+10); ctx.lineTo(x+4,y+14); ctx.lineTo(x-12,y+9); ctx.lineTo(x-25,y+12); ctx.closePath(); ctx.fill(); ctx.stroke(); }
    else if(k==='ruler'){ ctx.fillStyle='rgba(125,211,252,.6)'; ctx.strokeStyle='#0284c7'; ctx.fillRect(x-30,y-8,60,16); ctx.strokeRect(x-30,y-8,60,16); for(let i=0;i<=12;i++){ ctx.beginPath(); ctx.moveTo(x-28+i*4.7,y-8); ctx.lineTo(x-28+i*4.7,y-8+(i%2?4:7)); ctx.stroke(); } }
    else if(k==='coin'){ dot(x,y,15,'#c2773a','#7c2d12'); ctx.strokeStyle='#e8a873'; ctx.beginPath(); ctx.arc(x,y,11.5,0,6.2832); ctx.stroke(); tx('10',x,y+5,12,'#fff7ed','center',true); }
    else if(k==='wood'){ ctx.fillStyle='#d6a76c'; ctx.strokeStyle='#92400e'; [[-5],[4]].forEach(o=>{ ctx.beginPath(); ctx.moveTo(x-30,y+o[0]-3); ctx.lineTo(x+30,y+o[0]-2); ctx.lineTo(x+30,y+o[0]+1); ctx.lineTo(x-30,y+o[0]+3); ctx.closePath(); ctx.fill(); ctx.stroke(); }); }
    else if(k==='glass'){ ctx.fillStyle='rgba(186,230,253,.45)'; ctx.strokeStyle='#0369a1'; ctx.lineWidth=1.6; ctx.beginPath(); ctx.moveTo(x-17,y-17); ctx.lineTo(x-12,y+17); ctx.lineTo(x+12,y+17); ctx.lineTo(x+17,y-17); ctx.closePath(); ctx.fill(); ctx.stroke(); ctx.strokeStyle='rgba(255,255,255,.9)'; ctx.beginPath(); ctx.moveTo(x-9,y-12); ctx.lineTo(x-6,y+10); ctx.stroke(); }
    else if(k==='clip'){ ctx.strokeStyle='#64748b'; ctx.lineWidth=2.4; rr(x-24,y-9,48,18,9); ctx.stroke(); rr(x-16,y-4.5,36,9,4.5); ctx.stroke(); }
    else if(k==='eraser'){ ctx.fillStyle='#fff'; ctx.strokeStyle='#94a3b8'; rr(x-20,y-10,40,20,3); ctx.fill(); ctx.stroke(); ctx.fillStyle='#2563eb'; ctx.fillRect(x-4,y-11,20,22); tx('ERASE',x+6,y+3,7,'#fff','center',true); }
    else if(k==='band'){ ctx.strokeStyle='#b45309'; ctx.lineWidth=3; ctx.beginPath(); ctx.ellipse(x,y,23,10,0,0,6.2832); ctx.stroke(); }
    else if(k==='can'||k==='can2'){ ctx.fillStyle='#dc2626'; ctx.fillRect(x-15,y-17,30,34); ctx.fillStyle='#e2e8f0'; ctx.beginPath(); ctx.ellipse(x,y-17,15,4,0,0,6.2832); ctx.fill(); ctx.strokeStyle='#7f1d1d'; ctx.strokeRect(x-15,y-17,30,34);
      tx('かん',x,y+6,10,'#fff','center',true); if(k==='can2'){ ctx.fillStyle='#cbd5e1'; ctx.fillRect(x-15,y-4,30,10); ctx.strokeStyle='#64748b'; for(let i=0;i<6;i++){ ctx.beginPath(); ctx.moveTo(x-13+i*5,y-3); ctx.lineTo(x-10+i*5,y+5); ctx.stroke(); } } } }
  const TX0=8, TY0=252, TW=100, TH=88, TG2=4.8;
  function tileAt(x,y){ if(y<TY0||y>TY0+2*TH+6) return -1; const col=Math.floor((x-TX0)/(TW+TG2)), row=y<TY0+TH+3?0:1; if(col<0||col>5) return -1; return row*6+col; }
  function drawTester(){ const o=obj>=0?OB[obj]:null, lit=!!(o&&o.c);
    panel(8,8,322,236); tx('テスター（回路にすき間がある）',18,27,13,C.ink,'left',true);
    const L=44, R=296, Tp=96, B=210, gx=174, g0=gx-40, g1=gx+40;
    const wpath=[[L,112],[L,Tp],[R,Tp],[R,B],[g1,B]], wpath2=[[g0,B],[L,B],[L,186]];
    poly(wpath,'#0f172a',6); poly(wpath,'#ef4444',3.5); poly(wpath2,'#0f172a',6); poly(wpath2,'#334155',3.5);
    drawBattery(L,124,184,30,true);
    ctx.save(); ctx.translate(0,0); drawBulb(gx,Tp-30,lit,false); ctx.restore();
    // テスターの先（クリップ）
    const hw=o?o.hw:28; ctx.strokeStyle='#64748b'; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(g0,B); ctx.lineTo(gx-hw,B); ctx.moveTo(g1,B); ctx.lineTo(gx+hw,B); ctx.stroke();
    ctx.fillStyle='#94a3b8'; rr(g0-8,B-6,14,12,3); ctx.fill(); rr(g1-6,B-6,14,12,3); ctx.fill();
    if(o) icon(o.ic,gx,B); else { ctx.setLineDash([4,3]); ctx.strokeStyle='#0ea5e9'; ctx.lineWidth=1.5; rr(gx-30,B-16,60,32,6); ctx.stroke(); ctx.setLineDash([]); tx('ここに物',gx,B+5,10.5,'#0369a1','center',true); }
    tx('すき間に物をはさむ',gx,B+30,10.5,C.sub,'center',true);
    if(lit) flow([[L,112],[L,Tp],[gx-9,Tp],[gx-9,Tp-20],[gx+9,Tp-20],[gx+9,Tp],[R,Tp],[R,B],[L,B],[L,186]],22,60);
    if(o){ tx(o.nm,gx,136,12.5,C.ink,'center',true); tx(o.c?'明かりがつく → 電気を通す':'明かりがつかない → 通さない',gx,158,13,o.c?C.ok:C.no,'center',true); tx('（'+o.mat+'）',gx,177,11,C.sub,'center',true); }
    else { tx('下の物をタップして、',gx,146,12,C.teal,'center',true); tx('すき間に入れてみよう',gx,164,12,C.teal,'center',true); } }
  function drawTable(){ const x=338, w=294; panel(x,8,w,236);
    tx('調べた結果（表）',x+12,27,13,C.ink,'left',true);
    ctx.fillStyle='#dcfce7'; rr(x+8,36,138,24,6); ctx.fill(); ctx.fillStyle='#f1f5f9'; rr(x+150,36,136,24,6); ctx.fill();
    tx('電気を通す ○',x+16,53,12.5,C.ok,'left',true); tx('電気を通さない ×',x+158,53,12.5,C.no,'left',true);
    let a=0, b=0; OB.forEach((q,i)=>{ if(!tested[i]) return; if(q.c){ tx(q.sh,x+16,78+a*17,11.5,C.ink,'left',true); a++; } else { tx(q.sh,x+158,78+b*17,11.5,C.ink,'left',true); b++; } });
    if(!a) tx('（まだない）',x+16,78,11,'#94a3b8','left',true); if(!b) tx('（まだない）',x+158,78,11,'#94a3b8','left',true);
    ctx.strokeStyle='#e2e8f0'; ctx.beginPath(); ctx.moveTo(x+148,64); ctx.lineTo(x+148,192); ctx.stroke();
    ctx.fillStyle='#fefce8'; rr(x+8,196,w-16,42,7); ctx.fill();
    if(a) wrap('電気を通す物は、どれも 金ぞく（鉄・アルミニウム・どう）でできている。',x+14,213,w-28,11.5,'#854d0e',16,true);
    else wrap('金ぞくでできている物と、そうでない物をくらべよう。',x+14,213,w-28,11.5,'#854d0e',16,true); }
  function drawTiles(){ OB.forEach((q,i)=>{ const col=i%6, row=Math.floor(i/6), x=TX0+col*(TW+TG2), y=TY0+row*(TH+4), t=tested[i];
      ctx.fillStyle=i===obj?'#ecfeff':(t?(q.c?'#f0fdf4':'#f8fafc'):'#fff'); ctx.strokeStyle=i===obj?C.teal:'#cbd5e1'; ctx.lineWidth=i===obj?2.5:1.2; rr(x,y,TW,TH,9); ctx.fill(); ctx.stroke();
      icon(q.ic,x+TW/2,y+31);
      q.L.forEach((s,j)=>tx(s,x+TW/2,y+(q.L.length>1?64:70)+j*15,q.L.length>1?10.5:12,C.ink,'center',true));
      if(t){ const ok=q.c; dot(x+TW-13,y+13,10,ok?'#16a34a':'#94a3b8'); tx(ok?'○':'×',x+TW-13,y+18,12.5,'#fff','center',true); } }); }

  // ---------- 統計欄 ----------
  function stats(){ if(mode==='tsunagi'){ const r=ev();
      K('sA').innerHTML='豆電球の明かり'; sh('sA',r.k==='short'?'⚠ だめ':(r.lit?'つく':'つかない'),r.k==='short'?'ショート回路はやってはいけない':(r.lit?'回路ができている':'回路ができていない'));
      K('sB').innerHTML='電気の通り道（回路）'; sh('sB',r.ring?'わになる ○':'わでない ×',r.ring?'＋きょく→豆電球→－きょく':(r.k==='short'?'豆電球を通らない近道ができている':r.k==='cut'?'どう線が切れている':(r.k==='loose'?'豆電球がゆるんでいる':'どこかが切れている')));
      K('sC').innerHTML='どう線のつなぎ先'; sh('sC',SYM[E[0].at||'none']+' と '+SYM[E[1].at||'none'],'赤：'+nmOf(E[0].at)+'　黒：'+nmOf(E[1].at)+(cut?'（切れている）':''));
      K('sD').innerHTML='ためしたつなぎ方'; const n=Object.keys(seen).length; sh('sD',n+' 通り','明かりがついたのは '+nLit+' 通り');
      setShare('【電気の通り道】かん電池の＋きょく・豆電球・－きょくがどう線で1つの「わ」になると明かりがつく。いまのつなぎ方（'+nmOf(E[0].at)+'・'+nmOf(E[1].at)+'）は'+(r.k==='short'?'ショート回路（やってはいけない）':(r.lit?'明かりがついた':'明かりがつかない'))+'｜シミュラボ'); }
    else { const n=tested.reduce((s,v)=>s+v,0), yes=OB.filter((q,i)=>tested[i]&&q.c).map(q=>q.sh), no=OB.filter((q,i)=>tested[i]&&!q.c).map(q=>q.sh), o=obj>=0?OB[obj]:null;
      K('sA').innerHTML='調べた物'; sh('sA',n+' ／ 12',o?'いま：'+o.nm:'物をタップして調べる');
      K('sB').innerHTML='電気を通す物'; sh('sB',yes.length+' こ',yes.join('・')||'まだない');
      K('sC').innerHTML='電気を通さない物'; sh('sC',no.length+' こ',no.join('・')||'まだない');
      K('sD').innerHTML='わかること'; sh('sD','金ぞくは通す','鉄・アルミニウム・どう');
      setShare('【電気を通す物・通さない物】テスターで調べると、通す：'+(yes.join('・')||'—')+'／通さない：'+(no.join('・')||'—')+'。電気を通す物は金ぞく｜シミュラボ'); } }
  function vis(){ const a=mode==='tsunagi'; showF('ex',a); ['cut','loose','reset'].forEach(id=>show(id,a)); ['all','clr'].forEach(id=>show(id,!a));
    $('cut').textContent=cut?'🔗 どう線をつなぎなおす':'✂ どう線を切る'; $('loose').textContent=loose?'💡 豆電球をしめる':'💡 豆電球をゆるめる'; }
  function applyEx(v){ home(); danger=0; note='';
    if(v==='ok'){ put(1,'minus'); } else if(v==='same'){ put(1,'plus'); } else if(v==='side'){ put(1,'side'); } else if(v==='cut'){ put(1,'minus'); cut=true; }
    else if(v==='short'){ put(1,'minus'); put(2,'plus'); put(3,'minus'); } else if(v==='both'){ put(0,null); put(1,null); }
    vis(); after(); }
  function draw(){ ctx.fillStyle=C.bg; ctx.fillRect(0,0,W,H); if(mode==='tsunagi'){ drawTsunagi(); drawResult(); } else { drawTester(); drawTable(); drawTiles(); } }

  // ---------- 操作 ----------
  if(Q.has('mode')&&['tsunagi','tooshi'].indexOf(Q.get('mode'))>=0) $('mode').value=Q.get('mode');
  if(Q.has('ex')&&[].some.call($('ex').options,o=>o.value===Q.get('ex'))) $('ex').value=Q.get('ex');
  mode=$('mode').value; home();
  if(Q.has('obj')){ const i=+Q.get('obj'); if(i>=0&&i<12){ obj=i; tested[i]=1; } }
  if(Q.get('test')==='all') tested=tested.map(()=>1);
  $('mode').addEventListener('change',()=>{ mode=$('mode').value; vis(); stats(); });
  $('ex').addEventListener('change',()=>applyEx($('ex').value));
  $('cut').addEventListener('click',()=>{ cut=!cut; vis(); after(); });
  $('loose').addEventListener('click',()=>{ loose=!loose; vis(); after(); });
  $('reset').addEventListener('click',()=>{ $('ex').value='free'; applyEx('free'); recs=[]; seen={}; nLit=0; record(); stats(); });
  $('all').addEventListener('click',()=>{ tested=tested.map(()=>1); stats(); });
  $('clr').addEventListener('click',()=>{ tested=tested.map(()=>0); obj=-1; stats(); });
  cv.addEventListener('pointerdown',e=>{ const p=cpos(cv,e), x=p[0]/dpr, y=p[1]/dpr;
    if(mode==='tsunagi'){ if(danger>0) return; let bi=-1, bd=32; E.forEach((q,i)=>{ const d=Math.hypot(q.x-x,q.y-y); if(d<bd){ bd=d; bi=i; } });
      if(bi>=0){ drag={i:bi}; E[bi].at=null; note=''; $('ex').value='free'; try{ cv.setPointerCapture(e.pointerId); }catch(err){} }
      else if(Math.hypot(x-SX,y-SG)<36){ loose=!loose; vis(); after(); }
      return; }
    const t=tileAt(x,y); if(t>=0){ obj=t; tested[t]=1; stats(); } });
  cv.addEventListener('pointermove',e=>{ if(!drag) return; const p=cpos(cv,e); E[drag.i].x=clamp(p[0]/dpr,16,424); E[drag.i].y=clamp(p[1]/dpr,16,426); });
  const up=()=>{ if(!drag) return; const q=E[drag.i]; let best=null, bd=40; Object.keys(TG).forEach(k=>{ const d=Math.hypot(TG[k].x-q.x,TG[k].y-q.y); if(d<bd){ bd=d; best=k; } });
    if(best){ q.at=best; q.x=TG[best].x; q.y=TG[best].y; } drag=null; after(); };
  cv.addEventListener('pointerup',up); cv.addEventListener('pointercancel',up);
  function frame(t){ const dt=last?Math.min(0.05,(t-last)/1000):0; last=t; tNow+=dt;
    if(danger>0){ danger-=dt; if(danger<=0){ danger=0; put(2,null); put(3,null); note='あぶないので、どう線を外しました'; $('ex').value='free'; stats(); } }
    draw(); requestAnimationFrame(frame); }
  vis(); if(mode==='tsunagi'&&$('ex').value!=='free') applyEx($('ex').value); else { record(); stats(); }
  draw(); requestAnimationFrame(frame);
'''

DENKI_ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
<p>かん電池の<b>＋きょく</b>、豆電球、かん電池の<b>－きょく</b>が、どう線で<b>1つの「わ」のようにつながる</b>と、電気の通り道（<b>回路</b>）ができて、豆電球に明かりがつきます。どう線が片方しかつながっていない、両方とも同じきょくにつないでいる、かん電池の横（きょくではない所）につないでいる、どう線がとちゅうで切れている、豆電球がゆるんでいる――このようなときは、わがとぎれているので明かりはつきません。回路のとちゅうに物をはさんで調べると、<b>鉄・アルミニウム・どうなどの金ぞくは電気を通し</b>、紙・プラスチック・木・ガラス・ゴムは電気を通しません。</p>
''' + N('<b>対応する単元</b>：小学3年 A（5）電気の通り道「（ア）電気を通すつなぎ方と通さないつなぎ方があること」「（イ）電気を通す物と通さない物があること」。学習指導要領解説では、導線を乾電池の二つの極以外につないだり、つながっていなかったり、回路の一部が切れていたりすると豆電球が点灯しないことを捉えること、結果を表に分類・整理すること、「回路」という言葉を使って説明すること、乾電池の二つの極を直接導線でつながないよう安全に配慮することが示されています。') + '''
<h2>授業での使い方</h2>
<h3>導入：明かりがつくつなぎ方を予想する（①つなぎ方を調べる）</h3>
<p>実物の豆電球・ソケット・かん電池を配る前に、電子黒板でこのシミュレーターを見せ、「どこにどう線をつなぐと明かりがつくかな」と予想させます。赤いどう線は＋きょくにつながっています。黒いどう線の先を指で動かして、－きょく・＋きょく・かん電池の横などにつなぎ、明かりがつくかどうかを確かめます。右の「ためしたつなぎ方」に結果が残るので、つくつなぎ方とつかないつなぎ方をくらべ、共通点（わになっているか）を話し合えます。</p>
<h3>展開：つかないわけを考える・ショート回路の危険を知る</h3>
<p>「つなぎ方の例」から「どう線が切れている」「かん電池の横」を選んだり、豆電球をタップしてゆるめたりして、明かりがつかないわけを「回路」という言葉で説明させます。「ショート回路」は実験では絶対にやってはいけないつなぎ方です。シミュレーター上で危険マークを見せ、なぜあぶないのかを全員で確認してから実験に入ると安全です。</p>
<h3>まとめ：電気を通す物・通さない物（②電気を通す物を調べる）</h3>
<p>テスター（回路にすき間を作った物）のすき間に、身の回りの物を入れて調べ、表に仲間分けします。空きかんは、ぬってある所では明かりがつかず、紙やすりでけずった所ではつきます。「電気を通す物には、どんな共通点があるかな」と問い、金ぞくという言葉につなげます。</p>
<h3>児童への問いの例</h3>
<ol>
<li>豆電球に明かりがつくのは、どう線をかん電池のどこにつないだときでしょう？　つかなかったつなぎ方と、何がちがいますか？</li>
<li>どう線が両方ともかん電池につながっているのに、明かりがつかないことがありました。どうしてでしょう？</li>
<li>空きかんは、そのままでは明かりがつかないのに、けずるとつきました。どうしてでしょう？</li>
</ol>
<h2>しくみ・解説</h2>
<h3>言葉の意味（1文で）</h3>
<ul>
<li><b>回路</b>とは、かん電池の＋きょくから豆電球などを通って－きょくまで、電気が通る1つのわのような通り道のことです。</li>
<li><b>＋きょく・－きょく</b>とは、かん電池の両はしにある、電気の出入り口のことで、出っぱっている方が＋きょく、平らな方が－きょくです。</li>
<li><b>どう線</b>とは、電気を通すどう（金ぞく）の線を、電気を通さないビニルでおおった物のことです。</li>
<li><b>金ぞく</b>とは、鉄・アルミニウム・どうなどのなかまのことで、電気を通す、みがくと光るなどのせいしつがあります。</li>
<li><b>ショート回路</b>とは、かん電池の＋きょくと－きょくを、豆電球などを通さずにどう線だけでつないでしまう、とてもきけんなつなぎ方のことです。</li>
</ul>
<h3>つなぎ方の早見表</h3>
''' + T([["＋きょく と －きょく", "つく ○", "1つのわになっている（回路ができている）"],
          ["両方とも ＋きょく（または －きょく）", "つかない ×", "わになっていない"],
          ["片方だけつなぐ", "つかない ×", "わがとぎれている"],
          ["かん電池の横につなぐ", "つかない ×", "きょく以外の所では、電気の通り道にならない"],
          ["どう線がとちゅうで切れている", "つかない ×", "回路の一部が切れている"],
          ["豆電球がゆるんでいる", "つかない ×", "豆電球とソケットがつながっていない"],
          ["＋きょくと－きょくをどう線だけでつなぐ", "やってはいけない ⚠", "ショート回路。どう線やかん電池が熱くなってあぶない"]],
         ["つなぎ方", "明かり", "わけ"]) + '''
<h3>電気を通す物・通さない物の早見表</h3>
''' + T([["鉄のくぎ・クリップ", "鉄", "通す ○"], ["アルミニウムはく", "アルミニウム", "通す ○"], ["10円玉", "どう（どうのなかま）", "通す ○"],
          ["空きかん（けずった所）", "鉄やアルミニウム", "通す ○"], ["空きかん（ぬってある所）", "表面のとりょう（ぬり物）", "通さない ×"],
          ["紙", "紙", "通さない ×"], ["プラスチックのじょうぎ", "プラスチック", "通さない ×"], ["木のわりばし", "木", "通さない ×"],
          ["ガラスのコップ", "ガラス", "通さない ×"], ["消しゴム・わゴム", "プラスチックなど・ゴム", "通さない ×"]],
         ["調べた物", "できている物", "電気"]) + '''
<p>電気を通す物は、どれも<b>金ぞく</b>でできています。空きかんは鉄やアルミニウムでできていますが、表面がとりょうなどでぬってあると、そこでは電気が通りません。紙やすりでけずって金ぞくを出すと、電気を通します。</p>
<h3>ソケットを使わないとき（豆電球のつなぎ方）</h3>
<p>豆電球の中の細い線（フィラメント）の両はしは、口金の<b>横の部分</b>と、<b>おしりの出っぱり</b>の2か所につながっています。ソケットを使わずに明かりをつけるときは、この2か所にそれぞれどう線をつなぎ、かん電池の＋きょくと－きょくにつなぎます。どちらか1か所だけでは、わになりません。</p>
<h3>先生向けの補足</h3>
''' + N('・ショート回路の危険：豆電球（2.5 V・0.3 A 程度）を通すと流れる電流は約0.2〜0.3 Aですが、乾電池の両極を導線だけでつなぐと、乾電池の内部抵抗が小さいため数A（豆電球の10倍以上）の電流が流れ、導線や乾電池が発熱し、液もれや破裂の原因になります。<br>・電流の向き（＋極→－極）は第4学年「電流の働き」で扱います。本シミュレーターの黄色い粒は「電気が通っている」ことを示すための表示です。<br>・内容の取扱い（1）で、第3学年のA区分では3種類以上のものづくりを行うことになっています。スイッチやテスター、回路を使ったおもちゃ（電気を通す物を使ったクイズ・迷路など）が例です。') + '''
<h3>このシミュレーションで単純化していること</h3>
<ul>
<li>どう線の長さや太さ、かん電池の電気の残りぐあいは考えていません。明かりは「つく」「つかない」の2通りで表しています。</li>
<li>ショート回路は、実際にはどう線とかん電池が熱くなり、豆電球はほとんど光らなくなります。シミュレーターでは危険を知らせて、数秒でどう線を外すようにしています。</li>
<li>「電気を通す・通さない」は、豆電球がつくかどうかで分けています。えんぴつのしん（黒えん）や水道水などは電気をわずかに通しますが、かん電池1個と豆電球では明かりがつかないことが多いため、ここでは扱っていません。</li>
</ul>
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「小学校学習指導要領（平成29年告示）解説 理科編」第3学年 A（5）電気の通り道（''' + A(MEXT_SHO, "小学校学習指導要領・解説") + '''）</li>
<li>小学校理科の教科書（第3学年「電気の通り道」の単元）</li>
<li>一般社団法人 電池工業会「電池の正しい使い方」（ショートさせない・ほかの金属と一緒に持ち歩かない などの注意）</li>
</ul>
'''

sim(slug="denki-toorimichi", cat="rika", emoji="💡", score=81,
    title="電気の通り道シミュレーター（回路・電気を通す物）",
    title_tag="電気の通り道シミュレーター｜豆電球がつくつなぎ方と電気を通す物・通さない物（小3理科）",
    meta_desc="かん電池・豆電球・どう線を指でつないで、1つの「わ」（回路）になると明かりがつくことを確かめる小3理科「電気の通り道」の無料シミュレーター。つかないつなぎ方とショート回路の危険、テスターで鉄・アルミニウム・紙・プラスチックなどを調べて表に仲間分けできます。",
    og_title="電気の通り道シミュレーター（回路・電気を通す物）",
    og_desc="どう線を指でつないで、わになると豆電球がつく。ショート回路は危険マークで止める。テスターで電気を通す物・通さない物を表に分ける小3理科。",
    card_desc="どう線を指でつないで、わになると明かりがつく。テスターで電気を通す物を調べて表に仲間分け。",
    lead="どう線の先を指で動かして、かん電池につないでみましょう。＋きょく・豆電球・－きょくが1つのわになると明かりがつきます。②では、回路のすき間にくぎ・紙・アルミニウムはくなどを入れて、電気を通す物と通さない物を調べられます。",
    model="小3 電気の通り道",
    level="小学3年",
    unit="小学校 第3学年 A（5）電気の通り道",
    canvas=canvas(640, 440, light=True),
    controls=select("mode", "実けん", [("tsunagi", "① つなぎ方を調べる"), ("tooshi", "② 電気を通す物を調べる")])
           + select("ex", "つなぎ方の例", [("free", "自分でつなぐ"), ("ok", "＋きょくと－きょく（わになる）"), ("same", "両方とも＋きょく"),
                                        ("both", "どちらもつながない"), ("side", "かん電池の横につなぐ"), ("cut", "どう線が切れている"), ("short", "ショート回路（あぶない）")]),
    buttons=btn("cut", "✂ どう線を切る") + btn("loose", "💡 豆電球をゆるめる") + btn("reset", "↺ はじめから")
           + btn("all", "📋 全部調べる", True) + btn("clr", "表を消す"),
    stats=stats([("sA", "豆電球の明かり", True), ("sB", "電気の通り道（回路）", False), ("sC", "どう線のつなぎ先", False), ("sD", "ためしたつなぎ方", False)]),
    legend="①：どう線の先（点線の丸）を指で動かして、かん電池の＋きょく・－きょく・横につなげます。黄色の粒は、電気が通っていることを表します。左下の青いどう線で＋きょくと－きょくを直接つなぐと「ショート回路」になり、危険マークが出て、どう線は外されます。②：下の物をタップすると、テスターのすき間に入れて調べ、右の表に仲間分けします。",
    article=DENKI_ARTICLE,
    faqs=[("豆電球に明かりがつくのは、どんなつなぎ方ですか？", "かん電池の＋きょく、豆電球、かん電池の－きょくが、どう線で1つのわのようにつながったときです。このような電気の通り道を回路といいます。"),
          ("どう線を両方ともかん電池につないだのに、明かりがつかないのはなぜですか？", "両方とも同じきょく（＋きょくだけ・－きょくだけ）につないでいる、かん電池の横（きょくではない所）につないでいる、どう線がとちゅうで切れている、豆電球がゆるんでいる、などで、わがとぎれているからです。"),
          ("ショート回路とは何ですか？なぜあぶないのですか？", "かん電池の＋きょくと－きょくを、豆電球などを通さずにどう線だけでつなぐことです。大きな電気が流れて、どう線やかん電池が熱くなり、やけどや液もれの原因になるので、絶対にやってはいけません。"),
          ("電気を通す物と通さない物は、どうちがいますか？", "電気を通す物は、鉄・アルミニウム・どうなどの金ぞくでできています。紙・プラスチック・木・ガラス・ゴムは電気を通しません。"),
          ("空きかんは電気を通しますか？", "空きかんは鉄やアルミニウムでできているので、金ぞくが出ている所は電気を通します。ただし、表面がとりょうなどでぬってある所は電気を通さないので、紙やすりでけずってから調べると明かりがつきます。"),
          ("10円玉は電気を通しますか？", "通します。10円玉はどう（どうのなかまの金ぞく）でできているので、テスターのすき間に入れると明かりがつきます。")],
    rel=[("denki-kairo", "🔌", "電気回路シミュレーター"), ("magnet", "🧲", "磁力線シミュレーター"), ("hikari-oto", "🪞", "光と音のせいしつ"),
         ("mono-omosa", "⚖️", "物と重さ"), ("denryu-jikai", "🧭", "電流と磁界")],
    js=JS_DENKI)


# ============================================================ 2 光と音のせいしつ
JS_HIKARI = HELP + r'''
  const C={bg:'#f8fafc',ink:'#0f172a',sub:'#64748b',ok:'#15803d',red:'#dc2626',teal:'#0e7490',sun:'#f59e0b'};
  let mode='kagami', last=0, tNow=0, lastKey='';
  function banner(x,y,w,l1,l2){ ctx.fillStyle='rgba(254,226,226,.96)'; ctx.strokeStyle=C.red; ctx.lineWidth=1.8; rr(x,y,w,l2?42:26,7); ctx.fill(); ctx.stroke(); warnTri(x+16,y+(l2?20:13),9); tx(l1,x+32,y+18,12,'#991b1b','left',true); if(l2) tx(l2,x+32,y+35,12,'#991b1b','left',true); }
  function sun(x,y,r){ const g=ctx.createRadialGradient(x,y,2,x,y,r*2.2); g.addColorStop(0,'rgba(253,224,71,1)'); g.addColorStop(0.45,'rgba(253,224,71,.6)'); g.addColorStop(1,'rgba(253,224,71,0)'); ctx.fillStyle=g; ctx.beginPath(); ctx.arc(x,y,r*2.2,0,6.2832); ctx.fill(); dot(x,y,r,'#fbbf24','#f59e0b'); }

  // ===== ① かがみで日光をはね返す =====
  const GY=404, WX=410, WL=392, WT=68, WB=404, TY=210, T0=18, DT=5;
  const SD=(()=>{ const x=0.55,y=1,l=Math.hypot(x,y); return [x/l,y/l]; })();   // 日光の進む向き（左上から右下へ）
  const MXS=[118,196,274], MYY=378, ML=50;
  let nM=3, mir=[], sel=0, mdrag=false, tShow=T0;
  MXS.forEach(x=>mir.push({x:x,y:MYY,nx:0,ny:-1}));
  function aim(i,px,py){ const m=mir[i]; let rx=px-m.x, ry=py-m.y; const l=Math.hypot(rx,ry); if(l<1) return; rx/=l; ry/=l; let nx=rx-SD[0], ny=ry-SD[1]; const nl=Math.hypot(nx,ny); if(nl<1e-6) return; m.nx=nx/nl; m.ny=ny/nl; }
  function refl(m){ const d=SD[0]*m.nx+SD[1]*m.ny; return [SD[0]-2*d*m.nx, SD[1]-2*d*m.ny]; }
  function ends(m){ const tx_=-m.ny, ty_=m.nx; return [[m.x-tx_*ML/2,m.y-ty_*ML/2],[m.x+tx_*ML/2,m.y+ty_*ML/2]]; }
  function rayEnd(p,r){ let s=1e9; if(r[0]>1e-3) s=Math.min(s,(WX-p[0])/r[0]); if(r[0]<-1e-3) s=Math.min(s,(8-p[0])/r[0]); if(r[1]<-1e-3) s=Math.min(s,(8-p[1])/r[1]); if(r[1]>1e-3) s=Math.min(s,(GY-p[1])/r[1]); s=Math.max(0,s); const q=[p[0]+r[0]*s,p[1]+r[1]*s]; return {q:q,wall:r[0]>1e-3&&Math.abs(q[0]-WX)<0.5&&q[1]>=WT&&q[1]<=WB}; }
  function beams(){ const out=[]; for(let i=0;i<nM;i++){ const m=mir[i], r=refl(m), P=ends(m), a=rayEnd(P[0],r), b=rayEnd(P[1],r);
      let spot=null, hit=false; if(a.wall&&b.wall){ const lo=Math.min(a.q[1],b.q[1]), hi=Math.max(a.q[1],b.q[1]); spot=[lo,hi]; hit=lo<=TY+6&&hi>=TY-6; }
      out.push({m:m,r:r,P:P,a:a.q,b:b.q,spot:spot,hit:hit}); } return out; }
  const nHit=()=>beams().filter(b=>b.hit).length;
  function drawKagami(){ const B=beams(), h=B.filter(b=>b.hit).length;
    ctx.save(); rr(8,8,438,424,10); ctx.clip();
    const sky=ctx.createLinearGradient(0,8,0,GY); sky.addColorStop(0,'#bae6fd'); sky.addColorStop(1,'#f0f9ff'); ctx.fillStyle=sky; ctx.fillRect(8,8,438,GY-8);
    ctx.fillStyle='#86efac'; ctx.fillRect(8,GY,438,40); ctx.fillStyle='#4d7c0f'; ctx.fillRect(8,GY,438,3);
    // 日光（平行な光）
    ctx.strokeStyle='rgba(250,204,21,.35)'; ctx.lineWidth=1.2; for(let k=-12;k<12;k++){ const x0=k*44; ctx.beginPath(); ctx.moveTo(x0,8); ctx.lineTo(x0+SD[0]/SD[1]*(GY-8),GY); ctx.stroke(); }
    // 日かげのかべ
    ctx.fillStyle='#64748b'; ctx.fillRect(WL,WT,60,WB-WT); ctx.fillStyle='#475569'; ctx.fillRect(WL,WT,6,WB-WT);
    tx('日かげの',WL+30,WT-18,11,C.ink,'center',true); tx('かべ',WL+30,WT-5,11,C.ink,'center',true);
    dot(WX+6,TY,26,'#fff','#991b1b'); dot(WX+6,TY,18,'#ef4444'); dot(WX+6,TY,10,'#fff'); dot(WX+6,TY,4,'#ef4444');
    // かがみへ来る日光・はね返った光
    B.forEach(b=>{ ctx.fillStyle='rgba(253,224,71,.20)'; ctx.beginPath(); ctx.moveTo(b.P[0][0]-SD[0]*600,b.P[0][1]-SD[1]*600); ctx.lineTo(b.P[0][0],b.P[0][1]); ctx.lineTo(b.P[1][0],b.P[1][1]); ctx.lineTo(b.P[1][0]-SD[0]*600,b.P[1][1]-SD[1]*600); ctx.closePath(); ctx.fill(); });
    B.forEach(b=>{ ctx.fillStyle='rgba(250,204,21,.38)'; ctx.beginPath(); ctx.moveTo(b.P[0][0],b.P[0][1]); ctx.lineTo(b.a[0],b.a[1]); ctx.lineTo(b.b[0],b.b[1]); ctx.lineTo(b.P[1][0],b.P[1][1]); ctx.closePath(); ctx.fill();
      ctx.strokeStyle='rgba(234,179,8,.8)'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(b.P[0][0],b.P[0][1]); ctx.lineTo(b.a[0],b.a[1]); ctx.moveTo(b.P[1][0],b.P[1][1]); ctx.lineTo(b.b[0],b.b[1]); ctx.stroke(); });
    B.forEach(b=>{ if(!b.spot) return; ctx.fillStyle='rgba(255,251,200,.62)'; ctx.beginPath(); ctx.ellipse(WX+6,(b.spot[0]+b.spot[1])/2,26,(b.spot[1]-b.spot[0])/2+3,0,0,6.2832); ctx.fill(); });
    // かがみ
    B.forEach((b,i)=>{ const m=b.m; ctx.strokeStyle='#78716c'; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(m.x,m.y+4); ctx.lineTo(m.x,GY); ctx.stroke();
      ctx.strokeStyle='#334155'; ctx.lineWidth=7; ctx.beginPath(); ctx.moveTo(b.P[0][0]-m.nx*3,b.P[0][1]-m.ny*3); ctx.lineTo(b.P[1][0]-m.nx*3,b.P[1][1]-m.ny*3); ctx.stroke();
      ctx.strokeStyle='#e0f2fe'; ctx.lineWidth=4; ctx.beginPath(); ctx.moveTo(b.P[0][0],b.P[0][1]); ctx.lineTo(b.P[1][0],b.P[1][1]); ctx.stroke();
      if(i===sel){ ctx.setLineDash([4,3]); ctx.strokeStyle=C.teal; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(m.x,m.y,32,0,6.2832); ctx.stroke(); ctx.setLineDash([]); }
      tx(['①','②','③'][i],m.x-12,GY-6,13,b.hit?C.ok:C.ink,'right',true); if(b.hit) tx('当たり',m.x+5,GY-6,10.5,C.ok,'left',true); });
    sun(36,34,14);
    banner(64,12,320,'太陽を直接見ない／はね返した日光を','人の顔に当てない');
    ctx.restore(); ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1.2; rr(8,8,438,424,10); ctx.stroke();
    tx('かがみを指でつかんで、光を当てたい所へ動かそう',16,428,11,'#14532d','left',true); }
  function drawKagamiInfo(){ const x=454, w=178, h=nHit(), T=T0+DT*h; panel(x,8,w,424);
    tx('まと（日かげのかべ）',x+10,28,12.5,C.ink,'left',true);
    tx(h?'光 '+h+'まい分':'日かげのまま',x+10,56,19,h?'#b45309':C.sub,'left',true);
    // 温度計
    const tx0=x+30, ty0=78, ty1=230, tmin=10, tmax=40, ty=v=>ty1-(ty1-ty0)*(v-tmin)/(tmax-tmin);
    ctx.fillStyle='#fff'; ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1.5; rr(tx0-7,ty0-6,14,ty1-ty0+12,7); ctx.fill(); ctx.stroke(); dot(tx0,ty1+14,12,'#ef4444','#b91c1c');
    ctx.fillStyle='#ef4444'; ctx.fillRect(tx0-3.5,ty(tShow),7,ty1+6-ty(tShow));
    for(let v=10;v<=40;v+=5){ ctx.strokeStyle='#94a3b8'; ctx.beginPath(); ctx.moveTo(tx0+8,ty(v)); ctx.lineTo(tx0+(v%10?12:16),ty(v)); ctx.stroke(); if(v%10===0) tx(v+'℃',tx0+19,ty(v)+4,10,C.sub,'left',true); }
    tx(Math.round(tShow)+'℃',x+w-12,128,28,'#dc2626','right',true); tx('3分後の',x+w-12,152,10.5,C.sub,'right',true); tx('温度のめやす',x+w-12,166,10.5,C.sub,'right',true);
    // まい数と温度の表
    const by=262; tx('当てた光のまい数と温度',x+10,by,11.5,C.ink,'left',true);
    for(let k=0;k<=3;k++){ const yy=by+14+k*24, v=T0+DT*k, bw=(w-90)*(v-10)/30; ctx.fillStyle=k===h?'#fecaca':'#f1f5f9'; rr(x+8,yy-2,w-16,21,5); ctx.fill();
      tx(k?k+'まい':'0まい',x+14,yy+13,11,C.ink,'left',true); ctx.fillStyle=k===h?'#ef4444':'#fca5a5'; ctx.fillRect(x+54,yy+3,bw,11); tx(v+'℃',x+w-12,yy+13,11,C.ink,'right',true); }
    wrap('光を重ねるほど、まとは明るく、あたたかくなる。',x+10,380,w-20,12,'#854d0e',17,true); }

  // ===== ② 虫めがねで日光を集める =====
  const PY=388, LXc=196, PXc=12, F=15, D=6, TH=0.00931, TRN=0.9, CTH={black:30,white:200};
  let dd=7, paper='black', burn=0, burnt=null, ldrag=false, smoke=[];
  const spot=d=>D*Math.abs(F-d)/F+d*TH;          // 明るい部分の直径（cm）
  const conc=d=>TRN*Math.pow(D/spot(d),2);       // 明るさ（日光の何倍か）
  function lv(c){ const th=CTH[paper]; if(c>=th) return 3; if(c>=5) return 2; if(c>=1.5) return 1; return 0; }
  const LVN=['日なたと同じくらい','あたたかい','とても あつい','こげる！'], LVC=['#a16207','#ea580c','#dc2626','#7f1d1d'];
  function fmtD(s){ return s<1?(s*10).toFixed(1)+' mm':s.toFixed(1)+' cm'; }
  function fmtC(c){ return c<10?c.toFixed(1):(c<100?String(Math.round(c)):(c<1000?String(Math.round(c/10)*10):String(Math.round(c/100)*100))); }
  function drawMushi(){ const LY=PY-dd*PXc, s=spot(dd), c=conc(dd), L=lv(c), fy=LY+F*PXc;
    ctx.save(); rr(8,8,394,424,10); ctx.clip(); ctx.fillStyle='#f0f9ff'; ctx.fillRect(8,8,394,424);
    ctx.fillStyle='#d9f99d'; ctx.fillRect(8,PY+12,394,40);
    // 日光（真上から）
    ctx.strokeStyle='rgba(250,204,21,.45)'; ctx.lineWidth=1.3; for(let x=20;x<400;x+=18){ if(Math.abs(x-LXc)<=38){ ctx.beginPath(); ctx.moveTo(x,60); ctx.lineTo(x,LY); ctx.stroke(); } else { ctx.beginPath(); ctx.moveTo(x,60); ctx.lineTo(x,PY); ctx.stroke(); } }
    // 紙
    ctx.fillStyle=paper==='black'?'#1f2937':'#ffffff'; ctx.strokeStyle='#64748b'; ctx.lineWidth=1; ctx.fillRect(70,PY,260,10); ctx.strokeRect(70,PY,260,10);
    ctx.fillStyle='rgba(15,23,42,.35)'; ctx.fillRect(LXc-36,PY,72,3);
    // 集まる光
    const xl=LXc-36+36*dd/F, xr=LXc+36-36*dd/F, hs=Math.max(1.2,s*PXc/2);
    ctx.fillStyle='rgba(253,224,71,.42)'; ctx.beginPath(); ctx.moveTo(LXc-36,LY); ctx.lineTo(LXc+36,LY); ctx.lineTo(xr,PY); ctx.lineTo(xl,PY); ctx.closePath(); ctx.fill();
    ctx.strokeStyle='rgba(234,179,8,.85)'; ctx.lineWidth=1.2; for(let k=-2;k<=2;k++){ const x0=LXc+k*17; ctx.beginPath(); ctx.moveTo(x0,LY); ctx.lineTo(x0+(LXc-x0)*dd/F,PY); ctx.stroke(); }
    ctx.fillStyle='#fffbeb'; ctx.fillRect(LXc-hs,PY-2,hs*2,4); if(L>=2){ ctx.fillStyle='rgba(254,240,138,.9)'; ctx.beginPath(); ctx.arc(LXc,PY,Math.max(5,hs),Math.PI,0); ctx.fill(); }
    if(burnt) { ctx.fillStyle='#78350f'; ctx.fillRect(LXc-burnt/2,PY,burnt,3); }
    smoke.forEach(p=>{ ctx.fillStyle='rgba(100,116,139,'+(0.45*(1-p.a/2.2)).toFixed(3)+')'; ctx.beginPath(); ctx.arc(p.x,p.y,4+p.a*7,0,6.2832); ctx.fill(); });
    // 虫めがね
    ctx.fillStyle='rgba(186,230,253,.75)'; ctx.strokeStyle='#0369a1'; ctx.lineWidth=1.6; ctx.beginPath(); ctx.ellipse(LXc,LY,38,7,0,0,6.2832); ctx.fill(); ctx.stroke();
    ctx.fillStyle='#1f2937'; rr(LXc+38,LY-5,76,10,5); ctx.fill(); ctx.fillStyle='#475569'; rr(LXc+34,LY-6,10,12,3); ctx.fill();
    tx('虫めがね',LXc+50,LY-10,12,C.ink,'left',true); if(!ldrag) tx('↕ 指で上下に動かせる',LXc+50,LY+22,11,C.teal,'left',true);
    // きょりの目もり
    ctx.strokeStyle='#64748b'; ctx.lineWidth=1.3; ctx.beginPath(); ctx.moveTo(52,LY); ctx.lineTo(52,PY); ctx.stroke(); ctx.beginPath(); ctx.moveTo(46,LY); ctx.lineTo(58,LY); ctx.moveTo(46,PY); ctx.lineTo(58,PY); ctx.stroke();
    tx(dd.toFixed(1)+' cm',58,(LY+PY)/2+4,12,C.ink,'left',true);
    tx(paper==='black'?'黒い紙':'白い紙',334,PY+9,11,C.sub,'left',true);
    sun(40,30,12); banner(66,12,328,'虫めがねで 太陽を見てはいけない','集めた光を人・服・生き物に当てない');
    ctx.restore(); ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1.2; rr(8,8,394,424,10); ctx.stroke(); }
  function drawMushiInfo(){ const x=410, w=222, s=spot(dd), c=conc(dd), L=lv(c); panel(x,8,w,424);
    tx('上から見た紙',x+10,26,12.5,C.ink,'left',true);
    const cx=x+w/2, cy=122, k=13; ctx.fillStyle=paper==='black'?'#1f2937':'#ffffff'; ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1; ctx.fillRect(cx-90,cy-84,180,168); ctx.strokeRect(cx-90,cy-84,180,168);
    ctx.fillStyle=paper==='black'?'#0b1220':'#94a3b8'; ctx.beginPath(); ctx.arc(cx,cy,D/2*k,0,6.2832); ctx.fill();
    const r=Math.max(1.3,s/2*k), g=ctx.createRadialGradient(cx,cy,0,cx,cy,r*1.6+4); g.addColorStop(0,'rgba(255,255,255,1)'); g.addColorStop(0.55,L>=2?'rgba(254,249,195,1)':'rgba(254,240,138,.95)'); g.addColorStop(1,'rgba(253,224,71,0)');
    ctx.fillStyle=g; ctx.beginPath(); ctx.arc(cx,cy,r*1.6+4,0,6.2832); ctx.fill(); dot(cx,cy,r,'rgba(255,255,240,.95)');
    if(burnt){ const br=Math.max(4,burnt/PXc/2*k); ctx.fillStyle='#451a03'; ctx.beginPath(); for(let i=0;i<=16;i++){ const a=i/16*6.2832, rr_=br*(0.85+0.25*Math.sin(i*2.7)); i?ctx.lineTo(cx+Math.cos(a)*rr_,cy+Math.sin(a)*rr_):ctx.moveTo(cx+Math.cos(a)*rr_,cy+Math.sin(a)*rr_); } ctx.closePath(); ctx.fill(); }
    tx('明るい部分',x+10,234,12,C.sub,'left',true); tx(fmtD(s),x+w-12,236,19,C.ink,'right',true);
    tx('明るさ（日光の何倍）',x+10,264,12,C.sub,'left',true); tx('約'+fmtC(c)+'倍',x+w-12,266,19,'#b45309','right',true);
    tx('あたたかさ',x+10,294,12,C.sub,'left',true);
    const b0=x+12, b1=x+w-12, bw=(b1-b0)/4; LVC.forEach((cc,i)=>{ ctx.fillStyle=i<=L?cc:'#e5e7eb'; rr(b0+i*bw+1,302,bw-2,12,4); ctx.fill(); });
    tx(LVN[L],x+w/2,340,18,LVC[L],'center',true);
    wrap(L>=3?(paper==='black'?'明るい部分がとても小さく、黒い紙がこげて、けむりが出た！':'白い紙もこげ始めた！'):(s<1.2?'明るい部分が小さいほど、明るく、あつい。':'虫めがねを動かして、明るい部分を小さくしてみよう。'),x+12,366,w-24,12,C.ink,17,true);
    tx(paper==='black'?'黒い紙は光を吸い、あたたまりやすい':'白い紙は光をはね返し、こげにくい',x+12,420,10.5,C.sub,'left',true); }

  // ===== ③ 音のふるえ =====
  const INS={tri:{nm:'トライアングル',bt:'🔔 たたく',tau:1.5,fv:9,lab:'たたく強さ'},drum:{nm:'たいこ',bt:'🥁 たたく',tau:0.45,fv:6,lab:'たたく強さ'},
             gomu:{nm:'わゴム',bt:'🎸 はじく',tau:0.9,fv:7,lab:'はじく強さ'},ito:{nm:'糸電話',bt:'🗣 話す（もしもし）',tau:0.5,fv:8,lab:'声の大きさ'}};
  const PWN=['','よわい','少しよわい','ふつう','少し強い','強い'], VLN=['','小さい','少し小さい','ふつう','少し大きい','大きい'];
  let ins='tri', pw=3, hit=null, prev=null, pinch=false, soundOn=false, beads=[], AC=null, master=null, nodes=[], stopT=null;
  for(let i=0;i<9;i++) beads.push({x:-80+i*20+rnd(-4,4),y:0,vy:0,c:['#ef4444','#3b82f6','#22c55e','#eab308'][i%4]});
  function amp(h,t){ if(!h||t<0) return 0; let a; if(h.ins==='ito') a=t<1.4?h.pw*Math.min(1,t/0.08)*(0.55+0.45*Math.abs(Math.sin(Math.PI*t/0.35))):h.pw*Math.exp(-(t-1.4)/0.12);
    else a=h.pw*Math.exp(-t/INS[h.ins].tau); if(h.damp!=null&&t>h.damp) a*=Math.exp(-(t-h.damp)/0.05); return a; }
  const disp=(h,t)=>amp(h,t)*Math.sin(2*Math.PI*INS[h.ins].fv*t);
  const rdisp=(h,t)=>(pinch||t<0.08)?0:0.7*disp(h,t-0.08);
  const el=()=>hit?tNow-hit.t0:99;
  const moving=()=>amp(hit,el())>0.12;
  // 音（ボタンを押したときだけ・数秒で自動停止）
  function getAC(){ if(!AC){ const Ctor=window.AudioContext||window.webkitAudioContext; if(!Ctor) return null; AC=new Ctor(); } if(AC.state==='suspended'&&AC.resume) AC.resume(); return AC; }
  function stopSound(){ clearTimeout(stopT); if(AC&&master){ const n=AC.currentTime, g=master; g.gain.cancelScheduledValues(n); g.gain.setValueAtTime(g.gain.value,n); g.gain.linearRampToValueAtTime(0,n+0.05); nodes.forEach(o=>{ try{ o.stop(n+0.07); }catch(err){} }); setTimeout(()=>{ try{ g.disconnect(); }catch(err){} },300); } master=null; nodes=[]; }
  function playIns(h){ if(!soundOn) return; const c=getAC(); if(!c) return; stopSound(); const n0=c.currentTime, vol=0.022*h.pw;
    master=c.createGain(); master.gain.setValueAtTime(1,n0); master.connect(c.destination);
    const add=(type,f,g0,tau,f2)=>{ const o=c.createOscillator(), g=c.createGain(); o.type=type; o.frequency.setValueAtTime(f,n0); if(f2) o.frequency.exponentialRampToValueAtTime(f2,n0+0.25);
      g.gain.setValueAtTime(0.0001,n0); g.gain.exponentialRampToValueAtTime(g0,n0+0.008); g.gain.exponentialRampToValueAtTime(0.0001,n0+tau*5); o.connect(g); g.connect(master); o.start(n0); o.stop(n0+tau*5+0.05); nodes.push(o); };
    if(h.ins==='tri'){ add('sine',1320,vol,0.6); add('sine',1320*2.76,vol*0.45,0.4); add('sine',1320*5.4,vol*0.2,0.25); }
    else if(h.ins==='drum'){ add('sine',120,vol*1.6,0.12,55); add('triangle',190,vol*0.5,0.05); }
    else if(h.ins==='gomu'){ add('triangle',196,vol*1.4,0.25); add('sine',392,vol*0.4,0.18); }
    else if(!pinch){ const o=c.createOscillator(), g=c.createGain(); o.type='triangle'; o.frequency.setValueAtTime(260,n0); g.gain.setValueAtTime(0.0001,n0);
      for(let k=0;k<4;k++){ const t0=n0+k*0.35; o.frequency.setValueAtTime(k%2?300:250,t0); g.gain.linearRampToValueAtTime(vol*0.9,t0+0.06); g.gain.linearRampToValueAtTime(vol*0.25,t0+0.3); }
      g.gain.linearRampToValueAtTime(0.0001,n0+1.5); o.connect(g); g.connect(master); o.start(n0); o.stop(n0+1.6); nodes.push(o); }
    stopT=setTimeout(stopSound,4000); }
  function strike(){ if(hit&&hit.ins===ins) prev=hit; else prev=null; hit={ins:ins,pw:pw,t0:tNow,damp:null};
    if(ins==='drum') beads.forEach(b=>{ b.vy=-(70+pw*58)*rnd(0.85,1.15); }); playIns(hit); lastKey=''; stats(); }
  function damp(){ if(hit&&moving()){ hit.damp=el(); } stopSound(); lastKey=''; stats(); }
  function drawOto(){ const t=el(), dsp=hit?disp(hit,t):0, A=hit?amp(hit,t):0;
    panel(8,8,384,284); tx(INS[ins].nm,18,28,13.5,C.ink,'left',true);
    if(ins==='tri'){ const cx=200, sx=dsp*2.6;
      ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.moveTo(cx,38); ctx.lineTo(cx+sx*0.3,78); ctx.stroke();
      if(A>0.15){ [1,-1].forEach(sg=>{ ctx.strokeStyle='rgba(148,163,184,.35)'; ctx.lineWidth=6; ctx.beginPath(); ctx.moveTo(cx+sg*A*2.6,80); ctx.lineTo(cx-78+sg*A*2.6,215); ctx.lineTo(cx+78+sg*A*2.6,215); ctx.lineTo(cx+12+sg*A*2.6,100); ctx.stroke(); }); }
      ctx.strokeStyle='#64748b'; ctx.lineWidth=6; ctx.lineJoin='round'; ctx.beginPath(); ctx.moveTo(cx+sx,80); ctx.lineTo(cx-78+sx,215); ctx.lineTo(cx+78+sx,215); ctx.lineTo(cx+12+sx,100); ctx.stroke();
      const bt=t<0.15?(1-t/0.15):1; ctx.strokeStyle='#475569'; ctx.lineWidth=4; ctx.beginPath(); ctx.moveTo(cx+150,180); ctx.lineTo(cx+54+bt*46,160); ctx.stroke();
      if(A>0.15){ ctx.strokeStyle='rgba(14,116,144,.6)'; ctx.lineWidth=2; for(let k=1;k<=Math.min(4,Math.ceil(A));k++){ ctx.beginPath(); ctx.arc(cx-100,150,14*k,2.2,4.1); ctx.stroke(); } } }
    else if(ins==='drum'){ const cx=200, ty=150+dsp*1.4;
      ctx.fillStyle='#b91c1c'; ctx.fillRect(cx-110,150,220,96); ctx.fillStyle='#fde68a'; for(let k=0;k<6;k++) ctx.fillRect(cx-108+k*40,150,6,96);
      ctx.fillStyle='#7f1d1d'; ctx.beginPath(); ctx.ellipse(cx,246,110,22,0,0,3.1416); ctx.fill();
      ctx.fillStyle='#fef3c7'; ctx.strokeStyle='#92400e'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(cx-110,150); ctx.quadraticCurveTo(cx,ty+(ty-150),cx+110,150); ctx.quadraticCurveTo(cx,150+26,cx-110,150); ctx.ellipse(cx,150,110,24,0,0,6.2832); ctx.fill(); ctx.stroke();
      beads.forEach(b=>dot(cx+b.x,150-6+b.y+(ty-150)*(1-Math.abs(b.x)/110),5,b.c,'rgba(15,23,42,.5)'));
      const bt=t<0.15?(1-t/0.15):1; ctx.strokeStyle='#78350f'; ctx.lineWidth=6; ctx.lineCap='round'; ctx.beginPath(); ctx.moveTo(cx+150,60); ctx.lineTo(cx+40+bt*20,128-bt*50); ctx.stroke(); ctx.lineCap='butt'; dot(cx+40+bt*20,128-bt*50,8,'#fde68a','#78350f');
      tx('まくの上にビーズをのせている',18,48,11,C.sub,'left',true); }
    else if(ins==='gomu'){ const x0=70, x1=330, y=150;
      ctx.fillStyle='#e2e8f0'; ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1.5; rr(50,160,300,80,10); ctx.fill(); ctx.stroke(); ctx.fillStyle='#334155'; ctx.beginPath(); ctx.ellipse(200,200,34,22,0,0,6.2832); ctx.fill();
      ctx.fillStyle='#a16207'; ctx.fillRect(x0-6,y-4,12,14); ctx.fillRect(x1-6,y-4,12,14);
      if(A>0.15){ ctx.fillStyle='rgba(180,83,9,.18)'; ctx.beginPath(); for(let i=0;i<=40;i++){ const u=i/40; ctx.lineTo(x0+(x1-x0)*u,y-A*5*Math.sin(Math.PI*u)); } for(let i=40;i>=0;i--){ const u=i/40; ctx.lineTo(x0+(x1-x0)*u,y+A*5*Math.sin(Math.PI*u)); } ctx.closePath(); ctx.fill(); }
      ctx.strokeStyle='#b45309'; ctx.lineWidth=3; ctx.beginPath(); for(let i=0;i<=40;i++){ const u=i/40, yy=y+dsp*5*Math.sin(Math.PI*u); i?ctx.lineTo(x0+(x1-x0)*u,yy):ctx.moveTo(x0,yy); } ctx.stroke();
      tx('箱にはったわゴム',50,256,11,C.sub,'left',true); }
    else { const y=150, x0=96, x1=304, px=200, v=300;
      const cup=(x,dir,sh_)=>{ ctx.fillStyle='#fef3c7'; ctx.strokeStyle='#92400e'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.moveTo(x,y-18+sh_); ctx.lineTo(x-dir*40,y-30+sh_); ctx.lineTo(x-dir*40,y+30+sh_); ctx.lineTo(x,y+18+sh_); ctx.closePath(); ctx.fill(); ctx.stroke(); };
      cup(x0,1,dsp*0.8); const rd=hit?rdisp(hit,t):0; cup(x1,-1,rd*0.8);
      ctx.strokeStyle='#475569'; ctx.lineWidth=1.8; ctx.beginPath(); for(let X=x0;X<=x1;X+=2){ const tt=t-(X-x0)/v; let yy=y; if(hit&&!(pinch&&X>px)) yy=y+(hit?disp(hit,tt):0)*1.6*(1-(X-x0)/(x1-x0)*0.3); X===x0?ctx.moveTo(X,yy):ctx.lineTo(X,yy); } ctx.stroke();
      if(pinch){ dot(px,y-9,8,'#fcd9b6','#c08457'); dot(px,y+9,8,'#fcd9b6','#c08457'); tx('糸をつまんでいる',px,y-26,11.5,C.red,'center',true); }
      else tx('糸をタップすると、つまめる',px,y-26,11,C.teal,'center',true);
      tx('話す人',x0-20,y+52,12,C.ink,'center',true); tx('聞く人',x1+20,y+52,12,C.ink,'center',true);
      const heard=hit&&amp(hit,t)>0.12; if(heard) tx(pinch?'聞こえない…':'聞こえる！',x1+20,y+72,13,pinch?C.sub:C.ok,'center',true);
      tx('ピンとはった糸がふるえて、音がつたわる',30,256,11.5,C.sub,'left',true); }
    tx(moving()?'ふるえている（音が出ている）':(hit&&hit.damp!=null?'手でおさえた → ふるえも音も止まった':'止まっている（音は出ていない）'),18,280,12,moving()?C.ok:C.sub,'left',true); }
  function meter(x,y,w,lab,v,col){ tx(lab,x,y,12,C.ink,'left',true); ctx.fillStyle='#e5e7eb'; rr(x,y+8,w,16,8); ctx.fill(); if(v>0.01){ ctx.fillStyle=col; rr(x,y+8,Math.max(16,w*Math.min(1,v/5)),16,8); ctx.fill(); } }
  function drawOtoInfo(){ const x=400, w=232, t=el(), A=hit?amp(hit,t):0; panel(x,8,w,284);
    tx(INS[ins].lab+'：'+pw+'（'+PWN[pw]+'）',x+12,30,13,C.ink,'left',true);
    meter(x+12,58,w-24,'ふるえの大きさ（いま）',A,'#0ea5e9'); meter(x+12,104,w-24,'音の大きさ（いま）',ins==='ito'&&pinch?0:A,'#f97316');
    const last_=hit?hit.pw:0, pv=prev?prev.pw:0;
    ctx.fillStyle='#f8fafc'; rr(x+10,142,w-20,64,8); ctx.fill();
    tx('いま：強さ '+(last_||'—'),x+18,162,12,'#1d4ed8','left',true); tx(last_?'ふるえ・音 '+VLN[last_]:'',x+w-16,162,11.5,'#1d4ed8','right',true);
    tx('前　：強さ '+(pv||'—'),x+18,186,12,'#64748b','left',true); tx(pv?'ふるえ・音 '+VLN[pv]:'',x+w-16,186,11.5,'#64748b','right',true);
    wrap(ins==='ito'?(pinch?'糸をつまむと、ふるえがそこで止まり、聞く人には聞こえない。':'話すとコップがふるえ、糸をつたって、聞く人のコップもふるえる。'):'強く'+(ins==='gomu'?'はじく':'たたく')+'と、ふるえが大きく、音も大きい。ふるえを止めると、音も止まる。',x+12,228,w-24,12,'#854d0e',17,true); }
  function drawWave(){ const x=8, y=300, w=624, h=132; panel(x,y,w,h);
    tx('ふるえのようす（たてのはば ＝ ふるえの大きさ）',x+12,y+19,12.5,C.ink,'left',true); tx('※ふるえは見やすいように、ゆっくりにしてあります',x+w-12,y+19,10.5,C.sub,'right',true);
    const X0=x+44, X1=x+w-14, TM=2.5, gx=tt=>X0+(X1-X0)*tt/TM;
    const strip=(y0,hh,fn,h_,col,lw,upto,label)=>{ const yc=y0+hh/2; ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(X0,yc); ctx.lineTo(X1,yc); ctx.stroke();
      if(label) tx(label,X0-6,yc+4,10.5,col,'right',true); if(!h_) return; ctx.strokeStyle=col; ctx.lineWidth=lw; ctx.beginPath(); const tm=Math.min(TM,upto);
      for(let X=X0;X<=gx(tm);X+=1.5){ const tt=(X-X0)/(X1-X0)*TM, yy=yc-fn(h_,tt)/5*(hh/2-3); X===X0?ctx.moveTo(X,yy):ctx.lineTo(X,yy); } ctx.stroke(); };
    if(ins==='ito'){ strip(y+26,48,disp,hit,'#2563eb',1.8,el(),'話す'); strip(y+76,48,rdisp,hit,'#16a34a',1.8,el(),'聞く'); }
    else { strip(y+26,96,disp,prev,'#94a3b8',1.4,99,''); strip(y+26,96,disp,hit,'#2563eb',2,el(),''); tx('いま',X0-8,y+64,11,'#2563eb','right',true); tx('前',X0-8,y+82,11,'#94a3b8','right',true); }
    for(let s=0;s<=2.5;s+=0.5) tx(s+'秒',gx(s),y+h-4,10,C.sub,'center',false);
    if(hit&&el()<TM){ ctx.strokeStyle='rgba(220,38,38,.6)'; ctx.lineWidth=1.2; ctx.beginPath(); ctx.moveTo(gx(el()),y+26); ctx.lineTo(gx(el()),y+122); ctx.stroke(); } }

  // ===== 統計欄・表示切りかえ =====
  function stats(){ let key=mode;
    if(mode==='kagami'){ const h=nHit(); key+=nM+'|'+h; if(key===lastKey) return; lastKey=key;
      K('sA').innerHTML='かがみの数'; sh('sA',nM+' まい','まとに当たっている光 '+h+' まい');
      K('sB').innerHTML='まとの明るさ'; sh('sB',h?'光 '+h+' まい分':'日かげのまま',h>=2?'光を重ねると、もっと明るい':(h?'日かげより明るい':'かがみを動かして光を当てよう'));
      K('sC').innerHTML='まとの温度（めやす）'; sh('sC',(T0+DT*h)+' ℃','日かげ '+T0+' ℃より +'+(DT*h)+' ℃');
      K('sD').innerHTML='日光の進み方'; sh('sD','まっすぐ進む','かがみではね返すと向きが変わる');
      setShare('【光のせいしつ】かがみ'+nM+'まいで日光をはね返し、'+h+'まい分の光をまとに重ねると、まとの温度は約'+(T0+DT*h)+'℃（日かげ'+T0+'℃）。光を重ねるほど明るく、あたたかくなる｜シミュラボ'); }
    else if(mode==='mushi'){ const s=spot(dd), c=conc(dd), L=lv(c); key+=dd+paper+L+(burnt?1:0); if(key===lastKey) return; lastKey=key;
      K('sA').innerHTML='虫めがねと紙のきょり'; sh('sA',dd.toFixed(1)+' cm',dd>=13&&dd<=17?'光がいちばん集まる近く':'');
      K('sB').innerHTML='明るい部分の大きさ'; sh('sB',fmtD(s),'直径（虫めがねは直径6 cm）');
      K('sC').innerHTML='明るさ（日光の何倍）'; sh('sC','約'+fmtC(c)+'倍','明るい部分が小さいほど明るい');
      K('sD').innerHTML='紙のようす'; sh('sD',LVN[L]+(burnt&&L<3?'（こげあと）':''),paper==='black'?'黒い紙':'白い紙');
      setShare('【光のせいしつ】虫めがねを紙から'+dd.toFixed(1)+' cm にすると、明るい部分の直径は'+fmtD(s)+'、明るさは日光の約'+fmtC(c)+'倍（'+(paper==='black'?'黒い紙':'白い紙')+'：'+LVN[L]+'）｜シミュラボ'); }
    else { const mv=moving(); key+=ins+pw+mv+pinch+(hit?hit.t0:0); if(key===lastKey) return; lastKey=key;
      K('sA').innerHTML=INS[ins].lab; sh('sA',pw+'（'+PWN[pw]+'）','5だんかい');
      K('sB').innerHTML='ふるえの大きさ'; sh('sB',VLN[pw],pw>1?'よわい時の約'+pw+'倍のはば（めやす）':'いちばん小さい');
      K('sC').innerHTML='音の大きさ'; sh('sC',ins==='ito'&&pinch?'聞こえない':VLN[pw],ins==='ito'&&pinch?'糸をつまんでいる':'ふるえが大きいほど大きい');
      K('sD').innerHTML='いま'; sh('sD',mv?'ふるえている':'止まっている',mv?(ins==='ito'&&pinch?'聞く人には聞こえない':'音が出ている'):'音は出ていない');
      setShare(ins==='ito'?'【音のせいしつ】糸電話は、話すとコップと糸がふるえて音がつたわる。糸をつまむと、ふるえが止まって聞こえなくなる｜シミュラボ':'【音のせいしつ】'+INS[ins].nm+'を強さ'+pw+'で'+(ins==='gomu'?'はじく':'たたく')+'と、ふるえは'+VLN[pw]+'、音も'+VLN[pw]+'。音が出ている物はふるえている｜シミュラボ'); } }
  function vis(){ const k=mode==='kagami', m=mode==='mushi', o=mode==='oto';
    showF('n',k); showF('dd',m); showF('paper',m); showF('ins',o); showF('pw',o);
    ['aim','scr'].forEach(id=>show(id,k)); ['newp','foc'].forEach(id=>show(id,m)); ['hitB','damp','snd'].forEach(id=>show(id,o)); show('pinch',o&&ins==='ito');
    $('hitB').textContent=INS[ins].bt; $('snd').textContent=soundOn?'🔈 音を出す：ON':'🔇 音を出す：OFF'; $('pinch').textContent=pinch?'🤏 糸をはなす':'🤏 糸をつまむ';
    const lb=$('pw').closest('.field'); if(lb) lb.querySelector('label').textContent=INS[ins].lab; }
  function draw(){ ctx.fillStyle=C.bg; ctx.fillRect(0,0,W,H); if(mode==='kagami'){ drawKagami(); drawKagamiInfo(); } else if(mode==='mushi'){ drawMushi(); drawMushiInfo(); } else { drawOto(); drawOtoInfo(); drawWave(); } }
  function setDD(v){ dd=clamp(Math.round(v*10)/10,2,25); $('dd').value=dd; $('ddL').textContent=dd.toFixed(1)+' cm'; }

  // ===== 操作 =====
  ['mode','paper','ins'].forEach(id=>{ if(!Q.has(id)) return; const e=$(id), q=Q.get(id); if([].some.call(e.options,o=>o.value===q)) e.value=q; });
  mode=$('mode').value; paper=$('paper').value; ins=$('ins').value;
  if(Q.has('n')){ nM=clamp(Math.round(+Q.get('n')||3),1,3); $('n').value=nM; $('nL').textContent=nM+' まい'; }
  if(Q.has('pw')){ pw=clamp(Math.round(+Q.get('pw')||3),1,5); $('pw').value=pw; $('pwL').textContent=String(pw); }
  setDD(Q.has('d')?+Q.get('d'):dd);
  aim(0,WX,TY); aim(1,WX,TY); aim(2,WX,118);
  if(Q.get('aim')==='all') [0,1,2].forEach(i=>aim(i,WX,TY));
  hit={ins:ins,pw:pw,t0:-10,damp:null}; prev=ins==='ito'?null:{ins:ins,pw:1,t0:-20,damp:null};
  if(Q.get('pinch')==='1') pinch=true;
  if(Q.has('hitt')){ hit={ins:ins,pw:pw,t0:-(+Q.get('hitt')||0.3),damp:null}; }
  tShow=T0+DT*nHit();
  $('mode').addEventListener('change',()=>{ mode=$('mode').value; stopSound(); vis(); lastKey=''; stats(); });
  $('n').addEventListener('input',()=>{ nM=+$('n').value; $('nL').textContent=nM+' まい'; if(sel>=nM) sel=nM-1; stats(); });
  $('dd').addEventListener('input',()=>{ setDD(+$('dd').value); stats(); });
  $('paper').addEventListener('change',()=>{ paper=$('paper').value; burnt=null; burn=0; smoke=[]; lastKey=''; stats(); });
  $('ins').addEventListener('change',()=>{ ins=$('ins').value; stopSound(); hit={ins:ins,pw:pw,t0:-10,damp:null}; prev=null; pinch=false; vis(); lastKey=''; stats(); });
  $('pw').addEventListener('input',()=>{ pw=+$('pw').value; $('pwL').textContent=String(pw); stats(); });
  $('aim').addEventListener('click',()=>{ for(let i=0;i<3;i++) aim(i,WX,TY); stats(); });
  $('scr').addEventListener('click',()=>{ const ys=[120,300,170]; for(let i=0;i<3;i++) aim(i,WX,ys[i]+rnd(-20,20)); stats(); });
  $('newp').addEventListener('click',()=>{ burnt=null; burn=0; smoke=[]; lastKey=''; stats(); });
  $('foc').addEventListener('click',()=>{ setDD(F); stats(); });
  $('hitB').addEventListener('click',strike);
  $('damp').addEventListener('click',damp);
  $('snd').addEventListener('click',()=>{ soundOn=!soundOn; if(soundOn) getAC(); else stopSound(); vis(); });
  $('pinch').addEventListener('click',()=>{ pinch=!pinch; vis(); lastKey=''; stats(); });
  cv.addEventListener('pointerdown',e=>{ const p=cpos(cv,e), x=p[0]/dpr, y=p[1]/dpr;
    if(mode==='kagami'){ if(x>446) return; let bi=-1, bd=48; for(let i=0;i<nM;i++){ const d=Math.hypot(mir[i].x-x,mir[i].y-y); if(d<bd){ bd=d; bi=i; } }
      if(bi>=0){ sel=bi; mdrag=true; try{ cv.setPointerCapture(e.pointerId); }catch(err){} } else { aim(sel,x,y); stats(); } return; }
    if(mode==='mushi'){ const LY=PY-dd*PXc; if(x<402&&Math.abs(y-LY)<34&&x>LXc-70){ ldrag=true; try{ cv.setPointerCapture(e.pointerId); }catch(err){} } return; }
    if(x<392&&y<292){ if(ins==='ito'&&Math.abs(y-150)<26&&x>110&&x<290){ pinch=!pinch; vis(); lastKey=''; stats(); } else strike(); } });
  cv.addEventListener('pointermove',e=>{ const p=cpos(cv,e), x=p[0]/dpr, y=p[1]/dpr;
    if(mdrag){ const m=mir[sel]; if(Math.hypot(x-m.x,y-m.y)>36){ aim(sel,x,y); stats(); } }
    if(ldrag){ setDD((PY-y)/PXc); stats(); } });
  const up=()=>{ mdrag=false; ldrag=false; };
  cv.addEventListener('pointerup',up); cv.addEventListener('pointercancel',up);
  function frame(t){ const dt=last?Math.min(0.05,(t-last)/1000):0; last=t; tNow+=dt;
    if(mode==='kagami'){ const tg=T0+DT*nHit(); tShow+=(tg-tShow)*(1-Math.exp(-dt*1.6)); }
    if(mode==='mushi'){ const c=conc(dd), th=CTH[paper];
      if(c>=th){ burn+=dt*0.5*Math.sqrt(c/th); if(burn>=1&&!burnt){ burnt=Math.max(4,spot(dd)*PXc); lastKey=''; stats(); } if(Math.random()<dt*12) smoke.push({x:LXc+rnd(-3,3),y:PY-4,a:0}); }
      else burn=Math.max(0,burn-dt*0.4);
      smoke.forEach(p=>{ p.a+=dt; p.y-=dt*34; p.x+=Math.sin(p.a*3)*0.4; }); smoke=smoke.filter(p=>p.a<2.2); }
    if(mode==='oto'){ if(ins==='drum'){ const A=amp(hit,el()); beads.forEach(b=>{ if(b.vy!==0||b.y<0){ b.vy+=900*dt; b.y+=b.vy*dt; if(b.y>=0){ b.y=0; b.vy=A>0.5?-(30+A*36)*rnd(0.7,1.1):0; } } }); }
      stats(); }
    draw(); requestAnimationFrame(frame); }
  vis(); stats(); draw(); requestAnimationFrame(frame);
'''

HIKARI_ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
<p><b>日光はまっすぐ進み</b>、かがみではね返すと向きが変わります。はね返した日光を日かげのまとに当てると、まとは<b>明るく、あたたかく</b>なり、かがみの数をふやして光を重ねるほど、もっと明るく、あたたかくなります。虫めがねを使うと<b>日光を集める</b>ことができ、明るい部分を小さくするほど明るく、あつくなって、黒い紙がこげることもあります。音が出ている物は<b>ふるえて</b>いて、強くたたくとふるえが大きく、音も大きくなります。ふるえを止めると音も止まり、糸電話の糸をつまむと音がつたわらなくなります。</p>
''' + N('<b>対応する単元</b>：小学3年 A（3）光と音の性質「（ア）日光は直進し，集めたり反射させたりできること」「（イ）物に日光を当てると，物の明るさや暖かさが変わること」「（ウ）物から音が出たり伝わったりするとき，物は震えていること。また，音の大きさが変わるとき物の震え方が変わること」。学習指導要領解説では、何枚かの平面鏡で光を重ねて明るさや暖かさを比べること、虫眼鏡で光を集めたところを小さくすると明るさや暖かさが増し黒い紙などが焦げることがあること、音の大きさと震え方の関係を打楽器などで調べること、糸電話などで音の伝わりを捉えることが示されています。また、直接目で太陽を見ない・反射させた日光を人の顔に当てない・集めた日光を衣服や生物に当てないといった安全への配慮が示されています。') + '''
<h2>授業での使い方</h2>
<h3>導入：くもりの日・雨の日でも「日光」の学習を進める</h3>
<p>光の単元は天気に左右されます。くもりや雨で外に出られない日は、「① かがみで日光をはね返す」で、かがみを指でつかんで光の道すじを動かし、日光がまっすぐ進むことや、はね返すと向きが変わることを確かめます。晴れた日の実験の前に見せておくと、「どこに当てればいいか」「人の顔に当ててはいけない」といった約束を全員で確認できます。</p>
<h3>展開：光を重ねる・集める</h3>
<p>かがみの数を1まい・2まい・3まいとふやし、「🎯 全部まとにねらう」で光を重ねると、まとの温度のめやすが上がっていきます。右の表と、実際に放射温度計などではかった結果をくらべて、表にまとめる活動につなげます。「② 虫めがねで日光を集める」では、虫めがねを指で上下に動かし、明るい部分の大きさと明るさ・あたたかさの関係を調べます。黒い紙と白い紙をくらべることもできます。</p>
<h3>まとめ：音のふるえ（③ 音のふるえ）</h3>
<p>トライアングル・たいこ・わゴムを、強さを変えてたたいたり、はじいたりして、ふるえのグラフの「たてのはば」をくらべます。前にたたいたときのグラフが灰色で残るので、強さのちがいが一目でわかります。「✋ 手でおさえる」でふるえを止めると、音も止まります。糸電話では、糸をつまむと聞く人のコップがふるえなくなり、聞こえなくなることを確かめます。音は「🔇 音を出す」をONにしたときだけ、ボタンを押すと小さく鳴ります（数秒で自動で止まります）。</p>
<h3>児童への問いの例</h3>
<ol>
<li>かがみを2まい、3まいと使って光を重ねると、まとの明るさとあたたかさはどうなるでしょう？</li>
<li>虫めがねで集めた日光の、明るい部分を小さくすると、明るさとあたたかさはどうなるでしょう？　なぜ、人や服に当ててはいけないのでしょう？</li>
<li>たいこを強くたたいたときと、よわくたたいたときで、まくの上のビーズのはね方はどうちがうでしょう？　音の大きさとふるえには、どんな関係がありますか？</li>
</ol>
<h2>しくみ・解説</h2>
<h3>言葉の意味（1文で）</h3>
<ul>
<li><b>日光はまっすぐ進む</b>とは、太陽の光が、何かに当たるまでは曲がらずに、まっすぐな道すじで進むということです。</li>
<li><b>光をはね返す</b>とは、かがみなどに当たった日光が、向きを変えて進むことで、かがみの向きを変えると、はね返った光の行き先も変わります。</li>
<li><b>光を集める</b>とは、虫めがねを使って、日光を小さな部分に集めることで、明るい部分が小さいほど明るく、あつくなります。</li>
<li><b>音のふるえ</b>とは、音が出ている物が、細かく速く行ったり来たりしている動きのことで、ふるえが大きいほど音は大きくなります。</li>
</ul>
<h3>かがみのまい数と、まとの明るさ・温度の早見表（めやす）</h3>
''' + T([["0まい（日かげのまま）", "いちばん暗い", "約18℃"], ["1まい", "明るい", "約23℃"], ["2まい（光を重ねる）", "もっと明るい", "約28℃"], ["3まい（光を重ねる）", "とても明るい", "約33℃"]],
         ["まとに当てた光", "明るさ", "温度（3分後のめやす）"]) + '''
<p>このシミュレーターの温度は、日かげのかべにはったまと（18℃）に、はね返した日光を3分くらい当てたときの<b>めやす</b>として、光1まい分で約5℃上がるようにしています。実際の温度は、季節・時こく・天気・まとの色によって大きくかわるので、実験ではかった値を表にまとめてください。大切なのは「光を重ねるほど、明るく、あたたかくなる」という関係です。</p>
<h3>虫めがねの早見表（直径6 cm・光が集まるきょり15 cmの虫めがね）</h3>
''' + T([["2 cm", "約5.2 cm", "約1.2倍", "日なたと同じくらい"], ["7 cm", "約3.3 cm", "約3.0倍", "あたたかい"], ["10 cm", "約2.1 cm", "約7.4倍", "とても あつい"],
          ["13 cm", "約9.2 mm", "約38倍", "黒い紙はこげる"], ["15 cm", "約1.4 mm", "約1,700倍", "黒い紙も白い紙もこげる"], ["20 cm", "約2.2 cm", "約6.8倍", "とても あつい"]],
         ["紙とのきょり", "明るい部分の直径", "明るさ（日光の何倍）", "黒い紙のようす（めやす）"]) + '''
<p>明るい部分の大きさが半分になると、面積は4分の1になるので、同じ量の日光が4倍こく集まります。だから、明るい部分を小さくするほど、明るく、あつくなります。</p>
<h3>音の大きさとふるえの関係</h3>
''' + T([["よわくたたく（はじく）", "小さい", "小さい"], ["強くたたく（はじく）", "大きい", "大きい"], ["手でおさえて止める", "止まる", "止まる（聞こえない）"], ["糸電話の糸をつまむ", "つまんだ所から先はふるえない", "聞く人には聞こえない"]],
         ["すること", "ふるえ（ふれはば）", "音"]) + '''
<h3>先生向けの補足</h3>
''' + N('・虫めがねの計算：明るい部分の直径 ≒ レンズの直径 D ×｜f − d｜÷ f ＋ d × 0.0093（f＝焦点距離、d＝レンズと紙の距離、0.0093 rad ≒ 太陽の見かけの直径0.53°）。明るさ（日光の何倍か）≒ 0.9 ×（D ÷ 明るい部分の直径）²（0.9 はレンズの透過率のめやす）。D＝6 cm、f＝15 cm のとき、d＝f で直径約1.4 mm、約1,700倍になります。<br>・「こげる」の判定は、黒い紙で日光の約30倍以上、白い紙で約200倍以上をめやすとしています（白い紙は光の多くをはね返すため）。実際には紙の種類や当てる時間で変わります。<br>・音のグラフは、音の大きさ（ふれはば）の関係を見せるため、ふるえの速さ（振動数）を1秒間に数回まで遅くしてあります。実際のトライアングルは1秒間に千回以上ふるえています。振動数と音の高さは中学1年「音の性質」で扱います。') + '''
<h3>このシミュレーションで単純化していること</h3>
<ul>
<li>はね返した光の道すじは、見やすいように黄色の帯でかいています。実際の空気中では、光の道すじはほとんど見えず、当たった所が明るく見えます。</li>
<li>かがみはどれも同じ大きさで、日光は左上から同じ向きに来るものとしています。かがみの数は3まいまでです。</li>
<li>温度は「めやす」です。まとが日光を受けてあたたまるまでの時間や、風・まとの色のちがいは考えていません。</li>
<li>ふるえの大きさは、たたく強さに比例するとしています。音の大きさは「小さい〜大きい」の5だんかいで表しています。</li>
</ul>
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「小学校学習指導要領（平成29年告示）解説 理科編」第3学年 A（3）光と音の性質（''' + A(MEXT_SHO, "小学校学習指導要領・解説") + '''）</li>
<li>小学校理科の教科書（第3学年「光のせいしつ」「音のせいしつ」の単元）</li>
<li>国立天文台 編『理科年表』（太陽の視直径 約32′＝約0.53°）</li>
</ul>
'''

sim(slug="hikari-oto", cat="rika", emoji="🪞", score=80,
    title="光と音のせいしつシミュレーター（かがみ・虫めがね・音のふるえ）",
    title_tag="光と音の性質シミュレーター｜かがみで日光をはね返す・虫めがねで集める・音のふるえ（小3理科）",
    meta_desc="かがみの向きを指で変えて日光をはね返し、光を重ねるとまとが明るく・あたたかくなることを確かめる小3理科「光と音の性質」の無料シミュレーター。虫めがねで日光を集める（黒い紙がこげる）、トライアングル・たいこ・わゴムの音とふるえの大きさ、糸電話もグラフで比べられます。",
    og_title="光と音のせいしつシミュレーター（かがみ・虫めがね・音のふるえ）",
    og_desc="かがみで日光をはね返し、光を重ねると明るく・あたたかく。虫めがねで集めた光、音の大きさとふるえ、糸電話。小3理科をくもりの日でも。",
    card_desc="かがみで日光をはね返して重ねる、虫めがねで集める、音の大きさとふるえ。くもりの日でも小3の光と音。",
    lead="かがみを指でつかんで、日光をかべのまとに当ててみましょう。光を重ねるほど、まとは明るく、あたたかくなります。虫めがねで日光を集めたり、トライアングル・たいこ・わゴム・糸電話で、音の大きさとふるえのようすをくらべたりできます。",
    model="小3 光と音の性質",
    level="小学3年",
    unit="小学校 第3学年 A（3）光と音の性質",
    canvas=canvas(640, 440, light=True),
    controls=select("mode", "実けん", [("kagami", "① かがみではね返す"), ("mushi", "② 虫めがねで集める"), ("oto", "③ 音のふるえ")])
           + slider("n", "かがみの数", 1, 3, 3, 1, "{v} まい")
           + slider("dd", "虫めがねと紙のきょり", 2, 25, 7, 0.5, "{v} cm")
           + select("paper", "紙の色", [("black", "黒い紙"), ("white", "白い紙")])
           + select("ins", "音を出す物", [("tri", "トライアングル"), ("drum", "たいこ"), ("gomu", "わゴム"), ("ito", "糸電話")])
           + slider("pw", "たたく強さ", 1, 5, 3, 1),
    buttons=btn("aim", "🎯 全部まとにねらう", True) + btn("scr", "🔀 向きをばらばらに")
           + btn("foc", "🔍 明るい部分をいちばん小さく", True) + btn("newp", "📄 紙をとりかえる")
           + btn("hitB", "🔔 たたく", True) + btn("damp", "✋ 手でおさえる") + btn("snd", "🔇 音を出す：OFF") + btn("pinch", "🤏 糸をつまむ"),
    stats=stats([("sA", "かがみの数", False), ("sB", "まとの明るさ", True), ("sC", "まとの温度（めやす）", False), ("sD", "日光の進み方", False)]),
    legend="①：かがみ（①②③）を指でつかんで動かすと、はね返った光がその方向へ進みます。空をタップすると、えらんだかがみの光がそこへ向きます。黄色の帯は光の道すじ（見やすくするための表示）。②：虫めがねを指で上下に動かすと、紙までのきょりが変わります。右は上から見た紙。③：絵をタップするか「たたく」ボタンで音を出します。下のグラフのたてのはばが、ふるえの大きさです（灰色は前にたたいたとき）。音は「音を出す」をONにしたときだけ、小さく鳴ります。",
    article=HIKARI_ARTICLE,
    faqs=[("かがみではね返した日光は、どのように進みますか？", "まっすぐ進みます。かがみの向きを変えると、はね返った日光の進む向きも変わります。日光がまっすぐ進むので、かべに当たった所だけが明るくなります。"),
          ("かがみの数をふやして光を重ねると、どうなりますか？", "光を重ねるほど、当たった所は明るく、あたたかくなります。1まいより2まい、2まいより3まいの方が、明るく、温度も高くなります。"),
          ("虫めがねで日光を集めると、どうなりますか？", "明るい部分を小さくするほど、明るく、あつくなります。黒い紙に当てると、こげてけむりが出ることがあります。虫めがねで太陽を見たり、集めた光を人や服・生き物に当てたりしてはいけません。"),
          ("黒い紙と白い紙では、どちらがこげやすいですか？", "黒い紙の方がこげやすいです。黒い紙は光を多く吸ってあたたまり、白い紙は光の多くをはね返すからです。"),
          ("音が出ているとき、物はどうなっていますか？", "物はふるえています。強くたたくとふるえが大きくなり、音も大きくなります。ふるえを手でおさえて止めると、音も止まります。"),
          ("糸電話の糸をつまむと、なぜ聞こえなくなるのですか？", "糸電話は、話した声でコップがふるえ、そのふるえが糸をつたわって、聞く人のコップをふるわせることで音がつたわります。糸をつまむと、そこでふるえが止まってしまうので、聞こえなくなります。")],
    rel=[("hikari-kussetsu", "🔦", "光の反射と屈折"), ("totsu-lens", "🔍", "凸レンズの像"), ("taiyou-ugoki", "🌞", "太陽の動き"),
         ("unari-teijouha", "🎵", "うなり"), ("denki-toorimichi", "💡", "電気の通り道")],
    js=JS_HIKARI)
