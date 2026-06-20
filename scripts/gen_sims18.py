# -*- coding: utf-8 -*-
"""シミュラボ：美容・ファッションカテゴリ 10本（gen_sims11のTPLを再利用）。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq, write_all

B='美容・ファッション'
SIMS=[]

SIMS.append(dict(id='datsumo-sougaku', cat=B, emoji='🪒',
  title='脱毛の総額シミュレーター｜全身脱毛、結局いくらかかる？｜シミュラボ',
  desc='脱毛したい部位と完了までの回数から、脱毛にかかる総額の目安と1回あたり・分割払いの目安を試算する無料シミュレーター。',
  ogtitle='脱毛の総額シミュレーター｜結局いくらかかる？', ogdesc='部位と回数から脱毛の総額・1回あたり・分割目安を試算。',
  h1='脱毛の総額シミュレーター',
  lead='「脱毛って結局いくら？」を先に把握。部位と完了までの回数から、総額・1回あたり・分割払いの目安を出します。契約前の比較に。',
  inputs='''    <h2>🪒 条件を選ぶ</h2>
    <div class="field"><label>部位</label><select id="part"><option value="20000">全身脱毛</option><option value="8000">顔</option><option value="12000">VIO</option><option value="3000" selected>ワキ</option><option value="9000">腕・脚</option></select></div>
    <div class="field"><label>完了までの回数 <span class="hint">（回・目安5〜8回）</span></label><input type="number" id="n" value="6" min="1" max="20" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">総額を見る</button>''',
  result='''      <div class="label">脱毛の総額の目安</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1回あたり</div><div class="v" id="per">—</div></div>
      <div class="stat"><div class="k">月々(24回払い)</div><div class="v accent" id="m">—</div></div>
      <div class="stat"><div class="k">回数</div><div class="v" id="nv">—</div></div></div>''',
  article='''    <h2>回数の目安</h2>
    <div class="note"><strong>計算式</strong><br>総額 ＝ 1回の料金 × 回数<br>※料金は部位ごとの一般的な目安です。クリニック・サロンで差があります。</div>
    <p>自己処理が楽になるまで5回前後、ツルツルを目指すなら8回以上が目安と言われます。都度払い・回数パック・通い放題で総額が変わるので、回数を入れて比較してみてください。</p>
    <h2>よくある質問</h2>'''+faq([('医療脱毛とサロンの違いは？','医療は効果が高く回数少なめ・1回が高め、サロンは1回安め・回数多めの傾向です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const p=+$('part').value||0, n=Math.max(1,+$('n').value||1);
    const total=p*n;
    $('sub').textContent=`${sel('part').text}・${n}回`;
    $('per').textContent=yen(p); $('m').textContent=yen(total/24); $('nv').textContent=n+'回';
    SHARE=`脱毛の総額シミュ、${sel('part').text}を${n}回で約${yen(total)}でした🪒\\n先に総額を知って賢く選ぼ。👇`;
    show(); anim($('big'),0,total,900);
  }'''))

SIMS.append(dict(id='cosme-nenkan', cat=B, emoji='💄',
  title='コスメ代 年間シミュレーター｜美容にかけてるお金、年いくら？｜シミュラボ',
  desc='毎月のスキンケア・メイク用品の費用から、コスメ代が1年・10年・生涯でいくらになるかを計算する無料シミュレーター。',
  ogtitle='コスメ代 年間シミュレーター｜年いくら？', ogdesc='月のスキンケア・メイク代から、コスメ代を年間で計算。',
  h1='コスメ代 年間シミュレーター',
  lead='毎月のスキンケアとメイク用品、合計すると年でいくら？気づきにくい美容の出費を、年間・生涯で見える化します。',
  inputs='''    <h2>💄 条件を入れる</h2>
    <div class="row"><div class="field"><label>スキンケア <span class="hint">（円/月）</span></label><input type="number" id="skin" value="5000" min="0" inputmode="numeric"></div>
    <div class="field"><label>メイク用品 <span class="hint">（円/月）</span></label><input type="number" id="make" value="3000" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">年間のコスメ代を見る</button>''',
  result='''      <div class="label">年間のコスメ代</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1ヶ月あたり</div><div class="v" id="m">—</div></div>
      <div class="stat"><div class="k">10年で</div><div class="v accent" id="y10">—</div></div>
      <div class="stat"><div class="k">生涯(50年)</div><div class="v" id="life">—</div></div></div>''',
  article='''    <h2>美容費の考え方</h2>
    <div class="note"><strong>計算式</strong><br>年間 ＝（スキンケア ＋ メイク用品）× 12</div>
    <p>美容は自分への投資。ただ無意識に増えがちなので、年単位で把握すると「使うところ・抑えるところ」のメリハリがつけやすくなります。</p>
    <h2>よくある質問</h2>'''+faq([('美容院や脱毛も含む？','このツールはコスメ（化粧品）のみ。美容院や脱毛は別ツールで。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const s=Math.max(0,+$('skin').value||0), m=Math.max(0,+$('make').value||0);
    const year=(s+m)*12;
    $('sub').textContent=`スキンケア${num(s)}＋メイク${num(m)}（月${num(s+m)}円）`;
    $('m').textContent=yen(s+m); $('y10').textContent=yen(year*10); $('life').textContent=yen(year*50);
    SHARE=`コスメ代の年間シミュ、私は年で約${yen(year)}・生涯で${yen(year*50)}でした💄\\n美は一日にしてならず…！👇`;
    show(); anim($('big'),0,year,900);
  }'''))

SIMS.append(dict(id='fuku-shogai', cat=B, emoji='👗',
  title='服の生涯コストシミュレーター｜一生で服にいくら使う？｜シミュラボ',
  desc='毎月の洋服代から、一生で服にかける総額と、買う服の総枚数の目安を計算するエンタメシミュレーター。',
  ogtitle='服の生涯コストシミュレーター｜一生でいくら？', ogdesc='月の服代から、一生の被服費と総枚数を計算。',
  h1='服の生涯コストシミュレーター',
  lead='毎月の洋服代、一生だとどれくらい？被服費の総額と、買う服のだいたいの枚数を出します。クローゼットを見直すきっかけに。',
  inputs='''    <h2>👗 条件を入れる</h2>
    <div class="row"><div class="field"><label>1ヶ月の服代 <span class="hint">（円）</span></label><input type="number" id="m" value="8000" min="0" inputmode="numeric"></div>
    <div class="field"><label>これからの年数 <span class="hint">（年）</span></label><input type="number" id="years" value="50" min="1" max="90" inputmode="numeric"></div></div>
    <div class="field"><label>1着の平均価格 <span class="hint">（円・枚数の計算用）</span></label><input type="number" id="price" value="3000" min="1" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">生涯コストを見る</button>''',
  result='''      <div class="label">一生で服にかけるお金</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">買う服の総数</div><div class="v accent" id="cnt">—</div></div>
      <div class="stat"><div class="k">年間</div><div class="v" id="year">—</div></div>
      <div class="stat"><div class="k">1ヶ月</div><div class="v" id="mv">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>生涯コスト ＝ 月の服代 × 12 × 年数／総枚数 ＝ 生涯コスト ÷ 1着の価格</div>
    <p>「1着を長く着る」「本当に好きな服を買う」だけで、満足度を保ちつつコストは下がります。フリマアプリの活用や、手持ち服の稼働率チェックもおすすめ。</p>
    <h2>よくある質問</h2>'''+faq([('クリーニング代は？','含みません。被服の購入費のみの概算です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const m=Math.max(0,+$('m').value||0), years=Math.max(1,+$('years').value||1), price=Math.max(1,+$('price').value||1);
    const total=m*12*years, cnt=total/price;
    $('sub').textContent=`月${num(m)}円 × 12 × ${years}年`;
    $('cnt').textContent=num(cnt)+'着'; $('year').textContent=yen(m*12); $('mv').textContent=yen(m);
    SHARE=`服の生涯コストシミュ、一生で約${yen(total)}・なんと${num(cnt)}着も買う計算でした👗\\nお気に入りを長く着よ…！👇`;
    show(); anim($('big'),0,total,900);
  }'''))

SIMS.append(dict(id='biyoin-nenkan', cat=B, emoji='💇',
  title='美容院 年間費用シミュレーター｜髪にかけてるお金、年いくら？｜シミュラボ',
  desc='1回の美容院の料金と通う頻度から、美容院代が年間・10年でいくらになるかを計算する無料シミュレーター。',
  ogtitle='美容院 年間費用シミュレーター｜年いくら？', ogdesc='1回の料金と頻度から、美容院代を年間で計算。',
  h1='美容院 年間費用シミュレーター',
  lead='カット、カラー、トリートメント…美容院代って年でいくら？1回の料金と通う頻度から、年間・10年の費用を出します。',
  inputs='''    <h2>💇 条件を入れる</h2>
    <div class="row"><div class="field"><label>1回の料金 <span class="hint">（円）</span></label><input type="number" id="price" value="8000" min="0" inputmode="numeric"></div>
    <div class="field"><label>年に通う回数 <span class="hint">（回）</span></label><input type="number" id="freq" value="6" min="0" max="52" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">年間費用を見る</button>''',
  result='''      <div class="label">美容院の年間費用</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1ヶ月あたり</div><div class="v" id="m">—</div></div>
      <div class="stat"><div class="k">10年で</div><div class="v accent" id="y10">—</div></div>
      <div class="stat"><div class="k">通う間隔</div><div class="v" id="span">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>年間費用 ＝ 1回の料金 × 年の回数</div>
    <p>カラーやパーマを足すと1回の単価が上がります。間隔を少し空ける、メニューを絞る、などで年間ではけっこう変わります。お気に入りの美容師さんとの時間も大事にしつつ、賢く。</p>
    <h2>よくある質問</h2>'''+faq([('セルフカラーと比べたい','1回の料金にセルフ材料費を入れて、頻度を上げて比較してみてください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const price=Math.max(0,+$('price').value||0), freq=Math.max(0,+$('freq').value||0);
    const year=price*freq;
    $('sub').textContent=`${num(price)}円 × 年${freq}回`;
    $('m').textContent=yen(year/12); $('y10').textContent=yen(year*10); $('span').textContent= freq>0?(12/freq).toFixed(1)+'ヶ月に1回':'—';
    SHARE=`美容院の年間費用シミュ、私は年で約${yen(year)}（10年で${yen(year*10)}）でした💇\\nキレイの維持費、大事だなぁ。👇`;
    show(); anim($('big'),0,year,900);
  }'''))

SIMS.append(dict(id='diet-mokuhyou', cat=B, emoji='🥗',
  title='ダイエット目標カロリーシミュレーター｜1日何kcal減らせばいい？｜シミュラボ',
  desc='減らしたい体重と期間から、1日に減らすべきカロリーと週ごとの減量ペースの目安を計算する無料シミュレーター（無理のない範囲で）。',
  ogtitle='ダイエット目標カロリー｜1日何kcal減らす？', ogdesc='目標体重と期間から、1日に必要なカロリー赤字を計算。',
  h1='ダイエット目標カロリーシミュレーター',
  lead='「いつまでに何kg」から、1日にどれくらいカロリーを減らせばいいかを逆算します。無理は禁物——ペースが速すぎる場合は教えてくれます。',
  inputs='''    <h2>🥗 条件を入れる</h2>
    <div class="row"><div class="field"><label>減らしたい体重 <span class="hint">（kg）</span></label><input type="number" id="kg" value="5" min="0" max="50" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>期間 <span class="hint">（ヶ月）</span></label><input type="number" id="months" value="3" min="1" max="36" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">必要カロリーを見る</button>''',
  result='''      <div class="label">1日に減らすカロリー</div>
      <div class="big"><span id="big">0</span><span class="unit">kcal</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">週の減量ペース</div><div class="v accent" id="week">—</div></div>
      <div class="stat"><div class="k">必要な総カロリー</div><div class="v" id="total">—</div></div>
      <div class="stat"><div class="k">ペース判定</div><div class="v" id="judge">—</div></div></div>''',
  article='''    <h2>計算の考え方</h2>
    <div class="note"><strong>計算式</strong><br>体脂肪1kg ≒ 7,200kcal<br>1日の赤字 ＝ 減量kg × 7,200 ÷（期間 × 30.4日）</div>
    <p>健康的な減量ペースは月-1〜2kg（体重の5%以内/月）が目安。食事だけでなく運動を組み合わせると、筋肉を守りながら減らせます。無理な制限はリバウンドのもと。心配な場合は専門家へ。</p>
    <h2>よくある質問</h2>'''+faq([('速いほど良い？','いいえ。急激な減量は健康とリバウンドのリスク。月-2kgまでが目安です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const kg=Math.max(0,+$('kg').value||0), months=Math.max(1,+$('months').value||1);
    const total=kg*7200, perDay=total/(months*30.4), week=kg/(months*4.345);
    let j; if(week<=0.5)j='◎ 無理なし'; else if(week<=1)j='○ 適正'; else j='△ 速すぎかも';
    $('sub').textContent=`${kg}kg を ${months}ヶ月で`;
    $('week').textContent=week.toFixed(2)+'kg/週'; $('total').textContent=num(total)+'kcal'; $('judge').textContent=j;
    SHARE=`ダイエット目標シミュ、${kg}kgを${months}ヶ月なら1日${num(perDay)}kcal減らす計算でした🥗（${j}）\\n無理なくいこ。👇`;
    show(); anim($('big'),0,perDay,900);
  }'''))

SIMS.append(dict(id='nail-matsu', cat=B, emoji='💅',
  title='ネイル・まつエク 年間費用シミュレーター｜指先と目元の維持費は？｜シミュラボ',
  desc='ネイルとまつエクの1回の料金と通う頻度から、年間・10年の維持費を計算する無料シミュレーター。',
  ogtitle='ネイル・まつエク 年間費用｜維持費はいくら？', ogdesc='ネイルとまつエクの料金・頻度から年間維持費を計算。',
  h1='ネイル・まつエク 年間費用シミュレーター',
  lead='指先も目元も、こだわると維持費がかかるもの。ネイルとまつエクの料金と頻度から、年間の維持費を出します。',
  inputs='''    <h2>💅 条件を入れる</h2>
    <div class="row"><div class="field"><label>ネイル1回 <span class="hint">（円）</span></label><input type="number" id="np" value="6000" min="0" inputmode="numeric"></div>
    <div class="field"><label>ネイル 年の回数</label><input type="number" id="nf" value="12" min="0" max="52" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>まつエク1回 <span class="hint">（円）</span></label><input type="number" id="mp" value="5000" min="0" inputmode="numeric"></div>
    <div class="field"><label>まつエク 年の回数</label><input type="number" id="mf" value="9" min="0" max="52" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">年間維持費を見る</button>''',
  result='''      <div class="label">年間の維持費（合計）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">ネイル年間</div><div class="v" id="nv">—</div></div>
      <div class="stat"><div class="k">まつエク年間</div><div class="v" id="mv">—</div></div>
      <div class="stat"><div class="k">10年で</div><div class="v accent" id="y10">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>年間 ＝ ネイル(料金×回数) ＋ まつエク(料金×回数)</div>
    <p>3〜4週間ごとのお直しが一般的。頻度を少し空けたり、長持ちするメニューを選ぶと年間ではけっこう変わります。自分のテンションが上がるなら、立派な投資です。</p>
    <h2>よくある質問</h2>'''+faq([('セルフと比べたい','1回の料金をセルフ材料費にして頻度を上げると比較できます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const np=Math.max(0,+$('np').value||0), nf=Math.max(0,+$('nf').value||0), mp=Math.max(0,+$('mp').value||0), mf=Math.max(0,+$('mf').value||0);
    const nail=np*nf, matsu=mp*mf, total=nail+matsu;
    $('sub').textContent=`ネイル年${nf}回・まつエク年${mf}回`;
    $('nv').textContent=yen(nail); $('mv').textContent=yen(matsu); $('y10').textContent=yen(total*10);
    SHARE=`ネイル・まつエクの年間維持費シミュ、合計で年${yen(total)}でした💅（10年で${yen(total*10)}）\\nキレイの維持費、なかなか…！👇`;
    show(); anim($('big'),0,total,900);
  }'''))

SIMS.append(dict(id='hada-nenrei', cat=B, emoji='✨',
  title='肌年齢診断｜あなたの肌、実年齢より若い？｜シミュラボ',
  desc='睡眠・紫外線対策・保湿・喫煙・水分などの生活習慣から、肌年齢の目安を診断するエンタメシミュレーター。',
  ogtitle='肌年齢診断｜あなたの肌は実年齢より若い？', ogdesc='生活習慣から肌年齢の目安を診断。',
  h1='肌年齢診断',
  lead='同じ年齢でも、習慣で肌の印象は変わります。5つの生活習慣から「肌年齢」の目安を診断します（エンタメ診断・スキンケアのヒントに）。',
  inputs='''    <h2>✨ 生活習慣を選ぶ</h2>
    <div class="field"><label>実年齢 <span class="hint">（歳）</span></label><input type="number" id="age" value="30" min="10" max="100" inputmode="numeric"></div>
    <div class="field"><label>睡眠</label><select id="q1"><option value="-3">毎日しっかり眠れる</option><option value="0" selected>普通</option><option value="3">不足・不規則</option></select></div>
    <div class="field"><label>紫外線対策</label><select id="q2"><option value="-3">毎日日焼け止め</option><option value="0" selected>たまに</option><option value="3">ほぼしない</option></select></div>
    <div class="field"><label>保湿ケア</label><select id="q3"><option value="-2">しっかり</option><option value="0" selected>ふつう</option><option value="2">あまりしない</option></select></div>
    <div class="field"><label>喫煙</label><select id="q4"><option value="0">吸わない</option><option value="2" selected>たまに</option><option value="5">毎日</option></select></div>
    <div class="field"><label>水分・食事のバランス</label><select id="q5"><option value="-2">良い</option><option value="0" selected>普通</option><option value="3">偏りがち</option></select></div>
    <button class="btn btn-primary" id="calcBtn">肌年齢を診断する</button>''',
  result='''      <div class="label">あなたの肌年齢は</div>
      <div class="big"><span id="big">0</span><span class="unit">歳</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:18px;">—</div>''',
  article='''    <h2>肌年齢を左右する習慣</h2>
    <p>肌の老化の大きな原因は紫外線と乾燥、そして睡眠不足・喫煙と言われます。本診断はそれを簡易点数化したエンタメです。気になる項目から、できることを少しずつ。</p>
    <div class="note">💡 いちばん効くのは「日焼け止め」と「睡眠」。今日からできる対策で、肌年齢は変えられます。</div>
    <h2>よくある質問</h2>'''+faq([('医学的な数値ですか？','いいえ。生活習慣から目安を出すエンタメ診断です。気になる肌悩みは専門家へ。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const age=Math.max(10,+$('age').value||10);
    let d=0; for(const id of ['q1','q2','q3','q4','q5']) d+=(+$(id).value||0);
    const skin=Math.max(12,Math.round(age+d)), gap=skin-age;
    let a; if(gap<=-3)a='うらやましい若肌！今のケアを続けて✨'; else if(gap<=1)a='実年齢相応。日焼け止めと睡眠でさらに若返りも。'; else a='少しお疲れ肌かも。まずは紫外線対策と保湿から見直してみて。';
    $('sub').textContent=`実年齢${age}歳 → 肌年齢${skin}歳（${gap>=0?'+':''}${gap}歳）`;
    $('adv').textContent='✨ '+a;
    SHARE=`肌年齢診断、実年齢${age}歳に対して肌年齢は${skin}歳でした✨\\n${gap<=0?'若肌キープ！':'スキンケア見直そ…'}あなたは？👇`;
    show(); anim($('big'),0,skin,900);
  }'''))

SIMS.append(dict(id='wardrobe', cat=B, emoji='👚',
  title='クローゼット稼働率シミュレーター｜持ってる服、ちゃんと着てる？｜シミュラボ',
  desc='持っている服の数とよく着る服の数から、クローゼットの稼働率と「死蔵している服」の数・割合を可視化する無料シミュレーター。',
  ogtitle='クローゼット稼働率｜持ってる服、着てる？', ogdesc='持ってる服とよく着る服から、稼働率と死蔵率を可視化。',
  h1='クローゼット稼働率シミュレーター',
  lead='クローゼットはパンパンなのに「着る服がない」——その正体は稼働率かも。持っている服とよく着る服の数から、稼働率と死蔵率を出します。',
  inputs='''    <h2>👚 条件を入れる</h2>
    <div class="row"><div class="field"><label>持っている服の数 <span class="hint">（着・ざっくり）</span></label><input type="number" id="have" value="80" min="1" inputmode="numeric"></div>
    <div class="field"><label>よく着る服の数 <span class="hint">（着）</span></label><input type="number" id="wear" value="20" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">稼働率を見る</button>''',
  result='''      <div class="label">クローゼットの稼働率</div>
      <div class="big"><span id="big">0</span><span class="unit">%</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">死蔵している服</div><div class="v accent" id="dead">—</div></div>
      <div class="stat"><div class="k">死蔵率</div><div class="v" id="deadr">—</div></div>
      <div class="stat"><div class="k">判定</div><div class="v" id="judge">—</div></div></div>''',
  article='''    <h2>稼働率とは</h2>
    <div class="note"><strong>計算式</strong><br>稼働率 ＝ よく着る服 ÷ 持っている服 ×100</div>
    <p>「服の8割は、2割のお気に入りで着回している」とよく言われます（パレートの法則）。稼働率が低いなら、死蔵服を手放すとクローゼットも気持ちもスッキリ。フリマアプリでお小遣いにも。</p>
    <h2>よくある質問</h2>'''+faq([('理想の稼働率は？','決まりはありませんが、5割を超えると「着回せている」感覚になりやすいです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const have=Math.max(1,+$('have').value||1), wear=Math.max(0,Math.min(have,+$('wear').value||0));
    const rate=wear/have*100, dead=have-wear, dr=dead/have*100;
    let j; if(rate>=60)j='よく着回せてる◎'; else if(rate>=35)j='まずまず'; else j='死蔵多め…整理どき';
    $('sub').textContent=`${have}着中 ${wear}着をよく着る`;
    $('dead').textContent=num(dead)+'着'; $('deadr').textContent=Math.round(dr)+'%'; $('judge').textContent=j;
    SHARE=`クローゼット稼働率シミュ、私は${Math.round(rate)}%（死蔵${num(dead)}着）でした👚（${j}）\\n衣替えで見直そ…！👇`;
    show(); anim($('big'),0,rate,900);
  }'''))

SIMS.append(dict(id='kami-nobiru', cat=B, emoji='✂️',
  title='髪が伸びるまでシミュレーター｜目標の長さまであと何ヶ月？｜シミュラボ',
  desc='今の髪の長さと目標の長さから、髪が伸びるまでにかかる月数の目安を計算する無料シミュレーター。',
  ogtitle='髪が伸びるまで｜目標の長さまで何ヶ月？', ogdesc='今の長さと目標から、髪が伸びるまでの月数を計算。',
  h1='髪が伸びるまでシミュレーター',
  lead='伸ばしたいけど、いつになる？今の髪の長さと目標の長さから、伸びるまでの月数を計算します（髪は1ヶ月に約1.2cm伸びます）。',
  inputs='''    <h2>✂️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>今の長さ <span class="hint">（cm）</span></label><input type="number" id="now" value="20" min="0" max="150" inputmode="numeric"></div>
    <div class="field"><label>目標の長さ <span class="hint">（cm）</span></label><input type="number" id="goal" value="40" min="0" max="150" inputmode="numeric"></div></div>
    <div class="field"><label>伸びる速さ <span class="hint">（cm/月・標準1.2）</span></label><input type="number" id="rate" value="1.2" min="0.5" max="2" step="0.1" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">何ヶ月か見る</button>''',
  result='''      <div class="label">目標の長さまで</div>
      <div class="big"><span id="big">0</span><span class="unit">ヶ月</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">伸ばす長さ</div><div class="v" id="diff">—</div></div>
      <div class="stat"><div class="k">年にすると</div><div class="v accent" id="year">—</div></div>
      <div class="stat"><div class="k">1年で伸びる</div><div class="v" id="peryear">—</div></div></div>''',
  article='''    <h2>髪が伸びる速さ</h2>
    <div class="note"><strong>計算式</strong><br>かかる月数 ＝（目標 − 今）÷ 1ヶ月に伸びる長さ<br>髪は平均で1ヶ月約1.2cm（年14cmほど）伸びます。</div>
    <p>伸ばす途中は毛先のケアが大事。栄養・睡眠・頭皮環境も伸びやすさに関わると言われます。途中の「中途半端期」を乗り越えれば理想の長さに。</p>
    <h2>よくある質問</h2>'''+faq([('もっと早く伸ばせる？','個人差はありますが、平均は月1.2cm前後。健康的な生活が近道です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const now=Math.max(0,+$('now').value||0), goal=Math.max(0,+$('goal').value||0), rate=Math.max(0.1,+$('rate').value||1.2);
    const diff=Math.max(0,goal-now), months=diff/rate;
    $('sub').textContent=`${now}cm → ${goal}cm（${rate}cm/月）`;
    $('diff').textContent=diff.toFixed(0)+'cm'; $('year').textContent=(months/12).toFixed(1)+'年'; $('peryear').textContent=(rate*12).toFixed(0)+'cm';
    SHARE=`髪が伸びるまでシミュ、今${now}cmから${goal}cmまで約${Math.ceil(months)}ヶ月でした✂️\\nコツコツ伸ばそ…！👇`;
    show(); anim($('big'),0,months,900);
  }'''))

SIMS.append(dict(id='depacos', cat=B, emoji='💋',
  title='デパコス vs プチプラ 生涯差シミュレーター｜どれだけ差がつく？｜シミュラボ',
  desc='デパコスとプチプラの毎月のコスメ代から、一生でどれだけ差がつくかを計算するエンタメシミュレーター。',
  ogtitle='デパコス vs プチプラ｜生涯でどれだけ差？', ogdesc='デパコスとプチプラの月額から、生涯の差額を計算。',
  h1='デパコス vs プチプラ 生涯差シミュレーター',
  lead='デパコス派とプチプラ派、一生だとどれくらい差がつく？毎月のコスメ代から、生涯の差額を出します（どっちが正解、はありません）。',
  inputs='''    <h2>💋 条件を入れる</h2>
    <div class="row"><div class="field"><label>デパコス <span class="hint">（円/月）</span></label><input type="number" id="depa" value="15000" min="0" inputmode="numeric"></div>
    <div class="field"><label>プチプラ <span class="hint">（円/月）</span></label><input type="number" id="puchi" value="4000" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>これからの年数 <span class="hint">（年）</span></label><input type="number" id="years" value="50" min="1" max="90" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">生涯差を見る</button>''',
  result='''      <div class="label">一生で生まれる差額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">デパコス生涯</div><div class="v" id="dv">—</div></div>
      <div class="stat"><div class="k">プチプラ生涯</div><div class="v accent" id="pv">—</div></div>
      <div class="stat"><div class="k">月の差</div><div class="v" id="md">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>生涯 ＝ 月額 × 12 × 年数／差額 ＝ デパコス − プチプラ</div>
    <p>デパコスは満足度や肌悩みへの効果、プチプラはコスパと気軽さが魅力。大事なのは「自分が納得して使えるか」。差額を知ったうえで、賢く組み合わせるのが◎。</p>
    <h2>よくある質問</h2>'''+faq([('どっちがいい？','正解はありません。効きを感じるアイテムはデパコス、消耗品はプチプラ、の使い分けも人気です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const depa=Math.max(0,+$('depa').value||0), puchi=Math.max(0,+$('puchi').value||0), years=Math.max(1,+$('years').value||1);
    const dv=depa*12*years, pv=puchi*12*years, diff=Math.abs(dv-pv);
    $('sub').textContent=`月 デパコス${num(depa)}／プチプラ${num(puchi)}・${years}年`;
    $('dv').textContent=yen(dv); $('pv').textContent=yen(pv); $('md').textContent=yen(Math.abs(depa-puchi));
    SHARE=`デパコス vs プチプラ、一生で約${yen(diff)}もの差がつく計算でした💋\\n使い分けが賢いのかも。あなたは？👇`;
    show(); anim($('big'),0,diff,900);
  }'''))

if __name__=='__main__':
    write_all(SIMS)
    print(f'beauty done. {len(SIMS)} sims.')
