# -*- coding: utf-8 -*-
"""理科の授業向け：高校物理（物理「円運動と単振動」＝単振動／物理基礎「波」＝うなり・定常波・弦と気柱の固有振動）"""
import math
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

MEXT_KOU = "https://www.mext.go.jp/a_menu/shotou/new-cs/1407074.htm"
G = 9.8


# ---- 記事の数値（Python で計算して埋め込む）
def _agm(a, b):
    for _ in range(60):
        a, b = (a + b) / 2, math.sqrt(a * b)
    return a
def _T0(L): return 2 * math.pi * math.sqrt(L / G)
def _ratio(th): return 1 / _agm(1, math.cos(math.radians(th) / 2))   # 大きい振れ角の周期 T / 近似式 T0（楕円積分）
def _f2(v): return "%.2f" % v
def _f3(v): return "%.3f" % v

SPRING_TABLE = T([["%.2f kg" % m] + ["%s s" % _f2(2 * math.pi * math.sqrt(m / k)) for k in (10, 20, 40, 80)]
                  for m in (0.10, 0.25, 0.50, 1.00, 2.00)],
                 ["おもりの質量 m", "k＝10 N/m", "k＝20 N/m", "k＝40 N/m", "k＝80 N/m"])
PEND_TABLE = T([["%.2f m" % L, "%s s" % _f2(_T0(L)), "%s Hz" % _f2(1 / _T0(L))] for L in (0.25, 0.50, 1.00, 1.50, 2.00)],
               ["振り子の長さ L", "周期 T＝2π√(L/g)", "振動数 f＝1/T"])
BIG_TABLE = T([["%d°" % th, "%.4f" % _ratio(th), "＋%.2f%%" % ((_ratio(th) - 1) * 100), "%s s" % _f3(_T0(1.0) * _ratio(th))]
               for th in (5, 10, 20, 30, 45, 60, 90)],
              ["振れ角 θ₀", "T÷T₀", "近似式からのずれ", "長さ1.00mの振り子の周期（T₀＝%s s）" % _f3(_T0(1.0))])

# ============================================================ 1 単振動
TAN_ARTICLE = "<h2>このシミュレーションでわかること</h2>\n" + P(
    "単振動は、<b>等速円運動をする点を直径上に正射影した運動</b>です。変位 x、速度 v、加速度 a は同じ周期で振動し、v は x より1/4周期、a は x と半周期ずれます。"
    "周期は、ばね振り子が <b>T＝2π√(m/k)</b>、単振り子が <b>T＝2π√(L/g)</b>（振れ角が小さいとき）で、どちらも<b>振幅によらない</b>のが特徴です。") + '''
<p>高等学校「物理」の「(1) 様々な運動」(ｳ)円運動と単振動 ㋑単振動（学習指導要領 平成30年告示）で学ぶ内容です。内容の取扱いでは「単振動をする物体の変位，速度，加速度及び復元力」を扱い、具体例として「ばね振り子と単振り子」を扱うことになっています。解説では、単振動を等速円運動と関連付けて扱うことや、単振り子の長さと周期との関係を調べる実験が例として挙げられています。このシミュレーションは、その作図と実験を画面の上で再現します。</p>
<p>ばね定数 k・質量 m・振幅 A を変えると、おもりの単振動と、それに対応する等速円運動（上の円）が同時に動き、x・v・a の時間変化のグラフと、運動エネルギー・弾性力による位置エネルギーの棒グラフがその場で描かれます。単振り子に切り替えると、近似式 T₀＝2π√(L/g) どおりに動く振り子（灰色）と、運動方程式を数値積分して求めた実際の振り子を重ねて比べられます。</p>
<h2>授業での使い方</h2>
<ul>
<li><b>導入</b>：ばね振り子を動かし、上の円をまわる点の「影」（正射影）が、おもりとぴったり同じ動きをすることを観察させます。解説にある「投影装置などによる観察」の代わりになります。おもりは指やペンでつかんで引っぱり、はなして振動させることもできます。</li>
<li><b>展開</b>：x・v・a のグラフを縦にならべ、山の位置のずれ（位相のずれ）を読み取らせます。グラフの縦の点線は1/4周期ごとです。振幅を変えても周期が変わらないこと、質量を4倍にすると周期が2倍になることを確かめます。単振り子に切り替えて、長さと周期の関係を調べる実験の予想や結果の確認にも使えます。</li>
<li><b>まとめ</b>：エネルギーの棒グラフで、運動エネルギーと位置エネルギーの和が一定であること（物理基礎の力学的エネルギー保存）を確かめます。単振り子の振れ角を大きくすると、近似式の振り子と実際の振り子が少しずつずれていき、T＝2π√(L/g) が「振れ角が小さいときの式」であることがわかります。</li>
</ul>
<p>生徒への問いの例：</p>
<ol>
<li>おもりの速さが最大になるのはどの位置でしょう。そのとき、加速度と復元力はどうなっているでしょう。</li>
<li>おもりの質量を4倍にすると、周期は何倍になるでしょう。ばね定数を4倍にしたときはどうでしょう。</li>
<li>単振り子の振れ角を60°にすると、周期は T₀＝2π√(L/g) より長くなるでしょうか、短くなるでしょうか。それはなぜでしょう。</li>
</ol>
<h2>しくみ・解説</h2>
<h3>用語の意味</h3>
<ul>
<li><b>単振動</b>とは、等速円運動をする点を直径上に正射影したときに見られる、直線上の往復運動です。</li>
<li><b>復元力</b>とは、物体をつり合いの位置にもどす向きにはたらき、大きさが変位に比例する力（F＝−Kx、K は正の定数）です。</li>
<li><b>振幅 A</b> とは、つり合いの位置（振動の中心）から振動の端までの距離です。</li>
<li><b>周期 T</b> とは1回の振動にかかる時間〔s〕で、<b>振動数 f</b> とは1秒あたりの振動の回数〔Hz〕です（f＝1/T）。</li>
<li><b>角振動数 ω</b> とは、単振動に対応する等速円運動の角速度〔rad/s〕で、ω＝2π/T＝2πf です。</li>
<li><b>位相</b>とは、振動がどの段階にあるかを表す角 ωt（初期位相を含めて ωt＋θ₀）です。</li>
</ul>
<h3>変位・速度・加速度の式と位相のずれ</h3>
''' + N("x＝A sin ωt　　v＝Aω cos ωt　　a＝−Aω² sin ωt＝−ω²x<br>速さの最大値 v<sub>max</sub>＝Aω（つり合いの位置）　加速度の大きさの最大値 a<sub>max</sub>＝Aω²（振動の端）") + '''
<p>振動の中心を時刻0に正の向きに通過するとき、変位は x＝A sin ωt と表せます。速度 v は x より位相が π/2（1/4周期）進み、加速度 a は x と逆位相（位相が π ずれる）です。a＝−ω²x なので、加速度はいつも変位と逆向きで、変位に比例します。このシミュレーションでは、おもりを端まで引いてからはなすので、x＝A cos ωt（初期位相 π/2）のグラフになります。</p>
''' + T([["つり合いの位置（x＝0）", "最大（Aω）", "0", "0"],
          ["振動の端（x＝±A）", "0", "最大（Aω²）", "最大（kA）"]],
         ["おもりの位置", "速さ", "加速度の大きさ", "復元力の大きさ"]) + '''
<h3>ばね振り子と単振り子の周期</h3>
''' + N("ばね振り子：運動方程式 ma＝−kx と a＝−ω²x をくらべて ω＝√(k/m)　→　<b>T＝2π√(m/k)</b><br>"
        "単振り子：復元力 −mg sinθ ≒ −(mg/L)x（θ が小さいとき）→ ω＝√(g/L)　→　<b>T＝2π√(L/g)</b>") + '''
<p><b>計算例1（ばね振り子）</b>：k＝20 N/m、m＝0.50 kg のとき、T＝2π√(0.50÷20)＝2π×0.158＝<b>0.993 s</b>。振幅 A＝0.10 m なら、ω＝√(20÷0.50)＝6.32 rad/s、速さの最大値 Aω＝0.632 m/s、加速度の大きさの最大値 Aω²＝4.00 m/s²、力学的エネルギー ½kA²＝0.100 J です（このシミュレーションの初期設定）。</p>
<p><b>計算例2（単振り子）</b>：長さ L＝1.00 m、g＝9.8 m/s² のとき、T＝2π√(1.00÷9.8)＝<b>2.01 s</b>。周期を2倍にするには、長さを4倍にします。周期の式には、おもりの質量も振幅も入っていません。</p>
<p>ばね振り子の周期の早見表（T＝2π√(m/k)）：</p>
''' + SPRING_TABLE + '''
<p>単振り子の周期の早見表（g＝9.8 m/s²、振れ角が小さいとき）：</p>
''' + PEND_TABLE + '''
<h3>振れ角が大きいときの単振り子（近似のずれ）</h3>
<p>T＝2π√(L/g) は、sinθ≒θ と近似できる「振れ角が小さいとき」の式です。振れ角が大きいと、復元力 mg sinθ が近似の mgθ より小さくなるので、周期は少し長くなります。このシミュレーションでは、運動方程式 d²θ/dt²＝−(g/L) sinθ をルンゲ＝クッタ法（4次）で数値積分して実際の周期を求め、近似式の値とくらべています（数値積分の結果は、楕円積分による厳密な値と小数第4位まで一致することを確かめています）。</p>
''' + BIG_TABLE + '''
<p>振れ角10°では0.2%ほど、30°では1.7%ほどのずれなので、授業の実験（振れ角10°前後）では近似式で十分です。</p>
<h3>単振動の力学的エネルギー</h3>
''' + N("ばね振り子：½mv²＋½kx²＝½kA²（一定）<br>単振り子：½mv²＋mgL(1−cosθ)＝mgL(1−cosθ₀)（一定）") + '''
<p>おもりが端にあるとき運動エネルギーは0で位置エネルギーが最大、つり合いの位置を通るとき位置エネルギーが0で運動エネルギーが最大です。</p>
<h3>このシミュレーションで単純にしていること</h3>
<ul>
<li>摩擦や空気の抵抗は考えていません（振幅はへりません）。ばねと糸の質量も考えていません。重力加速度は g＝9.8 m/s² です。</li>
<li>ばね振り子は、なめらかな水平面の上で振動するものとしています。鉛直につるしたばね振り子も、つり合いの位置を中心に同じ周期 T＝2π√(m/k) で単振動します。</li>
<li>単振り子は、近似式の周期で3周期分（3T₀）動くごとに、最初の位置からやり直して表示します。近似式の振り子とのずれがたまっていく様子を、くり返し見るためです。</li>
<li>グラフの縦の目もりは、それぞれの量の最大値に合わせています（x・v・a の大きさを、そのまま比べるものではありません）。</li>
</ul>
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「高等学校学習指導要領（平成30年告示）解説 理科編 理数編」物理 (1) 様々な運動 (ｳ)円運動と単振動（<a href="''' + MEXT_KOU + '''" target="_blank" rel="noopener">文部科学省 学習指導要領のページ</a>）</li>
<li>高等学校「物理」の教科書（数研出版、東京書籍、啓林館、第一学習社など）の単振動の章</li>
</ul>
'''

TAN_FAQS = [
    ("単振動の周期は、なぜ振幅によらないのですか？", "復元力が変位に比例する（F＝−kx）ので、振幅を2倍にすると復元力も2倍になり、速さも2倍になります。進む距離が2倍でも速さが2倍なので、1往復にかかる時間は変わりません。式でも T＝2π√(m/k) に振幅 A は入っていません。"),
    ("ばね振り子の周期の求め方は？", "T＝2π√(m/k)（m：おもりの質量〔kg〕、k：ばね定数〔N/m〕）で求めます。例えば k＝20 N/m、m＝0.50 kg なら T＝2π√(0.50÷20)≒0.99 s です。質量を4倍にすると周期は2倍、ばね定数を4倍にすると周期は1/2倍になります。"),
    ("単振り子の周期の式 T＝2π√(L/g) は、いつでも使えますか？", "振れ角が小さいとき（sinθ≒θ と近似できるとき）の式です。振れ角が大きいと実際の周期は少し長くなり、30°で約1.7%、60°で約7.3%、90°で約18%長くなります。授業の実験のように振れ角が10°前後なら、ずれは0.2%ほどです。"),
    ("単振動で、速さが最大になる位置と、加速度が最大になる位置はどこですか？", "速さが最大（Aω）になるのはつり合いの位置（x＝0）で、そのとき加速度と復元力は0です。加速度の大きさが最大（Aω²）になるのは振動の端（x＝±A）で、そのとき速さは0です。"),
    ("鉛直につるしたばね振り子の周期は、水平のときと同じですか？", "同じです。重力は、つり合いの位置（ばねが mg/k だけのびた位置）をずらすだけで、そこからの変位に対してはたらく力は −kx のままです。そのため周期は T＝2π√(m/k) になります。"),
    ("単振動と等速円運動は、どのような関係ですか？", "半径 A・角速度 ω の等速円運動をする点を、直径上に正射影（真横や真上から光を当てたときの影）すると、振幅 A・角振動数 ω の単振動になります。単振動の速度・加速度は、円運動の速度・向心加速度を正射影したものです。"),
]

TAN_JS = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const G=9.8, TAU=Math.PI*2, CX=250, CY=96, SX=400, PVX=240, PVY=26, LS=100, GX0=82, GX1=626;
  let mode='spring', t=0, run=true, last=null, sg=1, drag=false, P={};
  const fld=(id)=>$(id).closest('.field');
  function lab(id,s){ const e=$(id); if(e&&e.previousElementSibling) e.previousElementSibling.textContent=s; }
  function fx(v,d){ const s=v.toFixed(d); return (+s===0)?(0).toFixed(d):s; }
  function sn(v,d){ const s=fx(v,d); return (+s>0?'+':'')+s.replace('-','−'); }
  function fJ(v){ return v>=1?v.toFixed(2):(v>=0.1?v.toFixed(3):v.toFixed(4)); }
  function txt(s,x,y,col,sz,b,al){ ctx.fillStyle=col; ctx.font=(b?'bold ':'')+sz+'px sans-serif'; ctx.textAlign=al||'left'; ctx.fillText(s,x,y); }
  function rr(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
  function arrow(x1,y1,x2,y2,col,lw){ const L=Math.hypot(x2-x1,y2-y1); if(L<4) return; ctx.strokeStyle=col; ctx.fillStyle=col; ctx.lineWidth=lw||2.5; ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2,y2); ctx.stroke();
    const a=Math.atan2(y2-y1,x2-x1), h=Math.min(10,L*0.6); ctx.beginPath(); ctx.moveTo(x2,y2); ctx.lineTo(x2-h*Math.cos(a-0.45),y2-h*Math.sin(a-0.45)); ctx.lineTo(x2-h*Math.cos(a+0.45),y2-h*Math.sin(a+0.45)); ctx.closePath(); ctx.fill(); ctx.lineWidth=1; }
  // 単振り子の運動方程式 θ''=-(g/L)sinθ を RK4 で半周期ぶん積分し、表にしておく（後半は対称性 θ(t+T/2)=-θ(t) を使う）
  function pendTable(L,th0,T0){ const f=(th)=>-(G/L)*Math.sin(th), dt=T0/4000; let th=th0, om=0, tt=0, half=T0/2; const ths=[th], oms=[om];
    for(let i=0;i<20000;i++){ const k1t=om, k1o=f(th), k2t=om+dt/2*k1o, k2o=f(th+dt/2*k1t), k3t=om+dt/2*k2o, k3o=f(th+dt/2*k2t), k4t=om+dt*k3o, k4o=f(th+dt*k3t);
      const nth=th+dt/6*(k1t+2*k2t+2*k3t+k4t), nom=om+dt/6*(k1o+2*k2o+2*k3o+k4o);
      ths.push(nth); oms.push(nom);
      if(om<0&&nom>=0){ half=tt+dt*om/(om-nom); break; }
      th=nth; om=nom; tt+=dt; }
    return {T:2*half, half:half, dt:dt, ths:ths, oms:oms}; }
  function pend(tau){ const r=P.tab; let s=1; tau=((tau%r.T)+r.T)%r.T; if(tau>=r.half){ tau-=r.half; s=-1; }
    const u=tau/r.dt, n=r.ths.length-1, i=Math.min(Math.floor(u),n), j=Math.min(i+1,n), fr=u-Math.floor(u);
    return [s*(r.ths[i]+(r.ths[j]-r.ths[i])*fr), s*(r.oms[i]+(r.oms[j]-r.oms[i])*fr)]; }
  function params(){ mode=$('mode').value; const m=+$('m').value;
    if(mode==='spring'){ const k=+$('k').value, A=+$('A').value/100, w=Math.sqrt(k/m); P={m:m,k:k,A:A,w:w,T:TAU/w,E:0.5*k*A*A}; }
    else { const L=+$('L').value, th0=+$('th').value*Math.PI/180, w0=Math.sqrt(G/L), T0=TAU/w0, r=pendTable(L,th0,T0);
      P={m:m,L:L,th0:th0,w0:w0,T0:T0,T:r.T,tab:r,E:m*G*L*(1-Math.cos(th0)),vmax:Math.sqrt(2*G*L*(1-Math.cos(th0)))}; }
    ['k','A'].forEach((id)=>{ fld(id).style.display=mode==='spring'?'':'none'; });
    ['L','th'].forEach((id)=>{ fld(id).style.display=mode==='spring'?'none':''; });
    showStats(); }
  function showStats(){
    if(mode==='spring'){ lab('sT','周期 T＝2π√(m/k)'); lab('sF','振動数 f＝1/T'); lab('sV','速さの最大値 Aω'); lab('sA','加速度の大きさの最大値 Aω²');
      setStat('sT',P.T.toFixed(3)+' s'); setStat('sF',(1/P.T).toFixed(3)+' Hz'); setStat('sV',(P.A*P.w).toFixed(3)+' m/s'); setStat('sA',(P.A*P.w*P.w).toFixed(2)+' m/s²');
      setShare('【単振動】ばね定数'+P.k+'N/m・質量'+P.m.toFixed(2)+'kgのばね振り子の周期は T＝2π√(m/k)＝'+P.T.toFixed(3)+'秒。振幅'+Math.round(P.A*100)+'cmを変えても周期は同じ｜シミュラボ'); }
    else { const d=(P.T/P.T0-1)*100;
      lab('sT','周期 T₀（近似式 2π√(L/g)）'); lab('sF','周期 T（数値積分）'); lab('sV','近似式とのずれ'); lab('sA','速さの最大値');
      setStat('sT',P.T0.toFixed(3)+' s'); setStat('sF',P.T.toFixed(3)+' s'); setStat('sV','+'+d.toFixed(2)+' %'); setStat('sA',P.vmax.toFixed(2)+' m/s');
      setShare('【単振り子】長さ'+P.L.toFixed(2)+'m・振れ角'+Math.round(P.th0*180/Math.PI)+'°の周期は'+P.T.toFixed(3)+'秒。近似式 2π√(L/g)＝'+P.T0.toFixed(3)+'秒より'+d.toFixed(2)+'%長い｜シミュラボ'); } }
  function sst(tt){ const ph=P.w*tt, x=sg*P.A*Math.cos(ph), v=-sg*P.A*P.w*Math.sin(ph); return {x:x,v:v,a:-P.w*P.w*x,ph:ph}; }
  function pst(tt){ const tp=((tt%(3*P.T0))+3*P.T0)%(3*P.T0), q=pend(tp); return {tp:tp,th:sg*q[0],om:sg*q[1],tha:sg*P.th0*Math.cos(P.w0*tp)}; }
  function panel(lines){ ctx.fillStyle='#f0fdfa'; rr(474,10,156,240,10); ctx.fill(); ctx.strokeStyle='#99f6e4'; ctx.stroke();
    lines.forEach((l,i)=>txt(l[0],484,32+i*23.5,l[1]||'#0f172a',l[2]||13,!!l[3])); }
  function drawSpring(){ const s=sst(t), R=P.A*SX, xp=CX+s.x*SX, ph=s.ph+(sg<0?Math.PI:0), pm=((ph%TAU)+TAU)%TAU;
    txt('等速円運動（半径 A・角速度 ω）',12,20,'#6d28d9',13,true);
    ctx.strokeStyle='#c4b5fd'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.arc(CX,CY,R,0,TAU); ctx.stroke(); ctx.lineWidth=1;
    ctx.setLineDash([4,4]); ctx.strokeStyle='#cbd5e1'; ctx.beginPath(); ctx.moveTo(CX-R-16,CY); ctx.lineTo(CX+R+16,CY); ctx.stroke(); ctx.setLineDash([]);
    const qx=CX+R*Math.cos(ph), qy=CY-R*Math.sin(ph);
    ctx.strokeStyle='#a78bfa'; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(CX,CY,15,0,-pm,true); ctx.stroke(); ctx.lineWidth=1;
    if(R>40) txt('ωt',CX+24*Math.cos(pm/2)-6,CY-24*Math.sin(pm/2)+5,'#7c3aed',12,true);
    ctx.strokeStyle='#7c3aed'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.moveTo(CX,CY); ctx.lineTo(qx,qy); ctx.stroke(); ctx.lineWidth=1;
    ctx.fillStyle='#0f172a'; ctx.beginPath(); ctx.arc(CX,CY,2.5,0,TAU); ctx.fill();
    ctx.setLineDash([5,4]); ctx.strokeStyle='#7c3aed'; ctx.beginPath(); ctx.moveTo(qx,qy); ctx.lineTo(qx,190); ctx.stroke(); ctx.setLineDash([]);
    ctx.fillStyle='#7c3aed'; ctx.beginPath(); ctx.arc(qx,qy,6,0,TAU); ctx.fill();
    txt('正射影',Math.min(qx+6,420),Math.max(qy+18,(qy+190)/2),'#7c3aed',12,true);
    // 床・壁・ばね・おもり
    ctx.fillStyle='#cbd5e1'; ctx.fillRect(14,232,452,5); ctx.fillStyle='#94a3b8'; ctx.fillRect(14,170,10,62);
    ctx.strokeStyle='#64748b'; for(let y=174;y<232;y+=9){ ctx.beginPath(); ctx.moveTo(14,y+8); ctx.lineTo(22,y); ctx.stroke(); }
    const x1=24, x2=xp-24, n=14; ctx.strokeStyle='#475569'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(x1,212); const a=x1+8, b=x2-6; ctx.lineTo(a,212);
    for(let i=0;i<n;i++){ ctx.lineTo(a+(b-a)*(i+0.5)/n, 212+(i%2?9:-9)); } ctx.lineTo(b,212); ctx.lineTo(x2,212); ctx.stroke(); ctx.lineWidth=1;
    ctx.setLineDash([2,3]); ctx.strokeStyle='#64748b'; ctx.beginPath(); ctx.moveTo(CX,184); ctx.lineTo(CX,242); ctx.stroke(); ctx.setLineDash([]);
    [[CX-R,'−A'],[CX,'O'],[CX+R,'+A']].forEach((q)=>{ ctx.strokeStyle='#475569'; ctx.beginPath(); ctx.moveTo(q[0],237); ctx.lineTo(q[0],243); ctx.stroke(); txt(q[1],q[0],252,'#475569',12,true,'center'); });
    ctx.fillStyle='#0e7490'; rr(xp-24,192,48,40,6); ctx.fill(); txt('m',xp,218,'#fff',15,true,'center');
    const vm=P.A*P.w; arrow(xp,184,xp+s.v/vm*58,184,'#2563eb',3); if(Math.abs(s.v)/vm>0.15) txt('v',xp+s.v/vm*58+(s.v>0?6:-14),180,'#2563eb',13,true);
    arrow(xp,212,xp-s.x/P.A*58,212,'#dc2626',3); if(Math.abs(s.x)/P.A>0.15) txt('F',xp-s.x/P.A*58+(s.x<0?6:-14),207,'#dc2626',13,true);
    panel([['ばね振り子','#0e7490',14,1],['T＝2π√(m/k)','#0f172a',13],['＝'+P.T.toFixed(3)+' s','#c2410c',19,1],['f＝'+(1/P.T).toFixed(3)+' Hz'],['ω＝'+P.w.toFixed(2)+' rad/s'],
      ['x＝'+sn(s.x,3)+' m','#0e7490',13,1],['v＝'+sn(s.v,3)+' m/s','#2563eb',13,1],['a＝'+sn(s.a,2)+' m/s²','#dc2626',13,1],['F＝−kx＝'+sn(-P.k*s.x,2)+' N','#dc2626',13]]);
    return s; }
  function drawPend(){ const s=pst(t), Lp=P.L*LS, th0=P.th0;
    ctx.fillStyle='#94a3b8'; rr(PVX-70,PVY-14,140,9,3); ctx.fill(); ctx.fillStyle='#64748b'; ctx.fillRect(PVX-5,PVY-6,10,6);
    ctx.setLineDash([5,5]); ctx.strokeStyle='#cbd5e1'; ctx.beginPath(); ctx.moveTo(PVX,PVY); ctx.lineTo(PVX,PVY+Lp+18); ctx.stroke();
    ctx.beginPath(); ctx.arc(PVX,PVY,Lp,Math.PI/2-th0,Math.PI/2+th0); ctx.stroke(); ctx.setLineDash([]);
    const gx=PVX+Lp*Math.sin(s.tha), gy=PVY+Lp*Math.cos(s.tha);
    ctx.setLineDash([4,4]); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.moveTo(PVX,PVY); ctx.lineTo(gx,gy); ctx.stroke(); ctx.setLineDash([]);
    ctx.beginPath(); ctx.arc(gx,gy,12,0,TAU); ctx.fillStyle='rgba(148,163,184,.25)'; ctx.fill(); ctx.stroke(); ctx.lineWidth=1;
    const bx=PVX+Lp*Math.sin(s.th), by=PVY+Lp*Math.cos(s.th);
    ctx.strokeStyle='#334155'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(PVX,PVY); ctx.lineTo(bx,by); ctx.stroke(); ctx.lineWidth=1;
    const gr=ctx.createRadialGradient(bx-4,by-4,2,bx,by,12); gr.addColorStop(0,'#a5f3fc'); gr.addColorStop(1,'#0e7490'); ctx.fillStyle=gr; ctx.beginPath(); ctx.arc(bx,by,12,0,TAU); ctx.fill();
    ctx.fillStyle='#0f172a'; ctx.beginPath(); ctx.arc(PVX,PVY,3.5,0,TAU); ctx.fill();
    const fl=-62*Math.sin(s.th)/Math.max(Math.sin(th0),1e-3); arrow(bx,by,bx+fl*Math.cos(s.th),by-fl*Math.sin(s.th),'#dc2626',3);
    if(Math.abs(fl)>16) txt('mg sinθ',bx+fl*Math.cos(s.th)+(fl>0?6:-62),by-fl*Math.sin(s.th)+16,'#dc2626',12,true);
    txt('L＝'+P.L.toFixed(2)+' m',PVX+8,PVY+Math.min(Lp*0.45,90),'#0e7490',13,true);
    txt('θ₀＝'+Math.round(th0*180/Math.PI)+'°',PVX-12,PVY+22,'#c2410c',12,true,'right');
    const d=(P.T/P.T0-1)*100;
    panel([['単振り子','#0e7490',14,1],['近似式 T₀＝2π√(L/g)','#0f172a',12],['＝'+P.T0.toFixed(3)+' s','#64748b',17,1],['数値積分 T＝','#0f172a',12],['＝'+P.T.toFixed(3)+' s','#c2410c',19,1],
      ['ずれ '+'+'+d.toFixed(2)+' %','#c2410c',13,1],['θ＝'+sn(s.th*180/Math.PI,1)+'°','#0e7490',13,1],['v＝'+(Math.abs(s.om)*P.L).toFixed(2)+' m/s','#2563eb',13,1],['灰色＝近似式の振り子','#64748b',12]]);
    return s; }
  function curve(fn,t0,t1,y0,h,amp,col,lw,dash){ ctx.strokeStyle=col; ctx.lineWidth=lw; if(dash) ctx.setLineDash(dash); ctx.beginPath();
    const n=Math.max(2,Math.round((GX1-GX0)*(t1-t0)/P.win)); for(let i=0;i<=n;i++){ const tt=t0+(t1-t0)*i/n, X=GX0+(tt/P.win)*(GX1-GX0), Y=y0+h/2-fn(tt)/amp*(h/2-5); i?ctx.lineTo(X,Y):ctx.moveTo(X,Y); }
    ctx.stroke(); ctx.setLineDash([]); ctx.lineWidth=1; }
  function frame(y0,h,div){ ctx.fillStyle='#f8fafc'; ctx.fillRect(GX0,y0,GX1-GX0,h);
    for(let j=0;j<=div;j++){ const X=GX0+(GX1-GX0)*j/div; ctx.strokeStyle=(j%(div/2)===0)?'#cbd5e1':'#e5e7eb'; ctx.setLineDash(j%(div/2)===0?[]:[3,3]); ctx.beginPath(); ctx.moveTo(X,y0); ctx.lineTo(X,y0+h); ctx.stroke(); }
    ctx.setLineDash([]); ctx.strokeStyle='#94a3b8'; ctx.beginPath(); ctx.moveTo(GX0,y0+h/2); ctx.lineTo(GX1,y0+h/2); ctx.stroke(); }
  function graphsSpring(){ P.win=2*P.T; const tc=((t%P.win)+P.win)%P.win, Xc=GX0+tc/P.win*(GX1-GX0);
    const rows=[['変位 x','m',(tt)=>sst(tt).x,P.A,'#0e7490'],['速度 v','m/s',(tt)=>sst(tt).v,P.A*P.w,'#2563eb'],['加速度 a','m/s²',(tt)=>sst(tt).a,P.A*P.w*P.w,'#dc2626']];
    rows.forEach((r,i)=>{ const y0=262+i*74, h=64; frame(y0,h,8);
      txt(r[0],8,y0+h/2-3,r[4],13,true); txt('〔'+r[1]+'〕',8,y0+h/2+14,'#64748b',12);
      curve(r[2],0,P.win,y0,h,r[3],r[4]+'55',1.5); if(tc>0) curve(r[2],0,tc,y0,h,r[3],r[4],2.6);
      const Y=y0+h/2-r[2](tc)/r[3]*(h/2-5); ctx.fillStyle=r[4]; ctx.beginPath(); ctx.arc(Xc,Y,4.5,0,TAU); ctx.fill(); });
    ctx.strokeStyle='rgba(15,23,42,.35)'; ctx.beginPath(); ctx.moveTo(Xc,262); ctx.lineTo(Xc,474); ctx.stroke();
    ['0','T/2','T','3T/2','2T'].forEach((s,j)=>txt(s,GX0+(GX1-GX0)*j/4,490,'#475569',12,true,j===0?'left':(j===4?'right':'center')));
    txt('時間 t →',8,490,'#475569',12,true); }
  function graphsPend(){ P.win=3*P.T0; const tc=pst(t).tp, Xc=GX0+tc/P.win*(GX1-GX0), y0=262, h=190, amp=P.th0*180/Math.PI;
    frame(y0,h,6); txt('振れ角 θ',8,y0+h/2-3,'#0e7490',13,true); txt('〔°〕',8,y0+h/2+14,'#64748b',12);
    txt('＋'+Math.round(amp)+'°',GX0-4,y0+12,'#64748b',12,false,'right'); txt('−'+Math.round(amp)+'°',GX0-4,y0+h-3,'#64748b',12,false,'right');
    curve((tt)=>P.th0*Math.cos(P.w0*tt)*180/Math.PI,0,P.win,y0,h,amp,'#94a3b8',2,[6,5]);
    const fe=(tt)=>pend(tt)[0]*180/Math.PI; curve(fe,0,P.win,y0,h,amp,'#0e749055',1.5); if(tc>0) curve(fe,0,tc,y0,h,amp,'#0e7490',2.6);
    for(let j=1;j<=3;j++){ const tj=j*P.T; if(tj<=P.win+1e-9){ const X=GX0+tj/P.win*(GX1-GX0); ctx.fillStyle='#c2410c'; ctx.beginPath(); ctx.moveTo(X,y0+2); ctx.lineTo(X-5,y0-6); ctx.lineTo(X+5,y0-6); ctx.closePath(); ctx.fill(); } }
    ctx.fillStyle='#0e7490'; ctx.beginPath(); ctx.arc(Xc,y0+h/2-fe(tc)/amp*(h/2-5),4.5,0,TAU); ctx.fill();
    ctx.strokeStyle='rgba(15,23,42,.35)'; ctx.beginPath(); ctx.moveTo(Xc,y0); ctx.lineTo(Xc,y0+h); ctx.stroke();
    ['0','T₀','2T₀','3T₀'].forEach((s,j)=>txt(s,GX0+(GX1-GX0)*j/3,y0+h+16,'#475569',12,true,j===0?'left':(j===3?'right':'center')));
    ctx.fillStyle='rgba(255,255,255,.88)'; ctx.fillRect(GX1-322,y0+2,320,19); txt('— 実際（数値積分）　- - 近似式　▼ 実際の周期 T ごと',GX1-6,y0+16,'#475569',12,false,'right');
    txt('3周期で '+(3*(P.T-P.T0)).toFixed(3)+' s おくれる（近似式 3T₀＝'+(3*P.T0).toFixed(2)+' s、実際 3T＝'+(3*P.T).toFixed(2)+' s）',GX0,y0+h+36,'#c2410c',13,true); }
  function energy(K,U,lbU){ const E=P.E, X=180, Wb=330, y=500;
    txt('力学的エネルギー〔J〕（摩擦・空気の抵抗なし）',12,y+8,'#0f172a',13,true);
    const rowsE=[['運動エネルギー K',[[K,'#f97316']],K],[lbU,[[U,'#16a34a']],U],['K＋U（一定）',[[K,'#f97316'],[U,'#16a34a']],K+U]];
    rowsE.forEach((r,i)=>{ const yy=y+18+i*25; txt(r[0],12,yy+14,'#334155',12,true); ctx.fillStyle='#f1f5f9'; ctx.fillRect(X,yy,Wb,18); let x=X;
      r[1].forEach((q)=>{ const w=Wb*clamp(q[0]/E,0,1); ctx.fillStyle=q[1]; ctx.fillRect(x,yy,w,18); x+=w; });
      txt(fJ(r[2])+' J',X+Wb+8,yy+14,'#0f172a',13,true); }); }
  function draw(){ ctx.fillStyle='#ffffff'; ctx.fillRect(0,0,W,H);
    if(mode==='spring'){ const s=drawSpring(); graphsSpring(); energy(0.5*P.m*s.v*s.v,0.5*P.k*s.x*s.x,'弾性エネルギー U'); }
    else { const s=drawPend(); graphsPend(); const v=s.om*P.L; energy(0.5*P.m*v*v,P.m*G*P.L*(1-Math.cos(s.th)),'重力の位置エネルギー U'); } }
  function loop(ts){ if(last===null) last=ts; let dt=(ts-last)/1000; last=ts; if(dt>0.1) dt=0.1;
    if(drag) t=0; else if(run) t+=dt*(+$('spd').value);
    if(t>1e5) t=0; draw(); requestAnimationFrame(loop); }
  function dragTo(x,y){ if(mode==='spring'){ const d=(x-CX)/SX; sg=d<0?-1:1; $('A').value=clamp(Math.round(Math.abs(d)*100),2,20); $('A').dispatchEvent(new Event('input')); }
    else { const a=Math.atan2(x-PVX,y-PVY); sg=a<0?-1:1; $('th').value=clamp(Math.round(Math.abs(a)*180/Math.PI),5,90); $('th').dispatchEvent(new Event('input')); } t=0; }
  cv.addEventListener('pointerdown',(e)=>{ const p=cpos(cv,e), x=p[0]/dpr, y=p[1]/dpr; if(y>256||x>468) return; drag=true; try{ cv.setPointerCapture(e.pointerId); }catch(_){} dragTo(x,y); e.preventDefault(); });
  cv.addEventListener('pointermove',(e)=>{ if(!drag) return; const p=cpos(cv,e); dragTo(p[0]/dpr,p[1]/dpr); });
  const up=()=>{ if(drag){ drag=false; t=0; run=true; $('toggle').textContent='⏸ 一時停止'; } };
  cv.addEventListener('pointerup',up); cv.addEventListener('pointercancel',up);
  ['k','m','A','L','th'].forEach((id)=>$(id).addEventListener('input',()=>{ params(); if(!drag) t=0; }));
  ['mode','spd'].forEach((id)=>$(id).addEventListener('change',()=>{ if(id==='mode'){ sg=1; t=0; } params(); }));
  $('toggle').addEventListener('click',()=>{ run=!run; $('toggle').textContent=run?'⏸ 一時停止':'▶ 再開'; });
  $('reset').addEventListener('click',()=>{ t=0; run=true; $('toggle').textContent='⏸ 一時停止'; });
  params(); draw(); requestAnimationFrame(loop);
'''

sim(slug="tan-shindou", cat="rika", emoji="🌀", score=79,
    title="単振動シミュレーター（ばね振り子・単振り子）",
    title_tag="単振動シミュレーター｜ばね振り子の周期 T＝2π√(m/k)・単振り子 T＝2π√(L/g)と等速円運動の正射影",
    meta_desc="高校物理「円運動と単振動」をブラウザで再現。ばね定数・質量・振幅を変えると、おもりの単振動が等速円運動の正射影になる様子と、変位・速度・加速度のグラフ（位相のずれ）、エネルギーの棒グラフを同時に表示。単振り子の周期 T＝2π√(L/g) と数値積分の比較もできます。",
    og_title="単振動シミュレーター（ばね振り子・単振り子）",
    og_desc="等速円運動の正射影として単振動を見る。x・v・a の位相のずれ、周期 T＝2π√(m/k)、単振り子の近似式と数値積分の比較。",
    card_desc="ばね振り子と単振り子の単振動を、等速円運動の正射影・x/v/aのグラフ・エネルギーで見る。周期の式も確認。",
    lead="ばね定数 k・質量 m・振幅 A を変えると、おもりの単振動と、それに対応する等速円運動が同時に動きます。変位・速度・加速度のグラフで位相のずれを、棒グラフで力学的エネルギーの保存を確かめられます。単振り子では、周期の近似式 T＝2π√(L/g) と数値積分した実際の動きを重ねて比べられます。",
    model="物理 円運動と単振動", level="高校（物理）", unit="高等学校 物理 (1)様々な運動 (ｳ)円運動と単振動 ㋑単振動",
    canvas=canvas(640, 590, light=True),
    controls=select("mode", "振り子の種類", [("spring", "ばね振り子（水平）"), ("pend", "単振り子")])
           + slider("k", "ばね定数 k", 5, 100, 20, 1, "{v} N/m") + slider("m", "おもりの質量 m", 0.1, 2, 0.5, 0.05, "{v} kg")
           + slider("A", "振幅 A", 2, 20, 10, 1, "{v} cm")
           + slider("L", "振り子の長さ L", 0.25, 2, 1, 0.05, "{v} m") + slider("th", "振れ角 θ₀", 5, 90, 10, 1, "{v}°")
           + select("spd", "再生の速さ", [("1", "実際の速さ"), ("0.5", "1/2倍（スロー）"), ("0.25", "1/4倍（スロー）")]),
    buttons=btn("toggle", "⏸ 一時停止", True) + btn("reset", "↺ 最初から"),
    stats=stats([("sT", "周期 T", True), ("sF", "振動数 f", False), ("sV", "速さの最大値", False), ("sA", "加速度の大きさの最大値", False)]),
    legend="おもり（振り子）は指やペンでつかんで引っぱり、はなすと振動を始めます。青い矢印＝速度 v、赤い矢印＝復元力 F。紫の点は、半径＝振幅の等速円運動をする点で、その真下の影（正射影）がおもりと同じ動きをします。グラフの縦の点線は1/4周期ごとです。単振り子では、灰色の振り子が近似式 T₀＝2π√(L/g) どおりの動き、色のついた振り子が運動方程式を数値積分した実際の動きです。",
    article=TAN_ARTICLE, faqs=TAN_FAQS,
    rel=[("furiko-jikken", "⏱️", "振り子の実験"), ("bane-nobi", "🪀", "ばねののびと力"), ("pendulum-wave", "🎐", "振り子の波"),
         ("lissajous", "➰", "リサージュ図形"), ("building-quake", "🏢", "地震でビルはどう揺れる？")],
    js=TAN_JS)


# ============================================================ 2 うなりと定常波
SOUND_TABLE = T([["%d ℃" % tc, "%.1f m/s" % (331.5 + 0.6 * tc)] for tc in (-10, 0, 10, 15, 20, 25, 30, 35)],
                ["気温 t", "音速 V＝331.5＋0.6t"])
_V20 = 331.5 + 0.6 * 20
MODE_TABLE = T([["弦（両端を固定）", "両端が節", "λₙ＝2L/n", "fₙ＝nv/2L（v＝√(S/ρ)）", "基本振動の整数倍すべて（1, 2, 3, …倍）"],
                ["閉管（片方が閉じた管）", "閉じた端が節、開いた端が腹", "λ＝4L/(2n−1)", "f＝(2n−1)V/4L", "奇数倍だけ（1, 3, 5, …倍）"],
                ["開管（両方が開いた管）", "両端が腹", "λ＝2L/n", "f＝nV/2L", "整数倍すべて（1, 2, 3, …倍）"]],
               ["振動するもの", "端のようす（変位）", "波長", "固有振動数", "現れる振動"])
PIPE_EX = T([["閉管", "%.0f Hz" % (_V20 / 2), "%.0f Hz" % (3 * _V20 / 2), "%.0f Hz" % (5 * _V20 / 2)],
             ["開管", "%.1f Hz" % (_V20 / 1), "%.0f Hz" % (2 * _V20), "%.0f Hz" % (3 * _V20)]],
            ["L＝0.50 m・20℃（V＝343.5 m/s）", "基本振動", "2番目の固有振動", "3番目の固有振動"])

UNARI_ARTICLE = "<h2>このシミュレーションでわかること</h2>\n" + P(
    "振動数 f₁ と f₂ がわずかに異なる2つの音を重ねると、1秒間に <b>|f₁−f₂| 回</b>のうなりが聞こえます。"
    "逆向きに進む同じ波を重ねると<b>定常波（定在波）</b>ができ、隣り合う節の間隔は <b>λ/2</b> です。"
    "弦の固有振動数は <b>fₙ＝nv/2L</b>（v＝√(S/ρ)）、閉管は <b>f＝(2n−1)V/4L</b>、開管は <b>f＝nV/2L</b>、音速は <b>V＝331.5＋0.6t</b> 〔m/s〕です。") + '''
<p>高等学校「物理基礎」の「(2) 様々な物理現象とエネルギーの利用」(ｱ)波 ㋐波の性質（重ね合わせ・定在波）と ㋑音と振動（気柱の共鳴・弦の振動・うなり）で学ぶ内容です（学習指導要領 平成30年告示）。内容の取扱いには「定在波も扱い」「波の反射，共振，うなりなどを扱う」とあり、解説では、うなりの合成波の形をコンピュータで調べることや、弦の振動数と弦の質量・張力との関係を調べることが例に挙げられています。正弦波の式と位相は「物理」の (2) 波で扱います。</p>
<p>表示を4つに切りかえられます。①うなり：2つの音の波形と合成波を表示し、実際の音を鳴らせます。②定常波：右へ進む入射波と、端で反射して左へ進む反射波を重ね、腹と節ができる様子を見ます。③弦の固有振動：弦の長さ・張力・線密度から振動数を求めます。④気柱の固有振動：閉管と開管の空気の振動（縦波）を、粒の動きと変位のグラフで表示します。</p>
<h2>授業での使い方</h2>
<ul>
<li><b>導入</b>：おんさ2本の代わりに、①うなりで 440 Hz と 444 Hz の音を鳴らし、「ウォーン、ウォーン」と大きくなる回数を数えさせます。振動数の差を変えると、うなりの速さが変わることがすぐにわかります（音はボタンを押したときだけ鳴り、10秒で止まります。最初は音量を小さくしてください）。</li>
<li><b>展開</b>：②定常波で「1/8周期すすめる」を押しながら、入射波と反射波の重ね合わせをノートに作図させ、画面と答え合わせをします。固定端と自由端で、端が節になるか腹になるかを比べます。③弦では、張力を4倍にすると振動数が2倍になることを確かめ、④気柱では、閉管と開管で現れる固有振動のちがいを比べます。気柱共鳴管の実験で、共鳴が起こる長さを予想するときにも使えます。</li>
<li><b>まとめ</b>：弦・閉管・開管の「端のようす」と固有振動数の式を表にまとめます。ギターの弦を押さえると音が高くなる理由や、管楽器の音の高さとも結びつけられます。</li>
</ul>
<p>生徒への問いの例：</p>
<ol>
<li>440 Hz のおんさと、振動数がわからないおんさを同時に鳴らすと、1秒間に3回うなりました。もう一方のおんさの振動数は何 Hz でしょう。どちらか1つに決めるには、どうすればよいでしょう。</li>
<li>弦の張力を4倍にすると、基本振動の振動数は何倍になるでしょう。弦の長さを半分にしたときはどうでしょう。</li>
<li>同じ長さの閉管と開管では、どちらの基本振動数が高いでしょう。閉管に2倍振動が現れないのはなぜでしょう。</li>
</ol>
<h2>しくみ・解説</h2>
<h3>用語の意味</h3>
<ul>
<li><b>波の重ね合わせの原理</b>とは、2つの波が重なった点の変位は、それぞれの波の変位の和になるという原理です。</li>
<li><b>うなり</b>とは、振動数がわずかに異なる2つの音が重なったとき、音の大きさが周期的に大きくなったり小さくなったりする現象です。</li>
<li><b>定常波（定在波）</b>とは、振幅・波長・振動数が等しく、互いに逆向きに進む2つの波が重なってできる、どちらにも進まない波です。</li>
<li><b>節</b>とは定常波でまったく振動しない点で、<b>腹</b>とは最も大きく振動する点です。</li>
<li><b>固有振動</b>とは、弦や気柱が、両端の条件で決まる定常波をつくって振動することで、その振動数を<b>固有振動数</b>といいます。いちばん低い固有振動を<b>基本振動</b>、その n 倍の振動数のものを <b>n 倍振動</b>といいます。</li>
<li><b>共鳴（共振）</b>とは、外から加わる振動の振動数が物体の固有振動数と一致したとき、物体が大きく振動する現象です。</li>
<li><b>開口端補正</b>とは、気柱の開いた端の腹が管口より少し外側にできるときの、そのずれの長さ Δx です。</li>
</ul>
<h3>うなりの回数</h3>
''' + N("うなりの回数（1秒あたり） f＝|f₁−f₂|　　うなりの周期 T＝1/|f₁−f₂|") + '''
<p>振幅の等しい2つの音 y₁＝A sin 2πf₁t、y₂＝A sin 2πf₂t を重ねると、y＝2A cos{π(f₁−f₂)t}・sin{π(f₁＋f₂)t} となります。聞こえる音の高さは、ほぼ2つの平均の振動数 (f₁＋f₂)/2 で、振幅（音の大きさ）が 2A|cos{π(f₁−f₂)t}| にしたがって変化します。この大きさの山は1秒間に |f₁−f₂| 回やってきます。</p>
<p><b>計算例</b>：440 Hz と 443 Hz の音を重ねると、うなりは |440−443|＝<b>3 回/秒</b>、うなりの周期は 1÷3≒<b>0.33 秒</b>です。振動数がわからないおんさとのうなりが3回/秒なら、そのおんさは 437 Hz か 443 Hz です。わからない方のおんさに小さなおもりを付けると振動数が少し下がるので、うなりが減れば 443 Hz、増えれば 437 Hz と決められます。</p>
<h3>定常波（定在波）</h3>
''' + N("y₁＝A sin 2π(t/T − x/λ)（右へ進む）、y₂＝A sin 2π(t/T ＋ x/λ)（左へ進む）<br>y＝y₁＋y₂＝2A cos(2πx/λ)・sin(2πt/T)　→　隣り合う節の間隔＝λ/2、腹と節の間隔＝λ/4") + '''
<p>合成波は、場所によって振幅 2A|cos(2πx/λ)| が決まり、どの点も同じ周期でその場で振動するだけで、波形は左右に進みません。反射でできる定常波では、<b>固定端は節</b>、<b>自由端は腹</b>になります。</p>
<p><b>計算例</b>：波長 λ＝40 cm の波が固定端で反射してできる定常波では、節は端から 0 cm、20 cm、40 cm、…の位置、腹は端から 10 cm、30 cm、…の位置にできます。</p>
<h3>弦の固有振動</h3>
''' + N("弦を伝わる波の速さ v＝√(S/ρ)（S：張力〔N〕、ρ：線密度〔kg/m〕）<br>n 倍振動の波長 λₙ＝2L/n　　固有振動数 fₙ＝v/λₙ＝nv/2L（n＝1, 2, 3, …）") + '''
<p>両端が固定された弦では、両端が節になる定常波だけが続きます。長さ L の中に半波長（λ/2）がちょうど n 個入るので λₙ＝2L/n です。</p>
<p><b>計算例</b>：長さ L＝0.50 m、張力 S＝40 N、線密度 ρ＝1.0 g/m＝1.0×10⁻³ kg/m の弦では、v＝√(40÷0.0010)＝<b>200 m/s</b>、基本振動数 f₁＝200÷(2×0.50)＝<b>200 Hz</b>、2倍振動 400 Hz、3倍振動 600 Hz です（このシミュレーションの初期設定）。張力を4倍にすると v も f も2倍、線密度を4倍にすると1/2倍、長さを半分にすると f は2倍になります。</p>
<h3>気柱の固有振動（閉管・開管）</h3>
''' + N("音速 V＝331.5＋0.6t 〔m/s〕（t：セルシウス温度〔℃〕）<br>閉管：λ＝4L/(2n−1)、f＝(2n−1)V/4L（基本振動の奇数倍だけ）<br>開管：λ＝2L/n、f＝nV/2L（基本振動の整数倍すべて）") + MODE_TABLE + '''
<p>閉じた端では空気が動けないので変位の節、開いた端では空気が自由に動けるので変位の腹になります。閉管では長さ L の中に λ/4 の奇数倍しか入らないため、基本振動の偶数倍の振動は現れません。なお、変位の節の位置では空気が押し縮められたり引きのばされたりするので、密度（圧力）の変化はいちばん大きくなります。</p>
''' + PIPE_EX + '''
<p>音速の早見表：</p>
''' + SOUND_TABLE + '''
<h3>気柱共鳴管の実験と開口端補正（発展）</h3>
<p>気柱共鳴管の口に 440 Hz のおんさを近づけ、水面を下げていくと、1回目に L₁＝18.6 cm、2回目に L₂＝57.6 cm で共鳴したとします。共鳴が起こる長さの差は半波長なので、λ/2＝57.6−18.6＝39.0 cm、λ＝78.0 cm、音速は V＝fλ＝440×0.780＝<b>343 m/s</b> と求められます。また、1回目の共鳴では L₁＋Δx＝λ/4 なので、開口端補正は Δx＝19.5−18.6＝<b>0.9 cm</b> です。開口端補正の大きさは、管の半径の0.6倍ほどになることが知られています。このシミュレーションで「開口端補正を考える」を選ぶと、半径 2 cm の管として Δx＝1.2 cm を加えて計算します（閉管は L＋Δx、開管は L＋2Δx）。</p>
<h3>このシミュレーションで単純にしていること</h3>
<ul>
<li>音はすべて正弦波（純音）としています。実際の楽器の音は、基本振動に倍振動が混ざった音です。</li>
<li>定常波・弦・気柱の動きは、目で追えるように実際よりゆっくり表示しています。気柱の空気の粒の動きは、大きく誇張しています。</li>
<li>弦の波の速さの式 v＝√(S/ρ) は、教科書によっては発展として扱われたり、問題文で与えられたりします。</li>
<li>音は Web Audio の機能で、端末の中だけで作って鳴らしています（外部との通信はありません）。スピーカーの性能によって、低い音や高い音は聞こえにくいことがあります。</li>
</ul>
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「高等学校学習指導要領（平成30年告示）解説 理科編 理数編」物理基礎 (2) (ｱ)波 ㋐波の性質・㋑音と振動、物理 (2) 波（<a href="''' + MEXT_KOU + '''" target="_blank" rel="noopener">文部科学省 学習指導要領のページ</a>）</li>
<li>高等学校「物理基礎」「物理」の教科書（数研出版、東京書籍、啓林館、第一学習社など）の波と音の章（音速 V＝331.5＋0.6t、弦と気柱の固有振動）</li>
</ul>
'''

UNARI_FAQS = [
    ("うなりの回数は、どうやって求めますか？", "2つの音の振動数の差の大きさ |f₁−f₂| が、1秒あたりのうなりの回数です。例えば 440 Hz と 443 Hz なら、1秒間に3回うなります。うなりの周期（音が大きくなってから次に大きくなるまでの時間）は 1/|f₁−f₂| 秒で、この例では約0.33秒です。"),
    ("定常波（定在波）の節と節の間隔は？", "隣り合う節と節の間隔は半波長 λ/2、隣り合う腹と節の間隔は λ/4 です。固定端で反射してできる定常波では端が節に、自由端で反射してできる定常波では端が腹になります。"),
    ("閉管で偶数倍の振動が現れないのはなぜですか？", "閉管では、閉じた端が変位の節、開いた端が変位の腹になります。長さ L の中に λ/4 の奇数倍（λ/4、3λ/4、5λ/4、…）しか入らないので、固有振動数は基本振動数 V/4L の奇数倍（1倍、3倍、5倍、…）だけになります。"),
    ("開口端補正とは何ですか？", "気柱の開いた端にできる腹が、実際には管口より少し外側にできることを考えに入れたときの、そのずれの長さ Δx のことです。管の半径のおよそ0.6倍で、気柱共鳴管の実験では、1回目と2回目に共鳴する長さの差（＝λ/2）を使うと Δx の影響を消して波長を求められます。"),
    ("弦の振動数を高くするには、どうすればよいですか？", "弦の固有振動数は fₙ＝(n/2L)√(S/ρ) なので、弦を短くする、張力を大きくする、線密度の小さい（細い・軽い）弦にする、のいずれかで高くなります。張力を4倍にすると振動数は2倍になります。"),
    ("音速の式 V＝331.5＋0.6t の t は何ですか？", "気温（セルシウス温度、単位は℃）です。0℃で 331.5 m/s、気温が1℃上がるごとに約 0.6 m/s 速くなり、20℃では 343.5 m/s です。"),
]

UNARI_JS = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const TAU=Math.PI*2, X0=60, X1=612;
  let mode='beat', t=0, run=true, last=null, AC=null, master=null, oscs=[], playing=null, pStart=0, stopT=null, note='';
  const fld=(id)=>$(id).closest('.field');
  function lab(id,s){ const e=$(id); if(e&&e.previousElementSibling) e.previousElementSibling.textContent=s; }
  function show(id,on){ const e=$(id); if(e) e.style.display=on?'':'none'; }
  function txt(s,x,y,col,sz,b,al){ ctx.fillStyle=col; ctx.font=(b?'bold ':'')+sz+'px sans-serif'; ctx.textAlign=al||'left'; ctx.fillText(s,x,y); }
  function rr(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
  function g3(v){ return v>=1000?v.toFixed(0):v.toPrecision(3); }
  function f1d(v){ return (Math.round(v*10)/10).toString(); }
  function hz(v){ return v>=1000?v.toFixed(0):v.toFixed(1); }
  const SH={beat:['f1','df','vol'],stand:['lam','end'],str:['Ls','S','rho','n','vol'],pipe:['tube','Lp','temp','np','corr','vol']};
  const ALL=['f1','df','lam','end','Ls','S','rho','n','tube','Lp','temp','np','corr','vol'];
  function V(){ const f1=+$('f1').value, df=+$('df').value, Ls=+$('Ls').value, S=+$('S').value, rho=+$('rho').value/1000, n=+$('n').value, np=+$('np').value, Lp=+$('Lp').value/100, tc=+$('temp').value;
    const vs=Math.sqrt(S/rho), Vs=331.5+0.6*tc, cl=$('tube').value==='closed', dx=$('corr').value==='1'?0.012:0;
    const h=cl?2*np-1:np, Le=cl?Lp+dx:Lp+2*dx, lp=cl?4*Le/h:2*Le/np;
    return {f1:f1,df:df,f2:f1+df,lam:+$('lam').value/100,fixed:$('end').value==='fixed',Ls:Ls,S:S,rho:rho,n:n,vs:vs,ls:2*Ls/n,fs:n*vs/(2*Ls),fs1:vs/(2*Ls),
      np:np,Lp:Lp,tc:tc,Vs:Vs,cl:cl,dx:dx,h:h,Le:Le,lp:lp,fp:Vs/lp,fp1:cl?Vs/(4*Le):Vs/(2*Le)}; }
  // ---- 音（ボタンを押したときだけ。10秒で自動停止）
  function getAC(){ if(!AC){ const C=window.AudioContext||window.webkitAudioContext; if(!C) return null; AC=new C(); } if(AC.state==='suspended'&&AC.resume) AC.resume(); return AC; }
  function stopSound(){ clearTimeout(stopT); if(AC&&master){ const n=AC.currentTime, g=master; g.gain.cancelScheduledValues(n); g.gain.setValueAtTime(g.gain.value,n); g.gain.linearRampToValueAtTime(0,n+0.06);
      oscs.forEach((o)=>{ try{ o.stop(n+0.08); }catch(_){} }); setTimeout(()=>{ try{ g.disconnect(); }catch(_){} },300); }
    master=null; oscs=[]; playing=null; $('stopS').textContent='■ 音を止める'; }
  function freqsOf(kind){ const v=V(); if(mode==='beat') return kind==='p1'?[v.f1]:(kind==='p2'?[v.f2]:[v.f1,v.f2]); return [mode==='str'?v.fs:v.fp]; }
  function playSound(kind){ stopSound(); const c=getAC(); if(!c){ note='このブラウザでは音を鳴らせません'; return; } const fs=freqsOf(kind);
    if(fs.some((f)=>f<20||f>12000)){ note='この振動数（'+hz(fs[0])+' Hz）は鳴らせません（20〜12000 Hz）'; return; }
    note=''; const vol=+$('vol').value, n0=c.currentTime; master=c.createGain(); master.gain.setValueAtTime(0,n0); master.gain.linearRampToValueAtTime(vol,n0+0.08); master.connect(c.destination);
    oscs=fs.map((f)=>{ const o=c.createOscillator(); o.type='sine'; o.frequency.setValueAtTime(f,n0); const g=c.createGain(); g.gain.value=1/fs.length; o.connect(g); g.connect(master); o.start(n0); return o; });
    playing=kind; pStart=n0; if(mode==='beat') t=0; stopT=setTimeout(stopSound,10000); $('stopS').textContent='■ 音を止める（再生中）'; }
  function retune(){ if(!playing||!AC) return; const fs=freqsOf(playing); if(fs.some((f)=>f<20||f>12000)){ stopSound(); return; } oscs.forEach((o,i)=>{ o.frequency.setTargetAtTime(fs[i],AC.currentTime,0.01); }); }
  // ---- ① うなり
  function strip(y0,h,fn,amp,col,lw,ts,dur){ ctx.strokeStyle=col; ctx.lineWidth=lw; ctx.beginPath(); const n=(X1-X0)*2;
    for(let i=0;i<=n;i++){ const X=X0+(X1-X0)*i/n, y=y0+h/2-fn(ts+dur*i/n)/amp*(h/2-4); i?ctx.lineTo(X,y):ctx.moveTo(X,y); } ctx.stroke(); ctx.lineWidth=1; }
  function axisBox(y0,h){ ctx.fillStyle='#f8fafc'; ctx.fillRect(X0,y0,X1-X0,h); ctx.strokeStyle='#cbd5e1'; ctx.beginPath(); ctx.moveTo(X0,y0+h/2); ctx.lineTo(X1,y0+h/2); ctx.stroke(); }
  function drawBeat(v){ const d=Math.abs(v.df), nb=Math.max(1,Math.ceil(d-1e-9)), wd=d>0?nb/d:1, tw=((t%wd)+wd)%wd, dur=10/v.f1, ts=Math.round(tw*v.f1)/v.f1;
    txt('f₁＝'+v.f1+' Hz',X0,22,'#2563eb',15,true); txt('f₂＝'+f1d(v.f2)+' Hz',X0+140,22,'#ea580c',15,true);
    txt(d>0?'うなり '+f1d(d)+' 回/秒':'うなりは起こらない',X1,22,'#0f766e',16,true,'right');
    const y1=(tt)=>Math.sin(TAU*v.f1*tt), y2=(tt)=>Math.sin(TAU*v.f2*tt);
    [[36,54,y1,1,'#2563eb','f₁'],[96,54,y2,1,'#ea580c','f₂'],[156,96,(tt)=>y1(tt)+y2(tt),2,'#0f766e','合成波']].forEach((r)=>{ axisBox(r[0],r[1]); strip(r[0],r[1],r[2],r[3],r[4],2,ts,dur); txt(r[5],X0-6,r[0]+r[1]/2+5,r[4],13,true,'right'); });
    txt('▲ 拡大図：'+(dur*1000).toFixed(1)+' ミリ秒間（下の全体図の ▼ の時刻）',X0,268,'#475569',12);
    const ey=304, eh=132, ec=ey+eh/2, ea=eh/2-6;
    txt('合成波の全体（'+(Math.round(wd*100)/100)+' 秒間）：音の大きさ（振幅）が大きくなったり小さくなったりする',X0-50,294,'#0f172a',13,true);
    axisBox(ey,eh); ctx.strokeStyle='#99f6e4'; ctx.beginPath();
    for(let X=X0;X<=X1;X+=1.5){ const e=Math.abs(2*Math.cos(Math.PI*v.df*(X-X0)/(X1-X0)*wd))/2*ea; ctx.moveTo(X,ec-e); ctx.lineTo(X,ec+e); } ctx.stroke();
    [1,-1].forEach((s)=>{ ctx.strokeStyle='#0f766e'; ctx.lineWidth=2; ctx.beginPath(); for(let X=X0;X<=X1;X+=2){ const e=Math.abs(Math.cos(Math.PI*v.df*(X-X0)/(X1-X0)*wd))*ea; const y=ec-s*e; X===X0?ctx.moveTo(X,y):ctx.lineTo(X,y); } ctx.stroke(); ctx.lineWidth=1; });
    if(d>0){ for(let k=1;k<=nb;k++){ const X=X0+(k/d)/wd*(X1-X0); ctx.fillStyle='#ea580c'; ctx.beginPath(); ctx.arc(X,ec-ea,4,0,TAU); ctx.fill(); txt(String(k),X-(k===nb?8:-6),ec-ea+16,'#ea580c',13,true,k===nb?'right':'left'); } }
    const stp=wd<=1.5?0.25:0.5; for(let s=0;s<=wd+1e-9;s+=stp){ const X=X0+s/wd*(X1-X0); ctx.strokeStyle='#94a3b8'; ctx.beginPath(); ctx.moveTo(X,ey+eh); ctx.lineTo(X,ey+eh+5); ctx.stroke();
      txt((Math.round(s*100)/100)+(s===0?'':' s'),X,ey+eh+18,'#475569',12,false,s===0?'left':(Math.abs(s-wd)<0.01?'right':'center')); }
    const Xc=X0+tw/wd*(X1-X0); ctx.strokeStyle='rgba(220,38,38,.7)'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.moveTo(Xc,ey); ctx.lineTo(Xc,ey+eh); ctx.stroke(); ctx.lineWidth=1;
    ctx.fillStyle='#dc2626'; ctx.beginPath(); ctx.moveTo(Xc,ey+1); ctx.lineTo(Xc-6,ey-8); ctx.lineTo(Xc+6,ey-8); ctx.closePath(); ctx.fill();
    txt('うなりの回数 ＝ |f₁ − f₂| ＝ |'+v.f1+' − '+f1d(v.f2)+'| ＝ '+f1d(d)+' 回/秒',X0-50,486,'#0f172a',15,true);
    txt(d>0?'うなりの周期 ＝ 1 ÷ '+f1d(d)+' ＝ '+(1/d).toFixed(3)+' 秒（大きい音から、次の大きい音まで）':'2つの音の振動数が同じなので、音の大きさは変わりません',X0-50,510,'#334155',13); }
  // ---- ② 定常波
  function drawStand(v){ const Lw=1.2, sx=(X1-X0)/Lw, k=TAU/v.lam, Tv=2.4, ph=TAU*t/Tv, sgn=v.fixed?-1:1;
    const yi=(x)=>Math.sin(ph-k*x), yr=(x)=>sgn*Math.sin(ph-k*(2*Lw-x)), ys=(x)=>yi(x)+yr(x), env=(x)=>2*Math.abs(v.fixed?Math.sin(k*(Lw-x)):Math.cos(k*(Lw-x)));
    const nodes=[], anti=[]; for(let m=0;m<60;m++){ const a=Lw-(v.fixed?0:v.lam/4)-m*v.lam/2, b=Lw-(v.fixed?v.lam/4:0)-m*v.lam/2; if(a>=-1e-9) nodes.push(a); if(b>=-1e-9) anti.push(b); }
    ctx.setLineDash([3,4]); ctx.strokeStyle='#c4b5fd'; nodes.forEach((x)=>{ const X=X0+x*sx; ctx.beginPath(); ctx.moveTo(X,26); ctx.lineTo(X,424); ctx.stroke(); }); ctx.setLineDash([]);
    const rows=[['入射波 → 右向きに進む',26,80,yi,1,'#2563eb'],['反射波 ← 左向きに進む（右端で反射）',134,80,yr,1,'#ea580c'],['合成波（定常波）＝ 入射波 ＋ 反射波',244,180,ys,2,'#0f766e']];
    rows.forEach((r)=>{ const y0=r[1], h=r[2], c=y0+h/2, a=(h/2-6)/r[4]; txt(r[0],X0,y0-8,r[5],13,true); ctx.fillStyle='rgba(248,250,252,.6)'; ctx.fillRect(X0,y0,X1-X0,h);
      ctx.strokeStyle='#cbd5e1'; ctx.beginPath(); ctx.moveTo(X0,c); ctx.lineTo(X1,c); ctx.stroke();
      if(r[4]===2){ ctx.setLineDash([5,4]); ctx.strokeStyle='#5eead4'; [1,-1].forEach((s)=>{ ctx.beginPath(); for(let X=X0;X<=X1;X+=2){ const y=c-s*env((X-X0)/sx)*a; X===X0?ctx.moveTo(X,y):ctx.lineTo(X,y); } ctx.stroke(); }); ctx.setLineDash([]); }
      ctx.strokeStyle=r[5]; ctx.lineWidth=r[4]===2?3:2.2; ctx.beginPath(); for(let X=X0;X<=X1;X+=1.5){ const y=c-r[3]((X-X0)/sx)*a; X===X0?ctx.moveTo(X,y):ctx.lineTo(X,y); } ctx.stroke(); ctx.lineWidth=1; });
    // 右端
    if(v.fixed){ ctx.fillStyle='#94a3b8'; ctx.fillRect(X1,20,10,408); ctx.strokeStyle='#64748b'; for(let y=24;y<424;y+=10){ ctx.beginPath(); ctx.moveTo(X1+2,y+8); ctx.lineTo(X1+10,y); ctx.stroke(); } }
    else { ctx.strokeStyle='#64748b'; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(X1+5,20); ctx.lineTo(X1+5,428); ctx.stroke(); ctx.lineWidth=1; const c=334, a=84/2; ctx.strokeStyle='#0f766e'; ctx.lineWidth=2.5; ctx.strokeRect(X1,c-ys(Lw)*a-5,10,10); ctx.lineWidth=1; }
    txt(v.fixed?'固定端':'自由端',X1+12,14,'#475569',12,true,'right');
    nodes.forEach((x)=>txt('節',X0+x*sx,442,'#7c3aed',13,true,'center')); anti.forEach((x)=>txt('腹',X0+x*sx,442,'#ea580c',13,true,'center'));
    const xa=anti[anti.length-1], xn=nodes[nodes.length-1], c=334, a=84/2;
    ctx.fillStyle='#ea580c'; ctx.beginPath(); ctx.arc(X0+xa*sx,c-ys(xa)*a,6,0,TAU); ctx.fill(); ctx.fillStyle='#7c3aed'; ctx.beginPath(); ctx.arc(X0+xn*sx,c-ys(xn)*a,6,0,TAU); ctx.fill();
    const fr=((t/Tv)%1+1)%1, e8=fr*8, r8=Math.round(e8)%8; let ft;
    if(Math.abs(e8-Math.round(e8))<0.03){ ft=['0','1/8 T','1/4 T','3/8 T','1/2 T','5/8 T','3/4 T','7/8 T'][r8]; } else ft=fr.toFixed(2)+' T';
    txt('λ＝'+Math.round(v.lam*100)+' cm　隣り合う節の間隔 λ/2＝'+f1d(v.lam*50)+' cm　腹と節の間隔 λ/4＝'+f1d(v.lam*25)+' cm',X0-50,474,'#0f172a',14,true);
    txt('時刻 t＝'+ft+'（T：周期）　「1/8周期すすめる」で作図と比べよう',X0-50,498,'#334155',13);
    txt('オレンジの点（腹）と紫の点（節）は、その場で上下するだけ（波形は左右に進まない）',X0-50,520,'#334155',13); }
  // ---- 調和（固有振動数の一覧）
  function harmonics(list,cur,y0,title,unitf){ txt(title,16,y0,'#0f172a',13,true); const base=y0+112, max=list[list.length-1]*1.1;
    ctx.strokeStyle='#94a3b8'; ctx.beginPath(); ctx.moveTo(30,base); ctx.lineTo(626,base); ctx.stroke();
    list.forEach((f,i)=>{ const X=40+f/max*580, on=i===cur; ctx.fillStyle=on?'#0f766e':'#cbd5e1'; ctx.fillRect(X-7,base-(on?88:70),14,on?88:70);
      txt(unitf(i),X,base+16,on?'#0f766e':'#475569',12,true,'center'); txt(hz(f)+' Hz',X,base+31,on?'#0f766e':'#64748b',12,on,'center'); }); }
  // ---- ③ 弦
  function drawStr(v){ const XA=80, XB=560, yc=120, amp=58, ph=TAU*t/1.6, n=v.n, sxl=(XB-XA);
    txt('弦の固有振動　'+(n===1?'基本振動（n＝1）':n+'倍振動（n＝'+n+'）'),16,22,'#0f172a',15,true);
    txt('動きはゆっくり表示（実際は1秒間に'+Math.round(v.fs)+'回）',624,22,'#64748b',12,false,'right');
    ctx.setLineDash([5,4]); ctx.strokeStyle='#5eead4'; [1,-1].forEach((s)=>{ ctx.beginPath(); for(let i=0;i<=240;i++){ const X=XA+sxl*i/240, y=yc-s*amp*Math.sin(n*Math.PI*i/240); i?ctx.lineTo(X,y):ctx.moveTo(X,y); } ctx.stroke(); }); ctx.setLineDash([]);
    ctx.strokeStyle='#0f766e'; ctx.lineWidth=3; ctx.beginPath(); for(let i=0;i<=240;i++){ const X=XA+sxl*i/240, y=yc-amp*Math.sin(n*Math.PI*i/240)*Math.cos(ph); i?ctx.lineTo(X,y):ctx.moveTo(X,y); } ctx.stroke(); ctx.lineWidth=1;
    [XA,XB].forEach((X)=>{ ctx.fillStyle='#64748b'; ctx.beginPath(); ctx.moveTo(X,yc); ctx.lineTo(X-9,yc+18); ctx.lineTo(X+9,yc+18); ctx.closePath(); ctx.fill(); });
    ctx.strokeStyle='#94a3b8'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(30,yc); ctx.lineTo(XA,yc); ctx.moveTo(XB,yc); ctx.lineTo(600,yc); ctx.stroke(); ctx.lineWidth=1;
    ctx.fillStyle='#475569'; ctx.fillRect(600,yc-14,10,40); txt('おもり（張力 S）',610,yc+44,'#475569',12,false,'right');
    for(let j=0;j<=n;j++) txt('節',XA+sxl*j/n,yc+amp+22,'#7c3aed',13,true,'center'); for(let j=0;j<n;j++) txt('腹',XA+sxl*(j+0.5)/n,yc+amp+22,'#ea580c',13,true,'center');
    const by=yc+amp+36, bx2=n>=2?XA+sxl*2/n:XB; ctx.strokeStyle='#0f172a'; ctx.beginPath(); ctx.moveTo(XA,by-5); ctx.lineTo(XA,by); ctx.lineTo(bx2,by); ctx.lineTo(bx2,by-5); ctx.stroke();
    txt(n>=2?'λₙ＝'+g3(v.ls)+' m':'λ/2 ＝ L',(XA+bx2)/2,by+15,'#0f172a',12,true,'center');
    ctx.fillStyle='#f0fdfa'; rr(16,250,608,108,10); ctx.fill(); ctx.strokeStyle='#99f6e4'; ctx.stroke();
    txt('v ＝ √(S/ρ) ＝ √('+v.S+' N ÷ '+v.rho.toFixed(4)+' kg/m) ＝ '+g3(v.vs)+' m/s',30,276,'#0f172a',14,true);
    txt('λₙ ＝ 2L/n ＝ 2×'+v.Ls.toFixed(2)+' ÷ '+n+' ＝ '+g3(v.ls)+' m　（弦の長さ L＝'+v.Ls.toFixed(2)+' m）',30,302,'#0f172a',14);
    txt('fₙ ＝ nv/2L ＝ '+n+'×'+g3(v.vs)+' ÷ (2×'+v.Ls.toFixed(2)+') ＝ '+hz(v.fs)+' Hz',30,336,'#c2410c',17,true);
    harmonics([1,2,3,4,5,6].map((k)=>k*v.fs1),n-1,384,'この弦の固有振動数（基本振動数の整数倍）',(i)=>i===0?'基本':(i+1)+'倍');
    if(note) txt(note,16,545,'#dc2626',12,true); }
  // ---- ④ 気柱
  function drawPipe(v){ const TX0=100, TX1=560, yc=124, sx=(TX1-TX0)/v.Lp, k=TAU/v.lp, ph=TAU*t/1.6, top=69, bot=179;
    const u=(x)=>v.cl?Math.sin(k*x):Math.cos(k*(x+v.dx));
    txt((v.cl?'閉管（片方の端が閉じた管）':'開管（両端が開いた管）')+'　'+(v.h===1?'基本振動':v.h+'倍振動'),16,22,'#0f172a',15,true);
    txt('空気の粒は左右に振動（縦波）・ゆっくり表示',624,22,'#64748b',12,false,'right');
    txt('緑の線＝空気の変位を縦向きにかきなおした図',624,40,'#0f766e',12,false,'right');
    ctx.fillStyle='#f1f5f9'; ctx.fillRect(TX0,top,TX1-TX0,bot-top); ctx.strokeStyle='#64748b'; ctx.lineWidth=4; ctx.beginPath(); ctx.moveTo(TX0,top); ctx.lineTo(TX1,top); ctx.moveTo(TX0,bot); ctx.lineTo(TX1,bot); ctx.stroke(); ctx.lineWidth=1;
    if(v.cl){ ctx.fillStyle='#475569'; ctx.fillRect(TX0-12,top-4,12,bot-top+8); }
    for(let i=0;i<36;i++){ const x=(i+0.5)/36*v.Lp; for(let r=0;r<5;r++){ const X=TX0+x*sx+14*u(x)*Math.cos(ph); ctx.fillStyle='#475569'; ctx.beginPath(); ctx.arc(X,81+r*22,2.6,0,TAU); ctx.fill(); } }
    const xs=v.cl?0:-v.dx, xe=v.Lp+v.dx; ctx.setLineDash([5,4]); ctx.strokeStyle='#5eead4'; [1,-1].forEach((s)=>{ ctx.beginPath(); for(let i=0;i<=200;i++){ const x=xs+(xe-xs)*i/200, X=TX0+x*sx, y=yc-s*46*u(x); i?ctx.lineTo(X,y):ctx.moveTo(X,y); } ctx.stroke(); }); ctx.setLineDash([]);
    ctx.strokeStyle='#0f766e'; ctx.lineWidth=2.5; ctx.beginPath(); for(let i=0;i<=200;i++){ const x=xs+(xe-xs)*i/200, X=TX0+x*sx, y=yc-46*u(x)*Math.cos(ph); i?ctx.lineTo(X,y):ctx.moveTo(X,y); } ctx.stroke(); ctx.lineWidth=1;
    const nodes=[], anti=[]; for(let j=0;j<40;j++){ const a=v.cl?j*v.lp/2:-v.dx+v.lp/4+j*v.lp/2, b=v.cl?v.lp/4+j*v.lp/2:-v.dx+j*v.lp/2; if(a<=v.Lp+v.dx+1e-9) nodes.push(a); if(b<=v.Lp+v.dx+1e-9) anti.push(b); }
    nodes.forEach((x)=>txt('節',TX0+x*sx,200,'#7c3aed',13,true,'center')); anti.forEach((x)=>txt('腹',TX0+x*sx,200,'#ea580c',13,true,'center'));
    if(v.dx>0){ [[TX1,TX1+v.dx*sx]].concat(v.cl?[]:[[TX0-v.dx*sx,TX0]]).forEach((q)=>{ ctx.strokeStyle='#c2410c'; ctx.beginPath(); ctx.moveTo(q[0],206); ctx.lineTo(q[1],206); ctx.stroke(); txt('Δx',(q[0]+q[1])/2,220,'#c2410c',12,true,'center'); }); }
    ctx.strokeStyle='#0f172a'; ctx.beginPath(); ctx.moveTo(TX0,226); ctx.lineTo(TX1,226); ctx.moveTo(TX0,221); ctx.lineTo(TX0,231); ctx.moveTo(TX1,221); ctx.lineTo(TX1,231); ctx.stroke();
    txt('L＝'+Math.round(v.Lp*100)+' cm',(TX0+TX1)/2,241,'#0f172a',12,true,'center');
    ctx.fillStyle='#f0fdfa'; rr(16,252,608,108,10); ctx.fill(); ctx.strokeStyle='#99f6e4'; ctx.stroke();
    txt('V ＝ 331.5 ＋ 0.6t ＝ 331.5 ＋ 0.6×'+v.tc+' ＝ '+v.Vs.toFixed(1)+' m/s',30,278,'#0f172a',14,true);
    const Ls=v.dx>0?'('+v.Lp.toFixed(2)+'＋'+(v.cl?'':'2×')+'0.012)':v.Lp.toFixed(2);
    txt(v.cl?'λ ＝ 4'+(v.dx>0?'(L＋Δx)':'L')+'/(2n−1) ＝ 4×'+Ls+' ÷ '+v.h+' ＝ '+g3(v.lp)+' m':'λ ＝ 2'+(v.dx>0?'(L＋2Δx)':'L')+'/n ＝ 2×'+Ls+' ÷ '+v.np+' ＝ '+g3(v.lp)+' m',30,304,'#0f172a',14);
    txt('f ＝ V/λ ＝ '+v.Vs.toFixed(1)+' ÷ '+g3(v.lp)+' ＝ '+hz(v.fp)+' Hz',30,338,'#c2410c',17,true);
    const L6=v.cl?[1,3,5,7,9,11]:[1,2,3,4,5,6];
    harmonics(L6.map((q)=>q*v.fp1),v.np-1,386,v.cl?'この閉管の固有振動数（基本振動数の奇数倍だけ）':'この開管の固有振動数（基本振動数の整数倍）',(i)=>i===0?'基本':L6[i]+'倍');
    if(note) txt(note,16,545,'#dc2626',12,true); }
  function draw(){ ctx.fillStyle='#ffffff'; ctx.fillRect(0,0,W,H); const v=V();
    if(mode==='beat') drawBeat(v); else if(mode==='stand') drawStand(v); else if(mode==='str') drawStr(v); else drawPipe(v);
    if(playing&&mode!=='stand') txt('🔊 再生中（10秒で自動停止）',W-12,H-6,'#dc2626',12,true,'right'); }
  function update(){ const v=V();
    if(mode==='beat'){ const d=Math.abs(v.df); lab('s1','振動数 f₁'); lab('s2','振動数 f₂'); lab('s3','うなりの回数 |f₁−f₂|'); lab('s4','うなりの周期');
      setStat('s1',v.f1+' Hz'); setStat('s2',f1d(v.f2)+' Hz'); setStat('s3',f1d(d)+' 回/秒'); setStat('s4',d>0?(1/d).toFixed(3)+' 秒':'なし');
      setShare('【うなり】'+v.f1+'Hzと'+f1d(v.f2)+'Hzの音を重ねると、1秒間に|f₁−f₂|＝'+f1d(d)+'回うなる｜シミュラボ'); }
    else if(mode==='stand'){ lab('s1','波長 λ'); lab('s2','隣り合う節の間隔 λ/2'); lab('s3','腹と節の間隔 λ/4'); lab('s4','右端');
      setStat('s1',Math.round(v.lam*100)+' cm'); setStat('s2',f1d(v.lam*50)+' cm'); setStat('s3',f1d(v.lam*25)+' cm'); setStat('s4',v.fixed?'固定端→節':'自由端→腹');
      setShare('【定常波】波長'+Math.round(v.lam*100)+'cmの波が'+(v.fixed?'固定端':'自由端')+'で反射してできる定常波は、節の間隔が λ/2＝'+f1d(v.lam*50)+'cm｜シミュラボ'); }
    else if(mode==='str'){ lab('s1','波の速さ v＝√(S/ρ)'); lab('s2','波長 λₙ＝2L/n'); lab('s3','固有振動数 fₙ＝nv/2L'); lab('s4','基本振動数 f₁');
      setStat('s1',g3(v.vs)+' m/s'); setStat('s2',g3(v.ls)+' m'); setStat('s3',hz(v.fs)+' Hz'); setStat('s4',hz(v.fs1)+' Hz');
      setShare('【弦の固有振動】長さ'+v.Ls.toFixed(2)+'m・張力'+v.S+'N・線密度'+f1d(v.rho*1000)+'g/mの弦の'+(v.n===1?'基本振動':v.n+'倍振動')+'は fₙ＝nv/2L＝'+hz(v.fs)+'Hz｜シミュラボ'); }
    else { lab('s1','音速 V＝331.5＋0.6t'); lab('s2','波長 λ'); lab('s3','固有振動数 f'); lab('s4','基本振動数');
      setStat('s1',v.Vs.toFixed(1)+' m/s'); setStat('s2',g3(v.lp)+' m'); setStat('s3',hz(v.fp)+' Hz'); setStat('s4',hz(v.fp1)+' Hz');
      setShare('【気柱の固有振動】'+v.tc+'℃・長さ'+Math.round(v.Lp*100)+'cmの'+(v.cl?'閉管':'開管')+'の'+(v.h===1?'基本振動':v.h+'倍振動')+'は'+hz(v.fp)+'Hz（音速'+v.Vs.toFixed(1)+'m/s）｜シミュラボ'); }
    retune(); }
  const LEG={beat:'青＝振動数 f₁ の音、オレンジ＝f₂ の音、緑＝2つを重ね合わせた合成波。上の3段は短い時間（f₁ の10周期分）を拡大した図、下の段は合成波の全体で、振幅（音の大きさ）の変化を表します。音は「🔊」ボタンを押したときだけ鳴り、10秒で自動的に止まります。はじめは端末の音量を小さくしてください。',
    stand:'入射波と反射波は、振幅・波長・振動数が同じで、進む向きだけが逆の波です。紫の点線＝節の位置（入射波と反射波がいつも打ち消し合う）。合成波の水色の点線は振動のはば（腹で2A）。動きは実際よりゆっくりです。',
    str:'両端（こま）を固定した弦の定常波。水色の点線は振動のはば。張力 S はおもりの重さで決まり、線密度 ρ は弦1mあたりの質量です。「🔊」で、その固有振動数の音（正弦波）を鳴らせます。',
    pipe:'管の中の点は空気の粒（の集まり）で、管の向きに振動する縦波です。緑の線は、その変位を縦向きにかきなおした図で、節・腹は変位の節・腹です。粒の動きは大きく誇張しています。「🔊」で、その固有振動数の音（正弦波）を鳴らせます。'};
  function setMode(){ mode=$('mode').value; stopSound(); note=''; t=0; run=true; $('pause').textContent='⏸ 一時停止';
    ALL.forEach((id)=>{ fld(id).style.display=SH[mode].indexOf(id)>=0?'':'none'; });
    show('p1',mode==='beat'); show('p2',mode==='beat'); show('stepB',mode==='stand'); show('play',mode!=='stand'); show('stopS',mode!=='stand');
    $('play').textContent=mode==='beat'?'🔊 うなりを聞く（f₁＋f₂）':'🔊 この振動数の音を鳴らす';
    const lg=document.querySelector('.lab-legend'); if(lg) lg.textContent=LEG[mode]; update(); }
  function loop(ts){ if(last===null) last=ts; let dt=(ts-last)/1000; last=ts; if(dt>0.1) dt=0.1;
    if(run){ if(playing&&AC&&mode==='beat') t=AC.currentTime-pStart; else t+=dt; } if(t>1e5) t=0;
    draw(); requestAnimationFrame(loop); }
  ['f1','df','lam','Ls','S','rho','n','Lp','temp','np'].forEach((id)=>$(id).addEventListener('input',update));
  ['end','tube','corr'].forEach((id)=>$(id).addEventListener('change',update));
  $('vol').addEventListener('change',()=>{ if(master&&AC) master.gain.setTargetAtTime(+$('vol').value,AC.currentTime,0.02); });
  $('mode').addEventListener('change',setMode);
  $('play').addEventListener('click',()=>playSound('both')); $('p1').addEventListener('click',()=>playSound('p1')); $('p2').addEventListener('click',()=>playSound('p2'));
  $('stopS').addEventListener('click',stopSound);
  $('pause').addEventListener('click',()=>{ run=!run; $('pause').textContent=run?'⏸ 一時停止':'▶ 再開'; });
  $('stepB').addEventListener('click',()=>{ run=false; $('pause').textContent='▶ 再開'; t=(Math.floor(t/2.4*8+1e-6)+1)*2.4/8; });
  document.addEventListener('visibilitychange',()=>{ if(document.hidden) stopSound(); });
  (function(){ const b=document.querySelector('.lab-btns'), c=document.querySelector('.lab-ctl'); if(b&&c&&c.parentNode) c.parentNode.insertBefore(b,c); })();
  setMode(); draw(); requestAnimationFrame(loop);
'''

sim(slug="unari-teijouha", cat="rika", emoji="🎵", score=78,
    title="うなりと定常波のシミュレーター（弦・気柱の固有振動）",
    title_tag="うなり・定常波（定在波）シミュレーター｜うなりの回数|f₁−f₂|と弦・気柱（閉管・開管）の固有振動数を音つきで確かめる",
    meta_desc="高校物理基礎「波・音と振動」をブラウザで再現。2つの音の重ね合わせでうなり（|f₁−f₂|回/秒）を見て聞き、逆向きに進む波から定常波の腹と節ができる様子、弦の固有振動 f＝nv/2L、閉管・開管の気柱の固有振動（音速331.5＋0.6t）を計算つきで確かめられます。",
    og_title="うなりと定常波のシミュレーター（弦・気柱の固有振動）",
    og_desc="うなりの回数|f₁−f₂|を音で確かめ、定常波の腹・節、弦と気柱（閉管・開管）の固有振動数を計算つきで見る。",
    card_desc="2つの音のうなりを見て聞き、定常波の腹と節、弦・閉管・開管の固有振動数を計算つきで確かめる。",
    lead="表示を4つに切りかえて、波の重ね合わせを確かめます。①うなりでは2つの音の波形と合成波を表示し、実際の音も鳴らせます。②定常波では入射波と反射波から腹と節ができる様子を、③弦と④気柱（閉管・開管）では固有振動のようすと振動数の計算を見られます。",
    model="物理基礎 波（音と振動）", level="高校（物理基礎・物理）",
    unit="高等学校 物理基礎 (2)様々な物理現象とエネルギーの利用 (ｱ)波 ㋐波の性質 ㋑音と振動",
    canvas=canvas(640, 550, light=True),
    controls=select("mode", "表示するもの", [("beat", "① うなり"), ("stand", "② 定常波（定在波）"),
                                         ("str", "③ 弦の固有振動"), ("pipe", "④ 気柱（閉管・開管）")])
           + slider("f1", "振動数 f₁", 200, 1000, 440, 1, "{v} Hz") + slider("df", "振動数の差 f₂−f₁", -20, 20, 4, 0.5, "{v} Hz")
           + slider("lam", "波長 λ", 20, 120, 40, 5, "{v} cm")
           + select("end", "右端での反射", [("fixed", "固定端"), ("free", "自由端")])
           + slider("Ls", "弦の長さ L", 0.3, 1.5, 0.5, 0.05, "{v} m") + slider("S", "張力 S", 1, 100, 40, 1, "{v} N")
           + slider("rho", "線密度 ρ", 0.5, 10, 1, 0.1, "{v} g/m") + slider("n", "n（n倍振動）", 1, 6, 2, 1, "n＝{v}")
           + select("tube", "管の種類", [("closed", "閉管（一方が閉じた管）"), ("open", "開管（両方が開いた管）")])
           + slider("Lp", "気柱の長さ L", 10, 100, 50, 1, "{v} cm") + slider("temp", "気温 t", -10, 40, 20, 1, "{v} ℃")
           + slider("np", "何番目の固有振動か", 1, 6, 1, 1, "{v}番目")
           + select("corr", "開口端補正（発展）", [("0", "考えない"), ("1", "考える（Δx＝1.2 cm）")])
           + select("vol", "音量", [("0.08", "小さめ"), ("0.16", "ふつう")]),
    buttons=btn("play", "🔊 うなりを聞く（f₁＋f₂）", True) + btn("p1", "f₁だけ") + btn("p2", "f₂だけ") + btn("stopS", "■ 音を止める")
           + btn("pause", "⏸ 一時停止") + btn("stepB", "▶| 1/8周期すすめる"),
    stats=stats([("s1", "振動数 f₁", False), ("s2", "振動数 f₂", False), ("s3", "うなりの回数", True), ("s4", "うなりの周期", False)]),
    legend="青＝振動数 f₁ の音、オレンジ＝f₂ の音、緑＝2つを重ね合わせた合成波。音は「🔊」ボタンを押したときだけ鳴り、10秒で自動的に止まります。",
    article=UNARI_ARTICLE, faqs=UNARI_FAQS,
    rel=[("wave", "🌊", "波の干渉シミュレーター"), ("doppler", "🚑", "ドップラー効果シミュレーター"), ("mosquito-on", "🦟", "モスキート音テスト"),
         ("building-quake", "🏢", "地震でビルはどう揺れる？"), ("tan-shindou", "🌀", "単振動シミュレーター")],
    js=UNARI_JS)
