# -*- coding: utf-8 -*-
"""シミュラボ：SEO強化 新規20本（重複なし・詳細本文＋リッチアニメ）。
   gen_sims11のTPL(write_all)を再利用。すべてCTAなしカテゴリに投入。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq, write_all

FIN='マネー・保険・不動産'; MONEY='お金・時間'; TAX='税金・確定申告'; WORK='仕事・働き方'
HEALTH='健康・カラダ'; CAR='クルマ・乗り物'; LIFE='人生・自分ごと'; MANNER='冠婚葬祭・贈り物'; KIDS='子ども・育児'
SIMS=[]
def add(**k): SIMS.append(k)
def C(t): return '<div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：'+t+'</div>'
def REF(items): return '<h2>参考</h2><ul class="seo-refs">'+''.join('<li>'+i+'</li>' for i in items)+'</ul>'

# ===== 1. 固定資産税 =====
add(id='kotei-shisanzei', cat=FIN, emoji='🏘️',
  title='固定資産税 計算｜評価額から年間の税額をシミュレーション｜シミュラボ',
  desc='土地・建物の固定資産税評価額から、固定資産税・都市計画税の年額や住宅用地の軽減後の税額を概算する無料シミュレーター。',
  ogtitle='固定資産税 計算｜評価額から年税額は？', ogdesc='評価額から固定資産税・都市計画税の年額を概算（住宅用地軽減対応）。',
  h1='固定資産税 計算シミュレーター',
  lead='土地・建物の評価額から、毎年かかる固定資産税の目安を計算します。住宅用地の軽減（1/6）にも対応した概算ツールです。',
  inputs='''    <h2>🏘️ 評価額を入れる</h2>
    <div class="row"><div class="field"><label>土地の評価額 <span class="hint">（万円）</span></label><input type="number" id="land" value="1200" min="0" inputmode="numeric"></div>
    <div class="field"><label>建物の評価額 <span class="hint">（万円）</span></label><input type="number" id="bld" value="800" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>土地の種類</label><select id="kind"><option value="1" selected>住宅用地（小規模・1/6軽減）</option><option value="0">非住宅・更地</option></select></div>
    <button class="btn btn-primary" id="calcBtn">固定資産税を計算する</button>''',
  result='''      <div class="label">固定資産税（年・目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">うち都市計画税</div><div class="v" id="toshi">—</div></div>
      <div class="stat"><div class="k">1期あたり(÷4)</div><div class="v accent" id="ki">—</div></div>
      <div class="stat"><div class="k">課税標準(土地)</div><div class="v" id="hyo">—</div></div></div>''',
  article=C('固定資産税は <b>課税標準額 × 1.4%</b>。住宅用地は課税標準が <b>1/6</b>（小規模住宅用地）に軽減され、税額が大きく下がります。')+'''
    <h2>固定資産税の計算方法</h2>
    <p>固定資産税は、土地・家屋の「固定資産税評価額」をもとに計算され、毎年1月1日時点の所有者に課税されます。標準税率は1.4%。あわせて市街化区域では都市計画税（最大0.3%）もかかります。住宅が建つ土地（住宅用地）は税負担が軽くなる特例があります。</p>
    <div class="note"><strong>計算式</strong><br>固定資産税 ＝ 課税標準額 × 1.4%<br>都市計画税 ＝ 課税標準額 × 0.3%<br>住宅用地（200㎡まで）は課税標準が固定資産税1/6・都市計画税1/3</div>
    <h2>軽減のポイント</h2>
    <table class="seo-table"><tr><th>区分</th><th>固定資産税</th><th>都市計画税</th></tr>
    <tr><td>小規模住宅用地(〜200㎡)</td><td>1/6</td><td>1/3</td></tr>
    <tr><td>一般住宅用地(200㎡超)</td><td>1/3</td><td>2/3</td></tr>
    <tr><td>非住宅・更地</td><td>軽減なし</td><td>軽減なし</td></tr></table>
    <p>新築住宅は一定期間、建物分の税額が1/2に減額される特例もあります。本ツールは概算で、実際は自治体の評価・負担調整措置で変わります。</p>
    <h2>よくある質問</h2>'''+faq([
    ('評価額はどこで分かる？','毎年送られる「課税明細書」や、市区町村の固定資産課税台帳で確認できます。'),
    ('いつ払う？','多くの自治体で年4回（6月・9月・12月・翌2月ごろ）の分割納付です。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['総務省「固定資産税」','各自治体の住宅用地特例']),
  js='''  function calc(){const land=Math.max(0,+$('land').value||0)*10000,bld=Math.max(0,+$('bld').value||0)*10000,res=$('kind').value==='1';
    const landBase=res?land/6:land, toshiLand=res?land/3:land;
    const koteichi=(landBase+bld)*0.014, toshi=(toshiLand+bld)*0.003, total=koteichi+toshi;
    $('sub').textContent=`土地${num(land/10000)}万・建物${num(bld/10000)}万・${res?'住宅用地':'非住宅'}`;
    $('toshi').textContent=yen(toshi);$('ki').textContent=yen(total/4);$('hyo').textContent=yen(landBase);
    show();anim($('big'),0,total,800);
    SHARE=`固定資産税シミュ、年 約${yen(total)}（1期${yen(total/4)}）の計算でした🏘️`;}''')

# ===== 2. 住宅ローン控除 =====
add(id='loan-koujo', cat=FIN, emoji='🏠',
  title='住宅ローン控除 計算｜年末残高から減税額・戻る税金は？｜シミュラボ',
  desc='年末のローン残高と控除率・控除期間から、住宅ローン控除（住宅ローン減税）で戻ってくる税金の年額・総額を概算する無料シミュレーター。',
  ogtitle='住宅ローン控除 計算｜いくら戻る？', ogdesc='年末ローン残高から住宅ローン控除の年額・総額を概算。',
  h1='住宅ローン控除 計算シミュレーター',
  lead='住宅ローン控除（減税）でいくら戻る？年末のローン残高・控除率・残りの控除年数から、戻ってくる税金の目安を計算します。',
  inputs='''    <h2>🏠 条件を入れる</h2>
    <div class="row"><div class="field"><label>年末のローン残高 <span class="hint">（万円）</span></label><input type="number" id="zan" value="3000" min="0" inputmode="numeric"></div>
    <div class="field"><label>控除率 <span class="hint">（%）</span></label><input type="number" id="rate" value="0.7" min="0" max="1" step="0.1" inputmode="decimal"></div></div>
    <div class="field"><label>残りの控除年数 <span class="hint">（年・最大13）</span></label><input type="number" id="yrs" value="13" min="1" max="13" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">控除額を計算する</button>''',
  result='''      <div class="label">今年戻る税金（目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">控除期間の総額</div><div class="v accent" id="total">—</div></div>
      <div class="stat"><div class="k">月あたり換算</div><div class="v" id="mo">—</div></div>
      <div class="stat"><div class="k">控除率</div><div class="v" id="rv">—</div></div></div>
      <div class="anim-bar" id="bw"><span id="bar"></span><b id="bl"></b></div>
      <div class="anim-cap">控除期間の進み（最大13年）</div>''',
  article=C('住宅ローン控除は <b>年末ローン残高 × 0.7%</b>（最大13年）が、所得税・住民税から戻ります。残高が減るほど控除額も小さくなります。')+'''
    <h2>住宅ローン控除のしくみ</h2>
    <p>住宅ローン控除（住宅ローン減税）は、年末時点のローン残高の0.7%が、その年の所得税（引ききれない分は住民税の一部）から差し引かれる制度です。新築の認定住宅などは控除期間が13年。住宅性能や入居年で借入限度額が異なります。</p>
    <div class="note"><strong>計算式</strong><br>年間の控除額 ＝ 年末ローン残高 × 0.7%<br>（払った所得税・住民税が上限。残高が減ると控除も減少）</div>
    <p>戻る額は「実際に納めた税額」が上限です。納税額より控除可能額が大きい場合、満額は戻りません。本ツールは残高×控除率の概算です。</p>
    <h2>よくある質問</h2>'''+faq([
    ('初年度の手続きは？','初年度は確定申告が必要です。2年目以降は会社員なら年末調整で手続きできます。'),
    ('中古住宅でも使える？','一定の要件（築年数・耐震基準など）を満たせば利用できます。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['国税庁「住宅借入金等特別控除」','国土交通省 住宅ローン減税']),
  js='''  function calc(){const z=Math.max(0,+$('zan').value||0)*10000,r=Math.max(0,+$('rate').value||0.7)/100,y=Math.max(1,Math.min(13,+$('yrs').value||13));
    const year=z*r, total=year*y;
    $('sub').textContent=`残高${num(z/10000)}万円・控除率${(r*100).toFixed(1)}%`;
    $('total').textContent=yen(total);$('mo').textContent=yen(year/12);$('rv').textContent=(r*100).toFixed(1)+'%';
    const pct=Math.round((13-y)/13*100);$('bar').style.width='0%';setTimeout(()=>{$('bar').style.width=pct+'%';},40);$('bl').textContent='残'+y+'年';
    show();anim($('big'),0,year,800);
    SHARE=`住宅ローン控除シミュ、今年 約${yen(year)}・残り${y}年で総額 約${yen(total)}戻る計算でした🏠`;}''')

# ===== 3. 預金利息 =====
add(id='yokin-risoku', cat=FIN, emoji='🏦',
  title='預金利息 計算｜金利と期間から利息・税引後の受取額は？｜シミュラボ',
  desc='預入額・年利・期間から、預金の利息（単利・複利）と税金（20.315%）を引いた受取額を計算する無料シミュレーター。',
  ogtitle='預金利息 計算｜税引後でいくら増える？', ogdesc='預入額・金利・期間から利息と税引後の受取額を計算。',
  h1='預金利息 計算シミュレーター',
  lead='預金でいくら増える？預入額・年利・期間から、利息と、税金（20.315%）を引いたあとの受取額を計算します。複利・単利に対応。',
  inputs='''    <h2>🏦 条件を入れる</h2>
    <div class="row"><div class="field"><label>預入額 <span class="hint">（万円）</span></label><input type="number" id="p" value="100" min="0" inputmode="numeric"></div>
    <div class="field"><label>年利 <span class="hint">（%）</span></label><input type="number" id="r" value="0.2" min="0" step="0.01" inputmode="decimal"></div></div>
    <div class="row"><div class="field"><label>期間 <span class="hint">（年）</span></label><input type="number" id="y" value="5" min="1" inputmode="numeric"></div>
    <div class="field"><label>方式</label><select id="m"><option value="c" selected>複利（年1回）</option><option value="s">単利</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">利息を計算する</button>''',
  result='''      <div class="label">税引後の利息</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">受取総額</div><div class="v accent" id="recv">—</div></div>
      <div class="stat"><div class="k">税引前の利息</div><div class="v" id="pre">—</div></div>
      <div class="stat"><div class="k">税金(20.315%)</div><div class="v" id="zei">—</div></div></div>''',
  article=C('利息は複利なら <b>元本×((1+年利)^年数 − 1)</b>。利息には <b>20.315%</b> の税金がかかり、受取額はその分減ります。')+'''
    <h2>預金利息の計算方法</h2>
    <p>利息の付き方には「単利（元本にのみ利息）」と「複利（利息にも利息）」があります。多くの定期預金は複利です。さらに利息には所得税・住民税あわせて20.315%が源泉徴収されます。</p>
    <div class="note"><strong>計算式</strong><br>複利：受取利息 ＝ 元本 ×（(1+年利)^年数 − 1）<br>単利：受取利息 ＝ 元本 × 年利 × 年数<br>税引後 ＝ 利息 ×（1 − 0.20315）</div>
    <p>低金利では利息はわずかですが、金利・期間・複利の効果を確認できます。インフレ下では実質価値が目減りする点にも注意。</p>
    <h2>よくある質問</h2>'''+faq([
    ('税金は自動で引かれる？','預金利息は源泉分離課税で、受取時に自動で20.315%が差し引かれます。確定申告は原則不要です。'),
    ('複利と単利どちらが得？','同じ金利なら複利が有利です。期間が長いほど差が広がります。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['金融広報中央委員会「金利・複利」','国税庁 利子所得']),
  js='''  function calc(){const p=Math.max(0,+$('p').value||0)*10000,r=Math.max(0,+$('r').value||0)/100,y=Math.max(1,+$('y').value||1),c=$('m').value==='c';
    const pre=c?p*(Math.pow(1+r,y)-1):p*r*y, zei=pre*0.20315, net=pre-zei;
    $('sub').textContent=`${num(p/10000)}万円・年利${(r*100)}%・${y}年・${c?'複利':'単利'}`;
    $('recv').textContent=yen(p+net);$('pre').textContent=yen(pre);$('zei').textContent=yen(zei);
    show();anim($('big'),0,net,800);
    SHARE=`預金利息シミュ、${num(p/10000)}万円を年利${r*100}%で${y}年→税引後利息 約${yen(net)}でした🏦`;}''')

# ===== 4. クレジット分割手数料 =====
add(id='credit-bunkatsu', cat=MONEY, emoji='💳',
  title='クレジット分割手数料 計算｜分割払いの手数料はいくら？｜シミュラボ',
  desc='利用金額・分割回数・実質年率から、クレジットカード分割払いの手数料総額と毎月の支払額を計算する無料シミュレーター。',
  ogtitle='分割払い手数料 計算｜総額いくら増える？', ogdesc='利用額・回数・実質年率から分割手数料と月々の支払を計算。',
  h1='クレジット分割手数料 計算',
  lead='クレジットの分割払い、手数料はいくら？利用金額・分割回数・実質年率から、手数料の総額と毎月の支払額を計算します。',
  inputs='''    <h2>💳 条件を入れる</h2>
    <div class="row"><div class="field"><label>利用金額 <span class="hint">（円）</span></label><input type="number" id="p" value="120000" min="0" inputmode="numeric"></div>
    <div class="field"><label>分割回数 <span class="hint">（回）</span></label><input type="number" id="n" value="12" min="1" max="60" inputmode="numeric"></div></div>
    <div class="field"><label>実質年率 <span class="hint">（%・目安12〜15）</span></label><input type="number" id="r" value="15" min="0" max="20" step="0.1" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">手数料を計算する</button>''',
  result='''      <div class="label">手数料の総額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">毎月の支払</div><div class="v accent" id="mo">—</div></div>
      <div class="stat"><div class="k">支払総額</div><div class="v" id="total">—</div></div>
      <div class="stat"><div class="k">手数料率(対利用額)</div><div class="v" id="hr">—</div></div></div>''',
  article=C('分割払いは <b>実質年率（約12〜15%）</b>の手数料がかかります。回数が多いほど手数料も増えます。1回・2回・ボーナス一括は通常無料です。')+'''
    <h2>分割手数料の考え方</h2>
    <p>分割払いの手数料は、残高に対して実質年率で計算されます。本ツールは元利均等の利息計算で手数料総額を概算します（カード会社の「100円あたりの手数料」表とは多少差が出ます）。</p>
    <div class="note"><strong>計算式（概算）</strong><br>毎月の支払 ＝ 元利均等返済額（残高×月利ベース）<br>手数料総額 ＝ 支払総額 − 利用金額</div>
    <p>3回以上の分割は手数料がかかるのが一般的。大きな買い物は、手数料無料の「2回払い」や「ボーナス一括」、または貯めてから一括が有利です。リボ払いはさらに高コストになりがちです。</p>
    <h2>よくある質問</h2>'''+faq([
    ('1回・2回払いは手数料ある？','通常は無料です。手数料がかかるのは3回払い以上が一般的です。'),
    ('リボ払いとの違いは？','分割は回数固定、リボは毎月一定額。リボは残高が減りにくく手数料が膨らみやすいです。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['日本クレジット協会「分割払い・手数料」']),
  js='''  function calc(){const p=Math.max(0,+$('p').value||0),n=Math.max(1,+$('n').value||1),r=Math.max(0,+$('r').value||0)/100/12;
    let mo,total; if(r<=0){mo=p/n;}else{const f=r*Math.pow(1+r,n)/(Math.pow(1+r,n)-1);mo=p*f;} total=mo*n; const fee=total-p;
    $('sub').textContent=`${num(p)}円・${n}回・実質年率${$('r').value}%`;
    $('mo').textContent=yen(mo);$('total').textContent=yen(total);$('hr').textContent=(p>0?(fee/p*100).toFixed(1):0)+'%';
    show();anim($('big'),0,fee,800);
    SHARE=`分割手数料シミュ、${num(p)}円を${n}回払い→手数料 約${yen(fee)}（総額${yen(total)}）でした💳`;}''')

# ===== 5. 固定費見直し =====
add(id='koteihi', cat=MONEY, emoji='📉',
  title='固定費 見直し 節約シミュレーター｜年間・生涯でいくら浮く？｜シミュラボ',
  desc='スマホ・保険・サブスクなどの月額削減額から、固定費見直しで浮くお金を年間・10年・30年で計算する無料シミュレーター。',
  ogtitle='固定費 見直し 節約｜生涯でいくら浮く？', ogdesc='スマホ・保険・サブスクの削減額から年間・生涯の節約額を計算。',
  h1='固定費 見直し 節約シミュレーター',
  lead='固定費を見直すと、生涯ではいくら浮く？スマホ・保険・サブスクなどの「月の削減額」から、年間・10年・30年の節約額を計算します。',
  inputs='''    <h2>📉 月の削減見込みを入れる</h2>
    <div class="row"><div class="field"><label>スマホ・通信 <span class="hint">（円/月）</span></label><input type="number" id="a" value="3000" min="0" inputmode="numeric"></div>
    <div class="field"><label>保険の見直し <span class="hint">（円/月）</span></label><input type="number" id="b" value="2000" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>サブスク解約 <span class="hint">（円/月）</span></label><input type="number" id="c" value="1500" min="0" inputmode="numeric"></div>
    <div class="field"><label>その他 <span class="hint">（円/月）</span></label><input type="number" id="d" value="0" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">節約額を見る</button>''',
  result='''      <div class="label">30年でうく金額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">月の削減</div><div class="v accent" id="mo">—</div></div>
      <div class="stat"><div class="k">年間</div><div class="v" id="yr">—</div></div>
      <div class="stat"><div class="k">10年</div><div class="v" id="y10">—</div></div></div>''',
  article=C('固定費は「一度の見直しで効果がずっと続く」のが最大の強み。月 <b>たった数千円</b> の削減でも、30年では <b>数百万円</b> の差になります。')+'''
    <h2>固定費見直しが最強の節約な理由</h2>
    <p>食費や娯楽費の節約は毎回がまんが必要ですが、固定費（通信・保険・サブスクなど）は一度見直せば、あとは何もしなくても効果が続きます。とくにスマホの格安SIMへの乗り換え、保険の払いすぎ、使っていないサブスクの解約は効果が大きい定番です。</p>
    <div class="note"><strong>計算式</strong><br>年間 ＝ 月の削減額 × 12／30年 ＝ 月の削減額 × 360<br>（運用に回せばさらに大きく）</div>
    <h2>見直しの優先順位</h2>
    <table class="seo-table"><tr><th>項目</th><th>削減のめやす</th></tr>
    <tr><td>スマホ（格安SIM）</td><td>月3,000〜5,000円</td></tr>
    <tr><td>生命保険・医療保険</td><td>月2,000〜5,000円</td></tr>
    <tr><td>使っていないサブスク</td><td>月1,000〜3,000円</td></tr>
    <tr><td>電力・ガスの乗り換え</td><td>月500〜2,000円</td></tr></table>
    <h2>よくある質問</h2>'''+faq([
    ('何から見直すべき？','金額が大きく手間が一度きりの「スマホ」「保険」から始めるのが効率的です。'),
    ('浮いたお金はどうする？','つみたて投資に回すと、複利でさらに大きな差になります。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['金融庁「家計管理・固定費の見直し」']),
  js='''  function calc(){const m=['a','b','c','d'].reduce((s,id)=>s+Math.max(0,+$(id).value||0),0);
    const yr=m*12, y10=m*120, y30=m*360;
    $('sub').textContent=`月の削減 合計 ${yen(m)}`;$('mo').textContent=yen(m);$('yr').textContent=yen(yr);$('y10').textContent=yen(y10);
    show();anim($('big'),0,y30,900);
    SHARE=`固定費見直しシミュ、月${yen(m)}の削減で30年 約${yen(y30)}も浮く計算でした📉`;}''')

# ===== 6. 生命保険料控除 =====
add(id='seiho-koujo', cat=TAX, emoji='🛡️',
  title='生命保険料控除 計算｜年末調整で戻る税金はいくら？｜シミュラボ',
  desc='一般・介護医療・個人年金の年間保険料から、生命保険料控除の額と、戻ってくる税金（所得税・住民税）の目安を計算する無料シミュレーター。',
  ogtitle='生命保険料控除 計算｜いくら戻る？', ogdesc='3区分の保険料から控除額と節税額を計算（新制度）。',
  h1='生命保険料控除 計算シミュレーター',
  lead='生命保険料控除で税金はいくら戻る？「一般・介護医療・個人年金」の年間保険料から、控除額と節税額の目安を計算します（新制度）。',
  inputs='''    <h2>🛡️ 年間保険料を入れる</h2>
    <div class="row"><div class="field"><label>一般生命保険 <span class="hint">（円/年）</span></label><input type="number" id="a" value="80000" min="0" inputmode="numeric"></div>
    <div class="field"><label>介護医療保険 <span class="hint">（円/年）</span></label><input type="number" id="b" value="50000" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>個人年金保険 <span class="hint">（円/年）</span></label><input type="number" id="c" value="80000" min="0" inputmode="numeric"></div>
    <div class="field"><label>所得税率</label><select id="r"><option value="0.05">5%</option><option value="0.10" selected>10%</option><option value="0.20">20%</option><option value="0.23">23%</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">控除額・節税額を見る</button>''',
  result='''      <div class="label">節税額（所得税＋住民税）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">所得税の控除</div><div class="v accent" id="sho">—</div></div>
      <div class="stat"><div class="k">住民税の控除</div><div class="v" id="ju">—</div></div>
      <div class="stat"><div class="k">控除の合計(所得税)</div><div class="v" id="koujo">—</div></div></div>''',
  article=C('新制度では3区分（一般・介護医療・個人年金）ごとに所得税 <b>最大4万円</b>・住民税最大2.8万円。合計で所得税 <b>最大12万円</b> の控除になります。')+'''
    <h2>生命保険料控除のしくみ（新制度）</h2>
    <p>2012年以降の契約は「新制度」で、一般生命・介護医療・個人年金の3区分。各区分ごとに、年間保険料に応じて所得税で最大4万円（住民税で最大2.8万円）が控除されます。3区分合計の上限は所得税12万円・住民税7万円です。</p>
    <div class="note"><strong>控除額（所得税・新制度）</strong><br>年2万円以下＝全額／2万〜4万＝÷2＋1万／4万〜8万＝÷4＋2万／8万超＝一律4万円<br>節税 ≒ 控除合計 ×（所得税率＋住民税10%）</div>
    <p>会社員は年末調整で、控除証明書を提出すれば手続きできます。本ツールは概算です。</p>
    <h2>よくある質問</h2>'''+faq([
    ('旧制度との違いは？','旧制度（2011年以前）は一般・年金の2区分で各最大5万円。新旧の合算上限は所得税12万円です。'),
    ('証明書はどこで？','秋ごろに保険会社から「控除証明書」が届きます。年末調整や確定申告で使います。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['国税庁「生命保険料控除」']),
  js='''  function ko(p){if(p<=20000)return p;if(p<=40000)return p/2+10000;if(p<=80000)return p/4+20000;return 40000;}
  function koJu(p){if(p<=12000)return p;if(p<=32000)return p/2+6000;if(p<=56000)return p/4+14000;return 28000;}
  function calc(){const a=Math.max(0,+$('a').value||0),b=Math.max(0,+$('b').value||0),c=Math.max(0,+$('c').value||0),r=+$('r').value||0.1;
    const ks=Math.min(120000,ko(a)+ko(b)+ko(c)), kj=Math.min(70000,koJu(a)+koJu(b)+koJu(c));
    const sho=ks*r, ju=kj*0.10, total=sho+ju;
    $('sub').textContent=`保険料 計${yen(a+b+c)}・税率${Math.round(r*100)}%`;
    $('sho').textContent=yen(sho);$('ju').textContent=yen(ju);$('koujo').textContent=yen(ks);
    show();anim($('big'),0,total,800);
    SHARE=`生命保険料控除シミュ、節税額 約${yen(total)}（控除${yen(ks)}）の計算でした🛡️`;}''')

# ===== 7. 印紙税 =====
add(id='inshizei', cat=TAX, emoji='📜',
  title='印紙税 計算｜契約書・領収書の収入印紙はいくら？｜シミュラボ',
  desc='契約金額と文書の種類（不動産売買・工事請負・領収書）から、必要な収入印紙の金額を調べる無料ツール。軽減税率にも対応。',
  ogtitle='印紙税 計算｜収入印紙はいくら？', ogdesc='契約金額と文書種類から必要な収入印紙額を判定。',
  h1='印紙税 計算ツール',
  lead='契約書や領収書に貼る収入印紙はいくら？契約金額と文書の種類から、必要な印紙税額を判定します（主要文書・概算）。',
  inputs='''    <h2>📜 条件を入れる</h2>
    <div class="row"><div class="field"><label>契約金額・記載金額 <span class="hint">（万円）</span></label><input type="number" id="amt" value="3000" min="0" inputmode="numeric"></div>
    <div class="field"><label>文書の種類</label><select id="kind"><option value="estate" selected>不動産売買契約書</option><option value="work">工事請負契約書</option><option value="receipt">領収書(売上代金)</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">印紙税を調べる</button>''',
  result='''      <div class="label">必要な収入印紙</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">文書の種類</div><div class="v accent" id="kn">—</div></div>
      <div class="stat"><div class="k">記載金額</div><div class="v" id="am">—</div></div>
      <div class="stat"><div class="k">区分</div><div class="v" id="band">—</div></div></div>''',
  article=C('印紙税は契約金額の<b>段階</b>で決まる定額です。不動産売買・建設工事の契約書は<b>軽減税率</b>が適用されます（領収書は5万円未満なら非課税）。')+'''
    <h2>印紙税とは</h2>
    <p>契約書や領収書など、決められた「課税文書」を作成すると印紙税がかかり、収入印紙を貼って納めます。金額は契約金額の段階ごとの定額で、不動産の譲渡・建設工事の請負契約書には軽減措置があります。</p>
    <h2>主な印紙税額（軽減後・抜粋）</h2>
    <table class="seo-table"><tr><th>契約金額</th><th>不動産売買/工事請負</th><th>領収書</th></tr>
    <tr><td>100万〜500万</td><td>1,000円</td><td>200円</td></tr>
    <tr><td>500万〜1,000万</td><td>5,000円</td><td>200円</td></tr>
    <tr><td>1,000万〜5,000万</td><td>10,000円</td><td>200円</td></tr>
    <tr><td>5,000万〜1億</td><td>30,000円</td><td>200円</td></tr></table>
    <p>領収書は記載金額5万円未満なら非課税。電子契約（電子データ）には印紙税がかからないため、電子化で節約できます。本ツールは主要文書の概算です。</p>
    <h2>よくある質問</h2>'''+faq([
    ('電子契約なら印紙不要？','はい。紙の文書でなく電子データのみなら印紙税はかかりません。'),
    ('貼り忘れたら？','過怠税として本来の3倍が課されることがあります。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['国税庁「印紙税額一覧表」']),
  js='''  function calc(){const a=Math.max(0,+$('amt').value||0)*10000,kind=$('kind').value;
    let tax=0,band='';
    if(kind==='receipt'){ if(a<50000){tax=0;band='5万未満(非課税)';}else if(a<=1000000){tax=200;band='〜100万';}else if(a<=2000000){tax=400;band='〜200万';}else if(a<=3000000){tax=600;band='〜300万';}else{tax=1000;band='300万超';} }
    else { // 不動産/工事 軽減
      if(a<=1000000){tax=500;band='〜100万';}else if(a<=5000000){tax=1000;band='〜500万';}else if(a<=10000000){tax=5000;band='〜1000万';}else if(a<=50000000){tax=10000;band='〜5000万';}else if(a<=100000000){tax=30000;band='〜1億';}else{tax=60000;band='1億超';}
    }
    const kn={estate:'不動産売買',work:'工事請負',receipt:'領収書'}[kind];
    $('sub').textContent=`${kn}・記載金額${num(a)}円`;$('kn').textContent=kn;$('am').textContent=yen(a);$('band').textContent=band;
    show();anim($('big'),0,tax,700);
    SHARE=`印紙税シミュ、${kn}（${num(a/10000)}万円）の収入印紙は ${yen(tax)} でした📜`;}''')

# ===== 8. 社会保険料 =====
add(id='shakaihoken-ryou', cat=WORK, emoji='🩺',
  title='社会保険料 計算｜給与から引かれる健康保険・厚生年金は？｜シミュラボ',
  desc='月給と年齢から、給与天引きされる社会保険料（健康保険・厚生年金・雇用保険・介護保険）の本人負担額の目安を計算する無料シミュレーター。',
  ogtitle='社会保険料 計算｜給与天引きはいくら？', ogdesc='月給・年齢から健康保険・厚生年金などの本人負担を概算。',
  h1='社会保険料 計算シミュレーター',
  lead='毎月の給料から引かれる社会保険料はいくら？月給と年齢から、健康保険・厚生年金・雇用保険・介護保険の本人負担の目安を計算します。',
  inputs='''    <h2>🩺 条件を入れる</h2>
    <div class="row"><div class="field"><label>月給（額面） <span class="hint">（万円）</span></label><input type="number" id="g" value="30" min="0" inputmode="numeric"></div>
    <div class="field"><label>年齢</label><select id="age"><option value="0" selected>40歳未満</option><option value="1">40〜64歳（介護あり）</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">社会保険料を計算する</button>''',
  result='''      <div class="label">毎月の社会保険料（本人負担）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">健康保険＋介護</div><div class="v" id="kenpo">—</div></div>
      <div class="stat"><div class="k">厚生年金</div><div class="v accent" id="nenkin">—</div></div>
      <div class="stat"><div class="k">雇用保険</div><div class="v" id="koyou">—</div></div></div>
      <div class="anim-bar" id="bw"><span id="bar"></span><b id="bl"></b></div>
      <div class="anim-cap">月給に占める社会保険料の割合</div>''',
  article=C('会社員の社会保険料（本人負担）は、月給の <b>約14〜15%</b>。健康保険・厚生年金・雇用保険（40歳以上は介護保険も）の合計で、会社が同額前後を負担しています。')+'''
    <h2>社会保険料の内訳（本人負担の目安）</h2>
    <table class="seo-table"><tr><th>保険</th><th>本人負担率(概算)</th></tr>
    <tr><td>健康保険</td><td>約5.0%</td></tr>
    <tr><td>介護保険(40〜64歳)</td><td>約0.9%</td></tr>
    <tr><td>厚生年金</td><td>9.15%</td></tr>
    <tr><td>雇用保険</td><td>0.6%</td></tr></table>
    <div class="note"><strong>ポイント</strong><br>厚生年金・健康保険は「標準報酬月額」で決まり、4〜6月の給与で1年分が決まります（残業が多いと高くなることも）。会社も同程度を負担しています。</div>
    <p>本ツールは概算です（健康保険料率は加入する協会・組合や都道府県で異なります）。</p>
    <h2>よくある質問</h2>'''+faq([
    ('4〜6月は残業しない方がいい？','この時期の給与で標準報酬月額（＝保険料）が決まるため、残業が多いと保険料が上がることがあります。'),
    ('会社負担はいくら？','健康保険・厚生年金は労使折半。会社も本人とほぼ同額を負担しています。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['全国健康保険協会（協会けんぽ）保険料率','日本年金機構 厚生年金保険料']),
  js='''  function calc(){const g=Math.max(0,+$('g').value||0)*10000,kaigo=$('age').value==='1';
    const kenpoR=0.05+(kaigo?0.009:0), kenpo=g*kenpoR, nenkin=g*0.0915, koyou=g*0.006, total=kenpo+nenkin+koyou;
    $('sub').textContent=`月給${num(g/10000)}万円・${kaigo?'40〜64歳':'40歳未満'}`;
    $('kenpo').textContent=yen(kenpo);$('nenkin').textContent=yen(nenkin);$('koyou').textContent=yen(koyou);
    const pct=g>0?Math.round(total/g*100):0;$('bar').style.width='0%';setTimeout(()=>{$('bar').style.width=pct+'%';},40);$('bl').textContent=pct+'%';
    show();anim($('big'),0,total,800);
    SHARE=`社会保険料シミュ、月給${num(g/10000)}万円なら毎月 約${yen(total)}（月給の${pct}%）引かれる計算でした🩺`;}''')

# ===== 9. 傷病手当金 =====
add(id='shoubyo-teate', cat=WORK, emoji='🤒',
  title='傷病手当金 計算｜病気・けがで休んだら いくらもらえる？｜シミュラボ',
  desc='標準報酬月額（月給）と休んだ日数から、健康保険の傷病手当金の日額・総額の目安を計算する無料シミュレーター。',
  ogtitle='傷病手当金 計算｜休職中いくらもらえる？', ogdesc='月給と休んだ日数から傷病手当金の日額・総額を概算。',
  h1='傷病手当金 計算シミュレーター',
  lead='病気やけがで働けず休んだとき、健康保険からもらえる「傷病手当金」。月給と休む日数から、受け取れる目安を計算します。',
  inputs='''    <h2>🤒 条件を入れる</h2>
    <div class="row"><div class="field"><label>月給（標準報酬月額の目安） <span class="hint">（万円）</span></label><input type="number" id="g" value="30" min="0" inputmode="numeric"></div>
    <div class="field"><label>連続して休む日数 <span class="hint">（日）</span></label><input type="number" id="d" value="60" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">もらえる額を見る</button>''',
  result='''      <div class="label">傷病手当金の総額（目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1日あたり</div><div class="v accent" id="day">—</div></div>
      <div class="stat"><div class="k">支給される日数</div><div class="v" id="days">—</div></div>
      <div class="stat"><div class="k">最初の3日間</div><div class="v" id="machi">—</div></div></div>''',
  article=C('傷病手当金は <b>標準報酬日額 × 2/3 × 支給日数</b>。連続3日休んだ後（待期）、4日目から支給され、通算 <b>最長1年6か月</b> 受け取れます。')+'''
    <h2>傷病手当金のしくみ</h2>
    <p>会社員（健康保険の被保険者）が、業務外の病気・けがで働けず給与が出ないとき、健康保険から支給されるのが傷病手当金です。連続して3日間休む「待期」を満たすと、4日目から支給されます。</p>
    <div class="note"><strong>計算式</strong><br>標準報酬日額 ＝ 標準報酬月額 ÷ 30<br>1日の支給額 ＝ 標準報酬日額 × 2/3<br>総額 ＝ 1日の支給額 ×（休んだ日数 − 待期3日）</div>
    <p>支給期間は支給開始から「通算」で最長1年6か月。会社から給与が一部出る場合は差額調整されます。本ツールは概算です。</p>
    <h2>よくある質問</h2>'''+faq([
    ('待期3日とは？','連続して3日間仕事を休むこと（有給・公休でもOK）。これを満たすと4日目から支給対象です。'),
    ('退職後ももらえる？','一定の条件（継続して1年以上の加入など）を満たせば、退職後も受給を続けられる場合があります。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['全国健康保険協会「傷病手当金」']),
  js='''  function calc(){const g=Math.max(0,+$('g').value||0)*10000,d=Math.max(0,+$('d').value||0);
    const dayAmt=g/30*2/3, pay=Math.max(0,d-3), total=dayAmt*pay;
    $('sub').textContent=`月給${num(g/10000)}万円・休み${d}日`;
    $('day').textContent=yen(dayAmt);$('days').textContent=pay+'日';$('machi').textContent='待期(無給)';
    show();anim($('big'),0,total,800);
    SHARE=`傷病手当金シミュ、月給${num(g/10000)}万円で${d}日休むと 約${yen(total)}（日額${yen(dayAmt)}）もらえる計算でした🤒`;}''')

# ===== 10. 雇用保険料 =====
add(id='koyouhoken', cat=WORK, emoji='🧮',
  title='雇用保険料 計算｜給与から引かれる雇用保険はいくら？｜シミュラボ',
  desc='月給・賞与と業種から、給与天引きされる雇用保険料（本人負担）の月額・年額を計算する無料シミュレーター。',
  ogtitle='雇用保険料 計算｜本人負担はいくら？', ogdesc='月給と業種から雇用保険料の本人負担を計算。',
  h1='雇用保険料 計算シミュレーター',
  lead='給料から引かれる雇用保険料はいくら？月給と業種から、本人負担の月額・年額を計算します。',
  inputs='''    <h2>🧮 条件を入れる</h2>
    <div class="row"><div class="field"><label>月給（額面） <span class="hint">（万円）</span></label><input type="number" id="g" value="30" min="0" inputmode="numeric"></div>
    <div class="field"><label>業種</label><select id="biz"><option value="0.006" selected>一般の事業</option><option value="0.007">建設・農林水産・清酒製造</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">雇用保険料を計算する</button>''',
  result='''      <div class="label">毎月の雇用保険料（本人負担）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">年間の負担</div><div class="v accent" id="yr">—</div></div>
      <div class="stat"><div class="k">本人負担率</div><div class="v" id="rate">—</div></div>
      <div class="stat"><div class="k">月給</div><div class="v" id="gv">—</div></div></div>''',
  article=C('雇用保険料の本人負担は、賃金の <b>約0.6%</b>（一般の事業）。失業時の基本手当や育児休業給付などの財源になります。')+'''
    <h2>雇用保険料のしくみ</h2>
    <p>雇用保険料は、毎月の賃金（賞与含む）に保険料率をかけて計算され、本人と会社で負担します。本人負担率は一般の事業で0.6%、建設業など一部は0.7%です（料率は年度で見直されます）。</p>
    <div class="note"><strong>計算式</strong><br>雇用保険料（本人）＝ 賃金 × 本人負担率（0.6%）<br>失業給付・育児休業給付・教育訓練給付などの財源になります。</div>
    <p>健康保険・厚生年金と違い、雇用保険料は標準報酬月額ではなく「実際の賃金」に毎月かかります。本ツールは月給ベースの概算です。</p>
    <h2>よくある質問</h2>'''+faq([
    ('賞与にもかかる？','はい。賞与にも同じ率で雇用保険料がかかります。'),
    ('何に使われる？','失業時の基本手当、育児休業給付金、教育訓練給付などの財源です。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['厚生労働省「雇用保険料率」']),
  js='''  function calc(){const g=Math.max(0,+$('g').value||0)*10000,r=+$('biz').value||0.006;
    const mo=g*r, yr=mo*12;
    $('sub').textContent=`月給${num(g/10000)}万円・本人負担率${(r*100).toFixed(1)}%`;
    $('yr').textContent=yen(yr);$('rate').textContent=(r*100).toFixed(1)+'%';$('gv').textContent=yen(g);
    show();anim($('big'),0,mo,700);
    SHARE=`雇用保険料シミュ、月給${num(g/10000)}万円で毎月 約${yen(mo)}（年${yen(yr)}）でした🧮`;}''')

# ===== 11. 純アルコール量 =====
add(id='junalcohol', cat=HEALTH, emoji='🍺',
  title='純アルコール量 計算｜お酒の適量は？1日20gの目安をチェック｜シミュラボ',
  desc='お酒の種類・度数・量から、純アルコール量（グラム）を計算し、生活習慣病リスクが上がるとされる1日20gの目安と比べる無料ツール。',
  ogtitle='純アルコール量 計算｜お酒の適量は？', ogdesc='種類・度数・量から純アルコール量を計算し適量(20g)と比較。',
  h1='純アルコール量 計算ツール',
  lead='そのお酒、純アルコールにすると何グラム？種類・度数・量から純アルコール量を計算し、「節度ある適量＝1日20g」の目安と比べます。',
  inputs='''    <h2>🍺 飲んだお酒を入れる</h2>
    <div class="row"><div class="field"><label>お酒の種類</label><select id="kind"><option value="5">ビール(5%)</option><option value="5">缶チューハイ(5%)</option><option value="12">ワイン(12%)</option><option value="15" selected>日本酒(15%)</option><option value="25">焼酎(25%)</option><option value="40">ウイスキー(40%)</option></select></div>
    <div class="field"><label>量 <span class="hint">（ml）</span></label><input type="number" id="ml" value="180" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">純アルコール量を見る</button>''',
  result='''      <div class="label">純アルコール量</div>
      <div class="big"><span id="big">0</span><span class="unit">g</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">適量(20g)比</div><div class="v accent" id="hiritsu">—</div></div>
      <div class="stat"><div class="k">分解時間の目安</div><div class="v" id="time">—</div></div>
      <div class="stat"><div class="k">判定</div><div class="v" id="judge">—</div></div></div>
      <div class="anim-bar" id="bw"><span id="bar"></span><b id="bl"></b></div>
      <div class="anim-cap">1日の適量(純アルコール20g)に対する割合</div>''',
  article=C('純アルコール量 ＝ <b>量(ml) × 度数(%) ÷ 100 × 0.8</b>。生活習慣病のリスクが上がるとされる目安は <b>1日20g</b>（ビール中瓶1本相当）です。')+'''
    <h2>純アルコール量の計算</h2>
    <p>お酒の強さは種類で大きく違います。健康への影響は「純アルコール量（グラム）」で見るのが基本。厚生労働省は、生活習慣病のリスクを高める飲酒量を「1日あたり純アルコールで男性40g・女性20g以上」とし、節度ある適量を約20gとしています。</p>
    <div class="note"><strong>計算式</strong><br>純アルコール量(g) ＝ 量(ml) × 度数(%) ÷ 100 × 0.8（アルコール比重）</div>
    <h2>お酒の種類別 純アルコール量（目安）</h2>
    <table class="seo-table"><tr><th>お酒</th><th>量</th><th>純アルコール</th></tr>
    <tr><td>ビール(5%)</td><td>500ml</td><td>約20g</td></tr>
    <tr><td>日本酒(15%)</td><td>180ml(1合)</td><td>約22g</td></tr>
    <tr><td>ワイン(12%)</td><td>180ml</td><td>約17g</td></tr>
    <tr><td>焼酎(25%)</td><td>100ml</td><td>約20g</td></tr></table>
    <p>分解にかかる時間は体重・体質で差があります（本ツールは体重60kgでの概算）。休肝日をつくることも大切です。</p>
    <h2>よくある質問</h2>'''+faq([
    ('適量はどれくらい？','節度ある適度な飲酒は1日純アルコール約20gとされます。女性や高齢者は少なめが推奨されます。'),
    ('分解時間の目安は？','体重60kgで純アルコール約1gあたり0.12時間が目安。個人差が大きいので運転は絶対に避けましょう。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['厚生労働省「健康日本21・飲酒のガイドライン」','e-ヘルスネット 純アルコール量']),
  js='''  function calc(){const d=+$('kind').value||5,ml=Math.max(0,+$('ml').value||0);
    const g=ml*d/100*0.8, ratio=g/20, hours=g*0.12;
    let j; if(g<=20)j='適量の範囲'; else if(g<=40)j='やや多め'; else j='飲みすぎ注意';
    $('sub').textContent=`度数${d}%・${ml}ml`;
    $('hiritsu').textContent=Math.round(ratio*100)+'%';$('time').textContent='約'+hours.toFixed(1)+'時間';$('judge').textContent=j;
    const pct=Math.min(100,Math.round(ratio*100));$('bar').style.width='0%';setTimeout(()=>{$('bar').style.width=pct+'%';},40);$('bl').textContent=g.toFixed(1)+'g';
    show();anim($('big'),0,g,800,1);
    SHARE=`純アルコール量シミュ、このお酒は ${g.toFixed(1)}g（適量20gの${Math.round(ratio*100)}%）でした🍺 ${j}`;}''')

# ===== 12. 熱中症危険度(WBGT) =====
add(id='necchusho', cat=HEALTH, emoji='🥵',
  title='熱中症 危険度チェック｜気温と湿度からWBGT(暑さ指数)を計算｜シミュラボ',
  desc='気温と湿度から、熱中症の危険度を示すWBGT（暑さ指数）の目安を計算し、注意〜危険のレベルと対策を表示する無料ツール。',
  ogtitle='熱中症 危険度｜WBGT(暑さ指数)を計算', ogdesc='気温と湿度からWBGT(暑さ指数)と熱中症レベルを判定。',
  h1='熱中症 危険度チェック（WBGT）',
  lead='その暑さ、どれくらい危険？気温と湿度から、熱中症の指標「WBGT（暑さ指数）」の目安を計算し、注意〜危険のレベルを表示します。',
  inputs='''    <h2>🥵 気温と湿度を入れる</h2>
    <div class="row"><div class="field"><label>気温 <span class="hint">（℃）</span></label><input type="number" id="t" value="32" min="-10" max="50" inputmode="numeric"></div>
    <div class="field"><label>湿度 <span class="hint">（%）</span></label><input type="number" id="h" value="70" min="0" max="100" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">危険度を見る</button>''',
  result='''      <div class="label">WBGT（暑さ指数・目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">℃</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">危険レベル</div><div class="v accent" id="lv">—</div></div>
      <div class="stat"><div class="k">運動の目安</div><div class="v" id="undou">—</div></div>
      <div class="stat"><div class="k">対策</div><div class="v" id="taisaku">—</div></div></div>
      <div class="anim-bar" id="bw"><span id="bar"></span><b id="bl"></b></div>
      <div class="anim-cap">21:注意 25:警戒 28:厳重警戒 31:危険</div>''',
  article=C('熱中症は気温だけでなく<b>湿度</b>が大きく影響します。指標は <b>WBGT（暑さ指数）</b>。<b>28℃以上で厳重警戒、31℃以上は危険</b>で運動は原則中止です。')+'''
    <h2>WBGT（暑さ指数）とは</h2>
    <p>WBGTは、気温・湿度・輻射熱から算出する熱中症予防の指標です。湿度が高いと汗が蒸発しにくく、同じ気温でも危険度が上がります。本ツールは屋内・日射なしを想定した気温×湿度の概算式です（屋外の直射日光下ではさらに高くなります）。</p>
    <h2>WBGTと熱中症の危険度</h2>
    <table class="seo-table"><tr><th>WBGT</th><th>レベル</th><th>運動の目安</th></tr>
    <tr><td>21未満</td><td>ほぼ安全</td><td>適宜水分補給</td></tr>
    <tr><td>21〜25</td><td>注意</td><td>積極的に水分補給</td></tr>
    <tr><td>25〜28</td><td>警戒</td><td>積極的に休憩</td></tr>
    <tr><td>28〜31</td><td>厳重警戒</td><td>激しい運動は中止</td></tr>
    <tr><td>31以上</td><td>危険</td><td>運動は原則中止</td></tr></table>
    <p>のどが渇く前にこまめな水分・塩分補給を。室内でもエアコンを使い、高齢者や子どもは特に注意してください。体調不良時はすぐ涼しい場所で休みましょう。</p>
    <h2>よくある質問</h2>'''+faq([
    ('気温が低くても危険なことは？','湿度が非常に高いとWBGTは上がります。梅雨明けや体が暑さに慣れていない時期も注意です。'),
    ('屋外ではもっと高い？','直射日光下では本ツールの値より数℃高くなることがあります。環境省の実測値も確認しましょう。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['環境省「熱中症予防情報サイト（WBGT）」','日本スポーツ協会 熱中症予防運動指針']),
  js='''  function calc(){const t=+$('t').value||0,h=Math.max(0,Math.min(100,+$('h').value||0));
    let w=0.725*t+0.0368*h+0.00364*t*h-3.246; w=Math.round(w*10)/10;
    let lv,un,ta; if(w<21){lv='ほぼ安全';un='適宜水分';ta='水分補給';}else if(w<25){lv='注意';un='積極的に水分';ta='水分・休憩';}else if(w<28){lv='警戒';un='積極的に休憩';ta='こまめに休憩';}else if(w<31){lv='厳重警戒';un='激しい運動中止';ta='外出を控える';}else{lv='危険';un='運動は原則中止';ta='涼しい室内へ';}
    $('sub').textContent=`気温${t}℃・湿度${h}%`;$('lv').textContent=lv;$('undou').textContent=un;$('taisaku').textContent=ta;
    const pct=Math.min(100,Math.round(w/35*100));$('bar').style.width='0%';setTimeout(()=>{$('bar').style.width=pct+'%';},40);$('bl').textContent=w+'℃';
    show();anim($('big'),0,w,800,1);
    SHARE=`熱中症 危険度チェック、WBGT ${w}℃＝「${lv}」でした🥵 こまめな水分補給を！`;}''')

# ===== 13. 体感温度 =====
add(id='taikan-ondo', cat=HEALTH, emoji='🌡️',
  title='体感温度 計算｜湿度・風速から「暑い/寒い」体感を計算｜シミュラボ',
  desc='夏は湿度（蒸し暑さ）、冬は風速（風の冷たさ）から、実際に感じる体感温度の目安を計算する無料シミュレーター。',
  ogtitle='体感温度 計算｜湿度・風で何℃に感じる？', ogdesc='夏は湿度、冬は風速から体感温度の目安を計算。',
  h1='体感温度 計算シミュレーター',
  lead='同じ気温でも、湿度が高いと蒸し暑く、風が強いと寒く感じます。夏は湿度、冬は風速から「体感温度」の目安を計算します。',
  inputs='''    <h2>🌡️ 条件を入れる</h2>
    <div class="field"><label>季節モード</label><select id="mode"><option value="summer" selected>夏（湿度で計算）</option><option value="winter">冬（風速で計算）</option></select></div>
    <div class="row"><div class="field"><label>気温 <span class="hint">（℃）</span></label><input type="number" id="t" value="30" min="-20" max="50" inputmode="numeric"></div>
    <div class="field"><label id="lab2">湿度（%）</label><input type="number" id="x" value="80" min="0" max="100" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">体感温度を見る</button>''',
  result='''      <div class="label">体感温度（目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">℃</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">実際の気温</div><div class="v" id="real">—</div></div>
      <div class="stat"><div class="k">気温との差</div><div class="v accent" id="diff">—</div></div>
      <div class="stat"><div class="k">体感</div><div class="v" id="feel">—</div></div></div>''',
  article=C('体感温度は、夏は<b>湿度</b>（汗が蒸発しにくいと暑い）、冬は<b>風速</b>（風が体温を奪う）で変わります。風速1m/sにつき体感は約1℃下がるとされます。')+'''
    <h2>体感温度のしくみ</h2>
    <p>気温が同じでも、人が感じる暑さ・寒さは湿度や風で変わります。夏は湿度が高いと汗が蒸発できず暑く感じ（ミスナールの式）、冬は風が強いと体の熱が奪われて寒く感じます（ウインドチル）。</p>
    <div class="note"><strong>計算式（目安）</strong><br>夏（湿度）：体感 ＝ 気温 − 1/2.3 ×（気温−10）×（0.8 − 湿度/100）<br>冬（風速）：風速1m/sごとに体感が約1℃低下</div>
    <p>蒸し暑い日は熱中症に、風の強い寒い日は低体温・凍傷に注意。体感に合わせた服装・冷暖房を心がけましょう。本ツールは目安です。</p>
    <h2>よくある質問</h2>'''+faq([
    ('湿度が高いとなぜ暑い？','汗が蒸発するときに体の熱を奪いますが、湿度が高いと汗が蒸発しにくく、熱がこもって暑く感じます。'),
    ('風速1mで何℃下がる？','体感温度はおおむね風速1m/sにつき約1℃低く感じるとされます。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['ミスナールの体感温度式','気象庁 ウインドチル（風冷)']),
  js='''  document.getElementById('mode').addEventListener('change',function(){$('lab2').textContent=this.value==='summer'?'湿度（%）':'風速（m/s）';$('x').value=this.value==='summer'?80:5;});
  function calc(){const mode=$('mode').value,t=+$('t').value||0,x=Math.max(0,+$('x').value||0);
    let feel; if(mode==='summer'){feel=t-1/2.3*(t-10)*(0.8-x/100);}else{feel=t-x;}
    feel=Math.round(feel*10)/10; const diff=Math.round((feel-t)*10)/10;
    let f; if(feel>=30)f='かなり暑い'; else if(feel>=25)f='暑い'; else if(feel>=15)f='快適'; else if(feel>=5)f='肌寒い'; else f='寒い';
    $('sub').textContent=mode==='summer'?`気温${t}℃・湿度${x}%`:`気温${t}℃・風速${x}m/s`;
    $('real').textContent=t+'℃';$('diff').textContent=(diff>=0?'+':'')+diff+'℃';$('feel').textContent=f;
    show();anim($('big'),0,feel,800,1);
    SHARE=`体感温度シミュ、気温${t}℃でも体感は ${feel}℃（${f}）でした🌡️`;}''')

# ===== 14. タンパク質必要量 =====
add(id='tanpaku', cat=HEALTH, emoji='🍗',
  title='タンパク質 必要量 計算｜1日に何g必要？体重から計算｜シミュラボ',
  desc='体重と活動量（運動なし〜筋トレ）から、1日に必要なタンパク質の量（グラム）と、卵・鶏むね肉での換算量を計算する無料ツール。',
  ogtitle='タンパク質 必要量 計算｜1日に何g？', ogdesc='体重と運動量から1日のタンパク質必要量を計算。',
  h1='タンパク質 必要量 計算ツール',
  lead='1日に必要なタンパク質は何グラム？体重と運動量から計算し、卵や鶏むね肉だと何個・何g分かも表示します。',
  inputs='''    <h2>🍗 条件を入れる</h2>
    <div class="row"><div class="field"><label>体重 <span class="hint">（kg）</span></label><input type="number" id="w" value="60" min="0" inputmode="numeric"></div>
    <div class="field"><label>活動量</label><select id="act"><option value="0.9">運動しない（維持）</option><option value="1.4" selected>軽い運動・健康維持</option><option value="1.7">筋トレ・ダイエット中</option><option value="2.0">本格的な増量</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">必要量を計算する</button>''',
  result='''      <div class="seo-anim ptag-stage" id="stage"><div class="pop-emoji" id="meat">🍗</div></div>
      <div class="label">1日に必要なタンパク質</div>
      <div class="big"><span id="big">0</span><span class="unit">g</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">卵で換算</div><div class="v accent" id="egg">—</div></div>
      <div class="stat"><div class="k">鶏むね肉で</div><div class="v" id="chicken">—</div></div>
      <div class="stat"><div class="k">1食あたり</div><div class="v" id="meal">—</div></div></div>''',
  article=C('タンパク質の1日必要量は <b>体重1kgあたり約0.9〜2.0g</b>。運動量が多いほど多く必要で、<b>1食20〜30g</b>に分けて摂るのが効率的です。')+'''
    <h2>1日に必要なタンパク質</h2>
    <p>タンパク質は筋肉・臓器・肌・髪などの材料になる必須の栄養素。一般的な健康維持なら体重1kgあたり0.9〜1.0g、運動・ダイエット中は1.4〜1.7g、本格的に筋肉を増やすなら2.0g程度が目安です。</p>
    <div class="note"><strong>計算式</strong><br>1日の必要量(g) ＝ 体重(kg) × 係数(0.9〜2.0)<br>食品換算：卵1個＝約6g／鶏むね肉100g＝約23g</div>
    <h2>高タンパク食品の目安</h2>
    <table class="seo-table"><tr><th>食品</th><th>タンパク質</th></tr>
    <tr><td>卵 1個</td><td>約6g</td></tr>
    <tr><td>鶏むね肉 100g</td><td>約23g</td></tr>
    <tr><td>納豆 1パック</td><td>約8g</td></tr>
    <tr><td>ヨーグルト 100g</td><td>約4g</td></tr>
    <tr><td>プロテイン 1杯</td><td>約20g</td></tr></table>
    <p>一度に大量に摂っても吸収には限りがあるため、3食に分けてこまめに摂るのがおすすめです。腎臓に持病がある方は医師に相談を。</p>
    <h2>よくある質問</h2>'''+faq([
    ('摂りすぎは良くない？','余分なタンパク質はエネルギーとして使われたり排出されます。腎機能に不安がある人は摂りすぎ注意です。'),
    ('プロテインは必要？','食事で足りるのが理想ですが、不足分を手軽に補うのにプロテインは便利です。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['厚生労働省「日本人の食事摂取基準」たんぱく質']),
  js='''  function calc(){const w=Math.max(0,+$('w').value||0),act=+$('act').value||1.4;
    const g=w*act;
    $('sub').textContent=`体重${w}kg・係数${act}g/kg`;
    $('egg').textContent=Math.round(g/6)+'個';$('chicken').textContent=Math.round(g/23*100)+'g';$('meal').textContent=Math.round(g/3)+'g';
    const m=$('meat');m.classList.remove('on');void m.offsetWidth;m.classList.add('on');
    show();anim($('big'),0,g,800);
    SHARE=`タンパク質シミュ、私の1日の必要量は約${Math.round(g)}g（卵${Math.round(g/6)}個分）でした🍗`;}''')

# ===== 15. 自動車保険 等級 =====
add(id='jidoshahoken', cat=CAR, emoji='🚗',
  title='自動車保険 等級割引シミュレーター｜等級で保険料はいくら変わる？｜シミュラボ',
  desc='現在のノンフリート等級と基準保険料から、等級別の割引・割増後の保険料と、翌年の等級・保険料を計算する無料シミュレーター。',
  ogtitle='自動車保険 等級割引｜保険料はいくら？', ogdesc='等級と基準保険料から割引後の保険料を計算。',
  h1='自動車保険 等級割引シミュレーター',
  lead='自動車保険は「等級」で保険料が大きく変わります。今の等級と基準保険料から、割引後の保険料と、翌年の等級・保険料を計算します。',
  inputs='''    <h2>🚗 条件を入れる</h2>
    <div class="row"><div class="field"><label>現在の等級 <span class="hint">（1〜20）</span></label><input type="number" id="kyu" value="10" min="1" max="20" inputmode="numeric"></div>
    <div class="field"><label>基準保険料（6等級相当） <span class="hint">（円/年）</span></label><input type="number" id="base" value="80000" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">保険料を計算する</button>''',
  result='''      <div class="label">今年の保険料（目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">割引率</div><div class="v accent" id="rate">—</div></div>
      <div class="stat"><div class="k">来年(無事故)</div><div class="v" id="next">—</div></div>
      <div class="stat"><div class="k">来年の保険料</div><div class="v" id="nextp">—</div></div></div>''',
  article=C('自動車保険の等級は<b>1〜20等級</b>。事故がなければ毎年1等級上がり割引が増え、事故を起こすと3等級下がります。20等級は<b>約63%割引</b>です。')+'''
    <h2>ノンフリート等級制度とは</h2>
    <p>等級は、事故歴に応じて保険料が変わる仕組みです。新規契約は6等級から始まり、1年間無事故なら翌年1等級アップ。等級が上がるほど割引率が高くなります。事故で保険を使うと等級が下がり（3等級ダウン事故が基本）、数年間は割増になります。</p>
    <h2>等級別の割引・割増（目安）</h2>
    <table class="seo-table"><tr><th>等級</th><th>割引・割増(無事故)</th></tr>
    <tr><td>6等級</td><td>約 −19%（基準）</td></tr>
    <tr><td>10等級</td><td>約 −45%</td></tr>
    <tr><td>15等級</td><td>約 −53%</td></tr>
    <tr><td>20等級</td><td>約 −63%</td></tr></table>
    <p>等級は他社に乗り換えても引き継がれます。少額の事故は等級ダウンを避けて自費で直す方が、トータルで安くなる場合もあります。本ツールは概算です。</p>
    <h2>よくある質問</h2>'''+faq([
    ('事故を起こすと何等級下がる？','一般的な事故は3等級ダウン、当て逃げや盗難など一部は1等級ダウンです。'),
    ('20等級まで何年？','6等級から無事故なら毎年1つ上がるので、20等級まで最短14年です。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['損害保険料率算出機構 ノンフリート等級別料率']),
  js='''  function disc(k){const T={1:0.64,2:0.28,3:0.12,4:-0.02,5:-0.13,6:-0.19,7:-0.30,8:-0.40,9:-0.43,10:-0.45,11:-0.47,12:-0.48,13:-0.49,14:-0.50,15:-0.53,16:-0.55,17:-0.57,18:-0.59,19:-0.61,20:-0.63};return T[k]!==undefined?T[k]:-0.19;}
  function calc(){const k=Math.max(1,Math.min(20,+$('kyu').value||6)),base=Math.max(0,+$('base').value||0);
    const d=disc(k), p=base*(1+d), nk=Math.min(20,k+1), np=base*(1+disc(nk));
    $('sub').textContent=`${k}等級・基準${num(base)}円`;
    $('rate').textContent=(d<=0?'':'+')+Math.round(d*100)+'%';$('next').textContent=nk+'等級';$('nextp').textContent=yen(np);
    show();anim($('big'),0,p,800);
    SHARE=`自動車保険 等級シミュ、${k}等級なら年 約${yen(p)}（割引${Math.round(-d*100)}%）でした🚗`;}''')

# ===== 16. 駐車場 月極vsコインP =====
add(id='chushajo', cat=CAR, emoji='🅿️',
  title='駐車場 月極 vs コインパーキング｜どっちが得かシミュレーション｜シミュラボ',
  desc='月極駐車場の月額と、コインパーキングの1回料金・利用回数から、年間コストを比較してどちらが得かを計算する無料シミュレーター。',
  ogtitle='月極 vs コインP｜駐車場どっちが得？', ogdesc='月極とコインパーキングの年間コストを比較。',
  h1='駐車場 月極 vs コインパーキング',
  lead='車を停めるなら月極とコインパーキング、どっちが得？月極の月額と、コインパーキングの1回料金・利用回数から年間コストを比較します。',
  inputs='''    <h2>🅿️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>月極駐車場 <span class="hint">（円/月）</span></label><input type="number" id="m" value="15000" min="0" inputmode="numeric"></div>
    <div class="field"><label>コインP 1回の料金 <span class="hint">（円）</span></label><input type="number" id="c" value="800" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>1ヶ月にコインPを使う回数 <span class="hint">（回）</span></label><input type="number" id="n" value="12" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">どっちが得か見る</button>''',
  result='''      <div class="label">年間の差額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">月極(年)</div><div class="v" id="tuki">—</div></div>
      <div class="stat"><div class="k">コインP(年)</div><div class="v" id="coin">—</div></div>
      <div class="stat"><div class="k">お得なのは</div><div class="v accent" id="win">—</div></div></div>''',
  article=C('月極とコインパーキングの分岐点は<b>利用回数</b>。たまにしか乗らないならコインP、毎日乗るなら月極が有利になりやすいです。')+'''
    <h2>月極とコインパーキングの比較</h2>
    <p>月極駐車場は使っても使わなくても定額。コインパーキングは使った分だけですが、頻繁に使うと割高になります。「月に何回使うか」で損益が分かれます。</p>
    <div class="note"><strong>計算式</strong><br>月極（年）＝ 月額 × 12<br>コインP（年）＝ 1回料金 × 月の回数 × 12</div>
    <p>カーシェアという選択肢もあります。週末しか乗らない、近所の買い物中心、という人は所有よりカーシェアの方が安く済むことも。利用スタイルで最適解は変わります。</p>
    <h2>よくある質問</h2>'''+faq([
    ('何回くらいから月極が得？','「月極の月額 ÷ コインP1回料金」が、月の利用回数の損益分岐です。これを超えると月極が得になります。'),
    ('カーシェアはどう？','月数回・短時間ならカーシェアが安いことも。保険・ガソリン込みなのも利点です。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['各駐車場・カーシェア料金の比較']),
  js='''  function calc(){const m=Math.max(0,+$('m').value||0),c=Math.max(0,+$('c').value||0),n=Math.max(0,+$('n').value||0);
    const tuki=m*12, coin=c*n*12, diff=Math.abs(tuki-coin), win=tuki<coin?'月極':(tuki>coin?'コインP':'同じ');
    $('sub').textContent=`月極${num(m)}円/月・コインP${num(c)}円×${n}回/月`;
    $('tuki').textContent=yen(tuki);$('coin').textContent=yen(coin);$('win').textContent=win;
    show();anim($('big'),0,diff,800);
    SHARE=`駐車場シミュ、年間で「${win}」が約${yen(diff)}お得でした🅿️`;}''')

# ===== 17. 定期代 元取り =====
add(id='teikidai', cat=CAR, emoji='🚃',
  title='定期代 元取りシミュレーター｜通勤定期はお得？都度払いと比較｜シミュラボ',
  desc='片道運賃・1ヶ月定期代・通勤日数から、定期券と都度払いを比較し、月にどれだけお得か・元が取れる日数を計算する無料シミュレーター。',
  ogtitle='定期代 元取り｜定期はお得？', ogdesc='片道運賃・定期代・通勤日数から定期の損得を計算。',
  h1='定期代 元取りシミュレーター',
  lead='通勤定期は本当にお得？片道運賃・1ヶ月の定期代・通勤日数から、都度払いと比べてどれだけ得か、何日で元が取れるかを計算します。',
  inputs='''    <h2>🚃 条件を入れる</h2>
    <div class="row"><div class="field"><label>片道の運賃 <span class="hint">（円）</span></label><input type="number" id="f" value="280" min="0" inputmode="numeric"></div>
    <div class="field"><label>1ヶ月の定期代 <span class="hint">（円）</span></label><input type="number" id="t" value="9800" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>1ヶ月の通勤日数 <span class="hint">（日）</span></label><input type="number" id="d" value="20" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">定期はお得か見る</button>''',
  result='''      <div class="label">定期で月にうく金額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">都度払い(月)</div><div class="v" id="tudo">—</div></div>
      <div class="stat"><div class="k">元が取れる日数</div><div class="v accent" id="moto">—</div></div>
      <div class="stat"><div class="k">判定</div><div class="v" id="judge">—</div></div></div>''',
  article=C('定期は <b>都度払い ＝ 片道 × 2 × 通勤日数</b> と比べてお得かで判断。<b>定期代 ÷ 往復運賃</b> の日数だけ通えば元が取れます。')+'''
    <h2>定期券は何日で元が取れる？</h2>
    <p>1ヶ月定期は「ひと月に何日通うか」で得かどうかが決まります。往復運賃で定期代を割った日数を超えて通勤すれば、定期の方がお得です。リモートワークが多い人は、定期より都度払い＋IC運賃が安くなることもあります。</p>
    <div class="note"><strong>計算式</strong><br>都度払い（月）＝ 片道運賃 × 2 × 通勤日数<br>元が取れる日数 ＝ 定期代 ÷（片道運賃 × 2）</div>
    <p>3ヶ月・6ヶ月定期はさらに割引率が高くなります。テレワークが週2以上あるなら、6ヶ月定期より回数券や都度払いが有利なケースも。働き方に合わせて選びましょう。</p>
    <h2>よくある質問</h2>'''+faq([
    ('週3出社でも定期は得？','「元が取れる日数」より実際の通勤日数が多ければ得です。少ないなら都度払いが有利です。'),
    ('3ヶ月・6ヶ月定期は？','長い定期ほど割引率が上がります。出社が安定しているなら6ヶ月定期が最安になりやすいです。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['各鉄道会社の定期運賃']),
  js='''  function calc(){const f=Math.max(0,+$('f').value||0),t=Math.max(0,+$('t').value||0),d=Math.max(0,+$('d').value||0);
    const tudo=f*2*d, save=tudo-t, moto=f>0?Math.ceil(t/(f*2)):0;
    $('sub').textContent=`片道${num(f)}円・定期${num(t)}円・月${d}日`;
    $('tudo').textContent=yen(tudo);$('moto').textContent=moto+'日';$('judge').textContent=save>=0?'定期がお得':'都度払いがお得';
    show();anim($('big'),0,Math.abs(save),800);
    SHARE=`定期代シミュ、${save>=0?'定期で月'+yen(save)+'お得':'都度払いが月'+yen(-save)+'お得'}（元取り${moto}日）でした🚃`;}''')

# ===== 18. 何曜日 =====
add(id='youbi-keisan', cat=LIFE, emoji='📅',
  title='何曜日 計算｜指定した日付の曜日を一発で調べる（万年カレンダー）｜シミュラボ',
  desc='過去・未来の任意の日付を入れると、その日が何曜日か、平日か休日か、今日から何日かを一発で調べる万年カレンダー型の無料ツール。',
  ogtitle='何曜日 計算｜その日付は何曜日？', ogdesc='任意の日付の曜日・平日休日・今日からの日数を計算。',
  h1='何曜日 計算ツール',
  lead='あの日は何曜日だった？この日付は何曜日になる？過去でも未来でも、入れた日付の曜日・平日/休日・今日からの日数を一発で調べます。',
  inputs='''    <h2>📅 日付を入れる</h2>
    <div class="field"><label>調べたい日付</label><input type="date" id="d" value="2000-01-01"></div>
    <button class="btn btn-primary" id="calcBtn">曜日を調べる</button>''',
  result='''      <div class="seo-anim ptag-stage" id="stage"><div class="pop-emoji" id="ico">📅</div></div>
      <div class="label">その日付は</div>
      <div class="big"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">平日 / 休日</div><div class="v accent" id="hw">—</div></div>
      <div class="stat"><div class="k">今日から</div><div class="v" id="diff">—</div></div>
      <div class="stat"><div class="k">月の第何週</div><div class="v" id="week">—</div></div></div>''',
  article=C('曜日は「ツェラーの公式」などで計算できますが、本ツールはブラウザの日付機能で<b>過去・未来の任意の日付</b>の曜日を正確に判定します。')+'''
    <h2>曜日計算の使いどころ</h2>
    <p>「生まれた日は何曜日だった？」「来年の誕生日は何曜日？」「記念日は土日にあたる？」——過去から未来まで、どんな日付でも一発で曜日が分かります。予定づくりやイベントの計画に便利です。</p>
    <div class="note"><strong>豆知識</strong><br>同じ日付の曜日は、平年は翌年に1つ、うるう年をまたぐと2つずれます。カレンダーは28年で同じ並びに戻ります（グレゴリオ暦のうるう年規則による）。</div>
    <p>本ツールの「平日/休日」は土日のみで判定し、祝日は含みません（祝日は年により変動するため）。</p>
    <h2>よくある質問</h2>'''+faq([
    ('かなり昔の日付でも分かる？','はい。グレゴリオ暦の範囲で、過去でも未来でも正確に曜日を判定します。'),
    ('祝日も判定できる？','本ツールは土日のみを休日として判定します。祝日は年によって変わるため含みません。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['ツェラーの公式（曜日の計算）']),
  js='''  const YOBI=['日','月','火','水','木','金','土'];
  function calc(){const v=$('d').value; if(!v){return;}
    const dt=new Date(v+'T00:00:00'); const now=new Date(); now.setHours(0,0,0,0);
    const w=dt.getDay(); const diff=Math.round((dt-now)/86400000);
    $('big').textContent=YOBI[w]+'曜日';
    $('sub').textContent=`${dt.getFullYear()}年${dt.getMonth()+1}月${dt.getDate()}日`;
    $('hw').textContent=(w===0||w===6)?'休日(土日)':'平日';
    $('diff').textContent=diff===0?'今日':(diff>0?'あと'+num(diff)+'日':num(-diff)+'日前');
    $('week').textContent='第'+(Math.floor((dt.getDate()-1)/7)+1)+'週';
    const ic=$('ico');ic.classList.remove('on');void ic.offsetWidth;ic.classList.add('on');
    show();
    SHARE=`何曜日シミュ、${dt.getFullYear()}/${dt.getMonth()+1}/${dt.getDate()} は「${YOBI[w]}曜日」でした📅`;}''')

# ===== 19. お中元・お歳暮 相場 =====
add(id='chugen-seibo', cat=MANNER, emoji='🎁',
  title='お中元・お歳暮 相場｜相手別の金額と贈る時期の早見｜シミュラボ',
  desc='贈る相手（上司・取引先・親戚・友人）から、お中元・お歳暮の相場（金額の目安）と、地域別の贈る時期を調べる無料ツール。',
  ogtitle='お中元・お歳暮 相場｜いくらが目安？', ogdesc='相手別のお中元・お歳暮の相場と贈る時期の早見。',
  h1='お中元・お歳暮 相場 早見',
  lead='お中元・お歳暮、いくらの品を贈ればいい？贈る相手から相場の目安と、地域別の贈る時期を表示します。',
  inputs='''    <h2>🎁 条件を入れる</h2>
    <div class="row"><div class="field"><label>贈る相手</label><select id="who"><option value="0" selected>会社の上司</option><option value="1">取引先・お世話になった方</option><option value="2">親・親戚</option><option value="3">友人・知人</option><option value="4">仲人</option></select></div>
    <div class="field"><label>種類</label><select id="kind"><option value="natsu" selected>お中元（夏）</option><option value="fuyu">お歳暮（冬）</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">相場を見る</button>''',
  result='''      <div class="label">相場の目安（中央値）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">相場のレンジ</div><div class="v accent" id="range">—</div></div>
      <div class="stat"><div class="k">贈る時期(関東)</div><div class="v" id="kanto">—</div></div>
      <div class="stat"><div class="k">贈る時期(関西)</div><div class="v" id="kansai">—</div></div></div>''',
  article=C('お中元・お歳暮の相場は相手で変わり、<b>3,000〜5,000円</b>が中心。とくにお世話になった方やお歳暮は、お中元より少し高めにするのが一般的です。')+'''
    <h2>相手別の相場（目安）</h2>
    <table class="seo-table"><tr><th>贈る相手</th><th>相場</th></tr>
    <tr><td>会社の上司</td><td>3,000〜5,000円</td></tr>
    <tr><td>取引先・恩人</td><td>5,000〜10,000円</td></tr>
    <tr><td>親・親戚</td><td>3,000〜5,000円</td></tr>
    <tr><td>友人・知人</td><td>2,000〜3,000円</td></tr></table>
    <div class="note"><strong>贈る時期</strong><br>お中元：関東 7月初〜15日／関西 7月中旬〜8月15日<br>お歳暮：関東 12月初〜20日ごろ／関西 12月13日〜20日ごろ</div>
    <p>一般にお歳暮はお中元よりやや高め。両方贈る場合は、1年の締めくくりのお歳暮を重視します。時期を過ぎたら「暑中見舞い」「寒中見舞い」として贈れます。本ツールは一般的な目安です。</p>
    <h2>よくある質問</h2>'''+faq([
    ('お中元とお歳暮、両方必要？','どちらか一方なら、1年の締めのお歳暮が優先されます。両方贈るとより丁寧です。'),
    ('喪中でも贈っていい？','お祝いではないため、喪中でもお中元・お歳暮は贈って問題ないとされます。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['一般的な贈答マナー・百貨店の相場目安']),
  js='''  function calc(){const who=+$('who').value||0,fuyu=$('kind').value==='fuyu';
    const R=[[3000,5000],[5000,10000],[3000,5000],[2000,3000],[5000,10000]][who];
    let lo=R[0],hi=R[1]; if(fuyu){lo=Math.round(lo*1.1);hi=Math.round(hi*1.1);} const mid=Math.round((lo+hi)/2/100)*100;
    const labels=['会社の上司','取引先・恩人','親・親戚','友人・知人','仲人'];
    $('sub').textContent=`${labels[who]}・${fuyu?'お歳暮':'お中元'}`;
    $('range').textContent=yen(lo)+'〜'+yen(hi);
    $('kanto').textContent=fuyu?'12月初〜20日':'7月初〜15日';$('kansai').textContent=fuyu?'12/13〜20日':'7月中〜8/15';
    show();anim($('big'),0,mid,700);
    SHARE=`お中元・お歳暮シミュ、${labels[who]}への${fuyu?'お歳暮':'お中元'}は ${yen(lo)}〜${yen(hi)}が目安でした🎁`;}''')

# ===== 20. 七五三 年齢早見 =====
add(id='shichigosan', cat=KIDS, emoji='🎎',
  title='七五三 年齢早見｜何歳でいつ？数え年・満年齢で自動判定｜シミュラボ',
  desc='子どもの生年と性別から、七五三（男の子3・5歳／女の子3・7歳）を数え年・満年齢それぞれで何年に行うかを自動で表示する無料ツール。',
  ogtitle='七五三 いつ？年齢早見', ogdesc='生年と性別から七五三を数え年・満年齢で自動判定。',
  h1='七五三 年齢早見ツール',
  lead='七五三は何歳の年にやる？子どもの生年と性別から、男の子（3・5歳）・女の子（3・7歳）の七五三を、数え年・満年齢それぞれで何年に行うか表示します。',
  inputs='''    <h2>🎎 子どもの情報を入れる</h2>
    <div class="row"><div class="field"><label>生まれた年 <span class="hint">（西暦）</span></label><input type="number" id="y" value="2021" min="2000" max="2035" inputmode="numeric"></div>
    <div class="field"><label>性別</label><select id="sex"><option value="m">男の子</option><option value="f" selected>女の子</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">七五三の年を調べる</button>''',
  result='''      <div class="label">次の七五三は</div>
      <div class="big"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="yaku-steps" id="steps"></div>
      <div class="anim-cap">数え年で行うのが伝統。最近は満年齢でもOK</div>''',
  article=C('七五三は <b>男の子＝3歳・5歳／女の子＝3歳・7歳</b>。伝統的には<b>数え年</b>で行いますが、近年は<b>満年齢</b>で行う家庭も増えています。')+'''
    <h2>七五三の年齢</h2>
    <p>七五三は子どもの成長を祝う行事で、11月15日ごろに神社へお参りします。年齢は地域・家庭により数え年・満年齢どちらもありますが、現在はどちらでも問題ないとされています。</p>
    <table class="seo-table"><tr><th>性別</th><th>祝う年齢</th><th>由来</th></tr>
    <tr><td>男の子</td><td>3歳・5歳</td><td>3歳「髪置」5歳「袴着」</td></tr>
    <tr><td>女の子</td><td>3歳・7歳</td><td>3歳「髪置」7歳「帯解」</td></tr></table>
    <div class="note"><strong>数え年と満年齢</strong><br>数え年 ＝ その年 − 生まれ年 ＋ 1<br>満年齢 ＝ その年 − 生まれ年（誕生日後）<br>きょうだい一緒にやるため、上の子は満・下の子は数え、と合わせることもあります。</div>
    <p>本ツールは数え年・満年齢それぞれで七五三にあたる西暦を表示します。早生まれの兄弟と一緒に祝う調整にもどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([
    ('数え年と満年齢どっちが正しい？','どちらでも構いません。きょうだいや体格・成長に合わせて選ぶ家庭が増えています。'),
    ('男の子の3歳はやる？','地域によります。3歳・5歳の両方やる地域もあれば、5歳のみの地域もあります。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['神社本庁「七五三」']),
  js='''  function calc(){const y=Math.max(1900,+$('y').value||2021),sex=$('sex').value;
    const ages=sex==='m'?[3,5]:[3,7]; const now=new Date().getFullYear();
    // 数え年: 行う年 = 生年 + 年齢 - 1 / 満: 生年 + 年齢
    const steps=ages.map(a=>{const kazoe=y+a-1, man=y+a; return {a,kazoe,man};});
    // 次の七五三（数え年ベースで未来/今年に最も近い）
    let next=null; steps.forEach(s=>{ if(s.kazoe>=now && (!next||s.kazoe<next.kazoe)) next=s; });
    $('steps').innerHTML=steps.map(s=>`<div class="yaku-step${next&&s.a===next.a?' on':''}"><div class="lab">${s.a}歳</div><div class="age">数え${s.kazoe}年/満${s.man}年</div></div>`).join('');
    if(next){ $('big').textContent=next.kazoe+'年'; $('sub').textContent=`${y}年生まれ・${sex==='m'?'男の子':'女の子'}／次は${next.a}歳（数え年）`; }
    else { $('big').textContent='お祝い済み'; $('sub').textContent=`${y}年生まれ・${sex==='m'?'男の子':'女の子'}`; }
    show();
    SHARE=`七五三 早見、${y}年生まれの${sex==='m'?'男の子':'女の子'}の次の七五三は ${next?next.kazoe+'年（数え'+next.a+'歳）':'お祝い済み'} でした🎎`;}''')

if __name__=='__main__':
    write_all(SIMS)
    print(f'seo5 done. {len(SIMS)} sims.')
