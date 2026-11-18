# -*- coding: utf-8 -*-
"""理科の授業向けシミュ：さわれる周期表（2026-11-18）
   shuukihyou … 中2「物質の成り立ち（元素・周期表）」／中3「原子の成り立ちとイオン」／化学基礎「電子配置と周期表（周期律・イオン化エネルギー）」
   元素データ＝ data/shuukihyou.json（PubChem Periodic Table の CSV から data/make_shuukihyou_json.py で作成）"""
import io, os
from common import T, N, P, slider, select, btn, stats

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = io.open(os.path.join(HERE, "data", "shuukihyou.json"), encoding="utf-8").read()
MEXT_CHU = "https://www.mext.go.jp/a_menu/shotou/new-cs/1387016.htm"
MEXT_KOU = "https://www.mext.go.jp/a_menu/shotou/new-cs/1407074.htm"
PUBCHEM = "https://pubchem.ncbi.nlm.nih.gov/periodic-table/"
def A(url, label): return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, label)

SIMS = []

STAGE = r'''
<style>
.pt-wrap{width:100%;max-width:min(760px,100%);min-width:0;justify-self:stretch;margin:0 auto;box-sizing:border-box;overflow-x:auto;-webkit-overflow-scrolling:touch;padding:4px 2px 6px;}
.pt{container-type:inline-size;min-width:560px;display:grid;grid-template-columns:repeat(18,minmax(0,1fr));gap:2px;user-select:none;-webkit-user-select:none;}
.pt .c{position:relative;aspect-ratio:1/1.18;border-radius:5px;background:#e5e7eb;color:#0f172a;cursor:pointer;display:flex;flex-direction:column;align-items:center;justify-content:center;line-height:1;
  transition:background-color .45s,color .45s,transform .18s,box-shadow .2s,opacity .45s;animation:ptIn .5s backwards cubic-bezier(.2,1.4,.4,1);border:0;padding:0;font:inherit;}
.pt .c b{font-size:clamp(10px,2.25cqw,17px);font-weight:800;letter-spacing:-.02em;}
.pt .c i{position:absolute;left:3px;top:2px;font-style:normal;font-size:clamp(6px,1.1cqw,9px);opacity:.75;}
.pt .c u{text-decoration:none;font-size:clamp(5px,1.02cqw,8px);margin-top:2px;white-space:nowrap;opacity:.85;display:none;}
.pt .c em{font-style:normal;font-size:clamp(6px,1.15cqw,9px);margin-top:1px;opacity:.9;font-weight:700;}
@container (min-width:600px){.pt .c u{display:block;}}
.pt .c:hover{transform:translateY(-2px) scale(1.08);z-index:3;box-shadow:0 4px 10px rgba(15,23,42,.25);}
.pt .c.sel{z-index:4;transform:scale(1.14);box-shadow:0 0 0 2px #fff,0 0 0 4px #0e7490,0 6px 16px rgba(14,116,144,.5);}
.pt .c.sel::after{content:"";position:absolute;inset:-4px;border-radius:8px;border:2px solid #22d3ee;animation:ptPulse 1.4s infinite;}
.pt .c.hid{opacity:.13;}
.pt .c.pop{animation:ptPop .6s cubic-bezier(.2,1.6,.4,1);}
.pt .c.unk{background-image:repeating-linear-gradient(135deg,rgba(255,255,255,.55) 0 3px,transparent 3px 7px);}
.pt .c.st-g b{animation:ptFloat 1.6s ease-in-out infinite;}
.pt .c.st-l b{animation:ptSway 2.2s ease-in-out infinite;}
.pt .ph{aspect-ratio:1/1.18;border-radius:5px;border:1.5px dashed #94a3b8;color:#475569;font-size:clamp(6px,1.1cqw,9px);display:flex;align-items:center;justify-content:center;text-align:center;line-height:1.15;}
.pt .gap{grid-column:1/-1;height:6px;}
.pt .gl{font-size:clamp(6px,1.05cqw,9px);color:#64748b;text-align:center;align-self:end;}
@keyframes ptIn{from{opacity:0;transform:translateY(-14px) scale(.6);}}
@keyframes ptPop{0%{transform:scale(.3);}60%{transform:scale(1.35);}100%{transform:scale(1);}}
@keyframes ptPulse{0%{opacity:1;transform:scale(1);}100%{opacity:0;transform:scale(1.35);}}
@keyframes ptFloat{0%,100%{transform:translateY(0);}50%{transform:translateY(-3px);}}
@keyframes ptSway{0%,100%{transform:rotate(0);}50%{transform:rotate(-5deg);}}
@media (prefers-reduced-motion:reduce){.pt .c,.pt .c b,.pt .c.sel::after{animation:none!important;transition:none!important;}}
.pt-scale{width:100%;max-width:640px;min-width:0;display:flex;flex-wrap:wrap;gap:6px 12px;justify-content:center;font-size:12.5px;color:#334155;min-height:22px;}
.pt-scale span{display:inline-flex;align-items:center;gap:5px;}
.pt-scale s{display:inline-block;width:14px;height:14px;border-radius:4px;text-decoration:none;}
.pt-scale .bar{width:200px;height:12px;border-radius:6px;}
.pt-hint{font-size:12px;color:#64748b;margin:-6px 0 0;}
@media (min-width:700px){.pt-hint{display:none;}}
</style>
@@TOPCTL@@
<div class="pt-wrap"><div class="pt" id="pt" role="grid" aria-label="周期表"></div></div>
<p class="pt-hint">← 表は横にスクロールできます →</p>
<div class="pt-scale" id="ptScale"></div>
<canvas id="cv" class="lab" width="640" height="380" aria-label="選んだ元素の原子のモデル（ドラッグで回せます）"></canvas>
<canvas id="gr" class="lab light" width="640" height="210" aria-label="原子番号と性質のグラフ（タップで元素を選べます）"></canvas>
'''

ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
<p>周期表は、118種類の元素を<b>原子番号（陽子の数）</b>の順に並べ、性質の似た元素が縦の列（<b>族</b>）にそろうように折り返した表です。元素をタッチすると、その原子の<b>電子殻（K殻・L殻・M殻…）</b>に電子が入っていくようすが立体のモデルで回り、横の行（<b>周期</b>）が電子殻の数、典型元素の族の一の位が<b>価電子の数</b>と対応していることを確かめられます。表の色を「温度と状態」「イオン化エネルギー」「発見の歴史」などに切り替えると、同じ表の上に元素の性質のくり返し（<b>周期律</b>）が浮かび上がります。</p>
''' + N('<b>対応する単元</b>：中学校 第1分野（4）化学変化と原子・分子「物質の成り立ち」（中学2年：元素と元素記号、周期表で多くの種類の元素があること・金属と非金属）、第1分野（6）化学変化とイオン「原子の成り立ちとイオン」（中学3年：陽子・中性子・電子）。高等学校「化学基礎」（2）物質の構成 ア（ｱ）物質の構成粒子「㋐原子の構造」「㋑電子配置と周期表」（元素の周期律・電子配置と族や周期の関係・イオン化エネルギーの変化）。') + '''
<h2>授業での使い方</h2>
<h3>導入：元素は何種類ある？（中学2年）</h3>
<p>「なかま（金属・非金属）」の色で表全体を見せ、金属が左から中央に多く、非金属が右上に集まっていることに気付かせます。次に「発見の歴史」に切り替えて「▶ 自動で動かす」を押すと、金・銀・銅・鉄・炭素など古くから知られていた元素から始まり、1800年代に一気に増え、2004年に日本の理化学研究所が見つけた<b>ニホニウム（Nh）</b>で表が埋まっていくようすが見られます。</p>
<h3>展開：電子殻と周期・族（中学3年〜化学基礎）</h3>
<p>水素（H）を選んで「陽子を1つ足す ▶」を押していくと、陽子が1個増えるたびに電子が1個ずつ外側から飛んできて、内側の殻から順に入ります。K殻が2個でいっぱいになるとL殻へ、L殻が8個でいっぱいになると次の周期（Na）が始まることを確かめます。そのとき表の上では、選んでいる元素が右へ進み、行の終わり（貴ガス）で次の行の左端に移ります。</p>
<h3>まとめ：周期律をグラフで見る（化学基礎）</h3>
<p>「イオン化エネルギー」に切り替えると、下のグラフに原子番号ごとの第一イオン化エネルギーが描かれます。貴ガス（He・Ne・Ar…）で山になり、アルカリ金属（Li・Na・K…）で谷になる形が周期ごとにくり返すことから、「周期律」という言葉の意味をつかませます。表の色でも、右上ほど濃く左下ほどうすいことが見えます。</p>
<h3>生徒への問いの例</h3>
<ol>
<li>常温（25℃）で液体の元素は2つしかありません。どれとどれだろう？（「温度と状態」で探そう）温度を30℃に上げると、ほかに液体になる元素はあるだろうか？</li>
<li>ナトリウム（Na）とカリウム（K）は同じ1族です。電子配置を比べると、どこが同じで、どこがちがうだろう？</li>
<li>イオン化エネルギーのグラフで、ヘリウムがいちばん高く、リチウムで急に下がるのはなぜだろう？（ヒント：いちばん外側の電子殻と原子核のきょり）</li>
</ol>
<h2>しくみ・解説</h2>
<h3>用語</h3>
<ul>
<li><b>元素</b>とは、物質をつくっている原子の種類のことです。2026年の時点で118種類が確認されています。</li>
<li><b>原子番号</b>とは、原子核の中の<b>陽子の数</b>です。原子全体では電気を帯びていないので、電子の数も原子番号と同じです。</li>
<li><b>電子殻</b>とは、原子核のまわりで電子が入る層のことで、内側から<b>K殻・L殻・M殻・N殻</b>…とよびます。入ることのできる電子の数は最大で2個・8個・18個・32個（内側からn番目の殻は2n²個）です。</li>
<li><b>価電子</b>とは、いちばん外側の殻にあって、化学結合やイオンのでき方に関わる電子です。典型元素では族の番号の一の位と同じ数で（例：1族は1個、17族は7個）、<b>貴ガス（18族）の価電子は0個</b>として扱います。</li>
<li><b>典型元素</b>は1・2族と13〜18族、<b>遷移元素</b>は3〜12族の元素です。遷移元素は、いちばん外側の殻の電子の数が1個か2個のものが多く、横にとなり合う元素どうしの性質も似ています。</li>
<li><b>イオン化エネルギー（第一イオン化エネルギー）</b>とは、原子から電子を1個取り去って1価の陽イオンにするのに必要なエネルギーです。小さいほど陽イオンになりやすい元素です。</li>
<li><b>電気陰性度</b>とは、結合している原子が、共有している電子を引きつける強さの目安です（ここではポーリングの値）。フッ素が最大です。</li>
</ul>
<h3>周期表の主な族の名前</h3>
''' + T([["1族（Hを除く）", "アルカリ金属", "Li・Na・K", "1個", "1価の陽イオンになりやすい。水と激しく反応する"],
          ["2族", "アルカリ土類金属", "Be・Mg・Ca", "2個", "2価の陽イオンになりやすい"],
          ["17族", "ハロゲン", "F・Cl・Br・I", "7個", "1価の陰イオンになりやすい。単体は二原子分子"],
          ["18族", "貴ガス", "He・Ne・Ar", "0個（Heの最外殻は2個）", "ほかの原子とほとんど結びつかない"]],
         ["族", "名前", "例", "価電子", "性質"]) + '''
<h3>電子配置の例</h3>
''' + T([["H（1）", "1", "", "", "", "1"], ["C（6）", "2", "4", "", "", "4"], ["O（8）", "2", "6", "", "", "6"],
          ["Ne（10）", "2", "8", "", "", "0"], ["Na（11）", "2", "8", "1", "", "1"], ["Cl（17）", "2", "8", "7", "", "7"],
          ["Ar（18）", "2", "8", "8", "", "0"], ["K（19）", "2", "8", "8", "1", "1"], ["Ca（20）", "2", "8", "8", "2", "2"]],
         ["元素（原子番号）", "K殻", "L殻", "M殻", "N殻", "価電子"]) + '''
<p>K（カリウム）では、M殻にまだ空き（最大18個）があるのに、9個目の電子がN殻に入ります。これは、M殻の中にもエネルギーの高い部分（3d軌道）があり、N殻の一部（4s軌道）のほうが先に電子が入りやすいためです。高校では、原子番号20（Ca）までの電子配置を中心に学びます。</p>
<h3>状態は融点と沸点で決まる</h3>
<p>「温度と状態」では、それぞれの元素の単体の<b>融点</b>と<b>沸点</b>（1気圧）を、スライダーの温度とくらべて、固体（青）・液体（緑）・気体（オレンジ）に色分けしています。25℃で液体なのは<b>臭素（Br）</b>と<b>水銀（Hg）</b>だけで、セシウム（融点28℃）とガリウム（融点30℃）は手のひらの温度で溶けるほど融点が低い金属です。</p>
''' + P('原子のモデルは、電子が決まった円の上を回る「電子殻のモデル（ボーアのモデル）」で描いています。実際の電子は、雲のように原子核のまわりに広がって存在しています。原子核と電子殻の大きさの比も実際とはまったく異なり（原子核は原子の約10万分の1の大きさ）、見やすいように拡大しています。中性子の数は、原子量を四捨五入した値から陽子の数を引いた目安です（同位体によって異なります）。') + '''
''' + N('<b>データについて</b>：原子量・電子配置・融点・沸点・密度・第一イオン化エネルギー・電気陰性度・発見年は、米国国立衛生研究所（NIH）の ' + A(PUBCHEM, "PubChem Periodic Table") + ' の値を使っています。ヘリウムは1気圧では冷やしても固体にならないため、液体と気体だけで表示しています。炭素（約3640℃）とヒ素（約615℃）は1気圧では液体にならずに<b>昇華</b>するため、その温度で固体から気体に変わるようにしています。原子番号104以降の元素は、できる原子の数がごくわずかで寿命も短いため、性質の多くはわかっておらず、色をうすくしています。金属・非金属の分け方のうち、ホウ素・ケイ素・ゲルマニウム・ヒ素・アンチモン・テルルは両方の性質をもつため「半金属」としました（教科書によって分け方が異なります）。') + '''
<h2>参考</h2>
<ul class="seo-refs">
<li>''' + A(MEXT_CHU, "文部科学省「中学校学習指導要領（平成29年告示）解説 理科編」") + ''' 第1分野（4）化学変化と原子・分子、（6）化学変化とイオン</li>
<li>''' + A(MEXT_KOU, "文部科学省「高等学校学習指導要領（平成30年告示）解説 理科編 理数編」") + ''' 化学基礎（2）物質の構成</li>
<li>''' + A(PUBCHEM, "PubChem Periodic Table（National Center for Biotechnology Information）") + '''</li>
<li>日本化学会「元素の周期表」、中学校理科・高等学校「化学基礎」の教科書</li>
</ul>
'''

FAQS = [
    ("周期表の縦の列と横の行は何を表していますか？", "縦の列を<b>族</b>（1〜18族）、横の行を<b>周期</b>（第1〜第7周期）といいます。同じ族の元素は価電子の数が同じで性質が似ており、周期の番号は電子が入っているいちばん外側の電子殻の番号（電子殻の数）と同じです。"),
    ("常温で液体の元素はどれですか？", "25℃・1気圧で液体の元素は、非金属の<b>臭素（Br）</b>と金属の<b>水銀（Hg）</b>の2つです。セシウム（融点28℃）とガリウム（融点30℃）も、少し温めるだけで液体になります。"),
    ("イオン化エネルギーは周期表でどう変わりますか？", "同じ周期では右へ行くほど大きくなり、貴ガスで最大になります。同じ族では下へ行くほど小さくなります。そのため、周期表の左下の元素ほど陽イオンになりやすく、右上（貴ガスを除く）の元素ほど陰イオンになりやすい傾向があります。"),
    ("貴ガスの価電子が0個なのはなぜですか？", "貴ガスは、いちばん外側の電子殻の電子の数が安定な数（Heは2個、それ以外は8個）になっていて、ほかの原子と結びついたりイオンになったりしにくいためです。化学結合に関わる電子がないという意味で、価電子は0個として扱います。"),
    ("日本で発見された元素はありますか？", "原子番号113の<b>ニホニウム（Nh）</b>は、理化学研究所のグループが2004年に初めて合成し、2016年に「日本」にちなんで命名されました。アジアの国で発見・命名された初めての元素です。"),
    ("中性子の数はどうやって求めますか？", "中性子の数＝質量数−陽子の数（原子番号）です。たとえば質量数23のナトリウムは陽子11個なので、中性子は12個です。同じ元素でも中性子の数がちがう原子（同位体）があります。"),
]

JS = r'''
  const D = ''' + DATA + r''';
  const pt=$('pt'), cv=$('cv'), gr=$('gr');
  const dpr=Math.min(2,window.devicePixelRatio||1);
  const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const GW=gr.width,GH=gr.height; gr.width=GW*dpr; gr.height=GH*dpr; const g2=gr.getContext('2d'); g2.setTransform(dpr,0,0,dpr,0,0);
  const FF='"Hiragino Sans","Hiragino Kaku Gothic ProN","Noto Sans JP","Yu Gothic UI","Yu Gothic",Meiryo,sans-serif';
  function tx(c,s,x,y,size,col,align,bold){ c.font=(bold?'bold ':'')+size+'px '+FF; c.fillStyle=col; c.textAlign=align||'left'; c.fillText(s,x,y); c.textAlign='left'; }
  const SHELL='KLMNOPQ';
  const KIND={h:['水素','#bae6fd'],alkali:['アルカリ金属','#fca5a5'],alkaline:['アルカリ土類金属','#fdba74'],trans:['遷移元素（金属）','#fde68a'],
    metal:['そのほかの金属','#cbd5e1'],half:['半金属','#a7f3d0'],nonmetal:['非金属','#86efac'],halogen:['ハロゲン','#67e8f9'],noble:['貴ガス','#c4b5fd'],
    lan:['ランタノイド（金属）','#fbcfe8'],act:['アクチノイド（金属）','#f0abfc']};
  // 1気圧で昇華する元素（K）・ヘリウムは固体にならない
  const SUBL={6:3915, 33:888};
  D.forEach(e=>{ e.val = (e.g<=2||e.g>=13)&&e.row<8 ? (e.g===18?0:(e.g<=2?e.g:e.g-10)) : null; if(e.z===2) e.val=0;
    e.nn = e.m? Math.max(0,Math.round(e.m)-e.z) : null; e.heavy=e.z>=104; });
  function stateAt(e,K){
    if(SUBL[e.z]) return K<SUBL[e.z]?'s':'g';
    if(e.bp==null) return 'u';
    if(e.z===2) return K<e.bp?'l':'g';
    if(e.mp==null) return 'u';
    if(e.bp<e.mp) return K<e.bp?'s':'g';
    return K<e.mp?'s':(K<e.bp?'l':'g');
  }
  const STC={s:'#60a5fa',l:'#34d399',g:'#fb923c',u:'#e2e8f0'}, STJ={s:'固体',l:'液体',g:'気体',u:'わかっていない'};
  function lerpC(a,b,t){ const p=s=>[1,3,5].map(i=>parseInt(s.substr(i,2),16)); const A=p(a),B=p(b); return 'rgb('+A.map((v,i)=>Math.round(v+(B[i]-v)*t)).join(',')+')'; }
  function ramp(t){ t=clamp(t,0,1); return t<.5? lerpC('#ecfeff','#22d3ee',t*2) : lerpC('#22d3ee','#3730a3',(t-.5)*2); }
  const NUM={ie:{k:'ie',nm:'第一イオン化エネルギー',u:'eV',lo:3.5,hi:25,log:false},en:{k:'en_',nm:'電気陰性度',u:'',lo:.7,hi:4,log:false},
             d:{k:'d',nm:'密度',u:'g/cm³',lo:-4.2,hi:1.36,log:true}};
  const ERA=[[0,'古代〜1600年代','#a16207'],[1799,'1700年代','#d97706'],[1899,'1800年代','#16a34a'],[1945,'1900〜1945年','#0284c7'],[2100,'1946年以降','#7c3aed']];
  function era(y){ for(const r of ERA) if(y<=r[0]) return r; return ERA[ERA.length-1]; }
  function ylab(y){ return y===0?'古代から知られていた':y+'年'; }
  function fmtT(c){ return Math.round(c)+'℃'; }

  // ---- 表をつくる ----
  const cells={};
  (function(){
    const fr=document.createDocumentFragment();
    for(let g=1;g<=18;g++){ const d=document.createElement('div'); d.className='gl'; d.textContent=g; d.style.gridColumn=g; d.style.gridRow=1; fr.appendChild(d); }
    const ph=(r,t)=>{ const d=document.createElement('div'); d.className='ph'; d.style.gridColumn=3; d.style.gridRow=r; d.innerHTML=t; fr.appendChild(d); };
    ph(7,'57–71<br>ランタ<br>ノイド'); ph(8,'89–103<br>アクチ<br>ノイド');
    const gp=document.createElement('div'); gp.className='gap'; gp.style.gridRow=9; fr.appendChild(gp);
    D.forEach(e=>{
      const c=document.createElement('button'); c.type='button'; c.className='c';
      const r = e.row<8 ? e.row+1 : e.row+2;          // 1行目は族の番号
      const col = e.row<8 ? e.g : (e.z-(e.row===8?57:89)+3);
      c.style.gridColumn=col; c.style.gridRow=r; c.style.animationDelay=((col+r)*22)+'ms';
      c.innerHTML='<i>'+e.z+'</i><b>'+e.s+'</b><u'+(e.ja.length>7?' style="transform:scale(.62)"':e.ja.length>5?' style="transform:scale(.8)"':'')+'>'+e.ja+'</u><em></em>';
      c.setAttribute('aria-label',e.ja+' 原子番号'+e.z);
      c.addEventListener('click',()=>{ stopPlay(); select(e.z); });
      fr.appendChild(c); cells[e.z]=c; e.el=c; e.em=c.querySelector('em');
    });
    pt.appendChild(fr);
  })();

  // ---- 状態 ----
  let cur=11, mode=$('mode').value, playing=false, playT=0;
  let yaw=-.5, pitch=.95, drag=null, spin=1;
  let atom={z:0, el:[]};   // 電子のアニメ
  let grAnim=0;
  const temp=$('temp'), year=$('year');
  function showF(id,on){ const f=$(id).closest('.field'); if(f) f.style.display=on?'':'none'; }

  function paint(){
    const K=+temp.value+273.15, Y=+year.value; let sc='';
    D.forEach(e=>{
      const c=e.el; let bg='#e5e7eb', fg='#0f172a', em='', cls='', hid=false;
      if(mode==='kind'){ bg=KIND[e.k][1]; }
      else if(mode==='state'){ const s=stateAt(e,K); bg=STC[s]; cls=s==='u'?'unk':'st-'+s; if(s==='s') fg='#0b2447'; }
      else if(mode==='year'){ if(e.y>Y){ hid=true; } else { const r=era(e.y); bg=r[2]; fg='#fff'; } em=e.y? (e.y>Y?'':String(e.y)) : '古代'; }
      else if(mode==='val'){ if(e.val==null){ bg='#f1f5f9'; fg='#94a3b8'; em='—'; } else { bg=['#c4b5fd','#fca5a5','#fdba74','#fde68a','#d9f99d','#86efac','#67e8f9','#93c5fd'][e.val]||'#ddd'; em=e.val+'個'; } }
      else { const N=NUM[mode], v=e[N.k]; if(v==null){ bg='#e2e8f0'; cls='unk'; } else { const t=((N.log?Math.log10(v):v)-N.lo)/(N.hi-N.lo); bg=ramp(t); fg=t>.62?'#fff':'#0f172a'; em=(mode==='d'&&v<0.01? v.toExponential(0): (+v).toFixed(mode==='en'?2:1)); } }
      if(e.heavy && mode!=='year' && mode!=='kind') cls+=' unk';
      c.style.background=bg; c.style.color=fg; e.em.textContent=em;
      const wasHid=c.classList.contains('hid');
      c.className='c '+cls+(hid?' hid':'')+(e.z===cur?' sel':'');
      if(mode==='year' && wasHid && !hid && playing){ void c.offsetWidth; c.classList.add('pop'); }
      if(e.heavy && mode==='kind') c.style.opacity='.6'; else c.style.opacity='';
    });
    // 凡例
    if(mode==='kind') sc=Object.keys(KIND).map(k=>'<span><s style="background:'+KIND[k][1]+'"></s>'+KIND[k][0]+'</span>').join('')+'<span>（104番以降はうすく表示）</span>';
    else if(mode==='state'){ const n={s:0,l:0,g:0}; D.forEach(e=>{const s=stateAt(e,K); if(n[s]!=null)n[s]++;});
      sc='<span><b>'+fmtT(+temp.value)+'</b>（1気圧）</span>'+['s','l','g'].map(s=>'<span><s style="background:'+STC[s]+'"></s>'+STJ[s]+' '+n[s]+'</span>').join('')+'<span><s style="background:'+STC.u+'"></s>わかっていない</span>'; }
    else if(mode==='year'){ const n=D.filter(e=>e.y<=Y).length; sc='<span><b>'+Y+'年</b>までに <b>'+n+'</b> 種類</span>'+ERA.map(r=>'<span><s style="background:'+r[2]+'"></s>'+r[1]+'</span>').join(''); }
    else if(mode==='val') sc='<span>典型元素の価電子の数（貴ガスは0個）。遷移元素は「—」</span>';
    else { const N=NUM[mode]; sc='<span>'+N.nm+'：小</span><span class="bar" style="background:linear-gradient(90deg,'+[0,.25,.5,.75,1].map(ramp).join(',')+')"></span><span>大'+(N.log?'（目盛りは対数）':'')+'</span>'; }
    $('ptScale').innerHTML=sc;
  }

  function select(z,fromStep){
    cur=clamp(z,1,118); const e=D[cur-1];
    D.forEach(x=>x.el.classList.toggle('sel',x.z===cur));
    if(!fromStep && e.el.scrollIntoView && $('pt').parentNode.scrollWidth>$('pt').parentNode.clientWidth){ const w=$('pt').parentNode; w.scrollLeft=e.el.offsetLeft-w.clientWidth/2; }
    buildAtom(e); updStats(); drawGraph();
  }

  // ---- 原子のモデル ----
  function shellR(n,tot){ const maxR=Math.min(W*.36,H*.42)-6; const inner=26+Math.min(14,Math.cbrt(D[cur-1].z)*3); return inner+(maxR-inner)*(tot<=1?0.25:(n/(Math.max(tot,3)-1))); }
  function buildAtom(e){
    const old=atom.el, prevZ=atom.z; const list=[]; let k=0;
    e.sh.forEach((cnt,n)=>{ for(let i=0;i<cnt;i++){ list.push({n, i, cnt, ph:(i/cnt)*Math.PI*2, t: 1, k:k++}); } });
    // 前の原子にあった電子はそのまま、増えた分は外から飛んでくる
    const keep = Math.abs(e.z-prevZ)===1 || prevZ===0 ? Math.min(prevZ,e.z) : 0;
    list.forEach((p,j)=>{ p.t = (j<keep && prevZ)?1:0; p.delay = (j<keep?0: (j-keep)*0.05); p.a=Math.random()*6.28; });
    atom={z:e.z, el:list, born:performance.now(), sh:e.sh.slice()};
    nucleus(e);
  }
  let NUC=[];
  function nucleus(e){
    const np=Math.min(e.z,40), nn=Math.min(e.nn==null?e.z:e.nn,50), tot=np+nn; NUC=[];
    const R=7+Math.cbrt(tot)*4.2;
    for(let i=0;i<tot;i++){ const y=1-2*(i+.5)/tot, r=Math.sqrt(1-y*y), th=i*2.39996; const f=Math.cbrt((i+1)/tot);
      NUC.push({x:Math.cos(th)*r*R*f, y:y*R*f, z:Math.sin(th)*r*R*f, p: (i*np/tot)%1 < np/tot ? true : (Math.floor(i*np/tot)!==Math.floor((i+1)*np/tot)) }); }
    let pc=0; NUC.forEach((q,i)=>{ q.p = Math.round((i+1)*np/tot)>pc; if(q.p) pc++; });
    NUC.R=R;
  }
  function proj(x,y,z){
    const cy=Math.cos(yaw), sy=Math.sin(yaw), cp=Math.cos(pitch), sp=Math.sin(pitch);
    let X=x*cy+z*sy, Z=-x*sy+z*cy; let Y=y*cp-Z*sp; Z=y*sp+Z*cp;
    const f=520/(520+Z); return [W/2+X*f, H/2+12+Y*f, Z, f];
  }
  let last=performance.now();
  function frame(now){
    const dt=Math.min(.05,(now-last)/1000); last=now;
    if(!drag) yaw+=dt*.25*spin;
    if(playing) stepPlay(dt);
    drawAtom(now/1000, dt);
    if(grAnim<1){ grAnim=Math.min(1,grAnim+dt*1.6); drawGraph(); }
    requestAnimationFrame(frame);
  }
  function drawAtom(t,dt){
    const e=D[cur-1]; const tot=e.sh.length;
    const bg=ctx.createRadialGradient(W/2,H/2,20,W/2,H/2,W*.7); bg.addColorStop(0,'#16213f'); bg.addColorStop(1,'#060a17');
    ctx.fillStyle=bg; ctx.fillRect(0,0,W,H);
    // 輪（殻）— 殻ごとに少し傾けて立体に
    const items=[];
    const age=(performance.now()-atom.born)/1000;
    for(let n=0;n<tot;n++){
      const R=shellR(n,tot), tilt=n*0.0; const outer = n===tot-1;
      ctx.beginPath();
      for(let a=0;a<=64;a++){ const th=a/64*Math.PI*2; const q=proj(Math.cos(th)*R,0,Math.sin(th)*R); a?ctx.lineTo(q[0],q[1]):ctx.moveTo(q[0],q[1]); }
      ctx.strokeStyle= outer&&e.val!=null ? 'rgba(250,204,21,.55)' : 'rgba(148,163,184,.35)'; ctx.lineWidth=outer?1.6:1; ctx.stroke();
      const lq=proj(R,0,0); items.push({z:lq[2]-1000, f:()=>tx(ctx,SHELL[n]+'殻',lq[0]+6,lq[1]-4,11,'rgba(203,213,225,.75)','left')});
    }
    // 電子
    atom.el.forEach(p=>{
      const R=shellR(p.n,tot), sp=1.2/(1+p.n*.55);
      p.a+=dt*sp;
      if(p.t<1 && age>p.delay) p.t=Math.min(1,p.t+dt*1.8);
      const th=p.ph+p.a, e3=1-Math.pow(1-p.t,3);
      const rr = R + (1-e3)*W*.55, yy=(1-e3)*-120;
      const q=proj(Math.cos(th)*rr, yy, Math.sin(th)*rr);
      const valence = p.n===tot-1 && e.val!=null && e.val>0;
      items.push({z:q[2], f:()=>{ const r=4.2*q[3]; if(p.t<1){ ctx.strokeStyle='rgba(125,211,252,'+(.5*(1-p.t))+')'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(q[0],q[1]); ctx.lineTo(q[0]+(q[0]-W/2)*.15,q[1]-18*(1-p.t)); ctx.stroke(); }
        const gg=ctx.createRadialGradient(q[0]-r*.3,q[1]-r*.3,0,q[0],q[1],r*2.2); const col=valence?'250,204,21':'125,211,252';
        gg.addColorStop(0,'rgba('+col+',1)'); gg.addColorStop(.45,'rgba('+col+',.85)'); gg.addColorStop(1,'rgba('+col+',0)');
        ctx.fillStyle=gg; ctx.beginPath(); ctx.arc(q[0],q[1],r*2.2,0,7); ctx.fill(); }});
    });
    // 原子核
    NUC.forEach(nq=>{ const q=proj(nq.x,nq.y,nq.z); items.push({z:q[2], f:()=>{ const r=3.6*q[3]+1.2; const gg=ctx.createRadialGradient(q[0]-r*.4,q[1]-r*.4,0,q[0],q[1],r);
      gg.addColorStop(0,nq.p?'#fecaca':'#f1f5f9'); gg.addColorStop(1,nq.p?'#dc2626':'#64748b'); ctx.fillStyle=gg; ctx.beginPath(); ctx.arc(q[0],q[1],r,0,7); ctx.fill(); }}); });
    items.sort((a,b)=>b.z-a.z).forEach(o=>o.f());
    // 文字
    tx(ctx,e.s,18,52,40,'#f8fafc','left',true);
    tx(ctx,e.ja+'（原子番号 '+e.z+'）',18,76,15,'#cbd5e1','left',true);
    tx(ctx,'陽子 '+e.z+'個（赤）・中性子 '+(e.nn==null?'?':'約'+e.nn)+'個（灰）・電子 '+e.z+'個',18,96,12,'#94a3b8');
    const lines=e.sh.map((c,i)=>SHELL[i]+'殻 '+c);
    lines.forEach((s,i)=>{ const y=30+i*19; const last=i===lines.length-1; ctx.font='bold 13px '+FF; const w=ctx.measureText(s).width+14;
      ctx.fillStyle=last&&e.val!=null?'rgba(250,204,21,.18)':'rgba(148,163,184,.14)'; ctx.fillRect(W-18-w,y-14,w,19); tx(ctx,s,W-25,y,13,last&&e.val!=null?'#fde047':'#e2e8f0','right',true); });
    if(e.val!=null) tx(ctx,'価電子 '+e.val+'個（黄色）',W-18,30+lines.length*19+6,12,'#fde047','right',true);
    if(e.z>20 && e.row<8 && e.g>=3 && e.g<=12) tx(ctx,'遷移元素：内側の殻に電子が入っていく',W-18,30+lines.length*19+6,11,'#cbd5e1','right');
    tx(ctx,'電子殻のモデル（実際の電子は雲のように広がっている）・ドラッグで回せます',W/2,H-10,11,'rgba(148,163,184,.8)','center');
  }
  cv.addEventListener('pointerdown',ev=>{ drag={x:ev.clientX,y:ev.clientY,yaw,pitch}; cv.setPointerCapture(ev.pointerId); });
  cv.addEventListener('pointermove',ev=>{ if(!drag) return; yaw=drag.yaw+(ev.clientX-drag.x)*.012; pitch=clamp(drag.pitch+(ev.clientY-drag.y)*.012,-1.5,1.5); });
  const up=()=>{ drag=null; }; cv.addEventListener('pointerup',up); cv.addEventListener('pointercancel',up);

  // ---- グラフ ----
  const GL=46, GR=14, GT=24, GB=30;
  function gmap(){
    if(mode==='state') return {nm:'融点（青）・沸点（オレンジ）［℃］', max:103, lo:-273, hi:4000, get:e=>null, two:true};
    if(mode==='year') return {nm:'見つかっている元素の数（年ごと）', year:true};
    if(mode==='val') return {nm:'価電子の数（原子番号1〜56の典型元素）', max:56, lo:0, hi:8, get:e=>e.val, bar:true};
    const N=NUM[mode]||NUM.ie; const m=(mode in NUM)?mode:'ie'; const N2=NUM[m];
    return {nm:N2.nm+(N2.u?'［'+N2.u+'］':'')+(mode in NUM?'':'（周期律の例）'), max: m==='d'?96:(m==='en'?96:104), lo:m==='ie'?0:(m==='en'?0:-0.5), hi:m==='ie'?26:(m==='en'?4.2:23), get:e=>e[N2.k], label:m==='ie'};
  }
  function gx(z,max){ return GL+(z-1)/(max-1)*(GW-GL-GR); }
  function drawGraph(){
    const c=g2, M=gmap(); c.clearRect(0,0,GW,GH); c.fillStyle='#fff'; c.fillRect(0,0,GW,GH);
    tx(c,M.nm,GL,16,12.5,'#0f172a','left',true);
    const y0=GH-GB, y1=GT;
    c.strokeStyle='#cbd5e1'; c.lineWidth=1; c.beginPath(); c.moveTo(GL,y1); c.lineTo(GL,y0); c.lineTo(GW-GR,y0); c.stroke();
    if(M.year){
      const ys=[1600,1700,1800,1900,2000,2016]; const X=y=>GL+(y-1600)/(2016-1600)*(GW-GL-GR); const Yv=n=>y0-(n/118)*(y0-y1);
      ys.forEach(y=>{ tx(c,String(y),X(y),y0+14,10,'#64748b','center'); });
      [0,30,60,90,118].forEach(n=>{ tx(c,String(n),GL-6,Yv(n)+4,10,'#64748b','right'); });
      c.beginPath(); let n=D.filter(e=>e.y===0).length; c.moveTo(X(1600),Yv(n));
      const lim=1600+(+year.value-1600)*1;
      for(let y=1601;y<=2016;y++){ if(y>+year.value) break; n+=D.filter(e=>e.y===y).length; c.lineTo(X(y),Yv(n)); }
      c.strokeStyle='#0e7490'; c.lineWidth=2.2; c.stroke();
      const xc=X(+year.value); c.strokeStyle='rgba(14,116,144,.35)'; c.setLineDash([4,4]); c.beginPath(); c.moveTo(xc,y1); c.lineTo(xc,y0); c.stroke(); c.setLineDash([]);
      tx(c,n+'種類',Math.min(xc+6,GW-60),Yv(n)-6,12,'#0e7490','left',true);
      return;
    }
    const max=M.max, Yv=v=>y0-(v-M.lo)/(M.hi-M.lo)*(y0-y1), lim=Math.max(2,Math.round(max*grAnim));
    for(let z=1;z<=max;z+= (max>60?10:5)){ tx(c,String(z),gx(z,max),y0+14,10,'#64748b','center'); }
    tx(c,'原子番号',GW-GR,y0+26,10,'#64748b','right');
    [M.lo,(M.lo+M.hi)/2,M.hi].forEach(v=>tx(c,(Math.abs(v)>=100?Math.round(v):+v.toFixed(1))+'',GL-6,Yv(v)+4,10,'#64748b','right'));
    if(M.two){
      const K=+temp.value; c.strokeStyle='rgba(220,38,38,.45)'; c.setLineDash([5,4]); c.beginPath(); c.moveTo(GL,Yv(K)); c.lineTo(GW-GR,Yv(K)); c.stroke(); c.setLineDash([]);
      tx(c,'いまの温度 '+fmtT(K),GW-GR,Yv(K)-4,10.5,'#dc2626','right',true);
      [['mp','#3b82f6'],['bp','#f97316']].forEach(([k,col])=>{ c.beginPath(); let on=false;
        for(let z=1;z<=lim;z++){ const e=D[z-1]; let v=e[k]; if(SUBL[z]) v=SUBL[z]; if(z===2&&k==='mp') v=null; if(v==null){on=false;continue;} const X=gx(z,max), Y=Yv(v-273.15); on?c.lineTo(X,Y):c.moveTo(X,Y); on=true; }
        c.strokeStyle=col; c.lineWidth=1.6; c.stroke(); });
    } else if(M.bar){
      for(let z=1;z<=lim;z++){ const v=M.get(D[z-1]); if(v==null) continue; const X=gx(z,max); c.fillStyle=z===cur?'#f59e0b':'#67e8f9'; c.fillRect(X-2.5,Yv(v),5,y0-Yv(v)); }
    } else {
      c.beginPath(); let on=false;
      for(let z=1;z<=lim;z++){ const v=M.get(D[z-1]); if(v==null){on=false;continue;} const X=gx(z,max),Y=Yv(M.lo<0?Math.max(v,0):v); on?c.lineTo(X,Y):c.moveTo(X,Y); on=true; }
      c.strokeStyle='#0e7490'; c.lineWidth=1.8; c.stroke();
      if(M.label) [2,10,18,36,54,86].forEach(z=>{ if(z>lim) return; const v=D[z-1].ie; tx(c,D[z-1].s,gx(z,max),Yv(v)-5,10.5,'#6d28d9','center',true); });
      if(M.label) [3,11,19,37,55].forEach(z=>{ if(z>lim) return; const v=D[z-1].ie; tx(c,D[z-1].s,gx(z,max),Yv(v)+13,10.5,'#dc2626','center',true); });
    }
    if(cur<=max){ const X=gx(cur,max); c.strokeStyle='rgba(245,158,11,.6)'; c.lineWidth=1; c.beginPath(); c.moveTo(X,y1); c.lineTo(X,y0); c.stroke();
      const v=M.two?null:M.get(D[cur-1]); if(v!=null && !M.bar){ c.fillStyle='#f59e0b'; c.beginPath(); c.arc(X,Yv(v),4.5,0,7); c.fill(); }
      c.fillStyle='rgba(255,255,255,.9)'; c.fillRect(X-13,y0+3,26,14); tx(c,D[cur-1].s,X,y0+14,11,'#b45309','center',true); }
  }
  gr.addEventListener('pointerdown',ev=>{ const M=gmap(); if(M.year) return; const r=gr.getBoundingClientRect(); const x=(ev.clientX-r.left)*GW/r.width;
    const z=Math.round((x-GL)/(GW-GL-GR)*(M.max-1))+1; if(z>=1&&z<=M.max){ stopPlay(); select(z); } });

  // ---- 統計・シェア ----
  function updStats(){
    const e=D[cur-1], K=+temp.value+273.15;
    setStat('sEl', e.s+' '+e.ja); setStat('sZ', String(e.z)); setStat('sPos','第'+e.p+'周期・'+(e.row<8?e.g+'族':(e.row===8?'ランタノイド':'アクチノイド')));
    setStat('sEc', e.sh.map((c,i)=>SHELL[i]+c).join(' '));
    setStat('sVal', e.val==null?'—':e.val+'個');
    let m='';
    if(mode==='state') m=fmtT(+temp.value)+'で'+STJ[stateAt(e,K)];
    else if(mode==='year') m=e.y?e.y+'年に発見':'古代から';
    else if(mode==='kind') m=KIND[e.k][0];
    else if(mode==='val') m=e.val==null?'遷移元素':'価電子'+e.val+'個';
    else { const N=NUM[mode], v=e[N.k]; m=v==null?'わかっていない':(v+' '+N.u); }
    setStat('sMode', m); $('sModeK') && ($('sModeK').textContent=({kind:'なかま',state:'状態',ie:'イオン化エネルギー',en:'電気陰性度',d:'密度',year:'発見',val:'周期・族'})[mode]);
    setShare('【さわれる周期表】'+e.ja+'（'+e.s+'）：原子番号'+e.z+'・電子配置 '+e.sh.map((c,i)=>SHELL[i]+c).join(' ')+(e.val!=null?'・価電子'+e.val+'個':'')+'｜シミュラボ');
  }
  window.setStat = window.setStat || function(id,v){ const el=$(id); if(el) el.textContent=v; };

  // ---- 自動で動かす ----
  function stepPlay(dt){
    playT+=dt;
    if(mode==='state'){ const v=Math.min(4000,+temp.value+dt*360); temp.value=v; temp.dispatchEvent(new Event('input')); if(v>=4000) stopPlay(); }
    else if(mode==='year'){ const v=Math.min(2016,+year.value+dt*34); year.value=Math.round(v*10)/10; onYear(); if(v>=2016) stopPlay(); }
    else if(playT>0.75){ playT=0; if(cur>=36) { stopPlay(); return; } select(cur+1,true); }
  }
  function startPlay(){
    playing=true; playT=0; $('play').textContent='■ 止める';
    if(mode==='state' && +temp.value>=3990){ temp.value=-273; }
    if(mode==='year'){ if(+year.value>=2015) year.value=1600; onYear(); }
    if(mode!=='state'&&mode!=='year'){ if(cur>=36) cur=0; select(cur===0?1:cur,true); }
  }
  function stopPlay(){ playing=false; $('play').textContent='▶ 自動で動かす'; }
  $('play').addEventListener('click',()=> playing?stopPlay():startPlay());
  $('zp').addEventListener('click',()=>{ stopPlay(); select(cur+1,true); });
  $('zm').addEventListener('click',()=>{ stopPlay(); select(cur-1,true); });
  function onYear(){ const L=$('yearL'); if(L) L.textContent=Math.floor(+year.value)+'年'; paint(); drawGraph(); updStats(); }
  temp.addEventListener('input',()=>{ const L=$('tempL'); if(L) L.textContent=fmtT(+temp.value)+'（'+Math.round(+temp.value+273.15)+' K）'; paint(); drawGraph(); updStats(); });
  year.addEventListener('input',onYear);
  $('mode').addEventListener('change',()=>{ stopPlay(); mode=$('mode').value; showF('temp',mode==='state'); showF('year',mode==='year');
    if(mode==='year' && +year.value>=2016) year.value=2016; grAnim=0; paint(); drawGraph(); updStats(); });
  showF('temp',false); showF('year',false);
  temp.dispatchEvent(new Event('input')); onYear();
  const qz=+(new URLSearchParams(location.search).get('z')||0); if(qz>=1&&qz<=118) cur=qz;
  paint(); select(cur); requestAnimationFrame(frame);
  window.__pt={D, select, stateAt, get cur(){return cur;}, get mode(){return mode;}, setMode:m=>{ $('mode').value=m; $('mode').dispatchEvent(new Event('change')); }};
'''

SIMS.append(dict(
    slug="shuukihyou", cat="rika", emoji="🧪", score=84,
    title="さわれる周期表（電子配置が3Dで回る・温度で状態が変わる・発見の歴史）",
    title_tag="周期表シミュレーター｜タッチで電子配置が3Dで回る・温度で固体/液体/気体・イオン化エネルギーの周期律（中学・高校化学）",
    meta_desc="118元素の周期表をタッチすると、その原子の電子殻（K殻・L殻・M殻）に電子が入るようすが立体で回るシミュレーター。表の色を、金属・非金属のなかま、温度ごとの固体・液体・気体、イオン化エネルギー、電気陰性度、価電子、発見の年に切り替えられ、周期律がグラフでわかる。中2・中3理科、高校「化学基礎」向け。",
    og_title="さわれる周期表｜電子配置が3Dで回る・温度で状態が変わる・発見の歴史",
    og_desc="元素をタッチすると電子が飛んできて殻に入る。温度を上げると表が固体→液体→気体に色を変え、発見の歴史を再生すると表が埋まっていく。イオン化エネルギーの山と谷で周期律が見える。",
    card_desc="元素をタッチすると電子配置が3Dで回る。温度で状態が変わり、発見の歴史を再生すると表が埋まっていく周期表。",
    lead="周期表の元素をタッチすると、下の画面にその原子のモデルが現れ、電子が1個ずつ飛んできて内側の殻から入っていきます（ドラッグで回せます）。「表の色」を切り替えると、金属・非金属のなかま、温度ごとの固体・液体・気体、イオン化エネルギー、価電子の数、発見された年で表が色分けされ、いちばん下のグラフで原子番号との関係を確かめられます。「▶ 自動で動かす」で、温度を上げる・発見の歴史を再生する・水素から順に電子を足す、の動きを見られます。",
    model="中2 物質の成り立ち／中3 原子の成り立ちとイオン／化学基礎 電子配置と周期表",
    level="中学2年・3年、高校（化学基礎）",
    unit="中学校 第1分野（4）化学変化と原子・分子、（6）化学変化とイオン／高等学校 化学基礎（2）物質の構成 ア（ｱ）物質の構成粒子",
    canvas=STAGE.replace("@@TOPCTL@@", '<div class="lab-ctl">' + select("mode", "表の色", [("kind", "なかま（金属・非金属・族）"), ("state", "温度と状態（固体・液体・気体）"),
                                     ("ie", "イオン化エネルギー"), ("en", "電気陰性度"), ("val", "価電子の数"),
                                     ("year", "発見の歴史"), ("d", "密度")])
             + slider("temp", "温度", -273, 4000, 25, 1) + slider("year", "年", 1600, 2016, 2016, 1) + '</div>'),
    controls="",
    buttons=btn("zm", "◀ 陽子を1つ減らす") + btn("zp", "陽子を1つ足す ▶") + btn("play", "▶ 自動で動かす", True),
    stats=stats([("sEl", "元素", True), ("sZ", "原子番号（陽子の数）", False), ("sPos", "周期・族", False), ("sEc", "電子配置", False), ("sVal", "価電子", False), ("sMode", "表の色の値", False)]),
    legend="表の元素をタッチ（またはグラフをタッチ）で選べます。原子のモデルは赤＝陽子・灰＝中性子・水色＝電子・黄色＝価電子。104番以降の元素は性質の多くがわかっていないため、うすく表示しています。",
    article=ARTICLE, faqs=FAQS,
    rel=[("denshi-haichi", "⚛️", "原子の構造と電子配置のシミュレーター（周期表・価電子・イオン）"),
         ("joutai-henka", "🧊", "状態変化と粒子のシミュレーター（固体・液体・気体）"),
         ("bunshi-katachi-3d", "⚛️", "分子の形 3Dビューア"),
         ("chuwa-ion", "⚗️", "酸・アルカリと中和のシミュレーター（BTB溶液の色とイオンのモデル）"),
         ("kagaku-shitsuryou", "🧪", "化学変化と質量シミュレーター（銅・マグネシウムの酸化）")],
    js=JS))
