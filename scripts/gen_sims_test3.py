# -*- coding: utf-8 -*-
"""シミュラボ：テスト系 第3弾10本（既存 slug=brain「脳トレ・診断テスト」に追加）。モスキート音/反射神経/視力/色覚など測定系ゲーム。
gen_sims_tool TPL流用（calcBtn=スタート、測定UIは__JS__で構築）。CTAなし。

seo_internal.py / gen_images.py のauto-importに 'gen_sims_test3' を追加して使う。
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq
from gen_sims_tool import TPL, viz
from sim_quiz import make_engines
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CAT = '脳トレ・診断テスト'
SIMS = []
tally_quiz, num_quiz, band_quiz, add, q_article, render = make_engines(SIMS, CAT, TPL, viz)

STYLE = '''<style>
.gm-wrap{margin-top:6px}
.gm-bar{display:flex;gap:10px;justify-content:center;margin:4px 0 10px;font-weight:800;color:var(--ink-2);font-size:14px}
.gm-bar b{color:var(--teal-d);font-size:18px}
.gm-stage{min-height:180px;display:flex;flex-direction:column;align-items:center;justify-content:center;border:1.5px solid var(--line);border-radius:14px;padding:18px;background:#fff;text-align:center}
.gm-opt{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-top:12px}
.gm-opt button{padding:10px 16px;border:1.5px solid var(--line);border-radius:10px;background:#fff;font-size:16px;font-weight:700;cursor:pointer}
.gm-opt button:hover{border-color:var(--teal)}
.gm-big-btn{font-size:18px;font-weight:800;padding:16px 28px;border-radius:12px;border:none;background:var(--teal);color:#fff;cursor:pointer}
.gm-arena{position:relative;height:260px;border:1.5px solid var(--line);border-radius:14px;background:#f8fafc;overflow:hidden}
.gm-target{position:absolute;width:48px;height:48px;border-radius:50%;background:var(--teal);cursor:pointer}
.landolt{font-weight:900;line-height:1;color:var(--ink);font-family:sans-serif}
</style>'''

def game(id, emoji, title, desc, ogtitle, ogdesc, h1, lead, intro_html, start_label, result_html, article, js):
    inputs = STYLE + '\n    <h2>'+intro_html+'</h2>\n    <div class="gm-wrap"><div class="gm-bar" id="bar"></div><div id="game"></div></div>\n    <button class="btn btn-primary" id="calcBtn">'+start_label+'</button>'
    add(id=id, emoji=emoji, title=title, desc=desc, ogtitle=ogtitle, ogdesc=ogdesc, h1=h1, lead=lead,
        inputs=inputs, result=result_html, article=article, js=js)

RES = lambda lbl,unit: '''      <div class="label">'''+lbl+'''</div>
      <div class="big"><span id="big">0</span><span class="unit">'''+unit+'''</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="grade" style="text-align:left;margin-top:12px;">—</div>
      <button class="btn btn-ghost" id="again" style="margin-top:12px;">もう一度</button>'''

def art(intro, h2, p, faqs, warn=''):
    w = ('<br><b>'+warn+'</b>') if warn else ''
    return ('    <div class="note"><strong>これは何？</strong>：'+intro+w+'</div>\n    <h2>'+h2+'</h2>\n    <p>'+p+'</p>\n    <h2>よくある質問</h2>'+faq(faqs))

# ============================================================
# 1. モスキート音（モスキート音 28000/KD11/TP31000）★★ — 聴力年齢
# ============================================================
game('mosquito-on','🦟',
  'モスキート音テスト｜何歳まで聞こえる？聴力年齢チェック｜シミュラボ',
  '高い周波数の「モスキート音」を再生し、何kHzまで聞こえるかで聴力の年齢の目安を測る無料テスト。加齢で聞こえにくくなる高音を、イヤホンでチェックできます。',
  'モスキート音テスト｜何歳まで聞こえる？', 'モスキート音で聴力年齢をチェック。何kHzまで聞こえる？',
  'モスキート音テスト（聴力年齢チェック）',
  '年をとると高い音から聞こえにくくなります。だんだん高くなる「モスキート音」を再生して、何kHzまで聞こえるかで聴力年齢の目安をチェック。イヤホン推奨、音量にご注意を。',
  '🦟 高い音、どこまで聞こえる？',
  'テスト開始',
  RES('聞こえた最高の音','kHz'),
  art('だんだん高くなる音を再生し、聞こえる最高周波数で聴力年齢の目安を測ります。','モスキート音と聴力年齢','人の可聴域は加齢とともに高音側から狭まり、若い人は20kHz近くまで聞こえても、年齢が上がると15kHz、12kHzと聞こえにくくなります。これを利用したのが「モスキート音」。スマホやPCのスピーカーでは高音が出にくいことがあるため、イヤホン・ヘッドホンの使用がおすすめです。',
    [('スピーカーでも測れる？','機器により高音が再生されにくいことがあります。イヤホン推奨です。'),('聞こえなくても異常？','加齢による自然な変化で、病気とは限りません。気になる場合は耳鼻科へ。'),('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')],
    warn='※あくまで簡易的な目安です。聞こえに不安がある場合は耳鼻咽喉科を受診してください。音量は小さめから始めてください。'),
  r'''  const FR=[8000,10000,12000,14000,15000,16000,17000,18000,19000,20000];
  const AGEMAP=['60歳以上','50代','40代後半','40代','30代','20代後半','24歳以下','24歳以下','10代並み','10代並み'];
  let i=0,lastHeard=-1,ctx=null,osc=null,gain=null;const game=$('game'),bar=$('bar');
  function ensure(){if(!ctx)ctx=new (window.AudioContext||window.webkitAudioContext)();}
  function stop(){try{if(osc){osc.stop();osc.disconnect();}}catch(e){}osc=null;}
  function play(f){ensure();stop();osc=ctx.createOscillator();gain=ctx.createGain();gain.gain.value=0.18;osc.type='sine';osc.frequency.value=f;osc.connect(gain);gain.connect(ctx.destination);osc.start();setTimeout(stop,2000);}
  function step(){if(i>=FR.length){end();return;}const khz=FR[i]/1000;bar.innerHTML='テスト中 <b>'+khz+'</b> kHz';
    game.innerHTML='<div class="gm-stage"><div style="font-size:40px">🔊</div><div style="font-weight:800;margin:6px 0">'+khz+' kHz の音</div><button class="gm-big-btn" id="pl">▶ 再生（2秒）</button><div class="gm-opt"><button id="yes">聞こえた</button><button id="no">聞こえない</button></div></div>';
    $('pl').addEventListener('click',()=>play(FR[i]));
    $('yes').addEventListener('click',()=>{lastHeard=i;i++;step();});
    $('no').addEventListener('click',()=>{end();});
    play(FR[i]);}
  function end(){stop();
    if(lastHeard<0){$('big').textContent='—';$('sub').textContent='8kHzが聞こえませんでした（環境・音量をご確認ください）';$('grade').textContent='🔈 イヤホンの装着・音量を確認して、もう一度お試しください。';show();return;}
    const khz=FR[lastHeard]/1000;$('big').textContent=khz;$('sub').textContent='聴力年齢の目安：'+AGEMAP[lastHeard];
    $('grade').textContent='👂 '+khz+'kHzまで聞こえました。聴力年齢の目安は「'+AGEMAP[lastHeard]+'」相当です（簡易判定）。';
    SHARE='モスキート音テスト、'+khz+'kHzまで聞こえました（聴力年齢の目安：'+AGEMAP[lastHeard]+'）🦟 あなたは？';show();}
  function calc(){i=0;lastHeard=-1;step();}
  const ag=$('again');if(ag)ag.addEventListener('click',()=>{$('resultPanel').style.display='none';calc();});
''')

# ============================================================
# 2. 反射神経テスト（反射神経 テスト 350）
# ============================================================
game('hansha-shinkei','⚡',
  '反射神経テスト｜画面が変わった瞬間にタップ！反応速度を測定｜シミュラボ',
  '画面が緑に変わった瞬間にタップして、反応速度（ミリ秒）を測る無料の反射神経テスト。5回の平均で判定。ゲームやスポーツの反応の速さチェックに。',
  '反射神経テスト｜反応速度を測定', '緑になった瞬間にタップ。反応速度を5回平均で測定。',
  '反射神経テスト',
  '画面が緑に変わったら、すぐタップ!変わるタイミングはランダム。5回の平均反応速度（ミリ秒）を測ります。早とちりは無効。さあ、何ミリ秒?',
  '⚡ 緑になったらすぐタップ',
  'スタート（5回）',
  RES('平均反応速度','ms'),
  art('画面が変わった瞬間にタップして反応速度を測るテストです。','反射神経（反応速度）とは','反応速度は、刺激を受けてから体を動かすまでの時間です。一般に視覚への単純反応は200〜250ミリ秒ほどが平均とされ、若い人やゲーマーは速い傾向。睡眠不足や疲労で遅くなります。5回の平均で、その日のコンディションもチェックできます。',
    [('平均はどれくらい？','視覚反応で200〜250ミリ秒が目安。150ミリ秒台ならかなり速いほうです。'),('早く押しすぎたら？','緑になる前のタップは「早すぎ」となり、その回はやり直しです。'),('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  r'''  let trial=0,times=[],state='idle',t0=0,to=null;const TOTAL=5;const game=$('game'),bar=$('bar');
  function fmtBar(){bar.innerHTML='第 <b>'+Math.min(trial+1,TOTAL)+'</b>/'+TOTAL+' 回';}
  function wait(){state='wait';fmtBar();
    game.innerHTML='<div class="gm-stage" id="st" style="background:#ef4444;color:#fff;cursor:pointer"><div style="font-size:22px;font-weight:900">待て…</div><div style="font-size:13px;margin-top:6px">緑になったらタップ</div></div>';
    $('st').addEventListener('click',onClick);
    to=setTimeout(()=>{state='go';t0=performance.now();const st=$('st');if(st){st.style.background='#22c55e';st.innerHTML='<div style="font-size:26px;font-weight:900">今だ！タップ</div>';}},1200+Math.random()*2800);}
  function onClick(){if(state==='wait'){clearTimeout(to);const st=$('st');if(st){st.style.background='#f59e0b';st.innerHTML='<div style="font-size:20px;font-weight:900">早すぎ！</div><div style="font-size:13px">もう一度この回をやり直し</div>';}state='early';setTimeout(wait,900);}
    else if(state==='go'){const dt=Math.round(performance.now()-t0);times.push(dt);trial++;state='show';
      game.innerHTML='<div class="gm-stage"><div style="font-size:30px;font-weight:900;color:var(--teal-d)">'+dt+' ms</div><div style="margin-top:8px">'+(trial<TOTAL?'次へ…':'計測完了')+'</div></div>';
      setTimeout(()=>{if(trial<TOTAL)wait();else end();},800);}}
  function end(){const avg=Math.round(times.reduce((a,b)=>a+b,0)/times.length);$('big').textContent=avg;$('sub').textContent='5回の平均（最速 '+Math.min(...times)+'ms）';
    let g;if(avg<=180)g='🏆 反応神経の達人！プロゲーマー級です。';else if(avg<=230)g='✨ 速い！平均以上の反応速度。';else if(avg<=300)g='🙂 平均的な反応速度です。';else g='🌱 ゆったりめ。休憩して再挑戦すると速くなるかも。';
    $('grade').textContent=g;SHARE='反射神経テスト、平均 '+avg+'ms（最速'+Math.min(...times)+'ms）でした⚡ あなたは？';show();}
  function calc(){trial=0;times=[];wait();}
  const ag=$('again');if(ag)ag.addEventListener('click',()=>{$('resultPanel').style.display='none';calc();});
''')

# ============================================================
# 3. クリック速度（クリック 速度 / 連打測定 TP33000）★★
# ============================================================
game('click-cps','🖱️',
  'クリック連打速度テスト（CPS）｜10秒で何回クリックできる？｜シミュラボ',
  '10秒間で何回クリック（タップ）できるかを測り、1秒あたりのクリック数（CPS）を判定する無料の連打速度テスト。マウス連打・タップ速度のチェックに。',
  'クリック連打速度テスト（CPS）｜10秒で何回？', '10秒の連打数とCPSを測定。あなたの連打速度は？',
  'クリック連打速度テスト（CPS）',
  '10秒間でどれだけ連打できる?1秒あたりのクリック数（CPS）を測定します。マウスでもタップでもOK。最初のクリックで計測スタート！',
  '🖱️ 10秒間ひたすら連打！',
  'スタート',
  RES('CPS（1秒あたり）','回/秒'),
  art('10秒間の連打数から1秒あたりのクリック数（CPS）を測るテストです。','CPS（クリック・パー・セカンド）とは','CPSは1秒あたりのクリック回数で、連打速度の指標です。一般的な人で6〜8CPSほど、速い人は10CPS超。マウスのボタン、タップの仕方、指の使い方（ジッタークリックなど）で変わります。ゲームの連打要素のトレーニングにも。',
    [('平均はどれくらい？','6〜8CPSが一般的。10を超えるとかなり速いほうです。'),('スマホでもできる？','はい。画面タップで測定できます。'),('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  r'''  let clicks=0,started=false,t0=0,to=null;const game=$('game'),bar=$('bar');
  function fmtBar(){bar.innerHTML='クリック <b>'+clicks+'</b> 回';}
  function panel(label,sub){game.innerHTML='<div class="gm-stage" id="pad" style="cursor:pointer;background:#ecfeff"><div style="font-size:30px;font-weight:900;color:var(--teal-d)">'+label+'</div><div style="margin-top:6px;color:var(--ink-2)">'+sub+'</div></div>';$('pad').addEventListener('click',hit);}
  function hit(){if(!started){started=true;clicks=0;t0=performance.now();to=setTimeout(end,10000);}clicks++;fmtBar();
    const left=Math.max(0,(10000-(performance.now()-t0))/1000).toFixed(1);
    const pad=$('pad');if(pad)pad.firstChild.textContent=clicks;}
  function end(){started=false;clearTimeout(to);const cps=Math.round(clicks/10*100)/100;$('big').textContent=cps;$('sub').textContent='10秒で '+clicks+' 回';
    let g;if(cps>=10)g='🏆 連打マスター！驚異のスピード。';else if(cps>=8)g='✨ 速い！平均以上の連打力。';else if(cps>=6)g='🙂 平均的な連打速度です。';else g='🌱 これから。指の使い方を工夫すると伸びます！';
    $('grade').textContent=g;SHARE='クリック連打速度テスト、'+cps+'CPS（10秒で'+clicks+'回）でした🖱️ あなたは？';show();}
  function calc(){clicks=0;started=false;fmtBar();panel('0','ここを連打（最初のクリックで計測開始）');}
  const ag=$('again');if(ag)ag.addEventListener('click',()=>{$('resultPanel').style.display='none';calc();});
''')

# ============================================================
# 4. 視力テスト（視力 テスト 70/KD2/TP38000）★★ ランドルト環
# ============================================================
game('shiryoku-test','👁️',
  '視力テスト｜ランドルト環の切れ目はどっち？簡易視力チェック｜シミュラボ',
  'ランドルト環（C字）の切れ目の向きを答える、画面でできる簡易視力テスト。だんだん小さくなる輪で、どこまで見えるかをチェック。目の疲れのセルフチェックに。',
  '視力テスト｜ランドルト環の切れ目はどっち？', '画面でできる簡易視力チェック。Cの切れ目を当てよう。',
  '視力テスト（ランドルト環）',
  '「C」のような輪（ランドルト環）の切れ目はどっち?だんだん小さくなる輪で、どこまで見分けられるかチェック。あくまで簡易的な目安です。画面から約30〜40cm離れて挑戦を。',
  '👁️ Cの切れ目の向きを当てよう',
  'スタート',
  RES('見分けられた最小サイズ','レベル'),
  art('ランドルト環（C字）の切れ目の向きを当てる簡易視力テストです。','ランドルト環と視力','視力検査でおなじみの「C」のマークがランドルト環。切れ目の向きを見分けられる小ささで視力を測ります。本ツールは画面サイズや距離で結果が変わるため、正確な検査ではなく「目安・遊び」です。スマホやPCの長時間使用で目が疲れているときのセルフチェックにどうぞ。',
    [('正確な視力が分かる？','いいえ。画面・距離で変わるため、あくまで目安です。正確には眼科で検査を。'),('見えにくいと感じたら？','疲れ目のほか、視力低下の可能性も。気になる場合は眼科へ。'),('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')],
    warn='※画面の大きさ・明るさ・見る距離で結果が変わります。正確な視力測定ではありません。'),
  r'''  const DIRS=[['上','rotate(-90deg)'],['右','rotate(0deg)'],['下','rotate(90deg)'],['左','rotate(180deg)']];
  let size=120,level=0,miss=0;const game=$('game'),bar=$('bar');let cur=0;
  function fmtBar(){bar.innerHTML='レベル <b>'+level+'</b>　／　ミス '+miss+'/2';}
  function ask(){fmtBar();cur=Math.floor(Math.random()*4);
    game.innerHTML='<div class="gm-stage"><div class="landolt" style="font-size:'+size+'px;transform:'+DIRS[cur][1]+'">C</div><div style="margin-top:10px;color:var(--ink-2);font-size:13px">切れ目はどっち？</div><div class="gm-opt"><button data-d="0">上</button><button data-d="3">左</button><button data-d="1">右</button><button data-d="2">下</button></div></div>';
    game.querySelectorAll('.gm-opt button').forEach(b=>b.addEventListener('click',()=>{
      if(+b.dataset.d===cur){level++;size=Math.max(8,Math.round(size*0.82));ask();}
      else{miss++;if(miss>=2){end();}else{ask();}}}));}
  function end(){$('big').textContent=level;$('sub').textContent='切れ目を見分けられた段階数（小さいほど高得点）';
    let g;if(level>=12)g='🦅 タカの目級！とてもよく見えています。';else if(level>=8)g='✨ 良好。はっきり見えています。';else if(level>=5)g='🙂 平均的です。';else g='🌱 お疲れ目かも。休憩や、気になれば眼科を。';
    $('grade').textContent=g;SHARE='視力テスト（ランドルト環）、レベル'+level+'まで見分けられました👁️ あなたは？';show();}
  function calc(){size=120;level=0;miss=0;ask();}
  const ag=$('again');if(ag)ag.addEventListener('click',()=>{$('resultPanel').style.display='none';calc();});
''')

# ============================================================
# 5. 色覚・色彩識別テスト（色覚 テスト 200/KD41/TP15000）
# ============================================================
game('shikikaku-test','🎨',
  '色の識別テスト｜1つだけ違う色のタイルを探せ｜シミュラボ',
  '並んだタイルの中から、1つだけ微妙に色が違うものを探す無料の色彩識別テスト。だんだん色の差が小さくなり、どこまで見分けられるかで色の識別力をチェック。',
  '色の識別テスト｜1つだけ違う色を探せ', '微妙に色が違うタイルを探す色彩識別テスト。何段階まで？',
  '色の識別テスト（色彩感度チェック）',
  '同じ色に見えるタイルの中に、1つだけ微妙に違う色が。それはどれ?進むほど色の差が小さくなります。あなたの色を見分ける力をチェック！',
  '🎨 1つだけ違う色をタップ',
  'スタート',
  RES('見分けられた段階','レベル'),
  art('1つだけ微妙に色が違うタイルを探す色彩識別テストです。','色を見分ける力','色の細かな違いを見分ける力には個人差があり、ディスプレイの設定や明るさにも左右されます。本ツールは医学的な色覚検査ではなく、色彩感度の「遊び・目安」です。デザインや画像編集が好きな方は高得点を出しやすいかもしれません。',
    [('色覚異常が分かる？','いいえ。医学的な検査ではありません。正確には専門の検査を受けてください。'),('画面で結果が変わる？','はい。明るさ・色設定・環境光で変わります。あくまで目安です。'),('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')],
    warn='※医学的な色覚検査ではありません。画面設定・環境光で結果が変わります。'),
  r'''  let level=0,diff=60,miss=0;const game=$('game'),bar=$('bar');let odd=0,size=4;
  function fmtBar(){bar.innerHTML='レベル <b>'+level+'</b>　／　ミス '+miss+'/2';}
  function ask(){fmtBar();size=Math.min(3+Math.floor(level/3),6);const n=size*size;odd=Math.floor(Math.random()*n);
    const baseH=Math.floor(Math.random()*360),baseS=55,baseL=60;
    const oddL=baseL+(Math.random()<0.5?-1:1)*Math.max(2,diff/10);
    let h='<div style="display:grid;gap:5px;grid-template-columns:repeat('+size+',1fr);max-width:300px;margin:0 auto">';
    for(let i=0;i<n;i++){const c=i===odd?('hsl('+baseH+','+baseS+'%,'+oddL+'%)'):('hsl('+baseH+','+baseS+'%,'+baseL+'%)');
      h+='<button data-i="'+i+'" style="aspect-ratio:1;border:none;border-radius:8px;background:'+c+';cursor:pointer"></button>';}
    h+='</div>';game.innerHTML='<div class="gm-stage" style="padding:14px">'+h+'</div>';
    game.querySelectorAll('button[data-i]').forEach(b=>b.addEventListener('click',()=>{
      if(+b.dataset.i===odd){level++;diff=Math.max(3,diff*0.82);ask();}
      else{miss++;if(miss>=2)end();else ask();}}));}
  function end(){$('big').textContent=level;$('sub').textContent='色の差を見分けられた段階数';
    let g;if(level>=12)g='🎨 達人級の色彩感度！';else if(level>=8)g='✨ 良好。色の違いに敏感です。';else if(level>=5)g='🙂 平均的です。';else g='🌱 これから。明るい環境で再挑戦を！';
    $('grade').textContent=g;SHARE='色の識別テスト、レベル'+level+'まで見分けられました🎨 あなたは？';show();}
  function calc(){level=0;diff=60;miss=0;ask();}
  const ag=$('again');if(ag)ag.addEventListener('click',()=>{$('resultPanel').style.display='none';calc();});
''')

# ============================================================
# 6. IQテスト風（iq テスト 10000/KD46/TP33000）
# ============================================================
game('iq-test','🧠',
  'IQテスト（簡易版）｜10問であなたの論理思考力をチェック｜シミュラボ',
  '数列・法則・論理の10問で、論理的思考力の目安をスコア化する無料の簡易IQテスト。あくまでエンタメ版で、正式な知能検査ではありません。気軽に頭の体操を。',
  'IQテスト（簡易版）｜10問で論理思考力チェック', '数列・法則の10問で論理思考力をスコア化。エンタメ版。',
  'IQテスト（簡易版）',
  '数列や法則を見抜く10問で、論理的思考力の目安をチェック!※これはエンタメの簡易版で、正式な知能検査（IQ）ではありません。気軽な頭の体操としてどうぞ。',
  '🧠 法則を見抜こう（全10問）',
  'スタート（10問）',
  RES('スコアの目安','pt'),
  art('数列・法則・論理の問題で論理的思考力の目安をスコア化します。','IQ（知能指数）について','IQは本来、専門家が標準化された検査で測るものです。本ツールはそれを模した簡易的なクイズで、結果は「論理パズルの正解数」をスコアに換算したエンタメです。実際のIQとは異なります。頭の体操・気分転換としてお楽しみください。',
    [('正式なIQが分かる？','いいえ。エンタメの簡易版です。正式なIQは専門機関の検査が必要です。'),('難しすぎる？','法則を落ち着いて探すのがコツ。直感より一手ずつ確かめて。'),('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')],
    warn='※エンタメの簡易テストです。正式な知能検査（IQ）ではありません。'),
  r'''  const Q=[
   ['2, 4, 6, 8, ?',['9','10','12','14'],1],
   ['1, 2, 4, 8, 16, ?',['20','24','32','30'],2],
   ['仲間はずれはどれ？',['4','8','12','15'],3],
   ['1, 4, 9, 16, ?',['20','25','24','21'],1],
   ['1, 1, 2, 3, 5, 8, ?',['11','12','13','15'],2],
   ['AはBより速い。CはAより速い。一番速いのは？',['A','B','C','同じ'],2],
   ['2, 6, 18, 54, ?',['108','162','150','216'],1],
   ['仲間はずれはどれ？',['イヌ','ネコ','トリ','クルマ'],3],
   ['3, 6, 11, 18, ?',['25','27','29','24'],1],
   ['100, 96, 88, 72, ?',['40','48','56','64'],0]];
  let order=[],idx=0,score=0;const game=$('game'),bar=$('bar');
  function shuffle(a){a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
  function fmtBar(){bar.innerHTML='第 <b>'+Math.min(idx+1,10)+'</b>/10 問　／　正解 <b>'+score+'</b>';}
  function ask(){if(idx>=10){end();return;}fmtBar();const q=Q[order[idx]];
    let h='<div class="gm-stage"><div style="font-size:22px;font-weight:800;margin-bottom:10px">'+q[0]+'</div><div class="gm-opt" style="flex-direction:column;max-width:260px;margin:0 auto">';
    q[1].forEach((o,k)=>{h+='<button data-k="'+k+'" style="width:100%">'+o+'</button>';});h+='</div></div>';
    game.innerHTML=h;
    game.querySelectorAll('button[data-k]').forEach(b=>b.addEventListener('click',()=>{
      if(+b.dataset.k===q[2])score++;idx++;fmtBar();ask();}));}
  function end(){const iq=80+score*5;$('big').textContent=iq;$('sub').textContent='10問中 '+score+'問 正解（目安スコア）';
    let g;if(score>=9)g='🏆 論理思考が抜群！冴えています。';else if(score>=7)g='✨ 平均以上の論理力です。';else if(score>=5)g='🙂 平均的です。';else g='🌱 これから。法則を一手ずつ確かめると伸びます！';
    $('grade').textContent=g+'（※エンタメの目安スコアです）';SHARE='IQテスト（簡易版）、目安スコア '+iq+'（10問中'+score+'問正解）でした🧠 あなたは？';show();}
  function calc(){order=shuffle(Q.map((_,i)=>i));idx=0;score=0;ask();}
  const ag=$('again');if(ag)ag.addEventListener('click',()=>{$('resultPanel').style.display='none';calc();});
''')

# ============================================================
# 7. タイピング速度テスト（タイピング 速度 400/TP8000）
# ============================================================
game('typing-sokudo','⌨️',
  'タイピング速度テスト｜表示された文をどれだけ速く打てる？｜シミュラボ',
  '表示された英文をそのまま入力し、1分あたりの文字数（CPM）と正確性を測る無料のタイピング速度テスト。キーボード入力の速さチェック・練習に。',
  'タイピング速度テスト｜CPM・正確性を測定', '表示文を入力してタイピング速度（CPM）と正確性を測定。',
  'タイピング速度テスト',
  '表示された文をそのまま入力!打ち終わるまでの速さから、1分あたりの文字数（CPM）と正確性を測ります。最初の入力で計測スタート。',
  '⌨️ 表示された文を速く正確に入力',
  'スタート',
  RES('タイピング速度','文字/分'),
  art('表示された文を入力し、1分あたりの文字数と正確性を測るテストです。','タイピング速度（CPM）とは','CPMは1分あたりに打てる文字数で、タイピングの速さの指標です。本テストは英文で測定します。速さだけでなく「正確性」も大切で、ミスが多いと実用速度は下がります。毎日少しずつ練習すると、見ずに打つ「タッチタイピング」が身につきます。',
    [('日本語じゃないの？','本テストは入力環境に左右されにくい英文で測定します。'),('速い目安は？','英文で250CPM（約50WPM）を超えると速いほうです。'),('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  r'''  const TEXTS=['the quick brown fox jumps over the lazy dog','practice makes perfect every single day','typing fast is a useful everyday skill','a smooth sea never made a skilled sailor','simple steps lead to big results over time'];
  let target='',t0=0,started=false;const game=$('game'),bar=$('bar');
  function fmtBar(){bar.innerHTML=started?'計測中…':'入力を始めると計測開始';}
  function render(){target=TEXTS[Math.floor(Math.random()*TEXTS.length)];started=false;fmtBar();
    game.innerHTML='<div class="gm-stage" style="align-items:stretch"><div style="font-size:18px;font-weight:700;letter-spacing:.5px;margin-bottom:10px;color:var(--ink)">'+target+'</div><textarea id="ta" rows="3" autocomplete="off" autocapitalize="off" spellcheck="false" style="width:100%;font-size:16px;padding:10px;border:1.5px solid var(--line);border-radius:10px" placeholder="ここに入力…"></textarea></div>';
    const ta=$('ta');ta.focus();
    ta.addEventListener('input',()=>{if(!started){started=true;t0=performance.now();fmtBar();}
      if(ta.value.length>=target.length){finish(ta.value);}});}
  function finish(typed){const sec=(performance.now()-t0)/1000;const n=target.length;
    let correct=0;for(let i=0;i<n;i++){if(typed[i]===target[i])correct++;}
    const acc=Math.round(correct/n*100);const cpm=Math.round(n/sec*60);
    $('big').textContent=cpm;$('sub').textContent=sec.toFixed(1)+'秒・正確性 '+acc+'%';
    let g;if(cpm>=250&&acc>=95)g='🏆 タッチタイピング達人！速くて正確。';else if(cpm>=180)g='✨ 速い！平均以上のタイピング。';else if(cpm>=110)g='🙂 平均的な速さです。';else g='🌱 これから。毎日の練習で必ず速くなります！';
    $('grade').textContent=g;SHARE='タイピング速度テスト、'+cpm+'文字/分・正確性'+acc+'%でした⌨️ あなたは？';show();}
  function calc(){render();}
  const ag=$('again');if(ag)ag.addEventListener('click',()=>{$('resultPanel').style.display='none';calc();});
''')

# ============================================================
# 8. リズム感テスト（タップのタイミング精度）
# ============================================================
game('rhythm-test','🥁',
  'リズム感テスト｜ビートに合わせてタップ！タイミング精度を測定｜シミュラボ',
  '一定のビートに合わせてタップし、どれだけ正確なタイミングで叩けるかを測る無料のリズム感テスト。平均のズレ（ミリ秒）でリズム感をチェック。音楽好きに。',
  'リズム感テスト｜タイミング精度を測定', 'ビートに合わせてタップ。平均のズレでリズム感を判定。',
  'リズム感テスト',
  '一定のリズムで鳴るビートに合わせてタップ!どれだけ正確なタイミングで叩けるか、平均のズレ（ミリ秒）を測ります。音を出して挑戦してね。',
  '🥁 ビートに合わせてタップ',
  'スタート',
  RES('平均のズレ','ms'),
  art('一定のビートに合わせてタップし、タイミングの正確さを測るテストです。','リズム感（タイミング精度）','リズム感は、一定の間隔を体で正確に刻む力です。音楽・ダンス・スポーツのほか、歩行や作業のリズムにも関わります。ビートからのズレ（誤差）が小さいほどリズム感が良いといえます。カウントの後、本番のビートでタップしてください。',
    [('ズレの目安は？','平均50ミリ秒以内ならかなり正確。100ミリ秒以内で良好です。'),('音が出ない','端末の音量・マナーモードをご確認ください。'),('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  r'''  const BPM=100,INT=60000/BPM,COUNT=4,BEATS=8;
  let ctx=null,beatTimes=[],errs=[],started=false,startAt=0;const game=$('game'),bar=$('bar');
  function ensure(){if(!ctx)ctx=new (window.AudioContext||window.webkitAudioContext)();}
  function click(t,hi){ensure();const o=ctx.createOscillator(),g=ctx.createGain();o.frequency.value=hi?1200:800;g.gain.value=0.001;o.connect(g);g.connect(ctx.destination);const now=ctx.currentTime+t/1000;o.start(now);g.gain.setValueAtTime(0.25,now);g.gain.exponentialRampToValueAtTime(0.001,now+0.05);o.stop(now+0.06);}
  function run(){errs=[];beatTimes=[];started=false;ensure();
    game.innerHTML='<div class="gm-stage" id="pad" style="cursor:pointer;background:#ecfeff"><div id="msg" style="font-size:22px;font-weight:900;color:var(--teal-d)">カウント…</div><div style="margin-top:6px;color:var(--ink-2);font-size:13px">本番の合図でタップ</div></div>';
    $('pad').addEventListener('click',onTap);
    const base=performance.now();
    // count-in (4) then BEATS本番
    for(let i=0;i<COUNT;i++){click(i*INT,false);}
    for(let i=0;i<BEATS;i++){const t=(COUNT+i)*INT;beatTimes.push(base+t);click(t,true);}
    // 本番開始メッセージ
    setTimeout(()=>{const m=$('msg');if(m)m.textContent='タップ！';started=true;},COUNT*INT-60);
    setTimeout(end,(COUNT+BEATS+1)*INT);}
  function onTap(){if(!started)return;const now=performance.now();
    let best=1e9;beatTimes.forEach(bt=>{const d=Math.abs(now-bt);if(d<best)best=d;});
    if(best<INT/2){errs.push(best);const m=$('msg');if(m)m.textContent='ナイス！('+errs.length+')';}}
  function end(){if(errs.length===0){$('big').textContent='—';$('sub').textContent='タップが取れませんでした';$('grade').textContent='🔈 音を出して、合図に合わせてタップしてみてください。';show();return;}
    const avg=Math.round(errs.reduce((a,b)=>a+b,0)/errs.length);$('big').textContent=avg;$('sub').textContent=errs.length+'回のタップの平均ズレ';
    let g;if(avg<=40)g='🏆 完璧なリズム感！メトロノーム級。';else if(avg<=70)g='✨ 良好なリズム感です。';else if(avg<=110)g='🙂 平均的なリズム感です。';else g='🌱 これから。声に出してカウントすると合わせやすいです！';
    $('grade').textContent=g;SHARE='リズム感テスト、平均ズレ '+avg+'msでした🥁 あなたは？';show();}
  function calc(){run();}
  const ag=$('again');if(ag)ag.addEventListener('click',()=>{$('resultPanel').style.display='none';calc();});
''')

# ============================================================
# 9. 瞬発反応・的当てテスト
# ============================================================
game('mato-tap','🎯',
  '的当て反応テスト｜現れた的を素早くタップ！30秒で何個？｜シミュラボ',
  'ランダムに現れる的を素早くタップして、30秒で何個倒せるかと平均反応速度を測る無料の瞬発反応テスト。動体視力・瞬発力・集中力のチェックに。',
  '的当て反応テスト｜30秒で何個タップできる？', '現れた的を素早くタップ。瞬発反応・動体視力テスト。',
  '的当て反応テスト',
  'パッと現れる的を、できるだけ速くタップ!30秒で何個倒せるか、平均反応速度とあわせて測定します。瞬発力と集中力の勝負！',
  '🎯 現れた的を素早くタップ',
  'スタート（30秒）',
  RES('倒した的の数','個'),
  art('ランダムに現れる的を素早くタップする瞬発反応テストです。','瞬発反応・動体視力','的が現れた位置を素早く捉え、正確にタップする力は、瞬発反応・動体視力・手と目の協調（ハンドアイコーディネーション）を使います。スポーツやゲームに通じる力で、集中して数をこなすほどスコアが伸びます。平均反応速度も一緒にチェックできます。',
    [('スコアの目安は？','30秒で30個前後が一つの目安。速い人は40個超を狙えます。'),('スマホでもできる？','はい。画面タップで遊べます。'),('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  r'''  let hits=0,times=[],appearAt=0,to=null,remain=30,running=false;const game=$('game'),bar=$('bar');
  function fmtBar(){bar.innerHTML='のこり <b>'+remain+'</b> 秒　／　ヒット <b>'+hits+'</b>';}
  function spawn(){const arena=$('arena');if(!arena)return;const w=arena.clientWidth-48,h=arena.clientHeight-48;
    const x=Math.random()*Math.max(0,w),y=Math.random()*Math.max(0,h);
    arena.innerHTML='<div class="gm-target" id="tg" style="left:'+x+'px;top:'+y+'px"></div>';
    appearAt=performance.now();
    $('tg').addEventListener('click',()=>{if(!running)return;times.push(performance.now()-appearAt);hits++;fmtBar();spawn();});}
  function calc(){hits=0;times=[];running=true;remain=30;
    game.innerHTML='<div class="gm-arena" id="arena"></div>';spawn();
    fmtBar();clearInterval(to);to=setInterval(()=>{remain--;fmtBar();if(remain<=0){clearInterval(to);end();}},1000);}
  function end(){running=false;const arena=$('arena');if(arena)arena.innerHTML='';
    $('big').textContent=hits;const avg=times.length?Math.round(times.reduce((a,b)=>a+b,0)/times.length):0;
    $('sub').textContent='30秒・平均反応 '+avg+'ms';
    let g;if(hits>=40)g='🏆 反応の鬼！驚異の瞬発力。';else if(hits>=30)g='✨ 速い！優れた瞬発反応。';else if(hits>=20)g='🙂 平均的です。';else g='🌱 これから。的を予測せず反応で狙うと伸びます！';
    $('grade').textContent=g;SHARE='的当て反応テスト、30秒で '+hits+'個（平均反応'+avg+'ms）でした🎯 あなたは？';show();}
  const ag=$('again');if(ag)ag.addEventListener('click',()=>{$('resultPanel').style.display='none';calc();});
''')

# ============================================================
# 10. 集中力テスト（Go/No-Go）
# ============================================================
game('gonogo-test','🚦',
  '集中力テスト（Go/No-Go）｜青はタップ・赤は我慢！｜シミュラボ',
  '青が出たらタップ、赤が出たら我慢する無料の集中力テスト（Go/No-Go課題）。正答率と、つい押してしまう「お手つき」から、集中力と衝動の抑制力をチェック。',
  '集中力テスト（Go/No-Go）｜青はタップ赤は我慢', '青はタップ・赤は我慢。集中力と抑制力をチェック。',
  '集中力テスト（Go/No-Go）',
  '青いマルが出たらすぐタップ、赤いマルが出たら我慢!つい押してしまう「お手つき」をどれだけ抑えられるか。集中力と衝動の抑制力を測るテストです。',
  '🚦 青はタップ／赤は我慢',
  'スタート（20回）',
  RES('集中力スコア','点'),
  art('青はタップ・赤は我慢する集中力テスト（Go/No-Go課題）です。','Go/No-Go課題と抑制力','Go/No-Go課題は、「反応すべき時に反応し、すべきでない時に我慢する」力＝注意と衝動の抑制を測る心理課題です。赤（No-Go）でつい押してしまう「お手つき」が多いほど、衝動性が高め。青（Go）の見逃しは不注意の指標。集中して取り組みましょう。',
    [('スコアはどう決まる？','青への正解＋赤を我慢できた回数から、お手つきを引いて算出します。'),('難しい？','テンポよく出るので、集中力が続くかが勝負です。'),('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  r'''  const TOTAL=20;let i=0,go=0,nogoOK=0,falseAlarm=0,miss=0,curGo=false,answered=false,to=null;const game=$('game'),bar=$('bar');
  function fmtBar(){bar.innerHTML='第 <b>'+Math.min(i+1,TOTAL)+'</b>/'+TOTAL+'　／　お手つき <b>'+falseAlarm+'</b>';}
  function blank(cb){game.innerHTML='<div class="gm-stage"><div style="font-size:30px;color:var(--ink-2)">+</div></div>';setTimeout(cb,400+Math.random()*500);}
  function trial(){if(i>=TOTAL){end();return;}fmtBar();answered=false;curGo=Math.random()<0.65;
    const color=curGo?'#3b82f6':'#ef4444';
    game.innerHTML='<div class="gm-stage" id="pad" style="cursor:pointer"><div style="width:90px;height:90px;border-radius:50%;background:'+color+'"></div><div style="margin-top:8px;color:var(--ink-2);font-size:13px">'+(curGo?'青！タップ':'赤！我慢')+'</div></div>';
    $('pad').addEventListener('click',()=>{if(answered)return;answered=true;
      if(curGo){go++;}else{falseAlarm++;}fmtBar();});
    to=setTimeout(()=>{if(!answered){if(curGo)miss++;else nogoOK++;}i++;blank(trial);},1000);}
  function end(){const score=Math.max(0,go+nogoOK-falseAlarm*2-miss);$('big').textContent=score;
    $('sub').textContent='青に反応'+go+'・赤を我慢'+nogoOK+'・お手つき'+falseAlarm+'・見逃し'+miss;
    let g;if(falseAlarm<=1&&score>=16)g='🏆 鉄の集中力！抑制力が抜群です。';else if(score>=12)g='✨ 良好な集中力・抑制力です。';else if(score>=8)g='🙂 平均的です。';else g='🌱 これから。赤は「待つ」を意識すると伸びます！';
    $('grade').textContent=g;SHARE='集中力テスト（Go/No-Go）、スコア '+score+'点（お手つき'+falseAlarm+'）でした🚦 あなたは？';show();}
  function calc(){i=0;go=0;nogoOK=0;falseAlarm=0;miss=0;blank(trial);}
  const ag=$('again');if(ag)ag.addEventListener('click',()=>{$('resultPanel').style.display='none';calc();});
''')

if __name__=='__main__':
    render()
    print(f'test3 done. {len(SIMS)} sims.')
