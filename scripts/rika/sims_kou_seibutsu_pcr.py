# -*- coding: utf-8 -*-
"""理科の授業向けシミュ（高校 生物：PCR法）— シミュラボのリクエスト（2026-11-23 受付 2fd0dd528e／伊藤さん）から
   pcr-hou … 熱変性・アニーリング・伸長の3段階と、サイクルごとに目的の長さのDNAが増えるしくみ
   生物（3）遺伝情報の発現と発生 ア（ｳ）遺伝子を扱う技術（バイオテクノロジー）
   モデル：鎖を「位置 0〜40 の区間」として正確に追う。上の鎖（T）は左が5′、下の鎖（B）は右が5′。
     プライマーF は位置12から右へ、プライマーR は位置28から左へ伸びる（どちらも 5′→3′）。
     n サイクル後：二本鎖は 2^n 本、うち両方の鎖が目的の長さのものは 2^n − 2n 本。"""
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
  const sm=v=>{ v=clamp(v,0,1); return v*v*(3-2*v); }, lerp=(a,b,k)=>a+(b-a)*k;

  // ===== 鎖のモデル =====
  const L=40, TA=12, TB=28, PL=4;          // 鋳型の長さ・増やしたい領域 [TA,TB]・プライマーの長さ
  const C_ORIG='#1e3a8a', C_NEW='#f59e0b', C_F='#16a34a', C_R='#c026d3';
  let dups, n=0, ph='idle', u=0, playing=false, names=true, t=0;
  function reset(){ dups=[{T:{s:0,e:L,nw:false},B:{s:0,e:L,nw:false}}]; n=0; ph='idle'; u=0; playing=false; upd(); }
  // 1サイクル：上の鎖（T）を鋳型にすると、Rから左へ伸びて下の鎖 [T.s, TB] ができる。下の鎖（B）を鋳型にすると、Fから右へ伸びて上の鎖 [TA, B.e] ができる。
  function nextDups(d){ const o=[]; for(const x of d){ o.push({T:x.T,B:{s:x.T.s,e:TB,nw:true}}); o.push({T:{s:TA,e:x.B.e,nw:true},B:x.B}); } return o; }
  const total=k=>Math.pow(2,k), target=k=>k<3?0:Math.pow(2,k)-2*k;
  const isTarget=d=>d.T.s===TA&&d.T.e===TB&&d.B.s===TA&&d.B.e===TB;
  const detail=()=>n<3||(n===3&&ph==='idle');
  const TEMP={idle:72,den:95,ann:55,ext:72};
  function dur(){ const d=n<3?[2.6,2.8,4.4]:[.8,.8,1.2]; return ph==='den'?d[0]:ph==='ann'?d[1]:d[2]; }
  function advance(){ if(ph==='idle'){ if(n>=+$('cyc').value){ playing=false; upd(); return false; } ph='den'; u=0; }
    else if(ph==='den'){ ph='ann'; u=0; } else if(ph==='ann'){ ph='ext'; u=0; }
    else { if(n<10) dups=nextDups(dups); n++; ph='idle'; u=0; if(n>=+$('cyc').value) playing=false; }
    upd(); return true; }
  function step(dt){ t+=dt; if(!playing) return; if(ph==='idle'){ u+=dt/(n<3?1.2:.35); if(u>=1) advance(); return; } u+=dt/dur(); if(u>=1){ u=1; advance(); } }
  function upd(){ $('play').textContent=playing?'⏸ 一時停止':'▶ 再生'; }

  // ===== 分子の表示（3サイクル目まで） =====
  const X0=58, SX=(W-116)/L, MY=50, MH=330, X=c=>X0+c*SX;
  function seg(x1,x2,y,col,w){ ctx.strokeStyle=col; ctx.lineWidth=w; ctx.lineCap='butt'; ctx.beginPath(); ctx.moveTo(x1,y); ctx.lineTo(x2,y); ctx.stroke(); }
  function arrow(x,y,dir,col,sz){ ctx.fillStyle=col; ctx.beginPath(); ctx.moveTo(x+dir*sz*1.5,y); ctx.lineTo(x-dir*1,y-sz); ctx.lineTo(x-dir*1,y+sz); ctx.closePath(); ctx.fill(); }
  // 鎖を描く。type 'T'：左が5′・右が3′（矢印は右端）／'B'：右が5′・左が3′（矢印は左端）。grow=新しい鎖がどこまで伸びたか（0〜1）
  function strand(S,type,y,w,grow,primerOnly,small){ let s=S.s, e=S.e; const g=grow==null?1:grow;
    if(S.nw){ const ps=type==='T'?TA:TB-PL, pe=type==='T'?TA+PL:TB; if(!primerOnly){ if(type==='T'){ const end=lerp(pe,e,g); if(end>pe) seg(X(pe),X(end),y,C_NEW,w); e=end; } else { const end=lerp(ps,s,g); if(end<ps) seg(X(end),X(ps),y,C_NEW,w); s=end; } }
      seg(X(ps),X(pe),y,type==='T'?C_F:C_R,w); if(primerOnly){ s=ps; e=pe; } }
    else seg(X(s),X(e),y,C_ORIG,w);
    const col=S.nw?(type==='T'?C_F:C_R):C_ORIG, ecol=S.nw&&!primerOnly?C_NEW:col;
    if(type==='T') arrow(X(e),y,1,primerOnly?col:ecol,w*.95); else arrow(X(s),y,-1,primerOnly?col:ecol,w*.95);
    if(names&&!small&&!primerOnly){ const fs=9.5; if(type==='T'){ tx("5′",X(s)-4,y+3.5,fs,'#475569','right',true); tx("3′",X(e)+w*1.6+3,y+3.5,fs,'#475569','left',true); } else { tx("3′",X(s)-w*1.6-3,y+3.5,fs,'#475569','right',true); tx("5′",X(e)+4,y+3.5,fs,'#475569','left',true); } }
    return [s,e]; }
  function ticks(s,e,y1,y2,al){ if(al<=.01||e<=s) return; ctx.strokeStyle='rgba(100,116,139,'+(.55*al)+')'; ctx.lineWidth=1.2; ctx.beginPath(); for(let c=Math.ceil(s+.01)-.5;c<e;c+=1){ if(c<s) continue; ctx.moveTo(X(c),y1); ctx.lineTo(X(c),y2); } ctx.stroke(); }
  function pol(x,y){ ctx.beginPath(); ctx.ellipse(x,y,10,8,0,0,7); ctx.fillStyle='rgba(13,148,136,.9)'; ctx.fill(); ctx.strokeStyle='#115e59'; ctx.lineWidth=1.3; ctx.stroke(); }
  function slotY(j,N){ const hs=(MH-46)/N; return [MY+18+(j+.5)*hs, Math.min(8,hs*.2), hs]; }
  function dDetail(){
    // 増やしたい領域
    ctx.fillStyle='rgba(254,240,138,.55)'; ctx.fillRect(X(TA),MY-4,X(TB)-X(TA),MH+8); ctx.strokeStyle='#eab308'; ctx.lineWidth=1; ctx.setLineDash([4,3]); ctx.strokeRect(X(TA),MY-4,X(TB)-X(TA),MH+8); ctx.setLineDash([]);
    if(names) tx('増やしたい領域',(X(TA)+X(TB))/2,MY+8,10.5,'#a16207','center',true);
    const N=dups.length, small=N>=4, w=N>=4?4.2:5.5;
    if(ph==='idle'){ dups.forEach((d,i)=>{ const [y,dd]=slotY(i,N); if(isTarget(d)){ rr(X(TA)-26,y-dd-9,X(TB)-X(TA)+52,dd*2+18,8); ctx.fillStyle='rgba(187,247,208,.8)'; ctx.fill(); ctx.strokeStyle='#16a34a'; ctx.lineWidth=1.4; ctx.stroke(); }
        ticks(Math.max(d.T.s,d.B.s),Math.min(d.T.e,d.B.e),y-dd+w/2,y+dd-w/2,1); strand(d.T,'T',y-dd,w,1,false,small); strand(d.B,'B',y+dd,w,1,false,small);
        if(isTarget(d)&&names) tx('目的の長さの二本鎖',X(TB)+34,y+4,10.5,'#15803d','left',true); });
      if(n===0&&names){ const [y,dd]=slotY(0,1); tx('もとの二本鎖DNA（鋳型）',X(5),y-dd-30,12,C_ORIG,'left',true);
        [[TB-PL,TB,-1,'プライマーRが結合する場所',C_R],[TA,TA+PL,1,'プライマーFが結合する場所',C_F]].forEach(o=>{ const yy=y+o[2]*(dd+16); ctx.strokeStyle=o[4]; ctx.lineWidth=1.6; ctx.setLineDash([3,2]); ctx.strokeRect(X(o[0]),Math.min(yy,y+o[2]*dd)-3,X(o[1])-X(o[0]),Math.abs(yy-y-o[2]*dd)+6); ctx.setLineDash([]); tx(o[3],(X(o[0])+X(o[1]))/2,yy+o[2]*16+4,10.5,o[4],'center',true); }); }
      return; }
    const N2=N*2, k=ph==='den'?sm(u):1, sm2=N2>=8;
    dups.forEach((d,i)=>{ const [y0,d0]=slotY(i,N), [ya,da]=slotY(2*i,N2), [yb,db]=slotY(2*i+1,N2);
      const yT=lerp(y0-d0,ya-da,k), yB=lerp(y0+d0,yb+db,k);
      if(ph==='den') ticks(Math.max(d.T.s,d.B.s),Math.min(d.T.e,d.B.e),y0-d0+w/2,y0+d0-w/2,1-sm(u*2.2));
      strand(d.T,'T',yT,w,1,false,sm2); strand(d.B,'B',yB,w,1,false,sm2);
      if(ph==='den') return;
      // 新しい鎖：スロット 2i では T を鋳型に下の鎖、スロット 2i+1 では B を鋳型に上の鎖
      const nB={s:d.T.s,e:TB,nw:true}, nT={s:TA,e:d.B.e,nw:true}, yNB=ya+da, yNT=yb-db;
      if(ph==='ann'){ const a=sm(u/.75), wob=Math.sin(t*9+i)*3*(1-a);
        ctx.save(); ctx.translate(lerp(60,0,a)+wob,lerp(34,0,a)); strand(nB,'B',yNB,w,0,true,true); ctx.restore(); ctx.save(); ctx.translate(lerp(-60,0,a)-wob,lerp(-34,0,a)); strand(nT,'T',yNT,w,0,true,true); ctx.restore();
        if(u>.75){ ticks(TB-PL,TB,ya-da+w/2,yNB-w/2,sm((u-.75)/.25)); ticks(TA,TA+PL,yNT+w/2,yb+db-w/2,sm((u-.75)/.25)); } }
      else { const g=sm(u); const r1=strand(nB,'B',yNB,w,g,false,sm2), r2=strand(nT,'T',yNT,w,g,false,sm2);
        ticks(r1[0],TB,ya-da+w/2,yNB-w/2,1); ticks(TA,r2[1],yNT+w/2,yb+db-w/2,1);
        if(u<.98){ pol(X(r1[0])-6,yNB-1); pol(X(r2[1])+6,yNT+1); } }
    });
    if(names&&ph==='ext'&&dups.length<=2){ const [ya,da]=slotY(0,dups.length*2); tx('← 新しい鎖は 5′→3′ の向きに伸びる',X(TB-PL)-14,ya+da+22,10.5,'#b45309','right',true); }
  }
  // ===== 全体の表示（4サイクル目から） =====
  function dOverall(){ const tot=total(n), cnt=[1,1,Math.max(0,n-1),Math.max(0,n-1),target(n)], reps=[[[0,L],[0,TB]],[[TA,L],[0,L]],[[TA,L],[TA,TB]],[[TA,TB],[0,TB]],[[TA,TB],[TA,TB]]];
    const cw=41, chh=15, cols=Math.floor((W-24)/cw), rows=Math.floor((MH-22)/chh), cap=cols*rows; const show=Math.min(tot,cap);
    const list=[]; if(tot<=cap){ cnt.forEach((c,k)=>{ for(let i=0;i<c;i++) list.push(k); }); } else { const kl=Math.round(cap*2*n/tot); for(let i=0;i<kl;i++) list.push(i<2?i:(i%2?3:2)); while(list.length<cap) list.push(4); }
    const sep=ph==='den'?sm(u)*2.4:(ph==='ann'||ph==='ext')?2.4:0, g=ph==='ext'?sm(u):0;
    list.forEach((k,i)=>{ const cx=12+(i%cols)*cw, cy=MY+8+Math.floor(i/cols)*chh, ww=cw-7, x=c=>cx+c/L*ww, r=reps[k], tgt=k===4;
      if(tgt&&ph==='idle'){ ctx.fillStyle='rgba(187,247,208,.9)'; ctx.fillRect(x(TA)-2,cy-1,x(TB)-x(TA)+4,11); }
      const cT=(k===0)?C_ORIG:C_NEW, cB=(k===1)?C_ORIG:C_NEW;
      seg(x(r[0][0]),x(r[0][1]),cy+2-sep,cT,2.6); seg(x(r[1][0]),x(r[1][1]),cy+7+sep,cB,2.6);
      if(g>0){ seg(x(lerp(TB,r[0][0],g)),x(TB),cy+4.2-sep*.2,C_NEW,1.6); seg(x(TA),x(lerp(TA,r[1][1],g)),cy+4.8+sep*.2,C_NEW,1.6); } });
    if(tot>cap) pill('全部で '+num(tot)+' 本のうち '+cap+' 本を表示（ほとんどが目的の長さ）',W/2,MY+MH-6,11.5,'#0f172a','rgba(255,255,255,.95)');
  }
  // ===== 温度のグラフと本数のグラフ =====
  function tempAt(f){ if(f<.06) return lerp(72,95,f/.06); if(f<.30) return 95; if(f<.40) return lerp(95,55,(f-.30)/.10); if(f<.60) return 55; if(f<.66) return lerp(55,72,(f-.60)/.06); return 72; }
  function fracNow(){ return ph==='den'?.06+u*.24:ph==='ann'?.40+u*.20:ph==='ext'?.66+u*.34:0; }
  function nowTemp(){ return ph==='idle'?(n===0?25:72):Math.round(tempAt(fracNow())); }
  function dTemp(){ const x=6, y=MY+MH+12, w=404, h=H-y-6; rr(x,y,w,h,10); ctx.fillStyle='#fff'; ctx.fill(); ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; ctx.stroke();
    const Lx=x+40, R=x+w-12, Tp=y+26, B=y+h-26, c0=Math.max(0,Math.min(n-1,(+$('cyc').value)-3)), span=3, Xc=c=>Lx+(c-c0)/span*(R-Lx), Y=v=>B-(v-20)/(100-20)*(B-Tp);
    tx('温度の変化',x+10,y+17,12,'#0f172a','left',true);
    [[95,'#ef4444','熱変性'],[72,'#f59e0b','伸長'],[55,'#3b82f6','アニーリング']].forEach(o=>{ ctx.strokeStyle='rgba(148,163,184,.35)'; ctx.lineWidth=1; ctx.setLineDash([3,3]); ctx.beginPath(); ctx.moveTo(Lx,Y(o[0])); ctx.lineTo(R,Y(o[0])); ctx.stroke(); ctx.setLineDash([]); tx(o[0]+'℃',Lx-5,Y(o[0])+4,10.5,o[1],'right',true); });
    ctx.save(); ctx.beginPath(); ctx.rect(Lx,Tp-8,R-Lx,B-Tp+16); ctx.clip();
    const cur=n+fracNow(); ctx.lineWidth=2.4; ctx.lineJoin='round';
    for(const pass of [0,1]){ ctx.strokeStyle=pass?'#0d9488':'#cbd5e1'; ctx.beginPath(); let first=true; for(let c=c0;c<=c0+span+.001;c+=.01){ if(pass&&c>cur) break; const v=tempAt(c-Math.floor(c+1e-9)); const xx=Xc(c), yy=Y(c>=+$('cyc').value?72:v); first?ctx.moveTo(xx,yy):ctx.lineTo(xx,yy); first=false; } ctx.stroke(); }
    ctx.restore();
    for(let c=c0;c<c0+span;c++){ if(c>=+$('cyc').value) break; tx((c+1)+'サイクル目',Xc(c+.5),B+17,10.5,'#475569','center',c===n&&ph!=='idle'); ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(Xc(c),Tp-6); ctx.lineTo(Xc(c),B+4); ctx.stroke(); }
    if(cur<=c0+span){ const v=ph==='idle'?72:tempAt(fracNow()); ctx.beginPath(); ctx.arc(Xc(cur),Y(n===0&&ph==='idle'?72:v),6,0,7); ctx.fillStyle='#f59e0b'; ctx.fill(); ctx.strokeStyle='#fff'; ctx.lineWidth=2; ctx.stroke(); }
  }
  function dCount(){ const x=416, y=MY+MH+12, w=W-x-6, h=H-y-6; rr(x,y,w,h,10); ctx.fillStyle='#fff'; ctx.fill(); ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; ctx.stroke();
    tx('二本鎖DNAの数',x+10,y+17,12,'#0f172a','left',true); const c1=n, c0=Math.max(0,c1-5), m=c1-c0+1, bw=(w-24)/6, B=y+h-24, Hh=h-64, mx=total(c1);
    for(let c=c0;c<=c1;c++){ const bx=x+12+(c-c0)*bw, hh=Math.max(2,total(c)/mx*Hh), th=target(c)/mx*Hh; ctx.fillStyle='#cbd5e1'; ctx.fillRect(bx+3,B-hh,bw-6,hh); if(th>0){ ctx.fillStyle='#22c55e'; ctx.fillRect(bx+3,B-th,bw-6,th); }
      const tv=total(c); tx(tv>=1e8?(tv/1e8).toFixed(1)+'億':tv>=1e5?Math.round(tv/1e4)+'万':num(tv),bx+bw/2,B-hh-4,tv>=1e5?9:10,'#0f172a','center',true); tx(c+'回',bx+bw/2,B+14,10,'#475569','center'); }
    ctx.fillStyle='#22c55e'; ctx.fillRect(x+w-104,y+8,9,9); tx('目的の長さ',x+w-92,y+16,9.5,'#15803d','left',true);
  }
  function title(){ if(ph==='den') return ['① 熱変性（約95℃）：塩基どうしの水素結合が切れ、2本の一本鎖に分かれる','#dc2626'];
    if(ph==='ann') return ['② アニーリング（約55℃）：2種類のプライマーが、相補的な配列に結合する','#2563eb'];
    if(ph==='ext') return ['③ 伸長（約72℃）：DNAポリメラーゼがプライマーの3′端から新しい鎖を合成する','#d97706'];
    if(n===0) return ['はじめの状態：増やしたい領域をふくむ二本鎖DNAが1本','#0f172a'];
    return [n+'サイクル終了：二本鎖は '+num(total(n))+' 本、そのうち目的の長さは '+num(target(n))+' 本','#0f172a']; }
  function draw(){ ctx.clearRect(0,0,W,H); ctx.fillStyle='#f8fafc'; ctx.fillRect(0,0,W,H);
    const tt=title(); rr(0,0,W,36,10); ctx.fillStyle='#fff'; ctx.fill(); ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; ctx.stroke(); tx(tt[0],12,23,12.5,tt[1],'left',true);
    const tc=nowTemp(); tx(tc+'℃',W-12,24,15,tc>=90?'#dc2626':tc>=65?'#d97706':tc>=40?'#2563eb':'#475569','right',true);
    ctx.save(); rr(0,MY-8,W,MH+16,10); ctx.clip(); ctx.fillStyle='#fff'; ctx.fillRect(0,MY-8,W,MH+16); if(detail()) dDetail(); else dOverall(); ctx.restore(); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1; rr(.5,MY-7.5,W-1,MH+15,10); ctx.stroke();
    if(names&&detail()){ const y=MY+MH-4; rr(8,y-13,W-16,20,7); ctx.fillStyle='rgba(255,255,255,.92)'; ctx.fill(); let x=16; [[C_ORIG,'もとのDNA（鋳型）'],[C_NEW,'新しく合成された鎖'],[C_F,'プライマーF'],[C_R,'プライマーR']].forEach(o=>{ seg(x,x+18,y-3,o[0],5); tx(o[1],x+23,y+1,10.5,'#0f172a','left',true); x+=23+tw(o[1],10.5,true)+12; }); pol(x+8,y-3); tx('DNAポリメラーゼ',x+22,y+1,10.5,'#0f172a','left',true); }
    dTemp(); dCount();
    setStat('sN',n+' 回'); setStat('sD',num(total(n))+' 本'); setStat('sG',num(target(n))+' 本'); { const rt=n?target(n)/total(n):0; setStat('sR',rt>.9995?'99.9 %以上':(Math.round(rt*1000)/10)+' %'); }
    setShare('【PCR法】'+n+'サイクルで、二本鎖DNAは'+num(total(n))+'本に。そのうち目的の長さは'+num(target(n))+'本｜シミュラボ'); }
  function loop(){ const sp=+$('spd').value, k=Math.max(1,Math.round(sp*2)); for(let i=0;i<k;i++) step(1/120); draw(); requestAnimationFrame(loop); }
  $('play').addEventListener('click',()=>{ if(!playing&&ph==='idle'&&n>=+$('cyc').value){ return; } playing=!playing; if(playing&&ph==='idle') u=1; upd(); });
  $('stepb').addEventListener('click',()=>{ playing=false; if(ph==='idle') advance(); else { u=1; advance(); } upd(); });
  $('rst').addEventListener('click',reset);
  $('cyc').addEventListener('input',()=>{ if(n>+$('cyc').value) reset(); });
  $('names').addEventListener('click',()=>{ names=!names; $('names').textContent=names?'🏷 名前をかくす':'🏷 名前を表示'; });
  window.__test={step:function(s){ const k=Math.round(s*60); for(let i=0;i<k;i++) step(1/60); draw(); },play:function(){ playing=true; if(ph==='idle') u=1; },next:function(){ $('stepb').click(); draw(); },
    get s(){ return {n:n,ph:ph,u:+u.toFixed(2),N:dups.length,tgt:dups.filter(isTarget).length,formula:[total(n),target(n)],d:dups.slice(0,8).map(d=>'T['+d.T.s+','+d.T.e+(d.T.nw?'n':'o')+'] B['+d.B.s+','+d.B.e+(d.B.nw?'n':'o')+']')}; }};
  reset(); loop();
'''

ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
<p><b>PCR法</b>（ポリメラーゼ連鎖反応法）は、DNAの中の目的の領域だけを、試験管の中で短時間に大量に増やす方法です。温度を「高温 → 低温 → 中くらい」と変えるだけで、DNAの二本鎖が分かれ、プライマーが結合し、DNAポリメラーゼが新しい鎖を合成します。このシミュレーターでは、3つの段階でDNAに何が起きているかと、サイクルをくり返すうちに目的の長さのDNAが増えていくしくみを、鎖を色分けして追うことができます。</p>
''' + N('<b>対応する単元</b>：高等学校「生物」（3）遺伝情報の発現と発生 ア（ｳ）遺伝子を扱う技術（その原理と有用性）。DNAの複製（DNAポリメラーゼ・鎖の方向性・相補性）の学習とあわせて使えます。') + '''
<h2>授業での使い方</h2>
<h3>導入：1サイクルを段階ごとに止めて見る</h3>
<p>「⏭ 次の段階へ」を押すと、1段階ずつ進みます。①熱変性では、塩基どうしの水素結合（鎖のあいだの細い線）が切れて、2本の一本鎖に分かれます。鎖そのものは切れません。②アニーリングでは、緑のプライマーFと紫のプライマーRが、それぞれの鋳型の相補的な配列に結合します。ここで止めて「どちら向きにDNAが伸びるだろう」と予想させます。③伸長では、DNAポリメラーゼがプライマーの3′端から 5′→3′ の向きに新しい鎖（オレンジ）を合成します。プライマーは新しい鎖の一部になります。</p>
<h3>展開：1〜3サイクル目を追う</h3>
<p>1サイクル目にできる新しい鎖は、プライマーの位置から始まり、鋳型の端まで伸びるので、目的の領域より長くなります。2サイクル目では、その長い鎖が鋳型になり、もう一方のプライマーから伸びた鎖は、1サイクル目の鎖の始まり（プライマーの位置）で止まります。こうして、両端がプライマーで決まった長さの一本鎖ができます。3サイクル目で、その鎖が鋳型になって、目的の長さの二本鎖（緑のわく）がはじめて2本できます。</p>
<h3>まとめ：サイクルをくり返す</h3>
<p>「サイクル数」を10や20、30に上げて再生すると、4サイクル目からは全体の表示に切りかわり、DNAが1サイクルごとに2倍に増えるようすと、そのほとんどが目的の長さのDNAになっていくことがわかります。右下のグラフで本数を確かめられます。</p>
<h3>生徒への問いの例</h3>
<ol>
<li>プライマーが2種類必要なのはなぜだろう？1種類だけだと、何サイクルくり返してもどうなるだろう？</li>
<li>2種類のプライマーの3′端が、増やしたい領域の内側を向いていなければならないのはなぜだろう？</li>
<li>目的の長さの二本鎖は、何サイクル目にはじめてできるだろう？10サイクル後には全体の何%になるだろう？</li>
</ol>
<h2>しくみ・解説</h2>
<h3>用語</h3>
<ul>
<li><b>鋳型（いがた）</b>とは、新しい鎖を合成するときに、塩基配列のもとになるDNAの鎖です。</li>
<li><b>プライマー</b>とは、鋳型の特定の配列に相補的に結合する短い一本鎖のDNAです。DNAポリメラーゼは、プライマーの3′端にヌクレオチドをつないで鎖を伸ばします。PCR法では、増やしたい領域をはさむ2種類を使います。</li>
<li><b>DNAポリメラーゼ</b>とは、鋳型に相補的なヌクレオチドを、鎖の3′端に次々につないでいく酵素です。新しい鎖は必ず 5′→3′ の向きに伸びます。PCR法では、95℃でも失活しない好熱菌のDNAポリメラーゼを使います。</li>
<li><b>5′端・3′端</b>とは、DNAの鎖の両端の区別です。二本鎖DNAでは、2本の鎖が逆向きに並んでいます。</li>
</ul>
<h3>3つの段階</h3>
''' + T([["① 熱変性", "約95℃", "塩基対の水素結合が切れ、二本鎖DNAが2本の一本鎖に分かれる"],
          ["② アニーリング", "約50〜65℃", "温度を下げると、プライマーが鋳型の相補的な配列に結合する"],
          ["③ 伸長", "約72℃", "DNAポリメラーゼが、プライマーの3′端から新しい鎖を 5′→3′ の向きに合成する"]],
         ["段階", "温度（代表的な例）", "DNAに起きること"]) + '''
<h3>サイクルごとの本数</h3>
<p>理想的な条件では、1サイクルごとにすべての鎖が鋳型になるので、二本鎖DNAは 1 → 2 → 4 → 8 … と2倍ずつ増え、n サイクル後には 2<sup>n</sup> 本になります。このうち、もとの長い鎖や、片側だけが長い鎖をふくむ二本鎖は 2n 本しかないので、両方の鎖が目的の長さである二本鎖は 2<sup>n</sup> − 2n 本です。</p>
''' + T([["1", "2", "0", "0%"], ["2", "4", "0", "0%"], ["3", "8", "2", "25%"], ["5", "32", "22", "約69%"],
          ["10", "1,024", "1,004", "約98%"], ["20", "1,048,576", "1,048,536", "約99.996%"], ["30", "約10億7千万", "約10億7千万", "ほぼ100%"]],
         ["サイクル数", "二本鎖DNAの数", "目的の長さの二本鎖", "割合"]) + '''
''' + P('2種類のプライマーの位置が、増えるDNAの両端を決めます。プライマーを設計することで、長いDNAの中の調べたい部分だけを選んで増やすことができます。') + '''
<h3>このシミュレーターのモデル</h3>
<p>鎖の長さ・プライマーの長さは模式的なものです（実際のプライマーは20塩基ほど、増やす領域は数百〜数千塩基対がふつうです）。温度は教材でよく使われる代表的な値で、アニーリングの温度はプライマーの配列によって変わります。すべての鎖が毎回かならず複製される理想的な条件を表しており、実際には、サイクル数が増えるとプライマーやヌクレオチドが減るなどの理由で、増え方はしだいにゆるやかになります。4サイクル目からは、鎖1本ずつではなく、全体の本数と種類の割合を表示します。</p>
<h2>参考</h2>
<ul>
<li>''' + A(MEXT_KOU, "文部科学省 高等学校学習指導要領（平成30年告示）解説 理科編") + '''（生物（3）遺伝情報の発現と発生）</li>
<li>高等学校「生物」の教科書（遺伝子を扱う技術：PCR法、DNAの複製）</li>
</ul>
'''

sim(slug="pcr-hou", cat="rika", emoji="🧬", score=81,
    title="PCR法のシミュレーター（熱変性・アニーリング・伸長とDNAの増え方）",
    title_tag="PCR法のしくみシミュレーター｜熱変性・アニーリング・伸長とプライマー、DNAが増えるサイクル（高校生物）",
    meta_desc="PCR法の3段階（熱変性・アニーリング・伸長）で、DNAの二本鎖・プライマー・DNAポリメラーゼがどう動くかを、鎖を色分けして1段階ずつ追えるシミュレーター。1〜3サイクル目で目的の長さのDNAができる過程と、サイクルごとに2倍に増える様子、温度変化のグラフを連動して観察できます。",
    og_title="PCR法のシミュレーター（熱変性・アニーリング・伸長とDNAの増え方）",
    og_desc="95℃で分かれ、55℃でプライマーが結合し、72℃で伸びる。目的の長さの二本鎖がはじめてできるのは3サイクル目。もとのDNA・新しい鎖・2種類のプライマーを色分けして、増えるしくみを追う。",
    card_desc="熱変性・アニーリング・伸長の3段階と、3サイクル目に目的の長さのDNAができるしくみを、鎖を色分けして追う。",
    lead="紺色がもとのDNA（鋳型）、黄色の帯が増やしたい領域です。「⏭ 次の段階へ」で1段階ずつ、「▶ 再生」で続けて進みます。温度が変わるたびに、二本鎖が分かれ、緑と紫の2種類のプライマーが結合し、DNAポリメラーゼがオレンジ色の新しい鎖を合成します。どの鎖が次のサイクルの鋳型になるかを追ってみましょう。",
    model="生物 遺伝子を扱う技術（PCR法）",
    level="高校（生物）",
    unit="高等学校 生物（3）遺伝情報の発現と発生 ア（ｳ）遺伝子を扱う技術",
    canvas=canvas(640, 590, light=True),
    controls=slider("cyc", "サイクル数（ここまで進める）", 1, 30, 3, 1, "{v} サイクル")
             + select("spd", "速さ", [("1", "×1"), ("2", "×2"), ("4", "×4"), ("0.5", "×0.5（ゆっくり）")]),
    buttons=btn("play", "▶ 再生", True) + btn("stepb", "⏭ 次の段階へ") + btn("rst", "↺ はじめから") + btn("names", "🏷 名前をかくす"),
    stats=stats([("sN", "終わったサイクル", False), ("sD", "二本鎖DNAの数", True), ("sG", "目的の長さの二本鎖", True), ("sR", "目的の長さの割合", False)]),
    legend=PH + "紺＝もとのDNA（鋳型）、オレンジ＝新しく合成された鎖、緑＝プライマーF、紫＝プライマーR、青緑の丸＝DNAポリメラーゼ。矢印の先が鎖の3′端です。上の鎖は左が5′端、下の鎖は右が5′端。鎖のあいだの細い線は塩基対（水素結合）、黄色の帯は増やしたい領域、緑のわくは目的の長さの二本鎖です。",
    article=ARTICLE,
    faqs=[("PCR法の3つの段階は？", "①熱変性（約95℃）：二本鎖DNAの塩基対の水素結合が切れて、2本の一本鎖に分かれます。②アニーリング（約50〜65℃）：プライマーが鋳型の相補的な配列に結合します。③伸長（約72℃）：DNAポリメラーゼがプライマーの3′端から新しい鎖を合成します。この3段階を1サイクルとして、20〜40回ほどくり返します。"),
          ("プライマーが2種類必要なのはなぜ？", "DNAの2本の鎖は逆向きで、DNAポリメラーゼは 5′→3′ の向きにしか鎖を伸ばせません。そのため、2本の鎖それぞれについて、増やしたい領域の端に結合するプライマーが1種類ずつ必要です。2種類のプライマーが領域を両側からはさむことで、両端が決まった長さのDNAが増えていきます。"),
          ("目的の長さのDNAは何サイクル目にできるの？", "両方の鎖が目的の長さである二本鎖DNAは、3サイクル目にはじめてできます。1サイクル目の新しい鎖は鋳型の端まで伸びるので長く、2サイクル目に両端がプライマーで決まった長さの一本鎖ができ、3サイクル目にそれが鋳型になって、目的の長さの二本鎖になります。"),
          ("n サイクル後、DNAは何本になるの？", "理想的な条件では、1サイクルごとに2倍になるので、1本の二本鎖DNAから始めると n サイクル後には 2ⁿ 本になります。このうち両方の鎖が目的の長さのものは 2ⁿ − 2n 本です。30サイクルでは約10億本になり、ほぼすべてが目的の長さです。"),
          ("なぜ熱に強いDNAポリメラーゼを使うの？", "熱変性の段階では約95℃まで温度を上げます。ふつうの酵素はこの温度で変性して失活するので、サイクルのたびに酵素を加え直さなければなりません。温泉などにすむ好熱菌のDNAポリメラーゼは高温でも失活しないので、温度を上げ下げするだけで反応をくり返せます。"),
          ("熱変性でDNAの鎖は切れるの？", "切れません。熱変性で切れるのは、2本の鎖の塩基どうしを結びつけている水素結合です。それぞれの鎖のヌクレオチドどうしをつなぐ結合（糖とリン酸の結合）はそのままなので、塩基配列は保たれます。")],
    rel=[("dna", "🧬", "DNA二重らせん"), ("kouso-shikkatsu", "🌡️", "酵素の失活シミュレーター"),
         ("tensha-honyaku-genkaku", "🧫", "原核生物の転写と翻訳シミュレーター"), ("saibou-bunretsu", "🔬", "細胞分裂シミュレーター"), ("mendel-iden", "🌱", "遺伝の規則性シミュレーター")],
    js=JS)
