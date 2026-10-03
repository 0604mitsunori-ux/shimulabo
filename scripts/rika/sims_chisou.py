# -*- coding: utf-8 -*-
"""理科の授業向け：地層のでき方と柱状図（小6 土地のつくりと変化／中1 地層の重なりと過去の様子）と、
   火山の形と火成岩（中1 火山と地震：火山活動と火成岩）"""
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

MEXT_SHO = "https://www.mext.go.jp/a_menu/shotou/new-cs/1387014.htm"
MEXT_CHU = "https://www.mext.go.jp/a_menu/shotou/new-cs/1387016.htm"
def A(url, label): return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, label)
TEXTBOOKS = "東京書籍「新しい科学」、啓林館「未来へひろがるサイエンス」、大日本図書「理科の世界」、学校図書「中学校科学」、教育出版「自然の探究 中学理科」"


# ============================================================ 1 地層のでき方と柱状図
sim(slug="chisou", cat="rika", emoji="⛏️", score=80,
    title="地層のでき方と柱状図シミュレーター（鍵層・化石・断層・しゅう曲）",
    title_tag="柱状図・地層のでき方シミュレーター｜火山灰の鍵層・示準化石・示相化石（小6・中1理科）",
    meta_desc="海面の上下でれき・砂・泥が積もり、噴火で火山灰の層（鍵層）ができる様子を断面図で再現。4地点のボーリングの柱状図を並べ、標高をそろえて地層のつながりと傾きを読み取れます。断層・しゅう曲、示準化石・示相化石、柱状図の問題の解き方つき。",
    og_title="地層のでき方と柱状図シミュレーター（鍵層・化石・断層・しゅう曲）",
    og_desc="海の深さで積もる粒が変わり、噴火で火山灰の層ができる。4地点の柱状図を並べ、鍵層の標高から地層の傾きを読み取る小6・中1理科の教材です。",
    card_desc="海の深さで変わる粒と火山灰の層で地層ができる。4地点の柱状図を並べ、鍵層の標高から地層の傾きを読む。",
    lead="海の深さ（海面の高さ）によって積もる粒が変わり、地層が下から積み重なります。噴火で火山灰の層ができたあと大地を隆起させ、A〜Dの4地点のボーリングで柱状図を並べると、火山灰の層（鍵層）の標高から地層のつながりと傾きを読み取れます。断層・しゅう曲も試せます。",
    model="小6 土地のつくりと変化／中1 地層の重なりと過去の様子",
    level="小学6年、中学1年",
    unit="小学校 第6学年 B（4）土地のつくりと変化／中学校 第2分野（2）大地の成り立ちと変化",
    canvas=canvas(640, 648, light=True),
    controls=slider("dep", "海の深さ", 5, 100, 83, 1)
           + select("auto", "海面の動き", [("auto", "自動（例と同じ順に上下）"), ("man", "スライダーや図で動かす")])
           + slider("tilt", "隆起の傾き", -8, 8, 4, 1)
           + select("view", "柱状図のならべ方", [("depth", "地表をそろえる（深さ）"), ("elev", "標高をそろえる")]),
    buttons=btn("go", "▶ 海にもどして積もらせる", True) + btn("erupt", "🌋 噴火") + btn("fault", "↕ 断層を入れる")
           + btn("fold", "〰 しゅう曲させる") + btn("reset", "↺ はじめの例"),
    stats=stats([("sN", "地層の数", False), ("sK0", "A地点 鍵層の深さ", True), ("sK1", "B地点 鍵層の深さ", True),
                 ("sK2", "C地点 鍵層の深さ", True), ("sK3", "D地点 鍵層の深さ", True),
                 ("sTilt", "地層の傾き（100mで）", False), ("sNew", "いちばん新しい層", False)]),
    legend="上の断面図：A〜Dの印を指でドラッグするか、地面をタップすると、ボーリングする場所を変えられます。下の柱状図は西から東の順に並べ、火山灰の層①（鍵層）の上面を赤い点線でつないでいます。「▶ 海にもどして積もらせる」を押すと、海の底で地層が積もるところから見られます（海面は自動で上下します。スライダーや断面図のタップで自分で動かすこともできます）。断面図は高さを横の約2.5倍に強調しています。",
    article='''
<h2>このシミュレーションでわかること</h2>
<p>川の水に運ばれた土砂は、海の深さ（岸からの距離）に合った粒が積もり、地層は下から上へと順に重なっていきます。火山が噴火すると、火山灰の層が広い範囲にできます。陸になった土地をボーリングして<b>柱状図</b>を並べ、火山灰の層（<b>鍵層</b>）の<b>標高</b>をそろえて比べると、離れた場所の地層のつながりと<b>傾き</b>を読み取れます。</p>
<p>対応する単元は、小学校学習指導要領 理科 第6学年 B（4）「土地のつくりと変化」と、中学校学習指導要領 理科 第2分野（2）「大地の成り立ちと変化」の「地層の重なりと過去の様子」（<b>中学1年</b>）です。中学校の解説では、野外の観察記録と<b>地層が形成されるモデル実験</b>の結果を関連付けて考えることや、離れた地点の地層やボーリングコアを比べ、火山灰層などを手掛かりに地層の広がり方を調べる活動が例に挙げられています。</p>

<h2>授業での使い方</h2>
<ul>
<li><b>導入</b>：崖や切り通しの写真で、色や粒の大きさのちがう層が重なっていることを確かめます。「▶ 海にもどして積もらせる」を押し、海の底で地層ができていく様子を早送りで見せます。下の図の「この場所」が岸から遠くなると泥が、近くなるとれきが積もることに注目させます。</li>
<li><b>展開</b>：れき・砂・泥をまぜた土を水といっしょに水そうへ流しこむモデル実験のあとに使うと、実験で見た「粒の大きいものから先にしずむ」ことと、海で長い年月をかけて地層ができることを結び付けられます。隆起したあとは、A〜Dの柱状図を「地表をそろえる」で比べてから「標高をそろえる」に切りかえ、火山灰の層の高さが東ほど低いこと（地層の傾き）を見つけます。</li>
<li><b>まとめ</b>：下の例題で柱状図の読み取りを練習し、ボーリングの印を動かして答えを確かめます。「断層」「しゅう曲」を押して、大地に力がはたらいたときの地層の変化も見ておきます。</li>
</ul>
<p>児童・生徒への問いの例：</p>
<ol>
<li>下から「れき → 砂 → 泥」の順に重なっている地層ができた間に、その場所の海の深さはどう変わったと考えられるでしょうか。</li>
<li>火山灰の層が、離れた場所の地層を比べる手がかりになるのはなぜでしょうか。</li>
<li>4地点の柱状図で、火山灰の層の深さがそろわないのはなぜでしょうか（地表の標高と、地層の傾きの2つから考えましょう）。</li>
</ol>

<h2>しくみ・解説</h2>
<h3>地層のでき方（流れる水の働き）</h3>
<p>川の水に運ばれた土砂は、海や湖に流れこむと流れがゆるやかになり、底に積もります（堆積）。粒が大きく重いものほど早くしずむので、岸の近くには<b>れき</b>、少しはなれた所には<b>砂</b>、沖の深い所には<b>泥</b>（どろ）が積もります。粒は大きさで次のように区別します。</p>
''' + T([["れき", "直径2mm以上", "れき岩"],
          ["砂", "直径2mm〜約0.06mm（1/16mm）", "砂岩"],
          ["泥", "直径約0.06mm（1/16mm）以下", "泥岩"],
          ["火山灰", "火山の噴火でふき出された細かい粒", "凝灰岩"]],
         ["粒", "大きさ", "固まってできる岩石（堆積岩）"]) + '''
<p>このほか、生物の死がいなどが積もってできた石灰岩やチャートもあります。海面が上がったり土地がしずんだりして、ある場所の海が深くなる（岸から遠くなる）と、積もる粒は小さくなります。浅くなると、その反対です。地層はふつう、下にあるものほど古く、上にあるものほど新しいので、下から上への粒の大きさの変化から、その場所の海の深さの移り変わりが分かります。</p>
<h3>火山灰の層と鍵層</h3>
<p>火山が噴火すると、火山灰は風に運ばれて広い範囲に、ほぼ同じ時期に降り積もります。そのため、離れた場所の地層に同じ火山灰の層があれば、その層は同じ時期にできたと考えられます。このように、地層を比べる手がかりになる層を<b>鍵層</b>（かぎ層）といいます。火山灰の層のほか、決まった化石をふくむ層も鍵層になります。</p>
<p>砂や泥の層は、同じ時期にできた層でも、岸に近い所では砂、遠い所では泥のように、場所によって粒が変わることがあります。粒の種類だけで層をつなぐとまちがえることがあるので、鍵層を手がかりにします。</p>
<h3>柱状図の読み取り方（例題）</h3>
<p><b>柱状図</b>は、ある地点の地層の重なり方を、柱のような図で表したものです。ボーリング調査で地下の土や岩石を取り出し（ボーリングコア）、地表からの深さごとに記録します。離れた地点の柱状図を比べるときは、<b>深さではなく標高をそろえる</b>のがポイントです。</p>
''' + N("鍵層の上面の標高［m］＝ 地点の標高［m］− 地表から鍵層の上面までの深さ［m］") + '''
<p><b>例題1</b>　西から東へ一直線に、100mずつはなれて並んだA〜Dの4地点でボーリング調査をしました。各地点の標高と、火山灰の層の上面の深さは次のとおりです。</p>
''' + T([["A", "60m", "10m"], ["B（Aの東100m）", "70m", "24m"], ["C（Bの東100m）", "55m", "13m"], ["D（Cの東100m）", "65m", "27m"]],
         ["地点", "地表の標高", "火山灰の層の上面の深さ"]) + '''
<p>（1）各地点の火山灰の層の上面の標高を求めなさい。<br>
→ A：60−10＝50m、B：70−24＝46m、C：55−13＝42m、D：65−27＝38m　答え <b>A 50m、B 46m、C 42m、D 38m</b></p>
<p>（2）この地域の地層は、どの方位に向かって低くなるように傾いていますか。また、100mにつき何m低くなっていますか。<br>
→ 東へ100m進むごとに、火山灰の層の上面の標高が4mずつ低くなっています。　答え <b>東、4m</b></p>
<p>（3）A地点の東50mにあるE地点（標高66m）では、火山灰の層の上面は地表から何mの深さにあると考えられますか。<br>
→ Aから東へ50mなので、火山灰の層の上面の標高は 50−2＝48m。66−48＝18。　答え <b>18m</b></p>
''' + P("シミュレーターの初期状態（↺ はじめの例）のA〜D地点が、例題1と同じです。柱状図を「標高をそろえる」にすると、火山灰の層①をつなぐ赤い点線が右下がり（東が低い）になります。ボーリングの印を西から100mの位置（AとBの間）に動かすと、例題1（3）の答え（18m）を確かめられます。") + '''
<p><b>例題2</b>　地図の上で、B地点はA地点の真北300m、C地点はA地点の真東300mにあります。標高と火山灰の層の上面の深さは、A（標高80m・深さ20m）、B（標高85m・深さ25m）、C（標高75m・深さ21m）でした。（1）地層はどの方位に低くなるように傾いていますか。（2）A地点の真南200mにあるD地点（標高72m）では、火山灰の層の上面は地表から何mの深さにありますか。<br>
→ 火山灰の層の上面の標高は、A：60m、B：60m、C：54m。南北方向（AとB）は同じ高さなので傾いておらず、東西方向（AとC）は東が6m低くなっています。　答え（1）<b>東</b><br>
→ DはAの真南で、南北方向には傾いていないので、火山灰の層の上面の標高はAと同じ60m。72−60＝12。　答え（2）<b>12m</b></p>
<p><b>例題3</b>　ある地点の地層は、下から「れき岩 → 砂岩 → 泥岩」の順に重なっていて、れき岩の層からシジミの化石が見つかりました。（1）この地層ができた間に、この場所の海の深さはどう変わったと考えられますか。（2）れき岩の層ができたころ、この場所はどのような環境だったと考えられますか。<br>
→ 上の層ほど粒が小さいので、海がだんだん深くなった（岸から遠くなった）と考えられます。シジミは河口や湖など、海水と淡水がまじる所にすむので、河口の近くだったと考えられます。　答え（1）<b>だんだん深くなった</b>（2）<b>河口や湖のような、海水と淡水がまじる所</b></p>
<h3>化石からわかること（示相化石・示準化石）</h3>
<p>地層の中の化石からは、その地層ができた当時の環境や、地層ができた時代が分かります。当時の<b>環境</b>を示す化石を<b>示相化石</b>、地層ができた<b>時代</b>を示す化石を<b>示準化石</b>といいます。</p>
''' + T([["サンゴ", "あたたかくて浅い海"], ["アサリ・ハマグリ", "浅い海（岸の近く）"], ["シジミ", "河口や湖（海水と淡水がまじる所）"],
          ["ホタテガイ", "冷たい浅い海"], ["ブナ（の葉）", "やや寒い気候の陸地"]],
         ["示相化石の例", "地層ができた当時の環境"]) + T([
          ["古生代（約5億4000万年前〜約2億5200万年前）", "三葉虫、フズリナ"],
          ["中生代（約2億5200万年前〜約6600万年前）", "アンモナイト、恐竜"],
          ["新生代（約6600万年前〜現在）", "ビカリア、ナウマンゾウ"]],
         ["地質年代", "示準化石の例"]) + '''
<p>示準化石には、広い範囲にすんでいて、短い期間だけ栄えて絶滅した生物の化石が適しています。地球の歴史は、地層や化石をもとに、古生代・中生代・新生代などの<b>地質年代</b>に区分されています。</p>
<p>シミュレーターでは、浅い海（河口付近）で積もったれきの層にシジミの化石を、いちばん下の砂の層にビカリアの化石を入れています。柱状図に化石の印が出るので、例題3のように「その層ができたときの環境や時代」を考える材料に使えます（化石の種類と位置は説明のための例です）。</p>
<h3>断層・しゅう曲・隆起</h3>
<p>地層に大きな力がはたらくと、地層が切れてずれたり（<b>断層</b>）、波打つように曲がったり（<b>しゅう曲</b>）します。断層のうち、両側から引っぱる力がはたらいて、断層面の上側の地層がずり下がったものを<b>正断層</b>、両側からおす力がはたらいて、上側の地層がずり上がったものを<b>逆断層</b>といいます。しゅう曲は、主に両側からおす力でできます。海の底でできた地層が陸で見られるのは、大地が持ち上げられたから（<b>隆起</b>）です。</p>
<p>断層がすべての地層をずらしていれば、その断層は、いちばん上の地層が積もったあとにできたと考えられます。シミュレーターの断層は西にかたむいた断層面で、西側（断層面の上側）の地層が6mずれます。</p>
''' + N("<b>このシミュレーターで単純化している点</b><br>"
        "・断面図は、高さを横の約2.5倍に強調しています。海の深さは「浅い・やや深い・深い」の目安で、実際の深さ（m）とは対応していません。<br>"
        "・積もる速さはどの粒も同じとし、時間を大きく早送りしています。実際には、厚い地層ができるには長い年月がかかり、積もる速さも場所や粒によって大きくちがいます。<br>"
        "・1つの層は、その時の海の深さに合った1種類の粒でできていて、断面の左右で変わらないものとしています（実際には、同じ時期の層でも場所によって粒が変わることがあります）。<br>"
        "・隆起のときは、断面全体が同じ傾きで持ち上がるものとしています。地表の形（丘や谷）、ボーリングの深さ（35m）、断層のずれ（6m）、しゅう曲の大きさ（上下7m）は、説明のために決めた値です。<br>"
        "・化石の種類と位置は、説明のための例です。") + '''
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「小学校学習指導要領（平成29年告示）解説 理科編」第6学年 B（4）土地のつくりと変化（''' + A(MEXT_SHO, "小学校学習指導要領解説") + '''）</li>
<li>文部科学省「中学校学習指導要領（平成29年告示）解説 理科編」第2分野（2）大地の成り立ちと変化（''' + A(MEXT_CHU, "中学校学習指導要領解説") + '''）</li>
<li>小学校理科の教科書の第6学年「土地のつくりと変化」、中学校理科の教科書（''' + TEXTBOOKS + '''）の第1学年「大地の成り立ちと変化」の単元</li>
<li>国際層序委員会（ICS）「国際年代層序表」（地質年代の区分と年代）</li>
</ul>
''',
    faqs=[("柱状図とは何ですか？", "ボーリング調査などで調べた、ある地点の地層の重なり方を、地表からの深さにそって柱の形に表した図です。離れた地点の柱状図を並べ、火山灰の層などの鍵層の標高をそろえて比べると、地層のつながりや傾きが分かります。"),
          ("鍵層とは何ですか？", "離れた場所の地層を比べるときの手がかりになる層です。火山灰の層は、噴火のときに広い範囲にほぼ同時に降り積もるので、代表的な鍵層です。決まった化石をふくむ層が鍵層になることもあります。"),
          ("柱状図から地層の傾きはどう求めますか？", "各地点で「地点の標高−鍵層までの深さ」を計算して鍵層の標高を求め、比べます。標高が低い方へ地層が傾いています。たとえばA地点（標高60m・深さ10m）の鍵層は50m、その東100mのB地点（標高70m・深さ24m）は46mなので、東へ100mにつき4m低くなっています。"),
          ("示相化石と示準化石のちがいは何ですか？", "示相化石は地層ができた当時の環境を示す化石（サンゴ→あたたかくて浅い海、シジミ→河口や湖など）、示準化石は地層ができた時代を示す化石（三葉虫→古生代、アンモナイト→中生代、ビカリア→新生代など）です。"),
          ("地層の粒の大きさから何が分かりますか？", "その層が積もったときの海の深さ（岸からの距離）が分かります。粒の大きいれきは岸の近くの浅い所、泥は沖の深い所に積もります。下から上へ「れき→砂→泥」と粒が小さくなっていれば、その場所の海がだんだん深くなったと考えられます。"),
          ("断層としゅう曲は、どんな力でできますか？", "どちらも地層に大きな力がはたらいてできます。両側から引っぱる力では正断層、両側からおす力では逆断層ができます。しゅう曲は、主に両側からおす力で地層が波打つように曲がったものです。")],
    rel=[("jishin-ha", "📳", "地震の伝わり方シミュレーター"), ("kazan-kaseigan", "🌋", "火山の形と火成岩"),
         ("tsunami-kishi", "🌊", "津波はなぜ岸で高くなる？"), ("kaibatsu-check", "⛰️", "うちの海抜チェッカー"),
         ("chikyu-yure", "🌐", "地球まるごと地震カウンター")],
    js=r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  cv.setAttribute('role','img'); cv.setAttribute('aria-label','海の底で地層が積もる断面図と、4地点のボーリングの柱状図');
  cv.style.cursor='pointer';
  const SX0=46, SX1=628, XW=400, SY0=28, SY1=282, Z0=18, Z1=87, BD=35, ZBS=18.5, RATE=3, TMAX=48, MARGIN=4;
  const XF=200, ZF=75, TANF=Math.tan(Math.PI/3);
  const HP=[57,60,66,70,64,55,59,65,62];
  const SCRIPT=[['g',3],['s',5],['m',6],['a',1],['m',5],['s',7],['g',4],['s',6],['m',10]];
  const ZCEN={g:17,s:50,m:83}, ZN={g:'浅い',s:'やや深い',m:'深い'};
  const TY={g:{n:'れき',c:'#f2d3a7',d:'#9a5b13'},s:{n:'砂',c:'#fbecb2',d:'#a16207'},m:{n:'泥',c:'#cbd5e1',d:'#475569'},a:{n:'火山灰',c:'#fdeef5',d:'#be185d'}};
  const CIR=['①','②','③','④','⑤','⑥','⑦','⑧','⑨','⑩'];
  const DEFB=[50,150,250,350], NAMES=['A','B','C','D'];
  const CT=304, CY0=362, CY1=606, CXS=[96,196,296,396], CW=50, RX=446;
  const xp=(x)=>SX0+x/XW*(SX1-SX0), zp=(z)=>SY1-(z-Z0)/(Z1-Z0)*(SY1-SY0), xm=(px)=>(px-SX0)/(SX1-SX0)*XW;
  const PXM=(SY1-SY0)/(Z1-Z0);
  const ease=(t)=>t<=0?0:(t>=1?1:t*t*(3-2*t));
  const f1=(v)=>(Math.round(v*10)/10).toFixed(1);
  const line=(a,b,c,d)=>{ ctx.beginPath(); ctx.moveTo(a,b); ctx.lineTo(c,d); ctx.stroke(); };
  function txt(s,x,y,font,col,al,halo){ ctx.font=font; ctx.textAlign=al||'left'; if(halo){ ctx.lineJoin='round'; ctx.lineWidth=3.5; ctx.strokeStyle='rgba(255,255,255,.95)'; ctx.strokeText(s,x,y); } ctx.fillStyle=col; ctx.fillText(s,x,y); }
  function tw(s,font){ ctx.font=font; return ctx.measureText(s).width; }
  function rr(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.lineTo(x+w-r,y); ctx.quadraticCurveTo(x+w,y,x+w,y+r); ctx.lineTo(x+w,y+h-r); ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h); ctx.lineTo(x+r,y+h); ctx.quadraticCurveTo(x,y+h,x,y+h-r); ctx.lineTo(x,y+r); ctx.quadraticCurveTo(x,y,x+r,y); ctx.closePath(); }
  function arrow(x1,y1,x2,y2,col,lw){ ctx.strokeStyle=col; ctx.fillStyle=col; ctx.lineWidth=lw; line(x1,y1,x2,y2); const a=Math.atan2(y2-y1,x2-x1), h=6+lw; ctx.beginPath(); ctx.moveTo(x2+Math.cos(a)*2,y2+Math.sin(a)*2); ctx.lineTo(x2-h*Math.cos(a-0.5),y2-h*Math.sin(a-0.5)); ctx.lineTo(x2-h*Math.cos(a+0.5),y2-h*Math.sin(a+0.5)); ctx.closePath(); ctx.fill(); }
  function wrap(s,x,y,mw,lh,font,col){ ctx.font=font; let cur='', yy=y; for(const ch of s){ ctx.font=font; if(ctx.measureText(cur+ch).width>mw && cur){ txt(cur,x,yy,font,col); cur=ch; yy+=lh; } else cur+=ch; } if(cur) txt(cur,x,yy,font,col); return yy; }
  function Hx(x){ x=clamp(x,0,400); const i=Math.min(7,Math.floor(x/50)), t=(x-i*50)/50, p0=HP[Math.max(0,i-1)], p1=HP[i], p2=HP[i+1], p3=HP[Math.min(8,i+2)];
    return 0.5*(2*p1+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t); }
  // ---- 状態 ----
  let L=[], BOT=[0], phase='land', k=-0.04, U=29, fA=0, fAT=0, fS=0, fST=0, fType=0, lastF='', lift=1, ero=1, drill=1;
  let si=0, rem=0, ashQ=0, ashCur=null, endT=0, erupt=0, depositing=false, msg='', msgT=0, tm=0, sel=0, dragging='', dirty=true, last=performance.now();
  let B=DEFB.map((x,i)=>({n:NAMES[i],x:x}));
  function rebot(){ BOT=[0]; L.forEach((l)=>{ BOT.push(BOT[BOT.length-1]+l.th); }); }
  const TT=()=>BOT[BOT.length-1];
  const curTop=()=>(L.length?L[L.length-1]:null);
  const zone=(d)=>d<33.4?'g':(d<66.7?'s':'m');
  function newLayer(t){ const f=t==='g'?'shijimi':((t==='s'&&!L.some((l)=>l.f==='vicarya'))?'vicarya':''); L.push({t:t,th:0,f:f,done:false}); rebot(); return L[L.length-1]; }
  // ---- 地層の形（隆起・傾き・しゅう曲・断層） ----
  function gm(){ if(phase==='sea') return [ZBS,0]; if(phase==='lift'){ const e=ease(lift); return [ZBS+(U-ZBS)*e,k*e]; } return [U,k]; }
  const foldz=(x)=>fA*Math.cos(2*Math.PI*(x-125)/300);
  const hasF=()=>fType!==0||Math.abs(fS)>1e-6;
  const zc=(x)=>ZF-(XF-x)*TANF;
  function base(x,hw){ const g=gm(); return g[0]+g[1]*(x-200)+foldz(x)+(hw?fS:0); }
  function topMat(x){ const t=TT(), zf=base(x,false)+t; if(!hasF()) return zf; const c=zc(x), zh=base(x,true)+t; return zh>c?zh:Math.min(c,zf); }
  function G(x){ const tg=topMat(x); if(phase==='sea'||phase==='lift') return tg; const gl=Math.min(Hx(x),tg-0.3); return phase==='erode'?tg+(gl-tg)*ease(ero):gl; }
  function calcU(){ const t=TT(); let mx=-1e9; for(let x=0;x<=400;x++) mx=Math.max(mx,Hx(x)-t-k*(x-200)); return Math.ceil(mx+MARGIN); }
  function blocks(x){ return hasF()?[[false,-1e9,zc(x)],[true,zc(x),1e9]]:[[false,-1e9,1e9]]; }
  function column(x){ const g=G(x), lo=g-BD, iv=[];
    blocks(x).forEach((bk)=>{ const b=base(x,bk[0]), a=Math.max(lo,bk[1]), c=Math.min(g,bk[2]); if(c<=a) return;
      if(b>a) iv.push({i:-1,top:Math.min(b,c),bot:a});
      for(let i=0;i<L.length;i++){ const t=Math.min(b+BOT[i+1],c), bt=Math.max(b+BOT[i],a); if(t>bt+1e-6) iv.push({i:i,top:t,bot:bt}); } });
    iv.sort((p,q)=>q.top-p.top); return {g:g,iv:iv}; }
  const ashIdx=()=>L.findIndex((l)=>l.t==='a');
  function ashAt(x,col){ const ia=ashIdx(); if(ia<0) return {s:'none'}; const hit=col.iv.find((v)=>v.i===ia); if(hit) return {s:'ok',d:col.g-hit.top,z:hit.top};
    let up=false; blocks(x).forEach((bk)=>{ const b=base(x,bk[0]), zb=b+BOT[ia], zt=b+BOT[ia+1]; if(zt>bk[1]&&zb<bk[2]&&zb>=col.g-1e-6) up=true; }); return {s:up?'cut':'deep'}; }
  function tiltRead(list){ const q=list.filter((o)=>o.a.s==='ok'); if(q.length<2) return null; let mx=0, mz=0; q.forEach((o)=>{ mx+=o.x/q.length; mz+=o.a.z/q.length; }); let sxx=0, sxz=0; q.forEach((o)=>{ sxx+=(o.x-mx)*(o.x-mx); sxz+=(o.x-mx)*(o.a.z-mz); }); return sxx<1?null:sxz/sxx*100; }
  function surfLayer(x){ const g=G(x)-0.02, hw=hasF()&&g>zc(x), zr=g-base(x,hw); if(zr<0) return -1; for(let i=L.length-1;i>=0;i--){ if(zr>=BOT[i]) return i; } return -1; }
  function youngest(){ let m=-1; for(let x=0;x<=400;x+=4) m=Math.max(m,surfLayer(x)); return m; }
  const sorted=()=>B.map((b,i)=>i).sort((a,b)=>B[a].x-B[b].x);
  // ---- 模様（柱状図の記号）と化石 ----
  const PS=(typeof DOMMatrix!=='undefined'&&window.CanvasPattern&&CanvasPattern.prototype.setTransform)?2:1;
  function mkPat(kind){ const w=kind==='g'?22:(kind==='b'?12:14), h=kind==='g'?18:(kind==='b'?12:10); const c=document.createElement('canvas'); c.width=w*PS; c.height=h*PS; const g=c.getContext('2d'); g.scale(PS,PS);
    if(kind==='b'){ g.fillStyle='#a8a29e'; g.fillRect(0,0,w,h); g.strokeStyle='#78716c'; g.lineWidth=1; g.beginPath(); g.moveTo(0,h); g.lineTo(w,0); g.moveTo(-w/2,h/2); g.lineTo(w/2,-h/2); g.moveTo(w/2,h*1.5); g.lineTo(w*1.5,h/2); g.stroke(); }
    else { const q=TY[kind]; g.fillStyle=q.c; g.fillRect(0,0,w,h); g.strokeStyle=q.d; g.fillStyle=q.d;
      if(kind==='g'){ g.lineWidth=0.9; const C=[[5,5,2.8],[14,5,1.8],[18,13,2.5],[9,13,1.7],[2,15,1.2]]; C.forEach((o)=>{ g.beginPath(); g.arc(o[0],o[1],o[2],0,Math.PI*2); g.stroke(); }); }
      else if(kind==='s'){ const C=[[2,2],[7,4],[11,1.5],[4,7],[10,8],[13,5.5],[1,9]]; C.forEach((o)=>{ g.beginPath(); g.arc(o[0],o[1],0.75,0,Math.PI*2); g.fill(); }); }
      else if(kind==='m'){ g.lineWidth=0.9; g.beginPath(); g.moveTo(1,3); g.lineTo(6,3); g.moveTo(8,8); g.lineTo(13,8); g.stroke(); }
      else { g.lineWidth=1; g.beginPath(); g.moveTo(2,2); g.lineTo(4,6); g.lineTo(6,2); g.moveTo(9,5); g.lineTo(11,9); g.lineTo(13,5); g.stroke(); } }
    const pt=ctx.createPattern(c,'repeat'); if(PS===2&&pt&&pt.setTransform) pt.setTransform(new DOMMatrix([0.5,0,0,0.5,0,0])); return pt; }
  const PAT={g:mkPat('g'),s:mkPat('s'),m:mkPat('m'),a:mkPat('a'),b:mkPat('b')};
  function shijimi(x,y,s){ ctx.save(); ctx.translate(x,y); ctx.scale(s,s); ctx.beginPath(); ctx.moveTo(-6.5,2.5); ctx.quadraticCurveTo(-6.5,-4.5,0,-6.5); ctx.quadraticCurveTo(6.5,-4.5,6.5,2.5); ctx.quadraticCurveTo(0,6.5,-6.5,2.5); ctx.closePath(); ctx.fillStyle='#4a3424'; ctx.fill(); ctx.strokeStyle='#e7d3b4'; ctx.lineWidth=0.8;
    for(let r=1;r<=2;r++){ ctx.beginPath(); ctx.moveTo(-6.5+r*2,2.3-r*0.5); ctx.quadraticCurveTo(0,6.2-r*2.6,6.5-r*2,2.3-r*0.5); ctx.stroke(); } ctx.restore(); }
  function vicarya(x,y,s){ ctx.save(); ctx.translate(x,y); ctx.rotate(-0.6); ctx.scale(s,s); ctx.beginPath(); ctx.moveTo(0,-10); ctx.lineTo(4.6,4); ctx.quadraticCurveTo(0,8.5,-4.6,4); ctx.closePath(); ctx.fillStyle='#d6b47e'; ctx.fill(); ctx.strokeStyle='#7c5a2c'; ctx.lineWidth=0.9; ctx.stroke();
    for(let j=0;j<4;j++){ const yy=-6.2+j*3.2, hw=1.2+j*0.95; ctx.beginPath(); ctx.moveTo(-hw,yy); ctx.lineTo(hw,yy+0.9); ctx.stroke(); ctx.beginPath(); ctx.arc(hw-0.3,yy+0.5,0.8,0,Math.PI*2); ctx.fillStyle='#7c5a2c'; ctx.fill(); } ctx.restore(); }
  function fossil(f,x,y,s){ if(f==='shijimi') shijimi(x,y,s); else if(f==='vicarya') vicarya(x,y,s); }
  // ---- 断面図 ----
  function bandPath(lo,hi){ ctx.beginPath(); for(let x=-8;x<=408;x+=4){ const X=xp(x), Y=zp(hi(x)); if(x===-8) ctx.moveTo(X,Y); else ctx.lineTo(X,Y); } for(let x=408;x>=-8;x-=4) ctx.lineTo(xp(x),zp(lo(x))); ctx.closePath(); }
  function faultClip(hw){ const za=Z0-40, zb=Z1+40, xa=xp(XF-(ZF-za)/TANF), xb=xp(XF-(ZF-zb)/TANF), ya=zp(za), yb=zp(zb), ex=hw?SX0-90:SX1+90;
    ctx.beginPath(); ctx.moveTo(ex,yb); ctx.lineTo(xb,yb); ctx.lineTo(xa,ya); ctx.lineTo(ex,ya); ctx.closePath(); ctx.clip(); }
  function drawStrata(){ const bl=hasF()?[false,true]:[false];
    bl.forEach((hw)=>{ ctx.save(); if(hasF()) faultClip(hw);
      bandPath(()=>Z0-60,(x)=>base(x,hw)); ctx.fillStyle=PAT.b; ctx.fill();
      for(let i=0;i<L.length;i++){ if(L[i].th<=0.001) continue; bandPath((x)=>base(x,hw)+BOT[i],(x)=>base(x,hw)+BOT[i+1]); ctx.fillStyle=PAT[L[i].t]; ctx.fill(); }
      ctx.strokeStyle='rgba(30,41,59,.55)'; ctx.lineWidth=0.9;
      for(let i=0;i<=L.length;i++){ ctx.beginPath(); for(let x=-8;x<=408;x+=4){ const X=xp(x), Y=zp(base(x,hw)+BOT[i]); if(x===-8) ctx.moveTo(X,Y); else ctx.lineTo(X,Y); } ctx.stroke(); }
      ctx.restore(); }); }
  function clipGround(){ ctx.beginPath(); ctx.moveTo(SX0-4,SY1+60); for(let x=0;x<=400;x+=2) ctx.lineTo(xp(x),zp(G(x))); ctx.lineTo(SX1+4,SY1+60); ctx.closePath(); ctx.clip(); }
  function drawGround(){ ctx.beginPath(); for(let x=0;x<=400;x+=2){ const X=xp(x), Y=zp(G(x)); if(x===0) ctx.moveTo(X,Y); else ctx.lineTo(X,Y); } ctx.strokeStyle='#4d7c0f'; ctx.lineWidth=3.5; ctx.stroke(); }
  function drawFossils(){ const land=phase==='land'||phase==='erode';
    L.forEach((l,i)=>{ if(!l.f) return; const hpx=l.th*PXM; if(hpx<10) return; const mid=(BOT[i]+BOT[i+1])/2;
      for(let j=0;j<4;j++){ const x=((i*53+j*97+31)%372)+14;
        blocks(x).forEach((bk)=>{ const z=base(x,bk[0])+mid; if(z<=bk[1]||z>=bk[2]) return; if(land&&z>G(x)-1.2) return; const Y=zp(z); if(Y<SY0+8||Y>SY1-8) return; fossil(l.f,xp(x),Y,hpx<16?0.75:0.95); }); } }); }
  function drawFault(){ if(!hasF()) return; const xa=XF-(ZF-(Z0-30))/TANF, xb=XF-(ZF-(Z1+30))/TANF;
    ctx.save(); clipGround(); ctx.strokeStyle='#dc2626'; ctx.lineWidth=2.6; line(xp(xa),zp(Z0-30),xp(xb),zp(Z1+30));
    let zt=Z0; for(let x=100;x<=300;x+=1){ if(zc(x)>=G(x)){ zt=G(x); break; } }
    const zmid=(zt+Z0)/2, X=xp(XF-(ZF-zmid)/TANF), Y=zp(zmid), dx=xp(xb)-xp(xa), dy=zp(Z1+30)-zp(Z0-30), ln=Math.hypot(dx,dy), ux=dx/ln, uy=dy/ln, nx=-uy, ny=ux, sh=fS<0?-1:1;
    arrow(X-nx*11-ux*9*sh,Y-ny*11-uy*9*sh,X-nx*11+ux*9*sh,Y-ny*11+uy*9*sh,'#b91c1c',2);
    arrow(X+nx*11+ux*9*sh,Y+ny*11+uy*9*sh,X+nx*11-ux*9*sh,Y+ny*11-uy*9*sh,'#b91c1c',2);
    ctx.restore();
    const lb=fS<-1e-6?'正断層':(fS>1e-6?'逆断層':''); if(lb) txt(lb,xp(XF-(ZF-zt)/TANF)+9,zp(zt)+17,'bold 12px sans-serif','#b91c1c','left',true); }
  function drawForce(){ if(!lastF) return; const y=SY1-28;
    if(lastF==='pull'){ arrow(SX0+44,y,SX0+8,y,'#7c3aed',3); arrow(SX1-44,y,SX1-8,y,'#7c3aed',3); txt('引っぱる力',SX0+50,y+4,'bold 12px sans-serif','#6d28d9','left',true); }
    else { arrow(SX0+6,y,SX0+42,y,'#7c3aed',3); arrow(SX1-6,y,SX1-42,y,'#7c3aed',3); txt('おす力',SX0+48,y+4,'bold 12px sans-serif','#6d28d9','left',true); } }
  function ashLabel(){ const ia=ashIdx(); if(ia<0) return; for(let pass=0;pass<2;pass++) for(let x=392;x>=16;x-=6){ if(pass===0&&B.some((b)=>b.x>x-76&&b.x<x+6)) continue; let z=null; blocks(x).forEach((bk)=>{ const zt=base(x,bk[0])+BOT[ia+1]; if(zt>bk[1]&&zt<bk[2]) z=zt; });
      if(z!==null&&z<G(x)-4&&z>Z0+3){ txt('火山灰の層（鍵層）',xp(x),zp(z)-5,'bold 11px sans-serif','#9d174d','right',true); return; } } }
  function drawBorings(){ B.forEach((b,i)=>{ const X=xp(b.x), g=G(b.x), Y=zp(g), on=i===sel, dd=phase==='land'?drill:0;
      if(dd>0){ const yb=Math.min(SY1,zp(g-BD*dd)); ctx.fillStyle='rgba(255,255,255,.55)'; ctx.fillRect(X-3,Y,6,yb-Y); ctx.strokeStyle=on?'#f59e0b':'#1e293b'; ctx.lineWidth=on?2.2:1.2; ctx.strokeRect(X-3,Y,6,yb-Y); }
      ctx.strokeStyle=on?'#d97706':'#334155'; ctx.lineWidth=on?2.4:1.6; ctx.beginPath(); ctx.moveTo(X-8,Y); ctx.lineTo(X,Y-17); ctx.lineTo(X+8,Y); ctx.stroke(); line(X,Y-17,X,Y);
      txt(b.n,X-2,Y-22,'bold 15px sans-serif',on?'#b45309':'#0f172a','right',true); txt(f1(g)+'m',X,Y-22,'11px sans-serif','#334155','left',true); }); }
  function seaY(){ const dpx=10+0.5*(+$('dep').value); if(phase==='sea') return zp(base(200,false)+TT())-dpx; if(phase==='lift'){ const y0=zp(ZBS+TT())-dpx, e=ease(Math.min(1,lift*1.7)); return y0+(SY1+60-y0)*e; } return SY1+100; }
  function drawFall(sy,ty){ const top=curTop(); if(!top||top.t==='a'||ty-sy<14) return; const t=top.t, n=t==='g'?16:(t==='s'?30:44), sz=t==='g'?2.6:(t==='s'?1.4:0.9), sp=t==='g'?0.95:(t==='s'?0.6:0.32);
    ctx.fillStyle=TY[t].d; for(let i=0;i<n;i++){ const fx=(i*0.6180339)%1, q=(tm*sp+i*0.377)%1, X=SX0+10+fx*(SX1-SX0-60)+Math.sin(tm*1.3+i)*3, Y=sy+6+q*(ty-sy-10); ctx.globalAlpha=0.3+0.6*Math.min(1,q*3); ctx.beginPath(); ctx.arc(X,Y,t==='g'?sz*(0.7+0.6*((i*0.37)%1)):sz,0,Math.PI*2); ctx.fill(); } ctx.globalAlpha=1; }
  function drawSeaTop(sy){ ctx.strokeStyle='rgba(255,255,255,.9)'; ctx.lineWidth=2; ctx.beginPath(); for(let X=SX0;X<=SX1;X+=4){ const Y=sy+Math.sin(X*0.09+tm*2.2)*1.6; if(X===SX0) ctx.moveTo(X,Y); else ctx.lineTo(X,Y); } ctx.stroke(); txt('海面',SX0+8,sy-6,'bold 12px sans-serif','#0369a1','left',true); }
  function drawSeaInfo(sy,ty){ const z=zone(+$('dep').value), bx=SX1-22;
    if(depositing) drawFall(sy,ty);
    ctx.strokeStyle='#0f172a'; ctx.lineWidth=1.4; line(bx,sy+3,bx,ty-2); line(bx-5,sy+3,bx+5,sy+3); line(bx-5,ty-2,bx+5,ty-2);
    txt('海の深さ：'+ZN[z],bx-8,(sy+ty)/2+5,'bold 13px sans-serif','#0f172a','right',true);
    let an=0; L.forEach((l,i)=>{ if(l.t==='a') an++; const Y=zp(ZBS+(BOT[i]+BOT[i+1])/2)+4;
      if(l.t==='a') txt('火山灰の層'+CIR[Math.min(9,an-1)],xp(150),Y,'bold 11px sans-serif','#9d174d','left',true);
      else if(l.th*PXM>=11) txt(TY[l.t].n,xp(150),Y,'bold 11px sans-serif','#1e293b','left',true); });
    const top=curTop(); let s=''; if(ashCur||ashQ>0) s='火山灰が積もっている'; else if(depositing&&top) s=TY[top.t].n+'が積もっている'; else if($('auto').value==='auto') s='海の深さが変わっていく…';
    if(s) txt(s,xp(262),ty-8,'bold 13px sans-serif','#0f172a','center',true);
    if(L.length&&SY1-ty>52){ arrow(SX0+14,SY1-8,SX0+14,ty+8,'#334155',1.5); txt('上ほど新しい',SX0+22,ty+18,'11px sans-serif','#1e293b','left',true); txt('下ほど古い',SX0+22,SY1-8,'11px sans-serif','#1e293b','left',true); } }
  function drawAshFall(ty){ const a=Math.min(1,erupt/0.5), yb=phase==='land'?SY1:ty; ctx.fillStyle='rgba(87,83,78,'+(0.65*a).toFixed(2)+')';
    for(let i=0;i<110;i++){ const fx=(i*0.6180339)%1, q=(tm*0.45+i*0.173)%1, X=SX0+fx*(SX1-SX0)+Math.sin(tm+i)*5, Y=SY0+q*(yb-SY0); ctx.beginPath(); ctx.arc(X,Y,1.2,0,Math.PI*2); ctx.fill(); }
    const s='火山の噴火：火山灰が広い範囲に降り積もる', w=tw(s,'bold 12px sans-serif')+20; ctx.globalAlpha=a; ctx.fillStyle='#7f1d1d'; rr((SX0+SX1-w)/2,SY0+6,w,22,6); ctx.fill(); txt(s,(SX0+SX1)/2,SY0+21,'bold 12px sans-serif','#fff','center'); ctx.globalAlpha=1; }
  function drawToast(){ if(msgT<=0||!msg) return; ctx.save(); ctx.globalAlpha=Math.min(1,msgT/0.4); ctx.font='bold 12px sans-serif'; const ls=[]; let cur='';
    for(const ch of msg){ if(ctx.measureText(cur+ch).width>500&&cur){ ls.push(cur); cur=ch; } else cur+=ch; } if(cur) ls.push(cur);
    ctx.fillStyle='rgba(15,23,42,.9)'; rr(60,SY0+40,520,ls.length*18+14,8); ctx.fill(); ls.forEach((s,i)=>{ txt(s,320,SY0+59+i*18,'bold 12px sans-serif','#fff','center'); }); ctx.restore(); }
  function drawSection(){ const land=phase==='land'||phase==='erode';
    const title=phase==='sea'?'海の底の断面図（地層が積もるようす）':(phase==='lift'?'大地が隆起して、海の底が陸になる':(phase==='erode'?'雨や川の水で地表がけずられる（侵食）':'いまの土地の断面図（西 → 東）'));
    txt(title,8,19,'bold 14px sans-serif','#0f172a');
    if(phase==='land') txt('A〜Dの印をドラッグ・地面をタップで、ほる場所を変える',SX1,19,'11px sans-serif','#64748b','right');
    if(phase==='sea') txt('図をタップ・ドラッグすると海面が上下する',SX1,19,'11px sans-serif','#64748b','right');
    ctx.save(); ctx.beginPath(); ctx.rect(SX0,SY0,SX1-SX0,SY1-SY0); ctx.clip();
    const sk=ctx.createLinearGradient(0,SY0,0,SY1); sk.addColorStop(0,'#dbeafe'); sk.addColorStop(1,'#f8fafc'); ctx.fillStyle=sk; ctx.fillRect(SX0,SY0,SX1-SX0,SY1-SY0);
    const sy=seaY(), ty=zp(base(200,false)+TT());
    if(sy<SY1+50){ const wg=ctx.createLinearGradient(0,sy,0,SY1); wg.addColorStop(0,'#7dd3fc'); wg.addColorStop(1,'#0369a1'); ctx.fillStyle=wg; ctx.fillRect(SX0,sy,SX1-SX0,SY1-sy+60); }
    if(land){ ctx.save(); clipGround(); drawStrata(); ctx.restore(); } else drawStrata();
    drawFossils();
    if(land){ drawGround(); drawFault(); if(fA>0.5) txt('しゅう曲',xp(125),zp(G(125)-7),'bold 12px sans-serif','#6d28d9','center',true); drawForce(); ashLabel(); if(phase==='land') drawBorings(); }
    if((phase==='sea'||phase==='lift')&&sy<SY1) drawSeaTop(sy);
    if(phase==='sea') drawSeaInfo(sy,ty);
    if(erupt>0) drawAshFall(ty);
    ctx.restore();
    ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1; ctx.strokeRect(SX0+0.5,SY0+0.5,SX1-SX0-1,SY1-SY0-1);
    if(land){ ctx.strokeStyle='#334155'; ctx.lineWidth=1; for(let z=20;z<=80;z+=10){ const y=zp(z); line(SX0-4,y,SX0,y); txt(z+'m',SX0-6,y+4,'11px sans-serif','#475569','right'); } txt('標高',6,SY0+11,'11px sans-serif','#475569');
      const RU=[100,200,300]; RU.forEach((x)=>{ const X=xp(x); line(X,SY1,X,SY1+4); txt(x+'m',X,SY1+15,'11px sans-serif','#475569','center'); });
      txt('西',SX0,SY1+15,'bold 12px sans-serif','#0f172a','left'); txt('東',SX1,SY1+15,'bold 12px sans-serif','#0f172a','right'); txt('高さは横の約2.5倍に強調',SX0+6,SY0+14,'10px sans-serif','#64748b','left',true); }
    else { txt('← 岸（陸）の方',SX0,SY1+15,'11px sans-serif','#475569','left'); txt('沖の方 →',SX1,SY1+15,'11px sans-serif','#475569','right'); }
    drawToast(); }
  // ---- 下の図：海岸のようす ----
  function drawCoast(){ const dep=+$('dep').value, z=zone(dep), XA=40, YA=362, SL=0.3, yf=(x)=>YA+SL*(x-XA), XM=520, xsh=XM-3.6*dep, ys=yf(xsh), X0=8, X1=632, YT=CT+26, YB=540;
    txt('海岸から沖までのようす（横から見たイメージ）',8,CT+18,'bold 14px sans-serif','#0f172a');
    ctx.save(); rr(X0,YT,X1-X0,YB-YT,8); ctx.clip();
    const sk=ctx.createLinearGradient(0,YT,0,YB); sk.addColorStop(0,'#e0f2fe'); sk.addColorStop(1,'#ffffff'); ctx.fillStyle=sk; ctx.fillRect(X0,YT,X1-X0,YB-YT);
    const wg=ctx.createLinearGradient(0,ys,0,yf(X1)); wg.addColorStop(0,'#93c5fd'); wg.addColorStop(1,'#1e40af'); ctx.fillStyle=wg; ctx.beginPath(); ctx.moveTo(xsh,ys); ctx.lineTo(X1+4,ys); ctx.lineTo(X1+4,yf(X1+4)); ctx.closePath(); ctx.fill();
    ctx.fillStyle='#e7dcc8'; ctx.beginPath(); ctx.moveTo(X0-4,yf(X0-4)); ctx.lineTo(X1+4,yf(X1+4)); ctx.lineTo(X1+4,YB+4); ctx.lineTo(X0-4,YB+4); ctx.closePath(); ctx.fill();
    if(erupt>0){ const a=Math.min(1,erupt/0.5); for(let i=0;i<9;i++){ const q=(tm*0.35+i/9)%1; ctx.fillStyle='rgba(120,113,108,'+(a*(1-q)*0.8).toFixed(2)+')'; ctx.beginPath(); ctx.arc(66+q*q*60,YT+14-q*10,5+q*12,0,Math.PI*2); ctx.fill(); }
      ctx.fillStyle='rgba(87,83,78,'+(0.6*a).toFixed(2)+')'; for(let i=0;i<70;i++){ const fx=(i*0.6180339)%1, q=(tm*0.4+i*0.21)%1, X=80+fx*(X1-80), Y=YT+q*(yf(X)-YT); ctx.beginPath(); ctx.arc(X,Y,1.1,0,Math.PI*2); ctx.fill(); } }
    ctx.fillStyle='#78716c'; ctx.beginPath(); ctx.moveTo(14,yf(14)+2); ctx.lineTo(58,YT+16); ctx.lineTo(72,YT+16); ctx.lineTo(118,yf(118)+2); ctx.closePath(); ctx.fill(); txt('火山',65,yf(65)-4,'bold 11px sans-serif','#fff','center');
    ctx.strokeStyle='#65a30d'; ctx.lineWidth=4; line(X0-4,yf(X0-4),xsh,ys);
    ctx.strokeStyle='#38bdf8'; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(124,yf(124)-2); ctx.quadraticCurveTo((124+xsh)/2,yf((124+xsh)/2)-8,xsh,ys); ctx.stroke(); txt('川',132,yf(132)-8,'bold 11px sans-serif','#0369a1','left',true);
    const ZS=[['g',0,120],['s',120,240],['m',240,800]];
    ZS.forEach((zz)=>{ const xa=Math.max(X0,xsh+zz[1]), xb=Math.min(X1+4,xsh+zz[2]); if(xb<=xa+2) return; ctx.beginPath(); ctx.moveTo(xa,yf(xa)); ctx.lineTo(xb,yf(xb)); ctx.lineTo(xb,yf(xb)+10); ctx.lineTo(xa,yf(xa)+10); ctx.closePath(); ctx.fillStyle=PAT[zz[0]]; ctx.fill(); ctx.strokeStyle='rgba(30,41,59,.45)'; ctx.lineWidth=0.8; ctx.stroke();
      const n=zz[0]==='g'?5:(zz[0]==='s'?9:14), rr0=zz[0]==='g'?2.6:(zz[0]==='s'?1.4:0.9), sp=zz[0]==='g'?0.8:(zz[0]==='s'?0.5:0.25); ctx.fillStyle=TY[zz[0]].d;
      for(let i=0;i<n;i++){ const X=xa+((i*0.618+0.1)%1)*(xb-xa), q=(tm*sp+i*0.37)%1, Y=ys+5+q*(yf(X)-ys-8); if(X<=xsh+2||Y>yf(X)-3) continue; ctx.beginPath(); ctx.arc(X,Y,rr0,0,Math.PI*2); ctx.fill(); }
      const xc=zz[0]==='m'?Math.min(xa+70,(xa+xb)/2):(xa+xb)/2; if(xc<X1-14) txt(TY[zz[0]].n,xc,yf(xc)-7,'bold 13px sans-serif','#0f172a','center',true); });
    ctx.strokeStyle='#0284c7'; ctx.lineWidth=1.5; line(xsh,ys,X1+4,ys); txt('海面',X1-6,ys-5,'11px sans-serif','#0369a1','right',true); txt('岸',xsh-2,ys-8,'bold 12px sans-serif','#166534','center',true);
    const ym=yf(XM); ctx.setLineDash([4,3]); ctx.strokeStyle='#0f172a'; ctx.lineWidth=1.3; line(XM,ys+2,XM,ym-2); ctx.setLineDash([]);
    ctx.fillStyle='#dc2626'; ctx.beginPath(); ctx.moveTo(XM,ym-1); ctx.lineTo(XM-7,ym-13); ctx.lineTo(XM+7,ym-13); ctx.closePath(); ctx.fill();
    txt('この場所',XM,ys-22,'bold 12px sans-serif','#b91c1c','center',true); txt('（上の断面図）',XM,ys-8,'11px sans-serif','#b91c1c','center',true);
    if(ym-ys>22) txt('深さ',XM+6,(ys+ym)/2+4,'bold 11px sans-serif','#0f172a','left',true);
    ctx.restore(); ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1; rr(X0,YT,X1-X0,YB-YT,8); ctx.stroke();
    let y=wrap('川の水に運ばれた土砂は、粒が大きく重いもの（れき）ほど岸の近くで先にしずみ、小さく軽いもの（泥）ほど沖まで運ばれて積もります。',10,YB+19,620,17,'12px sans-serif','#334155')+19;
    y=wrap('海面が上がると岸が遠くなり、「この場所」は深くなって、積もる粒が小さくなります。海面が下がると、その反対です。',10,y,620,17,'12px sans-serif','#334155')+22;
    const st=(ashCur||ashQ>0)?'いま：噴火で火山灰が積もっている':'いま：海の深さ「'+ZN[z]+'」→ '+TY[z].n+'が積もる'+(L.length?'（'+L.length+'層目）':'');
    txt(st,10,Math.min(H-6,y),'bold 14px sans-serif','#0e7490'); }
  function drawSteps(){ txt('海の底でできた地層が、陸の上で見られるまで',8,CT+18,'bold 14px sans-serif','#0f172a');
    const S=[['① 隆起','大地が持ち上がり、海の底が陸になる。このとき地層が傾くことがある。'],['② 侵食','雨や川の水で地表がけずられ、いまの丘や谷の形になる。'],['③ ボーリング','A〜Dの4地点で、地表から35mの深さまでほって地層を調べる。']];
    const cur=phase==='lift'?0:(phase==='erode'?1:2);
    S.forEach((s,i)=>{ const y=CT+32+i*66, on=i===cur; ctx.fillStyle=on?'#ecfeff':'#f8fafc'; ctx.strokeStyle=on?'#0891b2':'#e2e8f0'; ctx.lineWidth=on?2:1; rr(10,y,620,56,8); ctx.fill(); ctx.stroke();
      txt(s[0],24,y+23,'bold 15px sans-serif',on?'#0e7490':'#94a3b8'); wrap(s[1],24,y+44,590,16,'13px sans-serif',on?'#0f172a':'#94a3b8'); }); }
  // ---- 下の図：柱状図 ----
  function drawColumns(){ const elev=$('view').value==='elev', order=sorted(), ia=ashIdx();
    const cols=order.map((i)=>{ const c=column(B[i].x); return {i:i,x:B[i].x,c:c,a:ashAt(B[i].x,c)}; });
    txt('柱状図（西 → 東の順）',8,CT+16,'bold 14px sans-serif','#0f172a');
    txt(elev?'標高をそろえて表示':'地表をそろえて表示（深さ）',RX-14,CT+16,'bold 11px sans-serif','#0e7490','right');
    let zt=0, zb=BD; if(elev){ zt=-1e9; zb=1e9; cols.forEach((o)=>{ zt=Math.max(zt,o.c.g); zb=Math.min(zb,o.c.g-BD); }); zt=Math.ceil(zt/5)*5; zb=Math.floor(zb/5)*5; }
    const yOf=(o,z)=>elev?CY0+(zt-z)/(zt-zb)*(CY1-CY0):CY0+(o.c.g-z)/BD*(CY1-CY0);
    cols.forEach((o,j)=>{ if(o.i===sel){ ctx.fillStyle='#fef3c7'; rr(CXS[j]-CW/2-14,CT+26,CW+28,CY1+40-CT-26,8); ctx.fill(); } });
    ctx.strokeStyle='#334155'; ctx.lineWidth=1; line(42,CY0,42,CY1);
    if(elev){ const st=(zt-zb)>45?10:5; for(let v=zb;v<=zt+1e-9;v+=st){ const y=CY0+(zt-v)/(zt-zb)*(CY1-CY0); line(38,y,42,y); txt(v+'m',36,y+4,'10px sans-serif','#475569','right'); } txt('標高',6,CY0-10,'11px sans-serif','#475569'); }
    else { for(let v=0;v<=BD;v+=5){ const y=CY0+v/BD*(CY1-CY0); line(38,y,42,y); txt(v+'m',36,y+4,'10px sans-serif','#475569','right'); } txt('深さ',6,CY0-10,'11px sans-serif','#475569'); }
    let an=0; const AO={}; L.forEach((l,ii)=>{ if(l.t==='a'){ AO[ii]=an; an++; } });
    cols.forEach((o,j)=>{ const cx=CXS[j], x0=cx-CW/2, on=o.i===sel, g=o.c.g, ytop=yOf(o,g), ybot=yOf(o,g-BD), yd=ytop+(ybot-ytop)*drill;
      txt(B[o.i].n,cx,CY0-24,'bold 16px sans-serif',on?'#b45309':'#0f172a','center'); txt('標高'+f1(g)+'m',cx,CY0-9,'11px sans-serif','#334155','center');
      ctx.save(); ctx.beginPath(); ctx.rect(x0,ytop,CW,Math.max(0,yd-ytop)); ctx.clip();
      o.c.iv.forEach((v)=>{ const y1=yOf(o,v.top), y2=yOf(o,v.bot); ctx.fillStyle=v.i<0?PAT.b:PAT[L[v.i].t]; ctx.fillRect(x0,y1,CW,y2-y1); ctx.strokeStyle='rgba(30,41,59,.75)'; ctx.lineWidth=0.9; line(x0,y2,x0+CW,y2);
        if(v.i>=0&&L[v.i].f&&y2-y1>=16) fossil(L[v.i].f,x0+CW-12,(y1+y2)/2,0.9); });
      ctx.restore();
      if(an>=2) o.c.iv.forEach((v)=>{ if(v.i>=0&&L[v.i].t==='a'){ const y1=yOf(o,v.top), y2=yOf(o,v.bot); if(y1<yd) txt(CIR[Math.min(9,AO[v.i])],x0-2,(y1+y2)/2+4,'bold 10px sans-serif','#9d174d','right',true); } });
      ctx.strokeStyle=on?'#d97706':'#1e293b'; ctx.lineWidth=on?2.4:1.2; ctx.strokeRect(x0,ytop,CW,Math.max(0,yd-ytop));
      if(drill>=1){ const a=o.a; if(a.s==='ok'){ txt('鍵層 '+f1(a.d)+'m',cx,CY1+15,'bold 11px sans-serif','#9d174d','center'); txt('（標高'+f1(a.z)+'m）',cx,CY1+30,'11px sans-serif','#475569','center'); }
        else txt(a.s==='cut'?'鍵層はけずられた':(a.s==='deep'?'鍵層は35mより下':'火山灰の層なし'),cx,CY1+15,'11px sans-serif','#475569','center'); } });
    if(drill>=1&&ia>=0){ ctx.save(); ctx.setLineDash([5,4]); ctx.strokeStyle='#db2777'; ctx.lineWidth=1.8; for(let j=0;j<cols.length-1;j++){ const p=cols[j], q=cols[j+1]; if(p.a.s==='ok'&&q.a.s==='ok') line(CXS[j]+CW/2,yOf(p,p.a.z),CXS[j+1]-CW/2,yOf(q,q.a.z)); } ctx.restore(); }
    drawSide(cols); }
  function drawSide(cols){ let y=CT+16; txt('記号',RX,y,'bold 12px sans-serif','#0f172a'); y+=7;
    const LG=[['g','れき（れき岩）'],['s','砂（砂岩）'],['m','泥（泥岩）'],['a','火山灰（凝灰岩）'],['b','古い岩石']];
    LG.forEach((r)=>{ ctx.fillStyle=PAT[r[0]]; ctx.fillRect(RX,y,24,12); ctx.strokeStyle='#475569'; ctx.lineWidth=0.8; ctx.strokeRect(RX,y,24,12); txt(r[1],RX+30,y+10,'11px sans-serif','#1e293b'); y+=15; });
    shijimi(RX+12,y+7,0.85); txt('シジミ：示相化石（河口や湖）',RX+30,y+11,'11px sans-serif','#1e293b'); y+=17;
    vicarya(RX+12,y+7,0.85); txt('ビカリア：示準化石（新生代）',RX+30,y+11,'11px sans-serif','#1e293b'); y+=21;
    const bx=RX-4, by=y, bw=W-6-bx, bh=CY1+36-by; ctx.fillStyle='#f0fdfa'; ctx.strokeStyle='#5eead4'; ctx.lineWidth=1.2; rr(bx,by,bw,bh,8); ctx.fill(); ctx.stroke();
    let yy=by+19; const ia=ashIdx();
    if(drill<1){ txt('ボーリング中…',RX+4,yy,'bold 12px sans-serif','#0f766e'); return; }
    if(ia<0){ yy=wrap('火山灰の層（鍵層）がないので、地層のつながりは粒の重なり方で比べます。',RX+4,yy,bw-14,16,'12px sans-serif','#0f172a')+22; }
    else { txt('火山灰の層①の上面の標高',RX+4,yy,'bold 12px sans-serif','#0f172a'); yy+=18;
      const all=B.map((b)=>{ const c=column(b.x); return {n:b.n,a:ashAt(b.x,c)}; });
      for(let r=0;r<2;r++){ const s=all.slice(r*2,r*2+2).map((o)=>o.n+' '+(o.a.s==='ok'?f1(o.a.z)+'m':'？')).join('　'); txt(s,RX+4,yy,'12px sans-serif','#0f172a'); yy+=17; }
      const tl=tiltRead(cols); yy+=2;
      if(tl===null){ yy=wrap('2地点以上で鍵層が見つからないので、傾きは読めません。',RX+4,yy,bw-14,16,'12px sans-serif','#0f172a')+20; }
      else if(Math.abs(tl)<0.05){ txt('→ ほぼ水平',RX+4,yy,'bold 13px sans-serif','#be123c'); yy+=17; txt('（地層は傾いていない）',RX+4,yy,'11px sans-serif','#334155'); yy+=20; }
      else { const d=tl<0?'東':'西'; txt('→ '+d+'へ100mで'+f1(Math.abs(tl))+'m低い',RX+4,yy,'bold 13px sans-serif','#be123c'); yy+=17; txt('（地層は'+d+'に低く傾いている）',RX+4,yy,'11px sans-serif','#334155'); yy+=20; } }
    const yi=youngest(); txt('地層の数：'+(yi+1)+'層',RX+4,yy,'12px sans-serif','#0f172a'); yy+=17;
    txt('いちばん新しい層：'+(yi>=0?TY[L[yi].t].n+'（'+(yi+1)+'層目）':'なし'),RX+4,yy,'11px sans-serif','#0f172a'); yy+=17;
    if(fA>0.5){ txt('しゅう曲：地層が波打っている',RX+4,yy,'11px sans-serif','#6d28d9'); yy+=15; }
    if(fS<-0.5) txt('正断層：西側が'+f1(-fS)+'m下がった',RX+4,yy,'11px sans-serif','#b91c1c'); else if(fS>0.5) txt('逆断層：西側が'+f1(fS)+'m上がった',RX+4,yy,'11px sans-serif','#b91c1c'); }
  function drawPanel(){ ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; line(6,CT,W-6,CT); if(phase==='sea') drawCoast(); else if(phase==='lift'||phase==='erode') drawSteps(); else drawColumns(); }
  // ---- 統計欄 ----
  function updStats(){ let sh='';
    if(phase==='land'){ const cs=B.map((b)=>{ const c=column(b.x); return {x:b.x,c:c,a:ashAt(b.x,c)}; }), yi=youngest();
      setStat('sN',(yi+1)+'層');
      cs.forEach((o,i)=>{ setStat('sK'+i,o.a.s==='ok'?f1(o.a.d)+' m':(o.a.s==='cut'?'けずられた':(o.a.s==='deep'?'35mより下':'なし'))); });
      const tl=tiltRead(cs); setStat('sTilt',tl===null?'読めない':(Math.abs(tl)<0.05?'ほぼ水平':(tl<0?'東が':'西が')+f1(Math.abs(tl))+'m低い'));
      setStat('sNew',yi>=0?TY[L[yi].t].n+'（'+(yi+1)+'層目）':'古い岩石');
      if(tl!==null&&cs.every((o)=>o.a.s==='ok')) sh='【地層と柱状図】火山灰の鍵層の深さはA'+f1(cs[0].a.d)+'m・B'+f1(cs[1].a.d)+'m・C'+f1(cs[2].a.d)+'m・D'+f1(cs[3].a.d)+'m。標高をそろえると、地層は'+(Math.abs(tl)<0.05?'ほぼ水平':(tl<0?'東':'西')+'へ100mあたり'+f1(Math.abs(tl))+'m低くなるように傾いている')+'｜シミュラボ';
      else sh='【地層と柱状図】'+(yi+1)+'層の地層を4地点でボーリング。火山灰の層（鍵層）の標高をそろえて、地層のつながりと傾きを読み取る｜シミュラボ'; }
    else { const top=curTop(), n=L.filter((l)=>l.th>0.05).length; setStat('sN',n+'層'); for(let i=0;i<4;i++) setStat('sK'+i,phase==='sea'?'海の中':'調査前');
      setStat('sTilt',phase==='sea'||k===0?'水平':(k<0?'東が':'西が')+f1(Math.abs(k)*100)+'m低い');
      setStat('sNew',top?TY[top.t].n+(phase==='sea'?'（積もり中）':'（'+L.length+'層目）'):'まだない');
      sh=phase==='sea'?'【地層のでき方】海の深さが変わると積もる粒が変わる（浅い：れき、やや深い：砂、深い：泥）。いま'+Math.max(1,L.length)+'層目が積もっている｜シミュラボ':'【地層のでき方】海の底でできた'+n+'層の地層が隆起して陸になった｜シミュラボ'; }
    setShare(sh); }
  function draw(){ ctx.clearRect(0,0,W,H); ctx.fillStyle='#fff'; ctx.fillRect(0,0,W,H); rebot(); drawSection(); drawPanel(); updStats(); }
  // ---- 進め方 ----
  function depLabel(){ const z=zone(+$('dep').value); $('depL').textContent=ZN[z]+'（'+TY[z].n+'が積もる）'; }
  function tiltLabel(){ const v=+$('tilt').value; $('tiltL').textContent=v===0?'水平':(v>0?'東':'西')+'が'+Math.abs(v)+'m低い／100m'; }
  function btns(){ $('go').textContent=phase==='sea'?'⬆ 隆起させる（陸にする）':'▶ 海にもどして積もらせる'; $('fault').textContent=['↕ 断層を入れる','↕ 逆断層にする','↕ 断層をなくす'][fType]; $('fold').textContent=fAT>0?'〰 しゅう曲をもどす':'〰 しゅう曲させる'; }
  function toast(s){ msg=s; msgT=3.4; dirty=true; }
  function loadExample(){ L=[]; SCRIPT.forEach((s)=>{ const l=newLayer(s[0]); l.th=s[1]; l.done=true; }); rebot();
    $('tilt').value=4; tiltLabel(); k=-0.04; $('dep').value=83; depLabel(); $('auto').value='auto'; $('view').value='depth';
    fA=0; fAT=0; fS=0; fST=0; fType=0; lastF=''; phase='land'; lift=1; ero=1; drill=1; U=calcU(); B=DEFB.map((x,i)=>({n:NAMES[i],x:x})); sel=0;
    si=SCRIPT.length; rem=0; ashQ=0; ashCur=null; erupt=0; depositing=false; dirty=true; btns(); }
  function startSea(){ L=[]; rebot(); phase='sea'; si=0; rem=SCRIPT[0][1]; ashQ=0; ashCur=null; endT=0; erupt=0; fA=0; fAT=0; fS=0; fST=0; fType=0; lastF=''; lift=0; ero=0; drill=0; dirty=true; btns(); }
  function startLift(){ if(TT()<6){ toast('もう少し積もらせてから隆起させましょう（6m以上）。'); return; }
    const out=[]; L.filter((l)=>l.th>0.05).forEach((l)=>{ const q=out[out.length-1]; if(q&&q.t===l.t&&l.t!=='a'){ q.th+=l.th; if(!q.f) q.f=l.f; } else out.push(l); });
    L=out; L.forEach((l)=>{ l.done=true; }); ashCur=null; ashQ=0; rebot(); k=-(+$('tilt').value)/100; U=calcU(); phase='lift'; lift=0; depositing=false; dirty=true; btns(); }
  function depositAsh(dt){ if(!ashCur){ const top=curTop(); if(top) top.done=true; ashCur=newLayer('a'); erupt=2.2; } ashCur.th=Math.min(1,ashCur.th+dt*0.8); rebot(); if(ashCur.th>=1-1e-9){ ashCur.th=1; ashCur.done=true; ashCur=null; return true; } return false; }
  function stepSea(dt){ depositing=false;
    if(ashQ>0){ if(depositAsh(dt)) ashQ--; return; }
    if($('auto').value==='auto'){
      if(si>=SCRIPT.length){ endT+=dt; if(endT>0.8) startLift(); return; }
      const typ=SCRIPT[si][0];
      if(typ==='a'){ if(depositAsh(dt)){ si++; rem=si<SCRIPT.length?SCRIPT[si][1]:0; } return; }
      const tgt=ZCEN[typ]; let d=+$('dep').value;
      if(Math.abs(d-tgt)>0.5){ d+=Math.sign(tgt-d)*Math.min(Math.abs(tgt-d),70*dt); $('dep').value=d; depLabel(); return; }
      let top=curTop(); if(!top||top.t!==typ||top.done) top=newLayer(typ);
      const a=Math.min(rem,RATE*dt); top.th+=a; rem-=a; depositing=true; if(rem<=1e-9){ top.done=true; si++; rem=si<SCRIPT.length?SCRIPT[si][1]:0; }
    } else {
      const z=zone(+$('dep').value); let top=curTop();
      if(!top||top.t!==z){ if(top&&top.t!=='a'&&top.th<0.3){ L.pop(); top=curTop(); } if(!top||top.t!==z) top=newLayer(z); }
      top.done=false; top.th+=RATE*dt; depositing=true;
      if(top.th>0) { rebot(); if(TT()>=TMAX){ startLift(); return; } }
    }
    rebot(); }
  function stepAnim(dt){ if(phase==='lift'){ lift=Math.min(1,lift+dt/2.4); if(lift>=1){ phase='erode'; ero=0; } return true; }
    if(phase==='erode'){ ero=Math.min(1,ero+dt/2.0); if(ero>=1){ phase='land'; drill=0; btns(); if(TT()<30) toast('積もった地層がうすいので、低い所では地層がけずられて、下の古い岩石が出ています。'); } return true; }
    let ch=false;
    if(phase==='land'&&drill<1){ drill=Math.min(1,drill+dt/1.2); ch=true; }
    if(fA!==fAT){ const d=fAT-fA; fA+=Math.sign(d)*Math.min(Math.abs(d),8*dt); ch=true; }
    if(fS!==fST){ const d=fST-fS; fS+=Math.sign(d)*Math.min(Math.abs(d),7*dt); if(Math.abs(fST-fS)<1e-9) fS=fST; ch=true; }
    return ch; }
  $('go').addEventListener('click',()=>{ if(phase==='sea') startLift(); else if(phase==='land') startSea(); });
  $('erupt').addEventListener('click',()=>{ if(phase==='sea'){ ashQ++; dirty=true; } else toast('噴火は、海の底で地層が積もっているときに使えます。「▶ 海にもどして積もらせる」を押してください。'); });
  $('fault').addEventListener('click',()=>{ if(phase!=='land'){ toast('断層は、隆起して陸になったあとに入れられます。'); return; } fType=(fType+1)%3; fST=[0,-6,6][fType]; lastF=fType===1?'pull':(fType===2?'push':(fAT>0?'push':'')); btns(); dirty=true; });
  $('fold').addEventListener('click',()=>{ if(phase!=='land'){ toast('しゅう曲は、隆起して陸になったあとに試せます。'); return; } fAT=fAT>0?0:7; lastF=fAT>0?'push':(fType===1?'pull':(fType===2?'push':'')); btns(); dirty=true; });
  $('reset').addEventListener('click',()=>{ loadExample(); });
  $('dep').addEventListener('input',()=>{ depLabel(); if(phase==='sea') $('auto').value='man'; else if(phase==='land'&&msgT<=0) toast('海の深さは、「▶ 海にもどして積もらせる」を押したあとに動かせます。'); dirty=true; });
  $('auto').addEventListener('change',()=>{ dirty=true; });
  $('tilt').addEventListener('input',()=>{ tiltLabel(); if(phase==='land'){ k=-(+$('tilt').value)/100; U=calcU(); } dirty=true; });
  $('view').addEventListener('change',()=>{ dirty=true; });
  function pxy(e){ const q=cpos(cv,e); return [q[0]/dpr,q[1]/dpr]; }
  function setSea(y){ const top=zp(base(200,false)+TT()); $('dep').value=clamp(Math.round(((top-y)-10)/0.5),5,100); depLabel(); $('auto').value='man'; }
  cv.addEventListener('pointerdown',(e)=>{ const q=pxy(e), x=q[0], y=q[1];
    if(y>=SY0&&y<=SY1+6&&x>=SX0-6&&x<=SX1+6){
      if(phase==='sea'){ dragging='sea'; setSea(y); }
      else if(phase==='land'){ let hit=-1, best=26; B.forEach((b,i)=>{ const d=Math.abs(xp(b.x)-x); if(d<best){ best=d; hit=i; } }); if(hit>=0) sel=hit; else B[sel].x=clamp(Math.round(xm(x)),4,396); dragging='bor'; }
      else return;
      try{ cv.setPointerCapture(e.pointerId); }catch(err){ } e.preventDefault(); dirty=true; return; }
    if(phase==='land'&&y>CT){ const od=sorted(); for(let j=0;j<4;j++){ if(Math.abs(x-CXS[j])<46){ sel=od[j]; dirty=true; return; } } } });
  cv.addEventListener('pointermove',(e)=>{ if(!dragging) return; const q=pxy(e); if(dragging==='sea'){ if(phase==='sea') setSea(q[1]); } else if(phase==='land') B[sel].x=clamp(Math.round(xm(q[0])),4,396); dirty=true; });
  ['pointerup','pointercancel'].forEach((n)=>cv.addEventListener(n,()=>{ dragging=''; }));
  function loop(now){ const dt=Math.min(0.05,Math.max(0,(now-last)/1000)); last=now; tm+=dt; let ch=false;
    if(phase==='sea'){ stepSea(dt); ch=true; }
    if(stepAnim(dt)) ch=true;
    if(erupt>0){ erupt=Math.max(0,erupt-dt); ch=true; }
    if(msgT>0){ msgT=Math.max(0,msgT-dt); ch=true; }
    if(ch||dirty){ dirty=false; draw(); }
    requestAnimationFrame(loop); }
  loadExample(); draw(); requestAnimationFrame(loop);
''')


# ============================================================ 2 火山の形と火成岩
sim(slug="kazan-kaseigan", cat="rika", emoji="🌋", score=79,
    title="火山の形と火成岩シミュレーター（マグマのねばりけ・冷え方）",
    title_tag="火成岩と火山の形のシミュレーター｜マグマのねばりけ・斑状組織と等粒状組織（中1理科）",
    meta_desc="マグマのねばりけを変えると、火山の形（たて状火山・成層火山・溶岩ドーム）、噴火のようす、溶岩や岩石の色が変わります。急に冷えた火山岩の斑状組織と、ゆっくり冷えた深成岩の等粒状組織ができる様子をアニメで比べ、火成岩6種と鉱物の割合も確かめられます。",
    og_title="火山の形と火成岩シミュレーター（マグマのねばりけ・冷え方）",
    og_desc="マグマのねばりけで火山の形・噴火・岩石の色が変わる。斑状組織と等粒状組織のでき方をアニメで比べる中1理科の教材です。",
    card_desc="マグマのねばりけで火山の形・噴火・岩石の色が変わる。斑状組織と等粒状組織のでき方もアニメで比べる。",
    lead="マグマのねばりけのスライダーを動かすと、火山の形・噴火のようす・溶岩や岩石の色が変わります。「冷やして結晶をつくる」ボタンを押すと、地表付近で急に冷えた火山岩（斑状組織）と、地下深くでゆっくり冷えた深成岩（等粒状組織）のでき方をアニメで比べられます。",
    model="中1 火山と地震（火山活動と火成岩）",
    level="中学1年",
    unit="中学校 第2分野（2）大地の成り立ちと変化",
    canvas=canvas(640, 656, light=True),
    controls=slider("visc", "マグマのねばりけ", 0, 100, 50, 1)
           + select("ex", "例の火山", [("", "（スライダーで選ぶ）"), ("8", "マウナロア（ハワイ）"), ("14", "キラウエア（ハワイ）"),
                                     ("50", "桜島（鹿児島県）"), ("56", "浅間山（群馬県・長野県）"),
                                     ("86", "雲仙普賢岳の平成新山（長崎県）"), ("93", "昭和新山（北海道）")])
           + select("cool", "冷え方", [("surf", "ア 火山岩（急に）"), ("deep", "イ 深成岩（ゆっくり）")]),
    buttons=btn("grow", "❄️ 冷やして結晶をつくる", True) + btn("erupt", "⏸ 噴火を止める"),
    stats=stats([("sShape", "火山の形", False), ("sErupt", "噴火のようす", False), ("sRock", "岩石の名前", True),
                 ("sTex", "組織（つくり）", True), ("sColor", "岩石の色", False), ("sMafic", "有色鉱物の割合", False)]),
    legend="上：マグマのねばりけによる火山の形と噴火のようす（大きさは実際の比率ではありません）。右上のゲージや下のグラフをタップ・ドラッグしても、ねばりけを変えられます。下左：同じマグマが地表付近で急に冷えた岩石（ア 火山岩）と、地下深くでゆっくり冷えた岩石（イ 深成岩）をルーペで見たようすです。円や分類表をタップすると、統計欄の岩石が切りかわります。右下：ふくまれる鉱物の割合の目安。",
    article='''
<h2>このシミュレーションでわかること</h2>
<p>マグマのねばりけが弱いと、傾斜がゆるやかな火山（たて状火山）ができ、噴火はおだやかで、溶岩や岩石は黒っぽくなります。ねばりけが強いと、ドーム状の火山（溶岩ドーム）ができ、噴火は激しく、岩石は白っぽくなります。また、マグマが地表付近で急に冷えると<b>斑状組織</b>の<b>火山岩</b>に、地下深くでゆっくり冷えると<b>等粒状組織</b>の<b>深成岩</b>になります。</p>
<p>対応する単元は、中学校学習指導要領 理科 第2分野（2）「大地の成り立ちと変化」の「火山と地震」のうち「火山活動と火成岩」で、<b>中学1年</b>で学習します。学習指導要領では、粘性（ねばりけ）と関係付けながら代表的な火山を扱うこと、火山岩と深成岩の代表的な岩石と、代表的な造岩鉱物を扱うことが示されています。小学校第6学年「土地のつくりと変化」の「土地は、火山の噴火によって変化すること」の発展としても使えます。</p>

<h2>授業での使い方</h2>
<ul>
<li><b>導入</b>：「例の火山」でマウナロア、桜島、昭和新山を順に選び、火山の形と噴火のようすを比べます。「形のちがいは何によって決まるのか」を問いかけ、マグマのねばりけに目を向けさせます。</li>
<li><b>展開</b>：水の量を変えてねばりけを変えた小麦粉（ホットケーキミックスなど）を、穴をあけた板の下からおし出して火山の形をつくるモデル実験のあとに使い、ねばりけのスライダーで結果を確かめます。火成岩の観察（ルーペや双眼実体顕微鏡）のあとに「冷やして結晶をつくる」ボタンを押し、斑状組織と等粒状組織のでき方を比べます。ミョウバンなどの濃い水溶液をゆっくり冷やした場合と急に冷やした場合で、できる結晶の大きさを比べる実験とも結び付けられます。</li>
<li><b>まとめ</b>：右下の分類表と鉱物の割合のグラフで、火成岩の名前・色・組織と、ふくまれる鉱物の関係を整理します。</li>
</ul>
<p>生徒への問いの例：</p>
<ol>
<li>溶岩ドームをつくるマグマが、激しい噴火を起こしやすいのはなぜでしょうか（マグマにふくまれる気体のぬけやすさで考えましょう）。</li>
<li>火山岩には、大きな結晶（斑晶）と、細かい粒やガラス（石基）が混じっています。斑晶と石基は、それぞれどこで、どのように冷えてできたのでしょうか。</li>
<li>花こう岩が白っぽく、斑れい岩が黒っぽく見えるのはなぜでしょうか（ふくまれる鉱物の種類と割合で考えましょう）。</li>
</ol>

<h2>しくみ・解説</h2>
<h3>マグマのねばりけと火山の形・噴火・色</h3>
''' + T([["火山の形", "傾斜がゆるやかな形<br>（たて状火山）", "円すい形<br>（成層火山）", "ドーム状<br>（溶岩ドーム）"],
          ["噴火のようす", "おだやか<br>（溶岩が流れ出す）", "中間<br>（爆発的な噴火と溶岩の流出をくり返す）", "激しい<br>（爆発的。火砕流が起こることもある）"],
          ["溶岩・火山灰の色", "黒っぽい", "灰色っぽい（中間）", "白っぽい"],
          ["火山の例", "マウナロア、キラウエア（ハワイ）", "桜島、浅間山、富士山", "昭和新山、雲仙普賢岳（平成新山）"]],
         ["マグマのねばりけ", "弱い", "中くらい", "強い"]) + '''
<p>ねばりけが強いマグマは流れにくいので、溶岩が火口の上にもり上がってドーム状になります。また、マグマにとけている気体（火山ガス。大部分は水蒸気）がぬけにくく、たまった気体が一気にふき出すため、爆発的な激しい噴火になりやすくなります。ねばりけが弱いマグマは気体がぬけやすく、溶岩が遠くまで流れて、傾斜のゆるやかな火山になります。マグマのねばりけは、マグマにふくまれる二酸化ケイ素の割合が多いほど、また温度が低いほど強くなります（発展）。</p>
<p>火山の噴火でふき出されるもの（<b>火山噴出物</b>）には、溶岩、火山弾、軽石、火山灰、火山ガスなどがあります。</p>
<h3>火成岩のでき方と組織</h3>
<p>マグマが冷えて固まった岩石を<b>火成岩</b>といいます。火成岩は、冷え方によって2つに分けられます。</p>
''' + T([["火山岩", "地表や地表付近で、急に冷えて固まった", "<b>斑状組織</b>：大きな結晶（<b>斑晶</b>）のまわりを、細かい粒やガラス（<b>石基</b>）がうめている", "玄武岩・安山岩・流紋岩"],
          ["深成岩", "地下深くで、長い時間をかけてゆっくり冷えて固まった", "<b>等粒状組織</b>：同じくらいの大きさの結晶が、すき間なく組み合わさっている", "斑れい岩・閃緑岩・花こう岩"]],
         ["種類", "でき方", "つくり（組織）", "岩石の例"]) + '''
<p>マグマがゆっくり冷えると、結晶が大きく育つ時間があるので、大きな結晶ができます。急に冷えると、結晶が大きく育つ前に固まるので、細かい結晶や、結晶にならなかったガラスの部分ができます。火山岩の斑晶は、マグマが地下にあるうちにゆっくり冷えてできた結晶で、その後マグマが地表付近に上がって急に冷え、まわりが石基になったと考えられています。</p>
<h3>火成岩の分類と鉱物</h3>
''' + T([["火山岩（斑状組織）", "玄武岩", "安山岩", "流紋岩"],
          ["深成岩（等粒状組織）", "斑れい岩", "閃緑岩", "花こう岩"],
          ["有色鉱物の割合（目安）", "約50％", "約30％", "約10％"],
          ["多くふくまれる鉱物", "チョウ石、キ石、カンラン石", "チョウ石、カクセン石、キ石", "チョウ石、セキエイ、クロウンモ"]],
         ["岩石の色", "黒っぽい", "中間（灰色っぽい）", "白っぽい"]) + '''
<p>火成岩をつくる鉱物（造岩鉱物）は、白色や無色の<b>無色鉱物</b>と、黒っぽい色や緑っぽい色の<b>有色鉱物</b>に分けられます。有色鉱物の割合が多い岩石ほど黒っぽく見えます。</p>
''' + T([["セキエイ（石英）", "無色・白色", "不規則な形。決まった方向に割れない", "無色鉱物"],
          ["チョウ石（長石）", "白色・うすい桃色", "柱状・短冊状。決まった方向に割れる", "無色鉱物"],
          ["クロウンモ（黒雲母）", "黒色〜褐色", "板状・六角形。うすくはがれる", "有色鉱物"],
          ["カクセン石（角閃石）", "緑黒色〜黒色", "長い柱状", "有色鉱物"],
          ["キ石（輝石）", "緑黒色〜褐色", "短い柱状", "有色鉱物"],
          ["カンラン石", "黄緑色", "丸みのある粒状", "有色鉱物"]],
         ["鉱物", "色", "形の特徴", "分類"]) + '''
<p>右下のグラフの割合（体積の割合）は、次の値をもとにしたおおよその目安です。玄武岩・斑れい岩：チョウ石50％、キ石36％、カンラン石12％、カクセン石2％。安山岩・閃緑岩：チョウ石60％、カクセン石20％、キ石8％、セキエイ8％、クロウンモ4％。流紋岩・花こう岩：チョウ石60％、セキエイ30％、クロウンモ8％、カクセン石2％。グラフでは、3つの区分のそれぞれ中央をこの値とし、その間を直線でつないでいます（両はしは一定）。</p>
<h3>例題</h3>
<p><b>例題1</b>　ある火成岩をルーペで観察すると、同じくらいの大きさの鉱物がすき間なく組み合わさっていました。鉱物はセキエイとチョウ石が多く、黒くてうすくはがれる鉱物が少しふくまれていました。（1）このつくりを何といいますか。（2）岩石の名前は何ですか。<br>
→ 結晶の大きさがそろっているので等粒状組織（深成岩）。白っぽい鉱物が多く、クロウンモをふくむので花こう岩。　答え（1）<b>等粒状組織</b>（2）<b>花こう岩</b></p>
<p><b>例題2</b>　黒っぽい溶岩が冷えて固まった岩石を観察すると、斑晶としてカンラン石やキ石が見られました。（1）岩石の名前は何ですか。（2）この溶岩を流した火山は、どのような形をしていると考えられますか。<br>
→ 斑状組織（火山岩）で黒っぽいので玄武岩。黒っぽい溶岩をつくるマグマはねばりけが弱く、傾斜がゆるやかな火山になります。　答え（1）<b>玄武岩</b>（2）<b>傾斜がゆるやかな形（たて状火山）</b></p>
<p><b>例題3</b>　安山岩と閃緑岩は、ふくまれる鉱物の種類がよく似ているのに、つくりがちがいます。その理由を説明しなさい。<br>
→ もとのマグマの性質は似ていますが、冷え方がちがうからです。安山岩は地表付近で急に冷えたので斑状組織に、閃緑岩は地下深くでゆっくり冷えたので等粒状組織になりました。</p>
''' + P("シミュレーターで確かめるには、「例の火山」でマウナロアを選び、「冷え方」を切りかえます（下の円をタップしても切りかわります）。統計欄の岩石の名前が、玄武岩（火山岩）と斑れい岩（深成岩）に変わります。「冷やして結晶をつくる」ボタンを押すと、①地下でゆっくり冷えて斑晶が育ち、②地表付近で急に冷えて石基になる順番を見られます。") + N(
        "<b>このシミュレーターで単純化している点</b><br>"
        "・火山の大きさや高さは、実際の比率ではありません（例：マウナロアの標高は約4,170m、昭和新山は約400m）。噴火のようすも、ねばりけによる傾向を表したイメージです。<br>"
        "・マグマのねばりけ、岩石の色、鉱物の割合は本来つながって変わるもので、3つに分けたのは目安です。鉱物の割合はおおよその例で、同じ名前の岩石でも試料によって大きくちがいます。<br>"
        "・富士山は形が成層火山の代表例ですが、溶岩の多くは玄武岩で、マグマのねばりけは比較的弱い火山です。また、昭和新山や平成新山の溶岩はデイサイトという岩石で、安山岩と流紋岩の中間にあたります（高校で学習）。<br>"
        "・結晶のでき方のアニメは、時間を大きく早送りしています。斑晶や結晶の鉱物は、鉱物の割合に合わせて選んでいます。") + '''
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「中学校学習指導要領（平成29年告示）解説 理科編」第2分野（2）大地の成り立ちと変化（''' + A(MEXT_CHU, "中学校学習指導要領解説") + '''）</li>
<li>中学校理科の教科書（''' + TEXTBOOKS + '''）の第1学年「大地の成り立ちと変化」の単元</li>
<li>気象庁「日本活火山総覧（第4版）」</li>
<li>国土地理院「日本の主な山岳標高」、アメリカ地質調査所（USGS）ハワイ火山観測所の資料（火山の標高）</li>
</ul>
''',
    faqs=[("マグマのねばりけと火山の形には、どんな関係がありますか？", "ねばりけが弱いと溶岩が流れやすく、傾斜がゆるやかな火山（たて状火山。例：マウナロア）になります。中くらいだと円すい形の火山（成層火山。例：桜島）、強いと溶岩が盛り上がってドーム状の火山（溶岩ドーム。例：昭和新山）になります。"),
          ("斑状組織と等粒状組織のちがいは何ですか？", "斑状組織は、大きな結晶（斑晶）のまわりを細かい粒やガラス（石基）がうめているつくりで、地表付近で急に冷えた火山岩に見られます。等粒状組織は、同じくらいの大きさの結晶がすき間なく組み合わさったつくりで、地下深くでゆっくり冷えた深成岩に見られます。"),
          ("火成岩の6種類は、どのように分類しますか？", "組織で火山岩（斑状組織）と深成岩（等粒状組織）に分け、色（ふくまれる有色鉱物の割合）で黒っぽい・中間・白っぽいに分けます。火山岩は黒っぽい順に玄武岩・安山岩・流紋岩、深成岩は斑れい岩・閃緑岩・花こう岩です。"),
          ("岩石が白っぽいか黒っぽいかは、何で決まりますか？", "ふくまれる鉱物の種類と割合で決まります。セキエイやチョウ石などの無色鉱物が多いと白っぽく、カンラン石・キ石・カクセン石・クロウンモなどの有色鉱物が多いと黒っぽくなります。有色鉱物の割合は、玄武岩・斑れい岩で約50％、流紋岩・花こう岩で約10％が目安です。"),
          ("富士山はどのタイプの火山ですか？", "形は円すい形の成層火山で、教科書でも成層火山の例としてよく取り上げられます。ただし、富士山の溶岩の多くは黒っぽい玄武岩で、マグマのねばりけは比較的弱い火山です。溶岩と火山灰などが交互に積み重なって、大きな円すい形になりました。"),
          ("ねばりけが強いマグマは、なぜ激しい噴火になるのですか？", "マグマにとけている気体（火山ガス）がぬけにくく、地下でたまった気体が一気にふき出すからです。ねばりけが弱いマグマは気体がぬけやすいので、溶岩がおだやかに流れ出す噴火になりやすくなります。")],
    rel=[("jishin-ha", "📳", "地震の伝わり方シミュレーター"), ("chisou", "⛏️", "地層のでき方と柱状図"),
         ("chikyu-yure", "🌐", "地球まるごと地震カウンター"), ("joutai-henka", "🧊", "状態変化と粒子のシミュレーター"),
         ("jishin-live", "🗾", "日本はいまも揺れている")],
    js=r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  cv.setAttribute('role','img'); cv.setAttribute('aria-label','マグマのねばりけによる火山の形と噴火のようす、火山岩と深成岩のつくり、鉱物の割合の図');
  cv.style.cursor='pointer';
  const SY0=26, SY1=294, GY=210, CX=300, MCY=258, RA=60, CA={x:86,y:392}, CB={x:252,y:392}, GX=436, GW=186;
  const MIN=['カンラン石','キ石','カクセン石','クロウンモ','チョウ石','セキエイ'];
  const MCOL=['#a3c23f','#2f5d3a','#1f2a24','#2a1a10','#f7f2e8','#cfd8e3'];
  const COMP=[[12,36,2,0,50,0],[0,8,20,4,60,8],[0,0,2,8,60,30]];
  const VR=['玄武岩','安山岩','流紋岩'], PR=['斑れい岩','閃緑岩','花こう岩'], SH=['たて状火山','成層火山','溶岩ドーム'], SHD=['傾斜がゆるやかな形','円すい形','ドーム状（おわんをふせた形）'];
  const ER=['おだやか','中間','激しい'], ERD=['溶岩がおだやかに流れ出す','爆発的な噴火と溶岩の流出をくり返す','激しく爆発する（火砕流が起こることも）'];
  const CO=['黒っぽい','灰色っぽい','白っぽい'], NB=['弱い','中くらい','強い'];
  const EXN=['マウナロア・キラウエア（ハワイ）','桜島・浅間山・富士山','昭和新山・雲仙普賢岳（平成新山）'];
  const PRF=[{R:262,H:46,e:1.8},{R:186,H:122,e:0.72},{R:72,H:84,e:2.6}];
  const ease=(t)=>t<=0?0:(t>=1?1:t*t*(3-2*t));
  const line=(a,b,c,d)=>{ ctx.beginPath(); ctx.moveTo(a,b); ctx.lineTo(c,d); ctx.stroke(); };
  function txt(s,x,y,font,col,al,halo){ ctx.font=font; ctx.textAlign=al||'left'; if(halo){ ctx.lineJoin='round'; ctx.lineWidth=3.5; ctx.strokeStyle='rgba(255,255,255,.95)'; ctx.strokeText(s,x,y); } ctx.fillStyle=col; ctx.fillText(s,x,y); }
  function rr(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.lineTo(x+w-r,y); ctx.quadraticCurveTo(x+w,y,x+w,y+r); ctx.lineTo(x+w,y+h-r); ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h); ctx.lineTo(x+r,y+h); ctx.quadraticCurveTo(x,y+h,x,y+h-r); ctx.lineTo(x,y+r); ctx.quadraticCurveTo(x,y,x+r,y); ctx.closePath(); }
  function rng(seed){ let a=seed>>>0; return function(){ a=(a+0x6D2B79F5)>>>0; let t=a; t=Math.imul(t^(t>>>15),t|1); t^=t+Math.imul(t^(t>>>7),t|61); return ((t^(t>>>14))>>>0)/4294967296; }; }
  let p=0.5, erupting=true, ct=99, tm=3, last=performance.now(), drag='', dirty=true;
  const cls=(q)=>q<1/3?0:(q<2/3?1:2);
  function comp(q){ q=clamp(q,1/6,5/6); const lo=q<=0.5, a=lo?COMP[0]:COMP[1], b=lo?COMP[1]:COMP[2], t=lo?(q-1/6)*3:(q-0.5)*3; return a.map((v,i)=>v+(b[i]-v)*t); }
  function mafic(q){ const c=comp(q); return c[0]+c[1]+c[2]+c[3]; }
  function pick(u,c){ let s=0; for(let i=0;i<6;i++){ s+=c[i]; if(u*100<s) return i; } return 4; }
  const mixc=(a,b,t)=>a.map((v,i)=>Math.round(v+(b[i]-v)*t));
  const tri3=(q,A,Bc,C)=>q<=0.5?mixc(A,Bc,q/0.5):mixc(Bc,C,(q-0.5)/0.5);
  const rgb=(c)=>'rgb('+c.join(',')+')';
  const rockC=(q)=>tri3(q,[62,60,60],[136,128,121],[222,215,204]);
  const glassC=(q)=>tri3(q,[46,46,48],[112,106,100],[206,198,187]);
  function shW(q){ const a=ease((q-0.25)/0.17), b=ease((q-0.583)/0.17); return [1-a,a*(1-b),b]; }
  function vh(dx,q){ const w=shW(q); let h=0; for(let i=0;i<3;i++){ if(w[i]<=0) continue; const u=Math.abs(dx)/PRF[i].R; if(u<1) h+=w[i]*PRF[i].H*(1-Math.pow(u,PRF[i].e)); }
    const ap=Math.abs(dx)/128; if(ap<1) h=Math.max(h,w[2]*18*Math.pow(1-ap,1.3));
    if(w[1]>0){ const u=Math.abs(dx)/13; if(u<1) h-=w[1]*8*(1-u*u); } return Math.max(0,h); }
  function reach(q){ for(let d=330;d>0;d-=2){ if(vh(d,q)>1.2) return d; } return 10; }
  // ---- 結晶（決まった乱数で配置） ----
  const rA=rng(7), PH=[]; for(let n=0;PH.length<7&&n<800;n++){ const a=rA()*Math.PI*2, r=Math.sqrt(rA())*(RA-14), x=Math.cos(a)*r, y=Math.sin(a)*r; if(PH.every((o)=>Math.hypot(o.x-x,o.y-y)>27)) PH.push({x:x,y:y,L:16+rA()*9,rot:rA()*Math.PI,u:rA(),t0:rA()*1.0}); }
  const GM=[]; for(let n=0;n<430;n++){ const a=rA()*Math.PI*2, r=Math.sqrt(rA())*(RA-1); GM.push({x:Math.cos(a)*r,y:Math.sin(a)*r,L:2.4+rA()*3.2,rot:rA()*Math.PI,u:rA(),t0:3.55+rA()*0.9}); }
  const rB=rng(23), SD=[]; for(let i=-5;i<=5;i++){ for(let j=-5;j<=5;j++){ const x=j*23+(Math.abs(i)%2?11.5:0)+(rB()-0.5)*15, y=i*23*0.866+(rB()-0.5)*15; if(Math.hypot(x,y)<RA+18) SD.push({x:x,y:y,u:rB(),t0:rB()*1.8,ang:rB()*Math.PI}); } }
  SD.forEach((s)=>{ s.d=4.7-s.t0-0.3*s.u; });
  function clipH(poly,mx,my,nx,ny){ const out=[]; for(let i=0;i<poly.length;i++){ const a=poly[i], b=poly[(i+1)%poly.length], da=(a[0]-mx)*nx+(a[1]-my)*ny, db=(b[0]-mx)*nx+(b[1]-my)*ny; if(da<=0) out.push(a); if((da<=0)!==(db<=0)){ const t=da/(da-db); out.push([a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t]); } } return out; }
  const CELL=SD.map((s,i)=>{ let poly=[[-RA-40,-RA-40],[RA+40,-RA-40],[RA+40,RA+40],[-RA-40,RA+40]]; SD.forEach((o,j)=>{ if(i!==j&&Math.hypot(o.x-s.x,o.y-s.y)<70) poly=clipH(poly,(s.x+o.x)/2,(s.y+o.y)/2,o.x-s.x,o.y-s.y); }); return poly; });
  function crys(x,y,L,rot,m){ if(L<=0.3) return; const asp=[1.25,1.5,2.4,1.0,2.2,1.1][m], w=L/asp; ctx.save(); ctx.translate(x,y); ctx.rotate(rot); ctx.beginPath();
    if(m===4) ctx.rect(-L/2,-w/2,L,w); else { const n=m===1?8:6; for(let i=0;i<n;i++){ const a=(i+0.5)/n*Math.PI*2, X=Math.cos(a)*L/2, Y=Math.sin(a)*w/2; if(i) ctx.lineTo(X,Y); else ctx.moveTo(X,Y); } ctx.closePath(); }
    ctx.fillStyle=MCOL[m]; ctx.fill(); ctx.strokeStyle='rgba(15,23,42,.6)'; ctx.lineWidth=0.9; ctx.stroke();
    if(L>9){ ctx.lineWidth=0.6; if(m===4){ ctx.strokeStyle='rgba(148,163,184,.9)'; for(let j=-1;j<=1;j++) line(-L/2+1.5,j*w/4,L/2-1.5,j*w/4); } else if(m===3){ ctx.strokeStyle='rgba(180,130,70,.6)'; for(let j=-2;j<=2;j++) line(-L/2.7,j*w/7,L/2.7,j*w/7); } else if(m===5){ ctx.fillStyle='rgba(255,255,255,.6)'; ctx.beginPath(); ctx.ellipse(-L/6,-w/6,L/7,w/10,0.4,0,Math.PI*2); ctx.fill(); } else { ctx.strokeStyle='rgba(255,255,255,.3)'; line(-L/3,-w/5,L/3,-w/5); } }
    ctx.restore(); }
  function lath(x,y,L,rot,m){ const w=Math.max(0.9,L*0.32); ctx.save(); ctx.translate(x,y); ctx.rotate(rot); ctx.fillStyle=MCOL[m]; ctx.fillRect(-L/2,-w/2,L,w); ctx.restore(); }
  function detail(m,x,y,a){ ctx.lineWidth=0.7; const ux=Math.cos(a), uy=Math.sin(a), vx=-uy, vy=ux;
    if(m===4){ ctx.strokeStyle='rgba(148,163,184,.85)'; for(let j=-3;j<=3;j++) line(x+vx*j*3.2-ux*30,y+vy*j*3.2-uy*30,x+vx*j*3.2+ux*30,y+vy*j*3.2+uy*30); }
    else if(m===3){ ctx.strokeStyle='rgba(161,98,7,.55)'; for(let j=-6;j<=6;j++) line(x+vx*j*1.8-ux*30,y+vy*j*1.8-uy*30,x+vx*j*1.8+ux*30,y+vy*j*1.8+uy*30); }
    else if(m===5){ ctx.fillStyle='rgba(255,255,255,.6)'; ctx.beginPath(); ctx.ellipse(x-3,y-3,5,2.5,a,0,Math.PI*2); ctx.fill(); }
    else if(m===1||m===2){ ctx.strokeStyle='rgba(255,255,255,.25)'; for(let j=-1;j<=1;j+=2) line(x+vx*j*4-ux*30,y+vy*j*4-uy*30,x+vx*j*4+ux*30,y+vy*j*4+uy*30); }
    else { ctx.strokeStyle='rgba(0,0,0,.3)'; line(x-6,y-2,x+1,y+3); line(x+1,y+3,x+5,y-1); } }
  // ---- 火山の断面 ----
  function mark(s,x,y){ ctx.fillStyle='#fff'; ctx.strokeStyle='#0f172a'; ctx.lineWidth=1.6; ctx.beginPath(); ctx.arc(x,y,9,0,Math.PI*2); ctx.fill(); ctx.stroke(); txt(s,x,y+4,'bold 11px sans-serif','#0f172a','center'); }
  function tri(x,y){ ctx.fillStyle='#dc2626'; ctx.beginPath(); ctx.moveTo(x,y); ctx.lineTo(x-6,y-8); ctx.lineTo(x+6,y-8); ctx.closePath(); ctx.fill(); }
  function drawErupt(q,top){ const t=tm, wl=clamp(1-q*1.6,0,1), wa=clamp((q-0.22)/0.5,0,1), wb=clamp((q-0.3)/0.3,0,1), wp=clamp((q-0.7)/0.15,0,1), R=reach(q);
    if(wl>0.03){ const Lf=R*(0.35+0.6*wl); [-1,1].forEach((sd)=>{ ctx.beginPath(); for(let d=0;d<=Lf;d+=3){ const X=CX+sd*d, Y=GY-vh(d,q)-2; if(d===0) ctx.moveTo(X,Y+2); else ctx.lineTo(X,Y); }
        ctx.lineCap='round'; ctx.strokeStyle='rgba(220,38,38,'+(0.55+0.45*wl).toFixed(2)+')'; ctx.lineWidth=6; ctx.stroke(); ctx.setLineDash([6,10]); ctx.lineDashOffset=-t*26; ctx.strokeStyle='rgba(253,224,71,.9)'; ctx.lineWidth=2.4; ctx.stroke(); ctx.setLineDash([]); ctx.lineCap='butt'; });
      ctx.fillStyle='#f97316'; for(let i=0;i<12;i++){ const u=(t*1.1+i*0.137)%1, sd=i%2?1:-1, X=CX+sd*u*(6+(i%4)*4), Y=top-Math.sin(u*Math.PI)*(8+16*wl); ctx.beginPath(); ctx.arc(X,Y,1.8,0,Math.PI*2); ctx.fill(); }
      if(wl>0.35){ const dd=Lf*0.62; txt('溶岩が流れ出す',CX+dd,GY-vh(dd,q)-12,'bold 11px sans-serif','#b91c1c','left',true); } }
    if(wa>0.03){ const Hp=Math.min(top-SY0-4,60+150*wa); for(let i=15;i>=0;i--){ const u=(t*0.2+i/16)%1, yy=top-6-u*Hp, xx=CX+u*u*50+Math.sin(t*0.8+i*1.7)*3*u, r=5+u*(9+16*wa), g=Math.round(95+70*u);
        ctx.fillStyle='rgba('+g+','+(g-2)+','+(g-6)+','+(Math.min(1,(1-u)*1.1)*(0.4+0.5*wa)).toFixed(2)+')'; ctx.beginPath(); ctx.arc(xx,yy,r,0,Math.PI*2); ctx.fill(); }
      if(wa>0.35) txt('火山灰・軽石',CX+44,SY0+17,'bold 11px sans-serif','#44403c','left',true); }
    if(wb>0.05){ ctx.fillStyle='#1c1917'; ctx.globalAlpha=Math.min(1,wb); for(let i=0;i<8;i++){ const u=(t*0.55+i*0.127)%1, sd=i%2?1:-1, vx=sd*(28+i*7), vy=70+(i%3)*14, X=CX+vx*u*1.5, Y=top-(vy*u*1.5-60*u*u*2.25); if(Y>GY-vh(X-CX,q)) continue; ctx.beginPath(); ctx.ellipse(X,Y,2.8,2,u*3,0,Math.PI*2); ctx.fill(); } ctx.globalAlpha=1; }
    if(wp>0.05){ const u=(t*0.17)%1; for(let j=0;j<10;j++){ const uu=u-j*0.025; if(uu<0) continue; const d=uu*(R+130), X=CX+d, Y=GY-vh(d,q)-7; ctx.fillStyle='rgba(120,113,108,'+(0.5*wp*(1-uu*0.5)).toFixed(2)+')'; ctx.beginPath(); ctx.arc(X,Y,7+j*0.8+uu*12,0,Math.PI*2); ctx.fill(); }
      if(wp>0.4) txt('火砕流',CX+R+34,GY-26,'bold 12px sans-serif','#44403c','left',true); } }
  function drawInfo(q){ const c=cls(q);
    ctx.fillStyle='rgba(255,255,255,.92)'; ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1; rr(12,32,262,96,8); ctx.fill(); ctx.stroke();
    txt('火山の形：'+SH[c],22,54,'bold 15px sans-serif','#0f172a'); txt('（'+SHD[c]+'）',22,72,'11px sans-serif','#475569');
    txt('例：'+EXN[c],22,92,'12px sans-serif','#0f172a'); txt('噴火：'+ERD[c],22,114,'bold 11px sans-serif','#9a3412');
    ctx.fillStyle='rgba(255,255,255,.92)'; ctx.strokeStyle='#cbd5e1'; rr(GX-10,32,GW+20,96,8); ctx.fill(); ctx.stroke();
    txt('マグマのねばりけ：'+NB[c],GX,47,'bold 11px sans-serif','#0f172a');
    const ZC=['#fde68a','#fdba74','#fca5a5']; ZC.forEach((col,i)=>{ ctx.fillStyle=col; ctx.fillRect(GX+i*GW/3,53,GW/3,15); }); ctx.strokeStyle='#475569'; ctx.lineWidth=1; ctx.strokeRect(GX,53,GW,15);
    NB.forEach((s,i)=>{ txt(s,GX+(i+0.5)*GW/3,64,'10px sans-serif','#334155','center'); }); needle(GX+q*GW,68);
    txt('溶岩・岩石の色：'+CO[c],GX,93,'bold 11px sans-serif','#0f172a');
    const cg=ctx.createLinearGradient(GX,0,GX+GW,0); cg.addColorStop(0,rgb(rockC(0))); cg.addColorStop(0.5,rgb(rockC(0.5))); cg.addColorStop(1,rgb(rockC(1))); ctx.fillStyle=cg; ctx.fillRect(GX,99,GW,14); ctx.strokeStyle='#475569'; ctx.lineWidth=1; ctx.strokeRect(GX,99,GW,14); needle(GX+q*GW,113);
    txt('黒っぽい',GX+4,110,'10px sans-serif','#ffffff','left'); txt('白っぽい',GX+GW-4,110,'10px sans-serif','#1f2937','right'); }
  function needle(x,y1){ ctx.strokeStyle='#dc2626'; ctx.lineWidth=2.5; line(x,y1-4,x,y1+2); ctx.fillStyle='#dc2626'; ctx.beginPath(); ctx.moveTo(x,y1+1); ctx.lineTo(x-6,y1+9); ctx.lineTo(x+6,y1+9); ctx.closePath(); ctx.fill(); }
  function drawScene(){ const q=p, w=shW(q), top=GY-vh(0,q), rc=rockC(q);
    txt('マグマのねばりけと火山（断面のイメージ）',8,18,'bold 14px sans-serif','#0f172a');
    txt('右上のゲージをタップ・ドラッグしても変えられます',632,18,'11px sans-serif','#64748b','right');
    ctx.save(); rr(6,SY0,628,SY1-SY0,10); ctx.clip();
    const sk=ctx.createLinearGradient(0,SY0,0,GY); sk.addColorStop(0,'#bfdbfe'); sk.addColorStop(1,'#f0f9ff'); ctx.fillStyle=sk; ctx.fillRect(6,SY0,628,GY-SY0);
    const gg=ctx.createLinearGradient(0,GY,0,SY1); gg.addColorStop(0,'#c9a77c'); gg.addColorStop(1,'#7c5c3e'); ctx.fillStyle=gg; ctx.fillRect(6,GY,628,SY1-GY);
    ctx.strokeStyle='rgba(80,50,20,.18)'; ctx.lineWidth=1; for(let y=GY+13;y<SY1;y+=13) line(6,y,634,y);
    const mg=ctx.createRadialGradient(CX,MCY,4,CX,MCY,92); mg.addColorStop(0,'#fde047'); mg.addColorStop(0.5,'#f97316'); mg.addColorStop(1,'#b91c1c'); ctx.fillStyle=mg; ctx.beginPath(); ctx.ellipse(CX,MCY,90,21,0,0,Math.PI*2); ctx.fill();
    txt('マグマだまり',CX-46,MCY+5,'bold 12px sans-serif','#fff','center');
    ctx.beginPath(); ctx.moveTo(CX-330,GY+1); for(let dx=-330;dx<=330;dx+=3) ctx.lineTo(CX+dx,GY-vh(dx,q)); ctx.lineTo(CX+330,GY+1); ctx.closePath();
    const vg=ctx.createLinearGradient(0,GY-130,0,GY); vg.addColorStop(0,rgb(mixc(rc,[255,255,255],0.18))); vg.addColorStop(1,rgb(rc)); ctx.fillStyle=vg; ctx.fill();
    if(w[1]>0.05){ ctx.save(); ctx.clip(); for(let j=1;j<=4;j++){ const s=1-j*0.18; ctx.beginPath(); let st=false; for(let dx=-330;dx<=330;dx+=3){ const hh=s*vh(dx/s,q); if(hh<1.5){ st=false; continue; } const X=CX+dx, Y=GY-hh; if(!st){ ctx.moveTo(X,Y); st=true; } else ctx.lineTo(X,Y); }
        ctx.strokeStyle=j%2?'rgba(255,255,255,'+(0.4*w[1]).toFixed(2)+')':'rgba(0,0,0,'+(0.28*w[1]).toFixed(2)+')'; ctx.lineWidth=2; ctx.stroke(); } ctx.restore(); }
    ctx.strokeStyle='rgba(15,23,42,.6)'; ctx.lineWidth=1.5; ctx.beginPath(); for(let dx=-330;dx<=330;dx+=3){ const X=CX+dx, Y=GY-vh(dx,q); if(dx===-330) ctx.moveTo(X,Y); else ctx.lineTo(X,Y); } ctx.stroke();
    ctx.strokeStyle='#ea580c'; ctx.lineWidth=6; line(CX,MCY-19,CX,top+2); ctx.strokeStyle='#fed7aa'; ctx.lineWidth=2; line(CX,MCY-19,CX,top+2);
    if(erupting) drawErupt(q,top);
    const da=Math.min(64,reach(q)*0.42), ya=GY-vh(-da,q);
    mark('ア',CX-da,ya-3); txt('地表付近：急に冷える',CX-da-14,ya-1,'bold 11px sans-serif','#0f172a','right',true);
    mark('イ',CX+108,MCY); txt('地下深く：ゆっくり冷える',CX+122,MCY+4,'bold 11px sans-serif','#0f172a','left',true);
    ctx.restore(); drawInfo(q);
    ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1; rr(6,SY0,628,SY1-SY0,10); ctx.stroke(); }
  // ---- 結晶のでき方（ルーペで見たようす） ----
  function drawA(c){ const cx=CA.x, cy=CA.y; ctx.save(); ctx.beginPath(); ctx.arc(cx,cy,RA,0,Math.PI*2); ctx.clip();
    const mx=ease((ct-3.45)/1.2); ctx.fillStyle='#fb923c'; ctx.fillRect(cx-RA,cy-RA,RA*2,RA*2); if(mx>0){ ctx.globalAlpha=mx; ctx.fillStyle=rgb(glassC(p)); ctx.fillRect(cx-RA,cy-RA,RA*2,RA*2); ctx.globalAlpha=1; }
    GM.forEach((g)=>{ const s=ease((ct-g.t0)/0.35); if(s>0) lath(cx+g.x,cy+g.y,g.L*s,g.rot,pick(g.u,c)); });
    PH.forEach((h)=>{ const s=ease((ct-h.t0)/(3.0-h.t0)); if(s>0) crys(cx+h.x,cy+h.y,h.L*s,h.rot,pick(h.u,c)); });
    ctx.restore(); }
  function drawB(c){ const cx=CB.x, cy=CB.y; ctx.save(); ctx.beginPath(); ctx.arc(cx,cy,RA,0,Math.PI*2); ctx.clip();
    ctx.fillStyle='#fb923c'; ctx.fillRect(cx-RA,cy-RA,RA*2,RA*2);
    SD.forEach((s,i)=>{ const kk=ease((ct-s.t0)/s.d); if(kk<=0) return; const m=pick(s.u,c), poly=CELL[i];
      ctx.beginPath(); poly.forEach((v,j)=>{ const X=cx+s.x+(v[0]-s.x)*kk, Y=cy+s.y+(v[1]-s.y)*kk; if(j) ctx.lineTo(X,Y); else ctx.moveTo(X,Y); }); ctx.closePath();
      ctx.fillStyle=MCOL[m]; ctx.fill(); ctx.strokeStyle='rgba(15,23,42,.6)'; ctx.lineWidth=0.9; ctx.stroke();
      if(kk>0.6){ ctx.save(); ctx.clip(); detail(m,cx+s.x,cy+s.y,s.ang); ctx.restore(); } });
    ctx.restore(); }
  function drawCrystals(){ const c=comp(p), k=cls(p), surf=$('cool').value==='surf';
    txt('ア 火山岩',CA.x,314,'bold 13px sans-serif','#0f172a','center'); txt('地表付近で急に冷えた',CA.x,328,'11px sans-serif','#475569','center');
    txt('イ 深成岩',CB.x,314,'bold 13px sans-serif','#0f172a','center'); txt('地下深くでゆっくり冷えた',CB.x,328,'11px sans-serif','#475569','center');
    drawA(c); drawB(c);
    const RG=[[CA,surf],[CB,!surf]]; RG.forEach((o)=>{ ctx.strokeStyle=o[1]?'#f59e0b':'#334155'; ctx.lineWidth=o[1]?4:2; ctx.beginPath(); ctx.arc(o[0].x,o[0].y,RA+(o[1]?1:0),0,Math.PI*2); ctx.stroke(); });
    if(ct>=4.7){ const h=PH.reduce((a,b)=>(b.x>a.x?b:a),PH[0]); ctx.strokeStyle='#0f172a'; ctx.lineWidth=1.2; line(160,358,CA.x+h.x+4,CA.y+h.y-2); txt('斑晶',162,362,'bold 12px sans-serif','#0f172a','left',true);
      line(160,436,CA.x+44,CA.y+30); ctx.fillStyle='#0f172a'; ctx.beginPath(); ctx.arc(CA.x+44,CA.y+30,2,0,Math.PI*2); ctx.fill(); txt('石基',162,440,'bold 12px sans-serif','#0f172a','left',true); }
    const capA=ct<3.45?['① 地下でゆっくり冷えて','大きな結晶（斑晶）が育つ']:(ct<4.7?['② 地表付近で急に冷えて','小さな結晶とガラス（石基）に']:null);
    if(capA){ txt(capA[0],CA.x,471,'bold 11px sans-serif','#9a3412','center'); txt(capA[1],CA.x,486,'bold 11px sans-serif','#9a3412','center'); }
    else { txt('斑状組織',CA.x,471,'bold 13px sans-serif','#0f172a','center'); txt('→ '+VR[k],CA.x,488,'bold 13px sans-serif','#b45309','center'); }
    if(ct<4.8){ txt('地下深くでゆっくり冷えて',CB.x,471,'bold 11px sans-serif','#9a3412','center'); txt('結晶が大きく育つ',CB.x,486,'bold 11px sans-serif','#9a3412','center'); }
    else { txt('等粒状組織',CB.x,471,'bold 13px sans-serif','#0f172a','center'); txt('→ '+PR[k],CB.x,488,'bold 13px sans-serif','#b45309','center'); } }
  // ---- 分類表 ----
  function drawTable(){ const k=cls(p), surf=$('cool').value==='surf', X0=336, W0=84, CWD=70, Y0=304, RH=[22,30,30,22,22,22];
    const rows=[['','黒っぽい','中間','白っぽい'],['火山岩|斑状組織'].concat(VR),['深成岩|等粒状組織'].concat(PR),['マグマのねばりけ'].concat(NB),['火山の形'].concat(SH),['噴火のようす'].concat(ER)];
    const tot=RH.reduce((a,b)=>a+b,0), HC=[[62,60,60],[136,128,121],[222,215,204]];
    ctx.fillStyle='rgba(251,191,36,.22)'; ctx.fillRect(X0+W0+k*CWD,Y0,CWD,tot);
    let y=Y0; rows.forEach((r,ri)=>{ let x=X0; r.forEach((s,ci)=>{ const w=ci?CWD:W0, h=RH[ri];
        if(ri===0){ if(ci){ ctx.fillStyle=rgb(HC[ci-1]); ctx.fillRect(x,y,w,h); txt(s,x+w/2,y+15,'bold 11px sans-serif',ci===3?'#1f2937':'#ffffff','center'); } }
        else { ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1; ctx.strokeRect(x+0.5,y+0.5,w,h);
          if(!ci){ const sp=s.split('|'); if(sp.length>1){ txt(sp[0],x+5,y+13,'bold 11px sans-serif','#0f172a'); txt(sp[1],x+5,y+26,'10px sans-serif','#475569'); } else txt(s,x+5,y+15,(s.length>6?'10px':'bold 11px')+' sans-serif','#0f172a'); }
          else { const big=ri===1||ri===2; txt(s,x+w/2,y+(big?20:15),(big?'bold 13px':'11px')+' sans-serif',ci-1===k?'#0f172a':'#64748b','center'); } }
        x+=w; }); y+=RH[ri]; });
    ctx.strokeStyle='#ea580c'; ctx.lineWidth=3; ctx.strokeRect(X0+W0+k*CWD+1.5,Y0+22+(surf?0:30)+1.5,CWD-3,27);
    txt('冷え方 → つくり（組織）、鉱物の割合 → 色',X0,Y0+tot+17,'11px sans-serif','#475569'); txt('表や円をタップすると切りかわります',X0,Y0+tot+33,'10px sans-serif','#64748b'); }
  // ---- 鉱物の割合 ----
  function drawMinerals(){ const X0=52, X1=388, Y0=516, Y1=612, xs=(t)=>X0+t*(X1-X0), ys=(v)=>Y1-v/100*(Y1-Y0), k=cls(p);
    txt('ふくまれる鉱物の割合（体積の割合のおおよその目安）',8,504,'bold 13px sans-serif','#0f172a');
    let lo=[]; for(let j=0;j<=20;j++) lo.push(0);
    for(let m=0;m<6;m++){ const up=lo.map((v,j)=>v+comp(j/20)[m]); ctx.beginPath(); up.forEach((v,j)=>{ if(j) ctx.lineTo(xs(j/20),ys(v)); else ctx.moveTo(xs(0),ys(v)); }); for(let j=20;j>=0;j--) ctx.lineTo(xs(j/20),ys(lo[j])); ctx.closePath();
      ctx.fillStyle=MCOL[m]; ctx.fill(); ctx.strokeStyle='rgba(15,23,42,.3)'; ctx.lineWidth=0.8; ctx.stroke(); lo=up;
      if(m===3){ ctx.strokeStyle='#0f172a'; ctx.lineWidth=2; ctx.beginPath(); up.forEach((v,j)=>{ if(j) ctx.lineTo(xs(j/20),ys(v)); else ctx.moveTo(xs(0),ys(v)); }); ctx.stroke(); } }
    ctx.save(); ctx.setLineDash([3,3]); ctx.strokeStyle='rgba(255,255,255,.85)'; ctx.lineWidth=1; line(xs(1/3),Y0,xs(1/3),Y1); line(xs(2/3),Y0,xs(2/3),Y1); ctx.restore();
    ctx.strokeStyle='#334155'; ctx.lineWidth=1; ctx.strokeRect(X0,Y0,X1-X0,Y1-Y0);
    const TK=[0,50,100]; TK.forEach((v)=>{ txt(v+'%',X0-4,ys(v)+4,'10px sans-serif','#475569','right'); });
    txt('キ石',xs(0.08),ys(27),'bold 11px sans-serif','#fff','center'); txt('カクセン石',xs(0.36),ys(31),'bold 11px sans-serif','#fff','center');
    txt('チョウ石',xs(0.38),ys(66),'bold 12px sans-serif','#334155','center'); txt('セキエイ',xs(0.88),ys(88),'bold 11px sans-serif','#334155','center');
    const bm=mafic(0.78); txt('↑ 無色鉱物',xs(0.74),ys(bm)-5,'bold 10px sans-serif','#0f172a','left',true); txt('↓ 有色鉱物',xs(0.74),ys(bm)+13,'bold 10px sans-serif','#0f172a','left',true);
    ctx.strokeStyle='#dc2626'; ctx.lineWidth=2.5; line(xs(p),Y0-2,xs(p),Y1+2); tri(xs(p),Y0-2);
    const XL=[[1/6,'玄武岩・斑れい岩'],[0.5,'安山岩・閃緑岩'],[5/6,'流紋岩・花こう岩']]; XL.forEach((o,i)=>{ txt(o[1],xs(o[0]),Y1+14,(i===k?'bold ':'')+'10px sans-serif',i===k?'#b45309':'#334155','center'); });
    txt('← 黒っぽい・ねばりけ弱い',X0,Y1+29,'10px sans-serif','#475569','left'); txt('白っぽい・ねばりけ強い →',X1,Y1+29,'10px sans-serif','#475569','right');
    const cq=comp(p); let y=520; txt('いまのマグマ（ねばりけ'+NB[k]+'）',402,y,'bold 12px sans-serif','#0f172a');
    for(let m=5;m>=0;m--){ y+=15; ctx.fillStyle=MCOL[m]; ctx.fillRect(402,y-10,13,11); ctx.strokeStyle='#64748b'; ctx.lineWidth=0.8; ctx.strokeRect(402,y-10,13,11); txt(MIN[m],421,y,'11px sans-serif','#1e293b'); const v=cq[m]; txt(v<0.5?'ほぼなし':'約'+Math.round(v)+'％',630,y,'bold 11px sans-serif','#0f172a','right'); }
    y+=21; txt('有色鉱物：約'+Math.round(mafic(p)/5)*5+'％',402,y,'bold 12px sans-serif','#0f172a'); y+=17; txt('→ 岩石は'+CO[k],402,y,'bold 12px sans-serif','#9a3412'); }
  function updStats(){ const k=cls(p), surf=$('cool').value==='surf';
    setStat('sShape',SH[k]); setStat('sErupt',ER[k]); setStat('sRock',surf?VR[k]:PR[k]); setStat('sTex',surf?'斑状組織':'等粒状組織'); setStat('sColor',CO[k]); setStat('sMafic','約'+Math.round(mafic(p)/5)*5+'％');
    setShare('【火山と火成岩】マグマのねばりけが'+NB[k]+' → '+SH[k]+'（例：'+EXN[k]+'）・噴火は'+ER[k]+'。地表付近で急に冷えると'+VR[k]+'（斑状組織）、地下深くでゆっくり冷えると'+PR[k]+'（等粒状組織）｜シミュラボ'); }
  function draw(){ ctx.clearRect(0,0,W,H); ctx.fillStyle='#fff'; ctx.fillRect(0,0,W,H); drawScene(); drawCrystals(); drawTable(); drawMinerals(); updStats(); }
  // ---- 操作 ----
  function viscLabel(){ $('viscL').textContent=NB[cls(p)]+'（'+Math.round(p*100)+'）'; }
  function setP(v){ p=clamp(v,0,1); $('visc').value=Math.round(p*100); viscLabel(); $('ex').value=''; dirty=true; }
  $('visc').addEventListener('input',()=>{ p=+$('visc').value/100; viscLabel(); $('ex').value=''; dirty=true; });
  $('ex').addEventListener('change',()=>{ const v=$('ex').value; if(v!==''){ p=+v/100; $('visc').value=+v; viscLabel(); } dirty=true; });
  $('cool').addEventListener('change',()=>{ dirty=true; });
  $('grow').addEventListener('click',()=>{ ct=0; dirty=true; });
  $('erupt').addEventListener('click',()=>{ erupting=!erupting; $('erupt').textContent=erupting?'⏸ 噴火を止める':'▶ 噴火させる'; dirty=true; });
  function pxy(e){ const q=cpos(cv,e); return [q[0]/dpr,q[1]/dpr]; }
  cv.addEventListener('pointerdown',(e)=>{ const q=pxy(e), x=q[0], y=q[1]; let hit=false;
    if(x>=GX-10&&x<=GX+GW+10&&y>=40&&y<=86){ drag='g'; setP((x-GX)/GW); hit=true; }
    else if(x>=52&&x<=388&&y>=508&&y<=640){ drag='m'; setP((x-52)/336); hit=true; }
    else if(Math.hypot(x-CA.x,y-CA.y)<=RA+6){ $('cool').value='surf'; dirty=true; return; }
    else if(Math.hypot(x-CB.x,y-CB.y)<=RA+6){ $('cool').value='deep'; dirty=true; return; }
    else if(x>=420&&x<=630&&y>=304&&y<=452){ const col=clamp(Math.floor((x-420)/70),0,2); setP((col+0.5)/3); if(y>=326&&y<356) $('cool').value='surf'; else if(y>=356&&y<386) $('cool').value='deep'; dirty=true; return; }
    if(hit){ try{ cv.setPointerCapture(e.pointerId); }catch(err){ } e.preventDefault(); } });
  cv.addEventListener('pointermove',(e)=>{ if(!drag) return; const q=pxy(e); setP(drag==='g'?(q[0]-GX)/GW:(q[0]-52)/336); });
  ['pointerup','pointercancel'].forEach((n)=>cv.addEventListener(n,()=>{ drag=''; }));
  function loop(now){ const dt=Math.min(0.05,Math.max(0,(now-last)/1000)); last=now; let ch=dirty; if(erupting){ tm+=dt; ch=true; } if(ct<6){ ct+=dt; ch=true; } if(ch){ dirty=false; draw(); } requestAnimationFrame(loop); }
  viscLabel(); draw(); requestAnimationFrame(loop);
''')
