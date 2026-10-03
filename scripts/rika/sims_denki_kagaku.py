# -*- coding: utf-8 -*-
"""理科の授業向けシミュ（電流と磁界・化学変化と質量）
   denryu-jikai      … 小5「電流がつくる磁力」／中2「電流と磁界」（第1分野（3）電流とその利用 ア（イ））
   kagaku-shitsuryou … 中2「化学変化と物質の質量」（第1分野（4）化学変化と原子・分子 ア（ウ））"""
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

MEXT_SHO = "https://www.mext.go.jp/a_menu/shotou/new-cs/1387014.htm"
MEXT_CHU = "https://www.mext.go.jp/a_menu/shotou/new-cs/1387016.htm"
def A(url, label): return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, label)
def NW(t): return '<span style="white-space:nowrap">%s</span>' % t


# ============================================================ 1 電流と磁界
JS_DENRYU = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const FF='"Hiragino Sans","Hiragino Kaku Gothic ProN","Noto Sans JP","Yu Gothic UI","Yu Gothic",Meiryo,sans-serif';
  const C={bg:'#f8fafc',ink:'#0f172a',sub:'#64748b',cur:'#f97316',fld:'#2563eb',frc:'#16a34a',N:'#dc2626',S:'#2563eb',wire:'#57534e',coil:'#b45309',lead:'#94a3b8'};
  const VIEWS={m1:[['wire','まっすぐな導線'],['coil','コイル']],m3:[['swing','ぶらんこ実験（力の向き）'],['motor','モーターが回るしくみ']],m4:[['move','磁石を出し入れする'],['gen','発電機（交流）']]};
  const DIR8=['東','北東','北','北西','西','南西','南','南東'];
  const Q=new URLSearchParams(location.search);
  let dirI=1, earth=false, probe=[4.9,-3.3], drag=null, dragOff=0, last=0, tNow=0, stT=0, wo=0, so=0, nd={}, curKey='';
  let core=true, swOn=true, shown=-1, recs=[];
  let magUp=1, phi=0, phiV=0, swingInit=true, comm=true, pSide=1, alpha=0.7, omega=0, motorInit=true;
  let magN=1, mX=120, mPrev=120, mTarget=null, Lprev=null, vS=0, ndl=0, ndlV=0, iNow=0, peakAbs=0, hist=[], theta=0.5, thPrev=0.5, wGen=0, playing=true, rotA=0;

  // ---------- 描画の部品 ----------
  function fmt(v,d){ return (+v).toFixed(d==null?1:d); }
  function tx(s,x,y,size,col,align,bold){ ctx.font=(bold?'bold ':'')+size+'px '+FF; ctx.textAlign=align||'left'; ctx.fillStyle=col; ctx.fillText(s,x,y); ctx.textAlign='left'; }
  function tw(s,size,bold){ ctx.font=(bold?'bold ':'')+size+'px '+FF; return ctx.measureText(s).width; }
  function rr(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
  function tag(s,x,y,size,col,align,bd){ const w=tw(s,size,true), x0=align==='right'?x-w:align==='center'?x-w/2:x; ctx.fillStyle='rgba(255,255,255,0.9)'; rr(x0-4,y-size-1,w+8,size+6,5); ctx.fill(); if(bd){ ctx.strokeStyle=bd; ctx.lineWidth=1.2; ctx.stroke(); } tx(s,x0,y,size,col,'left',true); }
  function head(x,y,ux,uy,col,s){ const l=Math.hypot(ux,uy)||1; ux/=l; uy/=l; s=s||6; const bx=x-ux*s*1.6, by=y-uy*s*1.6; ctx.fillStyle=col; ctx.beginPath(); ctx.moveTo(x,y); ctx.lineTo(bx-uy*s*0.85,by+ux*s*0.85); ctx.lineTo(bx+uy*s*0.85,by-ux*s*0.85); ctx.closePath(); ctx.fill(); }
  function arr(x1,y1,x2,y2,col,w,s){ const dx=x2-x1, dy=y2-y1, l=Math.hypot(dx,dy); if(l<1) return; s=s||Math.max(5,w*2); const ux=dx/l, uy=dy/l, cut=Math.min(l,s*1.3); ctx.strokeStyle=col; ctx.lineWidth=w; ctx.lineCap='round'; ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2-ux*cut,y2-uy*cut); ctx.stroke(); head(x2,y2,ux,uy,col,s); }
  function dot(x,y,r,col){ ctx.fillStyle=col; ctx.beginPath(); ctx.arc(x,y,r,0,7); ctx.fill(); }
  function panel(x,y,w,h,title){ ctx.fillStyle='#fff'; ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1.2; rr(x,y,w,h,10); ctx.fill(); ctx.stroke(); if(title) tx(title,x+10,y+19,12.5,C.ink,'left',true); }
  function legend(items,y){ let x=14; items.forEach(it=>{ if(it[2]==='dot'){ dot(x+5,y-4,4.5,it[1]); x+=15; } else if(it[2]==='line'){ ctx.strokeStyle=it[1]; ctx.lineWidth=3; ctx.lineCap='round'; ctx.beginPath(); ctx.moveTo(x,y-4); ctx.lineTo(x+12,y-4); ctx.stroke(); x+=17; } tx(it[0],x,y,11.5,it[2]?it[1]:C.sub,'left',true); x+=tw(it[0],11.5,true)+14; }); }
  // 立体（平行投影）：x 右、y 奥、z 上
  function mk(cx,cy,k,yaw,pitch){ const cw=Math.cos(yaw), sw=Math.sin(yaw), cp=Math.cos(pitch), sp=Math.sin(pitch), a=k*cw, b=k*sw*sp, c=k*sw, d=-k*cw*sp, e=-k*cp;
    return {a:a,b:b,c:c,d:d,e:e,cx:cx,cy:cy,k:k, p:(x,y,z)=>[cx+a*x+c*y, cy+b*x+d*y+e*(z||0)], v:(x,y,z)=>[a*x+c*y, b*x+d*y+e*(z||0)],
      inv:(X,Y)=>{ const u=X-cx, w=Y-cy, det=a*d-b*c; return [(d*u-c*w)/det,(-b*u+a*w)/det]; } }; }
  function poly(P,pts,close){ ctx.beginPath(); pts.forEach((q,i)=>{ const s=P.p(q[0],q[1],q[2]); if(i) ctx.lineTo(s[0],s[1]); else ctx.moveTo(s[0],s[1]); }); if(close) ctx.closePath(); }
  function face(P,pts,fill){ poly(P,pts,true); ctx.fillStyle=fill; ctx.fill(); ctx.strokeStyle='rgba(15,23,42,0.3)'; ctx.lineWidth=1; ctx.stroke(); }
  function box(P,x0,x1,y0,y1,z0,z1,cf,cs,ct){ const xs=P.c<0?x0:x1; face(P,[[xs,y0,z0],[xs,y1,z0],[xs,y1,z1],[xs,y0,z1]],cs); face(P,[[x0,y0,z1],[x1,y0,z1],[x1,y1,z1],[x0,y1,z1]],ct); face(P,[[x0,y0,z0],[x1,y0,z0],[x1,y0,z1],[x0,y0,z1]],cf); }
  function line3(P,p,q,col,w){ const a=P.p(p[0],p[1],p[2]), b=P.p(q[0],q[1],q[2]); ctx.strokeStyle=col; ctx.lineWidth=w; ctx.lineCap='round'; ctx.beginPath(); ctx.moveTo(a[0],a[1]); ctx.lineTo(b[0],b[1]); ctx.stroke(); }
  function arr3(P,p,q,col,w,s){ const a=P.p(p[0],p[1],p[2]), b=P.p(q[0],q[1],q[2]); arr(a[0],a[1],b[0],b[1],col,w,s); }
  function pathLen(pts){ let L=0; for(let i=1;i<pts.length;i++) L+=Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1]); return L; }
  function ptAt(pts,s){ for(let i=1;i<pts.length;i++){ const dx=pts[i][0]-pts[i-1][0], dy=pts[i][1]-pts[i-1][1], l=Math.hypot(dx,dy); if(s<=l&&l>0) return [pts[i-1][0]+dx*s/l, pts[i-1][1]+dy*s/l, i-1]; s-=l; } const q=pts[pts.length-1]; return [q[0],q[1],pts.length-2]; }
  function dotsOn(pts,off,gap){ const L=pathLen(pts); if(L<1) return []; const n=Math.max(1,Math.round(L/gap)), g=L/n, o=((off%g)+g)%g, out=[]; for(let s=o; s<L-0.01; s+=g) out.push(ptAt(pts,s)); return out; }
  // 電池の記号（ang＝導線の向き、plusAt＝＋極（長い線）の側 ±1）
  function battery(x,y,ang,plusAt){ const u=[Math.cos(ang),Math.sin(ang)], n=[-u[1],u[0]];
    ctx.save(); ctx.translate(x,y); ctx.rotate(ang); ctx.fillStyle=C.bg; ctx.fillRect(-9,-16,18,32);
    ctx.strokeStyle=C.ink; ctx.lineCap='butt'; ctx.lineWidth=2.4; ctx.beginPath(); ctx.moveTo(4*plusAt,-14); ctx.lineTo(4*plusAt,14); ctx.stroke();
    ctx.lineWidth=6; ctx.beginPath(); ctx.moveTo(-4*plusAt,-7); ctx.lineTo(-4*plusAt,7); ctx.stroke(); ctx.lineCap='round'; ctx.restore();
    tx('＋',x+u[0]*12*plusAt-n[0]*21,y+u[1]*12*plusAt-n[1]*21+5,13,C.ink,'center',true); tx('－',x-u[0]*12*plusAt-n[0]*21,y-u[1]*12*plusAt-n[1]*21+5,13,C.ink,'center',true); }

  // ---------- 入力・統計欄 ----------
  const fld=id=>{ const e=$(id); return e?e.closest('.field'):null; };
  const K=id=>$(id).previousElementSibling;
  function sh(id,m,sub){ const e=$(id); if(e) e.innerHTML=m+(sub?'<span style="display:block;font-size:12px;font-weight:700;color:#59616c;margin-top:2px">'+sub+'</span>':''); }
  function show(id,on){ const e=$(id); if(e) e.style.display=on?'':'none'; }
  function showF(id,on){ const e=fld(id); if(e) e.style.display=on?'':'none'; }
  function Iof(){ return +$('cur').value; }
  function setViews(m){ const s=$('view'), v=VIEWS[m]; if(!v) return; if(s.dataset.m!==m){ s.innerHTML=v.map(o=>'<option value="'+o[0]+'">'+o[1]+'</option>').join(''); s.dataset.m=m; } }

  // =============== ① 導線・コイルのまわりの磁界 ===============
  const PB=mk(224,236,21,-0.32,0.56), BX=7.6, BY=5.6, CN=8, CL=7.4, CA=1.9;
  const CPW=[[3,0],[2.12,2.12],[0,3],[-2.12,2.12],[-3,0],[-2.12,-2.12],[0,-3],[2.12,-2.12]];
  const CPC=[[-6.0,0],[6.0,0],[0,-4.1],[0,4.1],[-4.9,-3.9],[4.9,-3.9]];
  // 厚紙をつらぬく導線（上向きの電流を＋）。B[μT]＝20×I[A]÷r[cm]
  function coilList(I){ const L=[]; for(let j=0;j<CN;j++){ L.push([-CL/2+CL*j/CN,-CA,20*I*dirI]); L.push([-CL/2+CL*(j+0.5)/CN,CA,-20*I*dirI]); } return L; }
  function Bsum(list,x,y){ let bx=0,by=0; for(const q of list){ const dx=x-q[0], dy=y-q[1], r2=dx*dx+dy*dy+0.04, c=q[2]/r2; bx-=dy*c; by+=dx*c; } return [bx,by]; }
  function Bat(x,y){ const I=Iof(); return $('view').value==='coil'?Bsum(coilList(I),x,y):Bsum([[0,0,20*I*dirI]],x,y); }
  function needle(key,x,y,dt){ const b=Bat(x,y), tg=Math.atan2(b[1]+(earth?30:0.3),b[0]); let a=nd[key]; if(a==null){ nd[key]=tg; return tg; } let d=tg-a; d=Math.atan2(Math.sin(d),Math.cos(d)); a+=d*Math.min(1,dt*9); nd[key]=a; return a; }
  function boardPath(P){ poly(P,[[-BX,-BY,0],[BX,-BY,0],[BX,BY,0],[-BX,BY,0]],true); }
  function drawBoard(P){ face(P,[[-BX,-BY,-0.45],[BX,-BY,-0.45],[BX,-BY,0],[-BX,-BY,0]],'#e7dfcc'); face(P,[[-BX,-BY,-0.45],[-BX,BY,-0.45],[-BX,BY,0],[-BX,-BY,0]],'#ddd4bf');
    boardPath(P); ctx.fillStyle='rgba(255,251,240,0.94)'; ctx.fill(); ctx.strokeStyle='#d6cfbd'; ctx.lineWidth=1.4; ctx.stroke();
    const n0=P.p(-BX+0.9,BY-2.6,0), n1=P.p(-BX+0.9,BY-0.7,0); arr(n0[0],n0[1],n1[0],n1[1],'#a8a29e',2,4); tx('北',n1[0]+7,n1[1]+9,11,'#a8a29e','left',true); }
  function onBoard(P,fn){ ctx.save(); ctx.setTransform(dpr*P.a,dpr*P.b,dpr*P.c,dpr*P.d,dpr*P.cx,dpr*P.cy); fn(); ctx.restore(); }
  function compassB(P,x,y,R,ang,hl){ onBoard(P,()=>{ ctx.translate(x,y);
    ctx.fillStyle='rgba(15,23,42,0.14)'; ctx.beginPath(); ctx.arc(0.12,-0.14,R,0,7); ctx.fill();
    ctx.fillStyle=hl?'#fffbe6':'#fff'; ctx.strokeStyle=hl?'#ca8a04':'#64748b'; ctx.lineWidth=hl?0.13:0.08; ctx.beginPath(); ctx.arc(0,0,R,0,7); ctx.fill(); ctx.stroke();
    ctx.rotate(ang); const L=R*0.84, w=R*0.22;
    ctx.fillStyle=C.N; ctx.beginPath(); ctx.moveTo(L,0); ctx.lineTo(0,w); ctx.lineTo(0,-w); ctx.closePath(); ctx.fill();
    ctx.fillStyle='#e2e8f0'; ctx.beginPath(); ctx.moveTo(-L,0); ctx.lineTo(0,w); ctx.lineTo(0,-w); ctx.closePath(); ctx.fill(); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=0.04; ctx.stroke();
    ctx.fillStyle='#334155'; ctx.beginPath(); ctx.arc(0,0,R*0.11,0,7); ctx.fill(); }); }
  // 導線のまわりの磁力線：本数は電流に比例（同じ磁束ごとに1本＝半径は等比で並ぶ）
  function wireLines(P,I,s){ if(I<=0) return; const st=0.6/I; let k=0; ctx.lineWidth=1.3;
    for(let lr=Math.log(0.72); lr<Math.log(9.6); lr+=st, k++){ const r=Math.exp(lr); ctx.strokeStyle='rgba(37,99,235,'+Math.max(0.3,0.8-0.045*r).toFixed(3)+')'; ctx.beginPath();
      for(let j=0;j<=80;j++){ const t=j/80*2*Math.PI, q=P.p(r*Math.cos(t),r*Math.sin(t),0); if(j) ctx.lineTo(q[0],q[1]); else ctx.moveTo(q[0],q[1]); } ctx.stroke();
      if(r>1.5) [0.55+0.9*k, 0.55+0.9*k+Math.PI].forEach(t0=>{ const x=r*Math.cos(t0), y=r*Math.sin(t0); if(Math.abs(x)>BX-0.4||Math.abs(y)>BY-0.4) return; const q=P.p(x,y,0), v=P.v(-Math.sin(t0)*s,Math.cos(t0)*s,0); head(q[0]+v[0]*0.12,q[1]+v[1]*0.12,v[0],v[1],'rgba(37,99,235,0.95)',4.2); }); } }
  function miniCompass(px,py,ang){ ctx.fillStyle='#fff'; ctx.strokeStyle='#64748b'; ctx.lineWidth=1.2; ctx.beginPath(); ctx.arc(px,py,9,0,7); ctx.fill(); ctx.stroke();
    ctx.save(); ctx.translate(px,py); ctx.rotate(ang); ctx.fillStyle=C.N; ctx.beginPath(); ctx.moveTo(7.5,0); ctx.lineTo(0,2.6); ctx.lineTo(0,-2.6); ctx.closePath(); ctx.fill(); ctx.fillStyle='#cbd5e1'; ctx.beginPath(); ctx.moveTo(-7.5,0); ctx.lineTo(0,2.6); ctx.lineTo(0,-2.6); ctx.closePath(); ctx.fill(); ctx.restore(); }
  function insetTop(x0,y0,w,h,s,on){ panel(x0,y0,w,h,'上から見ると'); const cx=x0+w/2, cy=y0+92;
    if(on) [22,38,54].forEach((r,i)=>{ ctx.strokeStyle='rgba(37,99,235,'+(0.85-i*0.2)+')'; ctx.lineWidth=1.6; ctx.beginPath(); ctx.arc(cx,cy,r,0,7); ctx.stroke(); head(cx-6*s,cy-r,-s,0,C.fld,4.5); head(cx+6*s,cy+r,s,0,C.fld,4.5); });
    [[0,-38],[38,0],[0,38],[-38,0]].forEach(q=>{ const ang=on?Math.atan2(-q[0]*s,q[1]*s):-Math.PI/2; miniCompass(cx+q[0],cy+q[1],ang); });
    ctx.fillStyle='#fff'; ctx.strokeStyle=C.ink; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(cx,cy,10,0,7); ctx.fill(); ctx.stroke();
    if(s>0) dot(cx,cy,3,C.ink); else { ctx.beginPath(); ctx.moveTo(cx-6,cy-6); ctx.lineTo(cx+6,cy+6); ctx.moveTo(cx+6,cy-6); ctx.lineTo(cx-6,cy+6); ctx.stroke(); }
    tx(s>0?'・＝電流が上（手前）へ':'×＝電流が下（向こう）へ',x0+8,y0+h-27,11,C.cur,'left',true);
    tx('磁界は'+(on?(s>0?'反時計回り':'時計回り'):'できない'),x0+8,y0+h-10,11.5,C.fld,'left',true); }
  function insetScrew(x0,y0,w,h,s){ panel(x0,y0,w,h,'右ねじの法則'); const sx=x0+32, ya=y0+32, yb=y0+h-12, mid=(ya+yb)/2+2, tipY=s>0?ya:yb, hdY=s>0?yb:ya;
    ctx.strokeStyle=C.fld; ctx.lineWidth=2.4; ctx.beginPath(); ctx.ellipse(sx,mid,23,8,0,Math.PI,2*Math.PI); ctx.stroke();
    ctx.fillStyle='#cbd5e1'; ctx.strokeStyle='#64748b'; ctx.lineWidth=1.2; ctx.fillRect(sx-6,ya+12,12,yb-ya-24); ctx.strokeRect(sx-6,ya+12,12,yb-ya-24);
    for(let y=ya+17;y<yb-15;y+=7){ ctx.beginPath(); ctx.moveTo(sx-6,y+3); ctx.lineTo(sx+6,y-3); ctx.stroke(); }
    const tb=tipY+(s>0?12:-12); ctx.fillStyle='#cbd5e1'; ctx.beginPath(); ctx.moveTo(sx-6,tb); ctx.lineTo(sx+6,tb); ctx.lineTo(sx,tipY); ctx.closePath(); ctx.fill(); ctx.stroke();
    ctx.fillStyle='#94a3b8'; rr(sx-14,s>0?hdY-12:hdY,28,12,3); ctx.fill(); ctx.stroke();
    ctx.strokeStyle=C.fld; ctx.lineWidth=2.4; ctx.beginPath(); ctx.ellipse(sx,mid,23,8,0,0,Math.PI); ctx.stroke();
    if(s>0) head(sx+19,mid+4.6,13.5,-6.6,C.fld,5); else head(sx-19,mid+4.6,-13.5,-6.6,C.fld,5);
    arr(sx+34,mid+(s>0?24:-24),sx+34,mid-(s>0?24:-24),C.cur,3,5);
    const tx0=x0+76; tx('ねじの進む向き',tx0,y0+50,11,C.cur,'left',true); tx('＝電流の向き',tx0,y0+66,11,C.cur,'left',true);
    tx('ねじを回す向き',tx0,y0+98,11,C.fld,'left',true); tx('＝磁界の向き',tx0,y0+114,11,C.fld,'left',true); }
  function sceneWire(dt){ const P=PB, I=Iof(), s=dirI, zt=6.4, zb=-5.3, RX=10.5;
    wo+=Math.min(170,36*I)*s*dt;
    const LP=[[0,0,zb],[0,0,zt],[RX,0,zt],[RX,0,zb],[0,0,zb]].map(q=>P.p(q[0],q[1],q[2]));
    ctx.strokeStyle=C.lead; ctx.lineWidth=2.2; ctx.lineJoin='round'; ctx.beginPath(); ctx.moveTo(LP[1][0],LP[1][1]); for(let i=2;i<5;i++) ctx.lineTo(LP[i][0],LP[i][1]); ctx.stroke();
    const p0=P.p(0,0,0), pt=LP[1], pb=LP[0];
    ctx.strokeStyle=C.wire; ctx.lineWidth=4.5; ctx.beginPath(); ctx.moveTo(pb[0],pb[1]); ctx.lineTo(p0[0],p0[1]); ctx.stroke();
    const dots=I>0?dotsOn(LP,wo,24):[];
    dots.forEach(d=>dot(d[0],d[1],3.1,C.cur));
    const pbat=P.p(RX,0,0.3); battery(pbat[0],pbat[1],Math.PI/2,s>0?1:-1); tx('電源',pbat[0]-14,pbat[1]+4,11.5,C.sub,'right',true);
    drawBoard(P);
    ctx.save(); boardPath(P); ctx.clip(); wireLines(P,I,s); ctx.restore();
    CPW.forEach((c,i)=>compassB(P,c[0],c[1],0.82,needle('w'+i,c[0],c[1],dt),false));
    compassB(P,probe[0],probe[1],1.1,needle('wp',probe[0],probe[1],dt),true);
    onBoard(P,()=>{ ctx.fillStyle='#44403c'; ctx.beginPath(); ctx.arc(0,0,0.22,0,7); ctx.fill(); });
    ctx.strokeStyle=C.wire; ctx.lineWidth=4.5; ctx.beginPath(); ctx.moveTo(p0[0],p0[1]); ctx.lineTo(pt[0],pt[1]); ctx.stroke();
    dots.forEach(d=>{ if(d[2]===0&&d[1]<p0[1]) dot(d[0],d[1],3.1,C.cur); });
    if(I>0){ const a1=P.p(0,0,s>0?2.4:4.6), a2=P.p(0,0,s>0?4.6:2.4); arr(a1[0]-16,a1[1],a2[0]-16,a2[1],C.cur,3,6); tag('電流',a1[0]-24,(a1[1]+a2[1])/2+5,12,C.cur,'right'); }
    const pp=P.p(probe[0],probe[1],0); tag('指で動かせる方位磁針',pp[0],pp[1]+31,11,'#a16207','center');
    tx('まっすぐな導線のまわりの磁界',14,24,15,C.ink,'left',true);
    tx('電流 '+fmt(I)+' A　'+(s>0?'下から上へ':'上から下へ')+'流れる',14,44,12.5,C.sub,'left');
    insetTop(472,10,158,192,s,I>0); insetScrew(472,210,158,150,s);
    legend([['電流（＋極→－極）',C.cur,'dot'],['磁力線（磁界の向き）',C.fld,'line'],['方位磁針は赤いほうがN極',C.sub]],388);
    tx(earth?'方位磁針は地球の磁界（北向き・約30 μT）も受けています':'地球の磁界は小さいとして、導線の磁界だけで向きを決めています',14,410,11,C.sub,'left');
    tx('導線や電源をタップすると電流の向きが反対になります',14,428,11,C.sub,'left'); }

  // コイル：厚紙の面の磁力線（等高線で同じ磁束ごとに1本）
  let CCache=null; const CH=0.12;
  function Aat(list,x,y){ let A=0; for(const q of list){ const dx=x-q[0], dy=y-q[1]; A-=q[2]*0.5*Math.log(dx*dx+dy*dy+1e-6); } return A; }
  function coilCache(P,I){ const key=I+'|'+dirI; if(CCache&&CCache.key===key) return CCache;
    const list=coilList(I), nx=Math.round(2*BX/CH)+1, ny=Math.round(2*BY/CH)+1, F=new Float32Array(nx*ny), M=new Uint8Array(nx*ny);
    for(let j=0;j<ny;j++){ const y=-BY+j*CH; for(let i=0;i<nx;i++){ const x=-BX+i*CH; let A=0, nr=0; for(const q of list){ const dx=x-q[0], dy=y-q[1], r2=dx*dx+dy*dy; A-=q[2]*0.5*Math.log(r2+1e-6); if(r2<0.1) nr=1; } F[j*nx+i]=A; M[j*nx+i]=nr; } }
    const unit=coilList(1), g1=Math.abs(Aat(unit,0,CA-0.4)-Aat(unit,0,-CA+0.4)), dA=g1*0.3, Acap=Math.abs(Aat(list,0,CA-0.3))*1.1, levels=[];
    for(let k=0; I>0&&(k+0.5)*dA<Acap; k++){ levels.push([(k+0.5)*dA,k]); levels.push([-(k+0.5)*dA,k]); }
    const segs=[];
    levels.forEach(Lv=>{ const L=Lv[0];
      for(let j=0;j<ny-1;j++) for(let i=0;i<nx-1;i++){ const k=j*nx+i; if(M[k]||M[k+1]||M[k+nx]||M[k+nx+1]) continue;
        const v0=F[k]-L, v1=F[k+1]-L, v2=F[k+nx+1]-L, v3=F[k+nx]-L; const b0=v0>0, b1=v1>0, b2=v2>0, b3=v3>0; if(b0===b1&&b1===b2&&b2===b3) continue;
        const X=-BX+i*CH, Y=-BY+j*CH, pts=[];
        if(b0!==b1) pts.push([X+CH*v0/(v0-v1),Y]); if(b1!==b2) pts.push([X+CH,Y+CH*v1/(v1-v2)]); if(b3!==b2) pts.push([X+CH*v3/(v3-v2),Y+CH]); if(b0!==b3) pts.push([X,Y+CH*v0/(v0-v3)]);
        for(let m=0;m+1<pts.length;m+=2){ const a=P.p(pts[m][0],pts[m][1],0), b=P.p(pts[m+1][0],pts[m+1][1],0); segs.push(a[0],a[1],b[0],b[1]); } } });
    const arrows=[]; [0,-(CL/2+2.4),CL/2+2.4].forEach(x=>{ const i=Math.round((x+BX)/CH);
      levels.forEach(Lv=>{ const L=Lv[0]; for(let j=0;j<ny-1;j++){ const k=j*nx+i; if(M[k]||M[k+nx]) continue; const v1=F[k]-L, v2=F[k+nx]-L; if((v1>0)===(v2>0)) continue; const y=-BY+(j+v1/(v1-v2))*CH;
        if(Math.abs(x)<0.1&&Math.abs(y)<CA){ if(Lv[1]%3!==1) continue; } if(Math.abs(Math.abs(y)-CA)<0.45&&Math.abs(x)<CL/2+0.3) continue; arrows.push([x,y]); } }); });
    CCache={key:key,segs:segs,arrows:arrows,list:list}; return CCache; }
  function insetCoil(x0,y0,w,h,s,on){ panel(x0,y0,w,h,'右手でにぎると'); const cx=x0+w/2+4, cy=y0+80;
    for(let i=0;i<4;i++){ const x=cx-30+i*20; ctx.strokeStyle='#92400e'; ctx.lineWidth=3; ctx.beginPath(); ctx.ellipse(x,cy,7,24,0,-Math.PI/2,Math.PI/2); ctx.stroke(); }
    if(on) arr(cx+(s>0?52:-52),cy,cx-(s>0?60:-60),cy,C.fld,4,7);
    for(let i=0;i<4;i++){ const x=cx-30+i*20; ctx.strokeStyle=C.coil; ctx.lineWidth=3; ctx.beginPath(); ctx.ellipse(x,cy,7,24,0,Math.PI/2,Math.PI*1.5); ctx.stroke(); if(on) head(x-7,cy+(s>0?-9:9),0,s>0?-1:1,C.cur,6); }
    if(on){ const nx=s>0?cx-66:cx+66, sx=s>0?cx+62:cx-62; dot(nx,cy-36,10,C.N); tx('N',nx,cy-31,13,'#fff','center',true); dot(sx,cy-36,10,C.S); tx('S',sx,cy-31,13,'#fff','center',true); }
    tx('4本の指＝電流の向き',x0+10,y0+h-42,11.5,C.cur,'left',true); tx('親指＝コイルの中の磁界',x0+10,y0+h-26,11.5,C.fld,'left',true); tx('（親指の側がN極）',x0+10,y0+h-10,11,C.sub,'left',true); }
  function insetStrong(x0,y0,w,h){ panel(x0,y0,w,h,'磁界を強くするには');
    ['・電流を大きくする','・コイルの巻き数をふやす','・鉄しんを入れる（電磁石）'].forEach((t,i)=>tx(t,x0+10,y0+44+i*21,11.5,C.ink,'left',true));
    tx('②電磁石の強さで確かめよう',x0+10,y0+h-12,10.5,C.sub,'left',true); }
  function sceneCoil(dt){ const P=PB, I=Iof(), s=dirI, cc=coilCache(P,I);
    wo+=Math.min(170,36*I)*s*dt;
    const nT=CN*28, hx=[]; for(let k=0;k<=nT;k++){ const t=2*Math.PI*CN*k/nT, z=CA*Math.sin(t), q=P.p(-CL/2+CL*t/(2*Math.PI*CN),-CA*Math.cos(t),z); hx.push([q[0],q[1],z]); }
    const zL=4.6, L2=P.p(-1.7,-CA,zL), L1=P.p(-CL/2,-CA,zL), R1=P.p(CL/2,-CA,zL), R2=P.p(1.7,-CA,zL);
    const path=[[L2[0],L2[1],9],[L1[0],L1[1],9]].concat(hx).concat([[R1[0],R1[1],9],[R2[0],R2[1],9]]);
    const dots=I>0?dotsOn(path,wo,22):[];
    for(let j=0;j<CN;j++){ ctx.strokeStyle='rgba(180,83,9,0.6)'; ctx.lineWidth=3; ctx.beginPath(); for(let k=j*28+14;k<=j*28+28;k++){ if(k===j*28+14) ctx.moveTo(hx[k][0],hx[k][1]); else ctx.lineTo(hx[k][0],hx[k][1]); } ctx.stroke(); }
    dots.forEach(d=>{ if(path[d[2]][2]<0) dot(d[0],d[1],3,C.cur); });
    drawBoard(P);
    ctx.save(); boardPath(P); ctx.clip(); ctx.strokeStyle='rgba(37,99,235,0.6)'; ctx.lineWidth=1.3; ctx.beginPath(); const sg=cc.segs; for(let i=0;i<sg.length;i+=4){ ctx.moveTo(sg[i],sg[i+1]); ctx.lineTo(sg[i+2],sg[i+3]); } ctx.stroke();
    cc.arrows.forEach(a=>{ const b=Bsum(cc.list,a[0],a[1]), q=P.p(a[0],a[1],0), v=P.v(b[0],b[1],0); head(q[0]+v[0]/Math.hypot(v[0],v[1])*2,q[1]+v[1]/Math.hypot(v[0],v[1])*2,v[0],v[1],'rgba(37,99,235,0.95)',4.2); }); ctx.restore();
    CPC.forEach((c,i)=>compassB(P,c[0],c[1],0.72,needle('c'+i,c[0],c[1],dt),false));
    compassB(P,probe[0],probe[1],1.1,needle('cp',probe[0],probe[1],dt),true);
    for(let j=0;j<CN;j++){ ctx.lineCap='round'; ctx.strokeStyle=C.coil; ctx.lineWidth=3.6; ctx.beginPath(); for(let k=j*28;k<=j*28+14;k++){ if(k===j*28) ctx.moveTo(hx[k][0],hx[k][1]); else ctx.lineTo(hx[k][0],hx[k][1]); } ctx.stroke();
      ctx.strokeStyle='rgba(253,230,138,0.55)'; ctx.lineWidth=1.1; ctx.stroke(); }
    ctx.strokeStyle=C.coil; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(hx[0][0],hx[0][1]); ctx.lineTo(L1[0],L1[1]); ctx.lineTo(L2[0],L2[1]); ctx.moveTo(R2[0],R2[1]); ctx.lineTo(R1[0],R1[1]); ctx.lineTo(hx[nT][0],hx[nT][1]); ctx.stroke();
    const pbat=P.p(0,-CA,zL); battery(pbat[0],pbat[1],Math.atan2(P.b,P.a),s>0?-1:1); tx('電源',pbat[0]+2,pbat[1]-36,11.5,C.sub,'center',true);
    dots.forEach(d=>{ if(path[d[2]][2]>=0) dot(d[0],d[1],3,C.cur); });
    if(I>0) for(let j=0;j<CN;j+=2){ const t=2*Math.PI*j+Math.PI/2, q=P.p(-CL/2+CL*t/(2*Math.PI*CN),0,CA), v=P.v(CL/(2*Math.PI*CN)*s,CA*s,0); head(q[0]+v[0]*0.08,q[1]+v[1]*0.08,v[0],v[1],C.cur,5); }
    if(I>0){ const nL=P.p(-CL/2-0.9,0,CA+1.1), nR=P.p(CL/2+0.9,0,CA+1.1), lN=s>0; dot(nL[0],nL[1],11,lN?C.N:C.S); tx(lN?'N':'S',nL[0],nL[1]+5,14,'#fff','center',true); dot(nR[0],nR[1],11,lN?C.S:C.N); tx(lN?'S':'N',nR[0],nR[1]+5,14,'#fff','center',true); }
    const pp=P.p(probe[0],probe[1],0); tag('指で動かせる方位磁針',pp[0],pp[1]+31,11,'#a16207','center');
    tx('コイルのまわりの磁界',14,24,15,C.ink,'left',true);
    tx('電流 '+fmt(I)+' A　'+(I>0?(s>0?'左のはしがN極（棒磁石と同じ形の磁界）':'右のはしがN極（棒磁石と同じ形の磁界）'):'電流が流れていない'),14,44,12.5,C.sub,'left');
    insetCoil(472,10,158,192,s,I>0); insetStrong(472,210,158,150);
    legend([['電流（＋極→－極）',C.cur,'dot'],['磁力線（磁界の向き）',C.fld,'line'],['方位磁針は赤いほうがN極',C.sub]],388);
    tx('コイルの中では磁力線がほぼ平行（磁界が強く、向きがそろう）',14,410,11,C.sub,'left');
    tx('電源をタップすると電流の向きが反対になります',14,428,11,C.sub,'left'); }

  // =============== ② 電磁石の強さ（小5） ===============
  const M2={x0:110,x1:374,y:125,h:13,c0:168,c1:330};
  function nbat(){ return $('bat').value==='two'?2:1; }
  function clipN(N,I){ return Math.round((core?1:0.06)*0.0533*N*I); }
  const ANCH=(()=>{ const a=[]; [[-9,0.8],[-2,0.6],[5,0.42]].forEach(q=>a.push([M2.x0,M2.y+q[0],q[1]])); for(let i=0;i<7;i++) a.push([M2.x0+5+i*6.5,M2.y+M2.h,0.2-i*0.055]); return a; })();
  const PILE=(()=>{ const a=[]; let r=7; for(let i=0;i<26;i++){ r=(r*9301+49297)%233280; const u=r/233280; r=(r*9301+49297)%233280; const v=r/233280; a.push([30+u*112,368+v*12,u*6.28]); } return a; })();
  function clipShape(x,y,ang,col){ ctx.save(); ctx.translate(x,y); ctx.rotate(ang); ctx.strokeStyle=col||'#64748b'; ctx.lineWidth=1.5; rr(-3.6,0,7.2,16,3.6); ctx.stroke(); rr(-1.7,3.2,3.4,10,1.7); ctx.stroke(); ctx.restore(); }
  function cellH(cx,y,pr){ const L=84, h=28, x0=cx-L/2; ctx.fillStyle='#9ca3af'; if(pr) ctx.fillRect(x0+L,y-6,6,12); else ctx.fillRect(x0-6,y-6,6,12);
    const g=ctx.createLinearGradient(0,y-h/2,0,y+h/2); g.addColorStop(0,'#4b5563'); g.addColorStop(0.45,'#111827'); g.addColorStop(1,'#374151'); ctx.fillStyle=g; rr(x0,y-h/2,L,h,6); ctx.fill();
    ctx.fillStyle='#ca8a04'; if(pr) ctx.fillRect(x0+L-26,y-h/2,20,h); else ctx.fillRect(x0+6,y-h/2,20,h);
    tx('＋',pr?x0+L-16:x0+16,y+5,14,'#fff','center',true); tx('－',pr?x0+14:x0+L-14,y+5,14,'#fff','center',true); tx('1.5V',cx+(pr?-6:6),y+4,11,'#e5e7eb','center',true); }
  const M2B={x:176,y:310,w:220,h:40}, M2SW={x:396,y:282};
  function sceneMag(dt){ const N=+$('turns').value, nb=nbat(), I=1.5*nb, on=swOn, target=on?clipN(N,I):0, s=dirI, leftN=s>0;
    if(shown<0) shown=target; if(shown<target) shown=Math.min(target,shown+dt*40); else if(shown>target) shown=Math.max(target,shown-dt*90); const ns=Math.round(shown);
    tx('電磁石の強さをくらべよう',14,26,16,C.ink,'left',true);
    tx('まき数 '+N+'回・かん電池'+(nb===2?'2個（直列つなぎ）':'1個')+(core?'':'・鉄しんなし')+(on?'':'・スイッチ切'),14,47,12.5,C.sub,'left');
    // クリップの山
    ctx.fillStyle='#e2e8f0'; rr(20,358,134,30,6); ctx.fill(); PILE.forEach(p=>clipShape(p[0],p[1]-8,p[2],'#94a3b8')); tx('クリップの山',87,402,11,C.sub,'center',true);
    // 導線・回路
    const t=3+2.2*N/50, top=M2.y-M2.h-t, bot=M2.y+M2.h+t, LX=M2.c0+8, RXc=M2.c1-8, YB=M2B.y+M2B.h/2, XR=M2SW.x;
    ctx.strokeStyle='#475569'; ctx.lineWidth=2.4; ctx.lineJoin='round'; ctx.beginPath(); ctx.moveTo(LX,bot-2); ctx.lineTo(LX,YB); ctx.lineTo(XR,YB); ctx.lineTo(XR,196); ctx.lineTo(RXc,196); ctx.lineTo(RXc,bot-2); ctx.stroke();
    // あまった導線
    const extra=Math.round((300-N)/50); for(let i=0;i<extra;i++){ ctx.strokeStyle='#b45309'; ctx.lineWidth=1.6; ctx.beginPath(); ctx.ellipse(LX,222+i*5,15,6,0,0,7); ctx.stroke(); }
    if(extra>0){ tx('あまった導線',LX+22,228,11,'#92400e','left',true); tx('（切らずにまとめる）',LX+22,244,11,'#92400e','left',true); }
    // かん電池
    if(nb===1) cellH(M2B.x+M2B.w/2,YB,s>0); else { cellH(M2B.x+M2B.w/2-45,YB,s>0); cellH(M2B.x+M2B.w/2+45,YB,s>0); }
    tx('かん電池'+(nb===2?'2個（直列つなぎ）':'1個')+'　タップで向きを反対に',M2B.x+M2B.w/2,YB+32,11,C.sub,'center',true);
    // 電流計
    const ay=232; ctx.fillStyle='#fff'; ctx.strokeStyle='#0e7490'; ctx.lineWidth=2.4; ctx.beginPath(); ctx.arc(XR,ay,15,0,7); ctx.fill(); ctx.stroke(); tx('A',XR,ay+5,14,'#0e7490','center',true); tag(fmt(on?I:0)+' A',XR-22,ay+5,12,'#0e7490','right');
    tx('電流計',XR+20,ay+5,11,C.sub,'left',true);
    // スイッチ
    const sy=M2SW.y; ctx.fillStyle=C.bg; ctx.fillRect(XR-6,sy-16,12,32); dot(XR,sy-14,3.5,'#334155'); dot(XR,sy+14,3.5,'#334155'); ctx.strokeStyle='#334155'; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(XR,sy+14); ctx.lineTo(on?XR:XR+17,sy-12); ctx.stroke(); tx('スイッチ',XR+(on?12:24),sy+5,11,C.sub,'left',true);
    // 鉄しん
    if(core){ const g=ctx.createLinearGradient(0,M2.y-M2.h,0,M2.y+M2.h); g.addColorStop(0,'#e5e7eb'); g.addColorStop(0.5,'#9ca3af'); g.addColorStop(1,'#6b7280'); ctx.fillStyle=g; rr(M2.x0,M2.y-M2.h,M2.x1-M2.x0,2*M2.h,4); ctx.fill(); ctx.strokeStyle='#4b5563'; ctx.lineWidth=1.2; ctx.stroke(); tx('鉄しん',(M2.c1+M2.x1)/2,M2.y+4,10.5,'#1f2937','center',true); }
    else { ctx.setLineDash([5,4]); ctx.strokeStyle='#9ca3af'; ctx.lineWidth=1.2; rr(M2.x0,M2.y-M2.h,M2.x1-M2.x0,2*M2.h,4); ctx.stroke(); ctx.setLineDash([]); tx('なし',(M2.c1+M2.x1)/2,M2.y+4,10.5,C.sub,'center',true); }
    // コイル
    const g2=ctx.createLinearGradient(0,top,0,bot); g2.addColorStop(0,'#f59e0b'); g2.addColorStop(0.5,'#b45309'); g2.addColorStop(1,'#78350f'); ctx.fillStyle=g2; rr(M2.c0,top,M2.c1-M2.c0,bot-top,5); ctx.fill();
    ctx.strokeStyle='rgba(69,26,3,0.5)'; ctx.lineWidth=1; const nl=Math.round(Math.min(64,12+N/5)); for(let i=0;i<=nl;i++){ const x=M2.c0+3+(M2.c1-M2.c0-9)*i/nl; ctx.beginPath(); ctx.moveTo(x,top+1); ctx.lineTo(x+3,bot-1); ctx.stroke(); }
    tx(N+'回まき',(M2.c0+M2.c1)/2,top-7,12,'#92400e','center',true);
    // 極
    if(on){ const lc=leftN?C.N:C.S, rc=leftN?C.S:C.N; dot(M2.x0+28,M2.y-M2.h-18,11,lc); tx(leftN?'N':'S',M2.x0+28,M2.y-M2.h-13,13,'#fff','center',true); dot(M2.x1-22,M2.y-M2.h-18,11,rc); tx(leftN?'S':'N',M2.x1-22,M2.y-M2.h-13,13,'#fff','center',true); }
    // 方位磁針
    const cxp=440, cyp=M2.y; const tg=on?(leftN?Math.PI:0):-Math.PI/2; let a=nd.m2; if(a==null) a=tg; let d=tg-a; d=Math.atan2(Math.sin(d),Math.cos(d)); a+=d*Math.min(1,dt*8); nd.m2=a;
    ctx.fillStyle='#fff'; ctx.strokeStyle='#64748b'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.arc(cxp,cyp,22,0,7); ctx.fill(); ctx.stroke();
    ctx.save(); ctx.translate(cxp,cyp); ctx.rotate(a); ctx.fillStyle=C.N; ctx.beginPath(); ctx.moveTo(18,0); ctx.lineTo(0,5); ctx.lineTo(0,-5); ctx.closePath(); ctx.fill(); ctx.fillStyle='#cbd5e1'; ctx.beginPath(); ctx.moveTo(-18,0); ctx.lineTo(0,5); ctx.lineTo(0,-5); ctx.closePath(); ctx.fill(); ctx.restore(); dot(cxp,cyp,2.5,'#334155');
    tx('方位磁針',cxp,cyp+38,11,C.sub,'center',true); tx('北↑',cxp+26,cyp-16,10.5,'#a8a29e','left',true);
    // クリップ（ついている）
    for(let n=0;n<ns;n++){ const c=ANCH[n%ANCH.length], k=Math.floor(n/ANCH.length), th=c[2]+0.05*k; const x=c[0]-Math.sin(th)*15*k, y=c[1]+Math.cos(th)*15*k; clipShape(x,y,th,'#475569'); }
    if(on) tag('クリップ '+ns+'こ',84,248,13,'#0f172a','center','#94a3b8'); else tag('電流が流れていない',84,248,12,C.sub,'center');
    // 記録表
    const tx0=476, ty0=168; panel(tx0,ty0,156,200,'けっかの記録');
    tx('まき数',tx0+12,ty0+42,11,C.sub,'left',true); tx('電池',tx0+66,ty0+42,11,C.sub,'left',true); tx('クリップ',tx0+146,ty0+42,11,C.sub,'right',true);
    ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(tx0+8,ty0+48); ctx.lineTo(tx0+148,ty0+48); ctx.stroke();
    if(!recs.length){ tx('「📋 結果を記録」を',tx0+78,ty0+80,11,C.sub,'center'); tx('押すと、ここに表が',tx0+78,ty0+97,11,C.sub,'center'); tx('できます',tx0+78,ty0+114,11,C.sub,'center'); }
    recs.forEach((r,i)=>{ const y=ty0+68+i*20, b=i===recs.length-1; tx(r[0]+'回',tx0+12,y,12,C.ink,'left',b); tx((r[1]===2?'2個':'1個')+(r[3]?'':'＊'),tx0+66,y,12,C.ink,'left',b); tx(r[2]+'こ',tx0+146,y,12,C.ink,'right',true); });
    if(recs.some(r=>!r[3])) tx('＊鉄しんなし',tx0+12,ty0+192,10,C.sub,'left');
    tx('変える条件は1つだけ。ほかの条件（導線の長さなど）はそろえよう',14,420,11.5,C.sub,'left',true);
    tx('電流の向きを反対にすると、N極とS極が入れかわります',14,436,11.5,C.sub,'left'); }

  // =============== ③ 磁界の中の電流が受ける力 ===============
  const PS=mk(236,282,16,0.55,0.38), LP=10.4, WY=2.4, PX=1.2;
  const NC=['#ef4444','#b91c1c','#f87171'], SC=['#3b82f6','#1d4ed8','#60a5fa'];
  function insetFleming(x0,y0,w,h,P,sc,mu,sig){ panel(x0,y0,w,h,'フレミングの左手の法則'); const ox=x0+w/2-4, oy=y0+104;
    [[P.v(sig,0,0),C.frc,'親指','力'],[P.v(0,0,-mu),C.fld,'人差し指','磁界'],[P.v(0,sc,0),C.cur,'中指','電流']].forEach(v=>{ const l=Math.hypot(v[0][0],v[0][1]), ux=v[0][0]/l, uy=v[0][1]/l, L=40;
      ctx.strokeStyle=v[1]; ctx.globalAlpha=0.22; ctx.lineWidth=13; ctx.lineCap='round'; ctx.beginPath(); ctx.moveTo(ox,oy); ctx.lineTo(ox+ux*L,oy+uy*L); ctx.stroke(); ctx.globalAlpha=1; arr(ox,oy,ox+ux*(L+6),oy+uy*(L+6),v[1],3.5,6);
      const lx=clamp(ox+ux*(L+26),x0+30,x0+w-30), ly=clamp(oy+uy*(L+24),y0+38,y0+h-36); tx(v[2],lx,ly-3,10.5,v[1],'center',true); tx(v[3],lx,ly+11,12,v[1],'center',true); });
    dot(ox,oy,4,'#334155'); tx('中指から順に「電・磁・力」',x0+w/2,y0+h-10,10.5,C.sub,'center',true); }
  function insetTable(x0,y0,w,h,sc,mu){ panel(x0,y0,w,h,'向きを変えると');
    tx('電流',x0+14,y0+42,11,C.cur,'left',true); tx('磁界',x0+62,y0+42,11,C.fld,'left',true); tx('力',x0+118,y0+42,11,C.frc,'left',true);
    [[1,1],[-1,1],[1,-1],[-1,-1]].forEach((r,i)=>{ const y=y0+64+i*21, on=r[0]===sc&&r[1]===mu, f=-r[0]*r[1]; if(on){ ctx.fillStyle='#ecfdf5'; rr(x0+6,y-14,w-12,20,5); ctx.fill(); }
      tx(r[0]>0?'もと':'反対',x0+14,y,11.5,C.ink,'left',on); tx(r[1]>0?'もと':'反対',x0+62,y,11.5,C.ink,'left',on); tx(f<0?'外側':'内側',x0+112,y,11.5,C.frc,'left',true); });
    tx('両方反対にすると力は同じ向き',x0+w/2,y0+h-10,10.5,C.sub,'center',true); }
  function sceneSwing(dt){ const P=PS, I=Iof(), sc=dirI, mu=magUp, sig=-sc*mu, tgt=Math.atan(0.05*I)*sig;
    if(swingInit){ phi=tgt; phiV=0; swingInit=false; }
    for(let k=0;k<4;k++){ const h=dt/4; phiV+=(-100*(phi-tgt)-2.4*phiV)*h; phi+=phiV*h; }
    const xb=PX+LP*Math.sin(phi), zb=LP*(1-Math.cos(phi)), top=mu>0?NC:SC, bot=mu>0?SC:NC, G=['#94a3b8','#64748b','#cbd5e1'];
    so+=Math.min(150,30*I)*sc*dt;
    box(P,-6,8,-4,4,-3.4,-2.8,'#e9d5b0','#d4bc91','#f3e6cc');
    box(P,-4.75,-4.25,-0.25,0.25,-2.8,11.2,G[0],G[1],G[2]); box(P,-4.75,PX+0.25,-0.25,0.25,10.8,11.2,G[0],G[1],G[2]); box(P,PX-0.25,PX+0.25,-2.9,2.9,10.4,10.8,G[0],G[1],G[2]);
    line3(P,[PX,WY,LP],[xb,WY,zb],C.coil,3.2);
    box(P,-1.6,4.8,-1.5,1.5,-2.8,-1.2,bot[0],bot[1],bot[2]);
    [[0.0,-0.8],[1.8,-0.8],[0.0,0.8],[1.8,0.8],[3.4,0]].forEach(q=>arr3(P,[q[0],q[1],mu*1.05],[q[0],q[1],-mu*1.05],C.fld,1.8,4));
    line3(P,[xb,-WY,zb],[xb,WY,zb],C.coil,3.6);
    const path=[[PX,-WY,LP],[xb,-WY,zb],[xb,WY,zb],[PX,WY,LP]].map(q=>P.p(q[0],q[1],q[2])), dots=I>0?dotsOn(path,so,20):[];
    dots.forEach(d=>{ if(d[2]>0) dot(d[0],d[1],3,C.cur); });
    box(P,-1.6,4.8,-1.5,1.5,1.2,2.8,top[0],top[1],top[2]);
    line3(P,[PX,-WY,LP],[xb,-WY,zb],C.coil,3.2);
    dots.forEach(d=>{ if(d[2]===0) dot(d[0],d[1],3,C.cur); });
    box(P,4.8,6.4,-1.5,1.5,-2.8,2.8,'#9ca3af','#6b7280','#d1d5db');
    const lt=P.p(3.0,-1.5,2.0), lb=P.p(3.0,-1.5,-2.0); tx(mu>0?'N':'S',lt[0],lt[1]+6,16,'#fff','center',true); tx(mu>0?'S':'N',lb[0],lb[1]+6,16,'#fff','center',true);
    // 電源
    const hf=P.p(PX,-WY,LP), hb=P.p(PX,WY,LP), bx=(hf[0]+hb[0])/2, by=72;
    ctx.strokeStyle=C.lead; ctx.lineWidth=2.2; ctx.beginPath(); ctx.moveTo(hf[0],hf[1]); ctx.lineTo(hf[0],by); ctx.lineTo(bx-10,by); ctx.moveTo(bx+10,by); ctx.lineTo(hb[0],by); ctx.lineTo(hb[0],hb[1]); ctx.stroke();
    dot(hf[0],hf[1],3.5,'#334155'); dot(hb[0],hb[1],3.5,'#334155'); battery(bx,by,0,sc>0?-1:1); tx('電源',hb[0]+12,by+5,11.5,C.sub,'left',true);
    // 矢印
    if(I>0){ arr3(P,[xb,-1.3*sc,zb-0.6],[xb,1.3*sc,zb-0.6],C.cur,3.4,6); const ct=P.p(xb,-1.7*sc,zb-1.0); tag('電流',ct[0],ct[1]+14,12,C.cur,'center');
      const L=1.2+0.5*I; arr3(P,[xb,0,zb],[xb+sig*L,0,zb],C.frc,5,8); const ft=P.p(xb+sig*(L+0.5),0,zb+0.9); tag('力',ft[0],ft[1],13,C.frc,'center'); }
    const fl=P.p(6.4,-1.5,0); tag('磁界（N→S）',fl[0]+10,fl[1]+5,11.5,C.fld,'left');
    const op=P.p(-1.6,-1.5,-3.2), ip=P.p(4.6,-1.5,-3.2); tx('← 外側',op[0]-6,op[1]+20,11,C.sub,'center',true); tx('内側 →',ip[0]-10,ip[1]+20,11,C.sub,'center',true);
    tx('磁界の中の電流が受ける力（ぶらんこ実験）',14,24,15,C.ink,'left',true);
    tx(I>0?'電流 '+fmt(I)+' A　導線は磁石の'+(sig<0?'外側':'内側')+'へ動く':'電流が0なので力ははたらかない',14,44,12.5,C.sub,'left');
    insetFleming(472,10,158,200,P,sc,mu,sig); insetTable(472,218,158,150,sc,mu);
    legend([['電流',C.cur,'dot'],['磁界（N→S）',C.fld,'line'],['力',C.frc,'line']],412);
    tx('U字形磁石をタップするとN極とS極が入れかわります',14,432,11,C.sub,'left'); }
  // モーター
  const PM=mk(222,208,20,-0.55,0.34);
  function sym(x,y,d){ ctx.fillStyle='#fff'; ctx.strokeStyle=C.cur; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(x,y,8,0,7); ctx.fill(); ctx.stroke(); if(d>0){ ctx.beginPath(); ctx.moveTo(x-4.5,y-4.5); ctx.lineTo(x+4.5,y+4.5); ctx.moveTo(x+4.5,y-4.5); ctx.lineTo(x-4.5,y+4.5); ctx.stroke(); } else dot(x,y,2.6,C.cur); }
  function insetFront(x0,y0,w,h,mu,Px,Pz,pDir,I,wd){ panel(x0,y0,w,h,'手前から見ると'); const cx=x0+w/2, cy=y0+100, R=40;
    ctx.fillStyle=mu>0?'#ef4444':'#3b82f6'; rr(x0+10,cy-38,20,76,4); ctx.fill(); ctx.fillStyle=mu>0?'#3b82f6':'#ef4444'; rr(x0+w-30,cy-38,20,76,4); ctx.fill();
    tx(mu>0?'N':'S',x0+20,cy+5,14,'#fff','center',true); tx(mu>0?'S':'N',x0+w-20,cy+5,14,'#fff','center',true);
    for(let k=-2;k<=2;k++){ const y=cy+k*15; ctx.strokeStyle='rgba(37,99,235,0.28)'; ctx.lineWidth=1.2; ctx.beginPath(); ctx.moveTo(x0+32,y); ctx.lineTo(x0+w-32,y); ctx.stroke(); }
    ctx.strokeStyle='rgba(124,58,237,0.35)'; ctx.setLineDash([3,4]); ctx.beginPath(); ctx.arc(cx,cy,R,0,7); ctx.stroke(); ctx.setLineDash([]);
    const px=cx+R*Px/2.5, py=cy-R*Pz/2.5, qx=cx-R*Px/2.5, qy=cy+R*Pz/2.5;
    ctx.strokeStyle=C.coil; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(px,py); ctx.lineTo(qx,qy); ctx.stroke(); dot(cx,cy,3,'#64748b');
    if(I>0){ const L=12+3.2*I; arr(px,py,px,py+pDir*mu*L,C.frc,3,5); arr(qx,qy,qx,qy-pDir*mu*L,C.frc,3,5); sym(px,py,pDir); sym(qx,qy,-pDir); } else { dot(px,py,6,C.coil); dot(qx,qy,6,C.coil); }
    if(Math.abs(wd)>0.3){ const Rr=R+12; ctx.strokeStyle='#7c3aed'; ctx.lineWidth=2.4; ctx.beginPath(); ctx.arc(cx,cy,Rr,-2.2,-0.95); ctx.stroke();
      if(wd<0){ const e=-0.95; head(cx+Math.cos(e)*Rr+Math.cos(e+1.57)*4,cy+Math.sin(e)*Rr+Math.sin(e+1.57)*4,-Math.sin(e),Math.cos(e),'#7c3aed',5); } else { const e=-2.2; head(cx+Math.cos(e)*Rr-Math.cos(e+1.57)*4,cy+Math.sin(e)*Rr-Math.sin(e+1.57)*4,Math.sin(e),-Math.cos(e),'#7c3aed',5); } }
    tx('×＝電流が奥へ　・＝手前へ',x0+w/2,y0+h-10,10.5,C.sub,'center',true); }
  function sceneMotor(dt){ const P=PM, I=Iof(), sc=dirI, mu=magUp, T0=3.95, cd=1.2;
    if(motorInit){ motorInit=false; omega=(I>0&&comm)?-sc*mu*(2/Math.PI)*T0*I/cd:0; }
    for(let k=0;k<4;k++){ const h=dt/4, cs=Math.cos(alpha); let tau=comm?-sc*mu*T0*I*Math.abs(cs):-sc*mu*T0*I*cs*pSide; tau-=cd*omega; if(Math.abs(omega)>0.02) tau-=0.25*Math.sign(omega); omega+=tau*h; alpha+=omega*h; }
    if(comm&&I>0&&Math.abs(omega)<0.05&&Math.abs(Math.cos(alpha))<0.04) alpha+=-sc*mu*0.06;
    alpha=((alpha%(2*Math.PI))+2*Math.PI)%(2*Math.PI);
    const r=2.9, YL=3.0, Px=r*Math.cos(alpha), Pz=r*Math.sin(alpha), Qx=-Px, Qz=-Pz, pDir=comm?(Px>=0?1:-1)*sc:pSide*sc, Lc=mu>0?NC:SC, Rc=mu>0?SC:NC;
    so+=Math.min(150,30*I)*pDir*dt;
    box(P,4.2,6.0,-3.2,3.2,-3.2,3.2,Rc[0],Rc[1],Rc[2]);
    [2.8,0].forEach(y=>[-2.4,-1.2,0,1.2,2.4].forEach(z=>{ line3(P,[-4.2,y,z],[4.2,y,z],'rgba(37,99,235,0.3)',1.3); const a=P.p(mu*3.2,y,z), v=P.v(mu,0,0); head(a[0],a[1],v[0],v[1],'rgba(37,99,235,0.65)',4); }));
    line3(P,[0,-6.0,0],[0,4.4,0],'#64748b',3.5);
    box(P,-6.0,-4.2,-3.2,3.2,-3.2,3.2,Lc[0],Lc[1],Lc[2]);
    const ln=P.p(-5.1,-3.2,0.2), rn=P.p(5.1,-3.2,0.2); tx(mu>0?'N':'S',ln[0],ln[1]+8,22,'#fff','center',true); tx(mu>0?'S':'N',rn[0],rn[1]+8,22,'#fff','center',true);
    // 回る向き（奥の矢印）
    const turn=Math.abs(omega)>0.3?Math.sign(omega):((comm&&I>0)?-sc*mu:0);
    if(turn){ const R3=3.9, pts=[]; for(let i=0;i<=20;i++){ const t=0.85+1.45*i/20; pts.push([R3*Math.cos(t),3.4,R3*Math.sin(t)]); } ctx.strokeStyle='#7c3aed'; ctx.lineWidth=2.6; poly(P,pts); ctx.stroke();
      const te=turn<0?0.85:2.3, q=P.p(R3*Math.cos(te),3.4,R3*Math.sin(te)), v=turn<0?P.v(Math.sin(te),0,-Math.cos(te)):P.v(-Math.sin(te),0,Math.cos(te)); head(q[0]+v[0]*0.2,q[1]+v[1]*0.2,v[0],v[1],'#7c3aed',6);
      const lq=P.p(0,3.4,R3+0.8); tx('回る向き',lq[0],lq[1],11.5,'#7c3aed','center',true); }
    const A=[Px,-YL,Pz], B=[Px,YL,Pz], Cc=[Qx,YL,Qz], D=[Qx,-YL,Qz];
    ctx.lineJoin='round'; ctx.strokeStyle=C.coil; ctx.lineWidth=5; poly(P,[A,B,Cc,D]); ctx.stroke(); ctx.strokeStyle='rgba(253,230,138,0.5)'; ctx.lineWidth=1.4; ctx.stroke();
    const ca=0.95, cyA=comm?-4.9:-4.6, cyD=comm?-4.9:-5.4;
    [[A,Px,Pz,cyA,alpha],[D,Qx,Qz,cyD,alpha+Math.PI]].forEach(c=>{ const m=[c[1]*0.35,-YL-0.6,c[2]*0.35]; line3(P,c[0],m,C.coil,3.4); line3(P,m,[ca*Math.cos(c[4]),c[3],ca*Math.sin(c[4])],C.coil,3.4); });
    // 整流子（またはリング）
    const ring=(y0,y1,a0,a1,col,colT)=>{ const n=18, pts=[]; for(let i=0;i<=n;i++){ const t=a0+(a1-a0)*i/n; pts.push([ca*Math.cos(t),y1,ca*Math.sin(t)]); } for(let i=n;i>=0;i--){ const t=a0+(a1-a0)*i/n; pts.push([ca*Math.cos(t),y0,ca*Math.sin(t)]); } face(P,pts,col);
      const cap=[[0,y1,0]]; for(let i=0;i<=n;i++){ const t=a0+(a1-a0)*i/n; cap.push([ca*Math.cos(t),y1,ca*Math.sin(t)]); } face(P,cap,colT); };
    if(comm){ ring(-4.3,-5.5,alpha+Math.PI+0.1,alpha+2*Math.PI-0.1,'#c2410c','#fb923c'); ring(-4.3,-5.5,alpha+0.1,alpha+Math.PI-0.1,'#b45309','#fbbf24'); }
    else { ring(-4.35,-4.85,0,2*Math.PI,'#b45309','#fbbf24'); ring(-5.15,-5.65,0,2*Math.PI,'#c2410c','#fb923c'); }
    line3(P,[0,-5.6,0],[0,-6.2,0],'#64748b',3.5);
    const yR=comm?-4.9:-4.6, yLb=comm?-4.9:-5.4;
    box(P,0.97,1.75,yR-0.3,yR+0.3,-0.36,0.36,'#374151','#1f2937','#4b5563'); box(P,-1.75,-0.97,yLb-0.3,yLb+0.3,-0.36,0.36,'#374151','#1f2937','#4b5563');
    const zB=-5.0, yB=-5.1; ctx.strokeStyle=C.lead; ctx.lineWidth=2.2; poly(P,[[1.75,yR,0],[2.6,yR,0],[2.6,yB,zB],[1.4,yB,zB]]); ctx.stroke(); poly(P,[[-1.75,yLb,0],[-2.6,yLb,0],[-2.6,yB,zB],[-1.4,yB,zB]]); ctx.stroke();
    const pb=P.p(0,yB,zB); battery(pb[0],pb[1],Math.atan2(P.b,P.a),sc>0?1:-1); tx('電源（タップで電流を反対に）',pb[0],pb[1]+32,11,C.sub,'center',true);
    if(I>0){ const pts=[A,B,Cc,D].map(q=>P.p(q[0],q[1],q[2])); dotsOn(pts,so,18).forEach(d=>dot(d[0],d[1],3,C.cur));
      arr3(P,[Px,-1.5-0.8*pDir,Pz],[Px,-1.5+0.8*pDir,Pz],C.cur,3.2,5.5); arr3(P,[Qx,-1.5+0.8*pDir,Qz],[Qx,-1.5-0.8*pDir,Qz],C.cur,3.2,5.5);
      const L=1.1+0.34*I; arr3(P,[Px,0.6,Pz],[Px,0.6,Pz-pDir*mu*L],C.frc,5,7); arr3(P,[Qx,0.6,Qz],[Qx,0.6,Qz+pDir*mu*L],C.frc,5,7);
      const up=-pDir*mu>0, fq=up?P.p(Px,0.6,Pz+L+0.4):P.p(Qx,0.6,Qz+L+0.4); tag('力',fq[0]+12,fq[1]+5,12,C.frc,'left'); }
    [['A',A],['B',B],['C',Cc],['D',D]].forEach(l=>{ const q=P.p(l[1][0]*1.22,l[1][1]+(l[1][1]>0?0.5:-0.4),l[1][2]*1.22); tx(l[0],q[0],q[1]+4,12,'#92400e','center',true); });
    const cl=P.p(0,-5.5,-1.1); tag(comm?'整流子':'リング（整流子なし）',cl[0]+22,cl[1]+20,11.5,'#92400e','left'); const bl=P.p(1.75,yR,0.4); tag('ブラシ',bl[0]+10,bl[1]-4,11.5,'#374151','left');
    const rps=Math.abs(omega)/(2*Math.PI);
    tx('モーターが回るしくみ（整流子とブラシ）',14,24,15,C.ink,'left',true);
    tx('電流 '+fmt(I)+' A　'+(rps<0.02?'止まっている':'手前から見て'+(omega<0?'時計回り':'反時計回り')+'・毎秒 '+fmt(rps,2)+' 回転'),14,44,12.5,C.sub,'left');
    insetFront(472,10,158,192,mu,Px,Pz,pDir,I,omega);
    panel(472,210,158,150,'整流子のはたらき');
    (comm?['コイルが半回転するごとに','整流子とブラシが','コイルに流れる電流の','向きを切りかえる。','→ いつも同じ向きに回る']:['整流子がないと、','半回転すると力が','反対向きになり、','コイルは行ったり来たり','して止まってしまう']).forEach((t,i)=>tx(t,484,246+i*21,11.5,i===4?'#7c3aed':C.ink,'left',i===4));
    legend([['電流',C.cur,'dot'],['磁界（N→S）',C.fld,'line'],['力',C.frc,'line']],412);
    tx('「整流子をはずす」で、整流子がないとどうなるか比べられます',14,432,11,C.sub,'left'); }

  // =============== ④ 電磁誘導・発電機 ===============
  const CX4=432, CY4=190, CL4=170, CR4=44, NT4=11, MXMIN=95, MXMAX=405, XIN=392, XOUT=118, GX4=212;
  function flux(X,fl){ const a=38, d=68, xN=X+d*fl, xS=X-d*fl; let L=0; for(let j=0;j<NT4;j++){ const xj=CX4-CL4/2+CL4*(j+0.5)/NT4, zN=xj-xN, zS=xj-xS; L+=0.5*(-zN/Math.sqrt(zN*zN+a*a)+zS/Math.sqrt(zS*zS+a*a)); } return L; }
  const G4=(()=>{ let mx=0; for(let X=MXMIN; X<MXMAX; X+=1) mx=Math.max(mx,Math.abs(flux(X+0.5,1)-flux(X-0.5,1))); return 6/(180*mx); })();
  function galvo(x,y,w,h,val){ panel(x,y,w,h,''); tx('検流計',x+9,y+17,11.5,C.ink,'left',true); const cx=x+w/2, cy=y+h-12, R=h-34;
    ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1.4; ctx.beginPath(); ctx.arc(cx,cy,R,-Math.PI/2-0.9,-Math.PI/2+0.9); ctx.stroke();
    for(let k=-10;k<=10;k+=2){ const t=-Math.PI/2+k*0.09, l=k%10===0?9:5; ctx.beginPath(); ctx.moveTo(cx+Math.cos(t)*(R-l),cy+Math.sin(t)*(R-l)); ctx.lineTo(cx+Math.cos(t)*R,cy+Math.sin(t)*R); ctx.stroke(); }
    tx('0',cx,cy-R-4,10,C.sub,'center'); tx('左',cx-R*0.82,cy-R*0.45,10,C.sub,'center',true); tx('右',cx+R*0.82,cy-R*0.45,10,C.sub,'center',true);
    const t=-Math.PI/2+clamp(val,-11,11)*0.09; ctx.strokeStyle='#dc2626'; ctx.lineWidth=2.6; ctx.lineCap='round'; ctx.beginPath(); ctx.moveTo(cx,cy); ctx.lineTo(cx+Math.cos(t)*(R-4),cy+Math.sin(t)*(R-4)); ctx.stroke(); dot(cx,cy,4,'#334155'); }
  function coilBack(){ const x0=CX4-CL4/2; ctx.fillStyle='rgba(180,83,9,0.08)'; ctx.fillRect(x0,CY4-CR4,CL4,2*CR4);
    for(let j=0;j<NT4;j++){ const xj=x0+CL4*(j+0.5)/NT4; ctx.strokeStyle='#92400e'; ctx.lineWidth=3; ctx.beginPath(); ctx.ellipse(xj,CY4,10,CR4,0,-Math.PI/2,Math.PI/2); ctx.stroke(); } }
  function coilFront(cur){ const x0=CX4-CL4/2; for(let j=0;j<NT4;j++){ const xj=x0+CL4*(j+0.5)/NT4; ctx.strokeStyle=C.coil; ctx.lineWidth=3.4; ctx.beginPath(); ctx.ellipse(xj,CY4,10,CR4,0,Math.PI/2,Math.PI*1.5); ctx.stroke(); ctx.strokeStyle='rgba(253,230,138,0.5)'; ctx.lineWidth=1; ctx.stroke(); }
    if(Math.abs(cur)>0.15) for(let j=1;j<NT4;j+=3){ const xj=x0+CL4*(j+0.5)/NT4; head(xj-10,CY4+(cur>0?-8:8),0,cur>0?-1:1,C.cur,5); }
    tx('コイル',CX4,CY4+CR4+18,11.5,'#92400e','center',true); }
  function leads4(cur,dt){ const x0=CX4-CL4/2, x1=CX4+CL4/2, yt=CY4-CR4+4; so+=clamp(cur,-9,9)*22*dt;
    const pts=[[x1,yt],[x1,122],[CX4+38,122],[CX4+38,106],[CX4-38,106],[CX4-38,122],[x0,122],[x0,yt]];
    ctx.strokeStyle=C.lead; ctx.lineWidth=2.2; ctx.lineJoin='round'; ctx.beginPath(); pts.forEach((p,i)=>{ if(i) ctx.lineTo(p[0],p[1]); else ctx.moveTo(p[0],p[1]); }); ctx.stroke();
    if(Math.abs(cur)>0.15) dotsOn(pts,so,22).forEach(d=>{ if(d[2]!==3) dot(d[0],d[1],3,C.cur); }); }
  function drawBar(X,Y,fl){ const L=160, h=34, x0=X-L/2; const nR=fl>0; ctx.fillStyle='rgba(15,23,42,0.12)'; rr(x0+4,Y-h/2+6,L,h,4); ctx.fill();
    ctx.fillStyle=nR?'#ef4444':'#3b82f6'; ctx.fillRect(X,Y-h/2,L/2,h); ctx.fillStyle=nR?'#3b82f6':'#ef4444'; ctx.fillRect(x0,Y-h/2,L/2,h);
    ctx.fillStyle='rgba(255,255,255,0.25)'; ctx.fillRect(x0,Y-h/2,L,7); ctx.strokeStyle='rgba(15,23,42,0.4)'; ctx.lineWidth=1; ctx.strokeRect(x0,Y-h/2,L,h);
    tx(nR?'N':'S',X+L/2-16,Y+7,18,'#fff','center',true); tx(nR?'S':'N',x0+16,Y+7,18,'#fff','center',true); }
  function chart(x,y,w,h,span,gen){ panel(x,y,w,h,''); const top=y+32, bot=y+h-12, zy=(top+bot)/2, sc=(bot-top)/20, x1=x+w-12, x0=x+50;
    tx(gen?'電流のようす（オシロスコープ）':'誘導電流の変化（検流計の針のふれ）',x+10,y+19,11.5,C.ink,'left',true); tx('時間 →（最近'+span+'秒）',x1,y+19,10.5,C.sub,'right');
    ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; [-10,-5,5,10].forEach(v=>{ ctx.beginPath(); ctx.moveTo(x0,zy-v*sc); ctx.lineTo(x1,zy-v*sc); ctx.stroke(); });
    ctx.strokeStyle='#94a3b8'; ctx.beginPath(); ctx.moveTo(x0,zy); ctx.lineTo(x1,zy); ctx.stroke(); tx('右(＋)',x0-4,zy-10*sc+4,10,C.sub,'right'); tx('0',x0-4,zy+4,10,C.sub,'right'); tx('左(－)',x0-4,zy+10*sc+4,10,C.sub,'right');
    if(gen){ ctx.setLineDash([6,5]); ctx.strokeStyle='#94a3b8'; ctx.beginPath(); ctx.moveTo(x0,zy-6*sc); ctx.lineTo(x1,zy-6*sc); ctx.stroke(); ctx.setLineDash([]); tag('直流（かん電池）：向きは一定',x1-4,zy-6*sc-4,10.5,C.sub,'right'); }
    ctx.save(); ctx.beginPath(); ctx.rect(x0,top-6,x1-x0,bot-top+12); ctx.clip(); ctx.strokeStyle=C.cur; ctx.lineWidth=2.2; ctx.beginPath(); let st=false;
    hist.forEach(p=>{ const X=x1-(tNow-p[0])/span*(x1-x0), Y=zy-clamp(p[1],-11,11)*sc; if(st) ctx.lineTo(X,Y); else { ctx.moveTo(X,Y); st=true; } }); ctx.stroke(); ctx.restore();
    if(!gen&&hist.every(p=>Math.abs(p[1])<0.05)) tx('「➡ 磁石を入れる」「⬅ 磁石を出す」を押すか、磁石を指で動かしてください',x+w/2,zy+20,11,C.sub,'center'); }
  function needleStep(dt){ for(let k=0;k<3;k++){ const h=dt/3; ndlV+=(-625*(ndl-iNow)-35*ndlV)*h; ndl+=ndlV*h; } hist.push([tNow,iNow]); while(hist.length&&tNow-hist[0][0]>8.5) hist.shift(); }
  function moveWord(){ if(Math.abs(vS)<6) return '止まっている'; return (magN>0?'N極':'S極')+(vS>0?'を近づけている':'を遠ざけている'); }
  function sceneMove(dt){ const v=60*(+$('spd').value);
    if(drag!=='mag'&&mTarget!=null){ const d=mTarget-mX; if(Math.abs(d)<=v*dt){ mX=mTarget; mTarget=null; } else mX+=Math.sign(d)*v*dt; }
    const Ln=flux(mX,magN); let iRaw=0; if(Lprev!=null&&dt>0) iRaw=G4*(Ln-Lprev)/dt; Lprev=Ln;
    vS+=((dt>0?(mX-mPrev)/dt:0)-vS)*Math.min(1,dt*12); mPrev=mX; iNow+=(iRaw-iNow)*Math.min(1,dt*30); if(Math.abs(iNow)<0.02) iNow=0; needleStep(dt); peakAbs=Math.max(peakAbs,Math.abs(iNow));
    coilBack(); drawBar(mX,CY4,magN); coilFront(iNow); leads4(iNow,dt);
    galvo(CX4-75,8,150,98,ndl);
    if(Math.abs(iNow)>0.15){ const lN=iNow>0; dot(CX4-CL4/2-14,CY4-CR4-8,10,lN?C.N:C.S); tx(lN?'N':'S',CX4-CL4/2-14,CY4-CR4-3,13,'#fff','center',true); dot(CX4+CL4/2+14,CY4-CR4-8,10,lN?C.S:C.N); tx(lN?'S':'N',CX4+CL4/2+14,CY4-CR4-3,13,'#fff','center',true); }
    tag('↔ 磁石は指で動かせます',mX,CY4+38,11,'#a16207','center');
    panel(14,34,316,76,'');
    tx('磁石：'+moveWord(),26,55,12.5,C.ink,'left',true);
    tx('針：'+(Math.abs(ndl)<0.15?'0（電流は流れない）':(ndl>0?'右':'左')+'にふれる（'+fmt(Math.abs(ndl))+' 目もり）'),26,76,12.5,C.cur,'left',true);
    tx(Math.abs(iNow)>0.15?'コイルの左はしが'+(iNow>0?'N':'S')+'極になり、'+(vS>0?'近づく磁石をしりぞける':'遠ざかる磁石を引きとめる'):'コイルの中の磁界が変化したときだけ電流が流れる',26,97,11.5,C.sub,'left',true);
    tx('電磁誘導（磁石を出し入れする）',14,24,15,C.ink,'left',true);
    chart(14,262,616,140,8,false);
    legend([['誘導電流',C.cur,'dot'],['N極',C.N,'dot'],['S極',C.S,'dot']],428); }
  function sceneGen(dt){ const f=+$('rps').value;
    if(drag!=='rot'&&playing) theta+=2*Math.PI*f*dt;
    const w=dt>0?(theta-thPrev)/dt:0; thPrev=theta; wGen+=(w-wGen)*Math.min(1,dt*10); if(!playing&&drag!=='rot'&&Math.abs(wGen)<0.05) wGen=0;
    iNow=-3.6*(wGen/(2*Math.PI))*Math.sin(theta)*magN; needleStep(dt);
    coilBack();
    const L=132, h=30; ctx.save(); ctx.translate(GX4+0,CY4); ctx.rotate(-theta); ctx.fillStyle='rgba(15,23,42,0.12)'; ctx.fillRect(-L/2+4,-h/2+5,L,h);
    ctx.fillStyle=magN>0?'#ef4444':'#3b82f6'; ctx.fillRect(0,-h/2,L/2,h); ctx.fillStyle=magN>0?'#3b82f6':'#ef4444'; ctx.fillRect(-L/2,-h/2,L/2,h); ctx.strokeStyle='rgba(15,23,42,0.4)'; ctx.lineWidth=1; ctx.strokeRect(-L/2,-h/2,L,h);
    tx(magN>0?'N':'S',L/2-15,7,17,'#fff','center',true); tx(magN>0?'S':'N',-L/2+15,7,17,'#fff','center',true);
    ctx.fillStyle='#e5e7eb'; ctx.strokeStyle='#475569'; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(0,0,11,0,7); ctx.fill(); ctx.stroke(); ctx.strokeStyle='#475569'; ctx.lineWidth=4; ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(0,-34); ctx.stroke(); dot(0,-34,7,'#f59e0b'); ctx.restore();
    coilFront(iNow); leads4(iNow,dt);
    galvo(CX4-75,8,150,98,ndl);
    tag('↻ 指で回すこともできます',GX4,CY4+92,11,'#a16207','center');
    panel(14,34,316,76,'');
    const red=clamp((iNow-0.5)/4,0,1), grn=clamp((-iNow-0.5)/4,0,1);
    [[262,'#ef4444',red,'赤'],[304,'#22c55e',grn,'緑']].forEach(l=>{ if(l[2]>0){ const g=ctx.createRadialGradient(l[0],66,2,l[0],66,22); g.addColorStop(0,l[1]); g.addColorStop(1,'rgba(255,255,255,0)'); ctx.globalAlpha=l[2]; ctx.fillStyle=g; ctx.beginPath(); ctx.arc(l[0],66,22,0,7); ctx.fill(); ctx.globalAlpha=1; }
      ctx.fillStyle=l[2]>0?l[1]:'#e5e7eb'; ctx.strokeStyle='#64748b'; ctx.lineWidth=1.2; ctx.beginPath(); ctx.arc(l[0],66,9,0,7); ctx.fill(); ctx.stroke(); tx(l[3]+'LED',l[0],96,10.5,C.sub,'center',true); });
    tx('2つのLEDを反対向きにつなぐと、',26,55,12,C.ink,'left',true); tx('交互に光る＝電流の向きが変わる',26,75,12,C.cur,'left',true);
    const fq=(playing&&drag!=='rot')?f:Math.abs(wGen)/(2*Math.PI); tx('毎秒 '+fmt(fq)+' 回転＝'+fmt(fq)+' Hzの交流',26,97,11.5,C.sub,'left',true);
    tx('発電機（磁石を回してコイルに電流を流す）',14,24,15,C.ink,'left',true);
    chart(14,262,616,140,4,true);
    legend([['電流（交流）',C.cur,'dot'],['N極',C.N,'dot'],['S極',C.S,'dot']],428); }

  // ---------- 統計欄・共有 ----------
  function stats(){ const m=$('mode').value, v=$('view').value, I=Iof();
    if(m==='m1'){ const wire=v==='wire', b=Bat(probe[0],probe[1]), by=b[1]+(earth?30:0.3), ang=Math.atan2(by,b[0]), bm=Math.hypot(b[0],b[1]), r=Math.hypot(probe[0],probe[1]);
      K('sA').innerHTML='電流の大きさ'; sh('sA',fmt(I)+' A',I>0?'＋極から出て－極へ流れる':'電流が流れていない');
      if(wire){ K('sB').innerHTML='電流の向き'; sh('sB',dirI>0?'下から上へ':'上から下へ','');
        K('sC').innerHTML='磁界の向き（上から見て）'; sh('sC',I>0?(dirI>0?'反時計回り':'時計回り'):'磁界ができない','右ねじの法則');
        K('sD').innerHTML='動かせる方位磁針のN極'; sh('sD',DIR8[((Math.round(ang/(Math.PI/4))%8)+8)%8]+'を向く',I>0?'導線から'+fmt(r)+' cm・地球の磁界の'+fmt(bm/30)+'倍':'電流の磁界がないので北を向く');
        setShare('【右ねじの法則】導線に'+(dirI>0?'下から上へ':'上から下へ')+fmt(I)+' Aの電流を流すと、導線を中心とした同心円状の磁界ができ、上から見て'+(dirI>0?'反時計回り':'時計回り')+'の向きになる｜シミュラボ'); }
      else { K('sB').innerHTML='電流の向き'; sh('sB',dirI>0?'左のはしから入る':'右のはしから入る','');
        K('sC').innerHTML='コイルの中の磁界'; sh('sC',I>0?(dirI>0?'右から左へ':'左から右へ'):'磁界ができない',I>0?(dirI>0?'左はしがN極':'右はしがN極'):'');
        K('sD').innerHTML='動かせる方位磁針のN極'; sh('sD',DIR8[((Math.round(ang/(Math.PI/4))%8)+8)%8]+'を向く','');
        setShare('【コイルのまわりの磁界】電流'+fmt(I)+' Aを流したコイルは棒磁石と同じ形の磁界をつくり、'+(dirI>0?'左':'右')+'のはしがN極になる（右手の4本の指を電流の向きに合わせると親指がN極の向き）｜シミュラボ'); } }
    else if(m==='m2'){ const N=+$('turns').value, nb=nbat(), I2=1.5*nb, n=swOn?clipN(N,I2):0;
      K('sA').innerHTML='コイルのまき数'; sh('sA',N+'回','導線の長さは同じ');
      K('sB').innerHTML='電流の大きさ'; sh('sB',swOn?fmt(I2)+' A':'0 A',swOn?'かん電池'+(nb===2?'2個の直列つなぎ':'1個'):'スイッチが切れている');
      K('sC').innerHTML='ついたクリップ'; sh('sC',n+'こ',core?'鉄しんあり':'鉄しんなし');
      K('sD').innerHTML='左はしの極'; sh('sD',swOn?(dirI>0?'N極':'S極'):'磁石ではない',swOn?'右はしは'+(dirI>0?'S極':'N極'):'電流を流したときだけ磁石になる');
      setShare('【電磁石の強さ】コイルのまき数'+N+'回・かん電池'+(nb===2?'2個の直列つなぎ':'1個')+(core?'':'・鉄しんなし')+'で、クリップが'+n+'こついた。まき数をふやしたり電流を大きくしたりすると電磁石は強くなる｜シミュラボ'); }
    else if(m==='m3'&&v==='swing'){ const sig=-dirI*magUp;
      K('sA').innerHTML='電流の向き（下の導線）'; sh('sA',dirI>0?'手前から奥へ':'奥から手前へ',fmt(I)+' A');
      K('sB').innerHTML='磁界の向き'; sh('sB',magUp>0?'上から下へ':'下から上へ',magUp>0?'N極が上':'N極が下');
      K('sC').innerHTML='導線が受ける力'; sh('sC',I>0?(sig<0?'磁石の外側へ':'磁石の内側へ'):'はたらかない',I>0?'電流が大きいほど大きい':'');
      K('sD').innerHTML='ぶらんこのふれ'; sh('sD',Math.round(Math.abs(phi)*180/Math.PI)+'°','');
      setShare('【フレミングの左手の法則】電流'+fmt(I)+' A・磁界が'+(magUp>0?'上から下':'下から上')+'のとき、導線は磁石の'+(sig<0?'外側':'内側')+'へ力を受けた。電流か磁界の向きの一方を反対にすると力も反対向きになる｜シミュラボ'); }
    else if(m==='m3'){ const rps=Math.abs(omega)/(2*Math.PI), still=rps<0.02;
      K('sA').innerHTML='電流の大きさ'; sh('sA',fmt(I)+' A','');
      K('sB').innerHTML='回る向き（手前から見て）'; sh('sB',still?'止まっている':(omega<0?'時計回り':'反時計回り'),'');
      K('sC').innerHTML='回る速さ'; sh('sC','毎秒 '+fmt(rps,2)+' 回転','電流に比例するモデル');
      K('sD').innerHTML='整流子'; sh('sD',comm?'あり':'なし',comm?'半回転ごとに電流の向きを切りかえ':'力が半回転ごとに逆向き→止まる');
      setShare('【モーターのしくみ】電流'+fmt(I)+' Aで、コイルは'+(still?'止まっている':'手前から見て'+(omega<0?'時計回り':'反時計回り')+'に毎秒'+fmt(rps,2)+'回転')+'。整流子が半回転ごとに電流の向きを切りかえるので同じ向きに回り続ける｜シミュラボ'); }
    else if(v==='move'){ const p=magN>0?'N':'S';
      K('sA').innerHTML='磁石の動き'; sh('sA',moveWord(),'');
      K('sB').innerHTML='検流計の針'; sh('sB',Math.abs(ndl)<0.15?'0（ふれない）':(ndl>0?'右':'左')+'にふれる',Math.abs(ndl)<0.15?'':fmt(Math.abs(ndl))+' 目もり');
      K('sC').innerHTML='いちばん大きくふれた'; sh('sC',fmt(peakAbs)+' 目もり','速く動かすほど大きい');
      K('sD').innerHTML='コイルの左はしの極'; sh('sD',Math.abs(iNow)<0.15?'なし':(iNow>0?'N極':'S極'),Math.abs(iNow)<0.15?'電流が流れていない':(vS>0?'近づく磁石をしりぞける':'遠ざかる磁石を引きとめる'));
      setShare('【電磁誘導】コイルに磁石の'+p+'極を入れると検流計の針は'+(magN>0?'右':'左')+'、出すと'+(magN>0?'左':'右')+'にふれる。磁石を止めると0、速く動かすほど大きくふれる（最大'+fmt(peakAbs)+'目もり）｜シミュラボ'); }
    else { const f=(playing&&drag!=='rot')?+$('rps').value:Math.abs(wGen)/(2*Math.PI);
      K('sA').innerHTML='回す速さ'; sh('sA','毎秒 '+fmt(f)+' 回転','');
      K('sB').innerHTML='交流の周波数'; sh('sB',fmt(f)+' Hz','1秒にくり返す回数');
      K('sC').innerHTML='電流の向きが変わる'; sh('sC','1秒に '+fmt(2*f)+' 回','');
      K('sD').innerHTML='電流の最大値'; sh('sD',fmt(3.6*f)+' 目もり','速く回すほど大きい');
      setShare('【発電機と交流】磁石を毎秒'+fmt(f)+'回転させると、向きが1秒に'+fmt(2*f)+'回入れかわる交流（'+fmt(f)+' Hz）が流れた。速く回すほど電流も大きい｜シミュラボ'); } }
  function update(){ const m=$('mode').value; setViews(m); const v=$('view').value;
    showF('view',!!VIEWS[m]); showF('cur',m==='m1'||m==='m3'); showF('bat',m==='m2'); showF('turns',m==='m2'); showF('spd',m==='m4'&&v==='move'); showF('rps',m==='m4'&&v==='gen');
    show('rev',m!=='m4'); show('flipM',m==='m3'||m==='m4'); show('earth',m==='m1'); show('core',m==='m2'); show('sw',m==='m2'); show('rec',m==='m2'); show('comm',m==='m3'&&v==='motor'); show('push',m==='m4'&&v==='move'); show('pull',m==='m4'&&v==='move'); show('play',m==='m4'&&v==='gen');
    $('earth').textContent=earth?'🌏 地球の磁界をはずす':'🌏 地球の磁界も入れる'; $('core').textContent=core?'鉄しんをぬく':'鉄しんを入れる'; $('sw').textContent=swOn?'スイッチを切る':'スイッチを入れる';
    $('comm').textContent=comm?'整流子をはずす':'整流子をつける'; $('play').textContent=playing?'⏸ 止める':'▶ 回す'; $('flipM').textContent=m==='m4'?'🧲 磁石のN極・S極を入れかえる':'🧲 磁石の極を反対にする';
    const key=m+v; if(key!==curKey){ curKey=key; hist=[]; ndl=0; ndlV=0; iNow=0; Lprev=null; mTarget=null; peakAbs=0; swingInit=true; motorInit=true;
      if(key==='m4gen'&&playing){ const f=+$('rps').value; wGen=2*Math.PI*f; thPrev=theta; for(let k=0;k<=240;k++){ const t=tNow-4+k/60, th=theta-2*Math.PI*f*(tNow-t); hist.push([t,-3.6*f*Math.sin(th)*magN]); } iNow=hist[hist.length-1][1]; ndl=iNow; } }
    stats(); }

  // ---------- 操作 ----------
  ['mode','cur','bat','turns','spd','rps'].forEach(k=>{ const el=$(k); if(!el||!Q.has(k)) return; const v=Q.get(k); if(el.tagName==='SELECT'&&![].some.call(el.options,o=>o.value===v)) return; el.value=v; el.dispatchEvent(new Event('input')); });
  setViews($('mode').value); if(Q.has('view')&&[].some.call($('view').options,o=>o.value===Q.get('view'))) $('view').value=Q.get('view');
  if(Q.get('rev')==='1') dirI=-1; if(Q.get('flip')==='1'){ magUp=-1; magN=-1; } if(Q.get('earth')==='1') earth=true; if(Q.get('comm')==='0'){ comm=false; pSide=1; }
  ['mode','view'].forEach(id=>$(id).addEventListener('change',update));
  ['cur','bat','turns','spd','rps'].forEach(id=>{ $(id).addEventListener('input',update); $(id).addEventListener('change',update); });
  $('rev').addEventListener('click',()=>{ dirI=-dirI; update(); });
  $('flipM').addEventListener('click',()=>{ if($('mode').value==='m4'){ magN=-magN; Lprev=null; } else magUp=-magUp; update(); });
  $('earth').addEventListener('click',()=>{ earth=!earth; update(); });
  $('core').addEventListener('click',()=>{ core=!core; update(); });
  $('sw').addEventListener('click',()=>{ swOn=!swOn; update(); });
  $('rec').addEventListener('click',()=>{ const N=+$('turns').value, nb=nbat(); recs.push([N,nb,swOn?clipN(N,1.5*nb):0,core]); if(recs.length>6) recs.shift(); });
  $('comm').addEventListener('click',()=>{ comm=!comm; if(!comm) pSide=Math.cos(alpha)>=0?1:-1; update(); });
  $('push').addEventListener('click',()=>{ mTarget=XIN; peakAbs=0; });
  $('pull').addEventListener('click',()=>{ mTarget=XOUT; peakAbs=0; });
  $('play').addEventListener('click',()=>{ playing=!playing; update(); });
  cv.addEventListener('pointerdown',e=>{ const p=cpos(cv,e), x=p[0]/dpr, y=p[1]/dpr, m=$('mode').value, v=$('view').value;
    if(m==='m1'){ const pp=PB.p(probe[0],probe[1],0);
      if(Math.hypot(x-pp[0],y-pp[1])<30) drag='probe';
      else { const p0=PB.p(0,0,0), bt=v==='wire'?PB.p(10.5,0,0.3):PB.p(0,-CA,4.6), onWire=v==='wire'&&Math.abs(x-p0[0])<14&&y>PB.p(0,0,6.4)[1]-6&&y<PB.p(0,0,-5.3)[1]+6;
        if(onWire||Math.hypot(x-bt[0],y-bt[1])<26){ dirI=-dirI; update(); return; }
        const b=PB.inv(x,y); if(x<466&&Math.abs(b[0])<BX&&Math.abs(b[1])<BY){ probe=[clamp(b[0],-BX+1,BX-1),clamp(b[1],-BY+1,BY-1)]; drag='probe'; stats(); } else return; } }
    else if(m==='m2'){ if(x>M2B.x&&x<M2B.x+M2B.w&&y>M2B.y-6&&y<M2B.y+M2B.h+6){ dirI=-dirI; update(); } else if(Math.abs(x-M2SW.x)<26&&Math.abs(y-M2SW.y)<24){ swOn=!swOn; update(); } return; }
    else if(m==='m3'){ if(v==='swing'){ const mg=PS.p(2.6,0,0), hf=PS.p(PX,-WY,LP), hb=PS.p(PX,WY,LP); if(Math.abs(x-mg[0])<80&&Math.abs(y-mg[1])<46){ magUp=-magUp; update(); } else if(Math.abs(x-(hf[0]+hb[0])/2)<40&&Math.abs(y-72)<26){ dirI=-dirI; update(); } }
      else { const l=PM.p(-5.1,-3.2,0), r=PM.p(5.1,-3.2,0), b=PM.p(0,-5.1,-5.0); if(Math.hypot(x-l[0],y-l[1])<48||Math.hypot(x-r[0],y-r[1])<48){ magUp=-magUp; update(); } else if(Math.hypot(x-b[0],y-b[1])<28){ dirI=-dirI; update(); } } return; }
    else if(v==='move'){ if(Math.abs(x-mX)<84&&Math.abs(y-CY4)<28){ drag='mag'; dragOff=x-mX; mTarget=null; peakAbs=0; } else return; }
    else { if(Math.hypot(x-GX4,y-CY4)<92){ drag='rot'; rotA=Math.atan2(-(y-CY4),x-GX4); } else return; }
    try{ cv.setPointerCapture(e.pointerId); }catch(_){ } e.preventDefault(); });
  cv.addEventListener('pointermove',e=>{ if(!drag) return; const p=cpos(cv,e), x=p[0]/dpr, y=p[1]/dpr;
    if(drag==='probe'){ const b=PB.inv(x,y); probe=[clamp(b[0],-BX+1,BX-1),clamp(b[1],-BY+1,BY-1)]; stats(); }
    else if(drag==='mag') mX=clamp(x-dragOff,MXMIN,MXMAX);
    else if(drag==='rot'){ const a=Math.atan2(-(y-CY4),x-GX4); let d=a-rotA; d=Math.atan2(Math.sin(d),Math.cos(d)); theta+=d; rotA=a; } });
  const endDrag=()=>{ drag=null; }; cv.addEventListener('pointerup',endDrag); cv.addEventListener('pointercancel',endDrag);
  function frame(t){ const dt=last?Math.min(0.05,(t-last)/1000):0; last=t; tNow+=dt; const m=$('mode').value, v=$('view').value;
    ctx.fillStyle=C.bg; ctx.fillRect(0,0,W,H);
    if(m==='m1'){ if(v==='coil') sceneCoil(dt); else sceneWire(dt); }
    else if(m==='m2') sceneMag(dt);
    else if(m==='m3'){ if(v==='motor') sceneMotor(dt); else sceneSwing(dt); }
    else { if(v==='gen') sceneGen(dt); else sceneMove(dt); }
    stT+=dt; if(stT>0.25&&(m==='m3'||m==='m4')){ stT=0; stats(); }
    requestAnimationFrame(frame); }
  update(); frame(performance.now());
'''

DENRYU_ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
<p>電流が流れる導線やコイルのまわりには<b>磁界</b>ができます。磁界の向きは電流の向きで決まり（<b>右ねじの法則</b>）、電流が大きいほど、導線に近いほど強くなります。コイルに鉄しんを入れた<b>電磁石</b>は、電流を大きくしたり巻き数を多くしたりすると強くなります。磁界の中の導線に電流を流すと<b>力</b>がはたらき、その向きは電流の向きと磁界の向きで決まります（<b>フレミングの左手の法則</b>）。この力でコイルを回し続けるのが<b>モーター</b>です。反対に、コイルの中の磁界を変化させるとコイルに電流が流れます（<b>電磁誘導</b>）。これを利用したのが<b>発電機</b>です。</p>
''' + N("対応する単元：小学校第5学年 A（3）電流がつくる磁力／中学校第2学年 第1分野（3）電流とその利用 ア（イ）電流と磁界（電流がつくる磁界、磁界中の電流が受ける力、電磁誘導と発電）") + '''
<h2>授業での使い方</h2>
<h3>導入：見えない磁界を「見える」ようにする</h3>
<p>中2では「① 電流がつくる磁界」で、実験の前に方位磁針の向きを予想させます。電流を0 Aから少しずつ大きくすると、方位磁針がそろって円をえがく向きに回っていく様子が見られます。「地球の磁界も入れる」を押すと、電流が小さいときや導線から遠い所では方位磁針が北を向こうとすることもわかり、実験で針が円の向きにそろわないときの理由の説明に使えます。小5では「② 電磁石の強さ」で、コイルに電流を流したときだけクリップがつくことを確かめます。</p>
<h3>展開：条件を1つずつ変えて調べる</h3>
<p>小5の電磁石では、まき数だけを変える（かん電池はそのまま）、かん電池の数だけを変える（まき数はそのまま）という比べ方をさせ、「📋 結果を記録」で表にまとめます。まき数を変えるときに<b>導線の長さをそろえる</b>こと（あまった導線は切らずにまとめておく）も画面に出しています。中2の「③ 電流が受ける力」では、電流の向き・磁界の向きを1つずつ反対にして力の向きを表にまとめさせ、モーターの画面で「整流子をはずす」を押して、整流子の役割を考えさせます。「④ 電磁誘導」では、磁石を指で出し入れして、検流計の針がふれるのは磁石が動いているときだけであることを確かめます。</p>
<h3>まとめ：モーターと発電機をつなげる</h3>
<p>モーターは「電流が磁界から受ける力」で回り、発電機は「コイルの中の磁界の変化」で電流をつくります。発電機の画面で、回す速さを変えると交流の向きの変わり方と大きさが変わることを確かめ、家庭のコンセントの交流（東日本50 Hz、西日本60 Hz）につなげてまとめます。</p>
<p><b>児童・生徒への問いの例</b></p>
<ol>
<li>導線に下から上へ大きな電流を流したとき、導線の西側に置いた方位磁針のN極はどちらを向くでしょう。（中2　答え：南。上から見て反時計回りの磁界ができるため）</li>
<li>電磁石のまき数を2倍にして強さを比べるとき、導線の長さをそろえるのはなぜでしょう。（小5　答え：導線の長さが変わると流れる電流の大きさも変わり、まき数のちがいだけを比べられなくなるため）</li>
<li>コイルに磁石のN極を入れたまま止めると、検流計の針はどうなるでしょう。そのあと引きぬくとどうなるでしょう。（中2　答え：止めると0にもどる。引きぬくと入れたときと反対にふれる）</li>
</ol>
<h2>しくみ・解説</h2>
<h3>電流がつくる磁界（右ねじの法則）</h3>
<p>まっすぐな導線に電流を流すと、導線を中心とした<b>同心円状の磁界</b>ができます。右ねじを電流の向きに進めるとき、ねじを回す向きが磁界の向きです（右ねじの法則）。右手の親指を電流の向きに合わせたとき、残りの4本の指が曲がる向きが磁界の向き、と覚えることもできます。コイルでは、右手の4本の指を電流の向きに合わせてコイルをにぎると、親指の向きがコイルの中の磁界の向きになり、親指の側がN極です。コイルのまわりの磁界は棒磁石のまわりの磁界と同じ形になります。</p>
''' + T([[NW("まっすぐな導線"), "導線を中心とした同心円", "右ねじの法則（ねじの進む向き＝電流、回す向き＝磁界）", "電流を大きくする・導線に近づく"],
          ["コイル", "棒磁石と同じ形。コイルの中はほぼ平行", "右手の4本の指＝電流の向き、親指＝N極の向き", "電流を大きくする・巻き数をふやす・鉄しんを入れる"]],
         ["", "磁力線の形", "向きの決め方", "磁界を強くするには"]) + '''
<p>まっすぐな導線のまわりの磁界の強さは、電流に比例し、導線からの距離に反比例します（高校の物理で学ぶ式：B＝μ<sub>0</sub>I÷2πr）。たとえば3 Aの電流から2 cm離れた所の磁界は約30 μT（マイクロテスラ）で、日本付近の地球の磁界の水平方向の強さ（約30 μT）と同じくらいです。電流が小さいときや導線から遠い所で方位磁針がうまく円の向きにそろわないのは、地球の磁界の影響を受けるからです。</p>
''' + T([["1 A", "20 μT", "10 μT", "約0.7倍"], ["3 A", "60 μT", "30 μT", "約2倍"], ["5 A", "100 μT", "50 μT", "約3.3倍"]],
         ["電流", "導線から1 cm", "導線から2 cm", "1 cmの所で、地球の磁界（約30 μT）の"]) + '''
<h3>電磁石の強さ（小5）</h3>
<p>電流が流れているコイルは、中に入れた鉄しんを磁石にします（電磁石）。電流の向きを反対にすると、N極とS極が入れかわります。電磁石の強さは、電流の大きさとコイルのまき数で変わります。比べるときは、変える条件を1つにして、ほかの条件はそろえます。まき数を変えるときも導線の全体の長さは同じにし、あまった導線は切らずにまとめておきます。</p>
''' + T([["100回", "1個（1.5 A）", "8こ", "もとにする"], ["200回", "1個（1.5 A）", "16こ", "まき数を2倍"], ["100回", "2個の直列つなぎ（3.0 A）", "16こ", "電流を2倍"], ["200回", "2個の直列つなぎ（3.0 A）", "32こ", "両方2倍"]],
         ["まき数", "かん電池", "ついたクリップ（モデル）", "変えた条件"]) + '''
<p>表の数はこのシミュレーションのモデル（クリップの数がまき数×電流に比例するとした値）です。実際の実験では、鉄しんの太さやクリップのつき方で数がばらつくので、何回か調べて比べます。</p>
<h3>磁界の中の電流が受ける力（フレミングの左手の法則）</h3>
<p>U字形磁石の間に導線をつるし（電気ぶらんこ）、電流を流すと、導線は磁界から力を受けて動きます。電流の向きか磁界の向きのどちらか一方を反対にすると、力の向きも反対になります。両方を反対にすると、力の向きはもとと同じです。電流を大きくしたり、磁石を強くしたりすると、力は大きくなります。</p>
''' + T([["もとのまま", "もとのまま", "磁石の外側へ"], ["反対", "もとのまま", "磁石の内側へ"], ["もとのまま", "反対", "磁石の内側へ"], ["反対", "反対", "磁石の外側へ"]],
         ["電流の向き", "磁界の向き", "力の向き（このシミュレーターの図）"]) + '''
<p>電流・磁界・力の向きの関係は、左手の中指・人差し指・親指をたがいに直角に開いて、中指を電流、人差し指を磁界の向きに合わせたとき、親指が力の向きになる、とまとめられます。これを<b>フレミングの左手の法則</b>といい、中指から順に「電・磁・力」と覚えます。中学校では、電流や磁界の向きを変えたときに力の向きが変わることを実験で確かめます（この法則の名前は、教科書によっては発展として紹介されています。高校の物理で詳しく学びます）。</p>
<h3>モーターが回るしくみ（整流子とブラシ）</h3>
<p>磁界の中のコイルに電流を流すと、コイルの向かい合う2つの辺に反対向きの力がはたらき、コイルが回ります。ところが、コイルが半回転すると力の向きが回転をじゃまする向きになるため、そのままではコイルは行ったり来たりして止まってしまいます。そこでモーターには<b>整流子</b>と<b>ブラシ</b>がついていて、コイルが半回転するごとにコイルに流れる電流の向きを切りかえます。こうしてコイルはいつも同じ向きに回り続けます。</p>
<h3>電磁誘導と発電機</h3>
<p>コイルに磁石を出し入れすると、コイルの中の磁界が変化して、コイルに電圧が生じ電流が流れます。この現象を<b>電磁誘導</b>、流れる電流を<b>誘導電流</b>といいます。</p>
''' + T([["N極を入れる", "右（＋）", "コイルの左はしがN極（近づく磁石をしりぞける）"], ["N極を出す", "左（－）", "コイルの左はしがS極（遠ざかる磁石を引きとめる）"], ["S極を入れる", "左（－）", "コイルの左はしがS極"], ["S極を出す", "右（＋）", "コイルの左はしがN極"], ["磁石を止める", "0（ふれない）", "磁界が変化しないので電流は流れない"]],
         ["操作", "検流計の針（このシミュレーターの図）", "コイルにできる磁界"]) + '''
<p>誘導電流は、磁石を速く動かすほど、磁石が強いほど、コイルの巻き数が多いほど大きくなります。誘導電流の向きが「磁石の動きをさまたげる向き」になること（レンツの法則）は、高校の物理で詳しく学びます。発電機は、磁石やコイルを回し続けることで電磁誘導を起こし続け、電流をつくります。回転するたびにコイルの中の磁界の向きが入れかわるので、電流の向きが周期的に変わる<b>交流</b>になります。</p>
<h3>直流と交流</h3>
''' + T([["直流", "向きが一定", "かん電池、光電池、スマートフォンの充電池"], ["交流", "向きと大きさが周期的に変わる", "家庭のコンセント（東日本50 Hz、西日本60 Hz）、発電所の発電機"]],
         ["", "電流の向き", "例"]) + '''
<p>1秒間に向きの変化をくり返す回数を<b>周波数</b>といい、単位はヘルツ（Hz）です。50 Hzの交流では、1秒間に電流の向きが100回入れかわります。発光ダイオード（LED）を2つ、向きを反対にしてつなぐと、交流では2つが交互に光ります。</p>
<h3>このシミュレーションで単純化していること</h3>
<ul>
<li>まっすぐな導線のまわりの磁界は B＝μ<sub>0</sub>I÷2πr で計算しています。地球の磁界は、日本付近の水平方向の強さを約30 μT（北向き）としています（伏角や場所によるちがいは考えていません）。「地球の磁界も入れる」を押していないときは、地球の磁界をとても小さいとして、導線の磁界だけで方位磁針の向きを決めています。</li>
<li>コイルの磁力線は、厚紙をつらぬく導線を長い直線電流の集まりとみなして計算した厚紙の面の磁界です。本数は電流の大きさに比例させていますが、強さは実際の値ではありません。</li>
<li>電磁石のクリップの数は、まき数×電流に比例するモデルです。かん電池1個の電流を1.5 A、2個の直列つなぎを3.0 Aとし、電池の中の抵抗は考えていません。鉄しんがないときは、鉄しんありの約6％の強さとしています。</li>
<li>ぶらんこのふれの大きさ、モーターの回る速さ（電流に比例）、検流計の目もりはモデルの値です。モーターは、コイルが回ることで生じる電圧（逆起電力）を考えず、まさつで速さが決まるとしています。</li>
<li>電磁誘導は、棒磁石を両はしの磁極で表したモデルでコイルを通る磁界の量を計算し、その変化の速さに比例する電流としています。発電機は、磁界の量が回転の角度で正弦波状に変わるとしています。</li>
<li>見やすさのため、磁石・コイル・導線の大きさや位置関係は実際の実験装置とは変えています。</li>
</ul>
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「小学校学習指導要領（平成29年告示）解説 理科編」第5学年 A（3）電流がつくる磁力　''' + A(MEXT_SHO, "小学校学習指導要領解説") + '''</li>
<li>文部科学省「中学校学習指導要領（平成29年告示）解説 理科編」第1分野（3）電流とその利用（イ）電流と磁界　''' + A(MEXT_CHU, "中学校学習指導要領解説") + '''</li>
<li>小学校理科の教科書（第5学年「電流がうみ出す力」「電磁石の性質」などの単元）、中学校理科の教科書（第2学年「電流と磁界」の単元）</li>
<li>国土地理院「磁気図」（日本付近の地磁気の水平分力）</li>
</ul>
'''

sim(slug="denryu-jikai", cat="rika", emoji="🧭", score=82,
    title="電流と磁界シミュレーター（電磁石・モーター・発電機）",
    title_tag="電磁誘導・モーターの仕組み・電磁石のシミュレーター｜右ねじの法則・フレミング左手の法則・発電機（電流と磁界）",
    meta_desc="電流がつくる磁界（右ねじの法則）、電磁石の強さ、磁界の中の電流が受ける力（フレミングの左手の法則）とモーターの仕組み、電磁誘導と発電機を、立体の図と矢印で確かめる無料シミュレーター。方位磁針や磁石を指で動かせます。小5・中2の理科の授業向け。",
    og_title="電流と磁界シミュレーター（電磁石・モーター・発電機）",
    og_desc="右ねじの法則、電磁石の強さ、フレミングの左手の法則とモーター、電磁誘導と発電機を立体の図と矢印で確かめる。小5・中2の授業向け。",
    card_desc="右ねじの法則・電磁石・モーターの整流子・電磁誘導を、電流・磁界・力の矢印つき立体図で確かめる。",
    lead="電流のまわりにできる磁界、電磁石の強さ、磁界の中の電流が受ける力とモーター、磁石の出し入れで流れる誘導電流と発電機の4つの実験を、立体の図と矢印で確かめられます。電流の向き（＋極→－極）・磁界の向き・力の向きを色分けした矢印で示し、方位磁針や磁石は指で動かせます。",
    model="小5 電流がつくる磁力／中2 電流と磁界（電磁誘導・モーター）",
    level="小学5年、中学2年",
    unit="小学校 第5学年 A（3）電流がつくる磁力／中学校 第1分野（3）電流とその利用 ア（イ）電流と磁界",
    canvas=canvas(640, 440, light=True),
    controls=select("mode", "実験", [("m1", "① 電流がつくる磁界（中2）"), ("m2", "② 電磁石の強さ（小5）"), ("m3", "③ 電流が受ける力・モーター（中2）"), ("m4", "④ 電磁誘導・発電機（中2）")])
           + select("view", "表示", [("wire", "まっすぐな導線"), ("coil", "コイル")])
           + slider("cur", "電流の大きさ", 0, 5, 3, 0.5, "{v} A")
           + select("bat", "かん電池", [("one", "1個（1.5 A）"), ("two", "2個の直列つなぎ（3.0 A）")])
           + slider("turns", "コイルのまき数", 50, 300, 100, 50, "{v}回")
           + slider("spd", "磁石を動かす速さ（1〜5）", 1, 5, 3, 1)
           + slider("rps", "回す速さ", 0.2, 2.5, 1, 0.1, "毎秒 {v} 回転"),
    buttons=btn("rev", "🔄 電流の向きを反対にする") + btn("flipM", "🧲 磁石の極を反対にする") + btn("earth", "🌏 地球の磁界も入れる")
           + btn("core", "鉄しんをぬく") + btn("sw", "スイッチを切る") + btn("rec", "📋 結果を記録", True)
           + btn("comm", "整流子をはずす") + btn("push", "➡ 磁石を入れる", True) + btn("pull", "⬅ 磁石を出す", True) + btn("play", "⏸ 止める"),
    stats=stats([("sA", "電流の大きさ", True), ("sB", "電流の向き", False), ("sC", "磁界の向き", False), ("sD", "方位磁針", False)]),
    legend="オレンジの粒と矢印＝電流の向き（＋極から出て－極へ）、青＝磁界の向き（磁力線）、緑＝力の向き。方位磁針は赤いほうがN極です。方位磁針・磁石は指で動かせ、導線・電源・磁石をタップすると向きが反対になります。",
    article=DENRYU_ARTICLE,
    faqs=[("右ねじの法則とは何ですか？", "電流がつくる磁界の向きを決めるきまりです。右ねじを電流の向きに進めるとき、ねじを回す向きが磁界の向きになります。まっすぐな導線のまわりには、導線を中心とした同心円状の磁界ができ、下から上へ流れる電流なら、上から見て反時計回りの向きです。"),
          ("フレミングの左手の法則の覚え方は？", "左手の中指・人差し指・親指をたがいに直角に開き、中指を電流の向き、人差し指を磁界の向き（N極からS極）に合わせると、親指の向きが導線の受ける力の向きになります。中指から順に「電・磁・力」と覚えます。電流か磁界の一方を反対にすると力も反対向きになります。"),
          ("モーターの整流子は何のためにあるのですか？", "コイルが半回転するごとに、コイルに流れる電流の向きを切りかえるためです。切りかえないと、半回転したところで力が回転をじゃまする向きになり、コイルは行ったり来たりして止まってしまいます。整流子とブラシのおかげで、コイルは同じ向きに回り続けます。"),
          ("誘導電流を大きくするにはどうすればよいですか？", "磁石を速く動かす、強い磁石を使う、コイルの巻き数をふやす、のいずれかです。磁石を止めるとコイルの中の磁界が変化しないので、誘導電流は流れません。"),
          ("電磁石を強くするにはどうすればよいですか？（小5）", "電流を大きくする（かん電池を直列つなぎにする）か、コイルのまき数をふやします。比べるときは、変える条件を1つにして、導線の長さなどほかの条件はそろえます。電流の向きを反対にすると、電磁石のN極とS極が入れかわります。"),
          ("直流と交流のちがいは何ですか？", "直流は電流の向きが一定の電流（かん電池など）、交流は向きと大きさが周期的に変わる電流（家庭のコンセントなど）です。1秒間にくり返す回数を周波数といい、東日本は50 Hz、西日本は60 Hzです。発電機では、磁石やコイルを回すと交流が生じます。")],
    rel=[("magnet", "🧲", "磁力線シミュレーター"), ("denki-kairo", "🔌", "電気回路シミュレーター"), ("solar-hatsuden", "🔋", "今日のソーラー発電シミュ"), ("denkidai-keisan", "💡", "電気代計算機")],
    js=JS_DENRYU)


# ============================================================ 2 化学変化と質量
JS_KAGAKU = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const FF='"Hiragino Sans","Hiragino Kaku Gothic ProN","Noto Sans JP","Yu Gothic UI","Yu Gothic",Meiryo,sans-serif';
  const C={bg:'#f8fafc',ink:'#0f172a',sub:'#64748b',acc:'#0e7490',grid:'#e2e8f0',O:'#dc2626',ok:'#047857'};
  // 質量の比は教科書の値（銅：酸素＝4：1、マグネシウム：酸素＝3：2）。p は1回の加熱で反応する割合（モデル）
  const MET={cu:{nm:'銅',ox:'酸化銅',sym:'Cu',r:0.25,a:4,b:1,p:0.7,col:'#b45309',oxc:'#1c1917',pt:'#c2410c',list:[0.4,0.6,0.8,1.0,1.2,1.4]},
             mg:{nm:'マグネシウム',ox:'酸化マグネシウム',sym:'Mg',r:2/3,a:3,b:2,p:0.8,col:'#a8a29e',oxc:'#f5f5f4',pt:'#475569',list:[0.3,0.6,0.9,1.2,1.5]}};
  // 炭酸水素ナトリウム1.00 g＋うすい塩酸（十分な量）→ 二酸化炭素 1.00×44.01÷84.01＝0.52 g
  const RX={gas:{m0:82.46,gas:0.52},ppt:{m0:96.35,gas:0}};
  const HEAT=0.9, Q=new URLSearchParams(location.search);
  let smp=null, recs=[], noise=false, heatT=0, autoRun=false, last=0, tNow=0, stT=0, sl=null, bub=[];

  // ---------- 描画の部品 ----------
  function fmt2(v){ return (+v).toFixed(2); }
  function r2(v){ return Math.round(v*100+1e-7)/100; }
  function tx(s,x,y,size,col,align,bold){ const parts=String(s).split(/_(\d)/), fs=n=>(bold?'bold ':'')+n+'px '+FF; let w=0;
    const seg=parts.map((t,i)=>{ const sub=i%2===1; ctx.font=fs(sub?Math.round(size*0.72):size); const m=ctx.measureText(t).width; w+=m; return [t,sub,m]; });
    let cx=align==='center'?x-w/2:align==='right'?x-w:x; ctx.fillStyle=col; ctx.textAlign='left';
    seg.forEach(g=>{ if(!g[0]) return; ctx.font=fs(g[1]?Math.round(size*0.72):size); ctx.fillText(g[0],cx,y+(g[1]?size*0.25:0)); cx+=g[2]; }); return w; }
  function tw(s,size,bold){ ctx.font=(bold?'bold ':'')+size+'px '+FF; return ctx.measureText(s).width; }
  function rr(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
  function panel(x,y,w,h){ ctx.fillStyle='#fff'; ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1.2; rr(x,y,w,h,10); ctx.fill(); ctx.stroke(); }
  function dot(x,y,r,col){ ctx.fillStyle=col; ctx.beginPath(); ctx.arc(x,y,r,0,7); ctx.fill(); }
  function tag(s,x,y,size,col,align){ const w=tw(s,size,true), x0=align==='right'?x-w:align==='center'?x-w/2:x; ctx.fillStyle='rgba(255,255,255,0.92)'; rr(x0-4,y-size-1,w+8,size+6,5); ctx.fill(); tx(s,x0,y,size,col,'left',true); }
  function head(x,y,ux,uy,col,s){ const l=Math.hypot(ux,uy)||1; ux/=l; uy/=l; const bx=x-ux*s*1.6, by=y-uy*s*1.6; ctx.fillStyle=col; ctx.beginPath(); ctx.moveTo(x,y); ctx.lineTo(bx-uy*s*0.85,by+ux*s*0.85); ctx.lineTo(bx+uy*s*0.85,by-ux*s*0.85); ctx.closePath(); ctx.fill(); }
  function arr(x1,y1,x2,y2,col,w,s){ const dx=x2-x1, dy=y2-y1, l=Math.hypot(dx,dy); if(l<1) return; const ux=dx/l, uy=dy/l; ctx.strokeStyle=col; ctx.lineWidth=w; ctx.lineCap='round'; ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2-ux*s*1.3,y2-uy*s*1.3); ctx.stroke(); head(x2,y2,ux,uy,col,s); }
  function mix(a,b,t){ const p=h=>[1,3,5].map(i=>parseInt(h.substr(i,2),16)), A=p(a), B=p(b); return 'rgb('+A.map((x,i)=>Math.round(x+(B[i]-x)*clamp(t,0,1))).join(',')+')'; }
  // 原子のモデル（色・半径・文字の色）
  const EL={Cu:['#c2410c',14,'#fff'],Mg:['#94a3b8',13,'#fff'],O:['#ef4444',10,'#fff'],H:['#ffffff',7.5,'#334155'],C:['#374151',11,'#fff'],Na:['#8b5cf6',13,'#fff'],Cl:['#16a34a',12,'#fff'],S:['#eab308',12,'#422006'],Ba:['#0d9488',15,'#fff']};
  function atom(x,y,el,s,al){ const e=EL[el], r=e[1]*(s||1); ctx.save(); ctx.globalAlpha=al==null?1:al; const g=ctx.createRadialGradient(x-r*0.35,y-r*0.4,r*0.1,x,y,r); g.addColorStop(0,'rgba(255,255,255,0.9)'); g.addColorStop(0.4,e[0]); g.addColorStop(1,e[0]);
    ctx.fillStyle=g; ctx.beginPath(); ctx.arc(x,y,r,0,7); ctx.fill(); ctx.strokeStyle='rgba(15,23,42,0.4)'; ctx.lineWidth=1; ctx.stroke(); if(r>=7) tx(el,x,y+r*0.36,Math.max(8,Math.round(r*(el.length>1?0.78:0.95))),e[2],'center',true); ctx.restore(); }
  const MOL={NaHCO3:[['Na',-30,-11],['H',27,-15],['O',-14,-7],['O',14,-8],['O',0,15],['C',0,0]], HCl:[['H',-9,0],['Cl',7,0]], NaCl:[['Na',-10,0],['Cl',10,0]], H2O:[['H',-11,8],['H',11,8],['O',0,0]], CO2:[['O',-17,0],['O',17,0],['C',0,0]],
    H2SO4:[['H',-30,-5],['H',30,-5],['O',-16,0],['O',16,0],['O',0,-16],['O',0,16],['S',0,0]], BaOH2:[['H',-36,7],['H',36,7],['O',-22,0],['O',22,0],['Ba',0,0]], BaSO4:[['O',-4,0],['O',24,0],['O',10,-15],['O',10,15],['S',10,0],['Ba',-24,0]]};
  function mol(name,x,y,al){ MOL[name].forEach(a=>atom(x+a[1],y+a[2],a[0],1,al)); }

  // ---------- ① 金属の加熱 ----------
  function newSample(){ const k=$('metal').value, m=+$('mass').value; smp={k:k,m:m,n:0,f:0,cap:1,off:0,reads:[r2(m)],done:false};
    if(noise){ smp.cap=k==='cu'?0.9+Math.random()*0.08:0.94+Math.random()*0.05; smp.off=[-0.01,0,0,0.01][Math.floor(Math.random()*4)]; } heatT=0; autoRun=false; }
  function applyHeat(){ const s=smp, M=MET[s.k]; s.n++; if(s.done){ s.reads.push(s.reads[s.n-1]); return; }
    s.f=s.cap*(1-Math.pow(1-M.p,s.n)); const rd=r2(s.m*(1+M.r*s.f)+s.off); s.reads.push(rd);
    if(s.n>=2&&rd===s.reads[s.n-1]){ s.done=true; record(s.k,s.m,r2(rd-s.reads[0])); } }
  function record(k,m,o){ recs=recs.filter(r=>!(r.k===k&&Math.abs(r.m-m)<1e-6)); recs.push({k:k,m:m,o:o}); }
  function batch(){ const k=$('metal').value, M=MET[k]; M.list.forEach(m=>{ let cap=1, off=0; if(noise){ cap=k==='cu'?0.9+Math.random()*0.08:0.94+Math.random()*0.05; off=[-0.01,0,0,0.01][Math.floor(Math.random()*4)]; } record(k,m,r2(r2(m*(1+M.r*cap)+off)-r2(m))); }); }
  function meas(s){ const M=MET[s.k], rd=s.reads[s.n], o=Math.max(0,r2(rd-s.reads[0])), oxide=Math.min(rd,r2(o*(M.a+M.b)/M.b)); return {rd:rd,o:o,oxide:oxide,unr:Math.max(0,r2(rd-oxide))}; }
  function ratioTxt(k,m,o){ const M=MET[k]; if(!(o>0)) return '—'; const v=M.a*o/m; return Math.abs(v-M.b)<0.006?M.a+'：'+M.b:M.a+'：'+v.toFixed(2); }
  function slope(k){ const p=recs.filter(r=>r.k===k); if(p.length<2) return null; return p.reduce((a,r)=>a+r.m*r.o,0)/p.reduce((a,r)=>a+r.m*r.m,0); }
  function apparatus(x,y,w,h){ const s=smp, M=MET[s.k], heating=heatT>0, cx=x+w/2, gy=y+160, by=y+h-14;
    panel(x,y,w,h); tx('ステンレス皿で加熱する',x+10,y+20,12.5,C.ink,'left',true);
    ctx.fillStyle='#1e293b'; rr(x+10,y+30,w-20,56,8); ctx.fill(); tx('電子てんびん（皿の質量は引いた値）',x+18,y+46,10,'#94a3b8','left',true);
    tx(fmt2(s.reads[s.n])+' g',x+w-18,y+77,23,'#a7f3d0','right',true); tx(s.n?'加熱'+s.n+'回目のあと':'加熱前',x+18,y+76,11,'#e2e8f0','left',true);
    tx(s.done?'質量が一定になった':(heating?(s.k==='mg'?'強い光を出して燃え、白くなる':'加熱され、黒い酸化銅に変わる'):(s.n?'よく混ぜて、また加熱する':'加熱すると酸素と結びつく')),cx,y+106,11.5,s.done?C.ok:C.sub,'center',true);
    // バーナー・三脚・金網
    ctx.strokeStyle='#475569'; ctx.lineWidth=2.4; ctx.beginPath(); ctx.moveTo(cx-44,gy); ctx.lineTo(cx-62,by); ctx.moveTo(cx+44,gy); ctx.lineTo(cx+62,by); ctx.stroke();
    ctx.fillStyle='#64748b'; rr(cx-24,by-8,48,10,3); ctx.fill(); ctx.fillStyle='#94a3b8'; ctx.fillRect(cx-7,gy+38,14,by-gy-44); ctx.fillStyle='#475569'; ctx.fillRect(cx-9,gy+34,18,6);
    if(heating){ const fl=0.85+0.15*Math.sin(tNow*40), g=ctx.createLinearGradient(0,gy+34,0,gy); g.addColorStop(0,'rgba(37,99,235,0.95)'); g.addColorStop(1,'rgba(147,197,253,0.25)'); ctx.fillStyle=g; ctx.beginPath(); ctx.moveTo(cx-8,gy+34); ctx.quadraticCurveTo(cx-13,gy+14,cx,gy+2+5*(1-fl)); ctx.quadraticCurveTo(cx+13,gy+14,cx+8,gy+34); ctx.closePath(); ctx.fill(); }
    ctx.strokeStyle='#475569'; ctx.lineWidth=2.4; ctx.beginPath(); ctx.moveTo(cx-58,gy); ctx.lineTo(cx+58,gy); ctx.stroke();
    // 皿と粉末
    const dy=gy-7; ctx.fillStyle='#cbd5e1'; ctx.beginPath(); ctx.ellipse(cx,dy,50,9,0,0,7); ctx.fill(); ctx.strokeStyle='#64748b'; ctx.lineWidth=1.2; ctx.stroke(); ctx.fillStyle='#e2e8f0'; ctx.beginPath(); ctx.ellipse(cx,dy-2,42,6.5,0,0,7); ctx.fill();
    const pc=mix(M.col,M.oxc,s.f); ctx.fillStyle=pc; ctx.beginPath(); ctx.ellipse(cx,dy-4,31,5,0,0,7); ctx.fill();
    for(let i=0;i<30;i++){ const a=i*2.399, q=Math.sqrt((i+0.5)/30); dot(cx+Math.cos(a)*29*q,dy-4+Math.sin(a)*4.2*q,1.1,mix(pc,i%2?'#ffffff':'#000000',0.22)); }
    if(heating){ const R=s.k==='mg'?62:34, gl=ctx.createRadialGradient(cx,dy-6,2,cx,dy-6,R); gl.addColorStop(0,s.k==='mg'?'rgba(255,255,255,0.98)':'rgba(249,115,22,0.75)'); gl.addColorStop(1,'rgba(255,255,255,0)'); ctx.fillStyle=gl; ctx.beginPath(); ctx.arc(cx,dy-6,R,0,7); ctx.fill(); }
    tx(M.nm+'の粉末 '+fmt2(s.m)+' g',cx,dy-20,11.5,C.ink,'center',true); }
  function graph1(x,y,w,h){ const s=smp, M=MET[s.k], X0=x+42, X1=x+w-14, Y0=y+h-40, Y1=y+48, nx=Math.max(5,s.n+1);
    panel(x,y,w,h); tx('加熱した回数と質量',x+10,y+20,12.5,C.ink,'left',true);
    let lo=Math.max(0,Math.floor(s.m*10-1e-6)/10-0.1), hi=Math.ceil(s.m*(1+M.r)*10-1e-6)/10+0.1; const st=(hi-lo)>1.0?0.2:0.1; lo=Math.floor(lo/st+1e-6)*st; hi=Math.ceil(hi/st-1e-6)*st;
    const px=i=>X0+(X1-X0)*i/nx, py=v=>Y0-(Y0-Y1)*(v-lo)/(hi-lo);
    ctx.strokeStyle=C.grid; ctx.lineWidth=1; for(let v=lo; v<=hi+1e-6; v+=st){ ctx.beginPath(); ctx.moveTo(X0,py(v)); ctx.lineTo(X1,py(v)); ctx.stroke(); tx(v.toFixed(1),X0-5,py(v)+4,10.5,C.sub,'right'); }
    for(let i=0;i<=nx;i++) tx(String(i),px(i),Y0+15,10.5,C.sub,'center');
    ctx.strokeStyle=C.ink; ctx.lineWidth=1.3; ctx.beginPath(); ctx.moveTo(X0,Y1-4); ctx.lineTo(X0,Y0); ctx.lineTo(X1,Y0); ctx.stroke();
    tx('質量［g］',x+10,y+36,10.5,C.sub,'left',true); tx('加熱した回数［回］',X1,Y0+32,10.5,C.sub,'right',true);
    if(s.done){ const fy=py(s.reads[s.n]); ctx.setLineDash([5,4]); ctx.strokeStyle=C.ok; ctx.lineWidth=1.4; ctx.beginPath(); ctx.moveTo(X0,fy); ctx.lineTo(X1,fy); ctx.stroke(); ctx.setLineDash([]); tag('一定になった',X1-2,fy-7,10.5,C.ok,'right'); }
    ctx.strokeStyle=M.pt; ctx.lineWidth=2; ctx.beginPath(); s.reads.forEach((v,i)=>{ if(i) ctx.lineTo(px(i),py(v)); else ctx.moveTo(px(i),py(v)); }); ctx.stroke();
    s.reads.forEach((v,i)=>{ ctx.fillStyle='#fff'; ctx.strokeStyle=M.pt; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(px(i),py(v),4,0,7); ctx.fill(); ctx.stroke(); });
    const lv=s.reads[s.n], lr=s.n<nx-1; tag(fmt2(lv)+' g',px(s.n)+(lr?8:-8),py(lv)+(s.done?19:-8),11,C.ink,lr?'left':'right'); }
  function graph2(x,y,w,h){ const X0=x+40, X1=x+w-12, Y0=y+h-74, Y1=y+48, XM=1.6, YM=1.0, px=v=>X0+(X1-X0)*v/XM, py=v=>Y0-(Y0-Y1)*v/YM;
    panel(x,y,w,h); tx('金属と結びつく酸素の質量',x+10,y+20,12.5,C.ink,'left',true);
    ctx.strokeStyle=C.grid; ctx.lineWidth=1; for(let v=0.2;v<=YM+1e-6;v+=0.2){ ctx.beginPath(); ctx.moveTo(X0,py(v)); ctx.lineTo(X1,py(v)); ctx.stroke(); } for(let v=0.4;v<=XM+1e-6;v+=0.4){ ctx.beginPath(); ctx.moveTo(px(v),Y0); ctx.lineTo(px(v),Y1); ctx.stroke(); }
    for(let v=0;v<=YM+1e-6;v+=0.2) tx(v.toFixed(1),X0-5,py(v)+4,10.5,C.sub,'right'); for(let v=0;v<=XM+1e-6;v+=0.4) tx(v.toFixed(1),px(v),Y0+15,10.5,C.sub,'center');
    ctx.strokeStyle=C.ink; ctx.lineWidth=1.3; ctx.beginPath(); ctx.moveTo(X0,Y1-4); ctx.lineTo(X0,Y0); ctx.lineTo(X1,Y0); ctx.stroke();
    tx('酸素［g］',x+10,y+36,10.5,C.sub,'left',true); tx('金属の質量［g］',X1,Y0+31,10.5,C.sub,'right',true);
    ['cu','mg'].forEach(k=>{ const M=MET[k], sp=slope(k); if(sp==null) return; const xe=Math.min(XM,YM/sp); ctx.strokeStyle=M.pt; ctx.lineWidth=1.8; ctx.setLineDash([6,4]); ctx.beginPath(); ctx.moveTo(px(0),py(0)); ctx.lineTo(px(xe),py(sp*xe)); ctx.stroke(); ctx.setLineDash([]); });
    recs.forEach(r=>{ const M=MET[r.k], X=px(r.m), Y=py(r.o); ctx.fillStyle=M.pt; if(r.k==='cu'){ ctx.fillRect(X-4,Y-4,8,8); } else { ctx.beginPath(); ctx.arc(X,Y,4.5,0,7); ctx.fill(); } });
    if(smp.done){ const X=px(smp.m), Y=py(r2(smp.reads[smp.n]-smp.reads[0])); ctx.strokeStyle='#f59e0b'; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(X,Y,8,0,7); ctx.stroke(); }
    if(!recs.length){ ctx.fillStyle='rgba(255,255,255,0.85)'; ctx.fillRect(X0+4,(Y0+Y1)/2-22,X1-X0-8,40); tx('一定になるまで加熱すると',(X0+X1)/2+2,(Y0+Y1)/2-6,10.5,C.sub,'center',true); tx('ここに点が記録されます',(X0+X1)/2+2,(Y0+Y1)/2+11,10.5,C.sub,'center',true); }
    [['cu',y+h-24],['mg',y+h-8]].forEach(q=>{ const k=q[0], M=MET[k], sp=slope(k), n=recs.filter(r=>r.k===k).length; ctx.fillStyle=M.pt; if(k==='cu') ctx.fillRect(x+12,q[1]-9,8,8); else { ctx.beginPath(); ctx.arc(x+16,q[1]-5,4.5,0,7); ctx.fill(); }
      tx(M.nm+(sp!=null?'：酸素＝'+ratioTxt(k,1,sp):(n?'（あと1点で直線）':'')),x+26,q[1],10.5,M.pt,'left',true); }); }
  function model(x,y,w,h){ const s=smp, M=MET[s.k], me=meas(s), fr=Math.min(1,me.o/(s.m*M.r)), nR=Math.min(12,2*Math.floor(6*fr+1e-6));
    panel(x,y,w,h); tx('原子のモデル　2'+M.sym+' ＋ O_2 → 2'+M.sym+'O',x+10,y+20,12.5,C.ink,'left',true);
    tx('空気中の酸素（分子）',x+14,y+42,10.5,C.sub,'left',true);
    for(let i=0;i<8;i++){ const ox=x+30+i*30, oy=y+59; if(i<8-nR/2){ atom(ox-5.5,oy,'O',0.85); atom(ox+5.5,oy,'O',0.85); } else { ctx.strokeStyle='#e2e8f0'; ctx.setLineDash([3,3]); ctx.beginPath(); ctx.arc(ox,oy,8,0,7); ctx.stroke(); ctx.setLineDash([]); } }
    tx(M.nm+'の原子（12こ）',x+14,y+86,10.5,C.sub,'left',true);
    for(let i=0;i<12;i++){ const col=i%6, row=Math.floor(i/6), ax=x+34+col*40, ay=y+106+row*34; if(i<nR) atom(ax+14,ay-5,'O',0.9); atom(ax,ay,M.sym,0.95); }
    const t0=x+288; [['結びついた'+M.nm+'原子：'+nR+'こ（12このうち）',C.ink,true],['結びついた酸素原子：'+nR+'こ（同じ数）',C.O,true],['原子1この質量の比は '+M.nm+'：酸素＝'+(s.k==='cu'?'4：1':'3：2'),C.ink,false],['→ 質量の比 '+M.nm+'：酸素＝'+M.a+'：'+M.b+' で結びつく',C.acc,true],[nR>=12?'全部結びつくと、それ以上は重くならない':(s.done?'中まで反応しきらなかった'+M.nm+'が残っている':'原子の数は変わらず、組み合わせが変わるだけ'),C.sub,true]]
      .forEach((l,i)=>tx(l[0],t0,y+42+i*24,11.5,l[1],'left',l[2])); }

  // ---------- ② 密閉した容器（質量保存） ----------
  function resetSeal(){ sl={r:0,lid:$('vessel').value==='closed',out:0,reacting:false,rows:[],f1:false,f2:false,f1lid:true}; bub=[]; }
  function stepSeal(dt){ const k=$('rx').value, R=RX[k]; if(sl.reacting){ sl.r=Math.min(1,sl.r+dt/2.4); if(sl.r>=1) sl.reacting=false; }
    const prod=sl.r*R.gas; if(!sl.lid&&prod>sl.out){ sl.out+=(prod-sl.out)*Math.min(1,dt*2.4); if(prod-sl.out<0.002) sl.out=prod; }
    const now=r2(R.m0-sl.out);
    if(sl.r>=1&&!sl.f1&&(sl.lid||prod-sl.out<0.002)){ sl.f1=true; sl.f1lid=sl.lid; sl.rows.push([sl.lid?'反応後（ふたをしたまま）':'反応後（ふたなし）',now]); }
    if(sl.f1&&sl.f1lid&&!sl.lid&&!sl.f2&&prod-sl.out<0.002){ sl.f2=true; sl.rows.push(['ふたを開けたあと',now]); }
    if(sl.reacting&&k==='gas'&&Math.random()<dt*30) bub.push({x:110+Math.random()*96,y:322,v:40+Math.random()*40,r:1.5+Math.random()*2.5});
    bub.forEach(b=>{ b.y-=b.v*dt; }); bub=bub.filter(b=>b.y>300); }
  function drawSeal(){ const k=$('rx').value, R=RX[k], gas=k==='gas', prod=sl.r*R.gas, inside=Math.max(0,prod-sl.out), now=r2(R.m0-sl.out), cx=158;
    panel(8,8,300,414); tx(gas?'炭酸水素ナトリウム ＋ うすい塩酸':'うすい硫酸 ＋ 水酸化バリウム水溶液',20,28,12.5,C.ink,'left',true);
    tx(gas?'気体（二酸化炭素）が発生する反応':'白い沈殿（硫酸バリウム）ができる反応',20,46,11,C.sub,'left',true);
    // 電子てんびん
    ctx.fillStyle='#e2e8f0'; rr(36,346,244,62,10); ctx.fill(); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1.2; ctx.stroke(); ctx.fillStyle='#94a3b8'; rr(64,334,188,12,4); ctx.fill();
    ctx.fillStyle='#1e293b'; rr(146,358,124,38,6); ctx.fill(); tx(fmt2(now)+' g',262,385,21,'#a7f3d0','right',true); tx('電子てんびん',50,383,11,'#334155','left',true);
    // 容器
    const sw=sl.lid&&gas?Math.min(4,inside/R.gas*4):0, L=cx-56-sw, Rr=cx+56+sw, T=176, B=330, lq=B-28;
    ctx.beginPath(); ctx.moveTo(cx-17,120); ctx.lineTo(cx-17,138); ctx.bezierCurveTo(cx-17,160,L,158,L,T); ctx.lineTo(L,B-10); ctx.quadraticCurveTo(L,B,L+10,B); ctx.lineTo(Rr-10,B); ctx.quadraticCurveTo(Rr,B,Rr,B-10); ctx.lineTo(Rr,T); ctx.bezierCurveTo(Rr,158,cx+17,160,cx+17,138); ctx.lineTo(cx+17,120);
    ctx.fillStyle='rgba(224,242,254,0.5)'; ctx.fill(); ctx.strokeStyle='#38bdf8'; ctx.lineWidth=2.2; ctx.stroke();
    // 中身
    const pour=Math.min(1,sl.r*5);
    if(gas){ if(pour>0){ ctx.fillStyle='rgba(125,211,252,0.55)'; rr(L+3,B-26*pour,Rr-L-6,26*pour-2,6); ctx.fill(); }
      if(sl.r<1){ ctx.fillStyle='#f8fafc'; ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1; ctx.beginPath(); ctx.ellipse(cx-26,B-6,26*(1-sl.r)+3,8*(1-sl.r)+2,0,Math.PI,2*Math.PI); ctx.fill(); ctx.stroke(); }
      bub.forEach(b=>{ ctx.strokeStyle='rgba(255,255,255,0.95)'; ctx.lineWidth=1.2; ctx.beginPath(); ctx.arc(b.x,b.y,b.r,0,7); ctx.stroke(); }); }
    else { const cl=clamp(sl.r*1.4,0,1); ctx.fillStyle='rgba(186,230,253,0.45)'; rr(L+3,B-28,Rr-L-6,26,6); ctx.fill();
      if(cl>0){ ctx.globalAlpha=cl; ctx.fillStyle='rgba(241,245,249,0.92)'; rr(L+3,B-28,Rr-L-6,26,6); ctx.fill(); ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1; ctx.stroke();
        ctx.fillStyle='#f8fafc'; rr(L+5,B-9,Rr-L-10,7,3); ctx.fill(); ctx.strokeStyle='#94a3b8'; ctx.stroke(); for(let i=0;i<46;i++) dot(L+9+((i*37)%(Rr-L-18)),B-24+((i*13)%14),1.5,'#94a3b8'); ctx.globalAlpha=1; } }
    // 小さい試験管（中の液を流しこむ）
    ctx.save(); ctx.translate(cx+30,B-8); ctx.rotate(-0.15-pour*1.2); ctx.fillStyle='rgba(255,255,255,0.7)'; ctx.strokeStyle='#7dd3fc'; ctx.lineWidth=1.6; rr(-8,-74,16,74,7); ctx.fill(); ctx.stroke();
    if(pour<1){ ctx.fillStyle=gas?'rgba(125,211,252,0.75)':'rgba(186,230,253,0.75)'; rr(-6.5,-40*(1-pour),13,40*(1-pour),6); ctx.fill(); } ctx.restore();
    if(sl.r<1){ if(gas){ tx('うすい塩酸',Rr+6,T+70,10.5,C.sub,'left',true); tx('炭酸水素',L-6,B-30,10.5,C.sub,'right',true); tx('ナトリウム',L-6,B-15,10.5,C.sub,'right',true); }
      else { tx('水酸化',Rr+6,T+62,10.5,C.sub,'left',true); tx('バリウム',Rr+6,T+77,10.5,C.sub,'left',true); tx('水溶液',Rr+6,T+92,10.5,C.sub,'left',true); tx('うすい',L-6,B-30,10.5,C.sub,'right',true); tx('硫酸',L-6,B-15,10.5,C.sub,'right',true); } }
    else if(!gas){ tx('白い沈殿',L-6,B-22,10.5,C.sub,'right',true); tx('（硫酸バリウム）',L-6,B-7,10,C.sub,'right',true); }
    // 二酸化炭素
    const nIn=gas?Math.round(10*inside/R.gas):0, nOut=gas?Math.round(10*sl.out/R.gas):0;
    for(let i=0;i<nIn;i++){ const ax=L+18+((i*47)%(Rr-L-36))+3*Math.sin(tNow*2+i), ay=T+6+((i*29)%(lq-T-20))+3*Math.cos(tNow*2.3+i*1.3); atom(ax-6,ay,'O',0.45); atom(ax+6,ay,'O',0.45); atom(ax,ay,'C',0.45); }
    for(let i=0;i<nOut;i++){ const ph=((tNow*18+i*7)%48), ax=cx+Math.sin(i*1.7+tNow*0.8)*(8+ph*0.9), ay=108-ph, al=clamp(1-ph/48,0,1); atom(ax-6,ay,'O',0.45,al); atom(ax+6,ay,'O',0.45,al); atom(ax,ay,'C',0.45,al); }
    // ふた（開けても電子てんびんの上に置く）
    if(sl.lid){ ctx.fillStyle='#0284c7'; rr(cx-20,106,40,18,4); ctx.fill(); ctx.strokeStyle='rgba(255,255,255,0.5)'; ctx.lineWidth=1; for(let i=-14;i<=14;i+=7){ ctx.beginPath(); ctx.moveTo(cx+i,109); ctx.lineTo(cx+i,121); ctx.stroke(); } tx('ふた',cx+26,119,10.5,'#0284c7','left',true); }
    else { ctx.fillStyle='#0284c7'; rr(222,320,30,14,4); ctx.fill(); tx('ふた',237,314,10.5,'#0284c7','center',true); }
    if(gas&&nOut>0) tag('二酸化炭素が出ていく',cx+28,84,11,C.sub,'left');
    if(sl.lid&&gas&&inside>0.05) tag('二酸化炭素は容器の中',cx,96,11,C.sub,'center');
    // 質量の記録
    panel(316,8,316,188); tx('質量の記録',328,28,12.5,C.ink,'left',true);
    const rows=[['反応前',R.m0]].concat(sl.rows); rows.forEach((r,i)=>{ const y=56+i*27; tx(r[0],330,y,12,C.ink,'left',true); tx(fmt2(r[1])+' g',616,y,13,C.ink,'right',true); ctx.strokeStyle=C.grid; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(328,y+9); ctx.lineTo(620,y+9); ctx.stroke(); });
    let msg=''; const d=r2(R.m0-now);
    if(sl.r<0.005) msg=sl.lid?'ふたをしたまま反応させると、質量はどうなるかな？':'ふたをしないで反応させると、質量はどうなるかな？';
    else if(!gas) msg='沈殿ができても、質量は変わらない';
    else if(d>0.004) msg='出ていった二酸化炭素の分（'+fmt2(d)+' g）だけ軽くなった';
    else msg='密閉しているので、反応の前後で質量は変わらない';
    tx(msg,474,178,11.5,d>0.004?C.O:C.acc,'center',true);
    // 原子のモデル
    panel(316,204,316,218); tx('原子のモデル（反応の前と後）',328,224,12.5,C.ink,'left',true);
    tx('反応前',330,258,11,C.sub,'left',true); tx('反応後',330,326,11,C.sub,'left',true);
    if(gas){ mol('NaHCO3',428,252); tx('NaHCO_3',428,290,10,C.sub,'center',true); tx('＋',474,258,15,C.sub,'center',true); mol('HCl',506,253); tx('HCl',506,290,10,C.sub,'center',true);
      mol('NaCl',398,320); tx('NaCl',398,351,10,C.sub,'center',true); tx('＋',428,326,15,C.sub,'center',true); mol('H2O',458,318); tx('H_2O',458,351,10,C.sub,'center',true); tx('＋',486,326,15,C.sub,'center',true);
      const esc=sl.out>0.004; mol('CO2',528,320,esc?0.4:1); tx('CO_2',528,351,10,C.sub,'center',true); if(esc){ arr(552,312,580,298,C.sub,1.6,4); tx('外へ',584,304,10.5,C.sub,'left',true); }
      atomTable(['Na','H','C','O','Cl'],[1,2,1,3,1]); }
    else { mol('H2SO4',410,252); tx('H_2SO_4',410,291,10,C.sub,'center',true); tx('＋',462,258,15,C.sub,'center',true); mol('BaOH2',530,253); tx('Ba(OH)_2',530,291,10,C.sub,'center',true);
      mol('BaSO4',412,322); tx('BaSO_4（沈殿）',412,354,10,C.sub,'center',true); tx('＋',466,326,15,C.sub,'center',true); mol('H2O',504,320); mol('H2O',556,320); tx('2H_2O',530,354,10,C.sub,'center',true);
      atomTable(['Ba','S','O','H'],[1,1,6,4]); } }
  function atomTable(els,n){ const y0=370, x0=400, dx=(620-x0)/els.length; tx('原子の数',330,y0,10.5,C.sub,'left',true); tx('反応前',330,y0+16,10.5,C.sub,'left',true); tx('反応後',330,y0+31,10.5,C.sub,'left',true);
    ctx.strokeStyle=C.grid; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(328,y0+5); ctx.lineTo(620,y0+5); ctx.stroke();
    els.forEach((e,i)=>{ const x=x0+dx*(i+0.5), c=EL[e][0]==='#ffffff'?'#334155':EL[e][0]; tx(e,x,y0,11.5,c,'center',true); tx(n[i]+'こ',x,y0+16,11,C.ink,'center',true); tx(n[i]+'こ',x,y0+31,11,C.ink,'center',true); });
    tx('種類も数も同じ → 質量の総和も同じ',474,415,11,C.acc,'center',true); }

  // ---------- 統計欄 ----------
  const fld=id=>{ const e=$(id); return e?e.closest('.field'):null; };
  const K=id=>$(id).previousElementSibling;
  function sh(id,m,sub){ const e=$(id); if(e) e.innerHTML=m+(sub?'<span style="display:block;font-size:12px;font-weight:700;color:#59616c;margin-top:2px">'+sub+'</span>':''); }
  function show(id,on){ const e=$(id); if(e) e.style.display=on?'':'none'; }
  function showF(id,on){ const e=fld(id); if(e) e.style.display=on?'':'none'; }
  function stats(){ if($('jk').value==='heat'){ const s=smp, M=MET[s.k], me=meas(s), rt=ratioTxt(s.k,s.m,me.o);
      K('sA').innerHTML='金属の質量（加熱前）'; sh('sA',fmt2(s.m)+' g',M.nm);
      K('sB').innerHTML='結びついた酸素'; sh('sB',fmt2(me.o)+' g',s.n?'加熱'+s.n+'回目のあと':'まだ加熱していない');
      K('sC').innerHTML=M.ox+'の質量'; sh('sC',fmt2(me.oxide)+' g',me.unr>0.004&&s.n?'反応していない'+M.nm+' '+fmt2(me.unr)+' g':(s.n?'すべて反応した':''));
      K('sD').innerHTML='質量の比（'+M.nm+'：酸素）'; sh('sD',s.done?rt:(s.n?'まだ途中':'加熱前'),s.done?fmt2(s.m)+' g：'+fmt2(me.o)+' g':'一定になるまで加熱しよう');
      if(s.done) setShare('【化学変化と質量】'+M.nm+fmt2(s.m)+' gを加熱すると、'+s.n+'回目で質量が'+fmt2(me.rd)+' gで一定になった。結びついた酸素は'+fmt2(me.o)+' g（'+M.nm+'：酸素＝'+rt+'）｜シミュラボ');
      else if(s.n) setShare('【化学変化と質量】'+M.nm+fmt2(s.m)+' gを'+s.n+'回加熱すると'+fmt2(me.rd)+' gに。結びついた酸素は'+fmt2(me.o)+' gで、反応していない'+M.nm+'は'+fmt2(me.unr)+' g｜シミュラボ');
      else setShare('【化学変化と質量】'+M.nm+'を加熱すると、'+M.nm+'：酸素＝'+M.a+'：'+M.b+'の質量の比で酸素と結びつき、'+M.ox+'になる｜シミュラボ'); }
    else { const k=$('rx').value, R=RX[k], gas=k==='gas', now=r2(R.m0-sl.out);
      K('sA').innerHTML='反応前の質量'; sh('sA',fmt2(R.m0)+' g','容器・ふたもふくめる');
      K('sB').innerHTML='いまの質量'; sh('sB',fmt2(now)+' g',sl.r<0.005?'まだ反応していない':(sl.out>0.004?'気体が出ていった':(gas?(sl.lid?'密閉しているので変わらない':'気体が出ていく'):'沈殿ができても変わらない')));
      K('sC').innerHTML='出ていった気体'; sh('sC',fmt2(sl.out)+' g',gas?'二酸化炭素':'気体は発生しない');
      K('sD').innerHTML='原子の数（反応の前と後）'; sh('sD','変わらない',gas?'Na・H・C・O・Cl':'Ba・S・O・H');
      setShare(gas?'【質量保存の法則】炭酸水素ナトリウム＋うすい塩酸：反応前'+fmt2(R.m0)+' g → いま'+fmt2(now)+' g'+(sl.out>0.004?'（二酸化炭素'+fmt2(sl.out)+' gが出ていった）':'（密閉していれば質量は変わらない）')+'｜シミュラボ'
        :'【質量保存の法則】うすい硫酸と水酸化バリウム水溶液を混ぜると白い沈殿ができるが、質量は'+fmt2(R.m0)+' gのまま変わらない｜シミュラボ'); } }
  function update(){ const heat=$('jk').value==='heat';
    showF('metal',heat); showF('mass',heat); showF('rx',!heat); showF('vessel',!heat);
    ['heat','auto','batch','clr','err'].forEach(id=>show(id,heat)); ['react','open','reset'].forEach(id=>show(id,!heat));
    $('err').textContent=noise?'誤差：あり':'誤差：なし'; $('open').textContent=sl.lid?'ふたを開ける':'ふたを閉める';
    stats(); }

  // ---------- 操作 ----------
  ['jk','metal','mass','rx','vessel'].forEach(k=>{ const el=$(k); if(!el||!Q.has(k)) return; const v=Q.get(k); if(el.tagName==='SELECT'&&![].some.call(el.options,o=>o.value===v)) return; el.value=v; el.dispatchEvent(new Event('input')); });
  if(Q.get('err')==='1') noise=true;
  newSample(); resetSeal();
  if(Q.get('batch')==='1') batch();
  for(let i=0;i<Math.min(12,+(Q.get('heat')||0));i++) applyHeat();
  if(Q.get('seal')==='done'||Q.get('seal')==='open'){ sl.r=1; stepSeal(0); if(Q.get('seal')==='open'){ sl.lid=false; sl.out=RX[$('rx').value].gas; stepSeal(0); } }
  $('jk').addEventListener('change',update);
  $('metal').addEventListener('change',()=>{ newSample(); update(); });
  $('mass').addEventListener('input',()=>{ newSample(); update(); });
  ['rx','vessel'].forEach(id=>$(id).addEventListener('change',()=>{ resetSeal(); update(); }));
  $('heat').addEventListener('click',()=>{ if(heatT===0){ heatT=HEAT; autoRun=false; } });
  $('auto').addEventListener('click',()=>{ if(!smp.done){ autoRun=true; if(heatT===0) heatT=HEAT; } });
  $('batch').addEventListener('click',()=>{ batch(); update(); });
  $('clr').addEventListener('click',()=>{ recs=[]; update(); });
  $('err').addEventListener('click',()=>{ noise=!noise; newSample(); update(); });
  $('react').addEventListener('click',()=>{ if(sl.r<1) sl.reacting=true; });
  $('open').addEventListener('click',()=>{ sl.lid=!sl.lid; update(); });
  $('reset').addEventListener('click',()=>{ resetSeal(); update(); });
  cv.addEventListener('pointerdown',e=>{ const p=cpos(cv,e), x=p[0]/dpr, y=p[1]/dpr;
    if($('jk').value==='heat'){ if(x<214&&y>110&&y<254&&heatT===0){ heatT=HEAT; autoRun=false; } return; }
    if(x>130&&x<186&&y>100&&y<128){ sl.lid=!sl.lid; update(); } else if(x>96&&x<222&&y>130&&y<332&&sl.r<1){ sl.reacting=true; } });
  function frame(t){ const dt=last?Math.min(0.05,(t-last)/1000):0; last=t; tNow+=dt; const heat=$('jk').value==='heat';
    if(heatT>0){ heatT-=dt; if(heatT<=0){ heatT=0; applyHeat(); if(autoRun&&!smp.done) heatT=HEAT; else autoRun=false; stats(); } }
    if(!heat) stepSeal(dt);
    ctx.fillStyle=C.bg; ctx.fillRect(0,0,W,H);
    if(heat){ apparatus(8,8,206,246); graph1(220,8,204,246); graph2(430,8,202,246); model(8,262,624,160); } else drawSeal();
    stT+=dt; if(!heat&&stT>0.2){ stT=0; stats(); }
    requestAnimationFrame(frame); }
  update(); frame(performance.now());
'''

KAGAKU_ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
<p>化学変化の前後で、物質全体の質量は変わりません（<b>質量保存の法則</b>）。原子の組み合わせが変わるだけで、原子の種類と数は変わらないからです。気体が発生する反応でも、密閉した容器の中なら質量は変わらず、ふたを開けると出ていった気体の分だけ軽くなります。また、金属を加熱すると空気中の酸素と結びついて質量が増えますが、結びつく酸素の質量には限度があり、加熱をくり返すと質量は一定になります。金属の質量と結びつく酸素の質量は比例し、<b>銅：酸素＝4：1</b>、<b>マグネシウム：酸素＝3：2</b>の質量の比で結びつきます。</p>
''' + N("対応する単元：中学校第2学年 第1分野（4）化学変化と原子・分子 ア（ウ）化学変化と物質の質量（化学変化と質量の保存、質量変化の規則性）") + '''
<h2>授業での使い方</h2>
<h3>導入：質量は変わる？変わらない？</h3>
<p>「② 密閉した容器の反応」で、炭酸水素ナトリウムとうすい塩酸を、ふたをした容器の中で反応させるとき、電子てんびんの値がどうなるかを予想させます。反応させても値は変わらず、ふたを開けると二酸化炭素が出ていって軽くなることを確かめ、「質量が減ったのは、物質がなくなったからではなく、気体として外へ出ていったから」と気づかせます。沈殿ができる反応（うすい硫酸と水酸化バリウム水溶液）では、ふたを開けても質量が変わらないことも比べられます。</p>
<h3>展開：加熱をくり返してグラフにする</h3>
<p>「① 金属を加熱する」で金属と質量を選び、「🔥 加熱する」をくり返し押します。質量は増えていきますが、増え方がだんだん小さくなり、やがて一定になります。一定になると、右のグラフに「金属の質量」と「結びついた酸素の質量」の点が記録されます。金属の質量を変えて何回か実験し（または「📊 まとめて実験」）、点が原点を通る直線の上に並ぶことから、金属と酸素が一定の割合で結びつくことを見いださせます。「誤差：なし」のボタンを押して「誤差：あり」にすると、実際の実験のように点が少しずれるので、直線の引き方や誤差の考え方を話し合う材料になります。</p>
<h3>まとめ：原子のモデルで説明する</h3>
<p>下の原子のモデルで、銅原子と酸素原子が1こずつ結びつくこと、すべての銅原子が酸素と結びつくとそれ以上は重くならないことを確かめます。銅原子1この質量が酸素原子1この約4倍なので、質量の比が銅：酸素＝4：1になることにつなげます。</p>
<p><b>生徒への問いの例</b></p>
<ol>
<li>ふたをした容器の中で炭酸水素ナトリウムとうすい塩酸を反応させたあと、ふたを開けると質量が減るのはなぜでしょう。</li>
<li>銅の粉末を加熱しても、質量がある値より大きくならないのはなぜでしょう。原子のモデルを使って説明しましょう。</li>
<li>銅1.2 gを加熱したら、質量が1.4 gになりました。まだ酸素と結びついていない銅は何gでしょう。（答え：0.4 g）</li>
</ol>
<h2>しくみ・解説</h2>
<h3>質量保存の法則</h3>
<p>化学変化では、原子の組み合わせが変わって別の物質ができますが、原子そのものがなくなったり、新しくできたりすることはありません。反応の前後で原子の種類と数が同じなので、反応に関係する物質全体の質量（質量の総和）は変わりません。これを<b>質量保存の法則</b>といいます。状態変化（とける・沸騰するなど）でも質量は変わりません。</p>
''' + N("炭酸水素ナトリウム＋塩酸 → 塩化ナトリウム＋水＋二酸化炭素<br>NaHCO<sub>3</sub>＋HCl → NaCl＋H<sub>2</sub>O＋CO<sub>2</sub>") + T([["反応前（NaHCO<sub>3</sub>＋HCl）", "1こ", "2こ", "1こ", "3こ", "1こ"], ["反応後（NaCl＋H<sub>2</sub>O＋CO<sub>2</sub>）", "1こ", "2こ", "1こ", "3こ", "1こ"]],
         ["", "Na", "H", "C", "O", "Cl"]) + '''
<h3>密閉した容器と、ふたを開けた容器</h3>
''' + T([["ふたをしたまま反応させる", "82.46 g", "82.46 g", "変わらない（二酸化炭素は容器の中にある）"], ["そのあと、ふたを開ける", "82.46 g", "81.94 g", "二酸化炭素0.52 gが出ていった"], ["はじめからふたをしない", "82.46 g", "81.94 g", "発生した二酸化炭素がそのまま出ていく"], ["沈殿ができる反応（硫酸＋水酸化バリウム）", "96.35 g", "96.35 g", "気体が出ないので、ふたを開けても変わらない"]],
         ["実験", "反応前", "反応後", "わけ"]) + '''
<p>表の値はこのシミュレーションの例です（炭酸水素ナトリウム1.00 gと十分な量のうすい塩酸を、容器・ふたごとはかった値）。炭酸水素ナトリウム1.00 gから発生する二酸化炭素は、化学反応式から 1.00×44÷84≒0.52 g と計算できます。開いた容器で質量が減っても、出ていった気体の質量まで合わせれば、質量の総和は変わっていません。</p>
<h3>金属を加熱したときの質量の変化</h3>
<p>銅やマグネシウムの粉末をステンレス皿に入れて加熱すると、空気中の酸素と結びついて酸化銅（黒色）や酸化マグネシウム（白色）になり、結びついた酸素の分だけ質量が増えます。粉末をよくかき混ぜて加熱と質量の測定をくり返すと、増え方はしだいに小さくなり、やがて質量が変わらなくなります。金属がすべて酸素と結びつくと、それ以上は酸素と結びつかないからです。</p>
''' + T([["0回（加熱前）", "0.80 g", "0.60 g"], ["1回", "0.94 g", "0.92 g"], ["2回", "0.98 g", "0.98 g"], ["3回", "0.99 g", "1.00 g"], ["4回", "1.00 g", "1.00 g（一定）"], ["5回", "1.00 g（一定）", "—"]],
         ["加熱した回数", "銅 0.80 g", "マグネシウム 0.60 g"]) + '''
<p>表はこのシミュレーションのモデルの値です（1回の加熱で、残っている金属のうち銅は7割、マグネシウムは8割が反応するとしています）。</p>
<h3>金属の質量と結びつく酸素の質量（比例のグラフ）</h3>
''' + T([["0.40 g", "0.10 g", "0.50 g"], ["0.80 g", "0.20 g", "1.00 g"], ["1.20 g", "0.30 g", "1.50 g"], ["2.00 g", "0.50 g", "2.50 g"]], ["銅", "結びつく酸素", "酸化銅"]) + T([["0.30 g", "0.20 g", "0.50 g"], ["0.60 g", "0.40 g", "1.00 g"], ["0.90 g", "0.60 g", "1.50 g"], ["1.20 g", "0.80 g", "2.00 g"]], ["マグネシウム", "結びつく酸素", "酸化マグネシウム"]) + '''
<p>金属の質量を横軸、結びつく酸素の質量を縦軸にとると、点は原点を通る直線の上に並びます（比例）。直線の傾きから、<b>銅：酸素＝4：1</b>（銅：酸化銅＝4：5）、<b>マグネシウム：酸素＝3：2</b>（マグネシウム：酸化マグネシウム＝3：5）がわかります。</p>
<h3>原子のモデルで考える</h3>
''' + N("2Cu＋O<sub>2</sub> → 2CuO（銅原子1こと酸素原子1こが結びつく）<br>2Mg＋O<sub>2</sub> → 2MgO（マグネシウム原子1こと酸素原子1こが結びつく）") + '''
<p>どちらも金属原子と酸素原子が1：1の数の割合で結びつきます。原子1この質量は、銅原子が酸素原子の約4倍、マグネシウム原子が酸素原子の約1.5倍なので、質量の比はそれぞれ銅：酸素＝4：1、マグネシウム：酸素＝3：2（＝1.5：1）になります。</p>
<h3>計算問題の解き方（例題）</h3>
<p><b>例題1</b>　銅2.0 gを完全に酸化させると、酸化銅は何gできるか。<br>銅：酸素＝4：1 より、結びつく酸素は 2.0×1/4＝0.5 g。酸化銅は 2.0＋0.5＝<b>2.5 g</b>（銅：酸化銅＝4：5 から 2.0×5/4 と求めてもよい）。</p>
<p><b>例題2（反応していない銅が残る問題）</b>　銅1.2 gを加熱したところ、加熱後の質量は1.4 gになった。まだ酸素と結びついていない銅は何gか。<br>増えた質量が結びついた酸素なので 1.4－1.2＝0.2 g。0.2 gの酸素と結びついた銅は 0.2×4＝0.8 g。結びついていない銅は 1.2－0.8＝<b>0.4 g</b>。このときできた酸化銅は 0.8＋0.2＝1.0 g です。</p>
<p><b>例題3</b>　マグネシウム0.9 gを完全に酸化させると、酸化マグネシウムは何gできるか。また、酸化マグネシウムを2.0 g得るには、マグネシウムは何g必要か。<br>マグネシウム：酸化マグネシウム＝3：5 より、0.9×5/3＝<b>1.5 g</b>。2.0 g得るには 2.0×3/5＝<b>1.2 g</b>。</p>
<p><b>例題4</b>　同じ質量の酸素と結びつく銅とマグネシウムの質量の比はいくらか。<br>酸素1 gと結びつくのは、銅4 g、マグネシウム1.5 g。よって銅：マグネシウム＝4：1.5＝<b>8：3</b>。</p>
<p><b>例題5（発展）</b>　銅とマグネシウムの混合物3.0 gを完全に酸化させると、4.5 gになった。混合物中の銅は何gか。<br>銅を x g、マグネシウムを（3.0－x）g とすると、結びついた酸素は x/4＋（3.0－x）×2/3＝4.5－3.0＝1.5。これを解くと x＝1.2。銅<b>1.2 g</b>、マグネシウム1.8 g。</p>
<h3>関連：酸化と還元でも質量は保存される</h3>
<p>酸化銅と炭素の粉末を混ぜて加熱すると、酸化銅は酸素をうばわれて銅にもどり（還元）、炭素は酸化されて二酸化炭素になります（2CuO＋C → 2Cu＋CO<sub>2</sub>）。たとえば酸化銅2.00 gと炭素0.15 gが過不足なく反応すると、銅1.60 gと二酸化炭素0.55 gができ、2.00＋0.15＝1.60＋0.55 で質量の総和は変わりません。試験管の中の質量が減るのは、二酸化炭素が外へ出ていくからです。</p>
<h3>このシミュレーションで単純化していること</h3>
<ul>
<li>質量の比は教科書の値（銅：酸素＝4：1、マグネシウム：酸素＝3：2）で計算しています。原子の質量（原子量）から計算すると、銅：酸素＝3.97：1、マグネシウム：酸素＝3：1.97 です（高校の化学で学びます）。</li>
<li>加熱1回で反応する割合（銅7割、マグネシウム8割）と、電子てんびんの値（0.01 gの位まで）はモデルです。「誤差：あり」では、粉末の中まで反応しきらない分（銅で2〜10％、マグネシウムで1〜6％）と、0.01 gの測定のずれを入れています。実際の実験では、マグネシウムが空気中の窒素とも反応したり、加熱中に粉末が飛び散ったりして、比がずれることがあります。</li>
<li>密閉した容器の実験では、炭酸水素ナトリウム1.00 gと十分な量のうすい塩酸を使い、発生した二酸化炭素0.52 gがふたを開けると全部出ていくとしています。実際には、二酸化炭素の一部が水にとけて残るため、減る質量は計算より少し小さくなります。また、容器がふくらむことによる浮力の変化は考えていません。</li>
<li>原子のモデルの原子の数（12こ）や大きさ・色は模式的なものです。</li>
</ul>
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「中学校学習指導要領（平成29年告示）解説 理科編」第1分野（4）化学変化と原子・分子（ウ）化学変化と物質の質量　''' + A(MEXT_CHU, "中学校学習指導要領解説") + '''</li>
<li>中学校理科の教科書（第2学年「化学変化と原子・分子」の単元）</li>
<li>日本化学会 原子量専門委員会「原子量表」（原子量 Cu 63.55、Mg 24.31、O 16.00、C 12.01、Na 22.99）</li>
</ul>
'''

sim(slug="kagaku-shitsuryou", cat="rika", emoji="🧪", score=80,
    title="化学変化と質量シミュレーター（銅・マグネシウムの酸化）",
    title_tag="質量保存の法則・化学変化と質量のシミュレーター｜銅とマグネシウムの酸化（4：1、3：2）と計算問題",
    meta_desc="質量保存の法則（密閉した容器では質量が変わらず、ふたを開けると気体の分だけ軽くなる）と、銅・マグネシウムの加熱による質量の変化や酸素との質量の比（4：1、3：2）を、グラフと原子のモデルで確かめる中2理科の無料シミュレーター。例題つき。",
    og_title="化学変化と質量シミュレーター（銅・マグネシウムの酸化）",
    og_desc="質量保存の法則と、銅・マグネシウムの酸化での質量の比（4：1、3：2）を、加熱のグラフと原子のモデルで確かめる。中2の授業向け。",
    card_desc="加熱をくり返すと質量は一定に。銅：酸素＝4：1、マグネシウム：酸素＝3：2をグラフと原子のモデルで確かめる。",
    lead="銅やマグネシウムを加熱して、質量が一定になるまでのグラフと、金属と結びつく酸素の質量の比例のグラフを作れます。密閉した容器の反応では、質量が変わらず、ふたを開けると気体の分だけ軽くなることを原子のモデルとあわせて確かめられます。",
    model="中2 化学変化と物質の質量（質量保存の法則・質量変化の規則性）",
    level="中学2年",
    unit="中学校 第1分野（4）化学変化と原子・分子 ア（ウ）化学変化と物質の質量",
    canvas=canvas(640, 430, light=True),
    controls=select("jk", "実験", [("heat", "① 金属を加熱する（質量の比）"), ("seal", "② 密閉した容器の反応（質量保存）")])
           + select("metal", "金属", [("cu", "銅"), ("mg", "マグネシウム")])
           + slider("mass", "金属の質量", 0.2, 1.5, 0.8, 0.05, "{v} g")
           + select("rx", "反応", [("gas", "炭酸水素ナトリウム＋うすい塩酸"), ("ppt", "うすい硫酸＋水酸化バリウム水溶液")])
           + select("vessel", "容器", [("closed", "ふたをして密閉する"), ("open", "ふたをしない")]),
    buttons=btn("heat", "🔥 加熱する", True) + btn("auto", "⏩ 一定になるまで") + btn("batch", "📊 まとめて実験")
           + btn("clr", "記録を消す") + btn("err", "誤差：なし")
           + btn("react", "⚗ 反応させる", True) + btn("open", "ふたを開ける") + btn("reset", "⏮ はじめから"),
    stats=stats([("sA", "金属の質量", False), ("sB", "結びついた酸素", True), ("sC", "酸化物の質量", False), ("sD", "質量の比", False)]),
    legend="①：左＝ステンレス皿の加熱と電子てんびんの値、中＝加熱した回数と質量のグラフ、右＝金属の質量と結びついた酸素の質量のグラフ（質量が一定になると点が記録されます）、下＝原子のモデル。②：容器ごと電子てんびんにのせてはかります。ふたを開けても、ふたは電子てんびんの上に置いています。",
    article=KAGAKU_ARTICLE,
    faqs=[("質量保存の法則とは何ですか？", "化学変化の前後で、反応に関係する物質全体の質量が変わらないというきまりです。化学変化では原子の組み合わせが変わるだけで、原子の種類と数は変わらないため、質量の総和も変わりません。"),
          ("気体が発生する反応で、ふたを開けると質量が減るのはなぜですか？", "発生した気体（炭酸水素ナトリウムと塩酸の反応では二酸化炭素）が容器の外へ出ていくからです。密閉したままなら質量は変わりません。出ていった気体の質量を合わせれば、質量の総和は反応の前後で同じです。"),
          ("銅を加熱し続けても、質量が一定になるのはなぜですか？", "銅がすべて酸素と結びついて酸化銅になると、それ以上は酸素と結びつかないからです。一定の質量の銅と結びつく酸素の質量には限度があり、その限度は銅の質量に比例します。"),
          ("銅と酸素が4：1の質量の比で結びつくのはなぜですか？", "銅原子と酸素原子は1こずつ結びつき（2Cu＋O₂→2CuO）、銅原子1この質量が酸素原子1この約4倍だからです。マグネシウム原子は酸素原子の約1.5倍の質量なので、マグネシウム：酸素＝1.5：1＝3：2になります。"),
          ("反応していない銅の質量はどうやって求めますか？", "まず「加熱後の質量－加熱前の質量」で結びついた酸素の質量を求め、それを4倍して酸素と結びついた銅の質量を出します。はじめの銅の質量からそれを引いた値が、反応していない銅の質量です。例：銅1.2 gが1.4 gになったら、酸素0.2 g、結びついた銅0.8 g、反応していない銅0.4 g。"),
          ("スチールウールを燃やすと重くなるのは、質量保存の法則に反しませんか？", "反しません。鉄が空気中の酸素と結びついて酸化鉄になるため、結びついた酸素の分だけ重くなります。反応した酸素の質量まで合わせれば、反応の前後で質量の総和は変わりません。")],
    rel=[("joutai-henka", "🧊", "状態変化と粒子のシミュレーター"), ("diffusion", "🫧", "拡散シミュレーター"), ("shitsudo-roten", "☁️", "湿度と雲のでき方シミュレーター"), ("coffee-milk", "☕", "コーヒーにミルクを落とすと")],
    js=JS_KAGAKU)
