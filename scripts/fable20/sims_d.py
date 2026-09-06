# -*- coding: utf-8 -*-
"""Fable20 D: 津波・銀行取り付け・迷路AI・マルコフ文章・感染エージェント"""
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

# ============================================================ 16 津波
sim(slug="tsunami-kishi", cat="wonder", emoji="🌊", score=71,
    title="津波はなぜ岸で高くなる？ シミュレーター", model="浅水波方程式（1次元・有限差分）",
    model_note="津波の伝播予測（気象庁・JAMSTEC）で実際に使われる基礎方程式",
    title_tag="津波はなぜ岸で高くなる？シミュレーター｜沖で1mの津波が岸で何mになるか浅水波方程式で計算",
    meta_desc="沖ではわずか1mの津波が、岸に近づくと数倍の高さになる理由を、津波予測に使われる浅水波方程式をブラウザで解いて再現。水深・海底の傾斜・沖の波高を変えて、到達時間と岸での高さを体感できる無料シミュレーター。グリーンの法則も解説。",
    og_title="津波はなぜ岸で高くなる？ シミュレーター", og_desc="沖で1mの津波が岸で何mに？浅水波方程式で計算。",
    card_desc="沖では1mの津波が岸で数倍に。水深と海底の傾斜を変えて、津波が高くなる瞬間を再現。",
    lead="沖合の船は津波にほとんど気づきません。ところが同じ波が岸に届くと、数倍の高さの壁になります。津波の予測に使われる「浅水波方程式」をブラウザで解いて、水深・傾斜・沖の高さを変えながら、その理由を見てください。",
    canvas=canvas(640, 360),
    controls=slider("depth", "沖の水深", 500, 6000, 3000, 100, "{v}m") + slider("h0", "沖での津波の高さ", 0.3, 3, 1, 0.1, "{v}m")
           + slider("slope", "海底の傾斜（岸に向かう浅くなり方）", 1, 5, 3, 1) + slider("sp", "再生速度", 1, 10, 5, 1, "×{v}"),
    buttons=btn("go", "🌊 津波を発生させる", True) + btn("toggle", "⏸ 一時停止"),
    stats=stats([("sH", "岸での高さ", True), ("sV", "沖の速さ", False), ("sVc", "岸の速さ", False), ("sT", "岸に届くまで", False)]),
    legend="青＝海面（高さを強調表示）、茶＝海底。津波は沖ではジェット機の速さ、岸では自動車の速さ。遅くなった分、波は縮んで高くなります。",
    article=P("津波の速さは水深で決まります（<b>v = √(g × 水深)</b>）。水深4,000mでは時速約700km、水深10mでは時速約36km。岸に近づいて速度が落ちると、後ろから来る波が追いつき、エネルギーが縮んだ分だけ<b>高さが上がります</b>。沖で1mなら、岸で3〜5mになることも珍しくありません。") + '''
<h2>この画面で解いている式</h2>
''' + N("∂h/∂t + ∂(hu)/∂x = 0　（水の量は保存する）<br>∂u/∂t + u ∂u/∂x + g ∂η/∂x = 0　（水は水面の傾きの方向に加速する）") + '''
<p>水深に比べて波長がはるかに長い波（津波の波長は数十〜数百km）は、この「浅水波方程式」で正確に記述できます。気象庁の津波予報も、この式を3次元の海底地形に適用して計算しています。本ページは1次元・有限差分法で、沖から岸までの断面を毎フレーム解いています。</p>
<h2>グリーンの法則：高さは水深の4乗根に反比例</h2>
''' + T([["4,000m", "約710km/h", "1.0m（基準）"], ["1,000m", "約360km/h", "1.4m"], ["100m", "約110km/h", "2.5m"], ["10m", "約36km/h", "4.5m"]], ["水深", "津波の速さ", "高さ（沖で1mの場合の理論値）"]) + '''
<p>エネルギーが保存されるとき、津波の高さは水深の1/4乗に反比例します（グリーンの法則）。水深が4,000mから10mに（400分の1に）なると、高さは 400^0.25 ≈ 4.5倍。実際には湾の形（V字湾で集中）や海底の摩擦、砕波でさらに変わりますが、この式が「沖で小さく岸で大きい」理由の本質です。</p>
<h2>「引き波」と逃げる時間</h2>
<p>沖で津波が発生すると、岸に届くまでの時間は距離÷速さ。震源が近い日本海溝沿いでは<b>数分〜30分</b>で到達します。2011年の東北地方太平洋沖地震では、沖合のGPS波浪計で高さ約6mの津波を観測した後、岸では10〜15m（遡上高は最大40m）に達しました。「揺れたら、高い所へ」が鉄則である理由がこの速さと増幅にあります。</p>
''',
    faqs=[("普通の波と津波は何が違う？", "風の波は波長が数十mで海面付近だけが動きますが、津波は波長が数十〜数百kmあり、海底から海面まで水全体が動きます。そのため運ぶエネルギーが桁違いで、高さ1mでも人は流されます。"),
          ("岸での高さが理論値と違うのは？", "本シミュレーターは海底の摩擦・砕波・波の非線形効果を簡略化しており、傾斜が急だと理論値より低く、緩いと近い値になります。実際の津波は湾の形状でさらに2〜3倍になることもあります。"),
          ("津波の速さを実感するには？", "水深4,000mでの時速700kmはジェット旅客機と同じです。沖にいる船が津波に気づかないのは、高さ1m・波長100kmの“うねり”が数分かけて通過するだけだからです。")],
    rel=[("building-quake", "🏢", "地震でビルはどう揺れる？"), ("jishin-live", "🗾", "日本はいまも揺れている"), ("ripple", "💧", "波紋シミュレーター"), ("wave", "🌊", "波の干渉シミュレーター")],
    js=r'''
  const cv=$('cv'), x=cv.getContext('2d'), W=cv.width, H=cv.height;
  const NX=300, LEN=200000; // 200km 断面
  let h, u, d, t, run=true, started=false, maxCoast=0, arrive=null, dxm=LEN/NX;
  const g=9.81;
  function bathy(){ const D=+$('depth').value, s=+$('slope').value; d=new Float64Array(NX); for(let i=0;i<NX;i++){ const r=i/(NX-1); // 0=沖 1=岸
      const k=[0.7,1.0,1.5,2.2,3.0][s-1]; d[i]=Math.max(5, D*Math.pow(1-r,k)); } }
  function reset(){ bathy(); h=new Float64Array(NX); u=new Float64Array(NX); t=0; started=false; maxCoast=0; arrive=null; draw(); }
  // u[i] は h[i] と h[i+1] の間（スタッガード格子）。線形＋弱非線形の浅水波を leapfrog で解く
  function go(){ reset(); const A=+$('h0').value; for(let i=0;i<NX;i++){ const xx=(i-30)/9; h[i]=A*Math.exp(-xx*xx); } for(let i=0;i<NX-1;i++){ u[i]=0.5*(h[i]+h[i+1])*Math.sqrt(g/(0.5*(d[i]+d[i+1]))); } started=true; }
  function step(){ const cmax=Math.sqrt(g*(+$('depth').value+3)); const dt=0.4*dxm/cmax;
    for(let i=0;i<NX-1;i++){ const dh=(h[i+1]-h[i])/dxm; const Hm=0.5*(d[i]+d[i+1]+h[i]+h[i+1]); u[i]-=dt*g*dh; u[i]*=1-dt*0.001*Math.abs(u[i])/Math.max(3,Hm); }
    u[NX-1]=0;
    for(let i=1;i<NX;i++){ const Hl=Math.max(0.5,d[i-1]+h[i-1]), Hr=Math.max(0.5,d[i]+h[i]); const fl=0.5*(Hl+Hr)*u[i-1]; const fr=i<NX-1?0.5*(Hr+Math.max(0.5,d[i+1]+h[i+1]))*u[i]:0; h[i]-=dt*(fr-fl)/dxm; }
    // 沖側スポンジ（反射を吸収）
    for(let i=0;i<16;i++){ const k=1-0.06*(16-i)/16; h[i]*=k; u[i]*=k; }
    t+=dt;
    const coast=Math.max(h[NX-2],h[NX-3],h[NX-4]); if(coast>maxCoast) maxCoast=coast; if(arrive==null&&coast>+$('h0').value*0.3) arrive=t; }
  function draw(){ x.fillStyle='#0b1020'; x.fillRect(0,0,W,H); const D=+$('depth').value; const top=40, bot=H-24; const sy=(depth)=>top+80+(depth/D)*(bot-top-80);
    x.fillStyle='#6b4f2a'; x.beginPath(); x.moveTo(0,bot); for(let i=0;i<NX;i++) x.lineTo(i/(NX-1)*W, sy(d[i])); x.lineTo(W,bot); x.fill();
    const amp=60/Math.max(1,+$('h0').value*3); x.fillStyle='rgba(56,189,248,.55)'; x.beginPath(); x.moveTo(0,sy(0)); for(let i=0;i<NX;i++) x.lineTo(i/(NX-1)*W, sy(0)-h[i]*amp); x.lineTo(W,sy(0)); for(let i=NX-1;i>=0;i--) x.lineTo(i/(NX-1)*W, sy(d[i])); x.closePath(); x.fill();
    x.strokeStyle='#e0f2fe'; x.lineWidth=2; x.beginPath(); for(let i=0;i<NX;i++){ const X=i/(NX-1)*W, Y=sy(0)-h[i]*amp; i?x.lineTo(X,Y):x.moveTo(X,Y); } x.stroke();
    x.fillStyle='rgba(255,255,255,.5)'; x.font='11px sans-serif'; x.fillText('沖（水深'+D+'m）', 8, 16); x.fillText('岸 →', W-40, 16); x.fillText('※波の高さは強調表示', 8, 30);
    const i0=20; let ii=0,mx=0; for(let i=0;i<NX;i++) if(h[i]>mx){mx=h[i];ii=i;} if(started&&mx>0.05){ x.fillStyle='#fbbf24'; x.font='bold 12px sans-serif'; x.fillText('▲ '+mx.toFixed(1)+'m / 時速'+Math.round(Math.sqrt(g*d[ii])*3.6)+'km', clamp(ii/(NX-1)*W-40,0,W-150), sy(0)-mx*amp-8); }
    x.fillStyle='rgba(255,255,255,.5)'; x.font='11px sans-serif'; x.fillText('経過 '+Math.floor(t/60)+'分'+Math.floor(t%60)+'秒', W-110, H-8);
    const v0=Math.sqrt(g*D)*3.6, vc=Math.sqrt(g*10)*3.6;
    setStat('sH', started?maxCoast.toFixed(1)+'m':'—'); setStat('sV', '時速'+Math.round(v0)+'km'); setStat('sVc', '時速'+Math.round(vc)+'km'); setStat('sT', arrive!=null?Math.floor(arrive/60)+'分'+Math.floor(arrive%60)+'秒':'—');
    setShare('沖（水深'+D+'m）で'+$('h0').value+'mの津波→岸では'+(started?maxCoast.toFixed(1):'？')+'m🌊 沖の速さは時速'+Math.round(v0)+'km（ジェット機並み）、岸まで'+(arrive!=null?Math.floor(arrive/60)+'分':'？')+'。津波が岸で高くなる理由👇'); }
  function loop(){ if(run&&started){ for(let i=0;i<+$('sp').value*2;i++) step(); } draw(); requestAnimationFrame(loop); }
  ['depth','slope'].forEach(id=>$(id).addEventListener('input',reset));
  $('go').addEventListener('click',go); $('toggle').addEventListener('click',()=>{ run=!run; $('toggle').textContent=run?'⏸ 一時停止':'▶ 再生'; });
  go(); loop();
''')

# ============================================================ 17 銀行の取り付け騒ぎ
sim(slug="bank-run", cat="finance", emoji="🏦", score=70,
    title="銀行の取り付け騒ぎシミュレーター", model="ダイアモンド＝ディビッグ型モデル＋不安の伝播（エージェントベース）",
    model_note="Diamond & Dybvig (1983, ノーベル経済学賞2022)。預金保険制度の理論的根拠",
    title_tag="銀行の取り付け騒ぎシミュレーター｜健全な銀行でも噂だけで倒産する理由（ダイアモンド＝ディビッグ）",
    meta_desc="銀行は預金の一部しか手元に置いていない。だから「危ないらしい」という噂で預金者が一斉に引き出せば、健全な銀行でも倒産する——2022年ノーベル経済学賞のモデルをエージェントシミュレーションで再現。準備率・不安の伝わりやすさ・預金保険の有無で結果がどう変わるかを体感。",
    og_title="銀行の取り付け騒ぎシミュレーター", og_desc="健全な銀行でも噂だけで倒産する。預金保険の効果を体感。",
    card_desc="健全な銀行でも「危ないらしい」の噂で倒産する。準備率と預金保険で結果がどう変わるか。",
    lead="銀行はあなたの預金の大半を貸し出していて、手元にあるのはごく一部。だから「あの銀行、危ないらしい」と噂が広がって皆が一斉に引き出せば、健全な銀行でも倒れます。不安の伝わりやすさ・準備率・預金保険を変えて、パニックが起きる条件を見てください。",
    canvas=canvas(640, 380),
    controls=slider("res", "銀行の手元資金（準備率）", 5, 60, 15, 5, "{v}%") + slider("panic", "不安の伝わりやすさ", 0, 1, 0.4, 0.05)
           + slider("seed", "最初に不安になる人", 1, 20, 2, 1, "{v}%") + select("ins", "預金保険", [("no", "なし"), ("yes", "あり（1,000万円まで保護）")]) + slider("sp", "再生速度", 1, 10, 4, 1, "×{v}"),
    buttons=btn("toggle", "⏸ 一時停止") + btn("reset", "リセット") + btn("rumor", "📰 「危ないらしい」と噂を流す"),
    stats=stats([("sDay", "経過日数", False), ("sRes", "銀行の残り資金", True), ("sQ", "引き出しに並ぶ人", False), ("sState", "銀行の状態", False)]),
    legend="点＝預金者（灰＝安心、黄＝不安、赤＝引き出し済み）。右のバー＝銀行の手元資金。資金が尽きた瞬間、残りの人は引き出せなくなります。",
    article=P("取り付け騒ぎの恐ろしさは、<b>「皆が引き出すと思うから引き出す」という予想が自己実現する</b>ことです。銀行が健全かどうかは関係ありません。この構造を数学的に示したのがダイアモンドとディビッグ（1983年）で、2022年にノーベル経済学賞を受けました。解決策は預金保険＝「取り付けに参加しなくても損しない」保証です。") + '''
<h2>なぜ銀行は全額を手元に置かないのか</h2>
<p>銀行の仕事は、いつでも引き出せる預金を集め、それを長期の貸出（住宅ローン・企業融資）に回すことです。貸したお金はすぐには戻らないため、手元に残す現金は預金の数%〜十数%（準備率）。これは無責任ではなく、経済にお金を循環させる銀行の本質的な役割です。ただし「全員が同時に引き出す」ことだけには耐えられません。</p>
<h2>2つの均衡：良い世界と悪い世界</h2>
''' + T([["良い均衡", "皆が「他の人は引き出さない」と信じる", "必要な人だけ引き出し、銀行は問題なく機能"], ["悪い均衡", "皆が「他の人が引き出す」と信じる", "全員が窓口に殺到し、健全な銀行が倒産"]], ["均衡", "預金者の予想", "結果"]) + '''
<p>どちらの世界になるかは、銀行の財務ではなく<b>預金者の予想</b>で決まります。噂・SNS・報道が予想を切り替えるスイッチになるため、「危ないらしい」という一言が実際に銀行を倒せるのです。</p>
<h2>2023年、SNS時代の取り付け</h2>
<p>2023年3月、米シリコンバレー銀行では、SNSで不安が拡散してから<b>わずか1日で約420億ドル（総預金の約4分の1）</b>が引き出され、翌日に破綻しました。かつては窓口の行列が必要だった取り付けが、スマホの操作で数時間に圧縮された事例です。本シミュレーターの「不安の伝わりやすさ」を上げると、この速さが再現できます。</p>
<h2>預金保険という発明</h2>
<p>日本では預金保険制度により、1金融機関あたり元本1,000万円とその利息までが保護されます（決済用預金は全額）。「引き出さなくても損しない」ことが保証されれば、悪い均衡に飛び移る理由がなくなります。本ページで預金保険を「あり」にすると、噂が流れても不安が広がりにくくなることが確認できます。</p>
''',
    faqs=[("準備率を上げれば安全？", "上げるほど取り付けには強くなりますが、その分貸し出せるお金が減り、銀行の本来の機能（お金を回す）が弱まります。準備率100%の銀行は取り付けに耐えますが、それはもはや「金庫」です。"),
          ("預金保険があれば絶対に起きない？", "保護限度額を超える大口預金者（企業など）は依然として引き出す動機があり、シリコンバレー銀行では預金の9割超が限度額超過でした。制度は個人のパニックを止めるのに有効ですが、万能ではありません。"),
          ("このモデルで日本の銀行を評価できる？", "できません。本ページは「噂と予想で取り付けが起きる仕組み」を示す抽象モデルで、実在の銀行の健全性とは無関係です。")],
    rel=[("shinrai-shinka", "🤝", "信頼の進化"), ("uwasa-kakusan", "🗣️", "噂が全員に届くまで"), ("ryukou-curve", "📈", "流行はなぜ急に終わる？"), ("infure", "📉", "物価2倍まで何年？")],
    js=r'''
  const cv=$('cv'), x=cv.getContext('2d'), W=cv.width, H=cv.height, NP=400;
  let st, cash, day, run=true, dead=false, queue=0, hist=[];
  // st: 0=安心 1=不安 2=引き出し済み 3=引き出せなかった
  function reset(){ st=new Array(NP).fill(0); const s=Math.round(NP*+$('seed').value/100); for(let i=0;i<s;i++) st[Math.random()*NP|0]=1; cash=+$('res').value/100*NP; day=0; dead=false; queue=0; hist=[cash]; draw(); }
  function step(){ if(dead) return; day++; const p=+$('panic').value, ins=$('ins').value==='yes'; const R=+$('res').value/100*NP; const nb=[];
    cash=Math.min(R, cash+(R-cash)*0.2); // 銀行は毎日、貸出の回収・資産売却で少しずつ現金を補充
    for(let i=0;i<NP;i++){ if(st[i]!==0) continue; let anx=0; for(let k=0;k<6;k++){ const j=Math.random()*NP|0; if(st[j]===1) anx++; if(st[j]===2) anx+=0.25; if(st[j]===3) anx+=3; }
      const drop=(cash/R)<0.25; const prob=p*(anx/6)*(ins?0.15:1)+(drop?0.12*(ins?0.3:1):0); if(Math.random()<prob) nb.push(i); }
    nb.forEach(i=>st[i]=1);
    queue=0; for(let i=0;i<NP;i++){ if(st[i]===1){ if(Math.random()<0.35){ if(cash>=1){ cash-=1; st[i]=2; } else { st[i]=3; } } else queue++; } }
    if(cash<1 && st.some(s=>s===1||s===3)){ dead=true; st=st.map(s=>s===1?3:s); }
    if(!dead){ for(let i=0;i<NP;i++){ if(st[i]===1&&Math.random()<(ins?0.5:0.2)) st[i]=0; else if(st[i]===2&&Math.random()<(ins?0.08:0.03)){ st[i]=0; cash=Math.min(R,cash+1); } } }
    hist.push(cash); if(hist.length>120) hist.shift(); }
  function draw(){ x.fillStyle='#0b1020'; x.fillRect(0,0,W,H); const cols=25, cell=18;
    for(let i=0;i<NP;i++){ const c=i%cols, r=Math.floor(i/cols); const px=16+c*cell, py=16+r*cell; x.fillStyle=['#475569','#fbbf24','#ef4444','#7f1d1d'][st[i]]; x.beginPath(); x.arc(px+7,py+7,st[i]===1?7:6,0,7); x.fill(); }
    const bx=500, by=30, bw=100, bh=H-70; const R=+$('res').value/100*NP; x.strokeStyle='#94a3b8'; x.strokeRect(bx,by,bw,bh); const fh=Math.max(0,cash/R)*bh; x.fillStyle=cash/R>0.5?'#22c55e':cash/R>0.2?'#f59e0b':'#ef4444'; x.fillRect(bx,by+bh-fh,bw,fh);
    x.fillStyle='#e5e7eb'; x.font='bold 12px sans-serif'; x.fillText('銀行の手元資金', bx-6, by-10); x.fillText(Math.round(cash/R*100)+'%', bx+30, by+bh/2);
    x.fillStyle='#94a3b8'; x.font='11px sans-serif'; x.fillText('（預金総額の'+$('res').value+'%）', bx-10, by+bh+18);
    if(dead){ x.fillStyle='rgba(127,29,29,.85)'; x.fillRect(16,H/2-40,460,80); x.fillStyle='#fff'; x.font='bold 22px sans-serif'; x.fillText('💥 資金が尽きました（取り付け騒ぎ）', 40, H/2+8); }
    const n2=st.filter(s=>s===2).length, n3=st.filter(s=>s===3).length, n1=st.filter(s=>s===1).length;
    setStat('sDay', day+'日'); setStat('sRes', Math.round(cash/R*100)+'%'); setStat('sQ', (n1)+'人'); setStat('sState', dead?'破綻（'+n3+'人が引き出せず）':n1>NP*0.1?'⚠️ 窓口に行列':'平常');
    setShare('準備率'+$('res').value+'%・不安の伝わりやすさ'+$('panic').value+'・預金保険'+($('ins').value==='yes'?'あり':'なし')+'→'+day+'日目に'+(dead?'銀行が破綻🏦💥 '+n3+'人が引き出せず':'手元資金'+Math.round(cash/R*100)+'%で耐えている🏦')+'。噂だけで健全な銀行が倒れる仕組み👇'); }
  let f=0; function loop(){ if(run){ f++; if(f%Math.max(1,12-+$('sp').value)===0) step(); } draw(); requestAnimationFrame(loop); }
  ['res','seed','ins'].forEach(id=>$(id).addEventListener('change',reset));
  $('toggle').addEventListener('click',()=>{ run=!run; $('toggle').textContent=run?'⏸ 一時停止':'▶ 再生'; });
  $('reset').addEventListener('click',reset);
  $('rumor').addEventListener('click',()=>{ if(dead) return; for(let i=0;i<NP;i++) if(st[i]===0&&Math.random()<0.2) st[i]=1; });
  reset(); loop();
''')

# ============================================================ 18 迷路をAIが解く
sim(slug="maze-ai", cat="play", emoji="🧩", score=69,
    title="迷路をAIが解く 探索アルゴリズム対決", model="グラフ探索（幅優先／深さ優先／A*／貪欲法）＋迷路生成（再帰的バックトラック）",
    model_note="Hart, Nilsson & Raphael (1968) A*。カーナビ・ゲームAI・配送計画の経路探索の基礎",
    title_tag="迷路をAIが解く 探索アルゴリズム対決｜幅優先・深さ優先・A*はどう違う？アニメで比較",
    meta_desc="自動生成した迷路を、幅優先探索・深さ優先探索・A*・貪欲法の4つのアルゴリズムが解く様子をアニメで比較する無料シミュレーター。調べたマス数と経路の長さで「賢い探し方」の違いが分かる。カーナビの経路探索のしくみ。",
    og_title="迷路をAIが解く 探索アルゴリズム対決", og_desc="幅優先・深さ優先・A*・貪欲法。4つの解き方をアニメで比較。",
    card_desc="自動生成した迷路を4つのアルゴリズムが解く。調べたマス数と経路の長さで「賢さ」を比較。",
    lead="カーナビが一瞬でルートを出せるのは、迷路を賢く探す「アルゴリズム」のおかげ。同じ迷路を、しらみつぶしに調べる方法・一本道を突き進む方法・ゴールの方向を推定する方法で解かせて、調べたマスの数と見つけた経路の違いを見てください。",
    canvas=canvas(640, 400),
    controls=select("algo", "アルゴリズム", [("astar", "A*（エースター）：距離＋ゴールまでの推定"), ("bfs", "幅優先探索：近い順にしらみつぶし"), ("dfs", "深さ優先探索：一本道を突き進む"), ("greedy", "貪欲法：ゴールに近そうな方へ")])
           + slider("size", "迷路の大きさ", 10, 40, 24, 2, "{v}マス") + slider("loops", "抜け道の多さ", 0, 30, 5, 1, "{v}%") + slider("sp", "再生速度", 1, 10, 5, 1, "×{v}"),
    buttons=btn("solve", "▶ 解かせる", True) + btn("newmaze", "🔀 新しい迷路") + btn("compare", "📊 4つ全部で比較"),
    stats=stats([("sVis", "調べたマス", False), ("sLen", "経路の長さ", True), ("sOpt", "最短との差", False), ("sRes", "比較結果", False)]),
    legend="青＝調べたマス、黄＝いま調べている先端、緑＝見つけた経路。左上がスタート、右下がゴール。",
    article=P("賢い探索とは「調べるマスを減らしつつ、最短の経路を見つける」こと。<b>幅優先は必ず最短だが調べすぎ、深さ優先は速いが遠回り、貪欲法は速いが最短の保証なし。A*はゴールまでの推定距離を使って、最短を保証しつつ調べるマスを減らします</b>。カーナビ・ゲームのキャラ・配送計画はほぼA*の仲間です。") + '''
<h2>4つのアルゴリズム</h2>
''' + T([["幅優先探索（BFS）", "スタートから近い順に全部調べる", "必ず最短", "調べるマスが多い"], ["深さ優先探索（DFS）", "行けるところまで進み、行き止まりで戻る", "メモリが少なくて済む", "最短でないことが多い"],
          ["貪欲法（Greedy）", "ゴールまでの直線距離が近いマスを優先", "調べるマスが少ない", "壁に阻まれると遠回りに"], ["A*（エースター）", "「ここまでの距離＋ゴールまでの推定」が小さい順", "最短を保証しつつ効率的", "推定（ヒューリスティック）の設計が要"]], ["アルゴリズム", "探し方", "長所", "短所"]) + '''
<h2>A*が「賢い」理由</h2>
<p>A*は各マスに <b>f = g + h</b> という点数を付けます。g はスタートからの実距離、h はゴールまでの推定距離（迷路ならマンハッタン距離）。h が「実際の距離を超えない」推定なら、A*は必ず最短経路を見つけることが証明されています。1968年にスタンフォード研究所のロボット「シェーキー」の経路計画のために開発されました。</p>
<h2>現実での使われ方</h2>
''' + T([["カーナビ・地図アプリ", "道路をグラフとみなし、A*やその改良版（ダイクストラ法＋前処理）で最短ルート"], ["ゲームのキャラクター", "敵キャラが壁を避けてプレイヤーに向かう移動はほぼA*"], ["配送・物流", "倉庫ロボットの走行経路、配送順の決定"], ["ネットワーク", "インターネットのパケットの経路選択（ダイクストラ法）"]], ["分野", "使い方"]) + '''
<h2>観察のコツ</h2>
<p>「抜け道の多さ」を上げると迷路に複数の経路が生まれ、深さ優先と貪欲法が遠回りする様子がはっきり見えます。抜け道0%（完全迷路）では経路が1本しかないため、どのアルゴリズムも同じ経路にたどり着き、違いは「調べたマスの数」だけになります。</p>
''',
    faqs=[("迷路はどう作っている？", "「再帰的バックトラック」という方法で、スタートから壁を掘り進み、行き止まりで戻る操作を繰り返して完全迷路（経路が1本）を作ります。「抜け道の多さ」の分だけ、あとから壁をランダムに壊しています。"),
          ("A*が幅優先より調べるマスが少ないのはなぜ？", "幅優先はゴールの方向を知らないため、全方向に均等に広がります。A*はゴールまでの推定距離で「見込みのない方向」を後回しにできるため、無駄な探索が減ります。"),
          ("貪欲法が遠回りする理由は？", "「ゴールに近そう」だけで選ぶため、壁の裏側の行き止まりに引き込まれます。戻って別の道を探す間に、経路が長くなります。")],
    rel=[("ga-route", "🧬", "遺伝的アルゴリズムで最短ルート"), ("neural-play", "🧠", "ニューラルネットが学ぶ瞬間"), ("sort-visualizer", "📊", "ソートアルゴリズム可視化"), ("markov-bunsho", "✍️", "AIはこうやって文章を作る")],
    js=r'''
  const cv=$('cv'), x=cv.getContext('2d'), W=cv.width, H=cv.height;
  let n, grid, cell, S, G, state=null, results={};
  const K=(r,c)=>r*n+c;
  function gen(){ n=+$('size').value; cell=Math.min((W-20)/n,(H-20)/n); grid=Array.from({length:n},()=>Array.from({length:n},()=>({N:1,S:1,E:1,W:1,v:false})));
    const st=[[0,0]]; grid[0][0].v=true; while(st.length){ const [r,c]=st[st.length-1]; const nb=[]; if(r>0&&!grid[r-1][c].v) nb.push([r-1,c,'N','S']); if(r<n-1&&!grid[r+1][c].v) nb.push([r+1,c,'S','N']); if(c>0&&!grid[r][c-1].v) nb.push([r,c-1,'W','E']); if(c<n-1&&!grid[r][c+1].v) nb.push([r,c+1,'E','W']);
      if(!nb.length){ st.pop(); continue; } const [nr,nc,a,b]=nb[Math.random()*nb.length|0]; grid[r][c][a]=0; grid[nr][nc][b]=0; grid[nr][nc].v=true; st.push([nr,nc]); }
    const extra=Math.round(n*n*+$('loops').value/100); for(let k=0;k<extra;k++){ const r=Math.random()*n|0, c=Math.random()*n|0; if(Math.random()<0.5&&c<n-1){ grid[r][c].E=0; grid[r][c+1].W=0; } else if(r<n-1){ grid[r][c].S=0; grid[r+1][c].N=0; } }
    S=[0,0]; G=[n-1,n-1]; state=null; results={}; setStat('sRes','—'); draw(); }
  function nbrs(r,c){ const o=[]; const g=grid[r][c]; if(!g.N) o.push([r-1,c]); if(!g.S) o.push([r+1,c]); if(!g.W) o.push([r,c-1]); if(!g.E) o.push([r,c+1]); return o; }
  function hfn(r,c){ return Math.abs(G[0]-r)+Math.abs(G[1]-c); }
  function start(algo){ const open=[{r:0,c:0,g:0,f:hfn(0,0)}]; state={algo, open, closed:new Set(), prev:new Map(), path:null, visited:0, done:false, gmap:new Map([[K(0,0),0]])}; }
  function tick(){ const s=state; if(!s||s.done) return; if(!s.open.length){ s.done=true; return; }
    let idx=0; if(s.algo==='bfs') idx=0; else if(s.algo==='dfs') idx=s.open.length-1; else { let best=1e9; s.open.forEach((o,i)=>{ const v=s.algo==='astar'?o.g+hfn(o.r,o.c):hfn(o.r,o.c); if(v<best){best=v;idx=i;} }); }
    const cur=s.open.splice(idx,1)[0]; const k=K(cur.r,cur.c); if(s.closed.has(k)) return; s.closed.add(k); s.visited++;
    if(cur.r===G[0]&&cur.c===G[1]){ const p=[]; let key=k; while(key!=null){ p.push(key); key=s.prev.get(key); } s.path=p; s.done=true; return; }
    for(const [nr,nc] of nbrs(cur.r,cur.c)){ const nk=K(nr,nc); if(s.closed.has(nk)) continue; const ng=cur.g+1; if(s.algo==='astar'||s.algo==='bfs'){ if(s.gmap.has(nk)&&s.gmap.get(nk)<=ng) continue; } else if(s.gmap.has(nk)) continue; s.gmap.set(nk,ng); s.prev.set(nk,k); s.open.push({r:nr,c:nc,g:ng}); } }
  function shortest(){ const q=[[0,0]]; const d=new Map([[0,0]]); while(q.length){ const [r,c]=q.shift(); if(r===G[0]&&c===G[1]) return d.get(K(r,c)); for(const [nr,nc] of nbrs(r,c)){ const k=K(nr,nc); if(!d.has(k)){ d.set(k,d.get(K(r,c))+1); q.push([nr,nc]); } } } return null; }
  function draw(){ x.fillStyle='#0b1020'; x.fillRect(0,0,W,H); const ox=(W-cell*n)/2, oy=(H-cell*n)/2;
    if(state){ x.fillStyle='rgba(59,130,246,.35)'; state.closed.forEach(k=>{ x.fillRect(ox+(k%n)*cell, oy+Math.floor(k/n)*cell, cell, cell); }); x.fillStyle='#fbbf24'; state.open.forEach(o=>x.fillRect(ox+o.c*cell+cell*0.25, oy+o.r*cell+cell*0.25, cell*0.5, cell*0.5));
      if(state.path){ x.strokeStyle='#4ade80'; x.lineWidth=Math.max(2,cell*0.35); x.beginPath(); state.path.forEach((k,i)=>{ const X=ox+(k%n+0.5)*cell, Y=oy+(Math.floor(k/n)+0.5)*cell; i?x.lineTo(X,Y):x.moveTo(X,Y); }); x.stroke(); } }
    x.strokeStyle='#e5e7eb'; x.lineWidth=2; x.beginPath(); for(let r=0;r<n;r++) for(let c=0;c<n;c++){ const g=grid[r][c], X=ox+c*cell, Y=oy+r*cell; if(g.N){ x.moveTo(X,Y); x.lineTo(X+cell,Y); } if(g.W){ x.moveTo(X,Y); x.lineTo(X,Y+cell); } if(g.S){ x.moveTo(X,Y+cell); x.lineTo(X+cell,Y+cell); } if(g.E){ x.moveTo(X+cell,Y); x.lineTo(X+cell,Y+cell); } } x.stroke();
    x.fillStyle='#f472b6'; x.fillRect(ox+cell*0.2,oy+cell*0.2,cell*0.6,cell*0.6); x.fillStyle='#22c55e'; x.fillRect(ox+(n-1)*cell+cell*0.2,oy+(n-1)*cell+cell*0.2,cell*0.6,cell*0.6);
    const opt=shortest(); const nm={astar:'A*',bfs:'幅優先',dfs:'深さ優先',greedy:'貪欲法'};
    if(state){ setStat('sVis', state.visited+'マス'); setStat('sLen', state.path?(state.path.length-1)+'歩':'探索中'); setStat('sOpt', state.path?'+'+(state.path.length-1-opt)+'歩':'—');
      if(state.path) setShare(n+'×'+n+'の迷路を'+nm[state.algo]+'が解いた🧩 調べたマス'+state.visited+'・経路'+(state.path.length-1)+'歩（最短'+opt+'歩）。カーナビの探索アルゴリズムを体感👇'); } }
  function loop(){ if(state&&!state.done){ for(let i=0;i<+$('sp').value;i++) tick(); } draw(); requestAnimationFrame(loop); }
  $('solve').addEventListener('click',()=>start($('algo').value)); $('newmaze').addEventListener('click',gen); ['size','loops'].forEach(id=>$(id).addEventListener('change',gen));
  $('compare').addEventListener('click',()=>{ const out=[]; for(const a of ['astar','bfs','dfs','greedy']){ start(a); while(!state.done) tick(); out.push({a,v:state.visited,l:state.path?state.path.length-1:'-'}); } const nm={astar:'A*',bfs:'幅優先',dfs:'深さ優先',greedy:'貪欲法'}; setStat('sRes', out.map(o=>nm[o.a]+' '+o.v+'マス/'+o.l+'歩').join('　')); start($('algo').value); setShare('同じ迷路で比較🧩 '+out.map(o=>nm[o.a]+'：調べた'+o.v+'マス・経路'+o.l+'歩').join('／')+'。A*が賢い理由👇'); });
  gen(); start('astar'); loop();
''')

# ============================================================ 19 マルコフ連鎖で文章
sim(slug="markov-bunsho", cat="play", emoji="✍️", score=72,
    title="AIはこうやって文章を作る マルコフ連鎖シミュレーター", model="n-gram言語モデル（マルコフ連鎖）＋温度サンプリング",
    model_note="Shannon (1948)。ChatGPTの「次の語を予測する」原理の最小版",
    title_tag="AIはこうやって文章を作る｜マルコフ連鎖で「次の文字を予測する」言語モデルの最小版を体感",
    meta_desc="文章を貼り付けると、「直前の数文字から次の文字の確率を数える」だけの最小の言語モデル（マルコフ連鎖）が学習し、それっぽい文章を生成する無料シミュレーター。記憶の長さ（n）と温度を変えると、ChatGPTの“らしさ”と“暴走”の関係が体感できる。",
    og_title="AIはこうやって文章を作る マルコフ連鎖シミュレーター", og_desc="「次の文字を予測する」だけの最小言語モデルを体感。",
    card_desc="文章を貼ると「次の文字の確率」を数えて学習し、それっぽい文を生成。ChatGPTの原理の最小版。",
    lead="ChatGPTがやっていることを一言でいえば「次に来る言葉を予測する」。その最小版が、直前の数文字から次の文字の出現確率を数えるだけの「マルコフ連鎖」です。好きな文章を貼り付けて学習させ、記憶の長さと“温度”を変えると、AIらしさと暴走の境目が見えてきます。",
    canvas="",
    controls='''<div class="field" style="grid-column:1/-1;"><div class="slider-head"><label for="src">学習させる文章（長いほど賢くなります）</label></div><textarea id="src" rows="6" style="width:100%;padding:10px;border:1px solid var(--line);border-radius:8px;font-size:13px;line-height:1.6;"></textarea></div>'''
           + slider("order", "記憶の長さ n（直前の何文字を見るか）", 1, 6, 2, 1, "{v}文字") + slider("temp", "温度（ランダムさ）", 0.2, 2.0, 1.0, 0.1) + slider("len", "生成する長さ", 50, 400, 150, 10, "{v}文字"),
    buttons=btn("gen", "✍️ 文章を生成する", True) + btn("sample1", "例：昔話") + btn("sample2", "例：ニュース風") + btn("sample3", "例：自分で書く"),
    stats=stats([("sV", "学習した文字の種類", False), ("sCtx", "覚えたパターン数", True), ("sPerp", "次の文字の平均候補数", False), ("sNov", "元の文章にない4文字組", False)]),
    legend='<div id="out" style="text-align:left;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px;min-height:80px;font-size:15px;line-height:1.9;white-space:pre-wrap;"></div><div id="probs" style="text-align:left;font-size:12px;color:var(--ink-2);margin-top:8px;"></div>',
    article=P("大規模言語モデルも本質は「これまでの文脈から、次の語の確率分布を出し、そこから1つ選ぶ」の繰り返しです。マルコフ連鎖はこれを<b>直前 n 文字だけを見て、出現回数を数える</b>という最小の方法で行います。n を増やすと文章らしくなり、増やしすぎると元の文章の丸写しになる——AIの「学習」と「暗記」の境目がここにあります。") + '''
<h2>しくみ：確率表を作って、サイコロを振る</h2>
''' + T([["1. 学習", "文章を先頭から読み、「直前 n 文字 → 次の1文字」の組み合わせを全部数える（確率表を作る）"], ["2. 生成", "最初の n 文字を決め、表を引いて次の文字を確率に従って選ぶ。それを繰り返す"], ["3. 温度", "確率の“とがり方”を調整。低温＝最も多い文字ばかり選ぶ（無難）、高温＝珍しい文字も選ぶ（創造的だが破綻）"]], ["ステップ", "内容"]) + '''
<p>1948年、クロード・シャノンは論文「通信の数学的理論」でこの方法を示し、英語の文字の統計だけから“英語らしい”文字列が生成できることを実演しました。現代の言語モデルは「直前 n 文字」を「数千語の文脈」に、「数える」を「ニューラルネットワークで推定する」に置き換えたものですが、「次を予測してサンプリングする」骨格は同じです。</p>
<h2>スライダーで見える「AIの性格」</h2>
''' + T([["n = 1〜2", "文字の並びはそれっぽいが意味不明。“言語らしさ”の最小単位"], ["n = 3〜4", "単語や言い回しが出てくる。短い文章では丸写しが混ざる"], ["n = 5〜6", "ほぼ元の文章の丸写し（過学習・暗記）。学習データが少ないとこうなる"], ["温度 0.2〜0.5", "同じフレーズを繰り返す。“無難で退屈なAI”"], ["温度 1.5〜2.0", "破綻した文字列。“幻覚（ハルシネーション）”の最小版"]], ["設定", "出てくる文章"]) + '''
<h2>「AIは丸暗記している」は本当か</h2>
<p>本ページで n を6にすると、生成文はほぼ学習文の切り貼りになります。学習データに対してモデルの記憶容量が大きすぎるときに起きる現象で、大規模モデルでも学習データに何度も出てくる文章（有名な詩・ライセンス文など）はそのまま出力されることがあります。一方、n=3で十分な量の文章を学習させると、元にない組み合わせ（右下の「元の文章にない4文字組」）が増え、「学習」と「暗記」の違いが数字で見えます。</p>
''',
    faqs=[("これはChatGPTと同じ？", "原理の骨格（次の文字の確率を推定し、サンプリングする）は同じですが、ChatGPTは数千億のパラメータを持つニューラルネットワークで文脈全体を読み、単語の意味の近さも扱います。本ページは「数える」だけの最小版で、その差が“賢さ”の差です。"),
          ("「次の文字の平均候補数」とは？", "確率表の各文脈で、次に来うる文字の種類数の平均です（パープレキシティに近い概念）。大きいほどモデルが迷っており、小さいほど文章が決まりきっています。"),
          ("貼り付けた文章は送信される？", "いいえ。学習も生成もすべてブラウザ内で行い、サーバーには何も送られません。")],
    rel=[("neural-play", "🧠", "ニューラルネットが学ぶ瞬間"), ("maze-ai", "🧩", "迷路をAIが解く"), ("catchcopy", "🎪", "うさんくさいキャッチコピー製造機"), ("ai-bunsho", "📝", "AI文章作成 時短シミュレーター")],
    js=r'''
  const S1='むかしむかし、あるところにおじいさんとおばあさんが住んでいました。おじいさんは山へしばかりに、おばあさんは川へせんたくに行きました。おばあさんが川でせんたくをしていると、川上から大きな桃がどんぶらこ、どんぶらこと流れてきました。おばあさんはその桃をひろいあげて、家に持ち帰りました。おじいさんが帰ってきて、二人で桃を切ろうとすると、桃の中から元気な男の子が生まれました。二人はその子を桃太郎と名づけて、大切に育てました。桃太郎はすくすくと育ち、たいそう力持ちになりました。ある日、桃太郎は鬼ヶ島へ鬼退治に行くことにしました。おばあさんはきびだんごを作って持たせてくれました。道の途中で、犬と猿ときじに出会い、きびだんごをあげて家来にしました。鬼ヶ島に着くと、鬼たちが酒を飲んで騒いでいました。桃太郎と家来たちは力を合わせて鬼と戦い、とうとう鬼を降参させました。桃太郎は鬼から宝物をもらい、村へ帰りました。おじいさんとおばあさんは大喜びで、それからみんなで幸せに暮らしました。';
  const S2='本日午前、市内の中心部で新しい商業施設がオープンした。開店前から多くの買い物客が列を作り、初日の来場者数は約三万人に達する見込みだという。施設の運営会社によると、地元の食材を使った飲食店や体験型の店舗が特徴で、週末には各種イベントも予定されている。市の担当者は「周辺地域の活性化につながることを期待している」と話した。一方、周辺道路では午前中から渋滞が発生し、警察が交通整理にあたった。運営会社は公共交通機関の利用を呼びかけている。今後は、駐車場の増設や臨時バスの運行も検討するという。専門家は「初年度の来場者数が今後の地域経済に与える影響は大きい」と分析している。市では来月、施設周辺の交通状況について調査を行う方針だ。';
  const out=$('out'), probs=$('probs'); let table=null, src='';
  function learn(){ src=$('src').value.replace(/\s+/g,''); const n=+$('order').value; table=new Map(); for(let i=0;i+n<src.length;i++){ const k=src.slice(i,i+n), c=src[i+n]; if(!table.has(k)) table.set(k,new Map()); const m=table.get(k); m.set(c,(m.get(c)||0)+1); }
    const chars=new Set(src).size; let cand=0; table.forEach(m=>cand+=m.size); setStat('sV', chars+'種類'); setStat('sCtx', table.size+'個'); setStat('sPerp', table.size?(cand/table.size).toFixed(2)+'種類':'—'); }
  function pick(m,temp){ const items=[...m.entries()]; const ws=items.map(([c,v])=>Math.pow(v,1/temp)); const tot=ws.reduce((a,b)=>a+b,0); let r=Math.random()*tot; for(let i=0;i<items.length;i++){ r-=ws[i]; if(r<=0) return items[i]; } return items[items.length-1]; }
  function generate(){ learn(); const n=+$('order').value, temp=+$('temp').value, L=+$('len').value; if(src.length<=n+2){ out.textContent='文章をもう少し長く入力してください。'; return; }
    const starts=[...table.keys()].filter(k=>/[。\n]/.test(src[src.indexOf(k)-1]||'。')); let cur=starts.length?starts[Math.random()*starts.length|0]:src.slice(0,n); let text=cur; let lastM=null;
    for(let i=0;i<L;i++){ const m=table.get(cur); if(!m) break; const [c]=pick(m,temp); text+=c; cur=text.slice(-n); lastM=m; }
    out.textContent=text;
    if(lastM){ const items=[...lastM.entries()].sort((a,b)=>b[1]-a[1]).slice(0,6); const tot=[...lastM.values()].reduce((a,b)=>a+b,0); probs.innerHTML='直前「<b>'+cur+'</b>」の次の文字の確率： '+items.map(([c,v])=>'「'+c+'」'+Math.round(v/tot*100)+'%').join('　'); }
    let novel=0, total=0; for(let i=0;i+4<=text.length;i++){ total++; if(!src.includes(text.slice(i,i+4))) novel++; } setStat('sNov', total?Math.round(novel/total*100)+'%':'—');
    setShare('マルコフ連鎖（記憶'+n+'文字・温度'+temp+'）に文章を学習させて生成✍️「'+text.slice(0,40)+'…」元の文章にない4文字組'+(total?Math.round(novel/total*100):0)+'%。ChatGPTの原理の最小版👇'); }
  $('gen').addEventListener('click',generate);
  $('sample1').addEventListener('click',()=>{ $('src').value=S1; generate(); }); $('sample2').addEventListener('click',()=>{ $('src').value=S2; generate(); }); $('sample3').addEventListener('click',()=>{ $('src').value=''; $('src').focus(); out.textContent=''; });
  ['order','temp'].forEach(id=>$(id).addEventListener('change',()=>{ if($('src').value) generate(); }));
  $('src').value=S1; generate();
''')

# ============================================================ 20 感染エージェント
sim(slug="kansen-agent", cat="health", emoji="🦠", score=73,
    title="感染はこう広がる SIRシミュレーター", model="エージェントベースSIRモデル（感受性・感染・回復）",
    model_note="Kermack & McKendrick (1927)。感染症数理モデルの原点。ワクチン・行動制限の効果予測に使用",
    title_tag="感染はこう広がる SIRシミュレーター｜マスク・ワクチン・外出制限でピークはどう変わる？",
    meta_desc="街を動き回る人々の間で感染が広がる様子をエージェントシミュレーションで再現。感染しやすさ・接触の多さ・ワクチン接種率・外出制限を変えると、感染のピークの高さと時期、最終的な感染者数がどう変わるかを体感できる無料ツール。集団免疫の閾値も解説。",
    og_title="感染はこう広がる SIRシミュレーター", og_desc="マスク・ワクチン・外出制限でピークはどう変わる？街の中の感染を再現。",
    card_desc="街を動く人々の間で感染が広がる。マスク・ワクチン・外出制限でピークの高さがどう変わるか。",
    lead="1人の感染者から、街の中でどう広がるのか。人々が動き回って接触し、一定期間で回復する——それだけのルールで、感染の「山」が生まれます。感染しやすさ・接触の多さ・ワクチン・外出制限を変えて、山の高さと時期がどう動くかを見てください。",
    canvas=canvas(640, 400),
    controls=slider("beta", "接触したときの感染しやすさ", 0.05, 1, 0.5, 0.05) + slider("move", "人の動き回り（接触の多さ）", 0, 3, 1.5, 0.1)
           + slider("vac", "ワクチン接種率（免疫あり）", 0, 90, 0, 5, "{v}%") + slider("stay", "外出しない人の割合", 0, 90, 0, 5, "{v}%") + slider("rec", "回復までの日数", 3, 21, 10, 1, "{v}日") + slider("sp", "再生速度", 1, 10, 4, 1, "×{v}"),
    buttons=btn("toggle", "⏸ 一時停止") + btn("reset", "リセット"),
    stats=stats([("sDay", "経過日数", False), ("sI", "いま感染中", True), ("sPeak", "ピーク（人数／日）", False), ("sTotal", "最終的な感染者", False)]),
    legend="灰＝未感染、赤＝感染中、青＝回復（免疫）、緑＝ワクチン接種済み。右のグラフ＝感染中の人数の推移。",
    article=P("感染の広がりを決めるのは<b>基本再生産数 R₀</b>＝1人の感染者が平均何人にうつすか。R₀が1を超えると流行し、1未満なら自然に収束します。ワクチンや外出制限は、感染の「山」を低く・遅くします。同じ最終感染者数でも、山を低くすれば医療が持ちこたえられる——これが「カーブをならす」の意味です。") + '''
<h2>SIRモデルの3つの状態</h2>
''' + T([["S（Susceptible）", "まだ感染していない人", "感染者と接触すると一定確率で I へ"], ["I（Infectious）", "感染中で、他人にうつす人", "一定日数で R へ"], ["R（Recovered）", "回復して免疫を持つ人（ワクチン接種者も含む）", "再感染しない"]], ["状態", "意味", "遷移"]) + '''
<p>1927年にカーマックとマッケンドリックが提案した、感染症数理モデルの原点です。本ページは方程式ではなく、1人1人が街を動き回って接触する「エージェントベース」で同じ現象を再現しています。動き回る速さ・接触時の感染確率・回復日数が、実効的な R₀ を決めます。</p>
<h2>集団免疫の閾値</h2>
''' + T([["R₀ = 1.5（季節性インフルエンザ級）", "33%"], ["R₀ = 2.5〜3", "60〜67%"], ["R₀ = 5〜6（新型コロナ変異株級）", "80〜83%"], ["R₀ = 12〜18（麻疹）", "92〜95%"]], ["R₀", "必要な免疫保有率（1 − 1/R₀）"]) + '''
<p>免疫を持つ人の割合が 1 − 1/R₀ を超えると、感染者が平均1人未満にしかうつせなくなり、流行は起きません。ワクチン接種率のスライダーを上げていくと、ある割合を境に「山が立たなくなる」ことが確認できます。麻疹のワクチン接種率が95%必要と言われるのはこの計算です。</p>
<h2>「動き回り」を減らす効果</h2>
<p>外出しない人の割合を増やすと、接触の総数が減り、山は低く・遅くなります。ただし全員が家にいるわけにいかないため、実際には「一定期間だけ接触を減らして山をならし、その間にワクチンを行き渡らせる」戦略が取られました。本ページでも、外出制限とワクチンを組み合わせると、山を立てずに収束させられます。</p>
''',
    faqs=[("最終的な感染者数が100%にならないのは？", "感染者が減ると接触相手も減るため、免疫のある人が増えた時点で流行は自然に終息します。R₀が2〜3でも、最終的な感染者は人口の8〜9割で止まるのがSIRモデルの結論です。"),
          ("マスクはどのスライダー？", "「接触したときの感染しやすさ」がマスクや換気に相当します。「人の動き回り」が外出頻度や人混みの多さ、「外出しない人」が在宅・隔離です。"),
          ("現実の予測はこれでできる？", "本ページは原理を示す簡略モデルです。実際の予測では、年齢構成・接触パターン・潜伏期間・無症状感染などを加えた大規模モデルが使われますが、SIRの骨格はそのまま生きています。")],
    rel=[("uwasa-kakusan", "🗣️", "噂が全員に届くまで"), ("lotka-volterra", "🐰", "キツネとウサギ 増減"), ("ryukou-curve", "📈", "流行はなぜ急に終わる？"), ("forest-fire", "🔥", "森林火災シミュレーター")],
    js=r'''
  const cv=$('cv'), x=cv.getContext('2d'), W=cv.width, H=cv.height, NP=300, AW=420;
  let ag, day, hist, run=true, peak=0, peakDay=0, tick=0;
  function reset(){ const vac=+$('vac').value/100, stay=+$('stay').value/100; ag=Array.from({length:NP},(_,i)=>({x:rnd(6,AW-6),y:rnd(6,H-6),vx:randn(),vy:randn(),s:Math.random()<vac?3:0,t:0,home:Math.random()<stay}));
    const inf=ag.filter(a=>a.s===0); for(let i=0;i<3&&i<inf.length;i++){ inf[i].s=1; } day=0; hist=[]; peak=0; peakDay=0; tick=0; draw(); }
  function step(){ const mv=+$('move').value, beta=+$('beta').value, rec=+$('rec').value; tick++;
    ag.forEach(a=>{ if(a.home) return; a.vx+=randn()*0.3; a.vy+=randn()*0.3; const sp=Math.hypot(a.vx,a.vy)||1; const cap=mv; if(sp>cap){ a.vx*=cap/sp; a.vy*=cap/sp; } a.x+=a.vx; a.y+=a.vy; if(a.x<6||a.x>AW-6) a.vx*=-1; if(a.y<6||a.y>H-6) a.vy*=-1; a.x=clamp(a.x,6,AW-6); a.y=clamp(a.y,6,H-6); });
    if(tick%10===0){ day++; for(const a of ag){ if(a.s===1){ a.t++; if(a.t>=rec) a.s=2; } }
      for(let i=0;i<NP;i++){ const a=ag[i]; if(a.s!==1) continue; for(let j=0;j<NP;j++){ const b=ag[j]; if(b.s!==0) continue; const d=Math.hypot(a.x-b.x,a.y-b.y); if(d<13&&Math.random()<beta*(a.home||b.home?0.2:1)) b.s=1; } }
      const I=ag.filter(a=>a.s===1).length; hist.push(I); if(I>peak){ peak=I; peakDay=day; } } }
  function draw(){ x.fillStyle='#0b1020'; x.fillRect(0,0,W,H); x.fillStyle='#111827'; x.fillRect(0,0,AW,H);
    ag.forEach(a=>{ x.fillStyle=['#6b7280','#ef4444','#3b82f6','#22c55e'][a.s]; x.beginPath(); x.arc(a.x,a.y,a.s===1?4:3,0,7); x.fill(); });
    const L=AW+16,PW=W-L-10,B=H-24,PH=B-30; x.fillStyle='rgba(255,255,255,.4)'; x.font='10px sans-serif'; x.fillText('感染中の人数', L, 16); x.fillText('日数 →', L+PW-36, H-8);
    x.strokeStyle='rgba(255,255,255,.08)'; for(let g=0;g<=4;g++){ const y=B-PH*g/4; x.beginPath(); x.moveTo(L,y); x.lineTo(L+PW,y); x.stroke(); }
    const n=Math.max(hist.length,60); x.fillStyle='rgba(239,68,68,.35)'; x.beginPath(); x.moveTo(L,B); hist.forEach((v,i)=>x.lineTo(L+i/n*PW, B-v/NP*PH)); x.lineTo(L+(hist.length-1)/n*PW,B); x.fill();
    x.strokeStyle='#ef4444'; x.lineWidth=2; x.beginPath(); hist.forEach((v,i)=>{ const X=L+i/n*PW, Y=B-v/NP*PH; i?x.lineTo(X,Y):x.moveTo(X,Y); }); x.stroke();
    const I=ag.filter(a=>a.s===1).length, R=ag.filter(a=>a.s===2).length, S=ag.filter(a=>a.s===0).length;
    setStat('sDay', day+'日'); setStat('sI', I+'人'); setStat('sPeak', peak+'人／'+peakDay+'日目'); setStat('sTotal', (I+R)+'人（'+Math.round((I+R)/NP*100)+'%）');
    if(I===0&&day>0){ x.fillStyle='#e5e7eb'; x.font='bold 14px sans-serif'; x.fillText('✅ 収束', L+8, 36); }
    setShare('感染しやすさ'+$('beta').value+'・ワクチン'+$('vac').value+'%・外出制限'+$('stay').value+'%でシミュ🦠 ピークは'+peakDay+'日目に'+peak+'人、最終感染者'+Math.round((I+R)/NP*100)+'%。ワクチンで山が消える瞬間を体感👇'); }
  function loop(){ if(run){ for(let i=0;i<+$('sp').value;i++) step(); } draw(); requestAnimationFrame(loop); }
  ['vac','stay'].forEach(id=>$(id).addEventListener('change',reset));
  $('toggle').addEventListener('click',()=>{ run=!run; $('toggle').textContent=run?'⏸ 一時停止':'▶ 再生'; });
  $('reset').addEventListener('click',reset);
  reset(); loop();
''')
