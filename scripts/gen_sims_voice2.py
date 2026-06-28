# -*- coding: utf-8 -*-
"""シミュラボ：Typeless訴求 第2弾10本（音声入力・時短カテゴリ）。
   gen_sims_voiceのCTA付きTPL（Typelessアフィリ＋adsense焼き込み済）を再利用。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq
from gen_sims_voice import TPL, TYPELESS
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

V = '音声入力・時短'
SIMS = []
def add(**k): k.setdefault('cat', V); SIMS.append(k)
def C(t): return '<div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：'+t+'</div>'

add(id='moji-jikan', emoji='🔊',
  title='文字起こし 所要時間 計算｜録音◯分の手作業は何時間？｜シミュラボ',
  desc='録音時間から、人が手作業で文字起こしする所要時間を計算し、AI音声認識でどれだけ短縮できるかを示す無料シミュレーター。',
  ogtitle='文字起こし 所要時間｜手作業だと何時間？', ogdesc='録音時間から手作業の文字起こし時間とAI短縮効果を計算。',
  h1='文字起こし 所要時間 計算',
  lead='1時間の録音、手で文字起こしすると何時間かかる？録音時間から手作業の所要時間を計算し、AI音声認識での短縮効果を見ます。',
  inputs='''    <h2>🔊 条件を入れる</h2>
    <div class="row"><div class="field"><label>録音時間 <span class="hint">（分）</span></label><input type="number" id="rec" value="60" min="0" inputmode="numeric"></div>
    <div class="field"><label>手作業の倍率 <span class="hint">（録音の何倍）</span></label><input type="number" id="x" value="4" min="1" step="0.5" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">所要時間を見る</button>''',
  result='''      <div class="label">手作業の文字起こし時間</div>
      <div class="big"><span id="big">0</span><span class="unit">分</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">AIなら(目安)</div><div class="v accent" id="ai">—</div></div>
      <div class="stat"><div class="k">短縮できる時間</div><div class="v" id="save">—</div></div>
      <div class="stat"><div class="k">時間に直すと</div><div class="v" id="hr">—</div></div></div>''',
  article=C('手作業の文字起こしは録音時間の <b>約4〜5倍</b>かかります。1時間の録音なら4〜5時間。AIならほぼ録音時間内で下書きが完成します。')+'''
    <h2>文字起こしの所要時間</h2>
    <p>慣れていても、手作業の文字起こしは録音時間の4〜5倍が目安。聞き直し・修正・整文を含めるとさらに膨らみます。AI音声認識を使えば、再生しながらほぼリアルタイムで文字化でき、あとは整えるだけです。</p>
    <div class="note"><strong>計算式</strong><br>手作業の時間 ＝ 録音時間 × 倍率(4〜5)<br>AIの目安 ＝ 録音時間 × 約1.2（再生＋軽い修正）</div>'''+TYPELESS+'''
    <h2>よくある質問</h2>'''+faq([('AIの精度は？','近年のAIは高精度で、固有名詞だけ直せばOKなレベルです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const rec=Math.max(0,+$('rec').value||0),x=Math.max(1,+$('x').value||4);
    const manual=rec*x, ai=rec*1.2, save=manual-ai;
    $('sub').textContent=`録音${rec}分・倍率${x}倍`;
    $('ai').textContent=num(ai)+'分';$('save').textContent=num(save)+'分';$('hr').textContent=(manual/60).toFixed(1)+'時間';
    show();anim($('big'),0,manual,800);
    SHARE=`文字起こし所要時間シミュ、録音${rec}分の手作業は約${num(manual)}分。AIなら約${num(ai)}分でした🔊`;}''')

add(id='voicememo-okoshi', emoji='🎙️',
  title='ボイスメモ 文字起こし 時短｜録音メモを文字化する時間｜シミュラボ',
  desc='1日のボイスメモ録音時間から、手で文字起こしする手間と、AIで文字化したときの年間の時短を計算する無料シミュレーター。',
  ogtitle='ボイスメモ 文字起こし 時短', ogdesc='ボイスメモの文字起こしをAIにした時の年間時短を計算。',
  h1='ボイスメモ 文字起こし 時短シミュレーター',
  lead='思いついたことをボイスメモ。でも文字に起こすのが面倒…。1日の録音時間から、AI文字起こしで浮く年間の時間を計算します。',
  inputs='''    <h2>🎙️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>1日のボイスメモ録音 <span class="hint">（分）</span></label><input type="number" id="rec" value="10" min="0" inputmode="numeric"></div>
    <div class="field"><label>時間価値 <span class="hint">（円/時）</span></label><input type="number" id="w" value="2000" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">年間の時短を見る</button>''',
  result='''      <div class="label">年間で浮く時間の価値</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1日の時短</div><div class="v accent" id="day">—</div></div>
      <div class="stat"><div class="k">年間の時短時間</div><div class="v" id="yr">—</div></div>
      <div class="stat"><div class="k">手作業なら年</div><div class="v" id="manual">—</div></div></div>''',
  article=C('ボイスメモを手で文字起こしすると録音の約4倍。AIなら一瞬で文字化でき、その差がまるごと時短になります。')+'''
    <h2>ボイスメモ活用の壁を解消</h2>
    <p>移動中や寝る前に音声でメモするのは手軽ですが、あとで文字に起こすのが面倒で結局使わなくなりがち。AI文字起こしなら録音がそのままテキストになり、メモ習慣が続きます。</p>
    <div class="note"><strong>計算式</strong><br>手作業 ＝ 録音 × 4／AI ≒ 録音 × 1.1<br>年間の時短 ＝ 1日の差 × 365</div>'''+TYPELESS+'''
    <h2>よくある質問</h2>'''+faq([('iPhoneのボイスメモでも？','録音した音声をAIツールに通せば文字化できます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const rec=Math.max(0,+$('rec').value||0),w=Math.max(0,+$('w').value||0);
    const day=rec*(4-1.1), yrMin=day*365, yrH=yrMin/60, money=yrH*w, manualY=rec*4*365/60;
    $('sub').textContent=`1日${rec}分・時間価値${num(w)}円`;
    $('day').textContent=num(day)+'分';$('yr').textContent=num(yrH)+'時間';$('manual').textContent=num(manualY)+'時間';
    show();anim($('big'),0,money,800);
    SHARE=`ボイスメモ文字起こしシミュ、AI化で年間 約${yen(money)}（${num(yrH)}時間）の時短でした🎙️`;}''')

add(id='youtube-moji', emoji='📺',
  title='YouTube・動画 文字起こし時間｜字幕作成は何時間かかる？｜シミュラボ',
  desc='動画の長さと本数から、手作業で字幕・文字起こしを作る時間と、AI文字起こしでの短縮効果を計算する無料シミュレーター。',
  ogtitle='動画・YouTube 文字起こし時間', ogdesc='動画の字幕作成の手作業時間とAI短縮を計算。',
  h1='YouTube・動画 文字起こし時間シミュレーター',
  lead='動画の字幕や文字起こし、手作業だと何時間？動画の長さと本数から所要時間を計算し、AIでの短縮効果を見ます。発信者・編集者に。',
  inputs='''    <h2>📺 条件を入れる</h2>
    <div class="row"><div class="field"><label>1本の動画の長さ <span class="hint">（分）</span></label><input type="number" id="len" value="15" min="0" inputmode="numeric"></div>
    <div class="field"><label>月の本数 <span class="hint">（本）</span></label><input type="number" id="n" value="8" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">作成時間を見る</button>''',
  result='''      <div class="label">月の文字起こし時間（手作業）</div>
      <div class="big"><span id="big">0</span><span class="unit">時間</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">AIなら月</div><div class="v accent" id="ai">—</div></div>
      <div class="stat"><div class="k">月の短縮</div><div class="v" id="save">—</div></div>
      <div class="stat"><div class="k">年間の短縮</div><div class="v" id="yr">—</div></div></div>''',
  article=C('動画の文字起こし・字幕作成は、尺の <b>約5倍</b>の時間がかかります。AI字幕＋整文なら大幅短縮でき、SEO・アクセシビリティにも有利です。')+'''
    <h2>動画の文字起こしを効率化</h2>
    <p>字幕や概要欄、ブログ化のための文字起こしは、発信を伸ばすうえで重要ですが手間が大きい作業。AI文字起こしを使えば、話した内容が一気にテキスト化され、字幕・記事化のスピードが激変します。</p>
    <div class="note"><strong>計算式</strong><br>手作業 ＝ 尺 × 5 × 本数／AI ≒ 尺 × 1.5 × 本数</div>'''+TYPELESS+'''
    <h2>よくある質問</h2>'''+faq([('SEOに効く？','動画を記事化すると検索流入が増えます。文字起こしはその第一歩です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const len=Math.max(0,+$('len').value||0),n=Math.max(0,+$('n').value||0);
    const manual=len*5*n/60, ai=len*1.5*n/60, save=manual-ai;
    $('sub').textContent=`1本${len}分・月${n}本`;
    $('ai').textContent=ai.toFixed(1)+'時間';$('save').textContent=save.toFixed(1)+'時間';$('yr').textContent=num(save*12)+'時間';
    show();anim($('big'),0,manual,800,1);
    SHARE=`動画文字起こしシミュ、月${n}本の字幕は手作業約${manual.toFixed(1)}時間。AIなら${ai.toFixed(1)}時間でした📺`;}''')

add(id='flick-voice', emoji='📱',
  title='音声入力 vs フリック入力 速度｜スマホ入力どっちが速い？｜シミュラボ',
  desc='1日のスマホ文字入力量から、フリック入力と音声入力の所要時間を比較し、音声入力で浮く時間を計算する無料シミュレーター。',
  ogtitle='音声入力 vs フリック｜どっちが速い？', ogdesc='スマホの入力量からフリックと音声入力の時間差を計算。',
  h1='音声入力 vs フリック入力 速度シミュレーター',
  lead='スマホの入力、フリックと音声でどれだけ違う？1日の入力文字数から、音声入力で浮く時間を計算します。',
  inputs='''    <h2>📱 条件を入れる</h2>
    <div class="row"><div class="field"><label>1日のスマホ入力量 <span class="hint">（文字）</span></label><input type="number" id="ch" value="2000" min="0" inputmode="numeric"></div>
    <div class="field"><label>フリック速度 <span class="hint">（文字/分）</span></label><input type="number" id="fl" value="60" min="10" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">速度を比べる</button>''',
  result='''      <div class="label">音声入力で1日に浮く時間</div>
      <div class="big"><span id="big">0</span><span class="unit">分</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">フリック</div><div class="v" id="flv">—</div></div>
      <div class="stat"><div class="k">音声入力</div><div class="v accent" id="vo">—</div></div>
      <div class="stat"><div class="k">年間の時短</div><div class="v" id="yr">—</div></div></div>''',
  article=C('音声入力は約300字/分。フリックが60字/分なら、音声は <b>約5倍速</b>。スマホ入力ほど差が出ます。')+'''
    <h2>スマホ入力こそ音声が効く</h2>
    <p>フリック入力は速い人でも60〜80字/分ほど。一方、話す速さは約300字/分です。チャットやメモ、SNS投稿など、スマホでの文字入力を音声に変えると、毎日まとまった時間が浮きます。</p>
    <div class="note"><strong>計算式</strong><br>フリック時間 ＝ 文字数 ÷ フリック速度<br>音声時間 ＝ 文字数 ÷ 300<br>差 × 365 ＝ 年間の時短</div>'''+TYPELESS+'''
    <h2>よくある質問</h2>'''+faq([('外で使いづらい？','小声入力やイヤホンマイク対応のツールも。自宅・移動中だけでも効果的です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const ch=Math.max(0,+$('ch').value||0),fl=Math.max(1,+$('fl').value||60);
    const flm=ch/fl, vom=ch/300, day=flm-vom, yr=day*365/60;
    $('sub').textContent=`1日${num(ch)}字・フリック${fl}字/分`;
    $('flv').textContent=num(flm)+'分';$('vo').textContent=num(vom)+'分';$('yr').textContent=num(yr)+'時間';
    show();anim($('big'),0,day,800);
    SHARE=`音声入力vsフリック、音声で1日約${num(day)}分・年${num(yr)}時間も浮く計算でした📱`;}''')

add(id='typing-kotsu', emoji='⌨️',
  title='タイピングを速くする vs 音声入力｜どっちが早い？診断｜シミュラボ',
  desc='今のタイピング速度から、練習で上達する時間と、音声入力に切り替えた場合の速さを比較し、最適な選択を提案する無料ツール。',
  ogtitle='タイピング練習 vs 音声入力｜どっちが早い？', ogdesc='今のタイピング速度から音声入力との速さを比較。',
  h1='タイピングを速くする vs 音声入力 診断',
  lead='タイピングを練習して速くする？それとも音声入力に切り替える？今の速度から、どちらが早く「速く書ける」かを比べます。',
  inputs='''    <h2>⌨️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>今のタイピング速度 <span class="hint">（文字/分）</span></label><input type="number" id="sp" value="120" min="10" inputmode="numeric"></div>
    <div class="field"><label>1日の入力量 <span class="hint">（文字）</span></label><input type="number" id="ch" value="4000" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">どっちが早いか見る</button>''',
  result='''      <div class="label">音声入力で1日に浮く時間</div>
      <div class="big"><span id="big">0</span><span class="unit">分</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">今の入力時間</div><div class="v" id="now">—</div></div>
      <div class="stat"><div class="k">音声入力なら</div><div class="v accent" id="vo">—</div></div>
      <div class="stat"><div class="k">判定</div><div class="v" id="judge">—</div></div></div>''',
  article=C('タイピングの上達には数十時間の練習が必要。一方、音声入力は <b>今日から約300字/分</b>。すでに速い人でも音声の方が速いことが多いです。')+'''
    <h2>練習より「切り替え」が早い</h2>
    <p>タイピングを今より速くするには、まとまった練習時間がかかります。しかも上限はせいぜい150〜200字/分ほど。音声入力なら練習ゼロで約300字/分。「速く書きたい」目的なら、切り替えが近道です。</p>
    <div class="note"><strong>計算式</strong><br>今の時間 ＝ 文字数 ÷ タイピング速度<br>音声 ＝ 文字数 ÷ 300<br>差が音声入力で浮く時間</div>'''+TYPELESS+'''
    <h2>よくある質問</h2>'''+faq([('コードも音声で？','コードや細かい編集はキーボードが向きますが、文章は音声が速いです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const sp=Math.max(1,+$('sp').value||120),ch=Math.max(0,+$('ch').value||0);
    const now=ch/sp, vo=ch/300, day=now-vo;
    $('sub').textContent=`タイピング${sp}字/分・1日${num(ch)}字`;
    $('now').textContent=num(now)+'分';$('vo').textContent=num(vo)+'分';$('judge').textContent=day>0?'音声入力が速い':'今のままでも十分速い';
    show();anim($('big'),0,Math.max(0,day),800);
    SHARE=`タイピングvs音声入力、音声なら1日約${num(Math.max(0,day))}分速い計算でした⌨️`;}''')

add(id='fukugyo-okoshi', emoji='💰',
  title='文字起こし副業 収入シミュレーター｜月いくら稼げる？｜シミュラボ',
  desc='受ける録音時間と単価から、文字起こし副業の月収目安を計算し、AIで効率化したときの時給アップを示す無料シミュレーター。',
  ogtitle='文字起こし副業 収入｜月いくら？', ogdesc='録音時間と単価から文字起こし副業の月収を計算。',
  h1='文字起こし副業 収入シミュレーター',
  lead='文字起こし副業で月いくら稼げる？受ける量と単価から月収を計算し、AIツールで効率化したときの実質時給アップも見ます。',
  inputs='''    <h2>💰 条件を入れる</h2>
    <div class="row"><div class="field"><label>月に受ける録音 <span class="hint">（分）</span></label><input type="number" id="rec" value="600" min="0" inputmode="numeric"></div>
    <div class="field"><label>単価 <span class="hint">（円/録音1分）</span></label><input type="number" id="tan" value="200" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">月収・時給を見る</button>''',
  result='''      <div class="label">文字起こし副業の月収</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">手作業の時給</div><div class="v" id="t1">—</div></div>
      <div class="stat"><div class="k">AI活用の時給</div><div class="v accent" id="t2">—</div></div>
      <div class="stat"><div class="k">作業時間/月</div><div class="v" id="hr">—</div></div></div>''',
  article=C('文字起こし副業は単価が決まっているので、<b>速く仕上げるほど時給が上がります</b>。AI音声入力で下書きを作れば、同じ報酬でも時給が大きく跳ね上がります。')+'''
    <h2>文字起こし副業で稼ぐコツ</h2>
    <p>報酬は録音時間×単価で固定。手作業は録音の約4倍の時間がかかるため、時給は意外と伸びません。AIで文字化→人が整える、にすると作業時間が大幅に減り、実質時給が2〜3倍になることも。</p>
    <div class="note"><strong>計算式</strong><br>月収 ＝ 録音分 × 単価<br>手作業時間 ＝ 録音 × 4／AI活用 ≒ 録音 × 1.5<br>時給 ＝ 月収 ÷ 作業時間</div>'''+TYPELESS+'''
    <h2>よくある質問</h2>'''+faq([('未経験でもできる？','可能ですが時給は低めになりがち。AI活用で効率を上げるのが現実的です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const rec=Math.max(0,+$('rec').value||0),tan=Math.max(0,+$('tan').value||0);
    const income=rec*tan, hM=rec*4/60, hAI=rec*1.5/60, t1=hM>0?income/hM:0, t2=hAI>0?income/hAI:0;
    $('sub').textContent=`月${rec}分・単価${num(tan)}円/分`;
    $('t1').textContent=yen(t1);$('t2').textContent=yen(t2);$('hr').textContent=hAI.toFixed(1)+'時間';
    show();anim($('big'),0,income,800);
    SHARE=`文字起こし副業シミュ、月収${yen(income)}・AI活用で時給${yen(t2)}（手作業${yen(t1)}）でした💰`;}''')

add(id='ronbun-voice', emoji='📝',
  title='レポート・論文 音声執筆 時短｜何時間ラクになる？｜シミュラボ',
  desc='レポート・論文の文字数から、タイピング執筆と音声入力での執筆時間を比較し、短縮できる時間を計算する学生向け無料シミュレーター。',
  ogtitle='レポート・論文 音声執筆 時短', ogdesc='文字数から論文・レポートを音声執筆した時の時短を計算。',
  h1='レポート・論文 音声執筆 時短シミュレーター',
  lead='レポートや論文、音声入力で書いたら何時間ラクになる？文字数から、タイピングと音声執筆の時間差を計算します。学生・研究者に。',
  inputs='''    <h2>📝 条件を入れる</h2>
    <div class="row"><div class="field"><label>書く文字数 <span class="hint">（字）</span></label><input type="number" id="ch" value="8000" min="0" inputmode="numeric"></div>
    <div class="field"><label>タイピング速度 <span class="hint">（字/分）</span></label><input type="number" id="sp" value="80" min="10" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">時短を見る</button>''',
  result='''      <div class="label">音声執筆で短縮できる時間</div>
      <div class="big"><span id="big">0</span><span class="unit">分</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">タイピング執筆</div><div class="v" id="t1">—</div></div>
      <div class="stat"><div class="k">音声執筆(目安)</div><div class="v accent" id="t2">—</div></div>
      <div class="stat"><div class="k">短縮率</div><div class="v" id="rate">—</div></div></div>''',
  article=C('論文・レポートは「考えながら打つ」と手が止まりがち。骨子を決めて<b>口述→AIが整文</b>にすると、執筆時間が半分近くになることもあります。')+'''
    <h2>音声で書く論文・レポート</h2>
    <p>構成さえ決まっていれば、内容を話して一気に下書きするのが速い書き方。話すと思考が止まりにくく、ゼロから打つよりスピードが上がります。あとはAIが書き言葉に整え、推敲するだけ。</p>
    <div class="note"><strong>計算式</strong><br>タイピング ＝ 文字数 ÷ 速度<br>音声執筆 ≒ タイピングの約55%（構成・推敲を含む実感値）</div>'''+TYPELESS+'''
    <h2>よくある質問</h2>'''+faq([('話し言葉にならない？','AIが書き言葉・論文調に整えてくれます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const ch=Math.max(0,+$('ch').value||0),sp=Math.max(1,+$('sp').value||80);
    const t1=ch/sp, t2=t1*0.55, save=t1-t2;
    $('sub').textContent=`${num(ch)}字・タイピング${sp}字/分`;
    $('t1').textContent=num(t1)+'分';$('t2').textContent=num(t2)+'分';$('rate').textContent='約'+Math.round(save/t1*100)+'%';
    show();anim($('big'),0,save,800);
    SHARE=`論文・レポート音声執筆シミュ、${num(ch)}字で約${num(save)}分（${Math.round(save/t1*100)}%）短縮でした📝`;}''')

add(id='nippou-voice', emoji='🗒️',
  title='日報・週報 音声入力 時短｜報告書作成は年何時間？｜シミュラボ',
  desc='1日の日報・報告書の作成時間から、音声入力で短縮できる年間の時間と人件費を計算する無料シミュレーター。',
  ogtitle='日報・週報 音声入力 時短', ogdesc='日報の作成を音声入力にした時の年間時短を計算。',
  h1='日報・週報 音声入力 時短シミュレーター',
  lead='毎日の日報・報告書、地味に時間を取られていませんか。1日の作成時間から、音声入力で浮く年間の時間とコストを計算します。',
  inputs='''    <h2>🗒️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>1日の報告作成時間 <span class="hint">（分）</span></label><input type="number" id="min" value="20" min="0" inputmode="numeric"></div>
    <div class="field"><label>時給 <span class="hint">（円）</span></label><input type="number" id="w" value="2500" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">年間の時短を見る</button>''',
  result='''      <div class="label">年間の削減額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1日の時短</div><div class="v accent" id="day">—</div></div>
      <div class="stat"><div class="k">年間の時短時間</div><div class="v" id="yr">—</div></div>
      <div class="stat"><div class="k">10年で</div><div class="v" id="y10">—</div></div></div>''',
  article=C('定型的な日報・週報は音声入力と相性抜群。話すだけで下書きができ、作成時間を <b>約2/3</b> 削減できます。')+'''
    <h2>毎日の報告書を音声で</h2>
    <p>日報・週報・営業報告は形式が決まっているものが多く、音声入力＋AI整形がはまります。「今日やったこと」を話すだけで体裁の整った報告書に。毎日の積み重ねが年間では大きな時短に。</p>
    <div class="note"><strong>計算式</strong><br>年間の時短 ＝ 1日の作成時間 × 2/3 × 240営業日<br>削減額 ＝ 時短時間 × 時給</div>'''+TYPELESS+'''
    <h2>よくある質問</h2>'''+faq([('決まった項目でも便利？','項目を話すだけで整形され、むしろ定型ほど効果的です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const mi=Math.max(0,+$('min').value||0),w=Math.max(0,+$('w').value||0);
    const day=mi*2/3, yrH=day*240/60, money=yrH*w;
    $('sub').textContent=`1日${mi}分・時給${num(w)}円`;
    $('day').textContent=num(day)+'分';$('yr').textContent=num(yrH)+'時間';$('y10').textContent=yen(money*10);
    show();anim($('big'),0,money,800);
    SHARE=`日報・週報 音声入力シミュ、年間 約${yen(money)}（${num(yrH)}時間）の時短でした🗒️`;}''')

add(id='zoom-gijiroku', emoji='💻',
  title='Web会議(Zoom)議事録 時短｜文字起こしで年いくら削減？｜シミュラボ',
  desc='週のWeb会議数と1回の議事録作成時間から、AI文字起こしで削減できる年間の作業時間と人件費を計算する無料シミュレーター。',
  ogtitle='Web会議(Zoom)議事録 時短', ogdesc='Web会議の議事録をAI文字起こしにした時の年間削減を計算。',
  h1='Web会議(Zoom)議事録 時短シミュレーター',
  lead='オンライン会議の議事録づくり、AI文字起こしにすると年間どれだけ浮く？週の会議数と作成時間から削減効果を計算します。',
  inputs='''    <h2>💻 条件を入れる</h2>
    <div class="row"><div class="field"><label>週のWeb会議数 <span class="hint">（回）</span></label><input type="number" id="n" value="6" min="0" inputmode="numeric"></div>
    <div class="field"><label>1回の議事録作成 <span class="hint">（分）</span></label><input type="number" id="min" value="35" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>時給 <span class="hint">（円）</span></label><input type="number" id="w" value="3000" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">削減額を見る</button>''',
  result='''      <div class="label">議事録の年間 削減額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">年間の時短</div><div class="v accent" id="yr">—</div></div>
      <div class="stat"><div class="k">年間の会議数</div><div class="v" id="cnt">—</div></div>
      <div class="stat"><div class="k">1回あたり時短</div><div class="v" id="per">—</div></div></div>''',
  article=C('Zoom等のWeb会議は録音・録画が簡単。<b>AI文字起こし＋要約</b>にすれば、議事録の作成時間を約2/3削減できます。')+'''
    <h2>オンライン会議の議事録を自動化</h2>
    <p>Web会議は音声を取りやすいのが利点。録音をAIで文字起こしし、要点をまとめれば、議事録は確認・整形だけで完成します。会議が多いチームほど効果は絶大です。</p>
    <div class="note"><strong>計算式</strong><br>年間削減 ＝ 1回の作成 × 2/3 × 週の会議数 × 52 × 時給</div>'''+TYPELESS+'''
    <h2>よくある質問</h2>'''+faq([('録音は必要？','録音（録画）があればAIで文字起こしできます。会議ツールの録音機能でOKです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const n=Math.max(0,+$('n').value||0),mi=Math.max(0,+$('min').value||0),w=Math.max(0,+$('w').value||0);
    const per=mi*2/3, yrH=per*n*52/60, money=yrH*w;
    $('sub').textContent=`週${n}回・1回${mi}分・時給${num(w)}円`;
    $('yr').textContent=num(yrH)+'時間';$('cnt').textContent=num(n*52)+'回';$('per').textContent=num(per)+'分';
    show();anim($('big'),0,money,800);
    SHARE=`Web会議 議事録シミュ、AI文字起こしで年間 約${yen(money)}（${num(yrH)}時間）削減でした💻`;}''')

add(id='shukatsu-voice', emoji='🎓',
  title='就活ES 音声入力 時短｜エントリーシート作成は何時間？｜シミュラボ',
  desc='エントリーシートの設問数・文字数と応募社数から、ES作成の総時間と、音声入力で短縮できる時間を計算する就活生向け無料シミュレーター。',
  ogtitle='就活ES 音声入力 時短', ogdesc='ES作成の総時間と音声入力での短縮を計算。',
  h1='就活ES 音声入力 時短シミュレーター',
  lead='エントリーシート、何時間かかってる？設問数・文字数・社数から総作成時間を計算し、音声入力での時短を見ます。就活生に。',
  inputs='''    <h2>🎓 条件を入れる</h2>
    <div class="row"><div class="field"><label>1社のES合計文字数 <span class="hint">（字）</span></label><input type="number" id="ch" value="2000" min="0" inputmode="numeric"></div>
    <div class="field"><label>応募社数 <span class="hint">（社）</span></label><input type="number" id="n" value="20" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">時短を見る</button>''',
  result='''      <div class="label">音声入力で短縮できる時間</div>
      <div class="big"><span id="big">0</span><span class="unit">時間</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">手書き/タイピング</div><div class="v" id="t1">—</div></div>
      <div class="stat"><div class="k">音声入力(目安)</div><div class="v accent" id="t2">—</div></div>
      <div class="stat"><div class="k">ES総文字数</div><div class="v" id="total">—</div></div></div>''',
  article=C('ESは1社で複数設問×数百字。何十社も出すと膨大な作業に。<b>話して下書き→AIが整文</b>すれば、考えをまとめる時間も短縮できます。')+'''
    <h2>就活ESを音声で効率化</h2>
    <p>自己PRやガクチカは「話す方が言葉が出る」もの。エピソードを口に出して下書きし、AIで文章に整えると、ゼロから書くより速く・濃い内容になります。空いた時間は面接対策や企業研究に回せます。</p>
    <div class="note"><strong>計算式</strong><br>総文字数 ＝ 1社の文字数 × 社数<br>タイピング ＝ 総字 ÷ 60字/分／音声 ≒ その約55%</div>'''+TYPELESS+'''
    <h2>よくある質問</h2>'''+faq([('丸写しにならない？','話した内容をAIが整えるだけなので、あなたの言葉・経験がベースです。最終チェックは必ず。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const ch=Math.max(0,+$('ch').value||0),n=Math.max(0,+$('n').value||0);
    const total=ch*n, t1=total/60/60, t2=t1*0.55, save=t1-t2;
    $('sub').textContent=`1社${num(ch)}字・${n}社`;
    $('t1').textContent=t1.toFixed(1)+'時間';$('t2').textContent=t2.toFixed(1)+'時間';$('total').textContent=num(total)+'字';
    show();anim($('big'),0,save,800,1);
    SHARE=`就活ES音声入力シミュ、${n}社ぶんで約${save.toFixed(1)}時間も短縮できる計算でした🎓`;}''')

def render():
    for s in SIMS:
        d=os.path.join(ROOT,'sims',s['id']); os.makedirs(d,exist_ok=True)
        html=(TPL.replace('__TITLE__',s['title']).replace('__DESC__',s['desc'])
              .replace('__OGTITLE__',s['ogtitle']).replace('__OGDESC__',s['ogdesc'])
              .replace('__CAT__',V).replace('__H1__',s['h1']).replace('__LEAD__',s['lead'])
              .replace('__INPUTS__',s['inputs']).replace('__RESULT__',s['result'])
              .replace('__ARTICLE__',s['article']).replace('__JS__',s['js']).replace('__ID__',s['id']))
        with open(os.path.join(d,'index.html'),'w',encoding='utf-8') as f: f.write(html)
        print('created sims/'+s['id'])

if __name__=='__main__':
    render()
    print(f'voice2 done. {len(SIMS)} sims.')
