# -*- coding: utf-8 -*-
"""理科の授業向けシミュ（光・力）：光の反射と屈折（全反射・コイン・ストロー・光ファイバー）／ばねの伸びと力（フックの法則・重さと質量）"""
import math
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

MEXT_SHO = "https://www.mext.go.jp/a_menu/shotou/new-cs/1387014.htm"
MEXT_CHU = "https://www.mext.go.jp/a_menu/shotou/new-cs/1387016.htm"
MEXT_KOU = "https://www.mext.go.jp/a_menu/shotou/new-cs/1407074.htm"
def A(url): return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, url)

# ---------------------------------------------------------------- 数値（記事の早見表は JS と同じ式で計算）
NW, NGL = 1.33, 1.50
def _r1(v): return math.floor(v * 10 + 0.5) / 10
def _deg(v): return "%.1f°" % _r1(v)
def _refr(n1, n2, a):
    s = n1 * math.sin(math.radians(a)) / n2
    return None if s > 1 else math.degrees(math.asin(s))
CRIT_W = math.degrees(math.asin(1 / NW))      # 48.75°
CRIT_G = math.degrees(math.asin(1 / NGL))     # 41.81°
def _fa(v): return "%d°" % v if float(v).is_integer() else "%.1f°" % v
IN_TABLE = T([[_fa(a), _deg(_refr(1, NW, a)), _deg(_refr(1, NGL, a))] for a in (0, 10, 20, 30, 40, 45, 50, 60, 70, 80)],
             ["入射角", "空気→水の屈折角", "空気→ガラスの屈折角"])
def _out(n, a):
    r = _refr(n, 1, a)
    return "全反射" if r is None else _deg(r)
OUT_TABLE = T([[_fa(a), _out(NW, a), _out(NGL, a)] for a in (0, 10, 20, 30, 40, 45, 50, 60)],
              ["入射角", "水→空気の屈折角", "ガラス→空気の屈折角"])

HIKARI_ARTICLE = "<h2>このシミュレーションでわかること</h2>\n" + P(
    "光が物質の境界面ではね返るとき、<b>入射角と反射角は等しく</b>なります。光が空気から水やガラスへ進むときは<b>入射角＞屈折角</b>、"
    "水やガラスから空気へ進むときは<b>入射角＜屈折角</b>となるように境界面で折れ曲がります。水やガラスから空気へ進む光は、入射角が臨界角"
    "（水 約48.8°、ガラス 約41.8°）より大きくなると、境界面ですべて反射します（<b>全反射</b>）。") + '''
<p>中学校第1学年の理科「光の反射・屈折」で学ぶ内容です。入射角を指やスライダーで変えると、反射角・屈折角が分度器の目盛りと数値で表示されます。「水の中のコインが浮いて見える」「ストローが曲がって見える」「光ファイバー」の場面も切りかえて見られます。「鏡ではね返す」では、小学校第3学年の「日光は鏡ではね返すことができる」ことも確かめられます。</p>
''' + N("対応する単元：中学校第1学年 第1分野（1）身近な物理現象（ア）光と音 ㋐光の反射・屈折（全反射も扱い、入射角と屈折角の定性的な関係に触れる）／小学校第3学年 A（3）光と音の性質（日光は直進し、集めたり反射させたりできること）／高等学校「物理」（2）波（ウ）光（屈折の法則）") + '''
<h2>授業での使い方</h2>
<h3>導入：身近な現象から問いをつくる</h3>
<p>「水の中のコインが浮いて見える」で、水を入れる前と後をくらべます。水がないとカップのふちにかくれて見えなかったコインが、水を入れると見えるようになります。「光はどこで、どのように曲がったのだろう」を問いにして、光の進み方に注目させます。小3では「鏡ではね返す」に切りかえ、はね返した光を的に当てるには鏡をどう向ければよいかを考えさせます。</p>
<h3>展開：入射角を変えて表にまとめる</h3>
<p>光源装置と半円形ガラス（台形ガラス）の実験の前後に使います。入射角を10°ずつ変えて屈折角を表に記録させると、「空気→ガラスでは屈折角が入射角より小さい」「入射角が大きくなると屈折角も大きくなる」ことが見つかります。次に「ガラス→空気」に切りかえて、光の道すじが逆向きにたどれることと、「入射角を0°から動かす」で全反射が起こるようすを確かめます。</p>
<h3>まとめ：作図と身近な道具</h3>
<p>コインやストローの場面で、目に届く光を逆向きにのばした線（点線）と、見えている物の位置の関係を作図で確かめます。光ファイバーの場面では、曲げても光が出口まで届くこと、曲げすぎると光がもれることを見せ、全反射が通信に使われていることにつなげます。</p>
<p><b>生徒への問いの例</b></p>
<ol>
<li>光が空気からガラスへ進むとき、入射角と屈折角はどちらが大きいでしょう。ガラスから空気へ進むときはどうでしょう。</li>
<li>水の中から空気へ進む光の入射角を大きくしていくと、屈折した光はどうなるでしょう。</li>
<li>水を入れたカップの底のコインが、実際より浅いところにあるように見えるのはなぜでしょう。光の道すじをかいて説明しましょう。</li>
</ol>
<h2>しくみ・解説</h2>
<h3>反射・屈折・全反射とは</h3>
<ul>
<li><b>反射</b>とは、光が物質の境界面ではね返る現象のことです。</li>
<li><b>入射角</b>とは、境界面に垂直な線（法線）と入射する光との間の角のことです。法線と反射した光との間の角を<b>反射角</b>、法線と屈折した光との間の角を<b>屈折角</b>といいます。</li>
<li><b>屈折</b>とは、光が種類のちがう物質の境界面へななめに進むとき、境界面で進む向きが変わる現象のことです。</li>
<li><b>全反射</b>とは、水やガラスから空気へ光が進むとき、入射角が臨界角より大きいと屈折する光がなくなり、光がすべて反射する現象のことです。</li>
</ul>
''' + T([["反射（鏡・水面・ガラスの表面）", "入射角＝反射角"],
          ["空気 → 水・ガラス", "入射角＞屈折角（法線に近づくように曲がる）"],
          ["水・ガラス → 空気", "入射角＜屈折角（法線から遠ざかるように曲がる）"],
          ["入射角が0°（境界面に垂直）", "曲がらずにまっすぐ進む"],
          ["水・ガラス → 空気で、入射角が臨界角より大きい", "全反射（光はすべて反射する）"]],
         ["光の進み方", "きまり"]) + '''
<h3>入射角と屈折角の早見表（空気から水・ガラスへ）</h3>
''' + IN_TABLE + '''
<h3>入射角と屈折角の早見表（水・ガラスから空気へ）</h3>
''' + OUT_TABLE + '''
<p>臨界角は、水では約48.8°、ガラスでは約41.8°です。入射角がこれより大きいと全反射になります。中学校では、入射角と屈折角のどちらが大きいか（定性的な関係）を理解できれば十分です。</p>
<h3>高校の発展：屈折の法則（スネルの法則）</h3>
<p>物質の光の曲げやすさは<b>屈折率</b>（真空を1としたときの値。空気はほぼ1.00、水は1.33、ガラスは約1.5）で表されます。屈折率 n<sub>1</sub> の物質から n<sub>2</sub> の物質へ光が進むとき、入射角 i と屈折角 r の間には次の関係があります。</p>
''' + N("n<sub>1</sub> × sin i ＝ n<sub>2</sub> × sin r<br>例：空気→水、入射角30° → sin r ＝ 1.00×0.5÷1.33 ＝ 0.376 → r ≒ 22.1°<br>臨界角 θ<sub>c</sub>（屈折率 n の物質→空気）：sin θ<sub>c</sub> ＝ 1÷n　→ 水：1÷1.33＝0.752 → 約48.8°／ガラス：1÷1.5＝0.667 → 約41.8°") + '''
<h3>水の中のコインが浮いて見える・ストローが曲がって見えるわけ</h3>
<p>コインで反射した光は、水面で法線から遠ざかるように折れ曲がってから目に届きます。私たちの目は、光がまっすぐ進んできたと感じるので、目に届いた光を逆向きにのばした線の先（点線）にコインがあるように見えます。そのため、コインは実際より浅いところに浮き上がって見えます。ストローも、水の中の部分が浮き上がって見えるので、水面のところで折れ曲がっているように見えます。</p>
''' + N("真上近くから見たとき：見かけの深さ ≒ 実際の深さ ÷ 1.33（約0.75倍）<br>例：深さ10 cmのコイン → 約7.5 cmの深さにあるように見える（ななめから見るほど、さらに浅く見える）") + '''
<p>作図の手順：①コインから水面までの光をかく → ②水面で法線から遠ざかるように折れ曲がって目に届く光をかく → ③目に届いた光を水の中へ逆向きにのばし（点線）、コインの真上を通る線と交わる点が見かけの位置です。このシミュレーションも、この作図のしかたで見かけの位置を描いています。</p>
<h3>光ファイバー</h3>
<p>光ファイバーは、光を通しやすいガラスなどでできた細い線です。中に入った光は、側面に臨界角より大きい入射角で当たるため、全反射をくり返して、曲がった線の中でも遠くまで届きます。インターネットなどの通信や、体の中を見る内視鏡（胃カメラ）に使われています。曲げすぎると側面への入射角が臨界角より小さくなり、光が外へもれます。</p>
<h3>このシミュレーションで単純化していること</h3>
<ul>
<li>屈折率は、水1.33、ガラス1.50、空気1.00としています。実際のガラスは種類によって約1.4〜1.9とちがい、同じ物質でも光の色（波長）によって少しずつちがいます（このため、プリズムで白色光がいろいろな色に分かれます）。</li>
<li>屈折が起こるときも、境界面では光の一部が反射しています。反射した光の明るさは、高校・大学で学ぶフレネルの式で計算した割合（目安）で表しています。入射角が小さいときは、空気と水の境界で約2%、空気とガラスの境界で約4%だけが反射します。</li>
<li>コイン・ストローの見かけの位置は、上の作図の手順（目に届く光を逆向きにのばした線と、物体の真上を通る線との交点）で描いています。カップは光を通さないものとし、ストローの場面ではコップのかべによる屈折は考えていません。</li>
<li>光ファイバーは、空気中に置いたガラスの棒（屈折率1.50）として計算しています。実際の光ファイバーは、中心のコアを、屈折率が少し小さいクラッドでつつんだつくりになっています。</li>
<li>強い光を直接目で見たり、鏡ではね返した日光を人の顔に当てたりしないよう、実験では注意しましょう。</li>
</ul>
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「中学校学習指導要領（平成29年告示）解説 理科編」第1分野（1）身近な物理現象（ア）光と音　''' + A(MEXT_CHU) + '''</li>
<li>文部科学省「小学校学習指導要領（平成29年告示）解説 理科編」第3学年 A（3）光と音の性質　''' + A(MEXT_SHO) + '''</li>
<li>文部科学省「高等学校学習指導要領（平成30年告示）解説 理科編 理数編」物理（2）波　''' + A(MEXT_KOU) + '''</li>
<li>中学校理科の教科書（東京書籍「新しい科学」1年、啓林館「未来へひろがるサイエンス」1年 など）の「光の反射・屈折」の単元</li>
<li>国立天文台 編「理科年表」（水の屈折率 約1.33）</li>
</ul>
'''

HIKARI_FAQS = [
    ("入射角と屈折角は、どちらが大きくなりますか？", "光が空気から水やガラスへ進むときは、入射角のほうが大きく（入射角＞屈折角）なります。反対に、水やガラスから空気へ進むときは、屈折角のほうが大きく（入射角＜屈折角）なります。入射角が0°（境界面に垂直）のときは、光は曲がらずにまっすぐ進みます。"),
    ("全反射は、どんなときに起こりますか？", "光が水やガラスから空気へ進むときに、入射角が臨界角より大きいと起こります。臨界角は水で約48.8°、ガラスで約41.8°です。空気から水やガラスへ進むときには、全反射は起こりません。"),
    ("反射角は、いつも入射角と同じですか？", "はい。鏡でも水面でもガラスの表面でも、光が反射するときは入射角と反射角が等しくなります。これを反射の法則といいます。角度は、境界面ではなく、境界面に垂直な線（法線）からはかります。"),
    ("水の中のコインが浮き上がって見えるのはなぜですか？", "コインからの光が、水面で法線から遠ざかるように屈折して目に届くからです。目は光がまっすぐ来たと感じるので、光を逆向きにのばした線の先にコインがあるように見え、実際より浅く見えます。真上近くから見ると、深さはおよそ0.75倍（1÷1.33）に見えます。"),
    ("光ファイバーは、なぜ曲がっていても光を届けられるのですか？", "ファイバーの中を進む光が、側面に臨界角より大きい入射角で当たり、全反射をくり返して進むからです。光がほとんど外にもれないので、遠くまで届きます。ただし、曲げすぎると入射角が臨界角より小さくなり、光がもれてしまいます。"),
    ("屈折率とは何ですか？中学で覚える必要はありますか？", "屈折率は、物質が光をどれだけ曲げるかを表す数で、空気はほぼ1.00、水は1.33、ガラスは約1.5です。屈折率と屈折の法則（n₁ sin i ＝ n₂ sin r）は高校の物理で学ぶ内容で、中学校では入射角と屈折角の大小の関係を理解すれば十分です。"),
]

HIKARI_JS = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const FF='"Hiragino Sans","Hiragino Kaku Gothic ProN","Noto Sans JP","Yu Gothic UI","Yu Gothic",Meiryo,sans-serif';
  const D=Math.PI/180, NI={air:1.00,water:1.33,glass:1.50}, NG=1.50, NW=1.33;
  const MED={aw:['air','water'],ag:['air','glass'],wa:['water','air'],ga:['glass','air'],mir:['air','mirror']};
  const JP={air:'空気',water:'水',glass:'ガラス',mirror:'鏡'};
  const BGC={air:'#ffffff',water:'#dbeafe',glass:'#d1f0ea'};
  const C={inc:'#e11d48',ref:'#7c3aed',tra:'#2563eb',ink:'#0f172a',sub:'#475569',crit:'#c2410c'};
  const OX=320, OY=212, PR=148, BAND=H-56;
  const CUP={l:140,r:420,b:380,rim:165,ws:185,s:19.1}, COIN={x:230,y:376};
  const GL={l:170,r:470,b:384,rim:120,ws:190,s:20}, Q0={x:290,y:190};
  const FB={x0:110,xc:440,yb:110,hw:18};
  const E1d={x:560,y:50}, E2d={x:600,y:50};
  let E1={x:E1d.x,y:E1d.y}, E2={x:E2d.x,y:E2d.y}, water=true, sweep=false, sv=0, dirty=true, down=false, last=0;
  const fd=v=>{ const r=Math.round(v*10)/10; return Math.abs(r-Math.round(r))<1e-9?String(Math.round(r)):r.toFixed(1); };
  const f1=v=>(Math.round(v*10)/10).toFixed(1);
  const fld=id=>$(id).closest('.field');
  const K=id=>$(id).previousElementSibling;
  function sh(id,m,sub){ const e=$(id); if(e) e.innerHTML=m+(sub?'<span style="display:block;font-size:12px;font-weight:700;color:#59616c;margin-top:2px">'+sub+'</span>':''); }
  function tx(s,x,y,size,col,align,bold,halo){ ctx.font=(bold?'bold ':'')+size+'px '+FF; ctx.textAlign=align||'left'; if(halo){ ctx.lineJoin='round'; ctx.lineWidth=4; ctx.strokeStyle='rgba(255,255,255,0.92)'; ctx.strokeText(s,x,y); } ctx.fillStyle=col; ctx.fillText(s,x,y); return ctx.measureText(s).width; }
  function fitT(s,x,y,maxW,size,col,align,bold,halo){ let z=size; ctx.font=(bold?'bold ':'')+z+'px '+FF; while(ctx.measureText(s).width>maxW&&z>10){ z-=0.5; ctx.font=(bold?'bold ':'')+z+'px '+FF; } tx(s,x,y,z,col,align,bold,halo); }
  function rr(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
  function line(x1,y1,x2,y2,col,w,dash){ ctx.strokeStyle=col; ctx.lineWidth=w||1; ctx.setLineDash(dash||[]); ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2,y2); ctx.stroke(); ctx.setLineDash([]); }
  function beam(x1,y1,x2,y2,a,w,arrow){ a=clamp(a,0,1); if(a<0.02) return; ctx.lineCap='round';
    line(x1,y1,x2,y2,'rgba(251,113,133,'+(0.35*a).toFixed(3)+')',w+6); line(x1,y1,x2,y2,'rgba(225,29,72,'+a.toFixed(3)+')',w);
    if(arrow){ const L=Math.hypot(x2-x1,y2-y1); if(L<36) return; const mx=x1+(x2-x1)*0.55, my=y1+(y2-y1)*0.55, an=Math.atan2(y2-y1,x2-x1);
      ctx.save(); ctx.translate(mx,my); ctx.rotate(an); ctx.fillStyle='rgba(225,29,72,'+Math.max(0.45,a).toFixed(3)+')'; ctx.beginPath(); ctx.moveTo(9,0); ctx.lineTo(-7,-7); ctx.lineTo(-7,7); ctx.closePath(); ctx.fill(); ctx.restore(); } }
  function box(x,y,w,h,title,val,col){ ctx.fillStyle='rgba(255,255,255,0.95)'; ctx.strokeStyle=col; ctx.lineWidth=2; rr(x,y,w,h,10); ctx.fill(); ctx.stroke(); fitT(title,x+10,y+17,w-16,12,col,'left',true); fitT(val,x+10,y+h-9,w-16,22,C.ink,'left',true); }
  function band(l1,c1,l2){ ctx.fillStyle='#ffffff'; ctx.fillRect(0,BAND,W,H-BAND); line(0,BAND,W,BAND,'#cbd5e1',1); fitT(l1,12,BAND+23,W-24,16,c1,'left',true); fitT(l2,12,BAND+45,W-24,13,C.sub,'left',false); }
  function refr(n1,n2,i){ const s=n1*Math.sin(i)/n2; return s>1?null:Math.asin(s); }
  function fres(n1,n2,i){ const t=refr(n1,n2,i); if(t===null) return 1; const ci=Math.cos(i), ct=Math.cos(t);
    const rs=Math.pow((n1*ci-n2*ct)/(n1*ci+n2*ct),2), rp=Math.pow((n1*ct-n2*ci)/(n1*ct+n2*ci),2); return (rs+rp)/2; }
  function eyeIcon(E,Tg){ const an=Math.atan2(Tg.y-E.y,Tg.x-E.x);
    ctx.strokeStyle='rgba(14,116,144,0.45)'; ctx.lineWidth=1.5; ctx.setLineDash([3,4]); ctx.beginPath(); ctx.arc(E.x,E.y,24,0,7); ctx.stroke(); ctx.setLineDash([]);
    ctx.save(); ctx.translate(E.x,E.y); ctx.rotate(an); ctx.fillStyle='#fff'; ctx.strokeStyle='#0f172a'; ctx.lineWidth=2;
    ctx.beginPath(); ctx.moveTo(-15,0); ctx.quadraticCurveTo(0,-13,15,0); ctx.quadraticCurveTo(0,13,-15,0); ctx.closePath(); ctx.fill(); ctx.stroke();
    ctx.fillStyle='#0e7490'; ctx.beginPath(); ctx.arc(5,0,5.5,0,7); ctx.fill(); ctx.fillStyle='#0f172a'; ctx.beginPath(); ctx.arc(6,0,2.5,0,7); ctx.fill(); ctx.restore();
    tx('目',E.x,E.y-30,13,C.ink,'center',true,true); }
  function coin(x,y,al,dash){ ctx.globalAlpha=al; ctx.fillStyle='#eab308'; ctx.strokeStyle='#a16207'; ctx.lineWidth=2; ctx.setLineDash(dash?[4,3]:[]);
    ctx.beginPath(); ctx.ellipse(x,y,18,5,0,0,7); ctx.fill(); ctx.stroke(); ctx.setLineDash([]); ctx.globalAlpha=1; }
  // 水中の点Q→水面の点P→目E と屈折して届く P を求める（n×sin(水中の角)＝sin(空気中の角)）
  function solveP(Q,E,ys,n){ let lo=Math.min(Q.x,E.x), hi=Math.max(Q.x,E.x); if(hi-lo<1e-6) return Q.x;
    const f=px=>n*(px-Q.x)/Math.hypot(px-Q.x,ys-Q.y)-(E.x-px)/Math.hypot(E.x-px,E.y-ys);
    for(let i=0;i<50;i++){ const m=(lo+hi)/2; if(f(m)>0) hi=m; else lo=m; } return (lo+hi)/2; }
  // 見かけの位置：目に届く光を逆向きにのばした線と、物体の真上を通る線との交点（教科書の作図）
  function appY(Q,px,E,ys,n){ if(Math.abs(Q.x-px)<0.5||Math.abs(px-E.x)<0.5) return ys+(Q.y-ys)/n; return ys+(Q.x-px)*(ys-E.y)/(px-E.x); }
  function wallHit(A,B,cup){ let best=null; [cup.l,cup.r].forEach(wx=>{ if((A.x-wx)*(B.x-wx)<0){ const t=(wx-A.x)/(B.x-A.x), y=A.y+t*(B.y-A.y); if(y>cup.rim&&(!best||t<best.t)) best={x:wx,y:y,t:t}; } }); return best; }
  function cross(x,y){ line(x-8,y-8,x+8,y+8,'#0f172a',3); line(x-8,y+8,x+8,y-8,'#0f172a',3); }

  // ================= 入射角を変えて調べる
  function calcRay(){ const k=$('med').value, m=MED[k], th=+$('ang').value*D, n1=NI[m[0]], mir=m[1]==='mirror', n2=mir?null:NI[m[1]];
    const t=mir?null:refr(n1,n2,th), tir=!mir&&t===null, R=mir?1:fres(n1,n2,th), crit=(!mir&&n1>n2)?Math.asin(n2/n1):null;
    return {k:k,m:m,th:th,n1:n1,n2:n2,mir:mir,t:t,tir:tir,R:R,crit:crit}; }
  function protractor(half){ ctx.strokeStyle='rgba(71,85,105,0.6)'; ctx.lineWidth=1.2; ctx.beginPath(); if(half) ctx.arc(OX,OY,PR,Math.PI,2*Math.PI); else ctx.arc(OX,OY,PR,0,7); ctx.stroke();
    for(let d=0;d<360;d+=5){ if(half&&d>90&&d<270) continue; const a=d*D, ux=Math.sin(a), uy=-Math.cos(a), L=d%30===0?14:(d%10===0?9:5); ctx.lineWidth=d%30===0?1.8:1; ctx.beginPath(); ctx.moveTo(OX+ux*PR,OY+uy*PR); ctx.lineTo(OX+ux*(PR-L),OY+uy*(PR-L)); ctx.stroke(); }
    for(let d=0;d<360;d+=30){ if(half&&d>90&&d<270) continue; const a=d*D, m=d%180, lab=Math.min(m,180-m); tx(lab+'°',OX+Math.sin(a)*(PR+15),OY-Math.cos(a)*(PR+15)+4,11,C.sub,'center',true,true); } }
  function source(S){ ctx.save(); ctx.translate(S.x,S.y); ctx.rotate(Math.atan2(OY-S.y,OX-S.x)); ctx.fillStyle='#334155'; rr(-38,-11,38,22,5); ctx.fill(); ctx.fillStyle='#fde047'; ctx.fillRect(-4,-8,5,16); ctx.restore(); }
  function drawRay(r){ const th=r.th, deg=th/D;
    ctx.fillStyle=BGC[r.m[0]]; ctx.fillRect(0,0,W,OY);
    if(r.mir){ ctx.fillStyle='#f1f5f9'; ctx.fillRect(0,OY,W,BAND-OY); ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=2; for(let x=0;x<W+40;x+=16){ ctx.beginPath(); ctx.moveTo(x,OY+8); ctx.lineTo(x-24,OY+38); ctx.stroke(); } ctx.fillStyle='#94a3b8'; ctx.fillRect(0,OY,W,8); }
    else { ctx.fillStyle=BGC[r.m[1]]; ctx.fillRect(0,OY,W,BAND-OY); }
    const lab=(m,y)=>{ const w=tx(JP[m],14,y,17,C.ink,'left',true,true); if(m!=='mirror') tx('（屈折率 '+NI[m].toFixed(2)+'）',14+w+2,y,12,C.sub,'left',false,true); };
    lab(r.m[0],OY-12); lab(r.m[1],OY+(r.mir?62:28));
    tx('境界面',W-12,OY-8,12,C.sub,'right',true,true);
    protractor(r.mir);
    line(0,OY,W,OY,'#334155',2);
    line(OX,OY-PR-6,OX,r.mir?OY:OY+PR+6,'#64748b',1.5,[6,5]);
    tx('法線',OX+6,OY-PR+30,12,C.sub,'left',true,true);
    if(r.crit){ const c=r.crit, px=OX-PR*Math.sin(c), py=OY-PR*Math.cos(c); line(OX,OY,px,py,'rgba(234,88,12,0.6)',1.5,[3,4]); ctx.fillStyle='#ea580c'; ctx.beginPath(); ctx.arc(px,py,5,0,7); ctx.fill(); tx('臨界角',px-9,py-6,12,C.crit,'right',true,true); }
    const S={x:OX-188*Math.sin(th), y:OY-188*Math.cos(th)}, rl=PR+28;
    beam(S.x,S.y,OX,OY,1,3.2,true);
    const strong=r.mir||r.tir; beam(OX,OY,OX+rl*Math.sin(th),OY-rl*Math.cos(th),strong?1:0.2+0.8*Math.sqrt(r.R),strong?3.2:2.2,true);
    if(r.t!==null) beam(OX,OY,OX+rl*Math.sin(r.t),OY+rl*Math.cos(r.t),Math.max(0.45,1-r.R),3.2,true);
    source(S);
    const arc=(a0,a1,rad,col)=>{ ctx.strokeStyle=col; ctx.lineWidth=2.5; ctx.beginPath(); ctx.arc(OX,OY,rad,a0,a1); ctx.stroke(); };
    if(deg>0.5){ arc(-Math.PI/2-th,-Math.PI/2,42,C.inc); arc(-Math.PI/2,-Math.PI/2+th,46,C.ref); }
    if(r.t!==null&&r.t>0.009) arc(Math.PI/2-r.t,Math.PI/2,54,C.tra);
    if(deg>13){ const b=-Math.PI/2-th/2, b2=-Math.PI/2+th/2; tx(fd(deg)+'°',OX+Math.cos(b)*64,OY+Math.sin(b)*64+5,13,C.inc,'center',true,true); tx(fd(deg)+'°',OX+Math.cos(b2)*68,OY+Math.sin(b2)*68+5,13,C.ref,'center',true,true); }
    if(r.t!==null&&r.t/D>13){ const b3=Math.PI/2-r.t/2; tx(fd(r.t/D)+'°',OX+Math.cos(b3)*76,OY+Math.sin(b3)*76+5,13,C.tra,'center',true,true); }
    box(8,8,128,50,'入射角',fd(deg)+'°',C.inc);
    box(W-136,8,128,50,'反射角',fd(deg)+'°',C.ref);
    if(!r.mir) box(W-136,BAND-60,128,52,'屈折角',r.tir?'全反射':fd(r.t/D)+'°',C.tra);
    if(r.crit) box(8,BAND-60,150,52,'臨界角（'+JP[r.m[0]]+'→空気）',fd(r.crit/D)+'°',C.crit);
    const nm=JP[r.m[0]]+'→'+JP[r.m[1]];
    if(r.mir) band('入射角 '+fd(deg)+'° ＝ 反射角 '+fd(deg)+'°　光は鏡で同じ角度ではね返る',C.ref,'小3：日光はまっすぐ進み、鏡ではね返すことができる。光源（左上）や図をドラッグして角度を変えよう');
    else if(r.tir) band('全反射：入射角 '+fd(deg)+'° が臨界角 '+fd(r.crit/D)+'° より大きいので、光はすべてはね返る',C.crit,'光ファイバーは、この全反射をくり返して、光を遠くまで届けている');
    else if(deg<0.05) band(nm+'：入射角 0°（境界面に垂直）の光は、曲がらずにまっすぐ進む',C.ink,'光源（左上）や図をドラッグして、入射角を変えてみよう');
    else if(r.n1<r.n2) band(nm+'：入射角 '+fd(deg)+'° ＞ 屈折角 '+fd(r.t/D)+'°',C.tra,'空気から水やガラスに進む光は、境界面で法線に近づくように折れ曲がる（全反射は起こらない）');
    else band(nm+'：入射角 '+fd(deg)+'° ＜ 屈折角 '+fd(r.t/D)+'°',C.tra,JP[r.m[0]]+'から空気に進む光は、法線から遠ざかるように曲がる。入射角が臨界角 '+fd(r.crit/D)+'° をこえると全反射');
    return r; }

  // ================= 水の中のコイン
  function drawCoin(){ const cup=CUP, ws=cup.ws, E=E1;
    ctx.fillStyle='#f8fafc'; ctx.fillRect(0,0,W,BAND); ctx.fillStyle='#e7e5e4'; ctx.fillRect(0,cup.b+7,W,BAND-cup.b-7);
    if(water){ ctx.fillStyle='rgba(147,197,253,0.55)'; ctx.fillRect(cup.l,ws,cup.r-cup.l,cup.b-ws); line(cup.l,ws,cup.r,ws,'#3b82f6',2); tx('水',cup.r-12,ws+24,15,'#1d4ed8','right',true); }
    ctx.strokeStyle='#a16207'; ctx.lineWidth=7; ctx.lineCap='butt'; ctx.beginPath(); ctx.moveTo(cup.l-3.5,cup.rim); ctx.lineTo(cup.l-3.5,cup.b+3.5); ctx.lineTo(cup.r+3.5,cup.b+3.5); ctx.lineTo(cup.r+3.5,cup.rim); ctx.stroke(); ctx.lineCap='round';
    tx('カップ',cup.r+12,cup.b-24,12,C.sub,'left',true); tx('（光を通さない）',cup.r+8,cup.b-8,12,C.sub,'left',true);
    coin(COIN.x,COIN.y,1,false);
    const C0={x:COIN.x,y:COIN.y-3}; let vis=false, Ap=null, P=null, hit=null, aw=0, aa=0;
    if(water){ const px=solveP(C0,E,ws,NW);
      if(px>cup.l&&px<cup.r){ P={x:px,y:ws}; hit=wallHit(P,E,cup); if(!hit){ vis=true; Ap={x:C0.x,y:appY(C0,px,E,ws,NW)}; aw=Math.atan2(Math.abs(px-C0.x),C0.y-ws)/D; aa=Math.atan2(Math.abs(E.x-px),ws-E.y)/D; } }
      else { const wx=px<=cup.l?cup.l:cup.r, t=(wx-C0.x)/(px-C0.x); hit={x:wx,y:C0.y+t*(ws-C0.y)}; } }
    else { hit=wallHit(C0,E,cup); vis=!hit; }
    if(water&&vis){ line(P.x,ws-46,P.x,ws+46,'#64748b',1.3,[4,4]); tx('法線',P.x+5,ws-34,11,C.sub,'left',true,true);
      beam(C0.x,C0.y,P.x,P.y,1,2.6,true); beam(P.x,P.y,E.x,E.y,1,2.6,true); line(P.x,P.y,Ap.x,Ap.y,'#475569',1.6,[6,4]);
      coin(Ap.x,Ap.y+3,0.5,true); tx('うき上がって見える',Ap.x,Ap.y-12,12,'#a16207','center',true,true);
      const ga=(x,y1,y2,col,lb)=>{ line(x,y1,x,y2,col,2); ctx.fillStyle=col; [[y1,1],[y2,-1]].forEach(q=>{ ctx.beginPath(); ctx.moveTo(x,q[0]); ctx.lineTo(x-4,q[0]+7*q[1]); ctx.lineTo(x+4,q[0]+7*q[1]); ctx.closePath(); ctx.fill(); }); tx(lb,x-8,(y1+y2)/2+4,12,col,'right',true,true); };
      line(cup.l-110,ws,cup.l-8,ws,'#94a3b8',1,[2,3]); line(cup.l-38,Ap.y+3,cup.l-8,Ap.y+3,'#94a3b8',1,[2,3]); line(cup.l-18,C0.y+3,cup.l-8,C0.y+3,'#94a3b8',1,[2,3]);
      ga(cup.l-16,ws,C0.y+3,'#0f172a','実際 '+f1((C0.y+3-ws)/cup.s)+'cm'); ga(cup.l-36,ws,Ap.y+3,'#a16207','見かけ '+f1((Ap.y+3-ws)/cup.s)+'cm');
    } else if(!water&&vis){ beam(C0.x,C0.y,E.x,E.y,1,2.6,true); }
    else { const st=P||C0; if(P) beam(C0.x,C0.y,P.x,P.y,1,2.6,true); beam(st.x,st.y,hit.x,hit.y,1,2.6,false); cross(hit.x,hit.y);
      const kx=E.x>(cup.l+cup.r)/2?cup.r:cup.l; if((E.x-kx)*(kx===cup.r?1:-1)>0){ const s=(cup.b-E.y)/(cup.rim-E.y), qx=E.x+s*(kx-E.x); line(E.x,E.y,clamp(qx,cup.l,cup.r),cup.b,'#64748b',1.4,[6,5]); } }
    eyeIcon(E,P&&vis?P:C0); tx('（目はドラッグで動かせる）',clamp(E.x,78,W-78),E.y+40,11,C.sub,'center',false,true);
    tx('実際のコイン',COIN.x,COIN.y-14,12,'#a16207','center',true,true);
    const real=(C0.y+3-ws)/cup.s, app=Ap?(Ap.y+3-ws)/cup.s:null;
    if(water&&vis) band('コインは実際より浅く見える：深さ '+f1(real)+' cm → 見かけ '+f1(app)+' cm',C.tra,'水中から空気中へ出る光は、水面で法線から遠ざかるように曲がる。目は光がまっすぐ来たと感じる');
    else if(water) band('この目の位置からは、水を入れてもコインは見えない',C.ink,'目（右上）をドラッグして、コインが見える位置をさがそう');
    else if(vis) band('水がないので、コインからの光はまっすぐ目に届く（実際の位置に見える）',C.ink,'目を動かして、カップのふちでかくれる位置にしてから「水を入れる」を押してみよう');
    else band('水がないと、カップのふちにさえぎられてコインは見えない',C.ink,'「💧 水を入れる」を押すと、どうなるかな？');
    return {vis:vis,real:real,app:app,aw:aw,aa:aa}; }

  // ================= ストロー
  function strawLine(pts,al,w,col){ ctx.globalAlpha=al; ctx.lineCap='round'; ctx.lineJoin='round'; ctx.strokeStyle=col; ctx.lineWidth=w; ctx.beginPath(); pts.forEach((p,i)=>{ if(i) ctx.lineTo(p.x,p.y); else ctx.moveTo(p.x,p.y); }); ctx.stroke(); ctx.globalAlpha=1; }
  function drawStraw(){ const g=GL, ws=g.ws, E=E2, ph=+$('tilt').value*D, d={x:Math.sin(ph),y:Math.cos(ph)};
    const Lw=Math.min((g.b-12-ws)/d.y,(g.r-12-Q0.x)/Math.max(1e-6,d.x)), Lu=150;
    const top={x:Q0.x-d.x*Lu,y:Q0.y-d.y*Lu}, Tp={x:Q0.x+d.x*Lw,y:Q0.y+d.y*Lw};
    ctx.fillStyle='#f8fafc'; ctx.fillRect(0,0,W,BAND); ctx.fillStyle='#e7e5e4'; ctx.fillRect(0,g.b+6,W,BAND-g.b-6);
    ctx.fillStyle='rgba(147,197,253,0.55)'; ctx.fillRect(g.l,ws,g.r-g.l,g.b-ws); line(g.l,ws,g.r,ws,'#3b82f6',2); tx('水',g.l+12,g.b-14,15,'#1d4ed8','left',true);
    ctx.strokeStyle='rgba(100,116,139,0.8)'; ctx.lineWidth=4; ctx.beginPath(); ctx.moveTo(g.l-2,g.rim); ctx.lineTo(g.l-2,g.b+2); ctx.lineTo(g.r+2,g.b+2); ctx.lineTo(g.r+2,g.rim); ctx.stroke();
    const ap=[{x:Q0.x,y:Q0.y}]; for(let i=1;i<=24;i++){ const Q={x:Q0.x+d.x*Lw*i/24,y:Q0.y+d.y*Lw*i/24}; ap.push({x:Q.x,y:appY(Q,solveP(Q,E,ws,NW),E,ws,NW)}); }
    strawLine([Q0,Tp],0.25,11,'#ec4899'); ctx.setLineDash([6,5]); strawLine([Q0,Tp],0.9,1.5,'#9d174d'); ctx.setLineDash([]);
    strawLine([top,Q0].concat(ap.slice(1)),1,11,'#ec4899'); strawLine([top,Q0].concat(ap.slice(1)),1,3,'#fbcfe8');
    const pT=solveP(Tp,E,ws,NW), P={x:pT,y:ws}, At=ap[ap.length-1];
    line(P.x,ws-40,P.x,ws+40,'#64748b',1.3,[4,4]);
    beam(Tp.x,Tp.y,P.x,P.y,1,2.4,true); beam(P.x,P.y,E.x,E.y,1,2.4,true); line(P.x,P.y,At.x,At.y,'#475569',1.6,[6,4]);
    tx('実際のストロー（水の中）',Tp.x-8,Tp.y+2,12,'#9d174d','right',true,true);
    tx('見えるストロー',At.x+10,At.y-10,12,'#be185d','left',true,true);
    eyeIcon(E,P); tx('（目はドラッグで動かせる）',clamp(E.x,78,W-78),E.y+40,11,C.sub,'center',false,true);
    const real=(Tp.y-ws)/g.s, app=(At.y-ws)/g.s;
    band('水の中の部分が浮き上がって見えるので、ストローが水面で折れ曲がって見える',C.tra,'ストローの先：深さ '+f1(real)+' cm → 見かけ '+f1(app)+' cm（目の位置や傾きを変えてみよう）');
    return {ph:ph/D,real:real,app:app}; }

  // ================= 光ファイバー
  function fiberGeo(){ const R=120-(+$('bend').value)*10, c=[], up=[], lo=[];
    for(let i=0;i<20;i++) c.push({x:FB.x0+(FB.xc-FB.x0)*i/20,y:FB.yb});
    for(let i=0;i<=40;i++){ const a=-Math.PI/2+Math.PI*i/40; c.push({x:FB.xc+R*Math.cos(a),y:FB.yb+R+R*Math.sin(a)}); }
    for(let i=1;i<=20;i++) c.push({x:FB.xc-(FB.xc-FB.x0)*i/20,y:FB.yb+2*R});
    const n=c.length-1;
    for(let i=0;i<=n;i++){ const p=c[Math.max(0,i-1)], q=c[Math.min(n,i+1)]; let ux=q.x-p.x, uy=q.y-p.y; const l=Math.hypot(ux,uy); ux/=l; uy/=l;
      up.push({x:c[i].x+uy*FB.hw,y:c[i].y-ux*FB.hw}); lo.push({x:c[i].x-uy*FB.hw,y:c[i].y+ux*FB.hw}); }
    return {c:c,up:up,lo:lo,R:R,n:n}; }
  function hitSeg(p,d,a,b){ const ex=b.x-a.x, ey=b.y-a.y, den=d.x*ey-d.y*ex; if(Math.abs(den)<1e-12) return null; const ax=a.x-p.x, ay=a.y-p.y, t=(ax*ey-ay*ex)/den, u=(ax*d.y-ay*d.x)/den; if(u<-1e-9||u>1+1e-9) return null; return t; }
  // ガラスの中の光を追跡：側面への入射角が臨界角より大きければ全反射、小さければ外へ屈折してもれる
  function trace(G,al){ const be=Math.asin(Math.sin(al)/NG); let p={x:G.c[0].x,y:G.c[0].y}, d={x:Math.cos(be),y:Math.sin(be)}; const path=[{x:p.x,y:p.y}], bp=[]; let nb=0, minInc=90, leak=null, out=null, back=false;
    const segs=[]; for(let i=0;i<G.n;i++){ segs.push({a:G.up[i],b:G.up[i+1],k:'w'}); segs.push({a:G.lo[i],b:G.lo[i+1],k:'w'}); }
    segs.push({a:G.up[G.n],b:G.lo[G.n],k:'x'}); segs.push({a:G.up[0],b:G.lo[0],k:'b'});
    for(let it=0;it<500;it++){ let bt=1e9, bs=null;
      for(const s of segs){ const t=hitSeg(p,d,s.a,s.b); if(t!==null&&t>1e-3&&t<bt){ bt=t; bs=s; } }
      if(!bs) break;
      const q={x:p.x+d.x*bt,y:p.y+d.y*bt}; path.push(q);
      if(bs.k==='x'){ const so=NG*d.y; out={p:q,d:Math.abs(so)<=1?{x:-Math.cos(Math.asin(so)),y:so}:null}; break; }
      if(bs.k==='b'){ back=true; break; }
      const sx=bs.b.x-bs.a.x, sy=bs.b.y-bs.a.y, sl=Math.hypot(sx,sy); let nx=-sy/sl, ny=sx/sl; if(nx*d.x+ny*d.y>0){ nx=-nx; ny=-ny; }
      const ci=-(nx*d.x+ny*d.y), inc=Math.acos(clamp(ci,-1,1)); minInc=Math.min(minInc,inc/D);
      if(NG*Math.sin(inc)>1){ d={x:d.x+2*ci*nx,y:d.y+2*ci*ny}; const l=Math.hypot(d.x,d.y); d.x/=l; d.y/=l; nb++; bp.push(q); p=q; }
      else { const tt=Math.asin(NG*Math.sin(inc)); let ux=d.x+ci*nx, uy=d.y+ci*ny; const ul=Math.hypot(ux,uy)||1; ux/=ul; uy/=ul;
        leak={p:q,d:{x:-nx*Math.cos(tt)+ux*Math.sin(tt),y:-ny*Math.cos(tt)+uy*Math.sin(tt)},inc:inc/D}; break; } }
    return {path:path,bp:bp,nb:nb,minInc:minInc,leak:leak,out:out,back:back,be:be/D}; }
  function drawFiber(){ const al=+$('alpha').value*D, G=fiberGeo(), R=trace(G,al), crit=Math.asin(1/NG)/D;
    ctx.fillStyle='#f8fafc'; ctx.fillRect(0,0,W,BAND);
    ctx.fillStyle='rgba(125,211,252,0.38)'; ctx.strokeStyle='#0284c7'; ctx.lineWidth=2; ctx.beginPath(); G.up.forEach((p,i)=>{ if(i) ctx.lineTo(p.x,p.y); else ctx.moveTo(p.x,p.y); }); for(let i=G.lo.length-1;i>=0;i--) ctx.lineTo(G.lo[i].x,G.lo[i].y); ctx.closePath(); ctx.fill(); ctx.stroke();
    tx('ガラス（屈折率 1.50）',FB.xc-6,FB.yb-FB.hw-10,12,'#0369a1','right',true,true); tx('まわりは空気',W-14,BAND-12,12,C.sub,'right',true,true);
    const S={x:FB.x0-72*Math.cos(al),y:FB.yb-72*Math.sin(al)};
    beam(S.x,S.y,FB.x0,FB.yb,1,2.8,false);
    ctx.save(); ctx.translate(S.x,S.y); ctx.rotate(al); ctx.fillStyle='#334155'; rr(-34,-10,34,20,5); ctx.fill(); ctx.fillStyle='#fde047'; ctx.fillRect(-4,-7,5,14); ctx.restore();
    for(let i=1;i<R.path.length;i++) beam(R.path[i-1].x,R.path[i-1].y,R.path[i].x,R.path[i].y,1,2.6,i===1&&R.path.length>2);
    R.bp.forEach(q=>{ ctx.fillStyle='#fff'; ctx.strokeStyle='#e11d48'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.arc(q.x,q.y,3.5,0,7); ctx.fill(); ctx.stroke(); });
    if(R.bp.length){ const q=R.bp[0]; tx('全反射',q.x,q.y+(q.y<FB.yb+4?-9:20),12,'#be123c','center',true,true); }
    tx('入口',FB.x0+4,FB.yb-FB.hw-8,13,C.ink,'left',true,true);
    tx('出口',FB.x0+4,FB.yb+2*G.R+FB.hw+17,13,C.ink,'left',true,true);
    if(R.leak){ const q=R.leak.p; beam(q.x,q.y,q.x+R.leak.d.x*100,q.y+R.leak.d.y*100,0.95,2.6,true); ctx.fillStyle='rgba(251,191,36,0.45)'; ctx.beginPath(); ctx.arc(q.x,q.y,14,0,7); ctx.fill(); tx('光がもれる！',clamp(q.x+R.leak.d.x*112,50,W-50),clamp(q.y+R.leak.d.y*112+16,20,BAND-8),13,'#b45309','center',true,true); }
    else if(R.out){ const q=R.out.p; if(R.out.d) beam(q.x,q.y,q.x+R.out.d.x*60,q.y+R.out.d.y*60,1,2.6,false); const gg=ctx.createRadialGradient(q.x,q.y,2,q.x,q.y,26); gg.addColorStop(0,'rgba(253,224,71,0.9)'); gg.addColorStop(1,'rgba(253,224,71,0)'); ctx.fillStyle=gg; ctx.beginPath(); ctx.arc(q.x,q.y,26,0,7); ctx.fill(); }
    box(W-334,8,160,50,'側面での全反射',R.nb+' 回',C.inc); box(W-168,8,160,50,'側面への入射角（最小）',fd(R.minInc)+'°',C.tra);
    if(R.leak) band('曲げがきつく、側面への入射角 '+fd(R.leak.inc)+'° が臨界角 '+fd(crit)+'° より小さくなって、光がもれた',C.crit,'光ファイバーは、曲げすぎると光がもれる。「曲げのきつさ」や「光を入れる角度」を変えてみよう');
    else if(R.back||!R.out) band('光が入口のほうへもどってしまった',C.ink,'「光を入れる角度」を変えてみよう');
    else band('全反射を '+R.nb+' 回くり返して、曲がったガラスの中を光が出口まで届いた',C.tra,'側面への入射角は最小でも '+fd(R.minInc)+'° ＞ 臨界角 '+fd(crit)+'°（ガラス→空気）なので、光は外にもれない');
    return {al:al/D,be:R.be,nb:R.nb,leak:!!R.leak,minInc:R.minInc,R:G.R}; }

  // ================= 表示・統計
  function vis(){ const sc=$('scene').value, show={med:sc==='ray',ang:sc==='ray',tilt:sc==='straw',alpha:sc==='fiber',bend:sc==='fiber'};
    for(const k in show) fld(k).style.display=show[k]?'':'none';
    $('sweep').style.display=sc==='ray'?'':'none'; $('crit').style.display=(sc==='ray'&&(['wa','ga'].indexOf($('med').value)>=0))?'':'none';
    $('water').style.display=sc==='coin'?'':'none'; $('eyeR').style.display=(sc==='coin'||sc==='straw')?'':'none';
    $('water').textContent=water?'💧 水をぬく':'💧 水を入れる'; }
  function setStats(sc,I){
    if(sc==='ray'){ const r=I, deg=r.th/D, nm=JP[r.m[0]]+'→'+JP[r.m[1]];
      K('sI').innerHTML='入射角'; sh('sI',fd(deg)+'°',nm);
      K('sR').innerHTML='反射角'; sh('sR',fd(deg)+'°',r.mir?'入射角と同じ':(r.tir?'光はすべて反射':'はね返る光 約'+Math.max(1,Math.round(r.R*100))+'%'));
      K('sT').innerHTML='屈折角'; if(r.mir) sh('sT','なし','光は鏡を通りぬけない'); else if(r.tir) sh('sT','全反射','屈折する光がない'); else sh('sT',fd(r.t/D)+'°',deg<0.05?'曲がらない':(r.t<r.th?'入射角より小さい':'入射角より大きい'));
      if(r.crit){ K('sC').innerHTML='臨界角'; sh('sC',fd(r.crit/D)+'°','こえると全反射'); }
      else if(r.mir){ K('sC').innerHTML='反射のきまり'; sh('sC','等しい','入射角＝反射角'); }
      else { K('sC').innerHTML='屈折率'; sh('sC',NI[r.m[0]].toFixed(2)+' → '+NI[r.m[1]].toFixed(2),'全反射は起こらない'); }
      if(r.mir) setShare('【光の反射】入射角'+fd(deg)+'°の光は、鏡で反射角'+fd(deg)+'°ではね返る（入射角＝反射角）｜シミュラボ');
      else if(r.tir) setShare('【全反射】'+nm+'で入射角'+fd(deg)+'°は臨界角'+fd(r.crit/D)+'°より大きいので、光はすべて反射する｜シミュラボ');
      else setShare('【光の屈折】'+nm+'で入射角'+fd(deg)+'°のとき、屈折角は'+fd(r.t/D)+'°（入射角'+(r.t<r.th?'＞':(r.t>r.th?'＜':'＝'))+'屈折角）。反射角は'+fd(deg)+'°｜シミュラボ');
    } else if(sc==='coin'){
      K('sI').innerHTML='実際の深さ'; sh('sI',f1(I.real)+' cm','水面からコインまで');
      K('sR').innerHTML='見かけの深さ'; if(water&&I.vis) sh('sR',f1(I.app)+' cm','実際の約'+(Math.round(I.app/I.real*100)/100)+'倍'); else sh('sR',I.vis?f1(I.real)+' cm':'見えない',I.vis?'水がないので実際の位置':'');
      K('sT').innerHTML='水面での角度'; if(water&&I.vis) sh('sT',fd(I.aw)+'°→'+fd(I.aa)+'°','水中→空気中'); else sh('sT',water?'見えない':'水なし','');
      K('sC').innerHTML='見え方'; sh('sC',water&&I.vis?'浮いて見える':(I.vis?'実際の位置':'見えない'),water?'水あり':'水なし');
      setShare(water&&I.vis?'【光の屈折】深さ'+f1(I.real)+'cmの水の底のコインは、約'+f1(I.app)+'cmの深さに浮き上がって見える｜シミュラボ':'【光の屈折】水を入れると、カップのふちにかくれていたコインが見えるようになる？｜シミュラボ');
    } else if(sc==='straw'){
      K('sI').innerHTML='ストローの傾き'; sh('sI',fd(I.ph)+'°','真下の向きから');
      K('sR').innerHTML='先の実際の深さ'; sh('sR',f1(I.real)+' cm','');
      K('sT').innerHTML='先の見かけの深さ'; sh('sT',f1(I.app)+' cm','実際の約'+(Math.round(I.app/I.real*100)/100)+'倍');
      K('sC').innerHTML='見え方'; sh('sC','折れて見える','水の中が浮き上がる');
      setShare('【光の屈折】水に入れたストローは、水の中の部分が浮き上がって見えるので折れ曲がって見える（先の深さ'+f1(I.real)+'cm→見かけ'+f1(I.app)+'cm）｜シミュラボ');
    } else {
      K('sI').innerHTML='光を入れる角度'; sh('sI',fd(I.al)+'°','入口の面の法線から');
      K('sR').innerHTML='ガラスの中の角度'; sh('sR',fd(I.be)+'°','入口で屈折した後');
      K('sT').innerHTML='全反射の回数'; sh('sT',I.nb+' 回','側面で');
      K('sC').innerHTML='結果'; sh('sC',I.leak?'途中でもれる':'出口まで届く',I.leak?'曲げがきつすぎる':'臨界角 '+fd(Math.asin(1/NG)/D)+'°');
      setShare('【光ファイバーと全反射】光を'+fd(I.al)+'°で入れると、'+(I.leak?'曲げすぎて途中で光がもれた':'全反射を'+I.nb+'回くり返して出口まで届いた')+'｜シミュラボ'); } }
  function render(){ const sc=$('scene').value; ctx.clearRect(0,0,W,H); let I;
    if(sc==='ray') I=drawRay(calcRay()); else if(sc==='coin') I=drawCoin(); else if(sc==='straw') I=drawStraw(); else I=drawFiber();
    setStats(sc,I); }

  // ================= 操作
  ['scene','med','ang','tilt','alpha','bend'].forEach(id=>{ $(id).addEventListener('input',()=>{ if(id==='scene'||id==='med') vis(); if(id!=='ang') sweep=false; dirty=true; }); $(id).addEventListener('change',()=>{ vis(); dirty=true; }); });
  const bendL=()=>{ const v=+$('bend').value; $('bendL').textContent=v+' / 10'+(v<=2?'（ゆるい）':v>=8?'（きつい）':''); };
  $('bend').addEventListener('input',bendL); bendL();
  function setAng(v){ $('ang').value=(Math.round(v*10)/10).toFixed(1); $('ang').dispatchEvent(new Event('input')); }
  $('sweep').addEventListener('click',()=>{ if(sweep){ sweep=false; $('sweep').textContent='▶ 入射角を0°から動かす'; return; } sweep=true; sv=0; setAng(0); $('sweep').textContent='■ 止める'; });
  $('crit').addEventListener('click',()=>{ const r=calcRay(); if(r.crit){ sweep=false; $('sweep').textContent='▶ 入射角を0°から動かす'; setAng(Math.floor(r.crit/D*10)/10-0.1); } });
  $('water').addEventListener('click',()=>{ water=!water; vis(); dirty=true; });
  $('eyeR').addEventListener('click',()=>{ E1={x:E1d.x,y:E1d.y}; E2={x:E2d.x,y:E2d.y}; dirty=true; });
  function pt(e){ const p=cpos(cv,e); return {x:p[0]/dpr,y:p[1]/dpr}; }
  function act(q){ const sc=$('scene').value;
    if(sc==='ray'){ if(q.y>BAND) return; const dx=q.x-OX, dy=q.y-OY; if(Math.hypot(dx,dy)<14) return; sweep=false; $('sweep').textContent='▶ 入射角を0°から動かす'; setAng(clamp(Math.atan2(Math.abs(dx),Math.abs(dy))/D,0,89)); }
    else if(sc==='coin'){ E1={x:clamp(q.x,18,W-18),y:clamp(q.y,40,CUP.rim-16)}; dirty=true; }
    else if(sc==='straw'){ E2={x:clamp(q.x,18,W-18),y:clamp(q.y,40,GL.rim-16)}; dirty=true; }
    else { const dx=FB.x0-q.x, dy=FB.yb-q.y; if(dx>4){ $('alpha').value=Math.round(clamp(Math.atan2(Math.abs(dy),dx)/D,0,30)); $('alpha').dispatchEvent(new Event('input')); } } }
  cv.addEventListener('pointerdown',e=>{ down=true; try{ cv.setPointerCapture(e.pointerId); }catch(_){ } act(pt(e)); e.preventDefault(); });
  cv.addEventListener('pointermove',e=>{ if(down) act(pt(e)); });
  ['pointerup','pointercancel','pointerleave'].forEach(t=>cv.addEventListener(t,()=>{ down=false; }));
  function frame(t){ const dt=last?Math.min(0.05,(t-last)/1000):0; last=t;
    if(sweep){ sv=Math.min(89,sv+12*dt); setAng(sv); if(sv>=89){ sweep=false; $('sweep').textContent='▶ 入射角を0°から動かす'; } }
    if(dirty){ dirty=false; render(); }
    requestAnimationFrame(frame); }
  vis(); render(); dirty=false; requestAnimationFrame(frame);
'''

sim(slug="hikari-kussetsu", cat="rika", emoji="🔦", score=78,
    title="光の反射と屈折シミュレーター（入射角・屈折角・全反射）",
    title_tag="光の屈折・反射のシミュレーター｜入射角と屈折角・全反射を分度器で確かめる（中1 光と音）",
    meta_desc="入射角を指でドラッグすると、反射角・屈折角が分度器の目盛りと数値でわかる無料シミュレーター。空気→水・ガラス、水・ガラス→空気を切りかえて全反射と臨界角も確認できます。水の中のコインが浮いて見える、ストローが曲がって見える、光ファイバーの作図つき。中1理科「光の反射・屈折」の授業に。",
    og_title="光の反射と屈折シミュレーター（入射角・屈折角・全反射）",
    og_desc="入射角を変えると反射角・屈折角が分度器で見える。全反射・臨界角、浮いて見えるコイン、光ファイバーも。中1「光と音」の授業向け。",
    card_desc="入射角を指で動かすと反射角・屈折角が分度器でわかる。全反射、浮いて見えるコイン、光ファイバーも。",
    lead="光源や図を指でドラッグして入射角を変えると、反射角と屈折角が分度器の目盛りと数値で表示されます。空気→水、空気→ガラス、水→空気、ガラス→空気を切りかえると、入射角と屈折角の大小や全反射が確かめられます。「水の中のコイン」「ストロー」「光ファイバー」の場面も選べます。",
    model="中1 光の反射・屈折（全反射）／小3 光の性質",
    level="中学1年、小学3年、高校（物理）",
    unit="中学校 第1分野（1）身近な物理現象（ア）光と音 ㋐光の反射・屈折／小学校 第3学年 A（3）光と音の性質",
    canvas=canvas(640, 460, light=True),
    controls=select("scene", "場面", [("ray", "入射角を変えて調べる"), ("coin", "水の中のコインが浮いて見える"), ("straw", "ストローが曲がって見える"), ("fiber", "光ファイバー（全反射）")])
           + select("med", "光の進む向き", [("aw", "空気 → 水"), ("ag", "空気 → ガラス"), ("wa", "水 → 空気"), ("ga", "ガラス → 空気"), ("mir", "鏡ではね返す（小3）")])
           + slider("ang", "入射角", 0, 89, 40, 0.1, "{v}°")
           + slider("tilt", "ストローの傾き（真下から）", 15, 70, 40, 1, "{v}°")
           + slider("alpha", "光を入れる角度", 0, 30, 6, 1, "{v}°")
           + slider("bend", "曲げのきつさ", 0, 10, 4, 1, "{v}"),
    buttons=btn("sweep", "▶ 入射角を0°から動かす", True) + btn("crit", "臨界角の手前にする") + btn("water", "💧 水をぬく") + btn("eyeR", "目の位置をもどす"),
    stats=stats([("sI", "入射角", False), ("sR", "反射角", False), ("sT", "屈折角", True), ("sC", "臨界角", False)]),
    legend="赤い線＝光の道すじ（矢印は進む向き）。角度は、境界面に垂直な線（法線・点線）からはかります。入射角＝赤、反射角＝むらさき、屈折角＝青。屈折が起こるときも光の一部は反射するので、反射した光をうすく描いています。コイン・ストローの場面では、目を指でドラッグできます（灰色の点線＝目に届いた光を逆向きにのばした線）。",
    article=HIKARI_ARTICLE, faqs=HIKARI_FAQS,
    rel=[("totsu-lens", "🔍", "凸レンズの像（作図）"), ("double-slit", "⚛️", "ダブルスリット実験"), ("wave", "🌊", "波の干渉シミュレーター"), ("taiyou-ugoki", "🌞", "太陽の動き")],
    js=HIKARI_JS)


# ============================================================ 2 ばねの伸びと力
def _fN(v):
    s = "%.2f" % (math.floor(v * 100 + 0.5) / 100)
    return s.rstrip("0").rstrip(".")
BANE_TABLE = T([["%d g" % m, "%s N" % _fN(m / 100), "%.1f cm" % _r1(5 * m / 100), "%.1f cm" % _r1(2.5 * m / 100), "約%s N" % _fN(m / 100 / 6)]
                for m in (20, 40, 60, 80, 100, 200, 300)],
               ["おもりの質量", "重さ（地球）", "ばねA（1 Nで5 cm）ののび", "ばねB（1 Nで2.5 cm）ののび", "月面での重さ"])

BANE_ARTICLE = "<h2>このシミュレーションでわかること</h2>\n" + P(
    "ばねののびは、ばねに加える力の大きさに<b>比例</b>します（<b>フックの法則</b>）。力の大きさを横軸、ばねののびを縦軸にとると、グラフは<b>原点を通る直線</b>になり、"
    "やわらかいばねほど直線の傾きが大きくなります。月面では、同じおもりでも重さ（重力）が約6分の1になるので、のびも約6分の1になりますが、<b>質量は変わりません</b>。") + '''
<p>中学校第1学年の理科「力の働き」で学ぶ内容です。おもりの数と、ばねの強さ（1 Nの力で何cmのびるか）を変えると、ばねがのびて、測定した点が力とのびのグラフに打たれていきます。2本のばねをくらべたり、弾性の限界をこえて元にもどらなくなるようすを見たりすることもできます。</p>
''' + N("対応する単元：中学校第1学年 第1分野（1）身近な物理現象（イ）力の働き ㋐力の働き（ばねに加える力の大きさとばねの伸びとの関係、重さと質量との違い、力の単位ニュートン、2力のつり合い）／高等学校「物理基礎」（1）（イ）様々な力とその働き（フックの法則）") + '''
<h2>授業での使い方</h2>
<h3>導入：予想を立てる</h3>
<p>「おもりを2個、3個とふやしていくと、ばねののびはどうなるだろう」と予想させてから、おもりを1個ずつつるします。おもりを1個ふやすごとに、のびが同じだけふえることに気づかせます。左の図をタップしても、おもりが1個ふえます。</p>
<h3>展開：グラフに表してきまりを見つける</h3>
<p>ばねばかりやばねを使った実験の前後に使います。「測定のずれ：あり」にすると、実際の実験のように点が少しずつずれます。点を折れ線で結ぶのではなく、点の並びの真ん中を通る直線を引くことを、「直線を引く」ボタンで確かめられます。ばねAとばねBの強さを変えて、直線の傾きのちがいもくらべます。</p>
<h3>まとめ：重さと質量・弾性の限界</h3>
<p>「月面で調べる」を押すと、同じおもりなのにばねののびが約6分の1になります。「ばねばかりではかる重さは場所で変わるが、てんびんではかる質量は変わらない」ことを確かめます。また、100 gのおもりを使ってやわらかいばねを大きくのばすと、弾性の限界をこえて、おもりをはずしても元の長さにもどらなくなるようすが見られます。</p>
<p><b>生徒への問いの例</b></p>
<ol>
<li>0.2 Nの力で1 cmのびるばねに、0.6 Nの力を加えると何cmのびるでしょう。（答え：3 cm）</li>
<li>グラフで、点を折れ線で結ばずに直線を引くのはなぜでしょう。</li>
<li>質量60 gのおもりを月面でばねにつるすと、ばねののびと、おもりの質量はどうなるでしょう。</li>
</ol>
<h2>しくみ・解説</h2>
<h3>力・重さ・質量とは</h3>
<ul>
<li><b>フックの法則</b>とは、ばねののびが、ばねに加える力の大きさに比例するという法則です。</li>
<li><b>重さ</b>とは、物体にはたらく重力の大きさのことで、単位はニュートン（記号 N）です。ばねばかりではかります。</li>
<li><b>質量</b>とは、物体そのものの量のことで、場所によって変わらず、単位はgやkgです。上皿てんびんや電子てんびんではかります。</li>
<li><b>1 N</b>とは、質量が約100 gの物体にはたらく重力の大きさです。</li>
<li><b>弾性</b>とは、変形した物体が元にもどろうとする性質のことです。力を加えすぎて元にもどらなくなる限度を<b>弾性の限界</b>といいます。</li>
</ul>
''' + N("ばねののび〔cm〕＝ 1 Nあたりののび〔cm/N〕× ばねに加えた力〔N〕<br>おもりの重さ〔N〕≒ 質量〔g〕÷ 100（地球上）<br>月面での重さ ≒ 地球での重さ × 1/6（質量は同じ）") + '''
<h3>早見表（おもりの質量と重さ・ばねののび）</h3>
''' + BANE_TABLE + '''
<h3>計算問題の解き方</h3>
<p>例：0.3 Nの力で1.5 cmのびるばねがあります。</p>
<ol>
<li>0.9 Nの力を加えたときののび：力が 0.9÷0.3＝3倍 なので、のびも3倍 → 1.5×3＝4.5 cm</li>
<li>6 cmのばすのに必要な力：1 cmあたり 0.3÷1.5＝0.2 N なので → 0.2×6＝1.2 N</li>
<li>質量120 gのおもりをつるしたときののび：重さは 120÷100＝1.2 N → 上の2. より 6 cm</li>
</ol>
<h3>2力のつり合い</h3>
<p>おもりが止まっているとき、おもりには下向きの重力と、ばねが上向きに引く力がはたらいていて、2つの力はつり合っています。図の矢印のように、2力がつり合う条件は「<b>大きさが等しい</b>」「<b>向きが反対</b>」「<b>一直線上にある</b>」の3つです。だから、ばねののびで、おもりにはたらく重力の大きさ（重さ）をはかることができます。</p>
<h3>グラフのかき方と誤差</h3>
<p>測定値には必ず誤差（ずれ）がふくまれます。そのため、点を折れ線で結ぶのではなく、点の並びの真ん中を通るように、なめらかな線（ここでは原点を通る直線）を引きます。直線になったことから、ばねののびは力の大きさに比例するとわかります。このシミュレーションの「直線を引く」は、原点を通る直線のうち、点からのずれがいちばん小さくなる直線（最小二乗法）を引いています。</p>
<h3>高校の発展：ばね定数</h3>
<p>高校の物理基礎では、ばねの弾性力の大きさ F〔N〕と、ばねののび x〔m〕の関係を <b>F＝kx</b> と表し、k を<b>ばね定数</b>〔N/m〕といいます。1 Nで5 cm（0.05 m）のびるばねのばね定数は 1÷0.05＝20 N/m です。ばね定数が大きいほど、のびにくい（かたい）ばねです。</p>
<h3>このシミュレーションで単純化していること</h3>
<ul>
<li>教科書にならって、質量100 gの物体にはたらく重力を1 Nとしています。正確には、地球上で約0.98 N（重力加速度 9.8 m/s²）です。</li>
<li>月面の重力は地球の約6分の1（月面の重力加速度 約1.6 m/s²）としています。</li>
<li>ばねの重さや、ばねがのび始めるまでの小さな力は考えていません。</li>
<li>弾性の限界は、どのばねも「のびが16 cmをこえたとき」としています。こえたあとは、のびが急に大きくなり、おもりをはずしても元の長さにもどらないように描いています。実際のばねの弾性の限界は、ばねの材料や太さによってちがいます。実験では、ばねを大きくのばしすぎないようにしましょう。</li>
<li>「測定のずれ：あり」では、のびの読み取りに ±0.4 cm以内のずれをランダムに加えています。</li>
</ul>
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「中学校学習指導要領（平成29年告示）解説 理科編」第1分野（1）身近な物理現象（イ）力の働き　''' + A(MEXT_CHU) + '''</li>
<li>文部科学省「高等学校学習指導要領（平成30年告示）解説 理科編 理数編」物理基礎　''' + A(MEXT_KOU) + '''</li>
<li>中学校理科の教科書（東京書籍「新しい科学」1年、啓林館「未来へひろがるサイエンス」1年 など）の「力の働き」の単元</li>
<li>国立天文台 編「理科年表」（重力加速度、月の重力）</li>
</ul>
'''

BANE_FAQS = [
    ("ばねののびと力の大きさには、どんな関係がありますか？", "ばねののびは、ばねに加える力の大きさに比例します。これをフックの法則といいます。たとえば、0.2 Nで1 cmのびるばねは、0.4 Nで2 cm、0.6 Nで3 cmのびます。力の大きさとのびのグラフは、原点を通る直線になります。"),
    ("1 N（ニュートン）はどれくらいの力ですか？", "質量が約100 gの物体にはたらく重力の大きさが、およそ1 Nです。20 gのおもりなら約0.2 N、50 gなら約0.5 Nです。正確には、100 gの物体にはたらく重力は地球上で約0.98 Nです。"),
    ("重さと質量のちがいは何ですか？", "重さは物体にはたらく重力の大きさで、単位はN（ニュートン）、ばねばかりではかり、場所によって変わります。質量は物体そのものの量で、単位はgやkg、てんびんではかり、どこでも変わりません。月面では、重さは地球の約6分の1になりますが、質量は同じです。"),
    ("月面でばねにおもりをつるすと、のびはどうなりますか？", "月面では重力が地球の約6分の1なので、同じおもりでもばねを引く力（重さ）が約6分の1になり、ばねののびも約6分の1になります。おもりの質量は変わらないので、てんびんではかると地球と同じ値になります。"),
    ("弾性の限界をこえると、どうなりますか？", "ばねを大きくのばしすぎて弾性の限界をこえると、力とのびが比例しなくなり、おもりをはずしても元の長さにもどらなくなります。グラフでは、それまでの直線から点がはずれていきます。"),
    ("グラフをかくとき、点を折れ線で結ばないのはなぜですか？", "測定値には必ず誤差（ずれ）がふくまれるからです。点の並びの真ん中を通るように直線（または、なめらかな曲線）を引くと、ばねののびと力の本当の関係がわかります。ばねの実験では、原点を通る直線になります。"),
]

BANE_JS = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const FF='"Hiragino Sans","Hiragino Kaku Gothic ProN","Noto Sans JP","Yu Gothic UI","Yu Gothic",Meiryo,sans-serif';
  const S=10, TOPY=34, Y0=98, XR=160, XA=86, XB=234, XMAX=24, XL=16, DH=7, BAND=H-34;
  const GX=374, GY=384, GW=248, GH=206;
  const COL={A:'#2563eb',B:'#ea580c'}, INK='#0f172a', SUB='#475569', RED='#dc2626', GRN='#16a34a';
  const SP={A:{Fmax:0},B:{Fmax:0}};
  let pts=[], moon=false, err=false, fitOn=true, cur=null, dirty=true;
  const f1=v=>(Math.round(v*10+1e-9)/10).toFixed(1);
  const fN=v=>{ let s=(Math.round(v*100+1e-9)/100).toFixed(2); s=s.replace(/0+$/,'').replace(/\.$/,''); return s; };
  const fld=id=>$(id).closest('.field');
  function sh(id,m,sub){ const e=$(id); if(e) e.innerHTML=m+(sub?'<span style="display:block;font-size:12px;font-weight:700;color:#59616c;margin-top:2px">'+sub+'</span>':''); }
  function tx(s,x,y,size,col,align,bold,halo){ ctx.font=(bold?'bold ':'')+size+'px '+FF; ctx.textAlign=align||'left'; if(halo){ ctx.lineJoin='round'; ctx.lineWidth=4; ctx.strokeStyle='rgba(255,255,255,0.92)'; ctx.strokeText(s,x,y); } ctx.fillStyle=col; ctx.fillText(s,x,y); return ctx.measureText(s).width; }
  function fitT(s,x,y,maxW,size,col,align,bold){ let z=size; ctx.font=(bold?'bold ':'')+z+'px '+FF; while(ctx.measureText(s).width>maxW&&z>10){ z-=0.5; ctx.font=(bold?'bold ':'')+z+'px '+FF; } tx(s,x,y,z,col,align,bold); }
  function rr(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
  function line(x1,y1,x2,y2,col,w,dash){ ctx.strokeStyle=col; ctx.lineWidth=w||1; ctx.setLineDash(dash||[]); ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2,y2); ctx.stroke(); ctx.setLineDash([]); }
  function arrow(x,y1,y2,col){ if(Math.abs(y2-y1)<3) return; const d=y2>y1?1:-1; line(x,y1,x,y2-d*8,col,4); ctx.fillStyle=col; ctx.beginPath(); ctx.moveTo(x,y2); ctx.lineTo(x-7,y2-d*11); ctx.lineTo(x+7,y2-d*11); ctx.closePath(); ctx.fill(); }
  const kv=id=>+$('k'+id).value;
  // ばねののび：弾性の限界(のび16cm)までは比例。こえると急にのび、はずしても元にもどらない（もどるときは同じ傾きで、のびが残る）
  function springX(id,f){ const k=kv(id); if(!k) return null; const sp=SP[id], Fl=XL/k; if(f>sp.Fmax) sp.Fmax=f;
    const dmg=sp.Fmax>Fl+1e-9, perm=dmg?0.5*k*(sp.Fmax-Fl):0, over=f>Fl+1e-9;
    const x=(dmg&&f>=sp.Fmax-1e-9)?XL+1.5*k*(f-Fl):perm+k*f;
    return {k:k,x:Math.min(XMAX,x),full:x>XMAX+1e-9,dmg:dmg,over:over,perm:perm}; }
  function update(){ const n=+$('n').value, m=+$('mass').value, fE=n*m/100, f=fE/(moon?6:1);
    const A=springX('A',f), B=springX('B',f); cur={n:n,m:m,M:n*m,fE:fE,f:f,A:A,B:B};
    [['A',A],['B',B]].forEach(q=>{ const id=q[0], s=q[1]; if(!s) return; const key=id+'|'+f.toFixed(4)+'|'+s.perm.toFixed(2)+'|'+(s.over?1:0);
      if(pts.some(p=>p.key===key)) return; const no=(err&&n>0)?clamp(randn()*0.18,-0.4,0.4):0;
      pts.push({key:key,id:id,f:f,x:clamp(s.x+no,0,XMAX),moon:moon,bad:s.dmg}); if(pts.length>160) pts.shift(); });
    const sub=(s,id)=>s.full?'のびきった':s.over?'弾性の限界をこえた':s.dmg?'元にもどらない':'1 Nで'+s.k+' cm';
    sh('sF',(moon?'約 ':'')+fN(f)+' N',moon?'地球の約1/6（地球では'+fN(fE)+' N）':(m+' gのおもり1個で約'+fN(m/100)+' N'));
    sh('sA',f1(A.x)+' cm',sub(A,'A'));
    if(B) sh('sB',f1(B.x)+' cm',sub(B,'B')); else sh('sB','使っていない','「ばねB」を1以上に');
    sh('sM',(n*m)+' g','地球でも月でも同じ');
    $('renew').style.display=(A.dmg||(B&&B.dmg))?'':'none';
    $('moonBtn').textContent=moon?'🌍 地球にもどす':'🌙 月面で調べる';
    $('errBtn').textContent='測定のずれ：'+(err?'あり':'なし'); $('fitBtn').textContent=fitOn?'直線をかくす':'直線を引く';
    setShare(moon?'【重さと質量】月面では質量'+(n*m)+'gのおもりの重さは約'+fN(f)+'N（地球の約1/6）。ばねAののびも'+f1(A.x)+'cmと約1/6｜シミュラボ'
      :'【ばねののび】'+(n*m)+'g（'+fN(f)+'N）のおもりで、ばねA（1Nで'+A.k+'cm）は'+f1(A.x)+'cmのびる。のびは力の大きさに比例（フックの法則）｜シミュラボ');
    dirty=true; }

  function spring(x,yb,k,dmg){ const top=TOPY, lead=8, nz=28, w=12; ctx.strokeStyle=dmg?'#b91c1c':'#475569'; ctx.lineWidth=1.3+(6-k)*0.35; ctx.lineJoin='round'; ctx.lineCap='round';
    ctx.beginPath(); ctx.moveTo(x,top); ctx.lineTo(x,top+lead); const L=yb-lead-(top+lead);
    for(let i=1;i<nz;i++) ctx.lineTo(x+(i%2?w:-w),top+lead+L*i/nz); ctx.lineTo(x,yb-lead); ctx.lineTo(x,yb); ctx.stroke(); }
  function drawLeft(c){ ctx.fillStyle=moon?'#e5e7eb':'#f8fafc'; ctx.fillRect(0,0,318,BAND);
    if(moon){ ctx.fillStyle='rgba(148,163,184,0.35)'; [[40,380,18],[270,330,12],[120,420,10],[250,410,20]].forEach(q=>{ ctx.beginPath(); ctx.arc(q[0],q[1],q[2],0,7); ctx.fill(); }); }
    ctx.fillStyle=moon?'#475569':'#0e7490'; rr(8,40,50,22,11); ctx.fill(); tx(moon?'月面':'地球',33,56,12,'#fff','center',true);
    ctx.fillStyle='#94a3b8'; rr(24,16,290,11,3); ctx.fill(); ctx.fillStyle='#a8b3c2'; ctx.fillRect(300,16,9,BAND-16);
    ctx.fillStyle='#fef3c7'; ctx.strokeStyle='#d6a74f'; ctx.lineWidth=1.5; ctx.fillRect(XR-15,Y0-12,30,XMAX*S+22); ctx.strokeRect(XR-15,Y0-12,30,XMAX*S+22);
    for(let i=0;i<=XMAX;i++){ const y=Y0+i*S, L=i%5===0?8:4; line(XR-15,y,XR-15+L,y,'#92400e',1); line(XR+15,y,XR+15-L,y,'#92400e',1); if(i%2===0) tx(String(i),XR,y+4,10,'#78350f','center',true); }
    tx('のび〔cm〕',XR,Y0-18,11,SUB,'center',true);
    [['A',XA],['B',XB]].forEach(q=>{ const id=q[0], x=q[1], s=c[id]; if(!s) return; const yb=Y0+s.x*S;
      ctx.fillStyle='#64748b'; ctx.beginPath(); ctx.arc(x,TOPY-2,3.5,0,7); ctx.fill();
      spring(x,yb,s.k,s.dmg);
      ctx.fillStyle=COL[id]; ctx.beginPath(); ctx.arc(x+(id==='A'?-22:22),TOPY+16,10,0,7); ctx.fill(); tx(id,x+(id==='A'?-22:22),TOPY+21,13,'#fff','center',true);
      const ex=id==='A'?XR-15:XR+15; line(x+(id==='A'?6:-6),yb,ex,yb,COL[id],2); ctx.fillStyle=COL[id]; ctx.beginPath(); ctx.moveTo(ex,yb); ctx.lineTo(ex+(id==='A'?-8:8),yb-5); ctx.lineTo(ex+(id==='A'?-8:8),yb+5); ctx.closePath(); ctx.fill();
      line(x,yb,x,yb+8,'#334155',2);
      const w=c.m>=100?40:c.m>=50?34:28;
      for(let i=0;i<c.n;i++){ const y=yb+8+i*DH; ctx.fillStyle=moon?'#9ca3af':'#64748b'; rr(x-w/2,y,w,DH-1,2); ctx.fill(); ctx.fillStyle='rgba(255,255,255,0.25)'; ctx.fillRect(x-w/2+2,y+1,w-4,1.5); }
      if(c.n) tx(c.M+' g',x+w/2+4,yb+8+c.n*DH-1,10.5,SUB,'left',true,true);
      if(id==='A'&&c.n>0){ const Fm=c.m/10, L=Math.max(6,c.f/Fm*58), yc=yb+8+c.n*DH/2, Ld=Math.min(L,BAND-6-yc);
        arrow(x,yb,yb-L,GRN); arrow(x,yc,yc+Ld,RED);
        tx('ばねの力',x-20,yb-L/2-2,11,GRN,'right',true,true); tx(fN(c.f)+' N',x-20,yb-L/2+11,11,GRN,'right',true,true);
        tx('重力',x-24,yc+Ld/2+2,11,RED,'right',true,true); tx(fN(c.f)+' N',x-24,yc+Ld/2+15,11,RED,'right',true,true); } }); }
  function drawRight(c){ ctx.fillStyle='#fff'; ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1.5; rr(328,8,304,146,10); ctx.fill(); ctx.stroke();
    fitT('おもり '+c.n+'個 × '+c.m+' g ＝ 質量 '+c.M+' g',340,32,282,15,INK,'left',true);
    fitT(moon?'月面：重さ '+fN(c.fE)+' N ÷ 6 ≒ '+fN(c.f)+' N':'地球：重さ（重力の大きさ）'+fN(c.f)+' N',340,57,282,14,RED,'left',true);
    [['A',82],['B',106]].forEach(q=>{ const id=q[0], s=c[id]; if(!s){ fitT('ばねB：使っていない',340,q[1],282,14,SUB,'left',true); return; }
      fitT('ばね'+id+'（1 Nで'+s.k+' cm）：のび '+f1(s.x)+' cm'+(s.dmg?'（限界をこえた）':''),340,q[1],282,14,s.dmg?'#b91c1c':COL[id],'left',true); });
    fitT('のび〔cm〕＝ 1 Nあたりののび × 力〔N〕',340,132,282,12.5,SUB,'left',false);
    const Fm=c.m/10, st=Fm<=2?0.5:Fm<=5?1:2;
    let ym=Math.max(c.A.x,c.B?c.B.x:0); ['A','B'].forEach(id=>{ if(c[id]) ym=Math.max(ym,c[id].k*Fm); }); pts.forEach(p=>{ if(c[p.id]&&p.f<=Fm+1e-9) ym=Math.max(ym,p.x); });
    const ys=ym<=5?1:ym<=10?2:4, YM=Math.max(ys,Math.min(XMAX,Math.ceil(ym/ys-1e-9)*ys)), X=f=>GX+f/Fm*GW, Y=x=>GY-x/YM*GH;
    ctx.fillStyle='#fff'; ctx.fillRect(GX,GY-GH,GW,GH);
    for(let f=st;f<=Fm+1e-9;f+=st) line(X(f),GY,X(f),GY-GH,'#e2e8f0',1);
    for(let x=ys;x<=YM+1e-9;x+=ys) line(GX,Y(x),GX+GW,Y(x),'#e2e8f0',1);
    line(GX,GY-GH,GX,GY,INK,1.5); line(GX,GY,GX+GW,GY,INK,1.5);
    for(let f=0;f<=Fm+1e-9;f+=st) tx(fN(f),X(f),GY+15,11,SUB,'center');
    for(let x=0;x<=YM+1e-9;x+=ys) tx(String(x),GX-5,Y(x)+4,11,SUB,'right');
    tx('ばねののび〔cm〕',GX-30,GY-GH-10,11.5,SUB,'left',true); tx('力の大きさ〔N〕',GX+GW,GY+31,11.5,SUB,'right',true);
    tx('●A ■B（白ぬき＝月面）✕＝限界後',GX+GW,GY-GH-10,10.5,SUB,'right',false);
    if(fitOn) ['A','B'].forEach(id=>{ const s=c[id]; if(!s) return; const P=pts.filter(p=>p.id===id&&!p.bad&&p.f>0); if(!P.length) return;
      let sxy=0,sxx=0; P.forEach(p=>{ sxy+=p.f*p.x; sxx+=p.f*p.f; }); const sl=sxy/sxx; let fe=Fm; if(sl*fe>YM) fe=YM/sl;
      line(X(0),Y(0),X(fe),Y(sl*fe),COL[id],2.2); const lx=X(fe), ly=Y(sl*fe);
      tx('1 Nで約'+f1(sl)+' cm',Math.min(lx,GX+GW-4),sl*fe>YM*0.88?ly+16:ly-8,11.5,COL[id],'right',true,true); });
    pts.forEach(p=>{ if(p.f>Fm+1e-9||!c[p.id]) return; const x=X(p.f), y=Y(p.x), col=COL[p.id];
      if(p.bad){ line(x-5,y-5,x+5,y+5,'#b91c1c',2.5); line(x-5,y+5,x+5,y-5,'#b91c1c',2.5); return; }
      ctx.lineWidth=2; ctx.strokeStyle=col; ctx.fillStyle=p.moon?'#fff':col; ctx.beginPath(); if(p.id==='A') ctx.arc(x,y,4.6,0,7); else ctx.rect(x-4.3,y-4.3,8.6,8.6); ctx.fill(); ctx.stroke(); }); }
  function draw(){ const c=cur; ctx.clearRect(0,0,W,H); ctx.fillStyle='#ffffff'; ctx.fillRect(0,0,W,H);
    drawLeft(c); drawRight(c);
    const A=c.A, B=c.B, anyOver=A.over||(B&&B.over), anyDmg=A.dmg||(B&&B.dmg);
    let msg, col=INK;
    if(A.full||(B&&B.full)){ msg='⚠ ばねがのびきった！ 弾性の限界を大きくこえている'; col='#b91c1c'; }
    else if(anyOver){ msg='⚠ 弾性の限界をこえた！ のびが力に比例しなくなり、グラフの直線からはずれる（✕）'; col='#b91c1c'; }
    else if(anyDmg){ msg='⚠ 限界をこえたばねは、おもりをはずしても元の長さにもどらない（のびが残る）'; col='#b91c1c'; }
    else if(moon) { msg='月面では重さが約1/6 → のびも約1/6。でも質量 '+c.M+' g は地球と同じ'; col='#475569'; }
    else if(c.n===0) msg='おもりをつるすと、ばねがのびる（左の図をタップしても1個ふえる）';
    else { msg='おもり1個（'+fN(c.m/100)+' N）ふえるごとに、ばねAは '+f1(A.k*c.m/100)+' cmずつのびる → のびは力に比例'; col=COL.A; }
    ctx.fillStyle='#fff'; ctx.fillRect(0,BAND,W,H-BAND); line(0,BAND,W,BAND,'#cbd5e1',1); fitT(msg,12,BAND+22,W-24,15,col,'left',true); }

  function setN(v){ $('n').value=clamp(v,0,10); $('n').dispatchEvent(new Event('input')); }
  $('n').addEventListener('input',update); $('mass').addEventListener('change',update);
  ['A','B'].forEach(id=>$('k'+id).addEventListener('input',()=>{ SP[id].Fmax=0; pts=pts.filter(p=>p.id!==id); if(id==='B') kBL(); update(); }));
  const kBL=()=>{ const v=+$('kB').value; $('kBL').textContent=v?'1Nで'+v+'cm':'使わない'; }; kBL();
  $('add').addEventListener('click',()=>setN(+$('n').value+1));
  $('sub').addEventListener('click',()=>setN(+$('n').value-1));
  $('moonBtn').addEventListener('click',()=>{ moon=!moon; update(); });
  $('errBtn').addEventListener('click',()=>{ err=!err; update(); });
  $('fitBtn').addEventListener('click',()=>{ fitOn=!fitOn; update(); });
  $('clr').addEventListener('click',()=>{ pts=[]; update(); });
  $('renew').addEventListener('click',()=>{ SP.A.Fmax=0; SP.B.Fmax=0; pts=pts.filter(p=>!p.bad); update(); });
  cv.addEventListener('pointerdown',e=>{ const p=cpos(cv,e), x=p[0]/dpr, y=p[1]/dpr; if(x<318&&y<BAND){ e.preventDefault(); setN(+$('n').value+1); } });
  const n0=+$('n').value; for(let i=0;i<=n0;i++){ $('n').value=i; update(); } $('n').dispatchEvent(new Event('input'));
  function frame(){ if(dirty){ dirty=false; draw(); } requestAnimationFrame(frame); }
  draw(); dirty=false; requestAnimationFrame(frame);
'''

sim(slug="bane-nobi", cat="rika", emoji="🪀", score=77,
    title="ばねののびと力のシミュレーター（フックの法則・重さと質量）",
    title_tag="ばねののびと力の大きさのシミュレーター｜フックの法則のグラフ・重さと質量のちがい（中1 力の働き）",
    meta_desc="おもりの数とばねの強さを変えると、ばねののびが力の大きさに比例するようすを、測定点が打たれていく力とのびのグラフで確かめられる無料シミュレーター。2本のばねの比較、弾性の限界、月面での重さ（約1/6）と質量のちがい、2力のつり合いの矢印つき。中1理科「力の働き」の授業に。",
    og_title="ばねののびと力のシミュレーター（フックの法則・重さと質量）",
    og_desc="おもりをつるすと、ばねののびと力のグラフに点が打たれる。比例の直線、2本のばねの比較、弾性の限界、月面での重さと質量。中1「力の働き」の授業向け。",
    card_desc="おもりをつるすと力とのびのグラフに点が打たれ、比例の直線に。月面での重さと質量のちがいも。",
    lead="おもりをつるすと、ばねがのびて、力の大きさとばねののびのグラフに測定点が打たれていきます。ばねの強さを変えて2本のばねをくらべたり、弾性の限界をこえて元にもどらなくなるようすを見たりできます。「月面で調べる」で、重さ（約6分の1）と質量のちがいも確かめられます。",
    model="中1 力の働き（ばねののび・重さと質量）",
    level="中学1年、高校（物理基礎）",
    unit="中学校 第1分野（1）身近な物理現象（イ）力の働き ㋐力の働き",
    canvas=canvas(640, 460, light=True),
    controls='<div class="lab-btns" style="grid-column:1/-1;margin:0 0 4px;">' + btn("add", "＋ おもりを1個つるす", True) + btn("sub", "－ 1個はずす") + btn("moonBtn", "🌙 月面で調べる") + '</div>'
           + slider("n", "おもりの数", 0, 10, 3, 1, "{v} 個")
           + select("mass", "おもり1個の質量", [("20", "20 g（約0.2 N）"), ("50", "50 g（約0.5 N）"), ("100", "100 g（約1 N）")])
           + slider("kA", "ばねAの強さ", 1, 6, 5, 0.5, "1Nで{v}cm")
           + slider("kB", "ばねBの強さ", 0, 6, 2.5, 0.5, "1Nで{v}cm"),
    buttons=btn("fitBtn", "直線をかくす") + btn("errBtn", "測定のずれ：なし") + btn("clr", "グラフを消す") + btn("renew", "🔧 ばねを新しくする"),
    stats=stats([("sF", "ばねを引く力（おもりの重さ）", True), ("sA", "ばねAののび", False), ("sB", "ばねBののび", False), ("sM", "おもりの質量", False)]),
    legend="ばねの強さは「1 Nの力で何cmのびるか」で表しています（数が大きいほど、やわらかいばね）。グラフの●＝ばねA、■＝ばねB、白ぬき＝月面で測った点、✕＝弾性の限界をこえた後の点。緑の矢印＝ばねがおもりを引く力、赤の矢印＝おもりにはたらく重力（2力はつり合っています）。質量100 gの物体にはたらく重力を1 Nとしています。",
    article=BANE_ARTICLE, faqs=BANE_FAQS,
    rel=[("teko-tsuriai", "⚖️", "てこのつり合い"), ("suiatsu-fuyuu", "🛟", "水圧と浮力"), ("kassha-shigoto", "🏗️", "滑車と仕事"), ("furiko-jikken", "⏱️", "振り子の実験"), ("gravity", "🌌", "重力シミュレーター")],
    js=BANE_JS)
