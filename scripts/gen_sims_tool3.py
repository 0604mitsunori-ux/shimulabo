# -*- coding: utf-8 -*-
"""シミュラボ：便利ツール 第3弾10本（既存 slug=tool「便利ツール」に追加）。消費税/割引/偏差値/比率/年齢など常時検索される計算ツール。
gen_sims_tool TPL流用（try無し）。CTAなし。

seo_internal.py / gen_images.py のauto-importに 'gen_sims_tool3' を追加して使う。
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq
from gen_sims_tool import TPL, viz
from sim_quiz import make_engines
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CAT = '便利ツール'
SIMS = []
tally_quiz, num_quiz, band_quiz, add, q_article, render = make_engines(SIMS, CAT, TPL, viz)
ANIM = r'''  function anim(v,el2){const el=el2||$('big'),t0=performance.now();(function s(n){const p=Math.min(1,(n-t0)/700),e=1-Math.pow(1-p,3);el.textContent=Math.round(v*e).toLocaleString('ja-JP');if(p<1)requestAnimationFrame(s);})(performance.now());}'''

# ============================================================
# 1. 消費税計算（消費税 計算 18000/KD26/TP138000）★★
# ============================================================
add(id='zeikomi-keisan', emoji='🧾',
  title='消費税計算機｜税込・税抜・消費税額をすぐ計算（10%・8%）｜シミュラボ',
  desc='金額を入れるだけで、消費税込み・税抜き・消費税額を自動計算する無料ツール。税率10%・軽減税率8%に対応。税抜→税込、税込→税抜の両方向に計算できます。',
  ogtitle='消費税計算機｜税込・税抜をすぐ計算', ogdesc='10%・8%対応。税込/税抜/消費税額を自動計算。',
  h1='消費税計算機',
  lead='税込はいくら?税抜は?金額と税率を入れるだけで、消費税込み・税抜き・消費税額を一度に計算します。10%・8%（軽減税率）対応。',
  inputs='''    <h2>🧾 条件を入れる</h2>
    <div class="field"><label>金額 <span class="hint">円</span></label><input type="number" id="amt" value="1000" min="0" inputmode="numeric"></div>
    <div class="row"><div class="field"><label>税率</label><select id="rate"><option value="10" selected>10%（標準）</option><option value="8">8%（軽減税率）</option></select></div>
    <div class="field"><label>入力した金額は</label><select id="dir"><option value="in" selected>税抜き価格</option><option value="out">税込み価格</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">消費税を計算</button>''',
  result='''      <div class="label">税込み価格</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">税抜き価格</div><div class="v" id="net">—</div></div>
      <div class="stat"><div class="k">消費税額</div><div class="v accent" id="tax">—</div></div></div>''',
  article='''    <div class="note"><strong>計算式</strong><br>税込 ＝ 税抜 ×（1＋税率）／税抜 ＝ 税込 ÷（1＋税率）／消費税額 ＝ 税込 − 税抜</div>
    <h2>消費税の計算方法</h2>
    <p>消費税は、税抜価格に税率（標準10%・軽減8%）を掛けて求めます。税込価格から税抜を出すには、税込を1.1（または1.08）で割ります。端数は1円未満を切り捨てるのが一般的ですが、事業者により切り上げ・四捨五入の場合もあります。食品や定期購読の新聞などは軽減税率8%の対象です。</p>
    <h2>よくある質問</h2>'''+faq([
      ('軽減税率8%とは？','飲食料品（酒類・外食を除く）や定期購読の新聞などに適用される税率です。'),
      ('端数はどうなる？','一般に1円未満は切り捨てですが、事業者により異なる場合があります。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const a=Math.max(0,+$('amt').value||0),r=(+$('rate').value||10)/100,dir=$('dir').value;
    let net,gross,tax;
    if(dir==='in'){net=a;tax=Math.floor(a*r);gross=net+tax;}
    else{gross=a;net=Math.round(a/(1+r));tax=gross-net;}
    $('sub').textContent=`税率${(+$('rate').value)}%・${sel('dir').text}で入力`;
    $('net').textContent=yen(net);$('tax').textContent=yen(tax);
    SHARE=`消費税計算機、${yen(a)}（${sel('dir').text}）→ 税込${yen(gross)}・税抜${yen(net)}・消費税${yen(tax)}でした🧾`;show();anim(gross);}
'''+ANIM)

# ============================================================
# 2. 割引計算（割引 計算 1100/KD0/TP15000）★
# ============================================================
add(id='waribiki-keisan', emoji='🏷️',
  title='割引計算機｜○％OFF・○円引きで割引後の価格をすぐ計算｜シミュラボ',
  desc='元の価格と割引率を入れるだけで、割引後の価格と割引額を自動計算する無料ツール。○％OFFのセール価格や、二重割引の計算にも使えます。',
  ogtitle='割引計算機｜○％OFFの価格をすぐ計算', ogdesc='元の価格と割引率から割引後価格・割引額を自動計算。',
  h1='割引計算機',
  lead='「30%OFF」って結局いくら?元の価格と割引率を入れるだけで、割引後の価格と割引額を計算します。セールのお買い物に。',
  inputs='''    <h2>🏷️ 条件を入れる</h2>
    <div class="field"><label>元の価格 <span class="hint">円</span></label><input type="number" id="price" value="3000" min="0" inputmode="numeric"></div>
    <div class="field"><label>割引率 <span class="hint">%OFF</span></label><input type="number" id="rate" value="30" min="0" max="100" inputmode="decimal"></div>
    <div class="field"><label>さらに追加割引（任意）<span class="hint">%OFF</span></label><input type="number" id="rate2" value="0" min="0" max="100" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">割引後の価格を計算</button>''',
  result='''      <div class="label">割引後の価格</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">割引額（合計）</div><div class="v accent" id="off">—</div></div>
      <div class="stat"><div class="k">実質の割引率</div><div class="v" id="eff">—</div></div></div>''',
  article='''    <div class="note"><strong>計算式</strong><br>割引後 ＝ 元の価格 ×（1−割引率）／二重割引 ＝ さらに ×（1−追加割引率）</div>
    <h2>割引の計算方法</h2>
    <p>割引後の価格は「元の価格 ×（1−割引率）」で求められます。3,000円の30%OFFなら2,100円。注意したいのが二重割引で、「30%OFF後にさらに20%OFF」は合計50%OFFではなく、実質44%OFF（0.7×0.8＝0.56倍）になります。本ツールは追加割引にも対応しているので、レジ前でのお得チェックに使えます。</p>
    <h2>よくある質問</h2>'''+faq([
      ('二重割引は足し算じゃないの？','違います。順番に掛け算します。30%＋20%は50%ではなく実質44%OFFです。'),
      ('○円引きは？','元の価格から直接その額を引きます。本ツールは％OFF向けです。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const p=Math.max(0,+$('price').value||0),r=Math.min(100,Math.max(0,+$('rate').value||0)),r2=Math.min(100,Math.max(0,+$('rate2').value||0));
    const after=Math.round(p*(1-r/100)*(1-r2/100)), off=p-after, eff=p>0?Math.round((1-after/p)*1000)/10:0;
    $('sub').textContent= r2>0 ? `${num(r)}%OFF後さらに${num(r2)}%OFF` : `${num(r)}%OFF`;
    $('off').textContent=yen(off);$('eff').textContent=eff+'%OFF';
    SHARE=`割引計算機、${yen(p)}の${num(r)}%OFF${r2>0?('+'+num(r2)+'%'):''}は ${yen(after)}（${yen(off)}おトク）でした🏷️`;show();anim(after);}
'''+ANIM)

# ============================================================
# 3. 偏差値計算（偏差値 計算 7900/KD2/TP32000）★★
# ============================================================
add(id='hensachi-keisan', emoji='📊',
  title='偏差値計算機｜点数・平均点・標準偏差から偏差値を計算｜シミュラボ',
  desc='自分の点数・平均点・標準偏差を入れるだけで、偏差値を自動計算する無料ツール。テストの立ち位置（上位何％か）の目安も分かります。',
  ogtitle='偏差値計算機｜点数・平均から偏差値を計算', ogdesc='点数・平均点・標準偏差から偏差値を自動計算。上位％も。',
  h1='偏差値計算機',
  lead='このテスト、偏差値いくつ?自分の点数・平均点・標準偏差を入れると、偏差値を計算します。上位何％かの目安も表示。',
  inputs='''    <h2>📊 条件を入れる</h2>
    <div class="row"><div class="field"><label>自分の点数</label><input type="number" id="score" value="70" inputmode="decimal"></div>
    <div class="field"><label>平均点</label><input type="number" id="avg" value="60" inputmode="decimal"></div></div>
    <div class="field"><label>標準偏差 <span class="hint">分からなければ15</span></label><input type="number" id="sd" value="15" min="0.1" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">偏差値を計算</button>''',
  result='''      <div class="label">あなたの偏差値</div>
      <div class="big"><span id="big">0</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">平均点との差</div><div class="v" id="diff">—</div></div>
      <div class="stat"><div class="k">上位の目安</div><div class="v accent" id="rank">—</div></div></div>''',
  article='''    <div class="note"><strong>計算式</strong><br>偏差値 ＝ 50 ＋ 10 ×（自分の点数 − 平均点）÷ 標準偏差</div>
    <h2>偏差値とは</h2>
    <p>偏差値は、平均点を50として、自分の点数が平均からどれだけ離れているかを表す指標です。標準偏差で割ることで、点数のばらつきが違うテストどうしを比較できます。偏差値60は上位約16％、偏差値70は上位約2.3％にあたります（得点が正規分布の場合）。標準偏差が分からないときは、目安として15前後で計算してみてください。</p>
    <h2>よくある質問</h2>'''+faq([
      ('標準偏差が分からない','テスト全体のばらつきの指標です。不明なら15前後を目安に入れてみてください。'),
      ('偏差値の上限は？','理論上は青天井ですが、現実には25〜75程度に収まることがほとんどです。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function erf(x){const s=x<0?-1:1;x=Math.abs(x);const t=1/(1+0.3275911*x);const y=1-(((((1.061405429*t-1.453152027)*t)+1.421413741)*t-0.284496736)*t+0.254829592)*t*Math.exp(-x*x);return s*y;}
  function calc(){const sc=+$('score').value||0,m=+$('avg').value||0,sd=Math.max(0.1,+$('sd').value||0.1);
    const h=Math.round((50+10*(sc-m)/sd)*10)/10;
    const z=(h-50)/10; const upper=Math.round((1-0.5*(1+erf(z/Math.SQRT2)))*1000)/10;
    $('big').textContent=h;$('sub').textContent=`点数${num(sc)}・平均${num(m)}・標準偏差${num(sd)}`;
    $('diff').textContent=(sc-m>=0?'+':'')+num(sc-m)+'点';$('rank').textContent='上位 約'+Math.max(0.1,upper)+'%';
    SHARE=`偏差値計算機、点数${num(sc)}・平均${num(m)}なら偏差値${h}（上位約${Math.max(0.1,upper)}%）でした📊`;show();
    const el=$('big'),t0=performance.now();(function s(n){const p=Math.min(1,(n-t0)/700);el.textContent=(Math.round(h*p*10)/10).toFixed(1);if(p<1)requestAnimationFrame(s);else el.textContent=h;})(performance.now());}
''')

# ============================================================
# 4. 比率計算（比率 計算 5700/KD1/TP27000）★★
# ============================================================
add(id='hiritsu-keisan', emoji='⚖️',
  title='比率計算機｜比例式 A:B＝C:X の X をすぐ計算｜シミュラボ',
  desc='A:B＝C:X の比例式から、未知の数Xを自動計算する無料ツール。比を簡単な整数に約分する機能もあり、料理の分量や図面の縮尺計算に使えます。',
  ogtitle='比率計算機｜比例式 A:B＝C:X を計算', ogdesc='比例式の未知数Xを自動計算。比の約分も。',
  h1='比率計算機',
  lead='A:B＝C:?の「?」をすぐ計算。比例式の未知数を求めます。料理の分量、図面の縮尺、混合比の計算などに。',
  inputs='''    <h2>⚖️ 比例式を入れる（A:B＝C:X）</h2>
    <div class="row"><div class="field"><label>A</label><input type="number" id="a" value="2" inputmode="decimal"></div>
    <div class="field"><label>B</label><input type="number" id="b" value="3" inputmode="decimal"></div></div>
    <div class="row"><div class="field"><label>C</label><input type="number" id="c" value="10" inputmode="decimal"></div>
    <div class="field"><label>X（求める数）</label><input type="text" id="x" value="?" disabled></div></div>
    <button class="btn btn-primary" id="calcBtn">X を計算</button>''',
  result='''      <div class="label">X の値</div>
      <div class="big"><span id="big">0</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">いちばん簡単な比</div><div class="v accent" id="ratio">—</div></div></div>''',
  article='''    <div class="note"><strong>計算式</strong><br>A:B ＝ C:X のとき　X ＝ B × C ÷ A</div>
    <h2>比率（比例式）の計算方法</h2>
    <p>「A対BがC対Xに等しい」という比例式は、外側どうし・内側どうしの積が等しい性質（A×X＝B×C）を使って解きます。つまりX＝B×C÷A。たとえば2:3＝10:Xなら、X＝3×10÷2＝15。料理で「2人分のレシピを5人分にしたい」、図面の縮尺、濃度や混合比の計算などに役立ちます。本ツールは比をいちばん簡単な整数比にも直します。</p>
    <h2>よくある質問</h2>'''+faq([
      ('小数や分数でも使える？','はい。A・B・Cに小数を入れてもXを計算できます。'),
      ('比を簡単にしたい','A:Bの最大公約数で割った「いちばん簡単な比」も表示します。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function gcd(a,b){a=Math.abs(a);b=Math.abs(b);while(b){[a,b]=[b,a%b];}return a||1;}
  function calc(){const a=+$('a').value||0,b=+$('b').value||0,c=+$('c').value||0;
    if(a===0){$('big').textContent='—';$('sub').textContent='Aに0は使えません';show();return;}
    const x=b*c/a;$('big').textContent=(Math.round(x*1000)/1000).toLocaleString('ja-JP');
    $('x').value=Math.round(x*1000)/1000;
    // 約分（整数のときのみ）
    let rtxt='—';
    if(Number.isInteger(a)&&Number.isInteger(b)){const g=gcd(a,b);rtxt=(a/g)+' : '+(b/g);}
    $('sub').textContent=`${num(a)} : ${num(b)} ＝ ${num(c)} : X`;$('ratio').textContent=rtxt;
    SHARE=`比率計算機、${num(a)}:${num(b)}＝${num(c)}:X なら X＝${Math.round(x*1000)/1000} でした⚖️`;show();}
''')

# ============================================================
# 5. 年齢計算（年齢 計算 2500/KD52/TP31000）
# ============================================================
add(id='nenrei-keisan', emoji='🎂',
  title='年齢計算機｜生年月日から満年齢・数え年・干支をすぐ計算｜シミュラボ',
  desc='生年月日を入れるだけで、今日時点の満年齢・数え年・干支・生まれてからの日数を自動計算する無料ツール。基準日を変えれば指定日の年齢も分かります。',
  ogtitle='年齢計算機｜満年齢・数え年・干支を計算', ogdesc='生年月日から満年齢・数え年・干支・生後日数を計算。',
  h1='年齢計算機',
  lead='今、何歳?生年月日を入れると、満年齢・数え年・干支・生まれてからの日数を計算します。基準日を変えれば、その日の年齢も分かります。',
  inputs='''    <h2>🎂 生年月日を入れる</h2>
    <div class="field"><label>生年月日</label><input type="date" id="bd" value="1990-05-15"></div>
    <div class="field"><label>基準日 <span class="hint">（その日の年齢を計算）</span></label><input type="date" id="base"></div>
    <button class="btn btn-primary" id="calcBtn">年齢を計算</button>''',
  result='''      <div class="label">満年齢</div>
      <div class="big"><span id="big">0</span><span class="unit">歳</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">数え年</div><div class="v accent" id="kazoe">—</div></div>
      <div class="stat"><div class="k">干支</div><div class="v" id="eto">—</div></div>
      <div class="stat"><div class="k">生まれてからの日数</div><div class="v" id="days">—</div></div></div>''',
  article='''    <div class="note"><strong>満年齢と数え年</strong><br>満年齢は誕生日ごとに1歳増えます。数え年は生まれた時点を1歳とし、元日ごとに1歳増える昔の数え方です。</div>
    <h2>年齢の計算方法</h2>
    <p>満年齢は、基準日の年から生まれた年を引き、まだ誕生日が来ていなければ1を引きます。数え年は「その年−生まれ年＋1」。厄年や七五三、長寿祝いは数え年で考える風習もあります。本ツールは干支（十二支）や、生まれてからの通算日数も表示します。基準日を空欄にすると今日時点で計算します。</p>
    <h2>よくある質問</h2>'''+faq([
      ('数え年はいつ増える？','元日（1月1日）ごとに1歳増えるのが伝統的な数え方です。'),
      ('法律上の年齢は？','日本では誕生日の前日が満了日とされますが、本ツールは一般的な満年齢で計算します。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  const ETO=['申','酉','戌','亥','子','丑','寅','卯','辰','巳','午','未'];
  function calc(){const bv=$('bd').value;if(!bv){$('big').textContent='—';$('sub').textContent='生年月日を入れてね';show();return;}
    const bd=new Date(bv);const base=$('base').value?new Date($('base').value):new Date();
    let age=base.getFullYear()-bd.getFullYear();
    const m=base.getMonth()-bd.getMonth();if(m<0||(m===0&&base.getDate()<bd.getDate()))age--;
    const kazoe=base.getFullYear()-bd.getFullYear()+1;
    const days=Math.floor((base-bd)/86400000);
    $('sub').textContent=(($('base').value)?'基準日 '+$('base').value:'今日')+' 時点';
    $('kazoe').textContent=kazoe+'歳';$('eto').textContent=ETO[bd.getFullYear()%12]+'年';$('days').textContent=num(days)+'日';
    SHARE=`年齢計算機、満${age}歳（数え${kazoe}歳・${ETO[bd.getFullYear()%12]}年）でした🎂`;show();anim(age);}
'''+ANIM)

# ============================================================
# 6. ローマ数字変換（ローマ数字 変換 2900/KD0）
# ============================================================
add(id='roma-suji', emoji='🔢',
  title='ローマ数字変換ツール｜数字⇔ローマ数字を相互変換（I・V・X・L…）｜シミュラボ',
  desc='アラビア数字（1・2・3…）とローマ数字（I・V・X・L・C・D・M）を相互変換できる無料ツール。1〜3999に対応。時計や章番号、年号の表記に。',
  ogtitle='ローマ数字変換｜数字⇔ローマ数字', ogdesc='数字とローマ数字を相互変換。1〜3999対応。',
  h1='ローマ数字変換ツール',
  lead='「2024」をローマ数字で?「XIV」は何番?アラビア数字とローマ数字を相互に変換します。時計・章番号・映画のナンバリングに。',
  inputs='''    <h2>🔢 変換する</h2>
    <div class="field"><label>変換の向き</label><select id="dir"><option value="n2r" selected>数字 → ローマ数字</option><option value="r2n">ローマ数字 → 数字</option></select></div>
    <div class="field"><label>入力 <span class="hint">数字は1〜3999</span></label><input type="text" id="val" value="2024" autocomplete="off"></div>
    <button class="btn btn-primary" id="calcBtn">変換する</button>''',
  result='''      <div class="label">変換結果</div>
      <div class="big" style="font-size:34px;letter-spacing:2px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>''',
  article='''    <div class="note"><strong>ローマ数字の基本</strong><br>I=1, V=5, X=10, L=50, C=100, D=500, M=1000。小さい数が大きい数の左にあると引き算（IV=4, IX=9, XL=40）。</div>
    <h2>ローマ数字の読み方・書き方</h2>
    <p>ローマ数字は、I・V・X・L・C・D・Mの7文字を組み合わせて表します。基本は大きい順に足し算（例：XVI＝16）ですが、4や9のように「小さい記号が大きい記号の前」にくると引き算します（IV＝4、IX＝9、XL＝40、CM＝900）。同じ記号は3つまで。0や負の数、4000以上は基本的に表せません。時計の文字盤、書籍の章番号、映画の続編表記などで使われます。</p>
    <h2>よくある質問</h2>'''+faq([
      ('4はなぜIVなの？','IIIIではなく、5(V)から1(I)を引く「IV」と書くのが標準的な表記です。'),
      ('0やマイナスは？','ローマ数字には0や負の数を表す記号がありません。'),
      ('データは送信されますか？','いいえ。変換はすべてブラウザ内で完結します。')]),
  js=r'''  const MAP=[[1000,'M'],[900,'CM'],[500,'D'],[400,'CD'],[100,'C'],[90,'XC'],[50,'L'],[40,'XL'],[10,'X'],[9,'IX'],[5,'V'],[4,'IV'],[1,'I']];
  function toRoman(n){let r='';for(const [v,s] of MAP){while(n>=v){r+=s;n-=v;}}return r;}
  function fromRoman(s){s=s.toUpperCase();const V={I:1,V:5,X:10,L:50,C:100,D:500,M:1000};let n=0,prev=0,ok=/^[IVXLCDM]+$/.test(s);if(!ok)return null;
    for(let i=s.length-1;i>=0;i--){const c=V[s[i]];if(c<prev)n-=c;else{n+=c;prev=c;}}return n;}
  function calc(){const dir=$('dir').value,raw=($('val').value||'').trim();
    if(dir==='n2r'){const n=parseInt(raw,10);if(!(n>=1&&n<=3999)){$('big').textContent='—';$('sub').textContent='1〜3999の整数を入れてね';show();return;}
      const r=toRoman(n);$('big').textContent=r;$('sub').textContent=n+' をローマ数字に';SHARE=`ローマ数字変換、${n} ＝ ${r} でした🔢`;}
    else{const n=fromRoman(raw);if(n===null||n===0){$('big').textContent='—';$('sub').textContent='正しいローマ数字を入れてね（I V X L C D M）';show();return;}
      $('big').textContent=n;$('sub').textContent=raw.toUpperCase()+' を数字に';SHARE=`ローマ数字変換、${raw.toUpperCase()} ＝ ${n} でした🔢`;}
    show();}
''')

# ============================================================
# 7. 標準偏差計算（標準偏差 計算 1100/KD2）
# ============================================================
add(id='hyojun-hensa', emoji='📈',
  title='標準偏差計算機｜数値を入れるだけで平均・分散・標準偏差を計算｜シミュラボ',
  desc='カンマや改行で区切った数値を入れるだけで、平均・分散・標準偏差（母集団・標本）を自動計算する無料ツール。データのばらつきの分析に。',
  ogtitle='標準偏差計算機｜平均・分散・標準偏差', ogdesc='数値リストから平均・分散・標準偏差を自動計算。',
  h1='標準偏差計算機',
  lead='データのばらつきを数値で。カンマや改行で区切った数値を入れると、平均・分散・標準偏差を計算します。母集団・標本の両方に対応。',
  inputs='''    <h2>📈 数値を入れる</h2>
    <div class="field"><label>数値（カンマ・改行・スペース区切り）</label><textarea id="data" rows="4" style="width:100%;font-size:15px;padding:10px;border:1.5px solid var(--line);border-radius:10px;">50, 60, 70, 80, 90</textarea></div>
    <button class="btn btn-primary" id="calcBtn">計算する</button>''',
  result='''      <div class="label">標準偏差（標本）</div>
      <div class="big"><span id="big">0</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">平均</div><div class="v accent" id="mean">—</div></div>
      <div class="stat"><div class="k">標準偏差（母集団）</div><div class="v" id="pop">—</div></div>
      <div class="stat"><div class="k">分散・データ数</div><div class="v" id="var">—</div></div></div>''',
  article='''    <div class="note"><strong>標本と母集団</strong><br>標本標準偏差は「n−1」で割り（推定向け）、母集団標準偏差は「n」で割ります（全データが揃っている場合）。</div>
    <h2>標準偏差とは</h2>
    <p>標準偏差は、データが平均からどれだけばらついているかを表す指標です。値が大きいほどばらつきが大きく、小さいほど平均の近くに集まっています。求め方は、各データと平均の差を2乗して平均（これが分散）、その平方根が標準偏差。手元のデータ全体を分析するなら母集団、一部から全体を推定するなら標本を使います。テストの点数分析や品質管理などに使われます。</p>
    <h2>よくある質問</h2>'''+faq([
      ('母集団と標本どっち？','全データが揃っているなら母集団、一部のサンプルから推定するなら標本を使います。'),
      ('区切りは何でもいい？','カンマ・改行・スペースのいずれでもOK。数値以外は無視されます。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const raw=$('data').value||'';const arr=raw.split(/[\s,、，\n]+/).map(s=>parseFloat(s)).filter(v=>!isNaN(v));
    if(arr.length<1){$('big').textContent='—';$('sub').textContent='数値を入れてね';show();return;}
    const n=arr.length,mean=arr.reduce((a,b)=>a+b,0)/n;
    const ss=arr.reduce((a,b)=>a+(b-mean)*(b-mean),0);
    const popVar=ss/n, sampVar=n>1?ss/(n-1):0;
    const popSd=Math.sqrt(popVar), sampSd=Math.sqrt(sampVar);
    const rd=x=>Math.round(x*1000)/1000;
    $('big').textContent=rd(sampSd).toLocaleString('ja-JP');
    $('sub').textContent=`データ ${n}個`;$('mean').textContent=rd(mean);
    $('pop').textContent=rd(popSd);$('var').textContent='分散'+rd(sampVar)+' / '+n+'個';
    SHARE=`標準偏差計算機、${n}個のデータで 平均${rd(mean)}・標準偏差${rd(sampSd)} でした📈`;show();}
''')

# ============================================================
# 8. 体積計算（体積 計算 200/KD0/TP1400）
# ============================================================
add(id='taiseki-keisan', emoji='📦',
  title='体積計算機｜立方体・直方体・円柱・球・円錐の体積を計算｜シミュラボ',
  desc='形状を選んで寸法を入れるだけで、立方体・直方体・円柱・球・円錐の体積を自動計算する無料ツール。リットル換算も表示します。',
  ogtitle='体積計算機｜直方体・円柱・球などを計算', ogdesc='形状と寸法から体積を自動計算。リットル換算も。',
  h1='体積計算機',
  lead='箱や筒、ボールの体積は?形を選んで寸法を入れるだけで、体積を計算します。水槽の容量やリットル換算にも。',
  inputs='''    <h2>📦 形と寸法を入れる</h2>
    <div class="field"><label>形状</label><select id="shape">
      <option value="cube">立方体（一辺）</option><option value="box" selected>直方体（縦・横・高さ）</option>
      <option value="cyl">円柱（半径・高さ）</option><option value="sphere">球（半径）</option><option value="cone">円錐（半径・高さ）</option></select></div>
    <div class="row"><div class="field"><label id="lA">縦</label><input type="number" id="A" value="10" min="0" inputmode="decimal"></div>
    <div class="field"><label id="lB">横</label><input type="number" id="B" value="20" min="0" inputmode="decimal"></div></div>
    <div class="field"><label id="lC">高さ</label><input type="number" id="C" value="15" min="0" inputmode="decimal"></div>
    <p class="hint" style="margin:2px 0 0;">単位はcmで入れるとリットル換算も表示します。</p>
    <button class="btn btn-primary" id="calcBtn">体積を計算</button>''',
  result='''      <div class="label">体積</div>
      <div class="big"><span id="big">0</span><span class="unit">立方単位</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">cm³ なら</div><div class="v accent" id="liter">—</div></div></div>''',
  article='''    <div class="note"><strong>体積の公式</strong><br>立方体 a³／直方体 縦×横×高さ／円柱 πr²h／球 4/3πr³／円錐 1/3πr²h</div>
    <h2>体積の計算方法</h2>
    <p>体積は立体が占める空間の大きさです。直方体は「縦×横×高さ」、円柱は「底面積（πr²）×高さ」、球は「4/3×π×半径³」で求めます。寸法をcmで入れた場合、1リットル＝1,000cm³なので、cm³の値を1,000で割るとリットルに換算できます。水槽の容量計算や、収納・梱包のサイズ確認に便利です。</p>
    <h2>よくある質問</h2>'''+faq([
      ('単位は何でもいい？','はい。同じ単位で入れれば、その単位の3乗が体積になります。'),
      ('リットルにしたい','cmで入力すれば、cm³÷1000でリットル換算を表示します。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  const LBL={cube:['一辺','',''],box:['縦','横','高さ'],cyl:['半径','高さ',''],sphere:['半径','',''],cone:['半径','高さ','']};
  function upd(){const s=$('shape').value,l=LBL[s];$('lA').textContent=l[0];
    $('lB').parentElement.style.display=l[1]?'':'none';$('lB').previousElementSibling;$('lB').parentElement.querySelector('label').textContent=l[1]||'';
    $('lC').parentElement.style.display=l[2]?'':'none';$('lC').textContent=l[2]||'';}
  function calc(){const s=$('shape').value,a=Math.max(0,+$('A').value||0),b=Math.max(0,+$('B').value||0),c=Math.max(0,+$('C').value||0),PI=Math.PI;let v=0,name='';
    if(s==='cube'){v=a*a*a;name='立方体';}
    else if(s==='box'){v=a*b*c;name='直方体';}
    else if(s==='cyl'){v=PI*a*a*b;name='円柱';}
    else if(s==='sphere'){v=4/3*PI*a*a*a;name='球';}
    else{v=1/3*PI*a*a*b;name='円錐';}
    const rv=Math.round(v*1000)/1000;
    $('big').textContent=rv.toLocaleString('ja-JP');$('sub').textContent=name+'の体積';
    $('liter').textContent=(Math.round(v/1000*1000)/1000).toLocaleString('ja-JP')+' L';
    SHARE=`体積計算機、${name}の体積は ${rv} 立方単位（${Math.round(v/1000*1000)/1000}L）でした📦`;show();}
  $('shape').addEventListener('change',upd);upd();
''')

# ============================================================
# 9. 約分計算（約分 計算）
# ============================================================
add(id='yakubun-keisan', emoji='➗',
  title='約分計算機｜分数を約分・帯分数・小数にすぐ変換｜シミュラボ',
  desc='分子と分母を入れるだけで、分数を約分（いちばん簡単な分数）し、帯分数・小数にも変換する無料ツール。最大公約数も表示します。',
  ogtitle='約分計算機｜分数を約分・帯分数・小数に', ogdesc='分子・分母から約分・帯分数・小数・最大公約数を計算。',
  h1='約分計算機',
  lead='この分数、約分するとどうなる?分子と分母を入れると、いちばん簡単な分数に約分し、帯分数・小数にも直します。',
  inputs='''    <h2>➗ 分数を入れる</h2>
    <div class="row"><div class="field"><label>分子</label><input type="number" id="num" value="24" inputmode="numeric"></div>
    <div class="field"><label>分母</label><input type="number" id="den" value="36" min="1" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">約分する</button>''',
  result='''      <div class="label">約分した分数</div>
      <div class="big" style="font-size:34px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">帯分数</div><div class="v accent" id="mixed">—</div></div>
      <div class="stat"><div class="k">小数</div><div class="v" id="dec">—</div></div>
      <div class="stat"><div class="k">最大公約数</div><div class="v" id="g">—</div></div></div>''',
  article='''    <div class="note"><strong>約分のやり方</strong><br>分子と分母を、その最大公約数（GCD）で割ると、いちばん簡単な分数になります。</div>
    <h2>約分とは</h2>
    <p>約分は、分数の分子と分母を同じ数で割って、より簡単な分数にすることです。たとえば24/36は、分子・分母の最大公約数12で割ると2/3になります。約分しても分数の値（大きさ）は変わりません。仮分数（分子≧分母）は、帯分数（整数＋真分数）にも直せます。計算の見直しや、答え合わせに使えます。</p>
    <h2>よくある質問</h2>'''+faq([
      ('最大公約数って？','分子と分母を割り切れる最大の数です。これで割ると一度で約分できます。'),
      ('帯分数とは？','「2と1/3」のように整数と分数を組み合わせた表し方です。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function gcd(a,b){a=Math.abs(a);b=Math.abs(b);while(b){[a,b]=[b,a%b];}return a||1;}
  function calc(){let nu=Math.trunc(+$('num').value||0),de=Math.trunc(+$('den').value||0);
    if(de===0){$('big').textContent='—';$('sub').textContent='分母に0は使えません';show();return;}
    const sign=(nu<0)!==(de<0)?-1:1;nu=Math.abs(nu);de=Math.abs(de);
    const g=gcd(nu,de),sn=nu/g,sd=de/g;
    $('big').textContent=(sign<0?'-':'')+sn+' / '+sd;
    $('sub').textContent=`${(sign<0?'-':'')}${Math.abs(+$('num').value||0)} / ${Math.abs(+$('den').value||0)} を約分`;
    // 帯分数
    let mixed='—';if(sn>=sd&&sd!==0){const w=Math.floor(sn/sd),r=sn%sd;mixed=(sign<0?'-':'')+(r===0?(''+w):(w+' と '+r+'/'+sd));}
    else mixed=(sign<0?'-':'')+sn+'/'+sd;
    $('mixed').textContent=mixed;$('dec').textContent=(sign*sn/sd).toFixed(4).replace(/\.?0+$/,'');$('g').textContent=g;
    SHARE=`約分計算機、${nu}/${de} ＝ ${(sign<0?'-':'')}${sn}/${sd} でした➗`;show();}
''')

# ============================================================
# 10. 順列・組み合わせ計算（順列 組み合わせ 計算）
# ============================================================
add(id='junretsu-keisan', emoji='🎰',
  title='順列・組み合わせ計算機｜nPr・nCr・階乗をすぐ計算｜シミュラボ',
  desc='n個からr個を選ぶ順列(nPr)・組み合わせ(nCr)・階乗(n!)を自動計算する無料ツール。くじや当選確率、場合の数の計算に使えます。',
  ogtitle='順列・組み合わせ計算機｜nPr・nCr・階乗', ogdesc='n個からr個の順列・組み合わせ・階乗を自動計算。',
  h1='順列・組み合わせ計算機',
  lead='「5人から3人を選ぶ」は何通り?n個からr個を選ぶ順列(nPr)・組み合わせ(nCr)・階乗(n!)を計算します。場合の数・確率の計算に。',
  inputs='''    <h2>🎰 数を入れる</h2>
    <div class="row"><div class="field"><label>n（全体の数）</label><input type="number" id="n" value="5" min="0" max="170" inputmode="numeric"></div>
    <div class="field"><label>r（選ぶ数）</label><input type="number" id="r" value="3" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">計算する</button>''',
  result='''      <div class="label">組み合わせ nCr（順番を区別しない）</div>
      <div class="big"><span id="big">0</span><span class="unit">通り</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">順列 nPr（順番を区別）</div><div class="v accent" id="perm">—</div></div>
      <div class="stat"><div class="k">n の階乗（n!）</div><div class="v" id="fact">—</div></div></div>''',
  article='''    <div class="note"><strong>公式</strong><br>順列 nPr ＝ n!÷(n−r)!／組み合わせ nCr ＝ n!÷(r!×(n−r)!)／階乗 n! ＝ n×(n−1)×…×1</div>
    <h2>順列と組み合わせの違い</h2>
    <p>順列(nPr)は「順番を区別して」並べる場合の数、組み合わせ(nCr)は「順番を区別せず」選ぶ場合の数です。たとえば5人から3人を選ぶとき、組み合わせは10通り、順番（並び順）まで区別する順列は60通り。くじ引きの当選確率、座席の並び、チーム分けなど「場合の数」を求めるときに使います。階乗(n!)は1からnまでの整数をすべて掛けた数です。</p>
    <h2>よくある質問</h2>'''+faq([
      ('nPrとnCrどっちを使う？','順番が意味を持つなら順列(nPr)、選ぶだけで順番は関係ないなら組み合わせ(nCr)です。'),
      ('大きい数は？','階乗は急激に大きくなります。nが大きいと近似表示になる場合があります。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function fact(n){let f=1;for(let i=2;i<=n;i++)f*=i;return f;}
  function calc(){const n=Math.max(0,Math.trunc(+$('n').value||0)),r=Math.max(0,Math.trunc(+$('r').value||0));
    if(r>n){$('big').textContent='—';$('sub').textContent='r は n 以下にしてね';show();return;}
    let nPr=1;for(let i=0;i<r;i++)nPr*=(n-i);
    let nCr=nPr;for(let i=2;i<=r;i++)nCr/=i;nCr=Math.round(nCr);
    const f=fact(n);
    const fmt=x=>x>=1e15?x.toExponential(3):Math.round(x).toLocaleString('ja-JP');
    $('big').textContent=fmt(nCr);$('sub').textContent=`${n}個から${r}個を選ぶ`;
    $('perm').textContent=fmt(nPr)+'通り';$('fact').textContent=fmt(f);
    SHARE=`順列・組み合わせ計算機、${n}個から${r}個は 組み合わせ${fmt(nCr)}通り・順列${fmt(nPr)}通り でした🎰`;show();
    const el=$('big'),tv=nCr,t0=performance.now();(function s(t){const p=Math.min(1,(t-t0)/700);el.textContent=fmt(Math.round(tv*p));if(p<1)requestAnimationFrame(s);else el.textContent=fmt(tv);})(performance.now());}
''')

if __name__=='__main__':
    render()
    print(f'tool3 done. {len(SIMS)} sims.')
