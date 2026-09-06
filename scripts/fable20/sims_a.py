# -*- coding: utf-8 -*-
"""Fable20 A: 生態・待ち行列・エレベーター・信頼の進化・噂の拡散"""
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

# ============================================================ 1 キツネとウサギ
sim(slug="lotka-volterra", cat="wonder", emoji="🐰", score=70,
    title="キツネとウサギ 増減シミュレーター", model="ロトカ・ヴォルテラ方程式（捕食者－被食者モデル）",
    model_note="Lotka (1925) / Volterra (1926)。数理生態学の基礎方程式",
    title_tag="キツネとウサギ 増減シミュレーター｜捕食者と獲物はなぜ周期的に増減する？",
    meta_desc="ウサギが増えるとキツネが増え、キツネが増えるとウサギが減る——生態学の基本方程式（ロトカ・ヴォルテラ）をブラウザで動かし、増減の周期や「キツネを減らすと何が起きるか」を体感できる無料シミュレーター。",
    og_title="キツネとウサギ 増減シミュレーター", og_desc="捕食者と獲物が周期的に増減する理由を、数理生態学の方程式で体感。",
    card_desc="ウサギが増えればキツネも増え、やがて両方減る。生態系の“波”を方程式で動かす。",
    lead="ウサギが増えるとキツネが増え、キツネが増えるとウサギが減り、するとキツネも減って——。誰も指揮していないのに、2種類の生き物は決まったリズムで増減を繰り返します。増殖率や捕食率を動かして、その波を観察してください。",
    canvas=canvas(640, 360),
    controls=slider("a", "ウサギの増殖率 α", 0.5, 2.0, 1.1, 0.05) + slider("b", "キツネに食べられる率 β", 0.1, 1.0, 0.4, 0.05)
           + slider("g", "キツネの死亡率 γ", 0.1, 1.0, 0.4, 0.05) + slider("sp", "再生速度", 1, 8, 3, 1, "×{v}"),
    buttons=btn("toggle", "⏸ 一時停止") + btn("reset", "リセット") + btn("cull", "🦊 キツネを半分に減らす") + btn("feed", "🐰 ウサギを2倍に増やす"),
    stats=stats([("sR", "ウサギ", False), ("sF", "キツネ", True), ("sT", "増減の周期", False), ("sMax", "ウサギの最大", False)]),
    legend="緑＝ウサギ、オレンジ＝キツネ。右の小さな図は「ウサギ数×キツネ数」の軌道（ぐるぐる回る＝周期的に増減）。",
    article=P("キツネはウサギがいないと餓死し、ウサギはキツネがいないと増え続ける。この2つを式にしただけで、どちらも絶滅せず、<b>一定の周期で増減を繰り返す</b>ことが導けます。増減は「振り子」のように永遠に続き、平衡点に落ち着きません。") + '''
<h2>この画面の裏で解いている式</h2>
''' + N("dR/dt = αR − βRF　（ウサギ：自然に増え、キツネに会うと減る）<br>dF/dt = δβRF − γF　（キツネ：ウサギを食べると増え、自然に減る）") + '''
<p>R がウサギ、F がキツネの数です。式の中身は「ウサギとキツネが出会う回数は R×F に比例する」というだけ。この“出会いの項”が2つの種を結びつけ、周期的な振動を生みます。本シミュレーターはこの式をルンゲ＝クッタ法で数値積分しています（δ＝0.1で固定）。</p>
<h2>スライダーで何が起きるか</h2>
''' + T([["ウサギの増殖率 α を上げる", "波の山が高くなり、周期が短くなる。キツネの平均数（＝α/β）が増える"],
          ["捕食率 β を上げる", "キツネが効率よく食べるので、キツネの平衡数は減る（意外）。波が激しくなる"],
          ["キツネの死亡率 γ を上げる", "ウサギの平衡数（＝γ/δ）が増える。キツネが減りやすく、ウサギ天国に近づく"],
          ["キツネを半分に減らす", "ウサギが一時的に急増→餌が増えたキツネが元以上に増える→ウサギ激減。“駆除の逆効果”"]], ["操作", "起きること"]) + '''
<h2>現実で観測された「10年周期」</h2>
<p>カナダのハドソン湾会社が19世紀から残した毛皮の取引記録では、カンジキウサギとカナダオオヤマネコの捕獲数が<b>約10年周期</b>で増減しており、この方程式の予測と驚くほど一致します。第一次世界大戦中にアドリア海で漁獲が減った際、サメなど捕食魚の割合が増えた現象を説明するために、数学者ヴォルテラがこの式を導いたのが始まりです。</p>
<p>害虫駆除で「殺虫剤を撒いたら害虫が前より増えた」という現象（駆除の逆効果）も、この式で説明できます。殺虫剤が害虫だけでなく天敵も減らすため、回復の早い害虫が先に増え、天敵が追いつく前に大発生するのです。</p>
''',
    faqs=[("なぜ平衡点に落ち着かないの？", "ロトカ・ヴォルテラ方程式は摩擦にあたる項を持たないため、振り子と同じでエネルギーが保存され、永遠に振動します。現実には環境収容力（餌の上限）などの項が加わるため、実際の生態系では振動が徐々に小さくなったり、逆に周期が安定したりします。"),
          ("キツネの平均数が「ウサギの増殖率」で決まるのはなぜ？", "式を解くと、キツネの平均数は α/β、ウサギの平均数は γ/δ になります。つまりキツネの数はキツネ自身の性質ではなく、餌であるウサギがどれだけ増えるかで決まります。生態系の“意外な連鎖”です。"),
          ("数値は現実の個体数？", "いいえ。単位は相対的なもので、表示は見やすさのために10倍しています。周期や増減のパターンを見る目的でお使いください。")],
    rel=[("kansen-agent", "🦠", "感染はこう広がる"), ("shinrai-shinka", "🤝", "信頼の進化"), ("boids", "🐦", "鳥の群れシミュレーター"), ("forest-fire", "🔥", "森林火災シミュレーター")],
    js=r'''
  const cv=$('cv'), x=cv.getContext('2d'), W=cv.width, H=cv.height;
  const PLOT_W=430, PH_X=470, PH_W=150;
  let R, F, t, hist, run=true, peaks, maxR, sp;
  const p = () => ({a:+$('a').value, b:+$('b').value, g:+$('g').value, d:0.1});
  function reset(){ R=10; F=4; t=0; hist=[]; peaks=[]; maxR=0; draw(); }
  function deriv(r,f,q){ return [q.a*r - q.b*r*f, q.d*q.b*r*f - q.g*f]; }
  function rk4(dt){ const q=p(); const k1=deriv(R,F,q); const k2=deriv(R+dt/2*k1[0],F+dt/2*k1[1],q); const k3=deriv(R+dt/2*k2[0],F+dt/2*k2[1],q); const k4=deriv(R+dt*k3[0],F+dt*k3[1],q);
    R=Math.max(0.01, R+dt/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0])); F=Math.max(0.01, F+dt/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1])); t+=dt; }
  function step(){ const n=+$('sp').value*2; for(let i=0;i<n;i++){ rk4(0.01); }
    hist.push([t,R,F]); if(hist.length>1200) hist.shift();
    const L=hist.length; if(L>=3){ const a=hist[L-3][1],b=hist[L-2][1],c=hist[L-1][1]; if(b>a&&b>=c&&b>2){ if(!peaks.length||hist[L-2][0]-peaks[peaks.length-1]>0.5) peaks.push(hist[L-2][0]); if(peaks.length>4) peaks.shift(); } }
    maxR=Math.max(maxR,R); }
  function draw(){
    x.fillStyle='#0b1020'; x.fillRect(0,0,W,H);
    const ymax=Math.max(30, maxR*1.15, 20);
    // grid
    x.strokeStyle='rgba(255,255,255,.08)'; x.lineWidth=1; for(let i=1;i<5;i++){ x.beginPath(); x.moveTo(0,H*i/5); x.lineTo(PLOT_W,H*i/5); x.stroke(); }
    x.fillStyle='rgba(255,255,255,.35)'; x.font='11px sans-serif'; x.fillText('個体数（×10匹）', 6, 14); x.fillText('時間 →', PLOT_W-44, H-6);
    if(hist.length>1){ const t0=hist[0][0], t1=Math.max(hist[hist.length-1][0], t0+12);
      const sx=(tt)=>(tt-t0)/(t1-t0)*PLOT_W, sy=(v)=>H-8-(v/ymax)*(H-30);
      for(const [idx,col] of [[1,'#4ade80'],[2,'#fb923c']]){ x.strokeStyle=col; x.lineWidth=2; x.beginPath(); hist.forEach((h,i)=>{ const X=sx(h[0]),Y=sy(h[idx]); i?x.lineTo(X,Y):x.moveTo(X,Y); }); x.stroke(); }
      // phase portrait
      x.strokeStyle='rgba(255,255,255,.12)'; x.strokeRect(PH_X,20,PH_W,PH_W);
      x.fillStyle='rgba(255,255,255,.35)'; x.fillText('ウサギ→', PH_X+PH_W-42, 20+PH_W+12); x.save(); x.translate(PH_X-4,20+PH_W/2); x.rotate(-Math.PI/2); x.fillText('キツネ→',-20,0); x.restore();
      const rmax=ymax, fmax=Math.max(15, ...hist.map(h=>h[2]))*1.1;
      x.strokeStyle='#a78bfa'; x.lineWidth=1.5; x.beginPath(); hist.forEach((h,i)=>{ const X=PH_X+h[1]/rmax*PH_W, Y=20+PH_W-h[2]/fmax*PH_W; i?x.lineTo(X,Y):x.moveTo(X,Y); }); x.stroke();
      x.fillStyle='#fff'; x.beginPath(); x.arc(PH_X+R/rmax*PH_W, 20+PH_W-F/fmax*PH_W, 4, 0, 7); x.fill();
      // labels
      x.fillStyle='#4ade80'; x.font='bold 12px sans-serif'; x.fillText('🐰 ウサギ '+Math.round(R*10)+'匹', 6, 32); x.fillStyle='#fb923c'; x.fillText('🦊 キツネ '+Math.round(F*10)+'匹', 6, 48);
    }
    setStat('sR', Math.round(R*10)+'匹'); setStat('sF', Math.round(F*10)+'匹'); setStat('sMax', Math.round(maxR*10)+'匹');
    let per='計測中'; if(peaks.length>=2){ per=(peaks[peaks.length-1]-peaks[peaks.length-2]).toFixed(1)+' 年'; }
    setStat('sT', per);
    setShare('ウサギとキツネの増減は約'+(per==='計測中'?'？':per)+'周期🐰🦊 ウサギ最大'+Math.round(maxR*10)+'匹。キツネを減らすと逆にウサギが激減する“駆除の逆効果”も再現できる👇');
  }
  function loop(){ if(run){ step(); } draw(); requestAnimationFrame(loop); }
  $('toggle').addEventListener('click',()=>{ run=!run; $('toggle').textContent=run?'⏸ 一時停止':'▶ 再生'; });
  $('reset').addEventListener('click',reset);
  $('cull').addEventListener('click',()=>{ F=Math.max(0.2,F*0.5); });
  $('feed').addEventListener('click',()=>{ R=R*2; });
  reset(); loop();
''')

# ============================================================ 2 行列 1列 vs 個別列
sim(slug="queue-docchi", cat="wonder", emoji="🧍", score=71,
    title="行列、1列並び vs レジ別 どっちが速い？", model="待ち行列理論（M/M/c・フォーク型 vs 個別列）",
    model_note="Erlang (1909) に始まる待ち行列理論。銀行・空港・コールセンターの設計に使用",
    title_tag="行列は1列に並ぶべき？レジ別に並ぶべき？｜待ち時間を待ち行列シミュレーションで比較",
    meta_desc="「1本の列から空いたレジへ」と「レジごとに並ぶ」では、どちらが待ち時間が短い？同じ客・同じレジ時間で2つの並び方を同時にシミュレーションし、平均待ち時間と最大待ち時間の差を可視化する無料ツール。銀行やATMの列が1本なのはこの理由。",
    og_title="行列、1列並び vs レジ別 どっちが速い？", og_desc="同じ客で2つの並び方を同時シミュレーション。待ち時間の差を可視化。",
    card_desc="1本の列から空いたレジへ、とレジごとに並ぶのは、待ち時間がどれだけ違う？同じ客で同時に実験。",
    lead="銀行やATM、空港の保安検査は「1本の列から空いたところへ」。スーパーは「レジごとに並ぶ」。同じ客・同じレジ時間で2つの方式を同時に走らせると、待ち時間にどれだけ差が出るのかを見てください。",
    canvas=canvas(640, 380),
    controls=slider("c", "レジの台数", 2, 6, 3, 1, "{v}台") + slider("lam", "客の到着（1分あたり）", 0.5, 5, 2.7, 0.1, "{v}人")
           + slider("s", "1人あたりのレジ時間（平均）", 0.5, 2.0, 1.0, 0.1, "{v}分") + select("var", "レジ時間のばらつき", [("hi", "大きい（会計に手間取る客がいる）"), ("lo", "小さい（ほぼ一定）")]) + slider("sp", "再生速度", 1, 10, 4, 1, "×{v}"),
    buttons=btn("toggle", "⏸ 一時停止") + btn("reset", "リセット"),
    stats=stats([("sA", "1列並び 平均待ち", False), ("sB", "レジ別 平均待ち", True), ("sMax", "最大待ち（1列／レジ別）", False), ("sRho", "レジ稼働率", False)]),
    legend="上＝1本の列（空いたレジへ）、下＝レジ別に並ぶ。同じ客が同じ順番・同じレジ時間で来店しています。緑のマス＝接客中。",
    article=P("同じ客・同じレジ台数でも、<b>「1本の列」のほうが平均待ち時間も最大待ち時間も短くなる</b>のが待ち行列理論の結論です。レジ別に並ぶと、「自分の列の前の人が手間取る」という運の要素で、空いているレジがあるのに待つ人が出るからです。") + '''
<h2>なぜ1列のほうが速いのか</h2>
<p>レジ別に並ぶ方式では、あるレジが手間取る客で止まっている間に、隣のレジが空いてしまう瞬間があります。この「レジが空いているのに待っている人がいる」時間が無駄です。1本の列なら、空いたレジにすぐ次の人が入るため、この無駄が構造的に起きません。列を作る側からすれば<b>「待ちの不公平」がなくなる</b>ことも大きな利点で、銀行・郵便局・空港・Apple Storeなどが1列方式を採用している理由です。</p>
<h2>待ち時間が急に増える「稼働率」のライン</h2>
''' + T([["〜70%", "ほぼ待たない。列ができてもすぐ消える"], ["80%", "ときどき列。平均待ちがレジ時間の1〜2倍になる"], ["90%", "つねに列。平均待ちがレジ時間の数倍。ばらつきの影響が激しい"], ["95%以上", "待ち時間が爆発的に伸びる。少しの混雑増で列が無限に近づく"]], ["レジ稼働率（λ×s÷c）", "様子"]) + '''
<p>稼働率が同じでも、レジ時間の<b>ばらつきが大きいほど待ち時間は長く</b>なります（ポラチェック＝ヒンチンの公式）。「たまに手間取る客がいる」だけで、平均待ちは倍近くになることも。会計を速くするより、ばらつきを減らす（セルフレジの分離、カゴ数で列を分ける）ほうが効くこともあります。</p>
<h2>現実の設計に使われている</h2>
<p>待ち行列理論は1909年、デンマークの電話会社の技術者アーランが「交換手を何人置けば電話がつながるか」を計算するために生み出しました。現在はコールセンターのオペレーター数、病院の診察室数、サーバーの台数、ディズニーランドのファストパスまで、あらゆる「待ち」の設計に使われています。</p>
''',
    faqs=[("スーパーはなぜレジ別に並ぶの？", "1本の列を作るには売り場の通路幅が必要で、カートを持った客が長い1列を作ると通路が塞がるためです。物理的な制約で、待ち時間の短さより売り場の動線を優先しています。"),
          ("レジ別でも「空いたら移動」すれば同じでは？", "移動（ジョッキング）を許すと差は縮まりますが、移動の判断が遅れる分だけ無駄が残ります。本シミュレーターのレジ別方式は「最初に短い列を選び、その後は移動しない」設定です。"),
          ("待ち時間がずっと増え続けるのはなぜ？", "稼働率が100%を超えると（客の到着がレジの処理能力を上回ると）列は理論上無限に伸びます。スライダーで到着を減らすかレジを増やしてください。")],
    rel=[("elevator-sim", "🛗", "エレベーター待ち時間シミュレーター"), ("manin-densha", "🚃", "満員電車 混雑率シミュレーター"), ("jutai", "🚗", "渋滞は勝手に生まれる"), ("machi-jikan", "⏳", "人生の「待ち時間」")],
    js=r'''
  const cv=$('cv'), x=cv.getContext('2d'), W=cv.width, H=cv.height;
  let t, nextArr, sysA, sysB, run=true, cid;
  const expo=(m)=>-Math.log(1-Math.random())*m;
  function svc(){ const s=+$('s').value; if($('var').value==='lo'){ let v=0; for(let i=0;i<8;i++) v+=expo(s/8); return v; } return expo(s); }
  function mk(c){ return { srv:Array.from({length:c},()=>({busyUntil:0,cust:null})), q:[], qs:Array.from({length:c},()=>[]), waits:[], sumW:0, maxW:0, served:0 }; }
  function reset(){ t=0; nextArr=expo(1/+$('lam').value); const c=+$('c').value; sysA=mk(c); sysB=mk(c); cid=0; draw(); }
  function arrive(){ const cu={id:cid++, at:t, st:svc()};
    sysA.q.push({...cu});
    // B: 最短の列へ（同着はランダム）
    let best=[],bl=1e9; sysB.qs.forEach((q,i)=>{ const L=q.length+(sysB.srv[i].cust?1:0); if(L<bl){bl=L;best=[i];} else if(L===bl) best.push(i); });
    sysB.qs[best[Math.random()*best.length|0]].push({...cu}); }
  function serve(sys, single){ sys.srv.forEach((s,i)=>{ if(s.cust && s.busyUntil<=t){ s.cust=null; sys.served++; }
      if(!s.cust){ const q=single?sys.q:sys.qs[i]; if(q.length){ const cu=q.shift(); const w=t-cu.at; sys.sumW+=w; sys.maxW=Math.max(sys.maxW,w); sys.waits.push(w); if(sys.waits.length>400) sys.waits.shift(); s.cust=cu; s.busyUntil=t+cu.st; } } }); }
  function step(){ const dt=0.01*+$('sp').value; t+=dt; while(nextArr<=t){ arrive(); nextArr+=expo(1/+$('lam').value); } serve(sysA,true); serve(sysB,false); }
  function person(px,py,col){ x.fillStyle=col; x.beginPath(); x.arc(px,py-5,4,0,7); x.fill(); x.fillRect(px-4,py,8,9); }
  function draw(){
    x.fillStyle='#0b1020'; x.fillRect(0,0,W,H); const c=+$('c').value;
    x.font='bold 13px sans-serif'; x.fillStyle='#93c5fd'; x.fillText('A. 1本の列 → 空いたレジへ', 12, 20);
    x.fillStyle='#fca5a5'; x.fillText('B. レジごとに並ぶ（最初に短い列を選ぶ）', 12, 200);
    const bw=54, gap=16, x0=W-24-c*(bw+gap);
    // A
    sysA.srv.forEach((s,i)=>{ const bx=x0+i*(bw+gap); x.fillStyle=s.cust?'#16a34a':'#1e293b'; x.fillRect(bx,40,bw,40); x.strokeStyle='#475569'; x.strokeRect(bx,40,bw,40); x.fillStyle='#e2e8f0'; x.font='11px sans-serif'; x.fillText('レジ'+(i+1), bx+12, 64); if(s.cust) person(bx+bw/2, 100, '#facc15'); });
    const qa=sysA.q; const shown=Math.min(qa.length,40); for(let i=0;i<shown;i++){ person(x0-30-i*13, 60, i<3?'#facc15':'#94a3b8'); }
    x.fillStyle='#cbd5e1'; x.font='12px sans-serif'; x.fillText('待ち '+qa.length+'人', 12, 64);
    // B
    sysB.srv.forEach((s,i)=>{ const bx=x0+i*(bw+gap); x.fillStyle=s.cust?'#16a34a':'#1e293b'; x.fillRect(bx,220,bw,40); x.strokeStyle='#475569'; x.strokeRect(bx,220,bw,40); x.fillStyle='#e2e8f0'; x.font='11px sans-serif'; x.fillText('レジ'+(i+1), bx+12, 244); if(s.cust) person(bx+bw/2, 280, '#facc15');
      const q=sysB.qs[i]; const n=Math.min(q.length,7); for(let k=0;k<n;k++) person(bx+bw/2, 300+k*11, k<2?'#facc15':'#94a3b8'); if(q.length>7){ x.fillStyle='#94a3b8'; x.fillText('+'+(q.length-7), bx+bw/2-8, 300+7*11+8); } });
    const wb=sysB.qs.reduce((a,q)=>a+q.length,0); x.fillStyle='#cbd5e1'; x.font='12px sans-serif'; x.fillText('待ち '+wb+'人', 12, 244);
    x.fillStyle='rgba(255,255,255,.5)'; x.fillText('経過 '+Math.floor(t)+'分', W-80, H-8);
    const avg=(s)=>s.waits.length?s.sumW/(s.served+s.srv.filter(v=>v.cust).length||1):0;
    const a=avg(sysA), b=avg(sysB), rho=+$('lam').value*+$('s').value/c;
    setStat('sA', a.toFixed(1)+'分'); setStat('sB', b.toFixed(1)+'分'); setStat('sMax', sysA.maxW.toFixed(0)+'分 / '+sysB.maxW.toFixed(0)+'分'); setStat('sRho', Math.round(rho*100)+'%'+(rho>=1?' ⚠️限界超え':''));
    setShare('レジ'+c+'台・稼働率'+Math.round(rho*100)+'%で実験🧍 1列並びの平均待ち'+a.toFixed(1)+'分 vs レジ別'+b.toFixed(1)+'分（最大'+sysA.maxW.toFixed(0)+'分 vs '+sysB.maxW.toFixed(0)+'分）。銀行の列が1本な理由👇');
  }
  function loop(){ if(run){ for(let i=0;i<3;i++) step(); } draw(); requestAnimationFrame(loop); }
  ['c','lam','s','var'].forEach(id=>$(id).addEventListener('change',reset));
  $('toggle').addEventListener('click',()=>{ run=!run; $('toggle').textContent=run?'⏸ 一時停止':'▶ 再生'; });
  $('reset').addEventListener('click',reset);
  reset(); loop();
''')

# ============================================================ 3 エレベーター
sim(slug="elevator-sim", cat="wonder", emoji="🛗", score=69,
    title="エレベーター待ち時間シミュレーター", model="離散事象シミュレーション（SCAN／最短距離／先着順の群管理）",
    model_note="ディスクスケジューリングと同型のアルゴリズム。実際の群管理制御の基礎",
    title_tag="エレベーター待ち時間シミュレーター｜台数・階数・制御方式で待ち時間はどう変わる？",
    meta_desc="ビルの階数・エレベーター台数・混雑度・制御アルゴリズム（進行方向優先／最寄り優先／先着順）を変えて、平均待ち時間と最大待ち時間がどう変わるかを見る無料シミュレーター。「なぜ自分の階に来ないのか」の答え。",
    og_title="エレベーター待ち時間シミュレーター", og_desc="台数・階数・制御方式で待ち時間はどう変わる？アルゴリズムを比べて体感。",
    card_desc="なぜ自分の階に来ない？台数・階数・制御アルゴリズムを変えて、待ち時間の変化を観察。",
    lead="「押したのに全然来ない」「上に行きたいのに下に行く」——エレベーターの動きには理由があります。階数・台数・混雑度・制御アルゴリズムを変えて、平均待ちと“最大待ち”がどう変わるかを見てください。",
    canvas=canvas(640, 400),
    controls=slider("fl", "階数", 5, 30, 15, 1, "{v}階") + slider("el", "エレベーターの台数", 1, 4, 2, 1, "{v}台")
           + slider("lam", "混雑度（1分あたりの利用者）", 1, 30, 12, 1, "{v}人") + select("mode", "制御方式", [("scan", "進行方向の呼びを順に（SCAN・一般的）"), ("sstf", "いちばん近い呼びへ（最短距離優先）"), ("fcfs", "呼んだ順（先着順）")])
           + slider("sp", "再生速度", 1, 10, 4, 1, "×{v}"),
    buttons=btn("toggle", "⏸ 一時停止") + btn("reset", "リセット"),
    stats=stats([("sAvg", "平均待ち時間", True), ("sMax", "最大待ち時間", False), ("sDone", "運んだ人数", False), ("sWait", "いま待っている人", False)]),
    legend="各階の点＝待っている人（赤いほど長く待っている）。箱＝かご（数字は乗っている人数）。1階が出入口で、利用者の半分は1階から乗ります。",
    article=P("エレベーターの待ち時間を決めるのは「速さ」より<b>制御アルゴリズム</b>です。進行方向の呼びを順に拾う SCAN 方式は、平均も最大も安定します。最寄り優先は平均は良いのに<b>端の階の人が延々と待たされる</b>ことがあり、先着順は平均が大きく悪化します。") + '''
<h2>3つの制御方式の違い</h2>
''' + T([["進行方向優先（SCAN）", "上りなら上の呼びを順に全部拾ってから折り返す", "平均・最大とも安定。実際のエレベーターの基本", "混雑時は途中階で満員になりやすい"],
          ["最短距離優先（SSTF）", "いま一番近い呼びへ向かう", "空いていれば平均待ちは最短", "遠い階の人が後回しにされ続ける“飢餓”が起きる"],
          ["先着順（FCFS）", "呼ばれた順に律儀に向かう", "公平に見える", "行ったり来たりが増え、全員の待ちが長くなる"]], ["方式", "動き方", "長所", "短所"]) + '''
<p>この3方式は、ハードディスクの読み書きヘッドをどう動かすかという「ディスクスケジューリング」とまったく同じ問題です。エレベーターの答えがコンピュータに、コンピュータの答えがエレベーターに使われています。</p>
<h2>台数を増やすと何が変わるか</h2>
<p>台数を2倍にしても、待ち時間は半分にはなりません。一方で、混雑度が処理能力に近づくと待ち時間は<b>急激に</b>伸びます（待ち行列の性質）。ビルの設計では「朝の出勤ピーク5分間に、在館人数の何%を運べるか（5分間輸送能力）」という指標で台数を決めます。オフィスビルでは11〜15%が目安です。</p>
<h2>「押したのに来ない」の正体</h2>
<p>SCAN方式では、上り運転中のかごは下の階の呼びを無視して上へ進み続けます。あなたの下の階で押した人は「目の前を通り過ぎた」ように感じますが、全体の平均待ちを最小にするための合理的な動きです。最大待ちが気になる高層ビルでは、低層用・高層用にかごを分ける（バンク分け）や、乗る前に行き先を入力する行先予報システムで解決しています。</p>
''',
    faqs=[("エレベーターの速さを上げれば解決？", "速さより「止まる回数」が支配的です。1回の停止（減速・ドア開閉・乗降）に10秒前後かかるため、途中階で何度も止まるほど遅くなります。急行運転や行先予報で停止回数を減らすのが実務的な解決策です。"),
          ("行先予報システムって何？", "乗る前にホールで行き先階を入力し、同じ階へ行く人を同じかごにまとめる方式です。停止回数が減るため、同じ台数で輸送能力が2〜3割上がるとされ、高層オフィスビルで普及しています。"),
          ("現実のエレベーターはどの方式？", "基本はSCAN（コレクティブ制御）で、複数台の場合はどのかごに呼びを割り当てるかを群管理コンピュータが決めています。最近はAIで乗客数を予測し、混む前にかごを配置する方式もあります。")],
    rel=[("queue-docchi", "🧍", "行列、1列並び vs レジ別"), ("manin-densha", "🚃", "満員電車 混雑率シミュレーター"), ("jisa-shukkin", "🕘", "時差出勤の効果"), ("sort-visualizer", "📊", "ソートアルゴリズム可視化")],
    js=r'''
  const cv=$('cv'), x=cv.getContext('2d'), W=cv.width, H=cv.height;
  let t, F, E, cars, waiting, nextArr, run=true, done, sumW, maxW, fifo;
  const expo=(m)=>-Math.log(1-Math.random())*m;
  const CAP=10, SPEED=1.0, DOOR=2.5;
  function reset(){ t=0; F=+$('fl').value; E=+$('el').value; waiting=Array.from({length:F+1},()=>[]); fifo=[];
    cars=Array.from({length:E},(_,i)=>({pos:1+Math.round(i*(F-1)/Math.max(1,E-1)*0.5), dir:0, riders:[], door:0, target:null})); nextArr=expo(60/+$('lam').value); done=0; sumW=0; maxW=0; draw(); }
  function spawn(){ let from, to; if(Math.random()<0.5){ from=1; to=2+Math.floor(Math.random()*(F-1)); } else { from=2+Math.floor(Math.random()*(F-1)); to=Math.random()<0.6?1:1+Math.floor(Math.random()*F); if(to===from) to=1; }
    waiting[from].push({t0:t, to}); fifo.push({floor:from, t0:t}); }
  function hasCallDir(fl, d){ return waiting[fl].some(p=>Math.sign(p.to-fl)===d); }
  function stopsAhead(c, d){ const list=[]; for(let f=1;f<=F;f++){ if(d>0?f>c.pos+1e-3:f<c.pos-1e-3){ if(c.riders.some(r=>r.to===f) || hasCallDir(f,d) ) list.push(f); } } return list; }
  function anyWaitAhead(c,d){ let best=null; for(let f=1;f<=F;f++){ if(d>0?f>c.pos+1e-3:f<c.pos-1e-3){ if(waiting[f].length && (best==null || Math.abs(f-c.pos)<Math.abs(best-c.pos))) best=f; } } return best; }
  function choose(c){ const mode=$('mode').value;
    if(mode==='scan'){ if(c.dir===0){ // idle: nearest floor with anyone waiting
        let best=null,bd=1e9; for(let f=1;f<=F;f++){ if(waiting[f].length){ const d=Math.abs(f-c.pos); if(d<bd){bd=d;best=f;} } } if(best==null) return null; c.dir=Math.sign(best-c.pos)||0; if(c.dir===0) return best; }
      let s=stopsAhead(c,c.dir); if(s.length) return c.dir>0?s[0]:s[s.length-1];
      const w=anyWaitAhead(c,c.dir); if(w!=null) return w; // 進行方向に逆向きの呼びだけ→端まで行って折返し
      c.dir=-c.dir; s=stopsAhead(c,c.dir); if(s.length) return c.dir>0?s[0]:s[s.length-1]; const w2=anyWaitAhead(c,c.dir); if(w2!=null) return w2; c.dir=0; return null; }
    if(mode==='sstf'){ let best=null,bd=1e9; for(let f=1;f<=F;f++){ const d=Math.abs(f-c.pos); if(d<1e-3) continue; if(c.riders.some(r=>r.to===f)||waiting[f].length){ if(d<bd){bd=d;best=f;} } } if(best!=null) c.dir=Math.sign(best-c.pos); return best; }
    // fcfs: 乗客の行き先を先に(乗せた順)、なければ最も古い呼び
    if(c.riders.length){ const f=c.riders[0].to; c.dir=Math.sign(f-c.pos); return f; }
    const claimed=new Set(cars.filter(o=>o!==c&&o.target!=null&&!o.riders.length).map(o=>o.target));
    for(const q of fifo){ if(waiting[q.floor].length && !claimed.has(q.floor)){ c.dir=Math.sign(q.floor-c.pos); return q.floor; } }
    return null; }
  function step(dt){ t+=dt; while(nextArr<=t){ spawn(); nextArr+=expo(60/+$('lam').value); }
    cars.forEach(c=>{ if(c.door>0){ c.door-=dt; return; }
      const mode=$('mode').value;
      if(mode!=='fcfs' || c.target==null) c.target=choose(c); else if(c.riders.length===0 && !waiting[c.target].length) c.target=choose(c);
      if(c.target==null){ c.dir=0; return; }
      const d=c.target-c.pos; const mv=SPEED*dt; if(Math.abs(d)<=mv+1e-6){ c.pos=c.target; arrive(c); } else c.pos+=Math.sign(d)*mv; }); }
  function arrive(c){ const f=c.pos; const mode=$('mode').value; let stopped=false;
    const before=c.riders.length; c.riders=c.riders.filter(r=>{ if(r.to===f){ done++; return false; } return true; }); if(c.riders.length!==before) stopped=true;
    if(c.riders.length===0 && waiting[f].length){ const same=waiting[f].find(p=>Math.sign(p.to-f)===c.dir); if(!same) c.dir=Math.sign(waiting[f][0].to-f); }
    const keep=[]; waiting[f].forEach(p=>{ const okDir = mode!=='scan' || Math.sign(p.to-f)===c.dir; if(okDir && c.riders.length<CAP){ const w=t-p.t0; sumW+=w; maxW=Math.max(maxW,w); c.riders.push({to:p.to,t0:p.t0}); stopped=true; } else keep.push(p); });
    waiting[f]=keep; fifo=fifo.filter(q=>waiting[q.floor].length);
    if(stopped) c.door=DOOR; c.target=null; }
  function draw(){ x.fillStyle='#0b1020'; x.fillRect(0,0,W,H);
    const top=20, bottom=H-16, fh=(bottom-top)/F; const shaftX=300, sw=44, sgap=14;
    for(let f=1;f<=F;f++){ const y=bottom-(f-1)*fh; x.strokeStyle='rgba(255,255,255,.08)'; x.beginPath(); x.moveTo(60,y); x.lineTo(W-20,y); x.stroke(); x.fillStyle='rgba(255,255,255,.45)'; x.font='10px sans-serif'; x.fillText(f+'F', 36, y-2);
      const ws=waiting[f]; const n=Math.min(ws.length,18); for(let i=0;i<n;i++){ const age=t-ws[i].t0; const col=age<30?'#a3e635':age<90?'#fbbf24':'#ef4444'; x.fillStyle=col; x.beginPath(); x.arc(70+i*11, y-fh/2, Math.min(4,fh/3), 0, 7); x.fill(); } if(ws.length>18){ x.fillStyle='#e5e7eb'; x.fillText('+'+(ws.length-18), 70+18*11, y-fh/2+3); } }
    cars.forEach((c,i)=>{ const cx=shaftX+i*(sw+sgap); x.fillStyle='rgba(255,255,255,.05)'; x.fillRect(cx,top-fh,sw,bottom-top+fh); const y=bottom-(c.pos-1)*fh; const ch=Math.max(10,fh-2);
      x.fillStyle=c.door>0?'#facc15':(c.dir>0?'#38bdf8':c.dir<0?'#f472b6':'#94a3b8'); x.fillRect(cx+2,y-ch,sw-4,ch); x.fillStyle='#0b1020'; x.font='bold 11px sans-serif'; x.fillText(c.riders.length+'人', cx+10, y-ch/2+4);
      x.fillStyle='#cbd5e1'; x.font='10px sans-serif'; x.fillText((c.dir>0?'▲':c.dir<0?'▼':'■')+(c.door>0?'扉':''), cx+12, bottom+12); });
    const wait=waiting.reduce((a,l)=>a+l.length,0); const served=done+cars.reduce((a,c)=>a+c.riders.length,0);
    x.fillStyle='rgba(255,255,255,.5)'; x.font='11px sans-serif'; x.fillText('経過 '+Math.floor(t/60)+'分'+Math.floor(t%60)+'秒', W-110, 14);
    const avg=served?sumW/served:0; setStat('sAvg', avg.toFixed(0)+'秒'); setStat('sMax', maxW.toFixed(0)+'秒'); setStat('sDone', done+'人'); setStat('sWait', wait+'人');
    const mn={scan:'進行方向優先',sstf:'最短距離優先',fcfs:'先着順'}[$('mode').value];
    setShare(F+'階建て・エレベーター'+E+'台・'+mn+'で実験🛗 平均待ち'+avg.toFixed(0)+'秒・最大待ち'+maxW.toFixed(0)+'秒（'+done+'人輸送）。「押したのに来ない」の正体はアルゴリズム👇'); }
  function loop(){ if(run){ const n=+$('sp').value; for(let i=0;i<n;i++) step(1/6); } draw(); requestAnimationFrame(loop); }
  ['fl','el','mode'].forEach(id=>$(id).addEventListener('change',reset));
  $('toggle').addEventListener('click',()=>{ run=!run; $('toggle').textContent=run?'⏸ 一時停止':'▶ 再生'; });
  $('reset').addEventListener('click',reset);
  reset(); loop();
''')

# ============================================================ 4 信頼の進化
sim(slug="shinrai-shinka", cat="wonder", emoji="🤝", score=72,
    title="信頼の進化シミュレーター（囚人のジレンマ）", model="反復囚人のジレンマ × レプリケーター動学（進化ゲーム理論）",
    model_note="Axelrod (1984)『つきあい方の科学』。協力の進化を説明する古典",
    title_tag="信頼の進化シミュレーター｜ずるい人と正直な人、生き残るのはどっち？（囚人のジレンマ）",
    meta_desc="「常に裏切る」「常に協力」「やられたらやり返す」など6つの戦略を何世代も戦わせ、どの生き方が生き残るかを見る進化ゲームシミュレーター。ノイズ（うっかりミス）や付き合いの長さで勝者が変わる、アクセルロッドの有名な実験をブラウザで再現。",
    og_title="信頼の進化シミュレーター（囚人のジレンマ）", og_desc="ずるい人と正直な人、何世代も戦わせると生き残るのはどっち？",
    card_desc="常に裏切る／常に協力／やられたらやり返す…6つの生き方を何世代も戦わせ、生き残る戦略を観察。",
    lead="裏切れば得、でも全員が裏切れば全員が損。この「囚人のジレンマ」を何度も繰り返す社会で、どんな生き方が生き残るのか。6つの戦略を世代交代させて、信頼が進化する条件を確かめてください。",
    canvas=canvas(640, 360),
    controls=slider("noise", "うっかりミス率（ノイズ）", 0, 0.2, 0.02, 0.01) + slider("rounds", "1回の付き合いの長さ（ラウンド数）", 2, 50, 20, 1, "{v}回")
           + slider("bad", "最初の「常に裏切る」の割合", 5, 80, 40, 5, "{v}%") + slider("sp", "再生速度", 1, 10, 3, 1, "×{v}"),
    buttons=btn("toggle", "⏸ 一時停止") + btn("reset", "リセット"),
    stats=stats([("sGen", "世代", False), ("sTop", "いちばん多い戦略", True), ("sTopP", "その割合", False), ("sCoop", "社会の協力率", False)]),
    legend="面積＝各戦略の人口割合の推移。世代ごとに、得点の高い戦略ほど子孫を多く残します（レプリケーター動学）。",
    article=P("裏切り者だらけの社会でも、<b>「やられたらやり返す（しっぺ返し）」</b>のように「まず協力し、裏切られたら報復し、相手が戻れば許す」戦略は生き残り、やがて社会全体を協力的にします。ただし<b>付き合いが短い</b>か<b>うっかりミスが多い</b>と、報復の連鎖で協力は崩れます。") + '''
<h2>6つの戦略</h2>
''' + T([["🕊️ 常に協力", "何があっても協力", "裏切り者に食い物にされる"], ["😈 常に裏切り", "何があっても裏切る", "短期では最強、長期で孤立"],
          ["🤝 しっぺ返し", "最初は協力。前回相手がした行動をそのまま返す", "アクセルロッドの大会で優勝した戦略"],
          ["🙏 寛容なしっぺ返し", "しっぺ返しだが、裏切られても3割の確率で許す", "ノイズがある世界で最も強い"],
          ["💢 根に持つ", "一度でも裏切られたら永遠に裏切る", "ミスに弱い"], ["🎲 ランダム", "半々で協力／裏切り", "誰からも信用されない"]], ["戦略", "ルール", "特徴"]) + '''
<h2>得点表（囚人のジレンマ）</h2>
''' + T([["両方協力", "3点ずつ"], ["自分だけ裏切り", "自分5点・相手0点"], ["両方裏切り", "1点ずつ"]], ["組み合わせ", "得点"]) + '''
<p>1回きりなら「裏切り」が必ず得です。しかし何度も付き合うと、「裏切ればやり返される」ため、協力し合ったほうが合計点は高くなります。付き合いが長いほど協力の価値が上がる——これを<b>「未来の影」</b>と呼びます。</p>
<h2>アクセルロッドの実験（1980年）</h2>
<p>政治学者ロバート・アクセルロッドは、世界中の研究者から戦略プログラムを募って総当たり戦を行いました。優勝したのは最も短い4行のプログラム「しっぺ返し」。勝った戦略に共通していたのは、①自分から裏切らない（上品）、②裏切りには即座に報復する、③相手が戻れば許す、④分かりやすい、の4点でした。この結果は『つきあい方の科学』として出版され、ビジネス・外交・生物学に大きな影響を与えました。</p>
''',
    faqs=[("ノイズを上げると協力が崩れるのはなぜ？", "しっぺ返し同士がうっかり1回裏切ると、報復が交互に続く「血の復讐」状態になります。これを断ち切れるのが「寛容なしっぺ返し」で、ノイズのある現実世界では寛容さが合理的だと分かります。"),
          ("ラウンド数を減らすとどうなる？", "付き合いが短いと報復の機会が減り、「常に裏切り」が有利になります。一見さん相手の商売で不正が起きやすく、常連相手では起きにくいのと同じ理屈です。"),
          ("これは人間以外にも当てはまる？", "はい。吸血コウモリの血の分け合い、魚の掃除共生、細菌の協力行動など、多くの生物で「反復囚人のジレンマ」型の協力が観察されています。")],
    rel=[("uwasa-kakusan", "🗣️", "噂が全員に届くまで"), ("echo-chamber", "📢", "エコーチェンバー 意見分極"), ("bank-run", "🏦", "銀行の取り付け騒ぎ"), ("schelling", "🏘️", "街の分断シミュレーター")],
    js=r'''
  const cv=$('cv'), x=cv.getContext('2d'), W=cv.width, H=cv.height;
  const STR=[['常に協力','#38bdf8'],['常に裏切り','#ef4444'],['しっぺ返し','#22c55e'],['寛容なしっぺ返し','#a3e635'],['根に持つ','#f59e0b'],['ランダム','#a78bfa']];
  const PAY=[[3,0],[5,1]]; // PAY[me][you] me:0=C 1=D  -> my points
  let pop, gen, hist, run=true, coopRate;
  function act(s, myHist, opHist){ const last=opHist.length?opHist[opHist.length-1]:0;
    switch(s){ case 0: return 0; case 1: return 1; case 2: return last; case 3: return last===1&&Math.random()<0.3?0:last; case 4: return opHist.includes(1)?1:0; default: return Math.random()<0.5?0:1; } }
  function play(a,b){ const n=+$('rounds').value, eps=+$('noise').value; const ha=[],hb=[]; let sa=0,sb=0,coop=0;
    for(let r=0;r<n;r++){ let ma=act(a,ha,hb), mb=act(b,hb,ha); if(Math.random()<eps) ma=1-ma; if(Math.random()<eps) mb=1-mb; sa+=PAY[ma][mb]; sb+=PAY[mb][ma]; coop+=(ma===0)+(mb===0); ha.push(ma); hb.push(mb); }
    return [sa/n, sb/n, coop/(2*n)]; }
  function reset(){ const bad=+$('bad').value/100; const rest=(1-bad)/5; pop=[rest,bad,rest,rest,rest,rest]; gen=0; hist=[pop.slice()]; coopRate=0; draw(); }
  function generation(){ const fit=[0,0,0,0,0,0]; let cw=0, tw=0;
    for(let i=0;i<6;i++) for(let j=i;j<6;j++){ if(pop[i]<1e-4&&pop[j]<1e-4) continue; let si=0,sj=0,c=0; for(let k=0;k<2;k++){ const r=play(i,j); si+=r[0]; sj+=r[1]; c+=r[2]; } si/=2; sj/=2; c/=2;
      fit[i]+=pop[j]*si; if(j!==i) fit[j]+=pop[i]*sj; const w=pop[i]*pop[j]*(i===j?1:2); cw+=w*c; tw+=w; }
    coopRate=tw?cw/tw:0; const mean=pop.reduce((a,p,i)=>a+p*fit[i],0); const mu=0.002;
    pop=pop.map((p,i)=>Math.max(0,p*fit[i]/mean)); const s=pop.reduce((a,b)=>a+b,0); pop=pop.map(p=>p/s*(1-mu*6)+mu); gen++; hist.push(pop.slice()); if(hist.length>220) hist.shift(); }
  function draw(){ x.fillStyle='#0b1020'; x.fillRect(0,0,W,H); const PW=W-170, ph=H-30;
    const L=hist.length; for(let k=0;k<L;k++){ const px=k/Math.max(1,219)*PW; const w=PW/219+0.6; let y=10; for(let i=0;i<6;i++){ const h=hist[k][i]*ph; x.fillStyle=STR[i][1]; x.fillRect(px,y,w,h); y+=h; } }
    x.fillStyle='rgba(255,255,255,.4)'; x.font='11px sans-serif'; x.fillText('世代 →', PW-40, H-6);
    let top=0; pop.forEach((p,i)=>{ if(p>pop[top]) top=i; });
    STR.forEach((s,i)=>{ const y=24+i*30; x.fillStyle=s[1]; x.fillRect(PW+16,y-10,12,12); x.fillStyle='#e5e7eb'; x.font=(i===top?'bold ':'')+'12px sans-serif'; x.fillText(s[0], PW+34, y); x.fillStyle='#94a3b8'; x.fillText(Math.round(pop[i]*100)+'%', PW+34, y+13); });
    setStat('sGen', gen); setStat('sTop', STR[top][0]); setStat('sTopP', Math.round(pop[top]*100)+'%'); setStat('sCoop', Math.round(coopRate*100)+'%');
    setShare('囚人のジレンマを'+gen+'世代進化させたら、最多は「'+STR[top][0]+'」'+Math.round(pop[top]*100)+'%🤝 社会の協力率'+Math.round(coopRate*100)+'%（ミス率'+Math.round(+$('noise').value*100)+'%・付き合い'+$('rounds').value+'回）。信頼が進化する条件👇'); }
  let f=0; function loop(){ if(run){ f++; if(f%Math.max(1,11-+$('sp').value)===0) generation(); } draw(); requestAnimationFrame(loop); }
  ['bad'].forEach(id=>$(id).addEventListener('change',reset));
  $('toggle').addEventListener('click',()=>{ run=!run; $('toggle').textContent=run?'⏸ 一時停止':'▶ 再生'; });
  $('reset').addEventListener('click',reset);
  reset(); loop();
''')

# ============================================================ 5 噂の拡散
sim(slug="uwasa-kakusan", cat="wonder", emoji="🗣️", score=68,
    title="噂が全員に届くまでシミュレーター", model="スモールワールド・ネットワーク（ワッツ＝ストロガッツ）上の伝播",
    model_note="Watts & Strogatz (1998, Nature)。六次の隔たりを説明したネットワーク科学の出発点",
    title_tag="噂が全員に届くまでシミュレーター｜「近道」が少しあるだけで拡散は何倍速くなる？",
    meta_desc="1人に話した噂が、友だちの友だちを伝って全員に届くまで何日かかる？人数・友だちの数・「遠くの知り合い（近道）」の割合・話す確率を変えて、ネットワーク上の拡散をアニメで体感する無料シミュレーター。六次の隔たりの正体。",
    og_title="噂が全員に届くまでシミュレーター", og_desc="遠くの知り合いが少しいるだけで、噂は何倍速く広がる？",
    card_desc="1人に話した噂が全員に届くまで何日？「遠くの知り合い」が数%いるだけで拡散速度が激変。",
    lead="「ここだけの話」を1人にしただけなのに、気づけば全員が知っている。噂は友だちの友だちを伝って広がります。人数・友だちの数・「遠くの知り合い（近道）」の割合を変えて、全員に届くまでの日数を見てください。",
    canvas=canvas(640, 400),
    controls=slider("n", "人数", 30, 200, 100, 10, "{v}人") + slider("k", "1人あたりの友だち数", 2, 10, 4, 2, "{v}人")
           + slider("p", "遠くの知り合い（近道）の割合", 0, 1, 0.1, 0.01) + slider("q", "会ったときに話す確率", 0.1, 1, 0.5, 0.05) + slider("sp", "再生速度", 1, 10, 4, 1, "×{v}"),
    buttons=btn("toggle", "⏸ 一時停止") + btn("reset", "リセット（ネットワークを作り直す）"),
    stats=stats([("sDay", "経過日数", False), ("sKnow", "知っている人", True), ("sAll", "全員に届く日（予測）", False), ("sDist", "平均の“隔たり”", False)]),
    legend="円周に並ぶ点＝人、線＝友だち関係。赤＝噂を知っている人。中央を横切る線が「遠くの知り合い（近道）」です。",
    article=P("友だちが「ご近所」だけの世界では噂はゆっくりしか広がりません。ところが<b>全体の数%が「遠くの知り合い」を持つだけで</b>、全員に届く日数は数分の1に縮みます。これがスモールワールド現象＝「六次の隔たり」の正体です。") + '''
<h2>この画面のネットワーク</h2>
<p>人を円周に並べ、隣り合う k 人と友だちにします（ご近所だけの規則的な世界）。次に、各つながりを確率 p で「ランダムな遠くの誰か」につなぎ替えます。この単純な操作で、ネットワークの性質が劇的に変わることを示したのが1998年のワッツとストロガッツの論文です。</p>
''' + T([["p = 0（近道なし）", "人数に比例", "隣から隣へ、リレーのように広がる"], ["p = 0.01〜0.1", "人数の対数に比例", "ごく少数の近道が“ワープ”になり、一気に短くなる"], ["p = 1（完全ランダム）", "最短", "ただし現実の人間関係には遠い"]], ["近道の割合", "平均の隔たり", "噂の広がり方"]) + '''
<h2>六次の隔たり</h2>
<p>1967年、心理学者ミルグラムはアメリカ中西部の住民に「ボストンの株式仲買人へ手紙を、知り合いだけを経由して届けてください」と依頼しました。届いた手紙の平均経由数は<b>約6人</b>。世界の誰とでも6人でつながる「六次の隔たり」です。2011年のFacebookの調査（7億人）では平均<b>4.74人</b>、2016年には3.57人まで縮まっています。ただし本ページでは、あなたと友だちの間の“隔たり”の平均をBFS（幅優先探索）で実際に計算しています。</p>
<h2>SNSの拡散・感染症・停電にも同じ構造</h2>
<p>「近道」があるネットワークでは、噂も感染症も停電の連鎖も一気に広がります。一方で、ワクチンや情報を「ハブ（つながりの多い人）」に集中的に届けると、少ないコストで拡散を止められる——これもネットワーク科学の重要な結論です。</p>
''',
    faqs=[("「全員に届く日（予測）」はどう計算している？", "リセットのたびに、同じ設定で拡散を裏で20回シミュレーションし、その平均日数を表示しています。実際の1回の結果は運によってばらつきます。"),
          ("話す確率を下げると止まる？", "確率が低くても、いつかは話すので理論上は全員に届きます。ただし日数は大きく伸びます。感染症でいえば「マスクで感染確率を下げる」ことに相当し、ピークを遅らせる効果があります。"),
          ("現実の人間関係との違いは？", "現実には「友だちが極端に多い人（ハブ）」がいて、つながりの数に大きな偏りがあります（スケールフリー性）。本シミュレーターは友だち数を均等にした基本モデルです。")],
    rel=[("kansen-agent", "🦠", "感染はこう広がる"), ("echo-chamber", "📢", "エコーチェンバー 意見分極"), ("ryukou-curve", "📈", "流行はなぜ急に終わる？"), ("forest-fire", "🔥", "森林火災シミュレーター")],
    js=r'''
  const cv=$('cv'), x=cv.getContext('2d'), W=cv.width, H=cv.height;
  let N, adj, know, day, run=true, doneDay, pred, dist, fresh;
  function buildNet(n,k,p){ const a=Array.from({length:n},()=>new Set()); for(let i=0;i<n;i++) for(let j=1;j<=k/2;j++){ let t=(i+j)%n; if(Math.random()<p){ let tries=0; do{ t=Math.random()*n|0; tries++; }while((t===i||a[i].has(t))&&tries<20); } a[i].add(t); a[t].add(i); } return a.map(s=>[...s]); }
  function avgDist(a){ const n=a.length; let tot=0,cnt=0; const S=Math.min(n,40); for(let s=0;s<S;s++){ const src=Math.floor(s*n/S); const d=new Array(n).fill(-1); d[src]=0; const q=[src]; for(let h=0;h<q.length;h++){ const u=q[h]; for(const v of a[u]) if(d[v]<0){ d[v]=d[u]+1; q.push(v); } } for(let i=0;i<n;i++) if(d[i]>0){ tot+=d[i]; cnt++; } } return cnt?tot/cnt:0; }
  function spreadOnce(a,q){ const n=a.length; const kn=new Array(n).fill(false); kn[0]=true; let c=1,d=0; while(c<n&&d<2000){ d++; const nw=[]; for(let i=0;i<n;i++) if(kn[i]) for(const j of a[i]) if(!kn[j]&&Math.random()<q) nw.push(j); for(const j of nw) if(!kn[j]){ kn[j]=true; c++; } } return d; }
  function reset(){ N=+$('n').value; adj=buildNet(N,+$('k').value,+$('p').value); know=new Array(N).fill(false); know[0]=true; fresh=new Set([0]); day=0; doneDay=null;
    dist=avgDist(adj); let s=0; for(let i=0;i<20;i++) s+=spreadOnce(adj,+$('q').value); pred=s/20; draw(); }
  function step(){ if(doneDay!=null) return; day++; const q=+$('q').value; const nw=[]; for(let i=0;i<N;i++) if(know[i]) for(const j of adj[i]) if(!know[j]&&Math.random()<q) nw.push(j); fresh=new Set(nw); nw.forEach(j=>know[j]=true); if(know.every(v=>v)) doneDay=day; }
  function pos(i){ const a=i/N*Math.PI*2-Math.PI/2; const r=Math.min(W,H)/2-24; return [W/2+Math.cos(a)*r, H/2+Math.sin(a)*r]; }
  function draw(){ x.fillStyle='#0b1020'; x.fillRect(0,0,W,H); x.lineWidth=1;
    for(let i=0;i<N;i++) for(const j of adj[i]) if(j>i){ const [ax,ay]=pos(i),[bx,by]=pos(j); const far=Math.min(Math.abs(i-j),N-Math.abs(i-j))>+$('k').value; x.strokeStyle=far?'rgba(167,139,250,.35)':'rgba(255,255,255,.12)'; x.beginPath(); x.moveTo(ax,ay); x.lineTo(bx,by); x.stroke(); }
    for(let i=0;i<N;i++){ const [px,py]=pos(i); x.fillStyle=know[i]?(fresh.has(i)?'#fb923c':'#ef4444'):'#334155'; x.beginPath(); x.arc(px,py,fresh.has(i)?6:4,0,7); x.fill(); }
    const c=know.filter(v=>v).length; x.fillStyle='#e5e7eb'; x.font='bold 22px sans-serif'; x.textAlign='center'; x.fillText(c+' / '+N+'人', W/2, H/2-4); x.font='12px sans-serif'; x.fillStyle='#94a3b8'; x.fillText(day+'日目', W/2, H/2+16); x.textAlign='left';
    setStat('sDay', day+'日'); setStat('sKnow', c+'人（'+Math.round(c/N*100)+'%）'); setStat('sAll', (doneDay!=null?'実測 '+doneDay+'日':'約'+pred.toFixed(1)+'日')); setStat('sDist', dist.toFixed(2)+'人');
    setShare(N+'人の噂は'+(doneDay!=null?doneDay:'約'+pred.toFixed(0))+'日で全員に🗣️ 「遠くの知り合い」'+Math.round(+$('p').value*100)+'%で平均の隔たりは'+dist.toFixed(1)+'人。六次の隔たりの正体を体感👇'); }
  let f=0; function loop(){ if(run){ f++; if(f%Math.max(1,12-+$('sp').value)===0) step(); } draw(); requestAnimationFrame(loop); }
  ['n','k','p','q'].forEach(id=>$(id).addEventListener('change',reset));
  $('toggle').addEventListener('click',()=>{ run=!run; $('toggle').textContent=run?'⏸ 一時停止':'▶ 再生'; });
  $('reset').addEventListener('click',reset);
  reset(); loop();
''')
