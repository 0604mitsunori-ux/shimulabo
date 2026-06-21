# -*- coding: utf-8 -*-
"""シミュラボ：受験・進学カテゴリ 10本（gen_sims11のTPLを再利用）。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq, write_all

J = '受験・進学'
SIMS = []
def add(**k): SIMS.append(k)

add(id='heigan-goukaku', cat=J, emoji='🌸',
  title='併願校 合格確率シミュレーター｜どれか1校に受かる確率は？｜シミュラボ',
  desc='複数の併願校それぞれの合格可能性から、少なくとも1校に合格できる確率を計算する受験生・先生向け無料シミュレーター。',
  ogtitle='併願校 合格確率｜どれか1校に受かる確率は？', ogdesc='各校の合格率から、少なくとも1校合格する確率を計算。',
  h1='併願校 合格確率シミュレーター',
  lead='何校か受ければ、どこかには受かる？各併願校の合格可能性（%）から、少なくとも1校に合格できる確率を計算します。出願校数を決める参考に。',
  inputs='''    <h2>🌸 各校の合格可能性（%）</h2>
    <div class="field"><label>各校の合格率を入力（カンマ区切り・例 30,50,80）</label><input type="text" id="rates" value="30,50,80,90" placeholder="例: 30,50,80"></div>
    <button class="btn btn-primary" id="calcBtn">合格確率を見る</button>''',
  result='''      <div class="label">どれか1校に合格する確率</div>
      <div class="big"><span id="big">0</span><span class="unit">%</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">受験校数</div><div class="v" id="n">—</div></div>
      <div class="stat"><div class="k">全落ちの確率</div><div class="v accent" id="miss">—</div></div>
      <div class="stat"><div class="k">判定</div><div class="v" id="judge">—</div></div></div>''',
  article='''    <h2>併願の考え方</h2>
    <div class="note"><strong>計算式</strong><br>全落ち確率 ＝（1−合格率A）×（1−合格率B）×…<br>どれか合格 ＝ 1 − 全落ち確率</div>
    <p>1校ずつの合格率が低くても、複数受ければ「どこかに受かる」確率は上がります。安全校・実力校・挑戦校をバランスよく組むのが王道。確実に進学先を確保するなら、合格可能性の高い「安全校」を必ず1〜2校入れましょう。</p>
    <h2>よくある質問</h2>'''+faq([('各校の合格率はどう出す？','模試のA〜E判定や過去の合否データを%に置き換えて入力してください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const arr=($('rates').value.match(/\\d+(?:\\.\\d+)?/g)||[]).map(Number).filter(x=>x>=0&&x<=100);
    if(!arr.length){alert('合格率を入力してね');return;}
    let miss=1; arr.forEach(p=>miss*=(1-p/100)); const win=(1-miss)*100;
    let j; if(win>=90)j='かなり安心'; else if(win>=70)j='まずまず'; else j='安全校を追加推奨';
    $('sub').textContent=`${arr.length}校：${arr.join('% / ')}%`;$('n').textContent=arr.length+'校';$('miss').textContent=(miss*100).toFixed(1)+'%';$('judge').textContent=j;
    SHARE=`併願校 合格確率シミュ、${arr.length}校でどれか1校に受かる確率は約${win.toFixed(1)}%でした🌸`;show();anim($('big'),0,win,800,1);}''')

add(id='hitsuyo-hensachi', cat=J, emoji='📈',
  title='必要偏差値シミュレーター｜第一志望まであと偏差値いくつ？｜シミュラボ',
  desc='今の偏差値と志望校の偏差値、受験までの月数から、合格に必要な偏差値の差と、追いつくための1日の勉強時間の目安を計算する無料シミュレーター。',
  ogtitle='必要偏差値シミュレーター｜志望校まであと何？', ogdesc='今と志望校の偏差値差から必要な勉強量を計算。',
  h1='必要偏差値シミュレーター',
  lead='志望校まで偏差値はあといくつ？今の偏差値・志望校の偏差値・受験までの月数から、必要な伸びと、追いつくための1日の勉強時間の目安を出します。',
  inputs='''    <h2>📈 条件を入れる</h2>
    <div class="row"><div class="field"><label>今の偏差値</label><input type="number" id="now" value="52" min="20" max="80" inputmode="numeric"></div>
    <div class="field"><label>志望校の偏差値</label><input type="number" id="goal" value="60" min="20" max="80" inputmode="numeric"></div></div>
    <div class="field"><label>受験まで <span class="hint">（ヶ月）</span></label><input type="number" id="months" value="10" min="1" max="36" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">必要な勉強量を見る</button>''',
  result='''      <div class="label">あと必要な偏差値</div>
      <div class="big"><span id="big">0</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1ヶ月で上げる目安</div><div class="v accent" id="per">—</div></div>
      <div class="stat"><div class="k">1日の勉強時間 目安</div><div class="v" id="hours">—</div></div>
      <div class="stat"><div class="k">難易度</div><div class="v" id="judge">—</div></div></div>''',
  article='''    <h2>偏差値を上げるには</h2>
    <div class="note"><strong>目安</strong><br>偏差値を1上げるのに、継続的な学習が必要。一般に偏差値10アップには相応の時間と正しい方法が要ります。<br>本ツールは「1ヶ月で上げる偏差値」と必要な勉強時間の目安を概算します。</div>
    <p>偏差値は周りとの相対評価なので、上げるほど難しくなります。残り期間が短いほど1日の負荷が増えます。苦手分野の克服と過去問演習で効率よく。無理のない計画を。</p>
    <h2>よくある質問</h2>'''+faq([('本当にこの時間で上がる？','個人差があります。質の高い学習と継続が前提の目安です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const now=+$('now').value||50,goal=+$('goal').value||50,m=Math.max(1,+$('months').value||1);
    const diff=Math.max(0,goal-now), per=diff/m;
    const hours=Math.min(12, 2 + per*2.2); // ざっくり：1ヶ月1上げるごとに+2.2h目安
    let j; if(diff<=3)j='現実的'; else if(diff<=8)j='しっかり努力で可能'; else j='高い目標！戦略重要';
    $('sub').textContent=`偏差値 ${now} → ${goal}・残り${m}ヶ月`;$('per').textContent='+'+per.toFixed(1);$('hours').textContent=hours.toFixed(1)+'時間';$('judge').textContent=j;
    SHARE=`必要偏差値シミュ、志望校まであと偏差値${diff}（1日約${hours.toFixed(1)}時間が目安）でした📈`;show();anim($('big'),0,diff,800,0);}''')

add(id='juken-sougaku', cat=J, emoji='💰',
  title='受験総費用シミュレーター｜受験にトータルいくらかかる？｜シミュラボ',
  desc='受験料・併願校数・滑り止めの入学金・塾や交通費から、受験にかかる総額を試算する保護者向け無料シミュレーター。',
  ogtitle='受験総費用シミュレーター｜トータルいくら？', ogdesc='受験料・入学金・塾代から受験の総額を試算。',
  h1='受験総費用シミュレーター',
  lead='受験は受験料だけじゃない。併願校の受験料、滑り止めの入学金（納めて捨てることも）、直前の塾・交通費まで含めた総額を試算します。家計の準備に。',
  inputs='''    <h2>💰 条件を入れる</h2>
    <div class="row"><div class="field"><label>1校の受験料 <span class="hint">（円）</span></label><input type="number" id="fee" value="35000" min="0" inputmode="numeric"></div>
    <div class="field"><label>受験する校数</label><input type="number" id="n" value="5" min="1" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>滑り止めの入学金 <span class="hint">（円・納める場合）</span></label><input type="number" id="nyugaku" value="250000" min="0" inputmode="numeric"></div>
    <div class="field"><label>直前期の塾・交通費 <span class="hint">（円）</span></label><input type="number" id="other" value="100000" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">総額を見る</button>''',
  result='''      <div class="label">受験の総費用</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">受験料の合計</div><div class="v" id="feev">—</div></div>
      <div class="stat"><div class="k">入学金（捨てる分）</div><div class="v accent" id="nv">—</div></div>
      <div class="stat"><div class="k">その他</div><div class="v" id="ov">—</div></div></div>''',
  article='''    <h2>受験費用の内訳</h2>
    <div class="note"><strong>計算式</strong><br>総額 ＝ 受験料 × 校数 ＋ 滑り止め入学金 ＋ 塾・交通費</div>
    <p>第一志望の合格発表前に、滑り止めの入学金の納付期限が来ることが多く、「捨てる入学金」が発生しがち。遠方受験は宿泊・交通費もかさみます。早めに見積もって準備を。</p>
    <h2>よくある質問</h2>'''+faq([('入学金は戻る？','原則返還されないことが多いです。納付期限と合格発表日の確認を。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const fee=Math.max(0,+$('fee').value||0),n=Math.max(1,+$('n').value||1),ny=Math.max(0,+$('nyugaku').value||0),ot=Math.max(0,+$('other').value||0);
    const feeTotal=fee*n, total=feeTotal+ny+ot;
    $('sub').textContent=`受験料${num(fee)}円×${n}校 ＋ 入学金 ＋ 諸費用`;$('feev').textContent=yen(feeTotal);$('nv').textContent=yen(ny);$('ov').textContent=yen(ot);
    SHARE=`受験総費用シミュ、トータル約${yen(total)}でした💰 受験はお金もかかる…！`;show();anim($('big'),0,total,800);}''')

add(id='juken-jikan', cat=J, emoji='⏰',
  title='受験までの勉強時間シミュレーター｜本番まで何時間勉強できる？｜シミュラボ',
  desc='受験までの月数と1日の勉強時間から、本番までに確保できる総勉強時間と、ライバルとの差を可視化する無料シミュレーター。',
  ogtitle='受験までの勉強時間｜本番まで何時間？', ogdesc='残り月数と1日の勉強時間から総勉強時間を計算。',
  h1='受験までの勉強時間シミュレーター',
  lead='受験本番まで、あと何時間勉強できる？残りの月数と1日の勉強時間から、確保できる総時間を計算。1日1時間の差が、本番までにどれだけ開くかも分かります。',
  inputs='''    <h2>⏰ 条件を入れる</h2>
    <div class="row"><div class="field"><label>受験まで <span class="hint">（ヶ月）</span></label><input type="number" id="months" value="10" min="1" max="36" inputmode="numeric"></div>
    <div class="field"><label>1日の勉強時間 <span class="hint">（時間）</span></label><input type="number" id="hours" value="3" min="0" max="16" step="0.5" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">総勉強時間を見る</button>''',
  result='''      <div class="label">本番までの総勉強時間</div>
      <div class="big"><span id="big">0</span><span class="unit">時間</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1日+1時間で</div><div class="v accent" id="plus">—</div></div>
      <div class="stat"><div class="k">残り日数</div><div class="v" id="days">—</div></div>
      <div class="stat"><div class="k">フル(8h/日)なら</div><div class="v" id="full">—</div></div></div>''',
  article='''    <h2>時間は最大の武器</h2>
    <div class="note"><strong>計算式</strong><br>総勉強時間 ＝ 1日の勉強時間 × 30.4 × 残り月数</div>
    <p>1日1時間の差でも、10ヶ月で約300時間の差に。残り時間は誰にも平等ですが、使い方で差がつきます。スキマ時間の活用や、苦手分野への集中投下で効率を上げましょう。</p>
    <h2>よくある質問</h2>'''+faq([('量より質では？','その通り。総量を把握したうえで、質の高い学習を計画してください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const m=Math.max(1,+$('months').value||1),h=Math.max(0,+$('hours').value||0);
    const total=h*30.4*m, plus=(h+1)*30.4*m, days=Math.round(m*30.4), full=8*30.4*m;
    $('sub').textContent=`1日${h}時間 × ${m}ヶ月`;$('plus').textContent=num(plus)+'時間';$('days').textContent=days+'日';$('full').textContent=num(full)+'時間';
    SHARE=`受験までの勉強時間シミュ、本番まで約${num(total)}時間 勉強できる計算でした⏰ 1日+1時間で${num(plus-total)}時間の差！`;show();anim($('big'),0,total,800);}''')

add(id='chugaku-juken', cat=J, emoji='✏️',
  title='中学受験 費用シミュレーター｜塾代込みで総額いくら？｜シミュラボ',
  desc='中学受験の塾代（通塾年数）・受験料・入学金・初年度納入金から、中学受験にかかる総費用の目安を試算する無料シミュレーター。',
  ogtitle='中学受験 費用シミュレーター｜総額いくら？', ogdesc='塾代・受験料・入学金から中学受験の総費用を試算。',
  h1='中学受験 費用シミュレーター',
  lead='中学受験は塾代がメイン。通塾年数・受験料・私立中の初年度費用から、トータルの目安を試算します。早めに見積もって資金計画を。',
  inputs='''    <h2>✏️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>塾代 <span class="hint">（万円/年）</span></label><input type="number" id="juku" value="100" min="0" inputmode="numeric"></div>
    <div class="field"><label>通塾年数 <span class="hint">（年・小4〜6なら3）</span></label><input type="number" id="years" value="3" min="1" max="6" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>受験料の合計 <span class="hint">（万円・併願含む）</span></label><input type="number" id="fee" value="15" min="0" inputmode="numeric"></div>
    <div class="field"><label>私立中の初年度費用 <span class="hint">（万円・入学金＋年間）</span></label><input type="number" id="nyu" value="120" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">総費用を見る</button>''',
  result='''      <div class="label">中学受験〜入学の総費用</div>
      <div class="big"><span id="big">0</span><span class="unit">万円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">塾代の合計</div><div class="v accent" id="jukuv">—</div></div>
      <div class="stat"><div class="k">受験〜入学</div><div class="v" id="other">—</div></div>
      <div class="stat"><div class="k">月あたり(塾)</div><div class="v" id="mo">—</div></div></div>''',
  article='''    <h2>中学受験のお金</h2>
    <div class="note"><strong>計算式</strong><br>総額 ＝ 塾代 × 通塾年数 ＋ 受験料 ＋ 私立中の初年度費用</div>
    <p>中学受験は塾代が大きく、小4〜6の3年間で200〜300万円かかることも。さらに合格後は私立中の学費が続きます。早期から計画的に準備するのがおすすめです。本ツールは目安です。</p>
    <h2>よくある質問</h2>'''+faq([('塾以外の費用は？','講習費・教材費・模試代も含めて「塾代/年」に入れると正確です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const j=Math.max(0,+$('juku').value||0),y=Math.max(1,+$('years').value||1),f=Math.max(0,+$('fee').value||0),n=Math.max(0,+$('nyu').value||0);
    const jukuT=j*y, total=jukuT+f+n;
    $('sub').textContent=`塾${j}万×${y}年 ＋ 受験${f}万 ＋ 入学${n}万`;$('jukuv').textContent=num(jukuT)+'万円';$('other').textContent=num(f+n)+'万円';$('mo').textContent=num(j/12*10000)+'円';
    SHARE=`中学受験 費用シミュ、塾代込みで総額 約${num(total)}万円でした✏️`;show();anim($('big'),0,total,800);}''')

add(id='moshi-hantei', cat=J, emoji='📝',
  title='模試判定シミュレーター｜点数と偏差値からA〜E判定｜シミュラボ',
  desc='模試の得点・平均点・標準偏差から偏差値を出し、志望校の偏差値と比べてA〜E判定の目安を表示する受験生向け無料シミュレーター。',
  ogtitle='模試判定シミュレーター｜A〜E判定の目安', ogdesc='点数と志望校偏差値から合格判定A〜Eの目安を表示。',
  h1='模試判定シミュレーター',
  lead='模試の点数と志望校の偏差値から、合格判定（A〜E）の目安を出します。自分の位置を把握して、次の学習計画に活かしましょう。',
  inputs='''    <h2>📝 条件を入れる</h2>
    <div class="row"><div class="field"><label>自分の得点</label><input type="number" id="score" value="62" min="0" inputmode="numeric"></div>
    <div class="field"><label>平均点</label><input type="number" id="mean" value="55" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>標準偏差 <span class="hint">（不明なら15）</span></label><input type="number" id="sd" value="15" min="1" inputmode="numeric"></div>
    <div class="field"><label>志望校の偏差値</label><input type="number" id="goal" value="58" min="20" max="80" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">判定を見る</button>''',
  result='''      <div class="label">合格判定の目安</div>
      <div class="big" style="font-size:52px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:18px;">—</div>''',
  article='''    <h2>判定の目安</h2>
    <div class="note"><strong>計算式</strong><br>偏差値 ＝ 50 ＋ 10 ×（得点 − 平均）÷ 標準偏差<br>判定：志望校偏差値との差で A(+3以上)/B(+0)/C(-3)/D(-6)/E に区分</div>
    <p>A判定でも油断は禁物、E判定でも諦める必要はありません。判定はあくまで「今の位置」。本番までの伸びしろを信じて、弱点を埋めていきましょう。</p>
    <h2>よくある質問</h2>'''+faq([('E判定から受かる？','十分あり得ます。判定は現状で、努力で変わります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const s=+$('score').value||0,m=+$('mean').value||0,sd=Math.max(1,+$('sd').value||1),goal=+$('goal').value||50;
    const h=50+10*(s-m)/sd, d=h-goal;
    let r,a; if(d>=3){r='A';a='合格圏内！この調子でケアレスミス対策を。';}else if(d>=0){r='B';a='合格に手が届く位置。得点の安定を狙おう。';}else if(d>=-3){r='C';a='あと一歩。苦手分野を集中的に。';}else if(d>=-6){r='D';a='伸びしろ大。基礎固めから着実に。';}else{r='E';a='今からでも逆転可能。計画的に積み上げよう。';}
    $('big').textContent=r+'判定';$('sub').textContent=`偏差値${h.toFixed(1)}（志望校${goal}）`;$('adv').textContent='📝 '+a;
    SHARE=`模試判定シミュ、偏差値${h.toFixed(1)}で志望校は「${r}判定」でした📝`;show();}''')

add(id='goukaku-saiteiten', cat=J, emoji='🎯',
  title='合格最低点まであと何点シミュレーター｜目標点との差は？｜シミュラボ',
  desc='現在の得点（または得点率）と合格最低点から、合格までに必要な点数と、科目ごとに何点上げればよいかの目安を計算する無料シミュレーター。',
  ogtitle='合格最低点まであと何点｜目標との差は？', ogdesc='今の点数と合格最低点から、あと必要な点数を計算。',
  h1='合格最低点まであと何点シミュレーター',
  lead='合格最低点まで、あと何点？今の得点と合格最低点から、必要な上積みと、科目ごとに何点ずつ上げればいいかの目安を出します。',
  inputs='''    <h2>🎯 条件を入れる</h2>
    <div class="row"><div class="field"><label>今の得点（合計）</label><input type="number" id="now" value="280" min="0" inputmode="numeric"></div>
    <div class="field"><label>合格最低点</label><input type="number" id="min" value="320" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>科目数 <span class="hint">（何教科に振り分ける？）</span></label><input type="number" id="n" value="5" min="1" max="10" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">あと何点か見る</button>''',
  result='''      <div class="label">合格まであと</div>
      <div class="big"><span id="big">0</span><span class="unit">点</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1科目あたり</div><div class="v accent" id="per">—</div></div>
      <div class="stat"><div class="k">達成率</div><div class="v" id="rate">—</div></div>
      <div class="stat"><div class="k">状態</div><div class="v" id="judge">—</div></div></div>''',
  article='''    <h2>目標を分解する</h2>
    <div class="note"><strong>計算式</strong><br>あと必要な点 ＝ 合格最低点 − 今の得点<br>1科目あたり ＝ 必要な点 ÷ 科目数</div>
    <p>「あと40点」は遠く感じても、「5科目で1科目8点ずつ」なら現実的に見えてきます。大きな目標は小さく分解すると、やるべきことが明確に。取りやすい科目から上積みを。</p>
    <h2>よくある質問</h2>'''+faq([('得点率でもいい？','はい。今の得点率と合格最低点の率でも同じ計算ができます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const now=+$('now').value||0,min=+$('min').value||0,n=Math.max(1,+$('n').value||1);
    const need=Math.max(0,min-now), per=need/n, rate=min>0?now/min*100:0;
    let j; if(need<=0)j='合格圏！'; else if(per<=10)j='あと少し'; else j='計画的に積み上げを';
    $('sub').textContent=`今${now}点 → 最低点${min}点`;$('per').textContent='+'+per.toFixed(1)+'点';$('rate').textContent=rate.toFixed(0)+'%';$('judge').textContent=j;
    SHARE=`合格最低点シミュ、合格まであと${need}点（1科目+${per.toFixed(1)}点）でした🎯`;show();anim($('big'),0,need,800);}''')

add(id='nyushi-shindan', cat=J, emoji='🧭',
  title='入試方式 診断｜一般・推薦・総合型、あなたに有利なのは？｜シミュラボ',
  desc='評定・学力・課外活動・自己アピールの傾向から、一般選抜・学校推薦・総合型選抜のどれが向いているかを診断する受験生向け無料ツール。',
  ogtitle='入試方式 診断｜一般・推薦・総合型どれが有利？', ogdesc='あなたの強みから向いている入試方式を診断。',
  h1='入試方式 診断',
  lead='大学受験は「一般・学校推薦・総合型（旧AO）」など方式いろいろ。あなたの強みから、どの方式が有利かを診断します。出願戦略の第一歩に。',
  inputs='''    <h2>🧭 あてはまるものを選ぶ</h2>
    <div class="field"><label>評定平均は？</label><select id="q1"><option value="suisen">高い（4.0以上）</option><option value="mid" selected>普通（3.5前後）</option><option value="ippan">低め</option></select></div>
    <div class="field"><label>学力テストは？</label><select id="q2"><option value="ippan">得意・伸びている</option><option value="mid" selected>普通</option><option value="suisen">苦手</option></select></div>
    <div class="field"><label>部活・課外活動・資格は？</label><select id="q3"><option value="sogo">実績やアピールがある</option><option value="mid" selected>人並み</option><option value="ippan">特になし</option></select></div>
    <div class="field"><label>自己PR・志望理由を語るのは？</label><select id="q4"><option value="sogo">得意</option><option value="mid" selected>普通</option><option value="ippan">苦手</option></select></div>
    <button class="btn btn-primary" id="calcBtn">向いてる方式を見る</button>''',
  result='''      <div class="label">あなたに向いている入試方式</div>
      <div class="big" style="font-size:32px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:18px;">—</div>''',
  article='''    <h2>入試方式の特徴</h2>
    <p><strong>一般選抜</strong>＝学力勝負。逆転も可能。<strong>学校推薦型</strong>＝評定平均が重要、早く決まる。<strong>総合型選抜</strong>＝活動実績・志望理由・面接重視で個性が活きる。複数方式を併用するのも戦略。自分の強みに合った方式を選びましょう。</p>
    <h2>よくある質問</h2>'''+faq([('併用できる？','総合型・推薦で挑戦しつつ一般の準備も、は有効な戦略です。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const c={ippan:0,suisen:0,sogo:0,mid:0};for(const id of ['q1','q2','q3','q4'])c[$(id).value]++;
    let t,d; const top=['ippan','suisen','sogo'].reduce((a,b)=>c[a]>=c[b]?a:b);
    if(top==='suisen'&&c.suisen>0){t='学校推薦型 選抜';d='評定平均が武器。指定校・公募推薦で早めの合格を狙えます。評定をキープしつつ志望理由書の準備を。';}
    else if(top==='sogo'&&c.sogo>0){t='総合型選抜（旧AO）';d='活動実績や自己表現が活きるタイプ。志望理由・探究・面接対策で個性をアピールしましょう。';}
    else{t='一般選抜';d='学力で勝負するタイプ。過去問演習と苦手克服で得点力を上げ、逆転を狙えます。';}
    $('big').textContent=t;$('sub').textContent='4つの傾向から診断';$('adv').textContent='🧭 '+d;
    SHARE=`入試方式 診断、私に向いているのは「${t}」でした🧭`;show();}''')

add(id='yobikou-hiyou', cat=J, emoji='🏫',
  title='予備校 vs 宅浪 費用シミュレーター｜浪人の費用はどれだけ違う？｜シミュラボ',
  desc='予備校に通う場合と宅浪（自宅浪人）の費用を比較し、1年でどれだけ差がつくかを試算する受験生・保護者向け無料シミュレーター。',
  ogtitle='予備校 vs 宅浪 費用｜どれだけ違う？', ogdesc='予備校と宅浪の費用を比較して差額を試算。',
  h1='予備校 vs 宅浪 費用シミュレーター',
  lead='浪人するなら予備校？それとも宅浪（自宅浪人）？それぞれの費用を比べて、1年でどれだけ差がつくかを出します。進路選びの判断材料に。',
  inputs='''    <h2>🏫 条件を入れる</h2>
    <div class="row"><div class="field"><label>予備校の年間費用 <span class="hint">（万円・授業＋講習）</span></label><input type="number" id="yobi" value="100" min="0" inputmode="numeric"></div>
    <div class="field"><label>宅浪の年間費用 <span class="hint">（万円・参考書＋模試）</span></label><input type="number" id="taku" value="15" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">差額を見る</button>''',
  result='''      <div class="label">予備校と宅浪の差額</div>
      <div class="big"><span id="big">0</span><span class="unit">万円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">予備校</div><div class="v" id="yv">—</div></div>
      <div class="stat"><div class="k">宅浪</div><div class="v accent" id="tv">—</div></div>
      <div class="stat"><div class="k">月あたりの差</div><div class="v" id="mo">—</div></div></div>''',
  article='''    <h2>予備校と宅浪</h2>
    <div class="note"><strong>比較の考え方</strong><br>差額 ＝ 予備校の年間費用 − 宅浪の年間費用</div>
    <p>予備校は費用が高い分、カリキュラム・添削・仲間・自習環境が整います。宅浪は安いけれど自己管理が必須。費用だけでなく「合格への近道はどちらか」で選ぶのが大切です。映像授業や単科受講で中間を取る手も。</p>
    <h2>よくある質問</h2>'''+faq([('宅浪は受かる？','自己管理ができれば十分可能。模試で客観的な位置確認を。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const y=Math.max(0,+$('yobi').value||0),t=Math.max(0,+$('taku').value||0);const diff=Math.abs(y-t);
    $('sub').textContent=`予備校${y}万 / 宅浪${t}万`;$('yv').textContent=num(y)+'万円';$('tv').textContent=num(t)+'万円';$('mo').textContent=num(diff/12*10000)+'円';
    SHARE=`予備校 vs 宅浪 費用シミュ、その差は約${num(diff)}万円でした🏫`;show();anim($('big'),0,diff,800);}''')

add(id='shigan-bairitsu', cat=J, emoji='📊',
  title='志願倍率シミュレーター｜倍率から合格できる人数は？｜シミュラボ',
  desc='志願者数と募集定員から志願倍率を計算し、自分の順位だと合格圏内かを確認できる受験生向け無料シミュレーター。',
  ogtitle='志願倍率シミュレーター｜合格できる人数は？', ogdesc='志願者数と定員から倍率と合格ラインの順位を計算。',
  h1='志願倍率シミュレーター',
  lead='志願者数と募集定員から、志願倍率と「上位何番までが合格圏か」を計算します。自分の模試順位と照らして、合格可能性をチェックしましょう。',
  inputs='''    <h2>📊 条件を入れる</h2>
    <div class="row"><div class="field"><label>志願者数 <span class="hint">（人）</span></label><input type="number" id="apply" value="600" min="1" inputmode="numeric"></div>
    <div class="field"><label>募集定員 <span class="hint">（人）</span></label><input type="number" id="teiin" value="200" min="1" inputmode="numeric"></div></div>
    <div class="field"><label>あなたの順位 <span class="hint">（だいたいで・任意）</span></label><input type="number" id="rank" value="180" min="1" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">倍率を見る</button>''',
  result='''      <div class="label">志願倍率</div>
      <div class="big"><span id="big">0</span><span class="unit">倍</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">合格圏（上位）</div><div class="v accent" id="line">—</div></div>
      <div class="stat"><div class="k">あなたの位置</div><div class="v" id="you">—</div></div>
      <div class="stat"><div class="k">合格率(順位から)</div><div class="v" id="rate">—</div></div></div>''',
  article='''    <h2>倍率の見方</h2>
    <div class="note"><strong>計算式</strong><br>志願倍率 ＝ 志願者数 ÷ 募集定員<br>合格圏 ＝ 上位 定員番目まで（目安）</div>
    <p>倍率が高くても、自分が上位にいれば合格圏。逆に低倍率でも油断は禁物。実倍率（受験者数ベース）や補欠合格もあるため、本ツールは目安です。志望校の過去倍率と合わせて確認を。</p>
    <h2>よくある質問</h2>'''+faq([('実質倍率とは？','欠席者を除いた「受験者数÷合格者数」。志願倍率より低くなることが多いです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const a=Math.max(1,+$('apply').value||1),t=Math.max(1,+$('teiin').value||1),r=Math.max(1,+$('rank').value||1);
    const b=a/t, inLine=r<=t;
    $('sub').textContent=`志願${num(a)}人 ÷ 定員${num(t)}人`;$('line').textContent=t+'位まで';$('you').textContent=r+'位（'+(inLine?'圏内✓':'圏外')+'）';$('rate').textContent=(inLine?'合格圏':'あと'+(r-t)+'人')+'';
    SHARE=`志願倍率シミュ、倍率${b.toFixed(1)}倍・あなたの${r}位は${inLine?'合格圏内✓':'圏外（あと'+(r-t)+'人）'}でした📊`;show();anim($('big'),0,b,800,1);}''')

if __name__=='__main__':
    write_all(SIMS)
    print(f'juken done. {len(SIMS)} sims.')
