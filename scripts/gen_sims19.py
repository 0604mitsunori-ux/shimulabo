# -*- coding: utf-8 -*-
"""シミュラボ：スポーツ・運動カテゴリ 10本（gen_sims11のTPLを再利用）。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq, write_all

S='スポーツ・運動'
SIMS=[]

SIMS.append(dict(id='marathon-yosoku', cat=S, emoji='🏃',
  title='フルマラソン完走タイム予測｜今の走力でフルは何時間？｜シミュラボ',
  desc='5kmや10kmなど短い距離のタイムから、フルマラソンの完走予想タイムを計算する無料シミュレーター（リーゲルの式）。',
  ogtitle='フルマラソン完走タイム予測｜フルは何時間？', ogdesc='短い距離のタイムからフルマラソンの予想タイムを計算。',
  h1='フルマラソン完走タイム予測',
  lead='5kmや10kmのタイムから、フルマラソンの完走タイムを予測します。サブ4・サブ3.5の目標づくりに。マラソン界で使われる「リーゲルの式」採用。',
  inputs='''    <h2>🏃 条件を入れる</h2>
    <div class="field"><label>基準にする距離</label><select id="dist"><option value="5">5km</option><option value="10" selected>10km</option><option value="21.0975">ハーフ(21.1km)</option></select></div>
    <div class="row"><div class="field"><label>そのタイム（分）</label><input type="number" id="min" value="50" min="1" inputmode="numeric"></div>
    <div class="field"><label>（秒）</label><input type="number" id="sec" value="0" min="0" max="59" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">フルの予想タイムを見る</button>''',
  result='''      <div class="label">フルマラソン予想タイム</div>
      <div class="big"><span id="big">0:00</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1kmあたり</div><div class="v accent" id="pace">—</div></div>
      <div class="stat"><div class="k">サブ4(4時間切り)</div><div class="v" id="sub4">—</div></div>
      <div class="stat"><div class="k">基準ペース</div><div class="v" id="base">—</div></div></div>''',
  article='''    <h2>リーゲルの式とは</h2>
    <div class="note"><strong>計算式</strong><br>T2 ＝ T1 ×（D2 ÷ D1）^1.06<br>距離が伸びるほどペースは落ちる、を反映した予測式です。</div>
    <p>あくまで「同じ走り込みができれば」の理論値。実際は当日の気温・補給・後半の失速で変わります。練習の指標としてどうぞ。サブ4（4時間切り）は市民ランナーの一つの目標です。</p>
    <h2>よくある質問</h2>'''+faq([('初心者でも当てはまる？','走り込み量で変わります。経験が浅いほど予測より遅くなりがちです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function fmt(sec){sec=Math.round(sec);const h=Math.floor(sec/3600),m=Math.floor(sec%3600/60),s=sec%60;return (h>0?h+':':'')+('0'+m).slice(-2)+':'+('0'+s).slice(-2);}
  function pace(secPerKm){const m=Math.floor(secPerKm/60),s=Math.round(secPerKm%60);return m+"'"+('0'+s).slice(-2)+'"/km';}
  function calc(){
    const D1=+$('dist').value, T1=(Math.max(0,+$('min').value||0)*60+Math.max(0,+$('sec').value||0));
    const D2=42.195, T2=T1*Math.pow(D2/D1,1.06);
    $('big').textContent=fmt(T2);
    $('sub').textContent=`${sel('dist').text} ${$('min').value}分${$('sec').value}秒 から予測`;
    $('pace').textContent=pace(T2/D2); $('sub4').textContent= T2<14400?'達成見込み🎉':'あと'+fmt(T2-14400); $('base').textContent=pace(T1/D1);
    SHARE=`フルマラソン完走タイム予測、私の予想は ${fmt(T2)}（1km ${pace(T2/D2)}）でした🏃\\nあなたは？👇`;
    show();
  }'''))

SIMS.append(dict(id='run-pace', cat=S, emoji='👟',
  title='ランニング目標ペース計算｜目標タイムには1km何分？｜シミュラボ',
  desc='目標の距離とタイムから、1kmあたりのペース・時速・100mあたりのタイムを計算する無料のランニングペース計算機。',
  ogtitle='ランニング目標ペース計算｜1km何分で走る？', ogdesc='目標距離とタイムから、必要なペース・時速を計算。',
  h1='ランニング目標ペース計算',
  lead='「この大会をこのタイムで」から、1kmあたり何分で走ればいいかを逆算。ペース走の目安づくりに使えます。',
  inputs='''    <h2>👟 条件を入れる</h2>
    <div class="field"><label>距離</label><select id="dist"><option value="5">5km</option><option value="10">10km</option><option value="21.0975">ハーフ</option><option value="42.195" selected>フル</option></select></div>
    <div class="row"><div class="field"><label>目標タイム（時間）</label><input type="number" id="h" value="4" min="0" max="12" inputmode="numeric"></div>
    <div class="field"><label>（分）</label><input type="number" id="m" value="0" min="0" max="59" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">必要ペースを見る</button>''',
  result='''      <div class="label">1kmあたりのペース</div>
      <div class="big"><span id="big">0</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">時速</div><div class="v accent" id="kmh">—</div></div>
      <div class="stat"><div class="k">100mあたり</div><div class="v" id="h100">—</div></div>
      <div class="stat"><div class="k">総距離</div><div class="v" id="dv">—</div></div></div>''',
  article='''    <h2>ペースの考え方</h2>
    <div class="note"><strong>計算式</strong><br>1kmペース ＝ 目標タイム ÷ 距離</div>
    <p>レース本番は、最初を抑えて後半上げる「ネガティブスプリット」が失速しにくいと言われます。表示ペースを目安に、練習で体に覚えさせましょう。</p>
    <h2>よくある質問</h2>'''+faq([('ペース走って？','一定ペースで走る練習。このペースを体に覚えさせると本番が安定します。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function pace(s){const m=Math.floor(s/60),x=Math.round(s%60);return m+"'"+('0'+x).slice(-2)+'"';}
  function calc(){
    const D=+$('dist').value, T=(Math.max(0,+$('h').value||0)*3600+Math.max(0,+$('m').value||0)*60);
    const per=T/D;
    $('big').textContent=pace(per)+'/km';
    $('sub').textContent=`${sel('dist').text} を ${$('h').value}時間${$('m').value}分で`;
    $('kmh').textContent=(D/(T/3600)).toFixed(1)+'km/h'; $('h100').textContent=pace(per/10).replace("'",'"').replace('"','')+'秒'; $('dv').textContent=D+'km';
    SHARE=`ランニング目標ペース、${sel('dist').text}を${$('h').value}時間${$('m').value}分なら 1km ${pace(per)} ペースでした👟\\n練習がんばろ。👇`;
    show();
  }'''))

SIMS.append(dict(id='kintore-1rm', cat=S, emoji='🏋️',
  title='1RM計算機（最大挙上重量）｜あなたのMAXは何kg？｜シミュラボ',
  desc='扱える重量と回数から、1回だけ挙げられる最大重量（1RM）を推定し、各強度の目標重量も表示する無料の筋トレ計算機。',
  ogtitle='1RM計算機｜あなたのMAXは何kg？', ogdesc='重量×回数から最大挙上重量(1RM)と各強度を計算。',
  h1='1RM計算機（最大挙上重量）',
  lead='ベンチプレスなどで「今の重量を○回」から、1回だけ挙げられる最大重量（1RM）を推定します。安全に強くなるための目標設定に。',
  inputs='''    <h2>🏋️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>扱った重量 <span class="hint">（kg）</span></label><input type="number" id="w" value="60" min="1" inputmode="numeric"></div>
    <div class="field"><label>挙げた回数 <span class="hint">（回）</span></label><input type="number" id="r" value="8" min="1" max="20" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">1RMを計算する</button>''',
  result='''      <div class="label">推定1RM（最大挙上重量）</div>
      <div class="big"><span id="big">0</span><span class="unit">kg</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">筋肥大向け(80%)</div><div class="v accent" id="p80">—</div></div>
      <div class="stat"><div class="k">持久力向け(65%)</div><div class="v" id="p65">—</div></div>
      <div class="stat"><div class="k">入力</div><div class="v" id="inp">—</div></div></div>''',
  article='''    <h2>1RMとは</h2>
    <div class="note"><strong>計算式（エプリー式）</strong><br>1RM ＝ 重量 ×（1 ＋ 回数 ÷ 30）</div>
    <p>1RMは「1回だけ挙げられる最大重量」。直接測るのはケガのリスクがあるため、扱える重量×回数から推定するのが一般的です。筋肥大なら70〜85%、筋力なら85%以上が目安。安全第一で。</p>
    <h2>よくある質問</h2>'''+faq([('回数が多いと精度は？','12回を超えると誤差が大きくなります。1〜10回で測ると正確です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const w=Math.max(1,+$('w').value||1), r=Math.max(1,+$('r').value||1);
    const rm=w*(1+r/30);
    $('sub').textContent=`${w}kg × ${r}回 から推定`;
    $('p80').textContent=(rm*0.8).toFixed(1)+'kg'; $('p65').textContent=(rm*0.65).toFixed(1)+'kg'; $('inp').textContent=w+'kg×'+r;
    SHARE=`1RM計算、私の推定MAXは約${rm.toFixed(1)}kgでした🏋️（${w}kg×${r}回）\\nあなたのMAXは？👇`;
    show(); anim($('big'),0,rm,900,1);
  }'''))

SIMS.append(dict(id='tairyoku-nenrei', cat=S, emoji='💪',
  title='体力年齢診断｜あなたの体力、実年齢より若い？｜シミュラボ',
  desc='運動習慣・階段での息切れ・柔軟性・睡眠などから、体力年齢の目安を診断するエンタメシミュレーター。',
  ogtitle='体力年齢診断｜体力は実年齢より若い？', ogdesc='運動習慣などから体力年齢の目安を診断。',
  h1='体力年齢診断',
  lead='同じ年齢でも、体力には大きな差。5つの質問から「体力年齢」の目安を診断します（エンタメ診断・運動のきっかけに）。',
  inputs='''    <h2>💪 あてはまるものを選ぶ</h2>
    <div class="field"><label>実年齢 <span class="hint">（歳）</span></label><input type="number" id="age" value="35" min="10" max="100" inputmode="numeric"></div>
    <div class="field"><label>運動の頻度</label><select id="q1"><option value="-5">週3以上</option><option value="-1" selected>たまに</option><option value="4">ほぼしない</option></select></div>
    <div class="field"><label>駅の階段で</label><select id="q2"><option value="-3">余裕</option><option value="0" selected>少し息切れ</option><option value="4">かなりきつい</option></select></div>
    <div class="field"><label>体の柔らかさ（前屈）</label><select id="q3"><option value="-2">手のひらが床につく</option><option value="0" selected>指先が届く</option><option value="3">床に届かない</option></select></div>
    <div class="field"><label>睡眠</label><select id="q4"><option value="-2">しっかり眠れる</option><option value="0" selected>普通</option><option value="3">不足ぎみ</option></select></div>
    <div class="field"><label>片足立ち（目を閉じて）</label><select id="q5"><option value="-3">30秒以上</option><option value="0" selected>10秒くらい</option><option value="3">すぐぐらつく</option></select></div>
    <button class="btn btn-primary" id="calcBtn">体力年齢を診断する</button>''',
  result='''      <div class="label">あなたの体力年齢は</div>
      <div class="big"><span id="big">0</span><span class="unit">歳</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:18px;">—</div>''',
  article='''    <h2>体力年齢を上げるには</h2>
    <p>運動習慣・心肺機能・柔軟性・バランス感覚は、年齢に関わらず鍛えられます。本診断はそれを簡易点数化したエンタメ。気になる項目から、ウォーキングやストレッチで少しずつ。</p>
    <div class="note">💡 いちばん効くのは「週2〜3の運動」。少し息が上がる運動を習慣にすると、体力年齢はぐっと若返ります。</div>
    <h2>よくある質問</h2>'''+faq([('医学的な数値？','いいえ。生活と感覚から目安を出すエンタメ診断です。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const age=Math.max(10,+$('age').value||10);
    let d=0; for(const id of ['q1','q2','q3','q4','q5']) d+=(+$(id).value||0);
    const fit=Math.max(15,Math.round(age+d)), gap=fit-age;
    let a; if(gap<=-4)a='かなり若い体力！この習慣を続けて💪'; else if(gap<=1)a='実年齢相応。週2の運動でさらに若返りも。'; else a='運動不足ぎみかも。まずはウォーキングと階段から始めよう。';
    $('sub').textContent=`実年齢${age}歳 → 体力年齢${fit}歳（${gap>=0?'+':''}${gap}歳）`;
    $('adv').textContent='💪 '+a;
    SHARE=`体力年齢診断、実年齢${age}歳に対して体力年齢は${fit}歳でした💪\\n${gap<=0?'若い！':'運動しよ…'}あなたは？👇`;
    show(); anim($('big'),0,fit,900);
  }'''))

SIMS.append(dict(id='shomou-undou', cat=S, emoji='🔥',
  title='運動の消費カロリー計算｜その運動、何kcal燃える？｜シミュラボ',
  desc='運動の種目・時間・体重から、消費カロリーと燃える脂肪量を計算する無料シミュレーター（MET値ベース）。',
  ogtitle='運動の消費カロリー計算｜何kcal燃える？', ogdesc='種目・時間・体重から運動の消費カロリーを計算。',
  h1='運動の消費カロリー計算',
  lead='ジョギング30分で何kcal？運動の種目・時間・体重から、消費カロリーと燃える脂肪量を計算します。運動メニュー選びの参考に。',
  inputs='''    <h2>🔥 条件を選ぶ</h2>
    <div class="field"><label>運動の種目</label><select id="met"><option value="3.5">ウォーキング</option><option value="7" selected>ジョギング</option><option value="10">ランニング(速め)</option><option value="8">水泳</option><option value="6">サイクリング</option><option value="5">筋トレ</option><option value="3">ヨガ</option><option value="7.3">なわとび</option></select></div>
    <div class="row"><div class="field"><label>時間 <span class="hint">（分）</span></label><input type="number" id="min" value="30" min="0" inputmode="numeric"></div>
    <div class="field"><label>体重 <span class="hint">（kg）</span></label><input type="number" id="w" value="60" min="20" max="200" step="0.1" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">消費カロリーを見る</button>''',
  result='''      <div class="label">消費カロリー</div>
      <div class="big"><span id="big">0</span><span class="unit">kcal</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">燃える脂肪</div><div class="v accent" id="fat">—</div></div>
      <div class="stat"><div class="k">ごはん換算</div><div class="v" id="rice">—</div></div>
      <div class="stat"><div class="k">運動強度(METs)</div><div class="v" id="metv">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式（METs法）</strong><br>消費カロリー ＝ METs × 3.5 × 体重(kg) ÷ 200 × 時間(分)<br>脂肪1g ≒ 7.2kcal／ごはん1杯 ≒ 252kcal</div>
    <p>METsは運動の強さを表す数値。同じ時間でも強度が高いほどよく燃えます。続けやすい運動を選んで、習慣にするのが結局いちばんの近道です。</p>
    <h2>よくある質問</h2>'''+faq([('正確な値ですか？','体格・強度で変わる概算です。傾向の目安としてお使いください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const met=+$('met').value||1, min=Math.max(0,+$('min').value||0), w=Math.max(1,+$('w').value||1);
    const kcal=met*3.5*w/200*min, fat=kcal/7.2;
    $('sub').textContent=`${sel('met').text} ${min}分・${w}kg`;
    $('fat').textContent=num(fat)+'g'; $('rice').textContent=(kcal/252).toFixed(1)+'杯'; $('metv').textContent=met;
    SHARE=`運動の消費カロリー、${sel('met').text}${min}分で約${num(kcal)}kcal・脂肪${num(fat)}g燃える計算でした🔥\\n運動えらい！👇`;
    show(); anim($('big'),0,kcal,900);
  }'''))

SIMS.append(dict(id='golf-handi', cat=S, emoji='⛳',
  title='ゴルフ ハンデ目安シミュレーター｜あなたのハンデはどのくらい？｜シミュラボ',
  desc='平均スコアとコースの基準打数(パー)から、ゴルフのハンディキャップの目安と「100切り・90切り」までの距離を計算する無料シミュレーター。',
  ogtitle='ゴルフ ハンデ目安｜あなたのハンデは？', ogdesc='平均スコアからゴルフのハンデ目安を計算。',
  h1='ゴルフ ハンデ目安シミュレーター',
  lead='平均スコアから、ゴルフのハンディキャップの目安を計算します。100切り・90切りまであと何打かも分かります。上達の目標づくりに。',
  inputs='''    <h2>⛳ 条件を入れる</h2>
    <div class="row"><div class="field"><label>平均スコア <span class="hint">（打・18ホール）</span></label><input type="number" id="score" value="100" min="60" max="200" inputmode="numeric"></div>
    <div class="field"><label>コースの基準(パー)</label><input type="number" id="par" value="72" min="60" max="80" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">ハンデを見る</button>''',
  result='''      <div class="label">ハンディキャップの目安</div>
      <div class="big"><span id="big">0</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">パーオーバー</div><div class="v" id="over">—</div></div>
      <div class="stat"><div class="k">100切りまで</div><div class="v accent" id="g100">—</div></div>
      <div class="stat"><div class="k">レベル</div><div class="v" id="lv">—</div></div></div>''',
  article='''    <h2>ハンデの目安</h2>
    <div class="note"><strong>計算の考え方</strong><br>ハンデ目安 ＝（平均スコア − パー）× 0.8（簡易計算）</div>
    <p>正式なハンディキャップは複数ラウンドの成績から算出されますが、ここでは平均スコアから簡易に目安を出します。アマチュアの平均は100前後。90切りで「中級者」、80台で「上級者」と言われます。</p>
    <h2>よくある質問</h2>'''+faq([('正式なハンデと同じ？','いいえ。簡易な目安です。正式にはJGAなどの算出方法があります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const score=Math.max(60,+$('score').value||100), par=Math.max(60,+$('par').value||72);
    const over=score-par, handi=Math.max(0,Math.round(over*0.8));
    let lv; if(score<80)lv='上級者🏆'; else if(score<90)lv='中級者'; else if(score<100)lv='90切り目前'; else lv='これから上達';
    $('sub').textContent=`平均${score}・パー${par}`;
    $('over').textContent='+'+over; $('g100').textContent= score<=100?'達成🎉':'あと'+(score-100)+'打'; $('lv').textContent=lv;
    SHARE=`ゴルフのハンデ目安シミュ、平均${score}でハンデ約${handi}でした⛳（${lv}）\\nあなたのスコアは？👇`;
    show(); anim($('big'),0,handi,900);
  }'''))

SIMS.append(dict(id='swim-pace', cat=S, emoji='🏊',
  title='水泳ペース換算シミュレーター｜100mあたり何秒？｜シミュラボ',
  desc='泳いだ距離とタイムから、100mあたりのペース・1mあたり・時速を計算する無料の水泳ペース換算ツール。',
  ogtitle='水泳ペース換算｜100mあたり何秒？', ogdesc='距離とタイムから水泳の100mペース・時速を計算。',
  h1='水泳ペース換算シミュレーター',
  lead='泳いだ距離とタイムから、100mあたりのペースに換算します。練習の記録や、自分の泳力の把握に。',
  inputs='''    <h2>🏊 条件を入れる</h2>
    <div class="row"><div class="field"><label>距離 <span class="hint">（m）</span></label><input type="number" id="dist" value="50" min="1" inputmode="numeric"></div>
    <div class="field"><label>タイム <span class="hint">（秒）</span></label><input type="number" id="sec" value="50" min="1" step="0.1" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">ペースを見る</button>''',
  result='''      <div class="label">100mあたりのペース</div>
      <div class="big"><span id="big">0</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1mあたり</div><div class="v accent" id="per1">—</div></div>
      <div class="stat"><div class="k">時速</div><div class="v" id="kmh">—</div></div>
      <div class="stat"><div class="k">距離</div><div class="v" id="dv">—</div></div></div>''',
  article='''    <h2>ペース換算の使い方</h2>
    <div class="note"><strong>計算式</strong><br>100mペース ＝ タイム ÷ 距離 × 100</div>
    <p>「100mあたり」にそろえると、距離が違う記録どうしも比べられます。一般的な大人の目安は100mを2分前後。続けるほど自然と縮みます。</p>
    <h2>よくある質問</h2>'''+faq([('クロール以外でも使える？','はい。泳法を問わず距離とタイムで換算できます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function fmt(s){const m=Math.floor(s/60),x=Math.round(s%60);return m>0?(m+"'"+('0'+x).slice(-2)+'"'):x.toFixed(0)+'秒';}
  function calc(){
    const dist=Math.max(1,+$('dist').value||1), sec=Math.max(0.1,+$('sec').value||1);
    const per100=sec/dist*100;
    $('big').textContent=fmt(per100);
    $('sub').textContent=`${dist}m を ${sec}秒`;
    $('per1').textContent=(sec/dist).toFixed(2)+'秒'; $('kmh').textContent=(dist/sec*3.6).toFixed(2)+'km/h'; $('dv').textContent=dist+'m';
    SHARE=`水泳ペース換算、私は100mあたり ${fmt(per100)} ペースでした🏊（${dist}m/${sec}秒）\\nあなたは？👇`;
    show();
  }'''))

SIMS.append(dict(id='jitensha', cat=S, emoji='🚴',
  title='サイクリング 所要時間＆消費カロリー｜その距離、何分で何kcal？｜シミュラボ',
  desc='走る距離と平均速度・体重から、サイクリングの所要時間と消費カロリーを計算する無料シミュレーター。',
  ogtitle='サイクリング 所要時間＆消費カロリー', ogdesc='距離と速度・体重から所要時間と消費カロリーを計算。',
  h1='サイクリング 所要時間＆消費カロリー',
  lead='その距離、自転車だと何分かかって、何kcal燃える？距離・平均速度・体重から、所要時間と消費カロリーを出します。',
  inputs='''    <h2>🚴 条件を入れる</h2>
    <div class="row"><div class="field"><label>距離 <span class="hint">（km）</span></label><input type="number" id="dist" value="20" min="0" inputmode="numeric"></div>
    <div class="field"><label>平均速度 <span class="hint">（km/h）</span></label><input type="number" id="spd" value="18" min="1" inputmode="numeric"></div></div>
    <div class="field"><label>体重 <span class="hint">（kg）</span></label><input type="number" id="w" value="60" min="20" max="200" step="0.1" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">所要時間を見る</button>''',
  result='''      <div class="label">所要時間</div>
      <div class="big"><span id="big">0</span><span class="unit">分</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">消費カロリー</div><div class="v accent" id="kcal">—</div></div>
      <div class="stat"><div class="k">燃える脂肪</div><div class="v" id="fat">—</div></div>
      <div class="stat"><div class="k">平均速度</div><div class="v" id="sv">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>所要時間 ＝ 距離 ÷ 速度<br>消費カロリー ＝ METs(約6) × 3.5 × 体重 ÷ 200 × 時間(分)</div>
    <p>サイクリングは膝への負担が少なく、長く続けやすい有酸素運動。通勤を自転車に変えるだけで、移動しながら運動できて一石二鳥です。</p>
    <h2>よくある質問</h2>'''+faq([('坂道は？','本ツールは平地の目安です。上り坂が多いと消費は増えます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const dist=Math.max(0,+$('dist').value||0), spd=Math.max(1,+$('spd').value||1), w=Math.max(1,+$('w').value||1);
    const min=dist/spd*60, kcal=6*3.5*w/200*min, fat=kcal/7.2;
    $('sub').textContent=`${dist}km・${spd}km/h・${w}kg`;
    $('kcal').textContent=num(kcal)+'kcal'; $('fat').textContent=num(fat)+'g'; $('sv').textContent=spd+'km/h';
    SHARE=`サイクリング${dist}km、約${num(min)}分で${num(kcal)}kcal燃える計算でした🚴\\n移動しながら運動、最高👇`;
    show(); anim($('big'),0,min,900);
  }'''))

SIMS.append(dict(id='taishibo-otoshi', cat=S, emoji='📉',
  title='体脂肪1kg落とす運動量シミュレーター｜何時間運動すればいい？｜シミュラボ',
  desc='落としたい脂肪の量と運動の種目・体重から、必要な運動時間と「1日30分なら何日かかるか」を計算する無料シミュレーター。',
  ogtitle='体脂肪を落とす運動量｜何時間運動すればいい？', ogdesc='落としたい脂肪量から必要な運動時間を計算。',
  h1='体脂肪1kg落とす運動量シミュレーター',
  lead='脂肪を運動だけで落とすと、どれくらい大変？落としたい脂肪量と運動の種目から、必要な運動時間を出します（食事の見直しと併用が現実的）。',
  inputs='''    <h2>📉 条件を入れる</h2>
    <div class="row"><div class="field"><label>落としたい脂肪 <span class="hint">（kg）</span></label><input type="number" id="kg" value="1" min="0.1" max="30" step="0.1" inputmode="decimal"></div>
    <div class="field"><label>体重 <span class="hint">（kg）</span></label><input type="number" id="w" value="60" min="20" max="200" inputmode="numeric"></div></div>
    <div class="field"><label>運動の種目</label><select id="met"><option value="3.5">ウォーキング</option><option value="7" selected>ジョギング</option><option value="10">ランニング</option><option value="8">水泳</option><option value="6">サイクリング</option></select></div>
    <button class="btn btn-primary" id="calcBtn">必要な運動量を見る</button>''',
  result='''      <div class="label">必要な運動時間（合計）</div>
      <div class="big"><span id="big">0</span><span class="unit">時間</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">必要カロリー</div><div class="v" id="kcal">—</div></div>
      <div class="stat"><div class="k">1日30分なら</div><div class="v accent" id="days">—</div></div>
      <div class="stat"><div class="k">種目</div><div class="v" id="mv">—</div></div></div>''',
  article='''    <h2>運動だけは大変、だから…</h2>
    <div class="note"><strong>計算式</strong><br>必要カロリー ＝ 脂肪kg × 7,200<br>必要時間 ＝ 必要カロリー ÷（METs × 3.5 × 体重 ÷ 200）</div>
    <p>脂肪1kgを運動だけで落とすには相当な時間がかかります。だから「食事の見直し＋運動」の合わせ技が現実的。運動は脂肪燃焼だけでなく、筋肉維持・健康維持にも効きます。</p>
    <h2>よくある質問</h2>'''+faq([('食事制限と比べると？','食事の見直しのほうが短期の効果は出やすいです。運動は維持と健康に効きます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const kg=Math.max(0.1,+$('kg').value||1), w=Math.max(1,+$('w').value||1), met=+$('met').value||7;
    const kcal=kg*7200, perMin=met*3.5*w/200, mins=kcal/perMin, hours=mins/60, days=mins/30;
    $('sub').textContent=`脂肪${kg}kg・${sel('met').text}・${w}kg`;
    $('kcal').textContent=num(kcal)+'kcal'; $('days').textContent=num(days)+'日'; $('mv').textContent=sel('met').text;
    SHARE=`体脂肪${kg}kgを${sel('met').text}だけで落とすには約${num(hours)}時間（1日30分で${num(days)}日）必要でした📉\\n食事も大事だ…！👇`;
    show(); anim($('big'),0,hours,900);
  }'''))

SIMS.append(dict(id='shinpaku-zone', cat=S, emoji='❤️',
  title='心拍ゾーン計算｜脂肪燃焼に効く心拍数は？｜シミュラボ',
  desc='年齢から最大心拍数を求め、脂肪燃焼ゾーン・有酸素ゾーンなど運動強度別の目標心拍数を計算する無料シミュレーター。',
  ogtitle='心拍ゾーン計算｜脂肪燃焼に効く心拍数は？', ogdesc='年齢から最大心拍数と脂肪燃焼ゾーンを計算。',
  h1='心拍ゾーン計算',
  lead='効率よく脂肪を燃やすには、運動中の心拍数がカギ。年齢から最大心拍数を求め、目的別の目標心拍ゾーンを出します。',
  inputs='''    <h2>❤️ 条件を入れる</h2>
    <div class="field"><label>年齢 <span class="hint">（歳）</span></label><input type="number" id="age" value="35" min="10" max="100" inputmode="numeric"></div>
    <div class="field"><label>安静時心拍数 <span class="hint">（bpm・分からなければ60）</span></label><input type="number" id="rest" value="60" min="40" max="100" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">心拍ゾーンを見る</button>''',
  result='''      <div class="label">最大心拍数</div>
      <div class="big"><span id="big">0</span><span class="unit">bpm</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">脂肪燃焼ゾーン</div><div class="v accent" id="fat">—</div></div>
      <div class="stat"><div class="k">有酸素ゾーン</div><div class="v" id="cardio">—</div></div>
      <div class="stat"><div class="k">全力ゾーン</div><div class="v" id="max">—</div></div></div>''',
  article='''    <h2>心拍ゾーンとは</h2>
    <div class="note"><strong>計算式</strong><br>最大心拍数 ＝ 220 − 年齢<br>脂肪燃焼ゾーン ＝ 最大心拍の60〜70%／有酸素 ＝ 70〜80%</div>
    <p>脂肪燃焼を狙うなら「ややきつい」と感じる60〜70%の強度が効率的。スマートウォッチで心拍を見ながら運動すると、頑張りすぎ・ゆるすぎを防げます。</p>
    <h2>よくある質問</h2>'''+faq([('220−年齢は正確？','簡易式です。個人差があるので目安としてお使いください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const age=Math.max(10,+$('age').value||10);
    const max=220-age;
    $('sub').textContent=`年齢${age}歳・最大心拍 ${max}bpm`;
    $('fat').textContent=Math.round(max*0.6)+'〜'+Math.round(max*0.7)+'bpm'; $('cardio').textContent=Math.round(max*0.7)+'〜'+Math.round(max*0.8)+'bpm'; $('max').textContent=Math.round(max*0.9)+'〜'+max+'bpm';
    SHARE=`心拍ゾーン計算、私の最大心拍は${max}bpm、脂肪燃焼ゾーンは${Math.round(max*0.6)}〜${Math.round(max*0.7)}bpmでした❤️\\n運動の参考に👇`;
    show(); anim($('big'),0,max,900);
  }'''))

if __name__=='__main__':
    write_all(SIMS)
    print(f'sports done. {len(SIMS)} sims.')
