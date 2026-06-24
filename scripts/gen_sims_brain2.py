# -*- coding: utf-8 -*-
"""シミュラボ：脳トレ・診断テスト 第2弾 10本（既存 slug=brain カテゴリに追加）。
診断クイズ6＋ミニゲーム4。gen_sims_brain の TPL/CAT/viz を流用（try無し＝calcバインド確実）。

seo_internal.py / gen_images.py のauto-importに 'gen_sims_brain2' を追加して使う。
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq
from gen_sims_brain import TPL, CAT, viz
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SIMS=[]

QUIZ_INPUTS = '''    <h2>__QHEAD__</h2>
    <p style="color:var(--ink-2);font-size:13px;margin:-4px 0 6px;">直感で選んでOK。<span id="prog" style="font-weight:800;color:var(--teal-d);">0 / __QN__ 問</span></p>
    <div id="quiz" class="quiz"></div>
    <button class="btn btn-primary" id="calcBtn" style="margin-top:8px;">結果を見る</button>'''
QUIZ_RESULT = '''      <div class="label">__RLABEL__</div>
      <div id="emoji" style="font-size:64px;line-height:1.1;">❓</div>
      <div class="big" style="font-size:26px;"><span id="big">—</span></div>
      <div class="sub" id="score">—</div>
      <div class="alert good" id="advice" style="text-align:left;margin-top:14px;">—</div>'''
S4 = [['とても当てはまる',3],['まあ当てはまる',2],['あまり当てはまらない',1],['全く当てはまらない',0]]
def q(text): return [text, [list(o) for o in S4]]

def quiz_sim(id, emoji, title, desc, ogtitle, ogdesc, h1, lead, qhead, questions, bands, rlabel, sharetpl, article, gaugecol='#6366f1'):
    qn=len(questions); maxscore=sum(max(p for _,p in opts) for _,opts in questions)
    js = ('  const Q=' + json.dumps(questions, ensure_ascii=False) + ';\n'
          '  const BANDS=' + json.dumps(bands, ensure_ascii=False) + ';\n'
          '  const MAXS=' + str(maxscore) + ', RLABEL=' + json.dumps(rlabel, ensure_ascii=False) + ';\n'
          '  const SHARETPL=' + json.dumps(sharetpl, ensure_ascii=False) + ';\n'
          '  const GCOL=' + json.dumps(gaugecol, ensure_ascii=False) + ';\n'
          + r'''  const wrap=$('quiz');
  Q.forEach((qq,i)=>{const d=document.createElement('div');d.className='q';
    let h='<p class="qt"><b>Q'+(i+1)+'.</b> '+qq[0]+'</p><div class="opts" style="grid-template-columns:1fr;">';
    qq[1].forEach(o=>{h+='<button type="button" class="opt" data-q="'+i+'" data-p="'+o[1]+'">'+o[0]+'</button>';});
    d.innerHTML=h+'</div>';wrap.appendChild(d);});
  wrap.addEventListener('click',e=>{const b=e.target.closest('.opt');if(!b)return;const qi=b.dataset.q;
    wrap.querySelectorAll('.opt[data-q="'+qi+'"]').forEach(o=>o.classList.toggle('on',o===b));
    const p=$('prog');if(p)p.textContent=document.querySelectorAll('#quiz .opt.on').length+' / '+Q.length+' 問';});
  function calc(){const on=document.querySelectorAll('#quiz .opt.on');
    if(on.length<Q.length){alert('あと'+(Q.length-on.length)+'問！全部の質問に答えてね');
      const qs=document.querySelectorAll('#quiz .q');for(let j=0;j<qs.length;j++){if(!qs[j].querySelector('.opt.on')){qs[j].scrollIntoView({behavior:'smooth',block:'center'});break;}}return;}
    let s=0;on.forEach(b=>s+=(+b.dataset.p||0));
    let band=BANDS[BANDS.length-1];for(const bd of BANDS){if(s<=bd[0]){band=bd;break;}}
    $('emoji').textContent=band[1];$('big').textContent=band[2];$('score').textContent='スコア '+s+' / '+MAXS;
    $('advice').textContent='💡 '+band[3];
    SHARE=SHARETPL.replace('{label}',band[2]).replace('{score}',s);
    show();gauge(s,MAXS,GCOL);}
''')
    SIMS.append(dict(id=id, emoji=emoji, cat=CAT, title=title, desc=desc, ogtitle=ogtitle, ogdesc=ogdesc, h1=h1, lead=lead,
        inputs=QUIZ_INPUTS.replace('__QHEAD__',qhead).replace('__QN__',str(qn)),
        result=QUIZ_RESULT.replace('__RLABEL__',rlabel), visual=viz(), article=article, js=js))

def quiz_article(intro, faqs):
    return ('    <div class="note"><strong>これは何？</strong>：' + intro
            + '<br><b>※医療的な診断ではなく、セルフチェックのエンタメ診断です。</b></div>\n'
            '    <h2>使い方</h2>\n    <p>各質問に直感で答えるだけ。最後に「結果を見る」を押すと、スコアからあなたの傾向を判定します。</p>\n'
            '    <h2>よくある質問</h2>' + faq(faqs))

def game(**k):
    k.setdefault('visual','')
    SIMS.append(k)

# ============================================================
# 診断クイズ 6本
# ============================================================
quiz_sim('naikou-gaikou','🔵',
  '内向型・外向型診断｜あなたはどっち？12問でチェック｜シミュラボ',
  '人といて充電するか、ひとりで充電するか——内向型・外向型のどちらの傾向が強いかを12問でセルフチェックする無料診断。両方の良さも解説します（エンタメ）。',
  '内向型・外向型診断｜あなたはどっち？','12問で内向型・外向型のどちらかをセルフチェック。',
  '内向型・外向型 診断',
  '大勢といると元気が出る「外向型」？ひとりの時間で回復する「内向型」？12問であなたの傾向をセルフチェックします。どちらにも良さがあります。',
  '🔵 当てはまる度合いで答えてね',
  [q('ひとりの時間で元気が回復する'),q('大人数より少人数で話すほうが好き'),q('考えてから話すタイプだ'),
   q('にぎやかな場所が長いと疲れる'),q('深く狭い人間関係を好む'),q('初対面では聞き役になりがち'),
   q('SNSより1対1のやりとりが落ち着く'),q('予定が詰まっていると疲れる'),q('刺激より静けさを求める'),
   q('じっくり一人で作業するのが好き'),q('にぎやかな飲み会の後はぐったりする'),q('自分の内面をよく見つめる')],
  [[10,'🟠','しっかり外向型','人とのつながりで元気になるタイプ。社交が得意。'],
   [20,'🟡','ややバランス（両向型）','場面で内向・外向を使い分けられる柔軟タイプ。'],
   [28,'🔵','やや内向型','一人時間で回復するタイプ。落ち着きと深さが武器。'],
   [36,'🔷','しっかり内向型','内省的で集中力の高いタイプ。静けさを大切に。']],
  'あなたの傾向は',
  '内向型・外向型診断、私は「{label}」（スコア{score}）でした🔵 あなたは？',
  quiz_article('人とのかかわり方やエネルギーの回復のしかたから、内向型・外向型の傾向をセルフチェックします。',
    [('どちらが良いの？','優劣はありません。両方に強みがあり、多くの人は中間（両向型）です。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  gaugecol='#3b82f6')

quiz_sim('negative-shikou','🌧️',
  'ネガティブ思考度診断｜考えすぎ・マイナス思考を10問チェック｜シミュラボ',
  '物事を悪いほうに考えがちな「ネガティブ思考」の強さを10問でセルフチェックする無料診断。考えすぎのクセと、気持ちを軽くするヒントが分かります（エンタメ）。',
  'ネガティブ思考度診断｜マイナス思考をチェック','10問であなたのネガティブ思考度をセルフチェック。',
  'ネガティブ思考度診断',
  'つい物事を悪いほうに考えてしまう…その「ネガティブ思考」の強さを10問でセルフチェック。考えすぎのクセと、気持ちを軽くするヒントを表示します。',
  '🌧️ 当てはまる度合いで答えてね',
  [q('失敗を引きずって何度も思い出す'),q('良いことより悪いことに目が向く'),q('「どうせ自分なんて」と思いがち'),
   q('まだ起きていない悪い結果を想像する'),q('人の何気ない一言を深読みする'),q('うまくいっても素直に喜べない'),
   q('完璧でないと意味がないと感じる'),q('過去の後悔をよく思い出す'),q('自分を人と比べて落ち込む'),q('断られると「嫌われた」と感じる')],
  [[8,'☀️','ポジティブ寄り','前向きにとらえるのが得意。心の切り替えが上手。'],
   [16,'⛅','バランス型','良い面も悪い面も見られる現実的なタイプ。'],
   [24,'🌧️','やや考えすぎ','マイナス面に注目しがち。事実と解釈を分けると軽くなります。'],
   [30,'⛈️','かなりネガティブ寄り','考えすぎてしまう傾向。「今できること」に絞る練習を。']],
  'あなたのネガティブ思考度は',
  'ネガティブ思考度診断、私は「{label}」（スコア{score}）でした🌧️ あなたは？',
  quiz_article('物事のとらえ方から、ネガティブ思考（マイナスに考えるクセ）の強さをセルフチェックします。',
    [('ネガティブ思考は悪い？','危機を察知する力でもあります。強すぎると疲れるので、バランスが大切です。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  gaugecol='#64748b')

quiz_sim('smartphone-izon','📱',
  'スマホ依存度診断｜あなたのスマホ依存をセルフチェック（10問）｜シミュラボ',
  'スマホを手放せない「スマホ依存」の度合いを10問でセルフチェックする無料診断。依存度と、使いすぎをやわらげるヒントが分かります（エンタメ）。',
  'スマホ依存度診断｜あなたの依存度は？','10問であなたのスマホ依存度をセルフチェック。',
  'スマホ依存度診断',
  '気づけばスマホを触っている…その「スマホ依存」の度合いを10問でセルフチェック。あなたの依存度と、使いすぎをやわらげるヒントを表示します。',
  '📱 当てはまる度合いで答えてね',
  [q('朝起きてまずスマホを見る'),q('通知が来ていないか何度も確認する'),q('スマホがないと不安になる'),
   q('気づくと長時間スマホを見ている'),q('食事中や会話中も触ってしまう'),q('寝る直前までスマホを見ている'),
   q('「ちょっとだけ」が長くなる'),q('歩きスマホをすることがある'),q('SNSの反応が気になって何度も開く'),q('使う時間を減らそうとしても難しい')],
  [[8,'😌','依存ほぼなし','スマホと上手に距離を取れているタイプ。'],
   [16,'🙂','ふつう','多くの人と同じくらい。意識すればコントロール可能。'],
   [24,'📱','やや依存気味','スマホ時間が長め。通知オフや置き場所の工夫を。'],
   [30,'🔴','かなり依存気味','手放せなくなっているかも。寝室にスマホを持ち込まない等から。']],
  'あなたのスマホ依存度は',
  'スマホ依存度診断、私は「{label}」（スコア{score}）でした📱 あなたは？',
  quiz_article('スマホとの距離感から、スマホ依存の度合いをセルフチェックします。',
    [('どれくらいが使いすぎ？','明確な基準はありませんが、生活に支障が出るなら見直しのサインです。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  gaugecol='#0ea5e9')

quiz_sim('rakkan-hikan','🌤️',
  '楽観・悲観度診断｜あなたはどっち寄り？10問でチェック｜シミュラボ',
  '物事を前向きにとらえる「楽観」か、慎重に構える「悲観」か——あなたの考え方の傾向を10問でセルフチェックする無料診断（エンタメ）。',
  '楽観・悲観度診断｜あなたはどっち寄り？','10問で楽観・悲観のどちら寄りかをセルフチェック。',
  '楽観・悲観度診断',
  '「なんとかなる」の楽観派？「念のため備える」の慎重派？あなたの考え方の傾向を10問でセルフチェックします。どちらにも強みがあります。',
  '🌤️ 当てはまる度合いで答えてね',
  [q('困ったときも「なんとかなる」と思える'),q('失敗してもすぐ気持ちを切り替えられる'),q('未来は明るいと感じることが多い'),
   q('初めてのことも前向きに挑戦できる'),q('自分は運がいいほうだと思う'),q('落ち込んでも引きずりにくい'),
   q('うまくいくイメージを持ちやすい'),q('人の好意を素直に受け取れる'),q('失敗を「経験」と捉えられる'),q('明日はきっと良くなると思える')],
  [[8,'🌧️','慎重・悲観寄り','リスクに備える堅実タイプ。準備力が強み。'],
   [16,'⛅','バランス型','楽観と慎重を使い分けられる現実派。'],
   [24,'🌤️','やや楽観寄り','前向きで立ち直りが早いタイプ。'],
   [30,'☀️','しっかり楽観派','とてもポジティブ。周りを明るくする太陽タイプ。']],
  'あなたの傾向は',
  '楽観・悲観度診断、私は「{label}」（スコア{score}）でした🌤️ あなたは？',
  quiz_article('物事のとらえ方から、楽観的か悲観的かの傾向をセルフチェックします。',
    [('楽観と悲観どっちが良い？','どちらにも強みがあります。場面で使い分けられるのが理想です。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  gaugecol='#f59e0b')

quiz_sim('kyoukan-ryoku','🤝',
  '共感力診断（エンパス度）｜人の気持ちがわかる力をチェック｜シミュラボ',
  '人の気持ちを察し、寄り添う力「共感力（エンパス度）」を10問でセルフチェックする無料診断。共感力の高さと、自分を守るヒントが分かります（エンタメ）。',
  '共感力診断（エンパス度）｜気持ちがわかる力','10問であなたの共感力（エンパス度）をセルフチェック。',
  '共感力診断（エンパス度）',
  '人の気持ちにすぐ気づき、つい寄り添ってしまう…その「共感力（エンパス度）」を10問でセルフチェック。共感力の高さと、自分を守るヒントを表示します。',
  '🤝 当てはまる度合いで答えてね',
  [q('人の表情や声の変化にすぐ気づく'),q('相手の感情が自分にも伝わってくる'),q('困っている人を放っておけない'),
   q('映画や物語に強く感情移入する'),q('場の空気を敏感に読み取る'),q('人の相談によくのる'),
   q('相手の立場で考えるのが得意'),q('誰かが悲しんでいると自分もつらい'),q('人の長所に気づきやすい'),q('ニュースの被害者に心を痛める')],
  [[10,'🙂','マイペース型','感情に振り回されにくい安定タイプ。'],
   [20,'🤝','共感力ふつう〜高め','相手に寄り添える優しいタイプ。'],
   [28,'💞','共感力が高い','人の気持ちに敏感なエンパス傾向。聞き役に最適。'],
   [30,'🫧','とても高い（強エンパス）','共感力が非常に高い分、疲れやすい面も。自分の境界線を大切に。']],
  'あなたの共感力は',
  '共感力診断（エンパス度）、私は「{label}」（スコア{score}）でした🤝 あなたは？',
  quiz_article('人の気持ちへの気づきやすさから、共感力（エンパス度）をセルフチェックします。',
    [('共感力が高いと疲れる？','人の感情を受け取りやすい分、消耗することも。休む工夫が大切です。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  gaugecol='#ec4899')

quiz_sim('kichoumen-zubora','🧹',
  '几帳面・ズボラ度診断｜あなたはきっちり？おおざっぱ？｜シミュラボ',
  'きっちり整える「几帳面」か、おおらかな「ズボラ」か——あなたの生活スタイルを10問でセルフチェックする無料診断（エンタメ）。',
  '几帳面・ズボラ度診断｜きっちり？おおざっぱ？','10問であなたの几帳面・ズボラ度をセルフチェック。',
  '几帳面・ズボラ度診断',
  '何でもきっちりの「几帳面」？細かいことは気にしない「ズボラ」？あなたの生活スタイルを10問でセルフチェックします。どちらも長所です。',
  '🧹 当てはまる度合いで答えてね',
  [q('使ったものは元の場所に戻す'),q('予定はきっちり立てて動く'),q('部屋は基本的に片付いている'),
   q('細かい締め切りもきちんと守る'),q('書類やデータを整理している'),q('持ち物は決まった場所に置く'),
   q('計画通り進まないと気になる'),q('小さな汚れやズレが気になる'),q('家計簿や記録をつけている'),q('物事を最後まできっちり仕上げる')],
  [[8,'😎','おおらかズボラ派','細かいことを気にしない自由なタイプ。発想が柔軟。'],
   [16,'🙂','ほどほど','きっちりとゆるさのバランスが良いタイプ。'],
   [24,'🧹','几帳面寄り','整理整頓・計画が得意なしっかり者。'],
   [30,'✨','かなり几帳面','とてもきっちり。頼れる反面、たまには力を抜いても◎。']],
  'あなたのタイプは',
  '几帳面・ズボラ度診断、私は「{label}」（スコア{score}）でした🧹 あなたは？',
  quiz_article('生活や仕事のスタイルから、几帳面さ・ズボラさの傾向をセルフチェックします。',
    [('几帳面とズボラどっちが良い？','どちらも長所です。几帳面は信頼、ズボラは柔軟さにつながります。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  gaugecol='#10b981')

# ============================================================
# ミニゲーム 4本
# ============================================================
# 8. 暗算（フラッシュ暗算）（暗算 50000/KD0）★
game(id='ankan-flash', emoji='➕', cat=CAT,
  title='フラッシュ暗算ゲーム｜次々現れる数を足す脳トレ（無料）｜シミュラボ',
  desc='画面に次々と現れる数字を頭の中で足していく「フラッシュ暗算」の無料脳トレゲーム。正解すると数字が1つ増え、何個まで足せるか挑戦できます（エンタメ）。',
  ogtitle='フラッシュ暗算ゲーム｜数を足す脳トレ', ogdesc='次々現れる数字を暗算で足すフラッシュ暗算ゲーム。何個まで足せる？',
  h1='フラッシュ暗算ゲーム',
  lead='画面に数字が1つずつパッパッと表示されます。それを頭の中で足し算！全部消えたら合計を入力。正解すると数字が1つ増えます。あなたは何個まで足せる？',
  inputs='''    <h2>➕ 出てくる数字を足そう</h2>
    <div id="game" style="display:none;text-align:center;background:var(--bg-2,#f6f8fb);border:1px solid var(--line);border-radius:14px;padding:24px;margin-bottom:12px;">
      <div id="show" style="font-size:46px;font-weight:900;min-height:58px;">—</div>
      <input type="number" id="ans" inputmode="numeric" autocomplete="off" placeholder="合計は？" style="font-size:22px;text-align:center;width:180px;padding:10px;margin-top:12px;border:1.5px solid var(--line);border-radius:10px;display:none;">
      <div style="margin-top:12px;"><button class="btn btn-primary" id="submit" style="width:auto;padding:10px 26px;display:none;">これだ！</button></div>
      <div id="lvl" style="margin-top:10px;color:var(--ink-2);font-weight:800;font-size:13px;">—</div>
    </div>
    <button class="btn btn-primary" id="calcBtn">▶ スタート</button>''',
  result='''      <div class="label">足せた数字の個数</div>
      <div class="big"><span id="big">—</span><span class="unit">個</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">判定</div><div class="v accent" id="judge">—</div></div>
      <div class="stat"><div class="k">最後の合計</div><div class="v" id="lastsum">—</div></div></div>''',
  article='''    <div class="note"><strong>遊び方</strong><br>「スタート」を押すと数字が1つずつ表示されます。頭の中で足し算し、全部表示し終わったら合計を入力。正解すると数字が1個増えてレベルアップ！</div>
    <h2>フラッシュ暗算とは</h2>
    <p>次々に表示される数字を瞬時に足していく暗算トレーニングです。そろばん教室でもおなじみで、集中力・処理速度・ワーキングメモリを鍛えるとされています。続けるほど速く正確になります。<b>※エンタメの脳トレです。</b></p>
    <h2>よくある質問</h2>'''+faq([
      ('数字が速くて見えない','レベルが上がるほど数が増えます。最初はゆっくりなので慣れていきましょう。'),
      ('コツは？','前の合計を覚えながら足すこと。声に出さず頭の中で積み上げます。'),
      ('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  js=r'''  let count=2,sum=0,running=false,lastSum=0;
  function flash(arr,done){let i=0;function step(){if(i>=arr.length){$('show').textContent='＝？';done();return;}
    $('show').textContent='＋'+arr[i];i++;setTimeout(()=>{$('show').textContent='';setTimeout(step,160);},650);}step();}
  function round(){sum=0;const arr=[];for(let k=0;k<count;k++){const n=2+Math.floor(Math.random()*18);arr.push(n);sum+=n;}
    $('lvl').textContent='レベル '+count+'個　集中！';$('ans').style.display='none';$('submit').style.display='none';
    flash(arr,()=>{$('ans').style.display='';$('submit').style.display='';$('ans').value='';$('ans').focus();});}
  function start(){count=2;running=true;$('game').style.display='';$('resultPanel').style.display='none';$('calcBtn').textContent='▶ もう一回';round();}
  function submit(){if(!running)return;if(Math.trunc(+$('ans').value)===sum){count++;round();}else{lastSum=sum;finish();}}
  function finish(){running=false;const best=count-1;$('big').textContent=best;
    const j=best>=9?'暗算名人🧮':best>=7?'すごい！':best>=5?'平均的':'これから伸びる';
    $('sub').textContent='正しい合計は「'+lastSum+'」でした';$('judge').textContent=j;$('lastsum').textContent=lastSum;
    SHARE='フラッシュ暗算ゲーム、私は'+best+'個まで足せました➕（'+j+'）あなたは何個？';
    $('game').style.display='none';show();}
  $('submit').addEventListener('click',submit);
  $('ans').addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();submit();}});
  function calc(){start();}''')

# 9. 動体視力テスト（動体視力 テスト 300/KD0）
game(id='doutai-shiryoku', emoji='👁️', cat=CAT,
  title='動体視力テスト｜一瞬の数字を読み取れる？反応＆視力チェック｜シミュラボ',
  desc='画面に一瞬だけ表示される数字を読み取る動体視力テスト。正解するほど表示時間が短くなり、あなたの動体視力レベルを測れる無料の脳トレ（エンタメ）。',
  ogtitle='動体視力テスト｜一瞬の数字を読み取れる？', ogdesc='一瞬表示される数字を読み取る動体視力テスト。レベルはどこまで？',
  h1='動体視力テスト',
  lead='画面に数字が一瞬だけ表示されます。消える前に読み取って入力！正解するほど表示時間が短くなります。あなたの動体視力はどこまで？（エンタメテスト）',
  inputs='''    <h2>👁️ 一瞬の数字を読み取ろう</h2>
    <div id="game" style="display:none;text-align:center;background:var(--bg-2,#f6f8fb);border:1px solid var(--line);border-radius:14px;padding:24px;margin-bottom:12px;">
      <div id="show" style="font-size:44px;font-weight:900;letter-spacing:4px;min-height:56px;">—</div>
      <input type="number" id="ans" inputmode="numeric" autocomplete="off" style="font-size:22px;text-align:center;width:180px;padding:10px;margin-top:12px;border:1.5px solid var(--line);border-radius:10px;display:none;">
      <div style="margin-top:12px;"><button class="btn btn-primary" id="submit" style="width:auto;padding:10px 26px;display:none;">答える</button></div>
      <div id="lvl" style="margin-top:10px;color:var(--ink-2);font-weight:800;font-size:13px;">—</div>
    </div>
    <button class="btn btn-primary" id="calcBtn">▶ スタート</button>''',
  result='''      <div class="label">動体視力レベル</div>
      <div class="big"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">最短で読めた時間</div><div class="v accent" id="ms">—</div></div>
      <div class="stat"><div class="k">判定</div><div class="v" id="judge">—</div></div></div>''',
  article='''    <div class="note"><strong>遊び方</strong><br>「スタート」で4桁の数字が一瞬表示されます。消えたら入力。正解すると次は表示時間が短くなり、レベルアップ！</div>
    <h2>動体視力とは</h2>
    <p>動いているものや一瞬のものを正確にとらえる力を「動体視力」といいます。スポーツや運転で重要とされ、トレーニングで鍛えられるとも言われます。本テストは一瞬表示される数字を読み取れる速さでレベルを判定するエンタメです。</p>
    <h2>よくある質問</h2>'''+faq([
      ('スマホでもできる？','できます。表示が速いので集中して見てください。'),
      ('コツは？','画面の中心を見て、数字の形をパッと捉えること。'),
      ('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  js=r'''  let cur='',level=1,dur=1100,running=false,best=1100;
  function round(){cur=String(1000+Math.floor(Math.random()*9000));$('lvl').textContent='レベル '+level+'（表示 '+dur+'ms）';
    $('ans').style.display='none';$('submit').style.display='none';$('show').textContent=cur;
    setTimeout(()=>{$('show').textContent='？？？？';$('ans').style.display='';$('submit').style.display='';$('ans').value='';$('ans').focus();},dur);}
  function start(){level=1;dur=1100;running=true;$('game').style.display='';$('resultPanel').style.display='none';$('calcBtn').textContent='▶ もう一回';round();}
  function submit(){if(!running)return;if($('ans').value===cur){best=dur;level++;dur=Math.max(120,Math.round(dur*0.82));round();}else{finish();}}
  function finish(){running=false;const lv=level-1;$('big').textContent='Lv.'+lv;
    const j=best<=200?'動体視力すごい！👁️':best<=400?'かなり良い':best<=700?'平均的':'これから鍛えよう';
    $('sub').textContent='正解は「'+cur+'」でした';$('ms').textContent=best+'ms';$('judge').textContent=j;
    SHARE='動体視力テスト、私はLv.'+lv+'（最短'+best+'ms）でした👁️（'+j+'）あなたは？';
    $('game').style.display='none';show();}
  $('submit').addEventListener('click',submit);
  $('ans').addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();submit();}});
  function calc(){start();}''')

# 10. 計算力テスト（1分間）
game(id='keisanryoku', emoji='⚡', cat=CAT,
  title='計算力テスト｜1分間で何問解ける？暗算スピード測定（無料）｜シミュラボ',
  desc='1分間でかんたんな計算を何問解けるかを測る無料の計算力テスト。暗算のスピードと正確さをチェックできる脳トレです（エンタメ）。',
  ogtitle='計算力テスト｜1分間で何問解ける？', ogdesc='1分間で計算を何問解けるか測定。暗算スピードの脳トレ。',
  h1='計算力テスト（1分間）',
  lead='制限時間は1分。かんたんな計算を、できるだけ速く正確に解きましょう。答えを入力してEnter（または「次へ」）。あなたは1分で何問解ける？',
  inputs='''    <h2>⚡ 1分で何問解ける？</h2>
    <div id="game" style="display:none;text-align:center;background:var(--bg-2,#f6f8fb);border:1px solid var(--line);border-radius:14px;padding:22px;margin-bottom:12px;">
      <div id="timer" style="font-size:20px;font-weight:900;color:var(--accent);">残り 60 秒</div>
      <div id="q" style="font-size:32px;font-weight:900;margin-top:8px;">—</div>
      <input type="number" id="ans" inputmode="numeric" autocomplete="off" style="font-size:22px;text-align:center;width:140px;padding:10px;margin-top:12px;border:1.5px solid var(--line);border-radius:10px;">
      <div style="margin-top:12px;"><button class="btn btn-primary" id="submit" style="width:auto;padding:10px 26px;">次へ</button></div>
      <div id="cnt" style="margin-top:10px;color:var(--ink-2);font-weight:800;font-size:13px;">正解 0</div>
    </div>
    <button class="btn btn-primary" id="calcBtn">▶ スタート（60秒）</button>''',
  result='''      <div class="label">1分間の正解数</div>
      <div class="big"><span id="big">—</span><span class="unit">問</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">判定</div><div class="v accent" id="judge">—</div></div>
      <div class="stat"><div class="k">1問あたり</div><div class="v" id="per">—</div></div></div>''',
  article='''    <div class="note"><strong>遊び方</strong><br>「スタート」で60秒のタイマー開始。出てくる計算の答えを入力してEnter。時間内にできるだけ多く正解しよう！</div>
    <h2>計算力テストとは</h2>
    <p>単純計算を速く正確に解く力は、脳のウォーミングアップに最適とされます。毎日続けると処理速度が上がっていくのを実感できます。100マス計算のような感覚で、スキマ時間にどうぞ。<b>※エンタメの脳トレです。</b></p>
    <h2>よくある質問</h2>'''+faq([
      ('平均は何問？','個人差がありますが、20問前後が一つの目安。30問以上ならかなり速いです。'),
      ('難しさは？','足し算・引き算・かけ算のかんたんな問題です。'),
      ('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  js=r'''  let correct=0,running=false,timeLeft=60,timer=null,ansVal=0;
  function newQ(){const op=['+','-','×'][Math.floor(Math.random()*3)];let a,b;
    if(op==='×'){a=2+Math.floor(Math.random()*8);b=2+Math.floor(Math.random()*8);}
    else{a=5+Math.floor(Math.random()*45);b=2+Math.floor(Math.random()*Math.min(a-1,40));}
    ansVal=op==='+'?a+b:op==='-'?a-b:a*b;$('q').textContent=a+' '+op+' '+b+' = ?';$('ans').value='';$('ans').focus();}
  function start(){correct=0;timeLeft=60;running=true;$('game').style.display='';$('resultPanel').style.display='none';$('calcBtn').textContent='▶ もう一回';
    $('cnt').textContent='正解 0';$('timer').textContent='残り 60 秒';newQ();
    clearInterval(timer);timer=setInterval(()=>{timeLeft--;$('timer').textContent='残り '+timeLeft+' 秒';if(timeLeft<=0)finish();},1000);}
  function submit(){if(!running)return;if(Math.trunc(+$('ans').value)===ansVal){correct++;$('cnt').textContent='正解 '+correct;}newQ();}
  function finish(){running=false;clearInterval(timer);$('big').textContent=correct;
    const j=correct>=30?'計算マスター⚡':correct>=20?'速い！':correct>=12?'平均的':'これから伸びる';
    $('sub').textContent='1分間の結果';$('judge').textContent=j;$('per').textContent=correct>0?(60/correct).toFixed(1)+'秒':'—';
    SHARE='計算力テスト、私は1分間で'+correct+'問正解でした⚡（'+j+'）あなたは？';
    $('game').style.display='none';show();}
  $('submit').addEventListener('click',submit);
  $('ans').addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();submit();}});
  function calc(){start();}''')

# 11. 注意力テスト（順番タッチ）
game(id='chuuiryoku', emoji='🎯', cat=CAT,
  title='注意力テスト｜1から順にタッチ！集中力チェック（無料）｜シミュラボ',
  desc='バラバラに並んだ数字を1から順にすばやくタッチする注意力・集中力テスト。かかった時間であなたの注意力レベルを測れる無料の脳トレ（エンタメ）。',
  ogtitle='注意力テスト｜1から順にタッチ', ogdesc='散らばった数字を1から順にタッチ。かかった時間で注意力をチェック。',
  h1='注意力テスト（順番タッチ）',
  lead='バラバラに散らばった1〜15の数字を、1から順番にできるだけ速くタッチ！かかった時間で、あなたの注意力・集中力レベルを判定します。',
  inputs='''    <h2>🎯 1から順にタッチしよう</h2>
    <div id="game" style="display:none;margin-bottom:12px;">
      <div id="hud" style="text-align:center;color:var(--ink-2);font-weight:800;font-size:13px;margin-bottom:8px;">次にタッチ：<b id="nextn" style="color:var(--accent);font-size:16px;">1</b>　経過 <span id="tt">0.0</span>秒</div>
      <div id="board" style="position:relative;width:100%;height:340px;background:var(--bg-2,#f6f8fb);border:1px solid var(--line);border-radius:14px;overflow:hidden;"></div>
    </div>
    <button class="btn btn-primary" id="calcBtn">▶ スタート</button>''',
  result='''      <div class="label">クリアタイム</div>
      <div class="big"><span id="big">—</span><span class="unit">秒</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">判定</div><div class="v accent" id="judge">—</div></div>
      <div class="stat"><div class="k">お手つき</div><div class="v" id="miss">—</div></div></div>''',
  article='''    <div class="note"><strong>遊び方</strong><br>「スタート」で1〜15の数字がランダムに配置されます。1→2→3…と順番にタッチ。違う数字を押すとお手つき（＋ペナルティ）。全部押すとクリア！</div>
    <h2>注意力テストとは</h2>
    <p>散らばった数字を順番に探してタッチする課題は「トレイル・メイキング」と呼ばれ、注意力・視覚探索・処理速度を測る脳トレとして知られています。速く正確にできるほど、注意の切り替えがスムーズな証拠です。<b>※エンタメの脳トレです。</b></p>
    <h2>よくある質問</h2>'''+faq([
      ('平均タイムは？','15個で15〜25秒が一つの目安。10秒台ならかなり速いです。'),
      ('コツは？','次の数字を先に目で探しながらタッチすると速くなります。'),
      ('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  js=r'''  const N=15;let next=1,t0=0,miss=0,running=false,raf2=0;
  function layout(){const b=$('board');b.innerHTML='';const W=b.clientWidth||320,H=b.clientHeight||340,sz=46;
    const pos=[];function ok(x,y){return pos.every(p=>Math.hypot(p.x-x,p.y-y)>sz+6);}
    for(let i=1;i<=N;i++){let x,y,tries=0;do{x=8+Math.random()*(W-sz-16);y=8+Math.random()*(H-sz-16);tries++;}while(!ok(x,y)&&tries<200);pos.push({x,y});
      const el=document.createElement('button');el.className='num';el.textContent=i;el.dataset.n=i;
      el.style.cssText='position:absolute;left:'+x+'px;top:'+y+'px;width:'+sz+'px;height:'+sz+'px;border-radius:50%;border:none;font-weight:900;font-size:16px;cursor:pointer;background:linear-gradient(135deg,#0fb5c4,#6366f1);color:#fff;box-shadow:0 3px 8px rgba(0,0,0,.15);';
      b.appendChild(el);}}
  function tick(){$('tt').textContent=((performance.now()-t0)/1000).toFixed(1);if(running)raf2=requestAnimationFrame(tick);}
  function start(){next=1;miss=0;running=true;$('game').style.display='';$('resultPanel').style.display='none';$('calcBtn').textContent='▶ もう一回';$('nextn').textContent='1';layout();t0=performance.now();cancelAnimationFrame(raf2);tick();}
  $('board')&&$('board').addEventListener('click',e=>{const b=e.target.closest('.num');if(!b||!running)return;const n=+b.dataset.n;
    if(n===next){b.style.visibility='hidden';next++;$('nextn').textContent=Math.min(next,N);if(next>N)finish();}
    else{miss++;b.animate([{transform:'scale(1)'},{transform:'scale(0.8)'},{transform:'scale(1)'}],{duration:150});}});
  function finish(){running=false;cancelAnimationFrame(raf2);const sec=(performance.now()-t0)/1000+miss*1.0;
    $('big').textContent=sec.toFixed(1);const j=sec<=12?'注意力ばつぐん🎯':sec<=20?'良い集中力':sec<=30?'平均的':'落ち着いていこう';
    $('sub').textContent='1〜15を順番にタッチ';$('judge').textContent=j;$('miss').textContent=miss+'回';
    SHARE='注意力テスト、私は'+sec.toFixed(1)+'秒でクリアしました🎯（'+j+'）あなたは？';
    $('game').style.display='none';show();}
  function calc(){start();}''')

# ============================================================
def render():
    for s in SIMS:
        s.setdefault('visual','')
        d=os.path.join(ROOT,'sims',s['id']); os.makedirs(d,exist_ok=True)
        html=(TPL.replace('__TITLE__',s['title']).replace('__DESC__',s['desc'])
              .replace('__OGTITLE__',s['ogtitle']).replace('__OGDESC__',s['ogdesc'])
              .replace('__CAT__',s['cat']).replace('__H1__',s['h1']).replace('__LEAD__',s['lead'])
              .replace('__INPUTS__',s['inputs']).replace('__RESULT__',s['result'])
              .replace('__VISUAL__',s['visual']).replace('__ARTICLE__',s['article'])
              .replace('__JS__',s['js']).replace('__ID__',s['id']))
        with open(os.path.join(d,'index.html'),'w',encoding='utf-8') as f: f.write(html)
        print('created sims/'+s['id'])

if __name__=='__main__':
    render()
    print(f'brain2 done. {len(SIMS)} sims.')
