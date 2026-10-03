# -*- coding: utf-8 -*-
"""理科の授業向け（天文）：月の満ち欠けの仕組み／月食・日食シミュレーター
   照合メモ
   - 月齢＝平均朔望月 29.530588853日・基準新月 2000-01-06 18:14 UTC（目安）。国立天文台の正午月齢（東京 2026年10月）と比べると 0.73〜0.76日小さい。
     Meeus の真の朔望で 2000〜2040年を調べると、モデル月齢は真の月齢より最大0.73日小さく〜0.43日大きくなる。
   - 南中時刻＝12時＋月齢×24/29.53時。国立天文台（東京 2026年10月）との差は −8分〜＋57分。
   - 食のしきい値・食分・継続時間は Meeus『Astronomical Algorithms』54章の式（地球半径単位、u＝本影円錐の半径）。
     国立天文台の一覧に載る2025〜2030年の月食10回・日食14回の種類（皆既・部分・金環）がすべて一致することを確認済み（半影月食は一覧に無い）。
"""
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

A = lambda url, text=None: '<a href="%s" rel="noopener" target="_blank">%s</a>' % (url, text or url)
NW = lambda t: '<span style="white-space:nowrap">%s</span>' % t   # 表の短いセルを折り返さない

# ============================================================ 1 月の満ち欠けの仕組み
sim(slug="tsuki-michikake", cat="rika", emoji="🌓", score=82,
    title="月の満ち欠けの仕組みシミュレーター（月の形と見える時刻・方角）",
    title_tag="月の満ち欠けの仕組みシミュレーター｜月の形が変わる理由と見える時刻・方角",
    meta_desc="月の満ち欠けはなぜ起こる？宇宙（北極側）から見た太陽の光・地球・月の位置と、日本から見た月の形・方角を並べて動かせる無料シミュレーター。月齢と時刻のスライダーで、上弦の月が夕方に南の空に見える理由などを確かめられます。小4・小6・中3の理科の授業に。",
    og_title="月の満ち欠けの仕組みシミュレーター",
    og_desc="宇宙から見た位置関係と、日本から見た月の形・方角が連動。月齢と時刻を動かして、満ち欠けの仕組みを確かめよう。",
    card_desc="月齢と時刻を動かすと、宇宙から見た位置と日本から見た月の形・方角が連動。上弦の月が夕方南に見える理由も。",
    lead="月は自分では光らず、太陽の光が当たった半分が光っています。左の「宇宙（北極の上）から見た図」と右の「日本から見た空」が連動するので、月齢と時刻を動かして、月の形と見える方角・時刻がどう変わるかを確かめてください。",
    model="小4 月と星／小6 月と太陽／中3 月や金星の運動と見え方",
    level="小学4年・6年、中学3年",
    unit="小学校 第4学年 B(5)「月と星」・第6学年 B(5)「月と太陽」／中学校 第2分野（6）地球と宇宙（月や金星の運動と見え方）",
    canvas=canvas(640, 420),
    controls=slider("age", "月齢（新月からの日数）", 0, 29.5, 7.4, 0.1, "{v}日") + slider("hour", "時刻（日本）", 0, 24, 18, 0.5)
           + select("preset", "形をえらぶ", [("", "（スライダーで動かす）"), ("0", "新月（月齢0）"), ("2.5", "三日月（月齢2〜3）"), ("7.38", "上弦の月（月齢7.4）"),
                                          ("14.77", "満月（月齢14.8）"), ("22.15", "下弦の月（月齢22.1）"), ("27", "明け方の細い月（月齢27）")]),
    buttons=btn("today", "📅 今日の月齢にする", True) + btn("play", "▶ 時刻を進める") + btn("plus1", "＋1日（同じ時刻）"),
    stats=stats([("sAge", "月齢", False), ("sName", "月の名前", True), ("sWin", "見える時間帯（目安）", False), ("sTr", "南中時刻（目安）", False)]),
    legend="左：北極の上から見た太陽の光・地球・月（大きさと距離は誇張）。赤い点が日本、白い線がその地平線で、線より外側にある月が見えます。右：日本（北緯35°）で南を向いて見た空。黄色い点線の先に太陽があります。左の図の月や日本、右の空を指でドラッグしても動かせます。",
    article='''
<h2>このシミュレーションでわかること</h2>
<p>月は自分では光らず、太陽の光が当たっている半分だけが光っています。月が地球のまわりを回る（公転する）と、その光っている半分を地球から見る向きが変わるので、月の形は<b>新月→三日月→上弦の月→満月→下弦の月→新月</b>と、平均約29.5日で変わって見えます。これが月の満ち欠けです。</p>
<p>また、地球は1日に1回まわっている（自転している）ので、月も太陽と同じように東からのぼり、南の空を通って西にしずみます。月の形によって、見える時刻と方角が決まっています。</p>
''' + T([[NW("小学校4年"), NW("B(5) 月と星"), "月は日によって形が変わって見え、1日のうちでも時刻によって位置が変わること"],
          [NW("小学校6年"), NW("B(5) 月と太陽"), "月の輝いている側に太陽があること。月の形の見え方は、太陽と月との位置関係によって変わること（地球から見た位置関係で扱う）"],
          [NW("中学校3年"), "第2分野（6）地球と宇宙「月や金星の運動と見え方」", "月の観察記録や資料に基づいて、月の公転と見え方を関連付けて理解すること"]],
         ["学年", "単元", "学習指導要領（平成29年告示）の内容"]) + '''
<p>学年は一般的な配当です。教科書によって扱う時期が前後することがあります。</p>

<h2>授業での使い方</h2>
<p><b>導入（小4）</b>：右の空の図だけを見せて、時刻のスライダーを動かします。月も太陽と同じように東からのぼり、南を通って西にしずむことを確かめます。「＋1日（同じ時刻）」を押すと、同じ時刻に見える月の位置と形が日ごとに変わることもわかります。</p>
<p><b>展開（小6）</b>：時刻を夕方（18時）にして、「形をえらぶ」で三日月・上弦の月・満月を順に出します。右の図の黄色い点線（太陽の方向）と、月の光っている側を見比べます。小6は地球から見た位置関係で扱うので、左の図は使わなくてもかまいません。</p>
<p><b>展開（中3）</b>：左の図の月を指で動かして公転させ、地球上の日本（赤い点）を動かして自転させます。「日本の地平線より外側に月があるか」「光っている半分のうち、地球に向いている側（水色の線）がどれだけ光っているか」で、見え方を説明させます。</p>
<p><b>まとめ・家庭学習</b>：下の早見表と見比べます。「今日の月齢にする」で今夜の月の形と見える時間を予想し、家で観察する課題にもできます。</p>
<p>児童・生徒への問いの例です。</p>
<ul>
<li>（小4）夕方、南の空に見える月は、どんな形をしているでしょう。（上弦の月。右半分が光っている）</li>
<li>（小6）三日月の光っている側は、どちらを向いていますか。その先には何がありますか。（西の地平線の方。しずんだばかりの太陽がある）</li>
<li>（中3）上弦の月が真夜中に西にしずむのはなぜでしょう。左の図の日本の位置と地平線を使って説明しましょう。</li>
</ul>

<h2>しくみ・解説</h2>
<h3>形が変わって見えるわけ</h3>
<p>太陽の光はいつも同じ向きから来るので、月はいつも太陽に向いた半分が光っています（左の図の月の明るい半分）。地球から見えるのは、地球に向いている半分（水色の線の側）です。この2つの「半分」の重なり方が、月の位置によって変わります。</p>
''' + T([["新月", "太陽と同じ方向", "光っている半分が地球の反対を向く → 見えない"],
          ["上弦の月", "太陽から東へ90°", "光っている半分のうち、地球側の半分が見える → 右半分が光る"],
          ["満月", "太陽と反対の方向", "光っている半分がまるごと地球を向く → 全体が光る"],
          ["下弦の月", "太陽から西へ90°", "左半分が光る"]], ["月", "地球から見た月の方向", "見え方"]) + P("月の満ち欠けは、地球の影が月にかかって起こるのではありません。地球の影に月が入るのは「月食」で、満月のときにまれに起こります。") + '''
<h3>月が見える時刻と方角</h3>
<p>月は1日に約12°ずつ、太陽から東へはなれていきます。そのため、月が南の空でいちばん高くなる時刻（南中時刻）は、1日に約49分ずつおそくなります。このシミュレーションでは次の式で計算しています。</p>
''' + N("南中時刻 ≒ 12時 ＋ 月齢 × 約49分（24時間 ÷ 29.53日）<br>月の出 ≒ 南中の約6時間前　月の入り ≒ 南中の約6時間後") + '''
<p>計算例：月齢10の月の南中時刻は、12時 ＋ 10 × 49分 ＝ 12時 ＋ 8時間10分 ＝ <b>20時10分ごろ</b>。月の出は14時ごろ、月の入りは翌日の2時ごろです。</p>
<h3>早見表（目安）</h3>
''' + T([["0", "新月", "見えない", "12時", "6時〜18時", "太陽と同じ方向で見えない"],
          ["2〜3", "三日月", "右側（西側）が細く光る", "14時", "8時〜20時", "日の入り後の西の空"],
          ["7.4", "上弦の月", "右半分（西側）が光る", "18時", "12時〜24時", "夕方に南の空、真夜中に西にしずむ"],
          ["14.8", "満月", "全体が光る", "0時", NW("18時〜翌6時"), "一晩中。真夜中に南の空"],
          ["22.1", "下弦の月", "左半分（東側）が光る", "6時", "0時〜12時", "明け方に南の空"],
          ["27", "明け方の細い月", "左側（東側）が細く光る", "10時", "4時〜16時", "日の出前の東の空"]],
         ["月齢", "名前", "形（日本から見て）", "南中（ごろ）", "地平線の上にある時間", "見やすい時間と方角"]) + '''
<p>国立天文台の「月はいつどんなふうに見える？昼間も見えるの？」の表（上弦は昼ごろ東から上り、日の入りのころ南、真夜中ごろ西に沈む など）と同じ傾向になります。</p>
<h3>図と対応させて読む（中学校3年）</h3>
<p>左の図で、日本（赤い点）が「夕方」の位置にあるとき、日本の真上の方向（南の空）にあるのは上弦の位置の月です。そのまま地球が6時間まわって日本が「真夜中」の位置に来ると、上弦の月は日本の地平線の西のはしに来ます。これが「上弦の月は夕方に南の空に見え、真夜中に西にしずむ」理由です。同じように考えると、満月は真夜中に南、下弦の月は明け方に南の空に見えます。図では、月の位置の名前（新月・上弦・満月・下弦）と、地球のまわりの時刻（正午・夕方・真夜中・明け方）が同じ向きに並んでいます。その時刻に、その月が南の空に来ます。</p>
<p>右の図では、月の光っている側が、いつも太陽のある方向（黄色い点線の先）を向いています。夕方の三日月は西の低い空で右下が光り、その先にはしずんだばかりの太陽があります。これが小学校6年の「月の輝いている側に太陽がある」ことです。</p>
<h3>このシミュレーションで単純化していること</h3>
<ul>
<li>左の図の大きさと距離は誇張しています。実際の地球と月の距離は地球の直径の約30倍、月の直径は地球の約4分の1、太陽までの距離は月までの約390倍です。</li>
<li>月と太陽は、春分・秋分の日の太陽と同じ通り道（真東からのぼり真西にしずむ。北緯35°で南中の高さ55°）を通るとして計算しています。実際の月の通り道は日によって北や南にずれ、のぼる方角や時刻も変わります。</li>
<li>月齢は、平均の朔望月（29.530588853日）と基準の新月（2000年1月6日18時14分、世界時）から計算した目安です。国立天文台が発表する月齢とは最大で0.8日ほどずれることがあります（例：2026年10月4日正午は、このシミュレーターで22.3、国立天文台の東京の値で23.0）。</li>
<li>南中時刻なども目安です。国立天文台の東京の値と比べると、2026年10月は8分早い〜57分おそいずれがありました。日本の時刻は、東経135°の時刻としています。</li>
</ul>

<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「小学校学習指導要領（平成29年告示）」「中学校学習指導要領（平成29年告示）」理科（''' + A("https://www.mext.go.jp/a_menu/shotou/new-cs/1384661.htm") + '''）</li>
<li>国立天文台「月はいつどんなふうに見える？昼間も見えるの？」（''' + A("https://www.nao.ac.jp/faq/a0201.html") + '''）</li>
<li>国立天文台「「月齢」ってなに？なぜ小数がつくの？」（''' + A("https://www.nao.ac.jp/faq/a0204.html") + '''）</li>
<li>国立天文台 暦計算室「月の出入り 東京（2026年10月）」（''' + A("https://eco.mtk.nao.ac.jp/koyomi/dni/2026/m1310.html") + '''）…月齢・南中時刻の照合に使用</li>
</ul>
''',
    faqs=[("月の満ち欠けはなぜ起こるのですか？", "月は太陽の光を反射して光っていて、いつも太陽に向いた半分が光っています。月が地球のまわりを回ると、その光っている半分を地球から見る角度が変わるため、光って見える部分の形が変わります。周期は平均約29.5日です。"),
          ("地球の影で月が欠けるのではないのですか？", "ちがいます。満ち欠けは、光っている半分の見え方が変わるために起こります。地球の影が月にかかるのは「月食」で、太陽・地球・月が一直線に並ぶ満月のときにだけ、まれに起こります。"),
          ("上弦の月と下弦の月はどう見分けますか？", "日本では、上弦の月は右半分（西側）が光る半月で、夕方に南の空に見えます。下弦の月は左半分（東側）が光る半月で、明け方に南の空に見えます。"),
          ("月の出は毎日どれくらいおそくなりますか？", "平均すると約50分（24時間÷29.53日＝約48.8分）です。実際には日によって幅があり、2026年10月の東京では1日に26分〜72分おそくなりました（国立天文台の月の出の時刻から計算）。"),
          ("昼間に月が見えるのはなぜですか？", "月が地平線より上にあれば、昼でも見えます。上弦の前後の月は午後の東〜南の空に、下弦の前後の月は午前の南〜西の空に見えます。太陽の近くにある細い月は、空が明るいため見つけにくくなります。"),
          ("南半球では月の形はどう見えますか？", "北半球とは左右が逆に見えます。南半球では月を見るときに北を向くので東が右になり、上弦の月は左側が光って見えます。")],
    rel=[("kyou-no-tsuki", "🌙", "今日の月（月齢・満ち欠け・次の満月はいつ？）"), ("gesshoku-nisshoku", "🌘", "月食・日食シミュレーター"),
         ("hiruma-nagasa", "🌅", "昼の長さメーター"), ("hoshizora-shisu", "🔭", "今夜の星空指数"), ("solar-system", "🪐", "太陽系シミュレーター")],
    js=r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const x=cv.getContext('2d'); x.setTransform(dpr,0,0,dpr,0,0);
  cv.style.cursor='pointer';
  const SYN=29.530588853, EPOCH=Date.UTC(2000,0,6,18,14), R=Math.PI/180, LAT=35*R;
  const LX=164, LY=228, RE=22, RO=112;               // 左：宇宙（北極の上）から見た図
  const X0=324, SX0=482, SXW=146, HZ=262, SKY=2.3;   // 右：日本から見た空（高さ1°＝2.3px）
  const F=(s,b)=>(b?'bold ':'')+s+'px system-ui,-apple-system,"Hiragino Sans","Noto Sans JP",sans-serif';
  let age=+$('age').value, hour=+$('hour').value, play=false, todayTxt='', drag=null, last=0, need=true;
  const wrap=(v,m)=>((v%m)+m)%m;
  const lamOf=(a)=>360*a/SYN;                        // 太陽から東へはなれた角度
  const transitH=(a)=>wrap(12+24*a/SYN,24);          // 南中時刻（目安）
  const haMoon=()=>wrap(15*(hour-12)-lamOf(age)+180,360)-180;   // 時角（0＝南中、−90＝東の地平線、＋90＝西）
  const haSun=()=>wrap(15*(hour-12)+180,360)-180;
  function altAz(h){ h*=R; return [Math.asin(Math.cos(LAT)*Math.cos(h))/R, Math.atan2(Math.sin(h),Math.cos(h)*Math.sin(LAT))/R]; }  // 高さ・方位（南から西回り）
  function sky(alt,A){ return [SX0+A/90*SXW, HZ-alt*SKY]; }
  const toS=(mx,my)=>[LX+mx, LY-my];
  const dirName=(A)=>['北','北東','東','南東','南','南西','西','北西'][Math.round(wrap(A+180,360)/45)%8];
  function hm(h){ h=wrap(h,24); let a=Math.floor(h), b=Math.round((h-a)*60); if(b===60){ a=(a+1)%24; b=0; } return a+':'+String(b).padStart(2,'0'); }
  function about(h){ h=wrap(Math.round(h*2)/2,24); const a=Math.floor(h); return a+'時'+(h>a?'半':'')+'ごろ'; }
  function aboutSet(h){ const r=Math.round(h*2)/2; return r===24?'24時ごろ':r>24?'翌'+about(r-24):about(r); }   // 月の入り（24時をこえたら「翌」）
  const word=(h)=>h<4?'真夜中':h<7?'明け方':h<10?'朝':h<14?'昼':h<17?'午後':h<20?'夕方':'夜';
  const isNew=(a)=>a<1||a>=28.5;
  function nameOf(a){
    if(isNew(a)) return ['新月','ほとんど見えない'];
    if(a<4) return ['三日月','右側（西側）が細く光る'];
    if(a<6.4) return ['上弦の前の月','右側が光る・半月より細い'];
    if(a<8.4) return ['上弦の月','右半分（西側）が光る'];
    if(a<13.8) return ['満月の前の月','右側が光る・半月より太い'];
    if(a<15.8) return ['満月','ほぼ全体が光る'];
    if(a<21.2) return ['満月のあとの月','左側が光る・半月より太い'];
    if(a<23.2) return ['下弦の月','左半分（東側）が光る'];
    if(a<26) return ['下弦のあとの月','左側が光る・半月より細い'];
    return ['明け方の細い月','左側（東側）が細く光る'];
  }
  function upWin(a){ if(isNew(a)) return 'ほぼ見えない'; let r=Math.round(wrap(transitH(a)-6,24)); if(r===24) r=0; const s=r+12; return r+'時〜'+(s>24?'翌'+(s-24):s)+'時'; }
  function darkWin(a){ if(isNew(a)) return ''; let st=null, en=null;   // 空が暗く（太陽の高さ−6°以下）、月が高さ5°以上にある時間
    for(let i=0;i<=96;i++){ const h=12+i*0.25; const m=altAz(wrap(15*(h-12)-lamOf(a)+180,360)-180)[0], s=altAz(wrap(15*(h-12)+180,360)-180)[0];
      if(m>5&&s<-6){ if(st===null) st=h; en=h; } }
    return st===null?'':hm(st)+'〜'+hm(en); }
  function lerp(c1,c2,f){ const p=(s)=>[1,3,5].map(i=>parseInt(s.slice(i,i+2),16)); const a=p(c1), b=p(c2); return 'rgb('+a.map((v,i)=>Math.round(v+(b[i]-v)*f)).join(',')+')'; }
  function skyCols(s){ if(s>=8) return ['#4c9be0','#bfe3fa']; if(s<=-12) return ['#060b1c','#111a36'];
    if(s>=0){ const f=s/8; return [lerp('#3a64a0','#4c9be0',f), lerp('#f0b27c','#bfe3fa',f)]; }
    const f=(s+12)/12; return [lerp('#060b1c','#3a64a0',f), lerp('#111a36','#f0b27c',f)]; }
  function rr(a,b,w,h,r){ x.beginPath(); x.moveTo(a+r,b); x.arcTo(a+w,b,a+w,b+h,r); x.arcTo(a+w,b+h,a,b+h,r); x.arcTo(a,b+h,a,b,r); x.arcTo(a,b,a+w,b,r); x.closePath(); }
  // 月の形：e＝太陽からの角度（0＝新月〜180＝満月）、th＝太陽のある向き（画面の角度）
  function phase(cx,cy,r,e,th,lit,dark){
    x.save(); x.translate(cx,cy); x.rotate(th);
    if(dark){ x.fillStyle=dark; x.beginPath(); x.arc(0,0,r,0,2*Math.PI); x.fill(); }
    if(e>0.5){ const a=r*Math.cos(e*R); x.fillStyle=lit; x.beginPath(); x.arc(0,0,r,-Math.PI/2,Math.PI/2,false); x.ellipse(0,0,Math.abs(a),r,0,Math.PI/2,-Math.PI/2,a>0); x.closePath(); x.fill(); }
    x.restore();
  }
  function arc(cx,cy,r,a1,a2,col){ // 反時計回り（数学の角度）の矢印
    x.strokeStyle=col; x.fillStyle=col; x.lineWidth=1.6; x.beginPath();
    for(let i=0;i<=12;i++){ const a=(a1+(a2-a1)*i/12)*R, px=cx+r*Math.cos(a), py=cy-r*Math.sin(a); i?x.lineTo(px,py):x.moveTo(px,py); } x.stroke();
    const a=a2*R, px=cx+r*Math.cos(a), py=cy-r*Math.sin(a), tx=-Math.sin(a), ty=-Math.cos(a), nx=-ty, ny=tx;
    x.beginPath(); x.moveTo(px+tx*6,py+ty*6); x.lineTo(px-tx*2+nx*4.5,py-ty*2+ny*4.5); x.lineTo(px-tx*2-nx*4.5,py-ty*2-ny*4.5); x.closePath(); x.fill();
  }
  function drawSpace(){
    x.fillStyle='#0b1020'; x.fillRect(0,0,X0-2,H);
    x.lineWidth=1;
    for(let y=66;y<=354;y+=36){ x.strokeStyle='rgba(253,224,71,.13)'; x.beginPath(); x.moveTo(6,y); x.lineTo(X0-8,y); x.stroke();
      x.fillStyle='rgba(253,224,71,.6)'; x.beginPath(); x.moveTo(30,y); x.lineTo(21,y-4.5); x.lineTo(21,y+4.5); x.closePath(); x.fill(); }
    x.textAlign='left'; x.textBaseline='alphabetic';
    x.fillStyle='#fff'; x.font=F(13,1); x.fillText('宇宙（北極の上）から見た図',8,20);
    x.fillStyle='#fde68a'; x.font=F(12,1); x.fillText('日本の時刻 '+hm(hour)+'（'+word(hour)+'）',8,38);
    x.fillText('太陽の光 →',8,56);
    // 月の通り道と公転の向き
    x.setLineDash([3,5]); x.strokeStyle='rgba(255,255,255,.28)'; x.beginPath(); x.arc(LX,LY,RO,0,2*Math.PI); x.stroke(); x.setLineDash([]);
    arc(LX,LY,RO,298,330,'rgba(255,255,255,.6)');
    const ga=toS(124*Math.cos(326*R),124*Math.sin(326*R)); x.font=F(10); x.fillStyle='rgba(203,213,225,.85)'; x.textAlign='left'; x.fillText('公転',ga[0]+2,ga[1]+8);
    for(let k=0;k<8;k++){ const l=k*45*R, s=toS(-RO*Math.cos(l),-RO*Math.sin(l)); phase(s[0],s[1],6,90,Math.PI,'rgba(233,228,210,.4)','rgba(70,80,105,.5)'); }
    x.font=F(11,1); x.textAlign='center'; x.textBaseline='middle'; x.fillStyle='#cbd5e1';
    [['新月',0],['上弦',90],['満月',180],['下弦',270]].forEach(d=>{ const l=d[1]*R, s=toS(-136*Math.cos(l),-136*Math.sin(l)); x.fillText(d[0],s[0],s[1]); });
    // 日本（観察する人）から月への視線（見えないときは点線。地球の後ろにかくれる）
    const th=(180+15*(hour-12))*R, zx=Math.cos(th), zy=Math.sin(th), ex=-Math.sin(th), ey=Math.cos(th);
    const o=toS(RE*zx,RE*zy), l=lamOf(age)*R, mx=-RO*Math.cos(l), my=-RO*Math.sin(l), m=toS(mx,my), vis=(mx*zx+my*zy)>0;
    x.strokeStyle=vis?'rgba(253,230,138,.9)':'rgba(148,163,184,.55)'; x.lineWidth=vis?2:1.5; if(!vis) x.setLineDash([4,4]);
    x.beginPath(); x.moveTo(o[0],o[1]); x.lineTo(m[0],m[1]); x.stroke(); x.setLineDash([]);
    // 地球（左半分が昼）・時刻のめやす・自転の矢印
    phase(LX,LY,RE,90,Math.PI,'#4f9fdc','#173153'); x.strokeStyle='rgba(255,255,255,.35)'; x.lineWidth=1; x.beginPath(); x.arc(LX,LY,RE,0,2*Math.PI); x.stroke();
    x.font=F(10); x.fillStyle='rgba(203,213,225,.8)';
    [['正午',180],['夕方',270],['真夜中',0],['明け方',90]].forEach(d=>{ const s=toS(64*Math.cos(d[1]*R),64*Math.sin(d[1]*R)); x.fillText(d[0],s[0],s[1]); });
    arc(LX,LY,RE+5,112,158,'rgba(255,255,255,.6)');
    // 地平線と東西、日本
    const h1=toS(RE*zx+24*ex,RE*zy+24*ey), h2=toS(RE*zx-24*ex,RE*zy-24*ey);
    x.strokeStyle='#fff'; x.lineWidth=1.6; x.beginPath(); x.moveTo(h1[0],h1[1]); x.lineTo(h2[0],h2[1]); x.stroke();
    const el=toS(RE*zx+31*ex,RE*zy+31*ey), wl=toS(RE*zx-31*ex,RE*zy-31*ey);
    x.font=F(10,1); x.fillStyle='#fff'; x.fillText('東',el[0],el[1]); x.fillText('西',wl[0],wl[1]);
    x.fillStyle='#ef4444'; x.beginPath(); x.arc(o[0],o[1],4.5,0,2*Math.PI); x.fill(); x.strokeStyle='#fff'; x.lineWidth=1.2; x.stroke();
    const nl=toS((RE-11)*zx,(RE-11)*zy); x.font=F(10,1); x.lineWidth=3; x.strokeStyle='#0b1020'; x.strokeText('日本',nl[0],nl[1]); x.fillStyle='#fff'; x.fillText('日本',nl[0],nl[1]);
    // 月（いま）：明るい半分＝太陽側、水色の線＝地球に向いている側
    x.strokeStyle='rgba(125,211,252,.95)'; x.lineWidth=2.5; x.beginPath(); x.arc(m[0],m[1],15,(-lamOf(age)-90)*R,(-lamOf(age)+90)*R,false); x.stroke();
    phase(m[0],m[1],11,90,Math.PI,'#f8f4e3','#3b4660');
    x.textBaseline='alphabetic'; x.textAlign='left'; x.font=F(10.5); x.fillStyle='rgba(203,213,225,.85)';
    x.fillText('地球の自転（地球のまわりの矢印）も月の公転も反時計回り',8,398);
    x.fillText('水色の線＝地球に向いた側（大きさ・距離は誇張）',8,414);
  }
  function drawSky(){
    const sp=altAz(haSun()), sAlt=sp[0], Hm=haMoon(), mp=altAz(Hm), mAlt=mp[0];
    const L=lamOf(age), e=L<=180?L:360-L, vis=Math.abs(Hm)<90, nm=nameOf(age), k=(1-Math.cos(L*R))/2;
    const cols=skyCols(sAlt), g=x.createLinearGradient(0,0,0,HZ); g.addColorStop(0,cols[0]); g.addColorStop(1,cols[1]);
    x.save(); x.beginPath(); x.rect(X0,0,W-X0,HZ); x.clip();
    x.fillStyle=g; x.fillRect(X0,0,W-X0,HZ);
    if(sAlt<-3){ x.fillStyle='rgba(255,255,255,'+Math.min(.75,(-3-sAlt)/10).toFixed(2)+')'; for(let i=0;i<44;i++) x.fillRect(X0+8+(i*67)%(W-X0-16), 52+(i*37)%(HZ-64), 1.4, 1.4); }
    x.setLineDash([3,5]); x.strokeStyle=sAlt>0?'rgba(30,58,95,.45)':'rgba(255,255,255,.35)'; x.lineWidth=1.3; x.beginPath();
    for(let h=-90;h<=90;h+=3){ const q=altAz(h), s=sky(q[0],q[1]); h===-90?x.moveTo(s[0],s[1]):x.lineTo(s[0],s[1]); } x.stroke(); x.setLineDash([]);
    if(sAlt>-2){ const s=sky(sAlt,sp[1]), gl=x.createRadialGradient(s[0],s[1],5,s[0],s[1],40); gl.addColorStop(0,'rgba(255,244,190,.95)'); gl.addColorStop(1,'rgba(255,244,190,0)');
      x.fillStyle=gl; x.beginPath(); x.arc(s[0],s[1],40,0,2*Math.PI); x.fill(); x.fillStyle='#fff6c4'; x.beginPath(); x.arc(s[0],s[1],12,0,2*Math.PI); x.fill(); }
    let below=false, endP=null;
    if(vis&&!isNew(age)){ const dH=L<=180?L:L-360, n=Math.ceil(Math.abs(dH)/2); x.setLineDash([2,5]); x.strokeStyle='rgba(250,204,21,.95)'; x.lineWidth=2; x.beginPath();
      for(let i=0;i<=n;i++){ const q=altAz(Hm+dH*i/n); if(q[0]<0){ below=true; break; } const s=sky(q[0],q[1]); i?x.lineTo(s[0],s[1]):x.moveTo(s[0],s[1]); endP=s; }
      x.stroke(); x.setLineDash([]); }
    if(vis&&!isNew(age)){ const s=sky(mAlt,mp[1]), a1=altAz(Hm-0.5), a2=altAz(Hm+0.5), p1=sky(a1[0],a1[1]), p2=sky(a2[0],a2[1]), sg=L<180?1:-1;
      const th=Math.atan2((p2[1]-p1[1])*sg,(p2[0]-p1[0])*sg);
      if(sAlt<0){ const gl=x.createRadialGradient(s[0],s[1],6,s[0],s[1],42); gl.addColorStop(0,'rgba(255,250,225,'+(0.1+0.3*k).toFixed(2)+')'); gl.addColorStop(1,'rgba(255,250,225,0)'); x.fillStyle=gl; x.beginPath(); x.arc(s[0],s[1],42,0,2*Math.PI); x.fill(); }
      phase(s[0],s[1],14,e,th,sAlt>0?'#f8fafc':'#fbf6e2',sAlt>0?'rgba(120,150,190,.25)':'rgba(60,72,100,.6)'); }
    else if(vis){ const s=sky(mAlt,mp[1]); x.setLineDash([3,3]); x.strokeStyle=sAlt>0?'rgba(30,58,95,.55)':'rgba(255,255,255,.4)'; x.lineWidth=1.2; x.beginPath(); x.arc(s[0],s[1],14,0,2*Math.PI); x.stroke(); x.setLineDash([]);
      x.font=F(10.5,1); x.fillStyle=sAlt>0?'#1e3a5f':'#e2e8f0'; x.textAlign='center'; x.fillText('新月（見えない）',s[0],s[1]+30); }
    x.restore();
    if(below&&endP){ const right=endP[0]>SX0; x.font=F(10.5,1); x.fillStyle='#fde68a'; x.textAlign=right?'right':'left'; x.fillText('この先に太陽（地平線の下）',endP[0]+(right?-6:6),Math.min(endP[1]-8,HZ-8)); }
    x.fillStyle='rgba(6,11,28,.6)'; rr(X0+6,6,W-X0-12,40,8); x.fill();
    x.textAlign='left'; x.fillStyle='#fff'; x.font=F(13,1); x.fillText('日本から見た空（南を向いて）',X0+14,22);
    let st; if(isNew(age)) st='新月のころ：太陽と同じ方向で見えない'; else if(!vis) st='いま月は地平線の下（見えない）'; else st='いま：'+dirName(mp[1])+'の空・高さ'+Math.round(mAlt)+'°'+(sAlt>3?'（昼の空）':sAlt>-8?(hour<12?'（明け方の空）':'（夕方の空）'):'');
    x.font=F(12,1); x.fillStyle='#fde68a'; x.fillText(st,X0+14,39);
    // 地面：方角・月の出／南中／月の入り
    x.fillStyle='#14211a'; x.fillRect(X0,HZ,W-X0,H-HZ);
    x.strokeStyle='rgba(255,255,255,.6)'; x.lineWidth=1.5; x.beginPath(); x.moveTo(X0,HZ); x.lineTo(W,HZ); x.stroke();
    x.font=F(12,1); x.fillStyle='#e2e8f0'; x.textAlign='center';
    [['東',-90],['南東',-45],['南',0],['南西',45],['西',90]].forEach(d=>{ x.fillText(d[0],Math.min(W-10,Math.max(X0+10,SX0+d[1]/90*SXW)),HZ+16); });
    if(!isNew(age)){ const T=transitH(age); x.font=F(11); x.fillStyle='#fde68a';
      x.textAlign='left'; x.fillText('月の出 '+about(T-6),X0+6,HZ+33); x.textAlign='center'; x.fillText('南中 '+about(T),SX0,HZ+33); x.textAlign='right'; x.fillText('月の入り '+aboutSet(T+6),W-6,HZ+33); }
    x.strokeStyle='rgba(255,255,255,.12)'; x.lineWidth=1; x.beginPath(); x.moveTo(X0+6,HZ+42); x.lineTo(W-6,HZ+42); x.stroke();
    // 月の形（南の空で見たとき）と説明
    const cx=X0+46, cy=HZ+90;
    phase(cx,cy,27,e,L<180?0:Math.PI,'#fbf6e2','#2a3350'); x.strokeStyle='rgba(255,255,255,.35)'; x.lineWidth=1; x.beginPath(); x.arc(cx,cy,27,0,2*Math.PI); x.stroke();
    x.font=F(10); x.fillStyle='rgba(203,213,225,.8)'; x.textAlign='center'; x.fillText('南の空での形',cx,cy+43);
    const tx=X0+90; x.textAlign='left'; x.fillStyle='#fff'; x.font=F(nm[0].length>5?16:19,1); x.fillText(nm[0],tx,HZ+70);
    x.font=F(11.5); x.fillStyle='#e2e8f0'; x.fillText(nm[1],tx,HZ+89); x.fillText('月齢 '+age.toFixed(1)+'日・光る部分 '+Math.round(k*100)+'%',tx,HZ+107);
    const dw=darkWin(age); x.fillStyle='#fde68a'; x.fillText(dw?'暗い空で見える：'+dw+'ごろ':'暗い空ではほとんど見えない',tx,HZ+125);
    if(todayTxt){ x.fillStyle='#93c5fd'; x.font=F(10.5); x.fillText(todayTxt,tx,HZ+143); }
  }
  function draw(){
    x.clearRect(0,0,W,H); drawSpace(); drawSky();
    x.strokeStyle='rgba(255,255,255,.15)'; x.lineWidth=1; x.beginPath(); x.moveTo(X0-1,0); x.lineTo(X0-1,H); x.stroke();
    const nm=nameOf(age), T=transitH(age);
    setStat('sAge',age.toFixed(1)+'日'); setStat('sName',nm[0]); $('sName').style.fontSize=nm[0].length>5?'15px':'';
    setStat('sWin',upWin(age)); setStat('sTr',about(T));
    setShare('【月の満ち欠け】月齢'+age.toFixed(1)+'日は「'+nm[0]+'」🌙 '+(isNew(age)?'太陽と同じ方向にあって見えません':about(T-6)+'に東からのぼり、'+about(T)+'に南の空、'+aboutSet(T+6)+'に西にしずみます（目安）')+'｜シミュラボ');
  }
  function syncUI(){ $('age').value=age.toFixed(1); $('ageL').textContent=age.toFixed(1)+'日'; $('hour').value=String(Math.round(hour*2)/2); $('hourL').textContent=hm(hour)+'（'+word(hour)+'）'; }
  function frame(ts){ const dt=last?Math.min(0.1,(ts-last)/1000):0; last=ts;
    if(play){ hour+=dt*2; age=wrap(age+dt*2/24,SYN); if(hour>=24) hour-=24; syncUI(); need=true; }
    if(need){ need=false; draw(); }
    requestAnimationFrame(frame); }
  function pos(e){ const q=cpos(cv,e); return [q[0]/dpr,q[1]/dpr]; }
  function move(q){
    if(drag==='moon'){ const a=Math.atan2(LY-q[1],q[0]-LX)/R; age=wrap(a-180,360)/360*SYN; todayTxt=''; $('preset').value=''; }
    else if(drag==='obs'){ const a=Math.atan2(LY-q[1],q[0]-LX)/R; hour=wrap(12+(a-180)/15,24); }
    else if(drag==='sky'){ const A=clamp((q[0]-SX0)/SXW*90,-89,89), h=Math.atan(Math.tan(A*R)*Math.sin(LAT))/R; hour=wrap(transitH(age)+h/15,24); }
    syncUI(); draw(); }
  cv.addEventListener('pointerdown',e=>{ const q=pos(e);
    if(q[0]<X0-2) drag=Math.hypot(q[0]-LX,q[1]-LY)<RE+16?'obs':'moon'; else drag=q[1]<HZ?'sky':null;
    if(drag){ try{ cv.setPointerCapture(e.pointerId); }catch(_){ } move(q); } });
  cv.addEventListener('pointermove',e=>{ if(drag) move(pos(e)); });
  ['pointerup','pointercancel'].forEach(n=>cv.addEventListener(n,()=>{ drag=null; }));
  $('age').addEventListener('input',()=>{ age=+$('age').value; todayTxt=''; $('preset').value=''; syncUI(); draw(); });
  $('hour').addEventListener('input',()=>{ hour=(+$('hour').value)%24; syncUI(); draw(); });
  $('preset').addEventListener('change',()=>{ const v=$('preset').value; if(v!==''){ age=+v; todayTxt=''; syncUI(); draw(); } });
  $('today').addEventListener('click',()=>{ const d=new Date(); d.setHours(Math.floor(hour),Math.round((hour%1)*60),0,0); age=wrap((d.getTime()-EPOCH)/864e5,SYN);
    todayTxt=(d.getMonth()+1)+'/'+d.getDate()+' '+hm(hour)+'の月齢（目安）'; $('preset').value=''; syncUI(); draw(); });
  $('play').addEventListener('click',()=>{ play=!play; if(play) todayTxt=''; $('play').textContent=play?'⏸ 止める':'▶ 時刻を進める'; });
  $('plus1').addEventListener('click',()=>{ age=wrap(age+1,SYN); todayTxt=''; $('preset').value=''; syncUI(); draw(); });
  syncUI(); draw(); need=false; requestAnimationFrame(frame);
''')

# ============================================================ 2 月食・日食
sim(slug="gesshoku-nisshoku", cat="rika", emoji="🌘", score=80,
    title="月食・日食シミュレーター（起こるしくみと、毎月は起きない理由）",
    title_tag="月食・日食の仕組みシミュレーター｜なぜ毎月起きない？影と月の通り道の傾き",
    meta_desc="月食・日食はなぜ起こる？太陽・地球・月が一直線に並んだときの影の落ち方を、宇宙から見た図と地上から見た様子で再現。月の通り道が約5°傾いているため毎月は起きないことも、ずれを動かして確かめられる無料シミュレーター。次に日本で見られる月食・日食の日付も紹介。",
    og_title="月食・日食シミュレーター",
    og_desc="月の通り道のずれを動かすと、皆既月食・部分月食・皆既日食・金環日食が起きたり起きなかったり。毎月は起きない理由がわかる。",
    card_desc="月の通り道のずれを動かすと、皆既月食・部分月食・金環日食が起きたり起きなかったり。毎月は起きない理由がわかる。",
    lead="月食は満月のころ、月が地球の影に入る現象。日食は新月のころ、月の影が地球に落ちる現象です。満月・新月の前後の時間と、月の通り道のずれを動かして、食が起こる条件を確かめてください。",
    model="小6 月と太陽（発展）／中3 月や金星の運動と見え方（日食・月食）",
    level="小学6年、中学3年",
    unit="中学校 第2分野（6）地球と宇宙（月や金星の運動と見え方。内容の取扱いで日食・月食にも触れる）／小学校 第6学年 B(5)「月と太陽」の発展",
    canvas=canvas(640, 460),
    controls=select("side", "見るとき", [("full", "満月のころ（月食）"), ("new", "新月のころ（日食）")]) + slider("t", "月齢", -5, 5, 0, 0.1)
           + slider("beta", "月の通り道のずれ", -5.15, 5.15, 0.3, 0.05)
           + select("dist", "月までの距離", [("mean", "平均（約38万km）"), ("near", "近いとき（約36万km）"), ("far", "遠いとき（約41万km）")]),
    buttons=btn("play", "▶ 食の進み方を再生", True) + btn("zero", "一直線にそろえる（ずれ0）") + btn("year", "📅 1年分を試す"),
    stats=stats([("sType", "この食の種類", True), ("sMag", "最大の食分", False), ("sNow", "いまの様子", False), ("sDur", "続く時間（目安）", False)]),
    legend="上：横から見た太陽・地球・月と影（大きさの比はほぼ実際どおり、距離と月の通り道の傾きは誇張）。左下：地上から見た様子（東が左）。右下：ずれの大きさと食が起こる範囲、1年分の結果（赤＝皆既、オレンジ＝部分・輪は金環、灰色＝半影、白い輪＝起きない）。図を指でドラッグしても動かせます。",
    article='''
<h2>このシミュレーションでわかること</h2>
<p><b>月食</b>は、満月のころに太陽・地球・月がこの順に一直線に並び、月が地球の影に入る現象です。<b>日食</b>は、新月のころに太陽・月・地球がこの順に並び、月が太陽をかくす（月の影が地球に落ちる）現象です。</p>
<p>月の通り道は、地球の公転面（太陽と地球を通る面）に対して約5°かたむいています。そのため、ふだんの満月・新月では月が影の上か下を通り、食は毎月は起こりません。このシミュレーターでは、満月・新月のときの月の上下の「ずれ」を動かして、食が起こる条件を確かめられます。</p>
''' + T([[NW("中学校3年"), "第2分野（6）地球と宇宙「月や金星の運動と見え方」", "内容の取扱いに「日食や月食にも触れること」とある"],
          [NW("小学校6年"), NW("B(5) 月と太陽（発展）"), "月の形の見え方と、太陽と月の位置関係を学んだあとの発展として"]], ["学年", "単元", "扱い"]) + '''
<p>月の通り道の傾き（約5°）や食の種類のくわしい区別は、学習指導要領の範囲をこえる発展的な内容です。</p>

<h2>授業での使い方</h2>
<p><b>導入</b>：「満月は毎月あるのに、月食がめったに起きないのはなぜ？」と問いかけ、予想を出させます。そのあと「一直線にそろえる（ずれ0）」を押し、ずれがなければ満月のたびに月食が起こることを確かめます。</p>
<p><b>展開</b>：「月の通り道のずれ」を少しずつ大きくして、皆既月食→部分月食→半影月食→起きない、と変わる境目を記録させます。「新月のころ（日食）」に切り替えて同じことをし、「月までの距離」を変えて皆既日食と金環日食のちがいも確かめます。</p>
<p><b>まとめ</b>：「1年分を試す」で、12か月分の新月・満月のうち何回食が起きたかを数えます。食は年に2回ほどの時期にまとまって起こることに気づかせます。</p>
<p>児童・生徒への問いの例です。</p>
<ul>
<li>月食が起こるのは、月がどんな形のときでしょう。それはなぜでしょう。（満月。太陽・地球・月の順に並ぶと、月は太陽と反対側にあるから）</li>
<li>皆既月食の月が真っ黒にならず、赤黒く見えるのはなぜでしょう。（地球の大気を通った赤い光が曲げられて、影の中の月を照らすから）</li>
<li>皆既日食と金環日食のちがいは、何で決まるでしょう。（月までの距離。近いと月が太陽より大きく見えて皆既日食、遠いと小さく見えて金環日食）</li>
</ul>

<h2>しくみ・解説</h2>
<h3>月食と日食のちがい</h3>
''' + T([[NW("並び方"), "太陽－地球－月", "太陽－月－地球"], [NW("月の形"), "満月のころ", "新月のころ"], [NW("何の影？"), "地球の影に月が入る", "月の影が地球に落ちる"],
          [NW("見られる場所"), "月が見える場所なら、どこでも同じように見える", "月の影が通る、限られた場所だけ"],
          [NW("種類"), "皆既月食・部分月食・半影月食", "皆既日食・金環日食・部分日食"],
          [NW("続く時間"), "欠け始めから終わりまで長いと4時間近く。皆既は長いと1時間40分ほど", "1か所で部分食が2〜3時間ほど。皆既・金環は数分"]], ["", "月食", "日食"]) + '''
<p>「食分」は、月（日食では太陽）の直径のどれだけが欠けたかを表す数です。月食で1以上なら皆既月食です。</p>
<h3>なぜ毎月は起きない？（月の通り道の傾き）</h3>
<p>月の通り道は、地球の公転面に対して約5.1°かたむいています。満月・新月のときに、月が公転面の近く（通り道が公転面と交わる「交点」の近く）にいるときだけ食が起こります。食が起こる「ずれ」の大きさは次のとおりです（月までの距離が平均のとき）。</p>
''' + T([["皆既月食", "約0.44°以内"], ["部分月食（本影に入る月食）", "約0.96°以内"], ["半影月食（目ではほとんど気づかない）", "約1.49°以内"],
          ["日食（地球のどこかで部分日食）", "約1.47°以内"], ["皆既日食・金環日食（地球のどこかで）", "約0.95°以内"], ["起きない", "それより大きいとき（最大で約5.1°）"]],
         ["起こる食", "満月・新月のときの上下のずれ"]) + '''
<p>月の直径は約0.5°なので、ずれが「月3個分」より大きいと食は起こりません。交点の近くで満月・新月になる時期は約半年ごとにめぐってくるので、食は年に2回ほどの時期にまとまって起こります。国立天文台の暦Wikiでは、満月が交点の両側約17°以内なら半影月食、約11°以内なら部分月食、約6°以内なら皆既月食が起こるとされています。</p>
<h3>影の大きさと、太陽・月の見かけの大きさ</h3>
<p>月の位置での地球の本影（こい影）は、月の直径の約2.7倍（月までの距離によって約2.6〜2.8倍）の大きさです。月はこの影の中を1時間に月の直径くらいずつ進みます。2026年3月3日の皆既月食では、部分食の始まりが18時50分、皆既が20時04分〜21時03分、部分食の終わりが22時18分でした（国立天文台）。</p>
<p>太陽の直径は月の約400倍ですが、地球からの距離も約390倍遠いので、空では太陽と月がほぼ同じ大きさ（約0.5°）に見えます。月までの距離は約36万〜41万kmの間で変わるので、近いときは月が太陽より大きく見えて皆既日食に、遠いときは小さく見えて金環日食になります。</p>
''' + T([["近いとき（約36万km）", "約0.56°", "太陽より大きい → 皆既日食"], ["平均（約38万km）", "約0.52°", "太陽よりわずかに小さい → 金環日食"],
          ["遠いとき（約41万km）", "約0.49°", "太陽より小さい → 金環日食"], ["太陽（平均）", "約0.53°", "（くらべる基準）"]],
         ["月までの距離", "月の見かけの直径", "中心が重なったときの日食"]) + '''
<h3>皆既月食の月が赤く見えるわけ</h3>
<p>地球には大気があります。太陽の光が大気を通るとき、青い光は散らばって通りにくく、赤い光は通りぬけやすいうえ、大気がレンズのように光を曲げて本影の内側に届けます。このかすかな赤い光が月を照らすので、皆既食中の月は赤銅色（しゃくどういろ）に見えます（国立天文台「月食とは」より要約）。</p>
<h3>次に日本で見られる月食・日食（国立天文台による）</h3>
''' + T([[NW("2028年7月7日"), NW("部分月食"), "日本で見られる（欠けたまま月がしずむ「月入帯食」）", "国立天文台「月食一覧」"],
          [NW("2029年1月1日"), NW("皆既月食"), "日本全国で見られる（0時7分に欠け始める）", "国立天文台「皆既月食（2026年3月）」"],
          [NW("2030年6月1日"), NW("金環日食"), "北海道の大部分で金環食、全国で部分食", "国立天文台「2023年4月20日 日食 解説資料」"],
          [NW("2035年9月2日"), NW("皆既日食"), "日本で皆既日食（中心食）が見られる", "国立天文台「日食一覧」"]], ["日付", "種類", "日本での見え方", "出典"]) + '''
<p>2026年10月4日に国立天文台のページで確認しました。日付は食が最大になるときの日本時間です。国立天文台の月食一覧には半影月食は載っていません。地域ごとの時刻や見え方は、国立天文台暦計算室の「月食各地予報」「日食各地予報」で調べられます。</p>
<h3>日食を観察するときの注意</h3>
''' + N("太陽を肉眼で直接見てはいけません（数秒でも目を痛めます）。色つきの下じき、サングラス、すすを付けたガラスなども危険です。日食グラスを正しく使う、ピンホール（小さな穴）で太陽の像を映す、望遠鏡の太陽投影板に映す、などの方法で観察してください（国立天文台「観察のしかた」より）。") + '''
<h3>このシミュレーションで単純化していること</h3>
<ul>
<li>上の図は、太陽・地球・月の大きさの比をほぼ実際どおりにし、距離と月の通り道の傾きを誇張しています。実際の月までの距離は地球の直径の約30倍です。</li>
<li>「ずれ」は、満月・新月の瞬間に月が地球の公転面からどれだけ上下にはなれているかを、地球の中心から見た角度で表したものです。影を横切る間に通り道がわずかに傾く効果は省いています。</li>
<li>影の大きさ、食が起こる条件、食分、続く時間は、J. Meeus『Astronomical Algorithms』の食の計算式（大気による影の広がりをふくむ）で計算しています。この条件で、国立天文台の月食一覧・日食一覧に載っている2025〜2030年の月食10回・日食14回の種類（皆既・部分・金環）を判定すると、すべて一致しました（半影月食は一覧に載っていないため除いています）。</li>
<li>日食の「地上から見た様子」は、月の影の中心にいちばん近い場所から見た場合です。実際の見え方や続く時間は場所によってちがいます。</li>
<li>「1年分を試す」は、満月・新月のたびに月の通り道の向きが太陽に対して約31°ずつずれていくとして計算しています。</li>
</ul>

<h2>参考</h2>
<ul class="seo-refs">
<li>国立天文台「月食とは」（''' + A("https://www.nao.ac.jp/astro/basic/lunar-eclipse.html") + '''）</li>
<li>国立天文台「日食とは」（''' + A("https://www.nao.ac.jp/astro/basic/solar-eclipse.html") + '''）</li>
<li>国立天文台「月食一覧」（''' + A("https://www.nao.ac.jp/astro/basic/lunar-eclipse-list.html") + '''）</li>
<li>国立天文台「日食一覧」（''' + A("https://www.nao.ac.jp/astro/basic/solar-eclipse-list.html") + '''）</li>
<li>国立天文台「皆既月食（2026年3月）」（''' + A("https://www.nao.ac.jp/astro/sky/2026/03-topics02.html") + '''）</li>
<li>国立天文台「2023年4月20日 日食（金環皆既日食）解説資料」（''' + A("https://www.nao.ac.jp/contents/astro/sky/2023/04/partial-eclipse-factsheet.pdf") + '''）</li>
<li>国立天文台「日食 観察のしかた」（''' + A("https://www.nao.ac.jp/astro/basic/solar-eclipse-obs.html") + '''）</li>
<li>国立天文台 暦計算室「暦Wiki 月食の条件」（''' + A("https://eco.mtk.nao.ac.jp/koyomi/wiki/B7EEBFA92FBEF2B7EF.html") + '''）</li>
<li>文部科学省「中学校学習指導要領（平成29年告示）」理科（''' + A("https://www.mext.go.jp/a_menu/shotou/new-cs/1384661.htm") + '''）</li>
<li>Jean Meeus『Astronomical Algorithms』第2版（Willmann-Bell, 1998）</li>
</ul>
''',
    faqs=[("満月のたびに月食が起きないのはなぜですか？", "月の通り道が、地球の公転面に対して約5°かたむいているからです。ふだんの満月は、地球の影の上か下を通ります。満月が、通り道と公転面の交わる点（交点）の近くで起こるときだけ、月食になります。"),
          ("皆既月食で月が赤く見えるのはなぜですか？", "地球の大気を通った太陽の光のうち、赤い光が曲げられて地球の影の中に届き、月を照らすからです。大気中のちりの量によって、明るいオレンジ色から黒っぽい色まで変わります。"),
          ("皆既日食と金環日食は何がちがうのですか？", "月までの距離のちがいです。月が近いと太陽より大きく見えて太陽を全部かくし（皆既日食）、遠いと小さく見えて太陽がリングのようにはみ出します（金環日食）。"),
          ("日食と月食はどちらが多いのですか？", "地球全体で数えると、半影月食もふくめればほぼ同じ回数で、どちらも平均すると年に2回あまりです。ただし日食は見られる場所が限られるので、決まった場所で見られる回数は月食のほうが多くなります（国立天文台 暦Wikiより）。"),
          ("次に日本で見られる月食・日食はいつですか？", "国立天文台によると、月食は2028年7月7日の部分月食、日本全国で見られる皆既月食は2029年1月1日です。日食は2030年6月1日の金環日食（北海道の大部分で金環食、全国で部分食）です。"),
          ("日食はどうやって観察すればよいですか？", "太陽を肉眼で直接見たり、下じきやサングラスで見たりしてはいけません。日食グラスを正しく使う、ピンホールで太陽の像を映すなど、安全な方法で観察してください。")],
    rel=[("tsuki-michikake", "🌓", "月の満ち欠けの仕組みシミュレーター"), ("kyou-no-tsuki", "🌙", "今日の月（月齢・満ち欠け・次の満月はいつ？）"),
         ("solar-system", "🪐", "太陽系シミュレーター"), ("hoshizora-shisu", "🔭", "今夜の星空指数"), ("gravity", "🌌", "重力シミュレーター")],
    js=r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const x=cv.getContext('2d'); x.setTransform(dpr,0,0,dpr,0,0);
  cv.style.cursor='pointer';
  const R=Math.PI/180, INC=5.145, KM=0.2725, SUN=0.2666, VS=0.40;   // 月の半径（地球半径単位）、太陽の見かけの半径（度）、日食時の見かけの速さ（度/時）
  const DIST={mean:{km:384400,u:0.0059,n:0.5458}, near:{km:356500,u:-0.0123,n:0.5858}, far:{km:406700,u:0.0241,n:0.5058}};   // u：本影円錐の半径、n：影に対する月の速さ（地球半径/時）
  const F=(s,b)=>(b?'bold ':'')+s+'px system-ui,-apple-system,"Hiragino Sans","Noto Sans JP",sans-serif';
  const Y0=128, XE=420, ER=30, RO=150, TOP=228, GC=159, GY=356, CLL=66, CLS=56, SCL=42, SCS=84;   // SCL：月食の図の地球半径1つ分(px)、SCS：日食の図の1°(px)
  let side=$('side').value, t=+$('t').value, beta=+$('beta').value, play=false, hold=0, yr=null, last=0, need=true, drag=null;
  function prm(){ const d=DIST[$('dist').value]||DIST.mean; return {pi:Math.asin(6378.14/d.km)/R, sm:Math.asin(1737.4/d.km)/R, u:d.u, n:d.n}; }
  function lunar(g,p){ const a=Math.abs(g), lt=0.4678-p.u, lp=1.0128-p.u, lh=1.5573+p.u, sd=(L)=>L>a?60/p.n*Math.sqrt(L*L-a*a):0;
    return {type:a<lt?'皆既月食':a<lp?'部分月食':a<lh?'半影月食':'', magU:(lp-a)/0.545, magP:(lh-a)/0.545, tot:2*sd(lt), par:2*sd(lp), pen:2*sd(lh)}; }
  function solar(g,p){ const a=Math.abs(g), cen=a<0.9972, d=cen?0:(a-0.9972)*p.pi, rs=SUN+p.sm;   // d：影の中心にいちばん近い場所での太陽と月の中心のはなれ（度）
    return {type:cen?(p.sm>=SUN?'皆既日食':'金環日食'):a<1.5433+p.u?'部分日食':'', d:d, mag:cen?p.sm/SUN:Math.max(0,(rs-d)/(2*SUN)),
      par:rs>d?2*Math.sqrt(rs*rs-d*d)/VS*60:0, cen:cen?2*Math.abs(p.sm-SUN)/VS*60:0}; }
  function nowSt(p,g){
    if(side==='full'){ const dd=Math.hypot(-p.n*t,g), sg=0.7403-p.u, rh=1.2848+p.u;
      if(dd<=sg-KM) return ['皆既食中（赤銅色）',3];
      if(dd<sg+KM) return ['部分食中（食分'+((sg+KM-dd)/(2*KM)).toFixed(2)+'）',2];
      if(dd<rh+KM) return ['半影食中（少し暗い）',1];
      return ['欠けていない',0]; }
    const S=solar(g,p), dd=Math.hypot(-VS*t,S.d);
    if(S.type&&S.type!=='部分日食'&&dd<Math.abs(p.sm-SUN)) return [p.sm>=SUN?'皆既食中':'金環食中',3];
    if(S.type&&dd<SUN+p.sm) return ['部分食中（食分'+((SUN+p.sm-dd)/(2*SUN)).toFixed(2)+'）',2];
    return ['欠けていない',0]; }
  const hp=(g)=>{ const a=Math.abs(g); return Math.sign(g)*(a<=1.7?a*ER:51+(a-1.7)*(13/4.1)); };     // 地球半径→図の高さ（1.7より外はちぢめる）
  const hpInv=(h)=>{ const a=Math.abs(h); return Math.sign(h)*(a<=51?a/ER:1.7+(a-51)*(4.1/13)); };
  const circ=(cx,cy,r)=>{ x.beginPath(); x.arc(cx,cy,r,0,2*Math.PI); };
  function lerp(c1,c2,f){ const q=(s)=>[1,3,5].map(i=>parseInt(s.slice(i,i+2),16)); const a=q(c1), b=q(c2); return 'rgb('+a.map((v,i)=>Math.round(v+(b[i]-v)*f)).join(',')+')'; }
  function rr(a,b,w,h,r){ x.beginPath(); x.moveTo(a+r,b); x.arcTo(a+w,b,a+w,b+h,r); x.arcTo(a+w,b+h,a,b+h,r); x.arcTo(a,b+h,a,b,r); x.arcTo(a,b,a+w,b,r); x.closePath(); }
  function phase(cx,cy,r,e,th,lit,dark){
    x.save(); x.translate(cx,cy); x.rotate(th);
    if(dark){ x.fillStyle=dark; circ(0,0,r); x.fill(); }
    if(e>0.5){ const a=r*Math.cos(e*R); x.fillStyle=lit; x.beginPath(); x.arc(0,0,r,-Math.PI/2,Math.PI/2,false); x.ellipse(0,0,Math.abs(a),r,0,Math.PI/2,-Math.PI/2,a>0); x.closePath(); x.fill(); }
    x.restore(); }
  function overlapA(x1,y1,r1,x2,y2,r2){ const d=Math.hypot(x2-x1,y2-y1); if(d>=r1+r2) return 0; if(d<=Math.abs(r1-r2)) return Math.PI*Math.min(r1,r2)*Math.min(r1,r2);
    const a=r1*r1*Math.acos((d*d+r1*r1-r2*r2)/(2*d*r1)), b=r2*r2*Math.acos((d*d+r2*r2-r1*r1)/(2*d*r2)), c=0.5*Math.sqrt((-d+r1+r2)*(d+r1-r2)*(d-r1+r2)*(d+r1+r2)); return a+b-c; }
  function drawSide(p,g,L,S){
    x.fillStyle='#0b1020'; x.fillRect(0,0,W,TOP);
    const sg=x.createRadialGradient(-270,Y0,170,-270,Y0,300); sg.addColorStop(0,'#fff1b8'); sg.addColorStop(1,'#f59e0b'); x.fillStyle=sg; circ(-270,Y0,300); x.fill();
    x.textAlign='left'; x.fillStyle='#7c2d12'; x.font=F(12,1); x.fillText('太陽',2,Y0+48);
    x.setLineDash([4,6]); x.strokeStyle='rgba(255,255,255,.22)'; x.lineWidth=1; x.beginPath(); x.moveTo(34,Y0); x.lineTo(W,Y0); x.stroke(); x.setLineDash([]);
    x.fillStyle='rgba(203,213,225,.7)'; x.font=F(10.5); x.fillText('地球の公転面',40,Y0-7);
    // 新月・満月の位置
    x.setLineDash([2,4]); x.strokeStyle='rgba(203,213,225,.18)'; x.beginPath(); x.moveTo(XE-RO,60); x.lineTo(XE-RO,200); x.moveTo(XE+RO,60); x.lineTo(XE+RO,200); x.stroke(); x.setLineDash([]);
    x.font=F(10.5,1); x.fillStyle='rgba(226,232,240,.85)'; x.textAlign='center'; x.fillText('新月の位置',XE-RO,54); x.fillText('満月の位置',XE+RO,54);
    // 地球の影（半影・本影）
    const sgm=0.7403-p.u, rho=1.2848+p.u, pe=(xx)=>ER+(rho-1)*ER*(xx-XE)/RO, um=(xx)=>ER-(1-sgm)*ER*(xx-XE)/RO;
    const penPath=()=>{ x.beginPath(); x.moveTo(XE,Y0-ER); x.lineTo(W,Y0-pe(W)); x.lineTo(W,Y0+pe(W)); x.lineTo(XE,Y0+ER); x.closePath(); };
    const umPath=()=>{ x.beginPath(); x.moveTo(XE,Y0-ER); x.lineTo(W,Y0-um(W)); x.lineTo(W,Y0+um(W)); x.lineTo(XE,Y0+ER); x.closePath(); };
    x.globalAlpha=side==='full'?1:0.45; x.fillStyle='rgba(148,163,184,.16)'; penPath(); x.fill(); x.fillStyle='rgba(2,6,23,.9)'; umPath(); x.fill(); x.strokeStyle='rgba(148,163,184,.35)'; x.lineWidth=1; x.stroke();
    x.font=F(10); x.fillStyle='rgba(203,213,225,.75)'; x.textAlign='center'; x.fillText('本影',505,Y0+4); x.fillText('半影',612,Y0-pe(612)+11); x.globalAlpha=1;
    // 月の通り道（傾いた円を横から見た形。傾きは誇張）
    const hn=(side==='new'?1:-1)*hp(g), pN=[XE-RO,Y0-hn], pF=[XE+RO,Y0+hn], mr=KM*ER;
    x.setLineDash([5,5]); x.strokeStyle='rgba(203,213,225,.5)'; x.lineWidth=1.2; x.beginPath(); x.ellipse(XE,Y0,Math.hypot(RO,hn),12,Math.atan2(hn,RO),0,2*Math.PI); x.stroke(); x.setLineDash([]);
    // 月の影（新月のとき）
    if(side==='new'){ const xm=pN[0], ym=pN[1], pr=(0.5461+p.u)*ER, dy=ym-Y0;
      x.fillStyle='rgba(148,163,184,.22)'; x.beginPath(); x.moveTo(xm,ym-mr); x.lineTo(XE,ym-pr); x.lineTo(XE,ym+pr); x.lineTo(xm,ym+mr); x.closePath(); x.fill();
      const surf=Math.abs(dy)<ER?XE-Math.sqrt(ER*ER-dy*dy):XE-4, tip=p.sm>=SUN?surf+4:surf-(8+p.u*600);
      x.fillStyle='rgba(2,6,23,.95)'; x.beginPath(); x.moveTo(xm,ym-mr); x.lineTo(tip,ym); x.lineTo(xm,ym+mr); x.closePath(); x.fill(); }
    // 地球（左半分が昼）
    phase(XE,Y0,ER,90,Math.PI,'#4f9fdc','#173153'); x.strokeStyle='rgba(255,255,255,.35)'; x.lineWidth=1; circ(XE,Y0,ER); x.stroke();
    if(side==='new'){ const ym=pN[1], pr=(0.5461+p.u)*ER, dy=ym-Y0; x.save(); circ(XE,Y0,ER); x.clip(); x.fillStyle='rgba(2,6,23,.45)'; x.fillRect(XE-ER,ym-pr,ER,2*pr);
      if(Math.abs(dy)<ER){ x.fillStyle='#020617'; circ(XE-Math.sqrt(ER*ER-dy*dy)+2,ym,3); x.fill(); } x.restore(); }
    x.font=F(11,1); x.fillStyle='#e2e8f0'; x.textAlign='center'; x.fillText('地球',XE,Y0+ER+15);
    // 月
    const sel=side==='new'?pN:pF, oth=side==='new'?pF:pN;
    x.setLineDash([2,3]); x.strokeStyle='rgba(203,213,225,.45)'; x.lineWidth=1; circ(oth[0],oth[1],mr); x.stroke(); x.setLineDash([]);
    x.save(); circ(sel[0],sel[1],mr); x.clip(); phase(sel[0],sel[1],mr,90,Math.PI,'#f8f4e3','#3b4660');
    if(side==='full'){ x.fillStyle='rgba(10,12,25,.4)'; penPath(); x.fill(); x.fillStyle='rgba(150,52,22,.96)'; umPath(); x.fill(); }
    x.restore(); x.strokeStyle='rgba(255,255,255,.55)'; circ(sel[0],sel[1],mr+0.5); x.stroke();
    // 見出しと結論
    x.textAlign='left'; x.fillStyle='#fff'; x.font=F(13,1); x.fillText('宇宙から見た図（横から・満月／新月の瞬間）',18,20);
    x.font=F(10.5); x.fillStyle='rgba(203,213,225,.75)'; x.fillText('大きさの比はほぼ実際どおり。距離と通り道の傾きは誇張',18,36);
    x.textAlign='right'; x.fillText('点線の楕円＝月の通り道',W-8,20);
    let cap, hit;
    if(side==='full'){ hit=!!L.type; cap=hit?('満月が地球の'+(L.type==='皆既月食'?'本影にすっぽり入る':L.type==='部分月食'?'本影に一部入る':'半影だけに入る')+' → '+L.type):('満月は地球の影の'+(g>0?'上':'下')+'を通る → 月食は起きない'); }
    else { hit=!!S.type; cap=hit?('月の影が地球に'+(S.type==='部分日食'?'少しかかる（うすい影だけ）':'とどく')+' → '+S.type):('月の影は地球の'+(g>0?'上':'下')+'にそれる → 日食は起きない'); }
    x.font=F(13,1); x.fillStyle=hit?'#fca5a5':'#cbd5e1'; x.fillText(cap,W-8,TOP-10);
  }
  function drawGround(p,g,S,st){
    const GW=318; x.save(); x.beginPath(); x.rect(0,TOP,GW,H-TOP); x.clip();
    if(side==='full'){
      x.fillStyle='#070c1d'; x.fillRect(0,TOP,GW,H-TOP); x.fillStyle='rgba(255,255,255,.5)'; for(let i=0;i<30;i++) x.fillRect((i*71)%GW,TOP+48+(i*43)%(H-TOP-60),1.2,1.2);
      const sg=(0.7403-p.u)*SCL, rh=(1.2848+p.u)*SCL, mr=KM*SCL;
      const gr=x.createRadialGradient(GC,GY,sg,GC,GY,rh); gr.addColorStop(0,'rgba(148,163,184,.22)'); gr.addColorStop(1,'rgba(148,163,184,.04)');
      x.fillStyle=gr; circ(GC,GY,rh); x.fill(); x.setLineDash([4,4]); x.strokeStyle='rgba(203,213,225,.45)'; x.lineWidth=1; x.stroke(); x.setLineDash([]);
      x.fillStyle='rgba(30,41,59,.55)'; circ(GC,GY,sg); x.fill(); x.strokeStyle='rgba(203,213,225,.6)'; x.stroke();
      x.font=F(10); x.fillStyle='rgba(203,213,225,.8)'; x.textAlign='center'; x.fillText('本影',GC,GY+sg-7); x.fillText('半影',GC,GY+rh-6);
      let my=GY-g*SCL, off=false; if(Math.abs(g*SCL)>CLL){ my=GY-Math.sign(g)*CLL; off=true; }
      const mx=GC-p.n*t*SCL;
      x.setLineDash([3,4]); x.strokeStyle='rgba(250,204,21,.4)'; x.beginPath(); x.moveTo(8,my); x.lineTo(GW-8,my); x.stroke(); x.setLineDash([]);
      x.fillStyle='rgba(250,204,21,.75)'; x.beginPath(); x.moveTo(8,my); x.lineTo(17,my-4.5); x.lineTo(17,my+4.5); x.closePath(); x.fill();
      x.save(); circ(mx,my,mr); x.clip(); x.fillStyle='#efe9d3'; x.fillRect(mx-mr,my-mr,2*mr,2*mr);
      const g2=x.createRadialGradient(GC,GY,sg,GC,GY,rh); g2.addColorStop(0,'rgba(10,12,25,.55)'); g2.addColorStop(1,'rgba(10,12,25,0)'); x.fillStyle=g2; circ(GC,GY,rh); x.fill();
      const g3=x.createRadialGradient(GC,GY,0,GC,GY,sg); g3.addColorStop(0,'rgba(105,30,12,.97)'); g3.addColorStop(1,'rgba(168,68,30,.95)'); x.fillStyle=g3; circ(GC,GY,sg); x.fill();
      x.restore();
      if(off){ const rt=mx>GC; x.font=F(10.5,1); x.fillStyle='#fde68a'; x.textAlign=rt?'right':'left'; x.fillText('実際はもっと'+(g>0?'上':'下')+'を通る',mx+(rt?-mr-6:mr+6),my+4); }
    } else {
      const sr=SUN*SCS, mr=p.sm*SCS; let mo=Math.sign(g)*S.d*SCS, off=false; if(Math.abs(mo)>CLS){ mo=Math.sign(g)*CLS; off=true; }
      const mx=GC-VS*t*SCS, my=GY-mo, cov=overlapA(GC,GY,sr,mx,my,mr)/(Math.PI*sr*sr), tot=mr>=sr&&Math.hypot(mx-GC,my-GY)<=mr-sr+0.01;
      const b=tot?0.05:1-0.6*Math.pow(cov,3);
      x.fillStyle=lerp('#0a1226','#5aa7e0',b); x.fillRect(0,TOP,GW,H-TOP);
      if(tot){ x.fillStyle='rgba(255,255,255,.7)'; for(let i=0;i<14;i++) x.fillRect((i*83)%GW,TOP+50+(i*47)%(H-TOP-70),1.4,1.4);
        const co=x.createRadialGradient(GC,GY,sr,GC,GY,sr*3.2); co.addColorStop(0,'rgba(255,255,255,.85)'); co.addColorStop(1,'rgba(255,255,255,0)'); x.fillStyle=co; circ(GC,GY,sr*3.2); x.fill(); }
      else { const gl=x.createRadialGradient(GC,GY,sr,GC,GY,sr*2.6); gl.addColorStop(0,'rgba(255,248,200,'+(0.75*b).toFixed(2)+')'); gl.addColorStop(1,'rgba(255,248,200,0)'); x.fillStyle=gl; circ(GC,GY,sr*2.6); x.fill(); }
      x.fillStyle='#fff8d6'; circ(GC,GY,sr); x.fill();
      x.save(); circ(GC,GY,sr); x.clip(); x.fillStyle='#0b0f1a'; circ(mx,my,mr); x.fill(); x.restore();
      x.setLineDash([3,3]); x.strokeStyle=b>0.5?'rgba(15,23,42,.5)':'rgba(203,213,225,.55)'; x.lineWidth=1; circ(mx,my,mr); x.stroke(); x.setLineDash([]);
      x.font=F(10.5,1); x.fillStyle=b>0.5?'#1e3a5f':'#e2e8f0';
      if(tot){ x.textAlign='center'; x.fillText('コロナ（皆既中だけ見える）',GC,GY+sr*3.2+2); } else { x.textAlign='left'; x.fillText('太陽',GC+sr+8,GY+4); }
      const rt=mx>GC; x.textAlign=rt?'right':'left'; x.fillText(off?'月（実際はもっと'+(g>0?'上':'下')+'）':cov>0?'月':'月（ふだんは見えない）',mx+(rt?-mr-6:mr+6),my+(Math.abs(my-GY)<sr+mr?-mr-4:4));
    }
    x.restore();
    x.fillStyle='rgba(6,11,28,.62)'; rr(4,TOP+4,GW-8,40,8); x.fill();
    x.textAlign='left'; x.fillStyle='#fff'; x.font=F(13,1); x.fillText('地上から見た様子',12,TOP+21);
    x.font=F(10.5); x.fillStyle='rgba(226,232,240,.9)'; x.fillText(side==='full'?'南の空・東が左。月は右から左へ進む':'月の影の中心近くから・東が左　⚠太陽を直接見ない',12,TOP+37);
    x.fillStyle='rgba(6,11,28,.62)'; rr(4,H-26,GW-8,22,6); x.fill();
    x.font=F(12,1); x.fillStyle=st[1]?'#fca5a5':'#e2e8f0'; x.fillText('いま：'+st[0],12,H-10);
  }
  function dot(cx,cy,ty,done){
    if(!done){ x.fillStyle='rgba(148,163,184,.3)'; circ(cx,cy,2.5); x.fill(); return; }
    if(!ty){ x.strokeStyle='rgba(203,213,225,.6)'; x.lineWidth=1.2; circ(cx,cy,5.5); x.stroke(); return; }
    if(ty==='金環日食'){ x.strokeStyle='#f59e0b'; x.lineWidth=3; circ(cx,cy,5); x.stroke(); return; }
    x.fillStyle=ty.indexOf('皆既')>=0?'#ef4444':ty.indexOf('半影')>=0?'#94a3b8':'#f59e0b'; circ(cx,cy,6); x.fill(); }
  const GT=TOP+44, GB=H-16, GM=(GT+GB)/2, GS=(GB-GT)/2/5.4, X1=322;
  function drawRight(p){
    x.fillStyle='#0b1020'; x.fillRect(X1,TOP,W-X1,H-TOP);
    x.textAlign='left'; x.fillStyle='#fff'; x.font=F(13,1); x.fillText('ずれと食の起こりやすさ',X1+10,TOP+21);
    const gx=X1+14; x.fillStyle='rgba(148,163,184,.2)'; x.fillRect(gx,GT,14,GB-GT);
    const bands=side==='full'?[[(1.5573+p.u)*p.pi,'#64748b'],[(1.0128-p.u)*p.pi,'#f59e0b'],[(0.4678-p.u)*p.pi,'#ef4444']]:[[(1.5433+p.u)*p.pi,'#f59e0b'],[0.9972*p.pi,'#ef4444']];
    bands.forEach(b=>{ x.fillStyle=b[1]; x.fillRect(gx,GM-b[0]*GS,14,2*b[0]*GS); });
    x.font=F(10); x.fillStyle='rgba(203,213,225,.8)'; [[5,'上5°'],[0,'0°'],[-5,'下5°']].forEach(v=>x.fillText(v[1],gx+18,GM-v[0]*GS+4));
    const yb=GM-beta*GS; x.fillStyle='#fff'; x.beginPath(); x.moveTo(gx-1,yb); x.lineTo(gx-9,yb-6); x.lineTo(gx-9,yb+6); x.closePath(); x.fill();
    x.strokeStyle='#fff'; x.lineWidth=2; x.beginPath(); x.moveTo(gx,yb); x.lineTo(gx+14,yb); x.stroke();
    // 1年分（12か月×新月・満月）
    const sx0=X1+80, cw=(W-8-sx0)/12; let ns=0, nl=0; const det={};
    x.font=F(10.5); x.fillStyle='rgba(203,213,225,.85)'; x.fillText('1年（12か月）の新月・満月',sx0,TOP+42);
    x.font=F(10.5,1); x.textAlign='right'; x.fillStyle='#cbd5e1'; x.fillText('新月',sx0-4,TOP+66); x.fillText('満月',sx0-4,TOP+90);
    for(let k=0;k<12;k++){ const cxk=sx0+cw*(k+0.5);
      for(let j=0;j<2;j++){ const i=2*k+j, cyk=TOP+62+24*j, done=!!yr&&i<=yr.idx; let ty='';
        if(done){ const ev=yr.ev[i], gg=ev.beta/p.pi; ty=ev.side==='new'?solar(gg,p).type:lunar(gg,p).type; if(ty){ if(ev.side==='new') ns++; else nl++; det[ty]=(det[ty]||0)+1; } }
        dot(cxk,cyk,ty,done); if(yr&&yr.run&&i===yr.idx){ x.strokeStyle='#fff'; x.lineWidth=1.5; circ(cxk,cyk,9); x.stroke(); } }
      x.font=F(9.5); x.fillStyle='rgba(203,213,225,.6)'; x.textAlign='center'; x.fillText(String(k+1),cxk,TOP+112); }
    const tx=X1+62; x.textAlign='left'; x.font=F(11,1); x.fillStyle='#fde68a';
    if(yr){ const n=yr.run?yr.idx+1:yr.ev.length; x.fillText((yr.run?'調べています… ':'')+'日食 '+ns+'回・月食 '+nl+'回（'+n+'回中）',tx,TOP+136);
      x.font=F(10.5); x.fillStyle='#e2e8f0'; const ks=Object.keys(det); x.fillText(ks.length?ks.map(k=>k+det[k]).join('・'):'食は起きなかった',tx,TOP+153); }
    else { x.fillText('📅「1年分を試す」で12か月分を調べる',tx,TOP+136); x.font=F(10.5); x.fillStyle='#e2e8f0'; x.fillText('新月・満月は1年に約25回あります',tx,TOP+153); }
    x.font=F(11,1); x.fillStyle='#cbd5e1'; x.fillText(side==='full'?'月食が起こるずれ（いまの距離で）':'日食が起こるずれ（いまの距離で）',tx,TOP+178);
    x.font=F(10.5); x.fillStyle='#e2e8f0';
    if(side==='full'){ x.fillText('皆既 '+((0.4678-p.u)*p.pi).toFixed(2)+'°以内・部分 '+((1.0128-p.u)*p.pi).toFixed(2)+'°以内',tx,TOP+195); x.fillText('半影 '+((1.5573+p.u)*p.pi).toFixed(2)+'°以内（ほぼ気づかない）',tx,TOP+211); }
    else { x.fillText('皆既・金環 '+(0.9972*p.pi).toFixed(2)+'°以内（地球のどこかで）',tx,TOP+195); x.fillText('部分 '+((1.5433+p.u)*p.pi).toFixed(2)+'°以内（地球のどこかで）',tx,TOP+211); }
  }
  function dur(m){ if(m<1) return '1分未満'; if(m<60) return Math.round(m)+'分'; const r=Math.round(m/5)*5, h=Math.floor(r/60), mm=r%60; return h+'時間'+(mm?mm+'分':''); }
  function fit(id,v){ setStat(id,v); const e=$(id); if(e) e.style.fontSize=v.length>9?'14px':v.length>6?'16px':''; }
  function tLabel(){ const full=side==='full', a=full?14.765+t/24:((t/24)%29.5306+29.5306)%29.5306, nm=full?'満月':'新月';
    return a.toFixed(2)+'日・'+(Math.abs(t)<0.05?nm+'ちょうど':nm+'の'+Math.abs(t).toFixed(1)+'時間'+(t<0?'前':'後')); }
  const bLabel=()=>Math.abs(beta)<0.005?'0°（一直線）':(beta>0?'上 ':'下 ')+Math.abs(beta).toFixed(2)+'°';
  function draw(){
    const p=prm(), g=beta/p.pi, L=lunar(g,p), S=solar(g,p), st=nowSt(p,g);
    x.clearRect(0,0,W,H); drawSide(p,g,L,S); drawGround(p,g,S,st); drawRight(p);
    x.strokeStyle='rgba(255,255,255,.18)'; x.lineWidth=1; x.beginPath(); x.moveTo(0,TOP); x.lineTo(W,TOP); x.moveTo(X1-2,TOP); x.lineTo(X1-2,H); x.stroke();
    if(side==='full'){ fit('sType',L.type||'月食は起きない'); fit('sMag',L.magU>0?L.magU.toFixed(2):L.magP>0?'半影 '+L.magP.toFixed(2):'0（欠けない）');
      fit('sDur',L.type==='皆既月食'?'皆既 約'+dur(L.tot):L.type==='部分月食'?'部分食 約'+dur(L.par):L.type==='半影月食'?'半影食 約'+dur(L.pen):'なし'); }
    else { fit('sType',S.type||'日食は起きない'); fit('sMag',S.type?S.mag.toFixed(2):'0（欠けない）');
      fit('sDur',S.type==='皆既日食'?'皆既 約'+dur(S.cen):S.type==='金環日食'?'金環 約'+dur(S.cen):S.type==='部分日食'?'部分食 約'+dur(S.par):'なし'); }
    fit('sNow',st[0]);
    $('tL').textContent=tLabel(); $('betaL').textContent=bLabel();
    const typ=side==='full'?(L.type||'月食は起きない'):(S.type||'日食は起きない');
    setShare('【月食・日食】'+(side==='full'?'満月':'新月')+'のとき、月の通り道のずれが'+Math.abs(beta).toFixed(2)+'°なら「'+typ+'」。ずれが約1.5°より大きいと食は起きません🌘｜シミュラボ');
  }
  function stopPlay(){ play=false; hold=0; $('play').textContent='▶ 食の進み方を再生'; }
  let yrTimer=0;
  function stopYear(){ if(yr&&yr.run){ yr.run=false; clearTimeout(yrTimer); $('year').textContent='📅 1年分を試す'; } }
  function stepYear(){ if(!yr||!yr.run) return; yr.idx++;   // 新月・満月を1回ずつ、0.45秒おきに調べる
    if(yr.idx>=yr.ev.length){ yr.idx=yr.ev.length-1; yr.run=false; $('year').textContent='📅 もう一度 1年分を試す'; }
    else { const ev=yr.ev[yr.idx]; side=ev.side; beta=ev.beta; t=0; $('side').value=side; $('beta').value=beta.toFixed(2); $('t').value='0'; yrTimer=setTimeout(stepYear,450); }
    draw(); }
  function startYear(){ const u0=Math.random()*360, ev=[]; const b=(u)=>Math.asin(Math.sin(INC*R)*Math.sin(u*R))/R;   // 通り道の向きは1回の満ち欠けで約30.7°ずれる
    for(let k=0;k<12;k++){ const un=u0+30.6705*k; ev.push({side:'new',beta:b(un)},{side:'full',beta:b(un+195.3353)}); }
    clearTimeout(yrTimer); yr={ev:ev,idx:-1,run:true}; stopPlay(); $('year').textContent='📅 調べています…（止める）'; stepYear(); }
  function frame(ts){ const dt=last?Math.min(0.1,(ts-last)/1000):0; last=ts;
    if(play){ if(hold>0){ hold-=dt; } else { const prev=t; t=Math.min(5,t+dt*1.5); if(prev<0&&t>=0){ t=0; hold=1.2; } if(t>=5) stopPlay(); } $('t').value=t.toFixed(1); need=true; }
    if(need){ need=false; draw(); }
    requestAnimationFrame(frame); }
  function pos(e){ const q=cpos(cv,e); return [q[0]/dpr,q[1]/dpr]; }
  function mv(q){ const p=prm(); stopYear(); stopPlay();
    if(drag==='side') beta=clamp(hpInv(Y0-q[1])*p.pi,-5.15,5.15);
    else if(drag==='gauge') beta=clamp((GM-q[1])/GS,-5.15,5.15);
    else if(side==='full'){ t=clamp((GC-q[0])/(p.n*SCL),-5,5); beta=clamp((GY-q[1])/SCL*p.pi,-5.15,5.15); }
    else t=clamp((GC-q[0])/(VS*SCS),-5,5);
    $('beta').value=beta.toFixed(2); $('t').value=t.toFixed(1); draw(); }
  cv.addEventListener('pointerdown',e=>{ const q=pos(e); drag=q[1]<TOP?'side':q[0]<X1-2?'ground':q[0]<X1+56?'gauge':null; if(!drag) return; try{ cv.setPointerCapture(e.pointerId); }catch(_){ } mv(q); });
  cv.addEventListener('pointermove',e=>{ if(drag) mv(pos(e)); });
  ['pointerup','pointercancel'].forEach(n=>cv.addEventListener(n,()=>{ drag=null; }));
  $('side').addEventListener('change',()=>{ side=$('side').value; stopYear(); draw(); });
  $('t').addEventListener('input',()=>{ t=+$('t').value; stopPlay(); draw(); });
  $('beta').addEventListener('input',()=>{ beta=+$('beta').value; stopYear(); draw(); });
  $('dist').addEventListener('change',()=>{ draw(); });
  $('play').addEventListener('click',()=>{ if(play){ stopPlay(); } else { if(t>=0) t=-5; play=true; hold=0; stopYear(); $('play').textContent='⏸ 止める'; } draw(); });
  $('zero').addEventListener('click',()=>{ beta=0; $('beta').value='0'; stopYear(); draw(); });
  $('year').addEventListener('click',()=>{ if(yr&&yr.run) stopYear(); else startYear(); });
  draw(); need=false; requestAnimationFrame(frame);
''')
