# -*- coding: utf-8 -*-
"""シミュラボ：SEO強化 新規30本（Ahrefsで選定した低KD×一定ボリュームKW）。
   計算12＋診断18。gen_sims11のTPL(write_all)を再利用。CTAなしカテゴリ。"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq, write_all

HEALTH='健康・カラダ'; KIDS='子ども・育児'; TAX='税金・確定申告'; WORK='仕事・働き方'
SENIOR='シニア・終活・介護'; BIZ='店舗・ビジネス'; MENTAL='メンタル・自己分析'
BEAUTY='美容・ファッション'; LOVE='恋愛・婚活'; STUDY='学生・勉強'
SIMS=[]
def add(**k): SIMS.append(k)
def C(t): return '<div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：'+t+'</div>'
def REF(items): return '<h2>参考</h2><ul class="seo-refs">'+''.join('<li>'+i+'</li>' for i in items)+'</ul>'
def J(s): return json.dumps(s, ensure_ascii=False)

# ========================= 計算 12本 =========================

add(id='tdee-keisan', cat=HEALTH, emoji='🔥',
  title='メンテナンスカロリー(TDEE) 計算｜1日の維持カロリーは？｜シミュラボ',
  desc='性別・年齢・身長・体重・活動量から、体重を維持できる1日の総消費カロリー（メンテナンスカロリー＝TDEE）と、減量・増量の目安を計算する無料ツール。',
  ogtitle='メンテナンスカロリー(TDEE)計算｜維持は何kcal？', ogdesc='TDEE(維持カロリー)と減量・増量の目安を計算。',
  h1='メンテナンスカロリー(TDEE)計算',
  lead='いまの体重を維持できる1日のカロリー（メンテナンスカロリー＝TDEE）は何kcal？基礎代謝×活動量から計算し、減量・増量の目安も表示します。',
  inputs='''    <h2>🔥 条件を入れる</h2>
    <div class="row"><div class="field"><label>性別</label><select id="sex"><option value="m">男性</option><option value="f">女性</option></select></div>
    <div class="field"><label>年齢 <span class="hint">（歳）</span></label><input type="number" id="age" value="30" min="10" max="100" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>身長 <span class="hint">（cm）</span></label><input type="number" id="h" value="170" min="100" max="230" inputmode="numeric"></div>
    <div class="field"><label>体重 <span class="hint">（kg）</span></label><input type="number" id="w" value="65" min="20" max="250" step="0.1" inputmode="decimal"></div></div>
    <div class="field"><label>活動量</label><select id="act"><option value="1.2">ほぼ運動しない</option><option value="1.375" selected>軽い運動(週1〜3)</option><option value="1.55">中程度(週3〜5)</option><option value="1.725">よく動く(週6〜7)</option></select></div>
    <button class="btn btn-primary" id="calcBtn">維持カロリーを計算する</button>''',
  result='''      <div class="label">メンテナンスカロリー(TDEE)</div>
      <div class="big"><span id="big">0</span><span class="unit">kcal</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">基礎代謝(BMR)</div><div class="v" id="bmr">—</div></div>
      <div class="stat"><div class="k">減量(-500)</div><div class="v accent" id="diet">—</div></div>
      <div class="stat"><div class="k">増量(+300)</div><div class="v" id="bulk">—</div></div></div>''',
  article=C('メンテナンスカロリー（TDEE）＝ <b>基礎代謝(BMR) × 活動係数</b>。これより少なく食べれば減量、多ければ増量します。')+'''
    <h2>TDEEの計算方法</h2>
    <p>TDEE（Total Daily Energy Expenditure＝1日の総消費カロリー）は、基礎代謝に日々の活動量を掛けて求めます。この値（メンテナンスカロリー）と同じだけ食べれば体重は維持されます。</p>
    <div class="note"><strong>計算式（ミフリン・サンジョール式）</strong><br>BMR ＝ 10×体重 ＋ 6.25×身長 − 5×年齢 ＋（男性+5／女性−161）<br>TDEE ＝ BMR × 活動係数（1.2〜1.725）</div>
    <p>体脂肪1kg ≒ 7,200kcal。1日−500kcalで月約2kgの減量ペースが目安です。</p>
    <h2>よくある質問</h2>'''+faq([('基礎代謝との違いは？','基礎代謝は安静時の消費。TDEEはそれに活動を加えた1日の総消費です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['厚生労働省「日本人の食事摂取基準」','Mifflin-St Jeor式']),
  js='''  function calc(){const sex=$('sex').value,age=Math.max(1,+$('age').value||1),h=Math.max(1,+$('h').value||1),w=Math.max(0,+$('w').value||0),act=+$('act').value||1.2;
    const bmr=10*w+6.25*h-5*age+(sex==='m'?5:-161), tdee=bmr*act;
    $('sub').textContent=`${sex==='m'?'男性':'女性'}・${age}歳・${h}cm・${w}kg`;
    $('bmr').textContent=num(bmr)+'kcal';$('diet').textContent=num(tdee-500)+'kcal';$('bulk').textContent=num(tdee+300)+'kcal';
    show();anim($('big'),0,tdee,800);
    SHARE=`メンテナンスカロリー(TDEE)は約${num(tdee)}kcalでした🔥 減量なら${num(tdee-500)}kcal`;}''')

add(id='shussan-teate', cat=KIDS, emoji='🤰',
  title='出産手当金 計算｜産休でいくらもらえる？標準報酬から計算｜シミュラボ',
  desc='月給（標準報酬月額）と産前産後の休業日数から、健康保険の出産手当金の日額・総額の目安を計算する無料シミュレーター。',
  ogtitle='出産手当金 計算｜産休でいくらもらえる？', ogdesc='月給と産休日数から出産手当金の総額を概算。',
  h1='出産手当金 計算シミュレーター',
  lead='産休中にもらえる「出産手当金」はいくら？月給（標準報酬月額）と休業日数から、受け取れる目安を計算します。',
  inputs='''    <h2>🤰 条件を入れる</h2>
    <div class="row"><div class="field"><label>月給（標準報酬月額の目安） <span class="hint">（万円）</span></label><input type="number" id="g" value="28" min="0" inputmode="numeric"></div>
    <div class="field"><label>産休の日数 <span class="hint">（日・産前42+産後56=98）</span></label><input type="number" id="d" value="98" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">出産手当金を計算する</button>''',
  result='''      <div class="label">出産手当金の総額（目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1日あたり</div><div class="v accent" id="day">—</div></div>
      <div class="stat"><div class="k">支給日数</div><div class="v" id="days">—</div></div>
      <div class="stat"><div class="k">標準報酬日額</div><div class="v" id="nichi">—</div></div></div>''',
  article=C('出産手当金は <b>標準報酬日額 × 2/3 × 産休日数</b>。原則、産前42日＋産後56日＝最大98日が対象です。')+'''
    <h2>出産手当金のしくみ</h2>
    <p>会社員（健康保険の被保険者）が産休で給与をもらえない期間、健康保険から支給されるのが出産手当金です。産前42日（多胎は98日）＋産後56日が対象。育休前の収入の約2/3が受け取れます。</p>
    <div class="note"><strong>計算式</strong><br>標準報酬日額 ＝ 標準報酬月額 ÷ 30<br>1日の支給 ＝ 標準報酬日額 × 2/3<br>総額 ＝ 1日の支給 × 産休日数</div>
    <p>「出産育児一時金（50万円）」とは別にもらえます。本ツールは概算です。</p>
    <h2>よくある質問</h2>'''+faq([('出産育児一時金とは別？','はい。出産費用に充てる一時金（原則50万円）とは別に、給与の代わりとして出産手当金が支給されます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['全国健康保険協会「出産手当金」']),
  js='''  function calc(){const g=Math.max(0,+$('g').value||0)*10000,d=Math.max(0,+$('d').value||0);
    const nichi=g/30, day=nichi*2/3, total=day*d;
    $('sub').textContent=`月給${num(g/10000)}万円・産休${d}日`;
    $('day').textContent=yen(day);$('days').textContent=d+'日';$('nichi').textContent=yen(nichi);
    show();anim($('big'),0,total,800);
    SHARE=`出産手当金シミュ、月給${num(g/10000)}万円で産休${d}日なら 約${yen(total)}もらえる計算でした🤰`;}''')

add(id='haigusha-koujo', cat=TAX, emoji='💑',
  title='配偶者特別控除 計算｜配偶者の年収でいくら控除？｜シミュラボ',
  desc='配偶者の給与年収と本人の所得税率から、配偶者控除・配偶者特別控除の額と節税額の目安を計算する無料シミュレーター。',
  ogtitle='配偶者特別控除 計算｜いくら控除される？', ogdesc='配偶者の年収から配偶者(特別)控除と節税額を計算。',
  h1='配偶者特別控除 計算シミュレーター',
  lead='配偶者の年収がいくらなら、いくら控除される？配偶者の給与年収と本人の税率から、配偶者控除・配偶者特別控除と節税額を計算します。',
  inputs='''    <h2>💑 条件を入れる</h2>
    <div class="row"><div class="field"><label>配偶者の給与年収 <span class="hint">（万円）</span></label><input type="number" id="p" value="130" min="0" inputmode="numeric"></div>
    <div class="field"><label>本人の所得税率</label><select id="r"><option value="0.05">5%</option><option value="0.10" selected>10%</option><option value="0.20">20%</option><option value="0.23">23%</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">控除額を計算する</button>''',
  result='''      <div class="label">節税額（所得税＋住民税）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">控除の種類</div><div class="v accent" id="kind">—</div></div>
      <div class="stat"><div class="k">所得税の控除</div><div class="v" id="koujo">—</div></div>
      <div class="stat"><div class="k">住民税の控除</div><div class="v" id="ju">—</div></div></div>''',
  article=C('配偶者の給与年収が <b>103万円以下→配偶者控除</b>、<b>103万〜201万円→配偶者特別控除</b>。201万円を超えると控除はゼロになります（本人の所得制限あり）。')+'''
    <h2>配偶者控除・配偶者特別控除のしくみ</h2>
    <p>配偶者の収入が一定以下なら、納税者本人の所得から控除が受けられます。年収103万円までは「配偶者控除（38万円）」、103万円を超えても201.6万円までは「配偶者特別控除」が段階的に適用されます（いわゆる103万・150万・201万の壁）。</p>
    <table class="seo-table"><tr><th>配偶者の給与年収</th><th>所得税の控除</th></tr>
    <tr><td>〜103万円</td><td>38万円（配偶者控除）</td></tr>
    <tr><td>〜150万円</td><td>38万円（特別控除・満額）</td></tr>
    <tr><td>〜201万円</td><td>段階的に減少</td></tr>
    <tr><td>201万円超</td><td>0円</td></tr></table>
    <p>本人の合計所得が900万円超だと控除は減額されます。本ツールは本人所得900万円以下・概算です。</p>
    <h2>よくある質問</h2>'''+faq([('150万の壁とは？','配偶者特別控除が満額(38万)になる上限。これを超えると控除が段階的に減ります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['国税庁「配偶者控除・配偶者特別控除」']),
  js='''  function calc(){const p=Math.max(0,+$('p').value||0),r=+$('r').value||0.1;
    let ks=0,kj=0,kind;
    if(p<=103){ks=38;kj=33;kind='配偶者控除';}
    else if(p<=150){ks=38;kj=33;kind='配偶者特別控除(満額)';}
    else if(p<=155){ks=36;kj=33;kind='配偶者特別控除';}
    else if(p<=160){ks=31;kj=31;kind='配偶者特別控除';}
    else if(p<=167){ks=26;kj=26;kind='配偶者特別控除';}
    else if(p<=175){ks=21;kj=21;kind='配偶者特別控除';}
    else if(p<=183){ks=16;kj=16;kind='配偶者特別控除';}
    else if(p<=190){ks=11;kj=11;kind='配偶者特別控除';}
    else if(p<=197){ks=6;kj=6;kind='配偶者特別控除';}
    else if(p<=201){ks=3;kj=3;kind='配偶者特別控除';}
    else {ks=0;kj=0;kind='控除なし';}
    const sho=ks*10000*r, ju=kj*10000*0.10, total=sho+ju;
    $('sub').textContent=`配偶者年収${p}万円・税率${Math.round(r*100)}%`;
    $('kind').textContent=kind;$('koujo').textContent=yen(ks*10000);$('ju').textContent=yen(kj*10000);
    show();anim($('big'),0,total,800);
    SHARE=`配偶者特別控除シミュ、配偶者年収${p}万円→「${kind}」で節税 約${yen(total)}でした💑`;}''')

add(id='saishushoku-teate', cat=WORK, emoji='🎯',
  title='再就職手当 計算｜早期再就職でいくらもらえる？｜シミュラボ',
  desc='基本手当日額と支給残日数から、失業保険の早期再就職でもらえる「再就職手当」の金額を計算する無料シミュレーター。',
  ogtitle='再就職手当 計算｜いくらもらえる？', ogdesc='基本手当日額と残日数から再就職手当を計算。',
  h1='再就職手当 計算シミュレーター',
  lead='失業保険をもらいきる前に就職が決まったら「再就職手当」がもらえます。基本手当日額と支給残日数から金額を計算します。',
  inputs='''    <h2>🎯 条件を入れる</h2>
    <div class="row"><div class="field"><label>基本手当日額 <span class="hint">（円）</span></label><input type="number" id="day" value="6000" min="0" inputmode="numeric"></div>
    <div class="field"><label>支給日数の残り <span class="hint">（日）</span></label><input type="number" id="zan" value="70" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>所定給付日数</label><input type="number" id="shotei" value="90" min="1" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">再就職手当を計算する</button>''',
  result='''      <div class="label">再就職手当（目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">支給率</div><div class="v accent" id="rate">—</div></div>
      <div class="stat"><div class="k">残り日数の割合</div><div class="v" id="ratio">—</div></div>
      <div class="stat"><div class="k">判定</div><div class="v" id="judge">—</div></div></div>''',
  article=C('再就職手当 ＝ <b>基本手当日額 × 残り日数 × 支給率</b>。残日数が所定給付日数の <b>2/3以上なら70%、1/3以上なら60%</b> が支給されます。')+'''
    <h2>再就職手当のしくみ</h2>
    <p>失業手当（基本手当）の受給中に安定した職に早く就くと、残りの手当の一部が「再就職手当」として一時金でもらえます。早く決まるほど（残日数が多いほど）支給率が高くなる、就職を後押しする制度です。</p>
    <div class="note"><strong>計算式</strong><br>残日数が所定給付日数の2/3以上 → 残日数 × 70%<br>1/3以上2/3未満 → 残日数 × 60%<br>再就職手当 ＝ 基本手当日額 × 残日数 × 支給率</div>
    <p>支給には「1/3以上の残日数」「待期満了後の就職」などの条件があります。本ツールは概算です。</p>
    <h2>よくある質問</h2>'''+faq([('いつ申請する？','再就職した日の翌日から1か月以内に、ハローワークへ申請します。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['ハローワーク「再就職手当」']),
  js='''  function calc(){const day=Math.max(0,+$('day').value||0),zan=Math.max(0,+$('zan').value||0),sh=Math.max(1,+$('shotei').value||1);
    const ratio=zan/sh; let rate,judge;
    if(ratio>=2/3){rate=0.7;judge='早期(残2/3以上)';}else if(ratio>=1/3){rate=0.6;judge='残1/3以上';}else{rate=0;judge='対象外(残1/3未満)';}
    const total=day*zan*rate;
    $('sub').textContent=`日額${num(day)}円・残${zan}日/${sh}日`;
    $('rate').textContent=Math.round(rate*100)+'%';$('ratio').textContent=Math.round(ratio*100)+'%';$('judge').textContent=judge;
    show();anim($('big'),0,total,800);
    SHARE=`再就職手当シミュ、約${yen(total)}（支給率${Math.round(rate*100)}%）もらえる計算でした🎯`;}''')

add(id='pfc-balance', cat=HEALTH, emoji='🍱',
  title='PFCバランス 計算｜目標カロリーから三大栄養素のグラムは？｜シミュラボ',
  desc='1日の目標カロリーとPFCの比率から、タンパク質・脂質・炭水化物それぞれの必要グラム数を計算する無料ツール。ダイエット・筋トレに。',
  ogtitle='PFCバランス 計算｜P/F/Cのグラムは？', ogdesc='目標カロリーとPFC比率から三大栄養素のグラムを計算。',
  h1='PFCバランス 計算ツール',
  lead='1日の目標カロリーを、タンパク質・脂質・炭水化物（PFC）に振り分けると何グラム？目的別の比率でPFCのグラム数を計算します。',
  inputs='''    <h2>🍱 条件を入れる</h2>
    <div class="row"><div class="field"><label>1日の目標カロリー <span class="hint">（kcal）</span></label><input type="number" id="cal" value="2000" min="0" inputmode="numeric"></div>
    <div class="field"><label>目的（PFC比率）</label><select id="mode"><option value="standard" selected>標準(P15:F25:C60)</option><option value="diet">ダイエット(P30:F20:C50)</option><option value="muscle">筋肥大(P30:F25:C45)</option><option value="lowcarb">低糖質(P30:F40:C30)</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">PFCを計算する</button>''',
  result='''      <div class="label">タンパク質(P)</div>
      <div class="big"><span id="big">0</span><span class="unit">g</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">脂質(F)</div><div class="v accent" id="f">—</div></div>
      <div class="stat"><div class="k">炭水化物(C)</div><div class="v" id="c">—</div></div>
      <div class="stat"><div class="k">総カロリー</div><div class="v" id="calv">—</div></div></div>''',
  article=C('PFCのグラムは「カロリー × 各比率 ÷ そのkcal」で計算。<b>タンパク質4kcal/g・脂質9kcal/g・炭水化物4kcal/g</b>です。')+'''
    <h2>PFCバランスとは</h2>
    <p>PFCは三大栄養素（Protein＝タンパク質、Fat＝脂質、Carbohydrate＝炭水化物）。同じカロリーでも、この配分で体づくりの結果が変わります。ダイエットや筋トレでは、まずタンパク質を確保するのが基本です。</p>
    <div class="note"><strong>計算式</strong><br>P(g) ＝ カロリー×P比率 ÷ 4<br>F(g) ＝ カロリー×F比率 ÷ 9<br>C(g) ＝ カロリー×C比率 ÷ 4</div>
    <h2>目的別のPFC比率の目安</h2>
    <table class="seo-table"><tr><th>目的</th><th>P:F:C</th></tr>
    <tr><td>標準・維持</td><td>15:25:60</td></tr>
    <tr><td>ダイエット</td><td>30:20:50</td></tr>
    <tr><td>筋肥大</td><td>30:25:45</td></tr>
    <tr><td>低糖質</td><td>30:40:30</td></tr></table>
    <h2>よくある質問</h2>'''+faq([('まず何を意識する？','タンパク質を体重×1.5〜2g確保するのが基本。残りを脂質・炭水化物で配分します。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['厚生労働省「エネルギー産生栄養素バランス」']),
  js='''  const M={standard:[15,25,60],diet:[30,20,50],muscle:[30,25,45],lowcarb:[30,40,30]};
  function calc(){const cal=Math.max(0,+$('cal').value||0),m=M[$('mode').value]||M.standard;
    const p=cal*m[0]/100/4, f=cal*m[1]/100/9, c=cal*m[2]/100/4;
    $('sub').textContent=`${num(cal)}kcal・P${m[0]}:F${m[1]}:C${m[2]}`;
    $('f').textContent=num(f)+'g';$('c').textContent=num(c)+'g';$('calv').textContent=num(cal)+'kcal';
    show();anim($('big'),0,p,800);
    SHARE=`PFCバランス、${num(cal)}kcalならP${num(p)}g・F${num(f)}g・C${num(c)}gでした🍱`;}''')

add(id='mental-leap', cat=KIDS, emoji='👶',
  title='メンタルリープ 計算｜赤ちゃんのぐずり期はいつ？週数で判定｜シミュラボ',
  desc='赤ちゃんの生年月日（出産予定日）から、ぐずりや甘えが増える「メンタルリープ」の時期を週数で計算し、次のぐずり期までの目安を表示する無料ツール。',
  ogtitle='メンタルリープ 計算｜次のぐずり期は？', ogdesc='赤ちゃんの週数からメンタルリープ(ぐずり期)を判定。',
  h1='メンタルリープ 計算ツール',
  lead='赤ちゃんが急にぐずる「メンタルリープ」。生年月日から今の週数を出し、いまがぐずり期か、次のぐずり期はいつかを判定します（目安）。',
  inputs='''    <h2>👶 赤ちゃんの生年月日</h2>
    <div class="field"><label>生年月日（予定日でもOK）</label><input type="date" id="bd" value="2026-03-01"></div>
    <button class="btn btn-primary" id="calcBtn">ぐずり期を調べる</button>''',
  result='''      <div class="label">今の週数（修正なし）</div>
      <div class="big"><span id="big">0</span><span class="unit">週</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">いまの状態</div><div class="v accent" id="state">—</div></div>
      <div class="stat"><div class="k">次のぐずり期</div><div class="v" id="next">—</div></div>
      <div class="stat"><div class="k">その時期</div><div class="v" id="when">—</div></div></div>''',
  article=C('メンタルリープは、赤ちゃんの知能がぐんと発達する前後にぐずりが増える時期。生後 <b>約5・8・12・19・26・37・46・55週</b> ごろに訪れるとされます。')+'''
    <h2>メンタルリープ（ぐずり期）とは</h2>
    <p>メンタルリープは、赤ちゃんの「精神的な飛躍（脳の発達）」の前に、ぐずり・後追い・甘えが増える時期のこと。生後1年半ほどの間に約10回訪れるとされ、「魔の3週目」「黄昏泣き」もこの一種と言われます。</p>
    <div class="note"><strong>ぐずり期の目安（生後）</strong><br>約5週・8週・12週・19週・26週・37週・46週・55週<br>※早産児は出産予定日を基準に補正してください</div>
    <p>ぐずりは成長のサイン。長くは続かないので、抱っこやスキンシップで乗り切りましょう。本ツールは目安です。</p>
    <h2>よくある質問</h2>'''+faq([('ぐずり期はどれくらい続く？','数日〜2週間ほどで落ち着くことが多いとされます。個人差があります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['「ワンダーウィーク（メンタルリープ）」研究']),
  js='''  const L=[5,8,12,19,26,37,46,55];
  function calc(){const v=$('bd').value; if(!v){return;}
    const bd=new Date(v+'T00:00:00'); const now=new Date(); now.setHours(0,0,0,0);
    const wk=Math.floor((now-bd)/86400000/7);
    if(wk<0){$('sub').textContent='まだ生まれていません（予定日前）';show();return;}
    let inLeap=L.some(l=>Math.abs(wk-l)<=1);
    let nx=L.find(l=>l>wk);
    $('sub').textContent=`${bd.getFullYear()}/${bd.getMonth()+1}/${bd.getDate()} 生まれ`;
    $('state').textContent=inLeap?'ぐずり期かも':'落ち着き期';
    $('next').textContent=nx?('生後'+nx+'週'):'リープ期終了';
    $('when').textContent=nx?('あと'+(nx-wk)+'週ごろ'):'—';
    show();anim($('big'),0,wk,700);
    SHARE=`メンタルリープ、生後${wk}週で${inLeap?'いまぐずり期かも':'落ち着き期'}でした👶 次は生後${nx||'-'}週`;}''')

add(id='kaigohoken-ryou', cat=SENIOR, emoji='🧓',
  title='介護保険料 計算｜40歳以上の介護保険料はいくら？｜シミュラボ',
  desc='年齢区分と月給または所得から、介護保険料（40〜64歳は給与天引き／65歳以上は所得段階）の目安を計算する無料シミュレーター。',
  ogtitle='介護保険料 計算｜いくら払う？', ogdesc='40〜64歳・65歳以上の介護保険料の目安を計算。',
  h1='介護保険料 計算シミュレーター',
  lead='40歳になると始まる介護保険料。年齢区分と収入から、毎月（毎年）の介護保険料の目安を計算します。',
  inputs='''    <h2>🧓 条件を入れる</h2>
    <div class="field"><label>年齢区分</label><select id="kbn"><option value="2" selected>40〜64歳（給与天引き）</option><option value="1">65歳以上（年金天引き）</option></select></div>
    <div class="row"><div class="field"><label id="lab">月給（額面・万円）</label><input type="number" id="x" value="30" min="0" inputmode="numeric"></div>
    <div class="field"><label>区分(65歳以上のみ)</label><select id="dan"><option value="1.0" selected>標準(第5段階)</option><option value="0.5">住民税非課税</option><option value="1.3">本人課税</option><option value="1.7">高所得</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">介護保険料を計算する</button>''',
  result='''      <div class="label">介護保険料（目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">区分</div><div class="v accent" id="kv">—</div></div>
      <div class="stat"><div class="k">月あたり</div><div class="v" id="mo">—</div></div>
      <div class="stat"><div class="k">納め方</div><div class="v" id="how">—</div></div></div>''',
  article=C('介護保険料は <b>40歳から生涯</b> 払います。40〜64歳は健康保険に上乗せ（給与天引き・本人約0.9%）、65歳以上は所得段階別の定額（年金天引き）です。')+'''
    <h2>介護保険料のしくみ</h2>
    <p>40歳になった月から介護保険の被保険者となり、保険料の納付が始まります。40〜64歳（第2号）は加入している医療保険と一緒に徴収。65歳以上（第1号）は市区町村ごとの基準額に所得段階の倍率をかけた定額で、原則年金から天引きされます。</p>
    <div class="note"><strong>目安</strong><br>40〜64歳：月給 × 約0.9%（本人負担・労使折半後）<br>65歳以上：基準額(月約6,000円)× 所得段階の倍率(0.5〜1.7など)</div>
    <p>料率・基準額は加入する保険や自治体で異なります。本ツールは概算です。</p>
    <h2>よくある質問</h2>'''+faq([('いつまで払う？','介護保険料は40歳から生涯、納め続けます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['厚生労働省「介護保険制度」']),
  js='''  document.getElementById('kbn').addEventListener('change',function(){$('lab').textContent=this.value==='1'?'（65歳以上は段階で計算）':'月給（額面・万円）';});
  function calc(){const kbn=$('kbn').value;let mo,kv,how;
    if(kbn==='2'){const g=Math.max(0,+$('x').value||0)*10000;mo=g*0.009;kv='40〜64歳';how='給与天引き';$('sub').textContent=`40〜64歳・月給${num(g/10000)}万円`;}
    else{const base=6000,d=+$('dan').value||1;mo=base*d;kv='65歳以上';how='年金天引き';$('sub').textContent=`65歳以上・倍率${d}`;}
    $('kv').textContent=kv;$('mo').textContent=yen(mo);$('how').textContent=how;
    show();anim($('big'),0,mo*12,800);
    SHARE=`介護保険料シミュ、年 約${yen(mo*12)}（月${yen(mo)}）の計算でした🧓`;}''')

add(id='tekika-keisan', cat=HEALTH, emoji='💧',
  title='点滴 滴下数 計算｜1分間の滴下数を自動計算（看護）｜シミュラボ',
  desc='指示された輸液量・時間と、輸液セットの滴下数（20滴or60滴）から、1分間の滴下数・10秒あたりの滴数を計算する看護師向け無料ツール。',
  ogtitle='点滴 滴下数 計算｜1分間の滴下数は？', ogdesc='輸液量・時間・滴下セットから1分間の滴下数を計算。',
  h1='点滴 滴下数 計算ツール',
  lead='点滴の滴下数を一発計算。指示された輸液量・時間と、輸液セット（成人用20滴／小児用60滴）から、1分間・10秒あたりの滴下数を求めます。',
  inputs='''    <h2>💧 条件を入れる</h2>
    <div class="row"><div class="field"><label>輸液量 <span class="hint">（mL）</span></label><input type="number" id="ml" value="500" min="0" inputmode="numeric"></div>
    <div class="field"><label>指示時間 <span class="hint">（時間）</span></label><input type="number" id="hr" value="2" min="0" step="0.5" inputmode="decimal"></div></div>
    <div class="field"><label>輸液セット</label><select id="gtt"><option value="20" selected>成人用（20滴=1mL）</option><option value="60">小児用（60滴=1mL）</option></select></div>
    <button class="btn btn-primary" id="calcBtn">滴下数を計算する</button>''',
  result='''      <div class="label">1分間の滴下数</div>
      <div class="big"><span id="big">0</span><span class="unit">滴/分</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">10秒あたり</div><div class="v accent" id="ten">—</div></div>
      <div class="stat"><div class="k">1時間の量</div><div class="v" id="hrml">—</div></div>
      <div class="stat"><div class="k">総滴数</div><div class="v" id="total">—</div></div></div>''',
  article=C('滴下数(滴/分) ＝ <b>輸液量(mL) × 滴下セット(20 or 60) ÷ 指示時間(分)</b>。10秒あたりに直すと数えやすくなります。')+'''
    <h2>滴下数の計算方法</h2>
    <p>点滴の速度は1分間の滴下数で管理します。輸液セットは成人用が1mL＝20滴、小児用（微量用）が1mL＝60滴です。指示された量を時間で割り、滴下数に換算します。</p>
    <div class="note"><strong>計算式</strong><br>1分間の滴下数 ＝ 総量(mL) × セット係数(20/60) ÷ 総時間(分)<br>10秒あたり ＝ 1分の滴下数 ÷ 6</div>
    <p>実際は患者さんの状態や指示に従ってください。本ツールは計算補助です。</p>
    <h2>よくある質問</h2>'''+faq([('20滴と60滴の違いは？','成人用は1mL=20滴、小児・微量用は1mL=60滴。セットの表示を確認しましょう。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['看護技術「輸液・点滴の滴下数計算」']),
  js='''  function calc(){const ml=Math.max(0,+$('ml').value||0),hr=Math.max(0,+$('hr').value||0),gtt=+$('gtt').value||20;
    const min=hr*60, drops=min>0?ml*gtt/min:0;
    $('sub').textContent=`${num(ml)}mL・${hr}時間・${gtt}滴セット`;
    $('ten').textContent=(drops/6).toFixed(1)+'滴';$('hrml').textContent=(hr>0?num(ml/hr):0)+'mL';$('total').textContent=num(ml*gtt)+'滴';
    show();anim($('big'),0,drops,800,0);
    SHARE=`点滴 滴下数シミュ、${num(ml)}mLを${hr}時間→ ${Math.round(drops)}滴/分（10秒で${(drops/6).toFixed(1)}滴）でした💧`;}''')

add(id='koutsuhi-hikazei', cat=WORK, emoji='🚆',
  title='通勤交通費 非課税限度 計算｜交通費はいくらまで非課税？｜シミュラボ',
  desc='1か月の通勤費から、非課税となる通勤手当の限度額（公共交通機関は月15万円まで）と、課税される超過分を計算する無料ツール。',
  ogtitle='通勤交通費 非課税限度｜いくらまで非課税？', ogdesc='通勤費の非課税限度額と課税される超過分を計算。',
  h1='通勤交通費 非課税限度 計算',
  lead='通勤手当はいくらまで税金がかからない？1か月の通勤費から、非課税になる額と、課税される超過分を計算します（公共交通機関）。',
  inputs='''    <h2>🚆 条件を入れる</h2>
    <div class="field"><label>1か月の通勤費 <span class="hint">（円）</span></label><input type="number" id="m" value="20000" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">非課税額を計算する</button>''',
  result='''      <div class="label">非課税になる通勤手当</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">課税される分</div><div class="v accent" id="kazei">—</div></div>
      <div class="stat"><div class="k">非課税の上限</div><div class="v" id="genka">—</div></div>
      <div class="stat"><div class="k">判定</div><div class="v" id="judge">—</div></div></div>''',
  article=C('公共交通機関の通勤手当は <b>月15万円まで非課税</b>。これを超える分は給与として課税されます。マイカー通勤は距離別の限度額です。')+'''
    <h2>通勤手当の非課税限度</h2>
    <p>会社からもらう通勤手当は、一定額まで所得税・住民税がかかりません。電車・バスなどの公共交通機関は「最も経済的・合理的な経路の運賃」で、月15万円が上限です。</p>
    <h2>マイカー通勤の非課税限度（片道距離・月額）</h2>
    <table class="seo-table"><tr><th>片道距離</th><th>非課税限度(月)</th></tr>
    <tr><td>2km未満</td><td>全額課税</td></tr>
    <tr><td>2〜10km</td><td>4,200円</td></tr>
    <tr><td>10〜15km</td><td>7,100円</td></tr>
    <tr><td>15〜25km</td><td>12,900円</td></tr>
    <tr><td>25〜35km</td><td>18,700円</td></tr></table>
    <p>本ツールは公共交通機関（月15万上限）で計算します。</p>
    <h2>よくある質問</h2>'''+faq([('超えたらどうなる？','超過分は給与扱いとなり、所得税・住民税・社会保険料の対象になります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['国税庁「通勤手当の非課税限度額」']),
  js='''  function calc(){const m=Math.max(0,+$('m').value||0),lim=150000;
    const hi=Math.min(m,lim), kazei=Math.max(0,m-lim);
    $('sub').textContent=`1か月の通勤費 ${yen(m)}`;
    $('kazei').textContent=yen(kazei);$('genka').textContent=yen(lim);$('judge').textContent=kazei>0?'一部課税':'全額非課税';
    show();anim($('big'),0,hi,700);
    SHARE=`通勤交通費シミュ、${yen(m)}のうち非課税は${yen(hi)}（課税${yen(kazei)}）でした🚆`;}''')

add(id='nenshu-keisan', cat=WORK, emoji='💴',
  title='年収 計算｜月給と賞与から額面年収・手取りを計算｜シミュラボ',
  desc='毎月の額面給与と賞与（年）から、額面年収と、税・社会保険を引いた手取り年収・月の手取りの目安を計算する無料シミュレーター。',
  ogtitle='年収 計算｜月給から年収・手取りは？', ogdesc='月給と賞与から額面年収と手取りの目安を計算。',
  h1='年収 計算シミュレーター',
  lead='毎月の給料とボーナスから、額面年収はいくら？さらに税・社会保険を引いた手取りの目安も計算します。',
  inputs='''    <h2>💴 条件を入れる</h2>
    <div class="row"><div class="field"><label>毎月の額面給与 <span class="hint">（万円）</span></label><input type="number" id="m" value="28" min="0" inputmode="numeric"></div>
    <div class="field"><label>賞与（年間・額面） <span class="hint">（万円）</span></label><input type="number" id="b" value="80" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">年収・手取りを計算する</button>''',
  result='''      <div class="label">額面年収</div>
      <div class="big"><span id="big">0</span><span class="unit">万円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">手取り年収(概算)</div><div class="v accent" id="tedori">—</div></div>
      <div class="stat"><div class="k">月の手取り</div><div class="v" id="motedori">—</div></div>
      <div class="stat"><div class="k">手取り率</div><div class="v" id="rate">—</div></div></div>''',
  article=C('額面年収 ＝ <b>月給 × 12 ＋ 賞与</b>。手取りは税・社会保険で約 <b>75〜85%</b>（年収が高いほど手取り率は下がります）。')+'''
    <h2>年収と手取りの違い</h2>
    <p>「年収」は税・社会保険を引く前の額面（総支給）です。実際に使えるのは、そこから所得税・住民税・社会保険料を引いた「手取り」。手取り率は年収が上がるほど下がります（累進課税のため）。</p>
    <div class="note"><strong>手取り率の目安</strong><br>年収300万 → 約80%／500万 → 約78%／700万 → 約76%／1000万 → 約72%</div>
    <p>本ツールは独身・概算です。扶養や控除で手取りは変わります。</p>
    <h2>よくある質問</h2>'''+faq([('額面と手取りどっちが年収？','一般に「年収」は額面（総支給）を指します。求人票の年収も額面です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['国税庁・日本年金機構 各種料率']),
  js='''  function calc(){const m=Math.max(0,+$('m').value||0),b=Math.max(0,+$('b').value||0);
    const nen=(m*12+b)*10000; let r; if(nen<3000000)r=0.81;else if(nen<5000000)r=0.79;else if(nen<7000000)r=0.77;else if(nen<10000000)r=0.74;else r=0.71;
    const ted=nen*r;
    $('sub').textContent=`月${m}万×12＋賞与${b}万`;
    $('tedori').textContent=num(ted/10000)+'万円';$('motedori').textContent=yen(ted/12);$('rate').textContent=Math.round(r*100)+'%';
    show();anim($('big'),0,nen/10000,800);
    SHARE=`年収計算、額面${num(nen/10000)}万円→手取り 約${num(ted/10000)}万円（手取り率${Math.round(r*100)}%）でした💴`;}''')

add(id='roudou-bunpai', cat=BIZ, emoji='📊',
  title='労働分配率 計算｜人件費は適正？粗利からの割合を計算｜シミュラボ',
  desc='粗利益（売上総利益）と人件費から、労働分配率を計算し、業種別の目安と比べて人件費が適正かを判定する無料シミュレーター。',
  ogtitle='労働分配率 計算｜人件費は適正？', ogdesc='粗利と人件費から労働分配率を計算し目安と比較。',
  h1='労働分配率 計算シミュレーター',
  lead='人件費は適正？粗利益に対して人件費がどれくらいかを示す「労働分配率」を計算し、業種の目安と比べます。経営・採用の判断に。',
  inputs='''    <h2>📊 条件を入れる</h2>
    <div class="row"><div class="field"><label>粗利益（売上総利益） <span class="hint">（万円/年）</span></label><input type="number" id="g" value="5000" min="0" inputmode="numeric"></div>
    <div class="field"><label>人件費（年・総額） <span class="hint">（万円/年）</span></label><input type="number" id="p" value="2500" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">労働分配率を計算する</button>''',
  result='''      <div class="label">労働分配率</div>
      <div class="big"><span id="big">0</span><span class="unit">%</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">判定</div><div class="v accent" id="judge">—</div></div>
      <div class="stat"><div class="k">1人増やすと</div><div class="v" id="add">—</div></div>
      <div class="stat"><div class="k">粗利</div><div class="v" id="gv">—</div></div></div>
      <div class="anim-bar" id="bw"><span id="bar"></span><b id="bl"></b></div>
      <div class="anim-cap">労働分配率（目安50%前後）</div>''',
  article=C('労働分配率 ＝ <b>人件費 ÷ 粗利益 × 100</b>。一般に <b>50%前後</b> が目安で、高すぎると利益を圧迫、低すぎると待遇不足のサインです。')+'''
    <h2>労働分配率とは</h2>
    <p>労働分配率は、企業が生み出した付加価値（粗利益）のうち、どれだけを人件費に充てているかを示す指標です。高いほど従業員に還元している一方、利益は出にくくなります。採用や昇給の判断、自社の健全性チェックに使われます。</p>
    <div class="note"><strong>計算式</strong><br>労働分配率(%) ＝ 人件費 ÷ 粗利益（売上総利益）× 100</div>
    <h2>業種別の目安</h2>
    <table class="seo-table"><tr><th>業種</th><th>目安</th></tr>
    <tr><td>飲食・サービス業</td><td>50〜60%</td></tr>
    <tr><td>小売業</td><td>40〜50%</td></tr>
    <tr><td>製造業</td><td>45〜55%</td></tr></table>
    <h2>よくある質問</h2>'''+faq([('高いと悪い？','高すぎると利益を圧迫しますが、低すぎても人材定着に問題が出ます。バランスが大切です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['中小企業庁「中小企業実態基本調査」']),
  js='''  function calc(){const g=Math.max(0,+$('g').value||0),p=Math.max(0,+$('p').value||0);
    const r=g>0?p/g*100:0; let judge; if(r<40)judge='低め(余力あり)';else if(r<=60)judge='適正の範囲';else judge='高め(要注意)';
    $('sub').textContent=`粗利${num(g)}万・人件費${num(p)}万`;
    $('judge').textContent=judge;$('add').textContent=g>0?('+'+(400/g*100).toFixed(1)+'pt/年400万'):'—';$('gv').textContent=num(g)+'万';
    const pct=Math.min(100,Math.round(r));$('bar').style.width='0%';setTimeout(()=>{$('bar').style.width=pct+'%';},40);$('bl').textContent=r.toFixed(1)+'%';
    show();anim($('big'),0,r,800,1);
    SHARE=`労働分配率シミュ、${r.toFixed(1)}%（${judge}）でした📊`;}''')

add(id='metabo-handan', cat=HEALTH, emoji='📏',
  title='メタボ判定 計算｜腹囲とBMIでメタボリスクをチェック｜シミュラボ',
  desc='腹囲・身長・体重から、BMIとメタボリックシンドロームの基準（腹囲 男性85cm・女性90cm以上）に照らしてリスクの目安を判定する無料ツール。',
  ogtitle='メタボ判定｜腹囲とBMIでチェック', ogdesc='腹囲とBMIからメタボリスクの目安を判定。',
  h1='メタボ判定 計算ツール',
  lead='お腹まわり、大丈夫？腹囲・身長・体重から、BMIとメタボの基準（腹囲 男85cm・女90cm）でリスクの目安を判定します（医療判断は受診を）。',
  inputs='''    <h2>📏 条件を入れる</h2>
    <div class="row"><div class="field"><label>性別</label><select id="sex"><option value="m">男性</option><option value="f">女性</option></select></div>
    <div class="field"><label>腹囲 <span class="hint">（cm・へそ周り）</span></label><input type="number" id="w2" value="85" min="40" max="200" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>身長 <span class="hint">（cm）</span></label><input type="number" id="h" value="170" min="100" max="230" inputmode="numeric"></div>
    <div class="field"><label>体重 <span class="hint">（kg）</span></label><input type="number" id="w" value="68" min="20" max="250" step="0.1" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">メタボ判定する</button>''',
  result='''      <div class="label">あなたのBMI</div>
      <div class="big"><span id="big">0</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">腹囲判定</div><div class="v accent" id="fukui">—</div></div>
      <div class="stat"><div class="k">肥満判定</div><div class="v" id="himan">—</div></div>
      <div class="stat"><div class="k">メタボ傾向</div><div class="v" id="meta">—</div></div></div>''',
  article=C('メタボの基準は <b>腹囲 男性85cm・女性90cm以上</b>。これに高血圧・高血糖・脂質異常のうち2つ以上が重なると「メタボリックシンドローム」と判定されます。')+'''
    <h2>メタボリックシンドロームとは</h2>
    <p>内臓脂肪型肥満（腹囲が基準以上）に加え、血圧・血糖・脂質の異常が複数重なった状態です。本ツールは腹囲とBMIから「内臓脂肪の目安」をチェックするもので、血圧などの数値は含みません。</p>
    <div class="note"><strong>基準</strong><br>腹囲：男性85cm以上／女性90cm以上<br>BMI：体重(kg)÷身長(m)²、25以上で肥満</div>
    <p>正確な診断は健康診断・医療機関で。腹囲が気になる方は食事と運動の見直しを。</p>
    <h2>よくある質問</h2>'''+faq([('腹囲はどこを測る？','立った状態で、へその高さの胴回りを測ります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['厚生労働省 e-ヘルスネット「メタボリックシンドローム」']),
  js='''  function calc(){const sex=$('sex').value,fw=Math.max(0,+$('w2').value||0),h=Math.max(1,+$('h').value||1)/100,w=Math.max(0,+$('w').value||0);
    const bmi=w/(h*h), lim=sex==='m'?85:90, over=fw>=lim;
    let hi; if(bmi<18.5)hi='低体重';else if(bmi<25)hi='普通';else hi='肥満';
    let meta; if(over&&bmi>=25)meta='要注意';else if(over||bmi>=25)meta='予備軍の可能性';else meta='基準内';
    $('sub').textContent=`${sex==='m'?'男性':'女性'}・腹囲${fw}cm・${$('h').value}cm/${w}kg`;
    $('fukui').textContent=over?('基準超('+lim+'cm)'):'基準内';$('himan').textContent=hi;$('meta').textContent=meta;
    show();anim($('big'),0,bmi,800,1);
    SHARE=`メタボ判定、BMI${bmi.toFixed(1)}・腹囲${fw}cm→「${meta}」でした📏`;}''')

# ========================= 診断 18本（quizヘルパー） =========================

def dq(id, cat, emoji, title, desc, ogt, ogd, h1, lead, qs, bands, intro, types_label, faqs, refs, share_pre):
    inp = '    <h2>'+emoji+' 質問に答えてね</h2>\n'
    for i,(q,opts) in enumerate(qs):
        o = ''.join('<option value="%d">%s</option>' % (s, l) for l,s in opts)
        inp += '    <div class="field"><label>%s</label><select id="q%d">%s</select></div>\n' % (q, i, o)
    inp += '    <button class="btn btn-primary" id="calcBtn">診断する</button>'
    res = ('      <div class="seo-anim ptag-stage" id="stg"><div class="pop-emoji" id="ico">'+emoji+'''</div></div>
      <div class="label">あなたのタイプは</div>
      <div class="big" style="font-size:30px"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:16px">—</div>''')
    bandjs = ','.join('[%d,%s,%s]' % (b[0], J(b[1]), J(b[2])) for b in bands)
    js = ('  const B=['+bandjs+'''];
  function calc(){let s=0; const n='''+str(len(qs))+'''; for(let i=0;i<n;i++)s+=(+$('q'+i).value||0);
    let t=B[B.length-1]; for(const b of B){ if(s<=b[0]){ t=b; break; } }
    $('big').textContent=t[1]; $('sub').textContent='スコア '+s+'点';
    $('adv').innerHTML='<strong>'+t[1]+'</strong><br>'+t[2];
    const ic=$('ico'); ic.classList.remove('on'); void ic.offsetWidth; ic.classList.add('on');
    show(); SHARE='''+J(share_pre)+'''+t[1]+'でした'+'''+J(emoji)+''';}''')
    article = (C(intro) + '\n    <h2>診断でわかるタイプ</h2>\n    <p>'+types_label+'</p>\n    <div class="note">この診断は、いくつかの質問への回答を点数化して傾向を判定するエンタメ診断です。気軽に楽しんでください。</div>\n    <h2>よくある質問</h2>' + faq(faqs) + REF(refs))
    add(id=id, cat=cat, emoji=emoji, title=title, desc=desc, ogtitle=ogt, ogdesc=ogd, h1=h1, lead=lead, inputs=inp, result=res, article=article, js=js)

YN = lambda hi,mid,lo: [(hi[0],hi[1]),(mid[0],mid[1]),(lo[0],lo[1])]

dq('sake-type', MENTAL, '🍶', '酒タイプ診断｜あなたのお酒の飲み方タイプは？｜シミュラボ',
  'お酒の好みや飲み方の質問から、あなたの「酒タイプ」を診断する無料エンタメ診断。',
  '酒タイプ診断｜お酒の飲み方タイプは？','質問に答えてお酒の飲み方タイプを診断。',
  '酒タイプ診断','お酒の好みや飲み方から、あなたの「酒タイプ」を診断します。飲み会前の話のネタにどうぞ（エンタメ診断）。',
  [('お酒の強さは？',[('かなり強い',4),('普通',2),('弱い・飲めない',0)]),
   ('飲むペースは？',[('じっくり長く',0),('普通',2),('ハイペース',4)]),
   ('好きな場面は？',[('家でひとり晩酌',0),('少人数でしっぽり',2),('大人数でワイワイ',4)]),
   ('翌日は？',[('ケロッと元気',4),('ぼちぼち',2),('二日酔いしがち',0)])],
  [(4,'マイペース癒し系','自分のリズムで楽しむタイプ。無理せず晩酌を楽しむのが◎。'),
   (9,'バランス飲兵衛','場に合わせて楽しめる万能タイプ。適量を守れば最高の飲み相手。'),
   (16,'パーティー番長','盛り上げ上手な宴会の主役タイプ。飲みすぎ注意で純アルコール量も意識して。')],
  'お酒の強さ・ペース・好きな場面から、3つの飲み方タイプに分類します。','癒し系／バランス型／パーティー型などに分かれます。',
  [('当たってる？','傾向を点数化したエンタメ診断です。適量飲酒を心がけてください。'),('データは送信される？','いいえ、ブラウザ内で完結します。')],
  ['厚生労働省「適正飲酒」'], '酒タイプ診断、私は')

dq('maegami-shindan', BEAUTY, '💇', '前髪診断｜あなたに似合う前髪のタイプは？｜シミュラボ',
  '顔の印象やなりたいイメージの質問から、似合う前髪のタイプ（ぱっつん・流し・なし等）を提案する無料診断。',
  '前髪診断｜似合う前髪は？','質問に答えて似合う前髪タイプを提案。',
  '前髪診断','なりたい印象や雰囲気から、似合う前髪のタイプを提案します（エンタメ診断）。美容院のオーダーの参考にも。',
  [('なりたい印象は？',[('かわいい・若見え',0),('ナチュラル',2),('大人っぽい・クール',4)]),
   ('おでこは出したい？',[('隠したい',0),('どちらでも',2),('出したい',4)]),
   ('スタイリングは？',[('楽がいい',0),('そこそこ',2),('しっかりやる',4)])],
  [(3,'ぱっつん／重め前髪','目力アップで可愛い印象に。若見え効果も。'),
   (8,'流し前髪・シースルー','ナチュラルで好感度◎。誰にでも似合う万能タイプ。'),
   (12,'前髪なし・かきあげ','大人っぽく洗練された印象。おでこを見せて抜け感を。')],
  'なりたい印象・おでこ・スタイリング頻度から似合う前髪を提案します。','ぱっつん／流し・シースルー／前髪なしに分かれます。',
  [('本当に似合う？','あくまで提案です。美容師さんに相談すると確実です。'),('データは送信される？','いいえ、ブラウザ内で完結します。')],
  ['ヘアスタイルの一般的な印象論'], '前髪診断、私に似合うのは')

dq('mote-type', LOVE, '💘', 'モテタイプ診断｜あなたのモテ方のタイプは？｜シミュラボ',
  '恋愛の傾向の質問から、あなたの「モテタイプ」を診断する無料エンタメ診断。',
  'モテタイプ診断｜あなたのモテ方は？','質問に答えてモテタイプを診断。',
  'モテタイプ診断','あなたがどんなふうにモテるタイプかを診断します（エンタメ診断）。',
  [('初対面では？',[('受け身',0),('普通',2),('自分から話す',4)]),
   ('気になる人には？',[('そっと見守る',0),('さりげなく',2),('グイグイ',4)]),
   ('まわりからの印象は？',[('癒し系',0),('親しみやすい',2),('華やか',4)])],
  [(3,'癒し系モテ','一緒にいてホッとする安心感でモテるタイプ。'),
   (8,'親しみ系モテ','話しやすさと気さくさで好かれる人気者タイプ。'),
   (12,'華やかモテ','存在感とアプローチ力で惹きつけるタイプ。')],
  '初対面・アプローチ・印象から3つのモテタイプに分類します。','癒し系／親しみ系／華やか系に分かれます。',
  [('当たってる？','エンタメ診断です。話のネタにどうぞ。'),('データは送信される？','いいえ、ブラウザ内で完結します。')],
  ['恋愛傾向の一般論'], 'モテタイプ診断、私は')

dq('tsundere-shindan', LOVE, '😼', 'ツンデレ診断｜あなたのツンデレ度は？｜シミュラボ',
  '好きな人への態度の質問から、あなたのツンデレ度・タイプを診断する無料エンタメ診断。',
  'ツンデレ診断｜あなたのツンデレ度は？','質問に答えてツンデレ度を診断。',
  'ツンデレ診断','好きな人への態度から、あなたのツンデレ度を診断します（エンタメ診断）。',
  [('好きな人につい…',[('素直に甘える',0),('普通',2),('そっけなくしちゃう',4)]),
   ('褒められると？',[('喜ぶ',0),('照れる',2),('「べつに」と言う',4)]),
   ('本音は？',[('すぐ言える',0),('時々隠す',2),('なかなか言えない',4)])],
  [(3,'デレデレさん','素直で愛情表現がストレート。一緒にいて分かりやすい安心タイプ。'),
   (8,'ほどよくツンデレ','普段はクール、たまに見せる甘えがギャップ萌え。'),
   (12,'ガチツンデレ','照れ隠しが強め。素直になれた時の破壊力は抜群。')],
  '好きな人への態度・反応・本音の出し方からツンデレ度を判定します。','デレ型／ほどよいツンデレ／ガチツンデレに分かれます。',
  [('当たってる？','エンタメ診断です。'),('データは送信される？','いいえ、ブラウザ内で完結します。')],
  ['性格傾向の一般論'], 'ツンデレ診断、私は')

dq('aichaku-style', MENTAL, '🧷', '愛着スタイル診断｜あなたの人との距離感タイプは？｜シミュラボ',
  '人間関係や恋愛での距離感の質問から、愛着スタイル（安定型・不安型・回避型）の傾向を診断する無料診断。',
  '愛着スタイル診断｜距離感のタイプは？','質問に答えて愛着スタイルの傾向を診断。',
  '愛着スタイル診断','人との距離感や関わり方から、愛着スタイルの傾向を診断します（心理学ベースのエンタメ診断）。',
  [('相手の返信が遅いと？',[('気にしない',0),('少し気になる',2),('とても不安',4)]),
   ('深い関係になるのは？',[('心地よい',0),('普通',2),('ちょっと怖い',3)]),
   ('困ったとき人に頼るのは？',[('自然にできる',0),('時々',2),('苦手',4)]),
   ('ひとりの時間は？',[('好きだが寂しさも',2),('わりと平気',1),('絶対必要',4)])],
  [(4,'安定型','人を信頼し、適度な距離で安定した関係を築けるタイプ。'),
   (9,'不安型寄り','相手の気持ちが気になりやすいタイプ。安心できる関係づくりが鍵。'),
   (16,'回避型寄り','距離を取りたくなるタイプ。少しずつ頼る練習で関係が深まります。')],
  '返信・親密さ・頼り方などから、安定型／不安型／回避型の傾向を判定します。','安定型／不安型／回避型に分かれます。',
  [('診断は正確？','傾向を見るエンタメ診断です。深い悩みは専門家へ。'),('データは送信される？','いいえ、ブラウザ内で完結します。')],
  ['愛着理論（アタッチメント・スタイル）'], '愛着スタイル診断、私は')

dq('kaiwai-shindan', MENTAL, '🌐', '界隈診断｜あなたはどのネット界隈タイプ？｜シミュラボ',
  '趣味やSNSの使い方の質問から、あなたが属する「ネット界隈」タイプを診断する無料エンタメ診断。',
  '界隈診断｜あなたのネット界隈タイプは？','質問に答えてネット界隈タイプを診断。',
  '界隈診断','SNSの使い方や趣味から、あなたが馴染む「界隈」タイプを診断します（エンタメ診断）。',
  [('SNSでよく見るのは？',[('ニュース・学び',0),('趣味・推し',2),('ネタ・バズ',4)]),
   ('投稿スタイルは？',[('ほぼ見る専',0),('たまに投稿',2),('よく発信',4)]),
   ('熱中度は？',[('浅く広く',0),('そこそこ',2),('深く沼る',4)])],
  [(3,'まったり情報界隈','落ち着いて情報を楽しむ大人タイプ。'),
   (8,'推し活・趣味界隈','好きを深く楽しむ熱量タイプ。'),
   (12,'ネタ・バズ界隈','流行に敏感で発信好きなムードメーカー。')],
  'SNSの使い方・発信度・熱中度から3つの界隈タイプに分類します。','情報界隈／趣味界隈／ネタ界隈に分かれます。',
  [('当たってる？','エンタメ診断です。'),('データは送信される？','いいえ、ブラウザ内で完結します。')],
  ['SNS利用傾向の一般論'], '界隈診断、私は')

dq('personal-color', BEAUTY, '🎨', 'パーソナルカラー診断｜あなたはイエベ？ブルベ？｜シミュラボ',
  '肌・髪・瞳の色みの質問から、似合う色の傾向（イエベ春・夏・ブルベ秋・冬）を診断する無料セルフ診断。',
  'パーソナルカラー診断｜イエベ?ブルベ?','質問に答えてパーソナルカラーの傾向を診断。',
  'パーソナルカラー診断','肌・髪・瞳の印象から、似合う色の傾向（イエベ／ブルベ）をセルフ診断します（簡易版）。',
  [('地肌の色みは？',[('黄みがかる',0),('どちらとも',2),('青み・赤みがかる',4)]),
   ('似合うアクセは？',[('ゴールド',0),('どちらも',2),('シルバー',4)]),
   ('日焼けすると？',[('小麦色に',0),('普通',2),('赤くなる',4)]),
   ('得意な色は？',[('コーラル・オレンジ',0),('わからない',2),('ローズ・ブルー',4)])],
  [(5,'イエベ（イエローベース）','黄み・暖色が似合うタイプ。ゴールドやコーラルが得意。'),
   (10,'ニュートラル寄り','暖色・寒色どちらも似合うバランス型。幅広い色が楽しめます。'),
   (16,'ブルベ（ブルーベース）','青み・寒色が似合うタイプ。シルバーやローズが得意。')],
  '肌・アクセ・日焼け・得意色から、イエベ／ニュートラル／ブルベの傾向を判定します。','イエベ／ニュートラル／ブルベに分かれます。',
  [('正確に知りたい','光の下でのプロ診断が確実です。本ツールは簡易セルフ診断です。'),('データは送信される？','いいえ、ブラウザ内で完結します。')],
  ['パーソナルカラー(4シーズン)理論'], 'パーソナルカラー診断、私は')

dq('niau-kamigata', BEAUTY, '✂️', '似合う髪型診断｜あなたに似合うヘアスタイルは？｜シミュラボ',
  'なりたい印象や手入れの好みから、似合う髪型の長さ・テイストを提案する無料診断。',
  '似合う髪型診断｜似合うヘアは？','質問に答えて似合う髪型を提案。',
  '似合う髪型診断','なりたい印象やライフスタイルから、似合う髪型の方向性を提案します（エンタメ診断）。',
  [('なりたい雰囲気は？',[('かわいい',0),('ナチュラル',2),('かっこいい',4)]),
   ('手入れにかける時間は？',[('最小限',0),('普通',2),('しっかり',4)]),
   ('イメチェン願望は？',[('少し',0),('そこそこ',2),('大きく変えたい',4)])],
  [(3,'ふんわりミディアム','やわらかい印象で好感度◎。アレンジもしやすい万能レングス。'),
   (8,'ナチュラルボブ／ロング','こなれ感のある定番。自分らしさを活かせるタイプ。'),
   (12,'ショート／個性派スタイル','思い切った変化で新しい自分に。垢抜け効果大。')],
  'なりたい雰囲気・手入れ・イメチェン願望から方向性を提案します。','ミディアム／ボブ・ロング／ショート系に分かれます。',
  [('似合う保証はある？','提案です。骨格や髪質もあるので美容師さんに相談を。'),('データは送信される？','いいえ、ブラウザ内で完結します。')],
  ['ヘアスタイルの印象論'], '似合う髪型診断、私は')

dq('kamiiro-shindan', BEAUTY, '🌈', '髪色診断｜あなたに似合うヘアカラーは？｜シミュラボ',
  '肌の色みやなりたい印象から、似合うヘアカラーの方向性を提案する無料診断。',
  '髪色診断｜似合うヘアカラーは？','質問に答えて似合う髪色を提案。',
  '髪色診断','肌の印象やなりたい雰囲気から、似合うヘアカラーの方向性を提案します（エンタメ診断）。',
  [('肌の色みは？',[('黄みオークル',0),('標準',2),('青み・ピンク',4)]),
   ('なりたい印象は？',[('明るく元気',0),('ナチュラル',2),('落ち着き・透明感',4)]),
   ('挑戦度は？',[('定番でOK',0),('少し冒険',2),('派手もアリ',4)])],
  [(3,'暖色ブラウン系','黄み肌に映える王道カラー。オレンジ・ベージュ系が◎。'),
   (8,'ナチュラルブラウン系','誰にでも似合う定番。アッシュ寄りで抜け感も。'),
   (12,'寒色アッシュ・透明感系','青み肌に映える今っぽカラー。グレージュやブルー系が得意。')],
  '肌の色み・なりたい印象・挑戦度から似合う髪色を提案します。','暖色／ナチュラル／寒色アッシュに分かれます。',
  [('ブリーチは必要？','寒色や明るい色は必要なことも。美容師さんに相談を。'),('データは送信される？','いいえ、ブラウザ内で完結します。')],
  ['ヘアカラーとパーソナルカラーの関係'], '髪色診断、私に似合うのは')

dq('motedo-shindan', LOVE, '💖', 'モテ度診断｜あなたの今のモテ度は何点？｜シミュラボ',
  '見た目・気遣い・コミュニケーションの質問から、今のモテ度を点数で診断する無料エンタメ診断。',
  'モテ度診断｜今のモテ度は何点？','質問に答えて今のモテ度を診断。',
  'モテ度診断','見た目・気遣い・コミュ力から、いまのモテ度を診断します（エンタメ診断）。',
  [('身だしなみは？',[('正直さぼりがち',0),('普通',2),('いつも整える',4)]),
   ('人への気遣いは？',[('苦手',0),('人並み',2),('得意',4)]),
   ('会話の盛り上げは？',[('聞き役',1),('そこそこ',2),('得意',4)]),
   ('笑顔の頻度は？',[('少なめ',0),('普通',2),('いつも笑顔',4)])],
  [(4,'伸びしろたっぷり','少しの意識で大きく変わるタイプ。まずは笑顔と清潔感から。'),
   (10,'バランス good','十分モテる素質あり。気遣いをもう一押しで無敵。'),
   (16,'モテ偏差値高め','見た目・気遣い・会話のそろった人気者タイプ！')],
  '身だしなみ・気遣い・会話・笑顔からモテ度を点数化します。','伸びしろ型／バランス型／高モテ型に分かれます。',
  [('当たってる？','エンタメ診断です。改善のヒントにどうぞ。'),('データは送信される？','いいえ、ブラウザ内で完結します。')],
  ['第一印象・対人魅力の一般論'], 'モテ度診断、私は')

dq('inkya-shindan', MENTAL, '🌗', '陰キャ陽キャ診断｜あなたはどっち寄り？｜シミュラボ',
  '休日の過ごし方や人付き合いの質問から、陰キャ・陽キャの傾向を診断する無料エンタメ診断。',
  '陰キャ陽キャ診断｜あなたはどっち？','質問に答えて陰キャ陽キャ傾向を診断。',
  '陰キャ陽キャ診断','休日の過ごし方や人付き合いから、陰キャ・陽キャ傾向を診断します（エンタメ診断・優劣ではありません）。',
  [('休日は？',[('家でのんびり',0),('気分次第',2),('外で活動的',4)]),
   ('大人数の集まりは？',[('疲れる',0),('まあ平気',2),('大好き',4)]),
   ('初対面では？',[('緊張する',0),('普通',2),('すぐ打ち解ける',4)])],
  [(3,'インドア・陰キャ寄り','ひとり時間を大切にする落ち着きタイプ。深い関係を築くのが得意。'),
   (8,'バランス型（陰でも陽でもない）','状況で使い分けられる万能タイプ。いわゆる「陽キャ寄りの陰キャ」かも。'),
   (12,'アクティブ・陽キャ寄り','人と関わるのが好きなムードメーカータイプ。')],
  '休日・集まり・初対面の反応から陰陽の傾向を判定します。','陰キャ寄り／バランス型／陽キャ寄りに分かれます。',
  [('優劣ある？','ありません。どちらも魅力です。エンタメ診断です。'),('データは送信される？','いいえ、ブラウザ内で完結します。')],
  ['性格傾向（内向・外向）の一般論'], '陰キャ陽キャ診断、私は')

dq('tennen-do', MENTAL, '🍀', '天然度診断｜あなたの天然度は何％？｜シミュラボ',
  'うっかり度や思考の傾向の質問から、あなたの「天然度」を診断する無料エンタメ診断。',
  '天然度診断｜あなたの天然度は？','質問に答えて天然度を診断。',
  '天然度診断','うっかり度やマイペース度から、あなたの天然度を診断します（エンタメ診断）。',
  [('忘れ物は？',[('ほぼしない',0),('たまに',2),('しょっちゅう',4)]),
   ('話の流れは？',[('論理的',0),('普通',2),('よく脱線する',4)]),
   ('マイペース度は？',[('低い',0),('普通',2),('高い',4)])],
  [(3,'しっかり者','うっかりが少なく頼れるタイプ。天然度は控えめ。'),
   (8,'ちょい天然','たまに抜けてて愛されるタイプ。ほどよい癒し。'),
   (12,'天然炸裂','マイペースで和ませる天然キャラ。その個性が魅力！')],
  'うっかり度・話の流れ・マイペース度から天然度を判定します。','しっかり者／ちょい天然／天然炸裂に分かれます。',
  [('当たってる？','エンタメ診断です。'),('データは送信される？','いいえ、ブラウザ内で完結します。')],
  ['性格傾向の一般論'], '天然度診断、私は')

dq('yandere-shindan', LOVE, '🔪', 'ヤンデレ診断｜あなたのヤンデレ度は？｜シミュラボ',
  '恋愛での独占欲や束縛傾向の質問から、ヤンデレ度を診断する無料エンタメ診断。',
  'ヤンデレ診断｜あなたのヤンデレ度は？','質問に答えてヤンデレ度を診断。',
  'ヤンデレ診断','恋愛での独占欲や心配性度から、ヤンデレ度を診断します（エンタメ診断）。',
  [('恋人のスマホは？',[('全く気にしない',0),('少し気になる',2),('すごく気になる',4)]),
   ('連絡頻度は？',[('少なめでOK',0),('普通',2),('多めがいい',4)]),
   ('異性の友達は？',[('平気',0),('少しモヤる',2),('心配で仕方ない',4)])],
  [(3,'さっぱり安心型','相手を信頼できる健全タイプ。束縛とは無縁。'),
   (8,'ちょい心配性','たまに不安になるかわいいヤキモチタイプ。'),
   (12,'ヤンデレ注意報','愛が深いぶん独占欲も強め。信頼ベースの関係づくりを。')],
  '独占欲・連絡頻度・心配性度からヤンデレ度を判定します。','安心型／ちょい心配性／ヤンデレ型に分かれます。',
  [('当たってる？','エンタメ診断です。実際の関係は信頼と尊重を大切に。'),('データは送信される？','いいえ、ブラウザ内で完結します。')],
  ['恋愛の独占欲に関する一般論'], 'ヤンデレ診断、私は')

dq('doubutsu-kao', MENTAL, '🐾', '動物顔タイプ診断｜あなたは何顔？（質問版）｜シミュラボ',
  '雰囲気や印象の質問から、あなたを動物にたとえると何タイプかを診断する無料エンタメ診断（カメラ不要）。',
  '動物顔タイプ診断｜あなたは何顔？','質問に答えて動物顔タイプを診断（カメラ不要）。',
  '動物顔タイプ診断','雰囲気や印象の質問から、あなたを動物にたとえると何タイプかを診断します（カメラ不要・エンタメ診断）。',
  [('まわりからの印象は？',[('優しい・癒し',0),('かわいい・元気',2),('クール・大人',4)]),
   ('目もとの印象は？',[('たれ目・丸い',0),('ぱっちり',2),('切れ長',4)]),
   ('雰囲気は？',[('おっとり',0),('明るい',2),('落ち着き',4)])],
  [(3,'いぬ・うさぎ顔','親しみやすく優しい癒し系。安心感で好かれるタイプ。'),
   (8,'ねこ・りす顔','愛嬌があってかわいい元気系。ギャップ萌えも。'),
   (12,'きつね・狼顔','クールで大人っぽい雰囲気。ミステリアスな魅力。')],
  '印象・目もと・雰囲気から動物顔タイプを判定します（カメラ不要）。','いぬ/うさぎ顔／ねこ/りす顔／きつね顔に分かれます。',
  [('カメラは必要？','不要です。質問の回答だけで診断します。'),('データは送信される？','いいえ、ブラウザ内で完結します。')],
  ['顔タイプの印象論'], '動物顔タイプ診断、私は')

dq('kokkaku-shindan', BEAUTY, '👗', '骨格診断｜あなたはストレート/ウェーブ/ナチュラル？｜シミュラボ',
  '体の質感や特徴の質問から、骨格タイプ（ストレート・ウェーブ・ナチュラル）の傾向を診断する無料セルフ診断。',
  '骨格診断｜あなたの骨格タイプは？','質問に答えて骨格タイプの傾向を診断。',
  '骨格診断','体の質感や特徴から、骨格タイプ（似合う服の傾向）をセルフ診断します（簡易版）。',
  [('体の質感は？',[('ハリ・筋肉感',0),('やわらかい',4),('骨・関節しっかり',2)]),
   ('太るとどこから？',[('上半身・お腹',0),('下半身',4),('全体・脂肪つきにくい',2)]),
   ('手首・鎖骨は？',[('厚みがある',0),('華奢',4),('骨が目立つ',2)]),
   ('似合うと言われる服は？',[('シンプル・きれいめ',0),('やわらか・フリル',4),('ラフ・カジュアル',2)])],
  [(5,'ストレートタイプ','上半身に厚み・ハリがあるタイプ。シンプルできれいめが得意。'),
   (11,'ナチュラルタイプ','骨格がしっかりめ。ラフでこなれたスタイルが似合う。'),
   (16,'ウェーブタイプ','やわらかく華奢なタイプ。フリルや曲線的な服が得意。')],
  '質感・太り方・手首鎖骨・似合う服から骨格タイプを判定します。','ストレート／ナチュラル／ウェーブに分かれます。',
  [('正確に知りたい','プロ診断が確実です。本ツールは簡易セルフ診断です。'),('データは送信される？','いいえ、ブラウザ内で完結します。')],
  ['骨格スタイル分析(3タイプ)'], '骨格診断、私は')

dq('rolemodel-shindan', WORK, '🧭', 'ロールモデル診断｜あなたの働き方タイプは？｜シミュラボ',
  '仕事の価値観の質問から、あなたに合う働き方・キャリアタイプを診断する無料エンタメ診断。',
  'ロールモデル診断｜働き方タイプは？','質問に答えて働き方・キャリアタイプを診断。',
  'ロールモデル診断','仕事で大事にしたいことから、あなたに合う働き方・キャリアタイプを診断します（エンタメ診断）。',
  [('仕事で大事なのは？',[('安定・継続',0),('成長・挑戦',4),('人との関わり',2)]),
   ('働き方の理想は？',[('決まった枠で堅実に',0),('自由・裁量大きく',4),('チームで協力',2)]),
   ('評価されたいのは？',[('正確さ・信頼',0),('成果・実績',4),('貢献・サポート',2)])],
  [(3,'堅実スペシャリスト型','安定と正確さを強みに、信頼を積み上げるタイプ。専門性を磨くと◎。'),
   (8,'協調マネージャー型','人をつなぎチームで成果を出すタイプ。調整・育成が得意。'),
   (12,'挑戦リーダー型','成長と裁量を求めるタイプ。新規・起業・成果型の環境で輝く。')],
  '価値観・理想の働き方・評価軸からキャリアタイプを判定します。','スペシャリスト／マネージャー／リーダー型に分かれます。',
  [('転職の参考になる？','方向性のヒントになります。エンタメ診断です。'),('データは送信される？','いいえ、ブラウザ内で完結します。')],
  ['キャリアアンカー等の一般論'], 'ロールモデル診断、私は')

dq('tsuinrei-shindan', LOVE, '💫', 'ツインレイ診断｜運命の相手のサインは？｜シミュラボ',
  '相手との関係の質問から、ツインレイ（運命の相手）の傾向サインを診断する無料エンタメ診断。',
  'ツインレイ診断｜運命の相手のサイン？','質問に答えてツインレイ傾向を診断。',
  'ツインレイ診断','気になる相手との関係から、「ツインレイ（運命の相手）」と言われるサインの傾向を診断します（スピリチュアル系エンタメ診断）。',
  [('出会った時の感覚は？',[('普通',0),('なんか懐かしい',2),('雷に打たれた感覚',4)]),
   ('一緒にいると？',[('緊張する',0),('落ち着く',2),('自分でいられる',4)]),
   ('価値観は？',[('かなり違う',0),('部分的に合う',2),('不思議と通じ合う',4)])],
  [(3,'これから育つ縁','今はご縁の途中かも。焦らず関係を育てて。'),
   (8,'深いつながりの予感','心地よさと共鳴を感じる相手。大切にしたいご縁。'),
   (12,'ツインレイ級のサイン','強い引き合いと安心感。運命的なつながりの傾向が高め。')],
  '出会いの感覚・一緒にいる感覚・価値観の共鳴からサインを判定します。','育つ縁／深い縁／ツインレイ級に分かれます。',
  [('本当に運命の人？','スピリチュアル系のエンタメ診断です。楽しむ範囲でどうぞ。'),('データは送信される？','いいえ、ブラウザ内で完結します。')],
  ['ツインレイ(スピリチュアル)の一般的言説'], 'ツインレイ診断、私は')

dq('goiryoku-shindan', STUDY, '📖', '語彙力診断｜あなたの語彙力レベルは？｜シミュラボ',
  '言葉づかいや読書習慣の質問から、あなたの語彙力レベルの傾向を診断する無料エンタメ診断。',
  '語彙力診断｜語彙力レベルは？','質問に答えて語彙力レベルを診断。',
  '語彙力診断','言葉づかいや読書習慣から、語彙力レベルの傾向を診断します（エンタメ診断）。',
  [('本や記事を読む頻度は？',[('ほとんど読まない',0),('時々',2),('よく読む',4)]),
   ('「忸怩たる思い」の意味は？',[('わからない',0),('なんとなく',2),('説明できる',4)]),
   ('文章を書くとき語彙に？',[('困りがち',0),('普通',2),('こだわる',4)]),
   ('知らない言葉は？',[('そのまま',0),('時々調べる',2),('すぐ調べる',4)])],
  [(4,'語彙ビギナー','これから伸びるタイプ。1日1語の語彙メモから始めると効果的。'),
   (10,'標準語彙レベル','日常会話・ビジネスに困らないレベル。読書でさらに磨けます。'),
   (16,'語彙マスター','豊かな言葉を使いこなすタイプ。表現力で一目置かれる存在。')],
  '読書習慣・語の理解・言葉へのこだわりから語彙力を判定します。','ビギナー／標準／マスターに分かれます。',
  [('本当の語彙力テスト？','傾向を見るエンタメ診断です。本格テストは検定等で。'),('データは送信される？','いいえ、ブラウザ内で完結します。')],
  ['語彙・読解力の一般論'], '語彙力診断、私は')

if __name__=='__main__':
    write_all(SIMS)
    print(f'seo6 done. {len(SIMS)} sims.')
