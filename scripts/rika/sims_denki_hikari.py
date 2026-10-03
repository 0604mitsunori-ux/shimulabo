# -*- coding: utf-8 -*-
"""理科の授業向けシミュ（電気・光）：電気回路（直列・並列・オームの法則）／凸レンズの像（作図）"""
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

MEXT_SHO = "https://www.mext.go.jp/a_menu/shotou/new-cs/1387014.htm"
MEXT_CHU = "https://www.mext.go.jp/a_menu/shotou/new-cs/1387016.htm"
MEXT_KOU = "https://www.mext.go.jp/a_menu/shotou/new-cs/1407074.htm"
def A(url): return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, url)

# ============================================================ 1 電気回路
sim(slug="denki-kairo", cat="rika", emoji="🔌", score=80,
    title="電気回路シミュレーター（直列・並列・オームの法則）",
    title_tag="オームの法則・直列回路・並列回路のシミュレーター｜電流と電圧を回路図とグラフで確かめる",
    meta_desc="直列回路と並列回路で、各部分の電流・電圧と全体の抵抗がどう決まるかを、オームの法則（V＝RI）で確かめる無料シミュレーター。電流の流れを粒で表示し、電圧と電流のグラフも描けます。小4のかん電池のつなぎ方から中2・物理基礎まで授業で使えます。",
    og_title="電気回路シミュレーター（直列・並列・オームの法則）",
    og_desc="直列・並列で電流と電圧はどう変わる？電流の流れを粒で見て、オームの法則をグラフで確かめる。小4〜中2・物理基礎の授業向け。",
    card_desc="かん電池の直列・へい列から抵抗の直列・並列まで。電流の流れを粒で見て、オームの法則をグラフで確かめる。",
    lead="かん電池や抵抗を直列・並列につなぎかえて、回路を流れる電流と各部分の電圧を確かめられます。電流は粒の流れで表し、粒の速さは電流の大きさに比例します。中2モードでは電源の電圧と抵抗をスライダーで変えて、電圧と電流のグラフ（オームの法則）も描けます。",
    model="小4 電流の働き／中2 電流（オームの法則）／物理基礎 電気",
    level="小学4年、中学2年、高校（物理基礎）",
    unit="小学校 第4学年 A（3）電流の働き／中学校 第1分野（3）電流とその利用（ア）電流／高等学校 物理基礎（2）（ウ）電気",
    canvas=canvas(640, 440, light=True),
    controls=select("mode", "学年・モード", [("chu2", "中2 抵抗の直列・並列"), ("sho4", "小4 かん電池のつなぎ方")])
           + select("bat", "かん電池のつなぎ方", [("one", "かん電池1個"), ("ser", "2個の直列つなぎ"), ("par", "2個のへい列つなぎ")])
           + select("load", "つなぐもの", [("bulb", "豆電球"), ("motor", "モーター")])
           + select("conn", "つなぎ方", [("ser", "直列回路"), ("par", "並列回路")])
           + slider("volt", "電源の電圧", 0, 12, 6, 0.5, "{v} V")
           + slider("r1", "抵抗 R<sub>1</sub>", 1, 60, 10, 1, "{v} Ω")
           + slider("r2", "抵抗 R<sub>2</sub>", 1, 60, 20, 1, "{v} Ω")
           + select("gsel", "グラフに描く抵抗", [("all", "R1・R2・回路全体"), ("r1", "R1 だけ"), ("r2", "R2 だけ"), ("tot", "回路全体だけ")]),
    buttons=btn("rev", "🔄 かん電池の向きを反対にする") + btn("rec", "📍 いまの値をグラフに記録", True) + btn("clr", "記録を消す") + btn("ele", "電子の動きで見る"),
    stats=stats([("sI", "全体の電流", True), ("sR", "全体の抵抗", False), ("s1", "R<sub>1</sub> の電圧・電流", False), ("s2", "R<sub>2</sub> の電圧・電流", False)]),
    legend="オレンジの粒＝電流（＋極から出て－極へ流れる）。粒の速さは電流の大きさに比例します。Ⓐ＝電流計、Ⓥ＝電圧計。中2モードでは R1・R2・電源をタップすると、グラフに描く抵抗を選べます。小4モードでは、かん電池をタップすると向きが反対に、豆電球・モーターをタップすると入れかわります。",
    article='''
<h2>このシミュレーションでわかること</h2>
<p>かん電池2個を<b>直列つなぎ</b>にすると回路を流れる電流が大きくなり、豆電球は明るく、モーターは速く回ります。<b>へい列つなぎ</b>では、電流の大きさは1個のときと同じです。抵抗を直列につなぐと全体の抵抗は R<sub>1</sub>＋R<sub>2</sub> に増え、並列につなぐとどちらの抵抗よりも小さくなります。どの抵抗でも、加わる電圧と流れる電流は比例します（<b>オームの法則</b> V＝RI）。</p>
''' + N("対応する単元：小学校第4学年「電流の働き」（乾電池の数とつなぎ方）／中学校第2学年 第1分野（3）「電流とその利用」の（ア）電流（回路と電流・電圧、電流・電圧と抵抗、電気とそのエネルギー）／高等学校「物理基礎」（2）（ウ）電気（物質と電気抵抗）") + '''
<h2>授業での使い方</h2>
<h3>導入：予想を立てる</h3>
<p>小4では「かん電池を2個にすると、豆電球の明るさはどうなるかな」と予想させてから、モードを「小4 かん電池のつなぎ方」にして、1個 → 直列つなぎ → へい列つなぎの順に切りかえます。中2では実験の前に、直列回路と並列回路で各点の電流や各部分の電圧がどうなるかを予想させます。</p>
<h3>展開：実験の結果と比べる</h3>
<p>中2モードで電源の電圧を1 Vずつ上げながら「いまの値をグラフに記録」を押すと、点が原点を通る直線の上に並びます。電圧と電流が比例すること（オームの法則）と、抵抗が大きいほど直線の傾きがゆるやかになることを、実験で描いたグラフと見比べられます。直列・並列を切りかえて、電流計・電圧計の値のきまりを見つけさせる場面にも使えます。</p>
<h3>まとめ：計算問題の確かめ</h3>
<p>練習問題の値（電源の電圧と2つの抵抗）をスライダーで合わせると、全体の抵抗・電流と、それぞれの抵抗の電圧・電流がすぐに表示されます。自分の答えを確かめる使い方ができます。</p>
<p><b>児童・生徒への問いの例</b></p>
<ol>
<li>かん電池2個を直列つなぎにすると、けん流計のはりのふれ方はどう変わるでしょう。へい列つなぎではどうでしょう。（小4）</li>
<li>10 Ωと20 Ωの抵抗を直列につないで6 Vの電圧を加えると、それぞれの抵抗に何Vの電圧が加わるでしょう。（中2　答え：2 Vと4 V）</li>
<li>抵抗を並列につなぐと、全体の抵抗が1つ1つの抵抗より小さくなるのはなぜでしょう。電流の通り道に注目して説明しましょう。（中2・物理基礎）</li>
</ol>
<h2>しくみ・解説</h2>
<h3>オームの法則</h3>
<p>抵抗に流れる電流は、抵抗に加わる電圧に比例します。これをオームの法則といい、電圧を V［V］、抵抗を R［Ω］、電流を I［A］とすると次の式で表します。</p>
''' + N("V＝R×I　（変形すると I＝V÷R、R＝V÷I）<br>1 A＝1000 mA（例：0.2 A＝200 mA）") + '''
<p>電圧を横軸、電流を縦軸にとったグラフは原点を通る直線になり、抵抗が大きいほど直線の傾きがゆるやかになります（同じ電圧でも電流が流れにくいため）。</p>
<h3>直列回路と並列回路のきまり</h3>
''' + T([["電流", "どこでも同じ<br>I＝I<sub>1</sub>＝I<sub>2</sub>", "枝分かれした電流の和が全体の電流<br>I＝I<sub>1</sub>＋I<sub>2</sub>"],
          ["電圧", "各抵抗の電圧の和が電源の電圧<br>V＝V<sub>1</sub>＋V<sub>2</sub>", "どの抵抗にも電源と同じ電圧<br>V＝V<sub>1</sub>＝V<sub>2</sub>"],
          ["全体の抵抗", "R＝R<sub>1</sub>＋R<sub>2</sub><br>（どちらの抵抗よりも大きい）", "1/R＝1/R<sub>1</sub>＋1/R<sub>2</sub><br>（どちらの抵抗よりも小さい）"],
          ["電力が大きいのは", "抵抗の大きいほう", "抵抗の小さいほう"]], ["", "直列回路", "並列回路"]) + '''
<h3>計算問題の解き方（電源6 V、R<sub>1</sub>＝10 Ω、R<sub>2</sub>＝20 Ω）</h3>
<p><b>直列</b>：全体の抵抗は 10＋20＝30 Ω。電流は 6÷30＝0.2 A。R<sub>1</sub>の電圧は 10×0.2＝2 V、R<sub>2</sub>の電圧は 20×0.2＝4 V で、合計すると電源の6 Vになります。</p>
<p><b>並列</b>：どちらの抵抗にも6 Vが加わるので、R<sub>1</sub>には 6÷10＝0.6 A、R<sub>2</sub>には 6÷20＝0.3 A が流れます。全体の電流は 0.6＋0.3＝0.9 A、全体の抵抗は 6÷0.9＝約6.7 Ω です（1/R＝1/10＋1/20＝3/20 から R＝20/3 Ω と求めることもできます）。</p>
''' + T([["直列", "30 Ω", "0.2 A", "2 V・0.2 A・0.4 W", "4 V・0.2 A・0.8 W"],
          ["並列", "約6.7 Ω", "0.9 A", "6 V・0.6 A・3.6 W", "6 V・0.3 A・1.8 W"]],
         ["つなぎ方", "全体の抵抗", "全体の電流", "R<sub>1</sub>（10 Ω）", "R<sub>2</sub>（20 Ω）"]) + '''
<h3>かん電池のつなぎ方（小4）</h3>
''' + T([["かん電池1個", "0.2 A", "ふつう（くらべるもとにする）", "ふつう", "0.2 A"],
          ["2個の直列つなぎ", "0.4 A（1個の2倍）", "明るくなる", "速く回る", "0.4 A"],
          ["2個のへい列つなぎ", "0.2 A（1個と同じ）", "1個のときと同じ", "1個のときと同じ", "0.1 A（長持ち）"]],
         ["つなぎ方", "回路を流れる電流", "豆電球", "モーター", "かん電池1個に流れる電流"]) + '''
<p>直列つなぎでは2個分の電圧（1.5 V＋1.5 V＝3.0 V）が回路に加わるので、電流が大きくなります。へい列つなぎでは電圧は1個分のままですが、回路の電流を2個のかん電池が半分ずつ受け持つので、1個のときより長持ちします。かん電池の向きを反対にすると、電流の向きが反対になり、けん流計のはりのふれる向きやモーターの回る向きが反対になります（豆電球の明るさは変わりません）。</p>
<h3>電力と明るさ・発熱</h3>
<p>豆電球の明るさや電熱線の発熱は、電力 P＝V×I［W］が大きいほど大きくなります。直列回路では電流が同じなので<b>抵抗の大きいほう</b>の電圧と電力が大きく、並列回路では電圧が同じなので<b>抵抗の小さいほう</b>の電流と電力が大きくなります。シミュレーターでは、電力が大きい抵抗ほど明るく光るように描いています。</p>
<h3>物理基礎とのつながり</h3>
<p>導線の抵抗は長さに比例し、断面積に反比例します（R＝ρL/S、ρは抵抗率）。抵抗を直列につなぐことは導線を長くすること、並列につなぐことは導線を太くすることにあたるので、直列では全体の抵抗が大きく、並列では小さくなります。</p>
<h3>このシミュレーションで単純化していること</h3>
<ul>
<li>かん電池は1個1.5 Vとし、電池の中の抵抗（内部抵抗）は0としています。</li>
<li>豆電球とモーターは、どちらも7.5 Ωの一定の抵抗とみなしています。実際の豆電球はフィラメントが熱くなると抵抗が大きくなるため、直列つなぎにしたときの電流は2倍より少し小さくなります。モーターに流れる電流も、回る速さや羽根の重さで変わります。</li>
<li>抵抗 R<sub>1</sub>・R<sub>2</sub> は温度で値が変わらないものとし、電流計・電圧計は回路に影響しない理想的なものとしています。</li>
<li>粒の速さは電流の大きさを表すイメージです（電流がとても大きいときは、各部分の速さの比を保ったまま上限をつけています）。実際の電子の平均の速さはとても遅く、断面積1 mm²の銅線に1 Aの電流が流れるときで、1秒に0.1 mmにも届きません。</li>
<li>モーターの回転は、見やすいようにゆっくり表示しています。</li>
</ul>
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「小学校学習指導要領（平成29年告示）解説 理科編」第4学年 A（3）電流の働き　''' + A(MEXT_SHO) + '''</li>
<li>文部科学省「中学校学習指導要領（平成29年告示）解説 理科編」第1分野（3）電流とその利用　''' + A(MEXT_CHU) + '''</li>
<li>文部科学省「高等学校学習指導要領（平成30年告示）解説 理科編 理数編」物理基礎（2）（ウ）電気　''' + A(MEXT_KOU) + '''</li>
<li>中学校理科の教科書（東京書籍「新しい科学」2年、啓林館「未来へひろがるサイエンス」2年 など）の「電流」の単元</li>
<li>小学校理科の教科書（第4学年「電流のはたらき」）</li>
<li>日本産業規格 JIS C 0617（電気用図記号）</li>
</ul>
''',
    faqs=[("直列回路と並列回路は何がちがうの？", "直列回路は電流の通り道が1本で、どこでも電流の大きさが同じです。電圧は各抵抗に分かれて加わり、その和が電源の電圧になります。並列回路は通り道が枝分かれしていて、どの抵抗にも電源と同じ電圧が加わり、枝分かれした電流の和が全体の電流になります。"),
          ("オームの法則の式はどう使い分ければいい？", "V＝R×I を基本に、電流を求めるときは I＝V÷R、抵抗を求めるときは R＝V÷I と変形します。電流が mA で書かれているときは、1000で割って A に直してから計算します（例：200 mA＝0.2 A）。"),
          ("並列につなぐと全体の抵抗が小さくなるのはなぜ？", "電流の通り道が増えるからです。導線を太くすると電流が流れやすくなるのと同じで、同じ電圧でも全体の電流が大きくなるので、全体の抵抗（電圧÷電流）は小さくなります。同じ抵抗2個を並列につなぐと、全体の抵抗は1個の半分です。"),
          ("かん電池をへい列つなぎにすると長持ちするのはなぜ？", "へい列つなぎでは、回路を流れる電流を2個のかん電池が半分ずつ受け持つからです。1個あたりの電流が少ないので、1個のときと同じ明るさのまま長い時間使えます。直列つなぎは電流が大きくなるぶん、早く使い切ります。"),
          ("電流計と電圧計はどうつなぐの？", "電流計ははかりたい部分に直列に、電圧計ははかりたい部分に並列につなぎます。値の見当がつかないときは、－端子を最も大きい値の端子（電流計は5 A、電圧計は300 V）につなぎ、針のふれを見てから小さい値の端子につなぎかえます。"),
          ("同じ豆電球2個を直列につなぐと暗くなるのはなぜ？", "電源の電圧が2個の豆電球に分かれて加わるので、1個あたりの電圧と電流が小さくなり、電力が小さくなるからです。並列につなぐと、どちらの豆電球にも電源と同じ電圧が加わるので、1個のときと同じ明るさになります。")],
    rel=[("magnet", "🧲", "磁力線シミュレーター"), ("denkidai-keisan", "💡", "電気代計算機"), ("led-setsuyaku", "💡", "LED電球の節約シミュ"), ("solar-hatsuden", "🔋", "今日のソーラー発電シミュ")],
    js=r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const FF='"Hiragino Sans","Hiragino Kaku Gothic ProN","Noto Sans JP","Yu Gothic UI","Yu Gothic",Meiryo,sans-serif';
  const C={bg:'#f8fafc',wire:'#334155',cur:'#f97316',ele:'#2563eb',r1:'#7c3aed',r2:'#059669',tot:'#111827',am:'#0e7490',vm:'#b45309',ink:'#0f172a',sub:'#64748b',grid:'#e2e8f0'};
  const RL=7.5, E1=1.5, NB=' ';
  const Q=new URLSearchParams(location.search);
  const QK=['mode','bat','load','conn','volt','r1','r2','gsel'];
  QK.forEach(k=>{ const el=$(k); if(!el||!Q.has(k)) return; const v=Q.get(k); if(el.tagName==='SELECT'&&![].some.call(el.options,o=>o.value===v)) return; el.value=v; el.dispatchEvent(new Event('input')); });
  let rev=Q.get('rev')==='1', ele=Q.get('ele')==='1', recs=[], last=0, ang=0;
  const off={};
  const fmt=v=>{ if(!isFinite(v)) return '—'; const a=Math.abs(v); let s=a>=100?v.toFixed(0):a>=10?v.toFixed(1):a>=1?v.toFixed(2):v.toFixed(3); if(s.indexOf('.')>=0) s=s.replace(/0+$/,'').replace(/\.$/,''); return s; };
  const amp=v=>fmt(v)+NB+'A';
  const fld=id=>$(id).closest('.field');
  const K=id=>$(id).previousElementSibling;
  function sh(id,m,sub){ const e=$(id); if(e) e.innerHTML=m+(sub?'<span style="display:block;font-size:12px;font-weight:700;color:#59616c;margin-top:2px">'+sub+'</span>':''); }

  function calc(){ const mode=$('mode').value;
    if(mode==='sho4'){ const bat=$('bat').value, V=bat==='ser'?2*E1:E1, I=V/RL; return {mode:mode,bat:bat,load:$('load').value,V:V,I:I,Ic:bat==='par'?I/2:I,P:I*I*RL}; }
    const V=+$('volt').value, R1=+$('r1').value, R2=+$('r2').value, ser=$('conn').value==='ser'; let R,I,V1,V2,I1,I2;
    if(ser){ R=R1+R2; I=V/R; I1=I; I2=I; V1=I*R1; V2=I*R2; } else { R=R1*R2/(R1+R2); V1=V; V2=V; I1=V/R1; I2=V/R2; I=I1+I2; }
    return {mode:mode,ser:ser,V:V,R1:R1,R2:R2,R:R,I:I,V1:V1,V2:V2,I1:I1,I2:I2}; }

  // 電流の通り道（粒が流れる経路）。I の符号が向き
  function paths(s){
    if(s.mode==='sho4'){ const g=rev?-1:1, Y=340, L=70, R=430, T=150;
      if(s.bat==='par') return [{id:'4m',pts:[[335,Y],[R,Y],[R,T],[L,T],[L,Y],[165,Y]],I:g*s.I},{id:'4a',pts:[[165,Y],[335,Y]],I:g*s.I/2},{id:'4b',pts:[[165,Y],[165,400],[335,400],[335,Y]],I:g*s.I/2}];
      const x1=s.bat==='ser'?140:195, x2=s.bat==='ser'?360:305;
      return [{id:'4'+s.bat,pts:[[x2,Y],[R,Y],[R,T],[L,T],[L,Y],[x1,Y],[x2,Y]],I:g*s.I}]; }
    const g=ele?-1:1;
    if(s.ser) return [{id:'s',pts:[[55,235],[55,95],[375,95],[375,375],[55,375],[55,235]],I:g*s.I}];
    return [{id:'pm',pts:[[55,235],[55,95],[145,95]],I:g*s.I},{id:'p1',pts:[[145,95],[375,95],[375,205]],I:g*s.I1},{id:'p2',pts:[[145,95],[145,205],[375,205]],I:g*s.I2},{id:'pr',pts:[[375,205],[375,375],[55,375],[55,235]],I:g*s.I}]; }
  function ptAt(P,s){ for(let i=1;i<P.length;i++){ const dx=P[i][0]-P[i-1][0], dy=P[i][1]-P[i-1][1], l=Math.hypot(dx,dy); if(s<=l) return [P[i-1][0]+dx*s/l, P[i-1][1]+dy*s/l]; s-=l; } return P[P.length-1]; }
  function drawDots(ps,k,dt,col){ let mx=0; ps.forEach(p=>{ mx=Math.max(mx,Math.abs(p.I)); }); const sc=(k*mx>420)?420/(k*mx):1;
    ctx.fillStyle=col;
    ps.forEach(p=>{ let L=0; for(let i=1;i<p.pts.length;i++) L+=Math.hypot(p.pts[i][0]-p.pts[i-1][0],p.pts[i][1]-p.pts[i-1][1]);
      const a=p.pts[0], z=p.pts[p.pts.length-1], closed=a[0]===z[0]&&a[1]===z[1];
      const gap=closed?L/Math.max(1,Math.round(L/18)):18;
      const o=(((off[p.id]||0)+k*p.I*sc*dt)%gap+gap)%gap; off[p.id]=o;
      for(let s=o; s<L-0.5; s+=gap){ const q=ptAt(p.pts,s); ctx.beginPath(); ctx.arc(q[0],q[1],3.3,0,7); ctx.fill(); } }); }

  // ---- 描画の部品 ----
  function mix(a,b,t){ const p=h=>[1,3,5].map(i=>parseInt(h.substr(i,2),16)); const A=p(a),B=p(b); return 'rgb('+A.map((x,i)=>Math.round(x+(B[i]-x)*t)).join(',')+')'; }
  function tx(s,x,y,size,col,align,bold){ const parts=String(s).split(/_(\d)/); const fs=n=>(bold?'bold ':'')+n+'px '+FF; let w=0;
    const seg=parts.map((t,i)=>{ const sub=i%2===1; ctx.font=fs(sub?Math.round(size*0.72):size); const m=ctx.measureText(t).width; w+=m; return [t,sub,m]; });
    let cx=align==='center'?x-w/2:align==='right'?x-w:x; ctx.fillStyle=col; ctx.textAlign='left';
    seg.forEach(g=>{ if(!g[0]) return; ctx.font=fs(g[1]?Math.round(size*0.72):size); ctx.fillText(g[0],cx,y+(g[1]?size*0.25:0)); cx+=g[2]; }); return w; }
  function rr(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
  function wire(pts,w){ ctx.strokeStyle=C.wire; ctx.lineWidth=w||3; ctx.lineJoin='round'; ctx.lineCap='round'; ctx.beginPath(); pts.forEach((p,i)=>{ if(i) ctx.lineTo(p[0],p[1]); else ctx.moveTo(p[0],p[1]); }); ctx.stroke(); }
  function jdot(x,y,r){ ctx.fillStyle=C.wire; ctx.beginPath(); ctx.arc(x,y,r||4.5,0,7); ctx.fill(); }
  function meter(x,y,ch,col,r){ r=r||16; ctx.fillStyle='#fff'; ctx.strokeStyle=col; ctx.lineWidth=2.5; ctx.beginPath(); ctx.arc(x,y,r,0,7); ctx.fill(); ctx.stroke(); tx(ch,x,y+5,r>15?15:13,col,'center',true); }
  function pill(x,y,t,col,align){ ctx.font='bold 13px '+FF; const w=ctx.measureText(t).width+12; const x0=align==='left'?x:align==='right'?x-w:x-w/2; ctx.fillStyle='#fff'; ctx.strokeStyle=col; ctx.lineWidth=1.5; rr(x0,y-10,w,20,6); ctx.fill(); ctx.stroke(); ctx.fillStyle=col; ctx.textAlign='left'; ctx.fillText(t,x0+6,y+5); }
  function arrowHead(x,y,dir,col){ const d={up:[0,-1],down:[0,1],left:[-1,0],right:[1,0]}[dir]; const px=-d[1], py=d[0]; ctx.fillStyle=col; ctx.beginPath(); ctx.moveTo(x+d[0]*8,y+d[1]*8); ctx.lineTo(x-d[0]*6+px*7,y-d[1]*6+py*7); ctx.lineTo(x-d[0]*6-px*7,y-d[1]*6-py*7); ctx.closePath(); ctx.fill(); }
  function resistor(x,y,P,col){ const b=Math.min(1,Math.sqrt(Math.max(0,P)/7.2));
    if(b>0.02){ const r=24+44*b; const g=ctx.createRadialGradient(x,y,6,x,y,r); g.addColorStop(0,'rgba(251,191,36,'+(0.15+0.55*b).toFixed(3)+')'); g.addColorStop(1,'rgba(251,191,36,0)'); ctx.fillStyle=g; ctx.beginPath(); ctx.arc(x,y,r,0,7); ctx.fill(); }
    ctx.fillStyle=mix('#ffffff','#fb923c',b*0.85); ctx.strokeStyle=col; ctx.lineWidth=2.5; ctx.fillRect(x-30,y-11,60,22); ctx.strokeRect(x-30,y-11,60,22); }
  function supply(x,y,V){ ctx.fillStyle=C.bg; ctx.fillRect(x-24,y-6,48,12); ctx.strokeStyle=C.ink; ctx.lineCap='butt'; ctx.lineWidth=2.5; ctx.beginPath(); ctx.moveTo(x-20,y-7); ctx.lineTo(x+20,y-7); ctx.stroke(); ctx.lineWidth=6; ctx.beginPath(); ctx.moveTo(x-10,y+7); ctx.lineTo(x+10,y+7); ctx.stroke(); ctx.lineCap='round';
    tx('＋',x-31,y-2,14,C.ink,'center',true); tx('－',x-31,y+20,14,C.ink,'center',true); tx('電源',x+30,y-6,12,C.sub,'left'); tx(fmt(V)+' V',x+30,y+13,15,C.ink,'left',true); }
  function rlab(x,y,nm,R,P,col){ tx(nm+' = '+fmt(R)+' Ω',x,y,13,col,'center',true); tx('電力 '+fmt(P)+' W',x,y+15,11,C.sub,'center'); }

  // ---- 中2：抵抗の直列・並列 ----
  function draw2(s,dt){ const T=95, B=375, Lx=55, Rx=375;
    tx(s.ser?'直列回路':'並列回路',14,24,15,C.ink,'left',true);
    wire([[Lx,T],[Rx,T],[Rx,B],[Lx,B],[Lx,T]]);
    if(!s.ser) wire([[145,T],[145,205],[Rx,205]]);
    const lead=(x1,x2,y,ym,mx)=>{ wire([[x1,y],[x1,ym],[mx-16,ym]],1.8); wire([[x2,y],[x2,ym],[mx+16,ym]],1.8); };
    if(s.ser){ lead(165,225,T,38,195); lead(275,335,T,38,305); } else { lead(265,325,T,38,295); lead(265,325,205,262,295); }
    drawDots(paths(s),200,dt,ele?C.ele:C.cur);
    supply(Lx,235,s.V);
    if(s.ser){
      meter(105,T,'A',C.am); resistor(195,T,s.V1*s.I1,C.r1); resistor(305,T,s.V2*s.I2,C.r2);
      [165,225,275,335].forEach(x=>jdot(x,T,3.5)); meter(195,38,'V_1',C.vm); meter(305,38,'V_2',C.vm);
      pill(105,62,amp(s.I),C.am); pill(214,38,fmt(s.V1)+' V',C.vm,'left'); pill(324,38,fmt(s.V2)+' V',C.vm,'left');
      rlab(195,124,'R_1',s.R1,s.V1*s.I1,C.r1); rlab(305,124,'R_2',s.R2,s.V2*s.I2,C.r2);
    } else {
      jdot(145,T); jdot(Rx,205); meter(100,T,'A',C.am); meter(190,T,'A_1',C.am,15); meter(190,205,'A_2',C.am,15);
      resistor(295,T,s.V1*s.I1,C.r1); resistor(295,205,s.V2*s.I2,C.r2);
      [[265,T],[325,T],[265,205],[325,205]].forEach(p=>jdot(p[0],p[1],3.5)); meter(295,38,'V_1',C.vm); meter(295,262,'V_2',C.vm);
      pill(100,62,amp(s.I),C.am); pill(190,62,amp(s.I1),C.am); pill(190,178,amp(s.I2),C.am); pill(314,38,fmt(s.V1)+' V',C.vm,'left'); pill(314,262,fmt(s.V2)+' V',C.vm,'left');
      rlab(295,124,'R_1',s.R1,s.V1*s.I1,C.r1); rlab(295,168,'R_2',s.R2,s.V2*s.I2,C.r2);
    }
    const fl=s.ser?[['電流','I = I_1 = I_2 = '+amp(s.I)],['電圧','V = V_1 + V_2 = '+fmt(s.V1)+' + '+fmt(s.V2)+' = '+fmt(s.V)+' V'],['抵抗','R = R_1 + R_2 = '+fmt(s.R1)+' + '+fmt(s.R2)+' = '+fmt(s.R)+' Ω'],['オームの法則',s.V>0?'I = V÷R = '+fmt(s.V)+'÷'+fmt(s.R)+' = '+amp(s.I):'電圧が0 Vなので電流は流れない']]
                 :[['電圧','V = V_1 = V_2 = '+fmt(s.V)+' V'],['電流','I = I_1 + I_2 = '+fmt(s.I1)+' + '+fmt(s.I2)+' = '+amp(s.I)],['抵抗','1/R = 1/R_1 + 1/R_2 → R = '+fmt(s.R)+' Ω'],['オームの法則',s.V>0?'R = V÷I = '+fmt(s.V)+'÷'+fmt(s.I)+' = '+fmt(s.R)+' Ω':'電圧が0 Vなので電流は流れない']];
    const fx=s.ser?100:96, fy=s.ser?286:300, fh=s.ser?22:20;
    fl.forEach((r,i)=>{ const w=tx(r[0]+'：',fx,fy+i*fh,12,C.sub,'left',true); tx(r[1],fx+w,fy+i*fh,13,C.ink,'left'); });
    tx(ele?'● 電子の動き（－極から＋極へ）':'● 電流の向き（＋極から出て－極へ）',14,404,12,ele?C.ele:C.cur,'left',true);
    tx('粒の速さは電流の大きさに比例',14,424,11.5,C.sub,'left'); }

  function niceStep(x){ if(!(x>0)) return 1; const e=Math.pow(10,Math.floor(Math.log10(x))), f=x/e; return (f<=1?1:f<=2?2:f<=2.5?2.5:f<=5?5:10)*e; }
  function graph(s){ const gx=447, gy=396, gw=181, gh=316, VM=12;
    tx('電圧と電流の関係',410,22,13,C.ink,'left',true); tx('オームの法則  V = R × I',410,40,11.5,C.sub,'left');
    const sel=$('gsel').value, L=[];
    if(sel==='all'||sel==='r1') L.push({k:'r1',R:s.R1,col:C.r1,v:s.V1,i:s.I1,nm:'R_1'});
    if(sel==='all'||sel==='r2') L.push({k:'r2',R:s.R2,col:C.r2,v:s.V2,i:s.I2,nm:'R_2'});
    if(sel==='all'||sel==='tot') L.push({k:'tot',R:s.R,col:C.tot,v:s.V,i:s.I,nm:'全体',dash:true});
    let im=0; L.forEach(l=>{ im=Math.max(im,VM/l.R); }); const st=niceStep(im/4), YM=Math.ceil(im/st-1e-9)*st;
    const X=v=>gx+v/VM*gw, Y=i=>gy-i/YM*gh;
    ctx.fillStyle='#fff'; ctx.fillRect(gx,gy-gh,gw,gh);
    ctx.strokeStyle=C.grid; ctx.lineWidth=1;
    for(let v=3;v<=VM;v+=3){ ctx.beginPath(); ctx.moveTo(X(v),gy); ctx.lineTo(X(v),gy-gh); ctx.stroke(); }
    for(let i=st;i<=YM+1e-9;i+=st){ ctx.beginPath(); ctx.moveTo(gx,Y(i)); ctx.lineTo(gx+gw,Y(i)); ctx.stroke(); }
    ctx.strokeStyle=C.ink; ctx.lineWidth=1.5; ctx.beginPath(); ctx.moveTo(gx,gy-gh); ctx.lineTo(gx,gy); ctx.lineTo(gx+gw,gy); ctx.stroke();
    for(let v=0;v<=VM;v+=3) tx(String(v),X(v),gy+15,11,C.sub,'center');
    for(let i=0;i<=YM+1e-9;i+=st) tx(fmt(i),gx-5,Y(i)+4,11,C.sub,'right');
    tx('電流 [A]',410,64,11,C.sub,'left'); tx('電圧 [V]',gx+gw,gy+32,11,C.sub,'right');
    if(sel==='all'&&s.V>0){ ctx.setLineDash([4,4]); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1.2; ctx.beginPath();
      if(s.ser){ ctx.moveTo(gx,Y(s.I)); ctx.lineTo(X(s.V),Y(s.I)); } else { ctx.moveTo(X(s.V),gy); ctx.lineTo(X(s.V),Y(s.I)); }
      ctx.stroke(); ctx.setLineDash([]);
      if(s.ser) tx('電流は同じ',Math.min(X(Math.max(s.V1,s.V2,s.V))+8,gx+gw-58),Math.min(gy-4,Y(s.I)+15),11,C.sub,'left',true); else { if(X(s.V)+62<gx+gw) tx('電圧は同じ',X(s.V)+5,gy-8,11,C.sub,'left',true); else tx('電圧は同じ',X(s.V)-5,gy-8,11,C.sub,'right',true); } }
    L.forEach(l=>{ const ve=Math.min(VM,YM*l.R); ctx.strokeStyle=l.col; ctx.lineWidth=2.5; ctx.setLineDash(l.dash?[7,5]:[]); ctx.beginPath(); ctx.moveTo(X(0),Y(0)); ctx.lineTo(X(ve),Y(ve/l.R)); ctx.stroke(); ctx.setLineDash([]);
      if(ve<VM-1e-9) tx(l.nm,X(ve)+4,Y(ve/l.R)+14,12,l.col,'left',true); else tx(l.nm,X(VM)-3,Y(VM/l.R)-6,12,l.col,'right',true); });
    recs.forEach(r=>{ L.forEach(l=>{ const p=r[l.k]; ctx.strokeStyle=l.col; ctx.lineWidth=2; ctx.fillStyle='#fff'; ctx.beginPath(); ctx.arc(X(p[0]),Y(p[1]),4.5,0,7); ctx.fill(); ctx.stroke(); }); });
    L.forEach(l=>{ ctx.fillStyle=l.col; ctx.strokeStyle='#fff'; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(X(l.v),Y(l.i),6,0,7); ctx.fill(); ctx.stroke(); });
    L.forEach((l,k)=>{ const t=l.i>0?l.nm+'：'+fmt(l.v)+'÷'+fmt(l.i)+' = '+fmt(l.R)+' Ω':l.nm+' = '+fmt(l.R)+' Ω'; tx(t,gx+6,gy-gh+16+k*17,11.5,l.col,'left',true); });
    if(recs.length) tx('記録 '+recs.length+'回',gx+gw-4,gy-6,11,C.sub,'right'); }

  // ---- 小4：かん電池のつなぎ方 ----
  function cell(cx,y,pr){ const L=102, h=36, x0=cx-55+(pr?0:8);
    ctx.fillStyle='#9ca3af'; if(pr) ctx.fillRect(cx+47,y-7,8,14); else ctx.fillRect(cx-55,y-7,8,14);
    const g=ctx.createLinearGradient(0,y-h/2,0,y+h/2); g.addColorStop(0,'#4b5563'); g.addColorStop(0.45,'#111827'); g.addColorStop(1,'#374151'); ctx.fillStyle=g; rr(x0,y-h/2,L,h,7); ctx.fill();
    ctx.fillStyle='#ca8a04'; if(pr) ctx.fillRect(x0+L-34,y-h/2,26,h); else ctx.fillRect(x0+8,y-h/2,26,h);
    tx('＋',pr?x0+L-21:x0+21,y+6,17,'#fff','center',true); tx('－',pr?x0+16:x0+L-16,y+6,17,'#fff','center',true); tx('1.5V',cx+(pr?-8:8),y+5,12,'#e5e7eb','center',true); }
  function bulb(x,y,b){ const gy=y-34;
    if(b>0.02){ const r=30+40*b; const g=ctx.createRadialGradient(x,gy,8,x,gy,r); g.addColorStop(0,'rgba(253,224,71,'+(0.25+0.6*b).toFixed(3)+')'); g.addColorStop(1,'rgba(253,224,71,0)'); ctx.fillStyle=g; ctx.beginPath(); ctx.arc(x,gy,r,0,7); ctx.fill();
      ctx.strokeStyle='rgba(234,179,8,'+(0.9*b).toFixed(3)+')'; ctx.lineWidth=2.5; for(let k=0;k<9;k++){ const t=Math.PI*(1+k/8), r1=31+20*b; ctx.beginPath(); ctx.moveTo(x+Math.cos(t)*31,gy+Math.sin(t)*31); ctx.lineTo(x+Math.cos(t)*r1,gy+Math.sin(t)*r1); ctx.stroke(); } }
    ctx.fillStyle='#94a3b8'; rr(x-16,y-12,32,22,4); ctx.fill(); ctx.strokeStyle='#64748b'; ctx.lineWidth=1.5; ctx.stroke();
    ctx.fillStyle=b>0.02?mix('#f8fafc','#fde047',Math.min(1,0.35+0.65*b)):'#f8fafc'; ctx.strokeStyle='#94a3b8'; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(x,gy,24,0,7); ctx.fill(); ctx.stroke();
    ctx.strokeStyle=mix('#78716c','#ea580c',b); ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(x-8,y-14); ctx.lineTo(x-8,gy); for(let k=0;k<4;k++) ctx.lineTo(x-6+k*4,gy+(k%2?4:-4)); ctx.lineTo(x+8,gy); ctx.lineTo(x+8,y-14); ctx.stroke();
    tx('豆電球',x+34,y-46,12,C.sub,'left',true); }
  function motor(x,y,a,dir){ ctx.fillStyle='#cbd5e1'; ctx.strokeStyle='#64748b'; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(x,y,24,0,7); ctx.fill(); ctx.stroke();
    ctx.save(); ctx.translate(x,y); ctx.rotate(a); ctx.fillStyle='rgba(37,99,235,0.78)'; for(let k=0;k<3;k++){ ctx.rotate(2*Math.PI/3); ctx.beginPath(); ctx.ellipse(0,-24,9,22,0,0,7); ctx.fill(); } ctx.restore();
    ctx.fillStyle='#334155'; ctx.beginPath(); ctx.arc(x,y,6,0,7); ctx.fill();
    const R=56, a0=-Math.PI*0.82, a1=-Math.PI*0.18; ctx.strokeStyle='#2563eb'; ctx.lineWidth=2.5; ctx.beginPath(); ctx.arc(x,y,R,a0,a1); ctx.stroke();
    const e=dir>0?a1:a0, tx0=x+Math.cos(e)*R, ty0=y+Math.sin(e)*R, d=dir>0?[-Math.sin(e),Math.cos(e)]:[Math.sin(e),-Math.cos(e)], px=-d[1], py=d[0];
    ctx.fillStyle='#2563eb'; ctx.beginPath(); ctx.moveTo(tx0+d[0]*9,ty0+d[1]*9); ctx.lineTo(tx0-d[0]*5+px*7,ty0-d[1]*5+py*7); ctx.lineTo(tx0-d[0]*5-px*7,ty0-d[1]*5-py*7); ctx.closePath(); ctx.fill();
    tx('モーター',x+62,y-40,12,C.sub,'left',true); }
  function galv(x,y,I){ ctx.fillStyle='#fff'; ctx.strokeStyle='#475569'; ctx.lineWidth=2; rr(x-54,y-34,108,68,8); ctx.fill(); ctx.stroke();
    const cx=x, cy=y+22, R=40; ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.arc(cx,cy,R,-Math.PI/2-Math.PI/3,-Math.PI/2+Math.PI/3); ctx.stroke();
    for(let k=-5;k<=5;k++){ const t=-Math.PI/2+k*Math.PI/15, l=(k%5===0)?9:5; ctx.beginPath(); ctx.moveTo(cx+Math.cos(t)*(R-l),cy+Math.sin(t)*(R-l)); ctx.lineTo(cx+Math.cos(t)*R,cy+Math.sin(t)*R); ctx.stroke(); }
    tx('0',cx,cy-R-3,10,C.sub,'center'); tx('0.5',cx-43,cy-23,10,C.sub,'center'); tx('0.5',cx+43,cy-23,10,C.sub,'center');
    const th=-Math.PI/2+clamp(I/0.5,-1.15,1.15)*Math.PI/3; ctx.strokeStyle='#dc2626'; ctx.lineWidth=2.5; ctx.beginPath(); ctx.moveTo(cx,cy); ctx.lineTo(cx+Math.cos(th)*(R-5),cy+Math.sin(th)*(R-5)); ctx.stroke();
    ctx.fillStyle='#334155'; ctx.beginPath(); ctx.arc(cx,cy,4,0,7); ctx.fill(); }
  function diagram4(s){ const x0=462,y0=14,w=168,h=158; ctx.fillStyle='#fff'; ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1.5; rr(x0,y0,w,h,10); ctx.fill(); ctx.stroke();
    tx('回路図',x0+10,y0+20,12,C.ink,'left',true); tx('（けん流計は省略）',x0+50,y0+20,10,C.sub,'left');
    const L=x0+30,R=x0+w-30,T=y0+52,B=y0+112,cx=(L+R)/2;
    ctx.strokeStyle=C.ink; ctx.lineWidth=2; ctx.lineCap='butt'; ctx.beginPath(); ctx.moveTo(cx-12,T); ctx.lineTo(L,T); ctx.lineTo(L,B); ctx.moveTo(cx+12,T); ctx.lineTo(R,T); ctx.lineTo(R,B); ctx.stroke();
    ctx.fillStyle='#fff'; ctx.beginPath(); ctx.arc(cx,T,12,0,7); ctx.fill(); ctx.stroke();
    if(s.load==='bulb'){ const d=12*Math.SQRT1_2; ctx.beginPath(); ctx.moveTo(cx-d,T-d); ctx.lineTo(cx+d,T+d); ctx.moveTo(cx+d,T-d); ctx.lineTo(cx-d,T+d); ctx.stroke(); } else tx('M',cx,T+5,13,C.ink,'center',true);
    const sym=(x,y)=>{ const pl=rev?-1:1; ctx.strokeStyle=C.ink; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(x+5*pl,y-11); ctx.lineTo(x+5*pl,y+11); ctx.stroke(); ctx.lineWidth=5; ctx.beginPath(); ctx.moveTo(x-5*pl,y-6); ctx.lineTo(x-5*pl,y+6); ctx.stroke(); ctx.lineWidth=2; };
    const seg=(a,b,y)=>{ ctx.strokeStyle=C.ink; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(a,y); ctx.lineTo(b,y); ctx.stroke(); };
    if(s.bat==='one'){ seg(L,cx-5,B); seg(cx+5,R,B); sym(cx,B); }
    else if(s.bat==='ser'){ seg(L,cx-21,B); seg(cx-11,cx+11,B); seg(cx+21,R,B); sym(cx-16,B); sym(cx+16,B); }
    else { const y2=B+26; seg(L,cx-26,B); seg(cx+26,R,B); seg(cx-26,cx-5,B); seg(cx+5,cx+26,B); seg(cx-26,cx-5,y2); seg(cx+5,cx+26,y2);
      ctx.beginPath(); ctx.moveTo(cx-26,B); ctx.lineTo(cx-26,y2); ctx.moveTo(cx+26,B); ctx.lineTo(cx+26,y2); ctx.stroke(); sym(cx,B); sym(cx,y2); }
    ctx.lineCap='round'; }
  function bars(s){ const x0=462,y0=186,w=168,h=244; ctx.fillStyle='#fff'; ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1.5; rr(x0,y0,w,h,10); ctx.fill(); ctx.stroke();
    tx('電流の大きさくらべ',x0+10,y0+20,12,C.ink,'left',true);
    const base=y0+h-38, I0=E1/RL, sc=150/(2*I0), it=[['one','1個',I0],['ser','直列',2*I0],['par','へい列',I0]];
    it.forEach((t,i)=>{ const cx=x0+32+i*52, bh=t[2]*sc, on=t[0]===s.bat; ctx.fillStyle=on?C.cur:'#cbd5e1'; rr(cx-16,base-bh,32,bh,4); ctx.fill(); tx(fmt(t[2])+' A',cx,base-bh-6,11.5,on?C.ink:C.sub,'center',on); tx(t[1],cx,base+17,12.5,on?C.ink:C.sub,'center',true); });
    tx('（豆電球・モーターをつないだとき）',x0+w/2,y0+h-6,10,C.sub,'center'); }
  function draw4(s,dt){ const Y=340,Lx=70,Rx=430,T=150, pr=!rev, bulbOn=s.load==='bulb';
    const nm={one:'かん電池1個',ser:'かん電池2個の直列つなぎ',par:'かん電池2個のへい列つなぎ'}[s.bat];
    const msg=s.bat==='one'?'これを「1個のとき」として、つなぎ方をくらべよう':s.bat==='ser'?(bulbOn?'電流が大きくなり、豆電球が明るくなる':'電流が大きくなり、モーターが速く回る'):'電流の大きさは1個のときと同じ。かん電池は長持ち';
    tx(nm,14,30,17,C.ink,'left',true); tx(msg,14,52,13,C.sub,'left');
    if(s.bat==='par'){ wire([[335,Y],[Rx,Y],[Rx,T],[Lx,T],[Lx,Y],[165,Y]]); wire([[165,Y],[335,Y]]); wire([[165,Y],[165,400],[335,400],[335,Y]]); }
    else { const x1=s.bat==='ser'?140:195, x2=s.bat==='ser'?360:305; wire([[x2,Y],[Rx,Y],[Rx,T],[Lx,T],[Lx,Y],[x1,Y]]); }
    drawDots(paths(s),250,dt,C.cur);
    if(s.bat==='par'){ jdot(165,Y); jdot(335,Y); cell(250,Y,pr); cell(250,400,pr); }
    else if(s.bat==='ser'){ cell(195,Y,pr); cell(305,Y,pr); } else cell(250,Y,pr);
    const b=Math.min(1,Math.sqrt(s.P/(4*E1*E1/RL)));
    ang+=2*Math.PI*4*s.I*(rev?-1:1)*dt;
    if(bulbOn) bulb(250,T,b); else motor(250,T,ang,rev?-1:1);
    galv(Lx,245,s.I*(rev?-1:1)); tx('けん流計',132,236,13,C.ink,'left',true); tx(amp(s.I)+'・はりは'+(rev?'左':'右')+'にふれる',132,256,13,C.sub,'left');
    arrowHead(Rx,250,pr?'up':'down',C.cur); arrowHead(350,T,pr?'left':'right',C.cur); arrowHead(110,Y,pr?'right':'left',C.cur);
    tx('電流の向き',Rx-12,255,12,C.cur,'right',true);
    diagram4(s); bars(s);
    tx('● 電流の向き（＋極から出て－極へ）',14,432,12,C.cur,'left',true); }

  // ---- 統計・共有文 ----
  function update(){ const s=calc(), m4=s.mode==='sho4';
    ['bat','load'].forEach(id=>{ fld(id).style.display=m4?'':'none'; }); ['conn','volt','r1','r2','gsel'].forEach(id=>{ fld(id).style.display=m4?'none':''; });
    $('rev').style.display=m4?'':'none'; ['rec','clr','ele'].forEach(id=>{ $(id).style.display=m4?'none':''; });
    $('ele').textContent=ele?'電流の向きで見る':'電子の動きで見る';
    if(m4){ const bulbOn=s.load==='bulb', one=s.bat==='one', ser=s.bat==='ser';
      K('sI').innerHTML='回路を流れる電流'; sh('sI',amp(s.I),one?'1個のとき':ser?'1個のときの2倍':'1個のときと同じ');
      K('sR').innerHTML=bulbOn?'豆電球の明るさ':'モーターの回る速さ'; sh('sR',one?'ふつう':ser?(bulbOn?'明るい':'速い'):'1個と同じ',one?'これをもとにくらべる':ser?(bulbOn?'1個のときより明るい':'1個のときの約2倍'):(bulbOn?'長い時間つく':'長い時間回る'));
      K('s1').innerHTML='かん電池1個の電流'; sh('s1',amp(s.Ic),s.bat==='par'?'2個で半分ずつ':'');
      K('s2').innerHTML='かん電池の長持ち'; sh('s2',one?'ふつう':ser?'早くへる':'長持ち',one?'':ser?'1個のときより早くなくなる':'1個のときより長く使える');
      const nm={one:'かん電池1個',ser:'かん電池2個の直列つなぎ',par:'かん電池2個のへい列つなぎ'}[s.bat];
      setShare('【かん電池のつなぎ方】'+nm+'では、回路の電流は'+(one?amp(s.I):ser?'1個のときの2倍':'1個のときと同じ')+'。'+(bulbOn?'豆電球':'モーター')+'は'+(one?'これをもとにくらべる':ser?(bulbOn?'明るくなる':'速く回る'):'1個のときと同じで、かん電池は長持ち')+'｜シミュラボ');
    } else {
      K('sI').innerHTML='全体の電流'; sh('sI',amp(s.I),s.I>0&&s.I<1?fmt(s.I*1000)+NB+'mA':'');
      K('sR').innerHTML='全体の抵抗'; sh('sR',fmt(s.R)+NB+'Ω',s.ser?'R<sub>1</sub>＋R<sub>2</sub>':'R<sub>1</sub>・R<sub>2</sub>より小さい');
      K('s1').innerHTML='R<sub>1</sub> の電圧・電流'; sh('s1',fmt(s.V1)+NB+'V・'+amp(s.I1),'');
      K('s2').innerHTML='R<sub>2</sub> の電圧・電流'; sh('s2',fmt(s.V2)+NB+'V・'+amp(s.I2),'');
      setShare('【'+(s.ser?'直列回路':'並列回路')+'・オームの法則】電源'+fmt(s.V)+' V、R1＝'+fmt(s.R1)+' Ω、R2＝'+fmt(s.R2)+' Ω → 全体の抵抗'+fmt(s.R)+' Ω、電流'+fmt(s.I)+' A（R1は'+fmt(s.V1)+' V・'+fmt(s.I1)+' A、R2は'+fmt(s.V2)+' V・'+fmt(s.I2)+' A）｜シミュラボ'); } }

  QK.forEach(id=>{ $(id).addEventListener('input',()=>{ if(id==='r1'||id==='r2'||id==='conn') recs=[]; update(); }); $(id).addEventListener('change',update); });
  $('rev').addEventListener('click',()=>{ rev=!rev; update(); });
  $('rec').addEventListener('click',()=>{ const s=calc(); recs.push({r1:[s.V1,s.I1],r2:[s.V2,s.I2],tot:[s.V,s.I]}); if(recs.length>40) recs.shift(); });
  $('clr').addEventListener('click',()=>{ recs=[]; });
  $('ele').addEventListener('click',()=>{ ele=!ele; update(); });
  cv.addEventListener('pointerdown',e=>{ const p=cpos(cv,e), x=p[0]/dpr, y=p[1]/dpr, s=calc();
    if(s.mode==='sho4'){ if(y>312&&y<422&&x>130&&x<372){ rev=!rev; update(); } else if(Math.abs(x-250)<58&&y>62&&y<210){ $('load').value=$('load').value==='bulb'?'motor':'bulb'; update(); } return; }
    const hits=s.ser?[['r1',195,95],['r2',305,95],['tot',55,235]]:[['r1',295,95],['r2',295,205],['tot',55,235]];
    for(const h of hits){ if(Math.abs(x-h[1])<38&&Math.abs(y-h[2])<24){ $('gsel').value=h[0]; update(); return; } }
    if(x>405){ $('gsel').value='all'; update(); } });
  function frame(t){ const dt=last?Math.min(0.05,(t-last)/1000):0; last=t; const s=calc();
    ctx.fillStyle=C.bg; ctx.fillRect(0,0,W,H);
    if(s.mode==='sho4') draw4(s,dt); else { draw2(s,dt); graph(s); }
    requestAnimationFrame(frame); }
  update(); frame(performance.now());
''')

# ============================================================ 2 凸レンズの像
sim(slug="totsu-lens", cat="rika", emoji="🔍", score=76,
    title="凸レンズの像（作図）シミュレーター",
    title_tag="凸レンズの像の作図シミュレーター｜実像・虚像と焦点の位置を3本の光で確かめる",
    meta_desc="凸レンズの像を3本の光で作図する無料シミュレーター。物体や焦点を動かすと、実像（上下左右が逆）・虚像・像ができない位置と、像の位置・大きさ（倍率）の変わり方を確かめられます。中1「光と音」の授業や定期テストの復習に。高校のレンズの式にも対応。",
    og_title="凸レンズの像（作図）シミュレーター",
    og_desc="物体を動かすと3本の光で像を作図。実像・虚像・像ができない位置が一目でわかる。中1「光と音」の授業向け。",
    card_desc="物体を動かすと3本の光で像を作図。実像・虚像・像ができない位置と、像の大きさの変化がひと目でわかる。",
    lead="物体を指でドラッグするか、位置のボタンを押すと、凸レンズを通る代表的な3本の光で像を作図します。実像（上下左右が逆）・虚像（同じ向きで大きい）・像ができない位置と、スクリーンを置く場所がわかります。焦点距離も変えられます。",
    model="中1 光と音（凸レンズの働き）／高校物理 レンズの式",
    level="中学1年、高校（物理）",
    unit="中学校 第1分野（1）身近な物理現象（ア）光と音（凸レンズの働き）／高等学校 物理（2）波（ウ）光",
    canvas=canvas(640, 400),
    controls=slider("a", "物体とレンズの距離", 1, 42, 25, 0.5, "{v} cm") + slider("f", "焦点距離", 5, 15, 10, 0.5, "{v} cm")
           + select("rays", "作図する光", [("all", "①②③ の3本"), ("12", "①と② の2本"), ("1", "① だけ"), ("2", "② だけ"), ("3", "③ だけ")])
           + select("obj", "物体", [("arrow", "矢印"), ("candle", "ろうそく")]),
    buttons='<span style="align-self:center;font-size:13px;font-weight:800;color:var(--ink-2)">物体の位置：</span>'
           + btn("p3", "2fより遠く") + btn("p2", "2f") + btn("p15", "fと2fの間") + btn("p1", "焦点の上") + btn("p05", "焦点の内側")
           + '<div style="flex-basis:100%;height:0"></div>' + btn("fan", "光の束を表示") + btn("cover", "レンズの上半分をかくす"),
    stats=stats([("sA", "物体の位置（焦点距離の何倍か）", False), ("sB", "像の位置（レンズから）", False), ("sM", "像の大きさ（倍率）", True), ("sT", "像の種類", False)]),
    legend="赤①＝光軸に平行に進む光（屈折して反対側の焦点を通る）、緑②＝レンズの中心を通る光（直進）、青③＝焦点を通ってレンズに入る光（屈折して光軸に平行に進む）。F＝焦点、2F＝焦点距離の2倍の位置、f＝焦点距離。物体と焦点Fは指でドラッグできます。点線は、光を逆向きにのばした線です。",
    article='''
<h2>このシミュレーションでわかること</h2>
<p>物体を凸レンズの焦点より外側に置くと、レンズの反対側に上下左右が逆向きの<b>実像</b>ができ、スクリーンに映ります。物体をレンズに近づけるほど実像はレンズから遠くなって大きくなり、焦点距離の2倍の位置では物体と同じ大きさになります。物体が焦点の上にあると像はできず、焦点より内側では、レンズをのぞくと物体と同じ向きの大きな<b>虚像</b>が見えます。</p>
''' + N("対応する単元：中学校第1学年 第1分野（1）身近な物理現象（ア）光と音「凸レンズの働き」。あわせて、高等学校「物理」（2）波（ウ）光で学ぶレンズの式（1/a＋1/b＝1/f）も表示しています。") + '''
<h2>授業での使い方</h2>
<h3>導入：身近な体験から問いをつくる</h3>
<p>虫眼鏡で窓の外の景色を紙に映すと逆さまに映り、近くの文字をのぞくと同じ向きで大きく見えます。「同じレンズなのに、なぜ見え方がちがうのか」を問いにして、物体の位置に注目させます。</p>
<h3>展開：5つの場合を比べて表にまとめる</h3>
<p>光学台での実験の前後に、「物体の位置」のボタン（2fより遠く／2f／fと2fの間／焦点の上／焦点の内側）で5つの場合を順に映し、像の位置・大きさ・向きを表にまとめさせます。「作図する光」で①だけ・②だけを表示すると、作図の手順を1本ずつ確かめられます。物体をドラッグして少しずつ動かせば、像の位置と大きさが連続して変わる様子も見られます。</p>
<h3>まとめ：作図と定期テストの確かめ</h3>
<p>ノートにかいた作図をシミュレーターの図と見比べて確かめます。「光の束を表示」では、物体の1点から出た光がレンズのどこを通っても像の1点に集まることがわかります。「レンズの上半分をかくす」は、定期テストでよく出る問題の確かめに使えます。</p>
<p><b>生徒への問いの例</b></p>
<ol>
<li>物体をレンズから遠ざけていくと、スクリーンにできる像の位置と大きさはどう変わるでしょう。</li>
<li>物体を焦点の上に置くと、スクリーンをどこに動かしても像が映らないのはなぜでしょう。3本の光を使って説明しましょう。</li>
<li>凸レンズの上半分を厚紙でかくすと、スクリーンの像はどうなるでしょう。</li>
</ol>
<h2>しくみ・解説</h2>
<h3>作図に使う3本の光</h3>
<ol>
<li>光軸に平行に進む光は、レンズで屈折したあと、反対側の焦点を通る（①赤）</li>
<li>レンズの中心を通る光は、そのまま直進する（②緑）</li>
<li>焦点を通ってからレンズに入る光は、屈折したあと光軸に平行に進む（③青）</li>
</ol>
<p>物体の先端から出たこれらの光が、レンズを通ったあとで交わる点が像の先端です。3本のうち2本をかけば像の位置は決まります。レンズを通った光が広がって交わらないとき（物体が焦点より内側のとき）は、光を逆向きにのばした線（点線）が交わる点に像があるように見えます。これが虚像です。</p>
<h3>物体の位置と像の早見表</h3>
''' + T([["焦点距離の2倍より遠い", "反対側の焦点と、焦点距離の2倍の位置の間", "物体より小さい", "実像（上下左右が逆）"],
          ["焦点距離の2倍の位置", "反対側の焦点距離の2倍の位置", "物体と同じ", "実像（上下左右が逆）"],
          ["焦点と、焦点距離の2倍の位置の間", "反対側の焦点距離の2倍の位置より遠く", "物体より大きい", "実像（上下左右が逆）"],
          ["焦点の上", "できない", "—", "—"],
          ["焦点より内側", "物体と同じ側（レンズをのぞくと見える）", "物体より大きい", "虚像（物体と同じ向き）"]],
         ["物体の位置", "像のできる位置", "像の大きさ", "像の種類と向き"]) + '''
<h3>焦点距離10 cmのレンズの例</h3>
''' + T([["30 cm（焦点距離の3倍）", "反対側15 cm", "0.5倍", "実像"],
          ["20 cm（2倍）", "反対側20 cm", "1倍", "実像"],
          ["15 cm（1.5倍）", "反対側30 cm", "2倍", "実像"],
          ["12 cm（1.2倍）", "反対側60 cm", "5倍", "実像"],
          ["10 cm（焦点）", "できない", "—", "—"],
          ["5 cm（0.5倍）", "物体と同じ側10 cm", "2倍", "虚像"]],
         ["物体の位置", "像の位置", "像の大きさ", "像の種類"]) + '''
<h3>高校：レンズの式</h3>
<p>レンズから物体までの距離を a、レンズから像までの距離を b、焦点距離を f とすると、次の式が成り立ちます。虚像のときは b をマイナスとして計算します。像の倍率は m＝|b÷a| です。</p>
''' + N("1/a＋1/b＝1/f<br>例1：f＝10 cm、a＝30 cm → 1/b＝1/10－1/30＝1/15 → b＝15 cm（実像、倍率0.5倍）<br>例2：f＝10 cm、a＝5 cm → 1/b＝1/10－1/5＝－1/10 → b＝－10 cm（虚像、倍率2倍）") + '''
<h3>このシミュレーションで単純化していること</h3>
<ul>
<li>厚さを考えない「薄いレンズ」として、作図と同じようにレンズの中心の線で1回だけ光を曲げています（実際の光は、レンズに入るときと出るときの2回屈折します）。</li>
<li>光軸に近い光として計算しているので、レンズのふちを通る光のずれ（収差）や、色による焦点のずれは表していません。作図のきまりどおり、レンズの外を通るように見える光も中心の線で曲げています。</li>
<li>見やすさのため、物体やレンズを実際の実験より大きく描いています（画面の7 pxを1 cmとしています）。</li>
<li>横から見た図では上下の逆転しかわからないため、右上の「正面から見ると」で上下左右が逆になることを示しています（矢印の旗、ろうそくのろうのたれは、左右を見分けるための目印です）。</li>
</ul>
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「中学校学習指導要領（平成29年告示）解説 理科編」第1分野（1）身近な物理現象　''' + A(MEXT_CHU) + '''</li>
<li>文部科学省「高等学校学習指導要領（平成30年告示）解説 理科編 理数編」物理（2）波　''' + A(MEXT_KOU) + '''</li>
<li>中学校理科の教科書（東京書籍「新しい科学」1年、啓林館「未来へひろがるサイエンス」1年 など）の「光と音」の単元</li>
</ul>
''',
    faqs=[("実像と虚像のちがいは？", "実像は、レンズを通った光が実際に集まってできる像で、スクリーンに映ります。凸レンズでできる実像は上下左右が逆向きです。虚像は、光が集まらず、レンズをのぞいたときに光がそこから出ているように見える像で、スクリーンには映りません。凸レンズの虚像は物体と同じ向きで、物体より大きく見えます。"),
          ("物体を焦点に置くと像ができないのはなぜ？", "焦点から出た光は、凸レンズで屈折したあと光軸に平行に進みます。物体の先端から出た光がどれもたがいに平行になって交わらないため、実像も虚像もできません。物体を外側から焦点に近づけていくと、像はレンズからどんどん遠く、大きくなっていきます。"),
          ("凸レンズの上半分をかくすと、像はどうなる？", "像は欠けずに全体が映り、暗くなります。物体の1点から出た光は、レンズのいろいろな場所を通って像の1点に集まるので、下半分を通った光だけでも像全体ができます。レンズを通る光の量が減るので暗くなります。"),
          ("虫眼鏡で物が大きく見えるのはなぜ？", "虫眼鏡は凸レンズです。物体を焦点より内側に置いてのぞくと、物体と同じ向きの大きな虚像が見えます。"),
          ("焦点距離を短くすると、像はどう変わる？", "物体を同じ位置に置いたままでも、焦点距離が短い（ふくらみの大きい）レンズほど光を大きく曲げるので、実像はレンズに近い位置にでき、小さくなります。焦点距離のスライダーや焦点Fのドラッグで確かめられます。"),
          ("カメラや目でも同じことが起きているの？", "はい。カメラはレンズでつくった実像を撮像素子に映し、目は水晶体（凸レンズのはたらき）でつくった実像を網膜に映しています。どちらも像は上下左右が逆向きです。")],
    rel=[("ripple", "🌊", "波紋シミュレーター"), ("double-slit", "⚛️", "ダブルスリット実験"), ("wave", "🌊", "波の干渉シミュレーター"), ("mosquito-on", "🦟", "モスキート音テスト")],
    js=r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const FF='"Hiragino Sans","Hiragino Kaku Gothic ProN","Noto Sans JP","Yu Gothic UI","Yu Gothic",Meiryo,sans-serif';
  const S=7, X0=310, Y0=200, HL=100, HO=6;   // 7px＝1cm、レンズの位置、光軸、レンズの半分の高さ(px)、物体の高さ(cm)
  const C={bg:'#0b1020',axis:'#64748b',ink:'#e2e8f0',sub:'#94a3b8',r1:'#f87171',r2:'#4ade80',r3:'#60a5fa',lens:'rgba(147,197,253,0.22)',lensS:'#93c5fd',obj:'#fbbf24',img:'#fde68a',foc:'#facc15'};
  const Q=new URLSearchParams(location.search);
  ['a','f','rays','obj'].forEach(k=>{ const el=$(k); if(!el||!Q.has(k)) return; const v=Q.get(k); if(el.tagName==='SELECT'&&![].some.call(el.options,o=>o.value===v)) return; el.value=v; el.dispatchEvent(new Event('input')); });
  let fan=Q.get('fan')==='1', cover=Q.get('cover')==='1', drag=null, last=0, tt=0;
  const fmt=v=>{ if(!isFinite(v)) return '—'; const a=Math.abs(v); let s=a>=100?v.toFixed(0):a>=10?v.toFixed(1):v.toFixed(2); if(s.indexOf('.')>=0) s=s.replace(/0+$/,'').replace(/\.$/,''); return s; };
  function sh(id,m,sub){ const e=$(id); if(e) e.innerHTML=m+(sub?'<span style="display:block;font-size:12px;font-weight:700;color:#59616c;margin-top:2px">'+sub+'</span>':''); }
  function st(){ const f=+$('f').value, a=+$('a').value; if(Math.abs(a-f)<1e-9) return {f:f,a:a,kind:'none',b:Infinity,m:Infinity}; const b=a*f/(a-f), m=Math.abs(b/a); return {f:f,a:a,b:b,m:m,kind:b>0?'real':'virt'}; }
  function tx(s,x,y,size,col,align,bold){ ctx.font=(bold?'bold ':'')+size+'px '+FF; ctx.textAlign=align||'left'; ctx.fillStyle=col; ctx.fillText(s,x,y); ctx.textAlign='left'; }
  function tag(s,x,y,size,col,align){ ctx.font='bold '+size+'px '+FF; const w=ctx.measureText(s).width; const x0=align==='right'?x-w:align==='center'?x-w/2:x; ctx.fillStyle='rgba(11,16,32,0.78)'; ctx.fillRect(x0-5,y-size-1,w+10,size+8); tx(s,x0,y,size,col,'left',true); }
  function rr(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
  function arrowMid(x1,y1,x2,y2,col){ const dx=x2-x1, dy=y2-y1, l=Math.hypot(dx,dy); if(l<30) return; const ux=dx/l, uy=dy/l, mx=x1+dx*0.5, my=y1+dy*0.5; ctx.fillStyle=col; ctx.beginPath(); ctx.moveTo(mx+ux*7,my+uy*7); ctx.lineTo(mx-ux*5-uy*5,my-uy*5+ux*5); ctx.lineTo(mx-ux*5+uy*5,my-uy*5-ux*5); ctx.closePath(); ctx.fill(); }
  // 物体・像（横から見た図）。hp＞0 で上向き、hp＜0 で下向き（倒立）
  function glyph(kind,x,yb,hp,alpha,dashed,col){ if(Math.abs(hp)<0.5) return; ctx.save(); ctx.globalAlpha=alpha; const sg=hp>0?1:-1, yt=yb-hp;
    if(kind==='arrow'){ ctx.strokeStyle=col; ctx.fillStyle=col; ctx.lineWidth=4; if(dashed) ctx.setLineDash([5,4]); const hd=Math.min(12,Math.abs(hp)*0.45); ctx.beginPath(); ctx.moveTo(x,yb); ctx.lineTo(x,yt+sg*hd*0.7); ctx.stroke(); ctx.setLineDash([]); ctx.beginPath(); ctx.moveTo(x,yt); ctx.lineTo(x-hd*0.7,yt+sg*hd); ctx.lineTo(x+hd*0.7,yt+sg*hd); ctx.closePath(); ctx.fill(); }
    else { const ah=Math.abs(hp), w=Math.max(4,Math.min(40,ah*0.3)), yTop=yb-hp*0.66; ctx.fillStyle='#fef3c7'; ctx.fillRect(x-w/2,Math.min(yb,yTop),w,Math.abs(yb-yTop));
      if(dashed){ ctx.strokeStyle='#fde68a'; ctx.setLineDash([4,3]); ctx.lineWidth=1.5; ctx.strokeRect(x-w/2,Math.min(yb,yTop),w,Math.abs(yb-yTop)); ctx.setLineDash([]); }
      ctx.strokeStyle='#78350f'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.moveTo(x,yTop); ctx.lineTo(x,yb-hp*0.71); ctx.stroke();
      const yf=yb-hp*0.70, gl=ctx.createRadialGradient(x,yb-hp*0.84,1,x,yb-hp*0.84,ah*0.45); gl.addColorStop(0,'rgba(253,224,71,0.45)'); gl.addColorStop(1,'rgba(253,224,71,0)'); ctx.fillStyle=gl; ctx.beginPath(); ctx.arc(x,yb-hp*0.84,ah*0.45,0,7); ctx.fill();
      const g=ctx.createLinearGradient(0,yf,0,yt); g.addColorStop(0,'#f97316'); g.addColorStop(1,'#fde047'); ctx.fillStyle=g; ctx.beginPath(); ctx.moveTo(x,yf); ctx.quadraticCurveTo(x-w*0.9,yb-hp*0.80,x,yt); ctx.quadraticCurveTo(x+w*0.9,yb-hp*0.80,x,yf); ctx.fill(); }
    ctx.restore(); }
  // 正面から見た形（左右がわかる目印つき）
  function front(kind,cx,cy,hp,rot,alpha,col){ ctx.save(); ctx.globalAlpha=alpha; ctx.translate(cx,cy); if(rot) ctx.rotate(Math.PI);
    if(kind==='arrow'){ ctx.strokeStyle=col; ctx.fillStyle=col; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(0,hp/2); ctx.lineTo(0,-hp/2+6); ctx.stroke(); ctx.beginPath(); ctx.moveTo(0,-hp/2); ctx.lineTo(-hp*0.17,-hp/2+hp*0.26); ctx.lineTo(hp*0.17,-hp/2+hp*0.26); ctx.closePath(); ctx.fill();
      ctx.fillStyle='#f87171'; ctx.beginPath(); ctx.moveTo(1.5,-hp*0.16); ctx.lineTo(hp*0.42,-hp*0.02); ctx.lineTo(1.5,hp*0.12); ctx.closePath(); ctx.fill(); }
    else { const w=hp*0.26; ctx.fillStyle='#fef3c7'; ctx.fillRect(-w/2,-hp*0.14,w,hp*0.64); ctx.fillRect(w/2-1,-hp*0.14,hp*0.07,hp*0.24); ctx.beginPath(); ctx.arc(w/2-1+hp*0.035,hp*0.1,hp*0.035,0,7); ctx.fill();
      const g=ctx.createLinearGradient(0,-hp*0.14,0,-hp/2); g.addColorStop(0,'#f97316'); g.addColorStop(1,'#fde047'); ctx.fillStyle=g; ctx.beginPath(); ctx.moveTo(0,-hp*0.16); ctx.quadraticCurveTo(-w*0.8,-hp*0.3,0,-hp/2); ctx.quadraticCurveTo(w*0.8,-hp*0.3,0,-hp*0.16); ctx.fill(); }
    ctx.restore(); }
  function inset(s,kind){ const x0=494,y0=8,w=138,h=104; ctx.fillStyle='rgba(15,23,42,0.92)'; ctx.strokeStyle='#334155'; ctx.lineWidth=1; rr(x0,y0,w,h,8); ctx.fill(); ctx.stroke();
    tx('正面から見ると',x0+8,y0+17,11,C.sub,'left',true);
    const lx=x0+34, rx=x0+102, cy=y0+58; front(kind,lx,cy,34,false,1,C.obj); tx('物体',lx,y0+h-6,11,C.ink,'center'); tx('→',(lx+rx)/2,cy+5,14,C.sub,'center',true);
    if(s.kind==='none'){ tx('できない',rx,cy+4,12,C.sub,'center',true); tx('像',rx,y0+h-6,11,C.ink,'center'); }
    else { front(kind,rx,cy,34*clamp(s.m,0.3,1.35),s.kind==='real',s.kind==='real'?1:0.7,C.img); tx(s.kind==='real'?'スクリーン':'のぞくと',rx,y0+h-6,11,C.ink,'center'); } }
  function dim(x1,x2,y,label){ if(Math.abs(x2-x1)<2) return; ctx.strokeStyle=C.sub; ctx.lineWidth=1.2; ctx.beginPath(); ctx.moveTo(x1,y); ctx.lineTo(x2,y); ctx.moveTo(x1,y-5); ctx.lineTo(x1,y+5); ctx.moveTo(x2,y-5); ctx.lineTo(x2,y+5); ctx.stroke(); tx(label,(x1+x2)/2,y-5,11.5,C.sub,'center'); }

  function draw(){ const s=st(), f=s.f, a=s.a, kind=$('obj').value, sel=$('rays').value;
    ctx.fillStyle=C.bg; ctx.fillRect(0,0,W,H);
    // 光軸・目もり・焦点
    ctx.strokeStyle=C.axis; ctx.lineWidth=1.2; ctx.beginPath(); ctx.moveTo(0,Y0); ctx.lineTo(W,Y0); ctx.stroke(); tx('光軸',W-6,Y0-6,11,C.sub,'right');
    ctx.strokeStyle='rgba(148,163,184,0.5)'; for(let c=-45;c<=50;c+=5){ const x=X0+c*S, big=c%10===0; ctx.beginPath(); ctx.moveTo(x,Y0-(big?4:2)); ctx.lineTo(x,Y0+(big?4:2)); ctx.stroke(); }
    [-1,1].forEach(sd=>{ const xf=X0+sd*f*S, x2=X0+sd*2*f*S; ctx.fillStyle=C.foc; ctx.beginPath(); ctx.arc(xf,Y0,5,0,7); ctx.fill(); tx('F',xf,Y0+21,13,C.foc,'center',true);
      if(x2>-5&&x2<W+5){ ctx.strokeStyle=C.sub; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(x2,Y0-7); ctx.lineTo(x2,Y0+7); ctx.stroke(); tx('2F',x2,Y0+21,12,C.sub,'center',true); } });
    // レンズ
    const t=6+100/f; ctx.fillStyle=C.lens; ctx.strokeStyle=C.lensS; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(X0,Y0-HL); ctx.quadraticCurveTo(X0+t,Y0,X0,Y0+HL); ctx.quadraticCurveTo(X0-t,Y0,X0,Y0-HL); ctx.fill(); ctx.stroke();
    ctx.setLineDash([3,5]); ctx.strokeStyle='rgba(147,197,253,0.35)'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(X0,10); ctx.lineTo(X0,H-62); ctx.stroke(); ctx.setLineDash([]);
    tx('凸レンズ',X0-16,Y0-HL-4,12,C.lensS,'right',true);
    const xo=X0-a*S, yo=Y0-HO*S, xi=isFinite(s.b)?X0+s.b*S:NaN, yi=isFinite(s.b)?Y0+(s.b/a)*HO*S:NaN;
    const scrOn=s.kind==='real'&&xi<=W-10, xe=scrOn?xi:W;
    const outK=yL=>(yL-yo)/(X0-xo)-(yL-Y0)/(f*S);
    const blocked=yL=>cover&&yL<=Y0+0.5;
    // 光の束
    if(fan||cover){ ctx.strokeStyle='rgba(255,255,255,0.22)'; ctx.lineWidth=1; for(let k=0;k<=12;k++){ const yL=Y0-HL+k*(2*HL/12); ctx.beginPath(); ctx.moveTo(xo,yo); ctx.lineTo(X0,yL); if(!blocked(yL)){ ctx.lineTo(xe,yL+outK(yL)*(xe-X0)); } ctx.stroke(); } }
    // 代表的な3本の光
    const want=sel==='all'?[1,2,3]:sel==='12'?[1,2]:[+sel]; const rays=[];
    if(want.indexOf(1)>=0) rays.push({n:1,col:C.r1,yL:yo});
    if(want.indexOf(2)>=0) rays.push({n:2,col:C.r2,yL:Y0});
    if(want.indexOf(3)>=0&&s.kind!=='none') rays.push({n:3,col:C.r3,yL:yo+a*HO*S/(a-f)});
    const pass=[];
    rays.forEach(r=>{ ctx.strokeStyle=r.col; ctx.lineWidth=2.2;
      if(r.n===3&&s.kind==='virt'){ ctx.save(); ctx.globalAlpha=0.55; ctx.setLineDash([3,4]); ctx.beginPath(); ctx.moveTo(X0-f*S,Y0); ctx.lineTo(xo,yo); ctx.stroke(); ctx.restore(); }
      ctx.beginPath(); ctx.moveTo(xo,yo); ctx.lineTo(X0,r.yL); ctx.stroke(); arrowMid(xo,yo,X0,r.yL,r.col);
      const nm=['','①','②','③'][r.n];
      if(blocked(r.yL)){ tx(nm,X0-24,r.yL-8,14,r.col,'center',true); ctx.strokeStyle=r.col; ctx.lineWidth=2.5; ctx.beginPath(); ctx.moveTo(X0-14,r.yL-6); ctx.lineTo(X0-2,r.yL+6); ctx.moveTo(X0-2,r.yL-6); ctx.lineTo(X0-14,r.yL+6); ctx.stroke(); return; }
      const ye=r.yL+outK(r.yL)*(xe-X0); ctx.strokeStyle=r.col; ctx.lineWidth=2.2; ctx.beginPath(); ctx.moveTo(X0,r.yL); ctx.lineTo(xe,ye); ctx.stroke(); arrowMid(X0,r.yL,xe,ye,r.col);
      const ly=r.yL+outK(r.yL)*22; tx(nm,X0+24,ly+(r.n===3&&s.kind==='real'&&ly+18<H-34?18:-9),14,r.col,'center',true);
      if(s.kind==='virt'){ ctx.save(); ctx.globalAlpha=0.7; ctx.setLineDash([5,5]); ctx.beginPath(); ctx.moveTo(X0,r.yL); ctx.lineTo(xi,yi); ctx.stroke(); ctx.restore(); }
      pass.push([[xo,yo],[X0,r.yL],[xe,ye],r.col]); });
    // 光の粒（進む向き）
    pass.forEach(p=>{ const L1=Math.hypot(p[1][0]-p[0][0],p[1][1]-p[0][1]), L2=Math.hypot(p[2][0]-p[1][0],p[2][1]-p[1][1]); ctx.fillStyle=p[3];
      for(let d=(tt*90)%46; d<L1+L2; d+=46){ let x,y; if(d<L1){ x=p[0][0]+(p[1][0]-p[0][0])*d/L1; y=p[0][1]+(p[1][1]-p[0][1])*d/L1; } else { const e=(d-L1)/L2; x=p[1][0]+(p[2][0]-p[1][0])*e; y=p[1][1]+(p[2][1]-p[1][1])*e; } ctx.beginPath(); ctx.arc(x,y,2.6,0,7); ctx.fill(); } });
    if(cover){ ctx.fillStyle='#a16207'; ctx.fillRect(X0-13,Y0-HL-6,26,HL+6); ctx.strokeStyle='#fbbf24'; ctx.lineWidth=1; ctx.strokeRect(X0-13,Y0-HL-6,26,HL+6); tag('厚紙でかくす',X0+18,Y0-HL+10,12,'#fbbf24','left'); }
    // 物体
    glyph(kind,xo,Y0,HO*S,1,false,C.obj); tx('物体',xo,Y0+38,12,C.obj,'center',true);
    // 像・スクリーン
    const showImg=want.length>=2||fan||cover, ia=cover?0.5:1;
    if(s.kind==='real'){
      if(scrOn&&showImg){ const top=Y0-70, bot=Math.min(H-4,Math.max(Y0+80,yi+16)); ctx.fillStyle='rgba(226,232,240,0.85)'; ctx.fillRect(xi+3,top,7,bot-top); if(xi+82<W) tag('スクリーン',xi+16,Y0-40,12,C.ink,'left'); else tag('スクリーン',xi-4,Y0-40,12,C.ink,'right');
        { glyph(kind,xi,Y0,-s.m*HO*S,ia,false,C.img); tag('実像',xi-8,Math.min(H-78,yi+20),12,C.img,'right'); } }
      else if(!scrOn&&showImg) tag('像は右の画面外（レンズから'+fmt(s.b)+' cm）→',W-6,Y0+44,12,C.img,'right');
    } else if(s.kind==='virt'){
      if(showImg&&xi>-30) { glyph(kind,xi,Y0,s.m*HO*S,0.6*ia,true,C.img); tag('虚像',xi+8,Math.max(26,yi+14),12,C.img,'left'); }
      if(xi<=-30) tag('← 像は左の画面外（レンズから'+fmt(-s.b)+' cm）',6,Y0-44,12,C.img,'left');
      const ex=W-34, ey=Y0-24; ctx.strokeStyle=C.ink; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(ex-14,ey); ctx.quadraticCurveTo(ex,ey-10,ex+14,ey); ctx.quadraticCurveTo(ex,ey+10,ex-14,ey); ctx.stroke(); ctx.fillStyle=C.ink; ctx.beginPath(); ctx.arc(ex-3,ey,3.5,0,7); ctx.fill();
      tag('レンズをのぞくと見える',W-6,ey-18,12,C.ink,'right'); tag('スクリーンには映らない',W-6,Y0+64,12,C.sub,'right');
    } else tag('光が平行に進むので、像はできない',W-6,Y0+64,12,C.ink,'right');
    if(!showImg&&s.kind!=='none') tag('もう1本光をかくと、交わる点に像ができる',W-6,Y0+88,12,C.sub,'right');
    if(cover) tag('像は欠けずに暗くなる',X0+18,Y0-HL+30,12,'#fbbf24','left');
    // 距離・式・説明
    dim(xo,X0,H-64,'物体まで '+fmt(a)+' cm');
    if(showImg&&s.kind==='real'&&xi<=W) dim(X0,xi,H-64,'像まで '+fmt(s.b)+' cm'); else if(showImg&&s.kind==='virt'&&xi>=0) dim(xi,X0,H-44,'像まで '+fmt(-s.b)+' cm（物体と同じ側）');
    tx('レンズの式（高校）  1/a + 1/b = 1/f',12,20,12,C.sub,'left');
    tx(s.kind==='none'?'1/'+fmt(a)+' + 1/b = 1/'+fmt(f)+'  → 1/b = 0（像はできない）':'1/'+fmt(a)+' + 1/'+(s.b<0?'(−'+fmt(-s.b)+')':fmt(s.b))+' = 1/'+fmt(f)+(s.kind==='virt'?'（虚像は b がマイナス）':''),12,38,12,C.ink,'left');
    const r=a/f, cap=s.kind==='none'?'物体が焦点の上 → 光が平行に進み、像はできない':s.kind==='virt'?'物体が焦点の内側 → スクリーンには映らない。のぞくと大きな虚像（同じ向き）':Math.abs(r-2)<1e-9?'物体が焦点距離の2倍の位置 → 反対側の2倍の位置に、同じ大きさの実像':r>2?'物体が焦点距離の2倍より遠い → 焦点と2倍の位置の間に、小さい実像':'物体が焦点と2倍の位置の間 → 2倍の位置より遠くに、大きい実像';
    tag(cap,10,H-8,13,C.ink,'left');
    inset(s,kind); }

  function update(){ const s=st();
    sh('sA',fmt(s.a/s.f)+'倍',fmt(s.a)+' cm（焦点距離 '+fmt(s.f)+' cm）');
    if(s.kind==='none'){ sh('sB','できない','光が平行に進む'); sh('sM','なし','像ができない'); sh('sT','像なし','物体が焦点の上');
      setShare('【凸レンズの像】焦点距離'+fmt(s.f)+' cmの凸レンズの焦点の上に物体を置くと、光が平行に進み像はできない｜シミュラボ'); }
    else if(s.kind==='real'){ const mm=Math.round(s.m*100)/100; sh('sB',fmt(s.b)+' cm','反対側・焦点距離の'+fmt(s.b/s.f)+'倍'); sh('sM',mm+'倍',Math.abs(s.m-1)<0.005?'物体と同じ大きさ':s.m<1?'物体より小さい':'物体より大きい'); sh('sT','実像','上下左右が逆向き');
      setShare('【凸レンズの像】焦点距離'+fmt(s.f)+' cmのレンズから'+fmt(s.a)+' cm（焦点距離の'+fmt(s.a/s.f)+'倍）に物体を置くと、反対側'+fmt(s.b)+' cmに'+mm+'倍の実像（上下左右が逆）ができる｜シミュラボ'); }
    else { const mm=Math.round(s.m*100)/100; sh('sB',fmt(-s.b)+' cm','物体と同じ側（のぞくと見える）'); sh('sM',mm+'倍','物体より大きい'); sh('sT','虚像','物体と同じ向き');
      setShare('【凸レンズの像】焦点距離'+fmt(s.f)+' cmのレンズから'+fmt(s.a)+' cm（焦点の内側）に物体を置くと、'+mm+'倍の虚像（同じ向き）が見える｜シミュラボ'); } }

  function setv(id,v){ const el=$(id); if(+el.value===v) return; el.value=v; el.dispatchEvent(new Event('input')); }
  const moveA=x=>setv('a',clamp(Math.round((X0-x)/S*2)/2,1,42));
  ['a','f'].forEach(id=>{ $(id).addEventListener('input',update); $(id).addEventListener('change',update); });
  const PRE=[['p3',3],['p2',2],['p15',1.5],['p1',1],['p05',0.5]];
  PRE.forEach(p=>{ $(p[0]).addEventListener('click',()=>{ setv('a',clamp(Math.round(+$('f').value*p[1]*2)/2,1,42)); }); });
  $('fan').addEventListener('click',()=>{ fan=!fan; $('fan').textContent=fan?'光の束を消す':'光の束を表示'; });
  $('cover').addEventListener('click',()=>{ cover=!cover; $('cover').textContent=cover?'かくすのをやめる':'レンズの上半分をかくす'; });
  if(fan) $('fan').textContent='光の束を消す';
  if(cover) $('cover').textContent='かくすのをやめる';
  cv.addEventListener('pointerdown',e=>{ const p=cpos(cv,e), x=p[0]/dpr, y=p[1]/dpr, s=st(), xo=X0-s.a*S;
    if(Math.abs(x-xo)<20&&y>Y0-HO*S-20&&y<Y0+8) drag='a';
    else if(Math.abs(y-Y0)<20&&(Math.abs(x-(X0-s.f*S))<18||Math.abs(x-(X0+s.f*S))<18)) drag='f';
    else if(x<X0-4){ drag='a'; moveA(x); }
    else return;
    try{ cv.setPointerCapture(e.pointerId); }catch(_){ } e.preventDefault(); });
  cv.addEventListener('pointermove',e=>{ if(!drag) return; const x=cpos(cv,e)[0]/dpr; if(drag==='a') moveA(x); else setv('f',clamp(Math.round(Math.abs(x-X0)/S*2)/2,5,15)); });
  const endDrag=()=>{ drag=null; }; cv.addEventListener('pointerup',endDrag); cv.addEventListener('pointercancel',endDrag);
  function frame(t){ const dt=last?Math.min(0.05,(t-last)/1000):0; last=t; tt+=dt; draw(); requestAnimationFrame(frame); }
  update(); frame(performance.now());
''')
