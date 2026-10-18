# -*- coding: utf-8 -*-
"""理科の授業向け：運動とエネルギー（中3 運動の規則性＝記録タイマー／中3 仕事とエネルギー＝滑車と仕事の原理）"""
import math
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

MEXT_CHU = "https://www.mext.go.jp/a_menu/shotou/new-cs/1387016.htm"
MEXT_KOU = "https://www.mext.go.jp/a_menu/shotou/new-cs/1407074.htm"
G = 9.8

# ---- 記事の数値（Python で計算して埋め込む）
def _tape(th, v0=0.0, n=5):
    a = G * math.sin(math.radians(th))
    X = lambda t: v0 * t + a * t * t / 2
    return a, [(X((j + 1) / 10) - X(j / 10)) * 100 for j in range(n)]
def _f2(v): return "%.2f" % (math.floor(v * 100 + 0.5) / 100)

_rows = []
for th in (0, 10, 15, 20, 30, 45, 60, 90):
    v0 = 0.5 if th == 0 else 0.0
    a, pcs = _tape(th, v0)
    _rows.append(["%d°%s" % (th, "（50cm/sで押す）" if th == 0 else ("（自由落下）" if th == 90 else "")),
                  "%.3f" % math.sin(math.radians(th)), _f2(a), "、".join(_f2(x) for x in pcs),
                  _f2(a) + "cm" if th else "0（同じ長さ）", "%d" % round((v0 + a * 0.5) * 100)])
TAPE_TABLE = T(_rows, ["斜面の角度", "sinθ", "速さの増え方 a（m/s²）", "0.1秒ごとのテープの長さ ①〜⑤（cm）", "1本ごとに長くなる長さ", "0.5秒後の速さ（cm/s）"])

# ============================================================ 1 記録タイマーと台車の運動
KIROKU_ARTICLE = "<h2>このシミュレーションでわかること</h2>\n" + P(
    "斜面を下る台車は、斜面に沿った一定の力を受け続けるので、<b>速さが時間に比例して一定の割合で増えます</b>。斜面の角度が大きいほど速さの増え方は大きくなり、角度が90°のとき（自由落下）にいちばん大きくなります。"
    "水平面で力がはたらかないときは、台車は<b>等速直線運動</b>をします。") + '''
<p>中学校3年の理科「運動とエネルギー」の（ｲ）運動の規則性（学習指導要領 第1分野（5）ア（ｲ）㋑「力と運動」）で学ぶ内容です。高校の物理基礎「運動の表し方」「直線運動の加速度」の導入にも使えます。</p>
<p>斜面の角度（0°＝水平、90°＝自由落下）を決めて「スタート」をおすと、記録タイマーが1秒間に50回（東日本）または60回（西日本）テープに打点します。テープは0.1秒ごと（5打点ごと／6打点ごと）に色分けされ、切ったテープを順にならべた<b>テープグラフ</b>と、移動距離－時間（または速さ－時間）のグラフが同時にできあがります。</p>
<h2>授業での使い方</h2>
<ul>
<li><b>導入</b>：水平（0°）で台車を押した記録と、斜面（15°など）を下る記録を見せ、「テープの打点の間かくのちがいから、どんな運動かわかるかな？」と問いかけます。</li>
<li><b>展開</b>：記録タイマーを使った実験の前後に使います。斜面の角度を変えて何回か記録すると、前の記録が点線で残るので、テープグラフの階段の「上がり方」を比べられます。テープをタップすると、そのテープの長さと、その0.1秒間の平均の速さが表示されます。録画した映像で確かめる代わりに、スロー再生（1/10）で台車の動きと打点の関係を見せることもできます。</li>
<li><b>まとめ</b>：角度を90°にして自由落下にし、「斜面の角度が90°になると自由落下になり、速さの変わり方がいちばん大きくなる」ことを確かめます。水平で押した場合は、テープの長さがそろう（等速直線運動）ことから、慣性の法則にふれます。</li>
</ul>
<p>生徒への問いの例：</p>
<ol>
<li>テープグラフのテープの上の端をつなぐと、どんな形の線になるでしょう。その線は何を表しているでしょう。</li>
<li>斜面の角度を2倍にすると、速さの増え方も2倍になるでしょうか。（15°と30°で比べてみよう）</li>
<li>西日本（1秒間に60回）の記録タイマーでは、何打点ごとに切れば0.1秒ごとのテープになるでしょう。</li>
</ol>
<h2>しくみ・解説</h2>
<h3>用語の意味</h3>
<ul>
<li><b>記録タイマー</b>とは、一定の時間ごと（1秒間に50回または60回）に記録テープに点を打ち、物体の運動のようすを記録する装置です。</li>
<li><b>テープグラフ</b>とは、記録テープを一定の時間（0.1秒）ごとに切り、左から時間の順にならべてはったグラフで、テープの長さが速さを表します。</li>
<li><b>等速直線運動</b>とは、一直線上を一定の速さで進む運動です。</li>
<li><b>慣性の法則</b>とは、物体に力がはたらかないか、はたらく力がつり合っているとき、静止している物体は静止し続け、運動している物体は等速直線運動を続けるという法則です。</li>
<li><b>自由落下</b>とは、静止していた物体が重力だけを受けて真下に落ちる運動です。</li>
</ul>
<h3>打点の間かくと0.1秒の区切り方</h3>
''' + T([["東日本（50Hz）", "50回", "1/50秒＝0.02秒", "5打点ごと（打点の間が5つ）"],
          ["西日本（60Hz）", "60回", "1/60秒＝約0.017秒", "6打点ごと（打点の間が6つ）"]],
         ["地域（電源の周波数）", "1秒間に打つ点の数", "打点の間かく", "0.1秒分のテープ"]) + '''
<p>記録タイマーは、コンセントの交流（東日本50Hz・西日本60Hz）に合わせて振動して点を打つので、地域によって1秒間に打つ点の数がちがいます。0.1秒ごとに切れば、どちらの地域でもテープの長さは同じになります（このシミュレーションの「打点の数」を切りかえて確かめられます）。最初の打点が重なって見分けにくい部分は、実際の実験では切り捨ててから区切ります。</p>
<h3>テープの長さから速さを求める</h3>
''' + N("0.1秒間の平均の速さ（cm/s）＝ 0.1秒分のテープの長さ（cm）÷ 0.1（秒）＝ テープの長さ × 10<br>"
        "例：0.1秒分のテープが6.3cmなら、6.3 ÷ 0.1 ＝ 63cm/s") + '''
<p>テープグラフのテープの長さは「0.1秒間に進んだ距離」なので、速さに比例します。テープの上の端の真ん中をつないだ線は、<b>速さ－時間のグラフ</b>と同じ形になります。斜面を下る台車では右上がりの直線、水平面で押した台車では横に平らな直線になります。</p>
<h3>斜面の角度と速さの増え方（早見表）</h3>
''' + N("斜面に沿った力 ＝ 重力 × sinθ（斜面のどこでも一定）<br>"
        "速さの増え方（加速度）a ＝ g × sinθ（g＝9.8m/s²）<br>"
        "t秒後の速さ v ＝ a × t、t秒間の移動距離 x ＝ ½ × a × t²<br>"
        "0.1秒ごとのテープは、1本ごとに a × 0.1² ＝ a（cm）ずつ長くなる") + TAPE_TABLE + '''
<p>表の数値は、摩擦や空気の抵抗がないとして a＝9.8×sinθ で計算したものです（このシミュレーションと同じ計算）。たとえば15°では、0.1秒ごとのテープが 1.27、3.80、6.34 … cm と、1本ごとに2.54cmずつ長くなります。中学校では速さの変わり方を「斜面の角度が大きいほど、速さの増え方が大きい」と定性的に扱い、a＝g sinθ の式は高校の物理基礎で学びます。</p>
<h3>計算問題の解き方</h3>
<p>例：1秒間に50回打点する記録タイマーで、台車の運動を記録しました。5打点ごとに切ったテープの長さが、順に 2.0cm、4.0cm、6.0cm でした。3本目のテープの間の平均の速さは何cm/sですか。</p>
<ol>
<li>5打点分は 0.02秒 × 5 ＝ 0.1秒</li>
<li>3本目は0.1秒間に6.0cm進んだので、6.0 ÷ 0.1 ＝ 60cm/s</li>
<li>テープが1本ごとに2.0cmずつ長くなっているので、速さは0.1秒ごとに20cm/sずつ増えている（一定の割合で速くなる運動）</li>
</ol>
<h3>このシミュレーションで単純にしていること</h3>
<ul>
<li>台車と斜面・記録タイマーとテープの間の摩擦や、空気の抵抗は考えていません。実際の実験では摩擦があるため、速さの増え方は表の値より少し小さくなります。</li>
<li>摩擦がなければ、斜面を下る速さの増え方は台車の質量によらないので、質量は設定していません。</li>
<li>斜面の長さは2.0mとし、台車が斜面の下に着くか、1.0秒たったところで記録を終えます。図の斜面の長さや台車の大きさは見やすいように変えています。</li>
<li>斜面の台車は静止の状態から手をはなし、水平（0°）のときは「最初に押す速さ」で押し出したあと、手をはなしたものとしています。</li>
</ul>
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「中学校学習指導要領（平成29年告示）解説 理科編」第1分野（5）運動とエネルギー（ｲ）運動の規則性（pp.54〜56）（<a href="''' + MEXT_CHU + '''" target="_blank" rel="noopener">文部科学省 中学校学習指導要領解説のページ</a>）</li>
<li>文部科学省「高等学校学習指導要領（平成30年告示）解説 理科編 理数編」物理基礎（1）ア（ｱ）運動の表し方（<a href="''' + MEXT_KOU + '''" target="_blank" rel="noopener">文部科学省 高等学校学習指導要領解説のページ</a>）</li>
<li>中学校理科の教科書（東京書籍「新しい科学」、啓林館「未来へひろがるサイエンス」、大日本図書「理科の世界」など）3年「運動とエネルギー」</li>
<li>重力加速度 g＝9.8m/s²（高等学校「物理基礎」の教科書で用いられる値）</li>
</ul>
'''

KIROKU_FAQS = [
    ("記録タイマーのテープを5打点ごと（6打点ごと）に切るのはなぜですか？",
     "0.1秒ごとの移動距離を比べるためです。1秒間に50回打点する記録タイマー（東日本）は打点の間かくが0.02秒なので、5打点分で0.1秒になります。1秒間に60回打点する記録タイマー（西日本）は6打点分で0.1秒です。"),
    ("テープグラフの見方を教えてください。",
     "テープグラフは、0.1秒ごとに切ったテープを時間の順にならべたグラフです。テープの長さは0.1秒間に進んだ距離なので、速さに比例します。テープの上の端をつなぐと速さ－時間のグラフと同じ形になり、斜面を下る台車では右上がりの直線になります。"),
    ("斜面の角度を大きくすると、台車の運動はどう変わりますか？",
     "斜面に沿った力（重力×sinθ）が大きくなるので、速さの増え方が大きくなります。摩擦がないとき、速さの増え方は 9.8×sinθ（m/s²）で、15°で約2.54、30°で4.9、90°（自由落下）で9.8 です。斜面の角度が90°のときが自由落下で、速さの増え方がいちばん大きくなります。"),
    ("水平面で台車を押して手をはなすと、どんな運動になりますか？",
     "台車の運動の向きに力がはたらかないので、手をはなしたときの速さのまま一直線上を進む等速直線運動になります（慣性の法則）。0.1秒ごとのテープの長さがすべて同じになります。実際は摩擦があるので、少しずつおそくなります。"),
    ("台車を重くすると、斜面を下る速さの増え方は変わりますか？",
     "摩擦や空気の抵抗がなければ変わりません。台車が重くなると斜面に沿った力も同じ割合で大きくなるため、速さの増え方は 9.8×sinθ のままです。実際の実験では、摩擦の影響で少しちがいが出ることがあります。"),
    ("東日本と西日本で、記録タイマーが1秒間に打つ点の数がちがうのはなぜですか？",
     "記録タイマーは家庭用の交流電源の周波数に合わせて点を打つからです。電源の周波数は東日本が50Hz、西日本が60Hzなので、1秒間に打つ点の数はそれぞれ50回と60回になります。"),
]

KIROKU_JS = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const h1=document.querySelector('.sim-head h1'); if(h1&&!h1.children.length){ const t0=h1.textContent, i=t0.indexOf('（'); if(i>0){ h1.textContent=t0.slice(0,i); const sp=document.createElement('span'); sp.style.display='inline-block'; sp.textContent=t0.slice(i); h1.appendChild(sp); } }
  const bt=document.querySelector('.lab-btns'); if(bt){ cv.parentNode.insertBefore(bt,cv.nextSibling); bt.style.marginTop='0'; }
  const G=9.8, TMAX=1.0, LTR=2.0;
  const GA={x0:46,x1:316,y0:268,y1:440}, GB={x0:380,x1:626,y0:268,y1:440};
  const PC=['#fef08a','#bae6fd'], PCS=['#ca8a04','#0284c7'];
  function setV(id,s){ const e=$(id); if(!e) return; e.textContent=s; e.style.fontSize=s.length>10?'14px':(s.length>7?'16px':''); }
  function rrect(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
  function txt(t,x,y,size,col,weight,align,maxW){ ctx.textAlign=align||'left'; let s=size; ctx.font=(weight||'')+' '+s+'px sans-serif';
    if(maxW){ while(ctx.measureText(t).width>maxW&&s>8){ s-=0.5; ctx.font=(weight||'')+' '+s+'px sans-serif'; } }
    ctx.fillStyle=col||'#0f172a'; ctx.fillText(t,x,y); }
  function dot(x,y,r,c){ ctx.fillStyle=c; ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.fill(); }
  function line(x1,y1,x2,y2,w,c,dash){ ctx.strokeStyle=c; ctx.lineWidth=w; if(dash) ctx.setLineDash(dash); ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2,y2); ctx.stroke(); if(dash) ctx.setLineDash([]); }
  function arrow(x,y,dx,dy,c,w){ const L=Math.hypot(dx,dy); if(L<3) return; const ux=dx/L, uy=dy/L; line(x,y,x+dx-ux*6,y+dy-uy*6,w||3,c);
    ctx.fillStyle=c; ctx.beginPath(); ctx.moveTo(x+dx,y+dy); ctx.lineTo(x+dx-ux*9-uy*5,y+dy-uy*9+ux*5); ctx.lineTo(x+dx-ux*9+uy*5,y+dy-uy*9-ux*5); ctx.closePath(); ctx.fill(); }
  const f1=(v)=>(Math.round(v*10)/10).toFixed(1);
  const f2=(v)=>(Math.round(v*100)/100).toFixed(2);
  const CIR='①②③④⑤⑥⑦⑧⑨⑩';
  function niceMax(v){ const L=[5,10,20,30,40,50,60,80,100,120,150,200,250,300,400,500,600]; for(const x of L){ if(v<=x*1.0001) return x; } return Math.ceil(v/100)*100; }
  function calc(){ const th=+$('ang').value, v0=+$('v0').value/100, hz=+$('hz').value, n=hz/10, a=G*Math.sin(th*Math.PI/180);
    const X=(t)=>v0*t+a*t*t/2; let tEnd=TMAX;
    if(X(TMAX)>LTR) tEnd=a>1e-9?(-v0+Math.sqrt(v0*v0+2*a*LTR))/a:LTR/v0;
    const nd=Math.floor(tEnd*hz+1e-9), dots=[]; for(let k=0;k<=nd;k++) dots.push(X(k/hz));
    const np=Math.floor(tEnd*10+1e-9), pcs=[]; for(let j=0;j<np;j++) pcs.push({x0:X(j/10),L:X((j+1)/10)-X(j/10)});
    return {th:th,v0:v0,hz:hz,n:n,a:a,tEnd:tEnd,X:X,dots:dots,pcs:pcs,len:X(tEnd),done:false}; }
  let cur=calc(), ghost=null, st='done', t=0, sel=-1, anims=[], doneSeen=0;
  cur.done=true; t=cur.tEnd; doneSeen=cur.pcs.length;
  function kind(c){ if(c.th>=90) return 'fall'; if(c.th>0) return 'slope'; return c.v0>0?'uniform':'rest'; }
  function update(){ const c=calc(), k=kind(c);
    setV('s1',{fall:'自由落下（どんどん速くなる）',slope:'だんだん速くなる',uniform:'等速直線運動',rest:'静止したまま'}[k]);
    setV('s2',f2(c.a)+' cm'); setV('s3',(c.hz===50?'0.02秒（5打点で0.1秒）':'約0.017秒（6打点で0.1秒）')); setV('s4',Math.round((c.v0+c.a*0.5)*100)+' cm/s');
    if(k==='rest') setShare('【記録タイマー】水平面で押さない台車は静止したまま。打点はすべて同じ所に重なる（慣性の法則）｜シミュラボ');
    else if(k==='uniform') setShare('【記録タイマー】水平面で'+Math.round(c.v0*100)+'cm/sで押した台車は、0.1秒ごとのテープの長さがすべて'+f1(c.v0*10)+'cmの等速直線運動（慣性の法則）｜シミュラボ');
    else setShare('【記録タイマー】斜面の角度'+c.th+'°'+(k==='fall'?'（自由落下）':'')+'では、0.1秒ごとのテープが'+f2(c.a)+'cmずつ長くなる（速さの増え方 9.8×sin'+c.th+'°＝'+f2(c.a)+'m/s²）｜シミュラボ'); }
  function prepare(){ if(cur.done) ghost=cur; cur=calc(); st='idle'; t=0; sel=-1; anims=[]; doneSeen=0; $('start').textContent='▶ スタート（台車をはなす）'; update(); }
  function start(){ if(cur.done) ghost=cur; cur=calc(); st='run'; t=0; sel=-1; anims=[]; doneSeen=0; $('start').textContent='▶ もう一度記録する'; update(); }
  function setVal(id,v){ const e=$(id); e.value=v; e.dispatchEvent(new Event('input')); }
  ['ang','v0'].forEach((id)=>$(id).addEventListener('input',prepare));
  $('hz').addEventListener('change',prepare);
  $('start').addEventListener('click',start);
  $('reset').addEventListener('click',()=>{ ghost=null; cur=calc(); st='idle'; t=0; sel=-1; anims=[]; doneSeen=0; $('start').textContent='▶ スタート（台車をはなす）'; update(); });
  $('b0').addEventListener('click',()=>{ setVal('ang',0); if(+$('v0').value===0) setVal('v0',50); });
  $('b90').addEventListener('click',()=>{ setVal('ang',90); setVal('v0',0); });
  function tapeRect(j){ const c=cur, sx=608/Math.max(c.len,1e-6), p=c.pcs[j]; return [16+p.x0*sx,206,Math.max(1,p.L*sx),22]; }
  function slotRect(j,ymax){ const c=cur, sw=(GA.x1-GA.x0)/10, sy=(GA.y1-GA.y0)/ymax, L=c.pcs[j].L*100; return [GA.x0+j*sw+2,GA.y1-L*sy,sw-4,L*sy]; }
  // ---------- 実験のようす
  function scene(){ const c=cur, th=c.th*Math.PI/180, co=Math.cos(th), si=Math.sin(th), k=kind(c);
    ctx.fillStyle='#f8fafc'; rrect(6,6,326,178,10); ctx.fill(); ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; ctx.stroke();
    const Lpx=Math.min(co>1e-6?250/co:1e9, si>1e-6?116/si:1e9), Ey=162;
    const Sx=175-Lpx*co/2, Sy=Ey-Lpx*si, Ex=Sx+Lpx*co, nx=si, ny=-co;
    const tt=st==='idle'?0:Math.min(t,c.tEnd), u=(k==='fall'?28:6)+c.X(tt)/LTR*(Lpx-(k==='fall'?58:52)), Px=Sx+co*u, Py=Sy+si*u;
    if(k==='fall'){ line(Sx-50,Ey+4,Sx+70,Ey+4,3,'#94a3b8'); line(Sx-40,Ey+4,Sx-40,20,4,'#94a3b8'); line(Sx-40,22,Sx,22,4,'#94a3b8'); line(Sx+10,Sy,Sx+10,Ey,1,'#cbd5e1',[4,4]); }
    else if(k==='slope'){ ctx.fillStyle='#e2e8f0'; ctx.beginPath(); ctx.moveTo(Sx,Sy+3); ctx.lineTo(Ex,Ey+3); ctx.lineTo(Sx,Ey+3); ctx.closePath(); ctx.fill(); line(Sx,Sy,Ex,Ey,5,'#94a3b8');
      ctx.strokeStyle='#ea580c'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.arc(Ex,Ey+3,30,Math.PI,Math.PI+th,false); ctx.stroke();
      txt(c.th+'°',Ex-46*Math.cos(th/2),Ey+3-46*Math.sin(th/2)+5,13,'#c2410c','bold','center'); }
    else line(16,Ey+3,322,Ey+3,5,'#94a3b8');
    // 記録タイマー
    const Tx=Sx-co*22+nx*10, Ty=Sy-si*22+ny*10;
    ctx.save(); ctx.translate(Tx,Ty); ctx.rotate(th); ctx.fillStyle='#334155'; rrect(-16,-10,32,20,4); ctx.fill(); ctx.fillStyle='#f97316'; ctx.fillRect(10,-3,6,6); ctx.restore();
    if(k==='fall') txt('記録タイマー',Tx+16,Ty+4,11,'#334155','bold','left'); else txt('記録タイマー',Math.max(10,Tx-28),Ty-16,11,'#334155','bold','left');
    // テープ
    const bx=Px+nx*10, by=Py+ny*10;
    line(Tx+co*14,Ty+si*14,bx,by,4,'#fcd34d');
    // 台車（自由落下はおもり）
    if(k==='fall'){ ctx.fillStyle='#0e7490'; rrect(bx-13,by,26,26,5); ctx.fill(); txt('おもり',bx-18,by+17,11,'#0e7490','bold','right'); arrow(bx+22,by+2,0,24,'#64748b',2.5); txt('重力',bx+30,by+20,11,'#475569','bold','left'); }
    else { ctx.save(); ctx.translate(Px,Py); ctx.rotate(th); ctx.fillStyle='#0e7490'; rrect(0,-24,46,16,4); ctx.fill(); ctx.fillStyle='#1e293b'; ctx.beginPath(); ctx.arc(10,-5,5,0,Math.PI*2); ctx.arc(36,-5,5,0,Math.PI*2); ctx.fill(); ctx.restore();
      const cx=Px+co*23+nx*16, cy=Py+si*23+ny*16;
      if(k==='slope'){ arrow(cx,cy,0,32,'#64748b',2.5); arrow(cx,cy,co*32*si,si*32*si,'#dc2626',3);
        txt('↓ 重力',14,178,11,'#475569','bold','left'); txt('→ 斜面に沿った力（重力×sin'+c.th+'°）',62,178,11,'#dc2626','bold','left',200); }
      else txt('台車',cx,cy-14,11,'#0e7490','bold','center'); }
    if(k==='uniform') txt('運動の向きに力ははたらかない',322,26,11,'#475569','bold','right');
    if(k==='rest') txt('押さないと台車は動かない（静止し続ける）',322,26,11,'#b91c1c','bold','right',300); }
  // ---------- 数値パネル
  function panel(){ const c=cur, k=kind(c), tt=st==='idle'?0:Math.min(t,c.tEnd);
    ctx.fillStyle='#fff'; rrect(340,6,294,178,10); ctx.fill(); ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; ctx.stroke();
    const nd=st==='idle'?0:Math.floor(tt*c.hz+1e-9)+1;
    [['経過時間',f2(tt)+' 秒',352,24],['速さ',Math.round((c.v0+c.a*tt)*100)+' cm/s',496,24],['移動距離',f1(c.X(tt)*100)+' cm',352,80],['打点の数',nd+' 個',496,80]].forEach((q)=>{
      txt(q[0],q[2],q[3],11.5,'#64748b','bold','left'); txt(q[1],q[2],q[3]+28,24,'#0f172a','bold','left',134); });
    const rule={fall:'自由落下：速さの増え方がいちばん大きい',slope:'斜面に沿った力が一定 → 速さが一定の割合で増える',uniform:'力がはたらかない → 等速直線運動（慣性）',rest:'力がはたらかない → 静止し続ける（慣性）'}[k];
    txt(rule,352,130,12.5,'#c2410c','bold','left',272);
    txt(k==='slope'||k==='fall'?'0.1秒ごとのテープが '+f2(c.a)+' cm ずつ長くなる（'+f2(c.a)+'＝9.8×sin'+c.th+'°）':'0.1秒ごとのテープの長さは、どれも '+f1(c.v0*10)+' cm',352,150,11.5,'#334155','','left',272);
    const sl={'0.1':'1/10','0.2':'1/5','0.5':'1/2','1':'実際の速さ'}[$('spd').value]||'';
    txt(st==='run'?'● 記録中（スロー '+sl+'）':(st==='done'?'■ 記録終了：0.1秒分のテープ '+c.pcs.length+' 本':'▶「スタート」で'+(k==='uniform'?'台車を押す':'台車をはなす')),352,172,11.5,st==='run'?'#15803d':'#475569','bold','left',272); }
  // ---------- 記録テープ
  function strip(){ const c=cur, tt=st==='idle'?0:Math.min(t,c.tEnd);
    txt('記録テープ（'+c.n+'打点＝0.1秒ごとに色分け。全長 '+f1(c.len*100)+' cm を縮めて表示）',16,200,11.5,'#334155','bold','left',608);
    ctx.fillStyle='#f1f5f9'; ctx.fillRect(16,206,608,22);
    if(c.len<1e-6){ if(st!=='idle'){ ctx.fillStyle='#fef9c3'; ctx.fillRect(16,206,30,22); dot(22,217,3.5,'#111'); txt('台車が動かないので、打点がすべて同じ所に重なる',54,222,12,'#b91c1c','bold','left'); } return; }
    const sx=608/c.len, xt=c.X(tt);
    ctx.fillStyle='#fffbeb'; ctx.fillRect(16,206,xt*sx,22);
    c.pcs.forEach((p,j)=>{ if(p.x0>=xt) return; const w=Math.min(p.L,xt-p.x0)*sx; ctx.fillStyle=PC[j%2]; ctx.fillRect(16+p.x0*sx,206,Math.max(0.5,w),22);
      if(sel===j){ ctx.strokeStyle='#dc2626'; ctx.lineWidth=2; ctx.strokeRect(16+p.x0*sx,206,p.L*sx,22); }
      if(p.x0+p.L<=xt+1e-9&&p.L*sx>13) txt(CIR[j],16+(p.x0+p.L/2)*sx,242,11,PCS[j%2],'bold','center'); });
    const nd=Math.floor(tt*c.hz+1e-9); for(let k=0;k<=nd&&k<c.dots.length;k++) dot(16+c.dots[k]*sx,217,1.7,'#111827'); }
  // ---------- テープグラフ
  function graphA(){ const c=cur, sw=(GA.x1-GA.x0)/10;
    let mx=5; c.pcs.forEach((p)=>{ mx=Math.max(mx,p.L*100); }); if(ghost) ghost.pcs.forEach((p)=>{ mx=Math.max(mx,p.L*100); }); const ym=niceMax(mx), sy=(GA.y1-GA.y0)/ym;
    txt('テープグラフ（0.1秒ごとに切ってならべる・cm）',GA.x0-38,258,12.5,'#0f172a','bold','left',312);
    const step=ym<=10?2:(ym<=30?5:(ym<=60?10:(ym<=150?25:50)));
    for(let v=0;v<=ym+1e-9;v+=step){ const y=GA.y1-v*sy; line(GA.x0,y,GA.x1,y,1,'#eef2f7'); txt(String(v),GA.x0-5,y+4,10.5,'#64748b','','right'); }
    for(let j=0;j<=10;j+=2){ const x=GA.x0+j*sw; txt(j===10?'1.0秒':(j/10).toFixed(1),x,GA.y1+15,10.5,'#64748b','','center'); }
    line(GA.x0,GA.y1,GA.x1,GA.y1,1.5,'#94a3b8'); line(GA.x0,GA.y0,GA.x0,GA.y1,1.5,'#94a3b8');
    if(ghost){ ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1.2; ctx.setLineDash([4,3]); ghost.pcs.forEach((p,j)=>{ const L=p.L*100; ctx.strokeRect(GA.x0+j*sw+2,GA.y1-L*sy,sw-4,L*sy); }); ctx.setLineDash([]); }
    const fly={}; anims.forEach((a)=>{ fly[a.j]=1; });
    const tops=[];
    for(let j=0;j<doneSeen;j++){ if(fly[j]) continue; const r=slotRect(j,ym); ctx.fillStyle=PC[j%2]; ctx.fillRect(r[0],r[1],r[2],r[3]); ctx.strokeStyle=sel===j?'#dc2626':PCS[j%2]; ctx.lineWidth=sel===j?2.5:1; ctx.strokeRect(r[0],r[1],r[2],r[3]);
      const x0=c.pcs[j].x0; for(let k=0;k<=c.n;k++){ const d=c.dots[j*c.n+k]; if(d===undefined) break; dot(r[0]+r[2]/2,GA.y1-(d-x0)*100*sy,1.4,'#111827'); }
      tops.push([r[0]+r[2]/2,r[1]]); }
    if(tops.length>=2){ ctx.strokeStyle='#dc2626'; ctx.lineWidth=2; ctx.setLineDash([5,3]); ctx.beginPath(); tops.forEach((p,i)=>{ if(i) ctx.lineTo(p[0],p[1]); else ctx.moveTo(p[0],p[1]); }); ctx.stroke(); ctx.setLineDash([]); }
    anims.forEach((a)=>{ const r0=tapeRect(a.j), r1=slotRect(a.j,ym), e=a.s<0.5?2*a.s*a.s:1-Math.pow(-2*a.s+2,2)/2; ctx.fillStyle=PC[a.j%2]; ctx.globalAlpha=0.9;
      ctx.fillRect(r0[0]+(r1[0]-r0[0])*e,r0[1]+(r1[1]-r0[1])*e,r0[2]+(r1[2]-r0[2])*e,r0[3]+(r1[3]-r0[3])*e); ctx.globalAlpha=1; });
    return ym; }
  // ---------- 移動距離／速さ－時間のグラフ
  function graphB(){ const c=cur, vel=$('gb').value==='v', tt=st==='idle'?0:Math.min(t,c.tEnd), sw=(GB.x1-GB.x0)/10;
    const f=(r,x)=>vel?(r.v0+r.a*x)*100:r.X(x)*100;
    let mx=5; mx=Math.max(mx,f(c,c.tEnd)); if(ghost) mx=Math.max(mx,f(ghost,ghost.tEnd)); const ym=niceMax(mx), sy=(GB.y1-GB.y0)/ym;
    txt(vel?'速さ－時間のグラフ（cm/s）':'移動距離－時間のグラフ（cm）',GB.x0-34,258,12.5,'#0f172a','bold','left',260);
    const step=ym/5;
    for(let i=0;i<=5;i++){ const v=step*i, y=GB.y1-v*sy; line(GB.x0,y,GB.x1,y,1,'#eef2f7'); txt(String(Math.round(v)),GB.x0-5,y+4,10.5,'#64748b','','right'); }
    for(let j=0;j<=10;j+=2){ const x=GB.x0+j*sw; txt(j===10?'1.0秒':(j/10).toFixed(1),x,GB.y1+15,10.5,'#64748b','','center'); }
    line(GB.x0,GB.y1,GB.x1,GB.y1,1.5,'#94a3b8'); line(GB.x0,GB.y0,GB.x0,GB.y1,1.5,'#94a3b8');
    const gx=(x)=>GB.x0+x*10*sw, gy=(v)=>GB.y1-v*sy;
    function curve(r,te,col,w,dash){ ctx.strokeStyle=col; ctx.lineWidth=w; if(dash) ctx.setLineDash(dash); ctx.beginPath(); const n=Math.max(1,Math.ceil(te/0.005)); for(let i=0;i<=n;i++){ const x=te*i/n; if(i) ctx.lineTo(gx(x),gy(f(r,x))); else ctx.moveTo(gx(x),gy(f(r,x))); } ctx.stroke(); if(dash) ctx.setLineDash([]); }
    if(ghost){ curve(ghost,ghost.tEnd,'#94a3b8',1.5,[5,4]); txt('点線：前の記録（'+ghost.th+'°）',GB.x0+6,GB.y0+12,10.5,'#64748b','','left'); }
    if(tt>0){ curve(c,tt,'#0e7490',2.5); for(let j=1;j<=10&&j/10<=tt+1e-9;j++) dot(gx(j/10),gy(f(c,j/10)),3,'#0e7490'); dot(gx(tt),gy(f(c,tt)),4.5,'#dc2626'); } }
  function draw(){ ctx.fillStyle='#fff'; ctx.fillRect(0,0,W,H); scene(); panel(); strip(); graphA(); graphB();
    const c=cur;
    if(sel>=0&&sel<c.pcs.length){ const L=c.pcs[sel].L*100; txt(CIR[sel]+' '+(sel/10).toFixed(1)+'〜'+((sel+1)/10).toFixed(1)+'秒のテープ：'+f1(L)+' cm → この0.1秒間の平均の速さ '+Math.round(L*10)+' cm/s',320,480,12.5,'#b91c1c','bold','center',620); }
    else txt('テープグラフのテープをタップすると、長さと平均の速さが出ます。摩擦・空気の抵抗なし、g＝9.8m/s²',320,480,11.5,'#64748b','','center',620); }
  function stepF(dt){ if(st==='run'){ t+=dt*(+$('spd').value);
      while(doneSeen<cur.pcs.length&&(doneSeen+1)/10<=t+1e-9){ anims.push({j:doneSeen,s:0}); doneSeen++; }
      if(t>=cur.tEnd){ t=cur.tEnd; st='done'; cur.done=true; } }
    anims.forEach((a)=>{ a.s+=dt/0.55; }); anims=anims.filter((a)=>a.s<1); }
  cv.addEventListener('pointerdown',(e)=>{ const p=cpos(cv,e), x=p[0]/dpr, y=p[1]/dpr;
    if(x>=GA.x0&&x<=GA.x1&&y>=GA.y0-10&&y<=GA.y1+4){ const j=Math.floor((x-GA.x0)/((GA.x1-GA.x0)/10)); if(j>=0&&j<doneSeen){ sel=(sel===j)?-1:j; e.preventDefault(); } return; }
    if(x>=16&&x<=624&&y>=200&&y<=234&&cur.len>0){ const xs=(x-16)/608*cur.len; const j=cur.pcs.findIndex((q)=>xs>=q.x0&&xs<q.x0+q.L); if(j>=0&&j<doneSeen){ sel=(sel===j)?-1:j; e.preventDefault(); } return; }
    if(x<=332&&y<=184&&st!=='run'){ e.preventDefault(); start(); } });
  update();
  let last=performance.now();
  function loop(now){ const dt=Math.min(0.05,Math.max(0,(now-last)/1000)); last=now; stepF(dt); draw(); requestAnimationFrame(loop); }
  draw(); requestAnimationFrame(loop);
'''

sim(slug="kiroku-timer", cat="rika", emoji="🛒", score=78,
    title="記録タイマーと台車の運動シミュレーター（斜面の運動・自由落下）",
    title_tag="記録タイマー・テープグラフのシミュレーター｜斜面を下る台車の運動・等速直線運動・自由落下（中3理科 運動の規則性）",
    meta_desc="中3理科「運動の規則性」の記録タイマーの実験を再現。斜面の角度（0°〜90°）を決めて台車を走らせると、1秒間に50回（東日本）・60回（西日本）の打点が記録テープに並び、0.1秒ごとに切ったテープグラフと移動距離・速さのグラフができます。等速直線運動・自由落下も。",
    og_title="記録タイマーと台車の運動シミュレーター（中3 運動の規則性）",
    og_desc="斜面の角度を変えて台車を走らせると、記録テープの打点・テープグラフ・速さと移動距離のグラフができる。水平で等速、90°で自由落下。",
    card_desc="斜面の角度を変えると打点とテープグラフが変わる。水平で等速直線運動、90°で自由落下。50Hz/60Hz切りかえ。",
    lead="斜面の角度を決めて「スタート」をおすと、台車が斜面を下り、記録タイマーの打点が記録テープに並びます。0.1秒ごとに切ったテープを並べたテープグラフと、移動距離（速さ）－時間のグラフが同時にできあがります。",
    model="中3 運動の規則性（記録タイマー・斜面の運動）", level="中学3年、高校 物理基礎",
    unit="中学校 第1分野（5）ア（ｲ）運動の規則性／高等学校 物理基礎（1）ア（ｱ）運動の表し方",
    canvas=canvas(640, 490, light=True),
    controls=slider("ang", "斜面の角度", 0, 90, 15, 5, "{v}°")
             + slider("v0", "最初に押す速さ", 0, 100, 0, 10, "{v}cm/s")
             + select("hz", "記録タイマー", [("50", "1秒間に50回打点（東日本）"), ("60", "1秒間に60回打点（西日本）")])
             + select("spd", "再生の速さ", [("0.2", "スロー（1/5）"), ("0.1", "スロー（1/10）"), ("0.5", "スロー（1/2）"), ("1", "実際の速さ")])
             + select("gb", "右のグラフ", [("x", "移動距離－時間"), ("v", "速さ－時間")]),
    buttons=btn("start", "▶ スタート（台車をはなす）", True) + btn("b0", "水平（0°）で押す") + btn("b90", "自由落下（90°）") + btn("reset", "↺ 記録を消す"),
    stats=stats([("s1", "運動のようす", True), ("s2", "0.1秒ごとのテープの増え方", False), ("s3", "打点の間かく", False), ("s4", "0.5秒後の速さ", False)]),
    legend="斜面の角度は0°で水平、90°で自由落下です。「最初に押す速さ」は台車を押し出す速さです（斜面では0のとき静止からはなします）。テープは0.1秒（50回打点なら5打点、60回打点なら6打点）ごとに黄色と水色で色分けしています。テープグラフの赤い点線は、テープの上の端をつないだ線（速さ－時間のグラフと同じ形）です。条件を変えて記録すると、前の記録が灰色の点線で残ります。摩擦と空気の抵抗は考えていません（g＝9.8m/s²）。斜面の長さは2.0mで、図の大きさは見やすく変えています。",
    article=KIROKU_ARTICLE, faqs=KIROKU_FAQS,
    rel=[("kassha-shigoto", "🏗️", "滑車と仕事の原理シミュレーター"), ("furiko-jikken", "⏱️", "振り子の実験シミュレーター"),
         ("bane-nobi", "🌀", "ばねののびと力の大きさ"), ("newtons-cradle", "🟤", "ニュートンのゆりかご"), ("gravity", "🌌", "重力シミュレーター")],
    js=KIROKU_JS)

# ============================================================ 2 滑車と仕事の原理
MASS0, H0, T0 = 1000, 50, 5           # 初期値：1000g（10N）を50cm持ち上げる、5秒
W0, h0 = MASS0 / 100, H0 / 100
def _n(v):
    r = math.floor(v * 100 + 0.5) / 100
    s = ("%.2f" % r).rstrip("0").rstrip(".")
    return ("約" if abs(v - r) > 1e-9 else "") + s
_ways = [("直接持ち上げる", W0, h0, "—"), ("定滑車", W0, h0, "力の向きを変えられる（下に引ける）"),
         ("動滑車", W0 / 2, 2 * h0, "2本のひもで支えるので力は半分"), ("定滑車＋動滑車", W0 / 2, 2 * h0, "力は半分で、下向きに引ける"),
         ("動滑車2個（＋定滑車）", W0 / 4, 4 * h0, "力は1/4、引く距離は4倍"), ("斜面（長さ100cm）", W0 * h0 / 1.0, 1.0, "力 ＝ 重力 × 高さ ÷ 斜面の長さ"),
         ("てこ（支点からのきょり 2:1）", W0 / 2, 2 * h0, "力点を支点から遠くする")]
WAYS_TABLE = T([[nm, _n(F) + " N", _n(d) + " m", _n(F * d) + " J", note] for nm, F, d, note in _ways],
               ["持ち上げ方", "必要な力", "力を加えて動かす距離", "仕事（力×距離）", "ポイント"])
POWER_TABLE = T([["%d秒" % s, "%s J" % _n(W0 * h0), _n(W0 * h0 / s) + " W"] for s in (1, 2, 5, 10, 20)],
                ["かかった時間", "仕事", "仕事率（仕事÷時間）"])

KASSHA_ARTICLE = "<h2>このシミュレーションでわかること</h2>\n" + P(
    "定滑車・動滑車・斜面・てこなどの道具を使うと、物体を持ち上げるのに必要な力を小さくできますが、そのぶん力を加えて動かす距離が長くなり、"
    "<b>仕事（力×距離）の大きさは道具を使わないときと変わりません</b>。これを<b>仕事の原理</b>といいます。") + '''
<p>中学校3年の理科「運動とエネルギー」の（ｳ）力学的エネルギー ㋐仕事とエネルギー（学習指導要領 第1分野（5）ア（ｳ））で学ぶ内容です。学習指導要領の内容の取扱いでは「仕事の原理にも触れること」とされています。</p>
<p>物体の質量と持ち上げる高さを決め、「直接持ち上げる／定滑車／動滑車／定滑車＋動滑車／動滑車2個／斜面／てこ」を切りかえると、必要な力・力を加えて動かす距離・仕事（J）が表に並びます。持ち上げるのにかかった時間を決めると、仕事率（W）も計算されます。</p>
<h2>授業での使い方</h2>
<ul>
<li><b>導入</b>：「重い物を楽に持ち上げるには、どんな道具を使えばよいかな？」と問いかけ、動滑車を選んで、必要な力が半分になることを見せます。</li>
<li><b>展開</b>：ばねばかりと滑車を使った実験の前後に使います。表の「必要な力」と「距離」をかけ算すると、どの方法でも同じ値になることに気づかせます。右側の長方形（たて＝力、横＝距離）の面積が仕事で、形が変わっても面積は同じです。図を指でドラッグすると、手を動かした長さと物体が上がった高さを比べられます。</li>
<li><b>まとめ</b>：かかった時間を変えて、同じ仕事でも短い時間でするほど仕事率が大きいことを確かめます。</li>
</ul>
<p>生徒への問いの例：</p>
<ol>
<li>動滑車を使うと、ひもを引く力は半分になります。では、ひもを引く距離はどうなるでしょう。</li>
<li>定滑車を使っても力の大きさは変わりません。それでも定滑車を使うのはなぜでしょう。</li>
<li>同じ物体を、Aさんは5秒、Bさんは10秒かけて同じ高さまで持ち上げました。仕事と仕事率をそれぞれ比べましょう。</li>
</ol>
<h2>しくみ・解説</h2>
<h3>用語の意味</h3>
<ul>
<li><b>仕事</b>とは、物体に力を加えてその力の向きに物体を動かしたときの「力の大きさ × 力の向きに動かした距離」で、単位はジュール（J）です。</li>
<li><b>仕事の原理</b>とは、道具を使っても使わなくても、同じ状態にするための仕事の大きさは変わらないという原理です。</li>
<li><b>仕事率</b>とは、1秒間あたりにする仕事の大きさで、単位はワット（W）です。</li>
<li><b>定滑車</b>とは、天井などに固定されて回るだけの滑車で、力の向きを変えられますが、力の大きさは変わりません。</li>
<li><b>動滑車</b>とは、物体といっしょに動く滑車で、2本のひもで物体を支えるので、ひもを引く力は半分になりますが、引く距離は2倍になります。</li>
</ul>
''' + N("仕事（J）＝ 力の大きさ（N）× 力の向きに動かした距離（m）<br>"
        "仕事率（W）＝ 仕事（J）÷ かかった時間（s）<br>"
        "物体を持ち上げる仕事 ＝ 物体にはたらく重力（N）× 持ち上げる高さ（m）<br>"
        "100gの物体にはたらく重力の大きさ ＝ 1N（教科書の約束。正確には約0.98N）") + '''
<h3>道具ごとの力・距離・仕事（早見表）</h3>
<p>1000g（重力10N）の物体を50cm（0.5m）持ち上げるときの値です（滑車・ひも・棒の質量と摩擦は考えません）。</p>
''' + WAYS_TABLE + '''
<p>どの方法でも、仕事は 10N × 0.5m ＝ 5J になります。力が半分なら距離は2倍、力が1/4なら距離は4倍と、力と距離は反比例の関係になっています。斜面では「力 × 斜面の長さ ＝ 重力 × 高さ」、てこでは「支点から力点までのきょり ÷ 支点から作用点までのきょり」の倍だけ力が小さくなり、そのぶん大きく動かす必要があります。</p>
<h3>仕事率の早見表</h3>
''' + POWER_TABLE + '''
<h3>計算問題の解き方</h3>
<p>例：質量2kgの物体を、動滑車を使って1.5mの高さまで、6秒かけて引き上げました。100gの物体にはたらく重力の大きさを1Nとします。</p>
<ol>
<li>物体にはたらく重力：2kg＝2000g なので 20N</li>
<li>動滑車なので、ひもを引く力は 20 ÷ 2 ＝ 10N、ひもを引く距離は 1.5 × 2 ＝ 3m</li>
<li>仕事：10N × 3m ＝ 30J（直接持ち上げても 20N × 1.5m ＝ 30J で同じ）</li>
<li>仕事率：30J ÷ 6秒 ＝ 5W</li>
</ol>
<h3>このシミュレーションで単純にしていること</h3>
<ul>
<li>滑車・ひも・てこの棒の質量と、滑車の軸・斜面の摩擦は考えていません。実際の実験では、動滑車の重さや摩擦のぶん、ひもを引く力が少し大きくなり、道具を使ったほうが仕事は少し大きくなります。</li>
<li>物体はゆっくり一定の速さで持ち上げるものとし、力の大きさは物体を支えてつり合うときの値です。</li>
<li>100gの物体にはたらく重力の大きさを1Nとして計算しています（中学校の教科書と同じ約束）。</li>
<li>図の大きさ（滑車の位置や動く長さ）は見やすいように変えた模式図です。正しい数値は右側と下の表を見てください。</li>
</ul>
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「中学校学習指導要領（平成29年告示）解説 理科編」第1分野（5）運動とエネルギー（ｳ）力学的エネルギー ㋐仕事とエネルギー（pp.56〜57）（<a href="''' + MEXT_CHU + '''" target="_blank" rel="noopener">文部科学省 中学校学習指導要領解説のページ</a>）</li>
<li>中学校理科の教科書（東京書籍「新しい科学」、啓林館「未来へひろがるサイエンス」、大日本図書「理科の世界」など）3年「運動とエネルギー」の仕事の単元</li>
</ul>
'''

KASSHA_FAQS = [
    ("仕事の原理とは何ですか？",
     "道具を使っても使わなくても、物体を同じ状態にするための仕事の大きさは変わらないという原理です。動滑車や斜面・てこを使うと必要な力は小さくなりますが、そのぶん力を加えて動かす距離が長くなるので、力×距離の仕事は同じになります。"),
    ("動滑車を使うと、なぜ力が半分になるのですか？",
     "動滑車は物体といっしょに動き、物体を左右2本のひもで支えるからです。1本のひもにかかる力は重力の半分になります。そのかわり、物体を1m上げるには左右のひもを1mずつ、合わせて2m引く必要があります。"),
    ("定滑車を使うと、どんな良いことがありますか？",
     "力の大きさは変わりませんが、力の向きを変えられます。物体を上に持ち上げるのに、ひもを下向きに引けばよいので、自分の体重も使えて作業しやすくなります。"),
    ("仕事率はどうやって求めますか？ 単位は何ですか？",
     "仕事率（W）＝ 仕事（J）÷ かかった時間（秒）で求め、単位はワット（W）です。1Wは1秒間に1Jの仕事をする仕事率です。同じ仕事でも、短い時間でするほど仕事率は大きくなります。"),
    ("物体を持ったまま水平に歩くと、仕事をしたことになりますか？",
     "理科でいう仕事は0です。物体を支える力は上向きですが、物体は水平に動いていて、力の向きには動いていないからです。仕事は「力の向きに動いた距離」で計算します。"),
    ("100gの物体にはたらく重力が1Nなのはなぜですか？",
     "中学校の教科書では、計算しやすいように「100gの物体にはたらく重力の大きさを1N」とする約束で問題を解きます。正確には、100gの物体にはたらく重力は約0.98N（0.1kg×9.8m/s²）です。"),
]

KASSHA_JS = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const h1=document.querySelector('.sim-head h1'); if(h1&&!h1.children.length){ const t0=h1.textContent, i=t0.indexOf('（'); if(i>0){ h1.textContent=t0.slice(0,i); const sp=document.createElement('span'); sp.style.display='inline-block'; sp.textContent=t0.slice(i); h1.appendChild(sp); } }
  const bt=document.querySelector('.lab-btns'); if(bt){ cv.parentNode.insertBefore(bt,cv.nextSibling); bt.style.marginTop='0'; }
  const M=[['direct','直接持ち上げる'],['fixed','定滑車'],['move','動滑車'],['combo','定滑車＋動滑車'],['move2','動滑車2個（＋定滑車）'],['slope','斜面'],['lever','てこ']];
  const FY=266, OW=58, OH=42, TY=300, RH=23;
  let mode='move', p=0, run=false, el=0, grab=null, g0=null, finished=false;
  const fld=(id)=>$(id).closest('.field');
  function setV(id,s){ const e=$(id); if(!e) return; e.textContent=s; e.style.fontSize=s.length>10?'14px':(s.length>7?'16px':''); }
  function setK(id,s){ const e=$(id); if(e&&e.previousElementSibling) e.previousElementSibling.textContent=s; }
  function rrect(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
  function txt(t,x,y,size,col,weight,align,maxW){ ctx.textAlign=align||'left'; let s=size; ctx.font=(weight||'')+' '+s+'px sans-serif';
    if(maxW){ while(ctx.measureText(t).width>maxW&&s>8){ s-=0.5; ctx.font=(weight||'')+' '+s+'px sans-serif'; } }
    ctx.fillStyle=col||'#0f172a'; ctx.fillText(t,x,y); }
  function dot(x,y,r,c){ ctx.fillStyle=c; ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.fill(); }
  function line(x1,y1,x2,y2,w,c,dash){ ctx.strokeStyle=c; ctx.lineWidth=w; ctx.lineCap='round'; if(dash) ctx.setLineDash(dash); ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2,y2); ctx.stroke(); if(dash) ctx.setLineDash([]); }
  function arrow(x,y,dx,dy,c,w){ const L=Math.hypot(dx,dy); if(L<3) return; const ux=dx/L, uy=dy/L; line(x,y,x+dx-ux*6,y+dy-uy*6,w||3,c);
    ctx.fillStyle=c; ctx.beginPath(); ctx.moveTo(x+dx,y+dy); ctx.lineTo(x+dx-ux*10-uy*5.5,y+dy-uy*10+ux*5.5); ctx.lineTo(x+dx-ux*10+uy*5.5,y+dy-uy*10-ux*5.5); ctx.closePath(); ctx.fill(); }
  function nf(v){ const r=Math.round(v*100)/100; return (Math.abs(v-r)>1e-9?'約':'')+String(r); }
  function V(){ const m=+$('mass').value, hc=+$('ht').value; return {m:m,hc:hc,T:+$('tm').value,Lc:+$('sl').value,k:+$('lk').value,Wt:m/100,h:hc/100}; }
  function FD(id,v){ const Wt=v.Wt, h=v.h;
    if(id==='move'||id==='combo') return [Wt/2,2*h]; if(id==='move2') return [Wt/4,4*h];
    if(id==='slope') return [Wt*h/(v.Lc/100),v.Lc/100]; if(id==='lever') return [Wt/v.k,v.k*h]; return [Wt,h]; }
  function rowName(id,v){ const n=M.find((q)=>q[0]===id)[1]; if(id==='slope') return n+'（長さ'+v.Lc+'cm）'; if(id==='lever') return n+'（支点からのきょり '+v.k+':1）'; return n; }
  function distName(id){ return id==='slope'?'斜面に沿って引く距離':(id==='lever'?'押し下げる距離':(id==='direct'?'持ち上げる距離':'ひもを引く距離')); }
  // ---------- 描画の部品
  function ceiling(x0,x1){ ctx.fillStyle='#cbd5e1'; ctx.fillRect(x0,12,x1-x0,10); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1; for(let x=x0+4;x<x1;x+=10){ ctx.beginPath(); ctx.moveTo(x,12); ctx.lineTo(x+6,6); ctx.stroke(); } }
  function pulley(x,y,r,fill){ ctx.fillStyle=fill; ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.fill(); ctx.strokeStyle='#475569'; ctx.lineWidth=2; ctx.stroke(); ctx.globalAlpha=0.5; ctx.beginPath(); ctx.arc(x,y,r-5,0,Math.PI*2); ctx.stroke(); ctx.globalAlpha=1; dot(x,y,3.5,'#334155'); }
  function rope(pts){ ctx.strokeStyle='#92400e'; ctx.lineWidth=2.4; ctx.lineJoin='round'; ctx.beginPath(); pts.forEach((q,i)=>{ if(i) ctx.lineTo(q[0],q[1]); else ctx.moveTo(q[0],q[1]); }); ctx.stroke(); }
  function ropeArc(x,y,r,a0,a1,ccw){ ctx.strokeStyle='#92400e'; ctx.lineWidth=2.4; ctx.beginPath(); ctx.arc(x,y,r,a0,a1,!!ccw); ctx.stroke(); }
  function obj(cx,top,v){ ctx.fillStyle='#0e7490'; rrect(cx-OW/2,top,OW,OH,6); ctx.fill(); txt(v.m+'g',cx,top+18,12.5,'#fff','bold','center',OW-6); txt(nf(v.Wt)+'N',cx,top+34,11,'#cffafe','','center',OW-6); }
  function hand(x,y,dx,dy,F){ arrow(x,y,dx*36,dy*36,'#dc2626',3.5); ctx.fillStyle='#fcd34d'; ctx.beginPath(); ctx.arc(x,y,9,0,Math.PI*2); ctx.fill(); ctx.strokeStyle='#b45309'; ctx.lineWidth=1.5; ctx.stroke();
    if(Math.abs(dx)<1e-6) txt(nf(F)+'N',x+12,y+dy*22+4,13,'#dc2626','bold','left'); else txt(nf(F)+'N',x+dx*36+6,y+dy*36+4,13,'#dc2626','bold','left'); }
  function hookLine(x,y1,y2){ line(x,y1,x,y2,2,'#475569'); }
  // ---------- 方法ごとの図（模式図。動く長さは見やすく縮めている）
  function geo(v){ const base=Math.min(120,v.hc*1.2), r={};
    r.direct=base; r.fixed=base; r.move=Math.min(base,58); r.combo=Math.min(base,55); r.move2=Math.min(base,27);
    const ratio=Math.max(1.05,v.Lc/v.hc); r.slope=Math.min(base,150,170/Math.sqrt(ratio*ratio-1)); r.lever=Math.min(base,40); return r; }
  function travel(v){ const g=geo(v), id=mode;
    if(id==='direct') return [0,-1,g.direct]; if(id==='fixed') return [0,1,g.fixed]; if(id==='move') return [0,-1,2*g.move]; if(id==='combo') return [0,1,2*g.combo]; if(id==='move2') return [0,1,4*g.move2];
    if(id==='slope'){ const ratio=Math.max(1.05,v.Lc/v.hc), Hs=g.slope, Lp=Hs*ratio, hz=Math.sqrt(Lp*Lp-Hs*Hs); return [hz/Lp,-Hs/Lp,Lp]; }
    return [0,1,v.k*g.lever]; }
  function drawApp(v){ const g=geo(v), fd=FD(mode,v), F=fd[0], id=mode;
    ctx.fillStyle='#f8fafc'; rrect(4,4,330,290,10); ctx.fill();
    line(10,FY,328,FY,3,'#94a3b8');
    if(id==='direct'){ const top=FY-OH-p*g.direct; obj(166,top,v); hand(166,top-12,0,-1,F); }
    else if(id==='fixed'){ const top=FY-OH-p*g.fixed, px=170, py=56, r=18; ceiling(130,210); hookLine(px,22,py); pulley(px,py,r,'#e2e8f0');
      ropeArc(px,py,r,Math.PI,0); rope([[px-r,py],[px-r,top]]); const hy=100+p*g.fixed; rope([[px+r,py],[px+r,hy]]); obj(px-r,top,v); hand(px+r,hy,0,1,F);
      txt('定滑車',px-r-6,py-6,11,'#475569','bold','right'); }
    else if(id==='move'){ const top=FY-OH-p*g.move, r=18, px=130, py=top-26; ceiling(84,200); obj(px,top,v); hookLine(px,py,top);
      pulley(px,py,r,'#fde68a'); ropeArc(px,py,r,Math.PI,0,true); const hy=165-2*p*g.move; rope([[px-r,22],[px-r,py]]); rope([[px+r,py],[px+r,hy]]); hand(px+r,hy,0,-1,F);
      txt('動滑車',px-r-6,py+4,11,'#92400e','bold','right'); }
    else if(id==='combo'){ const top=FY-OH-p*g.combo, r=18, mx=128, my=top-26, fx=164, fy=56; ceiling(96,210); hookLine(fx,22,fy); obj(mx,top,v); hookLine(mx,my,top);
      pulley(mx,my,r,'#fde68a'); pulley(fx,fy,r,'#e2e8f0'); ropeArc(mx,my,r,Math.PI,0,true); ropeArc(fx,fy,r,Math.PI,0); const hy=112+2*p*g.combo;
      rope([[mx-r,22],[mx-r,my]]); rope([[mx+r,my],[fx-r,fy]]); rope([[fx+r,fy],[fx+r,hy]]); hand(fx+r,hy,0,1,F);
      txt('動滑車',mx-r-6,my+4,11,'#92400e','bold','right'); txt('定滑車',fx,fy+r+14,11,'#475569','bold','center'); }
    else if(id==='move2'){ const d=p*g.move2, top=FY-OH-d, r=16, ax=110, ay=top-22, bx=126, by=150-2*d, cx=158, cy=56; ceiling(80,200); hookLine(cx,22,cy); obj(ax,top,v); hookLine(ax,ay,top);
      pulley(ax,ay,r,'#fde68a'); pulley(bx,by,r,'#fde68a'); pulley(cx,cy,r,'#e2e8f0'); hookLine(bx,by,by+r+7); ctx.fillStyle='#475569'; ctx.fillRect(bx-4,by+r+5,8,4);
      ropeArc(ax,ay,r,Math.PI,0,true); rope([[ax-r,22],[ax-r,ay]]); rope([[ax+r,ay],[bx,by+r+8]]);
      ropeArc(bx,by,r,Math.PI,0,true); rope([[bx-r,22],[bx-r,by]]); rope([[bx+r,by],[cx-r,cy]]); ropeArc(cx,cy,r,Math.PI,0); const hy=96+4*d; rope([[cx+r,cy],[cx+r,hy]]); hand(cx+r,hy,0,1,F);
      txt('動滑車A',ax-r-4,ay+4,10.5,'#92400e','bold','right'); txt('動滑車B',bx-r-4,by+4,10.5,'#92400e','bold','right'); }
    else if(id==='slope'){ const tv=travel(v), ux=tv[0], uy=tv[1], Lp=tv[2], Hs=-uy*Lp, hz=ux*Lp, x0=22, x1=x0+hz, y1=FY-Hs, ang=Math.atan2(uy,ux);
      ctx.fillStyle='#e2e8f0'; ctx.beginPath(); ctx.moveTo(x0,FY); ctx.lineTo(x1,y1); ctx.lineTo(x1,FY); ctx.closePath(); ctx.fill(); ctx.fillRect(x1,y1,326-x1,FY-y1);
      line(x0,FY,x1,y1,3,'#94a3b8'); line(x1,y1,326,y1,3,'#94a3b8');
      line(x1+14,FY-2,x1+14,y1+2,1.2,'#64748b',[3,3]); txt('高さ '+v.hc+'cm',x1+18,(FY+y1)/2+4,11,'#475569','bold','left');
      ctx.save(); ctx.translate(x0+hz/2,FY-Hs/2); ctx.rotate(ang); txt('斜面の長さ '+v.Lc+'cm',0,16,11,'#475569','bold','center'); ctx.restore();
      const s=p*Lp, bw=40, bh=26, px=x0+ux*s, py=FY+uy*s;
      ctx.save(); ctx.translate(px,py); ctx.rotate(ang); ctx.fillStyle='#0e7490'; rrect(0,-bh,bw,bh,5); ctx.fill(); txt(v.m+'g',bw/2,-bh/2+4,11,'#fff','bold','center',36); ctx.restore();
      const ax=px+ux*bw+uy*bh/2, ay=py+uy*bw-ux*bh/2, hx=ax+ux*34, hy=ay+uy*34; rope([[ax,ay],[hx,hy]]); hand(hx,hy,ux,uy,F); }
    else { const k=v.k, a=52, fx=100, fy=150, s0=g.lever/(2*a), sn=s0*(1-2*p), cs=Math.sqrt(1-sn*sn);
      ctx.fillStyle='#94a3b8'; ctx.beginPath(); ctx.moveTo(fx,fy); ctx.lineTo(fx-16,FY); ctx.lineTo(fx+16,FY); ctx.closePath(); ctx.fill();
      const lx=fx-a*cs, ly=fy+a*sn, rx=fx+k*a*cs, ry=fy-k*a*sn; line(lx-8*cs,ly+8*sn,rx,ry,7,'#a16207'); dot(fx,fy,4,'#334155');
      obj(lx,ly-OH-3,v); hand(rx,ry-4,0,1,F); txt('支点',fx+12,fy+24,11,'#334155','bold','left'); txt('作用点',lx,ly+18,10.5,'#475569','','center'); txt('力点',rx-12,ry+20,10.5,'#475569','','right'); }
    const d=fd[1]*p*100;
    txt('上がった高さ '+Math.round(p*v.hc)+' cm',160,287,12,'#0e7490','bold','right',150); txt('／',167,287,12,'#94a3b8','','center');
    txt((id==='direct'?'手を動かした距離':distName(id))+' '+Math.round(d)+' cm',174,287,12,'#dc2626','bold','left',152); }
  // ---------- 右の数値と「力×距離」の長方形
  function drawPanel(v){ const id=mode, fd=FD(id,v), F=fd[0], d=fd[1], Wk=F*d, P=Wk/v.T;
    ctx.fillStyle='#fff'; rrect(340,4,296,290,10); ctx.fill(); ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; ctx.stroke();
    txt(rowName(id,v),352,28,16,'#0f172a','bold','left',272);
    txt('必要な力 F ＝ '+nf(F)+' N',352,54,15,'#dc2626','bold','left',272);
    txt(distName(id)+' d ＝ '+nf(d)+' m',352,76,13.5,'#334155','bold','left',272);
    txt('仕事 ＝ '+nf(F)+' N × '+nf(d)+' m ＝ '+nf(Wk)+' J',352,100,15,'#0e7490','bold','left',272);
    // 長方形：横＝距離、たて＝力
    let dmax=v.h; M.forEach((q)=>{ dmax=Math.max(dmax,FD(q[0],v)[1]); });
    const X0=378, X1=620, Y0=120, Y1=228, sx=(X1-X0)/dmax, sy=(Y1-Y0)/v.Wt;
    line(X0,Y1,X1+6,Y1,1.5,'#94a3b8'); line(X0,Y0-4,X0,Y1,1.5,'#94a3b8');
    txt('力',X0-4,Y0-6,10,'#64748b','','right'); txt(nf(v.Wt)+'N',X0-4,Y0+4,10,'#64748b','','right'); txt('0',X0-4,Y1+4,10,'#64748b','','right'); txt('→ 距離',X1+8,Y1-5,10,'#64748b','','right');
    ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1.2; ctx.setLineDash([4,3]); ctx.strokeRect(X0,Y0,v.h*sx,v.Wt*sy); ctx.setLineDash([]);
    ctx.fillStyle='rgba(14,116,144,.28)'; ctx.fillRect(X0,Y1-F*sy,d*sx*p,F*sy);
    ctx.strokeStyle='#0e7490'; ctx.lineWidth=2; ctx.strokeRect(X0,Y1-F*sy,d*sx,F*sy);
    txt(nf(d)+'m',Math.min(X0+d*sx,X1-6),Y1+14,10,'#0e7490','bold','center'); if(Math.abs(d-v.h)*sx>34) txt(nf(v.h)+'m',X0+v.h*sx,Y1+14,10,'#94a3b8','','center');
    txt('面積＝仕事 '+nf(Wk)+' J',X0+Math.max(d*sx,96)/2+2,Y1-F*sy/2+(F*sy<22?-F*sy/2-6:4),11.5,'#0e7490','bold','center',200);
    if(id!=='direct'&&id!=='fixed') txt('点線＝直接持ち上げるとき',X1,Y0+4,10,'#64748b','','right');
    txt('仕事率 ＝ '+nf(Wk)+' J ÷ '+v.T+' 秒 ＝ '+nf(P)+' W',352,256,14,'#7c3aed','bold','left',272);
    const msg=run?'⏱ 経過 '+el.toFixed(1)+' / '+v.T+' 秒':(finished?'✓ '+v.T+'秒で持ち上げた（仕事率 '+nf(P)+' W）':(p>0?'手で動かし中（時間は計らない）':'▶「持ち上げる」または図をドラッグ'));
    txt(msg,352,280,12,run?'#15803d':'#475569','bold','left',272); }
  // ---------- 下の表
  function drawTable(v){ const cols=[16,300,436,560];
    ctx.fillStyle='#ecfeff'; ctx.fillRect(6,TY,628,22);
    ['持ち上げ方（タップで切りかえ）','必要な力','動かす距離','仕事（力×距離）'].forEach((h,i)=>txt(h,cols[i],TY+15,11.5,'#155e75','bold',i?'center':'left',i?120:270));
    M.forEach((q,j)=>{ const y=TY+22+j*RH, fd=FD(q[0],v), on=q[0]===mode;
      if(on){ ctx.fillStyle='#fef3c7'; ctx.fillRect(6,y,628,RH); } else if(j%2){ ctx.fillStyle='#f8fafc'; ctx.fillRect(6,y,628,RH); }
      line(6,y+RH,634,y+RH,1,'#e5e7eb');
      txt((on?'▶ ':'')+rowName(q[0],v),cols[0],y+16,12.5,'#0f172a',on?'bold':'','left',270);
      txt(nf(fd[0])+' N',cols[1],y+16,13,'#dc2626',on?'bold':'','center',120); txt(nf(fd[1])+' m',cols[2],y+16,13,'#334155',on?'bold':'','center',120);
      txt(nf(fd[0]*fd[1])+' J',cols[3],y+16,13,'#15803d','bold','center',120); });
    const yb=TY+22+M.length*RH;
    txt('→ どの方法でも仕事は '+nf(v.Wt*v.h)+' J で同じ（仕事の原理）',320,yb+19,14,'#15803d','bold','center',620);
    txt('滑車・ひも・棒の質量と摩擦は考えない。100gの物体にはたらく重力＝1N として計算',320,yb+35,11,'#64748b','','center',620); }
  function draw(){ const v=V(); ctx.fillStyle='#fff'; ctx.fillRect(0,0,W,H); drawApp(v); drawPanel(v); drawTable(v); }
  function update(){ const v=V(), fd=FD(mode,v), Wk=fd[0]*fd[1];
    setK('s2',distName(mode)); setV('s1',nf(fd[0])+' N'); setV('s2',nf(fd[1])+' m'); setV('s3',nf(Wk)+' J'); setV('s4',nf(Wk/v.T)+' W');
    $('go').textContent='▶ 持ち上げる（'+v.T+'秒）';
    setShare('【仕事の原理】'+v.m+'gの物体を'+v.hc+'cm持ち上げる：'+rowName(mode,v)+'なら力'+nf(fd[0])+'N・'+nf(fd[1])+'m動かして仕事'+nf(Wk)+'J。直接でも動滑車でも斜面でも仕事は同じ'+nf(v.Wt*v.h)+'J｜シミュラボ'); }
  function setMode(m){ mode=m; $('meth').value=m; fld('sl').style.display=m==='slope'?'':'none'; fld('lk').style.display=m==='lever'?'':'none'; p=0; run=false; el=0; finished=false; update(); }
  function fixSlope(){ const h=+$('ht').value, s=$('sl'); s.min=String(h+10); if(+s.value<h+10) s.value=String(h+10); const l=$('slL'); if(l) l.textContent=s.value+'cm'; }
  ['mass','ht','tm','sl','lk'].forEach((id)=>$(id).addEventListener('input',()=>{ if(id==='ht') fixSlope(); if(id!=='tm'){ p=0; run=false; el=0; finished=false; } update(); }));
  $('meth').addEventListener('change',()=>setMode($('meth').value));
  $('go').addEventListener('click',()=>{ p=0; el=0; run=true; finished=false; });
  $('down').addEventListener('click',()=>{ p=0; el=0; run=false; finished=false; });
  cv.addEventListener('pointerdown',(e)=>{ const q=cpos(cv,e), x=q[0]/dpr, y=q[1]/dpr;
    if(y>=TY+22&&y<TY+22+M.length*RH){ const j=Math.floor((y-TY-22)/RH); e.preventDefault(); setMode(M[j][0]); return; }
    if(x<=334&&y<=294){ e.preventDefault(); run=false; finished=false; g0=[x,y,p]; grab=true; try{ cv.setPointerCapture(e.pointerId); }catch(er){} } });
  cv.addEventListener('pointermove',(e)=>{ if(!grab) return; const q=cpos(cv,e), x=q[0]/dpr, y=q[1]/dpr, tv=travel(V()); p=clamp(g0[2]+((x-g0[0])*tv[0]+(y-g0[1])*tv[1])/tv[2],0,1); });
  const endG=()=>{ grab=false; }; cv.addEventListener('pointerup',endG); cv.addEventListener('pointercancel',endG);
  fixSlope(); setMode('move');
  let last=performance.now();
  function loop(now){ const dt=Math.min(0.05,Math.max(0,(now-last)/1000)); last=now;
    if(run){ const T=+$('tm').value; el=Math.min(T,el+dt); p=el/T; if(el>=T){ run=false; finished=true; p=1; } }
    draw(); requestAnimationFrame(loop); }
  draw(); requestAnimationFrame(loop);
'''

sim(slug="kassha-shigoto", cat="rika", emoji="🏗️", score=76,
    title="滑車と仕事の原理シミュレーター（仕事・仕事率）",
    title_tag="仕事の原理・滑車のシミュレーター｜定滑車・動滑車・斜面・てこで仕事と仕事率を計算（中3理科 仕事とエネルギー）",
    meta_desc="中3理科「仕事とエネルギー」の仕事の原理をブラウザで確かめられます。物体の質量と高さを決めて、直接・定滑車・動滑車・動滑車2個・斜面・てこを切りかえると、必要な力（N）・動かす距離（m）・仕事（J）が表に並び、仕事はどれも同じに。かかった時間から仕事率（W）も計算。",
    og_title="滑車と仕事の原理シミュレーター（中3 仕事とエネルギー）",
    og_desc="動滑車なら力は半分、でもひもを引く距離は2倍。直接・定滑車・動滑車・斜面・てこで仕事（J）が同じになることを確かめる。仕事率（W）も。",
    card_desc="定滑車・動滑車・斜面・てこで、力は小さくなっても距離が長くなり、仕事は同じ。仕事率も計算。",
    lead="物体の質量と持ち上げる高さを決め、持ち上げ方（直接・定滑車・動滑車・斜面・てこ など）を切りかえると、必要な力・動かす距離・仕事が表に並びます。かかった時間を決めると、仕事率も計算されます。",
    model="中3 仕事とエネルギー（仕事の原理・仕事率）", level="中学3年",
    unit="中学校 第1分野（5）ア（ｳ）力学的エネルギー ㋐仕事とエネルギー",
    canvas=canvas(640, 524, light=True),
    controls=select("meth", "持ち上げ方", [(k, n) for k, n in [("move", "動滑車"), ("direct", "直接持ち上げる"), ("fixed", "定滑車"), ("combo", "定滑車＋動滑車"), ("move2", "動滑車2個（＋定滑車）"), ("slope", "斜面"), ("lever", "てこ")]])
             + slider("mass", "物体の質量", 100, 3000, MASS0, 100, "{v}g") + slider("ht", "持ち上げる高さ", 10, 100, H0, 10, "{v}cm")
             + slider("tm", "持ち上げるのにかかる時間", 1, 20, T0, 1, "{v}秒")
             + slider("sl", "斜面の長さ", 20, 300, 100, 10, "{v}cm") + slider("lk", "てこ：力点のきょり（作用点の何倍）", 2, 4, 2, 1, "{v}倍"),
    buttons=btn("go", "▶ 持ち上げる（5秒）", True) + btn("down", "↺ 下ろす"),
    stats=stats([("s1", "必要な力", True), ("s2", "ひもを引く距離", False), ("s3", "仕事", False), ("s4", "仕事率", False)]),
    legend="赤い矢印が手で加える力です。右の長方形は、たて＝力、横＝動かす距離で、面積が仕事を表します（点線は直接持ち上げるとき）。下の表の行をタップすると持ち上げ方が切りかわり、図を指でドラッグすると手で動かせます。滑車・ひも・棒の質量と摩擦は考えていません。100gの物体にはたらく重力を1Nとしています。図は模式図です。",
    article=KASSHA_ARTICLE, faqs=KASSHA_FAQS,
    rel=[("teko-tsuriai", "⚖️", "てこのつり合いシミュレーター"), ("kiroku-timer", "🛒", "記録タイマーと台車の運動シミュレーター"),
         ("kamu-pulley", "🔩", "カムとベルト・プーリのシミュレーター"), ("gears", "⚙️", "歯車シミュレーター"), ("bane-nobi", "🌀", "ばねののびと力の大きさ")],
    js=KASSHA_JS)
