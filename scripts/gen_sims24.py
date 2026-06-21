# -*- coding: utf-8 -*-
"""シミュラボ：全カテゴリ3本ずつ補充 その3（car/travel/home/food/beauty）。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq, write_all

SIMS=[]
def add(**k): SIMS.append(k)

# ===== クルマ・乗り物 =====
add(id='kuruma-shogai', cat='クルマ・乗り物', emoji='🚗',
  title='車の生涯総額シミュレーター｜一生で車にいくら使う？｜シミュラボ',
  desc='車の購入価格・買い替え台数・年間維持費・運転年数から、一生で車にかかる総額を試算する無料シミュレーター。',
  ogtitle='車の生涯総額｜一生で車にいくら使う？', ogdesc='購入・維持・台数から、車にかかる生涯総額を試算。',
  h1='車の生涯総額シミュレーター',
  lead='車は一生でいくらかかる乗り物？購入価格・買い替え台数・年間維持費・運転年数から、生涯の総額を出します。カーシェアと比べる材料にも。',
  inputs='''    <h2>🚗 条件を入れる</h2>
    <div class="row"><div class="field"><label>1台の購入価格 <span class="hint">（万円）</span></label><input type="number" id="price" value="250" min="0" inputmode="numeric"></div>
    <div class="field"><label>生涯の買い替え台数 <span class="hint">（台）</span></label><input type="number" id="cars" value="5" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>年間維持費 <span class="hint">（万円・税/保険/車検/ガソリン等）</span></label><input type="number" id="maint" value="40" min="0" inputmode="numeric"></div>
    <div class="field"><label>運転する年数 <span class="hint">（年）</span></label><input type="number" id="yr" value="50" min="1" max="80" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">生涯総額を見る</button>''',
  result='''      <div class="label">一生で車にかかる総額</div>
      <div class="big"><span id="big">0</span><span class="unit">万円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">車両代の合計</div><div class="v" id="body">—</div></div>
      <div class="stat"><div class="k">維持費の合計</div><div class="v accent" id="m">—</div></div>
      <div class="stat"><div class="k">月あたり</div><div class="v" id="mo">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>生涯総額 ＝ 購入価格 × 台数 ＋ 年間維持費 × 運転年数</div>
    <p>車両代より、実は維持費の合計のほうが大きくなることも。維持費には税金・保険・車検・ガソリン・駐車場が含まれます。本当に必要な使い方か、カーシェアで足りるか、判断の材料に。</p>
    <h2>よくある質問</h2>'''+faq([('ローン金利は？','含みません。本体価格ベースの概算です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const price=Math.max(0,+$('price').value||0),cars=Math.max(0,+$('cars').value||0),maint=Math.max(0,+$('maint').value||0),yr=Math.max(1,+$('yr').value||1);
    const body=price*cars,m=maint*yr,total=body+m;
    $('sub').textContent=`${num(price)}万×${cars}台 ＋ 維持${num(maint)}万×${yr}年`;$('body').textContent=num(body)+'万円';$('m').textContent=num(m)+'万円';$('mo').textContent=num(total*10000/(yr*12))+'円';
    SHARE=`車の生涯総額シミュ、一生で約${num(total)}万円でした🚗\\n維持費の合計が大きい…！👇`;show();anim($('big'),0,total,900);}''')

add(id='jidousha-zei', cat='クルマ・乗り物', emoji='🧾',
  title='自動車税シミュレーター｜排気量で税金はいくら？｜シミュラボ',
  desc='車の排気量から、毎年の自動車税（種別割）の目安と、10年・生涯で払う総額を表示する無料シミュレーター。',
  ogtitle='自動車税シミュレーター｜排気量で税金はいくら？', ogdesc='排気量から自動車税の目安と生涯の総額を表示。',
  h1='自動車税シミュレーター',
  lead='毎年5月にやってくる自動車税。排気量を選ぶと、年間の税額と10年・生涯で払う総額が分かります。車選びの維持費比較に。',
  inputs='''    <h2>🧾 排気量を選ぶ</h2>
    <div class="field"><label>排気量</label><select id="cc"><option value="10800">軽自動車</option><option value="25000">〜1.0L</option><option value="30500" selected>〜1.5L</option><option value="36000">〜2.0L</option><option value="43500">〜2.5L</option><option value="50000">〜3.0L</option></select></div>
    <div class="field"><label>これからの保有年数 <span class="hint">（年）</span></label><input type="number" id="yr" value="40" min="1" max="80" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">税額を見る</button>''',
  result='''      <div class="label">年間の自動車税</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">月あたり</div><div class="v" id="mo">—</div></div>
      <div class="stat"><div class="k">10年で</div><div class="v" id="y10">—</div></div>
      <div class="stat"><div class="k">これからの総額</div><div class="v accent" id="total">—</div></div></div>''',
  article='''    <h2>自動車税のしくみ</h2>
    <div class="note"><strong>目安</strong><br>排気量が大きいほど税額も上がります。軽自動車は一律で割安。<br>※2019年10月以降の新車登録は税率が引き下げられています（本ツールは一般的な目安）。</div>
    <p>排気量の大きい車ほど毎年の税負担が増えます。維持費を抑えたいなら軽自動車やコンパクトカーが有利。13年超の車は税が重くなる点にも注意。</p>
    <h2>よくある質問</h2>'''+faq([('エコカー減税は？','対象車は軽減されます。本ツールは標準的な目安です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const cc=+$('cc').value||0,yr=Math.max(1,+$('yr').value||1);
    $('sub').textContent=`${sel('cc').text}・${yr}年`;$('mo').textContent=yen(cc/12);$('y10').textContent=yen(cc*10);$('total').textContent=yen(cc*yr);
    SHARE=`自動車税シミュ、${sel('cc').text}は年${yen(cc)}・これから${yr}年で${yen(cc*yr)}でした🧾\\n維持費は車選びから。👇`;show();anim($('big'),0,cc,900);}''')

add(id='taiya-cost', cat='クルマ・乗り物', emoji='🛞',
  title='タイヤ生涯コストシミュレーター｜タイヤ交換、一生でいくら？｜シミュラボ',
  desc='タイヤ1セットの価格と交換頻度・運転年数から、一生で払うタイヤ交換費の総額を試算する無料シミュレーター。',
  ogtitle='タイヤ生涯コスト｜タイヤ交換、一生でいくら？', ogdesc='タイヤの価格と交換頻度から、生涯のタイヤ代を試算。',
  h1='タイヤ生涯コストシミュレーター',
  lead='意外と忘れがちなタイヤ代。1セットの価格と交換頻度・運転年数から、一生で払うタイヤ交換費を出します（スタッドレス併用ならさらに）。',
  inputs='''    <h2>🛞 条件を入れる</h2>
    <div class="row"><div class="field"><label>タイヤ1セットの価格 <span class="hint">（円・工賃込み）</span></label><input type="number" id="set" value="60000" min="0" inputmode="numeric"></div>
    <div class="field"><label>交換頻度 <span class="hint">（◯年ごと）</span></label><input type="number" id="freq" value="4" min="1" inputmode="numeric"></div></div>
    <div class="field"><label>運転する年数 <span class="hint">（年）</span></label><input type="number" id="yr" value="40" min="1" max="80" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">生涯コストを見る</button>''',
  result='''      <div class="label">一生のタイヤ交換費</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">交換回数</div><div class="v" id="cnt">—</div></div>
      <div class="stat"><div class="k">年あたり積立</div><div class="v accent" id="save">—</div></div>
      <div class="stat"><div class="k">1回あたり</div><div class="v" id="per">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>交換回数 ＝ 運転年数 ÷ 交換頻度<br>生涯コスト ＝ 1セットの価格 × 交換回数</div>
    <p>タイヤは「ゴムの劣化」で年数でも交換が必要（走行が少なくても約4〜5年が目安）。スタッドレスを使う地域はさらに費用がかかります。毎年少しずつ積み立てておくと安心。</p>
    <h2>よくある質問</h2>'''+faq([('溝が残ってても交換？','ゴムは経年劣化します。安全のため年数での交換も大切です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const set=Math.max(0,+$('set').value||0),freq=Math.max(1,+$('freq').value||1),yr=Math.max(1,+$('yr').value||1);
    const cnt=Math.floor(yr/freq),total=set*cnt;
    $('sub').textContent=`${num(set)}円 ・ ${freq}年ごと ・ ${yr}年`;$('cnt').textContent=cnt+'回';$('save').textContent=yen(total/yr);$('per').textContent=yen(set);
    SHARE=`タイヤ生涯コストシミュ、一生で約${yen(total)}（${cnt}回交換）でした🛞\\n忘れがちな出費…！👇`;show();anim($('big'),0,total,900);}''')

# ===== 旅行・おでかけ =====
add(id='shogai-ryokou', cat='旅行・おでかけ', emoji='🧳',
  title='生涯旅行回数シミュレーター｜あと何回、旅に行ける？｜シミュラボ',
  desc='年に行く旅行の回数とこれからの年数から、一生であと何回旅行できるか・総費用を可視化するエンタメシミュレーター。',
  ogtitle='生涯旅行回数｜あと何回、旅に行ける？', ogdesc='年の旅行回数から、生涯であと何回旅行できるかを可視化。',
  h1='生涯旅行回数シミュレーター',
  lead='元気に旅できる時間にも、限りがあります。年に行く回数とこれからの年数から、一生であと何回旅行できるかを出します。「行きたい場所リスト」を作りたくなる一本。',
  inputs='''    <h2>🧳 条件を入れる</h2>
    <div class="row"><div class="field"><label>年に行く旅行回数 <span class="hint">（回）</span></label><input type="number" id="freq" value="2" min="0" inputmode="numeric"></div>
    <div class="field"><label>これからの年数 <span class="hint">（年）</span></label><input type="number" id="yr" value="50" min="1" max="80" inputmode="numeric"></div></div>
    <div class="field"><label>1回の旅行費用 <span class="hint">（円・総費用の計算用）</span></label><input type="number" id="cost" value="80000" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">あと何回か見る</button>''',
  result='''      <div class="label">これから行ける旅行</div>
      <div class="big"><span id="big">0</span><span class="unit">回</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">生涯の旅行費</div><div class="v accent" id="money">—</div></div>
      <div class="stat"><div class="k">元気に動ける期間で</div><div class="v" id="genki">—</div></div>
      <div class="stat"><div class="k">1回の重み</div><div class="v" id="weight">—</div></div></div>''',
  article='''    <h2>旅は元気なうちに</h2>
    <div class="note"><strong>計算式</strong><br>生涯回数 ＝ 年の回数 × 年数</div>
    <p>数えてみると「無限」ではないと気づきます。とくに体力が必要な旅は、元気なうちにこそ。行きたい場所をリスト化して、優先順位の高いものから計画してみてください。</p>
    <h2>よくある質問</h2>'''+faq([('現実的な回数？','体力や予算で変わります。今のペースでの目安としてどうぞ。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const freq=Math.max(0,+$('freq').value||0),yr=Math.max(1,+$('yr').value||1),cost=Math.max(0,+$('cost').value||0);
    const total=freq*yr,money=total*cost,genki=Math.min(total,freq*Math.min(yr,30));
    $('sub').textContent=`年${freq}回 × ${yr}年`;$('money').textContent=yen(money);$('genki').textContent='約'+num(genki)+'回';$('weight').textContent='プライスレス';
    SHARE=`生涯旅行回数シミュ、これから約${num(total)}回旅に行ける計算でした🧳\\n行きたい場所、リストにしよ…！👇`;show();anim($('big'),0,total,900);}''')

add(id='gaika-ryougae', cat='旅行・おでかけ', emoji='💱',
  title='外貨両替シミュレーター｜手数料込みでいくら受け取れる？｜シミュラボ',
  desc='両替する日本円・為替レート・両替手数料から、実際に受け取れる外貨の額と実質レート・手数料額を計算する無料シミュレーター。',
  ogtitle='外貨両替シミュレーター｜いくら受け取れる？', ogdesc='円・レート・手数料から、受け取れる外貨を計算。',
  h1='外貨両替シミュレーター',
  lead='旅行前の外貨両替、手数料込みだと実際いくら受け取れる？両替額・レート・手数料から、受取額と実質レートを出します。両替所選びの比較に。',
  inputs='''    <h2>💱 条件を入れる</h2>
    <div class="row"><div class="field"><label>両替する日本円 <span class="hint">（円）</span></label><input type="number" id="yen" value="100000" min="0" inputmode="numeric"></div>
    <div class="field"><label>為替レート <span class="hint">（円/1通貨）</span></label><input type="number" id="rate" value="150" min="0.01" step="0.01" inputmode="decimal"></div></div>
    <div class="field"><label>両替手数料 <span class="hint">（％）</span></label><input type="number" id="fee" value="3" min="0" max="20" step="0.1" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">受取額を見る</button>''',
  result='''      <div class="label">受け取れる外貨</div>
      <div class="big"><span id="big">0</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">実質レート</div><div class="v" id="real">—</div></div>
      <div class="stat"><div class="k">手数料額</div><div class="v accent" id="feeY">—</div></div>
      <div class="stat"><div class="k">手数料なしなら</div><div class="v" id="nofee">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>受取外貨 ＝ 円 ÷ レート ×（1 − 手数料率）<br>実質レート ＝ 円 ÷ 受取外貨</div>
    <p>「手数料無料」をうたっていても、レートに上乗せ（スプレッド）されていることが多いです。実質レートで比べるのが正解。海外ATMやデビット、両替アプリなど方法で差が出ます。</p>
    <h2>よくある質問</h2>'''+faq([('どこが安い？','一般に空港より街中・専門両替所、カード系が有利なことが多いです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const yenA=Math.max(0,+$('yen').value||0),rate=Math.max(0.01,+$('rate').value||1),fee=Math.max(0,+$('fee').value||0)/100;
    const recv=yenA/rate*(1-fee),nofee=yenA/rate,real=recv>0?yenA/recv:0;
    $('big').textContent=num(recv);$('sub').textContent=`${num(yenA)}円・レート${rate}・手数料${(fee*100).toFixed(1)}％`;
    $('real').textContent=real.toFixed(2)+'円';$('feeY').textContent=yen(yenA*fee);$('nofee').textContent=num(nofee);
    SHARE=`外貨両替シミュ、${num(yenA)}円が手数料込みで約${num(recv)}（実質レート${real.toFixed(2)}円）でした💱\\n手数料、地味に効く…！👇`;show();anim($('big'),0,recv,900);}''')

add(id='camp-hiyou', cat='旅行・おでかけ', emoji='⛺',
  title='キャンプ装備 元取りシミュレーター｜何泊で元が取れる？｜シミュラボ',
  desc='キャンプ装備一式の購入費と、1泊のキャンプ場代・ホテル代から、装備の元が取れる泊数と年間の節約を試算する無料シミュレーター。',
  ogtitle='キャンプ装備 元取り｜何泊で元が取れる？', ogdesc='装備費とホテルとの差額から、元取り泊数を試算。',
  h1='キャンプ装備 元取りシミュレーター',
  lead='キャンプ装備、買っても元取れる？装備一式の費用と、ホテル泊との差額から、何泊で元が取れるか・年間の節約を出します。アウトドアデビューの後押しに。',
  inputs='''    <h2>⛺ 条件を入れる</h2>
    <div class="row"><div class="field"><label>装備一式の購入費 <span class="hint">（円）</span></label><input type="number" id="gear" value="150000" min="0" inputmode="numeric"></div>
    <div class="field"><label>年のキャンプ泊数 <span class="hint">（泊）</span></label><input type="number" id="freq" value="6" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>1泊のキャンプ場代 <span class="hint">（円）</span></label><input type="number" id="camp" value="3000" min="0" inputmode="numeric"></div>
    <div class="field"><label>ホテルなら1泊 <span class="hint">（円）</span></label><input type="number" id="hotel" value="12000" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">元取りを見る</button>''',
  result='''      <div class="label">元が取れる泊数</div>
      <div class="big"><span id="big">0</span><span class="unit">泊</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1泊あたりの節約</div><div class="v" id="diff">—</div></div>
      <div class="stat"><div class="k">今のペースで</div><div class="v accent" id="years">—</div></div>
      <div class="stat"><div class="k">年間の節約</div><div class="v" id="year">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>1泊の節約 ＝ ホテル代 − キャンプ場代<br>元取り泊数 ＝ 装備費 ÷ 1泊の節約</div>
    <p>キャンプは初期投資が大きいですが、回数を重ねるほどお得に。レンタルで試してから買う、中古やセールを活用する、で初期費用を抑えられます。何より自然の中の時間はプライスレス。</p>
    <h2>よくある質問</h2>'''+faq([('道具が増えて結局高くつく？','ハマると沼…。最初は最小限から揃えるのがおすすめです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const gear=Math.max(0,+$('gear').value||0),freq=Math.max(0,+$('freq').value||0),camp=Math.max(0,+$('camp').value||0),hotel=Math.max(0,+$('hotel').value||0);
    const diff=Math.max(1,hotel-camp),be=gear/diff,years=freq>0?be/freq:0;
    $('sub').textContent=`装備${num(gear)}円・1泊の差${num(hotel-camp)}円`;$('diff').textContent=yen(hotel-camp);$('years').textContent=num(years)+'年';$('year').textContent=yen(diff*freq);
    SHARE=`キャンプ装備 元取りシミュ、約${num(be)}泊（今のペースで${num(years)}年）で元が取れる計算でした⛺\\n自然の時間はプライスレス！👇`;show();anim($('big'),0,be,900);}''')

# ===== 住まい・暮らし =====
add(id='koushinryo', cat='住まい・暮らし', emoji='📋',
  title='更新料 生涯コストシミュレーター｜賃貸の更新料、一生でいくら？｜シミュラボ',
  desc='家賃と更新料（家賃の何ヶ月分か）・更新間隔・住む年数から、一生で払う更新料の総額を試算する無料シミュレーター。',
  ogtitle='更新料 生涯コスト｜更新料、一生でいくら？', ogdesc='家賃と更新間隔から、生涯の更新料総額を試算。',
  h1='更新料 生涯コストシミュレーター',
  lead='2年ごとにやってくる更新料。家賃・更新料の月数・住む年数から、一生で払う更新料の総額を出します（更新料なし物件との比較にも）。',
  inputs='''    <h2>📋 条件を入れる</h2>
    <div class="row"><div class="field"><label>家賃 <span class="hint">（円/月）</span></label><input type="number" id="rent" value="80000" min="0" inputmode="numeric"></div>
    <div class="field"><label>更新料 <span class="hint">（家賃の◯ヶ月分）</span></label><input type="number" id="months" value="1" min="0" max="3" step="0.5" inputmode="decimal"></div></div>
    <div class="row"><div class="field"><label>更新の間隔 <span class="hint">（年）</span></label><input type="number" id="span" value="2" min="1" inputmode="numeric"></div>
    <div class="field"><label>賃貸に住む年数 <span class="hint">（年）</span></label><input type="number" id="yr" value="40" min="1" max="80" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">生涯コストを見る</button>''',
  result='''      <div class="label">一生で払う更新料</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">更新の回数</div><div class="v" id="cnt">—</div></div>
      <div class="stat"><div class="k">1回あたり</div><div class="v" id="per">—</div></div>
      <div class="stat"><div class="k">月割にすると</div><div class="v accent" id="mo">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>更新回数 ＝ 住む年数 ÷ 更新間隔<br>生涯コスト ＝ 家賃 × 更新料の月数 × 更新回数</div>
    <p>更新料は地域や物件で有無・金額が異なります（関西は不要なことも）。長く住むほど積み上がるので、更新料なし物件は隠れたお得ポイント。引っ越し費用とあわせて比較を。</p>
    <h2>よくある質問</h2>'''+faq([('更新料は必ず払う？','契約によります。なし物件や交渉余地があることも。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const rent=Math.max(0,+$('rent').value||0),months=Math.max(0,+$('months').value||0),span=Math.max(1,+$('span').value||1),yr=Math.max(1,+$('yr').value||1);
    const cnt=Math.floor(yr/span),per=rent*months,total=per*cnt;
    $('sub').textContent=`家賃${num(rent)}円・${months}ヶ月分・${span}年ごと・${yr}年`;$('cnt').textContent=cnt+'回';$('per').textContent=yen(per);$('mo').textContent=yen(total/(yr*12));
    SHARE=`更新料 生涯コストシミュ、一生で約${yen(total)}（${cnt}回）でした📋\\n更新料なし物件、お得かも…！👇`;show();anim($('big'),0,total,900);}''')

add(id='kaden-denkidai', cat='住まい・暮らし', emoji='🔌',
  title='家電別 電気代シミュレーター｜あの家電、年いくら？｜シミュラボ',
  desc='家電の種類と電気単価から、その家電にかかる年間・10年の電気代の目安を表示する無料シミュレーター。',
  ogtitle='家電別 電気代｜あの家電、年いくら？', ogdesc='家電の種類と電気単価から、年間電気代を表示。',
  h1='家電別 電気代シミュレーター',
  lead='エアコン、冷蔵庫、こたつ…どの家電が電気を食う？家電を選ぶと、年間・10年の電気代の目安が分かります。買い替えや使い方の見直しに。',
  inputs='''    <h2>🔌 条件を選ぶ</h2>
    <div class="field"><label>家電</label><select id="kwh"><option value="800">エアコン(よく使う)</option><option value="300" selected>冷蔵庫</option><option value="200">照明(LED・家全体)</option><option value="150">テレビ(毎日)</option><option value="100">温水洗浄便座</option><option value="250">こたつ(冬)</option><option value="180">乾燥機付き洗濯機</option></select></div>
    <div class="field"><label>電気単価 <span class="hint">（円/kWh）</span></label><input type="number" id="price" value="31" min="0" step="0.1" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">電気代を見る</button>''',
  result='''      <div class="label">年間の電気代</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1ヶ月あたり</div><div class="v" id="mo">—</div></div>
      <div class="stat"><div class="k">10年で</div><div class="v accent" id="y10">—</div></div>
      <div class="stat"><div class="k">年間消費電力</div><div class="v" id="kwhv">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>年間電気代 ＝ 年間消費電力(kWh) × 電気単価</div>
    <p>消費電力が大きいのはエアコン・冷蔵庫・暖房系。古い家電は最新の省エネモデルより電気代が高いことも多く、買い替えで元が取れるケースもあります。使い方の見直しも効果的。</p>
    <h2>よくある質問</h2>'''+faq([('正確な値？','使用時間・機種で変わる目安です。実際の消費電力で入れるとより正確です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const kwh=+$('kwh').value||0,price=Math.max(0,+$('price').value||0);const year=kwh*price;
    $('sub').textContent=`${sel('kwh').text}・${price}円/kWh`;$('mo').textContent=yen(year/12);$('y10').textContent=yen(year*10);$('kwhv').textContent=num(kwh)+'kWh';
    SHARE=`家電別 電気代シミュ、${sel('kwh').text}は年${yen(year)}でした🔌\\n意外と電気代かかる…！👇`;show();anim($('big'),0,year,900);}''')

add(id='mizu-setsuyaku', cat='住まい・暮らし', emoji='💧',
  title='節水 効果シミュレーター｜節水で年いくら浮く？｜シミュラボ',
  desc='1日の節水量と水道・下水の単価から、節水で1年・10年にどれだけ水道代が浮くかを試算する無料シミュレーター。',
  ogtitle='節水 効果シミュレーター｜年いくら浮く？', ogdesc='1日の節水量から、節水で浮く水道代を試算。',
  h1='節水 効果シミュレーター',
  lead='シャワーを少し短く、節水シャワーヘッドに——その効果は年でいくら？1日の節水量と水道単価から、節水で浮く金額を出します。',
  inputs='''    <h2>💧 条件を入れる</h2>
    <div class="row"><div class="field"><label>1日の節水量 <span class="hint">（L・世帯合計）</span></label><input type="number" id="l" value="50" min="0" inputmode="numeric"></div>
    <div class="field"><label>水道+下水の単価 <span class="hint">（円/L・目安0.24）</span></label><input type="number" id="price" value="0.24" min="0" step="0.01" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">節約額を見る</button>''',
  result='''      <div class="label">年間の節約額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1ヶ月あたり</div><div class="v" id="mo">—</div></div>
      <div class="stat"><div class="k">10年で</div><div class="v accent" id="y10">—</div></div>
      <div class="stat"><div class="k">年間の節水量</div><div class="v" id="lv">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>年間の節約 ＝ 1日の節水量 × 単価 × 365<br>（水道+下水で1L ≒ 0.24円が一つの目安）</div>
    <p>シャワー1分で約10L。家族でこまめに意識すると、年間ではまとまった節約に。節水シャワーヘッドや食洗機（手洗いより節水）も効果的。環境にもやさしい習慣です。</p>
    <h2>よくある質問</h2>'''+faq([('食洗機は節水？','手洗いより少ない水で洗えることが多く、節水・時短になります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const l=Math.max(0,+$('l').value||0),price=Math.max(0,+$('price').value||0);const year=l*price*365;
    $('sub').textContent=`1日${num(l)}L × ${price}円 × 365`;$('mo').textContent=yen(year/12);$('y10').textContent=yen(year*10);$('lv').textContent=num(l*365)+'L';
    SHARE=`節水 効果シミュ、1日${num(l)}Lの節水で年${yen(year)}・10年で${yen(year*10)}浮く計算でした💧\\n環境にもお財布にも◎👇`;show();anim($('big'),0,year,900);}''')

# ===== グルメ・食 =====
add(id='shokuhi-tekisei', cat='グルメ・食', emoji='🍚',
  title='適正食費シミュレーター｜うちの食費、使いすぎ？｜シミュラボ',
  desc='手取り月収と世帯人数から、無理のない適正食費の目安（エンゲル係数ベース）と1日あたりの食費を表示する無料シミュレーター。',
  ogtitle='適正食費シミュレーター｜食費、使いすぎ？', ogdesc='手取りと人数から、適正な食費の目安を表示。',
  h1='適正食費シミュレーター',
  lead='食費って、いくらまでが適正？手取り月収と世帯人数から、無理のない食費の目安（エンゲル係数の考え方）を出します。家計の見直しに。',
  inputs='''    <h2>🍚 条件を入れる</h2>
    <div class="row"><div class="field"><label>手取り月収 <span class="hint">（円・世帯）</span></label><input type="number" id="income" value="250000" min="0" inputmode="numeric"></div>
    <div class="field"><label>世帯人数 <span class="hint">（人）</span></label><input type="number" id="n" value="1" min="1" max="10" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">適正食費を見る</button>''',
  result='''      <div class="label">適正食費の目安（月）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1日あたり</div><div class="v accent" id="day">—</div></div>
      <div class="stat"><div class="k">1人あたり(月)</div><div class="v" id="per">—</div></div>
      <div class="stat"><div class="k">目安の割合</div><div class="v" id="rate">—</div></div></div>''',
  article='''    <h2>エンゲル係数の考え方</h2>
    <div class="note"><strong>目安</strong><br>食費は手取りの15〜20％が一つの目安（単身は外食が増え高めになりがち）。<br>本ツールは手取りの約15％を基準にしています。</div>
    <p>食費は「削りすぎない」のも大事。健康とのバランスを取りつつ、外食・中食・自炊の比率を見直すと、満足度を保ったまま適正化できます。</p>
    <h2>よくある質問</h2>'''+faq([('外食込み？','はい。食に使う総額の目安です。自炊中心なら下げられます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const income=Math.max(0,+$('income').value||0),n=Math.max(1,+$('n').value||1);
    const rate=n===1?0.16:0.15;const month=income*rate;
    $('sub').textContent=`手取り${num(income)}円・${n}人`;$('day').textContent=yen(month/30.4);$('per').textContent=yen(month/n);$('rate').textContent=Math.round(rate*100)+'％';
    SHARE=`適正食費シミュ、我が家の目安は月${yen(month)}（1日${yen(month/30.4)}）でした🍚\\nうちは使いすぎ？👇`;show();anim($('big'),0,month,900);}''')

add(id='osake-shogai', cat='グルメ・食', emoji='🍶',
  title='一生で飲むお酒シミュレーター｜生涯でどれだけ飲む？｜シミュラボ',
  desc='1週間に飲むお酒の杯数とこれからの年数から、一生で飲むお酒の杯数・量・金額を計算するエンタメシミュレーター。',
  ogtitle='一生で飲むお酒｜生涯でどれだけ飲む？', ogdesc='週の杯数から、一生で飲むお酒の量と金額を計算。',
  h1='一生で飲むお酒シミュレーター',
  lead='晩酌に飲み会…一生でどれだけお酒を飲むんだろう？週の杯数とこれからの年数から、生涯の杯数・量・金額を出します（飲みすぎ注意のきっかけにも）。',
  inputs='''    <h2>🍶 条件を入れる</h2>
    <div class="row"><div class="field"><label>1週間に飲む杯数 <span class="hint">（杯）</span></label><input type="number" id="week" value="7" min="0" inputmode="numeric"></div>
    <div class="field"><label>これからの年数 <span class="hint">（年）</span></label><input type="number" id="yr" value="40" min="1" max="70" inputmode="numeric"></div></div>
    <div class="field"><label>1杯の値段 <span class="hint">（円・金額の計算用）</span></label><input type="number" id="price" value="500" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">一生分を見る</button>''',
  result='''      <div class="label">一生で飲む杯数</div>
      <div class="big"><span id="big">0</span><span class="unit">杯</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">お酒代の総額</div><div class="v accent" id="money">—</div></div>
      <div class="stat"><div class="k">中ジョッキ何杯分(L)</div><div class="v" id="litre">—</div></div>
      <div class="stat"><div class="k">1年で</div><div class="v" id="year">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>生涯の杯数 ＝ 週の杯数 × 52 × 年数</div>
    <p>楽しいお酒も、生涯にするとかなりの量と金額に。適量を守れば人生の楽しみ、飲みすぎは健康とお財布の敵。休肝日を作るだけでも、量・金額・健康に大きな差が出ます。</p>
    <h2>よくある質問</h2>'''+faq([('適量は？','一般に1日ビール中瓶1本程度が目安。週2日の休肝日が推奨されます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const week=Math.max(0,+$('week').value||0),yr=Math.max(1,+$('yr').value||1),price=Math.max(0,+$('price').value||0);
    const cups=week*52*yr,money=cups*price,litre=cups*0.35;
    $('sub').textContent=`週${week}杯 × ${yr}年`;$('money').textContent=yen(money);$('litre').textContent=num(litre)+'L';$('year').textContent=num(week*52)+'杯';
    SHARE=`一生で飲むお酒シミュ、生涯${num(cups)}杯・${yen(money)}分でした🍶\\n適量で長く楽しも…！👇`;show();anim($('big'),0,cups,900);}''')

add(id='okashi-nenkan', cat='グルメ・食', emoji='🍫',
  title='お菓子・間食 年間費シミュレーター｜おやつ代、年いくら？｜シミュラボ',
  desc='1日のお菓子・間食代から、年間・10年でいくら使っているかと、摂取カロリーの目安を計算する無料シミュレーター。',
  ogtitle='お菓子・間食 年間費｜おやつ代、年いくら？', ogdesc='1日のおやつ代から、年間費と摂取カロリーを計算。',
  h1='お菓子・間食 年間費シミュレーター',
  lead='ついつい買っちゃうお菓子、年でいくら？1日の間食代から、年間・10年の費用と、摂取カロリーの目安を出します。お財布にも体にも、ちょっと意識を。',
  inputs='''    <h2>🍫 条件を入れる</h2>
    <div class="row"><div class="field"><label>1日のお菓子・間食代 <span class="hint">（円）</span></label><input type="number" id="day" value="300" min="0" inputmode="numeric"></div>
    <div class="field"><label>1日の間食カロリー <span class="hint">（kcal・目安）</span></label><input type="number" id="kcal" value="200" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">年間費を見る</button>''',
  result='''      <div class="label">年間のお菓子・間食代</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">10年で</div><div class="v accent" id="y10">—</div></div>
      <div class="stat"><div class="k">年間の摂取カロリー</div><div class="v" id="kcalY">—</div></div>
      <div class="stat"><div class="k">脂肪にすると(年)</div><div class="v" id="fat">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>年間費 ＝ 1日の間食代 × 365<br>年間カロリー ＝ 1日の間食kcal × 365</div>
    <p>1日300円・200kcalでも、1年では約11万円・7.3万kcal。間食は心の栄養でもあるので、ゼロにせず「質と量」を意識するのが続くコツ。たまのご褒美おやつは大切に。</p>
    <h2>よくある質問</h2>'''+faq([('間食はダメ？','適量なら問題なし。ナッツや果物など質を選ぶのもおすすめです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const day=Math.max(0,+$('day').value||0),kcal=Math.max(0,+$('kcal').value||0);const year=day*365,kcalY=kcal*365;
    $('sub').textContent=`1日${num(day)}円・${num(kcal)}kcal`;$('y10').textContent=yen(year*10);$('kcalY').textContent=num(kcalY)+'kcal';$('fat').textContent=num(kcalY/7.2/1000)+'kg';
    SHARE=`お菓子・間食 年間費シミュ、年${yen(year)}・摂取${num(kcalY)}kcalでした🍫\\nおやつは質と量で…！👇`;show();anim($('big'),0,year,900);}''')

# ===== 美容・ファッション =====
add(id='kutsu-shogai', cat='美容・ファッション', emoji='👜',
  title='靴・バッグ 生涯コストシミュレーター｜一生でいくら買う？｜シミュラボ',
  desc='毎月の靴・バッグ代とこれからの年数から、一生でかかる費用と買う個数の目安を計算するエンタメシミュレーター。',
  ogtitle='靴・バッグ 生涯コスト｜一生でいくら買う？', ogdesc='月の靴・バッグ代から、生涯の費用と個数を計算。',
  h1='靴・バッグ 生涯コストシミュレーター',
  lead='お気に入りの靴やバッグ、一生でどれだけ買う？毎月の予算とこれからの年数から、生涯の費用と個数を出します。お気に入りを長く使うきっかけに。',
  inputs='''    <h2>👜 条件を入れる</h2>
    <div class="row"><div class="field"><label>1ヶ月の靴・バッグ代 <span class="hint">（円）</span></label><input type="number" id="m" value="5000" min="0" inputmode="numeric"></div>
    <div class="field"><label>これからの年数 <span class="hint">（年）</span></label><input type="number" id="yr" value="50" min="1" max="80" inputmode="numeric"></div></div>
    <div class="field"><label>1点の平均価格 <span class="hint">（円・個数の計算用）</span></label><input type="number" id="price" value="8000" min="1" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">生涯コストを見る</button>''',
  result='''      <div class="label">一生で靴・バッグに使うお金</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">買う個数</div><div class="v accent" id="cnt">—</div></div>
      <div class="stat"><div class="k">年間</div><div class="v" id="year">—</div></div>
      <div class="stat"><div class="k">10年で</div><div class="v" id="y10">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>生涯コスト ＝ 月の予算 × 12 × 年数／個数 ＝ 生涯コスト ÷ 1点の価格</div>
    <p>数より「長く使える良いもの」を選ぶと、満足度を保ちつつトータルでお得なことも。お手入れして長持ちさせる、使わないものはフリマで循環させる、も賢い選択です。</p>
    <h2>よくある質問</h2>'''+faq([('高い物のほうが得？','長く使えるなら結果的にお得なことも。使用頻度で「1回あたりコスト」を考えると◎。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const m=Math.max(0,+$('m').value||0),yr=Math.max(1,+$('yr').value||1),price=Math.max(1,+$('price').value||1);
    const total=m*12*yr,cnt=total/price;
    $('sub').textContent=`月${num(m)}円 × ${yr}年`;$('cnt').textContent=num(cnt)+'点';$('year').textContent=yen(m*12);$('y10').textContent=yen(m*12*10);
    SHARE=`靴・バッグ 生涯コストシミュ、一生で約${yen(total)}・${num(cnt)}点でした👜\\nお気に入りを長く使お…！👇`;show();anim($('big'),0,total,900);}''')

add(id='gym-motodori', cat='美容・ファッション', emoji='🏋️',
  title='ジム会費 元取りシミュレーター｜1回あたりいくら通えてる？｜シミュラボ',
  desc='ジムの月会費と月の利用回数から、1回あたりの単価と「都度払いと比べてお得か」を判定する無料シミュレーター。',
  ogtitle='ジム会費 元取り｜1回あたりいくら？', ogdesc='月会費と利用回数から、1回あたりの単価を計算。',
  h1='ジム会費 元取りシミュレーター',
  lead='ジムの会費、ちゃんと通って元取れてる？月会費と利用回数から、1回あたりの単価を計算。幽霊会員になっていないかチェックしましょう。',
  inputs='''    <h2>🏋️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>月会費 <span class="hint">（円）</span></label><input type="number" id="fee" value="8000" min="0" inputmode="numeric"></div>
    <div class="field"><label>月の利用回数 <span class="hint">（回）</span></label><input type="number" id="n" value="8" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>都度払いの相場 <span class="hint">（円/回・比較用）</span></label><input type="number" id="drop" value="2500" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">1回あたりを見る</button>''',
  result='''      <div class="label">1回あたりの単価</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">判定</div><div class="v accent" id="judge">—</div></div>
      <div class="stat"><div class="k">元取りライン</div><div class="v" id="be">—</div></div>
      <div class="stat"><div class="k">年会費</div><div class="v" id="year">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>1回あたり ＝ 月会費 ÷ 月の利用回数<br>都度払い相場より安ければ「元が取れている」</div>
    <p>会費は通っても通わなくても同じ。1回あたりの単価が都度払いより高いなら、通う回数を増やすか、都度払い・回数券への切り替えも検討を。「行く仕組み」づくりが継続のコツ。</p>
    <h2>よくある質問</h2>'''+faq([('幽霊会員かも…','利用0回だと単価は無限大。通うか、解約・プラン変更の見直しを。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const fee=Math.max(0,+$('fee').value||0),n=Math.max(0,+$('n').value||0),drop=Math.max(1,+$('drop').value||1);
    const per=n>0?fee/n:Infinity,be=fee/drop;
    let j=n===0?'幽霊会員…👻':(per<=drop?'元取れてる◎':'もっと通お…！');
    $('sub').textContent=`月会費${num(fee)}円・月${n}回`;$('big').textContent=isFinite(per)?num(per):'∞';$('judge').textContent=j;$('be').textContent='月'+Math.ceil(be)+'回';$('year').textContent=yen(fee*12);
    SHARE=`ジム会費 元取りシミュ、私は1回あたり${isFinite(per)?yen(per):'∞'}でした🏋️（${j}）\\nちゃんと通お…！👇`;show();if(isFinite(per))anim($('big'),0,per,900);}''')

add(id='supple-nenkan', cat='美容・ファッション', emoji='💊',
  title='サプリ・美容ドリンク 年間費シミュレーター｜美容習慣、年いくら？｜シミュラボ',
  desc='毎日のサプリ・美容ドリンク・プロテインなどの費用から、年間・10年でいくらかかるかを計算する無料シミュレーター。',
  ogtitle='サプリ・美容ドリンク 年間費｜年いくら？', ogdesc='1日のサプリ・美容ドリンク代から、年間費を計算。',
  h1='サプリ・美容ドリンク 年間費シミュレーター',
  lead='毎日のサプリや美容ドリンク、続けると年でいくら？1日あたりの費用から、年間・10年のコストを出します。続ける価値の見極めに。',
  inputs='''    <h2>💊 条件を入れる</h2>
    <div class="field"><label>1日のサプリ・美容ドリンク代 <span class="hint">（円・合計）</span></label><input type="number" id="day" value="300" min="0" inputmode="numeric"></div>
    <div class="field"><label>続ける年数 <span class="hint">（年）</span></label><input type="number" id="yr" value="10" min="1" max="60" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">年間費を見る</button>''',
  result='''      <div class="label">年間のサプリ・美容費</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1ヶ月あたり</div><div class="v" id="mo">—</div></div>
      <div class="stat"><div class="k">続ける年数で</div><div class="v accent" id="total">—</div></div>
      <div class="stat"><div class="k">1日あたり</div><div class="v" id="dv">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>年間費 ＝ 1日の費用 × 365</div>
    <p>サプリは「続けてこそ」のものが多く、トータルでは大きな投資に。本当に効果を実感できているか、食事で摂れないかを時々見直すと、ムダなく続けられます。基本は食事から、が王道。</p>
    <h2>よくある質問</h2>'''+faq([('サプリは必要？','基本は食事から。不足分を補う位置づけがおすすめです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const day=Math.max(0,+$('day').value||0),yr=Math.max(1,+$('yr').value||1);const year=day*365,total=year*yr;
    $('sub').textContent=`1日${num(day)}円 × 365 × ${yr}年`;$('mo').textContent=yen(year/12);$('total').textContent=yen(total);$('dv').textContent=yen(day);
    SHARE=`サプリ・美容ドリンク 年間費シミュ、年${yen(year)}・${yr}年で${yen(total)}でした💊\\n続ける価値、見極めよ…！👇`;show();anim($('big'),0,year,900);}''')

if __name__=='__main__':
    write_all(SIMS)
    print(f'batch3 done. {len(SIMS)} sims.')
