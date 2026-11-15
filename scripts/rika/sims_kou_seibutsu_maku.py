# -*- coding: utf-8 -*-
"""理科の授業向けシミュ（高校 生物：細胞膜）— シミュラボのリクエスト（2026-11-14 受付 714a7a7b09・1b090c2a6f）から
   maku-yuso         … 生物（2）生命現象と物質 ア（ｱ）細胞と分子 ㋑生命現象とタンパク質（膜輸送タンパク質：チャネル・担体・ポンプ）
   rinshishitsu-maku … 生物（2）生命現象と物質 ア（ｱ）細胞と分子 ㋐生体物質と細胞（生体膜・リン脂質の親水性と疎水性）
   自己集合の物理モデルは sims_kou_seibutsu_maku_lip.js（node で単体テストできるよう別ファイル）"""
import io, os
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

HERE = os.path.dirname(os.path.abspath(__file__))
MEXT_KOU = "https://www.mext.go.jp/a_menu/shotou/new-cs/1407074.htm"
def A(url, label): return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, label)

HELP = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const FF='"Hiragino Sans","Hiragino Kaku Gothic ProN","Noto Sans JP","Yu Gothic UI","Yu Gothic",Meiryo,sans-serif';
  function tx(s,x,y,size,col,align,bold){ ctx.font=(bold?'bold ':'')+size+'px '+FF; ctx.fillStyle=col; ctx.textAlign=align||'left'; ctx.fillText(s,x,y); ctx.textAlign='left'; }
  function tw(s,size,bold){ ctx.font=(bold?'bold ':'')+size+'px '+FF; return ctx.measureText(s).width; }
  function rr(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
  function pill(s,x,y,size,col,bg){ const w=tw(s,size,true)+12; rr(x-w/2,y-size+1,w,size+8,6); ctx.fillStyle=bg||'rgba(255,255,255,.88)'; ctx.fill(); tx(s,x,y+2,size,col,'center',true); }
  const fld=id=>{ const e=$(id); return e?e.closest('.field'):null; };
  function showF(id,on){ const f=fld(id); if(f) f.style.display=on?'':'none'; }
'''

# ============================================================ 1 膜輸送
YUSO_ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
<p>細胞膜は、物質を何でも通すわけではありません。酸素や二酸化炭素のような小さな分子は<b>リン脂質二重層</b>をそのまま通りぬけますが、イオンやグルコースは膜の<b>タンパク質</b>（チャネル・担体・ポンプ）を通って出入りします。チャネルと担体による輸送は濃度の高い側から低い側への<b>受動輸送</b>で、濃度差がなくなるところで出入りがつり合います。ナトリウムポンプは<b>ATPのエネルギー</b>を使って、濃度の低い側から高い側へイオンを運ぶ<b>能動輸送</b>で、細胞の内と外の濃度差をつくり出します。</p>
''' + N('<b>対応する単元</b>：高等学校「生物」（2）生命現象と物質 ア（ｱ）細胞と分子「㋑生命現象とタンパク質」。学習指導要領解説では、タンパク質が生命現象を支えている例として、酵素・<b>膜輸送タンパク質</b>・ホルモン受容体などを取り上げることが考えられるとしています。生体膜のつくり（リン脂質の親水性部分と疎水性部分）は「㋐生体物質と細胞」で扱い、姉妹編の<a href="/sims/rinshishitsu-maku/">リン脂質と細胞膜のでき方シミュレーター</a>で確かめられます。') + '''
<h2>授業での使い方</h2>
<h3>導入：何が膜を通れるか</h3>
<p>「単純拡散（O₂）」で、酸素が膜のどこからでも通りぬけ、上下の数がそろっていくことを見ます。次に「チャネル」に切り替え、カリウムイオンは膜の脂質の部分ではね返され、チャネルの穴からしか通れないことに気付かせます。「🚪 チャネルを閉じる」を押すと、出入りが止まります。</p>
<h3>展開：受動輸送と能動輸送のちがい</h3>
<p>「担体（グルコース）」では、グルコースが担体に結合し、担体の形が変わって反対側に放されるようすを観察します。細胞外を多くしても、担体の数が限られているので、運ばれる速さには上限があります。最後に「ナトリウムポンプ」に切り替えると、最初は内外で同じだったNa⁺とK⁺の数に差ができていきます。グラフで、受動輸送では2本の線が近づき（濃度差がなくなる）、ポンプでは離れていく（濃度差ができる）ことを比べさせます。ATPを0にするとポンプは止まります。</p>
<h3>まとめ：細胞のようす</h3>
<p>「細胞のようす（全部）」では、ポンプがNa⁺を外へ・K⁺を中へくみ出し、K⁺がチャネルから少しずつもれ出し、グルコースが担体で入ってくるという、実際の細胞に近い組み合わせになります。「ATPの数」を10にして始め、ATPを使い切ると何が起こるかを予想させてから確かめます（速さ×4がおすすめです）。</p>
<h3>生徒への問いの例</h3>
<ol>
<li>酸素は膜のどこからでも通れるのに、カリウムイオンはチャネルからしか通れないのはなぜだろう？（ヒント：膜の内側の疎水性の部分）</li>
<li>チャネルを開けたままにしておくと、細胞の内と外のK⁺の数はどうなるだろう？そのあと、K⁺の出入りは止まっているのだろうか？</li>
<li>ナトリウムポンプは1回の動きで、Na⁺を何個外へ、K⁺を何個中へ運んでいるだろう？そのとき何が使われているだろう？</li>
</ol>
<h2>しくみ・解説</h2>
<h3>用語</h3>
<ul>
<li><b>細胞膜</b>とは、細胞の内と外を仕切る厚さ5〜10 nmほどの膜で、<b>リン脂質二重層</b>にタンパク質がうまったつくりをしています（流動モザイクモデル）。</li>
<li><b>選択的透過性</b>とは、細胞膜が物質の種類によって通したり通さなかったりする性質のことです。</li>
<li><b>拡散</b>とは、粒子が熱運動によって、濃度の高いところから低いところへ広がっていく現象です。</li>
<li><b>受動輸送</b>とは、濃度勾配にしたがって（濃度の高い側から低い側へ）物質が移動する輸送で、エネルギー（ATP）を使いません。単純拡散と、チャネルや担体を通る輸送（促進拡散）があります。</li>
<li><b>能動輸送</b>とは、ATPなどのエネルギーを使って、濃度勾配に逆らって（濃度の低い側から高い側へ）物質を運ぶ輸送です。</li>
<li><b>チャネル</b>とは、特定のイオンだけを通す穴をもつ膜タンパク質で、開いたり閉じたりします。水を通すチャネルは<b>アクアポリン</b>とよばれます。</li>
<li><b>担体（輸送体）</b>とは、運ぶ物質と結合して形を変え、膜の反対側に放す膜タンパク質です（例：グルコース輸送体）。</li>
<li><b>ナトリウムポンプ（Na⁺/K⁺-ATPアーゼ）</b>とは、ATPを1分子分解するごとにNa⁺を3個細胞外へ、K⁺を2個細胞内へ運ぶ膜タンパク質です。</li>
</ul>
<h3>4つのしくみの比較</h3>
''' + T([["単純拡散", "リン脂質二重層", "O₂・CO₂など小さな分子、脂溶性の物質", "高い→低い", "使わない"],
          ["チャネル", "チャネル（穴）", "特定のイオン（K⁺・Na⁺など）、水（アクアポリン）", "高い→低い", "使わない"],
          ["担体", "担体（形を変える）", "グルコース・アミノ酸など", "高い→低い", "使わない"],
          ["ポンプ", "ポンプ（形を変える）", "Na⁺（外へ3個）・K⁺（中へ2個）", "低い→高い", "使う（1回にATP 1分子）"]],
         ["しくみ", "通る場所", "通る物質の例", "濃度", "ATP"]) + '''
<h3>実際の細胞の濃度（哺乳類の細胞の目安）</h3>
''' + T([["Na⁺", "約145 mmol/L", "約5〜15 mmol/L", "外が約10〜30倍"], ["K⁺", "約5 mmol/L", "約140 mmol/L", "中が約30倍"]],
         ["イオン", "細胞外", "細胞内", "差"]) + '''
<p>この濃度差はナトリウムポンプがつくり、保っています。安静にしているヒトでは、全身で使うATPのうちかなりの割合（数十％ともいわれます）がナトリウムポンプに使われています。この濃度差は、神経の興奮（活動電位）や、腸でのグルコースの吸収（Na⁺といっしょに運ぶ共輸送）にも使われます。</p>
''' + P('上下の部屋は同じ広さなので、粒子の数がそのまま濃度にあたります。粒子は熱運動を表すために、まっすぐ進んではランダムに向きを変えます。実際の大きさ・速さ・濃度の比はそのままではなく、観察しやすいように数を少なくし、膜を厚く、タンパク質を大きく描いています。イオンの電荷による力（膜電位）は考えていません。') + '''
<h2>参考</h2>
<ul class="seo-refs">
<li>''' + A(MEXT_KOU, "文部科学省「高等学校学習指導要領（平成30年告示）解説 理科編 理数編」") + ''' 生物（2）生命現象と物質</li>
<li>高等学校「生物」の教科書「細胞と分子」「膜輸送タンパク質」</li>
<li>B. Alberts ほか『Essential 細胞生物学（原書第5版）』南江堂（膜輸送の原理）</li>
</ul>
'''

YUSO_JS = HELP + r'''
  const MT=180, MB=216, YT=6, YB=394, GY=408, GH=104;   // 膜の上端・下端、部屋、グラフ
  const SP={
    o2:{nm:'O₂',col:'#dc2626',r:5},
    k:{nm:'K⁺',col:'#ea580c',r:6},
    na:{nm:'Na⁺',col:'#7c3aed',r:5.5},
    glc:{nm:'グルコース',col:'#16a34a',r:6.5}
  };
  const MODES={
    diff:{main:'o2',kind:'受動輸送',prot:[]},
    chan:{main:'k',kind:'受動輸送',prot:[['ch','k',140],['ch','k',320],['ch','k',500]]},
    carr:{main:'glc',kind:'受動輸送',prot:[['ca','glc',200],['ca','glc',440]]},
    pump:{main:'na',kind:'能動輸送',prot:[['pu','',210],['pu','',430]]},
    cell:{main:'na',kind:'受動＋能動',prot:[['ch','k',70],['ch','na',180],['ca','glc',300],['pu','',430],['pu','',560]]}
  };
  let mode='diff', parts=[], prots=[], tm=0, spd=1, paused=false, atp=60, used=0, flux={oi:0,io:0}, hist=[], gateOpen=true, flashT=0, flashX=0, last=0;
  function count(sp){ let o=0,i=0; parts.forEach(p=>{ if(p.sp!==sp||p.st!=='free') return; if(p.y<MT) o++; else i++; }); return [o,i]; }
  function mk(sp,side,x,y){ const a=Math.random()*6.2832; return {sp:sp, x:x==null?rnd(12,W-12):x, y:y==null?(side==='o'?rnd(YT+10,MT-12):rnd(MB+12,YB-10)):y, a:a, st:'free', t:0}; }
  function reset(){
    mode=$('mode').value; const M=MODES[mode]; parts=[]; tm=0; used=0; flux={oi:0,io:0}; hist=[]; gateOpen=true; atp=+$('atp').value;
    prots=M.prot.map(p=>({ty:p[0],sp:p[1],x:p[2],side:'o',ph:'idle',t:0,load:[],na:0,k:0,wait:0}));
    prots.forEach(p=>{ if(p.ty==='pu') p.side='i'; if(p.ty==='ca') p.side=Math.random()<0.5?'o':'i'; });
    const add=(sp,o,i)=>{ for(let k=0;k<o;k++) parts.push(mk(sp,'o')); for(let k=0;k<i;k++) parts.push(mk(sp,'i')); };
    if(mode==='pump'){ add('na',20,20); add('k',20,20); }
    else if(mode==='cell'){ add('na',30,8); add('k',8,30); add('glc',14,4); add('o2',14,4); }
    else add(M.main,+$('nOut').value,+$('nIn').value);
    const isAtp=(mode==='pump'||mode==='cell'), isCh=(mode==='chan'||mode==='cell');
    showF('nOut',!isAtp); showF('nIn',!isAtp); showF('atp',isAtp); $('gate').style.display=isCh?'':'none'; $('addAtp').style.display=isAtp?'':'none';
    $('gate').textContent='🚪 チャネルを閉じる';
    stats(); draw();
  }
  // ---- 物理 ----
  const V=70;
  function moveFree(p,dt){
    if(Math.random()<2.2*dt) p.a+=randn()*1.6;
    let nx=p.x+Math.cos(p.a)*V*dt, ny=p.y+Math.sin(p.a)*V*dt; const r=SP[p.sp].r;
    if(nx<r){ nx=r; p.a=Math.PI-p.a; } else if(nx>W-r){ nx=W-r; p.a=Math.PI-p.a; }
    if(p.y<MT){ // 細胞外
      if(ny<YT+r){ ny=YT+r; p.a=-p.a; }
      if(ny>MT-r){ if(!tryCross(p,'o')){ ny=MT-r; p.a=-p.a; } else return; }
    } else {
      if(ny>YB-r){ ny=YB-r; p.a=-p.a; }
      if(ny<MB+r){ if(!tryCross(p,'i')){ ny=MB+r; p.a=-p.a; } else return; }
    }
    p.x=nx; p.y=ny;
  }
  function startCross(p,from,x,dur){ p.st='cross'; p.from=from; p.cx=x; p.t=0; p.dur=dur; p.x0=p.x; }
  function tryCross(p,from){
    if(p.sp==='o2'){ if(Math.random()<0.45){ startCross(p,from,p.x,0.45); return true; } return false; }
    for(const q of prots){ if(q.ty==='ch' && q.sp===p.sp && Math.abs(p.x-q.x)<13){ if(gateOpen){ startCross(p,from,q.x,0.32); return true; } } }
    return false;
  }
  function stepCross(p,dt){ p.t+=dt; const f=Math.min(1,p.t/p.dur); const r=SP[p.sp].r;
    const y0=p.from==='o'?MT-r:MB+r, y1=p.from==='o'?MB+r:MT-r; p.x=p.x0+(p.cx-p.x0)*Math.min(1,f*3); if(p.sp==='o2') p.x=p.cx+Math.sin(f*9)*2; p.y=y0+(y1-y0)*f;
    if(f>=1){ p.st='free'; p.a=p.from==='o'?rnd(0.4,2.7):rnd(-2.7,-0.4); if(p.sp===MODES[mode].main||mode==='cell'&&p.sp==='na'){} if(p.from==='o') flux.oi+=(p.sp===mainSp()?1:0); else flux.io+=(p.sp===mainSp()?1:0); } }
  function mainSp(){ return MODES[mode].main; }
  function mouth(q,side){ return [q.x, side==='o'?MT-6:MB+6]; }
  function grab(q,sp,side,rad){ const m=mouth(q,side); let best=null,bd=rad*rad; parts.forEach(p=>{ if(p.st!=='free'||p.sp!==sp||p.cool>0) return; if(side==='o'?p.y>MT:p.y<MB) return; const d=(p.x-m[0])**2+(p.y-m[1])**2; if(d<bd){ bd=d; best=p; } }); return best; }
  function release(q,p,side){ const m=mouth(q,side); p.st='free'; p.cool=1.2; p.x=m[0]+rnd(-8,8); p.y=side==='o'?MT-SP[p.sp].r-4:MB+SP[p.sp].r+4; p.a=side==='o'?rnd(-2.7,-0.4):rnd(0.4,2.7); }
  function stepProt(q,dt){
    q.t+=dt;
    if(q.ty==='ca'){
      if(q.ph==='idle'){ const p=grab(q,'glc',q.side,17); if(p){ p.st='bound'; q.load=[p]; q.ph='flip'; q.t=0; q.from=q.side; } else if(Math.random()<0.6*dt){ q.ph='flip'; q.t=0; q.from=q.side; } }
      else if(q.ph==='flip' && q.t>0.6){ q.side=q.side==='o'?'i':'o'; q.ph='idle'; q.t=0; q.load.forEach(p=>{ release(q,p,q.side); if(p.sp===mainSp()){ if(q.side==='i') flux.oi++; else flux.io++; } }); q.load=[]; }
    } else if(q.ty==='pu'){
      if(q.ph==='idle' && q.side==='i'){ if(q.load.filter(p=>p.sp==='na').length<3){ const p=grab(q,'na','i',32); if(p){ p.st='bound'; q.load.push(p); } }
        else if(atp>0){ atp--; used++; flashT=0.9; flashX=q.x; q.ph='flip'; q.t=0; } }
      else if(q.ph==='idle' && q.side==='o'){ if(q.load.filter(p=>p.sp==='k').length<2){ const p=grab(q,'k','o',32); if(p){ p.st='bound'; q.load.push(p); } } else { q.ph='flip'; q.t=0; } }
      else if(q.ph==='flip' && q.t>0.6){ q.side=q.side==='o'?'i':'o'; q.ph='idle'; q.t=0; const keep=[];
        q.load.forEach(p=>{ if((q.side==='o'&&p.sp==='na')||(q.side==='i'&&p.sp==='k')){ release(q,p,q.side); if(p.sp===mainSp()){ if(q.side==='i') flux.oi++; else flux.io++; } } else keep.push(p); }); q.load=keep; }
    }
  }
  function step(dt){ tm+=dt; parts.forEach(p=>{ if(p.cool>0) p.cool-=dt; if(p.st==='free') moveFree(p,dt); else if(p.st==='cross') stepCross(p,dt); }); prots.forEach(q=>stepProt(q,dt)); if(flashT>0) flashT-=dt;
    if(!hist.length || tm-hist[hist.length-1].t>=0.25){ const h={t:tm}; ['o2','k','na','glc'].forEach(s=>{ h[s]=count(s); }); hist.push(h); if(hist.length>400) hist.shift(); } }
  // ---- 描画 ----
  function drawPart(p){ const s=SP[p.sp], r=s.r;
    if(p.sp==='o2'){ ctx.fillStyle=s.col; ctx.beginPath(); ctx.arc(p.x-2.6,p.y,r*0.72,0,6.3); ctx.arc(p.x+2.6,p.y,r*0.72,0,6.3); ctx.fill(); return; }
    if(p.sp==='glc'){ ctx.fillStyle=s.col; ctx.beginPath(); for(let k=0;k<6;k++){ const a=k*1.0472+0.5236; ctx.lineTo(p.x+r*Math.cos(a),p.y+r*Math.sin(a)); } ctx.closePath(); ctx.fill(); ctx.strokeStyle='#14532d'; ctx.lineWidth=1; ctx.stroke(); return; }
    ctx.fillStyle=s.col; ctx.beginPath(); ctx.arc(p.x,p.y,r,0,6.3); ctx.fill(); ctx.strokeStyle='#fff'; ctx.lineWidth=1.4; ctx.beginPath(); ctx.moveTo(p.x-2.6,p.y); ctx.lineTo(p.x+2.6,p.y); ctx.moveTo(p.x,p.y-2.6); ctx.lineTo(p.x,p.y+2.6); ctx.stroke(); }
  function drawMembrane(){
    const holes=prots.map(q=>[q.x-20,q.x+20]);
    ctx.lineCap='round';
    for(let x=6;x<W;x+=11){ if(holes.some(h=>x>h[0]&&x<h[1])) continue;
      ctx.strokeStyle='#e6b422'; ctx.lineWidth=1.6; ctx.beginPath(); ctx.moveTo(x-1.5,MT+5); ctx.lineTo(x-1.5,MT+16); ctx.moveTo(x+1.5,MT+5); ctx.lineTo(x+1.5,MT+16); ctx.moveTo(x-1.5,MB-5); ctx.lineTo(x-1.5,MB-16); ctx.moveTo(x+1.5,MB-5); ctx.lineTo(x+1.5,MB-16); ctx.stroke();
      ctx.fillStyle='#e0483e'; ctx.beginPath(); ctx.arc(x,MT+4,4.3,0,6.3); ctx.fill(); ctx.beginPath(); ctx.arc(x,MB-4,4.3,0,6.3); ctx.fill(); }
  }
  function drawProt(q){ const x=q.x, f=q.ph==='flip'?Math.min(1,q.t/0.6):0;
    if(q.ty==='ch'){ const col=q.sp==='k'?'#fb923c':'#a78bfa', dk=q.sp==='k'?'#9a3412':'#5b21b6';
      ctx.fillStyle=col; rr(x-20,MT-4,15,MB-MT+8,6); ctx.fill(); rr(x+5,MT-4,15,MB-MT+8,6); ctx.fill();
      if(!gateOpen){ ctx.fillStyle=dk; rr(x-6,MT+8,12,10,3); ctx.fill(); }
      tx((q.sp==='k'?'K⁺':'Na⁺')+'チャネル',x,MT-10,10,dk,'center',true); return; }
    if(q.ty==='ca'){ // 開いている側に口を向けたV字。flip中は形が変わる
      const s=q.ph==='flip'?(q.from==='o'?1-2*f:-1+2*f):(q.side==='o'?1:-1); // 1=上に開く
      const top=s>0?22:6, bot=s>0?6:22;
      ctx.fillStyle='#86efac'; ctx.beginPath(); ctx.moveTo(x-24,MT-4); ctx.lineTo(x-top/2-2,MT-4); ctx.lineTo(x-bot/2-2,MB+4); ctx.lineTo(x-24,MB+4); ctx.closePath(); ctx.fill();
      ctx.beginPath(); ctx.moveTo(x+24,MT-4); ctx.lineTo(x+top/2+2,MT-4); ctx.lineTo(x+bot/2+2,MB+4); ctx.lineTo(x+24,MB+4); ctx.closePath(); ctx.fill();
      ctx.strokeStyle='#15803d'; ctx.lineWidth=1.2; ctx.stroke();
      q.load.forEach(p=>{ p.x=x; p.y=(MT+MB)/2; drawPart(p); });
      tx('担体',x,MT-10,10,'#15803d','center',true); return; }
    if(q.ty==='pu'){ const s=q.ph==='flip'?(q.side==='i'?f:1-f):(q.side==='o'?1:0);
      ctx.fillStyle='#fda4af'; rr(x-26,MT-8,52,MB-MT+16,10); ctx.fill(); ctx.strokeStyle='#be123c'; ctx.lineWidth=1.4; ctx.stroke();
      const cy=MT+(MB-MT)*(1-s)*0.5+ (MB-MT)*0.25; ctx.fillStyle='#fff1f2'; rr(x-14,cy-9,28,18,6); ctx.fill();
      const na=q.load.filter(p=>p.sp==='na'), k=q.load.filter(p=>p.sp==='k');
      na.forEach((p,i)=>{ p.x=x-9+i*9; p.y=cy-2; drawPart(p); }); k.forEach((p,i)=>{ p.x=x-5+i*10; p.y=cy+4; drawPart(p); });
      tx('ポンプ',x,MT-12,10,'#be123c','center',true);
      if(q.side==='i'&&q.ph==='idle'&&na.length===3&&atp<=0) pill('ATPがない',x,MB+26,10,'#be123c');
      return; }
  }
  function drawGraph(){ const gx=46, gw=W-60, gy=GY, gh=GH; ctx.fillStyle='#fff'; ctx.fillRect(0,GY-6,W,H-GY+6);
    ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; ctx.strokeRect(gx,gy,gw,gh);
    const sps=(mode==='pump'||mode==='cell')?['na','k']:[mainSp()];
    let mx=10; hist.forEach(h=>sps.forEach(s=>{ mx=Math.max(mx,h[s][0],h[s][1]); })); mx=Math.ceil(mx/10)*10;
    tx(String(mx),gx-6,gy+9,10,'#64748b','right'); tx('0',gx-6,gy+gh,10,'#64748b','right'); tx('数',gx-30,gy+gh/2+4,10,'#64748b','left');
    const win=60, t1=Math.max(win,tm), t0=t1-win; tx('時間（秒）→ 直近60秒',gx+gw,gy+gh+0,9,'#94a3b8','right');
    sps.forEach(s=>{ [0,1].forEach(side=>{ ctx.strokeStyle=SP[s].col; ctx.lineWidth=side?2.4:1.8; ctx.setLineDash(side?[]:[5,4]); ctx.beginPath(); let st=false;
      hist.forEach(h=>{ if(h.t<t0) return; const X=gx+(h.t-t0)/win*gw, Y=gy+gh-h[s][side]/mx*gh; if(!st){ ctx.moveTo(X,Y); st=true; } else ctx.lineTo(X,Y); }); ctx.stroke(); }); });
    ctx.setLineDash([]);
    let lx=gx+6; sps.forEach(s=>{ tx(SP[s].nm+'：',lx,gy+13,10,SP[s].col,'left',true); lx+=tw(SP[s].nm+'：',10,true); ctx.strokeStyle=SP[s].col; ctx.lineWidth=2.4; ctx.beginPath(); ctx.moveTo(lx,gy+9); ctx.lineTo(lx+16,gy+9); ctx.stroke(); tx('細胞内',lx+19,gy+13,10,'#334155'); lx+=58; ctx.setLineDash([5,4]); ctx.lineWidth=1.8; ctx.beginPath(); ctx.moveTo(lx,gy+9); ctx.lineTo(lx+16,gy+9); ctx.stroke(); ctx.setLineDash([]); tx('細胞外',lx+19,gy+13,10,'#334155'); lx+=66; });
  }
  function draw(){
    ctx.clearRect(0,0,W,H);
    ctx.fillStyle='#eff6ff'; ctx.fillRect(0,0,W,MT); ctx.fillStyle='#fefce8'; ctx.fillRect(0,MB,W,YB-MB+6);
    drawMembrane(); prots.forEach(drawProt);
    parts.forEach(p=>{ if(p.st!=='bound') drawPart(p); });
    const sps=(mode==='pump'||mode==='cell')?['na','k','glc','o2']:[mainSp()];
    const lab=(side)=>sps.filter(s=>parts.some(p=>p.sp===s)).map(s=>SP[s].nm+' '+count(s)[side]).join('　');
    pill('細胞外　'+lab(0),W/2,22,12,'#1e3a8a'); pill('細胞内　'+lab(1),W/2,YB-8,12,'#713f12');
    if(flashT>0) pill('ATP → ADP＋リン酸',flashX,MT-30,11,'#be123c','rgba(255,241,242,.95)');
    if(paused) pill('一時停止中',W-60,22,11,'#334155');
    drawGraph();
  }
  function stats(){ const ms=mainSp();
    if(mode==='pump'||mode==='cell'){ const a=count('na'), b=count('k'); setStat('sA','Na⁺ '+a[0]+':'+a[1]+'・K⁺ '+b[0]+':'+b[1]); }
    else { const c=count(ms); setStat('sA',SP[ms].nm+' '+c[0]+'：'+c[1]); }
    setStat('sB',SP[ms].nm+' '+flux.oi+' ／ '+flux.io);
    setStat('sC',MODES[mode].kind);
    setStat('sD',(mode==='pump'||mode==='cell')?(used+' ／ '+atp):'使わない');
    const c=count(ms); setShare('【膜輸送】'+MODES[mode].kind+'：'+SP[ms].nm+'の数 細胞外'+c[0]+'・細胞内'+c[1]+(used?'（ATP '+used+'個使用）':'')+'｜シミュラボ');
  }
  function loop(ts){ const dt=Math.min(0.05,(ts-(last||ts))/1000); last=ts;
    if(!paused){ const n=Math.max(1,Math.round(spd*2)); for(let k=0;k<n;k++) step(dt*spd/n); }
    draw(); if(Math.floor(tm*4)!==Math.floor((tm-dt*spd)*4)) stats(); requestAnimationFrame(loop); }
  ['mode','nOut','nIn','atp'].forEach(id=>$(id).addEventListener('change',reset));
  ['nOut','nIn','atp'].forEach(id=>$(id).addEventListener('input',reset));
  $('spd').addEventListener('change',()=>{ spd=+$('spd').value; });
  $('pause').addEventListener('click',()=>{ paused=!paused; $('pause').textContent=paused?'▶ 再開':'⏸ 一時停止'; });
  $('rst').addEventListener('click',reset);
  $('gate').addEventListener('click',()=>{ gateOpen=!gateOpen; $('gate').textContent=gateOpen?'🚪 チャネルを閉じる':'🚪 チャネルを開く'; });
  $('addAtp').addEventListener('click',()=>{ atp+=20; stats(); });
  cv.addEventListener('pointerdown',e=>{ const c=cpos(cv,e); const x=c.x/dpr, y=c.y/dpr; if(y<YT||y>YB||(y>MT-4&&y<MB+4)) return; const sp=(mode==='pump'||mode==='cell')?(y<MT?'na':'k'):mainSp(); const p=mk(sp,y<MT?'o':'i',clamp(x,10,W-10),y); parts.push(p); stats(); });
  window.__yuso={ step:(n,dt)=>{ for(let k=0;k<n;k++) step(dt||0.05); stats(); draw(); }, count:count, st:()=>({mode:mode,tm:tm,atp:atp,used:used,flux:flux}) };
  reset(); requestAnimationFrame(loop);
'''

sim(slug="maku-yuso", cat="rika", emoji="🚪", score=80,
    title="膜輸送のシミュレーター（拡散・チャネル・担体・ナトリウムポンプ）",
    title_tag="膜輸送のシミュレーター｜受動輸送と能動輸送、チャネル・担体・ナトリウムポンプの働き（高校生物）",
    meta_desc="細胞膜をはさんだ細胞外と細胞内で、O₂の単純拡散、K⁺チャネル、グルコースの担体、ATPを使うナトリウムポンプ（Na⁺/K⁺-ATPアーゼ）の働きを粒子の動きで比べられるシミュレーター。受動輸送では濃度差がなくなり、能動輸送では濃度差ができる様子をグラフで確認。高校「生物」細胞と分子の授業向け。",
    og_title="膜輸送のシミュレーター（拡散・チャネル・担体・ナトリウムポンプ）",
    og_desc="O₂は膜をそのまま通り、K⁺はチャネルだけを通り、グルコースは担体が形を変えて運ぶ。ナトリウムポンプはATPを使ってNa⁺を外へ3個・K⁺を中へ2個。受動輸送と能動輸送のちがいがグラフでわかる。",
    card_desc="単純拡散・チャネル・担体・ナトリウムポンプを切り替えて、受動輸送と能動輸送のちがいを粒子とグラフで比べる。",
    lead="細胞膜をはさんで、上が細胞外、下が細胞内です。輸送のしくみを切り替えると、O₂が膜をそのまま通りぬける単純拡散、K⁺がチャネルの穴だけを通る様子、グルコースが担体に結合して反対側に運ばれる様子、ナトリウムポンプがATPを使ってNa⁺とK⁺を濃度差に逆らって運ぶ様子を観察できます。下のグラフで、細胞外と細胞内の数の変化を比べられます。",
    model="生物 細胞と分子（膜輸送タンパク質・受動輸送と能動輸送）",
    level="高校（生物）、生物基礎の発展",
    unit="高等学校 生物（2）生命現象と物質 ア（ｱ）細胞と分子 ㋑生命現象とタンパク質",
    canvas=canvas(640, 520, light=True),
    controls=select("mode", "輸送のしくみ", [("diff", "単純拡散（O₂）"), ("chan", "チャネル（K⁺）"), ("carr", "担体（グルコース）"),
                                              ("pump", "ナトリウムポンプ（Na⁺・K⁺）"), ("cell", "細胞のようす（全部）")])
             + slider("nOut", "細胞外の数（はじめ）", 0, 60, 40, 1)
             + slider("nIn", "細胞内の数（はじめ）", 0, 60, 4, 1)
             + slider("atp", "ATPの数（はじめ）", 0, 150, 60, 1)
             + select("spd", "速さ", [("1", "×1"), ("2", "×2"), ("4", "×4"), ("0.5", "×0.5（ゆっくり）")]),
    buttons=btn("pause", "⏸ 一時停止", True) + btn("rst", "↺ はじめから") + btn("gate", "🚪 チャネルを閉じる") + btn("addAtp", "＋ATP 20"),
    stats=stats([("sA", "粒子の数（細胞外：細胞内）", True), ("sB", "膜を通った数（外→内／内→外）", False), ("sC", "輸送のしかた", False), ("sD", "ATP（使った／残り）", False)]),
    legend="上＝細胞外、下＝細胞内、まん中＝細胞膜（赤い丸＝リン脂質の親水性の部分、黄色の線＝疎水性の部分）。赤い2つの丸＝O₂、オレンジ＝K⁺、紫＝Na⁺、緑の六角形＝グルコース。オレンジ・紫の筒＝チャネル、緑＝担体、ピンク＝ナトリウムポンプ。上下の部屋は同じ広さなので、数＝濃度。部屋をタップすると粒子を1個足せます。グラフの実線＝細胞内、点線＝細胞外。",
    article=YUSO_ARTICLE,
    faqs=[("受動輸送と能動輸送のちがいは？", "受動輸送は、濃度の高い側から低い側へ、濃度勾配にしたがって物質が移動する輸送で、ATPなどのエネルギーを使いません（単純拡散、チャネル、担体）。能動輸送は、ATPのエネルギーを使って濃度勾配に逆らい、濃度の低い側から高い側へ物質を運ぶ輸送です（ナトリウムポンプなど）。"),
          ("酸素は膜を通れるのに、イオンが通れないのはなぜ？", "細胞膜の内側はリン脂質の疎水性の部分（脂肪酸の尾）でできています。酸素や二酸化炭素のような小さく電荷をもたない分子はこの部分に溶けこんで通りぬけられますが、電荷をもつイオンや大きな極性分子は疎水性の部分を通りにくいため、チャネルや担体などのタンパク質を通って移動します。"),
          ("チャネルと担体のちがいは？", "チャネルは膜に穴をつくるタンパク質で、開いているあいだ特定のイオンが次々に通りぬけます。担体は運ぶ物質と結合して形を変え、反対側に放すタンパク質で、1回ごとに形を変える必要があるため、運ぶ速さには上限があります。どちらも濃度勾配にしたがう受動輸送です。"),
          ("ナトリウムポンプは何をしているの？", "ATPを1分子分解するごとに、Na⁺を3個細胞外へ、K⁺を2個細胞内へ運びます。これにより、細胞外はNa⁺が多く、細胞内はK⁺が多いという濃度差がつくられ、保たれています。この濃度差は神経の興奮や、グルコースなどの吸収に使われます。"),
          ("濃度差がなくなったら、粒子の出入りは止まるの？", "止まりません。粒子は熱運動を続けているので、両側から同じくらいの数が出入りし、全体として数が変わらなくなります（動的平衡）。シミュレーターの「膜を通った数」で、外→内と内→外の両方が増え続けることを確かめられます。"),
          ("水はどうやって細胞膜を通るの？", "水分子は小さいので脂質二重層を少しずつ通りぬけますが、多くの細胞では、水を通すチャネルであるアクアポリンを通って速く出入りします。アクアポリンを発見したピーター・アグレは2003年にノーベル化学賞を受賞しました。")],
    rel=[("rinshishitsu-maku", "🧼", "リン脂質と細胞膜のでき方シミュレーター"), ("diffusion", "🫧", "拡散シミュレーター"),
         ("hito-karada", "🫀", "人の体のシミュレーター"), ("kougousei", "🍃", "光合成と呼吸のシミュレーター"), ("saibou-bunretsu", "🔬", "細胞分裂のシミュレーター")],
    js=YUSO_JS)



# ============================================================ 2 リン脂質の自己集合（ミセル・二重層・小胞）
LIP_CORE = io.open(os.path.join(HERE, "sims_kou_seibutsu_maku_lip.js"), encoding="utf-8").read().replace("if(typeof module!=='undefined') module.exports=makeLip;", "")

LIP_ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
<p>セッケンやリン脂質の分子は、水になじむ<b>親水性の部分（頭）</b>と、水をきらう<b>疎水性の部分（尾）</b>を1つの分子の中にあわせもっています（両親媒性分子）。水の中では、疎水性の尾が水にふれないように集まり、親水性の頭が外側の水に向くように並びます。その結果、<b>水面では尾を空気側に向けて1層に並び</b>（単分子膜）、水中では、尾が1本の分子は<b>ミセル</b>、尾が2本のリン脂質は<b>脂質二重層</b>になりやすくなります。閉じた二重層（<b>小胞</b>）は、内側にも水を包みこんだまま安定に保たれます。細胞膜がリン脂質二重層でできているのは、分子の性質と水との相互作用によって、ひとりでにこの構造ができるからです。</p>
''' + N('<b>対応する単元</b>：高等学校「生物」（2）生命現象と物質 ア（ｱ）細胞と分子「㋐生体物質と細胞」。学習指導要領解説では、親水性の物質と疎水性の物質が基本的には混じり合わないこと、生体膜を構成するリン脂質は分子の中に親水性の部分と疎水性の部分の両方をもっていることを示す資料に基づいて、細胞が安定してその構造を保てる理由を考察させることや、洗剤の働きやシャボン玉の構造など身近な例を取り上げることが考えられるとしています。化学（油脂とセッケン）の界面活性剤の学習にも使えます。膜をはさんだ物質の出入りは<a href="/sims/maku-yuso/">膜輸送のシミュレーター</a>で確かめられます。') + '''
<h2>授業での使い方</h2>
<h3>導入：水面に分子を落とす</h3>
<p>「はじめの状態」を「水面に落とす」、分子の数を10個にして始めます。分子が尾を空気側に向けて水面に並ぶことを確かめ、なぜ逆向き（頭が空気側）にならないのかを考えさせます。「＋10個入れる」で少しずつ増やしていくと、水面がすき間なく埋まったあとに入れた分子は水面に並べず、水中で集まり始めます。</p>
<h3>展開：尾が1本と2本で比べる</h3>
<p>「水面なし」「ばらばら（水中）」で、尾が1本の分子を60〜100個入れると、分子がランダムに動き回りながら集まり、尾を内側に、頭を外側に向けた丸い<b>ミセル</b>がいくつもできます。同じ数で尾を2本にすると、丸くはまとまれず、2層に並んだ<b>二重層</b>のかけらができ、時間がたつとかけらどうしがつながって長くなっていきます。速さを「×1」や「一時停止」にして、分子の向き（頭は外、尾は内）を1つずつ確かめさせます。</p>
<h3>まとめ：小胞と細胞膜</h3>
<p>「小胞を1つ置く」で始めると、内側にも水を包みこんだ二重層の袋が、ゆれながらも壊れずに保たれます。とちゅうで尾を1本に切り替えると、小胞はくずれてミセルに分かれていきます。細胞膜の材料として尾が2本のリン脂質が向いている理由をまとめさせます。</p>
<h3>生徒への問いの例</h3>
<ol>
<li>水面に並んだ分子は、尾（疎水性の部分）をどちら側に向けているだろう？それはなぜだろう？</li>
<li>分子の数をだんだん増やしていくと、水面と水中で起こることはどう変わるだろう？</li>
<li>尾が2本の分子は、なぜミセルではなく二重層をつくりやすいのだろう？分子の形（頭と尾の太さ）に注目して説明しよう。</li>
</ol>
<h2>しくみ・解説</h2>
<h3>用語</h3>
<ul>
<li><b>親水性</b>とは水になじみやすい性質、<b>疎水性</b>とは水になじみにくい性質のことです。リン脂質ではリン酸を含む部分が親水性、2本の脂肪酸の部分が疎水性です。</li>
<li><b>両親媒性分子</b>とは、1つの分子の中に親水性の部分と疎水性の部分をもつ分子のことで、セッケン（脂肪酸ナトリウム）、合成洗剤、リン脂質などがあります。</li>
<li><b>単分子膜</b>とは、両親媒性分子が水面に、疎水性の部分を空気側に向けて1層に並んだ膜のことです。</li>
<li><b>ミセル</b>とは、両親媒性分子が水中で、疎水性の部分を内側に、親水性の部分を外側に向けて集まった粒です。セッケンや洗剤が油よごれを包みこんで落とすのは、油がミセルの内側に取りこまれるからです。</li>
<li><b>脂質二重層</b>とは、リン脂質が疎水性の部分を向かい合わせにして2層に並んだ膜で、細胞膜や核膜などの生体膜の基本のつくりです。</li>
<li><b>小胞（リポソーム）</b>とは、脂質二重層が閉じて、内側に水を包みこんだ袋です。</li>
</ul>
<h3>なぜ集まるのか（疎水効果）</h3>
<p>疎水性の尾のまわりでは、水分子どうしの水素結合のつながり方が制限されるため、尾が水にふれている面積が小さいほど全体として安定になります。そのため、尾どうしが寄り集まって水から隠れるように集まります（<b>疎水効果</b>）。親水性の頭は水と相互作用するので、集まりの外側に並びます。水面では、尾を空気側に出せば水にふれずにすむので、まず水面に並びます。水面が埋まると、残りの分子は水中で集まって尾を隠します。</p>
<h3>分子の形と集まり方</h3>
''' + T([["尾が1本（セッケン・脂肪酸など）", "頭が大きく尾が細い（円すい形）", "ミセル", "球（このシミュレーターでは円）の内側に尾を向けて並ぶと、すき間なく詰められる"],
          ["尾が2本（リン脂質）", "頭と尾の幅が近い（円柱形）", "脂質二重層・小胞", "丸い粒にすると尾がつかえるので、平らな2層に並ぶ。端は尾が水にふれて不安定なので、閉じた袋（小胞）になると安定"]],
         ["分子", "形", "できやすい構造", "理由"]) + '''
<h3>このシミュレーターのモデル</h3>
<p>分子は、頭1個と尾の粒（尾1本なら2個、2本なら4個）をつないだ形が変わらない分子として、熱運動を表すランダムな力で動き、回転します（ブラウン運動）。水は粒としては描かず、次の簡単なルールで水との相互作用を表しています。</p>
<ul>
<li>どの粒も、ほかの粒と重なると押し返し合う。</li>
<li>尾の粒どうしは、近づくと引き合う。</li>
<li>水の中にある尾の粒は、まわりにほかの分子の尾が少ないほど不安定になる（尾が水にふれていることにあたる）。空気中の尾は不安定にならない。</li>
<li>頭は空気中に出られない。尾は空気側に引き寄せられる。</li>
<li>尾が2本の分子どうしは、尾の先が向かい合うと少し安定になる（2本の尾が平らに並びやすいことにあたる）。</li>
</ul>
<p>決まった完成図に切り替えているのではなく、構造の名前は、集まった分子の向きと位置から自動で判定しています（尾が内向きにそろった丸い集まり＝ミセル、内側にも水がある閉じた2層＝小胞、それ以外の2層の集まり＝二重層）。</p>
''' + P('画面は細長い立体を切った2次元の断面として表しています。ミセルや小胞は球、二重層は平らな膜の断面にあたります。実際の3次元では、二重層のかけらの縁（ふち）全体で尾が水にふれるので、かけらが曲がって閉じ、小胞になる力がはたらきます。2次元のこのモデルでは縁が両端の2か所しかないため、平らなかけらが閉じて小胞になるまでには授業時間をこえる長い時間がかかります。そこで「小胞を1つ置く」で、小胞が安定に保たれることと、尾を1本にすると崩れることを確かめられるようにしています。分子の大きさ、動く速さ、時間の長さは実際の値ではありません。') + '''
<h3>身近な例と生命の起源</h3>
<ul>
<li><b>セッケン・洗剤</b>：水にとけると、水面に並んで表面張力を下げ、濃くなるとミセルをつくります。ミセルが内側に油を取りこむことで、油よごれが水に分散して落ちます。</li>
<li><b>シャボン玉</b>：うすい水の膜の両側の表面に、セッケンの分子が尾を空気側に向けて並んだつくりです（尾が外向きで、細胞膜とは向きが逆）。</li>
<li><b>生命の起源</b>：原始の地球で、脂肪酸のような単純な両親媒性分子がひとりでに小胞をつくり、内側に物質を閉じこめて原始的な細胞の膜になったという考え方があります。脂肪酸の小胞は実験でもつくられています。</li>
</ul>
<h2>参考</h2>
<ul class="seo-refs">
<li>''' + A(MEXT_KOU, "文部科学省「高等学校学習指導要領（平成30年告示）解説 理科編 理数編」") + ''' 生物（2）ア（ｱ）㋐生体物質と細胞</li>
<li>高等学校「生物」の教科書「細胞を構成する物質」「生体膜」、高等学校「化学」の教科書「油脂とセッケン」</li>
<li>J. N. Israelachvili『分子間力と表面張力』（分子の形と集合体の形：臨界充填パラメータ）</li>
<li>I. R. Cooke, K. Kremer, M. Deserno（2005）Tunable generic model for fluid bilayer membranes. Physical Review E 72: 011506（水を粒で表さない膜のモデル）</li>
</ul>
'''

LIP_JS = HELP + LIP_CORE + r'''
  let L=null, S=W/72, paused=false, spd=4, an=null, fr=0, tsim=0;
  const KN={mic:'ミセル',bil:'二重層',ves:'小胞'};
  function reset(){
    const air=$('air').value==='on', st=$('start').value, n=+$('n0').value;
    L=makeLip({type:+$('kind').value, air:air});
    if(st==='ves') L.ring(36, air?31:26, 8);
    else if(st==='drop' && air) L.drop(n);
    else if(st!=='none') for(let i=0;i<n;i++) L.add();
    showF('n0', st!=='ves' && st!=='none'); tsim=0; an=L.analyze(); stats(); draw();
  }
  function addN(k){ const room=260-L.M.length; k=Math.min(k,room); if(k<=0) return; if($('start').value==='drop' && L.P.air) L.drop(k); else for(let i=0;i<k;i++) L.add(); an=L.analyze(); stats(); }
  const bb=new Float64Array(10);
  function drawMol(m,ox){
    const sh=L.shape(); L.beads(m,bb); const X=i=>(bb[i*2]+ox)*S, Y=i=>bb[i*2+1]*S;
    const ch=L.P.type===1?[[0,1,2]]:[[0,1,2],[0,3,4]];
    ctx.strokeStyle='#e6b422'; ctx.lineWidth=sh[1][3]*1.7*S; ctx.lineCap='round'; ctx.lineJoin='round';
    ch.forEach(c=>{ ctx.beginPath(); ctx.moveTo(X(c[0]),Y(c[0])); ctx.lineTo(X(c[1]),Y(c[1])); ctx.lineTo(X(c[2]),Y(c[2])); ctx.stroke(); });
    ctx.strokeStyle='#b7791f'; ctx.lineWidth=0.8; ch.forEach(c=>{ ctx.beginPath(); ctx.moveTo(X(c[1]),Y(c[1])); ctx.lineTo(X(c[2]),Y(c[2])); ctx.stroke(); });
    ctx.fillStyle='#e0483e'; ctx.beginPath(); ctx.arc(X(0),Y(0),sh[0][3]*S,0,6.3); ctx.fill(); ctx.strokeStyle='#9b1c1c'; ctx.lineWidth=1; ctx.stroke();
  }
  function draw(){
    ctx.clearRect(0,0,W,H); const yA=L.P.yA*S;
    const g=ctx.createLinearGradient(0,0,0,H); g.addColorStop(0,'#dbeafe'); g.addColorStop(1,'#bfdbfe'); ctx.fillStyle=g; ctx.fillRect(0,0,W,H);
    if(L.P.air){ ctx.fillStyle='#f8fafc'; ctx.fillRect(0,0,W,yA); ctx.strokeStyle='#60a5fa'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(0,yA); ctx.lineTo(W,yA); ctx.stroke(); tx('空気',8,18,13,'#64748b','left',true); tx('水',8,yA+20,13,'#1d4ed8','left',true); }
    else tx('水',8,20,13,'#1d4ed8','left',true);
    for(const m of L.M){ drawMol(m,0); if(m.x<4) drawMol(m,L.P.W); else if(m.x>L.P.W-4) drawMol(m,-L.P.W); }
    if($('lab').value==='on' && an){
      an.list.forEach(c=>{ if(!KN[c.kind]) return; let x=c.x; x-=L.P.W*Math.floor(x/L.P.W); const yy=c.kind==='ves'?c.y*S:Math.max(c.y*S-c.r*S-6,(L.P.air?yA:0)+16); pill(KN[c.kind]+'（'+c.n+'）',clamp(x*S,40,W-40),yy,11,'#0f172a'); });
      if(L.P.air && an.surf) pill('水面に並んだ分子 '+an.surf+'個（単分子膜）',W-120,18,11,'#1e3a8a');
    }
    tx('速さ ×'+spd+(paused?'　一時停止中':''),W-8,H-8,11,'#334155','right',true);
  }
  function stats(){ const a=an; if(!a) return;
    setStat('sN', a.N+'個');
    setStat('sS', L.P.air? a.surf+'個' : '水面なし');
    setStat('sA', 'ミセル'+a.mic+'・二重層'+a.bil+'・小胞'+a.ves);
    setStat('sF', (a.free+a.small)+'個');
    setShare('【リン脂質と細胞膜】尾が'+L.P.type+'本の分子'+a.N+'個 → '+(L.P.air?'水面に'+a.surf+'個・':'')+'ミセル'+a.mic+'・二重層'+a.bil+'・小胞'+a.ves+'｜シミュラボ');
  }
  function loop(){
    if(!paused && L.M.length){ const t0=performance.now(), want=spd*4; let k=0; while(k<want){ L.step(); k++; if(performance.now()-t0>13) break; } tsim+=k*L.P.dt; }
    if(++fr%10===0){ an=L.analyze(); stats(); }
    draw(); requestAnimationFrame(loop);
  }
  $('kind').addEventListener('change',()=>{ L.setType(+$('kind').value); an=L.analyze(); stats(); });
  ['air','start'].forEach(id=>$(id).addEventListener('change',reset));
  $('n0').addEventListener('change',reset);
  $('spd').addEventListener('change',()=>{ spd=+$('spd').value; });
  $('lab').addEventListener('change',()=>draw());
  $('pause').addEventListener('click',()=>{ paused=!paused; $('pause').textContent=paused?'▶ 再開':'⏸ 一時停止'; });
  $('add10').addEventListener('click',()=>addN(10));
  $('rst').addEventListener('click',reset);
  cv.addEventListener('pointerdown',e=>{ if(L.M.length>=260) return; const c=cpos(cv,e); const x=c.x/dpr/S, y=c.y/dpr/S;
    if(L.P.air && y<L.P.yA+1.5){ L.M.push({x:x,y:L.P.yA+1.6,th:-Math.PI/2}); } else L.add(clamp(x,0.5,L.P.W-0.5),clamp(y,(L.P.air?L.P.yA+2:2),L.P.H-2),Math.random()*6.2832);
    an=L.analyze(); stats(); });
  window.__lip={ run:n=>{ for(let k=0;k<n;k++) L.step(); an=L.analyze(); stats(); draw(); return an; }, L:()=>L };
  spd=+$('spd').value; reset(); requestAnimationFrame(loop);
'''

sim(slug="rinshishitsu-maku", cat="rika", emoji="🧼", score=81,
    title="リン脂質と細胞膜のでき方シミュレーター（単分子膜・ミセル・脂質二重層・小胞）",
    title_tag="リン脂質二重層のシミュレーター｜親水性と疎水性、ミセル・脂質二重層・小胞のでき方（高校生物）",
    meta_desc="親水性の頭と疎水性の尾をもつ分子を水に入れると、ランダムに動きながら水面に並び、水中ではミセルや脂質二重層に集まっていく様子を観察できるシミュレーター。尾が1本と2本の分子の切り替え、分子の数（濃度）の変更、小胞の安定性、一時停止と速度変更つき。高校「生物」生体物質と細胞の授業向け。",
    og_title="リン脂質と細胞膜のでき方シミュレーター（単分子膜・ミセル・脂質二重層・小胞）",
    og_desc="ばらばらの分子が、水との相互作用だけで集まって膜になる。尾が1本ならミセル、2本なら二重層。水面がいっぱいになると水中で集まり始める。完成図ではなく、集まっていく途中が見える。",
    card_desc="親水性と疎水性をもつ分子が水面に並び、水中でミセルや脂質二重層に集まっていく過程を、尾の数と分子数を変えて観察する。",
    lead="赤い丸が水になじむ親水性の部分（頭）、黄色の線が水をきらう疎水性の部分（尾）です。分子はランダムに動き・回転しながら、水との相互作用によって向きを変えて集まっていきます。水面では尾を空気側に向けて並び、水中では尾が1本ならミセル、2本（リン脂質）なら脂質二重層ができます。分子を少しずつ足したり、尾の本数を切り替えたりして、できる構造のちがいを比べられます。",
    model="生物 細胞と分子（生体膜・リン脂質の親水性と疎水性）",
    level="高校（生物・化学）、生物基礎の発展",
    unit="高等学校 生物（2）生命現象と物質 ア（ｱ）細胞と分子 ㋐生体物質と細胞",
    canvas=canvas(640, 445, light=True),
    controls=select("kind", "分子の種類（途中で変更可）", [("2", "尾2本（リン脂質）"), ("1", "尾1本（セッケン）")])
             + select("start", "はじめの状態", [("rand", "ばらばら（水中）"), ("drop", "水面に落とす"), ("ves", "小胞を1つ置く"), ("none", "分子なし")])
             + slider("n0", "はじめの分子の数", 10, 200, 80, 10)
             + select("air", "水面", [("on", "あり（上が空気）"), ("off", "なし（全部が水）")])
             + select("spd", "速さ", [("4", "×4"), ("8", "×8（はやい）"), ("2", "×2"), ("1", "×1（ゆっくり）")])
             + select("lab", "構造の名前", [("on", "表示する"), ("off", "表示しない")]),
    buttons=btn("pause", "⏸ 一時停止", True) + btn("add10", "＋10個入れる") + btn("rst", "↺ はじめから"),
    stats=stats([("sN", "分子の数", False), ("sS", "水面に並んだ分子", False), ("sA", "水中の集まり", True), ("sF", "ばらばらの分子", False)]),
    legend="赤い丸＝親水性の部分（頭）、黄色の線＝疎水性の部分（尾）。上の白い部分＝空気、青い部分＝水。水をタップするとその場所に分子を1個、水面より上をタップすると水面に分子を1個入れます。「＋10個入れる」は「水面に落とす」のときは水面に、それ以外は水中のばらばらの位置に入れます。構造の名前（ミセル・二重層・小胞）は、分子の向きと位置から自動で判定しています。左右の端はつながっています。",
    article=LIP_ARTICLE,
    faqs=[("リン脂質はなぜ二重層になるの？", "リン脂質は親水性の頭と疎水性の2本の尾をもつ分子です。水中では尾が水にふれないように尾どうしを向かい合わせにし、頭を両側の水に向けて2層に並ぶと安定します。尾が2本で頭と尾の幅が近い（円柱形に近い）ので、丸いミセルにはなりにくく、平らな二重層になります。"),
          ("ミセルと脂質二重層のちがいは？", "ミセルは、尾を内側、頭を外側に向けて集まった丸い粒で、内側に水はありません。脂質二重層は、尾を向かい合わせにした2層の膜です。尾が1本で頭が大きい分子（セッケンなど）はミセルを、尾が2本のリン脂質は二重層をつくりやすくなります。"),
          ("水面では分子はどう並ぶの？", "疎水性の尾を空気側に、親水性の頭を水側に向けて1層に並びます（単分子膜）。尾を空気中に出せば水にふれずにすむからです。セッケンが水の表面張力を下げるのはこのためで、水面がいっぱいになると、残りの分子は水中でミセルをつくります。"),
          ("小胞とは何？細胞とどう関係しているの？", "小胞は、脂質二重層が閉じて内側に水を包みこんだ袋です。細胞膜も、細胞の内側と外側をリン脂質二重層で仕切っています。人工的につくった小胞はリポソームとよばれ、薬を包んで運ぶ技術などに使われています。原始の生命も、両親媒性分子の小胞の中で生まれたという考え方があります。"),
          ("セッケンで油よごれが落ちるのはなぜ？", "セッケンの分子は、疎水性の尾を油に、親水性の頭を水に向けて油を取り囲み、ミセルの内側に油を取りこみます。外側が親水性なので、油を包んだミセルは水に分散し、すすぐと流れ落ちます。"),
          ("このシミュレーションで水はどう表されているの？", "水は粒としては描かず、「尾は水にふれていると不安定」「尾どうしは引き合う」「頭は空気中に出られない」などの簡単なルールで、水との相互作用を表しています（水を粒で表さない膜のモデル）。分子は熱運動を表すランダムな力で動き、構造は完成図に切り替わるのではなく、ルールにしたがって集まることでできます。")],
    rel=[("maku-yuso", "🚪", "膜輸送のシミュレーター"), ("joutai-henka", "🧊", "状態変化と粒子のシミュレーター"),
         ("diffusion", "🫧", "拡散シミュレーター"), ("saibou-bunretsu", "🔬", "細胞分裂のシミュレーター"), ("denshi-haichi", "⚛️", "原子の構造と電子配置のシミュレーター")],
    js=LIP_JS)
