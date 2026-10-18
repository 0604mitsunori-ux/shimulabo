# -*- coding: utf-8 -*-
"""理科の授業向けシミュ（小学3年）
   mono-omosa … 小3「物と重さ」（A（1））
   kaze-gomu  … 小3「風とゴムの力の働き」（A（2））"""
import math
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

MEXT_SHO = "https://www.mext.go.jp/a_menu/shotou/new-cs/1387014.htm"
def A(url, label): return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, label)

# 2本で共通の描画ヘルパー（JS）
HELP = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const FF='"Hiragino Sans","Hiragino Kaku Gothic ProN","Noto Sans JP","Yu Gothic UI","Yu Gothic",Meiryo,sans-serif';
  const h1=document.querySelector('.sim-head h1'); if(h1&&!h1.children.length){ const t0=h1.textContent, i0=t0.indexOf('（'); if(i0>0){ h1.textContent=t0.slice(0,i0); const sp=document.createElement('span'); sp.style.display='inline-block'; sp.textContent=t0.slice(i0); h1.appendChild(sp); } }
  function tx(s,x,y,size,col,align,bold,maxW){ let z=size; ctx.font=(bold?'bold ':'')+z+'px '+FF; if(maxW){ while(ctx.measureText(s).width>maxW&&z>8){ z-=0.5; ctx.font=(bold?'bold ':'')+z+'px '+FF; } } ctx.fillStyle=col; ctx.textAlign=align||'left'; ctx.fillText(s,x,y); ctx.textAlign='left'; }
  function tw(s,size,bold){ ctx.font=(bold?'bold ':'')+size+'px '+FF; return ctx.measureText(s).width; }
  function rr(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
  function panel(x,y,w,h){ ctx.fillStyle='#fff'; ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1.2; rr(x,y,w,h,10); ctx.fill(); ctx.stroke(); }
  function tag(s,x,y,size,col,align){ const w=tw(s,size,true), x0=align==='right'?x-w:align==='center'?x-w/2:x; ctx.fillStyle='rgba(255,255,255,0.94)'; rr(x0-5,y-size-2,w+10,size+8,6); ctx.fill(); ctx.strokeStyle=col; ctx.lineWidth=1.2; ctx.stroke(); tx(s,x0,y,size,col,'left',true); }
  function dot(x,y,r,fill,stroke){ ctx.fillStyle=fill; ctx.beginPath(); ctx.arc(x,y,r,0,6.2832); ctx.fill(); if(stroke){ ctx.strokeStyle=stroke; ctx.lineWidth=1.2; ctx.stroke(); } }
  function line(x1,y1,x2,y2){ ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2,y2); ctx.stroke(); }
  const K=id=>$(id).previousElementSibling;
  const SH0={};
  function sh(id,m,sub){ const e=$(id); if(!e) return; const v=m+'|'+(sub||''); if(SH0[id]===v) return; SH0[id]=v; e.style.fontSize=m.length>7?'15px':(m.length>5?'17px':''); e.innerHTML=m+(sub?'<span style="display:block;font-size:12px;font-weight:700;color:#59616c;margin-top:2px">'+sub+'</span>':''); }
  function lab(id,s){ const k=K(id); if(k&&k.textContent!==s) k.textContent=s; }
  function show(id,on){ const e=$(id); if(e) e.style.display=on?'':'none'; }
  function showF(id,on){ const e=$(id), f=e?e.closest('.field'):null; if(f) f.style.display=on?'':'none'; }
  const Q=new URLSearchParams(location.search);
'''

# ============================================================ 1 物と重さ
V_CUBE = 27  # 1辺3cmの立方体（cm³）
BLOCKS = [("木", 0.5), ("プラスチック（アクリル）", 1.19), ("ゴム", 1.3), ("ガラス", 2.5),
          ("アルミニウム", 2.70), ("鉄", 7.87), ("どう（銅）", 8.96)]
BW = {n: round(r * V_CUBE, 1) for n, r in BLOCKS}
FOIL_G = round(30 * 100 * 0.0011 * 2.70, 1)   # 30cm×1m・厚さ11µm のアルミはく → 8.9 g

JS_OMOSA = HELP + r'''
  const C={bg:'#f8fafc',ink:'#0f172a',sub:'#64748b',red:'#dc2626',blue:'#2563eb',green:'#15803d'};
  // 同じ大きさのブロック：1辺3cmの立方体（体積27 cm³）。重さ＝1cm³あたりの重さ（密度）×27
  const V=27, BS=44;
  const BL=[{id:'ki',nm:'木',sn:'木',rho:0.5,f:'#e7c08a',e:'#a16207',t:'#5b3a17'},
    {id:'pura',nm:'プラスチック',sn:'プラ',rho:1.19,f:'#bfdbfe',e:'#2563eb',t:'#1e3a8a'},
    {id:'gomu',nm:'ゴム',sn:'ゴム',rho:1.3,f:'#3f3f46',e:'#18181b',t:'#f4f4f5'},
    {id:'garasu',nm:'ガラス',sn:'ガラス',rho:2.5,f:'#cffafe',e:'#0891b2',t:'#155e75'},
    {id:'arumi',nm:'アルミニウム',sn:'アルミ',rho:2.70,f:'#e5e7eb',e:'#6b7280',t:'#374151'},
    {id:'tetsu',nm:'鉄',sn:'鉄',rho:7.87,f:'#6b7280',e:'#374151',t:'#f9fafb'},
    {id:'dou',nm:'どう',sn:'どう',rho:8.96,f:'#c2703d',e:'#7c2d12',t:'#fff7ed'}];
  const BY={}; BL.forEach(b=>{ b.g=Math.round(b.rho*V*10)/10; BY[b.id]=b; });
  const SHP={clay:{M:100,nm:'ねん土',list:[['maru','⚪ 丸める','丸めた'],['taira','🥞 平らにする','平らにした'],['himo','〰️ ほそ長くする','ほそ長くした'],['bara','🔹 細かく分ける','細かく分けた']],pcs:[24,20,18,15,13,10]},
             foil:{M:8.9,nm:'アルミはく',list:[['hiro','📄 広げる','広げた'],['maru','⚪ 丸める','丸めた'],['tatamu','📐 おりたたむ','おりたたんだ'],['bara','🔹 細かくちぎる','細かくちぎった']],pcs:[1.6,1.4,1.3,1.2,1.1,0.9,0.8,0.6]}};
  let m='clay', kd='dial', shp='maru', anim=null, off=[], offOrd=[], recS={}, rd=0, hits=[], tNow=0, last=0;
  let place={L:'ki',R:'tetsu',S:null}, recB={}, th=0, om=0, drag=null;
  const KN={dial:'自動上皿はかり',dig:'デジタルはかり'};
  const fmtG=(g)=>kd==='dial'?(Math.round(g)+' g'):(g.toFixed(1)+' g');
  const fmt1=(g)=>(Math.round(g*10)/10).toFixed(1)+' g';
  const ease=(t)=>t<0?0:t>1?1:t*t*(3-2*t);
  const S=()=>SHP[m];
  function shpName(k){ const it=S().list.find(a=>a[0]===k); return it?it[2]:''; }
  function massOn(){ if(shp!=='bara') return S().M; let g=0; S().pcs.forEach((p,i)=>{ if(!off[i]) g+=p; }); return Math.round(g*10)/10; }

  // ---------- ブロック（立方体）
  function block(b,cx,by,s,alpha){ s=s||BS; const x=cx-s/2, y=by-s, d=s*0.17; ctx.save(); if(alpha!=null) ctx.globalAlpha=alpha;
    ctx.strokeStyle=b.e; ctx.lineWidth=1.3;
    ctx.beginPath(); ctx.moveTo(x,y); ctx.lineTo(x+d,y-d); ctx.lineTo(x+s+d,y-d); ctx.lineTo(x+s,y); ctx.closePath(); ctx.fillStyle=b.f; ctx.fill(); ctx.fillStyle='rgba(255,255,255,.35)'; ctx.fill(); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(x+s,y); ctx.lineTo(x+s+d,y-d); ctx.lineTo(x+s+d,y+s-d); ctx.lineTo(x+s,y+s); ctx.closePath(); ctx.fillStyle=b.f; ctx.fill(); ctx.fillStyle='rgba(0,0,0,.2)'; ctx.fill(); ctx.stroke();
    ctx.fillStyle=b.f; ctx.fillRect(x,y,s,s);
    if(b.id==='ki'){ ctx.strokeStyle='rgba(146,64,14,.35)'; ctx.lineWidth=1; for(let k=1;k<4;k++){ ctx.beginPath(); ctx.moveTo(x+2,y+k*s/4); ctx.quadraticCurveTo(x+s/2,y+k*s/4+(k%2?3:-3),x+s-2,y+k*s/4); ctx.stroke(); } }
    if(['arumi','tetsu','dou'].indexOf(b.id)>=0){ const g=ctx.createLinearGradient(x,y,x+s,y+s); g.addColorStop(0,'rgba(255,255,255,.45)'); g.addColorStop(0.5,'rgba(255,255,255,0)'); g.addColorStop(1,'rgba(255,255,255,.15)'); ctx.fillStyle=g; ctx.fillRect(x,y,s,s); }
    if(b.id==='garasu'||b.id==='pura'){ ctx.strokeStyle='rgba(255,255,255,.9)'; ctx.lineWidth=3; line(x+6,y+s-8,x+s-14,y+6); }
    ctx.strokeStyle=b.e; ctx.lineWidth=1.3; ctx.strokeRect(x,y,s,s);
    tx(b.sn,cx,y+s/2+5*s/44,Math.round(14*s/44),b.t,'center',true,s-4);
    ctx.restore(); }

  // ---------- はかり（自動上皿はかり／デジタル）。py＝皿の上面。下の端のyを返す
  function scaleDraw(cx,py,s,val){ let bottom;
    ctx.strokeStyle='#64748b'; ctx.lineWidth=1.5;
    if(kd==='dial'){ const by=py+18*s, bh=130*s; ctx.fillStyle='#e2e8f0'; rr(cx-75*s,by,150*s,bh,12*s); ctx.fill(); ctx.stroke();
      const dc=by+64*s, R=52*s; ctx.fillStyle='#fff'; ctx.beginPath(); ctx.arc(cx,dc,R,0,7); ctx.fill(); ctx.strokeStyle='#334155'; ctx.lineWidth=2; ctx.stroke();
      for(let g=0; g<500; g+=10){ const a=-Math.PI/2+2*Math.PI*g/500, big=g%100===0, mid=g%50===0, l=big?10*s:(mid?7*s:4*s);
        ctx.strokeStyle=big?'#0f172a':'#64748b'; ctx.lineWidth=big?1.8:1; line(cx+Math.cos(a)*(R-2),dc+Math.sin(a)*(R-2),cx+Math.cos(a)*(R-2-l),dc+Math.sin(a)*(R-2-l));
        if(big) tx(String(g),cx+Math.cos(a)*(R-23*s),dc+Math.sin(a)*(R-23*s)+4*s,10.5*s,'#0f172a','center',true); }
      tx('g',cx,dc-12*s,10*s,C.sub,'center',true);
      const a=-Math.PI/2+2*Math.PI*clamp(val,0,500)/500; ctx.strokeStyle=C.red; ctx.lineWidth=2.4*s; ctx.lineCap='round'; line(cx-Math.cos(a)*7*s,dc-Math.sin(a)*7*s,cx+Math.cos(a)*(R-6*s),dc+Math.sin(a)*(R-6*s)); ctx.lineCap='butt';
      dot(cx,dc,4*s,'#334155'); bottom=by+bh; }
    else { const by=py+18*s, bh=58*s; ctx.fillStyle='#e2e8f0'; rr(cx-75*s,by,150*s,bh,10*s); ctx.fill(); ctx.stroke();
      ctx.fillStyle='#d9e7c9'; rr(cx-58*s,by+11*s,116*s,36*s,5*s); ctx.fill(); ctx.strokeStyle='#475569'; ctx.lineWidth=1.2; ctx.stroke();
      tx(Math.max(0,val).toFixed(1),cx+30*s,by+39*s,26*s,'#1f2937','right',true); tx('g',cx+36*s,by+39*s,14*s,'#1f2937','left',true); bottom=by+bh; }
    ctx.fillStyle='#94a3b8'; ctx.fillRect(cx-8*s,py+6*s,16*s,12*s);
    ctx.fillStyle='#cbd5e1'; ctx.strokeStyle='#64748b'; ctx.lineWidth=1.3; rr(cx-65*s,py,130*s,7*s,3*s); ctx.fill(); ctx.stroke();
    return bottom; }

  // ---------- ねん土・アルミはく
  function grad(x,y,r,c0,c1){ const g=ctx.createRadialGradient(x-r*0.35,y-r*0.35,r*0.15,x,y,r*1.1); g.addColorStop(0,c0); g.addColorStop(1,c1); return g; }
  function clayBall(x,by,r){ ctx.fillStyle=grad(x,by-r,r,'#fcc9a1','#e2864a'); ctx.beginPath(); ctx.ellipse(x,by-r*0.96,r*1.03,r*0.96,0,0,7); ctx.fill(); ctx.strokeStyle='#b45f2a'; ctx.lineWidth=1.2; ctx.stroke(); }
  function foilBit(x,y,r,seed){ ctx.beginPath(); const n=11; for(let k=0;k<n;k++){ const a=k/n*6.283, q=r*(0.78+0.22*Math.abs(Math.sin(seed*7.3+k*2.1))); const px=x+Math.cos(a)*q, py=y+Math.sin(a)*q; if(k) ctx.lineTo(px,py); else ctx.moveTo(px,py); } ctx.closePath();
    ctx.fillStyle=grad(x,y,r,'#ffffff','#a3aab5'); ctx.fill(); ctx.strokeStyle='#6b7280'; ctx.lineWidth=1; ctx.stroke(); ctx.strokeStyle='rgba(100,116,139,.5)'; line(x-r*0.4,y-r*0.2,x+r*0.3,y+r*0.3); }
  const CPOS=[[-52,0],[-17,0],[17,0],[51,0],[-34,1],[34,1]], FPOS=[[-56,0],[-30,0],[-4,0],[22,0],[48,0],[-42,1],[-14,1],[14,1]];
  function pieceR(i){ return m==='clay'?30*Math.cbrt(S().pcs[i]/100):9*Math.sqrt(S().pcs[i]/1.0); }
  function deskPos(k,deskY,i){ const r=pieceR(i), col=k%3, row=Math.floor(k/3); return [28+col*30, deskY-r-row*30]; }
  function drawObj(k,cx,by,alpha,deskY,hit){ ctx.save(); ctx.globalAlpha=alpha;
    if(m==='clay'){
      if(k==='maru') clayBall(cx,by,32);
      else if(k==='taira'){ ctx.fillStyle=grad(cx,by-10,70,'#fcc9a1','#e2864a'); rr(cx-72,by-15,144,15,7.5); ctx.fill(); ctx.strokeStyle='#b45f2a'; ctx.lineWidth=1.2; ctx.stroke(); }
      else if(k==='himo'){ ctx.lineCap='round'; ctx.strokeStyle='#b45f2a'; ctx.lineWidth=14; ctx.beginPath(); for(let x=-82;x<=82;x+=4){ const y=by-7-3*Math.sin(x/11); if(x===-82) ctx.moveTo(cx+x,y); else ctx.lineTo(cx+x,y); } ctx.stroke(); ctx.strokeStyle='#ec9a62'; ctx.lineWidth=11; ctx.stroke(); ctx.strokeStyle='rgba(255,220,190,.7)'; ctx.lineWidth=3; ctx.beginPath(); for(let x=-80;x<=80;x+=4){ const y=by-10-3*Math.sin(x/11); if(x===-80) ctx.moveTo(cx+x,y); else ctx.lineTo(cx+x,y); } ctx.stroke(); ctx.lineCap='butt'; }
      else { let ko=0; const ord=offOrd.slice(); S().pcs.forEach((p,i)=>{ const r=pieceR(i); let x,y;
          if(off[i]&&deskY){ const q=deskPos(ord.indexOf(i),deskY,i); x=q[0]; y=q[1]; } else { const P=CPOS[i]; x=cx+P[0]; y=P[1]?by-30-r*0.75:by-r; }
          clayBall(x,y+r,r); if(hit) hits.push({i:i,x:x,y:y,r:r+6}); }); } }
    else {
      if(k==='hiro'){ ctx.beginPath(); ctx.moveTo(cx-95,by+11); ctx.lineTo(cx-76,by); ctx.lineTo(cx+76,by); ctx.lineTo(cx+95,by+11); ctx.lineTo(cx+95,by+8); ctx.lineTo(cx+76,by-3); ctx.lineTo(cx-76,by-3); ctx.lineTo(cx-95,by+8); ctx.closePath();
        const g=ctx.createLinearGradient(cx-95,0,cx+95,0); g.addColorStop(0,'#cbd5e1'); g.addColorStop(0.4,'#ffffff'); g.addColorStop(1,'#9ca3af'); ctx.fillStyle=g; ctx.fill(); ctx.strokeStyle='#6b7280'; ctx.lineWidth=1; ctx.stroke(); tx('30cm×1m',cx,by-8,11,C.sub,'center',true); }
      else if(k==='maru') foilBit(cx,by-25,26,1);
      else if(k==='tatamu'){ ctx.fillStyle='#e5e7eb'; ctx.strokeStyle='#6b7280'; ctx.lineWidth=1; for(let j=0;j<4;j++){ rr(cx-34+j,by-4-j*3.4,68,4,1.5); ctx.fill(); ctx.stroke(); } }
      else { S().pcs.forEach((p,i)=>{ const r=pieceR(i); let x,y;
          if(off[i]&&deskY){ const q=deskPos(offOrd.indexOf(i),deskY,i); x=q[0]; y=q[1]; } else { const P=FPOS[i]; x=cx+P[0]; y=P[1]?by-r-16:by-r*0.8; }
          foilBit(x,y,r,i+1); if(hit) hits.push({i:i,x:x,y:y,r:r+8}); }); } }
    ctx.restore(); }

  // ---------- 形をかえるモード
  const SC={cx:200,py:250,s:1.15};
  function drawShape(dt){ const M=S();
    panel(8,8,330,424); tx(M.nm+'の形をかえて、重さをはかる',20,30,14,C.ink,'left',true,306);
    ctx.fillStyle='#f0f9ff'; rr(20,42,306,62,10); ctx.fill(); ctx.strokeStyle='#bae6fd'; ctx.stroke();
    tx(KN[kd]+'の目もり',34,66,12.5,'#0369a1','left',true); tx(fmtG(rd),312,94,32,C.ink,'right',true);
    if(kd==='dial'&&m==='foil') tx('目もりが小さくて読みにくい',34,94,10.5,C.red,'left',true);
    const bottom=scaleDraw(SC.cx,SC.py,SC.s,rd);
    ctx.fillStyle='#e7d3b1'; ctx.fillRect(9,bottom,328,Math.max(0,431-bottom)); ctx.strokeStyle='#b08d57'; ctx.lineWidth=2; line(9,bottom,337,bottom);
    hits=[]; const by=SC.py;
    if(anim){ const t=anim.t, lift=t<0.35?ease(t/0.35):(t<0.85?1:1-ease((t-0.85)/0.35)), y=by-46*lift;
      if(t<0.35) drawObj(anim.from,SC.cx,y,1,null,false);
      else if(t<0.85){ const a=(t-0.35)/0.5; drawObj(anim.from,SC.cx,y,1-a,null,false); drawObj(anim.to,SC.cx,y,a,null,false); }
      else drawObj(anim.to,SC.cx,y,1,null,false);
      if(t>0.2&&t<1.05) tag('形をかえています…',SC.cx,128,12,'#0369a1','center'); }
    else drawObj(shp,SC.cx,by,1,bottom,true);
    if(!anim&&shp==='bara'){ tx('かけらをタップすると、はかりの外に出せるよ',172,126,11.5,'#0e7490','center',true,300); }
    // 記ろく（表）
    const x=346, w=286; panel(x,8,w,424); tx('記ろく（表）',x+12,30,14,C.ink,'left',true); tx(M.nm+'　はじめ '+fmt1(M.M),x+w-12,30,11.5,C.sub,'right',true);
    const ty=44; ctx.fillStyle='#f1f5f9'; ctx.fillRect(x+10,ty,w-20,26); tx('形',x+22,ty+18,12.5,C.sub,'left',true); tx('重さ',x+w-24,ty+18,12.5,C.sub,'right',true);
    M.list.forEach((it,i)=>{ const y=ty+26+i*38, cur=it[0]===shp&&!anim, v=recS[it[0]];
      if(cur){ ctx.fillStyle='#ecfeff'; ctx.fillRect(x+10,y,w-20,38); }
      ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; line(x+10,y+38,x+w-10,y+38);
      tx(it[2],x+22,y+25,15,C.ink,'left',true);
      if(v!=null) tx(fmt1(v),x+w-24,y+26,17,Math.abs(v-M.M)<0.05?C.green:C.red,'right',true); else tx('まだ',x+w-24,y+25,13,'#94a3b8','right',true); });
    // まとめのことば
    const my=ty+26+4*38+14; ctx.fillStyle='#f8fafc'; rr(x+10,my,w-20,432-my-10,10); ctx.fill(); ctx.strokeStyle='#e2e8f0'; ctx.stroke();
    const L=msgShape(); L.forEach((s,i)=>tx(s[0],x+22,my+28+i*27,s[2]||14,s[1]||C.ink,'left',true,w-44)); }
  function msgShape(){ const M=S(), n=Object.keys(recS).length, same=Object.keys(recS).every(k=>Math.abs(recS[k]-M.M)<0.05), nOff=off.filter(Boolean).length;
    if(anim) return [['はかりから下ろして、',C.ink],['形をかえています。',C.ink],['はかりの目もりは 0 g に',C.sub],['もどったよ。',C.sub]];
    if(shp==='bara'&&nOff>0) return [['かけらが '+nOff+'こ、はかりの外にある。',C.red],['のっている分だけ：'+fmt1(massOn()),C.ink],['全部のせてはかると',C.ink],['何gになるかな？',C.ink]];
    if(n>=2&&same) return [['形をかえても、',C.green,17],['重さはかわらない！',C.green,17],['どの形でも '+fmt1(M.M)+'。',C.ink],['（全部のせてはかったとき）',C.sub,12.5]];
    return [['ボタンをおして、形を',C.ink],['かえてみよう。',C.ink],['重くなる？軽くなる？',C.blue],['かわらない？ 予想しよう。',C.blue]]; }

  // ---------- 同じ大きさでくらべるモード
  const TR={y:34}, BAL={cx:194,py:236,L:116}, SB={cx:510,py:194,s:0.75};
  function trayX(i){ return 8+624/7*(i+0.5); }
  function where(id){ for(const k of ['L','R','S']) if(place[k]===id) return k; return null; }
  function panPos(k){ const c=Math.cos(th), s=Math.sin(th), sg=k==='L'?-1:1; return [BAL.cx+sg*BAL.L*c, BAL.py+sg*BAL.L*s-26]; }
  function balTxt(){ const a=place.L&&BY[place.L], b=place.R&&BY[place.R];
    if(!a&&!b) return ['からっぽ','両方の皿にのせよう',C.sub];
    if(!a||!b) return [(a?'左':'右')+'がさがる',(a||b).nm+'だけ',C.sub];
    if(Math.abs(a.g-b.g)<0.05) return ['つり合う','同じ重さ',C.green];
    const hv=a.g>b.g?a:b; return [(a.g>b.g?'左':'右')+'（'+hv.nm+'）が重い',a.nm+' と '+b.nm,C.red]; }
  function drawBlocks(dt){
    // トレイ
    panel(8,8,624,96); tx('同じ大きさのブロック（1辺3cmの立方体）　指でてんびん・はかりへ運ぼう',20,24,12,C.ink,'left',true,600);
    BL.forEach((b,i)=>{ const x=trayX(i); if(where(b.id)||(drag&&drag.id===b.id)){ ctx.setLineDash([4,3]); ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1.2; ctx.strokeRect(x-BS/2,82-BS,BS,BS); ctx.setLineDash([]); } else block(b,x,82,BS);
      tx(b.nm,x,98,11,C.sub,'center',true,84); });
    // てんびん
    panel(8,110,372,196); tx('てんびん',20,132,13.5,C.ink,'left',true); const bt=balTxt(); tx('→ '+bt[0],86,132,14,bt[2],'left',true,200);
    const cx=BAL.cx, py=BAL.py, c=Math.cos(th), s=Math.sin(th), L=BAL.L;
    ctx.fillStyle='#475569'; rr(cx-90,290,180,10,4); ctx.fill(); ctx.fillStyle='#94a3b8'; ctx.fillRect(cx-6,py,12,290-py);
    ctx.strokeStyle='#64748b'; ctx.lineWidth=1.2; for(let k=-2;k<=2;k++) line(cx+k*9,280,cx+k*9,k===0?272:276);
    ctx.strokeStyle='#334155'; ctx.lineWidth=7; ctx.lineCap='round'; line(cx-L*c,py-L*s,cx+L*c,py+L*s); ctx.lineCap='butt';
    ['L','R'].forEach(k=>{ const sg=k==='L'?-1:1, ex=cx+sg*L*c, ey=py+sg*L*s; ctx.fillStyle='#64748b'; ctx.fillRect(ex-3,ey-24,6,24);
      const pp=panPos(k); ctx.fillStyle='#cbd5e1'; ctx.strokeStyle='#64748b'; ctx.lineWidth=1.3; rr(pp[0]-46,pp[1]-4,92,7,3); ctx.fill(); ctx.stroke();
      if(place[k]) block(BY[place[k]],pp[0],pp[1]-4,BS); else tx(k==='L'?'左の皿':'右の皿',pp[0],pp[1]-14,11,'#94a3b8','center',true); });
    const pl=50; ctx.strokeStyle=C.red; ctx.lineWidth=2.2; line(cx,py,cx-pl*s,py+pl*c); dot(cx,py,5,'#1f2937');
    // はかり
    panel(388,110,244,196); tx('はかり',400,132,13.5,C.ink,'left',true); tx(KN[kd],400,150,10.5,C.sub,'left',true); tx(fmtG(rd),620,140,20,C.ink,'right',true);
    scaleDraw(SB.cx,SB.py,SB.s,rd); if(place.S) block(BY[place.S],SB.cx,SB.py,BS); else tx('ここにのせる',SB.cx,SB.py-12,11,'#94a3b8','center',true);
    // 重いじゅん
    panel(8,312,624,120); const ks=Object.keys(recB).sort((a,b)=>BY[b].g-BY[a].g);
    tx('はかった重さ（重いじゅん）',20,332,13,C.ink,'left',true); tx(ks.length+' / 7こ',620,332,12,C.sub,'right',true);
    if(!ks.length) tx('ブロックをはかりにのせると、ここに重いじゅんにならぶよ',320,384,13,'#94a3b8','center',true,580);
    ks.forEach((id,k)=>{ const b=BY[id], col=k<4?0:1, row=k%4, x=col?328:16, y=342+row*22;
      dot(x+9,y+9,8,k===0?'#f59e0b':'#e2e8f0'); tx(String(k+1),x+9,y+13,10.5,k===0?'#fff':C.ink,'center',true);
      tx(b.nm,x+22,y+14,11.5,C.ink,'left',true,72); const bw=Math.max(3,150*b.g/250); ctx.fillStyle=b.f; rr(x+98,y+3,bw,13,3); ctx.fill(); ctx.strokeStyle=b.e; ctx.lineWidth=1; ctx.stroke();
      tx(fmt1(b.g),x+102+bw,y+14,11.5,C.ink,'left',true); });
    if(drag&&drag.moved) block(BY[drag.id],drag.x,drag.y+BS/2,BS,0.85); }

  // ---------- 統計・シェア
  function stats(){ if(m!=='block'){ const M=S(), done=!anim&&Math.abs(rd-massOn())<0.06, n=Object.keys(recS).length;
      lab('s1','はかりの目もり'); lab('s2','いまの形'); lab('s3','はじめの重さとのちがい'); lab('s4','調べた形');
      sh('s1',fmtG(rd),KN[kd]); sh('s2',anim?'かえている…':shpName(shp),M.nm);
      const df=massOn()-M.M; sh('s3',anim||!done?'はかり中…':(Math.abs(df)<0.05?'0 g（同じ）':(df>0?'+':'−')+Math.abs(df).toFixed(1)+' g'),anim||!done?'':(Math.abs(df)<0.05?'形をかえても同じ':'外にかけらがある'));
      sh('s4',n+' / 4',n>=2&&Object.keys(recS).every(k=>Math.abs(recS[k]-M.M)<0.05)?'どれも '+fmt1(M.M):'形をかえてはかろう');
      const gs=(M.M%1?M.M.toFixed(1):String(M.M))+'g'; setShare('【物と重さ】'+M.nm+gs+'を'+M.list.map(a=>a[2].replace(/た$/,'ても').replace(/だ$/,'でも')).join('・')+'、重さは'+gs+'のまま。物は形をかえても重さはかわらない｜シミュラボ'); }
    else { const bt=balTxt(), ks=Object.keys(recB).sort((a,b)=>BY[b].g-BY[a].g);
      lab('s1','はかりの目もり'); lab('s2','てんびん'); lab('s3','いちばん重い物'); lab('s4','はかった物');
      sh('s1',fmtG(rd),place.S?BY[place.S].nm+'（1辺3cm）':'何ものっていない'); sh('s2',bt[0],bt[1]);
      sh('s3',ks.length?BY[ks[0]].nm+' '+fmt1(BY[ks[0]].g):'まだ',ks.length>1?'いちばん軽い：'+BY[ks[ks.length-1]].nm+' '+fmt1(BY[ks[ks.length-1]].g):'はかりにのせよう');
      const big=ks.length?BY[ks[0]]:null, sm=ks.length?BY[ks[ks.length-1]]:null;
      sh('s4',ks.length+' / 7こ',ks.length>1?big.nm+'は'+sm.nm+'の約'+Math.round(big.g/sm.g)+'倍の重さ':'同じ大きさでくらべよう');
      setShare('【物と重さ】同じ大きさ（1辺3cmの立方体）でも、木'+BY.ki.g+'g・アルミニウム'+BY.arumi.g+'g・鉄'+BY.tetsu.g+'g。体積が同じでも、物によって重さはちがう｜シミュラボ'); } }

  function syncSel(){ ['L','R','S'].forEach(k=>{ $('p'+k).value=place[k]||''; }); }
  function put(id,k){ ['L','R','S'].forEach(q=>{ if(place[q]===id) place[q]=null; }); if(k){ place[k]=id; if(k==='S') recB[id]=1; } syncSel(); }
  function setShp(k){ if(m==='block') return; if(k===shp&&!off.some(Boolean)) return; if(k===shp){ off=[]; offOrd=[]; return; } anim={t:0,from:shp,to:k}; }
  function setMode(v){ m=v; anim=null; off=[]; offOrd=[]; recS={}; drag=null;
    if(v!=='block'){ shp=S().list[0][0]; kd=v==='foil'?'dig':'dial'; $('kd').value=kd; S().list.forEach((it,i)=>{ $('sh'+i).textContent=it[1]; }); rd=S().M; }
    else { kd='dial'; $('kd').value=kd; }
    [0,1,2,3].forEach(i=>show('sh'+i,v!=='block')); show('all',v==='block'); ['pL','pR','pS'].forEach(id=>showF(id,v==='block'));
    $('clr').textContent=v==='block'?'記ろくを消す':'表を消す'; }
  function draw(dt){ ctx.fillStyle=C.bg; ctx.fillRect(0,0,W,H); if(m==='block') drawBlocks(dt); else drawShape(dt); }

  // ---------- 操作
  const opt=BL.map(b=>'<option value="'+b.id+'">'+b.nm+'</option>').join('');
  ['pL','pR','pS'].forEach(id=>{ $(id).innerHTML='<option value="">（なし）</option>'+opt; });
  if(Q.has('m')&&['clay','foil','block'].indexOf(Q.get('m'))>=0) $('m').value=Q.get('m');
  setMode($('m').value);
  if(Q.has('kd')&&KN[Q.get('kd')]){ kd=Q.get('kd'); $('kd').value=kd; }
  if(m!=='block'&&Q.has('sh')&&S().list.some(a=>a[0]===Q.get('sh'))){ recS[shp]=S().M; shp=Q.get('sh'); }
  if(m!=='block'&&Q.get('rec')==='1') S().list.forEach(a=>{ recS[a[0]]=S().M; });
  if(Q.has('off')&&shp==='bara'){ Q.get('off').split(',').forEach(i=>{ i=+i; if(i>=0&&i<S().pcs.length&&!off[i]){ off[i]=true; offOrd.push(i); } }); }
  ['L','R','S'].forEach(k=>{ if(Q.has(k)) place[k]=BY[Q.get(k)]?Q.get(k):null; }); if(place.S) recB[place.S]=1;
  if(Q.get('all')==='1') BL.forEach(b=>{ recB[b.id]=1; });
  syncSel();
  { const bt=place.L&&place.R?BY[place.R].g-BY[place.L].g:(place.R?10:(place.L?-10:0)); th=0.16*Math.tanh(bt/4); }
  rd=m==='block'?(place.S?BY[place.S].g:0):massOn();
  $('m').addEventListener('change',()=>{ setMode($('m').value); stats(); });
  $('kd').addEventListener('change',()=>{ kd=$('kd').value; stats(); });
  [0,1,2,3].forEach(i=>$('sh'+i).addEventListener('click',()=>setShp(S().list[i][0])));
  $('all').addEventListener('click',()=>{ BL.forEach(b=>{ recB[b.id]=1; }); stats(); });
  $('clr').addEventListener('click',()=>{ if(m==='block'){ recB={}; if(place.S) recB[place.S]=1; } else { recS={}; } stats(); });
  ['L','R','S'].forEach(k=>$('p'+k).addEventListener('change',()=>{ const v=$('p'+k).value; if(v) put(v,k); else { place[k]=null; syncSel(); } stats(); }));
  function hitBlock(x,y){ for(let i=0;i<BL.length;i++){ const b=BL[i]; if(!where(b.id)&&Math.abs(x-trayX(i))<40&&y>28&&y<104) return [b.id,null]; }
    for(const k of ['L','R']){ if(place[k]){ const pp=panPos(k); if(Math.abs(x-pp[0])<34&&y>pp[1]-60&&y<pp[1]+4) return [place[k],k]; } }
    if(place.S&&Math.abs(x-SB.cx)<34&&y>SB.py-60&&y<SB.py+6) return [place.S,'S']; return null; }
  function dropAt(x,y){ for(const k of ['L','R']){ const pp=panPos(k); if(Math.abs(x-pp[0])<70&&y>pp[1]-90&&y<pp[1]+50) return k; } if(x>388&&y>110&&y<306) return 'S'; return null; }
  cv.addEventListener('pointerdown',e=>{ const p=cpos(cv,e), x=p[0]/dpr, y=p[1]/dpr;
    if(m!=='block'){ if(anim||shp!=='bara') return; for(let j=hits.length-1;j>=0;j--){ const h=hits[j]; if(Math.hypot(x-h.x,y-h.y)<h.r){ const i=h.i; off[i]=!off[i]; if(off[i]) offOrd.push(i); else offOrd=offOrd.filter(q=>q!==i); e.preventDefault(); stats(); return; } } return; }
    const hb=hitBlock(x,y); if(!hb) return; drag={id:hb[0],from:hb[1],x:x,y:y,x0:x,y0:y,moved:false}; if(hb[1]){ place[hb[1]]=null; syncSel(); }
    try{ cv.setPointerCapture(e.pointerId); }catch(err){} e.preventDefault(); });
  cv.addEventListener('pointermove',e=>{ if(!drag) return; const p=cpos(cv,e); drag.x=p[0]/dpr; drag.y=p[1]/dpr; if(Math.hypot(drag.x-drag.x0,drag.y-drag.y0)>6) drag.moved=true; });
  const up=()=>{ if(!drag) return; const d=drag; drag=null;
    if(d.moved){ const k=dropAt(d.x,d.y); put(d.id,k); } else if(!d.from) put(d.id,'S'); else put(d.id,null);
    stats(); };
  cv.addEventListener('pointerup',up); cv.addEventListener('pointercancel',up);

  function frame(t){ const dt=last?Math.min(0.05,(t-last)/1000):0; last=t; tNow+=dt;
    let tgt;
    if(m!=='block'){ if(anim){ anim.t+=dt; if(anim.t>=1.2){ shp=anim.to; anim=null; off=[]; offOrd=[]; } }
      tgt=(anim&&anim.t>0.12)?0:massOn(); }
    else { tgt=place.S?BY[place.S].g:0;
      const mL=place.L?BY[place.L].g:0, mR=place.R?BY[place.R].g:0, thT=0.16*Math.tanh((mR-mL)/4);
      om+=(-(th-thT)*60-om*7)*dt; th+=om*dt; }
    rd+=(tgt-rd)*(1-Math.exp(-dt*6)); if(Math.abs(tgt-rd)<0.03) rd=tgt;
    if(m!=='block'&&!anim&&rd===tgt&&!off.some(Boolean)) recS[shp]=S().M;
    stats(); draw(dt); requestAnimationFrame(frame); }
  if(m!=='block'&&!off.some(Boolean)) recS[shp]=S().M;
  stats(); draw(0); requestAnimationFrame(frame);
'''

OMOSA_ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
''' + P('物は、<b>形をかえても重さはかわりません</b>。ねん土を丸めても、平らにしても、細かく分けても、全部をはかりにのせれば重さは同じです。また、物は、<b>同じ大きさ（体積）でも、しゅるいによって重さがちがう</b>ことがあります。1辺3cmの立方体では、木は約%s g、アルミニウムは約%s g、鉄は約%s gで、鉄は木の約%d倍の重さです。' % (
    BW["木"], BW["アルミニウム"], BW["鉄"], round(BW["鉄"] / BW["木"]))) + N(
    '<b>対応する単元</b>：小学3年 A（1）物と重さ「（ア）物は，形が変わっても重さは変わらないこと」「（イ）物は，体積が同じでも重さは違うことがあること」（小学校学習指導要領解説 理科編 pp.31〜32）。解説では、てんびんを用いたり、自動上皿はかりで重さを数値化したりして比べ、結果を表に整理することが示されています。') + '''
<p>①②では、ねん土（100 g）やアルミはく（約%s g）の形をボタンでかえると、はかりから下ろして形をかえ、もう一度のせるようすが動きます。結果は右の表にたまります。③では、同じ大きさの7しゅるいのブロックを指でてんびんの皿やはかりに運んで、どちらが重いか、何gかを調べ、重いじゅんにならべます。</p>
''' % FOIL_G + '''<h2>授業での使い方</h2>
<ul>
<li><b>導入</b>：実際にねん土を手にのせ、「平らにすると重さはどうなるか」「細かく分けると軽くなるか」を予想させます。手ごたえだけでは決めにくいことを話し合い、はかりで数にして調べる必要に気づかせます。</li>
<li><b>展開</b>：実物で実験したあと、①で4つの形の重さを表にまとめ、全員の結果と見くらべます。「細かく分ける」でかけらを1つタップしてはかりの外に出すと重さがへるので、<b>全部のせてはかること</b>の大切さを確かめられます。アルミはく（②）は軽いので、自動上皿はかりの目もりでは読みにくく、デジタルはかりに切りかえると小数まで読めます。</li>
<li><b>まとめ</b>：③で、手で持ってくらべにくい「プラスチックとゴム」「ガラスとアルミニウム」をてんびんにのせ、はかりで数にして重いじゅんにならべます。同じ大きさでも鉄やどうはとても重いことを、身の回りの道具（鉄のフライパン、木のまな板など）と結びつけます。</li>
</ul>
<p>児童への問いの例：</p>
<ol>
<li>ねん土を平らにしたら、重さはどうなるでしょう。重くなる・軽くなる・かわらない、のどれだと思いますか。そのわけも話しましょう。</li>
<li>細かく分けたねん土の重さをはかったら、はじめより軽くなりました。どうしてでしょう。どうすれば正しくはかれますか。</li>
<li>同じ大きさのプラスチックとゴムは、手で持ってもどちらが重いか分かりにくいです。どうすればくらべられますか。</li>
</ol>
<h2>しくみ・解説</h2>
<h3>ことばの意味</h3>
<ul>
<li><b>重さ</b>とは、物の重たさのことで、はかりを使うと「g（グラム）」などの数で表せます。</li>
<li><b><ruby>体積<rt>たいせき</rt></ruby></b>とは、物の大きさ（かさ）のことです。</li>
<li><b>てんびん</b>とは、左右の皿に物をのせて、下がった方が重いとくらべる道具で、つり合えば同じ重さです。</li>
<li><b>自動上皿はかり</b>とは、皿に物をのせると、はりが動いて重さを目もりで表すはかりです。</li>
</ul>
<h3>同じ大きさ（1辺3cmの立方体）の重さ 早見表</h3>
''' + T([[n, "%g g" % r, "%s g" % BW[n], "%.1f倍" % (BW[n] / BW["木"])] for n, r in BLOCKS],
        ["物（ブロック）", "1 cm³ あたりの重さ（先生向け）", "1辺3cm（27 cm³）の重さ", "木を1としたとき"]) + '''
<p>どれも同じ大きさなのに、いちばん軽い木といちばん重いどうでは、約%d倍もちがいます。プラスチックとゴム（約3 gちがい）、ガラスとアルミニウム（約5 gちがい）は、手で持つと区別しにくいですが、てんびんにのせるとはっきり分かります。</p>
''' % round(BW["どう（銅）"] / BW["木"]) + '''
<h3>形をかえたときの重さ（このシミュレーションの記ろく）</h3>
''' + T([["ねん土", "丸めた・平らにした・ほそ長くした・細かく分けた", "100 g（どれも同じ）"],
          ["アルミはく（30cm×1m）", "広げた・丸めた・おりたたんだ・細かくちぎった", "%.1f g（どれも同じ）" % FOIL_G],
          ["細かく分けたかけらを1つ外に出す", "はかりにのっている分だけになる", "軽く見える（全部のせると元にもどる）"]],
         ["物", "形のかえ方", "重さ"]) + N(
    '<b>先生向けの補足</b>：重さ（質量）は、物をつくっている粒の量で決まります。形をかえても、物を足したりへらしたりしなければ重さは変わりません。これは学習指導要領の「粒子の保存性」にかかわる内容で、第5学年「物の溶け方」（水に溶かしても全体の重さは変わらない）につながります。1 cm³あたりの重さ（密度）は中学1年で学ぶ考え方で、3年では「同じ大きさでも物によって重さがちがう」ととらえれば十分です。') + '''
<h3>このシミュレーションで単純にしていること</h3>
<ul>
<li>ブロックの重さは、理科年表などにある1 cm³あたりの重さ（密度）から計算した目安です。木は種類によって約0.3〜0.8 g、ゴムやプラスチック、ガラスも種類によって重さがちがいます（木は0.5 g、ゴムは1.3 g、プラスチックはアクリル、ガラスはふつうの板ガラスとして計算）。</li>
<li>アルミはくの重さは、はば30cm・長さ1m・あつさ0.011 mm（11 µm）として計算しています。</li>
<li>自動上皿はかりは、はり1回りが500 g（1目もり10 g）としています。目もりはいちばん近い1 g単位で読んだ数を表示しています。デジタルはかりは0.1 gまで表示します。</li>
<li>てんびんは、少しでも重い方に大きくかたむくようにしています。つり合っているときは、はりがまん中で止まります。</li>
</ul>
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「小学校学習指導要領（平成29年告示）解説 理科編」第3学年 A（1）物と重さ（pp.31〜32）（''' + A(MEXT_SHO, "文部科学省 小学校学習指導要領解説のページ") + '''）</li>
<li>小学校理科（3年）の教科書の「物の重さ」の単元</li>
<li>国立天文台 編『理科年表』（鉄 7.87、アルミニウム 2.70、銅 8.96 g/cm³ など）</li>
</ul>
'''

sim(slug="mono-omosa", cat="rika", emoji="🧱", score=80,
    title="物と重さのシミュレーター（形をかえる・同じ大きさでくらべる）",
    title_tag="物と重さのシミュレーター｜形をかえても重さは同じ？同じ体積の木・鉄・アルミの重さくらべ（小3理科）",
    meta_desc="小3理科「物と重さ」のシミュレーション。ねん土やアルミはくを丸める・平らにする・細かく分けると重さはどうなる？自動上皿はかりとデジタルはかりで確かめ表にまとめます。同じ大きさの木・プラスチック・鉄など7種をてんびんとはかりでくらべ、重いじゅんにならべられます。",
    og_title="物と重さのシミュレーター（小3理科）",
    og_desc="形をかえても重さはかわらない。同じ大きさでも物によって重さはちがう。ねん土・アルミはくと7種のブロックを、てんびん・はかりで調べる。",
    card_desc="ねん土の形をかえても重さは同じ？同じ大きさの木・鉄・アルミをてんびんとはかりでくらべる。",
    lead="ねん土やアルミはくの形をかえて、はかりで重さをはかってみましょう。同じ大きさのブロックを指でてんびんやはかりに運ぶと、物によって重さがちがうことも分かります。",
    model="小3 物と重さ", level="小学3年",
    unit="小学校 第3学年 A（1）物と重さ",
    canvas=canvas(640, 440, light=True),
    controls=select("m", "やること", [("clay", "① ねん土の形をかえる"), ("foil", "② アルミはくの形をかえる"), ("block", "③ 同じ大きさでくらべる（てんびん・はかり）")])
             + select("kd", "はかり", [("dial", "自動上皿はかり（はり）"), ("dig", "デジタルはかり")])
             + select("pL", "てんびんの左の皿", [("", "（なし）")]) + select("pR", "てんびんの右の皿", [("", "（なし）")])
             + select("pS", "はかりにのせる物", [("", "（なし）")]),
    buttons=btn("sh0", "⚪ 丸める", True) + btn("sh1", "🥞 平らにする", True) + btn("sh2", "〰️ ほそ長くする", True) + btn("sh3", "🔹 細かく分ける", True)
            + btn("all", "全部はかって重いじゅんに", True) + btn("clr", "表を消す"),
    stats=stats([("s1", "はかりの目もり", True), ("s2", "いまの形", False), ("s3", "はじめの重さとのちがい", False), ("s4", "調べた形", False)]),
    legend="①②：ボタンで形をかえると、はかりから下ろして形をかえ、もう一度のせます。結果は右の表にたまります。細かく分けたときは、かけらをタップしてはかりの外に出せます。③：ブロックはどれも1辺3cmの立方体（同じ大きさ）です。指でてんびんの皿やはかりへ運び、タップするとはかりにのります。重さの値は1 cm³あたりの重さから計算した目安です。",
    article=OMOSA_ARTICLE,
    faqs=[("物の形をかえると、重さはかわりますか？", "かわりません。ねん土を丸めても、平らにしても、細かく分けても、全部をはかりにのせれば重さは同じです。物を足したりへらしたりしなければ、重さはかわりません。"),
          ("細かく分けたねん土をはかったら、軽くなりました。なぜですか？", "かけらがはかりからこぼれたり、手や机にねん土が残ったりして、全部をのせていないからです。かけらを全部のせてはかると、はじめと同じ重さになります。"),
          ("同じ大きさなのに、物によって重さがちがうのはなぜですか？", "物のしゅるいによって、同じ大きさあたりの重さがちがうからです。1辺3cmの立方体では、木は約14 g、アルミニウムは約73 g、鉄は約213 gです。"),
          ("てんびんでは、どうやって重さをくらべますか？", "左右の皿に物をのせると、重い方の皿が下がります。つり合ったときは、2つの重さが同じです。手で持って区別しにくいときも、てんびんならはっきり分かります。"),
          ("自動上皿はかりのつかい方で気をつけることは？", "平らな所に置き、何ものせないときにはりが0をさしているか確かめます。物はそっと皿のまん中にのせ、目もりは正面から読みます。"),
          ("鉄は木の何倍くらい重いですか？", "同じ大きさなら、鉄は木の約16倍の重さです（木の1 cm³あたりの重さを0.5 gとしたとき）。木の種類によって倍数はかわります。")],
    rel=[("youkaido", "🧂", "物の溶け方"), ("teko-tsuriai", "⚖️", "てこのつり合いシミュレーター"), ("bane-nobi", "🪀", "ばねののびと力"),
         ("kuuki-mizu", "💉", "とじこめた空気と水"), ("kaze-gomu", "🚗", "風とゴムの力の働き")],
    js=JS_OMOSA)


# ============================================================ 2 風とゴムの力の働き
G_, MASS, MU, AS, CDR, RHO = 9.8, 0.1, 0.04, 0.04, 1.2, 1.2
D0, CORE = 0.3, 0.6
WV = {1: 3.0, 2: 4.0, 3: 5.0}

def wind_dist(V0, mu=MU, dt=0.002):
    """送風機の風で走る車の進むきょり（m）。JSと同じ式"""
    k = 0.5 * RHO * CDR * AS; s = u = t = 0.0
    while t < 60:
        d = s + D0; vw = V0 * (1 if d < CORE else CORE / d); rel = vw - u
        F = k * rel * abs(rel); fr = mu * MASS * G_
        if u <= 1e-6 and F <= fr and t > 0.05: break
        a = (F - fr) / MASS if (u > 1e-6 or F > fr) else 0
        u = max(0.0, u + a * dt); s += u * dt; t += dt
    return s

def rub_dist(n, x): return 0.9 * n * (x / 5) ** 1.5
def fmtd(d):
    cm = int(round(d * 100)); m_, c_ = divmod(cm, 100)
    return ("%dm%02dcm" % (m_, c_)) if m_ else "%dcm" % c_
WD = {k: wind_dist(v) for k, v in WV.items()}

JS_KAZE = HELP + r'''
  const C={bg:'#f8fafc',ink:'#0f172a',sub:'#64748b',red:'#dc2626',blue:'#2563eb',green:'#15803d',wind:'#0284c7',g1:'#f97316',g2:'#be123c'};
  // 車：重さ100 g・帆20cm×20cm。ころがるときのまさつ係数0.04。送風機の口での風の速さ 弱3・中4・強5 m/秒、口から0.6 mより先は きょりに反比例して弱まる
  // ゴム：進むきょり＝0.9 m×本数×(のばす長さ÷5cm)^1.5（輪ゴムのめやす）。どちらも1回ごとに少しばらつく
  const X0=104, X1=620, PXM=(X1-X0)/10, TY=132, CL=38, PZ=3;
  const G=9.8, MASS=0.1, MU=0.04, KW=0.5*1.2*1.2*0.04, D0=0.3, CORE=0.6, SPD=1.5;
  const WV={1:3.0,2:4.0,3:5.0}, WN={1:'弱い風',2:'中くらいの風',3:'強い風'}, WS={1:'弱',2:'中',3:'強'};
  const rubD=(n,x)=>0.9*n*Math.pow(x/5,1.5);
  let pw='gomu', wl=1, px=5, nb=1, st='idle', run=null, trials=[], queue=0, wait=0, last=0, tNow=0, fanA=0, parts=[], dragP=false, lastD=null;
  let game={on:false,tg:3.2,tries:[],ok:false};
  function fmtD(d){ const cm=Math.round(d*100), m=Math.floor(cm/100), c=cm%100; return m?(m+'m'+(c<10?'0':'')+c+'cm'):(c+'cm'); }
  const r10=(d)=>Math.round(d*10)/10;
  function cond(){ return pw==='kaze'?{k:'w'+wl,a:'風',b:WS[wl],col:C.wind,ord:wl,nm:WN[wl]}:{k:'g'+nb+'_'+px,a:'ゴム'+nb+'本',b:px+'cm',col:nb===1?C.g1:C.g2,ord:100*nb+px,nm:'ゴム'+nb+'本・'+px+'cmのばす'}; }
  function noise(sd,lim){ return clamp(randn()*sd,-lim,lim); }
  function start(){ const c=cond(); lastD=null;
    if(pw==='kaze'){ run={c:c,type:'w',s:0,u:0,t:0,V0:WV[wl]*(1+noise(0.03,0.07)),mu:MU*(1+noise(0.05,0.12)),done:false}; }
    else { const dT=rubD(nb,px)*(1+noise(0.05,0.12)), a=MU*G; run={c:c,type:'g',s:0,t:0,dT:dT,a:a,v0:Math.sqrt(2*a*dT),done:false}; }
    st='run'; }
  function windStep(r,dt){ const d=r.s+D0, vw=r.V0*(d<CORE?1:CORE/d), rel=vw-r.u, F=KW*rel*Math.abs(rel), fr=r.mu*MASS*G;
    if(r.u<=1e-6&&F<=fr&&r.t>0.05){ r.done=true; return; } const a=(r.u>1e-6||F>fr)?(F-fr)/MASS:0; r.u=Math.max(0,r.u+a*dt); r.s+=r.u*dt; r.t+=dt; }
  function finish(){ const d=run.s, c=run.c; lastD=d; trials.push({k:c.k,a:c.a,b:c.b,col:c.col,ord:c.ord,nm:c.nm,d:d}); st='stop';
    if(game.on&&run.type==='g'){ const ok=d>=game.tg&&d<=game.tg+0.5; game.tries.push({nm:c.nm,d:d,ok:ok}); if(ok) game.ok=true; }
    if(queue>0){ queue--; wait=queue>0?0.9:0; } stats(); }
  function cats(){ const mp={}; trials.forEach(t=>{ if(!mp[t.k]) mp[t.k]={k:t.k,a:t.a,b:t.b,col:t.col,ord:t.ord,ds:[]}; mp[t.k].ds.push(t.d); });
    let cs=Object.keys(mp).map(k=>mp[k]).sort((a,b)=>a.ord-b.ord); if(cs.length>7) cs=cs.slice(cs.length-7); cs.forEach(c=>{ c.avg=c.ds.reduce((a,b)=>a+b,0)/c.ds.length; }); return cs; }
  function finding(){ const cs=cats();
    if(pw==='kaze'){ const w=cs.filter(c=>c.k[0]==='w'); if(w.length>=2){ const inc=w.every((c,i)=>!i||c.avg>w[i-1].avg); return inc?['風が強いほど遠くへ','力が大きいとよく進む']:['くらべてみよう','やり方をかえて3回ずつ']; } return ['くらべてみよう','風の強さをかえよう']; }
    for(const q of [nb,3-nb]){ const g=cs.filter(c=>c.k[0]==='g'&&c.k.indexOf('g'+q+'_')===0); if(g.length>=2&&g.every((c,i)=>!i||c.avg>g[i-1].avg)) return ['長くのばすほど遠くへ','力が大きいとよく進む']; }
    const same=cs.filter(c=>c.k[0]==='g'&&c.b===px+'cm'); if(same.length>=2){ const inc=same.every((c,i)=>!i||c.avg>same[i-1].avg); if(inc) return ['本数が多いと遠くへ','力が大きいとよく進む']; }
    return ['くらべてみよう','やり方をかえて3回ずつ']; }

  // ---------- 描画
  function drawCar(fx,s,wind){ const x=fx-CL, y=TY; const ang=s/0.03;
    if(wind){ ctx.fillStyle='#78350f'; ctx.fillRect(x+CL*0.45,y-48,3,36); ctx.fillStyle='#fde68a'; ctx.strokeStyle='#b45309'; ctx.lineWidth=1.2; ctx.beginPath(); ctx.moveTo(x+CL*0.45,y-48); ctx.quadraticCurveTo(x+CL*0.45-7,y-32,x+CL*0.45,y-16); ctx.lineTo(x+CL*0.45+2,y-16); ctx.lineTo(x+CL*0.45+2,y-48); ctx.closePath(); ctx.fill(); ctx.stroke(); }
    ctx.fillStyle='#38bdf8'; ctx.strokeStyle='#0369a1'; ctx.lineWidth=1.3; rr(x,y-20,CL,12,4); ctx.fill(); ctx.stroke();
    ctx.fillStyle='#0369a1'; ctx.fillRect(fx-2,y-17,4,4);
    [x+8,x+CL-8].forEach(wx=>{ dot(wx,y-6,6,'#1f2937'); ctx.strokeStyle='#e5e7eb'; ctx.lineWidth=1.5; line(wx,y-6,wx+Math.cos(ang)*5,y-6+Math.sin(ang)*5); dot(wx,y-6,1.8,'#e5e7eb'); }); }
  function drawFan(on,dt){ const cx=52, cy=TY-38; ctx.fillStyle='#94a3b8'; ctx.fillRect(cx-4,cy,8,TY-cy); ctx.fillStyle='#64748b'; rr(cx-24,TY-6,48,6,3); ctx.fill();
    ctx.fillStyle='#e2e8f0'; ctx.beginPath(); ctx.arc(cx,cy,27,0,7); ctx.fill(); ctx.strokeStyle='#475569'; ctx.lineWidth=2; ctx.stroke();
    if(on) fanA+=dt*(8+wl*6); ctx.fillStyle='#60a5fa'; for(let k=0;k<3;k++){ const a=fanA+k*2.094; ctx.beginPath(); ctx.ellipse(cx+Math.cos(a)*12,cy+Math.sin(a)*12,12,6,a,0,7); ctx.fill(); }
    dot(cx,cy,4,'#1e3a8a'); ctx.strokeStyle='rgba(71,85,105,.5)'; ctx.lineWidth=1; for(let r=10;r<27;r+=8){ ctx.beginPath(); ctx.arc(cx,cy,r,0,7); ctx.stroke(); }
    tx('送風き',cx,TY+18,11,C.sub,'center',true); }
  function drawWind(on,dt){ if(on&&Math.random()<dt*(20+wl*14)*3) parts.push({x:80,y:TY-62+Math.random()*52,v:0});
    parts.forEach(p=>{ const s=(p.x-X0)/PXM, d=s+D0, vw=WV[wl]*(d<CORE?1:CORE/Math.max(d,0.05)); p.x+=vw*PXM*dt*SPD*0.9; p.a=clamp(vw/WV[wl],0,1); });
    parts=parts.filter(p=>p.x<X1&&p.a>0.12); ctx.lineWidth=1.6; parts.forEach(p=>{ ctx.strokeStyle='rgba(2,132,199,'+(0.55*p.a)+')'; line(p.x,p.y,p.x+12,p.y); }); }
  function drawCourse(dt){ panel(8,8,624,184); const c=cond();
    tx('スタートから進んだきょり',20,30,13.5,C.ink,'left',true); tx(game.on?'🎯 ゴールゲーム：'+c.nm:c.nm,620,30,13.5,c.col,'right',true,330);
    ctx.fillStyle='#f1f5f9'; ctx.fillRect(9,TY,622,12); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1.5; line(9,TY,631,TY);
    // メジャー
    ctx.fillStyle='#fde68a'; ctx.fillRect(X0,TY+14,X1-X0,22); ctx.strokeStyle='#ca8a04'; ctx.lineWidth=1; ctx.strokeRect(X0,TY+14,X1-X0,22);
    for(let k=0;k<=100;k++){ const x=X0+k*PXM/10, big=k%10===0, mid=k%5===0; ctx.strokeStyle=big?'#713f12':'#a16207'; ctx.lineWidth=big?1.4:0.8; line(x,TY+14,x,TY+14+(big?11:(mid?7:4))); if(big) tx(k?(k/10)+'m':'0',x+(k===100?-3:2),TY+34,10.5,'#713f12',k===100?'right':'left',true); }
    trials.slice(-12).forEach(t=>{ const x=X0+Math.min(10,t.d)*PXM; ctx.fillStyle=t.col; ctx.beginPath(); ctx.moveTo(x,TY+14); ctx.lineTo(x-5,TY+6); ctx.lineTo(x+5,TY+6); ctx.closePath(); ctx.fill(); });
    // ゴールのはこ
    if(game.on){ const gx=X0+game.tg*PXM, gw=0.5*PXM; ctx.fillStyle=game.ok?'rgba(34,197,94,.25)':'rgba(250,204,21,.3)'; ctx.fillRect(gx,TY-26,gw,26); ctx.strokeStyle='#92400e'; ctx.lineWidth=2.5; ctx.beginPath(); ctx.moveTo(gx,TY-26); ctx.lineTo(gx,TY); ctx.lineTo(gx+gw,TY); ctx.lineTo(gx+gw,TY-26); ctx.stroke();
      ctx.strokeStyle='#334155'; ctx.lineWidth=1.5; line(gx+gw/2,TY-26,gx+gw/2,TY-58); ctx.fillStyle=C.red; ctx.beginPath(); ctx.moveTo(gx+gw/2,TY-58); ctx.lineTo(gx+gw/2+18,TY-51); ctx.lineTo(gx+gw/2,TY-44); ctx.fill(); tx('ゴール',gx+gw/2,TY-62,11,'#92400e','center',true); }
    // スタートの台
    const isW=pw==='kaze', fanOn=st==='run'&&isW;
    if(isW){ drawFan(fanOn,dt); drawWind(fanOn,dt); }
    else { ctx.fillStyle='#a16207'; ctx.fillRect(X0-4,TY-38,8,38); ctx.fillStyle='#78350f'; rr(X0-14,TY-4,28,6,2); ctx.fill(); parts=[]; tx('ゴムの台',X0-46,TY+18,11,C.sub,'center',true); }
    ctx.strokeStyle='#64748b'; ctx.lineWidth=1; ctx.setLineDash([3,3]); line(X0,TY-70,X0,TY); ctx.setLineDash([]); if(st==='idle') tx('スタート',X0+4,TY-62,10.5,C.sub,'left',true);
    // 車
    let fx, s=0;
    if(st==='run'||st==='stop'){ s=run?run.s:0; fx=X0+Math.min(10.2,s)*PXM; } else fx=X0-(isW?0:px*PZ);
    if(!isW){ const hx=fx, hy=TY-15, n=nb; ctx.strokeStyle='#b45309'; ctx.lineWidth=2+n*0.8;
      if(st==='idle'&&px>0){ line(X0,TY-34,hx,hy); line(X0,TY-8,hx,hy); tag(px+'cm のばす',X0-36,TY-46,12,C.g1,'center'); }
      else { ctx.beginPath(); ctx.ellipse(X0+3,TY-21,4,13,0,0,7); ctx.stroke(); } }
    drawCar(fx,s,isW);
    if(st==='idle') tx(isW?'▶ で送風きをつけよう':'車を指で左へ引いて、はなそう',isW?X0+60:X0+40,TY-80,12.5,'#0e7490','left',true);
    if(st==='stop'&&lastD!=null){ tag(fmtD(lastD),clamp(fx-CL/2,X0+20,580),isW?TY-58:TY-36,14,C.ink,'center'); }
    if(!isW&&st==='idle') tx('（スタートの台は大きくかいています）',X0+150,TY+52,10.5,'#94a3b8','left',true); }
  function drawGraph(){ panel(8,198,624,234); const cs=cats();
    tx('進んだきょりの記ろく',20,220,13.5,C.ink,'left',true); tx('● ＝ 1回ごと　ぼう ＝ だいたい',620,220,11.5,C.sub,'right',true);
    const GX0=58, GX1=618, GY0=392, GY1=240, mx=cs.length?Math.max(...cs.map(c=>Math.max(...c.ds))):0, ym=clamp(Math.ceil(mx+0.5),4,10), st2=ym>6?2:1, gy=v=>GY0-(GY0-GY1)*v/ym;
    ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; for(let v=st2;v<=ym;v+=st2){ line(GX0,gy(v),GX1,gy(v)); tx(v+'m',GX0-6,gy(v)+4,10.5,C.sub,'right',true); } tx('0',GX0-6,GY0+4,10.5,C.sub,'right',true);
    ctx.strokeStyle=C.ink; ctx.lineWidth=1.3; line(GX0,GY1-6,GX0,GY0); line(GX0,GY0,GX1,GY0);
    if(!cs.length){ tx('▶ 走らせると、ここに記ろくがたまるよ。',338,306,13.5,'#94a3b8','center',true); tx('同じやり方で3回ずつためして、くらべよう。',338,328,12.5,'#94a3b8','center',true); return; }
    const n=Math.max(4,cs.length), cw=(GX1-GX0)/n;
    cs.forEach((c,i)=>{ const x=GX0+cw*(i+0.5), cur=c.k===cond().k; ctx.globalAlpha=0.32; ctx.fillStyle=c.col; ctx.fillRect(x-18,gy(c.avg),36,GY0-gy(c.avg)); ctx.globalAlpha=1; ctx.strokeStyle=c.col; ctx.lineWidth=cur?2.6:1.4; ctx.strokeRect(x-18,gy(c.avg),36,GY0-gy(c.avg));
      c.ds.slice(-8).forEach((d,j,arr)=>dot(x+(j-(arr.length-1)/2)*7,gy(d),4.2,c.col,'#fff'));
      tx(fmtD(r10(c.avg)),x,gy(Math.max(c.avg,...c.ds.slice(-8)))-9,11,C.ink,'center',true,cw-4);
      tx(c.a,x,GY0+17,11.5,c.col,'center',true,cw-4); tx(c.b+'（'+c.ds.length+'回）',x,GY0+32,11,C.ink,'center',true,cw-4); }); }
  function drawGame(){ panel(8,198,624,234); tx('🎯 ゴールゲーム：車をゴールのはこの中に止めよう',20,222,14,C.ink,'left',true,600);
    tx('ゴールのはこ：'+fmtD(game.tg)+' 〜 '+fmtD(game.tg+0.5)+'（はこの中に車の先が止まればゴール）',20,246,12.5,'#92400e','left',true,600);
    if(game.ok){ ctx.fillStyle='#dcfce7'; rr(20,256,600,40,10); ctx.fill(); tx('ゴール！🎉　'+game.tries.length+'回目で入ったよ。「ゴールを動かす」でもう一度。',320,282,15,C.green,'center',true,580); }
    else tx(game.tries.length?'ゴムをのばす長さや本数を調べて、ちょうどよい力にしよう。':'まずは1回走らせて、どこまで進むか見てみよう。',20,280,12.5,C.sub,'left',true,600);
    game.tries.slice(-5).forEach((t,i,arr)=>{ const y=318+i*22, k=game.tries.length-arr.length+i+1; let h;
      if(t.ok) h='ゴール！'; else if(t.d<game.tg) h='あと '+fmtD(game.tg-t.d)+' たりない'; else h=fmtD(t.d-game.tg-0.5)+' 行きすぎ';
      tx(k+'回目',28,y,12.5,C.sub,'left',true); tx(t.nm,90,y,12.5,C.ink,'left',true,230); tx('→ '+fmtD(t.d),330,y,12.5,C.ink,'left',true); tx(h,450,y,12.5,t.ok?C.green:C.red,'left',true,170); }); }
  function draw(dt){ ctx.fillStyle=C.bg; ctx.fillRect(0,0,W,H); drawCourse(dt); if(game.on) drawGame(); else drawGraph(); }

  // ---------- 統計
  function stats(){ const c=cond(), my=trials.filter(t=>t.k===c.k), av=my.length?my.reduce((a,t)=>a+t.d,0)/my.length:0;
    lab('s1','今回進んだきょり'); lab('s2','このやり方のだいたい'); lab('s3','力の大きさ'); lab('s4',game.on?'ゴールまで':'わかること');
    sh('s1',st==='run'?'走っている…':(lastD!=null?fmtD(lastD):'0m'),st==='run'||lastD!=null?c.nm:'まだ走らせていない');
    sh('s2',my.length?'約'+fmtD(r10(av)):'まだ',my.length?my.length+'回の記ろくから':'3回ためそう');
    sh('s3',pw==='kaze'?WN[wl]:'ゴム'+nb+'本・'+px+'cm',pw==='kaze'?'送風きの口で約'+WV[wl]+'m/秒':'長い・多いほど強い');
    if(game.on){ const t=game.tries[game.tries.length-1]; sh('s4',game.ok?'ゴール！':(t?(t.d<game.tg?'あと'+fmtD(game.tg-t.d):fmtD(t.d-game.tg-0.5)+'行きすぎ'):fmtD(game.tg)),game.tries.length+'回ためした'); }
    else { const f=finding(); sh('s4',f[0],f[1]); }
    const cs=cats(); if(cs.length>=2){ const a=cs[0], b=cs[cs.length-1], f0=finding()[0]; setShare('【風とゴムの力】'+a.a+'・'+a.b+'でだいたい'+fmtD(r10(a.avg))+'、'+b.a+'・'+b.b+'でだいたい'+fmtD(r10(b.avg))+'。'+(/へ$/.test(f0)?f0+'進む':'')+'｜シミュラボ'); }
    else setShare('【風とゴムの力のはたらき】風やゴムの力で車を走らせ、進んだきょりをぼうグラフでくらべるシミュレーター｜シミュラボ'); }
  function setIdle(){ if(st!=='run'){ st='idle'; lastD=null; } }
  function syncUI(){ showF('wl',pw==='kaze'); showF('px',pw==='gomu'); showF('nb',pw==='gomu'); showF('pw',!game.on); show('newg',game.on);
    $('game').textContent=game.on?'ゲームをやめる':'🎯 ゴールゲーム'; $('pxL').textContent=px+' cm'; $('px').value=px; }
  function newGoal(){ let t; do{ t=Math.round(rnd(1.5,7.0)*10)/10; }while(Math.abs(t-game.tg)<0.8); game={on:true,tg:t,tries:[],ok:false}; setIdle(); }

  // ---------- 操作
  if(Q.get('pw')==='kaze') $('pw').value='kaze';
  pw=$('pw').value; wl=+$('wl').value; nb=+$('nb').value; px=+$('px').value;
  if(Q.has('x')){ px=clamp(+Q.get('x')||5,1,15); } if(Q.has('n')){ nb=Q.get('n')==='2'?2:1; $('nb').value=String(nb); }
  if(Q.get('pre')==='1'){ const keep=[pw,wl,px,nb]; const L=pw==='kaze'?[[1],[2],[3]]:[[5,1],[10,1],[15,1]];
    L.forEach(q=>{ if(pw==='kaze') wl=q[0]; else { px=q[0]; nb=q[1]; } for(let r=0;r<3;r++){ start(); if(run.type==='g') run.s=run.dT; else { while(!run.done) windStep(run,0.002); } finish(); } });
    pw=keep[0]; wl=keep[1]; px=keep[2]; nb=keep[3]; $('wl').value=String(wl); st='idle'; lastD=null; }
  if(Q.get('game')==='1'){ pw='gomu'; $('pw').value='gomu'; game={on:true,tg:3.2,tries:[],ok:false}; }
  syncUI();
  if(Q.get('go')==='1'){ start(); }
  $('pw').addEventListener('change',()=>{ pw=$('pw').value; queue=0; if(st!=='run') st='idle'; lastD=null; syncUI(); stats(); });
  $('wl').addEventListener('change',()=>{ wl=+$('wl').value; setIdle(); stats(); });
  $('nb').addEventListener('change',()=>{ nb=+$('nb').value; setIdle(); stats(); });
  $('px').addEventListener('input',()=>{ px=+$('px').value; $('pxL').textContent=px+' cm'; setIdle(); stats(); });
  $('go').addEventListener('click',()=>{ if(st!=='run'){ queue=0; start(); stats(); } });
  $('rep').addEventListener('click',()=>{ if(st!=='run'){ queue=3; start(); stats(); } });
  $('game').addEventListener('click',()=>{ if(st==='run') return; if(game.on){ game.on=false; } else { pw='gomu'; $('pw').value='gomu'; newGoal(); } queue=0; setIdle(); syncUI(); stats(); });
  $('newg').addEventListener('click',()=>{ if(st==='run') return; newGoal(); stats(); });
  $('clr').addEventListener('click',()=>{ if(st==='run') return; trials=[]; game.tries=[]; game.ok=false; st='idle'; lastD=null; stats(); });
  cv.addEventListener('pointerdown',e=>{ const p=cpos(cv,e), x=p[0]/dpr, y=p[1]/dpr; if(st==='run') return;
    if(pw==='kaze'){ if(x<96&&y>TY-80&&y<TY+10){ queue=0; start(); stats(); } return; }
    const fx=st==='idle'?X0-px*PZ:X0+(run?run.s:0)*PXM; if(y>TY-60&&y<TY+20&&((x>fx-CL-24&&x<fx+24)||(x>X0-80&&x<X0+30))){ st='idle'; lastD=null; dragP=true; try{ cv.setPointerCapture(e.pointerId); }catch(err){} e.preventDefault(); } });
  cv.addEventListener('pointermove',e=>{ if(!dragP) return; const x=cpos(cv,e)[0]/dpr; px=clamp(Math.round((X0-x+CL*0.2)/PZ),1,15); $('px').value=px; $('pxL').textContent=px+' cm'; stats(); });
  const up=()=>{ if(!dragP) return; dragP=false; queue=0; start(); stats(); };
  cv.addEventListener('pointerup',up); cv.addEventListener('pointercancel',up);
  function frame(t){ const dt=last?Math.min(0.05,(t-last)/1000):0; last=t; tNow+=dt;
    if(st==='run'&&run){ const h=dt*SPD;
      if(run.type==='w'){ let k=0; while(k<h&&!run.done){ windStep(run,0.002); k+=0.002; } if(run.done) finish(); }
      else { run.t+=h; const tt=Math.min(run.t,run.v0/run.a); run.s=run.v0*tt-run.a*tt*tt/2; if(run.t>=run.v0/run.a){ run.s=run.dT; finish(); } } }
    else if(st==='stop'&&queue>0){ wait-=dt; if(wait<=0){ start(); } }
    if(st==='run') stats();
    draw(dt); requestAnimationFrame(frame); }
  stats(); draw(0); requestAnimationFrame(frame);
'''

KAZE_ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
''' + P('<b>風の力</b>や<b>ゴムの力</b>で、物を動かすことができます。風を強くするほど、またゴムを長くのばしたり本数をふやしたりするほど、力が大きくなり、車は<b>遠くまで進みます</b>。同じやり方で何回か走らせると、進んだきょりは少しずつちがう（ばらつく）ので、何回かの記ろくから「だいたいこのくらい」と考えます。') + N(
    '<b>対応する単元</b>：小学3年 A（2）風とゴムの力の働き「（ア）風の力は，物を動かすことができること。また，風の力の大きさを変えると，物が動く様子も変わること」「（イ）ゴムの力は，物を動かすことができること。また，ゴムの力の大きさを変えると，物が動く様子も変わること」（小学校学習指導要領解説 理科編 pp.32〜33）。解説では、風の強さやゴムの伸びと物の動きとの関係を表に整理すること、目的に合わせて風やゴムの力を調整することが示されています。') + '''
<p>送風機の風の強さ（弱・中・強）や、ゴムをのばす長さ（1〜15cm）・ゴムの本数（1本・2本）をかえて車を走らせると、進んだきょりがメジャーの上に記ろくされ、下のぼうグラフに「●（1回ごと）」と「ぼう（だいたい）」でたまります。「🎯 ゴールゲーム」では、ゴールのはこの中に車を止めるために、ゴムの力をちょうせつします。</p>
<h2>授業での使い方</h2>
<ul>
<li><b>導入</b>：実際に風やゴムで動く車をつくって走らせたあと、「もっと遠くまで走らせるにはどうすればよいか」を話し合います。風を受けたときやゴムを引っぱったときの手ごたえと結びつけて予想させます。</li>
<li><b>展開</b>：「3回ためす」で同じやり方を3回走らせ、記ろくがばらつくことを確かめます。そのうえで、ゴムをのばす長さを5cm・10cm・15cmにかえて、ぼうグラフでくらべます。風は「弱い風」と「強い風」でくらべます。実際の実験で教室や廊下がせまいときの、予想や確かめにも使えます。</li>
<li><b>まとめ</b>：「🎯 ゴールゲーム」で、ゴールのはこにぴったり止めるには何cmのばせばよいかを、それまでの記ろくから考えます。「目的に合わせて力の大きさをちょうせつする」活動になります。</li>
</ul>
<p>児童への問いの例：</p>
<ol>
<li>ゴムをのばす長さを5cmから10cmにすると、車の進むきょりはどうなるでしょう。</li>
<li>同じやり方で3回走らせたのに、きょりが少しずつちがいました。どの記ろくを使えばよいでしょう。</li>
<li>ゴールのはこが3mのところにあります。前の記ろくを見て、ゴムを何cmのばせばよいと思いますか。</li>
</ol>
<h2>しくみ・解説</h2>
<h3>ことばの意味</h3>
<ul>
<li><b>風の力</b>とは、うごく空気（風）が物をおす力のことで、風が強いほど大きくなります。</li>
<li><b>ゴムの力</b>とは、のばしたりねじったりしたゴムが、もとの形にもどろうとする力のことです。</li>
<li><b>進んだきょり</b>とは、スタートの線から車が止まった所までの長さのことです。</li>
<li><b>だいたい</b>（先生向け：平均）とは、何回かの記ろくをならしたときの、まん中あたりの長さのことです。</li>
<li><b>ぼうグラフ</b>とは、数の大きさをぼうの長さで表したグラフで、くらべやすくなります。</li>
</ul>
<h3>進むきょり 早見表（このシミュレーションのめやす・ばらつきなし）</h3>
''' + T([["ゴム1本", fmtd(rub_dist(1, 5)), fmtd(rub_dist(1, 10)), fmtd(rub_dist(1, 15))],
          ["ゴム2本", fmtd(rub_dist(2, 5)), fmtd(rub_dist(2, 10)), fmtd(rub_dist(2, 15))]],
         ["ゴムの本数", "5cmのばす", "10cmのばす", "15cmのばす"]) + T(
    [["弱い風（約3 m/秒）", fmtd(WD[1])], ["中くらいの風（約4 m/秒）", fmtd(WD[2])], ["強い風（約5 m/秒）", fmtd(WD[3])]],
    ["送風機の風（口での風の速さ）", "進むきょり"]) + '''
<p>実際には1回ごとに少しちがい、このシミュレーションでも同じやり方で、だいたい ±5〜10％ くらいばらつきます。ゴムは、のばす長さを2倍（5cm→10cm）にすると、きょりは約2.8倍になります。本数を2本にすると、きょりは約2倍になります。</p>
<h3>「だいたい」の考え方</h3>
<p>同じやり方でも、車の置き方や手のはなし方、ゆかのようすで、進むきょりは少しずつかわります。1回だけの記ろくで決めずに、3回くらい走らせて、「だいたいこのあたり」と考えます。ぼうグラフのぼうは、何回かの記ろくをならした長さ（平均）です。</p>
''' + N('<b>先生向けの補足</b>：本シミュレーションの「だいたい」は算術平均を10cm単位にまるめた値です。平均は算数の第5学年で学ぶため、3年生には「記ろくの点が集まっているあたり」「いちばん長い記ろくと短い記ろくのあいだ」ととらえさせると無理がありません。本単元は第5学年「振り子の運動」（条件をそろえて何回か測る）につながります。') + '''
<h3>このシミュレーションのしくみ（先生向け）</h3>
<ul>
<li><b>車</b>：重さ100 g、帆20cm×20cm、ころがるときのまさつ係数0.04。</li>
<li><b>ゴム</b>：進むきょり＝0.9 m×本数×（のばす長さ÷5cm）<sup>1.5</sup>。ばねのように力がのびに比例するなら、きょりはのびの2乗に比例しますが、輪ゴムはのびが大きくなると力の増え方がゆるやかになるため、1.5乗としためやすです。</li>
<li><b>風</b>：帆が受ける力＝½×空気の密度×抗力係数1.2×帆の面積×（風の速さ−車の速さ）<sup>2</sup>。送風機の風は、口から0.6 mまでは同じ速さで、それより先はきょりに反比例して弱まるとしています。風の力がまさつより小さくなると車は止まります。</li>
<li>1回ごとのばらつきは、ゴムは5％、風は風の速さ3％・まさつ5％の大きさの乱数で表しています。</li>
<li>メジャーの上の車とスタートの台は、見やすいように大きくかいています（車の長さは約20cmのつもり）。</li>
</ul>
<p>ゴムを強く引っぱりすぎると切れたり、手や顔に当たったりします。実際の実験では、ゴムをのばす長さを決めて、人のいる方に向けないようにします。</p>
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「小学校学習指導要領（平成29年告示）解説 理科編」第3学年 A（2）風とゴムの力の働き（pp.32〜33）、内容の取扱い（ものづくり p.38）（''' + A(MEXT_SHO, "文部科学省 小学校学習指導要領解説のページ") + '''）</li>
<li>小学校理科（3年）の教科書の「風とゴムの力のはたらき」の単元</li>
</ul>
'''

sim(slug="kaze-gomu", cat="rika", emoji="🚗", score=81,
    title="風とゴムの力の働きシミュレーター（車が進むきょりをくらべる）",
    title_tag="風とゴムの力の働き シミュレーター｜風の強さ・ゴムをのばす長さと車の進むきょり（小3理科）",
    meta_desc="小3理科「風とゴムの力の働き」のシミュレーション。送風機の風の強さ（弱・強）や、ゴムをのばす長さ・本数をかえて車を走らせ、進んだきょりを表とぼうグラフに記録。何回かためしたばらつきから「だいたい」を考え、ゴールのはこに止めるゲームで力の調整も体験できます。",
    og_title="風とゴムの力の働きシミュレーター（小3理科）",
    og_desc="風を強く、ゴムを長くのばすほど車は遠くへ。進んだきょりをぼうグラフでくらべ、ゴールのはこに止めるゲームも。",
    card_desc="風の強さやゴムをのばす長さで車の進むきょりはどうかわる？ぼうグラフとゴールゲームで。",
    lead="送風機の風の強さや、ゴムをのばす長さ・本数をかえて車を走らせましょう。進んだきょりがぼうグラフにたまります。ゴールのはこに車を止めるゲームもあります。",
    model="小3 風とゴムの力の働き", level="小学3年",
    unit="小学校 第3学年 A（2）風とゴムの力の働き",
    canvas=canvas(640, 440, light=True),
    controls=select("pw", "車を動かす力", [("gomu", "ゴムの力"), ("kaze", "風の力（送風き）")])
             + select("wl", "風の強さ", [("1", "弱い風"), ("2", "中くらいの風"), ("3", "強い風")])
             + slider("px", "ゴムをのばす長さ", 1, 15, 5, 1, "{v} cm")
             + select("nb", "ゴムの本数", [("1", "1本"), ("2", "2本")]),
    buttons=btn("go", "▶ 走らせる", True) + btn("rep", "3回ためす") + btn("game", "🎯 ゴールゲーム") + btn("newg", "ゴールを動かす") + btn("clr", "記ろくを消す"),
    stats=stats([("s1", "今回進んだきょり", True), ("s2", "このやり方のだいたい", False), ("s3", "力の大きさ", False), ("s4", "わかること", False)]),
    legend="上：横から見たコース（メジャーは0〜10m。▼は止まった所）。ゴムの力では、車を指で左へ引いてはなすと走ります（スタートの台と車は大きくかいています）。下：進んだきょりのぼうグラフ（●＝1回ごと、ぼう＝だいたい）。同じやり方でも1回ごとに少しばらつきます。",
    article=KAZE_ARTICLE,
    faqs=[("ゴムを長くのばすと、車の進み方はどうなりますか？", "ゴムを長くのばすほど、もとにもどろうとする力が大きくなり、車は遠くまで進みます。このシミュレーションでは、ゴム1本を5cmのばすと約%s、10cmのばすと約%s進みます。" % (fmtd(rub_dist(1, 5)), fmtd(rub_dist(1, 10)))),
          ("風を強くすると、車の進み方はどうなりますか？", "風が強いほど、帆をおす力が大きくなり、車は遠くまで進みます。このシミュレーションでは、弱い風で約%s、強い風で約%s進みます。" % (fmtd(WD[1]), fmtd(WD[3]))),
          ("ゴムの本数をふやすと、どうなりますか？", "ゴムの力が大きくなり、車は遠くまで進みます。同じ長さだけのばすなら、2本にすると1本のときの約2倍進みます。"),
          ("同じやり方なのに、進んだきょりが毎回ちがうのはなぜですか？", "車の置き方や手のはなし方、ゆかのようすなどが毎回少しずつちがうからです。1回だけで決めずに、3回くらいためして「だいたいこのくらい」と考えます。"),
          ("ゴムを使う実験で気をつけることは？", "ゴムを強く引っぱりすぎると切れたり、手や顔に当たったりします。のばす長さを決めて、人のいる方に向けないようにしましょう。")],
    rel=[("kuuki-mizu", "💉", "とじこめた空気と水"), ("bane-nobi", "🪀", "ばねののびと力"), ("furiko-jikken", "⏱️", "振り子の実験"),
         ("mono-omosa", "🧱", "物と重さ"), ("magnet", "🧲", "磁力線シミュレーター")],
    js=JS_KAZE)
