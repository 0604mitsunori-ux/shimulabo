# -*- coding: utf-8 -*-
"""理科の授業向け：細胞分裂（中3 生命の連続性）と 水圧・浮力（中3 運動とエネルギー）
   saibou-bunretsu … 中学校 第2分野（5）生命の連続性（ア）（ｱ）生物の成長と殖え方（㋐細胞分裂と生物の成長／㋑生物の殖え方）
   suiatsu-fuyuu   … 中学校 第1分野（5）運動とエネルギー（ア）（ｱ）力のつり合いと合成・分解（㋐水中の物体に働く力）
   照合メモ（2026-10-18）
   - 水圧：100gの物体にはたらく重力＝1N（g≒10N/kg）の約束で、水の深さ1cmごとに 0.01N/cm²（＝100Pa）。1mで1N/cm²＝10kPa、10mで100kPa（大気圧101.3kPaとほぼ同じ）。
     g＝9.8 で計算すると 1m で 9.8kPa。
   - 浮力：物体は底面5cm×5cm＝25cm²の直方体。水中にある部分の高さ1cmごとに 25cm³ → 0.25N。
     中（100cm³）・300g：空気中3.00N、全部沈めると2.00N、浮力1.00N。上面2cm（0.02N/cm²×25cm²＝0.50N）と下面6cm（0.06N/cm²×25cm²＝1.50N）の差＝1.00N。
     密度が水より小さい物体（質量m g＜体積V cm³）は、水中にある部分の体積が m cm³（深さ m/25 cm）になったところで浮き、ばねばかりは0N。
   - ペットボトル：穴から出る水の速さ v＝√(2gh)（トリチェリの式・高校物理）。深さ4cm→0.89m/s、10cm→1.40m/s、16cm→1.77m/s。
   - 染色体の数（体細胞）：ヒト46・タマネギ16・エンドウ14・ソラマメ12・イネ24・キイロショウジョウバエ8・イヌ78・ネコ38。生殖細胞はその半分。
"""
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

MEXT = ('<a href="https://www.mext.go.jp/a_menu/shotou/new-cs/1384661.htm" target="_blank" rel="noopener">'
        '文部科学省「平成29・30・31年改訂学習指導要領（本文、解説）」</a>')

# ============================================================ 1 細胞分裂
SAIBOU_ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
''' + P('<b>体細胞分裂</b>では、染色体が複製されてから2つの細胞に等しく分けられるので、分裂してできた細胞の染色体の数は<b>もとの細胞と同じ</b>です。生殖細胞をつくる<b>減数分裂</b>では染色体の数が<b>半分</b>になり、<b>受精</b>によってもとの数にもどります。根の先端近くでは細胞分裂がさかんで、根元に近いほど細胞が大きくなっています。') + '''
<p>中学3年 第2分野（5）生命の連続性「生物の成長と殖え方」（細胞分裂と生物の成長／生物の殖え方）の内容です。学習指導要領の解説では、体細胞分裂の観察を行って順序性を見いだすこと、染色体が複製されることに触れること、映像などを活用して染色体の動きを見せることが示されています。このシミュレーションは、その「染色体の動き」を段階ごとに止めたり、動かしたりして見られるようにしたものです。</p>
<h2>授業での使い方</h2>
<ul>
<li><b>導入</b>：「顕微鏡で見た根の先端」に切り替え、A・B・Cの場所をタップして見くらべます。「根はどこでのびているのだろう」「細胞の大きさや形がちがうのはなぜだろう」と問いかけます。根に等間隔の印をつけて育てると、先端に近い部分の間隔が大きく広がることとも結びつけられます。</li>
<li><b>展開</b>：タマネギの根の先端の観察（下の手順）の前に「体細胞分裂」の①〜⑦を再生し、どんな形の細胞を探せばよいかを確かめます。観察のあとは、スケッチした細胞が①〜⑦のどれに当たるかを話し合い、分裂の順番に並べます。顕微鏡の図の細胞をタップすると、その細胞の段階が表示されます。</li>
<li><b>まとめ</b>：「減数分裂と受精」に切り替え、染色体の数が「4本 → 2本 → 受精で4本」と変わることを体細胞分裂（4本 → 4本）とくらべます。有性生殖では子が両親から半分ずつ染色体を受けつぐこと、次の「遺伝の規則性と遺伝子」につながることを確かめます。</li>
</ul>
<p>生徒への問いの例：</p>
<ol>
<li>体細胞分裂の前に、染色体が複製されて2倍になっておくのはなぜだろう。</li>
<li>タマネギの根の先端で、分裂している細胞が多いのはどのあたりだろう。根元に近いところとくらべて、細胞の大きさはどうちがうだろう。</li>
<li>減数分裂で染色体の数が半分にならなかったら、受精卵の染色体の数は、代を重ねるごとにどうなってしまうだろう。</li>
</ol>
<h2>しくみ・解説</h2>
<h3>用語の意味</h3>
<ul>
<li><b>細胞分裂</b>とは、1つの細胞が2つの細胞に分かれることです。</li>
<li><b>体細胞分裂</b>とは、体をつくる細胞（体細胞）が数を増やすときの細胞分裂で、分裂後の細胞の染色体の数はもとの細胞と同じです。</li>
<li><b>染色体</b>とは、細胞分裂のときに核の中に見えるひものようなもので、遺伝子をふくみます。生物の種類によって数が決まっています。</li>
<li><b>減数分裂</b>とは、生殖細胞（卵・精子、植物では卵細胞・精細胞）がつくられるときの特別な細胞分裂で、染色体の数がもとの細胞の半分になります。</li>
<li><b>受精</b>とは、卵（卵細胞）の核と精子（精細胞）の核が合体することで、受精卵の染色体の数は親の体細胞と同じになります。</li>
<li><b>成長点</b>とは、根やくきの先端近くにある、細胞分裂がさかんに行われている部分です。根の成長点は、先端をおおう根冠に守られています。</li>
</ul>
<h3>体細胞分裂の順序（中学の言い方と高校の言い方）</h3>
''' + T([["①", "分裂前の細胞", "間期", "核がある。染色体は細い糸のように広がっていて見えにくい。分裂の前に複製されて2本ずつになる"],
          ["②", "核の中に染色体が見えるようになる", "前期", "核の形が見えなくなり、染色体が太く短くなって見える（複製された2本がくっついた形）"],
          ["③", "染色体が細胞の中央に並ぶ", "中期", "染色体が細胞の中央（赤道面）に並ぶ"],
          ["④", "染色体が2つに分かれて両端へ移動する", "後期", "複製されていた染色体が分かれ、同じ数ずつ両端（両極）へ移動する"],
          ["⑤", "中央に仕切りができ始める", "終期", "両端に新しい核ができ始め、植物の細胞では中央に仕切り（細胞板）ができる"],
          ["⑥", "2つの細胞に分かれる", "（間期にもどる）", "もとの細胞と同じ数の染色体をもつ2つの細胞ができる"],
          ["⑦", "それぞれの細胞が大きくなる", "間期", "分裂でできた細胞が、もとの大きさまで大きくなる"]],
         ["", "中学の教科書の言い方", "高校（生物基礎）の言い方", "染色体・細胞のようす"]) + '''
<p>動物の細胞では、仕切りができる代わりに、細胞のまん中がくびれて2つに分かれます。前期・中期・後期・終期という呼び方は、高校の「生物基礎」で学びます。</p>
<h3>染色体の数の早見表</h3>
<p>染色体の数は生物の種類ごとに決まっています。体細胞分裂では数が変わらず、減数分裂でできる生殖細胞では半分になり、受精でもとにもどります。</p>
''' + T([["ヒト", "46本", "23本", "23本＋23本＝46本"], ["タマネギ", "16本", "8本", "8本＋8本＝16本"], ["エンドウ", "14本", "7本", "7本＋7本＝14本"],
          ["ソラマメ", "12本", "6本", "6本＋6本＝12本"], ["イネ", "24本", "12本", "12本＋12本＝24本"], ["キイロショウジョウバエ", "8本", "4本", "4本＋4本＝8本"],
          ["イヌ", "78本", "39本", "39本＋39本＝78本"], ["ネコ", "38本", "19本", "19本＋19本＝38本"], ["このシミュレーションの生物", "4本", "2本", "2本＋2本＝4本"]],
         ["生物", "体細胞の染色体", "生殖細胞の染色体（減数分裂）", "受精卵の染色体"]) + '''
<h3>体細胞分裂と減数分裂のちがい</h3>
''' + T([["何のための分裂か", "体の細胞をふやす（成長・無性生殖）", "生殖細胞（卵・精子）をつくる"],
          ["どこで起こるか", "根やくきの先端（成長点）、体のいろいろな部分", "動物は卵巣・精巣、植物はめしべの胚珠・おしべのやく"],
          ["分裂の回数", "1回", "続けて2回"],
          ["できる細胞の数", "2つ", "4つ"],
          ["染色体の数（このシミュレーション）", "4本 → 4本（変わらない）", "4本 → 2本（半分）→ 受精で4本"]],
         ["", "体細胞分裂", "減数分裂"]) + '''
<p>減数分裂では、同じ形・大きさの染色体どうしが対になって並び、対の染色体が1本ずつ別々の細胞に入ります。そのため、生殖細胞は対の染色体を1本ずつもちます。このシミュレーションの赤と青は、その生物が自分の両親から1本ずつ受けついだ染色体を表し、緑は受精の相手（もう一方の親）から来た染色体を表しています。中学では、減数分裂のくわしい過程（2回の分裂）までは扱わず、「染色体の数が半分になる」ことを学びます。</p>
<h3>タマネギの根の先端の観察の手順</h3>
''' + T([["1", "タマネギの種子（または鱗茎の底）を水につけて根を出させ、根の先端を約5mm切り取る", "細胞分裂がさかんな先端付近を観察するため"],
          ["2", "うすい塩酸に入れて、約60℃の湯で数分あたためる（時間は教科書の指示に従う）", "細胞どうしの結合を切り、細胞を1つ1つ離れやすくするため"],
          ["3", "根を水でよくすすぎ、スライドガラスにのせて、柄つき針で軽くほぐす", "塩酸を取りのぞき、染色液がしみこみやすくするため"],
          ["4", "酢酸オルセイン液（または酢酸カーミン液）を1滴落とし、数分おく", "核や染色体を赤紫色（酢酸カーミンは赤色）に染めて見やすくするため"],
          ["5", "カバーガラスをかけ、ろ紙をのせて、指の腹で真上から静かに押しつぶす（ずらさない）", "細胞の重なりをなくし、1層に広げるため"],
          ["6", "顕微鏡の低倍率で先端付近を探してから、高倍率（400〜600倍）で観察する", "分裂中の細胞を見つけ、染色体のようすを観察するため"]],
         ["", "操作", "目的"]) + N('塩酸は皮ふや目につかないように保護めがねをかけ、ついたときはすぐに大量の水で洗います。酢酸オルセイン液は衣服につくと落ちにくいので注意します。') + '''
<h3>根はどこでのびるのか（成長点）</h3>
<p>根の先端付近（A）には小さな細胞がすき間なく並び、分裂の途中の細胞が多く見られます。少し上（B）や根元に近いところ（C）では、分裂している細胞はほとんどなく、細胞が縦に長く大きくなっています。生物の成長は、<b>細胞分裂で細胞の数が増える</b>ことと、<b>分裂でできた細胞が大きくなる</b>ことによって起こります。</p>
<h3>発展：細胞周期（高校 生物基礎）</h3>
<p>分裂を終えた細胞が次の分裂を終えるまでの1回りを<b>細胞周期</b>といいます。細胞周期は、分裂の準備をする<b>間期</b>と、分裂が進む<b>分裂期</b>（前期・中期・後期・終期）に分けられ、DNA（染色体）の複製は間期に行われます。細胞周期の大部分は間期なので、根の先端を見ても、分裂期の細胞は一部です。高校では、それぞれの時期の細胞の数の割合から、各時期にかかる時間の長さを推定する実習も行います。</p>
''' + N('<b>このシミュレーションで単純にしていること</b>：染色体は見やすいように4本（2対）にし、色を変えて描いています（実際の染色体に色はなく、染色液で赤紫色に染めて観察します）。顕微鏡の図は模式図で、細胞の大きさや分裂中の細胞の割合はおよその目安です。減数分裂でできる4つの細胞は、ここでは卵や精子の区別をせずに描いています（動物の卵をつくる減数分裂では、実際には大きな卵が1つできます）。') + '''
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「中学校学習指導要領（平成29年告示）」理科 第2分野（5）生命の連続性（ア）（ｱ）生物の成長と殖え方／「中学校学習指導要領（平成29年告示）解説 理科編」（体細胞分裂の観察、染色体の複製、減数分裂）</li>
<li>''' + MEXT + '''</li>
<li>文部科学省「高等学校学習指導要領（平成30年告示）解説 理科編」生物基礎（細胞周期とDNAの複製）</li>
<li>中学校理科の教科書（第3学年）「生物の成長と殖え方」（タマネギの根の体細胞分裂の観察）</li>
</ul>
'''

SAIBOU_FAQS = [
    ("体細胞分裂とは何ですか？", "体をつくる細胞（体細胞）が数を増やすときの細胞分裂です。分裂の前に染色体が複製され、2つの細胞に等しく分けられるので、分裂後の細胞の染色体の数はもとの細胞と同じです。"),
    ("体細胞分裂はどんな順番で進みますか？", "①分裂前の細胞（染色体が複製される）→②核の中に染色体が見えるようになる→③染色体が細胞の中央に並ぶ→④染色体が2つに分かれて両端へ移動する→⑤中央に仕切りができ始める→⑥2つの細胞になる、の順です。高校では②〜⑤を前期・中期・後期・終期と呼びます。"),
    ("体細胞分裂と減数分裂のちがいは何ですか？", "体細胞分裂は体の細胞をふやす分裂で、染色体の数は変わりません。減数分裂は卵や精子などの生殖細胞をつくる分裂で、染色体の数が半分になります。受精すると、受精卵の染色体の数はもとにもどります（ヒトでは23本＋23本＝46本）。"),
    ("タマネギの根の先端を観察するのはなぜですか？", "根の先端近くには細胞分裂がさかんな成長点があり、分裂の途中の細胞がたくさん見つかるからです。また、植物の細胞は染色体の数が少なく見やすいものが多く、タマネギの根は手に入れやすく、簡単に育てられます。"),
    ("塩酸と酢酸オルセイン液は何のために使うのですか？", "あたためたうすい塩酸は、細胞どうしの結合を切って細胞を離れやすくし、押しつぶしたときに細胞が重ならないようにするために使います。酢酸オルセイン液は、核や染色体を赤紫色に染めて見やすくするために使います。"),
    ("生物はどのようにして成長するのですか？", "細胞分裂で細胞の数が増えることと、分裂でできた細胞の1つ1つが大きくなることによって成長します。タマネギの根では、先端付近で分裂した細胞が、根元に向かうにつれて縦に長くなっていきます。"),
]

SAIBOU_JS = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const CX=320, CY=216, CW=300, CH=184, RED='#e11d48', BLUE='#2563eb', GREEN='#16a34a';
  const CHR=[{len:36,col:RED},{len:36,col:BLUE},{len:22,col:RED},{len:22,col:BLUE}];
  const SC=[[-26,-18,0.6],[22,-22,-0.9],[-18,24,1.9],[26,16,0.3]], YY=[-58,20,-20,58];
  const PAIR=[[-11,-30],[11,-30],[11,30],[-11,30]], SIDE=[-1,1,1,-1];
  const NUMS=['①','②','③','④','⑤','⑥','⑦'];
  const TAI=[
    {n:'分裂前の細胞', s:'①分裂前', hi:'間期', d:'核があり、染色体は細い糸のように広がっていて見えにくい。分裂の前に、染色体は複製されて2本ずつになる。', c:'1つの細胞に染色体4本', k:1},
    {n:'核の中に染色体が見えるようになる', s:'②染色体が見える', hi:'前期', d:'核の形が見えなくなり、染色体が太く短くなって見えるようになる（複製された2本がくっついた形）。', c:'染色体4本（どれも複製されて2本がくっついている）', k:1},
    {n:'染色体が細胞の中央に並ぶ', s:'③中央に並ぶ', hi:'中期', d:'染色体が細胞の中央に並ぶ。分裂の途中の細胞の中で、いちばん見つけやすい形。', c:'4本の染色体が中央に並ぶ', k:1},
    {n:'染色体が分かれて両端へ移動する', s:'④両端へ分かれる', hi:'後期', d:'複製されていた染色体が2つに分かれ、細胞の両端へ移動する。両端に同じ4本ずつが分けられる。', c:'両端に4本ずつ分かれる', k:1},
    {n:'中央に仕切りができ始める', s:'⑤仕切りができる', hi:'終期', d:'両端に集まった染色体のまわりに新しい核ができ始め、細胞の中央に仕切りができ始める。', c:'両端に4本ずつ', k:1},
    {n:'2つの細胞に分かれる', s:'⑥2つの細胞に', hi:'間期にもどる', d:'仕切りが完成し、もとの細胞と同じ染色体（4本）をもつ2つの細胞になる。', c:'2つの細胞に4本ずつ（もとと同じ）', k:2},
    {n:'それぞれの細胞が大きくなる', s:'⑦大きくなる', hi:'間期', d:'分裂でできた細胞が、それぞれ大きくなる。細胞の数が増え、1つ1つが大きくなることで、根がのびる（成長）。', c:'2つの細胞に4本ずつ', k:2}];
  const GEN=[
    {n:'生殖細胞をつくる細胞', s:'①もとの細胞', d:'染色体は4本。形と大きさが同じものが2本ずつ（2対）ある。赤と青は、この生物が両親から1本ずつ受けついだもの。', c:'1つの細胞に染色体4本（2対）', ch:4, k:1},
    {n:'染色体が複製され、対になって並ぶ', s:'②対になって並ぶ', d:'複製された染色体が、同じ形・大きさのものどうしで対になって、中央に並ぶ。', c:'4本が2本ずつ対になって並ぶ', ch:4, k:1},
    {n:'対の染色体が1本ずつ両端へ分かれる', s:'③対が分かれる', d:'対になっていた染色体が1本ずつ両端へ分かれる（体細胞分裂とのちがい）。', c:'両端に2本ずつ（対が分かれる）', ch:4, k:1},
    {n:'2つの細胞に分かれる', s:'④2つの細胞に', d:'それぞれの細胞の染色体は2本。もとの細胞の半分になった。', c:'2つの細胞に2本ずつ（半分）', ch:2, k:2},
    {n:'もう一度分かれて、生殖細胞が4つできる', s:'⑤生殖細胞が4つ', d:'続けてもう1回分裂し、染色体の数がもとの半分（2本）の生殖細胞が4つできる。', c:'4つの生殖細胞に2本ずつ（半分）', ch:2, k:4},
    {n:'受精して受精卵になる', s:'⑥受精卵', d:'卵（2本）と、もう一方の親の精子（2本）が受精すると、受精卵の染色体は4本にもどる。', c:'受精卵：2本＋2本＝4本（もとにもどる）', ch:4, k:1}];
  const LOCS=[{s:'A 先端付近', name:'A：根の先端付近（成長点）', ch:26, rate:0.22, y0:350, y1:388, len:'1倍'},
              {s:'B 少し上', name:'B：先端から少し上', ch:56, rate:0.05, y0:250, y1:300, len:'約2倍'},
              {s:'C 根元に近い', name:'C：根元に近いところ', ch:104, rate:0, y0:92, y1:152, len:'約4倍'}];
  const KEN_ST=['分裂していない細胞（核が1つ見える）','核の中に染色体が見えるようになっている（高校：前期）','染色体が中央に並んでいる（高校：中期）','染色体が分かれて両端へ移動している（高校：後期）','中央に仕切りができ始めている（高校：終期）'];
  const FX=440, FY=218, FR=154, CWm=30;
  let mode='tai', p=2, playing=false, hold=0, tgt=null, loc=0, sel=-1, last=0, statKey='';
  function prng(seed){ let a=seed>>>0; return function(){ a=(a+0x6D2B79F5)>>>0; let t=a; t=Math.imul(t^(t>>>15),t|1); t^=t+Math.imul(t^(t>>>7),t|61); return ((t^(t>>>14))>>>0)/4294967296; }; }
  const THR=[];
  function mkThr(){ const r=prng(7); for(let i=0;i<4;i++){ const pts=[]; let a=r()*6.28, rad=0.3+0.35*r(); for(let j=0;j<9;j++){ a+=0.5+r()*0.9; rad=Math.min(0.78,Math.max(0.15,rad+(r()-0.5)*0.35)); pts.push([Math.cos(a)*rad,Math.sin(a)*rad]); } THR.push(pts); } }
  mkThr();
  function genCells(li){ const L=LOCS[li], R=prng(11+li*97), cells=[];
    for(let c=-6;c<=6;c++){ const x0=FX+c*CWm-CWm/2; let y=FY-FR-L.ch*R();
      while(y<FY+FR){ const h=L.ch*(0.85+0.3*R()), cx=x0+CWm/2, cy=y+h/2, dd=Math.hypot(cx-FX,cy-FY);
        let st=0; if(R()<L.rate){ const q=R(); st=q<0.45?1:(q<0.65?2:(q<0.8?3:4)); }
        if(dd<FR+20) cells.push({x:x0,y:y,w:CWm,h:h,st:st,seed:Math.floor(R()*1e6),inn:dd<FR-4}); y+=h; } }
    if(li===1 && !cells.some(function(c){ return c.inn&&c.st>0; })){ const c=cells.filter(function(c){ return c.inn; })[3]; if(c) c.st=1; }
    return cells; }
  const CELLS=[genCells(0),genCells(1),genCells(2)];
  function list(){ return mode==='gen'?GEN:TAI; }
  function maxP(){ return list().length-1; }
  function smooth(f){ f=clamp(f,0,1); return f*f*(3-2*f); }
  function lerp(a,b,t){ return a+(b-a)*t; }
  function rr(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
  function wrap(t,x,y,maxW,lh,maxL){ let line='', n=0; for(const ch of t){ const tt=line+ch; if(ctx.measureText(tt).width>maxW && line){ ctx.fillText(line,x,y+n*lh); n++; line=ch; if(maxL&&n>=maxL) return n; } else line=tt; } if(line){ ctx.fillText(line,x,y+n*lh); n++; } return n; }
  function fit(t,x,y,maxW,size,weight){ let s=size; ctx.font=weight+' '+s+'px sans-serif'; while(ctx.measureText(t).width>maxW && s>9){ s--; ctx.font=weight+' '+s+'px sans-serif'; } ctx.fillText(t,x,y); }
  function chromatid(x,y,len,rot,bend,col,a,w){ if(a<=0.01) return; const l=len/2, sx=Math.sin(bend)*l, cy=Math.cos(bend)*l;
    ctx.save(); ctx.globalAlpha*=a; ctx.translate(x,y); ctx.rotate(rot); ctx.strokeStyle=col; ctx.lineWidth=w; ctx.lineCap='round'; ctx.lineJoin='round';
    ctx.beginPath(); ctx.moveTo(sx,-cy); ctx.lineTo(0,0); ctx.lineTo(sx,cy); ctx.stroke(); ctx.restore(); }
  function xchrom(x,y,len,rot,col,a,w){ const g=3.4, c=Math.cos(rot), s=Math.sin(rot);
    chromatid(x-g*c,y-g*s,len,rot,-0.35,col,a,w); chromatid(x+g*c,y+g*s,len,rot,0.35,col,a,w);
    if(a>0.3){ ctx.save(); ctx.globalAlpha*=a; ctx.fillStyle='#334155'; ctx.beginPath(); ctx.arc(x,y,2.4,0,6.283); ctx.fill(); ctx.restore(); } }
  function threads(x,y,r,a){ if(a<=0.01) return; ctx.save(); ctx.globalAlpha*=a*0.8; ctx.lineWidth=1.6; ctx.lineCap='round';
    THR.forEach(function(pts,i){ ctx.strokeStyle=CHR[i].col; ctx.beginPath(); ctx.moveTo(x+pts[0][0]*r,y+pts[0][1]*r);
      for(let j=1;j<pts.length-1;j++){ const mx=(pts[j][0]+pts[j+1][0])/2, my=(pts[j][1]+pts[j+1][1])/2; ctx.quadraticCurveTo(x+pts[j][0]*r,y+pts[j][1]*r,x+mx*r,y+my*r); } ctx.stroke(); });
    ctx.restore(); }
  function nucleus(x,y,r,a){ if(a<=0.01) return; ctx.save(); ctx.globalAlpha*=a; ctx.fillStyle='rgba(203,213,225,.35)'; ctx.strokeStyle='#64748b'; ctx.lineWidth=1.6;
    ctx.beginPath(); ctx.arc(x,y,r,0,6.283); ctx.fill(); ctx.stroke(); ctx.restore(); }
  function cellBox(x0,x1,y0,y1){ ctx.fillStyle='#f7fee7'; ctx.strokeStyle='#65a30d'; ctx.lineWidth=3; rr(x0,y0,x1-x0,y1-y0,14); ctx.fill(); ctx.stroke(); }
  function vplate(x,y,hl){ if(hl<=0.5) return; ctx.strokeStyle='#65a30d'; ctx.lineWidth=3; ctx.lineCap='round'; ctx.beginPath(); ctx.moveTo(x,y-hl); ctx.lineTo(x,y+hl); ctx.stroke(); }
  function hplate(x,y,hl){ if(hl<=0.5) return; ctx.strokeStyle='#65a30d'; ctx.lineWidth=3; ctx.lineCap='round'; ctx.beginPath(); ctx.moveTo(x-hl,y); ctx.lineTo(x+hl,y); ctx.stroke(); }
  function badge(t,x,y,col){ ctx.font='bold 13px sans-serif'; const w=ctx.measureText(t).width+14; ctx.fillStyle='rgba(255,255,255,.92)'; rr(x-w/2,y-11,w,20,10); ctx.fill(); ctx.strokeStyle=col||'#0e7490'; ctx.lineWidth=1.2; ctx.stroke(); ctx.fillStyle=col||'#0e7490'; ctx.textAlign='center'; ctx.fillText(t,x,y+4); }
  // ---------- 体細胞分裂 ----------
  function drawTai(p){ const k=Math.min(5,Math.floor(p)), e=smooth(p-k), T=CY-CH/2, B=CY+CH/2;
    if(p<5){ cellBox(CX-CW/2,CX+CW/2,T,B); vplate(CX,CY,k<3?0:(k===3?e*0.6:lerp(0.6,1,e))*CH/2); }
    else { const wd=lerp(CW/2,CW*0.92,e); cellBox(CX-wd,CX,T,B); cellBox(CX,CX+wd,T,B); }
    if(k===0){ nucleus(CX,CY,62,1-e); threads(CX,CY,62,1-e); }
    if(k===3){ nucleus(CX-75,CY,44,e*0.7); nucleus(CX+75,CY,44,e*0.7); }
    if(k===4){ nucleus(CX-75,CY,44,lerp(0.7,1,e)); nucleus(CX+75,CY,44,lerp(0.7,1,e)); threads(CX-75,CY,44,e); threads(CX+75,CY,44,e); }
    if(k===5){ const wd=lerp(CW/2,CW*0.92,e), r=lerp(44,52,e); nucleus(CX-wd/2,CY,r,1); nucleus(CX+wd/2,CY,r,1); threads(CX-wd/2,CY,r,1); threads(CX+wd/2,CY,r,1); }
    for(let i=0;i<4;i++){ const c=CHR[i];
      if(k===0) xchrom(CX+SC[i][0],CY+SC[i][1],c.len*(1.6-0.6*e),SC[i][2],c.col,e,lerp(1.5,6,e));
      else if(k===1) xchrom(lerp(CX+SC[i][0],CX,e),lerp(CY+SC[i][1],CY+YY[i],e),c.len,lerp(SC[i][2],0,e),c.col,1,6);
      else if(k<=4){ for(let s=0;s<2;s++){ const dir=s?1:-1, rot=s?Math.PI:0; let x,y,b,a=1;
          if(k===2){ x=lerp(CX+dir*3.4,CX+dir*100,e); y=CY+YY[i]*lerp(1,0.75,e); b=lerp(-0.35,0.9,e); if(e<0.08){ ctx.fillStyle='#334155'; ctx.beginPath(); ctx.arc(CX,y,2.4,0,6.283); ctx.fill(); } }
          else if(k===3){ x=lerp(CX+dir*100,CX+dir*75,e); y=CY+YY[i]*lerp(0.75,0.45,e); b=lerp(0.9,0.5,e); }
          else { x=CX+dir*75; y=CY+YY[i]*0.45; b=0.5; a=1-e; }
          chromatid(x,y,c.len,rot,b,c.col,a,6); } } }
    if(p>=2.5 && p<5){ badge('4本',CX-75,T+18); badge('4本',CX+75,T+18); }
    else if(p>=5){ const wd=lerp(CW/2,CW*0.92,e); badge('4本',CX-wd/2,T+18); badge('4本',CX+wd/2,T+18); }
    else badge('4本',CX-CW/2+34,T+20); }
  // ---------- 減数分裂と受精 ----------
  function drawGen(p){ const k=Math.min(4,Math.floor(p)), e=smooth(p-k), T=CY-CH/2, B=CY+CH/2, u=clamp(p-4,0,1);
    const aCells=k<4?1:1-smooth(u/0.35);
    if(aCells>0.01){ ctx.save(); ctx.globalAlpha=aCells;
      cellBox(CX-CW/2,CX+CW/2,T,B);
      vplate(CX,CY,(k<2?0:(k===2?e:1))*CH/2);
      const hp=k<3?0:(k===3?e:1); hplate(CX-75,CY,hp*75); hplate(CX+75,CY,hp*75);
      if(k===0){ nucleus(CX,CY,62,1-e); threads(CX,CY,62,1-e); }
      for(let i=0;i<4;i++){ const c=CHR[i], sd=SIDE[i], yq=i<2?-16:16;
        if(k===0) xchrom(lerp(CX+SC[i][0],CX+PAIR[i][0],e),lerp(CY+SC[i][1],CY+PAIR[i][1],e),c.len*(1.6-0.6*e),lerp(SC[i][2],0,e),c.col,e,lerp(1.5,6,e));
        else if(k===1) xchrom(lerp(CX+PAIR[i][0],CX+sd*100,e),CY+PAIR[i][1]*lerp(1,0.8,e),c.len,0,c.col,1,6);
        else if(k===2) xchrom(lerp(CX+sd*100,CX+sd*75,e),lerp(CY+PAIR[i][1]*0.8,CY+yq,e),c.len,lerp(0,Math.PI/2,e),c.col,1,6);
        else { for(let s=0;s<2;s++){ const dir=s?1:-1, x=CX+sd*75, y0=CY+yq+dir*3.6, y1=CY+dir*CH/4+(i<2?-8:8), ee=k===3?e:1;
            chromatid(x,lerp(y0,y1,ee),c.len,s?-Math.PI/2:Math.PI/2,k===3?0.7*Math.sin(Math.PI*e):0,c.col,1,6); } } }
      if(p>=2.5 && p<3.5){ badge('2本',CX-75,T+18); badge('2本',CX+75,T+18); }
      else if(p>=3.5){ [-1,1].forEach(function(sd){ [-1,1].forEach(function(sv){ badge('2本',CX+sd*75+sd*48,CY+sv*CH/4,'#b45309'); }); }); }
      else badge('4本',CX-CW/2+34,T+20);
      ctx.restore(); }
    if(k===4) drawFert(u); }
  function drawFert(u){ const a1=smooth(u/0.35), mv=smooth((u-0.35)/0.45), e3=smooth((u-0.8)/0.2), EX=CX-50, sx=lerp(CX+190,EX+78,mv);
    if(a1<=0.01) return; ctx.save(); ctx.globalAlpha=a1;
    ctx.fillStyle='#fff7ed'; ctx.strokeStyle='#f59e0b'; ctx.lineWidth=3; ctx.beginPath(); ctx.arc(EX,CY,70,0,6.283); ctx.fill(); ctx.stroke();
    nucleus(EX,CY,lerp(30,42,e3),1);
    chromatid(lerp(EX-8,EX-18,e3),CY,36,0,0,RED,1,6); chromatid(lerp(EX+8,EX+6,e3),CY,22,0,0,BLUE,1,6);
    ctx.save(); ctx.globalAlpha*=1-e3;
    ctx.strokeStyle='#4d7c0f'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(sx+16,CY); for(let i=0;i<=24;i++){ ctx.lineTo(sx+16+i*3,CY+Math.sin(i*0.8+u*30)*4); } ctx.stroke();
    ctx.fillStyle='#ecfccb'; ctx.beginPath(); ctx.ellipse(sx,CY,17,12,0,0,6.283); ctx.fill(); ctx.stroke();
    ctx.restore();
    chromatid(lerp(sx-5,EX-6,e3),CY,lerp(20,36,e3),0,0,GREEN,1,lerp(4,6,e3)); chromatid(lerp(sx+5,EX+18,e3),CY,lerp(13,22,e3),0,0,GREEN,1,lerp(4,6,e3));
    ctx.textAlign='center';
    if(e3<0.99){ ctx.save(); ctx.globalAlpha*=1-e3; ctx.fillStyle='#b45309'; ctx.font='bold 14px sans-serif'; ctx.fillText('卵（卵細胞）：2本',EX,CY-80);
      ctx.fillStyle='#3f6212'; ctx.fillText('精子（精細胞）：2本',sx+30,CY+36); ctx.font='12px sans-serif'; ctx.fillText('もう一方の親から',sx+30,CY+52); ctx.restore(); }
    if(e3>0.01){ ctx.save(); ctx.globalAlpha*=e3; badge('受精卵',EX,CY-84,'#0e7490');
      ctx.fillStyle='#334155'; ctx.font='13px sans-serif'; ctx.textAlign='left'; wrap('同じ形・大きさの染色体が、また2本ずつ（2対）そろった。半分は卵から、半分は精子から受けついでいる。',EX+96,CY-58,200,19,4); ctx.restore(); }
    ctx.restore(); }
  // ---------- 顕微鏡（根の先端） ----------
  function mcell(c,hl){ ctx.strokeStyle='#d9a7c7'; ctx.lineWidth=1.4; ctx.strokeRect(c.x,c.y,c.w,c.h); const x=c.x+c.w/2, y=c.y+c.h/2, R=prng(c.seed), dk='#701a75';
    if(c.st===0){ ctx.fillStyle='rgba(157,23,77,.5)'; ctx.beginPath(); ctx.ellipse(x,y,7,7.5,0,0,6.283); ctx.fill(); ctx.fillStyle='rgba(88,10,45,.75)'; ctx.beginPath(); ctx.arc(x+1.5,y-1,1.8,0,6.283); ctx.fill(); }
    else { ctx.strokeStyle=dk; ctx.lineWidth=2.2; ctx.lineCap='round';
      if(c.st===1){ ctx.save(); ctx.strokeStyle='rgba(157,23,77,.35)'; ctx.lineWidth=1; ctx.beginPath(); ctx.arc(x,y,9,0,6.283); ctx.stroke(); ctx.restore();
        for(let i=0;i<7;i++){ const a=R()*6.283, r=R()*5.5, b=R()*6.283, l=2.5+R()*1.5; const px=x+Math.cos(a)*r, py=y+Math.sin(a)*r; ctx.beginPath(); ctx.moveTo(px-Math.cos(b)*l,py-Math.sin(b)*l); ctx.lineTo(px+Math.cos(b)*l,py+Math.sin(b)*l); ctx.stroke(); } }
      else if(c.st===2){ for(let i=0;i<7;i++){ const px=x-10+i*3.3, py=y+(R()-0.5)*2; ctx.beginPath(); ctx.moveTo(px,py-3); ctx.lineTo(px+(R()-0.5)*2,py+3); ctx.stroke(); } }
      else if(c.st===3){ [-1,1].forEach(function(sd){ const yy=y+sd*c.h*0.24; for(let i=0;i<6;i++){ const px=x-8+i*3.2; ctx.beginPath(); ctx.moveTo(px-1.5,yy-sd*2.5); ctx.lineTo(px,yy+sd*1.5); ctx.lineTo(px+1.5,yy-sd*2.5); ctx.stroke(); } }); }
      else { ctx.fillStyle='rgba(112,26,117,.8)'; [-1,1].forEach(function(sd){ ctx.beginPath(); ctx.ellipse(x,y+sd*c.h*0.3,9,3.5,0,0,6.283); ctx.fill(); });
        ctx.save(); ctx.strokeStyle='#a21caf'; ctx.lineWidth=1.5; ctx.setLineDash([3,2]); ctx.beginPath(); ctx.moveTo(x-12,y); ctx.lineTo(x+12,y); ctx.stroke(); ctx.restore(); } }
    if(hl){ ctx.strokeStyle='#0e7490'; ctx.lineWidth=3; ctx.strokeRect(c.x+1.5,c.y+1.5,c.w-3,c.h-3); } }
  function counts(){ const cs=CELLS[loc]; let tot=0, dv=0; cs.forEach(function(c){ if(c.inn){ tot++; if(c.st>0) dv++; } }); return [dv,tot]; }
  function drawKen(){ const RX=96, L=LOCS[loc];
    ctx.textAlign='left'; ctx.fillStyle='#0f172a'; ctx.font='bold 18px sans-serif'; ctx.fillText('顕微鏡で見たタマネギの根の先端（模式図）',14,26);
    ctx.font='13px sans-serif'; ctx.fillStyle=sel>=0?'#0e7490':'#475569';
    const sc=sel>=0?CELLS[loc][sel]:null; fit(sc?('タップした細胞：'+KEN_ST[sc.st]):'左の根のA・B・Cをタップして場所を選ぶ。右の円の中の細胞をタップすると、その細胞の段階がわかります。',14,48,W-28,13,sc?'bold':'');
    // 根
    ctx.save(); ctx.beginPath(); ctx.moveTo(RX-32,64); ctx.lineTo(RX-32,372); ctx.quadraticCurveTo(RX-30,420,RX,424); ctx.quadraticCurveTo(RX+30,420,RX+32,372); ctx.lineTo(RX+32,64); ctx.closePath();
    ctx.fillStyle='#fefce8'; ctx.fill(); ctx.clip();
    ctx.strokeStyle='rgba(161,98,7,.35)'; ctx.lineWidth=1; for(let k=1;k<5;k++){ const x=RX-32+64*k/5; ctx.beginPath(); ctx.moveTo(x,64); ctx.lineTo(x,396); ctx.stroke(); }
    let y=394; while(y>64){ ctx.beginPath(); ctx.moveTo(RX-32,y); ctx.lineTo(RX+32,y); ctx.stroke(); y-=5+(394-y)*0.075; }
    ctx.fillStyle='#fde68a'; ctx.beginPath(); ctx.moveTo(RX-34,398); ctx.quadraticCurveTo(RX,388,RX+34,398); ctx.lineTo(RX+34,430); ctx.lineTo(RX-34,430); ctx.closePath(); ctx.fill();
    ctx.restore();
    ctx.strokeStyle='#a16207'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(RX-32,64); ctx.lineTo(RX-32,372); ctx.quadraticCurveTo(RX-30,420,RX,424); ctx.quadraticCurveTo(RX+30,420,RX+32,372); ctx.lineTo(RX+32,64); ctx.stroke();
    ctx.fillStyle='#92400e'; ctx.font='12px sans-serif'; ctx.textAlign='left'; ctx.fillText('根冠',RX+38,420); ctx.fillText('↑ 根元のほう',RX-30,60);
    LOCS.forEach(function(Lc,i){ const on=i===loc; ctx.lineWidth=on?3:1.5; ctx.strokeStyle=on?'#0e7490':'#64748b'; ctx.fillStyle=on?'rgba(14,116,144,.14)':'rgba(255,255,255,0)';
      ctx.beginPath(); ctx.rect(RX-38,Lc.y0,76,Lc.y1-Lc.y0); ctx.fill(); ctx.stroke();
      ctx.fillStyle=on?'#0e7490':'#334155'; ctx.font='bold 20px sans-serif'; ctx.textAlign='left'; ctx.fillText(Lc.s.charAt(0),RX+44,(Lc.y0+Lc.y1)/2+2);
      ctx.font=(on?'bold ':'')+'12px sans-serif'; ctx.fillText(['根の先端付近','先端から少し上','根元に近い'][i],RX+44,(Lc.y0+Lc.y1)/2+19);
      if(i===0){ ctx.fillText('（成長点）',RX+44,(Lc.y0+Lc.y1)/2+34); } });
    ctx.strokeStyle='rgba(14,116,144,.5)'; ctx.lineWidth=1.2; ctx.setLineDash([5,4]); ctx.beginPath(); ctx.moveTo(RX+38,L.y0); ctx.lineTo(FX-FR*0.55,FY-FR*0.83); ctx.moveTo(RX+38,L.y1); ctx.lineTo(FX-FR*0.55,FY+FR*0.83); ctx.stroke(); ctx.setLineDash([]);
    // 視野
    ctx.save(); ctx.beginPath(); ctx.arc(FX,FY,FR,0,6.283); ctx.fillStyle='#fdf2f8'; ctx.fill(); ctx.clip();
    CELLS[loc].forEach(function(c,i){ mcell(c,i===sel); });
    ctx.restore(); ctx.strokeStyle='#1f2937'; ctx.lineWidth=7; ctx.beginPath(); ctx.arc(FX,FY,FR+3,0,6.283); ctx.stroke();
    ctx.fillStyle='#475569'; ctx.font='11px sans-serif'; ctx.textAlign='right'; ctx.fillText('酢酸オルセインで染めたようす（約400倍のイメージ）',W-10,FY+FR+18);
    const cn=counts(); ctx.textAlign='left'; ctx.fillStyle='#0e7490'; fit(L.name,250,H-28,W-260,14,'bold'); fit('分裂中の細胞 '+cn[0]+'個／'+cn[1]+'個　細胞の長さ（Aを1として）'+L.len,250,H-9,W-260,14,'bold'); }
  // ---------- 共通 ----------
  function dotsX(i,n){ return 46+i*(548/(n-1)); }
  function drawHead(){ const L=list(), idx=Math.round(p), it=L[idx];
    ctx.textAlign='left'; ctx.fillStyle='#0f172a'; fit(NUMS[idx]+' '+it.n,14,26,440,19,'bold');
    ctx.textAlign='right'; ctx.font='bold 12px sans-serif'; ctx.fillStyle='#64748b'; ctx.fillText(mode==='tai'?('高校の言い方：'+it.hi):'減数分裂と受精',W-14,24);
    ctx.textAlign='left'; ctx.font='13px sans-serif'; ctx.fillStyle='#334155'; wrap(it.d,14,48,W-28,17,2);
    const n=L.length, y=88; ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(dotsX(0,n),y); ctx.lineTo(dotsX(n-1,n),y); ctx.stroke();
    ctx.strokeStyle='#0e7490'; ctx.beginPath(); ctx.moveTo(dotsX(0,n),y); ctx.lineTo(dotsX(0,n)+(dotsX(n-1,n)-dotsX(0,n))*p/(n-1),y); ctx.stroke();
    for(let i=0;i<n;i++){ const x=dotsX(i,n), on=i===idx; ctx.beginPath(); ctx.arc(x,y,on?13:11,0,6.283); ctx.fillStyle=on?'#0e7490':(i<p?'#a5f3fc':'#f1f5f9'); ctx.fill(); ctx.strokeStyle=on?'#0e7490':'#94a3b8'; ctx.lineWidth=1.5; ctx.stroke();
      ctx.fillStyle=on?'#fff':'#334155'; ctx.font='bold 13px sans-serif'; ctx.textAlign='center'; ctx.fillText(String(i+1),x,y+5); } }
  function drawFoot(){ const it=list()[Math.round(p)];
    ctx.textAlign='center'; ctx.fillStyle='#0f172a'; fit(it.c,W/2,330,W-24,17,'bold');
    ctx.fillStyle='#f8fafc'; ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; rr(14,344,W-28,64,10); ctx.fill(); ctx.stroke();
    const rows=[['tai','体細胞分裂：4本の細胞 → 4本の細胞が2つ（数は変わらない）'],['gen','減数分裂：4本の細胞 → 2本の生殖細胞（半分）→ 受精で4本にもどる']];
    rows.forEach(function(r,i){ const on=r[0]===mode, y=368+i*26; ctx.textAlign='left'; ctx.fillStyle=on?(i?'#b45309':'#0e7490'):'#64748b'; ctx.fillText(on?'▶':'　',24,y); fit(r[1],44,y,W-72,14,on?'bold':''); });
    ctx.textAlign='center'; ctx.fillStyle='#64748b'; ctx.font='12px sans-serif'; ctx.fillText('図をタップ → 次の段階へ　／　上の1〜'+list().length+'をタップ → その段階へ',W/2,430); }
  function stats(){ let key, a, b, c, ka, kb, kc;
    if(mode==='ken'){ const cn=counts(); ka='観察している場所'; a=LOCS[loc].s; kb='分裂中の細胞（視野の中）'; b=cn[0]+'個／'+cn[1]+'個'; kc='細胞の長さ（A＝1）'; c=LOCS[loc].len; }
    else { const it=list()[Math.round(p)]; ka='いまの段階'; a=it.s; kb='1つの細胞の染色体'; b=(mode==='gen'?it.ch:4)+'本'; kc='細胞の数'; c=it.k+'個'; }
    key=[a,b,c,ka].join('|'); if(key===statKey) return; statKey=key;
    [['sStage',ka,a],['sChr',kb,b],['sCell',kc,c]].forEach(function(r){ const el=$(r[0]); if(!el) return; el.textContent=r[2]; const kk=el.parentNode.querySelector('.k'); if(kk) kk.textContent=r[1]; });
    $('sStage').style.fontSize=a.length>7?'15px':'18px';
    if(mode==='ken') setShare('【細胞分裂】タマネギの根の'+LOCS[loc].name.slice(2)+'では、分裂中の細胞が'+b+'。根の先端付近は細胞が小さく分裂がさかん、根元に近いほど細胞が大きい｜シミュラボ');
    else if(mode==='gen') setShare('【減数分裂と受精】染色体4本の細胞 → 減数分裂で2本の生殖細胞（半分）→ 受精で4本にもどる。いまの段階：'+a+'｜シミュラボ');
    else setShare('【体細胞分裂】染色体4本の細胞が「'+a+'」の段階。分裂後の2つの細胞も4本ずつで、数は変わらない｜シミュラボ');
    if(mode!=='ken') $('stL').textContent=a; }
  function draw(){ ctx.fillStyle='#ffffff'; ctx.fillRect(0,0,W,H);
    if(mode==='ken') drawKen(); else { drawHead(); if(mode==='gen') drawGen(p); else drawTai(p); drawFoot(); }
    stats(); }
  function setPlay(){ $('play').textContent=playing?'⏸ 止める':'▶ 再生'; }
  function syncSl(){ $('st').value=Math.round(p*100); }
  function step(dt){ if(mode==='ken') return;
    if(playing){ if(hold>0){ hold-=dt; return; } const nx=Math.floor(p+1e-6)+1; p+=dt*0.55; if(p>=nx){ p=nx; hold=1.2; if(p>=maxP()){ p=maxP(); playing=false; setPlay(); } } syncSl(); }
    else if(tgt!==null){ const d=tgt-p, s=dt*2.4; if(Math.abs(d)<=s){ p=tgt; tgt=null; } else p+=Math.sign(d)*s; syncSl(); } }
  function setMode(m){ mode=m; playing=false; tgt=null; hold=0; setPlay(); sel=-1; statKey='';
    const ken=mode==='ken'; $('st').closest('.field').style.display=ken?'none':''; $('play').style.display=ken?'none':''; $('reset').style.display=ken?'none':'';
    if(!ken){ $('st').max=maxP()*100; p=mode==='gen'?1:2; syncSl(); }
    $('prev').textContent=ken?'◀ 前の場所':'◀ 前へ'; $('next').textContent=ken?'次の場所 ▶':'次へ ▶'; draw(); }
  $('mode').addEventListener('change',function(){ setMode($('mode').value); });
  $('st').addEventListener('input',function(){ playing=false; tgt=null; setPlay(); p=clamp(+$('st').value/100,0,maxP()); statKey=''; });
  $('play').addEventListener('click',function(){ if(playing){ playing=false; } else { if(p>=maxP()-1e-6) p=0; tgt=null; hold=0.3; playing=true; } setPlay(); });
  $('reset').addEventListener('click',function(){ playing=false; setPlay(); tgt=0; });
  $('next').addEventListener('click',function(){ if(mode==='ken'){ loc=(loc+2)%3; sel=-1; statKey=''; return; } playing=false; setPlay(); const b=tgt!==null?tgt:p; tgt=Math.min(maxP(),Math.floor(b+1e-6)+1); });
  $('prev').addEventListener('click',function(){ if(mode==='ken'){ loc=(loc+1)%3; sel=-1; statKey=''; return; } playing=false; setPlay(); const b=tgt!==null?tgt:p; tgt=Math.max(0,Math.ceil(b-1e-6)-1); });
  cv.addEventListener('pointerdown',function(e){ const q=cpos(cv,e), x=q[0]/dpr, y=q[1]/dpr;
    if(mode==='ken'){
      if(x<262){ let best=-1, bd=1e9; LOCS.forEach(function(L,i){ const d=Math.abs(y-(L.y0+L.y1)/2); if(d<bd){ bd=d; best=i; } }); if(best>=0 && bd<70){ loc=best; sel=-1; statKey=''; } return; }
      if(Math.hypot(x-FX,y-FY)<FR){ const cs=CELLS[loc]; let f=-1; for(let i=0;i<cs.length;i++){ const c=cs[i]; if(x>=c.x&&x<c.x+c.w&&y>=c.y&&y<c.y+c.h){ f=i; break; } } sel=(f===sel)?-1:f; }
      return; }
    const n=list().length;
    if(y>70 && y<106){ let bi=0, bd=1e9; for(let i=0;i<n;i++){ const d=Math.abs(x-dotsX(i,n)); if(d<bd){ bd=d; bi=i; } } if(bd<30){ playing=false; setPlay(); tgt=bi; } return; }
    if(y>=106 && y<318){ playing=false; setPlay(); const b=tgt!==null?tgt:p; tgt=b>=maxP()-1e-6?0:Math.floor(b+1e-6)+1; } });
  function frame(ts){ const dt=last?Math.min(0.05,(ts-last)/1000):0; last=ts; step(dt); draw(); requestAnimationFrame(frame); }
  setMode('tai'); draw();
  requestAnimationFrame(frame);
'''

sim(slug="saibou-bunretsu", cat="rika", emoji="🧫", score=80,
    title="細胞分裂シミュレーター（体細胞分裂・減数分裂と受精）",
    title_tag="体細胞分裂のシミュレーター｜タマネギの根の細胞分裂の順序と染色体の動き・減数分裂との比較（中3理科）",
    meta_desc="タマネギの根の先端の体細胞分裂を、分裂前→染色体が見える→中央に並ぶ→両端へ分かれる→仕切りができ2つの細胞に、と段階ごとに再生。染色体の数が体細胞分裂では変わらず、減数分裂では半分になり受精でもとにもどることを比較できます。顕微鏡で見た根の先端の模式図つき。",
    og_title="細胞分裂シミュレーター（体細胞分裂・減数分裂と受精）",
    og_desc="体細胞分裂の順序と染色体の動きを段階ごとに再生。減数分裂では染色体が半分になり、受精でもとにもどることを比較。",
    card_desc="体細胞分裂の順序と染色体の動きを段階ごとに再生。減数分裂・受精との比較、根の先端の顕微鏡図つき。",
    lead="タマネギの根の先端の細胞が分裂するようすを、段階ごとに止めたり再生したりできます。色分けした4本の染色体で、体細胞分裂では数が変わらず、減数分裂では半分になり受精でもとにもどることを比べられます。",
    model="中3 生物の成長と殖え方（細胞分裂）",
    level="中学3年（高校 生物基礎の細胞周期も参考に）",
    unit="中学校 第2分野（5）生命の連続性",
    canvas=canvas(640, 440, light=True),
    controls=select("mode", "表示する内容", [("tai", "体細胞分裂（タマネギの根の先端）"), ("gen", "減数分裂と受精（体細胞分裂とくらべる）"),
                                           ("ken", "顕微鏡で見た根の先端（場所によるちがい）")])
             + slider("st", "段階（左右に動かす）", 0, 600, 200, 1),
    buttons=btn("play", "▶ 再生", True) + btn("prev", "◀ 前へ") + btn("next", "次へ ▶") + btn("reset", "⏮ 最初から"),
    stats=stats([("sStage", "いまの段階", True), ("sChr", "1つの細胞の染色体", False), ("sCell", "細胞の数", False)]),
    legend="染色体は見やすいように4本（形と大きさが同じものが2本ずつ＝2対）にして色分けしています。赤・青＝この生物が両親から1本ずつ受けついだ染色体、緑＝受精する相手（もう一方の親）から来た染色体。X字の形は、複製された2本がくっついた染色体です。顕微鏡の図は模式図です。",
    article=SAIBOU_ARTICLE, faqs=SAIBOU_FAQS,
    rel=[("mendel-iden", "🌱", "遺伝の規則性シミュレーター"), ("dna", "🧬", "DNA二重らせん"), ("kougousei", "🍃", "光合成のしくみ"),
         ("hito-karada", "🫀", "人の体のつくりとはたらき"), ("shinka-sim", "🧬", "進化シミュレーター")],
    js=SAIBOU_JS)


# ============================================================ 2 水圧と浮力
def _p(cm): return cm * 0.01          # 水圧 N/cm²（100g→1N の約束）
SUIATSU_P_TABLE = T([["1cm", "0.01 N/cm²", "100 Pa（1 hPa）"], ["10cm", "0.1 N/cm²", "1,000 Pa（1 kPa）"], ["50cm", "0.5 N/cm²", "5,000 Pa（5 kPa）"],
                     ["1m", "1 N/cm²", "10,000 Pa（10 kPa）"], ["10m", "10 N/cm²", "100,000 Pa（100 kPa）＝大気圧（約101 kPa）とほぼ同じ"]],
                    ["水の深さ", "水圧（1cm²あたりの力）", "水圧（パスカル）"])
SUIATSU_F_TABLE = T([["小（5cm×5cm×高さ2cm）", "50 cm³", "0.25 N", "0.50 N"], ["中（5cm×5cm×高さ4cm）", "100 cm³", "0.25 N", "1.00 N"],
                     ["大（5cm×5cm×高さ8cm）", "200 cm³", "0.25 N", "2.00 N"]],
                    ["物体（直方体）", "体積", "水中に1cm沈めるごとにふえる浮力", "全部沈めたときの浮力"])

SUIATSU_ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
''' + P('<b>水圧</b>は水の重さによって生じる圧力で、<b>深いほど大きく</b>、水中の物体に<b>あらゆる向きから</b>はたらきます。水中の物体の下の面を押す水圧は上の面を押す水圧より大きいので、その差によって上向きの力＝<b>浮力</b>がはたらきます。ばねばかりの値は、浮力の分だけ小さくなります。') + '''
<p>中学3年 第1分野（5）運動とエネルギー「力のつり合いと合成・分解」の「水中の物体に働く力」の内容です。学習指導要領の解説では、ゴム膜を張った円筒を水中に沈める実験で水圧と深さの関係や水圧があらゆる向きに働くことに気付かせること、ばねばかりにつるした物体を水中に沈めると示す値が小さくなることから浮力を理解させ、浮力を上面と下面の水圧の差から定性的に捉えさせることが示されています。このシミュレーションでは、その3つの実験（ばねばかり・ゴム膜をはった筒・穴のあいたペットボトル）を切り替えて試せます。</p>
<h2>授業での使い方</h2>
<ul>
<li><b>導入</b>：「穴のあいたペットボトル」に切り替え、下の穴ほど水が勢いよく飛ぶことを見せます。「なぜ下の穴ほど勢いがよいのだろう」と問いかけ、2年で学んだ大気圧と結びつけて水圧の予想を立てます。</li>
<li><b>展開</b>：「ゴム膜をはった筒」で、深くするとゴム膜のへこみが大きくなること、筒を横向きにすると左右のへこみが同じになることを確かめます。次に「ばねばかりで浮力をはかる」で物体を少しずつ沈め、ばねばかりの値と浮力の変わり方を右のグラフで読み取ります。実物の実験の結果とくらべるのにも使えます。</li>
<li><b>まとめ</b>：物体の大きさ（体積）や質量を変えて、浮力は「水中にある部分の体積」で決まり、物体の重さでは決まらないこと、全部沈めると深さを変えても浮力は変わらないことを確かめます。質量を小さくして、物体が浮く条件も考えます。</li>
</ul>
<p>生徒への問いの例：</p>
<ol>
<li>物体を全部沈めたあと、さらに深く沈めると、ばねばかりの値はどうなるだろう。それはなぜだろう。</li>
<li>同じ大きさで、質量が100gの物体と300gの物体では、はたらく浮力はどちらが大きいだろう。</li>
<li>ゴム膜をはった筒を縦向きにして沈めたとき、上と下のゴム膜のへこみ方がちがうのはなぜだろう。このちがいと浮力には、どんな関係があるだろう。</li>
</ol>
<h2>しくみ・解説</h2>
<h3>用語の意味</h3>
<ul>
<li><b>水圧</b>とは、水の重さによって生じる圧力のことで、水中の物体の表面に垂直に、あらゆる向きからはたらきます。</li>
<li><b>浮力</b>とは、水中にある物体にはたらく上向きの力のことで、物体の下の面と上の面にはたらく水圧の差によって生じます。</li>
<li><b>圧力</b>とは、面を垂直に押す力の、1m²（または1cm²）あたりの大きさです。単位はパスカル（Pa）で、1 Pa＝1 N/m²です。</li>
</ul>
<h3>水圧の式と早見表</h3>
''' + N('水圧〔Pa〕＝ 水の密度〔kg/m³〕× 9.8 × 水の深さ〔m〕<br>中学校の約束（100gの物体にはたらく重力＝1N）では、<b>深さ1cmごとに約0.01 N/cm²（約100 Pa）</b>、<b>1mで約10 kPa</b>大きくなります。') + '''
<p>深さ1cmの水圧は、底面積1cm²・高さ1cmの水（1cm³＝1g）の重さ、0.01Nが1cm²の面を押していると考えるとわかります。深さが2倍、3倍になると、上にある水の重さも2倍、3倍になるので、水圧は深さに比例します。</p>
''' + SUIATSU_P_TABLE + '''
<p>正確に9.8 N/kgで計算すると、深さ1mの水圧は9.8 kPaです。海で10m深くもぐるごとに、およそ1気圧ずつ大きな圧力がかかることになります。</p>
<h3>浮力の求め方</h3>
''' + N('浮力〔N〕＝ 空気中でのばねばかりの値〔N〕－ 水中でのばねばかりの値〔N〕<br>力のつり合い：物体にはたらく重力 ＝ 浮力 ＋ ばねばかりが引く力') + '''
<p>例：体積100cm³（5cm×5cm×高さ4cm）、質量300gの物体は、空気中でばねばかりが3.00Nを示します。全部水に沈めると2.00Nになったので、浮力は 3.00－2.00＝1.00N です。</p>
<p>水圧の差で確かめると、上面が深さ2cmのとき、上面を押す力は 0.02 N/cm²×25cm²＝0.50N（下向き）、下面（深さ6cm）を押す力は 0.06 N/cm²×25cm²＝1.50N（上向き）。その差 1.50－0.50＝1.00N が浮力になります。横から押す力は、左右で同じ大きさなので打ち消し合います。</p>
''' + SUIATSU_F_TABLE + '''
<p>物体を少しずつ沈めると、水中にある部分の体積に比例して浮力が大きくなります。全部沈んだあとは、深くしても上面と下面の水圧の差（＝物体の高さ分の水圧）が変わらないので、浮力は一定です。浮力の大きさは物体の体積（水中にある部分）で決まり、物体の質量や材質には関係しません。</p>
<h3>浮くか、沈むか</h3>
<p>物体を全部沈めたときの浮力が物体の重力より大きいと、物体は浮き上がり、水中にある部分の浮力と重力がつり合ったところで浮かびます。これは、物体の密度（1cm³あたりの質量）が水の密度（約1 g/cm³）より小さいときです。このシミュレーションでは、質量が体積の数値より小さいと浮き、ばねばかりの値は0Nになります。</p>
''' + T([["鉄", "7.87", "沈む"], ["銅", "8.96", "沈む"], ["アルミニウム", "2.70", "沈む"], ["水（4℃）", "1.00", "—"],
          ["氷（0℃）", "0.92", "浮く"], ["ポリプロピレン", "約0.9", "浮く"], ["木（スギ・乾燥）", "約0.4", "浮く"]],
         ["物質", "密度〔g/cm³〕", "水に入れると"]) + '''
<h3>発展：アルキメデスの原理（高校 物理基礎・物理）</h3>
<p>水中の物体にはたらく浮力の大きさは、物体が押しのけた水の重さに等しくなります（<b>アルキメデスの原理</b>）。式では F＝ρVg（ρ：水の密度、V：水中にある部分の体積、g：重力加速度）です。体積100cm³の物体を全部沈めると100cm³＝100gの水を押しのけるので、浮力は約1Nになります。鉄でできた船が浮くのは、中が空洞になっていて、船全体として押しのける水の体積が大きいからです。</p>
<h3>ペットボトルの穴から出る水</h3>
<p>深い位置の穴ほど水圧が大きいので、水が勢いよく出ます。高校の物理では、穴から出る水の速さが v＝√(2gh)（h：水面から穴までの深さ）になることを学びます。深さ4cmで約0.9 m/s、16cmで約1.8 m/sです。同じ深さの穴なら、向きがちがっても同じ勢いで出ます。</p>
''' + N('<b>このシミュレーションで単純にしていること</b>：100gの物体にはたらく重力を1N、水の密度を1 g/cm³としています。水面にはたらく大気圧は、物体の上下や筒の内外で打ち消し合うので省いています。物体を沈めても容器の水面は上がらないものとし、ペットボトルは水を足し続けて水面の高さを一定にしているものとします。穴から出る水の飛び方は空気の抵抗などを考えない計算なので、実際は少し手前に落ちます。矢印やゴム膜のへこみは、見やすいように大きさを強調しています。') + '''
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「中学校学習指導要領（平成29年告示）」理科 第1分野（5）運動とエネルギー（ア）（ｱ）力のつり合いと合成・分解／「中学校学習指導要領（平成29年告示）解説 理科編」（水圧の実験、浮力と水圧の定性的な関係）</li>
<li>''' + MEXT + '''</li>
<li>国立天文台 編『理科年表』（物質の密度）</li>
<li>中学校理科の教科書（第3学年）「水中の物体に働く力」、高等学校「物理基礎」「物理」の教科書（浮力・アルキメデスの原理）</li>
</ul>
'''

SUIATSU_FAQS = [
    ("水圧とは何ですか？", "水の重さによって生じる圧力です。水中の物体の表面に垂直に、あらゆる向きからはたらき、深さに比例して大きくなります。深さ1cmごとに約0.01 N/cm²（約100 Pa）、1mで約10 kPa大きくなります。"),
    ("浮力の大きさはどうやって求めますか？", "空気中でのばねばかりの値から、水中でのばねばかりの値を引いて求めます。空気中で3.0N、水中で2.0Nなら、浮力は1.0Nです。浮力は、物体の下の面と上の面を押す水圧の差によって生じます。"),
    ("物体を深く沈めるほど、浮力は大きくなりますか？", "物体の一部が水の上に出ている間は、沈めるほど（水中にある部分の体積が大きくなるほど）浮力は大きくなります。全部沈んだあとは、深さを変えても浮力は変わりません。上面と下面の深さの差（物体の高さ）が変わらず、水圧の差も同じだからです。"),
    ("重い物体ほど、浮力は大きくなりますか？", "なりません。浮力の大きさは、水中にある部分の体積で決まります。同じ体積なら、鉄でもアルミニウムでも、全部沈めたときの浮力は同じです（100cm³なら約1N）。"),
    ("物体が水に浮くか沈むかは、何で決まりますか？", "物体にはたらく重力と、全部沈めたときの浮力の大きさで決まります。浮力のほうが大きければ浮き、重力のほうが大きければ沈みます。物体の密度が水の密度（約1 g/cm³）より小さいと浮き、大きいと沈むともいえます。"),
    ("鉄でできた船が水に浮くのはなぜですか？", "船は中が空洞になっているので、船全体として押しのける水の体積が大きく、その分の大きな浮力がはたらくからです。船全体の平均の密度は水より小さくなっています。浮力が押しのけた水の重さに等しいことを、アルキメデスの原理といいます。"),
]

SUIATSU_JS = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const PX=12, SY=232, FL=SY+16*PX, OX=195, CL=72, CR=318, S=25, PB=9, BX0=206, BX1=286, BB=300, TRAY=448, PC='#0369a1';
  const HOLES=[{sd:1,h:14,n:'上の穴'},{sd:1,h:8,n:'真ん中の穴'},{sd:1,h:2,n:'下の穴'},{sd:-1,h:14,n:'左の穴'}];
  let mode='bane', dB=+$('dep').value, dG=6, wl=18, drag=null, tt=0, last=0, statKey='';
  const lab=document.querySelector('label[for=dep]');
  function fld(id){ return $(id).closest('.field'); }
  function f2(v){ return (Math.round(v*100)/100).toFixed(2); }
  function f1(v){ return (Math.round(v*10)/10).toFixed(1); }
  function pr(z){ return Math.max(0,z)*0.01; }
  function rr(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
  function fit(t,x,y,maxW,size,weight){ let s=size; ctx.font=weight+' '+s+'px sans-serif'; while(ctx.measureText(t).width>maxW && s>9){ s--; ctx.font=weight+' '+s+'px sans-serif'; } ctx.fillText(t,x,y); }
  function arrow(x0,y0,x1,y1,col,w){ const L=Math.hypot(x1-x0,y1-y0); if(L<3) return; const hs=Math.min(7,L*0.55), a=Math.atan2(y1-y0,x1-x0);
    ctx.strokeStyle=col; ctx.fillStyle=col; ctx.lineWidth=w||2; ctx.beginPath(); ctx.moveTo(x0,y0); ctx.lineTo(x1-Math.cos(a)*hs*0.8,y1-Math.sin(a)*hs*0.8); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x1-Math.cos(a-0.45)*hs,y1-Math.sin(a-0.45)*hs); ctx.lineTo(x1-Math.cos(a+0.45)*hs,y1-Math.sin(a+0.45)*hs); ctx.closePath(); ctx.fill(); }
  function phys(d){ const h=+$('sz').value, m=+$('m').value, V=S*h, Wt=m/100, fl=m<V, dF=m/S; const dObj=(fl&&d>dF)?dF:d, sub=clamp(dObj,0,h), Fb=sub*S*0.01;
    return {h:h,m:m,V:V,Wt:Wt,fl:fl,dObj:dObj,sub:sub,Fb:Fb,rd:Math.max(0,Wt-Fb),top:dObj-h,slack:fl&&d>dF+1e-9,dens:m/V}; }
  function tank(){ ctx.fillStyle='rgba(56,189,248,.22)'; ctx.fillRect(CL,SY,CR-CL,FL-SY); ctx.strokeStyle='#0284c7'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.moveTo(CL,SY); ctx.lineTo(CR,SY); ctx.stroke();
    ctx.strokeStyle='#475569'; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(CL,SY-34); ctx.lineTo(CL,FL); ctx.lineTo(CR,FL); ctx.lineTo(CR,SY-34); ctx.stroke();
    ctx.fillStyle='#0369a1'; ctx.font='10px sans-serif'; ctx.textAlign='left';
    for(let c=0;c<=16;c++){ const y=SY+c*PX; ctx.fillRect(CL+1,y-0.5,c%2===0?9:5,1); if(c%4===0 && c>0 && c<16) ctx.fillText(c+'cm',CL+12,y+4); }
    ctx.fillText('深さ',CL+12,SY+14); ctx.textAlign='right'; ctx.fillText('水面',CR-4,SY-4); }
  function stand(yArm){ ctx.fillStyle='#94a3b8'; ctx.fillRect(28,6,7,FL-6); ctx.fillRect(14,FL,40,7); ctx.fillRect(28,6,OX-28+4,6); }
  function springScale(rd){ const y0=18, y1=88; ctx.fillStyle='#64748b'; ctx.fillRect(OX-2,12,4,6);
    ctx.fillStyle='#f8fafc'; ctx.strokeStyle='#64748b'; ctx.lineWidth=1.5; rr(OX-15,16,30,86,6); ctx.fill(); ctx.stroke();
    const py=y0+Math.min(rd,5)/5*(y1-y0);
    ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1.2; ctx.beginPath(); ctx.moveTo(OX,19); for(let i=1;i<=12;i++){ ctx.lineTo(OX+(i%2?6:-6),19+(py-19)*i/12); } ctx.lineTo(OX,py); ctx.stroke();
    ctx.fillStyle='#334155'; ctx.font='9px sans-serif'; ctx.textAlign='right';
    for(let v=0;v<=10;v++){ const y=y0+v/10*(y1-y0); ctx.fillRect(OX+9,y-0.5,v%2?3:6,1); if(v%2===0) ctx.fillText(String(v/2),OX-6+0,y+3); }
    ctx.fillStyle='#dc2626'; ctx.fillRect(OX-12,py-1.5,24,3);
    ctx.fillStyle='#64748b'; ctx.fillRect(OX-1.5,102,3,8); ctx.strokeStyle='#64748b'; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(OX,113,4,-Math.PI*0.5,Math.PI*0.9); ctx.stroke();
    ctx.fillStyle='#0f172a'; rr(OX+22,34,92,34,8); ctx.fill(); ctx.fillStyle='#86efac'; ctx.font='bold 19px ui-monospace,Menlo,Consolas,monospace'; ctx.textAlign='right'; ctx.fillText(f2(rd)+' N',OX+108,58);
    ctx.fillStyle='#475569'; ctx.font='11px sans-serif'; ctx.textAlign='left'; ctx.fillText('ばねばかり',OX+24,28); }
  function graphBox(x0,y0,x1,y1,xmax,ymax,xt,yt,xlab,ylab,yfmt){ ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; ctx.font='10px sans-serif'; ctx.fillStyle='#64748b';
    for(let v=0;v<=ymax+1e-9;v+=yt){ const y=y1-v/ymax*(y1-y0); ctx.beginPath(); ctx.moveTo(x0,y); ctx.lineTo(x1,y); ctx.stroke(); ctx.textAlign='right'; ctx.fillText(yfmt(v),x0-4,y+3); }
    for(let v=0;v<=xmax+1e-9;v+=xt){ const x=x0+v/xmax*(x1-x0); ctx.beginPath(); ctx.moveTo(x,y0); ctx.lineTo(x,y1); ctx.stroke(); ctx.textAlign='center'; ctx.fillText(String(v),x,y1+12); }
    ctx.strokeStyle='#64748b'; ctx.lineWidth=1.3; ctx.beginPath(); ctx.moveTo(x0,y0); ctx.lineTo(x0,y1); ctx.lineTo(x1,y1); ctx.stroke();
    ctx.fillStyle='#475569'; ctx.textAlign='right'; ctx.fillText(xlab,x1,y1+25); ctx.textAlign='left'; ctx.fillText(ylab,x0-30,y0-7); }
  // ---------- ばねばかりで浮力 ----------
  function drawBane(){ const c=phys(dB), top=SY+c.top*PX, bot=SY+c.dObj*PX, OW=60;
    stand(); tank(); springScale(c.rd);
    ctx.strokeStyle='#334155'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.moveTo(OX,117);
    if(c.slack){ const sg=Math.min(40,(dB-c.dObj)*PX*0.8+8); ctx.bezierCurveTo(OX+sg,117+(top-117)*0.3,OX+sg,117+(top-117)*0.7,OX,top); } else ctx.lineTo(OX,top); ctx.stroke();
    const light=c.dens<1; ctx.fillStyle=light?'#e7c38f':'#a8b3c2'; ctx.strokeStyle='#334155'; ctx.lineWidth=2; ctx.fillRect(OX-OW/2,top,OW,bot-top); ctx.strokeRect(OX-OW/2,top,OW,bot-top);
    const wt=Math.max(top,SY); if(bot>wt){ ctx.fillStyle='rgba(56,189,248,.28)'; ctx.fillRect(OX-OW/2,wt,OW,bot-wt); }
    ctx.fillStyle='#0f172a'; ctx.textAlign='center';
    if(c.h>=4){ fit(c.V+'cm³',OX,(top+bot)/2-3,OW-6,12,'bold'); fit(c.m+'g',OX,(top+bot)/2+12,OW-6,12,'bold'); } else fit(c.V+'cm³・'+c.m+'g',OX,(top+bot)/2+4,OW-4,11,'bold');
    ctx.save(); ctx.beginPath(); ctx.rect(CL+2,SY,CR-CL-4,FL-SY-2); ctx.clip();
    if(c.dObj>0){ const L=3*c.dObj; [-18,0,18].forEach(function(dx){ arrow(OX+dx,bot+L+3,OX+dx,bot+1,PC,2); }); }
    if(c.top>0){ const L=3*c.top; [-18,0,18].forEach(function(dx){ arrow(OX+dx,top-L-3,OX+dx,top-1,PC,2); }); }
    const fr=c.h>=8?[0.12,0.37,0.63,0.88]:(c.h>=4?[0.2,0.5,0.8]:[0.5]);
    fr.forEach(function(f){ const z=c.top+f*c.h; if(z<=0) return; const L=3*z, y=SY+z*PX; arrow(OX-OW/2-L-3,y,OX-OW/2-1,y,PC,2); arrow(OX+OW/2+L+3,y,OX+OW/2+1,y,PC,2); });
    ctx.restore();
    if(c.slack){ ctx.fillStyle='#b45309'; ctx.font='bold 13px sans-serif'; ctx.textAlign='center'; ctx.fillText('浮いている（糸がたるむ）',OX,FL+22); }
    else { ctx.fillStyle='#475569'; ctx.font='12px sans-serif'; ctx.textAlign='center'; ctx.fillText('物体を上下にドラッグして沈められます',OX,FL+22); }
    // 右パネル
    const X=352; ctx.textAlign='left'; ctx.fillStyle='#475569'; ctx.font='13px sans-serif'; ctx.fillText('ばねばかりの値',X,20);
    ctx.fillStyle='#1d4ed8'; ctx.font='bold 30px sans-serif'; ctx.fillText(f2(c.rd)+' N',X,52);
    if(c.slack){ ctx.font='bold 13px sans-serif'; ctx.fillStyle='#b45309'; ctx.fillText('浮力＝重力で浮いている',X+130,48); }
    ctx.fillStyle='#334155'; fit('空気中での値（重力）：'+f2(c.Wt)+' N',X,76,W-X-8,13,'');
    ctx.fillStyle='#c2410c'; fit('浮力 ＝ '+f2(c.Wt)+' － '+f2(c.rd)+' ＝ '+f2(c.Fb)+' N',X,98,W-X-8,15,'bold');
    ctx.fillStyle='#334155'; fit('水中にある部分の体積：'+Math.round(c.sub*S)+' cm³（全体 '+c.V+' cm³）',X,118,W-X-8,12,'');
    ctx.fillStyle=PC; fit('上面の水圧：'+(c.top>0?f2(pr(c.top))+' N/cm²（'+Math.round(pr(c.top)*10000)+' Pa）':'0（水の外）'),X,138,W-X-8,12,'');
    fit('下面の水圧：'+f2(pr(c.dObj))+' N/cm²（'+Math.round(pr(c.dObj)*10000)+' Pa）',X,156,W-X-8,12,'');
    ctx.fillStyle=c.dens<1?'#b45309':'#334155'; fit('密度 '+f2(c.dens)+' g/cm³ → 水（1.00）より'+(c.dens<1?'小さいので浮く':(c.dens>1?'大きいので沈む':'と同じ')),X,176,W-X-8,12,'bold');
    const gx0=388, gx1=626, gy0=214, gy1=392, ymax=Math.max(0.5,Math.ceil(c.Wt*2-1e-9)/2), yt=ymax>3?1:(ymax>1.5?0.5:0.25);
    ctx.fillStyle='#0f172a'; ctx.font='bold 12px sans-serif'; ctx.textAlign='left'; ctx.fillText('沈めた深さと、ばねばかりの値・浮力',X,198);
    graphBox(gx0,gy0,gx1,gy1,15,ymax,3,yt,'物体の底面の深さ（cm）','（N）',function(v){ return v.toFixed(yt<0.5?2:1); });
    function gx(d){ return gx0+d/15*(gx1-gx0); } function gy(v){ return gy1-v/ymax*(gy1-gy0); }
    [['rd','#1d4ed8'],['Fb','#ea580c']].forEach(function(s){ ctx.strokeStyle=s[1]; ctx.lineWidth=2.4; ctx.beginPath(); for(let i=0;i<=150;i++){ const d=i/10, q=phys(d); if(i) ctx.lineTo(gx(d),gy(q[s[0]])); else ctx.moveTo(gx(d),gy(q[s[0]])); } ctx.stroke();
      ctx.fillStyle=s[1]; ctx.beginPath(); ctx.arc(gx(dB),gy(c[s[0]]),5,0,6.283); ctx.fill(); });
    ctx.font='bold 12px sans-serif'; ctx.textAlign='left'; ctx.fillStyle='#1d4ed8'; ctx.fillText('━ ばねばかりの値',X+8,H-12); ctx.fillStyle='#ea580c'; ctx.fillText('━ 浮力',X+130,H-12);
    return c; }
  // ---------- ゴム膜をはった筒 ----------
  function drawGomu(){ const vert=$('dir').value==='v', cd=clamp(dG,0,vert?11.5:14), cy=SY+cd*PX;
    stand(); tank();
    const topY=vert?cy-48:cy-24; ctx.fillStyle='#64748b'; ctx.fillRect(OX-3,12,6,topY-12);
    let z1, z2;
    if(vert){ z1=cd-4; z2=cd+4; const bt=1.5*Math.max(0,z1), bb=1.5*Math.max(0,z2), t=cy-48, b=cy+48;
      ctx.beginPath(); ctx.moveTo(OX-24,t); ctx.quadraticCurveTo(OX,t+2*bt,OX+24,t); ctx.lineTo(OX+24,b); ctx.quadraticCurveTo(OX,b-2*bb,OX-24,b); ctx.closePath(); ctx.fillStyle='#ffffff'; ctx.fill();
      ctx.strokeStyle='#334155'; ctx.lineWidth=2.5; ctx.beginPath(); ctx.moveTo(OX-24,t); ctx.lineTo(OX-24,b); ctx.moveTo(OX+24,t); ctx.lineTo(OX+24,b); ctx.stroke();
      ctx.strokeStyle='#f59e0b'; ctx.lineWidth=3.5; ctx.beginPath(); ctx.moveTo(OX-24,t); ctx.quadraticCurveTo(OX,t+2*bt,OX+24,t); ctx.stroke(); ctx.beginPath(); ctx.moveTo(OX-24,b); ctx.quadraticCurveTo(OX,b-2*bb,OX+24,b); ctx.stroke();
      [-12,0,12].forEach(function(dx){ const tt2=(dx+24)/48, k=4*tt2*(1-tt2); if(z1>0) arrow(OX+dx,t+bt*k-3*z1-4,OX+dx,t+bt*k-1,PC,2); if(z2>0) arrow(OX+dx,b-bb*k+3*z2+4,OX+dx,b-bb*k+1,PC,2); });
      ctx.font='bold 12px sans-serif'; ctx.textAlign='right'; ctx.fillStyle='#b45309'; ctx.fillText('上の膜',OX-30,t+4); ctx.fillText('下の膜',OX-30,b+4); }
    else { z1=cd; z2=cd; const bl=1.5*Math.max(0,cd), l=OX-48, r=OX+48;
      ctx.beginPath(); ctx.moveTo(l,cy-24); ctx.lineTo(r,cy-24); ctx.quadraticCurveTo(r-2*bl,cy,r,cy+24); ctx.lineTo(l,cy+24); ctx.quadraticCurveTo(l+2*bl,cy,l,cy-24); ctx.closePath(); ctx.fillStyle='#ffffff'; ctx.fill();
      ctx.strokeStyle='#334155'; ctx.lineWidth=2.5; ctx.beginPath(); ctx.moveTo(l,cy-24); ctx.lineTo(r,cy-24); ctx.moveTo(l,cy+24); ctx.lineTo(r,cy+24); ctx.stroke();
      ctx.strokeStyle='#f59e0b'; ctx.lineWidth=3.5; ctx.beginPath(); ctx.moveTo(l,cy-24); ctx.quadraticCurveTo(l+2*bl,cy,l,cy+24); ctx.stroke(); ctx.beginPath(); ctx.moveTo(r,cy-24); ctx.quadraticCurveTo(r-2*bl,cy,r,cy+24); ctx.stroke();
      if(cd>0) [-12,0,12].forEach(function(dy){ const tt2=(dy+24)/48, k=4*tt2*(1-tt2), L=3*cd; arrow(l+bl*k-L-4,cy+dy,l+bl*k-1,cy+dy,PC,2); arrow(r-bl*k+L+4,cy+dy,r-bl*k+1,cy+dy,PC,2); });
      ctx.font='bold 12px sans-serif'; ctx.textAlign='center'; ctx.fillStyle='#b45309'; ctx.fillText('左の膜',l,cy+42); ctx.fillText('右の膜',r,cy+42); }
    ctx.fillStyle='#475569'; ctx.font='12px sans-serif'; ctx.textAlign='center'; ctx.fillText('筒を上下にドラッグして深さを変えられます',OX,FL+22);
    const X=352, n1=vert?'上':'左', n2=vert?'下':'右';
    ctx.textAlign='left'; ctx.fillStyle='#0f172a'; ctx.font='bold 15px sans-serif'; ctx.fillText('ゴム膜のへこみ方（'+(vert?'縦向き':'横向き')+'）',X,22);
    ctx.fillStyle='#334155'; fit(n1+'の膜：深さ '+f1(Math.max(0,z1))+' cm → 水圧 '+f2(pr(z1))+' N/cm²',X,48,W-X-8,13,'');
    fit(n2+'の膜：深さ '+f1(z2)+' cm → 水圧 '+f2(pr(z2))+' N/cm²',X,70,W-X-8,13,'');
    ctx.fillStyle='#b45309';
    if(vert){ fit('下の膜のほうが大きくへこむ（深いほど水圧が大きい）',X,96,W-X-8,13,'bold'); ctx.fillStyle='#334155'; fit('上下の水圧の差 '+f2(pr(z2)-pr(z1))+' N/cm² が、浮力のもとになる',X,118,W-X-8,12,''); }
    else { fit('左右の膜は同じだけへこむ（同じ深さなら同じ水圧）',X,96,W-X-8,13,'bold'); ctx.fillStyle='#334155'; fit('水圧は、横向きにもはたらいている',X,118,W-X-8,12,''); }
    ctx.fillStyle='#334155'; fit('筒の向きを変えてくらべよう（あらゆる向きからはたらく）',X,140,W-X-8,12,'');
    const gx0=388, gx1=626, gy0=214, gy1=392;
    ctx.fillStyle='#0f172a'; ctx.font='bold 12px sans-serif'; ctx.textAlign='left'; ctx.fillText('水の深さと水圧（1cmごとに0.01 N/cm²）',X,198);
    graphBox(gx0,gy0,gx1,gy1,16,0.16,4,0.04,'水の深さ（cm）','（N/cm²）',function(v){ return v.toFixed(2); });
    ctx.strokeStyle=PC; ctx.lineWidth=2.4; ctx.beginPath(); ctx.moveTo(gx0,gy1); ctx.lineTo(gx1,gy0); ctx.stroke();
    [[z1,'#f59e0b'],[z2,'#b45309']].forEach(function(s){ if(s[0]<0) return; const x=gx0+s[0]/16*(gx1-gx0), y=gy1-pr(s[0])/0.16*(gy1-gy0); ctx.fillStyle=s[1]; ctx.beginPath(); ctx.arc(x,y,5.5,0,6.283); ctx.fill(); });
    ctx.font='bold 12px sans-serif'; ctx.fillStyle='#b45309'; ctx.textAlign='left'; ctx.fillText('● ゴム膜の位置の水圧',X+8,H-12);
    return {z1:z1,z2:z2,vert:vert,cd:cd}; }
  // ---------- 穴のあいたペットボトル ----------
  function drawBottle(){ const wy=BB-wl*PB;
    ctx.strokeStyle='#94a3b8'; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(10,TRAY); ctx.lineTo(W-10,TRAY); ctx.stroke();
    ctx.fillStyle='#e2e8f0'; ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1.5; ctx.fillRect(BX0-8,BB,BX1-BX0+16,TRAY-BB); ctx.strokeRect(BX0-8,BB,BX1-BX0+16,TRAY-BB);
    ctx.fillStyle='#64748b'; ctx.font='11px sans-serif'; ctx.textAlign='center'; ctx.fillText('台',(BX0+BX1)/2,BB+30);
    ctx.fillStyle='rgba(56,189,248,.35)'; ctx.fillRect(BX0+2,wy,BX1-BX0-4,BB-wy);
    ctx.strokeStyle='#0284c7'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.moveTo(BX0+2,wy); ctx.lineTo(BX1-2,wy); ctx.stroke();
    ctx.strokeStyle='#475569'; ctx.lineWidth=2.5; ctx.beginPath(); ctx.moveTo(236,78); ctx.lineTo(236,92); ctx.quadraticCurveTo(BX0,100,BX0,124); ctx.lineTo(BX0,BB); ctx.lineTo(BX1,BB); ctx.lineTo(BX1,124); ctx.quadraticCurveTo(BX1,100,256,92); ctx.lineTo(256,78); ctx.stroke();
    ctx.fillStyle='#38bdf8'; ctx.fillRect(232,70,28,9);
    ctx.fillStyle='#0369a1'; ctx.font='11px sans-serif'; ctx.textAlign='left'; ctx.fillText('水面',BX1+6,wy+4);
    const jets=[];
    HOLES.forEach(function(ho){ const x0=ho.sd>0?BX1:BX0, y0=BB-ho.h*PB, hd=wl-ho.h;
      ctx.fillStyle='#0f172a'; ctx.beginPath(); ctx.arc(x0,y0,3,0,6.283); ctx.fill();
      if(hd<=0.05){ jets.push(0); return; } const v=Math.sqrt(2*980*hd), drop=(TRAY-y0)/PB, tl=Math.sqrt(2*drop/980); jets.push(v);
      const pts=[]; for(let i=0;i<=40;i++){ const t=tl*i/40, x=x0+ho.sd*v*t*PB, y=y0+490*t*t*PB; if(x<4||x>W-4) break; pts.push([x,y]); }
      ctx.save(); ctx.lineCap='round'; ctx.strokeStyle='rgba(14,165,233,.35)'; ctx.lineWidth=4; ctx.beginPath(); pts.forEach(function(q,i){ if(i) ctx.lineTo(q[0],q[1]); else ctx.moveTo(q[0],q[1]); }); ctx.stroke();
      ctx.strokeStyle='#0284c7'; ctx.lineWidth=2.5; ctx.setLineDash([9,7]); ctx.lineDashOffset=-tt*90; ctx.stroke(); ctx.restore();
      const lp=pts[pts.length-1]; if(lp && lp[1]>TRAY-6){ ctx.fillStyle='rgba(14,165,233,.5)'; ctx.beginPath(); ctx.ellipse(lp[0],TRAY-2,9,3,0,0,6.283); ctx.fill(); } });
    ctx.fillStyle='#0f172a'; ctx.font='bold 11px sans-serif'; ctx.textAlign='center';
    [14,8,2].forEach(function(h){ const hd=wl-h; ctx.fillText(hd>0.05?('深さ'+f1(hd)+'cm'):'水の外',(BX0+BX1)/2,BB-h*PB+4); });
    ctx.fillStyle='#475569'; ctx.font='12px sans-serif'; ctx.textAlign='left'; ctx.fillText('上下にドラッグして',14,24); ctx.fillText('水面の高さを変えられます',14,42);
    const X=330; ctx.textAlign='left'; ctx.fillStyle='#0f172a'; ctx.font='bold 15px sans-serif'; ctx.fillText('穴の深さと水圧（水面からの深さ）',X,22);
    HOLES.slice(0,3).forEach(function(ho,i){ const hd=wl-ho.h; ctx.fillStyle=hd>0.05?'#334155':'#94a3b8';
      fit(ho.n+'：'+(hd>0.05?('深さ '+f1(hd)+' cm → 水圧 '+f2(pr(hd))+' N/cm²'):'水面より上なので水が出ない'),X,46+i*21,W-X-8,13,i===2?'bold':''); });
    ctx.fillStyle='#334155'; fit('左の穴：上の穴と同じ深さ → 同じ勢いで出る',X,110,W-X-8,13,'');
    ctx.fillStyle='#b45309'; fit('深いところの穴ほど、水が勢いよく遠くまで飛ぶ',X,134,W-X-8,14,'bold');
    return {wl:wl}; }
  function setK(id,t,v){ const el=$(id); if(!el) return; el.textContent=v; const k=el.parentNode.querySelector('.k'); if(k) k.textContent=t; }
  function stats(r){ let rows, sh;
    if(mode==='bane'){ rows=[['sRead','ばねばかりの値',f2(r.rd)+' N'],['sAir','空気中での値（重力）',f2(r.Wt)+' N'],['sBuoy','浮力',f2(r.Fb)+' N'],['sP','下面の水圧',f2(pr(r.dObj))+' N/cm²']];
      sh='【水圧と浮力】体積'+r.V+'cm³・'+r.m+'gの物体を底面の深さ'+f1(dB)+'cmまで沈めると、ばねばかり'+f2(r.rd)+'N・浮力'+f2(r.Fb)+'N（空気中'+f2(r.Wt)+'N）｜シミュラボ'; }
    else if(mode==='gomu'){ const a=r.vert?'上':'左', b=r.vert?'下':'右'; rows=[['sRead',a+'と'+b+'の水圧の差',f2(pr(r.z2)-pr(r.z1))+' N/cm²'],['sAir',a+'の膜の水圧',f2(pr(r.z1))+' N/cm²'],['sBuoy',b+'の膜の水圧',f2(pr(r.z2))+' N/cm²'],['sP','筒の中心の深さ',f1(r.cd)+' cm']];
      sh='【水圧】ゴム膜をはった筒を'+(r.vert?'縦':'横')+'向きに沈めると、'+a+'の膜'+f2(pr(r.z1))+'N/cm²・'+b+'の膜'+f2(pr(r.z2))+'N/cm²。深いほど水圧は大きく、あらゆる向きからはたらく｜シミュラボ'; }
    else { const p=function(h){ return f2(pr(wl-h))+' N/cm²'; }; rows=[['sRead','下の穴の水圧',p(2)],['sAir','上の穴の水圧',p(14)],['sBuoy','真ん中の穴の水圧',p(8)],['sP','水面の高さ（底から）',f1(wl)+' cm']];
      sh='【水圧】ペットボトルの穴：上の穴'+p(14)+'、下の穴'+p(2)+'。深いところの穴ほど水が勢いよく出る｜シミュラボ'; }
    const key=JSON.stringify(rows); if(key===statKey) return; statKey=key; rows.forEach(function(x){ setK(x[0],x[1],x[2]); }); setShare(sh); }
  function depVal(){ return mode==='bottle'?wl:(mode==='gomu'?dG:dB); }
  function setDep(v){ const sl=$('dep'), mx=+sl.max; v=clamp(v,0,mx); if(mode==='bottle') wl=v; else if(mode==='gomu') dG=v; else dB=v; sl.value=v; $('depL').textContent=f1(v)+'cm'; }
  function draw(){ ctx.fillStyle='#ffffff'; ctx.fillRect(0,0,W,H); const r=mode==='bane'?drawBane():(mode==='gomu'?drawGomu():drawBottle()); stats(r); }
  function setMode(m){ mode=m; statKey=''; const sl=$('dep');
    $('toAir').style.display=mode==='bane'?'':'none'; $('toFull').style.display=mode==='bane'?'':'none';
    fld('sz').style.display=mode==='bane'?'':'none'; fld('m').style.display=mode==='bane'?'':'none'; fld('dir').style.display=mode==='gomu'?'':'none';
    if(mode==='bottle'){ sl.max=18; lab.textContent='水面の高さ（底から）'; } else if(mode==='gomu'){ sl.max=15; lab.textContent='筒の中心の深さ'; } else { sl.max=15; lab.textContent='沈める深さ（底面）'; }
    setDep(depVal()); draw(); }
  $('mode').addEventListener('change',function(){ setMode($('mode').value); });
  $('dep').addEventListener('input',function(){ setDep(+$('dep').value); });
  $('toAir').addEventListener('click',function(){ setDep(0); });
  $('toFull').addEventListener('click',function(){ setDep(+$('sz').value+2); });
  ['sz','m','dir'].forEach(function(id){ $(id).addEventListener('input',function(){ statKey=''; }); $(id).addEventListener('change',function(){ statKey=''; }); });
  cv.addEventListener('pointerdown',function(e){ const q=cpos(cv,e), x=q[0]/dpr, y=q[1]/dpr; if(x>(mode==='bottle'?320:345)) return;
    drag={y0:y,v0:depVal()}; try{ cv.setPointerCapture(e.pointerId); }catch(err){} if(mode==='bottle') setDep((BB-y)/PB); });
  cv.addEventListener('pointermove',function(e){ if(!drag) return; const q=cpos(cv,e), y=q[1]/dpr;
    if(mode==='bottle') setDep((BB-y)/PB); else setDep(drag.v0+(y-drag.y0)/PX); });
  const up=function(){ drag=null; }; cv.addEventListener('pointerup',up); cv.addEventListener('pointercancel',up);
  function frame(ts){ const dt=last?Math.min(0.05,(ts-last)/1000):0; last=ts; tt+=dt; draw(); requestAnimationFrame(frame); }
  setMode('bane'); draw();
  requestAnimationFrame(frame);
'''

sim(slug="suiatsu-fuyuu", cat="rika", emoji="🌊", score=80,
    title="水圧と浮力のシミュレーター（ばねばかり・ゴム膜・ペットボトル）",
    title_tag="水圧と浮力のシミュレーター｜ばねばかりで浮力をはかる・深さと水圧の関係（中3理科 水中の物体に働く力）",
    meta_desc="ばねばかりにつるした物体を水に沈めると、深さとともに水圧の矢印が大きくなり、ばねばかりの値が浮力の分だけ減ります。浮力は水中にある部分の体積に比例し、全部沈むと一定。ゴム膜をはった筒、穴のあいたペットボトルの水圧の実験も。中3理科「水中の物体に働く力」向け。",
    og_title="水圧と浮力のシミュレーター（ばねばかり・ゴム膜・ペットボトル）",
    og_desc="物体を沈めるとばねばかりの値が減る＝浮力。深さと水圧の関係、浮力は体積で決まることをグラフで確かめられます。",
    card_desc="物体を沈めると、ばねばかりの値が浮力の分だけ減る。深さと水圧、浮く・沈む条件をグラフで確かめる。",
    lead="ばねばかりにつるした物体を指で水に沈めると、深いほど水圧の矢印が大きくなり、ばねばかりの値が浮力の分だけ小さくなります。大きさや質量を変えて浮力が何で決まるかを確かめ、ゴム膜をはった筒・穴のあいたペットボトルの実験にも切り替えられます。",
    model="中3 水中の物体に働く力（水圧・浮力）",
    level="中学3年",
    unit="中学校 第1分野（5）運動とエネルギー",
    canvas=canvas(640, 460, light=True),
    controls=select("mode", "実験", [("bane", "ばねばかりで浮力"), ("gomu", "ゴム膜をはった筒"), ("bottle", "穴のあいたペットボトル")])
             + select("sz", "物体の大きさ", [("4", "中 100cm³（高さ4cm）"), ("2", "小 50cm³（高さ2cm）"), ("8", "大 200cm³（高さ8cm）")])
             + slider("m", "物体の質量", 10, 500, 300, 10, "{v}g")
             + slider("dep", "沈める深さ（底面）", 0, 15, 6, 0.5, "{v}cm")
             + select("dir", "筒の向き", [("v", "縦向き（上下にゴム膜）"), ("h", "横向き（左右にゴム膜）")]),
    buttons=btn("toAir", "⤒ 水から出す") + btn("toFull", "⤓ 全部沈める"),
    stats=stats([("sRead", "ばねばかりの値", True), ("sAir", "空気中での値（重力）", False), ("sBuoy", "浮力", False), ("sP", "下面の水圧", False)]),
    legend="物体は底面5cm×5cmの直方体。青い矢印＝水圧（矢印の長さ＝水圧の大きさ。見やすいように強調しています）。100gの物体にはたらく重力を1N、水の密度を1 g/cm³として計算しています（水圧は深さ1cmごとに0.01 N/cm²）。物体を沈めても水面の高さは変わらないものとしています。",
    article=SUIATSU_ARTICLE, faqs=SUIATSU_FAQS,
    rel=[("bane-nobi", "🪀", "ばねののびと力"), ("kassha-shigoto", "🏗️", "滑車と仕事"), ("teko-tsuriai", "⚖️", "てこのつり合いシミュレーター"),
         ("kiatsu-jet", "🎢", "気圧ジェットコースター指数"), ("joutai-henka", "🧊", "状態変化と粒子のシミュレーター")],
    js=SUIATSU_JS)
