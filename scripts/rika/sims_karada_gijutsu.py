# -*- coding: utf-8 -*-
"""理科の授業向け：人の体（小6 人の体のつくりと働き／中2 動物の体のつくりと働き）・技術（中学 技術C 動力伝達の機構）"""
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

MEXT_SHO = "https://www.mext.go.jp/a_menu/shotou/new-cs/1387014.htm"
MEXT_CHU = "https://www.mext.go.jp/a_menu/shotou/new-cs/1387016.htm"
KYOIKU_SHOKA = "https://www.kyoiku-shuppan.co.jp/docs/pages/rika/6_jintai/shoka/shoka1.html"
JSME_CROSS = "https://www.jsme.or.jp/jsme-medwiki/doku.php?id=16:1003435"

# ---- 記事の数値（Python で計算して埋め込む）
HR0, SV0 = 70, 70                     # 安静時のおとなの目安
HR1, SV1 = 130, 100                   # 運動中（ジョギングくらい）の目安
Q0, Q1 = HR0 * SV0, HR1 * SV1         # mL/分
BR0, TV0, BR1, TV1 = 15, 500, 30, 1500
V0, V1 = BR0 * TV0, BR1 * TV1         # mL/分
def _c(n): return "{:,}".format(int(round(n)))

# ============================================================ 1 人の体のつくりと働き
KARADA_ARTICLE = "<h2>このシミュレーションでわかること</h2>\n" + P(
    "血液は、心臓の働きで体の中をめぐり、酸素・養分・二酸化炭素などを運んでいます。心臓から肺へ行ってもどる流れを<b>肺循環</b>、"
    "心臓から全身へ行ってもどる流れを<b>体循環</b>といいます。肺から心臓にもどる血液には酸素が多く、全身から心臓にもどる血液には二酸化炭素が多くふくまれます。") + '''
<p>小学校6年の理科「人の体のつくりと働き」（学習指導要領 第6学年 B（1））と、中学校2年の理科「動物の体のつくりと働き」（第2分野（3）ア（ｳ）の「生命を維持する働き」）で学ぶ内容です。小学校の学習指導要領解説（理科編 p.86）には、人や動物の体のつくりや働きを調べるときに「映像や模型，図書，コンピュータシミュレーションなどを活用」することが書かれています。</p>
<p>画面は3つです。<b>①血液の循環</b>では、心拍数と1回に送り出す血液の量から、心臓が1分間に送り出す血液の量を計算します。<b>②呼吸</b>では、肺の中の肺胞で酸素と二酸化炭素が入れかわるようすを、<b>③消化と吸収</b>では、食べ物が口から小腸へ進むあいだに消化され、柔毛から吸収されるようすを見られます。「ことば」で、小6向けと中2向けの言い方を切りかえられます（例：「酸素が多い血液」⇔「動脈血」、「だ液」⇔「アミラーゼ」）。</p>
<h2>授業での使い方</h2>
<ul>
<li><b>導入</b>：自分の脈拍を15秒数えて4倍し、1分間の脈拍を求めます。①の画面で心拍数を同じ値にして、「心臓が1回ちぢむと、手首の脈が1回ふれる」ことを確かめます。</li>
<li><b>展開</b>：①で血液の色が変わる場所（肺と全身の毛細血管）に注目させ、酸素と二酸化炭素がどこで入れかわるかを考えます。②は気体検知管で吸う空気とはいた空気を調べる実験の前後に、③はだ液でデンプンの変化を調べる実験（ヨウ素液）の前後に使えます。心臓の部屋・血管・臓器をタップすると、名前と働きが表示されます。</li>
<li><b>まとめ</b>：3つの画面を行き来して、呼吸・消化・血液の循環・排出に関わる臓器が、たがいに関わり合って生命を維持していることを整理します。画面のアドレスの最後に <code>#kokyu</code>（呼吸）や <code>#shoka</code>（消化と吸収）を付けると、その画面から始まります。</li>
</ul>
<p>児童・生徒への問いの例：</p>
<ol>
<li>肺から心臓にもどる血液と、全身から心臓にもどる血液では、何がちがうでしょう。（中2：肺動脈と肺静脈には、それぞれ動脈血・静脈血のどちらが流れているでしょう。）</li>
<li>運動すると脈拍が増えるのはなぜでしょう。「1分間に送り出す血液の量」を使って説明しましょう。</li>
<li>ごはんをよくかんでいると甘く感じるのはなぜでしょう。だ液は、でんぷんにどんな変化を起こすでしょう。</li>
</ol>
<h2>しくみ・解説</h2>
<h3>血液の循環（肺循環と体循環）</h3>
<p>心臓は筋肉でできたポンプで、中は4つの部屋（右心房・右心室・左心房・左心室）に分かれています。図は体の正面から見た向きなので、<b>図の左側が体の右側</b>です。</p>
''' + T([["右心房", "大静脈（全身から）", "静脈血（二酸化炭素が多い）"], ["右心室", "肺動脈（肺へ）", "静脈血"],
          ["左心房", "肺静脈（肺から）", "動脈血（酸素が多い）"], ["左心室", "大動脈（全身へ）", "動脈血"]],
         ["心臓の部屋", "つながる血管", "流れる血液"]) + '''
<ul>
<li><b>肺循環</b>：右心室 → 肺動脈 → 肺の毛細血管（二酸化炭素を出し、酸素を受けとる）→ 肺静脈 → 左心房</li>
<li><b>体循環</b>：左心室 → 大動脈 → 全身の毛細血管（酸素や養分をわたし、二酸化炭素などを受けとる）→ 大静脈 → 右心房</li>
</ul>
''' + N("血管の名前は「心臓から出ていく血管＝動脈」「心臓にもどる血管＝静脈」で決まり、血液の名前は「酸素が多い＝動脈血」「二酸化炭素が多い＝静脈血」で決まります。そのため、<b>肺動脈には静脈血、肺静脈には動脈血</b>が流れています。") + '''
<p>心臓の部屋の出口や静脈には<b>弁</b>があり、血液が逆にもどらないようにしています。全身に血液を送り出す左心室は、かべの筋肉がいちばん厚くなっています。</p>
<h3>1分間に送り出す血液の量の計算</h3>
''' + N("1分間に送り出す血液の量 ＝ 心拍数（1分間）× 1回に送り出す量<br>例：%d回 × %dmL ＝ %smL ≒ 約%.1fL" % (HR0, SV0, _c(Q0), Q0 / 1000)) + '''
<p>1日では %.1fL × 60 × 24 ＝ 約%sL（200Lのドラム缶 約%d本分）になります。1日の拍動の回数は %d × 60 × 24 ＝ 約%s回です。おとなの体の血液は約5L（体重の約13分の1）なので、安静時は約1分で、体の血液と同じくらいの量が心臓から送り出されている計算になります。</p>
''' % (Q0 / 1000, _c(Q0 * 1440 / 1000), int(Q0 * 1440 / 1000 / 200), HR0, _c(HR0 * 1440)) + T(
    [["安静にしているとき（おとなの目安）", "約%d回" % HR0, "約%dmL" % SV0, "約%.1fL" % (Q0 / 1000)],
     ["運動中（ジョギングくらいの目安）", "約%d回" % HR1, "約%dmL" % SV1, "約%dL" % (Q1 / 1000)]],
    ["体のようす", "心拍数（1分間）", "1回に送り出す量", "1分間に送り出す量"]) + '''
<p>運動すると、筋肉がたくさんの酸素と養分を使うので、心拍数も1回に送り出す量も増え、1分間に送り出す血液の量は数倍になります。子どもは体が小さいぶん1回に送り出す量が少なく、心拍数はおとなより多めです。これらの数値は目安で、年齢・体格・体調によって変わります。<b>このシミュレーションは学習用で、医療的な判断に使うものではありません。</b>自分の脈拍の目安は<a href="../myakuhaku-heikin/">脈拍・心拍数 平均チェック</a>でも確かめられます。</p>
<h3>呼吸（肺胞での気体の交換）</h3>
''' + T([["酸素", "約21%", "約17%"], ["二酸化炭素", "約0.04%", "約4%"]], ["気体（体積の割合）", "吸う空気", "はいた空気"]) + '''
<p>残りはおもにちっ素（約78%）で、ほとんど変わりません。肺の中には、気管支の先に<b>肺胞</b>という小さなふくろが数億個あり、まわりを毛細血管がとりまいています。肺胞の中の空気から酸素が血液にとけこみ、血液中の二酸化炭素が肺胞の中に出されます。肺胞がたくさんあることで、空気にふれる表面積が大きくなり、気体の交換が効率よく行われます。肺には筋肉がないので、中学校では<b>横隔膜</b>やろっ骨の間の筋肉の動きで肺がふくらんだりちぢんだりすることも学びます。</p>
''' + N("1分間に出入りする空気の量 ＝ 呼吸数 × 1回の呼吸の量 ＝ %d回 × %dmL ＝ %.1fL<br>取り入れる酸素の量（目安）＝ %.1fL × （21%% − 17%%）＝ 約%dmL" % (BR0, TV0, V0 / 1000, V0 / 1000, V0 * 0.04)) + '''
<p>安静時のおとなの呼吸数は1分間に12〜20回ほど、1回の呼吸で出入りする空気は約500mLが目安です。運動中は呼吸数も1回の量も増え、%d回 × %smL なら1分間に%dLになります。取り入れられた酸素は、血液によって全身の細胞に運ばれ、養分からエネルギーを取り出すのに使われます。</p>
''' % (BR1, _c(TV1), V1 / 1000) + '''
<h3>消化と吸収（消化酵素の働き）</h3>
<p>食べ物は、口 → 食道 → 胃 → 小腸 → 大腸 → こう門（肛門）と進みます。この1本の管を消化管といいます。消化液にふくまれる<b>消化酵素</b>が、養分を小さな物に分解して、小腸から吸収されやすくします。</p>
''' + T([["だ液", "だ液せん", "アミラーゼ", "デンプン → 麦芽糖など"],
          ["胃液", "胃", "ペプシン", "タンパク質 → 小さく分解"],
          ["胆汁", "肝臓（胆のうにためる）", "ふくまない", "脂肪を細かい粒にして、分解を助ける"],
          ["すい液", "すい臓", "アミラーゼ", "デンプン → 麦芽糖など"],
          ["すい液", "すい臓", "トリプシン", "タンパク質 → さらに小さく分解"],
          ["すい液", "すい臓", "リパーゼ", "脂肪 → 脂肪酸とモノグリセリド"],
          ["小腸の壁の消化酵素", "小腸", "いくつかの消化酵素", "麦芽糖など → ブドウ糖／分解されたタンパク質 → アミノ酸"]],
         ["消化液", "出すところ", "消化酵素", "分解するもの → できるもの"]) + '''
<ul>
<li><b>ブドウ糖とアミノ酸</b>：小腸の柔毛（じゅう毛）の<b>毛細血管</b>に入り、肝臓を通って全身へ運ばれます。</li>
<li><b>脂肪酸とモノグリセリド</b>：柔毛に吸収されたあと再び脂肪になり、<b>リンパ管</b>に入って、やがて血液に合流します。</li>
<li>水分はおもに小腸で吸収され、大腸でも吸収されます。吸収されなかった物は、便としてこう門から出されます。</li>
</ul>
<p>小6の言葉の画面では、消化酵素の名前は出さずに「だ液」「胃液」などの消化液で表し、でんぷんからできる物を「糖」と表しています。だ液の実験では、ヨウ素液はでんぷんがあると青むらさき色になります。だ液を入れて体温くらい（約40℃）にあたためたでんぷんの液では、ヨウ素液を加えても色が変わらず、でんぷんが別の物に変わったことがわかります。小腸の内側にはたくさんのひだがあり、その表面は柔毛という小さな出っぱりでおおわれているので、養分を吸収する表面積がとても大きくなっています（小腸の長さは、のばすと約6m）。</p>
<h3>このシミュレーションで単純にしていること</h3>
<ul>
<li>心臓と血管は模式図です。肺の毛細血管はまとめて1つの箱で、全身の毛細血管は「脳・うで」「小腸 → 肝臓」「腎臓」「あし」の4つの通り道で表しています。</li>
<li>見やすくするため、酸素が多い血液を赤、二酸化炭素が多い血液を青で表しています。実際の静脈血は暗い赤色です。</li>
<li>心臓が打つ速さ（心拍数）は実際と同じですが、血液が流れる速さは見やすいように速くしています（実際は約1分で体をひとめぐりします）。</li>
<li>③の消化と吸収は、場所ごとにかかる時間を実際より大きく縮めています。実際には、胃に2〜4時間ほどとどまり、食べてから便になって出るまでには24〜72時間ほどかかるといわれ、個人差が大きいです。「吸収された養分」の％は、このモデルの中での目安です。</li>
<li>数値はおとなの目安です。医療的な判断には使えません。</li>
</ul>
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「小学校学習指導要領（平成29年告示）解説 理科編」第6学年 B（1）人の体のつくりと働き（pp.85〜86）（<a href="''' + MEXT_SHO + '''" target="_blank" rel="noopener">文部科学省 小学校学習指導要領解説のページ</a>）</li>
<li>文部科学省「中学校学習指導要領（平成29年告示）解説 理科編」第2分野（3）ア（ｳ）動物の体のつくりと働き（pp.89〜90）（<a href="''' + MEXT_CHU + '''" target="_blank" rel="noopener">文部科学省 中学校学習指導要領解説のページ</a>）</li>
<li>小学校理科の教科書（東京書籍「新しい理科」、啓林館「わくわく理科」、大日本図書「たのしい理科」など）6年「人の体のつくりと働き」</li>
<li>中学校理科の教科書（東京書籍「新しい科学」、啓林館「未来へひろがるサイエンス」、大日本図書「理科の世界」など）2年「動物の体のつくりと働き」</li>
<li>教育出版 小学校理科のウェブ資料「消化の仕組み」（<a href="''' + KYOIKU_SHOKA + '''" target="_blank" rel="noopener">教育出版のページ</a>）</li>
</ul>
'''

KARADA_FAQS = [
    ("肺循環と体循環のちがいは何ですか？", "肺循環は、右心室 → 肺動脈 → 肺 → 肺静脈 → 左心房 と流れ、肺で二酸化炭素を出して酸素を受けとる流れです。体循環は、左心室 → 大動脈 → 全身 → 大静脈 → 右心房 と流れ、全身の細胞に酸素や養分をわたし、二酸化炭素などを受けとる流れです。"),
    ("動脈血と静脈血のちがいは何ですか？ 肺動脈に流れているのはどちらですか？", "動脈血は酸素を多くふくむ血液（あざやかな赤色）、静脈血は二酸化炭素を多くふくむ血液（暗い赤色）です。肺動脈は心臓から肺へ向かう血管なので「動脈」ですが、全身からもどった静脈血が流れています。反対に、肺静脈には動脈血が流れています。"),
    ("心臓は1分間にどれくらいの血液を送り出していますか？", "安静にしているおとなでは、心拍数が1分間に約70回、1回に送り出す量が約70mLなので、70×70＝4,900mLで、約5Lです。運動するとどちらも増え、1分間に十数Lになることもあります。数値は目安で、年齢や体格によって変わります。"),
    ("消化酵素にはどんなものがありますか？", "だ液のアミラーゼ（デンプン → 麦芽糖など）、胃液のペプシン（タンパク質を分解）、すい液のアミラーゼ・トリプシン・リパーゼ（リパーゼは脂肪 → 脂肪酸とモノグリセリド）、小腸の壁の消化酵素（→ ブドウ糖・アミノ酸）などがあります。胆汁は消化酵素をふくみませんが、脂肪を細かい粒にして消化を助けます。"),
    ("吸う空気とはいた空気では、何がちがいますか？", "体積の割合で、酸素は吸う空気で約21%、はいた空気で約17%に減り、二酸化炭素は吸う空気で約0.04%、はいた空気で約4%に増えます。肺の肺胞で、酸素が血液に取り入れられ、二酸化炭素が出されるためです。"),
    ("小腸の柔毛（じゅう毛）には、どんな働きがありますか？", "小腸の内側のひだをおおう小さな出っぱりで、養分にふれる表面積を大きくして、効率よく吸収します。ブドウ糖とアミノ酸は柔毛の毛細血管に入って肝臓へ運ばれ、脂肪酸とモノグリセリドは柔毛の中で再び脂肪になってリンパ管に入ります。"),
]

KARADA_JS = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const h1=document.querySelector('.sim-head h1'); if(h1&&!h1.children.length){ const t=h1.textContent, i=t.indexOf('（'); if(i>0){ h1.textContent=t.slice(0,i); const sp=document.createElement('span'); sp.style.display='inline-block'; sp.textContent=t.slice(i); h1.appendChild(sp); } }
  const RED=[220,38,38], BLUE=[37,99,235];
  const mixc=(a,b,f)=>'rgb('+Math.round(a[0]+(b[0]-a[0])*f)+','+Math.round(a[1]+(b[1]-a[1])*f)+','+Math.round(a[2]+(b[2]-a[2])*f)+')';
  const sm=(v)=>{ v=clamp(v,0,1); return v*v*(3-2*v); };
  const lerp=(a,b,f)=>a+(b-a)*f;
  const bump=(p,a,b)=>(p>=a&&p<=b)?Math.sin(Math.PI*(p-a)/(b-a)):0;
  const S6=()=>$('lv').value==='s6';
  const tx=(a,b)=>(S6()?a:b);
  const fld=(id)=>$(id).closest('.field');
  let mode='J', run=true, T=0, cph=0, rph=0, beatN=0, beatT=-9, pulses=[], info=null, dragTL=false, dp=0, lastKey='';
  const bar=document.createElement('div'); bar.className='lab-btns'; bar.style.marginTop='0';
  ['tJ','tK','tS'].forEach((id)=>{ const b=$(id); if(b) bar.appendChild(b); });
  cv.parentNode.insertBefore(bar,cv);
  cv.parentNode.style.gridTemplateColumns='minmax(0,1fr)';
  function setK(id,s){ const e=$(id); if(e&&e.previousElementSibling) e.previousElementSibling.textContent=s; }
  function setV(id,s){ const e=$(id); if(!e) return; e.textContent=s; e.style.fontSize=s.length>10?'14px':(s.length>7?'16px':''); }
  // ---------- 描画の道具
  function rrect(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
  function txt(t,x,y,size,col,weight,align,maxW,halo){ ctx.textAlign=align||'left'; let s=size; ctx.font=(weight||'')+' '+s+'px sans-serif';
    if(maxW){ while(ctx.measureText(t).width>maxW&&s>8){ s-=0.5; ctx.font=(weight||'')+' '+s+'px sans-serif'; } }
    if(halo){ ctx.lineWidth=3.5; ctx.strokeStyle='rgba(255,255,255,.92)'; ctx.lineJoin='round'; ctx.strokeText(t,x,y); }
    ctx.fillStyle=col||'#0f172a'; ctx.fillText(t,x,y); }
  function dot(x,y,r,c){ ctx.fillStyle=c; ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.fill(); }
  function poly(pts,w,c,dash){ ctx.strokeStyle=c; ctx.lineWidth=w; ctx.lineJoin='round'; ctx.lineCap='round'; if(dash) ctx.setLineDash(dash); ctx.beginPath(); pts.forEach((p,i)=>{ if(i) ctx.lineTo(p[0],p[1]); else ctx.moveTo(p[0],p[1]); }); ctx.stroke(); if(dash) ctx.setLineDash([]); }
  function panel(x,y,w,h){ ctx.fillStyle='rgba(255,255,255,.95)'; rrect(x,y,w,h,10); ctx.fill(); ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; ctx.stroke(); }
  function mkPath(pts){ const cum=[0]; for(let i=1;i<pts.length;i++) cum.push(cum[i-1]+Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1])); return {pts:pts,cum:cum,len:cum[cum.length-1]}; }
  function at(P,d){ d=clamp(d,0,P.len); let lo=0,hi=P.cum.length-1; while(hi-lo>1){ const m=(lo+hi)>>1; if(P.cum[m]<=d) lo=m; else hi=m; }
    const sg=(P.cum[hi]-P.cum[lo])||1, f=(d-P.cum[lo])/sg, a=P.pts[lo], b=P.pts[hi]; return [a[0]+(b[0]-a[0])*f, a[1]+(b[1]-a[1])*f]; }
  function bez(p0,p1,p2,p3,n){ const o=[]; for(let i=0;i<=n;i++){ const t=i/n,u=1-t; o.push([u*u*u*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t*t*t*p3[0], u*u*u*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t*t*t*p3[1]]); } return o; }
  function arcPts(c,r,a0,a1,n){ const o=[]; for(let i=0;i<=n;i++){ const a=(a0+(a1-a0)*i/n)*Math.PI/180; o.push([c[0]+r*Math.cos(a), c[1]+r*Math.sin(a)]); } return o; }
  function inR(x,y,a,b,c,d){ return x>=a&&x<=c&&y>=b&&y<=d; }
  function nearPts(pts,x,y,r){ for(const p of pts){ if(Math.hypot(p[0]-x,p[1]-y)<r) return true; } return false; }
  function wrapLines(t,maxW){ const out=[]; let cur=''; for(const ch of t){ if(ctx.measureText(cur+ch).width>maxW&&cur){ out.push(cur); cur=ch; } else cur+=ch; } if(cur) out.push(cur); return out; }
  function bubble(){ if(!info) return; ctx.font='12.5px sans-serif'; const lines=wrapLines(info.t,250); let w=0; lines.forEach((l)=>{ w=Math.max(w,ctx.measureText(l).width); }); w+=18; const h=lines.length*18+12;
    const x=clamp(info.x-w/2,6,W-w-6); let y=info.y-h-14; if(y<6) y=Math.min(H-h-6,info.y+16);
    ctx.globalAlpha=Math.min(1,info.life*2); ctx.fillStyle='rgba(15,23,42,.93)'; rrect(x,y,w,h,8); ctx.fill(); lines.forEach((l,i)=>txt(l,x+9,y+20+i*18,12.5,'#fff','','left')); ctx.globalAlpha=1; }

  // ================= ① 血液の循環
  const RA=[230,132,70,58], RV=[230,194,88,68], LA=[340,132,70,58], LV=[322,194,88,68];
  const EN=[309,98], EX=[331,98], LANES=[300,328,356,384], LW=[0.3,0.25,0.2,0.25];
  const LOOPS=[[60,30],[140,52],[220,72],[300,94]].map((q)=>bez(EN,[EN[0]-q[0],EN[1]-q[1]],[EX[0]+q[0],EX[1]-q[1]],EX,32));
  const H1=LOOPS.map((lp)=>{ const a=[[230,160],[262,160],[264,198],[278,232],[309,236],[309,194],[309,120]]; const pts=a.concat(lp); const i0=a.length, i1=pts.length-1;
    const P=mkPath(pts.concat([[331,108],[392,122],[392,136],[392,160],[380,198],[364,232],[410,236]])); P.o0=P.cum[i0]; P.o1=P.cum[i1]; return P; });
  const H2=LANES.map((y)=>{ const pts=[[410,236],[544,236],[544,y],[506,y]]; const c0=pts.length; for(let x=496;x>=316;x-=4) pts.push([x,y+3+3.5*Math.sin((496-x)/6)]); const c1=pts.length-1;
    pts.push([300,y+6],[136,y+6],[96,y+6],[96,160],[230,160]); const P=mkPath(pts); P.c0=P.cum[c0]; P.c1=P.cum[c1]; P.cm=(P.c0+P.c1)/2; P.e1=P.cum[c0+12]; P.e2=P.cum[c0+34]; P.cap=pts.slice(c0,c1+1); return P; });
  function pickLane(){ let r=Math.random(), j=0; while(j<3&&r>LW[j]){ r-=LW[j]; j++; } return j; }
  const parts=[]; for(let i=0;i<100;i++){ const h=Math.random()<0.45?0:1, k=h?pickLane():(Math.random()*4|0), PP=h?H2[k]:H1[k]; parts.push({h:h,k:k,d:Math.random()*PP.len,nut:Math.random()<0.2,ws:Math.random()<0.3}); }
  function oxy(p){ const P=p.h?H2[p.k]:H1[p.k]; if(!p.h){ if(p.d<=P.o0) return 0; if(p.d>=P.o1) return 1; return sm((p.d-P.o0)/(P.o1-P.o0)*1.7); }
    if(p.d<=P.c0) return 1; if(p.d>=P.c1) return 0; return 1-sm((p.d-P.c0)/(P.c1-P.c0)*1.5); }
  function stepJ(dt){ const hr=+$('hr').value, sv=+$('sv').value, Q=hr*sv/1000, ph=cph%1;
    const v=210*(Q/4.9)*(0.55+1.1*bump(ph,0.15,0.5))/0.795;
    for(const p of parts){ const P=p.h?H2[p.k]:H1[p.k]; const d0=p.d; p.d+=v*dt; const cr=(e)=>d0<e&&p.d>=e;
      if(p.h){ if(p.k===0||p.k===3){ if(cr(P.cm)){ p.nut=false; if(Math.random()<0.7) p.ws=true; } }
        else if(p.k===1){ if(cr(P.e1)) p.nut=true; if(cr(P.e2)&&p.nut&&Math.random()<0.35) p.nut=false; }
        else if(cr(P.cm)) p.ws=false; }
      if(p.d>=P.len){ p.d-=P.len; p.h=1-p.h; p.k=p.h?pickLane():(Math.random()*4|0); const P2=p.h?H2[p.k]:H1[p.k]; if(p.d>P2.len) p.d=0; } } }
  function chamber(r,s,f,st,lw){ const cx=r[0]+r[2]/2, cy=r[1]+r[3]/2, w=r[2]*s, h=r[3]*s; rrect(cx-w/2,cy-h/2,w,h,11); ctx.fillStyle=f; ctx.fill(); ctx.strokeStyle=st; ctx.lineWidth=lw; ctx.stroke(); }
  function valve(x,y,a,o){ ctx.save(); ctx.translate(x,y); ctx.rotate(a); ctx.strokeStyle='#9a3412'; ctx.lineWidth=2.2; ctx.lineCap='round'; const h=7;
    ctx.beginPath(); ctx.moveTo(0,-h); ctx.lineTo(lerp(3,9,o),lerp(0,-h+1,o)); ctx.moveTo(0,h); ctx.lineTo(lerp(3,9,o),lerp(0,h-1,o)); ctx.stroke(); ctx.restore(); }
  function drawJ(){ const s6=S6(), hr=+$('hr').value, sv=+$('sv').value, Q=hr*sv, ph=cph%1;
    const aS=1-0.07*bump(ph,0,0.13), vS=1-0.08*bump(ph,0.15,0.5);
    const VEN='#93c5fd', VENi='#eff6ff', ART='#fca5a5', ARTi='#fef2f2';
    // 肺
    ctx.fillStyle='#fdf2f8'; rrect(196,6,248,96,34); ctx.fill(); ctx.strokeStyle='#f9a8d4'; ctx.lineWidth=2; ctx.stroke();
    ctx.fillStyle='rgba(244,114,182,.10)'; ctx.beginPath(); ctx.ellipse(262,56,58,42,0,0,Math.PI*2); ctx.fill(); ctx.beginPath(); ctx.ellipse(378,56,58,42,0,0,Math.PI*2); ctx.fill();
    poly([[320,0],[320,20]],8,'#cbd5e1');
    LOOPS.forEach((lp)=>poly(lp,1.4,'rgba(219,39,119,.32)'));
    txt(tx('肺','肺（毛細血管）'),210,28,13,'#be185d','bold','left',0,true);
    // 全身（毛細血管の通り道）
    const LC=['#f8fafc','#fefce8','#f5f3ff','#f8fafc'];
    poly([[96,160],[96,392]],13,VEN); poly([[96,160],[96,392]],8,VENi);
    poly([[544,236],[544,392]],13,ART); poly([[544,236],[544,392]],8,ARTi);
    LANES.forEach((y,j)=>{ ctx.fillStyle=LC[j]; rrect(128,y-13,384,26,8); ctx.fill(); ctx.strokeStyle='#e2e8f0'; ctx.lineWidth=1; ctx.stroke();
      if(j===1){ ctx.fillStyle='#fef3c7'; rrect(410,y-12,94,24,6); ctx.fill(); ctx.fillStyle='#ffedd5'; rrect(318,y-12,90,24,6); ctx.fill();
        txt('小腸',457,y-3,9.5,'#a16207','bold','center'); txt(tx('かん臓','肝臓'),363,y-3,9.5,'#9a3412','bold','center'); }
      if(j===2){ ctx.fillStyle='#ede9fe'; rrect(318,y-12,186,24,6); ctx.fill(); }
      poly(H2[j].cap,1.3,'rgba(219,39,119,.45)');
      poly([[544,y],[506,y]],7,ART); poly([[136,y+6],[96,y+6]],7,VEN);
      const nm=['脳・うで など',tx('小腸 → かん臓','小腸 → 肝臓'),tx('じん臓','腎臓'),'あし など'][j];
      const an=['',' 養分を受けとる',tx(' 不要な物をこし出す（→にょう）',' 尿素などをこし出す（→尿）'),''][j];
      txt(nm,136,y-1,11.5,'#334155','bold'); if(an){ ctx.font='bold 11.5px sans-serif'; const w=ctx.measureText(nm).width; txt(an,136+w,y-1,10.5,'#64748b','','left',176-w); } });
    // 心臓
    ctx.fillStyle='#ffe4e6'; rrect(222,124,196,146,30); ctx.fill(); ctx.strokeStyle='#fb7185'; ctx.lineWidth=2; ctx.stroke();
    chamber(RA,aS,'#dbeafe','#60a5fa',2); chamber(RV,vS,'#dbeafe','#60a5fa',2.5); chamber(LA,aS,'#fee2e2','#f87171',2); chamber(LV,vS,'#fee2e2','#ef4444',4.5);
    // 血管
    poly([[230,160],[96,160]],13,VEN); poly([[230,160],[96,160]],8,VENi);
    poly([[410,236],[544,236]],13,ART); poly([[410,236],[544,236]],8,ARTi);
    poly([[309,198],[309,98]],13,VEN); poly([[309,198],[309,98]],8,VENi);
    poly([[331,98],[331,108],[392,122],[392,136]],13,ART); poly([[331,98],[331,108],[392,122],[392,136]],8,ARTi);
    if(!s6){ const av=1-sm(bump(ph,0.12,0.52)*1.6), sl=sm(bump(ph,0.17,0.48)*1.6);
      valve(264,195,Math.PI/2,av); valve(380,195,Math.PI/2,av); valve(309,196,-Math.PI/2,sl); valve(413,236,0,sl); txt('弁',248,200,10,'#9a3412','bold','right',0,true); }
    // 血液の粒
    for(const p of parts){ const P=p.h?H2[p.k]:H1[p.k]; const q=at(P,p.d); dot(q[0],q[1],3.4,mixc(BLUE,RED,oxy(p))); if(p.nut) dot(q[0]+3,q[1]-3,1.9,'#eab308'); if(p.ws) dot(q[0]-3,q[1]-3,1.9,'#6b7280'); }
    // 部屋の名前
    if(s6){ txt('全身から',265,144,10.5,'#1e3a8a','bold','center',0,true); txt('もどる',265,155,10.5,'#1e3a8a','bold','center',0,true);
      txt('肺へ',268,250,10.5,'#1e3a8a','bold','center',0,true); txt('送り出す',268,261,10.5,'#1e3a8a','bold','center',0,true);
      txt('肺から',345,150,10.5,'#991b1b','bold','left',0,true); txt('もどる',345,162,10.5,'#991b1b','bold','left',0,true);
      txt('全身へ',362,250,10.5,'#991b1b','bold','center',0,true); txt('送り出す',362,261,10.5,'#991b1b','bold','center',0,true); }
    else { txt('右心房',265,152,12,'#1e3a8a','bold','center',0,true); txt('右心室',266,256,12,'#1e3a8a','bold','center',0,true);
      txt('左心房',344,152,12,'#991b1b','bold','left',0,true); txt('左心室',360,256,12,'#991b1b','bold','center',0,true); }
    txt(tx('全身から','大静脈'),106,234,12,'#1d4ed8','bold','left',0,true);
    txt(tx('全身へ','大動脈'),538,272,12,'#b91c1c','bold','right',0,true);
    txt(tx('肺へ','肺動脈'),302,118,12,'#1d4ed8','bold','right',0,true);
    txt(tx('肺から','肺静脈'),400,120,12,'#b91c1c','bold','left',0,true);
    txt('体の正面から見た図（図の左が体の右）',320,281,10,'#64748b','','center');
    if(T-beatT<0.4){ ctx.globalAlpha=1-(T-beatT)/0.4; txt('ドクン',426,176,17,'#e11d48','bold','left'); ctx.globalAlpha=1; }
    // 左上：色の説明
    panel(6,6,186,102);
    dot(18,22,5,mixc(BLUE,RED,1)); txt(tx('酸素が多い血液','動脈血（酸素が多い）'),28,26,11.5,'#0f172a','bold','left',160);
    dot(18,41,5,mixc(BLUE,RED,0)); txt(tx('二酸化炭素が多い血液','静脈血（二酸化炭素が多い）'),28,45,11.5,'#0f172a','bold','left',160);
    txt(tx('肺をめぐる：心臓→肺→心臓','肺循環：心臓→肺→心臓'),14,65,11,'#334155','','left',172);
    txt(tx('全身をめぐる：心臓→全身→心臓','体循環：心臓→全身→心臓'),14,82,11,'#334155','','left',172);
    dot(19,96,3,'#eab308'); txt('養分',26,100,10.5,'#475569'); dot(64,96,3,'#6b7280'); txt('不要な物（二酸化炭素以外）',71,100,10.5,'#475569','','left',116);
    // 右上：1分間の量
    panel(450,6,184,102);
    txt(tx('1分間に心臓が送り出す血液','1分間に送り出す血液の量'),542,24,11.5,'#475569','bold','center',172);
    txt((Q/1000).toFixed(1)+' L',542,58,30,'#b91c1c','bold','center');
    txt(hr+'回 × '+sv+'mL ＝ '+num(Q)+'mL',542,79,12,'#334155','','center',172);
    txt('1日で 約'+num(Q*1.44)+' L（目安）',542,98,11,'#64748b','','center',172);
    // 手首の脈
    panel(552,124,82,90); txt(tx('手首の脈','手首の脈拍'),593,140,11,'#475569','bold','center');
    ctx.strokeStyle='#e11d48'; ctx.lineWidth=1.7; ctx.beginPath();
    for(let x=558;x<=628;x++){ const tt=T-(628-x)/70*2.4; let v=0; for(const pt of pulses){ const u=tt-pt; if(u>=0&&u<0.42) v+=Math.sin(Math.PI*u/0.42)*Math.exp(-2.2*u); } const y=192-v*30; if(x===558) ctx.moveTo(x,y); else ctx.lineTo(x,y); }
    ctx.stroke(); txt(tx('心臓1回＝脈1回','拍動1回＝脈拍1回'),593,208,9.5,'#64748b','','center',78); }
  function hitJ(x,y){
    if(inR(x,y,230,132,300,190)) return tx('右心房：全身からもどってきた、二酸化炭素が多い血液が入る部屋','右心房：大静脈から、全身をめぐってきた静脈血が入る部屋');
    if(inR(x,y,230,194,318,262)) return tx('右心室：血液を肺へ送り出す部屋','右心室：静脈血を肺動脈へ送り出す部屋（肺循環のはじまり）');
    if(inR(x,y,340,132,410,190)) return tx('左心房：肺で酸素を受けとった血液が入る部屋','左心房：肺静脈から、肺で酸素を受けとった動脈血が入る部屋');
    if(inR(x,y,322,194,410,262)) return tx('左心室：血液を全身へ送り出す部屋。かべの筋肉がいちばん厚い','左心室：動脈血を大動脈へ送り出す部屋（体循環のはじまり）。全身へ送るので、かべの筋肉がいちばん厚い');
    if(inR(x,y,300,98,318,132)) return tx('心臓から肺へ向かう血管。二酸化炭素が多い血液が流れる','肺動脈：右心室から肺へ向かう血管。名前は「動脈」でも、静脈血が流れる');
    if(nearPts([[331,100],[350,112],[370,117],[392,122],[392,134]],x,y,12)) return tx('肺から心臓へもどる血管。酸素が多い血液が流れる','肺静脈：肺から左心房へもどる血管。名前は「静脈」でも、動脈血が流れる');
    if(inR(x,y,410,228,552,244)||inR(x,y,536,236,552,392)) return tx('心臓から全身へ向かう太い血管。酸素が多い血液が流れる','大動脈：左心室から全身へ向かう太い血管。動脈血が流れる。動脈のかべは厚く、弾力がある');
    if(inR(x,y,88,152,230,168)||inR(x,y,88,160,104,392)) return tx('全身から心臓へもどる太い血管。二酸化炭素が多い血液が流れる','大静脈：全身から右心房へもどる太い血管。静脈血が流れる。静脈には逆流を防ぐ弁がある');
    if(inR(x,y,196,6,444,102)) return tx('肺の毛細血管：血液が二酸化炭素を出し、酸素を受けとる（②呼吸の画面でくわしく見られます）','肺の毛細血管：肺胞で二酸化炭素を出し、酸素を受けとる。静脈血が動脈血に変わる（②呼吸）');
    for(let j=0;j<4;j++){ const y0=LANES[j]; if(inR(x,y,128,y0-13,512,y0+13)){
      if(j===1) return tx('小腸で吸収した養分を受けとり、かん臓へ運ぶ。かん臓は養分の一部をたくわえる','小腸の毛細血管で吸収した養分（ブドウ糖・アミノ酸）を肝臓へ運ぶ。肝臓は養分をたくわえ、有害な物を無害な物に変える');
      if(j===2) return tx('じん臓：血液の中の不要な物をこし出して、にょうをつくる','腎臓：血液から尿素などの不要な物をこし出して尿をつくる（尿はぼうこうにためられる）');
      return tx('体のすみずみの毛細血管：細胞に酸素と養分をわたし、二酸化炭素などの不要な物を受けとる','全身の毛細血管：血しょうがしみ出て組織液になり、細胞に酸素や養分をわたし、二酸化炭素などを受けとる'); } }
    return null; }

  // ================= ② 呼吸
  const AC=[470,172], AR0=66, CRd=AR0+13;
  const CAPA=arcPts(AC,CRd,168,12,40), CAP=mkPath([[318,206]].concat(CAPA,[[630,206]])), CAP0=CAP.cum[1], CAP1=CAP.cum[CAPA.length];
  const BRP=mkPath([[372,40],[386,66],[404,86],[424,101],[438,114]]);
  const AWL=mkPath([[150,0],[150,104],[118,128],[104,150]]), AWR=mkPath([[150,0],[150,104],[182,128],[196,150]]);
  const o2=[], co2=[], rbc=[], air=[];
  for(let i=0;i<16;i++){ const a=rnd(0,Math.PI*2), r=rnd(0,AR0-12); o2.push({st:'air',x:AC[0]+r*Math.cos(a),y:AC[1]+r*Math.sin(a),vx:rnd(-20,20),vy:rnd(-20,20),t:0,s:0,fx:0,fy:0,gx:0,gy:0}); }
  for(let i=0;i<12;i++){ const m={st:'wait',w:rnd(0,3),x:0,y:0,vx:0,vy:0,t:0,s:0,sx:0,fx:0,fy:0,gx:0,gy:0}; if(i<5){ const a=rnd(0,Math.PI*2), r=rnd(0,AR0-14); m.st='air'; m.x=AC[0]+r*Math.cos(a); m.y=AC[1]+r*Math.sin(a); } co2.push(m); }
  for(let i=0;i<9;i++) rbc.push({s:i*CAP.len/9});
  for(let i=0;i<16;i++) air.push({sd:i%2,s:rnd(0,AWL.len),k:i});
  function breath(){ const p=rph%1; return p<0.4?{b:0.5-0.5*Math.cos(Math.PI*p/0.4),inh:true}:{b:0.5+0.5*Math.cos(Math.PI*(p-0.4)/0.6),inh:false}; }
  function ampK(){ return Math.min(1.8,Math.sqrt(+$('tv').value/500)); }
  function curR(){ return AR0*(1+0.05*breath().b*ampK()); }
  function walk(m,dt,R){ m.vx+=randn()*90*dt; m.vy+=randn()*90*dt; const sp=Math.hypot(m.vx,m.vy); if(sp>45){ m.vx*=45/sp; m.vy*=45/sp; }
    m.x+=m.vx*dt; m.y+=m.vy*dt; const dx=m.x-AC[0], dy=m.y-AC[1], d=Math.hypot(dx,dy)||1;
    if(d>R-6){ const k=(R-6)/d; m.x=AC[0]+dx*k; m.y=AC[1]+dy*k; const nx=dx/d, ny=dy/d, vn=m.vx*nx+m.vy*ny; if(vn>0){ m.vx-=2*vn*nx; m.vy-=2*vn*ny; } } }
  function capS(ang){ return CAP0+clamp((168-ang)/156,0,1)*(CAP1-CAP0); }
  function stepK(dt){ const B=breath(), R=curR(), Q=(+$('hr').value)*(+$('sv').value)/1000, vb=42*(Q/4.9);
    rbc.forEach((c)=>{ c.s=(c.s+vb*dt)%CAP.len; });
    for(const m of o2){
      if(m.st==='wait'){ if(B.inh&&Math.random()<dt*2.5){ m.st='in'; m.s=0; } }
      else if(m.st==='in'){ m.s+=dt*80; const q=at(BRP,m.s); m.x=q[0]; m.y=q[1]; if(m.s>=BRP.len){ m.st='air'; m.vx=rnd(-20,20); m.vy=rnd(5,30); } }
      else if(m.st==='air'){ walk(m,dt,R); const dx=m.x-AC[0], dy=m.y-AC[1], d=Math.hypot(dx,dy), ang=Math.atan2(dy,dx)*180/Math.PI;
        if(ang>18&&ang<162&&d>R-10&&Math.random()<dt*0.9){ m.st='x'; m.t=0; m.fx=m.x; m.fy=m.y; const a=ang*Math.PI/180; m.gx=AC[0]+CRd*Math.cos(a); m.gy=AC[1]+CRd*Math.sin(a); m.s=capS(ang); } }
      else if(m.st==='x'){ m.t+=dt/0.6; m.x=lerp(m.fx,m.gx,sm(m.t)); m.y=lerp(m.fy,m.gy,sm(m.t)); if(m.t>=1) m.st='b'; }
      else if(m.st==='b'){ m.s+=vb*dt; const q=at(CAP,m.s); m.x=q[0]; m.y=q[1]; if(m.s>=CAP.len-2) m.st='wait'; } }
    for(const m of co2){
      if(m.st==='wait'){ m.w-=dt; if(m.w<=0){ m.st='bl'; m.s=0; m.sx=CAP0+rnd(0.05,0.55)*(CAP1-CAP0); } }
      else if(m.st==='bl'){ m.s+=vb*dt; const q=at(CAP,m.s); m.x=q[0]; m.y=q[1];
        if(m.s>=m.sx){ m.st='x'; m.t=0; m.fx=m.x; m.fy=m.y; const a=Math.atan2(m.y-AC[1],m.x-AC[0]); m.gx=AC[0]+(R-14)*Math.cos(a); m.gy=AC[1]+(R-14)*Math.sin(a); } }
      else if(m.st==='x'){ m.t+=dt/0.6; m.x=lerp(m.fx,m.gx,sm(m.t)); m.y=lerp(m.fy,m.gy,sm(m.t)); if(m.t>=1){ m.st='air'; m.vx=rnd(-15,15); m.vy=rnd(-30,-5); } }
      else if(m.st==='air'){ walk(m,dt,R); if(!B.inh&&Math.random()<dt*1.6) m.st='go'; }
      else if(m.st==='go'){ const e=BRP.pts[BRP.pts.length-1], dx=e[0]-m.x, dy=e[1]-m.y, d=Math.hypot(dx,dy); if(d<5){ m.st='out'; m.s=BRP.len; } else { m.x+=dx/d*70*dt; m.y+=dy/d*70*dt; } }
      else if(m.st==='out'){ m.s-=dt*85; const q=at(BRP,Math.max(0,m.s)); m.x=q[0]; m.y=q[1]; if(m.s<=0){ m.st='wait'; m.w=rnd(0.3,2.2); } } }
    const spd=(40+60*ampK())*Math.sqrt(+$('br').value/15);
    air.forEach((a)=>{ const P=a.sd?AWR:AWL; a.s+=(B.inh?1:-1)*dt*spd; a.s=((a.s%P.len)+P.len)%P.len; }); }
  function o2icon(x,y){ dot(x-2.4,y,2.7,'#ea580c'); dot(x+2.4,y,2.7,'#ea580c'); }
  function co2icon(x,y){ dot(x-4,y,2.5,'#94a3b8'); dot(x+4,y,2.5,'#94a3b8'); dot(x,y,2.4,'#1f2937'); }
  function drawK(){ const s6=S6(), B=breath(), amp=ampK(), R=curR(), br=+$('br').value;
    // 胸
    ctx.fillStyle='#fff7ed'; ctx.beginPath(); ctx.moveTo(130,0); ctx.lineTo(130,24); ctx.quadraticCurveTo(66,28,40,70); ctx.lineTo(26,318); ctx.lineTo(274,318); ctx.lineTo(260,70); ctx.quadraticCurveTo(234,28,170,24); ctx.lineTo(170,0); ctx.closePath(); ctx.fill(); ctx.strokeStyle='#fed7aa'; ctx.lineWidth=2; ctx.stroke();
    ctx.strokeStyle='#f3e3cf'; ctx.lineWidth=3; for(let k=0;k<5;k++){ const y=96+k*38; ctx.beginPath(); ctx.moveTo(146,y); ctx.quadraticCurveTo(72,y-6,42,y+26); ctx.stroke(); ctx.beginPath(); ctx.moveTo(154,y); ctx.quadraticCurveTo(228,y-6,258,y+26); ctx.stroke(); }
    const ex=0.05*B.b*amp, ey=0.08*B.b*amp;
    [94,206].forEach((cx)=>{ const rx=50*(1+ex), ry=85*(1+ey), cy=116+ry; ctx.fillStyle='#fce7f3'; ctx.beginPath(); ctx.ellipse(cx,cy,rx,ry,0,0,Math.PI*2); ctx.fill(); ctx.strokeStyle='#f472b6'; ctx.lineWidth=2; ctx.stroke(); });
    [[[104,150],[84,192],[70,230]],[[104,150],[118,200],[112,246]],[[196,150],[216,192],[230,230]],[[196,150],[184,196],[176,224]],[[84,192],[100,214]],[[216,192],[200,214]]].forEach((b)=>poly(b,3,'rgba(148,163,184,.55)'));
    poly([[150,0],[150,104]],15,'#94a3b8'); poly([[150,0],[150,104]],11,'#e2e8f0'); for(let y=8;y<100;y+=9) poly([[144,y],[156,y]],1.4,'#94a3b8');
    poly([[150,104],[118,128],[104,150]],10,'#94a3b8'); poly([[150,104],[118,128],[104,150]],6,'#e2e8f0');
    poly([[150,104],[182,128],[196,150]],10,'#94a3b8'); poly([[150,104],[182,128],[196,150]],6,'#e2e8f0');
    ctx.save(); ctx.translate(166,252); ctx.rotate(-0.45); ctx.fillStyle='#fda4af'; ctx.beginPath(); ctx.ellipse(0,0,25,19,0,0,Math.PI*2); ctx.fill(); ctx.strokeStyle='#e11d48'; ctx.lineWidth=1.5; ctx.stroke(); ctx.restore();
    const apex=290+14*B.b*Math.min(1.6,amp); ctx.strokeStyle='#fb923c'; ctx.lineWidth=7; ctx.lineCap='round'; ctx.beginPath(); ctx.moveTo(30,314); ctx.quadraticCurveTo(150,2*apex-314,270,314); ctx.stroke();
    air.forEach((a)=>{ const q=at(a.sd?AWR:AWL,a.s); if(B.inh){ if(a.k%5===0) o2icon(q[0],q[1]); else dot(q[0],q[1],2.4,'#cbd5e1'); } else { if(a.k%6===0) o2icon(q[0],q[1]); else if(a.k%4===2) co2icon(q[0],q[1]); else dot(q[0],q[1],2.4,'#cbd5e1'); } });
    txt(B.inh?tx('↓ すう','↓ 吸う'):tx('↑ はく','↑ はく'),12,24,18,B.inh?'#0891b2':'#7c3aed','bold','left');
    txt('1分間に'+br+'回',12,44,11,'#475569','','left');
    txt('気管',160,56,12,'#334155','bold','left',0,true); if(!s6) txt('気管支',196,108,11,'#334155','bold','left',0,true);
    txt('肺',94,220,15,'#be185d','bold','center',0,true); txt('心臓',166,256,10,'#881337','bold','center');
    if(!s6) txt('横隔膜',272,298,11,'#c2410c','bold','right',0,true);
    // 拡大のつなぎ線
    ctx.strokeStyle='#38bdf8'; ctx.lineWidth=1.5; ctx.setLineDash([4,4]); ctx.beginPath(); ctx.arc(226,206,10,0,Math.PI*2); ctx.stroke(); ctx.beginPath(); ctx.moveTo(234,200); ctx.lineTo(306,70); ctx.moveTo(234,212); ctx.lineTo(306,300); ctx.stroke(); ctx.setLineDash([]);
    // 拡大図
    panel(306,6,328,322);
    txt(tx('肺胞（はいほう）の拡大','肺胞の拡大（イメージ）'),318,28,13,'#0f172a','bold','left',170);
    o2icon(500,22); txt('酸素 → 血液へ',510,26,11,'#9a3412','bold'); co2icon(500,40); txt('二酸化炭素 → 肺胞へ',510,44,11,'#334155','bold','left',118);
    poly(BRP.pts,22,'#f9a8d4'); poly(BRP.pts,16,'#f8fafc');
    [[408,126,20],[396,166,17],[532,100,21],[560,136,18],[512,72,15]].forEach((c)=>{ ctx.fillStyle='#fdf2f8'; ctx.beginPath(); ctx.arc(c[0],c[1],c[2],0,Math.PI*2); ctx.fill(); ctx.strokeStyle='#fbcfe8'; ctx.lineWidth=2; ctx.stroke(); });
    ctx.fillStyle='#f8fafc'; ctx.beginPath(); ctx.arc(AC[0],AC[1],R,0,Math.PI*2); ctx.fill(); ctx.strokeStyle='#f472b6'; ctx.lineWidth=3; ctx.stroke();
    poly(CAP.pts,22,'#f1f5f9');
    for(let i=1;i<CAP.pts.length;i++){ const f=clamp((CAP.cum[i]-CAP0)/(CAP1-CAP0)*1.6,0,1); poly([CAP.pts[i-1],CAP.pts[i]],18,mixc([191,219,254],[254,202,202],f)); }
    rbc.forEach((c)=>{ const q=at(CAP,c.s), f=clamp((c.s-CAP0)/(CAP1-CAP0)*1.6,0,1); dot(q[0],q[1],5.6,mixc(BLUE,RED,f)); dot(q[0]-1,q[1]-1,2,'rgba(255,255,255,.35)'); });
    o2.forEach((m)=>{ if(m.st!=='wait') o2icon(m.x,m.y); }); co2.forEach((m)=>{ if(m.st!=='wait') co2icon(m.x,m.y); });
    txt(tx('肺胞','肺胞'),470,140,13,'#be185d','bold','center',0,true);
    txt('毛細血管',470,288,11.5,'#9f1239','bold','center',0,true);
    txt(B.inh?'↓ 空気':'↑ 空気',340,62,11,B.inh?'#0891b2':'#7c3aed','bold','left');
    txt(tx('心臓から来た','肺動脈から'),322,230,11,'#1d4ed8','bold','left'); txt(tx('二酸化炭素が多い血液','（静脈血）'),322,245,11,'#1d4ed8','','left',98);
    txt(tx('心臓へもどる','肺静脈へ'),624,230,11,'#b91c1c','bold','right'); txt(tx('酸素が多い血液','（動脈血）'),624,245,11,'#b91c1c','','right',98);
    poly([[324,214],[346,208]],2,'#1d4ed8'); ctx.fillStyle='#1d4ed8'; ctx.beginPath(); ctx.moveTo(352,206); ctx.lineTo(343,204); ctx.lineTo(345,212); ctx.closePath(); ctx.fill();
    poly([[594,198],[616,204]],2,'#b91c1c'); ctx.fillStyle='#b91c1c'; ctx.beginPath(); ctx.moveTo(622,206); ctx.lineTo(613,200); ctx.lineTo(612,208); ctx.closePath(); ctx.fill();
    txt(tx('毛細血管で、血液が酸素を受けとり、二酸化炭素を出す','肺胞と毛細血管の間で、酸素と二酸化炭素が入れかわる'),470,314,11,'#475569','','center',310);
    // 吸う空気・はいた空気の割合
    const bx=80, sc=7.4;
    txt(tx('すう空気','吸う空気'),12,346,12,'#0f172a','bold');
    ctx.fillStyle='#fb923c'; ctx.fillRect(bx,337,21*sc,9); txt('酸素 約21%',bx+21*sc+5,346,11,'#9a3412','bold');
    ctx.fillStyle='#64748b'; ctx.fillRect(bx,350,1.5,9); txt('二酸化炭素 約0.04%',bx+6,359,11,'#334155');
    txt('はいた空気',12,384,12,'#0f172a','bold');
    ctx.fillStyle='#fb923c'; ctx.fillRect(bx,375,17*sc,9); txt('酸素 約17%',bx+17*sc+5,384,11,'#9a3412','bold');
    ctx.fillStyle='#64748b'; ctx.fillRect(bx,388,4*sc,9); txt('二酸化炭素 約4%',bx+4*sc+5,397,11,'#334155');
    txt(tx('残りはおもにちっ素（約78%）。数値は目安','残りはおもに窒素（約78%）。数値は目安'),12,414,10,'#64748b','','left',290);
    // 右下：1分間の空気
    const V=br*(+$('tv').value);
    panel(318,338,316,76);
    txt(tx('1分間に出入りする空気','1分間に出入りする空気'),330,358,11.5,'#475569','bold','left');
    txt((V/1000).toFixed(1)+' L',330,392,26,'#0e7490','bold','left');
    txt(br+'回 × '+num(+$('tv').value)+'mL',470,362,12,'#334155','','left',156);
    txt(tx('取り入れる酸素','取り入れる酸素（目安）'),470,382,11,'#475569','','left',156);
    txt('約'+num(V*0.04)+'mL（目安）',470,402,13,'#c2410c','bold','left',156); }
  function hitK(x,y){
    if(inR(x,y,140,0,160,106)) return tx('気管：鼻や口から入った空気の通り道。肺につながっている','気管：空気の通り道。気管支に分かれて、左右の肺につながる');
    if(Math.hypot(x-AC[0],y-AC[1])<AR0) return tx('肺胞：肺の中の小さなふくろ。まわりを毛細血管がとりまき、酸素と二酸化炭素が入れかわる','肺胞：肺の中の小さなふくろで、数億個ある。表面積が大きいので、気体の交換が効率よく行われる');
    if(nearPts(CAP.pts,x,y,14)) return tx('毛細血管：肺胞をとりまく細い血管。ここで血液が酸素を受けとり、二酸化炭素を出す','毛細血管：肺胞をとりまく。肺動脈から来た静脈血が、酸素を受けとって動脈血になり、肺静脈へ向かう');
    if(Math.hypot((x-166)/26,(y-252)/20)<1) return tx('心臓：肺で酸素を受けとった血液を、全身へ送り出す','心臓：肺静脈から入った動脈血を、左心室から大動脈で全身へ送り出す');
    if(Math.hypot((x-94)/52,(y-202)/88)<1||Math.hypot((x-206)/52,(y-202)/88)<1) return tx('肺：小さなふくろ（肺胞）がたくさん集まっている。血液に酸素を取り入れ、二酸化炭素を出す','肺：たくさんの肺胞が集まってできている。肺には筋肉がなく、横隔膜やろっ骨の間の筋肉の動きでふくらんだりちぢんだりする');
    if(inR(x,y,26,286,274,320)) return tx('むねとおなかの間のまく（横隔膜）：下がると肺がふくらみ、空気が入る','横隔膜：下がると胸の空間が広がって肺がふくらみ、空気が吸いこまれる。上がると空気がはき出される');
    return null; }

  // ================= ③ 消化と吸収
  const SD=[4,2,6,5,9,6,2], ST=34;
  const SP=[mkPath([[120,41],[120,41]]),
    mkPath([[120,44],[120,60],[121,80],[124,100],[130,113],[138,120]]),
    mkPath([[138,120],[152,116],[164,122],[168,134],[162,146],[150,150],[140,146],[136,136],[144,128],[156,130],[158,140],[148,148],[132,152]]),
    mkPath([[132,152],[120,156],[112,164],[114,174],[126,179],[142,177],[150,186],[150,198]]),
    mkPath([[150,198],[92,198],[87,204],[92,209],[150,209],[155,215],[150,220],[92,220],[87,226],[92,231],[150,231],[155,237],[150,242],[92,242],[84,252],[78,262]]),
    mkPath([[78,262],[71,252],[70,230],[70,198],[73,186],[82,182],[160,182],[170,186],[173,200],[173,240],[170,258],[160,270],[142,276],[128,282]]),
    mkPath([[128,282],[123,292],[122,304],[122,318]])];
  const SI=SP[3].pts.concat(SP[4].pts), LI=SP[5].pts;
  function stg(p){ let t=clamp(p,0,1)*ST; for(let i=0;i<7;i++){ if(t<=SD[i]||i===6) return [i,clamp(t/SD[i],0,1)]; t-=SD[i]; } return [6,1]; }
  function stStart(i){ let a=0; for(let k=0;k<i;k++) a+=SD[k]; return a/ST; }
  function lvls(s,u){ let A,Pr,F,Wt;
    if(s===0) A=sm(u); else if(s<=2) A=1; else if(s===3) A=1+sm(u); else if(s===4) A=u<0.35?2+sm(u/0.35):3+sm((u-0.35)/0.65); else A=4;
    if(s<2) Pr=0; else if(s===2) Pr=sm(u); else if(s===3) Pr=1+sm(u); else if(s===4) Pr=u<0.35?2+sm(u/0.35):3+sm((u-0.35)/0.65); else Pr=4;
    if(s<3) F=0; else if(s===3) F=u<0.5?sm(u/0.5):1+sm((u-0.5)/0.5); else if(s===4) F=u<0.35?2:2+sm((u-0.35)/0.65); else F=3;
    if(s<4) Wt=0; else if(s===4) Wt=0.75*sm((u-0.2)/0.8); else if(s===5) Wt=0.75+0.25*sm(u); else Wt=1;
    return [A,Pr,F,Wt]; }
  const PLACE=()=>['口','食道','胃','小腸（前半）','小腸（後半）','大腸',tx('こう門','肛門')];
  const JUICE=()=>S6()?['だ液','なし（運ぶだけ）','胃液','たん汁・すい液','小腸の消化液','なし（水分を吸収）','なし']:['だ液（アミラーゼ）','なし（運ぶだけ）','胃液（ペプシン）','胆汁・すい液（アミラーゼ・トリプシン・リパーゼ）','小腸の壁の消化酵素','なし（水分を吸収）','なし'];
  const JUICE_S=()=>S6()?['だ液','なし','胃液','たん汁・すい液','小腸の消化液','なし','なし']:['だ液（アミラーゼ）','なし','胃液（ペプシン）','胆汁・すい液','小腸の壁の消化酵素','なし','なし'];
  const DESC=()=>S6()?['歯で細かくし、だ液と混ぜる（でんぷんが変化しはじめる）','筋肉の動きで胃へ送る（ここでは消化しない）','胃液と混ぜて、たんぱく質を消化しはじめる','たん汁・すい液で、でんぷん・たんぱく質・しぼうを消化','小腸のかべで消化を仕上げ、じゅう毛から吸収する','おもに水分を吸収する','吸収されなかった物を便として出す']
    :['だ液のアミラーゼがデンプンを分解しはじめる','ぜん動運動で胃へ送る（ここでは消化しない）','胃液のペプシンがタンパク質を分解する','胆汁が脂肪を細かくし、すい液の消化酵素が分解する','小腸の壁の消化酵素で仕上げ、柔毛から吸収する','おもに水分を吸収する','吸収されなかった物を便として排出する'];
  function stepS(dt){ dp+=dt*(+$('spd').value)/ST; if(dp>=1){ dp=1; run=false; $('pause').textContent='▶ 再生'; } syncPos(); }
  function syncPos(){ const v=Math.round(dp*100); if(+$('pos').value!==v){ $('pos').value=v; const l=$('posL'); if(l) l.textContent=v+'%'; } }
  function hexa(x,y,r,f,s){ ctx.beginPath(); for(let k=0;k<6;k++){ const a=Math.PI/6+k*Math.PI/3, px=x+r*Math.cos(a), py=y+r*Math.sin(a); if(k) ctx.lineTo(px,py); else ctx.moveTo(px,py); } ctx.closePath(); ctx.fillStyle=f; ctx.fill(); ctx.strokeStyle=s; ctx.lineWidth=1.2; ctx.stroke(); }
  function uX(kd,n,i){ if(n<=0) return i*15; if(n===1) return kd?i*15+Math.floor(i/3)*10:i*15+Math.floor(i/4)*14; if(n===2) return i*15+Math.floor(i/2)*9; return i*21; }
  function bnd(kd,n,i){ if(n<=0) return true; if(n===1) return kd?Math.floor(i/3)===Math.floor((i+1)/3):Math.floor(i/4)===Math.floor((i+1)/4); if(n===2) return Math.floor(i/2)===Math.floor((i+1)/2); return false; }
  function pY(kd,n,i){ if(n<=0) return 0; if(n===1) return ((kd?Math.floor(i/3):Math.floor(i/4))%2)?3:-3; if(n===2) return (Math.floor(i/2)%2)?3:-3; return (i%2)?3:-3; }
  function chPos(kd,L,i,yc){ const n=Math.min(3,Math.floor(L)), f=sm(L-n); if(L>=3) return [262+uX(kd,3,i), yc+pY(kd,3,i)]; return [262+lerp(uX(kd,n,i),uX(kd,n+1,i),f), yc+lerp(pY(kd,n,i),pY(kd,n+1,i),f)]; }
  function toVillus(x0,y0,q,lane){ const vx=lane?594:612, d1=Math.max(0,558-x0), d2=vx-558, d3=Math.max(0,318-y0), tot=d1+d2+d3, s=q*tot;
    if(s<=d1) return [x0+s,y0]; if(s<=d1+d2) return [558+(s-d1),y0]; return [vx,y0+(s-d1-d2)]; }
  const PCOL=['#86efac','#93c5fd','#f9a8d4','#fcd34d','#c4b5fd'];
  function chainDraw(kd,L,yc){ const n=Math.min(3,Math.floor(L)), f=L-n;
    if(L<3){ const P=[]; for(let i=0;i<12;i++) P.push(chPos(kd,L,i,yc));
      for(let i=0;i<11;i++){ const now=bnd(kd,n,i), nx=bnd(kd,n+1,i); if(now||nx){ const a=(now&&!nx)?1-f:1; if(a>0.02){ ctx.globalAlpha=a; poly([P[i],P[i+1]],2.2,'#64748b'); ctx.globalAlpha=1; }
          if(now&&!nx&&f>0.04&&f<0.96) txt('✂',(P[i][0]+P[i+1][0])/2,yc-11,12,'#dc2626','bold','center'); } }
      for(let i=0;i<12;i++){ const c=PCOL[i%5]; if(kd){ dot(P[i][0],P[i][1],6,c); ctx.strokeStyle='#334155'; ctx.lineWidth=1; ctx.beginPath(); ctx.arc(P[i][0],P[i][1],6,0,Math.PI*2); ctx.stroke(); } else hexa(P[i][0],P[i][1],6.3,'#fde68a','#b45309'); } }
    else { const g=L-3; for(let i=0;i<12;i++){ const st=i/12*0.55, q=clamp((g-st)/0.45,0,1); const b=chPos(kd,3,i,yc); const p=toVillus(b[0],b[1],q,0);
      ctx.globalAlpha=q>0.85?Math.max(0,(1-q)/0.15):1; if(kd){ dot(p[0],p[1],6,PCOL[i%5]); ctx.strokeStyle='#334155'; ctx.lineWidth=1; ctx.beginPath(); ctx.arc(p[0],p[1],6,0,Math.PI*2); ctx.stroke(); } else hexa(p[0],p[1],6.3,'#fde68a','#b45309'); ctx.globalAlpha=1; } } }
  function zig(x,y,c){ poly([[x,y],[x+4,y-3],[x+8,y],[x+12,y-3],[x+16,y]],1.8,c); }
  function mono(x,y){ ctx.fillStyle='#fb923c'; rrect(x-2,y-6,5,12,2); ctx.fill(); zig(x+3,y+2,'#a16207'); }
  function fatDraw(F,yc){ if(F<2){ const f1=sm(Math.min(1,F)), f2=F>1?sm(F-1):0;
      for(let i=0;i<6;i++){ const x=lerp(318+(i%3)*12,282+i*42,f1), y=lerp(yc+(i<3?-5:6),yc+(i%2?3:-3),f1), r=lerp(14,7.5,f1);
        ctx.globalAlpha=1-f2; dot(x,y,r,'#fde047'); ctx.strokeStyle='#ca8a04'; ctx.lineWidth=1; ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.stroke(); ctx.globalAlpha=1;
        if(f2>0){ ctx.globalAlpha=f2; mono(x-8,y); zig(x+2,y-7,'#a16207'); zig(x+2,y+6,'#a16207'); ctx.globalAlpha=1; } } }
    else { const g=F-2; for(let i=0;i<6;i++){ const q=clamp((g-i/6*0.6)/0.4,0,1), x0=282+i*42, y0=yc+(i%2?3:-3), p=toVillus(x0,y0,q,1);
        ctx.globalAlpha=q>0.85?Math.max(0,(1-q)/0.15):1;
        if(q<=0){ mono(p[0]-8,p[1]); zig(p[0]+2,p[1]-7,'#a16207'); zig(p[0]+2,p[1]+6,'#a16207'); }
        else if(p[0]<556){ ctx.save(); ctx.translate(p[0],p[1]); ctx.scale(0.7,0.7); mono(-8,0); zig(2,-7,'#a16207'); ctx.restore(); }
        else { dot(p[0],p[1],5,'#facc15'); ctx.strokeStyle='#a16207'; ctx.lineWidth=1; ctx.beginPath(); ctx.arc(p[0],p[1],5,0,Math.PI*2); ctx.stroke(); } ctx.globalAlpha=1; } } }
  function waterDraw(Wt,s,u,yc){ for(let i=0;i<8;i++){ const q=clamp(Wt*8-i,0,1), x0=268+i*24; let p=[x0,yc], a=1;
      if(i<6) { p=toVillus(x0,yc,q,0); if(q>0.85) a=Math.max(0,(1-q)/0.15); } else { p=[x0,yc-q*16]; a=1-q; }
      if(a>0.01){ ctx.globalAlpha=a; dot(p[0],p[1]+1,5,'#60a5fa'); ctx.fillStyle='#60a5fa'; ctx.beginPath(); ctx.moveTo(p[0]-4,p[1]-1); ctx.lineTo(p[0],p[1]-9); ctx.lineTo(p[0]+4,p[1]-1); ctx.fill(); ctx.globalAlpha=1; } }
    const fb=s>=5?(s===5?sm(u):1):0, out=s===6?sm(u):0; const fx=lerp(470,496,fb)+out*24;
    ctx.globalAlpha=1-out*0.8; poly([[fx,yc-8],[fx+8,yc-2],[fx+2,yc+4],[fx+12,yc+9]],3,fb>0.5?'#92400e':'#16a34a'); poly([[fx+18,yc-8],[fx+12,yc-1],[fx+22,yc+3],[fx+16,yc+10]],3,fb>0.5?'#92400e':'#16a34a');
    if(fb>0.5) txt('便',fx+12,yc+24,11,'#92400e','bold','center'); ctx.globalAlpha=1; }
  function pill(t,x,y,bg,fg){ ctx.font='bold 10.5px sans-serif'; const w=ctx.measureText(t).width+14; rrect(x-w,y-11,w,16,8); ctx.fillStyle=bg; ctx.fill(); txt(t,x-7,y+1,10.5,fg,'bold','right'); }
  function drawBody(s,u){ const s6=S6();
    ctx.fillStyle='#fff7ed'; ctx.strokeStyle='#fed7aa'; ctx.lineWidth=2;
    ctx.beginPath(); ctx.arc(120,26,22,0,Math.PI*2); ctx.fill(); ctx.stroke(); ctx.fillRect(110,46,20,28);
    ctx.beginPath(); ctx.moveTo(70,74); ctx.quadraticCurveTo(120,66,170,74); ctx.lineTo(186,92); ctx.lineTo(184,320); ctx.quadraticCurveTo(120,332,56,320); ctx.lineTo(54,92); ctx.closePath(); ctx.fill(); ctx.stroke();
    ctx.fillStyle='#be123c'; ctx.beginPath(); ctx.ellipse(120,40,7,3,0,0,Math.PI*2); ctx.fill();
    const glow=(on)=>{ ctx.shadowColor=on?'rgba(245,158,11,.9)':'transparent'; ctx.shadowBlur=on?12:0; };
    glow(s===3); ctx.fillStyle='#e8a87c'; ctx.beginPath(); ctx.moveTo(58,104); ctx.lineTo(108,98); ctx.lineTo(136,104); ctx.lineTo(140,112); ctx.lineTo(122,124); ctx.lineTo(100,136); ctx.lineTo(70,140); ctx.lineTo(58,128); ctx.closePath(); ctx.fill(); glow(false); ctx.strokeStyle='#c2410c'; ctx.lineWidth=1.2; ctx.stroke();
    glow(s===2); ctx.fillStyle='#fecdd3'; ctx.beginPath(); ctx.moveTo(136,118); ctx.quadraticCurveTo(150,106,168,116); ctx.quadraticCurveTo(180,134,170,152); ctx.quadraticCurveTo(152,164,128,152); ctx.quadraticCurveTo(140,144,144,132); ctx.quadraticCurveTo(142,124,136,118); ctx.closePath(); ctx.fill(); glow(false); ctx.strokeStyle='#fb7185'; ctx.lineWidth=1.5; ctx.stroke();
    poly([[122,164],[146,161],[168,155]],9,'#f59e0b'); poly([[122,164],[146,161],[168,155]],6.5,'#fde68a');
    ctx.fillStyle='#86efac'; ctx.beginPath(); ctx.ellipse(106,141,6,8,0,0,Math.PI*2); ctx.fill(); ctx.strokeStyle='#16a34a'; ctx.lineWidth=1; ctx.stroke(); poly([[108,148],[113,160]],2,'#16a34a');
    glow(s===3||s===4); poly(SI,9,'#fda4af'); glow(false); poly(SI,5,'#ffe4e6');
    glow(s===5); poly(LI,13,'#fdba74'); glow(false); poly(LI,8.5,'#ffedd5');
    glow(s===1); poly(SP[1].pts,7,'#fca5a5'); glow(false); poly(SP[1].pts,3.5,'#fee2e2'); poly(SP[6].pts.slice(0,3),8,'#fdba74');
    // 消化液のしずく
    const ph=(T*1.6)%1;
    if(s===0){ [[104,52],[136,52]].forEach((p)=>{ dot(lerp(p[0],120,ph),lerp(p[1],42,ph),2.2,'#38bdf8'); }); }
    if(s===2){ for(let k=0;k<5;k++){ const a=k*1.26+T; dot(152+16*Math.cos(a)*(1-ph*0.5),136+10*Math.sin(a)*(1-ph*0.5),1.8,'#22d3ee'); } }
    if(s===3){ dot(lerp(108,113,ph),lerp(148,160,ph),2.2,'#16a34a'); dot(lerp(130,116,ph),lerp(162,166,ph),2.2,'#d97706'); }
    if(s===4){ for(let k=0;k<6;k++){ const q=at(SP[4],((k/6+ph/6)%1)*SP[4].len); dot(q[0],q[1]-4,1.6,'#db2777'); } }
    if(s===5){ for(let k=0;k<4;k++){ const q=at(SP[5],((k/4+ph/4)%1)*SP[5].len); dot(q[0]+(ph*6),q[1]-ph*6,1.8,'#3b82f6'); } }
    // 食べ物の位置
    const P=SP[s], q=s===0?[120,41]:at(P,P.len*u), r=s===0?6+Math.sin(T*12)*1.2:6; ctx.globalAlpha=s===6?1-0.8*u:1; dot(q[0],q[1],r+1.5,'#fff'); dot(q[0],q[1],r,'#a16207'); ctx.globalAlpha=1;
    // 名前
    const lab=(t,x,y,lx,ly,al)=>{ poly([[lx,ly],[al==='right'?x+3:x-3,y-4]],1,'#94a3b8'); txt(t,x,y,11,'#334155','bold',al,0,true); };
    lab('口',50,44,110,41,'right'); lab('食道',50,84,119,84,'right'); lab(tx('かん臓','肝臓'),50,114,64,114,'right'); lab(tx('たんのう','胆のう'),50,146,100,143,'right');
    lab('大腸',50,224,66,224,'right'); lab(tx('こう門','肛門'),50,306,118,304,'right'); lab('胃',194,130,176,130,'left'); lab('すい臓',194,162,170,158,'left'); lab('小腸',194,218,157,218,'left'); }
  function drawS(){ const s6=S6(); const sg=stg(dp), s=sg[0], u=sg[1]; const L=lvls(s,u);
    drawBody(s,u);
    // 見出し
    txt('いまの場所：'+PLACE()[s],252,26,16,'#0f172a','bold','left',296);
    txt('はたらく消化液：'+JUICE()[s],252,45,12,'#0e7490','bold','left',300);
    txt(DESC()[s],252,61,11.5,'#475569','','left',300);
    // ヨウ素液
    const io=L[0]<0.3?0:(L[0]<1.8?1:2), ioc=['#5b21b6','#a78bfa','#d6a35b'][io];
    ctx.fillStyle='#f8fafc'; rrect(612,8,14,40,6); ctx.fill(); ctx.strokeStyle='#64748b'; ctx.lineWidth=1.2; ctx.stroke(); ctx.fillStyle=ioc; rrect(613.5,24,11,22.5,5); ctx.fill();
    txt('ヨウ素液',606,24,10,'#475569','bold','right'); txt(['青むらさき','うすい青むらさき','変化しない'][io],606,40,10,'#334155','','right',64);
    // 柔毛
    ctx.fillStyle='#ffe4e6'; ctx.beginPath(); ctx.moveTo(558,318); ctx.lineTo(558,104); ctx.quadraticCurveTo(558,78,593,78); ctx.quadraticCurveTo(628,78,628,104); ctx.lineTo(628,318); ctx.closePath(); ctx.fill(); ctx.strokeStyle='#fb7185'; ctx.lineWidth=2; ctx.stroke();
    poly([[568,318],[568,104],[593,92],[618,104],[618,318]],2.5,'rgba(220,38,38,.7)'); for(let y=130;y<318;y+=38) poly([[568,y],[580,y+8],[606,y-6],[618,y+4]],1.2,'rgba(220,38,38,.45)');
    poly([[594,98],[594,318]],4,'#bef264'); poly([[594,98],[594,318]],2,'#65a30d');
    txt(tx('じゅう毛','柔毛'),593,72,11.5,'#be123c','bold','center');
    txt(tx('毛細血管（→かん臓へ）','毛細血管（→肝臓へ）'),632,331,10,'#b91c1c','bold','right'); txt('リンパ管（中央の線）',632,344,10,'#4d7c0f','bold','right');
    // 4つの養分
    const RY=[68,130,192,254], YC=RY.map((y)=>y+36);
    const nmA=tx('でんぷん（ごはん・パン）','デンプン（ごはん・パン）'), nmP=tx('たんぱく質（肉・魚・たまご）','タンパク質（肉・魚・卵）'), nmF=tx('しぼう（油・バター）','脂肪（油・バター）'), nmW=tx('水・食物せんい','水・食物繊維');
    const fA=L[0]<0.5?'':L[0]<1.5?'→ 短くなる':L[0]<2.5?tx('→ さらに小さく','→ 麦芽糖など'):L[0]<3.05?tx('→ 糖','→ ブドウ糖'):tx('→ 糖 → 血液へ','→ ブドウ糖 → 毛細血管へ');
    const fP=L[1]<0.5?'':L[1]<1.5?'→ 小さく分かれる':L[1]<2.5?'→ さらに小さく':L[1]<3.05?'→ アミノ酸':'→ アミノ酸 → 毛細血管へ';
    const fF=L[2]<0.5?'':L[2]<1.5?tx('→ 細かい粒（たん汁）','→ 細かい粒（胆汁）'):L[2]<2.05?tx('→ しぼう酸・モノグリセリド','→ 脂肪酸・モノグリセリド'):'→ リンパ管へ';
    const fW=s<4?'':s===4?'→ 小腸で吸収':s===5?'→ 大腸で吸収':'→ 残りは便に';
    [[nmA,fA,'#b45309'],[nmP,fP,'#1d4ed8'],[nmF,fF,'#a16207'],[nmW,fW,'#0369a1']].forEach((r,i)=>{ txt(r[0],252,RY[i]+13,12,'#0f172a','bold','left',165); if(r[1]) txt(r[1],262,RY[i]+58,11,r[2],'bold','left',284); if(i<3) poly([[252,RY[i]+62],[548,RY[i]+62]],1,'#eef2f7'); });
    const tagA=L[0]>0&&L[0]<1?tx('だ液','アミラーゼ（だ液）'):L[0]>1&&L[0]<2?tx('すい液','アミラーゼ（すい液）'):L[0]>2&&L[0]<3?tx('小腸の消化液','小腸の壁の消化酵素'):L[0]>3&&L[0]<4?tx('じゅう毛で吸収','柔毛で吸収'):'';
    const tagP=L[1]>0&&L[1]<1?tx('胃液','ペプシン（胃液）'):L[1]>1&&L[1]<2?tx('すい液','トリプシン（すい液）'):L[1]>2&&L[1]<3?tx('小腸の消化液','小腸の壁の消化酵素'):L[1]>3&&L[1]<4?tx('じゅう毛で吸収','柔毛で吸収'):'';
    const tagF=L[2]>0&&L[2]<1?tx('たん汁','胆汁（消化酵素なし）'):L[2]>1&&L[2]<2?tx('すい液','リパーゼ（すい液）'):L[2]>2&&L[2]<3?tx('じゅう毛 → リンパ管','柔毛 → リンパ管'):'';
    const tagW='';
    [[tagA,'#e0f2fe','#0369a1'],[tagP,'#ccfbf1','#0f766e'],[tagF,'#fef3c7','#92400e'],[tagW,'#dbeafe','#1d4ed8']].forEach((g,i)=>{ if(g[0]) pill(g[0],548,RY[i]+12,g[1],g[2]); });
    chainDraw(0,L[0],YC[0]+2); chainDraw(1,L[1],YC[1]+2); fatDraw(L[2],YC[2]+2); waterDraw(L[3],s,u,YC[3]+2);
    // 進み具合（タップで移動）
    const X0=16, WW=608; let x=X0; const nm=['口','食道','胃','小腸','','大腸',tx('こう門','肛門')], cl=['#bae6fd','#e2e8f0','#fecdd3','#fbcfe8','#fbcfe8','#fed7aa','#e7e5e4'];
    for(let i=0;i<7;i++){ const w=SD[i]/ST*WW; ctx.fillStyle=cl[i]; ctx.fillRect(x,362,w,30); x+=w; }
    x=X0; for(let i=0;i<7;i++){ const w=SD[i]/ST*WW; if(i===3) txt('小腸',x+(SD[3]+SD[4])/ST*WW/2,382,12,'#334155','bold','center'); else if(nm[i]) txt(nm[i],x+w/2,382,12,'#334155','bold','center',w-4); x+=w; }
    ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1; ctx.strokeRect(X0,362,WW,30);
    const mx=X0+dp*WW; ctx.fillStyle='rgba(15,23,42,.10)'; ctx.fillRect(X0,362,mx-X0,30); poly([[mx,358],[mx,396]],2.5,'#0f172a'); ctx.fillStyle='#0f172a'; ctx.beginPath(); ctx.moveTo(mx-7,350); ctx.lineTo(mx+7,350); ctx.lineTo(mx,359); ctx.closePath(); ctx.fill();
    txt('（時間の長さは実際とはちがいます）',X0,412,10,'#64748b','','left'); txt('▲ 帯をタップ・ドラッグすると、その場所へ動かせます',X0+WW,412,10,'#64748b','','right'); }
  function hitS(x,y){
    if(Math.hypot(x-120,y-26)<23) return [tx('口：歯で食べ物を細かくし、だ液と混ぜる。だ液はでんぷんを別の物に変える','口：歯でかみくだく。だ液にふくまれるアミラーゼが、デンプンを麦芽糖などに分解する'),0];
    if(inR(x,y,112,46,132,116)) return [tx('食道：口と胃をつなぐ管。筋肉の動きで食べ物を胃へ送る','食道：口と胃をつなぐ管。ぜん動運動で食べ物を胃へ送る'),1];
    if(inR(x,y,130,106,180,158)) return [tx('胃：胃液を出して、たんぱく質を消化する','胃：胃液にふくまれるペプシンが、タンパク質を分解する（胃液は塩酸をふくみ、強い酸性）'),2];
    if(inR(x,y,98,130,114,152)) return [tx('たんのう：かん臓でつくられたたん汁をためておく','胆のう：肝臓でつくられた胆汁をためる。胆汁は消化酵素をふくまないが、脂肪を細かい粒にして消化を助ける'),3];
    if(inR(x,y,56,96,128,142)) return [tx('かん臓：たん汁をつくる。小腸で吸収した養分をたくわえる','肝臓：胆汁をつくる。養分をたくわえ、有害な物を無害な物に変える'),3];
    if(inR(x,y,118,150,172,170)) return [tx('すい臓：すい液を出す。すい液は、でんぷん・たんぱく質・しぼうを消化する','すい臓：すい液を出す。すい液はアミラーゼ・トリプシン・リパーゼをふくむ'),3];
    if(inR(x,y,82,190,160,256)) return [tx('小腸：消化を仕上げ、内側のじゅう毛から養分を吸収する（のばすと長さ約6m）','小腸：壁の消化酵素で分解を仕上げ、柔毛から養分を吸収する（のばすと長さ約6m）'),4];
    if(nearPts(LI,x,y,10)) return [tx('大腸：おもに水分を吸収する','大腸：おもに水分を吸収する。残りは便になる'),5];
    if(inR(x,y,108,280,136,322)) return [tx('こう門：吸収されなかった物が、便として出される','肛門：吸収されなかった物が、便として排出される'),6];
    if(inR(x,y,556,70,632,332)) return [tx('じゅう毛：小腸のかべの小さな出っぱり。糖・アミノ酸は毛細血管へ、しぼう酸・モノグリセリドはリンパ管へ入る','柔毛：小腸の壁の小さな突起。ブドウ糖・アミノ酸は毛細血管へ、脂肪酸・モノグリセリドは再び脂肪になってリンパ管へ入る'),null];
    return null; }
  function updateS(force){ const sg=stg(dp), s=sg[0], u=sg[1], L=lvls(s,u); const io=L[0]<0.3?0:(L[0]<1.8?1:2);
    const ab=Math.round(((clamp(L[0]-3,0,1)+clamp(L[1]-3,0,1)+clamp(L[2]-2,0,1))/3)*100);
    const key=s+'|'+io+'|'+ab+'|'+S6(); if(!force&&key===lastKey) return; lastKey=key;
    setV('s1',PLACE()[s]); setV('s2',JUICE_S()[s]); setV('s3',['青むらさき色','うすい青むらさき色','変化しない'][io]); setV('s4',ab+'%');
    setShare(tx('【消化と吸収】いま'+PLACE()[s]+'。'+JUICE()[s].replace('なし','消化液なし')+'。吸収された養分 '+ab+'%（でんぷん→糖、たんぱく質→アミノ酸、しぼう→しぼう酸とモノグリセリド）｜シミュラボ',
      '【消化と吸収】いま'+PLACE()[s]+'。'+JUICE()[s].replace('なし','消化液なし')+'。吸収された養分 '+ab+'%（デンプン→ブドウ糖、タンパク質→アミノ酸、脂肪→脂肪酸とモノグリセリド）｜シミュラボ')); }

  // ================= 切りかえ・数値
  const SL={J:['心拍数（1分間）','1回に送り出す血液の量','1分間に送り出す血液の量','1日に送り出す血液の量（目安）'],K:['呼吸数（1分間）','1回の呼吸で出入りする空気','1分間に出入りする空気','1分間に取り入れる酸素（目安）'],S:['いまの場所','はたらく消化液','ヨウ素液を加えると','吸収された養分（モデル）']};
  function update(){ SL[mode].forEach((t,i)=>setK('s'+(i+1),(mode==='S'&&i===2)?tx('ヨウ素液を加えると（でんぷん）','ヨウ素液を加えると（デンプン）'):t));
    if(mode==='J'){ const hr=+$('hr').value, sv=+$('sv').value, Q=hr*sv; setV('s1',hr+'回'); setV('s2',sv+'mL'); setV('s3',(Q/1000).toFixed(1)+'L'); setV('s4','約'+num(Q*1.44)+'L');
      setShare('【血液の循環】心拍数'+hr+'回/分 × 1回'+sv+'mL ＝ 1分間に'+(Q/1000).toFixed(1)+'L、1日で約'+num(Q*1.44)+'Lの血液を心臓が送り出す（目安）｜シミュラボ'); }
    else if(mode==='K'){ const b=+$('br').value, tv=+$('tv').value, V=b*tv; setV('s1',b+'回'); setV('s2',num(tv)+'mL'); setV('s3',(V/1000).toFixed(1)+'L'); setV('s4','約'+num(V*0.04)+'mL');
      setShare('【呼吸】1分間に'+b+'回 × '+num(tv)+'mL ＝ '+(V/1000).toFixed(1)+'Lの空気が出入りし、酸素を約'+num(V*0.04)+'mL取り入れる（吸う空気の酸素21%・はいた空気約17%で計算）｜シミュラボ'); }
    else updateS(true); }
  const HASH={J:'junkan',K:'kokyu',S:'shoka'};
  function setMode(m){ mode=m; info=null;
    [['tJ','J'],['tK','K'],['tS','S']].forEach((a)=>{ const b=$(a[0]); b.className='btn '+(a[1]===m?'btn-primary':'btn-ghost'); b.setAttribute('aria-pressed',a[1]===m?'true':'false'); });
    ['hr','sv'].forEach((id)=>{ fld(id).style.display=m==='J'?'':'none'; }); ['br','tv'].forEach((id)=>{ fld(id).style.display=m==='K'?'':'none'; }); ['pos','spd'].forEach((id)=>{ fld(id).style.display=m==='S'?'':'none'; });
    $('rest').style.display=m==='S'?'none':''; $('ex').style.display=m==='S'?'none':''; $('eat').style.display=m==='S'?'':'none';
    if(m==='S'&&dp>=1) dp=0;
    run=true; $('pause').textContent='⏸ 一時停止';
    try{ history.replaceState(null,'',location.pathname+location.search+'#'+HASH[m]); }catch(e){}
    update(); }
  function preset(ex){ const v=ex?{hr:130,sv:100,br:30,tv:1500}:{hr:70,sv:70,br:15,tv:500}; Object.keys(v).forEach((id)=>{ $(id).value=v[id]; $(id).dispatchEvent(new Event('input')); }); }
  ['hr','sv','br','tv'].forEach((id)=>$(id).addEventListener('input',update));
  $('lv').addEventListener('change',()=>{ lastKey=''; update(); });
  $('pos').addEventListener('input',()=>{ dp=(+$('pos').value)/100; run=false; $('pause').textContent='▶ 再生'; updateS(); });
  $('tJ').addEventListener('click',()=>setMode('J')); $('tK').addEventListener('click',()=>setMode('K')); $('tS').addEventListener('click',()=>setMode('S'));
  $('pause').addEventListener('click',()=>{ if(!run&&mode==='S'&&dp>=1) dp=0; run=!run; $('pause').textContent=run?'⏸ 一時停止':'▶ 再生'; });
  $('rest').addEventListener('click',()=>preset(false)); $('ex').addEventListener('click',()=>preset(true));
  $('eat').addEventListener('click',()=>{ dp=0; run=true; $('pause').textContent='⏸ 一時停止'; syncPos(); updateS(); });
  function scrub(x){ dp=clamp((x-16)/608,0,1); run=false; $('pause').textContent='▶ 再生'; syncPos(); updateS(); }
  cv.addEventListener('pointerdown',(e)=>{ const p=cpos(cv,e), x=p[0]/dpr, y=p[1]/dpr;
    if(mode==='S'&&y>=344&&y<=402){ e.preventDefault(); dragTL=true; try{ cv.setPointerCapture(e.pointerId); }catch(er){} scrub(x); return; }
    if(mode==='J'){ const t=hitJ(x,y); info=t?{t:t,x:x,y:y,life:5}:null; }
    else if(mode==='K'){ const t=hitK(x,y); info=t?{t:t,x:x,y:y,life:5}:null; }
    else { const h=hitS(x,y); info=h?{t:h[0],x:x,y:y,life:5}:null; if(h&&h[1]!=null){ dp=stStart(h[1])+0.002; syncPos(); updateS(); } } });
  cv.addEventListener('pointermove',(e)=>{ if(!dragTL) return; const p=cpos(cv,e); scrub(p[0]/dpr); });
  const endDrag=()=>{ dragTL=false; }; cv.addEventListener('pointerup',endDrag); cv.addEventListener('pointercancel',endDrag);
  function draw(){ ctx.fillStyle='#ffffff'; ctx.fillRect(0,0,W,H); if(mode==='J') drawJ(); else if(mode==='K') drawK(); else drawS(); bubble(); }
  let last=performance.now();
  function loop(now){ const dt=Math.min(0.05,Math.max(0,(now-last)/1000)); last=now;
    if(run){ T+=dt; cph+=dt*(+$('hr').value)/60; rph+=dt*(+$('br').value)/60;
      const nb=Math.floor(cph); if(nb!==beatN){ beatN=nb; beatT=T; pulses.push(T+0.12); if(pulses.length>8) pulses.shift(); }
      if(mode==='J') stepJ(dt); else if(mode==='K') stepK(dt); else { stepS(dt); updateS(); } }
    if(info){ info.life-=dt; if(info.life<=0) info=null; }
    draw(); requestAnimationFrame(loop); }
  const h0=(location.hash||'').replace('#',''); const m0=h0==='kokyu'?'K':(h0==='shoka'?'S':'J');
  pulses=[-1.2,-0.34]; for(let i=0;i<40;i++) stepJ(0.05);
  setMode(m0); draw(); requestAnimationFrame(loop);
'''

sim(slug="hito-karada", cat="rika", emoji="🫀", score=80,
    title="人の体のつくりと働き（血液の循環・呼吸・消化）",
    title_tag="血液の循環（肺循環・体循環）シミュレーション｜心臓の4つの部屋・肺胞での呼吸・消化酵素のはたらき（小6・中2理科）",
    meta_desc="小6「人の体のつくりと働き」・中2「動物の体のつくりと働き」のシミュレーション。心臓の4つの部屋と肺循環・体循環、動脈血と静脈血の流れ、心拍数と1分間に送り出す血液の量、肺胞での気体の交換、消化酵素の分解と柔毛での吸収を動きで確かめられます。",
    og_title="人の体のつくりと働き（血液の循環・呼吸・消化）シミュレーター",
    og_desc="心拍数を変えると1分間に送り出す血液の量が変わる。肺循環・体循環、肺胞での気体の交換、消化酵素のはたらきを動きで確かめる。",
    card_desc="心臓の4つの部屋と肺循環・体循環、肺胞での気体の交換、消化酵素のはたらきを動きで確かめる。",
    lead="血液の循環（肺循環・体循環）、肺での呼吸、消化と吸収の3つを切りかえて見られます。心拍数を変えると、心臓が1分間に送り出す血液の量も変わります。",
    model="小6 人の体のつくりと働き／中2 動物の体のつくりと働き", level="小学6年、中学2年",
    unit="小学校 第6学年 B（1）人の体のつくりと働き／中学校 第2分野（3）ア（ｳ）動物の体のつくりと働き",
    canvas=canvas(640, 420, light=True),
    controls=select("lv", "ことば", [("s6", "小6の言葉"), ("c2", "中2の言葉")])
             + slider("hr", "心拍数（1分間）", 40, 200, HR0, 5, "{v}回") + slider("sv", "1回に送り出す血液の量", 30, 130, SV0, 5, "{v}mL")
             + slider("br", "呼吸数（1分間）", 6, 40, BR0, 1, "{v}回") + slider("tv", "1回の呼吸の量", 300, 3000, TV0, 100, "{v}mL")
             + slider("pos", "どこまで進んだか", 0, 100, 0, 1, "{v}%") + select("spd", "進む速さ", [("1", "ふつう"), ("0.5", "ゆっくり"), ("2", "はやい")]),
    buttons=btn("tJ", "🫀 ① 血液の循環", True) + btn("tK", "🫁 ② 呼吸") + btn("tS", "🍙 ③ 消化と吸収")
            + btn("pause", "⏸ 一時停止") + btn("rest", "🧘 安静時") + btn("ex", "🏃 運動中") + btn("eat", "▶ 食べる（最初から）", True),
    stats=stats([("s1", "心拍数（1分間）", False), ("s2", "1回に送り出す血液の量", False), ("s3", "1分間に送り出す血液の量", True), ("s4", "1日に送り出す血液の量（目安）", False)]),
    legend="図は模式図です。①は体の正面から見た向き（図の左が体の右）で、酸素が多い血液を赤、二酸化炭素が多い血液を青で表しています（実際の静脈血は暗い赤色）。心臓が打つ速さは実際と同じですが、血液の流れは見やすく速めています。心臓の部屋・血管・臓器をタップすると名前と働きが出ます。③は進み具合の帯をタップ・ドラッグすると、その場所の消化のようすを見られます。数値はおとなの目安で、医療的な判断には使えません。",
    article=KARADA_ARTICLE, faqs=KARADA_FAQS,
    rel=[("myakuhaku-heikin", "💓", "脈拍・心拍数 平均チェック"), ("reaction-test", "⚡", "反応速度テスト"), ("mendel-iden", "🌱", "遺伝の規則性シミュレーター"),
         ("diffusion", "🫧", "拡散シミュレーター"), ("ketsueki-iden", "🩸", "血液型 遺伝 判定")],
    js=KARADA_JS)


# ============================================================ 2 カムとベルト・プーリ
KAMU_ARTICLE = "<h2>このシミュレーションでわかること</h2>\n" + P(
    "ベルトとプーリでは、<b>速度伝達比 ＝ 原動プーリの回転数 ÷ 従動プーリの回転数 ＝ 従動プーリの直径 ÷ 原動プーリの直径</b> です。"
    "従動プーリを大きくするほど従動プーリはゆっくり回り、回す力（トルク）は大きくなります。カム機構では、カム（原動節）の形によって、従動節の上下の動き方が変わります。") + '''
<p>中学校 技術・家庭（技術分野）の「C エネルギー変換の技術」で学ぶ<b>動力伝達の機構</b>です。学習指導要領の解説（技術・家庭編 p.42）は、動力伝達の機構として「ベルトとプーリなどの摩擦を利用して動力を伝える機構」「歯車などのかみ合いを利用して動力を伝える機構」「カム機構などの目的とする動きに変換して動力を伝える機構」を挙げています。また p.45 では、課題の解決策を具体化するときに、繰り返し試行錯誤できる実験装置や「ＩＣＴを活用したシミュレーション等を用いて試行・試作させることも考えられる」としています。歯車のかみ合いは<a href="../gears/">歯車シミュレーター</a>で試せます。</p>
<h2>授業での使い方</h2>
<ul>
<li><b>導入</b>：自転車・洗濯機・自動車など身の回りの機械で、回転がどのように伝えられているかを考えます。「ベルトとプーリ」の画面で、原動プーリと従動プーリの赤い印（●）が何回まわったかを数え、回転数の比を予想してから確かめます。</li>
<li><b>展開</b>：直径の組み合わせを変えて、速度伝達比と回転数を表に記録し、「直径の比」と「回転数の比」の関係をまとめます。「十字掛けにする」で回る向きが逆になることも確かめます。「カム機構」の画面では、3つの形のカムで従動節の動きのグラフをくらべ、「30°だけ回す」で角度ごとの高さを読み取ります。プーリやカムは指でドラッグして手で回せます。</li>
<li><b>まとめ</b>：「ゆっくり強く回したい」「ものを決まった間かくで持ち上げたい」など、製作の課題に合う機構を選び、理由を説明します（解説 p.45 の試行・試作）。</li>
</ul>
<p>生徒への問いの例：</p>
<ol>
<li>原動プーリの直径が20mm、従動プーリの直径が60mmです。速度伝達比はいくつでしょう。原動プーリが1分間に1,200回転するとき、従動プーリは1分間に何回転するでしょう。（答え：速度伝達比 3、400回転）</li>
<li>原動プーリと従動プーリを逆向きに回したいとき、ベルトの掛け方をどうすればよいでしょう。</li>
<li>従動節を「しばらく止めておき、ときどきすばやく上下させたい」とき、どの形のカムを使えばよいでしょう。</li>
</ol>
<h2>しくみ・解説</h2>
<h3>動力を伝える3つのしくみ</h3>
''' + T([["摩擦を利用する", "ベルトとプーリ、摩擦車", "軸がはなれていても伝えられ、音が静か。大きな力がかかると、すべることがある"],
          ["かみ合いを利用する", "歯車、チェーンとスプロケット", "すべらないので、回転を正確に伝えられる"],
          ["目的の動きに変える", "カム機構など", "回転運動を、往復運動などの別の動きに変える"]],
         ["伝え方", "例", "特徴"]) + '''
<h3>速度伝達比の計算（ベルトとプーリ）</h3>
''' + N("速度伝達比 ＝ 原動プーリの回転数 ÷ 従動プーリの回転数 ＝ 従動プーリの直径 ÷ 原動プーリの直径<br>従動プーリの回転数 ＝ 原動プーリの回転数 ÷ 速度伝達比") + '''
<p>ベルトがすべらないとすると、ベルトが動く速さは、どちらのプーリのふちでも同じです。プーリのふちが1分間に進む長さは「円周（直径 × 3.14）× 回転数」なので、<b>原動プーリの直径 × 原動プーリの回転数 ＝ 従動プーリの直径 × 従動プーリの回転数</b>となり、上の式が成り立ちます。教科書では、回転数を「回転速度（単位 min<sup>-1</sup>＝1分間あたりの回転数）」と書くこともあります。</p>
''' + T([["20mm", "20mm", "1", "1,200回", "同じ速さ・同じ力"], ["20mm", "40mm", "2", "600回", "ゆっくり・トルク約2倍"],
          ["20mm", "60mm", "3", "400回", "ゆっくり・トルク約3倍"], ["20mm", "80mm", "4", "300回", "ゆっくり・トルク約4倍"],
          ["40mm", "20mm", "0.5", "2,400回", "速く・トルク約0.5倍"]],
         ["原動プーリの直径", "従動プーリの直径", "速度伝達比", "従動プーリの回転数（原動 1,200回/分のとき）", "回り方"]) + '''
<p>速度伝達比が1より大きいと、従動プーリはゆっくり回り、回す力（トルク）は大きくなります。1より小さいと速く回り、トルクは小さくなります（摩擦などによる損失を考えないとき）。速さと力の両方を同時に大きくすることはできません。</p>
<h3>ベルトの掛け方と回る向き</h3>
<p>ベルトをそのまま掛ける<b>平行掛け</b>では、原動プーリと従動プーリは<b>同じ向き</b>に回ります。ベルトを交差させて掛ける<b>十字掛け</b>（たすき掛け）では、<b>逆向き</b>に回ります。ベルトとプーリは摩擦で動力を伝えるので、大きな力がかかったり、ベルトがゆるんだりすると、すべって回転が正しく伝わらないことがあります。ベルトの張りやすり減りを点検すること（保守点検）が大切です。回転を正確に伝えたいところには、歯車やチェーン、歯の付いたベルトが使われます。</p>
<h3>カム機構</h3>
<p>カム機構は、回転するカム（<b>原動節</b>）の形にそって、<b>従動節</b>を往復運動させるしくみです。カムの回転の中心から、ふちまでの長さが場所によってちがうので、カムが回ると、ふちに当たっている従動節が上下します。カムが1回転すると、従動節は1回上下します。</p>
''' + T([["円形（偏心カム）", "なめらかに上下する（ゆっくり → 速く → ゆっくり）", "なめらかな波の形", "上下の幅 ＝ 中心のずれ（偏心量）× 2"],
          ["卵形カム", "1回転のうち半分以上は止まっていて、とがった部分が来たときだけ上下する", "平らな部分と山", "自動車のエンジンの弁（バルブ）の開け閉めなど"],
          ["ハート形カム", "一定の速さで上がり、一定の速さで下がる", "直線の山（三角の形）", "一定の速さで往復させたいところ"]],
         ["カムの形", "従動節の動き", "動きのグラフ", "メモ"]) + '''
<p>グラフの横軸はカムの回転角、縦軸は従動節の高さ（いちばん下からの高さ）です。グラフが平らなところは従動節が止まっているところ、かたむきが急なところは速く動いているところです。卵形カムでは、もとの円の部分（カムの回転の中心からの長さが同じ部分）に従動節が当たっているあいだは止まっていて、このシミュレーションの寸法では1回転の約6〜7割が止まっています。</p>
<h3>このシミュレーションで単純にしていること</h3>
<ul>
<li>ベルトはすべらず、のび縮みもしないものとしています。ベルトの厚さは考えず、プーリの直径で計算しています。</li>
<li>摩擦などによる損失は考えていません（トルクの倍率は目安です）。</li>
<li>従動節は先が細く、カムのふちの1点に当たるものとしています。実際の機械には、先にローラーが付いたものや、平らな面で当たるものもあり、動きが少しちがいます。</li>
<li>偏心カムは円板の半径40mm、卵形カムは大きい円の半径30mm・小さい円の半径12mm、ハート形カムはいちばん短い半径22mmで描いています。</li>
<li>アニメーションは選んだ回転数どおりの速さで動きます（1分間に30回転なら、2秒で1回転）。</li>
</ul>
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「中学校学習指導要領（平成29年告示）解説 技術・家庭編」技術分野 C エネルギー変換の技術（p.42 動力伝達の機構、p.45 ICTを活用したシミュレーション）（<a href="''' + MEXT_CHU + '''" target="_blank" rel="noopener">文部科学省 中学校学習指導要領解説のページ</a>）</li>
<li>中学校 技術・家庭（技術分野）の教科書（開隆堂出版、東京書籍、教育図書）の「エネルギー変換の技術」の章</li>
<li>日本機械学会「機械工学辞典」クロス掛けベルト伝動（<a href="''' + JSME_CROSS + '''" target="_blank" rel="noopener">日本機械学会のページ</a>）</li>
</ul>
'''

KAMU_FAQS = [
    ("速度伝達比はどうやって求めますか？", "速度伝達比 ＝ 原動プーリの回転数 ÷ 従動プーリの回転数 ＝ 従動プーリの直径 ÷ 原動プーリの直径 で求めます。原動プーリ20mm・従動プーリ60mmなら、60÷20＝3です。原動プーリが1分間に1,200回転すると、従動プーリは1,200÷3＝400回転します。"),
    ("従動プーリを原動プーリより速く回すには、どうすればよいですか？", "従動プーリの直径を、原動プーリより小さくします（速度伝達比が1より小さくなります）。そのかわり、回す力（トルク）は小さくなります。"),
    ("十字掛けにすると、なぜ回る向きが逆になるのですか？", "ベルトを交差させると、原動プーリの上側を動くベルトが、従動プーリでは下側に回りこむためです。平行掛けでは同じ向き、十字掛け（たすき掛け）では逆向きに回ります。"),
    ("カム機構の原動節と従動節とは何ですか？", "カム機構で、回転して動きをつくり出すカムを原動節、カムに当たって動かされる部分を従動節といいます。カム機構は、カムの回転運動を、従動節の往復運動などに変えるしくみです。"),
    ("円形の偏心カム・卵形カム・ハート形カムでは、動きはどうちがいますか？", "偏心カムは、なめらかに上下します（上下の幅は中心のずれの2倍）。卵形カムは、1回転のうち半分以上は止まっていて、とがった部分が来たときだけ上下します。ハート形カムは、一定の速さで上がり、一定の速さで下がります。"),
    ("ベルトとプーリは、歯車とくらべてどんなところがちがいますか？", "ベルトとプーリは摩擦で動力を伝えるので、軸がはなれていても伝えられ、音が静かですが、大きな力がかかるとすべることがあります。歯車はかみ合いで伝えるので、すべらず回転を正確に伝えられます。"),
]

KAMU_JS = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const h1=document.querySelector('.sim-head h1'); if(h1&&!h1.children.length){ const t=h1.textContent, i=t.indexOf('（'); if(i>0){ h1.textContent=t.slice(0,i); const sp=document.createElement('span'); sp.style.display='inline-block'; sp.textContent=t.slice(i); h1.appendChild(sp); } }
  let mode='P', run=true, cross=false, thA=-Math.PI/2, thB=-Math.PI/2, turnA=0, turnB=0, beltS=0, thC=0, grab=null, lastAng=0, wasRun=true;
  let cacheKey='', SAMP=[], RMIN=0, RMAX=0, STROKE=0;
  const bar=document.createElement('div'); bar.className='lab-btns'; bar.style.marginTop='0';
  ['tP','tC'].forEach((id)=>{ const b=$(id); if(b) bar.appendChild(b); });
  cv.parentNode.insertBefore(bar,cv);
  cv.parentNode.style.gridTemplateColumns='minmax(0,1fr)';
  const fld=(id)=>$(id).closest('.field');
  function setK(id,s){ const e=$(id); if(e&&e.previousElementSibling) e.previousElementSibling.textContent=s; }
  function setV(id,s){ const e=$(id); if(!e) return; e.textContent=s; e.style.fontSize=s.length>10?'14px':(s.length>7?'16px':''); }
  function rrect(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
  function txt(t,x,y,size,col,weight,align,maxW,halo){ ctx.textAlign=align||'left'; let s=size; ctx.font=(weight||'')+' '+s+'px sans-serif';
    if(maxW){ while(ctx.measureText(t).width>maxW&&s>8){ s-=0.5; ctx.font=(weight||'')+' '+s+'px sans-serif'; } }
    if(halo){ ctx.lineWidth=3.5; ctx.strokeStyle='rgba(255,255,255,.92)'; ctx.lineJoin='round'; ctx.strokeText(t,x,y); }
    ctx.fillStyle=col||'#0f172a'; ctx.fillText(t,x,y); }
  function dot(x,y,r,c){ ctx.fillStyle=c; ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.fill(); }
  function poly(pts,w,c,dash){ ctx.strokeStyle=c; ctx.lineWidth=w; ctx.lineJoin='round'; ctx.lineCap='round'; if(dash) ctx.setLineDash(dash); ctx.beginPath(); pts.forEach((p,i)=>{ if(i) ctx.lineTo(p[0],p[1]); else ctx.moveTo(p[0],p[1]); }); ctx.stroke(); if(dash) ctx.setLineDash([]); }
  function mkPath(pts){ const cum=[0]; for(let i=1;i<pts.length;i++) cum.push(cum[i-1]+Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1])); return {pts:pts,cum:cum,len:cum[cum.length-1]}; }
  function at(P,d){ d=clamp(d,0,P.len); let lo=0,hi=P.cum.length-1; while(hi-lo>1){ const m=(lo+hi)>>1; if(P.cum[m]<=d) lo=m; else hi=m; }
    const sg=(P.cum[hi]-P.cum[lo])||1, f=(d-P.cum[lo])/sg, a=P.pts[lo], b=P.pts[hi]; return [a[0]+(b[0]-a[0])*f, a[1]+(b[1]-a[1])*f]; }
  const wrapPi=(a)=>{ while(a>Math.PI) a-=2*Math.PI; while(a<-Math.PI) a+=2*Math.PI; return a; };
  function fmtN(v){ const r=Math.round(v*100)/100; return (Math.abs(v-r)<1e-9?'':'約')+r; }
  function arrowHead(x,y,tx2,ty2,col){ ctx.fillStyle=col; ctx.beginPath(); ctx.moveTo(x+tx2*9,y+ty2*9); ctx.lineTo(x-tx2*2-ty2*5,y-ty2*2+tx2*5); ctx.lineTo(x-tx2*2+ty2*5,y-ty2*2-tx2*5); ctx.closePath(); ctx.fill(); }
  function rarrow(cx,cy,R,a0,a1,dir,col){ ctx.strokeStyle=col; ctx.lineWidth=2.5; ctx.beginPath(); ctx.arc(cx,cy,R,a0,a1); ctx.stroke(); const ae=dir>0?a1:a0; arrowHead(cx+R*Math.cos(ae),cy+R*Math.sin(ae),-Math.sin(ae)*dir,Math.cos(ae)*dir,col); }

  // ================= ベルトとプーリ
  const AX=172, BX=468, PY=168, KS=1.9;
  function PV(){ const d1=+$('d1').value, d2=+$('d2').value, n1=+$('n1').value; return {d1:d1,d2:d2,n1:n1,i:d2/d1,n2:n1*d1/d2,r1:d1/2*KS,r2:d2/2*KS}; }
  function beltPath(r1,r2,cr){ const d=BX-AX, ph=Math.acos(clamp((cr?(r1+r2):(r1-r2))/d,-1,1)), pts=[];
    const arc=(cx,r,a0,a1,n)=>{ for(let k=0;k<=n;k++){ const a=a0+(a1-a0)*k/n; pts.push([cx+r*Math.cos(a),PY+r*Math.sin(a)]); } };
    arc(AX,r1,ph,2*Math.PI-ph,72); if(cr) arc(BX,r2,Math.PI-ph,-Math.PI+ph,72); else arc(BX,r2,-ph,ph,72); pts.push(pts[0].slice()); return mkPath(pts); }
  function rotP(dA){ const v=PV(); thA+=dA; const dB=dA*v.d1/v.d2; thB+=cross?-dB:dB; turnA+=dA/(2*Math.PI); turnB+=dB/(2*Math.PI); beltS+=dA*v.r1; }
  function pulley(cx,r,th,fill,edge){ ctx.fillStyle=fill; ctx.beginPath(); ctx.arc(cx,PY,r-2,0,Math.PI*2); ctx.fill(); ctx.strokeStyle=edge; ctx.lineWidth=2; ctx.stroke();
    ctx.globalAlpha=0.45; ctx.lineWidth=1; ctx.beginPath(); ctx.arc(cx,PY,Math.max(9,r*0.62),0,Math.PI*2); ctx.stroke(); ctx.globalAlpha=1;
    const hub=Math.min(9,r*0.35); ctx.lineWidth=3; ctx.strokeStyle=edge; for(let k=0;k<4;k++){ const a=th+k*Math.PI/2; ctx.beginPath(); ctx.moveTo(cx+hub*Math.cos(a),PY+hub*Math.sin(a)); ctx.lineTo(cx+(r-5)*Math.cos(a),PY+(r-5)*Math.sin(a)); ctx.stroke(); }
    const mr=Math.max(r*0.68,r-12); dot(cx+mr*Math.cos(th),PY+mr*Math.sin(th),Math.max(3.5,Math.min(6,r*0.12)),'#dc2626'); dot(cx,PY,hub,'#334155'); dot(cx,PY,2.5,'#f8fafc'); }
  function drawP(){ const v=PV(), BP=beltPath(v.r1,v.r2,cross);
    txt('原動プーリ（モーターなどで回す） → ベルト → 従動プーリ',14,22,12.5,'#475569','bold','left',612);
    pulley(AX,v.r1,thA,'#dbeafe','#1d4ed8'); pulley(BX,v.r2,thB,'#ffedd5','#c2410c');
    poly(BP.pts,7,'#1f2937'); const n=Math.max(6,Math.floor(BP.len/26));
    for(let k=0;k<n;k++){ const s=((beltS+k*BP.len/n)%BP.len+BP.len)%BP.len, q=at(BP,s); dot(q[0],q[1],2.2,'#fbbf24'); }
    rarrow(AX,PY,v.r1+15,-Math.PI*0.72,-Math.PI*0.28,1,'#1d4ed8'); rarrow(BX,PY,v.r2+15,-Math.PI*0.72,-Math.PI*0.28,cross?-1:1,'#c2410c');
    txt('時計回り',AX,PY-v.r1-24,11,'#1d4ed8','bold','center'); txt(cross?'反時計回り':'時計回り',BX,PY-v.r2-24,11,'#c2410c','bold','center');
    txt('原動プーリ（直径'+v.d1+'mm）',AX,292,13.5,'#1d4ed8','bold','center',280); txt('従動プーリ（直径'+v.d2+'mm）',BX,292,13.5,'#c2410c','bold','center',280);
    txt('回った数 '+Math.abs(turnA).toFixed(1)+'回転',AX,310,12,'#334155','','center'); txt('回った数 '+Math.abs(turnB).toFixed(1)+'回転',BX,310,12,'#334155','','center');
    const nice=Math.abs(v.i*100-Math.round(v.i*100))<1e-9;
    txt('速度伝達比 ＝ 従動プーリの直径 ÷ 原動プーリの直径 ＝ '+v.d2+' ÷ '+v.d1+' ＝ '+fmtN(v.i),14,338,14,'#0f172a','bold','left',612);
    txt('従動プーリの回転数 ＝ 原動プーリの回転数 ÷ 速度伝達比 ＝ '+v.n1+' ÷ '+(nice?String(Math.round(v.i*100)/100):'（'+v.d2+' ÷ '+v.d1+'）')+' ＝ '+fmtN(v.n2)+'回/分',14,360,13,'#334155','','left',612);
    txt('回る向き：'+(cross?'逆向き（十字掛け）':'同じ向き（平行掛け）')+'　　回す力（トルク）：約'+(Math.round(v.i*100)/100)+'倍'+(v.i>1?'（ゆっくり・強く）':v.i<1?'（速く・弱く）':'（変わらない）')+'　※損失は考えない',14,382,12.5,'#334155','','left',612);
    txt('赤い●が回った数を数えてみよう。プーリは指でドラッグして手で回せます',14,400,11,'#64748b','','left',612); }

  // ================= カム機構
  const OX=150, OY=262, KC=1.9, GX0=364, GX1=622, GY0=46, GY1=250;
  const SHAPE={ecc:'円形（偏心カム）',egg:'卵形カム',heart:'ハート形カム'};
  function CP(){ const sh=$('shape').value; return {sh:sh,p:+$(sh).value}; }
  function camR(phi,c){ const a=((phi%(2*Math.PI))+3*Math.PI)%(2*Math.PI)-Math.PI;
    if(c.sh==='ecc'){ const R=40, e=c.p; return e*Math.cos(a)+Math.sqrt(R*R-e*e*Math.sin(a)*Math.sin(a)); }
    if(c.sh==='heart') return 22+c.p*(1-Math.abs(a)/Math.PI);
    const R0=30, rs=12, cc=R0+c.p-rs, al=Math.acos((R0-rs)/cc), be=Math.atan2(rs*Math.sin(al),cc+rs*Math.cos(al)), b=Math.abs(a);
    if(b>=al) return R0; if(b>=be) return R0/Math.cos(b-al); return cc*Math.cos(b)+Math.sqrt(Math.max(0,rs*rs-cc*cc*Math.sin(b)*Math.sin(b))); }
  function eggDwell(p){ const R0=30, rs=12, cc=R0+p-rs, al=Math.acos((R0-rs)/cc); return 1-al/Math.PI; }
  function prep(){ const c=CP(), key=c.sh+c.p; if(key===cacheKey) return; cacheKey=key; SAMP=[]; let mn=1e9, mx=-1e9;
    for(let k=0;k<=720;k++){ const r=camR(Math.PI-k/720*2*Math.PI,c); SAMP.push(r); mn=Math.min(mn,r); mx=Math.max(mx,r); } RMIN=mn; RMAX=mx; STROKE=mx-mn; }
  function motionText(c){ if(c.sh==='ecc') return 'なめらかに上下'; if(c.sh==='egg') return '約'+Math.round(eggDwell(c.p)*100)+'%は止まる'; return '一定の速さで上下'; }
  function drawC(){ prep(); const c=CP(), rpm=+$('cr').value, th=thC, rUp=camR(Math.PI-th,c), disp=rUp-RMIN, deg=((th*180/Math.PI)%360+360)%360;
    // カム
    ctx.beginPath(); for(let k=0;k<=240;k++){ const ph=k/240*2*Math.PI, r=camR(ph,c)*KC, ps=ph+th-1.5*Math.PI, x=OX+r*Math.cos(ps), y=OY+r*Math.sin(ps); if(k) ctx.lineTo(x,y); else ctx.moveTo(x,y); }
    ctx.closePath(); ctx.fillStyle='#e2e8f0'; ctx.fill(); ctx.strokeStyle='#475569'; ctx.lineWidth=2.5; ctx.stroke();
    const p0=th-1.5*Math.PI;
    if(c.sh==='ecc'){ const ex=OX+c.p*KC*Math.cos(p0), ey=OY+c.p*KC*Math.sin(p0); poly([[OX,OY],[ex,ey]],1.5,'#dc2626',[3,3]); poly([[ex-6,ey],[ex+6,ey]],2,'#dc2626'); poly([[ex,ey-6],[ex,ey+6]],2,'#dc2626');
      txt('＋＝円板の中心（回転の中心から'+c.p+'mmずれている）',10,398,10.5,'#b91c1c','bold','left',300); }
    if(c.sh==='egg'){ ctx.strokeStyle='rgba(71,85,105,.45)'; ctx.setLineDash([4,4]); ctx.lineWidth=1.2; ctx.beginPath(); ctx.arc(OX,OY,30*KC,0,Math.PI*2); ctx.stroke(); ctx.setLineDash([]);
      txt('点線＝もとの円（ここに当たっている間は止まる）',10,398,10.5,'#475569','bold','left',300); }
    if(c.sh==='heart') txt('いちばん短い半径22mm → 長い半径'+(22+c.p)+'mm（半回転で一定に増える）',10,398,10.5,'#475569','bold','left',300);
    dot(OX+camR(0,c)*KC*0.72*Math.cos(p0),OY+camR(0,c)*KC*0.72*Math.sin(p0),4,'#dc2626');
    dot(OX,OY,8,'#334155'); dot(OX,OY,2.5,'#f8fafc');
    rarrow(OX,OY,RMAX*KC+13,Math.PI*0.82,Math.PI*1.18,1,'#0e7490');
    txt('カム',14,146,13.5,'#0e7490','bold','left',0,true); txt('（原動節）',14,162,11.5,'#0e7490','bold','left',0,true); txt('時計回りに回る',14,178,10.5,'#475569','','left',0,true);
    // 従動節
    const tipY=OY-rUp*KC; ctx.fillStyle='#cbd5e1'; rrect(OX-24,126,15,14,3); ctx.fill(); rrect(OX+9,126,15,14,3); ctx.fill(); ctx.strokeStyle='#64748b'; ctx.lineWidth=1; rrect(OX-24,126,15,14,3); ctx.stroke(); rrect(OX+9,126,15,14,3); ctx.stroke();
    poly([[OX,tipY-6],[OX,tipY-116]],9,'#64748b'); poly([[OX,tipY-6],[OX,tipY-116]],5,'#cbd5e1'); dot(OX,tipY-4,5,'#475569');
    ctx.fillStyle='#475569'; rrect(OX-20,tipY-123,40,7,3); ctx.fill();
    txt('従動節',OX+14,tipY-64,13,'#0f172a','bold','left',0,true); txt('ガイド',OX-28,138,10,'#64748b','','right');
    // 目盛り（いちばん下からの高さ）
    const y0=OY-RMIN*KC-123; poly([[218,y0],[218,y0-30*KC]],1.5,'#94a3b8');
    for(let mm=0;mm<=30;mm+=5){ const y=y0-mm*KC; poly([[214,y],[mm%10?218:222,y]],1.2,'#94a3b8'); if(mm%10===0) txt(mm+'',226,y+4,10,'#64748b','','left'); }
    poly([[OX+20,tipY-120],[214,tipY-120]],1,'#0e7490',[3,3]); ctx.fillStyle='#0e7490'; ctx.beginPath(); ctx.moveTo(216,tipY-120); ctx.lineTo(209,tipY-124); ctx.lineTo(209,tipY-116); ctx.closePath(); ctx.fill();
    txt('mm',226,y0-30*KC-8,10,'#64748b','','left');
    // グラフ
    txt('従動節の動き（グラフ）',330,24,13.5,'#0f172a','bold','left');
    for(let mm=0;mm<=30;mm+=10){ const y=GY1-mm/32*(GY1-GY0); poly([[GX0,y],[GX1,y]],1,'#e5e7eb'); txt(mm+'',GX0-6,y+4,10.5,'#64748b','','right'); }
    for(let dg=0;dg<=360;dg+=90){ const x=GX0+dg/360*(GX1-GX0); poly([[x,GY0],[x,GY1]],1,'#f1f5f9'); txt(dg+'°',x,GY1+16,10.5,'#64748b','','center'); }
    ctx.save(); ctx.translate(334,(GY0+GY1)/2); ctx.rotate(-Math.PI/2); txt('従動節の高さ（mm）',0,0,11,'#475569','bold','center'); ctx.restore();
    txt('カムの回転角',(GX0+GX1)/2,GY1+32,11,'#475569','bold','center');
    const gy=(r)=>GY1-(r-RMIN)/32*(GY1-GY0), gx=(k)=>GX0+k/720*(GX1-GX0);
    if(c.sh==='egg'){ ctx.fillStyle='rgba(34,197,94,.12)'; let k0=-1; for(let k=0;k<=720;k++){ const flat=SAMP[k]-RMIN<1e-6; if(flat&&k0<0) k0=k; if((!flat||k===720)&&k0>=0){ const k1=flat?k:k-1; if(k1>k0) ctx.fillRect(gx(k0),GY0,gx(k1)-gx(k0),GY1-GY0); k0=-1; } }
      txt('止まっている',gx(360),GY0+16,11,'#15803d','bold','center'); }
    poly(SAMP.map((r,k)=>[gx(k),gy(r)]),2,'#cbd5e1');
    const kc=Math.round(deg/360*720); if(kc>0) poly(SAMP.slice(0,kc+1).map((r,k)=>[gx(k),gy(r)]),3,'#0e7490');
    poly([[gx(kc),GY0],[gx(kc),GY1]],1.2,'#0e7490',[3,3]); dot(gx(kc),gy(SAMP[kc]),5,'#dc2626');
    txt('上下の幅 '+(Math.round(STROKE*10)/10)+'mm',GX1,GY0+(c.sh==='egg'?34:14),12,'#b91c1c','bold','right',0,true);
    // 説明
    const lines=c.sh==='ecc'?['なめらかに上下する（ゆっくり → 速く → ゆっくり）','上下の幅 ＝ 中心のずれ（偏心量）'+c.p+'mm × 2 ＝ '+(2*c.p)+'mm']
      :c.sh==='egg'?['1回転のうち約'+Math.round(eggDwell(c.p)*100)+'%は止まり、とがった部分で上下','例：自動車のエンジンの弁（バルブ）の開け閉め']
      :['一定の速さで上がり、一定の速さで下がる','グラフが直線になる（等速の往復運動）'];
    txt(SHAPE[c.sh],330,304,14.5,'#0f172a','bold','left',300);
    txt(lines[0],330,324,12.5,'#334155','','left',300); txt(lines[1],330,343,12,'#334155','','left',300);
    txt('カム1回転で従動節は1回上下（1分間に'+rpm+'回）',330,362,12,'#334155','','left',300);
    txt('回転角 '+Math.round(deg)+'°　いまの高さ '+disp.toFixed(1)+'mm',330,382,12,'#0e7490','bold','left',300);
    txt('カムを指でドラッグすると手で回せます。グラフをタップするとその角度に回ります',330,398,10,'#64748b','','left',300); }

  // ================= 切りかえ・数値
  function update(){
    if(mode==='P'){ const v=PV(); ['速度伝達比','原動プーリの回転数','従動プーリの回転数','回る向き'].forEach((t,i)=>setK('s'+(i+1),t));
      setV('s1',fmtN(v.i)); setV('s2',v.n1+'回/分'); setV('s3',fmtN(v.n2)+'回/分'); setV('s4',cross?'逆向き':'同じ向き');
      setShare('【ベルトとプーリ】原動プーリ'+v.d1+'mm・従動プーリ'+v.d2+'mmで速度伝達比'+fmtN(v.i)+'。原動'+v.n1+'回/分 → 従動'+fmtN(v.n2)+'回/分（'+(cross?'十字掛けで逆向き':'平行掛けで同じ向き')+'）｜シミュラボ'); }
    else { prep(); const c=CP(); ['カムの形','カム（原動節）の回転数','従動節の上下の幅','従動節の動き方'].forEach((t,i)=>setK('s'+(i+1),t));
      setV('s1',SHAPE[c.sh]); setV('s2',(+$('cr').value)+'回/分'); setV('s3',(Math.round(STROKE*10)/10)+'mm'); setV('s4',motionText(c));
      setShare('【カム機構】'+SHAPE[c.sh]+'で、従動節は'+(Math.round(STROKE*10)/10)+'mm上下し、'+(c.sh==='ecc'?'なめらかに上下する':c.sh==='egg'?'1回転の約'+Math.round(eggDwell(c.p)*100)+'%は止まっている':'一定の速さで上がって下がる')+'。カム1回転で1往復｜シミュラボ'); } }
  const HASH={P:'pulley',C:'cam'};
  function setMode(m){ mode=m; grab=null;
    [['tP','P'],['tC','C']].forEach((a)=>{ const b=$(a[0]); b.className='btn '+(a[1]===m?'btn-primary':'btn-ghost'); b.setAttribute('aria-pressed',a[1]===m?'true':'false'); });
    ['d1','d2','n1'].forEach((id)=>{ fld(id).style.display=m==='P'?'':'none'; });
    fld('shape').style.display=m==='C'?'':'none'; fld('cr').style.display=m==='C'?'':'none';
    ['ecc','egg','heart'].forEach((id)=>{ fld(id).style.display=(m==='C'&&$('shape').value===id)?'':'none'; });
    ['crossB','count0'].forEach((id)=>{ $(id).style.display=m==='P'?'':'none'; }); ['step','home'].forEach((id)=>{ $(id).style.display=m==='C'?'':'none'; });
    run=true; $('pause').textContent='⏸ 一時停止';
    try{ history.replaceState(null,'',location.pathname+location.search+'#'+HASH[m]); }catch(e){}
    update(); }
  ['d1','d2','n1','cr','ecc','egg','heart'].forEach((id)=>$(id).addEventListener('input',update));
  $('shape').addEventListener('change',()=>{ setMode('C'); });
  $('tP').addEventListener('click',()=>setMode('P')); $('tC').addEventListener('click',()=>setMode('C'));
  $('pause').addEventListener('click',()=>{ run=!run; $('pause').textContent=run?'⏸ 一時停止':'▶ 再生'; });
  $('crossB').addEventListener('click',()=>{ cross=!cross; $('crossB').textContent=cross?'＝ 平行掛けにする':'✖ 十字掛けにする'; update(); });
  $('count0').addEventListener('click',()=>{ turnA=0; turnB=0; thA=-Math.PI/2; thB=-Math.PI/2; });
  $('step').addEventListener('click',()=>{ thC+=Math.PI/6; run=false; $('pause').textContent='▶ 再生'; });
  $('home').addEventListener('click',()=>{ thC=0; run=false; $('pause').textContent='▶ 再生'; });
  function angAt(x,y){ return mode==='P'?Math.atan2(y-PY,x-(grab==='A'?AX:BX)):Math.atan2(y-OY,x-OX); }
  cv.addEventListener('pointerdown',(e)=>{ const p=cpos(cv,e), x=p[0]/dpr, y=p[1]/dpr;
    if(mode==='P'){ const v=PV(); if(Math.hypot(x-AX,y-PY)<=v.r1+10) grab='A'; else if(Math.hypot(x-BX,y-PY)<=v.r2+10) grab='B'; else grab=null; }
    else { prep(); if(Math.hypot(x-OX,y-OY)<=RMAX*KC+12) grab='C'; else if(x>=GX0-4&&x<=GX1+4&&y>=GY0-10&&y<=GY1+24){ const r=Math.floor(thC/(2*Math.PI)); thC=r*2*Math.PI+clamp((x-GX0)/(GX1-GX0),0,1)*2*Math.PI; run=false; $('pause').textContent='▶ 再生'; grab='G'; } else grab=null; }
    if(grab){ e.preventDefault(); try{ cv.setPointerCapture(e.pointerId); }catch(er){} if(grab!=='G'){ wasRun=run; run=false; lastAng=angAt(x,y); } } });
  cv.addEventListener('pointermove',(e)=>{ if(!grab) return; const p=cpos(cv,e), x=p[0]/dpr, y=p[1]/dpr;
    if(grab==='G'){ const r=Math.floor(thC/(2*Math.PI)); thC=r*2*Math.PI+clamp((x-GX0)/(GX1-GX0),0,0.9999)*2*Math.PI; return; }
    const a=angAt(x,y), d=wrapPi(a-lastAng); lastAng=a;
    if(grab==='A') rotP(d); else if(grab==='B'){ const v=PV(); rotP(d*v.d2/v.d1*(cross?-1:1)); } else if(grab==='C') thC+=d; });
  const endGrab=()=>{ if(grab&&grab!=='G'){ run=wasRun; $('pause').textContent=run?'⏸ 一時停止':'▶ 再生'; } grab=null; };
  cv.addEventListener('pointerup',endGrab); cv.addEventListener('pointercancel',endGrab);
  function draw(){ ctx.fillStyle='#ffffff'; ctx.fillRect(0,0,W,H); if(mode==='P') drawP(); else drawC(); }
  let last=performance.now();
  function loop(now){ const dt=Math.min(0.05,Math.max(0,(now-last)/1000)); last=now;
    if(run){ if(mode==='P') rotP(2*Math.PI*(+$('n1').value)/60*dt); else thC+=2*Math.PI*(+$('cr').value)/60*dt; }
    draw(); requestAnimationFrame(loop); }
  const h0=(location.hash||'').replace('#','');
  setMode(h0==='cam'?'C':'P'); draw(); requestAnimationFrame(loop);
'''

sim(slug="kamu-pulley", cat="rika", emoji="🔩", score=74,
    title="カムとベルト・プーリのシミュレーター（動力伝達の機構）",
    title_tag="カム機構・ベルトとプーリのシミュレーター｜速度伝達比と回転数、カムの形と従動節の動き（中学 技術 動力伝達）",
    meta_desc="中学 技術・家庭（技術分野）「エネルギー変換の技術」の動力伝達の機構をブラウザで試せます。ベルトとプーリは直径で速度伝達比と回転数が変わり、十字掛けで回る向きが逆に。カム機構は円形（偏心）・卵形・ハート形で従動節の動きをグラフで比べられます。",
    og_title="カムとベルト・プーリのシミュレーター（動力伝達の機構）",
    og_desc="プーリの直径で速度伝達比と回転数が変わる。カムの形で従動節の動きが変わる。中学技術の動力伝達を動かして確かめる。",
    card_desc="プーリの直径で回転数と速度伝達比が変わる。カムの形で従動節の動きが変わる。中学技術の動力伝達。",
    lead="原動プーリと従動プーリの直径を変えると、回転数と速度伝達比が変わります。カムの形を変えると、従動節の上下の動き方が変わります（動きのグラフつき）。",
    model="中学 技術 動力伝達の機構（ベルトとプーリ・カム）", level="中学校（技術・家庭 技術分野）",
    unit="中学校 技術・家庭（技術分野）C エネルギー変換の技術（1）ア",
    canvas=canvas(640, 410, light=True),
    controls=slider("d1", "原動プーリの直径", 20, 100, 40, 10, "{v}mm") + slider("d2", "従動プーリの直径", 20, 100, 80, 10, "{v}mm")
             + slider("n1", "原動プーリの回転数", 10, 120, 30, 10, "{v}回/分")
             + select("shape", "カムの形", [("ecc", "円形（偏心カム）"), ("egg", "卵形カム"), ("heart", "ハート形カム")])
             + slider("ecc", "中心のずれ（偏心量）", 5, 15, 10, 1, "{v}mm") + slider("egg", "とがった部分の高さ", 10, 30, 20, 2, "{v}mm")
             + slider("heart", "半径の差（最大−最小）", 10, 30, 20, 2, "{v}mm") + slider("cr", "カムの回転数", 6, 60, 20, 2, "{v}回/分"),
    buttons=btn("tP", "🔁 ベルトとプーリ", True) + btn("tC", "🥚 カム機構")
            + btn("pause", "⏸ 一時停止") + btn("crossB", "✖ 十字掛けにする") + btn("count0", "↺ 回った数を0にする")
            + btn("step", "↻ 30°だけ回す") + btn("home", "↺ 最初の位置へ"),
    stats=stats([("s1", "速度伝達比", True), ("s2", "原動プーリの回転数", False), ("s3", "従動プーリの回転数", False), ("s4", "回る向き", False)]),
    legend="ベルトとプーリ：青＝原動プーリ、オレンジ＝従動プーリ。赤い●で回った数を数えられます。ベルトはすべらないものとしています。カム機構：グラフの横軸はカムの回転角、縦軸は従動節のいちばん下からの高さです。プーリとカムは指でドラッグして回せます。",
    article=KAMU_ARTICLE, faqs=KAMU_FAQS,
    rel=[("gears", "⚙️", "歯車シミュレーター"), ("teko-tsuriai", "⚖️", "てこのつり合いシミュレーター"),
         ("denki-kairo", "🔌", "電気回路シミュレーター（直列・並列・オームの法則）"), ("solar-hatsuden", "🔋", "今日のソーラー発電シミュ")],
    js=KAMU_JS)
