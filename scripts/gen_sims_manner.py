# -*- coding: utf-8 -*-
"""シミュラボ：冠婚葬祭・贈り物の相場 10本（新カテゴリ slug=manner）。香典/ご祝儀/お年玉/出産祝い等の相場早見ツール群。
gen_sims_tool TPL流用（try無し）。CTAなし。

seo_internal.py / gen_images.py のauto-importに 'gen_sims_manner' を追加して使う。
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq
from gen_sims_tool import TPL, viz
from sim_quiz import make_engines
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CAT = '冠婚葬祭・贈り物'
SIMS = []
tally_quiz, num_quiz, band_quiz, add, q_article, render = make_engines(SIMS, CAT, TPL, viz)

ANIM = r'''  function anim(v){const el=$('big'),t0=performance.now();(function s(n){const p=Math.min(1,(n-t0)/700),e=1-Math.pow(1-p,3);el.textContent=Math.round(v*e).toLocaleString('ja-JP');if(p<1)requestAnimationFrame(s);})(performance.now());}'''
MNOTE = '※金額はあくまで一般的な目安です。地域の慣習やお付き合いの深さで変わります。'

RES_AMOUNT = '''      <div class="label">__LBL__</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">目安レンジ</div><div class="v accent" id="range">—</div></div>
      <div class="stat"><div class="k">ワンポイント</div><div class="v" id="note">—</div></div></div>'''
RES_TEXT = '''      <div class="label">__LBL__</div>
      <div id="emoji" style="font-size:52px;line-height:1.1;">📩</div>
      <div class="big" style="font-size:24px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="desc" style="text-align:left;margin-top:14px;">—</div>'''

# ============================================================
# 1. 香典の相場（香典 相場 35000/KD11/TP19000）★
# ============================================================
add(id='koden-souba', emoji='🕯️',
  title='香典の相場早見｜故人との関係・年代別にいくら包む？｜シミュラボ',
  desc='故人との関係と自分の年代を選ぶだけで、香典の相場の目安が分かる無料の早見ツール。金額の決め方や、避けるべき数字（4・9）のマナーも解説します。',
  ogtitle='香典の相場早見｜関係・年代別にいくら？', ogdesc='故人との関係と年代から香典の相場の目安を表示。',
  h1='香典の相場早見',
  lead='香典はいくら包めばいい?故人との関係と、ご自身の年代を選ぶだけで、香典の相場の目安を表示します。マナーのワンポイントも。',
  inputs='''    <h2>🕯️ 条件を選ぶ</h2>
    <div class="field"><label>故人との関係</label><select id="rel">
      <option value="0">自分の親</option><option value="1">兄弟・姉妹</option><option value="2">祖父母</option>
      <option value="3">おじ・おば</option><option value="4">その他の親戚</option>
      <option value="5" selected>職場（上司・同僚・部下）</option><option value="6">友人・知人とその家族</option><option value="7">ご近所・面識程度</option></select></div>
    <div class="field"><label>あなたの年代</label><select id="age"><option value="0">20代</option><option value="1" selected>30代</option><option value="2">40代以上</option></select></div>
    <button class="btn btn-primary" id="calcBtn">香典の相場を見る</button>''',
  result=RES_AMOUNT.replace('__LBL__','香典の目安（推奨額）'),
  article='''    <div class="note"><strong>香典のマナー</strong><br>金額は「4（死）」「9（苦）」を連想させる4,000円・9,000円などを避けます。新札は避け、一度折り目をつけるのが一般的です。</div>
    <h2>香典の相場の決め方</h2>
    <p>香典の金額は、故人との関係が近いほど、また自分の年齢が上がるほど高くなる傾向です。親なら5〜10万円、兄弟姉妹で3〜5万円、職場・友人関係で5,000〜1万円が一つの目安。地域や宗派、家どうしのお付き合いによっても変わります。表書きは仏式で「御霊前」「御香典」など、宗派により異なる点に注意しましょう。'''+MNOTE+'''</p>
    <h2>よくある質問</h2>'''+faq([
      ('新札はだめ？','「不幸を予期して用意していた」とされ避けるのが一般的。新札しかなければ折り目をつけます。'),
      ('避ける金額は？','4,000円・9,000円など「4」「9」を含む額は避けるのがマナーです。'),
      ('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  js=r'''  const T=[[50000,100000,50000,70000,100000,'自分の親'],[30000,50000,30000,30000,50000,'兄弟・姉妹'],[10000,30000,10000,10000,30000,'祖父母'],[10000,20000,10000,10000,20000,'おじ・おば'],[5000,10000,5000,5000,10000,'その他の親戚'],[5000,10000,5000,5000,10000,'職場の方'],[5000,10000,5000,5000,10000,'友人・知人'],[3000,5000,3000,3000,5000,'ご近所']];
  function calc(){const r=T[+sel('rel').value||0],a=+sel('age').value||0;const rec=r[2+a];
    $('sub').textContent=r[5]+'・'+sel('age').text+'の目安';
    $('range').textContent=num(r[0])+'〜'+num(r[1])+'円';
    $('note').textContent='4・9のつく額は避ける';
    SHARE=`香典の相場早見、${r[5]}（${sel('age').text}）なら約${num(rec)}円が目安でした🕯️`;show();anim(rec);}
'''+ANIM)

# ============================================================
# 2. ご祝儀の相場（ご祝儀 相場 3100/KD1/TP28000）★
# ============================================================
add(id='shukugi-souba', emoji='💌',
  title='ご祝儀の相場早見｜結婚式でいくら包む？関係・出席形態別｜シミュラボ',
  desc='新郎新婦との関係と出席形態（一人・夫婦・欠席）から、結婚式のご祝儀の相場を表示する無料の早見ツール。割り切れる偶数を避けるマナーも解説。',
  ogtitle='ご祝儀の相場早見｜結婚式でいくら包む？', ogdesc='関係と出席形態から結婚式のご祝儀の相場を表示。',
  h1='ご祝儀の相場早見',
  lead='結婚式のご祝儀、いくら包む?新郎新婦との関係と出席形態を選ぶと、相場の目安を表示します。',
  inputs='''    <h2>💌 条件を選ぶ</h2>
    <div class="field"><label>新郎新婦との関係</label><select id="rel">
      <option value="0" selected>友人</option><option value="1">兄弟・姉妹</option><option value="2">いとこ・親戚</option>
      <option value="3">甥・姪</option><option value="4">職場の同僚・部下</option><option value="5">職場の上司</option></select></div>
    <div class="field"><label>出席のかたち</label><select id="form"><option value="single" selected>一人で出席</option><option value="couple">夫婦で出席</option><option value="absent">欠席（お祝いのみ）</option></select></div>
    <button class="btn btn-primary" id="calcBtn">ご祝儀の相場を見る</button>''',
  result=RES_AMOUNT.replace('__LBL__','ご祝儀の目安'),
  article='''    <div class="note"><strong>ご祝儀のマナー</strong><br>「2」など割り切れる偶数は「別れ」を連想させ避けるのが通例（近年はペアを意味する2万円は許容も）。新札を用意し、ご祝儀袋に包みます。</div>
    <h2>ご祝儀の相場</h2>
    <p>結婚式のご祝儀は、友人・同僚で3万円が最も一般的。兄弟姉妹や甥・姪など近い親族は5万円が目安です。夫婦で出席する場合は2人分として5〜7万円ほど。欠席する場合は1万円程度のお祝いや、相当額の品物を贈るのが一般的です。地域や家の慣習で異なる場合もあります。'''+MNOTE+'''</p>
    <h2>よくある質問</h2>'''+faq([
      ('4万・2万はだめ？','4は「死」、2は「割れる」を連想。気にする方も多いので3万・5万が無難です。'),
      ('夫婦で出席なら？','2人分として5〜7万円が目安。ご祝儀袋は1つにまとめます。'),
      ('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  js=r'''  const T=[[30000,'友人'],[50000,'兄弟・姉妹'],[30000,'いとこ・親戚'],[50000,'甥・姪'],[30000,'職場の同僚・部下'],[30000,'職場の上司']];
  function calc(){const r=T[+sel('rel').value||0],f=$('form').value;let rec,lo,hi,memo;
    if(f==='couple'){rec=r[0]+20000;lo=rec;hi=rec+20000;memo='2人分・ご祝儀袋は1つに';}
    else if(f==='absent'){rec=10000;lo=5000;hi=10000;memo='品物でも可';}
    else{rec=r[0];lo=r[0];hi=r[0]+20000;memo='新札を用意';}
    $('sub').textContent=r[1]+'・'+sel('form').text;
    $('range').textContent=num(lo)+'〜'+num(hi)+'円';$('note').textContent=memo;
    SHARE=`ご祝儀の相場早見、${r[1]}・${sel('form').text}なら約${num(rec)}円が目安でした💌`;show();anim(rec);}
'''+ANIM)

# ============================================================
# 3. お年玉の相場（お年玉 相場 10000/KD1/TP14000）★
# ============================================================
add(id='otoshidama-souba', emoji='🧧',
  title='お年玉の相場早見｜年齢・学年別にいくら渡す？｜シミュラボ',
  desc='子どもの年齢・学年を選ぶだけで、お年玉の相場の目安が分かる無料の早見ツール。渡し方やポチ袋のマナーも解説します。',
  ogtitle='お年玉の相場早見｜年齢・学年別にいくら？', ogdesc='子どもの年齢・学年からお年玉の相場の目安を表示。',
  h1='お年玉の相場早見',
  lead='お年玉、いくら渡す?子どもの年齢・学年を選ぶと、お年玉の相場の目安を表示します。毎年の参考に。',
  inputs='''    <h2>🧧 子どもの年齢・学年</h2>
    <div class="field"><label>年齢・学年</label><select id="g">
      <option value="0">未就学児（0〜6歳）</option><option value="1">小学校 低学年</option><option value="2" selected>小学校 高学年</option>
      <option value="3">中学生</option><option value="4">高校生</option><option value="5">大学生・成人</option></select></div>
    <button class="btn btn-primary" id="calcBtn">お年玉の相場を見る</button>''',
  result=RES_AMOUNT.replace('__LBL__','お年玉の目安'),
  article='''    <div class="note"><strong>お年玉のマナー</strong><br>ポチ袋に入れ、お札は表が内側になるよう三つ折りに。新札を用意するのが望ましいとされます。</div>
    <h2>お年玉の相場</h2>
    <p>お年玉は年齢が上がるほど高くなるのが一般的。未就学児で500〜1,000円、小学生で1,000〜3,000円、中学生で3,000〜5,000円、高校生で5,000〜1万円が目安です。「年齢÷2×1,000円」を目安にする家庭もあります。親戚間で金額を合わせておくと、後々のトラブルを防げます。'''+MNOTE+'''</p>
    <h2>よくある質問</h2>'''+faq([
      ('赤ちゃんにもあげる？','現金よりおもちゃや絵本を贈る家庭も。あげる場合は500〜1,000円が目安です。'),
      ('新札じゃないとだめ？','マナーとしては新札が望ましいですが、必須ではありません。'),
      ('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  js=r'''  const T=[[500,1000,1000,'未就学児'],[1000,2000,1000,'小学校低学年'],[2000,3000,3000,'小学校高学年'],[3000,5000,3000,'中学生'],[5000,10000,5000,'高校生'],[10000,10000,10000,'大学生・成人']];
  function calc(){const r=T[+sel('g').value||0];
    $('sub').textContent=r[3]+'の目安';
    $('range').textContent=num(r[0])+'〜'+num(r[1])+'円';$('note').textContent='ポチ袋に新札で';
    SHARE=`お年玉の相場早見、${r[3]}なら${num(r[0])}〜${num(r[1])}円が目安でした🧧`;show();anim(r[2]);}
'''+ANIM)

# ============================================================
# 4. 出産祝いの相場（出産祝い 相場 24000/KD0/TP16000）★
# ============================================================
add(id='shussan-iwai-souba', emoji='🍼',
  title='出産祝いの相場早見｜関係別にいくら贈る？｜シミュラボ',
  desc='贈る相手との関係を選ぶだけで、出産祝いの相場の目安が分かる無料の早見ツール。贈る時期やのしのマナーも解説します。',
  ogtitle='出産祝いの相場早見｜関係別にいくら？', ogdesc='関係から出産祝いの相場の目安を表示。時期やのしも。',
  h1='出産祝いの相場早見',
  lead='出産祝い、いくら贈る?贈る相手との関係を選ぶと、相場の目安を表示します。贈る時期のマナーも。',
  inputs='''    <h2>🍼 贈る相手との関係</h2>
    <div class="field"><label>関係</label><select id="rel">
      <option value="0">兄弟・姉妹</option><option value="1">祖父母（孫へ）</option><option value="2">その他の親戚</option>
      <option value="3" selected>友人</option><option value="4">職場（同僚・上司・部下）</option><option value="5">知人・ご近所</option></select></div>
    <button class="btn btn-primary" id="calcBtn">出産祝いの相場を見る</button>''',
  result=RES_AMOUNT.replace('__LBL__','出産祝いの目安'),
  article='''    <div class="note"><strong>贈る時期</strong><br>生後7日〜1ヶ月（お宮参り頃）までに贈るのが一般的。出産前は避け、母子の体調が落ち着いてからにします。</div>
    <h2>出産祝いの相場</h2>
    <p>出産祝いは関係の近さで金額が変わります。兄弟姉妹で1〜3万円、友人で5,000〜1万円、職場関係で3,000〜1万円が目安。祖父母から孫へは1〜5万円と幅があります。現金のほか、ベビー服やおむつ、カタログギフトなど実用品も喜ばれます。お返し（出産内祝い）は、いただいた額の半分〜1/3が目安です。'''+MNOTE+'''</p>
    <h2>よくある質問</h2>'''+faq([
      ('現金と品物どっち？','どちらでもOK。複数人で贈るなら、少し高めの品物を連名にする方法もあります。'),
      ('お返しはいくら？','出産内祝いとして、いただいた額の半分〜1/3が目安です。'),
      ('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  js=r'''  const T=[[10000,30000,10000,'兄弟・姉妹'],[10000,50000,30000,'祖父母（孫へ）'],[5000,10000,10000,'その他の親戚'],[5000,10000,5000,'友人'],[3000,10000,5000,'職場の方'],[3000,5000,3000,'知人・ご近所']];
  function calc(){const r=T[+sel('rel').value||0];
    $('sub').textContent=r[3]+'への目安';
    $('range').textContent=num(r[0])+'〜'+num(r[1])+'円';$('note').textContent='生後7日〜1ヶ月に';
    SHARE=`出産祝いの相場早見、${r[3]}なら${num(r[0])}〜${num(r[1])}円が目安でした🍼`;show();anim(r[2]);}
'''+ANIM)

# ============================================================
# 5. 結婚祝いの相場（結婚祝い 相場 4700/KD0/TP11000）
# ============================================================
add(id='kekkon-iwai-souba', emoji='🎁',
  title='結婚祝いの相場早見｜出席しない場合・品物でいくら？｜シミュラボ',
  desc='相手との関係と出席の有無から、結婚祝い（お祝い金・品物）の相場の目安が分かる無料の早見ツール。出席する場合はご祝儀の考え方も案内します。',
  ogtitle='結婚祝いの相場早見｜品物・欠席ならいくら？', ogdesc='関係と出席有無から結婚祝いの相場の目安を表示。',
  h1='結婚祝いの相場早見',
  lead='結婚式に出席しないとき、結婚祝いはいくら?相手との関係と出席の有無を選ぶと、お祝い金・品物の相場を表示します。',
  inputs='''    <h2>🎁 条件を選ぶ</h2>
    <div class="field"><label>相手との関係</label><select id="rel">
      <option value="0" selected>友人</option><option value="1">兄弟・姉妹</option><option value="2">いとこ・親戚</option><option value="3">職場の同僚・部下・上司</option></select></div>
    <div class="field"><label>結婚式への出席</label><select id="att"><option value="no" selected>出席しない（招待なし含む）</option><option value="yes">出席する</option></select></div>
    <button class="btn btn-primary" id="calcBtn">結婚祝いの相場を見る</button>''',
  result=RES_AMOUNT.replace('__LBL__','結婚祝いの目安'),
  article='''    <div class="note"><strong>出席する場合</strong><br>披露宴に出席するなら、お祝いは「ご祝儀」として渡すのが基本（→ご祝儀の相場早見もどうぞ）。別途プレゼントは任意です。</div>
    <h2>結婚祝いの相場</h2>
    <p>結婚式に出席しない場合の結婚祝いは、友人で5,000〜1万円、親族で1〜3万円が目安。招待されたが欠席する場合は、ご祝儀の1/3〜半額程度＋祝電やプレゼントが丁寧です。品物ならペアグッズ・キッチン家電・カタログギフトが定番。出席する場合は、お祝いはご祝儀に含めるのが一般的です。'''+MNOTE+'''</p>
    <h2>よくある質問</h2>'''+faq([
      ('招待されたけど欠席する','ご祝儀の1/3〜半額程度のお祝い、または祝電＋プレゼントが丁寧です。'),
      ('プレゼントの定番は？','ペアグッズ、キッチン家電、カタログギフトなどが喜ばれます。'),
      ('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  js=r'''  const T=[[5000,10000,'友人'],[30000,50000,'兄弟・姉妹'],[10000,30000,'いとこ・親戚'],[5000,10000,'職場の方']];
  function calc(){const r=T[+sel('rel').value||0],att=$('att').value;let lo,hi,rec,memo;
    if(att==='yes'){lo=0;hi=0;rec=0;memo='出席時はご祝儀で（別ツール参照）';
      $('sub').textContent=r[2]+'・出席する場合';$('range').textContent='ご祝儀として包みます';$('note').textContent=memo;
      $('big').textContent='—';show();return;}
    lo=r[0];hi=r[1];rec=r[0];
    $('sub').textContent=r[2]+'・出席しない場合';$('range').textContent=num(lo)+'〜'+num(hi)+'円';$('note').textContent='品物でも可';
    SHARE=`結婚祝いの相場早見、${r[2]}（欠席）なら${num(lo)}〜${num(hi)}円が目安でした🎁`;show();anim(rec);}
'''+ANIM)

# ============================================================
# 6. 内祝い・お返しの相場（内祝い 相場 3200/KD0）半返し計算
# ============================================================
add(id='uchiiwai-keisan', emoji='🎀',
  title='内祝い・お返しの金額計算｜半返し・三分の一をすぐ計算｜シミュラボ',
  desc='いただいたお祝いの金額を入れるだけで、内祝い（お返し）の目安（半返し・1/3返し）を自動計算する無料ツール。出産・結婚・快気祝いのお返しに。',
  ogtitle='内祝い・お返しの金額計算｜半返し・1/3', ogdesc='いただいた額から内祝い（半返し・1/3返し）を自動計算。',
  h1='内祝い・お返しの金額計算',
  lead='お祝いのお返し、いくらにする?いただいた金額を入れると、内祝いの目安（半返し・三分の一返し）を計算します。',
  inputs='''    <h2>🎀 いただいた金額</h2>
    <div class="field"><label>いただいたお祝いの金額 <span class="hint">円</span></label><input type="number" id="amt" value="10000" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">お返しの目安を計算</button>''',
  result='''      <div class="label">内祝いの目安（半返し）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">三分の一返し</div><div class="v" id="third">—</div></div>
      <div class="stat"><div class="k">いただいた額</div><div class="v accent" id="orig">—</div></div></div>''',
  article='''    <div class="note"><strong>お返しの目安</strong><br>内祝い（お返し）は「半返し（1/2）」が基本。高額をいただいた場合は1/3でも失礼にあたりません。</div>
    <h2>内祝い（お返し）の金額</h2>
    <p>出産・結婚・快気祝いなどのお返し（内祝い）は、いただいた金額の<b>半分（半返し）</b>が基本です。1万円なら5,000円程度。ただし、目上の方や高額をいただいた場合は1/3程度でも問題ありません。お返しはいただいてから1ヶ月以内が目安。のしの表書きは「内祝」とし、贈り主（赤ちゃんの名前など）を記します。'''+MNOTE+'''</p>
    <h2>よくある質問</h2>'''+faq([
      ('高額をもらった時は？','半返しだと高額になりすぎる場合、1/3程度でも失礼になりません。'),
      ('お返しの時期は？','お祝いをいただいてから1ヶ月以内が目安です。'),
      ('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const a=Math.max(0,+$('amt').value||0);const half=Math.round(a/2),third=Math.round(a/3);
    $('sub').textContent=num(a)+'円のお返しの目安';
    $('third').textContent=yen(third);$('orig').textContent=yen(a);
    SHARE=`内祝い・お返し計算、${num(a)}円なら半返し約${yen(half)}（1/3で${yen(third)}）でした🎀`;show();anim(half);}
'''+ANIM)

# ============================================================
# 7. 入学・卒業祝いの相場（nyugaku）
# ============================================================
add(id='nyugaku-iwai-souba', emoji='🎓',
  title='入学祝い・卒業祝いの相場早見｜関係・学齢別にいくら？｜シミュラボ',
  desc='贈る相手との関係と学齢（小・中・高・大）から、入学祝い・卒業祝いの相場の目安が分かる無料の早見ツール。贈る時期のマナーも解説します。',
  ogtitle='入学祝い・卒業祝いの相場｜関係・学齢別', ogdesc='関係と学齢から入学・卒業祝いの相場の目安を表示。',
  h1='入学祝い・卒業祝いの相場早見',
  lead='入学祝い・卒業祝い、いくら贈る?相手との関係と進む学齢を選ぶと、相場の目安を表示します。',
  inputs='''    <h2>🎓 条件を選ぶ</h2>
    <div class="field"><label>贈る相手との関係</label><select id="rel">
      <option value="0">孫（祖父母から）</option><option value="1" selected>甥・姪</option><option value="2">その他親戚の子</option><option value="3">友人・知人の子</option></select></div>
    <div class="field"><label>進む学校</label><select id="g"><option value="1.0">小学校</option><option value="1.0" selected>中学校</option><option value="1.3">高校</option><option value="1.6">大学・専門</option></select></div>
    <button class="btn btn-primary" id="calcBtn">お祝いの相場を見る</button>''',
  result=RES_AMOUNT.replace('__LBL__','入学・卒業祝いの目安'),
  article='''    <div class="note"><strong>贈る時期</strong><br>入学祝いは入学の2〜3週間前まで、遅くとも入学式前に。卒業と入学が重なる場合は入学祝いにまとめるのが一般的です。</div>
    <h2>入学・卒業祝いの相場</h2>
    <p>金額は関係の近さと進学先で変わります。孫へは1〜3万円、甥・姪で5,000〜1万円、友人の子で3,000〜5,000円が目安。高校・大学と上がるほど高めになります。図書カードや文具・通学グッズなど実用品も人気。卒業祝いと入学祝いが続く場合は、入学祝いにまとめて贈るのが一般的です。'''+MNOTE+'''</p>
    <h2>よくある質問</h2>'''+faq([
      ('卒業と入学、両方贈る？','続く場合は入学祝いにまとめるのが一般的です。'),
      ('現金以外なら？','図書カード、文具、通学に使えるグッズなどが喜ばれます。'),
      ('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  js=r'''  const T=[[10000,30000,'孫（祖父母から）'],[5000,10000,'甥・姪'],[5000,10000,'親戚の子'],[3000,5000,'友人・知人の子']];
  function calc(){const r=T[+sel('rel').value||0],m=+sel('g').value||1;
    const lo=Math.round(r[0]*m/1000)*1000,hi=Math.round(r[1]*m/1000)*1000,rec=lo;
    $('sub').textContent=r[2]+'・'+sel('g').text+'の目安';
    $('range').textContent=num(lo)+'〜'+num(hi)+'円';$('note').textContent='入学式前までに';
    SHARE=`入学・卒業祝いの相場早見、${r[2]}・${sel('g').text}なら${num(lo)}〜${num(hi)}円が目安でした🎓`;show();anim(rec);}
'''+ANIM)

# ============================================================
# 8. 喪中の範囲・喪中はがきチェッカー（喪中 31000/KD0）text
# ============================================================
add(id='mochu-checker', emoji='🕊️',
  title='喪中の範囲チェッカー｜この続柄は喪中？喪中はがきはいつ出す？｜シミュラボ',
  desc='亡くなった方との続柄を選ぶと、喪中とするのが一般的かどうか、喪中はがきを出す時期・相手の目安が分かる無料ツール。年賀欠礼のマナーに。',
  ogtitle='喪中の範囲チェッカー｜この続柄は喪中？', ogdesc='続柄から喪中の範囲と喪中はがきの時期・相手を案内。',
  h1='喪中の範囲チェッカー',
  lead='この場合、喪中になる?亡くなった方との続柄を選ぶと、喪中とするのが一般的かどうかと、喪中はがき（年賀欠礼）のマナーを表示します。',
  inputs='''    <h2>🕊️ 亡くなった方との続柄</h2>
    <div class="field"><label>続柄</label><select id="rel">
      <option value="2">配偶者</option><option value="2">父母・配偶者の父母</option><option value="2">子</option>
      <option value="1" selected>祖父母</option><option value="1">兄弟・姉妹</option><option value="1">孫</option>
      <option value="0">おじ・おば</option><option value="0">いとこ・その他</option></select></div>
    <button class="btn btn-primary" id="calcBtn">喪中かどうか調べる</button>''',
  result=RES_TEXT.replace('__LBL__','喪中の判定とマナー'),
  article='''    <div class="note"><strong>喪中の範囲</strong><br>一般に<b>二親等以内</b>（配偶者・父母・子・祖父母・兄弟姉妹・孫）の場合に喪中とすることが多いとされます。三親等以遠は喪中としないのが通例ですが、同居や故人との関係で判断します。</div>
    <h2>喪中・年賀欠礼のマナー</h2>
    <p>喪中（年賀欠礼）とするかは、亡くなった方との続柄で判断します。配偶者・父母・子・兄弟姉妹・祖父母・孫など二親等以内が一般的な範囲。喪中はがきは、相手が年賀状の準備を始める前の<b>11月中旬〜12月初旬</b>に届くよう出します。送る相手は、例年年賀状をやり取りしている方。すでに年賀状を受け取った後で不幸があった場合は、松の内が明けてから「寒中見舞い」でお知らせします。'''+MNOTE+'''</p>
    <h2>よくある質問</h2>'''+faq([
      ('喪中の期間は？','一般に一周忌（約1年）までを喪中とすることが多いですが、明確な決まりはありません。'),
      ('喪中はがきを出しそびれたら？','年明けに「寒中見舞い」で年賀欠礼をお詫び・お知らせします。'),
      ('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const v=+sel('rel').value,name=sel('rel').text;
    let emoji,head,desc;
    if(v>=2){emoji='🕊️';head='喪中とするのが一般的です';desc='「'+name+'」は一親等にあたり、喪中（年賀欠礼）とするのが通例です。喪中はがきは相手が年賀状を準備する前の11月中旬〜12月初旬に届くように。送る相手は、例年年賀状をやり取りしている方です。';}
    else if(v===1){emoji='🕊️';head='喪中とすることが多いです';desc='「'+name+'」は二親等にあたり、喪中とするのが一般的です。ただし同居の有無や故人との関係で判断する場合もあります。喪中はがきは11月中旬〜12月初旬に届くようにしましょう。';}
    else{emoji='✉️';head='喪中としないことが多いです';desc='「'+name+'」は三親等以遠にあたり、一般には喪中としないことが多いです。ただし、同居していた・特に親しかったなどの事情があれば、ご自身の気持ちで喪中とされても構いません。';}
    $('emoji').textContent=emoji;$('big').textContent=head;$('sub').textContent=name+'の場合';$('desc').textContent='📌 '+desc;
    SHARE=`喪中の範囲チェッカー、「${name}」は『${head}』でした🕊️`;show();}
''')

# ============================================================
# 9. 寒中・暑中見舞いの時期チェッカー（寒中見舞い 時期 6600/KD0）text
# ============================================================
add(id='kanchu-mimai', emoji='📮',
  title='寒中見舞い・暑中見舞いの時期チェッカー｜いつ出す？｜シミュラボ',
  desc='寒中見舞い・暑中見舞い・残暑見舞いの「出す時期」の目安が分かる無料ツール。それぞれの期間と、過ぎてしまった場合の対応も解説します。',
  ogtitle='寒中・暑中見舞いの時期｜いつ出す？', ogdesc='寒中・暑中・残暑見舞いの出す時期の目安を表示。',
  h1='寒中・暑中見舞いの時期チェッカー',
  lead='寒中見舞い・暑中見舞い、いつ出せばいい?種類を選ぶと、出す時期の目安と注意点を表示します。',
  inputs='''    <h2>📮 どの見舞い？</h2>
    <div class="field"><label>種類</label><select id="type">
      <option value="kanchu" selected>寒中見舞い</option><option value="shochu">暑中見舞い</option><option value="zansho">残暑見舞い</option></select></div>
    <button class="btn btn-primary" id="calcBtn">出す時期を調べる</button>''',
  result=RES_TEXT.replace('__LBL__','出す時期の目安'),
  article='''    <div class="note"><strong>季節の挨拶状の時期</strong><br>寒中見舞い：松の内明け（1/8頃）〜立春（2/4頃）／暑中見舞い：梅雨明け頃〜立秋（8/7頃）／残暑見舞い：立秋（8/7頃）〜8月末頃</div>
    <h2>季節の見舞い状、出す時期</h2>
    <p>寒中見舞いは、松の内（一般に1/7まで）が明けてから立春（2/4頃）までに出します。年賀状を出しそびれた場合や、喪中の方への挨拶にも使えます。暑中見舞いは梅雨明け〜立秋（8/7頃）まで、立秋を過ぎたら「残暑見舞い」として8月末頃までに。時期を過ぎないよう、相手に届くタイミングを意識して投函しましょう。'''+MNOTE+'''</p>
    <h2>よくある質問</h2>'''+faq([
      ('年賀状を出しそびれた','松の内明け〜立春に「寒中見舞い」として出すのが丁寧です。'),
      ('暑中と残暑の境目は？','立秋（8月7日頃）が境目。立秋以降は「残暑見舞い」になります。'),
      ('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const t=$('type').value;let emoji,head,desc;
    if(t==='kanchu'){emoji='❄️';head='松の内明け（1/8頃）〜立春（2/4頃）';desc='年賀状を出しそびれたとき、喪中の方への挨拶、寒さ厳しい時期のお見舞いに使えます。立春を過ぎると「余寒見舞い」になります。';}
    else if(t==='shochu'){emoji='☀️';head='梅雨明け頃〜立秋（8/7頃）';desc='夏の盛り、相手の健康を気づかう挨拶状です。梅雨明けを待って出し、立秋（8月7日頃）を過ぎたら「残暑見舞い」に切り替えます。';}
    else{emoji='🌾';head='立秋（8/7頃）〜8月末頃';desc='立秋を過ぎてから出す夏の挨拶状です。9月に入る前、遅くとも8月末までに届くようにしましょう。';}
    $('emoji').textContent=emoji;$('big').textContent=head;$('sub').textContent=sel('type').text+'を出す時期';$('desc').textContent='📌 '+desc;
    SHARE=`${sel('type').text}の時期チェッカー、出す時期は「${head}」でした📮`;show();}
''')

# ============================================================
# 10. 長寿祝い早見（長寿祝い 4600/TP39000・還暦 年齢 TP230000）
# ============================================================
add(id='chouju-iwai', emoji='🎏',
  title='長寿祝い早見｜還暦・古希・喜寿…何歳が何のお祝い？｜シミュラボ',
  desc='年齢を入れると、還暦・古希・喜寿・傘寿・米寿・卒寿・白寿・百寿など、その年齢にあたる長寿祝いと、テーマカラー・次のお祝いが分かる無料ツール。',
  ogtitle='長寿祝い早見｜還暦・古希・喜寿は何歳？', ogdesc='年齢から長寿祝い（還暦・古希・喜寿…）と色・由来を表示。',
  h1='長寿祝い早見',
  lead='還暦・古希・喜寿…何歳が何のお祝い?年齢を入れると、その年齢にあたる長寿祝いと、テーマカラー・由来、次のお祝いを表示します。',
  inputs='''    <h2>🎏 年齢を入れる</h2>
    <div class="field"><label>年齢 <span class="hint">歳（数え年が伝統。満年齢でもOK）</span></label><input type="number" id="age" value="60" min="0" max="130" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">長寿祝いを調べる</button>''',
  result=RES_TEXT.replace('__LBL__','長寿祝い').replace('📩','🎉'),
  article='''    <div class="note"><strong>長寿祝いと数え年</strong><br>長寿祝いは伝統的に「数え年」で祝いますが、近年は満年齢で祝うことも増えています。還暦のみ満60歳（数え61歳）で祝うのが一般的です。</div>
    <h2>長寿祝いの一覧</h2>
    <p>長寿祝いには、還暦（60）・古希（70）・喜寿（77）・傘寿（80）・米寿（88）・卒寿（90）・白寿（99）・百寿（100）などがあります。それぞれにテーマカラーがあり、還暦は「赤」、古希・喜寿は「紫」、傘寿・米寿は「黄（金茶）」、白寿は「白」が定番。お祝いは、家族での食事会やテーマカラーの品物を贈るのが一般的です。数え年で祝うのが伝統ですが、満年齢でも構いません。</p>
    <h2>よくある質問</h2>'''+faq([
      ('数え年と満年齢どっち？','伝統は数え年ですが、近年は満年齢での実施も一般的。家族で揃えればOKです。'),
      ('還暦の色が赤なのは？','生まれ年の干支に還る＝赤ちゃんに還る、という意味から「赤いちゃんちゃんこ」が定番です。'),
      ('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')]),
  js=r'''  const M=[[60,'還暦（かんれき）','赤','干支が一巡し生まれ年に還る節目。赤いちゃんちゃんこでお祝い。'],[70,'古希（こき）','紫','「人生七十古来稀なり」に由来。'],[77,'喜寿（きじゅ）','紫','「喜」の草書が七十七に見えることから。'],[80,'傘寿（さんじゅ）','黄（金茶）','「傘」の略字が八十に見えることから。'],[88,'米寿（べいじゅ）','黄（金茶）','「米」の字が八十八に分かれることから。'],[90,'卒寿（そつじゅ）','紫','「卒」の略字「卆」が九十に見えることから。'],[99,'白寿（はくじゅ）','白','「百」から「一」を取ると「白」になることから。'],[100,'百寿（ももじゅ／ひゃくじゅ）','白・桃','百歳の大きな節目。紀寿とも。'],[108,'茶寿（ちゃじゅ）','—','「茶」の字が十・十・八十八に分かれ百八に。'],[111,'皇寿（こうじゅ）','—','「皇」が白(99)＋一＋十＋一で百十一に。']];
  function calc(){const a=Math.max(0,+$('age').value||0);
    let hit=null,next=null;
    for(const m of M){if(m[0]===a){hit=m;}if(m[0]>a&&!next){next=m;}}
    if(hit){$('emoji').textContent='🎉';$('big').textContent=hit[1];$('sub').textContent=a+'歳のお祝い（テーマカラー：'+hit[2]+'）';
      $('desc').textContent='📌 '+hit[3]+(next?' ／ 次は「'+next[1].split('（')[0]+'」（'+next[0]+'歳）。':'');
      SHARE=`長寿祝い早見、${a}歳は「${hit[1]}」（${hit[2]}）でした🎉`;}
    else{const prev=[...M].reverse().find(m=>m[0]<a);
      $('emoji').textContent='🎏';$('big').textContent=next?('次は「'+next[1].split('（')[0]+'」'):'—';
      $('sub').textContent=a+'歳は長寿祝いの年ではありません';
      const tailNext=next?('次の長寿祝いは「'+next[1]+'」で'+next[0]+'歳（あと'+(next[0]-a)+'年）。'):'';
      const tailPrev=prev?(' 直近は「'+prev[1].split('（')[0]+'」'+prev[0]+'歳でした。'):'';
      $('desc').textContent='📌 '+tailNext+tailPrev;
      SHARE=`長寿祝い早見、${a}歳の次のお祝いは${next?('「'+next[1].split('（')[0]+'」'+next[0]+'歳'):'—'}でした🎏`;}
    show();}
''')

if __name__=='__main__':
    render()
    print(f'manner done. {len(SIMS)} sims.')
