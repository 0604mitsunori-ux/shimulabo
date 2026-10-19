# -*- coding: utf-8 -*-
"""理科の授業向け：植物（中2 植物の体のつくりと働き／小6 植物の養分と水の通り道／小5 植物の発芽，成長，結実）"""
import math
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

MEXT_SHO = "https://www.mext.go.jp/a_menu/shotou/new-cs/1387014.htm"
MEXT_CHU = "https://www.mext.go.jp/a_menu/shotou/new-cs/1387016.htm"

# ---- 光合成のモデル（相対値）。JS と同じ式で記事の数値を計算する
PMAX, KL, R0 = 4.0, 40.0, 1.0
def Pf(L): return PMAX * (1 - math.exp(-L / KL))
LC = -KL * math.log(1 - R0 / PMAX)                       # 出入りがつり合う光の強さ（約11.5）
def sunL(h): return 100 * math.sin(math.pi * (h - 6) / 12) if 6 < h < 18 else 0.0
TB = 6 + 12 / math.pi * math.asin(LC / 100); TE = 24 - TB  # つり合う時刻
DAYP = sum(Pf(sunL((i + 0.5) * 24 / 24000)) * 24 / 24000 for i in range(24000))
def hm(h):
    m = int(round(h * 60)); return "%d時%02d分" % (m // 60, m % 60)
def f1(v): return "%.1f" % (round(v * 10) / 10)
def sg(v): return ("＋" if v > 0.05 else ("−" if v < -0.05 else "±")) + f1(abs(v))
# 蒸散（光の強さ100・6時間）mL：葉の表0.2・裏0.6 mL/時 ×(0.2+0.8×光/100)、茎 0.4/6 mL/時
JF, JB, JS = 0.2 * 6, 0.6 * 6, 0.4
JA, JBB, JC, JD = JF + JB + JS, JB + JS, JF + JS, JS

def _light_rows():
    rows = []
    for L, lab in [(0, "0（まっ暗）"), (5, "5"), (LC, "約%.1f" % LC), (20, "20"), (40, "40"), (60, "60"), (100, "100（強い）")]:
        p = Pf(L); n = p - R0
        io = "酸素を取り入れ、二酸化炭素を出す（呼吸だけ）" if L == 0 else ("酸素を取り入れ、二酸化炭素を出す" if n < -0.05 else ("見かけの出入りなし（つり合う）" if abs(n) <= 0.05 else "酸素を出し、二酸化炭素を取り入れる"))
        rows.append([lab, f1(p), "1.0", sg(n), io])
    return rows

# ============================================================ 1 光合成と呼吸
KOUGOU_ARTICLE = "<h2>このシミュレーションでわかること</h2>\n" + P(
    "植物は、光が当たっているときは<b>光合成</b>と<b>呼吸</b>を同時に行い、光が当たらないときは<b>呼吸だけ</b>を行います。"
    "光が強いと光合成のほうが多くなるので、葉全体では<b>酸素を出し、二酸化炭素を取り入れます</b>。暗いと呼吸だけになり、酸素を取り入れて二酸化炭素を出します。"
    "その間のある明るさ（このシミュレーションでは光の強さ 約%d）で、気体の出入りがつり合います。" % round(LC)) + '''
<p>中学校2年の理科「生物の体のつくりと働き」の<b>植物の体のつくりと働き</b>（第2分野（3）ア（ｲ）㋐ 葉・茎・根のつくりと働き）と、小学校6年の理科「<b>植物の養分と水の通り道</b>」（第6学年 B（2））で学ぶ内容です。中学校の学習指導要領解説（理科編 p.88）は、光合成と呼吸が「気体の出入りに関して逆の関係にある」ことに注目させることが大切だとしています。小学校の解説（理科編 p.87）は、観察・実験とともに「映像や模型，その他の資料を活用すること」を挙げています。</p>
<p>画面は4つです。<b>①気体の出入り</b>では、光の強さ（または晴れた日の時刻）を変えると、葉が取り入れる・出す酸素と二酸化炭素の矢印の太さが変わり、光合成量・呼吸量・差し引きがグラフで分かります。<b>②BTB溶液</b>はオオカナダモを入れた試験管の色の変化（対照実験つき）、<b>③ヨウ素液</b>は葉にデンプンができたかを調べる実験（ふ入りの葉・アルミはく／小6の3枚の葉）、<b>④蒸散</b>はワセリンをぬった枝で水の減り方をくらべる実験です。数値はすべて<b>相対値</b>（くらべるための目安の値）です。</p>
<h2>授業での使い方</h2>
<ul>
<li><b>導入</b>：「植物は呼吸をしているか」「夜、植物は何をしているか」を予想させてから、①で光の強さを0にし、呼吸だけのときの矢印を見せます。次に光を強くしていき、矢印の太さの変化を観察します。</li>
<li><b>展開</b>：②でBTB溶液の実験の結果を予想させ、A〜Dのどれとどれをくらべると何が分かるか（対照実験）を話し合います。光の強さを弱くすると、Aの色があまり変わらなくなることも確かめられます。③④は、実際の実験の前の見通しや、結果の確認に使えます。</li>
<li><b>まとめ</b>：①を「晴れた日（時刻）」にして1日を早送りし、朝・昼・夜で気体の出入りがどう変わるかを説明させます。光合成と呼吸の式を書き、取り入れる気体と出す気体が逆になっていることを確かめます。画面のアドレスの最後に <code>#btb</code>・<code>#youso</code>・<code>#jousan</code> を付けると、その画面から始まります。</li>
</ul>
<p>生徒・児童への問いの例：</p>
<ol>
<li>暗い所に置いた植物は、酸素と二酸化炭素のどちらを出しているでしょう。それはなぜでしょう。</li>
<li>BTB溶液の実験で、オオカナダモを入れない試験管（C・D）を用意するのはなぜでしょう。</li>
<li>葉の表・裏にワセリンをぬった実験の結果から、葉の裏から出た水の量を求めましょう。（答え：B − D、または A − C）</li>
</ol>
<h2>しくみ・解説</h2>
<h3>光合成・呼吸・蒸散とは</h3>
<ul>
<li><b>光合成</b>とは、植物が光のエネルギーを使って、二酸化炭素と水からデンプンなどの養分と酸素をつくるはたらきです。細胞の中の<b>葉緑体</b>で行われます。</li>
<li><b>呼吸</b>とは、細胞がデンプンなどの養分を酸素を使って分解し、生きるためのエネルギーを取り出すはたらきです。二酸化炭素と水ができます。植物も動物も、昼も夜も行っています。</li>
<li><b>蒸散</b>とは、根から吸い上げた水が、主に葉の<b>気孔</b>から水蒸気になって出ていくことです。</li>
<li><b>気孔</b>とは、葉の表皮にある、2つの孔辺細胞に囲まれたすきまで、酸素・二酸化炭素の出入りや蒸散の出口になります。</li>
</ul>
''' + N("光合成：二酸化炭素 ＋ 水 →（光のエネルギー・葉緑体）→ デンプンなど ＋ 酸素<br>呼吸：デンプンなど ＋ 酸素 → 二酸化炭素 ＋ 水（生きるためのエネルギーを取り出す）<br>差し引き（見かけの光合成）＝ 光合成量 − 呼吸量") + T(
    [["行う所", "葉緑体（葉などの緑色の部分）", "すべての生きている細胞"],
     ["行うとき", "光が当たっているときだけ", "昼も夜もいつも"],
     ["取り入れる気体", "二酸化炭素", "酸素"],
     ["出す気体", "酸素", "二酸化炭素"],
     ["養分（デンプンなど）", "つくる", "使う（分解してエネルギーを取り出す）"]],
    ["", "光合成", "呼吸"]) + '''
<h3>光の強さと気体の出入り（早見表・相対値）</h3>
<p>このシミュレーションでは、光合成量 ＝ 4 ×（1 − e<sup>−光の強さ÷40</sup>）、呼吸量 ＝ 1（光の強さで変わらない）としています。光合成量は、光が弱いうちは光を強くするほど大きく増え、強くなるにつれて増え方が小さくなります。</p>
''' + T(_light_rows(), ["光の強さ", "光合成量", "呼吸量", "差し引き", "葉全体の気体の出入り"]) + '''
''' + N("<b>発展（高校で学ぶ言葉）</b>：光合成量と呼吸量が等しくなり、見かけの気体の出入りがなくなる光の強さを<b>補償点</b>（光補償点）といいます。このシミュレーションでは光の強さ 約%.1f です。光をそれ以上強くしても光合成量がほとんど増えなくなる光の強さを<b>光飽和点</b>といいます。中学校では「光が弱いと、光合成で出す酸素より呼吸で使う酸素のほうが多くなる」ところまで分かれば十分です。" % LC) + '''
<h3>晴れた日の1日の変化</h3>
<p>「晴れた日（時刻）」にすると、6時に日がのぼり、12時に光がいちばん強く、18時にしずむとして光の強さを変えます。夜（18時〜6時）は呼吸だけなので、葉は二酸化炭素を出しています。朝、光が強くなっていくと <b>%s</b>ごろに出入りがつり合い、そのあとは酸素を出すようになります。夕方は <b>%s</b>ごろに再びつり合います。</p>
''' % (hm(TB), hm(TE)) + T([["光合成量の合計", f1(DAYP)], ["呼吸量の合計（1 × 24時間）", "24.0"], ["差し引き", sg(DAYP - 24)]],
                           ["晴れた日の1日（相対値）", "値"]) + '''
<p>1日全体では光合成量のほうが大きいので、植物は養分をたくわえて成長できます。くもりの日や日かげでは光合成量が小さくなります。</p>
<h3>BTB溶液とオオカナダモの実験（対照実験）</h3>
<p>BTB溶液は、酸性で<b>黄色</b>、中性で<b>緑色</b>、アルカリ性で<b>青色</b>になる液です。二酸化炭素は水にとけると酸性を示すので、二酸化炭素が増えると黄色に、減ると青色に近づきます。青色のBTB溶液に息をふきこんで緑色にしてから、4本の試験管に分けて実験します。</p>
''' + T([["A", "入れる", "当てる", "青色", "光合成で二酸化炭素が使われて減った"],
          ["B", "入れる", "当てない（アルミはく）", "黄色", "呼吸だけなので二酸化炭素が増えた"],
          ["C", "入れない", "当てる", "緑色のまま", "光だけでは色は変わらない"],
          ["D", "入れない", "当てない（アルミはく）", "緑色のまま", "時間がたつだけでは色は変わらない"]],
         ["試験管", "オオカナダモ", "光", "結果", "わかること"]) + '''
<p><b>対照実験</b>とは、調べたい条件だけを変え、それ以外の条件をすべて同じにして行い、結果をくらべる実験です。AとCをくらべると、ちがうのはオオカナダモがあるかないかだけなので、Aの色の変化はオオカナダモのはたらきによるものだと分かります。AとBをくらべると、ちがうのは光が当たるかどうかだけです。光を弱くすると、光合成と呼吸がつり合ってAの色があまり変わらなくなります。</p>
<h3>ヨウ素液でデンプンを調べる実験</h3>
<ol>
<li>前の日から植物を暗い所に置き、葉のデンプンをなくしておきます。ふ入りの葉（アサガオなど）の一部をアルミはくでおおいます。</li>
<li>光を数時間当てます。</li>
<li>葉をとってアルミはくを外し、熱湯につけてやわらかくしてから、あたためたエタノールにつけて緑色をぬきます（脱色）。エタノールは火を使わずに湯であたためます。</li>
<li>水で洗ってヨウ素液につけると、デンプンがある所が<b>青紫色</b>になります。</li>
</ol>
''' + T([["a 緑色の部分・光が当たった", "ある", "当たった", "青紫色になる"],
          ["b ふ（白い部分）・光が当たった", "ない", "当たった", "変化なし"],
          ["c 緑色の部分・アルミはく", "ある", "当たらない", "変化なし"],
          ["d ふ・アルミはく", "ない", "当たらない", "変化なし"]],
         ["葉の部分", "葉緑体", "光", "ヨウ素液"]) + '''
<p>aとcをくらべると、デンプンをつくるには<b>光が必要</b>なことが、aとbをくらべると、デンプンは<b>葉の緑色の部分（葉緑体）</b>でつくられることが分かります。小学校6年では、前の日にアルミはくをかぶせた3枚の葉ア・イ・ウを使い、アは朝すぐ、イは日光に当ててから、ウはおおったまま調べて、イだけがでんぷんで青むらさき色になることを確かめます（湯でにてからエタノールで色をぬく方法のほか、ろ紙にはさんでたたく「たたき染め」の方法もあります）。</p>
<h3>蒸散の実験（ワセリンで気孔をふさぐ）</h3>
<p>葉の数と大きさをそろえた枝を水の入った試験管（メスシリンダー）にさし、水面に油をたらして水面からの蒸発を防ぎます。ワセリンをぬった所からは蒸散が起こらないので、水の減り方をくらべると、どこから水が出ていったかが分かります。下の表は、光の強さ100・6時間のときのこのシミュレーションの値です。</p>
''' + T([["A", "何もぬらない", "表＋裏＋茎", f1(JA) + "mL"],
          ["B", "葉の表にワセリン", "裏＋茎", f1(JBB) + "mL"],
          ["C", "葉の裏にワセリン", "表＋茎", f1(JC) + "mL"],
          ["D", "葉をとって切り口にワセリン", "茎だけ", f1(JD) + "mL"]],
         ["試験管", "条件", "水が出ていく所", "減った水の量"]) + N(
    "葉の表から ＝ C − D ＝ %s − %s ＝ %smL<br>葉の裏から ＝ B − D ＝ %s − %s ＝ %smL（A − C でも同じ）<br>茎から ＝ D ＝ %smL<br>A ＝ 表 ＋ 裏 ＋ 茎 ＝ %s ＋ %s ＋ %s ＝ %smL"
    % (f1(JC), f1(JD), f1(JF), f1(JBB), f1(JD), f1(JB), f1(JD), f1(JF), f1(JB), f1(JS), f1(JA))) + '''
<p>葉の裏からの蒸散がいちばん多いのは、多くの植物で<b>気孔が葉の裏側に多い</b>からです（植物の種類によってちがいます）。蒸散が起こると、根から水が吸い上げられます。小学校6年の解説は、蒸散の量を調べるときは気温が高い晴れの日を選ぶとしています。</p>
<h3>このシミュレーションで単純にしていること</h3>
<ul>
<li>光合成量・呼吸量・色の変わり方・水の量は、くらべやすくするための<b>相対値・目安</b>です。実際の値は植物の種類・葉の大きさ・温度・二酸化炭素の濃さなどで変わります。</li>
<li>呼吸量は光の強さや時刻で変わらないものとしています（実際は温度で変わります）。</li>
<li>BTB溶液の色は、光合成と呼吸の差し引きで二酸化炭素が増えたか減ったかだけで決めています。B・Dのアルミはくは、色が見えるように透かして描いています。</li>
<li>蒸散の量は、葉の表0.2mL・裏0.6mL・茎約0.07mL（1時間あたり、光の強さ100のとき）とし、葉からの蒸散は暗いと少なくなる（気孔が閉じる）ようにしています。</li>
</ul>
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「中学校学習指導要領（平成29年告示）解説 理科編」第2分野（3）ア（ｲ）植物の体のつくりと働き（pp.87〜88）（<a href="''' + MEXT_CHU + '''" target="_blank" rel="noopener">文部科学省 中学校学習指導要領解説のページ</a>）</li>
<li>文部科学省「小学校学習指導要領（平成29年告示）解説 理科編」第6学年 B（2）植物の養分と水の通り道（pp.86〜87）（<a href="''' + MEXT_SHO + '''" target="_blank" rel="noopener">文部科学省 小学校学習指導要領解説のページ</a>）</li>
<li>中学校理科（2年）の教科書の「植物の体のつくりと働き」の章、小学校理科（6年）の教科書の「植物の養分と水の通り道」の単元</li>
</ul>
'''

KOUGOU_FAQS = [
    ("植物は光合成と呼吸を同時に行っているのですか？", "はい。光が当たっているときは光合成と呼吸を同時に行っています。光が強いと光合成のほうが多いので、葉全体では酸素を出し二酸化炭素を取り入れているように見えます。光が当たらない夜は呼吸だけを行っています。"),
    ("夜、植物は二酸化炭素を出しているのですか？", "はい。夜は光合成ができないので呼吸だけになり、酸素を取り入れて二酸化炭素を出しています。ただし晴れた日の1日全体では、昼の光合成で取り入れる二酸化炭素のほうが多くなります。"),
    ("BTB溶液の実験で、オオカナダモを入れると青色になるのはなぜですか？", "光が当たるとオオカナダモが光合成を行い、水にとけている二酸化炭素を使うからです。二酸化炭素が減ると液が酸性からアルカリ性のほうに変わり、BTB溶液は緑色から青色になります。光を当てないと呼吸だけになり、二酸化炭素が増えて黄色になります。"),
    ("対照実験とは何ですか？", "調べたい条件だけを変え、それ以外の条件をすべて同じにして行い、結果をくらべる実験です。BTB溶液の実験では、オオカナダモを入れない試験管を用意して、色の変化がオオカナダモのはたらきによるものであることを確かめます。"),
    ("ふ入りの葉で、ふの部分が青紫色にならないのはなぜですか？", "ふ（白い部分）の細胞には葉緑体がないので、光が当たっても光合成ができず、デンプンがつくられないからです。光が当たった緑色の部分だけがヨウ素液で青紫色になります。"),
    ("蒸散の実験で、葉の裏から出た水の量はどう求めますか？", "葉の表にワセリンをぬった試験管（裏と茎から水が出る）の減った量から、葉をとった試験管（茎だけ）の減った量を引きます。例：4.0mL − 0.4mL ＝ 3.6mL。何もぬらない試験管から、葉の裏にワセリンをぬった試験管の量を引いても求められます。"),
]

KOUGOU_JS = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const h1=document.querySelector('.sim-head h1'); if(h1&&!h1.children.length){ const t=h1.textContent, i=t.indexOf('（'); if(i>0){ h1.textContent=t.slice(0,i); const sp=document.createElement('span'); sp.style.display='inline-block'; sp.textContent=t.slice(i); h1.appendChild(sp); } }
  const bar=document.createElement('div'); bar.className='lab-btns'; bar.style.marginTop='0';
  ['tG','tB','tY','tJ'].forEach((id)=>{ const b=$(id); if(b) bar.appendChild(b); });
  cv.parentNode.insertBefore(bar,cv);
  const fld=(id)=>$(id).closest('.field');
  function setK(id,s){ const e=$(id); if(e&&e.previousElementSibling&&e.previousElementSibling.textContent!==s) e.previousElementSibling.textContent=s; }
  function setV(id,s){ const e=$(id); if(!e||e.textContent===s) return; e.textContent=s; e.style.fontSize=s.length>10?'14px':(s.length>7?'16px':''); }
  function rrect(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
  function txt(t,x,y,size,col,weight,align,maxW,halo){ ctx.textAlign=align||'left'; let s=size; ctx.font=(weight||'')+' '+s+'px sans-serif';
    if(maxW){ while(ctx.measureText(t).width>maxW&&s>8){ s-=0.5; ctx.font=(weight||'')+' '+s+'px sans-serif'; } }
    if(halo){ ctx.lineWidth=3.5; ctx.strokeStyle='rgba(255,255,255,.92)'; ctx.lineJoin='round'; ctx.strokeText(t,x,y); }
    ctx.fillStyle=col||'#0f172a'; ctx.fillText(t,x,y); return ctx.measureText(t).width; }
  function wrap(t,x,y,maxW,lh,size,col,weight){ ctx.font=(weight||'')+' '+size+'px sans-serif'; ctx.textAlign='left'; ctx.fillStyle=col||'#0f172a'; let line='', yy=y;
    for(const ch of t){ if(ctx.measureText(line+ch).width>maxW&&line&&'、。）」→'.indexOf(ch)<0){ ctx.fillText(line,x,yy); line=ch; yy+=lh; } else line+=ch; } if(line) ctx.fillText(line,x,yy); return yy; }
  function dot(x,y,r,c){ ctx.fillStyle=c; ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.fill(); }
  function poly(pts,w,c,dash){ ctx.strokeStyle=c; ctx.lineWidth=w; ctx.lineJoin='round'; ctx.lineCap='round'; if(dash) ctx.setLineDash(dash); ctx.beginPath(); pts.forEach((p,i)=>{ if(i) ctx.lineTo(p[0],p[1]); else ctx.moveTo(p[0],p[1]); }); ctx.stroke(); if(dash) ctx.setLineDash([]); }
  function arrow(x1,y1,x2,y2,w,col,dash){ const dx=x2-x1, dy=y2-y1, L=Math.hypot(dx,dy)||1, ux=dx/L, uy=dy/L, hl=Math.max(11,w*1.4), hw=Math.max(7,w*1.05);
    ctx.strokeStyle=col; ctx.lineWidth=w; ctx.lineCap='butt'; if(dash) ctx.setLineDash(dash); ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2-ux*hl*0.85,y2-uy*hl*0.85); ctx.stroke(); ctx.setLineDash([]);
    ctx.fillStyle=col; ctx.beginPath(); ctx.moveTo(x2,y2); ctx.lineTo(x2-ux*hl-uy*hw,y2-uy*hl+ux*hw); ctx.lineTo(x2-ux*hl+uy*hw,y2-uy*hl-ux*hw); ctx.closePath(); ctx.fill(); }
  function hex(c){ return [parseInt(c.slice(1,3),16),parseInt(c.slice(3,5),16),parseInt(c.slice(5,7),16)]; }
  function mix(a,b,t){ const A=hex(a),B=hex(b); t=clamp(t,0,1); return 'rgb('+A.map((v,i)=>Math.round(v+(B[i]-v)*t)).join(',')+')'; }

  // ---- モデル（相対値）
  const PMAX=4, KL=40, R0=1, LC=-KL*Math.log(1-R0/PMAX), KB=0.25, TMAX=6;
  const Pf=(L)=>PMAX*(1-Math.exp(-L/KL));
  const sunL=(h)=>(h>6&&h<18)?100*Math.sin(Math.PI*(h-6)/12):0;
  let DAYP=0; for(let i=0;i<2400;i++){ DAYP+=Pf(sunL((i+0.5)*24/2400))*24/2400; }
  const TB=6+12/Math.PI*Math.asin(LC/100), TE=24-TB;
  const f1=(v)=>(Math.round(v*10)/10).toFixed(1);
  const sgn=(v)=>(v>0.05?'＋':(v<-0.05?'−':'±'))+f1(Math.abs(v));
  function hm(h){ const m=((Math.round(h*60))%1440+1440)%1440; return Math.floor(m/60)+'時'+String(m%60).padStart(2,'0')+'分'; }
  function lword(L){ return L<0.5?'まっ暗':(L<LC-1.5?'暗い':(L<25?'弱い':(L<55?'ふつう':(L<85?'やや強い':'強い')))); }
  function netWord(n){ return n>0.05?'酸素を出す':(n<-0.05?'二酸化炭素を出す':'出入りがつり合う'); }
  const CG='#16a34a', CR='#ea580c', CO2C='#475569', O2C='#0284c7', CN='#1d4ed8';
  let mode='G', run=false, st=0, hrv=+$('hr').value, tmv=+$('tm').value, tnow=0, grab=false;
  const isSun=()=>mode==='G'&&$('src').value==='sun';
  function curL(){ return isSun()?sunL(hrv):+$('L').value; }

  // ================= ① 気体の出入り
  const GX0=364, GX1=620, GY0=44, GY1=286, YMIN=-1.5, YMAX=4.5;
  const gy=(v)=>GY1-(v-YMIN)/(YMAX-YMIN)*(GY1-GY0);
  function gxv(v){ return GX0+v/(isSun()?24:100)*(GX1-GX0); }
  function sunIcon(x,y,r){ ctx.strokeStyle='#f59e0b'; ctx.lineWidth=2; for(let k=0;k<8;k++){ const q=k*Math.PI/4; ctx.beginPath(); ctx.moveTo(x+Math.cos(q)*(r+3),y+Math.sin(q)*(r+3)); ctx.lineTo(x+Math.cos(q)*(r+8),y+Math.sin(q)*(r+8)); ctx.stroke(); } dot(x,y,r,'#fbbf24'); }
  function lampIcon(x,y,L,len){ const n=Math.round(L/9); ctx.strokeStyle='rgba(245,158,11,'+(0.3+0.6*L/100)+')'; ctx.lineWidth=2;
    for(let k=0;k<n;k++){ const q=Math.PI*(0.12+0.76*k/Math.max(1,n-1)); ctx.beginPath(); ctx.moveTo(x+Math.cos(q)*13,y+Math.sin(q)*13); ctx.lineTo(x+Math.cos(q)*(16+len*(0.35+0.65*L/100)),y+Math.sin(q)*(16+len*(0.35+0.65*L/100))); ctx.stroke(); }
    ctx.fillStyle='#64748b'; ctx.fillRect(x-6,y-17,12,8); dot(x,y,10,L>0?mix('#e5e7eb','#fde047',0.3+0.7*L/100):'#e5e7eb'); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1; ctx.beginPath(); ctx.arc(x,y,10,0,Math.PI*2); ctx.stroke(); }
  function leaf(cx,cy,w,h,a,fill,edge){ ctx.save(); ctx.translate(cx,cy); ctx.rotate(a); ctx.beginPath(); ctx.moveTo(-w/2,0); ctx.bezierCurveTo(-w/4,-h/1.05,w/4,-h/1.5,w/2,0); ctx.bezierCurveTo(w/4,h/1.5,-w/4,h/1.05,-w/2,0); ctx.closePath();
    ctx.fillStyle=fill; ctx.fill(); ctx.strokeStyle=edge; ctx.lineWidth=2; ctx.stroke(); ctx.lineWidth=1.3; ctx.beginPath(); ctx.moveTo(-w/2-10,0); ctx.lineTo(w/2-4,0); ctx.stroke();
    for(let k=1;k<5;k++){ const x=-w/2+k*w/5; ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x+w/9,-h*0.32); ctx.moveTo(x,0); ctx.lineTo(x+w/9,h*0.3); ctx.stroke(); } ctx.restore(); }
  function flow(x1,y1,x2,y2,rate,col){ const n=Math.round(rate*3); for(let i=0;i<n;i++){ const s=(tnow*0.45+i/n)%1, x=x1+(x2-x1)*s, y=y1+(y2-y1)*s; dot(x,y,4.6,'#fff'); dot(x,y,3.6,col); } }
  function drawG(){ const L=curL(), Pp=Pf(L), R=R0, Nn=Pp-R, sun=isSun(), night=sun&&L<=0;
    // 空・光源
    ctx.fillStyle=sun?(night?'#1e293b':(L<LC?'#fde68a':'#dbeafe')):'#f1f5f9'; rrect(8,8,308,54,10); ctx.fill();
    if(sun){ const q=clamp((hrv-6)/12,0,1), sx=26+q*272, sy=54-Math.max(0,Math.sin(Math.PI*q))*34;
      if(!night) sunIcon(sx,sy,9); else { dot(290,26,9,'#fef3c7'); dot(294,22,8,'#1e293b'); [[40,20],[90,34],[150,18],[210,30],[250,44]].forEach((p)=>dot(p[0],p[1],1.4,'#e2e8f0')); }
      txt(hm(hrv)+'　光の強さ '+Math.round(L)+'（'+lword(L)+'）',16,night?50:24,13.5,night?'#f8fafc':'#0f172a','bold','left',night?250:200); }
    else { lampIcon(34,28,L,20); txt('電灯の光の強さ '+L,62,30,14,'#0f172a','bold','left',240); txt('（'+lword(L)+'・相対値）',62,48,12,'#475569','','left',240); }
    // 葉と矢印
    txt('光合成',58,84,14.5,CG,'bold','center'); txt('呼吸',262,84,14.5,CR,'bold','center');
    leaf(161,170,124,66,-0.1,L>0?'#22c55e':'#15803d','#14532d');
    if(Pp>0.02){ arrow(14,112,102,151,2+Pp*4,CG); arrow(102,190,14,229,2+Pp*4,CG); flow(14,112,102,151,Pp,CO2C); flow(102,190,14,229,Pp,O2C); }
    else { arrow(14,112,102,151,2,'#cbd5e1',[5,4]); arrow(102,190,14,229,2,'#cbd5e1',[5,4]); txt('光が当たらない',58,175,11.5,'#64748b','bold','center'); txt('→ 光合成なし',58,191,11.5,'#64748b','bold','center'); }
    arrow(308,112,220,151,2+R*4,CR); arrow(220,190,308,229,2+R*4,CR); flow(308,112,220,151,R,O2C); flow(220,190,308,229,R,CO2C);
    txt('二酸化炭素 '+f1(Pp)+' を取り入れる',12,104,12,CO2C,'bold','left',145); txt('酸素 '+f1(Pp)+' を出す',12,250,12,O2C,'bold','left',145);
    txt('酸素 '+f1(R)+' を取り入れる',310,104,12,O2C,'bold','right',145); txt('二酸化炭素 '+f1(R)+' を出す',310,250,12,CO2C,'bold','right',145);
    txt('葉',161,174,13,'#f0fdf4','bold','center');
    // 差し引き
    const nc=Nn>0.05?CN:(Nn<-0.05?CR:'#0f766e');
    ctx.fillStyle='#f8fafc'; rrect(8,262,308,80,10); ctx.fill(); ctx.strokeStyle=nc; ctx.lineWidth=2; rrect(8,262,308,80,10); ctx.stroke();
    txt('差し引き（葉全体で見た気体の出入り）',18,281,12.5,'#334155','bold','left',290);
    txt(Nn>0.05?'酸素を出し、二酸化炭素を取り入れる':(Nn<-0.05?(L<=0?'呼吸だけ：酸素を取り入れ、二酸化炭素を出す':'酸素を取り入れ、二酸化炭素を出す'):'出入りがつり合う（見かけの出入りなし）'),18,306,14.5,nc,'bold','left',290);
    txt('光合成 '+f1(Pp)+' − 呼吸 '+f1(R)+' ＝ '+sgn(Nn)+'（相対値）',18,330,13,'#0f172a','','left',290);
    // グラフ
    ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; rrect(326,8,306,334,10); ctx.stroke();
    txt('光合成量・呼吸量と差し引き（相対値）',334,27,13,'#0f172a','bold','left',292);
    if(sun){ ctx.fillStyle='rgba(30,41,59,.08)'; ctx.fillRect(gxv(0),GY0,gxv(6)-gxv(0),GY1-GY0); ctx.fillRect(gxv(18),GY0,gxv(24)-gxv(18),GY1-GY0); txt('夜',gxv(3),GY0+14,11,'#475569','bold','center'); txt('夜',gxv(21),GY0+14,11,'#475569','bold','center'); }
    for(let v=-1;v<=4;v++){ poly([[GX0,gy(v)],[GX1,gy(v)]],v===0?1.6:1,v===0?'#64748b':'#eef2f7'); txt(String(v),GX0-6,gy(v)+4,10.5,'#64748b','','right'); }
    const xt=sun?[0,6,12,18,24]:[0,25,50,75,100]; xt.forEach((v)=>txt(sun?v+'時':String(v),gxv(v),GY1+15,10.5,'#64748b','','center'));
    txt(sun?'時刻（晴れた日）':'光の強さ（相対値）→',(GX0+GX1)/2,GY1+31,11.5,'#475569','bold','center');
    if(!sun){ txt('暗い',GX0,GY1+46,10,'#94a3b8','','left'); txt('強い',GX1,GY1+46,10,'#94a3b8','','right'); }
    const xs=[], n=sun?240:200; for(let i=0;i<=n;i++){ const v=(sun?24:100)*i/n; xs.push([gxv(v),sun?sunL(v):v]); }
    poly(xs.map((p)=>[p[0],gy(R0)]),2,CR,[6,4]); poly(xs.map((p)=>[p[0],gy(Pf(p[1]))]),2.5,CG); poly(xs.map((p)=>[p[0],gy(Pf(p[1])-R0)]),3,CN);
    const lb=(sun?[TB,TE]:[LC]); lb.forEach((v)=>{ poly([[gxv(v),GY0+20],[gxv(v),GY1]],1.2,'#0f766e',[3,3]); });
    if(sun){ txt('つり合う',gxv(TB)+3,gy(-1.25),10,'#0f766e','bold','left'); txt('つり合う',gxv(TE)-3,gy(-1.25),10,'#0f766e','bold','right'); }
    else txt('← 約'+Math.round(LC)+'でつり合う',gxv(LC)+4,gy(-1.25),10.5,'#0f766e','bold','left');
    const cx=gxv(sun?hrv:L); poly([[cx,GY0],[cx,GY1]],1.5,'#0e7490'); dot(cx,gy(Pp),5,CG); dot(cx,gy(R0),4.5,CR); dot(cx,gy(Nn),5.5,CN);
    txt('― 光合成量',GX0+8,GY0+16+(sun?12:0),11.5,CG,'bold','left'); txt('- - 呼吸量',GX0+8,GY0+31+(sun?12:0),11.5,CR,'bold','left'); txt('― 差し引き',GX0+8,GY0+46+(sun?12:0),11.5,CN,'bold','left');
    // 式
    ctx.fillStyle='#f0fdf4'; rrect(8,352,624,100,10); ctx.fill();
    let w=txt('光合成',18,374,13.5,CG,'bold','left'); txt('（葉緑体で・光が当たっているとき）：二酸化炭素 ＋ 水 → デンプンなど ＋ 酸素',18+w,374,13,'#0f172a','','left',600-w);
    w=txt('呼吸',18,398,13.5,CR,'bold','left'); txt('（昼も夜もいつも）：デンプンなど ＋ 酸素 → 二酸化炭素 ＋ 水（エネルギーをとり出す）',18+w,398,13,'#0f172a','','left',600-w);
    if(sun) txt('晴れた日の1日の合計：光合成 '+f1(DAYP)+' − 呼吸 24.0 ＝ '+sgn(DAYP-24)+' → 1日全体では酸素を出している',18,424,12.5,CN,'bold','left',604);
    else txt('暗いと呼吸だけ。光の強さ 約'+Math.round(LC)+' で光合成と呼吸がつり合い、それより明るいと酸素を出す',18,424,12.5,CN,'bold','left',604);
    txt(sun?'グラフを指でなぞると時刻を変えられます。▶ で1日を早送りできます':'グラフを指でなぞると、光の強さを変えられます',18,444,11,'#64748b','','left',604); }

  // ================= ② BTB溶液
  const TX=[92,242,392,542];
  function btbCol(ci){ return ci<0?mix('#22a447','#1d4ed8',-ci):mix('#22a447','#eab308',ci); }
  function btbWord(ci){ return ci<-0.6?'青色':(ci<-0.2?'青緑色':(ci<0.2?'緑色':(ci<0.6?'黄緑色':'黄色'))); }
  function btbState(){ const L=+$('L').value, NA=Pf(L)-R0; const cA=clamp(-KB*NA*tmv/0.75,-1,1), cB=clamp(KB*R0*tmv/0.75,-1,1); return {L:L,NA:NA,c:[cA,cB,0,0]}; }
  function tubePath(x,top,bot,w){ const r=w/2; ctx.beginPath(); ctx.moveTo(x-r,top); ctx.lineTo(x-r,bot-r); ctx.arc(x,bot-r,r,Math.PI,0,true); ctx.lineTo(x+r,top); }
  function elodea(x,y0,y1){ poly([[x,y0],[x+3,(y0+y1)/2],[x,y1]],2.2,'#166534'); for(let y=y1+6;y<y0-4;y+=11){ ctx.fillStyle='#15803d'; for(const s of [-1,1]){ ctx.save(); ctx.translate(x+s*1.5,y); ctx.rotate(s*(0.9+0.2*Math.sin(y))); ctx.beginPath(); ctx.ellipse(s*7,0,8,2.6,0,0,Math.PI*2); ctx.fill(); ctx.restore(); } } }
  function drawB(){ const S=btbState(), L=S.L;
    txt('BTB溶液に息をふきこんで緑色にし、4本の試験管に分けて光を当てる',12,22,13,'#0f172a','bold','left',470);
    txt('経過 '+f1(tmv)+'時間',628,22,14,'#0e7490','bold','right');
    const desc=[['A','オオカナダモ','光あり'],['B','オオカナダモ','光なし（アルミはく）'],['C','水草なし','光あり'],['D','水草なし','光なし（アルミはく）']];
    TX.forEach((x,i)=>{ const lit=(i===0||i===2), top=96, bot=292, w=50, ci=S.c[i];
      if(lit) lampIcon(x,46,L,14); else { txt('光が当たらない',x,50,11,'#64748b','bold','center'); }
      txt(desc[i][0],x-38,82,18,'#0f172a','bold','center');
      ctx.save(); tubePath(x,top,bot,w); ctx.closePath(); ctx.clip(); ctx.fillStyle=btbCol(ci); ctx.globalAlpha=0.88; ctx.fillRect(x-w/2,top+16,w,bot-top); ctx.globalAlpha=1;
      if(i<2){ elodea(x,bot-8,top+34); }
      if(i===0&&S.NA>0.05){ const nb=Math.round(S.NA*2.2); for(let k=0;k<nb;k++){ const yy=bot-20-((tnow*38+k*53)%(bot-top-50)); ctx.strokeStyle='rgba(255,255,255,.95)'; ctx.lineWidth=1.3; ctx.beginPath(); ctx.arc(x+6+Math.sin(tnow*3+k)*4,yy,2.6,0,Math.PI*2); ctx.stroke(); } }
      ctx.restore();
      tubePath(x,top,bot,w); ctx.strokeStyle='#64748b'; ctx.lineWidth=2; ctx.stroke();
      ctx.fillStyle='#475569'; rrect(x-w/2-3,top-12,w+6,16,4); ctx.fill();
      if(!lit){ ctx.save(); tubePath(x-0,top-14,bot+4,w+12); ctx.closePath(); ctx.fillStyle='rgba(203,213,225,.42)'; ctx.fill(); ctx.strokeStyle='rgba(100,116,139,.55)'; ctx.lineWidth=1; for(let y=top;y<bot;y+=17){ ctx.beginPath(); ctx.moveTo(x-w/2-6,y); ctx.lineTo(x-4,y+6); ctx.lineTo(x+w/2+6,y-3); ctx.stroke(); } ctx.restore(); txt('アルミはく',x,top+30,10.5,'#334155','bold','center',0,true); }
      txt(desc[i][1],x,312,12.5,'#334155','bold','center',140); txt(desc[i][2],x,328,12,'#475569','','center',146);
      txt(btbWord(ci),x,350,15,ci<-0.2?'#1d4ed8':(ci>0.2?'#a16207':'#15803d'),'bold','center'); });
    // 色の目盛り
    const bx=150, bw=340, by=362; for(let k=0;k<bw;k++){ ctx.fillStyle=btbCol(1-2*k/bw); ctx.fillRect(bx+k,by,1.2,9); }
    txt('黄色（酸性）',bx-6,by+9,11,'#a16207','bold','right'); txt('青色（アルカリ性）',bx+bw+6,by+9,11,'#1d4ed8','bold','left'); txt('緑色（中性）',bx+bw/2,by+22,10.5,'#15803d','bold','center');
    txt('← 二酸化炭素が多い',bx,by+22,10,'#64748b','','left'); txt('二酸化炭素が少ない →',bx+bw,by+22,10,'#64748b','','right');
    let l2;
    if(tmv<0.05) l2='A と B：ちがうのは光の有無だけ。▶ で時間を進めて、色の変化を予想しよう';
    else l2='A と B：ちがうのは光の有無だけ → A は'+(S.NA>0.05?'光合成で二酸化炭素が減って':(S.NA<-0.05?'光が弱く、呼吸が多くて二酸化炭素がふえて':'光合成と呼吸がつり合って'))+btbWord(S.c[0])+'、B は呼吸で二酸化炭素がふえて'+btbWord(S.c[1]);
    txt('A と C：ちがうのはオオカナダモの有無だけ → 色の変化はオオカナダモのはたらき（C・D は対照実験）',12,412,12.5,'#0f172a','','left',616);
    txt(l2,12,434,12.5,'#0f172a','bold','left',616);
    txt('光の強さ '+L+'（相対値）を弱くすると、A の色の変わり方はどうなるかな',12,454,11,'#64748b','','left',616); }

  // ================= ③ ヨウ素液
  function heartPath(cx,cy,k,sc){ ctx.beginPath(); for(let i=0;i<=120;i++){ const t=i/120*2*Math.PI, x=16*Math.pow(Math.sin(t),3), y=-(13*Math.cos(t)-5*Math.cos(2*t)-2*Math.cos(3*t)-Math.cos(4*t)); const X=cx+x*k*sc, Y=cy+2.5*k+(y-2.5)*k*sc; if(i) ctx.lineTo(X,Y); else ctx.moveTo(X,Y); } ctx.closePath(); }
  const IOD='#d9b97c', PUR='#3b0764';
  function starch(){ return clamp(Math.max(0,Pf(+$('L').value)-R0)*tmv/4,0,1); }
  function foil(x,y,w,h){ const g=ctx.createLinearGradient(x,y,x+w,y+h); g.addColorStop(0,'#e2e8f0'); g.addColorStop(0.5,'#f8fafc'); g.addColorStop(1,'#94a3b8'); ctx.fillStyle=g; rrect(x,y,w,h,6); ctx.fill(); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1; rrect(x,y,w,h,6); ctx.stroke();
    ctx.strokeStyle='rgba(100,116,139,.45)'; for(let k=0;k<5;k++){ ctx.beginPath(); ctx.moveTo(x+6,y+12+k*h/5); ctx.lineTo(x+w*0.5,y+18+k*h/5); ctx.lineTo(x+w-6,y+8+k*h/5); ctx.stroke(); } }
  const STEPS={fu:['前の日から植物を暗い所に置き、葉のデンプンをなくしておく。ふ入りの葉の一部をアルミはくでおおう',
                   '光を当てる',
                   '葉をとってアルミはくを外し、熱湯につけたあと、あたためたエタノールにつけて緑色をぬく（脱色）',
                   '水で洗ってヨウ素液につける → デンプンがある所は青紫色になる'],
              abc:['前の日の午後、3枚の葉 ア・イ・ウ にアルミはくをかぶせる（夜のあいだに、葉のでんぷんがなくなる）',
                   '次の日の朝、アはアルミはくを外してすぐ調べる。イはアルミはくを外して日光に当てる。ウはかぶせたまま',
                   'イとウをとって、湯でにてから、あたためたエタノールで緑色をぬく（ろ紙にはさんでたたく「たたき染め」でもよい）',
                   'ヨウ素液をつける → でんぷんがある葉は青むらさき色になる']};
  function drawSteps(lf){ for(let k=0;k<4;k++){ const x=24+k*27; dot(x,22,11,k===st?'#0e7490':(k<st?'#99f6e4':'#e2e8f0')); txt('①②③④'[k],x,27,13,k===st?'#fff':'#0f172a','bold','center'); }
    let s=STEPS[lf][st]; if(st===1) s+=(lf==='fu'?'（':'（')+f1(tmv)+'時間・光の強さ '+$('L').value+'）';
    wrap(s,128,20,500,18,13,'#0f172a','bold'); }
  function drawY(){ const lf=$('lf').value, Sa=starch(); drawSteps(lf);
    if(lf==='fu'){ const cx=168, cy=226, k=8.2, FX=cx+3.2*k;
      if(st===0){ ctx.fillStyle='rgba(30,41,59,.10)'; rrect(8,68,316,384,10); ctx.fill(); txt('暗い所に一晩',20,90,12,'#334155','bold','left'); }
      if(st===1) lampIcon(40,92,+$('L').value,30);
      poly([[cx,cy-5*k],[cx-4,cy-5*k-30],[cx-14,82]],3,'#4d7c0f');
      let cF, cG; if(st<=1){ cF='#f3f6e8'; cG='#22a447'; } else if(st===2){ cF='#fffdf5'; cG='#fbf1cf'; } else { cF=IOD; cG=IOD; }
      heartPath(cx,cy,k,1); ctx.fillStyle=cF; ctx.fill(); heartPath(cx,cy,k,0.7); ctx.fillStyle=cG; ctx.fill();
      if(st===3&&Sa>0){ ctx.save(); ctx.beginPath(); ctx.rect(0,0,FX,H); ctx.clip(); heartPath(cx,cy,k,0.7); ctx.fillStyle=mix(IOD,PUR,0.2+0.65*Sa); ctx.fill(); ctx.restore(); }
      heartPath(cx,cy,k,1); ctx.strokeStyle='#3f6212'; ctx.lineWidth=2; ctx.stroke();
      ctx.strokeStyle='rgba(63,98,18,.35)'; ctx.lineWidth=1.2; poly([[cx,cy-5*k],[cx,cy+15*k]],1.2,'rgba(63,98,18,.35)');
      if(st<=1){ foil(FX,cy-13*k,cx+16*k+10-FX,30*k); txt('アルミはく',FX+(cx+16*k+10-FX)/2,cy+8*k,12,'#334155','bold','center',0,true); }
      else { ctx.strokeStyle='#94a3b8'; ctx.setLineDash([4,4]); ctx.lineWidth=1.2; ctx.beginPath(); ctx.moveTo(FX,cy-12*k); ctx.lineTo(FX,cy+15*k); ctx.stroke(); ctx.setLineDash([]); txt('点線から右をアルミはくでおおっていた',cx,cy+17*k+18,11.5,'#64748b','','center',300); }
      const lab=[['a',cx-6.5*k,cy+1.6*k],['b',cx-13.8*k,cy-4*k],['c',cx+8.4*k,cy+1.6*k],['d',cx+13.8*k,cy-4*k]];
      lab.forEach((p)=>{ dot(p[1],p[2],11,'#fff'); ctx.strokeStyle='#0f172a'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.arc(p[1],p[2],11,0,Math.PI*2); ctx.stroke(); txt(p[0],p[1],p[2]+5,14,'#0f172a','bold','center'); });
      // 表
      const X=[344,384,470,546], Y0=96; txt('部分',X[0],Y0,12,'#475569','bold'); txt('緑色の部分',X[1],Y0,12,'#475569','bold'); txt('光',X[2],Y0,12,'#475569','bold'); txt('ヨウ素液',X[3],Y0,12,'#475569','bold');
      const rows=[['a','○ ある','○ 当たる'],['b','×（ふ）','○ 当たる'],['c','○ ある','×（はく）'],['d','×（ふ）','×（はく）']];
      rows.forEach((r,i)=>{ const y=Y0+28+i*28; poly([[340,y-19],[630,y-19]],1,'#e2e8f0'); txt(r[0],X[0]+8,y,14,'#0f172a','bold','center'); txt(r[1],X[1],y,12.5,r[1][0]==='○'?'#15803d':'#b91c1c','','left',80); txt(r[2],X[2],y,12.5,r[2][0]==='○'?'#15803d':'#b91c1c','','left',72);
        const res=st<3?'？':((i===0&&Sa>0.15)?'青紫色':'変化なし'); txt(res,X[3],y,13,res==='青紫色'?'#6b21a8':'#334155','bold','left',84); });
      let concl;
      if(st<3) concl='手順④でヨウ素液につけると結果が分かります。a〜d のどこが青紫色になるか予想しよう。';
      else if(Sa>0.15) concl='a だけが青紫色になった。a と c をくらべる → デンプンをつくるには光が必要。a と b をくらべる → デンプンは葉の緑色の部分（葉緑体）でつくられる。';
      else concl='a も青紫色にならない。光が弱すぎる・光を当てた時間が短いと、デンプンがほとんどたまらない。光の強さや時間を変えてみよう。';
      ctx.fillStyle='#f8fafc'; rrect(340,222,292,128,10); ctx.fill(); wrap(concl,350,244,272,20,13,st===3?'#0f172a':'#475569',st===3?'bold':'');
      txt('デンプン（相対値）：a '+(st===3?Math.round(Sa*100):'？'),350,376,12,'#6b21a8','bold','left',272);
      txt('エタノールは火を使わず、湯であたためる',350,398,11,'#b91c1c','','left',272); }
    else { const P3=[[110,'ア'],[320,'イ'],[530,'ウ']], cy=205, k=4.6, Si=starch();
      P3.forEach((p,i)=>{ const x=p[0]; txt(p[1],x,128,20,'#0f172a','bold','center');
        let cov=(st===0)||(i===2&&st===1), col;
        if(i===0){ col=st===0?'#22a447':IOD; } else if(st<=1){ col='#22a447'; } else if(st===2){ col='#fbf1cf'; } else col=(i===1)?mix(IOD,PUR,Si>0?0.2+0.65*Si:0):IOD;
        if(i===1&&st===1){ ctx.strokeStyle='rgba(245,158,11,'+(0.3+0.6*(+$('L').value)/100)+')'; ctx.lineWidth=2; for(let r=0;r<6;r++){ ctx.beginPath(); ctx.moveTo(x-60+r*24,138); ctx.lineTo(x-70+r*24,154); ctx.stroke(); } }
        poly([[x,cy-5*k],[x,cy-5*k-22]],3,'#4d7c0f');
        heartPath(x,cy,k,1); ctx.fillStyle=col; ctx.fill(); ctx.strokeStyle='#3f6212'; ctx.lineWidth=2; ctx.stroke();
        if(cov){ foil(x-16*k-8,cy-13*k,32*k+16,30*k+6); txt('アルミはく',x,cy+20,12,'#334155','bold','center',0,true); }
        const s1=i===0?(st===0?'おおっている':'朝すぐ調べる'):(i===1?(st===0?'おおっている':'日光に当てる'):'おおったまま');
        txt(s1,x,306,13,'#334155','bold','center',190);
        let s2='';
        if(i===0&&st>=1) s2='→ 変化なし'; else if(st===3) s2=(i===1&&Si>0.15)?'→ 青むらさき色':'→ 変化なし';
        if(s2) txt(s2,x,328,14,s2.indexOf('青')>=0?'#6b21a8':'#334155','bold','center',190); });
      let concl;
      if(st<3) concl='ア・イ・ウのどれが青むらさき色になるか予想しよう。ちがう条件は「日光に当てたかどうか」だけにしてある。';
      else if(Si>0.15) concl='イだけが青むらさき色になった。イとウをくらべると、ちがうのは日光に当てたかどうかだけ → 葉に日光が当たると、でんぷんができる。アから、朝の葉にはでんぷんがなかったことも分かる。';
      else concl='イも色が変わらない。光が弱い・時間が短いと、でんぷんがほとんどできない。光の強さや時間を変えてみよう。';
      ctx.fillStyle='#f8fafc'; rrect(8,346,624,104,10); ctx.fill(); wrap(concl,20,370,600,21,13.5,st===3?'#0f172a':'#475569',st===3?'bold':''); } }

  // ================= ④ 蒸散
  function jousan(){ const L=+$('L').value, lf=0.2+0.8*L/100; const fr=Math.round(0.2*lf*tmv*10), bk=Math.round(0.6*lf*tmv*10), sm=Math.round(0.4/6*tmv*10);
    return {fr:fr/10,bk:bk/10,sm:sm/10,A:(fr+bk+sm)/10,B:(bk+sm)/10,C:(fr+sm)/10,D:sm/10}; }
  function drawJ(){ const J=jousan(), L=+$('L').value, vals=[J.A,J.B,J.C,J.D];
    txt('葉の数と大きさをそろえた枝を水にさし、水面に油をたらして、水の減り方をくらべる',12,22,13,'#0f172a','bold','left',480);
    txt('経過 '+f1(tmv)+'時間',628,22,14,'#0e7490','bold','right');
    const desc=[['A','何もぬらない'],['B','葉の表にワセリン'],['C','葉の裏にワセリン'],['D','葉をとり、切り口にワセリン']];
    const lfac=0.2+0.8*L/100;
    TX.forEach((x,i)=>{ const top=150, bot=318, lv0=172, lv=lv0+vals[i]*24;
      ctx.fillStyle='rgba(224,242,254,.5)'; ctx.fillRect(x-20,top,40,bot-top);
      ctx.fillStyle='rgba(56,189,248,.55)'; ctx.fillRect(x-20,lv,40,bot-lv); ctx.fillStyle='#facc15'; ctx.fillRect(x-20,lv-5,40,5);
      ctx.strokeStyle='#64748b'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(x-20,top-4); ctx.lineTo(x-20,bot); ctx.lineTo(x+20,bot); ctx.lineTo(x+20,top-4); ctx.stroke(); ctx.fillStyle='#94a3b8'; ctx.fillRect(x-30,bot,60,6);
      for(let m=0;m<=6;m++){ const y=lv0+m*24; poly([[x+12,y],[x+20,y]],1.2,'#64748b'); }
      if(vals[i]>0) poly([[x-28,lv0],[x-20,lv0]],1.5,'#0284c7'); txt('はじめ',x-30,lv0+4,9.5,'#0284c7','','right');
      poly([[x,bot-12],[x,62]],4,'#65a30d');
      if(i<3){ const LV=[[x-30,78,-0.25],[x+30,78,0.25],[x-30,116,-0.2],[x+30,116,0.2]];
        LV.forEach((q)=>{ ctx.save(); ctx.translate(q[0],q[1]); ctx.rotate(q[2]); ctx.beginPath(); ctx.ellipse(0,0,27,9,0,0,Math.PI*2); ctx.fillStyle='#22c55e'; ctx.fill(); ctx.strokeStyle='#15803d'; ctx.lineWidth=1.5; ctx.stroke();
          if(i===1||i===2){ ctx.beginPath(); ctx.ellipse(0,0,27,9,0,i===1?Math.PI:0,i===1?2*Math.PI:Math.PI); ctx.strokeStyle='#fde68a'; ctx.lineWidth=5; ctx.stroke(); ctx.strokeStyle='#ca8a04'; ctx.lineWidth=1; ctx.stroke(); }
          ctx.restore();
          const parts=[]; if(i!==1) parts.push([-13,0.2]); if(i!==2) parts.push([13,0.6]);
          parts.forEach((pp)=>{ const nn=Math.round(pp[1]*lfac*5); for(let k=0;k<nn;k++){ const s=(tnow*0.6+k/nn+q[0]*0.01)%1; const yy=q[1]+pp[0]*(1-s)-s*30; ctx.globalAlpha=1-s; dot(q[0]+Math.sin(k*2+q[1])*14,yy,2.4,'#7dd3fc'); ctx.globalAlpha=1; } }); }); }
      else { [[x-6,78],[x+6,78],[x-6,116],[x+6,116]].forEach((q)=>{ dot(q[0],q[1],4,'#fde68a'); }); const s=(tnow*0.5)%1; ctx.globalAlpha=1-s; dot(x+3,100-s*30,2.2,'#7dd3fc'); ctx.globalAlpha=1; }
      txt(desc[i][0],x-50,64,18,'#0f172a','bold','center');
      txt(desc[i][1],x,338,12,'#334155','bold','center',146);
      txt('減った水',x,357,11,'#64748b','','center'); txt(f1(vals[i])+'mL',x,377,16,'#0369a1','bold','center'); });
    ctx.fillStyle='#f0f9ff'; rrect(8,386,624,68,10); ctx.fill();
    txt('葉の表から ＝ C − D ＝ '+f1(J.C)+' − '+f1(J.D)+' ＝ '+f1(J.fr)+'mL　　葉の裏から ＝ B − D ＝ '+f1(J.B)+' − '+f1(J.D)+' ＝ '+f1(J.bk)+'mL',18,405,12.5,'#0f172a','','left',604);
    txt('茎から ＝ D ＝ '+f1(J.sm)+'mL　　A ＝ 表 ＋ 裏 ＋ 茎 ＝ '+f1(J.fr)+' ＋ '+f1(J.bk)+' ＋ '+f1(J.sm)+' ＝ '+f1(J.A)+'mL',18,425,12.5,'#0f172a','','left',604);
    txt(tmv<0.05?'▶ で時間を進めて、どの試験管の水がいちばん減るか予想しよう':'→ 葉の裏からの蒸散がいちばん多い（気孔は葉の裏側に多い）。光が弱いと気孔が閉じて減り方が小さくなる',18,446,12,'#0369a1','bold','left',604); }

  // ================= 数値・切りかえ
  const LW=['A','B','C','D'];
  function update(){ const L=curL();
    if(mode==='G'){ const Pp=Pf(L), Nn=Pp-R0; ['光合成量（相対値）','呼吸量（相対値）','差し引き（見かけの光合成）','葉全体として'].forEach((t,i)=>setK('s'+(i+1),t));
      setV('s1',f1(Pp)); setV('s2',f1(R0)); setV('s3',sgn(Nn)); setV('s4',netWord(Nn));
      setShare('【光合成と呼吸】'+(isSun()?hm(hrv)+'（晴れた日）':'光の強さ'+L)+'で光合成'+f1(Pp)+'・呼吸1.0（相対値）→差し引き'+sgn(Nn)+'。葉全体では'+netWord(Nn)+'。暗いと呼吸だけ、光の強さ約'+Math.round(LC)+'で出入りがつり合う｜シミュラボ'); }
    else if(mode==='B'){ const S=btbState(); ['A（オオカナダモ・光あり）','B（オオカナダモ・光なし）','C・D（水草なし）','経過時間'].forEach((t,i)=>setK('s'+(i+1),t));
      setV('s1',btbWord(S.c[0])); setV('s2',btbWord(S.c[1])); setV('s3','緑色のまま'); setV('s4',f1(tmv)+'時間');
      setShare('【BTB溶液とオオカナダモ】光の強さ'+S.L+'で'+f1(tmv)+'時間：光を当てたAは'+btbWord(S.c[0])+'、暗いBは'+btbWord(S.c[1])+'、水草なしのC・Dは緑色のまま（対照実験）｜シミュラボ'); }
    else if(mode==='Y'){ const lf=$('lf').value, Sa=starch(); ['光の強さ（相対値）','光に当てた時間','青紫色になった部分','手順'].forEach((t,i)=>setK('s'+(i+1),t));
      const res=st<3?'手順④で分かる':(Sa>0.15?(lf==='fu'?'a だけ':'イ だけ'):'なし');
      setV('s1',String($('L').value)); setV('s2',f1(tmv)+'時間'); setV('s3',res); setV('s4',(st+1)+' / 4');
      setShare(lf==='fu'?'【ヨウ素液とデンプン】ふ入りの葉に光の強さ'+$('L').value+'で'+f1(tmv)+'時間光を当てると、青紫色になるのは「緑色で光が当たった部分」だけ → 光合成には光と葉緑体が必要｜シミュラボ'
        :'【葉のでんぷん（小6）】日光に当てた葉イだけがヨウ素液で青むらさき色に → 葉に日光が当たるとでんぷんができる｜シミュラボ'); }
    else { const J=jousan(); ['A 何もぬらない','B 葉の表にワセリン','C 葉の裏にワセリン','D 葉をとる'].forEach((t,i)=>setK('s'+(i+1),t));
      setV('s1',f1(J.A)+'mL'); setV('s2',f1(J.B)+'mL'); setV('s3',f1(J.C)+'mL'); setV('s4',f1(J.D)+'mL');
      setShare('【蒸散の実験】'+f1(tmv)+'時間で水の減った量 A'+f1(J.A)+'mL・B'+f1(J.B)+'mL・C'+f1(J.C)+'mL・D'+f1(J.D)+'mL → 葉の裏から'+f1(J.bk)+'mL・表から'+f1(J.fr)+'mL。気孔は葉の裏に多い｜シミュラボ'); }
    $('hrL').textContent=hm(hrv); }
  const HASH={G:'',B:'btb',Y:'youso',J:'jousan'};
  function setPlay(){ $('play').textContent=run?'⏸ 止める':(isSun()?'▶ 1日を早送り':'▶ 時間を進める'); }
  function setMode(m){ mode=m; grab=false;
    [['tG','G'],['tB','B'],['tY','Y'],['tJ','J']].forEach((a)=>{ const b=$(a[0]); b.className='btn '+(a[1]===m?'btn-primary':'btn-ghost'); b.setAttribute('aria-pressed',a[1]===m?'true':'false'); });
    const sun=isSun();
    fld('src').style.display=m==='G'?'':'none'; fld('L').style.display=(m!=='G'||!sun)?'':'none'; fld('hr').style.display=(m==='G'&&sun)?'':'none';
    fld('tm').style.display=m!=='G'?'':'none'; fld('lf').style.display=m==='Y'?'':'none';
    $('play').style.display=(m!=='G'||sun)?'':'none'; $('rst').style.display=(m!=='G'||sun)?'':'none'; $('nx').style.display=m==='Y'?'':'none';
    $('nx').textContent=st===3?'⏮ 手順①にもどる':'🧪 次の手順へ'; setPlay();
    try{ history.replaceState(null,'',location.pathname+location.search+(HASH[m]?'#'+HASH[m]:'')); }catch(e){}
    update(); }
  [['tG','G'],['tB','B'],['tY','Y'],['tJ','J']].forEach((a)=>$(a[0]).addEventListener('click',()=>{ run=false; setMode(a[1]); }));
  $('src').addEventListener('change',()=>{ run=false; setMode('G'); });
  $('L').addEventListener('input',update);
  $('hr').addEventListener('input',()=>{ hrv=+$('hr').value; update(); });
  $('tm').addEventListener('input',()=>{ tmv=+$('tm').value; update(); });
  $('lf').addEventListener('change',()=>{ st=0; setMode('Y'); });
  $('nx').addEventListener('click',()=>{ st=(st+1)%4; run=false; setMode('Y'); });
  $('rst').addEventListener('click',()=>{ run=false; if(mode==='G'){ hrv=0; $('hr').value=0; } else { tmv=0; $('tm').value=0; $('tmL').textContent='0時間'; if(mode==='Y') st=0; } setMode(mode); });
  $('play').addEventListener('click',()=>{ if(!run&&mode!=='G'){ if(tmv>=TMAX-0.01) tmv=0; if(mode==='Y'&&st!==1) st=1; } run=!run; setMode(mode); });
  function setFromX(x){ const f=clamp((x-GX0)/(GX1-GX0),0,1); if(isSun()){ hrv=f*24; $('hr').value=hrv; } else { $('L').value=Math.round(f*100); $('L').dispatchEvent(new Event('input')); } update(); }
  cv.addEventListener('pointerdown',(e)=>{ if(mode!=='G') return; const p=cpos(cv,e), x=p[0]/dpr, y=p[1]/dpr;
    if(x>=GX0-14&&x<=GX1+14&&y>=GY0-10&&y<=GY1+40){ grab=true; run=false; setPlay(); e.preventDefault(); try{ cv.setPointerCapture(e.pointerId); }catch(er){} setFromX(x); } });
  cv.addEventListener('pointermove',(e)=>{ if(!grab) return; const p=cpos(cv,e); setFromX(p[0]/dpr); });
  const endG=()=>{ grab=false; }; cv.addEventListener('pointerup',endG); cv.addEventListener('pointercancel',endG);
  function draw(){ ctx.fillStyle='#ffffff'; ctx.fillRect(0,0,W,H); if(mode==='G') drawG(); else if(mode==='B') drawB(); else if(mode==='Y') drawY(); else drawJ(); }
  let last=performance.now(), acc=0;
  function loop(now){ const dt=Math.min(0.05,Math.max(0,(now-last)/1000)); last=now; tnow+=dt;
    if(run){ if(mode==='G'){ hrv=(hrv+dt*2)%24; $('hr').value=hrv; } else { tmv=Math.min(TMAX,tmv+dt*0.8); $('tm').value=tmv.toFixed(1); $('tmL').textContent=f1(tmv)+'時間'; if(tmv>=TMAX){ run=false; setPlay(); } } }
    acc+=dt; if(run||acc>0.25){ acc=0; update(); }
    draw(); requestAnimationFrame(loop); }
  const h0=(location.hash||'').replace('#',''); const m0=h0==='btb'?'B':(h0==='youso'?'Y':(h0==='jousan'?'J':'G'));
  setMode(m0); draw(); requestAnimationFrame(loop);
'''

sim(slug="kougousei", cat="rika", emoji="🍃", score=81,
    title="光合成と呼吸のシミュレーター（気体の出入り・BTB溶液・ヨウ素液・蒸散）",
    title_tag="光合成と呼吸のシミュレーション｜光の強さと気体の出入り・BTB溶液とオオカナダモ・ヨウ素液・蒸散の実験（中2・小6理科）",
    meta_desc="中2「植物の体のつくりと働き」・小6「植物の養分と水の通り道」のシミュレーション。光の強さや時刻を変えると、葉が出し入れする酸素・二酸化炭素の量と、光合成と呼吸の差し引きがグラフで分かります。BTB溶液の対照実験、ヨウ素液でデンプンを調べる実験、ワセリンを使った蒸散の実験つき。",
    og_title="光合成と呼吸のシミュレーター（気体の出入り・BTB溶液・ヨウ素液・蒸散）",
    og_desc="暗いと呼吸だけ、明るいと酸素を出す。光の強さで変わる光合成と呼吸の差し引きを、矢印とグラフで確かめる。BTB溶液・ヨウ素液・蒸散の実験つき。",
    card_desc="光の強さで変わる酸素・二酸化炭素の出入りを矢印とグラフで。BTB溶液・ヨウ素液・蒸散の実験も。",
    lead="光の強さ（または晴れた日の時刻）を変えると、葉が取り入れる・出す酸素と二酸化炭素の量が変わり、光合成と呼吸の差し引きがグラフで分かります。BTB溶液・ヨウ素液・蒸散の実験も切りかえて見られます。",
    model="中2 植物の体のつくりと働き／小6 植物の養分と水の通り道", level="小学6年、中学2年",
    unit="小学校 第6学年 B（2）植物の養分と水の通り道／中学校 第2分野（3）ア（ｲ）植物の体のつくりと働き",
    canvas=canvas(640, 460, light=True),
    controls=select("src", "光の当て方", [("lamp", "💡 電灯（光の強さを変える）"), ("sun", "🌞 晴れた日（時刻を変える）")])
             + slider("L", "光の強さ（相対値）", 0, 100, 60, 1) + slider("hr", "時刻", 0, 24, 9, 0.25)
             + slider("tm", "実験の時間", 0, 6, 3, 0.1, "{v}時間")
             + select("lf", "使う葉", [("fu", "ふ入りの葉（中2）"), ("abc", "3枚の葉 ア・イ・ウ（小6）")]),
    buttons=btn("tG", "🍃 ① 気体の出入り", True) + btn("tB", "🧪 ② BTB溶液") + btn("tY", "🟣 ③ ヨウ素液") + btn("tJ", "💧 ④ 蒸散")
            + btn("play", "▶ 時間を進める", True) + btn("rst", "⏮ はじめにもどす") + btn("nx", "🧪 次の手順へ"),
    stats=stats([("s1", "光合成量（相対値）", False), ("s2", "呼吸量（相対値）", False), ("s3", "差し引き（見かけの光合成）", True), ("s4", "葉全体として", False)]),
    legend="図は模式図で、数値はすべて相対値（くらべるための目安）です。①：緑の矢印＝光合成、オレンジの矢印＝呼吸（太いほど多い）。青い粒＝酸素、灰色の粒＝二酸化炭素。グラフを指でなぞると光の強さ（時刻）を変えられます。②：B・Dのアルミはくは色が見えるように透かして描いています。③④：「実験の時間」と光の強さで結果が変わります。",
    article=KOUGOU_ARTICLE, faqs=KOUGOU_FAQS,
    rel=[("hatsuga-jouken", "🫘", "種子の発芽と成長の条件シミュレーター"), ("hito-karada", "🫀", "人の体のつくりと働き（血液の循環・呼吸・消化）"),
         ("nenshou", "🕯️", "ものの燃え方と空気シミュレーター"), ("saibou-bunretsu", "🧫", "細胞分裂シミュレーター"), ("mendel-iden", "🌱", "遺伝の規則性シミュレーター")],
    js=KOUGOU_JS)


# ============================================================ 2 種子の発芽と成長の条件
def _gh(s, f, t):
    """発芽してからの日数 t → 土の上の高さ(cm)。JSと同じ式（目安）"""
    if t < 2.5: return 0.0
    hm_, tau = (28, 8) if (s and f) else ((16, 6) if s else (36, 7))
    return 2 + (hm_ - 2) * (1 - math.exp(-(t - 2.5) / tau))
GD = 3   # 水を与えてから根が出る（発芽する）まで：3日（目安）
H20 = {k: _gh(k[0], k[1], 20 - GD) for k in [(1, 1), (1, 0), (0, 1)]}

HATSUGA_ARTICLE = "<h2>このシミュレーションでわかること</h2>\n" + P(
    "種子が発芽するには、<b>水・空気・適当な温度</b>の3つが必要です。日光と肥料は、発芽には必要ありませんが、発芽したあとに<b>よく成長するためには日光と肥料が必要</b>です。"
    "インゲンマメは、種子の中の子葉にたくわえた<b>でんぷん</b>を使って発芽します。") + '''
<p>小学校5年の理科「<b>植物の発芽，成長，結実</b>」（学習指導要領 第5学年 B（1））で学ぶ内容です。学習指導要領の解説（理科編 pp.68〜69）は、発芽の条件と成長の条件は混同しやすいので、<b>変える条件と変えない条件を区別</b>して調べるように書いています。</p>
<p>インゲンマメの種子をまいたカップを2〜4こならべ、水・空気・温度・日光・肥料の条件を「○・×」で変えて、早送りで発芽と成長のようすを見られます。くらべる2つのカップを選ぶと、<b>ちがう条件の札が光って</b>、正しい比べ方（ちがう条件が1つだけ）になっているかが分かります。「子葉をヨウ素液で調べる」で、子葉のでんぷんが発芽のあとに減っていくことも確かめられます。</p>
<h2>授業での使い方</h2>
<ul>
<li><b>導入</b>：「種子が発芽するには何が必要か」を予想させます（水・土・日光・肥料・あたたかさ など）。予想した条件を1つずつ確かめるには、どんなカップを用意すればよいかを話し合います。</li>
<li><b>展開</b>：「実験」から①〜⑤を選び、ちがう条件が1つだけになっているかを確かめてから早送りします。④「まちがいやすい比べ方」では、冷蔵庫の中が暗いため、温度と日光の2つがちがってしまうことに気づかせます。実際の実験の結果と見くらべるのにも使えます。</li>
<li><b>まとめ</b>：結果を表に整理し、「発芽に必要な条件」と「成長に必要な条件」を分けて書きます。⑥⑦で日光・肥料のちがいによる成長のちがい（葉の色・数・大きさ、くきの太さ）を見て、発芽と成長の条件のちがいを確かめます。</li>
</ul>
<p>児童への問いの例：</p>
<ol>
<li>「発芽に水が必要か」を調べるとき、2つのカップでそろえる条件と、変える条件は何でしょう。</li>
<li>冷蔵庫に入れたカップとくらべるカップに、箱をかぶせるのはなぜでしょう。</li>
<li>発芽したあとの子葉にヨウ素液をつけると、発芽する前の種子とくらべて色はどうなるでしょう。それはなぜでしょう。</li>
</ol>
<h2>しくみ・解説</h2>
<h3>ことばの意味</h3>
<ul>
<li><b>発芽</b>とは、種子から根や芽が出ることです。</li>
<li><b>条件制御</b>（条件をそろえる）とは、調べたい条件だけを変えて、それ以外の条件をすべて同じにしてくらべることです。</li>
<li><b>子葉</b>とは、種子の中にある最初の葉で、インゲンマメでは発芽のための養分（でんぷん）をたくわえています。</li>
<li><b>ヨウ素液</b>は、でんぷんにつけると<b>青むらさき色</b>に変わる液です。でんぷんがあるかどうかを調べるのに使います。</li>
</ul>
<h3>発芽と成長に必要な条件（早見表）</h3>
''' + T([["水", "必要", "必要"], ["空気", "必要", "必要"], ["適当な温度", "必要", "関係する"],
          ["日光", "必要ない", "必要（ないと、ひょろ長く葉が黄色っぽくなる）"],
          ["肥料", "必要ない", "関係する（あるほうが、葉が多く大きく育つ）"]],
         ["条件", "発芽", "成長"]) + '''
<h3>条件のそろえ方（このシミュレーションの実験）</h3>
''' + T([["① 水は必要？", "水", "空気・温度・日光・肥料", "水なしは発芽しない → 水が必要"],
          ["② 空気は必要？", "空気（種子を水にしずめる）", "水・温度・日光・肥料", "水にしずめると発芽しない → 空気が必要"],
          ["③ 温度は関係する？", "温度（冷蔵庫／部屋）", "水・空気・日光（部屋のカップにも箱をかぶせて暗くする）・肥料", "冷蔵庫の中は発芽しない → 適当な温度が必要"],
          ["⑤ 日光は必要？", "日光（箱をかぶせる）", "水・空気・温度・肥料", "どちらも発芽する → 発芽に日光は必要ない"],
          ["⑥⑦ 成長と日光・肥料", "日光、または肥料", "そのほかの条件", "日光・肥料があるほうがよく育つ"]],
         ["調べること", "変える条件", "同じにする条件", "結果"]) + N(
    "<b>冷蔵庫を使うときの注意</b>：冷蔵庫の中は温度が低いだけでなく、<b>暗い</b>です。部屋の明るい所に置いたカップとくらべると、温度と日光の2つの条件がちがってしまい、発芽しなかった原因がどちらか分かりません。部屋に置くカップにも<b>箱をかぶせて暗くし</b>、ちがう条件を温度だけにします（このシミュレーションの③と④）。") + '''
<h3>インゲンマメの育ち方（目安）</h3>
''' + T([["0日目", "水をあたえる（種子をまく）"], ["1日目", "水を吸って、ふくらむ"], ["%d日目ごろ" % GD, "根が出る（発芽）"],
          ["5〜6日目ごろ", "くきがのびて、子葉が土の上に出る"], ["8〜10日目ごろ", "最初の本葉（2まい）が開く"],
          ["2〜3週間", "葉がふえて大きくなる。子葉はしぼんで落ちる"]],
         ["日数（あたたかい部屋）", "ようす"]) + '''
<p>日数は、20〜25℃くらいのあたたかい部屋で育てたときの目安です。温度が低いと発芽がおそくなり、冷蔵庫の中（約5℃）ではほとんど発芽しません。このシミュレーションの20日目の高さ（目安）は、日光と肥料あり 約%dcm、日光あり・肥料なし 約%dcm、日光なし 約%dcm（ひょろ長く、葉が黄色っぽい）です。</p>
''' % (round(H20[(1, 1)]), round(H20[(1, 0)]), round(H20[(0, 1)])) + '''
<h3>子葉のでんぷん（ヨウ素液）</h3>
<p>発芽する前のインゲンマメの種子を2つに切ってヨウ素液をつけると、子葉が<b>青むらさき色</b>になり、でんぷんがふくまれていることが分かります。発芽して育ったあとのしぼんだ子葉にヨウ素液をつけると、色はほとんど変わりません。子葉のでんぷんが、発芽や成長のための養分として使われたからです。ヨウ素液はうすめて使い、目や口に入らないように気をつけます。</p>
<h3>このシミュレーションで単純にしていること</h3>
<ul>
<li>発芽までの日数・高さ・葉の数は目安です。実際は種子や温度によってちがいます。</li>
<li>土は、肥料（養分）をふくまないバーミキュライトなどを使うものとしています（学習指導要領の解説も、養分をふくまない保水性のある土を使うことを挙げています）。「肥料あり」は肥料をとかした水をあたえることを表します。</li>
<li>温度は「あたたかい部屋（約20〜25℃）」と「冷蔵庫（約5℃）」の2つだけです。冷蔵庫に入れると日光は自動的に「なし」になります。</li>
<li>水にしずめた種子は、水の中の空気（酸素）が足りないので発芽しないものとしています。</li>
</ul>
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「小学校学習指導要領（平成29年告示）解説 理科編」第5学年 B（1）植物の発芽，成長，結実（pp.68〜69）（<a href="''' + MEXT_SHO + '''" target="_blank" rel="noopener">文部科学省 小学校学習指導要領解説のページ</a>）</li>
<li>小学校理科（5年）の教科書の「植物の発芽と成長」の単元</li>
</ul>
'''

HATSUGA_FAQS = [
    ("種子が発芽するのに必要な条件は何ですか？", "水・空気・適当な温度の3つです。日光や肥料は、発芽には必要ありません。"),
    ("日光や肥料は、植物に必要ないのですか？", "発芽には必要ありませんが、発芽したあとに植物がよく成長するためには必要です。日光に当てないと、くきがひょろ長くのび、葉が黄色っぽくなります。肥料がないと、葉の数が少なく、小さくなります。"),
    ("発芽の条件を調べるとき、冷蔵庫の中とくらべるカップに箱をかぶせるのはなぜですか？", "冷蔵庫の中は暗いからです。くらべるカップを明るい所に置くと、温度と日光の2つの条件がちがってしまいます。箱をかぶせて暗くすると、ちがう条件が温度だけになり、正しくくらべられます。"),
    ("条件をそろえるとは、どういうことですか？", "調べたい条件だけを変えて、それ以外の条件はすべて同じにすることです。たとえば水が必要かを調べるときは、水の有無だけを変え、空気・温度・日光などは同じにします。"),
    ("インゲンマメは何を養分にして発芽するのですか？", "種子の中の子葉にたくわえられたでんぷんを養分にして発芽します。発芽前の子葉はヨウ素液で青むらさき色になりますが、発芽して育ったあとのしぼんだ子葉は、ほとんど色が変わりません。"),
]

HATSUGA_JS = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const h1=document.querySelector('.sim-head h1'); if(h1&&!h1.children.length){ const t=h1.textContent, i=t.indexOf('（'); if(i>0){ h1.textContent=t.slice(0,i); const sp=document.createElement('span'); sp.style.display='inline-block'; sp.textContent=t.slice(i); h1.appendChild(sp); } }
  function setV(id,s){ const e=$(id); if(!e||e.textContent===s) return; e.textContent=s; e.style.fontSize=s.length>9?'14px':(s.length>6?'16px':''); }
  function rrect(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
  function txt(t,x,y,size,col,weight,align,maxW,halo){ ctx.textAlign=align||'left'; let s=size; ctx.font=(weight||'')+' '+s+'px sans-serif';
    if(maxW){ while(ctx.measureText(t).width>maxW&&s>8){ s-=0.5; ctx.font=(weight||'')+' '+s+'px sans-serif'; } }
    if(halo){ ctx.lineWidth=3.5; ctx.strokeStyle='rgba(255,255,255,.92)'; ctx.lineJoin='round'; ctx.strokeText(t,x,y); }
    ctx.fillStyle=col||'#0f172a'; ctx.fillText(t,x,y); }
  function dot(x,y,r,c){ ctx.fillStyle=c; ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.fill(); }
  function hex(c){ return [parseInt(c.slice(1,3),16),parseInt(c.slice(3,5),16),parseInt(c.slice(5,7),16)]; }
  function mix(a,b,t){ const A=hex(a),B=hex(b); t=clamp(t,0,1); return 'rgb('+A.map((v,i)=>Math.round(v+(B[i]-v)*t)).join(',')+')'; }

  const GD=3, DMAX=20, KEYS=['w','a','t','s','f'], NM=['水','空気','温度','日光','肥料'], NEED=['水','空気','適当な温度','日光','肥料'];
  const LET=['A','B','C','D'], SELC=['#2563eb','#ea580c'];
  const B0={w:1,a:1,t:1,s:1,f:0};
  const PRE={water:[{},{w:0}], air:[{},{a:0}], temp:[{s:0},{t:0,s:0}], bad:[{},{t:0,s:0}], sun:[{},{s:0}],
             gsun:[{f:1},{f:1,s:0}], gfert:[{f:1},{f:0}], all:[{},{w:0},{a:0},{t:0,s:0}]};
  let cups=[], sel=[0,1], day=+$('day').value, run=false, iod=false, flash=null, tnow=0;
  function mk(o){ return Object.assign({},B0,o); }
  function loadPre(p){ if(!PRE[p]) return; cups=PRE[p].map(mk); sel=[0,1]; }
  const okG=(c)=>c.w&&c.a&&c.t;
  const germ=(c,d)=>!!(okG(c)&&d>=GD);
  function hgt(c,g){ if(g<2.5) return 0; const p=(c.s&&c.f)?[28,8]:(c.s?[16,6]:[36,7]); return 2+(p[0]-2)*(1-Math.exp(-(g-2.5)/p[1])); }
  function starch(c,d){ if(!germ(c,d)) return 1; const g=d-GD; return c.s?Math.max(0.08,1-g/10):Math.max(0.03,1-g/9); }
  function cls(c){ return c.s&&c.f?3:(c.s?2:1); }

  // ---- 比べ方の判定
  function comp(){ const i=Math.min(sel[0],sel[1]), j=Math.max(sel[0],sel[1]), A=cups[i], B=cups[j], LA=LET[i], LB=LET[j];
    const dif=[]; KEYS.forEach((k,n)=>{ if(A[k]!==B[k]) dif.push(n); }); const nd=dif.length, d0=dif[0];
    let l1, col, l2, sh;
    if(nd===0){ l1=LA+' と '+LB+' は、条件がすべて同じ'; col='#64748b'; }
    else if(nd===1){ l1=LA+' と '+LB+'：ちがう条件は「'+NM[d0]+'」だけ ✔ 正しい比べ方'; col='#15803d'; }
    else { l1='⚠ '+LA+' と '+LB+'：ちがう条件が'+nd+'つ（'+dif.map((n)=>NM[n]).join('・')+'）→ 原因が分からない比べ方'; col='#b91c1c'; }
    const gi=germ(A,day), gj=germ(B,day);
    if(day<GD){ l2='まだ発芽していない。どうなるか予想してから ▶ 早送りで観察しよう'; sh='観察を続けよう'; }
    else if(gi!==gj){ const Y=gi?LA:LB, Nn=gi?LB:LA;
      if(nd===1){ l2=Y+' は発芽した・'+Nn+' は発芽しない → 発芽には'+NEED[d0]+'が必要'; sh='発芽に'+NEED[d0]+'が必要'; }
      else { l2=Y+' は発芽した・'+Nn+' は発芽しない → でも、ちがう条件が'+nd+'つあるので、どれが原因か決められない'; sh='比べ方を直そう'; } }
    else if(gi&&gj){
      if(nd===0){ l2='どちらも同じように発芽・成長している（同じ条件なので同じ結果）'; sh='同じ結果'; }
      else if(nd===1){ if(day<12){ l2='どちらも発芽した → 発芽に'+NM[d0]+'は必要ない。成長のちがいは、もっと日がたつと分かる'; sh='発芽に'+NM[d0]+'は不要'; }
        else { const gd=cls(A)>=cls(B)?LA:LB, bd=gd===LA?LB:LA;
          if(d0===3){ l2=gd+' は葉が緑色でよく育ち、'+bd+' はひょろ長く葉が黄色い → 成長には日光が必要（発芽にはいらない）'; sh='成長に日光が必要'; }
          else { l2=gd+' は葉が多く大きく育ち、'+bd+' は葉が少なく小さい → 成長には肥料が関係している'; sh='成長に肥料が関係'; } } }
      else { l2='どちらも発芽した。ちがう条件が'+nd+'つあるので、成長のちがいの原因は決められない'; sh='比べ方を直そう'; } }
    else { l2='どちらも発芽しない'+(nd>=1?'（どちらにも、発芽に必要な条件が足りない）':''); sh=nd>=2?'比べ方を直そう':'どちらも発芽しない'; }
    if(nd>=2&&day>=GD) sh='比べ方を直そう';
    return {i:i,j:j,dif:dif,nd:nd,l1:l1,l2:l2,col:col,sh:sh}; }

  // ---- 描画
  const SURF=246, CTOP=236, CBOT=300, PX=5, CH0=344, CHH=23, CHG=27;
  function colX(i){ const cw=624/cups.length; return [8+i*cw,cw]; }
  function bean(x,y,sc,rot){ ctx.save(); ctx.translate(x,y); ctx.rotate(rot||0); ctx.scale(sc,sc); ctx.beginPath(); ctx.moveTo(-12,0); ctx.bezierCurveTo(-12,-10,10,-11,12,-2); ctx.bezierCurveTo(13,6,4,8,0,4); ctx.bezierCurveTo(-4,8,-12,7,-12,0); ctx.closePath();
    ctx.fillStyle='#9a3412'; ctx.fill(); ctx.strokeStyle='#5b210b'; ctx.lineWidth=1; ctx.stroke(); ctx.fillStyle='rgba(254,215,170,.55)'; [[-6,-3],[2,-5],[7,0],[-3,2]].forEach((p)=>{ ctx.beginPath(); ctx.ellipse(p[0],p[1],2,1.2,0.4,0,Math.PI*2); ctx.fill(); }); ctx.restore(); }
  function leafE(x,y,len,wid,ang,col){ if(len<1) return; ctx.save(); ctx.translate(x,y); ctx.rotate(ang); ctx.beginPath(); ctx.moveTo(0,0); ctx.bezierCurveTo(len*0.25,-wid,len*0.75,-wid*0.9,len,0); ctx.bezierCurveTo(len*0.75,wid*0.9,len*0.25,wid,0,0); ctx.closePath(); ctx.fillStyle=col; ctx.fill(); ctx.strokeStyle='rgba(20,83,45,.6)'; ctx.lineWidth=1; ctx.stroke(); ctx.beginPath(); ctx.moveTo(2,0); ctx.lineTo(len-3,0); ctx.stroke(); ctx.restore(); }
  function trifo(x,y,sz,col,side){ leafE(x,y,22*sz,8*sz,side<0?Math.PI+0.3:-0.3,col); leafE(x,y,22*sz,8*sz,-Math.PI/2+side*0.12,col); leafE(x,y,20*sz,7.5*sz,side<0?Math.PI*0.8:Math.PI*0.2,col); }
  // 観察スケッチ風の絵（art/*.webp・2026-10-19）。読み込めないときは、これまでのコードでかいた絵を出す
  const ART={};
  ['tane','me','shiyou','honba','sanshutsu','kurai'].forEach((k)=>{ const im=new Image(); im.onload=()=>{ ART[k]=im; }; im.src='art/ingen-'+k+'.webp'; });
  function artUp(k,cx,base,h){ const im=ART[k]; if(!im) return false; const w=im.width*h/im.height; ctx.drawImage(im,cx-w/2,base-h,w,h); return true; }
  function drawPlant(c,cx,d){ const sub=!c.a, z=cups.length<=2?1.3:(cups.length===3?1.12:1);
    const sw=c.w?Math.min(1,d/1):0, sc=(1+0.45*sw)*z, by=sub?266:SURF-2;
    if(!germ(c,d)){ if(ART.tane){ const im=ART.tane, w=30*sc, h=im.height*w/im.width; ctx.drawImage(im,cx-w/2,by-h/2,w,h); } else bean(cx,by,sc*0.9,-0.15); return 0; }
    const g=d-GD, Hh=hgt(c,g), hp=Hh*PX, light=c.s, sf=c.s&&c.f;
    const stemC=light?'#4d7c0f':'#c9bd5f', lfC=sf?'#15803d':(light?'#65a30d':'#d9cf5c'), oldC=light&&!c.f&&g>11?'#b5b83a':lfC;
    // 根
    const rl=Math.min(48,g*13+4); ctx.strokeStyle='#f5f5f4'; ctx.lineWidth=2.4; ctx.lineCap='round'; ctx.beginPath(); ctx.moveTo(cx,SURF+2); ctx.quadraticCurveTo(cx+3,SURF+rl*0.5,cx-1,SURF+rl); ctx.stroke();
    ctx.lineWidth=1.3; for(let k=1;k<=Math.min(4,Math.floor(g/1.5));k++){ const y=SURF+6+k*9; if(y>SURF+rl-4) break; const s=k%2?1:-1; ctx.beginPath(); ctx.moveTo(cx+1,y); ctx.quadraticCurveTo(cx+s*8,y+3,cx+s*(10+Math.min(10,g*1.5)),y+8); ctx.stroke(); }
    if(ART.me&&ART.shiyou&&ART.honba&&ART.sanshutsu&&ART.kurai){ const gg=d-GD;
      if(gg<2.5){ artUp('me',cx,SURF+2,Math.max(16,gg*9+10)*z); return Hh; }
      const k=!light?'kurai':(sf&&gg>=13?'sanshutsu':(gg>=5?'honba':'shiyou'));
      artUp(k,cx+((!light&&gg>14)?(gg-14)*2:0),SURF+2,Math.max(30*z,hp+12*z)); return Hh; }
    const S=starch(c,d), cs=0.45+0.55*S;
    if(g<2.5){ // 種子の中からくきが出てくる
      const hh=Math.max(0,(g-1))*9; bean(cx,SURF-2,sc*0.9,-0.15);
      if(hh>0){ ctx.strokeStyle=stemC; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(cx+2,SURF-4); ctx.quadraticCurveTo(cx+8,SURF-4-hh*1.4,cx+12,SURF-4-hh*0.4); ctx.stroke(); }
      return Hh; }
    const top=SURF-hp, lean=(!light&&g>14)?(g-14)*5:0, lw=light?3.4*Math.min(z,1.15):2.2;
    ctx.strokeStyle=stemC; ctx.lineWidth=lw; ctx.beginPath(); ctx.moveTo(cx,SURF); ctx.quadraticCurveTo(cx,top+hp*0.3,cx+lean,top); ctx.stroke();
    const xAt=(y)=>cx+lean*Math.pow(clamp((SURF-y)/Math.max(1,hp),0,1),2);
    // 子葉
    const yc=SURF-Math.min(hp,34), cC=light?mix('#d9c27a','#84cc16',Math.min(1,g/6)):'#ead9a0';
    if(S>0.06){ const xc=xAt(yc); ctx.fillStyle=cC; ctx.strokeStyle='rgba(120,53,15,.6)'; ctx.lineWidth=1; [-1,1].forEach((s)=>{ ctx.beginPath(); ctx.ellipse(xc+s*9*cs*z,yc+1,10*cs*z,6*cs*z,s*0.3,0,Math.PI*2); ctx.fill(); ctx.stroke(); }); }
    // 本葉（初生葉）と三出複葉
    const pg=clamp((g-5)/3,0,1)*(sf?1:(light?0.8:0.55))*z; const t1d=sf?9:11, t1=light?clamp((g-t1d)/3,0,1)*(sf?1:0.65):0, t2=sf?clamp((g-13)/3,0,1):0;
    if(pg>0){ const yp=t1>0?SURF-hp*0.62:top; const xp=xAt(yp); leafE(xp,yp,30*pg,13*pg,Math.PI+0.35,oldC); leafE(xp,yp,30*pg,13*pg,-0.35,oldC); }
    if(t1>0){ const y1=t2>0?SURF-hp*0.85:top; trifo(xAt(y1),y1,t1*z,lfC,-1); }
    if(t2>0){ trifo(xAt(top),top,t2*z,lfC,1); }
    return Hh; }
  function cupDraw(c,cx,cw){ const tw=Math.min(104,cw-34), bw=tw*0.76;
    ctx.beginPath(); ctx.moveTo(cx-tw/2,CTOP); ctx.lineTo(cx+tw/2,CTOP); ctx.lineTo(cx+bw/2,CBOT); ctx.lineTo(cx-bw/2,CBOT); ctx.closePath(); ctx.fillStyle='rgba(241,245,249,.7)'; ctx.fill();
    const my=c.a?SURF:272; const fx=(y)=>tw/2-(tw-bw)/2*(y-CTOP)/(CBOT-CTOP);
    ctx.beginPath(); ctx.moveTo(cx-fx(my),my); ctx.lineTo(cx+fx(my),my); ctx.lineTo(cx+bw/2,CBOT); ctx.lineTo(cx-bw/2,CBOT); ctx.closePath(); ctx.fillStyle=c.w?(c.f?'#9c7b4f':'#a68b5b'):'#e4d8bd'; ctx.fill();
    ctx.fillStyle=c.w?'rgba(120,90,50,.35)':'rgba(160,140,100,.35)'; for(let k=0;k<14;k++){ const x=cx-bw/2+6+((k*37)%Math.max(8,bw-12)), y=my+6+((k*13)%Math.max(6,CBOT-my-10)); ctx.fillRect(x,y,2.4,1.6); }
    if(c.f&&c.w){ for(let k=0;k<6;k++) dot(cx-bw/2+10+k*(bw-20)/5,CBOT-8-(k%2)*8,1.6,'rgba(14,165,233,.7)'); }
    return {tw:tw,bw:bw,my:my}; }
  function cupGlass(c,cx,g){ const tw=g.tw,bw=g.bw; if(!c.a){ ctx.beginPath(); ctx.moveTo(cx-tw/2+1,CTOP+4); ctx.lineTo(cx+tw/2-1,CTOP+4); ctx.lineTo(cx+bw/2,CBOT); ctx.lineTo(cx-bw/2,CBOT); ctx.closePath(); ctx.fillStyle='rgba(56,189,248,.38)'; ctx.fill(); txt('水にしずめた',cx,CTOP+18,10.5,'#0369a1','bold','center',tw-6,true); }
    ctx.beginPath(); ctx.moveTo(cx-tw/2,CTOP); ctx.lineTo(cx-bw/2,CBOT); ctx.lineTo(cx+bw/2,CBOT); ctx.lineTo(cx+tw/2,CTOP); ctx.strokeStyle='#64748b'; ctx.lineWidth=1.8; ctx.stroke(); ctx.beginPath(); ctx.moveTo(cx-tw/2-3,CTOP); ctx.lineTo(cx+tw/2+3,CTOP); ctx.stroke(); }
  function chipText(c,j){ if(j===0) return c.w?'水：あり ○':'水：なし ×'; if(j===1) return c.a?'空気：ふれる ○':'空気：水にしずめる ×';
    if(j===2) return c.t?'温度：あたたかい ○':'温度：冷蔵庫 ×'; if(j===3) return c.s?'日光：当てる ○':(c.t?'日光：箱で暗く ×':'日光：なし（暗い）×'); return c.f?'肥料：あり ○':'肥料：なし ×'; }
  function draw(){ ctx.fillStyle='#ffffff'; ctx.fillRect(0,0,W,H); const C=comp();
    // 判定バナー
    ctx.fillStyle=C.nd===1?'#f0fdf4':(C.nd>=2?'#fef2f2':'#f8fafc'); rrect(6,4,628,56,10); ctx.fill(); ctx.strokeStyle=C.col; ctx.lineWidth=2; rrect(6,4,628,56,10); ctx.stroke();
    txt(C.l1,16,25,14,C.col,'bold','left',540); txt(Math.round(day*10)/10+'日目',626,25,15,'#0e7490','bold','right');
    txt(C.l2,16,48,13,'#0f172a','bold','left',608);
    cups.forEach((c,i)=>{ const cx0=colX(i), x0=cx0[0], cw=cx0[1], cx=x0+cw/2, isSel=sel.indexOf(i)>=0, ord=(i===C.i)?0:1;
      ctx.fillStyle=!c.t?'#e0f2fe':(!c.s?'#e7e5e4':'#fffbeb'); rrect(x0+3,66,cw-6,272,10); ctx.fill();
      if(isSel){ ctx.strokeStyle=SELC[ord]; ctx.lineWidth=3; rrect(x0+3,66,cw-6,272,10); ctx.stroke(); }
      dot(x0+20,86,13,isSel?SELC[ord]:'#94a3b8'); txt(LET[i],x0+20,92,16,'#fff','bold','center');
      if(!c.t) txt('冷蔵庫（約5℃・暗い）',x0+38,90,11,'#0369a1','bold','left',cw-44);
      else if(!c.s) txt('箱をかぶせて暗く',x0+38,90,11,'#44403c','bold','left',cw-44);
      else { const sx=x0+cw-22, sy=84; ctx.strokeStyle='#f59e0b'; ctx.lineWidth=1.6; for(let k=0;k<8;k++){ const q=k*Math.PI/4; ctx.beginPath(); ctx.moveTo(sx+Math.cos(q)*9,sy+Math.sin(q)*9); ctx.lineTo(sx+Math.cos(q)*13,sy+Math.sin(q)*13); ctx.stroke(); } dot(sx,sy,7,'#fbbf24'); txt('日光',sx-18,sy+5,11,'#b45309','bold','right'); }
      const g=cupDraw(c,cx,cw); const Hc=drawPlant(c,cx,day); cupGlass(c,cx,g);
      // 状態
      let s1, s2; const ge=germ(c,day);
      if(ge){ s1='発芽した（'+GD+'日目）'; s2=Hc>0?'高さ 約'+Math.round(Hc)+'cm':'根が出た'; }
      else if(c.w){ s1=day<1?'水を吸っている':'ふくらんだ'; s2=day>=GD+2?'発芽しない':'まだ発芽しない'; } else { s1='かわいたまま'; s2=day>=GD+2?'発芽しない':'変化なし'; }
      txt(s1,cx,316,12.5,ge?'#15803d':'#475569','bold','center',cw-12); txt(s2,cx,332,12,ge?'#334155':(s2==='発芽しない'?'#b91c1c':'#64748b'),ge?'':'bold','center',cw-12);
      if(iod){ const S=starch(c,day), ix=x0+cw-30, iy=128; ctx.fillStyle='rgba(255,255,255,.95)'; rrect(ix-25,iy-22,50,62,8); ctx.fill(); ctx.strokeStyle='#a855f7'; ctx.lineWidth=1.2; rrect(ix-25,iy-22,50,62,8); ctx.stroke();
        ctx.fillStyle=mix('#f3e3c3','#3b0764',0.1+0.75*S); ctx.beginPath(); ctx.ellipse(ix,iy,17,11,0,0,Math.PI*2); ctx.fill(); ctx.strokeStyle='#78350f'; ctx.lineWidth=1; ctx.stroke(); ctx.beginPath(); ctx.moveTo(ix-17,iy); ctx.lineTo(ix+17,iy); ctx.stroke();
        txt('子葉',ix,iy+24,10,'#6b21a8','bold','center'); txt(S>0.6?'でんぷん多い':(S>0.25?'へった':'ほぼない'),ix,iy+35,9.5,'#6b21a8','bold','center',48); }
      // 条件の札
      for(let j=0;j<5;j++){ const y=CH0+j*CHG, on=!!c[KEYS[j]], diff=isSel&&C.dif.indexOf(j)>=0;
        ctx.fillStyle=on?'#dcfce7':'#fee2e2'; rrect(x0+5,y,cw-10,CHH,6); ctx.fill(); ctx.strokeStyle=on?'#16a34a':'#dc2626'; ctx.lineWidth=1.2; rrect(x0+5,y,cw-10,CHH,6); ctx.stroke();
        if(diff){ const a=0.55+0.45*Math.abs(Math.sin(tnow*3)); ctx.strokeStyle='rgba(245,158,11,'+a+')'; ctx.lineWidth=3.5; rrect(x0+3,y-2,cw-6,CHH+4,7); ctx.stroke(); }
        txt(chipText(c,j),cx,y+16,12,on?'#14532d':'#7f1d1d','bold','center',cw-18); } });
    if(flash&&flash.t>0){ ctx.fillStyle='rgba(15,23,42,.88)'; rrect(60,200,520,44,10); ctx.fill(); txt(flash.m,320,227,14,'#fff','bold','center',500); }
    txt('カップをタップ → くらべる2つを選ぶ　札をタップ → ○×を切りかえる',320,494,11.5,'#64748b','','center',620); }

  function update(){ const C=comp(), gl=cups.map((c,i)=>germ(c,day)?LET[i]:null).filter((x)=>x);
    setV('s1',Math.round(day*10)/10+'日目'); setV('s2',(gl.length?gl.join('・'):'なし')+'（'+gl.length+'/'+cups.length+'）');
    setV('s3',C.nd===0?'なし（同じ条件）':(C.nd===1?NM[C.dif[0]]+'だけ':C.dif.map((n)=>NM[n]).join('・')+'（'+C.nd+'つ）')); setV('s4',C.sh);
    setShare('【発芽の条件】カップ'+LET[C.i]+'と'+LET[C.j]+'（ちがう条件：'+(C.nd?C.dif.map((n)=>NM[n]).join('・'):'なし')+'）を'+Math.round(day)+'日目にくらべると → '+C.sh+'。発芽に必要なのは水・空気・適当な温度｜シミュラボ'); }
  function setPlay(){ $('play').textContent=run?'⏸ 止める':'▶ 早送り'; }
  function setDay(v){ day=clamp(v,0,DMAX); $('day').value=day; $('dayL').textContent=(Math.round(day*10)/10)+'日目'; }
  $('pre').addEventListener('change',()=>{ if($('pre').value==='free') return; loadPre($('pre').value); run=false; setDay(0); setPlay(); update(); });
  $('day').addEventListener('input',()=>{ day=+$('day').value; update(); });
  $('play').addEventListener('click',()=>{ if(!run&&day>=DMAX-0.01) setDay(0); run=!run; setPlay(); });
  $('rst').addEventListener('click',()=>{ run=false; setDay(0); setPlay(); update(); });
  $('iod').addEventListener('click',()=>{ iod=!iod; $('iod').textContent=iod?'🔍 ヨウ素液をやめる':'🔍 子葉をヨウ素液で調べる'; });
  $('add').addEventListener('click',()=>{ if(cups.length<4){ cups.push(mk({})); $('pre').value='free'; update(); } });
  $('rem').addEventListener('click',()=>{ if(cups.length>2){ cups.pop(); sel=sel.map((k)=>Math.min(k,cups.length-1)); if(sel[0]===sel[1]) sel=[0,1]; $('pre').value='free'; update(); } });
  function toggle(c,j){ if(j===0){ c.w^=1; if(!c.w) c.a=1; } else if(j===1){ c.a^=1; if(!c.a) c.w=1; } else if(j===2){ c.t^=1; if(!c.t) c.s=0; }
    else if(j===3){ if(!c.t){ flash={m:'冷蔵庫の中は暗いので、日光は当てられません',t:2}; return; } c.s^=1; } else c.f^=1; $('pre').value='free'; }
  cv.addEventListener('pointerdown',(e)=>{ const p=cpos(cv,e), x=p[0]/dpr, y=p[1]/dpr; const cw=624/cups.length, i=Math.floor((x-8)/cw); if(i<0||i>=cups.length) return;
    if(y>=CH0-2&&y<CH0+5*CHG){ const j=Math.floor((y-CH0+2)/CHG); if(j>=0&&j<5){ toggle(cups[i],j); if(sel.indexOf(i)<0) sel=[sel[1],i]; update(); e.preventDefault(); } }
    else if(y>=64&&y<=340){ if(sel.indexOf(i)<0){ sel=[sel[1],i]; update(); } e.preventDefault(); } });
  let last=performance.now(), acc=0;
  function loop(now){ const dt=Math.min(0.05,Math.max(0,(now-last)/1000)); last=now; tnow+=dt;
    if(run){ setDay(day+dt*1.6); if(day>=DMAX){ run=false; setPlay(); } }
    if(flash){ flash.t-=dt; if(flash.t<=0) flash=null; }
    acc+=dt; if(run||acc>0.3){ acc=0; update(); }
    draw(); requestAnimationFrame(loop); }
  loadPre('water'); setDay(day); update(); draw(); requestAnimationFrame(loop);
'''

sim(slug="hatsuga-jouken", cat="rika", emoji="🫘", score=80,
    title="種子の発芽と成長の条件シミュレーター（インゲンマメ・条件をそろえる実験）",
    title_tag="発芽の条件シミュレーション｜水・空気・温度・日光・肥料を変えてインゲンマメの発芽と成長をくらべる（小5理科）",
    meta_desc="小5理科「植物の発芽，成長，結実」のシミュレーション。インゲンマメのカップを並べ、水・空気・温度・日光・肥料の条件を○×で変えて早送りで観察。くらべる2つのちがう条件が光るので、条件のそろえ方（条件制御）が分かります。子葉のでんぷんをヨウ素液で調べる機能つき。",
    og_title="種子の発芽と成長の条件シミュレーター（インゲンマメ）",
    og_desc="発芽に必要なのは水・空気・適当な温度。日光と肥料は成長に必要。カップの条件を変えて早送りで確かめ、条件のそろえ方も学べる。",
    card_desc="水・空気・温度・日光・肥料を○×で変えてインゲンマメを早送り。条件のそろえ方も分かる。",
    lead="インゲンマメの種子をまいたカップをならべ、水・空気・温度・日光・肥料の条件を変えて、早送りで発芽と成長のようすを見られます。くらべる2つのカップの「ちがう条件」が光ります。",
    model="小5 植物の発芽，成長，結実", level="小学5年",
    unit="小学校 第5学年 B（1）植物の発芽，成長，結実",
    canvas=canvas(640, 500, light=True),
    controls=select("pre", "実験", [("water", "① 水は必要？"), ("air", "② 空気は必要？（水にしずめる）"), ("temp", "③ 温度は関係する？（冷蔵庫と箱）"),
                                   ("bad", "④ まちがいやすい比べ方（窓辺と冷蔵庫）"), ("sun", "⑤ 日光は発芽に必要？"), ("gsun", "⑥ 成長と日光"),
                                   ("gfert", "⑦ 成長と肥料"), ("all", "⑧ 4つのカップを一度に"), ("free", "（自分で条件を変える）")])
             + slider("day", "日数", 0, 20, 10, 0.5, "{v}日目"),
    buttons=btn("play", "▶ 早送り", True) + btn("rst", "⏮ 0日目にもどす") + btn("iod", "🔍 子葉をヨウ素液で調べる")
            + btn("add", "＋ カップを足す") + btn("rem", "− カップを減らす"),
    stats=stats([("s1", "日数", False), ("s2", "発芽したカップ", False), ("s3", "くらべる2つのちがい", False), ("s4", "わかること", True)]),
    legend="インゲンマメの種子を、肥料（養分）をふくまない土（バーミキュライト）にまいたようすの模式図です。日数・高さは、あたたかい部屋で育てたときの目安です。カップをタップすると、くらべる2つ（青・オレンジのわく）を選べます。下の札をタップすると条件の○×が切りかわり、2つのカップでちがう条件の札が光ります。",
    article=HATSUGA_ARTICLE, faqs=HATSUGA_FAQS,
    rel=[("kougousei", "🍃", "光合成と呼吸のシミュレーター"), ("furiko-jikken", "⏱️", "振り子の実験シミュレーター（条件をそろえる）"),
         ("mendel-iden", "🌱", "遺伝の規則性シミュレーター"), ("nagareru-mizu", "🏞️", "流れる水の働きシミュレーター"), ("taiyou-ugoki", "🌞", "太陽の1日の動きと季節")],
    js=HATSUGA_JS)
