# -*- coding: utf-8 -*-
"""シミュラボ：推し活・エンタメカテゴリ 10本（gen_sims11のTPLを再利用）。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq, write_all

O='推し活・エンタメ'
SIMS=[]

SIMS.append(dict(id='oshi-nenkan', cat=O, emoji='💸',
  title='推し活 年間費用シミュレーター｜推しにかけてるお金、年いくら？｜シミュラボ',
  desc='グッズ・ライブ・配信などの推し活費から、1年・10年でいくら使っているかを計算するエンタメシミュレーター。',
  ogtitle='推し活 年間費用｜推しにかけてるお金は？', ogdesc='グッズ・ライブ・配信から推し活費を年間で計算。',
  h1='推し活 年間費用シミュレーター',
  lead='グッズにライブにサブスク…推しに使うお金、年でいくら？合計を見える化します（金額の多さは、愛の深さということで）。',
  inputs='''    <h2>💸 条件を入れる</h2>
    <div class="field"><label>グッズ・CD等 <span class="hint">（円/月）</span></label><input type="number" id="goods" value="8000" min="0" inputmode="numeric"></div>
    <div class="row"><div class="field"><label>ライブ・イベント <span class="hint">（円/回）</span></label><input type="number" id="livep" value="12000" min="0" inputmode="numeric"></div>
    <div class="field"><label>年の参加回数</label><input type="number" id="livef" value="4" min="0" max="100" inputmode="numeric"></div></div>
    <div class="field"><label>配信・サブスク <span class="hint">（円/月）</span></label><input type="number" id="sub" value="2000" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">年間費用を見る</button>''',
  result='''      <div class="label">推し活の年間費用</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub2">—</div>
      <div class="statline"><div class="stat"><div class="k">1ヶ月あたり</div><div class="v" id="m">—</div></div>
      <div class="stat"><div class="k">10年で</div><div class="v accent" id="y10">—</div></div>
      <div class="stat"><div class="k">愛の重さ</div><div class="v" id="love">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>年間 ＝（グッズ＋配信）× 12 ＋ ライブ単価 × 参加回数</div>
    <p>推し活は心の栄養。無理のない範囲で、ちゃんと楽しむのがいちばんです。金額を把握しておくと、ここぞの遠征やグッズに気持ちよくお金を使えます。</p>
    <h2>よくある質問</h2>'''+faq([('使いすぎ？','金額より「生活に無理がないか」が大事。把握できていれば大丈夫です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const g=Math.max(0,+$('goods').value||0), lp=Math.max(0,+$('livep').value||0), lf=Math.max(0,+$('livef').value||0), s=Math.max(0,+$('sub').value||0);
    const year=(g+s)*12+lp*lf;
    let love; if(year>=500000)love='激重❤️‍🔥'; else if(year>=200000)love='ガチ勢💪'; else if(year>=60000)love='しっかり推し'; else love='ライト層';
    $('sub2').textContent=`グッズ${num(g)}＋配信${num(s)}（月）＋ライブ年${lf}回`;
    $('m').textContent=yen(year/12); $('y10').textContent=yen(year*10); $('love').textContent=love;
    SHARE=`推し活の年間費用シミュ、私は年で約${yen(year)}でした💸（${love}）\\n推しは推せるときに推せ！👇`;
    show(); anim($('big'),0,year,900);
  }'''))

SIMS.append(dict(id='live-ensei', cat=O, emoji='🚄',
  title='ライブ遠征費シミュレーター｜遠征、年でいくら使ってる？｜シミュラボ',
  desc='1回の遠征費（交通・宿・チケット）と年の遠征回数から、ライブ遠征にかかる年間・生涯の費用を計算する無料シミュレーター。',
  ogtitle='ライブ遠征費｜遠征に年いくら使ってる？', ogdesc='1回の遠征費と回数から、年間の遠征費を計算。',
  h1='ライブ遠征費シミュレーター',
  lead='交通費に宿泊にチケット…遠征は楽しいけどお金もかかる。1回の遠征費と年の回数から、年間・生涯の遠征費を出します。',
  inputs='''    <h2>🚄 条件を入れる</h2>
    <div class="row"><div class="field"><label>1回の遠征費 <span class="hint">（交通+宿+チケ・円）</span></label><input type="number" id="cost" value="30000" min="0" inputmode="numeric"></div>
    <div class="field"><label>年の遠征回数</label><input type="number" id="freq" value="5" min="0" max="100" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">遠征費を見る</button>''',
  result='''      <div class="label">年間の遠征費</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub2">—</div>
      <div class="statline"><div class="stat"><div class="k">1回あたり</div><div class="v" id="per">—</div></div>
      <div class="stat"><div class="k">10年で</div><div class="v accent" id="y10">—</div></div>
      <div class="stat"><div class="k">月の積立目安</div><div class="v" id="save">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>年間 ＝ 1回の遠征費 × 年の回数／月の積立 ＝ 年間 ÷ 12</div>
    <p>遠征は早割・周遊きっぷ・相部屋で大きく節約できます。あらかじめ「遠征貯金」をしておくと、急な参戦にも慌てません。最高の思い出に、計画的に。</p>
    <h2>よくある質問</h2>'''+faq([('節約のコツは？','早割航空券・夜行バス・友達と相部屋が定番。ポイント還元も活用を。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const cost=Math.max(0,+$('cost').value||0), freq=Math.max(0,+$('freq').value||0);
    const year=cost*freq;
    $('sub2').textContent=`1回${num(cost)}円 × 年${freq}回`;
    $('per').textContent=yen(cost); $('y10').textContent=yen(year*10); $('save').textContent=yen(year/12);
    SHARE=`ライブ遠征費シミュ、私は年で約${yen(year)}（10年で${yen(year*10)}）でした🚄\\n遠征は思い出への投資…！👇`;
    show(); anim($('big'),0,year,900);
  }'''))

SIMS.append(dict(id='subsc-motodori', cat=O, emoji='📺',
  title='動画サブスク 元取りシミュレーター｜月何本観れば元が取れる？｜シミュラボ',
  desc='動画サブスクの月額と、レンタルした場合の1本の料金から、月に何本観れば元が取れるか・今の視聴本数での損得を計算する無料シミュレーター。',
  ogtitle='動画サブスク 元取り｜月何本で元が取れる？', ogdesc='サブスク月額とレンタル料から、元取り本数を計算。',
  h1='動画サブスク 元取りシミュレーター',
  lead='見放題サブスク、ちゃんと元取れてる？月額とレンタル料から、何本観れば元が取れるか・今の本数での損得を出します。',
  inputs='''    <h2>📺 条件を入れる</h2>
    <div class="row"><div class="field"><label>サブスク月額 <span class="hint">（円）</span></label><input type="number" id="sub" value="1000" min="0" inputmode="numeric"></div>
    <div class="field"><label>レンタルなら1本 <span class="hint">（円）</span></label><input type="number" id="rent" value="400" min="1" inputmode="numeric"></div></div>
    <div class="field"><label>月に観る本数 <span class="hint">（本）</span></label><input type="number" id="watch" value="8" min="0" max="200" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">損得を見る</button>''',
  result='''      <div class="label" id="lab">今の本数での損得</div>
      <div class="big"><span id="big">0</span><span class="unit">円 お得</span></div>
      <div class="sub" id="sub2">—</div>
      <div class="statline"><div class="stat"><div class="k">元取りライン</div><div class="v accent" id="be">—</div></div>
      <div class="stat"><div class="k">レンタル換算</div><div class="v" id="rentv">—</div></div>
      <div class="stat"><div class="k">年間のお得</div><div class="v" id="year">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>元取りライン ＝ 月額 ÷ レンタル1本<br>損得 ＝ 観る本数 × レンタル料 − 月額</div>
    <p>見放題は「観るほどお得」。ほとんど観ない月が続くなら解約も選択肢です。複数サブスクを契約しているなら、観ていないものを見直すと固定費がスッキリ。</p>
    <h2>よくある質問</h2>'''+faq([('オリジナル作品は？','金額換算しにくい価値もあります。あくまでレンタル比較の目安です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const sub=Math.max(0,+$('sub').value||0), rent=Math.max(1,+$('rent').value||1), watch=Math.max(0,+$('watch').value||0);
    const rentv=watch*rent, profit=rentv-sub, be=sub/rent;
    $('lab').textContent= profit>=0?'今の本数での お得額':'今の本数での 損';
    $('sub2').textContent=`月額${num(sub)}円・月${watch}本視聴`;
    $('be').textContent=Math.ceil(be)+'本/月'; $('rentv').textContent=yen(rentv); $('year').textContent=yen(Math.abs(profit)*12);
    SHARE=`動画サブスク元取りシミュ、月${watch}本観る私は${profit>=0?yen(profit)+'お得':yen(-profit)+'損'}でした📺（元取りは月${Math.ceil(be)}本）\\nあなたは？👇`;
    show(); anim($('big'),0,Math.abs(profit),900);
  }'''))

SIMS.append(dict(id='tsumige', cat=O, emoji='🎮',
  title='積みゲー消化シミュレーター｜全部クリアに何年かかる？｜シミュラボ',
  desc='積んでいるゲームの本数とクリア時間、週のプレイ時間から、すべて消化するのに何年かかるかを計算するエンタメシミュレーター。',
  ogtitle='積みゲー消化｜全部クリアに何年？', ogdesc='積みゲーの本数とプレイ時間から消化年数を計算。',
  h1='積みゲー消化シミュレーター',
  lead='買ったのに手をつけてないゲーム、何本ある？積み本数とプレイ時間から、全部クリアするのに何年かかるかを計算します（現実を直視）。',
  inputs='''    <h2>🎮 条件を入れる</h2>
    <div class="row"><div class="field"><label>積みゲーの本数 <span class="hint">（本）</span></label><input type="number" id="games" value="15" min="0" inputmode="numeric"></div>
    <div class="field"><label>1本のクリア時間 <span class="hint">（時間）</span></label><input type="number" id="clear" value="30" min="1" inputmode="numeric"></div></div>
    <div class="field"><label>週のプレイ時間 <span class="hint">（時間）</span></label><input type="number" id="play" value="5" min="0.5" step="0.5" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">消化にかかる年数を見る</button>''',
  result='''      <div class="label">全部消化するのに</div>
      <div class="big"><span id="big">0</span><span class="unit">年</span></div>
      <div class="sub" id="sub2">—</div>
      <div class="statline"><div class="stat"><div class="k">総プレイ時間</div><div class="v accent" id="total">—</div></div>
      <div class="stat"><div class="k">積みの総額(1本7千)</div><div class="v" id="price">—</div></div>
      <div class="stat"><div class="k">判定</div><div class="v" id="judge">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>総時間 ＝ 本数 × クリア時間<br>消化年数 ＝ 総時間 ÷（週のプレイ時間 × 52週）</div>
    <p>セールでつい買ってしまう積みゲー。全部やる前提だと意外な年月に。「今やりたい1本」に集中するか、思い切って手放すのも手です（罪悪感は手放してOK）。</p>
    <h2>よくある質問</h2>'''+faq([('減らすコツは？','新作を買う前に1本クリア、のルールが効きます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const games=Math.max(0,+$('games').value||0), clear=Math.max(1,+$('clear').value||1), play=Math.max(0.1,+$('play').value||1);
    const total=games*clear, years=total/(play*52);
    let j; if(years>=5)j='一生もの…😱'; else if(years>=2)j='なかなか手強い'; else if(years>=0.5)j='頑張れば消化可'; else j='余裕で消化';
    $('sub2').textContent=`${games}本 × ${clear}時間 ÷ 週${play}時間`;
    $('total').textContent=num(total)+'時間'; $('price').textContent=yen(games*7000); $('judge').textContent=j;
    SHARE=`積みゲー消化シミュ、全部クリアに約${years.toFixed(1)}年かかる計算でした🎮（${j}）\\nまずは1本…！あなたは？👇`;
    show(); anim($('big'),0,years,900,1);
  }'''))

SIMS.append(dict(id='eiga-shougai', cat=O, emoji='🎬',
  title='一生で観る映画の本数シミュレーター｜あと何本観られる？｜シミュラボ',
  desc='年間の映画鑑賞本数とこれからの年数から、一生で観られる映画の本数と総鑑賞時間を計算するエンタメシミュレーター。',
  ogtitle='一生で観る映画の本数｜あと何本？', ogdesc='年間本数と年数から、生涯の鑑賞本数・時間を計算。',
  h1='一生で観る映画の本数シミュレーター',
  lead='世の中には観たい映画が無限にある。でも一生で観られる本数には限りが…。年間の鑑賞本数から、これから観られる映画の本数を出します。',
  inputs='''    <h2>🎬 条件を入れる</h2>
    <div class="row"><div class="field"><label>年間の鑑賞本数 <span class="hint">（本）</span></label><input type="number" id="year" value="30" min="0" inputmode="numeric"></div>
    <div class="field"><label>これからの年数 <span class="hint">（年）</span></label><input type="number" id="years" value="50" min="1" max="90" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">一生分を見る</button>''',
  result='''      <div class="label">これから観られる映画</div>
      <div class="big"><span id="big">0</span><span class="unit">本</span></div>
      <div class="sub" id="sub2">—</div>
      <div class="statline"><div class="stat"><div class="k">総鑑賞時間</div><div class="v accent" id="hours">—</div></div>
      <div class="stat"><div class="k">日数にすると</div><div class="v" id="days">—</div></div>
      <div class="stat"><div class="k">月あたり</div><div class="v" id="m">—</div></div></div>''',
  article='''    <h2>限りある時間を、好きなことに</h2>
    <div class="note"><strong>計算式</strong><br>生涯本数 ＝ 年間本数 × 年数（1本2時間で時間換算）</div>
    <p>数字にすると意外と限られています。だからこそ「観たい映画リスト」を作って、本当に観たい作品から観るのがおすすめ。積ん読・積みドラマも同じですね。</p>
    <h2>よくある質問</h2>'''+faq([('ドラマでもできる？','本数を「観る作品数」に置き換えればOKです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const y=Math.max(0,+$('year').value||0), years=Math.max(1,+$('years').value||1);
    const total=y*years, hours=total*2, days=hours/24;
    $('sub2').textContent=`年${y}本 × ${years}年`;
    $('hours').textContent=num(hours)+'時間'; $('days').textContent=num(days)+'日分'; $('m').textContent=(y/12).toFixed(1)+'本';
    SHARE=`一生で観る映画シミュ、これから約${num(total)}本観られる計算でした🎬\\n観たい映画から観よ…！あなたは？👇`;
    show(); anim($('big'),0,total,900);
  }'''))

SIMS.append(dict(id='manga-otomegai', cat=O, emoji='📚',
  title='漫画 大人買いシミュレーター｜全巻そろえると総額・本棚の幅は？｜シミュラボ',
  desc='漫画の巻数と1巻の価格から、全巻大人買いの総額と、本棚に並べたときの幅・積んだときの高さを計算するエンタメシミュレーター。',
  ogtitle='漫画 大人買い｜全巻そろえると総額は？', ogdesc='巻数と単価から、全巻の総額・本棚の幅を計算。',
  h1='漫画 大人買いシミュレーター',
  lead='気になるあの作品、全巻そろえるといくら？そして本棚にどれだけ場所を取る？巻数と単価から、総額と本棚の幅・積んだ高さを出します。',
  inputs='''    <h2>📚 条件を入れる</h2>
    <div class="row"><div class="field"><label>巻数 <span class="hint">（巻）</span></label><input type="number" id="vol" value="100" min="1" inputmode="numeric"></div>
    <div class="field"><label>1巻の価格 <span class="hint">（円）</span></label><input type="number" id="price" value="500" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">総額を見る</button>''',
  result='''      <div class="label">全巻そろえる総額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub2">—</div>
      <div class="statline"><div class="stat"><div class="k">本棚の幅</div><div class="v accent" id="width">—</div></div>
      <div class="stat"><div class="k">積むと高さ</div><div class="v" id="height">—</div></div>
      <div class="stat"><div class="k">重さ</div><div class="v" id="weight">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>総額 ＝ 巻数 × 1巻の価格<br>幅 ＝ 巻数 × 約1.5cm／重さ ＝ 巻数 × 約200g</div>
    <p>長編をそろえると、お金も場所もそれなり。電子書籍なら場所いらずで一気読みも。紙の背表紙が並ぶ満足感も捨てがたいですよね。</p>
    <h2>よくある質問</h2>'''+faq([('電子と紙どっち？','一気読み・省スペースなら電子、コレクション性なら紙。好みで。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const vol=Math.max(1,+$('vol').value||1), price=Math.max(0,+$('price').value||0);
    const total=vol*price, width=vol*1.5, weight=vol*200;
    $('sub2').textContent=`${vol}巻 × ${num(price)}円`;
    $('width').textContent=(width/100).toFixed(1)+'m'; $('height').textContent=(width/100).toFixed(1)+'m'; $('weight').textContent=(weight/1000).toFixed(1)+'kg';
    SHARE=`漫画大人買いシミュ、全${vol}巻で約${yen(total)}・本棚${(width/100).toFixed(1)}m分でした📚\\nそろえる勇気…！あなたの推し作品は？👇`;
    show(); anim($('big'),0,total,900);
  }'''))

SIMS.append(dict(id='oshi-jikan', cat=O, emoji='⏰',
  title='推しに使う時間シミュレーター｜一生で何日、推しと過ごす？｜シミュラボ',
  desc='1日の推し活時間とこれからの年数から、一生で推しに使う時間を計算するエンタメシミュレーター。',
  ogtitle='推しに使う時間｜一生で何日、推しと過ごす？', ogdesc='1日の推し活時間から、生涯で推しに使う時間を計算。',
  h1='推しに使う時間シミュレーター',
  lead='動画を観たりSNSを追ったり…1日のうち推しに使う時間、一生だとどれくらい？「好き」に費やす時間を見える化します（幸せな時間の総量）。',
  inputs='''    <h2>⏰ 条件を入れる</h2>
    <div class="row"><div class="field"><label>1日の推し活時間 <span class="hint">（時間）</span></label><input type="number" id="hpd" value="2" min="0" max="20" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>これからの年数 <span class="hint">（年）</span></label><input type="number" id="years" value="20" min="1" max="80" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">推しと過ごす時間を見る</button>''',
  result='''      <div class="label">一生で推しに使う時間</div>
      <div class="big"><span id="big">0</span><span class="unit">日分</span></div>
      <div class="sub" id="sub2">—</div>
      <div class="statline"><div class="stat"><div class="k">合計時間</div><div class="v accent" id="hours">—</div></div>
      <div class="stat"><div class="k">1年で</div><div class="v" id="year">—</div></div>
      <div class="stat"><div class="k">幸福度</div><div class="v" id="happy">—</div></div></div>''',
  article='''    <h2>「好き」に使う時間は宝物</h2>
    <div class="note"><strong>計算式</strong><br>生涯時間 ＝ 1日の推し活時間 × 365 × 年数</div>
    <p>時間は有限。その中で「好き」に使える時間は、人生の幸福度に直結します。推し活の時間を「無駄」なんて誰にも言わせない。心の栄養、たっぷり摂りましょう。</p>
    <h2>よくある質問</h2>'''+faq([('使いすぎ？','生活に支障がなければOK。好きな時間は心の健康に良いとされます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const h=Math.max(0,+$('hpd').value||0), years=Math.max(1,+$('years').value||1);
    const hours=h*365*years, days=hours/24;
    let happy; if(h>=4)happy='幸せMAX❤️'; else if(h>=2)happy='充実♪'; else happy='ほどよく';
    $('sub2').textContent=`1日${h}時間 × 365日 × ${years}年`;
    $('hours').textContent=num(hours)+'時間'; $('year').textContent=num(h*365)+'時間'; $('happy').textContent=happy;
    SHARE=`推しに使う時間シミュ、一生で約${num(days)}日分も推しと過ごせる計算でした⏰\\n幸せな時間…！あなたは？👇`;
    show(); anim($('big'),0,days,900);
  }'''))

SIMS.append(dict(id='ticket-tousen', cat=O, emoji='🎫',
  title='チケット当選確率シミュレーター｜何口応募すれば当たる？｜シミュラボ',
  desc='抽選の倍率と応募口数から、ライブ・イベントのチケットに少なくとも1枚当たる確率を計算するエンタメシミュレーター。',
  ogtitle='チケット当選確率｜何口応募すれば当たる？', ogdesc='倍率と応募口数から、当選確率を計算。',
  h1='チケット当選確率シミュレーター',
  lead='人気公演の抽選、何口申し込めば当たる？倍率と応募口数から、少なくとも1枚当選する確率を計算します（複数名義・複数公演の戦略づくりに）。',
  inputs='''    <h2>🎫 条件を入れる</h2>
    <div class="row"><div class="field"><label>当選倍率 <span class="hint">（◯倍）</span></label><input type="number" id="rate" value="10" min="1" inputmode="numeric"></div>
    <div class="field"><label>応募する口数 <span class="hint">（名義×公演数）</span></label><input type="number" id="n" value="3" min="1" max="100" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">当選確率を見る</button>''',
  result='''      <div class="label">少なくとも1枚 当たる確率</div>
      <div class="big"><span id="big">0</span><span class="unit">%</span></div>
      <div class="sub" id="sub2">—</div>
      <div class="statline"><div class="stat"><div class="k">1口あたり</div><div class="v" id="single">—</div></div>
      <div class="stat"><div class="k">全部外れる確率</div><div class="v accent" id="miss">—</div></div>
      <div class="stat"><div class="k">判定</div><div class="v" id="judge">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>1口の当選率 ＝ 1 ÷ 倍率<br>少なくとも1当選 ＝ 1 −（1 − 当選率）^口数</div>
    <p>口数を増やすほど当選確率は上がりますが、倍率が高いと頭打ちに。複数名義・複数公演・先行抽選の活用が当選への近道。ただしルールやマナーは守って楽しみましょう。</p>
    <h2>よくある質問</h2>'''+faq([('倍率が分からない','SNSの体感や過去実績を参考に。10〜数十倍の人気公演も珍しくありません。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const rate=Math.max(1,+$('rate').value||1), n=Math.max(1,+$('n').value||1);
    const p=1/rate, win=1-Math.pow(1-p,n), miss=1-win;
    let j; if(win>=0.7)j='かなり有望🎉'; else if(win>=0.4)j='五分五分'; else j='狭き門…';
    $('sub2').textContent=`${rate}倍 に ${n}口 応募`;
    $('single').textContent=(p*100).toFixed(1)+'%'; $('miss').textContent=(miss*100).toFixed(1)+'%'; $('judge').textContent=j;
    SHARE=`チケット当選確率シミュ、${rate}倍に${n}口応募で当選確率 約${(win*100).toFixed(1)}%でした🎫（${j}）\\n当たれ…！👇`;
    show(); anim($('big'),0,win*100,900,1);
  }'''))

SIMS.append(dict(id='live-sankai', cat=O, emoji='🎤',
  title='一生で行けるライブ回数シミュレーター｜あと何回参戦できる？｜シミュラボ',
  desc='年に行くライブの回数とこれからの年数から、一生で参戦できるライブの回数と総額を計算するエンタメシミュレーター。',
  ogtitle='一生で行けるライブ回数｜あと何回参戦？', ogdesc='年の参戦回数から、生涯のライブ回数と総額を計算。',
  h1='一生で行けるライブ回数シミュレーター',
  lead='ライブに行ける回数にも、限りがある。だからこそ1回1回が宝物。年の参戦回数から、これから行けるライブの回数を出します。',
  inputs='''    <h2>🎤 条件を入れる</h2>
    <div class="row"><div class="field"><label>年に行く回数 <span class="hint">（回）</span></label><input type="number" id="year" value="6" min="0" inputmode="numeric"></div>
    <div class="field"><label>これからの年数 <span class="hint">（年）</span></label><input type="number" id="years" value="50" min="1" max="80" inputmode="numeric"></div></div>
    <div class="field"><label>1回の費用 <span class="hint">（円・総額の計算用）</span></label><input type="number" id="cost" value="12000" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">一生分を見る</button>''',
  result='''      <div class="label">これから参戦できるライブ</div>
      <div class="big"><span id="big">0</span><span class="unit">回</span></div>
      <div class="sub" id="sub2">—</div>
      <div class="statline"><div class="stat"><div class="k">生涯のライブ代</div><div class="v accent" id="cost2">—</div></div>
      <div class="stat"><div class="k">月あたり</div><div class="v" id="m">—</div></div>
      <div class="stat"><div class="k">1回の重み</div><div class="v" id="weight">—</div></div></div>''',
  article='''    <h2>1回1回を大切に</h2>
    <div class="note"><strong>計算式</strong><br>生涯回数 ＝ 年の回数 × 年数</div>
    <p>数えてみると「無限」ではないと気づきます。体力・お金・推しの活動期間…色々な条件があるからこそ、行けるときに行く。一期一会のライブを、全力で楽しみましょう。</p>
    <h2>よくある質問</h2>'''+faq([('現実的な回数？','体力や予算で変わります。あくまで「今のペースなら」の目安です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const y=Math.max(0,+$('year').value||0), years=Math.max(1,+$('years').value||1), cost=Math.max(0,+$('cost').value||0);
    const total=y*years, money=total*cost;
    $('sub2').textContent=`年${y}回 × ${years}年`;
    $('cost2').textContent=yen(money); $('m').textContent=(y/12).toFixed(1)+'回'; $('weight').textContent='プライスレス';
    SHARE=`一生で行けるライブ回数シミュ、これから約${num(total)}回参戦できる計算でした🎤\\n1回1回を大切に…！あなたは？👇`;
    show(); anim($('big'),0,total,900);
  }'''))

SIMS.append(dict(id='goods-shuunou', cat=O, emoji='📦',
  title='推しグッズ収納シミュレーター｜うちのグッズ、何箱分？｜シミュラボ',
  desc='集めた推しグッズの個数とサイズから、収納に必要な箱の数や占有スペースを計算するエンタメシミュレーター。',
  ogtitle='推しグッズ収納｜うちのグッズ、何箱分？', ogdesc='グッズの個数とサイズから、必要な収納箱の数を計算。',
  h1='推しグッズ収納シミュレーター',
  lead='増え続ける推しグッズ、収納どうする？個数とサイズから、必要な収納ケースの数と占有スペースを計算します（沼の深さの可視化）。',
  inputs='''    <h2>📦 条件を入れる</h2>
    <div class="field"><label>グッズの個数 <span class="hint">（個）</span></label><input type="number" id="n" value="200" min="0" inputmode="numeric"></div>
    <div class="field"><label>主なサイズ</label><select id="size"><option value="0.3">小（缶バッジ・アクキー等）</option><option value="1.5" selected>中（ぬい・写真集等）</option><option value="6">大（タペ・特大ぬい等）</option></select></div>
    <button class="btn btn-primary" id="calcBtn">収納量を見る</button>''',
  result='''      <div class="label">収納ケース（40L）にすると</div>
      <div class="big"><span id="big">0</span><span class="unit">箱</span></div>
      <div class="sub" id="sub2">—</div>
      <div class="statline"><div class="stat"><div class="k">総体積</div><div class="v accent" id="vol">—</div></div>
      <div class="stat"><div class="k">畳に並べると</div><div class="v" id="tatami">—</div></div>
      <div class="stat"><div class="k">沼の深さ</div><div class="v" id="numa">—</div></div></div>''',
  article='''    <h2>計算の考え方</h2>
    <div class="note"><strong>計算式</strong><br>総体積 ＝ 個数 × 1個の体積／箱数 ＝ 総体積 ÷ 収納ケース40L</div>
    <p>グッズは思い出の結晶。とはいえ収納は計画的に。お気に入りは飾る、保管はケースに、というメリハリで、推しに囲まれた快適な空間を。</p>
    <h2>よくある質問</h2>'''+faq([('飾る分は？','飾るグッズは別。あくまで「しまう量」の目安です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const n=Math.max(0,+$('n').value||0), sz=+$('size').value||1.5;
    const litres=n*sz, boxes=litres/40, tatami=litres/1620*10;
    let numa; if(boxes>=10)numa='底なし沼🌊'; else if(boxes>=4)numa='どっぷり'; else if(boxes>=1)numa='沼入り口'; else numa='まだ浅瀬';
    $('sub2').textContent=`${n}個 × ${sel('size').text}`;
    $('vol').textContent=num(litres)+'L'; $('tatami').textContent=tatami.toFixed(1)+'畳'; $('numa').textContent=numa;
    SHARE=`推しグッズ収納シミュ、私のグッズは収納ケース約${boxes.toFixed(1)}箱分でした📦（${numa}）\\n沼は深い…！あなたは？👇`;
    show(); anim($('big'),0,boxes,900,1);
  }'''))

if __name__=='__main__':
    write_all(SIMS)
    print(f'oshi done. {len(SIMS)} sims.')
