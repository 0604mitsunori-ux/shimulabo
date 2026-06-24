# -*- coding: utf-8 -*-
"""シミュラボ：脳トレ 第3弾10本（既存 slug=brain「脳トレ・診断テスト」に追加）。間違い探し/神経衰弱/記憶系のミニゲーム。
gen_sims_tool TPL流用（calcBtn=スタート、ゲームUIは__JS__で構築）。CTAなし。

seo_internal.py / gen_images.py のauto-importに 'gen_sims_brain3' を追加して使う。
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

# 共通スタイル（ゲーム盤）
STYLE = '''<style>
.gm-wrap{margin-top:6px}
.gm-bar{display:flex;gap:10px;justify-content:center;margin:4px 0 10px;font-weight:800;color:var(--ink-2);font-size:14px}
.gm-bar b{color:var(--teal-d);font-size:18px}
.gm-grid{display:grid;gap:6px;justify-content:center;margin:0 auto;max-width:340px}
.gm-cell{aspect-ratio:1;display:flex;align-items:center;justify-content:center;font-size:26px;border:1.5px solid var(--line);border-radius:10px;background:#fff;cursor:pointer;user-select:none;transition:transform .08s,background .15s}
.gm-cell:active{transform:scale(.92)}
.gm-cell.on{background:var(--teal);color:#fff;border-color:var(--teal)}
.gm-cell.ok{background:#dcfce7;border-color:#22c55e}
.gm-cell.ng{background:#fee2e2;border-color:#ef4444}
.gm-flash{font-size:40px;font-weight:900;letter-spacing:6px;text-align:center;padding:24px 0;color:var(--ink)}
.gm-opt{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-top:10px}
.gm-opt button{padding:10px 16px;border:1.5px solid var(--line);border-radius:10px;background:#fff;font-size:16px;font-weight:700;cursor:pointer}
.gm-opt button:hover{border-color:var(--teal)}
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

def art(intro, h2, p, faqs):
    return ('    <div class="note"><strong>これは何？</strong>：'+intro+'</div>\n    <h2>'+h2+'</h2>\n    <p>'+p+'</p>\n    <h2>よくある質問</h2>'+faq(faqs))

# ============================================================
# 1. 間違い探し（間違い探し 32000/KD6/TP30000）★★ — 仲間はずれの絵文字を探す
# ============================================================
game('machigai-sagashi','🔍',
  '間違い探しゲーム｜1つだけ違う絵文字を探せ！60秒で何問？｜シミュラボ',
  '並んだ絵文字の中から、1つだけ違うものを探してタップする無料の間違い探しゲーム。60秒で何問解けるか挑戦。脳の集中力・観察力のトレーニングに。',
  '間違い探しゲーム｜1つだけ違う絵文字を探せ', '60秒で何問解ける？1つだけ違う絵文字を探す脳トレゲーム。',
  '間違い探しゲーム',
  'たくさん並んだ絵文字の中に、1つだけ仲間はずれが。60秒でいくつ見つけられる?観察力と集中力の脳トレに。タップでスタート！',
  '🔍 1つだけ違う絵文字をタップ',
  'スタート（60秒）',
  RES('見つけた数','問'),
  art('並んだ絵文字から1つだけ違うものを探す間違い探しゲームです。','間違い探しと脳の働き','間違い探しは、視覚的な注意力・集中力・情報処理スピードを使う脳トレです。たくさんの似た情報の中から、わずかな違いを見つけ出す力は、日常の「うっかりミス」を減らすことにもつながります。レベルが上がるとマスが増えて難しくなります。スキマ時間に気軽に挑戦してみてください。',
    [('スマホでもできる？','はい。タップで操作でき、スマホ・PCどちらでも遊べます。'),('コツは？','全体をぼんやり眺めると、違う1つが「浮き上がって」見えやすくなります。'),('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  r'''  const PAIRS=[['🐶','🐺'],['🍎','🍅'],['🐱','🐯'],['😀','😄'],['🌝','🌚'],['🦊','🐺'],['🍊','🍋'],['🐸','🐢'],['⭐','🌟'],['🌷','🌹'],['🐭','🐹'],['🍇','🫐'],['🐤','🐥'],['🔵','🟣'],['🍩','🍪']];
  let score=0,timeLeft=0,timer=null;const bar=$('bar'),game=$('game');
  function fmtBar(){bar.innerHTML='のこり <b>'+timeLeft+'</b> 秒　／　正解 <b>'+score+'</b> 問';}
  function board(){const size=Math.min(3+Math.floor(score/3),7);const pr=PAIRS[Math.floor(Math.random()*PAIRS.length)];const odd=Math.floor(Math.random()*size*size);
    let h='<div class="gm-grid" style="grid-template-columns:repeat('+size+',1fr)">';
    for(let i=0;i<size*size;i++){h+='<button class="gm-cell" data-i="'+i+'">'+(i===odd?pr[1]:pr[0])+'</button>';}
    h+='</div>';game.innerHTML=h;
    game.querySelectorAll('.gm-cell').forEach(b=>b.addEventListener('click',()=>{
      if(timeLeft<=0)return;
      if(+b.dataset.i===odd){score++;fmtBar();board();}else{b.classList.add('ng');}}));}
  function end(){clearInterval(timer);timer=null;game.innerHTML='';
    $('big').textContent=score;$('sub').textContent='60秒で見つけた数';
    let g;if(score>=22)g='🏆 達人級！驚異の観察力です。';else if(score>=15)g='✨ 上級！集中力バッチリ。';else if(score>=9)g='🙂 平均的。もう一度挑戦してみよう。';else g='🌱 これから。慣れると一気に伸びます！';
    $('grade').textContent=g;SHARE='間違い探しゲーム、60秒で '+score+' 問 見つけました🔍 あなたは？';show();}
  function calc(){score=0;timeLeft=60;fmtBar();board();clearInterval(timer);
    timer=setInterval(()=>{timeLeft--;fmtBar();if(timeLeft<=0)end();},1000);}
  const ag=$('again');if(ag)ag.addEventListener('click',()=>{$('resultPanel').style.display='none';calc();});
''')

# ============================================================
# 2. 神経衰弱（神経衰弱 7200/KD1/TP8600）
# ============================================================
game('shinkei-suijaku','🃏',
  '神経衰弱ゲーム｜カードの記憶力に挑戦（無料・1人で遊べる）｜シミュラボ',
  '裏返したカードをめくってペアを揃える、定番の神経衰弱を1人で遊べる無料ゲーム。少ない手数・短い時間でクリアを目指そう。記憶力の脳トレに。',
  '神経衰弱ゲーム｜カードの記憶力に挑戦', '1人で遊べる神経衰弱。少ない手数でペアを揃えよう。',
  '神経衰弱ゲーム',
  'めくって覚えて、ペアを揃える定番の神経衰弱。1人で気軽に脳トレ。少ない手数・短い時間でのクリアを目指して！',
  '🃏 カードをめくってペアを揃えよう',
  'スタート（8ペア）',
  RES('クリアまでの手数','手'),
  art('裏返したカードのペアを揃える神経衰弱を1人用にした脳トレゲームです。','神経衰弱と記憶力','神経衰弱は、カードの位置を一時的に覚えておく「ワーキングメモリ（作業記憶）」を鍛える代表的な遊びです。一度見たカードの場所を覚え、ペアを推理する力が問われます。手数が少ないほど高得点。年齢を問わず楽しめる脳トレです。',
    [('1人でも遊べる？','はい。このゲームは1人用。自分の手数の少なさに挑戦できます。'),('コツは？','めくったカードの位置を声に出さず頭の中で復唱すると覚えやすくなります。'),('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  r'''  const FACES=['🍎','🍊','🍇','🍓','🍑','🍍','🥝','🍌'];
  let deck=[],first=null,lock=false,moves=0,matched=0;const bar=$('bar'),game=$('game');
  function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
  function fmtBar(){bar.innerHTML='手数 <b>'+moves+'</b>　／　そろった <b>'+matched+'</b>/8';}
  function render(){let h='<div class="gm-grid" style="grid-template-columns:repeat(4,1fr);max-width:300px">';
    deck.forEach((c,i)=>{h+='<button class="gm-cell" data-i="'+i+'">'+(c.open||c.done?c.f:'❓')+'</button>';});
    h+='</div>';game.innerHTML=h;
    game.querySelectorAll('.gm-cell').forEach(b=>b.addEventListener('click',()=>flip(+b.dataset.i)));}
  function flip(i){if(lock)return;const c=deck[i];if(c.open||c.done)return;c.open=true;render();
    if(first===null){first=i;}else{moves++;fmtBar();
      if(deck[first].f===c.f){deck[first].done=c.done=true;first=null;matched++;render();if(matched===8)end();}
      else{lock=true;setTimeout(()=>{deck[first].open=deck[i].open=false;first=null;lock=false;render();},700);}}}
  function end(){$('big').textContent=moves;$('sub').textContent='8ペアをそろえた手数';
    let g;if(moves<=12)g='🏆 神業！完璧な記憶力です。';else if(moves<=18)g='✨ 優秀！よく覚えていました。';else if(moves<=26)g='🙂 平均的。もう一度で縮められます。';else g='🌱 これから。位置を意識すると上達します！';
    $('grade').textContent=g;SHARE='神経衰弱ゲーム、'+moves+'手でクリアしました🃏 あなたは？';show();}
  function calc(){deck=shuffle(FACES.concat(FACES).map(f=>({f,open:false,done:false})));first=null;lock=false;moves=0;matched=0;fmtBar();render();}
  const ag=$('again');if(ag)ag.addEventListener('click',()=>{$('resultPanel').style.display='none';calc();});
''')

# ============================================================
# 3. 瞬間記憶（瞬間記憶 600/KD0 + 記憶力テスト 100/TP1000）
# ============================================================
game('shunkan-kioku','⚡',
  '瞬間記憶テスト｜一瞬で表示される数字を覚えられる？｜シミュラボ',
  '一瞬だけ表示される数字を記憶して入力する無料の瞬間記憶テスト。覚えられた桁数で記憶力を測定。だんだん桁が増えるチャレンジで脳トレ。',
  '瞬間記憶テスト｜一瞬の数字を覚えられる？', '一瞬表示される数字を記憶。何桁まで覚えられる？',
  '瞬間記憶テスト',
  '一瞬だけ光る数字、覚えられる?表示はわずか。消えた後に入力します。だんだん桁が増えていく、瞬間記憶力のテストです。',
  '⚡ 一瞬の数字を記憶しよう',
  'スタート（3桁から）',
  RES('覚えられた桁数','桁'),
  art('一瞬表示される数字を記憶して答える瞬間記憶テストです。','瞬間記憶力とは','瞬間記憶は、見たものを一瞬で頭に焼き付ける力で、ワーキングメモリの瞬発力にあたります。数字が増えるほど難しくなり、一般的な大人で7桁前後が一つの目安。速読や暗算、とっさの判断力にも関わる力です。繰り返すと少しずつ伸びていきます。',
    [('何桁が普通？','大人で7桁前後が目安。チャンク（かたまり）で覚えると伸びます。'),('表示が速すぎる？','一瞬で全体を「画像」として捉えるのがコツ。慣れると桁数が伸びます。'),('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  r'''  let digits=3,best=0,cur='';const bar=$('bar'),game=$('game');
  function fmtBar(){bar.innerHTML='レベル <b>'+digits+'</b> 桁';}
  function gen(n){let s='';for(let i=0;i<n;i++)s+=Math.floor(Math.random()*10);return s;}
  function flash(){cur=gen(digits);fmtBar();game.innerHTML='<div class="gm-flash">'+cur+'</div>';
    const show=Math.max(700,1200-digits*40);
    setTimeout(()=>{game.innerHTML='<div style="text-align:center"><input id="ans" inputmode="numeric" autocomplete="off" style="font-size:24px;letter-spacing:4px;text-align:center;width:80%;padding:10px;border:1.5px solid var(--line);border-radius:10px" placeholder="覚えた数字を入力"><div class="gm-opt"><button id="ok">こたえる</button></div></div>';
      const inp=$('ans');inp.focus();$('ok').addEventListener('click',judge);inp.addEventListener('keydown',e=>{if(e.key==='Enter')judge();});},show);}
  function judge(){const v=($('ans').value||'').trim();
    if(v===cur){best=digits;digits++;flash();}else{end();}}
  function end(){$('big').textContent=best;$('sub').textContent='連続で覚えられた最大桁数';
    let g;if(best>=9)g='🏆 驚異の記憶力！';else if(best>=7)g='✨ 平均以上。優秀です。';else if(best>=5)g='🙂 平均的な記憶力です。';else g='🌱 これから。繰り返すと伸びます！';
    $('grade').textContent=g;SHARE='瞬間記憶テスト、'+best+'桁まで覚えられました⚡ あなたは？';show();}
  function calc(){digits=3;best=0;flash();}
  const ag=$('again');if(ag)ag.addEventListener('click',()=>{$('resultPanel').style.display='none';calc();});
''')

# ============================================================
# 4. 順番記憶ゲーム（サイモン）
# ============================================================
game('simon-game','🟢',
  '順番記憶ゲーム｜光る順番を覚えて再現（サイモン）｜シミュラボ',
  '光ったパネルの順番を覚えて同じ順にタップする無料の記憶ゲーム。レベルが上がるごとに順番が1つずつ増加。記憶力・集中力の脳トレに。',
  '順番記憶ゲーム｜光る順番を覚えて再現', '光る順番を覚えて再現。何段階まで覚えられる？',
  '順番記憶ゲーム',
  '光ったパネルと同じ順番にタップ!1回ごとに順番が1つ増えていきます。どこまで覚えていられるか、記憶力に挑戦。',
  '🟢 光る順番を覚えてタップ',
  'スタート',
  RES('到達レベル','レベル'),
  art('光るパネルの順番を記憶して再現する記憶ゲーム（サイモン式）です。','順番記憶と脳','順番（系列）を覚える力は、ワーキングメモリと集中力を使います。電話番号や手順を覚える力に近く、加齢で落ちやすい一方、トレーニングで維持・向上が期待できます。レベルが上がるほど系列が長くなり、注意の持続も問われます。',
    [('何レベルが普通？','5〜6レベルが一つの目安。集中して順番を「リズム」で覚えると伸びます。'),('スマホでもできる？','はい。タップで操作できます。'),('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  r'''  const COLORS=['#22c55e','#3b82f6','#f59e0b','#ef4444'];
  let seq=[],pos=0,level=0,lock=true;const bar=$('bar'),game=$('game');
  function fmtBar(){bar.innerHTML='レベル <b>'+(level)+'</b>';}
  function render(){let h='<div class="gm-grid" style="grid-template-columns:repeat(2,1fr);max-width:240px">';
    for(let i=0;i<4;i++){h+='<button class="gm-cell" data-i="'+i+'" style="background:'+COLORS[i]+';opacity:.45;height:90px"></button>';}
    h+='</div>';game.innerHTML=h;
    game.querySelectorAll('.gm-cell').forEach(b=>b.addEventListener('click',()=>tap(+b.dataset.i)));}
  function light(i,t){const b=game.querySelector('.gm-cell[data-i="'+i+'"]');if(!b)return;b.style.opacity='1';setTimeout(()=>{b.style.opacity='.45';},t);}
  function play(){lock=true;let d=0;seq.forEach((i,k)=>{setTimeout(()=>light(i,400),d+k*650);});setTimeout(()=>{lock=false;},d+seq.length*650);}
  function next(){level++;fmtBar();pos=0;seq.push(Math.floor(Math.random()*4));play();}
  function tap(i){if(lock)return;light(i,200);if(i===seq[pos]){pos++;if(pos===seq.length){lock=true;setTimeout(next,700);}}else{end();}}
  function end(){$('big').textContent=level-1<0?0:level-1;$('sub').textContent='正しく再現できた最大レベル';
    const s=level-1;let g;if(s>=9)g='🏆 驚異の記憶力！';else if(s>=6)g='✨ 優秀な集中力です。';else if(s>=4)g='🙂 平均的です。';else g='🌱 これから。リズムで覚えると伸びます！';
    $('grade').textContent=g;SHARE='順番記憶ゲーム、レベル'+s+'まで到達しました🟢 あなたは？';show();}
  function calc(){seq=[];level=0;render();fmtBar();setTimeout(next,500);}
  const ag=$('again');if(ag)ag.addEventListener('click',()=>{$('resultPanel').style.display='none';calc();});
''')

# ============================================================
# 5. 逆唱テスト（数字を逆から）
# ============================================================
game('gyakushou-kioku','🔄',
  '逆唱テスト｜表示された数字を“逆から”言えるか？｜シミュラボ',
  '表示された数字を逆順で入力する無料の逆唱（ぎゃくしょう）テスト。前から覚えるより難しく、ワーキングメモリをより強く使います。何桁まで逆から言える？',
  '逆唱テスト｜数字を逆から言えるか？', '表示数字を逆順で入力。ワーキングメモリの脳トレ。',
  '逆唱テスト（数字の逆読み）',
  '表示された数字を、逆の順番で入力!前から覚えるより一段難しく、頭の中で並べ替える力（ワーキングメモリ）が鍛えられます。',
  '🔄 数字を逆から入力しよう',
  'スタート（3桁から）',
  RES('逆唱できた桁数','桁'),
  art('表示された数字を逆順で答える逆唱テストです。','逆唱とワーキングメモリ','逆唱は、覚えた情報を頭の中で操作・並べ替える「ワーキングメモリ」を強く使う課題です。順番通りに言う順唱より難しく、知能検査でも使われます。暗算や段取り、会話の理解にも関わる力。少しずつ桁を増やして挑戦してみましょう。',
    [('順唱との違いは？','逆から答えるため、覚えるだけでなく頭の中で並べ替える操作が加わります。'),('何桁が普通？','逆唱は順唱より2桁ほど少なく、4〜5桁が一つの目安です。'),('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  r'''  let digits=3,best=0,cur='';const bar=$('bar'),game=$('game');
  function fmtBar(){bar.innerHTML='レベル <b>'+digits+'</b> 桁（逆から）';}
  function gen(n){let s='';for(let i=0;i<n;i++)s+=Math.floor(Math.random()*10);return s;}
  function flash(){cur=gen(digits);fmtBar();game.innerHTML='<div class="gm-flash">'+cur+'</div>';
    setTimeout(()=>{game.innerHTML='<div style="text-align:center"><div style="color:var(--ink-2);font-size:13px;margin-bottom:6px">逆の順番で入力</div><input id="ans" inputmode="numeric" autocomplete="off" style="font-size:24px;letter-spacing:4px;text-align:center;width:80%;padding:10px;border:1.5px solid var(--line);border-radius:10px" placeholder="逆から入力"><div class="gm-opt"><button id="ok">こたえる</button></div></div>';
      const inp=$('ans');inp.focus();$('ok').addEventListener('click',judge);inp.addEventListener('keydown',e=>{if(e.key==='Enter')judge();});},Math.max(800,1300-digits*40));}
  function judge(){const v=($('ans').value||'').trim();const rev=cur.split('').reverse().join('');
    if(v===rev){best=digits;digits++;flash();}else{end();}}
  function end(){$('big').textContent=best;$('sub').textContent='逆から言えた最大桁数';
    let g;if(best>=7)g='🏆 驚異のワーキングメモリ！';else if(best>=5)g='✨ 平均以上。優秀です。';else if(best>=4)g='🙂 平均的です。';else g='🌱 これから。繰り返すと伸びます！';
    $('grade').textContent=g;SHARE='逆唱テスト、'+best+'桁まで逆から言えました🔄 あなたは？';show();}
  function calc(){digits=3;best=0;flash();}
  const ag=$('again');if(ag)ag.addEventListener('click',()=>{$('resultPanel').style.display='none';calc();});
''')

# ============================================================
# 6. 図形回転テスト（メンタルローテーション）
# ============================================================
game('mental-rotation','🔃',
  '図形回転テスト｜回転した文字は「同じ」か「鏡文字」か？｜シミュラボ',
  '回転して表示された文字が、元と「同じ向き」か「鏡（左右反転）」かを当てる無料のメンタルローテーション（心的回転）テスト。空間認識力の脳トレに。',
  '図形回転テスト｜同じ？それとも鏡文字？', '回転した文字が同じか鏡文字か判定。空間認識の脳トレ。',
  '図形回転テスト（メンタルローテーション）',
  '回転して表示された文字。元と「同じ」?それとも「鏡文字（左右反転）」?頭の中で回転させて見抜く、空間認識力のテストです。',
  '🔃 回転した文字を見抜こう',
  'スタート（10問）',
  RES('正解数','問'),
  art('回転した文字が同じか鏡像かを判定するメンタルローテーション課題です。','空間認識力（心的回転）とは','メンタルローテーション（心的回転）は、頭の中で図形を回転させて照合する空間認識力です。地図の読み取り、駐車、立体の理解、スポーツなどに関わります。男女差や個人差が大きい一方、練習で伸びることも知られています。素早く正確に判定できるか挑戦してみましょう。',
    [('コツは？','文字を頭の中でクルッと回してから、左右が合っているか確かめます。'),('何問正解が普通？','10問中7〜8問が一つの目安です。'),('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  r'''  const CH=['R','F','G','J','L','P','Q','E','7','2','5','B'];
  let q=0,score=0,curMirror=false;const TOTAL=10;const bar=$('bar'),game=$('game');
  function fmtBar(){bar.innerHTML='第 <b>'+Math.min(q+1,TOTAL)+'</b>/'+TOTAL+' 問　／　正解 <b>'+score+'</b>';}
  function ask(){if(q>=TOTAL){end();return;}fmtBar();
    const ch=CH[Math.floor(Math.random()*CH.length)];curMirror=Math.random()<0.5;
    const deg=[0,90,180,270][Math.floor(Math.random()*4)];
    const tf='rotate('+deg+'deg)'+(curMirror?' scaleX(-1)':'');
    game.innerHTML='<div style="text-align:center"><div style="display:inline-block;font-size:90px;font-weight:900;line-height:1;transform:'+tf+';color:var(--ink);width:120px;height:120px;display:flex;align-items:center;justify-content:center">'+ch+'</div><div class="gm-opt"><button data-m="0">同じ向き</button><button data-m="1">鏡文字</button></div></div>';
    game.querySelectorAll('.gm-opt button').forEach(b=>b.addEventListener('click',()=>{
      const ans=b.dataset.m==='1';if(ans===curMirror)score++;q++;fmtBar();ask();}));}
  function end(){$('big').textContent=score;$('sub').textContent=TOTAL+'問中の正解数';
    let g;if(score>=9)g='🏆 抜群の空間認識力！';else if(score>=7)g='✨ 平均以上。優秀です。';else if(score>=5)g='🙂 平均的です。';else g='🌱 これから。頭の中で回す練習を！';
    $('grade').textContent=g;SHARE='図形回転テスト、'+TOTAL+'問中 '+score+'問 正解でした🔃 あなたは？';show();}
  function calc(){q=0;score=0;ask();}
  const ag=$('again');if(ag)ag.addEventListener('click',()=>{$('resultPanel').style.display='none';calc();});
''')

# ============================================================
# 7. 仲間はずれ探し（語彙・分類）
# ============================================================
game('nakama-hazure','🧩',
  '仲間はずれ探しクイズ｜1つだけ違うものはどれ？｜シミュラボ',
  '4つの言葉のうち、1つだけ仲間はずれ（別の分類）のものを当てる無料クイズ。言葉の知識・分類する思考力の脳トレに。何問連続で正解できる？',
  '仲間はずれ探しクイズ｜1つだけ違うのは？', '4つの中から仲間はずれを当てる言葉の脳トレ。',
  '仲間はずれ探しクイズ',
  '4つの言葉のうち、1つだけ仲間はずれ。どれが違う?言葉の知識と「分ける力」を使う脳トレクイズ。何問連続で正解できるか挑戦！',
  '🧩 仲間はずれを1つ選ぼう',
  'スタート（10問）',
  RES('正解数','問'),
  art('4つの言葉から仲間はずれを選ぶ分類クイズです。','分類する力（カテゴリ思考）','「仲間はずれ探し」は、共通点を見つけて分類する力＝カテゴリ思考を使う脳トレです。物事の本質的な特徴を捉え、グループ分けする力は、整理整頓や問題解決、論理的思考の土台になります。語彙力も問われます。',
    [('答えが複数ありそう？','最も自然な分類で1つに決まるよう作っています。直感で選んでみてください。'),('子どもでもできる？','やさしい問題も多く、幅広い年齢で楽しめます。'),('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  r'''  const Q=[
   [['イヌ','ネコ','ウマ','サクラ'],3,'サクラだけ植物'],[['リンゴ','バナナ','ニンジン','ブドウ'],2,'ニンジンだけ野菜'],
   [['赤','青','緑','犬'],3,'犬だけ色じゃない'],[['東京','大阪','名古屋','富士山'],3,'富士山だけ都市じゃない'],
   [['カレー','ラーメン','寿司','コップ'],3,'コップだけ食べ物じゃない'],[['月','火星','地球','太陽'],3,'太陽だけ恒星'],
   [['野球','サッカー','テニス','ピアノ'],3,'ピアノだけスポーツじゃない'],[['春','夏','秋','北'],3,'北だけ季節じゃない'],
   [['鉛筆','消しゴム','定規','りんご'],3,'りんごだけ文房具じゃない'],[['1','3','5','8'],3,'8だけ偶数'],
   [['バラ','チューリップ','ひまわり','トマト'],3,'トマトだけ食べる野菜'],[['電車','バス','飛行機','机'],3,'机だけ乗り物じゃない'],
   [['金','銀','銅','水'],3,'水だけ金属じゃない'],[['ピアノ','ギター','バイオリン','絵筆'],3,'絵筆だけ楽器じゃない'],
   [['日本','フランス','アジア','ドイツ'],2,'アジアだけ国じゃない（大陸）']];
  let order=[],idx=0,score=0;const TOTAL=10;const bar=$('bar'),game=$('game');
  function shuffle(a){a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
  function fmtBar(){bar.innerHTML='第 <b>'+Math.min(idx+1,TOTAL)+'</b>/'+TOTAL+' 問　／　正解 <b>'+score+'</b>';}
  function ask(){if(idx>=TOTAL){end();return;}fmtBar();const item=Q[order[idx]];const ans=item[0][item[1]];
    // 選択肢をシャッフルし正解indexを追従
    const opts=shuffle(item[0]);
    let h='<div class="gm-opt" style="flex-direction:column;max-width:280px;margin:0 auto">';
    opts.forEach(o=>{h+='<button data-o="'+o+'" style="width:100%">'+o+'</button>';});h+='</div>';
    game.innerHTML=h;
    game.querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>{
      const ok=b.dataset.o===ans;b.classList.add(ok?'ok':'ng');if(ok)score++;
      game.querySelectorAll('button').forEach(x=>x.disabled=true);
      setTimeout(()=>{idx++;fmtBar();ask();},420);}));}
  function end(){$('big').textContent=score;$('sub').textContent=TOTAL+'問中の正解数';
    let g;if(score>=9)g='🏆 語彙も分類も完璧！';else if(score>=7)g='✨ 優秀な分類力です。';else if(score>=5)g='🙂 平均的です。';else g='🌱 これから。共通点を探す練習を！';
    $('grade').textContent=g;SHARE='仲間はずれ探しクイズ、'+TOTAL+'問中 '+score+'問 正解でした🧩 あなたは？';show();}
  function calc(){order=shuffle(Q.map((_,i)=>i)).slice(0,TOTAL);idx=0;score=0;ask();}
  const ag=$('again');if(ag)ag.addEventListener('click',()=>{$('resultPanel').style.display='none';calc();});
''')

# ============================================================
# 8. 位置記憶テスト（コルシ）
# ============================================================
game('ichi-kioku','🟦',
  '位置記憶テスト｜光ったマスの場所を覚えて再現｜シミュラボ',
  '光ったマスの位置を覚えて同じ場所をタップする無料の位置記憶テスト（コルシ式）。覚えるマスが1つずつ増えていく、視空間ワーキングメモリの脳トレ。',
  '位置記憶テスト｜光ったマスを覚えて再現', '光るマスの位置を記憶して再現。視空間記憶の脳トレ。',
  '位置記憶テスト',
  '一瞬光るマスの場所を覚えて、同じところをタップ!覚えるマスが少しずつ増えていきます。場所を覚える「視空間ワーキングメモリ」のテストです。',
  '🟦 光ったマスの場所を覚えよう',
  'スタート',
  RES('到達レベル','レベル'),
  art('光ったマスの位置を記憶して再現する位置記憶テスト（コルシブロック式）です。','視空間ワーキングメモリ','位置を覚える力は「視空間ワーキングメモリ」と呼ばれ、地図や駐車、片付けの場所記憶などに関わります。数字や言葉の記憶とは別系統で、加齢の影響も受けます。光る数が増えるほど難しくなります。集中して場所を焼き付けましょう。',
    [('何レベルが普通？','5前後が一つの目安。位置を「形」として覚えると伸びます。'),('スマホでもできる？','はい。タップで操作できます。'),('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  r'''  const N=4;let level=0,seq=[],input=[],lock=true;const bar=$('bar'),game=$('game');
  function fmtBar(){bar.innerHTML='レベル <b>'+level+'</b>（光る数 '+(level+2)+'）';}
  function render(){let h='<div class="gm-grid" style="grid-template-columns:repeat('+N+',1fr);max-width:280px">';
    for(let i=0;i<N*N;i++){h+='<button class="gm-cell" data-i="'+i+'" style="height:60px"></button>';}
    h+='</div>';game.innerHTML=h;
    game.querySelectorAll('.gm-cell').forEach(b=>b.addEventListener('click',()=>tap(+b.dataset.i)));}
  function flashSeq(){lock=true;seq.forEach((idx,k)=>{setTimeout(()=>{const b=game.querySelector('.gm-cell[data-i="'+idx+'"]');if(b){b.classList.add('on');setTimeout(()=>b.classList.remove('on'),450);}},500+k*600);});
    setTimeout(()=>{lock=false;},500+seq.length*600);}
  function next(){level++;fmtBar();input=[];const cnt=level+2;const pool=[...Array(N*N).keys()];seq=[];for(let i=0;i<cnt;i++){seq.push(pool.splice(Math.floor(Math.random()*pool.length),1)[0]);}render();flashSeq();}
  function tap(i){if(lock)return;const b=game.querySelector('.gm-cell[data-i="'+i+'"]');
    if(i===seq[input.length]){if(b){b.classList.add('ok');setTimeout(()=>b.classList.remove('ok'),250);}input.push(i);if(input.length===seq.length){lock=true;setTimeout(next,650);}}
    else{if(b)b.classList.add('ng');end();}}
  function end(){const s=level-1<0?0:level-1;$('big').textContent=s;$('sub').textContent='再現できた最大レベル';
    let g;if(s>=8)g='🏆 抜群の位置記憶！';else if(s>=5)g='✨ 優秀です。';else if(s>=3)g='🙂 平均的です。';else g='🌱 これから。形で覚えると伸びます！';
    $('grade').textContent=g;SHARE='位置記憶テスト、レベル'+s+'まで到達しました🟦 あなたは？';show();}
  function calc(){level=0;seq=[];input=[];render();fmtBar();setTimeout(next,400);}
  const ag=$('again');if(ag)ag.addEventListener('click',()=>{$('resultPanel').style.display='none';calc();});
''')

# ============================================================
# 9. 単語記憶テスト
# ============================================================
game('tango-kioku','📝',
  '単語記憶テスト｜表示された言葉をいくつ覚えられる？｜シミュラボ',
  '次々と表示される単語を覚え、後からどれが出たかを答える無料の単語記憶テスト。短期記憶の容量を測定。年齢とともに気になる「もの忘れ」のセルフチェックにも。',
  '単語記憶テスト｜いくつ覚えられる？', '表示された単語を記憶→どれが出たか判定。記憶力テスト。',
  '単語記憶テスト',
  '次々に出る単語を覚えて、あとで「出た?出てない?」を判定!短期記憶の容量を測るテストです。もの忘れのセルフチェックにも。',
  '📝 出てくる単語を覚えよう',
  'スタート（10語を記憶）',
  RES('記憶スコア','点'),
  art('表示された単語を覚え、後から再認する単語記憶テストです。','言葉の短期記憶','単語を覚えて思い出す力は、言語性の短期記憶・再認記憶です。買い物リストや人の名前を覚える力に近く、加齢で気になりやすい領域。「出た／出ていない」を正しく見分けられるかで、記憶の確かさを測ります。正答からお手つきを引いたスコアで評価します。',
    [('コツは？','単語どうしをつなげて物語にすると覚えやすくなります。'),('もの忘れが心配','遊び感覚のセルフチェックです。気になる場合は専門家にご相談を。'),('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  r'''  const WORDS=['りんご','電車','海','時計','ねこ','本','星','コーヒー','傘','鉛筆','花','山','靴','鳥','パン','橋','雪','机','鍵','船','森','雲','糸','窓','薬','旗','貝','針','畑','札'];
  let target=[],phase=0,qi=0,quiz=[],hit=0,miss=0;const bar=$('bar'),game=$('game');
  function shuffle(a){a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
  function showWords(){const all=shuffle(WORDS);target=all.slice(0,10);let i=0;bar.innerHTML='記憶中… <b>'+ (i+1) +'</b>/10';
    game.innerHTML='<div class="gm-flash" id="w"></div>';
    const tk=setInterval(()=>{if(i>=target.length){clearInterval(tk);startQuiz();return;}$('w').textContent=target[i];bar.innerHTML='記憶中… <b>'+(i+1)+'</b>/10';i++;},900);}
  function startQuiz(){const distract=shuffle(WORDS.filter(w=>!target.includes(w))).slice(0,10);
    quiz=shuffle(target.concat(distract));qi=0;hit=0;miss=0;askQ();}
  function askQ(){if(qi>=quiz.length){end();return;}const w=quiz[qi];bar.innerHTML='第 <b>'+(qi+1)+'</b>/20 問';
    game.innerHTML='<div style="text-align:center"><div class="gm-flash" style="padding:14px 0">'+w+'</div><div style="color:var(--ink-2);font-size:13px">さっき出た単語？</div><div class="gm-opt"><button data-a="1">出た</button><button data-a="0">出てない</button></div></div>';
    game.querySelectorAll('.gm-opt button').forEach(b=>b.addEventListener('click',()=>{
      const said=b.dataset.a==='1',was=target.includes(w);
      if(said&&was)hit++;else if(said&&!was)miss++;qi++;askQ();}));}
  function end(){const score=Math.max(0,hit-miss);$('big').textContent=score;$('sub').textContent='正しく「出た」と答えた数 − お手つき（'+hit+'−'+miss+'）';
    let g;if(score>=9)g='🏆 抜群の記憶力！';else if(score>=7)g='✨ 優秀です。';else if(score>=4)g='🙂 平均的です。';else g='🌱 これから。関連づけて覚えると伸びます！';
    $('grade').textContent=g;SHARE='単語記憶テスト、記憶スコア '+score+'点でした📝 あなたは？';show();}
  function calc(){showWords();}
  const ag=$('again');if(ag)ag.addEventListener('click',()=>{$('resultPanel').style.display='none';calc();});
''')

# ============================================================
# 10. 数字探し（シュルテテーブル）
# ============================================================
game('schulte','🔢',
  '数字探しゲーム（シュルテテーブル）｜1から順に速くタップ｜シミュラボ',
  'バラバラに並んだ1〜25の数字を、小さい順に素早くタップする無料の数字探しゲーム（シュルテテーブル）。動体視力・周辺視野・集中力のトレーニングに。',
  '数字探し（シュルテテーブル）｜1から順にタップ', '1〜25を順に速くタップ。集中力・周辺視野の脳トレ。',
  '数字探しゲーム（シュルテテーブル）',
  'バラバラの1〜25を、小さい順にできるだけ速くタップ!速読トレーニングでも使われる「シュルテテーブル」。集中力・周辺視野・情報処理スピードを鍛えます。',
  '🔢 1から順に素早くタップ',
  'スタート（1→25）',
  RES('クリアタイム','秒'),
  art('1〜25をバラバラに並べ、順にタップしてタイムを競う数字探し（シュルテテーブル）です。','シュルテテーブルとは','シュルテテーブルは、数字を順に探してタップするだけのシンプルな課題ですが、視野を広く使う「周辺視野」や、目を素早く動かす力、集中力を鍛えるとされ、速読トレーニングにも使われます。中央を見たまま周りの数字を捉えるのがコツ。タイムが速いほど高スコアです。',
    [('コツは？','視線を中央に置き、周辺視野で数字を探すとタイムが縮みます。'),('何秒が速い？','25個で30秒を切るとかなり速いほうです。'),('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  r'''  let next=1,startT=0,timer=null;const bar=$('bar'),game=$('game');
  function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
  function fmtBar(){const t=startT?((performance.now()-startT)/1000).toFixed(1):'0.0';bar.innerHTML='次は <b>'+Math.min(next,25)+'</b>　／　経過 '+t+'秒';}
  function render(){const nums=shuffle([...Array(25).keys()].map(n=>n+1));
    let h='<div class="gm-grid" style="grid-template-columns:repeat(5,1fr);max-width:300px">';
    nums.forEach(n=>{h+='<button class="gm-cell" data-n="'+n+'" style="height:54px;font-size:20px;font-weight:800">'+n+'</button>';});
    h+='</div>';game.innerHTML=h;
    game.querySelectorAll('.gm-cell').forEach(b=>b.addEventListener('click',()=>{
      const n=+b.dataset.n;if(n===next){b.classList.add('ok');b.disabled=true;next++;fmtBar();if(next>25)end();}else{b.classList.add('ng');setTimeout(()=>b.classList.remove('ng'),200);}}));}
  function end(){clearInterval(timer);const sec=((performance.now()-startT)/1000);$('big').textContent=sec.toFixed(1);$('sub').textContent='1〜25をタップした合計時間';
    let g;if(sec<=25)g='🏆 速読級！驚異の集中力。';else if(sec<=40)g='✨ 速い！周辺視野バッチリ。';else if(sec<=60)g='🙂 平均的です。';else g='🌱 これから。中央を見たまま探すと速くなります！';
    $('grade').textContent=g;SHARE='数字探し（シュルテテーブル）、'+sec.toFixed(1)+'秒でクリアしました🔢 あなたは？';show();}
  function calc(){next=1;render();startT=performance.now();fmtBar();clearInterval(timer);timer=setInterval(fmtBar,100);}
  const ag=$('again');if(ag)ag.addEventListener('click',()=>{$('resultPanel').style.display='none';calc();});
''')

if __name__=='__main__':
    render()
    print(f'brain3 done. {len(SIMS)} sims.')
