# -*- coding: utf-8 -*-
"""シミュラボ：グルメ・食カテゴリ 10本（gen_sims11のTPLを再利用）。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq, write_all

FOOD='グルメ・食'
SIMS=[]

SIMS.append(dict(id='ramen-roudou', cat=FOOD, emoji='🍜',
  title='ラーメン1杯の労働時間シミュレーター｜何分働けば一杯食べられる？｜シミュラボ',
  desc='ラーメンの値段と自分の時給から、一杯食べるために何分働く必要があるかを計算するエンタメシミュレーター。',
  ogtitle='ラーメン1杯の労働時間｜何分働けば食べられる？', ogdesc='ラーメンの値段と時給から、必要な労働時間を計算。',
  h1='ラーメン1杯の労働時間シミュレーター',
  lead='その一杯のために、あなたは何分働く？ラーメンの値段と時給から、一杯食べるのに必要な労働時間を計算します。お金と時間の関係を体感。',
  inputs='''    <h2>🍜 条件を入れる</h2>
    <div class="row"><div class="field"><label>ラーメン1杯の値段 <span class="hint">（円）</span></label><input type="number" id="price" value="900" min="0" inputmode="numeric"></div>
    <div class="field"><label>あなたの時給 <span class="hint">（円）</span></label><input type="number" id="wage" value="1100" min="1" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">労働時間を計算する</button>''',
  result='''      <div class="label">一杯のための労働時間</div>
      <div class="big"><span id="big">0</span><span class="unit">分</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">週1杯なら年間</div><div class="v accent" id="year">—</div></div>
      <div class="stat"><div class="k">月3杯の労働</div><div class="v" id="month">—</div></div>
      <div class="stat"><div class="k">時給</div><div class="v" id="wagev">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>労働時間（分）＝ 値段 ÷ 時給 × 60</div>
    <p>「いくらか」より「何時間ぶんの労働か」で考えると、お金の重みが変わって見えます。たまの一杯はごほうび、毎日だと労働時間もばかになりません。</p>
    <h2>よくある質問</h2>'''+faq([('税金は考慮されますか？','いいえ。額面の時給での概算です。手取り時給で入れるとより実感に近くなります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const price=Math.max(0,+$('price').value||0), wage=Math.max(1,+$('wage').value||1);
    const min=price/wage*60, yearMin=min*52, monthMin=min*3;
    $('sub').textContent=`${num(price)}円 ÷ 時給${num(wage)}円`;
    $('year').textContent=(yearMin/60).toFixed(1)+'時間'; $('month').textContent=num(monthMin)+'分'; $('wagev').textContent=num(wage)+'円';
    SHARE=`ラーメン1杯の労働時間シミュ、私は約${num(min)}分働かないと一杯食べられない🍜（時給${num(wage)}円）\\nありがたく味わお…！👇`;
    show(); anim($('big'),0,min,900);
  }'''))

SIMS.append(dict(id='gaishoku-jisui', cat=FOOD, emoji='🍳',
  title='外食 vs 自炊 シミュレーター｜自炊すると年いくら浮く？｜シミュラボ',
  desc='外食1食と自炊1食の費用、置き換える食数から、自炊にすると1年でどれだけ食費が浮くかを計算する無料シミュレーター。',
  ogtitle='外食 vs 自炊｜自炊すると年いくら浮く？', ogdesc='外食と自炊の差から、自炊で浮く食費を年間で計算。',
  h1='外食 vs 自炊 シミュレーター',
  lead='自炊って結局おトク？外食1食と自炊1食の費用から、自炊に置き換えると1年でどれだけ食費が浮くかを計算します。',
  inputs='''    <h2>🍳 条件を入れる</h2>
    <div class="row"><div class="field"><label>外食1食 <span class="hint">（円）</span></label><input type="number" id="out" value="900" min="0" inputmode="numeric"></div>
    <div class="field"><label>自炊1食 <span class="hint">（円）</span></label><input type="number" id="home" value="300" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>1日に自炊に置き換える食数 <span class="hint">（食）</span></label><input type="number" id="meals" value="2" min="0" max="3" step="0.5" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">浮く食費を見る</button>''',
  result='''      <div class="label">自炊で 1年に浮く食費</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1ヶ月あたり</div><div class="v" id="m">—</div></div>
      <div class="stat"><div class="k">10年で</div><div class="v accent" id="y10">—</div></div>
      <div class="stat"><div class="k">1食あたりの差</div><div class="v" id="per">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>年間の節約 ＝（外食1食 − 自炊1食）× 1日の食数 × 365</div>
    <p>自炊は食費だけでなく、栄養コントロールもしやすいのが利点。とはいえ時間と手間もかかるので、無理のない範囲でバランスを取るのがおすすめです。</p>
    <h2>よくある質問</h2>'''+faq([('調味料や光熱費は？','自炊1食の金額に少し上乗せして入れると、より実態に近くなります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const out=Math.max(0,+$('out').value||0), home=Math.max(0,+$('home').value||0), meals=Math.max(0,+$('meals').value||0);
    const diff=Math.max(0,out-home), year=diff*meals*365;
    $('sub').textContent=`差${num(diff)}円 × ${meals}食/日 × 365日`;
    $('m').textContent=yen(year/12); $('y10').textContent=yen(year*10); $('per').textContent=yen(diff);
    SHARE=`外食 vs 自炊シミュ、自炊にすると年で約${yen(year)}・10年で${yen(year*10)}も浮く計算でした🍳\\nがんばって自炊しよ…！👇`;
    show(); anim($('big'),0,year,900);
  }'''))

SIMS.append(dict(id='issho-tabemono', cat=FOOD, emoji='🍚',
  title='一生で食べる量シミュレーター｜あなたが一生で食べるお米は何kg？｜シミュラボ',
  desc='食べ物の種類と1日あたりの量、想定する年数から、一生で食べる総量を計算するエンタメシミュレーター。',
  ogtitle='一生で食べる量シミュレーター｜一生で何kg食べる？', ogdesc='食べ物と1日の量から、一生で食べる総量を計算。',
  h1='一生で食べる量シミュレーター',
  lead='お米、卵、パン…あなたが一生で食べる量は、どれくらい？食べ物と1日の量から、生涯の総量を計算します。想像すると、ちょっと感謝したくなる雑学。',
  inputs='''    <h2>🍚 条件を選ぶ</h2>
    <div class="field"><label>食べ物</label><select id="food"><option value="150">お米（1日150g）</option><option value="60">食パン（1日1枚60g）</option><option value="50">卵（1日1個50g）</option><option value="120">バナナ（1日1本120g）</option><option value="200">牛乳（1日200ml）</option></select></div>
    <div class="field"><label>これからの年数 <span class="hint">（年）</span></label><input type="number" id="years" value="60" min="1" max="100" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">一生分を見る</button>''',
  result='''      <div class="label">一生で食べる量</div>
      <div class="big"><span id="big">0</span><span class="unit">kg</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1年で</div><div class="v" id="year">—</div></div>
      <div class="stat"><div class="k">お相撲さん(150kg)何人分</div><div class="v accent" id="sumo">—</div></div>
      <div class="stat"><div class="k">これからの年数</div><div class="v" id="yv">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>一生で食べる量 ＝ 1日の量 × 365 × 年数</div>
    <p>毎日のお茶碗1杯でも、一生にするとびっくりする量に。私たちのカラダは、まさに食べたものでできています。日々の食事に感謝したくなりますね。</p>
    <h2>よくある質問</h2>'''+faq([('お相撲さん何人分って？','総量が体重150kgの人何人分かを表示しています（イメージ用）。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const g=+$('food').value||0, years=Math.max(1,+$('years').value||1);
    const kg=g*365*years/1000;
    $('sub').textContent=`${sel('food').text} × 365日 × ${years}年`;
    $('year').textContent=num(g*365/1000)+'kg'; $('sumo').textContent=(kg/150).toFixed(1)+'人分'; $('yv').textContent=years+'年';
    SHARE=`一生で食べる量シミュ、私が一生で食べる「${sel('food').text.replace(/（.*/,'')}」は約${num(kg)}kgでした🍚\\nお相撲さん${(kg/150).toFixed(1)}人分！あなたは？👇`;
    show(); anim($('big'),0,kg,900);
  }'''))

SIMS.append(dict(id='conveni-super', cat=FOOD, emoji='🛒',
  title='コンビニ vs スーパー シミュレーター｜コンビニ多用で年いくら損してる？｜シミュラボ',
  desc='1日のコンビニ食費と、同じものをスーパーで買った場合の金額から、1年・10年でどれだけ差がつくかを計算する無料シミュレーター。',
  ogtitle='コンビニ vs スーパー｜年いくら差がつく？', ogdesc='コンビニとスーパーの食費差を、年間で計算。',
  h1='コンビニ vs スーパー シミュレーター',
  lead='便利なコンビニ、でもスーパーと比べると…？1日のコンビニ食費と、スーパーで買った場合の金額から、積み上がる差額を出します。',
  inputs='''    <h2>🛒 条件を入れる</h2>
    <div class="row"><div class="field"><label>1日のコンビニ食費 <span class="hint">（円）</span></label><input type="number" id="conveni" value="700" min="0" inputmode="numeric"></div>
    <div class="field"><label>スーパーなら同じ物が <span class="hint">（円）</span></label><input type="number" id="super" value="450" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">差額を見る</button>''',
  result='''      <div class="label">1年で 多く払っている額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1ヶ月で</div><div class="v" id="m">—</div></div>
      <div class="stat"><div class="k">10年で</div><div class="v accent" id="y10">—</div></div>
      <div class="stat"><div class="k">1日あたりの差</div><div class="v" id="per">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>1年の差額 ＝（コンビニ − スーパー）× 365</div>
    <p>コンビニは時間や手間を買っている面もあるので、悪ではありません。ただ「差額」を知っておくと、ここぞの場面で使い分けられます。まとめ買い・作り置きも有効。</p>
    <h2>よくある質問</h2>'''+faq([('全部スーパーにすべき？','いいえ。便利さの価値もあります。差を知って、自分なりの使い方を決めるのがおすすめです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const c=Math.max(0,+$('conveni').value||0), s=Math.max(0,+$('super').value||0);
    const diff=Math.max(0,c-s), year=diff*365;
    $('sub').textContent=`差${num(diff)}円/日 × 365日`;
    $('m').textContent=yen(year/12); $('y10').textContent=yen(year*10); $('per').textContent=yen(diff);
    SHARE=`コンビニ vs スーパー、コンビニ多用で年に約${yen(year)}多く払ってた🛒（10年で${yen(year*10)}）\\n使い分け大事…！👇`;
    show(); anim($('big'),0,year,900);
  }'''))

SIMS.append(dict(id='karori-undou', cat=FOOD, emoji='🏃',
  title='食べ物のカロリー消費シミュレーター｜この一品、運動で消すと何分？｜シミュラボ',
  desc='食べ物のカロリーと体重から、ウォーキング・ランニング・自転車で消費するのに必要な運動時間を計算する無料シミュレーター。',
  ogtitle='食べ物のカロリー消費｜運動で消すと何分？', ogdesc='食べ物のカロリーと体重から、消費に必要な運動時間を計算。',
  h1='食べ物のカロリー消費シミュレーター',
  lead='そのケーキ、運動で消すなら何分？食べ物のカロリーと体重から、ウォーキング・ランニング・自転車での消費時間を計算します。',
  inputs='''    <h2>🏃 条件を選ぶ</h2>
    <div class="field"><label>食べ物</label><select id="food"><option value="500">ラーメン1杯</option><option value="350" selected>ショートケーキ</option><option value="340">ポテチ1袋</option><option value="500">ハンバーガー</option><option value="140">ビール中1杯</option><option value="250">ごはん1杯</option></select></div>
    <div class="field"><label>体重 <span class="hint">（kg）</span></label><input type="number" id="w" value="60" min="20" max="200" step="0.1" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">消費時間を見る</button>''',
  result='''      <div class="label">ウォーキングで消費するなら</div>
      <div class="big"><span id="big">0</span><span class="unit">分</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">ランニング</div><div class="v accent" id="run">—</div></div>
      <div class="stat"><div class="k">自転車</div><div class="v" id="bike">—</div></div>
      <div class="stat"><div class="k">カロリー</div><div class="v" id="kcal">—</div></div></div>''',
  article='''    <h2>計算の考え方</h2>
    <div class="note"><strong>計算式（体重60kgの目安）</strong><br>消費時間 ＝ カロリー ÷（運動ごとの1分あたり消費）<br>ウォーキング約3.6／ランニング約8.4／自転車約6.3 kcal/分（体重で変動）</div>
    <p>「食べた分を運動で消す」とけっこう大変なのが分かります。だからこそ、食べすぎを防ぐのがいちばんの近道。運動は楽しく続けるのがコツです。</p>
    <h2>よくある質問</h2>'''+faq([('正確な消費量ですか？','体重・強度で変わる概算です。傾向の目安としてお使いください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const kcal=+$('food').value||0, w=Math.max(1,+$('w').value||1);
    const walk=kcal/(0.06*w), run=kcal/(0.14*w), bike=kcal/(0.105*w);
    $('sub').textContent=`${sel('food').text}（${kcal}kcal）・体重${w}kg`;
    $('run').textContent=num(run)+'分'; $('bike').textContent=num(bike)+'分'; $('kcal').textContent=kcal+'kcal';
    SHARE=`「${sel('food').text}」を消費するには、ウォーキング約${num(walk)}分・ランニング約${num(run)}分が必要でした🏃\\n食べる前にひとがんばり…！👇`;
    show(); anim($('big'),0,walk,900);
  }'''))

SIMS.append(dict(id='cafe-nenkan', cat=FOOD, emoji='☕',
  title='カフェ代 年間シミュレーター｜カフェ通い、年いくら使ってる？｜シミュラボ',
  desc='1杯の値段と週の利用回数から、カフェ・コーヒーショップに年間・10年でいくら使っているかを計算する無料シミュレーター。',
  ogtitle='カフェ代 年間シミュレーター｜年いくら使ってる？', ogdesc='1杯の値段と週の回数から、カフェ代を年間で計算。',
  h1='カフェ代 年間シミュレーター',
  lead='毎日の一杯、塵も積もれば…。カフェの1杯の値段と週の利用回数から、年間・10年でいくら使っているかを計算します。',
  inputs='''    <h2>☕ 条件を入れる</h2>
    <div class="row"><div class="field"><label>1杯の値段 <span class="hint">（円）</span></label><input type="number" id="price" value="500" min="0" inputmode="numeric"></div>
    <div class="field"><label>週に何回 <span class="hint">（回）</span></label><input type="number" id="freq" value="5" min="0" max="30" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">年間のカフェ代を見る</button>''',
  result='''      <div class="label">年間のカフェ代</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1ヶ月あたり</div><div class="v" id="m">—</div></div>
      <div class="stat"><div class="k">10年で</div><div class="v accent" id="y10">—</div></div>
      <div class="stat"><div class="k">年間の杯数</div><div class="v" id="cups">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>年間のカフェ代 ＝ 1杯の値段 × 週の回数 × 52週</div>
    <p>カフェタイムは大事な息抜き。ただ金額にすると意外と大きいので、たまにマイボトルや家コーヒーに替えるだけでも、年単位では効いてきます。</p>
    <h2>よくある質問</h2>'''+faq([('我慢すべき？','いいえ。楽しみは大事です。金額を知って、自分にちょうどいい頻度を見つけましょう。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const price=Math.max(0,+$('price').value||0), freq=Math.max(0,+$('freq').value||0);
    const year=price*freq*52, cups=freq*52;
    $('sub').textContent=`${num(price)}円 × 週${freq}回 × 52週`;
    $('m').textContent=yen(year/12); $('y10').textContent=yen(year*10); $('cups').textContent=num(cups)+'杯';
    SHARE=`カフェ代の年間シミュ、私は年で約${yen(year)}使ってた☕（10年で${yen(year*10)}）\\nおいしいから、まあいっか…！あなたは？👇`;
    show(); anim($('big'),0,year,900);
  }'''))

SIMS.append(dict(id='obento-lunch', cat=FOOD, emoji='🍱',
  title='お弁当 vs 外食ランチ シミュレーター｜お弁当にすると年いくら浮く？｜シミュラボ',
  desc='外食ランチと手作り弁当の費用、週の出勤日数から、お弁当に替えると1年でどれだけ浮くかを計算する無料シミュレーター。',
  ogtitle='お弁当 vs 外食ランチ｜年いくら浮く？', ogdesc='外食ランチと手作り弁当の差から、年間の節約額を計算。',
  h1='お弁当 vs 外食ランチ シミュレーター',
  lead='毎日のランチ、外食かお弁当か。外食ランチと手作り弁当の費用から、お弁当に替えると1年でどれだけ浮くかを計算します。',
  inputs='''    <h2>🍱 条件を入れる</h2>
    <div class="row"><div class="field"><label>外食ランチ <span class="hint">（円/食）</span></label><input type="number" id="out" value="900" min="0" inputmode="numeric"></div>
    <div class="field"><label>手作り弁当 <span class="hint">（円/食）</span></label><input type="number" id="bento" value="300" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>週の出勤日数 <span class="hint">（日）</span></label><input type="number" id="days" value="5" min="0" max="7" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">浮く金額を見る</button>''',
  result='''      <div class="label">お弁当で 1年に浮く額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1ヶ月あたり</div><div class="v" id="m">—</div></div>
      <div class="stat"><div class="k">10年で</div><div class="v accent" id="y10">—</div></div>
      <div class="stat"><div class="k">1食あたりの差</div><div class="v" id="per">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>年間の節約 ＝（外食 − お弁当）× 週の出勤日数 × 52週</div>
    <p>毎日のランチ差600円でも、年間ではかなりの額。とはいえ毎日のお弁当作りは負担にもなるので、週の半分だけでも効果は十分あります。</p>
    <h2>よくある質問</h2>'''+faq([('お弁当の材料費は？','「手作り弁当」の金額に材料費を含めて入れてください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const out=Math.max(0,+$('out').value||0), bento=Math.max(0,+$('bento').value||0), days=Math.max(0,+$('days').value||0);
    const diff=Math.max(0,out-bento), year=diff*days*52;
    $('sub').textContent=`差${num(diff)}円 × 週${days}日 × 52週`;
    $('m').textContent=yen(year/12); $('y10').textContent=yen(year*10); $('per').textContent=yen(diff);
    SHARE=`お弁当 vs 外食ランチ、お弁当にすると年で約${yen(year)}・10年で${yen(year*10)}も浮く計算でした🍱\\n明日からお弁当…！？👇`;
    show(); anim($('big'),0,year,900);
  }'''))

SIMS.append(dict(id='tabehoudai', cat=FOOD, emoji='🍽️',
  title='食べ放題の元取りシミュレーター｜あと何皿で元が取れる？｜シミュラボ',
  desc='食べ放題の料金と1品の通常価格、食べた数から、元が取れているか・あと何皿で元が取れるかを計算するエンタメシミュレーター。',
  ogtitle='食べ放題の元取りシミュレーター｜元取れてる？', ogdesc='食べ放題の料金と1品の価格から、元取りラインを計算。',
  h1='食べ放題の元取りシミュレーター',
  lead='その食べ放題、元取れてる？料金と1品の通常価格、食べた数から、損か得か・あと何皿で元が取れるかを判定します。次の一皿の参考に。',
  inputs='''    <h2>🍽️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>食べ放題の料金 <span class="hint">（円）</span></label><input type="number" id="price" value="3000" min="0" inputmode="numeric"></div>
    <div class="field"><label>1品の通常価格 <span class="hint">（円）</span></label><input type="number" id="unit" value="400" min="1" inputmode="numeric"></div></div>
    <div class="field"><label>食べた数 <span class="hint">（品）</span></label><input type="number" id="eaten" value="6" min="0" max="100" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">損得を判定する</button>''',
  result='''      <div class="label" id="lab">今のところ</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">元取りライン</div><div class="v accent" id="be">—</div></div>
      <div class="stat"><div class="k">食べた分の価値</div><div class="v" id="value">—</div></div>
      <div class="stat"><div class="k">あと何品で元取り</div><div class="v" id="more">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>元取りライン ＝ 料金 ÷ 1品の価格<br>損得 ＝ 食べた数 × 1品の価格 − 料金</div>
    <p>「元を取る」を目指すと食べすぎてしまうもの。本来は楽しんで満足することがいちばんの「得」です。数字はあくまでネタとしてどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([('飲み放題は？','本ツールは食べ物のみの計算です。ドリンクは別途加えて考えてください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const price=Math.max(0,+$('price').value||0), unit=Math.max(1,+$('unit').value||1), eaten=Math.max(0,+$('eaten').value||0);
    const be=price/unit, value=eaten*unit, profit=value-price, more=Math.max(0,Math.ceil(be-eaten));
    $('lab').textContent= profit>=0?'今のところ お得（プラス）':'今のところ まだ損（マイナス）';
    $('sub').textContent=`料金${num(price)}円・1品${num(unit)}円・${eaten}品`;
    $('be').textContent=Math.ceil(be)+'品'; $('value').textContent=yen(value); $('more').textContent= more>0?more+'品':'達成済み🎉';
    SHARE=`食べ放題の元取りシミュ、${eaten}品食べて${profit>=0?'プラス'+yen(profit):'あと'+yen(-profit)+'で元取り'}🍽️\\n元取りラインは${Math.ceil(be)}品。あなたは何品いける？👇`;
    show(); anim($('big'),0,Math.abs(profit),900);
  }'''))

SIMS.append(dict(id='uber-jisui', cat=FOOD, emoji='🛵',
  title='フードデリバリー vs 自炊 シミュレーター｜デリバリー、年いくら高い？｜シミュラボ',
  desc='フードデリバリー1食（手数料込み）と自炊1食の費用、月の利用回数から、1年でどれだけ差がつくかを計算する無料シミュレーター。',
  ogtitle='デリバリー vs 自炊｜年いくら高い？', ogdesc='デリバリーと自炊の差から、年間の差額を計算。',
  h1='フードデリバリー vs 自炊 シミュレーター',
  lead='便利なフードデリバリー、でも手数料込みだと…？1食の費用と月の利用回数から、自炊と比べて1年でどれだけ差がつくかを出します。',
  inputs='''    <h2>🛵 条件を入れる</h2>
    <div class="row"><div class="field"><label>デリバリー1食 <span class="hint">（円・配送料込み）</span></label><input type="number" id="uber" value="1800" min="0" inputmode="numeric"></div>
    <div class="field"><label>自炊1食 <span class="hint">（円）</span></label><input type="number" id="home" value="300" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>月の利用回数 <span class="hint">（回）</span></label><input type="number" id="freq" value="8" min="0" max="90" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">差額を見る</button>''',
  result='''      <div class="label">自炊と比べて 1年に多く払う額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1ヶ月あたり</div><div class="v" id="m">—</div></div>
      <div class="stat"><div class="k">10年で</div><div class="v accent" id="y10">—</div></div>
      <div class="stat"><div class="k">1食あたりの差</div><div class="v" id="per">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>年間の差 ＝（デリバリー1食 − 自炊1食）× 月の利用回数 × 12</div>
    <p>デリバリーは「時間と手間」を買うサービス。忙しい日や疲れた日には十分価値があります。金額を知ったうえで、ここぞの場面で使うのが賢い使い方。</p>
    <h2>よくある質問</h2>'''+faq([('配送料や手数料は？','「デリバリー1食」に配送料・サービス料込みの金額を入れてください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const uber=Math.max(0,+$('uber').value||0), home=Math.max(0,+$('home').value||0), freq=Math.max(0,+$('freq').value||0);
    const diff=Math.max(0,uber-home), year=diff*freq*12;
    $('sub').textContent=`差${num(diff)}円 × 月${freq}回 × 12ヶ月`;
    $('m').textContent=yen(year/12); $('y10').textContent=yen(year*10); $('per').textContent=yen(diff);
    SHARE=`デリバリー vs 自炊、デリバリーは年で約${yen(year)}多く払う計算でした🛵（10年で${yen(year*10)}）\\n便利さの値段だなぁ。👇`;
    show(); anim($('big'),0,year,900);
  }'''))

SIMS.append(dict(id='nomikai-nenkan', cat=FOOD, emoji='🍻',
  title='飲み会の年間予算シミュレーター｜飲み会、年いくら使ってる？｜シミュラボ',
  desc='1回の飲み会の金額と月の回数から、飲み会に年間・10年でいくら使っているかを計算する無料シミュレーター。',
  ogtitle='飲み会の年間予算シミュレーター｜年いくら使ってる？', ogdesc='1回の金額と月の回数から、飲み会代を年間で計算。',
  h1='飲み会の年間予算シミュレーター',
  lead='付き合いも大事だけど、飲み会代って年でいくら？1回の金額と月の回数から、年間・10年の飲み会予算を出します。',
  inputs='''    <h2>🍻 条件を入れる</h2>
    <div class="row"><div class="field"><label>1回の飲み会 <span class="hint">（円）</span></label><input type="number" id="price" value="5000" min="0" inputmode="numeric"></div>
    <div class="field"><label>月に何回 <span class="hint">（回）</span></label><input type="number" id="freq" value="3" min="0" max="30" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">年間予算を見る</button>''',
  result='''      <div class="label">年間の飲み会代</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1ヶ月あたり</div><div class="v" id="m">—</div></div>
      <div class="stat"><div class="k">10年で</div><div class="v accent" id="y10">—</div></div>
      <div class="stat"><div class="k">年間の回数</div><div class="v" id="times">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>年間の飲み会代 ＝ 1回の金額 × 月の回数 × 12</div>
    <p>飲み会は人とのつながりを育てる大切な時間。一方で金額にすると大きいので、回数や一次会のみにするなど、バランスを取るのも手です。</p>
    <h2>よくある質問</h2>'''+faq([('交通費は？','含まれていません。タクシー代などは別途見込んでください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const price=Math.max(0,+$('price').value||0), freq=Math.max(0,+$('freq').value||0);
    const year=price*freq*12, times=freq*12;
    $('sub').textContent=`${num(price)}円 × 月${freq}回 × 12ヶ月`;
    $('m').textContent=yen(year/12); $('y10').textContent=yen(year*10); $('times').textContent=num(times)+'回';
    SHARE=`飲み会の年間予算シミュ、私は年で約${yen(year)}使ってた🍻（10年で${yen(year*10)}）\\n楽しいけど、お財布は正直…！👇`;
    show(); anim($('big'),0,year,900);
  }'''))

if __name__=='__main__':
    write_all(SIMS)
    print(f'food done. {len(SIMS)} sims.')
