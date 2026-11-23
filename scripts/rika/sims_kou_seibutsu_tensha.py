# -*- coding: utf-8 -*-
"""理科の授業向けシミュ（高校 生物：原核生物の転写と翻訳）— シミュラボのリクエスト（2026-11-23 受付 b227e5c2c6／伊藤さん）から
   tensha-honyaku-genkaku … 原核生物では転写が終わる前に翻訳が始まる（転写と翻訳の同時進行・ポリソーム）
   生物（3）遺伝情報の発現と発生 ア（ｱ）遺伝情報とその発現
   モデル：mRNA は 113 塩基（5′非翻訳領域12＋26コドン＋終止コドン＋3′側20）。塩基配列とアミノ酸は遺伝暗号表どおり（CODONS を __test.check で照合）。"""
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
  const FF='"Hiragino Sans","Hiragino Kaku Gothic ProN","Noto Sans JP","Yu Gothic UI","Yu Gothic",Meiryo,sans-serif', MONO='Consolas,"Courier New",monospace';
  function tx(s,x,y,size,col,align,bold,font){ ctx.font=(bold?'bold ':'')+size+'px '+(font||FF); ctx.fillStyle=col; ctx.textAlign=align||'left'; ctx.fillText(s,x,y); ctx.textAlign='left'; }
  function tw(s,size,bold){ ctx.font=(bold?'bold ':'')+size+'px '+FF; return ctx.measureText(s).width; }
  function rr(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
  function pill(s,x,y,size,col,bg){ const w=tw(s,size,true)+14; rr(x-w/2,y-size-2,w,size+11,7); ctx.fillStyle=bg||'rgba(255,255,255,.9)'; ctx.fill(); tx(s,x,y+2,size,col,'center',true); }
  const sm=v=>{ v=clamp(v,0,1); return v*v*(3-2*v); }, lerp=(a,b,k)=>a+(b-a)*k;

  // ===== 遺伝子（塩基配列は mRNA の向き 5′→3′） =====
  const UTR5='ACAGGAGGUCAC';                                   // リボソーム結合部位 AGGAGG をふくむ
  const CODONS=['AUG','GCU','AAA','GAA','CUG','UUC','GGU','ACC','AGC','GAU','CAU','CCG','GUU','UGG','AAC','CAG','AUC','UAC','CGU','UGC','GAA','AAA','GCU','CUG','ACC','GGU'];
  const AAS=['Met','Ala','Lys','Glu','Leu','Phe','Gly','Thr','Ser','Asp','His','Pro','Val','Trp','Asn','Gln','Ile','Tyr','Arg','Cys','Glu','Lys','Ala','Leu','Thr','Gly'];
  const STOP='UAA', UTR3='GCAUCGAUCCGGAAUCGGCU';
  const SEQ=UTR5+CODONS.join('')+STOP+UTR3, NT=SEQ.length, CDS=UTR5.length, NC=CODONS.length, STOPI=CDS+NC*3;
  const TABLE={AUG:'Met',GCU:'Ala',AAA:'Lys',GAA:'Glu',CUG:'Leu',UUC:'Phe',GGU:'Gly',ACC:'Thr',AGC:'Ser',GAU:'Asp',CAU:'His',CCG:'Pro',GUU:'Val',UGG:'Trp',AAC:'Asn',CAG:'Gln',AUC:'Ile',UAC:'Tyr',CGU:'Arg',UGC:'Cys'};
  const COMP={A:'U',U:'A',G:'C',C:'G'};
  const aaCol=i=>'hsl('+((AAS[i].charCodeAt(0)*47+AAS[i].charCodeAt(1)*31+AAS[i].charCodeAt(2)*13)%360)+',62%,58%)';

  // ===== 状態 =====
  const VT=7, VR=2.2;                                         // 転写 7 塩基/秒、翻訳 2.2 コドン/秒（どちらも1秒に約7塩基ぶん進む）
  let t=0, len=0, ribs=[], prots=[], launched=0, cool=0, termT=-1, playing=true, names=true, done=false;
  function reset(){ t=0; len=0; ribs=[]; prots=[]; launched=0; cool=0; termT=-1; done=false; playing=true; upd(); }
  function upd(){ $('play').textContent=playing?'⏸ 一時停止':'▶ 再生'; }
  const quota=()=>$('mode').value==='one'?1:7;
  function step(dt){ if(done) return; t+=dt;
    if(len<NT){ len=Math.min(NT,len+VT*dt); if(len>=NT) termT=t; }
    cool-=dt;
    // リボソームの結合：リボソーム結合部位と開始コドンが合成され、前のリボソームが先へ進んでいれば結合する
    if(launched<quota()&&cool<=0&&len>=CDS+3+9&&!ribs.some(r=>r.rel<0&&r.c<4.6)){ ribs.push({c:0,born:t,rel:-1,wait:0}); launched++; cool=1.1; }
    for(const r of ribs){ if(r.rel>=0) continue; const born=t-r.born; if(born<.7) continue;      // 結合してから動き出すまで
      if(r.c<NC-1){ const lim=(len-CDS-10)/3; r.c=Math.min(NC-1,Math.min(r.c+VR*dt,Math.max(r.c,lim))); }
      else { r.wait+=dt; if(r.wait>1.0){ r.rel=t; prots.push({t0:t,slot:prots.length}); } } }
    ribs=ribs.filter(r=>r.rel<0||t-r.rel<1.4);
    if(len>=NT&&launched>=quota()&&ribs.length===0&&t-termT>1.5){ done=true; playing=false; upd(); }
  }
  // ===== 上の段：細胞の中のようす =====
  const YD=96, XG=120, PXN=3, ANG=38*Math.PI/180, DX=-Math.cos(ANG), DY=Math.sin(ANG), NXv=Math.sin(ANG), NYv=Math.cos(ANG), SH=368;
  function anchor(){ const rel=termT>=0?sm((t-termT)/1.6):0; return [XG+len*PXN-6+rel*6,YD+22+rel*20]; }
  function mpos(i){ const a=anchor(), d=(len-i)*PXN, w=Math.sin(i*.22+t*2)*1.8; return [a[0]+DX*d+NXv*w,a[1]+DY*d+NYv*w]; }
  function bead(x,y,r,col,txt,fs){ ctx.beginPath(); ctx.arc(x,y,r,0,7); ctx.fillStyle=col; ctx.fill(); ctx.strokeStyle='rgba(15,23,42,.45)'; ctx.lineWidth=1; ctx.stroke(); if(txt) tx(txt,x,y+fs*.36,fs,'#0f172a','center',true); }
  function chainPos(base,k,r){ const d=(k-r)*4.4+9; const w=Math.sin(d*.13+base[0]*.05)*5.5*Math.min(1,d/30); return [base[0]+NXv*d+DX*w,base[1]+NYv*d+DY*w]; }
  function dScene(){
    const g=ctx.createLinearGradient(0,40,0,SH); g.addColorStop(0,'#f0fdf4'); g.addColorStop(1,'#ecfeff'); ctx.fillStyle=g; ctx.fillRect(0,40,W,SH-40);
    // DNA（上＝非鋳型鎖 5′→3′、下＝鋳型鎖 3′→5′）
    ctx.strokeStyle='#1e3a8a'; ctx.lineWidth=4; ctx.beginPath(); ctx.moveTo(26,YD-6); ctx.lineTo(W-26,YD-6); ctx.stroke(); ctx.strokeStyle='#3b82f6'; ctx.beginPath(); ctx.moveTo(26,YD+6); ctx.lineTo(W-26,YD+6); ctx.stroke();
    ctx.strokeStyle='rgba(100,116,139,.5)'; ctx.lineWidth=1; ctx.beginPath(); for(let x=30;x<W-26;x+=6){ ctx.moveTo(x,YD-4); ctx.lineTo(x,YD+4); } ctx.stroke();
    const xe=XG+NT*PXN; ctx.fillStyle='rgba(22,163,74,.85)'; ctx.fillRect(XG-26,YD-11,26,22); ctx.fillStyle='rgba(220,38,38,.9)'; ctx.fillRect(xe,YD-11,6,22);
    if(names){ tx("5′",14,YD-2,10,'#1e3a8a','center',true); tx("3′",W-14,YD-2,10,'#1e3a8a','center',true); tx("3′",14,YD+10,10,'#2563eb','center',true); tx("5′",W-14,YD+10,10,'#2563eb','center',true);
      tx('DNA',40,YD-18,11.5,'#1e3a8a','left',true); tx('プロモーター',XG-13,YD-18,10,'#15803d','center',true); tx('転写終結部位',xe+3,YD-18,10,'#b91c1c','center',true); tx('（転写の終わり）',xe+3,YD-30,9.5,'#b91c1c','center',false);
      tx('鋳型鎖（RNAポリメラーゼが読む鎖）',W-30,YD+24,10,'#2563eb','right',true); }
    // mRNA
    const n=Math.floor(len); if(n>1){ ctx.lineJoin='round'; ctx.lineCap='round';
      const part=(a,b,col,w)=>{ if(b<=a) return; ctx.strokeStyle=col; ctx.lineWidth=w; ctx.beginPath(); for(let i=a;i<=b;i++){ const p=mpos(i); i===a?ctx.moveTo(p[0],p[1]):ctx.lineTo(p[0],p[1]); } ctx.stroke(); };
      part(0,Math.min(n,NT),'#f97316',4); part(2,Math.min(n,8),'#a855f7',6); part(CDS,Math.min(n,CDS+3),'#16a34a',7); if(n>STOPI) part(STOPI,Math.min(n,STOPI+3),'#dc2626',7);
      const p5=mpos(0); if(names){ tx("5′",p5[0]-9,p5[1]+12,11,'#c2410c','center',true); if(n>30){ const pm=mpos(Math.floor(n*.35)); tx('mRNA',pm[0]-16,pm[1]-10,11.5,'#c2410c','right',true); }
        if(n>CDS+3&&!ribs.length&&launched===0){ const q=mpos(CDS+1); tx('開始コドン',q[0]-10,q[1]-4,10,'#15803d','right',true); }
        if(n>STOPI+3){ const q=mpos(STOPI+1); tx('終止コドン（翻訳の終わり）',q[0]+16,q[1]+16,10,'#b91c1c','left',true); }
        if(termT<0){ const a=anchor(); tx("3′",a[0]-16,a[1]+2,10.5,'#c2410c','center',true); } else { const a=mpos(NT); tx("3′",a[0]+10,a[1]+4,10.5,'#c2410c','center',true); } } }
    // RNAポリメラーゼ
    { const rel=termT>=0?sm((t-termT)/1.6):0, x=XG+len*PXN+rel*26, y=YD-rel*34; ctx.globalAlpha=1-rel*.75; ctx.beginPath(); ctx.ellipse(x,y,25,19,0,0,7); ctx.fillStyle='rgba(99,102,241,.82)'; ctx.fill(); ctx.strokeStyle='#3730a3'; ctx.lineWidth=1.6; ctx.stroke(); ctx.globalAlpha=1;
      if(names&&rel<.5){ tx('RNAポリメラーゼ',x,YD-44,10.5,'#3730a3','center',true); if(termT<0){ ctx.strokeStyle='#3730a3'; ctx.lineWidth=1.6; ctx.beginPath(); ctx.moveTo(x+32,YD-28); ctx.lineTo(x+58,YD-28); ctx.stroke(); ctx.fillStyle='#3730a3'; ctx.beginPath(); ctx.moveTo(x+64,YD-28); ctx.lineTo(x+56,YD-32); ctx.lineTo(x+56,YD-24); ctx.closePath(); ctx.fill(); } } }
    // リボソームとポリペプチド鎖
    ribs.forEach((r,ri)=>{ const base=mpos(CDS+r.c*3+1.5), rel=r.rel>=0?sm((t-r.rel)/1.2):0, ap=sm((t-r.born)/.7), k=Math.min(NC,Math.floor(r.c)+1);
      if(r.rel<0){ for(let j=0;j<k;j++){ const p=chainPos(base,k,j); bead(p[0],p[1],3.4,aaCol(j)); } }
      ctx.globalAlpha=(1-rel)*ap; ctx.beginPath(); ctx.ellipse(base[0]+NXv*(4+rel*16)+ (1-ap)*20,base[1]+NYv*(4+rel*16)+(1-ap)*-14,13,10.5,ANG*-1+.2,0,7); ctx.fillStyle='#d6a56c'; ctx.fill(); ctx.strokeStyle='#92400e'; ctx.lineWidth=1.3; ctx.stroke();
      ctx.beginPath(); ctx.ellipse(base[0]-NXv*(6+rel*14),base[1]-NYv*(6+rel*14),10,6.5,-ANG+.2,0,7); ctx.fillStyle='#b8864b'; ctx.fill(); ctx.stroke(); ctx.globalAlpha=1; });
    // できたタンパク質
    prots.forEach(p=>{ const k=sm((t-p.t0)/1.6), tx0=W-74+(p.slot%2)*42, ty0=178+Math.floor(p.slot/2)*44, sx=lerp(mpos(STOPI)[0]+60,tx0,k), sy=lerp(mpos(STOPI)[1]+50,ty0,k);
      for(let j=0;j<NC;j++){ const a=j*.9, rad=3+j*.36; const fx=sx+Math.cos(a)*rad, fy=sy+Math.sin(a)*rad; bead(fx,fy,3.2,aaCol(j)); } });
    if(names&&prots.length) tx('完成したポリペプチド鎖',W-12,156,10,'#0f172a','right',true);
    if(names){ const lead=ribs.find(r=>r.rel<0); if(lead){ const b=mpos(CDS+lead.c*3+1.5); tx('リボソーム',b[0]-22,b[1]-14,10.5,'#92400e','right',true); if(lead.c>5){ const q=chainPos(b,Math.floor(lead.c)+1,0); tx('ポリペプチド鎖',q[0]+8,q[1]+6,10.5,'#0f172a','left',true); } }
      pill('原核生物（細菌）の細胞の中：核膜がなく、DNAのすぐそばで翻訳が起こる',W/2,SH-10,10.5,'#0f172a','rgba(255,255,255,.88)'); }
  }
  // ===== 下の段：先頭のリボソームの拡大 =====
  function tRNA(x,y,ci,al,withAA){ ctx.globalAlpha=al; rr(x-14,y-30,28,34,6); ctx.fillStyle='#99f6e4'; ctx.fill(); ctx.strokeStyle='#0f766e'; ctx.lineWidth=1.3; ctx.stroke();
    const ac=CODONS[ci].split('').map(c=>COMP[c]); ac.forEach((c,i)=>tx(c,x-10.7+i*10.7,y,11,'#115e59','center',true,MONO)); if(withAA) bead(x,y-40,10,aaCol(ci),AAS[ci],8); ctx.globalAlpha=1; }
  function dZoom(){ const y0=SH+8, h=H-y0-4; rr(4,y0,W-8,h,10); ctx.fillStyle='#fff'; ctx.fill(); ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; ctx.stroke();
    tx('🔍 先頭のリボソームを拡大',14,y0+18,11.5,'#0f172a','left',true);
    const lead=ribs.find(r=>r.rel<0); const my=y0+h-52, CW=32, xP=250;
    if(!lead){ tx(launched===0?'リボソーム結合部位と開始コドンが合成されると、リボソームが結合します':done?'すべてのリボソームが翻訳を終えました':'（いまmRNAにリボソームはありません）',W/2,y0+h/2+4,12,'#64748b','center',true); return; }
    const k=Math.floor(lead.c+1e-6), f=lead.c-k, started=t-lead.born>=.7, last=k>=NC-1;
    const shift=last?0:sm((f-.6)/.4), X=i=>xP-CW/2+(i-(CDS+3*(k+shift)))*CW/3+CW/6;
    ctx.save(); rr(6,y0+2,W-12,h-4,9); ctx.clip();
    // リボソーム
    ctx.beginPath(); ctx.ellipse(xP+CW/2,my-58,104,62,0,0,7); ctx.fillStyle='rgba(214,165,108,.33)'; ctx.fill(); ctx.strokeStyle='rgba(146,64,14,.5)'; ctx.lineWidth=1.4; ctx.stroke();
    ctx.beginPath(); ctx.ellipse(xP+CW/2,my+10,92,22,0,0,7); ctx.fillStyle='rgba(184,134,75,.38)'; ctx.fill(); ctx.stroke();
    // mRNA（合成が済んだところまで）
    const n=Math.floor(len); for(let i=0;i<Math.min(n,NT);i++){ const x=X(i); if(x<-10||x>W+10) continue; const inC=i>=CDS&&i<STOPI+3, ci=Math.floor((i-CDS)/3);
      let bg=null; if(i>=2&&i<8) bg='#f3e8ff'; if(inC) bg=i>=STOPI?'#fecaca':ci===0?'#bbf7d0':(ci%2?'#ffedd5':'#fed7aa'); if(bg){ ctx.fillStyle=bg; ctx.fillRect(x-CW/6,my-9,CW/3+.5,18); }
      tx(SEQ[i],x,my+4.5,12,'#7c2d12','center',true,MONO); }
    ctx.strokeStyle='#f97316'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(Math.max(8,X(0)-8),my+11); ctx.lineTo(Math.min(W-8,X(Math.min(n,NT)-1)+8),my+11); ctx.stroke();
    if(X(0)>20) tx("5′",X(0)-16,my+5,11,'#c2410c','center',true); if(n<NT&&X(n)<W-60){ tx('← RNAポリメラーゼが合成中',X(n)+6,my+5,10.5,'#3730a3','left',true); } else if(n>=NT&&X(NT-1)<W-30) tx("3′",X(NT-1)+18,my+5,11,'#c2410c','center',true);
    if(names){ if(X(5)>30&&X(5)<W-30) tx('リボソーム結合部位',X(5),my+26,9.5,'#7e22ce','center',true); const xs=X(CDS+1); if(xs>30&&xs<W-30) tx('開始コドン',xs,my+26,9.5,'#15803d','center',true); const xt=X(STOPI+1); if(n>STOPI+2&&xt>30&&xt<W-40) tx('終止コドン',xt,my+26,9.5,'#b91c1c','center',true); }
    // tRNA とポリペプチド鎖
    const yT=my-13, xA=xP+CW, moved=!last&&f>=.5;
    if(started){
      const xPt=xP-shift*CW, xAt=xA-shift*CW;
      if(k>0&&f<.35){ const o=sm(f/.35); tRNA(xP-CW-o*40,yT-o*46,k-1,1-o,false); }              // 役目を終えた tRNA が離れる
      tRNA(xPt,yT,k,1,!moved&&false); if(!last){ const a=sm(f/.4); tRNA(lerp(xA+70,xAt,a),lerp(yT-78,yT,a),k+1,Math.min(1,a*1.6),true); }
      // 鎖：0〜k 番目（f>=.5 で k+1 番目の tRNA 側へ移る）
      const hx=moved?xAt:xPt, hy=yT-40, cnt=k+1; for(let j=0;j<cnt;j++){ const d=cnt-1-j; if(d>10) continue; const px=hx-d*17-Math.sin(d*.5)*4, py=hy-Math.min(d,5)*13-Math.max(0,d-5)*3+(moved?-20:0)+(moved&&d===0?0:0); bead(px,py,10,aaCol(j),AAS[j],8); }
      if(moved){ /* 新しいアミノ酸の下に鎖がつながった */ }
      if(cnt>11) tx('…',hx-11*17-10,hy-78,14,'#64748b','center',true);
      if(last){ pill(lead.wait>0?'終止コドンに到達：ポリペプチド鎖をはなす':'最後のアミノ酸をつないだ',xP+150,y0+40,11,'#fff','rgba(185,28,28,.9)'); }
    } else { const a=sm((t-lead.born)/.7); tRNA(xP,lerp(yT-70,yT,a),0,a,true); pill('開始コドンに、メチオニンを運ぶ tRNA が結合',xP+160,y0+40,11,'#fff','rgba(21,128,61,.92)'); }
    if(names){ tx('アミノ酸 '+(k+1)+' 個め',W-16,y0+18,11,'#0f172a','right',true); tx('リボソームの進む向き →',W-16,y0+h-10,10.5,'#92400e','right',true); tx('コドン',xP,my+40,9.5,'#7c2d12','center',true); tx('tRNA（下の3文字がアンチコドン）',16,y0+h-10,10,'#0f766e','left',true); }
    ctx.restore(); }
  function title(){ const act=ribs.filter(r=>r.rel<0).length;
    if(done) return ['終了：1本のmRNAから、'+prots.length+'個のポリペプチド鎖が合成された','#0f172a'];
    if(termT>=0) return ['⑤ 転写終結：RNAポリメラーゼとmRNAがDNAからはなれた。翻訳は続いている','#b91c1c'];
    if(act>=2) return ['④ 転写と翻訳が同時に進行：1本のmRNAに複数のリボソーム（ポリソーム）','#b45309'];
    if(act===1) return ['② 転写の途中で翻訳が始まった：mRNAの5′側にリボソームが結合','#15803d'];
    return ['① 転写：RNAポリメラーゼが鋳型鎖を読み、mRNAを 5′→3′ の向きに合成','#3730a3']; }
  function draw(){ ctx.clearRect(0,0,W,H); ctx.fillStyle='#f8fafc'; ctx.fillRect(0,0,W,H);
    const tt=title(); rr(0,0,W,34,10); ctx.fillStyle='#fff'; ctx.fill(); ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; ctx.stroke(); tx(tt[0],12,22,12.5,tt[1],'left',true);
    ctx.save(); rr(0,40,W,SH-40,10); ctx.clip(); dScene(); ctx.restore(); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1; rr(.5,40.5,W-1,SH-41,10); ctx.stroke();
    if(!playing&&!done) pill('一時停止中',70,60,12,'#0f172a','rgba(255,255,255,.95)');
    dZoom();
    const act=ribs.filter(r=>r.rel<0), mx=act.length?Math.max(...act.map(r=>Math.floor(r.c)+1)):0;
    setStat('sL',Math.floor(len)+' / '+NT+' 塩基'); setStat('sR',act.length+' 個'); setStat('sC',mx+' 個'); setStat('sP',prots.length+' 個');
    setShare('【原核生物の転写と翻訳】mRNAが'+Math.floor(len)+'塩基まで合成されたとき、リボソームは'+act.length+'個、完成したポリペプチド鎖は'+prots.length+'個｜シミュラボ'); }
  function loop(){ if(playing){ const sp=+$('spd').value, k=Math.max(1,Math.round(sp*2)); for(let i=0;i<k;i++) step(1/120); } draw(); requestAnimationFrame(loop); }
  $('play').addEventListener('click',()=>{ if(done){ reset(); return; } playing=!playing; upd(); });
  $('stepb').addEventListener('click',()=>{ playing=false; upd(); for(let i=0;i<18;i++) step(1/120); });
  $('rst').addEventListener('click',reset); $('mode').addEventListener('change',reset);
  $('names').addEventListener('click',()=>{ names=!names; $('names').textContent=names?'🏷 名前をかくす':'🏷 名前を表示'; });
  window.__test={step:function(s){ const k=Math.round(s*60); for(let i=0;i<k;i++) step(1/60); draw(); },
    check:function(){ const bad=[]; CODONS.forEach((c,i)=>{ if(TABLE[c]!==AAS[i]) bad.push(c+'/'+AAS[i]); }); return {bad:bad,NT:NT,CDS:CDS,NC:NC,STOPI:STOPI,stop:SEQ.substr(STOPI,3),start:SEQ.substr(CDS,3),rbs:SEQ.substr(2,6)}; },
    get s(){ return {t:+t.toFixed(1),len:Math.floor(len),ribs:ribs.map(r=>+r.c.toFixed(1)+(r.rel>=0?'x':'')),prots:prots.length,launched:launched,term:termT>=0,done:done}; }};
  reset(); loop();
'''

ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
<p>遺伝情報は、DNA → mRNA（転写）→ タンパク質（翻訳）の順に伝えられます。大腸菌などの原核生物には核膜がないので、DNAのすぐそばにリボソームがあり、<b>mRNAの合成（転写）が終わる前に、できた部分から翻訳が始まります</b>。このシミュレーターでは、RNAポリメラーゼがmRNAを伸ばしていくそばで、リボソームが次々に結合してポリペプチド鎖を合成していく様子を、続けて見ることができます。</p>
''' + N('<b>対応する単元</b>：高等学校「生物」（3）遺伝情報の発現と発生 ア（ｱ）遺伝情報とその発現（転写・翻訳、原核生物と真核生物のちがい）。「生物基礎」（1）の「遺伝情報とタンパク質の合成」の発展としても使えます。') + '''
<h2>授業での使い方</h2>
<h3>導入：転写を見る</h3>
<p>再生すると、RNAポリメラーゼ（紫）がプロモーターから右へ進み、DNAの鋳型鎖を読みながらmRNA（オレンジ）を合成します。mRNAは3′端（RNAポリメラーゼの側）が伸びていき、先にできた5′端の側がRNAポリメラーゼから出てきます。ここで一時停止して「翻訳はいつ始まるだろう」と問いかけます。</p>
<h3>展開：転写の途中で翻訳が始まる</h3>
<p>mRNAのリボソーム結合部位（紫）と開始コドン（緑）ができると、転写が続いているのに、リボソームが結合して翻訳が始まります。リボソームはmRNAの上を5′→3′の向きに進み、うしろにポリペプチド鎖が伸びていきます。下の段では、先頭のリボソームの中で、コドンに対応するアンチコドンをもつtRNAがアミノ酸を運び、鎖が1つずつ伸びる様子が見えます。mRNAの右端に「RNAポリメラーゼが合成中」と出ている間は、まだ転写が終わっていません。</p>
<h3>まとめ：ポリソームと、2つの「終わり」</h3>
<p>同じmRNAに、リボソームが次々に結合します（ポリソーム）。途中で止めて「どのリボソームがいちばん長いポリペプチド鎖をもっているか」を問うと、先に翻訳を始めたものほど先へ進み、鎖も長いことがわかります。リボソームは終止コドン（mRNA上の赤）でポリペプチド鎖をはなし、RNAポリメラーゼは転写終結部位（DNA上の赤）で転写を終えます。この2つは別のものです。「リボソームの数」を「1個だけ」にすると、1個のリボソームの動きだけを追えます。</p>
<h3>生徒への問いの例</h3>
<ol>
<li>転写が終わっていないのに翻訳を始められるのは、mRNAのどの部分ができていればよいからだろう？</li>
<li>RNAポリメラーゼとリボソームは、それぞれ何を読み取り、どちら向きに進んでいるだろう？</li>
<li>真核生物では、転写と翻訳が同時に進まないのはなぜだろう？細胞のつくりから考えよう。</li>
</ol>
<h2>しくみ・解説</h2>
<h3>用語</h3>
<ul>
<li><b>転写</b>とは、DNAの塩基配列を写し取って、RNAを合成することです。RNAポリメラーゼが、DNAの一方の鎖（鋳型鎖）に相補的なヌクレオチドを 5′→3′ の向きにつないでいきます。</li>
<li><b>翻訳</b>とは、mRNAの塩基配列をもとに、アミノ酸をつないでタンパク質（ポリペプチド鎖）を合成することです。リボソームで行われます。</li>
<li><b>コドン</b>とは、mRNAの連続した3つの塩基で、1つのアミノ酸を指定します。<b>開始コドン</b>（AUG）から翻訳が始まり、<b>終止コドン</b>で終わります。</li>
<li><b>tRNA（転移RNA）</b>とは、コドンに相補的な<b>アンチコドン</b>をもち、対応するアミノ酸をリボソームに運ぶRNAです。</li>
<li><b>ポリソーム</b>とは、1本のmRNAに複数のリボソームが結合したものです。同じmRNAから、同じタンパク質がいくつも合成されます。</li>
<li><b>プロモーター</b>とは、RNAポリメラーゼが結合して転写を始めるDNAの領域です。</li>
</ul>
<h3>だれが、何を読んで、どちらへ進むか</h3>
''' + T([["RNAポリメラーゼ", "DNAの鋳型鎖", "鋳型鎖を 3′→5′ の向きに読む", "mRNA（5′→3′ の向きに伸びる）", "転写終結部位"],
          ["リボソーム", "mRNAのコドン", "mRNAを 5′→3′ の向きに進む", "ポリペプチド鎖", "終止コドン"]],
         ["はたらくもの", "読み取るもの", "進む向き", "合成するもの", "どこで終わるか"]) + '''
<h3>原核生物と真核生物のちがい</h3>
''' + T([["転写の場所", "細胞質基質（核膜がない）", "核の中"],
          ["翻訳の場所", "細胞質基質", "細胞質基質（リボソーム）"],
          ["転写と翻訳の関係", "転写の途中で翻訳が始まる（同時に進む）", "転写が終わり、mRNAが核の外へ出てから翻訳される"],
          ["転写後の加工", "ふつう行われない", "スプライシングなどを受けてmRNAになる"]],
         ["", "原核生物", "真核生物"]) + '''
''' + P('翻訳に必要なのは「mRNAの全部」ではなく、リボソームが結合する部分と開始コドンです。原核生物では核膜がなく、できたばかりのmRNAにすぐリボソームが近づけるので、転写が終わる前に翻訳を始められます。') + '''
<h3>このシミュレーターのモデル</h3>
<p>mRNAは113塩基（翻訳される部分は26コドン）の、1つのタンパク質をコードする短い模式的な遺伝子です。塩基配列とアミノ酸の対応は遺伝暗号表にしたがっています（アミノ酸は Met＝メチオニン、Ala＝アラニン のように3文字の略号で表示）。細菌の開始コドンに対応するのは、正確にはホルミル基のついたメチオニンですが、ここではメチオニンとしています。実際の遺伝子はずっと長く、RNAポリメラーゼは1秒に数十塩基、リボソームは1秒に十数個のアミノ酸をつなぎます。DNAの二重らせんがほどける様子、リボソームの中の細かい構造、tRNAの立体的な形は省略しています。</p>
<h2>参考</h2>
<ul>
<li>''' + A(MEXT_KOU, "文部科学省 高等学校学習指導要領（平成30年告示）解説 理科編") + '''（生物（3）遺伝情報の発現と発生）</li>
<li>高等学校「生物」「生物基礎」の教科書（遺伝情報の発現：転写と翻訳、原核生物と真核生物の遺伝子発現）</li>
</ul>
'''

sim(slug="tensha-honyaku-genkaku", cat="rika", emoji="🧫", score=80,
    title="原核生物の転写と翻訳シミュレーター（転写の途中で翻訳が始まる・ポリソーム）",
    title_tag="原核生物の転写と翻訳シミュレーター｜転写と翻訳の同時進行・ポリソーム・コドンとtRNA（高校生物）",
    meta_desc="原核生物で、RNAポリメラーゼがmRNAを合成している途中に、リボソームが結合して翻訳が始まる様子を観察できるシミュレーター。mRNAの5′端・3′端、転写と翻訳の進む向き、複数のリボソームが並ぶポリソーム、コドンとtRNAによるポリペプチド鎖の伸長、終止コドンと転写終結部位のちがいを確かめられます。",
    og_title="原核生物の転写と翻訳シミュレーター（転写の途中で翻訳が始まる・ポリソーム）",
    og_desc="mRNAがまだ伸びている途中なのに、もうリボソームがついて翻訳している。核膜のない原核生物ならではの、転写と翻訳の同時進行。先頭のリボソームの中では、コドンとtRNAがアミノ酸を1つずつつないでいく。",
    card_desc="RNAポリメラーゼがmRNAを伸ばすそばで、リボソームが次々に結合して翻訳する、原核生物の遺伝子発現を見る。",
    lead="上の横線がDNA、紫の丸がRNAポリメラーゼ、オレンジの線がmRNAです。再生すると、mRNAが伸びていく途中で、できた部分にリボソーム（茶色）が結合し、ポリペプチド鎖が伸びはじめます。下の段では、先頭のリボソームの中で、コドンに合うtRNAがアミノ酸を運んでくる様子を拡大して見られます。途中で止めて、次に何が起こるかを予想してみましょう。",
    model="生物 遺伝情報の発現（原核生物の転写と翻訳・ポリソーム）",
    level="高校（生物）、生物基礎の発展",
    unit="高等学校 生物（3）遺伝情報の発現と発生 ア（ｱ）遺伝情報とその発現",
    canvas=canvas(640, 590, light=True),
    controls=select("mode", "リボソームの数", [("many", "複数（ポリソーム）"), ("one", "1個だけ")])
             + select("spd", "速さ", [("1", "×1"), ("0.5", "×0.5（ゆっくり）"), ("0.25", "×0.25（とてもゆっくり）"), ("2", "×2")]),
    buttons=btn("play", "⏸ 一時停止", True) + btn("stepb", "⏭ コマ送り") + btn("rst", "↺ はじめから") + btn("names", "🏷 名前をかくす"),
    stats=stats([("sL", "合成されたmRNAの長さ", True), ("sR", "mRNA上のリボソーム", True), ("sC", "いちばん長い鎖のアミノ酸", False), ("sP", "完成したポリペプチド鎖", False)]),
    legend=PH + "紺・青＝DNA（下の青が鋳型鎖）、緑の四角＝プロモーター、DNA上の赤＝転写終結部位、紫の丸＝RNAポリメラーゼ、オレンジの線＝mRNA（紫＝リボソーム結合部位、緑＝開始コドン、赤＝終止コドン）、茶色＝リボソーム、色のついた小さな丸＝アミノ酸。下の段の青緑＝tRNA。アミノ酸は3文字の略号（Met＝メチオニン など）です。",
    article=ARTICLE,
    faqs=[("原核生物では、なぜ転写の途中で翻訳が始まるの？", "原核生物には核膜がなく、DNAとリボソームが同じ細胞質基質にあるからです。mRNAのうち、リボソームが結合する部分と開始コドンが合成されれば、残りの部分がまだ合成中でも、リボソームが結合して翻訳を始められます。"),
          ("真核生物ではどうなるの？", "真核生物では、転写は核の中で行われ、できたRNAはスプライシングなどの加工を受けてmRNAになり、核膜孔を通って細胞質へ出てから翻訳されます。転写と翻訳の場所が核膜で隔てられているので、同時には進みません。"),
          ("ポリソームとは？", "1本のmRNAに複数のリボソームが結合したものです。それぞれのリボソームが同じmRNAを5′側から順に読み、同じアミノ酸配列のポリペプチド鎖を合成します。先に翻訳を始めたリボソームほど3′側へ進んでいて、ポリペプチド鎖も長くなっています。"),
          ("mRNAはどちら向きに合成されるの？", "5′→3′ の向きです。RNAポリメラーゼは、DNAの鋳型鎖を3′→5′の向きに読みながら、相補的なヌクレオチドをRNAの3′端につないでいきます。そのため、先に合成された5′端の側からリボソームが結合できます。"),
          ("終止コドンと転写終結部位はどうちがうの？", "終止コドンはmRNA上の3つの塩基で、リボソームがここに来ると翻訳が終わり、ポリペプチド鎖がはなれます。転写終結部位はDNA上の領域で、RNAポリメラーゼがここで転写を終え、mRNAをはなします。翻訳の終わりと転写の終わりは別の場所で決まっています。"),
          ("コドンとアンチコドンの関係は？", "mRNAのコドン（3つの塩基）に対して、相補的な3つの塩基（アンチコドン）をもつtRNAが結合します。tRNAはアンチコドンに対応した決まったアミノ酸を運んでくるので、コドンの並び順どおりにアミノ酸がつながります。たとえばコドン AUG には、アンチコドン UAC をもつtRNAがメチオニンを運んできます。")],
    rel=[("pcr-hou", "🧬", "PCR法のシミュレーター"), ("dna", "🧬", "DNA二重らせん"),
         ("kouso-shikkatsu", "🌡️", "酵素の失活シミュレーター"), ("saibou-bunretsu", "🔬", "細胞分裂シミュレーター"), ("maku-yuso", "🚪", "膜輸送のシミュレーター")],
    js=JS)
