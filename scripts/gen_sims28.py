# -*- coding: utf-8 -*-
"""シミュラボ：税金・確定申告カテゴリ 10本（gen_sims11のTPLを再利用）。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq, write_all

TX = '税金・確定申告'
SIMS = []
def add(**k): SIMS.append(k)

# 給与所得控除（共通で使う近似をJS内に都度記述）
add(id='juuminzei', cat=TX, emoji='🧾',
  title='住民税シミュレーター｜年収から住民税はいくら？｜シミュラボ',
  desc='額面年収から、給与所得控除・社会保険料・基礎控除を概算で引いて、1年の住民税の目安を計算する無料シミュレーター。',
  ogtitle='住民税シミュレーター｜年収から住民税はいくら？', ogdesc='年収から住民税の目安を概算で計算。',
  h1='住民税シミュレーター',
  lead='翌年にやってくる住民税、年収からいくらになる？給与所得控除や社会保険料を引いた概算で、年間の住民税の目安を出します（独身・概算）。',
  inputs='''    <h2>🧾 年収を入れる</h2>
    <div class="field"><label>額面年収 <span class="hint">（万円）</span></label><input type="number" id="g" value="450" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">住民税を計算する</button>''',
  result='''      <div class="label">年間の住民税（目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1ヶ月あたり</div><div class="v accent" id="mo">—</div></div>
      <div class="stat"><div class="k">課税所得</div><div class="v" id="ka">—</div></div>
      <div class="stat"><div class="k">所得割＋均等割</div><div class="v" id="uchi">—</div></div></div>''',
  article='''    <h2>住民税のしくみ</h2>
    <div class="note"><strong>概算の計算</strong><br>課税所得 ＝ 年収 − 給与所得控除 − 社会保険料(約15%) − 基礎控除43万<br>住民税 ＝ 課税所得 × 10% ＋ 均等割（約5,000円）</div>
    <p>住民税は前年の所得に対して課税され、翌年の6月から納めます。所得割（一律約10%）＋均等割が基本。扶養や各種控除で変わるため、本ツールは独身・概算の目安です。</p>
    <h2>よくある質問</h2>'''+faq([('いつ払う？','前年所得に対し、翌年6月〜翌々年5月に納めます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function kyuyo(g){ // 給与所得控除後の給与所得(円) g=円
    let c; if(g<=1625000)c=550000; else if(g<=1800000)c=g*0.4-100000; else if(g<=3600000)c=g*0.3+80000; else if(g<=6600000)c=g*0.2+440000; else if(g<=8500000)c=g*0.1+1100000; else c=1950000;
    return Math.max(0,g-c);
  }
  function calc(){const g=Math.max(0,+$('g').value||0)*10000;
    const sho=kyuyo(g), sha=g*0.15, ka=Math.max(0,sho-sha-430000);
    const tax=ka*0.10+5000;
    $('sub').textContent=`額面${num(g/10000)}万円`;$('mo').textContent=yen(tax/12);$('ka').textContent=yen(ka);$('uchi').textContent=yen(ka*0.1)+'＋5,000';
    SHARE=`住民税シミュ、年収${num(g/10000)}万円なら住民税は年 約${yen(tax)}（月${yen(tax/12)}）でした🧾`;show();anim($('big'),0,tax,800);}''')

add(id='shotokuzei', cat=TX, emoji='💴',
  title='所得税シミュレーター｜年収から所得税はいくら？｜シミュラボ',
  desc='額面年収から、給与所得控除・社会保険料・基礎控除を引いた課税所得をもとに、累進税率で所得税の目安を計算する無料シミュレーター。',
  ogtitle='所得税シミュレーター｜年収から所得税は？', ogdesc='年収から課税所得を出し、累進税率で所得税を計算。',
  h1='所得税シミュレーター',
  lead='年収からかかる所得税はいくら？給与所得控除などを引いた課税所得に、累進税率を当てはめて所得税の目安を計算します（独身・概算）。',
  inputs='''    <h2>💴 年収を入れる</h2>
    <div class="field"><label>額面年収 <span class="hint">（万円）</span></label><input type="number" id="g" value="450" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">所得税を計算する</button>''',
  result='''      <div class="label">年間の所得税（目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">課税所得</div><div class="v" id="ka">—</div></div>
      <div class="stat"><div class="k">適用税率</div><div class="v accent" id="rate">—</div></div>
      <div class="stat"><div class="k">月あたり</div><div class="v" id="mo">—</div></div></div>''',
  article='''    <h2>所得税の累進課税</h2>
    <div class="note"><strong>税率（課税所得）</strong><br>195万以下5%／〜330万10%／〜695万20%／〜900万23%／〜1800万33%／〜4000万40%／超45%<br>（基礎控除48万・給与所得控除・社会保険料控除後）</div>
    <p>所得税は所得が高いほど税率が上がる累進課税。本ツールは独身・概算で、扶養・各種控除（生命保険料・iDeCo等）で実際は下がります。復興特別所得税(2.1%)は考慮していません。</p>
    <h2>よくある質問</h2>'''+faq([('控除を増やすには？','iDeCo・ふるさと納税・各種保険料控除などで課税所得を減らせます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function kyuyo(g){let c;if(g<=1625000)c=550000;else if(g<=1800000)c=g*0.4-100000;else if(g<=3600000)c=g*0.3+80000;else if(g<=6600000)c=g*0.2+440000;else if(g<=8500000)c=g*0.1+1100000;else c=1950000;return Math.max(0,g-c);}
  function calc(){const g=Math.max(0,+$('g').value||0)*10000;
    const ka=Math.max(0,kyuyo(g)-g*0.15-480000);
    let tax,rate;
    if(ka<=1950000){tax=ka*0.05;rate='5%';}else if(ka<=3300000){tax=ka*0.10-97500;rate='10%';}else if(ka<=6950000){tax=ka*0.20-427500;rate='20%';}else if(ka<=9000000){tax=ka*0.23-636000;rate='23%';}else if(ka<=18000000){tax=ka*0.33-1536000;rate='33%';}else{tax=ka*0.40-2796000;rate='40%';}
    tax=Math.max(0,tax);
    $('sub').textContent=`額面${num(g/10000)}万円`;$('ka').textContent=yen(ka);$('rate').textContent=rate;$('mo').textContent=yen(tax/12);
    SHARE=`所得税シミュ、年収${num(g/10000)}万円なら所得税は年 約${yen(tax)}（税率${rate}）でした💴`;show();anim($('big'),0,tax,800);}''')

add(id='iryouhi-koujo', cat=TX, emoji='🩹',
  title='医療費控除シミュレーター｜確定申告でいくら戻る？｜シミュラボ',
  desc='1年の医療費・保険などで補填された額・所得から、医療費控除の額と還付される税金の目安を計算する無料シミュレーター。',
  ogtitle='医療費控除シミュレーター｜いくら戻る？', ogdesc='年間医療費と所得から医療費控除と還付額を計算。',
  h1='医療費控除シミュレーター',
  lead='1年の医療費が10万円を超えたら確定申告で取り戻せるかも。医療費・保険の補填額・所得から、控除額と戻ってくる税金の目安を計算します。',
  inputs='''    <h2>🩹 条件を入れる</h2>
    <div class="row"><div class="field"><label>年間の医療費 <span class="hint">（円・家族分も）</span></label><input type="number" id="hi" value="250000" min="0" inputmode="numeric"></div>
    <div class="field"><label>保険等で補填された額 <span class="hint">（円）</span></label><input type="number" id="ho" value="0" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>課税所得の税率帯</label><select id="rate"><option value="0.05">5%（〜195万）</option><option value="0.10" selected>10%（〜330万）</option><option value="0.20">20%（〜695万）</option><option value="0.23">23%（〜900万）</option><option value="0.33">33%（〜1800万）</option></select></div>
    <button class="btn btn-primary" id="calcBtn">還付額を見る</button>''',
  result='''      <div class="label">戻ってくる税金（目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">医療費控除額</div><div class="v accent" id="koujo">—</div></div>
      <div class="stat"><div class="k">所得税の還付</div><div class="v" id="sho">—</div></div>
      <div class="stat"><div class="k">住民税の軽減</div><div class="v" id="ju">—</div></div></div>''',
  article='''    <h2>医療費控除のしくみ</h2>
    <div class="note"><strong>計算式</strong><br>控除額 ＝ 医療費 − 補填額 − 10万円（所得200万未満は所得5%）<br>戻る税金 ≒ 控除額 ×（所得税率 ＋ 住民税10%）</div>
    <p>1年間（1〜12月）の医療費が10万円を超えると、確定申告で所得税の還付＋翌年の住民税が軽くなります。家族分も合算でき、通院の交通費も対象。レシートは保管を。セルフメディケーション税制との選択制です。</p>
    <h2>よくある質問</h2>'''+faq([('交通費も対象？','通院の公共交通費は対象です。自家用車のガソリン代は対象外。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const hi=Math.max(0,+$('hi').value||0),ho=Math.max(0,+$('ho').value||0),rate=+$('rate').value||0.1;
    const koujo=Math.max(0,hi-ho-100000), sho=koujo*rate, ju=koujo*0.10, back=sho+ju;
    $('sub').textContent=`医療費${num(hi)}円・補填${num(ho)}円・税率${Math.round(rate*100)}%`;$('koujo').textContent=yen(koujo);$('sho').textContent=yen(sho);$('ju').textContent=yen(ju);
    SHARE=`医療費控除シミュ、確定申告で約${yen(back)}戻ってくる計算でした🩹（控除${yen(koujo)}）`;show();anim($('big'),0,back,800);}''')

add(id='nenmatsu-chousei', cat=TX, emoji='📋',
  title='年末調整 還付額シミュレーター｜年末調整でいくら戻る？｜シミュラボ',
  desc='生命保険料控除・iDeCo・扶養などの控除額と税率から、年末調整で戻ってくる税金の目安を計算する無料シミュレーター。',
  ogtitle='年末調整 還付額シミュレーター｜いくら戻る？', ogdesc='各種控除と税率から年末調整の還付額を計算。',
  h1='年末調整 還付額シミュレーター',
  lead='12月のお給料で戻ってくる年末調整の還付金、いくらくらい？生命保険料控除やiDeCo、扶養などの控除額から、戻る税金の目安を計算します。',
  inputs='''    <h2>📋 控除額を入れる</h2>
    <div class="row"><div class="field"><label>生命保険料控除 <span class="hint">（円・最大12万）</span></label><input type="number" id="hoken" value="80000" min="0" max="120000" inputmode="numeric"></div>
    <div class="field"><label>iDeCo等の掛金 <span class="hint">（円/年）</span></label><input type="number" id="ideco" value="276000" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>扶養親族 <span class="hint">（人・一般）</span></label><input type="number" id="fuyou" value="0" min="0" max="10" inputmode="numeric"></div>
    <div class="field"><label>所得税率</label><select id="rate"><option value="0.05">5%</option><option value="0.10" selected>10%</option><option value="0.20">20%</option><option value="0.23">23%</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">還付額を見る</button>''',
  result='''      <div class="label">年末調整の還付（目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">控除の合計</div><div class="v accent" id="koujo">—</div></div>
      <div class="stat"><div class="k">うち扶養控除</div><div class="v" id="fv">—</div></div>
      <div class="stat"><div class="k">住民税の軽減も</div><div class="v" id="ju">—</div></div></div>''',
  article='''    <h2>年末調整で戻るしくみ</h2>
    <div class="note"><strong>計算式</strong><br>控除合計 ＝ 生命保険料控除 ＋ iDeCo掛金 ＋ 扶養控除(1人38万)…<br>還付 ≒ 控除合計 × 所得税率</div>
    <p>毎月の給与から多めに天引きされた所得税が、控除を反映して精算され、払いすぎた分が戻ります。保険料控除証明書やiDeCoの証明書を会社に提出するのを忘れずに。住民税も翌年軽くなります。</p>
    <h2>よくある質問</h2>'''+faq([('iDeCoも年末調整で？','会社員は年末調整で申告できます（証明書が必要）。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const h=Math.max(0,Math.min(120000,+$('hoken').value||0)),i=Math.max(0,+$('ideco').value||0),f=Math.max(0,+$('fuyou').value||0),rate=+$('rate').value||0.1;
    const fv=f*380000, koujo=h+i+fv, back=koujo*rate, ju=koujo*0.10;
    $('sub').textContent=`保険${num(h)}＋iDeCo${num(i)}＋扶養${f}人`;$('koujo').textContent=yen(koujo);$('fv').textContent=yen(fv);$('ju').textContent=yen(ju);
    SHARE=`年末調整シミュ、還付の目安は約${yen(back)}でした📋（控除合計${yen(koujo)}）`;show();anim($('big'),0,back,800);}''')

add(id='fuyou-koujo', cat=TX, emoji='👨‍👩‍👧',
  title='扶養控除シミュレーター｜扶養家族で税金はいくら減る？｜シミュラボ',
  desc='扶養する家族の人数と年齢区分（一般・特定扶養・老人扶養）から、扶養控除による所得税・住民税の節税額を計算する無料シミュレーター。',
  ogtitle='扶養控除シミュレーター｜税金はいくら減る？', ogdesc='扶養人数と区分から扶養控除の節税額を計算。',
  h1='扶養控除シミュレーター',
  lead='扶養する家族がいると税金が安くなります。扶養親族の人数と区分（一般・19〜22歳の特定扶養・70歳以上の老人扶養）から、節税額の目安を計算します。',
  inputs='''    <h2>👨‍👩‍👧 扶養家族を入れる</h2>
    <div class="row"><div class="field"><label>一般の扶養 <span class="hint">（人・控除38万）</span></label><input type="number" id="ippan" value="1" min="0" max="10" inputmode="numeric"></div>
    <div class="field"><label>特定扶養（19〜22歳） <span class="hint">（人・控除63万）</span></label><input type="number" id="tokutei" value="0" min="0" max="10" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>老人扶養（70歳〜） <span class="hint">（人・控除48万）</span></label><input type="number" id="rojin" value="0" min="0" max="10" inputmode="numeric"></div>
    <div class="field"><label>所得税率</label><select id="rate"><option value="0.05">5%</option><option value="0.10" selected>10%</option><option value="0.20">20%</option><option value="0.23">23%</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">節税額を見る</button>''',
  result='''      <div class="label">節税額（所得税＋住民税）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">控除の合計</div><div class="v accent" id="koujo">—</div></div>
      <div class="stat"><div class="k">所得税の軽減</div><div class="v" id="sho">—</div></div>
      <div class="stat"><div class="k">住民税の軽減</div><div class="v" id="ju">—</div></div></div>''',
  article='''    <h2>扶養控除の区分</h2>
    <div class="note"><strong>控除額（所得税）</strong><br>一般の扶養親族(16歳〜)＝38万／特定扶養(19〜22歳)＝63万／老人扶養(70歳〜・同居)＝58万、別居48万<br>節税 ≒ 控除 ×（所得税率＋住民税分）</div>
    <p>大学生世代（特定扶養）は控除が大きく節税効果も大。扶養に入れるには家族の年収要件（給与なら103万円以下）があります。本ツールは概算で、住民税の控除額は所得税と少し異なります。</p>
    <h2>よくある質問</h2>'''+faq([('16歳未満は？','児童手当の対象で、扶養控除（所得税）はありません。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const a=Math.max(0,+$('ippan').value||0),t=Math.max(0,+$('tokutei').value||0),r=Math.max(0,+$('rojin').value||0),rate=+$('rate').value||0.1;
    const koujo=a*380000+t*630000+r*480000, sho=koujo*rate, ju=(a*330000+t*450000+r*380000)*0.10, total=sho+ju;
    $('sub').textContent=`一般${a}・特定${t}・老人${r}人`;$('koujo').textContent=yen(koujo);$('sho').textContent=yen(sho);$('ju').textContent=yen(ju);
    SHARE=`扶養控除シミュ、節税額は年 約${yen(total)}でした👨‍👩‍👧`;show();anim($('big'),0,total,800);}''')

add(id='kabu-zei', cat=TX, emoji='📊',
  title='株の税金シミュレーター｜利益にかかる税金と手取りは？｜シミュラボ',
  desc='株式・投資信託の譲渡益や配当金から、約20.315%の税金と手取り額、NISAなら非課税でいくら得かを計算する無料シミュレーター。',
  ogtitle='株の税金シミュレーター｜税金と手取りは？', ogdesc='譲渡益・配当から税金(20.315%)と手取りを計算。',
  h1='株の税金シミュレーター',
  lead='株や投資信託でもうけたら税金は約20%。利益から税金と手取りを計算します。NISAなら非課税なので、どれだけ得かも分かります。',
  inputs='''    <h2>📊 条件を入れる</h2>
    <div class="field"><label>利益（譲渡益・配当） <span class="hint">（円）</span></label><input type="number" id="rieki" value="500000" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">税金と手取りを見る</button>''',
  result='''      <div class="label">税引後の手取り</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">税金(20.315%)</div><div class="v accent" id="zei">—</div></div>
      <div class="stat"><div class="k">NISAなら手取り</div><div class="v" id="nisa">—</div></div>
      <div class="stat"><div class="k">NISAでお得な額</div><div class="v" id="toku">—</div></div></div>''',
  article='''    <h2>株の税金</h2>
    <div class="note"><strong>計算式</strong><br>税金 ＝ 利益 × 20.315%（所得税15% ＋ 住民税5% ＋ 復興税0.315%）<br>手取り ＝ 利益 − 税金</div>
    <p>上場株式・投資信託の利益には一律約20%課税されます。NISA口座での利益は非課税なので、その分まるまる得に。特定口座（源泉徴収あり）なら確定申告は原則不要です。</p>
    <h2>よくある質問</h2>'''+faq([('損したら？','損失は確定申告で他の利益と相殺・3年間繰越できます（損益通算）。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const r=Math.max(0,+$('rieki').value||0);const zei=r*0.20315, net=r-zei;
    $('sub').textContent=`利益${num(r)}円`;$('zei').textContent=yen(zei);$('nisa').textContent=yen(r);$('toku').textContent=yen(zei);
    SHARE=`株の税金シミュ、利益${num(r)}円の税金は約${yen(zei)}・手取り${yen(net)}でした📊 NISAなら${yen(zei)}お得！`;show();anim($('big'),0,net,800);}''')

add(id='shouhizei', cat=TX, emoji='🛒',
  title='消費税計算ツール｜税込・税抜・軽減税率を一発計算｜シミュラボ',
  desc='金額から消費税（10%・軽減8%）の税込・税抜・税額を一発で計算する無料ツール。買い物や経理の確認に。',
  ogtitle='消費税計算ツール｜税込・税抜を一発計算', ogdesc='金額から消費税の税込・税抜・税額を計算。',
  h1='消費税計算ツール',
  lead='税抜から税込、税込から税抜、消費税額だけ——を一発で計算します。標準10%と軽減税率8%に対応。買い物や経理のちょっとした確認に。',
  inputs='''    <h2>🛒 条件を入れる</h2>
    <div class="row"><div class="field"><label>金額 <span class="hint">（円）</span></label><input type="number" id="amount" value="1000" min="0" inputmode="numeric"></div>
    <div class="field"><label>入力した金額は</label><select id="mode"><option value="nuki" selected>税抜価格</option><option value="komi">税込価格</option></select></div></div>
    <div class="field"><label>税率</label><select id="rate"><option value="0.10" selected>10%（標準）</option><option value="0.08">8%（軽減・飲食料品等）</option></select></div>
    <button class="btn btn-primary" id="calcBtn">計算する</button>''',
  result='''      <div class="label" id="lab">税込価格</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">税抜</div><div class="v" id="nuki">—</div></div>
      <div class="stat"><div class="k">消費税額</div><div class="v accent" id="zei">—</div></div>
      <div class="stat"><div class="k">税率</div><div class="v" id="rv">—</div></div></div>''',
  article='''    <h2>消費税の計算</h2>
    <div class="note"><strong>計算式</strong><br>税込 ＝ 税抜 ×（1 ＋ 税率）／税抜 ＝ 税込 ÷（1 ＋ 税率）</div>
    <p>標準税率は10%、飲食料品（酒類・外食除く）や新聞は軽減税率8%です。端数処理（切り捨て等）は事業者により異なります。本ツールは四捨五入の目安です。</p>
    <h2>よくある質問</h2>'''+faq([('外食は8%？','店内飲食は10%、テイクアウトは8%が原則です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const a=Math.max(0,+$('amount').value||0),mode=$('mode').value,rate=+$('rate').value||0.1;
    let nuki,komi; if(mode==='nuki'){nuki=a;komi=a*(1+rate);}else{komi=a;nuki=a/(1+rate);}
    const zei=komi-nuki; const showVal=mode==='nuki'?komi:nuki;
    $('lab').textContent=mode==='nuki'?'税込価格':'税抜価格';
    $('sub').textContent=`${mode==='nuki'?'税抜':'税込'} ${num(a)}円・税率${Math.round(rate*100)}%`;$('nuki').textContent=yen(nuki);$('zei').textContent=yen(zei);$('rv').textContent=Math.round(rate*100)+'%';
    SHARE=`消費税計算、${num(a)}円(${mode==='nuki'?'税抜':'税込'})は税込${yen(komi)}・消費税${yen(zei)}でした🛒`;show();anim($('big'),0,showVal,800);}''')

add(id='kojin-jigyo', cat=TX, emoji='🧑‍💼',
  title='個人事業主の税金シミュレーター｜所得からいくら引かれる？｜シミュラボ',
  desc='個人事業の所得（売上−経費）から、所得税・住民税・国民健康保険・国民年金のおおまかな合計負担と手取りを試算する無料シミュレーター。',
  ogtitle='個人事業主の税金シミュレーター｜手取りは？', ogdesc='事業所得から税・社会保険の合計負担と手取りを試算。',
  h1='個人事業主の税金シミュレーター',
  lead='フリーランス・個人事業主は、所得税・住民税・国保・年金を自分で納めます。所得（売上−経費）から、合計の負担と手取りの目安を試算します（独身・概算）。',
  inputs='''    <h2>🧑‍💼 条件を入れる</h2>
    <div class="row"><div class="field"><label>事業所得（売上−経費） <span class="hint">（万円）</span></label><input type="number" id="sho" value="400" min="0" inputmode="numeric"></div>
    <div class="field"><label>青色申告</label><select id="ao"><option value="650000" selected>あり（控除65万）</option><option value="0">なし</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">税・保険を見る</button>''',
  result='''      <div class="label">手取り（概算）</div>
      <div class="big"><span id="big">0</span><span class="unit">万円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">所得税＋住民税</div><div class="v" id="zei">—</div></div>
      <div class="stat"><div class="k">国保＋年金</div><div class="v accent" id="hoken">—</div></div>
      <div class="stat"><div class="k">負担率</div><div class="v" id="rate">—</div></div></div>''',
  article='''    <h2>個人事業主の負担</h2>
    <div class="note"><strong>概算の内訳</strong><br>課税所得 ＝ 事業所得 − 青色申告控除 − 基礎控除48万 − 社会保険料<br>所得税(累進)＋住民税(約10%)＋国民健康保険＋国民年金(約20万/年)</div>
    <p>会社員と違い社会保険も全額自己負担。青色申告（最大65万控除）や経費計上、小規模企業共済・iDeCoの活用で負担を減らせます。本ツールは独身・概算で、自治体や所得で変わります。</p>
    <h2>よくある質問</h2>'''+faq([('国保はいくら？','自治体・所得で変動。本ツールは所得の約10%＋均等割で概算しています。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const sho=Math.max(0,+$('sho').value||0)*10000,ao=+$('ao').value||0;
    const nenkin=200000, kokuho=Math.min(900000, sho*0.10+50000);
    const ka=Math.max(0,sho-ao-480000-nenkin-kokuho);
    let it; if(ka<=1950000)it=ka*0.05;else if(ka<=3300000)it=ka*0.10-97500;else if(ka<=6950000)it=ka*0.20-427500;else it=ka*0.23-636000; it=Math.max(0,it);
    const ju=ka*0.10+5000, zei=it+ju, hoken=nenkin+kokuho, net=sho-zei-hoken;
    $('sub').textContent=`事業所得${num(sho/10000)}万・青色${ao?'あり':'なし'}`;$('zei').textContent=yen(zei);$('hoken').textContent=yen(hoken);$('rate').textContent=Math.round((zei+hoken)/sho*100)+'%';
    SHARE=`個人事業主の税金シミュ、所得${num(sho/10000)}万で手取り約${num(net/10000)}万円（負担率${Math.round((zei+hoken)/sho*100)}%）でした🧑‍💼`;show();anim($('big'),0,net/10000,800);}''')

add(id='zoyozei', cat=TX, emoji='🎀',
  title='贈与税シミュレーター｜もらったお金の贈与税はいくら？｜シミュラボ',
  desc='1年間にもらった金額から、基礎控除110万円を引いて贈与税（一般税率・特例税率）を計算する無料シミュレーター。',
  ogtitle='贈与税シミュレーター｜贈与税はいくら？', ogdesc='もらった額から基礎控除110万を引いて贈与税を計算。',
  h1='贈与税シミュレーター',
  lead='1年間にもらったお金が110万円を超えると贈与税がかかります。もらった額と関係（親子など＝特例税率）から、贈与税額を計算します。',
  inputs='''    <h2>🎀 条件を入れる</h2>
    <div class="row"><div class="field"><label>1年でもらった額 <span class="hint">（万円）</span></label><input type="number" id="m" value="500" min="0" inputmode="numeric"></div>
    <div class="field"><label>贈与の種類</label><select id="type"><option value="tokurei" selected>特例（親・祖父母→18歳以上の子孫）</option><option value="ippan">一般（それ以外）</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">贈与税を計算する</button>''',
  result='''      <div class="label">贈与税の目安</div>
      <div class="big"><span id="big">0</span><span class="unit">万円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">基礎控除後</div><div class="v" id="kazei">—</div></div>
      <div class="stat"><div class="k">実質の手取り</div><div class="v accent" id="net">—</div></div>
      <div class="stat"><div class="k">負担率</div><div class="v" id="rate">—</div></div></div>''',
  article='''    <h2>贈与税のしくみ</h2>
    <div class="note"><strong>計算式</strong><br>課税額 ＝ もらった額 − 基礎控除110万円<br>贈与税 ＝ 課税額 × 税率 − 控除額（金額帯で変動）</div>
    <p>贈与税は「もらった人」が、もらった年の翌年に申告・納税します。親・祖父母から18歳以上の子・孫への贈与は「特例税率」で少し軽くなります。住宅取得・教育資金などの非課税特例もあります。本ツールは暦年課税の目安です。</p>
    <h2>よくある質問</h2>'''+faq([('110万以内なら？','非課税で申告も不要です（暦年課税の場合）。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const m=Math.max(0,+$('m').value||0)*10000, type=$('type').value;
    const ka=Math.max(0,m-1100000); let zei;
    function tax(k,sp){ // 万円単位の課税額kに対し
      const t=sp?[[2000000,0.10,0],[4000000,0.15,100000],[6000000,0.20,300000],[10000000,0.30,900000],[15000000,0.40,1900000],[30000000,0.45,2650000],[45000000,0.50,4150000],[1e12,0.55,6400000]]:[[2000000,0.10,0],[3000000,0.15,100000],[4000000,0.20,250000],[6000000,0.30,650000],[10000000,0.40,1250000],[15000000,0.45,1750000],[30000000,0.50,2500000],[1e12,0.55,4000000]];
      for(const [lim,r,c] of t){ if(k<=lim) return Math.max(0,k*r-c); } return 0;
    }
    zei=tax(ka, type==='tokurei');
    const net=m-zei;
    $('sub').textContent=`${num(m/10000)}万円・${type==='tokurei'?'特例':'一般'}税率`;$('kazei').textContent=num(ka/10000)+'万円';$('net').textContent=num(net/10000)+'万円';$('rate').textContent=Math.round(zei/m*100)+'%';
    SHARE=`贈与税シミュ、${num(m/10000)}万円もらうと贈与税は約${num(zei/10000)}万円でした🎀`;show();anim($('big'),0,zei/10000,800);}''')

add(id='taishokukin-zei', cat=TX, emoji='🏖️',
  title='退職金の税金シミュレーター｜退職金の手取りはいくら？｜シミュラボ',
  desc='退職金の額と勤続年数から、退職所得控除を引いた課税額・税金・手取りを計算する無料シミュレーター。退職金は税制優遇が大きい。',
  ogtitle='退職金の税金シミュレーター｜手取りはいくら？', ogdesc='退職金と勤続年数から退職所得控除・税・手取りを計算。',
  h1='退職金の税金シミュレーター',
  lead='退職金には大きな税制優遇（退職所得控除）があります。退職金の額と勤続年数から、引かれる税金と手取りを計算します。',
  inputs='''    <h2>🏖️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>退職金の額 <span class="hint">（万円）</span></label><input type="number" id="m" value="2000" min="0" inputmode="numeric"></div>
    <div class="field"><label>勤続年数 <span class="hint">（年）</span></label><input type="number" id="years" value="35" min="1" max="50" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">手取りを見る</button>''',
  result='''      <div class="label">退職金の手取り</div>
      <div class="big"><span id="big">0</span><span class="unit">万円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">退職所得控除</div><div class="v accent" id="koujo">—</div></div>
      <div class="stat"><div class="k">税金の合計</div><div class="v" id="zei">—</div></div>
      <div class="stat"><div class="k">課税退職所得</div><div class="v" id="ka">—</div></div></div>''',
  article='''    <h2>退職金が優遇される理由</h2>
    <div class="note"><strong>計算式</strong><br>退職所得控除 ＝ 勤続20年まで40万/年、20年超は70万/年<br>課税退職所得 ＝（退職金 − 控除）÷ 2<br>これに所得税・住民税がかかる</div>
    <p>長年の勤労への配慮で、退職金は控除が大きく、さらに残りを「半分」にしてから課税されるため、税金がかなり軽くなります。勤続年数が長いほど控除も増えます。本ツールは概算です。</p>
    <h2>よくある質問</h2>'''+faq([('一時金と年金どちら？','一時金は退職所得控除、年金受取は公的年金等控除。トータルで比較を。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const m=Math.max(0,+$('m').value||0)*10000, y=Math.max(1,+$('years').value||1);
    const koujo=(y<=20?40*y:800+70*(y-20))*10000;
    const ka=Math.max(0,(m-koujo)/2);
    let it;if(ka<=1950000)it=ka*0.05;else if(ka<=3300000)it=ka*0.10-97500;else if(ka<=6950000)it=ka*0.20-427500;else if(ka<=9000000)it=ka*0.23-636000;else it=ka*0.33-1536000; it=Math.max(0,it);
    const ju=ka*0.10, zei=it+ju, net=m-zei;
    $('sub').textContent=`退職金${num(m/10000)}万・勤続${y}年`;$('koujo').textContent=num(koujo/10000)+'万円';$('zei').textContent=yen(zei);$('ka').textContent=num(ka/10000)+'万円';
    SHARE=`退職金の税金シミュ、${num(m/10000)}万円の手取りは約${num(net/10000)}万円でした🏖️（控除${num(koujo/10000)}万・税優遇大）`;show();anim($('big'),0,net/10000,800);}''')

if __name__=='__main__':
    write_all(SIMS)
    print(f'tax done. {len(SIMS)} sims.')
