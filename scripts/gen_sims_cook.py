# -*- coding: utf-8 -*-
"""シミュラボ：新カテゴリ「料理・キッチン」20本（計量・換算など低KD×高需要）。write_all再利用。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq, write_all

COOK = '料理・キッチン'
SIMS = []
def add(**k): k['cat']=COOK; SIMS.append(k)
def C(t): return '<div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：'+t+'</div>'
def REF(items): return '<h2>参考</h2><ul class="seo-refs">'+''.join('<li>'+i+'</li>' for i in items)+'</ul>'

add(id='chomiryo-gram', emoji='🥄',
  title='調味料 大さじ・小さじ→グラム換算｜塩・砂糖・味噌は何g？｜シミュラボ',
  desc='塩・砂糖・醤油・味噌など調味料の大さじ・小さじを、何グラムかに換算する無料ツール。レシピの計量に。',
  ogtitle='調味料 大さじ・小さじ→グラム換算', ogdesc='塩・砂糖・味噌などの大さじ小さじをグラムに換算。',
  h1='調味料 大さじ・小さじ→グラム換算',
  lead='「塩 小さじ1は何グラム？」を一発換算。調味料を選んで杯数を入れるだけで、重さ（g）が分かります。',
  inputs='''    <h2>🥄 条件を入れる</h2>
    <div class="row"><div class="field"><label>調味料</label><select id="k"><option value="18">塩</option><option value="9" selected>砂糖（上白糖）</option><option value="18">醤油</option><option value="18">みそ</option><option value="18">みりん</option><option value="15">酒</option><option value="15">酢</option><option value="12">サラダ油</option><option value="12">バター</option><option value="9">小麦粉</option><option value="9">片栗粉</option><option value="4">ベーキングパウダー</option><option value="12">マヨネーズ</option><option value="15">ケチャップ</option><option value="21">はちみつ</option></select></div>
    <div class="field"><label>スプーン</label><select id="sp"><option value="1" selected>大さじ（15ml）</option><option value="0.3333">小さじ（5ml）</option></select></div></div>
    <div class="field"><label>杯数</label><input type="number" id="n" value="1" min="0" step="0.5" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">グラムに換算する</button>''',
  result='''      <div class="label">重さ</div>
      <div class="big"><span id="big">0</span><span class="unit">g</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">大さじ1あたり</div><div class="v accent" id="per">—</div></div>
      <div class="stat"><div class="k">小さじ1あたり</div><div class="v" id="ko">—</div></div>
      <div class="stat"><div class="k">杯数</div><div class="v" id="nv">—</div></div></div>''',
  article=C('大さじ1＝15ml、小さじ1＝5ml（＝大さじ1/3）。同じ容量でも<b>調味料ごとに重さ（比重）が違う</b>ため、塩は大さじ1＝18g、砂糖は9gと差が出ます。')+'''
    <h2>調味料 大さじ1のグラム早見</h2>
    <table class="seo-table"><tr><th>調味料</th><th>大さじ1</th><th>小さじ1</th></tr>
    <tr><td>塩</td><td>18g</td><td>6g</td></tr><tr><td>砂糖（上白糖）</td><td>9g</td><td>3g</td></tr>
    <tr><td>醤油・みそ・みりん</td><td>18g</td><td>6g</td></tr><tr><td>小麦粉・片栗粉</td><td>9g</td><td>3g</td></tr>
    <tr><td>はちみつ</td><td>21g</td><td>7g</td></tr><tr><td>サラダ油・バター</td><td>12g</td><td>4g</td></tr></table>
    <h2>よくある質問</h2>'''+faq([('大さじと小さじの違いは？','大さじ＝15ml、小さじ＝5ml。小さじ3杯で大さじ1です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['調味料の計量換算（一般的な目安）']),
  js='''  function calc(){const g1=+$('k').value||0,sp=+$('sp').value||1,n=Math.max(0,+$('n').value||0);
    const g=g1*sp*n;
    $('sub').textContent=`${sel('k').text} ${sel('sp').text} × ${n}`;
    $('per').textContent=g1+'g';$('ko').textContent=(g1/3).toFixed(1)+'g';$('nv').textContent=n+'杯';
    show();anim($('big'),0,g,700,1);
    SHARE=`調味料グラム換算、${sel('k').text}${sel('sp').text}×${n}＝約${g.toFixed(1)}gでした🥄`;}''')

add(id='kome-mizu', emoji='🍚',
  title='米の水加減 計算｜何合に水は何ml（cc）？無洗米も対応｜シミュラボ',
  desc='米の合数と仕上がりの好みから、炊飯に必要な水の量（ml・cc）を計算する無料ツール。白米・無洗米に対応。',
  ogtitle='米の水加減 計算｜水は何ml？', ogdesc='合数と好みから炊飯の水の量を計算（無洗米対応）。',
  h1='米の水加減 計算ツール',
  lead='「お米○合に水はどれくらい？」を一発計算。合数と仕上がりの好みから、必要な水の量（ml/cc）を出します。',
  inputs='''    <h2>🍚 条件を入れる</h2>
    <div class="row"><div class="field"><label>米の量 <span class="hint">（合）</span></label><input type="number" id="go" value="2" min="0" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>米の種類</label><select id="type"><option value="200" selected>白米</option><option value="220">無洗米</option></select></div></div>
    <div class="field"><label>仕上がり</label><select id="kata"><option value="0.95">かため</option><option value="1" selected>ふつう</option><option value="1.1">やわらかめ</option></select></div>
    <button class="btn btn-primary" id="calcBtn">水の量を計算する</button>''',
  result='''      <div class="label">水の量</div>
      <div class="big"><span id="big">0</span><span class="unit">ml</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">カップで</div><div class="v accent" id="cup">—</div></div>
      <div class="stat"><div class="k">米の重さ</div><div class="v" id="omosa">—</div></div>
      <div class="stat"><div class="k">炊き上がり</div><div class="v" id="up">—</div></div></div>''',
  article=C('白米は <b>1合に水200ml</b>（＝米の体積の約1.2倍）が目安。無洗米は表面のぬかがないぶん、やや多めの約220mlにします。')+'''
    <h2>米の水加減の目安</h2>
    <table class="seo-table"><tr><th>合数</th><th>白米の水</th><th>無洗米の水</th></tr>
    <tr><td>1合</td><td>200ml</td><td>220ml</td></tr><tr><td>2合</td><td>400ml</td><td>440ml</td></tr>
    <tr><td>3合</td><td>600ml</td><td>660ml</td></tr><tr><td>5合</td><td>1000ml</td><td>1100ml</td></tr></table>
    <p>1合＝180ml（約150g）。新米は水を少なめ、古米は多めにすると◎。炊飯器の目盛りがある場合はそちらが正確です。</p>
    <h2>よくある質問</h2>'''+faq([('1合は何ml？','米1合は180ml（約150g）。水は白米で約200mlが目安です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['炊飯の水加減（一般的な目安）']),
  js='''  function calc(){const go=Math.max(0,+$('go').value||0),base=+$('type').value||200,kata=+$('kata').value||1;
    const water=go*base*kata, omosa=go*150;
    $('sub').textContent=`${sel('type').text} ${go}合・${sel('kata').text}`;
    $('cup').textContent=(water/200).toFixed(1)+'カップ';$('omosa').textContent=num(omosa)+'g';$('up').textContent='約'+num(go*330)+'g';
    show();anim($('big'),0,water,700);
    SHARE=`米の水加減、${go}合（${sel('type').text}）は水 約${num(water)}mlでした🍚`;}''')

add(id='onsu-gram', emoji='⚖️',
  title='オンス⇔グラム 換算｜1オンスは何グラム？｜シミュラボ',
  desc='オンス(oz)とグラム(g)を相互換算する無料ツール。海外レシピの計量に。1オンス＝約28.35g。',
  ogtitle='オンス⇔グラム 換算｜1オンスは何g？', ogdesc='オンスとグラムを相互換算（1oz=28.35g）。',
  h1='オンス⇔グラム 換算ツール',
  lead='海外レシピでよく出る「オンス(oz)」をグラムに換算。逆方向（g→oz）にも対応します。1オンス＝約28.35g。',
  inputs='''    <h2>⚖️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>値</label><input type="number" id="v" value="8" min="0" step="0.1" inputmode="decimal"></div>
    <div class="field"><label>換算方向</label><select id="dir"><option value="o2g" selected>オンス → グラム</option><option value="g2o">グラム → オンス</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">換算する</button>''',
  result='''      <div class="label" id="lab">グラム</div>
      <div class="big"><span id="big">0</span><span class="unit" id="u">g</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1オンス</div><div class="v accent">28.35g</div></div>
      <div class="stat"><div class="k">1ポンド</div><div class="v">453.6g</div></div>
      <div class="stat"><div class="k">液量オンス</div><div class="v">約29.6ml</div></div></div>''',
  article=C('1オンス（oz・常用オンス）＝ <b>約28.35g</b>。料理では1oz≒28gで概算してOK。液体は「液量オンス(fl oz)＝約29.6ml」と別物なので注意。')+'''
    <h2>オンス・ポンドの換算</h2>
    <div class="note"><strong>計算式</strong><br>グラム ＝ オンス × 28.35<br>オンス ＝ グラム ÷ 28.35／1ポンド(lb) ＝ 16オンス ＝ 453.6g</div>
    <p>海外（特にアメリカ）のレシピは重さをオンス、容量を液量オンス・カップで表します。混同しないようにしましょう。</p>
    <h2>よくある質問</h2>'''+faq([('液量オンスとの違いは？','重さのオンス(28.35g)と容量の液量オンス(29.6ml)は別単位です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['ヤード・ポンド法の換算']),
  js='''  function calc(){const v=Math.max(0,+$('v').value||0),d=$('dir').value;
    let out,unit,lab; if(d==='o2g'){out=v*28.35;unit='g';lab='グラム';}else{out=v/28.35;unit='oz';lab='オンス';}
    $('lab').textContent=lab;$('u').textContent=unit;$('sub').textContent=`${v} ${d==='o2g'?'oz':'g'}`;
    show();anim($('big'),0,out,600,1);
    SHARE=`オンス換算、${v}${d==='o2g'?'oz＝約'+out.toFixed(1)+'g':'g＝約'+out.toFixed(2)+'oz'}でした⚖️`;}''')

add(id='ml-gram', emoji='💧',
  title='ml⇔グラム 換算｜水・牛乳・油は1mlで何グラム？｜シミュラボ',
  desc='水・牛乳・油・醤油・はちみつなど、食材ごとの比重でmlとグラムを相互換算する無料ツール。',
  ogtitle='ml⇔グラム 換算｜1mlは何g？', ogdesc='食材の比重別にmlとグラムを相互換算。',
  h1='ml⇔グラム 換算ツール',
  lead='「1mlは何グラム？」は食材で違います。水・牛乳・油などを選んで、ml↔gを比重込みで換算します。',
  inputs='''    <h2>💧 条件を入れる</h2>
    <div class="row"><div class="field"><label>食材</label><select id="d"><option value="1" selected>水</option><option value="1.03">牛乳</option><option value="0.92">サラダ油</option><option value="1.15">醤油</option><option value="1.4">はちみつ</option><option value="0.55">小麦粉</option><option value="0.85">砂糖</option></select></div>
    <div class="field"><label>換算方向</label><select id="dir"><option value="m2g" selected>ml → g</option><option value="g2m">g → ml</option></select></div></div>
    <div class="field"><label>値</label><input type="number" id="v" value="200" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">換算する</button>''',
  result='''      <div class="label" id="lab">グラム</div>
      <div class="big"><span id="big">0</span><span class="unit" id="u">g</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">比重</div><div class="v accent" id="hi">—</div></div>
      <div class="stat"><div class="k">大さじ換算</div><div class="v" id="osaji">—</div></div>
      <div class="stat"><div class="k">カップ(200ml)</div><div class="v" id="cup">—</div></div></div>''',
  article=C('mlは「容量」、gは「重さ」。<b>水は1ml＝1g</b>ですが、油は0.92g、はちみつは1.4gと比重で変わります。')+'''
    <h2>食材別の比重（1mlあたりのg）</h2>
    <table class="seo-table"><tr><th>食材</th><th>1ml</th></tr>
    <tr><td>水</td><td>1.0g</td></tr><tr><td>牛乳</td><td>1.03g</td></tr><tr><td>サラダ油</td><td>0.92g</td></tr>
    <tr><td>醤油</td><td>1.15g</td></tr><tr><td>はちみつ</td><td>1.4g</td></tr><tr><td>小麦粉</td><td>0.55g</td></tr></table>
    <h2>よくある質問</h2>'''+faq([('水なら同じ？','はい。水は1ml＝1gなので数値はそのままです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['食材の比重（一般的な目安）']),
  js='''  function calc(){const d=+$('d').value||1,dir=$('dir').value,v=Math.max(0,+$('v').value||0);
    let out,unit,lab; if(dir==='m2g'){out=v*d;unit='g';lab='グラム';}else{out=v/d;unit='ml';lab='ミリリットル';}
    $('lab').textContent=lab;$('u').textContent=unit;$('hi').textContent=d+'g/ml';
    $('osaji').textContent=(dir==='m2g'?(v/15).toFixed(1):(out/15).toFixed(1))+'杯';$('cup').textContent=(dir==='m2g'?(v/200).toFixed(2):(out/200).toFixed(2))+'杯';
    $('sub').textContent=`${sel('d').text} ${v}${dir==='m2g'?'ml':'g'}`;
    show();anim($('big'),0,out,600,1);
    SHARE=`ml⇔g換算、${sel('d').text}${v}${dir==='m2g'?'ml＝約'+out.toFixed(1)+'g':'g＝約'+out.toFixed(1)+'ml'}でした💧`;}''')

add(id='ninzu-bunryo', emoji='👨‍👩‍👧‍👦',
  title='レシピ 人数分 換算｜2人分を4人分にする分量は？｜シミュラボ',
  desc='元のレシピの人数と作りたい人数から、材料の分量を自動で増減換算する無料ツール。',
  ogtitle='レシピ 人数分 換算｜分量を自動計算', ogdesc='元の人数と作りたい人数から材料の分量を換算。',
  h1='レシピ 人数分 換算ツール',
  lead='「2人分のレシピを4人分にしたい」を一発換算。元の人数・作りたい人数・材料の量から、必要な分量を計算します。',
  inputs='''    <h2>👨‍👩‍👧‍👦 条件を入れる</h2>
    <div class="row"><div class="field"><label>元のレシピ</label><input type="number" id="from" value="2" min="1" inputmode="numeric"><span class="hint">人分</span></div>
    <div class="field"><label>作りたい</label><input type="number" id="to" value="4" min="1" inputmode="numeric"><span class="hint">人分</span></div></div>
    <div class="field"><label>材料の元の量 <span class="hint">（数値）</span></label><input type="number" id="amt" value="200" min="0" step="0.1" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">分量を換算する</button>''',
  result='''      <div class="label">必要な分量</div>
      <div class="big"><span id="big">0</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">倍率</div><div class="v accent" id="bai">—</div></div>
      <div class="stat"><div class="k">元の量</div><div class="v" id="moto">—</div></div>
      <div class="stat"><div class="k">作る人数</div><div class="v" id="ninzu">—</div></div></div>''',
  article=C('人数分の換算は <b>新しい量 ＝ 元の量 ×（作りたい人数 ÷ 元の人数）</b>。すべての材料に同じ倍率をかけます。')+'''
    <h2>分量換算のコツ</h2>
    <div class="note"><strong>計算式</strong><br>倍率 ＝ 作りたい人数 ÷ 元の人数<br>新しい分量 ＝ 元の分量 × 倍率</div>
    <p>塩・スパイスなどの調味料は、倍率どおりだと濃くなりがち。控えめにして味を見ながら調整するのがおすすめです。</p>
    <h2>よくある質問</h2>'''+faq([('調味料も同じ倍率？','基本は同じですが、塩・香辛料は少し控えめにして味見しながら足すと失敗しません。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['レシピのスケーリング（一般的な考え方）']),
  js='''  function calc(){const f=Math.max(1,+$('from').value||1),t=Math.max(1,+$('to').value||1),a=Math.max(0,+$('amt').value||0);
    const bai=t/f, out=a*bai;
    $('sub').textContent=`${f}人分 → ${t}人分`;$('bai').textContent=bai.toFixed(2)+'倍';$('moto').textContent=num(a);$('ninzu').textContent=t+'人分';
    show();anim($('big'),0,out,600,1);
    SHARE=`レシピ人数分換算、${f}人分→${t}人分で材料は${bai.toFixed(2)}倍（${num(a)}→${out.toFixed(0)}）でした👨‍👩‍👧‍👦`;}''')

add(id='cup-kanzan', emoji='🥛',
  title='計量カップ 換算｜1カップは何ml・何グラム？｜シミュラボ',
  desc='計量カップの杯数から、ml（200ml基準）と食材別のグラムを換算する無料ツール。米用カップ(180ml)にも対応。',
  ogtitle='計量カップ 換算｜1カップは何ml・何g？', ogdesc='カップをml・グラムに換算（米用180ml対応）。',
  h1='計量カップ 換算ツール',
  lead='「1カップは何ml？何グラム？」を一発換算。カップの杯数と中身から、mlとグラムを出します。',
  inputs='''    <h2>🥛 条件を入れる</h2>
    <div class="row"><div class="field"><label>カップ数</label><input type="number" id="n" value="1" min="0" step="0.25" inputmode="decimal"></div>
    <div class="field"><label>カップの種類</label><select id="size"><option value="200" selected>計量カップ（200ml）</option><option value="180">米用カップ（180ml）</option><option value="240">米国カップ（240ml）</option></select></div></div>
    <div class="field"><label>中身</label><select id="d"><option value="1">水・牛乳</option><option value="0.55">小麦粉</option><option value="0.85" selected>砂糖</option><option value="0.83">米</option><option value="0.92">油</option></select></div>
    <button class="btn btn-primary" id="calcBtn">換算する</button>''',
  result='''      <div class="label">容量</div>
      <div class="big"><span id="big">0</span><span class="unit">ml</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">重さ</div><div class="v accent" id="g">—</div></div>
      <div class="stat"><div class="k">大さじ換算</div><div class="v" id="osaji">—</div></div>
      <div class="stat"><div class="k">1カップ</div><div class="v" id="one">—</div></div></div>''',
  article=C('日本の計量カップは <b>1カップ＝200ml</b>。ただし<b>米用カップは180ml（1合）</b>、アメリカのカップは240mlと違うので注意。')+'''
    <h2>カップの種類と容量</h2>
    <table class="seo-table"><tr><th>種類</th><th>容量</th></tr>
    <tr><td>計量カップ（日本）</td><td>200ml</td></tr><tr><td>米用カップ（1合）</td><td>180ml</td></tr>
    <tr><td>米国カップ</td><td>約240ml</td></tr></table>
    <p>重さは中身で変わります（小麦粉1カップ≒110g、砂糖1カップ≒170g）。</p>
    <h2>よくある質問</h2>'''+faq([('米1合は何カップ？','米用カップで1杯（180ml）です。計量カップ(200ml)とは違います。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['計量カップの容量（一般的な目安）']),
  js='''  function calc(){const n=Math.max(0,+$('n').value||0),sz=+$('size').value||200,d=+$('d').value||1;
    const ml=n*sz, g=ml*d;
    $('sub').textContent=`${sel('d').text} ${n}カップ（${sz}ml）`;
    $('g').textContent=num(g)+'g';$('osaji').textContent=(ml/15).toFixed(1)+'杯';$('one').textContent=sz+'ml';
    show();anim($('big'),0,ml,600);
    SHARE=`計量カップ換算、${sel('d').text}${n}カップ＝${num(ml)}ml・約${num(g)}gでした🥛`;}''')

add(id='shokuzai-omosa', emoji='🥚',
  title='食材の重さ目安｜卵1個・豆腐1丁は何グラム？｜シミュラボ',
  desc='卵・豆腐・玉ねぎ・バターなど、よく使う食材1個（1丁）あたりの重さの目安と、個数からの合計グラムを表示する無料ツール。',
  ogtitle='食材の重さ目安｜1個は何グラム？', ogdesc='卵・豆腐などの食材の重さ目安と合計gを計算。',
  h1='食材の重さ目安ツール',
  lead='「卵1個は何グラム？」「豆腐一丁は？」をすぐ確認。食材を選んで個数を入れると、合計の重さが分かります。',
  inputs='''    <h2>🥚 条件を入れる</h2>
    <div class="row"><div class="field"><label>食材</label><select id="g1"><option value="55" selected>卵（Mサイズ・中身）</option><option value="300">豆腐（1丁）</option><option value="50">板チョコ（1枚）</option><option value="200">バター（1箱）</option><option value="60">食パン6枚切（1枚）</option><option value="200">玉ねぎ（1個）</option><option value="150">じゃがいも（1個）</option><option value="150">にんじん（1本）</option><option value="250">りんご（1個）</option><option value="90">バナナ（1本）</option></select></div>
    <div class="field"><label>個数</label><input type="number" id="n" value="1" min="0" step="0.5" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">重さを見る</button>''',
  result='''      <div class="label">合計の重さ（目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">g</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1個あたり</div><div class="v accent" id="per">—</div></div>
      <div class="stat"><div class="k">個数</div><div class="v" id="nv">—</div></div>
      <div class="stat"><div class="k">kg換算</div><div class="v" id="kg">—</div></div></div>''',
  article=C('レシピの「卵1個」は中身約55g（Mサイズ）、「豆腐1丁」は約300〜400g。食材の重さ目安を知っておくと、はかりがなくても分量を調整できます。')+'''
    <h2>よく使う食材の重さ目安</h2>
    <table class="seo-table"><tr><th>食材</th><th>1個（1丁）</th></tr>
    <tr><td>卵（M・中身）</td><td>約55g</td></tr><tr><td>豆腐（1丁）</td><td>約300g</td></tr>
    <tr><td>玉ねぎ</td><td>約200g</td></tr><tr><td>じゃがいも</td><td>約150g</td></tr>
    <tr><td>板チョコ</td><td>約50g</td></tr><tr><td>バター（1箱）</td><td>約200g</td></tr></table>
    <h2>よくある質問</h2>'''+faq([('個体差は？','野菜・果物は大きさで前後します。あくまで平均的な目安です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['食材の標準的な重さの目安']),
  js='''  function calc(){const g1=+$('g1').value||0,n=Math.max(0,+$('n').value||0);const g=g1*n;
    $('sub').textContent=`${sel('g1').text} × ${n}`;$('per').textContent=g1+'g';$('nv').textContent=n+'個';$('kg').textContent=(g/1000).toFixed(2)+'kg';
    show();anim($('big'),0,g,600);
    SHARE=`食材の重さ、${sel('g1').text}×${n}＝約${num(g)}gでした🥚`;}''')

add(id='oven-ondo', emoji='🌡️',
  title='オーブン温度 換算｜摂氏℃⇔華氏℉を計算｜シミュラボ',
  desc='オーブンの温度を摂氏（℃）と華氏（℉）で相互換算する無料ツール。海外レシピのオーブン設定に。',
  ogtitle='オーブン温度 換算｜℃⇔℉', ogdesc='オーブン温度を摂氏と華氏で相互換算。',
  h1='オーブン温度 換算ツール（℃⇔℉）',
  lead='海外レシピの「350°F」は何℃？オーブンの温度を摂氏と華氏で相互換算します。',
  inputs='''    <h2>🌡️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>温度</label><input type="number" id="v" value="180" inputmode="numeric"></div>
    <div class="field"><label>換算方向</label><select id="dir"><option value="c2f" selected>摂氏℃ → 華氏℉</option><option value="f2c">華氏℉ → 摂氏℃</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">換算する</button>''',
  result='''      <div class="label" id="lab">華氏</div>
      <div class="big"><span id="big">0</span><span class="unit" id="u">℉</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">160℃</div><div class="v">320℉</div></div>
      <div class="stat"><div class="k">180℃</div><div class="v accent">350℉</div></div>
      <div class="stat"><div class="k">200℃</div><div class="v">390℉</div></div></div>''',
  article=C('換算式は <b>℉＝℃×9/5＋32</b>、<b>℃＝(℉−32)×5/9</b>。よく使う180℃≒350℉、200℃≒400℉を覚えておくと便利。')+'''
    <h2>オーブン温度の早見</h2>
    <table class="seo-table"><tr><th>摂氏℃</th><th>華氏℉</th></tr>
    <tr><td>150℃</td><td>300℉</td></tr><tr><td>170℃</td><td>340℉</td></tr><tr><td>180℃</td><td>350℉</td></tr>
    <tr><td>200℃</td><td>400℉</td></tr><tr><td>230℃</td><td>450℉</td></tr></table>
    <h2>よくある質問</h2>'''+faq([('予熱は必要？','多くの焼き菓子は予熱必須。指定温度まで温めてから焼きます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['温度の単位換算（摂氏・華氏）']),
  js='''  function calc(){const v=+$('v').value||0,d=$('dir').value;
    let out,unit,lab; if(d==='c2f'){out=v*9/5+32;unit='℉';lab='華氏';}else{out=(v-32)*5/9;unit='℃';lab='摂氏';}
    $('lab').textContent=lab;$('u').textContent=unit;$('sub').textContent=`${v}${d==='c2f'?'℃':'℉'}`;
    show();anim($('big'),0,out,600);
    SHARE=`オーブン温度換算、${v}${d==='c2f'?'℃＝'+Math.round(out)+'℉':'℉＝'+Math.round(out)+'℃'}でした🌡️`;}''')

add(id='age-abura', emoji='🍤',
  title='揚げ物の油の温度 目安｜天ぷら・唐揚げは何度？｜シミュラボ',
  desc='天ぷら・唐揚げ・コロッケなど料理別の揚げ油の適温と、菜箸で見極める方法を表示する無料ツール。',
  ogtitle='揚げ物の油の温度 目安｜何度？', ogdesc='料理別の揚げ油の適温と見極め方を表示。',
  h1='揚げ物の油の温度 目安',
  lead='揚げ物の油は何℃がベスト？料理を選ぶと、適温と「菜箸での見極め方」が分かります。',
  inputs='''    <h2>🍤 料理を選ぶ</h2>
    <div class="field"><label>揚げる料理</label><select id="r"><option value="170">天ぷら（野菜）</option><option value="180" selected>唐揚げ・フライ</option><option value="180">コロッケ</option><option value="160">ドーナツ・かりんとう</option><option value="170">とんかつ</option><option value="200">フライドポテト(2度揚げ仕上げ)</option></select></div>
    <button class="btn btn-primary" id="calcBtn">適温を見る</button>''',
  result='''      <div class="label">適温の目安</div>
      <div class="big"><span id="big">0</span><span class="unit">℃</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">温度帯</div><div class="v accent" id="tai">—</div></div>
      <div class="stat"><div class="k">菜箸の見極め</div><div class="v" id="hashi">—</div></div>
      <div class="stat"><div class="k">パン粉なら</div><div class="v" id="panko">—</div></div></div>''',
  article=C('揚げ油は <b>低温160℃・中温170〜180℃・高温190〜200℃</b>。多くの揚げ物は中温(170〜180℃)が基本です。')+'''
    <h2>油の温度の見極め方（菜箸）</h2>
    <table class="seo-table"><tr><th>温度</th><th>菜箸を入れると</th></tr>
    <tr><td>低温(160℃)</td><td>箸先から小さな泡がゆっくり</td></tr>
    <tr><td>中温(170〜180℃)</td><td>箸全体から細かい泡が次々</td></tr>
    <tr><td>高温(190℃〜)</td><td>勢いよく大きな泡がすぐ出る</td></tr></table>
    <p>パン粉を落とすと、中温は途中まで沈んですぐ浮く、高温はすぐ散る、が目安です。</p>
    <h2>よくある質問</h2>'''+faq([('温度計がない時は？','乾いた菜箸を入れて泡の出方で判断できます（上の表参照）。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['揚げ物の油温（一般的な目安）']),
  js='''  function calc(){const t=+$('r').value||170;
    let tai,hashi,panko; if(t<=160){tai='低温';hashi='泡がゆっくり';panko='沈んでゆっくり浮く';}else if(t<=180){tai='中温';hashi='細かい泡が次々';panko='途中で沈みすぐ浮く';}else{tai='高温';hashi='大きな泡がすぐ';panko='沈まず散る';}
    $('sub').textContent=sel('r').text;$('tai').textContent=tai;$('hashi').textContent=hashi;$('panko').textContent=panko;
    show();anim($('big'),0,t,500);
    SHARE=`揚げ物の油温、${sel('r').text}は約${t}℃（${tai}）が目安でした🍤`;}''')

add(id='pasta-ryou', emoji='🍝',
  title='パスタの量 計算｜1人分は何グラム？ゆで湯と塩も｜シミュラボ',
  desc='食べる人数と量から、パスタの必要グラムと、ゆでるお湯・塩の量を計算する無料ツール。',
  ogtitle='パスタの量 計算｜1人分は何g？', ogdesc='人数からパスタのg・ゆで湯・塩を計算。',
  h1='パスタの量 計算ツール',
  lead='「パスタ1人分は何グラム？」を計算。人数と食べる量から、必要なパスタ・お湯・塩の量を出します。',
  inputs='''    <h2>🍝 条件を入れる</h2>
    <div class="row"><div class="field"><label>人数</label><input type="number" id="n" value="2" min="1" inputmode="numeric"></div>
    <div class="field"><label>1人の量</label><select id="r"><option value="70">少なめ(70g)</option><option value="100" selected>普通(100g)</option><option value="120">多め(120g)</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">必要量を見る</button>''',
  result='''      <div class="label">パスタの量</div>
      <div class="big"><span id="big">0</span><span class="unit">g</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">ゆでるお湯</div><div class="v accent" id="yu">—</div></div>
      <div class="stat"><div class="k">塩(湯の1%)</div><div class="v" id="shio">—</div></div>
      <div class="stat"><div class="k">1人分</div><div class="v" id="one">—</div></div></div>''',
  article=C('パスタは <b>1人分100g</b>が標準（少なめ70g・多め120g）。ゆで湯は<b>パスタ100gに対し1L</b>、塩は<b>湯の1%</b>が黄金比です。')+'''
    <h2>パスタの黄金比</h2>
    <div class="note"><strong>計算式</strong><br>お湯 ＝ パスタの量 × 10（100gに1L）<br>塩 ＝ お湯 × 1%（1Lに10g）</div>
    <p>塩を効かせると下味がつき、ソースとなじみます。たっぷりの湯でゆでると、くっつかず仕上がりが良くなります。</p>
    <h2>よくある質問</h2>'''+faq([('1人分は何g？','標準は乾麺で100g。よく食べる人は120g、軽めなら70〜80gが目安です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['パスタのゆで方（一般的な目安）']),
  js='''  function calc(){const n=Math.max(1,+$('n').value||1),r=+$('r').value||100;const g=n*r,yu=g*10,shio=yu*0.01;
    $('sub').textContent=`${n}人分・1人${r}g`;$('yu').textContent=(yu/1000).toFixed(1)+'L';$('shio').textContent=Math.round(shio)+'g';$('one').textContent=r+'g';
    show();anim($('big'),0,g,600);
    SHARE=`パスタの量、${n}人分＝${num(g)}g（お湯${(yu/1000).toFixed(1)}L・塩${Math.round(shio)}g）でした🍝`;}''')

add(id='gohan-cal', emoji='🍚',
  title='ご飯のカロリー 計算｜茶碗1杯・◯グラムは何kcal？｜シミュラボ',
  desc='ご飯の量（茶碗・丼・グラム）から、カロリーと糖質、角砂糖換算を計算する無料ツール。',
  ogtitle='ご飯のカロリー｜茶碗1杯は何kcal？', ogdesc='ご飯の量からカロリー・糖質・角砂糖換算を計算。',
  h1='ご飯のカロリー 計算ツール',
  lead='ご飯のカロリーは？茶碗・丼・グラムから、カロリーと糖質、角砂糖に換算した量を計算します。',
  inputs='''    <h2>🍚 条件を入れる</h2>
    <div class="row"><div class="field"><label>盛り</label><select id="g1"><option value="100">小盛(100g)</option><option value="150" selected>茶碗1杯(150g)</option><option value="200">大盛(200g)</option><option value="250">丼(250g)</option></select></div>
    <div class="field"><label>杯数</label><input type="number" id="n" value="1" min="0" step="0.5" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">カロリーを見る</button>''',
  result='''      <div class="label">カロリー</div>
      <div class="big"><span id="big">0</span><span class="unit">kcal</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">糖質</div><div class="v accent" id="tou">—</div></div>
      <div class="stat"><div class="k">角砂糖換算</div><div class="v" id="kaku">—</div></div>
      <div class="stat"><div class="k">ご飯の重さ</div><div class="v" id="g">—</div></div></div>''',
  article=C('ご飯は <b>100gで約168kcal</b>、茶碗1杯(150g)で約252kcal。糖質は重さの約37%です。')+'''
    <h2>ご飯のカロリー早見</h2>
    <table class="seo-table"><tr><th>盛り</th><th>カロリー</th><th>糖質</th></tr>
    <tr><td>小盛(100g)</td><td>約168kcal</td><td>約37g</td></tr><tr><td>茶碗1杯(150g)</td><td>約252kcal</td><td>約55g</td></tr>
    <tr><td>大盛(200g)</td><td>約336kcal</td><td>約74g</td></tr><tr><td>丼(250g)</td><td>約420kcal</td><td>約92g</td></tr></table>
    <h2>よくある質問</h2>'''+faq([('糖質制限の目安は？','茶碗1杯で糖質約55g。1食の糖質を抑えたい人は小盛や雑穀米も選択肢です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['日本食品標準成分表（ごはん）']),
  js='''  function calc(){const g1=+$('g1').value||150,n=Math.max(0,+$('n').value||0);const g=g1*n,kcal=g*1.68,tou=g*0.37;
    $('sub').textContent=`${sel('g1').text} × ${n}`;$('tou').textContent=tou.toFixed(0)+'g';$('kaku').textContent=(kcal/16).toFixed(1)+'個';$('g').textContent=num(g)+'g';
    show();anim($('big'),0,kcal,700);
    SHARE=`ご飯のカロリー、${sel('g1').text}×${n}＝約${num(kcal)}kcal（糖質${tou.toFixed(0)}g）でした🍚`;}''')

add(id='dashi-wari', emoji='🍲',
  title='めんつゆ・だしの黄金比 計算｜醤油・みりんの割合は？｜シミュラボ',
  desc='用途（そばつゆ・煮物・天つゆ）を選ぶと、だし・醤油・みりんの黄金比と分量を計算する無料ツール。',
  ogtitle='だし・めんつゆの黄金比｜割合は？', ogdesc='用途別にだし・醤油・みりんの黄金比と分量を計算。',
  h1='めんつゆ・だしの黄金比 計算',
  lead='煮物やめんつゆの味が決まる「黄金比」。用途を選んでだしの量を入れると、醤油・みりんの分量が分かります。',
  inputs='''    <h2>🍲 条件を入れる</h2>
    <div class="row"><div class="field"><label>用途</label><select id="u"><option value="1" selected>かけつゆ(だし8:醤油1:みりん1)</option><option value="2">煮物(だし8:醤油1:みりん1)</option><option value="3">天つゆ(だし4:醤油1:みりん1)</option><option value="4">つけつゆ(だし3:醤油1:みりん1)</option></select></div>
    <div class="field"><label>だしの量 <span class="hint">（ml）</span></label><input type="number" id="dashi" value="400" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">分量を計算する</button>''',
  result='''      <div class="label">醤油の量</div>
      <div class="big"><span id="big">0</span><span class="unit">ml</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">みりん</div><div class="v accent" id="mirin">—</div></div>
      <div class="stat"><div class="k">だし</div><div class="v" id="dv">—</div></div>
      <div class="stat"><div class="k">黄金比</div><div class="v" id="hi">—</div></div></div>''',
  article=C('和食の味は <b>だし：醤油：みりん</b> の比率で決まります。かけつゆ・煮物は <b>8:1:1</b>、天つゆは <b>4:1:1</b> が黄金比。')+'''
    <h2>用途別のだしの黄金比</h2>
    <table class="seo-table"><tr><th>用途</th><th>だし:醤油:みりん</th></tr>
    <tr><td>かけつゆ・煮物</td><td>8:1:1</td></tr><tr><td>天つゆ</td><td>4:1:1</td></tr>
    <tr><td>つけつゆ（濃いめ）</td><td>3:1:1</td></tr></table>
    <p>みりんの代わりに砂糖を使う場合は、みりん大さじ1≒砂糖小さじ1が目安です。</p>
    <h2>よくある質問</h2>'''+faq([('めんつゆ(3倍濃縮)で代用するには？','水でうすめて使います。商品の表示に従うのが確実です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['和食の調味黄金比（一般的な目安）']),
  js='''  const R={'1':8,'2':8,'3':4,'4':3};
  function calc(){const u=$('u').value,dashi=Math.max(0,+$('dashi').value||0);const ratio=R[u]||8;const unit=dashi/ratio;
    $('sub').textContent=`${sel('u').text}・だし${num(dashi)}ml`;$('mirin').textContent=Math.round(unit)+'ml';$('dv').textContent=num(dashi)+'ml';$('hi').textContent=ratio+':1:1';
    show();anim($('big'),0,unit,600);
    SHARE=`だしの黄金比、だし${num(dashi)}mlなら醤油・みりん各${Math.round(unit)}ml（${ratio}:1:1）でした🍲`;}''')

add(id='atsuryoku-jikan', emoji='⏲️',
  title='圧力鍋 時短 計算｜加圧時間はどれくらい短縮？｜シミュラボ',
  desc='通常の調理時間と食材から、圧力鍋を使った場合の加圧時間の目安と時短効果を計算する無料ツール。',
  ogtitle='圧力鍋 時短｜加圧時間は？', ogdesc='通常の調理時間から圧力鍋の加圧時間・時短率を計算。',
  h1='圧力鍋 時短 計算ツール',
  lead='圧力鍋を使うと調理時間はどれくらい短くなる？通常の煮込み時間と食材から、加圧時間の目安を計算します。',
  inputs='''    <h2>⏲️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>通常の調理時間 <span class="hint">（分）</span></label><input type="number" id="t" value="60" min="0" inputmode="numeric"></div>
    <div class="field"><label>食材</label><select id="k"><option value="0.33" selected>肉の煮込み</option><option value="0.25">豆・玄米</option><option value="0.4">カレー・シチュー</option><option value="0.3">魚の骨まで</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">時短を見る</button>''',
  result='''      <div class="label">圧力鍋の加圧時間（目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">分</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">短縮できる時間</div><div class="v accent" id="save">—</div></div>
      <div class="stat"><div class="k">時短率</div><div class="v" id="rate">—</div></div>
      <div class="stat"><div class="k">通常</div><div class="v" id="normal">—</div></div></div>''',
  article=C('圧力鍋は高温・高圧で、煮込み時間を <b>約1/3〜1/4</b> に短縮できます。豆や玄米、肉のかたまりほど効果大。')+'''
    <h2>圧力鍋の時短効果（目安）</h2>
    <table class="seo-table"><tr><th>料理</th><th>通常→加圧</th></tr>
    <tr><td>肉の煮込み</td><td>60分 → 約20分</td></tr><tr><td>豆・玄米</td><td>60分 → 約15分</td></tr>
    <tr><td>カレー・シチュー</td><td>40分 → 約16分</td></tr></table>
    <p>加圧時間に加え、加圧までの加熱・自然放置の時間も必要です。光熱費の節約にもつながります。</p>
    <h2>よくある質問</h2>'''+faq([('加圧時間だけで完成？','加圧後の余熱（自然放置）でさらに火が通ります。レシピの指示に従いましょう。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['圧力鍋調理の一般的な目安']),
  js='''  function calc(){const t=Math.max(0,+$('t').value||0),k=+$('k').value||0.33;const atsu=t*k,save=t-atsu;
    $('sub').textContent=`${sel('k').text}・通常${t}分`;$('save').textContent=Math.round(save)+'分';$('rate').textContent=Math.round((1-k)*100)+'%';$('normal').textContent=t+'分';
    show();anim($('big'),0,atsu,600);
    SHARE=`圧力鍋シミュ、通常${t}分が加圧 約${Math.round(atsu)}分に（${Math.round((1-k)*100)}%時短）でした⏲️`;}''')

add(id='hgm-daiyo', emoji='🥞',
  title='ホットケーキミックス 代用 計算｜薄力粉とBPで何g？｜シミュラボ',
  desc='必要なホットケーキミックスの量から、薄力粉・ベーキングパウダー・砂糖で代用する分量を計算する無料ツール。',
  ogtitle='ホットケーキミックス 代用｜分量は？', ogdesc='HMの必要量から薄力粉・BP・砂糖の代用分量を計算。',
  h1='ホットケーキミックス 代用 計算',
  lead='ホットケーキミックスがない！そんな時、薄力粉・ベーキングパウダー・砂糖で代用する分量を計算します。',
  inputs='''    <h2>🥞 条件を入れる</h2>
    <div class="field"><label>必要なホットケーキミックスの量 <span class="hint">（g）</span></label><input type="number" id="g" value="150" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">代用分量を見る</button>''',
  result='''      <div class="label">薄力粉</div>
      <div class="big"><span id="big">0</span><span class="unit">g</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">ベーキングパウダー</div><div class="v accent" id="bp">—</div></div>
      <div class="stat"><div class="k">砂糖</div><div class="v" id="sugar">—</div></div>
      <div class="stat"><div class="k">HM必要量</div><div class="v" id="hm">—</div></div></div>''',
  article=C('ホットケーキミックスは <b>薄力粉＋ベーキングパウダー＋砂糖</b> で代用できます。目安は薄力粉100gにBP小さじ1(4g)＋砂糖大さじ1〜2。')+'''
    <h2>代用の配合（HM 100gあたり）</h2>
    <div class="note"><strong>計算式（目安）</strong><br>薄力粉 ＝ HM量 × 約0.83<br>ベーキングパウダー ＝ HM量 × 約0.03<br>砂糖 ＝ HM量 × 約0.14</div>
    <p>甘さはお好みで調整可。風味を出したいときはバニラオイルを少量加えても。</p>
    <h2>よくある質問</h2>'''+faq([('ベーキングパウダーがない時は？','重曹で代用も可能ですが量と風味が変わります。BPの使用が無難です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['ホットケーキミックスの代用（一般的な配合）']),
  js='''  function calc(){const g=Math.max(0,+$('g').value||0);const h=g*0.83,bp=g*0.03,su=g*0.14;
    $('sub').textContent=`HM ${num(g)}gの代用`;$('bp').textContent=bp.toFixed(1)+'g(小さじ'+(bp/4).toFixed(1)+')';$('sugar').textContent=su.toFixed(0)+'g';$('hm').textContent=num(g)+'g';
    show();anim($('big'),0,h,600);
    SHARE=`HM代用シミュ、HM${num(g)}g＝薄力粉${h.toFixed(0)}g＋BP${bp.toFixed(1)}g＋砂糖${su.toFixed(0)}gでした🥞`;}''')

add(id='enbun-chomiryo', emoji='🧂',
  title='調味料の塩分 計算｜醤油・味噌の食塩相当量は？｜シミュラボ',
  desc='醤油・味噌・塩などの調味料の使用量から、含まれる塩分（食塩相当量）を計算する無料ツール。減塩に。',
  ogtitle='調味料の塩分 計算｜食塩相当量は？', ogdesc='醤油・味噌などの量から塩分(食塩相当量)を計算。',
  h1='調味料の塩分 計算ツール',
  lead='その調味料、塩分はどれくらい？醤油・味噌などの量から、含まれる食塩相当量を計算します。減塩の目安に。',
  inputs='''    <h2>🧂 条件を入れる</h2>
    <div class="row"><div class="field"><label>調味料</label><select id="p"><option value="14.5" selected>濃口醤油</option><option value="16">薄口醤油</option><option value="12.5">みそ</option><option value="100">塩</option><option value="3.3">ケチャップ</option><option value="1.9">マヨネーズ</option><option value="7.5">ソース(中濃)</option><option value="3.3">めんつゆ(3倍)</option></select></div>
    <div class="field"><label>使う量 <span class="hint">（g）</span></label><input type="number" id="g" value="18" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">塩分を計算する</button>''',
  result='''      <div class="label">食塩相当量</div>
      <div class="big"><span id="big">0</span><span class="unit">g</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1日目標(男7.5g)比</div><div class="v accent" id="m">—</div></div>
      <div class="stat"><div class="k">1日目標(女6.5g)比</div><div class="v" id="f">—</div></div>
      <div class="stat"><div class="k">大さじ1なら</div><div class="v" id="osaji">—</div></div></div>''',
  article=C('塩分（食塩相当量）＝ <b>調味料の量 × 塩分濃度</b>。濃口醤油は約14.5%、味噌は約12.5%。塩そのものは100%です。')+'''
    <h2>調味料の塩分濃度の目安</h2>
    <table class="seo-table"><tr><th>調味料</th><th>塩分濃度</th><th>大さじ1の塩分</th></tr>
    <tr><td>濃口醤油</td><td>約14.5%</td><td>約2.6g</td></tr><tr><td>みそ</td><td>約12.5%</td><td>約2.3g</td></tr>
    <tr><td>ソース(中濃)</td><td>約7.5%</td><td>約1.3g</td></tr><tr><td>ケチャップ</td><td>約3.3%</td><td>約0.5g</td></tr></table>
    <p>厚労省の食塩摂取目標は1日 男性7.5g・女性6.5g未満。調味料の塩分を意識すると減塩しやすくなります。</p>
    <h2>よくある質問</h2>'''+faq([('減塩のコツは？','だしや酸味・香辛料で味を補うと、塩分を減らしても満足感が保てます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['日本食品標準成分表・厚生労働省 食事摂取基準（食塩）']),
  js='''  function calc(){const p=+$('p').value||14.5,g=Math.max(0,+$('g').value||0);const salt=g*p/100;
    $('sub').textContent=`${sel('p').text} ${num(g)}g`;$('m').textContent=Math.round(salt/7.5*100)+'%';$('f').textContent=Math.round(salt/6.5*100)+'%';
    const tbsp=(p===100?18:15*1.0)*p/100; $('osaji').textContent='約'+( (sel('p').text==='塩'?18:15)*p/100 ).toFixed(1)+'g';
    show();anim($('big'),0,salt,600,1);
    SHARE=`調味料の塩分、${sel('p').text}${num(g)}g＝食塩 約${salt.toFixed(1)}gでした🧂`;}''')

add(id='kaitou-jikan', emoji='🧊',
  title='解凍時間の目安｜冷凍肉◯gは何時間で解凍できる？｜シミュラボ',
  desc='冷凍した肉や魚の重さと解凍方法（冷蔵庫・流水・常温）から、解凍にかかる時間の目安を表示する無料ツール。',
  ogtitle='解凍時間の目安｜何時間かかる？', ogdesc='重さと解凍方法から解凍時間の目安を表示。',
  h1='解凍時間の目安ツール',
  lead='冷凍した肉、いつ出せば間に合う？重さと解凍方法から、解凍にかかる時間の目安を表示します。',
  inputs='''    <h2>🧊 条件を入れる</h2>
    <div class="row"><div class="field"><label>重さ <span class="hint">（g）</span></label><input type="number" id="g" value="300" min="0" inputmode="numeric"></div>
    <div class="field"><label>解凍方法</label><select id="m"><option value="cold" selected>冷蔵庫</option><option value="water">流水</option><option value="room">常温</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">解凍時間を見る</button>''',
  result='''      <div class="label">解凍時間の目安</div>
      <div class="big"><span id="big">0</span><span class="unit" id="u">時間</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">方法</div><div class="v accent" id="mv">—</div></div>
      <div class="stat"><div class="k">安全性</div><div class="v" id="anzen">—</div></div>
      <div class="stat"><div class="k">100gあたり</div><div class="v" id="per">—</div></div></div>''',
  article=C('解凍は <b>冷蔵庫がいちばん安全</b>（100gあたり約1時間＝ドリップが少ない）。急ぐなら流水（密封して）。常温は雑菌が増えやすく非推奨です。')+'''
    <h2>解凍方法と時間の目安</h2>
    <table class="seo-table"><tr><th>方法</th><th>目安(300g)</th><th>特徴</th></tr>
    <tr><td>冷蔵庫</td><td>約3〜6時間</td><td>安全・おいしい</td></tr>
    <tr><td>流水(密封)</td><td>約20〜40分</td><td>速い</td></tr>
    <tr><td>常温</td><td>非推奨</td><td>菌が増えやすい</td></tr></table>
    <p>電子レンジの解凍モードも便利ですが、加熱ムラに注意。冷蔵庫解凍は前夜に移しておくのが基本です。</p>
    <h2>よくある質問</h2>'''+faq([('再冷凍はダメ？','一度解凍した生鮮品の再冷凍は品質・衛生面でおすすめできません。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['食品の解凍（衛生・一般的な目安）']),
  js='''  function calc(){const g=Math.max(0,+$('g').value||0),m=$('m').value;
    let val,unit,mv,anzen,per; const u100=g/100;
    if(m==='cold'){val=u100*1.5;unit='時間';mv='冷蔵庫';anzen='◎安全';per='約1.5時間';}
    else if(m==='water'){val=u100*10;unit='分';mv='流水(密封)';anzen='○';per='約10分';}
    else{val=u100*20;unit='分';mv='常温';anzen='△非推奨';per='約20分';}
    $('u').textContent=unit;$('sub').textContent=`${num(g)}g・${mv}`;$('mv').textContent=mv;$('anzen').textContent=anzen;$('per').textContent=per;
    show();anim($('big'),0,val,600,1);
    SHARE=`解凍時間の目安、${num(g)}gを${mv}で約${val.toFixed(1)}${unit}でした🧊`;}''')

add(id='kome-shinsui', emoji='⏳',
  title='米の浸水時間の目安｜夏・冬で何分つける？玄米も｜シミュラボ',
  desc='季節と米の種類（白米・無洗米・玄米）から、炊飯前の浸水（吸水）時間の目安を表示する無料ツール。',
  ogtitle='米の浸水時間｜何分つける？', ogdesc='季節と米の種類から浸水時間の目安を表示。',
  h1='米の浸水時間の目安ツール',
  lead='ふっくら炊くための浸水時間は季節で変わります。季節と米の種類から、つける時間の目安を表示します。',
  inputs='''    <h2>⏳ 条件を入れる</h2>
    <div class="row"><div class="field"><label>季節</label><select id="s"><option value="30">夏（水温高い）</option><option value="45" selected>春・秋</option><option value="90">冬（水温低い）</option></select></div>
    <div class="field"><label>米の種類</label><select id="k"><option value="1" selected>白米</option><option value="1">無洗米</option><option value="4">玄米</option><option value="0.5">早炊き</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">浸水時間を見る</button>''',
  result='''      <div class="label">浸水時間の目安</div>
      <div class="big"><span id="big">0</span><span class="unit">分</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">時間換算</div><div class="v accent" id="hr">—</div></div>
      <div class="stat"><div class="k">最低でも</div><div class="v" id="min">—</div></div>
      <div class="stat"><div class="k">ポイント</div><div class="v" id="point">—</div></div></div>''',
  article=C('白米の浸水は <b>夏30分・冬60〜90分</b>が目安。玄米は吸水しにくいので<b>数時間〜一晩</b>つけるとふっくら炊けます。')+'''
    <h2>浸水時間の目安</h2>
    <table class="seo-table"><tr><th>米・季節</th><th>浸水時間</th></tr>
    <tr><td>白米（夏）</td><td>約30分</td></tr><tr><td>白米（冬）</td><td>約60〜90分</td></tr>
    <tr><td>玄米</td><td>数時間〜一晩</td></tr></table>
    <p>炊飯器の「白米」モードは浸水・蒸らしを含む場合が多いです。時間がない時は早炊きモードでもOK。</p>
    <h2>よくある質問</h2>'''+faq([('浸水なしで炊ける？','炊けますが芯が残りやすいです。最低でも30分の浸水がおすすめです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['炊飯の浸水（一般的な目安）']),
  js='''  function calc(){const s=+$('s').value||45,k=+$('k').value||1;const t=s*k;
    $('sub').textContent=`${sel('s').text}・${sel('k').text}`;$('hr').textContent=(t/60).toFixed(1)+'時間';$('min').textContent='30分';$('point').textContent=k>=4?'玄米は長めに':'冷水でゆっくり';
    show();anim($('big'),0,t,500);
    SHARE=`米の浸水時間、${sel('s').text}の${sel('k').text}は約${Math.round(t)}分が目安でした⏳`;}''')

add(id='suihan-denki', emoji='🔌',
  title='炊飯器の保温 電気代｜つけっぱなしは月いくら？｜シミュラボ',
  desc='炊飯器の保温時間・消費電力から、保温にかかる電気代を1日・月・年で計算する無料ツール。',
  ogtitle='炊飯器の保温 電気代｜月いくら？', ogdesc='保温時間と消費電力から炊飯器の電気代を計算。',
  h1='炊飯器の保温 電気代シミュレーター',
  lead='炊飯器の保温つけっぱなし、電気代はいくら？保温時間と消費電力から、1日・1か月の電気代を計算します。',
  inputs='''    <h2>🔌 条件を入れる</h2>
    <div class="row"><div class="field"><label>1日の保温時間 <span class="hint">（時間）</span></label><input type="number" id="h" value="10" min="0" inputmode="numeric"></div>
    <div class="field"><label>保温の消費電力 <span class="hint">（W）</span></label><input type="number" id="w" value="15" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>電気料金 <span class="hint">（円/kWh）</span></label><input type="number" id="tan" value="31" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">電気代を計算する</button>''',
  result='''      <div class="label">1か月の電気代（保温）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1日あたり</div><div class="v accent" id="day">—</div></div>
      <div class="stat"><div class="k">年間</div><div class="v" id="yr">—</div></div>
      <div class="stat"><div class="k">再加熱との比較</div><div class="v" id="hikaku">—</div></div></div>''',
  article=C('炊飯器の保温は <b>1時間あたり約15W</b>。長時間の保温は電気代に加え、ご飯の味も落ちます。<b>冷凍→レンジ温めの方が安く・おいしい</b>ことも。')+'''
    <h2>保温の電気代の計算</h2>
    <div class="note"><strong>計算式</strong><br>電気代 ＝ 消費電力(W) ÷ 1000 × 時間 × 日数 × 単価(円/kWh)</div>
    <p>1食ごとに冷凍し、食べる分だけ電子レンジで温める方が、長時間保温より省エネでおいしく食べられます。</p>
    <h2>よくある質問</h2>'''+faq([('何時間まで保温OK？','機種によりますが、味の面では数時間まで。長時間なら冷凍がおすすめです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['家電の消費電力（一般的な目安）']),
  js='''  function calc(){const h=Math.max(0,+$('h').value||0),w=Math.max(0,+$('w').value||0),tan=Math.max(0,+$('tan').value||0);
    const day=w/1000*h*tan, mo=day*30, yr=day*365;
    $('sub').textContent=`保温${h}時間/日・${w}W・${tan}円/kWh`;$('day').textContent=yen(day);$('yr').textContent=yen(yr);$('hikaku').textContent='冷凍が割安';
    show();anim($('big'),0,mo,700);
    SHARE=`炊飯器の保温 電気代、1日${h}時間で月 約${yen(mo)}・年${yen(yr)}でした🔌`;}''')

add(id='nikuryo-ninzu', emoji='🍖',
  title='肉・魚の量 計算｜何人前は何グラム？焼肉・鍋・カレー｜シミュラボ',
  desc='人数と料理から、必要な肉・魚の量（グラム）の目安を計算する無料ツール。買い物・献立に。',
  ogtitle='肉の量 計算｜何人前は何g？', ogdesc='人数と料理から肉・魚の必要量の目安を計算。',
  h1='肉・魚の量 計算ツール',
  lead='「何人前で肉は何グラム？」を計算。人数と料理から、買うべき肉・魚の量の目安を出します。',
  inputs='''    <h2>🍖 条件を入れる</h2>
    <div class="row"><div class="field"><label>人数</label><input type="number" id="n" value="4" min="1" inputmode="numeric"></div>
    <div class="field"><label>料理</label><select id="r"><option value="150" selected>焼肉・すき焼き</option><option value="100">カレー・シチュー</option><option value="200">鍋</option><option value="180">ステーキ</option><option value="120">から揚げ</option><option value="80">炒め物</option><option value="100">魚(切り身)</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">必要量を見る</button>''',
  result='''      <div class="label">必要な量（目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">g</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1人分</div><div class="v accent" id="one">—</div></div>
      <div class="stat"><div class="k">100gパック</div><div class="v" id="pack">—</div></div>
      <div class="stat"><div class="k">kg換算</div><div class="v" id="kg">—</div></div></div>''',
  article=C('肉の量は料理で変わり、<b>1人前の目安は炒め物80g・カレー100g・焼肉150g・鍋200g</b>。よく食べる人や成長期は多めに。')+'''
    <h2>料理別 1人前の肉の量</h2>
    <table class="seo-table"><tr><th>料理</th><th>1人前</th></tr>
    <tr><td>炒め物</td><td>約80g</td></tr><tr><td>カレー・シチュー</td><td>約100g</td></tr>
    <tr><td>から揚げ</td><td>約120g</td></tr><tr><td>焼肉・すき焼き</td><td>約150g</td></tr>
    <tr><td>鍋</td><td>約200g</td></tr></table>
    <h2>よくある質問</h2>'''+faq([('子どもがいる場合は？','子どもは大人の半分〜2/3が目安。よく食べる家庭は1.2倍ほど見ておくと安心です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['1人前の分量（一般的な目安）']),
  js='''  function calc(){const n=Math.max(1,+$('n').value||1),r=+$('r').value||150;const g=n*r;
    $('sub').textContent=`${n}人前・${sel('r').text}`;$('one').textContent=r+'g';$('pack').textContent=(g/100).toFixed(1)+'パック';$('kg').textContent=(g/1000).toFixed(2)+'kg';
    show();anim($('big'),0,g,600);
    SHARE=`肉の量、${n}人前の${sel('r').text}＝約${num(g)}gでした🍖`;}''')

add(id='tamago-size', emoji='🥚',
  title='卵のサイズと重さ｜M・Lは何グラム？中身の重さ換算｜シミュラボ',
  desc='卵のサイズ（SS〜LL）と個数から、殻つき・中身の重さの合計と、レシピのMサイズ換算個数を計算する無料ツール。',
  ogtitle='卵のサイズと重さ｜M・Lは何g？', ogdesc='卵のサイズと個数から中身・殻つきの重さを計算。',
  h1='卵のサイズと重さ 計算ツール',
  lead='卵のM・Lは何グラム？サイズと個数から、殻つき・中身の重さと、レシピの「Mサイズ何個分」かを計算します。',
  inputs='''    <h2>🥚 条件を入れる</h2>
    <div class="row"><div class="field"><label>サイズ</label><select id="g1"><option value="46">SS(40〜46g)</option><option value="52">S(46〜52g)</option><option value="58" selected>MS(52〜58g)</option><option value="64">M(58〜64g)</option><option value="70">L(64〜70g)</option><option value="76">LL(70〜76g)</option></select></div>
    <div class="field"><label>個数</label><input type="number" id="n" value="2" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">重さを計算する</button>''',
  result='''      <div class="label">中身の重さ（合計）</div>
      <div class="big"><span id="big">0</span><span class="unit">g</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">殻つき合計</div><div class="v" id="kara">—</div></div>
      <div class="stat"><div class="k">Mサイズ換算</div><div class="v accent" id="m">—</div></div>
      <div class="stat"><div class="k">1個の中身</div><div class="v" id="one">—</div></div></div>''',
  article=C('卵のサイズは<b>殻つきの重さ</b>で決まります（M＝58〜64g）。中身（可食部）は殻を除いた約88%。レシピの「卵1個」はMサイズ（中身約50g）が基準です。')+'''
    <h2>卵のサイズと重さ</h2>
    <table class="seo-table"><tr><th>サイズ</th><th>殻つき</th><th>中身の目安</th></tr>
    <tr><td>S</td><td>46〜52g</td><td>約43g</td></tr><tr><td>M</td><td>58〜64g</td><td>約51g</td></tr>
    <tr><td>L</td><td>64〜70g</td><td>約57g</td></tr><tr><td>LL</td><td>70〜76g</td><td>約62g</td></tr></table>
    <p>お菓子作りは卵の量で仕上がりが変わるため、サイズを揃えるか重さで計るのがおすすめです。</p>
    <h2>よくある質問</h2>'''+faq([('レシピの卵1個は何サイズ？','一般にMサイズ（中身約50g）が基準です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['鶏卵の規格（サイズ別重量）']),
  js='''  function calc(){const k=+$('g1').value||58,n=Math.max(0,+$('n').value||0);const inner=k*0.88,innerTotal=inner*n,karaTotal=k*n;
    $('sub').textContent=`${sel('g1').text} × ${n}個`;$('kara').textContent=num(karaTotal)+'g';$('m').textContent=(innerTotal/51).toFixed(1)+'個分';$('one').textContent=inner.toFixed(0)+'g';
    show();anim($('big'),0,innerTotal,600);
    SHARE=`卵の重さ、${sel('g1').text}×${n}個＝中身 約${num(innerTotal)}g（Mサイズ${(innerTotal/51).toFixed(1)}個分）でした🥚`;}''')

if __name__=='__main__':
    write_all(SIMS)
    print(f'cook done. {len(SIMS)} sims.')
