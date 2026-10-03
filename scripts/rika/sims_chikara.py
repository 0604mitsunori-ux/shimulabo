# -*- coding: utf-8 -*-
"""理科の授業向け：力・運動（小6 てこの規則性／小5 振り子の運動）"""
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

MEXT_URL = "https://www.mext.go.jp/a_menu/shotou/new-cs/1387014.htm"
HINT_STYLE = ("grid-column:1/-1;background:#fffbeb;border:1px solid #fde68a;border-radius:10px;"
              "padding:10px 14px;font-size:15px;line-height:1.7;color:#1f2937;text-align:left;")

# ============================================================ 1 てこのつり合い
sim(slug="teko-tsuriai", cat="rika", emoji="⚖️", score=80,
    title="てこのつり合いシミュレーター",
    title_tag="てこの原理・てこのつり合いシミュレーター｜小6理科 実験用てこで「重さ×きょり」のきまりを確かめる",
    meta_desc="小6理科「てこの規則性」の実験用てこを画面で再現。左右の目盛りをタップして10gのおもりをつるすと、てこが左右どちらにかたむくか、水平につり合うかがアニメで分かります。てこの原理（重さ×支点からのきょり）の計算、ヒント、練習問題つき。",
    og_title="てこのつり合いシミュレーター（小6 てこの規則性）",
    og_desc="目盛りをタップしておもりをつるし、てこがつり合うきまり「重さ×支点からのきょり」を確かめる。",
    card_desc="目盛りをタップしておもりをつるし、てこがつり合うきまり（重さ×きょり）を見つける。ヒント・問題つき。",
    lead="実験用てこの左右の目盛りをタップして、10gのおもりをつるしたり、はずしたりできます。てこがどちらにかたむくか、水平につり合うのはどんなときかを、「おもりの重さ×支点からのきょり」で確かめましょう。",
    model="小6 てこの規則性", level="小学6年", unit="小学校 第6学年 A（3）てこの規則性",
    canvas=canvas(640, 480, light=True),
    controls="",
    buttons=btn("quiz", "🎯 もんだいを出す", True) + btn("hintBtn", "💡 ヒントをかくす") + btn("clear", "ぜんぶはずす"),
    stats=stats([("sL", "左のうでをかたむけるはたらき", False), ("sR", "右のうでをかたむけるはたらき", False), ("sRes", "結果", True)])
          + '<div id="hint" style="' + HINT_STYLE + '">目盛りの上の「+」をタップして、おもりをつるしてみよう。</div>',
    legend="目盛りの上の「+」をタップすると10gのおもりを1こつるし、おもりをタップすると1こはずします（1つの目盛りに100gまで）。青＝左のうで、オレンジ＝右のうで。棒の重さは左右で同じなので、計算には入れていません。",
    article="<h2>このシミュレーションでわかること</h2>\n" + P("てこが水平につり合うのは、<b>左のうでをかたむけるはたらき</b>と<b>右のうでをかたむけるはたらき</b>が等しいときです。てこをかたむけるはたらきは「<b>おもりの重さ×支点からのきょり</b>」で表せます。") + '''
<p>小学校6年の理科「てこの規則性」（学習指導要領 第6学年 A（3））で学ぶ内容です。実験用てこの目盛りにおもりをつるし、てこがどちらにかたむくか、どうすれば水平につり合うかを、何度でも試せます。一般に「てこの原理」とよばれるきまりを、自分の手で確かめられます。</p>
<h2>授業での使い方</h2>
<ul>
<li><b>導入</b>：左の目盛りにおもりをつるした画面を見せ、「右のどこに何gつるせば水平になるかな？」と予想させます。</li>
<li><b>展開</b>：実験用てこを使った実験の前後に使います。左のおもりはそのままにして、右の「きょり」と「重さ」の組み合わせを表に整理すると、「重さ×きょり」のきまりが見つかります（算数の「比例と反比例」ともつながります）。「もんだいを出す」ボタンで、くり返し練習もできます。</li>
<li><b>まとめ</b>：はさみ・くぎぬき・せんぬき・ピンセットなど、身の回りの道具の支点・力点・作用点を確かめます。</li>
</ul>
<p>児童への問いの例：</p>
<ol>
<li>左の3の目盛りに20gをつるしました。右の6の目盛りに何gつるすと、水平につり合うでしょう。</li>
<li>左のおもりはそのままで、右のおもりを支点から遠くへ動かすと、てこはどうなるでしょう。</li>
<li>くぎぬきで、柄のはしを持つと小さな力でくぎがぬけるのはなぜでしょう。</li>
</ol>
<h2>しくみ・解説</h2>
<h3>てこをかたむけるはたらき</h3>
''' + N("てこをかたむけるはたらき ＝ おもりの重さ（g）× 支点からのきょり（目盛りの数）<br>左のはたらき ＝ 右のはたらき のとき、てこは水平につり合います。") + '''
<p>2か所以上におもりをつるしたときは、それぞれの「重さ×きょり」をたし合わせます。たとえば左の6に10g、左の2に20gをつるしたときは、10×6＋20×2＝100 が左のうでをかたむけるはたらきです。</p>
<h3>計算問題の解き方</h3>
<p>例：左の4の目盛りに30gをつるしました。右の6の目盛りに何gつるすと、つり合いますか。</p>
<ol>
<li>左のはたらきを計算します：30×4＝120</li>
<li>右のはたらきも120になればよいので：□×6＝120</li>
<li>□＝120÷6＝20　答え 20g</li>
</ol>
<p>右の目盛りを変えると、つり合うおもりの重さは次のようになります。きょりが2倍になると、必要な重さは半分になります。</p>
''' + T([["1", "120g（このシミュレーションでは1か所100gまで）", "120×1＝120"], ["2", "60g", "60×2＝120"], ["3", "40g", "40×3＝120"],
          ["4", "30g", "30×4＝120"], ["5", "24g（10gのおもりでは作れない）", "24×5＝120"], ["6", "20g", "20×6＝120"]],
         ["右の目盛り（きょり）", "つり合うおもりの重さ", "右のはたらき"]) + '''
<h3>身の回りのてこ</h3>
<p>てこには、てこを支えるところ（<b>支点</b>）、力を加えるところ（<b>力点</b>）、ものに力がはたらくところ（<b>作用点</b>）があります。</p>
''' + T([["はさみ", "刃をとめているねじ", "指を入れる持ち手", "紙を切る刃", "支点が真ん中"],
          ["くぎぬき", "板にあたっているところ", "手で持つ柄のはし", "くぎをはさむところ", "支点が真ん中"],
          ["せんぬき", "王冠の上にあたる先", "手で持つところ", "王冠のふちにかかるところ", "作用点が真ん中"],
          ["ピンセット", "2本がつながった根もと", "指でおさえるところ", "ものをはさむ先", "力点が真ん中"]],
         ["道具", "支点", "力点", "作用点", "ならび方"]) + '''
<p>支点が真ん中の道具や、作用点が真ん中の道具は、支点から力点までのきょりを長くすると、小さな力で大きな力を出せます。ピンセットのように力点が真ん中の道具は、作用点にはたらく力が小さくなるので、小さなものや、こわれやすいものをやさしくつまむのに向いています。</p>
<h3>このシミュレーションで単純にしていること</h3>
<ul>
<li>棒（てこ）の重さは計算に入れていません。支点が棒の真ん中にあるので、棒の重さは左右で同じになり、つり合いには関係しないからです。</li>
<li>おもりは1こ10gで、1つの目盛りに100g（10こ）までつるせます。</li>
<li>わかりやすくするため、てこのかたむきは12°で止まるようにしています。</li>
<li>高校の物理では、この「重さ×きょり」を「力のモーメント」という考え方で学びます。</li>
</ul>
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「小学校学習指導要領（平成29年告示）解説 理科編」第6学年 A（3）てこの規則性（<a href="''' + MEXT_URL + '''" target="_blank" rel="noopener">文部科学省 学習指導要領解説のページ</a>）</li>
<li>小学校理科の教科書（東京書籍「新しい理科」、啓林館「わくわく理科」、大日本図書「たのしい理科」など）6年の「てこ」の単元</li>
</ul>
''',
    faqs=[("てこが水平につり合うのは、どんなときですか？", "左のうでをかたむけるはたらき（おもりの重さ×支点からのきょり）と、右のうでをかたむけるはたらきが等しいときです。たとえば、左の6の目盛りに10g（10×6＝60）、右の3の目盛りに20g（20×3＝60）をつるすと、水平につり合います。"),
          ("「てこの原理」とは何ですか？", "支点からのきょりが長いところに力を加えるほど、小さな力でものを動かせる、というてこのきまりを指す言葉です。小学校6年の理科では「てこの規則性」として、「おもりの重さ×支点からのきょり」が左右で等しいときにつり合うことを学びます。"),
          ("おもりを2か所以上につるしたときは、どう計算しますか？", "それぞれの目盛りで「重さ×きょり」を計算し、たし合わせます。左の6に10gと左の2に20gなら、10×6＋20×2＝100 が左のうでをかたむけるはたらきです。"),
          ("支点・力点・作用点のならび方で、道具はどう分けられますか？", "はさみやくぎぬきは支点が真ん中、せんぬきは作用点が真ん中、ピンセットは力点が真ん中にあります。支点から力点までのきょりが、支点から作用点までのきょりより長いと、小さな力で大きな力を出せます。"),
          ("上皿てんびんがつり合うのはなぜですか？", "上皿てんびんは、支点から左右の皿までのきょりが同じになっています。そのため、左右にのせたものの重さが等しいときに、てこをかたむけるはたらきも等しくなり、水平につり合います。"),
          ("重いものを小さな力で持ち上げるには、どうすればよいですか？", "支点から力点までのきょりを長く（力点を支点から遠く）して、支点から作用点までのきょりを短く（作用点を支点に近く）します。")],
    rel=[("gears", "⚙️", "歯車シミュレーター"), ("pendulum-wave", "🎐", "振り子の波"), ("newtons-cradle", "🟤", "ニュートンのゆりかご"), ("gravity", "🌌", "重力シミュレーター")],
    js=r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const CX=W/2, CY=190, SP=44, ARM=292, MAXA=12*Math.PI/180, CAP=10, BW=26, BH=11, BG=2, BASE_Y=H-74;
  const L=[0,0,0,0,0,0,0], R=[0,0,0,0,0,0,0];
  const COL={L:'#2563eb', Lf:'#bfdbfe', R:'#ea580c', Rf:'#fed7aa'};
  let ang=0, vel=0, hover=null, showHint=true, quiz=null, msg='', msgT=0;
  const statBox=document.querySelector('.lab-stats'), hintBox=$('hint');
  if(statBox && hintBox){ hintBox.style.gridColumn=''; hintBox.style.width='100%'; hintBox.style.maxWidth='640px'; hintBox.style.boxSizing='border-box'; statBox.after(hintBox);
    const fsSt=document.createElement('style'); fsSt.textContent='.panel:fullscreen #hint,.panel:-webkit-full-screen #hint{max-width:min(96vw,1100px)!important;}'; document.head.appendChild(fsSt); }
  function sum(a){ let s=0; for(let d=1;d<=6;d++) s+=a[d]*10*d; return s; }
  function terms(a){ const t=[]; for(let d=1;d<=6;d++) if(a[d]) t.push(a[d]*10+'×'+d); return t; }
  function pos(side,d){ return (side<0?'左':'右')+'の'+d; }
  function place(side,d){ const u=side*d*SP, c=Math.cos(ang), s=Math.sin(ang); return [CX+u*c-7*s, CY+u*s+7*c]; }
  function hit(x,y){ for(const side of [-1,1]){ const a=side<0?L:R; for(let d=1;d<=6;d++){ const p=place(side,d); if(Math.abs(x-p[0])>SP/2) continue;
        const top=p[1]+10, bot=top+a[d]*(BH+BG)+18;
        if(a[d]>0 && y>=top-4 && y<=bot) return {side:side,d:d,op:-1};
        if(y>=p[1]-82 && y<(a[d]>0?top-4:p[1]+44)) return {side:side,d:d,op:1}; } }
    return null; }
  function rr(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
  function fitText(t,x,y,maxW,size,weight){ let s=size; ctx.font=weight+' '+s+'px sans-serif'; while(ctx.measureText(t).width>maxW && s>10){ s--; ctx.font=weight+' '+s+'px sans-serif'; } ctx.fillText(t,x,y); }
  function solve2(k,A){ let best=null;
    for(let d1=6;d1>=2;d1--) for(let n1=1;n1<=CAP-A[d1];n1++){ const rest=k-n1*d1; if(rest<=0) break;
      for(let d2=d1-1;d2>=1;d2--){ if(rest%d2===0){ const n2=rest/d2; if(n2<=CAP-A[d2] && (!best||n1+n2<best[4])) best=[d1,n1,d2,n2,n1+n2]; } } }
    return best; }
  function hintHTML(l,r){
    let q=''; if(quiz) q='<div style="margin-bottom:6px">🎯 <b>もんだい</b>：'+quiz.text+'</div>';
    if(quiz && quiz.solved && l===r) return q+'<div style="color:#15803d">🎉 <b>せいかい！</b> 左 '+terms(L).join('＋')+'＝'+l+'、右 '+terms(R).join('＋')+'＝'+r+' で、はたらきが等しくなりました。「もんだいを出す」で次の問題へ。</div>';
    if(l===0 && r===0) return q+'目盛りの上の「+」をタップして、おもりをつるしてみよう。';
    if(l===r) return q+'✓ <b>水平につり合っています。</b> 左のはたらき '+l+' ＝ 右のはたらき '+r;
    const heavy=l>r?-1:1, light=-heavy, diff=Math.abs(l-r), A=light<0?L:R, HV=heavy<0?L:R, k=diff/10;
    const hs=heavy<0?'左':'右', ls=light<0?'左':'右';
    let txt=hs+'のはたらきのほうが <b>'+diff+'</b> 大きいので、'+hs+'にかたむきます。';
    if(!showHint) return q+txt+'<br>💡 ヒントはかくしています（「ヒントを見る」でひょうじ）。';
    const ops=[]; for(let d=6;d>=1;d--){ if(k%d===0 && k/d<=CAP-A[d]) ops.push([d,k/d*10]); }
    txt+='<br>💡 つり合わせるには：';
    if(ops.length){ txt+='<b>'+pos(light,ops[0][0])+'の目盛りに '+ops[0][1]+'g</b> をつるす'; if(ops.length>1) txt+='（'+ops.slice(1,3).map(o=>pos(light,o[0])+'に'+o[1]+'g').join('、')+' でもOK）'; }
    else { const two=solve2(k,A); if(two) txt+='<b>'+pos(light,two[0])+'に'+two[1]*10+'g と '+pos(light,two[2])+'に'+two[3]*10+'g</b> をつるす'; else txt+=ls+'のはたらきを、あと '+diff+' 大きくする'; }
    const rem=[]; for(let d=6;d>=1;d--){ if(k%d===0 && k/d<=HV[d]) rem.push([d,k/d*10]); }
    if(rem.length) txt+='<br>または、'+pos(heavy,rem[0][0])+'の目盛りから '+rem[0][1]+'g はずしても、つり合います。';
    return q+txt; }
  function update(){ const l=sum(L), r=sum(R);
    if(quiz && l===r && l>0) quiz.solved=true;
    setStat('sL', String(l)); setStat('sR', String(r));
    const res=l===r?(l===0?'おもりなし':'水平につり合う'):(l>r?'左にかたむく':'右にかたむく'); setStat('sRes', res);
    $('hint').innerHTML=hintHTML(l,r);
    const fl=terms(L).join('＋')||'0', fr=terms(R).join('＋')||'0';
    setShare('【てこのつり合い】左 '+fl+'＝'+l+'、右 '+fr+'＝'+r+' → '+res+'。てこをかたむけるはたらき＝おもりの重さ×支点からのきょり｜シミュラボ'); }
  function newQuiz(){ let ok=false;
    for(let tries=0;tries<300&&!ok;tries++){ L.fill(0); R.fill(0); const m=Math.random()<0.6?1:2;
      for(let i=0;i<m;i++){ const d=1+Math.floor(Math.random()*6), n=1+Math.floor(Math.random()*6); L[d]=Math.min(CAP,L[d]+n); }
      const k=sum(L)/10; for(let d=2;d<=6;d++) if(k%d===0 && k/d<=CAP) ok=true; }
    const desc=[]; for(let d=1;d<=6;d++) if(L[d]) desc.push('左の'+d+'の目盛りに'+L[d]*10+'g');
    quiz={text:desc.join('と、')+'がつるしてあります。右のうでの どこかに おもりをつるして、水平につり合わせよう。', solved:false};
    showHint=false; $('hintBtn').textContent='💡 ヒントを見る'; update(); }
  function step(dt){ const l=sum(L), r=sum(R); const tg=l>r?-MAXA:(l<r?MAXA:0);
    const acc=34*(tg-ang)-6*vel; vel+=acc*dt; ang+=vel*dt;
    if(ang>MAXA){ ang=MAXA; vel=-0.25*vel; } if(ang<-MAXA){ ang=-MAXA; vel=-0.25*vel; }
    if(msgT>0) msgT-=dt; }
  function draw(){ const l=sum(L), r=sum(R); const c=Math.cos(ang), s=Math.sin(ang);
    ctx.fillStyle='#ffffff'; ctx.fillRect(0,0,W,H);
    ctx.textAlign='left'; ctx.fillStyle='#64748b'; fitText('てこをかたむけるはたらき ＝ おもりの重さ(g) × 支点からのきょり(目盛り)', 14, 20, W-28, 13, '');
    ctx.fillStyle=COL.L; fitText('左：'+(terms(L).join(' ＋ ')||'おもりなし')+' ＝ '+l, 14, 44, W-28, 18, 'bold');
    ctx.fillStyle=COL.R; fitText('右：'+(terms(R).join(' ＋ ')||'おもりなし')+' ＝ '+r, 14, 68, W-28, 18, 'bold');
    ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1; ctx.setLineDash([6,6]); ctx.beginPath(); ctx.moveTo(16,CY); ctx.lineTo(W-16,CY); ctx.stroke(); ctx.setLineDash([]);
    ctx.fillStyle='#94a3b8'; rr(CX-110,BASE_Y,220,12,4); ctx.fill(); ctx.fillStyle='#b6c0cd'; ctx.fillRect(CX-5,CY,10,BASE_Y-CY);
    ctx.save(); ctx.translate(CX,CY); ctx.rotate(ang);
    ctx.fillStyle='#e2e8f0'; ctx.strokeStyle='#64748b'; ctx.lineWidth=1.5; rr(-ARM,-7,ARM*2,14,4); ctx.fill(); ctx.stroke();
    ctx.strokeStyle='#475569'; for(let d=1;d<=6;d++) for(const sd of [-1,1]){ const u=sd*d*SP; ctx.beginPath(); ctx.moveTo(u,-7); ctx.lineTo(u,7); ctx.stroke(); }
    ctx.restore();
    ctx.fillStyle='#334155'; ctx.beginPath(); ctx.arc(CX,CY,8,0,Math.PI*2); ctx.fill(); ctx.fillStyle='#fff'; ctx.beginPath(); ctx.arc(CX,CY,3,0,Math.PI*2); ctx.fill();
    ctx.fillStyle='#334155'; ctx.font='bold 13px sans-serif'; ctx.textAlign='left'; ctx.fillText('支点', CX+12, CY+32);
    for(const side of [-1,1]){ const a=side<0?L:R, fc=side<0?COL.Lf:COL.Rf, sc=side<0?COL.L:COL.R;
      for(let d=1;d<=6;d++){ const u=side*d*SP, tx=CX+u*c+7*s, ty=CY+u*s-7*c; const hv=hover&&hover.side===side&&hover.d===d;
        ctx.textAlign='center'; ctx.fillStyle='#334155'; ctx.font='bold 14px sans-serif'; ctx.fillText(String(d), tx, ty-8);
        const on=hv&&hover.op>0; ctx.beginPath(); ctx.arc(tx,ty-36,11,0,Math.PI*2); ctx.fillStyle=on?sc:'#f1f5f9'; ctx.fill(); ctx.strokeStyle=on?sc:'#cbd5e1'; ctx.lineWidth=1; ctx.stroke();
        ctx.fillStyle=on?'#fff':'#94a3b8'; ctx.font='bold 16px sans-serif'; ctx.fillText('+', tx, ty-30);
        const p=place(side,d); ctx.strokeStyle='#64748b'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.arc(p[0],p[1]+3,3,0,Math.PI*2); ctx.stroke();
        const n=a[d]; if(!n) continue;
        ctx.beginPath(); ctx.moveTo(p[0],p[1]+6); ctx.lineTo(p[0],p[1]+10); ctx.stroke();
        for(let i=0;i<n;i++){ const y=p[1]+10+i*(BH+BG); ctx.fillStyle=fc; ctx.strokeStyle=sc; ctx.lineWidth=1.2; rr(p[0]-BW/2,y,BW,BH,3); ctx.fill(); ctx.stroke(); }
        const yb=p[1]+10+n*(BH+BG);
        if(hv&&hover.op<0){ ctx.strokeStyle=sc; ctx.lineWidth=2; ctx.setLineDash([4,3]); rr(p[0]-BW/2-4,p[1]+6,BW+8,yb-p[1]-4,5); ctx.stroke(); ctx.setLineDash([]); }
        ctx.fillStyle=sc; ctx.font='bold 12px sans-serif'; ctx.fillText(n*10+'g', p[0], yb+12); } }
    if(quiz && quiz.solved && l===r){ ctx.fillStyle='#16a34a'; rr(CX-95,86,190,36,18); ctx.fill(); ctx.fillStyle='#fff'; ctx.font='bold 19px sans-serif'; ctx.textAlign='center'; ctx.fillText('せいかい！🎉', CX, 111); }
    else if(msgT>0){ ctx.fillStyle='#f59e0b'; rr(CX-150,86,300,34,17); ctx.fill(); ctx.fillStyle='#fff'; ctx.font='bold 15px sans-serif'; ctx.textAlign='center'; ctx.fillText(msg, CX, 108); }
    ctx.textAlign='center'; ctx.fillStyle='#64748b'; fitText('「+」や目盛りの上をタップ → おもりを1こ（10g）つるす　／　おもりをタップ → 1こはずす', CX, H-42, W-24, 13, '');
    ctx.font='bold 22px sans-serif'; ctx.fillStyle=l===r?(l?'#15803d':'#64748b'):(l>r?COL.L:COL.R);
    ctx.fillText(l>r?'◀ 左にかたむく':(l<r?'右にかたむく ▶':(l?'✓ 水平につり合っている':'目盛りをタップして、おもりをつるそう')), CX, H-12); }
  cv.addEventListener('pointerdown',(e)=>{ const pp=cpos(cv,e); const h=hit(pp[0]/dpr,pp[1]/dpr); if(!h) return; e.preventDefault(); const a=h.side<0?L:R;
    if(h.op>0){ if(a[h.d]<CAP) a[h.d]++; else { msg='1つの目盛りには100gまでです'; msgT=1.8; } } else if(a[h.d]>0) a[h.d]--;
    update(); });
  cv.addEventListener('pointermove',(e)=>{ if(e.pointerType!=='mouse') return; const pp=cpos(cv,e); hover=hit(pp[0]/dpr,pp[1]/dpr); cv.style.cursor=hover?'pointer':'default'; });
  cv.addEventListener('pointerleave',()=>{ hover=null; });
  $('quiz').addEventListener('click',newQuiz);
  $('hintBtn').addEventListener('click',()=>{ showHint=!showHint; $('hintBtn').textContent=showHint?'💡 ヒントをかくす':'💡 ヒントを見る'; update(); });
  $('clear').addEventListener('click',()=>{ L.fill(0); R.fill(0); quiz=null; update(); });
  L[4]=3; update();
  let last=performance.now();
  function loop(now){ const dt=Math.min(0.05,Math.max(0,(now-last)/1000)); last=now; step(dt); draw(); requestAnimationFrame(loop); }
  draw(); requestAnimationFrame(loop);
''')

# ============================================================ 2 振り子の実験
import math
def _r2(v): return math.floor(v * 100 + 0.5) / 100          # JS の Math.round(v*100)/100 と同じ丸め
def _t10(cm): return _r2(10 * 2 * math.pi * math.sqrt(cm / 100 / 9.8))
FURIKO_TABLE = T([["%dcm" % c, "%.2f秒" % _t10(c), "%.2f秒" % _r2(_t10(c) / 10)] for c in (10, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90, 100)],
                 ["振り子の長さ", "10往復の時間", "1往復の時間（10往復÷10）"])

FURIKO_ARTICLE = "<h2>このシミュレーションでわかること</h2>\n" + P("振り子が1往復する時間は、<b>振り子の長さによって変わり、おもりの重さや振れ幅によっては変わりません</b>（振れ幅が大きすぎないとき）。振り子が長いほど、1往復にかかる時間は長くなります。") + '''
<p>小学校5年の理科「振り子の運動」（学習指導要領 第5学年 A（2））で学ぶ内容です。変える条件を1つだけにして、ほかの条件は同じにする「条件をそろえた調べ方」の練習にも使えます。</p>
<h2>授業での使い方</h2>
<ul>
<li><b>導入</b>：ブランコやメトロノームを思い出させ、「振り子が1往復する時間は、何によって変わるのだろう」と問いかけます。糸の長さ・おもりの重さ・振れ幅の3つについて予想を立てます。</li>
<li><b>展開</b>：実験の計画を立てるときに使います。条件を変えると、前の記録とくらべて「変えた条件が1つだけか」が表示されます。「手で計ったときのずれ」を「あり」にして同じ条件で3回計ると、毎回少しずつちがう時間になり、平均をとる意味がわかります。実物の実験の前の練習や、実験のあとの確かめにも使えます。</li>
<li><b>まとめ</b>：記録表から「1往復の時間を変えるのは振り子の長さだけ」であることを確かめます。発展として、長さを4倍（25cm→100cm）にすると、1往復の時間がおよそ2倍（約1.0秒→約2.0秒）になることも見つけられます。振り子の長さで速さを調節する、メトロノームのものづくりにもつなげられます。</li>
</ul>
<p>児童への問いの例：</p>
<ol>
<li>おもりを重くすると、1往復の時間は長くなるでしょうか、短くなるでしょうか。</li>
<li>1往復の時間を長くするには、どの条件をどう変えればよいでしょう。</li>
<li>1往復ではなく、10往復の時間を計って10でわるのはなぜでしょう。</li>
</ol>
<h2>しくみ・解説</h2>
<h3>1往復と振り子の長さ</h3>
<p><b>1往復</b>は、おもりが手をはなした所から反対側まで行き、また元の所にもどってくるまでです。<b>振り子の長さ</b>は、糸をつるした所（支点）から、おもりの中心までの長さです。</p>
<h3>10往復の時間から1往復の時間を求める</h3>
''' + N("1往復の時間 ＝ 10往復の時間 ÷ 10<br>例：10往復が14.19秒なら、14.19÷10＝1.419 → 約1.42秒") + '''
<p>1往復は1〜2秒くらいと短いので、ストップウォッチをおすタイミングのずれ（0.2秒くらい）が大きく効いてしまいます。10往復の時間を計って10でわると、ずれも10分の1になります。さらに、同じ条件で3回計って<b>平均</b>をとると、より正しい時間になります。</p>
<p>例：14.1秒、14.3秒、14.2秒 → 平均は（14.1＋14.3＋14.2）÷3＝14.2秒 → 1往復は 14.2÷10＝1.42秒</p>
<h3>振り子の長さと1往復の時間（早見表）</h3>
''' + FURIKO_TABLE + '''
<p>このシミュレーションでは、高校の物理で学ぶ単振り子の式 <b>T＝2π√(L÷g)</b>（T：1往復の時間〔秒〕、L：振り子の長さ〔m〕、g：重力加速度 9.8m/s²）で時間を計算しています。この式には、おもりの重さも振れ幅も入っていません。長さを4倍にすると、1往復の時間は2倍になります。</p>
<h3>振れ幅が大きいと、ほんの少し長くなる（高校で学ぶ内容）</h3>
<p>上の式は、振れ幅が小さいときに成り立つ式です。くわしく計算すると、振れ幅が大きいほど1往復の時間はほんの少し長くなり、振れ幅30°では約1.7%長くなります（長さ1mの振り子なら、10往復で約0.35秒）。小学校の実験くらいの振れ幅では、手で計るずれと同じくらいの小さな差なので、「振れ幅では変わらない」と考えてよいです。このシミュレーションでは、振れ幅による差は入れていません。</p>
<h3>このシミュレーションで単純にしていること・実験の注意</h3>
<ul>
<li>空気のていこうや、支点のまさつは考えていません。そのため振れ幅はへりません。実際の振り子は少しずつ振れ幅が小さくなりますが、1往復の時間はほとんど変わりません。</li>
<li>糸はのびず、糸の重さはないものとして計算しています。</li>
<li>実物の実験でおもりを重くするときは、おもりを下につなげてつるさないようにします。おもり全体の中心が下がって、振り子の長さも変わってしまうからです（このシミュレーションでは、おもりの中心の位置は変わりません）。</li>
<li>「手で計ったときのずれ」を「あり」にすると、10往復の時間に −0.2〜＋0.2秒のずれをランダムに加えます。</li>
</ul>
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「小学校学習指導要領（平成29年告示）解説 理科編」第5学年 A（2）振り子の運動（<a href="''' + MEXT_URL + '''" target="_blank" rel="noopener">文部科学省 学習指導要領解説のページ</a>）</li>
<li>小学校理科の教科書（東京書籍「新しい理科」、啓林館「わくわく理科」、大日本図書「たのしい理科」など）5年の振り子の単元</li>
<li>高等学校「物理」の教科書（単振り子の周期 T＝2π√(L/g)）</li>
</ul>
'''

FURIKO_FAQS = [
    ("振り子が1往復する時間は、何によって変わりますか？", "振り子の長さ（糸をつるした所からおもりの中心までの長さ）によって変わります。おもりの重さや振れ幅を変えても、1往復の時間はほとんど変わりません。振り子が長いほど、1往復の時間は長くなります。"),
    ("なぜ10往復の時間を計って10でわるのですか？", "1往復は1〜2秒くらいと短く、ストップウォッチをおすタイミングのずれが大きく効くからです。10往復の時間を計って10でわると、ずれの影響が10分の1になります。同じ条件で何回か計って平均をとると、さらに正確になります。"),
    ("振り子の長さは、どこからどこまでですか？", "糸をつるした所（支点）から、おもりの中心までです。おもりのはしではなく、中心までを計ることに注意しましょう。"),
    ("おもりの数をふやすとき、下につなげてはいけないのはなぜですか？", "おもりを下につなげると、おもり全体の中心が下にずれて、振り子の長さまで長くなってしまうからです。重さだけを変えたいときは、おもりを同じ所に重ねてつるし、振り子の長さを変えないようにします。"),
    ("1往復がちょうど1秒になる振り子の長さは？", "約25cm（計算では24.8cm）です。1往復が2秒になる長さは約1m（99.3cm）です。長さを4倍にすると、1往復の時間は2倍になります。"),
    ("振れ幅を大きくしても、本当に時間は変わらないのですか？", "振れ幅が小さいうちは、ほとんど変わりません。くわしく計ると、振れ幅が大きいほどほんの少し長くなり、振れ幅30°では約1.7%長くなります。これは高校の物理で学ぶ内容で、小学校の実験では手で計るずれにかくれてしまうくらいの小さな差です。"),
]

FURIKO_JS = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  const G=9.8, PX=200, PY=40, S=3.4, X0=420, PW=W-X0-14, MAXROWS=30;
  const NAMES={L:'糸の長さ', w:'おもりの重さ', a:'振れ幅'}, UN={L:'cm', w:'g', a:'°'};
  const css=document.createElement('style');
  css.textContent='.furi-tbl{width:100%;border-collapse:collapse;font-size:13.5px;font-variant-numeric:tabular-nums;background:#fff;}'
    +'.furi-tbl th{background:#ecfeff;color:#155e75;font-size:12px;padding:8px 6px;border-bottom:2px solid #0e7490;text-align:center;white-space:nowrap;}'
    +'.furi-tbl td{padding:8px 6px;border-bottom:1px solid #e5e7eb;text-align:center;white-space:nowrap;}'
    +'.furi-tbl td.chk{text-align:left;white-space:normal;min-width:170px;font-size:12.5px;line-height:1.5;}'
    +'.furi-tbl td.chg{background:#fef08a;font-weight:800;}.furi-tbl td.ok{color:#15803d;}.furi-tbl td.ng{color:#b91c1c;font-weight:700;}.furi-tbl td.em{color:#64748b;white-space:normal;}'
    +'.panel:fullscreen #hint,.panel:fullscreen #recWrap,.panel:-webkit-full-screen #hint,.panel:-webkit-full-screen #recWrap{max-width:min(96vw,1100px)!important;}';
  document.head.appendChild(css);
  const statBox=document.querySelector('.lab-stats');
  ['recWrap','hint'].forEach((id)=>{ const el=$(id); if(statBox&&el){ el.style.gridColumn=''; el.style.width='100%'; el.style.maxWidth='640px'; el.style.boxSizing='border-box'; statBox.after(el); } });
  let state='idle', t=0, T=1, meas=0, cnt=0, man=false, rows=[], lastHint='', lastRes=null, full=false;
  function cond(){ return {L:+$('len').value, w:+$('wt').value, a:+$('amp').value}; }
  function period(cm){ return 2*Math.PI*Math.sqrt(cm/100/G); }
  function r2(v){ return Math.round(v*100)/100; }
  function f2(v){ return v.toFixed(2); }
  function diffs(p,c){ return ['L','w','a'].filter((k)=>p[k]!==c[k]); }
  function rr(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
  function resetView(){ setStat('s10','0.00秒'); setStat('s1','？秒'); }
  function checkCell(r,i){ if(!r.d) return ['1回目（くらべるもとになる記録）',''];
    if(r.d.length===0){ const g=rows.slice(0,i+1).filter((x)=>x.L===r.L&&x.w===r.w&&x.a===r.a); const av=g.reduce((s,x)=>s+x.t10,0)/g.length;
      return ['同じ条件で'+g.length+'回目　平均：10往復 '+f2(r2(av))+'秒 → 1往復 '+f2(r2(av/10))+'秒','ok']; }
    if(r.d.length===1){ const k=r.d[0], p=rows[i-1]; return ['✓「'+NAMES[k]+'」だけ変えた（'+p[k]+UN[k]+'→'+r[k]+UN[k]+'）','ok']; }
    return ['⚠ '+r.d.map((k)=>'「'+NAMES[k]+'」').join('と')+'の'+r.d.length+'つを変えた → これでは、どの条件が関係しているのか分からない','ng']; }
  function renderTable(){ const tb=$('recBody');
    if(!rows.length){ tb.innerHTML='<tr><td class="em" colspan="7">まだ記録はありません。「スタート」で10往復を計ると、ここに記録されます。</td></tr>'; return; }
    tb.innerHTML=rows.map((r,i)=>{ const ck=checkCell(r,i); const ch=(k)=>(r.d&&r.d.indexOf(k)>=0)?' class="chg"':'';
      return '<tr><td>'+(i+1)+'</td><td'+ch('L')+'>'+r.L+'cm</td><td'+ch('w')+'>'+r.w+'g</td><td'+ch('a')+'>'+r.a+'°</td><td>'+f2(r.t10)+'秒'+(r.man?' ✋':'')+'</td><td><b>'+f2(r.t1)+'秒</b></td><td class="chk'+(ck[1]?' '+ck[1]:'')+'">'+ck[0]+'</td></tr>'; }).join(''); }
  function hint(){ const c=cond(); let h='';
    if(state==='run') h='⏱️ 計測中… 振り子が10往復するまで待とう（いま <b>'+cnt+'</b> 往復）。手をはなした所にもどってきたら1往復です。';
    else if(state==='done' && lastRes){ h='📝 10往復 '+f2(lastRes.t10)+'秒 ÷ 10 ＝ 1往復 <b>'+f2(lastRes.t1)+'秒</b>';
      if(full) h+='<br>⚠ 記録表がいっぱいです（30回まで）。「表を消す」で新しく始めよう。';
      else { const i=rows.length-1; h+='（記録表の'+(i+1)+'回目）<br>'+(i===0?'次は、条件を<b>1つだけ</b>変えて計ってみよう。':'条件のチェック：'+checkCell(rows[i],i)[0]); } }
    else if(!rows.length) h='① 糸の長さ・おもりの重さ・振れ幅を決めて「スタート」をおそう。振り子が10往復する時間を計ります。1回目の記録が、くらべるもとになります。';
    else { const p=rows[rows.length-1], d=diffs(p,c);
      if(d.length===0) h='前の記録（'+rows.length+'回目）と同じ条件です。もう一度計って<b>平均</b>をとると、より正しい時間がわかります。';
      else if(d.length===1) h='✓ 前の記録から<b>「'+NAMES[d[0]]+'」だけ</b>を変えています（'+p[d[0]]+UN[d[0]]+' → '+c[d[0]]+UN[d[0]]+'）。1往復の時間はどうなるかな？ 予想してからスタート！';
      else h='⚠ 前の記録から'+d.map((k)=>'「'+NAMES[k]+'」').join('と')+'の<b>'+d.length+'つ</b>を変えています。どの条件が関係しているのか分からなくなるので、<b>変える条件は1つだけ</b>にしよう。'; }
    if(h!==lastHint){ $('hint').innerHTML=h; lastHint=h; } }
  function start(){ const c=cond(); T=period(c.L); t=0; cnt=0; man=+$('err').value===1;
    const e=man?Math.round(rnd(-0.2,0.2)*100)/100:0; meas=r2(10*T+e); state='run'; full=false;
    setStat('s10','0.00秒'); setStat('s1','計測中…'); $('start').textContent='▶ もう一度計る'; hint(); }
  function stop(){ state='idle'; t=0; cnt=0; resetView(); $('start').textContent='▶ スタート（10往復を計る）'; hint(); }
  function record(){ const c=cond(); const t1=r2(meas/10); lastRes={t10:meas, t1:t1};
    setStat('s10', f2(meas)+'秒'); setStat('s1', f2(t1)+'秒');
    setShare('【振り子の実験】糸の長さ'+c.L+'cm・おもり'+c.w+'g・振れ幅'+c.a+'°で、10往復'+f2(meas)+'秒 → 1往復'+f2(t1)+'秒。1往復の時間は何で変わる？｜シミュラボ');
    if(rows.length>=MAXROWS){ full=true; hint(); return; }
    const row={L:c.L, w:c.w, a:c.a, t10:meas, t1:t1, man:man}; const prev=rows.length?rows[rows.length-1]:null; row.d=prev?diffs(prev,row):null; rows.push(row);
    renderTable(); hint(); }
  function step(dt){ if(state==='idle') return; t+=dt*(+$('spd').value);
    if(state==='run'){ const n=Math.min(10,Math.floor(t/T+1e-9)); if(n!==cnt){ cnt=n; hint(); }
      setStat('s10', f2(Math.min(t,meas))+'秒');
      if(t>=Math.max(10*T,meas)){ state='done'; cnt=10; record(); } }
    if(t>1e6) t=0; }
  function draw(){ const c=cond(); const Lp=c.L*S, a0=c.a*Math.PI/180, rb=8*Math.cbrt(c.w/10);
    const th=state==='idle'?a0:a0*Math.cos(2*Math.PI*t/T);
    ctx.fillStyle='#ffffff'; ctx.fillRect(0,0,W,H);
    ctx.fillStyle='#94a3b8'; rr(PX-90,PY-20,180,10,3); ctx.fill(); ctx.fillStyle='#64748b'; ctx.fillRect(PX-6,PY-11,12,11);
    ctx.beginPath(); ctx.moveTo(PX,PY); ctx.arc(PX,PY,72,0,Math.PI); ctx.closePath(); ctx.fillStyle='rgba(14,116,144,.06)'; ctx.fill(); ctx.strokeStyle='rgba(14,116,144,.35)'; ctx.lineWidth=1; ctx.stroke();
    for(let dg=-80;dg<=80;dg+=10){ const an=Math.PI/2-dg*Math.PI/180, r1=(dg%30===0)?58:64; ctx.beginPath(); ctx.moveTo(PX+Math.cos(an)*72,PY+Math.sin(an)*72); ctx.lineTo(PX+Math.cos(an)*r1,PY+Math.sin(an)*r1); ctx.stroke(); }
    ctx.setLineDash([5,5]); ctx.strokeStyle='#cbd5e1'; ctx.beginPath(); ctx.moveTo(PX,PY); ctx.lineTo(PX,PY+Lp+rb+12); ctx.stroke();
    ctx.beginPath(); ctx.arc(PX,PY,Lp,Math.PI/2-a0,Math.PI/2+a0); ctx.stroke();
    ctx.strokeStyle='rgba(234,88,12,.6)'; ctx.beginPath(); ctx.moveTo(PX,PY); ctx.lineTo(PX+Math.sin(a0)*Lp,PY+Math.cos(a0)*Lp); ctx.stroke(); ctx.setLineDash([]);
    ctx.strokeStyle='#ea580c'; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(PX,PY,34,Math.PI/2-a0,Math.PI/2); ctx.stroke(); ctx.lineWidth=1;
    ctx.fillStyle='#c2410c'; ctx.font='bold 13px sans-serif'; ctx.textAlign='right'; ctx.fillText('振れ幅 '+c.a+'°', PX-10, PY+54);
    const bx=PX+Math.sin(th)*Lp, by=PY+Math.cos(th)*Lp;
    ctx.strokeStyle='#334155'; ctx.lineWidth=1.6; ctx.beginPath(); ctx.moveTo(PX,PY); ctx.lineTo(bx,by); ctx.stroke(); ctx.lineWidth=1;
    const gr=ctx.createRadialGradient(bx-rb*0.35,by-rb*0.35,rb*0.15,bx,by,rb); gr.addColorStop(0,'#f1f5f9'); gr.addColorStop(1,'#475569');
    ctx.fillStyle=gr; ctx.beginPath(); ctx.arc(bx,by,rb,0,Math.PI*2); ctx.fill();
    ctx.fillStyle='#0f172a'; ctx.beginPath(); ctx.arc(PX,PY,3.5,0,Math.PI*2); ctx.fill();
    ctx.fillStyle='#334155'; ctx.font='bold 12px sans-serif'; ctx.textAlign='left'; ctx.fillText(c.w+'g', bx+rb+4, by+4);
    if(state==='idle'){ const mx=PX+Math.sin(a0)*Lp*0.5+Math.cos(a0)*16, my=PY+Math.cos(a0)*Lp*0.5-Math.sin(a0)*16;
      ctx.font='bold 13px sans-serif'; const lt=c.L+'cm', lw=ctx.measureText(lt).width+12;
      ctx.fillStyle='rgba(255,255,255,0.92)'; rr(mx-2,my-11,lw,20,10); ctx.fill(); ctx.strokeStyle='#0e7490'; ctx.stroke(); ctx.fillStyle='#0e7490'; ctx.fillText(lt, mx+4, my+4);
      ctx.font='22px sans-serif'; ctx.fillText('✋', bx+rb, by-rb-2); }
    ctx.textAlign='left'; ctx.fillStyle='#475569'; ctx.font='bold 13px sans-serif'; ctx.fillText('ストップウォッチ', X0, 24);
    ctx.fillStyle='#0f172a'; rr(X0,32,PW,94,12); ctx.fill();
    const sw=state==='idle'?0:(state==='run'?Math.min(t,meas):meas);
    ctx.fillStyle=state==='run'?'#86efac':'#f8fafc'; ctx.font='bold 46px ui-monospace,Menlo,Consolas,monospace'; ctx.textAlign='right'; ctx.fillText(f2(sw), X0+PW-34, 94);
    ctx.font='bold 16px sans-serif'; ctx.fillText('秒', X0+PW-12, 94);
    ctx.textAlign='left'; ctx.font='12px sans-serif'; ctx.fillStyle='#94a3b8'; ctx.fillText(state==='run'?'● 計測中':(state==='done'?'■ ストップ':'スタートで計測'), X0+12, 116);
    ctx.fillStyle='#475569'; ctx.font='bold 13px sans-serif'; ctx.fillText('往復した回数', X0, 154);
    const nC=state==='idle'?0:(state==='done'?10:cnt);
    ctx.fillStyle='#0f172a'; ctx.font='bold 26px sans-serif'; ctx.fillText(nC+' / 10 往復', X0, 186);
    for(let i=0;i<10;i++){ ctx.fillStyle=i<nC?'#0e7490':'#e2e8f0'; rr(X0+i*PW/10,196,PW/10-3,10,3); ctx.fill(); }
    ctx.fillStyle='#475569'; ctx.font='bold 13px sans-serif'; ctx.fillText('いまの条件', X0, 238);
    const prev=rows.length?rows[rows.length-1]:null, dd=(prev&&state==='idle')?diffs(prev,c):[];
    [['L','糸の長さ',c.L+'cm'],['w','おもりの重さ',c.w+'g'],['a','振れ幅',c.a+'°']].forEach((it,i)=>{ const y=264+i*30, chg=dd.indexOf(it[0])>=0;
      if(chg){ ctx.fillStyle='#fef08a'; rr(X0-4,y-19,PW+8,27,7); ctx.fill(); }
      ctx.fillStyle='#334155'; ctx.font='14px sans-serif'; ctx.textAlign='left'; ctx.fillText((chg?'★ ':'')+it[1], X0+4, y);
      ctx.font='bold 17px sans-serif'; ctx.textAlign='right'; ctx.fillText(it[2], X0+PW-4, y); });
    if(dd.length){ ctx.textAlign='left'; ctx.font='bold 12px sans-serif'; ctx.fillStyle=dd.length===1?'#15803d':'#b91c1c'; ctx.fillText(dd.length===1?'★＝前の記録から変えた条件（1つ）':'★＝変えた条件が'+dd.length+'つ（1つにしよう）', X0, 352); }
    ctx.textAlign='center';
    if(state==='done' && lastRes){ ctx.fillStyle='#c2410c'; ctx.font='bold 18px sans-serif'; ctx.fillText('10往復 '+f2(lastRes.t10)+'秒 ÷ 10 ＝ 1往復 '+f2(lastRes.t1)+'秒', W/2, H-14); }
    else if(state==='run'){ ctx.fillStyle='#0e7490'; ctx.font='bold 15px sans-serif'; ctx.fillText('手をはなした所にもどってきたら「1往復」', W/2, H-14); }
    else { ctx.fillStyle='#64748b'; ctx.font='bold 15px sans-serif'; ctx.fillText('「スタート」で手をはなし、10往復する時間を計ります', W/2, H-14); } }
  ['len','wt','amp'].forEach((id)=>$(id).addEventListener('input',()=>{ if(state!=='idle') stop(); else hint(); }));
  $('err').addEventListener('change',()=>{ if(state!=='run') hint(); });
  $('start').addEventListener('click',start);
  $('stop').addEventListener('click',stop);
  $('clearTbl').addEventListener('click',()=>{ if(rows.length && !window.confirm('記録表をすべて消しますか？')) return; rows=[]; full=false; renderTable(); if(state==='done') stop(); else hint(); });
  $('copyTbl').addEventListener('click',async()=>{ const head=['回','糸の長さ(cm)','おもりの重さ(g)','振れ幅(°)','10往復の時間(秒)','1往復の時間(秒)','条件のチェック'];
    const txt=[head.join('\t')].concat(rows.map((r,i)=>[i+1,r.L,r.w,r.a,f2(r.t10),f2(r.t1),checkCell(r,i)[0]].join('\t'))).join('\n');
    let ok=false; try{ await navigator.clipboard.writeText(txt); ok=true; }catch(e){ const ta=document.createElement('textarea'); ta.value=txt; document.body.appendChild(ta); ta.select(); try{ ok=document.execCommand('copy'); }catch(e2){ ok=false; } ta.remove(); }
    $('copyTbl').textContent=ok?'コピーしました ✓':'コピーできませんでした'; setTimeout(()=>{ $('copyTbl').textContent='表をコピー'; },1600); });
  resetView(); renderTable(); hint();
  setShare('【振り子の実験】1往復の時間は「糸の長さ」「おもりの重さ」「振れ幅」のどれで変わる？ 条件を1つずつ変えて10往復の時間を計ろう｜シミュラボ');
  let last=performance.now();
  function loop(now){ const dt=Math.min(0.05,Math.max(0,(now-last)/1000)); last=now; step(dt); draw(); requestAnimationFrame(loop); }
  draw(); requestAnimationFrame(loop);
'''

sim(slug="furiko-jikken", cat="rika", emoji="⏱️", score=76,
    title="振り子の実験シミュレーター（1往復の時間を調べよう）",
    title_tag="振り子の実験シミュレーター｜振り子の周期（1往復の時間）は何で決まる？小5理科 振り子の運動",
    meta_desc="小5理科「振り子の運動」の実験をブラウザで再現。糸の長さ・おもりの重さ・振れ幅を変えてスタートすると、10往復の時間を自動で計り、1往復の時間（振り子の周期）を記録表にまとめます。変える条件が1つだけかのチェックや、手で計ったときのずれも試せます。",
    og_title="振り子の実験シミュレーター（1往復の時間を調べよう）",
    og_desc="糸の長さ・おもりの重さ・振れ幅を1つずつ変えて10往復の時間を計測。振り子の1往復の時間は何で決まる？",
    card_desc="糸の長さ・おもりの重さ・振れ幅を1つずつ変えて10往復を計測。1往復の時間は何で変わる？",
    lead="糸の長さ・おもりの重さ・振れ幅を決めて「スタート」をおすと、振り子が10往復する時間をストップウォッチで自動で計ります。結果は記録表にたまっていき、「変える条件は1つだけ」になっているかもチェックできます。",
    model="小5 振り子の運動", level="小学5年", unit="小学校 第5学年 A（2）振り子の運動",
    canvas=canvas(640, 440, light=True),
    controls=slider("len", "糸の長さ（振り子の長さ）", 10, 100, 50, 5, "{v}cm") + slider("wt", "おもりの重さ", 10, 50, 10, 10, "{v}g")
           + slider("amp", "振れ幅", 10, 30, 20, 5, "{v}°")
           + select("err", "手で計ったときのずれ", [("0", "なし（ぴったり計る）"), ("1", "あり（±0.2秒くらい）")])
           + select("spd", "早送り", [("1", "なし（実際の速さ）"), ("2", "2倍の速さ"), ("4", "4倍の速さ")]),
    buttons=btn("start", "▶ スタート（10往復を計る）", True) + btn("stop", "■ 止める") + btn("clearTbl", "表を消す") + btn("copyTbl", "表をコピー"),
    stats=stats([("s10", "10往復の時間", False), ("s1", "1往復の時間（10往復÷10）", True)])
          + '<div id="hint" style="' + HINT_STYLE + '">① 糸の長さ・おもりの重さ・振れ幅を決めて「スタート」をおそう。</div>'
          + '<div id="recWrap" style="grid-column:1/-1;overflow-x:auto;-webkit-overflow-scrolling:touch;text-align:left;">'
          + '<div style="font-weight:800;font-size:13px;color:#155e75;margin:2px 0 6px;">📋 記録表（10往復を計るたびに追加されます）</div>'
          + '<table class="furi-tbl"><thead><tr><th>回</th><th>糸の長さ</th><th>おもりの重さ</th><th>振れ幅</th><th>10往復の時間</th><th>1往復の時間</th><th>条件のチェック</th></tr></thead>'
          + '<tbody id="recBody"><tr><td colspan="7">まだ記録はありません。</td></tr></tbody></table></div>',
    legend="振り子の長さは、糸をつるした所（支点）からおもりの中心までです。「早送り」にしても、ストップウォッチは実際の時間で計ります。✋＝「手で計ったときのずれ：あり」で計った記録。空気のていこうは考えていないので、振れ幅はへりません。",
    article=FURIKO_ARTICLE, faqs=FURIKO_FAQS,
    rel=[("pendulum-wave", "🎐", "振り子の波"), ("newtons-cradle", "🟤", "ニュートンのゆりかご"), ("reaction-test", "⚡", "反応速度テスト"), ("building-quake", "🏢", "地震でビルはどう揺れる？")],
    js=FURIKO_JS)
