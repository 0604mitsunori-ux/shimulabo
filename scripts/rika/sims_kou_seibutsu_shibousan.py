# -*- coding: utf-8 -*-
"""理科の授業向けシミュ（高校 生物・化学：脂肪酸の構造と融点）— シミュラボのリクエスト（2026-11-23 受付 17d6954069／伊藤さん）から
   shibousan-yuuten … 飽和脂肪酸（ステアリン酸）・シス型不飽和脂肪酸（オレイン酸）・トランス型（エライジン酸）の分子の形・並び方・融解
   生物（2）ア（ｱ）㋐生体物質と細胞（脂質）・化学（有機化合物：油脂）
   モデル：分子の形は2次元の模式図。融点より低いと格子に並び、高いとばらばらに動く（力の計算はしていない）。融点は文献値。"""
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
  function pill(s,x,y,size,col,bg){ const w=tw(s,size,true)+16; rr(x-w/2,y-size-2,w,size+12,8); ctx.fillStyle=bg||'rgba(255,255,255,.9)'; ctx.fill(); tx(s,x,y+2,size,col,'center',true); }
  const sm=v=>{ v=clamp(v,0,1); return v*v*(3-2*v); }, PI=Math.PI, lerp=(a,b,k)=>a+(b-a)*k;
  const angd=(a,b)=>{ let d=b-a; while(d>PI) d-=2*PI; while(d<-PI) d+=2*PI; return d; };
  const mixc=(a,b,k)=>'rgb('+a.map((v,i)=>Math.round(v+(b[i]-v)*k)).join(',')+')';

  // ===== 物質（炭素数はどれも18。融点は文献値） =====
  const SUB={ st:{name:'ステアリン酸',kind:'飽和脂肪酸',f:'C₁₇H₃₅COOH',mp:69.6,db:'なし（すべて単結合）',col:'#334155',kink:0,sp:12.5,sh:0,tilt:0},
              ol:{name:'オレイン酸',kind:'不飽和脂肪酸（シス型）',f:'C₁₇H₃₃COOH',mp:13.4,db:'シス型が1個',col:'#0f766e',kink:.7,sp:18,sh:7,tilt:.07},
              el:{name:'エライジン酸',kind:'不飽和脂肪酸（トランス型）',f:'C₁₇H₃₃COOH',mp:45,db:'トランス型が1個',col:'#6d28d9',kink:0,sp:13.5,sh:2.5,tilt:.02} };
  const PX=[0,324], PW=316, PY=58, PH=342, ROWS=11, NB=17;
  function atoms(S,hx,hy,ang,b,dd,sg){ const pts=[[hx,hy]]; let ax=ang, x=hx, y=hy; for(let k=0;k<NB;k++){ ax+=sg*dd[k]; if(k===8) ax+=sg*S.kink; const th=ax+sg*(k%2?-1:1)*.5236; x+=b*Math.cos(th); y+=b*Math.sin(th); pts.push([x,y]); } return pts; }
  let t=0, Tc=25, paused=false, names=true, showC=true, panels=[null,null], single=[null,null];
  function mkPanel(i,key){ const S=SUB[key], ms=[]; const y0=PY+PH/2+6-(ROWS-1)*S.sp/2-(S.kink?18:0);
    for(let c=0;c<2;c++) for(let r=0;r<ROWS;r++){ const sh=(Math.random()-.5)*2*S.sh, tl=(Math.random()-.5)*2*S.tilt;
      ms.push({c:c,r:r,hx:PX[i]+(c?PW-16-sh:16+sh),hy:y0+r*S.sp,ang:c?PI-tl:tl,sg:c?-1:1,off:Math.min(r,ROWS-1-r)/(ROWS/2)*.55+Math.random()*.2,
        lx:PX[i]+rnd(30,PW-30),ly:PY+rnd(40,PH-40),la:rnd(0,6.28),lv:rnd(0,6.28),ph:rnd(0,6.28),tg:new Array(NB).fill(0),cu:new Array(NB).fill(0),m:0,pts:null}); }
    return {i:i,key:key,S:S,g:Tc>=S.mp?1:0,ms:ms,contact:0,links:[]}; }
  function mkSingle(key){ return {key:key,S:SUB[key],tg:new Array(NB).fill(0),cu:new Array(NB).fill(0)}; }
  function setSub(){ panels=[mkPanel(0,$('subL').value),mkPanel(1,$('subR').value)]; single=[mkSingle($('subL').value),mkSingle($('subR').value)]; }
  // 単結合のまわりの回転による鎖の曲がり。pair=対になった曲がり（鎖全体の向きは変わらない）、free=向きも変わる曲がり（液体・高温）
  function wiggle(S,o,pdef,pfree,dt){ const dbl=S.db.indexOf('なし')<0, tg=o.tg, cu=o.cu; if(!o.pr){ o.pr=new Array(NB).fill(0); o.fr=new Array(NB).fill(0); }
    for(let k=1;k<NB-2;k++){ if(Math.random()>dt*1.7) continue; if(dbl&&(k===8||k+2===8)){ o.pr[k]=0; o.fr[k]=0; continue; }
      const on=Math.random()<pdef, s=Math.random()<.5?1:-1; if(on&&Math.random()<pfree){ o.fr[k]=s; o.pr[k]=0; } else { o.pr[k]=on?s:0; o.fr[k]=0; } }
    for(let k=0;k<NB;k++){ tg[k]=.7*(o.pr[k]-(k>=2?o.pr[k-2]:0)+o.fr[k]); if(dbl&&k===8) tg[k]=0; cu[k]+=(tg[k]-cu[k])*Math.min(1,dt*7); } }
  function step(dt){ t+=dt; Tc=+$('temp').value; const hot=clamp((Tc+20)/120,0,1);
    for(const P of panels){ const S=P.S, tgt=Tc>=S.mp?1:0; P.g=clamp(P.g+(tgt>P.g?1:-1)*dt/3.2,0,1); if(Math.abs(P.g-tgt)<.004) P.g=tgt;
      const v=20+hot*34, amp=.5+hot*2.4;
      for(const m of P.ms){ m.m=sm((P.g*1.75-m.off)/.75); const near=Math.pow(clamp(1-(S.mp-Tc)/40,0,1),2); wiggle(S,m,lerp(.001+.02*near,.16+.1*hot,m.m),.45*m.m,dt);
        m.lv+=randn()*Math.sqrt(dt)*2; m.lx+=Math.cos(m.lv)*v*dt; m.ly+=Math.sin(m.lv)*v*dt; m.la+=randn()*Math.sqrt(dt)*(.5+hot*.8);
        const x0=PX[P.i]+26, x1=PX[P.i]+PW-26, y0=PY+52, y1=PY+PH-30; if(m.lx<x0){m.lx=x0;m.lv=PI-m.lv;} if(m.lx>x1){m.lx=x1;m.lv=PI-m.lv;} if(m.ly<y0){m.ly=y0;m.lv=-m.lv;} if(m.ly>y1){m.ly=y1;m.lv=-m.lv;}
        const cxm=m.lx+Math.cos(m.la)*55, cym=m.ly+Math.sin(m.la)*55; if(cxm<x0-10||cxm>x1+10||cym<y0-10||cym>y1+10) m.la+=angd(m.la,Math.atan2(PY+PH/2-m.ly,PX[P.i]+PW/2-m.lx))*Math.min(1,dt*2.5);
        const k=m.m, hx=lerp(m.hx,m.lx,k)+Math.sin(t*(9+hot*8)+m.ph)*amp*(1-k), hy=lerp(m.hy,m.ly,k)+Math.cos(t*(8+hot*7)+m.ph*1.7)*amp*(1-k), ang=m.ang+angd(m.ang,m.la)*k+Math.sin(t*6+m.ph)*.012*amp*(1-k);
        m.pts=atoms(S,hx,hy,ang,9,m.cu,m.sg); }
      // となりの分子と接している部分
      let n=0; P.links=[]; for(const a of P.ms){ if(a.m>.5||a.r===ROWS-1) continue; const b=P.ms[a.c*ROWS+a.r+1]; if(b.m>.5) continue;
        for(let i=0;i<=NB;i++){ let best=1e9,bj=0; for(let j=Math.max(0,i-4);j<=Math.min(NB,i+4);j++){ const d=Math.hypot(a.pts[i][0]-b.pts[j][0],a.pts[i][1]-b.pts[j][1]); if(d<best){best=d;bj=j;} } if(best<15.6){ n++; if(i%2===0) P.links.push([(a.pts[i][0]+b.pts[bj][0])/2,(a.pts[i][1]+b.pts[bj][1])/2]); } } }
      P.contact=n/((ROWS-1)*2*(NB+1)); }
    for(const s of single) wiggle(s.S,s,.01+.26*hot,0,dt);
  }
  // ===== 描く =====
  function dChain(S,pts,sc,det){ ctx.lineJoin='round'; ctx.lineCap='round'; ctx.strokeStyle=S.col; ctx.lineWidth=2.4*sc; ctx.beginPath(); pts.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1])); ctx.stroke();
    if(S.db.indexOf('なし')<0){ const a=pts[8], b=pts[9], dx=b[0]-a[0], dy=b[1]-a[1], l=Math.hypot(dx,dy), nx=-dy/l*2.3*sc, ny=dx/l*2.3*sc; ctx.strokeStyle='#f97316'; ctx.lineWidth=2.2*sc;
      ctx.beginPath(); ctx.moveTo(a[0]+nx,a[1]+ny); ctx.lineTo(b[0]+nx,b[1]+ny); ctx.moveTo(a[0]-nx,a[1]-ny); ctx.lineTo(b[0]-nx,b[1]-ny); ctx.stroke(); }
    if(det){ pts.forEach((p,i)=>{ if(!i) return; ctx.beginPath(); ctx.arc(p[0],p[1],3.6,0,7); ctx.fillStyle=(S.db.indexOf('なし')<0&&(i===8||i===9))?'#f97316':'#475569'; ctx.fill(); }); }
    ctx.beginPath(); ctx.arc(pts[0][0],pts[0][1],(det?7:4.3)*Math.min(1.4,sc),0,7); ctx.fillStyle='#ef4444'; ctx.fill(); ctx.strokeStyle='#7f1d1d'; ctx.lineWidth=1.1; ctx.stroke(); }
  function stateOf(P){ return P.g<=.02?'固体':P.g>=.98?'液体':(Tc>=P.S.mp?'融解中':'凝固中'); }
  function dThermo(){ const x0=44, x1=W-24, y=14, X=v=>x0+(v+20)/120*(x1-x0);
    rr(x0-6,y-5,x1-x0+12,12,6); ctx.fillStyle='#e2e8f0'; ctx.fill(); const g=ctx.createLinearGradient(x0,0,x1,0); g.addColorStop(0,'#3b82f6'); g.addColorStop(.45,'#22c55e'); g.addColorStop(.75,'#f59e0b'); g.addColorStop(1,'#ef4444');
    ctx.save(); rr(x0-6,y-5,Math.max(12,X(Tc)-x0+6),12,6); ctx.clip(); ctx.fillStyle=g; ctx.fillRect(x0-6,y-5,x1-x0+12,12); ctx.restore();
    ctx.beginPath(); ctx.arc(X(Tc),y+1,8,0,7); ctx.fillStyle='#0f172a'; ctx.fill(); ctx.fillStyle='#fff'; ctx.beginPath(); ctx.arc(X(Tc),y+1,3.2,0,7); ctx.fill();
    tx('🌡',8,y+7,16,'#0f172a'); for(let v=-20;v<=100;v+=20) tx(v+'℃',X(v),y+25,9.5,'#94a3b8','center');
    panels.forEach(P=>{ const x=X(P.S.mp); ctx.fillStyle=P.S.col; ctx.beginPath(); ctx.moveTo(x,y+8); ctx.lineTo(x-5,y+16); ctx.lineTo(x+5,y+16); ctx.closePath(); ctx.fill(); tx(P.S.name+'の融点',clamp(x,70,W-70),y+38,9.5,P.S.col,'center',true); }); }
  function dPanelMany(P){ const x=PX[P.i], S=P.S;
    ctx.save(); rr(x,PY,PW,PH,10); ctx.clip(); ctx.fillStyle=mixc([239,246,255],[255,247,237],P.g); ctx.fillRect(x,PY,PW,PH);
    if(showC){ for(const l of P.links){ ctx.fillStyle='rgba(34,197,94,.42)'; ctx.beginPath(); ctx.arc(l[0],l[1],4.6,0,7); ctx.fill(); } }
    for(const m of P.ms) dChain(S,m.pts,1,false);
    pill(S.name+'（'+S.kind+'）',x+PW/2,PY+20,12,'#fff',S.col);
    const st=stateOf(P); pill(st,x+PW-36,PY+48,13,'#fff',st==='固体'?'#2563eb':st==='液体'?'#ea580c':'#a16207');
    ctx.restore(); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1; rr(x+.5,PY+.5,PW-1,PH-1,10); ctx.stroke(); }
  function dPanelOne(P,s){ const x=PX[P.i], S=P.S; ctx.save(); rr(x,PY,PW,PH,10); ctx.clip(); ctx.fillStyle='#fff'; ctx.fillRect(x,PY,PW,PH);
    const pts=atoms(S,x+30,PY+(S.kink?92:128),0,15.5,s.cu,1); dChain(S,pts,1.5,true);
    pill(S.name+'（'+S.kind+'）',x+PW/2,PY+20,12,'#fff',S.col);
    const by0=PY+PH-74;
    if(names){ tx('−COOH（カルボキシ基）',pts[0][0]-10,pts[0][1]+28,10.5,'#b91c1c','left',true);
      // 単結合：回転できる
      [4,13].forEach((k,q)=>{ const a=pts[k], b=pts[k+1], mx=(a[0]+b[0])/2, my=(a[1]+b[1])/2, r=11, a0=t*3+q*2; ctx.strokeStyle='#2563eb'; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(mx,my,r,a0,a0+4.4); ctx.stroke();
        const ex=mx+Math.cos(a0+4.4)*r, ey=my+Math.sin(a0+4.4)*r, ta=a0+4.4+PI/2; ctx.fillStyle='#2563eb'; ctx.beginPath(); ctx.moveTo(ex+Math.cos(ta)*6,ey+Math.sin(ta)*6); ctx.lineTo(ex+Math.cos(ta+2.5)*5,ey+Math.sin(ta+2.5)*5); ctx.lineTo(ex+Math.cos(ta-2.5)*5,ey+Math.sin(ta-2.5)*5); ctx.closePath(); ctx.fill(); });
      tx('↻ 単結合のまわりは回転できる（青い矢印）',x+PW/2,PY+50,11,'#1d4ed8','center',true);
      if(S.db.indexOf('なし')<0){ const a=pts[8], b=pts[9], mx=(a[0]+b[0])/2, my=(a[1]+b[1])/2, cis=S.kink>0;
        const dx=b[0]-a[0], dy=b[1]-a[1], l=Math.hypot(dx,dy), nx=-dy/l, ny=dx/l; const sA=-1, sB=cis?-1:1;
        [[a,sA],[b,sB]].forEach(o=>{ const hx=o[0][0]+nx*15*o[1], hy=o[0][1]+ny*15*o[1]; ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1.6; ctx.beginPath(); ctx.moveTo(o[0][0],o[0][1]); ctx.lineTo(hx,hy); ctx.stroke(); ctx.beginPath(); ctx.arc(hx,hy,6,0,7); ctx.fillStyle='#fff'; ctx.fill(); ctx.strokeStyle='#64748b'; ctx.stroke(); tx('H',hx,hy+3.5,9,'#334155','center',true); });
        const ly=by0-44; rr(x+10,ly-15,PW-20,52,8); ctx.fillStyle='#fff7ed'; ctx.fill(); ctx.strokeStyle='#fdba74'; ctx.lineWidth=1; ctx.setLineDash([3,3]); ctx.beginPath(); ctx.moveTo(mx,my+8); ctx.lineTo(mx,ly-15); ctx.stroke(); ctx.setLineDash([]);
        tx('C=C 二重結合（'+(cis?'シス型':'トランス型')+'）：ここは回転できない',x+PW/2,ly+1,11,'#c2410c','center',true); tx(cis?'2つの H が同じ側 → 鎖がここで折れ曲がる':'2つの H が反対側 → 鎖はほぼまっすぐ',x+PW/2,ly+18,11,'#c2410c','center',true); tx('（H は二重結合の炭素についたものだけ表示）',x+PW/2,ly+32,9.5,'#9a3412','center',false); }
      else { const ly=by0-44; rr(x+10,ly-15,PW-20,52,8); ctx.fillStyle='#f1f5f9'; ctx.fill(); tx('炭素どうしはすべて単結合',x+PW/2,ly+1,11,'#334155','center',true); tx('低温ではまっすぐ伸びた形が多く、',x+PW/2,ly+18,11,'#334155','center',false); tx('高温ではあちこちで曲がる',x+PW/2,ly+32,11,'#334155','center',false); }
    }
    const by=PY+PH-74; rr(x+10,by,PW-20,64,8); ctx.fillStyle='#f8fafc'; ctx.fill();
    tx('示性式 '+S.f+'（炭素18個）',x+20,by+19,11.5,'#0f172a','left',true); tx('C=C 二重結合：'+S.db,x+20,by+37,11.5,'#0f172a','left',false); tx('融点 約'+S.mp+'℃',x+20,by+55,11.5,S.col,'left',true);
    ctx.restore(); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1; rr(x+.5,PY+.5,PW-1,PH-1,10); ctx.stroke(); }
  function dInfo(P){ const x=PX[P.i], y=PY+PH+8, S=P.S, st=stateOf(P); rr(x,y,PW,70,10); ctx.fillStyle='#fff'; ctx.fill(); ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; ctx.stroke();
    tx('融点 約'+S.mp+'℃',x+12,y+20,12.5,S.col,'left',true); tx('いま '+Tc+'℃ → '+st,x+PW-12,y+20,12.5,'#0f172a','right',true);
    tx('規則正しく並んで接している部分 '+Math.round(P.contact*100)+'%',x+12,y+40,11,'#0f172a','left',false); rr(x+12,y+48,PW-24,9,4.5); ctx.fillStyle='#e2e8f0'; ctx.fill(); if(P.contact>.01){ rr(x+12,y+48,Math.max(9,(PW-24)*Math.min(1,P.contact)),9,4.5); ctx.fillStyle='#22c55e'; ctx.fill(); } }
  function wrap(s,maxw,size){ const out=[]; let c=''; for(const ch of s){ if(tw(c+ch,size,false)>maxw){ out.push(c); c=ch; } else c+=ch; } if(c) out.push(c); return out; }
  function caption(){ const a=panels[0], b=panels[1], sa=stateOf(a), sb=stateOf(b);
    if($('view').value==='one') return '1分子の形を比べます。単結合のまわりは回転できるので、温度が高いほど鎖はいろいろな形に曲がります。二重結合のまわりは回転できず、シス型では鎖がそこで折れ曲がったままです。';
    if(sa==='固体'&&sb==='固体') return 'どちらも固体です。まっすぐな鎖は近づいて規則正しく並び、分子どうしが広い範囲で接します（緑の点）。折れ曲がった鎖は、すき間が大きくなります。温度を上げてみましょう。';
    if(sa==='液体'&&sb==='液体') return 'どちらも液体です。規則正しい並びがくずれ、分子はたがいの位置を変えながら動いています。融けても、分子の中の炭素の鎖や二重結合はそのままです。';
    return a.S.name+'は'+sa+'、'+b.S.name+'は'+sb+'です。炭素の数は同じ18個でも、分子どうしが接する部分が少ないほど引き合う力が弱く、低い温度で規則正しい並びがくずれます（融点が低い）。'; }
  function draw(){ ctx.clearRect(0,0,W,H); ctx.fillStyle='#f8fafc'; ctx.fillRect(0,0,W,H); dThermo();
    const one=$('view').value==='one';
    panels.forEach((P,i)=>{ if(one) dPanelOne(P,single[i]); else dPanelMany(P); dInfo(P); });
    if(paused) pill('一時停止中',W/2,PY+80,13,'#0f172a','rgba(255,255,255,.95)');
    if(names&&!one){ rr(W/2-150,PY+PH-28,300,22,7); ctx.fillStyle='rgba(255,255,255,.92)'; ctx.fill(); let x=W/2-140; ctx.beginPath(); ctx.arc(x+4,PY+PH-17,4.3,0,7); ctx.fillStyle='#ef4444'; ctx.fill(); tx('カルボキシ基',x+12,PY+PH-13,10.5,'#0f172a','left',true);
      x+=92; ctx.strokeStyle='#f97316'; ctx.lineWidth=2.2; ctx.beginPath(); ctx.moveTo(x,PY+PH-19); ctx.lineTo(x+14,PY+PH-19); ctx.moveTo(x,PY+PH-15); ctx.lineTo(x+14,PY+PH-15); ctx.stroke(); tx('二重結合',x+18,PY+PH-13,10.5,'#0f172a','left',true);
      x+=72; ctx.fillStyle='rgba(34,197,94,.6)'; ctx.beginPath(); ctx.arc(x+4,PY+PH-17,4.6,0,7); ctx.fill(); tx('分子どうしが接している所',x+12,PY+PH-13,10.5,'#0f172a','left',true); }
    const cy=PY+PH+86; rr(0,cy,W,H-cy,10); ctx.fillStyle='#fff'; ctx.fill(); ctx.strokeStyle='#e2e8f0'; ctx.stroke(); wrap(caption(),W-28,12.5).slice(0,4).forEach((l,i)=>tx(l,14,cy+21+i*18,12.5,'#0f172a','left',false));
    setStat('sT',Tc+' ℃'); setStat('sL',stateOf(panels[0])); setStat('sR',stateOf(panels[1])); setStat('sCL',Math.round(panels[0].contact*100)+' %'); setStat('sCR',Math.round(panels[1].contact*100)+' %');
    setShare('【脂肪酸の融点】'+Tc+'℃で、'+panels[0].S.name+'は'+stateOf(panels[0])+'、'+panels[1].S.name+'は'+stateOf(panels[1])+'。炭素数は同じでも、鎖の形で融点が変わる｜シミュラボ'); }
  function loop(){ if(!paused){ const sp=+$('spd').value, n=Math.max(1,Math.round(sp*2)); for(let i=0;i<n;i++) step(1/120); } draw(); requestAnimationFrame(loop); }
  $('subL').addEventListener('change',setSub); $('subR').addEventListener('change',setSub);
  $('pause').addEventListener('click',()=>{ paused=!paused; $('pause').textContent=paused?'▶ 再開':'⏸ 一時停止'; });
  $('names').addEventListener('click',()=>{ names=!names; $('names').textContent=names?'🏷 名前をかくす':'🏷 名前を表示'; });
  $('cont').addEventListener('click',()=>{ showC=!showC; $('cont').textContent=showC?'🟢 接している所をかくす':'🟢 接している所を表示'; });
  [['t0',0],['t30',30],['t50',50],['t80',80]].forEach(o=>$(o[0]).addEventListener('click',()=>{ $('temp').value=o[1]; $('temp').dispatchEvent(new Event('input')); }));
  window.__test={step:function(s){ const n=Math.round(s*60); for(let i=0;i<n;i++) step(1/60); draw(); },get s(){ return {T:Tc,L:[panels[0].key,stateOf(panels[0]),+panels[0].g.toFixed(2),Math.round(panels[0].contact*100)],R:[panels[1].key,stateOf(panels[1]),+panels[1].g.toFixed(2),Math.round(panels[1].contact*100)]}; }};
  $('subR').value='ol'; setSub(); step(1/60); loop();
'''

ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
<p>脂肪酸は、長い炭化水素の鎖の端にカルボキシ基（−COOH）がついた分子です。鎖の炭素どうしがすべて単結合のものを<b>飽和脂肪酸</b>、C=C 二重結合をもつものを<b>不飽和脂肪酸</b>といいます。このシミュレーターでは、炭素数が同じ18個のステアリン酸（飽和）、オレイン酸（シス型の不飽和）、エライジン酸（トランス型の不飽和）について、1分子の形、多数の分子の並び方、温度を変えたときの融解のようすを比べることができます。</p>
''' + N('<b>対応する単元</b>：高等学校「生物」（2）生命現象と物質 ア（ｱ）細胞と分子「㋐生体物質と細胞」（脂質・生体膜の流動性の理解の基礎）、高等学校「化学」有機化合物（油脂：飽和脂肪酸と不飽和脂肪酸、脂肪と脂肪油、硬化油）。') + '''
<h2>授業での使い方</h2>
<h3>導入：1分子の形を比べる</h3>
<p>「表示」を「1分子の構造」にして、ステアリン酸とオレイン酸を並べます。単結合のまわりは回転できるので、温度を上げると鎖はいろいろな形に曲がり、温度を下げるとまっすぐ伸びた形が多くなります。二重結合（オレンジ色）のまわりは回転できず、シス型では2つの H が同じ側にあるため、鎖がそこで折れ曲がったままです。ここで「どちらが密に並びやすいだろう」「温度を上げると、どちらが先に融けるだろう」と予想させます。</p>
<h3>展開：並び方と融解を確かめる</h3>
<p>「多数の分子（並び方と融解）」にもどし、温度を0℃にします。ステアリン酸はまっすぐな鎖がすき間なく並び、緑の点（分子どうしが接している所）が鎖の全体にあります。オレイン酸は折れ曲がりのために間があき、接している所が少なくなります。温度を少しずつ上げると、オレイン酸は約13℃で並びがくずれて液体になり、ステアリン酸は約70℃まで固体のままです。</p>
<h3>発展：シス型とトランス型</h3>
<p>右の物質をエライジン酸（トランス型）に替えると、同じ二重結合をもっていても鎖はほぼまっすぐで、ステアリン酸に近い並び方になり、融点は約45℃とオレイン酸よりずっと高くなります。二重結合があるかどうかだけでなく、立体的な配置が物質の性質に関わることがわかります。</p>
<h3>生徒への問いの例</h3>
<ol>
<li>炭素の数が同じなのに、オレイン酸の融点がステアリン酸より低いのはなぜだろう？分子の形と並び方から説明しよう。</li>
<li>融けて液体になったとき、分子の中の炭素の鎖や二重結合はどうなっているだろう？</li>
<li>シス型とトランス型では、どちらの融点が高いだろう？その理由を鎖の形から考えよう。</li>
</ol>
<h2>しくみ・解説</h2>
<h3>用語</h3>
<ul>
<li><b>脂肪酸</b>とは、炭化水素の鎖にカルボキシ基（−COOH）が1個ついた化合物です。油脂やリン脂質の成分です。</li>
<li><b>飽和脂肪酸</b>とは、炭化水素の鎖の炭素どうしの結合がすべて単結合である脂肪酸です。</li>
<li><b>不飽和脂肪酸</b>とは、炭化水素の鎖に C=C 二重結合をもつ脂肪酸です。</li>
<li><b>シス型・トランス型</b>とは、二重結合の炭素についた原子や鎖の向きのちがいによる立体的な配置です。同じ側にあるものをシス型、反対側にあるものをトランス型といいます。天然の不飽和脂肪酸の多くはシス型です。</li>
<li><b>融点</b>とは、固体が融けて液体になる温度です。</li>
</ul>
<h3>3つの脂肪酸の比較</h3>
''' + T([["ステアリン酸", "C₁₇H₃₅COOH", "なし", "まっすぐ伸びやすい", "約70℃（69.6℃）"],
          ["オレイン酸", "C₁₇H₃₃COOH", "シス型が1個", "二重結合で折れ曲がる", "約13℃（13.4℃）"],
          ["エライジン酸", "C₁₇H₃₃COOH", "トランス型が1個", "ほぼまっすぐ", "約45℃"]],
         ["脂肪酸", "示性式", "C=C 二重結合", "鎖の形", "融点"]) + '''
<h3>形と融点がつながる理由</h3>
<p>分子と分子のあいだには、近づくほど強くはたらく弱い引力（ファンデルワールス力）があります。まっすぐな鎖どうしは、広い範囲で近づいて規則正しく並べるので、全体として引き合う力が大きく、その並びをくずすには高い温度（大きな熱運動）が必要です。シス型の二重結合で折れ曲がった鎖は、となりの分子と近づける部分が少なく、引き合う力が小さいため、低い温度で並びがくずれて液体になります。</p>
''' + P('融解でくずれるのは「分子どうしの並び方」です。分子の中の共有結合（炭素の鎖や二重結合）は切れません。') + '''
<h3>生物や食品とのつながり</h3>
<p>細胞膜をつくるリン脂質にも、飽和脂肪酸と不飽和脂肪酸がふくまれています。折れ曲がった不飽和脂肪酸が多いほど、膜の中の分子は密に並びにくく、低い温度でも膜のやわらかさ（流動性）が保たれます。食品では、不飽和脂肪酸を多くふくむ植物油は常温で液体、飽和脂肪酸を多くふくむ牛脂やバターは常温で固体です。植物油に水素を付加して二重結合を減らすと、融点が上がって固体になります（硬化油）。</p>
<h3>このシミュレーターのモデル</h3>
<p>分子の形と動きは、構造と状態変化の関係をとらえるための、平面上の模式的な表現です。分子どうしの力を計算したものではなく、融点（文献値）より低い温度では分子を規則正しく並べ、高い温度ではばらばらに動かしています。実際の結晶の中の並び方は立体的で、ここに描いたものより複雑です。融点は測定条件や結晶の形によって少し異なり、オレイン酸は13〜16℃、エライジン酸は43〜45℃とする資料もあります。</p>
<h2>参考</h2>
<ul>
<li>''' + A(MEXT_KOU, "文部科学省 高等学校学習指導要領（平成30年告示）解説 理科編") + '''（生物（2）生命現象と物質、化学 有機化合物）</li>
<li>高等学校「化学」「生物」の教科書（油脂と脂肪酸、生体膜）、日本化学会編「化学便覧」（脂肪酸の融点）</li>
</ul>
'''

SUBS = [("st", "ステアリン酸（飽和）"), ("ol", "オレイン酸（シス型の不飽和）"), ("el", "エライジン酸（トランス型の不飽和）")]

sim(slug="shibousan-yuuten", cat="rika", emoji="🧈", score=79,
    title="脂肪酸の構造と融点シミュレーター（飽和・不飽和、シス型・トランス型）",
    title_tag="飽和脂肪酸と不飽和脂肪酸の融点シミュレーター｜シス型の折れ曲がりと分子の並び方（高校生物・化学）",
    meta_desc="炭素数18のステアリン酸・オレイン酸・エライジン酸を比べ、二重結合による鎖の折れ曲がりが、分子の並び方と融点のちがいにつながる様子を観察できるシミュレーター。温度を変えると、規則正しい並びがくずれて融解する様子と、1分子の単結合の回転・シス型とトランス型の形を見られます。",
    og_title="脂肪酸の構造と融点シミュレーター（飽和・不飽和、シス型・トランス型）",
    og_desc="炭素の数は同じ18個。まっすぐな鎖はぎっしり並んで70℃まで固体、シス型で折れ曲がった鎖は13℃で融ける。分子の形・並び方・温度を1つの画面でつなげて見る。",
    card_desc="ステアリン酸・オレイン酸・エライジン酸の鎖の形と並び方を比べ、温度を上げて融ける順番を確かめる。",
    lead="左右に、炭素数が同じ18個の脂肪酸を並べています。赤い丸がカルボキシ基、ジグザグの線が炭化水素の鎖、オレンジの二重線が C=C 二重結合です。温度のスライダーを動かすと、分子の熱運動が変わり、融点をこえた物質は規則正しい並びがくずれて液体になります。鎖の形と、並び方、融点のつながりを確かめてみましょう。",
    model="生物 細胞と分子（脂質）／化学 油脂（飽和脂肪酸と不飽和脂肪酸・融点）",
    level="高校（生物・化学）",
    unit="高等学校 生物（2）生命現象と物質 ア（ｱ）細胞と分子 ㋐生体物質と細胞",
    canvas=canvas(640, 570, light=True),
    controls=slider("temp", "温度", -20, 100, 25, 1, "{v} ℃")
             + select("view", "表示", [("many", "多数の分子（並び方と融解）"), ("one", "1分子の構造")])
             + select("subL", "左の物質", SUBS)
             + select("subR", "右の物質", SUBS)
             + select("spd", "速さ", [("1", "×1"), ("2", "×2"), ("0.5", "×0.5（ゆっくり）")]),
    buttons=btn("t0", "0℃", True) + btn("t30", "30℃", True) + btn("t50", "50℃", True) + btn("t80", "80℃", True) + btn("pause", "⏸ 一時停止") + btn("cont", "🟢 接している所をかくす") + btn("names", "🏷 名前をかくす"),
    stats=stats([("sT", "温度", True), ("sL", "左の物質の状態", False), ("sR", "右の物質の状態", False), ("sCL", "接している部分（左）", False), ("sCR", "接している部分（右）", False)]),
    legend=PH + "赤い丸＝カルボキシ基（−COOH）、ジグザグの線＝炭化水素の鎖（角が炭素原子）、オレンジの二重線＝C=C 二重結合、緑の点＝となりの分子と近くで接している所。上の温度計の▲は、それぞれの物質の融点です。分子の形と動きは平面上の模式図です。",
    article=ARTICLE,
    faqs=[("不飽和脂肪酸の融点が飽和脂肪酸より低いのはなぜ？", "天然の不飽和脂肪酸の多くはシス型の二重結合をもち、鎖がそこで折れ曲がっています。折れ曲がった鎖は、となりの分子と近づいて規則正しく並べる部分が少ないため、分子どうしの引き合う力が小さくなり、低い温度で並びがくずれて液体になります。"),
          ("シス型とトランス型は何がちがうの？", "二重結合の炭素についた原子や鎖の向きがちがいます。二重結合のまわりは回転できないので、同じ側にあるシス型と、反対側にあるトランス型は別の物質です。シス型は鎖が折れ曲がり、トランス型は鎖がほぼまっすぐなので、トランス型の方が密に並びやすく、融点が高くなります（オレイン酸 約13℃、エライジン酸 約45℃）。"),
          ("融けると分子はこわれるの？", "こわれません。融解でくずれるのは、分子どうしの規則正しい並び方です。分子の中の共有結合はそのままなので、炭素の鎖や二重結合は保たれています。冷やせば再び固体になります。"),
          ("単結合は回転できて、二重結合は回転できないのはなぜ？", "単結合では、結合している2つの原子が結合を軸にして回転しても結合は保たれます。二重結合は2組の電子対で結びついており、回転するには一方の結合を切らなければならないため、ふつうの温度では回転できません。そのため、シス型・トランス型という配置のちがいが保たれます。"),
          ("細胞膜と何か関係があるの？", "細胞膜のリン脂質は脂肪酸の鎖を2本もっています。折れ曲がった不飽和脂肪酸をふくむリン脂質が多いと、膜の中で分子が密に並びにくくなり、低い温度でも膜の流動性（やわらかさ）が保たれます。寒い環境の生物では、膜の不飽和脂肪酸の割合が高い例が知られています。"),
          ("植物油が液体で、バターや牛脂が固体なのはなぜ？", "植物油はオレイン酸やリノール酸などの不飽和脂肪酸を多くふくむ油脂で、融点が低いため常温で液体です。バターや牛脂はパルミチン酸やステアリン酸などの飽和脂肪酸を多くふくみ、融点が高いため常温で固体です。")],
    rel=[("sekken-shabondama", "🫧", "セッケン・シャボン玉・細胞膜のシミュレーター"), ("rinshishitsu-maku", "🧼", "リン脂質と細胞膜のでき方シミュレーター"),
         ("joutai-henka", "🧊", "状態変化と粒子のシミュレーター"), ("maku-yuso", "🚪", "膜輸送のシミュレーター"), ("kouso-shikkatsu", "🌡️", "酵素の失活シミュレーター")],
    js=JS)
