# -*- coding: utf-8 -*-
"""シミュラボ：全カテゴリ3本ずつ補充 その2（work/study/kids/pet/health/uranai）。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq, write_all

SIMS=[]
def add(**k): SIMS.append(k)

# ===== 仕事・働き方 =====
add(id='nenshu-tedori', cat='仕事・働き方', emoji='💴',
  title='年収手取りシミュレーター｜額面と手取りはどれだけ違う？｜シミュラボ',
  desc='額面年収から、税金・社会保険料を概算で引いた手取り年収・月の手取り・控除額を試算する無料シミュレーター。',
  ogtitle='年収手取りシミュレーター｜手取りはいくら？', ogdesc='額面年収から手取り・月収・控除額を概算で試算。',
  h1='年収手取りシミュレーター',
  lead='「年収◯万」と言っても、手元に残る額は別物。額面年収から、税金・社会保険料を引いた手取りの目安を出します（独身・概算）。',
  inputs='''    <h2>💴 条件を入れる</h2>
    <div class="field"><label>額面年収 <span class="hint">（万円）</span></label><input type="number" id="g" value="500" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">手取りを見る</button>''',
  result='''      <div class="label">手取り年収（概算）</div>
      <div class="big"><span id="big">0</span><span class="unit">万円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">月の手取り</div><div class="v accent" id="mo">—</div></div>
      <div class="stat"><div class="k">控除の合計</div><div class="v" id="hiku">—</div></div>
      <div class="stat"><div class="k">手取り率</div><div class="v" id="rate">—</div></div></div>''',
  article='''    <h2>手取りの考え方</h2>
    <div class="note"><strong>概算の内訳</strong><br>額面 −（所得税・住民税・健康保険・厚生年金・雇用保険）＝ 手取り<br>手取り率は年収が上がるほど下がります（おおむね75〜85％）。</div>
    <p>本ツールは独身・標準的な条件での概算です。扶養・各種控除・自治体で変わります。額面より手取りで生活設計するのが基本です。</p>
    <h2>よくある質問</h2>'''+faq([('正確な額？','いいえ。家族構成や控除で変わる概算です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const g=Math.max(0,+$('g').value||0);
    let rate;if(g<=300)rate=0.80;else if(g<=500)rate=0.78;else if(g<=700)rate=0.76;else if(g<=1000)rate=0.73;else rate=0.69;
    const net=g*rate;
    $('sub').textContent=`額面${num(g)}万円`;$('mo').textContent=num(net*10000/12)+'円';$('hiku').textContent=num(g-net)+'万円';$('rate').textContent=Math.round(rate*100)+'％';
    SHARE=`年収手取りシミュ、額面${num(g)}万円の手取りは約${num(net)}万円（月${num(net*10000/12)}円）でした💴\\n額面と手取り、違うなぁ。👇`;show();anim($('big'),0,net,900);}''')

add(id='shoushin-sa', cat='仕事・働き方', emoji='🏅',
  title='昇進の生涯賃金差シミュレーター｜役職が上がると生涯いくら違う？｜シミュラボ',
  desc='現在の年収と昇進後の年収、残りの勤続年数から、昇進した場合としない場合の生涯賃金の差を試算する無料シミュレーター。',
  ogtitle='昇進の生涯賃金差｜役職で生涯いくら違う？', ogdesc='昇進前後の年収から、生涯賃金の差を試算。',
  h1='昇進の生涯賃金差シミュレーター',
  lead='昇進すると、生涯ではどれだけ差がつく？現在の年収と昇進後の年収、残り勤続年数から、生涯賃金の差を出します。キャリアの判断材料に。',
  inputs='''    <h2>🏅 条件を入れる</h2>
    <div class="row"><div class="field"><label>今の年収 <span class="hint">（万円）</span></label><input type="number" id="now" value="500" min="0" inputmode="numeric"></div>
    <div class="field"><label>昇進後の年収 <span class="hint">（万円）</span></label><input type="number" id="up" value="650" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>残りの勤続年数 <span class="hint">（年）</span></label><input type="number" id="yr" value="20" min="1" max="50" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">生涯差を見る</button>''',
  result='''      <div class="label">昇進による生涯賃金差</div>
      <div class="big"><span id="big">0</span><span class="unit">万円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">年の差</div><div class="v" id="ydiff">—</div></div>
      <div class="stat"><div class="k">昇進後の生涯賃金</div><div class="v accent" id="upTotal">—</div></div>
      <div class="stat"><div class="k">残り勤続</div><div class="v" id="yv">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>生涯差 ＝（昇進後の年収 − 今の年収）× 残りの勤続年数</div>
    <p>年収差は1年では小さくても、残りの勤続年数ぶん積み上がると大きな差に。昇進にともなう責任・時間とのバランスも含めて判断を。転職での年収アップも同じ考え方で比較できます。</p>
    <h2>よくある質問</h2>'''+faq([('退職金や年金は？','含みません。年収ベースの概算です。退職金は役職で増えることが多いです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const now=Math.max(0,+$('now').value||0),up=Math.max(0,+$('up').value||0),yr=Math.max(1,+$('yr').value||1);const diff=(up-now)*yr;
    $('sub').textContent=`${num(now)}万 → ${num(up)}万・${yr}年`;$('ydiff').textContent=num(up-now)+'万円';$('upTotal').textContent=num(up*yr)+'万円';$('yv').textContent=yr+'年';
    SHARE=`昇進の生涯賃金差シミュ、生涯で約${num(diff)}万円の差がつく計算でした🏅\\nキャリアの一歩は大きい…！👇`;show();anim($('big'),0,Math.abs(diff),900);}''')

add(id='fukugyo-mokuhyou', cat='仕事・働き方', emoji='💼',
  title='副業 目標達成シミュレーター｜月◯万まであと何件・何時間？｜シミュラボ',
  desc='副業の目標月収・1件あたりの単価・1件にかかる時間から、目標達成に必要な件数と作業時間を試算する無料シミュレーター。',
  ogtitle='副業 目標達成シミュレーター｜あと何件？', ogdesc='目標月収と単価から、必要な件数・作業時間を試算。',
  h1='副業 目標達成シミュレーター',
  lead='副業で月◯万円を目指すには、あと何件・何時間？目標月収と単価・作業時間から、必要な件数と時間を逆算します。現実的かどうかの判断に。',
  inputs='''    <h2>💼 条件を入れる</h2>
    <div class="row"><div class="field"><label>目標の月収 <span class="hint">（円）</span></label><input type="number" id="goal" value="50000" min="0" inputmode="numeric"></div>
    <div class="field"><label>1件の単価 <span class="hint">（円）</span></label><input type="number" id="price" value="5000" min="1" inputmode="numeric"></div></div>
    <div class="field"><label>1件にかかる時間 <span class="hint">（時間）</span></label><input type="number" id="hours" value="3" min="0.1" step="0.1" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">必要な件数を見る</button>''',
  result='''      <div class="label">月に必要な件数</div>
      <div class="big"><span id="big">0</span><span class="unit">件</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">月の作業時間</div><div class="v accent" id="time">—</div></div>
      <div class="stat"><div class="k">実質時給</div><div class="v" id="jikyu">—</div></div>
      <div class="stat"><div class="k">1日あたり</div><div class="v" id="day">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>必要件数 ＝ 目標月収 ÷ 1件の単価<br>作業時間 ＝ 必要件数 × 1件の時間／実質時給 ＝ 単価 ÷ 1件の時間</div>
    <p>「実質時給」を見ると、その副業の効率が分かります。単価を上げる・作業を速くする・仕組み化するほど、同じ時間でも稼ぎが増えます。本業と無理なく両立できる範囲で。</p>
    <h2>よくある質問</h2>'''+faq([('税金は？','副業所得が年20万円超なら確定申告が必要な場合があります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const goal=Math.max(0,+$('goal').value||0),price=Math.max(1,+$('price').value||1),hours=Math.max(0.1,+$('hours').value||0.1);
    const cnt=goal/price,time=cnt*hours,jikyu=price/hours;
    $('sub').textContent=`目標${num(goal)}円・単価${num(price)}円`;$('time').textContent=num(time)+'時間';$('jikyu').textContent=yen(jikyu)+'/時';$('day').textContent=(time/30).toFixed(1)+'時間';
    SHARE=`副業 目標達成シミュ、月${num(goal)}円には月${num(cnt)}件・${num(time)}時間（実質時給${yen(jikyu)}）でした💼\\nコツコツいこ。👇`;show();anim($('big'),0,cnt,900);}''')

# ===== 学生・勉強 =====
add(id='juku-sougaku', cat='学生・勉強', emoji='🏫',
  title='塾代 総額シミュレーター｜中学〜高校で塾にいくらかかる？｜シミュラボ',
  desc='月の塾費用と通う年数、季節講習費から、塾にかかる総額を試算する無料シミュレーター。',
  ogtitle='塾代 総額シミュレーター｜塾にいくらかかる？', ogdesc='月の塾代と年数・講習費から、塾の総額を試算。',
  h1='塾代 総額シミュレーター',
  lead='塾は月謝だけでなく、季節講習や教材費も。月の費用・通う年数・講習費から、塾にかかる総額を出します。教育費の計画に。',
  inputs='''    <h2>🏫 条件を入れる</h2>
    <div class="row"><div class="field"><label>月の塾費用 <span class="hint">（円）</span></label><input type="number" id="m" value="30000" min="0" inputmode="numeric"></div>
    <div class="field"><label>通う年数 <span class="hint">（年）</span></label><input type="number" id="yr" value="3" min="0" max="12" inputmode="numeric"></div></div>
    <div class="field"><label>年間の講習・教材費 <span class="hint">（円）</span></label><input type="number" id="extra" value="200000" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">総額を見る</button>''',
  result='''      <div class="label">塾代の総額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">月謝の合計</div><div class="v" id="mon">—</div></div>
      <div class="stat"><div class="k">講習費の合計</div><div class="v" id="ex">—</div></div>
      <div class="stat"><div class="k">年あたり</div><div class="v accent" id="yv">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>総額 ＝ 月謝 × 12 × 年数 ＋ 年間の講習・教材費 × 年数</div>
    <p>受験学年は講習費が一気に増える傾向。早めに見積もっておくと家計の計画が立てやすくなります。集団・個別・オンラインで費用は大きく変わるので、目的に合った選択を。</p>
    <h2>よくある質問</h2>'''+faq([('相場は？','集団塾で月2〜4万円、個別はさらに高めが目安。学年・地域で差があります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const m=Math.max(0,+$('m').value||0),yr=Math.max(0,+$('yr').value||0),ex=Math.max(0,+$('extra').value||0);
    const mon=m*12*yr,exTotal=ex*yr,total=mon+exTotal;
    $('sub').textContent=`月${num(m)}円 × ${yr}年 ＋ 講習${num(ex)}円/年`;$('mon').textContent=yen(mon);$('ex').textContent=yen(exTotal);$('yv').textContent=yr>0?yen(total/yr):'—';
    SHARE=`塾代 総額シミュ、${yr}年で約${yen(total)}でした🏫\\n教育費は計画的に…！👇`;show();anim($('big'),0,total,900);}''')

add(id='gakureki-chingin', cat='学生・勉強', emoji='🎓',
  title='学歴別 生涯賃金シミュレーター｜進路で生涯年収はどう違う？｜シミュラボ',
  desc='最終学歴を選ぶと、一般的な統計をもとにした生涯賃金の目安と、学歴間の差を表示する無料シミュレーター。',
  ogtitle='学歴別 生涯賃金｜進路で生涯年収は違う？', ogdesc='最終学歴から生涯賃金の目安と学歴間の差を表示。',
  h1='学歴別 生涯賃金シミュレーター',
  lead='学歴によって、生涯に稼ぐ額はどれくらい違う？最終学歴を選ぶと、統計にもとづく生涯賃金の目安を表示します（あくまで平均で、人生の価値は学歴では決まりません）。',
  inputs='''    <h2>🎓 条件を選ぶ</h2>
    <div class="field"><label>最終学歴</label><select id="edu"><option value="2.0">高卒</option><option value="2.3">専門・短大卒</option><option value="2.7" selected>大卒</option><option value="3.1">大学院卒</option></select></div>
    <button class="btn btn-primary" id="calcBtn">生涯賃金の目安を見る</button>''',
  result='''      <div class="label">生涯賃金の目安</div>
      <div class="big"><span id="big">0</span><span class="unit">億円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">高卒との差</div><div class="v accent" id="diff">—</div></div>
      <div class="stat"><div class="k">月額換算(40年)</div><div class="v" id="mo">—</div></div>
      <div class="stat"><div class="k">学歴</div><div class="v" id="ev">—</div></div></div>''',
  article='''    <h2>あくまで平均の話</h2>
    <div class="note"><strong>目安（統計ベース）</strong><br>生涯賃金は学歴で平均的に差が出るとされますが、職種・企業・本人の努力で大きく変わります。</div>
    <p>学歴は選択肢を広げる一つの要素ですが、人生の豊かさや成功は学歴だけで決まりません。数字は「傾向」として参考に。自分に合った道を選ぶのがいちばんです。</p>
    <h2>よくある質問</h2>'''+faq([('絶対こうなる？','いいえ。平均的な傾向で、個人差が非常に大きいです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const oku=+$('edu').value||2.7;const base=2.0;
    $('sub').textContent=`${sel('edu').text}・平均の目安`;$('diff').textContent='+'+((oku-base).toFixed(1))+'億円';$('mo').textContent=num(oku*100000000/40/12)+'円';$('ev').textContent=sel('edu').text;
    SHARE=`学歴別 生涯賃金シミュ、${sel('edu').text}の目安は約${oku.toFixed(1)}億円でした🎓\\n※あくまで平均。道は自分次第！👇`;show();anim($('big'),0,oku,900,1);}''')

add(id='pomodoro', cat='学生・勉強', emoji='🍅',
  title='勉強計画ポモドーロシミュレーター｜目標時間に何セット必要？｜シミュラボ',
  desc='目標の勉強時間とポモドーロ（25分集中＋5分休憩）の設定から、必要なセット数と休憩込みの所要時間を計算する無料シミュレーター。',
  ogtitle='勉強計画ポモドーロ｜何セット必要？', ogdesc='目標勉強時間から、ポモドーロのセット数と所要を計算。',
  h1='勉強計画ポモドーロシミュレーター',
  lead='集中が続く「ポモドーロ・テクニック」で勉強計画を。目標の勉強時間から、必要なセット数と休憩を含めた所要時間を計算します。',
  inputs='''    <h2>🍅 条件を入れる</h2>
    <div class="field"><label>目標の勉強時間 <span class="hint">（時間）</span></label><input type="number" id="goal" value="3" min="0.5" step="0.5" inputmode="decimal"></div>
    <div class="row"><div class="field"><label>1セットの集中 <span class="hint">（分）</span></label><input type="number" id="work" value="25" min="5" inputmode="numeric"></div>
    <div class="field"><label>休憩 <span class="hint">（分）</span></label><input type="number" id="rest" value="5" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">計画を立てる</button>''',
  result='''      <div class="label">必要なセット数</div>
      <div class="big"><span id="big">0</span><span class="unit">セット</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">休憩込みの所要</div><div class="v accent" id="total">—</div></div>
      <div class="stat"><div class="k">休憩の合計</div><div class="v" id="restT">—</div></div>
      <div class="stat"><div class="k">長い休憩(4回ごと)</div><div class="v" id="long">—</div></div></div>''',
  article='''    <h2>ポモドーロ・テクニック</h2>
    <div class="note"><strong>計算式</strong><br>セット数 ＝ 目標勉強時間 ÷ 1セットの集中時間<br>所要 ＝ セット数 ×（集中 ＋ 休憩）</div>
    <p>「25分集中＋5分休憩」を1セットとし、4セットごとに長めの休憩を取る勉強法。短く区切ることで集中が続き、ダラダラ防止に。タイマーを使って実践してみてください。</p>
    <h2>よくある質問</h2>'''+faq([('25分じゃ短い？','人によります。集中が続くなら50分などに調整してOKです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const goal=Math.max(0,+$('goal').value||0)*60,work=Math.max(1,+$('work').value||1),rest=Math.max(0,+$('rest').value||0);
    const sets=Math.ceil(goal/work),total=sets*(work+rest),longRest=Math.floor(sets/4);
    function hm(m){m=Math.round(m);return Math.floor(m/60)+'時間'+(m%60)+'分';}
    $('sub').textContent=`目標${$('goal').value}時間・${work}分集中＋${rest}分休憩`;$('total').textContent=hm(total);$('restT').textContent=hm(sets*rest);$('long').textContent=longRest+'回';
    SHARE=`勉強計画ポモドーロシミュ、目標${$('goal').value}時間には${sets}セット（休憩込み${hm(total)}）でした🍅\\n集中して頑張ろ！👇`;show();anim($('big'),0,sets,900);}''')

# ===== 子ども・育児 =====
add(id='nyuuji-hiyou', cat='子ども・育児', emoji='🍼',
  title='0歳の育児費シミュレーター｜赤ちゃん1年目、いくらかかる？｜シミュラボ',
  desc='ミルク・おむつ・衣類・育児用品など、赤ちゃんの最初の1年にかかる費用の目安を試算する無料シミュレーター。',
  ogtitle='0歳の育児費｜赤ちゃん1年目いくら？', ogdesc='ミルク・おむつ・用品から、0歳の年間育児費を試算。',
  h1='0歳の育児費シミュレーター',
  lead='赤ちゃんを迎える最初の1年、何にいくらかかる？ミルク・おむつ・衣類・育児用品の費用から、0歳の年間育児費の目安を出します（出産準備の計画に）。',
  inputs='''    <h2>🍼 条件を入れる（月額）</h2>
    <div class="row"><div class="field"><label>ミルク・離乳食 <span class="hint">（円/月）</span></label><input type="number" id="milk" value="8000" min="0" inputmode="numeric"></div>
    <div class="field"><label>おむつ <span class="hint">（円/月）</span></label><input type="number" id="omutsu" value="5000" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>衣類・雑費 <span class="hint">（円/月）</span></label><input type="number" id="other" value="5000" min="0" inputmode="numeric"></div>
    <div class="field"><label>初期の育児用品 <span class="hint">（円・一括）</span></label><input type="number" id="init" value="150000" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">1年目の費用を見る</button>''',
  result='''      <div class="label">0歳1年目の育児費</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">月の費用</div><div class="v" id="mo">—</div></div>
      <div class="stat"><div class="k">育児用品(初期)</div><div class="v" id="iv">—</div></div>
      <div class="stat"><div class="k">出産育児一時金で</div><div class="v accent" id="hojo">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>1年目 ＝（ミルク＋おむつ＋衣類等）× 12 ＋ 初期の育児用品</div>
    <p>ベビーカー・チャイルドシート・ベビーベッドなどの初期費用がまとまって必要に。お下がりやレンタル、フリマの活用で抑えられます。出産育児一時金などの公的支援も忘れずに。</p>
    <h2>よくある質問</h2>'''+faq([('医療費は？','乳幼児医療費助成で自己負担が抑えられる自治体が多いです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const milk=Math.max(0,+$('milk').value||0),om=Math.max(0,+$('omutsu').value||0),ot=Math.max(0,+$('other').value||0),init=Math.max(0,+$('init').value||0);
    const mo=milk+om+ot,total=mo*12+init;
    $('sub').textContent=`月${num(mo)}円 × 12 ＋ 初期${num(init)}円`;$('mo').textContent=yen(mo);$('iv').textContent=yen(init);$('hojo').textContent='約'+num(Math.max(0,total-500000))+'円(差引)';
    SHARE=`0歳の育児費シミュ、1年目で約${yen(total)}でした🍼\\n準備は計画的に…！👇`;show();anim($('big'),0,total,900);}''')

add(id='kodomo-shokuhi', cat='子ども・育児', emoji='🍱',
  title='子どもの生涯食費シミュレーター｜成人まで食費はいくら？｜シミュラボ',
  desc='子どもの1日あたりの食費から、成人（または独立）までにかかる食費の総額を試算するエンタメシミュレーター。',
  ogtitle='子どもの生涯食費｜成人まで食費はいくら？', ogdesc='1日の食費から、子どもの成人までの食費総額を試算。',
  h1='子どもの生涯食費シミュレーター',
  lead='よく食べる我が子。成人までの食費って、トータルでいくら？1日の食費から、独立までにかかる食費の総額を出します（食べてくれるのは元気な証拠）。',
  inputs='''    <h2>🍱 条件を入れる</h2>
    <div class="row"><div class="field"><label>1日の食費 <span class="hint">（円・平均）</span></label><input type="number" id="day" value="800" min="0" inputmode="numeric"></div>
    <div class="field"><label>今の年齢 <span class="hint">（歳）</span></label><input type="number" id="age" value="5" min="0" max="22" inputmode="numeric"></div></div>
    <div class="field"><label>独立する年齢 <span class="hint">（歳）</span></label><input type="number" id="end" value="22" min="1" max="30" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">食費の総額を見る</button>''',
  result='''      <div class="label">独立までの食費（残り）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">年間の食費</div><div class="v" id="year">—</div></div>
      <div class="stat"><div class="k">残りの年数</div><div class="v" id="yr">—</div></div>
      <div class="stat"><div class="k">茶碗のごはん換算</div><div class="v accent" id="rice">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>残りの食費 ＝ 1日の食費 × 365 ×（独立年齢 − 今の年齢）</div>
    <p>食べ盛りになると食費はぐんと増えます。でもそれは元気に育っている証。数字にすると驚きますが、家族みんなで囲む食卓は、お金には代えられない時間です。</p>
    <h2>よくある質問</h2>'''+faq([('1日の食費の目安は？','幼児で数百円、中高生で千円超など年齢で大きく変わります。平均で入れてください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const day=Math.max(0,+$('day').value||0),age=Math.max(0,+$('age').value||0),end=Math.max(age+0.1,+$('end').value||1);const yr=end-age,total=day*365*yr;
    $('sub').textContent=`1日${num(day)}円 × ${num(yr)}年`;$('year').textContent=yen(day*365);$('yr').textContent=num(yr)+'年';$('rice').textContent=num(total/70)+'杯';
    SHARE=`子どもの生涯食費シミュ、独立まで残り約${yen(total)}でした🍱\\nたくさん食べて大きくなぁれ。👇`;show();anim($('big'),0,total,900);}''')

add(id='narai-goto', cat='子ども・育児', emoji='🎹',
  title='習い事 総額シミュレーター｜習い事に総額いくらかかる？｜シミュラボ',
  desc='習い事の月謝と続ける年数、発表会・道具代などから、習い事にかかる総額を試算する無料シミュレーター。',
  ogtitle='習い事 総額シミュレーター｜総額いくら？', ogdesc='月謝と年数・追加費用から、習い事の総額を試算。',
  h1='習い事 総額シミュレーター',
  lead='ピアノ、水泳、英語…習い事は月謝以外もかかります。月謝・続ける年数・発表会や道具代から、習い事の総額を出します。',
  inputs='''    <h2>🎹 条件を入れる</h2>
    <div class="row"><div class="field"><label>月謝 <span class="hint">（円）</span></label><input type="number" id="m" value="8000" min="0" inputmode="numeric"></div>
    <div class="field"><label>続ける年数 <span class="hint">（年）</span></label><input type="number" id="yr" value="6" min="0" max="18" inputmode="numeric"></div></div>
    <div class="field"><label>年間の発表会・道具代 <span class="hint">（円）</span></label><input type="number" id="extra" value="30000" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">総額を見る</button>''',
  result='''      <div class="label">習い事の総額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">月謝の合計</div><div class="v" id="mon">—</div></div>
      <div class="stat"><div class="k">発表会・道具</div><div class="v" id="ex">—</div></div>
      <div class="stat"><div class="k">年あたり</div><div class="v accent" id="yv">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>総額 ＝ 月謝 × 12 × 年数 ＋ 年間の追加費用 × 年数</div>
    <p>習い事は子どもの世界を広げる投資。一方で掛け持ちで負担が増えがちなので、本人が好きで続けられるものを優先するのが、お金の面でも満足度の面でも◎。</p>
    <h2>よくある質問</h2>'''+faq([('いくつも掛け持ちしたい','このツールで1つずつ出して合計すると全体像が見えます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const m=Math.max(0,+$('m').value||0),yr=Math.max(0,+$('yr').value||0),ex=Math.max(0,+$('extra').value||0);
    const mon=m*12*yr,exT=ex*yr,total=mon+exT;
    $('sub').textContent=`月${num(m)}円 × ${yr}年 ＋ 年${num(ex)}円`;$('mon').textContent=yen(mon);$('ex').textContent=yen(exT);$('yv').textContent=yr>0?yen(total/yr):'—';
    SHARE=`習い事 総額シミュ、${yr}年で約${yen(total)}でした🎹\\n好きを伸ばす投資！👇`;show();anim($('big'),0,total,900);}''')

# ===== ペット =====
add(id='pet-iryou', cat='ペット', emoji='🏥',
  title='ペットの生涯医療費シミュレーター｜一生でいくらかかる？｜シミュラボ',
  desc='年間の通院・ワクチン費用と、生涯に想定される手術・治療費から、ペットの生涯医療費の目安を試算する無料シミュレーター。',
  ogtitle='ペットの生涯医療費｜一生でいくらかかる？', ogdesc='年間の通院費と手術費から、生涯医療費を試算。',
  h1='ペットの生涯医療費シミュレーター',
  lead='大切な家族の健康。年間の通院・ワクチン費と、想定される手術・治療費から、ペットの生涯医療費の目安を出します。ペット保険を考える参考に。',
  inputs='''    <h2>🏥 条件を入れる</h2>
    <div class="row"><div class="field"><label>年間の通院・ワクチン費 <span class="hint">（円）</span></label><input type="number" id="year" value="40000" min="0" inputmode="numeric"></div>
    <div class="field"><label>想定寿命 <span class="hint">（年）</span></label><input type="number" id="life" value="15" min="1" max="30" inputmode="numeric"></div></div>
    <div class="field"><label>生涯の手術・大きな治療費 <span class="hint">（円・想定）</span></label><input type="number" id="surgery" value="300000" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">生涯医療費を見る</button>''',
  result='''      <div class="label">生涯の医療費の目安</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">通院・ワクチン計</div><div class="v" id="reg">—</div></div>
      <div class="stat"><div class="k">手術・治療</div><div class="v" id="sur">—</div></div>
      <div class="stat"><div class="k">月あたり積立目安</div><div class="v accent" id="save">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>生涯医療費 ＝ 年間の通院費 × 寿命 ＋ 想定の手術・治療費</div>
    <p>ペットは人間と違い公的保険がなく、医療費は全額自己負担。シニアになると通院が増えます。月々の積立や、ペット保険での備えを検討しておくと安心です。</p>
    <h2>よくある質問</h2>'''+faq([('保険に入るべき？','高額治療への備えになります。本ツールで自己負担額を把握して判断を。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const year=Math.max(0,+$('year').value||0),life=Math.max(1,+$('life').value||1),sur=Math.max(0,+$('surgery').value||0);
    const reg=year*life,total=reg+sur;
    $('sub').textContent=`年${num(year)}円 × ${life}年 ＋ 手術${num(sur)}円`;$('reg').textContent=yen(reg);$('sur').textContent=yen(sur);$('save').textContent=yen(total/(life*12));
    SHARE=`ペットの生涯医療費シミュ、約${yen(total)}でした🏥\\n月${yen(total/(life*12))}の積立で備えよ。👇`;show();anim($('big'),0,total,900);}''')

add(id='pet-toilet', cat='ペット', emoji='🚽',
  title='ペットのトイレ用品 年間費シミュレーター｜砂・シーツ代は年いくら？｜シミュラボ',
  desc='猫砂やペットシーツの1袋の価格と消費ペースから、トイレ用品にかかる年間・生涯の費用を計算する無料シミュレーター。',
  ogtitle='ペットのトイレ用品 年間費｜砂・シーツ代は？', ogdesc='猫砂・シーツの価格と消費から、年間費用を計算。',
  h1='ペットのトイレ用品 年間費シミュレーター',
  lead='地味に効く猫砂・ペットシーツ代。1袋の価格と消費ペースから、トイレ用品の年間・生涯費用を出します。まとめ買いの参考にも。',
  inputs='''    <h2>🚽 条件を入れる</h2>
    <div class="row"><div class="field"><label>1袋の価格 <span class="hint">（円）</span></label><input type="number" id="price" value="1200" min="0" inputmode="numeric"></div>
    <div class="field"><label>1袋が何日もつ <span class="hint">（日）</span></label><input type="number" id="days" value="14" min="1" inputmode="numeric"></div></div>
    <div class="field"><label>想定寿命 <span class="hint">（年）</span></label><input type="number" id="life" value="15" min="1" max="30" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">年間費を見る</button>''',
  result='''      <div class="label">年間のトイレ用品費</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1ヶ月あたり</div><div class="v" id="mo">—</div></div>
      <div class="stat"><div class="k">生涯で</div><div class="v accent" id="life2">—</div></div>
      <div class="stat"><div class="k">年間の使用袋数</div><div class="v" id="bags">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>年間費 ＝ 1袋の価格 ÷ もつ日数 × 365</div>
    <p>毎日使う消耗品なので、年・生涯ではまとまった額に。まとめ買いやサブスク、コスパの良い商品選びで節約できます。우리の子の快適さは保ちつつ、賢く。</p>
    <h2>よくある質問</h2>'''+faq([('多頭飼いは？','頭数分でもつ日数が短くなります。実際の消費ペースで入れてください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const price=Math.max(0,+$('price').value||0),days=Math.max(1,+$('days').value||1),life=Math.max(1,+$('life').value||1);
    const year=price/days*365,lifeT=year*life,bags=365/days;
    $('sub').textContent=`1袋${num(price)}円・${days}日もち`;$('mo').textContent=yen(year/12);$('life2').textContent=yen(lifeT);$('bags').textContent=num(bags)+'袋';
    SHARE=`ペットのトイレ用品 年間費シミュ、年${yen(year)}・生涯${yen(lifeT)}でした🚽\\nまとめ買いで節約しよ。👇`;show();anim($('big'),0,year,900);}''')

add(id='pet-trim', cat='ペット', emoji='✂️',
  title='ペットのトリミング 年間費シミュレーター｜年でいくら？｜シミュラボ',
  desc='トリミング1回の料金と通う頻度から、トリミングにかかる年間・生涯費用を計算する無料シミュレーター。',
  ogtitle='ペットのトリミング 年間費｜年でいくら？', ogdesc='1回の料金と頻度から、トリミングの年間費用を計算。',
  h1='ペットのトリミング 年間費シミュレーター',
  lead='トリミングが必要な犬種は、定期的なお手入れ費がかかります。1回の料金と頻度から、年間・生涯のトリミング費を出します。',
  inputs='''    <h2>✂️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>1回の料金 <span class="hint">（円）</span></label><input type="number" id="price" value="6000" min="0" inputmode="numeric"></div>
    <div class="field"><label>年に通う回数 <span class="hint">（回）</span></label><input type="number" id="freq" value="8" min="0" max="52" inputmode="numeric"></div></div>
    <div class="field"><label>想定寿命 <span class="hint">（年）</span></label><input type="number" id="life" value="14" min="1" max="30" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">年間費を見る</button>''',
  result='''      <div class="label">年間のトリミング費</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1ヶ月あたり</div><div class="v" id="mo">—</div></div>
      <div class="stat"><div class="k">生涯で</div><div class="v accent" id="life2">—</div></div>
      <div class="stat"><div class="k">通う間隔</div><div class="v" id="span">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>年間費 ＝ 1回の料金 × 年の回数</div>
    <p>プードルやシュナウザーなど被毛が伸び続ける犬種は、月1回程度のトリミングが目安。爪切り・耳掃除はセルフでできる部分も。シャンプーだけ自宅で、などの工夫で節約も。</p>
    <h2>よくある質問</h2>'''+faq([('猫もトリミングする？','長毛種はカットやブラッシングが必要なことがあります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const price=Math.max(0,+$('price').value||0),freq=Math.max(0,+$('freq').value||0),life=Math.max(1,+$('life').value||1);
    const year=price*freq,lifeT=year*life;
    $('sub').textContent=`1回${num(price)}円 × 年${freq}回`;$('mo').textContent=yen(year/12);$('life2').textContent=yen(lifeT);$('span').textContent= freq>0?(12/freq).toFixed(1)+'ヶ月に1回':'—';
    SHARE=`ペットのトリミング 年間費シミュ、年${yen(year)}・生涯${yen(lifeT)}でした✂️\\nきれいでいようね。👇`;show();anim($('big'),0,year,900);}''')

# ===== 健康・カラダ =====
add(id='tabako-cost', cat='健康・カラダ', emoji='🚭',
  title='喫煙の生涯コストシミュレーター｜タバコ代、一生でいくら？｜シミュラボ',
  desc='1日の喫煙本数と1箱の価格から、タバコ代の年間・生涯コストと、本数の累計を計算する無料シミュレーター。',
  ogtitle='喫煙の生涯コスト｜タバコ代、一生でいくら？', ogdesc='1日の本数と価格から、タバコ代の生涯コストを計算。',
  h1='喫煙の生涯コストシミュレーター',
  lead='毎日のタバコ代、一生だといくら？1日の本数と1箱の価格から、年間・生涯のコストと吸う本数を出します（禁煙のモチベーションづくりに）。',
  inputs='''    <h2>🚭 条件を入れる</h2>
    <div class="row"><div class="field"><label>1日の本数 <span class="hint">（本）</span></label><input type="number" id="n" value="20" min="0" inputmode="numeric"></div>
    <div class="field"><label>1箱(20本)の価格 <span class="hint">（円）</span></label><input type="number" id="price" value="600" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>これからの年数 <span class="hint">（年）</span></label><input type="number" id="yr" value="40" min="1" max="80" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">生涯コストを見る</button>''',
  result='''      <div class="label">これからの生涯コスト</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1年で</div><div class="v" id="y1">—</div></div>
      <div class="stat"><div class="k">吸う本数(生涯)</div><div class="v accent" id="cnt">—</div></div>
      <div class="stat"><div class="k">海外旅行に換算</div><div class="v" id="trip">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>生涯コスト ＝ 1日の本数 ÷ 20 × 1箱の価格 × 365 × 年数</div>
    <p>お金だけでなく健康面のメリットも大きい禁煙。浮いたお金で旅行や趣味を楽しむ、と考えると一歩踏み出しやすいかも。健康への影響は専門家・医療機関にご相談を。</p>
    <h2>よくある質問</h2>'''+faq([('禁煙したらこの額が浮く？','はい。本ツールの金額が、そのまま将来の節約額になります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const n=Math.max(0,+$('n').value||0),price=Math.max(0,+$('price').value||0),yr=Math.max(1,+$('yr').value||1);
    const y1=n/20*price*365,total=y1*yr,cnt=n*365*yr;
    $('sub').textContent=`1日${n}本・1箱${num(price)}円・${yr}年`;$('y1').textContent=yen(y1);$('cnt').textContent=num(cnt)+'本';$('trip').textContent=num(total/200000)+'回';
    SHARE=`喫煙の生涯コストシミュ、これから約${yen(total)}でした🚭\\n禁煙すれば海外旅行${num(total/200000)}回分…！👇`;show();anim($('big'),0,total,900);}''')

add(id='kakuzato', cat='健康・カラダ', emoji='🧊',
  title='角砂糖シミュレーター｜その飲み物、砂糖は角砂糖何個分？｜シミュラボ',
  desc='飲み物の量と糖分濃度から、含まれる砂糖の量を角砂糖の個数に換算するエンタメシミュレーター。',
  ogtitle='角砂糖シミュレーター｜砂糖は角砂糖何個分？', ogdesc='飲み物の量と糖分から、砂糖を角砂糖の個数に換算。',
  h1='角砂糖シミュレーター',
  lead='甘い飲み物に、砂糖はどれくらい入ってる？飲み物を選ぶと、含まれる砂糖を「角砂糖の個数」に換算します。見えると、ちょっと飲み方を考えたくなるかも。',
  inputs='''    <h2>🧊 条件を選ぶ</h2>
    <div class="field"><label>飲み物</label><select id="drink"><option value="11">コーラ(500ml)</option><option value="13" selected>エナジードリンク(500ml)</option><option value="7">スポーツドリンク(500ml)</option><option value="12">フルーツジュース(500ml)</option><option value="5">微糖カフェラテ(300ml)</option><option value="20">タピオカミルクティー(500ml)</option></select></div>
    <div class="field"><label>1日に飲む杯数 <span class="hint">（杯）</span></label><input type="number" id="n" value="1" min="0" max="20" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">角砂糖に換算する</button>''',
  result='''      <div class="label">含まれる砂糖（角砂糖）</div>
      <div class="big"><span id="big">0</span><span class="unit">個分</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">砂糖の量</div><div class="v" id="g">—</div></div>
      <div class="stat"><div class="k">1年で(毎日)</div><div class="v accent" id="year">—</div></div>
      <div class="stat"><div class="k">カロリー</div><div class="v" id="kcal">—</div></div></div>''',
  article='''    <h2>角砂糖換算で見える化</h2>
    <div class="note"><strong>換算の目安</strong><br>角砂糖1個 ＝ 約4g／砂糖1g ＝ 約4kcal</div>
    <p>液体の糖分は気づかないうちに摂りすぎがち。WHO は1日の糖類を約25g（角砂糖6個分）以下にと推奨しています。たまの楽しみはOK、毎日の習慣は見直しのきっかけに。</p>
    <h2>よくある質問</h2>'''+faq([('砂糖ゼロ飲料なら？','糖類ゼロ表示の飲み物は角砂糖換算もほぼゼロになります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const g=(+$('drink').value||0),n=Math.max(0,+$('n').value||0);const totalG=g*n,cubes=totalG/4;
    $('sub').textContent=`${sel('drink').text} × ${n}杯`;$('g').textContent=num(totalG)+'g';$('year').textContent=num(totalG*365/1000)+'kg';$('kcal').textContent=num(totalG*4)+'kcal';
    SHARE=`角砂糖シミュ、${sel('drink').text}には角砂糖約${Math.round(cubes)}個分の砂糖が🧊\\n見えると飲み方考えるなぁ…！👇`;show();anim($('big'),0,cubes,900);}''')

add(id='kaidan', cat='健康・カラダ', emoji='🪜',
  title='階段カロリーシミュレーター｜階段で1年どれだけ燃える？｜シミュラボ',
  desc='1日に上る階段の段数と体重から、消費カロリーと1年・10年での累計、エレベーターを使わない効果を計算する無料シミュレーター。',
  ogtitle='階段カロリー｜階段で1年どれだけ燃える？', ogdesc='1日の段数と体重から、階段の消費カロリーを計算。',
  h1='階段カロリーシミュレーター',
  lead='「エレベーターより階段」を続けると、どれだけ燃える？1日に上る段数と体重から、消費カロリーと年間の累計を出します。塵も積もれば、です。',
  inputs='''    <h2>🪜 条件を入れる</h2>
    <div class="row"><div class="field"><label>1日に上る段数 <span class="hint">（段）</span></label><input type="number" id="steps" value="100" min="0" inputmode="numeric"></div>
    <div class="field"><label>体重 <span class="hint">（kg）</span></label><input type="number" id="w" value="60" min="20" max="200" step="0.1" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">消費カロリーを見る</button>''',
  result='''      <div class="label">1日の消費カロリー</div>
      <div class="big"><span id="big">0</span><span class="unit">kcal</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1年で</div><div class="v accent" id="year">—</div></div>
      <div class="stat"><div class="k">脂肪にすると(年)</div><div class="v" id="fat">—</div></div>
      <div class="stat"><div class="k">10年で</div><div class="v" id="y10">—</div></div></div>''',
  article='''    <h2>階段は手軽な運動</h2>
    <div class="note"><strong>計算式（目安）</strong><br>1段上る消費 ≒ 0.1kcal × 体重 ÷ 60<br>（階段昇りは平地歩行の数倍の運動強度）</div>
    <p>階段の上り下りは、特別な時間を取らずにできるお手軽運動。1日100段でも、1年では意外な量に。エレベーターやエスカレーターを1回階段に変える、から始めてみては。</p>
    <h2>よくある質問</h2>'''+faq([('下りもカロリー使う？','上りより少なめですが消費します。本ツールは上り基準の概算です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const steps=Math.max(0,+$('steps').value||0),w=Math.max(1,+$('w').value||1);
    const day=steps*0.1*w/60,year=day*365;
    $('sub').textContent=`1日${num(steps)}段・体重${w}kg`;$('year').textContent=num(year)+'kcal';$('fat').textContent=num(year/7.2)+'g';$('y10').textContent=num(year*10)+'kcal';
    SHARE=`階段カロリーシミュ、1日${num(steps)}段で年${num(year)}kcal（脂肪${num(year/7.2)}g）燃える計算でした🪜\\n階段えらい！👇`;show();anim($('big'),0,day,900);}''')

# ===== 占い・診断 =====
add(id='birthstone', cat='占い・診断', emoji='💎',
  title='誕生石・誕生花診断｜あなたの誕生石とメッセージは？｜シミュラボ',
  desc='生まれ月から、あなたの誕生石・誕生花とその石言葉・花言葉、込められたメッセージを表示するエンタメ診断シミュレーター。',
  ogtitle='誕生石・誕生花診断｜あなたの誕生石は？', ogdesc='生まれ月から誕生石・誕生花と石言葉を表示。',
  h1='誕生石・誕生花診断',
  lead='あなたの生まれ月の誕生石・誕生花は？それぞれに込められた石言葉・花言葉とメッセージをお届けします。自分へのお守り選びや、贈り物の参考に。',
  inputs='''    <h2>💎 生まれ月を選ぶ</h2>
    <div class="field"><label>生まれた月</label><select id="m"><option value="1">1月</option><option value="2">2月</option><option value="3">3月</option><option value="4">4月</option><option value="5">5月</option><option value="6">6月</option><option value="7">7月</option><option value="8">8月</option><option value="9">9月</option><option value="10">10月</option><option value="11">11月</option><option value="12">12月</option></select></div>
    <button class="btn btn-primary" id="calcBtn">誕生石を見る</button>''',
  result='''      <div class="label">あなたの誕生石</div>
      <div class="big" style="font-size:40px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:18px;">—</div>''',
  article='''    <h2>誕生石・誕生花とは</h2>
    <p>生まれ月ごとに定められた宝石・花のこと。それぞれに「石言葉」「花言葉」があり、身につけると幸運やお守りになると言われます。自分用のジュエリーや、誕生日プレゼント選びの参考にどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([('複数ある月も？','月によって複数の誕生石があります。本ツールは代表的なものを表示します。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const m=+$('m').value||1;
    const D=[['ガーネット','スイートピー','真実の愛・友情。揺るがない絆を象徴します。'],['アメジスト','フリージア','誠実・心の平和。あなたを穏やかに守ります。'],['アクアマリン','チューリップ','幸福・聡明。爽やかな風のように前へ。'],['ダイヤモンド','桜','永遠の絆・純潔。最強の輝きはあなたの強さ。'],['エメラルド','カーネーション','幸運・愛。豊かなご縁を引き寄せます。'],['真珠','バラ','健康・長寿・純粋。気品あるあなたへ。'],['ルビー','ひまわり','情熱・勇気。太陽のような明るさを。'],['ペリドット','グラジオラス','夫婦愛・希望。前向きな力を授けます。'],['サファイア','ダリア','誠実・慈愛。深い知性と落ち着き。'],['オパール','ガーベラ','希望・幸運。多彩な魅力を放つあなたに。'],['トパーズ','菊','友情・成功。あたたかな人間関係を。'],['ターコイズ','ポインセチア','成功・繁栄。旅と挑戦のお守りに。']];
    const t=D[(m-1)%12];
    $('big').textContent=t[0];$('sub').textContent=`${m}月生まれ／誕生花：${t[1]}`;$('adv').textContent='💎 '+t[2];
    SHARE=`誕生石・誕生花診断、私(${m}月生まれ)の誕生石は「${t[0]}」でした💎\\n${t[2]}\\nあなたは？👇`;show();}''')

add(id='yesno-uranai', cat='占い・診断', emoji='🔮',
  title='イエス・ノー占い｜その悩み、答えはYES？NO？｜シミュラボ',
  desc='迷っていることを思い浮かべてボタンを押すと、今日のあなたへのYES／NOとひとことアドバイスを占うエンタメシミュレーター。',
  ogtitle='イエス・ノー占い｜答えはYES？NO？', ogdesc='迷いごとにYES/NOとアドバイスを占う。',
  h1='イエス・ノー占い',
  lead='決めかねていること、ありませんか。心の中で迷いを思い浮かべて、占いたいテーマを選んで占ってください。背中を押す（or 止める）ひとことつき。',
  inputs='''    <h2>🔮 占いたいことを選ぶ</h2>
    <div class="field"><label>テーマ</label><select id="theme"><option value="koi">恋愛・人間関係</option><option value="shigoto">仕事・お金</option><option value="kettei">迷っている決断</option><option value="kyou">今日の行動</option></select></div>
    <button class="btn btn-primary" id="calcBtn">YES？ NO？ を占う</button>''',
  result='''      <div class="label">今日のあなたへの答えは</div>
      <div class="big" style="font-size:52px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:18px;">—</div>''',
  article='''    <h2>背中を押すための占い</h2>
    <p>占いの本当の役割は「自分の本心に気づくこと」。YESと出て嬉しいか、NOと出てホッとするか——その反応に、あなたの本当の気持ちが表れます。最後に決めるのは、いつだってあなた自身です。</p>
    <h2>よくある質問</h2>'''+faq([('毎回変わる？','日付とテーマで変わります。本心を確かめるきっかけにどうぞ。'),('データは送信されますか？','いいえ。占いはすべてブラウザ内で完結します。')]),
  js='''  function calc(){const T=new Date(),today=`${T.getFullYear()}-${T.getMonth()+1}-${T.getDate()}`;const h=hash(today+'|'+$('theme').value);
    const yes=h%2===0;
    const yesMsg=['今がチャンス。思い切って動いて。','あなたの直感は正しい。信じて進もう。','一歩踏み出せば、道はひらけます。'];
    const noMsg=['今は待つが吉。焦らず準備を。','少し立ち止まって。別の道も見えてきます。','タイミングを変えれば、もっと良い結果に。'];
    const msg=(yes?yesMsg:noMsg)[(h>>2)%3];
    $('big').textContent=yes?'YES':'NO';$('big').style.color=yes?'#16a34a':'#e11d48';
    $('sub').textContent=`テーマ：${sel('theme').text}`;$('adv').textContent='🔮 '+msg;
    SHARE=`イエス・ノー占い、今日の私への答えは「${yes?'YES':'NO'}」でした🔮\\n${msg}\\nあなたは？👇`;show();}''')

add(id='biorhythm', cat='占い・診断', emoji='🌊',
  title='バイオリズム診断｜今日の身体・感情・知性の波は？｜シミュラボ',
  desc='生年月日から、身体・感情・知性の3つのバイオリズムを計算し、今日の調子と総合コンディションを表示するシミュレーター。',
  ogtitle='バイオリズム診断｜今日の調子は？', ogdesc='生年月日から身体・感情・知性のバイオリズムを計算。',
  h1='バイオリズム診断',
  lead='バイオリズムは、生まれた日から続く「身体・感情・知性」の3つの波。生年月日を入れると、今日のあなたのコンディションを波で表示します。',
  inputs='''    <h2>🌊 生年月日を入れる</h2>
    <div class="field"><label>生年月日</label><input type="date" id="d" value="1995-08-15"></div>
    <button class="btn btn-primary" id="calcBtn">今日の波を見る</button>''',
  result='''      <div class="label">今日の総合コンディション</div>
      <div class="big"><span id="big">0</span><span class="unit">％</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">身体(23日周期)</div><div class="v" id="p">—</div></div>
      <div class="stat"><div class="k">感情(28日周期)</div><div class="v accent" id="e">—</div></div>
      <div class="stat"><div class="k">知性(33日周期)</div><div class="v" id="i">—</div></div></div>''',
  article='''    <h2>バイオリズムとは</h2>
    <div class="note"><strong>計算式</strong><br>各リズム ＝ sin(2π × 生後日数 ÷ 周期)<br>身体23日・感情28日・知性33日の周期でプラスとマイナスを繰り返します。</div>
    <p>生まれた日からの日数で、3つの波の位置が決まります。プラスの日は調子が良く、マイナスや切り替わりの「要注意日」は無理をしないのが吉。あくまでエンタメとしてお楽しみください。</p>
    <h2>よくある質問</h2>'''+faq([('科学的根拠は？','明確な科学的根拠はありません。気分の指針・エンタメとしてどうぞ。'),('入力した誕生日は送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const v=$('d').value;if(!v){alert('生年月日を選んでね');return;}
    const b=new Date(v),T=new Date();b.setHours(0,0,0,0);T.setHours(0,0,0,0);const days=Math.round((T-b)/86400000);
    if(isNaN(days)||days<0){alert('正しい日付を入れてね');return;}
    const p=Math.sin(2*Math.PI*days/23),e=Math.sin(2*Math.PI*days/28),i=Math.sin(2*Math.PI*days/33);
    const pp=Math.round((p+1)/2*100),ep=Math.round((e+1)/2*100),ip=Math.round((i+1)/2*100),avg=Math.round((pp+ep+ip)/3);
    $('sub').textContent= avg>=60?'好調な一日！':avg>=40?'まずまずの一日':'無理は禁物の一日';
    $('p').textContent=pp+'％';$('e').textContent=ep+'％';$('i').textContent=ip+'％';
    SHARE=`バイオリズム診断、今日の総合コンディションは${avg}％でした🌊（身体${pp}/感情${ep}/知性${ip}）\\nあなたは？👇`;show();anim($('big'),0,avg,900);}''')

if __name__=='__main__':
    write_all(SIMS)
    print(f'batch2 done. {len(SIMS)} sims.')
