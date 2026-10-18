# -*- coding: utf-8 -*-
"""理科の授業向けシミュ（酸・アルカリと中和／とじこめた空気と水）
   chuwa-ion  … 中3「化学変化とイオン」（第1分野（6）ア（ア）㋑酸・アルカリ ㋒中和と塩）／小6「水溶液の性質」（A（2））
   kuuki-mizu … 小4「空気と水の性質」（A（1））"""
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

MEXT_SHO = "https://www.mext.go.jp/a_menu/shotou/new-cs/1387014.htm"
MEXT_CHU = "https://www.mext.go.jp/a_menu/shotou/new-cs/1387016.htm"
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
  function arrow(x1,y1,x2,y2,col,w,s){ const dx=x2-x1, dy=y2-y1, l=Math.hypot(dx,dy); if(l<2) return; const ux=dx/l, uy=dy/l; ctx.strokeStyle=col; ctx.lineWidth=w; ctx.lineCap='round'; ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2-ux*s*1.3,y2-uy*s*1.3); ctx.stroke(); ctx.lineCap='butt';
    ctx.fillStyle=col; ctx.beginPath(); ctx.moveTo(x2,y2); ctx.lineTo(x2-ux*s*1.7-uy*s,y2-uy*s*1.7+ux*s); ctx.lineTo(x2-ux*s*1.7+uy*s,y2-uy*s*1.7-ux*s); ctx.closePath(); ctx.fill(); }
  function mix(a,b,t){ const p=h=>[1,3,5].map(i=>parseInt(h.substr(i,2),16)), A=p(a), B=p(b); return 'rgb('+A.map((x,i)=>Math.round(x+(B[i]-x)*clamp(t,0,1))).join(',')+')'; }
  function dot(x,y,r,fill,stroke){ ctx.fillStyle=fill; ctx.beginPath(); ctx.arc(x,y,r,0,6.2832); ctx.fill(); if(stroke){ ctx.strokeStyle=stroke; ctx.lineWidth=1; ctx.stroke(); } }
  const K=id=>$(id).previousElementSibling;
  function sh(id,m,sub){ const e=$(id); if(e) e.innerHTML=m+(sub?'<span style="display:block;font-size:12px;font-weight:700;color:#59616c;margin-top:2px">'+sub+'</span>':''); }
  function show(id,on){ const e=$(id); if(e) e.style.display=on?'':'none'; }
  function showF(id,on){ const e=$(id), f=e?e.closest('.field'):null; if(f) f.style.display=on?'':'none'; }
  const Q=new URLSearchParams(location.search);
'''

# ============================================================ 1 酸・アルカリと中和
JS_CHUWA = HELP + r'''
  const C={bg:'#f8fafc',ink:'#0f172a',sub:'#64748b',grid:'#e2e8f0'};
  // モデル：塩酸10 cm³ の中に H⁺・Cl⁻ が各10こ。同じ濃さの水酸化ナトリウム水溶液 1 cm³ に Na⁺・OH⁻ が各1こ（濃さ2倍なら各2こ）
  // pH（参考）は 塩酸 0.1 mol/L、水酸化ナトリウム水溶液 0.1 mol/L（2倍は 0.2 mol/L）として計算
  const N0=10, CM=0.1, BX0=30, BX1=228, BY1=408, PCM=8.4, PIPX=202, RIM=150;
  const ION={H:{lb:'H⁺',col:'#dc2626',r:9.5,nm:'水素イオン'},Cl:{lb:'Cl⁻',col:'#16a34a',r:10.5,nm:'塩化物イオン'},Na:{lb:'Na⁺',col:'#7c3aed',r:10.5,nm:'ナトリウムイオン'},OH:{lb:'OH⁻',col:'#2563eb',r:10.5,nm:'水酸化物イオン'}};
  const ORD=['H','Cl','Na','OH'], STY={H:[[],3.2],Cl:[[7,4],3],Na:[[],3],OH:[[7,4],3]};
  const SOL=[{n:['塩酸'],k:'a',ph:'約1',st:'気体',ev:0},{n:['炭酸水'],k:'a',ph:'約4〜5',st:'気体',ev:0,bub:1},{n:['食塩水'],k:'n',ph:'7',st:'固体',ev:1},
             {n:['石灰水'],k:'b',ph:'約12',st:'固体',ev:1},{n:['アンモニア水'],k:'b',ph:'約11',st:'気体',ev:0},{n:['水酸化ナトリウム','水溶液'],k:'b',ph:'約13',st:'固体',ev:1}];
  const SNAME=['塩酸','炭酸水','食塩水','石灰水','アンモニア水','水酸化ナトリウム水溶液'];
  let v=0, k=1, indV='btb', parts=[], drops=[], autoOn=false, autoT=0, last=0, tNow=0;
  const done={lit:[0,0,0,0,0,0],btb:[0,0,0,0,0,0],evap:[0,0,0,0,0,0]};
  const vmax=()=>k===1?20:10, vn=()=>N0/k, chu=()=>$('mode').value==='chu', ind=()=>indV;
  function cnt(vv){ const a=k*vv; return {H:Math.max(0,N0-a),Cl:N0,Na:a,OH:Math.max(0,a-N0),W:Math.min(N0,a)}; }
  function pH(vv){ const d=(CM*N0-k*CM*vv)/(N0+vv), h=(d+Math.sqrt(d*d+4e-14))/2; return -Math.log10(h); }
  function topY(vv){ return BY1-(N0+vv)*PCM; }
  function btbCol(p){ if(p<=6.0) return '#facc15'; if(p<6.8) return mix('#facc15','#22c55e',(p-6.0)/0.8); if(p<=7.2) return '#22c55e'; if(p<7.6) return mix('#22c55e','#3b82f6',(p-7.2)/0.4); return '#3b82f6'; }
  function btbName(p){ return p<6.5?'黄色':(p<=7.4?'緑色':'青色'); }
  function ppCol(p){ return p<8.2?null:mix('#f9a8d4','#db2777',(p-8.2)/1.8); }
  function ppName(p){ return p<8.2?'無色':'赤色'; }
  function natOf(c){ return c.H>0?'酸性':(c.OH>0?'アルカリ性':'中性'); }
  function natCol(n){ return n==='酸性'?'#dc2626':(n==='中性'?'#15803d':'#2563eb'); }

  // ---------- イオンのモデル ----------
  const rad=t=>t==='W'?8.5:ION[t].r;
  function mk(t,x,y){ return {t:t,x:x,y:y,vx:rnd(-12,12),vy:rnd(-12,12),mate:null,a:rnd(0,6.28)}; }
  function freeSpot(r,yT){ for(let i=0;i<80;i++){ const x=rnd(BX0+r+2,BX1-r-2), y=rnd(yT+r+2,BY1-r-2); if(parts.every(p=>Math.hypot(p.x-x,p.y-y)>rad(p.t)+r+2)) return [x,y]; } return [rnd(BX0+r,BX1-r),rnd(yT+r,BY1-r)]; }
  function rebuild(){ parts=[]; drops=[]; const c=cnt(v), yT=topY(v); ['Cl','Na','H','OH','W'].forEach(t=>{ for(let i=0;i<c[t];i++){ const s=freeSpot(rad(t),yT); parts.push(mk(t,s[0],s[1])); } }); }
  function land(){ const yT=topY(v); for(let i=0;i<k;i++){ parts.push(mk('Na',PIPX+rnd(-16,10),yT+rnd(12,22))); const o=mk('OH',PIPX+rnd(-16,10),yT+rnd(12,22)); o.vy=30; parts.push(o);
      const fr=parts.filter(p=>p.t==='H'&&!p.mate); if(fr.length){ let b=fr[0], bd=1e9; fr.forEach(h=>{ const d=Math.hypot(h.x-o.x,h.y-o.y); if(d<bd){ bd=d; b=h; } }); b.mate=o; o.mate=b; } } }
  function step(dt){ if(dt<=0) return; const yT=topY(v);
    drops.forEach(d=>{ d.y+=dt*240; }); while(drops.length&&drops[0].y>=yT){ drops.shift(); land(); }
    parts.forEach(p=>{ if(p.mate){ const m=p.mate, dx=m.x-p.x, dy=m.y-p.y, d=Math.hypot(dx,dy)||1; p.vx=dx/d*75; p.vy=dy/d*75; }
      else { p.vx+=randn()*70*dt; p.vy+=randn()*70*dt; p.vx*=0.97; p.vy*=0.97; const s=Math.hypot(p.vx,p.vy); if(s>22){ p.vx*=22/s; p.vy*=22/s; } }
      if(p.t==='W') p.a+=dt*0.8;
      p.x+=p.vx*dt; p.y+=p.vy*dt; const r=rad(p.t);
      if(p.x<BX0+r){ p.x=BX0+r; p.vx=Math.abs(p.vx); } if(p.x>BX1-r){ p.x=BX1-r; p.vx=-Math.abs(p.vx); }
      if(p.y<yT+r){ p.y=yT+r; p.vy=Math.abs(p.vy); } if(p.y>BY1-r){ p.y=BY1-r; p.vy=-Math.abs(p.vy); } });
    const dead=new Set(), born=[];
    parts.forEach(p=>{ if(p.t==='OH'&&p.mate&&!dead.has(p)){ const m=p.mate; if(Math.hypot(m.x-p.x,m.y-p.y)<13){ dead.add(p); dead.add(m); born.push(mk('W',(p.x+m.x)/2,(p.y+m.y)/2)); } } });
    if(dead.size) parts=parts.filter(p=>!dead.has(p)).concat(born);
    for(let i=0;i<parts.length;i++){ const a=parts[i]; for(let j=i+1;j<parts.length;j++){ const b=parts[j]; if(a.mate===b) continue;
      const dx=b.x-a.x, dy=b.y-a.y, d=Math.hypot(dx,dy), mm=rad(a.t)+rad(b.t)+1; if(d>0&&d<mm){ const o=(mm-d)/2, nx=dx/d, ny=dy/d; a.x-=nx*o; a.y-=ny*o; b.x+=nx*o; b.y+=ny*o; } } } }
  function drawIon(p){ if(p.t==='W'){ const c=Math.cos(p.a), s=Math.sin(p.a);
      [[-0.85,0.6],[0.85,0.6]].forEach(h=>dot(p.x+(h[0]*c-h[1]*s)*7,p.y+(h[0]*s+h[1]*c)*7,3.6,'#f8fafc','#0369a1')); dot(p.x,p.y,6.2,'#7dd3fc','#0369a1'); return; }
    const I=ION[p.t]; dot(p.x,p.y,I.r,I.col,'rgba(15,23,42,.35)'); tx(I.lb,p.x,p.y+3.5,9.5,'#fff','center',true); }

  // ---------- ① 中和（中3） ----------
  function drawBeaker(){ const c=cnt(v), p=pH(v), yT=topY(v);
    panel(8,8,250,424); tx('ビーカーの中（イオンのモデル）',18,28,13,C.ink,'left',true); tx('ピペット：水酸化ナトリウム水溶液',18,45,10.5,C.sub,'left',true);
    [['H',c.H],['Cl',c.Cl],['Na',c.Na],['OH',c.OH]].forEach((r,i)=>{ const y=63+i*17, I=ION[r[0]]; dot(25,y-4,6.5,I.col); tx(I.lb,37,y,12.5,I.col,'left',true); tx(r[1]+'こ',112,y,12.5,C.ink,'right',true); });
    drawIon({t:'W',x:25,y:63+4*17-5,a:0}); tx('水',37,63+4*17,12.5,'#0369a1','left',true); tx(c.W+'こ',112,63+4*17,12.5,C.ink,'right',true);
    tx('液の体積',124,104,10.5,C.sub,'left',true); tx((N0+v)+' cm³',124,121,13,C.ink,'left',true);
    // 液
    let lc, la; if(ind()==='btb'){ lc=btbCol(p); la=0.42; } else { const q=ppCol(p); lc=q||'#e2e8f0'; la=q?0.45:0.45; }
    ctx.save(); ctx.globalAlpha=la; ctx.fillStyle=lc; ctx.fillRect(BX0,yT,BX1-BX0,BY1-yT); ctx.restore();
    ctx.strokeStyle='rgba(15,23,42,.22)'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.moveTo(BX0,yT); ctx.lineTo(BX1,yT); ctx.stroke();
    // 目もり
    for(let ml=10; ml<=30; ml+=5){ const y=BY1-ml*PCM; ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(BX0,y); ctx.lineTo(BX0+(ml%10?6:11),y); ctx.stroke(); if(ml%10===0) tx(String(ml),BX0+14,y+4,9.5,'#94a3b8','left',true); }
    parts.filter(q=>q.t==='W').forEach(drawIon); parts.filter(q=>q.t!=='W').forEach(drawIon);
    // ガラス
    ctx.strokeStyle='#64748b'; ctx.lineWidth=2.5; ctx.beginPath(); ctx.moveTo(BX0-8,RIM-3); ctx.quadraticCurveTo(BX0-2,RIM-2,BX0-2,RIM+6); ctx.lineTo(BX0-2,BY1-4); ctx.quadraticCurveTo(BX0-2,BY1+2,BX0+6,BY1+2);
    ctx.lineTo(BX1-6,BY1+2); ctx.quadraticCurveTo(BX1+2,BY1+2,BX1+2,BY1-4); ctx.lineTo(BX1+2,RIM); ctx.stroke();
    // こまごめピペット
    const px=PIPX; ctx.fillStyle='rgba(226,232,240,.75)'; ctx.strokeStyle='#64748b'; ctx.lineWidth=1.4; ctx.beginPath(); ctx.moveTo(px-6,84); ctx.lineTo(px-6,124); ctx.lineTo(px-1.6,140); ctx.lineTo(px+1.6,140); ctx.lineTo(px+6,124); ctx.lineTo(px+6,84); ctx.closePath(); ctx.fill(); ctx.stroke();
    ctx.fillStyle='#b91c1c'; rr(px-11,54,22,34,10); ctx.fill();
    drops.forEach(d=>dot(px,d.y,3.6,'rgba(148,163,184,.95)'));
    const n=vn(); tx(v<n?'中性まで あと '+(n-v)+' cm³':(v===n?'ちょうど中性になった':'中性より '+(v-n)+' cm³ 多い'),(BX0+BX1)/2,427,11.5,natCol(natOf(c)),'center',true); }
  function drawGraph(){ const x=266, y=8, w=366, h=254; panel(x,y,w,h);
    tx('加えた水酸化ナトリウム水溶液とイオンの数',x+10,y+21,12.5,C.ink,'left',true);
    const X0=x+36, X1=x+w-14, Y0=y+h-34, Y1=y+44, XM=20, YM=20, gx=a=>X0+(X1-X0)*a/XM, gy=b=>Y0-2-(Y0-2-Y1)*b/YM;
    ctx.strokeStyle=C.grid; ctx.lineWidth=1; for(let b=5;b<=YM;b+=5){ ctx.beginPath(); ctx.moveTo(X0,gy(b)); ctx.lineTo(X1,gy(b)); ctx.stroke(); }
    for(let a=2;a<=XM;a+=2){ ctx.beginPath(); ctx.moveTo(gx(a),Y0); ctx.lineTo(gx(a),Y1); ctx.stroke(); }
    for(let b=0;b<=YM;b+=5) tx(String(b),X0-6,gy(b)+4,10.5,C.sub,'right');
    for(let a=0;a<=XM;a+=2) tx(String(a),gx(a),Y0+14,10.5,C.sub,'center');
    ctx.strokeStyle=C.ink; ctx.lineWidth=1.3; ctx.beginPath(); ctx.moveTo(X0,Y1-4); ctx.lineTo(X0,Y0); ctx.lineTo(X1,Y0); ctx.stroke();
    tx('イオンの数［こ］',x+10,y+37,10.5,C.sub,'left',true); tx('加えた水酸化ナトリウム水溶液［cm³］',X1,Y0+29,10.5,C.sub,'right',true);
    const n=vn();
    if(v>=n){ ctx.setLineDash([5,4]); ctx.strokeStyle='#15803d'; ctx.lineWidth=1.4; ctx.beginPath(); ctx.moveTo(gx(n),Y0); ctx.lineTo(gx(n),Y1); ctx.stroke(); ctx.setLineDash([]); tag('中性',gx(n),Y1+10,10.5,'#15803d','center'); }
    const xs=[0]; if(n>0&&n<v) xs.push(n); if(v>0) xs.push(v);
    ORD.forEach(t=>{ const I=ION[t]; ctx.strokeStyle=I.col; ctx.lineWidth=STY[t][1]; ctx.setLineDash(STY[t][0]); ctx.beginPath(); xs.forEach((a,i)=>{ const b=cnt(a)[t]; if(i) ctx.lineTo(gx(a),gy(b)); else ctx.moveTo(gx(a),gy(b)); }); ctx.stroke(); ctx.setLineDash([]); });
    ORD.forEach(t=>{ ctx.fillStyle='#fff'; ctx.strokeStyle=ION[t].col; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(gx(v),gy(cnt(v)[t]),4,0,7); ctx.fill(); ctx.stroke(); });
    const lx=k===1?X0+10:X0+(X1-X0)*0.5, ly=Y1+16;
    ORD.forEach((t,i)=>{ const I=ION[t], yy=ly+i*15; ctx.strokeStyle=I.col; ctx.lineWidth=3; ctx.setLineDash(STY[t][0]); ctx.beginPath(); ctx.moveTo(lx,yy-4); ctx.lineTo(lx+22,yy-4); ctx.stroke(); ctx.setLineDash([]); tx(I.lb+' '+I.nm,lx+28,yy,11,I.col,'left',true); }); }
  function drawInfo(){ const x=266, y=270, w=366, h=162, c=cnt(v), p=pH(v), nat=natOf(c), nc=natCol(nat); panel(x,y,w,h);
    tx('いまの液は',x+12,y+28,12.5,C.sub,'left',true); tx(nat,x+82,y+30,22,nc,'left',true);
    const ps='pH '+p.toFixed(1), pw=tw(ps,18,true); tx(ps,x+w-14,y+30,18,C.ink,'right',true); tx('（参考）',x+w-18-pw,y+30,10.5,C.sub,'right',true);
    const b0=x+14, b1=x+w-14, by=y+45, g=ctx.createLinearGradient(b0,0,b1,0);
    [[0,'#dc2626'],[0.2,'#f97316'],[0.38,'#facc15'],[0.5,'#22c55e'],[0.64,'#0ea5e9'],[0.82,'#2563eb'],[1,'#6d28d9']].forEach(s=>g.addColorStop(s[0],s[1])); ctx.fillStyle=g; rr(b0,by,b1-b0,11,5.5); ctx.fill();
    [[0,'0'],[7,'7'],[14,'14']].forEach(q=>tx(q[1],b0+(b1-b0)*q[0]/14,by+25,10.5,C.sub,q[0]===0?'left':(q[0]===14?'right':'center'),true));
    tx('← 酸性が強い',b0+(b1-b0)*0.13,by+25,10.5,'#b91c1c','left',true); tx('アルカリ性が強い →',b0+(b1-b0)*0.87,by+25,10.5,'#1d4ed8','right',true);
    const mx=b0+(b1-b0)*clamp(p,0,14)/14; ctx.fillStyle=C.ink; ctx.beginPath(); ctx.moveTo(mx,by-1); ctx.lineTo(mx-6,by-9); ctx.lineTo(mx+6,by-9); ctx.closePath(); ctx.fill(); ctx.strokeStyle='#fff'; ctx.lineWidth=2.5; ctx.beginPath(); ctx.moveTo(mx,by); ctx.lineTo(mx,by+11); ctx.stroke();
    const pc=ppCol(p), ch=[['BTB溶液',btbCol(p),btbName(p)],['フェノールフタレイン',pc||'#ffffff',ppName(p)],['青色リトマス紙',c.H>0?'#ef4444':'#3b82f6',c.H>0?'赤くなる':'変化なし'],['赤色リトマス紙',c.OH>0?'#3b82f6':'#f87171',c.OH>0?'青くなる':'変化なし']];
    ch.forEach((q,i)=>{ const cx=x+12+(i>>1)*180, cy=y+94+(i%2)*21; ctx.fillStyle=q[1]; ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1; rr(cx,cy-11,24,14,4); ctx.fill(); ctx.stroke(); tx(q[0]+'：'+q[2],cx+30,cy,10.5,C.ink,'left',true); });
    const n=vn(), M=v===0?['塩酸の中では、塩化水素が H⁺ と Cl⁻ に分かれている。','酸性を示すのは、H⁺（水素イオン）があるから。']
      :(v<n?['加えた OH⁻ は H⁺ と結びついて水になる（中和）。','H⁺ がまだ残っているので、液は酸性。']
      :(v===n?['H⁺ と OH⁻ が過不足なく結びつき、液は中性になった。','Na⁺ と Cl⁻ は塩（塩化ナトリウム）として液にとけている。']
      :['H⁺ がもうないので、加えた OH⁻ はそのまま残る。','OH⁻ がふえていき、液はアルカリ性になる。']));
    tx(M[0],x+12,y+136,11,C.ink,'left',true); tx(M[1],x+12,y+153,11,C.ink,'left',true); }

  // ---------- ② 水溶液の仲間分け（小6） ----------
  function resOf(s,meth){ if(meth==='lit') return s.k==='a'?'青色→赤色':(s.k==='b'?'赤色→青色':'変化なし'); if(meth==='btb') return s.k==='a'?'黄色':(s.k==='b'?'青色':'緑色'); return s.ev?'白い固体が残る':'何も残らない'; }
  function drawSho(){ const meth=$('meth').value, D=done[meth];
    tx(meth==='evap'?'少しとって熱し、水を蒸発させて残る物を調べよう':'見た目はどれも無色とうめい。タップして調べよう',14,24,13.5,C.ink,'left',true);
    SOL.forEach((s,i)=>{ const x0=8+i*104, cx=x0+52, t=D[i];
      ctx.fillStyle=t?'#ffffff':'#f1f5f9'; ctx.strokeStyle=t?'#94a3b8':'#cbd5e1'; ctx.lineWidth=1.2; rr(x0+3,34,98,272,9); ctx.fill(); ctx.stroke();
      if(s.n.length===1) tx(s.n[0],cx,58,12.5,C.ink,'center',true); else { tx(s.n[0],cx,52,11.5,C.ink,'center',true); tx(s.n[1],cx,66,11.5,C.ink,'center',true); }
      // ビーカー
      const bx=cx-26, by0=76, by1=160, ly=110; let lc='rgba(186,230,253,.40)'; if(meth==='btb'&&t) lc=s.k==='a'?'rgba(250,204,21,.6)':(s.k==='b'?'rgba(59,130,246,.55)':'rgba(34,197,94,.55)');
      ctx.fillStyle=lc; ctx.fillRect(bx,ly,52,by1-ly);
      if(s.bub){ for(let j=0;j<6;j++){ const yy=by1-6-((tNow*22+j*13)%(by1-ly-8)); dot(bx+8+(j*17)%38,yy,1.8,'rgba(255,255,255,.95)','rgba(14,116,144,.5)'); } }
      ctx.strokeStyle='#64748b'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(bx-4,by0); ctx.lineTo(bx,by0+3); ctx.lineTo(bx,by1); ctx.lineTo(bx+52,by1); ctx.lineTo(bx+52,by0); ctx.stroke();
      // 調べ方ごとの結果
      if(meth==='lit'){ const ys=172, hs=62; ctx.fillStyle='#60a5fa'; ctx.fillRect(cx-25,ys,20,hs); ctx.fillStyle='#fca5a5'; ctx.fillRect(cx+5,ys,20,hs);
          if(t){ dot(cx-15,ys+30,7.5,s.k==='a'?'#ef4444':'#2563eb'); dot(cx+15,ys+30,7.5,s.k==='b'?'#2563eb':'#ef4444'); }
          tx('青色',cx-15,ys+hs+14,10,C.sub,'center',true); tx('赤色',cx+15,ys+hs+14,10,C.sub,'center',true); }
      else if(meth==='btb'){ if(t){ ctx.fillStyle=s.k==='a'?'#facc15':(s.k==='b'?'#3b82f6':'#22c55e'); rr(cx-22,178,44,40,8); ctx.fill(); }
          else { ctx.setLineDash([4,3]); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1.2; rr(cx-22,178,44,40,8); ctx.stroke(); ctx.setLineDash([]); tx('？',cx,205,16,'#94a3b8','center',true); }
          tx('BTB溶液を入れる',cx,248,10,C.sub,'center',true); }
      else { ctx.fillStyle='#e2e8f0'; ctx.strokeStyle='#64748b'; ctx.lineWidth=1.2; ctx.beginPath(); ctx.ellipse(cx,206,34,11,0,0,6.2832); ctx.fill(); ctx.stroke();
          if(t&&s.ev){ for(let j=0;j<16;j++){ const a=j*2.4, q=Math.sqrt((j+0.5)/16); dot(cx+Math.cos(a)*24*q,206+Math.sin(a)*7*q,2.2,'#ffffff','#94a3b8'); } }
          if(t){ ctx.fillStyle='#f97316'; ctx.beginPath(); ctx.moveTo(cx-7,236); ctx.quadraticCurveTo(cx-8,226,cx,219); ctx.quadraticCurveTo(cx+8,226,cx+7,236); ctx.closePath(); ctx.fill(); }
          tx('蒸発皿',cx,252,10,C.sub,'center',true); }
      if(t){ const r=resOf(s,meth); tx(r,cx,278,r.length>6?11:12,meth==='evap'?C.ink:natCol(s.k==='a'?'酸性':(s.k==='b'?'アルカリ性':'中性')),'center',true);
          tx(meth==='evap'?s.st+'がとけていた':'pH '+s.ph,cx,296,10.5,C.sub,'center',true); }
      else tx('タップして調べる',cx,284,10.5,'#0e7490','center',true); });
    const bins=meth==='evap'?[['何も残らない','#0369a1',q=>!q.ev,'気体がとけている水溶液'],['白い固体が残る','#475569',q=>!!q.ev,'固体がとけている水溶液']]
      :[['酸性','#dc2626',q=>q.k==='a',meth==='lit'?'青色リトマス紙が赤くなる':'BTB溶液が黄色になる'],['中性','#15803d',q=>q.k==='n',meth==='lit'?'どちらのリトマス紙も変化なし':'BTB溶液が緑色になる'],['アルカリ性','#2563eb',q=>q.k==='b',meth==='lit'?'赤色リトマス紙が青くなる':'BTB溶液が青色になる']];
    const gap=10, bw=(624-gap*(bins.length-1))/bins.length;
    bins.forEach((b,j)=>{ const x=8+j*(bw+gap); ctx.fillStyle='#fff'; ctx.strokeStyle=b[1]; ctx.lineWidth=1.6; rr(x,314,bw,118,10); ctx.fill(); ctx.stroke();
      tx(b[0],x+12,336,14,b[1],'left',true); let r=0; SOL.forEach((s,i)=>{ if(D[i]&&b[2](s)){ tx(SNAME[i],x+16,358+r*17,12.5,C.ink,'left',true); r++; } });
      if(!r) tx('（まだない）',x+16,358,11,'#94a3b8','left',true); tx(b[3],x+12,424,10.5,C.sub,'left',true); }); }

  // ---------- 統計欄 ----------
  function stats(){ if(chu()){ const c=cnt(v), p=pH(v), n=vn(), nat=natOf(c), bn=btbName(p);
      K('sA').innerHTML='加えた水酸化ナトリウム水溶液'; sh('sA',v+' cm³',v<n?'中性まで あと '+(n-v)+' cm³':(v===n?'ちょうど中性':'中性より '+(v-n)+' cm³ 多い'));
      K('sB').innerHTML='液の性質'; sh('sB',nat,ind()==='btb'?'BTB溶液：'+bn:'フェノールフタレイン：'+ppName(p));
      K('sC').innerHTML='残っている H⁺ ／ OH⁻'; sh('sC',c.H+'こ ／ '+c.OH+'こ','できた水 '+c.W+'こ');
      K('sD').innerHTML='pH（参考）'; sh('sD',p.toFixed(1),'7が中性');
      setShare('【中和とイオン】塩酸10 cm³（BTB溶液入り）に'+(k===2?'2倍の濃さの':'')+'水酸化ナトリウム水溶液を'+v+' cm³加えると'+nat+'（BTB溶液は'+bn+'・pH '+p.toFixed(1)+'）。H⁺ '+c.H+'こ、OH⁻ '+c.OH+'こ、できた水 '+c.W+'こ｜シミュラボ'); }
    else { const meth=$('meth').value, D=done[meth], nm=['リトマス紙','BTB溶液','蒸発させる'][['lit','btb','evap'].indexOf(meth)], nd=D.filter(x=>x).length;
      const pick=f=>SOL.map((s,i)=>D[i]&&f(s)?SNAME[i]:null).filter(x=>x);
      K('sA').innerHTML='調べた水溶液'; sh('sA',nd+'／6',nm);
      if(meth==='evap'){ const g=pick(s=>!s.ev), so=pick(s=>!!s.ev);
        K('sB').innerHTML='何も残らない'; sh('sB',g.length+'つ',g.join('・')||'—'); K('sC').innerHTML='白い固体が残る'; sh('sC',so.length+'つ',so.join('・')||'—');
        K('sD').innerHTML='わかること'; sh('sD','気体','何も残らない水溶液には気体がとけている');
        setShare('【水溶液の性質】水を蒸発させると、何も残らない：'+(g.join('・')||'—')+'／白い固体が残る：'+(so.join('・')||'—')+'｜シミュラボ'); }
      else { const a=pick(s=>s.k==='a'), n=pick(s=>s.k==='n'), b=pick(s=>s.k==='b');
        K('sB').innerHTML='酸性'; sh('sB',a.length+'つ',a.join('・')||'—'); K('sC').innerHTML='中性'; sh('sC',n.length+'つ',n.join('・')||'—'); K('sD').innerHTML='アルカリ性'; sh('sD',b.length+'つ',b.join('・')||'—');
        setShare('【水溶液の性質】'+nm+'で調べると、酸性：'+(a.join('・')||'—')+'／中性：'+(n.join('・')||'—')+'／アルカリ性：'+(b.join('・')||'—')+'｜シミュラボ'); } } }
  function vis(){ const c=chu(); showF('conc',c); showF('v',c); showF('meth',!c); ['add','auto','reset','ind'].forEach(id=>show(id,c)); $('ind').textContent=indV==='btb'?'🎨 指示薬：BTB溶液':'🎨 指示薬：フェノールフタレイン'; ['all','clr'].forEach(id=>show(id,!c)); }
  function syncV(){ $('v').max=vmax(); $('v').value=v; $('vL').textContent=v+' cm³'; }
  function addOne(){ if(v>=vmax()){ autoOn=false; $('auto').textContent='⏩ 自動で加える'; return; } v++; syncV(); drops.push({y:142}); stats(); }
  function draw(){ ctx.fillStyle=C.bg; ctx.fillRect(0,0,W,H); if(chu()){ drawBeaker(); drawGraph(); drawInfo(); } else drawSho(); }

  // ---------- 操作 ----------
  if(Q.get('ind')==='pp') indV='pp';
  ['mode','conc','meth'].forEach(id=>{ if(!Q.has(id)) return; const el=$(id), q=Q.get(id); if([].some.call(el.options,o=>o.value===q)) el.value=q; });
  k=+$('conc').value; if(Q.has('v')) v=clamp(Math.round(+Q.get('v')||0),0,vmax());
  if(Q.get('test')==='all') done[$('meth').value]=[1,1,1,1,1,1];
  $('mode').addEventListener('change',()=>{ vis(); stats(); });
  $('conc').addEventListener('change',()=>{ k=+$('conc').value; v=Math.min(v,vmax()); syncV(); rebuild(); stats(); });
  $('ind').addEventListener('click',()=>{ indV=indV==='btb'?'pp':'btb'; vis(); stats(); });
  $('meth').addEventListener('change',stats);
  $('v').addEventListener('input',()=>{ v=+$('v').value; autoOn=false; $('auto').textContent='⏩ 自動で加える'; rebuild(); stats(); });
  $('add').addEventListener('click',addOne);
  $('auto').addEventListener('click',()=>{ if(autoOn){ autoOn=false; } else { if(v>=vmax()){ v=0; syncV(); rebuild(); } autoOn=true; autoT=0.6; } $('auto').textContent=autoOn?'⏸ 止める':'⏩ 自動で加える'; stats(); });
  $('reset').addEventListener('click',()=>{ v=0; autoOn=false; $('auto').textContent='⏩ 自動で加える'; syncV(); rebuild(); stats(); });
  $('all').addEventListener('click',()=>{ done[$('meth').value]=[1,1,1,1,1,1]; stats(); });
  $('clr').addEventListener('click',()=>{ done[$('meth').value]=[0,0,0,0,0,0]; stats(); });
  cv.addEventListener('pointerdown',e=>{ const p=cpos(cv,e), x=p[0]/dpr, y=p[1]/dpr;
    if(chu()){ if(x<258&&y>40) addOne(); return; }
    if(y>34&&y<306){ const i=Math.floor((x-8)/104); if(i>=0&&i<6){ done[$('meth').value][i]=1; stats(); } } });
  function frame(t){ const dt=last?Math.min(0.05,(t-last)/1000):0; last=t; tNow+=dt;
    if(autoOn){ autoT+=dt; if(autoT>=0.9){ autoT=0; addOne(); } }
    if(chu()) step(dt); draw(); requestAnimationFrame(frame); }
  syncV(); vis(); rebuild(); stats(); draw();
  requestAnimationFrame(frame);
'''

CHUWA_ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
<p>うすい塩酸にBTB溶液を入れ、水酸化ナトリウム水溶液を少しずつ加えると、液の色は<b>黄色（酸性）→緑色（中性）→青色（アルカリ性）</b>と変わります。このとき液の中では、酸性のもとである<b>水素イオン（H⁺）</b>と、アルカリ性のもとである<b>水酸化物イオン（OH⁻）</b>が結びついて水（H₂O）ができ、たがいの性質を打ち消し合っています（中和）。残ったナトリウムイオン（Na⁺）と塩化物イオン（Cl⁻）は、塩（塩化ナトリウム）として液にとけています。イオンの数の変化を、モデル図と4本の折れ線グラフで同時に確かめられます。</p>
''' + N('<b>対応する単元</b>：中学3年 第1分野（6）化学変化とイオン ア（ア）水溶液とイオン「㋑酸・アルカリ」「㋒中和と塩」（内容の取扱いで、酸・アルカリでは pH にも触れることとされています）／小学6年 A（2）水溶液の性質「水溶液には，酸性，アルカリ性及び中性のものがあること」（リトマス紙などを用いた仲間分け）。実験の切りかえ（上のメニュー）で「小6 水溶液の仲間分け」を選ぶと、塩酸・炭酸水・食塩水・石灰水・アンモニア水・水酸化ナトリウム水溶液をリトマス紙・BTB溶液・蒸発で調べられます。') + '''
<h2>授業での使い方</h2>
<h3>導入：混ぜると性質はどうなる？（中3）</h3>
<p>「塩酸（酸性）に水酸化ナトリウム水溶液（アルカリ性）を加えていくと、液の性質はどうなるか」を予想させてから、「💧 1 cm³ 加える」を押していきます（ビーカーをタップしても加えられます）。BTB溶液の色が黄色のまましばらく変わらず、10 cm³ でちょうど緑色、そのあと青色になることを確かめます。</p>
<h3>展開：イオンの数をグラフにする（中3）</h3>
<p>1 cm³ ずつ加えるたびに、左のモデル図で OH⁻ が H⁺ と結びついて水になる様子と、右のグラフで4種類のイオンの数の変化を見ます。H⁺ は減って中性で0になり、OH⁻ は中性までは0で、そのあと増えます。Na⁺ は加えた量に比例して増え、Cl⁻ はずっと変わりません。「水酸化ナトリウム水溶液の濃さ」を2倍にすると、中性になるのが 5 cm³ になることも確かめられます。「🎨 指示薬」ボタンでフェノールフタレイン溶液に切りかえると、アルカリ性になったときだけ赤色に変わる（酸性・中性では無色）ことも比べられます。</p>
<h3>導入・まとめ：水溶液の仲間分け（小6）</h3>
<p>「小6 水溶液の仲間分け」に切りかえ、見た目はどれも無色とうめいな6つの水溶液を、リトマス紙で1つずつ調べて、酸性・中性・アルカリ性に分けます。「調べ方」を「蒸発させる」にすると、何も残らない水溶液（気体がとけている）と、白い固体が残る水溶液（固体がとけている）に分かれます。中3では、この仲間分けをふり返ってからイオンの学習に入ると、つながりがはっきりします。</p>
<h3>児童・生徒への問いの例</h3>
<ol>
<li>塩酸に水酸化ナトリウム水溶液を6 cm³ 加えた。BTB溶液は黄色のままなのに、中和は起きているといえるだろうか？（モデル図で H⁺ の数を数えてみよう）</li>
<li>中性になった液を蒸発させると、白い結晶が残った。この物質は何だろう？それはどのイオンとどのイオンからできたのだろう？</li>
<li>リトマス紙で調べると、炭酸水は酸性、食塩水は中性、石灰水はアルカリ性だった。炭酸水を蒸発させても何も残らないのはなぜだろう？</li>
</ol>
<h2>しくみ・解説</h2>
<h3>用語の意味（1文で）</h3>
<ul>
<li><b>酸</b>とは、水溶液にしたときに電離して水素イオン（H⁺）を生じる物質です（例：塩化水素 HCl → H⁺ ＋ Cl⁻）。</li>
<li><b>アルカリ</b>とは、水溶液にしたときに電離して水酸化物イオン（OH⁻）を生じる物質です（例：水酸化ナトリウム NaOH → Na⁺ ＋ OH⁻）。</li>
<li><b>中和</b>とは、酸の水溶液とアルカリの水溶液を混ぜたとき、H⁺ と OH⁻ が結びついて水ができ、たがいの性質を打ち消し合う反応です（H⁺ ＋ OH⁻ → H₂O）。</li>
<li><b>塩（えん）</b>とは、中和のときに、酸の陰イオンとアルカリの陽イオンが結びついてできる物質です（例：塩化ナトリウム NaCl）。</li>
<li><b>pH（ピーエイチ）</b>とは、酸性・アルカリ性の強さを0〜14の数値で表したもので、7が中性、7より小さいほど酸性が強く、7より大きいほどアルカリ性が強いことを表します。</li>
<li><b>指示薬</b>とは、液の性質によって色が変わる薬品で、リトマス紙・BTB溶液・フェノールフタレイン溶液などがあります。</li>
</ul>
''' + N('塩酸と水酸化ナトリウム水溶液の中和<br>HCl ＋ NaOH → NaCl ＋ H₂O（塩化水素＋水酸化ナトリウム → 塩化ナトリウム＋水）<br>イオンで書くと：H⁺ ＋ Cl⁻ ＋ Na⁺ ＋ OH⁻ → Na⁺ ＋ Cl⁻ ＋ H₂O') + '''
<h3>指示薬の色の早見表</h3>
''' + T([["青色リトマス紙", "赤色に変わる", "変化なし", "変化なし"], ["赤色リトマス紙", "変化なし", "変化なし", "青色に変わる"],
          ["BTB溶液", "黄色", "緑色", "青色"], ["フェノールフタレイン溶液", "無色", "無色", "赤色（pH約8以上）"],
          ["pH（参考）", "7より小さい", "7", "7より大きい"]],
         ["指示薬", "酸性", "中性", "アルカリ性"]) + '''
<h3>加えた量とイオンの数（モデル）</h3>
<p>このシミュレーションでは、うすい塩酸10 cm³ の中の H⁺ と Cl⁻ をそれぞれ10こ、同じ濃さの水酸化ナトリウム水溶液1 cm³ の中の Na⁺ と OH⁻ をそれぞれ1こと考えています（授業で数えやすい小さな数にしたモデルです）。</p>
''' + T([[NW("0 cm³"), "10", "10", "0", "0", "0", "20", "酸性（黄色）", "1.0"],
          [NW("2 cm³"), "8", "10", "2", "0", "2", "20", "酸性（黄色）", "1.2"],
          [NW("4 cm³"), "6", "10", "4", "0", "4", "20", "酸性（黄色）", "1.4"],
          [NW("6 cm³"), "4", "10", "6", "0", "6", "20", "酸性（黄色）", "1.6"],
          [NW("8 cm³"), "2", "10", "8", "0", "8", "20", "酸性（黄色）", "2.0"],
          [NW("10 cm³"), "0", "10", "10", "0", "10", "20", "中性（緑色）", "7.0"],
          [NW("12 cm³"), "0", "10", "12", "2", "10", "24", "アルカリ性（青色）", "12.0"],
          [NW("16 cm³"), "0", "10", "16", "6", "10", "32", "アルカリ性（青色）", "12.4"],
          [NW("20 cm³"), "0", "10", "20", "10", "10", "40", "アルカリ性（青色）", "12.5"]],
         ["加えた量", "H⁺", "Cl⁻", "Na⁺", "OH⁻", "できた水", "イオンの総数", "液の性質（BTB）", "pH（参考）"]) + '''
<p>グラフにすると、教科書によく出る4本の折れ線になります。</p>
<ul>
<li><b>H⁺（水素イオン）</b>：加えた OH⁻ と結びついて水になるので減り、中性で0になる。そのあとは0のまま。</li>
<li><b>Cl⁻（塩化物イオン）</b>：どの イオンとも結びつかないので、ずっと10こで変わらない。</li>
<li><b>Na⁺（ナトリウムイオン）</b>：どのイオンとも結びつかないので、加えた量に比例して増え続ける。</li>
<li><b>OH⁻（水酸化物イオン）</b>：中性までは H⁺ と結びついて水になるので0。中性をこえると、加えた分だけ増える。</li>
</ul>
<p>イオンの総数は、中性になるまでは変わらず（H⁺ が1こ減るたびに Na⁺ が1こ増える）、中性をこえると増えていきます。</p>
<h3>計算問題の解き方（例題）</h3>
<p><b>例題1</b>　うすい塩酸10 cm³ を中性にするのに、水酸化ナトリウム水溶液が10 cm³ 必要だった。同じ塩酸15 cm³ を中性にするには、水酸化ナトリウム水溶液は何 cm³ 必要か。<br>中和する体積は比例するので、10×15/10＝<b>15 cm³</b>。</p>
<p><b>例題2</b>　例題1の水酸化ナトリウム水溶液の濃さを2倍にすると、塩酸10 cm³ を中性にするのに何 cm³ 必要か。<br>1 cm³ にふくまれる OH⁻ が2倍になるので、必要な体積は半分の <b>5 cm³</b>（シミュレーションの「濃さ2倍」で確かめられます）。</p>
<p><b>例題3</b>　H⁺ が10このモデルの塩酸に、OH⁻ が6こ入った水酸化ナトリウム水溶液を加えた。液の中の H⁺、OH⁻、Na⁺、Cl⁻ はそれぞれ何こか。また、できた水の分子は何こか。<br>OH⁻ 6こはすべて H⁺ と結びつくので、<b>H⁺ 4こ、OH⁻ 0こ、Na⁺ 6こ、Cl⁻ 10こ、水 6こ</b>。H⁺ が残っているので液は酸性です。</p>
<h3>pH の値について（参考）</h3>
<p>統計欄の pH は、塩酸と水酸化ナトリウム水溶液の濃さをどちらも0.1 mol/L（約0.4％、濃さ2倍は0.2 mol/L）として計算した参考値です。中性の近くで pH が大きくとぶのは、わずかな H⁺ や OH⁻ の残りでも pH が大きく変わるためです（たとえば9 cm³ では pH 2.3、11 cm³ では pH 11.7）。中学校では「pH 7 が中性で、7より小さいほど酸性が強く、7より大きいほどアルカリ性が強い」ことを押さえれば十分です。</p>
''' + T([["うすい塩酸", "約1", "酸性"], ["レモンの果汁", "約2", "酸性"], ["食酢", "約3", "酸性"], ["炭酸水", "約4〜5", "酸性"],
          ["食塩水・砂糖水・純粋な水", "7", "中性"], ["せっけん水", "約9〜10", "アルカリ性"], ["うすいアンモニア水", "約11", "アルカリ性"],
          ["石灰水", "約12", "アルカリ性"], ["うすい水酸化ナトリウム水溶液", "約13", "アルカリ性"]],
         ["身の回りの水溶液", "pH（目安）", "性質"]) + '''
<h3>小6：水溶液の仲間分け</h3>
''' + T([["塩酸", "酸性", "何も残らない", "塩化水素（気体）"], ["炭酸水", "酸性", "何も残らない", "二酸化炭素（気体）"], ["食塩水", "中性", "白い固体が残る", "食塩（固体）"],
          ["石灰水", "アルカリ性", "白い固体が残る", "水酸化カルシウム（固体）"], ["アンモニア水", "アルカリ性", "何も残らない", "アンモニア（気体）"],
          ["水酸化ナトリウム水溶液", "アルカリ性", "白い固体が残る", "水酸化ナトリウム（固体）"]],
         ["水溶液", "リトマス紙での性質", "蒸発させると", "とけているもの"]) + '''
<p>塩酸とアンモニア水はつんとしたにおいがあります。においを調べるときは、直接かがずに手であおいでかぎます。蒸発させる実験は、換気をよくして少量で行います。</p>
<h3>中和について知っておきたいこと</h3>
<ul>
<li><b>中性にならなくても中和は起きている</b>：BTB溶液が黄色のままでも、加えた OH⁻ は H⁺ と結びついて水になっています。中和は「中性になること」ではなく「H⁺ と OH⁻ が結びつくこと」です。</li>
<li><b>水にとける塩ととけない塩</b>：塩酸と水酸化ナトリウム水溶液からできる塩化ナトリウムは水にとけるので、液の中では Na⁺ と Cl⁻ のままです。うすい硫酸と水酸化バリウム水溶液を混ぜると、水にとけにくい塩（硫酸バリウム）ができ、白い沈殿になります。</li>
<li><b>中和の熱</b>：中和が起きると熱が出て、液の温度が少し上がります。</li>
<li><b>身の回りの中和</b>：酸性になった土に石灰をまいて中和する（土壌の改良）、胃酸を中和する胃薬、温泉の強い酸性の水を石灰で中和する施設などがあります。</li>
</ul>
<h3>このシミュレーションで単純化していること</h3>
<ul>
<li>イオンの数（H⁺・Cl⁻ が各10こ）は数えやすいように決めたモデルで、実際の水溶液にはけた違いに多くのイオンがあります。イオンの大きさ・色・動きも模式的です。</li>
<li>中和で H⁺ と OH⁻ が結びつく動きは、見やすいようにゆっくり描いています。実際の中和は、混ぜたとたんにほぼ一瞬で起こります。</li>
<li>液の色は、BTB溶液では pH 6.0 以下を黄色、7.6 以上を青色、フェノールフタレイン溶液では pH 8.2 以上を赤色としています。水そのものがわずかに電離してできる H⁺ と OH⁻ は、モデル図では省略しています。</li>
<li>リトマス紙の仲間分けで示した pH は、市販の炭酸水や、学校の実験でよく使うくらいのうすさの水溶液の目安です。</li>
</ul>
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「中学校学習指導要領（平成29年告示）解説 理科編」第1分野（6）化学変化とイオン ア（ア）水溶液とイオン（''' + A(MEXT_CHU, "中学校学習指導要領解説") + '''）</li>
<li>文部科学省「小学校学習指導要領（平成29年告示）解説 理科編」第6学年 A（2）水溶液の性質（''' + A(MEXT_SHO, "小学校学習指導要領解説") + '''）</li>
<li>中学校理科の教科書（第3学年「化学変化とイオン」の単元）、小学校理科の教科書（第6学年「水溶液の性質」の単元）</li>
</ul>
'''

sim(slug="chuwa-ion", cat="rika", emoji="⚗️", score=82,
    title="酸・アルカリと中和のシミュレーター（BTB溶液の色とイオンのモデル）",
    title_tag="中和とイオンのシミュレーター｜塩酸＋水酸化ナトリウム水溶液・BTB溶液の色・イオンの数のグラフ（中3・小6理科）",
    meta_desc="塩酸に水酸化ナトリウム水溶液を1 cm³ずつ加えると、BTB溶液が黄→緑→青に。H⁺・Cl⁻・Na⁺・OH⁻の数をイオンのモデルと4本の折れ線グラフで表示し、中和で水と塩ができることを確かめる中3理科の無料シミュレーター。pHと指示薬の早見表、小6のリトマス紙の仲間分けつき。",
    og_title="酸・アルカリと中和のシミュレーター（BTB溶液の色とイオンのモデル）",
    og_desc="塩酸に水酸化ナトリウム水溶液を加えると、BTB溶液が黄→緑→青。イオンの数の4本のグラフとモデル図で中和を確かめる。小6のリトマス紙の仲間分けも。",
    card_desc="塩酸に水酸化ナトリウム水溶液を1 cm³ずつ。BTBの色とH⁺・OH⁻・Na⁺・Cl⁻の数をモデルとグラフで。",
    lead="うすい塩酸（BTB溶液入り）に、こまごめピペットで水酸化ナトリウム水溶液を1 cm³ずつ加えると、液の色が黄色→緑色→青色と変わります。ビーカーの中のイオン（H⁺・Cl⁻・Na⁺・OH⁻）の数と、加えた量とイオンの数のグラフ、pH（参考）を同時に確かめられます。小6向けに、身近な水溶液をリトマス紙で仲間分けするモードもあります。",
    model="中3 酸・アルカリと中和／小6 水溶液の性質",
    level="小学6年、中学3年",
    unit="中学校 第1分野（6）化学変化とイオン ア（ア）水溶液とイオン／小学校 第6学年 A（2）水溶液の性質",
    canvas=canvas(640, 440, light=True),
    controls=select("mode", "実験", [("chu", "中3 中和とイオン"), ("sho", "小6 水溶液の仲間分け")])
           + slider("v", "加えた量", 0, 20, 0, 1, "{v} cm³")
           + select("conc", "水酸化ナトリウム水溶液の濃さ", [("1", "塩酸と同じ"), ("2", "塩酸の2倍")])
           + select("meth", "調べ方", [("lit", "リトマス紙"), ("btb", "BTB溶液"), ("evap", "蒸発させる")]),
    buttons=btn("add", "💧 1 cm³ 加える", True) + btn("auto", "⏩ 自動で加える") + btn("reset", "⏮ はじめから") + btn("ind", "🎨 指示薬：BTB溶液")
           + btn("all", "🧪 全部調べる", True) + btn("clr", "⏮ やり直す"),
    stats=stats([("sA", "加えた水酸化ナトリウム水溶液", False), ("sB", "液の性質", True), ("sC", "残っている H⁺ ／ OH⁻", False), ("sD", "pH（参考）", False)]),
    legend="中3：左＝ビーカーの中のイオンのモデル（赤 H⁺ 水素イオン、緑 Cl⁻ 塩化物イオン、紫 Na⁺ ナトリウムイオン、青 OH⁻ 水酸化物イオン、水色 水の分子）。ビーカーをタップしても1 cm³ずつ加えられます。右上＝加えた量とイオンの数のグラフ、右下＝液の性質・pH（参考）と指示薬の色。小6：水溶液をタップすると、選んだ調べ方で調べ、下の箱に仲間分けされます。",
    article=CHUWA_ARTICLE,
    faqs=[("中和とは何ですか？", "酸の水溶液とアルカリの水溶液を混ぜたとき、水素イオン（H⁺）と水酸化物イオン（OH⁻）が結びついて水ができ、たがいの性質を打ち消し合う反応です。塩酸と水酸化ナトリウム水溶液の中和では、水と塩化ナトリウム（塩）ができます。"),
          ("塩酸に水酸化ナトリウム水溶液を加えると、BTB溶液の色はどう変わりますか？", "はじめは酸性なので黄色、ちょうど中和して中性になると緑色、さらに加えてアルカリ性になると青色になります。同じ濃さなら、塩酸10 cm³に水酸化ナトリウム水溶液10 cm³を加えたときに緑色になります。"),
          ("中性にならないと中和は起きていないのですか？", "いいえ。BTB溶液が黄色のままでも、加えたOH⁻はH⁺と結びついて水になっており、中和は起きています。中性になるのは、H⁺とOH⁻が過不足なく結びついたときです。"),
          ("中和のときのイオンの数のグラフはどうなりますか？", "H⁺は減って中性で0になり、そのあと0のままです。OH⁻は中性までは0で、そのあと増えます。Na⁺は加えた量に比例して増え続け、Cl⁻は変わりません。イオンの総数は中性までは一定で、そのあと増えます。"),
          ("塩（えん）とは何ですか？", "中和のときに、酸の陰イオンとアルカリの陽イオンが結びついてできる物質です。塩化ナトリウム（Na⁺とCl⁻）は水にとける塩、硫酸バリウム（うすい硫酸と水酸化バリウム水溶液からできる）は水にとけにくい塩で、白い沈殿になります。"),
          ("リトマス紙の色はどう変わりますか？", "酸性の水溶液は青色リトマス紙を赤色に、アルカリ性の水溶液は赤色リトマス紙を青色に変えます。中性の水溶液では、どちらのリトマス紙も色が変わりません。")],
    rel=[("kagaku-shitsuryou", "🧪", "化学変化と質量シミュレーター"), ("joutai-henka", "🧊", "状態変化と粒子のシミュレーター"),
         ("denki-kairo", "🔌", "電気回路シミュレーター"), ("youkaido", "🧂", "ものの溶け方・溶解度のシミュレーター"), ("diffusion", "🫧", "拡散シミュレーター")],
    js=JS_CHUWA)


# ============================================================ 2 とじこめた空気と水
JS_KUUKI = HELP + r'''
  const C={bg:'#f8fafc',ink:'#0f172a',sub:'#64748b',grid:'#e2e8f0',push:'#dc2626',back:'#2563eb'};
  // 注射器：断面積 6 cm²（内径約2.8 cm）・中身 40 mL。温度は一定（ボイルの法則 p×V＝一定）
  // 大気圧がピストンをおす力 F0＝101325 Pa×6 cm²÷9.80665 ≒ 6.2 kg重。おす力 F のとき 空気の体積＝もとの体積×F0÷(F0＋F)
  const F0=101325*6e-4/9.80665, FMAX=12, PX=6, YB=400, CX=146, BW=84, BXL=CX-BW/2, BXR=CX+BW/2, ROD=80;
  const MD={air:{a:40,w:0,col:'#2563eb',nm:'空気だけ',tt:'注射器にとじこめた空気'},water:{a:0,w:40,col:'#0d9488',nm:'水だけ',tt:'注射器にとじこめた水'},half:{a:20,w:20,col:'#9333ea',nm:'空気と水',tt:'空気と水を半分ずつ'}};
  let m='air', F=0, rel=false, drag=null, recs={air:{},water:{},half:{}}, gas=[], liq=[], last=0, tNow=0, lastKey='';
  const VtM=(mm,f)=>MD[mm].a*F0/(F0+f)+MD[mm].w, Va=f=>MD[m].a*F0/(F0+f), Vt=f=>VtM(m,f);
  function fOfVt(vt){ const M=MD[m]; if(M.a<=0) return 0; const va=Math.max(1,vt-M.w); return clamp(F0*(M.a/va-1),0,FMAX); }
  const pb=()=>YB-Vt(F)*PX, wTop=()=>YB-MD[m].w*PX;
  function initParts(){ const M=MD[m]; gas=[]; liq=[]; const ng=M.a>0?(m==='air'?30:16):0, top=YB-(M.a+M.w)*PX, bot=wTop();
    for(let i=0;i<ng;i++){ const a=rnd(0,6.283); gas.push({x:rnd(BXL+6,BXR-6),y:rnd(top+6,bot-6),vx:Math.cos(a)*80,vy:Math.sin(a)*80}); }
    if(M.w>0){ for(let j=0;;j++){ const y=YB-5.5-j*9.5; if(y<bot+5) break; for(let x=BXL+6+(j%2?5.5:0); x<=BXR-5.5; x+=11) liq.push({x:x,y:y,ph:rnd(0,6.28)}); } } }
  function step(dt){ const top=pb(), bot=wTop(), r=4.5;
    gas.forEach(g=>{ g.x+=g.vx*dt; g.y+=g.vy*dt;
      if(g.x<BXL+r){ g.x=BXL+r; g.vx=Math.abs(g.vx); } if(g.x>BXR-r){ g.x=BXR-r; g.vx=-Math.abs(g.vx); }
      if(g.y<top+r){ g.y=top+r; g.vy=Math.abs(g.vy); } if(g.y>bot-r){ g.y=bot-r; g.vy=-Math.abs(g.vy); } }); }
  function rec(){ recs[m][(Math.round(F*2)/2).toFixed(1)]=1; }
  function syncF(){ $('f').value=F; $('fL').textContent=F.toFixed(1)+' kg'; }

  function drawSyr(){ const M=MD[m], y=pb(), gy=y-12, top0=YB-(M.a+M.w)*PX;
    panel(8,8,238,424); tx(M.tt,16,26,13,C.ink,'left',true);
    // 中身
    if(M.w>0){ ctx.fillStyle='rgba(45,212,191,.16)'; ctx.fillRect(BXL,wTop(),BW,YB-wTop()); }
    if(M.a>0){ ctx.fillStyle='rgba(191,219,254,.35)'; ctx.fillRect(BXL,y,BW,wTop()-y); }
    liq.forEach(p=>dot(p.x+Math.sin(tNow*7+p.ph)*0.6,p.y+Math.cos(tNow*6+p.ph)*0.6,5,'#5eead4','#0f766e'));
    gas.forEach(g=>dot(g.x,g.y,4.5,'#60a5fa','#1d4ed8'));
    // つつ・目もり
    ctx.strokeStyle='#64748b'; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(BXL-1.5,96); ctx.lineTo(BXL-1.5,YB+1.5); ctx.lineTo(BXR+1.5,YB+1.5); ctx.lineTo(BXR+1.5,96); ctx.stroke();
    ctx.fillStyle='#94a3b8'; rr(BXL-18,90,BW+36,7,3); ctx.fill();
    ctx.fillStyle='#cbd5e1'; ctx.strokeStyle='#64748b'; ctx.lineWidth=1.2; ctx.fillRect(CX-5,YB+2,10,9); ctx.strokeRect(CX-5,YB+2,10,9);
    ctx.fillStyle='#334155'; rr(CX-46,YB+11,92,9,3); ctx.fill(); tx('ゴム板',CX+52,YB+20,10.5,C.sub,'left',true);
    for(let ml=0; ml<=50; ml+=5){ const yy=YB-ml*PX; ctx.strokeStyle='#64748b'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(BXR+1,yy); ctx.lineTo(BXR+(ml%10?7:12),yy); ctx.stroke(); if(ml%10===0) tx(String(ml),BXR+15,yy+4,10.5,C.sub,'left',true); }
    tx('mL',BXR+15,YB-50*PX-14,10.5,C.sub,'left',true);
    // もとの位置
    if(Math.abs(y-top0)>2){ ctx.setLineDash([5,4]); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1.3; ctx.beginPath(); ctx.moveTo(BXL,top0); ctx.lineTo(BXR,top0); ctx.stroke(); ctx.setLineDash([]); }
    // ピストン・おしぼう・指
    ctx.fillStyle='#e2e8f0'; ctx.strokeStyle='#64748b'; ctx.lineWidth=1.2; ctx.fillRect(CX-5,gy-ROD,10,ROD); ctx.strokeRect(CX-5,gy-ROD,10,ROD);
    ctx.fillStyle='#1f2937'; rr(BXL+1,gy,BW-2,12,3); ctx.fill();
    ctx.fillStyle='#94a3b8'; rr(CX-21,gy-ROD-8,42,8,3); ctx.fill();
    ctx.fillStyle='#fcd9b6'; ctx.strokeStyle='#c08457'; ctx.lineWidth=1.3; rr(CX-12,gy-ROD-34,24,27,10); ctx.fill(); ctx.stroke();
    ctx.fillStyle='rgba(255,255,255,.7)'; rr(CX-7,gy-ROD-31,14,9,4); ctx.fill();
    // 力の矢印
    const L=8+F/FMAX*62;
    if(F>0.05){ arrow(CX-26,gy-L-4,CX-26,gy-3,C.push,4,5.5); arrow(CX+26,y+L+4,CX+26,y+3,C.back,4,5.5);
      tx('おす力',BXL-14,gy-26,11,C.push,'right',true); tx(F.toFixed(1)+' kg',BXL-14,gy-11,11.5,C.push,'right',true);
      tx('おし返す力',BXL-14,y+20,11,C.back,'right',true); tx(F.toFixed(1)+' kg',BXL-14,y+35,11.5,C.back,'right',true);
      if(M.a===0) tx('動かない！',BXL-12,gy-56,13,C.push,'right',true); }
    else if(!drag) tx('指で下へ ↓',CX-18,gy-ROD-14,11.5,'#0e7490','right',true);
    tag(Vt(F).toFixed(1)+' mL',BXR+9,y+5,10.5,C.ink,'left');
    if(M.w>0) tag('水',BXL+8,wTop()+(M.a>0?18:Math.max(18,y-wTop()+30)),10.5,'#0f766e','left');
    if(M.a>0) tag('空気',BXL+8,y+18,10.5,'#1d4ed8','left'); }
  function drawGraph(){ const x=254, y=8, w=378, h=282; panel(x,y,w,h);
    tx('中の体積と手ごたえ（おし返す力）',x+10,y+22,13,C.ink,'left',true);
    const X0=x+40, X1=x+w-16, Y0=y+h-36, Y1=y+48, gx=a=>X0+(X1-X0)*a/50, gy=b=>Y0-(Y0-Y1)*b/FMAX;
    ctx.strokeStyle=C.grid; ctx.lineWidth=1; for(let b=2;b<=FMAX;b+=2){ ctx.beginPath(); ctx.moveTo(X0,gy(b)); ctx.lineTo(X1,gy(b)); ctx.stroke(); }
    for(let a=10;a<=50;a+=10){ ctx.beginPath(); ctx.moveTo(gx(a),Y0); ctx.lineTo(gx(a),Y1); ctx.stroke(); }
    for(let b=0;b<=FMAX;b+=2) tx(String(b),X0-6,gy(b)+4,10.5,C.sub,'right');
    for(let a=0;a<=50;a+=10) tx(String(a),gx(a),Y0+15,10.5,C.sub,'center');
    ctx.strokeStyle=C.ink; ctx.lineWidth=1.3; ctx.beginPath(); ctx.moveTo(X0,Y1-4); ctx.lineTo(X0,Y0); ctx.lineTo(X1,Y0); ctx.stroke();
    tx('手ごたえ［kg］',x+10,y+40,10.5,C.sub,'left',true); tx('中の体積（注射器の目もり）［mL］',X1,Y0+30,10.5,C.sub,'right',true);
    ctx.setLineDash([4,4]); ctx.strokeStyle='#94a3b8'; ctx.beginPath(); ctx.moveTo(gx(40),Y0); ctx.lineTo(gx(40),Y1); ctx.stroke(); ctx.setLineDash([]); tx('もとの体積',gx(40)-4,Y1+8,10,'#64748b','right',true);
    ['air','water','half'].forEach(mm=>{ const ks=Object.keys(recs[mm]).map(Number).sort((a,b)=>a-b); if(!ks.length) return; const col=MD[mm].col;
      ctx.strokeStyle=col; ctx.globalAlpha=0.5; ctx.lineWidth=1.6; ctx.beginPath(); ks.forEach((f,i)=>{ const X=gx(VtM(mm,f)), Y=gy(f); if(i) ctx.lineTo(X,Y); else ctx.moveTo(X,Y); }); ctx.stroke(); ctx.globalAlpha=1;
      ks.forEach(f=>dot(gx(VtM(mm,f)),gy(f),3.3,col)); });
    ctx.fillStyle='#fff'; ctx.strokeStyle=MD[m].col; ctx.lineWidth=3; ctx.beginPath(); ctx.arc(gx(Vt(F)),gy(F),6.5,0,7); ctx.fill(); ctx.stroke();
    ['air','water','half'].forEach((mm,i)=>{ dot(X0+12,Y1+12+i*16,4.5,MD[mm].col); tx(MD[mm].nm,X0+22,Y1+16+i*16,11,MD[mm].col,'left',true); }); }
  function msgs(){ const M=MD[m], va=Va(F);
    if(rel&&F>0.05) return [M.a>0?'手をはなすと、ピストンがもどる！':'手をはなした。','とじこめた'+(M.a>0?'空気':'水')+'がおし返す力で、もとの位置へ。',''];
    if(F<0.05) return [M.a===0?'とじこめた水を、ピストンでおしてみよう。':(M.w>0?'空気と水を半分ずつ入れた。おすとどうなる？':'とじこめた空気を、ピストンでおしてみよう。'),'注射器の図を指で下へなぞるか、スライダーを動かす。','手をはなすと、ピストンはどうなるかな？'];
    if(M.a===0) return ['水は、おしちぢめられない！','強くおしても、体積は 40 mL のまま変わらない。','手ごたえは大きいのに、ピストンは動かない。'];
    if(M.w>0) return ['空気の部分だけがちぢむ！','水（20 mL）はそのままで、空気だけが小さくなる。','空気 '+va.toFixed(1)+' mL・手ごたえ '+F.toFixed(1)+' kg'];
    return ['空気は、おしちぢめられる！','おしちぢめるほど、おし返す力（手ごたえ）が大きい。',F.toFixed(1)+' kgのものを持ち上げるくらいの力でおしている。']; }
  function drawInfo(){ const x=254, y=298, w=378, h=134; panel(x,y,w,h);
    tx('手ごたえ（おし返す力）',x+12,y+24,12.5,C.ink,'left',true); tx(F.toFixed(1)+' kg',x+w-14,y+27,20,C.back,'right',true);
    const b0=x+14, b1=x+w-14, by=y+36; ctx.fillStyle='#e2e8f0'; rr(b0,by,b1-b0,14,7); ctx.fill();
    if(F>0.02){ const g=ctx.createLinearGradient(b0,0,b1,0); g.addColorStop(0,'#93c5fd'); g.addColorStop(0.5,'#f59e0b'); g.addColorStop(1,'#dc2626'); ctx.fillStyle=g; rr(b0,by,Math.max(14,(b1-b0)*F/FMAX),14,7); ctx.fill(); }
    for(let b=0;b<=FMAX;b+=2) tx(String(b),b0+(b1-b0)*b/FMAX,by+28,10,C.sub,b===0?'left':(b===FMAX?'right':'center'),true);
    const M=msgs(); tx(M[0],x+12,y+88,12.5,C.ink,'left',true); tx(M[1],x+12,y+106,11.5,C.ink,'left',true); tx(M[2],x+12,y+124,11.5,C.sub,'left',true); }
  function stats(){ const vt=Vt(F), va=Va(F), M=MD[m], r=vt/40, pr=(F0+F)/F0, key=m+F.toFixed(2);
    if(key===lastKey) return; lastKey=key;
    sh('sA',vt.toFixed(1)+' mL',r>0.999?'もとの体積（40 mL）のまま':'もとの '+r.toFixed(2)+' 倍');
    sh('sB',F.toFixed(1)+' kg',F<0.05?'おしていない':F.toFixed(1)+' kgのものを持ち上げるくらい');
    sh('sC',M.a>0?Math.cbrt(va/M.a).toFixed(2)+' 倍':'空気なし',M.a>0?'空気の体積 '+va.toFixed(1)+' mL':'水の粒は間がつまっている');
    sh('sD',pr.toFixed(2)+' 倍','約 '+Math.round(101.3*pr)+' kPa（先生向け）');
    setShare(M.a>0?'【とじこめた空気と水】'+(M.w>0?'空気20 mL＋水20 mL':'空気40 mL')+'を'+F.toFixed(1)+' kgの力でおすと、中の体積は'+vt.toFixed(1)+' mLに。おしちぢめるほど手ごたえが大きくなる。水はおしちぢめられない｜シミュラボ'
      :'【とじこめた空気と水】水40 mLを'+F.toFixed(1)+' kgの力でおしても、体積は40 mLのまま。水はおしちぢめられない（空気はおしちぢめられる）｜シミュラボ'); }
  function draw(){ ctx.fillStyle=C.bg; ctx.fillRect(0,0,W,H); drawSyr(); drawGraph(); drawInfo(); }
  function setMode(v){ m=v; F=0; rel=false; drag=null; syncF(); initParts(); rec(); lastKey=''; stats(); }

  // ---------- 操作 ----------
  if(Q.has('m')&&MD[Q.get('m')]) $('m').value=Q.get('m');
  setMode($('m').value);
  if(Q.get('pre')==='1'){ const keep=m; ['air','water','half'].forEach(mm=>{ m=mm; for(let f=0;f<=FMAX;f+=1){ F=f; rec(); } }); m=keep; F=0; }
  if(Q.has('f')){ F=clamp(+Q.get('f')||0,0,FMAX); syncF(); rec(); lastKey=''; stats(); }
  $('m').addEventListener('change',()=>setMode($('m').value));
  $('f').addEventListener('input',()=>{ F=+$('f').value; rel=false; $('fL').textContent=F.toFixed(1)+' kg'; rec(); stats(); });
  $('rel').addEventListener('click',()=>{ if(F>0) rel=true; });
  $('clr').addEventListener('click',()=>{ recs={air:{},water:{},half:{}}; rec(); });
  cv.addEventListener('pointerdown',e=>{ const p=cpos(cv,e), x=p[0]/dpr, y=p[1]/dpr; if(x>250) return; drag={y0:y,f0:F,vt0:Vt(F)}; rel=false; try{ cv.setPointerCapture(e.pointerId); }catch(err){} });
  cv.addEventListener('pointermove',e=>{ if(!drag) return; const dy=cpos(cv,e)[1]/dpr-drag.y0;
    F=MD[m].a>0?fOfVt(drag.vt0-dy/PX):clamp(drag.f0+dy*0.06,0,FMAX); syncF(); rec(); stats(); });
  const up=()=>{ if(drag){ drag=null; if(F>0.05) rel=true; } };
  cv.addEventListener('pointerup',up); cv.addEventListener('pointercancel',up);
  function frame(t){ const dt=last?Math.min(0.05,(t-last)/1000):0; last=t; tNow+=dt;
    if(rel){ F*=Math.exp(-dt*4.5); if(F<0.03){ F=0; rel=false; } syncF(); stats(); }
    step(dt); draw(); requestAnimationFrame(frame); }
  for(let i=0;i<20;i++) step(1/60);
  draw(); requestAnimationFrame(frame);
'''

KUUKI_ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
<p>注射器にとじこめた空気をピストンでおすと、<b>体積は小さくなりますが、おし返す力（手ごたえ）は大きくなります</b>。おしちぢめるほど手ごたえは大きくなり、手をはなすとピストンはもとの位置にもどります。一方、とじこめた<b>水はおしちぢめられません</b>。強くおしても体積は変わりません。空気と水を半分ずつ入れると、空気の部分だけがちぢみます。粒のモデル図で、空気の粒どうしの間が小さくなる様子も見られます。</p>
''' + N('<b>対応する単元</b>：小学4年 A（1）空気と水の性質「（ア）閉じ込めた空気を圧すと，体積は小さくなるが，圧し返す力は大きくなること」「（イ）閉じ込めた空気は圧し縮められるが，水は圧し縮められないこと」。学習指導要領解説では、手ごたえなどの体感を基に調べること、力を加える前後の体積変化を図や絵で表現すること、空気と水の性質を利用したおもちゃや道具の仕組みを考えることが示されています。') + '''
<h2>授業での使い方</h2>
<h3>導入：おすとどうなるか予想する</h3>
<p>実際に注射器（または空気でっぽうのつつ）の空気をおしたあと、「中の空気はどうなっているのだろう」と問いかけます。このシミュレーターで、粒のモデル図を見ながら、体積が小さくなっても粒の数は変わらず、粒どうしの間がつまることを確かめます。ノートにかいた「空気の図」と比べさせると、考えを表現する活動につながります。</p>
<h3>展開：体積と手ごたえの関係を調べる</h3>
<p>スライダー（または注射器の図を指で下へなぞる）でおす力を少しずつ大きくし、中の体積（目もり）と手ごたえをグラフに記録します。「中身」を「水だけ」に切りかえると、いくらおしても目もりは40 mLのままで、グラフの点がまっすぐ上に並ぶことから、水はおしちぢめられないことがはっきりわかります。</p>
<h3>まとめ：空気と水を半分ずつ・身の回りの道具</h3>
<p>「空気と水（半分ずつ）」にすると、空気の部分だけがちぢみ、水の量（20 mL）は変わりません。最後に、空気でっぽう・ボール・自転車のタイヤなど、とじこめた空気の性質を利用した物の仕組みを説明させます。</p>
<h3>児童への問いの例</h3>
<ol>
<li>とじこめた空気をおすと、体積が小さくなった。中の空気の粒の数は、へったのだろうか？</li>
<li>空気をおしちぢめればおしちぢめるほど、手ごたえはどうなるだろう？手をはなすと、ピストンはどうなるだろう？</li>
<li>空気でっぽうの前の玉が勢いよく飛ぶのはなぜだろう？中に水を入れたら、玉は飛ぶだろうか？</li>
</ol>
<h2>しくみ・解説</h2>
<h3>言葉の意味（1文で）</h3>
<ul>
<li><b>とじこめた空気</b>とは、注射器やつつに入れて、出入りできないようにした空気のことです。</li>
<li><b>体積</b>とは、物がしめている場所の大きさのことで、注射器では目もり（mL）で読み取れます。</li>
<li><b>おし返す力（手ごたえ）</b>とは、おしちぢめられた空気が、もとの体積にもどろうとしてピストンをおし返す力のことです。</li>
<li><b>空気はおしちぢめられる</b>のは、空気の粒どうしの間にすき間があり、おすとその間が小さくなるからです。</li>
<li><b>水はおしちぢめられない</b>のは、水の粒どうしの間がつまっていて、ちぢむすき間がほとんどないからです。</li>
</ul>
<h3>体積と手ごたえの早見表（このシミュレーターの値）</h3>
''' + T([["40 mL（もと）", "0 kg", "1.00倍", "1.00倍"], ["35 mL", "約0.9 kg", "1.14倍", "0.96倍"], ["30 mL", "約2.1 kg", "1.33倍", "0.91倍"],
          ["25 mL", "約3.7 kg", "1.60倍", "0.86倍"], ["20 mL（もとの半分）", "約6.2 kg", "2.00倍", "0.79倍"], ["15 mL", "約10.3 kg", "2.67倍", "0.72倍"]],
         ["空気の体積", "手ごたえ（おす力）", "おし返す強さ（もとを1）", "粒の間かく（もとを1）"]) + '''
<p>注射器（中身40 mL・ピストンの断面積6 cm²）の空気を、ゆっくりおしたときの値です。体積がもとの半分になるまでおすと、約6 kgのものを持ち上げるくらいの力が必要になります。半分よりさらにちぢめようとすると、手ごたえは急に大きくなります。</p>
<h3>先生向けの補足：ボイルの法則</h3>
''' + N('温度が一定のとき、とじこめた気体の 圧力 p と 体積 V の積は一定（p × V ＝ 一定、ボイルの法則）<br>はじめ：大気圧 p₀ ≒ 101.3 kPa、体積 V₀ ＝ 40 mL<br>おす力 F のとき：p ＝ p₀ ＋ F ÷ A（A＝ピストンの断面積）、V ＝ V₀ × p₀ ÷ p<br>例：V ＝ 20 mL（半分）→ p ＝ 2 p₀ ≒ 203 kPa → F ＝ p₀ × A ≒ 101,325 Pa × 0.0006 m² ≒ 60.8 N（約6.2 kg重）') + '''
<p>このシミュレーターの「手ごたえ」は、ピストンをおす力を「kg重」（その重さのものを持ち上げるくらいの力）で表しています。1 kg重は約9.8 Nです。粒の間かくは、体積の3乗根（体積が半分なら約0.79倍）として計算しています。ボイルの法則は高校の物理で学ぶ内容で、小学4年では「おしちぢめるほど手ごたえが大きくなる」という関係をとらえることが目標です。</p>
<h3>水は本当に少しもちぢまない？</h3>
<p>実際の水も、ものすごく大きな力を加えるとほんのわずかにちぢみますが、その量はとても小さく、このシミュレーターの最大の力（12 kg）でおしても、40 mLの水は約0.004 mLしかちぢみません。注射器の目もりではまったく読み取れないので、「水はおしちぢめられない」と考えてよいのです。</p>
<h3>空気でっぽうの玉が飛ぶしくみ</h3>
<p>空気でっぽうは、つつの前と後ろを玉（前玉・後ろ玉）でふさいで、空気をとじこめた道具です。おしぼうで後ろ玉をおしこむと、とじこめた空気がおしちぢめられ、おし返す力が大きくなります。その力が、前玉をつつにとめている力より大きくなったとき、前玉が勢いよくおし出されて飛びます。つつの中に水を入れると、水はおしちぢめられないので、おし返す力をためることができず、前玉は勢いよくは飛びません（水がおし出されるだけです）。</p>
<h3>身の回りの「とじこめた空気」</h3>
''' + T([["ボール", "中の空気がおしちぢめられ、おし返す力ではずむ"], ["自転車・自動車のタイヤ", "おしちぢめた空気で重さを支え、でこぼこの衝撃をやわらげる"],
          ["エアーマット・プチプチ（緩衝材）", "空気のおし返す力で、物をやさしく受け止める"], ["空気でっぽう・ペットボトルロケット", "おしちぢめた空気がもとにもどろうとする力で、玉や水を飛ばす"]],
         ["道具", "空気の性質の使い方"]) + '''
<h3>このシミュレーションで単純化していること</h3>
<ul>
<li>温度は変わらないものとしています。実際には、空気を速くおしちぢめると少しあたたかくなり、手ごたえが計算より少し大きくなります（ゆっくりおすと、この表の値に近くなります）。</li>
<li>ピストンと注射器の間のまさつや、空気のもれは考えていません。実際の注射器では、まさつがあるため、手をはなしてもぴったりもとの位置まではもどらないことがあります。</li>
<li>空気の粒（30こ）と水の粒の数・大きさは模式的です。実際の粒はとても小さく、数もけた違いに多くあります。空気の粒の図は平面にかいていますが、統計欄の「粒の間かく」は立体で考えた値です。</li>
<li>「水だけ」で指をなぞったときの手ごたえは、おしこもうとした量に合わせて大きくなるようにしています（ピストンは動きません）。</li>
</ul>
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「小学校学習指導要領（平成29年告示）解説 理科編」第4学年 A（1）空気と水の性質（''' + A(MEXT_SHO, "小学校学習指導要領解説") + '''）</li>
<li>小学校理科の教科書（第4学年「とじこめた空気と水」の単元）</li>
<li>国立天文台 編『理科年表』（標準大気圧 101.325 kPa、水の圧縮率 約4.6×10⁻¹⁰ /Pa）</li>
</ul>
'''

sim(slug="kuuki-mizu", cat="rika", emoji="💉", score=80,
    title="とじこめた空気と水のシミュレーター（注射器をおすと）",
    title_tag="とじこめた空気と水のシミュレーター｜注射器をおすと体積と手ごたえはどう変わる？（小4理科 空気と水の性質）",
    meta_desc="注射器にとじこめた空気をおすと体積は小さくなり、おし返す力（手ごたえ）は大きくなる。水はおしちぢめられない。体積と手ごたえのグラフ、空気の粒の間かくのモデル図で確かめる小4理科「空気と水の性質」の無料シミュレーター。空気でっぽうの仕組みも解説。",
    og_title="とじこめた空気と水のシミュレーター（注射器をおすと）",
    og_desc="空気はおしちぢめられ、おすほど手ごたえが大きい。水はおしちぢめられない。注射器と粒のモデル、体積と手ごたえのグラフで確かめる小4理科。",
    card_desc="注射器の空気をおすと体積は小さく、手ごたえは大きく。水はおしちぢめられない。粒のモデルとグラフで。",
    lead="注射器に空気・水・半分ずつを入れて、ピストンを指でおしてみましょう。空気は体積が小さくなり、おすほど手ごたえ（おし返す力）が大きくなります。水はいくらおしても体積が変わりません。中の粒のようすと、体積と手ごたえのグラフを同時に確かめられます。",
    model="小4 空気と水の性質",
    level="小学4年",
    unit="小学校 第4学年 A（1）空気と水の性質",
    canvas=canvas(640, 440, light=True),
    controls=select("m", "注射器の中身", [("air", "空気だけ（40 mL）"), ("water", "水だけ（40 mL）"), ("half", "空気と水（20 mLずつ）")])
           + slider("f", "ピストンをおす力", 0, 12, 0, 0.1, "{v} kg"),
    buttons=btn("rel", "✋ 手をはなす", True) + btn("clr", "グラフの記録を消す"),
    stats=stats([("sA", "中の体積（目もり）", False), ("sB", "手ごたえ（おし返す力）", True), ("sC", "空気の粒の間かく", False), ("sD", "おし返す強さ（もとを1）", False)]),
    legend="左：先をゴム板におしつけた注射器（青い粒＝空気、緑の粒＝水。粒の数は模式的。点線＝ピストンのもとの位置）。注射器の図を指で下へなぞるとおせて、指をはなすともどります。スライダーでおすと、その力でおし続けます。右上：中の体積と手ごたえのグラフ（中身ごとに色を変えて記録）。手ごたえは「その重さのものを持ち上げるくらいの力」で表しています。",
    article=KUUKI_ARTICLE,
    faqs=[("とじこめた空気をおすと、体積と手ごたえはどうなりますか？", "体積は小さくなり、おし返す力（手ごたえ）は大きくなります。おしちぢめるほど手ごたえは大きくなり、手をはなすと、空気がおし返してピストンはもとの位置にもどります。"),
          ("水はなぜおしちぢめられないのですか？", "水の粒どうしの間がつまっていて、ちぢむすき間がほとんどないからです。空気は粒どうしの間にすき間が多いので、おすとその間が小さくなり、体積が小さくなります。"),
          ("空気をおしちぢめると、空気の量（粒の数）はへりますか？", "へりません。とじこめているので、空気は出入りしていません。粒の数は同じまま、粒どうしの間が小さくなって体積が小さくなります。"),
          ("空気と水を半分ずつ入れておすと、どうなりますか？", "空気の部分だけがちぢみ、水の体積は変わりません。たとえば空気20 mLと水20 mLなら、水は20 mLのままで、空気だけが小さくなります。"),
          ("空気でっぽうの玉が飛ぶのはなぜですか？", "後ろ玉をおすと、つつの中にとじこめた空気がおしちぢめられ、おし返す力が大きくなります。その力が前玉をとめている力より大きくなると、前玉がおし出されて勢いよく飛びます。"),
          ("体積と手ごたえには、きまった関係がありますか？", "温度が変わらなければ、空気の体積を半分にすると、中の空気がおし返す強さ（圧力）は2倍になります（ボイルの法則：圧力×体積＝一定）。このシミュレーターの注射器では、半分にするのに約6 kgのものを持ち上げるくらいの力が必要です。")],
    rel=[("joutai-henka", "🧊", "状態変化と粒子のシミュレーター"), ("suiatsu-fuyuu", "🌊", "水圧と浮力のシミュレーター"),
         ("teko-tsuriai", "⚖️", "てこのつり合いシミュレーター"), ("diffusion", "🫧", "拡散シミュレーター"), ("kiatsu-jet", "🎢", "気圧ジェットコースター指数")],
    js=JS_KUUKI)
