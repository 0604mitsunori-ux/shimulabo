# -*- coding: utf-8 -*-
"""シミュラボ：全カテゴリ3本ずつ補充 その1（money/life/marketing/love/biz/finance）。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq, write_all

SIMS=[]
def add(**k): SIMS.append(k)

# ===== お金・時間 =====
add(id='point-katsu', cat='お金・時間', emoji='🎯',
  title='ポイ活 還元シミュレーター｜キャッシュレスで年いくら貯まる？｜シミュラボ',
  desc='毎月のキャッシュレス決済額と還元率から、ポイントが年間・10年でいくら貯まるかを計算する無料シミュレーター。',
  ogtitle='ポイ活 還元シミュレーター｜年いくら貯まる？', ogdesc='決済額と還元率から、貯まるポイントを年間で計算。',
  h1='ポイ活 還元シミュレーター',
  lead='支払いをキャッシュレスに集約すると、ポイントがコツコツ貯まります。月の決済額と還元率から、年間・10年で貯まるポイントを出します。',
  inputs='''    <h2>🎯 条件を入れる</h2>
    <div class="row"><div class="field"><label>月のキャッシュレス決済額 <span class="hint">（円）</span></label><input type="number" id="m" value="150000" min="0" inputmode="numeric"></div>
    <div class="field"><label>還元率 <span class="hint">（％）</span></label><input type="number" id="r" value="1" min="0" max="20" step="0.1" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">貯まるポイントを見る</button>''',
  result='''      <div class="label">年間に貯まるポイント</div>
      <div class="big"><span id="big">0</span><span class="unit">pt</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1ヶ月あたり</div><div class="v" id="mo">—</div></div>
      <div class="stat"><div class="k">10年で</div><div class="v accent" id="y10">—</div></div>
      <div class="stat"><div class="k">還元率</div><div class="v" id="rv">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>年間ポイント ＝ 月の決済額 × 還元率 × 12</div>
    <p>固定費（光熱費・スマホ・サブスク）もカード払いにまとめると還元が増えます。還元率の高いカード選び＋まとめ払いがポイ活の基本。1ポイント=1円換算です。</p>
    <h2>よくある質問</h2>'''+faq([('使いすぎ注意？','ポイント目当ての浪費は本末転倒。普段の支払いを置き換えるのが基本です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const m=Math.max(0,+$('m').value||0),r=Math.max(0,+$('r').value||0);const y=m*r/100*12;
    $('sub').textContent=`月${num(m)}円 × ${r}％ × 12`;$('mo').textContent=num(m*r/100)+'pt';$('y10').textContent=num(y*10)+'pt';$('rv').textContent=r+'％';
    SHARE=`ポイ活シミュ、私は年で約${num(y)}pt・10年で${num(y*10)}pt貯まる計算でした🎯\\nちりつもポイント！👇`;show();anim($('big'),0,y,900);}''')

add(id='atm-tesuuryo', cat='お金・時間', emoji='🏧',
  title='ATM手数料 生涯コストシミュレーター｜手数料、一生でいくら払う？｜シミュラボ',
  desc='ATM手数料の1回の金額と月の利用回数から、一生で支払うATM手数料の総額を計算する無料シミュレーター。',
  ogtitle='ATM手数料 生涯コスト｜一生でいくら払う？', ogdesc='ATM手数料の回数から、生涯の手数料総額を計算。',
  h1='ATM手数料 生涯コストシミュレーター',
  lead='たかが数百円、されど一生分。ATM手数料の1回の金額と月の利用回数から、生涯で払う総額を出します。ネット銀行なら多くがゼロにできます。',
  inputs='''    <h2>🏧 条件を入れる</h2>
    <div class="row"><div class="field"><label>1回の手数料 <span class="hint">（円）</span></label><input type="number" id="fee" value="220" min="0" inputmode="numeric"></div>
    <div class="field"><label>月の利用回数 <span class="hint">（回）</span></label><input type="number" id="cnt" value="4" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>これからの年数 <span class="hint">（年）</span></label><input type="number" id="yr" value="50" min="1" max="90" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">生涯コストを見る</button>''',
  result='''      <div class="label">一生で払うATM手数料</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1年で</div><div class="v" id="y1">—</div></div>
      <div class="stat"><div class="k">10年で</div><div class="v accent" id="y10">—</div></div>
      <div class="stat"><div class="k">月あたり</div><div class="v" id="mo">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>生涯コスト ＝ 1回の手数料 × 月の回数 × 12 × 年数</div>
    <p>時間外・コンビニATMの手数料は積もると大きな額に。手数料無料の回数があるネット銀行や、給与口座からの計画的な引き出しでゼロに近づけられます。</p>
    <h2>よくある質問</h2>'''+faq([('無料にできる？','ネット銀行や条件を満たせば月数回無料のところが多いです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const fee=Math.max(0,+$('fee').value||0),cnt=Math.max(0,+$('cnt').value||0),yr=Math.max(1,+$('yr').value||1);const y1=fee*cnt*12,total=y1*yr;
    $('sub').textContent=`${num(fee)}円 × 月${cnt}回 × ${yr}年`;$('y1').textContent=yen(y1);$('y10').textContent=yen(y1*10);$('mo').textContent=yen(fee*cnt);
    SHARE=`ATM手数料の生涯コストシミュ、一生で約${yen(total)}も払う計算でした🏧\\nネット銀行で無料にしよ…！👇`;show();anim($('big'),0,total,900);}''')

add(id='tsumitate-fukuri', cat='お金・時間', emoji='📈',
  title='つみたて複利シミュレーター｜毎月の積立、◯年後いくら？｜シミュラボ',
  desc='毎月の積立額・想定利回り・積立年数から、複利で増えた将来の資産額と運用益を計算する無料シミュレーター。',
  ogtitle='つみたて複利シミュレーター｜◯年後いくら？', ogdesc='毎月の積立と利回りから、複利の将来額を計算。',
  h1='つみたて複利シミュレーター',
  lead='毎月コツコツ積み立てると、複利の力で雪だるま式に増えます。積立額・利回り・年数から、将来の資産額と運用益を出します。',
  inputs='''    <h2>📈 条件を入れる</h2>
    <div class="row"><div class="field"><label>毎月の積立 <span class="hint">（円）</span></label><input type="number" id="pmt" value="30000" min="0" inputmode="numeric"></div>
    <div class="field"><label>想定利回り <span class="hint">（％/年）</span></label><input type="number" id="r" value="5" min="0" max="20" step="0.1" inputmode="decimal"></div></div>
    <div class="field"><label>積立年数 <span class="hint">（年）</span></label><input type="number" id="yr" value="20" min="1" max="60" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">将来の資産を見る</button>''',
  result='''      <div class="label" id="lab">◯年後の資産</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">積み立てた元本</div><div class="v" id="moto">—</div></div>
      <div class="stat"><div class="k">運用益</div><div class="v accent" id="eki">—</div></div>
      <div class="stat"><div class="k">利回り</div><div class="v" id="rv">—</div></div></div>''',
  article='''    <h2>複利の力</h2>
    <div class="note"><strong>計算式</strong><br>将来額 ＝ 毎月積立 ×（(1+月利)^月数 − 1）÷ 月利<br>（月利 ＝ 年利 ÷ 12）</div>
    <p>利益が利益を生むのが複利。同じ積立でも、期間が長いほど運用益の割合が大きくなります。新NISAなどの非課税制度と組み合わせると効果的。※投資は元本保証ではありません。</p>
    <h2>よくある質問</h2>'''+faq([('必ず増える？','いいえ。利回りは想定値で、相場により変動・元本割れもあり得ます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const pmt=Math.max(0,+$('pmt').value||0),r=Math.max(0,+$('r').value||0)/100,yr=Math.max(1,+$('yr').value||1);const n=yr*12,mr=r/12;
    const fv=mr>0?pmt*((Math.pow(1+mr,n)-1)/mr):pmt*n;const moto=pmt*n;
    $('lab').textContent=`${yr}年後の資産`;$('sub').textContent=`月${num(pmt)}円・利回り${(r*100).toFixed(1)}％・${yr}年`;
    $('moto').textContent=yen(moto);$('eki').textContent=yen(fv-moto);$('rv').textContent=(r*100).toFixed(1)+'％';
    SHARE=`つみたて複利シミュ、月${num(pmt)}円を${yr}年で約${yen(fv)}に（運用益${yen(fv-moto)}）📈\\n複利すごい…！👇`;show();anim($('big'),0,fv,900);}''')

# ===== 人生・自分ごと =====
add(id='jinsei-calendar', cat='人生・自分ごと', emoji='📅',
  title='人生カレンダーシミュレーター｜あなたの人生、今何％？｜シミュラボ',
  desc='年齢と想定寿命から、人生をどれだけ過ごしたか（％）と、残りの日数・週末の回数を可視化するエンタメシミュレーター。',
  ogtitle='人生カレンダー｜あなたの人生、今何％？', ogdesc='年齢と寿命から、人生の消化率と残り日数を可視化。',
  h1='人生カレンダーシミュレーター',
  lead='人生を時間で見ると、見え方が変わります。年齢と想定寿命から、今どれだけ過ごしたか・残りどれくらいかを出します。今日を大切にするきっかけに。',
  inputs='''    <h2>📅 条件を入れる</h2>
    <div class="row"><div class="field"><label>今の年齢 <span class="hint">（歳）</span></label><input type="number" id="age" value="30" min="0" max="120" inputmode="numeric"></div>
    <div class="field"><label>想定寿命 <span class="hint">（歳）</span></label><input type="number" id="life" value="85" min="1" max="120" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">人生の進み具合を見る</button>''',
  result='''      <div class="label">人生の進み具合</div>
      <div class="big"><span id="big">0</span><span class="unit">％</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">残りの日数</div><div class="v accent" id="days">—</div></div>
      <div class="stat"><div class="k">残りの週末</div><div class="v" id="week">—</div></div>
      <div class="stat"><div class="k">残りの年数</div><div class="v" id="yr">—</div></div></div>''',
  article='''    <h2>時間は有限</h2>
    <div class="note"><strong>計算式</strong><br>進み具合 ＝ 年齢 ÷ 寿命 ×100／残り週末 ＝（寿命−年齢）× 52</div>
    <p>数字にすると、残りの時間は意外と限られていると気づきます。だからこそ「やりたいこと」を先延ばしにしない。今日という1日を大切に過ごしたくなる、そんなシミュレーターです。</p>
    <h2>よくある質問</h2>'''+faq([('縁起でもない？','時間の有限さを知ると、毎日が愛おしくなります。前向きに使ってください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const age=Math.max(0,+$('age').value||0),life=Math.max(age+0.1,+$('life').value||1);const pct=Math.min(100,age/life*100),rem=life-age;
    $('sub').textContent=`${age}歳 / 想定寿命${life}歳`;$('days').textContent=num(rem*365)+'日';$('week').textContent=num(rem*52)+'回';$('yr').textContent=num(rem)+'年';
    SHARE=`人生カレンダー、私の人生は今${Math.round(pct)}％・残り週末は約${num(rem*52)}回でした📅\\n一日一日を大切に。👇`;show();anim($('big'),0,pct,900);}''')

add(id='seimei-suimin', cat='人生・自分ごと', emoji='🛏️',
  title='一生で寝てる時間シミュレーター｜人生の何年、眠ってる？｜シミュラボ',
  desc='1日の睡眠時間と寿命から、一生で眠って過ごす時間（人生の何年・何％か）を計算するエンタメシミュレーター。',
  ogtitle='一生で寝てる時間｜人生の何年、眠ってる？', ogdesc='1日の睡眠時間から、一生で眠る時間を計算。',
  h1='一生で寝てる時間シミュレーター',
  lead='人生の約3分の1は睡眠、とよく言われます。本当にそうなの？1日の睡眠時間と寿命から、一生で眠って過ごす年数を出します。',
  inputs='''    <h2>🛏️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>1日の睡眠時間 <span class="hint">（時間）</span></label><input type="number" id="h" value="7" min="0" max="16" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>想定寿命 <span class="hint">（歳）</span></label><input type="number" id="life" value="85" min="1" max="120" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">眠る時間を見る</button>''',
  result='''      <div class="label">一生で眠って過ごす時間</div>
      <div class="big"><span id="big">0</span><span class="unit">年分</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">人生に占める割合</div><div class="v accent" id="pct">—</div></div>
      <div class="stat"><div class="k">日数にすると</div><div class="v" id="days">—</div></div>
      <div class="stat"><div class="k">起きている時間</div><div class="v" id="awake">—</div></div></div>''',
  article='''    <h2>睡眠は人生の土台</h2>
    <div class="note"><strong>計算式</strong><br>睡眠の年数 ＝ 1日の睡眠 × 365 × 寿命 ÷ 24時間 ÷ 365</div>
    <p>1日7時間なら人生の約29％が睡眠。「もったいない」ではなく、残りの時間を元気に過ごすための大切な投資です。質の良い睡眠で、起きている時間の充実度も上がります。</p>
    <h2>よくある質問</h2>'''+faq([('減らすべき？','いいえ。睡眠不足は健康にも効率にも悪影響。質を高めるのがおすすめです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const h=Math.max(0,+$('h').value||0),life=Math.max(1,+$('life').value||1);const yrs=h/24*life,pct=h/24*100;
    $('sub').textContent=`1日${h}時間 × ${life}年`;$('pct').textContent=Math.round(pct)+'％';$('days').textContent=num(yrs*365)+'日';$('awake').textContent=num(life-yrs)+'年';
    SHARE=`一生で寝てる時間シミュ、人生の約${Math.round(pct)}％・${num(yrs)}年分も眠ってる計算でした🛏️\\n睡眠は大事な投資。👇`;show();anim($('big'),0,yrs,900);}''')

add(id='sumaho-shogai', cat='人生・自分ごと', emoji='📱',
  title='スマホ生涯時間シミュレーター｜一生でスマホに何年使う？｜シミュラボ',
  desc='1日のスマホ利用時間とこれからの年数から、一生でスマホに費やす時間（何年分・映画何本分か）を可視化するエンタメシミュレーター。',
  ogtitle='スマホ生涯時間｜一生でスマホに何年？', ogdesc='1日のスマホ時間から、生涯のスマホ時間を可視化。',
  h1='スマホ生涯時間シミュレーター',
  lead='1日の何時間か、スマホに溶けていませんか。1日の利用時間とこれからの年数から、一生でスマホに費やす時間を可視化します（使い方を見直すきっかけに）。',
  inputs='''    <h2>📱 条件を入れる</h2>
    <div class="row"><div class="field"><label>1日のスマホ時間 <span class="hint">（時間）</span></label><input type="number" id="h" value="4" min="0" max="20" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>これからの年数 <span class="hint">（年）</span></label><input type="number" id="yr" value="60" min="1" max="90" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">生涯のスマホ時間を見る</button>''',
  result='''      <div class="label">一生でスマホに使う時間</div>
      <div class="big"><span id="big">0</span><span class="unit">年分</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">合計時間</div><div class="v accent" id="hours">—</div></div>
      <div class="stat"><div class="k">日数にすると</div><div class="v" id="days">—</div></div>
      <div class="stat"><div class="k">映画(2時間)で</div><div class="v" id="movie">—</div></div></div>''',
  article='''    <h2>スマホ時間を投資に変える</h2>
    <div class="note"><strong>計算式</strong><br>生涯時間 ＝ 1日の利用時間 × 365 × 年数</div>
    <p>1日4時間でも、60年で10年分。もちろん仕事や学びに使う時間も含みますが、「なんとなく見る時間」を少し減らすだけで、人生の自由時間がぐっと増えます。</p>
    <h2>よくある質問</h2>'''+faq([('全部ムダ？','いいえ。学びや仕事も含みます。「だらだら時間」を意識するのが目的です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const h=Math.max(0,+$('h').value||0),yr=Math.max(1,+$('yr').value||1);const hours=h*365*yr,yrs=hours/24/365;
    $('sub').textContent=`1日${h}時間 × ${yr}年`;$('hours').textContent=num(hours)+'時間';$('days').textContent=num(hours/24)+'日';$('movie').textContent=num(hours/2)+'本';
    SHARE=`スマホ生涯時間シミュ、一生で約${num(yrs)}年分もスマホに使う計算でした📱\\nちょっと減らそ…！👇`;show();anim($('big'),0,yrs,900,1);}''')

# ===== マーケティング =====
add(id='cvr-uriage', cat='マーケティング', emoji='📊',
  title='CVR×売上シミュレーター｜アクセスと成約率から売上は？｜シミュラボ',
  desc='月間アクセス数・コンバージョン率（CVR）・客単価から、月商・年商を試算し、CVRを1％改善したときの増収も分かる無料シミュレーター。',
  ogtitle='CVR×売上シミュレーター｜売上はいくら？', ogdesc='アクセス・CVR・客単価から月商と改善効果を試算。',
  h1='CVR×売上シミュレーター',
  lead='Webの売上は「アクセス×成約率×客単価」で決まります。3つの数字から月商・年商を試算。CVRを1％上げると、いくら増えるかも分かります。',
  inputs='''    <h2>📊 条件を入れる</h2>
    <div class="row"><div class="field"><label>月間アクセス数</label><input type="number" id="acc" value="10000" min="0" inputmode="numeric"></div>
    <div class="field"><label>CVR <span class="hint">（成約率％）</span></label><input type="number" id="cvr" value="2" min="0" max="100" step="0.1" inputmode="decimal"></div></div>
    <div class="field"><label>客単価 <span class="hint">（円）</span></label><input type="number" id="price" value="5000" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">売上を試算する</button>''',
  result='''      <div class="label">月商の試算</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">月のCV数</div><div class="v" id="cv">—</div></div>
      <div class="stat"><div class="k">年商</div><div class="v" id="year">—</div></div>
      <div class="stat"><div class="k">CVR+1%で増収(年)</div><div class="v accent" id="up">—</div></div></div>''',
  article='''    <h2>売上の方程式</h2>
    <div class="note"><strong>計算式</strong><br>月商 ＝ アクセス × CVR × 客単価<br>CVRを上げる・客単価を上げる・アクセスを増やす、の3つが売上アップの柱です。</div>
    <p>同じアクセスでもCVRが1％違うと売上は大きく変わります。LP改善・かご落ち対策・追客は、広告費を増やさずに売上を伸ばす効率的な打ち手です。</p>
    <h2>よくある質問</h2>'''+faq([('CVRの目安は？','業種で大きく異なります（EC1〜3％、BtoBリードはさらに低め等）。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const acc=Math.max(0,+$('acc').value||0),cvr=Math.max(0,+$('cvr').value||0)/100,price=Math.max(0,+$('price').value||0);
    const cv=acc*cvr,month=cv*price,up=acc*0.01*price*12;
    $('sub').textContent=`${num(acc)}アクセス × ${(cvr*100).toFixed(1)}％ × ${num(price)}円`;
    $('cv').textContent=num(cv)+'件';$('year').textContent=yen(month*12);$('up').textContent=yen(up);
    SHARE=`CVR×売上シミュ、月商${yen(month)}・年商${yen(month*12)}でした📊\\nCVR+1%で年${yen(up)}増。改善大事…！👇`;show();anim($('big'),0,month,900);}''')

add(id='follower-kachi', cat='マーケティング', emoji='⭐',
  title='フォロワーの資産価値シミュレーター｜あなたのSNS、いくらの価値？｜シミュラボ',
  desc='フォロワー数とPR案件の想定単価・月の本数から、SNSアカウントが生む月収・年収の目安を試算するエンタメシミュレーター。',
  ogtitle='フォロワーの資産価値｜SNSはいくらの価値？', ogdesc='フォロワー数とPR単価から、SNSの収益価値を試算。',
  h1='フォロワーの資産価値シミュレーター',
  lead='育てたフォロワーは立派な資産。フォロワー数とPR案件の単価から、あなたのSNSが生む収益の目安を試算します（皮算用として楽しんでください）。',
  inputs='''    <h2>⭐ 条件を入れる</h2>
    <div class="row"><div class="field"><label>フォロワー数</label><input type="number" id="fol" value="10000" min="0" inputmode="numeric"></div>
    <div class="field"><label>1フォロワーあたり単価 <span class="hint">（円・目安2〜4円）</span></label><input type="number" id="cpf" value="2.5" min="0" step="0.1" inputmode="decimal"></div></div>
    <div class="field"><label>月のPR本数 <span class="hint">（本）</span></label><input type="number" id="n" value="2" min="0" max="30" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">資産価値を見る</button>''',
  result='''      <div class="label">PR1本あたりの想定額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">月の想定収入</div><div class="v accent" id="mo">—</div></div>
      <div class="stat"><div class="k">年の想定収入</div><div class="v" id="year">—</div></div>
      <div class="stat"><div class="k">フォロワー単価</div><div class="v" id="cpfv">—</div></div></div>''',
  article='''    <h2>フォロワー単価とは</h2>
    <div class="note"><strong>計算式</strong><br>PR1本 ＝ フォロワー数 × 1フォロワーあたり単価<br>月収 ＝ PR1本 × 月の本数</div>
    <p>PR案件の相場は「フォロワー数×2〜4円」が一つの目安（ジャンル・エンゲージ率で変動）。数より「濃いファン」がいるアカウントほど単価は上がります。フォロワーは育てるほど資産になります。</p>
    <h2>よくある質問</h2>'''+faq([('本当にこの額もらえる？','あくまで目安です。実際はジャンル・実績・交渉で変わります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const fol=Math.max(0,+$('fol').value||0),cpf=Math.max(0,+$('cpf').value||0),n=Math.max(0,+$('n').value||0);
    const per=fol*cpf,mo=per*n;
    $('sub').textContent=`${num(fol)}人 × ${cpf}円 × 月${n}本`;$('mo').textContent=yen(mo);$('year').textContent=yen(mo*12);$('cpfv').textContent=cpf+'円';
    SHARE=`フォロワー資産価値シミュ、私のSNSはPR1本${yen(per)}・月${yen(mo)}の価値でした⭐\\nフォロワーは資産！👇`;show();anim($('big'),0,per,900);}''')

add(id='email-cv', cat='マーケティング', emoji='✉️',
  title='メルマガ効果シミュレーター｜1通でいくら売れる？｜シミュラボ',
  desc='配信数・開封率・クリック率・成約率・客単価から、メルマガ1通あたりの売上を試算する無料シミュレーター。',
  ogtitle='メルマガ効果シミュレーター｜1通でいくら売れる？', ogdesc='配信数と開封・クリック・成約率から、メルマガ売上を試算。',
  h1='メルマガ効果シミュレーター',
  lead='メルマガ1通で、どれくらい売れる？配信数から開封・クリック・成約とファネルをたどって、1通あたりの売上を試算します。改善ポイントも見えてきます。',
  inputs='''    <h2>✉️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>配信数</label><input type="number" id="send" value="10000" min="0" inputmode="numeric"></div>
    <div class="field"><label>開封率 <span class="hint">（％）</span></label><input type="number" id="open" value="20" min="0" max="100" step="0.1" inputmode="decimal"></div></div>
    <div class="row"><div class="field"><label>クリック率 <span class="hint">（開封者の％）</span></label><input type="number" id="click" value="10" min="0" max="100" step="0.1" inputmode="decimal"></div>
    <div class="field"><label>成約率 <span class="hint">（クリック者の％）</span></label><input type="number" id="cv" value="5" min="0" max="100" step="0.1" inputmode="decimal"></div></div>
    <div class="field"><label>客単価 <span class="hint">（円）</span></label><input type="number" id="price" value="5000" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">1通の売上を試算する</button>''',
  result='''      <div class="label">メルマガ1通の売上</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">開封</div><div class="v" id="o">—</div></div>
      <div class="stat"><div class="k">クリック</div><div class="v" id="c">—</div></div>
      <div class="stat"><div class="k">成約数</div><div class="v accent" id="v">—</div></div></div>''',
  article='''    <h2>メールのファネル</h2>
    <div class="note"><strong>計算式</strong><br>成約数 ＝ 配信 × 開封率 × クリック率 × 成約率<br>売上 ＝ 成約数 × 客単価</div>
    <p>件名で開封率、本文とリンクでクリック率、LPで成約率が決まります。どこがボトルネックかを把握して、一段ずつ改善すると売上はぐっと伸びます。リストは育てるほど資産に。</p>
    <h2>よくある質問</h2>'''+faq([('開封率の目安は？','一般に15〜25％程度。件名と配信タイミングで大きく変わります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const send=Math.max(0,+$('send').value||0),o=+$('open').value/100,c=+$('click').value/100,v=+$('cv').value/100,price=Math.max(0,+$('price').value||0);
    const opens=send*o,clicks=opens*c,cvs=clicks*v,sales=cvs*price;
    $('sub').textContent=`配信${num(send)}・開封${$('open').value}％・CL${$('click').value}％・CV${$('cv').value}％`;
    $('o').textContent=num(opens)+'件';$('c').textContent=num(clicks)+'件';$('v').textContent=num(cvs)+'件';
    SHARE=`メルマガ効果シミュ、1通で約${yen(sales)}の売上（成約${num(cvs)}件）でした✉️\\nリストは資産だ…！👇`;show();anim($('big'),0,sales,900);}''')

# ===== 恋愛・婚活 =====
add(id='deto-yosan', cat='恋愛・婚活', emoji='💐',
  title='デート費用 年間シミュレーター｜恋人とのデート、年いくら？｜シミュラボ',
  desc='1回のデート費用と月の回数から、デートにかかる年間・記念日までの費用を計算する無料シミュレーター。',
  ogtitle='デート費用 年間シミュレーター｜年いくら？', ogdesc='1回のデート費用と回数から、年間のデート代を計算。',
  h1='デート費用 年間シミュレーター',
  lead='楽しいデートも、積み重ねると結構な額に。1回の費用と月の回数から、年間・3年でのデート費用を出します（節約の参考にも、思い出の価値の確認にも）。',
  inputs='''    <h2>💐 条件を入れる</h2>
    <div class="row"><div class="field"><label>1回のデート費用 <span class="hint">（円・2人分）</span></label><input type="number" id="cost" value="8000" min="0" inputmode="numeric"></div>
    <div class="field"><label>月のデート回数 <span class="hint">（回）</span></label><input type="number" id="freq" value="4" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">年間のデート費用を見る</button>''',
  result='''      <div class="label">年間のデート費用</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1ヶ月あたり</div><div class="v" id="mo">—</div></div>
      <div class="stat"><div class="k">3年で</div><div class="v accent" id="y3">—</div></div>
      <div class="stat"><div class="k">年の回数</div><div class="v" id="cnt">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>年間 ＝ 1回の費用 × 月の回数 × 12</div>
    <p>お金をかけずに楽しめるデートもたくさん。費用を把握して、たまには贅沢、普段はおうちデート、とメリハリをつけると無理なく続きます。割り勘ルールを話し合っておくのも◎。</p>
    <h2>よくある質問</h2>'''+faq([('割り勘前提？','「2人分の合計」で入れてください。分担は二人で相談を。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const cost=Math.max(0,+$('cost').value||0),freq=Math.max(0,+$('freq').value||0);const year=cost*freq*12;
    $('sub').textContent=`1回${num(cost)}円 × 月${freq}回`;$('mo').textContent=yen(cost*freq);$('y3').textContent=yen(year*3);$('cnt').textContent=num(freq*12)+'回';
    SHARE=`デート費用 年間シミュ、年で約${yen(year)}でした💐\\n思い出はプライスレス…！👇`;show();anim($('big'),0,year,900);}''')

add(id='kekkonshiki-hiyou', cat='恋愛・婚活', emoji='💒',
  title='結婚式 費用シミュレーター｜自己負担はいくら？｜シミュラボ',
  desc='招待ゲスト数と1人あたりの費用・ご祝儀から、結婚式の総額と「ご祝儀を引いた自己負担額」を試算する無料シミュレーター。',
  ogtitle='結婚式 費用シミュレーター｜自己負担はいくら？', ogdesc='ゲスト数から結婚式の総額と自己負担額を試算。',
  h1='結婚式 費用シミュレーター',
  lead='結婚式って、結局いくら自己負担するの？ゲスト数と1人あたりの費用・ご祝儀から、総額と自己負担額（手出し）を試算します。',
  inputs='''    <h2>💒 条件を入れる</h2>
    <div class="field"><label>招待ゲスト数 <span class="hint">（人）</span></label><input type="number" id="g" value="60" min="0" inputmode="numeric"></div>
    <div class="row"><div class="field"><label>1人あたりの費用 <span class="hint">（円）</span></label><input type="number" id="cost" value="55000" min="0" inputmode="numeric"></div>
    <div class="field"><label>1人あたりのご祝儀 <span class="hint">（円）</span></label><input type="number" id="goshugi" value="32000" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">自己負担を見る</button>''',
  result='''      <div class="label">自己負担額（手出し）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">総額</div><div class="v" id="total">—</div></div>
      <div class="stat"><div class="k">ご祝儀の合計</div><div class="v accent" id="go">—</div></div>
      <div class="stat"><div class="k">ゲスト数</div><div class="v" id="gv">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>総額 ＝ ゲスト数 × 1人あたりの費用<br>自己負担 ＝ 総額 − ゲスト数 × ご祝儀</div>
    <p>結婚式は総額だけ見ると驚きますが、ご祝儀で多くがまかなわれます。実際の手出しは総額より大幅に少なくなることも。会場・人数・演出で大きく変わるので、優先順位を決めて。</p>
    <h2>よくある質問</h2>'''+faq([('ご祝儀の相場は？','友人3万円、上司・親族はそれ以上が一般的な目安です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const g=Math.max(0,+$('g').value||0),cost=Math.max(0,+$('cost').value||0),go=Math.max(0,+$('goshugi').value||0);
    const total=g*cost,goukei=g*go,jiko=Math.max(0,total-goukei);
    $('sub').textContent=`${g}人 × 1人${num(cost)}円`;$('total').textContent=yen(total);$('go').textContent=yen(goukei);$('gv').textContent=g+'人';
    SHARE=`結婚式 費用シミュ、総額${yen(total)}・ご祝儀差引の自己負担は約${yen(jiko)}でした💒\\n意外と手出しは抑えられる？👇`;show();anim($('big'),0,jiko,900);}''')

add(id='birthday-aishou', cat='恋愛・婚活', emoji='🎂',
  title='誕生日で相性占い｜ふたりの誕生日、相性は何％？｜シミュラボ',
  desc='自分と相手の誕生日から、運命数の組み合わせで相性を占うエンタメ相性診断シミュレーター。',
  ogtitle='誕生日で相性占い｜ふたりの相性は何％？', ogdesc='ふたりの誕生日から、相性とアドバイスを占う。',
  h1='誕生日で相性占い',
  lead='ふたりの誕生日から相性を占います。気になるあの人、恋人、友達と試してみて。盛り上がる定番のエンタメ占いです（数字で人を値踏みするものではありません）。',
  inputs='''    <h2>🎂 ふたりの誕生日を入れる</h2>
    <div class="field"><label>あなたの誕生日</label><input type="date" id="d1" value="1996-05-12"></div>
    <div class="field"><label>相手の誕生日</label><input type="date" id="d2" value="1995-09-23"></div>
    <button class="btn btn-primary" id="calcBtn">相性を占う</button>''',
  result='''      <div class="label">ふたりの相性は</div>
      <div class="big"><span id="big">0</span><span class="unit">％</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:18px;">—</div>''',
  article='''    <h2>この占いについて</h2>
    <p>ふたりの誕生日を数秘術ふうに組み合わせて相性を導くエンタメ占いです。同じ組み合わせなら結果は変わりません。相性が何％でも、思いやりがあれば良い関係は築けます。会話のきっかけにどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([('当たる？','エンタメ占いです。楽しむためのものとしてお使いください。'),('入力した誕生日は送信されますか？','いいえ。占いはすべてブラウザ内で完結します。')]),
  js='''  function calc(){const d1=$('d1').value,d2=$('d2').value;if(!d1||!d2){alert('ふたりの誕生日を入れてね');return;}
    const h=hash(d1+'|'+d2),sc=55+h%46;
    let a;if(sc>=85)a='息ぴったりのベストカップル。自然体でいられる関係です✨';else if(sc>=70)a='good な相性。お互いを尊重すれば長続きします。';else a='違いはあるけど学び合える二人。歩み寄りがカギ。';
    $('sub').textContent=`あなた(${d1}) × 相手(${d2})`;$('adv').textContent='🎂 '+a;
    SHARE=`誕生日で相性占い、ふたりの相性は${sc}％でした🎂\\n${sc>=70?'いい感じ…！':'違いを楽しむ二人。'}あなたは？👇`;show();anim($('big'),0,sc,900);}''')

# ===== 店舗・ビジネス =====
add(id='genka-rieki', cat='店舗・ビジネス', emoji='🧮',
  title='原価率→粗利シミュレーター｜その商売、粗利はいくら残る？｜シミュラボ',
  desc='売上と原価率から、粗利益と粗利率、年間の粗利を計算する無料の店舗経営シミュレーター。',
  ogtitle='原価率→粗利シミュレーター｜粗利はいくら？', ogdesc='売上と原価率から、粗利益・粗利率・年間粗利を計算。',
  h1='原価率→粗利シミュレーター',
  lead='売上が同じでも、原価率で手元に残る利益は大違い。月の売上と原価率から、粗利益・粗利率・年間粗利を出します。値づけや仕入れ見直しの参考に。',
  inputs='''    <h2>🧮 条件を入れる</h2>
    <div class="row"><div class="field"><label>月の売上 <span class="hint">（円）</span></label><input type="number" id="uri" value="1000000" min="0" inputmode="numeric"></div>
    <div class="field"><label>原価率 <span class="hint">（％）</span></label><input type="number" id="genka" value="30" min="0" max="100" step="0.1" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">粗利を見る</button>''',
  result='''      <div class="label">月の粗利益</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">粗利率</div><div class="v" id="ritsu">—</div></div>
      <div class="stat"><div class="k">原価(月)</div><div class="v" id="g">—</div></div>
      <div class="stat"><div class="k">年間の粗利</div><div class="v accent" id="year">—</div></div></div>''',
  article='''    <h2>原価率と粗利</h2>
    <div class="note"><strong>計算式</strong><br>粗利益 ＝ 売上 ×（1 − 原価率）<br>粗利率 ＝ 100％ − 原価率</div>
    <p>飲食は原価率30％前後が一つの目安。粗利からさらに人件費・家賃などを引いて最終利益になります。原価率を数％下げる・客単価を上げる工夫が、利益に直結します。</p>
    <h2>よくある質問</h2>'''+faq([('粗利と利益の違いは？','粗利は売上−原価。ここから経費を引いたのが営業利益です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const uri=Math.max(0,+$('uri').value||0),g=Math.max(0,Math.min(100,+$('genka').value||0))/100;const rieki=uri*(1-g);
    $('sub').textContent=`売上${num(uri)}円・原価率${(g*100).toFixed(0)}％`;$('ritsu').textContent=((1-g)*100).toFixed(0)+'％';$('g').textContent=yen(uri*g);$('year').textContent=yen(rieki*12);
    SHARE=`原価率→粗利シミュ、月商${yen(uri)}・原価率${(g*100).toFixed(0)}％で粗利は月${yen(rieki)}でした🧮\\n原価管理が利益のカギ。👇`;show();anim($('big'),0,rieki,900);}''')

add(id='kyakutanka-up', cat='店舗・ビジネス', emoji='⬆️',
  title='客単価アップ効果シミュレーター｜あと◯円で年商はどう変わる？｜シミュラボ',
  desc='現在の客単価と客数、値上げ額から、客単価を上げたときの年間の増収額を試算する無料の店舗経営シミュレーター。',
  ogtitle='客単価アップ効果｜あと◯円で年商はどう変わる？', ogdesc='客単価を上げると年商がどれだけ増えるかを試算。',
  h1='客単価アップ効果シミュレーター',
  lead='新規集客より手堅いのが客単価アップ。「あと一品」「セット提案」で単価を少し上げると、年商はどれだけ増える？を試算します。',
  inputs='''    <h2>⬆️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>今の客単価 <span class="hint">（円）</span></label><input type="number" id="now" value="3000" min="0" inputmode="numeric"></div>
    <div class="field"><label>月の客数 <span class="hint">（人）</span></label><input type="number" id="kyaku" value="1000" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>上げる単価 <span class="hint">（＋円）</span></label><input type="number" id="up" value="300" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">増収効果を見る</button>''',
  result='''      <div class="label">年間の増収額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1ヶ月あたり</div><div class="v" id="mo">—</div></div>
      <div class="stat"><div class="k">新しい客単価</div><div class="v accent" id="newp">—</div></div>
      <div class="stat"><div class="k">新しい年商</div><div class="v" id="year">—</div></div></div>''',
  article='''    <h2>客単価アップの威力</h2>
    <div class="note"><strong>計算式</strong><br>年間の増収 ＝ 上げる単価 × 月の客数 × 12（客数が変わらない前提）</div>
    <p>たった+300円でも、客数が多ければ年では大きな増収に。セット販売・トッピング・上位プランの提案などで、無理なく単価を上げる工夫が利益を押し上げます。</p>
    <h2>よくある質問</h2>'''+faq([('値上げで客が減らない？','付加価値とセットで提案するのがコツ。価値が伝われば離れにくいです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const now=Math.max(0,+$('now').value||0),k=Math.max(0,+$('kyaku').value||0),up=Math.max(0,+$('up').value||0);
    const moUp=up*k,year=moUp*12,newY=(now+up)*k*12;
    $('sub').textContent=`単価+${num(up)}円 × 月${num(k)}人`;$('mo').textContent=yen(moUp);$('newp').textContent=yen(now+up);$('year').textContent=yen(newY);
    SHARE=`客単価アップ効果シミュ、+${num(up)}円で年商が${yen(year)}も増える計算でした⬆️\\n単価アップは効く！👇`;show();anim($('big'),0,year,900);}''')

add(id='kaiin-monthly', cat='店舗・ビジネス', emoji='🔁',
  title='月額会員ビジネス シミュレーター｜継続率で月商はどう変わる？｜シミュラボ',
  desc='会員数・月会費・継続率から、サブスク／月額会員ビジネスの月商・年商と、会員1人あたりのLTVを試算する無料シミュレーター。',
  ogtitle='月額会員ビジネス｜継続率で月商はどう変わる？', ogdesc='会員数・会費・継続率から月商とLTVを試算。',
  h1='月額会員ビジネス シミュレーター',
  lead='サブスク・月額会員ビジネスの肝は「継続率」。会員数・月会費・継続率から、月商と会員1人あたりの生涯価値（LTV）を試算します。',
  inputs='''    <h2>🔁 条件を入れる</h2>
    <div class="row"><div class="field"><label>会員数 <span class="hint">（人）</span></label><input type="number" id="n" value="200" min="0" inputmode="numeric"></div>
    <div class="field"><label>月会費 <span class="hint">（円）</span></label><input type="number" id="fee" value="5000" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>月の継続率 <span class="hint">（％）</span></label><input type="number" id="keep" value="90" min="1" max="99.9" step="0.1" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">月商とLTVを見る</button>''',
  result='''      <div class="label">月商</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">年商</div><div class="v" id="year">—</div></div>
      <div class="stat"><div class="k">平均継続月数</div><div class="v" id="months">—</div></div>
      <div class="stat"><div class="k">会員1人のLTV</div><div class="v accent" id="ltv">—</div></div></div>''',
  article='''    <h2>継続率が命</h2>
    <div class="note"><strong>計算式</strong><br>月商 ＝ 会員数 × 月会費<br>平均継続月数 ＝ 1 ÷（1 − 継続率）／LTV ＝ 月会費 × 平均継続月数</div>
    <p>継続率が90％か95％かで、LTV（顧客生涯価値）は2倍以上変わります。新規獲得より「やめさせない工夫（解約防止）」のほうが、利益インパクトが大きいことも。</p>
    <h2>よくある質問</h2>'''+faq([('チャーンレートとは？','解約率のこと。継続率＝100％−解約率です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const n=Math.max(0,+$('n').value||0),fee=Math.max(0,+$('fee').value||0),keep=Math.max(0,Math.min(99.9,+$('keep').value||0))/100;
    const mo=n*fee,months=1/(1-keep),ltv=fee*months;
    $('sub').textContent=`会員${num(n)}人・月会費${num(fee)}円・継続${(keep*100).toFixed(1)}％`;$('year').textContent=yen(mo*12);$('months').textContent=months.toFixed(1)+'ヶ月';$('ltv').textContent=yen(ltv);
    SHARE=`月額会員ビジネスシミュ、月商${yen(mo)}・会員1人のLTVは${yen(ltv)}でした🔁\\n継続率がすべて…！👇`;show();anim($('big'),0,mo,900);}''')

# ===== マネー・保険・不動産 =====
add(id='ideco-setsuzei', cat='マネー・保険・不動産', emoji='🛡️',
  title='iDeCo節税シミュレーター｜掛金で税金はいくら減る？｜シミュラボ',
  desc='iDeCoの毎月の掛金と所得に応じた税率から、年間・積立期間トータルの節税額を試算する無料シミュレーター。',
  ogtitle='iDeCo節税シミュレーター｜税金はいくら減る？', ogdesc='iDeCoの掛金と税率から、年間・生涯の節税額を試算。',
  h1='iDeCo節税シミュレーター',
  lead='iDeCoの掛金は全額が所得控除。毎月の掛金と所得帯から、年間とトータルの節税額を試算します（老後資金づくり＋節税の二刀流）。',
  inputs='''    <h2>🛡️ 条件を入れる</h2>
    <div class="field"><label>毎月の掛金 <span class="hint">（円・上限は職業で異なる）</span></label><input type="number" id="pmt" value="23000" min="0" inputmode="numeric"></div>
    <div class="field"><label>所得の目安（税率）</label><select id="rate"><option value="0.15">〜年収300万（約15％）</option><option value="0.20" selected>年収400〜600万（約20％）</option><option value="0.30">年収700〜900万（約30％）</option><option value="0.43">年収1000万超（約43％）</option></select></div>
    <div class="field"><label>積立年数 <span class="hint">（年）</span></label><input type="number" id="yr" value="20" min="1" max="40" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">節税額を見る</button>''',
  result='''      <div class="label">年間の節税額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">積立期間トータル</div><div class="v accent" id="total">—</div></div>
      <div class="stat"><div class="k">掛金の総額</div><div class="v" id="moto">—</div></div>
      <div class="stat"><div class="k">税率</div><div class="v" id="rv">—</div></div></div>''',
  article='''    <h2>iDeCoの節税効果</h2>
    <div class="note"><strong>計算式</strong><br>年間の節税 ＝ 掛金 × 12 ×（所得税＋住民税の税率）</div>
    <p>掛金が全額所得控除になるため、所得が高い人ほど節税効果が大きくなります。さらに運用益も非課税。ただし原則60歳まで引き出せない点に注意。税率は概算です。</p>
    <h2>よくある質問</h2>'''+faq([('受取時に税金は？','受取時は退職所得控除や公的年金等控除の対象。トータルで有利になりやすい制度です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const pmt=Math.max(0,+$('pmt').value||0),rate=+$('rate').value||0.2,yr=Math.max(1,+$('yr').value||1);
    const y=pmt*12*rate,total=y*yr,moto=pmt*12*yr;
    $('sub').textContent=`月${num(pmt)}円・税率約${(rate*100).toFixed(0)}％・${yr}年`;$('total').textContent=yen(total);$('moto').textContent=yen(moto);$('rv').textContent=(rate*100).toFixed(0)+'％';
    SHARE=`iDeCo節税シミュ、年${yen(y)}・${yr}年で約${yen(total)}も節税できる計算でした🛡️\\n老後資金＋節税の二刀流！👇`;show();anim($('big'),0,y,900);}''')

add(id='haitou-shisan', cat='マネー・保険・不動産', emoji='💰',
  title='配当生活の必要資産シミュレーター｜月◯万の配当に元手いくら？｜シミュラボ',
  desc='欲しい毎月の配当額と想定利回りから、配当金生活に必要な資産額を逆算する無料シミュレーター。',
  ogtitle='配当生活の必要資産｜月◯万の配当に元手いくら？', ogdesc='欲しい月の配当と利回りから、必要な資産額を逆算。',
  h1='配当生活の必要資産シミュレーター',
  lead='配当金だけで暮らす「配当生活」。月にこれだけ配当が欲しい、から必要な資産額を逆算します。FIREや不労所得づくりの目標設定に。',
  inputs='''    <h2>💰 条件を入れる</h2>
    <div class="row"><div class="field"><label>欲しい月の配当 <span class="hint">（円・税引後）</span></label><input type="number" id="m" value="100000" min="0" inputmode="numeric"></div>
    <div class="field"><label>想定利回り <span class="hint">（％・税引後/年）</span></label><input type="number" id="r" value="4" min="0.1" max="20" step="0.1" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">必要な資産を見る</button>''',
  result='''      <div class="label">必要な資産額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">年間の配当</div><div class="v" id="year">—</div></div>
      <div class="stat"><div class="k">毎月5万積立なら</div><div class="v accent" id="years">—</div></div>
      <div class="stat"><div class="k">利回り</div><div class="v" id="rv">—</div></div></div>''',
  article='''    <h2>配当生活のはなし</h2>
    <div class="note"><strong>計算式</strong><br>必要資産 ＝ 年間の配当 ÷ 利回り<br>（年間の配当 ＝ 欲しい月の配当 × 12）</div>
    <p>利回り4％なら、月10万円の配当に3,000万円が必要。道のりは長いですが、積立＋複利でコツコツ近づけます。※配当は減配・株価変動のリスクがあり、保証されたものではありません。</p>
    <h2>よくある質問</h2>'''+faq([('利回り何％が現実的？','税引後で3〜4％程度が一つの目安。高利回りほどリスクも高まります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const m=Math.max(0,+$('m').value||0),r=Math.max(0.1,+$('r').value||0.1)/100;const year=m*12,need=year/r;
    const yearsTo=need>0?need/(50000*12):0;
    $('sub').textContent=`月${num(m)}円・利回り${(r*100).toFixed(1)}％`;$('year').textContent=yen(year);$('years').textContent=num(yearsTo)+'年';$('rv').textContent=(r*100).toFixed(1)+'％';
    SHARE=`配当生活の必要資産シミュ、月${num(m)}円の配当には約${yen(need)}必要でした💰\\nコツコツ目指そ…！👇`;show();anim($('big'),0,need,900);}''')

add(id='souzoku-zei', cat='マネー・保険・不動産', emoji='📜',
  title='相続税ざっくりシミュレーター｜うちは相続税かかる？｜シミュラボ',
  desc='遺産総額と法定相続人の数から、基礎控除を引いた課税対象額と、おおまかな相続税額の目安を試算する無料シミュレーター。',
  ogtitle='相続税ざっくりシミュレーター｜うちはかかる？', ogdesc='遺産総額と相続人数から、相続税の目安を試算。',
  h1='相続税ざっくりシミュレーター',
  lead='「うちは相続税がかかるの？」をまず把握。遺産総額と法定相続人の数から、基礎控除と課税対象額、おおまかな税額の目安を出します（正確には専門家へ）。',
  inputs='''    <h2>📜 条件を入れる</h2>
    <div class="row"><div class="field"><label>遺産の総額 <span class="hint">（万円）</span></label><input type="number" id="isan" value="5000" min="0" inputmode="numeric"></div>
    <div class="field"><label>法定相続人の数 <span class="hint">（人）</span></label><input type="number" id="n" value="3" min="1" max="20" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">相続税の目安を見る</button>''',
  result='''      <div class="label">相続税の目安（総額）</div>
      <div class="big"><span id="big">0</span><span class="unit">万円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">基礎控除</div><div class="v" id="kiso">—</div></div>
      <div class="stat"><div class="k">課税対象</div><div class="v accent" id="kazei">—</div></div>
      <div class="stat"><div class="k">判定</div><div class="v" id="judge">—</div></div></div>''',
  article='''    <h2>基礎控除を超えなければ非課税</h2>
    <div class="note"><strong>計算式</strong><br>基礎控除 ＝ 3,000万円 ＋ 600万円 × 法定相続人の数<br>遺産がこれを超えなければ、相続税はかかりません。</div>
    <p>多くの家庭は基礎控除内におさまります。超える場合の税額は、各相続人の取得額に応じた累進税率で計算されます（本ツールは超過分への簡易概算）。正確な計算・申告は税理士にご相談を。</p>
    <h2>よくある質問</h2>'''+faq([('正確な額？','いいえ。控除や特例（配偶者控除・小規模宅地等）で大きく変わります。必ず専門家へ。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const isan=Math.max(0,+$('isan').value||0),n=Math.max(1,+$('n').value||1);
    const kiso=3000+600*n,kazei=Math.max(0,isan-kiso);
    // 超過分への簡易概算（実際は各人按分の累進）
    let zei;if(kazei<=1000)zei=kazei*0.1;else if(kazei<=3000)zei=kazei*0.15-50;else if(kazei<=5000)zei=kazei*0.2-200;else if(kazei<=10000)zei=kazei*0.3-700;else zei=kazei*0.4-1700;
    zei=Math.max(0,zei);
    $('sub').textContent=`遺産${num(isan)}万・相続人${n}人`;$('kiso').textContent=num(kiso)+'万円';$('kazei').textContent=num(kazei)+'万円';$('judge').textContent=kazei<=0?'非課税の見込み🎉':'課税の可能性';
    SHARE=`相続税ざっくりシミュ、遺産${num(isan)}万・相続人${n}人で${kazei<=0?'基礎控除内＝非課税の見込み':'相続税の目安は約'+num(zei)+'万円'}でした📜\\nまずは把握から。👇`;show();anim($('big'),0,zei,900);}''')

if __name__=='__main__':
    write_all(SIMS)
    print(f'batch1 done. {len(SIMS)} sims.')
