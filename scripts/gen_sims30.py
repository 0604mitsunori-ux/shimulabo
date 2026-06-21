# -*- coding: utf-8 -*-
"""シミュラボ：季節・行事カテゴリ 10本（gen_sims11のTPLを再利用）。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq, write_all

SE = '季節・行事'
SIMS = []
def add(**k): SIMS.append(k)

add(id='kotoshi-pct', cat=SE, emoji='📅',
  title='今年あと何％シミュレーター｜今年は何％終わった？｜シミュラボ',
  desc='今日の日付から、今年がどれだけ過ぎたか（進捗％）と、年末までの残り日数・週末の回数を表示するエンタメシミュレーター。',
  ogtitle='今年あと何％｜今年は何％終わった？', ogdesc='今日の日付から今年の進捗％と残り日数を表示。',
  h1='今年あと何％シミュレーター',
  lead='今年って、もう何％過ぎたんだろう？今日の日付から、1年の進捗と年末までの残り日数・週末の回数を出します。目標の振り返りや、年末ダッシュのきっかけに。',
  inputs='''    <h2>📅 ボタンを押すだけ</h2>
    <p style="color:var(--ink-2);font-size:14px;">今日の日付をもとに、今年の進捗を計算します。</p>
    <button class="btn btn-primary" id="calcBtn">今年の進捗を見る</button>''',
  result='''      <div class="label">今年が過ぎた割合</div>
      <div class="big"><span id="big">0</span><span class="unit">％</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">年末までの残り</div><div class="v accent" id="days">—</div></div>
      <div class="stat"><div class="k">残りの週末</div><div class="v" id="week">—</div></div>
      <div class="stat"><div class="k">経過日数</div><div class="v" id="passed">—</div></div></div>''',
  article='''    <h2>1年の進捗を可視化</h2>
    <div class="note"><strong>計算式</strong><br>進捗％ ＝ 経過日数 ÷ 1年の日数 ×100</div>
    <p>「もう半分過ぎた」「あと2ヶ月しかない」——数字にすると、時間の感覚がはっきりします。今年の目標の進み具合をチェックして、残りの時間を有効に使いましょう。</p>
    <h2>よくある質問</h2>'''+faq([('うるう年は？','その年の日数（365 or 366）で正確に計算します。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const T=new Date();const y=T.getFullYear();const start=new Date(y,0,1),end=new Date(y+1,0,1);
    const days=Math.ceil((end-start)/86400000);const passed=Math.floor((T-start)/86400000);
    const pct=passed/days*100, rest=days-passed;
    $('sub').textContent=`${y}年・${T.getMonth()+1}月${T.getDate()}日時点`;$('days').textContent=rest+'日';$('week').textContent=Math.floor(rest/7)+'回';$('passed').textContent=passed+'日';
    SHARE=`今年あと何％シミュ、${y}年は${pct.toFixed(1)}％終了・残り${rest}日でした📅 ラストスパート！`;show();anim($('big'),0,pct,800,1);}''')

add(id='otoshidama', cat=SE, emoji='🧧',
  title='お年玉 総額シミュレーター｜お年玉、今年はいくら配る？｜シミュラボ',
  desc='渡す子どもの人数と年齢別の相場から、お正月に配るお年玉の総額と、子どもが生涯でもらう額の目安を計算する無料シミュレーター。',
  ogtitle='お年玉 総額シミュレーター｜いくら配る？', ogdesc='人数と相場からお年玉の総額を計算。',
  h1='お年玉 総額シミュレーター',
  lead='お正月、お年玉でいくら飛んでいく？渡す人数と1人あたりの金額から総額を計算。逆に、子どもが生涯でもらうお年玉の目安も分かります。',
  inputs='''    <h2>🧧 条件を入れる</h2>
    <div class="row"><div class="field"><label>渡す人数 <span class="hint">（人）</span></label><input type="number" id="n" value="5" min="0" inputmode="numeric"></div>
    <div class="field"><label>1人あたりの平均 <span class="hint">（円）</span></label><input type="number" id="m" value="5000" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">総額を見る</button>''',
  result='''      <div class="label">今年配るお年玉の総額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">10年配ると</div><div class="v accent" id="y10">—</div></div>
      <div class="stat"><div class="k">子が0〜18歳でもらう額</div><div class="v" id="life">—</div></div>
      <div class="stat"><div class="k">1人あたり</div><div class="v" id="per">—</div></div></div>''',
  article='''    <h2>お年玉のはなし</h2>
    <div class="note"><strong>計算式</strong><br>総額 ＝ 人数 × 1人あたりの金額</div>
    <p>相場は年齢で変わり、未就学児1,000円前後、小学生1,000〜5,000円、中高生5,000〜10,000円が目安。あげる側にはなかなかの出費ですが、子どもにとっては一大イベント。お正月の風物詩ですね。</p>
    <h2>よくある質問</h2>'''+faq([('相場は？','学年×1,000円という目安もあります。家庭・地域で差があります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const n=Math.max(0,+$('n').value||0),m=Math.max(0,+$('m').value||0);const t=n*m;
    $('sub').textContent=`${n}人 × ${num(m)}円`;$('y10').textContent=yen(t*10);$('life').textContent=yen(m*18);$('per').textContent=yen(m);
    SHARE=`お年玉 総額シミュ、今年配るお年玉は${yen(t)}でした🧧 お財布が…！`;show();anim($('big'),0,t,800);}''')

add(id='bonus-haibun', cat=SE, emoji='💰',
  title='ボーナス使い道シミュレーター｜黄金比で賢く配分｜シミュラボ',
  desc='ボーナスの手取り額から、貯金・投資・自己投資・ご褒美・生活費への理想的な配分（黄金比）を提案する無料シミュレーター。',
  ogtitle='ボーナス使い道シミュレーター｜黄金比で配分', ogdesc='ボーナスを貯金・投資・ご褒美に賢く配分。',
  h1='ボーナス使い道シミュレーター',
  lead='ボーナスが入ったら、どう使う？手取り額を入れると、貯金・投資・自己投資・ご褒美・生活補填への理想的な配分を提案します。使いすぎ防止に。',
  inputs='''    <h2>💰 条件を入れる</h2>
    <div class="field"><label>ボーナスの手取り <span class="hint">（円）</span></label><input type="number" id="b" value="400000" min="0" inputmode="numeric"></div>
    <div class="field"><label>配分タイプ</label><select id="type"><option value="balance" selected>バランス型</option><option value="save">貯蓄優先型</option><option value="enjoy">満喫型</option></select></div>
    <button class="btn btn-primary" id="calcBtn">配分を見る</button>''',
  result='''      <div class="label">貯金・投資にまわす額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">貯金</div><div class="v" id="save">—</div></div>
      <div class="stat"><div class="k">投資</div><div class="v accent" id="invest">—</div></div>
      <div class="stat"><div class="k">ご褒美・自己投資</div><div class="v" id="enjoy">—</div></div></div>''',
  article='''    <h2>ボーナス配分の黄金比</h2>
    <div class="note"><strong>配分の目安</strong><br>バランス型：貯金30%・投資20%・自己投資10%・ご褒美20%・生活20%<br>使い切らず、半分は将来のために回すのがおすすめ。</div>
    <p>ボーナスは「臨時収入」だからこそ、使い道を先に決めておくのが賢い使い方。一部は貯金・投資で将来に、一部は自分へのご褒美に。メリハリをつけると満足度も上がります。</p>
    <h2>よくある質問</h2>'''+faq([('全部使ってもいい？','たまには◎。ただ半分は将来に回すと安心です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const b=Math.max(0,+$('b').value||0),t=$('type').value;
    let s,i,e; if(t==='save'){s=0.5;i=0.25;e=0.25;}else if(t==='enjoy'){s=0.2;i=0.1;e=0.7;}else{s=0.35;i=0.25;e=0.4;}
    const save=b*s,inv=b*i,enjoy=b*e, future=save+inv;
    $('sub').textContent=`${num(b)}円・${sel('type').text}`;$('save').textContent=yen(save);$('invest').textContent=yen(inv);$('enjoy').textContent=yen(enjoy);
    SHARE=`ボーナス使い道シミュ、${num(b)}円を貯金${yen(save)}・投資${yen(inv)}・ご褒美${yen(enjoy)}に配分💰`;show();anim($('big'),0,future,800);}''')

add(id='christmas-yosan', cat=SE, emoji='🎄',
  title='クリスマス予算シミュレーター｜クリスマス、いくらかかる？｜シミュラボ',
  desc='プレゼント・ケーキ・チキン・飾り付けなどから、クリスマスにかかる総額を試算する無料シミュレーター。',
  ogtitle='クリスマス予算シミュレーター｜いくらかかる？', ogdesc='プレゼント・ケーキ・ごちそうからクリスマス予算を試算。',
  h1='クリスマス予算シミュレーター',
  lead='プレゼントにケーキ、ごちそう…クリスマスって意外とかかる。項目ごとの費用から総額を試算します。早めの予算立てで賢く楽しみましょう。',
  inputs='''    <h2>🎄 条件を入れる</h2>
    <div class="row"><div class="field"><label>プレゼント1人 <span class="hint">（円）</span></label><input type="number" id="present" value="8000" min="0" inputmode="numeric"></div>
    <div class="field"><label>人数</label><input type="number" id="n" value="2" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>ケーキ <span class="hint">（円）</span></label><input type="number" id="cake" value="4000" min="0" inputmode="numeric"></div>
    <div class="field"><label>ごちそう・飲み物 <span class="hint">（円）</span></label><input type="number" id="food" value="6000" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">総額を見る</button>''',
  result='''      <div class="label">クリスマスの総予算</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">プレゼント計</div><div class="v accent" id="pv">—</div></div>
      <div class="stat"><div class="k">食事・ケーキ</div><div class="v" id="fv">—</div></div>
      <div class="stat"><div class="k">人数</div><div class="v" id="nv">—</div></div></div>''',
  article='''    <h2>クリスマス費用の内訳</h2>
    <div class="note"><strong>計算式</strong><br>総額 ＝ プレゼント × 人数 ＋ ケーキ ＋ ごちそう</div>
    <p>いちばん大きいのはプレゼント。早割やポイント還元、手作りごはんで賢く抑えつつ、思い出に残るクリスマスを。予算を決めておくと、12月の出費が読めて安心です。</p>
    <h2>よくある質問</h2>'''+faq([('外食なら？','「ごちそう」欄に外食代を入れて計算してください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const p=Math.max(0,+$('present').value||0),n=Math.max(0,+$('n').value||0),c=Math.max(0,+$('cake').value||0),f=Math.max(0,+$('food').value||0);
    const pv=p*n,total=pv+c+f;
    $('sub').textContent=`プレゼント${num(p)}円×${n}人 ＋ ケーキ＋ごちそう`;$('pv').textContent=yen(pv);$('fv').textContent=yen(c+f);$('nv').textContent=n+'人';
    SHARE=`クリスマス予算シミュ、今年のクリスマスは総額約${yen(total)}でした🎄`;show();anim($('big'),0,total,800);}''')

add(id='nengajo-cost', cat=SE, emoji='🎍',
  title='年賀状コストシミュレーター｜年賀状、出すといくら？｜シミュラボ',
  desc='出す枚数とはがき代・印刷代から、年賀状にかかる総額と、メール・LINEに切り替えた場合の節約額を計算する無料シミュレーター。',
  ogtitle='年賀状コストシミュレーター｜出すといくら？', ogdesc='枚数とはがき代・印刷代から年賀状の総額を計算。',
  h1='年賀状コストシミュレーター',
  lead='年賀状、出すと意外とかかります。枚数・はがき代・印刷代から総額を計算。デジタル年賀（メール・LINE）に切り替えた場合の節約額も出します。',
  inputs='''    <h2>🎍 条件を入れる</h2>
    <div class="row"><div class="field"><label>出す枚数 <span class="hint">（枚）</span></label><input type="number" id="n" value="50" min="0" inputmode="numeric"></div>
    <div class="field"><label>はがき1枚 <span class="hint">（円）</span></label><input type="number" id="hagaki" value="85" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>1枚あたり印刷・インク代 <span class="hint">（円）</span></label><input type="number" id="print" value="30" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">総額を見る</button>''',
  result='''      <div class="label">年賀状の総額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">はがき代</div><div class="v" id="hv">—</div></div>
      <div class="stat"><div class="k">10年で</div><div class="v accent" id="y10">—</div></div>
      <div class="stat"><div class="k">デジタルなら節約</div><div class="v" id="save">—</div></div></div>''',
  article='''    <h2>年賀状の費用</h2>
    <div class="note"><strong>計算式</strong><br>総額 ＝ 枚数 ×（はがき代 ＋ 印刷・インク代）</div>
    <p>枚数が多いとまとまった出費に。近年はメールやLINE、年賀状アプリで済ませる人も増えています。大切な相手には手書きで、それ以外はデジタルで、と使い分けるのも◎。</p>
    <h2>よくある質問</h2>'''+faq([('印刷を業者に頼むと？','1枚あたりの単価を「印刷代」に入れて計算してください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const n=Math.max(0,+$('n').value||0),h=Math.max(0,+$('hagaki').value||0),p=Math.max(0,+$('print').value||0);
    const total=n*(h+p);
    $('sub').textContent=`${n}枚 ×（${num(h)}＋${num(p)}円）`;$('hv').textContent=yen(n*h);$('y10').textContent=yen(total*10);$('save').textContent=yen(total);
    SHARE=`年賀状コストシミュ、${n}枚で総額約${yen(total)}でした🎍`;show();anim($('big'),0,total,800);}''')

add(id='kisei-hiyou', cat=SE, emoji='🚄',
  title='帰省費用シミュレーター｜年末年始・お盆の帰省、いくら？｜シミュラボ',
  desc='交通費・お土産・お年玉・外食などから、年末年始やお盆の帰省にかかる費用を試算する無料シミュレーター。',
  ogtitle='帰省費用シミュレーター｜帰省にいくら？', ogdesc='交通費・お土産・お年玉から帰省費用を試算。',
  h1='帰省費用シミュレーター',
  lead='年末年始やお盆の帰省、トータルでいくら？家族の交通費・お土産・お年玉・外食を合計して、帰省にかかる費用を試算します。',
  inputs='''    <h2>🚄 条件を入れる</h2>
    <div class="row"><div class="field"><label>交通費（往復・家族合計） <span class="hint">（円）</span></label><input type="number" id="trans" value="40000" min="0" inputmode="numeric"></div>
    <div class="field"><label>お土産 <span class="hint">（円）</span></label><input type="number" id="omiyage" value="10000" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>お年玉・お小遣い <span class="hint">（円）</span></label><input type="number" id="otoshidama" value="15000" min="0" inputmode="numeric"></div>
    <div class="field"><label>外食・その他 <span class="hint">（円）</span></label><input type="number" id="other" value="15000" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">帰省費用を見る</button>''',
  result='''      <div class="label">帰省の総費用</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">交通費の割合</div><div class="v accent" id="trate">—</div></div>
      <div class="stat"><div class="k">年2回(盆・正月)</div><div class="v" id="twice">—</div></div>
      <div class="stat"><div class="k">交通費以外</div><div class="v" id="rest">—</div></div></div>''',
  article='''    <h2>帰省費用の内訳</h2>
    <div class="note"><strong>計算式</strong><br>総額 ＝ 交通費 ＋ お土産 ＋ お年玉 ＋ 外食・その他</div>
    <p>遠方ほど交通費がかさみます。繁忙期は運賃も高め。早割・回数券・高速の深夜割引などで交通費を抑えるのが節約のカギ。年2回帰ると倍かかるので、計画的に。</p>
    <h2>よくある質問</h2>'''+faq([('帰省を年1回にすると？','「年2回」の半額が目安。本ツールで1回分を出して比較を。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const t=Math.max(0,+$('trans').value||0),o=Math.max(0,+$('omiyage').value||0),y=Math.max(0,+$('otoshidama').value||0),e=Math.max(0,+$('other').value||0);
    const total=t+o+y+e;
    $('sub').textContent=`交通${num(t)}＋土産＋お年玉＋外食`;$('trate').textContent=total>0?Math.round(t/total*100)+'%':'-';$('twice').textContent=yen(total*2);$('rest').textContent=yen(o+y+e);
    SHARE=`帰省費用シミュ、今回の帰省は約${yen(total)}でした🚄（年2回なら${yen(total*2)}）`;show();anim($('big'),0,total,800);}''')

add(id='goshugi-souba', cat=SE, emoji='💐',
  title='ご祝儀・香典の相場シミュレーター｜関係別にいくら包む？｜シミュラボ',
  desc='相手との関係（友人・親族・上司など）と行事（結婚式・葬儀・出産祝いなど）から、ご祝儀・香典・お祝いの相場の目安を表示する無料ツール。',
  ogtitle='ご祝儀・香典の相場｜いくら包む？', ogdesc='関係と行事からご祝儀・香典の相場の目安を表示。',
  h1='ご祝儀・香典の相場シミュレーター',
  lead='結婚式のご祝儀、お葬式の香典、いくら包めばいい？相手との関係と行事から、相場の目安を表示します。マナーで迷ったときの早見に。',
  inputs='''    <h2>💐 条件を選ぶ</h2>
    <div class="field"><label>行事</label><select id="event"><option value="wedding" selected>結婚式（ご祝儀）</option><option value="funeral">葬儀（香典）</option><option value="birth">出産祝い</option></select></div>
    <div class="field"><label>相手との関係</label><select id="rel"><option value="friend" selected>友人・同僚</option><option value="relative">親族（いとこ等）</option><option value="close">兄弟姉妹・親しい親族</option><option value="boss">上司・恩師</option></select></div>
    <button class="btn btn-primary" id="calcBtn">相場を見る</button>''',
  result='''      <div class="label">相場の目安</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:18px;">—</div>''',
  article='''    <h2>ご祝儀・香典のマナー</h2>
    <div class="note"><strong>目安</strong><br>結婚式：友人3万／親族3〜5万／兄弟5万<br>香典：友人5千〜1万／親族1〜3万<br>出産祝い：友人5千〜1万／親族1〜3万</div>
    <p>ご祝儀は「4」「9」を避け、結婚式は割り切れない奇数（3万など）が定番。香典は新札を避けるなどのマナーも。地域・家のしきたりで変わるので、迷ったら周囲に確認を。本ツールは一般的な目安です。</p>
    <h2>よくある質問</h2>'''+faq([('夫婦で出席は？','結婚式の夫婦連名は5万円が一般的な目安です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const ev=$('event').value, rel=$('rel').value;
    const tbl={wedding:{friend:30000,relative:30000,close:50000,boss:30000},funeral:{friend:7000,relative:15000,close:30000,boss:10000},birth:{friend:7000,relative:15000,close:20000,boss:10000}};
    const v=tbl[ev][rel];
    const note={wedding:'割り切れない奇数（3万など）が定番。新札で。',funeral:'香典は新札を避けるのがマナー。表書きは宗派で確認を。',birth:'実用品や現金で。出産後1ヶ月以内が目安。'}[ev];
    $('sub').textContent=`${sel('event').text}・${sel('rel').text}`;$('adv').textContent='💐 '+note;
    SHARE=`ご祝儀・香典の相場シミュ、${sel('event').text}（${sel('rel').text}）の目安は約${yen(v)}でした💐`;show();anim($('big'),0,v,800);}''')

add(id='hanami-yosan', cat=SE, emoji='🌸',
  title='花見・BBQ予算シミュレーター｜1人いくら？幹事の計算に｜シミュラボ',
  desc='参加人数と食材・飲み物・場所代から、花見やBBQの総額と1人あたりの会費を計算する幹事向け無料シミュレーター。',
  ogtitle='花見・BBQ予算シミュレーター｜1人いくら？', ogdesc='人数と食材・飲み物から花見・BBQの会費を計算。',
  h1='花見・BBQ予算シミュレーター',
  lead='花見やBBQの幹事さんへ。人数と食材・飲み物・場所代から、総額と1人あたりの会費をサッと計算。集金額の設定に便利です。',
  inputs='''    <h2>🌸 条件を入れる</h2>
    <div class="row"><div class="field"><label>参加人数 <span class="hint">（人）</span></label><input type="number" id="n" value="10" min="1" inputmode="numeric"></div>
    <div class="field"><label>1人あたり食材 <span class="hint">（円）</span></label><input type="number" id="food" value="1500" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>1人あたり飲み物 <span class="hint">（円）</span></label><input type="number" id="drink" value="1000" min="0" inputmode="numeric"></div>
    <div class="field"><label>場所代・備品 <span class="hint">（円・全体）</span></label><input type="number" id="place" value="3000" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">会費を見る</button>''',
  result='''      <div class="label">1人あたりの会費</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">総額</div><div class="v accent" id="total">—</div></div>
      <div class="stat"><div class="k">集金は(端数切上)</div><div class="v" id="round">—</div></div>
      <div class="stat"><div class="k">人数</div><div class="v" id="nv">—</div></div></div>''',
  article='''    <h2>幹事の会費計算</h2>
    <div class="note"><strong>計算式</strong><br>総額 ＝（食材＋飲み物）× 人数 ＋ 場所代<br>1人あたり ＝ 総額 ÷ 人数</div>
    <p>会費は端数を切り上げて集めると、買い出しの予備費になり安心。多めに集めて余ったら返す or 次回に、が幹事のコツ。ドタキャン用に少し余裕を持たせるのも◎。</p>
    <h2>よくある質問</h2>'''+faq([('お酒を飲まない人は？','飲み物代を分けて、飲む人だけで割ると公平です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const n=Math.max(1,+$('n').value||1),f=Math.max(0,+$('food').value||0),d=Math.max(0,+$('drink').value||0),p=Math.max(0,+$('place').value||0);
    const total=(f+d)*n+p, per=total/n, round=Math.ceil(per/500)*500;
    $('sub').textContent=`${n}人・食材＋飲み物＋場所代`;$('total').textContent=yen(total);$('round').textContent=yen(round);$('nv').textContent=n+'人';
    SHARE=`花見・BBQ予算シミュ、1人あたり約${yen(per)}（集金は${yen(round)}が無難）でした🌸`;show();anim($('big'),0,per,800);}''')

add(id='valentine-yosan', cat=SE, emoji='🍫',
  title='バレンタイン予算シミュレーター｜本命・義理でいくら？｜シミュラボ',
  desc='本命チョコ・義理チョコ・友チョコ・自分チョコの個数と単価から、バレンタインにかかる総額を計算する無料シミュレーター。',
  ogtitle='バレンタイン予算シミュレーター｜いくらかかる？', ogdesc='本命・義理・友チョコの個数からバレンタイン予算を計算。',
  h1='バレンタイン予算シミュレーター',
  lead='本命に義理に友チョコに…バレンタイン、トータルでいくら？種類ごとの個数と単価から総額を計算します。予算オーバー防止に。',
  inputs='''    <h2>🍫 条件を入れる</h2>
    <div class="row"><div class="field"><label>本命チョコ <span class="hint">（円）</span></label><input type="number" id="honmei" value="3000" min="0" inputmode="numeric"></div>
    <div class="field"><label>義理チョコ 単価×個数</label><input type="number" id="giri" value="500" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>義理の個数</label><input type="number" id="girin" value="5" min="0" inputmode="numeric"></div>
    <div class="field"><label>友チョコ・自分用 <span class="hint">（円・合計）</span></label><input type="number" id="tomo" value="2000" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">総額を見る</button>''',
  result='''      <div class="label">バレンタインの総額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">義理チョコ計</div><div class="v accent" id="gv">—</div></div>
      <div class="stat"><div class="k">本命</div><div class="v" id="hv">—</div></div>
      <div class="stat"><div class="k">友・自分用</div><div class="v" id="tv">—</div></div></div>''',
  article='''    <h2>バレンタインの予算</h2>
    <div class="note"><strong>計算式</strong><br>総額 ＝ 本命 ＋ 義理単価 × 個数 ＋ 友・自分用</div>
    <p>近年は「自分へのご褒美チョコ」も人気。義理チョコは数が増えると地味にかさみます。手作りやシェア買いで節約も。気持ちが伝わるのがいちばんですね。</p>
    <h2>よくある質問</h2>'''+faq([('ホワイトデーのお返しは？','一般に「3倍返し」と言われますが、最近は同等が主流です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const h=Math.max(0,+$('honmei').value||0),g=Math.max(0,+$('giri').value||0),gn=Math.max(0,+$('girin').value||0),t=Math.max(0,+$('tomo').value||0);
    const gv=g*gn,total=h+gv+t;
    $('sub').textContent=`本命${num(h)}＋義理${num(g)}×${gn}＋友・自分`;$('gv').textContent=yen(gv);$('hv').textContent=yen(h);$('tv').textContent=yen(t);
    SHARE=`バレンタイン予算シミュ、今年は総額約${yen(total)}でした🍫`;show();anim($('big'),0,total,800);}''')

add(id='gyouji-countdown', cat=SE, emoji='🎉',
  title='行事カウントダウン｜次のイベントまであと何日？｜シミュラボ',
  desc='正月・節分・ひな祭り・GW・クリスマスなど、選んだ行事まであと何日かを表示するエンタメシミュレーター。',
  ogtitle='行事カウントダウン｜次のイベントまで何日？', ogdesc='選んだ年中行事まであと何日かを表示。',
  h1='行事カウントダウン',
  lead='次のあのイベントまで、あと何日？お正月・節分・ひな祭り・GW・お盆・ハロウィン・クリスマスなど、年中行事までのカウントダウンを表示します。',
  inputs='''    <h2>🎉 行事を選ぶ</h2>
    <div class="field"><label>イベント</label><select id="ev"><option value="1-1">お正月（1/1）</option><option value="2-3">節分（2/3）</option><option value="2-14">バレンタイン（2/14）</option><option value="3-3">ひな祭り（3/3）</option><option value="5-5">こどもの日（5/5）</option><option value="7-7">七夕（7/7）</option><option value="10-31">ハロウィン（10/31）</option><option value="12-25" selected>クリスマス（12/25）</option><option value="12-31">大晦日（12/31）</option></select></div>
    <button class="btn btn-primary" id="calcBtn">カウントダウン</button>''',
  result='''      <div class="label">次のイベントまで</div>
      <div class="big"><span id="big">0</span><span class="unit">日</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">その日</div><div class="v accent" id="date">—</div></div>
      <div class="stat"><div class="k">週末の回数</div><div class="v" id="week">—</div></div>
      <div class="stat"><div class="k">今日が当日なら</div><div class="v" id="today">—</div></div></div>''',
  article='''    <h2>行事を楽しもう</h2>
    <p>次のイベントまでの日数が分かると、準備や計画が立てやすくなります。プレゼントや旅行の手配、衣装やごちそうの準備に。残りの週末の回数も表示するので、計画的に楽しめます。</p>
    <h2>よくある質問</h2>'''+faq([('過ぎた行事は？','その年の分が過ぎていれば、翌年の同じ日までを表示します。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const v=$('ev').value.split('-').map(Number);const T=new Date();T.setHours(0,0,0,0);
    let target=new Date(T.getFullYear(),v[0]-1,v[1]); if(target<T)target=new Date(T.getFullYear()+1,v[0]-1,v[1]);
    const days=Math.round((target-T)/86400000);
    $('sub').textContent=`${sel('ev').text}まで`;$('date').textContent=`${target.getFullYear()}/${v[0]}/${v[1]}`;$('week').textContent=Math.floor(days/7)+'回';$('today').textContent=days===0?'今日です🎉':'—';
    SHARE=`行事カウントダウン、${sel('ev').text}まであと${days}日でした🎉`;show();anim($('big'),0,days,800);}''')

if __name__=='__main__':
    write_all(SIMS)
    print(f'season done. {len(SIMS)} sims.')
