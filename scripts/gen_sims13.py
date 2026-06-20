# -*- coding: utf-8 -*-
"""シミュラボ：クルマ・乗り物カテゴリ 10本（gen_sims11のTPLを再利用）。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq, write_all

CAR='クルマ・乗り物'
SIMS=[]

SIMS.append(dict(id='nenpi-gas', cat=CAR, emoji='⛽',
  title='年間ガソリン代シミュレーター｜車の維持、ガソリン代は年いくら？｜シミュラボ',
  desc='年間走行距離・燃費・ガソリン単価から、1年・1ヶ月のガソリン代と給油量を計算する無料シミュレーター。',
  ogtitle='年間ガソリン代シミュレーター｜年いくらかかる？', ogdesc='走行距離・燃費・単価から、年間のガソリン代を計算。',
  h1='年間ガソリン代シミュレーター',
  lead='毎月地味に効くガソリン代。年間走行距離・燃費・ガソリン単価から、1年でいくらかかるかを計算します。',
  inputs='''    <h2>⛽ 条件を入れる</h2>
    <div class="row"><div class="field"><label>年間走行距離 <span class="hint">（km）</span></label><input type="number" id="dist" value="8000" min="0" inputmode="numeric"></div>
    <div class="field"><label>燃費 <span class="hint">（km/L）</span></label><input type="number" id="nenpi" value="15" min="1" max="50" step="0.1" inputmode="decimal"></div></div>
    <div class="field"><label>ガソリン単価 <span class="hint">（円/L）</span></label><input type="number" id="price" value="175" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">ガソリン代を計算する</button>''',
  result='''      <div class="label">年間のガソリン代</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1ヶ月あたり</div><div class="v accent" id="m">—</div></div>
      <div class="stat"><div class="k">年間の給油量</div><div class="v" id="l">—</div></div>
      <div class="stat"><div class="k">5年で</div><div class="v" id="y5">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>年間ガソリン代 ＝ 年間走行距離 ÷ 燃費 × ガソリン単価</div>
    <p>燃費の良い車に乗り換えると、ここが大きく変わります。エコ運転（急発進・急加速を控える）でも数％は改善できます。</p>
    <h2>よくある質問</h2>'''+faq([('実燃費とカタログ燃費は違いますか？','はい。実燃費はカタログより1〜3割悪いことが多いです。実燃費で入れると正確です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const dist=Math.max(0,+$('dist').value||0), nenpi=Math.max(0.1,+$('nenpi').value||0.1), price=Math.max(0,+$('price').value||0);
    const liters=dist/nenpi, year=liters*price;
    $('sub').textContent=`${num(dist)}km ÷ ${nenpi}km/L × ${price}円`;
    $('m').textContent=yen(year/12); $('l').textContent=num(liters)+'L'; $('y5').textContent=yen(year*5);
    SHARE=`年間のガソリン代、約${yen(year)}でした⛽（月${yen(year/12)}）\\n燃費って大事…！あなたは？👇`;
    show(); anim($('big'),0,year,900);
  }'''))

SIMS.append(dict(id='ev-vs-gas', cat=CAR, emoji='🔌',
  title='EV vs ガソリン車 燃料費シミュレーター｜電気とガソリン、どっちが得？｜シミュラボ',
  desc='年間走行距離をもとに、EV（電気自動車）の電気代とガソリン車のガソリン代を比較し、どちらがどれだけ得かを試算する無料シミュレーター。',
  ogtitle='EV vs ガソリン車 燃料費｜どっちが得？', ogdesc='年間走行距離から、EVの電気代とガソリン代を比較。',
  h1='EV vs ガソリン車 燃料費シミュレーター',
  lead='EVは本当に安い？年間走行距離をもとに、電気自動車の電気代とガソリン車のガソリン代を比べ、どちらがどれだけお得かを試算します。',
  inputs='''    <h2>🔌 条件を入れる</h2>
    <div class="field"><label>年間走行距離 <span class="hint">（km）</span></label><input type="number" id="dist" value="10000" min="0" inputmode="numeric"></div>
    <div class="row"><div class="field"><label>ガソリン車の燃費 <span class="hint">（km/L）</span></label><input type="number" id="nenpi" value="15" min="1" step="0.1" inputmode="decimal"></div>
    <div class="field"><label>ガソリン単価 <span class="hint">（円/L）</span></label><input type="number" id="gp" value="175" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>EVの電費 <span class="hint">（km/kWh）</span></label><input type="number" id="denpi" value="7" min="1" step="0.1" inputmode="decimal"></div>
    <div class="field"><label>電気単価 <span class="hint">（円/kWh）</span></label><input type="number" id="ep" value="30" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">どっちが得か見る</button>''',
  result='''      <div class="label" id="lab">EVなら 年間で安くなる額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">ガソリン車(年)</div><div class="v" id="g">—</div></div>
      <div class="stat"><div class="k">EV(年)</div><div class="v accent" id="e">—</div></div>
      <div class="stat"><div class="k">10年の差</div><div class="v" id="d10">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>ガソリン代 ＝ 距離 ÷ 燃費 × ガソリン単価<br>電気代 ＝ 距離 ÷ 電費 × 電気単価</div>
    <p>燃料費だけならEVが有利なことが多いですが、車両価格・バッテリー・充電環境も含めた総額で判断を。自宅充電か外部充電かでも電気単価は変わります。</p>
    <h2>よくある質問</h2>'''+faq([('車両価格は含まれますか？','いいえ。本ツールは燃料費のみの比較です。総コストは車両価格も含めて検討してください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const dist=Math.max(0,+$('dist').value||0), nenpi=Math.max(0.1,+$('nenpi').value||0.1), gp=Math.max(0,+$('gp').value||0), denpi=Math.max(0.1,+$('denpi').value||0.1), ep=Math.max(0,+$('ep').value||0);
    const g=dist/nenpi*gp, e=dist/denpi*ep, diff=g-e;
    $('lab').textContent= diff>=0?'EVなら 年間で安くなる額':'ガソリン車のほうが 年間で安い額';
    $('sub').textContent=`年${num(dist)}km・ガソリン${gp}円/L・電気${ep}円/kWh`;
    $('g').textContent=yen(g); $('e').textContent=yen(e); $('d10').textContent=yen(Math.abs(diff)*10);
    SHARE= diff>=0?`EV vs ガソリン、燃料費はEVが年${yen(Math.abs(diff))}お得だった🔌（10年で${yen(Math.abs(diff)*10)}）\\nあなたは？👇`:`燃料費はガソリン車が年${yen(Math.abs(diff))}お得という結果に🔌\\n条件しだいだなぁ👇`;
    show(); anim($('big'),0,Math.abs(diff),900);
  }'''))

SIMS.append(dict(id='kuruma-yosan', cat=CAR, emoji='🚗',
  title='車購入予算シミュレーター｜年収でいくらの車が買える？｜シミュラボ',
  desc='年収・頭金・毎月の支払い上限から、無理のない車の購入予算の目安を試算する無料シミュレーター。',
  ogtitle='車購入予算シミュレーター｜年収でいくらの車が買える？', ogdesc='年収・頭金・月々の支払いから、無理のない車予算を試算。',
  h1='車購入予算シミュレーター',
  lead='年収に対して、どのくらいの車なら無理がない？年収・頭金・毎月の支払い上限から、車の購入予算の目安を出します。',
  inputs='''    <h2>🚗 条件を入れる</h2>
    <div class="row"><div class="field"><label>年収 <span class="hint">（万円）</span></label><input type="number" id="income" value="500" min="0" inputmode="numeric"></div>
    <div class="field"><label>頭金 <span class="hint">（万円）</span></label><input type="number" id="down" value="50" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>毎月の支払い上限 <span class="hint">（万円）</span></label><input type="number" id="month" value="3" min="0" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>ローン年数 <span class="hint">（年）</span></label><input type="number" id="years" value="5" min="1" max="10" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">予算を見る</button>''',
  result='''      <div class="label">無理のない車の予算</div>
      <div class="big"><span id="big">0</span><span class="unit">万円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">年収50%の目安</div><div class="v" id="half">—</div></div>
      <div class="stat"><div class="k">ローン総額</div><div class="v" id="loan">—</div></div>
      <div class="stat"><div class="k">毎月の支払い</div><div class="v accent" id="pay">—</div></div></div>''',
  article='''    <h2>予算の考え方</h2>
    <div class="note"><strong>考え方</strong><br>予算 ＝ 頭金 ＋（毎月の支払い × 12 × ローン年数）<br>一般に「車両価格は年収の半分まで」が無理のない目安と言われます。</div>
    <p>車は購入後も税金・保険・車検・ガソリン・駐車場がかかります。本体価格だけでなく、維持費も含めて余裕を持った予算にしましょう。</p>
    <h2>よくある質問</h2>'''+faq([('金利は含まれますか？','本ツールは無金利の概算です。実際はローン金利が上乗せされます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const income=Math.max(0,+$('income').value||0), down=Math.max(0,+$('down').value||0), month=Math.max(0,+$('month').value||0), years=Math.max(1,+$('years').value||1);
    const loan=month*12*years, budget=down+loan, half=income*0.5;
    $('sub').textContent=`頭金${down}万＋月${month}万×${years}年`;
    $('half').textContent=num(half)+'万円'; $('loan').textContent=num(loan)+'万円'; $('pay').textContent=num(month)+'万円/月';
    SHARE=`車購入予算シミュ、私の予算は約${num(budget)}万円でした🚗（年収50%目安は${num(half)}万円）\\nあなたは？👇`;
    show(); anim($('big'),0,budget,900);
  }'''))

SIMS.append(dict(id='kousoku-shita', cat=CAR, emoji='🛣️',
  title='高速 vs 下道シミュレーター｜時間を取る？お金を取る？｜シミュラボ',
  desc='距離・高速料金・平均速度から、高速道路と下道でかかる時間とお金を比較し、高速で短縮できる時間と追加費用を試算する無料シミュレーター。',
  ogtitle='高速 vs 下道シミュレーター｜時間とお金どっち？', ogdesc='高速と下道の時間・費用を比較。短縮時間と追加費用を試算。',
  h1='高速 vs 下道シミュレーター',
  lead='急ぐなら高速、節約なら下道。距離・高速料金・平均速度から、高速で短縮できる時間と、その分かかる追加費用を比べます。',
  inputs='''    <h2>🛣️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>距離 <span class="hint">（km）</span></label><input type="number" id="dist" value="300" min="0" inputmode="numeric"></div>
    <div class="field"><label>高速料金 <span class="hint">（円・片道）</span></label><input type="number" id="toll" value="6000" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>高速の平均速度 <span class="hint">（km/h）</span></label><input type="number" id="vh" value="80" min="10" inputmode="numeric"></div>
    <div class="field"><label>下道の平均速度 <span class="hint">（km/h）</span></label><input type="number" id="vl" value="35" min="5" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">比べてみる</button>''',
  result='''      <div class="label">高速で短縮できる時間</div>
      <div class="big"><span id="big">0</span><span class="unit">分</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">高速の所要</div><div class="v" id="th">—</div></div>
      <div class="stat"><div class="k">下道の所要</div><div class="v" id="tl">—</div></div>
      <div class="stat"><div class="k">時短1時間あたりの費用</div><div class="v accent" id="per">—</div></div></div>''',
  article='''    <h2>比べ方</h2>
    <div class="note"><strong>計算式</strong><br>所要時間 ＝ 距離 ÷ 平均速度<br>短縮時間 ＝ 下道の時間 − 高速の時間／追加費用 ＝ 高速料金</div>
    <p>「時短1時間あたりの費用」が自分の時給より安いと感じれば高速がお得。長距離・急ぎなら高速、近場・のんびりなら下道と使い分けを。</p>
    <h2>よくある質問</h2>'''+faq([('ガソリン代の差は？','高速のほうが燃費が良い傾向ですが、本ツールは時間と高速料金の比較に絞っています。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const dist=Math.max(0,+$('dist').value||0), toll=Math.max(0,+$('toll').value||0), vh=Math.max(1,+$('vh').value||1), vl=Math.max(1,+$('vl').value||1);
    const th=dist/vh, tl=dist/vl, save=(tl-th)*60, perHr=save>0?toll/(save/60):0;
    function hm(h){ const m=Math.round(h*60); return Math.floor(m/60)+'時間'+(m%60)+'分'; }
    $('sub').textContent=`距離${num(dist)}km・高速料金${num(toll)}円`;
    $('th').textContent=hm(th); $('tl').textContent=hm(tl); $('per').textContent=perHr>0?yen(perHr):'—';
    SHARE=`高速 vs 下道、高速だと約${num(save)}分の時短だった🛣️\\nその時短にかかる費用は1時間あたり${perHr>0?yen(perHr):'—'}。あなたなら？👇`;
    show(); anim($('big'),0,save,900);
  }'''))

SIMS.append(dict(id='shaken-tsumitate', cat=CAR, emoji='🔧',
  title='車の維持費 毎月積立シミュレーター｜車検・税金、毎月いくら貯めれば安心？｜シミュラボ',
  desc='車検・自動車税・任意保険・タイヤ等の費用から、毎月いくら積み立てておけば安心かを計算する無料シミュレーター。',
  ogtitle='車の維持費 毎月積立シミュレーター｜毎月いくら貯める？', ogdesc='車検・税金・保険・消耗品から、毎月の積立額を計算。',
  h1='車の維持費 毎月積立シミュレーター',
  lead='車検や税金は、まとめて来ると大きな出費。毎月いくら積み立てておけば慌てずに済むか、年間維持費から計算します。',
  inputs='''    <h2>🔧 維持費を入れる</h2>
    <div class="row"><div class="field"><label>車検費用 <span class="hint">（円・2年で）</span></label><input type="number" id="shaken" value="100000" min="0" inputmode="numeric"></div>
    <div class="field"><label>自動車税 <span class="hint">（円・年）</span></label><input type="number" id="tax" value="39500" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>任意保険 <span class="hint">（円・月）</span></label><input type="number" id="hoken" value="10000" min="0" inputmode="numeric"></div>
    <div class="field"><label>タイヤ・消耗品 <span class="hint">（円・年）</span></label><input type="number" id="other" value="20000" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">毎月の積立額を見る</button>''',
  result='''      <div class="label">毎月の積立目安</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">年間の維持費</div><div class="v accent" id="year">—</div></div>
      <div class="stat"><div class="k">車検の月割</div><div class="v" id="sh">—</div></div>
      <div class="stat"><div class="k">ガソリン除く総額</div><div class="v" id="note">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>毎月の積立 ＝ 車検÷24 ＋ 自動車税÷12 ＋ 任意保険 ＋ 消耗品÷12<br>※ガソリン代・駐車場代は別。</div>
    <p>車検や税金は「忘れたころに」やってきます。毎月コツコツ積み立てておけば、急な出費にも慌てません。ガソリン・駐車場は別途見込みましょう。</p>
    <h2>よくある質問</h2>'''+faq([('ローンは含まれますか？','いいえ。維持費のみです。ローン返済は別途加えてください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const shaken=Math.max(0,+$('shaken').value||0), tax=Math.max(0,+$('tax').value||0), hoken=Math.max(0,+$('hoken').value||0), other=Math.max(0,+$('other').value||0);
    const monthly=shaken/24+tax/12+hoken+other/12, year=monthly*12;
    $('sub').textContent=`車検${num(shaken)}/税${num(tax)}/保険${num(hoken)}月/消耗品${num(other)}`;
    $('year').textContent=yen(year); $('sh').textContent=yen(shaken/24); $('note').textContent=yen(year);
    SHARE=`車の維持費、毎月${yen(monthly)}積み立てれば安心という結果に🔧（年${yen(year)}・ガソリン別）\\n車ってお金かかる…！👇`;
    show(); anim($('big'),0,monthly,900);
  }'''))

SIMS.append(dict(id='souko-kyori', cat=CAR, emoji='🌍',
  title='生涯走行距離シミュレーター｜あなたの車、地球を何周する？｜シミュラボ',
  desc='年間走行距離と運転する年数から、一生で走る総距離を計算し、地球何周分・月何往復分かを可視化するエンタメシミュレーター。',
  ogtitle='生涯走行距離シミュレーター｜地球を何周する？', ogdesc='年間走行距離と年数から、生涯の走行距離を地球周回に換算。',
  h1='生涯走行距離シミュレーター',
  lead='あなたが一生のうちに車で走る距離は、どれくらい？年間走行距離と運転する年数から、生涯の総距離を地球何周分かで可視化します。',
  inputs='''    <h2>🌍 条件を入れる</h2>
    <div class="row"><div class="field"><label>年間走行距離 <span class="hint">（km）</span></label><input type="number" id="dist" value="8000" min="0" inputmode="numeric"></div>
    <div class="field"><label>運転する年数 <span class="hint">（年）</span></label><input type="number" id="years" value="40" min="1" max="80" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">生涯距離を見る</button>''',
  result='''      <div class="label">一生で走る距離</div>
      <div class="big"><span id="big">0</span><span class="unit">km</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">地球を</div><div class="v accent" id="earth">—</div></div>
      <div class="stat"><div class="k">月まで(38万km)</div><div class="v" id="moon">—</div></div>
      <div class="stat"><div class="k">東京〜大阪(往復1000km)</div><div class="v" id="osaka">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>生涯走行距離 ＝ 年間走行距離 × 運転する年数<br>地球1周＝約40,075km／地球〜月＝約38万km</div>
    <p>毎年8,000kmでも、40年で32万km。地球8周ぶんにもなります。それだけ走ってくれる愛車、たまにはメンテナンスでいたわってあげましょう。</p>
    <h2>よくある質問</h2>'''+faq([('1台での距離ですか？','運転する年数ぶんの合計距離です。買い替えても運転総距離としてお楽しみください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const dist=Math.max(0,+$('dist').value||0), years=Math.max(1,+$('years').value||1);
    const total=dist*years;
    $('sub').textContent=`年${num(dist)}km × ${years}年`;
    $('earth').textContent=(total/40075).toFixed(1)+'周'; $('moon').textContent=(total/384400).toFixed(2)+'回'; $('osaka').textContent=num(total/1000)+'往復';
    SHARE=`生涯走行距離シミュ、一生で約${num(total)}km走る計算でした🌍\\nなんと地球${(total/40075).toFixed(1)}周分！あなたは？👇`;
    show(); anim($('big'),0,total,900);
  }'''))

SIMS.append(dict(id='chuko-nedan', cat=CAR, emoji='📉',
  title='中古車 値落ちシミュレーター｜あなたの車、何年後にいくら？｜シミュラボ',
  desc='新車価格と年間の値落ち率から、数年後の予想下取り価格と値落ち総額を試算する無料シミュレーター。',
  ogtitle='中古車 値落ちシミュレーター｜何年後にいくら？', ogdesc='新車価格と値落ち率から、数年後の予想価格を試算。',
  h1='中古車 値落ちシミュレーター',
  lead='車は乗るほど価値が下がります。新車価格と値落ち率から、数年後にいくらになるか（下取り目安）を試算します。',
  inputs='''    <h2>📉 条件を入れる</h2>
    <div class="row"><div class="field"><label>新車価格 <span class="hint">（万円）</span></label><input type="number" id="new" value="250" min="0" inputmode="numeric"></div>
    <div class="field"><label>年間の値落ち率 <span class="hint">（％/年）</span></label><input type="number" id="rate" value="15" min="0" max="50" inputmode="numeric"></div></div>
    <div class="field"><label>何年後 <span class="hint">（年）</span></label><input type="number" id="years" value="5" min="1" max="20" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">予想価格を見る</button>''',
  result='''      <div class="label" id="lab">5年後の予想価格</div>
      <div class="big"><span id="big">0</span><span class="unit">万円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">値落ち総額</div><div class="v accent" id="loss">—</div></div>
      <div class="stat"><div class="k">残価率</div><div class="v" id="ratio">—</div></div>
      <div class="stat"><div class="k">1年あたり値落ち</div><div class="v" id="peryr">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>予想価格 ＝ 新車価格 ×（1 − 値落ち率）^年数</div>
    <p>新車は最初の数年でとくに値落ちが大きい傾向。人気車種・低走行・きれいな状態だと値落ちは緩やかになります。乗り換えを考えるなら下取り相場のチェックを。</p>
    <h2>よくある質問</h2>'''+faq([('車種で変わりますか？','はい。人気車種ほど値落ちが緩やかです。値落ち率を調整して試してください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const nw=Math.max(0,+$('new').value||0), rate=Math.max(0,Math.min(50,+$('rate').value||0))/100, years=Math.max(1,+$('years').value||1);
    const value=nw*Math.pow(1-rate,years), loss=nw-value, ratio=nw>0?value/nw*100:0;
    $('lab').textContent=`${years}年後の予想価格`;
    $('sub').textContent=`新車${num(nw)}万・値落ち${Math.round(rate*100)}%/年・${years}年後`;
    $('loss').textContent=num(loss)+'万円'; $('ratio').textContent=Math.round(ratio)+'%'; $('peryr').textContent=num(loss/years)+'万円';
    SHARE=`中古車の値落ちシミュ、新車${num(nw)}万円が${years}年後には約${num(value)}万円に📉（残価率${Math.round(ratio)}%）\\n車は資産価値も大事だ…👇`;
    show(); anim($('big'),0,value,900);
  }'''))

SIMS.append(dict(id='drive-yosan', cat=CAR, emoji='🚙',
  title='ドライブ費用シミュレーター｜日帰りドライブ、1人いくら？｜シミュラボ',
  desc='往復距離・燃費・ガソリン単価・高速料金・人数から、ドライブにかかる総額と1人あたりの費用を計算する無料シミュレーター。',
  ogtitle='ドライブ費用シミュレーター｜1人いくら？', ogdesc='距離・燃費・高速料金・人数から、ドライブ費用を割り勘計算。',
  h1='ドライブ費用シミュレーター',
  lead='みんなでドライブ、ガソリンと高速代で1人いくら？往復距離・燃費・高速料金・人数から、割り勘の金額を計算します。',
  inputs='''    <h2>🚙 条件を入れる</h2>
    <div class="row"><div class="field"><label>往復距離 <span class="hint">（km）</span></label><input type="number" id="dist" value="200" min="0" inputmode="numeric"></div>
    <div class="field"><label>燃費 <span class="hint">（km/L）</span></label><input type="number" id="nenpi" value="15" min="1" step="0.1" inputmode="decimal"></div></div>
    <div class="row"><div class="field"><label>ガソリン単価 <span class="hint">（円/L）</span></label><input type="number" id="price" value="175" min="0" inputmode="numeric"></div>
    <div class="field"><label>高速料金 <span class="hint">（円・往復）</span></label><input type="number" id="toll" value="4000" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>乗る人数 <span class="hint">（人）</span></label><input type="number" id="people" value="4" min="1" max="20" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">1人いくらか見る</button>''',
  result='''      <div class="label">1人あたりの費用</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">総額</div><div class="v accent" id="total">—</div></div>
      <div class="stat"><div class="k">ガソリン代</div><div class="v" id="gas">—</div></div>
      <div class="stat"><div class="k">高速代</div><div class="v" id="tollv">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>ガソリン代 ＝ 往復距離 ÷ 燃費 × ガソリン単価<br>総額 ＝ ガソリン代 ＋ 高速料金／1人あたり ＝ 総額 ÷ 人数</div>
    <p>大人数で乗るほど、1人あたりは割安に。運転してくれた人には、ガソリン代を多めに負担するなどの心づかいも◎。</p>
    <h2>よくある質問</h2>'''+faq([('駐車場代や食事は？','含まれません。ガソリンと高速のみの割り勘計算です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const dist=Math.max(0,+$('dist').value||0), nenpi=Math.max(0.1,+$('nenpi').value||0.1), price=Math.max(0,+$('price').value||0), toll=Math.max(0,+$('toll').value||0), people=Math.max(1,+$('people').value||1);
    const gas=dist/nenpi*price, total=gas+toll, per=total/people;
    $('sub').textContent=`往復${num(dist)}km・${people}人で割り勘`;
    $('total').textContent=yen(total); $('gas').textContent=yen(gas); $('tollv').textContent=yen(toll);
    SHARE=`ドライブ費用シミュ、${people}人で行くと1人あたり${yen(per)}でした🚙（総額${yen(total)}）\\n割り勘でお得！👇`;
    show(); anim($('big'),0,per,900);
  }'''))

SIMS.append(dict(id='tsukin-car', cat=CAR, emoji='🚉',
  title='車通勤 vs 電車通勤シミュレーター｜どっちが安い？｜シミュラボ',
  desc='片道距離・燃費・駐車場代と電車の定期代から、車通勤と電車通勤の月コストを比較する無料シミュレーター。',
  ogtitle='車通勤 vs 電車通勤｜どっちが安い？', ogdesc='ガソリン・駐車場と定期代を比べ、通勤コストを月単位で比較。',
  h1='車通勤 vs 電車通勤シミュレーター',
  lead='通勤、車と電車でどっちが安い？片道距離・燃費・駐車場代と、電車の定期代を比べて、月のコスト差を出します。',
  inputs='''    <h2>🚉 条件を入れる</h2>
    <div class="row"><div class="field"><label>片道距離 <span class="hint">（km）</span></label><input type="number" id="dist" value="15" min="0" inputmode="numeric"></div>
    <div class="field"><label>燃費 <span class="hint">（km/L）</span></label><input type="number" id="nenpi" value="15" min="1" step="0.1" inputmode="decimal"></div></div>
    <div class="row"><div class="field"><label>ガソリン単価 <span class="hint">（円/L）</span></label><input type="number" id="price" value="175" min="0" inputmode="numeric"></div>
    <div class="field"><label>月の出勤日数 <span class="hint">（日）</span></label><input type="number" id="days" value="20" min="0" max="31" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>駐車場代 <span class="hint">（円・月/会社+自宅）</span></label><input type="number" id="park" value="0" min="0" inputmode="numeric"></div>
    <div class="field"><label>電車の定期代 <span class="hint">（円・月）</span></label><input type="number" id="teiki" value="12000" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">どっちが安いか見る</button>''',
  result='''      <div class="label" id="lab">月の差額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">車通勤(月)</div><div class="v" id="car">—</div></div>
      <div class="stat"><div class="k">電車通勤(月)</div><div class="v" id="train">—</div></div>
      <div class="stat"><div class="k">年間の差</div><div class="v accent" id="year">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>車：往復ガソリン代 × 出勤日数 ＋ 駐車場代<br>電車：定期代（月）</div>
    <p>車通勤はガソリン以外にも、駐車場・保険・車検・税金がかかります（本ツールはガソリン＋駐車場で比較）。総合的には電車のほうが安いことも多いので、トータルで判断を。</p>
    <h2>よくある質問</h2>'''+faq([('車の維持費は含まれますか？','駐車場代のみ含みます。保険・車検・税金は別途考慮してください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const dist=Math.max(0,+$('dist').value||0), nenpi=Math.max(0.1,+$('nenpi').value||0.1), price=Math.max(0,+$('price').value||0), days=Math.max(0,+$('days').value||0), park=Math.max(0,+$('park').value||0), teiki=Math.max(0,+$('teiki').value||0);
    const carMonth=(dist*2/nenpi*price)*days+park, diff=teiki-carMonth;
    $('lab').textContent= diff>=0?'車通勤のほうが 月に安い額':'電車通勤のほうが 月に安い額';
    $('sub').textContent=`片道${num(dist)}km・${days}日/月`;
    $('car').textContent=yen(carMonth); $('train').textContent=yen(teiki); $('year').textContent=yen(Math.abs(diff)*12);
    SHARE= diff>=0?`車通勤 vs 電車通勤、車のほうが月${yen(Math.abs(diff))}お得だった🚉（年${yen(Math.abs(diff)*12)}）\\n※維持費別。あなたは？👇`:`通勤は電車のほうが月${yen(Math.abs(diff))}お得という結果に🚉\\nあなたは？👇`;
    show(); anim($('big'),0,Math.abs(diff),900);
  }'''))

SIMS.append(dict(id='kuruma-hoyuu', cat=CAR, emoji='🅿️',
  title='マイカー vs カーシェア損益分岐シミュレーター｜どっちがお得？｜シミュラボ',
  desc='マイカーの月額固定費とカーシェアの1回料金・利用頻度から、どちらがお得かの損益分岐を試算する無料シミュレーター。',
  ogtitle='マイカー vs カーシェア｜どっちがお得？', ogdesc='マイカーの固定費とカーシェア料金から損益分岐を試算。',
  h1='マイカー vs カーシェア損益分岐シミュレーター',
  lead='たまにしか乗らないなら、持たない選択も。マイカーの月固定費と、カーシェアの1回料金・利用回数から、どちらがお得かを出します。',
  inputs='''    <h2>🅿️ 条件を入れる</h2>
    <div class="field"><label>マイカーの月固定費 <span class="hint">（円・駐車場+保険+税+ローン等）</span></label><input type="number" id="own" value="40000" min="0" inputmode="numeric"></div>
    <div class="row"><div class="field"><label>カーシェア1回の料金 <span class="hint">（円）</span></label><input type="number" id="share" value="3000" min="0" inputmode="numeric"></div>
    <div class="field"><label>月の利用回数 <span class="hint">（回）</span></label><input type="number" id="freq" value="4" min="0" max="60" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">どっちがお得か見る</button>''',
  result='''      <div class="label" id="lab">あなたの場合のお得な選択</div>
      <div class="big" id="bigwrap"><span id="big">0</span><span class="unit">円/月 お得</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">マイカー(月)</div><div class="v" id="ownv">—</div></div>
      <div class="stat"><div class="k">カーシェア(月)</div><div class="v" id="sharev">—</div></div>
      <div class="stat"><div class="k">損益分岐の回数</div><div class="v accent" id="be">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>カーシェア月額 ＝ 1回料金 × 月の利用回数<br>損益分岐回数 ＝ マイカー月固定費 ÷ 1回料金<br>これより少ない利用ならカーシェアがお得。</div>
    <p>月に数回しか乗らないなら、カーシェアやレンタカーが割安になりがち。逆に毎日乗る・家族で使うならマイカーが有利。使い方しだいです。</p>
    <h2>よくある質問</h2>'''+faq([('ガソリン代は？','カーシェアは料金込みのことが多く、マイカーは別途かかります。本ツールは固定費ベースの簡易比較です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const own=Math.max(0,+$('own').value||0), share=Math.max(0,+$('share').value||0), freq=Math.max(0,+$('freq').value||0);
    const shareMonth=share*freq, diff=Math.abs(own-shareMonth), be=share>0?own/share:0;
    const ownerWins = own<=shareMonth;
    $('lab').textContent= ownerWins?'マイカーのほうがお得':'カーシェアのほうがお得';
    $('sub').textContent=`月${freq}回利用・1回${num(share)}円`;
    $('ownv').textContent=yen(own); $('sharev').textContent=yen(shareMonth); $('be').textContent=num(be)+'回/月';
    SHARE= ownerWins?`マイカー vs カーシェア、月${freq}回ならマイカーが${yen(diff)}お得🅿️（分岐点は月${num(be)}回）\\nあなたは？👇`:`月${freq}回の利用なら、カーシェアが${yen(diff)}お得だった🅿️（分岐点は月${num(be)}回）\\n持たない選択もアリ。👇`;
    show(); anim($('big'),0,diff,900);
  }'''))

if __name__=='__main__':
    write_all(SIMS)
    print(f'car done. {len(SIMS)} sims.')
