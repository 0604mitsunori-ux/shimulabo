# -*- coding: utf-8 -*-
"""理科の授業向けシミュ：雲のでき方（2026-11-18）
   kumo-dekikata … 中2「気象とその変化（霧や雲の発生）」
   上昇気流で空気のかたまりが上がる→膨張→温度が下がる→露点で雲／山を越えるフェーン現象／ペットボトルで雲を作る実験。
   既存 shitsudo-roten（露点・飽和水蒸気量の計算）とは役割分担：こちらは「上がる→冷える→雲」の動きが主役。"""
from common import T, N, P, slider, select, btn, stats

MEXT_CHU = "https://www.mext.go.jp/a_menu/shotou/new-cs/1387016.htm"
JMA = "https://www.jma.go.jp/jma/kishou/know/yougo_hp/kumo.html"
def A(url, label): return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, label)

SIMS = []

STAGE = r'''
<style>
.kd-tabs{display:flex;gap:6px;flex-wrap:wrap;justify-content:center;width:100%;max-width:640px;}
.kd-tabs button{flex:1 1 150px;border:1.5px solid var(--line);background:#fff;border-radius:999px;padding:9px 10px;font:inherit;font-size:13.5px;font-weight:800;color:var(--ink-2);cursor:pointer;}
.kd-tabs button.on{background:#0e7490;border-color:#0e7490;color:#fff;}
</style>
<div class="kd-tabs" role="tablist">
  <button type="button" data-m="rise" class="on">① 上昇気流で雲ができる</button>
  <button type="button" data-m="foehn">② 山を越える（フェーン現象）</button>
  <button type="button" data-m="bottle">③ ペットボトルで雲を作る</button>
</div>
<canvas id="cv" class="lab" width="640" height="420" aria-label="空気のかたまりが上がって雲ができるようす（かたまりをドラッグで上下できます）"></canvas>
<canvas id="gr" class="lab light" width="640" height="240" aria-label="高さと温度のグラフ、飽和水蒸気量のグラフ"></canvas>
'''

ARTICLE = '''
<h2>このシミュレーションでわかること</h2>
<p>地面近くの空気のかたまりが上昇すると、まわりの気圧が低くなるので<b>膨張</b>し、<b>温度が下がります</b>（雲ができる前は100 m上がるごとに約1℃）。温度が<b>露点</b>まで下がると、ふくみきれなくなった水蒸気が小さな水滴（または氷の粒）になり、<b>雲</b>ができます。地上の気温と湿度を変えると、雲ができ始める高さ（雲底）が変わることを確かめられます。</p>
<p>単元：中学校 第2分野（4）気象とその変化「霧や雲の発生」（中学2年）。山を越えた風が暑く乾く<b>フェーン現象</b>と、ペットボトルで雲を作る実験もあわせて扱います。</p>

<h2>授業での使い方</h2>
<ul>
<li><b>導入</b>：③ペットボトルの実験を先に見せ、「ふたを開けた瞬間に白くくもるのはなぜ？」と問いかけます。実際の実験の前後に使うと、目に見えない水蒸気と水滴の変化を説明しやすくなります。</li>
<li><b>展開</b>：①で空気のかたまりを指で上げ下げし、気温・露点・飽和水蒸気量の変化をグラフで確かめます。湿度を上げ下げして、雲底の高さがどう変わるか予想させます。</li>
<li><b>まとめ・発展</b>：②で山を越える空気を動かし、風下のふもとが風上より暑く乾く理由を、雲ができる前後の温度の下がり方のちがいから説明させます。</li>
</ul>
<p>問いの例：</p>
<ol>
<li>湿度が高い日と低い日では、雲ができ始める高さはどちらが低いでしょう。</li>
<li>空気のかたまりは、上昇するとなぜ温度が下がるのでしょう。</li>
<li>山を越えた風が、風上より暑くなるのはなぜでしょう（雲の中で温度の下がり方が小さくなる理由も考えよう）。</li>
</ol>

<h2>しくみ・解説</h2>
<h3>上昇→膨張→温度が下がる→露点で雲</h3>
<p>上空ほど気圧は低いので、上昇した空気のかたまりは膨張します。膨張するとき、かたまりは自分のもつエネルギーを使って外の空気を押し広げるため、温度が下がります。これを<b>断熱膨張</b>といいます（高校で詳しく学びます）。雲ができる前の空気は、<b>100 m上がるごとに約1℃</b>下がります。</p>
<p>温度が下がると飽和水蒸気量が小さくなり、やがて空気にふくまれる水蒸気量と等しくなります。このときの温度が露点です。さらに上昇すると、ふくみきれない水蒸気が、空気中のちりなど（<b>凝結核</b>）を中心に水滴になります。これが雲の粒です。</p>
''' + T([["雲ができる前（乾いた空気）", "100 mで約1℃下がる", "膨張して温度が下がる"],
         ["雲ができてから（湿った空気）", "100 mで約0.5℃下がる", "水蒸気が水滴になるときに熱を出すので、下がり方が小さくなる"],
         ["下降するとき（雲がない）", "100 mで約1℃上がる", "圧縮されて温度が上がる"]],
        ["上昇・下降", "温度の変わり方（目安）", "理由"]) + '''
<h3>雲ができ始める高さ（雲底）の求め方</h3>
<p>上昇する空気は、膨張すると1 m³あたりの水蒸気量も少し減るので、露点も100 mで約0.2℃下がります。気温は100 mで1℃、露点は0.2℃下がるので、その差は100 mで0.8℃ずつ縮まります。そのため、</p>
''' + P("雲ができ始める高さ（m）≒ 125 ×（地上の気温 − 地上の露点）") + '''
<p>となります。たとえば気温25℃・湿度60%の空気（露点 約16℃）なら、125×(25−16.3)＝約1,100 mで雲ができ始めます。</p>
''' + N("教科書や問題集では「露点は変わらないものとする」として、雲底＝100×（気温−露点）m と計算することがあります。問題文の条件に合わせてください。このシミュレーターの数値は、露点も下がる 125×（気温−露点）で計算しています。") + '''
<h3>フェーン現象</h3>
<p>湿った空気が山の斜面を上がると、途中で雲ができ（雨や雪を降らせ）、そこから上は100 mで約0.5℃しか下がりません。山を越えて下りるときは雲が消えているので、100 mで約1℃ずつ上がります。そのため、風下のふもとでは、風上より<b>気温が高く、湿度が低い</b>風になります。日本では、春や夏に日本海側で気温が大きく上がる原因になることがあります。</p>
<h3>ペットボトルで雲を作る実験</h3>
<p>少量の水と線香の煙を入れたペットボトルに、空気を入れるポンプ（炭酸飲料用の加圧キャップなど）で空気を押しこみ、ふたを開けると、中の空気が一気に膨張して温度が下がり、白くくもります。線香の煙は凝結核のはたらきをするので、煙がないとくもりにくくなります。もう一度空気を押しこむと、温度が上がって白いくもりは消えます。</p>
''' + N("この図では、空気のかたまりの大きさや粒の数、ペットボトルの温度の下がり方を、わかりやすく誇張しています。温度の下がり方（1℃・0.5℃）は中学校で使われるおよその値で、実際の大気では気温や水蒸気の量によって変わります。飽和水蒸気量は理科年表などの値とほぼ同じになる式で計算しています（25℃で約23.1 g/m³）。") + '''
<h2>参考</h2>
<ul class="seo-refs">
<li>''' + A(MEXT_CHU, "文部科学省「中学校学習指導要領（平成29年告示）解説 理科編」") + ''' 第2分野（4）気象とその変化「霧や雲の発生」</li>
<li>''' + A(JMA, "気象庁「予報用語 雲」") + '''</li>
<li>中学校理科の教科書（2年）「気象とその変化」「雲のでき方」の章</li>
<li>国立天文台編『理科年表』飽和水蒸気量の表</li>
</ul>
'''

FAQS = [
    ("雲はなぜ上空でできるのですか？", "空気のかたまりが上昇すると、まわりの気圧が低いので膨張し、温度が下がります。温度が露点より低くなると、ふくみきれなくなった水蒸気がちりなどを中心に小さな水滴や氷の粒になり、それが集まって雲に見えます。"),
    ("空気が上昇すると、100 mでどれくらい温度が下がりますか？", "雲ができる前の空気は100 mで約1℃、雲ができてからは約0.5℃下がります。雲の中では、水蒸気が水滴になるときに熱を出すので、温度の下がり方が小さくなります。"),
    ("雲ができ始める高さはどうやって求めますか？", "気温が露点まで下がる高さを求めます。露点が変わらないとすると 100×（気温−露点）m、露点も100 mで約0.2℃下がることを考えると およそ125×（気温−露点）m です。問題文の条件に合わせて計算してください。"),
    ("フェーン現象とは何ですか？", "湿った空気が山を越えるとき、風上側の斜面で雲ができて雨を降らせ、風下側に下りるときに温度が大きく上がって、ふもとに暑く乾いた風が吹く現象です。雲の中では100 mで約0.5℃しか下がらないのに、下りるときは約1℃ずつ上がるために起こります。"),
    ("ペットボトルの実験で線香の煙を入れるのはなぜですか？", "煙の小さな粒が、水蒸気が水滴になるときの中心（凝結核）になるからです。煙がないと、温度が露点より下がっても水滴ができにくく、白いくもりがはっきり見えません。"),
    ("雲と霧のちがいは何ですか？", "どちらも小さな水滴などが空気中にうかんだものです。地面に接しているものを霧、上空にうかんでいるものを雲とよびます。霧は、夜に地面が冷えて地面近くの空気が露点以下になったときなどにできます。"),
]

JS = r'''
const cv=$('cv'), gr=$('gr');
function setup(c){ const dpr=Math.min(2,window.devicePixelRatio||1); const W=c.width,H=c.height; c.width=W*dpr; c.height=H*dpr; const x=c.getContext('2d'); x.setTransform(dpr,0,0,dpr,0,0); return {x:x,W:W,H:H,dpr:dpr}; }
const A1=setup(cv), A2=setup(gr), ctx=A1.x, W=A1.W, H=A1.H, g=A2.x, GW=A2.W, GH=A2.H, dpr=A1.dpr;
const FONT='"Hiragino Sans","Noto Sans JP","Yu Gothic",Meiryo,sans-serif';
function txt(c,s,x,y,sz,col,al,w){ c.font=(w||700)+' '+sz+'px '+FONT; c.fillStyle=col; c.textAlign=al||'left'; c.fillText(s,x,y); c.textAlign='left'; }
// 飽和水蒸気量 g/m3（25℃で約23.1）
function sat(t){ const es=6.1078*Math.pow(10,7.5*t/(t+237.3)); return 217*es/(t+273.15); }
function dew(t,rh){ const v=sat(t)*rh/100; let lo=-60,hi=t; for(let i=0;i<50;i++){ const m=(lo+hi)/2; if(sat(m)>v) hi=m; else lo=m; } return (lo+hi)/2; }
let mode='rise', s=0, playing=false, last=0, drag=false;
let T0=25, RH=60, MH=2000, smoke=true;
let Td0=16, base=1100;
const PN=46, PTS=[]; for(let i=0;i<PN;i++){ const a=Math.random()*6.283, r=Math.sqrt(Math.random()); PTS.push({a:a,r:r,ph:Math.random()*6.283}); }
let puffs=[];
// ボトル
let bp=1.0, bT=0, bCloud=0, bHist=[], openT=-1;
function recalc(){ T0=+$('t0').value; RH=+$('rh').value; MH=+$('mh').value; smoke=$('smoke').value==='1'; Td0=dew(T0,RH); base=125*(T0-Td0); puffs=[]; }
function topH(){ return mode==='rise' ? Math.round(Math.min(Math.max(base+1200,2200),5200)/100)*100 : MH; }
function scaleMax(){ return mode==='rise' ? Math.max(3000, Math.ceil((topH()+400)/1000)*1000) : Math.max(3000, Math.ceil((MH+700)/500)*500); }
// かたまりの温度・露点（上昇）
function upT(h){ return h<=base ? T0-h/100 : T0-base/100-(h-base)/200; }
function upTd(h){ return h<=base ? Td0-0.2*h/100 : upT(h); }
// フェーン：s(0..1) → 位置・高さ・温度
function foehnState(sv){
  let h, x, side;
  if(sv<0.1){ h=0; side=0; } else if(sv<0.5){ h=MH*(sv-0.1)/0.4; side=0; } else if(sv<0.9){ h=MH*(1-(sv-0.5)/0.4); side=1; } else { h=0; side=1; }
  if(side===0) return {h:h, side:0, T:upT(h), Td:upTd(h)};
  const Ttop=upT(MH), Tdtop=upTd(MH), dH=MH-h;
  return {h:h, side:1, T:Ttop+dH/100, Td:Tdtop+0.2*dH/100};
}
function state(){
  if(mode==='rise'){ const h=s*topH(); return {h:h, side:0, T:upT(h), Td:upTd(h)}; }
  return foehnState(s);
}
function water(st){ // 水蒸気と水滴（g/m3 の目安）
  const vap=Math.min(sat(st.Td), sat(st.T));
  const cloudy = st.side===0 && st.h>base;
  const drop = cloudy ? Math.max(0, sat(upT(base))-sat(st.T)) : 0;
  return {vap:vap, drop:drop, sat:sat(st.T), cloudy:cloudy};
}
// ---------- 描画：上昇・フェーン ----------
function yOfH(h){ return H-40-(h/scaleMax())*(H-80); }
function sky(){
  const gg=ctx.createLinearGradient(0,0,0,H); gg.addColorStop(0,'#1e3a8a'); gg.addColorStop(.55,'#3b82f6'); gg.addColorStop(1,'#bfdbfe'); ctx.fillStyle=gg; ctx.fillRect(0,0,W,H);
  // 高さの目もり
  const SM=scaleMax(), step=SM>4000?1000:500;
  for(let h=0;h<=SM;h+=step){ const y=yOfH(h); ctx.strokeStyle='rgba(255,255,255,.18)'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(44,y); ctx.lineTo(W,y); ctx.stroke(); txt(ctx,h+'m',38,y+4,11,'rgba(255,255,255,.85)','right'); }
}
function cloudBlob(cx,cy,w,hgt,alpha){ // cy＝雲の底（平ら）
  ctx.fillStyle='rgba(255,255,255,'+alpha+')'; ctx.beginPath();
  const n=Math.max(2,Math.ceil(w/(hgt*.9))), sp=w/n;
  for(let i=0;i<n;i++){ const px=cx-w/2+sp*(i+.5), r=hgt*(.62+.3*Math.abs(Math.sin(i*1.9+cx*.01))); ctx.moveTo(px+r,cy-r*.55); ctx.arc(px,cy-r*.55,r,0,6.283); }
  for(let i=0;i<n-1;i++){ const px=cx-w/2+sp*(i+1), r=hgt*(.7+.25*Math.abs(Math.cos(i*2.3))); ctx.moveTo(px+r,cy-hgt*.9); ctx.arc(px,cy-hgt*.9,r,0,6.283); }
  ctx.fill(); }
function parcel(px,py,st,t){
  const p=1013*Math.exp(-st.h/8400), V=(st.T+273.15)/288.15*1013/p, r=26*Math.pow(V,2.2);
  const wt=water(st), frac=wt.drop/(wt.drop+wt.vap+1e-9);
  ctx.save(); ctx.beginPath(); ctx.arc(px,py,r,0,6.283);
  const warm=clamp((st.T+10)/45,0,1); ctx.fillStyle='rgba('+Math.round(120+135*warm)+','+Math.round(160-40*warm)+','+Math.round(255-170*warm)+',.30)'; ctx.fill();
  ctx.strokeStyle='rgba(255,255,255,.9)'; ctx.lineWidth=2; ctx.setLineDash([5,4]); ctx.stroke(); ctx.setLineDash([]);
  const nd=Math.round(frac*PN);
  PTS.forEach((q,i)=>{ const a=q.a+Math.sin(t*1.3+q.ph)*.25, rr=q.r*(r-6); const x=px+Math.cos(a)*rr, y=py+Math.sin(a)*rr;
    if(i<nd){ ctx.fillStyle='#ffffff'; ctx.beginPath(); ctx.arc(x,y,3.6,0,6.283); ctx.fill(); ctx.strokeStyle='rgba(30,64,175,.5)'; ctx.lineWidth=1; ctx.stroke(); }
    else { ctx.fillStyle='rgba(186,230,253,.95)'; ctx.beginPath(); ctx.arc(x,y,1.7,0,6.283); ctx.fill(); } });
  ctx.restore();
  // 温度ラベル
  const lx=px+r+8>W-120?px-r-118:px+r+8;
  ctx.fillStyle='rgba(15,23,42,.72)'; ctx.beginPath(); ctx.roundRect?ctx.roundRect(lx,py-24,112,48,8):ctx.rect(lx,py-24,112,48); ctx.fill();
  txt(ctx,'気温 '+st.T.toFixed(1)+'℃',lx+8,py-6,13,'#fff','left',800); txt(ctx,'露点 '+st.Td.toFixed(1)+'℃',lx+8,py+14,12,'#bae6fd','left',700);
  return r;
}
function drawRise(t){
  sky(); const st=state(), yb=yOfH(base), px=W*.64, py=yOfH(st.h);
  // 地面
  ctx.fillStyle='#65a30d'; ctx.fillRect(0,H-40,W,40); ctx.fillStyle='#3f6212'; ctx.fillRect(0,H-40,W,4);
  txt(ctx,'☀️ 日光で地面があたたまり、空気が上昇する',W*.5,H-14,13,'#fff','center',800);
  // 上昇気流の矢印
  for(let k=0;k<3;k++){ const ax=W*(.12+.4*k), ay=H-60-((t*40+k*60)%160); if(k===1) continue; ctx.strokeStyle='rgba(255,255,255,.55)'; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(ax,ay+30); ctx.lineTo(ax,ay); ctx.lineTo(ax-7,ay+9); ctx.moveTo(ax,ay); ctx.lineTo(ax+7,ay+9); ctx.stroke(); }
  // 雲底の線
  if(base<scaleMax()){ ctx.save(); ctx.setLineDash([8,6]); ctx.strokeStyle='#fde68a'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(44,yb); ctx.lineTo(W,yb); ctx.stroke(); ctx.restore();
    txt(ctx,'露点に達する高さ＝雲ができ始める（約'+Math.round(base/10)*10+'m）',52,yb-7,12.5,'#fde68a','left',800); }
  // 雲（通り過ぎた分だけ育つ）
  if(st.h>base){ const top=yOfH(st.h), hh=yb-top, rows=Math.max(1,Math.ceil(hh/34)); for(let k=0;k<rows;k++){ const cy=yb-k*(hh/rows), w=Math.max(70,(110+hh*.7)*(1-k/(rows+2))); cloudBlob(px,cy,w,Math.min(30,12+hh/8),.9); } }
  parcel(px,py,st,t);
}
function mtnY(x){ // 山の形（x: 0..W）
  const cx=W*.5, half=W*.33; const d=Math.abs(x-cx)/half; return d>=1 ? 0 : MH*(Math.cos(d*Math.PI)+1)/2; }
function foehnX(sv){ return sv<0.1 ? W*(.04+.13*sv/0.1) : sv<0.9 ? W*(.17+.66*(sv-0.1)/0.8) : W*(.83+.13*(sv-0.9)/0.1); }
function drawFoehn(t){
  sky(); const st=state(), yb=yOfH(base);
  // 山
  ctx.fillStyle='#4d7c0f'; ctx.beginPath(); ctx.moveTo(0,H-40); for(let x=0;x<=W;x+=4) ctx.lineTo(x,yOfH(mtnY(x))); ctx.lineTo(W,H); ctx.lineTo(0,H); ctx.closePath(); ctx.fill();
  ctx.fillStyle='#65a30d'; ctx.fillRect(0,H-40,W,40);
  // 風上の雲と雨
  if(base<MH){ ctx.save(); ctx.setLineDash([8,6]); ctx.strokeStyle='#fde68a'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(44,yb); ctx.lineTo(W*.5,yb); ctx.stroke(); ctx.restore();
    txt(ctx,'雲ができ始める（約'+Math.round(base/10)*10+'m）',50,yb-7,12,'#fde68a','left',800);
    // 斜面にそって雲
    const x0=W*.17, xs=[]; for(let x=x0;x<=W*.5;x+=6){ if(mtnY(x)>=base) xs.push(x); }
    if(xs.length){ const xa=xs[0]; ctx.strokeStyle='rgba(255,255,255,.85)'; ctx.lineWidth=1.6;
      for(let k=0;k<26;k++){ const rx=xa+((k*37)%Math.max(10,(W*.5-xa))), ry0=yb+10, len=(t*160+k*29)%90; const gy=yOfH(mtnY(rx)); if(ry0+len<gy){ ctx.beginPath(); ctx.moveTo(rx,ry0+len); ctx.lineTo(rx-3,ry0+len+9); ctx.stroke(); } }
      const hc=Math.min(26,(yb-yOfH(MH))/3+10); for(let k=0;k<3;k++){ const yy=yb-(yb-yOfH(MH)+10)*k/3, wk=(W*.53-xa)*(1-k*.18)+40; cloudBlob(W*.53-wk/2+20, yy+4, wk, hc, .92); }
      txt(ctx,'☔ 雨が降る',xa+4,yb+44,12,'#fff','left',800); } }
  // 両側のふもとの表示
  const lee=foehnState(0.99), win=foehnState(0.01);
  const rhW=Math.min(100,sat(win.Td)/sat(win.T)*100), rhL=Math.min(100,sat(lee.Td)/sat(lee.T)*100);
  ctx.fillStyle='rgba(15,23,42,.65)'; ctx.fillRect(8,H-92,150,46); ctx.fillRect(W-158,H-92,150,46);
  txt(ctx,'風上 '+win.T.toFixed(1)+'℃・湿度'+Math.round(rhW)+'%',14,H-74,12,'#fff','left',800); txt(ctx,'しめった風',14,H-55,11,'#bae6fd');
  txt(ctx,'風下 '+lee.T.toFixed(1)+'℃・湿度'+Math.round(rhL)+'%',W-152,H-74,12,'#fff','left',800); txt(ctx,base<MH?'🔥 暑くかわいた風':'雲ができず変化なし',W-152,H-55,11,base<MH?'#fdba74':'#bae6fd');
  // 風の矢印
  txt(ctx,'風 →',W*.04,yOfH(MH)+20,15,'rgba(255,255,255,.9)','left',800);
  const px=foehnX(s), py=Math.min(yOfH(st.h), H-40)-28;
  const pr=parcel(px,py,st,t);
}
// ---------- 描画：ペットボトル ----------
function drawBottle(t){
  const gg=ctx.createLinearGradient(0,0,0,H); gg.addColorStop(0,'#f1f5f9'); gg.addColorStop(1,'#e2e8f0'); ctx.fillStyle=gg; ctx.fillRect(0,0,W,H);
  ctx.fillStyle='#cbd5e1'; ctx.fillRect(0,H-36,W,36);
  const bx=W*.36, bw=150, by=104, bh=272;
  // ボトル
  ctx.save(); ctx.beginPath(); ctx.moveTo(bx-22,by); ctx.lineTo(bx+22,by); ctx.lineTo(bx+22,by+30); ctx.quadraticCurveTo(bx+bw/2,by+50,bx+bw/2,by+95); ctx.lineTo(bx+bw/2,by+bh-12); ctx.quadraticCurveTo(bx+bw/2,by+bh,bx+bw/2-12,by+bh); ctx.lineTo(bx-bw/2+12,by+bh); ctx.quadraticCurveTo(bx-bw/2,by+bh,bx-bw/2,by+bh-12); ctx.lineTo(bx-bw/2,by+95); ctx.quadraticCurveTo(bx-bw/2,by+50,bx-22,by+30); ctx.closePath();
  ctx.fillStyle='rgba(224,242,254,.55)'; ctx.fill(); ctx.clip();
  // 水
  ctx.fillStyle='rgba(56,189,248,.55)'; ctx.fillRect(bx-bw/2,by+bh-26,bw,26);
  // 煙（あり）
  if(smoke){ for(let k=0;k<30;k++){ const x=bx-bw/2+((k*53)%bw), y=by+60+((k*97+t*8)%(bh-90)); ctx.fillStyle='rgba(148,163,184,.25)'; ctx.beginPath(); ctx.arc(x,y,2,0,6.283); ctx.fill(); } }
  // 白いくもり
  if(bCloud>0.01){ for(let k=0;k<70;k++){ const fr=v=>v-Math.floor(v), x=bx-bw/2+fr(Math.sin(k*12.9898)*43758.5)*bw+Math.sin(t+k)*4, y=by+40+fr(Math.sin(k*78.233)*12345.6)*(bh-70); ctx.fillStyle='rgba(255,255,255,'+(.55*bCloud)+')'; ctx.beginPath(); ctx.arc(x,y,9+(k%5)*3,0,6.283); ctx.fill(); } }
  ctx.restore();
  ctx.strokeStyle='#64748b'; ctx.lineWidth=2.5; ctx.beginPath(); ctx.moveTo(bx-22,by); ctx.lineTo(bx-22,by+30); ctx.quadraticCurveTo(bx-bw/2,by+50,bx-bw/2,by+95); ctx.lineTo(bx-bw/2,by+bh-12); ctx.quadraticCurveTo(bx-bw/2,by+bh,bx-bw/2+12,by+bh); ctx.lineTo(bx+bw/2-12,by+bh); ctx.quadraticCurveTo(bx+bw/2,by+bh,bx+bw/2,by+bh-12); ctx.lineTo(bx+bw/2,by+95); ctx.quadraticCurveTo(bx+bw/2,by+50,bx+22,by+30); ctx.lineTo(bx+22,by); ctx.stroke();
  // ふた（ポンプ付き）
  const opened=openT>=0, fresh=opened && t-openT<1.2;
  ctx.fillStyle='#ef4444'; ctx.fillRect(bx-26, by-28-(opened?24:0), 52, 28);
  if(!opened){ ctx.fillStyle='#475569'; ctx.fillRect(bx-6,by-70,12,42); ctx.fillStyle='#334155'; ctx.fillRect(bx-24,by-76,48,10); txt(ctx,'ポンプ',bx+30,by-62,12,'#334155','left',800); }
  else { for(let k=0;k<6;k++){ const a=-1.57+(k-2.5)*.35, rr=20+((t-openT)*120)%50; ctx.strokeStyle='rgba(100,116,139,.6)'; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(bx+Math.cos(a)*rr,by-30+Math.sin(a)*rr); ctx.lineTo(bx+Math.cos(a)*(rr+12),by-30+Math.sin(a)*(rr+12)); if(fresh) ctx.stroke(); } if(fresh) txt(ctx,'プシュッ！',bx+34,by-40,15,'#0f172a','left',900); else txt(ctx,'ふたを開けた',bx+34,by-40,12,'#475569','left',800); }
  // 気圧計
  const gx=W*.72, gy=130; ctx.fillStyle='#fff'; ctx.beginPath(); ctx.arc(gx,gy,58,0,6.283); ctx.fill(); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=3; ctx.stroke();
  for(let k=0;k<=10;k++){ const a=Math.PI*.75+k/10*Math.PI*1.5; ctx.strokeStyle='#64748b'; ctx.lineWidth=k%5?1:2.5; ctx.beginPath(); ctx.moveTo(gx+Math.cos(a)*48,gy+Math.sin(a)*48); ctx.lineTo(gx+Math.cos(a)*56,gy+Math.sin(a)*56); ctx.stroke(); }
  const na=Math.PI*.75+clamp((bp-1)/1,0,1)*Math.PI*1.5; ctx.strokeStyle='#dc2626'; ctx.lineWidth=3; ctx.beginPath(); ctx.moveTo(gx,gy); ctx.lineTo(gx+Math.cos(na)*44,gy+Math.sin(na)*44); ctx.stroke();
  txt(ctx,'びんの中の気圧',gx,gy+98,12,'#334155','center',800); txt(ctx,bp.toFixed(2)+' 気圧',gx,gy+80,16,'#0f172a','center',900); txt(ctx,'1',gx-44,gy+46,11,'#64748b','center'); txt(ctx,'2',gx+44,gy+46,11,'#64748b','center');
  // 温度計
  const tx=W*.72, ty0=250, th=120, tc=T0+bT; ctx.fillStyle='#fff'; ctx.fillRect(tx-70,ty0,140,th+44); ctx.strokeStyle='#cbd5e1'; ctx.strokeRect(tx-70,ty0,140,th+44);
  txt(ctx,'びんの中の温度',tx,ty0+18,13,'#334155','center',800); txt(ctx,tc.toFixed(1)+'℃',tx,ty0+46,22,bT<-0.5?'#2563eb':bT>0.5?'#dc2626':'#0f172a','center',900);
  txt(ctx,bT>=0?'+'+bT.toFixed(1)+'℃':bT.toFixed(1)+'℃',tx,ty0+70,13,'#64748b','center',700);
  txt(ctx,bCloud>.3?'☁️ 白くくもった！':bCloud>.05?'うっすらくもる':'くもりなし',tx,ty0+100,14,bCloud>.3?'#0e7490':'#64748b','center',800);
  txt(ctx,smoke?'線香の煙：あり（凝結核）':'線香の煙：なし',bx,H-12,12,'#334155','center',700);
}
// ---------- グラフ ----------
function drawGraph(){
  g.clearRect(0,0,GW,GH); g.fillStyle='#fff'; g.fillRect(0,0,GW,GH);
  const L={x0:48,x1:GW*.58,y0:GH-34,y1:18}, R={x0:GW*.66,x1:GW-14,y0:GH-34,y1:18};
  if(mode!=='bottle'){
    const SM=mode==='rise'?topH():MH, st=state();
    const tmin=Math.floor(Math.min(upT(SM),upTd(SM),Td0)/5)*5-5, tmax=Math.ceil((mode==='foehn'?Math.max(T0,foehnState(.99).T):T0)/5)*5+5;
    const X=t=>L.x0+(t-tmin)/(tmax-tmin)*(L.x1-L.x0), Y=h=>L.y0-(h/SM)*(L.y0-L.y1);
    g.strokeStyle='#e2e8f0'; g.lineWidth=1; for(let t=tmin;t<=tmax;t+=5){ g.beginPath(); g.moveTo(X(t),L.y0); g.lineTo(X(t),L.y1); g.stroke(); txt(g,t+'',X(t),L.y0+14,10,'#64748b','center',600); }
    const hs=SM>2500?1000:500; for(let h=0;h<=SM+1;h+=hs){ g.beginPath(); g.moveTo(L.x0,Y(h)); g.lineTo(L.x1,Y(h)); g.stroke(); txt(g,Math.round(h)+'',L.x0-4,Y(h)+4,10,'#64748b','right',600); }
    txt(g,'高さ(m)',L.x0-4,12,10.5,'#334155','right',800); txt(g,'温度(℃)',L.x1,L.y0+28,10.5,'#334155','right',800);
    // 線
    function line(fn,col,dash){ g.save(); g.strokeStyle=col; g.lineWidth=2.5; if(dash) g.setLineDash(dash); g.beginPath(); for(let i=0;i<=60;i++){ const h=SM*i/60, v=fn(h); i?g.lineTo(X(v),Y(h)):g.moveTo(X(v),Y(h)); } g.stroke(); g.restore(); }
    line(upT,'#dc2626'); line(upTd,'#2563eb',[6,4]);
    if(mode==='foehn' && base<MH){ g.save(); g.strokeStyle='#f97316'; g.lineWidth=2.5; g.beginPath(); for(let i=0;i<=40;i++){ const sv=.5+.4*i/40, f=foehnState(sv); i?g.lineTo(X(f.T),Y(f.h)):g.moveTo(X(f.T),Y(f.h)); } g.stroke(); g.restore(); }
    if(base<SM){ g.save(); g.setLineDash([3,3]); g.strokeStyle='#ca8a04'; g.beginPath(); g.moveTo(L.x0,Y(base)); g.lineTo(L.x1,Y(base)); g.stroke(); g.restore(); txt(g,'雲底',L.x1-2,Y(base)-4,10.5,'#a16207','right',800); }
    g.fillStyle='#0f172a'; g.beginPath(); g.arc(X(st.T),Y(st.h),5,0,6.283); g.fill();
    txt(g,'━ 気温',L.x0+6,L.y1+8,10.5,'#dc2626','left',800); txt(g,'┅ 露点',L.x0+56,L.y1+8,10.5,'#2563eb','left',800); if(mode==='foehn') txt(g,'━ 下りる',L.x0+106,L.y1+8,10.5,'#f97316','left',800);
    satPanel(R, st.T, water(st).vap, water(st).drop);
  } else {
    // 温度の記録
    const tmin=T0-12, tmax=T0+6, n=bHist.length, X=i=>L.x0+i/150*(L.x1-L.x0), Y=v=>L.y0-(v-tmin)/(tmax-tmin)*(L.y0-L.y1);
    g.strokeStyle='#e2e8f0'; for(let v=Math.ceil(tmin/2)*2;v<=tmax;v+=2){ g.beginPath(); g.moveTo(L.x0,Y(v)); g.lineTo(L.x1,Y(v)); g.stroke(); txt(g,v+'',L.x0-4,Y(v)+4,10,'#64748b','right',600); }
    txt(g,'びんの中の温度(℃) の変化',L.x0,12,11,'#334155','left',800); txt(g,'時間 →',L.x1,L.y0+16,10.5,'#64748b','right',700);
    g.strokeStyle='#dc2626'; g.lineWidth=2.5; g.beginPath(); bHist.forEach((v,i)=>{ i?g.lineTo(X(i),Y(v)):g.moveTo(X(i),Y(v)); }); g.stroke();
    const vap=sat(T0); satPanel(R, T0+bT, Math.min(vap,sat(T0+bT)), Math.max(0,vap-sat(T0+bT))*(smoke?1:.25));
  }
}
function satPanel(R,t,vap,drop){
  const tmin=-10,tmax=40,amax=55, X=v=>R.x0+(v-tmin)/(tmax-tmin)*(R.x1-R.x0), Y=a=>R.y0-a/amax*(R.y0-R.y1);
  g.strokeStyle='#e2e8f0'; g.lineWidth=1; [0,20,40].forEach(v=>{ txt(g,v+'',X(v),R.y0+14,10,'#64748b','center',600); }); [0,25,50].forEach(a=>{ g.beginPath(); g.moveTo(R.x0,Y(a)); g.lineTo(R.x1,Y(a)); g.stroke(); txt(g,a+'',R.x0-4,Y(a)+4,10,'#64748b','right',600); });
  txt(g,'飽和水蒸気量(g/m³)',R.x0-4,12,10.5,'#334155','left',800);
  g.strokeStyle='#0e7490'; g.lineWidth=2.5; g.beginPath(); for(let v=tmin;v<=tmax;v+=1){ v===tmin?g.moveTo(X(v),Y(sat(v))):g.lineTo(X(v),Y(sat(v))); } g.stroke();
  const tc=clamp(t,tmin,tmax); g.fillStyle='#2563eb'; g.beginPath(); g.arc(X(tc),Y(vap),5,0,6.283); g.fill();
  if(drop>0.05){ g.strokeStyle='#94a3b8'; g.lineWidth=2; g.setLineDash([3,3]); g.beginPath(); g.moveTo(X(tc),Y(vap)); g.lineTo(X(tc),Y(vap+drop)); g.stroke(); g.setLineDash([]); g.fillStyle='#fff'; g.strokeStyle='#64748b'; g.beginPath(); g.arc(X(tc),Y(vap+drop),5,0,6.283); g.fill(); g.stroke();
    txt(g,'○ 水滴に',X(tc)+8,Y(vap+drop)+4,10.5,'#475569','left',800); }
  txt(g,'● 水蒸気',R.x0+4,R.y1+10,10.5,'#2563eb','left',800);
}
// ---------- 統計 ----------
function setK(id,k){ const el=$(id); if(el&&el.parentNode){ const kk=el.parentNode.querySelector('.k'); if(kk) kk.textContent=k; } }
function updStats(){
  if(mode==='bottle'){
    setK('sTd','びんの中の気圧'); setK('sBase','温度の変化'); setK('sH','白いくもり'); setK('sT','びんの中の温度'); setK('sW','水滴になった水（目安）'); setK('sLee','線香の煙');
    $('sTd').textContent=bp.toFixed(2)+' 気圧'; $('sBase').textContent=(bT>=0?'+':'')+bT.toFixed(1)+'℃'; $('sH').textContent=bCloud>.3?'くもった':bCloud>.05?'うっすら':'なし';
    $('sT').textContent=(T0+bT).toFixed(1)+'℃'; $('sW').textContent=(Math.max(0,sat(T0)-sat(T0+bT))*(smoke?1:.25)).toFixed(1)+' g/m³'; $('sLee').textContent=smoke?'あり':'なし';
    return;
  }
  const st=state(), wt=water(st);
  setK('sTd','地上の露点'); setK('sBase','雲ができ始める高さ'); setK('sH','かたまりの高さ'); setK('sT','かたまりの気温'); setK('sW','水滴になった水（目安）'); setK('sLee', mode==='foehn'?'風下のふもと':'飽和水蒸気量');
  $('sTd').textContent=Td0.toFixed(1)+'℃'; $('sBase').textContent='約'+(Math.round(base/10)*10).toLocaleString()+' m'; $('sH').textContent=Math.round(st.h).toLocaleString()+' m';
  $('sT').textContent=st.T.toFixed(1)+'℃'; $('sW').textContent=wt.drop.toFixed(1)+' g/m³';
  if(mode==='foehn'){ const lee=foehnState(.99); $('sLee').textContent=lee.T.toFixed(1)+'℃・'+Math.round(Math.min(100,sat(lee.Td)/sat(lee.T)*100))+'%'; }
  else $('sLee').textContent=wt.sat.toFixed(1)+' g/m³';
}
function share(){
  if(mode==='foehn'){ const lee=foehnState(.99); setShare('【フェーン現象】気温'+T0+'℃・湿度'+RH+'%の風が高さ'+MH+'mの山を越えると、風下のふもとは'+lee.T.toFixed(1)+'℃に'+(base<MH?'（雲ができて雨を降らせたぶん暑く乾く）':'')+'｜シミュラボ'); }
  else if(mode==='bottle') setShare('【ペットボトルで雲を作る】空気を押しこんでふたを開けると、膨張して温度が下がり白くくもる｜シミュラボ');
  else setShare('【雲のでき方】気温'+T0+'℃・湿度'+RH+'%の空気は、露点'+Td0.toFixed(1)+'℃。約'+(Math.round(base/10)*10).toLocaleString()+'mまで上がると雲ができる｜シミュラボ');
}
// ---------- 操作 ----------
function setMode(m){ mode=m; s=0; playing=false; puffs=[]; bp=1; bT=0; bCloud=0; bHist=[]; openT=-1;
  document.querySelectorAll('.kd-tabs button').forEach(b=>b.classList.toggle('on',b.dataset.m===m));
  const show=(id,on)=>{ const el=$(id).closest('.field'); if(el) el.style.display=on?'':'none'; };
  show('mh',m==='foehn'); show('smoke',m==='bottle'); show('rh',m!=='bottle');
  $('b1').textContent = m==='bottle' ? 'ポンプで空気を押しこむ' : '▶ 空気を動かす';
  $('b2').textContent = m==='bottle' ? 'ふたを開ける' : '⟲ 地上にもどす';
  updStats(); share(); }
document.querySelectorAll('.kd-tabs button').forEach(b=>b.addEventListener('click',()=>setMode(b.dataset.m)));
['t0','rh','mh','smoke'].forEach(id=>{ $(id).addEventListener('input',()=>{ recalc(); updStats(); share(); }); $(id).addEventListener('change',()=>{ recalc(); updStats(); share(); }); });
$('b1').addEventListener('click',()=>{
  if(mode==='bottle'){ if(bp<1.95){ bp=Math.min(2,bp+0.1); bT+=0.6; bCloud=Math.max(0,bCloud-.45); openT=-1; } return; }
  if(playing){ playing=false; $('b1').textContent='▶ 空気を動かす'; return; }
  if(s>=1) s=0; playing=true; $('b1').textContent='■ 止める';
});
$('b2').addEventListener('click',()=>{
  if(mode==='bottle'){ if(openT>=0 && performance.now()/1000-openT<1.2) return; const dT=(T0+273.15)*(1-Math.pow(1/bp,0.286))*0.16; bT-=dT; bp=1; openT=performance.now()/1000;
    const cool=-Math.min(0,bT); bCloud=smoke?clamp(cool/3,0,1):clamp(cool/14,0,.25); return; }
  playing=false; s=0; $('b1').textContent='▶ 空気を動かす';
});
cv.addEventListener('pointerdown',e=>{ if(mode==='bottle') return; drag=true; playing=false; $('b1').textContent='▶ 空気を動かす'; moveTo(e); cv.setPointerCapture(e.pointerId); });
cv.addEventListener('pointermove',e=>{ if(drag) moveTo(e); });
cv.addEventListener('pointerup',()=>{ drag=false; }); cv.addEventListener('pointercancel',()=>{ drag=false; });
function moveTo(e){ const p=cpos(cv,e), x=p.x/dpr, y=p.y/dpr;
  if(mode==='rise'){ const h=(H-40-y)/(H-80)*scaleMax(); s=clamp(h/topH(),0,1); }
  else { const fx=x/W; s=fx<.17?clamp((fx-.04)/.13*.1,0,.1):fx<.83?.1+(fx-.17)/.66*.8:clamp(.9+(fx-.83)/.13*.1,.9,1); }
  updStats(); }
function loop(now){
  const t=now/1000, dt=Math.min(.05,(now-last)/1000||0); last=now;
  if(playing && mode!=='bottle'){ s+=dt/(mode==='rise'?9:12); if(s>=1){ s=1; playing=false; $('b1').textContent='▶ もう一度'; } updStats(); }
  if(mode==='bottle'){ // 室温にもどっていく
    const opened=openT>=0; if(opened && t-openT>1.2){ bT+=(0-bT)*dt*.25; bCloud=Math.max(0,bCloud-dt*.06); }
    else if(!opened && bT>0){ bT+=(0-bT)*dt*.05; }
    if(!bHist.length || (t*10|0)!==(bHist.tt||0)){ bHist.push(T0+bT); if(bHist.length>150) bHist.shift(); bHist.tt=t*10|0; }
    updStats(); }
  if(mode==='rise') drawRise(t); else if(mode==='foehn') drawFoehn(t); else drawBottle(t);
  drawGraph();
  requestAnimationFrame(loop);
}
recalc(); setMode('rise'); s=0.62; updStats(); share(); requestAnimationFrame(loop);
window.__kd={sat:sat,dew:dew,get base(){return base;},get Td0(){return Td0;},foehnState:foehnState,setMode:setMode,setS:function(v){s=v;updStats();},openBottle:function(){$('b2').click();},pump:function(){$('b1').click();}};
'''

SIMS.append(dict(
    slug="kumo-dekikata", cat="rika", emoji="☁️", score=80,
    title="雲のでき方シミュレーター（上昇気流・断熱膨張・露点・フェーン現象・ペットボトル実験）",
    title_tag="雲のでき方シミュレーター｜空気が上昇→膨張→温度が下がる→露点で雲。雲ができる高さ・フェーン現象・ペットボトル実験（中2理科）",
    meta_desc="空気のかたまりを指で上げ下げすると、膨張して100mで約1℃ずつ温度が下がり、露点に達した高さで雲ができるようすを、気温・露点・飽和水蒸気量のグラフといっしょに確かめられるシミュレーター。地上の気温と湿度で雲ができ始める高さが変わる。山を越えるフェーン現象、ペットボトルで雲を作る実験つき。中学2年「霧や雲の発生」向け。",
    og_title="雲のでき方シミュレーター｜上昇→膨張→温度が下がる→露点で雲",
    og_desc="空気のかたまりを持ち上げると、膨らんで冷え、露点の高さで中の水蒸気が水滴に変わって雲になる。湿度を変えると雲ができる高さが変わる。山を越えると風下は暑く乾く（フェーン現象）。",
    card_desc="空気のかたまりを持ち上げると膨らんで冷え、露点の高さで雲に。フェーン現象とペットボトル実験つき。",
    lead="「① 上昇気流」では、空気のかたまりを指でドラッグして上げ下げできます。上がるほど膨らんで温度が下がり、露点に達した高さ（黄色の線）から中の水蒸気（水色の点）が水滴（白い粒）に変わって雲ができます。地上の気温と湿度を変えると、雲ができ始める高さが変わります。「② 山を越える」ではフェーン現象を、「③ ペットボトル」では、空気を押しこんでふたを開けると白くくもる実験を再現できます。",
    model="中2 気象とその変化（霧や雲の発生）",
    level="中学2年",
    unit="中学校 第2分野（4）気象とその変化 ア（ｲ）天気の変化「霧や雲の発生」",
    canvas=STAGE,
    controls='<div class="lab-ctl">' + slider("t0", "地上の気温", 5, 35, 25, 1, "{v}℃") + slider("rh", "地上の湿度", 30, 95, 60, 1, "{v}%")
             + slider("mh", "山の高さ", 500, 3000, 2000, 100, "{v} m")
             + select("smoke", "線香の煙（凝結核）", [("1", "入れる"), ("0", "入れない")]) + '</div>',
    buttons=btn("b1", "▶ 空気を動かす", True) + btn("b2", "⟲ 地上にもどす"),
    stats=stats([("sTd", "地上の露点", False), ("sBase", "雲ができ始める高さ", True), ("sH", "かたまりの高さ", False),
                 ("sT", "かたまりの気温", False), ("sW", "水滴になった水（目安）", False), ("sLee", "飽和水蒸気量", False)]),
    legend="かたまりの中の水色の点＝水蒸気（実際は目に見えません）、白い粒＝水滴（雲の粒）。かたまりの大きさと粒の数は誇張しています。グラフの赤＝かたまりの気温、青の点線＝露点、オレンジ＝山を下りるとき。",
    article=ARTICLE, faqs=FAQS,
    rel=[("shitsudo-roten", "☁️", "露点・飽和水蒸気量のシミュレーター"), ("zensen-tenki", "🌦️", "寒冷前線・温暖前線のシミュレーター"),
         ("tenki-kion", "🌤️", "天気と1日の気温のシミュレーター"), ("kiatsu-jet", "🎢", "気圧ジェットコースター指数"), ("amagumo-now", "🌧️", "いまの雨雲マップ")],
    js=JS))
