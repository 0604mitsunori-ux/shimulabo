# -*- coding: utf-8 -*-
"""シミュラボ：旅行・おでかけカテゴリ 10本（gen_sims11のTPLを再利用）。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq, write_all

TRAVEL='旅行・おでかけ'
SIMS=[]

SIMS.append(dict(id='ryohi', cat=TRAVEL, emoji='✈️',
  title='旅行費用 総額シミュレーター｜その旅行、ぜんぶでいくら？｜シミュラボ',
  desc='人数・泊数・宿泊費・交通費・食費や遊び代から、旅行にかかる総額と1人あたりの費用を計算する無料シミュレーター。',
  ogtitle='旅行費用 総額シミュレーター｜ぜんぶでいくら？', ogdesc='人数・泊数・宿泊・交通・食費から、旅行の総額を計算。',
  h1='旅行費用 総額シミュレーター',
  lead='旅行の計画、結局いくらかかる？人数・泊数・宿泊費・交通費・食費から、旅行の総額と1人あたりを計算します。',
  inputs='''    <h2>✈️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>人数 <span class="hint">（人）</span></label><input type="number" id="people" value="2" min="1" max="30" inputmode="numeric"></div>
    <div class="field"><label>泊数 <span class="hint">（泊）</span></label><input type="number" id="nights" value="2" min="0" max="60" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>1人1泊の宿泊費 <span class="hint">（円）</span></label><input type="number" id="hotel" value="12000" min="0" inputmode="numeric"></div>
    <div class="field"><label>1人の往復交通費 <span class="hint">（円）</span></label><input type="number" id="trans" value="15000" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>1人1日の食費・遊び代 <span class="hint">（円）</span></label><input type="number" id="food" value="10000" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">総額を計算する</button>''',
  result='''      <div class="label">旅行の総額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1人あたり</div><div class="v accent" id="per">—</div></div>
      <div class="stat"><div class="k">宿泊計</div><div class="v" id="lodge">—</div></div>
      <div class="stat"><div class="k">交通計</div><div class="v" id="tr">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>宿泊 ＝ 人数 × 泊数 × 1泊宿泊費<br>交通 ＝ 人数 × 往復交通費<br>食費・遊び ＝ 人数 ×（泊数＋1日）× 1日の食費</div>
    <p>意外と効くのが現地での食費・お土産・アクティビティ。少し多めに見積もっておくと、現地で安心して楽しめます。早割やパックでさらに節約も。</p>
    <h2>よくある質問</h2>'''+faq([('お土産代は？','「食費・遊び代」に少し上乗せして入れておくのがおすすめです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const people=Math.max(1,+$('people').value||1), nights=Math.max(0,+$('nights').value||0), hotel=Math.max(0,+$('hotel').value||0), trans=Math.max(0,+$('trans').value||0), food=Math.max(0,+$('food').value||0);
    const lodge=people*nights*hotel, tr=people*trans, fd=people*(nights+1)*food, total=lodge+tr+fd;
    $('sub').textContent=`${people}人・${nights}泊${nights+1}日`;
    $('per').textContent=yen(total/people); $('lodge').textContent=yen(lodge); $('tr').textContent=yen(tr);
    SHARE=`旅行費用シミュ、${people}人の${nights}泊旅行は総額${yen(total)}でした✈️（1人${yen(total/people)}）\\n旅は計画から楽しい！👇`;
    show(); anim($('big'),0,total,900);
  }'''))

SIMS.append(dict(id='mile-tamaru', cat=TRAVEL, emoji='🎫',
  title='マイル特典航空券シミュレーター｜カード払いで何ヶ月で旅に行ける？｜シミュラボ',
  desc='毎月のカード利用額とマイル還元率から、特典航空券に必要なマイルが貯まるまでの期間を試算する無料シミュレーター。',
  ogtitle='マイル特典航空券シミュレーター｜何ヶ月で貯まる？', ogdesc='カード利用額と還元率から、特典航空券まで何ヶ月かを試算。',
  h1='マイル特典航空券シミュレーター',
  lead='普段の支払いをカードに集約すると、マイルがコツコツ貯まります。月の利用額から、特典航空券まで何ヶ月かを試算します。',
  inputs='''    <h2>🎫 条件を入れる</h2>
    <div class="field"><label>毎月のカード利用額 <span class="hint">（円）</span></label><input type="number" id="spend" value="150000" min="0" inputmode="numeric"></div>
    <div class="row"><div class="field"><label>100円あたりのマイル <span class="hint">（マイル）</span></label><input type="number" id="rate" value="1" min="0" max="20" step="0.1" inputmode="decimal"></div>
    <div class="field"><label>必要マイル <span class="hint">（例:国内往復15000）</span></label><input type="number" id="goal" value="15000" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">何ヶ月で貯まるか見る</button>''',
  result='''      <div class="label">特典航空券まで</div>
      <div class="big"><span id="big">0</span><span class="unit">ヶ月</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">月に貯まるマイル</div><div class="v accent" id="mm">—</div></div>
      <div class="stat"><div class="k">年間のマイル</div><div class="v" id="ym">—</div></div>
      <div class="stat"><div class="k">1年で行ける回数</div><div class="v" id="trips">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>月のマイル ＝ 月のカード利用額 ÷ 100 × 還元率<br>必要月数 ＝ 必要マイル ÷ 月のマイル</div>
    <p>家賃・光熱費・スマホ代など固定費をカード払いにまとめると、マイルは一気に貯まります。ボーナスマイルや搭乗マイルを足せばさらに早く到達。</p>
    <h2>よくある質問</h2>'''+faq([('還元率が分かりません','カードの「100円＝何マイル」を確認してください。一般的には0.5〜1.0が多いです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const spend=Math.max(0,+$('spend').value||0), rate=Math.max(0,+$('rate').value||0), goal=Math.max(1,+$('goal').value||1);
    const mm=spend/100*rate, months=mm>0?goal/mm:0, ym=mm*12, trips=goal>0?ym/goal:0;
    $('sub').textContent=`月${num(spend)}円・100円=${rate}マイル`;
    $('mm').textContent=num(mm)+'マイル'; $('ym').textContent=num(ym)+'マイル'; $('trips').textContent=trips.toFixed(1)+'回';
    SHARE=`マイルシミュ、特典航空券まで約${months>0?Math.ceil(months):'—'}ヶ月でした🎫（月${num(mm)}マイル）\\nカード払いで旅に行こ！👇`;
    show(); anim($('big'),0,months>0?Math.ceil(months):0,900);
  }'''))

SIMS.append(dict(id='jisa-boke', cat=TRAVEL, emoji='🕐',
  title='時差ボケ回復シミュレーター｜現地に慣れるまで何日？｜シミュラボ',
  desc='時差と移動方向（東行き・西行き）から、時差ボケが回復するまでの目安日数を試算する無料シミュレーター。',
  ogtitle='時差ボケ回復シミュレーター｜慣れるまで何日？', ogdesc='時差と移動方向から、時差ボケ回復の目安日数を試算。',
  h1='時差ボケ回復シミュレーター',
  lead='海外旅行の時差ボケ、何日で慣れる？時差と移動方向から、体内時計が現地に合うまでの目安日数を出します。',
  inputs='''    <h2>🕐 条件を入れる</h2>
    <div class="field"><label>時差 <span class="hint">（時間）</span></label><input type="number" id="diff" value="8" min="0" max="14" inputmode="numeric"></div>
    <div class="field"><label>移動の方向</label><select id="dir"><option value="east">東向き(日本→アメリカ等)</option><option value="west" selected>西向き(日本→ヨーロッパ等)</option></select></div>
    <button class="btn btn-primary" id="calcBtn">回復日数を見る</button>''',
  result='''      <div class="label">時差ボケ回復の目安</div>
      <div class="big"><span id="big">0</span><span class="unit">日</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:18px;">—</div>''',
  article='''    <h2>計算の考え方</h2>
    <div class="note"><strong>目安</strong><br>体内時計は1日に約1時間ずつ調整されると言われます。一般に「東向き」のほうが慣れにくく、回復に時間がかかる傾向があります。</div>
    <p>到着後はなるべく現地時間で行動し、朝に日光を浴びると体内時計が整いやすくなります。機内では水分をしっかり、アルコールは控えめに。</p>
    <h2>よくある質問</h2>'''+faq([('個人差はありますか？','大きいです。年齢・体質・睡眠で変わる目安としてお使いください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const diff=Math.max(0,+$('diff').value||0), dir=$('dir').value;
    const rate = dir==='east' ? 1.0 : 1.5;
    const days=Math.ceil(diff/rate);
    $('sub').textContent=`時差${diff}時間・${dir==='east'?'東向き(慣れにくい)':'西向き(比較的慣れやすい)'}`;
    $('adv').textContent='🕐 '+(dir==='east'?'東向きは要注意。到着後は朝の光を浴びて、早寝を心がけて。':'西向きは比較的ラク。夜ふかし気味に過ごすと合わせやすいです。');
    SHARE=`時差ボケ回復シミュ、時差${diff}時間の${dir==='east'?'東向き':'西向き'}で約${days}日かかる見込み🕐\\n旅の前に知っておこ。👇`;
    show(); anim($('big'),0,days,800);
  }'''))

SIMS.append(dict(id='kaigai-iju', cat=TRAVEL, emoji='🌏',
  title='海外移住の生活費シミュレーター｜あの国で暮らすと月いくら？｜シミュラボ',
  desc='日本での月の生活費と移住先の国を選ぶと、現地の物価水準に応じた月の生活費の目安を試算する無料シミュレーター。',
  ogtitle='海外移住の生活費シミュレーター｜月いくらで暮らせる？', ogdesc='日本の生活費と国の物価水準から、海外の生活費を試算。',
  h1='海外移住の生活費シミュレーター',
  lead='あの国で暮らすと、生活費はどう変わる？日本での月の生活費と移住先を選ぶと、現地の物価水準に応じた目安を出します。',
  inputs='''    <h2>🌏 条件を入れる</h2>
    <div class="field"><label>日本での月の生活費 <span class="hint">（円）</span></label><input type="number" id="cost" value="200000" min="0" inputmode="numeric"></div>
    <div class="field"><label>人数 <span class="hint">（人）</span></label><input type="number" id="people" value="1" min="1" max="10" inputmode="numeric"></div>
    <div class="field"><label>移住先の国</label><select id="country">
      <option value="0.5">タイ（物価 約半分）</option><option value="0.55">マレーシア</option><option value="0.45">ベトナム</option>
      <option value="0.8">台湾</option><option value="0.85">韓国</option><option value="1.3">アメリカ</option>
      <option value="1.4">オーストラリア</option><option value="1.2">ドイツ</option><option value="1.6">シンガポール</option></select></div>
    <button class="btn btn-primary" id="calcBtn">現地の生活費を見る</button>''',
  result='''      <div class="label">現地での月の生活費</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">年間</div><div class="v accent" id="year">—</div></div>
      <div class="stat"><div class="k">日本との差(月)</div><div class="v" id="diff">—</div></div>
      <div class="stat"><div class="k">物価水準</div><div class="v" id="lv">—</div></div></div>''',
  article='''    <h2>計算の考え方</h2>
    <div class="note"><strong>計算式</strong><br>現地の生活費 ＝ 日本の生活費 × 物価係数 ×（1＋（人数−1）×0.6）<br>※物価係数はざっくりの目安です。</div>
    <p>東南アジアは生活費が抑えやすく、欧米・シンガポールは高め。家賃・医療・教育・ビザ要件は国でまったく違うので、移住前にしっかり下調べを。</p>
    <h2>よくある質問</h2>'''+faq([('家賃も含まれますか？','「日本での生活費」に家賃を含めて入れれば、現地家賃も比例した概算になります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const cost=Math.max(0,+$('cost').value||0), people=Math.max(1,+$('people').value||1), k=+$('country').value||1;
    const m=cost*k*(1+(people-1)*0.6), diff=cost*(1+(people-1)*0.6)-m;
    $('sub').textContent=`${sel('country').text}・${people}人`;
    $('year').textContent=yen(m*12); $('diff').textContent=(diff>=0?'−':'+')+yen(Math.abs(diff)).replace('¥','¥'); $('lv').textContent='日本の'+Math.round(k*100)+'%';
    SHARE=`海外移住シミュ、${sel('country').text.replace(/（.*/,'')}なら月${yen(m)}で暮らせる計算でした🌏\\n物価は日本の${Math.round(k*100)}%。あなたは？👇`;
    show(); anim($('big'),0,m,900);
  }'''))

SIMS.append(dict(id='tabi-tsumitate', cat=TRAVEL, emoji='🐷',
  title='旅行貯金シミュレーター｜あの旅まで、毎月いくら貯める？｜シミュラボ',
  desc='目標金額・出発までの月数・今ある貯金から、旅行のために毎月いくら貯めればよいかを計算する無料シミュレーター。',
  ogtitle='旅行貯金シミュレーター｜毎月いくら貯める？', ogdesc='目標額と出発までの月数から、毎月の旅行貯金額を計算。',
  h1='旅行貯金シミュレーター',
  lead='行きたい旅のために、毎月いくら貯めればいい？目標金額・出発までの月数・今ある貯金から、毎月の積立額を計算します。',
  inputs='''    <h2>🐷 条件を入れる</h2>
    <div class="row"><div class="field"><label>目標金額 <span class="hint">（円）</span></label><input type="number" id="goal" value="300000" min="0" inputmode="numeric"></div>
    <div class="field"><label>今ある旅行貯金 <span class="hint">（円）</span></label><input type="number" id="now" value="0" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>出発まで <span class="hint">（ヶ月）</span></label><input type="number" id="months" value="12" min="1" max="120" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">毎月の貯金額を見る</button>''',
  result='''      <div class="label">毎月の貯金額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">あと必要な額</div><div class="v accent" id="need">—</div></div>
      <div class="stat"><div class="k">1日あたり</div><div class="v" id="day">—</div></div>
      <div class="stat"><div class="k">残り月数</div><div class="v" id="mo">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>毎月の貯金 ＝（目標金額 − 今ある貯金）÷ 残り月数</div>
    <p>「旅行専用の口座」を作って自動積立にすると、貯まりやすく使い込みも防げます。1日あたりに換算すると、ハードルがぐっと下がりますよ。</p>
    <h2>よくある質問</h2>'''+faq([('ボーナスも使いたい','ボーナス予定額を「今ある貯金」に足して計算すると、毎月の負担が軽くなります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const goal=Math.max(0,+$('goal').value||0), now=Math.max(0,+$('now').value||0), months=Math.max(1,+$('months').value||1);
    const need=Math.max(0,goal-now), monthly=need/months;
    $('sub').textContent=`目標${num(goal)}円・あと${months}ヶ月`;
    $('need').textContent=yen(need); $('day').textContent=yen(monthly/30.44); $('mo').textContent=months+'ヶ月';
    SHARE=`旅行貯金シミュ、目標${yen(goal)}まで毎月${yen(monthly)}（1日${yen(monthly/30.44)}）でいけるみたい🐷\\nその旅、現実にしよ！👇`;
    show(); anim($('big'),0,monthly,900);
  }'''))

SIMS.append(dict(id='lcc-shinkansen', cat=TRAVEL, emoji='🚄',
  title='LCC vs 新幹線シミュレーター｜安さと速さ、どっちを取る？｜シミュラボ',
  desc='LCCと新幹線の料金・所要時間を比べ、価格差と時間差、そして「時給いくらなら新幹線が得か」の境界を試算する無料シミュレーター。',
  ogtitle='LCC vs 新幹線｜安さと速さどっち？', ogdesc='LCCと新幹線の料金・時間を比較。損益分岐の時給も試算。',
  h1='LCC vs 新幹線シミュレーター',
  lead='安いLCCか、速くて楽な新幹線か。料金と所要時間を比べ、「自分の時間を時給いくらで考えると新幹線が得か」までを出します。',
  inputs='''    <h2>🚄 条件を入れる</h2>
    <div class="row"><div class="field"><label>LCCの総額 <span class="hint">（円・空港アクセス込み）</span></label><input type="number" id="lcc" value="8000" min="0" inputmode="numeric"></div>
    <div class="field"><label>LCCの総所要 <span class="hint">（時間・移動+待ち込み）</span></label><input type="number" id="lcct" value="4" min="0" step="0.5" inputmode="decimal"></div></div>
    <div class="row"><div class="field"><label>新幹線の料金 <span class="hint">（円）</span></label><input type="number" id="sh" value="14000" min="0" inputmode="numeric"></div>
    <div class="field"><label>新幹線の所要 <span class="hint">（時間）</span></label><input type="number" id="sht" value="2.5" min="0" step="0.5" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">比べてみる</button>''',
  result='''      <div class="label">新幹線が高い分の差額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">短縮できる時間</div><div class="v accent" id="save">—</div></div>
      <div class="stat"><div class="k">この時給以上なら新幹線が得</div><div class="v" id="break">—</div></div>
      <div class="stat"><div class="k">安いのは</div><div class="v" id="cheap">—</div></div></div>''',
  article='''    <h2>比べ方</h2>
    <div class="note"><strong>計算式</strong><br>価格差 ＝ 新幹線 − LCC／時間差 ＝ LCC所要 − 新幹線所要<br>損益分岐の時給 ＝ 価格差 ÷ 時間差</div>
    <p>浮いた時間の価値を自分の時給で考えると判断しやすくなります。LCCは安いぶん空港が遠く待ち時間も長め。荷物や乗り換えの手間も含めて選びましょう。</p>
    <h2>よくある質問</h2>'''+faq([('LCCは本当に安い？','セール時は格安ですが、空港アクセス・受託手荷物・座席指定で加算されることも。総額で入れると正確です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const lcc=Math.max(0,+$('lcc').value||0), lcct=Math.max(0,+$('lcct').value||0), sh=Math.max(0,+$('sh').value||0), sht=Math.max(0,+$('sht').value||0);
    const priceDiff=sh-lcc, timeDiff=lcct-sht, brk=timeDiff>0?priceDiff/timeDiff:0;
    function hm(h){ const m=Math.round(h*60); return Math.floor(m/60)+'時間'+(m%60)+'分'; }
    $('sub').textContent=`LCC ${num(lcc)}円/${hm(lcct)}・新幹線 ${num(sh)}円/${hm(sht)}`;
    $('save').textContent=hm(Math.max(0,timeDiff)); $('break').textContent=brk>0?yen(brk)+'/時':'—'; $('cheap').textContent=lcc<=sh?'LCC':'新幹線';
    SHARE=`LCC vs 新幹線、新幹線は${yen(Math.abs(priceDiff))}高いけど${hm(Math.max(0,timeDiff))}速い🚄\\n時給${brk>0?yen(brk):'—'}以上なら新幹線が得。あなたは？👇`;
    show(); anim($('big'),0,Math.abs(priceDiff),900);
  }'''))

SIMS.append(dict(id='gasolin-doko', cat=TRAVEL, emoji='🛻',
  title='満タンでどこまで行ける？シミュレーター｜航続距離マップ｜シミュラボ',
  desc='ガソリンタンクの容量と燃費から、満タンで走れる距離（航続距離）と給油額、地球1周の何%かを計算するエンタメシミュレーター。',
  ogtitle='満タンでどこまで行ける？｜航続距離シミュ', ogdesc='タンク容量と燃費から、満タンで走れる距離を計算。',
  h1='満タンでどこまで行ける？シミュレーター',
  lead='ガソリン満タンで、どこまで行ける？タンク容量と燃費から走れる距離を計算します。週末ドライブの行き先選びにも。',
  inputs='''    <h2>🛻 条件を入れる</h2>
    <div class="row"><div class="field"><label>タンク容量 <span class="hint">（L）</span></label><input type="number" id="tank" value="40" min="1" max="120" inputmode="numeric"></div>
    <div class="field"><label>燃費 <span class="hint">（km/L）</span></label><input type="number" id="nenpi" value="15" min="1" step="0.1" inputmode="decimal"></div></div>
    <div class="field"><label>ガソリン単価 <span class="hint">（円/L・給油額の計算用）</span></label><input type="number" id="price" value="175" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">航続距離を見る</button>''',
  result='''      <div class="label">満タンで走れる距離</div>
      <div class="big"><span id="big">0</span><span class="unit">km</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">満タン給油額</div><div class="v accent" id="cost">—</div></div>
      <div class="stat"><div class="k">地球1周の</div><div class="v" id="earth">—</div></div>
      <div class="stat"><div class="k">東京〜大阪(約500km)</div><div class="v" id="osaka">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>航続距離 ＝ タンク容量 × 燃費／給油額 ＝ タンク容量 × ガソリン単価</div>
    <p>実際はエアコンや渋滞で燃費は落ちます。ガス欠を防ぐため、残り1〜2目盛りでの給油が安心。長距離前は満タンにしておきましょう。</p>
    <h2>よくある質問</h2>'''+faq([('実際もこの距離走れますか？','カタログ燃費だと届かないことも。実燃費を入れると現実的な距離になります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const tank=Math.max(0,+$('tank').value||0), nenpi=Math.max(0.1,+$('nenpi').value||0.1), price=Math.max(0,+$('price').value||0);
    const range=tank*nenpi, cost=tank*price;
    $('sub').textContent=`タンク${tank}L × 燃費${nenpi}km/L`;
    $('cost').textContent=yen(cost); $('earth').textContent=(range/40075*100).toFixed(1)+'%'; $('osaka').textContent=(range/500).toFixed(1)+'回分';
    SHARE=`満タンでどこまで？シミュ、約${num(range)}km走れる計算でした🛻（給油${yen(cost)}）\\n東京〜大阪${(range/500).toFixed(1)}回分！どこ行く？👇`;
    show(); anim($('big'),0,range,900);
  }'''))

SIMS.append(dict(id='onsen-seiha', cat=TRAVEL, emoji='♨️',
  title='全国制覇まで何年？シミュレーター｜47都道府県・温泉めぐり｜シミュラボ',
  desc='都道府県・温泉地・道の駅などの制覇を目標に、年間の訪問ペースから全国制覇まで何年かかるかを計算するエンタメシミュレーター。',
  ogtitle='全国制覇まで何年？｜47都道府県・温泉めぐり', ogdesc='年間の訪問ペースから、全国制覇まで何年かを計算。',
  h1='全国制覇まで何年？シミュレーター',
  lead='47都道府県、全国の温泉、道の駅…。今のペースで、全部めぐり切るまで何年かかる？目標と年間ペースから制覇までの年数を出します。',
  inputs='''    <h2>♨️ 条件を入れる</h2>
    <div class="field"><label>制覇したいもの</label><select id="target"><option value="47">47都道府県</option><option value="100">温泉地100選</option><option value="100">日本百名山</option><option value="1209">道の駅(全国約1200)</option><option value="34">世界遺産(国内)</option></select></div>
    <div class="row"><div class="field"><label>年間の訪問数 <span class="hint">（年）</span></label><input type="number" id="pace" value="5" min="0.5" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>すでに達成した数</label><input type="number" id="done" value="10" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">制覇まで何年か見る</button>''',
  result='''      <div class="label">全国制覇まで</div>
      <div class="big"><span id="big">0</span><span class="unit">年</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">残り</div><div class="v accent" id="remain">—</div></div>
      <div class="stat"><div class="k">年間ペース</div><div class="v" id="pacev">—</div></div>
      <div class="stat"><div class="k">達成率</div><div class="v" id="rate">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>制覇までの年数 ＝（目標数 − 達成数）÷ 年間の訪問数</div>
    <p>「あと何年」が分かると、旅のモチベーションがぐっと上がります。スタンプ帳やマップアプリで記録すると、達成感が積み上がって楽しいですよ。</p>
    <h2>よくある質問</h2>'''+faq([('ペースを上げたら？','年間の訪問数を増やして再計算すると、ぐっと早く制覇できるのが分かります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const total=+$('target').value||47, pace=Math.max(0.1,+$('pace').value||0.1), done=Math.max(0,+$('done').value||0);
    const remain=Math.max(0,total-done), years=remain/pace, rate=Math.min(100,done/total*100);
    $('sub').textContent=`${sel('target').text}（全${total}）`;
    $('remain').textContent=num(remain)+'ヶ所'; $('pacev').textContent=pace+'/年'; $('rate').textContent=Math.round(rate)+'%';
    SHARE=`全国制覇シミュ、「${sel('target').text}」を今のペースだとあと約${years.toFixed(1)}年で制覇♨️（達成率${Math.round(rate)}%）\\nコツコツめぐろ！👇`;
    show(); anim($('big'),0,years,900,1);
  }'''))

SIMS.append(dict(id='sekai-isshu', cat=TRAVEL, emoji='🗺️',
  title='世界一周シミュレーター｜夢の世界一周、いくらかかる？｜シミュラボ',
  desc='旅の日数・1日あたりの予算・周遊航空券の費用から、世界一周にかかる総費用と1ヶ国あたりの予算を試算するエンタメシミュレーター。',
  ogtitle='世界一周シミュレーター｜いくらで一周できる？', ogdesc='日数・1日予算・航空券から、世界一周の費用を試算。',
  h1='世界一周シミュレーター',
  lead='一度は夢見る世界一周。旅の日数・1日の予算・航空券代から、トータルでいくらかかるかを試算します。妄想旅にどうぞ。',
  inputs='''    <h2>🗺️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>旅の日数 <span class="hint">（日）</span></label><input type="number" id="days" value="90" min="1" max="1000" inputmode="numeric"></div>
    <div class="field"><label>1日あたりの予算 <span class="hint">（円・宿+食+移動）</span></label><input type="number" id="perday" value="10000" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>周遊航空券・国際移動 <span class="hint">（円）</span></label><input type="number" id="air" value="400000" min="0" inputmode="numeric"></div>
    <div class="field"><label>訪れる国数 <span class="hint">（ヶ国）</span></label><input type="number" id="countries" value="15" min="1" max="100" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">総費用を見る</button>''',
  result='''      <div class="label">世界一周の総費用</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">現地滞在費</div><div class="v" id="stay">—</div></div>
      <div class="stat"><div class="k">1ヶ国あたり</div><div class="v accent" id="per">—</div></div>
      <div class="stat"><div class="k">1日あたり</div><div class="v" id="day">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>現地滞在費 ＝ 日数 × 1日の予算<br>総費用 ＝ 現地滞在費 ＋ 航空券・国際移動費</div>
    <p>節約スタイル（ゲストハウス・現地飯・陸路移動）なら1日1万円以下も可能。物価の安い東南アジア・中南米を長め、欧米を短めにすると総額を抑えられます。</p>
    <h2>よくある質問</h2>'''+faq([('ビザや保険は？','含まれていません。長期の海外旅行保険・ビザ代も別途見込んでください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const days=Math.max(1,+$('days').value||1), perday=Math.max(0,+$('perday').value||0), air=Math.max(0,+$('air').value||0), countries=Math.max(1,+$('countries').value||1);
    const stay=days*perday, total=stay+air;
    $('sub').textContent=`${days}日・${countries}ヶ国`;
    $('stay').textContent=yen(stay); $('per').textContent=yen(total/countries); $('day').textContent=yen(total/days);
    SHARE=`世界一周シミュ、${days}日で${countries}ヶ国まわると総額${yen(total)}でした🗺️（1ヶ国${yen(total/countries)}）\\nいつか行きたい…！👇`;
    show(); anim($('big'),0,total,900);
  }'''))

SIMS.append(dict(id='theme-park', cat=TRAVEL, emoji='🎢',
  title='テーマパーク1日予算シミュレーター｜1日遊ぶと1人いくら？｜シミュラボ',
  desc='チケット・食事・グッズ・交通費と人数から、テーマパークで1日遊ぶときの総額と1人あたりの予算を計算する無料シミュレーター。',
  ogtitle='テーマパーク1日予算シミュレーター｜1人いくら？', ogdesc='チケット・食事・グッズ・交通から、1日の予算を計算。',
  h1='テーマパーク1日予算シミュレーター',
  lead='テーマパークで1日遊ぶと、結局いくら？チケット・食事・グッズ・交通費と人数から、当日の総額と1人あたりを計算します。',
  inputs='''    <h2>🎢 1人あたりの費用を入れる</h2>
    <div class="row"><div class="field"><label>チケット <span class="hint">（円/人）</span></label><input type="number" id="ticket" value="9400" min="0" inputmode="numeric"></div>
    <div class="field"><label>食事・飲み物 <span class="hint">（円/人）</span></label><input type="number" id="food" value="4000" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>グッズ・お土産 <span class="hint">（円/人）</span></label><input type="number" id="goods" value="5000" min="0" inputmode="numeric"></div>
    <div class="field"><label>交通費 <span class="hint">（円/人・往復）</span></label><input type="number" id="trans" value="3000" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>人数 <span class="hint">（人）</span></label><input type="number" id="people" value="2" min="1" max="30" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">1日の予算を見る</button>''',
  result='''      <div class="label">テーマパーク 1日の総額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1人あたり</div><div class="v accent" id="per">—</div></div>
      <div class="stat"><div class="k">チケット計</div><div class="v" id="tk">—</div></div>
      <div class="stat"><div class="k">飲食・グッズ計</div><div class="v" id="fg">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>1人あたり ＝ チケット＋食事＋グッズ＋交通<br>総額 ＝ 1人あたり × 人数</div>
    <p>意外と効くのが食事とグッズ。あらかじめ予算を決めておくと、当日の使いすぎを防げます。年パスやセット券、早割の活用も◎。</p>
    <h2>よくある質問</h2>'''+faq([('ホテル代は？','日帰り前提の計算です。泊まる場合は宿泊費を別途加えてください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const ticket=Math.max(0,+$('ticket').value||0), food=Math.max(0,+$('food').value||0), goods=Math.max(0,+$('goods').value||0), trans=Math.max(0,+$('trans').value||0), people=Math.max(1,+$('people').value||1);
    const per=ticket+food+goods+trans, total=per*people;
    $('sub').textContent=`${people}人・1人あたり${yen(per)}`;
    $('per').textContent=yen(per); $('tk').textContent=yen(ticket*people); $('fg').textContent=yen((food+goods)*people);
    SHARE=`テーマパーク1日予算シミュ、${people}人で総額${yen(total)}でした🎢（1人${yen(per)}）\\n夢の国はお金もかかる…！👇`;
    show(); anim($('big'),0,total,900);
  }'''))

if __name__=='__main__':
    write_all(SIMS)
    print(f'travel done. {len(SIMS)} sims.')
