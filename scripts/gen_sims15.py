# -*- coding: utf-8 -*-
"""シミュラボ：住まい・暮らしカテゴリ 10本（gen_sims11のTPLを再利用）。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq, write_all

HOME='住まい・暮らし'
SIMS=[]

SIMS.append(dict(id='yachin-tekisei', cat=HOME, emoji='🏠',
  title='適正家賃シミュレーター｜手取りからいくらの家賃が無理ない？｜シミュラボ',
  desc='毎月の手取り収入から、無理のない家賃の上限・推奨額・余裕重視ラインを計算する無料シミュレーター。',
  ogtitle='適正家賃シミュレーター｜手取りで家賃いくらまで？', ogdesc='手取り月収から無理のない家賃の目安を計算。',
  h1='適正家賃シミュレーター',
  lead='家賃は固定費の主役。毎月の手取りから、無理のない家賃の上限・推奨ライン・余裕重視ラインを出します。引っ越し・部屋探しの目安に。',
  inputs='''    <h2>🏠 手取りを入れる</h2>
    <div class="field"><label>毎月の手取り収入 <span class="hint">（円・ボーナス除く）</span></label><input type="number" id="m" value="250000" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">適正家賃を見る</button>''',
  result='''      <div class="label">無理のない家賃の上限</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">推奨ライン(25%)</div><div class="v accent" id="rec">—</div></div>
      <div class="stat"><div class="k">余裕重視(20%)</div><div class="v" id="safe">—</div></div>
      <div class="stat"><div class="k">年間の家賃(上限)</div><div class="v" id="year">—</div></div></div>''',
  article='''    <h2>家賃の目安</h2>
    <div class="note"><strong>計算式</strong><br>上限 ＝ 手取り × 30%／推奨 ＝ 手取り × 25%／余裕重視 ＝ 手取り × 20%</div>
    <p>「家賃は手取りの3割まで」がよく言われる目安。貯金や趣味に余裕を持ちたいなら25%以下が安心です。管理費・共益費も家賃に含めて考えましょう。</p>
    <h2>よくある質問</h2>'''+faq([('管理費は含めますか？','はい。家賃＋管理費・共益費の合計でこの割合に収めるのがおすすめです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const m=Math.max(0,+$('m').value||0);
    const up=m*0.30, rec=m*0.25, safe=m*0.20;
    $('sub').textContent=`手取り月${num(m)}円の場合`;
    $('rec').textContent=yen(rec); $('safe').textContent=yen(safe); $('year').textContent=yen(up*12);
    SHARE=`適正家賃シミュ、手取り${num(m)}円なら家賃は${yen(rec)}くらいが無理ない目安でした🏠（上限${yen(up)}）\\nあなたは？👇`;
    show(); anim($('big'),0,up,900);
  }'''))

SIMS.append(dict(id='hikkoshi-hiyou', cat=HOME, emoji='🚚',
  title='引っ越し費用シミュレーター｜引っ越し、いくらかかる？｜シミュラボ',
  desc='荷物量・移動距離・時期から、引っ越し業者に支払う費用の目安を試算する無料シミュレーター。繁忙期と通常期の差も分かる。',
  ogtitle='引っ越し費用シミュレーター｜いくらかかる？', ogdesc='荷物量・距離・時期から引っ越し費用の目安を試算。',
  h1='引っ越し費用シミュレーター',
  lead='引っ越し、業者にいくら払う？荷物量・距離・時期から費用の目安を出します。3〜4月の繁忙期は高くなるので、その差も分かります。',
  inputs='''    <h2>🚚 条件を選ぶ</h2>
    <div class="field"><label>荷物の量</label><select id="load"><option value="35000">単身（荷物少なめ）</option><option value="50000" selected>単身（標準）</option><option value="80000">二人暮らし</option><option value="110000">家族（3〜4人）</option></select></div>
    <div class="field"><label>移動距離</label><select id="dist"><option value="1.0">同じ市区町村</option><option value="1.25" selected>同じ都道府県</option><option value="1.8">遠距離（県外）</option></select></div>
    <div class="field"><label>時期</label><select id="season"><option value="1.0">通常期（5〜2月）</option><option value="1.5">繁忙期（3〜4月）</option></select></div>
    <button class="btn btn-primary" id="calcBtn">費用の目安を見る</button>''',
  result='''      <div class="label">引っ越し費用の目安</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">通常期なら</div><div class="v accent" id="normal">—</div></div>
      <div class="stat"><div class="k">繁忙期なら</div><div class="v" id="busy">—</div></div>
      <div class="stat"><div class="k">荷物量</div><div class="v" id="loadv">—</div></div></div>''',
  article='''    <h2>計算の考え方</h2>
    <div class="note"><strong>計算式</strong><br>費用 ＝ 荷物量の基本料金 × 距離係数 × 時期係数</div>
    <p>3〜4月は引っ越しが集中して料金が1.5倍ほどに跳ね上がります。時期をずらせるなら通常期が断然お得。複数社の相見積もりでさらに下げられます。</p>
    <h2>よくある質問</h2>'''+faq([('エアコン工事や不用品処分は？','含まれていません。オプション費用は別途見込んでください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const load=+$('load').value||0, dist=+$('dist').value||1, season=+$('season').value||1;
    const base=load*dist, est=base*season, normal=base*1.0, busy=base*1.5;
    $('sub').textContent=`${sel('load').text}・${sel('dist').text}・${sel('season').text}`;
    $('normal').textContent=yen(normal); $('busy').textContent=yen(busy); $('loadv').textContent=sel('load').text;
    SHARE=`引っ越し費用シミュ、${sel('load').text}の${sel('dist').text}で約${yen(est)}でした🚚\\n繁忙期だと${yen(busy)}…時期えらび大事！👇`;
    show(); anim($('big'),0,est,900);
  }'''))

SIMS.append(dict(id='chintai-mochiie', cat=HOME, emoji='🔑',
  title='賃貸 vs 持ち家 生涯コストシミュレーター｜どっちが得？｜シミュラボ',
  desc='家賃・居住年数と、持ち家の購入価格・年間維持費から、賃貸と持ち家の生涯コストを比較する無料シミュレーター。',
  ogtitle='賃貸 vs 持ち家 生涯コスト｜どっちが得？', ogdesc='家賃と持ち家価格・維持費から生涯コストを比較。',
  h1='賃貸 vs 持ち家 生涯コストシミュレーター',
  lead='永遠のテーマ「賃貸か持ち家か」。家賃・住む年数と、持ち家の価格・維持費から、ざっくり生涯コストを比べます。',
  inputs='''    <h2>🔑 条件を入れる</h2>
    <div class="row"><div class="field"><label>家賃 <span class="hint">（円/月・管理費込み）</span></label><input type="number" id="rent" value="90000" min="0" inputmode="numeric"></div>
    <div class="field"><label>住む年数 <span class="hint">（年）</span></label><input type="number" id="years" value="50" min="1" max="80" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>持ち家の購入総額 <span class="hint">（万円・諸費用込み）</span></label><input type="number" id="price" value="4000" min="0" inputmode="numeric"></div>
    <div class="field"><label>持ち家の年間維持費 <span class="hint">（万円・税+修繕）</span></label><input type="number" id="maint" value="40" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">生涯コストを比べる</button>''',
  result='''      <div class="label" id="lab">差額</div>
      <div class="big"><span id="big">0</span><span class="unit">万円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">賃貸の生涯コスト</div><div class="v" id="chintai">—</div></div>
      <div class="stat"><div class="k">持ち家の生涯コスト</div><div class="v accent" id="mochiie">—</div></div>
      <div class="stat"><div class="k">住む年数</div><div class="v" id="yv">—</div></div></div>''',
  article='''    <h2>計算の考え方</h2>
    <div class="note"><strong>計算式</strong><br>賃貸 ＝ 家賃 × 12 × 年数 ＋ 更新料（2年に1ヶ月分）<br>持ち家 ＝ 購入総額 ＋ 年間維持費 × 年数</div>
    <p>これはあくまで支払い総額の概算。持ち家には資産として残る価値が、賃貸には住み替えの自由があります。金利・地価・ライフプランで答えは変わります。</p>
    <h2>よくある質問</h2>'''+faq([('住宅ローン金利は？','本ツールは購入総額ベースの概算で、金利は別途です。詳細はローンシミュレーターと併用を。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const rent=Math.max(0,+$('rent').value||0), years=Math.max(1,+$('years').value||1), price=Math.max(0,+$('price').value||0), maint=Math.max(0,+$('maint').value||0);
    const chintai=(rent*12*years + rent*Math.floor(years/2))/10000; // 万円
    const mochiie=price + maint*years;
    const diff=Math.abs(chintai-mochiie);
    $('lab').textContent= chintai<=mochiie?'賃貸のほうが安い差額':'持ち家のほうが安い差額';
    $('sub').textContent=`家賃${num(rent)}円・${years}年・持ち家${num(price)}万`;
    $('chintai').textContent=num(chintai)+'万円'; $('mochiie').textContent=num(mochiie)+'万円'; $('yv').textContent=years+'年';
    SHARE=`賃貸 vs 持ち家、${years}年住むと賃貸${num(chintai)}万・持ち家${num(mochiie)}万で${chintai<=mochiie?'賃貸':'持ち家'}が${num(diff)}万円お得という結果に🔑\\nあなたは？👇`;
    show(); anim($('big'),0,diff,900);
  }'''))

SIMS.append(dict(id='denki-setsuyaku', cat=HOME, emoji='💡',
  title='電気代 節約シミュレーター｜ちょっとの工夫で年いくら浮く？｜シミュラボ',
  desc='今の電気代と節約の取り組みから、1年・10年でどれだけ電気代を節約できるかを試算する無料シミュレーター。',
  ogtitle='電気代 節約シミュレーター｜年いくら浮く？', ogdesc='今の電気代と節約の取り組みから、年間の節約額を試算。',
  h1='電気代 節約シミュレーター',
  lead='エアコンの設定温度や待機電力の見直しで、電気代はどれだけ変わる？今の電気代と取り組み内容から、年間の節約額を出します。',
  inputs='''    <h2>💡 条件を入れる</h2>
    <div class="field"><label>今の電気代 <span class="hint">（円/月・平均）</span></label><input type="number" id="bill" value="10000" min="0" inputmode="numeric"></div>
    <div class="field"><label>取り組み</label><select id="action"><option value="0.05">かんたん（待機電力カット）</option><option value="0.10" selected>しっかり（エアコン適正温度＋待機電力）</option><option value="0.15">がんばる（家電見直し＋LED＋契約見直し）</option></select></div>
    <button class="btn btn-primary" id="calcBtn">節約額を見る</button>''',
  result='''      <div class="label">1年で節約できる電気代</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1ヶ月あたり</div><div class="v" id="m">—</div></div>
      <div class="stat"><div class="k">10年で</div><div class="v accent" id="y10">—</div></div>
      <div class="stat"><div class="k">削減率</div><div class="v" id="rate">—</div></div></div>''',
  article='''    <h2>計算の考え方</h2>
    <div class="note"><strong>計算式</strong><br>年間の節約 ＝ 今の電気代 × 12 × 削減率</div>
    <p>冷房は1度上げる・暖房は1度下げるだけで約10%の節約効果と言われます。待機電力カット、LED化、電力会社の契約見直しも合わせると効果大。固定費なので一度の見直しがずっと効きます。</p>
    <h2>よくある質問</h2>'''+faq([('必ずこの額が下がりますか？','使い方により変わる目安です。生活スタイルに合わせて取り組んでください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const bill=Math.max(0,+$('bill').value||0), rate=+$('action').value||0;
    const y=bill*12*rate;
    $('sub').textContent=`月${num(bill)}円・${sel('action').text}`;
    $('m').textContent=yen(y/12); $('y10').textContent=yen(y*10); $('rate').textContent=Math.round(rate*100)+'%';
    SHARE=`電気代の節約シミュ、${sel('action').text}で年${yen(y)}・10年で${yen(y*10)}も浮く計算でした💡\\nちょっとの工夫が効くなぁ。👇`;
    show(); anim($('big'),0,y,900);
  }'''))

SIMS.append(dict(id='hitorigurashi', cat=HOME, emoji='📦',
  title='ひとり暮らし初期費用シミュレーター｜引っ越しに最初いくら必要？｜シミュラボ',
  desc='家賃と家具・家電のグレードから、ひとり暮らしを始めるのに必要な初期費用（敷金・礼金・家具家電など）の総額を試算する無料シミュレーター。',
  ogtitle='ひとり暮らし初期費用シミュレーター｜最初いくら必要？', ogdesc='家賃と家具家電から、ひとり暮らしの初期費用を試算。',
  h1='ひとり暮らし初期費用シミュレーター',
  lead='ひとり暮らしのスタート、最初にいくら必要？家賃と家具・家電のグレードから、敷金礼金から家電までの初期費用をまとめて出します。',
  inputs='''    <h2>📦 条件を入れる</h2>
    <div class="field"><label>家賃 <span class="hint">（円/月）</span></label><input type="number" id="rent" value="70000" min="0" inputmode="numeric"></div>
    <div class="field"><label>家具・家電</label><select id="kaden"><option value="150000">最低限でそろえる</option><option value="300000" selected>標準的にそろえる</option><option value="500000">こだわってそろえる</option></select></div>
    <button class="btn btn-primary" id="calcBtn">初期費用を見る</button>''',
  result='''      <div class="label">ひとり暮らしの初期費用</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">賃貸契約の初期費用</div><div class="v accent" id="contract">—</div></div>
      <div class="stat"><div class="k">家具・家電</div><div class="v" id="kadenv">—</div></div>
      <div class="stat"><div class="k">引っ越し代の目安</div><div class="v" id="move">—</div></div></div>''',
  article='''    <h2>計算の考え方</h2>
    <div class="note"><strong>計算式</strong><br>賃貸契約の初期費用 ＝ 家賃 × 約5（敷金・礼金・前家賃・仲介手数料・保証料など）<br>総額 ＝ 契約初期費用 ＋ 家具家電 ＋ 引っ越し代</div>
    <p>家賃の約5ヶ月分が契約時にかかるのが一般的。敷金礼金ゼロ物件やフリーレントを使うと初期費用をぐっと抑えられます。家電はセット購入やリサイクルも手。</p>
    <h2>よくある質問</h2>'''+faq([('家賃の5倍は多すぎ？','敷礼ゼロ物件なら3倍程度に下がります。物件によって幅があります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const rent=Math.max(0,+$('rent').value||0), kaden=+$('kaden').value||0;
    const contract=rent*5, move=50000, total=contract+kaden+move;
    $('sub').textContent=`家賃${num(rent)}円・${sel('kaden').text}`;
    $('contract').textContent=yen(contract); $('kadenv').textContent=yen(kaden); $('move').textContent=yen(move);
    SHARE=`ひとり暮らしの初期費用シミュ、家賃${num(rent)}円スタートで総額約${yen(total)}でした📦\\n最初がいちばんお金かかる…！👇`;
    show(); anim($('big'),0,total,900);
  }'''))

SIMS.append(dict(id='kounetsu', cat=HOME, emoji='🧾',
  title='光熱費の平均シミュレーター｜うちの光熱費、高い？普通？｜シミュラボ',
  desc='世帯人数と季節から、電気・ガス・水道の光熱費の平均的な目安を表示し、自分の家計と比べられる無料シミュレーター。',
  ogtitle='光熱費の平均シミュレーター｜高い？普通？', ogdesc='世帯人数と季節から、光熱費の平均的な目安を表示。',
  h1='光熱費の平均シミュレーター',
  lead='うちの光熱費って高いの？普通なの？世帯人数と季節から、電気・ガス・水道を合わせた光熱費の平均的な目安を出します。',
  inputs='''    <h2>🧾 条件を選ぶ</h2>
    <div class="field"><label>世帯人数</label><select id="people"><option value="1">1人暮らし</option><option value="2" selected>2人</option><option value="3">3人</option><option value="4">4人以上</option></select></div>
    <div class="field"><label>季節</label><select id="season"><option value="1.0">春・秋</option><option value="1.1">夏</option><option value="1.3">冬</option></select></div>
    <button class="btn btn-primary" id="calcBtn">平均の目安を見る</button>''',
  result='''      <div class="label">光熱費の月平均（目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">年間</div><div class="v accent" id="year">—</div></div>
      <div class="stat"><div class="k">1人あたり</div><div class="v" id="per">—</div></div>
      <div class="stat"><div class="k">季節</div><div class="v" id="seasonv">—</div></div></div>''',
  article='''    <h2>光熱費の目安</h2>
    <div class="note"><strong>計算の考え方</strong><br>世帯人数別の電気・ガス・水道の平均月額（春秋基準）に、季節の係数を掛けています。<br>目安：1人約1.1万／2人約1.9万／3人約2.3万／4人約2.5万円（春秋）</div>
    <p>冬は暖房で1.3倍ほどに増えがち。自分の光熱費と比べて、平均より高ければ節約の余地ありです。電力・ガス会社の見直しも効果的。</p>
    <h2>よくある質問</h2>'''+faq([('地域差はありますか？','あります。寒冷地は冬の暖房費が高めです。あくまで全国平均の目安です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const base={1:11000,2:19000,3:23000,4:25000}[+$('people').value||1]||19000;
    const f=+$('season').value||1, people=+$('people').value||1;
    const m=base*f;
    $('sub').textContent=`${sel('people').text}・${sel('season').text}`;
    $('year').textContent=yen(m*12); $('per').textContent=yen(m/people); $('seasonv').textContent=sel('season').text;
    SHARE=`光熱費の平均シミュ、${sel('people').text}・${sel('season').text}だと月${yen(m)}が目安でした🧾\\nうちは高い？安い？👇`;
    show(); anim($('big'),0,m,900);
  }'''))

SIMS.append(dict(id='net-hikari', cat=HOME, emoji='📶',
  title='ネット代見直しシミュレーター｜乗り換えで生涯いくら浮く？｜シミュラボ',
  desc='今のインターネット料金と乗り換え後の料金から、年間・残りの人生でどれだけ通信費が浮くかを試算する無料シミュレーター。',
  ogtitle='ネット代見直しシミュレーター｜生涯いくら浮く？', ogdesc='今のネット料金と乗り換え後から、浮く通信費を試算。',
  h1='ネット代見直しシミュレーター',
  lead='自宅のネット代、見直してる？今の料金と乗り換え後の料金から、年間・残りの人生で浮く金額を出します。固定費だからこそ効きます。',
  inputs='''    <h2>📶 条件を入れる</h2>
    <div class="row"><div class="field"><label>今のネット代 <span class="hint">（円/月）</span></label><input type="number" id="now" value="6000" min="0" inputmode="numeric"></div>
    <div class="field"><label>乗り換え後 <span class="hint">（円/月）</span></label><input type="number" id="aft" value="4000" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>あと何年使う <span class="hint">（年）</span></label><input type="number" id="yr" value="20" min="1" max="80" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">浮く金額を見る</button>''',
  result='''      <div class="label" id="lab">残りの人生で 浮く通信費</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">月の差</div><div class="v" id="md">—</div></div>
      <div class="stat"><div class="k">1年で</div><div class="v accent" id="y1">—</div></div>
      <div class="stat"><div class="k">10年で</div><div class="v" id="y10">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>浮く金額 ＝（今の料金 − 乗り換え後）× 12 × 年数</div>
    <p>光回線やプロバイダは、キャンペーン・セット割で意外と下げられます。スマホとのセット割を使えばさらにお得に。固定費は一度見直せばずっと効きます。</p>
    <h2>よくある質問</h2>'''+faq([('工事費や違約金は？','本ツールは月額差のみの概算です。乗り換え時の費用は別途ご確認を。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const now=Math.max(0,+$('now').value||0), aft=Math.max(0,+$('aft').value||0), yr=Math.max(1,+$('yr').value||1);
    const md=now-aft, total=md*12*yr;
    $('lab').textContent= total>=0?'残りの人生で 浮く通信費':'残りの人生で 増える通信費';
    $('sub').textContent=`月${num(now)}円 → ${num(aft)}円・${yr}年`;
    $('md').textContent=num(Math.abs(md))+'円'; $('y1').textContent=yen(Math.abs(md)*12); $('y10').textContent=yen(Math.abs(md)*12*10);
    SHARE= md>=0?`ネット代を見直すと、残り${yr}年で約${yen(Math.abs(total))}も浮く計算だった📶\\n固定費の見直し、効くなぁ。👇`:`今の案だと逆に${yen(Math.abs(total))}増える計算…📶要検討👇`;
    show(); anim($('big'),0,Math.abs(total),900);
  }'''))

SIMS.append(dict(id='kaji-jikan', cat=HOME, emoji='🧹',
  title='家事の生涯時間シミュレーター｜一生で家事に何日使ってる？｜シミュラボ',
  desc='1日の家事時間から、1年・一生で家事に費やす時間を計算し、何日分・映画何本分かを可視化するエンタメシミュレーター。',
  ogtitle='家事の生涯時間シミュレーター｜一生で何日？', ogdesc='1日の家事時間から、一生で家事に費やす時間を可視化。',
  h1='家事の生涯時間シミュレーター',
  lead='毎日の料理・掃除・洗濯。積み重ねると、一生でどれだけの時間に？1日の家事時間から、生涯の総時間を可視化します。時短家電を考えるきっかけに。',
  inputs='''    <h2>🧹 条件を入れる</h2>
    <div class="row"><div class="field"><label>1日の家事時間 <span class="hint">（時間）</span></label><input type="number" id="hpd" value="2" min="0" max="16" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>これからの年数 <span class="hint">（年）</span></label><input type="number" id="years" value="50" min="1" max="80" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">生涯の家事時間を見る</button>''',
  result='''      <div class="label">一生で家事に使う時間</div>
      <div class="big"><span id="big">0</span><span class="unit">日分</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">合計時間</div><div class="v accent" id="hours">—</div></div>
      <div class="stat"><div class="k">1年で</div><div class="v" id="year">—</div></div>
      <div class="stat"><div class="k">映画(2時間)にすると</div><div class="v" id="movie">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>生涯の家事時間 ＝ 1日の家事時間 × 365 × 年数</div>
    <p>1日2時間でも、50年で約3.8万時間＝1500日以上。食洗機・乾燥機・ロボット掃除機などの時短家電は「お金で時間を買う」投資ともいえます。</p>
    <h2>よくある質問</h2>'''+faq([('家事の時短は本当に効く？','毎日の積み重ねなので、少しの短縮でも生涯では大きな差になります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const h=Math.max(0,+$('hpd').value||0), years=Math.max(1,+$('years').value||1);
    const hours=h*365*years, days=hours/24;
    $('sub').textContent=`1日${h}時間 × 365日 × ${years}年`;
    $('hours').textContent=num(hours)+'時間'; $('year').textContent=num(h*365)+'時間'; $('movie').textContent=num(hours/2)+'本';
    SHARE=`家事の生涯時間シミュ、一生で約${num(days)}日分も家事してた🧹（${num(hours)}時間）\\n時短家電、ほしくなる…！👇`;
    show(); anim($('big'),0,days,900);
  }'''))

SIMS.append(dict(id='kagu-tsumitate', cat=HOME, emoji='🛋️',
  title='家具・家電 買い替え積立シミュレーター｜毎月いくら貯めれば慌てない？｜シミュラボ',
  desc='家電一式の購入額と平均寿命から、買い替えに備えて毎月いくら積み立てておけばよいかを計算する無料シミュレーター。',
  ogtitle='家具・家電 買い替え積立シミュレーター｜毎月いくら？', ogdesc='家電の購入額と寿命から、買い替え積立額を計算。',
  h1='家具・家電 買い替え積立シミュレーター',
  lead='冷蔵庫も洗濯機も、いつかは壊れる。家電一式の金額と寿命から、買い替えに備えて毎月いくら貯めておけば慌てないかを計算します。',
  inputs='''    <h2>🛋️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>家具・家電 一式の金額 <span class="hint">（万円）</span></label><input type="number" id="price" value="40" min="0" inputmode="numeric"></div>
    <div class="field"><label>平均の寿命 <span class="hint">（年）</span></label><input type="number" id="life" value="10" min="1" max="30" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">毎月の積立額を見る</button>''',
  result='''      <div class="label">毎月の積立目安</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">年間で</div><div class="v accent" id="year">—</div></div>
      <div class="stat"><div class="k">買い替え総額</div><div class="v" id="total">—</div></div>
      <div class="stat"><div class="k">寿命</div><div class="v" id="lifev">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>毎月の積立 ＝ 家電一式の金額 ÷（寿命 × 12ヶ月）</div>
    <p>家電は寿命がバラバラで、ある年にまとめて壊れると痛い出費に。あらかじめ「家電積立」をしておくと、買い替えのときも慌てません。</p>
    <h2>よくある質問</h2>'''+faq([('どの家電を含める？','冷蔵庫・洗濯機・エアコン・テレビ・電子レンジなど、主要な家電の合計でOKです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const price=Math.max(0,+$('price').value||0)*10000, life=Math.max(1,+$('life').value||1);
    const monthly=price/(life*12);
    $('sub').textContent=`${num(price/10000)}万円 ÷（${life}年 × 12ヶ月）`;
    $('year').textContent=yen(monthly*12); $('total').textContent=yen(price); $('lifev').textContent=life+'年';
    SHARE=`家電の買い替え積立シミュ、毎月${yen(monthly)}貯めれば慌てない計算でした🛋️（${life}年で${yen(price)}）\\n備えあれば憂いなし。👇`;
    show(); anim($('big'),0,monthly,900);
  }'''))

SIMS.append(dict(id='tatami-henkan', cat=HOME, emoji='📐',
  title='部屋の広さ換算シミュレーター｜畳・㎡・坪と坪単価｜シミュラボ',
  desc='部屋の畳数を平米（㎡）・坪に換算し、家賃を入れると坪単価・㎡単価も分かる無料シミュレーター。物件比較に便利。',
  ogtitle='部屋の広さ換算シミュレーター｜畳・㎡・坪', ogdesc='畳数を㎡・坪に換算し、家賃から坪単価も計算。',
  h1='部屋の広さ換算シミュレーター',
  lead='「8畳って何㎡？」を一発で。畳数を平米・坪に換算し、家賃を入れると坪単価・㎡単価も出ます。物件を比べるときの物差しに。',
  inputs='''    <h2>📐 条件を入れる</h2>
    <div class="row"><div class="field"><label>部屋の広さ <span class="hint">（畳）</span></label><input type="number" id="jou" value="8" min="0" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>家賃 <span class="hint">（円/月・坪単価の計算用）</span></label><input type="number" id="rent" value="80000" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">換算する</button>''',
  result='''      <div class="label">平米（㎡）に換算すると</div>
      <div class="big"><span id="big">0</span><span class="unit">㎡</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">坪</div><div class="v accent" id="tsubo">—</div></div>
      <div class="stat"><div class="k">㎡あたり家賃</div><div class="v" id="perm2">—</div></div>
      <div class="stat"><div class="k">坪単価</div><div class="v" id="pertsubo">—</div></div></div>''',
  article='''    <h2>換算の基準</h2>
    <div class="note"><strong>計算式</strong><br>㎡ ＝ 畳数 × 1.62（中京間の目安）<br>坪 ＝ ㎡ ÷ 3.305</div>
    <p>畳のサイズは地域で少し異なります（本ツールは1畳＝1.62㎡で計算）。坪単価が分かると、広さの割に高い・安いが比べやすくなります。</p>
    <h2>よくある質問</h2>'''+faq([('畳のサイズは地域で違う？','はい。京間・江戸間などで差があります。本ツールは1.62㎡で統一しています。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const jou=Math.max(0,+$('jou').value||0), rent=Math.max(0,+$('rent').value||0);
    const m2=jou*1.62, tsubo=m2/3.305;
    $('sub').textContent=`${jou}畳 ＝ 約${m2.toFixed(1)}㎡`;
    $('tsubo').textContent=tsubo.toFixed(1)+'坪'; $('perm2').textContent= m2>0?yen(rent/m2):'—'; $('pertsubo').textContent= tsubo>0?yen(rent/tsubo):'—';
    SHARE=`部屋の広さ換算、${jou}畳は約${m2.toFixed(1)}㎡（${tsubo.toFixed(1)}坪）でした📐\\n坪単価は${tsubo>0?yen(rent/tsubo):'—'}。あなたの部屋は？👇`;
    show(); anim($('big'),0,m2,900,1);
  }'''))

if __name__=='__main__':
    write_all(SIMS)
    print(f'home done. {len(SIMS)} sims.')
