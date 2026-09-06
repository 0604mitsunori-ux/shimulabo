# -*- coding: utf-8 -*-
"""Fable20 C: 部屋が散らかる・ニューラルネット・遺伝的アルゴリズム・流体・地震共振"""
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

# ============================================================ 11 部屋はなぜ散らかる
sim(slug="heya-chirakaru", cat="home", emoji="🧦", score=67,
    title="部屋はなぜ勝手に散らかる？ エントロピーシミュレーター", model="統計力学（エントロピー＝配置の場合の数）",
    model_note="ボルツマンの S = k log W。「片付いた状態」は場合の数が圧倒的に少ない",
    title_tag="部屋はなぜ勝手に散らかる？エントロピーシミュレーター｜片付けが続かない物理的な理由",
    meta_desc="物を使って戻す、を繰り返すだけで部屋は散らかっていく——その理由を「片付いた配置の場合の数」で説明する無料シミュレーター。物の数・戻す確率・定位置の数を変えて、散らかりが進む速さと、片付けに必要な労力を体感。",
    og_title="部屋はなぜ勝手に散らかる？ エントロピーシミュレーター", og_desc="片付けが続かないのは意志ではなく物理。場合の数で説明。",
    card_desc="使って戻すだけで部屋は必ず散らかる。「片付いた配置」は場合の数が圧倒的に少ないから。",
    lead="片付けても片付けても、気づけば散らかっている。それは意志が弱いからではなく、「片付いた状態」が「散らかった状態」より圧倒的に<b>場合の数が少ない</b>から。物の数と戻す確率を変えて、散らかりが進む様子とその理由を見てください。",
    canvas=canvas(640, 360),
    controls=slider("n", "物の数", 10, 80, 30, 5, "{v}個") + slider("ret", "使ったあと定位置に戻す確率", 0, 100, 60, 5, "{v}%")
           + slider("use", "1日に使う物の数", 1, 20, 6, 1, "{v}個") + slider("sp", "再生速度", 1, 10, 4, 1, "×{v}"),
    buttons=btn("toggle", "⏸ 一時停止") + btn("reset", "リセット（全部片付ける）") + btn("clean", "🧹 30分片付け（10個戻す）"),
    stats=stats([("sDay", "経過日数", False), ("sOut", "定位置にない物", True), ("sEnt", "散らかり度（エントロピー）", False), ("sW", "配置の場合の数", False)]),
    legend="左＝部屋（白い枠＝各物の定位置、色の点＝物）。定位置から外れた物は赤。右のグラフ＝散らかり度の推移。",
    article=P("「片付いた配置」は1通り。物が30個あれば「散らかった配置」は<b>何兆通り以上</b>。ランダムに動く物は、ただ数が多いという理由だけで散らかった配置に落ち着きます。片付けは、この確率の坂を毎回登り直す作業です。") + '''
<h2>エントロピー＝場合の数</h2>
<p>物理学者ボルツマンは、エントロピー S を「その状態が実現する配置の数 W」の対数として定義しました（S = k log W）。物が n 個・置き場所が m か所あるとき、「全部が定位置」は1通りですが、「k 個が定位置から外れている」配置は C(n,k)×(m−1)ᵏ 通りもあります。n=30・m=30 なら、10個外れた配置は 10²⁰ 通りを超えます。</p>
''' + T([["0個（完璧に片付いている）", "1通り"], ["1個", "870通り"], ["5個", "約2.9×10¹²通り"], ["10個", "約1.5×10²¹通り"], ["15個", "約2.3×10²⁷通り"]], ["定位置にない物の数（30個・置き場30か所）", "配置の場合の数"]) + '''
<h2>「戻す確率」の閾値</h2>
<p>1日に使う物の数を u、戻す確率を r とすると、毎日 u(1−r) 個が定位置から外れ、外れている物は使われて戻る分だけ減ります。落ち着く先の「定位置にない物の数」はおおよそ n(1−r) 付近。<b>戻す確率が9割でも1割は常に散らかっている</b>ため、「使ったら戻す」だけでは完璧には保てません。定期的な片付け（外部からエネルギーを入れる）が必要な理由です。</p>
<h2>散らかりにくい部屋の設計</h2>
<p>熱力学的に考えると、対策は3つ。①物の数 n を減らす（場合の数が減る）、②定位置を「使う場所のすぐそば」にして戻す確率 r を上げる、③片付けを毎日少しずつ行う（エントロピーの山を小さいうちに削る）。「片付けが続かない」のは性格ではなく、この3つのどれかが欠けている設計問題です。</p>
''',
    faqs=[("散らかり度はどう計算している？", "定位置にない物の数 k から、配置の場合の数 W = C(n,k)×(n−1)ᵏ を求め、その対数（log₁₀ W）を散らかり度として表示しています。"),
          ("「30分片付け」ボタンは何をしている？", "定位置から外れた物を10個、定位置に戻します。系の外からエネルギーを入れてエントロピーを下げる操作にあたります。"),
          ("本当に物理学の話？", "比喩ではなく、統計力学の考え方そのものです。「場合の数が多い状態へ向かう」という原理は、コーヒーとミルクが混ざる現象と部屋が散らかる現象の両方に共通します。")],
    rel=[("diffusion", "🌫️", "拡散シミュレーター"), ("coffee-milk", "☕", "コーヒーにミルクを落とすと"), ("sandpile", "⛰️", "砂山崩しシミュレーター"), ("tatami-henkan", "🏠", "部屋の広さ換算シミュレーター")],
    js=r'''
  const cv=$('cv'), x=cv.getContext('2d'), W=cv.width, H=cv.height;
  let n, items, day, hist, run=true;
  function logC(n,k){ let s=0; for(let i=1;i<=k;i++) s+=Math.log10(n-k+i)-Math.log10(i); return s; }
  function logW(k){ return k?logC(n,k)+k*Math.log10(Math.max(1,n-1)):0; }
  function reset(){ n=+$('n').value; const cols=Math.ceil(Math.sqrt(n*1.6)); items=Array.from({length:n},(_,i)=>{ const c=i%cols, r=Math.floor(i/cols); const hx=30+c*(330/cols), hy=30+r*(300/Math.ceil(n/cols)); return {hx,hy,x:hx,y:hy,home:true,col:'hsl('+(i*47%360)+',70%,60%)'}; }); day=0; hist=[0]; draw(); }
  function step(){ day++; const u=+$('use').value, r=+$('ret').value/100; for(let k=0;k<u;k++){ const it=items[Math.random()*n|0]; if(Math.random()<r){ it.home=true; it.x=it.hx; it.y=it.hy; } else { it.home=false; it.x=30+Math.random()*330; it.y=30+Math.random()*300; } }
    hist.push(items.filter(i=>!i.home).length); if(hist.length>200) hist.shift(); }
  function draw(){ x.fillStyle='#0b1020'; x.fillRect(0,0,W,H); x.fillStyle='#111827'; x.fillRect(16,16,360,H-32);
    items.forEach(it=>{ x.strokeStyle='rgba(255,255,255,.18)'; x.strokeRect(it.hx-6,it.hy-6,12,12); });
    items.forEach(it=>{ x.fillStyle=it.home?it.col:'#ef4444'; x.beginPath(); x.arc(it.x,it.y,5,0,7); x.fill(); });
    const k=items.filter(i=>!i.home).length; const lw=logW(k), lwmax=logW(Math.round(n*0.6));
    const L=400,B=H-28,PW=W-L-12,PH=B-30; x.strokeStyle='rgba(255,255,255,.08)'; for(let g=0;g<=4;g++){ const y=B-PH*g/4; x.beginPath(); x.moveTo(L,y); x.lineTo(L+PW,y); x.stroke(); }
    x.fillStyle='rgba(255,255,255,.4)'; x.font='10px sans-serif'; x.fillText('定位置にない物の数', L, 24); x.fillText('日数 →', L+PW-40, H-8); x.fillText(n+'個', L-18, B-PH+4); x.fillText('0', L-10, B+3);
    x.strokeStyle='#f87171'; x.lineWidth=2; x.beginPath(); hist.forEach((v,i)=>{ const X=L+i/199*PW, Y=B-v/n*PH; i?x.lineTo(X,Y):x.moveTo(X,Y); }); x.stroke();
    setStat('sDay', day+'日'); setStat('sOut', k+'個 / '+n+'個'); setStat('sEnt', lw.toFixed(1)); setStat('sW', k?'10^'+lw.toFixed(0)+' 通り':'1通り');
    setShare('物'+n+'個・戻す確率'+$('ret').value+'%で'+day+'日→定位置にない物'+k+'個🧦 この散らかり方の配置は10^'+lw.toFixed(0)+'通り、片付いた配置は1通り。部屋が勝手に散らかる物理的理由👇'); }
  let f=0; function loop(){ if(run){ f++; if(f%Math.max(1,12-+$('sp').value)===0) step(); } draw(); requestAnimationFrame(loop); }
  $('n').addEventListener('change',reset);
  $('toggle').addEventListener('click',()=>{ run=!run; $('toggle').textContent=run?'⏸ 一時停止':'▶ 再生'; });
  $('reset').addEventListener('click',reset);
  $('clean').addEventListener('click',()=>{ let c=0; for(const it of items){ if(!it.home&&c<10){ it.home=true; it.x=it.hx; it.y=it.hy; c++; } } });
  reset(); loop();
''')

# ============================================================ 12 ニューラルネット
sim(slug="neural-play", cat="play", emoji="🧠", score=73,
    title="ニューラルネットが学ぶ瞬間 シミュレーター", model="多層パーセプトロン（誤差逆伝播法・確率的勾配降下法）",
    model_note="Rumelhart, Hinton & Williams (1986)。現代のAIすべての基礎",
    title_tag="ニューラルネットが学ぶ瞬間｜ブラウザで本物のAIを学習させ、境界線が育つ様子を見る",
    meta_desc="渦巻き・円・XORなどのデータを、本物のニューラルネットワーク（多層パーセプトロン）がブラウザ内で学習する様子をリアルタイム表示。隠れ層のニューロン数・学習率・データのノイズを変えると、AIが「分かる」までの過程がどう変わるかを体感できる無料ツール。",
    og_title="ニューラルネットが学ぶ瞬間 シミュレーター", og_desc="本物のAIをブラウザで学習させ、境界線が育つ様子を見る。",
    card_desc="渦巻きや円のデータを本物のニューラルネットが学習。境界線が育っていく瞬間をリアルタイムで。",
    lead="ChatGPTも画像認識も、根っこは同じ「ニューラルネットワーク」。ここでは小さな本物のネットワークをブラウザ内で学習させ、赤と青を分ける境界線が少しずつ育っていく様子を見られます。ニューロンの数や学習率を変えると、賢くなる速さも、行き詰まり方も変わります。",
    canvas=canvas(640, 400),
    controls=select("data", "学習させるデータ", [("spiral", "渦巻き（難しい）"), ("circle", "円（中くらい）"), ("xor", "XOR・市松（中くらい）"), ("gauss", "2つの塊（かんたん）")])
           + slider("hid", "隠れ層のニューロン数", 2, 32, 8, 1, "{v}個") + slider("layers", "隠れ層の数", 1, 3, 2, 1, "{v}層")
           + slider("lr", "学習率", 0.01, 0.5, 0.1, 0.01) + slider("noise", "データのノイズ", 0, 0.5, 0.1, 0.05) + slider("sp", "再生速度", 1, 10, 5, 1, "×{v}"),
    buttons=btn("toggle", "⏸ 一時停止") + btn("reset", "リセット（初期化して学び直す）"),
    stats=stats([("sEp", "学習回数（エポック）", False), ("sAcc", "正解率", True), ("sLoss", "誤差（損失）", False), ("sParam", "パラメータ数", False)]),
    legend="点＝学習データ（赤・青の2種類）。背景色＝ネットワークの現在の判断（濃いほど自信あり）。右＝各ニューロンが担当している“見え方”。",
    article=P("ニューラルネットワークは、ランダムな重みから始めて「間違えたら、間違いが減る方向に重みを少し動かす」を何万回も繰り返すだけで、渦巻きのような複雑な境界を自力で見つけます。<b>賢さは設計者が教えたのではなく、データと誤差から“育った”</b>ものです。") + '''
<h2>この画面の中で起きていること</h2>
''' + T([["1. 順伝播", "入力（x, y座標）に重みを掛けて足し、活性化関数（tanh）を通す。これを層の数だけ繰り返して「赤か青か」を出力"], ["2. 誤差の計算", "出力と正解のずれ（交差エントロピー）を計算"], ["3. 誤差逆伝播", "各重みが誤差にどれだけ影響したか（勾配）を出力側から逆にたどって計算"], ["4. 更新", "勾配と逆方向に、学習率の分だけ重みを動かす"]], ["ステップ", "内容"]) + '''
<p>1986年にラメルハート、ヒントン、ウィリアムズが広めたこの「誤差逆伝播法」は、現在のあらゆる深層学習の中核です。本ページのネットワークは数百パラメータですが、ChatGPTのようなモデルは同じ原理を数千億〜数兆パラメータで動かしています。</p>
<h2>スライダーで分かる「AIの性格」</h2>
''' + T([["ニューロンを減らす（2〜3個）", "直線に近い境界しか引けず、渦巻きは学べない（表現力不足）"], ["ニューロンを増やす（16〜32個）", "複雑な境界を学べるが、ノイズまで覚えてしまうことがある（過学習）"], ["学習率を上げすぎる", "重みが振動して正解率が上下に暴れる、または発散する"], ["学習率を下げすぎる", "正しい方向に進むが、いつまでも到達しない"], ["層を増やす", "少ないニューロンでも複雑な形を表現できる＝“深層”学習の利点"]], ["操作", "起きること"]) + '''
<h2>右側の小さな図の見方</h2>
<p>右側は最初の隠れ層の各ニューロンが「入力空間のどこで発火するか」を示しています。1つ1つは単純な直線的なパターンですが、それらを重ね合わせることで、出力層は渦巻きのような複雑な形を作ります。ニューラルネットワークが「特徴を分担して覚える」様子です。</p>
''',
    faqs=[("これは本当にAI？ 見せかけではない？", "本物です。JavaScriptで多層パーセプトロンを実装し、誤差逆伝播で毎フレーム重みを更新しています。ライブラリも通信も使っていません。ページのソースコードを見れば数十行の学習ループが確認できます。"),
          ("渦巻きが学べないときは？", "ニューロン数を16以上・層を2〜3にして、学習率0.05〜0.1でしばらく待ってください。乱数の初期値によっては局所解にはまるので、リセットして再挑戦するのも本物の機械学習と同じ流儀です。"),
          ("正解率100%にならないのは？", "ノイズがあるとデータ自体に矛盾（赤の領域に混ざった青点）があるため、100%は原理的に不可能です。ノイズを0にすれば、十分なニューロンで100%近くに達します。")],
    rel=[("markov-bunsho", "✍️", "AIはこうやって文章を作る"), ("ga-route", "🧬", "遺伝的アルゴリズムで最短ルート"), ("maze-ai", "🧩", "迷路をAIが解く"), ("ai-inyou", "🤖", "AI被引用ポテンシャル診断")],
    js=r'''
  const cv=$('cv'), x=cv.getContext('2d'), W=cv.width, H=cv.height, S=400;
  let data, net, ep, run=true, loss=0, acc=0;
  function genData(){ const t=$('data').value, nz=+$('noise').value; data=[];
    for(let i=0;i<200;i++){ const c=i%2; let px,py; if(t==='spiral'){ const r=i/200*0.9+0.1, a=i/200*3*Math.PI+c*Math.PI; px=r*Math.sin(a); py=r*Math.cos(a); }
      else if(t==='circle'){ const r=c?rnd(0,0.45):rnd(0.6,0.95), a=rnd(0,7); px=r*Math.cos(a); py=r*Math.sin(a); }
      else if(t==='xor'){ px=rnd(-1,1); py=rnd(-1,1); const cc=(px>0)^(py>0); data.push({x:px+randn()*nz*0.5,y:py+randn()*nz*0.5,c:cc?1:0}); continue; }
      else { px=(c?0.5:-0.5)+randn()*0.3; py=(c?0.5:-0.5)+randn()*0.3; }
      data.push({x:px+randn()*nz*0.5, y:py+randn()*nz*0.5, c}); } }
  function mkNet(){ const h=+$('hid').value, L=+$('layers').value; const sizes=[2]; for(let i=0;i<L;i++) sizes.push(h); sizes.push(1);
    net={sizes, W:[], b:[]}; for(let l=0;l<sizes.length-1;l++){ const sc=Math.sqrt(2/sizes[l]); net.W.push(Array.from({length:sizes[l+1]},()=>Array.from({length:sizes[l]},()=>randn()*sc))); net.b.push(new Array(sizes[l+1]).fill(0)); } }
  function forward(px,py){ const acts=[[px,py]]; let a=[px,py]; for(let l=0;l<net.W.length;l++){ const last=l===net.W.length-1; const o=net.W[l].map((w,j)=>{ let s=net.b[l][j]; for(let i=0;i<w.length;i++) s+=w[i]*a[i]; return last?1/(1+Math.exp(-s)):Math.tanh(s); }); acts.push(o); a=o; } return acts; }
  function train(){ const lr=+$('lr').value; let L=0, correct=0; const idx=data.map((_,i)=>i).sort(()=>Math.random()-0.5);
    for(const i of idx){ const d=data[i]; const acts=forward(d.x,d.y); const out=acts[acts.length-1][0]; L+=-(d.c*Math.log(out+1e-9)+(1-d.c)*Math.log(1-out+1e-9)); if((out>0.5)===(d.c===1)) correct++;
      let delta=[out-d.c]; for(let l=net.W.length-1;l>=0;l--){ const prev=acts[l]; const nd=new Array(prev.length).fill(0);
        for(let j=0;j<net.W[l].length;j++){ for(let k=0;k<prev.length;k++){ nd[k]+=net.W[l][j][k]*delta[j]; net.W[l][j][k]-=lr*delta[j]*prev[k]; } net.b[l][j]-=lr*delta[j]; }
        delta=nd.map((v,k)=>v*(1-prev[k]*prev[k])); } }
    loss=L/data.length; acc=correct/data.length; ep++; }
  function reset(){ genData(); mkNet(); ep=0; loss=0; acc=0; draw(); }
  function draw(){ x.fillStyle='#0b1020'; x.fillRect(0,0,W,H);
    const G=40, cs=S/G; for(let i=0;i<G;i++) for(let j=0;j<G;j++){ const px=(i+0.5)/G*2-1, py=1-(j+0.5)/G*2; const o=forward(px,py); const v=o[o.length-1][0]; const a=Math.abs(v-0.5)*2; x.fillStyle=v>0.5?'rgba(59,130,246,'+(0.15+a*0.5)+')':'rgba(239,68,68,'+(0.15+a*0.5)+')'; x.fillRect(i*cs,j*cs,cs+0.5,cs+0.5); }
    data.forEach(d=>{ const X=(d.x+1)/2*S, Y=(1-d.y)/2*S; x.fillStyle=d.c?'#3b82f6':'#ef4444'; x.strokeStyle='#fff'; x.lineWidth=1; x.beginPath(); x.arc(X,Y,4,0,7); x.fill(); x.stroke(); });
    // hidden units
    const h=net.sizes[1], cols=4, sz=48, ox=S+16; x.fillStyle='rgba(255,255,255,.5)'; x.font='10px sans-serif'; x.fillText('隠れ層1の各ニューロン', ox, 14);
    for(let u=0;u<Math.min(h,24);u++){ const bx=ox+(u%cols)*(sz+6), by=22+Math.floor(u/cols)*(sz+6); if(by+sz>H) break; const g=10, c2=sz/g; for(let i=0;i<g;i++) for(let j=0;j<g;j++){ const px=(i+0.5)/g*2-1, py=1-(j+0.5)/g*2; let s=net.b[0][u]; s+=net.W[0][u][0]*px+net.W[0][u][1]*py; const v=Math.tanh(s); x.fillStyle=v>0?'rgba(59,130,246,'+Math.abs(v)+')':'rgba(239,68,68,'+Math.abs(v)+')'; x.fillRect(bx+i*c2,by+j*c2,c2+0.5,c2+0.5); } x.strokeStyle='rgba(255,255,255,.15)'; x.strokeRect(bx,by,sz,sz); }
    let np=0; net.W.forEach((w,l)=>{ np+=w.length*w[0].length+net.b[l].length; });
    setStat('sEp', ep); setStat('sAcc', Math.round(acc*100)+'%'); setStat('sLoss', loss.toFixed(3)); setStat('sParam', np+'個');
    const dn={spiral:'渦巻き',circle:'円',xor:'XOR',gauss:'2つの塊'}[$('data').value];
    setShare('ニューラルネット（'+$('layers').value+'層×'+$('hid').value+'ニューロン・'+np+'パラメータ）が'+dn+'を'+ep+'回学習→正解率'+Math.round(acc*100)+'%🧠 AIが「分かる」瞬間をブラウザで👇'); }
  function loop(){ if(run){ const n=+$('sp').value; for(let i=0;i<n;i++) train(); } draw(); requestAnimationFrame(loop); }
  ['data','hid','layers','noise'].forEach(id=>$(id).addEventListener('change',reset));
  $('toggle').addEventListener('click',()=>{ run=!run; $('toggle').textContent=run?'⏸ 一時停止':'▶ 再生'; });
  $('reset').addEventListener('click',reset);
  reset(); loop();
''')

# ============================================================ 13 遺伝的アルゴリズム
sim(slug="ga-route", cat="play", emoji="🧬", score=70,
    title="遺伝的アルゴリズムで最短ルート シミュレーター", model="遺伝的アルゴリズム（順序交叉・突然変異・エリート保存）による巡回セールスマン問題",
    model_note="Holland (1975)。物流・配送ルート・回路設計で使われる進化計算",
    title_tag="遺伝的アルゴリズムで最短ルート｜配達の巡回ルートが“進化”で短くなる様子を見る",
    meta_desc="地図上に配達先を置くと、遺伝的アルゴリズム（交叉・突然変異・淘汰）が世代を重ねて最短の巡回ルートを見つけていく過程をアニメで表示する無料シミュレーター。巡回セールスマン問題の難しさと、生物の進化を真似た解き方を体感。",
    og_title="遺伝的アルゴリズムで最短ルート", og_desc="配達ルートが“進化”で短くなる。巡回セールスマン問題を体感。",
    card_desc="配達先をクリックで置くと、進化計算が世代を重ねてルートを短くしていく。生物の進化を真似た最適化。",
    lead="配達先が20か所あるとき、全部を回る順番は2兆通り以上。総当たりでは無理な問題を、「良いルート同士を掛け合わせ、たまに突然変異させ、悪いものを淘汰する」——生物の進化を真似た方法で解いていきます。地図をクリックして配達先を増やしてみてください。",
    canvas=canvas(640, 400),
    controls=slider("n", "配達先の数（ランダム配置）", 5, 60, 20, 1, "{v}か所") + slider("pop", "1世代のルート数（個体数）", 20, 300, 100, 10, "{v}本")
           + slider("mut", "突然変異率", 0.01, 0.5, 0.1, 0.01) + slider("sp", "再生速度", 1, 10, 5, 1, "×{v}"),
    buttons=btn("toggle", "⏸ 一時停止") + btn("reset", "配置し直す") + btn("clear", "全消去（クリックで自由に置く）"),
    stats=stats([("sGen", "世代", False), ("sBest", "最短ルートの長さ", True), ("sImp", "最初の世代からの短縮", False), ("sComb", "順番の組み合わせ数", False)]),
    legend="点＝配達先（クリック／タップで追加）。太い線＝現在の最良ルート。薄い線＝その世代の他のルート候補。",
    article=P("配達先が n か所のとき、回る順番は (n−1)!/2 通り。20か所で約6×10¹⁶通り、30か所なら宇宙の年齢の間に総当たりしても終わりません。遺伝的アルゴリズムは<b>最良解の保証はないが、実用的に十分良い解を短時間で見つける</b>方法で、実際の配送計画に使われています。") + '''
<h2>進化の4ステップ</h2>
''' + T([["① 評価", "各ルートの総距離を計算（短いほど“適応度”が高い）"], ["② 選択", "トーナメント選択：ランダムに数本選び、いちばん短いものを親にする"], ["③ 交叉", "順序交叉（OX）：親Aのルートの一部を切り取り、残りを親Bの順で埋める"], ["④ 突然変異", "一定確率でルートの一部を反転（2-opt）して、新しい形を試す"]], ["ステップ", "内容"]) + '''
<p>さらに「エリート保存」として、各世代の最良ルートはそのまま次世代に残します。これで最良解が悪化することはなく、世代を重ねるほど単調に改善します。</p>
<h2>巡回セールスマン問題（TSP）</h2>
<p>「すべての都市を1回ずつ訪れて戻る最短経路」を求めるこの問題は、計算量理論で<b>NP困難</b>に分類される代表的な難問です。厳密解を求める最良のアルゴリズムでも都市数が増えると急激に時間がかかるため、実務では遺伝的アルゴリズム・焼きなまし法・アントコロニー最適化などの「近似アルゴリズム」が使われます。宅配便の配送順、基板への部品実装順、望遠鏡の観測順序などが応用例です。</p>
<h2>観察のコツ</h2>
<p>最初の数世代で急激に短くなり、その後は「あと一歩」がなかなか縮まらない——これは最適化全般に共通する形です。突然変異率を上げると停滞から抜け出しやすい反面、良い解が壊れやすくなります。個体数を増やすと安定しますが、1世代の計算が重くなります。</p>
''',
    faqs=[("最短が保証される？", "いいえ。遺伝的アルゴリズムは近似解法で、「これ以上短いルートがない」ことは証明できません。ただし20か所程度なら、経験的にほぼ最適解に到達します。"),
          ("線が交差しているルートは最適？", "交差があるルートは、その2本を付け替えれば必ず短くなるため最適ではありません。突然変異（2-opt）はまさにこの交差をほどく操作です。"),
          ("現実の配送はこれで決めている？", "基本は同じ発想ですが、実務では配達時間帯の指定・車両の積載量・交通状況なども制約に加えた「配送計画問題（VRP）」として解きます。")],
    rel=[("neural-play", "🧠", "ニューラルネットが学ぶ瞬間"), ("maze-ai", "🧩", "迷路をAIが解く"), ("shinka-sim", "🦎", "進化シミュレーター"), ("sort-visualizer", "📊", "ソートアルゴリズム可視化")],
    js=r'''
  const cv=$('cv'), x=cv.getContext('2d'), W=cv.width, H=cv.height;
  let pts=[], pop=[], gen=0, best=null, first=null, run=true;
  const dist=(a,b)=>Math.hypot(pts[a].x-pts[b].x, pts[a].y-pts[b].y);
  const len=(r)=>{ let s=0; for(let i=0;i<r.length;i++) s+=dist(r[i],r[(i+1)%r.length]); return s; };
  function randomPts(){ const n=+$('n').value; pts=Array.from({length:n},()=>({x:rnd(30,W-30),y:rnd(30,H-30)})); }
  function initPop(){ const n=pts.length, P=+$('pop').value; pop=[]; for(let i=0;i<P;i++){ const r=[...Array(n).keys()].sort(()=>Math.random()-0.5); pop.push(r); } gen=0; best=null; first=null; evalPop(); first=best?len(best):0; }
  function evalPop(){ pop.sort((a,b)=>len(a)-len(b)); if(!best||len(pop[0])<len(best)) best=pop[0].slice(); }
  function tourn(){ let b=null; for(let i=0;i<4;i++){ const c=pop[Math.random()*pop.length|0]; if(!b||len(c)<len(b)) b=c; } return b; }
  function ox(a,b){ const n=a.length; let i=Math.random()*n|0, j=Math.random()*n|0; if(i>j)[i,j]=[j,i]; const child=new Array(n).fill(-1); for(let k=i;k<=j;k++) child[k]=a[k]; const used=new Set(child); let p=0; for(let k=0;k<n;k++){ if(child[k]===-1){ while(used.has(b[p])) p++; child[k]=b[p]; used.add(b[p]); } } return child; }
  function mutate(r){ if(Math.random()<+$('mut').value){ let i=Math.random()*r.length|0, j=Math.random()*r.length|0; if(i>j)[i,j]=[j,i]; const seg=r.slice(i,j+1).reverse(); r.splice(i,seg.length,...seg); } }
  function generation(){ if(pts.length<4) return; const P=pop.length; const nxt=[best.slice()]; while(nxt.length<P){ const c=ox(tourn(),tourn()); mutate(c); nxt.push(c); } pop=nxt; evalPop(); gen++; }
  function fact(n){ let s=0; for(let i=2;i<=n;i++) s+=Math.log10(i); return s; }
  function draw(){ x.fillStyle='#0b1020'; x.fillRect(0,0,W,H);
    if(pts.length>=4){ x.strokeStyle='rgba(148,163,184,.08)'; x.lineWidth=1; for(let k=1;k<Math.min(pop.length,12);k++){ const r=pop[k]; x.beginPath(); r.forEach((i,q)=>{ q?x.lineTo(pts[i].x,pts[i].y):x.moveTo(pts[i].x,pts[i].y); }); x.closePath(); x.stroke(); }
      x.strokeStyle='#4ade80'; x.lineWidth=2.5; x.beginPath(); best.forEach((i,q)=>{ q?x.lineTo(pts[i].x,pts[i].y):x.moveTo(pts[i].x,pts[i].y); }); x.closePath(); x.stroke(); }
    pts.forEach((p,i)=>{ x.fillStyle=i===0?'#fbbf24':'#f8fafc'; x.beginPath(); x.arc(p.x,p.y,i===0?7:5,0,7); x.fill(); });
    if(pts.length<4){ x.fillStyle='#e5e7eb'; x.font='14px sans-serif'; x.fillText('クリック／タップで配達先を4か所以上置いてください', 150, H/2); }
    x.fillStyle='rgba(255,255,255,.5)'; x.font='11px sans-serif'; x.fillText('黄＝出発地点（配送センター）', 8, H-8);
    const bl=best?len(best):0; const n=pts.length; const comb=n>2?fact(n-1)-Math.log10(2):0;
    setStat('sGen', gen); setStat('sBest', Math.round(bl)+' px'); setStat('sImp', first?'−'+Math.round((1-bl/first)*100)+'%':'—'); setStat('sComb', n>2?'10^'+comb.toFixed(0)+' 通り':'—');
    setShare('配達先'+n+'か所（順番は10^'+comb.toFixed(0)+'通り）を遺伝的アルゴリズムで'+gen+'世代進化→ルート'+(first?Math.round((1-bl/first)*100):0)+'%短縮🧬 生物の進化を真似た最適化を体感👇'); }
  function loop(){ if(run&&pts.length>=4){ const k=+$('sp').value; for(let i=0;i<k;i++) generation(); } draw(); requestAnimationFrame(loop); }
  cv.addEventListener('pointerdown',(e)=>{ const [px,py]=cpos(cv,e); pts.push({x:px,y:py}); if(pts.length>=4) initPop(); });
  ['n','pop'].forEach(id=>$(id).addEventListener('change',()=>{ randomPts(); initPop(); }));
  $('toggle').addEventListener('click',()=>{ run=!run; $('toggle').textContent=run?'⏸ 一時停止':'▶ 再生'; });
  $('reset').addEventListener('click',()=>{ randomPts(); initPop(); });
  $('clear').addEventListener('click',()=>{ pts=[]; pop=[]; best=null; gen=0; });
  randomPts(); initPop(); loop();
''')

# ============================================================ 14 コーヒーにミルク（流体）
sim(slug="coffee-milk", cat="wonder", emoji="☕", score=72,
    title="コーヒーにミルクを落とすと 流体シミュレーター", model="ナビエ＝ストークス方程式の数値解法（Stable Fluids）",
    model_note="Stam (1999, SIGGRAPH)。映画のVFX・ゲームの流体表現の標準手法",
    title_tag="コーヒーにミルクを落とすと｜ブラウザで動く流体シミュレーター（ナビエ＝ストークス方程式）",
    meta_desc="カップにミルクを落とし、指でかき混ぜると渦が生まれて混ざっていく——流体の運動方程式（ナビエ＝ストークス）をブラウザで数値的に解く無料シミュレーター。粘り気（粘性）や拡散を変えて、コーヒー・はちみつ・水の違いを体感。",
    og_title="コーヒーにミルクを落とすと 流体シミュレーター", og_desc="指でかき混ぜて渦を作る。流体の方程式をブラウザで解く。",
    card_desc="カップにミルクを落として指でかき混ぜると、本物の流体方程式で渦が生まれ混ざっていく。",
    lead="コーヒーにミルクを一滴。スプーンでひと混ぜすると、渦を巻きながら混ざっていく。あの動きを、流体の運動方程式をブラウザで解いて再現しました。画面をなぞってかき混ぜ、粘り気を変えて、水・コーヒー・はちみつの違いを見てください。",
    canvas=canvas(400, 400),
    controls=slider("visc", "粘り気（粘性）", 0, 10, 1, 1) + slider("diff", "ミルクの広がりやすさ（拡散）", 0, 10, 2, 1) + slider("force", "かき混ぜる強さ", 1, 10, 5, 1) + select("liq", "液体プリセット", [("coffee", "コーヒー"), ("water", "水"), ("honey", "はちみつ"), ("ink", "水にインク")]),
    buttons=btn("drop", "🥛 ミルクを落とす") + btn("stir", "🥄 スプーンでひと混ぜ") + btn("reset", "新しいカップ"),
    stats=stats([("sMix", "混ざり具合", True), ("sVort", "渦の強さ", False), ("sT", "経過", False)]),
    legend="画面をドラッグ／スワイプするとかき混ぜられます。粘り気が高いほど渦がすぐ消え、拡散が高いほど境界がぼやけます。",
    article=P("流体の動きは<b>ナビエ＝ストークス方程式</b>という1本の式で記述できます。ただしこの式は解析的には解けず（解の存在自体がミレニアム懸賞問題）、コンピュータで格子に分けて近似します。本ページはその近似計算を、1秒に数十回、ブラウザの中で行っています。") + '''
<h2>この画面で解いている式</h2>
''' + N("∂u/∂t = −(u·∇)u + ν∇²u + f<br>移流（流れが流れを運ぶ）＋ 粘性（速度がならされる）＋ 外力（あなたの指）") + '''
<p>本ページは Jos Stam が1999年に発表した「Stable Fluids」法を用いています。①外力を加える、②粘性で速度を拡散させる、③流れに沿って速度と色を運ぶ（移流）、④体積が保存するよう圧力を補正する（射影）——の4段階を毎フレーム繰り返します。この手法は安定性が高く、映画のVFXやゲームの煙・水の表現の基礎になっています。</p>
<h2>粘り気で何が変わるか</h2>
''' + T([["水", "ほぼ0", "渦が長く残り、細かい乱れが生まれる"], ["コーヒー", "水と同程度〜やや高い", "ミルクの筋が渦を巻きながらゆっくり混ざる"], ["はちみつ", "水の約1万倍", "渦はすぐ消え、指の跡がそのまま残る（層流）"]], ["液体", "粘性（水との比較）", "見え方"]) + '''
<p>「渦が生まれるか、すぐ消えるか」を決めるのは<b>レイノルズ数</b>（慣性力÷粘性力）です。同じかき混ぜ方でも、粘性が高いとレイノルズ数が小さく、流れは整然とした層流に。小さいと乱流になり、渦が次々に生まれます。</p>
<h2>なぜ混ぜると速く混ざるのか</h2>
<p>ミルクを落として放置すると、分子の拡散だけで混ざるため数分〜十数分かかります。かき混ぜると、渦がミルクの塊を細く長く引き伸ばし、コーヒーとの境界面積を何百倍にも増やします。境界が増えた分だけ拡散が一気に進む——「混ぜる」とは、拡散の仕事を減らす操作なのです。</p>
''',
    faqs=[("画面がカクつく場合は？", "計算量が大きいため、古いスマホでは重くなることがあります。粘り気を上げる（計算が安定する）か、他のタブを閉じてお試しください。"),
          ("本当のコーヒーと違うところは？", "本物は3次元で、温度差による対流やミルクの密度差も働きます。本ページは2次元の非圧縮流体として計算しています。それでも渦の巻き方や引き伸ばされ方は、本物とよく似ます。"),
          ("「混ざり具合」はどう計算している？", "画面全体でミルクの濃度の“ばらつき”（標準偏差）を測り、完全に均一な状態を100%としています。")],
    rel=[("diffusion", "🌫️", "拡散シミュレーター"), ("heya-chirakaru", "🧦", "部屋はなぜ勝手に散らかる？"), ("ripple", "💧", "波紋シミュレーター"), ("tsunami-kishi", "🌊", "津波はなぜ岸で高くなる？")],
    js=r'''
  const cv=$('cv'), x=cv.getContext('2d'); const N=64, SZ=(N+2)*(N+2); const IX=(i,j)=>i+(N+2)*j;
  let u,v,u0,v0,d,d0,t=0, vort=0; const img=x.createImageData(N,N);
  function alloc(){ u=new Float32Array(SZ); v=new Float32Array(SZ); u0=new Float32Array(SZ); v0=new Float32Array(SZ); d=new Float32Array(SZ); d0=new Float32Array(SZ); t=0; }
  function setBnd(b,xa){ for(let i=1;i<=N;i++){ xa[IX(0,i)]=b===1?-xa[IX(1,i)]:xa[IX(1,i)]; xa[IX(N+1,i)]=b===1?-xa[IX(N,i)]:xa[IX(N,i)]; xa[IX(i,0)]=b===2?-xa[IX(i,1)]:xa[IX(i,1)]; xa[IX(i,N+1)]=b===2?-xa[IX(i,N)]:xa[IX(i,N)]; }
    xa[IX(0,0)]=0.5*(xa[IX(1,0)]+xa[IX(0,1)]); xa[IX(0,N+1)]=0.5*(xa[IX(1,N+1)]+xa[IX(0,N)]); xa[IX(N+1,0)]=0.5*(xa[IX(N,0)]+xa[IX(N+1,1)]); xa[IX(N+1,N+1)]=0.5*(xa[IX(N,N+1)]+xa[IX(N+1,N)]); }
  function linSolve(b,xa,x0,a,c){ for(let k=0;k<12;k++){ for(let j=1;j<=N;j++) for(let i=1;i<=N;i++){ xa[IX(i,j)]=(x0[IX(i,j)]+a*(xa[IX(i-1,j)]+xa[IX(i+1,j)]+xa[IX(i,j-1)]+xa[IX(i,j+1)]))/c; } setBnd(b,xa); } }
  function diffuse(b,xa,x0,df,dt){ const a=dt*df*N*N; if(a===0){ xa.set(x0); setBnd(b,xa); return; } linSolve(b,xa,x0,a,1+4*a); }
  function advect(b,dd,d0_,uu,vv,dt){ const dt0=dt*N; for(let j=1;j<=N;j++) for(let i=1;i<=N;i++){ let xx=i-dt0*uu[IX(i,j)], yy=j-dt0*vv[IX(i,j)]; xx=clamp(xx,0.5,N+0.5); yy=clamp(yy,0.5,N+0.5); const i0=xx|0,i1=i0+1,j0=yy|0,j1=j0+1; const s1=xx-i0,s0=1-s1,t1=yy-j0,t0=1-t1; dd[IX(i,j)]=s0*(t0*d0_[IX(i0,j0)]+t1*d0_[IX(i0,j1)])+s1*(t0*d0_[IX(i1,j0)]+t1*d0_[IX(i1,j1)]); } setBnd(b,dd); }
  function project(uu,vv,p,div){ for(let j=1;j<=N;j++) for(let i=1;i<=N;i++){ div[IX(i,j)]=-0.5*(uu[IX(i+1,j)]-uu[IX(i-1,j)]+vv[IX(i,j+1)]-vv[IX(i,j-1)])/N; p[IX(i,j)]=0; } setBnd(0,div); setBnd(0,p); linSolve(0,p,div,1,4);
    for(let j=1;j<=N;j++) for(let i=1;i<=N;i++){ uu[IX(i,j)]-=0.5*N*(p[IX(i+1,j)]-p[IX(i-1,j)]); vv[IX(i,j)]-=0.5*N*(p[IX(i,j+1)]-p[IX(i,j-1)]); } setBnd(1,uu); setBnd(2,vv); }
  function step(){ const dt=0.1, visc=+$('visc').value*0.00002, diff=+$('diff').value*0.00002;
    let tmp; diffuse(1,u0,u,visc,dt); diffuse(2,v0,v,visc,dt); project(u0,v0,u,v); advect(1,u,u0,u0,v0,dt); advect(2,v,v0,u0,v0,dt); project(u,v,u0,v0);
    diffuse(0,d0,d,diff,dt); advect(0,d,d0,u,v,dt); t+=dt; }
  function drop(cx,cy,r){ for(let j=1;j<=N;j++) for(let i=1;i<=N;i++){ if((i-cx)**2+(j-cy)**2<r*r) d[IX(i,j)]=1; } }
  function stir(){ const f=+$('force').value*0.6; for(let j=1;j<=N;j++) for(let i=1;i<=N;i++){ const dx=i-N/2, dy=j-N/2, r=Math.hypot(dx,dy); if(r>4&&r<N/2-2){ u[IX(i,j)]+=-dy/r*f*Math.exp(-r/22); v[IX(i,j)]+=dx/r*f*Math.exp(-r/22); } } }
  function preset(){ const p=$('liq').value; const set=(id,val)=>{ $(id).value=val; $(id).dispatchEvent(new Event('input')); }; if(p==='water'){ set('visc',0); set('diff',1); } else if(p==='honey'){ set('visc',10); set('diff',0); } else if(p==='ink'){ set('visc',0); set('diff',4); } else { set('visc',1); set('diff',2); } }
  function draw(){ const p=$('liq').value; const bg=p==='water'||p==='ink'?[210,230,245]:p==='honey'?[205,140,30]:[70,38,20]; const fg=p==='ink'?[20,30,120]:[250,246,235];
    let sum=0,sum2=0,vs=0; for(let j=1;j<=N;j++) for(let i=1;i<=N;i++){ const c=clamp(d[IX(i,j)],0,1); sum+=c; sum2+=c*c; const k=((j-1)*N+(i-1))*4; img.data[k]=bg[0]+(fg[0]-bg[0])*c; img.data[k+1]=bg[1]+(fg[1]-bg[1])*c; img.data[k+2]=bg[2]+(fg[2]-bg[2])*c; img.data[k+3]=255;
      vs+=Math.abs((v[IX(i+1,j)]-v[IX(i-1,j)])-(u[IX(i,j+1)]-u[IX(i,j-1)])); }
    const tmpc=document.createElement('canvas'); tmpc.width=N; tmpc.height=N; tmpc.getContext('2d').putImageData(img,0,0); x.imageSmoothingEnabled=true; x.drawImage(tmpc,0,0,cv.width,cv.height);
    x.strokeStyle='rgba(255,255,255,.35)'; x.lineWidth=6; x.beginPath(); x.arc(cv.width/2,cv.height/2,cv.width/2-3,0,7); x.stroke();
    const n=N*N, mean=sum/n, sd=Math.sqrt(Math.max(0,sum2/n-mean*mean)); const mix=mean>0.01?Math.max(0,100-sd/Math.sqrt(mean*(1-mean)+1e-9)*100):0; vort=vs/n;
    setStat('sMix', Math.round(mix)+'%'); setStat('sVort', (vort*100).toFixed(1)); setStat('sT', t.toFixed(0)+'秒');
    setShare('コーヒーにミルクを落として'+t.toFixed(0)+'秒→混ざり具合'+Math.round(mix)+'%☕ 流体の方程式（ナビエ＝ストークス）をブラウザで解いてかき混ぜられる👇'); }
  let last=null; function pointer(e){ const [px,py]=cpos(cv,e); const i=clamp((px/cv.width*N)|0,1,N), j=clamp((py/cv.height*N)|0,1,N); if(last){ const f=+$('force').value*0.8; const dx=(i-last[0]), dy=(j-last[1]); for(let a=-1;a<=1;a++) for(let b=-1;b<=1;b++){ const ii=clamp(i+a,1,N), jj=clamp(j+b,1,N); u[IX(ii,jj)]+=dx*f; v[IX(ii,jj)]+=dy*f; } } last=[i,j]; }
  cv.addEventListener('pointerdown',(e)=>{ last=null; pointer(e); cv.setPointerCapture(e.pointerId); }); cv.addEventListener('pointermove',(e)=>{ if(e.buttons) pointer(e); }); cv.addEventListener('pointerup',()=>last=null);
  function loop(){ step(); draw(); requestAnimationFrame(loop); }
  $('drop').addEventListener('click',()=>drop(N/2+rnd(-12,12),N/2+rnd(-12,12),5)); $('stir').addEventListener('click',stir); $('reset').addEventListener('click',()=>{ alloc(); drop(N/2,N/2,6); }); $('liq').addEventListener('change',preset);
  alloc(); drop(N/2+6,N/2-4,6); stir(); loop();
''')

# ============================================================ 15 地震でビルはどう揺れる
sim(slug="building-quake", cat="wonder", emoji="🏢", score=71,
    title="地震でビルはどう揺れる？ 共振シミュレーター", model="多質点系（せん断型モデル）の応答解析＋共振",
    model_note="建築の耐震設計で使う基本モデル。固有周期 T≈0.02〜0.03×高さ(m)",
    title_tag="地震でビルはどう揺れる？共振シミュレーター｜階数と地震の周期で揺れ方が変わる理由",
    meta_desc="地震の揺れの周期とビルの高さ（固有周期）が一致すると共振して大きく揺れる——建築の耐震設計で使う多質点モデルをブラウザで動かし、低層・中層・高層ビルの揺れ方の違い、長周期地震動で高層ビルが揺れる理由、制振装置の効果を体感できる無料シミュレーター。",
    og_title="地震でビルはどう揺れる？ 共振シミュレーター", og_desc="階数と地震の周期で揺れが変わる。共振と制振を体感。",
    card_desc="階数と地震の周期が合うと共振して大きく揺れる。高層ビルが遠くの地震で揺れる理由を体感。",
    lead="同じ地震でも、低いビルは激しく細かく、高いビルはゆっくり大きく揺れます。揺れの周期とビルの「固有周期」が一致すると、共振で揺れは何倍にも。階数と地震の周期を変えて、その瞬間を見つけてください。制振ダンパーの効果も試せます。",
    canvas=canvas(640, 400),
    controls=slider("fl", "ビルの階数", 3, 60, 20, 1, "{v}階") + slider("per", "地震の揺れの周期", 0.3, 8, 2.0, 0.1, "{v}秒")
           + slider("amp", "地面の揺れの大きさ", 1, 10, 5, 1) + slider("damp", "制振ダンパーの効き", 0, 10, 1, 1) + select("wave", "揺れのタイプ", [("sin", "一定の周期で揺れ続ける（長周期地震動）"), ("quake", "実際の地震っぽい波形（短い強い揺れ）")]),
    buttons=btn("toggle", "⏸ 一時停止") + btn("resonate", "🎯 このビルが共振する周期に合わせる") + btn("reset", "リセット"),
    stats=stats([("sT0", "このビルの固有周期", False), ("sAmp", "最上階の揺れ幅", True), ("sRatio", "地面に対する増幅率", False), ("sState", "状態", False)]),
    legend="左＝ビルの断面（各階が横にずれる）。右＝地面と最上階の揺れの時間変化。",
    article=P("ビルには高さで決まる<b>固有周期</b>（1往復にかかる時間）があり、目安は「0.02〜0.03秒 × 高さ（m）」。10階建て（約30m）で約0.6〜0.9秒、50階建て（約200m）で4〜6秒です。地震の揺れの周期がこれに一致すると<b>共振</b>し、地面の揺れの数倍〜10倍以上に増幅されます。") + '''
<h2>この画面のモデル</h2>
<p>各階を「質点」、柱を「ばね」とみなし、階数分の質点をばねで直列につないだ「せん断型多質点モデル」で計算しています。地面を横に揺らすと、1階から順に力が伝わり、ビル全体がしなります。これは実際の耐震設計で最初に用いる標準的なモデルです。</p>
''' + T([["1〜5階（〜15m）", "0.1〜0.5秒", "直下型の短い周期の揺れに共振。ガタガタと激しく揺れる"], ["10〜20階（30〜70m）", "0.6〜2秒", "多くの地震のエネルギーが集中する帯域"], ["30〜60階（100〜250m）", "3〜7秒", "遠くの巨大地震の長周期地震動に共振。ゆっくり大きく、長く揺れる"]], ["階数（高さ）", "固有周期の目安", "揺れやすい地震"]) + '''
<h2>長周期地震動：高層ビルが遠くの地震で揺れる理由</h2>
<p>2011年の東北地方太平洋沖地震では、震源から700km離れた大阪の55階建てビルが最上階で<b>約2.7m</b>（片側1.3m超）揺れ、10分以上揺れ続けました。短い周期の揺れは距離とともに減衰しますが、周期数秒の長周期地震動は減衰しにくく、堆積盆地（関東平野・大阪平野）で増幅されます。それが高層ビルの固有周期と一致したのです。</p>
<h2>制振ダンパーのはたらき</h2>
<p>共振を防ぐには周期をずらすか、揺れのエネルギーを吸収する「減衰」を増やします。オイルダンパー・粘弾性ダンパー・屋上の巨大なおもり（同調質量ダンパー）などがこの役割で、台北101の660トンの鉄球が有名です。本ページの「制振ダンパーの効き」を上げると、共振時の増幅率が急激に下がることが確認できます。</p>
''',
    faqs=[("固有周期はどう計算している？", "ビルの階数 n から、高さ h≈3.5n（m）として T≈0.025h を目安に設定し、多質点モデルの1次モードがその周期になるようばね定数を決めています。実際の建物は構造（鉄骨・RC）で0.02〜0.03の係数が変わります。"),
          ("免震と制振の違いは？", "免震は建物と地面の間に柔らかい層（積層ゴム）を入れて周期を3〜4秒以上に延ばし、地震の主なエネルギー帯から外す方法。制振は建物内部にダンパーを入れて揺れを吸収する方法です。本ページの「ダンパー」は制振に相当します。"),
          ("低いビルは安全？", "共振する周期が短いため、直下型地震の短周期成分に反応しやすく、加速度（衝撃）は高層より大きくなりがちです。高層は揺れ幅が大きく、低層は衝撃が大きい、という違いです。")],
    rel=[("tsunami-kishi", "🌊", "津波はなぜ岸で高くなる？"), ("jishin-live", "🗾", "日本はいまも揺れている"), ("chikyu-yure", "🌍", "地球まるごと地震カウンター"), ("sync", "✨", "同期現象シミュレーター")],
    js=r'''
  const cv=$('cv'), x=cv.getContext('2d'), W=cv.width, H=cv.height;
  let n, disp, vel, t, run=true, gHist=[], tHist=[], maxTop=0, maxG=0, k, m=1, c;
  function T0(){ return 0.025*3.5*n; }
  function setup(){ n=+$('fl').value; disp=new Float64Array(n); vel=new Float64Array(n); t=0; gHist=[]; tHist=[]; maxTop=0; maxG=0;
    // 1次固有周期 T0 に合わせて k を決定（せん断型: ω1 ≈ 2 sin(π/(2(2n+1))) sqrt(k/m)）
    const w1=2*Math.PI/T0(); const s=2*Math.sin(Math.PI/(2*(2*n+1))); k=(w1/s)**2*m; c=+$('damp').value*0.02*Math.sqrt(k*m); }
  function ground(tt){ const A=+$('amp').value*0.02, P=+$('per').value; if($('wave').value==='sin') return A*Math.sin(2*Math.PI*tt/P); const env=tt<2?tt/2:Math.exp(-(tt-2)/6); return A*env*(Math.sin(2*Math.PI*tt/P)+0.35*Math.sin(2*Math.PI*tt/(P*0.37)+1)+0.2*Math.sin(2*Math.PI*tt/(P*2.3))); }
  function step(dt){ const g=ground(t), gv=(ground(t+1e-3)-ground(t-1e-3))/2e-3; const acc=new Float64Array(n);
    for(let i=0;i<n;i++){ const below=i===0?g:disp[i-1], vb=i===0?gv:vel[i-1]; let f=-k*(disp[i]-below)-c*(vel[i]-vb); if(i<n-1) f+=k*(disp[i+1]-disp[i])+c*(vel[i+1]-vel[i]); acc[i]=f/m; }
    for(let i=0;i<n;i++){ vel[i]+=acc[i]*dt; disp[i]+=vel[i]*dt; } t+=dt;
    gHist.push(g); tHist.push(disp[n-1]); if(gHist.length>600){ gHist.shift(); tHist.shift(); } maxTop=Math.max(maxTop,Math.abs(disp[n-1])); maxG=Math.max(maxG,Math.abs(g)); }
  function draw(){ x.fillStyle='#0b1020'; x.fillRect(0,0,W,H); const bx=150, base=H-30, fh=Math.min(14,(H-70)/n), bw=70, scale=90;
    const g=ground(t); x.fillStyle='#374151'; x.fillRect(0,base,W*0.48,30); x.fillStyle='#9ca3af'; x.font='10px sans-serif'; x.fillText('地面', 8, base+18);
    for(let i=0;i<n;i++){ const y=base-(i+1)*fh; const dx0=(i===0?g:disp[i-1])*scale, dx1=disp[i]*scale; const drift=Math.abs(dx1-dx0)/fh; x.fillStyle=drift>0.5?'#ef4444':drift>0.25?'#f59e0b':'#60a5fa'; x.beginPath(); x.moveTo(bx+dx0-bw/2,y+fh); x.lineTo(bx+dx0+bw/2,y+fh); x.lineTo(bx+dx1+bw/2,y); x.lineTo(bx+dx1-bw/2,y); x.closePath(); x.fill(); x.strokeStyle='#0b1020'; x.stroke(); }
    const L=330,PW=W-L-12,mid=90,ph=70; x.strokeStyle='rgba(255,255,255,.15)'; x.beginPath(); x.moveTo(L,mid); x.lineTo(L+PW,mid); x.moveTo(L,mid+180); x.lineTo(L+PW,mid+180); x.stroke();
    x.fillStyle='#9ca3af'; x.fillText('地面の揺れ', L, 14); x.fillText('最上階の揺れ', L, 194);
    const sc=Math.max(0.2, maxG, maxTop); [[gHist,'#9ca3af',mid],[tHist,'#f472b6',mid+180]].forEach(([h,col,cy])=>{ x.strokeStyle=col; x.lineWidth=1.5; x.beginPath(); h.forEach((v,i)=>{ const X=L+i/599*PW, Y=cy-v/sc*ph; i?x.lineTo(X,Y):x.moveTo(X,Y); }); x.stroke(); });
    const ratio=maxG>0?maxTop/maxG:0; const T=T0(); const P=+$('per').value; const near=Math.abs(P-T)/T;
    setStat('sT0', T.toFixed(1)+'秒'); setStat('sAmp', '±'+(maxTop*100).toFixed(0)+'cm'); setStat('sRatio', ratio.toFixed(1)+'倍'); setStat('sState', near<0.1?'⚠️ 共振中':near<0.3?'共振に近い':'安定');
    setShare(n+'階建て（固有周期'+T.toFixed(1)+'秒）に周期'+P+'秒の地震→最上階は±'+(maxTop*100).toFixed(0)+'cm、地面の'+ratio.toFixed(1)+'倍🏢 '+(near<0.1?'共振！':'')+'高層ビルが遠くの地震で揺れる理由👇'); }
  function loop(){ if(run){ for(let i=0;i<4;i++) step(0.01); } draw(); requestAnimationFrame(loop); }
  ['fl','damp'].forEach(id=>$(id).addEventListener('input',()=>{ const keep=t; setup(); }));
  ['per','amp','wave'].forEach(id=>$(id).addEventListener('input',()=>{ maxTop=0; maxG=0; }));
  $('resonate').addEventListener('click',()=>{ $('per').value=clamp(T0(),0.3,8).toFixed(1); $('per').dispatchEvent(new Event('input')); maxTop=0; maxG=0; });
  $('toggle').addEventListener('click',()=>{ run=!run; $('toggle').textContent=run?'⏸ 一時停止':'▶ 再生'; });
  $('reset').addEventListener('click',setup);
  setup(); loop();
''')
