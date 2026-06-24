# -*- coding: utf-8 -*-
"""シミュラボ：健康・カラダ／運動／美容 5本。血圧・体脂肪率・ランニング消費カロリー・最大心拍数・美容体重。
既存カテゴリへ追加（health/sports/beauty）。YMYL配慮で「目安・医療判断は医師へ」免責付き。
gen_sims_tool TPL流用。seo_internal.py / gen_images.py のauto-importに 'gen_sims_karada' を追加。
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq
from gen_sims_tool import TPL, viz
from sim_quiz import make_engines
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CAT = '健康・カラダ'
SIMS = []
tally_quiz, num_quiz, band_quiz, add, q_article, render = make_engines(SIMS, CAT, TPL, viz)
ANIM = r'''  function anim(v){const el=$('big'),t0=performance.now();(function s(n){const p=Math.min(1,(n-t0)/700),e=1-Math.pow(1-p,3);el.textContent=(Math.round(v*e*10)/10).toLocaleString('ja-JP');if(p<1)requestAnimationFrame(s);else el.textContent=(Math.round(v*10)/10).toLocaleString('ja-JP');})(performance.now());}'''
MED = '※あくまで一般的な目安です。診断・治療ではありません。気になる数値や症状がある場合は医療機関にご相談ください。'

# ============================================================
# 1. 血圧チェッカー（血圧 56000/KD1/TP66000）★★★
# ============================================================
add(id='ketsuatsu-check', emoji='🩺',
  title='血圧の判定チェッカー｜上・下の数値であなたの血圧分類は？｜シミュラボ',
  desc='収縮期（上）・拡張期（下）の血圧を入れるだけで、日本高血圧学会の基準にもとづく分類（正常・高値・高血圧I〜III度）の目安が分かる無料ツール。※診断ではありません。',
  ogtitle='血圧の判定チェッカー｜あなたの血圧分類は？', ogdesc='上・下の血圧から高血圧学会基準の分類の目安を判定。',
  h1='血圧の判定チェッカー',
  lead='その血圧、正常?それとも高め?上（収縮期）と下（拡張期）の数値を入れると、日本高血圧学会の基準にもとづく分類の目安を表示します。健康管理のセルフチェックに。',
  inputs='''    <h2>🩺 血圧の数値を入れる</h2>
    <div class="row"><div class="field"><label>上（収縮期）<span class="hint">mmHg</span></label><input type="number" id="sys" value="120" min="0" inputmode="numeric"></div>
    <div class="field"><label>下（拡張期）<span class="hint">mmHg</span></label><input type="number" id="dia" value="80" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">血圧を判定する</button>''',
  result='''      <div class="label">血圧の分類（目安）</div>
      <div class="big" style="font-size:26px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="advice" style="text-align:left;margin-top:12px;">—</div>''',
  article='''    <div class="note"><strong>分類の基準（診察室血圧・日本高血圧学会）</strong><br>正常：上&lt;120 かつ 下&lt;80／正常高値：上120-129／高値血圧：上130-139 または 下80-89／I度高血圧：上140-159 または 下90-99／II度：上160-179 または 下100-109／III度：上≧180 または 下≧110</div>
    <h2>血圧の数値の見方</h2>
    <p>血圧は「上（収縮期）」と「下（拡張期）」の2つで評価し、どちらか高いほうの分類が適用されます。診察室で測る血圧と、家庭で測る血圧では基準が少し異なります（家庭血圧は5mmHgほど低い基準）。高血圧は自覚症状が出にくい一方、放置すると脳・心臓・腎臓の病気のリスクを高めます。継続的な測定と、気になる場合の受診が大切です。'''+MED+'''</p>
    <h2>よくある質問</h2>'''+faq([
      ('家庭で測ると基準が違う？','はい。家庭血圧は診察室より低めの基準（正常：上&lt;115/下&lt;75目安）です。本ツールは診察室血圧の基準です。'),
      ('1回高かったら高血圧？','いいえ。緊張や測定環境で変動します。複数回・別日の測定で判断します。'),
      ('データは送信されますか？','いいえ。判定はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const s=Math.max(0,+$('sys').value||0),d=Math.max(0,+$('dia').value||0);
    let cls,lv,adv;
    if(s>=180||d>=110){cls='III度高血圧';lv=5;adv='かなり高い数値です。早めに医療機関を受診してください。';}
    else if(s>=160||d>=100){cls='II度高血圧';lv=4;adv='高い状態です。医療機関への相談をおすすめします。';}
    else if(s>=140||d>=90){cls='I度高血圧';lv=3;adv='高血圧にあたります。生活習慣の見直しと受診を検討しましょう。';}
    else if(s>=130||d>=80){cls='高値血圧';lv=2;adv='やや高めです。減塩・運動など生活習慣に気を配りましょう。';}
    else if(s>=120){cls='正常高値血圧';lv=1;adv='正常範囲ですが上限寄りです。引き続き測定を。';}
    else{cls='正常血圧';lv=0;adv='良好な範囲です。この調子で健康管理を続けましょう。';}
    const cl=(lv>=3)?'warn':'good';$('advice').className='alert '+cl;
    $('big').textContent=cls;$('sub').textContent='上 '+s+' / 下 '+d+' mmHg（診察室血圧の基準）';
    $('advice').textContent=(lv>=3?'⚠️ ':'✅ ')+adv;
    SHARE='血圧チェッカー、上'+s+'/下'+d+'は「'+cls+'」でした🩺';show();}
''')

# ============================================================
# 2. 体脂肪率 計算（体脂肪率 計算 20000/KD1）★★★
# ============================================================
add(id='taishibo-keisan', emoji='📉',
  title='体脂肪率の推定計算機｜身長・体重・年齢から体脂肪率の目安｜シミュラボ',
  desc='身長・体重・年齢・性別から、体脂肪率の目安を推定する無料ツール（BMIベースの推定式）。体組成計がなくても、おおよその体脂肪率と判定が分かります。',
  ogtitle='体脂肪率の推定計算機｜体脂肪率の目安', ogdesc='身長・体重・年齢・性別から体脂肪率の目安を推定。',
  h1='体脂肪率の推定計算機',
  lead='体組成計がなくても、体脂肪率のおおよそが分かる!身長・体重・年齢・性別から、推定式で体脂肪率の目安を計算します。ダイエットの目安に。',
  inputs='''    <h2>📉 体の情報を入れる</h2>
    <div class="row"><div class="field"><label>身長 <span class="hint">cm</span></label><input type="number" id="h" value="165" min="0" inputmode="decimal"></div>
    <div class="field"><label>体重 <span class="hint">kg</span></label><input type="number" id="w" value="60" min="0" inputmode="decimal"></div></div>
    <div class="row"><div class="field"><label>年齢</label><input type="number" id="age" value="30" min="0" inputmode="numeric"></div>
    <div class="field"><label>性別</label><select id="sex"><option value="1" selected>男性</option><option value="0">女性</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">体脂肪率を推定</button>''',
  result='''      <div class="label">推定体脂肪率</div>
      <div class="big"><span id="big">0</span><span class="unit">%</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">BMI</div><div class="v" id="bmi">—</div></div>
      <div class="stat"><div class="k">判定</div><div class="v accent" id="judge">—</div></div></div>''',
  article='''    <div class="note"><strong>推定式（Deurenbergの式）</strong><br>体脂肪率(%) ＝ 1.2×BMI ＋ 0.23×年齢 − 10.8×性別(男1/女0) − 5.4</div>
    <h2>体脂肪率の目安</h2>
    <p>体脂肪率は、体重に占める脂肪の割合です。一般的な健康的範囲は、男性で10〜19％、女性で20〜29％ほど。本ツールはBMI・年齢・性別から推定する式を使っており、体組成計（インピーダンス法）の実測値とは差が出ることがあります。あくまで目安として、ダイエットや体づくりの参考にしてください。'''+MED+'''</p>
    <h2>よくある質問</h2>'''+faq([
      ('体組成計と違う？','はい。本ツールは推定式で、機器の実測値とは数％の差が出ることがあります。'),
      ('低ければ良い？','低すぎる体脂肪率は健康に良くありません。標準範囲を目安にしましょう。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const h=Math.max(1,+$('h').value||0)/100,w=Math.max(0,+$('w').value||0),age=Math.max(0,+$('age').value||0),sex=+$('sex').value;
    const bmi=w/(h*h);let bf=1.2*bmi+0.23*age-10.8*sex-5.4;bf=Math.max(2,Math.min(60,bf));
    const male=sex===1;let j;
    if(male){j=bf<10?'やせ（低め）':bf<20?'標準':bf<25?'やや高め':'高め';}
    else{j=bf<20?'やせ（低め）':bf<30?'標準':bf<35?'やや高め':'高め';}
    $('sub').textContent=(male?'男性':'女性')+'・BMI '+(Math.round(bmi*10)/10);$('bmi').textContent=Math.round(bmi*10)/10;$('judge').textContent=j;
    SHARE='体脂肪率の推定、約'+(Math.round(bf*10)/10)+'%（'+j+'）でした📉 ※推定値';show();anim(bf);}
'''+ANIM)

# ============================================================
# 3. ランニング消費カロリー（ランニング 消費カロリー 6100/KD0/TP11000）★★ cat=sports
# ============================================================
add(id='ranning-calorie', emoji='🏃', cat='スポーツ・運動',
  title='ランニング消費カロリー計算機｜距離・体重から消費カロリー｜シミュラボ',
  desc='走った距離と体重から、ランニングの消費カロリーを計算する無料ツール。脂肪燃焼量（g）の目安や、ごはん・おにぎり何個分かも分かります。ダイエットの目安に。',
  ogtitle='ランニング消費カロリー計算機｜距離×体重', ogdesc='距離と体重からランニングの消費カロリーを計算。脂肪燃焼量も。',
  h1='ランニング消費カロリー計算機',
  lead='そのラン、何キロカロリー消費?走った距離と体重を入れると、消費カロリーを計算します。脂肪燃焼量や「おにぎり何個分」もチェック。',
  inputs='''    <h2>🏃 走った内容を入れる</h2>
    <div class="row"><div class="field"><label>走った距離 <span class="hint">km</span></label><input type="number" id="dist" value="5" min="0" inputmode="decimal"></div>
    <div class="field"><label>体重 <span class="hint">kg</span></label><input type="number" id="w" value="60" min="0" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">消費カロリーを計算</button>''',
  result='''      <div class="label">消費カロリー</div>
      <div class="big"><span id="big">0</span><span class="unit">kcal</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">脂肪燃焼量の目安</div><div class="v accent" id="fat">—</div></div>
      <div class="stat"><div class="k">おにぎり換算</div><div class="v" id="onigiri">—</div></div></div>''',
  article='''    <div class="note"><strong>計算式（目安）</strong><br>消費カロリー ＝ 体重(kg) × 距離(km) × 1.05<br>※体重を運ぶエネルギーから概算。ペースや個人差は加味していません。</div>
    <h2>ランニングの消費カロリー</h2>
    <p>ランニングの消費カロリーは、おおよそ「体重×距離」に比例します。体重60kgの人が5km走ると約315kcal。脂肪1gは約7.2kcalに相当するので、消費カロリーを7.2で割るとおおよその脂肪燃焼量になります。ただし、実際の消費は走るペースや路面、気温でも変わります。続けることがいちばんのダイエットのコツです。'''+MED+'''</p>
    <h2>よくある質問</h2>'''+faq([
      ('歩きでも使える？','ウォーキングは消費が約半分。本ツールはランニング向けの概算です。'),
      ('体重が減れば消費も減る？','はい。体を運ぶエネルギーが減るため、同じ距離でも消費は少しずつ下がります。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const d=Math.max(0,+$('dist').value||0),w=Math.max(0,+$('w').value||0);
    const kcal=w*d*1.05, fat=kcal/7.2, oni=kcal/180;
    $('sub').textContent=w+'kg × '+d+'km × 1.05';$('fat').textContent=(Math.round(fat*10)/10)+'g';$('onigiri').textContent='約'+(Math.round(oni*10)/10)+'個分';
    SHARE='ランニング消費カロリー、'+w+'kgで'+d+'km走ると約'+Math.round(kcal)+'kcal（脂肪約'+(Math.round(fat*10)/10)+'g）でした🏃';show();
    const el=$('big'),t0=performance.now();(function s(n){const p=Math.min(1,(n-t0)/700);el.textContent=Math.round(kcal*p).toLocaleString('ja-JP');if(p<1)requestAnimationFrame(s);else el.textContent=Math.round(kcal).toLocaleString('ja-JP');})(performance.now());}
''')

# ============================================================
# 4. 最大心拍数・心拍ゾーン（最大心拍数 計算 1000/KD1）cat=sports
# ============================================================
add(id='saidai-shinpaku', emoji='❤️', cat='スポーツ・運動',
  title='最大心拍数・心拍ゾーン計算機｜脂肪燃焼ゾーンは何拍？｜シミュラボ',
  desc='年齢から最大心拍数を求め、脂肪燃焼ゾーン・有酸素ゾーン・高強度ゾーンの目標心拍数を計算する無料ツール。効率的なランニングやトレーニングの目安に。',
  ogtitle='最大心拍数・心拍ゾーン計算機', ogdesc='年齢から最大心拍数と脂肪燃焼/有酸素ゾーンを計算。',
  h1='最大心拍数・心拍ゾーン計算機',
  lead='脂肪を燃やすには心拍数いくつ?年齢から最大心拍数を求め、目的別（脂肪燃焼・有酸素・高強度）の目標心拍ゾーンを計算します。効率的な運動の目安に。',
  inputs='''    <h2>❤️ 年齢を入れる</h2>
    <div class="field"><label>年齢</label><input type="number" id="age" value="30" min="0" max="120" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">心拍ゾーンを計算</button>''',
  result='''      <div class="label">最大心拍数（推定）</div>
      <div class="big"><span id="big">0</span><span class="unit">拍/分</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">脂肪燃焼（60-70%）</div><div class="v accent" id="fat">—</div></div>
      <div class="stat"><div class="k">有酸素（70-80%）</div><div class="v" id="aero">—</div></div>
      <div class="stat"><div class="k">高強度（80-90%）</div><div class="v" id="hard">—</div></div></div>''',
  article='''    <div class="note"><strong>計算式</strong><br>最大心拍数 ＝ 220 − 年齢（簡易式）<br>各ゾーン ＝ 最大心拍数 × 強度（％）</div>
    <h2>心拍ゾーンの使い方</h2>
    <p>運動の強度は心拍数で管理できます。最大心拍数の60〜70％は「脂肪燃焼ゾーン」で、長く続けると体脂肪をエネルギーに使いやすい領域。70〜80％は持久力を高める「有酸素ゾーン」、80〜90％は「高強度ゾーン」です。ダイエット目的なら脂肪燃焼〜有酸素ゾーンを目安に。「220−年齢」は簡易式で、個人差があります。'''+MED+'''</p>
    <h2>よくある質問</h2>'''+faq([
      ('脂肪燃焼ゾーンが一番痩せる？','低強度は脂肪の利用割合が高い一方、総消費は強度が高いほど大きくなります。目的に合わせて。'),
      ('心拍はどう測る？','スマートウォッチや胸ベルト型の心拍計が便利です。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const age=Math.max(0,Math.min(120,+$('age').value||0));const mhr=220-age;const z=(lo,hi)=>Math.round(mhr*lo)+'〜'+Math.round(mhr*hi)+' 拍/分';
    $('sub').textContent=age+'歳・220−年齢';$('fat').textContent=z(0.6,0.7);$('aero').textContent=z(0.7,0.8);$('hard').textContent=z(0.8,0.9);
    SHARE='最大心拍数・心拍ゾーン、'+age+'歳の最大心拍は約'+mhr+'拍/分（脂肪燃焼'+Math.round(mhr*0.6)+'〜'+Math.round(mhr*0.7)+'）でした❤️';show();
    const el=$('big'),t0=performance.now();(function s(n){const p=Math.min(1,(n-t0)/700);el.textContent=Math.round(mhr*p);if(p<1)requestAnimationFrame(s);else el.textContent=mhr;})(performance.now());}
''')

# ============================================================
# 5. 美容体重・モデル体重（美容体重 8600/KD41/TP14000）cat=beauty
# ============================================================
add(id='biyo-taiju', emoji='💃', cat='美容・ファッション',
  title='美容体重・モデル体重 計算機｜身長から理想の体重の目安｜シミュラボ',
  desc='身長を入れるだけで、標準体重・美容体重・モデル体重・シンデレラ体重の目安を計算する無料ツール。BMIごとの体重を一覧で表示。無理のない目標設定に。',
  ogtitle='美容体重・モデル体重 計算機', ogdesc='身長から標準・美容・モデル・シンデレラ体重の目安を計算。',
  h1='美容体重・モデル体重 計算機',
  lead='身長から「キレイに見える体重」の目安を計算!標準体重・美容体重・モデル体重・シンデレラ体重を一覧で表示します。※健康を最優先に、無理のない目標を。',
  inputs='''    <h2>💃 身長を入れる</h2>
    <div class="field"><label>身長 <span class="hint">cm</span></label><input type="number" id="h" value="160" min="0" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">体重の目安を見る</button>''',
  result='''      <div class="label">美容体重（BMI20）</div>
      <div class="big"><span id="big">0</span><span class="unit">kg</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">標準体重（BMI22）</div><div class="v" id="std">—</div></div>
      <div class="stat"><div class="k">モデル体重（BMI19）</div><div class="v accent" id="model">—</div></div>
      <div class="stat"><div class="k">シンデレラ体重（BMI18）</div><div class="v" id="cinderella">—</div></div></div>''',
  article='''    <div class="note"><strong>計算式</strong><br>体重 ＝ 身長(m)² × BMI<br>標準=BMI22／美容=BMI20／モデル=BMI19／シンデレラ=BMI18</div>
    <h2>美容体重・モデル体重とは</h2>
    <p>「美容体重」は見た目がすっきりして見えるとされるBMI20前後、「モデル体重」はBMI19前後、「シンデレラ体重」はBMI18前後の体重を指す俗称です。一方、健康面で最も病気のリスクが低いとされるのはBMI22前後（標準体重）。BMI18.5未満は「低体重（やせ）」にあたり、過度なダイエットは体調を崩す原因になります。数値はあくまで目安。健康を最優先に、無理のない範囲で目標を立ててください。'''+MED+'''</p>
    <h2>よくある質問</h2>'''+faq([
      ('シンデレラ体重は健康的？','BMI18はやせ寄りで、人によっては低体重になります。健康を優先しましょう。'),
      ('標準体重が一番いい？','病気のリスクが最も低いとされるのはBMI22前後です。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const h=Math.max(1,+$('h').value||0)/100;const w=b=>Math.round(h*h*b*10)/10;
    $('sub').textContent='身長 '+($('h').value)+'cm の目安';
    $('std').textContent=w(22)+' kg';$('model').textContent=w(19)+' kg';$('cinderella').textContent=w(18)+' kg';
    SHARE='美容体重・モデル体重、身長'+($('h').value)+'cmなら美容体重'+w(20)+'kg（標準'+w(22)+'/モデル'+w(19)+'）でした💃';show();anim(w(20));}
'''+ANIM)

if __name__=='__main__':
    render()
    print(f'karada done. {len(SIMS)} sims.')
