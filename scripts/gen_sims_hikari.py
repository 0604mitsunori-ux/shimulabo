# -*- coding: utf-8 -*-
"""シミュラボ：光熱費・節約 10本（新カテゴリ slug=hikari）。電気代/ガソリン代/水道代など常時検索される計算ツール群。
gen_sims_tool TPL流用（try無し）。CTAなし。

seo_internal.py / gen_images.py のauto-importに 'gen_sims_hikari' を追加して使う。
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq
from gen_sims_tool import TPL, viz
from sim_quiz import make_engines
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CAT = '光熱費・節約'
SIMS = []
tally_quiz, num_quiz, band_quiz, add, q_article, render = make_engines(SIMS, CAT, TPL, viz)

ANIM = r'''  function anim(v){const el=$('big'),t0=performance.now();(function s(n){const p=Math.min(1,(n-t0)/800),e=1-Math.pow(1-p,3);el.textContent=Math.round(v*e).toLocaleString('ja-JP');if(p<1)requestAnimationFrame(s);})(performance.now());}'''
NOTE = '※電気料金の単価は契約・地域・時期で変わります。標準的な目安として31円/kWh前後で計算しています。'

# ============================================================
# 1. ガソリン代計算（ガソリン代 計算 22000/KD0/TP33000）★★
# ============================================================
add(id='gasolinedai', emoji='⛽',
  title='ガソリン代計算機｜走行距離・燃費からガソリン代を計算｜シミュラボ',
  desc='走行距離・燃費（km/L）・ガソリン単価を入れるだけで、ガソリン代を自動計算する無料ツール。片道・往復の費用や、1kmあたりの単価も分かります。',
  ogtitle='ガソリン代計算機｜走行距離・燃費から計算', ogdesc='距離・燃費・単価からガソリン代を自動計算。往復・1kmあたりも。',
  h1='ガソリン代計算機',
  lead='ドライブや通勤のガソリン代はいくら?走行距離・燃費・ガソリン単価を入れるだけで、片道・往復の費用を自動計算します。',
  inputs='''    <h2>⛽ 条件を入れる</h2>
    <div class="row"><div class="field"><label>走行距離（片道）<span class="hint">km</span></label><input type="number" id="dist" value="100" min="0" inputmode="decimal"></div>
    <div class="field"><label>燃費 <span class="hint">km/L</span></label><input type="number" id="nenpi" value="15" min="0.1" inputmode="decimal"></div></div>
    <div class="field"><label>ガソリン単価 <span class="hint">円/L</span></label><input type="number" id="tanka" value="175" min="0" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">ガソリン代を計算</button>''',
  result='''      <div class="label">ガソリン代（片道）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">往復</div><div class="v accent" id="round">—</div></div>
      <div class="stat"><div class="k">使用ガソリン量</div><div class="v" id="liter">—</div></div>
      <div class="stat"><div class="k">1kmあたり</div><div class="v" id="perkm">—</div></div></div>''',
  article='''    <div class="note"><strong>計算式</strong><br>ガソリン代 ＝ 走行距離 ÷ 燃費 × ガソリン単価</div>
    <h2>ガソリン代の計算方法</h2>
    <p>ガソリン代は「走行距離 ÷ 燃費 × 1Lあたりの単価」で求められます。たとえば100kmを燃費15km/L・単価175円で走ると、約1,167円。燃費がいい車ほど、また単価が安いほどガソリン代は下がります。長距離ドライブや通勤の費用、ガソリン代の割り勘の計算にも使えます。</p>
    <h2>よくある質問</h2>'''+faq([
      ('燃費がわからない','カタログ燃費（WLTCモード等）や、満タン法（給油量÷走行距離）で求められます。'),
      ('ガソリン単価の目安は？','レギュラーで概ね160〜185円/L前後。最新の店頭価格を入れると正確です。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const d=Math.max(0,+$('dist').value||0),n=Math.max(0.1,+$('nenpi').value||0.1),t=Math.max(0,+$('tanka').value||0);
    const liter=d/n, cost=liter*t, perkm=t/n;
    $('sub').textContent=`${num(d)}km ÷ ${num(n)}km/L × ${num(t)}円`;
    $('round').textContent=yen(cost*2);$('liter').textContent=num(liter)+'L';$('perkm').textContent=yen(perkm)+'/km';
    SHARE=`ガソリン代計算機、片道${num(d)}kmで約${yen(cost)}（往復${yen(cost*2)}）でした⛽`;show();anim(cost);}
'''+ANIM)

# ============================================================
# 2. エアコンの電気代（エアコン 電気代 18000/KD1/TP38000）★★
# ============================================================
add(id='aircon-denki', emoji='❄️',
  title='エアコンの電気代計算｜畳数・使用時間から1日・1ヶ月いくら？｜シミュラボ',
  desc='エアコンの畳数・1日の使用時間・日数から、電気代の目安を自動計算する無料ツール。つけっぱなしの月額や、冷房・暖房の電気代の目安が分かります。',
  ogtitle='エアコンの電気代計算｜1日・1ヶ月いくら？', ogdesc='畳数・使用時間からエアコンの電気代の目安を自動計算。',
  h1='エアコンの電気代計算機',
  lead='エアコンの電気代って実際いくら?畳数・1日の使用時間・日数を選ぶだけで、電気代の目安を計算します。つけっぱなしの月額もチェック。',
  inputs='''    <h2>❄️ 条件を入れる</h2>
    <div class="field"><label>エアコンの畳数の目安</label><select id="tatami">
      <option value="500">6畳用（冷房 約500W）</option><option value="600" selected>8〜10畳用（約600W）</option>
      <option value="800">12〜14畳用（約800W）</option><option value="1100">18〜20畳用（約1100W）</option></select></div>
    <div class="row"><div class="field"><label>1日の使用時間 <span class="hint">時間</span></label><input type="number" id="hours" value="8" min="0" inputmode="decimal"></div>
    <div class="field"><label>使う日数 <span class="hint">日</span></label><input type="number" id="days" value="30" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>電気料金の単価 <span class="hint">円/kWh</span></label><input type="number" id="tanka" value="31" min="0" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">電気代を計算</button>''',
  result='''      <div class="label">エアコンの電気代（期間合計）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1時間あたり</div><div class="v" id="hour">—</div></div>
      <div class="stat"><div class="k">1日あたり</div><div class="v" id="day">—</div></div>
      <div class="stat"><div class="k">消費電力の目安</div><div class="v accent" id="watt">—</div></div></div>''',
  article='''    <div class="note"><strong>計算式</strong><br>電気代 ＝ 消費電力(kW) × 使用時間 × 日数 × 単価（円/kWh）</div>
    <h2>エアコンの電気代の目安</h2>
    <p>エアコンの電気代は「消費電力(kW)×時間×単価」で計算します。実際の消費電力は設定温度・外気温・運転状況で変わり、立ち上がり時は大きく、安定すると下がります。本ツールは畳数ごとの平均的な消費電力で概算しています。こまめなフィルター掃除や、設定温度を控えめにする、つけっぱなしと小まめなオンオフの使い分けなどで節電できます。'''+NOTE+'''</p>
    <h2>よくある質問</h2>'''+faq([
      ('つけっぱなしは高い？','短時間の外出ならつけっぱなしの方が安いことも。長時間の不在は消すのが基本です。'),
      ('暖房の方が高い？','一般に外気温との差が大きい暖房の方が電気代は高くなりがちです。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const w=+sel('tatami').value||600,h=Math.max(0,+$('hours').value||0),d=Math.max(0,+$('days').value||0),t=Math.max(0,+$('tanka').value||0);
    const kwh=w/1000, perH=kwh*t, perD=perH*h, total=perD*d;
    $('sub').textContent=`${sel('tatami').text.split('（')[0]}・1日${num(h)}h × ${num(d)}日`;
    $('hour').textContent=yen(perH);$('day').textContent=yen(perD);$('watt').textContent=num(w)+'W';
    SHARE=`エアコンの電気代計算、${num(d)}日でおよそ${yen(total)}（1日${yen(perD)}）でした❄️`;show();anim(total);}
'''+ANIM)

# ============================================================
# 3. 電気代計算機（電気代 計算 6200/KD2）
# ============================================================
add(id='denkidai-keisan', emoji='💡',
  title='電気代計算機｜消費電力(W)と時間から電気代を計算｜シミュラボ',
  desc='消費電力(W)・使用時間・日数・電気単価から、電気代を自動計算する無料ツール。家電の電気代やワット数からの目安計算に使えます。',
  ogtitle='電気代計算機｜W・時間から電気代を計算', ogdesc='消費電力・使用時間・単価から電気代を自動計算。',
  h1='電気代計算機',
  lead='この家電の電気代はいくら?消費電力(W)・使用時間・日数・電気単価を入れるだけで、電気代を計算します。',
  inputs='''    <h2>💡 条件を入れる</h2>
    <div class="row"><div class="field"><label>消費電力 <span class="hint">W（ワット）</span></label><input type="number" id="watt" value="1000" min="0" inputmode="decimal"></div>
    <div class="field"><label>電気料金の単価 <span class="hint">円/kWh</span></label><input type="number" id="tanka" value="31" min="0" inputmode="decimal"></div></div>
    <div class="row"><div class="field"><label>1日の使用時間 <span class="hint">時間</span></label><input type="number" id="hours" value="3" min="0" inputmode="decimal"></div>
    <div class="field"><label>使う日数 <span class="hint">日</span></label><input type="number" id="days" value="30" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">電気代を計算</button>''',
  result='''      <div class="label">電気代（期間合計）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1時間あたり</div><div class="v" id="hour">—</div></div>
      <div class="stat"><div class="k">1日あたり</div><div class="v" id="day">—</div></div>
      <div class="stat"><div class="k">消費電力量</div><div class="v accent" id="kwh">—</div></div></div>''',
  article='''    <div class="note"><strong>計算式</strong><br>電気代 ＝ 消費電力(W) ÷ 1000 × 使用時間 × 日数 × 単価（円/kWh）</div>
    <h2>電気代の計算方法</h2>
    <p>電気代は「消費電力(kW)×使用時間×単価」で求められます。W（ワット）は家電の本体やラベルに記載。1kWh（キロワットアワー）あたりの単価は、契約プランで概ね27〜35円ほどです。複数の家電の電気代を比べて、節電の優先順位を考えるのに役立ちます。'''+NOTE+'''</p>
    <h2>よくある質問</h2>'''+faq([
      ('W数はどこを見る？','家電の本体ラベルや取扱説明書の「消費電力」を確認してください。'),
      ('単価の目安は？','契約により異なりますが、目安は1kWhあたり27〜35円ほどです。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const w=Math.max(0,+$('watt').value||0),t=Math.max(0,+$('tanka').value||0),h=Math.max(0,+$('hours').value||0),d=Math.max(0,+$('days').value||0);
    const kwh=w/1000, perH=kwh*t, perD=perH*h, total=perD*d;
    $('sub').textContent=`${num(w)}W・1日${num(h)}h × ${num(d)}日`;
    $('hour').textContent=yen(perH);$('day').textContent=yen(perD);$('kwh').textContent=num(kwh*h*d)+'kWh';
    SHARE=`電気代計算機、${num(w)}Wを${num(d)}日使うと約${yen(total)}でした💡`;show();anim(total);}
'''+ANIM)

# ============================================================
# 4. 家電別 電気代早見（kaden）
# ============================================================
add(id='kaden-denki', emoji='🔌',
  title='家電別 電気代早見シミュレーター｜冷蔵庫・ドライヤー等の電気代｜シミュラボ',
  desc='冷蔵庫・電子レンジ・ドライヤー・こたつ・テレビなど、家電を選んで使用時間を入れるだけで電気代の目安が分かる無料ツール。節電の参考に。',
  ogtitle='家電別 電気代早見｜冷蔵庫・ドライヤー等', ogdesc='家電を選んで電気代の目安を計算。節電の参考に。',
  h1='家電別 電気代早見シミュレーター',
  lead='どの家電が電気を食う?家電を選んで使用時間を入れるだけで、電気代の目安を表示します。節電の優先順位づけに。',
  inputs='''    <h2>🔌 家電を選ぶ</h2>
    <div class="field"><label>家電</label><select id="kaden">
      <option value="1100">ドライヤー（約1200W）</option><option value="1300">電子レンジ（約1300W）</option>
      <option value="500">こたつ（強 約500W）</option><option value="600">ホットカーペット（約600W）</option>
      <option value="1200">電気ストーブ（約1200W）</option><option value="40">液晶テレビ（約40W）</option>
      <option value="200">冷蔵庫（平均 約200W相当）</option><option value="660">炊飯器（炊飯時 約660W）</option>
      <option value="1200">ドラム式乾燥（約1200W）</option><option value="40">扇風機（約40W）</option></select></div>
    <div class="row"><div class="field"><label>1日の使用時間 <span class="hint">時間</span></label><input type="number" id="hours" value="1" min="0" inputmode="decimal"></div>
    <div class="field"><label>使う日数 <span class="hint">日</span></label><input type="number" id="days" value="30" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>電気単価 <span class="hint">円/kWh</span></label><input type="number" id="tanka" value="31" min="0" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">電気代を見る</button>''',
  result='''      <div class="label">電気代（期間合計）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1時間あたり</div><div class="v" id="hour">—</div></div>
      <div class="stat"><div class="k">1日あたり</div><div class="v accent" id="day">—</div></div>
      <div class="stat"><div class="k">消費電力</div><div class="v" id="watt">—</div></div></div>''',
  article='''    <div class="note"><strong>目安について</strong><br>消費電力は製品により幅があります。冷蔵庫は常時運転のため平均的な消費電力で概算しています。</div>
    <h2>家電別の電気代を比べると</h2>
    <p>電気代は「消費電力×使用時間」で決まります。ドライヤーや電子レンジ、電気ストーブなど<b>熱を作る家電は消費電力が大きい</b>のが特徴。一方、扇風機やテレビは小さめです。冷蔵庫は1台の消費電力は小さくても24時間動くため、年間では大きな割合に。古い家電は省エネモデルへの買い替えで電気代を抑えられることもあります。'''+NOTE+'''</p>
    <h2>よくある質問</h2>'''+faq([
      ('いちばん電気代が高い家電は？','熱を作る家電（ドライヤー・電気ストーブ・乾燥機など）は消費電力が大きい傾向です。'),
      ('冷蔵庫の電気代は？','1台あたりは小さくても24時間運転のため、年間では家庭の電力の大きな割合を占めます。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const w=+sel('kaden').value||0,h=Math.max(0,+$('hours').value||0),d=Math.max(0,+$('days').value||0),t=Math.max(0,+$('tanka').value||0);
    const kwh=w/1000, perH=kwh*t, perD=perH*h, total=perD*d;
    $('sub').textContent=`${sel('kaden').text.split('（')[0]}・1日${num(h)}h × ${num(d)}日`;
    $('hour').textContent=yen(perH);$('day').textContent=yen(perD);$('watt').textContent=num(w)+'W';
    SHARE=`家電別 電気代早見、${sel('kaden').text.split('（')[0]}を${num(d)}日使うと約${yen(total)}でした🔌`;show();anim(total);}
'''+ANIM)

# ============================================================
# 5. 水道代の目安（水道代 平均 6300/KD0）
# ============================================================
add(id='suidoudai', emoji='🚰',
  title='水道代の平均・目安シミュレーター｜世帯人数別に月いくら？｜シミュラボ',
  desc='世帯人数から、水道代の全国平均の目安を表示する無料ツール。使用量(m³)からの料金概算もでき、わが家の水道代が高いか安いかの判断に使えます。',
  ogtitle='水道代の平均・目安｜世帯人数別に月いくら？', ogdesc='世帯人数から水道代の平均目安を表示。使用量からの概算も。',
  h1='水道代の平均・目安シミュレーター',
  lead='うちの水道代って高い?安い?世帯人数を選ぶと、水道代の全国平均の目安を表示します。使用量からの概算もできます。',
  inputs='''    <h2>🚰 条件を選ぶ</h2>
    <div class="field"><label>世帯人数</label><select id="ninzu">
      <option value="1">1人暮らし</option><option value="2" selected>2人世帯</option><option value="3">3人世帯</option>
      <option value="4">4人世帯</option><option value="5">5人以上</option></select></div>
    <div class="field"><label>1ヶ月の使用量 <span class="hint">m³（分かれば）</span></label><input type="number" id="m3" value="0" min="0" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">水道代の目安を見る</button>''',
  result='''      <div class="label">水道代の月額目安（平均）</div>
      <div class="big"><span id="big">0</span><span class="unit">円/月</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">2ヶ月分（検針）</div><div class="v" id="two">—</div></div>
      <div class="stat"><div class="k">年額の目安</div><div class="v accent" id="year">—</div></div>
      <div class="stat"><div class="k">使用量からの概算</div><div class="v" id="byuse">—</div></div></div>''',
  article='''    <div class="note"><strong>目安について</strong><br>水道料金は自治体ごとに大きく異なります。本ツールは全国的な平均をもとにした概算です。</div>
    <h2>水道代の平均はどれくらい？</h2>
    <p>水道代は世帯人数が増えるほど高くなります。一般的な目安は、1人暮らしで月2,000〜2,500円ほど、2人世帯で約3,500〜4,000円、4人世帯で約6,000円前後（上下水道込み・地域差大）。多くの自治体は2ヶ月に1回の検針・請求です。お風呂の使い方やトイレ・洗濯の節水で、水道代を抑えられます。</p>
    <h2>よくある質問</h2>'''+faq([
      ('なぜ地域で差がある？','水源・設備・人口密度などで原価が異なるため、自治体ごとに料金が違います。'),
      ('節水のコツは？','お風呂の残り湯の活用、シャワー時間の短縮、節水コマなどが効果的です。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const n=+sel('ninzu').value||1,m3=Math.max(0,+$('m3').value||0);
    const avg=[0,2200,3700,4900,6000,7200][n];
    $('sub').textContent=sel('ninzu').text+'の全国平均の目安';
    $('two').textContent=yen(avg*2);$('year').textContent=yen(avg*12);
    // 概算：基本料金1100円 + 従量160円/m3（上下水道ざっくり）
    $('byuse').textContent = m3>0 ? yen(1100+m3*160)+'/月' : '使用量を入れると表示';
    SHARE=`水道代の目安、${sel('ninzu').text}でおよそ月${yen(avg)}でした🚰`;show();anim(avg);}
'''+ANIM)

# ============================================================
# 6. ガス代の目安（gas）
# ============================================================
add(id='gasudai', emoji='🔥',
  title='ガス代の平均・目安シミュレーター｜世帯人数・都市ガス/プロパン｜シミュラボ',
  desc='世帯人数と、都市ガス・プロパンガスの別から、ガス代の平均の目安を表示する無料ツール。わが家のガス代が高いか安いかの判断に。',
  ogtitle='ガス代の平均・目安｜世帯人数・都市/プロパン', ogdesc='世帯人数とガス種別からガス代の平均目安を表示。',
  h1='ガス代の平均・目安シミュレーター',
  lead='ガス代って平均いくら?世帯人数と、都市ガス・プロパン（LP）ガスの別を選ぶと、ガス代の目安を表示します。',
  inputs='''    <h2>🔥 条件を選ぶ</h2>
    <div class="field"><label>世帯人数</label><select id="ninzu">
      <option value="1">1人暮らし</option><option value="2" selected>2人世帯</option><option value="3">3人世帯</option>
      <option value="4">4人世帯</option><option value="5">5人以上</option></select></div>
    <div class="field"><label>ガスの種類</label><select id="type"><option value="1" selected>都市ガス</option><option value="1.7">プロパン（LP）ガス</option></select></div>
    <button class="btn btn-primary" id="calcBtn">ガス代の目安を見る</button>''',
  result='''      <div class="label">ガス代の月額目安（平均）</div>
      <div class="big"><span id="big">0</span><span class="unit">円/月</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">冬場（割高期）の目安</div><div class="v accent" id="winter">—</div></div>
      <div class="stat"><div class="k">年額の目安</div><div class="v" id="year">—</div></div></div>''',
  article='''    <div class="note"><strong>目安について</strong><br>ガス代は地域・会社・使用状況で大きく変わります。本ツールは平均的な目安での概算です。</div>
    <h2>ガス代の平均はどれくらい？</h2>
    <p>ガス代は世帯人数や季節で変わり、お湯を多く使う<b>冬場は高く</b>なります。一般に都市ガスよりプロパン（LP）ガスの方が単価が高い傾向です。目安は1人暮らしで月3,000円前後、4人世帯で5,000〜6,000円ほど（都市ガス・上下するため概算）。シャワー時間の短縮や追い焚きを減らすなどで節約できます。プロパンは会社により料金差が大きいため、見直しで下がることもあります。</p>
    <h2>よくある質問</h2>'''+faq([
      ('都市ガスとプロパンの違いは？','供給方法と料金体系が異なり、一般にプロパンの方が単価は高めです。'),
      ('冬にガス代が上がるのは？','水温が低くお湯を沸かすのにガスを多く使うためです。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const n=+sel('ninzu').value||1,ty=+$('type').value||1;
    const base=[0,3000,4500,5200,5800,6500][n], avg=Math.round(base*ty/10)*10;
    $('sub').textContent=sel('ninzu').text+'・'+sel('type').text+'の目安';
    $('winter').textContent=yen(Math.round(avg*1.4));$('year').textContent=yen(avg*12);
    SHARE=`ガス代の目安、${sel('ninzu').text}・${sel('type').text}でおよそ月${yen(avg)}でした🔥`;show();anim(avg);}
'''+ANIM)

# ============================================================
# 7. LED交換 節約シミュ（led）
# ============================================================
add(id='led-setsuyaku', emoji='💡',
  title='LED電球の節約シミュレーター｜白熱電球から替えるといくら得？｜シミュラボ',
  desc='白熱電球をLEDに替えると電気代がどれだけ安くなるかを計算する無料ツール。1年・10年の節約額や、何個替えるとどれだけ得かが分かります。',
  ogtitle='LED電球の節約シミュ｜白熱からいくら得？', ogdesc='白熱電球→LEDの電気代の差額・年間節約額を計算。',
  h1='LED電球の節約シミュレーター',
  lead='白熱電球をLEDに替えると、どれだけ節約できる?消費電力・点灯時間・個数を入れると、電気代の差額と節約額を計算します。',
  inputs='''    <h2>💡 条件を入れる</h2>
    <div class="row"><div class="field"><label>白熱電球のW <span class="hint">W</span></label><input type="number" id="old" value="60" min="0" inputmode="decimal"></div>
    <div class="field"><label>LEDのW <span class="hint">W（同じ明るさ）</span></label><input type="number" id="led" value="8" min="0" inputmode="decimal"></div></div>
    <div class="row"><div class="field"><label>1日の点灯時間 <span class="hint">時間</span></label><input type="number" id="hours" value="5" min="0" inputmode="decimal"></div>
    <div class="field"><label>交換する個数</label><input type="number" id="ko" value="5" min="1" inputmode="numeric"></div></div>
    <div class="field"><label>電気単価 <span class="hint">円/kWh</span></label><input type="number" id="tanka" value="31" min="0" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">節約額を計算</button>''',
  result='''      <div class="label">年間の節約額（合計）</div>
      <div class="big"><span id="big">0</span><span class="unit">円/年</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1個あたり年間</div><div class="v" id="one">—</div></div>
      <div class="stat"><div class="k">10年間の節約</div><div class="v accent" id="ten">—</div></div>
      <div class="stat"><div class="k">電気代の削減率</div><div class="v" id="rate">—</div></div></div>''',
  article='''    <div class="note"><strong>計算式</strong><br>節約額 ＝（白熱W − LED W）÷1000 × 点灯時間 × 365 × 個数 × 単価</div>
    <h2>LEDに替えるとどれだけお得？</h2>
    <p>LED電球は、同じ明るさでも白熱電球の<b>約1/7〜1/8の消費電力</b>。たとえば60Wの白熱電球をLED(約8W)に替えると、消費電力は大幅に減ります。さらにLEDは寿命が長く（約4万時間）、交換の手間や電球代も節約に。よく使う場所から替えるほど効果が大きくなります。'''+NOTE+'''</p>
    <h2>よくある質問</h2>'''+faq([
      ('明るさはどう選ぶ？','W数ではなく「lm（ルーメン）」で選びます。60W相当＝約810lmが目安です。'),
      ('元は取れる？','点灯時間が長い場所ほど早く回収できます。本ツールで年間節約額を確認できます。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const o=Math.max(0,+$('old').value||0),l=Math.max(0,+$('led').value||0),h=Math.max(0,+$('hours').value||0),k=Math.max(1,+$('ko').value||1),t=Math.max(0,+$('tanka').value||0);
    const oneYear=Math.max(0,(o-l))/1000*h*365*t, total=oneYear*k;
    const rate=o>0?Math.round((o-l)/o*100):0;
    $('sub').textContent=`${num(o)}W→${num(l)}W・${num(k)}個・1日${num(h)}h`;
    $('one').textContent=yen(oneYear);$('ten').textContent=yen(total*10);$('rate').textContent=rate+'%減';
    SHARE=`LED節約シミュ、${num(k)}個替えで年間約${yen(total)}（10年で${yen(total*10)}）の節約でした💡`;show();anim(total);}
'''+ANIM)

# ============================================================
# 8. 暖房 電気代比較（danbou）
# ============================================================
add(id='danbou-hikaku', emoji='🌡️',
  title='暖房の電気代比較シミュレーター｜エアコン・こたつ・ストーブどれが安い？｜シミュラボ',
  desc='エアコン・こたつ・ホットカーペット・電気ストーブの電気代を比較できる無料ツール。1時間・1ヶ月のコストを並べて、いちばん安い暖房が分かります。',
  ogtitle='暖房の電気代比較｜どの暖房が安い？', ogdesc='エアコン・こたつ・ストーブ等の電気代を比較。',
  h1='暖房の電気代比較シミュレーター',
  lead='冬の暖房、いちばん安いのはどれ?主な電気暖房の電気代を、1時間・1ヶ月で比較します。使い方の参考に。',
  inputs='''    <h2>🌡️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>1日の使用時間 <span class="hint">時間</span></label><input type="number" id="hours" value="6" min="0" inputmode="decimal"></div>
    <div class="field"><label>使う日数 <span class="hint">日</span></label><input type="number" id="days" value="30" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>電気単価 <span class="hint">円/kWh</span></label><input type="number" id="tanka" value="31" min="0" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">暖房の電気代を比較</button>''',
  result='''      <div class="label">いちばん安い暖房（1ヶ月）</div>
      <div class="big" style="font-size:30px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">こたつ</div><div class="v" id="kotatsu">—</div></div>
      <div class="stat"><div class="k">エアコン暖房</div><div class="v" id="aircon">—</div></div>
      <div class="stat"><div class="k">ホットカーペット</div><div class="v" id="carpet">—</div></div>
      <div class="stat"><div class="k">電気ストーブ</div><div class="v" id="stove">—</div></div></div>''',
  article='''    <div class="note"><strong>消費電力の目安</strong><br>こたつ 約300W／エアコン暖房 約600W／ホットカーペット 約500W／電気ストーブ 約1000W（製品差あり）</div>
    <h2>暖房の電気代を比べると</h2>
    <p>電気暖房の中では、<b>こたつやエアコンが比較的安く</b>、電気ストーブは消費電力が大きく割高になりがちです。エアコンは部屋全体、こたつ・カーペットは局所を温める方式。広い部屋はエアコン、足元だけならこたつ、と使い分けると効率的です。設定温度を控えめにし、サーキュレーターで暖気を循環させると節電になります。'''+NOTE+'''</p>
    <h2>よくある質問</h2>'''+faq([
      ('いちばん安い暖房は？','一般にこたつやエアコン（畳数に合った機種）が安め。電気ストーブは割高です。'),
      ('エアコンと灯油ストーブは？','灯油代次第ですが、電気代だけならエアコンは効率的とされます。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const h=Math.max(0,+$('hours').value||0),d=Math.max(0,+$('days').value||0),t=Math.max(0,+$('tanka').value||0);
    const W={kotatsu:300,aircon:600,carpet:500,stove:1000};
    const m=id=>W[id]/1000*h*d*t;
    const vals={kotatsu:m('kotatsu'),aircon:m('aircon'),carpet:m('carpet'),stove:m('stove')};
    const nm={kotatsu:'こたつ',aircon:'エアコン暖房',carpet:'ホットカーペット',stove:'電気ストーブ'};
    $('kotatsu').textContent=yen(vals.kotatsu);$('aircon').textContent=yen(vals.aircon);$('carpet').textContent=yen(vals.carpet);$('stove').textContent=yen(vals.stove);
    let best='kotatsu';for(const k in vals){if(vals[k]<vals[best])best=k;}
    $('big').textContent=nm[best];$('sub').textContent=`1日${num(h)}h × ${num(d)}日なら月${yen(vals[best])}が最安`;
    SHARE=`暖房の電気代比較、最安は「${nm[best]}」で月${yen(vals[best])}でした🌡️`;show();}
''')

# ============================================================
# 9. EV vs ガソリン 燃料費比較（ev）
# ============================================================
add(id='ev-vs-gasoline', emoji='🔋',
  title='EV vs ガソリン車 燃料費比較シミュレーター｜どっちが安い？｜シミュラボ',
  desc='月間の走行距離から、EV（電気自動車）の電気代とガソリン車の燃料費を比較できる無料ツール。年間でどれだけ差が出るかが分かります。',
  ogtitle='EV vs ガソリン車 燃料費比較｜どっちが安い？', ogdesc='走行距離からEVの電気代とガソリン車の燃料費を比較。',
  h1='EV vs ガソリン車 燃料費比較シミュレーター',
  lead='電気自動車(EV)とガソリン車、燃料費はどっちが安い?月間の走行距離を入れると、EVの電気代とガソリン車の燃料費を比較します。',
  inputs='''    <h2>🔋 条件を入れる</h2>
    <div class="field"><label>月間の走行距離 <span class="hint">km</span></label><input type="number" id="dist" value="800" min="0" inputmode="decimal"></div>
    <div class="row"><div class="field"><label>ガソリン車の燃費 <span class="hint">km/L</span></label><input type="number" id="nenpi" value="15" min="0.1" inputmode="decimal"></div>
    <div class="field"><label>ガソリン単価 <span class="hint">円/L</span></label><input type="number" id="gtanka" value="175" min="0" inputmode="decimal"></div></div>
    <div class="row"><div class="field"><label>EVの電費 <span class="hint">km/kWh</span></label><input type="number" id="denpi" value="7" min="0.1" inputmode="decimal"></div>
    <div class="field"><label>電気単価 <span class="hint">円/kWh</span></label><input type="number" id="etanka" value="31" min="0" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">燃料費を比較</button>''',
  result='''      <div class="label">月の燃料費の差（ガソリン − EV）</div>
      <div class="big"><span id="big">0</span><span class="unit">円/月 お得</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">ガソリン車</div><div class="v" id="gas">—</div></div>
      <div class="stat"><div class="k">EV（電気代）</div><div class="v accent" id="ev">—</div></div>
      <div class="stat"><div class="k">年間の差額</div><div class="v" id="year">—</div></div></div>''',
  article='''    <div class="note"><strong>計算式</strong><br>ガソリン車 ＝ 距離÷燃費×ガソリン単価／EV ＝ 距離÷電費×電気単価</div>
    <h2>EVとガソリン車、燃料費はどっちが安い？</h2>
    <p>一般に、走った距離あたりの「燃料費」は<b>EVの方が安い</b>傾向です（自宅充電・通常単価の場合）。ただし、EVは車両価格が高め、急速充電は単価が上がる、電気料金プランで差が出る、などの要素もあります。本ツールは燃料費（電気代・ガソリン代）のみの比較です。車両価格・税・メンテまで含めた総コストは別途検討を。'''+NOTE+'''</p>
    <h2>よくある質問</h2>'''+faq([
      ('電費(km/kWh)とは？','1kWhで走れる距離。EVの「燃費」にあたる指標で、概ね6〜8km/kWhほどです。'),
      ('急速充電だと変わる？','はい。外部の急速充電は単価が高めなので、自宅充電中心の方がお得です。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const d=Math.max(0,+$('dist').value||0),n=Math.max(0.1,+$('nenpi').value||0.1),g=Math.max(0,+$('gtanka').value||0),dp=Math.max(0.1,+$('denpi').value||0.1),e=Math.max(0,+$('etanka').value||0);
    const gas=d/n*g, ev=d/dp*e, diff=gas-ev;
    $('gas').textContent=yen(gas)+'/月';$('ev').textContent=yen(ev)+'/月';$('year').textContent=yen(Math.abs(diff)*12);
    $('sub').textContent = diff>=0 ? `EVの方が月 ${yen(diff)} お得` : `ガソリン車の方が月 ${yen(-diff)} お得`;
    SHARE=`EV vs ガソリン燃料費、月${num(d)}kmならEVが月${yen(Math.abs(diff))}お得（年${yen(Math.abs(diff)*12)}）でした🔋`;show();anim(Math.abs(diff));}
'''+ANIM)

# ============================================================
# 10. 光熱費 高すぎ？診断（世帯平均と比較）num風だが calc
# ============================================================
add(id='kounetsuhi-shindan', emoji='📊',
  title='光熱費 高すぎ？診断｜わが家の電気・ガス・水道は平均より高い？｜シミュラボ',
  desc='世帯人数と毎月の電気・ガス・水道代を入れると、全国平均と比べて高いか安いかを判定する無料ツール。節約の余地が分かります。',
  ogtitle='光熱費 高すぎ？診断｜平均と比較', ogdesc='世帯人数と光熱費から全国平均と比較し高い/安いを判定。',
  h1='光熱費 高すぎ？診断',
  lead='うちの光熱費、高すぎ?世帯人数と毎月の電気・ガス・水道代を入れると、全国平均と比べて判定します。節約の余地もチェック。',
  inputs='''    <h2>📊 条件を入れる</h2>
    <div class="field"><label>世帯人数</label><select id="ninzu">
      <option value="1">1人暮らし</option><option value="2" selected>2人世帯</option><option value="3">3人世帯</option>
      <option value="4">4人世帯</option><option value="5">5人以上</option></select></div>
    <div class="row"><div class="field"><label>電気代 <span class="hint">円/月</span></label><input type="number" id="d" value="9000" min="0" inputmode="numeric"></div>
    <div class="field"><label>ガス代 <span class="hint">円/月</span></label><input type="number" id="g" value="5000" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>水道代 <span class="hint">円/月（2ヶ月なら半額で）</span></label><input type="number" id="w" value="4000" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">平均と比べる</button>''',
  result='''      <div class="label">わが家の光熱費（月合計）</div>
      <div class="big"><span id="big">0</span><span class="unit">円/月</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="verdict" style="text-align:left;margin-top:12px;">—</div>
      <div class="statline"><div class="stat"><div class="k">全国平均の目安</div><div class="v accent" id="avg">—</div></div>
      <div class="stat"><div class="k">平均との差</div><div class="v" id="diff">—</div></div></div>''',
  article='''    <div class="note"><strong>目安について</strong><br>平均は世帯人数別の一般的な目安です。地域・季節・住居タイプで変わります。</div>
    <h2>光熱費の平均と、わが家の位置</h2>
    <p>光熱費（電気・ガス・水道）の合計は、世帯人数が増えるほど高くなります。目安は1人暮らしで月1.3〜1.5万円、2人世帯で約1.9〜2.2万円、4人世帯で約2.5〜3万円ほど（季節変動あり）。平均より高い場合は、契約プランの見直し・古い家電の買い替え・使い方の工夫で下げられる余地があります。まずは何にいちばん使っているかを把握するのが節約の第一歩です。</p>
    <h2>よくある質問</h2>'''+faq([
      ('平均より高いと問題？','必ずしも無駄とは限りませんが、見直しの余地はあります。内訳の把握から始めましょう。'),
      ('まず何を見直す？','契約プラン・基本料金、消費電力の大きい家電、お湯の使い方が効きやすいです。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const n=+sel('ninzu').value||1,d=Math.max(0,+$('d').value||0),g=Math.max(0,+$('g').value||0),w=Math.max(0,+$('w').value||0);
    const total=d+g+w, avg=[0,14000,20500,24000,27000,30000][n], diff=total-avg;
    $('sub').textContent=sel('ninzu').text+'・電気/ガス/水道の合計';
    $('avg').textContent=yen(avg)+'/月';
    if(diff>avg*0.12){$('verdict').className='alert warn';$('verdict').textContent='⚠️ 平均よりやや高めです。契約プランの見直しや、消費電力の大きい家電の使い方から節約の余地がありそうです。';}
    else if(diff<-avg*0.12){$('verdict').className='alert good';$('verdict').textContent='✨ 平均より節約できています！この調子で。';}
    else{$('verdict').className='alert good';$('verdict').textContent='🙂 ほぼ平均的です。気になる費目があれば見直してみましょう。';}
    $('diff').textContent=(diff>=0?'+':'')+yen(diff);
    SHARE=`光熱費 高すぎ？診断、わが家は月${yen(total)}（${sel('ninzu').text}平均${yen(avg)}）でした📊`;show();anim(total);}
'''+ANIM)

if __name__=='__main__':
    render()
    print(f'hikari done. {len(SIMS)} sims.')
