// 両親媒性分子の粗視化モデル（2D・暗黙の水）。単位：長さσ、エネルギーkT
function makeLip(opt){
  const P=Object.assign({W:72,H:50,yA:7,air:true,type:1,eps:2.2,wc:1.3,KR:40,EH:12,ET:12,wT:1.4,dt:0.02,mu:0.6,kal:3,ew:6,nc:10,tw:0.5,tr:0.5,hr:0.85,anti:1,seed:0},opt||{});
  let R=Math.random;
  if(P.seed){ let a=P.seed|0; R=function(){ a=a+0x6D2B79F5|0; let t=Math.imul(a^a>>>15,1|a); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; }; }
  function gn(){ let u=0,v=0; while(!u)u=R(); while(!v)v=R(); return Math.sqrt(-2*Math.log(u))*Math.cos(6.283185307*v); }
  const SHAPES={
    1:[[0,0,1,0.78],[1.05,0,0,0.5],[2.0,0,0,0.5]],
    2:[[0,0,1,P.hr],[0.35+P.hr,-P.tw,0,P.tr],[0.35+P.hr+2*P.tr-0.05,-P.tw,0,P.tr],[0.35+P.hr,P.tw,0,P.tr],[0.35+P.hr+2*P.tr-0.05,P.tw,0,P.tr]]
  };
  let shape=null, cen=[0,0];
  function setType(t){ P.type=t; const s=SHAPES[t]; let cx=0,cy=0; s.forEach(b=>{cx+=b[0];cy+=b[1];}); cx/=s.length; cy/=s.length; cen=[cx,cy]; shape=s.map(b=>[b[0]-cx,b[1]-cy,b[2],b[3]]); }
  setType(P.type);
  const M=[]; // {x,y,th}
  function topY(){ return P.air? P.yA-2.5 : 0.8; }
  function beads(m,out){ const c=Math.cos(m.th), s=Math.sin(m.th); for(let k=0;k<shape.length;k++){ const b=shape[k]; out[k*2]=m.x+b[0]*c-b[1]*s; out[k*2+1]=m.y+b[0]*s+b[1]*c; } return out; }
  function headPos(m){ const b=shape[0], c=Math.cos(m.th), s=Math.sin(m.th); return [m.x+b[0]*c-b[1]*s, m.y+b[0]*s+b[1]*c]; }
  function add(x,y,th){ if(x==null){ for(let tr=0;tr<60;tr++){ x=R()*P.W; y=(P.air?P.yA+2.5:2.5)+R()*(P.H-(P.air?P.yA:0)-5); if(free(x,y)) break; } } M.push({x:x,y:y,th:th==null?R()*6.2832:th}); }
  function free(x,y){ for(const m of M){ let dx=m.x-x; dx-=P.W*Math.round(dx/P.W); const dy=m.y-y; if(dx*dx+dy*dy<9) return false; } return true; }
  // 作業配列
  let TQ=new Float64Array(0), NC=new Float64Array(0), GP=new Float64Array(0); let BX=new Float64Array(0), BY=BX, FX=BX, FY=BX, BR=BX, BT=new Int8Array(0), BM=new Int32Array(0);
  const CS=2.9; let NCX=1,NCY=1, head=null, next=null;
  function ensure(){ const n=M.length*shape.length; if(TQ.length<M.length) TQ=new Float64Array(M.length*2+64); if(NC.length<n){ NC=new Float64Array(n*2+64); GP=new Float64Array(n*2+64); } if(BX.length<n){ const k=Math.max(n,64)*2; BX=new Float64Array(k); BY=new Float64Array(k); FX=new Float64Array(k); FY=new Float64Array(k); BR=new Float64Array(k); BT=new Int8Array(k); BM=new Int32Array(k); next=new Int32Array(k); } NCX=Math.max(1,Math.floor(P.W/CS)); NCY=Math.max(1,Math.ceil(P.H/CS)+1); if(!head||head.length!==NCX*NCY) head=new Int32Array(NCX*NCY); }
  const tmp=new Float64Array(12);
  let Epot=0;
  function step(){
    const nb=shape.length, n=M.length*nb; ensure();
    for(let i=0;i<M.length;i++){ beads(M[i],tmp); for(let k=0;k<nb;k++){ const j=i*nb+k; let x=tmp[k*2]; x-=P.W*Math.floor(x/P.W); BX[j]=x; BY[j]=tmp[k*2+1]; FX[j]=0; FY[j]=0; BR[j]=shape[k][3]; BT[j]=shape[k][2]; BM[j]=i; } }
    head.fill(-1); TQ.fill(0); const kal=(P.type===2?P.kal:0);
    for(let j=0;j<n;j++){ const cx=Math.min(NCX-1,Math.floor(BX[j]/P.W*NCX)), cy=clampi(Math.floor(BY[j]/CS),0,NCY-1); const c=cy*NCX+cx; next[j]=head[c]; head[c]=j; }
    const eps=P.eps*(P.type===1?1.2:1), wc=P.wc, KR=P.KR, kw=Math.PI/wc, ka=eps*Math.PI/(2*wc);
    Epot=0;
    const ew=P.ew, r1=1.25, r2=2.1;
    if(ew>0){ NC.fill(0,0,n);
      for(let cy=0;cy<NCY;cy++) for(let cx=0;cx<NCX;cx++){ const c=cy*NCX+cx;
        for(let dy=0;dy<=1;dy++) for(let dx=-1;dx<=1;dx++){ if(dy===0&&dx<0) continue; const yy=cy+dy; if(yy>=NCY) continue; let xx=cx+dx; if(xx<0) xx+=NCX; else if(xx>=NCX) xx-=NCX; const c2=yy*NCX+xx;
          for(let a=head[c];a>=0;a=next[a]){ if(BT[a]) continue; for(let b=(c2===c?next[a]:head[c2]);b>=0;b=next[b]){ if(BT[b]||BM[a]===BM[b]) continue;
            let ddx=BX[b]-BX[a]; ddx-=P.W*Math.round(ddx/P.W); const ddy=BY[b]-BY[a]; const rr=ddx*ddx+ddy*ddy; if(rr>=r2*r2) continue; const r=Math.sqrt(rr);
            const wv=r<r1?1:0.5*(1+Math.cos(Math.PI*(r-r1)/(r2-r1))); NC[a]+=wv; NC[b]+=wv; } } } }
      const nc=P.nc; for(let j=0;j<n;j++){ if(BT[j]){ GP[j]=0; continue; } let wat=1, sa=0; if(P.air){ sa=1/(1+Math.exp((BY[j]-P.yA)/0.5)); wat=1-sa; } const x=NC[j]/nc; if(x<1){ const g=(1-x)*(1-x); Epot+=ew*wat*g; GP[j]=-2*ew*wat*(1-x)/nc; if(P.air) FY[j]-=ew*g*sa*(1-sa)/0.5; } else GP[j]=0; } }
    for(let cy=0;cy<NCY;cy++) for(let cx=0;cx<NCX;cx++){ const c=cy*NCX+cx;
      for(let dy=0;dy<=1;dy++) for(let dx=-1;dx<=1;dx++){ if(dy===0&&dx<0) continue; const yy=cy+dy; if(yy>=NCY) continue; let xx=cx+dx; if(xx<0) xx+=NCX; else if(xx>=NCX) xx-=NCX; const c2=yy*NCX+xx; if(NCX<3&&dx!==0) continue;
        for(let a=head[c];a>=0;a=next[a]){ for(let b=(c2===c?next[a]:head[c2]);b>=0;b=next[b]){ if(BM[a]===BM[b]) continue;
          let ddx=BX[b]-BX[a]; ddx-=P.W*Math.round(ddx/P.W); const ddy=BY[b]-BY[a]; const r2=ddx*ddx+ddy*ddy; const d0=BR[a]+BR[b];
          const both=(BT[a]===0&&BT[b]===0); const rc=both?Math.max(d0+wc,ew>0?2.1:0):d0; if(r2>=rc*rc) continue; const r=Math.sqrt(r2)+1e-9; let f=0;
          if(both&&ew>0&&r>r1&&r<2.1){ const dw=-0.5*Math.PI/(2.1-r1)*Math.sin(Math.PI*(r-r1)/(2.1-r1)); f+=-(GP[a]+GP[b])*dw*-1; }
          if(r<d0){ f+=-KR*(d0-r); if(both) Epot-=eps; } else if(both&&r<d0+wc){ f+=ka*Math.sin(kw*(r-d0)); const cc=Math.cos(Math.PI*(r-d0)/(2*wc)); Epot-=eps*cc*cc; }
          // f>0 引き合う
          if(both&&kal){ const ma=M[BM[a]], mb=M[BM[b]]; const dth=ma.th-mb.th; const c2=Math.cos(dth); if(P.anti && c2>0) {} else { const wgt=(r<d0?1:Math.pow(Math.cos(Math.PI*(r-d0)/(2*wc)),2)); const tq=-2*kal*wgt*c2*Math.sin(dth); TQ[BM[a]]+=tq; TQ[BM[b]]-=tq; Epot-=kal*wgt*c2*c2; } }
          const fx=f*ddx/r, fy=f*ddy/r; FX[a]+=fx; FY[a]+=fy; FX[b]-=fx; FY[b]-=fy; } } } }
    // 外場：水面・壁
    const yA=P.yA, w=0.35, wT=P.wT;
    for(let j=0;j<n;j++){ const y=BY[j], r=BR[j];
      if(P.air){ const s=1/(1+Math.exp((y-yA)/w)); const g=s*(1-s)/w; if(BT[j]===1){ FY[j]+=P.EH*g; if(y<yA) FY[j]+=KR*(yA-y); } else { const s2=1/(1+Math.exp((y-yA)/wT)); FY[j]-=P.ET*s2*(1-s2)/wT; } if(y<1+r) FY[j]+=KR*(1+r-y); }
      else if(y<r) FY[j]+=KR*(r-y);
      if(y>P.H-r) FY[j]-=KR*(y-(P.H-r)); }
    // 剛体のブラウン運動（過減衰）
    const dt=P.dt, mu=P.mu, mur=mu*0.45, st=Math.sqrt(2*mu*dt), sr=Math.sqrt(2*mur*dt);
    for(let i=0;i<M.length;i++){ const m=M[i]; let Fx=0,Fy=0,Tq=0; for(let k=0;k<nb;k++){ const j=i*nb+k; Fx+=FX[j]; Fy+=FY[j]; let rx=BX[j]-m.x; rx-=P.W*Math.round(rx/P.W); const ry=BY[j]-m.y; Tq+=rx*FY[j]-ry*FX[j]; }
      Tq+=TQ[i]; let dx=mu*Fx*dt/nb*2+st*gn(), dy=mu*Fy*dt/nb*2+st*gn(), dth=mur*Tq*dt/nb+sr*gn();
      const L=0.25; if(dx>L)dx=L; else if(dx<-L)dx=-L; if(dy>L)dy=L; else if(dy<-L)dy=-L; if(dth>0.25)dth=0.25; else if(dth<-0.25)dth=-0.25;
      m.x+=dx; m.y+=dy; m.th+=dth; m.x-=P.W*Math.floor(m.x/P.W); }
  }
  function clampi(v,a,b){ return v<a?a:v>b?b:v; }
  // 構造の判定
  function analyze(){
    const nb=shape.length, N=M.length; const par=new Int32Array(N); for(let i=0;i<N;i++) par[i]=i;
    const find=i=>{ while(par[i]!==i){ par[i]=par[par[i]]; i=par[i]; } return i; };
    const H=M.map(headPos), U=M.map(m=>{ const c=Math.cos(m.th),s=Math.sin(m.th); return [c,s]; }); // u：頭→尾
    const T=M.map(m=>{ const b=beads(m,new Float64Array(nb*2)); let x=0,y=0,k=0; for(let q=1;q<nb;q++){ x+=b[q*2]; y+=b[q*2+1]; k++; } return [x/k,y/k]; });
    for(let i=0;i<N;i++) for(let j=i+1;j<N;j++){ let dx=T[j][0]-T[i][0]; dx-=P.W*Math.round(dx/P.W); const dy=T[j][1]-T[i][1]; if(dx*dx+dy*dy<(P.type===1?2.0*2.0:2.6*2.6)) { const a=find(i),b=find(j); if(a!==b) par[a]=b; } }
    const surf=new Uint8Array(N);
    if(P.air) for(let i=0;i<N;i++){ if(H[i][1]>P.yA-0.6 && H[i][1]<P.yA+1.6 && U[i][1]<-0.4) surf[i]=1; }
    const groups={}; for(let i=0;i<N;i++){ if(surf[i]) continue; const r=find(i); (groups[r]=groups[r]||[]).push(i); }
    const out={N:N,surf:0,free:0,mic:0,bil:0,ves:0,small:0,list:[]}; for(let i=0;i<N;i++) if(surf[i]) out.surf++;
    for(const k in groups){ const g=groups[k]; if(g.length<=2){ out.free+=g.length; continue; }
      // 中心（周期境界を考えて）
      const ref=T[g[0]]; let cx=0,cy=0; g.forEach(i=>{ let dx=T[i][0]-ref[0]; dx-=P.W*Math.round(dx/P.W); cx+=ref[0]+dx; cy+=T[i][1]; }); cx/=g.length; cy/=g.length;
      let inw=0,outw=0,minR=1e9,maxR=0; const ang=[];
      g.forEach(i=>{ let dx=H[i][0]-cx; dx-=P.W*Math.round(dx/P.W); const dy=H[i][1]-cy; const rr=Math.hypot(dx,dy)+1e-9; const d=(U[i][0]*dx+U[i][1]*dy)/rr; if(d<-0.3) inw++; else if(d>0.3) outw++; minR=Math.min(minR,rr); maxR=Math.max(maxR,rr);
        let tx=T[i][0]-cx; tx-=P.W*Math.round(tx/P.W); ang.push(Math.atan2(T[i][1]-cy,tx)); });
      ang.sort((p,q)=>p-q); let gap=ang[0]+6.2832-ang[ang.length-1]; for(let q=1;q<ang.length;q++) gap=Math.max(gap,ang[q]-ang[q-1]);
      const S=0; let kind;
      if(g.length<6) kind='small';
      else if(outw>=4 && inw>=6 && minR>2.2 && gap<1.0) kind='ves';
      else if(inw>=g.length*0.8 && maxR<(P.type===1?4.6:5.2) && gap<1.6) kind='mic';
      else kind='bil';
      if(kind==='small') out.small+=g.length; else out[kind]++;
      out.list.push({kind:kind,n:g.length,x:cx,y:cy,r:maxR,gap:gap,inw:inw,outw:outw,minR:minR});
    }
    return out;
  }
  // 2本尾の二重層のかけら（まっすぐ）を置く：n分子、中心(x,y)、向きang
  function strip(n,x,y,ang){ const h=Math.ceil(n/2), sp=1.75, ca=Math.cos(ang), sa=Math.sin(ang); for(let k=0;k<n;k++){ const up=k<h, i=up?k:k-h, t=(i-(up?h:n-h)/2+0.5)*sp; const off=up?-2.0:2.0; const px=x+t*ca-off*sa, py=y+t*sa+off*ca; const th=ang+(up?Math.PI/2:-Math.PI/2); const c=Math.cos(th),s=Math.sin(th); M.push({x:px+cen[0]*c-cen[1]*s,y:py+cen[0]*s+cen[1]*c,th:th}); } }
  // 閉じた輪（2Dの小胞）：内側の層の頭の半径 Ri
  function ring(x,y,Ri,open){ open=open||0;  const Ro=Ri+5.0, sp=1.75; [[Ri,1],[Ro,-1]].forEach(([R,sg])=>{ const n=Math.round(2*Math.PI*R/sp); for(let k=0;k<n;k++){ const a=k/n*6.2832; if(open && Math.abs(Math.atan2(Math.sin(a+1.5708),Math.cos(a+1.5708)))<open/2) continue; const hx=x+R*Math.cos(a), hy=y+R*Math.sin(a); const th=sg>0?a:a+Math.PI; const c=Math.cos(th),s=Math.sin(th); /* 頭→尾の向き：内層は外向き、外層は内向き */ M.push({x:hx+cen[0]*c-cen[1]*s,y:hy+cen[0]*s+cen[1]*c,th:th}); } }); }
  function drop(n){ for(let k=0;k<n;k++){ let x,y; for(let tr=0;tr<40;tr++){ x=R()*P.W; y=P.yA+1.5+R()*2.5; if(free(x,y)) break; } M.push({x:x,y:y,th:-Math.PI/2+(R()-0.5)*1.5}); } }
  return {drop:drop,ring:ring,NCa:()=>NC,P:P,M:M,add:add,strip:strip,step:step,analyze:analyze,setType:setType,beads:beads,shape:()=>shape,headPos:headPos,E:()=>Epot,R:()=>R()};
}
if(typeof module!=='undefined') module.exports=makeLip;
