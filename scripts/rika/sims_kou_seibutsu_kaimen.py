# -*- coding: utf-8 -*-
"""理科の授業向けシミュ（高校 生物・化学：親水部と疎水部をもつ分子の並び方）— シミュラボのリクエスト（2026-11-23 受付 116a3e351a／伊藤さん）から
   sekken-shabondama … 水面／油汚れ／ミセル／シャボン玉の膜／リン脂質二重層と小胞／膜の比較 の6場面
   生物（2）ア（ｱ）㋐生体物質と細胞（生体膜）・化学（有機化合物：油脂とセッケン）
   モデル：分子はばらばらに動いたあと、場面ごとの「並ぶ場所」に引き寄せられる模式的な表現（力の計算はしていない）。"""
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
  const sm=v=>{ v=clamp(v,0,1); return v*v*(3-2*v); }, lerp=(a,b,k)=>a+(b-a)*k, PI=Math.PI, TL=20;
  const VW=640, VH=430;
  function stride(n){ const a=[]; for(let i=0;i<n;i++) a.push(i); const f=i=>(i*.6180339887)%1; return a.sort((p,q)=>f(p)-f(q)); }

  let scene='surface', t=0, M=[], slots=[], paused=false, hide=false, names=true, note='', noteT=0;
  const st={stir:0,stirOn:false,oil:false,zoom:0,zoomOn:false,bend:0,bendOn:false};

  // ===== 場面ごとの「並ぶ場所」 =====
  const DROP=[[170,140],[330,245],[490,150]];
  function oilGeo(){ if(st.stir<.45){ const k=sm(st.stir/.45); return {type:'e',rx:lerp(120,61,k),ry:lerp(62,61,k),cx:320,cy:lerp(400,328,k)}; }
    const k=sm((st.stir-.45)/.55); return {type:'d',r:lerp(61,35,k),c:DROP.map((d,i)=>[lerp(320,d[0],k)+Math.sin(t*.7+i*2)*5*k,lerp(328,d[1],k)+Math.cos(t*.6+i)*5*k])}; }
  function oilSlot(j){ const g=oilGeo();
    if(g.type==='e'){ const ph=-PI/2+(j%2?1:-1)*Math.ceil(j/2)*(2*PI/45), px=g.cx+g.rx*Math.cos(ph), py=g.cy+g.ry*Math.sin(ph); if(py>392) return null;
      let nx=Math.cos(ph)/g.rx, ny=Math.sin(ph)/g.ry; const l=Math.hypot(nx,ny); nx/=l; ny/=l; return [px+nx*5,py+ny*5,Math.atan2(-ny,-nx)]; }
    const d=j%3, a=(Math.floor(j/3)+d/3)/15*2*PI, c=g.c[d]; return [c[0]+Math.cos(a)*(g.r+5),c[1]+Math.sin(a)*(g.r+5),a+PI]; }
  function inOil(x,y,pad){ if(scene==='oil'){ const g=oilGeo(); if(g.type==='e'){ const dx=(x-g.cx)/(g.rx+pad), dy=(y-g.cy)/(g.ry+pad); return dx*dx+dy*dy<1; } return g.c.some(c=>Math.hypot(x-c[0],y-c[1])<g.r+pad); }
    if(scene==='micelle'&&st.oil) return Math.hypot(x-320,y-225)<46+pad; return false; }
  function bendPos(idx,leaf){ const L=448, k=sm(st.bend), kap=Math.max(1e-4,k*2*PI/L), s=-L/2+7+idx*14, Y0=215+k*71;
    const cx=320+Math.sin(kap*s)/kap, cy=Y0-(1-Math.cos(kap*s))/kap, nx=-Math.sin(kap*s), ny=-Math.cos(kap*s), sd=leaf?-1:1;
    return [cx+nx*24*sd,cy+ny*24*sd,Math.atan2(-ny*sd,-nx*sd)]; }
  function build(){ const S=[]; const fix=(g,kind,x,y,th)=>S.push({g:g,kind:kind,pos:()=>[x,y,th]});
    const mic=(cx,cy,n)=>stride(n).forEach(i=>{ const a=i/n*2*PI; fix('mic',1,cx+Math.cos(a)*26,cy+Math.sin(a)*26,a+PI); });
    if(scene==='surface'){ stride(41).forEach(i=>fix('if',1,16+i*15.2,157,-PI/2)); for(let i=0;i<8;i++) S.push({g:'free',kind:1}); mic(170,300,14); mic(455,290,14); mic(315,370,14); }
    if(scene==='oil'){ for(let j=0;j<45;j++) S.push({g:'oil',kind:1,pos:()=>oilSlot(j)}); }
    if(scene==='micelle'){ for(let i=0;i<10;i++) S.push({g:'free',kind:1}); if(st.oil) stride(22).forEach(i=>{ const a=i/22*2*PI; fix('oil',1,320+Math.cos(a)*51,225+Math.sin(a)*51,a+PI); }); mic(150,130,14); mic(480,120,14); mic(190,330,14); mic(490,320,14); }
    if(scene==='bubble'){ stride(82).forEach(i=>{ const up=i%2===0, k=Math.floor(i/2); fix('if',1,16+k*15.2,up?187:243,up?-PI/2:PI/2); }); }
    if(scene==='bilayer'){ stride(64).forEach(i=>{ const leaf=i%2, k=Math.floor(i/2); S.push({g:'if',kind:2,pos:()=>bendPos(k,leaf)}); }); }
    if(scene==='compare'){ stride(38).forEach((i,q)=>{ const up=i%2===0, k=Math.floor(i/2); fix('if',1,22+k*15,up?187:243,up?-PI/2:PI/2);
        const j=stride(40)[q], leaf=j%2, k2=Math.floor(j/2); fix('if',2,345+k2*14.4,leaf?239:191,leaf?-PI/2:PI/2); });
      [38,39].forEach(q=>{ const j=stride(40)[q], leaf=j%2, k2=Math.floor(j/2); fix('if',2,345+k2*14.4,leaf?239:191,leaf?-PI/2:PI/2); }); }
    slots=S; }
  function inWater(x,y,kind){ if(x<8||x>VW-8||y<8||y>VH-8) return false;
    if(scene==='surface') return y>166;
    if(scene==='oil') return y<388&&!inOil(x,y,8);
    if(scene==='micelle') return !inOil(x,y,8);
    if(scene==='bubble') return y>196&&y<234;
    if(scene==='bilayer'){ const k=sm(st.bend); if(k<.5) return Math.abs(y-215)>52||Math.abs(x-320)>250; const d=Math.hypot(x-320,215+k*71-71.3-y); return d>112||d<30; }
    if(scene==='compare') return kind===1?(x<300&&y>196&&y<234):(x>338&&Math.abs(y-215)>52);
    return true; }
  function randWater(kind){ for(let i=0;i<200;i++){ const x=rnd(10,VW-10), y=rnd(10,VH-10); if(inWater(x,y,kind)) return [x,y]; } return [VW/2,VH/2]; }
  function defKind(i){ return scene==='bilayer'?2:scene==='compare'?(i%2?2:1):1; }
  function sync(){ const n=+$('n').value; while(M.length>n) M.pop();
    while(M.length<n){ const i=M.length, k=slots[i]?slots[i].kind:defKind(i), p=randWater(k); M.push({x:p[0],y:p[1],th:rnd(0,6.28),a:rnd(0,6.28),ph:rnd(0,6.28),rel:t+rnd(.2,1.2),kind:k,ok:false}); }
    M.forEach((m,i)=>{ const s=slots[i]; m.slot=(s&&s.g!=='free')?s:null; m.kind=s?s.kind:defKind(i); }); }
  function scatter(){ M.forEach((m,i)=>{ const p=randWater(m.kind); m.x=p[0]; m.y=p[1]; m.th=rnd(0,6.28); m.rel=t+rnd(.3,1.6)+i/Math.max(1,M.length)*2.2; m.ok=false; }); }
  function setScene(){ scene=$('scene').value; st.stir=0; st.stirOn=false; st.oil=false; st.zoom=0; st.zoomOn=false; st.bend=0; st.bendOn=false; build(); M=[]; sync(); scatter(); actLabel(); }
  function actLabel(){ const b=$('act'); let s='', on=true;
    if(scene==='oil') s=st.stirOn?'↺ 油汚れをもどす':'🌀 かき混ぜる'; else if(scene==='micelle') s=st.oil?'油滴を取りのぞく':'🫒 油滴を1つ入れる';
    else if(scene==='bubble') s=st.zoomOn?'🫧 シャボン玉全体を見る':'🔍 膜の断面を拡大'; else if(scene==='bilayer') s=st.bendOn?'▭ 平らな膜にもどす':'⭕ 閉じて袋にする'; else { s='（この場面の操作はありません）'; on=false; }
    b.textContent=s; b.disabled=!on; b.style.opacity=on?1:.45; }
  function say(s){ note=s; noteT=t+3.5; }

  // ===== 動かす =====
  function step(dt){ t+=dt;
    if(scene==='oil'&&st.stirOn&&st.stir<1) st.stir=Math.min(1,st.stir+dt/4.5);
    if(scene==='bubble') st.zoom=clamp(st.zoom+(st.zoomOn?1:-1)*dt/1.4,0,1);
    if(scene==='bilayer') st.bend=clamp(st.bend+(st.bendOn?1:-1)*dt/3.2,0,1);
    const swirl=scene==='oil'&&st.stirOn&&st.stir<1;
    for(const m of M){ let p=null; if(m.slot&&t>m.rel) p=m.slot.pos();
      if(p){ const a=Math.min(1,dt*3.4); m.x+=(p[0]-m.x)*a; m.y+=(p[1]-m.y)*a; let d=p[2]-m.th; while(d>PI) d-=2*PI; while(d<-PI) d+=2*PI; m.th+=d*Math.min(1,dt*4.5); m.ok=Math.hypot(p[0]-m.x,p[1]-m.y)<7; }
      else { m.ok=false; m.a+=randn()*Math.sqrt(dt)*2.2; m.th+=randn()*Math.sqrt(dt)*2.4; let vx=Math.cos(m.a)*34, vy=Math.sin(m.a)*34;
        if(swirl){ const dx=m.x-320, dy=m.y-200, r=Math.hypot(dx,dy)+1; vx+=-dy/r*120; vy+=dx/r*120; }
        const nx=m.x+vx*dt, ny=m.y+vy*dt; if(inWater(nx,ny,m.kind)){ m.x=nx; m.y=ny; } else { m.a+=PI*rnd(.6,1.4); if(!inWater(m.x,m.y,m.kind)){ const q=randWater(m.kind); m.x+=(q[0]-m.x)*.08; m.y+=(q[1]-m.y)*.08; } } }
    } }

  // ===== 描く =====
  function dMol(m){ const th=m.th+Math.sin(t*4+m.ph)*.11, cx=Math.cos(th), cy=Math.sin(th), px=-cy, py=cx, x=m.x+Math.sin(t*5+m.ph)*.7, y=m.y+Math.cos(t*4.3+m.ph)*.7;
    const offs=m.kind===2?[-3.2,3.2]:[0];
    for(const pass of [0,1]){ ctx.strokeStyle=pass?'#facc15':'#a16207'; ctx.lineWidth=pass?2.2:3.8; ctx.lineCap='round'; ctx.lineJoin='round';
      for(const o of offs){ ctx.beginPath(); for(let u=0;u<=1.001;u+=.2){ const w=Math.sin(u*6+t*5+m.ph+o)*1.7*u, l=4+u*(TL-4); const X=x+cx*l+px*(o+w), Y=y+cy*l+py*(o+w); u?ctx.lineTo(X,Y):ctx.moveTo(X,Y); } ctx.stroke(); } }
    ctx.beginPath(); ctx.arc(x,y,m.kind===2?5.6:5,0,7); ctx.fillStyle=m.kind===2?'#e11d48':'#ef4444'; ctx.fill(); ctx.strokeStyle='#7f1d1d'; ctx.lineWidth=1.2; ctx.stroke();
    ctx.fillStyle='rgba(255,255,255,.55)'; ctx.beginPath(); ctx.arc(x-1.6,y-1.8,1.6,0,7); ctx.fill(); }
  function water(x,y,w,h){ const g=ctx.createLinearGradient(0,y,0,y+h); g.addColorStop(0,'#dbeafe'); g.addColorStop(1,'#bfdbfe'); ctx.fillStyle=g; ctx.fillRect(x,y,w,h);
    ctx.fillStyle='rgba(255,255,255,.5)'; for(let k=0;k<18;k++){ const hx=Math.abs(Math.sin(k*12.99)*43758.5)%1, hy=Math.abs(Math.sin(k*78.2)*12543.1)%1; const px=x+((hx*w+t*6*(k%2?1:-1))%w+w)%w, py=y+hy*h; if(h>30){ ctx.beginPath(); ctx.arc(px,py,1.4,0,7); ctx.fill(); } } }
  function air(x,y,w,h){ const g=ctx.createLinearGradient(0,y,0,y+h); g.addColorStop(0,'#fffdf5'); g.addColorStop(1,'#fef9e7'); ctx.fillStyle=g; ctx.fillRect(x,y,w,h); }
  function oilFill(){ ctx.fillStyle='rgba(245,158,11,.62)'; ctx.fill(); ctx.strokeStyle='#b45309'; ctx.lineWidth=1.6; ctx.stroke(); }
  function lab(s,x,y,col){ pill(s,x,y,12.5,col||'#1e3a8a','rgba(255,255,255,.82)'); }
  function dEnv(){
    if(scene==='surface'){ air(0,0,VW,160); water(0,160,VW,VH-160); ctx.strokeStyle='#60a5fa'; ctx.lineWidth=2; ctx.beginPath(); for(let x=0;x<=VW;x+=8){ const y=160+Math.sin(x*.05+t*1.5)*1.2; x?ctx.lineTo(x,y):ctx.moveTo(x,y); } ctx.stroke(); lab('空気',60,60,'#92400e'); lab('水',60,405); }
    if(scene==='oil'){ water(0,0,VW,400); ctx.fillStyle='#cbd5e1'; ctx.fillRect(0,400,VW,30); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1; for(let x=-20;x<VW;x+=14){ ctx.beginPath(); ctx.moveTo(x,430); ctx.lineTo(x+20,400); ctx.stroke(); }
      const g=oilGeo(); ctx.save(); ctx.beginPath(); ctx.rect(0,0,VW,400); ctx.clip();
      if(g.type==='e'){ ctx.beginPath(); ctx.ellipse(g.cx,g.cy,g.rx,g.ry,0,0,7); oilFill(); } else { for(const c of g.c){ ctx.beginPath(); ctx.arc(c[0],c[1],g.r,0,7); oilFill(); } }
      ctx.restore();
      if(st.stirOn&&st.stir<1){ ctx.strokeStyle='rgba(255,255,255,.75)'; ctx.lineWidth=3; for(let k=0;k<5;k++){ const r=70+k*38, a=t*2.4+k*1.3; ctx.beginPath(); ctx.arc(320,200,r,a,a+1.1); ctx.stroke(); } }
      lab('水',50,36); lab('物の表面（布・食器など）',VW-110,420,'#334155'); const c=g.type==='e'?[g.cx,Math.min(380,g.cy-10)]:g.c[1]; tx('油',c[0],c[1]+5,14,'#78350f','center',true); if(g.type==='d'&&st.stir>.8){ tx('油',g.c[0][0],g.c[0][1]+5,14,'#78350f','center',true); tx('油',g.c[2][0],g.c[2][1]+5,14,'#78350f','center',true); } }
    if(scene==='micelle'){ water(0,0,VW,VH); if(st.oil){ ctx.beginPath(); ctx.arc(320,225,46,0,7); oilFill(); tx('油',320,230,14,'#78350f','center',true); } lab('水',50,36); }
    if(scene==='bubble'){ air(0,0,VW,180); water(0,180,VW,70); air(0,250,VW,VH-250); ctx.strokeStyle='#60a5fa'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(0,180); ctx.lineTo(VW,180); ctx.moveTo(0,250); ctx.lineTo(VW,250); ctx.stroke();
      lab('空気（シャボン玉の外側）',120,60,'#92400e'); lab('うすい水の層',VW/2,220); lab('空気（シャボン玉の内側）',120,380,'#92400e'); }
    if(scene==='bilayer'){ water(0,0,VW,VH); const k=sm(st.bend); lab(k>.9?'水（外側）':'水',60,36); if(k<.05) lab('水',60,405); if(k>.9) lab('水（内側）',320,215+71-71.3+4);
      if(k<.9&&!hide){ const a=bendPos(0,0), b=bendPos(0,1), c=bendPos(31,0), d=bendPos(31,1); const al=(1-k/.9)*(.45+.25*Math.sin(t*5));
        [[(a[0]+b[0])/2-9,(a[1]+b[1])/2],[(c[0]+d[0])/2+9,(c[1]+d[1])/2]].forEach(p=>{ ctx.fillStyle='rgba(239,68,68,'+al+')'; ctx.beginPath(); ctx.arc(p[0],p[1],20,0,7); ctx.fill(); });
        if(k<.05&&names) tx('膜の端：疎水部が水にふれる',320,300,12,'#b91c1c','center',true); } }
    if(scene==='compare'){ air(0,0,312,180); water(0,180,312,70); air(0,250,312,VH-250); water(328,0,312,VH); ctx.fillStyle='#f8fafc'; ctx.fillRect(312,0,16,VH);
      ctx.strokeStyle='#60a5fa'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(0,180); ctx.lineTo(312,180); ctx.moveTo(0,250); ctx.lineTo(312,250); ctx.stroke();
      pill('シャボン玉の膜',156,30,13,'#fff','#0e7490'); pill('リン脂質二重層（細胞膜）',484,30,13,'#fff','#be123c');
      lab('空気',50,100,'#92400e'); lab('空気',50,340,'#92400e'); lab('水',380,100); lab('水',380,340); }
  }
  function dBubbleWhole(k){ // k=0 全体 → 1 断面へ
    ctx.save(); ctx.globalAlpha=Math.pow(1-k,1.3); const s=1+9*k; ctx.translate(320,92); ctx.scale(s,s); ctx.translate(-320,-92);
    const g0=ctx.createLinearGradient(0,0,0,VH); g0.addColorStop(0,'#e0f2fe'); g0.addColorStop(1,'#f0f9ff'); ctx.fillStyle=g0; ctx.fillRect(0,0,VW,VH);
    const R=142, cx=320, cy=235+Math.sin(t*.8)*3; const g=ctx.createLinearGradient(cx-R,cy-R,cx+R,cy+R); ['#f0abfc','#93c5fd','#6ee7b7','#fde68a','#fca5a5','#c4b5fd'].forEach((c,i)=>g.addColorStop(i/5,c));
    ctx.beginPath(); ctx.arc(cx,cy,R,0,7); ctx.fillStyle='rgba(255,255,255,.35)'; ctx.fill(); ctx.strokeStyle=g; ctx.lineWidth=7; ctx.stroke();
    ctx.strokeStyle='rgba(255,255,255,.9)'; ctx.lineWidth=5; ctx.lineCap='round'; ctx.beginPath(); ctx.arc(cx,cy,R-22,3.6,4.3); ctx.stroke(); ctx.beginPath(); ctx.arc(cx,cy,R-22,4.5,4.62); ctx.stroke();
    ctx.strokeStyle='#0f172a'; ctx.lineWidth=1.6; ctx.setLineDash([4,3]); ctx.strokeRect(cx-20,cy-R-11,40,22); ctx.setLineDash([]);
    tx('この部分の断面を拡大',cx+30,cy-R-14,12,'#0f172a','left',true); tx('空気（内側）',cx,cy+6,14,'#92400e','center',true); tx('空気（外側）',80,60,14,'#92400e','center',true); tx('シャボン玉の膜',cx,cy+R+28,13,'#0e7490','center',true);
    ctx.restore(); }
  function wrap(s,maxw,size){ const out=[]; let cur=''; for(const ch of s){ if(tw(cur+ch,size,false)>maxw){ out.push(cur); cur=ch; } else cur+=ch; } if(cur) out.push(cur); return out; }
  function caption(){
    if(scene==='surface') return '水面：親水部を水の中に、疎水部を空気の側に向けて並びます。水面がいっぱいになると、水中で疎水部を内側にした集まり（ミセル）をつくり始めます。';
    if(scene==='oil') return st.stir>=1?'油は小さな油滴になって水中に散らばりました。まわりをセッケン分子が囲み、親水部が外側を向いているので、水になじんで流されます（乳化）。':'油汚れ：疎水部を油の中に、親水部を水の側に向けて、油の表面に集まります。「かき混ぜる」を押すと、油が表面からはなれます。';
    if(scene==='micelle') return 'ミセル：濃度が高くなると、疎水部を内側に、親水部を外側の水に向けて集まります。油滴があれば、疎水部を油の中に向けて取り囲みます。';
    if(scene==='bubble') return st.zoom<.5?'シャボン玉：うすい水の膜でできていて、膜の内側も外側も空気です。「膜の断面を拡大」を押してみましょう。':'シャボン玉の膜：うすい水の層の両面にセッケン分子が並びます。親水部は水の層に、疎水部は外側・内側の空気に向きます。';
    if(scene==='bilayer') return st.bend>.9?'袋状の膜（小胞）：端がなくなり、疎水部は水にふれません。内側にも外側にも水があります。細胞膜はこのつくりです。':'リン脂質二重層：膜の両側が水です。親水部は両側の水に接し、疎水部は膜の内部で向かい合います。膜の端では疎水部が水にふれてしまいます。';
    return 'どちらも分子が2層に並びますが、シャボン玉の膜は中央が水の層、リン脂質二重層は中央に疎水部が集まります。親水部は水の側、疎水部は水のない側を向きます。'; }
  function count(){ let a=0,b=0,c=0; for(const m of M){ if(m.ok&&m.slot){ if(m.slot.g==='if') a++; else b++; } else c++; } return [a,b,c]; }
  function draw(){
    ctx.clearRect(0,0,W,H); ctx.fillStyle='#f8fafc'; ctx.fillRect(0,0,W,H);
    ctx.save(); rr(0,0,VW,VH,10); ctx.clip();
    dEnv();
    const zk=scene==='bubble'?sm(st.zoom):1;
    if(!hide){ ctx.globalAlpha=zk; for(const m of M) dMol(m); ctx.globalAlpha=1; }
    if(scene==='compare'&&!hide&&names) pill('中央＝疎水部',484,219,11.5,'#854d0e','rgba(254,249,195,.92)');
    if(scene==='compare'&&!hide&&names) pill('中央＝水',156,219,11.5,'#1e3a8a','rgba(255,255,255,.92)');
    if(scene==='bubble'&&zk<1) dBubbleWhole(zk);
    if(names&&zk>.6){ const y=VH-17; const s2=scene==='compare'?'　尾1本＝セッケン、尾2本＝リン脂質':''; const w=276+tw(s2,11,true); rr(VW-w-8,y-13,w,24,7); ctx.fillStyle='rgba(255,255,255,.9)'; ctx.fill(); let x=VW-w;
      ctx.beginPath(); ctx.arc(x+6,y-1,5,0,7); ctx.fillStyle='#ef4444'; ctx.fill(); ctx.strokeStyle='#7f1d1d'; ctx.lineWidth=1.2; ctx.stroke(); tx('親水部（水になじむ）',x+15,y+3,11,'#0f172a','left',true); x+=130;
      ctx.strokeStyle='#a16207'; ctx.lineWidth=3.8; ctx.beginPath(); ctx.moveTo(x,y-1); ctx.lineTo(x+18,y-1); ctx.stroke(); ctx.strokeStyle='#facc15'; ctx.lineWidth=2.2; ctx.beginPath(); ctx.moveTo(x,y-1); ctx.lineTo(x+18,y-1); ctx.stroke(); tx('疎水部（水をきらう）'+s2,x+23,y+3,11,'#0f172a','left',true); }
    if(hide) pill('分子はどう並ぶ？ 予想してから「👀 答えを見る」を押そう',VW/2,VH/2-60,14,'#0f172a','rgba(254,243,199,.96)');
    if(paused) pill('一時停止中',VW/2,60,13,'#0f172a','rgba(255,255,255,.95)');
    if(note&&t<noteT) pill(note,VW/2,96,13,'#fff','rgba(185,28,28,.92)');
    ctx.restore(); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1; rr(.5,.5,VW-1,VH-1,10); ctx.stroke();
    rr(0,VH+6,W,H-VH-6,10); ctx.fillStyle='#fff'; ctx.fill(); ctx.strokeStyle='#e2e8f0'; ctx.stroke();
    wrap(caption(),W-28,12.5).slice(0,3).forEach((l,i)=>tx(l,14,VH+26+i*18,12.5,'#0f172a','left',false));
    const c=count(), nm={surface:'水と空気の境界',oil:'水と油の境界',micelle:'水中のミセル',bubble:'シャボン玉の膜',bilayer:'リン脂質二重層',compare:'膜の比較'}[scene];
    setStat('sD',nm); setStat('sA',c[0]+' 個'); setStat('sB',c[1]+' 個'); setStat('sC',c[2]+' 個');
    setShare('【セッケン・シャボン玉・細胞膜】親水部と疎水部をもつ分子が、'+nm+'でどう並ぶかを見た｜シミュラボ');
  }
  function loop(){ if(!paused){ const sp=+$('spd').value, n=Math.max(1,Math.round(sp*2)); for(let i=0;i<n;i++) step(1/120); } draw(); requestAnimationFrame(loop); }
  $('scene').addEventListener('change',setScene);
  $('n').addEventListener('input',sync);
  $('scat').addEventListener('click',()=>{ hide=false; $('hide').textContent='🙈 分子をかくす（予想する）'; scatter(); });
  $('hide').addEventListener('click',()=>{ hide=!hide; $('hide').textContent=hide?'👀 答えを見る':'🙈 分子をかくす（予想する）'; if(!hide) scatter(); });
  $('pause').addEventListener('click',()=>{ paused=!paused; $('pause').textContent=paused?'▶ 再開':'⏸ 一時停止'; });
  $('names').addEventListener('click',()=>{ names=!names; $('names').textContent=names?'🏷 名前をかくす':'🏷 名前を表示'; });
  $('act').addEventListener('click',()=>{
    if(scene==='oil'){ if(st.stirOn){ st.stirOn=false; st.stir=0; scatter(); } else { let n=0; for(const m of M) if(m.ok&&m.slot) n++; if(n<14){ say('セッケン分子が少ないので、油は表面からはなれません（いま'+n+'個）'); } else st.stirOn=true; } }
    else if(scene==='micelle'){ st.oil=!st.oil; build(); sync(); M.forEach(m=>{ m.rel=t+rnd(.1,1.2); if(inOil(m.x,m.y,10)){ const p=randWater(1); m.x=p[0]; m.y=p[1]; } }); }
    else if(scene==='bubble') st.zoomOn=!st.zoomOn; else if(scene==='bilayer') st.bendOn=!st.bendOn;
    actLabel(); });
  window.__test={step:function(s){ const n=Math.round(s*60); for(let i=0;i<n;i++) step(1/60); draw(); },get s(){ return {scene:scene,n:M.length,slots:slots.length,count:count(),st:JSON.parse(JSON.stringify(st))}; }};
  setScene(); loop();
'''

ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
<p>セッケンやリン脂質の分子は、水になじむ<b>親水部</b>と、水をきらい油になじむ<b>疎水部</b>の両方をもっています。そのため、水・油・空気の境界では、親水部を水の側に、疎水部を水のない側（空気や油）に向けて並びます。このシミュレーターでは、水面、油汚れ、ミセル、シャボン玉の膜、リン脂質二重層の5つの場面と、シャボン玉の膜と細胞膜を並べた比較で、分子の向きと集まり方を見比べることができます。</p>
''' + N('<b>対応する単元</b>：高等学校「生物」（2）生命現象と物質 ア（ｱ）細胞と分子「㋐生体物質と細胞」（生体膜とリン脂質）、「生物基礎」の細胞膜、高等学校「化学」有機化合物（油脂とセッケン：界面活性剤・ミセル・乳化）。') + '''
<h2>授業での使い方</h2>
<h3>導入：身近なセッケンから始める</h3>
<p>「水と空気の境界」で、ばらばらの分子が水面に集まり、親水部を水の中に、疎水部を空気の側に向けて並ぶ様子を見ます。分子の数を増やしていくと、水面がいっぱいになったあと、水中にミセルができ始めます。次に「水と油の境界」で、油汚れの表面に分子が集まるのを確かめてから「🌀 かき混ぜる」を押すと、油が表面からはなれて小さな油滴になり、まわりを分子が取り囲みます。分子の数を10個ほどに減らしてかき混ぜると、油ははなれません。</p>
<h3>展開：シャボン玉の膜から細胞膜を予想する</h3>
<p>「シャボン玉の膜」で断面を拡大し、うすい水の層の両面に分子が並び、疎水部が外側・内側の空気に向いていることを確かめます。そのうえで「細胞の内側にも外側にも水がある。リン脂質はどう並べばよいだろう」と問い、「リン脂質二重層」の場面で「🙈 分子をかくす（予想する）」を押して予想させてから、「👀 答えを見る」で確かめます。</p>
<h3>まとめ：2つの膜を比べる</h3>
<p>「膜の比較」では、シャボン玉の膜とリン脂質二重層を左右に並べます。どちらも分子が2層に並びますが、シャボン玉の膜は中央が水の層、リン脂質二重層は中央に疎水部が集まっています。「リン脂質二重層」の場面で「⭕ 閉じて袋にする」を押すと、平らな膜の端で水にふれていた疎水部（赤い印）が、閉じることでなくなり、内側にも外側にも水がある袋（小胞）になります。</p>
<h3>生徒への問いの例</h3>
<ol>
<li>水面に並んだセッケン分子は、どちらを水の側に向けているだろう？それはなぜだろう？</li>
<li>シャボン玉の膜とリン脂質二重層は、どちらも分子が2層に並んでいる。水のある場所と、分子の向きは、それぞれどうなっているだろう？</li>
<li>平らなリン脂質二重層の端では、何が困るのだろう？閉じて袋になると、それはどう解決されるだろう？</li>
</ol>
<h2>しくみ・解説</h2>
<h3>用語</h3>
<ul>
<li><b>親水部（親水基）</b>とは、水になじみやすい部分です。セッケンでは −COO⁻、リン脂質ではリン酸を含む部分にあたります。</li>
<li><b>疎水部（疎水基）</b>とは、水になじみにくく、油になじみやすい部分です。炭化水素の鎖（脂肪酸の部分）にあたります。</li>
<li><b>界面活性剤</b>とは、親水部と疎水部の両方をもち、水と油・水と空気の境界（界面）に集まる物質です。セッケンや合成洗剤が代表例です。</li>
<li><b>ミセル</b>とは、界面活性剤の分子が、疎水部を内側に、親水部を外側の水に向けて集まった粒子です。ある濃度をこえるとでき始めます。</li>
<li><b>乳化</b>とは、油が界面活性剤に囲まれて小さな粒になり、水の中に分散することです。</li>
<li><b>リン脂質二重層</b>とは、リン脂質が疎水部を内側に向かい合わせ、親水部を両側の水に向けて2層に並んだ構造で、細胞膜などの生体膜の基本になっています。</li>
</ul>
<h3>場面ごとの分子の向き</h3>
''' + T([["水と空気の境界（水面）", "水の中", "空気の側", "水面に1層"],
          ["水と油の境界（油汚れ・油滴）", "水の側", "油の中", "油の表面に1層"],
          ["水中のミセル", "外側（水）", "内側（疎水部どうし）", "球状に1層"],
          ["シャボン玉の膜", "中央の水の層", "外側・内側の空気", "水の層をはさんで2層"],
          ["リン脂質二重層（細胞膜）", "両側の水", "膜の内部（疎水部どうし）", "疎水部を向かい合わせて2層"]],
         ["場面", "親水部の向き", "疎水部の向き", "並び方"]) + '''
''' + P('どの場面でも決まりは同じです。「親水部は水の側、疎水部は水のない側」。まわりに何があるか（水・油・空気）がちがうので、並び方がちがって見えます。') + '''
<h3>セッケンで油汚れが落ちるしくみ</h3>
<p>セッケン分子は、疎水部を油汚れの中に、親水部を水の側に向けて、油の表面に集まります。こすったりかき混ぜたりすると、油は表面からはなれて小さな油滴になり、まわりをセッケン分子が取り囲みます。油滴の表面は親水部でおおわれているので、水になじみ、油滴どうしがくっつきにくくなって、水といっしょに流されます。</p>
<h3>なぜ細胞膜は二重層で、袋になるのか</h3>
<p>細胞の内側にも外側にも水があります。リン脂質は疎水部の尾を2本もち、ミセルのように小さく丸まるよりも、疎水部を向かい合わせた2層の膜になりやすい形をしています。平らな膜には端があり、そこでは疎水部が水にふれてしまいます。膜が閉じて袋状になると端がなくなるため、閉じた構造ができやすくなります。こうしてできた袋が、細胞や細胞小器官を区切る膜のもとになっています。</p>
<h3>このシミュレーターのモデル</h3>
<p>分子は、はじめばらばらに動き、やがて場面ごとの「並ぶ場所」に引き寄せられるように動かしています。分子どうしや水との力を計算したものではなく、並び方を見やすく示すための模式的な表現です。分子の大きさ・数、水の層や膜の厚さの比は実際とはちがいます（実際のシャボン玉の膜の水の層は、分子の長さよりずっと厚いことがふつうです）。分子が力のはたらきで集まっていく過程を見たいときは、「リン脂質と細胞膜のでき方シミュレーター」を使ってください。</p>
<h2>参考</h2>
<ul>
<li>''' + A(MEXT_KOU, "文部科学省 高等学校学習指導要領（平成30年告示）解説 理科編") + '''（生物（2）生命現象と物質、化学 有機化合物）</li>
<li>高等学校「生物」「生物基礎」「化学」の教科書（生体膜とリン脂質、セッケンと界面活性剤）</li>
</ul>
'''

sim(slug="sekken-shabondama", cat="rika", emoji="🫧", score=79,
    title="セッケン・シャボン玉・細胞膜のシミュレーター（親水部と疎水部をもつ分子の並び方）",
    title_tag="界面活性剤とリン脂質の並び方シミュレーター｜セッケン・ミセル・シャボン玉の膜・リン脂質二重層（高校生物・化学）",
    meta_desc="親水部と疎水部をもつ分子が、水面、油汚れ、水中のミセル、シャボン玉の膜、リン脂質二重層でどう並ぶかを見比べるシミュレーター。かき混ぜると油汚れが油滴になって落ちる様子、シャボン玉の膜の断面、平らな二重層が閉じて袋（小胞）になる様子をアニメーションで観察できます。",
    og_title="セッケン・シャボン玉・細胞膜のシミュレーター（親水部と疎水部をもつ分子の並び方）",
    og_desc="水面では疎水部を空気へ、油汚れでは油の中へ。シャボン玉の膜は中央が水、細胞膜は中央が疎水部。決まりは1つ「親水部は水の側、疎水部は水のない側」。6つの場面で分子の向きを見比べる。",
    card_desc="水面・油汚れ・ミセル・シャボン玉の膜・リン脂質二重層で、親水部と疎水部をもつ分子の向きと並び方を比べる。",
    lead="赤い丸が水になじむ親水部、黄色の線が水をきらう疎水部です。場面を切り替えると、ばらばらの分子が水・油・空気の境界に集まり、決まった向きに並びます。油汚れをかき混ぜて落とす、シャボン玉の膜の断面を拡大する、リン脂質二重層を閉じて袋にする、といった操作をしながら、分子の向きの決まりを見つけてみましょう。",
    model="生物 細胞と分子（生体膜とリン脂質）／化学 油脂とセッケン（界面活性剤）",
    level="高校（生物・生物基礎・化学）",
    unit="高等学校 生物（2）生命現象と物質 ア（ｱ）細胞と分子 ㋐生体物質と細胞",
    canvas=canvas(640, 500, light=True),
    controls=select("scene", "場面", [("surface", "① 水と空気の境界（水面）"), ("oil", "② 水と油の境界（油汚れを落とす）"), ("micelle", "③ 水中のミセル"),
                                     ("bubble", "④ シャボン玉の膜"), ("bilayer", "⑤ リン脂質二重層と袋状の膜"), ("compare", "⑥ 比べる：シャボン玉の膜と細胞膜")])
             + slider("n", "分子の数", 0, 100, 70, 2, "{v} 個")
             + select("spd", "速さ", [("1", "×1"), ("2", "×2"), ("0.5", "×0.5（ゆっくり）")]),
    buttons=btn("act", "操作", True) + btn("scat", "↺ ばらばらから並ぶ") + btn("hide", "🙈 分子をかくす（予想する）") + btn("pause", "⏸ 一時停止") + btn("names", "🏷 名前をかくす"),
    stats=stats([("sD", "場面", False), ("sA", "境界・膜に並んだ分子", True), ("sB", "ミセル・油滴を囲む分子", True), ("sC", "ばらばらの分子", False)]),
    legend=PH + "赤い丸＝親水部、黄色の線＝疎水部（尾が1本＝セッケン、2本＝リン脂質）。青＝水、うすい黄色＝空気、オレンジ＝油。分子の並び方を見やすく示す模式的な表現で、大きさや数の比は実際とはちがいます。",
    article=ARTICLE,
    faqs=[("セッケンで油汚れが落ちるのはなぜ？", "セッケン分子は、油になじむ疎水部を油汚れの中に、水になじむ親水部を水の側に向けて、油の表面に集まります。こすると油は表面からはなれて小さな油滴になり、まわりをセッケン分子が取り囲みます。表面が親水部でおおわれた油滴は水になじむので、水といっしょに流されます。これを乳化といいます。"),
          ("ミセルとは何？", "界面活性剤（セッケンなど）の分子が、疎水部を内側に、親水部を外側の水に向けて集まった粒子です。濃度が低いうちは分子がばらばらに溶け、水面に並びますが、ある濃度をこえると水中でミセルをつくり始めます。"),
          ("シャボン玉の膜はどんなつくり？", "うすい水の層を、内側と外側からセッケン分子の層がはさんだつくりです。セッケン分子は親水部を水の層に、疎水部をそれぞれ外側・内側の空気に向けて並んでいます。"),
          ("シャボン玉の膜と細胞膜はどこがちがうの？", "どちらも分子が2層に並びますが、向きが逆です。シャボン玉の膜は中央に水の層があり、疎水部が外側の空気に向いています。細胞膜のリン脂質二重層は、両側が水なので、親水部が両側の水に向き、疎水部が膜の中央で向かい合っています。"),
          ("なぜリン脂質は二重層になるの？", "細胞の内側にも外側にも水があるため、疎水部が水にふれないようにするには、疎水部どうしを向かい合わせて2層になる必要があるからです。リン脂質は疎水部の尾を2本もつので、小さな球（ミセル）よりも、平らな膜の形になりやすい分子です。"),
          ("二重層はなぜ袋状に閉じるの？", "平らな膜には端があり、そこでは疎水部が水にふれてしまいます。膜が閉じて袋状になると端がなくなり、疎水部が水にふれずにすむため、閉じた構造ができやすくなります。細胞膜も切れ目のない袋になっています。")],
    rel=[("rinshishitsu-maku", "🧼", "リン脂質と細胞膜のでき方シミュレーター"), ("maku-yuso", "🚪", "膜輸送のシミュレーター"),
         ("kouso-shikkatsu", "🌡️", "酵素の失活シミュレーター"), ("virus-sekken-alcohol", "🧴", "ウイルスと洗剤・アルコールのシミュレーター"), ("diffusion", "🫧", "拡散シミュレーター")],
    js=JS)
