# -*- coding: utf-8 -*-
"""理科の授業向けシミュ：化学反応式 組み立て（2026-11-18）
   hannoushiki … 中2「化学変化と原子・分子」化学反応式（係数をつけて原子の数をそろえる）
   原子のつぶ（モデル）を係数ボタン・タップ・ドラッグで増減 → 左右の原子の数がそろったら「反応させる」で原子が組み替わるアニメ。"""
from common import T, N, P, select, btn, stats

MEXT_CHU = "https://www.mext.go.jp/a_menu/shotou/new-cs/1387016.htm"
def A(url, label): return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, label)

SIMS = []

# 問題（JSにも同じものを渡す）: (名前, ことばの式, 左辺, 右辺, 答えの係数, ヒント, 解説)
PROBS = [
    ("水の生成（水素の燃焼）", "水素 ＋ 酸素 → 水", ["H2", "O2"], ["H2O"], [2, 1, 2],
     "酸素分子 O₂ には O が2個。右の水 H₂O には O が1個しかないので、まず水を2個にしてみよう。",
     "水素と酸素の混合気体に点火すると、爆発的に反応して水ができます。O₂ の O 2個を使い切るには H₂O が2個必要で、そのための H は4個＝H₂ が2個です。"),
    ("水の電気分解", "水 → 水素 ＋ 酸素", ["H2O"], ["H2", "O2"], [2, 2, 1],
     "右の O₂ には O が2個。左の H₂O を2個にすると O がそろうよ。そのあと H を数えよう。",
     "水に電流を流すと、陰極に水素、陽極に酸素が、体積比 2：1 で発生します。この体積比は、化学反応式の係数 2H₂ と O₂ の比と同じです。"),
    ("炭素の燃焼", "炭素 ＋ 酸素 → 二酸化炭素", ["C", "O2"], ["CO2"], [1, 1, 1],
     "左と右で C と O の数を1つずつ数えてみよう。もうそろっているかも？",
     "木炭（炭素）が燃えると二酸化炭素ができます。係数がすべて1なので、1は書かずに C + O₂ → CO₂ と表します。"),
    ("マグネシウムの燃焼", "マグネシウム ＋ 酸素 → 酸化マグネシウム", ["Mg", "O2"], ["MgO"], [2, 1, 2],
     "O₂ の O 2個に合わせて、MgO を2個にしてみよう。そのあと Mg を数えよう。",
     "マグネシウムは強い光を出して燃え、白い酸化マグネシウムになります。結びつく質量の比は マグネシウム：酸素＝3：2 です。"),
    ("銅の酸化", "銅 ＋ 酸素 → 酸化銅", ["Cu", "O2"], ["CuO"], [2, 1, 2],
     "マグネシウムの燃焼と同じ形。O をそろえるには CuO がいくつ必要？",
     "銅の粉を加熱すると、黒色の酸化銅になります。結びつく質量の比は 銅：酸素＝4：1 です。"),
    ("鉄と硫黄の反応", "鉄 ＋ 硫黄 → 硫化鉄", ["Fe", "S"], ["FeS"], [1, 1, 1],
     "Fe と S の数を左右で数えてみよう。",
     "鉄粉と硫黄の粉を混ぜて加熱すると、熱と光を出して黒い硫化鉄ができます。硫化鉄は磁石につかず、うすい塩酸を加えると、においのある硫化水素が発生します。"),
    ("酸化銀の熱分解", "酸化銀 → 銀 ＋ 酸素", ["Ag2O"], ["Ag", "O2"], [2, 4, 1],
     "O₂ の O 2個に合わせると Ag₂O は2個。Ag₂O 1個に Ag は2個入っているから、銀はいくつ必要？",
     "黒色の酸化銀を加熱すると、白っぽい銀が残り、酸素が発生します。銀は、こすると金属光沢が出て、電気をよく通します。"),
    ("炭酸水素ナトリウムの熱分解", "炭酸水素ナトリウム → 炭酸ナトリウム ＋ 水 ＋ 二酸化炭素", ["NaHCO3"], ["Na2CO3", "H2O", "CO2"], [2, 1, 1, 1],
     "右の Na₂CO₃ には Na が2個。左の NaHCO₃ を2個にして、H・C・O を1つずつ数えよう。",
     "炭酸水素ナトリウム（重曹）を加熱すると、炭酸ナトリウムが残り、水と二酸化炭素が出ます。ホットケーキがふくらむのは、この二酸化炭素のためです。"),
    ("酸化銅の還元（炭素）", "酸化銅 ＋ 炭素 → 銅 ＋ 二酸化炭素", ["CuO", "C"], ["Cu", "CO2"], [2, 1, 2, 1],
     "CO₂ の O 2個はどこから来る？ CuO 1個に O は1個だよ。",
     "酸化銅と炭素の粉を混ぜて加熱すると、炭素が酸化銅から酸素をうばって二酸化炭素になり、赤色の銅が残ります。酸化銅は<b>還元</b>され、炭素は<b>酸化</b>されています。"),
    ("酸化銅の還元（水素）", "酸化銅 ＋ 水素 → 銅 ＋ 水", ["CuO", "H2"], ["Cu", "H2O"], [1, 1, 1, 1],
     "Cu・O・H を、左右で1つずつ数えてみよう。",
     "加熱した酸化銅に水素を通すと、水素が酸素をうばって水になり、銅が残ります。還元と酸化は同時に起こります。"),
    ("塩酸と水酸化ナトリウム（中和）", "塩化水素 ＋ 水酸化ナトリウム → 塩化ナトリウム ＋ 水", ["HCl", "NaOH"], ["NaCl", "H2O"], [1, 1, 1, 1],
     "H は左に2個（HCl と NaOH に1個ずつ）。右の H₂O にも2個あるかな？",
     "酸の H⁺ とアルカリの OH⁻ が結びついて水ができ（中和）、残りの Na⁺ と Cl⁻ で塩（塩化ナトリウム）ができます。ここでは物質を原子の組み合わせのモデルで表しています。"),
    ("塩化銅の電気分解", "塩化銅 → 銅 ＋ 塩素", ["CuCl2"], ["Cu", "Cl2"], [1, 1, 1],
     "CuCl₂ 1個に Cl は2個。Cl₂ にも Cl は2個だね。",
     "塩化銅水溶液に電流を流すと、陰極に赤い銅が付き、陽極からプールのようなにおいの塩素が発生します。"),
    ("塩酸の電気分解", "塩化水素 → 水素 ＋ 塩素", ["HCl"], ["H2", "Cl2"], [2, 1, 1],
     "H₂ も Cl₂ も原子が2個ずつ。HCl をいくつにすればいい？",
     "うすい塩酸に電流を流すと、陰極から水素、陽極から塩素が発生します。塩素は水にとけやすいので、集まる量は水素より少なくなります。"),
    ("メタンの燃焼（発展）", "メタン ＋ 酸素 → 二酸化炭素 ＋ 水", ["CH4", "O2"], ["CO2", "H2O"], [1, 2, 1, 2],
     "まず C、次に H（H₂O をいくつ？）、最後に O の順にそろえるのがコツ。O₂ は最後に調整しよう。",
     "都市ガスの主成分のメタンが燃えると、二酸化炭素と水ができます。原子の種類が多い反応は、1種類しか出てこない原子（ここでは C と H）から先にそろえ、単体の O₂ を最後に合わせると解きやすくなります。"),
]

STAGE = r'''
<style>
.hs{width:100%;max-width:720px;display:grid;gap:10px;min-width:0;}
.hs-top{display:flex;gap:8px;align-items:center;flex-wrap:wrap;justify-content:center;}
.hs-top select{padding:9px 10px;border-radius:10px;border:1px solid var(--line);font:inherit;font-weight:700;max-width:100%;min-width:0;}
.hs-jp{text-align:center;font-weight:800;color:var(--ink-2);font-size:14px;}
.hs-eq{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:6px 4px;}
.hs-term{display:inline-flex;align-items:center;gap:2px;background:#f8fafc;border:1px solid var(--line);border-radius:12px;padding:4px 6px;}
.hs-term button{width:34px;height:34px;border-radius:9px;border:1px solid #cbd5e1;background:#fff;font-size:19px;font-weight:900;line-height:1;cursor:pointer;color:#0e7490;padding:0;}
.hs-term button:active{transform:scale(.92);}
.hs-term .co{min-width:24px;text-align:center;font-size:24px;font-weight:900;color:#0e7490;font-variant-numeric:tabular-nums;}
.hs-term .co.one{color:#cbd5e1;}
.hs-term .co.bump{animation:hsBump .35s;}
.hs-term .f{font-size:22px;font-weight:800;margin:0 4px 0 2px;font-family:"Times New Roman",serif;}
.hs-op{font-size:22px;font-weight:900;color:#64748b;padding:0 3px;}
.hs-op.ar{color:#0e7490;}
.hs-cnt{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;}
.hs-el{display:inline-flex;align-items:center;gap:6px;border-radius:999px;padding:4px 12px 4px 5px;font-size:13px;font-weight:800;background:#fef2f2;color:#991b1b;border:1px solid #fecaca;transition:background .3s,color .3s;}
.hs-el.ok{background:#ecfdf5;color:#065f46;border-color:#a7f3d0;}
.hs-el .d{width:24px;height:24px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-size:11px;font-weight:900;box-shadow:inset 0 -2px 3px rgba(0,0,0,.25);}
.hs-msg{min-height:44px;text-align:center;font-size:14px;font-weight:700;line-height:1.6;color:var(--ink-2);background:#f8fafc;border-radius:10px;padding:8px 12px;}
.hs-msg.good{background:#ecfdf5;color:#065f46;}
.hs-msg.bad{background:#fff7ed;color:#9a3412;}
.hs-txt{text-align:center;font-size:13px;color:var(--ink-3);}
.hs-txt b{font-family:"Times New Roman",serif;font-size:17px;color:var(--ink);}
.hs-dots{display:flex;flex-wrap:wrap;gap:4px;justify-content:center;}
.hs-dots button{width:26px;height:26px;border-radius:50%;border:1px solid #cbd5e1;background:#fff;font-size:11px;font-weight:800;color:#475569;cursor:pointer;padding:0;}
.hs-dots button.ok{background:#10b981;border-color:#10b981;color:#fff;}
.hs-dots button.cur{box-shadow:0 0 0 2px #fff,0 0 0 4px #0e7490;}
canvas.lab.hs-cv{max-width:720px;background:#fff;}
#react.pulse{animation:hsPulse 1.1s infinite;}
@keyframes hsBump{50%{transform:scale(1.4);}}
@keyframes hsPulse{0%,100%{box-shadow:0 0 0 0 rgba(14,116,144,.55);}50%{box-shadow:0 0 0 10px rgba(14,116,144,0);}}
@media (max-width:520px){.hs-term .f{font-size:18px;}.hs-term .co{font-size:20px;min-width:18px;}.hs-term button{width:30px;height:30px;font-size:17px;}.hs-op{font-size:18px;padding:0 1px;}.hs-term{padding:3px 4px;}}
</style>
<div class="hs">
  <div class="hs-top"><select id="prob" aria-label="問題をえらぶ"></select></div>
  <div class="hs-dots" id="dots"></div>
  <div class="hs-jp" id="jp"></div>
  <div class="hs-eq" id="eq"></div>
  <canvas id="cv" class="lab light hs-cv" width="720" height="420" aria-label="原子のつぶのモデル。左が反応前、右が反応後"></canvas>
  <div class="hs-cnt" id="cnt"></div>
  <div class="hs-msg" id="msg"></div>
  <div class="hs-txt" id="txt"></div>
</div>
'''

JS = r'''
  const PROBS = @@PROBS@@;
  const cv=$('cv'); if(cv.clientWidth&&cv.clientWidth<520){ cv.width=440; cv.height=400; } const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr;
  const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const FONT='"Hiragino Sans","Noto Sans JP","Yu Gothic",Meiryo,sans-serif';
  const COL={H:['#ffffff','#94a3b8','#0f172a'],O:['#f87171','#b91c1c','#fff'],C:['#475569','#0f172a','#fff'],Cu:['#f59e0b','#9a3412','#fff'],Mg:['#e2e8f0','#64748b','#0f172a'],
    Fe:['#a8a29e','#44403c','#fff'],S:['#fde047','#a16207','#0f172a'],Na:['#c4b5fd','#6d28d9','#fff'],Cl:['#86efac','#15803d','#0f172a'],Ag:['#f1f5f9','#94a3b8','#0f172a']};
  const JA={H:'水素',O:'酸素',C:'炭素',Cu:'銅',Mg:'マグネシウム',Fe:'鉄',S:'硫黄',Na:'ナトリウム',Cl:'塩素',Ag:'銀'};
  const rad=el=>el==='H'?.72:(el==='Cu'||el==='Ag'||el==='Fe'||el==='Mg'||el==='Na'?1.06:1);
  const MOL={H2:[['H',-.62,0],['H',.62,0]], O2:[['O',-.85,0],['O',.85,0]], Cl2:[['Cl',-.85,0],['Cl',.85,0]],
    H2O:[['H',-.95,.55],['H',.95,.55],['O',0,-.2]], CO2:[['O',-1.6,0],['O',1.6,0],['C',0,0]],
    MgO:[['Mg',-.88,0],['O',.88,0]], CuO:[['Cu',-.88,0],['O',.88,0]], FeS:[['Fe',-.88,0],['S',.88,0]], NaCl:[['Na',-.9,0],['Cl',.9,0]],
    Ag2O:[['Ag',-1.6,0],['Ag',1.6,0],['O',0,0]], HCl:[['H',-.8,0],['Cl',.55,0]], NaOH:[['Na',-1.65,0],['H',1.2,0],['O',0,0]],
    CH4:[['H',-1.15,0],['H',1.15,0],['H',0,-1.15],['H',0,1.15],['C',0,0]],
    NaHCO3:[['H',2.15,1.4],['Na',-2.65,1.25],['O',0,-1.55],['O',-1.32,.78],['O',1.32,.78],['C',0,0]],
    Na2CO3:[['Na',-2.65,1.25],['Na',2.65,1.25],['O',0,-1.55],['O',-1.32,.78],['O',1.32,.78],['C',0,0]],
    CuCl2:[['Cl',-1.65,0],['Cl',1.65,0],['Cu',0,0]]};
  ['Fe','Cu','Mg','C','Ag','S'].forEach(e=>MOL[e]=[[e,0,0]]);
  const BB={}; for(const f in MOL){ let a=1e9,b=-1e9,c=1e9,d=-1e9; MOL[f].forEach(([e,x,y])=>{ const r=rad(e); a=Math.min(a,x-r); b=Math.max(b,x+r); c=Math.min(c,y-r); d=Math.max(d,y+r); }); BB[f]={w:b-a,h:d-c,cx:(a+b)/2,cy:(c+d)/2,r:Math.max(b-a,d-c)/2}; }
  const atomsOf=f=>{ const m={}; (f.match(/[A-Z][a-z]?\d*/g)||[]).forEach(t=>{ const e=t.match(/[A-Z][a-z]?/)[0], n=+(t.slice(e.length)||1); m[e]=(m[e]||0)+n; }); return m; };
  const SUB='₀₁₂₃₄₅₆₇₈₉'; const subU=f=>f.replace(/\d/g,d=>SUB[d]); const subH=f=>f.replace(/(\d+)/g,'<sub>$1</sub>');
  const gcd=(a,b)=>b?gcd(b,a%b):a; const MAXC=8;
  let pi=0, cur=PROBS[0], c=[], mols=[], ghosts=[], drag=null, anim=null, done=false, hintN=0, tries=0;
  let solved=new Set(); try{ (JSON.parse(localStorage.getItem('hs_ok')||'[]')).forEach(i=>solved.add(i)); }catch(e){}
  const terms=()=>cur[2].concat(cur[3]); const nL=()=>cur[2].length;
  $('prob').innerHTML=PROBS.map((p,i)=>'<option value="'+i+'">'+(i+1)+'. '+p[0]+'</option>').join('');

  // ---- 配置 ----
  const TOP=40, BOT=H-38, OPW=26, ARW=46, PAD=10;
  let L=null;
  function layout(){
    const T=terms(), n=T.length, k=nL(); const gaps=(k-1)*OPW+ARW+(n-k-1)*OPW; const cw=(W-2*PAD-gaps)/n; const CH=BOT-TOP;
    const xs=[]; let x=PAD; for(let i=0;i<n;i++){ xs.push(x); x+=cw+(i===k-1?ARW:OPW); }
    let u=W<520?22:30; const grid=[];
    T.forEach((f,i)=>{ const b=BB[f], m=c[i]; let best=0, bc=1; for(let cols=1;cols<=m;cols++){ const rows=Math.ceil(m/cols); const uu=Math.min((cw-6)/(cols*(b.w+.7)), (CH-6)/(rows*(b.h+.7))); if(uu>best){best=uu;bc=cols;} } grid.push(bc); u=Math.min(u,best); });
    const pos=T.map((f,i)=>{ const b=BB[f], m=c[i], cols=grid[i], rows=Math.ceil(m/cols); const sw=(b.w+.7)*u, sh=(b.h+.7)*u; const ox=xs[i]+cw/2-(cols*sw)/2, oy=TOP+CH/2-(rows*sh)/2; const out=[];
      for(let j=0;j<m;j++){ const r=Math.floor(j/cols), cc=j%cols; const inRow=Math.min(cols,m-r*cols); const rx=xs[i]+cw/2-(inRow*sw)/2; out.push({x:rx+(cc+.5)*sw-b.cx*u, y:oy+(r+.5)*sh-b.cy*u}); } return out; });
    L={xs,cw,u,pos,n,k};
  }
  function sync(){
    layout();
    terms().forEach((f,i)=>{ const arr=mols[i]||(mols[i]=[]); while(arr.length<c[i]){ const p=L.pos[i][arr.length]; arr.push({x:p.x,y:TOP-30,s:0,f}); } while(arr.length>c[i]){ const m=arr.pop(); ghosts.push({...m,a:1}); } });
  }

  // ---- 描画 ----
  function atom(e,x,y,r,a){ const C=COL[e]; ctx.save(); ctx.globalAlpha=a==null?1:a; const g=ctx.createRadialGradient(x-r*.35,y-r*.4,r*.1,x,y,r); g.addColorStop(0,'#fff'); g.addColorStop(.25,C[0]); g.addColorStop(1,C[1]);
    ctx.fillStyle=g; ctx.beginPath(); ctx.arc(x,y,r,0,7); ctx.fill(); ctx.strokeStyle='rgba(15,23,42,.35)'; ctx.lineWidth=1; ctx.stroke();
    if(r>=7){ ctx.fillStyle=C[2]; ctx.font='800 '+Math.round(r*(e.length>1?.78:.95))+'px '+FONT; ctx.textAlign='center'; ctx.textBaseline='middle'; ctx.fillText(e,x,y+r*.05); } ctx.restore(); }
  function mol(f,x,y,u,a,s){ const sc=s==null?1:s; MOL[f].forEach(([e,ax,ay])=>atom(e,x+ax*u*sc,y+ay*u*sc,rad(e)*u*sc*.98,a)); }
  function txt(s,x,y,sz,col,al,w){ ctx.font=(w||800)+' '+sz+'px '+FONT; ctx.fillStyle=col; ctx.textAlign=al||'center'; ctx.textBaseline='alphabetic'; ctx.fillText(s,x,y); }
  let conf=[], t0=performance.now(), last=t0;
  function frame(now){
    const dt=Math.min(.05,(now-last)/1000); last=now; const t=(now-t0)/1000;
    ctx.clearRect(0,0,W,H);
    const T=terms(), k=nL(); const xL=L.xs[k-1]+L.cw+ARW/2;
    ctx.fillStyle='#f0f9ff'; ctx.fillRect(0,0,xL,H); ctx.fillStyle='#fffbeb'; ctx.fillRect(xL,0,W-xL,H);
    txt('反応前（左辺）',xL/2,24,14,'#0369a1'); txt('反応後（右辺）',xL+(W-xL)/2,24,14,'#b45309');
    ctx.save(); ctx.fillStyle='#0e7490'; ctx.beginPath(); const ay=TOP+(BOT-TOP)/2; ctx.moveTo(xL-14,ay-5); ctx.lineTo(xL+4,ay-5); ctx.lineTo(xL+4,ay-12); ctx.lineTo(xL+16,ay); ctx.lineTo(xL+4,ay+12); ctx.lineTo(xL+4,ay+5); ctx.lineTo(xL-14,ay+5); ctx.closePath(); ctx.fill(); ctx.restore();
    for(let i=0;i<T.length-1;i++){ if(i===k-1) continue; txt('+',L.xs[i]+L.cw+OPW/2,ay+8,24,'#94a3b8'); }
    T.forEach((f,i)=>{ txt((c[i]>1?c[i]:'')+subU(f),L.xs[i]+L.cw/2,H-12,18,'#334155','center',800); });
    const flying=anim&&anim.t<1;
    // 分子
    T.forEach((f,i)=>{ const isL=i<k; (mols[i]||[]).forEach((m,j)=>{ const p=L.pos[i][j]; if(!p) return;
        if(!(drag&&drag.m===m)){ m.x+=(p.x-m.x)*Math.min(1,dt*12); m.y+=(p.y-m.y)*Math.min(1,dt*12); }
        m.s=Math.min(1,m.s+dt*4);
        const bob=Math.sin(t*2+j*1.7+i)*1.5; let a=1;
        if(anim){ if(isL) a=anim.t<1?Math.max(0,1-anim.t*6):.18; else a=anim.t<1?0:(anim.ok?Math.min(1,(anim.t-1)*4):.15); }
        if(a<=0) return;
        const sc=m.s<1?(1-Math.pow(1-m.s,3))*1.0+(m.s<1?Math.sin(m.s*Math.PI)*.15:0):1;
        mol(f,m.x,m.y+bob,L.u,a,sc); }); });
    ghosts=ghosts.filter(g=>{ g.a-=dt*3; if(g.a<=0) return false; mol(g.f,g.x,g.y-(1-g.a)*20,L.u,g.a,1+(1-g.a)*.3); return true; });
    // 反応アニメ
    if(anim){ anim.t=Math.min(anim.dur?anim.t+dt/anim.dur:1,1.3); const e=anim.t; anim.atoms.forEach((A,q)=>{ let x,y,a=1;
        if(A.x1==null){ // あまった原子：ふるえる
          const sh=e>.35?Math.sin(t*40+q)*3:0; x=A.x0+sh; y=A.y0; atom(A.e,x,y,rad(A.e)*L.u,1); if(e>.4){ ctx.strokeStyle='#ef4444'; ctx.lineWidth=2.5; ctx.beginPath(); ctx.arc(x,y,rad(A.e)*L.u+4,0,7); ctx.stroke(); } return; }
        if(e>=1){ if(!anim.ok) atom(A.e,A.x1,A.y1,rad(A.e)*L.u,1); return; }
        const p=e<.18?0:Math.min(1,(e-.18)/.72); const ee=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;
        const bx=A.x0+(e<.18?(A.x0-A.cx)*e*1.6:(A.x0-A.cx)*.29*(1-ee)), by=A.y0+(e<.18?(A.y0-A.cy)*e*1.6:(A.y0-A.cy)*.29*(1-ee));
        const mx=(bx+A.x1)/2, my=Math.min(by,A.y1)-60-q%3*18;
        x=(1-ee)*(1-ee)*bx+2*(1-ee)*ee*mx+ee*ee*A.x1; y=(1-ee)*(1-ee)*by+2*(1-ee)*ee*my+ee*ee*A.y1;
        atom(A.e,x,y,rad(A.e)*L.u,a); });
      anim.miss.forEach(M=>{ if(anim.t<.9) return; ctx.save(); ctx.setLineDash([4,3]); ctx.strokeStyle='#ef4444'; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(M.x,M.y,rad(M.e)*L.u,0,7); ctx.stroke(); ctx.restore(); txt('?',M.x,M.y+5,14,'#ef4444'); });
      if(anim.t>=1&&!anim.fin){ anim.fin=true; finish(); }
    }
    // 紙ふぶき
    conf=conf.filter(p=>{ p.vy+=dt*260; p.x+=p.vx*dt; p.y+=p.vy*dt; p.r+=p.vr*dt; if(p.y>H+20) return false; ctx.save(); ctx.translate(p.x,p.y); ctx.rotate(p.r); ctx.fillStyle=p.c; ctx.fillRect(-4,-2.5,8,5); ctx.restore(); return true; });
    if(done&&anim&&anim.ok&&anim.t>=1){ const k2=Math.min(1,(anim.t-1)*5); ctx.save(); ctx.globalAlpha=k2; ctx.fillStyle='rgba(255,255,255,.85)'; ctx.fillRect(W/2-110,TOP+4,220,50); ctx.restore(); txt('⭕ 正解！',W/2,TOP+40,30,'#059669'); }
    if(!anim&&!drag&&tries===0&&hintN===0) txt('つぶの列をタップで1つ増やす／つぶを外へドラッグで減らす',W/2,TOP+8,12,'#94a3b8','center',700);
    requestAnimationFrame(frame);
  }

  // ---- 判定 ----
  function counts(){ const T=terms(), k=nL(), Lc={}, Rc={}, order=[]; T.forEach((f,i)=>{ const a=atomsOf(f); for(const e in a){ if(!order.includes(e)) order.push(e); const tgt=i<k?Lc:Rc; tgt[e]=(tgt[e]||0)+a[e]*c[i]; } }); return {Lc,Rc,order}; }
  function balanced(){ const {Lc,Rc,order}=counts(); return order.every(e=>(Lc[e]||0)===(Rc[e]||0)); }
  function minimal(){ return c.reduce((a,b)=>gcd(a,b))===1; }
  function render(){
    const T=terms(), k=nL();
    $('jp').textContent=cur[1];
    $('eq').innerHTML=T.map((f,i)=>(i?'<span class="hs-op'+(i===k?' ar':'')+'">'+(i===k?'→':'＋')+'</span>':'')+
      '<span class="hs-term"><button data-i="'+i+'" data-d="-1" aria-label="'+subU(f)+'を1つ減らす">−</button><b class="co'+(c[i]===1?' one':'')+'" id="co'+i+'">'+c[i]+'</b><button data-i="'+i+'" data-d="1" aria-label="'+subU(f)+'を1つ増やす">＋</button><span class="f">'+subH(f)+'</span></span>').join('');
    const {Lc,Rc,order}=counts();
    $('cnt').innerHTML=order.map(e=>{ const a=Lc[e]||0,b=Rc[e]||0, C=COL[e]; return '<span class="hs-el'+(a===b?' ok':'')+'"><span class="d" style="background:'+C[0]+';color:'+C[2]+';border:1px solid '+C[1]+'">'+e+'</span>'+JA[e]+' 左'+a+'個・右'+b+'個 '+(a===b?'✓':'✗')+'</span>'; }).join('');
    $('txt').innerHTML='いまの式：<b>'+T.map((f,i)=>(i?(i===k?' → ':' ＋ '):'')+(c[i]>1?c[i]:'')+subH(f)).join('')+'</b>（係数の1は書きません）';
    const bal=balanced(); $('react').classList.toggle('pulse',bal&&!done);
    $('dots').innerHTML=PROBS.map((p,i)=>'<button data-p="'+i+'" class="'+(solved.has(i)?'ok ':'')+(i===pi?'cur':'')+'" title="'+p[0]+'">'+(i+1)+'</button>').join('');
    const bad=order.filter(e=>(Lc[e]||0)!==(Rc[e]||0));
    setStat('sQ',(pi+1)+' / '+PROBS.length); setStat('sBal',bal?'そろった ✓':bad.map(e=>e).join('・')+' がちがう'); setStat('sOk',solved.size+'問 / '+PROBS.length);
    setShare('【化学反応式 組み立て】'+PROBS.length+'問中'+solved.size+'問 正解！ いま：'+$('txt').textContent.replace('いまの式：','').replace('（係数の1は書きません）','')+'｜シミュラボ');
  }
  function msg(s,cls){ const m=$('msg'); m.innerHTML=s; m.className='hs-msg'+(cls?' '+cls:''); }
  function setC(i,v){ v=clamp(v,1,MAXC); if(v===c[i]) { if(v===MAXC) msg('係数はこのシミュレーターでは '+MAXC+' までです。'); return; } c[i]=v; anim=null; done=false; sync(); render(); const e=$('co'+i); if(e){ e.classList.remove('bump'); void e.offsetWidth; e.classList.add('bump'); }
    if(balanced()) msg(minimal()?'左右の原子の数がそろいました！ <b>▶ 反応させる</b> を押して確かめよう。':'原子の数はそろっています。でも係数は、いちばん簡単な整数の比にします（全部を同じ数でわれないか見てみよう）。','good'); else msg('原子の数を左右でくらべよう。赤い ✗ の原子がまだそろっていません。'); }
  $('eq').addEventListener('click',ev=>{ const b=ev.target.closest('button'); if(!b) return; setC(+b.dataset.i, c[+b.dataset.i]+(+b.dataset.d)); });
  $('dots').addEventListener('click',ev=>{ const b=ev.target.closest('button'); if(b) load(+b.dataset.p); });
  $('prob').addEventListener('change',()=>load(+$('prob').value));

  // ---- 反応させる ----
  function react(){
    if(anim&&anim.t<1) return; tries++;
    const T=terms(), k=nL(); const src={}, dst={};
    T.forEach((f,i)=>{ (mols[i]||[]).forEach((m,j)=>{ const p=L.pos[i][j]; MOL[f].forEach(([e,ax,ay])=>{ const o={e,x:p.x+ax*L.u,y:p.y+ay*L.u,cx:p.x,cy:p.y}; ((i<k?src:dst)[e]=(i<k?src:dst)[e]||[]).push(o); }); }); });
    const atoms=[], miss=[];
    for(const e in Object.assign({},src,dst)){ const S=(src[e]||[]).slice(), D=(dst[e]||[]).slice();
      S.sort((a,b)=>a.x-b.x); D.sort((a,b)=>a.x-b.x);
      const n=Math.min(S.length,D.length); for(let q=0;q<n;q++) atoms.push({e,x0:S[q].x,y0:S[q].y,cx:S[q].cx,cy:S[q].cy,x1:D[q].x,y1:D[q].y});
      for(let q=n;q<S.length;q++) atoms.push({e,x0:S[q].x,y0:S[q].y,cx:S[q].cx,cy:S[q].cy,x1:null});
      for(let q=n;q<D.length;q++) miss.push(D[q]); }
    const ok=balanced();
    anim={t:0,dur:1.9,atoms,miss,ok,min:minimal()};
    if(!ok){ anim.dur=1.1; }
    msg(ok?'原子が組み替わっていきます…':'反応させてみると…','');
  }
  function finish(){
    const {Lc,Rc,order}=counts();
    if(!anim.ok){ const extra=order.filter(e=>(Lc[e]||0)>(Rc[e]||0)).map(e=>e+'が'+((Lc[e]||0)-(Rc[e]||0))+'個あまります'), lack=order.filter(e=>(Lc[e]||0)<(Rc[e]||0)).map(e=>e+'が'+((Rc[e]||0)-(Lc[e]||0))+'個足りません');
      msg('原子の数が合いません：'+extra.concat(lack).join('、')+'。<br>化学変化では原子はなくなったり、新しくできたりしません。係数を直そう。','bad'); return; }
    if(!anim.min){ msg('原子は組み替わりましたが、係数がいちばん簡単な整数の比になっていません。全部の係数を同じ数でわってみよう。','bad'); return; }
    done=true; solved.add(pi); try{ localStorage.setItem('hs_ok',JSON.stringify([...solved])); }catch(e){}
    for(let q=0;q<90;q++) conf.push({x:W/2+rnd(-60,60),y:H/2,vx:rnd(-260,260),vy:rnd(-380,-120),r:rnd(0,6),vr:rnd(-8,8),c:['#f43f5e','#f59e0b','#10b981','#0ea5e9','#8b5cf6'][q%5]});
    msg('⭕ 正解！ <b>'+$('txt').querySelector('b').innerHTML+'</b><br>'+cur[6]+(pi<PROBS.length-1?'<br><b>▶ 次の問題</b> へ進もう。':'<br>全部の問題をクリアしました！'),'good');
    render();
  }
  function load(i){ pi=clamp(i,0,PROBS.length-1); cur=PROBS[pi]; c=terms().map(()=>1); mols=[]; ghosts=[]; anim=null; done=false; hintN=0; tries=0; conf=[]; $('prob').value=pi; sync();
    terms().forEach((f,i)=>mols[i].forEach((m,j)=>{ m.y=L.pos[i][j].y; m.s=1; }));
    render(); msg('係数（式の前の数）を ＋ − で変えて、左右の原子の数をそろえよう。そろったら <b>▶ 反応させる</b>。'); }
  $('react').addEventListener('click',react);
  $('next').addEventListener('click',()=>load((pi+1)%PROBS.length));
  $('hint').addEventListener('click',()=>{ hintN++; const {Lc,Rc,order}=counts(); const bad=order.filter(e=>(Lc[e]||0)!==(Rc[e]||0));
    if(hintN%2===1&&bad.length){ const e=bad[0], a=Lc[e]||0, b=Rc[e]||0, side=a<b?'左':'右', k=nL(); const cand=terms().map((f,i)=>({f,i})).filter(o=>(o.i<k)===(a<b)&&atomsOf(o.f)[e]).map(o=>subU(o.f));
      msg('💡 いま <b>'+e+'（'+JA[e]+'）</b>は 左に'+a+'個・右に'+b+'個。少ない'+side+'側の、'+e+'をふくむもの（'+cand.join('・')+'）を増やしてみよう。'); }
    else if(!bad.length&&!minimal()) msg('💡 全部の係数を同じ数でわれます。わってみよう。');
    else if(!bad.length) msg('💡 もうそろっています！ <b>▶ 反応させる</b> を押そう。','good');
    else msg('💡 '+cur[5]); });
  $('ans').addEventListener('click',()=>{ c=cur[4].slice(); anim=null; done=false; sync(); render(); msg('答えの係数にしました。<b>▶ 反応させる</b> で原子が組み替わるようすを見よう（答えを見た問題も、反応させると正解になります）。','good'); });

  // ---- つぶをタップ・ドラッグ ----
  function hitCol(x){ for(let i=0;i<L.n;i++) if(x>=L.xs[i]&&x<=L.xs[i]+L.cw) return i; return -1; }
  cv.addEventListener('pointerdown',ev=>{ if(anim&&anim.t<1) return; const [px,py]=cpos(cv,ev).map(v=>v/dpr);
    let hit=null; terms().forEach((f,i)=>(mols[i]||[]).forEach(m=>{ if(Math.hypot(px-m.x-BB[f].cx*L.u,py-m.y-BB[f].cy*L.u)<BB[f].r*L.u+4) hit={i,m}; }));
    if(hit){ drag={...hit,ox:px-hit.m.x,oy:py-hit.m.y,sx:px,sy:py}; cv.setPointerCapture(ev.pointerId); return; }
    const i=hitCol(px); if(i>=0&&py>TOP-10&&py<BOT+30) setC(i,c[i]+1); });
  cv.addEventListener('pointermove',ev=>{ if(!drag) return; const [px,py]=cpos(cv,ev).map(v=>v/dpr); drag.m.x=px-drag.ox; drag.m.y=py-drag.oy; });
  const up=ev=>{ if(!drag) return; const [px,py]=cpos(cv,ev).map(v=>v/dpr); const i=drag.i; const out=py<TOP-6||py>BOT+6||px<L.xs[i]-L.cw*.25||px>L.xs[i]+L.cw*1.25;
    const moved=Math.hypot(px-drag.sx,py-drag.sy)>12; const m=drag.m; drag=null;
    if(out&&moved){ if(c[i]>1){ const arr=mols[i]; arr.splice(arr.indexOf(m),1); arr.push(m); setC(i,c[i]-1); } else msg('係数は1より小さくできません（その物質がなくなってしまいます）。'); }
    else if(!moved) setC(i,c[i]+1); };
  cv.addEventListener('pointerup',up); cv.addEventListener('pointercancel',()=>{ drag=null; });

  const qp=+(new URLSearchParams(location.search).get('q')||0); load(qp>=1&&qp<=PROBS.length?qp-1:0);
  requestAnimationFrame(frame);
  window.__hs={PROBS, load, setC, react, get c(){return c;}, balanced, minimal, get done(){return done;}, get anim(){return anim;}, finish, solved};
'''

import json
JS = JS.replace("@@PROBS@@", json.dumps(PROBS, ensure_ascii=False))

TABLE = T([(str(i + 1), p[0], p[1], " ＋ ".join((str(p[4][j]) if p[4][j] > 1 else "") + p[2][j].translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")) for j in range(len(p[2])))
           + " → " + " ＋ ".join((str(p[4][len(p[2]) + j]) if p[4][len(p[2]) + j] > 1 else "") + p[3][j].translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")) for j in range(len(p[3]))))
          for i, p in enumerate(PROBS)], ["#", "化学変化", "ことばの式", "化学反応式"])

ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
<p>化学反応式は、化学変化を<b>化学式</b>と<b>係数</b>で表したものです。化学変化の前後で、原子の<b>種類と数は変わりません</b>（原子が組み替わるだけ）。そのため、矢印（→）の左右で原子の数が等しくなるように、化学式の前に係数をつけます。このシミュレーターでは、原子をつぶ（モデル）で表し、係数を変えると分子のつぶが増えたり減ったりします。左右の数がそろったところで「反応させる」を押すと、原子が組み替わって反応後の物質になるようすをアニメーションで確かめられます。</p>
''' + N('<b>対応する単元</b>：中学校 第1分野（4）化学変化と原子・分子「化学変化」（中学2年：化学変化を原子や分子のモデルで説明し、化学反応式で表すこと）。分解・酸化と還元・化学変化と熱・中和（中学3年）の反応も問題に入れています。') + '''
<h2>授業での使い方</h2>
<h3>導入：原子はなくなる？ 増える？</h3>
<p>第1問（水の生成）をすべて係数1のまま「反応させる」を押させると、O が1個あまって赤くふるえます。「化学変化で原子が消えることはあるかな？」と問い、原子の数をそろえる必要があることに気付かせます。</p>
<h3>展開：係数のつけ方を練習する</h3>
<p>マグネシウムの燃焼・銅の酸化・酸化銀の分解と進め、「ふくまれる原子の種類が少ない式から」「単体（O₂・H₂ など）は最後に」というコツを見つけさせます。原子の数の表示（左○個・右○個）が全部 ✓ になると「反応させる」ボタンが光ります。</p>
<h3>まとめ：モデルと式を行き来する</h3>
<p>正解すると、式とその反応の説明が出ます。ノートに式を写し、同じ反応をつぶのモデルの図でもかかせると、係数（分子の数）と化学式の右下の小さい数（分子の中の原子の数）の違いが定着します。</p>
<p><b>生徒への問いの例</b></p>
<ul>
<li>2H₂O の「2」と、H₂O の「₂」は、それぞれ何の数を表していますか？</li>
<li>H₂ + O₂ → H₂O₂ とすると原子の数はそろいますが、なぜ正しくないのでしょう？（H₂O₂ は水ではない別の物質）</li>
<li>係数を全部2倍した式（4H₂ + 2O₂ → 4H₂O）は、なぜ答えにしないのでしょう？</li>
</ul>
<h2>しくみ・解説</h2>
<h3>化学反応式のつくり方（3ステップ）</h3>
<ol>
<li>反応前の物質を左に、反応後の物質を右に、ことばの式で書く（例：水素 ＋ 酸素 → 水）。</li>
<li>それぞれを化学式にする（H₂ ＋ O₂ → H₂O）。<b>化学式の右下の数は変えてはいけません</b>（変えると別の物質になる）。</li>
<li>左右で原子の数が等しくなるように、化学式の前に係数をつける（2H₂ ＋ O₂ → 2H₂O）。係数は<b>いちばん簡単な整数の比</b>にし、1は書きません。</li>
</ol>
''' + P('係数は「分子（または物質の単位）が何個か」、化学式の右下の数は「その中に原子が何個か」。2H₂O の H の数は 2×2＝4個です。') + '''
<h3>このシミュレーターの14問</h3>
''' + TABLE + '''
<p>酸化マグネシウム（MgO）・酸化銅（CuO）・硫化鉄（FeS）・塩化ナトリウム（NaCl）・炭酸水素ナトリウムなどは、分子ではなく原子（イオン）が規則正しく並んでできた物質です。また銅・鉄・銀などの金属や炭素は、たくさんの原子が集まってできています。このシミュレーターでは、教科書のモデル図と同じように、化学式の組み合わせ1つ分をひとまとまりのつぶで表しています。つぶの大きさ・色は見分けやすくするためのもので、実際の原子の大きさの比ではありません。</p>
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「''' + A(MEXT_CHU, "中学校学習指導要領（平成29年告示）解説 理科編") + '''」第1分野（4）化学変化と原子・分子</li>
<li>中学校理科の教科書（2年「化学変化と原子・分子」、3年「化学変化とイオン」）各社</li>
</ul>
'''

FAQS = [
    ("化学反応式の係数はどうやって決めますか？", "左右で原子の数が等しくなるように決めます。①ふくまれる物質の少ない原子（1か所にしか出てこない原子）からそろえる、②O₂ や H₂ などの単体は最後に合わせる、③最後に全部の係数を同じ数でわれないか確かめて、いちばん簡単な整数の比にする、の順に進めると解きやすくなります。"),
    ("係数と化学式の右下の小さい数のちがいは何ですか？", "係数（式の前の大きい数）は、その分子（物質の単位）が何個あるかを表します。化学式の右下の小さい数は、1個の分子の中にその原子が何個あるかを表します。2H₂O は「H₂O が2個」で、H は2×2＝4個、O は2個です。"),
    ("なぜ化学式の右下の数を変えて数をそろえてはいけないのですか？", "右下の数を変えると、別の物質になってしまうからです。たとえば H₂O の O を2にすると H₂O₂（過酸化水素）という別の物質になります。数をそろえるときは、係数だけを変えます。"),
    ("係数が1のときはどう書きますか？", "1は書きません。たとえば炭素の燃焼は 1C + 1O₂ → 1CO₂ ではなく、C + O₂ → CO₂ と書きます。"),
    ("4H₂ + 2O₂ → 4H₂O は間違いですか？", "原子の数はそろっていますが、化学反応式では係数をいちばん簡単な整数の比にするきまりがあるので、全部を2でわって 2H₂ + O₂ → 2H₂O と書きます。"),
    ("水の電気分解で水素と酸素が2：1の体積で出るのはなぜですか？", "化学反応式 2H₂O → 2H₂ + O₂ のとおり、水素分子が2個できるとき酸素分子は1個できるからです。同じ温度・圧力の気体は、分子の数が同じなら体積も同じなので、体積の比も2：1になります。"),
]

SIMS.append(dict(
    slug="hannoushiki", cat="rika", emoji="⚗️", score=82,
    title="化学反応式 組み立てシミュレーター（原子のつぶで係数をそろえる・14問）",
    title_tag="化学反応式の係数シミュレーター｜原子のモデルで左右の数をそろえる練習14問（水の生成・酸化銅の還元・炭酸水素ナトリウムの分解 中2理科）",
    meta_desc="化学反応式の係数を、原子のつぶ（モデル）で増やしたり減らしたりして、左右の原子の数をそろえる練習ができるシミュレーター。そろったら「反応させる」で原子が組み替わるアニメが動く。水の生成・水の電気分解・マグネシウムや銅の酸化・酸化銅の還元・炭酸水素ナトリウムの熱分解・中和など中学の定番14問。中2理科「化学変化と原子・分子」向け。",
    og_title="化学反応式 組み立てシミュレーター｜原子のつぶで係数をそろえる",
    og_desc="係数を変えると分子のつぶが増える。左右の原子の数がそろったら「反応させる」で、原子が組み替わって新しい物質になる。中学の定番14問。",
    card_desc="係数を変えると原子のつぶが増減。左右の数がそろったら「反応させる」で原子が組み替わる。中学の定番14問。",
    lead="化学式の前の係数を ＋ − で変える（つぶの列をタップしても増やせます）と、その分子のつぶが増えたり減ったりします。下の「原子の数」が左右で全部そろったら <b>▶ 反応させる</b> を押してください。原子が飛んでいって組み替わり、反応後の物質になります。数が合わないまま反応させると、あまった原子や足りない原子が赤く表示されます。",
    model="中2 化学変化と原子・分子（化学反応式）",
    level="中学2年（中学3年の復習にも）",
    unit="中学校 第1分野（4）化学変化と原子・分子 イ（ｱ）化学変化",
    canvas=STAGE,
    controls="",
    buttons=btn("hint", "💡 ヒント") + btn("ans", "答えを見る") + btn("react", "▶ 反応させる", True) + btn("next", "次の問題 →"),
    stats=stats([("sQ", "問題", False), ("sBal", "原子の数", True), ("sOk", "正解した問題", False)]),
    legend="つぶの色：水素H＝白、酸素O＝赤、炭素C＝黒、銅Cu＝オレンジ、マグネシウムMg＝銀、鉄Fe＝灰、硫黄S＝黄、ナトリウムNa＝むらさき、塩素Cl＝緑、銀Ag＝白銀。つぶを列の外へドラッグすると1つ減らせます。正解した問題はこの端末に記録され、上の丸が緑になります。",
    article=ARTICLE, faqs=FAQS,
    rel=[("kagaku-shitsuryou", "⚖️", "化学変化と質量シミュレーター（銅・マグネシウムの酸化）"),
         ("shuukihyou", "🧪", "さわれる周期表"),
         ("chuwa-ion", "⚗️", "酸・アルカリと中和のシミュレーター"),
         ("nenshou", "🔥", "ものの燃え方と空気シミュレーター"),
         ("bunshi-katachi-3d", "⚛️", "分子の形 3Dビューア")],
    js=JS))
