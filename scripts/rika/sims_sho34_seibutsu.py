# -*- coding: utf-8 -*-
"""理科の授業向け：小3 身の回りの生物（こん虫・植物の育ち方と体のつくり）／小4 季節と生物"""
import math
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

MEXT_SHO = "https://www.mext.go.jp/a_menu/shotou/new-cs/1387014.htm"
JMA_TOKYO = "https://www.data.jma.go.jp/stats/etrn/view/nml_sfc_ym.php?prec_no=44&block_no=47662&year=&month=&day=&view="

# ---- 共通の描画ヘルパー（JS）
HELP_JS = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const h1=document.querySelector('.sim-head h1'); if(h1&&!h1.children.length){ const t=h1.textContent, i=t.indexOf('（'); if(i>0){ h1.textContent=t.slice(0,i); const sp=document.createElement('span'); sp.style.display='inline-block'; sp.textContent=t.slice(i); h1.appendChild(sp); } }
  const fld=(id)=>$(id).closest('.field');
  function setK(id,s){ const e=$(id); if(e&&e.previousElementSibling&&e.previousElementSibling.textContent!==s) e.previousElementSibling.textContent=s; }
  function setV(id,s){ const e=$(id); if(!e||e.textContent===s) return; e.textContent=s; e.style.fontSize=s.length>11?'14px':(s.length>6?'16px':''); }
  function rrect(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
  function txt(t,x,y,size,col,weight,align,maxW,halo){ ctx.textAlign=align||'left'; let s=size; ctx.font=(weight||'')+' '+s+'px sans-serif';
    if(maxW){ while(ctx.measureText(t).width>maxW&&s>8){ s-=0.5; ctx.font=(weight||'')+' '+s+'px sans-serif'; } }
    if(halo){ ctx.lineWidth=3.5; ctx.strokeStyle='rgba(255,255,255,.92)'; ctx.lineJoin='round'; ctx.strokeText(t,x,y); }
    ctx.fillStyle=col||'#0f172a'; ctx.fillText(t,x,y); return ctx.measureText(t).width; }
  function wrap(t,x,y,maxW,lh,size,col,weight){ ctx.font=(weight||'')+' '+size+'px sans-serif'; ctx.textAlign='left'; ctx.fillStyle=col||'#0f172a'; let line='', yy=y;
    for(const ch of t){ if(ctx.measureText(line+ch).width>maxW&&line&&'、。）」→'.indexOf(ch)<0){ ctx.fillText(line,x,yy); line=ch; yy+=lh; } else line+=ch; } if(line) ctx.fillText(line,x,yy); return yy; }
  function dot(x,y,r,c){ ctx.fillStyle=c; ctx.beginPath(); ctx.arc(x,y,Math.max(0.1,r),0,Math.PI*2); ctx.fill(); }
  function ell(x,y,rx,ry,r,f,s,lw){ ctx.beginPath(); ctx.ellipse(x,y,Math.max(0.1,rx),Math.max(0.1,ry),r||0,0,Math.PI*2); if(f){ ctx.fillStyle=f; ctx.fill(); } if(s){ ctx.strokeStyle=s; ctx.lineWidth=lw||1.5; ctx.stroke(); } }
  function ln(x1,y1,x2,y2,w,c){ ctx.strokeStyle=c; ctx.lineWidth=w; ctx.lineCap='round'; ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2,y2); ctx.stroke(); }
  function poly(pts,w,c,dash){ ctx.strokeStyle=c; ctx.lineWidth=w; ctx.lineJoin='round'; ctx.lineCap='round'; if(dash) ctx.setLineDash(dash); ctx.beginPath(); pts.forEach((p,i)=>{ if(i) ctx.lineTo(p[0],p[1]); else ctx.moveTo(p[0],p[1]); }); ctx.stroke(); if(dash) ctx.setLineDash([]); }
  function hex(c){ return [parseInt(c.slice(1,3),16),parseInt(c.slice(3,5),16),parseInt(c.slice(5,7),16)]; }
  function mix(a,b,t){ const A=hex(a),B=hex(b); t=clamp(t,0,1); return 'rgb('+A.map((v,i)=>Math.round(v+(B[i]-v)*t)).join(',')+')'; }
  function chip(t,x,y,size,bg,col,align){ ctx.font='bold '+size+'px sans-serif'; const w=ctx.measureText(t).width+14, x0=align==='center'?x-w/2:(align==='right'?x-w:x); ctx.fillStyle=bg; rrect(x0,y-size-3,w,size+9,7); ctx.fill(); txt(t,x0+7,y,size,col,'bold','left'); return w; }
  function leafE(x,y,len,wid,ang,col,edge){ if(len<1) return; ctx.save(); ctx.translate(x,y); ctx.rotate(ang); ctx.beginPath(); ctx.moveTo(0,0); ctx.bezierCurveTo(len*0.25,-wid,len*0.75,-wid*0.9,len,0); ctx.bezierCurveTo(len*0.75,wid*0.9,len*0.25,wid,0,0); ctx.closePath(); ctx.fillStyle=col; ctx.fill(); ctx.strokeStyle=edge||'rgba(20,83,45,.55)'; ctx.lineWidth=1; ctx.stroke(); ctx.beginPath(); ctx.moveTo(2,0); ctx.lineTo(len-3,0); ctx.stroke(); ctx.restore(); }
  function caterpillar(x,y,Lp,col){ const n=11, sp=Lp/(n-1), r=Math.max(1.4,sp*0.78);
    for(let i=n-1;i>=0;i--){ const px=x-Lp/2+i*sp, py=y+Math.sin(tnow*4+i*0.7)*r*0.22; dot(px,py+r*0.7,Math.max(0.6,r*0.22),'#3f6212'); dot(px,py,r,i===0?'#4d7c0f':(col||'#84cc16')); if(i>0&&r>2.5) dot(px,py-r*0.15,r*0.18,'#fde047'); }
    if(r>3){ dot(x-Lp/2-r*0.3,y-r*0.2,r*0.18,'#1f2937'); } }
  function butterfly(x,y,s,flap){ const sx=0.28+0.72*Math.abs(Math.cos(flap));
    [-1,1].forEach((sd)=>{ ctx.save(); ctx.translate(x,y); ctx.scale(sd*sx*s,s);
      ctx.beginPath(); ctx.moveTo(0,2); ctx.bezierCurveTo(30,0,38,18,26,30); ctx.bezierCurveTo(14,36,4,20,0,8); ctx.closePath(); ctx.fillStyle='#f1f5f9'; ctx.fill(); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1.2/s; ctx.stroke();
      ctx.beginPath(); ctx.moveTo(0,-4); ctx.bezierCurveTo(10,-30,40,-36,46,-26); ctx.bezierCurveTo(44,-10,26,0,0,2); ctx.closePath(); ctx.fillStyle='#f8fafc'; ctx.fill(); ctx.stroke();
      ctx.save(); ctx.clip(); dot(46,-30,11,'#475569'); ctx.restore(); dot(27,-13,4.2,'#475569'); ctx.restore(); });
    ell(x,y+4*s,3*s,15*s,0,'#334155'); dot(x,y-12*s,3.6*s,'#1f2937');
    [-1,1].forEach((sd)=>{ ln(x+sd*1.5*s,y-14*s,x+sd*10*s,y-30*s,1.2,'#334155'); dot(x+sd*10*s,y-30*s,1.8*s,'#334155'); }); }
'''

# ============================================================ 1 こん虫の育ち方と体のつくり
BF_ST = [("たまご", 0, 7), ("よう虫", 7, 24), ("さなぎ", 24, 34), ("成虫", 34, 60)]
GH_ST = [("たまご", 0, 14), ("よう虫", 14, 49), ("成虫", 49, 60)]
BF_MOLT = [10, 13, 16, 20]          # よう虫が皮をぬぐ日（4回）。24日目に5回目でさなぎ
GH_MOLT = [21, 28, 35, 42]          # 49日目に5回目の皮をぬいで成虫
def bf_len(d): return 3 * 10 ** ((d - 7) / 17)          # よう虫の体長 mm（3mm→30mm）
def gh_len(d): return 7 * (40 / 7) ** ((d - 14) / 35)   # よう虫の体長 mm（7mm→40mm）
PLANTS = {"hosenka": dict(n="ホウセンカ", H=50, mid=42, sc=9, st=[("たね", 0, 6), ("芽が出る（子葉）", 6, 14), ("葉がふえる・くきがのびる", 14, 60), ("花がさく", 60, 80), ("実ができる", 80, 145), ("かれる", 145, 170)]),
          "himawari": dict(n="ヒマワリ", H=180, mid=52, sc=9, st=[("たね", 0, 8), ("芽が出る（子葉）", 8, 16), ("葉がふえる・くきがのびる", 16, 70), ("花がさく", 70, 95), ("実（たね）ができる", 95, 140), ("かれる", 140, 170)])}
def ph(k, d):
    p = PLANTS[k]; g = p["st"][1][1]
    if d < g: return 0.0
    return max(1.0, p["H"] / (1 + math.exp(-(min(d, p["st"][5][1]) - p["mid"]) / p["sc"])))
def mdate(d):
    ms = [31, 30, 31, 31, 30, 31]; m, dd = 5, 1 + d
    while dd > ms[m - 5]: dd -= ms[m - 5]; m += 1
    return "%d月%d日" % (m, dd)

def _stage_row(S):
    return " → ".join("%s（%d〜%d日目）" % (n, a, b) if i < len(S) - 1 else "%s（%d日目〜）" % (n, a) for i, (n, a, b) in enumerate(S))

KONCHU_ARTICLE = "<h2>このシミュレーションでわかること</h2>\n" + P(
    "こん虫の育ち方には、決まった<b>順番</b>があります。モンシロチョウは「<b>たまご → よう虫 → さなぎ → 成虫</b>」、バッタは「<b>たまご → よう虫 → 成虫</b>」と育ち、バッタは<b>さなぎになりません</b>。"
    "こん虫の成虫の体は<b>頭・むね・はら</b>の3つに分かれていて、<b>むねに6本のあし</b>があります。植物は「たね → 子葉 → 葉がふえる → 花 → 実（たね） → かれる」の順に育ち、体は<b>根・くき・葉</b>からできています。") + '''
<p>小学校3年の理科「<b>身の回りの生物</b>」（学習指導要領 第3学年 B（1））で学ぶ内容です。学習指導要領の解説（理科編 pp.39〜42）は、「卵→幼虫→蛹→成虫」と「卵→幼虫→成虫」のように<b>育ち方のちがうこん虫をくらべる</b>こと、成虫の体が頭・胸・腹の3つからできていて胸に3対6本のあしがあるものを「昆虫」という名前を使って説明できるようにすることを挙げています。植物は、内容の取扱いで「夏生一年生の双子葉植物」（ホウセンカ・ヒマワリなど）を扱うことになっています。</p>
<p>画面は4つです。<b>①育ち方</b>では、モンシロチョウとバッタ（トノサマバッタ）を同じ日数でならべ、早送りで育つようすをくらべます。<b>②体のつくりパズル</b>では、頭・むね・はら・あし・はねのパーツを指で動かして、こん虫の体を組み立てます。<b>③こん虫かな？</b>では、アリ・クモ・テントウムシ・ダンゴムシ・トンボ・ムカデがこん虫かどうかを答え、体の分かれ方とあしの数をたしかめます。<b>④植物の育ち方</b>では、ホウセンカとヒマワリの育ち方を日数のスライダーで見て、根・くき・葉の名前をたしかめます。</p>
<h2>授業での使い方</h2>
<ul>
<li><b>導入</b>：モンシロチョウのたまごやよう虫を見つけたあと、「このよう虫は、これからどうなるかな」と予想させてから、①を早送りします。飼育を始める前の見通しや、休み中に見られなかった時期（さなぎから成虫が出てくるところなど）の確認に使えます。</li>
<li><b>展開</b>：①で、たまごから同じ日数のときのモンシロチョウとバッタをくらべ、「ちがうところ」「同じところ」を話し合います。②のパズルでは、あしやはねを「はら」に付けようとするとヒントが出るので、あしがどこから出ているかを自分でたしかめられます。</li>
<li><b>まとめ</b>：③のクイズで、こん虫とこん虫でない生き物を「体の分かれ方」と「あしの数」で見分けます。④で植物の育ち方もならべ、こん虫も植物も「育つ順番が決まっている」ことをまとめます。画面のアドレスの最後に <code>#pazuru</code>・<code>#quiz</code>・<code>#shokubutsu</code> を付けると、その画面から始まります。</li>
</ul>
<p>児童への問いの例：</p>
<ol>
<li>モンシロチョウとバッタの育ち方で、ちがうところはどこでしょう。</li>
<li>こん虫のあしは、体のどの部分から何本出ているでしょう。</li>
<li>クモやダンゴムシがこん虫ではないのはなぜでしょう。</li>
</ol>
<h2>しくみ・解説</h2>
<h3>ことばの意味</h3>
<ul>
<li><b>こん虫</b>とは、成虫の体が<b>頭・むね・はら</b>の3つに分かれていて、むねに<b>6本（3対）のあし</b>がある動物のなかまです。</li>
<li><b>よう虫</b>とは、たまごからかえったあと、成虫になる前のこん虫のことです。食べ物を食べ、<b>皮をぬいで</b>大きくなります。</li>
<li><b>さなぎ</b>とは、よう虫から成虫になるとちゅうのすがたで、何も食べず、ほとんど動きません。中で成虫の体がつくられます。</li>
<li><b>成虫</b>とは、育ちきったこん虫で、はねのあるものが多く、たまごを産みます。</li>
</ul>
<h3>こん虫の育ち方（早見表）</h3>
''' + T([["モンシロチョウ", "たまご → よう虫 → さなぎ → 成虫", "なる"], ["アゲハ", "たまご → よう虫 → さなぎ → 成虫", "なる"],
          ["カブトムシ", "たまご → よう虫 → さなぎ → 成虫", "なる"], ["バッタ", "たまご → よう虫 → 成虫", "ならない"],
          ["トンボ", "たまご → よう虫（ヤゴ・水の中でくらす） → 成虫", "ならない"], ["コオロギ・セミ", "たまご → よう虫 → 成虫", "ならない"]],
         ["こん虫", "育つ順番", "さなぎに"]) + '''
<h3>このシミュレーションの日数（目安）</h3>
''' + T([["モンシロチョウ", _stage_row(BF_ST), "4回皮をぬいで大きくなり、5回目に皮をぬぐとさなぎになる（体長 約3mm → 約3cm）"],
          ["バッタ（トノサマバッタ）", _stage_row(GH_ST), "5回皮をぬいで成虫になる（体長 約7mm → 成虫 約4〜6cm）"]],
         ["こん虫", "育つ順番と日数", "よう虫のようす"]) + '''
<p>日数は、あたたかい季節（20〜25℃くらい）の<b>目安</b>です。モンシロチョウは、たまご 約1週間、よう虫 約2〜3週間、さなぎ 約10日で成虫になります（このシミュレーションでは %d日目に成虫）。バッタは、夏に産まれたたまごが約2週間でかえり、よう虫の時期は約1か月です（%d日目に成虫）。秋に産まれたバッタのたまごは、土の中で冬をこして、次の年にかえります。気温が低いと、どちらも日数が長くなります。</p>
''' % (BF_ST[3][1], GH_ST[2][1]) + '''
<h3>こん虫の体のつくり</h3>
''' + T([["頭", "目・しょっかく・口がある", "まわりのようすを感じる・食べる"], ["むね", "あしが6本（3対）、はねがあるものが多い", "歩く・とぶ"],
          ["はら", "いくつかの「ふし」に分かれている", "息をする・たまごを産む など"]],
         ["部分", "あるもの", "おもなはたらき"]) + N("あしやはねは、<b>すべて「むね」から出ています</b>。チョウやバッタの絵をかくとき、あしを「はら」から出してしまうまちがいが多いので、②のパズルで、あしやはねを「はら」に置こうとするとヒントが出るようにしています。") + '''
<h3>こん虫かどうかの見分け方（早見表）</h3>
''' + T([["アリ", "3つ（頭・むね・はら）", "6本", "こん虫"], ["テントウムシ", "3つ（はらは、かたいはねの下）", "6本", "こん虫"],
          ["トンボ", "3つ", "6本", "こん虫"], ["クモ", "2つ（頭とむねが1つになった部分・はら）", "8本", "こん虫ではない"],
          ["ダンゴムシ", "たくさんのふしに分かれている", "14本", "こん虫ではない"], ["ムカデ", "たくさんのふしに分かれている", "30本以上", "こん虫ではない"]],
         ["生き物", "体の分かれ方", "あしの数", "こたえ"]) + '''
<h3>植物の育ち方と体のつくり</h3>
<p>植物の体は<b>根・くき・葉</b>からできています。根は土の中にあり、くきは葉や花をつけています。たねから芽が出ると、はじめに<b>子葉</b>が出て、そのあと子葉とちがう形の葉がふえていきます。花がさいたあとに実ができ、実の中にたねができると、植物はかれます。</p>
''' + T([[PLANTS[k]["n"]] + ["%s（%s〜）" % (n, mdate(a)) for n, a, b in PLANTS[k]["st"][1:]] for k in ("hosenka", "himawari")],
         ["植物", "芽が出る", "葉がふえる", "花", "実", "かれる"]) + '''
<p>表の日付は、5月1日にたねをまいたときの目安です（このシミュレーションの高さの目安：ホウセンカ 約%dcm、ヒマワリ 約%dcm。ヒマワリの高さは品種によって大きくちがいます）。</p>
''' % (round(ph("hosenka", 100)), round(ph("himawari", 100))) + '''
<h3>生き物をあつかうときの注意</h3>
<ul>
<li>こん虫や植物、土にさわったあとは、<b>石けんで手をあらいましょう</b>。</li>
<li>よう虫は手で直接つままず、葉ごと動かします。飼育ケースの中は、ふんをとって清潔にします。</li>
<li>野外では、ハチや毒のある毛虫などに近づかないようにします。つかまえる生き物は必要な数だけにし、観察が終わったら元の場所にもどしましょう。</li>
</ul>
<h3>このシミュレーションで単純にしていること</h3>
<ul>
<li>日数・体長・高さは目安です。実際は気温・えさ・品種などで変わります。</li>
<li>たまごやよう虫は、見やすいように実際より大きくかいています（たまごは虫めがねでかくだいした図もつけています）。体の図は、写真ではなく形をわかりやすくした模式図です。</li>
<li>バッタはトノサマバッタの、夏に産まれたたまごの場合です。パズルの虫は、特定の種類ではない、こん虫の体のつくりを表した図です。</li>
</ul>
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「小学校学習指導要領（平成29年告示）解説 理科編」第3学年 B（1）身の回りの生物（pp.39〜42）（<a href="''' + MEXT_SHO + '''" target="_blank" rel="noopener">文部科学省 小学校学習指導要領解説のページ</a>）</li>
<li>小学校理科（3年）の教科書の「チョウを育てよう」「こん虫のかんさつ」「植物の育ち方」の単元</li>
</ul>
'''

KONCHU_FAQS = [
    ("こん虫とは、どんな生き物ですか？", "成虫の体が頭・むね・はらの3つに分かれていて、むねに6本（3対）のあしがある動物のなかまです。チョウ・バッタ・トンボ・アリ・テントウムシなどがこん虫です。"),
    ("さなぎにならないこん虫には、何がいますか？", "バッタ・トンボ・コオロギ・セミなどは、たまご→よう虫→成虫と育ち、さなぎになりません。チョウ・カブトムシ・テントウムシなどは、たまご→よう虫→さなぎ→成虫と育ちます。"),
    ("クモやダンゴムシは、こん虫ですか？", "どちらもこん虫ではありません。クモは体が2つに分かれていて、あしが8本です。ダンゴムシは体がたくさんのふしに分かれていて、あしが14本です。"),
    ("モンシロチョウは、たまごから何日くらいで成虫になりますか？", "あたたかい季節で約1か月あまりです。たまご約1週間、よう虫約2〜3週間、さなぎ約10日が目安です。気温が低いと長くかかります。"),
    ("こん虫のあしやはねは、体のどこから出ていますか？", "あしもはねも、すべて「むね」から出ています。あしは6本、はねは4まいのものが多いですが、はねが2まいのもの（ハエなど）や、はねのないもの（アリのはたらきアリなど）もいます。"),
    ("植物は、どんな順番で育ちますか？", "たねから芽が出て子葉が開き、葉がふえてくきがのび、花がさき、実ができてたねができると、かれます。体は根・くき・葉からできています。"),
]

KONCHU_JS = HELP_JS + r'''
  const bar=document.createElement('div'); bar.className='lab-btns'; bar.style.marginTop='0';
  ['tA','tB','tC','tD'].forEach((id)=>{ const b=$(id); if(b) bar.appendChild(b); });
  cv.parentNode.insertBefore(bar,cv);
  let mode='A', run=false, day=+$('day').value, pday=+$('pday').value, tnow=0, msg=null, drag=null;

  // ================= ① こん虫の育ち方
  const BF=[['たまご',0,7,'#fde68a'],['よう虫',7,24,'#86efac'],['さなぎ',24,34,'#e7c99a'],['成虫',34,60,'#93c5fd']];
  const GH=[['たまご',0,14,'#fde68a'],['よう虫',14,49,'#86efac'],['成虫',49,60,'#93c5fd']];
  const BFM=[10,13,16,20], GHM=[21,28,35,42], DMAX=60, TX0=20, TX1=620;
  const SCOL={'たまご':'#a16207','よう虫':'#15803d','さなぎ':'#92400e','成虫':'#1d4ed8'};
  // 観察スケッチ風の絵（art/*.webp・2026-10-19）。読み込めないときは、これまでのコードでかいた絵を出す
  const ART={};
  ['monshiro-tamago','monshiro-youchu','monshiro-sanagi','monshiro-seichu','batta-tamago','batta-youchu','batta-seichu'].forEach((k)=>{ const im=new Image(); im.onload=()=>{ ART[k]=im; }; im.src='art/'+k+'.webp'; });
  function art(k,x0,y0,w,h,sc,dx,dy){ const im=ART[k]; if(!im) return false; const s=Math.min((w-12)/im.width,(h-10)/im.height)*(sc||1);
    const iw=im.width*s, ih=im.height*s; ctx.drawImage(im,x0+(w-iw)/2+(dx||0),y0+(h-ih)/2+(dy||0),iw,ih); return true; }
  function stg(S,d){ for(let i=0;i<S.length;i++){ if(d<S[i][2]||i===S.length-1) return i; } return 0; }
  const molts=(M,d)=>M.filter((m)=>d>=m).length;
  const tx=(d)=>TX0+d*(TX1-TX0)/DMAX;
  function fmtL(mm){ return mm<10?Math.round(mm)+'mm':(Math.round(mm)/10).toFixed(1)+'cm'; }
  const bfLen=(d)=>3*Math.pow(10,(d-7)/17), ghLen=(d)=>7*Math.pow(40/7,(d-14)/35);
  function bfInfo(d){ const i=stg(BF,d), n=molts(BFM,d);
    if(i===0) return [BF[0][0],['キャベツなどの葉のうらに産みつけられる','長さ 約1mm。たてに細長い、黄色っぽい形','あと'+Math.max(1,Math.ceil(7-d))+'日ほどで よう虫がかえる']];
    if(i===1) return ['よう虫'+(n?'（皮を'+n+'回ぬいだ）':'（かえったばかり）'),['キャベツなどの葉を食べて大きくなる','体長 約'+fmtL(bfLen(d)),n<4?'皮をぬいで大きくなる（4回ぬぐ）':'つぎに皮をぬぐと、さなぎになる']];
    if(i===2) return [BF[2][0],['何も食べず、ほとんど動かない','長さ 約2cm。糸で体をささえている',d>=31?'中で成虫の体ができてきた（もようがすけて見える）':'さなぎの中で、成虫の体がつくられている']];
    return [BF[3][0],[d<35.5?'さなぎから成虫が出てきた（羽化）':'はねを広げると 約5cm','花のみつをすう','はね4まい・あし6本。たまごを産む']]; }
  function ghInfo(d){ const i=stg(GH,d), n=molts(GHM,d);
    if(i===0) return [GH[0][0],['土の中に、あわでつつんだ たまごのかたまりを産む','夏に産まれたたまごは 約2週間でかえる','あと'+Math.max(1,Math.ceil(14-d))+'日ほどで よう虫がかえる']];
    if(i===1) return ['よう虫'+(n?'（皮を'+n+'回ぬいだ）':'（かえったばかり）'),['草の葉を食べて大きくなる','体長 約'+fmtL(ghLen(d)),'成虫とにた形。はねはまだ小さい（さなぎにならない）']];
    return [GH[2][0],[d<50.5?'5回目に皮をぬいで成虫になった（さなぎにならない）':'体長 約4〜6cm','草の葉を食べる','はねがのびて とべる。あし6本']]; }
  function cabbage(x,y,w,h,eaten){ ell(x,y,w/2,h/2,0,'#bbf7d0','#4ade80',2); ln(x-w/2+6,y,x+w/2-6,y,2,'#86efac');
    for(let k=-3;k<=3;k++){ if(!k) continue; const xx=x+k*w/8; ln(xx,y,xx+w/12,y-h*0.36,1.2,'#86efac'); ln(xx,y,xx+w/12,y+h*0.36,1.2,'#86efac'); }
    const HO=[[0.28,-0.22,10],[-0.2,0.25,9],[0.12,0.3,12],[-0.32,-0.18,11],[0.38,0.12,8],[-0.05,-0.3,10]];
    for(let k=0;k<Math.round(eaten*HO.length);k++){ const q=HO[k]; ell(x+q[0]*w,y+q[1]*h,q[2],q[2]*0.75,0.4,'#f8fafc'); } }
  function pupa(x,y,s,ripe){ ln(x-16*s,y-62,x-16*s,y+60,5,'#a16207');
    ctx.beginPath(); ctx.moveTo(x,y-36*s); ctx.bezierCurveTo(x+16*s,y-20*s,x+14*s,y+8*s,x+3*s,y+32*s); ctx.bezierCurveTo(x-8*s,y+14*s,x-12*s,y-6*s,x-10*s,y-14*s); ctx.closePath();
    ctx.fillStyle=mix('#a3c46c','#e2e8f0',ripe*0.7); ctx.fill(); ctx.strokeStyle='#4d7c0f'; ctx.lineWidth=1.5; ctx.stroke();
    if(ripe>0){ ctx.globalAlpha=ripe; ell(x+3*s,y-6*s,6*s,14*s,0.2,'#f8fafc'); dot(x+5*s,y-14*s,3*s,'#475569'); ctx.globalAlpha=1; }
    ln(x-16*s,y-4*s,x+8*s,y-8*s,1,'#cbd5e1'); ln(x-16*s,y+4*s,x+8*s,y-8*s,1,'#cbd5e1'); }
  function grasshopper(x,y,L,wf,nymph){ const col=nymph?'#84cc16':'#65a30d', dk='#3f6212';
    ln(x-0.28*L,y+0.06*L,x-0.32*L,y+0.15*L,Math.max(1.2,0.02*L),dk); ln(x-0.32*L,y+0.15*L,x-0.37*L,y+0.23*L,Math.max(1.2,0.02*L),dk);
    ln(x-0.15*L,y+0.07*L,x-0.12*L,y+0.15*L,Math.max(1.2,0.02*L),dk); ln(x-0.12*L,y+0.15*L,x-0.09*L,y+0.23*L,Math.max(1.2,0.02*L),dk);
    ell(x+0.16*L,y,0.32*L,0.085*L,0,col,dk,1.2);
    for(let k=1;k<6;k++){ const xx=x-0.1*L+k*0.09*L; ln(xx,y-0.06*L,xx,y+0.06*L,0.8,'rgba(63,98,18,.45)'); }
    ctx.fillStyle=col; rrect(x-0.33*L,y-0.105*L,0.23*L,0.19*L,0.05*L); ctx.fill(); ctx.strokeStyle=dk; ctx.lineWidth=1.2; ctx.stroke();
    const hr=(nymph?0.13:0.1)*L; ell(x-0.4*L,y-0.01*L,hr*0.9,hr,0.2,col,dk,1.2); dot(x-0.44*L,y-0.045*L,hr*0.36,'#713f12');
    ln(x-0.44*L,y-0.09*L,x-0.62*L,y-0.32*L,Math.max(1,0.012*L),dk);
    if(wf>0.5){ ell(x+0.2*L,y-0.075*L,0.42*L*wf,0.065*L,0.03,'rgba(77,124,15,.92)',dk,1); }
    else if(wf>0){ ell(x-0.06*L,y-0.08*L,0.12*L*wf*2.2,0.05*L,0.25,'#65a30d',dk,1); }
    ctx.strokeStyle=dk; ctx.lineCap='round'; ctx.lineWidth=Math.max(3,0.07*L); ctx.beginPath(); ctx.moveTo(x-0.08*L,y+0.02*L); ctx.lineTo(x+0.3*L,y-0.13*L); ctx.stroke();
    ctx.strokeStyle=col; ctx.lineWidth=Math.max(2,0.05*L); ctx.beginPath(); ctx.moveTo(x-0.08*L,y+0.02*L); ctx.lineTo(x+0.3*L,y-0.13*L); ctx.stroke();
    ln(x+0.3*L,y-0.13*L,x+0.17*L,y+0.23*L,Math.max(1.2,0.022*L),dk); ln(x+0.17*L,y+0.23*L,x+0.26*L,y+0.24*L,Math.max(1,0.015*L),dk); }
  function grass(x0,y0,w,h,n){ for(let k=0;k<n;k++){ const gx=x0+8+k*(w-16)/(n-1), sw=Math.sin(tnow*1.3+k)*3; ctx.strokeStyle=k%2?'#4ade80':'#22c55e'; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(gx,y0+h); ctx.quadraticCurveTo(gx+4,y0+h*0.5,gx+10+sw,y0+h*(0.15+0.25*(k%3)/2)); ctx.stroke(); } }
  function drawBF(x0,y0,d){ const i=stg(BF,d), cx=x0+120, cy=y0+66;
    if(i===0&&ART['monshiro-tamago']){ ctx.fillStyle='#f0fdf4'; ctx.fillRect(x0,y0,240,132); art('monshiro-tamago',x0,y0,240,132,0.95); txt('かくだい（実物は長さ約1mm）',x0+236,y0+126,10.5,'#475569','bold','right'); return; }
    if(i===1&&ART['monshiro-youchu']){ ctx.fillStyle='#f0fdf4'; ctx.fillRect(x0,y0,240,132); art('monshiro-youchu',x0,y0,240,132,clamp(0.3+0.7*(bfLen(d)-3)/27,0.3,1)); return; }
    if(i===2&&ART['monshiro-sanagi']){ ctx.fillStyle='#fefce8'; ctx.fillRect(x0,y0,240,132); art('monshiro-sanagi',x0,y0,240,132,1); return; }
    if(i===3&&ART['monshiro-seichu']){ ctx.fillStyle='#e0f2fe'; ctx.fillRect(x0,y0,240,132); art('monshiro-seichu',x0,y0,240,132,0.95,Math.sin(tnow*0.9)*6,Math.cos(tnow*1.3)*3); return; }
    if(i<=1){ ctx.fillStyle='#f0fdf4'; ctx.fillRect(x0,y0,240,132); cabbage(cx,cy+4,206,112,i===1?clamp((d-7)/17,0,1):0);
      if(i===0){ const ex=cx-36, ey=cy+6; ell(ex,ey,2.6,6,0,'#facc15','#a16207',1);
        ctx.fillStyle='#fff'; ctx.beginPath(); ctx.arc(cx+52,cy-14,36,0,Math.PI*2); ctx.fill(); ctx.strokeStyle='#64748b'; ctx.lineWidth=3; ctx.stroke(); ln(cx+76,cy+12,cx+96,cy+36,6,'#64748b'); ln(ex+4,ey-4,cx+20,cy-22,1,'#94a3b8');
        ell(cx+52,cy-14,10,26,0,mix('#fde047','#fb923c',clamp(d/7,0,1)),'#a16207',1.5); for(let k=-2;k<=2;k++) ln(cx+52+k*3.6,cy-36,cx+52+k*3.6,cy+8,0.8,'rgba(161,98,7,.5)'); txt('かくだい',cx+52,cy+38,11,'#475569','bold','center'); }
      else caterpillar(cx-10,cy+4,24+bfLen(d)*3.3); }
    else if(i===2){ ctx.fillStyle='#fefce8'; ctx.fillRect(x0,y0,240,132); pupa(cx,cy,1.3,clamp((d-31)/3,0,1)); }
    else { ctx.fillStyle='#e0f2fe'; ctx.fillRect(x0,y0,240,132); ln(cx+60,y0+132,cx+62,cy+20,3,'#65a30d'); [[0,0],[8,6],[-7,7],[2,-8]].forEach((p)=>dot(cx+62+p[0],cy+16+p[1],5,'#facc15'));
      if(d<35.5) pupa(cx-50,cy,1.1,1);
      butterfly(cx-10+Math.sin(tnow*0.9)*14,cy-6+Math.cos(tnow*1.3)*6,1.3,tnow*7); } }
  function drawGH(x0,y0,d){ const i=stg(GH,d), cx=x0+120, cy=y0+66;
    if(i===0&&ART['batta-tamago']){ ctx.fillStyle='#f7f1e3'; ctx.fillRect(x0,y0,240,132); art('batta-tamago',x0,y0,240,132,1); txt('土の中（断面）',x0+6,y0+126,11,'#475569','bold','left'); return; }
    if(i===1&&ART['batta-youchu']){ ctx.fillStyle='#ecfccb'; ctx.fillRect(x0,y0,240,132); art('batta-youchu',x0,y0,240,132,clamp(0.3+0.7*(ghLen(d)-7)/33,0.3,1)); return; }
    if(i===2&&ART['batta-seichu']){ ctx.fillStyle='#ecfccb'; ctx.fillRect(x0,y0,240,132); art('batta-seichu',x0,y0,240,132,1); return; }
    if(i===0){ ctx.fillStyle='#e0f2fe'; ctx.fillRect(x0,y0,240,40); ctx.fillStyle='#a8865a'; ctx.fillRect(x0,y0+40,240,92); grass(x0,y0,240,40,9);
      for(let k=0;k<26;k++) dot(x0+8+(k*53)%228,y0+48+(k*29)%80,1.4,'rgba(68,50,30,.45)');
      ctx.save(); ctx.translate(cx,cy+18); ctx.rotate(-0.35); ell(0,0,44,15,0,'#e7d3a8','#92743f',1.5); for(let k=0;k<9;k++) ell(-34+k*8.5,(k%2?4:-4),4,6,0.3,mix('#fbbf24','#c2410c',clamp(d/14,0,1)),'#92400e',0.8); ctx.restore();
      txt('土の中',x0+8,y0+124,11.5,'#fef3c7','bold','left'); }
    else { ctx.fillStyle='#ecfccb'; ctx.fillRect(x0,y0,240,132); grass(x0,y0+40,240,92,10);
      if(i===1){ const n=molts(GHM,d); grasshopper(cx,cy+8,22+ghLen(d)*2.4,0.1+0.12*n,true); }
      else grasshopper(cx+6,cy+4,150,1,false); } }
  function timeline(S,M,y,d,ticks){ S.forEach((s)=>{ const a=tx(s[1]), b=tx(s[2]); ctx.fillStyle=s[3]; rrect(a,y,b-a-2,26,6); ctx.fill(); txt(s[0],(a+b)/2,y+18,13,'#0f172a','bold','center',b-a-6); });
    M.forEach((m)=>{ const x=tx(m); ctx.fillStyle='#166534'; ctx.beginPath(); ctx.moveTo(x,y+26); ctx.lineTo(x-4,y+33); ctx.lineTo(x+4,y+33); ctx.closePath(); ctx.fill(); });
    if(ticks){ for(let v=0;v<=DMAX;v+=10) txt(v+'日',tx(v),y+44,10.5,'#64748b','','center'); }
    const x=tx(d); ln(x,y-6,x,y+30,3,'#0e7490'); ctx.fillStyle='#0e7490'; ctx.beginPath(); ctx.moveTo(x-7,y-12); ctx.lineTo(x+7,y-12); ctx.lineTo(x,y-3); ctx.closePath(); ctx.fill(); }
  function seq(names,cur,x,y,extra){ let xx=x; names.forEach((n,i)=>{ if(i){ xx+=txt('→',xx+3,y,13,'#64748b','bold')+6; }
      if(i===cur){ xx+=chip(n,xx,y,13,'#cffafe','#0e7490'); } else xx+=txt(n,xx+2,y,13,'#334155','bold')+4; }); if(extra) txt(extra,xx+6,y,12.5,'#b91c1c','bold'); }
  function drawA(){ const d=day;
    ctx.fillStyle='#ecfeff'; rrect(6,4,628,44,10); ctx.fill();
    txt('たまごから '+Math.round(d)+'日目',18,34,22,'#0e7490','bold');
    txt('▼＝皮をぬぐ',626,22,11.5,'#166534','bold','right'); txt('下の帯を指でなぞると日数が変わります',626,40,11,'#64748b','','right');
    [[BF,BFM,'モンシロチョウ',bfInfo(d),drawBF],[GH,GHM,'バッタ（トノサマバッタ）',ghInfo(d),drawGH]].forEach((r,k)=>{ const y0=54+k*200, S=r[0], inf=r[3], si=stg(S,d);
      ctx.fillStyle='#f8fafc'; rrect(6,y0,628,192,10); ctx.fill(); ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; rrect(6,y0,628,192,10); ctx.stroke();
      ctx.save(); rrect(14,y0+8,240,132,8); ctx.clip(); r[4](14,y0+8,d); ctx.restore(); ctx.strokeStyle='#cbd5e1'; rrect(14,y0+8,240,132,8); ctx.stroke();
      txt(r[2],266,y0+26,15,'#334155','bold','left',360);
      txt(inf[0],266,y0+56,24,SCOL[S[si][0]],'bold','left',360);
      inf[1].forEach((l,j)=>txt(l,266,y0+82+j*22,13.5,j===0?'#0f172a':'#334155',j===0?'bold':'','left',360));
      timeline(S,r[1],y0+150,d,k===1); });
    ctx.fillStyle='#fff7ed'; rrect(6,458,628,40,10); ctx.fill();
    seq(['たまご','よう虫','さなぎ','成虫'],stg(BF,day),14,474,''); txt('（モンシロチョウ）',626,474,11.5,'#64748b','','right');
    seq(['たまご','よう虫','成虫'],stg(GH,day),14,493,'さなぎにならない'); txt('（バッタ）',626,493,11.5,'#64748b','','right'); }

  // ================= ② 体のつくりパズル
  const TCX=190, SL={head:{x:TCX,y:118},mune:{x:TCX,y:180},hara:{x:TCX,y:288}};
  const PCOL={head:'#fca5a5',mune:'#86efac',hara:'#93c5fd'}, PDK={head:'#b91c1c',mune:'#15803d',hara:'#1d4ed8'}, PNM={head:'頭',mune:'むね',hara:'はら',leg:'あし',wing:'はね'};
  const LEGY=[166,181,196], KNEE=[[46,150],[58,172],[52,222]], FOOT=[[62,122],[86,186],[76,270]];
  const LS=[]; for(let k=0;k<3;k++) for(const s of [-1,1]) LS.push({s:s,k:k});
  const HOME={head:[432,124],mune:[512,124],hara:[432,270],wing:[580,124]}, LHOME=[[520,218],[592,218],[520,290],[592,290],[520,362],[592,362]];
  let PZ=[], legOcc=[];
  function resetPZ(){ PZ=[]; ['head','mune','hara','wing'].forEach((t)=>PZ.push({t:t,x:HOME[t][0],y:HOME[t][1],hx:HOME[t][0],hy:HOME[t][1],pl:-1}));
    LHOME.forEach((h)=>PZ.push({t:'leg',x:h[0],y:h[1],hx:h[0],hy:h[1],pl:-1})); legOcc=[-1,-1,-1,-1,-1,-1]; msg=null; }
  const placed=(t)=>PZ.some((p)=>p.t===t&&p.pl>=0);
  function headShape(x,y){ [-1,1].forEach((s)=>poly([[x+s*6,y-16],[x+s*18,y-42],[x+s*30,y-60]],2.4,'#7f1d1d')); ell(x,y,22,18,0,PCOL.head,PDK.head,2); [-1,1].forEach((s)=>ell(x+s*14,y-3,7,9,s*0.3,'#1f2937')); ln(x-5,y+17,x-8,y+24,2,'#7f1d1d'); ln(x+5,y+17,x+8,y+24,2,'#7f1d1d'); }
  function muneShape(x,y){ ell(x,y,20,28,0,PCOL.mune,PDK.mune,2); ln(x,y-22,x,y+22,1,'rgba(21,128,61,.4)'); }
  function haraShape(x,y){ ell(x,y,28,66,0,PCOL.hara,PDK.hara,2); for(let k=1;k<7;k++){ const yy=y-66+k*132/7, hw=28*Math.sqrt(Math.max(0,1-Math.pow((yy-y)/66,2))); ln(x-hw+2,yy,x+hw-2,yy,1.2,'rgba(29,78,216,.45)'); } }
  function legShape(ax,ay,kx,ky,fx,fy){ poly([[ax,ay],[kx,ky],[fx,fy]],5,'#78350f'); dot(fx,fy,3,'#78350f'); }
  function wingShape(x,y,sc){ ctx.globalAlpha=0.55; [-1,1].forEach((s)=>{ ell(x+s*30*sc,y+50*sc,17*sc,56*sc,-s*0.28,'#e0f2fe','#38bdf8',1.5); ell(x+s*36*sc,y+62*sc,18*sc,44*sc,-s*0.5,'#e0f2fe','#38bdf8',1.5); }); ctx.globalAlpha=1; }
  function drawPiece(p){ if(p.t==='head') headShape(p.x,p.y); else if(p.t==='mune') muneShape(p.x,p.y); else if(p.t==='hara') haraShape(p.x,p.y);
    else if(p.t==='wing'){ if(p.pl>=0) wingShape(p.x,p.y-6,1); else wingShape(p.x,p.y-48,0.62); }
    else if(p.pl>=0){ const L=LS[p.pl]; legShape(TCX+L.s*16,LEGY[L.k],TCX+L.s*KNEE[L.k][0],KNEE[L.k][1],TCX+L.s*FOOT[L.k][0],FOOT[L.k][1]); }
    else legShape(p.x-26,p.y+10,p.x,p.y-16,p.x+24,p.y+14); }
  function hitPiece(x,y){ for(let i=PZ.length-1;i>=0;i--){ const p=PZ[i]; if(p.pl>=0) continue; const dx=x-p.x, dy=y-p.y;
      if(p.t==='hara'?(Math.abs(dx)<34&&Math.abs(dy)<70):(p.t==='head'?(Math.abs(dx)<34&&dy>-64&&dy<26):Math.hypot(dx,dy)<(p.t==='wing'?42:32))) return i; } return -1; }
  function say(t,c){ msg={t:t,c:c||'#b91c1c',life:3.2}; }
  function sendHome(p){ p.x=p.hx; p.y=p.hy; }
  function zoneAt(x,y){ const nr=(s,rx,ry)=>Math.abs(x-s.x)<rx&&Math.abs(y-s.y)<ry; return nr(SL.head,42,34)?'head':(nr(SL.mune,48,30)?'mune':(nr(SL.hara,56,80)?'hara':null)); }
  function drop(p){ const x=p.x, y=p.y; if(x>=378){ p.x=clamp(x,396,618); p.y=clamp(y,70,424); return; }
    const z=zoneAt(x,y);
    if(p.t==='head'||p.t==='mune'||p.t==='hara'){ const S=SL[p.t];
      if(z===p.t||Math.hypot(x-S.x,y-S.y)<46){ p.pl=1; p.x=S.x; p.y=S.y; say('○「'+PNM[p.t]+'」を置けた','#15803d'); return; }
      if(z){ say(p.t==='head'?'「頭」は いちばん前。目と しょっかく があるところだよ':(p.t==='mune'?'「むね」は 頭と はら の間だよ':'「はら」は いちばん後ろ。ふし（すじ）がたくさんあるよ')); }
      sendHome(p); return; }
    if(!placed('mune')){ if(z||x<378) say('先に「むね」を置こう。'+PNM[p.t]+'は 体のどこから出ているかな？','#b45309'); sendHome(p); return; }
    if(p.t==='wing'){ if(z==='mune'||Math.hypot(x-SL.mune.x,y-SL.mune.y)<62){ p.pl=1; p.x=SL.mune.x; p.y=SL.mune.y; say('○ はね は「むね」から出ている','#15803d'); return; }
      say(z==='hara'?'はね は「はら」ではなく「むね」から出ているよ。むねの上に置こう':(z==='head'?'頭にあるのは 目・しょっかく・口。はね は「むね」から':'はね は体のどこから出ているかな？'));
      sendHome(p); return; }
    let best=-1, bd=1e9; LS.forEach((L,j)=>{ if(legOcc[j]>=0) return; const kx=TCX+L.s*KNEE[L.k][0], ky=KNEE[L.k][1], ax=TCX+L.s*16, ay=LEGY[L.k];
      const dd=Math.min(Math.hypot(x-kx,y-ky),Math.hypot(x-ax,y-ay),Math.hypot(x-(TCX+L.s*FOOT[L.k][0]),y-FOOT[L.k][1])); if(dd<bd){ bd=dd; best=j; } });
    if(z==='hara'&&bd>34){ say('あし は「はら」からは出ていないよ。「むね」を見てみよう'); sendHome(p); return; }
    if(z==='head'&&bd>34){ say('頭にあるのは 目・しょっかく・口。あし は「むね」から出ているよ'); sendHome(p); return; }
    if(best>=0&&(bd<62||z==='mune')){ p.pl=best; legOcc[best]=PZ.indexOf(p); const n=legOcc.filter((v)=>v>=0).length; say('○ あし '+n+'本め（むねから）','#15803d'); return; }
    sendHome(p); }
  function drawB(){ const nP=PZ.filter((p)=>p.pl>=0).length, nL=legOcc.filter((v)=>v>=0).length, done=nP===PZ.length;
    ctx.fillStyle='#f8fafc'; rrect(6,6,368,436,10); ctx.fill(); ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1; rrect(6,6,368,436,10); ctx.stroke();
    ctx.fillStyle='#fffbeb'; rrect(382,6,252,436,10); ctx.fill(); ctx.strokeStyle='#fde68a'; rrect(382,6,252,436,10); ctx.stroke();
    txt('ここに組み立てる（上から見た図）',16,28,13,'#334155','bold','left',350); txt('パーツ',394,28,13,'#92400e','bold');
    ctx.setLineDash([6,5]); if(!placed('head')) ell(SL.head.x,SL.head.y,22,18,0,null,'#94a3b8',1.5); if(!placed('mune')) ell(SL.mune.x,SL.mune.y,20,28,0,null,'#94a3b8',1.5); if(!placed('hara')) ell(SL.hara.x,SL.hara.y,28,66,0,null,'#94a3b8',1.5); ctx.setLineDash([]);
    const on=PZ.filter((p)=>p.pl>=0), ord=['leg','hara','wing','mune','head'];
    ord.forEach((t)=>on.filter((p)=>p.t===t).forEach(drawPiece));
    if(placed('head')) txt('頭',SL.head.x,SL.head.y+12,13,PDK.head,'bold','center',0,true);
    if(placed('mune')) txt('むね',SL.mune.x,SL.mune.y+5,13,PDK.mune,'bold','center',0,true);
    if(placed('hara')) txt('はら',SL.hara.x,SL.hara.y+30,15,PDK.hara,'bold','center',0,true);
    if(nL){ chip('あし '+nL+'本',16,64,14,'#fef3c7','#92400e'); }
    if(placed('wing')) chip('はね 4まい',262,262,13,'#e0f2fe','#0369a1');
    PZ.forEach((p)=>{ if(p.pl>=0||(drag&&PZ[drag.i]===p)) return; drawPiece(p); txt(PNM[p.t],p.x,p.t==='hara'?p.y+84:(p.t==='leg'?p.y+34:p.y+(p.t==='wing'?50:42)),12.5,'#78350f','bold','center'); });
    if(drag){ const p=PZ[drag.i]; drawPiece(p); txt(PNM[p.t],p.x,p.y+(p.t==='hara'?84:40),12.5,'#78350f','bold','center'); }
    let t, c='#334155', bg='#f1f5f9';
    if(done){ t='完成！ こん虫の体は「頭・むね・はら」の3つ。むねに あし6本・はね4まい'; c='#15803d'; bg='#dcfce7'; }
    else if(msg){ t=msg.t; c=msg.c; bg=msg.c==='#15803d'?'#f0fdf4':(msg.c==='#b45309'?'#fffbeb':'#fef2f2'); }
    else t='パーツを指で動かして、左の点線の所に こん虫の体を組み立てよう（置けた '+nP+'/'+PZ.length+'）';
    ctx.fillStyle=bg; rrect(6,450,628,46,10); ctx.fill(); txt(t,320,479,15,c,'bold','center',608); }

  // ================= ③ こん虫かな？
  const QZ=[{n:'アリ',ok:1,d:'体が 頭・むね・はら の3つに分かれていて、むねから あしが6本出ている。こん虫です。'},
            {n:'クモ',ok:0,d:'体が2つ（頭とむねが1つになった部分と、はら）で、あしが8本。こん虫ではありません。'},
            {n:'テントウムシ',ok:1,d:'丸く見えるが、かたいはねの下に はらがある。頭・むね・はら の3つで、あし6本。こん虫です。'},
            {n:'ダンゴムシ',ok:0,d:'体がたくさんのふしに分かれていて、あしが14本。こん虫ではありません（エビやカニに近いなかま）。'},
            {n:'トンボ',ok:1,d:'頭・むね・はら の3つに分かれ、むねから はね4まいと あし6本が出ている。こん虫です。'},
            {n:'ムカデ',ok:0,d:'体がたくさんのふしに分かれていて、ふしごとに あしがある（30本以上）。こん虫ではありません。'}];
  let qi=0, qans=null, qscore=0, qlog=[];
  function legs(list,col,w){ list.forEach((g)=>poly(g,w||3,col)); }
  function animal(k,x,y){ const F=[], LB=[];
    if(k===0){ const c='#292524'; const G=[]; [[-40,[50,-66],[64,-84]],[-28,[66,-30],[80,-14]],[-16,[54,8],[66,54]]].forEach((a)=>[-1,1].forEach((s)=>G.push([[x+s*8,y+a[0]],[x+s*a[1][0],y+a[1][1]],[x+s*a[2][0],y+a[2][1]]])));
      legs(G,c,3); G.forEach((g)=>F.push(g[2])); [-1,1].forEach((s)=>poly([[x+s*7,y-82],[x+s*14,y-108],[x+s*38,y-118]],2.2,c));
      ell(x,y-70,18,15,0,c); ell(x,y-28,11,22,0,c); dot(x,y+2,6,c); ell(x,y+44,25,34,0,c); [-1,1].forEach((s)=>dot(x+s*8,y-74,3,'#78716c'));
      LB.push(['頭',x,y-70,'head'],['むね',x,y-28,'mune'],['はら',x,y+44,'hara']); }
    else if(k===1){ const c='#57534e'; const G=[]; const KN=[[64,-104],[86,-56],[86,-12],[70,36]], FT=[[92,-146],[128,-70],[128,12],[104,96]];
      for(let j=0;j<4;j++) [-1,1].forEach((s)=>G.push([[x+s*18,y-58+j*13],[x+s*KN[j][0],y+KN[j][1]],[x+s*FT[j][0],y+FT[j][1]]]));
      legs(G,c,3.2); G.forEach((g)=>F.push(g[2])); [-1,1].forEach((s)=>poly([[x+s*8,y-66],[x+s*16,y-80],[x+s*12,y-90]],3,c));
      ell(x,y+48,40,50,0,'#78716c',c,2); ell(x,y-36,30,32,0,'#a8a29e',c,2); [[-6,-58],[6,-58],[-12,-54],[12,-54]].forEach((p)=>dot(x+p[0],y+p[1],2.4,'#1c1917'));
      for(let j=0;j<4;j++) ell(x,y+30+j*14,10-j*2,3,0,'rgba(41,37,36,.35)');
      LB.push(['頭とむね（1つ）',x,y-36,'mune'],['はら',x,y+48,'hara']); }
    else if(k===2){ const c='#1c1917'; const G=[]; [[-44,[46,-58],[64,-74]],[-30,[60,-16],[78,-6]],[-14,[56,36],[70,62]]].forEach((a)=>[-1,1].forEach((s)=>G.push([[x+s*18,y+a[0]],[x+s*a[1][0],y+a[1][1]],[x+s*a[2][0],y+a[2][1]]])));
      legs(G,c,3); G.forEach((g)=>F.push(g[2])); [-1,1].forEach((s)=>poly([[x+s*8,y-70],[x+s*16,y-84],[x+s*20,y-88]],2,c));
      ell(x,y+10,58,62,0,'#dc2626','#7f1d1d',2); ln(x,y-48,x,y+70,1.5,'#7f1d1d');
      [[-26,-12,9],[26,-12,9],[-34,28,8],[34,28,8],[-14,42,7],[14,42,7],[0,-44,11]].forEach((p)=>dot(x+p[0],y+p[1],p[2],c));
      ell(x,y-50,32,15,0,c); dot(x-18,y-50,5,'#f8fafc'); dot(x+18,y-50,5,'#f8fafc'); ell(x,y-66,17,9,0,c); dot(x-8,y-68,2.6,'#f8fafc'); dot(x+8,y-68,2.6,'#f8fafc');
      LB.push(['頭',x,y-68,'head'],['むね',x,y-50,'mune'],['はら（はねの下）',x,y+16,'hara']); }
    else if(k===3){ const c='#334155'; const G=[]; for(let j=0;j<7;j++){ const yy=y-56+j*17; [-1,1].forEach((s)=>{ const hw=52*Math.sqrt(Math.max(0,1-Math.pow((yy-y)/96,2))); G.push([[x+s*(hw-4),yy],[x+s*(hw+12),yy+4],[x+s*(hw+16),yy+12]]); }); }
      legs(G,c,2.6); G.forEach((g)=>F.push(g[2])); [-1,1].forEach((s)=>poly([[x+s*10,y-88],[x+s*26,y-110],[x+s*42,y-118]],2.2,c));
      ell(x,y,52,94,0,'#64748b',c,2); for(let j=1;j<11;j++){ const yy=y-94+j*188/11, hw=52*Math.sqrt(Math.max(0,1-Math.pow((yy-y)/94,2))); ln(x-hw+3,yy,x+hw-3,yy,1.6,'#334155'); }
      LB.push(['たくさんのふし',x,y,'hara']); }
    else if(k===4){ const c='#1e293b'; const G=[]; [[-68,[22,-84],[30,-96]],[-60,[28,-66],[36,-56]],[-52,[24,-44],[30,-30]]].forEach((a)=>[-1,1].forEach((s)=>G.push([[x+s*8,y+a[0]],[x+s*a[1][0],y+a[1][1]],[x+s*a[2][0],y+a[2][1]]])));
      ctx.globalAlpha=0.5; [-1,1].forEach((s)=>{ ell(x+s*66,y-70,64,12,s*-0.05,'#e0f2fe','#0ea5e9',1.2); ell(x+s*66,y-46,64,15,s*0.08,'#e0f2fe','#0ea5e9',1.2); }); ctx.globalAlpha=1;
      ctx.fillStyle='#0369a1'; ctx.beginPath(); ctx.moveTo(x-6,y-40); ctx.lineTo(x+6,y-40); ctx.lineTo(x+4,y+118); ctx.lineTo(x-4,y+118); ctx.closePath(); ctx.fill(); for(let j=0;j<9;j++) ln(x-6,y-28+j*16,x+6,y-28+j*16,1.2,'#0c4a6e');
      legs(G,c,2.4); G.forEach((g)=>F.push(g[2])); ell(x,y-58,15,22,0,'#0284c7',c,1.5); ell(x,y-92,20,14,0,'#0ea5e9',c,1.5); dot(x-11,y-94,9,'#075985'); dot(x+11,y-94,9,'#075985');
      LB.push(['頭',x,y-92,'head'],['むね',x,y-58,'mune'],['はら',x,y+50,'hara']); }
    else { const c='#7c2d12'; const n=15; for(let j=0;j<n;j++){ const yy=y-104+j*15; [-1,1].forEach((s)=>ln(x+s*16,yy,x+s*(34+(j%2)*3),yy+8,2.2,'#c2410c')); ctx.fillStyle=j%2?'#7c2d12':'#9a3412'; rrect(x-17,yy-7,34,14,5); ctx.fill(); }
      ctx.fillStyle='#ea580c'; rrect(x-15,y-130,30,22,8); ctx.fill(); [-1,1].forEach((s)=>poly([[x+s*8,y-128],[x+s*24,y-150],[x+s*40,y-160]],2,c)); ln(x-4,y+108,x-14,y+124,2,c); ln(x+4,y+108,x+14,y+124,2,c);
      LB.push(['たくさんのふし',x,y,'hara']); }
    return {F:F,LB:LB}; }
  const QBTN={y:426,h:64};
  function drawC(){ const done=qi>=QZ.length;
    ctx.fillStyle='#ecfeff'; rrect(6,4,628,44,10); ctx.fill();
    if(done){ txt('けっか',18,33,20,'#0e7490','bold'); txt('せいかい '+qscore+' / '+QZ.length,626,33,18,'#0e7490','bold','right');
      ctx.fillStyle='#f0fdf4'; rrect(6,56,628,362,10); ctx.fill();
      txt(QZ.length+'問中 '+qscore+'問 せいかい！',320,104,28,qscore===QZ.length?'#15803d':'#0e7490','bold','center');
      txt('こん虫：アリ・テントウムシ・トンボ',320,160,18,'#15803d','bold','center'); txt('こん虫ではない：クモ・ダンゴムシ・ムカデ',320,196,18,'#b91c1c','bold','center');
      txt('見分け方：体が「頭・むね・はら」の3つ ＋ むねに あしが6本 → こん虫',320,250,15,'#0f172a','bold','center',600);
      QZ.forEach((q,i)=>txt((qlog[i]?'○ ':'× ')+q.n,90+(i%3)*190,300+Math.floor(i/3)*34,15,qlog[i]?'#15803d':'#b91c1c','bold','left'));
      ctx.fillStyle='#0e7490'; rrect(170,QBTN.y,300,QBTN.h,14); ctx.fill(); txt('もういちど はじめから ↻',320,QBTN.y+40,19,'#fff','bold','center'); return; }
    const q=QZ[qi]; txt('もんだい '+(qi+1)+' / '+QZ.length,18,33,18,'#0e7490','bold'); txt('これは こん虫かな？',320,33,19,'#0f172a','bold','center'); txt('せいかい '+qscore,626,33,15,'#0e7490','bold','right');
    ctx.fillStyle='#fff'; rrect(6,54,628,282,10); ctx.fill(); ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; rrect(6,54,628,282,10); ctx.stroke();
    chip(q.n,18,84,20,'#f1f5f9','#0f172a');
    ctx.save(); ctx.translate(320,196); ctx.scale(0.86,0.86); const A=animal(qi,0,0); ctx.restore();
    if(qans!==null){ const tr=(p)=>[320+p[0]*0.86,196+p[1]*0.86];
      if(A.F.length<=14) A.F.forEach((f,i)=>{ const p=tr(f); dot(p[0],p[1],9,'#fff'); ctx.strokeStyle='#ea580c'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.arc(p[0],p[1],9,0,Math.PI*2); ctx.stroke(); txt(String(i+1),p[0],p[1]+4.5,11,'#c2410c','bold','center'); });
      A.LB.forEach((b,i)=>{ const p=tr([b[1],b[2]]), lx=470+(i%2)*0; const ly=96+i*44; ln(p[0]+8,p[1],lx,ly-6,1.2,PDK[b[3]]); chip(b[0],lx,ly,14,b[3]==='head'?'#fee2e2':(b[3]==='mune'?'#dcfce7':'#dbeafe'),PDK[b[3]]); });
      const nl=qi===5?'30本以上':(A.F.length+'本'); chip('あし '+nl,18,320,15,'#ffedd5','#c2410c'); }
    ctx.fillStyle=qans===null?'#f8fafc':(qans?'#dcfce7':'#fee2e2'); rrect(6,342,628,78,10); ctx.fill();
    if(qans===null){ txt('ヒント：体はいくつに分かれている？ あしは何本？',320,376,16,'#475569','bold','center',600); txt('下のボタンで答えよう',320,402,13,'#64748b','','center'); }
    else { txt((qans?'○ せいかい！':'× ざんねん…')+'　'+q.n+'は'+(q.ok?'こん虫です':'こん虫ではありません'),18,368,17,qans?'#15803d':'#b91c1c','bold','left',604); wrap(q.d,18,394,604,20,14,'#0f172a',''); }
    if(qans===null){ ctx.fillStyle='#16a34a'; rrect(14,QBTN.y,300,QBTN.h,14); ctx.fill(); txt('○ こん虫',164,QBTN.y+41,22,'#fff','bold','center');
      ctx.fillStyle='#dc2626'; rrect(326,QBTN.y,300,QBTN.h,14); ctx.fill(); txt('× こん虫ではない',476,QBTN.y+41,22,'#fff','bold','center'); }
    else { ctx.fillStyle='#0e7490'; rrect(170,QBTN.y,300,QBTN.h,14); ctx.fill(); txt(qi<QZ.length-1?'つぎの もんだいへ ▶':'けっかを見る ▶',320,QBTN.y+40,20,'#fff','bold','center'); } }
  function tapC(x,y){ if(y<QBTN.y||y>QBTN.y+QBTN.h) return false;
    if(qi>=QZ.length){ if(x>170&&x<470){ qi=0; qans=null; qscore=0; qlog=[]; } return true; }
    if(qans===null){ let a=null; if(x>14&&x<314) a=1; else if(x>326&&x<626) a=0; if(a===null) return true; qans=(a===QZ[qi].ok); qlog[qi]=qans; if(qans) qscore++; }
    else if(x>170&&x<470){ qi++; qans=null; } return true; }

  // ================= ④ 植物の育ち方
  const PL={hosenka:{n:'ホウセンカ',H:50,mid:42,sc:9,st:[['たね',0,6],['芽が出る（子葉）',6,14],['葉がふえる・くきがのびる',14,60],['花がさく',60,80],['実ができる',80,145],['かれる',145,170]],
      ds:['小さな茶色いたね（直径 約3mm）を土にまく。水をやると、たねが水をすって ふくらむ','はじめに出る葉（子葉）は2まい。丸い形をしている','子葉とちがう形の葉（細長くて、ふちがギザギザ）がふえ、くきがのびて太くなる','くきと葉のつけねに、赤・ピンク・白などの花がさく','花のあとに実ができる。じゅくした実にさわると、はじけてたねがとび出す','たねをのこして、葉もくきも根も かれる']},
    himawari:{n:'ヒマワリ',H:180,mid:52,sc:9,st:[['たね',0,8],['芽が出る（子葉）',8,16],['葉がふえる・くきがのびる',16,70],['花がさく',70,95],['実（たね）ができる',95,140],['かれる',140,170]],
      ds:['しまもようのあるたね（長さ 約1cm）を土にまく。水をやると、たねが水をすって ふくらむ','はじめに出る葉（子葉）は2まい。たまご形をしている','大きなハート形の葉がふえ、くきがぐんぐんのびて太くなる','くきの先に、大きな黄色い花がさく','花のあとに、たくさんのたねができる。重くなって下を向く','たねをのこして、葉もくきも根も かれる']}};
  const PSHORT=['たね','子葉','葉がふえる','花','実','かれる'], PCL=['#fde68a','#bbf7d0','#86efac','#fbcfe8','#fed7aa','#d6d3d1'], PMAX=170;
  const ptx=(d)=>20+d*600/PMAX;
  function pH(P,d){ if(d<P.st[1][1]) return 0; return Math.max(1,P.H/(1+Math.exp(-(Math.min(d,P.st[5][1])-P.mid)/P.sc))); }
  function mdate(d){ const ms=[31,30,31,31,30,31]; let m=5, dd=1+Math.floor(d); while(dd>ms[m-5]){ dd-=ms[m-5]; m++; } return m+'月'+dd+'日'; }
  function drawD(){ const P=PL[$('pl').value], d=pday, si=stg(P.st,d), h=pH(P,d), g=P.st[1][1], GY=318, PX=206, k=262/P.H, hima=P.n==='ヒマワリ';
    const wf=clamp((d-P.st[5][1]+6)/14,0,1);
    const sky=ctx.createLinearGradient(0,8,0,GY); sky.addColorStop(0,'#bae6fd'); sky.addColorStop(1,'#f0f9ff'); ctx.save(); rrect(6,6,376,410,10); ctx.clip();
    ctx.fillStyle=sky; ctx.fillRect(6,6,376,GY-6); ctx.fillStyle='#a07850'; ctx.fillRect(6,GY,376,100); for(let j=0;j<40;j++) dot(10+(j*61)%368,GY+8+(j*37)%90,1.5,'rgba(60,40,20,.4)');
    ln(6,GY,382,GY,2,'#78350f');
    // ものさし
    ln(30,GY,30,GY-262,2,'#94a3b8'); const stp=hima?20:10; for(let v=0;v<=P.H;v+=stp){ const yy=GY-v*k; ln(30,yy,v%(stp*2)?36:40,yy,1.5,'#94a3b8'); if(v%(stp*2)===0) txt(v+'cm',44,v?yy+4:yy-4,10.5,'#475569','bold'); }
    const LB=[];
    if(d<g){ const sw=Math.min(1,d/2); ell(PX,GY+16,(hima?5:4)*(1+0.3*sw),(hima?9:4)*(1+0.3*sw),hima?0.3:0,hima?'#57534e':'#78350f','#292524',1); if(hima) ln(PX-2,GY+9,PX+2,GY+23,1,'#e7e5e4');
      if(d>g-2.5){ ln(PX,GY+22,PX+1,GY+22+(d-g+2.5)*6,2,'#fafaf9'); }
      LB.push(['たね',PX+10,GY+16,'#78350f']); }
    else { const rl=Math.min(92,10+(d-g)*2.6), rc=mix('#fafaf9','#a8a29e',wf);
      ctx.strokeStyle=rc; ctx.lineWidth=hima?3.2:2.4; ctx.lineCap='round'; ctx.beginPath(); ctx.moveTo(PX,GY); ctx.quadraticCurveTo(PX+4,GY+rl*0.5,PX-1,GY+rl); ctx.stroke();
      ctx.lineWidth=1.3; const nr=Math.min(7,Math.floor((d-g)/4)); for(let j=1;j<=nr;j++){ const yy=GY+6+j*rl/(nr+1.5), s=j%2?1:-1, rr=Math.min(34,6+(d-g)*0.9)*(1-j/(nr+3)); ctx.beginPath(); ctx.moveTo(PX,yy); ctx.quadraticCurveTo(PX+s*rr*0.6,yy+3,PX+s*rr,yy+10); ctx.stroke(); }
      LB.push(['根',PX+14,GY+rl*0.55,'#78350f']);
      const top=GY-h*k, stc=mix(hima?'#4d7c0f':'#86a35a',hima?'#a16207':'#a8a29e',wf), sw=hima?Math.min(7,2+h/22):Math.min(5,2+h/10);
      const droop=hima&&d>95?clamp((d-95)/20,0,1):0;
      ctx.strokeStyle=stc; ctx.lineWidth=sw; ctx.beginPath(); ctx.moveTo(PX,GY); ctx.quadraticCurveTo(PX-2,(GY+top)/2,PX+droop*10,top); ctx.stroke();
      const yc=GY-Math.min(h*k,hima?20:14), cotA=clamp(1-(d-(hima?50:40))/12,0,1);
      if(cotA>0){ ctx.globalAlpha=cotA; const cc=mix('#84cc16','#d9c27a',1-cotA); [-1,1].forEach((s)=>{ ell(PX+s*(hima?11:8),yc-2,hima?11:8,hima?6:6.5,s*-0.25,cc,'#3f6212',1); }); ctx.globalAlpha=1; }
      const nL=clamp(Math.floor((d-g-5)/(hima?3.2:2.6)),0,hima?18:24), lc=mix(hima?'#15803d':'#16a34a','#a16207',wf);
      let lfP=null;
      for(let j=0;j<nL;j++){ const t=(j+1)/(nL+1), yy=yc-t*(yc-top), s=j%2?1:-1, grow=clamp((nL-j)/3,0.35,1);
        const len=(hima?Math.min(46,10+h*0.35):Math.min(34,8+h*0.7))*grow, wid=hima?len*0.42:len*0.2;
        leafE(PX+droop*10*t*t,yy,len,wid,s<0?Math.PI+0.5-t*0.3:-0.5+t*0.3,lc); if(j===Math.floor(nL*0.4)) lfP=[PX+s*len*0.6,yy-len*0.25]; }
      if(nL>0&&lfP) LB.push(['葉',lfP[0],lfP[1],'#15803d']); else if(cotA>0) LB.push(['子葉',PX+14,yc-2,'#4d7c0f']);
      if(h*k>30) LB.push(['くき',PX+3,(GY+Math.max(top,yc-30))/2+10,'#4d7c0f']);
      if(!hima){ const nf=d>=60&&d<150?Math.min(8,Math.floor((d-58)/2.5)):0, fade=d>=80?clamp(1-(d-80)/60,0,1):1, nfr=d>=78?Math.min(8,Math.floor((d-76)/3)):0;
        let fp=null, frp=null;
        for(let j=0;j<8;j++){ const t=0.35+0.55*j/8, yy=yc-t*(yc-top), s=j%2?-1:1, xx=PX+s*7;
          if(j<nfr){ ell(xx+s*3,yy+8,3.5,8,s*0.2,wf>0.3?mix('#84cc16','#a16207',wf):'#86c06a','#3f6212',1); if(!frp) frp=[xx+s*3,yy+8]; }
          else if(j<nf&&fade>0.05){ ctx.globalAlpha=Math.max(0.25,fade); [0,1,2].forEach((q)=>ell(xx+s*(4+q*3),yy+4+q*2,4.5,3.5,0,'#f472b6','#be185d',0.8)); ctx.globalAlpha=1; if(!fp) fp=[xx+s*10,yy+6]; } }
        if(fp) LB.push(['花',fp[0],fp[1],'#be185d']); if(frp) LB.push(['実',frp[0],frp[1],'#a16207']); }
      else if(d>=55){ const hx=PX+droop*10, hy=top+droop*14, R=d<70?6+(d-55)*0.4:20;
        if(d<70){ ell(hx,hy-4,R,R,0,'#65a30d','#3f6212',1.5); LB.push(['つぼみ',hx+R,hy-4,'#4d7c0f']); }
        else { const pet=d<100?1:clamp(1-(d-100)/15,0,1); if(pet>0){ ctx.globalAlpha=pet; for(let q=0;q<16;q++){ const a=q/16*Math.PI*2; ell(hx+Math.cos(a)*(R+7),hy+Math.sin(a)*(R+7)*(1-droop*0.5),8,3.4,a,'#facc15','#ca8a04',0.8); } ctx.globalAlpha=1; }
          ell(hx,hy,R,R*(1-droop*0.5),0,d<95?'#78350f':mix('#78350f','#44403c',wf),'#451a03',1.5); for(let q=0;q<14;q++) dot(hx+((q*7)%13-6)*R/8,hy+((q*5)%11-5)*R/8*(1-droop*0.5),1.3,'#a16207');
          LB.push([d<95?'花':'実（たね）',hx+R+8,hy,d<95?'#ca8a04':'#78350f']); } } }
    ctx.restore();
    // 名前の札
    const used=[]; LB.forEach((b)=>{ let ly=b[2]; for(const u of used) if(Math.abs(u-ly)<26) ly=u+26; used.push(ly); const lx=300; ln(b[1],b[2],lx-4,ly-6,1.2,b[3]); chip(b[0],lx,ly,14,'#ffffff',b[3]); });
    // 右の説明
    ctx.fillStyle='#f8fafc'; rrect(390,6,244,410,10); ctx.fill(); ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; rrect(390,6,244,410,10); ctx.stroke();
    txt(P.n,402,34,18,'#0f172a','bold'); txt('たねまきから '+Math.round(d)+'日目',402,60,15,'#0e7490','bold','left',224); txt('（5月1日にまくと '+mdate(d)+'ごろ）',402,80,12,'#64748b','','left',224);
    const ly=wrap(P.st[si][0],402,112,224,24,20,'#15803d','bold');
    const dy=wrap(P.ds[si],402,ly+28,224,20,13.5,'#0f172a','');
    txt(d<g?'高さ 0cm（まだ芽が出ていない）':'高さ 約'+Math.round(h)+'cm',402,Math.max(dy+34,250),15,'#334155','bold','left',224);
    ctx.fillStyle='#ecfdf5'; rrect(398,330,228,78,10); ctx.fill(); wrap('植物の体は 根・くき・葉 からできている。育つ順番は、どの植物も同じ',408,356,210,20,13.5,'#047857','bold');
    // タイムライン
    P.st.forEach((s,i)=>{ const a=ptx(s[1]), b=ptx(s[2]); ctx.fillStyle=PCL[i]; rrect(a,428,b-a-2,26,6); ctx.fill(); txt(PSHORT[i],(a+b)/2,446,12.5,'#0f172a','bold','center',b-a-6); });
    [[0,'5月'],[31,'6月'],[61,'7月'],[92,'8月'],[123,'9月'],[153,'10月']].forEach((m)=>{ ln(ptx(m[0]),458,ptx(m[0]),464,1,'#94a3b8'); txt(m[1],ptx(m[0])+3,476,11,'#64748b','','left'); });
    const x=ptx(d); ln(x,422,x,458,3,'#0e7490'); ctx.fillStyle='#0e7490'; ctx.beginPath(); ctx.moveTo(x-7,416); ctx.lineTo(x+7,416); ctx.lineTo(x,425); ctx.closePath(); ctx.fill();
    txt('下の帯を指でなぞると日数が変わります',626,494,11,'#64748b','','right'); }

  // ================= 共通
  function draw(){ ctx.fillStyle='#fff'; ctx.fillRect(0,0,W,H); if(mode==='A') drawA(); else if(mode==='B') drawB(); else if(mode==='C') drawC(); else drawD(); }
  function update(){
    if(mode==='A'){ const b=BF[stg(BF,day)][0], g=GH[stg(GH,day)][0];
      setK('s1','たまごから'); setK('s2','モンシロチョウ'); setK('s3','バッタ'); setK('s4','わかること');
      setV('s1',Math.round(day)+'日目'); setV('s2',b); setV('s3',g); setV('s4','さなぎになるのはチョウだけ');
      setShare('【こん虫の育ち方】たまごから'+Math.round(day)+'日目：モンシロチョウは'+b+'、バッタは'+g+'。チョウは「たまご→よう虫→さなぎ→成虫」、バッタはさなぎにならない｜シミュラボ'); }
    else if(mode==='B'){ const nP=PZ.filter((p)=>p.pl>=0).length, nL=legOcc.filter((v)=>v>=0).length, bp=['head','mune','hara'].filter(placed).map((t)=>PNM[t]);
      setK('s1','置けたパーツ'); setK('s2','あしの数'); setK('s3','置けた体の部分'); setK('s4','わかること');
      setV('s1',nP+' / '+PZ.length); setV('s2',nL+'本'); setV('s3',bp.length?bp.join('・'):'まだ'); setV('s4',nP===PZ.length?'頭・むね・はら＋あし6本':'あしは どこから出る？');
      setShare('【こん虫の体のつくり】パズルで組み立てると、こん虫の体は頭・むね・はらの3つ。あし6本とはねは、すべて「むね」から出ている｜シミュラボ'); }
    else if(mode==='C'){ const done=qi>=QZ.length;
      setK('s1','もんだい'); setK('s2','せいかい'); setK('s3','見分け方'); setK('s4','こたえ');
      setV('s1',done?'おわり':(qi+1)+' / '+QZ.length); setV('s2',qscore+'問'); setV('s3','体3つ・あし6本');
      setV('s4',done?'こん虫は3種類':(qans===null?'？':(QZ[qi].ok?'こん虫':'こん虫ではない')));
      setShare('【こん虫かな？クイズ】'+(done?QZ.length+'問中'+qscore+'問せいかい！':'挑戦中')+'　体が頭・むね・はらの3つで、むねにあしが6本ならこん虫。クモ（あし8本）やダンゴムシ（あし14本）はこん虫ではない｜シミュラボ'); }
    else { const P=PL[$('pl').value], s=P.st[stg(P.st,pday)][0], h=pH(P,pday);
      setK('s1','たねまきから'); setK('s2','ようす'); setK('s3','高さ（目安）'); setK('s4','わかること');
      setV('s1',Math.round(pday)+'日目'); setV('s2',s); setV('s3',pday<P.st[1][1]?'0cm':'約'+Math.round(h)+'cm'); setV('s4','体は根・くき・葉');
      setShare('【植物の育ち方】'+P.n+'はたねまきから'+Math.round(pday)+'日目で「'+s+'」。たね→子葉→葉がふえる→花→実→かれる の順に育ち、体は根・くき・葉｜シミュラボ'); } }
  function setPlay(){ $('play').textContent=run?'⏸ 止める':'▶ 早送り'; }
  function setMode(m){ mode=m; run=false; drag=null; setPlay();
    ['tA','tB','tC','tD'].forEach((id)=>{ $(id).className='btn '+(id==='t'+m?'btn-primary':'btn-ghost'); });
    fld('day').style.display=m==='A'?'':'none'; fld('pl').style.display=m==='D'?'':'none'; fld('pday').style.display=m==='D'?'':'none';
    $('play').style.display=(m==='A'||m==='D')?'':'none'; $('rst').style.display=(m==='A'||m==='D')?'':'none';
    $('shuf').style.display=m==='B'?'':'none'; $('ans').style.display=m==='B'?'':'none';
    update(); draw(); }
  function setDay(v){ day=clamp(v,0,DMAX); $('day').value=day; $('dayL').textContent=Math.round(day)+'日目'; }
  function setPday(v){ pday=clamp(v,0,PMAX); $('pday').value=pday; $('pdayL').textContent=Math.round(pday)+'日目'; }
  $('tA').addEventListener('click',()=>setMode('A')); $('tB').addEventListener('click',()=>setMode('B')); $('tC').addEventListener('click',()=>setMode('C')); $('tD').addEventListener('click',()=>setMode('D'));
  $('day').addEventListener('input',()=>{ day=+$('day').value; update(); });
  $('pday').addEventListener('input',()=>{ pday=+$('pday').value; update(); });
  $('pl').addEventListener('change',()=>{ update(); });
  $('play').addEventListener('click',()=>{ if(mode==='A'&&!run&&day>=DMAX-0.01) setDay(0); if(mode==='D'&&!run&&pday>=PMAX-0.01) setPday(0); run=!run; setPlay(); });
  $('rst').addEventListener('click',()=>{ run=false; if(mode==='A') setDay(0); else setPday(0); setPlay(); update(); });
  $('shuf').addEventListener('click',()=>{ resetPZ(); update(); });
  $('ans').addEventListener('click',()=>{ resetPZ(); PZ.forEach((p,i)=>{ if(p.t==='leg'){ const j=legOcc.indexOf(-1); p.pl=j; legOcc[j]=i; } else { p.pl=1; p.x=SL[p.t]?SL[p.t].x:SL.mune.x; p.y=SL[p.t]?SL[p.t].y:SL.mune.y; } }); update(); });
  let scrub=false;
  function scrubAt(x,y){ if(mode==='A'&&((y>=196&&y<=250)||(y>=396&&y<=452))){ setDay(Math.round((x-TX0)/(TX1-TX0)*DMAX)); update(); return true; }
    if(mode==='D'&&y>=410&&y<=480){ setPday(Math.round((x-20)/600*PMAX)); update(); return true; } return false; }
  cv.addEventListener('pointerdown',(e)=>{ const p=cpos(cv,e), x=p[0]/dpr, y=p[1]/dpr;
    if(mode==='B'){ const i=hitPiece(x,y); if(i>=0){ drag={i:i,ox:x-PZ[i].x,oy:y-PZ[i].y}; const pc=PZ.splice(i,1)[0]; PZ.push(pc); legOcc=legOcc.map((v)=>v<0?v:(v>i?v-1:(v===i?PZ.length-1:v))); drag.i=PZ.length-1; try{ cv.setPointerCapture(e.pointerId); }catch(_){} e.preventDefault(); } return; }
    if(mode==='C'){ if(tapC(x,y)){ update(); e.preventDefault(); } return; }
    if(scrubAt(x,y)){ scrub=true; run=false; setPlay(); try{ cv.setPointerCapture(e.pointerId); }catch(_){} e.preventDefault(); } });
  cv.addEventListener('pointermove',(e)=>{ const p=cpos(cv,e), x=p[0]/dpr, y=p[1]/dpr;
    if(drag){ const q=PZ[drag.i]; q.x=clamp(x-drag.ox,10,630); q.y=clamp(y-drag.oy,10,490); e.preventDefault(); }
    else if(scrub){ if(mode==='A') setDay(Math.round((x-TX0)/(TX1-TX0)*DMAX)); else setPday(Math.round((x-20)/600*PMAX)); update(); e.preventDefault(); } });
  function endPtr(){ if(drag){ drop(PZ[drag.i]); drag=null; update(); } scrub=false; }
  cv.addEventListener('pointerup',endPtr); cv.addEventListener('pointercancel',endPtr);
  let last=performance.now(), acc=0;
  function loop(now){ const dt=Math.min(0.05,Math.max(0,(now-last)/1000)); last=now; tnow+=dt;
    if(run){ if(mode==='A'){ setDay(day+dt*4); if(day>=DMAX){ run=false; setPlay(); } } else if(mode==='D'){ setPday(pday+dt*10); if(pday>=PMAX){ run=false; setPlay(); } } }
    if(msg){ msg.life-=dt; if(msg.life<=0) msg=null; }
    acc+=dt; if(run||acc>0.3){ acc=0; update(); }
    draw(); requestAnimationFrame(loop); }
  resetPZ(); setDay(day); setPday(pday);
  const h0=(location.hash||'').replace('#',''); setMode(h0==='pazuru'?'B':(h0==='quiz'?'C':(h0==='shokubutsu'?'D':'A'))); requestAnimationFrame(loop);
'''

sim(slug="konchu-sodachi", cat="rika", emoji="🦋", score=80,
    title="こん虫の育ち方と体のつくりシミュレーター（モンシロチョウとバッタ・植物の育ち方）",
    title_tag="こん虫の育ち方と体のつくりシミュレーション｜モンシロチョウとバッタの育ち方・頭むねはら・植物の育ち方（小3理科）",
    meta_desc="小3理科「身の回りの生物」のシミュレーション。モンシロチョウ（たまご→よう虫→さなぎ→成虫）とバッタ（さなぎにならない）を日数スライダーと早送りでくらべられます。頭・むね・はら・あし6本を組み立てるパズル、クモやダンゴムシは「こん虫かな？」クイズ、ホウセンカ・ヒマワリの育ち方つき。",
    og_title="こん虫の育ち方と体のつくりシミュレーター（小3）",
    og_desc="モンシロチョウはさなぎになり、バッタはならない。早送りでくらべ、頭・むね・はら・あし6本のパズルと「こん虫かな？」クイズで体のつくりもたしかめる。",
    card_desc="チョウとバッタの育ち方を早送りでくらべ、頭・むね・はらのパズルと「こん虫かな？」クイズで体のつくりも。",
    lead="モンシロチョウとバッタを同じ日数でならべて、早送りで育ち方をくらべられます。頭・むね・はら・あしを組み立てるパズル、クモやダンゴムシが「こん虫かな？」のクイズ、植物（ホウセンカ・ヒマワリ）の育ち方の画面もあります。",
    model="小3 身の回りの生物（こん虫と植物の育ち方・体のつくり）", level="小学3年",
    unit="小学校 第3学年 B（1）身の回りの生物",
    canvas=canvas(640, 500, light=True),
    controls=slider("day", "たまごからの日数", 0, 60, 26, 1, "{v}日目")
             + select("pl", "植物", [("hosenka", "ホウセンカ"), ("himawari", "ヒマワリ")])
             + slider("pday", "たねまきからの日数", 0, 170, 65, 1, "{v}日目"),
    buttons=btn("tA", "🦋 ① 育ち方", True) + btn("tB", "🧩 ② 体のつくりパズル") + btn("tC", "❓ ③ こん虫かな？") + btn("tD", "🌻 ④ 植物の育ち方")
            + btn("play", "▶ 早送り", True) + btn("rst", "⏮ はじめにもどす") + btn("shuf", "🔀 パズルをやり直す") + btn("ans", "💡 答えを見る"),
    stats=stats([("s1", "たまごから", False), ("s2", "モンシロチョウ", False), ("s3", "バッタ", False), ("s4", "わかること", True)]),
    legend="図は形をわかりやすくした模式図で、たまごやよう虫は実際より大きくかいています。日数・体長・高さは、あたたかい季節の目安です。①④：下の帯を指でなぞると日数が変わります（▼＝皮をぬぐ日）。②：パーツを指で動かして組み立てます。③：下の大きなボタンで答えます。",
    article=KONCHU_ARTICLE, faqs=KONCHU_FAQS,
    rel=[("hatsuga-jouken", "🫘", "種子の発芽と成長の条件シミュレーター"), ("kisetsu-seibutsu", "🌸", "季節と生き物"),
         ("hito-karada", "🫀", "人の体のつくりと働き"), ("lotka-volterra", "🐰", "キツネとウサギ 増減シミュレーター"), ("taiyou-ugoki", "🌞", "太陽の1日の動きと季節")],
    js=KONCHU_JS)


# ============================================================ 2 季節と生き物
MN = ["4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月", "1月", "2月", "3月"]
TEMP = [14.3, 18.8, 21.9, 25.7, 26.9, 23.3, 18.0, 12.5, 7.7, 5.4, 6.1, 9.4]   # 気象庁 東京 平年値（1991〜2020年）4月〜3月
SEAS = ["春", "春", "夏", "夏", "夏", "秋", "秋", "秋", "冬", "冬", "冬", "春"]
def _M(lst):
    o = [None] * 12
    for (a, b), lv, sh, lg, stt in lst:
        for i in range(a, b + 1): o[i] = (lv, sh, lg, stt)
    assert all(o), lst
    return o
ORG = [
 ("ツバメ", "a", _M([((0, 0), 2, "巣をつくる", "南の国からやってきて、家ののき下などに、どろとかれ草で巣をつくる。", "nest"),
                    ((1, 1), 3, "ひなを育てる", "巣にたまごを産み、親がえさの虫を運んで ひなを育てる。", "hina"),
                    ((2, 2), 3, "ひなが巣立つ", "ひなが巣立つ。2回目の子育てをするものもいる。", "hina"),
                    ((3, 3), 3, "さかんにとぶ", "2回目のひなも巣立ち、若いツバメも空をとんで虫をとる。", "fly"),
                    ((4, 4), 2, "群れで集まる", "親子で群れをつくって集まり、南へ帰るじゅんびをする。", "flock"),
                    ((5, 5), 1, "南へわたる", "寒くなる前に、あたたかい南の国へ わたっていく。", "leave"),
                    ((6, 10), 0, "いない", "日本ではほとんど見られない。あたたかい南の国（東南アジアなど）ですごしている。", "gone"),
                    ((11, 11), 1, "やってくる", "3月の終わりごろから、南の国からやってくる（地方によってちがう）。", "fly")])),
 ("カエル", "a", _M([((0, 0), 1, "冬眠から目覚める", "土の中から出てきて、動き始める。", "wake"),
                    ((1, 1), 3, "鳴いてたまごを産む", "田んぼなどで さかんに鳴き、水の中にたまごを産む。", "eggs"),
                    ((2, 2), 3, "おたまじゃくし", "たまごから おたまじゃくしがかえり、水の中で育つ。", "tad"),
                    ((3, 3), 3, "子ガエルになる", "おたまじゃくしに あしが生え、子ガエルになって陸に上がる。", "young"),
                    ((4, 4), 3, "さかんに活動", "草むらなどで、さかんに虫を食べる。", "active"),
                    ((5, 5), 2, "活動", "虫を食べて、冬にそなえる。", "active"),
                    ((6, 6), 1, "動きがにぶい", "寒くなると、動きが にぶくなる。", "slow"),
                    ((7, 7), 0, "冬眠を始める", "土の中や落ち葉の下にもぐって、冬眠を始める。", "sleep"),
                    ((8, 10), 0, "冬眠", "土の中などで、じっと動かずに冬をこす（冬眠）。", "sleep"),
                    ((11, 11), 0, "冬眠", "まだ冬眠している。あたたかい日が続くと目覚める。", "sleep")])),
 ("テントウムシ", "a", _M([((0, 0), 3, "たまごを産む", "アブラムシを食べ、葉にたまごを産む。", "eggs"),
                    ((1, 1), 3, "よう虫・さなぎ", "よう虫がアブラムシを食べて育ち、さなぎになって成虫になる。", "larva"),
                    ((2, 2), 2, "新しい成虫", "新しく成虫になったテントウムシがふえる。", "adult"),
                    ((3, 4), 2, "活動", "草むらなどで見られる。暑すぎる日は、葉のかげなどで休む。", "adult"),
                    ((5, 6), 2, "活動", "すずしくなると、またアブラムシを食べて活動する。", "adult"),
                    ((7, 7), 1, "冬ごしの場所へ", "落ち葉の下や石のかげなどに 集まり始める。", "group"),
                    ((8, 10), 0, "成虫で冬ごし", "成虫のまま、落ち葉の下などに集まって、じっと冬をこす。", "group"),
                    ((11, 11), 1, "出てくる", "あたたかい日には、冬ごしの場所から出てくる。", "adult")])),
 ("カマキリ", "a", _M([((0, 0), 0, "たまごのまま", "えだについた あわのかたまり（らんのう）の中に、たまごがある。", "ootheca"),
                    ((1, 1), 1, "よう虫が出てくる", "5月の終わりごろ、らんのうから小さなよう虫が たくさん出てくる。", "hatch"),
                    ((2, 2), 2, "小さなよう虫", "小さなよう虫が 虫をとらえて食べ、皮をぬいで大きくなる。", "nymph"),
                    ((3, 3), 3, "よう虫が育つ", "皮をぬぐたびに大きくなる。", "nymph"),
                    ((4, 4), 3, "成虫になる", "最後に皮をぬいで、はねのある成虫になる。", "adult"),
                    ((5, 5), 3, "成虫", "バッタなどの虫をとらえて食べる。", "adult"),
                    ((6, 6), 2, "たまごを産む", "えだなどに、あわでつつんだ たまご（らんのう）を産む。", "lay"),
                    ((7, 7), 0, "たまごで冬ごし", "成虫は死んでしまい、らんのうの中のたまごで冬をこす。", "ootheca"),
                    ((8, 11), 0, "たまごで冬ごし", "らんのうの中のたまごで、冬をこす。", "ootheca")])),
 ("モンシロチョウ", "a", _M([((0, 0), 3, "成虫がとぶ", "さなぎで冬をこした成虫がとび、キャベツなどの葉にたまごを産む。", "adult"),
                    ((1, 1), 3, "たまご・よう虫", "たまご→よう虫→さなぎ→成虫と育ち、数がふえる。", "larva"),
                    ((2, 2), 3, "さかんにとぶ", "成虫がさかんにとび、花のみつをすう。", "adult"),
                    ((3, 4), 2, "活動", "成虫やよう虫が見られる。1年に何回も、たまごから成虫に育つ。", "adult"),
                    ((5, 5), 3, "さかんにとぶ", "すずしくなると、また数がふえる。", "adult"),
                    ((6, 6), 2, "活動", "成虫やよう虫が見られる。", "larva"),
                    ((7, 7), 1, "さなぎになる", "よう虫がさなぎになり、冬ごしのじゅんびをする。", "pupa"),
                    ((8, 10), 0, "さなぎで冬ごし", "さなぎのまま、かべや木のえだなどで じっと冬をこす。", "pupa"),
                    ((11, 11), 1, "成虫が出てくる", "あたたかくなると、さなぎから成虫が出てくる。", "adult")])),
 ("サクラ", "p", _M([((0, 0), 2, "花がちり葉が出る", "4月のはじめごろまで花がさき、花がちると葉が出てくる。", "hazakura"),
                    ((1, 3), 3, "葉がしげる", "葉がふえて こくしげり、えだがのびる。", "leaf"),
                    ((4, 4), 2, "葉がしげる", "葉がしげっている。えだには、来年の花や葉になる芽ができている。", "leaf"),
                    ((5, 5), 1, "葉の色が変わり始める", "葉が少しずつ 黄色や赤色に変わり始める。", "leafy"),
                    ((6, 6), 1, "葉が赤や黄色に", "葉が赤色や黄色に変わる。", "koyo"),
                    ((7, 7), 0, "葉が落ちる", "葉が落ちて、えだに芽（冬芽）が残る。", "fall"),
                    ((8, 10), 0, "芽で冬ごし", "葉は全部落ち、えだの芽（冬芽）で冬をこす。", "bare"),
                    ((11, 11), 2, "花がさく", "芽がふくらみ、3月の終わりごろに花がさく（東京）。", "flower")])),
 ("ヘチマ", "p", _M([((0, 0), 1, "たねをまく", "あたたかくなってきたら、たねをまく（4月の終わり〜5月）。", "seed"),
                    ((1, 1), 2, "芽が出る", "芽が出て子葉が開き、葉がふえていく。", "sprout"),
                    ((2, 2), 3, "くきがのびる", "くき（つる）がのび始め、まきひげでネットなどにからみつく。", "vine1"),
                    ((3, 3), 3, "ぐんぐんのびる・花", "くきが ぐんぐんのび、黄色い花がさく。", "flower"),
                    ((4, 4), 3, "実が大きくなる", "実ができて大きくなる。くきも まだよくのびる。", "fruit"),
                    ((5, 5), 2, "のびがゆっくり", "くきの のび方が ゆっくりになり、実が大きく育つ。", "fruit"),
                    ((6, 6), 1, "かれ始める", "葉が黄色くなってかれ始め、実が茶色くなる。", "wither"),
                    ((7, 7), 0, "かれる", "全体がかれる。実の中には 黒いたねができている。", "dead"),
                    ((8, 10), 0, "たねで冬ごし", "植物の体はかれて、たねで冬をこす。", "seedwinter"),
                    ((11, 11), 0, "たねで冬ごし", "たねのまま。あたたかくなったら、たねをまく。", "seedwinter")])),
 ("タンポポ", "p", _M([((0, 0), 3, "花がさく", "黄色い花がたくさんさき、わた毛（たね）ができる。", "flower"),
                    ((1, 1), 3, "わた毛がとぶ", "わた毛のついたたねが 風でとばされる。葉がよくしげる。", "fluff"),
                    ((2, 2), 3, "葉がしげる", "葉が大きく立ち上がって しげる。", "leaf"),
                    ((3, 4), 2, "葉がしげる", "葉がしげっている（花は少ない）。", "leaf"),
                    ((5, 5), 2, "また花がさく", "すずしくなると、また花がさくことがある。", "flower"),
                    ((6, 6), 1, "葉が地面に広がる", "葉を 地面に広げ始める。", "rosette"),
                    ((7, 10), 0, "ロゼットで冬ごし", "葉を地面にぴったり広げた形（ロゼット）で冬をこす。", "rosette"),
                    ((11, 11), 2, "花がさき始める", "あたたかくなると葉がのび、花がさき始める。", "flower")])),
]
GOYA = _M([((0, 0), 1, "たねをまく", "あたたかくなってきたら、たねをまく（4月の終わり〜5月）。", "seed"),
           ((1, 1), 2, "芽が出る", "芽が出て子葉が開き、葉がふえていく。", "sprout"),
           ((2, 2), 3, "くきがのびる", "くき（つる）がのび始め、まきひげでネットなどにからみつく。", "vine1"),
           ((3, 3), 3, "ぐんぐんのびる・花", "くきが ぐんぐんのび、黄色い花がさく。", "flower"),
           ((4, 4), 3, "実が大きくなる", "緑色の実（ゴーヤ）ができて大きくなる。くきも まだよくのびる。", "fruit"),
           ((5, 5), 2, "実がじゅくす", "のび方がゆっくりになる。じゅくした実は黄色くなり、われて赤いたねが見える。", "ripe"),
           ((6, 6), 1, "かれ始める", "葉が黄色くなって かれ始める。", "wither"),
           ((7, 7), 0, "かれる", "全体がかれる。たねが残る。", "dead"),
           ((8, 10), 0, "たねで冬ごし", "植物の体はかれて、たねで冬をこす。", "seedwinter"),
           ((11, 11), 0, "たねで冬ごし", "たねのまま。あたたかくなったら、たねをまく。", "seedwinter")])
ANI = [o for o in ORG if o[1] == "a"]; PLA = [o for o in ORG if o[1] == "p"]
ACTIVE = [sum(1 for o in ANI if o[2][i][0] >= 1) for i in range(12)]   # 活動している（見られる）動物の数
PGROW = [sum(o[2][i][0] for o in PLA) / len(PLA) for i in range(12)]
def pword(v): return "よく育つ" if v >= 2.3 else ("育つ" if v >= 1.5 else ("ゆっくり" if v >= 0.7 else "ほとんど育たない"))
import json as _json
ORG_JSON = _json.dumps([[o[0], o[1], [list(x) for x in o[2]]] for o in ORG], ensure_ascii=False)
GOYA_JSON = _json.dumps([list(x) for x in GOYA], ensure_ascii=False)

def _season_rows():
    rows = []
    for i in (0, 3, 6, 9):
        rows.append(["%s（%s）" % (MN[i], SEAS[i]), "%.1f℃" % TEMP[i]] + [o[2][i][1] for o in ORG])
    return rows

KISETSU_ARTICLE = "<h2>このシミュレーションでわかること</h2>\n" + P(
    "動物の活動や植物の成長は、<b>季節（気温）によってちがいます</b>。あたたかい季節には、動物の活動が<b>さかん</b>になり、植物は<b>よく育ちます</b>。"
    "寒い季節になると、動物は<b>たまご・よう虫・さなぎ・成虫</b>などのすがたで、土の中や落ち葉の下などで<b>冬ごし</b>をし、植物は<b>たね</b>を残してかれたり、<b>芽</b>や地面に広げた葉で冬をこしたりします。") + '''
<p>小学校4年の理科「<b>季節と生物</b>」（学習指導要領 第4学年 B（2））で学ぶ内容です。学習指導要領の解説（理科編 pp.54〜56）は、身近な動物は暖かい季節には数が多く活発に活動し、寒い季節には活動がにぶくなったり卵で冬をこしたりすること、植物は暖かくなる夏までは体全体がよく成長し、寒くなると成長がほとんど見られず、種子をつくってかれたり形を変えて冬をこしたりすることをとらえるようにするとしています。内容の取扱いでは、<b>1年を通じて動物の活動や植物の成長をそれぞれ2種類以上観察する</b>ことになっています。</p>
<p>月のスライダー（4月〜3月）を動かすと、その月の<b>平均気温のグラフ</b>（東京の平年値）と、動物5種類（ツバメ・カエル・テントウムシ・カマキリ・モンシロチョウ）、植物3種類（サクラ・ヘチマまたはツルレイシ・タンポポ）のようすが変わります。「この月を記録カードに」で選んだ月を最大4まいならべて、<b>観察カードのようにくらべる</b>ことができます。</p>
<h2>授業での使い方</h2>
<ul>
<li><b>導入</b>：春の観察の前に、「ツバメはいつごろやってくるかな」「冬の間、カエルやテントウムシはどこにいるのかな」と予想させます。今の月を選んで、これから観察する生き物を決めるのにも使えます。</li>
<li><b>展開</b>：1年間の観察で、実際の記録とシミュレーションの記録カードをくらべます。夏休みや冬休みなど、学校で観察できない時期のようすを補うのに使えます。地域によって時期はちがうので、「自分たちの町ではどうだったか」も話し合います。</li>
<li><b>まとめ</b>：「春夏秋冬の4まい」で4つの月をならべ、気温のグラフと見くらべて、「気温が高い季節ほど、動物の活動がさかんで、植物がよく育つ」ことを説明させます。冬ごしのすがたが生き物によってちがうことを表にまとめます。画面のアドレスの最後に <code>#kiroku</code> を付けると、記録カードの画面から始まります。</li>
</ul>
<p>児童への問いの例：</p>
<ol>
<li>気温のグラフと、活動している動物の数の折れ線を見くらべると、どんな関係があるでしょう。</li>
<li>ツバメ・カエル・テントウムシ・カマキリ・モンシロチョウは、それぞれどんなすがたで冬をこすでしょう。</li>
<li>ヘチマのくきが いちばんよくのびるのは、どの季節でしょう。それはなぜでしょう。</li>
</ol>
<h2>しくみ・解説</h2>
<h3>ことばの意味</h3>
<ul>
<li><b>冬ごし</b>（越冬）とは、生き物が寒い冬を、すがたや場所を変えてのりこえることです。</li>
<li><b>冬眠</b>とは、カエルやヘビ、クマなどが、冬の間 土の中や穴の中で、ほとんど動かずにすごすことです。</li>
<li><b>平年値</b>とは、気象庁が過去30年間（今は1991〜2020年）の観測をもとに計算した、その場所の「ふつうの年」の値です。</li>
</ul>
<h3>東京の月ごとの平均気温（平年値）</h3>
''' + T([[MN[i], "%.1f℃" % TEMP[i], SEAS[i], "%d種類" % ACTIVE[i], pword(PGROW[i])] for i in range(12)],
         ["月", "平均気温", "季節", "活動している動物（5種類中）", "植物のようす"]) + '''
<p>いちばん気温が高いのは8月（%.1f℃）、いちばん低いのは1月（%.1f℃）で、その差は%.1f℃です。1年の平均は%.1f℃です。気温が高い5月〜9月は5種類の動物がすべて活動していて、いちばん寒い12月〜2月（平均気温がおよそ8℃より低い月）は、どの動物も活動していません（ツバメは南の国へわたり、ほかの4種類は冬ごしをしています）。</p>
''' % (max(TEMP), min(TEMP), max(TEMP) - min(TEMP), sum(TEMP) / 12) + '''
<h3>季節ごとのようす（早見表）</h3>
''' + T(_season_rows(), ["月", "平均気温"] + [o[0] for o in ORG]) + '''
<h3>動物の冬ごし（早見表）</h3>
''' + T([["ツバメ", "あたたかい南の国へわたる", "日本にはいない"], ["カエル", "大人のカエル", "土の中・落ち葉の下（冬眠）"],
          ["テントウムシ", "成虫", "落ち葉の下・石のかげ（集まって）"], ["カマキリ", "たまご（らんのう）", "木のえだ・草のくき"],
          ["モンシロチョウ", "さなぎ", "かべ・木のえだ・へい"], ["バッタ（参考）", "たまご", "土の中"], ["アゲハ（参考）", "さなぎ", "木のえだ・かべ"]],
         ["動物", "冬をこすすがた", "冬をこす場所"]) + '''
<h3>植物の冬ごし（早見表）</h3>
''' + T([["サクラ", "葉を落とし、えだの芽（冬芽）で冬をこす"], ["ヘチマ・ツルレイシ", "体はかれて、たねで冬をこす"],
          ["タンポポ", "葉を地面に広げた形（ロゼット）で冬をこす"]], ["植物", "冬のすがた"]) + N(
    "ヘチマやツルレイシは、夏までくき（つる）がぐんぐんのびますが、すずしくなるとのび方がゆっくりになり、実をつけてかれます。タンポポのロゼットは、地面の近くで冷たい風をさけながら、日光をよく受けられる形です。") + '''
<h3>観察するときの注意</h3>
<ul>
<li>同じ場所の、同じ生き物を、決まった間かく（1週間〜1か月ごと）で観察し、気温もいっしょに記録します。</li>
<li>生き物や土にさわったあとは、<b>石けんで手をあらいましょう</b>。ハチや毒のある毛虫には近づかないようにします。</li>
<li>冬ごし中の生き物（落ち葉の下のテントウムシ、らんのう、さなぎなど）は、見たら元にもどし、持ち帰らないようにしましょう。</li>
</ul>
<h3>このシミュレーションで単純にしていること</h3>
<ul>
<li>気温は東京の平年値です。生き物のようすは関東地方の平地のおよその目安で、地域や年によって時期がちがいます（北の地方や山では春がおそく、冬が早く来ます）。</li>
<li>カエルはアマガエル、テントウムシはナナホシテントウ、カマキリはオオカマキリ、サクラはソメイヨシノの例です。種類によって時期がちがいます（たとえばヒキガエルは2〜3月ごろにたまごを産みます）。</li>
<li>「活動している動物の数」は、その月にふつうに活動しているすがたが見られるものを数えた目安です。絵は形をわかりやすくした模式図です。</li>
</ul>
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「小学校学習指導要領（平成29年告示）解説 理科編」第4学年 B（2）季節と生物（pp.54〜56）（<a href="''' + MEXT_SHO + '''" target="_blank" rel="noopener">文部科学省 小学校学習指導要領解説のページ</a>）</li>
<li>気象庁「過去の気象データ検索」東京の平年値（1991〜2020年）（<a href="''' + JMA_TOKYO + '''" target="_blank" rel="noopener">気象庁 平年値（年・月ごとの値）東京</a>）</li>
<li>小学校理科（4年）の教科書の「季節と生き物」（春・夏・秋・冬の生き物）の単元</li>
</ul>
'''

KISETSU_FAQS = [
    ("季節によって、動物の活動はどう変わりますか？", "あたたかい季節には数が多く、さかんに活動します。寒くなると活動がにぶくなり、冬はたまご・よう虫・さなぎ・成虫などのすがたで、土の中や落ち葉の下などでじっと冬をこします。ツバメのように、あたたかい南の国へわたる鳥もいます。"),
    ("季節によって、植物の成長はどう変わりますか？", "あたたかくなる春から夏にかけて、くきがよくのびて葉がしげります。すずしくなると成長がゆっくりになり、実やたねをつくります。冬は、たねを残してかれたり（ヘチマ）、葉を落として芽で冬をこしたり（サクラ）、葉を地面に広げて冬をこしたり（タンポポ）します。"),
    ("東京の月ごとの平均気温は何℃ですか？", "気象庁の平年値（1991〜2020年）で、4月14.3℃、5月18.8℃、6月21.9℃、7月25.7℃、8月26.9℃、9月23.3℃、10月18.0℃、11月12.5℃、12月7.7℃、1月5.4℃、2月6.1℃、3月9.4℃です。1年の平均は15.8℃です。"),
    ("テントウムシやカマキリは、どのように冬をこしますか？", "ナナホシテントウは成虫のまま、落ち葉の下や石のかげなどに集まって冬をこします。オオカマキリは、秋にあわでつつんだたまご（らんのう）を産み、たまごで冬をこします。"),
    ("ツバメは冬の間どこにいますか？", "日本で子育てをしたツバメの多くは、秋にあたたかい南の国（東南アジアなど）へわたり、冬をすごします。春になると、また日本にやってきて巣をつくります。"),
]

KISETSU_JS = HELP_JS + r'''
  const bar=document.createElement('div'); bar.className='lab-btns'; bar.style.marginTop='0';
  ['tM','tR'].forEach((id)=>{ const b=$(id); if(b) bar.appendChild(b); });
  cv.parentNode.insertBefore(bar,cv);
  const MN=['4月','5月','6月','7月','8月','9月','10月','11月','12月','1月','2月','3月'];
  const TEMP=[14.3,18.8,21.9,25.7,26.9,23.3,18.0,12.5,7.7,5.4,6.1,9.4];
  const SEAS=['春','春','夏','夏','夏','秋','秋','秋','冬','冬','冬','春'], SCOL={'春':'#db2777','夏':'#ea580c','秋':'#b45309','冬':'#2563eb'};
  const ORG=@@ORG@@, GOYA=@@GOYA@@;
  let mode='M', mon=+$('mon').value, run=false, tnow=0, ptimer=0, recs=[], pop=null, note=null, scrub=false;
  const orgs=()=>ORG.map((o)=>(o[0]==='ヘチマ'&&$('pl2').value==='goya')?['ツルレイシ',o[1],GOYA]:o);
  const anis=()=>orgs().filter((o)=>o[1]==='a'), plas=()=>orgs().filter((o)=>o[1]==='p');
  const activeN=(i)=>anis().filter((o)=>o[2][i][0]>=1).length;
  const pgrow=(i)=>{ const p=plas(); return p.reduce((s,o)=>s+o[2][i][0],0)/p.length; };
  const pword=(v)=>v>=2.3?'よく育つ':(v>=1.5?'育つ':(v>=0.7?'ゆっくり':'ほとんど育たない'));
  // ---- 生き物の絵（中心0,0・はば約110×80）
  function swallow(x,y,s,col){ col=col||'#1e3a8a'; const fl=Math.sin(tnow*8)*0.15;
    ctx.fillStyle=col; [-1,1].forEach((sd)=>{ ctx.beginPath(); ctx.moveTo(x,y-3*s); ctx.quadraticCurveTo(x+sd*14*s,y-(10+fl*20)*s,x+sd*30*s,y+(2-fl*10)*s); ctx.quadraticCurveTo(x+sd*14*s,y,x,y+4*s); ctx.closePath(); ctx.fill(); });
    ell(x,y+1*s,4*s,11*s,0,col); dot(x,y-10*s,4*s,col); dot(x,y-7*s,2.2*s,'#dc2626');
    ctx.strokeStyle=col; ctx.lineWidth=2*s; ctx.beginPath(); ctx.moveTo(x-1*s,y+10*s); ctx.lineTo(x-7*s,y+24*s); ctx.moveTo(x+1*s,y+10*s); ctx.lineTo(x+7*s,y+24*s); ctx.stroke(); }
  function perch(x,y){ ell(x,y-6,4,7,-0.5,'#1e3a8a'); dot(x-3,y-12,3.4,'#1e3a8a'); dot(x-4,y-9,1.6,'#dc2626'); ell(x+1,y-4,2.4,4,-0.5,'#f8fafc'); ln(x+3,y-2,x+11,y+6,1.4,'#1e3a8a'); }
  function nest(x,y){ ctx.fillStyle='#92400e'; ctx.beginPath(); ctx.arc(x,y,15,0,Math.PI); ctx.closePath(); ctx.fill(); for(let k=0;k<7;k++) dot(x-11+k*3.7,y+4+(k%2)*4,1.6,'#b45309'); }
  function frog(x,y,s,col){ col=col||'#22c55e'; const dk='#166534';
    ell(x-13*s,y+7*s,8*s,4*s,0.3,col,dk,1); ell(x+13*s,y+7*s,8*s,4*s,-0.3,col,dk,1); ell(x,y,16*s,11*s,0,col,dk,1.2); ell(x,y+4*s,10*s,5*s,0,'#dcfce7');
    [-1,1].forEach((sd)=>{ dot(x+sd*8*s,y-9*s,4.2*s,col); dot(x+sd*8*s,y-9*s,2.6*s,'#fff'); dot(x+sd*8*s,y-9*s,1.3*s,'#111'); }); }
  function tadpole(x,y,ph){ ctx.strokeStyle='#1f2937'; ctx.lineWidth=1.6; ctx.beginPath(); ctx.moveTo(x+4,y); for(let k=1;k<=6;k++) ctx.lineTo(x+4+k*2.4,y+Math.sin(tnow*9+ph+k)*2); ctx.stroke(); ell(x,y,5,3.6,0,'#1f2937'); }
  function water(){ ctx.fillStyle='#bae6fd'; ctx.fillRect(-60,0,120,44); for(let k=0;k<3;k++) ln(-46+k*36,8+k*9,-34+k*36,8+k*9,1,'#7dd3fc'); }
  function soil(y0){ ctx.fillStyle='#a07850'; ctx.fillRect(-60,y0,120,46-y0); for(let k=0;k<14;k++) dot(-50+(k*29)%100,y0+4+(k*13)%Math.max(4,36-y0),1.2,'rgba(60,40,20,.45)'); }
  function leafBg(){ ell(0,10,48,26,-0.1,'#bbf7d0','#4ade80',1.5); ln(-44,14,44,6,1.2,'#86efac'); }
  function ladybug(x,y,s){ for(const sd of [-1,1]) for(let k=0;k<3;k++) ln(x+sd*7*s,y-4*s+k*5*s,x+sd*13*s,y-6*s+k*7*s,1.2,'#111');
    ell(x,y,11*s,10*s,0,'#dc2626','#7f1d1d',1); ln(x,y-10*s,x,y+10*s,0.8,'#7f1d1d'); [[-5,-3],[5,-3],[-6,4],[6,4],[0,-8]].forEach((p)=>dot(x+p[0]*s,y+p[1]*s,2*s,'#111')); ell(x,y-11*s,6*s,4*s,0,'#111'); dot(x-3*s,y-11*s,1.2*s,'#fff'); dot(x+3*s,y-11*s,1.2*s,'#fff'); }
  function mantis(x,y,s,wing){ const col='#65a30d', dk='#3f6212';
    ln(x-2*s,y+2*s,x-6*s,y+16*s,1.4*s,dk); ln(x+6*s,y+2*s,x+12*s,y+16*s,1.4*s,dk); ln(x+4*s,y+2*s,x+2*s,y+16*s,1.4*s,dk);
    ell(x+16*s,y-1*s,20*s,5*s,-0.08,col,dk,1); if(wing) ell(x+14*s,y-4*s,19*s,4.6*s,-0.1,'#84cc16',dk,1);
    ln(x-2*s,y,x-18*s,y-14*s,3*s,col); ctx.fillStyle=col; ctx.beginPath(); ctx.moveTo(x-17*s,y-13*s); ctx.lineTo(x-29*s,y-20*s); ctx.lineTo(x-19*s,y-23*s); ctx.closePath(); ctx.fill(); dot(x-23*s,y-20*s,1.6*s,'#1f2937');
    poly([[x-14*s,y-10*s],[x-25*s,y-3*s],[x-21*s,y-14*s]],2.2*s,dk); ln(x-24*s,y-22*s,x-32*s,y-34*s,0.8*s,dk); }
  function ootheca(x,y){ ln(-50,-22,50,26,3,'#78350f'); ell(x,y,16,11,0.45,'#d6c29a','#92743f',1.2); for(let k=-1;k<=1;k++){ ctx.strokeStyle='#a8925f'; ctx.lineWidth=1; ctx.beginPath(); ctx.ellipse(x,y,16-Math.abs(k)*5,11-Math.abs(k)*3,0.45,Math.PI*1.1,Math.PI*1.9); ctx.stroke(); } }
  function pupaS(x,y){ ctx.beginPath(); ctx.moveTo(x,y-20); ctx.bezierCurveTo(x+9,y-10,x+8,y+4,x+2,y+18); ctx.bezierCurveTo(x-5,y+8,x-7,y-4,x-6,y-8); ctx.closePath(); ctx.fillStyle='#b5a77a'; ctx.fill(); ctx.strokeStyle='#78716c'; ctx.lineWidth=1; ctx.stroke(); ln(x-12,y-2,x+5,y-4,0.8,'#d6d3d1'); }
  function sakura(st){ const T='#78350f'; ln(0,40,0,4,7,T); ln(0,10,-24,-16,4,T); ln(0,6,24,-16,4,T); ln(0,4,0,-26,4,T); ln(-24,-16,-34,-26,2.5,T); ln(24,-16,34,-26,2.5,T);
    const C=[[-28,-20],[0,-28],[28,-20],[-14,-8],[14,-8],[0,-12],[-38,-6],[38,-6]];
    if(st==='bare'){ [[-34,-26],[34,-26],[0,-26],[-24,-16],[24,-16],[-12,-4],[12,-4]].forEach((p)=>dot(p[0],p[1],2.4,'#7c2d12')); return; }
    if(st==='fall'){ [[-28,-20],[28,-20],[0,-28]].forEach((p)=>dot(p[0],p[1],6,'#f97316')); [[-42,22],[30,28],[12,34],[-20,32]].forEach((p,i)=>leafE(p[0],p[1],8,3,0.6+i,'#ea580c')); return; }
    const base={flower:'#fbcfe8',hazakura:'#fbcfe8',leaf:'#22c55e',leafy:'#4ade80',koyo:'#f97316'}[st];
    C.forEach((p,i)=>{ let c=base; if(st==='hazakura'&&i%2) c='#86efac'; if(st==='leafy'&&i%3===0) c='#facc15'; if(st==='koyo'&&i%2) c='#facc15'; if(st==='leaf'&&i%2) c='#16a34a'; dot(p[0],p[1],15,c); });
    if(st==='flower'||st==='hazakura') for(let k=0;k<22;k++) dot(-46+(k*41)%92,-36+(k*17)%40,1.8,'#ec4899'); }
  function vineLeaf(x,y,c){ ell(x,y,7,6,0,c,'rgba(20,83,45,.5)',0.8); }
  function hechima(st,goya){ ln(-60,36,60,36,2,'#a16207'); ctx.fillStyle='#a07850'; ctx.fillRect(-60,37,120,9);
    if(st==='seed'||st==='seedwinter'){ if(st==='seedwinter') soil(8); [-14,0,14].forEach((x,i)=>ell(x,st==='seed'?32:24,goya?4:5,goya?3:2.6,0.3*i,goya?'#a8a29e':'#1c1917','#000',0.6)); if(st==='seed') txt('たねをまく',0,14,11,'#78350f','bold','center'); else txt('土の中のたね',0,42,10.5,'#fef3c7','bold','center'); return; }
    if(st==='sprout'){ ln(0,36,0,22,2,'#65a30d'); ell(-6,21,6,3.5,-0.3,'#84cc16'); ell(6,21,6,3.5,0.3,'#84cc16'); vineLeaf(0,15,'#22c55e'); return; }
    for(let x=-44;x<=44;x+=11) ln(x,-40,x,34,0.8,'#cbd5e1'); for(let y=-40;y<=30;y+=10) ln(-44,y,44,y,0.8,'#cbd5e1');
    const f=st==='vine1'?0.45:1, lc={vine1:'#22c55e',flower:'#16a34a',fruit:'#15803d',ripe:'#65a30d',wither:'#ca8a04',dead:'#a8a29e'}[st], vc=st==='dead'?'#a8a29e':(st==='wither'?'#a16207':'#4d7c0f');
    const pts=[]; for(let j=0;j<=10;j++) pts.push([Math.sin(j*1.3)*30*(j/10+0.2),36-j*7.4*f]); poly(pts,2,vc);
    if(f>0.9){ const p2=[]; for(let j=0;j<=8;j++) p2.push([-Math.sin(j*1.1)*36*(j/8),20-j*7]); poly(p2,1.6,vc); p2.forEach((p,i)=>{ if(i&&i%2===0) vineLeaf(p[0],p[1],lc); }); }
    pts.forEach((p,i)=>{ if(i&&(st!=='dead'||i%3===0)) vineLeaf(p[0]+(i%2?6:-6),p[1],lc); });
    if(st==='flower'||st==='fruit'){ [[-20,-18],[22,-6],[6,-34],[-30,6]].forEach((p,i)=>{ if(st==='fruit'&&i>1) return; for(let q=0;q<5;q++){ const a=q*Math.PI*2/5; dot(p[0]+Math.cos(a)*3.4,p[1]+Math.sin(a)*3.4,2.8,'#facc15'); } dot(p[0],p[1],1.6,'#ca8a04'); }); }
    if(st==='fruit'||st==='ripe'||st==='wither'||st==='dead'){ [[-10,-4],[24,-24],[34,10]].forEach((p)=>{
        if(goya){ const c=(st==='fruit')?'#4d7c0f':'#fb923c'; ell(p[0],p[1]+10,5,12,0,c,'#3f6212',1); for(let q=0;q<5;q++) dot(p[0]+(q%2?2:-2),p[1]+2+q*4,1.1,'rgba(255,255,255,.55)'); if(st!=='fruit'){ dot(p[0],p[1]+16,2,'#dc2626'); dot(p[0]+2,p[1]+12,1.8,'#dc2626'); } }
        else { const c=(st==='fruit'||st==='ripe')?'#4d7c0f':(st==='wither'?'#a16207':'#78350f'); ell(p[0],p[1]+14,4.5,14,0,c,'#365314',1); } }); } }
  function tanpopo(st){ ln(-60,34,60,34,2,'#a16207'); ctx.fillStyle='#ca9a6a'; ctx.fillRect(-60,35,120,11);
    if(st==='rosette'){ ctx.save(); ctx.translate(0,26); ctx.scale(1,0.38); for(let k=0;k<10;k++) leafE(0,0,40,8,k*Math.PI*2/10,'#166534'); ctx.restore(); return; }
    const up=st==='leaf'?1:0.6; for(let k=0;k<7;k++){ const a=-Math.PI/2+(k-3)*(st==='leaf'?0.22:0.42); leafE(0,34,(30+(k%2)*10)*up+10,6,a,'#16a34a'); }
    const heads=[[-18,-22],[4,-32],[24,-16]]; heads.forEach((h,i)=>{ if(st==='leaf'&&i!==1) return; ln(h[0]*0.2,34,h[0],h[1],1.6,'#65a30d');
      if(st==='fluff'&&i!==1){ for(let q=0;q<16;q++){ const a=q*Math.PI/8; ln(h[0],h[1],h[0]+Math.cos(a)*9,h[1]+Math.sin(a)*9,0.8,'#cbd5e1'); dot(h[0]+Math.cos(a)*9,h[1]+Math.sin(a)*9,1.3,'#f8fafc'); } }
      else { for(let q=0;q<12;q++){ const a=q*Math.PI/6; ell(h[0]+Math.cos(a)*5,h[1]+Math.sin(a)*5,4,1.8,a,'#facc15'); } dot(h[0],h[1],3.4,'#eab308'); } }); }
  // 観察スケッチ風の絵（art/*.webp・2026-10-19）。状態ごとに絵を当て、ないものはこれまでのコードの絵
  const ORG_ART={'ツバメ':['tsubame',{fly:'fly',leave:'fly',nest:'nest',hina:'hina',flock:'flock'}],
    'カエル':['kaeru',{eggs:'eggs',tad:'tad',young:'young',active:'adult',wake:'adult',slow:'adult',sleep:'sleep'}],
    'テントウムシ':['tento',{eggs:'eggs',larva:'larva',adult:'adult',group:'group'}],
    'カマキリ':['kamakiri',{ootheca:'ootheca',hatch:'hatch',nymph:'nymph',adult:'adult',lay:'adult'}],
    'モンシロチョウ':['../konchu-sodachi/art/monshiro',{adult:'seichu',larva:'youchu',pupa:'sanagi'}],
    'サクラ':['sakura',{bare:'bare',flower:'flower',hazakura:'hazakura',leaf:'leaf',leafy:'leaf',koyo:'koyo',fall:'fall'}],
    'ヘチマ':['hechima',{seed:'seed',sprout:'sprout',vine1:'vine1',flower:'flower',fruit:'fruit',wither:'wither',dead:'wither'}],
    'タンポポ':['tanpopo',{rosette:'rosette',leaf:'leaf',flower:'flower',fluff:'fluff'}]};
  const ART={};
  Object.values(ORG_ART).forEach(([pre,m])=>{ new Set(Object.values(m)).forEach((v)=>{ const k=pre+'-'+v, im=new Image(); im.onload=()=>{ ART[k]=im; }; im.src=(pre.startsWith('..')?'':'art/')+k+'.webp'; }); });
  function orgArt(name,st){ const o=ORG_ART[name]; if(!o||!o[1][st]) return null; return ART[o[0]+'-'+o[1][st]]||null; }
  function drawOrg(name,st,cx,cy,sc){ const im=orgArt(name,st);
    if(im){ ctx.save(); ctx.translate(cx,cy); ctx.scale(sc,sc); const s=Math.min(116/im.width,86/im.height), w=im.width*s, h=im.height*s; ctx.drawImage(im,-w/2,-h/2+2,w,h); ctx.restore(); return; }
    ctx.save(); ctx.translate(cx,cy); ctx.scale(sc,sc);
    if(name==='ツバメ'){ if(st==='nest'||st==='hina'){ ctx.fillStyle='#d6d3d1'; ctx.fillRect(-60,-46,120,16); nest(-14,-29); if(st==='hina'){ [-22,-14,-6].forEach((x)=>{ dot(x,-31,4,'#57534e'); ctx.fillStyle='#fde047'; ctx.beginPath(); ctx.moveTo(x-3,-34); ctx.lineTo(x+3,-34); ctx.lineTo(x,-42); ctx.closePath(); ctx.fill(); }); } swallow(26,8,0.95); }
      else if(st==='flock'){ ln(-60,0,60,-4,1.4,'#475569'); [-40,-20,0,20,40].forEach((x)=>perch(x,-x/30)); swallow(10,24,0.6); }
      else if(st==='gone'){ ctx.setLineDash([4,3]); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.arc(-10,-4,22,0,Math.PI*2); ctx.stroke(); ctx.setLineDash([]); txt('いない',-10,1,12,'#94a3b8','bold','center'); txt('南の国へ →',22,32,11,'#64748b','bold','center'); }
      else { swallow(-6,-6,1.25); if(st==='leave'){ ln(14,26,46,26,2,'#0e7490'); ctx.fillStyle='#0e7490'; ctx.beginPath(); ctx.moveTo(52,26); ctx.lineTo(44,21); ctx.lineTo(44,31); ctx.closePath(); ctx.fill(); txt('南へ',28,21,10.5,'#0e7490','bold','center'); } else { dot(30,-20,1.5,'#111'); dot(36,-12,1.5,'#111'); } } }
    else if(name==='カエル'){ if(st==='sleep'){ ctx.fillStyle='#bae6fd'; ctx.fillRect(-60,-46,120,32); soil(-14); ell(0,14,20,13,0,'#7a5a3e'); frog(0,15,0.8,'#6b8e5a'); txt('zzz',24,-20,12,'#475569','bold','left'); txt('土の中',-34,36,10,'#fef3c7','bold','center'); }
      else if(st==='wake'){ soil(10); frog(0,6,1,'#4ade80'); }
      else if(st==='eggs'||st==='tad'){ water(); if(st==='eggs'){ for(let k=0;k<9;k++){ const x=-30+(k%5)*9, y=18+Math.floor(k/5)*9; dot(x,y,4,'rgba(255,255,255,.85)'); dot(x,y,1.7,'#111'); } frog(26,-16,0.85); } else [[-30,14],[-6,24],[18,12],[36,28]].forEach((p,i)=>tadpole(p[0],p[1],i)); }
      else if(st==='young'){ water(); ell(0,-6,30,6,0,'#16a34a'); frog(0,-16,0.6); ln(6,-12,12,-8,2,'#16a34a'); tadpole(-30,22,1); }
      else { ctx.fillStyle='#dcfce7'; ctx.fillRect(-60,24,120,22); frog(-4,6,1.15,st==='slow'?'#86a37a':'#22c55e'); if(st==='active'){ dot(34,-22,2,'#111'); ln(30,-24,38,-20,0.8,'#64748b'); } else txt('…',30,-12,14,'#64748b','bold','center'); } }
    else if(name==='テントウムシ'){ if(st==='group'){ ctx.fillStyle='#d6a96a'; ctx.fillRect(-60,8,120,38); [[-30,14,0.4],[10,22,-0.6],[34,12,1.2]].forEach((p)=>leafE(p[0]-20,p[1],40,10,p[2],'#b45309')); [[-14,-4],[2,-2],[-6,-14],[10,-14]].forEach((p)=>ladybug(p[0],p[1],0.8)); txt('落ち葉の下',0,38,10.5,'#fff7ed','bold','center'); }
      else { leafBg(); if(st==='eggs'){ for(let k=0;k<8;k++) ell(-22+(k%4)*5,12+Math.floor(k/4)*6,2,3.2,0,'#facc15','#ca8a04',0.6); ladybug(20,0,1.1); }
        else if(st==='larva'){ ell(-6,8,16,6,0.1,'#374151'); for(let k=0;k<4;k++) dot(-14+k*6,7,1.6,'#fb923c'); for(let k=0;k<6;k++) dot(16+(k%3)*6,16+Math.floor(k/3)*5,2,'#4ade80'); }
        else ladybug(0,6,1.4); } }
    else if(name==='カマキリ'){ if(st==='ootheca') ootheca(-4,4); else if(st==='hatch'){ ootheca(-10,0); for(let k=0;k<5;k++){ ln(-12+k*6,10,-14+k*6,22+k%2*6,0.8,'#94a3b8'); mantis(-14+k*6,24+k%2*6,0.2,false); } }
      else if(st==='nymph'){ ln(-60,30,60,24,2,'#16a34a'); mantis(4,10,0.75,false); } else if(st==='lay'){ ln(-50,-22,50,26,3,'#78350f'); ell(-18,-6,12,8,0.45,'#d6c29a','#92743f',1); mantis(16,12,1,true); } else { ln(-60,34,60,28,2,'#16a34a'); mantis(4,10,1.2,true); } }
    else if(name==='モンシロチョウ'){ if(st==='pupa'){ ctx.fillStyle='#e7e5e4'; ctx.fillRect(-60,-46,120,92); for(let k=0;k<4;k++) ln(-60,-30+k*20,60,-30+k*20,0.8,'#d6d3d1'); pupaS(0,2); txt('かべ',36,32,10.5,'#78716c','bold','center'); }
      else if(st==='larva'){ ell(0,10,48,26,0,'#bbf7d0','#4ade80',1.5); caterpillar(0,10,60); }
      else { ln(28,46,28,10,2,'#65a30d'); [[0,0],[6,4],[-5,5]].forEach((p)=>dot(28+p[0],8+p[1],4,'#facc15')); butterfly(-12+Math.sin(tnow)*4,-6,0.62,tnow*7); } }
    else if(name==='サクラ') sakura(st);
    else if(name==='ヘチマ'||name==='ツルレイシ') hechima(st,name==='ツルレイシ');
    else if(name==='タンポポ') tanpopo(st);
    ctx.restore(); }
  // ---- 画面① 月ごとのようす
  const CX0=40, CX1=600, BY=186, KT=112/30, bw=(CX1-CX0)/12;
  function tcol(t){ return t<10?mix('#bfdbfe','#60a5fa',t/10):(t<20?mix('#86efac','#facc15',(t-10)/10):mix('#fdba74','#ef4444',(t-20)/8)); }
  function tcolL(t){ return t<10?mix('#eff6ff','#bfdbfe',t/10):(t<20?mix('#dcfce7','#fef08a',(t-10)/10):mix('#ffedd5','#fecaca',(t-20)/8)); }
  const LVA=['休み・いない','少し','活動','さかん'], LVP=['ほとんど育たない','ゆっくり','育つ','よく育つ'];
  function lvBar(x,y,lv,p){ for(let k=0;k<3;k++) dot(x-14+k*10,y-4,3.6,k<lv?(p?'#16a34a':'#ea580c'):'#e2e8f0'); txt((p?LVP:LVA)[lv],x+20,y,10.5,lv?'#334155':'#94a3b8','bold','left',p?92:66); }
  const cardBg=(lv)=>['#f1f5f9','#f7fee7','#ecfccb','#d9f99d'][lv];
  const ACARD=(i)=>[6+i*125.6,228,122,150], PCARD=(i)=>[6+i*209.3,400,205.3,144];
  function drawNote(){ if(note){ ctx.fillStyle='rgba(14,116,144,.94)'; rrect(100,256,440,44,10); ctx.fill(); txt(note.t,320,284,15,'#fff','bold','center',420); } }
  function drawM(){ const i=mon, t=TEMP[i], s=SEAS[i], A=anis(), Pp=plas(), na=activeN(i);
    ctx.fillStyle='#ecfeff'; rrect(6,4,628,44,10); ctx.fill();
    const w0=txt(MN[i],18,36,26,'#0e7490','bold'); const w=chip(s,28+w0,34,15,SCOL[s],'#fff'); txt('平均気温 '+t.toFixed(1)+'℃',38+w0+w,35,20,'#0f172a','bold','left',230);
    txt('東京の平年値',626,22,11,'#64748b','','right'); txt('カードをタップ → くわしく',626,40,11,'#64748b','','right');
    ctx.fillStyle='#fff'; rrect(6,52,628,158,10); ctx.fill(); ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; rrect(6,52,628,158,10); ctx.stroke();
    for(let v=0;v<=30;v+=10){ const y=BY-v*KT; ln(CX0,y,CX1,y,v?1:1.5,v?'#f1f5f9':'#94a3b8'); txt(v+'℃',CX0-4,y+4,10,'#64748b','','right'); }
    [0,5].forEach((v)=>txt(v+'種',CX1+30,BY-v*20+4,10,'#c2410c','bold','right'));
    TEMP.forEach((tv,j)=>{ const x=CX0+j*bw, h=tv*KT, sel=j===i; ctx.fillStyle=sel?tcol(tv):tcolL(tv);
      rrect(x+5,BY-h,bw-10,h,4); ctx.fill(); if(sel){ ctx.strokeStyle='#0e7490'; ctx.lineWidth=2.5; rrect(x+3,BY-h-2,bw-6,h+2,5); ctx.stroke(); }
      txt(tv.toFixed(1),x+bw/2,BY-h-5,sel?13:10,sel?'#0f172a':'#64748b','bold','center'); txt(MN[j],x+bw/2,BY+15,sel?12.5:11,sel?'#0e7490':'#475569','bold','center'); });
    const pts=MN.map((m,j)=>[CX0+j*bw+bw/2,BY-activeN(j)*20]); poly(pts,2,'rgba(234,88,12,.8)'); pts.forEach((p,j)=>dot(p[0],p[1],j===i?5:3.2,'#ea580c'));
    txt('棒＝平均気温（℃）　●＝活動している動物の数（5種類中）',CX0+2,67,11,'#475569','bold','left',330);
    txt('動物（5種類中 '+na+'種類が活動）',10,222,13,'#c2410c','bold','left',400);
    A.forEach((o,j)=>{ const c=ACARD(j), e=o[2][i]; ctx.fillStyle=cardBg(e[0]); rrect(c[0],c[1],c[2],c[3],10); ctx.fill();
      txt(o[0],c[0]+c[2]/2,c[1]+18,13,'#0f172a','bold','center',c[2]-8);
      ctx.save(); rrect(c[0]+6,c[1]+24,c[2]-12,82,8); ctx.clip(); ctx.fillStyle='rgba(255,255,255,.75)'; ctx.fillRect(c[0],c[1]+24,c[2],82); drawOrg(o[0],e[3],c[0]+c[2]/2,c[1]+65,1); ctx.restore();
      txt(e[1],c[0]+c[2]/2,c[1]+124,12.5,'#0f172a','bold','center',c[2]-8); lvBar(c[0]+28,c[1]+143,e[0],false); });
    txt('植物（'+pword(pgrow(i))+'）',10,394,13,'#15803d','bold','left',400);
    Pp.forEach((o,j)=>{ const c=PCARD(j), e=o[2][i]; ctx.fillStyle=cardBg(e[0]); rrect(c[0],c[1],c[2],c[3],10); ctx.fill();
      txt(o[0],c[0]+c[2]/2,c[1]+17,13,'#0f172a','bold','center',c[2]-8);
      ctx.save(); rrect(c[0]+8,c[1]+22,c[2]-16,86,8); ctx.clip(); ctx.fillStyle='rgba(255,255,255,.75)'; ctx.fillRect(c[0],c[1]+22,c[2],86); drawOrg(o[0],e[3],c[0]+c[2]/2,c[1]+64,1.05); ctx.restore();
      txt(e[1],c[0]+c[2]/2,c[1]+124,13,'#0f172a','bold','center',c[2]-8); lvBar(c[0]+c[2]/2-40,c[1]+140,e[0],true); });
    if(pop){ const o=orgs()[pop.k], e=o[2][i]; ctx.fillStyle='rgba(15,23,42,.93)'; rrect(24,236,592,118,12); ctx.fill();
      txt(o[0]+'（'+MN[i]+'）',40,264,17,'#fff','bold'); txt('×',600,262,18,'#cbd5e1','bold','right'); wrap(e[2],40,294,560,24,16,'#f8fafc','bold'); txt('タップでとじる',600,344,11,'#cbd5e1','','right'); }
    drawNote(); }
  // ---- 画面② 記録カード
  const RX0=74, RW=(634-RX0)/4, RY0=116, RH=(544-RY0)/8;
  function drawR(){ const O=orgs(), R=recs.slice().sort((a,b)=>a-b);
    ctx.fillStyle='#ecfeff'; rrect(6,4,628,44,10); ctx.fill(); txt('観察記録カード（'+R.length+'/4まい）',18,33,19,'#0e7490','bold');
    txt('月の見出しをタップ → その月を開く',626,33,11.5,'#64748b','','right');
    O.forEach((o,k)=>{ const y=RY0+k*RH; ctx.fillStyle=k%2?'#fff':'#f8fafc'; ctx.fillRect(6,y,628,RH); txt(o[0],10,y+RH/2+4,12,o[1]==='a'?'#c2410c':'#15803d','bold','left',60); });
    txt('動物',10,RY0-6,11,'#c2410c','bold'); ln(6,RY0+5*RH,634,RY0+5*RH,2,'#94a3b8'); txt('植物',10,RY0+5*RH+12,10,'#15803d','bold');
    for(let c=0;c<4;c++){ const x=RX0+c*RW, m=R[c]; ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; ctx.strokeRect(x+1,54,RW-2,544-54);
      if(m===undefined){ txt('📌で記録しよう',x+RW/2,84,11.5,'#94a3b8','bold','center'); continue; }
      const s=SEAS[m]; ctx.fillStyle=tcolL(TEMP[m]); ctx.fillRect(x+2,55,RW-4,58);
      txt(MN[m],x+12,80,20,'#0e7490','bold'); chip(s,x+RW-10,79,12,SCOL[s],'#fff','right'); txt(TEMP[m].toFixed(1)+'℃',x+12,104,15,'#0f172a','bold');
      ctx.fillStyle='#fff'; rrect(x+70,94,RW-82,10,5); ctx.fill(); ctx.fillStyle=tcol(TEMP[m]); rrect(x+70,94,(RW-82)*TEMP[m]/30,10,5); ctx.fill();
      O.forEach((o,k)=>{ const y=RY0+k*RH, e=o[2][m]; ctx.fillStyle=cardBg(e[0]); rrect(x+4,y+3,RW-8,RH-6,6); ctx.fill();
        ctx.save(); rrect(x+6,y+5,50,RH-10,5); ctx.clip(); ctx.fillStyle='rgba(255,255,255,.7)'; ctx.fillRect(x+6,y+5,50,RH-10); drawOrg(o[0],e[3],x+31,y+RH/2,0.44); ctx.restore();
        wrap(e[1],x+60,y+20,RW-66,14,11.5,'#0f172a','bold'); for(let q=0;q<3;q++) dot(x+64+q*8,y+RH-10,2.6,q<e[0]?(o[1]==='a'?'#ea580c':'#16a34a'):'#e2e8f0'); }); }
    drawNote(); }
  function draw(){ ctx.fillStyle='#fff'; ctx.fillRect(0,0,W,H); if(mode==='M') drawM(); else drawR(); }
  function update(){ const i=mon, na=activeN(i), pg=pgrow(i);
    $('monL').textContent=MN[i]+'（'+SEAS[i]+'）';
    setV('s1',MN[i]+'（'+SEAS[i]+'）'); setV('s2',TEMP[i].toFixed(1)+'℃'); setV('s3','5種類中 '+na+'種類'); setV('s4',pword(pg));
    setShare('【季節と生き物】'+MN[i]+'（東京の平均気温 '+TEMP[i].toFixed(1)+'℃）：動物は5種類中'+na+'種類が活動、植物は「'+pword(pg)+'」。あたたかい季節ほど動物の活動がさかんで、植物がよく育つ｜シミュラボ'); }
  function setMon(v){ mon=clamp(Math.round(v),0,11); $('mon').value=mon; pop=null; update(); }
  function setPlay(){ $('play').textContent=run?'⏸ 止める':'▶ 1年を早送り'; }
  function setMode(m){ mode=m; pop=null; ['tM','tR'].forEach((id)=>{ $(id).className='btn '+(id==='t'+m?'btn-primary':'btn-ghost'); }); $('clr').style.display=m==='R'?'':'none';
    if(m==='R'&&!recs.length){ recs=[0,3,6,9]; note={t:'例として 4月・7月・10月・1月 をならべました',life:2.6}; } draw(); }
  function addRec(m){ if(recs.indexOf(m)>=0){ note={t:MN[m]+'は もう記録してあります',life:1.8}; return; } recs.push(m); if(recs.length>4) recs.shift(); note={t:MN[m]+'を記録カードに入れました（'+recs.length+'/4）',life:1.8}; }
  $('tM').addEventListener('click',()=>setMode('M')); $('tR').addEventListener('click',()=>setMode('R'));
  $('mon').addEventListener('input',()=>{ mon=+$('mon').value; pop=null; update(); });
  $('pl2').addEventListener('change',()=>{ update(); });
  $('play').addEventListener('click',()=>{ if(!run&&mon>=11) setMon(0); run=!run; ptimer=0; if(run&&mode!=='M') setMode('M'); setPlay(); });
  $('rec').addEventListener('click',()=>{ addRec(mon); });
  $('four').addEventListener('click',()=>{ recs=[0,3,6,9]; setMode('R'); note={t:'春（4月）・夏（7月）・秋（10月）・冬（1月）をならべました',life:2.4}; });
  $('clr').addEventListener('click',()=>{ recs=[]; note={t:'カードを消しました。📌で記録しよう',life:2}; });
  cv.addEventListener('pointerdown',(e)=>{ const p=cpos(cv,e), x=p[0]/dpr, y=p[1]/dpr;
    if(mode==='R'){ if(y>=54&&y<=112&&x>=RX0){ const R=recs.slice().sort((a,b)=>a-b), c=Math.floor((x-RX0)/RW); if(R[c]!==undefined){ setMon(R[c]); setMode('M'); } } e.preventDefault(); return; }
    if(pop){ pop=null; e.preventDefault(); return; }
    if(y>=52&&y<=210&&x>=CX0&&x<CX1){ run=false; setPlay(); setMon(Math.floor((x-CX0)/bw)); try{ cv.setPointerCapture(e.pointerId); }catch(_){} scrub=true; e.preventDefault(); return; }
    for(let j=0;j<5;j++){ const c=ACARD(j); if(x>=c[0]&&x<=c[0]+c[2]&&y>=c[1]&&y<=c[1]+c[3]){ pop={k:j}; e.preventDefault(); return; } }
    for(let j=0;j<3;j++){ const c=PCARD(j); if(x>=c[0]&&x<=c[0]+c[2]&&y>=c[1]&&y<=c[1]+c[3]){ pop={k:5+j}; e.preventDefault(); return; } } });
  cv.addEventListener('pointermove',(e)=>{ if(!scrub) return; const p=cpos(cv,e), x=p[0]/dpr; const m=clamp(Math.floor((x-CX0)/bw),0,11); if(m!==mon) setMon(m); e.preventDefault(); });
  cv.addEventListener('pointerup',()=>{ scrub=false; }); cv.addEventListener('pointercancel',()=>{ scrub=false; });
  let last=performance.now();
  function loop(now){ const dt=Math.min(0.05,Math.max(0,(now-last)/1000)); last=now; tnow+=dt;
    if(run){ ptimer+=dt; if(ptimer>=1.1){ ptimer=0; if(mon>=11){ run=false; setPlay(); } else setMon(mon+1); } }
    if(note){ note.life-=dt; if(note.life<=0) note=null; }
    draw(); requestAnimationFrame(loop); }
  update(); setMode((location.hash||'')==='#kiroku'?'R':'M'); requestAnimationFrame(loop);
'''.replace("@@ORG@@", ORG_JSON).replace("@@GOYA@@", GOYA_JSON)

sim(slug="kisetsu-seibutsu", cat="rika", emoji="🌸", score=79,
    title="季節と生き物シミュレーター（気温と動物の活動・植物の成長・冬ごし）",
    title_tag="季節と生き物のシミュレーション｜月ごとの気温とツバメ・カエル・テントウムシ・サクラ・ヘチマのようす・冬ごし（小4理科）",
    meta_desc="小4理科「季節と生物」のシミュレーション。4月〜3月の月を選ぶと、東京の平均気温（気象庁の平年値）のグラフと、ツバメ・カエル・テントウムシ・カマキリ・モンシロチョウ、サクラ・ヘチマ・タンポポのようすが変わります。冬ごしのすがたも分かり、観察記録カードのように月をならべてくらべられます。",
    og_title="季節と生き物シミュレーター（小4 季節と生物）",
    og_desc="気温が高い季節ほど動物の活動がさかんで、植物がよく育つ。月ごとの平均気温と生き物のようすを1年分くらべ、冬ごしのすがたもたしかめる。",
    card_desc="月を動かすと気温のグラフと動物・植物のようすが変わる。冬ごしのすがたや観察カードでのくらべも。",
    lead="4月〜3月の月を選ぶと、その月の平均気温（東京の平年値）と、動物5種類・植物3種類のようすが変わります。選んだ月を観察記録カードのようにならべて、季節によるちがいをくらべられます。",
    model="小4 季節と生物（動物の活動・植物の成長と気温）", level="小学4年",
    unit="小学校 第4学年 B（2）季節と生物",
    canvas=canvas(640, 548, light=True),
    controls=slider("mon", "月（4月〜3月）", 0, 11, 0, 1)
             + select("pl2", "育てる植物", [("hechima", "ヘチマ"), ("goya", "ツルレイシ（ゴーヤ）")]),
    buttons=btn("tM", "🗓️ ① 月ごとのようす", True) + btn("tR", "📋 ② 記録カードでくらべる")
            + btn("play", "▶ 1年を早送り", True) + btn("rec", "📌 この月を記録カードに") + btn("four", "🌸 春夏秋冬の4まい") + btn("clr", "🗑️ カードを消す"),
    stats=stats([("s1", "月", False), ("s2", "平均気温（東京）", False), ("s3", "活動している動物", True), ("s4", "植物のようす", False)]),
    legend="気温は気象庁の東京の平年値（1991〜2020年）です。生き物のようすは関東地方の平地のおよその目安で、地域や年によってちがいます。グラフをタップ・なぞると月が変わり、カードをタップすると、くわしい説明が出ます。●の数は活動のさかんさ（植物は成長のようす）の目安です。",
    article=KISETSU_ARTICLE, faqs=KISETSU_FAQS,
    rel=[("konchu-sodachi", "🦋", "こん虫の育ち方と体のつくり"), ("hiruma-nagasa", "🌅", "昼の長さメーター"), ("taiyou-ugoki", "🌞", "太陽の1日の動きと季節"),
         ("hatsuga-jouken", "🫘", "種子の発芽と成長の条件シミュレーター"), ("tenki-kion", "🌤️", "天気と気温")],
    js=KISETSU_JS)
