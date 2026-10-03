# -*- coding: utf-8 -*-
"""理科の授業向け：気象（湿度・露点・雲のでき方）と地震（P波・S波・初期微動継続時間）"""
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

# 飽和水蒸気量［g/m³］（0〜40℃・1℃ごと）。中学校の教科書・問題集で使われる値（25℃=23.1 の系統）。
SAT = [4.8, 5.2, 5.6, 6.0, 6.4, 6.8, 7.3, 7.8, 8.3, 8.8, 9.4, 10.0, 10.7, 11.4, 12.1, 12.8, 13.6, 14.5, 15.4, 16.3,
       17.3, 18.3, 19.4, 20.6, 21.8, 23.1, 24.4, 25.8, 27.2, 28.8, 30.4, 32.1, 33.8, 35.7, 37.6, 39.6, 41.7, 43.9,
       46.2, 48.6, 51.1]
assert len(SAT) == 41 and all(SAT[i] < SAT[i + 1] for i in range(40))
SAT_JS = ",".join("%.1f" % v for v in SAT)


def _sat_table():
    rows = []
    for r in range(14):
        row = []
        for g in range(3):
            t = g * 14 + r
            row += (["%d℃" % t, "%.1f" % SAT[t]] if t <= 40 else ["", ""])
        rows.append(row)
    return T(rows, ["気温", "飽和水蒸気量［g/m³］"] * 3)


def _ps_table():
    pairs = [(6, 3.5), (7, 4), (8, 4), (6, 3)]
    head = ["初期微動継続時間"] + ["P波%g・S波%g km/秒<br>（係数%s）" % (p, s, ("%.1f" % (p * s / (p - s))) if abs(p * s / (p - s) * 10 - round(p * s / (p - s) * 10)) < 1e-9 else "約%.1f" % (p * s / (p - s))) for p, s in pairs]
    rows = []
    for t in [1, 2, 5, 10, 15, 20, 30]:
        rows.append(["%d秒" % t] + ["%.1f km" % (p * s / (p - s) * t) for p, s in pairs])
    return T(rows, head)


# ============================================================ 1 湿度と雲のでき方
sim(slug="shitsudo-roten", cat="rika", emoji="☁️", score=80,
    title="湿度と雲のでき方シミュレーター（飽和水蒸気量・露点）",
    title_tag="露点・飽和水蒸気量のシミュレーター｜湿度の計算と雲のでき方（中2理科）",
    meta_desc="気温と水蒸気量を動かすと、飽和水蒸気量のグラフ上で湿度と露点がその場で計算されます。空気を冷やすと露点で水滴ができ、上昇させると雲ができ始める高さが分かる無料シミュレーター。1℃ごとの飽和水蒸気量の表と計算問題の解き方つき。",
    og_title="湿度と雲のでき方シミュレーター（飽和水蒸気量・露点）",
    og_desc="気温と水蒸気量を動かして湿度・露点を計算。冷やすと露、上昇させると雲ができ始める高さが分かる中2理科の教材です。",
    card_desc="気温と水蒸気量から湿度・露点を計算。空気を冷やしたり上昇させたりして、露や雲ができる温度と高さを確かめる。",
    lead="気温と水蒸気量を決めると、飽和水蒸気量のグラフの上で湿度と露点がその場で計算されます。「冷やす」を押すと点が左へ動き、曲線にぶつかった温度（露点）で水滴ができ始めます。「上昇させる」モードでは、雲ができ始める高さを求められます。",
    model="中2 気象観測・天気の変化（霧や雲の発生）",
    level="中学2年",
    unit="中学校 第2分野（4）気象とその変化",
    canvas=canvas(640, 490, light=True),
    controls=select("mode", "モード", [("cool", "冷やす（露点と水滴）"), ("rise", "上昇させる（雲の高さ）")])
           + slider("t0", "気温（はじめ）", 0, 40, 25, 1, "{v}℃")
           + slider("v0", "水蒸気量", 4.8, 51.1, 12.8, 0.1, "{v} g/m³")
           + slider("tc", "冷やしたあとの気温", 0, 40, 10, 1, "{v}℃")
           + slider("hh", "上昇させる高さ", 0, 4000, 2000, 50, "{v} m"),
    buttons=btn("go", "❄ 冷やす", True) + btn("back", "↺ はじめにもどす"),
    stats=stats([("sT", "気温", False), ("sV", "水蒸気量", False), ("sS", "飽和水蒸気量", False), ("sRH", "湿度", True),
                 ("sTd", "露点", True), ("sH", "雲ができ始める高さ", False), ("sW", "水滴になった量", False)]),
    legend="オレンジの点＝はじめの空気（グラフの上を指やペンでなぞると動かせます）。緑の点＝冷やした・上昇させたあとの空気。点が青い曲線（飽和水蒸気量）にぶつかる温度が露点で、曲線より上にはみ出す分が水滴（露・霧・雲）になります。右の図は、飽和水蒸気量を「コップの大きさ」、水蒸気量を「中の水」にたとえたものです。",
    article='''
<h2>このシミュレーションでわかること</h2>
<p>空気を冷やしていくと、空気1m³にふくまれる水蒸気量がその気温の飽和水蒸気量と等しくなる温度（<b>露点</b>）で水滴ができ始め、さらに冷やすと、飽和水蒸気量をこえた分が水滴になります。湿度は「水蒸気量÷飽和水蒸気量×100」で求められます。空気が上昇すると100mにつき約1℃気温が下がるので、<b>（地上の気温−露点）×100m</b>の高さで雲ができ始めます。</p>
<p>対応する単元は、中学校学習指導要領 理科 第2分野（4）「気象とその変化」の「気象観測」と「天気の変化（霧や雲の発生）」で、主に<b>中学2年</b>で学習します。</p>

<h2>授業での使い方</h2>
<ul>
<li><b>導入</b>：冷たい飲み物を入れたコップの表面や、冬の窓ガラスに水滴がつく様子を見せて、「この水はどこから来たのか」を問います。シミュレーターで「冷やす」を押し、点が曲線にぶつかったところで水滴ができ始めることを確かめます。</li>
<li><b>展開</b>：金属製のコップに氷水を少しずつ加え、表面がくもり始めた水温（露点）を測る実験のあとに、測った気温と露点をシミュレーターに入れて湿度を求めます。雲をつくる実験（簡易真空容器などで袋の中の空気を膨張させる実験）のあとは「上昇させる」モードに切りかえ、上空で雲ができるしくみにつなげます。</li>
<li><b>まとめ</b>：下の例題を解いてから、統計欄の値で答え合わせをします。右側の「コップのたとえ」で、飽和水蒸気量（コップの大きさ）と水蒸気量（中の水）の関係を確認します。</li>
</ul>
<p>生徒への問いの例：</p>
<ol>
<li>気温を変えずに水蒸気量だけを増やすと、湿度と露点はそれぞれどう変わるでしょうか。</li>
<li>同じ空気でも、朝と昼で湿度がちがうのはなぜでしょうか（水蒸気量は変わらないとして考えましょう）。</li>
<li>湿度が高い日と低い日では、雲ができ始める高さはどちらが低くなるでしょうか。</li>
</ol>

<h2>しくみ・解説</h2>
<h3>飽和水蒸気量と湿度</h3>
<p>空気1m³がふくむことのできる水蒸気の最大の質量を<b>飽和水蒸気量</b>［g/m³］といい、気温が高いほど大きくなります。グラフの青い曲線がこれにあたります。空気のしめりぐあいを表す<b>湿度</b>は、次の式で求めます。</p>
''' + N("湿度［％］＝ 空気1m³にふくまれる水蒸気量［g/m³］÷ その気温での飽和水蒸気量［g/m³］× 100") + '''
<h3>露点</h3>
<p>空気を冷やしても、ふくまれている水蒸気量は変わりません。一方で飽和水蒸気量は小さくなるので、湿度は上がっていきます。水蒸気量と飽和水蒸気量が等しくなった温度が<b>露点</b>で、このとき湿度は100％です。露点より下げると、飽和水蒸気量をこえた分の水蒸気が水滴になります（凝結）。地表付近でできたものが露や霧、上空でできたものが雲です。</p>
<h3>計算問題の解き方（例題）</h3>
<p>飽和水蒸気量は、このページの下の早見表の値を使います。</p>
<p><b>例題1</b>　気温25℃の空気1m³に、12.8gの水蒸気がふくまれています。湿度は何％ですか。<br>
→ 25℃の飽和水蒸気量は23.1g/m³なので、12.8÷23.1×100＝55.41…　答え <b>約55％</b>（小数第1位を四捨五入）</p>
<p><b>例題2</b>　例題1の空気の露点は何℃ですか。<br>
→ 飽和水蒸気量が12.8g/m³になる気温を表でさがすと15℃です。　答え <b>15℃</b></p>
<p><b>例題3</b>　例題1の空気を10℃まで冷やすと、空気1m³あたり何gの水滴ができますか。また、容積200m³の理科室全体では何gですか。<br>
→ 10℃の飽和水蒸気量は9.4g/m³なので、12.8−9.4＝3.4g。理科室全体では3.4×200＝680g。　答え <b>3.4g、680g</b></p>
<p><b>例題4</b>　気温28℃、湿度50％の空気の露点は何℃ですか。<br>
→ 水蒸気量＝28℃の飽和水蒸気量×湿度÷100＝27.2×50÷100＝13.6g/m³。飽和水蒸気量が13.6g/m³になるのは16℃です。　答え <b>16℃</b></p>
<p><b>例題5</b>　例題4の空気が上昇すると、地上から何mの高さで雲ができ始めますか。空気は100m上昇するごとに1℃下がるものとします。<br>
→ 28℃から露点の16℃まで12℃下がる必要があるので、12×100＝1200m。　答え <b>1200m</b></p>
''' + P("例題1〜3をシミュレーターで確かめるには、気温（はじめ）を25℃、水蒸気量を12.8g/m³、冷やしたあとの気温を10℃にして「冷やす」を押します。統計欄に湿度55.4％、露点15.0℃、雲ができ始める高さ1000m、水滴になった量3.4g/m³が出ます。") + '''
<h3>雲のでき方</h3>
<p>空気のかたまりが上昇すると、上空ほど気圧が低いために膨張し、温度が下がります。中学校では「100m上昇するごとに約1℃下がる」として考えます。温度が露点まで下がると、水蒸気が小さな水滴（0℃より低いところでは氷の粒）になり、雲ができます。雲ができ始めてからは、水蒸気が水滴になるときに熱を出すため、温度の下がり方は100mにつき約0.5℃とゆるやかになります（発展。高校入試のフェーン現象の問題でよく使われる値です）。シミュレーターの「上昇させる」モードもこの値で計算しています。</p>
<h3>飽和水蒸気量の早見表（0〜40℃、1℃ごと）</h3>
''' + _sat_table() + N("<b>このシミュレーターで単純化している点</b><br>"
     "・飽和水蒸気量は、中学校の教科書や問題集でよく使われる値（25℃＝23.1g/m³の表）です。教科書によっては小数第1位が0.1ほどちがうことがあるので、授業では使っている教科書の表に合わせてください。表と表の間の温度は、となりの2つの値を直線で結んで計算しています（露点が小数になるのはこのためです）。<br>"
     "・教科書と同じく、冷やしても上昇しても、空気1m³中の水蒸気量は変わらないものとして計算しています。実際には上昇した空気は膨張するので露点も少し下がり（100mにつき約0.2℃）、雲ができ始める高さは（気温−露点）×約125mになります。また、気象庁などが水蒸気圧から求める露点は、この方法で求めた値より0.5℃ほど高くなります。<br>"
     "・0℃より低い温度は扱っていません（水蒸気量は露点が0℃以上になる範囲で動きます）。") + '''
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「中学校学習指導要領（平成29年告示）解説 理科編」（<a href="https://www.mext.go.jp/a_menu/shotou/new-cs/1387016.htm" target="_blank" rel="noopener">中学校学習指導要領解説</a>）</li>
<li>中学校理科の教科書（東京書籍「新しい科学」、啓林館「未来へひろがるサイエンス」、大日本図書「理科の世界」、学校図書「中学校科学」、教育出版「自然の探究 中学理科」）の第2学年「気象とその変化」の単元</li>
<li>気象庁「気象観測の手引き」（湿度・露点温度の観測）</li>
<li>国立天文台 編『理科年表』（丸善出版）</li>
</ul>
''',
    faqs=[("露点とは何ですか？", "空気を冷やしていったとき、ふくまれている水蒸気が水滴に変わり始める温度です。空気1m³中の水蒸気量が、その温度の飽和水蒸気量と等しくなる温度なので、露点では湿度が100％になります。たとえば水蒸気量12.8g/m³の空気の露点は、飽和水蒸気量が12.8g/m³になる15℃です。"),
          ("湿度はどうやって計算しますか？", "湿度［％］＝空気1m³にふくまれる水蒸気量［g/m³］÷その気温での飽和水蒸気量［g/m³］×100 で求めます。気温25℃（飽和水蒸気量23.1g/m³）で水蒸気量が12.8g/m³なら、12.8÷23.1×100＝約55％です。"),
          ("空気を冷やすと湿度が上がるのはなぜですか？", "冷やしても空気中の水蒸気量は変わりませんが、飽和水蒸気量（式の分母）が小さくなるからです。露点で湿度は100％になり、それより冷やしても湿度は100％のまま、入りきらなくなった水蒸気が水滴になります。"),
          ("雲ができ始める高さはどう求めますか？", "空気が100m上昇するごとに約1℃下がるとすると、（地上の気温−露点）×100［m］で求められます。気温25℃・露点15℃なら、10℃下がる必要があるので1000mです。"),
          ("教科書の飽和水蒸気量の表と値が少しちがいます。", "飽和水蒸気量の表は、教科書や問題集によって小数第1位が0.1ほどちがうことがあります。このシミュレーターは25℃を23.1g/m³とする表を使っています。授業やテストでは、使っている教科書や問題に書かれた表の値で計算してください。"),
          ("霧と雲はどうちがいますか？", "どちらも、空気中の水蒸気が冷やされてできた小さな水滴（や氷の粒）が浮かんでいるものです。地表付近にできたものを霧、上空にできたものを雲とよびます。")],
    rel=[("sentaku-kawaku", "👕", "洗濯物 乾く時間メーター"), ("kiatsu-jet", "🎢", "気圧ジェットコースター指数"),
         ("kaminari-alert", "⚡", "今日の雷ゴロゴロ度"), ("amagumo-now", "🌧️", "いまの雨雲マップ")],
    js=r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  cv.setAttribute('role','img'); cv.setAttribute('aria-label','気温と飽和水蒸気量のグラフ。点を動かすと湿度と露点が分かります');
  cv.style.cursor='pointer';
  const SAT=[@SAT@];
  const sat=(t)=>{ t=clamp(t,0,40); const i=Math.min(39,Math.floor(t)); return SAT[i]+(SAT[i+1]-SAT[i])*(t-i); };
  const dew=(v)=>{ if(v<=SAT[0]) return 0; for(let i=0;i<40;i++){ if(v<=SAT[i+1]+1e-9) return i+(v-SAT[i])/(SAT[i+1]-SAT[i]); } return 40; };
  const r1=(v)=>Math.round(v*10)/10, f1=(v)=>r1(v).toFixed(1);
  const PL=50, PR=380, PT=46, PB=390, YM=55;
  const gx=(t)=>PL+t/40*(PR-PL), gy=(v)=>PB-v/YM*(PB-PT);
  const RX=404, GY=396, TOPY=78, HMAX=4000;
  const hy=(h)=>GY-h/HMAX*(GY-TOPY);
  const line=(a,b,c,d)=>{ ctx.beginPath(); ctx.moveTo(a,b); ctx.lineTo(c,d); ctx.stroke(); };
  function txt(s,x,y,font,col,al,halo){ ctx.font=font; ctx.textAlign=al||'left'; if(halo){ ctx.lineJoin='round'; ctx.lineWidth=3.5; ctx.strokeStyle='rgba(255,255,255,.95)'; ctx.strokeText(s,x,y); } ctx.fillStyle=col; ctx.fillText(s,x,y); }
  function tw(s,font){ ctx.font=font; return ctx.measureText(s).width; }
  function rr(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.lineTo(x+w-r,y); ctx.quadraticCurveTo(x+w,y,x+w,y+r); ctx.lineTo(x+w,y+h-r); ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h); ctx.lineTo(x+r,y+h); ctx.quadraticCurveTo(x,y+h,x,y+h-r); ctx.lineTo(x,y+r); ctx.quadraticCurveTo(x,y,x+r,y); ctx.closePath(); }
  function lab(id){ const s=$(id), l=$(id+'L'); if(l) l.textContent = s.dataset.fmt ? s.dataset.fmt.replace('{v}', s.value) : s.value; }
  function hbText(hb){ const show=Math.round((T0-r1(dew(V0)))*100); return (Math.abs(hb-show)<0.5?'':'約')+show+'m'; }
  let T0=25, V0=12.8, Tc=25, hc=0, anim=null, flash=0, dragging=false, dirty=true, last=performance.now();
  const isRise=()=>$('mode').value==='rise';
  function st(){ const rise=isRise(), Td=dew(V0), hb=(T0-Td)*100, hTop=hb+Td*200; let T=Tc;
    if(rise) T = hc<=hb ? T0-hc/100 : Td-(hc-hb)/200;
    T=clamp(T,0,40); const S=r1(sat(T)), V=Math.min(V0,S), Wt=Math.max(0,r1(V0-S));
    return {rise:rise,T:T,S:S,V:V,Wt:Wt,RH:V/S*100,Td:Td,hb:hb,hTop:hTop}; }
  function vlab(){ $('v0L').textContent=V0.toFixed(1)+' g/m³'; }
  function syncInputs(){ const a=$('t0'); a.value=T0; lab('t0'); const b=$('v0'); b.max=sat(T0).toFixed(1); b.value=V0.toFixed(1); vlab(); const c=$('tc'); c.max=T0; if(+c.value>T0) c.value=T0; lab('tc'); }
  function reset(){ anim=null; flash=0; Tc=T0; hc=0; dirty=true; }
  function setMode(){ const r=isRise(); $('tc').closest('.field').style.display=r?'none':''; $('hh').closest('.field').style.display=r?'':'none'; $('go').textContent=r?'⬆ 上昇させる':'❄ 冷やす'; reset(); }
  $('t0').addEventListener('input',()=>{ T0=+$('t0').value; V0=clamp(r1(Math.min(V0,sat(T0))),SAT[0],sat(T0)); syncInputs(); reset(); });
  $('v0').addEventListener('input',()=>{ V0=clamp(+$('v0').value,SAT[0],sat(T0)); vlab(); reset(); });
  $('tc').addEventListener('input',()=>{ anim=null; flash=0; Tc=Math.min(T0,+$('tc').value); dirty=true; });
  $('hh').addEventListener('input',()=>{ anim=null; flash=0; hc=Math.min(+$('hh').value,st().hTop); dirty=true; });
  $('mode').addEventListener('change',setMode);
  $('go').addEventListener('click',()=>{ const s=st(); flash=0; if(s.rise){ hc=0; anim={k:'h',to:Math.min(+$('hh').value,s.hTop),pause:0}; } else { Tc=T0; anim={k:'t',to:Math.min(+$('tc').value,T0),pause:0}; } dirty=true; });
  $('back').addEventListener('click',reset);
  function step(dt){ if(!anim) return; dirty=true; if(anim.pause>0){ anim.pause-=dt; return; } const s=st();
    if(anim.k==='t'){ const prev=Tc; Tc=Math.max(anim.to,Tc-4*dt);
      if(prev>s.Td+1e-6 && Tc<=s.Td+1e-6){ flash=1.8; if(anim.to<s.Td-1e-6){ Tc=s.Td; anim.pause=0.9; return; } }
      if(Tc<=anim.to+1e-9){ Tc=anim.to; anim=null; } }
    else { const prev=hc; hc=Math.min(anim.to,hc+400*dt);
      if(prev<s.hb-1e-6 && hc>=s.hb-1e-6){ flash=1.8; if(anim.to>s.hb+1e-6){ hc=s.hb; anim.pause=0.9; return; } }
      if(hc>=anim.to-1e-9){ hc=anim.to; anim=null; } } }
  function drop(x,y,r){ ctx.fillStyle='#2563eb'; ctx.beginPath(); ctx.moveTo(x,y-r*1.6); ctx.quadraticCurveTo(x+r,y-r*0.2,x+r,y+r*0.3); ctx.arc(x,y+r*0.3,r,0,Math.PI); ctx.quadraticCurveTo(x-r,y-r*0.2,x,y-r*1.6); ctx.fill(); }
  function puff(x,y,r){ const c=[[0,0,1],[-0.85,0.25,0.68],[0.85,0.25,0.68],[-0.42,-0.48,0.62],[0.45,-0.42,0.58]]; ctx.beginPath(); c.forEach((q)=>{ ctx.moveTo(x+q[0]*r+q[2]*r,y+q[1]*r); ctx.arc(x+q[0]*r,y+q[1]*r,q[2]*r,0,Math.PI*2); });
    ctx.strokeStyle='#94a3b8'; ctx.lineWidth=2.4; ctx.stroke(); ctx.fillStyle='#ffffff'; ctx.fill(); }
  function drawGraph(s){
    txt('気温と飽和水蒸気量のグラフ',8,18,'bold 13px sans-serif','#0f172a');
    txt('水蒸気量［g/m³］',8,38,'11px sans-serif','#475569');
    ctx.beginPath(); ctx.moveTo(gx(0),gy(0)); for(let t=0;t<=40.001;t+=0.5) ctx.lineTo(gx(t),gy(sat(t))); ctx.lineTo(gx(40),gy(0)); ctx.closePath(); ctx.fillStyle='#e0f2fe'; ctx.fill();
    ctx.strokeStyle='rgba(15,23,42,.08)'; ctx.lineWidth=1;
    for(let t=5;t<=40;t+=5) line(gx(t),PT,gx(t),PB);
    for(let v=5;v<=YM;v+=5) line(PL,gy(v),PR,gy(v));
    ctx.strokeStyle='#334155'; ctx.lineWidth=1.5; line(PL,PT-6,PL,PB); line(PL,PB,PR+6,PB); ctx.lineWidth=1;
    for(let t=0;t<=40;t++) line(gx(t),PB,gx(t),PB+(t%5?3:6));
    for(let t=0;t<=40;t+=5) txt(String(t),gx(t),PB+18,'11px sans-serif','#475569','center');
    for(let v=0;v<=50;v+=10){ line(PL-5,gy(v),PL,gy(v)); txt(String(v),PL-8,gy(v)+4,'11px sans-serif','#475569','right'); }
    txt('気温［℃］',PR+6,PB+34,'11px sans-serif','#475569','right');
    ctx.strokeStyle='#0369a1'; ctx.lineWidth=3; line(226,34,246,34); txt('飽和水蒸気量の曲線',250,38,'bold 11px sans-serif','#0369a1');
    txt('↑ 曲線より上に出る分は水滴になる',gx(0.6),gy(45),'11px sans-serif','#94a3b8');
    txt('湿度100％未満の空気',PR-6,gy(5),'11px sans-serif','#0369a1','right');
    ctx.beginPath(); for(let t=0;t<=40.001;t+=0.25){ const X=gx(t), Y=gy(sat(t)); if(t===0) ctx.moveTo(X,Y); else ctx.lineTo(X,Y); } ctx.strokeStyle='#0369a1'; ctx.lineWidth=2.5; ctx.stroke();
    // 補助線
    const x0=gx(T0), y0=gy(V0), xd=gx(s.Td), S0=sat(T0);
    ctx.setLineDash([5,4]); ctx.lineWidth=1.3; ctx.strokeStyle='#64748b'; line(x0,y0,xd,y0); line(xd,y0,xd,PB);
    ctx.strokeStyle='#ea580c'; line(x0,y0,x0,gy(S0)); ctx.setLineDash([]);
    ctx.fillStyle='#ea580c'; ctx.beginPath(); ctx.arc(x0,gy(S0),3.5,0,Math.PI*2); ctx.fill();
    const sl='飽和 '+f1(S0)+'g', slw=tw(sl,'11px sans-serif');
    if(x0-8-slw>PL+2) txt(sl,x0-7,gy(S0)-5,'11px sans-serif','#c2410c','right',true); else txt(sl,x0+7,gy(S0)-5,'11px sans-serif','#c2410c','left',true);
    if(y0-gy(S0)>26){ const al='あと'+f1(S0-V0)+'g', alw=tw(al,'bold 11px sans-serif'); if(x0+8+alw<PR+20) txt(al,x0+7,(y0+gy(S0))/2+4,'bold 11px sans-serif','#c2410c','left',true); else txt(al,x0-7,(y0+gy(S0))/2+4,'bold 11px sans-serif','#c2410c','right',true); }
    ctx.fillStyle='#fff'; ctx.strokeStyle='#0369a1'; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(xd,y0,5,0,Math.PI*2); ctx.fill(); ctx.stroke();
    const dl='露点 '+f1(s.Td)+'℃', dlw=tw(dl,'bold 12px sans-serif');
    if(xd+6+dlw<PR) txt(dl,xd+5,PB-7,'bold 12px sans-serif','#0369a1','left',true); else txt(dl,xd-5,PB-7,'bold 12px sans-serif','#0369a1','right',true);
    // 冷やした（上昇した）あとの空気
    const moved = s.rise ? hc>0.5 : Tc<T0-1e-6;
    if(moved){ ctx.strokeStyle='#0d9488'; ctx.lineWidth=4; ctx.lineCap='round'; ctx.lineJoin='round'; ctx.beginPath(); ctx.moveTo(x0,y0); ctx.lineTo(gx(Math.max(s.T,s.Td)),y0);
      if(s.T<s.Td){ for(let t=s.Td;t>s.T;t-=0.2) ctx.lineTo(gx(t),gy(sat(t))); ctx.lineTo(gx(s.T),gy(sat(s.T))); } ctx.stroke(); ctx.lineCap='butt';
      if(s.Wt>0){ const bx=gx(s.T), ya=gy(V0), yb=gy(s.S); ctx.fillStyle='rgba(37,99,235,.30)'; ctx.fillRect(bx-6,ya,12,yb-ya); ctx.strokeStyle='#2563eb'; ctx.lineWidth=1.5; ctx.strokeRect(bx-6,ya,12,yb-ya);
        const wl='水滴 '+f1(s.Wt)+'g', ww=tw(wl,'bold 12px sans-serif'), my=Math.min(PB-24,(ya+yb)/2+4);
        if(bx-12-ww>PL) txt(wl,bx-11,my,'bold 12px sans-serif','#1d4ed8','right',true); else txt(wl,bx+11,my,'bold 12px sans-serif','#1d4ed8','left',true); }
      ctx.fillStyle='#0d9488'; ctx.strokeStyle='#fff'; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(gx(s.T),gy(s.V),6.5,0,Math.PI*2); ctx.fill(); ctx.stroke(); }
    ctx.fillStyle='#f97316'; ctx.strokeStyle='#fff'; ctx.lineWidth=2.5; ctx.beginPath(); ctx.arc(x0,y0,7.5,0,Math.PI*2); ctx.fill(); ctx.stroke();
    const il='はじめの空気', ilw=tw(il,'bold 12px sans-serif'), iy=Math.min(PB-22,y0+18);
    if(x0+12+ilw<PR+16) txt(il,x0+11,iy,'bold 12px sans-serif','#c2410c','left',true); else txt(il,x0-11,iy,'bold 12px sans-serif','#c2410c','right',true);
    if(flash>0){ const a=Math.min(1,flash/0.6); ctx.strokeStyle='rgba(2,132,199,'+a.toFixed(2)+')'; ctx.lineWidth=3; ctx.beginPath(); ctx.arc(xd,y0,9+(1.8-flash)*10,0,Math.PI*2); ctx.stroke();
      const msg=s.rise?'露点に達した → 雲ができ始める':'露点に達した → 水滴ができ始める'; const mw=tw(msg,'bold 12px sans-serif')+16;
      const bx=clamp(xd-mw/2,PL+4,PR-mw), by=Math.max(PT+4,y0-46);
      ctx.globalAlpha=a; ctx.fillStyle='#0369a1'; rr(bx,by,mw,22,6); ctx.fill(); txt(msg,bx+8,by+15,'bold 12px sans-serif','#fff'); ctx.globalAlpha=1; } }
  function drawCup(s){ const L=RX+4;
    txt('コップのたとえ（空気1m³）',L,18,'bold 13px sans-serif','#0f172a');
    const rows=[['c','コップ＝飽和水蒸気量 '+f1(s.S)+'g'],['w','中の水＝水蒸気量 '+f1(s.V)+'g'],['d','あふれた水＝水滴 '+f1(s.Wt)+'g']];
    rows.forEach((r,i)=>{ const y=40+i*19; if(r[0]==='c'){ ctx.strokeStyle='#334155'; ctx.lineWidth=2; ctx.strokeRect(L+1,y-10,11,11); } else if(r[0]==='w'){ ctx.fillStyle='#38bdf8'; ctx.fillRect(L,y-11,13,13); } else { drop(L+6.5,y-4,5); } txt(r[1],L+19,y,'12px sans-serif','#1e293b'); });
    const cx=RX+70, cw=76, k=5.4, by=GY, top=by-s.S*k, wl=by-s.V*k, xl=cx-cw/2, xr=cx+cw/2;
    if(s.Wt>0){ const gt=by-V0*k; ctx.fillStyle='rgba(96,165,250,.16)'; ctx.fillRect(xl,gt,cw,top-gt); ctx.setLineDash([4,3]); ctx.strokeStyle='#60a5fa'; ctx.lineWidth=1.5; ctx.strokeRect(xl,gt,cw,top-gt); ctx.setLineDash([]); if(top-gt>14) txt('入りきらない',cx,(gt+top)/2+4,'11px sans-serif','#1d4ed8','center'); }
    ctx.fillStyle='#f0f9ff'; ctx.fillRect(xl,top,cw,by-top);
    const gw=ctx.createLinearGradient(0,wl,0,by); gw.addColorStop(0,'#7dd3fc'); gw.addColorStop(1,'#0ea5e9'); ctx.fillStyle=gw; ctx.fillRect(xl,wl,cw,by-wl);
    ctx.strokeStyle='#334155'; ctx.lineWidth=2.5; ctx.beginPath(); ctx.moveTo(xl,top); ctx.lineTo(xl,by); ctx.lineTo(xr,by); ctx.lineTo(xr,top); ctx.stroke();
    if(wl-top>16) txt('あと'+f1(s.S-s.V)+'g',cx,(top+wl)/2+4,'11px sans-serif','#475569','center');
    if(by-wl>20) txt(f1(s.V)+'g',cx,wl+(by-wl)/2+5,'bold 13px sans-serif','#ffffff','center');
    if(s.Wt>0){ const pr=Math.min(46,12+Math.sqrt(s.Wt)*10), pry=Math.min(9,3+Math.sqrt(s.Wt)*1.6), px=xr+20+pr;
      for(let j=0;j<3;j++) drop(xr+7+j*5, top+14+j*Math.max(8,(by-top)/3.5), 3.6);
      ctx.fillStyle='rgba(37,99,235,.55)'; ctx.beginPath(); ctx.ellipse(px,by-pry+1,pr,pry,0,0,Math.PI*2); ctx.fill();
      txt('水滴 '+f1(s.Wt)+'g',px,by-pry-8,'bold 12px sans-serif','#1d4ed8','center',true); }
    txt('気温 '+f1(s.T)+'℃',cx,by+18,'bold 12px sans-serif','#0f172a','center');
    txt('湿度 '+f1(s.RH)+'％',cx,by+35,'bold 12px sans-serif','#0369a1','center'); }
  function drawRise(s){ const L=RX+4, AX=RX+30, R=W-4, px=RX+150;
    txt('空気のかたまりを上昇させる',L,18,'bold 13px sans-serif','#0f172a');
    txt('高さ '+Math.round(hc)+'m　気温 '+f1(s.T)+'℃',L,38,'bold 13px sans-serif','#0f766e');
    txt('100mごとに1℃下がる（雲の中は0.5℃）',L,56,'11px sans-serif','#64748b');
    const g=ctx.createLinearGradient(0,TOPY,0,GY); g.addColorStop(0,'#bfdbfe'); g.addColorStop(1,'#f0f9ff'); ctx.fillStyle=g; ctx.fillRect(AX,TOPY-8,R-AX,GY-TOPY+8);
    ctx.fillStyle='#86efac'; ctx.fillRect(AX,GY,R-AX,8);
    ctx.strokeStyle='#334155'; ctx.lineWidth=1; line(AX,TOPY-8,AX,GY+8);
    for(let h=0;h<=HMAX;h+=500){ const y=hy(h); line(AX-(h%1000?3:6),y,AX,y); if(h%1000===0) txt(h+'m',AX-8,y+4,'10px sans-serif','#475569','right'); }
    const yb=hy(Math.min(s.hb,HMAX));
    ctx.setLineDash([6,4]); ctx.strokeStyle='#0369a1'; ctx.lineWidth=1.5; line(AX,yb,R,yb); ctx.setLineDash([]);
    if(GY-yb>22){ txt('雲ができ始める',AX+5,yb-5,'bold 11px sans-serif','#0369a1','left',true); txt(hbText(s.hb),AX+5,yb+14,'bold 11px sans-serif','#0369a1','left',true); }
    else txt('雲ができ始める '+hbText(s.hb),AX+5,yb-5,'bold 11px sans-serif','#0369a1','left',true);
    const py=hy(hc), r=12+8*hc/HMAX, cloudy=s.T<=s.Td+1e-6;
    ctx.setLineDash([3,4]); ctx.strokeStyle='rgba(15,118,110,.55)'; ctx.lineWidth=1.5; line(px,GY,px,py+r); ctx.setLineDash([]);
    if(hc>s.hb+1){ for(let h=s.hb;h<hc;h+=70) puff(px+Math.sin(h*0.011)*9,hy(h),12+3*Math.sin(h*0.023)); }
    if(cloudy) puff(px,py,r+3); else { ctx.fillStyle='rgba(255,255,255,.92)'; ctx.strokeStyle='#0f766e'; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(px,py,r,0,Math.PI*2); ctx.fill(); ctx.stroke(); }
    txt(cloudy?'雲':'空気',px,py+4,'bold 11px sans-serif',cloudy?'#334155':'#0f766e','center');
    if(anim && anim.pause<=0){ ctx.strokeStyle='#0f766e'; ctx.lineWidth=2; line(px,py-r-4,px,py-r-16); line(px,py-r-16,px-5,py-r-10); line(px,py-r-16,px+5,py-r-10); }
    const lx=px+r+8; txt(Math.round(hc)+'m',lx,py-2,'bold 11px sans-serif','#0f172a','left',true); txt(f1(s.T)+'℃',lx,py+12,'bold 11px sans-serif','#0f766e','left',true);
    txt('地上（気温 '+T0+'℃）',AX+5,GY+22,'11px sans-serif','#334155');
    if(+$('hh').value>s.hTop+1 && hc>=s.hTop-1) txt('0℃に達したので、ここで止めています',AX+5,TOPY+8,'bold 11px sans-serif','#b91c1c','left',true); }
  function drawBand(s){ const y=442; ctx.fillStyle='#f8fafc'; ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; rr(6,y,W-12,44,8); ctx.fill(); ctx.stroke();
    txt('湿度 ＝ 水蒸気量 ÷ 飽和水蒸気量 × 100 ＝ '+f1(s.V)+' ÷ '+f1(s.S)+' × 100 ＝ '+f1(s.RH)+'％',16,y+18,'bold 13px sans-serif','#0f172a');
    const parts=[];
    if(s.rise) parts.push(['雲ができ始める高さ ＝ ('+T0+' − '+f1(s.Td)+') × 100 ＝ '+hbText(s.hb),'#0f766e']);
    else parts.push(['露点 ＝ 飽和水蒸気量が '+f1(V0)+'g になる温度 ＝ '+f1(s.Td)+'℃','#0369a1']);
    if(s.Wt>0) parts.push([(s.rise?'水滴（雲の粒）':'水滴')+' ＝ '+f1(V0)+' − '+f1(s.S)+' ＝ '+f1(s.Wt)+'g（1m³あたり）','#1d4ed8']);
    let font='bold 12px sans-serif', tot=0; parts.forEach((p)=>{ tot+=tw(p[0],font)+28; }); if(tot>W-36) font='bold 11px sans-serif';
    let x=16; parts.forEach((p,i)=>{ if(i){ txt('／',x+2,y+37,font,'#94a3b8'); x+=22; } txt(p[0],x,y+37,font,p[1]); x+=tw(p[0],font)+6; }); }
  function draw(){ const s=st(); ctx.clearRect(0,0,W,H); ctx.fillStyle='#fff'; ctx.fillRect(0,0,W,H); drawGraph(s); if(s.rise) drawRise(s); else drawCup(s); drawBand(s);
    setStat('sT',f1(s.T)+'℃'); setStat('sV',f1(s.V)+' g/m³'); setStat('sS',f1(s.S)+' g/m³'); setStat('sRH',f1(s.RH)+'%'); setStat('sTd',f1(s.Td)+'℃'); setStat('sH',hbText(s.hb)); setStat('sW',f1(s.Wt)+' g/m³');
    const rh0=f1(V0/r1(sat(T0))*100); let sh;
    if(s.rise) sh='【雲のでき方】気温'+T0+'℃・露点'+f1(s.Td)+'℃の空気が上昇すると、'+hbText(s.hb)+'の高さで雲ができ始める（100mで1℃下がるとして計算）｜シミュラボ';
    else if(s.Wt>0) sh='【湿度と露点】気温'+T0+'℃・水蒸気量'+f1(V0)+'g/m³（湿度'+rh0+'%）の空気は'+f1(s.Td)+'℃で露が出始め、'+f1(s.T)+'℃まで冷やすと1m³あたり'+f1(s.Wt)+'gの水滴ができる｜シミュラボ';
    else sh='【湿度と露点】気温'+T0+'℃・水蒸気量'+f1(V0)+'g/m³（湿度'+rh0+'%）の空気は'+f1(s.Td)+'℃で露が出始める。上昇すると'+hbText(s.hb)+'の高さで雲ができ始める｜シミュラボ';
    setShare(sh); }
  function pxy(e){ const p=cpos(cv,e); return [p[0]/dpr,p[1]/dpr]; }
  function setXY(x,y){ const t=clamp(Math.round((x-PL)/(PR-PL)*40),0,40); const v=clamp(r1((PB-y)/(PB-PT)*YM),SAT[0],sat(t)); T0=t; V0=r1(v); syncInputs(); reset(); }
  cv.addEventListener('pointerdown',(e)=>{ const q=pxy(e); if(q[0]<PL-14||q[0]>PR+14||q[1]<PT-14||q[1]>PB+14) return; dragging=true; try{ cv.setPointerCapture(e.pointerId); }catch(err){ } setXY(q[0],q[1]); e.preventDefault(); });
  cv.addEventListener('pointermove',(e)=>{ if(!dragging) return; const q=pxy(e); setXY(q[0],q[1]); });
  ['pointerup','pointercancel'].forEach((n)=>cv.addEventListener(n,()=>{ dragging=false; }));
  function loop(now){ const dt=Math.min(0.05,Math.max(0,(now-last)/1000)); last=now; step(dt); if(flash>0){ flash=Math.max(0,flash-dt); dirty=true; } if(dirty){ dirty=false; draw(); } requestAnimationFrame(loop); }
  syncInputs(); setMode(); draw(); requestAnimationFrame(loop);
'''.replace("@SAT@", SAT_JS))


# ============================================================ 2 地震の伝わり方
sim(slug="jishin-ha", cat="rika", emoji="📳", score=82,
    title="地震の伝わり方シミュレーター（P波・S波・初期微動継続時間）",
    title_tag="P波・S波と初期微動継続時間のシミュレーター｜震源距離の求め方（中1理科）",
    meta_desc="震央を動かして地震を起こすと、P波とS波が同心円状に広がり、5つの観測点の地震計に初期微動と主要動が記録されます。初期微動継続時間と震源からの距離の比例をグラフで確かめ、震源距離の求め方や緊急地震速報のしくみも学べる無料シミュレーター。",
    og_title="地震の伝わり方シミュレーター（P波・S波・初期微動継続時間）",
    og_desc="P波とS波が広がる様子と地震計の記録を同時に表示。初期微動継続時間から震源距離を求める中1理科の教材です。",
    card_desc="P波とS波が広がる様子と地震計の記録を同時に表示。初期微動継続時間から震源距離を求める練習にも使える。",
    lead="震央をドラッグして地震を起こすと、P波（青）とS波（赤）が同心円状に広がり、5つの観測点の地震計に初期微動と主要動が記録されます。初期微動継続時間が震源からの距離に比例することを、グラフと計算で確かめられます。",
    model="中1 火山と地震（地震の伝わり方）",
    level="中学1年",
    unit="中学校 第2分野（2）大地の成り立ちと変化",
    canvas=canvas(640, 600, light=True),
    controls=slider("vp", "P波の速さ", 4, 8, 6, 0.1, "{v} km/秒") + slider("vs", "S波の速さ", 2, 5, 3.5, 0.1, "{v} km/秒")
           + slider("dep", "震源の深さ", 0, 100, 10, 5, "{v} km")
           + select("st", "観測点を選ぶ", [("0", "A地点"), ("1", "B地点"), ("2", "C地点"), ("3", "D地点"), ("4", "E地点")])
           + slider("tt", "地震発生からの時間", 0, 90, 0, 0.1, "{v} 秒") + slider("sp", "再生速度", 1, 20, 8, 1, "×{v}")
           + select("gm", "グラフ", [("ps", "初期微動継続時間と距離"), ("tt", "P波・S波の到着時刻と距離")])
           + select("eew", "緊急地震速報（発展）", [("off", "表示しない"), ("on", "表示する")]),
    buttons=btn("quake", "▶ 地震を起こす", True) + btn("toggle", "⏸ 一時停止") + btn("rand", "🎲 震央をランダムに"),
    stats=stats([("sD", "A地点の震源距離", False), ("sP", "P波の到着時刻", False), ("sS", "S波の到着時刻", False), ("sPS", "初期微動継続時間", True)]),
    legend="地図の×＝震央（指やペンでドラッグすると動かせます）、▲＝観測点（タップで選べます。青＝P波が到着、赤＝S波が到着）。下の地震計の記録は震源に近い順に並べ、時刻はすべて地震が発生した瞬間を0秒としています。緊急地震速報を表示すると、紫の点線の円（速報が出た瞬間のS波の位置）の内側では速報が間に合いません。地図と観測点は説明のための架空のもので、地下の波の速さは一定としています。",
    article='''
<h2>このシミュレーションでわかること</h2>
<p>地震が起きると、震源から速いP波と遅いS波が同時に出て、ほぼ同心円状に広がります。P波が届くと小さな揺れ（<b>初期微動</b>）、S波が届くと大きな揺れ（<b>主要動</b>）が始まり、その時間の差（<b>初期微動継続時間</b>）は震源からの距離に比例します。震源からの距離は「P波の速さ×S波の速さ÷（P波の速さ−S波の速さ）×初期微動継続時間」で求められます。</p>
<p>対応する単元は、中学校学習指導要領 理科 第2分野（2）「大地の成り立ちと変化」の「火山と地震」（地震の伝わり方と地球内部の働き）で、主に<b>中学1年</b>で学習します。</p>

<h2>授業での使い方</h2>
<ul>
<li><b>導入</b>：「地震のとき、はじめにカタカタと小さく揺れて、あとからユサユサと大きく揺れた経験はありますか」と問いかけ、「地震を起こす」で2種類の波が広がる様子を見せます。</li>
<li><b>展開</b>：観測点ごとの地震計の記録を比べ、震源から遠い地点ほどP波・S波の到着がおそく、初期微動継続時間が長くなることを見つけます。グラフを「初期微動継続時間と距離」にして比例の関係を確かめ、教科書の例題と同じ速さにスライダーを合わせて計算問題を解きます。震央をドラッグして動かしても、どの観測点でも同じ比例の関係が成り立つことを確かめられます。</li>
<li><b>まとめ</b>：「緊急地震速報（発展）」を表示して、速報が出たときにS波がどこまで届いているかを地図で確かめ、震源に近い場所では速報が間に合わない理由を話し合います。</li>
</ul>
<p>生徒への問いの例：</p>
<ol>
<li>震源からの距離が2倍になると、初期微動継続時間は何倍になるでしょうか。</li>
<li>S波の速さだけを速くして、P波の速さに近づけると、同じ地点の初期微動継続時間は長くなるでしょうか、短くなるでしょうか。</li>
<li>緊急地震速報が、震源の近くでは強い揺れに間に合わないことがあるのはなぜでしょうか。</li>
</ol>

<h2>しくみ・解説</h2>
<h3>P波とS波</h3>
<p>地震は、地下の岩盤がずれ動くことで起こります。最初にずれ動いた場所が<b>震源</b>、その真上の地表の地点が<b>震央</b>です。震源からは、伝わる速さのちがう2種類の波が同時に出ます。</p>
''' + T([["P波（Primary wave）", "速い（気象庁の説明では秒速約7km）", "初期微動（小さな揺れ）", "波の進む向きに揺れる縦波"],
          ["S波（Secondary wave）", "おそい（同じく秒速約4km）", "主要動（大きな揺れ）", "進む向きと垂直に揺れる横波"]],
         ["波", "伝わる速さ", "起こす揺れ", "揺れ方"]) + '''
<p>速さは地下の岩石の種類や深さによって変わります。このシミュレーターの初期値（P波6km/秒・S波3.5km/秒）は計算しやすい典型的な値で、スライダーで教科書や問題集の例題の値に合わせられます。</p>
<h3>初期微動継続時間と震源からの距離</h3>
<p>震源からの距離をD［km］、P波の速さをVp、S波の速さをVs［km/秒］とすると、P波が届くまでの時間はD÷Vp、S波が届くまでの時間はD÷Vs［秒］です。初期微動継続時間はその差なので、次のようになります。</p>
''' + N("初期微動継続時間 ＝ D÷Vs − D÷Vp<br>震源距離 D ＝ Vp×Vs÷（Vp−Vs）× 初期微動継続時間") + '''
<p>初期微動継続時間は距離に<b>比例</b>します。P波6km/秒・S波3.5km/秒なら、6×3.5÷（6−3.5）＝8.4なので「震源距離＝8.4×初期微動継続時間」です。この関係は1899年に大森房吉が示したもので「大森公式」とよばれ、係数はふつう6〜8km/秒程度です。</p>
<p>このシミュレーターでは震源の深さも変えられます。比例の式で使うのは震央からではなく<b>震源からの距離（震源距離）</b>です。震源距離は、震央から観測点までの距離と震源の深さから、三平方の定理（中学3年の数学）で求めています。</p>
<h3>計算問題の解き方（例題）</h3>
<p><b>例題1</b>　P波の速さを6km/秒、S波の速さを3.5km/秒とします。ある地点の初期微動継続時間が15秒でした。震源からの距離は何kmですか。<br>
→ 距離をx kmとすると、x÷3.5−x÷6＝15。通分すると2.5x÷21＝15なので、x＝126。（式にあてはめても 8.4×15＝126）　答え <b>126km</b></p>
<p><b>例題2</b>　震源からの距離が84kmの地点で、初期微動継続時間は10秒でした。初期微動継続時間が25秒の地点は、震源から何kmですか。<br>
→ 初期微動継続時間は距離に比例するので、84×25÷10＝210。　答え <b>210km</b></p>
<p><b>例題3</b>　震源からの距離が42kmのA地点には10時15分27秒に、126kmのB地点には10時15分41秒にP波が届きました。（1）P波の速さ、（2）地震が発生した時刻、（3）S波の速さが3.5km/秒のときのA地点の初期微動継続時間を求めなさい。<br>
→ （1）距離の差÷時間の差＝（126−42）÷（41−27）＝84÷14＝6km/秒<br>
→ （2）A地点までP波は42÷6＝7秒かかるので、27秒−7秒＝20秒。発生時刻は<b>10時15分20秒</b><br>
→ （3）S波はA地点まで42÷3.5＝12秒かかるので、10時15分32秒に到着。32−27＝<b>5秒</b></p>
<p><b>例題4（発展）</b>　震源から21kmの地点の地震計にP波が届いた5秒後に、緊急地震速報が出されました。震源から105kmのC市では、速報を受けてから何秒後に主要動が始まりますか。P波は6km/秒、S波は3.5km/秒とします。<br>
→ P波が21kmの地点に届くのは地震発生の21÷6＝3.5秒後なので、速報は3.5＋5＝8.5秒後。S波がC市に届くのは105÷3.5＝30秒後。30−8.5＝21.5。　答え <b>21.5秒後</b></p>
''' + P("初期値のまま（P波6km/秒・S波3.5km/秒・深さ10km・震央は左下）で地震を起こすと、A〜E地点の震源距離は約84・126・168・210・252km、初期微動継続時間は10・15・20・25・30秒になります。グラフの点が原点を通る1本の直線にのることを確かめてください。") + '''
<h3>初期微動継続時間から震源距離を求める早見表</h3>
''' + _ps_table() + '''
<h3>緊急地震速報のしくみ（発展）</h3>
<p>気象庁の緊急地震速報は、震源に近い地震計でP波をとらえ、震源の位置や地震の規模、各地の震度をすぐに計算して、S波（主要動）が届く前に知らせるしくみです。地震波よりも、通信で送る情報のほうがはるかに速く伝わることを利用しています。ただし解析と伝達には数秒かかるため、震源に近い場所では、速報が強い揺れに間に合わないことがあります。</p>
<p>シミュレーターで「表示する」を選ぶと、いちばん近い観測点にP波が届いた5秒後に速報が出ると仮定して、そのときS波が届いている範囲（紫の点線の円の内側＝間に合わない範囲）と、各観測点で速報からS波が届くまでの時間（猶予）を表示します。</p>
''' + N("<b>このシミュレーターで単純化している点</b><br>"
     "・地下の波の速さは場所によらず一定とし、波は震源を中心とする球面（地表では同心円）で広がるとしています。実際は地下のつくりによって速さが変わるため、きれいな同心円にはなりません。<br>"
     "・地図と観測点は説明のための架空のものです。地震計の波形は見た目のためのモデルで、揺れの大きさや周期は実際の記録とは異なります（震源から遠いほど揺れが小さくなる傾向だけを表しています）。<br>"
     "・緊急地震速報は「いちばん近い観測点でP波をとらえて5秒後に発表」と単純化しています。実際に発表されるまでの時間は地震によって異なります。") + '''
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「中学校学習指導要領（平成29年告示）解説 理科編」（<a href="https://www.mext.go.jp/a_menu/shotou/new-cs/1387016.htm" target="_blank" rel="noopener">中学校学習指導要領解説</a>）</li>
<li>気象庁「緊急地震速報のしくみ」（<a href="https://www.jma.go.jp/jma/kishou/know/jishin/eew/shikumi/shikumi.html" target="_blank" rel="noopener">気象庁ホームページ</a>）</li>
<li>中学校理科の教科書（東京書籍「新しい科学」、啓林館「未来へひろがるサイエンス」、大日本図書「理科の世界」、学校図書「中学校科学」、教育出版「自然の探究 中学理科」）の第1学年「大地の成り立ちと変化」の単元</li>
<li>宇津徳治『地震学』（共立出版）</li>
</ul>
''',
    faqs=[("初期微動継続時間とは何ですか？", "P波が届いてからS波が届くまでの時間で、その間は初期微動（小さな揺れ）が続きます。震源から遠いほど長くなり、震源からの距離にほぼ比例します。"),
          ("初期微動継続時間から震源距離を求める式は？", "震源距離＝P波の速さ×S波の速さ÷（P波の速さ−S波の速さ）×初期微動継続時間 です。P波6km/秒・S波3.5km/秒なら係数は8.4なので、初期微動継続時間が10秒の地点は震源から84kmです。距離と時間は比例するので、ある地点のデータが分かっていれば、比を使っても求められます。"),
          ("P波とS波のちがいは何ですか？", "P波は速く伝わり、初期微動（カタカタという小さな揺れ）を起こします。S波はP波よりおそく伝わり、主要動（ユサユサという大きな揺れ）を起こします。P波は波の進む向きに揺れる縦波、S波は進む向きと垂直に揺れる横波です。"),
          ("震源と震央のちがいは何ですか？", "震源は地下で岩盤が最初にずれ動いた場所、震央は震源の真上にある地表の地点です。初期微動継続時間から求められるのは、震源からの距離（震源距離）です。"),
          ("緊急地震速報は、なぜ大きな揺れの前に届くのですか？", "震源に近い地震計で速いP波をとらえ、すぐに震源や揺れの大きさを計算して、おそいS波が届く前に通信で知らせるからです。ただし解析と伝達に数秒かかるため、震源に近い場所では間に合わないことがあります。"),
          ("P波とS波の速さはいつも同じですか？", "地下の岩石の種類や深さによって変わります。気象庁の説明ではP波は秒速約7km、S波は秒速約4kmです。問題集では「P波6km/秒・S波3km/秒」「P波8km/秒・S波4km/秒」のように計算しやすい値が使われることが多いので、スライダーをその値に合わせて確かめてください。")],
    rel=[("jishin-live", "🗾", "日本はいまも揺れている"), ("chikyu-yure", "🌐", "地球まるごと地震カウンター"),
         ("tsunami-kishi", "🌊", "津波はなぜ岸で高くなる？"), ("building-quake", "🏢", "地震でビルはどう揺れる？")],
    js=r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  cv.setAttribute('role','img'); cv.setAttribute('aria-label','震央と観測点の地図、P波とS波の広がり、地震計の記録、初期微動継続時間と震源距離のグラフ');
  cv.style.cursor='pointer';
  const MX=8, MY=30, MS=300;
  const GL=374, GR=628, GT=46, GB=292;
  const RY=360, RH=44, TX0=84, TX1=630;
  const ST=[{n:'A',x:99.0,y:201.0},{n:'B',x:66.1,y:137.1},{n:'C',x:204.0,y:225.1},{n:'D',x:157.3,y:86.1},{n:'E',x:251.2,y:122.9}];
  const COAST=[[0,140],[20,150],[38,166],[56,176],[70,192],[86,206],[100,222],[114,240],[126,262],[138,284],[146,300]];
  const PH=ST.map((_,i)=>[0,1,2,3].map((k)=>(((i+1)*(k+3)*37)%100)/100*Math.PI*2));
  let ex=40, ey=260, t=0, playing=true, dragging=false, sel=0, dirty=true, last=performance.now();
  const f1=(v)=>(Math.round(v*10)/10).toFixed(1);
  const line=(a,b,c,d)=>{ ctx.beginPath(); ctx.moveTo(a,b); ctx.lineTo(c,d); ctx.stroke(); };
  function txt(s,x,y,font,col,al,halo){ ctx.font=font; ctx.textAlign=al||'left'; if(halo){ ctx.lineJoin='round'; ctx.lineWidth=3.5; ctx.strokeStyle='rgba(255,255,255,.95)'; ctx.strokeText(s,x,y); } ctx.fillStyle=col; ctx.fillText(s,x,y); }
  function tw(s,font){ ctx.font=font; return ctx.measureText(s).width; }
  function rr(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.lineTo(x+w-r,y); ctx.quadraticCurveTo(x+w,y,x+w,y+r); ctx.lineTo(x+w,y+h-r); ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h); ctx.lineTo(x+r,y+h); ctx.quadraticCurveTo(x,y+h,x,y+h-r); ctx.lineTo(x,y+r); ctx.quadraticCurveTo(x,y,x+r,y); ctx.closePath(); }
  function tri(x,y,r){ ctx.beginPath(); ctx.moveTo(x,y-r); ctx.lineTo(x+r*0.9,y+r*0.6); ctx.lineTo(x-r*0.9,y+r*0.6); ctx.closePath(); }
  function dot(x,y,r,col){ ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.fillStyle=col; ctx.fill(); ctx.strokeStyle='#fff'; ctx.lineWidth=1.5; ctx.stroke(); }
  function setK(id,s){ const e=$(id); if(e && e.previousElementSibling) e.previousElementSibling.textContent=s; }
  function vlab(){ $('vpL').textContent=(+$('vp').value).toFixed(1)+' km/秒'; $('vsL').textContent=(+$('vs').value).toFixed(1)+' km/秒'; $('ttL').textContent=(+$('tt').value).toFixed(1)+' 秒'; }
  const surfR=(R,d)=>R>d?Math.sqrt(R*R-d*d):0;
  function model(){ const vp=+$('vp').value, vs=+$('vs').value, d=+$('dep').value;
    const D=ST.map((s)=>{ const dx=s.x-ex, dy=s.y-ey; return Math.sqrt(dx*dx+dy*dy+d*d); });
    const tp=D.map((x)=>x/vp), ts=D.map((x)=>x/vs);
    const tend=Math.ceil((Math.max.apply(null,ts)+12)/10)*10;
    const order=D.map((x,i)=>i).sort((a,b)=>D[a]-D[b]);
    return {vp:vp,vs:vs,d:d,D:D,tp:tp,ts:ts,tend:tend,order:order,k:vp*vs/(vp-vs),tal:Math.min.apply(null,tp)+5}; }
  function gsc(m){ const dmax=Math.max.apply(null,m.D); const DX=Math.max(100,Math.ceil(dmax*1.1/50)*50); const ps=$('gm').value==='ps';
    const raw=ps?DX/m.k:DX/m.vs; const s=raw<=20?2:(raw<=50?5:10); const YM=Math.max(2*s,Math.ceil(raw*1.05/s)*s);
    return {ps:ps,DX:DX,YM:YM,ys:YM<=20?5:(YM<=60?10:20),xs:DX>300?100:50,X:(v)=>GL+v/DX*(GR-GL),Y:(v)=>GB-v/YM*(GB-GT)}; }
  function sig(i,tt,m){ const tp=m.tp[i], ts=m.ts[i]; if(tt<tp) return 0; const ph=PH[i]; const u=tt-tp;
    const eP=Math.min(1,u/0.5)*(tt<ts?1:Math.max(0.35,Math.exp(-(tt-ts)/3)));
    let y=0.28*eP*(0.6*Math.sin(2*Math.PI*2.6*u+ph[0])+0.4*Math.sin(2*Math.PI*4.1*u+ph[1]));
    if(tt>=ts){ const w=tt-ts; const eS=Math.min(1,w/1.0)*Math.exp(-w/(8+m.D[i]/25)); y+=eS*(0.62*Math.sin(2*Math.PI*0.75*w+ph[2])+0.38*Math.sin(2*Math.PI*1.25*w+ph[3])); }
    return y; }
  function drawMap(m){ const X=(k)=>MX+k, Y=(k)=>MY+k, cx=X(ex), cy=Y(ey), eew=$('eew').value==='on';
    txt('地図（上から見た図）',MX,20,'bold 13px sans-serif','#0f172a');
    ctx.lineWidth=3; ctx.strokeStyle='#2563eb'; line(152,15,168,15); txt('P波',171,20,'12px sans-serif','#1e3a8a');
    ctx.strokeStyle='#dc2626'; line(200,15,216,15); txt('S波',219,20,'12px sans-serif','#7f1d1d');
    ctx.fillStyle='#334155'; tri(254,14,6); ctx.fill(); txt('観測点',262,20,'12px sans-serif','#334155');
    ctx.save(); ctx.beginPath(); ctx.rect(MX,MY,MS,MS); ctx.clip();
    ctx.fillStyle='#dbeafe'; ctx.fillRect(MX,MY,MS,MS);
    ctx.beginPath(); ctx.moveTo(X(0),Y(0)); ctx.lineTo(X(300),Y(0)); ctx.lineTo(X(300),Y(300)); for(let j=COAST.length-1;j>=0;j--) ctx.lineTo(X(COAST[j][0]),Y(COAST[j][1])); ctx.closePath();
    ctx.fillStyle='#f7fee7'; ctx.fill(); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1.2; ctx.stroke();
    ctx.strokeStyle='rgba(100,116,139,.18)'; ctx.lineWidth=1; for(let k=50;k<300;k+=50){ line(X(k),MY,X(k),MY+MS); line(MX,Y(k),MX+MS,Y(k)); }
    txt('海',X(14),Y(292),'12px sans-serif','#64748b');
    const rP=surfR(m.vp*t,m.d), rS=surfR(m.vs*t,m.d);
    if(rP>0){ ctx.beginPath(); ctx.arc(cx,cy,rP,0,Math.PI*2); if(rS>0){ ctx.moveTo(cx+rS,cy); ctx.arc(cx,cy,rS,0,Math.PI*2,true); } ctx.fillStyle='rgba(59,130,246,.18)'; ctx.fill(); }
    if(rS>0){ ctx.beginPath(); ctx.arc(cx,cy,rS,0,Math.PI*2); ctx.fillStyle='rgba(239,68,68,.20)'; ctx.fill(); }
    if(rP>0){ ctx.strokeStyle='#2563eb'; ctx.lineWidth=2.5; ctx.beginPath(); ctx.arc(cx,cy,rP,0,Math.PI*2); ctx.stroke(); }
    if(rS>0){ ctx.strokeStyle='#dc2626'; ctx.lineWidth=2.5; ctx.beginPath(); ctx.arc(cx,cy,rS,0,Math.PI*2); ctx.stroke(); }
    if(eew && t>=m.tal){ const rA=surfR(m.vs*m.tal,m.d); if(rA>0){ ctx.setLineDash([6,4]); ctx.strokeStyle='#7c3aed'; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(cx,cy,rA,0,Math.PI*2); ctx.stroke(); ctx.setLineDash([]);
        const ly=cy-rA-5, lx=clamp(cx,MX+50,MX+MS-50); if(ly>MY+100) txt('速報のときのS波',lx,ly,'bold 11px sans-serif','#6d28d9','center',true); else if(cy+rA+15<MY+MS-20) txt('速報のときのS波',lx,cy+rA+15,'bold 11px sans-serif','#6d28d9','center',true); } }
    ctx.strokeStyle='#b91c1c'; ctx.lineWidth=3.5; line(cx-7,cy-7,cx+7,cy+7); line(cx-7,cy+7,cx+7,cy-7);
    txt('震央',cx+10,cy+(cy>MY+MS-24?-8:17),'bold 12px sans-serif','#b91c1c','left',true);
    ST.forEach((s,i)=>{ const x=X(s.x), y=Y(s.y), k=t>=m.ts[i]?2:(t>=m.tp[i]?1:0);
      if(i===sel){ ctx.strokeStyle='#f59e0b'; ctx.lineWidth=3; ctx.beginPath(); ctx.arc(x,y-1,13,0,Math.PI*2); ctx.stroke(); }
      ctx.fillStyle=['#334155','#2563eb','#dc2626'][k]; tri(x,y,9); ctx.fill(); ctx.strokeStyle='#fff'; ctx.lineWidth=1.5; ctx.stroke();
      txt(s.n,x+11,y-6,'bold 14px sans-serif','#0f172a','left',true); });
    txt('地震発生から '+f1(t)+' 秒',MX+6,MY+19,'bold 14px sans-serif','#0f172a','left',true);
    txt('震源の深さ '+m.d+' km',MX+6,MY+37,'12px sans-serif','#334155','left',true);
    if(eew && t>=m.tal){ const bt='緊急地震速報（発生'+f1(m.tal)+'秒後）', bw=tw(bt,'bold 12px sans-serif')+16; ctx.fillStyle='#6d28d9'; rr(MX+6,MY+44,bw,20,6); ctx.fill(); txt(bt,MX+14,MY+58,'bold 12px sans-serif','#fff'); }
    ctx.strokeStyle='#0f172a'; ctx.lineWidth=2; line(MX+MS-62,MY+MS-12,MX+MS-12,MY+MS-12); txt('50 km',MX+MS-37,MY+MS-18,'11px sans-serif','#0f172a','center',true);
    ctx.restore(); ctx.strokeStyle='#64748b'; ctx.lineWidth=1; ctx.strokeRect(MX+0.5,MY+0.5,MS,MS); }
  function drawGraph(m){ const g=gsc(m);
    txt(g.ps?'初期微動継続時間と震源からの距離':'P波・S波が届くまでの時間と距離',GL-34,20,'bold 13px sans-serif','#0f172a');
    txt(g.ps?'初期微動継続時間［秒］':'地震発生からの時間［秒］',GL-34,38,'11px sans-serif','#475569');
    ctx.strokeStyle='rgba(15,23,42,.08)'; ctx.lineWidth=1;
    for(let v=g.xs;v<=g.DX;v+=g.xs) line(g.X(v),GT,g.X(v),GB);
    for(let v=g.ys;v<=g.YM+1e-9;v+=g.ys) line(GL,g.Y(v),GR,g.Y(v));
    ctx.strokeStyle='#334155'; ctx.lineWidth=1.5; line(GL,GT-4,GL,GB); line(GL,GB,GR,GB);
    for(let v=0;v<=g.DX;v+=g.xs) txt(String(v),g.X(v),GB+14,'11px sans-serif','#475569','center');
    for(let v=0;v<=g.YM+1e-9;v+=g.ys) txt(String(v),GL-5,g.Y(v)+4,'11px sans-serif','#475569','right');
    txt('震源からの距離［km］',GR,GB+30,'11px sans-serif','#475569','right');
    ctx.save(); ctx.beginPath(); ctx.rect(GL,GT-8,GR-GL+4,GB-GT+8); ctx.clip();
    if(g.ps){ ctx.setLineDash([6,4]); ctx.strokeStyle='#64748b'; ctx.lineWidth=1.6; line(g.X(0),g.Y(0),g.X(g.DX),g.Y(g.DX/m.k)); ctx.setLineDash([]);
      ST.forEach((s,i)=>{ if(t>=m.ts[i]){ const x=g.X(m.D[i]), y=g.Y(m.ts[i]-m.tp[i]); dot(x,y,i===sel?7:5,i===sel?'#f59e0b':'#0f172a'); txt(s.n,x+8,y+14,'bold 12px sans-serif','#0f172a','left',true); } }); }
    else { ctx.lineWidth=2; ctx.strokeStyle='#2563eb'; line(g.X(0),g.Y(0),g.X(g.DX),g.Y(g.DX/m.vp)); ctx.strokeStyle='#dc2626'; line(g.X(0),g.Y(0),g.X(g.DX),g.Y(g.DX/m.vs));
      if(t>0){ ctx.setLineDash([4,4]); ctx.strokeStyle='rgba(15,23,42,.45)'; ctx.lineWidth=1; line(GL,g.Y(t),GR,g.Y(t)); ctx.setLineDash([]); }
      const i0=sel; if(t>=m.ts[i0]){ const x=g.X(m.D[i0]); ctx.strokeStyle='#f59e0b'; ctx.lineWidth=4; line(x,g.Y(m.tp[i0]),x,g.Y(m.ts[i0])); }
      ST.forEach((s,i)=>{ const x=g.X(m.D[i]); if(t>=m.tp[i]){ dot(x,g.Y(m.tp[i]),i===sel?6:4.5,'#2563eb'); txt(s.n,x+6,g.Y(m.tp[i])+14,'bold 11px sans-serif','#0f172a','left',true); } if(t>=m.ts[i]) dot(x,g.Y(m.ts[i]),i===sel?6:4.5,'#dc2626'); }); }
    ctx.restore();
    if(g.ps){ txt('震源距離 ＝ '+f1(m.k)+' × 初期微動継続時間',GL+8,GT+14,'bold 12px sans-serif','#0f172a','left',true);
      txt('（'+m.vp.toFixed(1)+'×'+m.vs.toFixed(1)+'÷('+m.vp.toFixed(1)+'−'+m.vs.toFixed(1)+')＝'+f1(m.k)+'）',GL+8,GT+30,'11px sans-serif','#475569','left',true); }
    else { txt('S波 '+m.vs.toFixed(1)+' km/秒',GL+8,GT+14,'bold 12px sans-serif','#b91c1c','left',true); txt('P波 '+m.vp.toFixed(1)+' km/秒',GR-4,g.Y(g.DX/m.vp)+18,'bold 12px sans-serif','#1d4ed8','right',true);
      const i0=sel; if(t>=m.ts[i0]){ const x=g.X(m.D[i0]), y=(g.Y(m.tp[i0])+g.Y(m.ts[i0]))/2+4, lb='初期微動継続時間 '+f1(m.ts[i0]-m.tp[i0])+'秒', w=tw(lb,'bold 11px sans-serif');
        if(x-8-w>GL+2) txt(lb,x-7,y,'bold 11px sans-serif','#b45309','right',true); else txt(lb,x+7,y,'bold 11px sans-serif','#b45309','left',true); } } }
  function drawRows(m){ const tx=(v)=>TX0+v/m.tend*(TX1-TX0), tc=Math.min(t,m.tend), eew=$('eew').value==='on', yA=RY+5*RH;
    txt('地震計の記録（震源に近い順）',MX,RY-10,'bold 13px sans-serif','#0f172a');
    txt('青い帯＝初期微動　赤い帯＝主要動',W-6,RY-10,'11px sans-serif','#475569','right');
    m.order.forEach((i,r)=>{ const y0=RY+r*RH, yc=y0+RH/2+3;
      if(i===sel){ ctx.fillStyle='#fef3c7'; ctx.fillRect(MX,y0+1,W-MX-4,RH-2); }
      txt(ST[i].n+'地点',MX+4,yc-3,'bold 13px sans-serif','#0f172a'); txt(m.D[i].toFixed(0)+' km',MX+4,yc+13,'11px sans-serif','#475569');
      ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1; line(TX0,yc,TX1,yc);
      if(tc>=m.tp[i]){ ctx.fillStyle='rgba(59,130,246,.14)'; ctx.fillRect(tx(m.tp[i]),y0+3,tx(Math.min(tc,m.ts[i]))-tx(m.tp[i]),RH-6); }
      if(tc>=m.ts[i]){ ctx.fillStyle='rgba(239,68,68,.10)'; ctx.fillRect(tx(m.ts[i]),y0+3,tx(tc)-tx(m.ts[i]),RH-6); }
      const amp=6+10*Math.exp(-m.D[i]/150), xe=tx(tc), xs=Math.max(TX0,tx(m.tp[i])-1);
      ctx.strokeStyle='#0f172a'; ctx.lineWidth=1.1; ctx.beginPath(); ctx.moveTo(TX0,yc);
      if(xe>xs){ ctx.lineTo(xs,yc); for(let X=xs;X<=xe;X+=0.5){ const v=(X-TX0)/(TX1-TX0)*m.tend; ctx.lineTo(X,yc-sig(i,v,m)*amp); } } else ctx.lineTo(xe,yc);
      ctx.stroke();
      if(tc>=m.tp[i]){ ctx.strokeStyle='#2563eb'; ctx.lineWidth=2; line(tx(m.tp[i]),y0+4,tx(m.tp[i]),y0+RH-4); txt('P',tx(m.tp[i])-3,y0+13,'bold 11px sans-serif','#2563eb','right',true); }
      if(tc>=m.ts[i]){ ctx.strokeStyle='#dc2626'; ctx.lineWidth=2; line(tx(m.ts[i]),y0+4,tx(m.ts[i]),y0+RH-4); txt('S',tx(m.ts[i])+3,y0+13,'bold 11px sans-serif','#dc2626','left',true);
        const ps=m.ts[i]-m.tp[i], wpx=tx(m.ts[i])-tx(m.tp[i]), L1='初期微動 '+f1(ps)+'秒', L2=f1(ps)+'秒';
        if(tw(L1,'11px sans-serif')+6<wpx) txt(L1,tx(m.tp[i])+3,y0+RH-6,'11px sans-serif','#1d4ed8','left',true); else if(tw(L2,'11px sans-serif')+6<wpx) txt(L2,tx(m.tp[i])+3,y0+RH-6,'11px sans-serif','#1d4ed8','left',true); }
      if(eew && tc>=m.tal){ const gsec=m.ts[i]-m.tal; txt(gsec>0?'猶予 '+f1(gsec)+'秒':'間に合わない',TX1-2,y0+13,'bold 11px sans-serif','#6d28d9','right',true); } });
    ctx.strokeStyle='#334155'; ctx.lineWidth=1; line(TX0,yA,TX1,yA);
    const stp=m.tend<=60?5:(m.tend<=120?10:20);
    for(let v=0;v<=m.tend;v+=stp){ const x=tx(v); line(x,yA,x,yA+4); txt(String(v),x,yA+15,'11px sans-serif','#475569','center'); }
    txt('時間（秒）',MX+4,yA+15,'11px sans-serif','#475569');
    if(tc>0){ ctx.strokeStyle='rgba(15,23,42,.45)'; ctx.lineWidth=1; line(tx(tc),RY,tx(tc),yA); }
    if(eew && tc>=m.tal){ ctx.setLineDash([5,4]); ctx.strokeStyle='#7c3aed'; ctx.lineWidth=1.5; line(tx(m.tal),RY,tx(m.tal),yA); ctx.setLineDash([]); txt('速報',tx(m.tal)+3,yA-4,'bold 11px sans-serif','#6d28d9','left',true); } }
  function draw(m){ ctx.clearRect(0,0,W,H); ctx.fillStyle='#fff'; ctx.fillRect(0,0,W,H); drawMap(m); drawGraph(m); drawRows(m);
    const i=sel, n=ST[i].n+'地点', ps=m.ts[i]-m.tp[i];
    setK('sD',n+'の震源距離'); setStat('sD',f1(m.D[i])+' km'); setStat('sP',f1(m.tp[i])+' 秒後'); setStat('sS',f1(m.ts[i])+' 秒後'); setStat('sPS',f1(ps)+' 秒');
    setShare('【P波・S波】'+n+'（震源から'+f1(m.D[i])+'km）の初期微動継続時間は'+f1(ps)+'秒。P波'+m.vp.toFixed(1)+'km/秒・S波'+m.vs.toFixed(1)+'km/秒なら、震源距離＝'+f1(m.k)+'×初期微動継続時間｜シミュラボ'); }
  function tog(){ $('toggle').textContent=playing?'⏸ 一時停止':'▶ 再生'; }
  function frame(now){ const dt=Math.min(0.05,Math.max(0,(now-last)/1000)); last=now; const m=model();
    if(playing){ t+=dt*(+$('sp').value); if(t>=m.tend){ t=m.tend; playing=false; tog(); } dirty=true; }
    if(dirty){ dirty=false; const s=$('tt'); s.max=m.tend; s.value=Math.min(t,m.tend).toFixed(1); vlab(); draw(m); }
    requestAnimationFrame(frame); }
  function fixV(){ const vp=+$('vp').value, vs=+$('vs').value; if(vs>vp-0.5) $('vs').value=(vp-0.5).toFixed(1); }
  $('vp').addEventListener('input',fixV); $('vs').addEventListener('input',fixV);
  document.querySelectorAll('.lab-ctl input, .lab-ctl select').forEach((el)=>{ el.addEventListener('input',()=>{ dirty=true; }); el.addEventListener('change',()=>{ dirty=true; }); });
  $('tt').addEventListener('input',()=>{ playing=false; tog(); t=+$('tt').value; });
  $('st').addEventListener('change',()=>{ sel=+$('st').value; });
  $('quake').addEventListener('click',()=>{ t=0; playing=true; tog(); dirty=true; });
  $('toggle').addEventListener('click',()=>{ if(!playing && t>=model().tend-1e-6) t=0; playing=!playing; tog(); dirty=true; });
  $('rand').addEventListener('click',()=>{ ex=Math.round(rnd(15,285)); ey=Math.round(rnd(15,285)); t=0; playing=true; tog(); dirty=true; });
  function pxy(e){ const p=cpos(cv,e); return [p[0]/dpr,p[1]/dpr]; }
  function moveEpi(kx,ky){ ex=clamp(kx,4,296); ey=clamp(ky,4,296); t=0; playing=false; tog(); dirty=true; }
  function choose(i){ sel=i; $('st').value=String(i); dirty=true; }
  cv.addEventListener('pointerdown',(e)=>{ const q=pxy(e), x=q[0], y=q[1], m=model();
    if(x>=MX && x<=MX+MS && y>=MY && y<=MY+MS){ const kx=x-MX, ky=y-MY; let hit=-1, best=16; ST.forEach((s,i)=>{ const d=Math.hypot(s.x-kx,s.y-ky); if(d<best){ best=d; hit=i; } });
      if(hit>=0){ choose(hit); return; }
      dragging=true; try{ cv.setPointerCapture(e.pointerId); }catch(err){ } moveEpi(kx,ky); e.preventDefault(); return; }
    if(y>=RY && y<RY+5*RH){ choose(m.order[Math.floor((y-RY)/RH)]); return; }
    if(x>=GL-10 && x<=GR+10 && y>=GT-10 && y<=GB+10){ const g=gsc(m); let hit=-1, best=18;
      ST.forEach((s,i)=>{ const pts=g.ps?(t>=m.ts[i]?[m.ts[i]-m.tp[i]]:[]):[].concat(t>=m.tp[i]?[m.tp[i]]:[],t>=m.ts[i]?[m.ts[i]]:[]);
        pts.forEach((v)=>{ const d=Math.hypot(g.X(m.D[i])-x,g.Y(v)-y); if(d<best){ best=d; hit=i; } }); });
      if(hit>=0) choose(hit); } });
  cv.addEventListener('pointermove',(e)=>{ if(!dragging) return; const q=pxy(e); moveEpi(q[0]-MX,q[1]-MY); });
  const up=()=>{ if(dragging){ dragging=false; t=0; playing=true; tog(); dirty=true; } };
  cv.addEventListener('pointerup',up); cv.addEventListener('pointercancel',up);
  tog(); vlab(); draw(model()); requestAnimationFrame(frame);
''')
