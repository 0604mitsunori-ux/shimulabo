# -*- coding: utf-8 -*-
"""理科の授業向けシミュ（物の溶け方と溶解度・ものの燃え方と空気）
   youkaido … 小5「物の溶け方」／中1「水溶液」（第1分野（2）身の回りの物質 ア（イ））
   nenshou  … 小6「燃焼の仕組み」（第6学年 A（1））"""
import json
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

MEXT_SHO = "https://www.mext.go.jp/a_menu/shotou/new-cs/1387014.htm"
MEXT_CHU = "https://www.mext.go.jp/a_menu/shotou/new-cs/1387016.htm"
def A(url, label): return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, label)

FF = '"Hiragino Sans","Hiragino Kaku Gothic ProN","Noto Sans JP","Yu Gothic UI","Yu Gothic",Meiryo,sans-serif'

# ============================================================ 1 物の溶け方と溶解度
# 溶解度［g / 水100g］0〜80℃・10℃ごと。理科年表・教科書で一般的な値。
# ミョウバンは教科書と同じく結晶（硫酸カリウムアルミニウム十二水和物）の質量で表した値
# （理科年表の無水物の値 3.0, 4.0, 5.9, 8.4, 11.7, 17.0, 24.8, 40.0, 71.0 から換算すると一致）。
SOL = [
    ("alum", "ミョウバン", [5.7, 7.6, 11.4, 16.6, 23.8, 36.4, 57.4, 110.5, 321.6], "#7c3aed", "oct"),
    ("salt", "食塩", [35.7, 35.7, 35.8, 36.1, 36.3, 36.7, 37.1, 37.5, 38.0], "#475569", "cube"),
    ("kno3", "硝酸カリウム", [13.3, 22.0, 31.6, 45.6, 63.9, 85.2, 109.2, 138.0, 168.8], "#ea580c", "needle"),
    ("boric", "ホウ酸", [2.8, 3.6, 4.9, 6.8, 8.9, 11.4, 14.9, 18.7, 23.5], "#0891b2", "plate"),
]
for _k, _n, _s, _c, _sh in SOL:
    assert len(_s) == 9 and all(_s[i] <= _s[i + 1] for i in range(8)), _k
SUB_JS = json.dumps({k: {"n": n, "S": s, "c": c, "sh": sh} for k, n, s, c, sh in SOL}, ensure_ascii=False)
SD = {k: s for k, n, s, c, sh in SOL}


def _h(v):  # 四捨五入（小数第1位）
    from decimal import Decimal, ROUND_HALF_UP
    return str(Decimal(str(v)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def _sol_table():
    rows = [["%d℃" % (i * 10)] + ["%.1f" % SD[k][i] for k in ("salt", "alum", "kno3", "boric")] for i in range(9)]
    return T(rows, ["水温", "食塩", "ミョウバン", "硝酸カリウム", "ホウ酸"])


def _sol50_table():
    rows = [["%d℃" % t] + [_h(SD[k][t // 10] * 50 / 100) + " g" for k in ("salt", "alum")] for t in (0, 20, 40, 60, 80)]
    return T(rows, ["水温", "食塩", "ミョウバン"])


YOUKAI_ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
<p>物が水に溶ける量には限度があり、その量は<b>水の温度・水の量・溶かす物</b>によってちがいます。限度をこえた分は溶け残り、温度の高い水に溶かした物は、冷やしたり水を蒸発させたりすると<b>結晶</b>として出てきます。物が水に溶けても、水と物とを合わせた重さは変わりません。</p>
''' + N("対応する単元：小学校 第5学年 A（1）物の溶け方／中学校 第1学年 第1分野（2）身の回りの物質 ア（イ）水溶液（溶解度・再結晶・質量パーセント濃度、溶解度曲線）") + '''
<h2>授業での使い方</h2>
<h3>導入（小5）：溶けた物はどこへ行った？</h3>
<p>水50gにミョウバンを10g入れたときの電子てんびんの値（60.0g）を見せ、「溶けたら重さはどうなるか」を予想させます。スプーンをタップして少しずつ加えても、全体の重さは「水＋入れた物」のままであることを確かめます。下の粒子のモデルで、溶けた物は見えなくなっても、水の中に均一に広がっていることを示します。</p>
<h3>展開（小5・中1）：条件を1つずつ変える</h3>
<p>水の量だけ、水温だけ、溶かす物だけを変えて、溶ける限度がどう変わるかを調べます。「🔥 あたためる」で水温を上げると溶け残りが溶け、「❄ 冷やす」で下げると結晶が出てきます（ミョウバン・硝酸カリウムでははっきり出てきますが、食塩はほとんど出てきません）。食塩は「♨ 水を10g蒸発」で取り出せることを比べます。中1では右の溶解度曲線を指でなぞり、点の位置（曲線の上か下か）と溶け残りの関係を読み取らせます。</p>
<h3>まとめ（中1）：計算で確かめる</h3>
<p>下の例題を解いてから、同じ条件をシミュレーターに入れて答え合わせをします。統計欄の「溶けている量」「溶け残り」「濃度」と、図の下の式がそのまま計算の手順になっています。</p>
<p><b>児童・生徒への問いの例</b></p>
<ol>
<li>20℃の水50gにミョウバンを10g入れました。溶け残りを全部溶かすには、水温を何℃以上にすればよいでしょう。（答え：約35℃）</li>
<li>ミョウバンの水溶液は冷やすと結晶が出てくるのに、食塩水を冷やしてもほとんど出てこないのはなぜでしょう。溶解度曲線の形から説明しましょう。</li>
<li>水100gに食塩25gを溶かした食塩水の重さと、質量パーセント濃度はいくつでしょう。（答え：125g、20%）</li>
</ol>
<h2>しくみ・解説</h2>
<h3>用語の意味</h3>
<ul>
<li><b>水溶液</b>とは、物が水に溶けてできた、すき通った液のことです（色がついていても、すき通っていれば水溶液です）。</li>
<li><b>溶質</b>は溶けている物質、<b>溶媒</b>は溶質を溶かしている液体（水溶液では水）、<b>溶液</b>は溶質が溶媒に溶けた液のことです。</li>
<li><b>溶解度</b>とは、100gの水に溶ける物質の最大の質量［g］のことで、物質の種類と水の温度によって決まります。</li>
<li><b>飽和水溶液</b>とは、物質が溶解度まで溶けていて、それ以上は溶けない水溶液のことです。</li>
<li><b>溶解度曲線</b>とは、水の温度と溶解度の関係を表したグラフのことです。</li>
<li><b>再結晶</b>とは、固体の物質をいったん水に溶かし、水溶液を冷やしたり水を蒸発させたりして、再び結晶として取り出すことです。</li>
<li><b>質量パーセント濃度</b>とは、溶液の質量に対する溶質の質量の割合を百分率［%］で表したものです。</li>
</ul>
<h3>式の早見表</h3>
''' + T([["水 x g に溶ける限度", "溶解度 × x ÷ 100", "20℃のミョウバン、水50g：11.4 × 50 ÷ 100 ＝ 5.7 g"],
          ["溶け残り", "入れた量 − 溶ける限度", "10 − 5.7 ＝ 4.3 g"],
          ["水溶液の重さ", "水の重さ ＋ 溶けた物の重さ", "50 ＋ 5.7 ＝ 55.7 g（溶け残りも合わせると 60 g）"],
          ["冷やして出てくる結晶", "溶けていた量 − 冷やした温度での限度", "硝酸カリウム 水100g 60℃→20℃：109.2 − 31.6 ＝ 77.6 g"],
          ["水を蒸発させて出てくる結晶", "溶けていた量 − 残った水に溶ける限度", "20℃の水100gの食塩水（食塩30g）から水50gを蒸発：30 − 17.9 ＝ 12.1 g"],
          ["質量パーセント濃度［%］", "溶質の質量 ÷（溶質の質量 ＋ 溶媒の質量）× 100", "食塩25g＋水100g：25 ÷ 125 × 100 ＝ 20 %"]],
         ["求めるもの", "式", "例"]) + '''
<h3>溶けても重さが変わらないわけ（粒子のモデル）</h3>
<p>物が水に溶けると、目に見えないほど小さな粒になって、水の粒の間に<b>均一に広がります</b>。粒はなくなったわけではないので、水と物とを合わせた重さは変わりません。時間がたっても、溶けた物が下にたまることはなく、水溶液の濃さはどこも同じです（色のついたコーヒーシュガーや硫酸銅を溶かすと、色が全体に同じように広がることで確かめられます）。図の左下の「粒子のモデル」では、溶けた粒が動き回りながら広がる様子と、限度をこえた分が粒の集まり（固体）として残る様子を表しています。</p>
<h3>冷やす？ 蒸発させる？ 取り出し方は物によってちがう</h3>
<p>ミョウバンや硝酸カリウムは、水温によって溶解度が大きく変わる（溶解度曲線の傾きが大きい）ので、高い温度で溶かして<b>冷やす</b>と多くの結晶が出てきます。食塩は水温が変わっても溶解度がほとんど変わらない（60℃で37.1g、20℃で35.8g）ので、冷やしても水100gあたり1.3gしか出てきません。食塩を取り出すには、<b>水を蒸発させる</b>方法が向いています。結晶の形も物質によって決まっていて、食塩は立方体、ミョウバンは正八面体、硝酸カリウムは柱状（針状）、ホウ酸はうろこ状（板状）です。</p>
<h3>溶解度の表（水100gに溶ける量［g］）</h3>
''' + _sol_table() + '''
<p>小学校の実験でよく使う水50g（50mL）の場合は、この表の値の半分になります。</p>
''' + _sol50_table() + '''
<h3>計算問題の解き方（例題）</h3>
<p><b>例題1（小5）</b>　20℃の水50gに、ミョウバンは何gまで溶けますか。また、10g入れると何g溶け残りますか。<br>
→ 20℃の溶解度は11.4gなので、11.4×50÷100＝<b>5.7g</b>。溶け残りは 10−5.7＝<b>4.3g</b>。</p>
<p><b>例題2（小5）</b>　例題1の液を40℃にすると、溶け残りはどうなりますか。そのあと20℃にもどすとどうなりますか。<br>
→ 40℃の水50gには 23.8×50÷100＝11.9g まで溶けるので、10gは<b>全部溶けます</b>。20℃にもどすと、5.7gまでしか溶けていられないので、10−5.7＝<b>4.3gの結晶が出てきます</b>。</p>
<p><b>例題3（中1・再結晶）</b>　60℃の水100gに硝酸カリウムを溶けるだけ溶かし、20℃まで冷やしました。出てくる結晶は何gですか。<br>
→ 60℃で109.2g溶けていて、20℃では31.6gまでしか溶けないので、109.2−31.6＝<b>77.6g</b>。</p>
<p><b>例題4（中1・質量パーセント濃度）</b>　20℃の食塩の飽和水溶液の質量パーセント濃度は何%ですか。<br>
→ 水100gに35.8g溶けているので、35.8÷（35.8＋100）×100＝26.36…　<b>約26.4%</b>。</p>
<p><b>例題5（中1・蒸発）</b>　20℃の水100gに食塩30gを溶かしました。20℃のまま水を50g蒸発させると、何gの食塩が出てきますか。<br>
→ 残った水50gに溶けるのは 35.8×50÷100＝17.9g なので、30−17.9＝<b>12.1g</b>。</p>
''' + P("例題1〜2は、物質「ミョウバン」・水の量50g・水温20℃・加えた量10gで確かめられます（はじめの画面の設定です）。「🔥 あたためる」を2回押すと溶け残りがなくなり、「❄ 冷やす」を2回押すと4.3gの結晶が出てきます。例題3は、硝酸カリウム・水100g・60℃で加えた量を109.2gにしてから冷やします。") + N("<b>このシミュレーターで単純化している点</b><br>"
     "・溶解度は、理科年表や教科書で一般的に使われる値です。<b>教科書や問題集によって、小数第1位などが少しちがうことがあります</b>。授業やテストでは、使っている教科書や問題に書かれた値で計算してください。表の間の温度は、となりの2つの値を直線で結んで計算しています。<br>"
     "・ミョウバンの値は、教科書と同じく結晶（硫酸カリウムアルミニウム十二水和物）の質量で表しています。理科年表のように水を含まない形（無水物）で表すと、20℃で5.9g、60℃で24.8gと小さな値になります。ミョウバンは70℃をこえると溶ける量が急に増えるため、80℃の値（321.6g）はグラフの外に出ています。<br>"
     "・水1mLを1gとしています。溶けるまでの時間（かき混ぜる時間）や、冷やしてもすぐには結晶が出ない「過飽和」の状態は扱っていません。あたためたときに自然に蒸発する水も考えず、水は「♨ 水を10g蒸発」を押したときだけ減ります。<br>"
     "・粒子のモデルは、粒の数を水100gあたりの溶けた量に比例させた見本の図で、実際の粒の大きさや数ではありません（水の粒はかいていません）。") + '''
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「小学校学習指導要領（平成29年告示）解説 理科編」第5学年 A（1）物の溶け方（''' + A(MEXT_SHO, "小学校学習指導要領解説") + '''）</li>
<li>文部科学省「中学校学習指導要領（平成29年告示）解説 理科編」第1分野（2）ア（イ）水溶液（''' + A(MEXT_CHU, "中学校学習指導要領解説") + '''）</li>
<li>小学校理科の教科書（東京書籍「新しい理科」、啓林館「わくわく理科」、大日本図書「たのしい理科」など）5年の「物のとけ方」の単元、中学校理科の教科書（東京書籍「新しい科学」、啓林館「未来へひろがるサイエンス」、大日本図書「理科の世界」など）1年の「水溶液」の単元</li>
<li>国立天文台 編『理科年表』（丸善出版）物理/化学部「溶解度」</li>
<li>日本化学会 編『化学便覧 基礎編』（丸善出版）</li>
</ul>
'''

JS_YOUKAI = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  cv.setAttribute('role','img'); cv.setAttribute('aria-label','ビーカーと溶解度曲線。物を加えたり、冷やしたり、水を蒸発させたりすると、溶ける量と溶け残りが分かります');
  const FF='@FF@';
  const SUB=@SUB@, KEYS=['alum','salt','kno3','boric'];
  const r1=(v)=>Math.round(v*10+1e-7)/10, f1=(v)=>r1(v).toFixed(1);
  function sol(k,t){ const S=SUB[k].S; t=clamp(t,0,80); const i=Math.min(7,Math.floor(t/10)); return S[i]+(S[i+1]-S[i])*(t/10-i); }
  function satT(k,a){ const S=SUB[k].S; if(a<=S[0]+1e-9) return -1; for(let i=0;i<8;i++){ if(a<=S[i+1]+1e-9) return (i+(a-S[i])/(S[i+1]-S[i]))*10; } return 999; }
  // ---------- 描画の部品 ----------
  function tx(s,x,y,size,col,align,bold){ ctx.font=(bold?'bold ':'')+size+'px '+FF; ctx.textAlign=align||'left'; ctx.fillStyle=col; ctx.fillText(s,x,y); ctx.textAlign='left'; }
  function tw(s,size,bold){ ctx.font=(bold?'bold ':'')+size+'px '+FF; return ctx.measureText(s).width; }
  function halo(s,x,y,size,col,align,bold){ ctx.font=(bold?'bold ':'')+size+'px '+FF; ctx.textAlign=align||'left'; ctx.lineJoin='round'; ctx.lineWidth=3.5; ctx.strokeStyle='rgba(255,255,255,.95)'; ctx.strokeText(s,x,y); ctx.fillStyle=col; ctx.fillText(s,x,y); ctx.textAlign='left'; }
  function fit(s,x,y,size,col,maxW,bold){ let z=size; while(z>9 && tw(s,z,bold)>maxW) z-=0.5; tx(s,x,y,z,col,'left',bold); }
  function rr(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
  function panel(x,y,w,h,title){ ctx.fillStyle='#fff'; ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1.2; rr(x,y,w,h,10); ctx.fill(); ctx.stroke(); if(title) tx(title,x+10,y+19,12.5,'#0f172a','left',true); }
  function line(a,b,c,d){ ctx.beginPath(); ctx.moveTo(a,b); ctx.lineTo(c,d); ctx.stroke(); }
  function dot(x,y,r,col){ ctx.fillStyle=col; ctx.beginPath(); ctx.arc(x,y,r,0,7); ctx.fill(); }
  function crystal(x,y,s,sh,col,rot){ ctx.save(); ctx.translate(x,y); ctx.rotate(rot); ctx.fillStyle='#f8fafc'; ctx.strokeStyle=col; ctx.lineWidth=1.1; ctx.beginPath();
    if(sh==='cube'){ ctx.rect(-s/2,-s/2,s,s); }
    else if(sh==='oct'){ ctx.moveTo(0,-s*0.78); ctx.lineTo(s*0.62,0); ctx.lineTo(0,s*0.78); ctx.lineTo(-s*0.62,0); ctx.closePath(); }
    else if(sh==='needle'){ ctx.rect(-s*1.15,-s*0.2,s*2.3,s*0.4); }
    else { for(let i=0;i<6;i++){ const a=i*Math.PI/3, px=Math.cos(a)*s*0.75, py=Math.sin(a)*s*0.34; if(i) ctx.lineTo(px,py); else ctx.moveTo(px,py); } ctx.closePath(); }
    ctx.fill(); ctx.stroke(); if(sh==='oct'){ ctx.beginPath(); ctx.moveTo(-s*0.62,0); ctx.lineTo(s*0.62,0); ctx.stroke(); } ctx.restore(); }
  const pr=(i)=>{ const v=Math.sin(i*12.9898+4.1)*43758.5453; return v-Math.floor(v); };
  const PILE=[]; for(let j=0;j<60;j++){ const row=Math.floor(j/12), k=j%12; PILE.push([(k-5.5)*9.4*(1-row*0.14)+(pr(j)-0.5)*4, -5-row*7.4+(pr(j+99)-0.5)*3, (pr(j+7)-0.5)*1.3]); }
  // ---------- 状態 ----------
  let K='alum', WA=50, TT=20, M=10, evap=0, disV=0, anim=null, trail=null, drops=[], parts=[], last=performance.now(), drag=false, frozen=null, YM=40, pulse=0;
  function calc(){ const S1=r1(sol(K,TT)), lim=r1(S1*WA/100), dis=r1(Math.min(M,lim)), res=r1(M-dis), a=M/WA*100, conc=dis/(dis+WA)*100;
    const lim10=r1(S1*Math.max(0,WA-10)/100), ev=Math.max(0,r1(dis-lim10));
    return {S1:S1,lim:lim,dis:dis,res:res,a:a,conc:conc,st:satT(K,a),ev:ev,tot:r1(WA+M)}; }
  // ---------- 粒子のモデル ----------
  const MB={x0:16,x1:240,y0:332,y1:428}, KP=1.5, CAP=150;
  function partTargets(){ const a=M/WA*100; let nT=Math.round(a*KP), nD=Math.round(disV/WA*100*KP); if(nT>CAP){ nD=Math.round(nD*CAP/nT); nT=CAP; } return [nT,Math.min(nD,nT)]; }
  function slot(j){ const col=j%18, row=Math.floor(j/18); return [128-8.5*6.4+col*6.4+(row%2)*3.2, MB.y1-4-row*6.2]; }
  function seedParts(){ parts=[]; const tg=partTargets(), nS=tg[0]-tg[1]; for(let i=0;i<tg[0];i++){ if(i<nS){ const s=slot(i); parts.push({x:s[0],y:s[1],vx:0,vy:0,d:false}); } else parts.push({x:rnd(MB.x0+5,MB.x1-5),y:rnd(MB.y0+5,MB.y1-5),vx:rnd(-20,20),vy:rnd(-20,20),d:true}); } }
  function updParts(dt){ const tg=partTargets(), nT=tg[0], nD=tg[1];
    while(parts.length<nT) parts.push({x:128+rnd(-40,40),y:MB.y0+2,vx:0,vy:0,d:false});
    if(parts.length>nT) parts.length=nT;
    let cD=0; parts.forEach(p=>{ if(p.d) cD++; });
    while(cD<nD){ let p=null; for(let i=parts.length-1;i>=0;i--){ if(!parts[i].d){ p=parts[i]; break; } } if(!p) break; p.d=true; p.vx=rnd(-15,15); p.vy=rnd(-35,-10); cD++; }
    while(cD>nD){ let p=null; for(let i=0;i<parts.length;i++){ if(parts[i].d){ p=parts[i]; break; } } if(!p) break; p.d=false; cD--; }
    let j=0; parts.forEach(p=>{ if(!p.d){ const s=slot(j++); p.tx=s[0]; p.ty=s[1]; } });
    const k=Math.min(1,dt*3);
    parts.forEach(p=>{ if(p.d){ p.vx+=randn()*160*dt; p.vy+=randn()*160*dt; p.vx*=0.96; p.vy*=0.96; const sp=Math.hypot(p.vx,p.vy); if(sp>45){ p.vx*=45/sp; p.vy*=45/sp; }
        p.x+=p.vx*dt; p.y+=p.vy*dt; if(p.x<MB.x0+4){ p.x=MB.x0+4; p.vx=Math.abs(p.vx); } if(p.x>MB.x1-4){ p.x=MB.x1-4; p.vx=-Math.abs(p.vx); } if(p.y<MB.y0+4){ p.y=MB.y0+4; p.vy=Math.abs(p.vy); } if(p.y>MB.y1-4){ p.y=MB.y1-4; p.vy=-Math.abs(p.vy); } }
      else { p.x+=(p.tx-p.x)*k; p.y+=(p.ty-p.y)*k; } }); }
  // ---------- 描画 ----------
  const BX0=30, BX1=166, BT=74, BB=228, PCX=90;
  const wy=(g)=>BB-4-g/200*(BB-BT-22);
  function drawBeaker(c){ const sb=SUB[K];
    panel(6,6,244,294,sb.n+'を水に溶かす');
    // スプーン（タップで1g）
    const sx=200, sy=44, sc=1+pulse*0.4;
    ctx.save(); ctx.translate(sx,sy); ctx.scale(sc,sc); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=4; ctx.lineCap='round'; line(10,-3,38,-16); ctx.lineCap='butt';
    ctx.fillStyle='#e2e8f0'; ctx.strokeStyle='#64748b'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.ellipse(0,0,13,7.5,-0.25,0,7); ctx.fill(); ctx.stroke();
    ctx.fillStyle='#fff'; ctx.strokeStyle=sb.c; ctx.beginPath(); ctx.ellipse(0,-2,9,4.5,-0.25,0,7); ctx.fill(); ctx.stroke(); ctx.restore();
    tx('タップで1g',212,68,10.5,'#64748b','center',true);
    // 水
    const top=wy(WA);
    ctx.fillStyle='rgba(125,211,252,.30)'; ctx.fillRect(BX0+1.5,top,BX1-BX0-3,BB-top-1.5);
    ctx.strokeStyle='#38bdf8'; ctx.lineWidth=1.5; line(BX0+2,top,BX1-2,top);
    // 溶け残り・結晶
    const resV=Math.max(0,M-disV), nC=resV>0.04?Math.min(60,Math.ceil(Math.sqrt(resV)*6)):0;
    for(let j=0;j<nC;j++){ const q=PILE[j]; crystal(PCX+q[0],BB-3+q[1],sb.sh==='needle'?6.5:7.6,sb.sh,sb.c,q[2]); }
    // 落ちていく粒
    drops.forEach(d=>{ const p=clamp(d.p,0,1), x=d.x0+(d.x1-d.x0)*p, y=d.y0+(d.y1-d.y0)*p-Math.sin(p*Math.PI)*30; dot(x,y,2.2,sb.c); });
    // 目盛り
    ctx.strokeStyle='#64748b'; ctx.lineWidth=1; for(let g=50;g<=200;g+=50){ const y=wy(g); line(BX0,y,BX0+8,y); tx(String(g),BX0-4,y+3.5,9,'#64748b','right'); }
    tx('mL',BX0-4,BT+4,9,'#64748b','right');
    // ビーカー
    ctx.strokeStyle='#475569'; ctx.lineWidth=2.5; ctx.beginPath(); ctx.moveTo(BX0-6,BT); ctx.lineTo(BX0,BT+5); ctx.lineTo(BX0,BB-6); ctx.quadraticCurveTo(BX0,BB,BX0+6,BB); ctx.lineTo(BX1-6,BB); ctx.quadraticCurveTo(BX1,BB,BX1,BB-6); ctx.lineTo(BX1,BT+5); ctx.lineTo(BX1+6,BT); ctx.stroke();
    tx('水 '+Math.round(WA)+' g',BX0+8,top+15,11,'#0369a1','left',true);
    // 温度計
    const tx0=150; ctx.fillStyle='#fff'; ctx.strokeStyle='#64748b'; ctx.lineWidth=1.2; rr(tx0-3.5,52,7,BB-62,3.5); ctx.fill(); ctx.stroke();
    const ty=BB-14-TT/80*(BB-14-62); ctx.fillStyle='#ef4444'; ctx.fillRect(tx0-1.5,ty,3,BB-12-ty); dot(tx0,BB-12,5,'#ef4444');
    halo(Math.round(TT)+'℃',tx0,48,12,'#dc2626','center',true);
    // 電子てんびん
    ctx.fillStyle='#cbd5e1'; rr(16,BB+5,152,6,3); ctx.fill(); ctx.fillStyle='#e2e8f0'; ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1.2; rr(12,BB+11,158,52,8); ctx.fill(); ctx.stroke();
    tx('電子',22,BB+33,10.5,'#475569','left',true); tx('てんびん',18,BB+48,10.5,'#475569','left',true);
    ctx.fillStyle='#0f172a'; rr(66,BB+18,96,36,5); ctx.fill(); tx(f1(c.tot)+' g',155,BB+43,19,'#4ade80','right',true);
    tx('水＋入れた物',208,BB+30,10,'#64748b','center',true); tx('の重さ',208,BB+44,10,'#64748b','center',true); }
  function niceMax(v){ const L=[10,20,30,40,50,60,80,100,120,150,180,240,300,360]; for(let i=0;i<L.length;i++) if(v<=L[i]) return L[i]; return 360; }
  const PL=298, PR=618, PT=68, PB=262;
  const gx=(t)=>PL+t/80*(PR-PL), gy=(v)=>PB-v/YM*(PB-PT);
  function drawGraph(c){ const sb=SUB[K];
    panel(256,6,378,294,'溶解度曲線（水100gに溶ける量）');
    let lx=268; KEYS.forEach(k=>{ const sel=k===K; ctx.globalAlpha=sel?1:0.55; ctx.strokeStyle=SUB[k].c; ctx.lineWidth=sel?3.2:2; line(lx,37,lx+14,37); ctx.globalAlpha=1; tx(SUB[k].n,lx+18,41,11,sel?SUB[k].c:'#64748b','left',sel); lx+=30+tw(SUB[k].n,11,sel)+8; });
    tx(WA===100?'水100gなので、グラフの値がそのまま溶ける量':'水'+Math.round(WA)+'gなので、溶ける量はグラフの値×'+Math.round(WA)+'÷100',300,57,10.5,'#64748b');
    const cap=K==='alum'?60:sb.S[8]*1.04; YM=frozen||niceMax(Math.max(cap,c.a*1.06));
    const stp=[2,5,10,20,30,40,50,60,100].find(s=>YM/s<=6)||100;
    ctx.strokeStyle='rgba(15,23,42,.08)'; ctx.lineWidth=1; for(let t=10;t<=80;t+=10) line(gx(t),PT,gx(t),PB); for(let v=stp;v<=YM+1e-9;v+=stp) line(PL,gy(v),PR,gy(v));
    ctx.strokeStyle='#334155'; ctx.lineWidth=1.5; line(PL,PT-4,PL,PB); line(PL,PB,PR+4,PB);
    for(let t=0;t<=80;t+=10) tx(String(t),gx(t),PB+14,10,'#475569','center');
    for(let v=0;v<=YM+1e-9;v+=stp) tx(String(v),PL-5,gy(v)+3.5,10,'#475569','right');
    tx('［g］',PL-5,PT-6,10,'#475569','right'); tx('水温［℃］',PR,PB+30,10.5,'#475569','right');
    ctx.save(); ctx.beginPath(); ctx.rect(PL,PT-2,PR-PL+2,PB-PT+2); ctx.clip();
    const order=KEYS.filter(k=>k!==K).concat([K]);
    order.forEach(k=>{ const sel=k===K; ctx.globalAlpha=sel?1:0.35; ctx.strokeStyle=SUB[k].c; ctx.lineWidth=sel?3:1.6; ctx.beginPath(); for(let t=0;t<=80.001;t+=0.5){ const X=gx(t),Y=gy(sol(k,t)); if(t===0) ctx.moveTo(X,Y); else ctx.lineTo(X,Y); } ctx.stroke(); });
    ctx.globalAlpha=1;
    if(trail && trail.M===M && trail.WA===WA && trail.K===K && Math.abs(trail.T0-TT)>0.3){ ctx.strokeStyle='rgba(13,148,136,.75)'; ctx.lineWidth=4; ctx.lineCap='round'; ctx.beginPath(); const s=trail.T0>TT?-0.25:0.25; let first=true; for(let t=trail.T0; s<0?t>=TT-1e-9:t<=TT+1e-9; t+=s){ const X=gx(t),Y=gy(Math.min(c.a,sol(K,t))); if(first){ ctx.moveTo(X,Y); first=false; } else ctx.lineTo(X,Y); } ctx.lineTo(gx(TT),gy(Math.min(c.a,sol(K,TT)))); ctx.stroke(); ctx.lineCap='butt'; }
    ctx.restore();
    if(K==='alum' && YM<330) halo('↑ 80℃では321.6g（グラフの外）',PR-4,PT+12,10.5,sb.c,'right',true);
    const S=sol(K,TT), x=gx(TT), aC=Math.min(c.a,YM), yS=gy(Math.min(c.a,S)), yA=gy(aC);
    // 結晶が出始める（全部溶ける）温度
    if(c.st>=0 && c.st<=80 && c.a<=YM && Math.abs(c.st-TT)>0.3){ const xs=gx(c.st); ctx.setLineDash([5,4]); ctx.strokeStyle='#64748b'; ctx.lineWidth=1.3; line(x,yA,xs,yA); line(xs,yA,xs,PB); ctx.setLineDash([]);
      ctx.fillStyle='#fff'; ctx.strokeStyle=sb.c; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(xs,yA,4.5,0,7); ctx.fill(); ctx.stroke();
      const lab=(c.res>0?'全部溶ける ':'結晶が出始める ')+f1(c.st)+'℃', lw=tw(lab,11,true), up=clamp(yA-8,PT+12,PB-6), dn=clamp(yA+17,PT+12,PB-6);
      if(c.res>0){ if(xs+8+lw<PR+8) halo(lab,xs+8,up,11,'#334155','left',true); else halo(lab,xs-8,dn,11,'#334155','right',true); }
      else { if(xs-8-lw>PL+2) halo(lab,xs-8,up,11,'#334155','right',true); else halo(lab,xs+8,dn,11,'#334155','left',true); } }
    if(c.a>S+1e-6){ ctx.strokeStyle='#dc2626'; ctx.lineWidth=3; line(x,yS,x,yA+5);
      ctx.strokeStyle='#dc2626'; ctx.lineWidth=2.2; ctx.fillStyle='#fff'; ctx.beginPath(); ctx.arc(x,yA,6,0,7); ctx.fill(); ctx.stroke();
      if(c.a>YM){ ctx.fillStyle='#dc2626'; ctx.beginPath(); ctx.moveTo(x,PT-6); ctx.lineTo(x-5,PT+2); ctx.lineTo(x+5,PT+2); ctx.closePath(); ctx.fill(); }
      const l1='溶け残り', w1=tw(l1,11.5,true), my=(yS+yA)/2+4; if(x+10+w1<PR) halo(l1,x+9,my,11.5,'#dc2626','left',true); else halo(l1,x-9,my,11.5,'#dc2626','right',true);
      const l2='入れた量', w2=tw(l2,11,true); if(x+10+w2<PR) halo(l2,x+9,yA-6,11,'#b91c1c','left',true); else halo(l2,x-9,yA-6,11,'#b91c1c','right',true); }
    ctx.fillStyle=sb.c; ctx.strokeStyle='#fff'; ctx.lineWidth=2.2; ctx.beginPath(); ctx.arc(x,yS,7,0,7); ctx.fill(); ctx.stroke();
    const l3=c.res>0?'溶けている量（飽和）':(c.a>=S-1e-6?'溶けている量（飽和）':'溶けている量'), w3=tw(l3,11,true), y3=c.res>0?yS+17:yS-10;
    if(x+10+w3<PR+6) halo(l3,x+9,clamp(y3,PT+10,PB-18),11,sb.c,'left',true); else halo(l3,x-9,clamp(y3,PT+10,PB-18),11,sb.c,'right',true); }
  function drawModel(){ const sb=SUB[K];
    panel(6,306,244,128,'粒子のモデル');
    tx('●＝'+sb.n+'の粒',244,325,10.5,sb.c,'right',true);
    ctx.fillStyle='rgba(186,230,253,.45)'; rr(MB.x0,MB.y0,MB.x1-MB.x0,MB.y1-MB.y0,6); ctx.fill();
    parts.forEach(p=>{ ctx.fillStyle=sb.c; ctx.beginPath(); ctx.arc(p.x,p.y,2.9,0,7); ctx.fill(); if(!p.d){ ctx.strokeStyle='rgba(15,23,42,.55)'; ctx.lineWidth=0.8; ctx.stroke(); } });
    if(!parts.length) tx('まだ何も溶かしていません',128,384,11,'#64748b','center'); }
  function drawBand(c){ const sb=SUB[K], X=268, MW=356;
    panel(256,306,378,128,'');
    const L1='重さ：水 '+Math.round(WA)+' g ＋ '+sb.n+' '+f1(M)+' g ＝ '+f1(c.tot)+' g'+(evap>0.05?'（蒸発した水'+Math.round(evap)+' gの分は軽い）':'（溶けても変わらない）');
    fit(L1,X,330,13,'#0f172a',MW,true);
    fit('溶ける限度：'+f1(c.S1)+' × '+Math.round(WA)+' ÷ 100 ＝ '+f1(c.lim)+' g（'+Math.round(TT)+'℃）',X,356,13,'#0369a1',MW,true);
    let L3, col3='#dc2626'; if(c.res>0) L3='溶け残り：'+f1(M)+' − '+f1(c.lim)+' ＝ '+f1(c.res)+' g'; else if(c.lim-M<0.05 && M>0) { L3='ちょうど限度まで溶けている（飽和水溶液）'; col3='#7c2d12'; } else { L3='あと '+f1(c.lim-M)+' g 溶ける（全部溶けている）'; col3='#15803d'; }
    fit(L3,X,382,13,col3,MW,true);
    fit('濃度：'+f1(c.dis)+' ÷（'+f1(c.dis)+' ＋ '+Math.round(WA)+'）× 100 ＝ '+f1(c.conc)+' %',X,408,13,'#334155',MW,true);
    fit('（質量パーセント濃度＝溶けている物の重さ÷水溶液の重さ×100）',X,426,10.5,'#64748b',MW,false); }
  function draw(){ const c=calc(); ctx.clearRect(0,0,W,H); ctx.fillStyle='#f8fafc'; ctx.fillRect(0,0,W,H);
    drawBeaker(c); drawGraph(c); drawModel(); drawBand(c);
    setStat('sDis',f1(c.dis)+' g'); setStat('sRes',f1(c.res)+' g'); setStat('sLim',f1(c.lim)+' g'); setStat('sTot',f1(c.tot)+' g'); setStat('sCon',f1(c.conc)+' %');
    setStat('sSat',c.st<0?'0℃でも全部溶ける':(c.st>80?'80℃でも溶けきらない':f1(c.st)+'℃')); setStat('sEv',WA<=10?'—':f1(c.ev)+' g');
    const sb=SUB[K], head='【物の溶け方】'+Math.round(TT)+'℃の水'+Math.round(WA)+'gに'+sb.n+'は'+f1(c.lim)+'gまで溶ける。';
    setShare(head+(c.res>0?f1(M)+'g入れると'+f1(c.res)+'gが溶け残る':f1(M)+'gは全部溶けて濃度'+f1(c.conc)+'%')+'｜シミュラボ'); }
  // ---------- 操作 ----------
  function syncUI(){ const a=$('wa'); a.value=Math.round(WA); $('waL').textContent=Math.round(WA)+' g'; const b=$('tt'); b.value=Math.round(TT); $('ttL').textContent=Math.round(TT)+'℃'; const m=$('mm'); m.value=M; $('mmL').textContent=f1(M)+' g';
    $('cool').disabled=TT<=0.01; $('heat').disabled=TT>=79.99; $('evap').disabled=WA<=10.01; $('add1').disabled=M>=200; $('add10').disabled=M>=200; }
  function grains(g){ const n=Math.min(9,2+Math.round(g)); for(let i=0;i<n;i++) drops.push({p:-i*0.06,x0:200+rnd(-5,5),y0:44,x1:PCX+rnd(-28,28),y1:BB-8,}); }
  function add(g){ if(M>=200) return; M=r1(Math.min(200,M+g)); trail=null; grains(g); pulse=1; syncUI(); }
  function tempTo(d){ if(!trail || trail.M!==M || trail.WA!==WA || trail.K!==K) trail={T0:TT,M:M,WA:WA,K:K}; const base=anim&&anim.k==='T'?anim.to:Math.round(TT); anim={k:'T',to:clamp(base+d,0,80)}; }
  $('sub').addEventListener('change',()=>{ K=$('sub').value; trail=null; anim=null; disV=calc().dis; seedParts(); });
  $('wa').addEventListener('input',()=>{ anim=null; WA=+$('wa').value; evap=0; trail=null; syncUI(); });
  $('tt').addEventListener('input',()=>{ anim=null; TT=+$('tt').value; syncUI(); });
  $('mm').addEventListener('input',()=>{ M=r1(+$('mm').value); trail=null; syncUI(); });
  $('add1').addEventListener('click',()=>add(1)); $('add10').addEventListener('click',()=>add(10));
  $('cool').addEventListener('click',()=>tempTo(-10)); $('heat').addEventListener('click',()=>tempTo(10));
  $('evap').addEventListener('click',()=>{ if(WA<=10.01) return; trail=null; const base=anim&&anim.k==='W'?anim.to:WA; anim={k:'W',to:Math.max(10,base-10)}; });
  $('empty').addEventListener('click',()=>{ anim=null; M=0; evap=0; trail=null; disV=0; drops=[]; seedParts(); syncUI(); });
  function pxy(e){ const p=cpos(cv,e); return [p[0]/dpr,p[1]/dpr]; }
  function setG(q){ TT=clamp(Math.round((q[0]-PL)/(PR-PL)*80),0,80); const a=clamp((PB-q[1])/(PB-PT)*YM,0,YM); M=r1(clamp(a*WA/100,0,200)); syncUI(); }
  cv.style.cursor='pointer';
  cv.addEventListener('pointerdown',(e)=>{ const q=pxy(e);
    if(q[0]>=PL-16 && q[0]<=PR+16 && q[1]>=PT-14 && q[1]<=PB+16){ drag=true; frozen=YM; trail=null; anim=null; try{ cv.setPointerCapture(e.pointerId); }catch(err){} setG(q); e.preventDefault(); return; }
    if(q[0]<250 && q[1]<BB+4){ add(1); e.preventDefault(); } });
  cv.addEventListener('pointermove',(e)=>{ if(!drag) return; setG(pxy(e)); e.preventDefault(); });
  ['pointerup','pointercancel','pointerleave'].forEach(n=>cv.addEventListener(n,()=>{ drag=false; frozen=null; }));
  function step(dt){
    if(anim){ if(anim.k==='T'){ const d=anim.to-TT, s=Math.sign(d)*Math.min(Math.abs(d),12*dt); TT+=s; if(Math.abs(anim.to-TT)<1e-6){ TT=anim.to; anim=null; } }
      else { const s=Math.min(WA-anim.to,15*dt); WA-=s; evap+=s; if(WA-anim.to<1e-6){ evap+=WA-anim.to; WA=anim.to; anim=null; } } syncUI(); }
    const c=calc(), g=c.dis-disV; if(Math.abs(g)<1e-4) disV=c.dis; else { const r=Math.max(1.2,Math.abs(g)*1.6)*dt; disV+=g>0?Math.min(g,r):Math.max(g,-r); }
    drops.forEach(d=>{ d.p+=dt/0.55; }); drops=drops.filter(d=>d.p<1);
    if(pulse>0) pulse=Math.max(0,pulse-dt*4);
    updParts(dt); }
  function loop(now){ const dt=Math.min(0.05,Math.max(0,(now-last)/1000)); last=now; step(dt); draw(); requestAnimationFrame(loop); }
  disV=calc().dis; seedParts(); syncUI(); draw(); requestAnimationFrame(loop);
'''.replace("@SUB@", SUB_JS).replace("@FF@", FF)

sim(slug="youkaido", cat="rika", emoji="🧂", score=81,
    title="物の溶け方と溶解度シミュレーター（溶け残り・再結晶・濃度）",
    title_tag="溶解度曲線・再結晶のシミュレーター｜物の溶け方（ミョウバン・食塩・硝酸カリウム）と質量パーセント濃度の計算",
    meta_desc="水の量・水温・溶かす物（食塩・ミョウバン・硝酸カリウム・ホウ酸）を変えて物を加えると、溶け残りが出る量や、冷やす・水を蒸発させると出てくる結晶の量が溶解度曲線の上で分かる無料シミュレーター。溶けても重さが変わらないことや質量パーセント濃度の計算も。小5・中1の理科の授業向け。",
    og_title="物の溶け方と溶解度シミュレーター（溶け残り・再結晶・濃度）",
    og_desc="水の量・水温・溶かす物を変えて溶け残りを観察。溶解度曲線で再結晶と質量パーセント濃度を確かめる。小5・中1の授業向け。",
    card_desc="水の量・水温・溶かす物を変えて溶け残りを観察。溶解度曲線で再結晶と濃度の計算まで確かめられる。",
    lead="スプーンをタップして物を水に加えていくと、ある量から溶け残りが出ます。水温・水の量・溶かす物（食塩・ミョウバン・硝酸カリウム・ホウ酸）を変えると、溶ける限度が溶解度曲線の上でどう変わるかが分かります。冷やしたり水を蒸発させたりして結晶を取り出せ、水と物とを合わせた重さが変わらないことも電子てんびんで確かめられます。",
    model="小5 物の溶け方／中1 水溶液（溶解度・再結晶）",
    level="小学5年、中学1年",
    unit="小学校 第5学年 A（1）物の溶け方／中学校 第1分野（2）身の回りの物質 ア（イ）水溶液",
    canvas=canvas(640, 440, light=True),
    controls=select("sub", "溶かす物", [("alum", "ミョウバン"), ("salt", "食塩（塩化ナトリウム）"), ("kno3", "硝酸カリウム"), ("boric", "ホウ酸")])
           + slider("wa", "水の量", 10, 200, 50, 10, "{v} g")
           + slider("tt", "水温", 0, 80, 20, 1, "{v}℃")
           + slider("mm", "加えた量", 0, 200, 10, 0.1, "{v} g"),
    buttons=btn("add1", "🥄 1g 加える", True) + btn("add10", "🥄 10g 加える") + btn("heat", "🔥 10℃ あたためる") + btn("cool", "❄ 10℃ 冷やす")
           + btn("evap", "♨ 水を10g 蒸発") + btn("empty", "↺ 水だけにもどす"),
    stats=stats([("sDis", "溶けている量", True), ("sRes", "溶け残り（出てきた結晶）", True), ("sLim", "この水に溶ける限度", False), ("sTot", "全体の重さ（水＋物）", False),
                 ("sCon", "濃度（質量パーセント濃度）", False), ("sSat", "全部溶ける温度（＝結晶が出始める温度）", False), ("sEv", "水を10g蒸発させると出てくる量", False)]),
    legend="左上：ビーカーと電子てんびん（スプーンやビーカーをタップすると1gずつ加わります）。右上：溶解度曲線（水100gあたりの値。グラフを指でなぞると水温と加えた量を変えられます）。●＝溶けている量、○と赤い線＝溶け残り。左下：粒子のモデル（水の粒は省略）。右下：重さ・限度・濃度の計算。",
    article=YOUKAI_ARTICLE,
    faqs=[("溶解度とは何ですか？", "100gの水に溶ける物質の最大の質量［g］のことです。物質の種類と水の温度によって決まり、たとえば20℃の溶解度は食塩が35.8g、ミョウバンが11.4g、硝酸カリウムが31.6gです。水の量が50gなら、溶ける量はその半分になります。"),
          ("ミョウバンは冷やすと出てくるのに、食塩はほとんど出てこないのはなぜですか？", "ミョウバンは水温によって溶ける量が大きく変わりますが、食塩は水温が変わっても溶ける量がほとんど変わらないからです。水100gの場合、60℃から20℃に冷やすと、ミョウバンは57.4−11.4＝46.0g出てきますが、食塩は37.1−35.8＝1.3gしか出てきません。食塩は水を蒸発させて取り出します。"),
          ("物が水に溶けても重さが変わらないのはなぜですか？", "溶けた物は、目に見えないほど小さな粒になって水の中に均一に広がっているだけで、なくなったわけではないからです。水50gに食塩5gを溶かすと、食塩水の重さは55gになります。"),
          ("質量パーセント濃度はどうやって求めますか？", "質量パーセント濃度［%］＝溶質の質量÷（溶質の質量＋溶媒の質量）×100 で求めます。水100gに食塩25gを溶かした食塩水なら、25÷125×100＝20%です。分母は水の質量ではなく、水溶液全体の質量です。"),
          ("溶け残りがあるとき、溶けている物と溶け残りを分けるにはどうしますか？", "ろ過します。ろ紙の上に溶け残り（結晶）が残り、ろ紙を通った液（ろ液）には溶けている物がふくまれています。ろ液を冷やしたり、水を蒸発させたりすると、溶けていた物を取り出せます。"),
          ("教科書の溶解度の値と少しちがいます。", "溶解度の表は、教科書や資料によって小数第1位などが少しちがうことがあります。特にミョウバンは、結晶（水をふくむ形）の質量で表すか、水をふくまない形で表すかで値が大きくちがいます。このシミュレーターは結晶の質量で表した値（20℃で11.4g）を使っています。授業やテストでは、使っている教科書や問題の値で計算してください。")],
    rel=[("joutai-henka", "🧊", "状態変化と粒子のシミュレーター"), ("shitsudo-roten", "☁️", "湿度と雲のでき方シミュレーター"), ("diffusion", "🫧", "拡散シミュレーター"),
         ("kagaku-shitsuryou", "🧪", "化学変化と質量シミュレーター"), ("nenshou", "🕯️", "ものの燃え方と空気シミュレーター")],
    js=JS_YOUKAI)


# ============================================================ 2 ものの燃え方と空気
# モデル：びんの中の気体を「はじめの空気の量を100」とした割合で表す（窒素・酸素・二酸化炭素・その他）。
#   炎の大きさ f＝√((酸素−16.8)/(21−16.8))（上限1.8）、f＜0.25 で火が消える（＝酸素 約17%）。
#   酸素の減り方＝k×f［%/秒］、二酸化炭素の増え方＝その r 倍（ろうそく k＝0.5・r＝0.66、木 k＝0.8・r＝1.0）。
#   空気の入れかわり q［/秒］：ふたなし＋すき間＝0.8、ふたなし＝0.27、ふた＋すき間＝0.012、ふた＝0（炎の熱で強まる）。
NENSHOU_ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
<p>ろうそくや木（植物体）が燃えると、空気中の<b>酸素の一部が使われて、二酸化炭素ができます</b>。ふたをした集気びんの中では、酸素は約21%から約17%に減り、二酸化炭素は約0.04%から約3〜4%に増えたところで火が消えます。<b>酸素がなくなったから消えるのではありません</b>。窒素は燃えることに関係しないので、約78%のまま変わりません。びんの下にすき間があり、上の口も開いていると、空気が下から入って上から出ていくので、物は燃え続けます。</p>
''' + N("対応する単元：小学校 第6学年 A（1）燃焼の仕組み（植物体が燃えるときには、空気中の酸素が使われて二酸化炭素ができること）") + '''
<h2>授業での使い方</h2>
<h3>導入：ふたをすると、なぜ火が消える？</h3>
<p>「ふたをする・すき間なし」の集気びんでろうそくを燃やし、しばらくすると火が消えることを見せます（はじめの画面の設定です）。「びんの中の空気は、燃える前と後で何が変わったのか」を問いにして、予想を書かせます。</p>
<h3>展開1：空気の通り道を線香のけむりで調べる</h3>
<p>「ふた」と「下のすき間」を変えた4つの集気びんで、燃え続けるかどうかを比べます（教科書の実験と同じ組み合わせです）。「💨 線香のけむり」を押し、線香を指で動かしてすき間やびんの口に近づけると、けむりの動きから空気の流れが分かります。下にすき間がある「ふたなし」のびんでは、けむりがすき間から吸いこまれて上の口から出ていきます。ふたをしたびんでは、けむりはほとんど入っていきません。</p>
<h3>展開2：気体検知管と石灰水で、燃やす前と後の空気を比べる</h3>
<p>ふたをしたびんで火が消えたら、右上の気体検知管の値を、燃やす前の値と比べます。「🧪 石灰水を入れてふる」で、燃やす前の空気ではにごらないこと、燃やした後の空気では白くにごることを確かめます。</p>
<h3>まとめ：粒の図で説明する</h3>
<p>右の「空気の粒（100こ）」の図で、燃やす前と後の空気を表します。窒素の粒の数は変わらず、酸素の粒が4こほど減り、二酸化炭素の粒が3〜4こ増えたことを、自分の言葉で説明させます。</p>
<p><b>児童への問いの例</b></p>
<ol>
<li>ろうそくの火が消えたあと、集気びんの中の酸素は全部なくなっているでしょうか。気体検知管の値から考えましょう。</li>
<li>ふたをしないびんで、下にすき間があるときとないときでは、燃え方がどうちがうでしょう。線香のけむりの動きから理由を説明しましょう。</li>
<li>火が消えたびんの中に、もう一度火のついたろうそくを入れると、どうなるでしょう。（答え：すぐに消える。酸素は約17%残っているが、燃え続けるには足りない）</li>
</ol>
<h2>しくみ・解説</h2>
<h3>用語の意味</h3>
<ul>
<li><b>物が燃える</b>とは、物が空気中の酸素と結びついて、熱や光を出しながら別の物（二酸化炭素や水など）に変わることです。</li>
<li><b>酸素</b>は、物を燃やす働きがある気体で、空気の体積の約21%をしめています。</li>
<li><b>二酸化炭素</b>は、物を燃やす働きがなく、<b>石灰水を白くにごらせる</b>性質がある気体で、空気中には約0.04%ふくまれています。</li>
<li><b>窒素</b>は、空気の体積の約78%をしめる気体で、物を燃やす働きはなく、燃える前と後で量が変わりません。</li>
<li><b>気体検知管</b>は、気体を吸いこむと色が変わる薬が入った管で、色の変わった部分の境目の目盛りを読むと、酸素や二酸化炭素の割合［%］が分かります。</li>
</ul>
<h3>燃やす前と後の空気（早見表）</h3>
''' + T([["窒素", "約78%", "約78%", "変わらない（燃えることに関係しない）"],
          ["酸素", "約21%", "約17%", "減る（燃えるときに使われる）。0%にはならない"],
          ["二酸化炭素", "約0.04%", "約3〜4%", "増える（燃えるとできる）。石灰水が白くにごる"],
          ["その他（アルゴン・水蒸気など）", "約1%", "約1〜2%", "—"]],
         ["気体", "燃やす前", "燃やした後（火が消えたとき）", "変化"]) + '''
<p>このシミュレーションでは、ふたをした集気びんでろうそくを燃やすと、約12.6秒で火が消え、そのときの酸素は約17.1%、二酸化炭素は約2.6%です。木（わりばし）では、二酸化炭素は約4.0%になります。</p>
<h3>集気びんの条件と燃え方</h3>
''' + T([["ふたをする・すき間なし", "入らない", "火が消える（約12.6秒）"],
          ["ふたをする・下にすき間あり", "ほとんど入らない", "火が消える（約13.7秒）"],
          ["ふたをしない・すき間なし", "上の口のふちから入り、まん中から出ていく", "燃え続ける（炎は少し小さくなる。酸素 約19.3%）"],
          ["ふたをしない・下にすき間あり", "下のすき間から入り、上の口から出ていく", "よく燃え続ける（酸素 約20.4%）"]],
         ["集気びんの条件", "線香のけむりの動き", "ろうそくの燃え方（このシミュレーションの値）"]) + '''
<p>炎であたためられた空気は軽くなって上へ動くので、上の口から出ていきます。そのとき、まわりの新しい空気が下のすき間（すき間がなければ上の口のふち）から入ってきます。このように<b>空気が入れかわるところでは燃え続け、入れかわらないところでは燃えなくなります</b>。</p>
<h3>よくある誤解：火が消えたとき、酸素はなくなっている？</h3>
<p>なくなっていません。ふたをした集気びんでろうそくの火が消えたときも、酸素はまだ<b>約17%</b>残っています（空気中の約21%のうち、使われたのは5分の1ほどです）。ろうそくの炎は、まわりの酸素の割合がある程度より小さくなると、燃え続けることができなくなるためです。そのため、火が消えたびんの中に火のついたろうそくを入れ直しても、すぐに消えてしまいます。グラフの赤い線（酸素）が0%まで下がらず、約17%で止まっていることを確かめてください。</p>
<p>「二酸化炭素が増えたから消えた」と考える児童もいますが、二酸化炭素は約3〜4%しかなく、窒素も約78%のまま変わりません。消えた主なわけは、<b>燃え続けるのに必要な割合より酸素が少なくなったこと</b>です。二酸化炭素や窒素には物を燃やす働きがないので、「びんの中の気体」を窒素や二酸化炭素にすると、火はすぐに消えます。酸素にすると、空気中より激しく燃えます。</p>
<p>燃やした後の空気（酸素 約17%、二酸化炭素 約3〜4%）は、人がはいた息（酸素 約17%、二酸化炭素 約4%）とよく似ています。体の中でも、酸素が使われて二酸化炭素ができているからです（第6学年「人の体のつくりと働き」）。</p>
<h3>二酸化炭素の増え方が、酸素の減り方より少し小さいわけ（発展）</h3>
<p>ろうそくのろうは、主に炭素と水素からできています。燃えると、炭素は酸素と結びついて二酸化炭素に、水素は酸素と結びついて水（水蒸気）になります。使われた酸素の一部が水になる分、二酸化炭素の増え方は酸素の減り方より小さくなります（このシミュレーションでは約3分の2）。燃えた後の集気びんの内側が白くくもるのは、できた水蒸気が冷えて水滴になるためです。木の主な成分（セルロース）では、使われる酸素とできる二酸化炭素がほぼ同じ量になります。</p>
''' + N("<b>このシミュレーションで単純化している点</b><br>"
     "・びんの中の気体は、はじめの空気の量を100としたときの割合で表しています。そのため窒素は78%のまま変わらず、ろうそくから出た水蒸気などは「その他」に入れています。<br>"
     "・ろうそくは、酸素が約17%（16.8%）に近づくと炎が小さくなり、消えるものとしています。消えるまでの時間や消えたときの値は、集気びんの大きさ・ろうそくの太さ・びんの温度などで変わり、実際の実験では酸素 約16〜18%、二酸化炭素 約2〜4%になることがあります。<br>"
     "・空気の流れ（線香のけむりの動き）は、教科書の実験で見られる流れ方を簡単なきまりで表したもので、実際の流れを計算したものではありません。<br>"
     "・気体検知管は、酸素用（6〜24%）と、二酸化炭素用（0.03〜1%と0.5〜8%の2種類）を表示しています。実際の酸素用検知管は使ったあと熱くなるので、すぐにさわらないようにします。") + '''
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「小学校学習指導要領（平成29年告示）解説 理科編」第6学年 A（1）燃焼の仕組み（''' + A(MEXT_SHO, "小学校学習指導要領解説") + '''）</li>
<li>小学校理科の教科書（東京書籍「新しい理科」、啓林館「わくわく理科」、大日本図書「たのしい理科」など）6年の「ものの燃え方と空気」の単元</li>
<li>国立天文台 編『理科年表』（丸善出版）「大気の組成」（窒素 78.08%、酸素 20.95%、アルゴン 0.93%、二酸化炭素 約0.04%）</li>
</ul>
'''

JS_NENSHOU = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  cv.setAttribute('role','img'); cv.setAttribute('aria-label','集気びんの中でろうそくを燃やすシミュレーション。酸素と二酸化炭素の割合、気体検知管、石灰水の変化が分かります');
  const FF='@FF@';
  const AIR=[78.0,21.0,0.04,0.96], GAS={air:AIR,o2:[0,100,0,0],n2:[100,0,0,0],co2:[0,0,100,0]};
  const FUEL={candle:{k:0.5,r:0.66,n:'ろうそく'},wood:{k:0.8,r:1.0,n:'木'}};
  const OX=16.8, FMIN=0.25, CN='#94a3b8', CO='#ef4444', CC='#2563eb', CX='#e2e8f0';
  const BCX=136, BX0=66, BX1=206, NK0=106, NK1=166, MOUTH=76, SHO=96, BODY=124, BOT=404, CL0=46, CL1=226;
  const isLid=()=>$('lid').value==='on', isGap=()=>$('gap').value==='yes';
  const r1=(v)=>Math.round(v*10+1e-7)/10, f1=(v)=>r1(v).toFixed(1), fc=(v)=>v<0.995?(Math.round(v*100+1e-7)/100).toFixed(2):f1(v);
  const GASN=()=>({air:'空気',o2:'酸素',n2:'窒素',co2:'二酸化炭素'})[$('gas').value];
  function tx(s,x,y,size,col,align,bold){ ctx.font=(bold?'bold ':'')+size+'px '+FF; ctx.textAlign=align||'left'; ctx.fillStyle=col; ctx.fillText(s,x,y); ctx.textAlign='left'; }
  function tw(s,size,bold){ ctx.font=(bold?'bold ':'')+size+'px '+FF; return ctx.measureText(s).width; }
  function halo(s,x,y,size,col,align,bold){ ctx.font=(bold?'bold ':'')+size+'px '+FF; ctx.textAlign=align||'left'; ctx.lineJoin='round'; ctx.lineWidth=3.5; ctx.strokeStyle='rgba(255,255,255,.95)'; ctx.strokeText(s,x,y); ctx.fillStyle=col; ctx.fillText(s,x,y); ctx.textAlign='left'; }
  function fit(s,x,y,size,col,maxW,bold){ let z=size; while(z>9 && tw(s,z,bold)>maxW) z-=0.5; tx(s,x,y,z,col,'left',bold); }
  function rr(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
  function panel(x,y,w,h,title){ ctx.fillStyle='#fff'; ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1.2; rr(x,y,w,h,10); ctx.fill(); ctx.stroke(); if(title) tx(title,x+10,y+19,12.5,'#0f172a','left',true); }
  function line(a,b,c,d){ ctx.beginPath(); ctx.moveTo(a,b); ctx.lineTo(c,d); ctx.stroke(); }
  function dot(x,y,r,col){ ctx.fillStyle=col; ctx.beginPath(); ctx.arc(x,y,r,0,7); ctx.fill(); }
  // ---------- 状態 ----------
  let comp, before, after, lit, heat, fl=0, t, hist, recAcc, outT, lw=null, shake=0, fog, wisp, smokeOn=false, smoke=[], sen=null, dragSen=false, fast=false, emitAcc=0, last=performance.now();
  const fuel=()=>FUEL[$('fuel').value];
  function flameF(){ return Math.min(1.8,Math.sqrt(Math.max(0,(comp[1]-OX)/(21-OX)))); }
  function start(){ comp=GAS[$('gas').value].slice(); before=comp.slice(); after=null; lit=true; heat=0.7; t=0; hist=[[0,comp[1],comp[2]]]; recAcc=0; outT=null; lw=null; fog=0; wisp=0; fl=flameF(); }
  function baseQ(){ const L=isLid(), G=isGap(); return L?(G?0.012:0):(G?0.8:0.27); }
  function step(dt){ t+=dt; let f=0;
    if(lit){ f=flameF(); if(f<FMIN){ lit=false; outT=t; after=comp.slice(); wisp=5; f=0; } }
    fl=f; heat+=((lit?Math.min(1,f):0)-heat)*Math.min(1,dt/(lit?0.5:3));
    const q=baseQ()*(0.25+0.75*heat), F=fuel();
    comp[1]=Math.max(0,comp[1]-F.k*f*dt); comp[2]+=F.k*f*F.r*dt;
    for(let i=0;i<4;i++) comp[i]+=q*(AIR[i]-comp[i])*dt;
    fog=Math.max(0,fog+F.k*f*dt*0.1-(q+0.01)*fog*dt); if(wisp>0) wisp-=dt;
    recAcc+=dt; if(recAcc>=0.2){ recAcc=0; hist.push([t,comp[1],comp[2]]); if(hist.length>3000) hist=hist.filter((h,i)=>i%2===0); } }
  // ---------- 空気の流れ（線香のけむり） ----------
  function halfW(y){ if(y>=BODY) return BX1-BCX; if(y>=SHO) return (NK1-BCX)+(y-SHO)/(BODY-SHO)*((BX1-BCX)-(NK1-BCX)); return NK1-BCX; }
  function inside(x,y){ return y>=MOUTH && y<=BOT && Math.abs(x-BCX)<=halfW(y); }
  function opening(x,y){ if(!isLid() && Math.abs(x-BCX)<NK1-BCX+2 && y>=MOUTH-8 && y<=MOUTH+10) return true;
    if(isGap() && y>=396 && y<=418 && (Math.abs(x-BX0)<=14 || Math.abs(x-BX1)<=14)) return true; return false; }
  function vel(x,y){ const L=isLid(), G=isGap(), h=heat; let vx=0, vy=-12;
    if(!inside(x,y)){
      if(!L && Math.abs(x-BCX)<(G?34:16) && y<MOUTH+2){ vy-=70*h; vx+=(BCX-x)*0.5*h; }
      if(!L && G){ [BX0,BX1].forEach(nx=>{ const tx2=nx+Math.sign(BCX-nx)*10, dx=tx2-x, dy=400-y, d=Math.hypot(dx,dy); if(d<85){ const s=80*h*(1-d/85)/(d+1); vx+=dx*s; vy+=dy*s+12*h*(1-d/85); } }); }
      if(!L && !G){ [NK0+8,NK1-8].forEach(mx=>{ const dx=mx-x, dy=MOUTH+12-y, d=Math.hypot(dx,dy); if(d<65){ const s=70*h*(1-d/65)/(d+1); vx+=dx*s; vy+=dy*s+12*h*(1-d/65); } }); }
    } else { const dxc=x-BCX;
      if(!L && G){ vy=-55*h-3; vx=(y>340?-dxc*0.8:-dxc*0.25)*h; if(y<BODY) vx=-dxc*1.6*h; }
      else if(!L){ const core=Math.abs(dxc)<(y<BODY?14:24); if(core){ vy=-45*h-3; vx=-dxc*0.5*h; } else { vy=30*h; vx=(y>360?-Math.sign(dxc)*35*h:0); } }
      else { const core=Math.abs(dxc)<30; vy=(core?-22:16)*h-2; vx=y>360?-Math.sign(dxc)*18*h:(y<150?Math.sign(dxc)*18*h:0); } }
    return [vx,vy]; }
  function moveP(p,dt){ const v=vel(p.x,p.y); let nx=p.x+(v[0]+randn()*9)*dt, ny=p.y+(v[1]+randn()*9)*dt;
    const a=inside(p.x,p.y), b=inside(nx,ny);
    if(a!==b && !opening(nx,ny) && !opening(p.x,p.y)) return;
    if(!b && ny>BOT && nx>CL0 && nx<CL1 && !opening(nx,ny)) ny=BOT;
    p.x=nx; p.y=Math.min(ny,428); }
  function senDefault(){ return isGap()?{x:BX0-22,y:410}:{x:NK0-20,y:MOUTH-6}; }
  // ---------- 描画 ----------
  function flame(x,y,s,wood){ if(s<=0.01) return; const now=performance.now(), fk=1+Math.sin(now/90)*0.05+Math.sin(now/37)*0.03;
    const h=(wood?46:30)*s*fk, w=(wood?15:9)*Math.min(1.4,s);
    const g=ctx.createRadialGradient(x,y-h*0.45,2,x,y-h*0.45,h*1.1); g.addColorStop(0,'rgba(253,224,71,.45)'); g.addColorStop(1,'rgba(253,224,71,0)'); ctx.fillStyle=g; ctx.beginPath(); ctx.arc(x,y-h*0.45,h*1.1,0,7); ctx.fill();
    const g2=ctx.createLinearGradient(0,y-h,0,y); g2.addColorStop(0,s>1.2?'#fff7ed':'#fde68a'); g2.addColorStop(0.6,s>1.2?'#fde68a':'#fb923c'); g2.addColorStop(1,'#f97316');
    ctx.fillStyle=g2; ctx.beginPath(); ctx.moveTo(x,y-h); ctx.bezierCurveTo(x+w,y-h*0.45,x+w,y,x,y); ctx.bezierCurveTo(x-w,y,x-w,y-h*0.45,x,y-h); ctx.fill();
    ctx.fillStyle='rgba(59,130,246,.55)'; ctx.beginPath(); ctx.ellipse(x,y-2,w*0.35,h*0.12,0,0,7); ctx.fill(); }
  function drawScene(){ const L=isLid(), G=isGap(), F=$('fuel').value;
    panel(6,6,262,448,'集気びん（'+(L?'ふたあり':'ふたなし')+'・'+(G?'下にすき間あり':'すき間なし')+'）');
    tx('びんの口・下のすき間・線香は指で操作できます',16,40,10.5,'#64748b');
    ctx.fillStyle='#e7e5e4'; ctx.fillRect(10,430,254,6);
    ctx.fillStyle='#d6b98c'; rr(CL0,BOT,CL1-CL0,26,5); ctx.fill();
    if(G){ ctx.fillStyle='#fff'; [BX0,BX1].forEach(nx=>{ ctx.fillRect(nx-11,BOT-0.5,22,13); }); ctx.strokeStyle='#a16207'; ctx.lineWidth=1; [BX0,BX1].forEach(nx=>{ ctx.strokeRect(nx-11,BOT,22,12.5); }); }
    ctx.beginPath(); ctx.moveTo(BX0,BOT); ctx.lineTo(BX0,BODY); ctx.quadraticCurveTo(BX0,SHO,NK0,SHO); ctx.lineTo(NK0,MOUTH); ctx.lineTo(NK1,MOUTH); ctx.lineTo(NK1,SHO); ctx.quadraticCurveTo(BX1,SHO,BX1,BODY); ctx.lineTo(BX1,BOT); ctx.closePath();
    ctx.fillStyle='rgba(224,242,254,.35)'; ctx.fill();
    if(fog>0.08){ ctx.fillStyle='rgba(148,163,184,'+Math.min(0.5,(fog-0.08)*1.5).toFixed(3)+')'; for(let i=0;i<46;i++){ const s=Math.sin(i*91.7)*0.5+0.5, yy=BODY+8+s*(BOT-BODY-30), xx=i%2?BX0+4+Math.sin(i*7.1)*2.5:BX1-4+Math.sin(i*5.3)*2.5; ctx.beginPath(); ctx.arc(xx,yy,1.6+(i%3)*0.5,0,7); ctx.fill(); } }
    if(F==='candle'){ ctx.fillStyle='#fefce8'; ctx.strokeStyle='#d6d3d1'; ctx.lineWidth=1.2; ctx.fillRect(BCX-9,334,18,BOT-334); ctx.strokeRect(BCX-9,334,18,BOT-334); ctx.strokeStyle='#292524'; ctx.lineWidth=2; line(BCX,334,BCX,326); if(lit) flame(BCX,328,fl,false); }
    else { ctx.lineCap='round'; ctx.lineWidth=5; ctx.strokeStyle='#b45309'; line(BCX-24,BOT-2,BCX+10,352); line(BCX+24,BOT-2,BCX-10,352); line(BCX,BOT-2,BCX,348);
      if(t>2){ ctx.strokeStyle='#1c1917'; line(BCX+4,358,BCX+10,352); line(BCX-4,358,BCX-10,352); line(BCX,356,BCX,348); } ctx.lineCap='butt'; if(lit) flame(BCX,358,fl,true); }
    if(!lit && wisp>0){ ctx.strokeStyle='rgba(100,116,139,'+Math.min(0.6,wisp/5).toFixed(3)+')'; ctx.lineWidth=2; ctx.beginPath(); const y0=F==='candle'?326:350; for(let i=0;i<=20;i++){ const yy=y0-i*2.4, xx=BCX+Math.sin(i*0.7+performance.now()/260)*4*(i/20); if(i) ctx.lineTo(xx,yy); else ctx.moveTo(xx,yy); } ctx.stroke(); }
    ctx.strokeStyle='#64748b'; ctx.lineWidth=2.5; ctx.beginPath(); ctx.moveTo(BX0,BOT); ctx.lineTo(BX0,BODY); ctx.quadraticCurveTo(BX0,SHO,NK0,SHO); ctx.lineTo(NK0,MOUTH); ctx.lineTo(NK0-4,MOUTH); ctx.moveTo(BX1,BOT); ctx.lineTo(BX1,BODY); ctx.quadraticCurveTo(BX1,SHO,NK1,SHO); ctx.lineTo(NK1,MOUTH); ctx.lineTo(NK1+4,MOUTH); ctx.stroke();
    ctx.strokeStyle='rgba(255,255,255,.85)'; ctx.lineWidth=3; line(BX0+9,BODY+14,BX0+9,BOT-26);
    if(L){ ctx.fillStyle='rgba(186,230,253,.9)'; ctx.strokeStyle='#64748b'; ctx.lineWidth=1.2; ctx.fillRect(NK0-14,MOUTH-7,NK1-NK0+28,7); ctx.strokeRect(NK0-14,MOUTH-7,NK1-NK0+28,7); tx('ふた（ガラス板）',BCX,MOUTH-12,10.5,'#475569','center',true); }
    else tx('上の口',BCX,MOUTH-8,10.5,'#94a3b8','center',true);
    tx(G?'すき間':'すき間なし',BX0,446,10,'#a16207','center',true);
    smoke.forEach(p=>{ const a=0.42*(1-p.age/12), r=2+Math.min(7,p.age*1.3); ctx.fillStyle='rgba(100,116,139,'+Math.max(0,a).toFixed(3)+')'; ctx.beginPath(); ctx.arc(p.x,p.y,r,0,7); ctx.fill(); });
    if(smokeOn && sen){ ctx.strokeStyle='#65a30d'; ctx.lineWidth=3; ctx.lineCap='round'; line(sen.x,sen.y,sen.x-26,sen.y+20); ctx.lineCap='butt'; dot(sen.x,sen.y,3.5,'#f97316'); dot(sen.x,sen.y,1.6,'#fde047'); halo('線香',Math.max(30,sen.x-8),sen.y-9,10,'#3f6212','right',true); }
    const st=lit?(fl>1.2?'激しく燃えている':(fl>0.8?'燃えている':'炎が小さくなってきた')):(outT<0.3?'すぐに火が消えた':'火が消えた（'+outT.toFixed(1)+'秒後）');
    halo(st,BCX+64,446,13.5,lit?'#c2410c':'#334155','center',true); }
  function tube(y,label,lo,hi,v,col,ticks,labs){ const x0=290, x1=514;
    tx(label,x0-2,y-12,11,'#334155','left',true);
    ctx.fillStyle='#fefce8'; ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1.2; rr(x0,y-6,x1-x0,12,6); ctx.fill(); ctx.stroke();
    const xr=x0+clamp((v-lo)/(hi-lo),0,1)*(x1-x0); if(xr>x0+1){ ctx.save(); rr(x0,y-6,x1-x0,12,6); ctx.clip(); ctx.fillStyle=col; ctx.fillRect(x0,y-6,xr-x0,12); ctx.restore(); }
    ctx.strokeStyle='#64748b'; ctx.lineWidth=1; ticks.forEach(tv=>{ const xx=x0+(tv-lo)/(hi-lo)*(x1-x0); line(xx,y+6,xx,y+9); });
    labs.forEach(tv=>{ const xx=x0+(tv-lo)/(hi-lo)*(x1-x0); line(xx,y+6,xx,y+11); tx(String(tv),xx,y+21,9.5,'#64748b','center'); });
    if(v>lo && v<hi){ ctx.fillStyle='#0f172a'; ctx.beginPath(); ctx.moveTo(xr,y-8); ctx.lineTo(xr-4,y-14); ctx.lineTo(xr+4,y-14); ctx.closePath(); ctx.fill(); } }
  function drawTubes(){ const o=comp[1], c=comp[2];
    panel(276,6,358,138,'気体検知管で調べる');
    const ot=[]; for(let v=6;v<=24;v++) ot.push(v);
    tube(56,'酸素用（6〜24%）',6,24,o,'#f9a8d4',ot,[6,10,14,18,22]);
    const big=c>=0.995, ct=[]; if(big){ for(let v=0.5;v<=8.001;v+=0.5) ct.push(v); } else { for(let v=0.1;v<=1.001;v+=0.1) ct.push(Math.round(v*10)/10); }
    tube(110,big?'二酸化炭素用（0.5〜8%）':'二酸化炭素用（0.03〜1%）',big?0.5:0.03,big?8:1,c,'#c4b5fd',ct,big?[1,2,4,6,8]:[0.2,0.4,0.6,0.8,1]);
    tx(o>24?'24%より多い':(o<6?'6%より少ない':f1(o)+'%'),628,58,o>24||o<6?13:21,CO,'right',true); tx('はじめ '+f1(before[1])+'%',628,74,10.5,'#64748b','right');
    tx(c>8?'8%より多い':fc(c)+'%',628,112,c>8?13:21,CC,'right',true); tx('はじめ '+fc(before[2])+'%',628,128,10.5,'#64748b','right');
    tx(after?'（火が消えたあと）':'（いま）',628,25,10.5,'#64748b','right'); }
  function counts(v){ const n=[Math.round(v[0]),Math.round(v[1]),Math.round(v[2])]; let s=n[0]+n[1]+n[2]; while(s>100){ const i=n.indexOf(Math.max(n[0],n[1],n[2])); n[i]--; s--; } n.push(100-s); return n; }
  function grid(x0,y0,n){ const cols=[CN,CO,CC,CX]; let k=0; for(let g=0;g<4;g++){ for(let j=0;j<n[g];j++){ const r=Math.floor(k/10), c=k%10, X=x0+c*7.3+3, Y=y0+r*7.1+3; dot(X,Y,2.9,cols[g]); if(g===3){ ctx.strokeStyle='#94a3b8'; ctx.lineWidth=0.8; ctx.beginPath(); ctx.arc(X,Y,2.9,0,7); ctx.stroke(); } k++; } } }
  function drawDots(){ panel(276,150,358,120,'空気の粒（100こ）で表すと'); const nb=counts(before), nn=counts(comp);
    tx('燃やす前',292,185,11,'#334155','left',true); tx(after?'火が消えたあと':'いま',384,185,11,'#334155','left',true);
    grid(290,191,nb); grid(382,191,nn);
    const L=[['窒素',CN,0,'#475569'],['酸素',CO,1,CO],['二酸化炭素',CC,2,CC],['その他',CX,3,'#64748b']];
    L.forEach((it,i)=>{ const y=200+i*18; dot(476,y-4,4.2,it[1]); if(i===3){ ctx.strokeStyle='#94a3b8'; ctx.lineWidth=0.8; ctx.beginPath(); ctx.arc(476,y-4,4.2,0,7); ctx.stroke(); } tx(it[0]+' '+nb[it[2]]+' → '+nn[it[2]]+'こ',484,y,11,it[3],'left',true); });
    tx('1こ＝約1%',628,169,10,'#64748b','right'); }
  function drawGraph(){ panel(276,276,358,118,'酸素・二酸化炭素の割合の変化'); const PL=312, PR=614, PT=302, PB=372;
    let ym=25; for(let i=0;i<hist.length;i++){ if(hist[i][1]>24||hist[i][2]>24){ ym=100; break; } } if(comp[1]>24||comp[2]>24) ym=100;
    const tmax=Math.max(30,Math.ceil((t+0.01)/10)*10), ts=tmax<=60?10:(tmax<=150?30:60);
    const gx=(v)=>PL+v/tmax*(PR-PL), gy=(v)=>PB-Math.min(v,ym)/ym*(PB-PT);
    ctx.strokeStyle='rgba(15,23,42,.08)'; ctx.lineWidth=1; const ys=ym===25?5:20; for(let v=ys;v<=ym;v+=ys) line(PL,gy(v),PR,gy(v));
    ctx.strokeStyle='#334155'; ctx.lineWidth=1.3; line(PL,PT-2,PL,PB); line(PL,PB,PR+3,PB);
    for(let v=0;v<=ym;v+=ys) tx(String(v),PL-4,gy(v)+3.5,9.5,'#64748b','right'); tx('%',PL-4,PT-7,9.5,'#64748b','right');
    for(let v=0;v<=tmax;v+=ts) tx(String(v),gx(v),PB+12,9.5,'#64748b','center'); tx('秒',PR+11,PB+12,9.5,'#64748b','center');
    [[1,CO],[2,CC]].forEach(q=>{ ctx.strokeStyle=q[1]; ctx.lineWidth=2.4; ctx.beginPath(); hist.forEach((h,i)=>{ const X=gx(h[0]),Y=gy(h[q[0]]); if(i) ctx.lineTo(X,Y); else ctx.moveTo(X,Y); }); ctx.lineTo(gx(t),gy(comp[q[0]])); ctx.stroke(); });
    if(outT!=null){ const xo=gx(outT); ctx.setLineDash([4,3]); ctx.strokeStyle='#64748b'; ctx.lineWidth=1.2; line(xo,PT,xo,PB); ctx.setLineDash([]); halo('火が消えた',clamp(xo+4,PL+2,PR-60),PT+9,10.5,'#334155','left',true); }
    const xe=gx(t), yo=gy(comp[1]), yc=gy(comp[2]);
    const lo='酸素 '+f1(comp[1])+'%', lc='二酸化炭素 '+fc(comp[2])+'%';
    halo(lo,clamp(xe+6,PL+4,PR-tw(lo,11,true)),clamp(yo-6,PT+20,PB-20),11,CO,'left',true);
    halo(lc,clamp(xe+6,PL+4,PR-tw(lc,11,true)),clamp(yc-6,PT+34,PB-4),11,CC,'left',true);
    if(!lit && outT>0.3 && comp[1]>5 && ym===25){ halo('酸素は0%にならない（約'+Math.round(comp[1])+'%残る）',PL+8,gy(comp[1])+18,11,'#b91c1c','left',true); } }
  function drawLime(){ panel(276,400,358,54,''); const v=lw?lw.v:0, dx=shake>0?Math.sin(shake*40)*2.5:0;
    ctx.save(); ctx.translate(dx,0); ctx.fillStyle='rgba(186,230,253,.55)'; ctx.fillRect(290,418,16,28);
    if(lw){ ctx.fillStyle='rgba(248,250,252,'+(0.1+v*0.9).toFixed(3)+')'; ctx.fillRect(290,418,16,28); for(let i=0;i<9;i++) dot(292.5+(i*5.3)%11,421+(i*7.7)%23,1.1,'rgba(148,163,184,'+(v*0.9).toFixed(3)+')'); }
    ctx.strokeStyle='#64748b'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.moveTo(289,408); ctx.lineTo(289,444); ctx.quadraticCurveTo(289,449,298,449); ctx.quadraticCurveTo(307,449,307,444); ctx.lineTo(307,408); ctx.stroke(); ctx.restore();
    const s1=!lw?'石灰水：まだ調べていない（「石灰水を入れてふる」で調べる）':(v>0.5?'石灰水：白くにごった → 二酸化炭素がふえている':(v>0.12?'石灰水：少しにごった':'石灰水：にごらない（変化なし）'));
    fit(s1,318,424,12,lw&&v>0.12?'#1e3a8a':'#334155',308,true);
    fit('窒素：'+f1(comp[0])+'%（燃えることに関係しないので、変わらない）',318,444,11,'#475569',308,false); }
  function draw(){ ctx.clearRect(0,0,W,H); ctx.fillStyle='#f8fafc'; ctx.fillRect(0,0,W,H); drawScene(); drawTubes(); drawDots(); drawGraph(); drawLime();
    setStat('sO',f1(comp[1])+'%'); setStat('sC',fc(comp[2])+'%'); setStat('sN',f1(comp[0])+'%');
    setStat('sF',lit?(fl>1.2?'激しく燃える':(fl>0.8?'燃えている':'炎が小さい')):'消えた'); setStat('sT',lit?t.toFixed(1)+' 秒〜':outT.toFixed(1)+' 秒');
    setStat('sL',!lw?'まだ調べていない':(lw.v>0.5?'白くにごった':(lw.v>0.12?'少しにごった':'にごらない')));
    const cond=(isLid()?'ふたをした':'ふたをしない')+(isGap()?'・下にすき間がある':'')+'集気びん', F=fuel().n;
    let sh; if(after && $('gas').value==='air') sh='【ものの燃え方】'+cond+'の'+F+'は'+outT.toFixed(1)+'秒で火が消えた。酸素'+f1(before[1])+'%→'+f1(after[1])+'%、二酸化炭素'+fc(before[2])+'%→'+fc(after[2])+'%。酸素はなくならない｜シミュラボ';
    else if(lit) sh='【ものの燃え方】'+cond+'の中で'+F+'が燃えている（酸素'+f1(comp[1])+'%・二酸化炭素'+fc(comp[2])+'%）｜シミュラボ';
    else sh='【ものの燃え方】'+GASN()+'の中では'+F+'の火はすぐに消えた｜シミュラボ';
    setShare(sh); }
  // ---------- 操作 ----------
  function upd(dt){ let rem=dt; while(rem>1e-9){ const h=Math.min(0.05,rem); step(h); rem-=h; }
    if(smokeOn && sen){ emitAcc+=dt*28; while(emitAcc>=1){ emitAcc-=1; smoke.push({x:sen.x+rnd(-1.5,1.5),y:sen.y-2,age:0}); } }
    const n=Math.max(1,Math.ceil(dt/0.05)); smoke.forEach(p=>{ for(let i=0;i<n;i++) moveP(p,dt/n); p.age+=dt; });
    smoke=smoke.filter(p=>p.age<12 && p.y>28 && p.x>8 && p.x<266); if(smoke.length>500) smoke.splice(0,smoke.length-500);
    if(shake>0) shake=Math.max(0,shake-dt); }
  function smkLabel(){ $('smk').textContent=smokeOn?'💨 線香のけむり：オン':'💨 線香のけむり'; }
  $('start').addEventListener('click',start);
  $('fuel').addEventListener('change',start); $('gas').addEventListener('change',start);
  $('gap').addEventListener('change',()=>{ if(smokeOn) sen=senDefault(); });
  $('smk').addEventListener('click',()=>{ smokeOn=!smokeOn; if(smokeOn) sen=senDefault(); else smoke=[]; smkLabel(); });
  $('lime').addEventListener('click',()=>{ lw={v:clamp((comp[2]-0.15)/1.8,0,1)}; shake=1; });
  $('fast').addEventListener('click',()=>{ fast=!fast; $('fast').textContent=fast?'⏩ はやおくり：×4':'⏩ はやおくり'; });
  function pxy(e){ const p=cpos(cv,e); return [p[0]/dpr,p[1]/dpr]; }
  cv.addEventListener('pointerdown',(e)=>{ const q=pxy(e), x=q[0], y=q[1]; if(x>268) return;
    if(smokeOn && sen && Math.hypot(x-sen.x,y-sen.y)<28){ dragSen=true; try{ cv.setPointerCapture(e.pointerId); }catch(err){} e.preventDefault(); return; }
    if(Math.abs(x-BCX)<60 && y>46 && y<100){ $('lid').value=isLid()?'off':'on'; e.preventDefault(); return; }
    if(y>390 && y<448 && (Math.abs(x-BX0)<26 || Math.abs(x-BX1)<26)){ $('gap').value=isGap()?'no':'yes'; if(smokeOn) sen=senDefault(); e.preventDefault(); return; }
    if(!inside(x,y) && y>46){ smokeOn=true; smkLabel(); sen={x:clamp(x,40,262),y:clamp(y,50,426)}; dragSen=true; try{ cv.setPointerCapture(e.pointerId); }catch(err){} e.preventDefault(); } });
  cv.addEventListener('pointermove',(e)=>{ if(!dragSen) return; const q=pxy(e); if(!inside(q[0],q[1])) sen={x:clamp(q[0],40,262),y:clamp(q[1],50,426)}; e.preventDefault(); });
  ['pointerup','pointercancel'].forEach(n=>cv.addEventListener(n,()=>{ dragSen=false; }));
  cv.style.cursor='pointer';
  function loop(now){ const dt=Math.min(0.1,Math.max(0,(now-last)/1000)); last=now; upd(dt*(fast?4:1)); draw(); requestAnimationFrame(loop); }
  start(); draw(); requestAnimationFrame(loop);
'''.replace("@FF@", FF)

sim(slug="nenshou", cat="rika", emoji="🕯️", score=82,
    title="ものの燃え方と空気シミュレーター（集気びん・酸素と二酸化炭素）",
    title_tag="ものの燃え方と空気のシミュレーター｜集気びんのろうそく・酸素と二酸化炭素の割合（小6理科 燃焼の仕組み）",
    meta_desc="集気びんのふたや下のすき間を変えてろうそく・木を燃やすと、燃え続けるか消えるかと、酸素（約21%→約17%）・二酸化炭素（約0.04%→約3〜4%）の割合の変化が気体検知管の目盛りで分かる無料シミュレーター。線香のけむりで空気の流れ、石灰水の変化も。小6理科の授業向け。",
    og_title="ものの燃え方と空気シミュレーター（集気びん・酸素と二酸化炭素）",
    og_desc="集気びんのふた・すき間を変えてろうそくを燃やし、酸素21%→17%、二酸化炭素の増え方を気体検知管と石灰水で確かめる。小6の授業向け。",
    card_desc="集気びんのふたやすき間を変えてろうそくを燃やす。酸素21%→17%、二酸化炭素の増え方と石灰水を確かめる。",
    lead="集気びんの中でろうそく（または木）を燃やすと、空気の何が変わるのかを確かめられます。ふたや下のすき間を変えると燃え続けるか消えるかが変わり、線香のけむりで空気の流れが見えます。気体検知管の目盛りで酸素と二酸化炭素の割合を読み、石灰水の変化も調べられます。",
    model="小6 燃焼の仕組み（ものの燃え方と空気）",
    level="小学6年",
    unit="小学校 第6学年 A（1）燃焼の仕組み",
    canvas=canvas(640, 460, light=True),
    controls=select("lid", "びんの上（ふた）", [("on", "ふたをする"), ("off", "ふたをしない")])
           + select("gap", "びんの下", [("no", "すき間なし"), ("yes", "すき間あり")])
           + select("fuel", "燃やす物", [("candle", "ろうそく"), ("wood", "木（わりばし）")])
           + select("gas", "びんの中の気体", [("air", "空気"), ("o2", "酸素"), ("n2", "窒素"), ("co2", "二酸化炭素")]),
    buttons=btn("start", "🔥 火をつけて入れる（やり直し）", True) + btn("smk", "💨 線香のけむり") + btn("lime", "🧪 石灰水を入れてふる") + btn("fast", "⏩ はやおくり"),
    stats=stats([("sO", "酸素", True), ("sC", "二酸化炭素", True), ("sN", "窒素", False), ("sF", "火のようす", False), ("sT", "燃えた時間", False), ("sL", "石灰水", False)]),
    legend="左：集気びん（びんの口をタップするとふた、下をタップするとすき間を変えられます。びんの外をタップすると線香を置け、指で動かせます）。右上：気体検知管の目盛り（色の変わった部分の境目を読みます）。右中：空気の粒100こで表した成分（灰色＝窒素、赤＝酸素、青＝二酸化炭素、白＝その他）と、時間の変化のグラフ。右下：石灰水。",
    article=NENSHOU_ARTICLE,
    faqs=[("ろうそくの火が消えたとき、集気びんの中の酸素はなくなっていますか？", "なくなっていません。火が消えたときも、酸素は約17%残っています（燃やす前は約21%）。ろうそくの炎は、酸素の割合がある程度より少なくなると燃え続けられないため、酸素が残っていても火が消えます。"),
          ("ふたをしない集気びんで、下にすき間があるとよく燃えるのはなぜですか？", "炎であたためられた空気が上の口から出ていき、そのかわりに新しい空気（酸素をふくむ空気）が下のすき間から入ってくるからです。線香のけむりを近づけると、けむりがすき間から吸いこまれ、上の口から出ていく様子で確かめられます。"),
          ("石灰水が白くにごるのはなぜですか？", "石灰水に二酸化炭素がふれると、水に溶けにくい白い物（炭酸カルシウム）ができるからです。燃やす前の空気は二酸化炭素が約0.04%と少ないのでにごりませんが、ろうそくを燃やした後の空気（約3〜4%）では白くにごります。"),
          ("物が燃えたあと、窒素はどうなりますか？", "変わりません。窒素には物を燃やす働きがなく、燃えることに関係しないので、燃やす前も後も約78%のままです。びんの中を窒素だけにすると、火はすぐに消えます。"),
          ("燃やす前と後の空気の割合は、どのくらい変わりますか？", "気体検知管で調べると、酸素は約21%から約17%に減り、二酸化炭素は約0.04%から約3〜4%に増えます。窒素は約78%のままです。数値は集気びんの大きさや燃やす物によって少し変わります。"),
          ("酸素の中でろうそくを燃やすとどうなりますか？", "空気中よりも炎が大きく明るくなり、激しく燃えます。酸素には物を燃やす働きがあるからです。反対に、窒素や二酸化炭素の中では、火はすぐに消えます。")],
    rel=[("hito-karada", "🫀", "人の体のつくりと働き（呼吸）"), ("kagaku-shitsuryou", "🧪", "化学変化と質量シミュレーター"), ("youkaido", "🧂", "物の溶け方と溶解度シミュレーター"),
         ("diffusion", "🫧", "拡散シミュレーター"), ("joutai-henka", "🧊", "状態変化と粒子のシミュレーター")],
    js=JS_NENSHOU)
