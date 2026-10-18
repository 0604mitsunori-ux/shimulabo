# -*- coding: utf-8 -*-
"""理科の授業向けシミュ（高校 化学基礎・生物）
   denshi-haichi … 化学基礎（2）物質の構成 ア（ｱ）物質の構成粒子 ㋐原子の構造 ㋑電子配置と周期表／（ｲ）㋐イオンとイオン結合
   iden-fudou    … 生物（1）生物の進化 ア（ｲ）遺伝子の変化と進化の仕組み ㋒進化の仕組み（遺伝的浮動・ハーディー・ワインベルグの法則）"""
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

MEXT_KOU = "https://www.mext.go.jp/a_menu/shotou/new-cs/1407074.htm"
def A(url, label): return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, label)
def NW(t): return '<span style="white-space:nowrap">%s</span>' % t

HELP = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const FF='"Hiragino Sans","Hiragino Kaku Gothic ProN","Noto Sans JP","Yu Gothic UI","Yu Gothic",Meiryo,sans-serif';
  function tx(s,x,y,size,col,align,bold){ ctx.font=(bold?'bold ':'')+size+'px '+FF; ctx.fillStyle=col; ctx.textAlign=align||'left'; ctx.fillText(s,x,y); ctx.textAlign='left'; }
  function tw(s,size,bold){ ctx.font=(bold?'bold ':'')+size+'px '+FF; return ctx.measureText(s).width; }
  function rr(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
  function dot(x,y,r,fill,stroke,lw){ ctx.fillStyle=fill; ctx.beginPath(); ctx.arc(x,y,r,0,6.2832); ctx.fill(); if(stroke){ ctx.strokeStyle=stroke; ctx.lineWidth=lw||1; ctx.stroke(); } }
  function wrap(s,x,y,maxW,lh,size,col,bold){ let line='', yy=y; for(const ch of s){ if(tw(line+ch,size,bold)>maxW && line){ tx(line,x,yy,size,col,'left',bold); line=ch; yy+=lh; } else line+=ch; } if(line) tx(line,x,yy,size,col,'left',bold); return yy; }
  const K=id=>$(id).previousElementSibling;
  const fld=id=>{ const e=$(id); return e?e.closest('.field'):null; };
  function showF(id,on){ const f=fld(id); if(f) f.style.display=on?'':'none'; }
'''

# ============================================================ 1 原子の構造と電子配置
DENSHI_ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
<p>原子は、中心の<b>原子核（陽子と中性子）</b>と、そのまわりの<b>電子殻（K殻・L殻・M殻・N殻）</b>に入った電子からできています。原子番号1〜18の原子では、電子は内側の殻から順に K殻2個 → L殻8個 → M殻 と入り、19番のカリウムと20番のカルシウムでは、M殻が8個のところで次のN殻に入ります。最も外側の殻の電子（価電子）の数は周期表の族と対応し、原子がイオンになるときは、電子を失ったり受け取ったりして、最も近い<b>貴ガスと同じ電子配置</b>になります。</p>
''' + N('<b>対応する単元</b>：高等学校「化学基礎」（2）物質の構成 ア（ｱ）物質の構成粒子「㋐原子の構造」「㋑電子配置と周期表」、（ｲ）物質と化学結合「㋐イオンとイオン結合」。学習指導要領の内容の取扱いでは、原子番号・質量数・同位体を扱い、放射性同位体とその利用にも触れること、「原子の電子配置」は代表的な典型元素を扱うこと、「元素の周期律」ではイオン化エネルギーの変化にも触れることとされています。解説では、原子の簡単なモデルを用いて原子番号20番までの代表的な典型元素を扱うとしています（21〜36番は「発展」で表示できます）。') + '''
<h2>授業での使い方</h2>
<h3>導入：1番から順に電子を入れていく</h3>
<p>「次 ▶」を押して、水素から順に原子番号を1つずつ増やします。電子が内側のK殻から入り、K殻が2個、L殻が8個でいっぱいになると次の殻に移ること、18番のアルゴンのあと19番のカリウムでN殻に入ることに気付かせます。周期表の下の段（周期）が変わるところで、新しい電子殻が使われ始めることも確かめます。</p>
<h3>展開：族と価電子、イオンの生成</h3>
<p>Li・Na・K（1族）、F・Cl（17族）、He・Ne・Ar（18族）を順に選び、同じ族では価電子の数が同じであることを周期表のいちばん下の行で確かめます。次にNaを選んで「⚡ イオンにする」を押すと、価電子1個が出ていき、Neと同じ電子配置のNa⁺になります。Clでは電子を1個受け取ってArと同じ電子配置のCl⁻になります。Mg・Al・O・Sでも試し、イオンの価数と族の関係を整理させます。</p>
<h3>まとめ：同位体とイオン化エネルギー</h3>
<p>Clを選んで「質量数（同位体）」を ³⁵Cl と ³⁷Cl で切り替えると、変わるのは中性子の数だけで、電子配置は変わらないことがわかります。「📈 イオン化エネルギー」を押すと、第一イオン化エネルギーが貴ガスで大きく、アルカリ金属で小さいという周期的な変化を棒グラフで確かめられます。</p>
<h3>生徒への問いの例</h3>
<ol>
<li>ナトリウム（Na）とカリウム（K）は、どちらも周期表の1族にある。電子配置をくらべると、何が共通しているだろう？</li>
<li>マグネシウム原子は、電子を2個失ってMg²⁺になる。電子を6個受け取るのではなく、2個失うほうが起こりやすいのはなぜだろう？できたイオンはどの貴ガスと同じ電子配置だろう？</li>
<li>炭素12（¹²C）と炭素14（¹⁴C）で、数がちがうのは陽子・中性子・電子のどれだろう？化学的な性質はちがうだろうか？</li>
</ol>
<h2>しくみ・解説</h2>
<h3>用語</h3>
<ul>
<li><b>原子番号</b>とは、原子核に含まれる陽子の数のことで、元素の種類はこの数で決まります。</li>
<li><b>質量数</b>とは、原子核に含まれる陽子の数と中性子の数の和のことです。</li>
<li><b>同位体（アイソトープ）</b>とは、原子番号が同じで中性子の数が異なるため、質量数が異なる原子どうしのことです。化学的な性質はほぼ同じです。</li>
<li><b>電子殻</b>とは、原子核のまわりで電子が入るいくつかの層のことで、内側から K殻・L殻・M殻・N殻…とよびます。</li>
<li><b>電子配置</b>とは、原子のもつ電子が、どの電子殻に何個ずつ入っているかを表したものです。</li>
<li><b>最外殻電子</b>とは最も外側の電子殻に入っている電子のことで、そのうち原子がイオンになったり結合したりするときにはたらく電子を<b>価電子</b>といいます。貴ガスの価電子の数は0とします。</li>
<li><b>貴ガス</b>とは18族の元素（He・Ne・Ar・Kr など）のことで、安定な電子配置をもつため、ほかの原子とほとんど反応せず、イオンにもなりにくい元素です。</li>
<li><b>閉殻</b>とは、電子殻に入ることのできる最大数の電子が入った状態です（HeのK殻2個、NeのL殻8個）。ArのM殻は8個ですが、最外殻に8個の電子をもつ配置も閉殻と同じように安定です。</li>
<li><b>（第一）イオン化エネルギー</b>とは、原子から電子1個を取り去って1価の陽イオンにするのに必要なエネルギーのことです。小さい原子ほど陽イオンになりやすい原子です。</li>
</ul>
<h3>式と数値の早見表</h3>
''' + T([["原子番号", "＝ 陽子の数 ＝ 原子の電子の数"], ["質量数", "＝ 陽子の数 ＋ 中性子の数"], ["中性子の数", "＝ 質量数 − 原子番号"],
          ["n番目の電子殻の最大数", "2n²（K殻 2、L殻 8、M殻 18、N殻 32）"], ["イオンの電子の数", "＝ 原子番号 − イオンの価数（陽イオン）／ ＋ 価数（陰イオン）"]],
         ["量", "式"]) + T([["陽子", "1.673×10⁻²⁷ kg", "＋1（＋1.602×10⁻¹⁹ C）", "原子核の中"],
                           ["中性子", "1.675×10⁻²⁷ kg", "0", "原子核の中"],
                           ["電子", "9.109×10⁻³¹ kg（陽子の約1/1840）", "−1（−1.602×10⁻¹⁹ C）", "電子殻"]],
                          ["粒子", "質量", "電荷", "場所"]) + '''
<p>原子の大きさは約10⁻¹⁰ m、原子核の大きさは約10⁻¹⁵〜10⁻¹⁴ m で、原子核は原子の10万分の1程度しかありません。このシミュレーターの図は、原子核をとても大きく描いています。</p>
<h3>原子番号1〜20の電子配置</h3>
''' + T([[str(z), s, NW(n), str(k), str(l) if l else "", str(m) if m else "", str(nn) if nn else "", str(v), ion]
          for z, s, n, k, l, m, nn, v, ion in [
              (1, "H", "水素", 1, 0, 0, 0, 1, "H⁺"), (2, "He", "ヘリウム", 2, 0, 0, 0, 0, "（なりにくい）"),
              (3, "Li", "リチウム", 2, 1, 0, 0, 1, "Li⁺"), (4, "Be", "ベリリウム", 2, 2, 0, 0, 2, "Be²⁺"),
              (5, "B", "ホウ素", 2, 3, 0, 0, 3, "（なりにくい）"), (6, "C", "炭素", 2, 4, 0, 0, 4, "（なりにくい）"),
              (7, "N", "窒素", 2, 5, 0, 0, 5, "N³⁻"), (8, "O", "酸素", 2, 6, 0, 0, 6, "O²⁻"),
              (9, "F", "フッ素", 2, 7, 0, 0, 7, "F⁻"), (10, "Ne", "ネオン", 2, 8, 0, 0, 0, "（なりにくい）"),
              (11, "Na", "ナトリウム", 2, 8, 1, 0, 1, "Na⁺"), (12, "Mg", "マグネシウム", 2, 8, 2, 0, 2, "Mg²⁺"),
              (13, "Al", "アルミニウム", 2, 8, 3, 0, 3, "Al³⁺"), (14, "Si", "ケイ素", 2, 8, 4, 0, 4, "（なりにくい）"),
              (15, "P", "リン", 2, 8, 5, 0, 5, "（なりにくい）"), (16, "S", "硫黄", 2, 8, 6, 0, 6, "S²⁻"),
              (17, "Cl", "塩素", 2, 8, 7, 0, 7, "Cl⁻"), (18, "Ar", "アルゴン", 2, 8, 8, 0, 0, "（なりにくい）"),
              (19, "K", "カリウム", 2, 8, 8, 1, 1, "K⁺"), (20, "Ca", "カルシウム", 2, 8, 8, 2, 2, "Ca²⁺")]],
         ["原子番号", "記号", "元素", "K", "L", "M", "N", "価電子", "なりやすいイオン"]) + '''
<h3>族と価電子の早見表（典型元素）</h3>
''' + T([["1族", "1", "H, Li, Na, K", "1価の陽イオン（Li⁺, Na⁺, K⁺）"], ["2族", "2", "Be, Mg, Ca", "2価の陽イオン（Mg²⁺, Ca²⁺）"],
          ["13族", "3", "B, Al", "Al³⁺"], ["14族", "4", "C, Si", "イオンになりにくい"], ["15族", "5", "N, P", "（N³⁻）"],
          ["16族", "6", "O, S", "2価の陰イオン（O²⁻, S²⁻）"], ["17族", "7", "F, Cl", "1価の陰イオン（F⁻, Cl⁻）"],
          ["18族", "0", "He, Ne, Ar", "イオンになりにくい（貴ガス）"]],
         ["族", "価電子の数", "元素の例", "イオン"]) + '''
<p>周期の番号は、電子が入っている最も外側の電子殻の番号（1＝K殻、2＝L殻、3＝M殻、4＝N殻）と一致します。1族のうちHを除いた元素をアルカリ金属、2族元素をアルカリ土類金属、17族元素をハロゲン、18族元素を貴ガスといいます。</p>
<h3>計算の例</h3>
<ol>
<li><b>²³Na の粒子の数</b>：陽子 11個、中性子 23−11＝12個、電子 11個。Na⁺ になると電子は 11−1＝10個（Neと同じ K2 L8）。</li>
<li><b>³⁵Cl⁻ の粒子の数</b>：陽子 17個、中性子 35−17＝18個、電子 17＋1＝18個（Arと同じ K2 L8 M8）。</li>
<li><b>塩素の原子量</b>：³⁵Cl（相対質量 35.0、存在比 75.8％）と ³⁷Cl（37.0、24.2％）から、35.0×0.758＋37.0×0.242＝35.48 → <b>約35.5</b>。</li>
</ol>
<h3>19番・20番の電子がN殻に入る理由</h3>
<p>M殻には最大18個の電子が入りますが、カリウムとカルシウムでは、M殻が8個になったところで次の電子がN殻に入ります。これは電子がエネルギーの低いところから順に入るためで、詳しくは「化学」以降で学ぶ電子軌道で説明されます。21番スカンジウムからの遷移元素では、N殻に2個（または1個）入ったままM殻の電子が増えていき（例：Fe は K2 L8 M14 N2）、29番の銅でM殻が18個になります。「表示する範囲」を「発展」にすると、21〜36番も確かめられます。</p>
<h3>イオン化エネルギーの周期的な変化</h3>
''' + T([["He", "2372", "Li", "520"], ["Ne", "2081", "Na", "496"], ["Ar", "1521", "K", "419"]],
         ["貴ガス", "第一イオン化エネルギー［kJ/mol］", "アルカリ金属", "第一イオン化エネルギー［kJ/mol］"]) + '''
<p>同じ周期では右へ行くほど大きくなる傾向があり、貴ガスで最大、次の周期のアルカリ金属で急に小さくなります。同じ族では、下へ行くほど（原子が大きくなり、最外殻電子が原子核から遠くなるため）小さくなります。</p>
''' + P('電子を円周上に並べたボーアの原子模型（模式図）で表しています。実際の電子は決まった円の上を回っているわけではありません。電子殻の大きさ・原子核の大きさ・陽子と中性子の並び方は模式的です。電子の位置は見やすさのためにゆっくり回しています。存在比は IUPAC の値を丸めたもの、原子量は教科書で計算に使う概数をあわせて表示しています。') + '''
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「高等学校学習指導要領（平成30年告示）解説 理科編 理数編」化学基礎（2）物質の構成</li>
<li>''' + A(MEXT_KOU, "文部科学省「高等学校学習指導要領（平成30年告示）解説」") + '''</li>
<li>日本化学会 原子量専門委員会「原子量表」／IUPAC「Isotopic compositions of the elements」（同位体の存在比）</li>
<li>''' + A("https://physics.nist.gov/PhysRefData/ASD/ionEnergy.html", "NIST Atomic Spectra Database「Ionization Energies」") + '''（第一イオン化エネルギー）</li>
<li>高等学校「化学基礎」の教科書「物質の構成粒子」「イオンとイオン結合」</li>
</ul>
'''

DENSHI_JS = HELP + r'''
  const SYM=['','H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar','K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr'];
  const NAME=['','水素','ヘリウム','リチウム','ベリリウム','ホウ素','炭素','窒素','酸素','フッ素','ネオン','ナトリウム','マグネシウム','アルミニウム','ケイ素','リン','硫黄','塩素','アルゴン','カリウム','カルシウム','スカンジウム','チタン','バナジウム','クロム','マンガン','鉄','コバルト','ニッケル','銅','亜鉛','ガリウム','ゲルマニウム','ヒ素','セレン','臭素','クリプトン'];
  // 原子量（IUPAC を丸めた値）と、計算で使う概数（教科書の表の値）
  const AWP=['','1.008','4.003','6.94','9.012','10.81','12.01','14.01','16.00','19.00','20.18','22.99','24.31','26.98','28.09','30.97','32.07','35.45','39.95','39.10','40.08','44.96','47.87','50.94','52.00','54.94','55.85','58.93','58.69','63.55','65.38','69.72','72.63','74.92','78.97','79.90','83.80'];
  const AWR=['','1.0','4.0','6.9','9.0','10.8','12','14','16','19','20','23','24','27','28','31','32','35.5','40','39','40','45','48','51','52','55','56','59','59','63.5','65.4','70','73','75','79','80','84'];
  // 第一イオン化エネルギー [kJ/mol]（NIST）
  const IE=[0,1312,2372,520,900,801,1086,1402,1314,1681,2081,496,738,578,787,1012,1000,1251,1521,419,590,633,659,651,653,717,762,760,737,745,906,579,762,947,941,1140,1351];
  // 同位体 [質量数, 存在比, メモ]（先頭＝代表的な質量数）
  const ISO={1:[[1,'99.99%',''],[2,'0.01%','重水素'],[3,'ごく微量','三重水素・放射性']],2:[[4,'ほぼ100%',''],[3,'0.0001%','']],3:[[7,'92.4%',''],[6,'7.6%','']],4:[[9,'100%','']],
    5:[[11,'80.1%',''],[10,'19.9%','']],6:[[12,'98.9%',''],[13,'1.1%',''],[14,'ごく微量','放射性・年代測定']],7:[[14,'99.6%',''],[15,'0.4%','']],8:[[16,'99.76%',''],[18,'0.20%',''],[17,'0.04%','']],
    9:[[19,'100%','']],10:[[20,'90.5%',''],[22,'9.3%',''],[21,'0.3%','']],11:[[23,'100%','']],12:[[24,'79.0%',''],[26,'11.0%',''],[25,'10.0%','']],13:[[27,'100%','']],
    14:[[28,'92.2%',''],[29,'4.7%',''],[30,'3.1%','']],15:[[31,'100%','']],16:[[32,'95.0%',''],[34,'4.25%',''],[33,'0.75%',''],[36,'0.01%','']],17:[[35,'75.8%',''],[37,'24.2%','']],
    18:[[40,'99.6%',''],[36,'0.34%',''],[38,'0.06%','']],19:[[39,'93.3%',''],[41,'6.7%',''],[40,'0.01%','放射性']],20:[[40,'96.9%',''],[44,'2.1%',''],[42,'0.65%',''],[48,'0.19%',''],[43,'0.14%','']],
    21:[[45,'100%','']],22:[[48,'73.7%','']],23:[[51,'99.8%','']],24:[[52,'83.8%','']],25:[[55,'100%','']],26:[[56,'91.8%',''],[54,'5.8%','']],27:[[59,'100%','']],28:[[58,'68.1%',''],[60,'26.2%','']],
    29:[[63,'69.2%',''],[65,'30.8%','']],30:[[64,'49.2%',''],[66,'27.7%','']],31:[[69,'60.1%',''],[71,'39.9%','']],32:[[74,'36.5%',''],[72,'27.5%','']],33:[[75,'100%','']],34:[[80,'49.6%',''],[78,'23.8%','']],
    35:[[79,'50.7%',''],[81,'49.3%','']],36:[[84,'57.0%',''],[86,'17.3%','']]};
  // なりやすいイオン [記号, 名前, 受け取る電子の数（負＝失う）]
  const ION={1:['H⁺','水素イオン',-1],3:['Li⁺','リチウムイオン',-1],4:['Be²⁺','ベリリウムイオン',-2],7:['N³⁻','窒化物イオン',3],8:['O²⁻','酸化物イオン',2],9:['F⁻','フッ化物イオン',1],
    11:['Na⁺','ナトリウムイオン',-1],12:['Mg²⁺','マグネシウムイオン',-2],13:['Al³⁺','アルミニウムイオン',-3],16:['S²⁻','硫化物イオン',2],17:['Cl⁻','塩化物イオン',1],
    19:['K⁺','カリウムイオン',-1],20:['Ca²⁺','カルシウムイオン',-2],34:['Se²⁻','セレン化物イオン',2],35:['Br⁻','臭化物イオン',1]};
  const CF4={19:[2,8,8,1],20:[2,8,8,2],21:[2,8,9,2],22:[2,8,10,2],23:[2,8,11,2],24:[2,8,13,1],25:[2,8,13,2],26:[2,8,14,2],27:[2,8,15,2],28:[2,8,16,2],29:[2,8,18,1],30:[2,8,18,2],
    31:[2,8,18,3],32:[2,8,18,4],33:[2,8,18,5],34:[2,8,18,6],35:[2,8,18,7],36:[2,8,18,8]};
  const NOBLE={2:'He',10:'Ne',18:'Ar',36:'Kr'};
  const SUP={'0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹'};
  const sup=n=>String(n).split('').map(c=>SUP[c]).join('');
  const SHN=['K','L','M','N'], RAD=[46,74,102,130], CX=150, CY=160;
  const TX0=34, TCW=33, TY0=342, TCH=34;
  const COLC={h:'#dbeafe',alkali:'#fde2e4',alkearth:'#ffedd5',halogen:'#dcfce7',noble:'#ede9fe',trans:'#e5e7eb',main:'#f1f5f9'};
  const CATN={h:'非金属（1族）',alkali:'アルカリ金属',alkearth:'アルカリ土類金属',halogen:'ハロゲン',noble:'貴ガス',trans:'遷移元素（発展）',main:'典型元素'};
  const C={ink:'#0f172a',sub:'#64748b',p:'#e0483e',n:'#94a3b8',e:'#2563eb',v:'#f59e0b',st:'#16a34a',red:'#dc2626'};
  function conf(z){ return z<=18 ? [Math.min(z,2),clamp(z-2,0,8),clamp(z-10,0,8),0] : CF4[z].slice(); }
  function outer(c){ let o=0; for(let i=0;i<4;i++) if(c[i]>0) o=i; return o; }
  function group(z){ if(z===1) return 1; if(z===2) return 18; if(z<=10) return z<=4?z-2:z+8; if(z<=18) return z<=12?z-10:z; return z-18; }
  function period(z){ return z<=2?1:z<=10?2:z<=18?3:4; }
  function cat(z){ const g=group(z); return z===1?'h':g===18?'noble':g===1?'alkali':g===2?'alkearth':g===17?'halogen':(g>=3&&g<=12)?'trans':'main'; }
  function valence(z){ const g=group(z); if(g>=3&&g<=12) return null; return g===18?0:g<=2?g:g-10; }
  function ionConf(z){ const c=conf(z), io=ION[z]; if(!io) return c; c[outer(c)]+=io[2]; return c; }
  function cs(c){ const s=[]; for(let i=0;i<4;i++) if(c[i]>0) s.push(SHN[i]+c[i]); return s.length?s.join(' '):'電子なし'; }

  let z=11, rng=20, iso=0, ionOn=false, ionT=0, ie=false, flash=0, last=0, tm=0, nuc=null, nucKey='';
  const massA=()=>ISO[z][Math.min(iso,ISO[z].length-1)][0];

  // 原子核：陽子と中性子をひまわり状に並べる（並べ方は模式的）
  function makeNuc(){ const A=massA(), key=z+'-'+A; if(key===nucKey) return; nucKey=key;
    const tp=[]; for(let i=0;i<A;i++) tp.push(i<z?1:0);
    let sd=z*131+A*7; const r=()=>{ sd=(sd*16807)%2147483647; return sd/2147483647; };
    for(let i=A-1;i>0;i--){ const j=Math.floor(r()*(i+1)); const t=tp[i]; tp[i]=tp[j]; tp[j]=t; }
    const Rn=Math.min(31,4.7*Math.sqrt(A)), pr=Math.max(3,Rn/Math.sqrt(A)*1.12);
    nuc={pr:pr,pts:tp.map((t,k)=>{ const rad=A===1?0:Rn*Math.sqrt((k+0.5)/A)*0.92, th=k*2.39996; return [CX+rad*Math.cos(th),CY+rad*Math.sin(th),t]; }).reverse()}; }
  function drawNuc(){ makeNuc(); nuc.pts.forEach(q=>{ const g=ctx.createRadialGradient(q[0]-nuc.pr*0.35,q[1]-nuc.pr*0.4,nuc.pr*0.15,q[0],q[1],nuc.pr);
      g.addColorStop(0,q[2]?'#ffb4a8':'#eef2f7'); g.addColorStop(1,q[2]?C.p:C.n); ctx.fillStyle=g; ctx.beginPath(); ctx.arc(q[0],q[1],nuc.pr,0,6.2832); ctx.fill();
      ctx.strokeStyle='rgba(15,23,42,.25)'; ctx.lineWidth=0.6; ctx.stroke(); }); }
  function elec(x,y,col,a){ ctx.globalAlpha=a==null?1:a; dot(x,y,5.6,col,'#0f172a',1); ctx.fillStyle='rgba(255,255,255,.65)'; ctx.beginPath(); ctx.arc(x-1.6,y-1.8,1.7,0,6.2832); ctx.fill(); ctx.globalAlpha=1; }
  const ease=t=>t<0.5?2*t*t:1-Math.pow(-2*t+2,2)/2;

  function drawBohr(){
    ctx.save(); ctx.beginPath(); ctx.rect(0,0,298,304); ctx.clip();
    tx('原子のモデル（模式図）',8,18,13,C.ink,'left',true);
    const c=conf(z), o=outer(c), io=ION[z], t=ease(ionT), ionNow=io&&ionT>0.5, cd=ionNow?ionConf(z):c, od=outer(cd);
    const nob=valence(z)===0 || (ionNow && NOBLE[cd.reduce((a,b)=>a+b,0)]);
    for(let i=0;i<4;i++){ const solid=cd[i]>0 || (io&&io[2]<0&&i===o&&ionT<1);
      ctx.strokeStyle=solid?'#94a3b8':'#e2e8f0'; ctx.lineWidth=solid?1.6:1.2; ctx.setLineDash(solid?[]:[4,5]); ctx.beginPath(); ctx.arc(CX,CY,RAD[i],0,6.2832); ctx.stroke(); ctx.setLineDash([]);
      const lx=CX+RAD[i]*0.72+2, ly=CY+RAD[i]*0.70+12; tx(SHN[i],lx,ly,11,solid?'#475569':'#cbd5e1','left',true); }
    drawNuc();
    for(let i=0;i<4;i++){ const n=c[i]; const rot=tm*0.22*(i%2?-1:1)/(1+i*0.25)-Math.PI/2;
      const valShell=(i===o), isNobOuter=(i===od && nob);
      const col=isNobOuter?C.st:(valShell&&valence(z)!==0&&!ionNow)?C.v:C.e;
      if(io&&i===o&&io[2]<0){ for(let j=0;j<n;j++){ const a=rot+j*6.2832/n, r=RAD[i]+t*175; if(t<1) elec(CX+r*Math.cos(a),CY+r*Math.sin(a),C.v,1-t*0.6); } continue; }
      if(io&&i===o&&io[2]>0){ const m=n+io[2];
        for(let j=0;j<m;j++){ const af=rot+j*6.2832/m;
          if(j<n){ const a0=rot+j*6.2832/n, a=a0+(af-a0)*t; elec(CX+RAD[i]*Math.cos(a),CY+RAD[i]*Math.sin(a),ionNow?C.st:C.v); }
          else if(t>0){ const r=RAD[i]+(1-t)*190, a=af+(1-t)*0.7; elec(CX+r*Math.cos(a),CY+r*Math.sin(a),ionNow?C.st:'#f97316'); } }
        continue; }
      for(let j=0;j<n;j++){ const a=rot+j*6.2832/n; elec(CX+RAD[i]*Math.cos(a),CY+RAD[i]*Math.sin(a),col); } }
    // ラベル
    const lab=ionNow?io[0]:SYM[z]+' 原子'; tx(lab,8,44,ionNow?24:16,ionNow?C.red:C.ink,'left',true);
    if(ionNow){ const q=-io[2]; tx('電荷 '+(q>0?'＋':'−')+Math.abs(q),8,62,11,C.red,'left',true); }
    else tx('電気的に中性',8,62,11,C.sub);
    tx('● 陽子',236,18,11,C.p,'left',true); tx('● 中性子',236,32,11,'#64748b','left',true);
    tx('● 電子',8,262,11,C.e,'left',true); tx('● 価電子',8,277,11,'#d97706','left',true); tx('● 安定な最外殻',8,292,11,C.st,'left',true);
    tx('原子をタップ→イオン',292,296,10,'#94a3b8','right');
    ctx.restore(); }

  function drawInfo(){ const x0=304,y0=6,w=330,h=296; ctx.fillStyle='#f8fafc'; ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; rr(x0,y0,w,h,10); ctx.fill(); ctx.stroke();
    const g=group(z), ct=cat(z), A=massA(), c=conf(z), io=ION[z], ionNow=io&&ionT>0.5, cd=ionNow?ionConf(z):c, od=outer(cd), v=valence(z);
    tx('第'+period(z)+'周期・'+g+'族',316,26,12,C.sub,'left',true);
    const cw=tw(CATN[ct],11,true); ctx.fillStyle=COLC[ct]; rr(626-cw-12,13,cw+12,19,9); ctx.fill(); tx(CATN[ct],620-cw,27,11,'#334155','left',true);
    tx(String(A),350,48,14,C.ink,'right',true); tx(String(z),350,80,14,C.ink,'right',true);
    const sw=tw(SYM[z],42,true); tx(SYM[z],354,80,42,C.ink,'left',true);
    const nx=Math.max(420,358+sw+14); tx(NAME[z],nx,58,20,C.ink,'left',true); tx('原子番号 '+z+'・質量数 '+A,nx,80,12,C.sub);
    ctx.strokeStyle='#e2e8f0'; ctx.beginPath(); ctx.moveTo(316,94); ctx.lineTo(622,94); ctx.stroke();
    let x=316; const ne=cd.reduce((a,b)=>a+b,0);
    [['陽子',z,C.p],['中性子',A-z,'#64748b'],['電子',ne,C.e]].forEach(q=>{ dot(x+5,113,5,q[2]); tx(q[0],x+14,118,12,C.sub); const lw=tw(q[0],12); tx(String(q[1]),x+16+lw,118,16,C.ink,'left',true); x+=22+lw+tw(String(q[1]),16,true)+16; });
    tx('電子配置',316,150,12,C.sub,'left',true);
    for(let i=0;i<4;i++){ const bx=380+i*61, on=cd[i]>0, isO=on&&i===od; ctx.fillStyle=!on?'#fff':isO?((v===0||ionNow)?'#dcfce7':'#fef3c7'):'#e0ecff'; ctx.strokeStyle=isO?((v===0||ionNow)?C.st:'#d97706'):'#cbd5e1'; ctx.lineWidth=isO?2:1;
      rr(bx,132,55,28,7); ctx.fill(); ctx.stroke(); tx(SHN[i],bx+8,151,11,C.sub,'left',true); tx(on?String(cd[i]):'—',bx+44,153,17,on?C.ink:'#cbd5e1','right',true); }
    tx('価電子',316,186,12,C.sub,'left',true);
    if(v===null){ tx('—',380,188,20,C.ink,'left',true); tx('遷移元素：最外殻電子 '+c[outer(c)]+'個',408,186,12,C.sub); }
    else { tx(v+'個',380,188,20,ionNow?'#94a3b8':C.ink,'left',true); tx(v===0?'（最外殻 '+c[outer(c)]+'個で安定）':'（最外殻電子 '+v+'個）',380+tw(v+'個',20,true)+8,186,12,C.sub); }
    tx('イオン',316,216,12,C.sub,'left',true);
    const fl=flash>0;
    if(io){ const tgt=NOBLE[ionConf(z).reduce((a,b)=>a+b,0)], k=Math.abs(io[2]);
      tx(io[0]+'（'+io[1]+'）',380,218,15,ionNow?C.red:C.ink,'left',true);
      wrap((io[2]<0?'電子を'+k+'個失い、':'電子を'+k+'個受け取り、')+(tgt?tgt+'と同じ電子配置に':'陽子だけになる')+(z===7?'（参考）':''),380,236,240,15,12,fl?C.red:C.sub); }
    else { const m=v===0?'貴ガス：安定な電子配置なので、イオンになりにくい':v===null?'発展：遷移元素はイオンの価数が複数ある（例 Fe²⁺・Fe³⁺、Cu⁺・Cu²⁺）':(g===14||g===15)?'単原子のイオンになりにくい（共有結合をつくる）':'この範囲では扱いません';
      wrap(m,380,218,236,15,12,fl?C.red:C.ink,fl); }
    tx('同位体',316,266,12,C.sub,'left',true);
    let ix=380, iy=266; ISO[z].slice(0,4).forEach((q,i)=>{ const s=sup(q[0])+SYM[z]+' '+q[1]+(q[2]?'（'+q[2]+'）':''), cur=i===iso, ww=tw(s,12,cur)+12;
      if(ix+ww>628){ ix=380; iy+=15; } tx(s,ix,iy,12,cur?C.red:C.sub,'left',cur); ix+=ww; });
    tx('原子量 '+AWP[z]+'（計算では '+AWR[z]+'）',316,Math.min(296,Math.max(292,iy+18)),12,C.ink); }

  const GX0=346,GX1=628,GY0=46,GY1=262;
  function ieX(k){ return GX0+(k-0.5)/rng*(GX1-GX0); }
  function drawIE(){ const x0=304,y0=6,w=330,h=296; ctx.fillStyle='#f8fafc'; ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; rr(x0,y0,w,h,10); ctx.fill(); ctx.stroke();
    tx('第一イオン化エネルギー［kJ/mol］',316,26,13,C.ink,'left',true);
    for(let v=0;v<=2500;v+=500){ const y=GY1-v/2500*(GY1-GY0); ctx.strokeStyle=v?'#e2e8f0':'#94a3b8'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(GX0,y); ctx.lineTo(GX1,y); ctx.stroke(); tx(String(v),GX0-4,y+4,10,C.sub,'right'); }
    const bw=(GX1-GX0)/rng*0.72;
    for(let k=1;k<=rng;k++){ const x=ieX(k), y=GY1-IE[k]/2500*(GY1-GY0), ct=cat(k); ctx.fillStyle=k===z?C.red:ct==='noble'?'#8b5cf6':ct==='alkali'?'#f472b6':'#93c5fd'; ctx.fillRect(x-bw/2,y,bw,GY1-y);
      if(rng<=20||k===z||(k%2===1&&Math.abs(k-z)>1)) tx(SYM[k],x,GY1+13,rng<=20?10:9,k===z?C.red:C.sub,'center',k===z); }
    [2,10,18].forEach(k=>{ if(k<rng){ const x=(ieX(k)+ieX(k+1))/2; ctx.strokeStyle='rgba(100,116,139,.35)'; ctx.setLineDash([3,3]); ctx.beginPath(); ctx.moveTo(x,GY0); ctx.lineTo(x,GY1); ctx.stroke(); ctx.setLineDash([]); } });
    const s=SYM[z]+'（'+NAME[z]+'）'+IE[z]+' kJ/mol', xs=clamp(ieX(z),316+tw(s,12,true)/2,624-tw(s,12,true)/2); tx(s,xs,40,12,C.red,'center',true);
    tx('■ 貴ガス',316,292,11,'#8b5cf6','left',true); tx('■ アルカリ金属',372,292,11,'#db2777','left',true); tx('点線＝周期の区切り・棒をタップ',628,292,10,C.sub,'right'); }

  function cell(k){ return [TX0+(group(k)-1)*TCW, TY0+(period(k)-1)*TCH]; }
  function drawTable(){
    tx('周期表（タップして元素を選ぶ）',8,322,13,C.ink,'left',true); tx('上の数字＝族、左の数字＝周期',632,322,11,C.sub,'right');
    const g=group(z); ctx.fillStyle='rgba(250,204,21,.22)'; ctx.fillRect(TX0+(g-1)*TCW-1,TY0-14,TCW+2,4*TCH+36);
    for(let gg=1;gg<=18;gg++) tx(String(gg),TX0+(gg-1)*TCW+TCW/2,TY0-4,10,gg===g?'#a16207':C.sub,'center',gg===g);
    for(let p=1;p<=4;p++) tx(String(p),TX0-10,TY0+(p-1)*TCH+TCH/2+4,11,p===period(z)?'#a16207':C.sub,'center',true);
    for(let k=1;k<=36;k++){ const q=cell(k), dim=k>rng; ctx.globalAlpha=dim?0.32:1; ctx.fillStyle=COLC[cat(k)]; ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1;
      ctx.fillRect(q[0]+1,q[1]+1,TCW-2,TCH-2); ctx.strokeRect(q[0]+1.5,q[1]+1.5,TCW-3,TCH-3);
      tx(String(k),q[0]+4,q[1]+11,8,C.sub); tx(SYM[k],q[0]+TCW/2,q[1]+27,14,C.ink,'center',true); ctx.globalAlpha=1; }
    const q=cell(z); ctx.strokeStyle=C.red; ctx.lineWidth=3; ctx.strokeRect(q[0]+1,q[1]+1,TCW-2,TCH-2);
    tx(rng<=20?'↑ 21〜36番は発展（「表示する範囲」で切り替え）':'↑ 3〜12族＝遷移元素（最外殻電子は1〜2個）',TX0+2*TCW+4,TY0+4*TCH+15,10,'#64748b','left',true);
    // 空いているところに凡例と説明
    let lx=TX0+TCW+8; [['alkali','アルカリ金属'],['alkearth','アルカリ土類金属'],['trans','遷移元素'],['halogen','ハロゲン'],['noble','貴ガス']].forEach(a=>{ ctx.fillStyle=COLC[a[0]]; ctx.fillRect(lx,TY0+9,12,12); ctx.strokeStyle='#94a3b8'; ctx.strokeRect(lx+.5,TY0+9.5,11,11); tx(a[1],lx+16,TY0+20,11,'#334155'); lx+=tw(a[1],11)+30; });
    tx('同じ族（たての列）＝価電子の数が同じ → 性質が似る',TX0+2*TCW+6,TY0+TCH+16,11,'#334155','left',true);
    tx('周期（横の行）の番号＝電子が入る最も外側の殻',TX0+2*TCW+6,TY0+TCH+33,11,'#334155');
    tx('（1＝K殻、2＝L殻、3＝M殻、4＝N殻）',TX0+2*TCW+6,TY0+TCH+50,11,'#334155');
    tx('価電子',4,TY0+4*TCH+16,10,'#a16207','left',true);
    [[1,'1'],[2,'2'],[13,'3'],[14,'4'],[15,'5'],[16,'6'],[17,'7'],[18,'0']].forEach(a=>tx(a[1],TX0+(a[0]-1)*TCW+TCW/2,TY0+4*TCH+16,12,a[0]===g?'#a16207':'#334155','center',true)); }

  function draw(){ ctx.fillStyle='#fff'; ctx.fillRect(0,0,W,H); drawBohr(); if(ie) drawIE(); else drawInfo(); drawTable(); }
  function stats(){ const io=ION[z], ionNow=io&&ionOn, cd=ionNow?ionConf(z):conf(z), v=valence(z);
    setStat('sEl',SYM[z]+'（'+z+'番）'); setStat('sConf',cs(cd)); setStat('sVal',v===null?'—（遷移元素）':v+'個'); setStat('sIon',io?io[0]:'なりにくい');
    const tgt=io?NOBLE[ionConf(z).reduce((a,b)=>a+b,0)]:null;
    setShare('【電子配置】'+NAME[z]+' '+SYM[z]+'（原子番号'+z+'）は '+cs(conf(z))+(v===null?'':'、価電子'+v+'個')+(io?'。電子を'+Math.abs(io[2])+'個'+(io[2]<0?'失って':'受け取って')+io[0]+(tgt?'（'+tgt+'と同じ電子配置）':'')+'になる':'')+'｜シミュラボ'); }
  function fillIso(){ $('iso').innerHTML=ISO[z].map((q,i)=>'<option value="'+i+'">'+sup(q[0])+SYM[z]+'（中性子'+(q[0]-z)+'・'+q[1]+'）</option>').join(''); $('iso').value='0'; }
  function setZ(k){ z=clamp(k,1,rng); iso=0; ionOn=false; ionT=0; flash=0; $('z').value=z; $('zL').textContent=z+'（'+SYM[z]+'）'; fillIso(); $('ion').textContent='⚡ イオンにする'; stats(); draw(); }
  function setRng(r){ rng=r; $('rng').value=String(r); $('z').max=r; if(z>r) setZ(r); else { $('z').value=z; draw(); } }
  function toggleIon(){ if(!ION[z]){ flash=1.6; draw(); return; } ionOn=!ionOn; $('ion').textContent=ionOn?'↩ 原子にもどす':'⚡ イオンにする'; stats(); }
  $('z').addEventListener('input',()=>setZ(+$('z').value));
  $('rng').addEventListener('change',()=>setRng(+$('rng').value));
  $('iso').addEventListener('change',()=>{ iso=+$('iso').value; draw(); });
  $('prev').addEventListener('click',()=>setZ(z>1?z-1:rng));
  $('next').addEventListener('click',()=>setZ(z<rng?z+1:1));
  $('ion').addEventListener('click',toggleIon);
  $('ieb').addEventListener('click',()=>{ ie=!ie; $('ieb').textContent=ie?'📋 元素の情報にもどす':'📈 イオン化エネルギー'; draw(); });
  cv.addEventListener('pointerdown',e=>{ const p=cpos(cv,e), x=p[0]/dpr, y=p[1]/dpr;
    if(y>=TY0&&y<TY0+4*TCH&&x>=TX0&&x<TX0+18*TCW){ const gg=Math.floor((x-TX0)/TCW)+1, pp=Math.floor((y-TY0)/TCH)+1;
      for(let k=1;k<=36;k++) if(group(k)===gg&&period(k)===pp){ if(k>rng) setRng(36); setZ(k); return; } return; }
    if(ie&&x>=GX0&&x<=GX1&&y>=GY0-20&&y<=GY1+16){ setZ(clamp(Math.floor((x-GX0)/(GX1-GX0)*rng)+1,1,rng)); return; }
    if(x<298&&y<304&&Math.hypot(x-CX,y-CY)<RAD[3]+10) toggleIon(); });
  function frame(ts){ const dt=last?Math.min(0.1,(ts-last)/1000):0; last=ts; tm+=dt;
    const tgt=ionOn?1:0; if(ionT!==tgt){ ionT=tgt>ionT?Math.min(1,ionT+dt/1.3):Math.max(0,ionT-dt/0.9); }
    if(flash>0) flash=Math.max(0,flash-dt); draw(); requestAnimationFrame(frame); }
  setZ(11); requestAnimationFrame(frame);
'''

sim(slug="denshi-haichi", cat="rika", emoji="⚛️", score=82,
    title="原子の構造と電子配置のシミュレーター（周期表・価電子・イオン）",
    title_tag="電子配置のシミュレーター｜K殻・L殻・M殻と価電子、周期表、イオンの生成（化学基礎）",
    meta_desc="周期表のマスをタップすると、原子核（陽子・中性子）と電子殻K・L・M・Nに電子が入るボーア模型を表示。価電子の数、貴ガスの安定な電子配置、イオンになるときの電子の出入り、同位体の切り替え、イオン化エネルギーのグラフまで。高校「化学基礎」物質の構成粒子の授業向け。",
    og_title="原子の構造と電子配置のシミュレーター（周期表・価電子・イオン）",
    og_desc="原子番号1〜20（発展36）を選ぶと、電子がK殻2・L殻8・M殻8…と入るようすをボーア模型で表示。Na→Na⁺、Cl→Cl⁻ で電子が出入りして貴ガスと同じ電子配置になるアニメつき。",
    card_desc="周期表をタップすると電子殻に電子が入る。価電子・イオンの生成・同位体・イオン化エネルギーまで確かめられる。",
    lead="周期表のマスをタップすると、その原子の原子核（陽子・中性子）と、K殻・L殻・M殻・N殻に入る電子をボーア模型で表示します。「⚡ イオンにする」で電子が出入りして貴ガスと同じ電子配置になるようす、同位体の切り替え、イオン化エネルギーの周期的な変化も確かめられます。",
    model="化学基礎 物質の構成粒子（原子の構造・電子配置と周期表）",
    level="高校（化学基礎）、中学3年の発展",
    unit="高等学校 化学基礎（2）物質の構成 ア（ｱ）物質の構成粒子・（ｲ）㋐イオンとイオン結合",
    canvas=canvas(640, 500, light=True),
    controls=slider("z", "原子番号", 1, 20, 11, 1)
             + select("rng", "表示する範囲", [("20", "化学基礎（1〜20番）"), ("36", "発展（21〜36番も）")])
             + select("iso", "質量数（同位体）", [("0", "²³Na")]),
    buttons=btn("prev", "◀ 前") + btn("next", "次 ▶") + btn("ion", "⚡ イオンにする", True) + btn("ieb", "📈 イオン化エネルギー"),
    stats=stats([("sEl", "元素（原子番号）", False), ("sConf", "電子配置", True), ("sVal", "価電子の数", False), ("sIon", "なりやすいイオン", False)]),
    legend="左上：原子のモデル（赤＝陽子、灰色＝中性子、青＝電子、オレンジ＝価電子、緑＝貴ガスと同じ安定な最外殻。大きさは模式的で、原子核はとても大きく描いています）。原子をタップしてもイオンにできます。右上：元素の情報（左上の数字＝質量数、左下の数字＝原子番号）。下：周期表（黄色の列＝同じ族。いちばん下の行＝価電子の数）。",
    article=DENSHI_ARTICLE,
    faqs=[("価電子と最外殻電子のちがいは？", "最外殻電子は最も外側の電子殻に入っている電子のことです。価電子は、そのうちイオンになったり結合したりするときにはたらく電子で、典型元素では最外殻電子の数と同じです。ただし貴ガス（He・Ne・Arなど）は安定でほとんど反応しないので、価電子の数を0とします。"),
          ("K殻・L殻・M殻・N殻に入る電子の最大数は？", "内側から n 番目の電子殻には最大 2n² 個の電子が入ります。K殻（n＝1）は2個、L殻（n＝2）は8個、M殻（n＝3）は18個、N殻（n＝4）は32個です。"),
          ("カリウムの電子配置は？M殻にまだ入るのに、なぜN殻に入るの？", "カリウム（原子番号19）の電子配置は K2 L8 M8 N1 です。M殻には最大18個入りますが、電子はエネルギーの低いところから順に入るため、M殻が8個になったところで19個目はN殻に入ります。カルシウムは K2 L8 M8 N2 です。"),
          ("イオンになると、なぜ貴ガスと同じ電子配置になるの？", "貴ガスの電子配置（最外殻が2個または8個）は特に安定だからです。価電子が1〜3個の原子は電子を失って陽イオンに（Na→Na⁺はNeと同じ）、価電子が6〜7個の原子は電子を受け取って陰イオンに（Cl→Cl⁻はArと同じ）なりやすくなります。"),
          ("同位体どうしで化学的な性質は変わる？", "ほとんど変わりません。同位体は中性子の数（質量数）だけがちがい、陽子と電子の数、つまり電子配置が同じだからです。ただし質量がちがうので、重水素（²H）を含む水が少し重いなど、物理的な性質にはわずかな差があります。"),
          ("元素記号の左上と左下の数字は何？", "左上が質量数（陽子の数＋中性子の数）、左下が原子番号（陽子の数）です。たとえば ²³₁₁Na は、陽子11個・中性子12個のナトリウム原子を表します。")],
    rel=[("chuwa-ion", "⚗️", "酸・アルカリと中和のシミュレーター"), ("joutai-henka", "🧊", "状態変化と粒子のシミュレーター"),
         ("kagaku-shitsuryou", "🧪", "化学変化と質量シミュレーター"), ("double-slit", "🌈", "ダブルスリット実験")],
    js=DENSHI_JS)


# ============================================================ 2 遺伝的浮動とハーディー・ワインベルグの法則
FUDOU_ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
<p>集団の<b>遺伝子頻度</b>は、自然選択がはたらかなくても、配偶子が次の世代に受けつがれるときの偶然によって変化します（<b>遺伝的浮動</b>）。集団が小さいほど1世代あたりの変化が大きく、ある対立遺伝子が<b>固定</b>（頻度1）したり<b>消失</b>（頻度0）したりするまでの世代が短くなります。一方、十分に大きな集団で自由な交配が行われ、突然変異・移入や移出・自然選択がなければ、遺伝子頻度も遺伝子型頻度 p²：2pq：q² も世代を重ねても変わりません（<b>ハーディー・ワインベルグの法則</b>）。</p>
''' + N('<b>対応する単元</b>：高等学校「生物」（1）生物の進化 ア（ｲ）遺伝子の変化と進化の仕組み「㋒進化の仕組み」。学習指導要領解説では、遺伝子頻度が変化する要因として遺伝的浮動と自然選択を扱うとし、2色のコインを一対の遺伝子に見立てたモデル実験（親の世代のコインを比率を保ったまま数倍に増やし、そこから同じ数を無作為に選んで子の世代とする操作を繰り返す）が例示されています。このシミュレーターは、その操作をコンピュータで何百世代もくり返すものです。') + '''
<h2>授業での使い方</h2>
<h3>導入：コインのモデル実験とつなぐ</h3>
<p>班ごとに2色のコイン（各10枚＝N＝10個体分の遺伝子20個）でモデル実験を数世代行い、結果をグラフにします。次にこのシミュレーターを N＝10 にして「▶ 実行」を押し、同じ操作を100世代分くり返すと、班ごとにちがう結果になり、やがてどちらかの色に固定されることを確かめます。</p>
<h3>展開：集団の大きさを変えて仮説を確かめる</h3>
<p>「集団が大きいと、遺伝子頻度の変化はどうなるか」と仮説を立てさせ、N＝10・100・1000 で比べます。「乱数」を「固定 No.1」にすると、同じ条件では何度押しても同じ結果になるので、電子黒板とタブレットで同じグラフを見ながら話し合えます。「びん首効果」をありにすると、途中の5世代だけ個体数が減ったときに遺伝子頻度が大きくずれ、その後も戻らないようすが見られます。「選択の強さ」を0.05などにすると、Aの頻度が全体として上がる（自然選択）一方で、小さい集団では有利なAでも偶然消失することがあるとわかります。</p>
<h3>まとめ：ハーディー・ワインベルグの法則</h3>
<p>「モード」を「ハーディー・ワインベルグ」にし、「親の世代」を「AAとaaだけ」にして「▶ 次の世代をつくる」を押します。ヘテロ接合体のいない親の集団からでも、1世代の自由な交配で子の遺伝子型頻度が p²：2pq：q² になり、その後は世代を重ねても変わらないことを確かめます。集団を小さくすると、理論の値からずれやすくなることも確認します。</p>
<h3>生徒への問いの例</h3>
<ol>
<li>選択がはたらいていない（s＝0）のに、Aの頻度が1や0になる集団があるのはなぜだろう？</li>
<li>N＝10 と N＝1000 では、固定や消失が起こるまでの世代数はどうちがうだろう？絶滅危惧種のような小さな集団にとって、これは何を意味するだろう？</li>
<li>ある集団で潜性の形質を示す個体が16％いた。顕性の形質を示す個体のうち、ヘテロ接合体（Aa）は何％だろう？</li>
</ol>
<h2>しくみ・解説</h2>
<h3>用語</h3>
<ul>
<li><b>遺伝子プール</b>とは、ある集団の全個体がもつ遺伝子全体のことです。</li>
<li><b>遺伝子頻度</b>とは、遺伝子プールの中で、ある遺伝子座の対立遺伝子全体のうち特定の対立遺伝子が占める割合のことです（Aの頻度 p、aの頻度 q、p＋q＝1）。</li>
<li><b>遺伝子型頻度</b>とは、集団の中で AA・Aa・aa などの各遺伝子型をもつ個体が占める割合のことです。</li>
<li><b>遺伝的浮動</b>とは、次の世代に受けつがれる配偶子が偶然によって決まることで、遺伝子頻度が世代ごとに不規則に変動する現象です。</li>
<li><b>固定</b>とは、遺伝的浮動や自然選択の結果、集団の中である対立遺伝子の頻度が1（ほかの対立遺伝子が消失）になることです。</li>
<li><b>びん首効果</b>とは、集団の大きさが一時的に極端に小さくなることで、遺伝子頻度が大きく変わったり遺伝的多様性が失われたりする現象です。</li>
<li><b>自然選択</b>とは、生存や繁殖に有利な形質をもつ個体がより多くの子を残すことで、その形質の遺伝子の頻度が高まることです。</li>
<li><b>ハーディー・ワインベルグの法則</b>とは、①集団が十分に大きい、②自由に交配が行われる、③突然変異が起こらない、④移入や移出がない、⑤自然選択がはたらかない、という条件のもとでは、遺伝子頻度が世代を経ても変化しないという法則です。</li>
</ul>
<h3>ハーディー・ワインベルグの法則の式</h3>
<p>Aの頻度を p、aの頻度を q（p＋q＝1）とすると、配偶子の組み合わせ（下の表）から、次の世代の遺伝子型頻度は</p>
<p style="text-align:center;font-weight:800;">(pA＋qa)² ＝ p² AA ＋ 2pq Aa ＋ q² aa</p>
''' + T([["A（p）", "AA（p²）", "Aa（pq）"], ["a（q）", "Aa（pq）", "aa（q²）"]], ["卵＼精子", "A（p）", "a（q）"]) + '''
<p>次の世代のAの頻度は p²＋pq＝p(p＋q)＝<b>p</b> で、もとと変わりません。親の遺伝子型の割合がどうであっても、遺伝子頻度が p・q なら、1世代の自由な交配で遺伝子型頻度は p²：2pq：q² になります。</p>
<h3>早見表：遺伝子頻度と遺伝子型頻度</h3>
''' + T([["0.9", "0.1", "0.81", "0.18", "0.01"], ["0.8", "0.2", "0.64", "0.32", "0.04"], ["0.7", "0.3", "0.49", "0.42", "0.09"],
          ["0.6", "0.4", "0.36", "0.48", "0.16"], ["0.5", "0.5", "0.25", "0.50", "0.25"], ["0.99", "0.01", "0.9801", "0.0198", "0.0001"]],
         ["p（Aの頻度）", "q（aの頻度）", "AA（p²）", "Aa（2pq）", "aa（q²）"]) + '''
<h3>計算問題の例</h3>
<ol>
<li><b>潜性ホモ接合体の割合から q を求める</b>：潜性の形質（aa）を示す個体が16％のとき、q²＝0.16 より q＝0.4、p＝1−0.4＝0.6。AA＝0.6²＝0.36（36％）、Aa＝2×0.6×0.4＝0.48（48％）。顕性の形質を示す個体（84％）のうち Aa は 0.48÷0.84＝約57％です。</li>
<li><b>まれな潜性の形質</b>：aa が1万人に1人（q²＝0.0001）のとき、q＝0.01、p＝0.99。ヘテロ接合体は 2pq＝2×0.99×0.01＝0.0198、<b>約50人に1人</b>です。形質として現れる人の約200倍の人が、潜性の遺伝子をもっていることになります。</li>
<li><b>個体数から遺伝子頻度を求める</b>：1000個体の集団で AA 360、Aa 480、aa 160 のとき、Aの数は 2×360＋480＝1200（全体 2×1000＝2000）なので p＝0.6、q＝0.4。p²：2pq：q²＝0.36：0.48：0.16 となり、この集団はハーディー・ワインベルグ平衡にあるといえます。</li>
</ol>
<h3>遺伝的浮動の大きさの目安</h3>
<p>このシミュレーターでは、N 個体の集団がもつ 2N 個の遺伝子を、親の世代の遺伝子プールから無作為に選び直して次の世代とします（ライト・フィッシャーのモデル）。1世代あたりの遺伝子頻度のゆれ（標準偏差）は √(pq／2N)、p＝0.5 から固定か消失が起こるまでの平均の世代数は約 4N×ln2 ≒ 2.8N 世代です。ヘテロ接合体の割合は、1世代ごとに平均して (1−1/2N) 倍に減っていきます。</p>
''' + T([["10", "20", "0.112", "約28世代", "0.08"], ["20", "40", "0.079", "約55世代", "0.28"], ["50", "100", "0.050", "約140世代", "0.61"],
          ["100", "200", "0.035", "約280世代", "0.78"], ["1000", "2000", "0.011", "約2,800世代", "0.98"]],
         ["N（個体数）", "遺伝子の数 2N", "1世代のゆれ（p＝0.5）", "固定・消失までの平均（目安）", "50世代後のヘテロ接合体（最初を1）"]) + '''
<p>中立な（有利でも不利でもない）対立遺伝子が最終的に固定する確率は、そのときの頻度 p と同じです。Aが有利なとき（このシミュレーターの「選択の強さ s」）の固定する確率の近似式は (1−e<sup>−4Nsp</sup>)／(1−e<sup>−4Ns</sup>) で、たとえば N＝20、s＝0.05、p＝0.1 では約34％です。有利な遺伝子でも、小さい集団では偶然に消失することがあります。木村資生が提唱した<b>中立説</b>では、分子レベルの変化の多くは自然選択に有利でも不利でもなく、遺伝的浮動によって集団に広まると考えます。</p>
''' + P('世代は重ならず、各世代の個体数は一定（びん首の5世代だけ減る）としています。自然選択は、Aの遺伝子が選ばれる確率を (1＋s) 倍に重みづけて表しています（解説のモデル実験で「一方の色がより多く選択されるような条件」にあたります）。突然変異・移入・移出は考えていません。乱数を「固定」にすると、同じ条件では同じ結果が再現されます。') + '''
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「高等学校学習指導要領（平成30年告示）解説 理科編 理数編」生物（1）生物の進化（2色のコインを使った遺伝子頻度のモデル実験）</li>
<li>''' + A(MEXT_KOU, "文部科学省「高等学校学習指導要領（平成30年告示）解説」") + '''</li>
<li>日本遺伝学会『遺伝単（遺伝学用語集 対訳付き）』（2017年。顕性・潜性への言いかえ）</li>
<li>G. H. Hardy（1908）Mendelian proportions in a mixed population. Science 28: 49–50 ／ W. Weinberg（1908）</li>
<li>木村資生『生物進化を考える』岩波新書（1988年）</li>
<li>高等学校「生物」の教科書「進化の仕組み」</li>
</ul>
'''

FUDOU_JS = HELP + r'''
  const NS=[5,10,20,50,100,200,500,1000,5000,10000];
  const COLS=['#e11d48','#2563eb','#16a34a','#d97706','#7c3aed','#0891b2','#db2777','#65a30d','#ea580c','#4f46e5','#0d9488','#be123c','#1d4ed8','#15803d','#b45309','#6d28d9','#0e7490','#a21caf','#4d7c0f','#c2410c'];
  const C={ink:'#0f172a',sub:'#64748b',A:'#e0483e',a:'#2f6fdb',grid:'#e2e8f0',het:'#8b5cf6'};
  let mode='drift', Nn=20, p0=0.5, G=100, s=0, Kp=10, bn=0, par='hw', seed=0, lastSeed=1, R=Math.random;
  let pops=[], gShow=0, anim=false, cur=null, last=0, dirty=true;
  let hw=null, hist=[], hwT=1, parP=0.5, parG=[0.25,0.5,0.25], gen=0;
  function mulberry(a){ return function(){ a|=0; a=a+0x6D2B79F5|0; let t=Math.imul(a^a>>>15,1|a); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; }; }
  function seedR(k){ R=seed>0?mulberry(seed*1000003+k):Math.random; }
  function gauss(){ let u=0,v=0; while(!u)u=R(); while(!v)v=R(); return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v); }
  function binom(n,p){ if(p<=0) return 0; if(p>=1) return n; if(p>0.5) return n-binom(n,1-p);
    if(n*p<25){ const lq=Math.log(1-p); let x=0, i=0; for(;;){ i+=Math.floor(Math.log(1-R())/lq)+1; if(i>n) return x; x++; } }
    const m=n*p; return clamp(Math.round(m+Math.sqrt(m*(1-p))*gauss()),0,n); }
  const bnStart=()=>Math.max(2,Math.round(G*0.2));
  function runDrift(animate){ seedR(1); pops=[];
    for(let k=0;k<Kp;k++){ const a=new Float32Array(G+1); let p=p0; a[0]=p; let ab=-1;
      for(let g=1;g<=G;g++){ const n=(bn&&g>=bnStart()&&g<bnStart()+5)?Math.min(bn,Nn):Nn; const ps=p*(1+s)/(1+p*s); p=binom(2*n,ps)/(2*n); a[g]=p; if(ab<0&&(p===0||p===1)) ab=g; }
      pops.push({a:a,ab:ab}); }
    cur=null; if(animate){ gShow=0; anim=true; } else { gShow=G; anim=false; } dirty=true; stats(); }
  function kimura(){ if(s===0) return p0; const x=4*Nn*s; return (1-Math.exp(-x*p0))/(1-Math.exp(-x)); }
  function countAt(g){ let f=0,l=0,sum=0; pops.forEach(q=>{ const v=q.a[g]; if(v>=1) f++; else if(v<=0) l++; sum+=v; }); return [f,l,pops.length-f-l,sum/pops.length]; }
  // ---- ハーディー・ワインベルグ：親の遺伝子プールから配偶子を2つずつ無作為に選んで子をつくる
  function hwReset(){ seedR(7); parP=p0; parG=par==='hw'?[p0*p0,2*p0*(1-p0),(1-p0)*(1-p0)]:[p0,0,1-p0]; gen=0; hist=[p0]; hwNext(false); }
  function hwNext(animate){ let AA=0,Aa=0,aa=0; const show=[], ns=Math.min(Nn,100);
    for(let i=0;i<Nn;i++){ const e=R()<parP, sp=R()<parP; let c; if(e&&sp){AA++;c=0;} else if(e||sp){Aa++;c=1;} else {aa++;c=2;} if(i<ns) show.push(c); }
    hw={n:Nn,AA:AA,Aa:Aa,aa:aa,p:(2*AA+Aa)/(2*Nn),show:show,pp:parP,pg:parG.slice(),gen:gen+1}; gen++; hist.push(hw.p);
    hwT=animate?0:1; dirty=true; stats(); }
  function hwAdvance(){ parP=hw.p; parG=[hw.AA/hw.n,hw.Aa/hw.n,hw.aa/hw.n]; hwNext(true); }
  const pc=v=>(v*100).toFixed(1);
  function stats(){
    if(mode==='drift'){ const c=countAt(Math.min(G,Math.round(gShow))), cg=countAt(G);
      K('sA').textContent='Aが固定した集団'; K('sB').textContent='Aが消失した集団'; K('sC').textContent='最後の世代の p の平均'; K('sD').textContent='Aがいずれ固定する確率（理論）';
      setStat('sA',cg[0]+' / '+Kp); setStat('sB',cg[1]+' / '+Kp); setStat('sC',cg[3].toFixed(2)); setStat('sD',Math.round(kimura()*100)+'%');
      setShare('【遺伝的浮動】N='+Nn+'個体の集団'+Kp+'個を'+G+'世代：Aが固定'+cg[0]+'・消失'+cg[1]+'（'+(s?'選択 s='+s:'中立')+(bn?'・びん首あり':'')+'）。小さい集団ほど偶然で遺伝子頻度が大きくゆれる｜シミュラボ'); }
    else { const h=hw, n=h.n, q=1-h.pp;
      K('sA').textContent='子の世代 AA：Aa：aa（%）'; K('sB').textContent='理論 p²：2pq：q²（%）'; K('sC').textContent='子の世代のAの頻度 p'; K('sD').textContent='世代';
      setStat('sA',pc(h.AA/n)+'：'+pc(h.Aa/n)+'：'+pc(h.aa/n)); setStat('sB',pc(h.pp*h.pp)+'：'+pc(2*h.pp*q)+'：'+pc(q*q)); setStat('sC',h.p.toFixed(3)); setStat('sD','第'+h.gen+'世代');
      ['sA','sB'].forEach(id=>$(id).style.fontSize='15px');
      setShare('【ハーディー・ワインベルグ】Aの頻度p='+h.pp.toFixed(2)+'の集団'+num(n)+'個体で自由な交配→AA '+pc(h.AA/n)+'%・Aa '+pc(h.Aa/n)+'%・aa '+pc(h.aa/n)+'%（理論 '+pc(h.pp*h.pp)+'：'+pc(2*h.pp*q)+'：'+pc(q*q)+'）｜シミュラボ'); }
    if(mode==='drift') ['sA','sB'].forEach(id=>$(id).style.fontSize=''); }

  // ---- 描画：遺伝的浮動
  const X0=64,X1=616,Y0=40,Y1=350;
  const gx=g=>X0+g/G*(X1-X0), py=p=>Y1-p*(Y1-Y0);
  function niceStep(){ const c=[1,2,5,10,20,25,50,100,200]; for(const v of c) if(G/v<=10) return v; return 250; }
  function drawDrift(){
    tx('対立遺伝子Aの頻度 p の変化',8,20,13,C.ink,'left',true);
    tx('N＝'+num(Nn)+'個体（遺伝子は2N＝'+num(2*Nn)+'個）・'+Kp+'集団・'+(s?'選択 s＝'+s:'中立（s＝0）'),632,20,12,C.sub,'right',true);
    if(bn){ const b=bnStart(); ctx.fillStyle='rgba(245,158,11,.16)'; ctx.fillRect(gx(b-1),Y0,gx(b+4)-gx(b-1),Y1-Y0); tx('びん首（'+Math.min(bn,Nn)+'個体）',(gx(b-1)+gx(b+4))/2,Y0+14,11,'#b45309','center',true); }
    for(let i=0;i<=4;i++){ const v=i/4, y=py(v); ctx.strokeStyle=i%4?C.grid:'#94a3b8'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(X0,y); ctx.lineTo(X1,y); ctx.stroke();
      tx(v===1?'1 固定':v===0?'0 消失':v.toFixed(2),X0-5,y+4,11,i%4?C.sub:C.ink,'right',!(i%4)); }
    const st=niceStep(); for(let g=0;g<=G;g+=st){ const x=gx(g); ctx.strokeStyle='rgba(15,23,42,.06)'; ctx.beginPath(); ctx.moveTo(x,Y0); ctx.lineTo(x,Y1); ctx.stroke(); tx(String(g),x,Y1+15,11,C.sub,'center'); }
    tx('世代 →',X1,Y1+29,11,C.sub,'right',true);
    ctx.setLineDash([5,4]); ctx.strokeStyle='rgba(15,23,42,.35)'; ctx.beginPath(); ctx.moveTo(X0,py(p0)); ctx.lineTo(X1,py(p0)); ctx.stroke(); ctx.setLineDash([]);
    const gs=Math.min(G,Math.floor(gShow));
    pops.forEach((q,k)=>{ ctx.strokeStyle=COLS[k%COLS.length]; ctx.globalAlpha=0.85; ctx.lineWidth=Kp>12?1.3:1.8; ctx.lineJoin='round'; ctx.beginPath();
      const end=q.ab>=0?Math.min(gs,q.ab):gs; for(let g=0;g<=end;g++){ const x=gx(g), y=py(q.a[g]); if(g) ctx.lineTo(x,y); else ctx.moveTo(x,y); } ctx.stroke();
      if(q.ab>=0&&q.ab<=gs){ ctx.globalAlpha=1; dot(gx(q.ab),py(q.a[q.ab]),3.6,COLS[k%COLS.length],'#fff',1.2); } ctx.globalAlpha=1; });
    let g0=gs, head='第'+gs+'世代（最後）';
    if(cur!==null&&cur<=gs){ g0=cur; head='第'+cur+'世代の時点'; const x=gx(cur); ctx.strokeStyle='#0f172a'; ctx.lineWidth=1.2; ctx.beginPath(); ctx.moveTo(x,Y0); ctx.lineTo(x,Y1); ctx.stroke();
      const w=tw(head,11,true)+10, bx=clamp(x-w/2,X0,X1-w); ctx.fillStyle='#0f172a'; rr(bx,Y0+2,w,18,5); ctx.fill(); tx(head,bx+5,Y0+15,11,'#fff','left',true); }
    else if(gs<G) head='第'+gs+'世代';
    const c=countAt(g0), items=[['Aが固定（p＝1）',c[0]+'集団',C.A],['Aが消失（p＝0）',c[1]+'集団',C.a],['両方残っている',c[2]+'集団','#334155'],['p の平均',c[3].toFixed(2),'#334155']];
    items.forEach((it,i)=>{ const bx=8+i*156, by=384, bw=150; ctx.fillStyle='#f8fafc'; ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; rr(bx,by,bw,48,8); ctx.fill(); ctx.stroke();
      tx(it[0],bx+bw/2,by+16,11,C.sub,'center',true); tx(it[1],bx+bw/2,by+39,19,it[2],'center',true); });
    tx(head+'のようす。グラフをタップすると、その世代の数を表示します。',8,446,11,C.sub);
    tx(s===0?'中立では、Aがいずれ固定する確率＝最初の頻度 p₀（'+Math.round(p0*100)+'%）。集団が小さいほど早く固定・消失します。':'Aが有利（s＝'+s+'）：Aがいずれ固定する確率（理論）は約'+Math.round(kimura()*100)+'%。小さい集団では有利なAでも消失することがあります。',8,462,11,'#334155',null,true);
    if(Nn>=5000&&gs>=G) tx('集団が大きいと、p はほとんど動きません（ハーディー・ワインベルグの法則の条件①）。',8,478,11,'#0e7490','left',true); }

  // ---- 描画：ハーディー・ワインベルグ
  function indiv(x,y,r,c,a){ ctx.globalAlpha=a; ctx.fillStyle=c===2?C.a:C.A; ctx.beginPath(); ctx.arc(x,y,r,Math.PI/2,Math.PI*1.5); ctx.fill();
    ctx.fillStyle=c===0?C.A:C.a; ctx.beginPath(); ctx.arc(x,y,r,-Math.PI/2,Math.PI/2); ctx.fill(); ctx.strokeStyle='rgba(15,23,42,.45)'; ctx.lineWidth=1; ctx.beginPath(); ctx.arc(x,y,r,0,6.2832); ctx.stroke(); ctx.globalAlpha=1; }
  function drawHW(){ const h=hw, n=h.n, pp=h.pp, q=1-pp;
    tx('① 親の世代の遺伝子プール（配偶子）',8,20,13,C.ink,'left',true);
    const nA=Math.round(40*pp); let sd=h.gen*97+11; const ord=[]; for(let i=0;i<40;i++) ord.push(i<nA?1:0);
    for(let i=39;i>0;i--){ sd=(sd*16807)%2147483647; const j=sd%(i+1); const t=ord[i]; ord[i]=ord[j]; ord[j]=t; }
    ord.forEach((v,i)=>{ const x=20+(i%20)*14.5, y=36+Math.floor(i/20)*15; dot(x,y,5.5,v?C.A:C.a,'rgba(15,23,42,.35)'); });
    tx('A：p＝'+pp.toFixed(3),14,82,13,C.A,'left',true); tx('a：q＝'+q.toFixed(3),140,82,13,C.a,'left',true);
    tx('親の遺伝子型 AA '+pc(h.pg[0])+'%・Aa '+pc(h.pg[1])+'%・aa '+pc(h.pg[2])+'%',14,100,11,C.sub);
    ctx.strokeStyle='#64748b'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(150,108); ctx.lineTo(150,124); ctx.stroke(); ctx.fillStyle='#64748b'; ctx.beginPath(); ctx.moveTo(144,122); ctx.lineTo(156,122); ctx.lineTo(150,130); ctx.closePath(); ctx.fill();
    tx('無作為に2つずつ組み合わせて受精',162,124,11,C.sub,'left',true);
    tx('② 子の世代（第'+h.gen+'世代・'+num(n)+'個体'+(n>100?'のうち100個体':'')+'）',8,150,13,C.ink,'left',true);
    const ns=h.show.length, k=Math.floor(hwT*ns+0.0001);
    for(let i=0;i<ns;i++){ const x=24+(i%10)*28, y=172+Math.floor(i/10)*27; indiv(x,y,11,h.show[i],i<k?1:0.08); }
    tx('AA '+num(h.AA)+'・Aa '+num(h.Aa)+'・aa '+num(h.aa)+'（Aの頻度 p＝'+h.p.toFixed(3)+'）',8,456,12,C.ink,'left',true);
    indiv(14,472,6,0,1); tx('AA',24,476,11,C.sub); indiv(56,472,6,1,1); tx('Aa',66,476,11,C.sub); indiv(98,472,6,2,1); tx('aa',108,476,11,C.sub);
    tx('左半分＝卵、右半分＝精子からの遺伝子',134,476,11,C.sub);
    // 右：棒グラフ
    const BX0=338, BX1=630; tx('③ 遺伝子型頻度：子の世代と理論',BX0,20,13,C.ink,'left',true);
    const GY0=44, GY1=208, by=v=>GY1-v*(GY1-GY0);
    for(let i=0;i<=4;i++){ const y=by(i/4); ctx.strokeStyle=i?C.grid:'#94a3b8'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(BX0+28,y); ctx.lineTo(BX1,y); ctx.stroke(); tx((i*25)+'%',BX0+24,y+4,10,C.sub,'right'); }
    const obs=[h.AA/n,h.Aa/n,h.aa/n], th=[pp*pp,2*pp*q,q*q], lab=['AA','Aa','aa'], fill=[C.A,C.het,C.a];
    for(let i=0;i<3;i++){ const cx=BX0+28+(i+0.5)*(BX1-BX0-28)/3;
      ctx.fillStyle='#cbd5e1'; ctx.fillRect(cx-36,by(h.pg[i]),16,GY1-by(h.pg[i]));
      ctx.fillStyle=fill[i]; ctx.globalAlpha=0.85; ctx.fillRect(cx-16,by(obs[i]*hwT),34,GY1-by(obs[i]*hwT)); ctx.globalAlpha=1;
      ctx.strokeStyle='#0f172a'; ctx.lineWidth=2.2; ctx.setLineDash([5,3]); ctx.beginPath(); ctx.moveTo(cx-22,by(th[i])); ctx.lineTo(cx+24,by(th[i])); ctx.stroke(); ctx.setLineDash([]);
      tx(lab[i],cx,GY1+15,13,C.ink,'center',true); tx('子 '+pc(obs[i])+'%',cx,GY1+31,11,fill[i],'center',true); tx('理論 '+pc(th[i])+'%',cx,GY1+45,11,C.ink,'center'); }
    ctx.fillStyle='#cbd5e1'; ctx.fillRect(BX0+6,272,12,10); tx('親',BX0+22,282,11,C.sub); ctx.fillStyle=C.het; ctx.fillRect(BX0+50,272,12,10); tx('子',BX0+66,282,11,C.sub);
    ctx.strokeStyle='#0f172a'; ctx.lineWidth=2; ctx.setLineDash([5,3]); ctx.beginPath(); ctx.moveTo(BX0+94,277); ctx.lineTo(BX0+112,277); ctx.stroke(); ctx.setLineDash([]); tx('理論 p²・2pq・q²',BX0+116,282,11,C.sub);
    ctx.fillStyle='#f8fafc'; ctx.strokeStyle='#e2e8f0'; rr(BX0,292,BX1-BX0,48,8); ctx.fill(); ctx.stroke();
    tx('(p＋q)² ＝ p² ＋ 2pq ＋ q² ＝ 1',BX0+(BX1-BX0)/2,312,14,C.ink,'center',true);
    tx('p＝'+pp.toFixed(3)+' → p²＝'+(pp*pp).toFixed(3)+'・2pq＝'+(2*pp*q).toFixed(3)+'・q²＝'+(q*q).toFixed(3),BX0+(BX1-BX0)/2,332,11,C.sub,'center');
    // 右下：p の世代変化
    const HX0=BX0+30, HX1=BX1-4, HY0=368, HY1=468, L=Math.max(10,hist.length-1);
    tx('④ 世代ごとの Aの頻度 p',BX0,358,12,C.ink,'left',true);
    for(let i=0;i<=2;i++){ const y=HY1-i/2*(HY1-HY0); ctx.strokeStyle=i?C.grid:'#94a3b8'; ctx.beginPath(); ctx.moveTo(HX0,y); ctx.lineTo(HX1,y); ctx.stroke(); tx((i/2).toFixed(1),HX0-4,y+4,10,C.sub,'right'); }
    ctx.setLineDash([4,3]); ctx.strokeStyle='rgba(15,23,42,.35)'; ctx.beginPath(); ctx.moveTo(HX0,HY1-p0*(HY1-HY0)); ctx.lineTo(HX1,HY1-p0*(HY1-HY0)); ctx.stroke(); ctx.setLineDash([]);
    ctx.strokeStyle=C.A; ctx.lineWidth=2; ctx.beginPath(); hist.forEach((v,i)=>{ const x=HX0+i/L*(HX1-HX0), y=HY1-v*(HY1-HY0); if(i) ctx.lineTo(x,y); else ctx.moveTo(x,y); }); ctx.stroke();
    hist.forEach((v,i)=>dot(HX0+i/L*(HX1-HX0),HY1-v*(HY1-HY0),2.6,C.A));
    tx('世代 →',HX1,HY1+13,10,C.sub,'right'); tx('0',HX0,HY1+13,10,C.sub,'center'); }

  function draw(){ ctx.fillStyle='#fff'; ctx.fillRect(0,0,W,H); if(mode==='drift') drawDrift(); else drawHW(); }
  function frame(ts){ const dt=last?Math.min(0.1,(ts-last)/1000):0; last=ts;
    if(mode==='drift'&&anim){ gShow=Math.min(G,gShow+dt*G/2.2); if(gShow>=G) anim=false; dirty=true; }
    if(mode==='hw'&&hwT<1){ hwT=Math.min(1,hwT+dt/1.1); dirty=true; }
    if(dirty){ dirty=false; draw(); } requestAnimationFrame(frame); }
  // スライダーを動かしている間は表示だけ変え、指をはなしたら（change）計算に使う値を更新する
  function labels(){ const n=NS[+$('N').value], sv=+$('s').value; $('NL').textContent=num(n)+'個体'; $('p0L').textContent=(+$('p0').value).toFixed(2); $('GL').textContent=$('G').value+'世代'; $('sL').textContent=sv===0?'0（中立）':sv.toFixed(2)+'（A有利）'; $('KL').textContent=$('K').value+'集団'; }
  function readUI(){ Nn=NS[+$('N').value]; p0=+$('p0').value; G=+$('G').value; s=+$('s').value; Kp=+$('K').value; bn=+$('bn').value; par=$('par').value; seed=+$('seed').value; labels(); }
  function setMode(m){ mode=m; const d=m==='drift'; ['G','s','K','bn'].forEach(id=>showF(id,d)); showF('par',!d);
    $('run').textContent=d?'▶ 実行':'▶ 次の世代をつくる'; $('rst').textContent=d?'⏩ 結果だけすぐ表示':'⏮ 最初の世代にもどす';
    if(!d&&Nn<100){ $('N').value=NS.indexOf(1000); readUI(); }
    if(d) runDrift(false); else hwReset(); }
  function lockText(){ $('lock').textContent=seed>0?'🔓 乱数の固定をやめる':'🔒 乱数を固定する'; }
  ['N','p0','G','s','K'].forEach(id=>{ $(id).addEventListener('input',labels); $(id).addEventListener('change',()=>{ readUI(); if(mode==='drift') runDrift(true); else hwReset(); }); });
  ['bn','par'].forEach(id=>$(id).addEventListener('change',()=>{ readUI(); if(mode==='drift') runDrift(true); else hwReset(); }));
  $('seed').addEventListener('change',()=>{ readUI(); if(seed>0) lastSeed=seed; lockText(); if(mode==='drift') runDrift(true); else hwReset(); });
  $('mode').addEventListener('change',()=>{ readUI(); setMode($('mode').value); });
  $('run').addEventListener('click',()=>{ if(mode==='drift') runDrift(true); else hwAdvance(); });
  $('rst').addEventListener('click',()=>{ if(mode==='drift'){ gShow=G; anim=false; dirty=true; stats(); } else hwReset(); });
  $('lock').addEventListener('click',()=>{ $('seed').value=String(seed>0?0:lastSeed); readUI(); lockText(); if(mode==='drift') runDrift(true); else hwReset(); });
  cv.addEventListener('pointerdown',e=>{ if(mode!=='drift') return; const p=cpos(cv,e), x=p[0]/dpr, y=p[1]/dpr;
    if(x>=X0-4&&x<=X1+4&&y>=Y0&&y<=Y1+20){ const g=clamp(Math.round((x-X0)/(X1-X0)*G),0,G); cur=(cur===g)?null:g; dirty=true; } else { cur=null; dirty=true; } });
  readUI(); lockText(); setMode('drift'); requestAnimationFrame(frame);
'''

sim(slug="iden-fudou", cat="rika", emoji="🎲", score=78,
    title="遺伝的浮動とハーディー・ワインベルグの法則のシミュレーター",
    title_tag="遺伝的浮動のシミュレーター｜集団の大きさと遺伝子頻度の変化、ハーディー・ワインベルグの法則（高校生物）",
    meta_desc="集団の大きさN・最初の遺伝子頻度p・世代数・選択の強さを変えて、最大20集団の遺伝子頻度の変化を折れ線で同時に表示。小さい集団ほど固定・消失が早い遺伝的浮動やびん首効果、p²＋2pq＋q²のハーディー・ワインベルグ平衡を1世代ずつ確かめられます。乱数の固定つき。高校「生物」進化の仕組み向け。",
    og_title="遺伝的浮動とハーディー・ワインベルグの法則のシミュレーター",
    og_desc="N＝10の集団と1000の集団で、遺伝子頻度のゆれ方はどれだけちがう？複数の集団を同時に何百世代も追跡。p²：2pq：q²を配偶子の無作為な組み合わせで確かめるモードつき。",
    card_desc="小さい集団ほど遺伝子頻度が偶然で大きくゆれ、固定・消失する。p²＋2pq＋q²の平衡も1世代ずつ確かめる。",
    lead="2色のコインのモデル実験と同じ操作を、複数の集団で何百世代もくり返します。集団の大きさを変えると、遺伝子頻度のゆれ方（遺伝的浮動）や、固定・消失までの世代数がどう変わるかがわかります。モードを切り替えると、自由な交配で遺伝子型頻度が p²：2pq：q² になること（ハーディー・ワインベルグの法則）も確かめられます。",
    model="生物 遺伝子の変化と進化の仕組み（遺伝的浮動・自然選択）",
    level="高校（生物）",
    unit="高等学校 生物（1）生物の進化 ア（ｲ）遺伝子の変化と進化の仕組み ㋒進化の仕組み",
    canvas=canvas(640, 486, light=True),
    controls=select("mode", "モード", [("drift", "遺伝的浮動（複数の集団）"), ("hw", "ハーディー・ワインベルグ（1世代ずつ）")])
             + slider("N", "集団の大きさ N", 0, 9, 2, 1)
             + slider("p0", "最初のAの頻度 p₀", 0.05, 0.95, 0.5, 0.05)
             + slider("G", "世代数", 10, 500, 100, 10)
             + slider("s", "選択の強さ s", 0, 0.2, 0, 0.01)
             + slider("K", "集団の数", 1, 20, 10, 1)
             + select("bn", "びん首効果", [("0", "なし"), ("10", "途中の5世代だけ 10個体に"), ("3", "途中の5世代だけ 3個体に")])
             + select("par", "親の世代の遺伝子型", [("hw", "平衡（p²：2pq：q²）"), ("homo", "AAとaaだけ（Aaなし）")])
             + select("seed", "乱数", [("0", "毎回ちがう")] + [(str(i), "固定 No.%d" % i) for i in range(1, 10)]),
    buttons=btn("run", "▶ 実行", True) + btn("rst", "⏩ 結果だけすぐ表示") + btn("lock", "🔒 乱数を固定する"),
    stats=stats([("sA", "Aが固定した集団", True), ("sB", "Aが消失した集団", False), ("sC", "最後の世代の p の平均", False), ("sD", "Aがいずれ固定する確率（理論）", False)]),
    legend="遺伝的浮動：線1本が1つの集団のAの頻度 p（点線＝最初の頻度、●＝固定または消失した世代、オレンジの帯＝びん首）。グラフをタップすると、その世代の時点での集団の数を表示します。ハーディー・ワインベルグ：左＝親の遺伝子プールと、配偶子を2つずつ組み合わせてできた子（赤＝A、青＝a）、右＝遺伝子型頻度（灰色＝親、色＝子、点線＝理論 p²・2pq・q²）と、世代ごとの p。「乱数」を固定すると、同じ条件では同じ結果になります。",
    article=FUDOU_ARTICLE,
    faqs=[("遺伝的浮動と自然選択のちがいは？", "自然選択は、生存や繁殖に有利な遺伝子の頻度が高まるという方向性のある変化です。遺伝的浮動は、どの配偶子が次の世代に残るかが偶然で決まることによる方向性のない変化で、有利・不利と関係なく起こります。集団が小さいほど遺伝的浮動の影響が大きくなります。"),
          ("ハーディー・ワインベルグの法則が成り立つ条件は？", "①集団が十分に大きい（遺伝的浮動が無視できる）、②自由に交配が行われる、③突然変異が起こらない、④ほかの集団との間で移入や移出がない、⑤自然選択がはたらかない、の5つです。この条件では遺伝子頻度が世代を経ても変化せず、遺伝子型頻度は p²：2pq：q² に保たれます。"),
          ("潜性ホモ接合体の割合から遺伝子頻度を求めるには？", "潜性の形質を示す個体（aa）の割合が q² なので、その平方根が q です。たとえば aa が16％なら q＝√0.16＝0.4、p＝1−q＝0.6 で、ヘテロ接合体は 2pq＝0.48（48％）です。"),
          ("なぜ小さい集団ほど遺伝子頻度が固定・消失しやすいの？", "次の世代に受けつがれる遺伝子の数（2N個）が少ないと、偶然のかたよりが割合として大きくなるからです。1世代のゆれの大きさは √(pq／2N) で、p＝0.5 のとき N＝10 では約0.11、N＝1000 では約0.011 です。固定か消失までの平均の世代数はおよそ 2.8N 世代です。"),
          ("びん首効果とは？", "病気や災害などで集団の大きさが一時的に極端に小さくなると、そのとき生き残った少数の個体の遺伝子頻度が偶然に大きくかたより、その後に集団が大きくなっても遺伝的多様性が失われたままになる現象です。チーターやキタゾウアザラシの遺伝的多様性が低いのは、その例と考えられています。"),
          ("「優性・劣性」と「顕性・潜性」は同じ意味？", "同じ意味です。「優性・劣性」は形質が優れている・劣っているという誤解を生みやすいため、日本遺伝学会が2017年に「顕性・潜性」への言いかえを提案し、今の高校の教科書でも「顕性・潜性」が使われています。")],
    rel=[("mendel-iden", "🌱", "遺伝の規則性シミュレーター"), ("shinka-sim", "🧬", "進化シミュレーター"),
         ("ketsueki-iden", "🩸", "血液型 遺伝 判定"), ("dna", "🧬", "DNA二重らせん"), ("lotka-volterra", "🐰", "キツネとウサギ 増減シミュレーター")],
    js=FUDOU_JS)
