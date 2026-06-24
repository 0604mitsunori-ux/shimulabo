# -*- coding: utf-8 -*-
"""シミュラボ：計算ツール他7本。ルート/二次方程式/円の面積(tool)、内申点(juken)、引っ越し費用/賃貸初期費用(home)、自動車税(car)。
gen_sims_tool TPL流用。seo_internal.py / gen_images.py のauto-importに 'gen_sims_keisan2' を追加。
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
ANIM = r'''  function anim(v){const el=$('big'),t0=performance.now();(function s(n){const p=Math.min(1,(n-t0)/700),e=1-Math.pow(1-p,3);el.textContent=(Math.round(v*e*100)/100).toLocaleString('ja-JP');if(p<1)requestAnimationFrame(s);else el.textContent=(Math.round(v*100)/100).toLocaleString('ja-JP');})(performance.now());}'''

# ============================================================
# 1. ルート計算（ルート 計算 2100/KD1/TP201000）★★
# ============================================================
add(id='root-keisan', emoji='√',
  title='ルート計算機（平方根）｜√の値を計算・簡単な形に変形｜シミュラボ',
  desc='数値を入れるだけで平方根（ルート）の値を計算する無料ツール。√72＝6√2 のように、ルートを簡単な形（a√b）に変形する機能つき。数学の宿題や検算に。',
  ogtitle='ルート計算機（平方根）｜√の値・簡単な形', ogdesc='平方根の値を計算し、a√bの形にも変形。',
  h1='ルート計算機（平方根）',
  lead='√（ルート）の値は?数値を入れると平方根を計算し、√72＝6√2のように「いちばん簡単な形」にも変形します。数学の検算に。',
  inputs='''    <h2>√ 数値を入れる</h2>
    <div class="field"><label>√ の中の数</label><input type="number" id="n" value="72" min="0" step="any" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">ルートを計算</button>''',
  result='''      <div class="label">平方根（√n）の値</div>
      <div class="big"><span id="big">0</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">簡単な形</div><div class="v accent" id="simp">—</div></div>
      <div class="stat"><div class="k">2乗すると</div><div class="v" id="sq">—</div></div></div>''',
  article='''    <div class="note"><strong>平方根とは</strong><br>2乗するとその数になる値が平方根。√72は約8.485で、72＝36×2 なので √72＝6√2 と簡単にできます。</div>
    <h2>ルート（平方根）の計算</h2>
    <p>平方根は「2乗するとその数になる値」です。√の中の数を、平方数（4・9・16…）で割れる分だけ外に出すと、6√2のような「簡単な形」になります。これを「ルートを簡単にする」「根号を外に出す」といいます。本ツールは小数の値と、簡単な形の両方を表示するので、宿題の答え合わせや検算に便利です。</p>
    <h2>よくある質問</h2>'''+faq([
      ('簡単な形って？','√72＝6√2 のように、√の外に出せる数を出した形です。'),
      ('マイナスは？','負の数の平方根は実数では表せません（虚数になります）。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function simplify(n){if(!Number.isInteger(n)||n<0)return null;let out=1,inn=n;for(let i=2;i*i<=inn;i++){while(inn%(i*i)===0){out*=i;inn/=i*i;}}return [out,inn];}
  function calc(){const n=+$('n').value;if(n<0){$('big').textContent='—';$('sub').textContent='0以上の数を入れてね（負は虚数）';show();return;}
    const v=Math.sqrt(n);$('sub').textContent='√'+n+' ＝ '+(Math.round(v*1e6)/1e6);
    const sp=simplify(n);let stxt;
    if(sp){const[o,i]=sp;stxt=(i===1)?(''+o):(o===1?('√'+i):(o+'√'+i));}else stxt='√'+n+'（整数でないため）';
    $('simp').textContent=stxt;$('sq').textContent=Math.round(v*v*1e6)/1e6;
    SHARE='ルート計算機、√'+n+' ＝ '+(Math.round(v*1000)/1000)+'（簡単な形：'+stxt+'）でした√';show();anim(v);}
'''+ANIM)

# ============================================================
# 2. 二次方程式の解（二次方程式 解 250/KD0/TP3900）
# ============================================================
add(id='nijihoteishiki', emoji='🔣',
  title='二次方程式の解の計算機｜ax²+bx+c=0 を解の公式で解く｜シミュラボ',
  desc='a・b・cを入れるだけで、二次方程式 ax²+bx+c=0 を解の公式で解く無料ツール。判別式から実数解・重解・虚数解を自動判定。数学の宿題・検算に。',
  ogtitle='二次方程式の解の計算機｜解の公式', ogdesc='ax²+bx+c=0をa,b,c入力で解く。判別式も判定。',
  h1='二次方程式の解の計算機',
  lead='ax²+bx+c=0 を一発で解く!係数a・b・cを入れると、解の公式で解を計算します。判別式から実数解・重解・虚数解も自動で判定。',
  inputs='''    <h2>🔣 係数を入れる（ax²+bx+c=0）</h2>
    <div class="row"><div class="field"><label>a</label><input type="number" id="a" value="1" step="any" inputmode="decimal"></div>
    <div class="field"><label>b</label><input type="number" id="b" value="-5" step="any" inputmode="decimal"></div>
    <div class="field"><label>c</label><input type="number" id="c" value="6" step="any" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">解を求める</button>''',
  result='''      <div class="label">解</div>
      <div class="big" style="font-size:26px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">判別式 D＝b²−4ac</div><div class="v accent" id="disc">—</div></div></div>''',
  article='''    <div class="note"><strong>解の公式</strong><br>x ＝ ( −b ± √(b²−4ac) ) ÷ 2a<br>判別式 D＝b²−4ac が D&gt;0で異なる2実数解、D＝0で重解、D&lt;0で虚数解</div>
    <h2>二次方程式の解き方</h2>
    <p>二次方程式 ax²+bx+c=0 は、解の公式 x＝(−b±√(b²−4ac))÷2a で解けます。√の中の「b²−4ac」を判別式Dといい、Dの符号で解の種類が決まります。D&gt;0なら異なる2つの実数解、D＝0なら1つ（重解）、D&lt;0なら実数解なし（虚数解）です。本ツールは判別式の判定も表示するので、検算や解き方の確認に使えます。</p>
    <h2>よくある質問</h2>'''+faq([
      ('aが0だとどうなる？','aが0だと二次方程式ではなくなります（一次方程式 bx+c=0）。'),
      ('虚数解も出る？','D&lt;0のとき、虚数解（複素数）を表示します。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function rd(x){return Math.round(x*1e6)/1e6;}
  function calc(){const a=+$('a').value,b=+$('b').value,c=+$('c').value;
    if(a===0){$('big').textContent= b!==0?('x ＝ '+rd(-c/b)):'解なし/不定';$('sub').textContent='a＝0（一次方程式 bx+c=0）';$('disc').textContent='—';show();return;}
    const D=b*b-4*a*c;$('disc').textContent=rd(D)+(D>0?'（2つの実数解）':D===0?'（重解）':'（虚数解）');
    let txt;
    if(D>0){const r=Math.sqrt(D);txt='x ＝ '+rd((-b+r)/(2*a))+' , '+rd((-b-r)/(2*a));}
    else if(D===0){txt='x ＝ '+rd(-b/(2*a))+'（重解）';}
    else{const re=rd(-b/(2*a)),im=rd(Math.sqrt(-D)/(2*a));txt='x ＝ '+re+' ± '+im+'i';}
    $('big').textContent=txt;$('sub').textContent=a+'x² '+(b>=0?'+':'')+b+'x '+(c>=0?'+':'')+c+' = 0';
    SHARE='二次方程式の解、'+a+'x²'+(b>=0?'+':'')+b+'x'+(c>=0?'+':'')+c+'=0 → '+txt+' でした🔣';show();}
''')

# ============================================================
# 3. 円の面積・円周（円の面積 16000/KD0）★★★
# ============================================================
add(id='en-menseki', emoji='⭕',
  title='円の面積・円周の計算機｜半径や直径からすぐ計算｜シミュラボ',
  desc='半径または直径を入れるだけで、円の面積（πr²）と円周（2πr）を自動計算する無料ツール。直径からの計算にも対応。算数・数学の宿題や工作の採寸に。',
  ogtitle='円の面積・円周の計算機｜半径/直径から', ogdesc='半径または直径から円の面積・円周を自動計算。',
  h1='円の面積・円周の計算機',
  lead='円の面積と円周をすぐ計算!半径か直径を入れるだけで、面積（πr²）と円周（2πr）を求めます。宿題や工作の採寸に。',
  inputs='''    <h2>⭕ 数値を入れる</h2>
    <div class="field"><label>入力する値</label><select id="kind"><option value="r" selected>半径から</option><option value="d">直径から</option></select></div>
    <div class="field"><label>長さ <span class="hint">（半径または直径）</span></label><input type="number" id="v" value="5" min="0" step="any" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">計算する</button>''',
  result='''      <div class="label">円の面積</div>
      <div class="big"><span id="big">0</span><span class="unit">（単位²）</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">円周</div><div class="v accent" id="cir">—</div></div>
      <div class="stat"><div class="k">半径 / 直径</div><div class="v" id="rd">—</div></div></div>''',
  article='''    <div class="note"><strong>公式</strong><br>面積 ＝ π × 半径²　／　円周 ＝ 2 × π × 半径 ＝ π × 直径　（π≒3.14159）</div>
    <h2>円の面積と円周の求め方</h2>
    <p>円の面積は「半径×半径×円周率（π）」、円周は「直径×円周率」で求めます。円周率πはおよそ3.14159。半径が分かれば面積も円周も計算でき、直径は半径の2倍です。たとえば半径5cmの円は、面積が約78.54cm²、円周が約31.42cm。算数・数学の宿題のほか、円形のテーブルや花壇のサイズ計算にも使えます。</p>
    <h2>よくある質問</h2>'''+faq([
      ('円周率はいくつ？','約3.14159です。本ツールはより精密なπで計算します。'),
      ('直径からでも計算できる？','はい。「直径から」を選べば、直径を入れて計算できます。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const kind=$('kind').value,val=Math.max(0,+$('v').value||0);const r=kind==='r'?val:val/2;
    const area=Math.PI*r*r,cir=2*Math.PI*r;
    $('sub').textContent=(kind==='r'?'半径':'直径')+' '+val+' から';
    $('cir').textContent=(Math.round(cir*1000)/1000).toLocaleString('ja-JP');$('rd').textContent='半径'+(Math.round(r*100)/100)+' / 直径'+(Math.round(r*2*100)/100);
    SHARE='円の面積・円周、'+(kind==='r'?'半径':'直径')+val+'なら 面積'+(Math.round(area*100)/100)+'・円周'+(Math.round(cir*100)/100)+' でした⭕';show();anim(area);}
'''+ANIM)

# ============================================================
# 4. 内申点計算（内申点 計算 3000/KD0）cat=受験・進学
# ============================================================
add(id='naishinten', emoji='📋', cat='受験・進学',
  title='内申点計算機｜9教科の評定から内申点を合計・換算｜シミュラボ',
  desc='9教科の5段階評定を入れるだけで、内申点の合計（45点満点）と、実技4教科を2倍にする換算内申（65点満点）を計算する無料ツール。高校受験の目安に。',
  ogtitle='内申点計算機｜9教科の評定から合計・換算', ogdesc='9教科の評定から内申点（45点満点）と換算内申を計算。',
  h1='内申点計算機',
  lead='内申点は何点?9教科の5段階評定を選ぶと、合計（45点満点）と、実技4教科を2倍する換算内申（65点満点）を計算します。高校受験の目安に。',
  inputs='''    <h2>📋 各教科の評定（5段階）</h2>
    <div class="row"><div class="field"><label>国語</label><select id="s0">__O__</select></div><div class="field"><label>数学</label><select id="s1">__O__</select></div></div>
    <div class="row"><div class="field"><label>英語</label><select id="s2">__O__</select></div><div class="field"><label>理科</label><select id="s3">__O__</select></div></div>
    <div class="row"><div class="field"><label>社会</label><select id="s4">__O__</select></div><div class="field"><label>音楽</label><select id="s5">__O__</select></div></div>
    <div class="row"><div class="field"><label>美術</label><select id="s6">__O__</select></div><div class="field"><label>保健体育</label><select id="s7">__O__</select></div></div>
    <div class="field"><label>技術・家庭</label><select id="s8">__O__</select></div>
    <button class="btn btn-primary" id="calcBtn">内申点を計算</button>'''.replace('__O__','<option>5</option><option>4</option><option>3</option><option>2</option><option>1</option>'),
  result='''      <div class="label">内申点の合計（45点満点）</div>
      <div class="big"><span id="big">0</span><span class="unit">/45</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">主要5教科</div><div class="v" id="main">—</div></div>
      <div class="stat"><div class="k">実技4教科</div><div class="v" id="jitsu">—</div></div>
      <div class="stat"><div class="k">換算内申（実技2倍・65点満点）</div><div class="v accent" id="kanzan">—</div></div></div>''',
  article='''    <div class="note"><strong>内申点とは</strong><br>9教科の5段階評定の合計（45点満点）。多くの都道府県で、実技4教科（音楽・美術・保体・技家）を2倍にする「換算内申」が高校入試で使われます（例：5×1＋4×2＝65点満点）。</div>
    <h2>内申点の計算方法</h2>
    <p>内申点（評定）は、通知表の5段階評価を合計したものです。9教科すべてが5なら45点満点。高校入試では、実技4教科を2倍に換算する方式が多く使われます（東京都など）。計算方法や対象学年は都道府県・高校によって異なるため、志望校の募集要項で必ず確認してください。本ツールは一般的な目安です。</p>
    <h2>よくある質問</h2>'''+faq([
      ('実技2倍はどこでも？','多くの自治体で採用されますが、方式は都道府県で異なります。要項を確認しましょう。'),
      ('対象の学年は？','中3だけ、中1〜3など自治体で異なります。志望校の方式をご確認ください。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){let main=0,jitsu=0;for(let i=0;i<5;i++)main+=+$('s'+i).value;for(let i=5;i<9;i++)jitsu+=+$('s'+i).value;
    const total=main+jitsu,kanzan=main+jitsu*2;
    $('sub').textContent='9教科の評定の合計';$('main').textContent=main+'/25';$('jitsu').textContent=jitsu+'/20';$('kanzan').textContent=kanzan+'/65';
    SHARE='内申点計算機、合計'+total+'/45（換算内申'+kanzan+'/65）でした📋';show();anim(total);}
'''+ANIM)

# ============================================================
# 5. 引っ越し費用相場（引っ越し 費用 相場 800/KD3/TP39000）cat=住まい・暮らし
# ============================================================
add(id='hikkoshi-hiyou', emoji='🚚', cat='住まい・暮らし',
  title='引っ越し費用シミュレーター｜人数・距離・時期から相場の目安｜シミュラボ',
  desc='世帯人数・移動距離・時期（通常期/繁忙期）から、引っ越し費用の相場の目安を表示する無料ツール。単身〜家族まで対応。見積もり前の予算感づくりに。',
  ogtitle='引っ越し費用シミュレーター｜相場の目安', ogdesc='人数・距離・時期から引っ越し費用の相場目安を表示。',
  h1='引っ越し費用シミュレーター',
  lead='引っ越し、いくらかかる?世帯人数・移動距離・時期を選ぶと、費用の相場の目安を表示します。3〜4月の繁忙期は高くなる点も反映。',
  inputs='''    <h2>🚚 条件を選ぶ</h2>
    <div class="field"><label>世帯（荷物量）</label><select id="size"><option value="0" selected>単身（荷物少なめ）</option><option value="1">単身（荷物多め）</option><option value="2">2人世帯</option><option value="3">3〜4人家族</option></select></div>
    <div class="field"><label>移動距離</label><select id="dist"><option value="near" selected>近距離（〜50km・同市内程度）</option><option value="mid">中距離（50〜200km）</option><option value="far">遠距離（200km〜）</option></select></div>
    <div class="field"><label>時期</label><select id="season"><option value="1" selected>通常期（5〜2月）</option><option value="1.5">繁忙期（3〜4月）</option></select></div>
    <button class="btn btn-primary" id="calcBtn">費用の目安を見る</button>''',
  result='''      <div class="label">引っ越し費用の目安</div>
      <div class="big"><span id="big">0</span><span class="unit">円〜</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">目安レンジ</div><div class="v accent" id="range">—</div></div></div>''',
  article='''    <div class="note"><strong>費用について</strong><br>荷物量・距離が大きいほど、また3〜4月の繁忙期ほど高くなります。本ツールは一般的な相場の概算です。</div>
    <h2>引っ越し費用の相場</h2>
    <p>引っ越し費用は「荷物の量 × 移動距離 × 時期」でおおよそ決まります。単身の近距離なら3〜5万円ほど、家族の遠距離だと20万円を超えることも。特に進学・就職シーズンの3〜4月（繁忙期）は需要が集中し、料金が1.5倍ほどに上がる傾向です。複数社で相見積もりを取り、不要品を減らす・時期をずらすと費用を抑えられます。</p>
    <h2>よくある質問</h2>'''+faq([
      ('安くするには？','相見積もり、繁忙期を避ける、荷物を減らす、平日や時間指定なしが効果的です。'),
      ('見積もりは無料？','多くの業者で無料です。複数社を比較しましょう。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  const BASE=[[35000,55000],[45000,70000],[60000,100000],[80000,140000]];
  const DM={near:1,mid:1.4,far:2.0};
  function calc(){const sz=+$('size').value||0,dm=DM[$('dist').value]||1,sm=+$('season').value||1;
    const lo=Math.round(BASE[sz][0]*dm*sm/1000)*1000,hi=Math.round(BASE[sz][1]*dm*sm/1000)*1000;
    $('sub').textContent=sel('size').text.split('（')[0]+'・'+sel('dist').text.split('（')[0]+'・'+($('season').value=='1'?'通常期':'繁忙期');
    $('range').textContent=num(lo)+'〜'+num(hi)+'円';
    SHARE='引っ越し費用シミュ、目安は約'+num(lo)+'〜'+num(hi)+'円でした🚚';show();anim(lo);}
'''+ANIM)

# ============================================================
# 6. 賃貸初期費用（賃貸 初期費用 4700/KD1/TP18000）cat=住まい・暮らし
# ============================================================
add(id='shoki-hiyou', emoji='🔑', cat='住まい・暮らし',
  title='賃貸の初期費用シミュレーター｜家賃から契約時の総額を計算｜シミュラボ',
  desc='家賃を入れるだけで、賃貸契約の初期費用（敷金・礼金・仲介手数料・前家賃・保証料・火災保険・鍵交換）の合計の目安を計算する無料ツール。引っ越しの予算づくりに。',
  ogtitle='賃貸の初期費用シミュレーター｜契約時の総額', ogdesc='家賃から敷金・礼金・仲介手数料など初期費用の合計を計算。',
  h1='賃貸の初期費用シミュレーター',
  lead='賃貸契約、最初にいくら必要?家賃を入れると、敷金・礼金・仲介手数料・前家賃などを合計した初期費用の目安を計算します。各項目は調整も可能。',
  inputs='''    <h2>🔑 条件を入れる</h2>
    <div class="field"><label>家賃（管理費込み）<span class="hint">円/月</span></label><input type="number" id="rent" value="80000" min="0" inputmode="numeric"></div>
    <div class="row"><div class="field"><label>敷金 <span class="hint">ヶ月</span></label><input type="number" id="shiki" value="1" min="0" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>礼金 <span class="hint">ヶ月</span></label><input type="number" id="rei" value="1" min="0" step="0.5" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">初期費用を計算</button>''',
  result='''      <div class="label">初期費用の合計（目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">敷金＋礼金</div><div class="v" id="sr">—</div></div>
      <div class="stat"><div class="k">仲介手数料＋前家賃</div><div class="v" id="cf">—</div></div>
      <div class="stat"><div class="k">保証料・保険・鍵交換ほか</div><div class="v accent" id="etc">—</div></div></div>''',
  article='''    <div class="note"><strong>内訳の目安</strong><br>敷金（◯ヶ月）＋礼金（◯ヶ月）＋仲介手数料（家賃1ヶ月＋税）＋前家賃（1ヶ月）＋保証料（家賃0.5〜1ヶ月）＋火災保険（約2万円）＋鍵交換（約2万円）。<br>合計はおおむね家賃の4.5〜5ヶ月分が目安です。</div>
    <h2>賃貸の初期費用の内訳</h2>
    <p>賃貸契約の初期費用は、家賃のおよそ4.5〜5ヶ月分が一般的な目安です。内訳は、敷金・礼金・仲介手数料（家賃1ヶ月＋消費税）・前家賃・保証会社利用料・火災保険料・鍵交換費用など。最近は「敷金礼金ゼロ」の物件も増えていますが、その分、保証料や退去時費用がかかる場合もあります。見積もり（重要事項説明）で内訳を確認しましょう。</p>
    <h2>よくある質問</h2>'''+faq([
      ('安くする方法は？','敷金礼金ゼロ物件、フリーレント、仲介手数料の交渉などがあります。'),
      ('家賃の何ヶ月分？','一般的に4.5〜5ヶ月分が目安です。条件で前後します。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const r=Math.max(0,+$('rent').value||0),sk=Math.max(0,+$('shiki').value||0),re=Math.max(0,+$('rei').value||0);
    const shiki=r*sk,rei=r*re,chukai=Math.round(r*1.1),mae=r,hosho=Math.round(r*0.7),hoken=20000,kagi=22000;
    const etc=hosho+hoken+kagi;const total=shiki+rei+chukai+mae+etc;
    $('sub').textContent='家賃'+num(r)+'円・敷'+sk+'/礼'+re+'ヶ月（家賃の約'+(Math.round(total/r*10)/10)+'ヶ月分）';
    $('sr').textContent=yen(shiki+rei);$('cf').textContent=yen(chukai+mae);$('etc').textContent=yen(etc);
    SHARE='賃貸の初期費用シミュ、家賃'+num(r)+'円なら初期費用は約'+yen(total)+'でした🔑';show();anim(total);}
'''+ANIM)

# ============================================================
# 7. 自動車税計算（自動車税 計算 700/KD28/TP41000）cat=クルマ・乗り物
# ============================================================
add(id='jidoshazei', emoji='🚙', cat='クルマ・乗り物',
  title='自動車税の早見・計算機｜排気量から年間の税額がわかる｜シミュラボ',
  desc='排気量の区分を選ぶだけで、自動車税（種別割）の年間税額の目安が分かる無料ツール。2019年10月以降の新税率に対応。13年超の重課（増税）も反映できます。',
  ogtitle='自動車税の早見・計算機｜排気量から税額', ogdesc='排気量区分から自動車税（種別割）の年額を表示。新税率対応。',
  h1='自動車税の早見・計算機',
  lead='うちの車の自動車税はいくら?排気量の区分を選ぶと、年間の自動車税（種別割）の目安を表示します。2019年10月以降の新税率対応。',
  inputs='''    <h2>🚙 排気量を選ぶ</h2>
    <div class="field"><label>排気量の区分（自家用乗用車）</label><select id="cc">
      <option value="10800">軽自動車</option><option value="25000">1.0L以下</option><option value="30500" selected>1.0超〜1.5L</option>
      <option value="36000">1.5超〜2.0L</option><option value="43500">2.0超〜2.5L</option><option value="50000">2.5超〜3.0L</option>
      <option value="57000">3.0超〜3.5L</option><option value="65500">3.5超〜4.0L</option><option value="75500">4.0超〜4.5L</option>
      <option value="87000">4.5超〜6.0L</option><option value="110000">6.0L超</option></select></div>
    <div class="field"><label>初度登録からの年数</label><select id="old"><option value="1" selected>13年以内（通常）</option><option value="1.15">13年超（重課・約15%増）</option></select></div>
    <button class="btn btn-primary" id="calcBtn">自動車税を見る</button>''',
  result='''      <div class="label">自動車税（年額・目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">円/年</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">月あたり</div><div class="v accent" id="month">—</div></div></div>''',
  article='''    <div class="note"><strong>自動車税（種別割）について</strong><br>毎年4月1日時点の所有者にかかる税金。排気量が大きいほど高くなります。2019年10月以降に新車登録した車は新税率（一部引き下げ）。ガソリン車は初度登録から13年超で約15%重課されます。</div>
    <h2>自動車税の仕組み</h2>
    <p>自動車税（種別割）は、毎年4月1日時点で車を所有している人に課される税金で、5月ごろに納税通知書が届きます。税額は排気量の区分で決まり、軽自動車は一律10,800円。2019年10月以降に新車新規登録した自家用乗用車は、新税率が適用されます。また、ガソリン車は新車登録から13年を超えると約15%重課（増税）されます。本ツールは自家用乗用車の目安です。'''+'※実際の税額・適用は登録時期や地域で異なります。正確には自治体の通知をご確認ください。'+'''</p>
    <h2>よくある質問</h2>'''+faq([
      ('いつ払う？','毎年5月ごろに通知書が届き、5月末が納期限のことが多いです。'),
      ('なぜ古い車は高い？','環境負荷の観点から、13年超のガソリン車は約15%重課されます。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const base=+$('cc').value||0,o=+$('old').value||1;const tax=Math.round(base*o/100)*100;
    $('sub').textContent=sel('cc').text+'・'+($('old').value=='1'?'13年以内':'13年超(重課)');
    $('month').textContent=yen(Math.round(tax/12));
    SHARE='自動車税の早見、'+sel('cc').text+'なら年額 約'+yen(tax)+'でした🚙';show();anim(tax);}
'''+ANIM)

# 既存simと重複のため除外（naishin/naishin-keisan=内申点, jidousha-zei=自動車税 が既存）
SIMS[:] = [s for s in SIMS if s['id'] not in {'naishinten','jidoshazei'}]

if __name__=='__main__':
    render()
    print(f'keisan2 done. {len(SIMS)} sims.')
