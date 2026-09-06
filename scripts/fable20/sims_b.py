# -*- coding: utf-8 -*-
"""Fable20 B: エコーチェンバー・流行曲線・多数決の罠・満員電車・時差出勤"""
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

# ============================================================ 6 エコーチェンバー
sim(slug="echo-chamber", cat="wonder", emoji="📢", score=69,
    title="エコーチェンバー 意見分極シミュレーター", model="限定信頼モデル（ヘーゲルマン＝クラウゼ／デフアン）",
    model_note="Hegselmann & Krause (2002)、Deffuant et al. (2000)。計算社会科学の意見動学",
    title_tag="エコーチェンバー 意見分極シミュレーター｜「似た意見しか聞かない」だけで社会はいくつに割れる？",
    meta_desc="「自分と近い意見の人の話しか聞かない」というルールだけで、バラバラだった意見が2つ3つの極に固まる過程をアニメで見る無料シミュレーター。許容幅・SNSのおすすめ強度・頑固な人の割合を変えて、分極が起きる条件を体感。",
    og_title="エコーチェンバー 意見分極シミュレーター", og_desc="似た意見しか聞かないだけで、社会はいくつに割れる？",
    card_desc="「近い意見しか聞かない」だけで、バラバラの意見が2〜3の極に固まる。分極が起きる条件を探る。",
    lead="最初は意見がバラバラの100人。「自分と近い意見の人の話だけ聞いて、少し歩み寄る」を繰り返すと、社会はいくつの“極”に割れるのか。聞く耳の広さ・SNSのおすすめ・頑固な人の割合を変えて確かめてください。",
    canvas=canvas(640, 380),
    controls=slider("eps", "聞く耳の広さ（意見の差がこれ以内なら聞く）", 0.05, 0.6, 0.2, 0.01) + slider("mu", "歩み寄りの強さ", 0.1, 0.5, 0.3, 0.05)
           + slider("sns", "SNSのおすすめ強度（似た人とばかり会う）", 0, 1, 0.3, 0.05) + slider("stub", "頑固な人（両極端・意見を変えない）", 0, 20, 4, 1, "{v}%") + slider("sp", "再生速度", 1, 10, 4, 1, "×{v}"),
    buttons=btn("toggle", "⏸ 一時停止") + btn("reset", "リセット"),
    stats=stats([("sT", "経過ステップ", False), ("sK", "意見の“極”の数", True), ("sSpread", "意見のばらつき", False), ("sMid", "中道派の割合", False)]),
    legend="縦軸＝意見（上が賛成・下が反対）、横軸＝時間。1本1本の線が1人の意見の変化。線が束になる＝エコーチェンバー。",
    article=P("人は「自分と近い意見だけ聞く」傾向があります。その許容幅が広ければ社会は<b>1つの中道に合意</b>し、狭ければ<b>2つ、3つの極に分裂</b>します。悪意も操作もなしに、聞く耳の幅だけで分極が決まる——これが限定信頼モデルの結論です。") + '''
<h2>モデルのルール</h2>
<p>各人は 0（強い反対）〜1（強い賛成）の意見を持ちます。毎ステップ、誰かと出会い、意見の差が「聞く耳の広さ ε」以内なら、お互いに歩み寄ります（差の μ 倍だけ近づく）。差が ε より大きければ、相手の話は“聞こえない”。これだけです。</p>
''' + T([["ε ＞ 0.3 くらい", "全員が1つの意見に合意（コンセンサス）"], ["ε ≈ 0.2", "2つの極に分裂（分極）"], ["ε ≈ 0.1〜0.15", "3〜5個の小さな島（断片化）"], ["ε ＜ 0.05", "誰も動かず、バラバラのまま"]], ["聞く耳の広さ", "社会の行き着く先"]) + '''
<p>大まかに「極の数 ≈ 1 ÷ (2ε)」になることが知られています。聞く耳の広さがほんの少し狭まるだけで、合意が分裂に変わる境目（相転移）があります。</p>
<h2>SNSのおすすめと「頑固な人」の効果</h2>
<p><b>SNSのおすすめ強度</b>を上げると、そもそも似た意見の人としか出会わなくなり、ε が広くても分極が進みます。<b>頑固な人</b>（意見を絶対に変えない両極端の人）が数%いるだけで、周囲の人がじわじわ引き寄せられ、中道派が消えていきます。少数の“確信犯”が世論を動かす構造です。</p>
<h2>研究での使われ方</h2>
<p>限定信頼モデルは2000年代に提案され、フィルターバブル・政治的分極・ワクチン忌避・製品の口コミ形成などの研究に使われています。実際のSNSデータでは、リツイート網が政治的に2つのクラスターへ分かれる様子が繰り返し観測されており、このモデルの示す構造とよく一致します。</p>
''',
    faqs=[("極の数はどう数えている？", "意見を0.05刻みに区切り、人が集まっている区間の塊（連続した山）を数えています。頑固な人は数に含めます。"),
          ("分極を防ぐには？", "モデル上では「聞く耳の広さを少し広げる」「違う意見の人と出会う機会（SNSのおすすめを弱める）」が効きます。全員が変わる必要はなく、一部の人が広い ε を持つだけでも合意に向かいやすくなります。"),
          ("現実の人はこんなに単純？", "もちろん単純化です。ただし「近い意見にしか影響されない」という仮定は、社会心理学の実験（同化・対比効果）と整合しており、モデルの本質はよく支持されています。")],
    rel=[("uwasa-kakusan", "🗣️", "噂が全員に届くまで"), ("shinrai-shinka", "🤝", "信頼の進化"), ("tasuketsu-wana", "🗳️", "多数決の罠"), ("schelling", "🏘️", "街の分断シミュレーター")],
    js=r'''
  const cv=$('cv'), x=cv.getContext('2d'), W=cv.width, H=cv.height, NP=100;
  let op, stub, hist, t, run=true;
  function reset(){ op=Array.from({length:NP},()=>Math.random()); const ns=Math.round(NP*+$('stub').value/100); stub=new Array(NP).fill(false); for(let i=0;i<ns;i++){ stub[i]=true; op[i]=i%2?0.02:0.98; } hist=[op.slice()]; t=0; draw(); }
  function step(){ const eps=+$('eps').value, mu=+$('mu').value, sns=+$('sns').value;
    for(let m=0;m<NP;m++){ const i=Math.random()*NP|0; let j; if(Math.random()<sns){ // 似た人と会いやすい
        let best=-1,bd=9; for(let k=0;k<6;k++){ const c=Math.random()*NP|0; if(c===i) continue; const d=Math.abs(op[c]-op[i]); if(d<bd){bd=d;best=c;} } j=best<0?(i+1)%NP:best; } else { j=Math.random()*NP|0; if(j===i) continue; }
      const d=op[j]-op[i]; if(Math.abs(d)<=eps){ if(!stub[i]) op[i]+=mu*d; if(!stub[j]) op[j]-=mu*d; } }
    t++; hist.push(op.slice()); if(hist.length>300) hist.shift(); }
  function clusters(){ const bins=new Array(20).fill(0); op.forEach(v=>bins[Math.min(19,Math.floor(v*20))]++); let k=0,inn=false; bins.forEach(b=>{ if(b>=3&&!inn){k++;inn=true;} if(b<3) inn=false; }); return k; }
  function draw(){ x.fillStyle='#0b1020'; x.fillRect(0,0,W,H); const L=hist.length, PW=W-60;
    x.strokeStyle='rgba(255,255,255,.08)'; for(let g=0;g<=4;g++){ const y=10+(H-20)*g/4; x.beginPath(); x.moveTo(0,y); x.lineTo(PW,y); x.stroke(); }
    x.fillStyle='rgba(255,255,255,.4)'; x.font='11px sans-serif'; x.fillText('賛成', 4, 20); x.fillText('反対', 4, H-12);
    x.lineWidth=1; for(let i=0;i<NP;i++){ const c=op[i]; x.strokeStyle=stub[i]?'#f472b6':'hsla('+(c*200+10)+',80%,60%,.7)'; x.beginPath(); for(let k=0;k<L;k++){ const px=k/299*PW, py=10+(1-hist[k][i])*(H-20); k?x.lineTo(px,py):x.moveTo(px,py); } x.stroke(); }
    // histogram right
    const bins=new Array(20).fill(0); op.forEach(v=>bins[Math.min(19,Math.floor(v*20))]++); const mx=Math.max(...bins,1); bins.forEach((b,i)=>{ const y=10+(1-(i+1)/20)*(H-20); x.fillStyle='hsla('+((i+0.5)/20*200+10)+',80%,60%,.9)'; x.fillRect(PW+8, y, b/mx*48, (H-20)/20-1); });
    const mean=op.reduce((a,b)=>a+b,0)/NP, sd=Math.sqrt(op.reduce((a,b)=>a+(b-mean)**2,0)/NP), mid=op.filter(v=>v>0.4&&v<0.6).length, k=clusters();
    setStat('sT', t); setStat('sK', k+'個'); setStat('sSpread', sd.toFixed(2)); setStat('sMid', Math.round(mid/NP*100)+'%');
    setShare('聞く耳の広さ'+$('eps').value+'で'+t+'ステップ経過→意見の極は'+k+'個📢 中道派'+Math.round(mid/NP*100)+'%（頑固な人'+$('stub').value+'%・SNSおすすめ'+$('sns').value+'）。分極は悪意なしで起きる👇'); }
  let f=0; function loop(){ if(run){ f++; if(f%Math.max(1,11-+$('sp').value)===0) step(); } draw(); requestAnimationFrame(loop); }
  ['stub'].forEach(id=>$(id).addEventListener('change',reset));
  $('toggle').addEventListener('click',()=>{ run=!run; $('toggle').textContent=run?'⏸ 一時停止':'▶ 再生'; });
  $('reset').addEventListener('click',reset);
  reset(); loop();
''')

# ============================================================ 7 流行はなぜ急に終わる
sim(slug="ryukou-curve", cat="marketing", emoji="📈", score=68,
    title="流行はなぜ急に終わる？ 普及曲線シミュレーター", model="バス拡散モデル＋飽き（離脱）項（SIRS型）",
    model_note="Bass (1969)。新製品の普及予測に50年以上使われる標準モデル",
    title_tag="流行はなぜ急に終わる？普及曲線シミュレーター｜バスモデルで“ピーク”と“終わり”を予測",
    meta_desc="広告で知る人（イノベーター）と口コミで知る人（イミテーター）、そして飽きる人。3つの流れを式にしたバス拡散モデルで、流行の立ち上がり・ピーク・急な終わりをシミュレーション。広告費と口コミ係数でピークの時期がどう動くかを体感できる無料ツール。",
    og_title="流行はなぜ急に終わる？ 普及曲線シミュレーター", og_desc="広告・口コミ・飽きの3つの流れで、流行のピークと終わりを予測。",
    card_desc="広告で知る人・口コミで知る人・飽きる人。3つの流れで流行の山と急な終わりを再現。",
    lead="タピオカも、あのアプリも、ある日突然みんなが使い始め、そして急に誰も話題にしなくなる。「広告で知る」「口コミで知る」「飽きる」の3つの流れを式にすると、流行の山の高さと、終わりの早さが見えてきます。",
    canvas=canvas(640, 360),
    controls=slider("p", "広告の力（毎月、未経験者の何%が始めるか）", 0.1, 5, 0.5, 0.1, "{v}%") + slider("q", "口コミの力（利用者1人が月に誘う人数）", 0.05, 1.0, 0.35, 0.05, "{v}人")
           + slider("r", "飽きる速さ（毎月、利用者の何%がやめるか）", 0, 30, 8, 1, "{v}%") + slider("m", "市場の大きさ（潜在的な利用者）", 10, 1000, 100, 10, "{v}万人") + select("re", "飽きた人は", [("no", "二度と戻らない（一発屋型）"), ("yes", "しばらくして戻ることもある（定番型）")]),
    buttons=btn("run", "▶ 36ヶ月シミュレーション", True),
    stats=stats([("sPeak", "ピークの利用者数", True), ("sWhen", "ピークの時期", False), ("sTotal", "延べ経験者", False), ("sEnd", "ピークの半分以下になる月", False)]),
    legend="青＝いま使っている人、灰色＝まだ知らない人、オレンジ＝飽きた人。口コミが強いほど山は急で高く、飽きが速いほど山は細くなります。",
    article=P("流行が急に終わるのは、「口コミで増える速さ」と「飽きて減る速さ」の綱引きが、<b>まだ始めていない人が減った瞬間に逆転する</b>からです。増える側の燃料（未経験者）が尽きるのに対し、減る側は利用者の数に比例して続くため、ピークの後は落ちる一方になります。") + '''
<h2>バス拡散モデルの式</h2>
''' + N("新規利用者（今月） ＝ (p ＋ q × 利用経験者の割合) × まだ始めていない人の数<br>p：広告・自発的に知る力（イノベーション係数）　q：口コミの力（イミテーション係数）") + '''
<p>1969年にフランク・バスが提案したこのモデルは、家電・自動車・スマホ・SNS など、あらゆる新製品の普及曲線を2つの係数で驚くほどよく再現します。過去の製品では p ≈ 0.03、q ≈ 0.38 前後が典型値とされます。本シミュレーターはこれに「飽きてやめる」項を加えて、流行の“終わり”まで描いています。</p>
''' + T([["広告の力 p を上げる", "立ち上がりが早くなるが、山の高さはあまり変わらない"], ["口コミの力 q を上げる", "山が急に高くなる。しかしその分、未経験者が早く尽きて終わりも早い"], ["飽きる速さ r を上げる", "山が低く細くなる。“一発屋”の形"], ["市場を大きくする", "山が高く、時期が遅くなる（燃料が多い）"]], ["操作", "曲線の変化"]) + '''
<h2>ピークは「いつ」来るか</h2>
<p>飽きを無視した純粋なバスモデルでは、ピークは <b>t* = ln(q/p) ÷ (p+q)</b> で計算できます。p=0.5%・q=0.35なら約12ヶ月。口コミが強いほど、そして広告が弱いほどピークは遅く来ますが、来たときの山は高くなります。マーケティングでは「ピークまでに生産・在庫を間に合わせ、ピーク後に在庫を残さない」ためにこの予測が使われます。</p>
<h2>「定番」になれる条件</h2>
<p>飽きた人が戻ってこない一発屋型では、流行は必ず一度きりの山で終わります。一方、飽きた人が時間をおいて戻る定番型では、山は小さくても長く続き、一定の利用者数に落ち着きます。タピオカとコーヒーの違いは、まさに「戻る人がいるか」です。</p>
''',
    faqs=[("p と q の現実的な値は？", "研究の平均値では p≈0.03（月次換算で約0.25〜0.5%）、q≈0.38。SNSで拡散しやすい商品は q が0.5を超えることもあります。本ページの初期値はこれに合わせています。"),
          ("飽きる速さの目安は？", "ゲームアプリの月次解約率は10〜30%、サブスクの定番サービスで2〜5%とされます。r を30%にすると典型的な“1ヶ月で消えるアプリ”の曲線になります。"),
          ("このモデルで売上予測はできる？", "初期数ヶ月の実データから p と q を推定すれば、ピーク時期と最終普及率をある程度予測できます。実務では類似製品の p・q を借りる「アナロジー法」がよく使われます。")],
    rel=[("uwasa-kakusan", "🗣️", "噂が全員に届くまで"), ("buzz", "🔥", "バズ偏差値"), ("kansen-agent", "🦠", "感染はこう広がる"), ("influencer-soroban", "📱", "インフルエンサー皮算用")],
    js=r'''
  const cv=$('cv'), x=cv.getContext('2d'), W=cv.width, H=cv.height;
  function simulate(){ const p=+$('p').value/100, q=+$('q').value, r=+$('r').value/100, M=+$('m').value, back=$('re').value==='yes'; const dt=0.1;
    let S=M, I=0, R=0, cum=0; const rows=[]; for(let m=0;m<=36;m++){ rows.push({m,S,I,R}); for(let k=0;k<10;k++){ const newI=(p+q*I/M)*S*dt; const quit=r*I*dt; const ret=back?0.05*R*dt:0; S=S-newI+ret; I=I+newI-quit; R=R+quit-ret; cum+=newI; } }
    return {rows,cum}; }
  function draw(){ const {rows,cum}=simulate(); x.fillStyle='#0b1020'; x.fillRect(0,0,W,H); const M=+$('m').value; const L=48,B=H-28,PW=W-L-16,PH=B-16;
    const sx=(m)=>L+m/36*PW, sy=(v)=>B-v/M*PH;
    x.strokeStyle='rgba(255,255,255,.08)'; for(let g=0;g<=4;g++){ const y=B-PH*g/4; x.beginPath(); x.moveTo(L,y); x.lineTo(L+PW,y); x.stroke(); x.fillStyle='rgba(255,255,255,.4)'; x.font='10px sans-serif'; x.fillText(Math.round(M*g/4)+'万', 4, y+3); }
    for(let m=0;m<=36;m+=6){ x.fillStyle='rgba(255,255,255,.4)'; x.fillText(m+'ヶ月', sx(m)-12, H-8); }
    const series=[['S','#64748b'],['R','#fb923c'],['I','#38bdf8']];
    series.forEach(([k,col])=>{ x.strokeStyle=col; x.lineWidth=k==='I'?3:1.5; x.beginPath(); rows.forEach((r,i)=>{ i?x.lineTo(sx(r.m),sy(r[k])):x.moveTo(sx(r.m),sy(r[k])); }); x.stroke(); });
    x.fillStyle='rgba(56,189,248,.18)'; x.beginPath(); x.moveTo(sx(0),B); rows.forEach(r=>x.lineTo(sx(r.m),sy(r.I))); x.lineTo(sx(36),B); x.fill();
    let pk=rows[0]; rows.forEach(r=>{ if(r.I>pk.I) pk=r; }); const half=rows.find(r=>r.m>pk.m&&r.I<pk.I/2);
    x.fillStyle='#38bdf8'; x.font='bold 12px sans-serif'; x.fillText('▲ ピーク '+pk.I.toFixed(0)+'万人（'+pk.m+'ヶ月目）', Math.min(sx(pk.m)+6, W-200), sy(pk.I)-6);
    x.fillStyle='#64748b'; x.font='11px sans-serif'; x.fillText('まだ始めていない人', L+6, 26); x.fillStyle='#fb923c'; x.fillText('飽きた人', L+130, 26); x.fillStyle='#38bdf8'; x.fillText('いま使っている人', L+190, 26);
    setStat('sPeak', pk.I.toFixed(0)+'万人'); setStat('sWhen', pk.m+'ヶ月目'); setStat('sTotal', Math.min(cum, M*3).toFixed(0)+'万人'); setStat('sEnd', half?half.m+'ヶ月目':'36ヶ月以内には来ない');
    setShare('広告'+$('p').value+'%・口コミ'+$('q').value+'人・飽き'+$('r').value+'%でシミュ📈 流行のピークは'+pk.m+'ヶ月目に'+pk.I.toFixed(0)+'万人、'+(half?half.m+'ヶ月目には半減':'定番化')+'。流行が急に終わる理由👇'); }
  ['p','q','r','m','re'].forEach(id=>$(id).addEventListener('input',draw));
  $('run').addEventListener('click',draw);
  draw();
''')

# ============================================================ 8 多数決の罠
sim(slug="tasuketsu-wana", cat="wonder", emoji="🗳️", score=67,
    title="多数決の罠 投票方式シミュレーター", model="社会的選択理論（コンドルセ／ボルダ／決選投票／即時決選）",
    model_note="Condorcet (1785)、Arrow (1951)。同じ民意でも投票方式で勝者が変わることの証明",
    title_tag="多数決の罠 投票方式シミュレーター｜同じ民意でも投票ルールで勝者が変わる？",
    meta_desc="単純多数決・決選投票・ボルダ得点・総当たり（コンドルセ）の4方式で、同じ有権者の好みから勝者がどう変わるかを比べる無料シミュレーター。3候補の順位分布を動かして「多数決で最も嫌われた候補が勝つ」現象を再現。",
    og_title="多数決の罠 投票方式シミュレーター", og_desc="同じ民意でも、投票ルールで勝者が変わる。4方式で比較。",
    card_desc="同じ有権者の好みなのに、単純多数決・決選投票・ボルダ・総当たりで勝者が変わる。民意の罠を体感。",
    lead="多数決は民意を映す——とは限りません。3人の候補に対する有権者の「好みの順位」をいじると、単純多数決・決選投票・ボルダ得点・総当たりで、それぞれ別の候補が勝つことがあります。「最も嫌われた候補が勝つ」瞬間を作ってみてください。",
    canvas=canvas(640, 300, light=True),
    controls=slider("g1", "A＞B＞C と考える人", 0, 60, 35, 1, "{v}%") + slider("g2", "A＞C＞B と考える人", 0, 60, 5, 1, "{v}%")
           + slider("g3", "B＞C＞A と考える人", 0, 60, 30, 1, "{v}%") + slider("g4", "B＞A＞C と考える人", 0, 60, 3, 1, "{v}%")
           + slider("g5", "C＞B＞A と考える人", 0, 60, 22, 1, "{v}%") + slider("g6", "C＞A＞B と考える人", 0, 60, 5, 1, "{v}%"),
    buttons=btn("ex1", "例：最も嫌われた候補が勝つ") + btn("ex2", "例：三すくみ（コンドルセのパラドックス）") + btn("ex3", "例：どの方式でも同じ"),
    stats=stats([("sPl", "単純多数決", False), ("sRo", "決選投票", False), ("sBo", "ボルダ得点", False), ("sCo", "総当たり（コンドルセ）", True)]),
    legend="各方式の勝者を表示。割合の合計が100%でなくても、比率として計算します。",
    article=P("同じ有権者・同じ好みでも、<b>数え方（投票方式）を変えるだけで勝者が変わる</b>ことがあります。「どの方式が正しいか」には答えがなく、すべての望ましい性質を同時に満たす方式は存在しない——これが1951年に証明された<b>アローの不可能性定理</b>です。") + '''
<h2>4つの投票方式</h2>
''' + T([["単純多数決", "1位票がいちばん多い候補が勝ち", "分かりやすい", "票が割れると、過半数に嫌われた候補が勝つ"],
          ["決選投票", "上位2人で再投票", "過半数の支持を得た候補が勝つ", "1回目で3位だった“みんなの2番手”が消える"],
          ["ボルダ得点", "1位2点・2位1点・3位0点の合計", "幅広く好かれる候補が勝つ", "戦略的に嫌いな候補を最下位にする操作ができる"],
          ["総当たり（コンドルセ）", "全ペアで1対1対決し、全員に勝った候補が勝ち", "理屈のうえで最も“民意”に近い", "三すくみで勝者がいないことがある"]], ["方式", "数え方", "長所", "罠"]) + '''
<h2>「最も嫌われた候補が勝つ」しくみ</h2>
<p>A支持35%・B支持33%・C支持32%で、B支持者とC支持者は「Aだけは嫌」だとします。単純多数決ではAが勝ちますが、65%の人にとってAは最下位。1対1で比べれば、AはBにもCにも負けます。日本の小選挙区や知事選、アメリカ大統領選（2000年の第三候補問題）などで、この構造は現実に繰り返し起きています。</p>
<h2>三すくみ：勝者が存在しない民意</h2>
<p>「A＞B」「B＞C」「C＞A」がそれぞれ多数派になる状況では、総当たりで全員に勝つ候補がいません。じゃんけんのような循環で、1785年にコンドルセ侯爵が発見しました。この場合、議題を出す“順番”を決める人が事実上の勝者を決められます——議会運営で議長が強い理由の1つです。</p>
''',
    faqs=[("結局どの方式がいちばんいい？", "目的によります。「過半数に嫌われた候補を避けたい」なら決選投票や総当たり、「幅広く支持される候補を選びたい」ならボルダ。どの方式も何らかの罠を持つことが数学的に証明されており、方式の選択自体が政治的な決定です。"),
          ("日本の選挙はどの方式？", "衆議院の小選挙区・知事選・市長選はすべて単純多数決です。オーストラリアの下院やニューヨーク市長予備選は即時決選投票（順位付き投票）を採用しています。"),
          ("割合の合計が100%を超えるとどうなる？", "6つの数値の比率で計算するため、合計が100%でなくても問題ありません。全部0にするとエラー回避のため均等扱いになります。")],
    rel=[("echo-chamber", "📢", "エコーチェンバー 意見分極"), ("shinrai-shinka", "🤝", "信頼の進化"), ("kakuritsu-keisan", "🎲", "確率計算機"), ("same-class", "🏫", "同じクラスになる確率")],
    js=r'''
  const cv=$('cv'), x=cv.getContext('2d'), W=cv.width, H=cv.height;
  const ORD=[['A','B','C'],['A','C','B'],['B','C','A'],['B','A','C'],['C','B','A'],['C','A','B']];
  const NAME={A:'候補A',B:'候補B',C:'候補C'}, COL={A:'#2c6b86',B:'#c4442b',C:'#a97a24'};
  function calc(){ let w=[1,2,3,4,5,6].map(i=>+$('g'+i).value); let s=w.reduce((a,b)=>a+b,0); if(!s){ w=[1,1,1,1,1,1]; s=6; } w=w.map(v=>v/s);
    const first={A:0,B:0,C:0}, borda={A:0,B:0,C:0}; w.forEach((p,i)=>{ first[ORD[i][0]]+=p; borda[ORD[i][0]]+=2*p; borda[ORD[i][1]]+=p; });
    const pref=(a,b)=>w.reduce((acc,p,i)=>acc+(ORD[i].indexOf(a)<ORD[i].indexOf(b)?p:0),0);
    const C=['A','B','C']; const top=(o)=>C.slice().sort((a,b)=>o[b]-o[a]);
    const pl=top(first)[0]; const [r1,r2]=top(first); const ro=pref(r1,r2)>=0.5?r1:r2; const bo=top(borda)[0];
    let co=null; for(const c of C){ if(C.every(d=>d===c||pref(c,d)>0.5)) co=c; }
    const last={A:0,B:0,C:0}; w.forEach((p,i)=>last[ORD[i][2]]+=p);
    return {first,borda,pref,pl,ro,bo,co,last,r1,r2}; }
  function bar(y,label,vals,fmt){ x.fillStyle='#14181d'; x.font='bold 12px sans-serif'; x.fillText(label, 12, y+14); let bx=150; ['A','B','C'].forEach(c=>{ const w=vals[c]*380; x.fillStyle=COL[c]; x.fillRect(bx,y,w,20); x.fillStyle='#fff'; x.font='11px sans-serif'; if(w>28) x.fillText(c+' '+fmt(vals[c]), bx+4, y+14); bx+=w; }); }
  function draw(){ const r=calc(); x.fillStyle='#fff'; x.fillRect(0,0,W,H);
    bar(16,'1位票の割合', r.first, v=>Math.round(v*100)+'%');
    bar(50,'最下位にされた割合', r.last, v=>Math.round(v*100)+'%');
    const bsum=r.borda.A+r.borda.B+r.borda.C; bar(84,'ボルダ得点の割合', {A:r.borda.A/bsum,B:r.borda.B/bsum,C:r.borda.C/bsum}, v=>Math.round(v*100)+'%');
    x.fillStyle='#14181d'; x.font='bold 12px sans-serif'; x.fillText('1対1対決（総当たり）', 12, 134);
    const pairs=[['A','B'],['B','C'],['A','C']]; pairs.forEach(([a,b],i)=>{ const y=148+i*24; const pa=r.pref(a,b); x.fillStyle=COL[a]; x.fillRect(150,y,pa*380,18); x.fillStyle=COL[b]; x.fillRect(150+pa*380,y,(1-pa)*380,18); x.fillStyle='#fff'; x.font='11px sans-serif'; x.fillText(a+' '+Math.round(pa*100)+'%',154,y+13); x.fillText(b+' '+Math.round((1-pa)*100)+'%',150+pa*380+4,y+13); x.fillStyle=pa>0.5?COL[a]:COL[b]; x.font='bold 11px sans-serif'; x.fillText((pa>0.5?a:b)+'の勝ち', 540, y+13); });
    x.fillStyle='#59616c'; x.font='11px sans-serif'; x.fillText('決選投票：上位2人 '+r.r1+' vs '+r.r2+' → '+NAME[r.ro], 12, 244);
    const winners=[r.pl,r.ro,r.bo,r.co].filter(Boolean); const uniq=new Set(winners).size;
    x.fillStyle=uniq>1?'#c4442b':'#2c6b86'; x.font='bold 14px sans-serif'; x.fillText(uniq>1?'⚠️ 方式によって勝者が違います（'+uniq+'通り）':'✅ どの方式でも同じ候補が勝ちます', 12, 276);
    setStat('sPl', NAME[r.pl]); setStat('sRo', NAME[r.ro]); setStat('sBo', NAME[r.bo]); setStat('sCo', r.co?NAME[r.co]:'なし（三すくみ）');
    setShare('同じ民意で投票方式を変えたら…単純多数決:'+r.pl+'／決選投票:'+r.ro+'／ボルダ:'+r.bo+'／総当たり:'+(r.co||'勝者なし')+'🗳️ 多数決の罠を体感👇'); }
  function setv(v){ v.forEach((n,i)=>{ $('g'+(i+1)).value=n; $('g'+(i+1)).dispatchEvent(new Event('input')); }); draw(); }
  for(let i=1;i<=6;i++) $('g'+i).addEventListener('input',draw);
  $('ex1').addEventListener('click',()=>setv([35,0,33,0,32,0]));
  $('ex2').addEventListener('click',()=>setv([34,0,33,0,33,0]));
  $('ex3').addEventListener('click',()=>setv([45,10,20,5,15,5]));
  draw();
''')

# ============================================================ 9 満員電車
sim(slug="manin-densha", cat="life", emoji="🚃", score=68,
    title="満員電車 混雑率シミュレーター", model="粒子ベースの群衆密度モデル（1㎡あたりの人数と圧力）",
    model_note="国交省の混雑率定義＋群衆密度と圧力の関係（Fruin 1971、群衆事故研究）",
    title_tag="満員電車 混雑率シミュレーター｜混雑率100・150・200%は1㎡に何人？体感を可視化",
    meta_desc="混雑率100%・150%・180%・200%・250%が実際にどんな密度なのかを、車両の中に人を並べてアニメで可視化する無料シミュレーター。1㎡あたりの人数、体にかかる圧力、スマホが使えるかの目安まで。首都圏の路線別混雑率の実データつき。",
    og_title="満員電車 混雑率シミュレーター", og_desc="混雑率200%は1㎡に何人？車両の中を可視化。",
    card_desc="混雑率150%と200%、実際どれくらい違う？車両の中に人を並べて、密度と圧力を可視化。",
    lead="「混雑率180%」と言われても、どれくらいギュウギュウなのか想像しにくいもの。混雑率を動かすと、車両1両の中に実際に人が並び、1㎡あたりの人数と体にかかる圧力の目安が分かります。",
    canvas=canvas(640, 300, light=True),
    controls=slider("rate", "混雑率", 50, 300, 150, 10, "{v}%") + select("car", "車両", [("std", "一般的な通勤車両（定員約150人・20m）"), ("wide", "ワイドドア／ロング車両（定員約160人）")]) + slider("bag", "大きな荷物を持つ人の割合", 0, 50, 10, 5, "{v}%"),
    buttons=btn("shake", "🚃 発車・急ブレーキを再現"),
    stats=stats([("sN", "1両の乗客数", True), ("sD", "1㎡あたり", False), ("sP", "体にかかる圧力の目安", False), ("sPh", "スマホ操作", False)]),
    legend="上から見た車両1両。点＝乗客（大きい点＝大きな荷物）。急ブレーキで人がどれだけ押し寄せるかも再現します。",
    article=P("混雑率は「乗客数 ÷ 定員」。定員は座席＋つり革・ドア付近の立ち客の合計で、<b>定員100%でも立っている人はいます</b>。150%で肩が触れ合い、200%で体が密着して身動きが取れず、250%で電車が揺れるたびに体が斜めになります。") + '''
<h2>国土交通省による混雑率の目安</h2>
''' + T([["100%", "定員乗車。座席に座るか、つり革につかまるか、ドア付近の柱につかまることができる"], ["150%", "広げて楽に新聞を読める"], ["180%", "折りたたむなど無理をすれば新聞を読める"], ["200%", "体が触れ合い相当圧迫感があるが、週刊誌程度なら何とか読める"], ["250%", "電車が揺れるたびに体が斜めになって身動きができず、手も動かせない"]], ["混雑率", "国交省の定義"]) + '''
<h2>1㎡あたりの人数と「圧力」</h2>
<p>群衆研究では、1㎡あたり<b>4人</b>を超えると自由に動けなくなり、<b>6人</b>を超えると隣の人と押し合う圧力が生まれ、<b>8人以上</b>で群衆事故の危険域とされます。通勤車両の立席スペースは1両あたり約40㎡なので、混雑率200%（約300人）で立席部分は1㎡あたり約6人。急ブレーキで前方へ体重が集中すると、局所的に危険域に達することがあります。</p>
<h2>首都圏の主要路線の混雑率（国交省 2023年度）</h2>
''' + T([["日暮里・舎人ライナー（赤土小学校前→西日暮里）", "171%"], ["東西線（木場→門前仲町）", "148%"], ["横須賀線（武蔵小杉→西大井）", "158%"], ["中央線快速（中野→新宿）", "139%"], ["埼京線（板橋→池袋）", "135%"], ["東海道線（川崎→品川）", "140%"]], ["路線・区間", "最混雑時間帯の混雑率"]) + '''
<p>コロナ前（2019年度）は東西線199%・横須賀線195%など、200%前後の路線が多数ありました。テレワークの定着で全体に3〜5割下がっています。</p>
''',
    faqs=[("混雑率180%と200%はそんなに違う？", "1両あたり約30人、立席1㎡あたりで約0.7人の差ですが、体感は大きく違います。180%は「腕を動かせる」、200%は「腕が動かせない」境目にあたります。"),
          ("荷物の割合を変えると何が変わる？", "大きな荷物は1人分近いスペースを取るため、同じ乗客数でも実効的な密度が上がります。リュックを前に抱えるマナーはこの密度を下げるための工夫です。"),
          ("混雑率はどう測っている？", "鉄道各社が最混雑区間の最混雑1時間の乗客数を、目視や車両の重量センサーで推計し、定員で割っています。国交省が毎年公表しています。")],
    rel=[("jisa-shukkin", "🕘", "時差出勤の効果"), ("queue-docchi", "🧍", "行列、1列並び vs レジ別"), ("elevator-sim", "🛗", "エレベーター待ち時間"), ("hinan-crowd", "🚪", "群衆避難シミュレーター")],
    js=r'''
  const cv=$('cv'), x=cv.getContext('2d'), W=cv.width, H=cv.height;
  let ppl=[], shakeV=0, shakeT=0;
  const CAR={std:{cap:150,seat:54,len:20,wid:2.9},wide:{cap:160,seat:48,len:20,wid:2.9}};
  const M={x0:20,y0:40,w:600,h:190}; // 車両描画枠（20m×2.9m）
  function build(){ const c=CAR[$('car').value]; const n=Math.round(c.cap*+$('rate').value/100); const bagp=+$('bag').value/100; ppl=[];
    const seats=Math.min(n,c.seat); for(let i=0;i<seats;i++){ const side=i%2, k=Math.floor(i/2); ppl.push({x:M.x0+18+k*((M.w-36)/(c.seat/2)), y:side?M.y0+18:M.y0+M.h-18, seat:true, r:5, bag:false}); }
    const stand=n-seats; for(let i=0;i<stand;i++){ ppl.push({x:M.x0+30+Math.random()*(M.w-60), y:M.y0+40+Math.random()*(M.h-80), seat:false, r:Math.random()<bagp?7:5, bag:false, vx:0, vy:0}); }
    for(let it=0;it<60;it++) relax(); }
  function relax(){ for(let i=0;i<ppl.length;i++){ const a=ppl[i]; if(a.seat) continue; for(let j=0;j<ppl.length;j++){ if(i===j) continue; const b=ppl[j]; const dx=a.x-b.x, dy=a.y-b.y; const d=Math.hypot(dx,dy)||0.01; const min=a.r+b.r+1; if(d<min){ const f=(min-d)*0.5; a.x+=dx/d*f; a.y+=dy/d*f; } }
      a.x=clamp(a.x,M.x0+40,M.x0+M.w-40); a.y=clamp(a.y,M.y0+36,M.y0+M.h-36); } }
  function draw(){ x.fillStyle='#fff'; x.fillRect(0,0,W,H); x.fillStyle='#f1efe8'; x.fillRect(M.x0,M.y0,M.w,M.h); x.strokeStyle='#8b929c'; x.lineWidth=2; x.strokeRect(M.x0,M.y0,M.w,M.h);
    for(let d=0;d<4;d++){ const dx=M.x0+60+d*(M.w-120)/3; x.fillStyle='#cbd5e1'; x.fillRect(dx-20,M.y0-3,40,6); x.fillRect(dx-20,M.y0+M.h-3,40,6); }
    x.fillStyle='#d9d4c7'; x.fillRect(M.x0+8,M.y0+8,M.w-16,20); x.fillRect(M.x0+8,M.y0+M.h-28,M.w-16,20);
    const c=CAR[$('car').value]; const n=ppl.length; const standN=Math.max(0,n-c.seat); const area=c.len*c.wid-11; const dens=standN/area;
    ppl.forEach(p=>{ x.fillStyle=p.seat?'#7fa7b8':(dens>6?'#c4442b':dens>4?'#e08a3c':'#2c6b86'); x.beginPath(); x.arc(p.x,p.y,p.r,0,7); x.fill(); });
    x.fillStyle='#14181d'; x.font='bold 12px sans-serif'; x.fillText('← 進行方向', M.x0, M.y0-10); x.fillStyle='#59616c'; x.font='11px sans-serif'; x.fillText('立席スペース 1㎡あたり '+dens.toFixed(1)+'人', M.x0+120, M.y0-10);
    const press = dens<2?'ほぼなし':dens<4?'軽く触れる程度':dens<6?'肩・背中が常に密着（体重の1〜2割）':dens<8?'強い圧迫（体重の3〜5割）・呼吸が浅くなる':'危険域（群衆事故の研究で圧死が起きる密度）';
    const phone = dens<2?'自由に使える':dens<4?'胸の前なら使える':dens<6?'顔の前で固定なら何とか':'ほぼ不可能';
    setStat('sN', n+'人'); setStat('sD', dens.toFixed(1)+'人'); setStat('sP', press); setStat('sPh', phone);
    setShare('混雑率'+$('rate').value+'%は1両'+n+'人、立席1㎡あたり'+dens.toFixed(1)+'人🚃 圧力は「'+press+'」、スマホは「'+phone+'」。混雑率の体感を可視化👇'); }
  function loop(){ if(shakeT>0){ shakeT--; ppl.forEach(p=>{ if(!p.seat){ p.x+=shakeV; } }); relax(); shakeV*=0.92; } draw(); requestAnimationFrame(loop); }
  ['rate','car','bag'].forEach(id=>$(id).addEventListener('input',build));
  $('shake').addEventListener('click',()=>{ shakeV=-6; shakeT=40; });
  build(); loop();
''')

# ============================================================ 10 時差出勤
sim(slug="jisa-shukkin", cat="work", emoji="🕘", score=67,
    title="時差出勤の効果シミュレーター", model="出勤時刻分布（ガウス混合）とピーク混雑率のモデル",
    model_note="国交省「オフピーク通勤」の考え方。ピーク30分の集中度で混雑率が決まる",
    title_tag="時差出勤の効果シミュレーター｜何割が30分ずらすとピークの混雑率はどれだけ下がる？",
    meta_desc="会社の何割が出勤を何分ずらすと、朝のピーク混雑率がどれだけ下がるかを、時刻別の乗客分布グラフで見る無料シミュレーター。フレックス・時差通勤の効果を数字で。自分がずらした場合の混雑率も表示。",
    og_title="時差出勤の効果シミュレーター", og_desc="何割が30分ずらせば、ピークの混雑率はどれだけ下がる？",
    card_desc="全体の何割が何分ずらすと朝のピーク混雑率が何%下がるか。自分だけずらした場合の混雑率も。",
    lead="「時差出勤にご協力ください」と言われても、効果はピンときません。全体の何割が、何分ずらすと、ピークの混雑率がどこまで下がるのか。そして自分だけがずらしたら、どれだけ空いた電車に乗れるのかを見てください。",
    canvas=canvas(640, 340),
    controls=slider("peak", "現在のピーク混雑率", 100, 250, 180, 5, "{v}%") + slider("share", "時差出勤する人の割合", 0, 80, 30, 5, "{v}%")
           + slider("shift", "ずらす時間", 15, 120, 45, 15, "{v}分") + select("dir", "ずらす方向", [("both", "早出と遅出に半々"), ("late", "遅出（9時台へ）"), ("early", "早出（7時台へ）")]) + slider("me", "あなたの乗車時刻", 6.5, 10.5, 8.25, 0.25),
    buttons=btn("run", "▶ 計算する", True),
    stats=stats([("sPeak", "施策後のピーク混雑率", True), ("sDown", "ピークの低下", False), ("sMe", "あなたの時刻の混雑率", False), ("sBest", "いちばん空く時刻", False)]),
    legend="灰色＝現在の乗客分布、青＝時差出勤後の分布。横軸は乗車時刻、縦軸は混雑率。赤い点線が「あなたの乗車時刻」。",
    article=P("朝の通勤は<b>8時前後の30分に極端に集中</b>しています。全体の3割が45分ずらすだけで、ピーク混雑率は2割前後下がります。そして自分1人が30分早く（または遅く）乗るだけでも、混雑率は数十ポイント低い電車に乗れます。") + '''
<h2>なぜピークは「とがっている」のか</h2>
<p>始業時刻が9時に集中しているため、乗車時刻は8時〜8時30分に山を作ります。首都圏の主要路線では、ピーク1時間に1日の乗客の約20%、ピーク30分に約12%が集中します。混雑率は「その時間帯の乗客数 ÷ 輸送力」なので、山の高さがそのまま混雑率になります。</p>
<h2>時差出勤で山を“ならす”</h2>
''' + T([["1割が45分ずらす", "約5〜7%低下", "効果は小さいが確実"], ["3割が45分ずらす", "約15〜20%低下", "180%→150%前後。「新聞が読める」ライン"], ["5割が60分ずらす", "約30%低下", "ピーク自体が消え、なだらかな台形になる"]], ["施策", "ピーク混雑率の変化（目安）", "コメント"]) + '''
<p>コロナ禍のテレワークで実証されたように、ピークが1〜2割減るだけで体感は大きく変わります。東京都の「時差Biz」、JR東日本のオフピークポイントなど、企業と鉄道会社の両方がこの山をならすことに投資しているのはそのためです。</p>
<h2>自分だけがずらす戦略</h2>
<p>全社が動かなくても、自分が7時30分に乗れば混雑率は8時台の6〜7割程度、9時15分以降なら半分以下になることが多いです。フレックス制度があるなら、「30分の時差」が最もコスパの高い通勤改善になります。</p>
''',
    faqs=[("「ずらす方向」で効果は変わる？", "早出と遅出に分散させるのが最も効果的です。片側だけにずらすと、ずらした先で新しい山ができることがあります（特に遅出は9時台の元々の乗客と重なります）。"),
          ("実際の路線データではない？", "はい。首都圏の平均的な通勤時刻分布（8時前後をピークとする正規分布に近い形）をモデル化したものです。路線固有の時刻分布とは異なります。"),
          ("混雑率は何%を目指せばいい？", "国交省の目標は主要路線で150%以下です。「広げて楽に新聞が読める」レベルで、身体的な圧迫がほぼなくなる目安です。")],
    rel=[("manin-densha", "🚃", "満員電車 混雑率シミュレーター"), ("tsukin-car", "🚗", "車通勤 vs 電車通勤"), ("elevator-sim", "🛗", "エレベーター待ち時間"), ("queue-docchi", "🧍", "行列、1列並び vs レジ別")],
    js=r'''
  const cv=$('cv'), x=cv.getContext('2d'), W=cv.width, H=cv.height;
  const g=(t,m,s)=>Math.exp(-0.5*((t-m)/s)**2)/(s*Math.sqrt(2*Math.PI));
  function base(t){ return 0.8*g(t,8.1,0.32)+0.2*g(t,8.6,0.7); }
  function after(t){ const sh=+$('share').value/100, d=+$('shift').value/60, dir=$('dir').value; const b=base(t)*(1-sh);
    if(dir==='both') return b+sh*0.5*(0.8*g(t-(-d),8.1,0.32)+0.2*g(t-(-d),8.6,0.7))+sh*0.5*(0.8*g(t-d,8.1,0.32)+0.2*g(t-d,8.6,0.7));
    const s=dir==='late'?d:-d; return b+sh*(0.8*g(t-s,8.1,0.32)+0.2*g(t-s,8.6,0.7)); }
  function draw(){ x.fillStyle='#0b1020'; x.fillRect(0,0,W,H); const L=44,B=H-26,PW=W-L-12,PH=B-20; const t0=6.5,t1=10.5;
    const peak0=+$('peak').value; const FLOOR=60; const bmax=base(8.1); const scale=(peak0-FLOOR)/bmax; const cr=(v)=>FLOOR+v*scale;
    const sx=(t)=>L+(t-t0)/(t1-t0)*PW, sy=(v)=>B-Math.min(v,300)/300*PH;
    x.strokeStyle='rgba(255,255,255,.08)'; for(let v=50;v<=300;v+=50){ x.beginPath(); x.moveTo(L,sy(v)); x.lineTo(L+PW,sy(v)); x.stroke(); x.fillStyle='rgba(255,255,255,.4)'; x.font='10px sans-serif'; x.fillText(v+'%', 4, sy(v)+3); }
    for(let t=7;t<=10;t+=0.5){ x.fillStyle='rgba(255,255,255,.4)'; x.fillText(Math.floor(t)+':'+(t%1?'30':'00'), sx(t)-12, H-8); }
    x.strokeStyle='#ef4444'; x.setLineDash([4,4]); x.beginPath(); x.moveTo(L,sy(150)); x.lineTo(L+PW,sy(150)); x.stroke(); x.setLineDash([]); x.fillStyle='#ef4444'; x.fillText('目標150%', L+PW-60, sy(150)-4);
    let pk=0, bestT=t0, bestV=1e9, meV=0; const me=+$('me').value;
    x.fillStyle='rgba(148,163,184,.35)'; x.beginPath(); x.moveTo(sx(t0),B); for(let t=t0;t<=t1;t+=0.02){ x.lineTo(sx(t),sy(cr(base(t)))); } x.lineTo(sx(t1),B); x.fill();
    x.strokeStyle='#38bdf8'; x.lineWidth=2.5; x.beginPath(); for(let t=t0;t<=t1;t+=0.02){ const v=cr(after(t)); pk=Math.max(pk,v); if(t>=7&&t<=9.5&&v<bestV){bestV=v;bestT=t;} const X=sx(t),Y=sy(v); t===t0?x.moveTo(X,Y):x.lineTo(X,Y); } x.stroke();
    meV=cr(after(me)); x.strokeStyle='#f472b6'; x.setLineDash([3,3]); x.beginPath(); x.moveTo(sx(me),B); x.lineTo(sx(me),sy(meV)); x.stroke(); x.setLineDash([]); x.fillStyle='#f472b6'; x.font='bold 11px sans-serif'; x.fillText('あなた '+Math.round(meV)+'%', sx(me)+4, sy(meV)-6);
    x.fillStyle='#94a3b8'; x.font='11px sans-serif'; x.fillText('現在', L+8, 30); x.fillStyle='#38bdf8'; x.fillText('時差出勤後', L+40, 30);
    const fm=(t)=>{ const m=Math.round(t*60); return Math.floor(m/60)+':'+String(m%60).padStart(2,'0'); };
    setStat('sPeak', Math.round(pk)+'%'); setStat('sDown', '−'+Math.round(peak0-pk)+'pt'); setStat('sMe', Math.round(meV)+'%（'+fm(me)+'）'); setStat('sBest', fm(bestT)+'（'+Math.round(bestV)+'%）');
    setShare('全体の'+$('share').value+'%が'+$('shift').value+'分ずらすと、ピーク混雑率'+peak0+'%→'+Math.round(pk)+'%🕘 自分が'+fm(me)+'に乗ると'+Math.round(meV)+'%。時差出勤の効果を数字で👇'); }
  ['peak','share','shift','dir','me'].forEach(id=>$(id).addEventListener('input',draw)); $('run').addEventListener('click',draw);
  $('me').dataset.fmt='{v}'; const meL=$('meL'); const upd=()=>{ const m=Math.round(+$('me').value*60); meL.textContent=Math.floor(m/60)+':'+String(m%60).padStart(2,'0'); }; $('me').addEventListener('input',upd); upd();
  draw();
''')
