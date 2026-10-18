# -*- coding: utf-8 -*-
"""理科の授業向けシミュ（小学4年）
   hone-kinniku  … 小4「人の体のつくりと運動」（B（1））：ほね・きん肉・関節
   amamizu-yukue … 小4「雨水の行方と地面の様子」（B（3））：地面のかたむきと水の流れ・土のつぶとしみこみ方"""
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

MEXT_SHO = "https://www.mext.go.jp/a_menu/shotou/new-cs/1387014.htm"
JMA_AME = "https://www.jma.go.jp/jma/kishou/know/yougo_hp/amehyo.html"
def A(url, label): return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, label)
def FULL(html): return html.replace('<div class="field">', '<div class="field" style="grid-column:1/-1">', 1)
def TABS(html): return '<div class="lab-btns" style="grid-column:1/-1;margin:0 0 2px;">' + html + '</div>'

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
  const V=(x,y)=>({x:x,y:y}), ad=(a,b,k)=>V(a.x+b.x*(k==null?1:k),a.y+b.y*(k==null?1:k)), dst=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y);
  function ln(a,b){ ctx.beginPath(); ctx.moveTo(a.x,a.y); ctx.lineTo(b.x,b.y); ctx.stroke(); }
  const KIN='、。」）・！？ーっゃゅょ';
  function wrap(s,x,y,maxW,size,col,lh,bold){ let line='', yy=y; for(const ch of s){ if(ch==='\n'){ tx(line,x,yy,size,col,'left',bold); line=''; yy+=lh; continue; }
      if(line && tw(line+ch,size,bold)>maxW && KIN.indexOf(ch)<0){ tx(line,x,yy,size,col,'left',bold); line=ch; yy+=lh; } else line+=ch; }
    if(line){ tx(line,x,yy,size,col,'left',bold); yy+=lh; } return yy; }
  function setTab(ids,cur){ ids.forEach(id=>{ const e=$(id); if(!e) return; e.classList.toggle('btn-primary',id===cur); e.classList.toggle('btn-ghost',id!==cur); }); }
'''

# ============================================================ 1 ほねときん肉
JS_HONE = HELP + r'''
  const C={bg:'#f8fafc',ink:'#0f172a',sub:'#64748b',grid:'#e2e8f0',skin:'#fde4cc',skinL:'#d9a877',bone:'#fbf8ef',boneL:'#a8a29e',red:'#dc2626',pale:'#fbb6c1',tend:'#f5f5f4',joint:'#16a34a',sel:'#fde047',selL:'#ca8a04',relax:'#64748b',fur:'#eadccd',furL:'#a8927d'};
  const LX=8, LW=390, RX=406, RW=226, PY=8, PH=454;
  let mode='arm', ang=90, dir=1, cin=1, auto=false, aph=0, wt=false, moveT=0, drag=null, tNow=0, last=0, lastKey='', HIT=[];
  let selB=null, found={}, reveal=false, qmsg='体の曲がるところを、指でタップしてさがそう。', qlast='';
  let hs=0, hop=false, hph=0, hAct=0, view='both';

  function segD(p,a,b){ const dx=b.x-a.x, dy=b.y-a.y, l2=dx*dx+dy*dy; let t=l2?((p.x-a.x)*dx+(p.y-a.y)*dy)/l2:0; t=clamp(t,0,1); return Math.hypot(p.x-a.x-dx*t,p.y-a.y-dy*t); }
  function boneSeg(a,b,w,fill,ol){ ctx.lineCap='round'; ctx.strokeStyle=ol||C.boneL; ctx.lineWidth=w+2.4; ln(a,b); dot(a.x,a.y,w*0.72+1.2,ol||C.boneL); dot(b.x,b.y,w*0.72+1.2,ol||C.boneL);
    ctx.strokeStyle=fill||C.bone; ctx.lineWidth=w; ln(a,b); dot(a.x,a.y,w*0.72,fill||C.bone); dot(b.x,b.y,w*0.72,fill||C.bone); }
  function tendon(a,b){ ctx.lineCap='round'; ctx.strokeStyle='#a8a29e'; ctx.lineWidth=5; ln(a,b); ctx.strokeStyle=C.tend; ctx.lineWidth=3; ln(a,b); }
  function spindle(P1,P2,hw,col,t1,t2){ const L=dst(P1,P2), d=V((P2.x-P1.x)/L,(P2.y-P1.y)/L), n=V(-d.y,d.x), Q1=ad(P1,d,t1), Q2=ad(P2,d,-t2), M=V((Q1.x+Q2.x)/2,(Q1.y+Q2.y)/2);
    if(t1>0) tendon(P1,ad(Q1,d,6)); if(t2>0) tendon(ad(Q2,d,-6),P2);
    ctx.fillStyle=col; ctx.strokeStyle='rgba(127,29,29,.55)'; ctx.lineWidth=1.3; ctx.beginPath(); ctx.moveTo(Q1.x,Q1.y); ctx.quadraticCurveTo(M.x+n.x*hw*2,M.y+n.y*hw*2,Q2.x,Q2.y); ctx.quadraticCurveTo(M.x-n.x*hw*2,M.y-n.y*hw*2,Q1.x,Q1.y); ctx.closePath(); ctx.fill(); ctx.stroke();
    ctx.strokeStyle='rgba(255,255,255,.4)'; ctx.lineWidth=1; for(let k=-1;k<=1;k++){ const o=k*hw*0.5; ctx.beginPath(); ctx.moveTo(Q1.x,Q1.y); ctx.quadraticCurveTo(M.x+n.x*o*2,M.y+n.y*o*2,Q2.x,Q2.y); ctx.stroke(); }
    return M; }
  function lbl(lines,x,y,w,col,to,hit){ const h=8+lines.length*17; ctx.fillStyle='rgba(255,255,255,.96)'; ctx.strokeStyle=col; ctx.lineWidth=1.6; rr(x,y,w,h,7); ctx.fill(); ctx.stroke();
    if(to){ ctx.strokeStyle=col; ctx.lineWidth=1.4; const sx=to.x>x+w?x+w:(to.x<x?x:x+w/2), sy=to.y>y+h?y+h:(to.y<y?y:y+h/2); ln(V(sx,sy),to); dot(to.x,to.y,3,col); }
    lines.forEach((L,i)=>tx(L[0],x+8,y+19+i*17,L[1]||12.5,L[2]||col,'left',true)); if(hit) HIT.push({x:x,y:y,w:w,h:h,k:hit}); }
  function jring(P,r,col,dash){ ctx.strokeStyle=col; ctx.lineWidth=2.2; if(dash) ctx.setLineDash([5,4]); ctx.beginPath(); ctx.arc(P.x,P.y,r,0,7); ctx.stroke(); ctx.setLineDash([]); }

  // ================= うでの曲げのばし =================
  const S=V(150,86), E=V(150,254), LF=140;
  function armG(a){ const p=(180-a)*Math.PI/180, f=V(Math.sin(p),Math.cos(p)), n=V(f.y,-f.x); return {f:f,n:n,Wr:ad(E,f,LF)}; }
  function setAng(a){ a=clamp(a,45,180); if(Math.abs(a-ang)>0.25){ dir=a<ang?1:-1; moveT=0.7; } ang=a; $('ang').value=Math.round(ang); $('angL').textContent=Math.round(ang)+'°'; }
  function drawArm(){ panel(LX,PY,LW,PH); const g=armG(ang), f=g.f, n=g.n, Wr=g.Wr, gb=(180-ang)/135;
    // 皮ふ（かた・うで・手）
    ctx.lineCap='round'; ctx.lineJoin='round';
    const skin=(c,ex)=>{ ctx.fillStyle=c; ctx.beginPath(); ctx.ellipse(S.x-4,S.y-24,52+ex/2,32+ex/2,0,0,7); ctx.fill(); ctx.strokeStyle=c; ctx.lineWidth=70+ex; ln(V(S.x,S.y-14),E); ctx.lineWidth=56+ex; ln(E,Wr); };
    skin(C.skinL,3); skin(C.skin,0);
    ctx.save(); ctx.translate(Wr.x,Wr.y); ctx.rotate(Math.atan2(f.y,f.x)); ctx.fillStyle=C.skin; ctx.strokeStyle=C.skinL; ctx.lineWidth=2;
    ctx.beginPath(); ctx.ellipse(30,0,30,22,0,0,7); ctx.fill(); ctx.stroke(); ctx.beginPath(); ctx.ellipse(18,-21,13,8,-0.5,0,7); ctx.fill(); ctx.stroke();
    if(wt){ ctx.fillStyle='#475569'; rr(26,-34,8,68,3); ctx.fill(); ctx.fillStyle='#334155'; rr(18,-46,24,16,4); ctx.fill(); rr(18,30,24,16,4); ctx.fill(); }
    ctx.restore();
    tx('✋ 手を指で動かそう',18,30,12.5,'#0e7490','left',true);
    // ほね
    ctx.fillStyle=C.bone; ctx.strokeStyle=C.boneL; ctx.lineWidth=1.3; ctx.beginPath(); ctx.moveTo(S.x-38,S.y-30); ctx.lineTo(S.x-8,S.y-16); ctx.lineTo(S.x-32,S.y+34); ctx.closePath(); ctx.fill(); ctx.stroke();
    boneSeg(V(S.x,S.y+2),V(E.x,E.y-8),14);
    const e1=ad(E,f,10), w1=ad(Wr,f,-2); boneSeg(ad(e1,n,4.5),ad(w1,n,5),7); boneSeg(ad(e1,n,-4.5),ad(w1,n,-5),7);
    // きん肉（内側＝うでの前がわ、外側＝うでの後ろがわ）
    const Oi=V(S.x+16,S.y+20), Ii=ad(ad(E,f,34),n,9), Li=dst(Oi,Ii), Li0=dst(Oi,V(E.x+9,E.y+34));
    const Oo=V(S.x-17,S.y+20), Bo=V(S.x-17,E.y-30+gb*10), Io=ad(ad(E,n,-12),f,-5);
    const hwI=7+7*cin+(1-Li/Li0)*9+(wt?3*cin:0), hwO=7+7*(1-cin)-gb*2;
    const Mo=spindle(Oo,Bo,hwO,mix(C.pale,C.red,1-cin),10,0); tendon(Bo,Io);
    const Mi=spindle(Oi,Ii,hwI,mix(C.pale,C.red,cin),10,12);
    // 関節
    jring(E,21,C.joint,true); jring(S,17,C.joint,true);
    if(wt){ const pc=ad(Wr,f,30); tag('おもり',pc.x+n.x*62,pc.y+n.y*62+5,11,'#334155','center'); }
    if(moveT>0){ const tip=ad(Wr,f,66); arrow(tip.x,tip.y,tip.x+n.x*dir*34,tip.y+n.y*dir*34,'#0e7490',3.2,5.5); }
    // ラベル
    const on=cin>0.5;
    lbl([['内側のきん肉',12.5,C.ink],[on?'ちぢむ':'ゆるむ',16,on?C.red:C.relax]],262,22,112,on?C.red:'#94a3b8',Mi);
    lbl([['外側のきん肉',12.5,C.ink],[on?'ゆるむ':'ちぢむ',16,on?C.relax:C.red]],16,124,98,on?'#94a3b8':C.red,Mo);
    lbl([['ほね',12.5,C.ink],['かたい',12,C.sub]],16,200,98,'#a8a29e',V(S.x-2,184));
    lbl([['関節（ひじ）',12.5,C.joint],['曲がるところ',12,C.sub]],16,280,98,C.joint,V(E.x-21,E.y+4));
  }
  function infoArm(){ panel(RX,PY,RW,PH); const x=RX+12, xr=RX+RW-12, on=cin>0.5;
    tx(dir>0?'うでを曲げるとき':'うでをのばすとき',x,34,15.5,C.ink,'left',true);
    tx('ひじの角度',x,62,12,C.sub,'left',true); tx(Math.round(ang)+'°',xr,66,24,C.ink,'right',true);
    ctx.fillStyle='#e2e8f0'; rr(x,76,xr-x,10,5); ctx.fill(); ctx.fillStyle='#0e7490'; rr(x,76,Math.max(10,(xr-x)*(180-ang)/135),10,5); ctx.fill();
    tx('のばす',x,100,10.5,C.sub,'left',true); tx('曲げる',xr,100,10.5,C.sub,'right',true);
    const row=(y,nm,a)=>{ ctx.fillStyle=a?C.red:C.pale; rr(x,y-13,16,16,4); ctx.fill(); tx(nm,x+22,y,13,C.ink,'left',true); tx(a?'ちぢむ':'ゆるむ',xr,y+1,16,a?C.red:C.relax,'right',true);
      tx(a?'太く、かたくなる':'のびて、やわらかい',x+22,y+18,11,C.sub,'left',true); };
    row(134,'内側のきん肉',on); row(180,'外側のきん肉',!on);
    ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; ln(V(x,208),V(xr,208));
    let y=wrap('きん肉は、ちぢんでほねを引っぱり、体を動かします。曲げるときは内側、のばすときは外側のきん肉がちぢみます。',x,230,RW-24,12.5,C.ink,19);
    y=wrap('ほねとほねのつなぎ目で、曲がるところを関節といいます。',x,y+8,RW-24,12.5,C.joint,19,true);
    ctx.fillStyle='#ecfeff'; rr(x-4,y+6,RW-16,PY+PH-y-16,8); ctx.fill();
    wrap(wt?'おもりを持つと、内側のきん肉がもっと太く、かたくなります。自分のうででもたしかめよう。':'さわってみよう：うでを曲げて力を入れると、内側のきん肉がかたくふくらむよ。',x+2,y+28,RW-28,12.5,'#0e7490',19,true);
  }

  // ================= 全身のほね（前から見た図） =================
  const J={neck:V(200,106),waist:V(200,238),shL:V(146,126),shR:V(254,126),elL:V(132,204),elR:V(268,204),wrL:V(124,268),wrR:V(276,268),fiL:V(119,296),fiR:V(281,296),hiL:V(181,284),hiR:V(219,284),knL:V(177,368),knR:V(223,368),anL:V(176,436),anR:V(224,436)};
  const BN={head:{nm:'頭のほね',w:['のう（脳）を守る'],g:[1],tip:'頭をさわると、かたいほねがあるね。'},
    spine:{nm:'せぼね',w:['体をささえる','小さなほねがたくさんつながっていて、体を曲げたりひねったりできる'],g:[0,2],tip:'せなかのまん中をさわると、でこぼこしたほねがならんでいるよ。'},
    rib:{nm:'むねのほね（ろっこつ）',w:['心ぞうや はい を守る','かごのような形'],g:[1],tip:'むねをさわると、1本1本のほねがわかるよ。'},
    pelvis:{nm:'こしのほね',w:['上の体をささえる','おなかの中を守る'],g:[0,1],tip:'こしの横をさわると、かたいほねがあるね。'},
    arm:{nm:'うでのほね',w:['きん肉に引っぱられて、うでを動かす','かた・ひじ・手首・ゆびで曲がる'],g:[2],tip:'うでをさわると、中にかたいほねが通っているね。'},
    leg:{nm:'あしのほね',w:['体の重さをささえる','きん肉に引っぱられて、歩いたり走ったりする','太もものほねは、体でいちばん長いほね'],g:[0,2],tip:'ひざやすねをさわると、ほねがよくわかるよ。'}};
  const GR=[['体をささえる','#ea580c'],['体の中を守る','#2563eb'],['体を動かす','#16a34a']];
  function drawSkel(hl,alpha){ ctx.save(); ctx.globalAlpha=alpha||1; const fc=k=>hl===k?C.sel:C.bone, oc=k=>hl===k?C.selL:C.boneL;
    // 頭
    ctx.fillStyle=fc('head'); ctx.strokeStyle=oc('head'); ctx.lineWidth=2; ctx.beginPath(); ctx.ellipse(200,56,30,34,0,0,7); ctx.fill(); ctx.stroke();
    ctx.beginPath(); ctx.ellipse(200,82,19,13,0,0,Math.PI); ctx.fill(); ctx.stroke();
    dot(189,56,7,'#d6d3d1'); dot(211,56,7,'#d6d3d1'); ctx.fillStyle='#d6d3d1'; ctx.beginPath(); ctx.moveTo(200,66); ctx.lineTo(196,75); ctx.lineTo(204,75); ctx.closePath(); ctx.fill();
    // こしのほね
    ctx.fillStyle=fc('pelvis'); ctx.strokeStyle=oc('pelvis'); ctx.lineWidth=1.6; ctx.beginPath(); ctx.moveTo(194,250); ctx.bezierCurveTo(170,236,150,244,154,262); ctx.bezierCurveTo(158,280,172,290,184,296); ctx.lineTo(200,300); ctx.lineTo(216,296); ctx.bezierCurveTo(228,290,242,280,246,262); ctx.bezierCurveTo(250,244,230,236,206,250); ctx.closePath(); ctx.fill(); ctx.stroke();
    ctx.fillStyle='#ece9e4'; ctx.beginPath(); ctx.ellipse(188,284,6,5,0,0,7); ctx.ellipse(212,284,6,5,0,0,7); ctx.fill();
    // むねのほね
    ctx.fillStyle=fc('rib'); ctx.strokeStyle=oc('rib'); ctx.lineWidth=1.2; rr(196,128,8,66,3); ctx.fill(); ctx.stroke();
    for(let i=0;i<7;i++){ const y=132+i*11.5, w=[28,36,41,43,42,39,34][i]; [-1,1].forEach(s=>{ [[5.5,oc('rib')],[3.5,fc('rib')]].forEach(st=>{ ctx.strokeStyle=st[1]; ctx.lineWidth=st[0]; ctx.beginPath(); ctx.moveTo(200+s*6,y); ctx.bezierCurveTo(200+s*(w+8),y-4,200+s*(w+6),y+18,200+s*9,y+16); ctx.stroke(); }); }); }
    // せぼね
    for(let y=96;y<=260;y+=9){ ctx.fillStyle=fc('spine'); ctx.strokeStyle=oc('spine'); ctx.lineWidth=1.2; rr(194,y,12,7,2); ctx.fill(); ctx.stroke(); }
    // さこつ
    boneSeg(V(196,121),V(150,119),5); boneSeg(V(204,121),V(250,119),5);
    // うで・あし
    [['L',-1],['R',1]].forEach(q=>{ const s=q[0], o=q[1], c=fc('arm'), oa=oc('arm'), cl=fc('leg'), ol=oc('leg');
      boneSeg(J['sh'+s],J['el'+s],10,c,oa); const el=J['el'+s], wr=J['wr'+s], fi=J['fi'+s];
      boneSeg(V(el.x-3.5,el.y+6),V(wr.x-3.5,wr.y-2),4.5,c,oa); boneSeg(V(el.x+3.5,el.y+6),V(wr.x+3.5,wr.y-2),4.5,c,oa);
      for(let k=0;k<4;k++) boneSeg(V(wr.x+(k-1.5)*3.4,wr.y+5),V(fi.x+(k-1.5)*5.2,fi.y+10),2.4,c,oa);
      boneSeg(V(wr.x-o*6,wr.y+5),V(wr.x-o*13,wr.y+19),2.4,c,oa);
      const hi=J['hi'+s], kn=J['kn'+s], an=J['an'+s];
      boneSeg(hi,kn,12,cl,ol); boneSeg(V(kn.x,kn.y+8),an,9,cl,ol); boneSeg(V(kn.x+o*7,kn.y+12),V(an.x+o*7,an.y-4),4,cl,ol); dot(kn.x,kn.y-2,6.5,cl,ol);
      boneSeg(V(an.x,an.y+4),V(an.x+o*8,an.y+16),6,cl,ol); });
    ctx.restore(); }
  const BL=[['head','頭のほね','のうを守る',300,34,V(229,50)],['rib','むねのほね','むねの中を守る',300,140,V(244,158)],['arm','うでのほね','うでを動かす',300,212,V(273,236)],
            ['leg','あしのほね','体をささえる',300,388,V(226,402)],['spine','せぼね','体をささえる',16,206,V(193,222)],['pelvis','こしのほね','おなかを守る',16,314,V(162,272)]];
  function drawBody(){ panel(LX,PY,LW,PH); drawSkel(selB,1);
    Object.keys(J).forEach(k=>{ if(k!=='waist'&&k!=='neck'){ ctx.strokeStyle=C.joint; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(J[k].x,J[k].y,6,0,7); ctx.stroke(); } });
    BL.forEach(b=>{ const s=selB===b[0]; lbl([[b[1],12.5,s?C.selL:C.ink],[b[2],11,C.sub]],b[3],b[4],b[3]>200?92:90,s?C.selL:'#a8a29e',b[5],b[0]); });
    tx('ほねをタップしてみよう',18,30,12.5,'#0e7490','left',true);
    ctx.strokeStyle=C.joint; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(24,446,6,0,7); ctx.stroke(); tx('＝関節（曲がるところ）',34,451,11.5,C.joint,'left',true); }
  function infoBody(){ panel(RX,PY,RW,PH); const x=RX+12, xr=RX+RW-12;
    if(!selB){ tx('ほねのはたらき',x,34,15.5,C.ink,'left',true); let y=52;
      [[0,'せぼね・こしのほね・あしのほね'],[1,'頭のほね→のう\nむねのほね→心ぞう・はい'],[2,'きん肉に引っぱられて、関節のところで曲がる']].forEach((q,i)=>{ const g=GR[q[0]];
        ctx.fillStyle='#f8fafc'; ctx.strokeStyle=g[1]; ctx.lineWidth=1.5; rr(x-2,y,RW-20,94,8); ctx.fill(); ctx.stroke();
        tx((i+1)+'. '+g[0],x+8,y+24,14.5,g[1],'left',true); wrap(q[1],x+8,y+48,RW-40,12,C.ink,18); y+=104; });
      wrap('ほねか、図の名前をタップすると、くわしく出るよ。',x,y+16,RW-24,12.5,'#0e7490',19,true); return; }
    const b=BN[selB]; let y=wrap(b.nm,x,40,RW-24,18,C.ink,24,true);
    let cx=x; b.g.forEach(gi=>{ const g=GR[gi], w=tw(g[0],11.5,true)+14; ctx.fillStyle=g[1]; rr(cx,y-6,w,22,11); ctx.fill(); tx(g[0],cx+7,y+10,11.5,'#fff','left',true); cx+=w+6; });
    y+=36; tx('はたらき',x,y,12,C.sub,'left',true); y+=20;
    b.w.forEach(s=>{ dot(x+4,y-4,3,C.ink); y=wrap(s,x+14,y,RW-38,13,C.ink,19)+4; });
    ctx.fillStyle='#ecfeff'; rr(x-4,y+6,RW-16,86,8); ctx.fill(); wrap('さわってみよう：'+b.tip,x+2,y+28,RW-28,12.5,'#0e7490',19,true);
    wrap('人の体には、ほねがおよそ200こあります。',x,PY+PH-36,RW-24,11.5,C.sub,17); }
  function boneAt(P){ const x=P.x, y=P.y;
    for(const h of HIT){ if(x>=h.x&&x<=h.x+h.w&&y>=h.y&&y<=h.y+h.h) return h.k; }
    if(((x-200)/34)**2+((y-62)/42)**2<1) return 'head';
    if(Math.abs(x-200)<11&&y>94&&y<266) return 'spine';
    if(((x-200)/50)**2+((y-164)/44)**2<1) return 'rib';
    if(Math.abs(x-200)<50&&y>=238&&y<304) return 'pelvis';
    for(const s of ['L','R']){ if(segD(P,J['sh'+s],J['el'+s])<14||segD(P,J['el'+s],J['wr'+s])<14||segD(P,J['wr'+s],J['fi'+s])<15) return 'arm';
      if(segD(P,J['hi'+s],J['kn'+s])<16||segD(P,J['kn'+s],J['an'+s])<15||dst(P,V(J['an'+s].x,J['an'+s].y+12))<17) return 'leg'; }
    return null; }

  // ================= 関節さがしクイズ =================
  const QJ=[['neck','首','neck'],['waist','こし','waist'],['shL','かた','sh'],['shR','かた','sh'],['elL','ひじ','el'],['elR','ひじ','el'],['wrL','手首','wr'],['wrR','手首','wr'],['fiL','ゆび','fi'],['fiR','ゆび','fi'],
            ['hiL','足のつけ根','hi'],['hiR','足のつけ根','hi'],['knL','ひざ','kn'],['knR','ひざ','kn'],['anL','足首','an'],['anR','足首','an']];
  const QG=[['neck','首'],['waist','こし'],['sh','かた'],['el','ひじ'],['wr','手首'],['fi','ゆび'],['hi','足のつけ根'],['kn','ひざ'],['an','足首']];
  function drawSil(){ const shape=(c,ex)=>{ ctx.strokeStyle=c; ctx.fillStyle=c; ctx.lineCap='round'; ctx.lineJoin='round';
      [['L'],['R']].forEach(q=>{ const s=q[0]; ctx.lineWidth=26+ex; ctx.beginPath(); ctx.moveTo(J['sh'+s].x,J['sh'+s].y); ctx.lineTo(J['el'+s].x,J['el'+s].y); ctx.lineTo(J['wr'+s].x,J['wr'+s].y); ctx.stroke();
        const fi=J['fi'+s]; ctx.beginPath(); ctx.ellipse(fi.x,fi.y-8,12+ex/2,19+ex/2,0,0,7); ctx.fill();
        ctx.lineWidth=32+ex; ctx.beginPath(); ctx.moveTo(J['hi'+s].x,J['hi'+s].y-6); ctx.lineTo(J['kn'+s].x,J['kn'+s].y); ctx.lineTo(J['an'+s].x,J['an'+s].y); ctx.stroke();
        const an=J['an'+s], o=s==='L'?-1:1; ctx.beginPath(); ctx.ellipse(an.x+o*6,an.y+12,17+ex/2,9+ex/2,0,0,7); ctx.fill(); });
      ctx.lineWidth=2+ex; ctx.beginPath(); ctx.moveTo(150,114); ctx.lineTo(250,114); ctx.quadraticCurveTo(262,118,258,140); ctx.lineTo(244,214); ctx.quadraticCurveTo(250,270,240,300); ctx.lineTo(160,300); ctx.quadraticCurveTo(150,270,156,214); ctx.lineTo(142,140); ctx.quadraticCurveTo(138,118,150,114); ctx.closePath(); ctx.fill(); ctx.stroke();
      ctx.fillRect(188-ex/2,84,24+ex,34); ctx.beginPath(); ctx.ellipse(200,56,32+ex/2,36+ex/2,0,0,7); ctx.fill(); };
    shape(C.skinL,4); shape(C.skin,0);
    dot(189,52,3.2,'#475569'); dot(211,52,3.2,'#475569'); ctx.strokeStyle='#b45309'; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(200,66,9,0.2*Math.PI,0.8*Math.PI); ctx.stroke(); }
  function drawQuiz(){ panel(LX,PY,LW,PH); drawSil(); const nf=Object.keys(found).length;
    if(reveal||nf===QJ.length) drawSkel(null,0.4);
    QJ.forEach(q=>{ const p=J[q[0]], left=q[0].slice(-1)==='L';
      if(found[q[0]]){ dot(p.x,p.y,10,'rgba(22,163,74,.85)','#fff'); tx('✓',p.x,p.y+5,13,'#fff','center',true); tag(q[1],left?p.x-15:p.x+15,p.y+5,11.5,C.joint,left?'right':'left'); }
      else if(reveal){ jring(p,13,'#ea580c',true); } });
    tx('体の曲がるところを、タップしてさがそう',18,30,12.5,'#0e7490','left',true); }
  function infoQuiz(){ panel(RX,PY,RW,PH); const x=RX+12, xr=RX+RW-12, nf=Object.keys(found).length;
    let y=wrap('体の曲がるところ（関節）をさがそう！',x,34,RW-24,15,C.ink,21,true);
    tx('見つけた数',x,y+14,12,C.sub,'left',true); tx(nf+' / '+QJ.length,xr,y+20,24,nf===QJ.length?C.joint:C.ink,'right',true); y+=40;
    QG.forEach((g,i)=>{ const ks=QJ.filter(q=>q[2]===g[0]), f=ks.filter(q=>found[q[0]]).length, cx=x+(i%2)*104, cy=y+Math.floor(i/2)*26;
      ctx.fillStyle=f===ks.length?'#dcfce7':'#f1f5f9'; rr(cx-2,cy-15,100,22,6); ctx.fill();
      tx(g[1],cx+5,cy+1,12,f===ks.length?C.joint:C.ink,'left',true); tx(f+'/'+ks.length,cx+93,cy+1,11.5,f===ks.length?C.joint:C.sub,'right',true); });
    y+=5*26+8; ctx.fillStyle=qlast?'#dcfce7':'#fff7ed'; rr(x-4,y,RW-16,96,8); ctx.fill();
    wrap(qmsg,x+2,y+22,RW-28,12.5,qlast?'#166534':'#9a3412',19,true);
    wrap('自分の体も動かして、たしかめよう。',x,PY+PH-18,RW-24,11.5,C.sub,17); }
  function quizTap(P){ let best=null, bd=27; QJ.forEach(q=>{ const d=dst(P,J[q[0]]); if(d<bd){ bd=d; best=q; } });
    if(best){ if(found[best[0]]){ qmsg=best[1]+'は、もう見つけたよ。ほかもさがそう。'; qlast=''; }
      else { found[best[0]]=1; qlast=best[1];
        qmsg=best[2]==='fi'?'ゆび！ゆびには関節がいくつもあるよ。にぎったり、ひらいたりしてみよう。':best[2]==='neck'?'首！せぼねの小さなほねのつなぎ目で曲がるよ。':best[2]==='waist'?'こし！せぼねは小さなほねがたくさんつながっていて、曲がるよ。':best[1]+'！ほねとほねのつなぎ目で、曲がるところ（関節）だよ。';
        if(Object.keys(found).length===QJ.length) qmsg='ぜんぶ見つけた！関節は、どれもほねとほねのつなぎ目にあるね。'; } return; }
    const b=boneAt(P); qlast='';
    qmsg=b==='head'?'頭は曲がらないね。かたいほねでできているよ。':(b==='arm'||b==='leg')?'そこは曲がらない！中に、かたいほねが1本通っているよ。':(b==='rib'||b==='spine'||b==='pelvis')?'むねやおなかは、ひじやひざのようには曲がらないね。':'体の上をタップしてみよう。'; }

  // ================= ウサギ =================
  const lerp=(a,b,t)=>a+(b-a)*t, sm=x=>x*x*(3-2*x), GND=382, SMAX=0.65;
  function rab(){ const r=Math.PI/180, s=hs, H0=V(134,300), a1=lerp(62,100,s)*r, a2=lerp(160,118,s)*r, a3=lerp(2,70,s)*r;
    const K0=ad(H0,V(Math.cos(a1),Math.sin(a1)),60), A0=ad(K0,V(Math.cos(a2),Math.sin(a2)),62), T0=ad(A0,V(Math.cos(a3),Math.sin(a3)),74), oy=GND-5-T0.y, u=s/SMAX, o=V(0,oy);
    return {oy:oy, H:ad(H0,o), K:ad(K0,o), A:ad(A0,o), T:ad(T0,o), FS:V(268,300+oy), FE:V(lerp(262,284,u),lerp(340,332,u)+oy), FW:V(lerp(270,306,u),lerp(372,350,u)+oy), FP:V(lerp(292,328,u),lerp(379,352,u)+oy)}; }
  function spineP(t,oy){ const a=V(286,246+oy), c=V(216,212+oy), b=V(146,280+oy), m=1-t; return V(m*m*a.x+2*m*t*c.x+t*t*b.x, m*m*a.y+2*m*t*c.y+t*t*b.y); }
  function drawRabbit(){ panel(LX,PY,LW,PH); const R=rab(), oy=R.oy, Y=v=>v+oy;
    ctx.fillStyle='#d9f99d'; ctx.fillRect(LX+1,GND,LW-2,PY+PH-GND-6); ctx.strokeStyle='#65a30d'; ctx.lineWidth=2; ln(V(LX+1,GND),V(LX+LW-1,GND));
    // 毛（外から見た形）
    const fa=view==='outer'?1:0.32;
    const fur=(c,ex)=>{ ctx.fillStyle=c; ctx.strokeStyle=c; ctx.lineCap='round'; ctx.lineJoin='round';
      [[290,Y(162),13,50,-0.35],[307,Y(166),12,48,-0.1]].forEach(e=>{ ctx.beginPath(); ctx.ellipse(e[0],e[1],e[2]+ex/2,e[3]+ex/2,e[4],0,7); ctx.fill(); });
      ctx.beginPath(); ctx.ellipse(206,Y(292),106+ex/2,58+ex/2,-0.12,0,7); ctx.fill();
      ctx.beginPath(); ctx.ellipse(150,Y(318),52+ex/2,46+ex/2,0,0,7); ctx.fill();
      ctx.beginPath(); ctx.ellipse(268,Y(298),38+ex/2,42+ex/2,0,0,7); ctx.fill();
      ctx.beginPath(); ctx.ellipse(318,Y(232),44+ex/2,34+ex/2,0.15,0,7); ctx.fill();
      dot(98,Y(276),15+ex/2,c);
      ctx.lineWidth=22+ex; ln(R.K,R.A); ctx.lineWidth=17+ex; ln(R.A,R.T);
      ctx.lineWidth=15+ex; ctx.beginPath(); ctx.moveTo(R.FS.x,R.FS.y); ctx.lineTo(R.FE.x,R.FE.y); ctx.lineTo(R.FW.x,R.FW.y); ctx.lineTo(R.FP.x,R.FP.y); ctx.stroke(); };
    ctx.save(); ctx.globalAlpha=fa; fur(C.furL,3); fur(C.fur,0); ctx.restore();
    if(view==='outer'){ dot(336,Y(222),5,'#1f2937'); dot(361,Y(238),3.5,'#be185d'); ctx.strokeStyle='#78716c'; ctx.lineWidth=1; [[-6],[0],[6]].forEach(d=>{ ln(V(356,Y(242)),V(392,Y(236+d[0]*1.6))); }); }
    if(view==='both'){ const mc=mix(C.pale,C.red,hAct);
      spindle(ad(R.H,V(-4,-16)),ad(R.K,V(8,-6)),15,mc,0,6);
      const d2=V((R.A.x-R.K.x)/62,(R.A.y-R.K.y)/62), n2=V(-d2.y,d2.x); spindle(ad(ad(R.K,n2,8),d2,4),ad(R.A,n2,4),9,mc,0,24);
      spindle(ad(R.FS,V(-10,-14)),ad(R.FE,V(-4,0)),8,mix(C.pale,C.red,0.3),0,6);
      spindle(V(282,Y(232)),V(176,Y(250)),7,mix(C.pale,C.red,0.3),6,6); }
    if(view!=='outer'){
      ctx.fillStyle=C.bone; ctx.strokeStyle=C.boneL; ctx.lineWidth=1.6; ctx.save(); ctx.translate(322,Y(232)); ctx.rotate(0.2); ctx.beginPath(); ctx.ellipse(0,0,34,21,0,0,7); ctx.fill(); ctx.stroke(); ctx.restore(); dot(330,Y(224),8,'#e7e5e4');
      for(let k=0;k<8;k++){ const P0=spineP(0.1+k*0.055,oy); [[5,C.boneL],[3,C.bone]].forEach(st=>{ ctx.strokeStyle=st[1]; ctx.lineWidth=st[0]; ctx.beginPath(); ctx.moveTo(P0.x,P0.y); ctx.quadraticCurveTo(P0.x+16,P0.y+34,P0.x-4,P0.y+56-k*3); ctx.stroke(); }); }
      for(let k=0;k<=18;k++){ const P0=spineP(k/18,oy); dot(P0.x,P0.y,4.6,C.bone,C.boneL); }
      [[128,Y(279)],[116,Y(278)],[106,Y(277)]].forEach(p=>dot(p[0],p[1],3,C.bone,C.boneL));
      boneSeg(V(152,Y(270)),V(124,Y(300)),9);
      ctx.fillStyle=C.bone; ctx.strokeStyle=C.boneL; ctx.beginPath(); ctx.moveTo(254,Y(252)); ctx.lineTo(276,Y(256)); ctx.lineTo(270,Y(300)); ctx.closePath(); ctx.fill(); ctx.stroke();
      boneSeg(R.FS,R.FE,8); boneSeg(R.FE,R.FW,6); boneSeg(R.FW,R.FP,4);
      boneSeg(R.H,R.K,11); boneSeg(R.K,R.A,8); boneSeg(R.A,R.T,5); }
    [R.FS,R.FE,R.H,R.K,R.A].forEach(p=>jring(p,11,C.joint,true));
    if(view!=='outer'){ lbl([['頭のほね',12.5,C.ink]],318,300,76,'#a8a29e',V(338,Y(246)));
      lbl([['せぼね',12.5,C.ink]],150,140,70,'#a8a29e',spineP(0.45,oy));
      lbl([['むねのほね',12.5,C.ink]],318,342,76,'#a8a29e',V(258,Y(300))); }
    if(view==='both') lbl([['後ろあしの',12,C.ink],['きん肉',12.5,hAct>0.5?C.red:C.ink]],16,190,96,hAct>0.5?C.red:'#94a3b8',ad(R.H,V(10,24)));
    lbl([['関節',12.5,C.joint],['ひざ・かかと など',11,C.sub]],16,402,118,C.joint,ad(R.K,V(-8,6)));
    tx(hop?'ジャンプ中':'✋ 上へなぞるとジャンプ',18,30,12.5,'#0e7490','left',true); }
  function infoAni(){ panel(RX,PY,RW,PH); const x=RX+12, xr=RX+RW-12;
    tx('ウサギにも',x,34,15.5,C.ink,'left',true); tx('ほねときん肉がある',x,56,15.5,C.ink,'left',true);
    let y=84; tx('人',x+138,y,12,C.sub,'center',true); tx('ウサギ',x+184,y,12,C.sub,'center',true); y+=8;
    [['頭のほね'],['せぼね'],['むねのほね'],['あしのほね'],['きん肉'],['関節']].forEach((r,i)=>{ ctx.fillStyle=i%2?'#fff':'#f8fafc'; ctx.fillRect(x-4,y,RW-16,22); tx(r[0],x+2,y+16,12.5,C.ink,'left',true); tx('○',x+138,y+16,13,C.joint,'center',true); tx('○',x+184,y+16,13,C.joint,'center',true); y+=22; });
    y+=24; const act=hAct>0.5&&(hop||drag);
    ctx.fillStyle=act?'#fee2e2':'#ecfeff'; rr(x-4,y-16,RW-16,82,8); ctx.fill();
    wrap(act?'後ろあしのきん肉がちぢんで、地面を強くけってジャンプ！':'ウサギの体をやさしくさわると、かたいほねと、やわらかいきん肉があるのがわかるよ。',x+2,y+4,RW-28,12.5,act?C.red:'#0e7490',19,true);
    y+=86; y=wrap('人とのちがい：後ろあしが長く、きん肉が大きい。だから、大きくジャンプできる。',x,y,RW-24,12.5,C.ink,19);
    wrap('さわるときはやさしく。さわったあとは手をあらおう。',x,y+10,RW-24,11.5,C.sub,17); }

  // ================= 共通 =================
  function draw(){ ctx.fillStyle=C.bg; ctx.fillRect(0,0,W,H); HIT=[];
    if(mode==='arm'){ drawArm(); infoArm(); } else if(mode==='body'){ drawBody(); infoBody(); } else if(mode==='quiz'){ drawQuiz(); infoQuiz(); } else { drawRabbit(); infoAni(); } }
  function stats(){ const nf=Object.keys(found).length, key=[mode,Math.round(ang),cin>0.5,dir,wt,selB,nf,qlast,reveal,hAct>0.5,view].join('|'); if(key===lastKey) return; lastKey=key;
    const L=(id,t)=>{ K(id).textContent=t; };
    if(mode==='arm'){ const on=cin>0.5; L('sA','ひじの角度'); sh('sA',Math.round(ang)+'°',ang>=172?'うでをのばしている':'うでを曲げている');
      L('sB','内側のきん肉'); sh('sB',on?'ちぢむ':'ゆるむ',on?'太く、かたくなる':'のびて、やわらかい'); L('sC','外側のきん肉'); sh('sC',on?'ゆるむ':'ちぢむ',on?'のびて、やわらかい':'太く、かたくなる');
      L('sD','曲がるところ'); sh('sD','ひじの関節','ほねとほねのつなぎ目');
      setShare('【ほねときん肉】うでを'+(on?'曲げる':'のばす')+'とき、'+(on?'内側':'外側')+'のきん肉がちぢみ、'+(on?'外側':'内側')+'のきん肉がゆるむ。うでは、ひじの関節で曲がる（ひじの角度'+Math.round(ang)+'°）｜シミュラボ'); }
    else if(mode==='body'){ const b=selB?BN[selB]:null; L('sA','えらんだほね'); sh('sA',b?b.nm.replace('（ろっこつ）',''):'まだ',b?'':'ほねをタップしてね');
      L('sB','はたらき'); sh('sB',b?b.w[0]:'ささえる・守る',b?'':'・動かす'); L('sC','全身のほねの数'); sh('sC','約200こ','大人で約206こ'); L('sD','ほねのつなぎ目'); sh('sD','関節','曲がるところ');
      setShare(b?'【全身のほね】'+b.nm+'のはたらき：'+b.w.join('・')+'｜シミュラボ':'【全身のほね】ほねには「体をささえる」「体の中を守る」「きん肉といっしょに体を動かす」はたらきがある。人の体のほねは約200こ｜シミュラボ'); }
    else if(mode==='quiz'){ L('sA','見つけた関節'); sh('sA',nf+' / '+QJ.length,nf===QJ.length?'ぜんぶ見つけた！':'のこり '+(QJ.length-nf)+'か所');
      L('sB','いま見つけた'); sh('sB',qlast||'まだ',qlast?'曲がるところ':'体をタップ'); L('sC','曲がらない所'); sh('sC','ほねの1本の所','頭・うでやあしのとちゅう'); L('sD','関節とは'); sh('sD','つなぎ目','ほねとほねのつなぎ目');
      setShare('【体の関節さがし】体の曲がるところ（関節）を '+QJ.length+'か所中 '+nf+'か所 見つけた！関節は、ほねとほねのつなぎ目にある｜シミュラボ'); }
    else { L('sA','見ている動物'); sh('sA','ウサギ','学校でかわれることが多い'); L('sB','ほね'); sh('sB','ある','頭・せぼね・むね・あし');
      L('sC','きん肉'); sh('sC','ある',hAct>0.5&&(hop||drag)?'後ろあしのきん肉がちぢむ':'ほねについて体を動かす'); L('sD','関節'); sh('sD','ある','かた・ひじ・ひざ・かかと');
      setShare('【ウサギのほねときん肉】ウサギにも人と同じように、ほね・きん肉・関節がある。後ろあしのきん肉がちぢんでジャンプする｜シミュラボ'); } }
  function setPlay(){ const p=$('play'); if(!p) return; p.textContent=mode==='ani'?(hop?'⏸ 止める':'▶ ジャンプさせる'):(auto?'⏸ 止める':'▶ 自動で曲げのばし'); $('wt').textContent=wt?'🏋️ おもりをはなす':'🏋️ おもりを持つ'; }
  function setMode(m){ mode=m; drag=null; setTab(['tArm','tBody','tQuiz','tAni'],{arm:'tArm',body:'tBody',quiz:'tQuiz',ani:'tAni'}[m]);
    showF('ang',m==='arm'); showF('view',m==='ani'); show('play',m==='arm'||m==='ani'); show('wt',m==='arm'); show('ans',m==='quiz'); show('again',m==='quiz'); setPlay(); lastKey=''; stats(); draw(); }

  // ---------- 操作 ----------
  $('tArm').addEventListener('click',()=>setMode('arm')); $('tBody').addEventListener('click',()=>setMode('body'));
  $('tQuiz').addEventListener('click',()=>setMode('quiz')); $('tAni').addEventListener('click',()=>setMode('ani'));
  $('ang').addEventListener('input',()=>{ auto=false; setPlay(); setAng(+$('ang').value); });
  $('view').addEventListener('change',()=>{ view=$('view').value; lastKey=''; });
  $('play').addEventListener('click',()=>{ if(mode==='ani'){ hop=!hop; } else { auto=!auto; if(auto) aph=Math.acos(clamp((112.5-ang)/67.5,-1,1)); } setPlay(); });
  $('wt').addEventListener('click',()=>{ wt=!wt; setPlay(); });
  $('ans').addEventListener('click',()=>{ reveal=true; qmsg='オレンジの点線の所も、曲がるところ（関節）。自分の体でもたしかめよう。'; qlast=''; });
  $('again').addEventListener('click',()=>{ found={}; reveal=false; qlast=''; qmsg='体の曲がるところを、指でタップしてさがそう。'; });
  function armTo(P){ const dx=P.x-E.x, dy=P.y-E.y; if(Math.hypot(dx,dy)<25) return; let phi=Math.atan2(dx,dy)*180/Math.PI; if(phi<-90) phi+=360; setAng(180-phi); }
  cv.addEventListener('pointerdown',e=>{ const p=cpos(cv,e), P=V(p[0]/dpr,p[1]/dpr);
    if(mode==='body'){ const b=boneAt(P); selB=b||null; return; }
    if(mode==='quiz'){ if(P.x<LX+LW) quizTap(P); return; }
    if(P.x>LX+LW) return;
    if(mode==='arm'){ auto=false; setPlay(); drag={}; armTo(P); }
    else { hop=false; setPlay(); drag={y0:P.y,s0:hs}; }
    try{ cv.setPointerCapture(e.pointerId); }catch(err){} });
  cv.addEventListener('pointermove',e=>{ if(!drag) return; const p=cpos(cv,e), P=V(p[0]/dpr,p[1]/dpr);
    if(mode==='arm') armTo(P); else if(mode==='ani'){ const ns=clamp(drag.s0+(drag.y0-P.y)/140,0,SMAX); if(ns>hs+0.002) hAct=1; else if(ns<hs-0.002) hAct=0; hs=ns; } });
  const up=()=>{ drag=null; }; cv.addEventListener('pointerup',up); cv.addEventListener('pointercancel',up);
  function frame(t){ const dt=last?Math.min(0.05,(t-last)/1000):0; last=t; tNow+=dt;
    if(mode==='arm'){ if(auto){ aph+=dt*1.5; setAng(112.5-67.5*Math.cos(aph)); } cin+=((dir>0?1:0)-cin)*Math.min(1,dt*7); if(moveT>0) moveT-=dt; }
    if(mode==='ani'&&hop){ hph=(hph+dt*0.85)%1; const p=hph; const ns=p<0.3?SMAX*sm(p/0.3):SMAX*(1-sm((p-0.3)/0.7)); hAct=ns>=hs?1:0; hs=ns; }
    stats(); draw(); requestAnimationFrame(frame); }
  // URLで初期状態（例 ?mode=quiz&a=150&d=-1）
  if(Q.has('a')){ ang=clamp(+Q.get('a')||90,45,180); $('ang').value=Math.round(ang); }
  if(Q.get('d')==='-1'){ dir=-1; cin=0; }
  if(Q.get('wt')==='1') wt=true;
  if(Q.has('sel')&&BN[Q.get('sel')]) selB=Q.get('sel');
  if(Q.has('s')){ hs=clamp(+Q.get('s')||0,0,SMAX); hAct=1; }
  if(Q.has('view')){ view=Q.get('view'); $('view').value=view; }
  if(Q.get('found')==='all') QJ.forEach(q=>found[q[0]]=1); else if(Q.has('found')) QJ.slice(0,+Q.get('found')||0).forEach(q=>found[q[0]]=1);
  if(Q.get('reveal')==='1') reveal=true;
  $('angL').textContent=Math.round(ang)+'°';
  setMode(['arm','body','quiz','ani'].indexOf(Q.get('mode'))>=0?Q.get('mode'):'arm');
  requestAnimationFrame(frame);
'''

HONE_ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
<p>うでを曲げるときは、<b>うでの内側のきん肉がちぢみ、外側のきん肉がゆるみます</b>。のばすときは、その反対に<b>外側のきん肉がちぢみ、内側のきん肉がゆるみます</b>。きん肉はちぢんでほねを引っぱり、うでは<b>ほねとほねのつなぎ目（関節）</b>のところで曲がります。全身のほねの図では、ほねには「体をささえる」「体の中を守る」「きん肉といっしょに体を動かす」はたらきがあることを、関節さがしクイズでは、体の曲がるところと曲がらないところを確かめられます。ウサギにも、人と同じようにほね・きん肉・関節があります。</p>
''' + N('<b>対応する単元</b>：小学4年 B（1）人の体のつくりと運動「（ア）人の体には骨と筋肉があること」「（イ）人が体を動かすことができるのは，骨，筋肉の働きによること」。内容の取扱いで「関節の働きを扱うものとする」とされています。学習指導要領解説（理科編 p.53〜54）では、自分の体に直接触れて骨の位置や筋肉の存在を調べること、他の動物（学校飼育動物など身近で安全な哺乳類）の体の動きを観察すること、映像や模型などを活用することが示されています。') + '''
<h2>授業での使い方</h2>
<h3>導入：自分の体にさわって予想する</h3>
<p>うでを曲げたりのばしたりしながら、うでをさわらせます。「かたい所とやわらかい所があるね。うでの中はどうなっているのだろう」と問いかけ、ノートに「うでの中のようす」を絵でかかせます。そのあと「💪 うで」の図を見せて、自分の絵と比べさせます。</p>
<h3>展開：曲げる・のばすときのきん肉を調べる</h3>
<p>うでの図の手を指で動かして、ひじを曲げたりのばしたりします。曲げると内側のきん肉が赤く太くなり（ちぢむ）、外側はうすい色で細くなります（ゆるむ）。実際に、反対の手で内側と外側のきん肉をさわりながらうでを曲げのばしし、かたさの変わり方を確かめます。「🏋️ おもりを持つ」で、物を持ち上げるときに内側のきん肉がもっとかたくなることも話し合えます。</p>
<h3>まとめ：関節さがし・全身のほね・動物</h3>
<p>「❓ 関節さがし」で、体の曲がるところ（関節）をタップしてさがします。曲がらない所をタップすると「中にかたいほねが1本通っている」と出るので、曲がるところ＝ほねとほねのつなぎ目であることに気づかせます。「🦴 全身のほね」でほねのはたらきを整理し、「🐰 ウサギ」で、学校で飼っている動物にもほね・きん肉・関節があることを確かめます。</p>
<h3>児童への問いの例</h3>
<ol>
<li>うでを曲げるとき、内側のきん肉と外側のきん肉は、それぞれどうなっているだろう？</li>
<li>体の曲がるところと曲がらないところでは、中のほねのようすはどうちがうだろう？</li>
<li>ウサギが大きくジャンプできるのは、体のどこがどのようにはたらいているからだろう？</li>
</ol>
<h2>しくみ・解説</h2>
<h3>言葉の意味（1文で）</h3>
<ul>
<li><b>ほね（骨）</b>とは、体の中にあるかたい部分で、体をささえたり、体の中を守ったりしています。</li>
<li><b>きん肉（筋肉）</b>とは、ほねについているやわらかい部分で、ちぢんだりゆるんだりして、ほねを動かします。</li>
<li><b>関節</b>とは、ほねとほねのつなぎ目で、体が曲がるところのことです。</li>
<li><b>ちぢむ</b>とは、きん肉が短く太くなって、ほねを引っぱることです（このとき、さわるとかたくなります）。</li>
<li><b>ゆるむ</b>とは、きん肉が力をぬいて、のばされている状態のことです（さわるとやわらかいです）。</li>
</ul>
<h3>うでを曲げる・のばすときのきん肉（早見表）</h3>
''' + T([["うでを曲げる", "ちぢむ（太く、かたくなる）", "ゆるむ（のびて、やわらかい）", "内側のきん肉が下うでのほねを引っぱる"],
          ["うでをのばす", "ゆるむ（のびて、やわらかい）", "ちぢむ（太く、かたくなる）", "外側のきん肉がひじの後ろのほねを引っぱる"],
          ["物を持ち上げる", "ちぢむ（もっとかたくなる）", "ゆるむ", "重い物ほど、内側のきん肉が強くはたらく"]],
         ["うでの動き", "内側のきん肉", "外側のきん肉", "ほねの動き"]) + '''
<p>きん肉は、自分でちぢむことはできますが、自分でのびてほねをおすことはできません。そのため、うでには内側と外側の2つのきん肉があり、曲げるときと、のばすときで、はたらくきん肉が入れかわります。</p>
<h3>おもなほねとはたらき（早見表）</h3>
''' + T([["頭のほね", "頭", "のう（脳）を守る"], ["せぼね", "せなかのまん中", "体をささえる・体を曲げたりひねったりできる"],
          ["むねのほね（ろっこつ）", "むね", "心ぞうや はい（肺）を守る"], ["こしのほね", "こし", "上の体をささえる・おなかの中を守る"],
          ["うでのほね", "うで", "きん肉に引っぱられて、うでを動かす"], ["あしのほね", "あし", "体の重さをささえる・歩く、走る"]],
         ["ほね", "ある場所", "おもなはたらき"]) + '''
<p>人の体には、ほねがおよそ200こあります（大人で約206こ）。いちばん長いほねは太もものほね、いちばん小さいほねは耳の中にあるほねです。</p>
<h3>体の曲がるところ（関節）</h3>
''' + T([["首・こし", "せぼね（小さなほねがたくさんつながっている）"], ["かた", "うでのほねと、かたのほね"], ["ひじ", "うでのほね（上と下）"],
          ["手首・ゆび", "手のほね（ゆびには関節がいくつもある）"], ["足のつけ根", "あしのほねと、こしのほね"], ["ひざ・足首", "あしのほね"]],
         ["曲がるところ", "つながっているほね"]) + '''
<h3>先生向けの補足：筋肉は腱で骨についている</h3>
''' + N('筋肉の両端は、<b>腱（けん、すじ）</b>という丈夫な組織になっていて、関節をまたいで2つの骨についています。図の筋肉の両端にある白い細い部分が腱です。かかとの「アキレス腱」は、ふくらはぎの筋肉をかかとの骨につなぐ腱で、さわって確かめやすい例です。<br>図の「内側の筋肉」は上腕二頭筋（いわゆる力こぶ）、「外側の筋肉」は上腕三頭筋にあたります。一方が縮むとき他方がゆるむ組み合わせ（拮抗筋）になっています。教科書では「内側の筋肉」「外側の筋肉」と表すことが多いため、児童向けの表記はそれに合わせています。') + '''
<p>筋肉は縮むときにだけ力を出します（引っぱることはできても、おすことはできません）。そのため、曲げる筋肉とのばす筋肉が対になってはたらきます。第6学年「人の体のつくりと働き」、中学校第2分野「動物の体のつくりと働き」（運動器官）につながる内容です。</p>
<h3>このシミュレーションで単純化していること</h3>
<ul>
<li>うでの図は、ほね・きん肉を見やすくするため、皮ふをすかして、主なほねと2つのきん肉だけをかいています。実際には、うでにはもっと多くのきん肉があります。</li>
<li>きん肉が「ちぢむ・ゆるむ」は、うでを曲げているか、のばしているか（最後に動かした向き）で切りかえています。うでを止めたまま力を入れたときのようすは表していません。</li>
<li>全身のほねの図は、主なほねだけを簡単な形でかいています。手や足の小さなほね、頭のほねのつなぎ目などは省いています。</li>
<li>ウサギの図は、ほね・きん肉の位置を簡単にした模式図です。</li>
</ul>
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「小学校学習指導要領（平成29年告示）解説 理科編」第4学年 B（1）人の体のつくりと運動（''' + A(MEXT_SHO, "小学校学習指導要領・解説") + '''）</li>
<li>小学校理科の教科書（第4学年「人の体のつくりと運動」「ほねときん肉」の単元）</li>
</ul>
'''

sim(slug="hone-kinniku", cat="rika", emoji="💪", score=80,
    title="ほねときん肉のシミュレーター（うでの曲げのばし・関節）",
    title_tag="骨と筋肉・関節のシミュレーター｜うでを曲げるとちぢむ筋肉・ゆるむ筋肉（小4理科 人の体のつくりと運動）",
    meta_desc="うでの手を指で動かすと、ひじを曲げたときは内側のきん肉がちぢみ外側がゆるむ、のばすと入れかわる様子が色と太さでわかる小4理科「人の体のつくりと運動」の無料シミュレーター。全身の骨のはたらき、関節さがしクイズ、ウサギの骨と筋肉も。",
    og_title="ほねときん肉のシミュレーター（うでの曲げのばし・関節）",
    og_desc="うでを曲げると内側のきん肉がちぢみ、外側がゆるむ。関節さがしクイズ、全身のほねのはたらき、ウサギのほねときん肉も確かめる小4理科の教材。",
    card_desc="うでを曲げると内側のきん肉がちぢみ、のばすと外側がちぢむ。関節さがしクイズ・全身のほね・ウサギも。",
    lead="うでの図の手を指で動かして、ひじを曲げたりのばしたりしてみましょう。内側と外側のきん肉が、ちぢむ・ゆるむを入れかえながらほねを動かすようすがわかります。体の関節さがしクイズや、全身のほね、ウサギのほねときん肉も見られます。",
    model="小4 人の体のつくりと運動",
    level="小学4年",
    unit="小学校 第4学年 B（1）人の体のつくりと運動",
    canvas=canvas(640, 470, light=True),
    controls=TABS(btn("tArm", "💪 うで", True) + btn("tBody", "🦴 全身のほね") + btn("tQuiz", "❓ 関節さがし") + btn("tAni", "🐰 ウサギ"))
           + FULL(slider("ang", "ひじの角度", 45, 180, 90, 1, "{v}°"))
           + FULL(select("view", "ウサギの見え方", [("both", "ほねときん肉"), ("bone", "ほねだけ"), ("outer", "外から見た形")])),
    buttons=btn("play", "▶ 自動で曲げのばし", True) + btn("wt", "🏋️ おもりを持つ") + btn("ans", "こたえを見る", True) + btn("again", "↺ もう一度"),
    stats=stats([("sA", "ひじの角度", False), ("sB", "内側のきん肉", True), ("sC", "外側のきん肉", True), ("sD", "曲がるところ", False)]),
    legend="上のボタンで図を切りかえます。うで：手を指で動かすか、スライダーでひじの角度を変えます（赤くて太いきん肉＝ちぢんでいる、うすい色で細いきん肉＝ゆるんでいる、きん肉のはしの白い部分＝けん、緑の点線の円＝関節）。全身のほね：ほねや名前をタップすると、はたらきが出ます。関節さがし：体の曲がるところをタップ。ウサギ：上へなぞるか「▶ ジャンプさせる」で後ろあしが動きます。図は、ほねときん肉を見やすくした模式図です。",
    article=HONE_ARTICLE,
    faqs=[("うでを曲げるとき、きん肉はどうなっていますか？", "うでの内側のきん肉がちぢみ（太く、かたくなる）、外側のきん肉がゆるみます。ちぢんだ内側のきん肉が下うでのほねを引っぱるので、うでがひじの関節のところで曲がります。"),
          ("うでをのばすとき、きん肉はどうなっていますか？", "曲げるときと反対に、外側のきん肉がちぢみ、内側のきん肉がゆるみます。きん肉はちぢんでほねを引っぱることしかできないので、曲げるきん肉とのばすきん肉が入れかわってはたらきます。"),
          ("関節とは何ですか？", "ほねとほねのつなぎ目で、体が曲がるところのことです。かた・ひじ・手首・ゆび・足のつけ根・ひざ・足首などにあります。首やこしは、せぼねの小さなほねのつなぎ目で曲がります。"),
          ("ほねにはどんなはたらきがありますか？", "体をささえるはたらき（せぼね・こしのほね・あしのほね）、体の中を守るはたらき（頭のほねがのうを、むねのほねが心ぞうや肺を守る）、きん肉といっしょに体を動かすはたらきがあります。"),
          ("きん肉はほねにどうやってついていますか？", "きん肉のはしは「けん（すじ）」というじょうぶな部分になっていて、関節をまたいで2つのほねについています。かかとのアキレスけんは、ふくらはぎのきん肉をかかとのほねにつなぐけんです。"),
          ("ウサギなどの動物にも、ほねやきん肉はありますか？", "あります。ウサギにも、頭のほね・せぼね・むねのほね・あしのほねと、きん肉・関節があり、人と同じように、ほねときん肉のはたらきで体を動かします。ウサギは後ろあしが長く、きん肉が大きいので、大きくジャンプできます。")],
    rel=[("hito-karada", "🫀", "人の体のつくりと働き"), ("myakuhaku-heikin", "💓", "脈拍・心拍数 平均チェック"), ("reaction-test", "⚡", "反応速度テスト"),
         ("konchu-sodachi", "🦋", "こん虫の育ち方"), ("amamizu-yukue", "☔", "雨水のゆくえと地面のようす")],
    js=JS_HONE)


# ============================================================ 2 雨水のゆくえと地面のようす
JS_AMA = HELP + r'''
  const C={bg:'#f8fafc',ink:'#0f172a',sub:'#64748b',grid:'#e2e8f0',wd:'#1d4ed8'};
  let mode='slope', tNow=0, last=0, lastKey='', drag=null;
  const fr=v=>v-Math.floor(v), hs1=k=>fr(Math.sin(k*12.9898)*43758.5453), hs2=k=>fr(Math.sin(k*78.233)*12345.678);
  function fmtT(s){ s=Math.max(0,s); if(s>=600) return '約'+Math.round(s/60)+'分'; if(s<60) return Math.floor(s)+'秒'; const m=Math.floor(s/60), r=Math.floor(s%60); return m+'分'+(r<10?'0':'')+r+'秒'; }

  // ================= ① 地面のかたむきと水の流れ =================
  // 地面の断面（横20 m を128に分ける）。高さ h・水の深さ w は cm。雨と、土へのしみこみ（しみこむ力 f mm/時）を計算する
  const N=128, GX0=14, GX1=598, BY=330, PX=4.2, CW=(GX1-GX0)/N, SPEED=60, SUB=0.5;
  const h=new Float64Array(N), w=new Float64Array(N), F=new Float64Array(N);
  const SOIL={kotei:{nm:'校庭の土',f:10,c:'#b8915f',d:'#8a6a43'},suna:{nm:'すな場のすな',f:150,c:'#e8d09a',d:'#b9944f'},nendo:{nm:'ねん土っぽい土',f:2,c:'#a07f68',d:'#6b5040'},asph:{nm:'アスファルト',f:0,c:'#6b7280',d:'#374151'}};
  let shape='ex', soil='kotei', R=30, rain=true, tot={r:0,i:0,o:0}, rainT=0, acc=0, gEMA=0;
  function preset(k){ for(let i=0;i<N;i++){ const x=i/(N-1); let v;
      if(k==='ex') v=30-17*x+6*Math.sin(2*Math.PI*x*1.45+1.6)+1.5*Math.cos(x*37)*(1-0.7*x);
      else if(k==='slope') v=34-28*x;
      else if(k==='valley') v=6+32*Math.pow(2*x-1,2)+1.2*Math.sin(x*29);
      else v=14+0.8*Math.sin(x*31)+0.5*Math.sin(x*13);
      h[i]=clamp(v,1,48); } clearW(); }
  function clearW(){ w.fill(0); tot={r:0,i:0,o:0}; rainT=0; acc=0; gEMA=0; }
  function stepFlow(dt){ const rn=rain?R/36000*dt:0, fc=SOIL[soil].f/36000*dt;
    for(let i=0;i<N;i++){ w[i]+=rn; tot.r+=rn; const q=Math.min(w[i],fc); w[i]-=q; tot.i+=q; }
    for(let i=0;i<N-1;i++){ let q=0.24*((h[i]+w[i])-(h[i+1]+w[i+1])); q=q>0?Math.min(q,w[i]*0.5):Math.max(q,-w[i+1]*0.5); F[i]=q; }
    for(let i=0;i<N-1;i++){ w[i]-=F[i]; w[i+1]+=F[i]; }
    const d=w[N-1]*0.5; w[N-1]-=d; tot.o+=d; return d; }
  function adv(sec){ acc+=sec; let out=0, n=0; while(acc>=SUB){ out+=stepFlow(SUB); acc-=SUB; n++; if(rain) rainT+=SUB; } if(n) gEMA+=(out/(n*SUB)-gEMA)*0.15; }
  function puddles(){ const out=[]; let i=0; while(i<N){ if(w[i]>0.3){ let j=i, md=0, mi=i; while(j<N&&w[j]>0.3){ if(w[j]>md){ md=w[j]; mi=j; } j++; } out.push({a:i,b:j-1,d:md,m:mi}); i=j; } else i++; } return out; }
  const Y=v=>BY-v*PX, X=i=>GX0+(i+0.5)*CW;
  function rainWord(r){ return r<10?'ふつうの雨':r<20?'やや強い雨':r<30?'強い雨':r<50?'はげしい雨':r<80?'ひじょうにはげしい雨':'もうれつな雨'; }
  function drawSlope(){ const S=SOIL[soil];
    ctx.fillStyle=rain?'#e2e8f0':'#eef6fc'; rr(8,8,624,338,10); ctx.fill(); ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1.2; ctx.stroke();
    if(rain){ [[90,40],[250,34],[420,42],[565,36]].forEach(c=>{ dot(c[0],c[1],22,'#a3adbb'); dot(c[0]+24,c[1]+4,18,'#a3adbb'); dot(c[0]-24,c[1]+6,16,'#a3adbb'); });
      const nd=Math.round(14+R*1.2); ctx.strokeStyle='rgba(37,99,235,.55)'; ctx.lineWidth=1.5; ctx.beginPath();
      for(let k=0;k<nd;k++){ const x=GX0+hs1(k+1)*(GX1-GX0), i=clamp(Math.floor((x-GX0)/CW),0,N-1), top=Y(h[i]+w[i]), y=58+fr(hs2(k+1)+tNow*1.6)*(top-58); if(y+10<top){ ctx.moveTo(x,y); ctx.lineTo(x-1.5,y+10); } }
      ctx.stroke(); }
    // 地面
    ctx.beginPath(); ctx.moveTo(9,344); ctx.lineTo(9,Y(h[0])); for(let i=0;i<N;i++) ctx.lineTo(X(i),Y(h[i])); ctx.lineTo(GX1,Y(h[N-1])); ctx.lineTo(GX1,344); ctx.closePath(); ctx.fillStyle=S.c; ctx.fill();
    ctx.fillStyle=S.d; for(let k=0;k<170;k++){ const x=GX0+hs1(k+300)*(GX1-GX0), i=clamp(Math.floor((x-GX0)/CW),0,N-1), y=Y(h[i])+4+hs2(k+300)*Math.max(0,340-Y(h[i])-6), z=soil==='suna'?2.4:1.6; if(soil!=='asph') ctx.fillRect(x,y,z,z); }
    // みぞ
    const gy=Y(h[N-1]), lv=clamp(Math.sqrt(Math.max(0,gEMA))*60,0,24);
    ctx.fillStyle='#9ca3af'; ctx.fillRect(GX1,gy-2,32,34); ctx.fillStyle='#334155'; ctx.fillRect(GX1+5,gy,22,28); if(lv>0.5){ ctx.fillStyle='rgba(59,130,246,.85)'; ctx.fillRect(GX1+5,gy+28-lv,22,lv); }
    tx('みぞ',GX1+16,gy-8,11.5,C.ink,'center',true);
    // 水
    ctx.fillStyle='rgba(59,130,246,.8)'; for(let i=0;i<N;i++){ if(w[i]>0.03){ const y0=Y(h[i]+w[i]), y1=Y(h[i]); ctx.fillRect(X(i)-CW/2-0.4,y0,CW+0.8,Math.max(1.6,y1-y0)); } }
    ctx.strokeStyle='rgba(30,64,175,.6)'; ctx.lineWidth=2.2; ctx.beginPath(); for(let i=0;i<N;i++){ if(w[i]>0.002&&w[i]<=0.03){ ctx.moveTo(X(i)-CW/2,Y(h[i])); ctx.lineTo(X(i)+CW/2,Y(h[i])); } } ctx.stroke();
    ctx.strokeStyle=S.d; ctx.lineWidth=1.6; ctx.beginPath(); ctx.moveTo(9,Y(h[0])); for(let i=0;i<N;i++) ctx.lineTo(X(i),Y(h[i])); ctx.lineTo(GX1,Y(h[N-1])); ctx.stroke();
    // 水の流れる向き
    for(let i=5;i<N-5;i+=8){ if(w[i]<0.002||w[i]>0.3) continue; const sl=(h[i+3]+w[i+3])-(h[i-3]+w[i-3]); if(Math.abs(sl)<0.2) continue;
      const d=sl>0?-1:1, j0=i-d*3, j1=i+d*3; arrow(X(j0),Y(h[j0]+w[j0])-11,X(j1),Y(h[j1]+w[j1])-11,C.wd,2.4,4.6); }
    // 高い・低い・水たまり
    let im=0, il=0; for(let i=0;i<N;i++){ if(h[i]>h[im]) im=i; if(h[i]<h[il]) il=i; }
    tag('高い',clamp(X(im),30,570),Y(h[im])-12,12,'#b45309','center'); tx('低い',clamp(X(il),24,580),Math.min(338,Y(h[il])+20),12.5,'#fff','center',true);
    const pl=[]; puddles().sort((a,b)=>b.d-a.d).forEach(p=>{ const px=clamp(X(p.m),70,550); if(pl.some(q=>Math.abs(q-px)<120)) return; pl.push(px); tag('水たまり '+p.d.toFixed(1)+' cm',px,Y(h[p.m]+w[p.m])-12,11.5,C.wd,'center'); });
    tag('✋ 指で地面をなぞると、高さを変えられます',18,30,12,'#0e7490','left');
    tag(rain?'雨がふりはじめてから '+Math.floor(rainT/60)+'分':'雨がやんだ（'+Math.floor(rainT/60)+'分ふった）',624,30,12,C.ink,'right');
    tx('※高さは横の約14倍に強調',624,52,10.5,C.sub,'right',true); }
  function infoSlope(){ panel(8,354,624,108); const tr=tot.r||1e-9, pi=tot.i/tr, po=tot.o/tr, ps=Math.max(0,1-pi-po), mm=tot.r/N*10;
    tx('ふった雨のゆくえ',20,376,13.5,C.ink,'left',true); tx('ふった雨 '+mm.toFixed(1)+' mm',388,376,13,C.wd,'right',true);
    const b0=20, b1=388, by=386, seg=[[pi,SOIL[soil].d,'しみこんだ'],[po,'#2563eb','みぞへ流れた'],[ps,'#93c5fd','地面に残る']];
    ctx.fillStyle='#e2e8f0'; rr(b0,by,b1-b0,22,6); ctx.fill(); let xx=b0; ctx.save(); rr(b0,by,b1-b0,22,6); ctx.clip(); seg.forEach(s=>{ const ww=(b1-b0)*(tot.r>0?s[0]:0); ctx.fillStyle=s[1]; ctx.fillRect(xx,by,ww,22); xx+=ww; }); ctx.restore();
    seg.forEach((s,i)=>{ const x=20+i*124; ctx.fillStyle=s[1]; rr(x,424,14,14,3); ctx.fill(); tx(s[2],x+19,436,11.5,C.ink,'left',true); tx(Math.round(s[0]*100)+'%',x+19,454,13,C.ink,'left',true); });
    const f=SOIL[soil].f, msg=soil==='asph'?'アスファルトは、水がしみこまない。雨水はみぞに集まって、川へ流れていく。大雨のときは、みぞや川があふれることがある。'
      :soil==='suna'?'すな場のすなは、水がどんどんしみこむので、水たまりができにくい。':soil==='nendo'?'ねん土っぽい土は、つぶが細かく、水がほとんどしみこまない。水たまりが長く残る。'
      :'水は、高い所から低い所へ流れて、低い所に集まる。校庭の土はしみこみにくいので、水たまりができる。';
    wrap((R<=f&&soil!=='asph'?'雨の強さより、しみこむ力のほうが大きいので、ほとんどしみこむ。':'')+msg,404,376,216,12.5,C.ink,18,true); }

  // ================= ② 土のつぶの大きさとしみこみ方 =================
  // 同じカップに同じ量の土・水 100 mL を同時に注ぐ。しみこむ速さ r（mL/秒）・土にたくわえられる水 Rt（mL）・出てくるまでのおくれ tau（秒）は目安
  const CUP=[{nm:'すな',sub:'つぶが大きい',r:10,Rt:22,tau:3,c:'#e8d09a',d:'#b9944f',lc:'#d97706',gs:6.5},
             {nm:'校庭の土',sub:'つぶが中くらい',r:1.0,Rt:35,tau:12,c:'#b8915f',d:'#7a5a36',lc:'#92400e',gs:3.4},
             {nm:'ねん土っぽい土',sub:'つぶがとても小さい',r:0.12,Rt:45,tau:40,c:'#a07f68',d:'#5b4334',lc:'#7c3aed',gs:1.3}];
  const V0=100, TMAX=900, DT=0.1, NT=Math.round(TMAX/DT)+1;
  CUP.forEach(c=>{ c.O=new Float32Array(NT); let o=0; for(let k=0;k<NT;k++){ const I=Math.min(V0,c.r*k*DT), E=Math.max(0,I-c.Rt); o+=(E-o)*DT/c.tau; c.O[k]=o; } c.Ts=V0/c.r; });
  let tt=60, play=true, sp=5;
  const Ot=(c,t)=>c.O[clamp(Math.round(t/DT),0,NT-1)], It=(c,t)=>Math.min(V0,c.r*t), Tm=()=>tt<=60?60:(tt<=300?300:900);
  function drawCups(){ panel(8,8,624,268);
    CUP.forEach((c,i)=>{ const cx=112+i*208, I=It(c,tt), P=V0-I, O=Ot(c,tt), fr0=Math.min(1,I/c.Rt), rate=(Ot(c,tt+0.5)-Ot(c,tt-0.5));
      tx(c.nm,cx,32,15,C.ink,'center',true); tx(c.sub,cx,50,11.5,C.sub,'center',true);
      // 虫めがねで見たつぶ
      const mx=cx-72, my=104; ctx.save(); ctx.beginPath(); ctx.arc(mx,my,24,0,7); ctx.clip(); ctx.fillStyle='#fefce8'; ctx.fillRect(mx-24,my-24,48,48);
      for(let k=0;k<70;k++){ const gx=mx-26+hs1(k+i*97)*52, gy=my-26+hs2(k+i*97)*52, gr=c.gs*(0.7+hs1(k*3+i)*0.6); dot(gx,gy,gr,c.c,c.d); } ctx.restore();
      ctx.strokeStyle='#475569'; ctx.lineWidth=3; ctx.beginPath(); ctx.arc(mx,my,24,0,7); ctx.stroke(); ctx.lineWidth=5; ctx.lineCap='round'; ln(V(mx+17,my+17),V(mx+30,my+30)); ctx.lineCap='butt';
      tx('つぶ（拡大）',mx,my+48,10,C.sub,'center',true);
      // カップ
      const T0=66, SB=108, B0=168, xl=y=>cx-45+(y-T0)/(B0-T0)*10, xr=y=>cx+45-(y-T0)/(B0-T0)*10;
      const poly=(y0,y1)=>{ ctx.beginPath(); ctx.moveTo(xl(y0),y0); ctx.lineTo(xr(y0),y0); ctx.lineTo(xr(y1),y1); ctx.lineTo(xl(y1),y1); ctx.closePath(); };
      poly(SB,B0-2); ctx.fillStyle=c.c; ctx.fill(); const fy=SB+fr0*(B0-2-SB); if(fr0>0.01){ poly(SB,fy); ctx.fillStyle=c.d; ctx.globalAlpha=0.7; ctx.fill(); ctx.globalAlpha=1; }
      ctx.fillStyle=c.d; for(let k=0;k<40;k++){ const y=SB+3+hs2(k+i*31)*(B0-SB-8), x=xl(y)+3+hs1(k+i*31)*(xr(y)-xl(y)-6); ctx.fillRect(x,y,1.8,1.8); }
      if(P>0.3){ const wy=SB-P/V0*38; poly(wy,SB); ctx.fillStyle='rgba(59,130,246,.6)'; ctx.fill(); }
      ctx.strokeStyle='#64748b'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(xl(T0),T0); ctx.lineTo(xl(B0),B0); ctx.lineTo(xr(B0),B0); ctx.lineTo(xr(T0),T0); ctx.stroke();
      ctx.strokeStyle='#cbd5e1'; ctx.setLineDash([3,3]); ln(V(xl(B0)+2,B0-2),V(xr(B0)-2,B0-2)); ctx.setLineDash([]);
      tx('上の水',cx+52,88,10.5,C.sub,'left',true); tx(Math.round(P)+' mL',cx+52,103,12,'#2563eb','left',true);
      // しずく
      const bt=264, bw=O/V0*64, wy2=bt-bw;
      if(rate>0.02){ const nd=rate>1?4:rate>0.15?2:1; for(let k=0;k<nd;k++){ const yy=172+fr(tNow*(play?2.2:0)+k/nd)*Math.max(6,wy2-176); dot(cx+(k%3-1)*5,yy,2.6,'#3b82f6'); } }
      // ビーカー
      ctx.fillStyle='rgba(59,130,246,.65)'; if(bw>0.3) ctx.fillRect(cx-40,wy2,80,bw);
      ctx.strokeStyle='#64748b'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(cx-42,186); ctx.lineTo(cx-42,bt+2); ctx.lineTo(cx+42,bt+2); ctx.lineTo(cx+42,186); ctx.stroke();
      for(let v=20;v<=100;v+=20){ const y=bt-v/V0*64; ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1; ln(V(cx+42,y),V(cx+(v%50?36:32),y)); }
      tx('下に出た水',cx+48,226,10.5,C.sub,'left',true); tx(Math.round(O)+' mL',cx+48,244,14,c.lc,'left',true); }); }
  function drawGraph(){ panel(8,284,624,178); const tm=Tm(), X0=56, X1=612, Y0=440, Y1=322, gx=t=>X0+(X1-X0)*t/tm, gy=v=>Y0-(Y0-Y1)*v/V0;
    tx('下に出た水の量［mL］（数値は目安）',20,306,13,C.ink,'left',true);
    let lx=X1; for(let i=2;i>=0;i--){ const c=CUP[i], wd=tw(c.nm,11.5,true); tx(c.nm,lx,306,11.5,c.lc,'right',true); lx-=wd+4; ctx.strokeStyle=c.lc; ctx.lineWidth=3; ln(V(lx-20,302),V(lx,302)); lx-=32; }
    ctx.strokeStyle=C.grid; ctx.lineWidth=1; for(let v=25;v<=100;v+=25){ ln(V(X0,gy(v)),V(X1,gy(v))); } for(let v=0;v<=100;v+=25) tx(String(v),X0-6,gy(v)+4,10.5,C.sub,'right');
    const step=tm===60?10:tm===300?60:180; for(let t=0;t<=tm;t+=step){ ctx.strokeStyle=C.grid; if(t>0) ln(V(gx(t),Y0),V(gx(t),Y1)); tx(t===0?'0':(tm===60?t+'秒':(t/60)+'分'),gx(t),Y0+16,10.5,C.sub,'center'); }
    ctx.strokeStyle=C.ink; ctx.lineWidth=1.3; ctx.beginPath(); ctx.moveTo(X0,Y1-4); ctx.lineTo(X0,Y0); ctx.lineTo(X1,Y0); ctx.stroke();
    const te=Math.min(tt,tm); CUP.forEach(c=>{ ctx.strokeStyle=c.lc; ctx.lineWidth=3; ctx.beginPath(); for(let k=0;k<=300;k++){ const t=te*k/300, X=gx(t), Yv=gy(Ot(c,t)); if(k) ctx.lineTo(X,Yv); else ctx.moveTo(X,Yv); } ctx.stroke(); dot(gx(te),gy(Ot(c,te)),5,'#fff',c.lc); });
    if(tt<=tm){ ctx.setLineDash([4,4]); ctx.strokeStyle='#94a3b8'; ln(V(gx(tt),Y0),V(gx(tt),Y1)); ctx.setLineDash([]); }
    tag('注いでから '+fmtT(tt),X1,Y1+16,11.5,C.ink,'right'); }

  // ================= 共通 =================
  function draw(){ ctx.fillStyle=C.bg; ctx.fillRect(0,0,W,H); if(mode==='slope'){ drawSlope(); infoSlope(); } else { drawCups(); drawGraph(); } }
  function stats(){ const L=(id,t)=>{ K(id).textContent=t; };
    if(mode==='slope'){ const P=puddles(), md=P.reduce((a,p)=>Math.max(a,p.d),0), tr=tot.r||1e-9, mm=tot.r/N*10, pi=Math.round(tot.i/tr*100), po=Math.round(tot.o/tr*100), key='s|'+mm.toFixed(1)+'|'+P.length+'|'+md.toFixed(1)+'|'+pi+'|'+po+'|'+soil+'|'+R+'|'+rain;
      if(key===lastKey) return; lastKey=key; const ps=Math.max(0,100-pi-po);
      L('sA','ふった雨'); sh('sA',mm.toFixed(1)+' mm',rainWord(R)+'（'+R+' mm/時）'); L('sB','水たまり'); sh('sB',P.length+'か所',P.length?'いちばん深い '+md.toFixed(1)+' cm':'できていない');
      L('sC','しみこんだ水'); sh('sC',pi+' %',SOIL[soil].nm); L('sD','みぞへ流れた水'); sh('sD',po+' %','地面に残る '+ps+' %');
      setShare('【雨水のゆくえ】'+SOIL[soil].nm+'の地面に'+rainWord(R)+'（1時間に'+R+' mm）が'+Math.floor(rainT/60)+'分ふると、水は高い所から低い所へ流れて集まり、水たまりが'+P.length+'か所できた（しみこんだ水'+pi+'%・みぞへ'+po+'%）｜シミュラボ'); }
    else { const key='c|'+Math.round(tt)+'|'+CUP.map(c=>Math.round(Ot(c,tt))).join(','); if(key===lastKey) return; lastKey=key;
      ['sA','sB','sC'].forEach((id,i)=>{ const c=CUP[i], I=It(c,tt); L(id,c.nm+'：下に出た水'); sh(id,Math.round(Ot(c,tt))+' mL',I>=V0?'全部しみこんだ（'+fmtT(c.Ts)+'）':'しみこむまで '+fmtT(c.Ts)); });
      L('sD','注いでから'); sh('sD',fmtT(tt),'どれも水 100 mL'); $('tt').value=Math.round(tt); $('ttL').textContent=fmtT(tt);
      setShare('【土のつぶとしみこみ方】同じ100 mLの水が全部しみこむまで：すな約'+fmtT(CUP[0].Ts)+'、校庭の土約'+fmtT(CUP[1].Ts)+'、ねん土っぽい土'+fmtT(CUP[2].Ts)+'。つぶが大きいほど速くしみこむ（数値は目安）｜シミュラボ'); } }
  function setBtns(){ $('rainB').textContent=rain?'☔ 雨を止める':'☔ 雨をふらせる'; $('playB').textContent=play?'⏸ 止める':'▶ 進める'; }
  function setMode(m){ mode=m; drag=null; setTab(['tSlope','tCup'],m==='slope'?'tSlope':'tCup');
    ['shape','soil','R'].forEach(id=>showF(id,m==='slope')); ['tt','sp'].forEach(id=>showF(id,m==='cup'));
    show('rainB',m==='slope'); show('clrB',m==='slope'); show('pourB',m==='cup'); show('playB',m==='cup'); setBtns(); lastKey=''; stats(); draw(); }

  // ---------- 操作 ----------
  $('tSlope').addEventListener('click',()=>setMode('slope')); $('tCup').addEventListener('click',()=>setMode('cup'));
  $('shape').addEventListener('change',()=>{ shape=$('shape').value; if(shape!=='custom'){ preset(shape); } });
  $('soil').addEventListener('change',()=>{ soil=$('soil').value; });
  $('R').addEventListener('input',()=>{ R=+$('R').value; });
  $('rainB').addEventListener('click',()=>{ rain=!rain; setBtns(); });
  $('clrB').addEventListener('click',()=>{ clearW(); rain=true; setBtns(); });
  $('pourB').addEventListener('click',()=>{ tt=0; play=true; setBtns(); });
  $('playB').addEventListener('click',()=>{ if(tt>=TMAX) tt=0; play=!play; setBtns(); });
  $('tt').addEventListener('input',()=>{ tt=+$('tt').value; play=false; setBtns(); });
  $('sp').addEventListener('change',()=>{ sp=+$('sp').value; });
  function edit(P){ const hv=clamp((BY-P.y)/PX,1,48), ic=(P.x-GX0)/CW-0.5; for(let j=Math.floor(ic-7);j<=Math.ceil(ic+7);j++){ if(j<0||j>=N) continue; const g=Math.exp(-Math.pow((j-ic)/3.2,2)); h[j]+=(hv-h[j])*g*0.6; }
    if(shape!=='custom'){ shape='custom'; $('shape').value='custom'; } }
  cv.addEventListener('pointerdown',e=>{ const p=cpos(cv,e), x=p[0]/dpr, y=p[1]/dpr;
    if(mode==='slope'){ if(y>346||x<GX0||x>GX1) return; drag={}; edit(V(x,y)); }
    else { if(y<284) return; drag={tm:Tm()}; play=false; setBtns(); tt=clamp((x-56)/(612-56)*drag.tm,0,TMAX); }
    try{ cv.setPointerCapture(e.pointerId); }catch(err){} });
  cv.addEventListener('pointermove',e=>{ if(!drag) return; const p=cpos(cv,e), x=p[0]/dpr, y=p[1]/dpr;
    if(mode==='slope') edit(V(x,y)); else tt=clamp((x-56)/(612-56)*drag.tm,0,TMAX); });
  const up=()=>{ drag=null; }; cv.addEventListener('pointerup',up); cv.addEventListener('pointercancel',up);
  function frame(t){ const dt=last?Math.min(0.05,(t-last)/1000):0; last=t; tNow+=dt;
    if(mode==='slope') adv(dt*SPEED);
    else if(play){ tt=Math.min(TMAX,tt+dt*sp); if(tt>=TMAX){ play=false; setBtns(); } }
    stats(); draw(); requestAnimationFrame(frame); }
  // URLで初期状態（例 ?mode=cup&t=300 / ?shape=valley&soil=suna&R=50&min=20）
  if(Q.has('shape')&&['ex','slope','valley','flat'].indexOf(Q.get('shape'))>=0){ shape=Q.get('shape'); $('shape').value=shape; }
  if(Q.has('soil')&&SOIL[Q.get('soil')]){ soil=Q.get('soil'); $('soil').value=soil; }
  if(Q.has('R')){ R=clamp(Math.round((+Q.get('R')||30)/5)*5,5,80); $('R').value=R; $('RL').textContent=R+' mm/時'; }
  if(Q.has('t')){ tt=clamp(+Q.get('t')||0,0,TMAX); }
  preset(shape); adv(60*clamp(Q.has('min')?+Q.get('min'):15,0,60));
  setMode(Q.get('mode')==='cup'?'cup':'slope');
  requestAnimationFrame(frame);
'''

AMA_ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
<p>地面にふった雨水は、<b>高い所から低い所へと流れて、低い所に集まります</b>。だから、地面のへこんだ所に水たまりができます。また、<b>水のしみこみ方は、土のつぶの大きさによってちがいます</b>。つぶが大きいすなは水がすぐにしみこみ、つぶが小さい土ほど、しみこむのに時間がかかります。①では校庭の地面の高さを指でなぞって変え、雨の流れ方と水たまりのでき方を、②では、すな・校庭の土・ねん土っぽい土に同じ量の水を注いで、しみこむ速さを比べられます。</p>
''' + N('<b>対応する単元</b>：小学4年 B（3）雨水の行方と地面の様子「（ア）水は，高い場所から低い場所へと流れて集まること」「（イ）水のしみ込み方は，土の粒の大きさによって違いがあること」。学習指導要領解説（理科編 p.56〜57）では、雨水の流れる方向と地面の傾きとの関係を捉えること、虫眼鏡で土の粒の大きさを観察したり、粒の大きさの違う土を用いて水がしみ込むまでの時間を比べたりすることが示され、排水の仕組みや、雨水が川へと流れ込むことに触れて自然災害との関連を図ることも考えられるとされています。') + '''
<h2>授業での使い方</h2>
<h3>導入：雨のあとの校庭を思い出す</h3>
<p>雨のあとの校庭の写真を見せて、「水たまりができている所と、できていない所があるのはなぜだろう」と問いかけます。①の「地面の形」を「校庭の例」にして雨をふらせ、水がどちらへ流れ、どこに集まるかを予想してから確かめます。</p>
<h3>展開：地面のかたむきと水の流れを調べる</h3>
<p>地面を指でなぞってへこみをつくると、まわりの水がそこへ流れこんで、水たまりができます。「まっすぐなかたむき」では水たまりができずに全部みぞへ流れること、「まん中が低い」では、まん中に水が集まることを確かめます。校庭では、トレーに入れた水やビー玉で地面のかたむきを調べる活動とつなげられます（雨の日の校庭での観察は、天気の急な変化や雷に気をつけます）。</p>
<h3>まとめ：土のつぶの大きさとしみこみ方</h3>
<p>②で、すな・校庭の土・ねん土っぽい土に水を同時に注ぎ、下に出てくる水の量をグラフで比べます。虫めがねで見たつぶの大きさと結びつけ、「つぶが大きいほど、水が速くしみこむ」ことをまとめます。最後に①の「地面の土」を「アスファルト」に変えて、しみこまない地面では雨水がみぞから川へ一度に流れることを確かめ、大雨へのそなえにつなげます。</p>
<h3>児童への問いの例</h3>
<ol>
<li>雨水は、地面のどちらの方向へ流れていくだろう？水たまりができるのは、どんな所だろう？</li>
<li>すな場には水たまりができにくいのに、校庭にはできやすいのはなぜだろう？</li>
<li>町の中で、雨水を流したり、しみこませたりするために、どんなくふうがされているだろう？</li>
</ol>
<h2>しくみ・解説</h2>
<h3>言葉の意味（1文で）</h3>
<ul>
<li><b>雨水のゆくえ</b>とは、地面にふった雨水が、流れたり、しみこんだりして、どこへ行くかということです。</li>
<li><b>地面のかたむき</b>とは、地面の高さのちがいのことで、水は高い所から低い所へ流れます。</li>
<li><b>水たまり</b>とは、まわりより低い所に雨水が集まって、しみこまずに残ったものです。</li>
<li><b>しみこむ</b>とは、水が土のつぶとつぶのすき間を通って、地面の中へ入っていくことです。</li>
<li><b>つぶの大きさ</b>によって、つぶとつぶのすき間の大きさが変わるので、水のしみこみやすさが変わります。</li>
</ul>
<h3>土のつぶの大きさとしみこみ方（早見表・数値は目安）</h3>
''' + T([["すな（すな場のすな）", "大きい（約0.06〜2 mm）", "速い", "約10秒", "約78 mL"],
          ["校庭の土", "中くらい（すなと細かいつぶがまざる）", "ややおそい", "約1分40秒", "約65 mL"],
          ["ねん土っぽい土", "とても小さい（0.06 mmより小さいつぶが多い）", "とてもおそい", "約14分", "約55 mL"]],
         ["土", "つぶの大きさ", "しみこむ速さ", "100 mLが全部しみこむまで", "最後に下に出る水"]) + '''
<p>カップに同じ量の土を入れ、水100 mLを同時に注いだときの目安です。土のつまり方やかわき方、カップの大きさで時間は大きく変わるので、実際の実験では「どれが速いか」の順番に注目しましょう。注いだ水の一部は土の中にたくわえられるので、下に出てくる水は100 mLより少なくなります。</p>
<h3>なぜ、つぶが大きいと速くしみこむの？</h3>
<p>つぶが大きいと、つぶとつぶの間のすき間も大きくなり、水が通りやすくなります。つぶが小さいと、すき間がとても小さくなり、水が通りにくくなります。すな場にすなが使われているのは、雨のあとでも水たまりができにくく、早く使えるようにするためでもあります。</p>
<h3>雨の強さ（1時間にふる雨の量）</h3>
''' + T([["10〜20 mm", "やや強い雨", "ザーザーとふる"], ["20〜30 mm", "強い雨", "どしゃぶり"], ["30〜50 mm", "はげしい雨", "バケツをひっくり返したようにふる"],
          ["50〜80 mm", "ひじょうにはげしい雨", "たきのようにふる"], ["80 mm以上", "もうれつな雨", "息苦しくなるような圧迫感がある"]],
         ["1時間の雨の量", "気象庁のよび方", "ようす"]) + '''
<p>雨の量は、ふった雨がどこへも流れずにたまったときの深さ（mm）で表します。「1時間に30 mm」の雨が15分ふると、ふった雨は7.5 mmです。シミュレーターの「ふった雨のゆくえ」では、ふった雨のうち、しみこんだ水・みぞへ流れた水・地面に残っている水の割合がわかります。</p>
<h3>雨水と大雨へのそなえ</h3>
<p>町の中は、アスファルトやコンクリートの地面が多く、雨水がほとんどしみこみません。しみこまなかった雨水は、道のはしのみぞや下水を通って川へ流れていきます。短い時間に強い雨がふると、みぞや川に水が一度に集まって、あふれたり、低い土地が水につかったりすることがあります。そのため、雨水をためる池（調整池）をつくったり、水がしみこむ道（すき間の多い舗装）を使ったりするくふうがされています。また、校庭には、水はけをよくするためのかたむきやみぞがつくられています。</p>
''' + N('<b>先生向けの補足</b>：土の水の通しやすさは「透水係数」で表され、砂と粘土では千倍以上の差があります。粒の大きさの区分（砂・シルト・粘土）は分野によって境目の値が少し異なります。このシミュレーターの②は、水がしみ込む速さ（すな 10 mL/秒、校庭の土 1 mL/秒、ねん土っぽい土 0.12 mL/秒）、土が保つ水の量（22・35・45 mL）、下に出るまでの遅れを目安として与えた模式的なモデルで、実測値ではありません。①は、地面の断面（横20 m）を128に分け、となりどうしの水面の高さの差で水が移動し、地面のしみ込む力（mm/時の目安：すな150・校庭の土10・ねん土っぽい土2・アスファルト0）の分だけしみ込むとして計算しています。時間は60倍の早送りです。') + '''
<h3>このシミュレーションで単純化していること</h3>
<ul>
<li>①は地面を横から切った断面（1本の線の上）だけで計算しています。実際の校庭では、水は前後左右の低い方へ流れます。</li>
<li>①の図は、高さを横の約14倍に強調してかいています。実際のかたむきは、目で見てもわからないくらい小さいことが多いです。</li>
<li>土にしみこんだ水が、地面の中でどう動くかは表していません。しみこむ力は、雨がふり続いても変わらないものとしています。</li>
<li>②の数値は目安です。土のつまり方・かわき方・量によって、実際の時間は何倍も変わります。</li>
</ul>
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「小学校学習指導要領（平成29年告示）解説 理科編」第4学年 B（3）雨水の行方と地面の様子（''' + A(MEXT_SHO, "小学校学習指導要領・解説") + '''）</li>
<li>気象庁「雨の強さと降り方」（''' + A(JMA_AME, "気象庁 予報用語") + '''）</li>
<li>小学校理科の教科書（第4学年「雨水のゆくえと地面のようす」の単元）</li>
</ul>
'''

sim(slug="amamizu-yukue", cat="rika", emoji="☔", score=79,
    title="雨水のゆくえと地面のようすシミュレーター（水の流れ方・しみこみ方）",
    title_tag="雨水のゆくえと地面のようす シミュレーター｜地面のかたむきと水たまり・土のつぶとしみこみ方（小4理科）",
    meta_desc="校庭の地面の高さを指でなぞって雨をふらせると、水が高い所から低い所へ流れて集まり、水たまりができる。すな・校庭の土・ねん土っぽい土に同じ量の水を注いで、しみこむ速さをグラフで比べる小4理科「雨水の行方と地面の様子」の無料シミュレーター。",
    og_title="雨水のゆくえと地面のようすシミュレーター（水の流れ方・しみこみ方）",
    og_desc="雨水は高い所から低い所へ流れて集まる。土のつぶが大きいほど速くしみこむ。地面のかたむきと水たまり、土のつぶとしみこみ方を比べる小4理科の教材。",
    card_desc="地面をなぞって雨をふらせると、水は低い所に集まる。すな・土・ねん土っぽい土のしみこみ方もグラフで比べる。",
    lead="校庭の地面に雨をふらせると、水は高い所から低い所へ流れて集まります。地面の高さを指でなぞって変えて、水たまりのでき方を調べましょう。②では、すな・校庭の土・ねん土っぽい土に同じ量の水を注ぎ、しみこむ速さを比べられます。",
    model="小4 雨水の行方と地面の様子",
    level="小学4年",
    unit="小学校 第4学年 B（3）雨水の行方と地面の様子",
    canvas=canvas(640, 470, light=True),
    controls=TABS(btn("tSlope", "① 地面のかたむきと水の流れ", True) + btn("tCup", "② 土のつぶとしみこみ方"))
           + select("shape", "地面の形", [("ex", "校庭の例（でこぼこ）"), ("slope", "まっすぐなかたむき"), ("valley", "まん中が低い"), ("flat", "ほぼ平ら"), ("custom", "自分でなぞった形")])
           + select("soil", "地面の土", [("kotei", "校庭の土"), ("suna", "すな場のすな"), ("nendo", "ねん土っぽい土"), ("asph", "アスファルト")])
           + slider("R", "雨の強さ（1時間に）", 5, 80, 30, 5, "{v} mm/時")
           + FULL(slider("tt", "注いでからの時間", 0, 900, 60, 1))
           + select("sp", "早送り", [("5", "5倍"), ("1", "ふつう（1倍）"), ("20", "20倍")]),
    buttons=btn("rainB", "☔ 雨を止める", True) + btn("clrB", "↺ 水をなくす") + btn("pourB", "💧 もう一度注ぐ", True) + btn("playB", "⏸ 止める"),
    stats=stats([("sA", "ふった雨", False), ("sB", "水たまり", True), ("sC", "しみこんだ水", False), ("sD", "みぞへ流れた水", False)]),
    legend="①：地面を横から切った図（横20 m・高さは約14倍に強調）。青＝水、青い矢印＝水の流れる向き、右はしのみぞ＝はい水口。指で地面をなぞると高さを変えられます。時間は60倍の早送りです。②：上はカップ（下に小さなあな）とビーカー、左の丸は虫めがねで見たつぶ。グラフをなぞると、その時間のようすが見られます。②の数値は目安です。",
    article=AMA_ARTICLE,
    faqs=[("雨水はどのように流れますか？", "雨水は、高い所から低い所へと流れて、低い所に集まります。だから、地面のへこんだ所に水たまりができます。水の流れる向きを見ると、地面のかたむきがわかります。"),
          ("水のしみこみ方は、土によってどうちがいますか？", "土のつぶの大きさによってちがいます。つぶが大きいすなは水が速くしみこみ、つぶが小さい土ほど、しみこむのに時間がかかります。"),
          ("つぶが大きいと、なぜ水が速くしみこむのですか？", "つぶが大きいと、つぶとつぶの間のすき間も大きくなり、水が通りやすいからです。つぶが小さいと、すき間が小さくなり、水が通りにくくなります。"),
          ("すな場に水たまりができにくいのはなぜですか？", "すな場のすなは、校庭の土よりつぶが大きく、雨水がすぐに地面の中へしみこむからです。校庭の土はつぶが小さく、ふみかためられているので、しみこみにくく、水たまりができやすくなります。"),
          ("しみこみ方を比べる実験で、そろえる条件は何ですか？", "カップの大きさ、入れる土の量、注ぐ水の量、注ぎ方をそろえます。変えるのは土の種類（つぶの大きさ）だけにして、水が全部しみこむまでの時間や、下に出てきた水の量を比べます。"),
          ("雨水のゆくえは、大雨の災害とどう関係がありますか？", "アスファルトなど水がしみこまない地面では、雨水がみぞや下水から川へ一度に流れこみます。強い雨が短い時間にふると、みぞや川があふれたり、低い土地が水につかったりすることがあります。そのため、雨水をためる池や水がしみこむ道などのくふうがされています。")],
    rel=[("nagareru-mizu", "🏞️", "流れる水の働きシミュレーター"), ("kaibatsu-check", "⛰️", "うちの海抜チェッカー"), ("amagumo-now", "🌧️", "いまの雨雲マップ"),
         ("tenki-kion", "🌡️", "天気と気温"), ("chisou", "⛏️", "地層のでき方と柱状図シミュレーター")],
    js=JS_AMA)
