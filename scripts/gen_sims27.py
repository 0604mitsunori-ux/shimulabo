# -*- coding: utf-8 -*-
"""シミュラボ：シニア・終活・介護カテゴリ 10本（gen_sims11のTPLを再利用）。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq, write_all

S = 'シニア・終活・介護'
SIMS = []
def add(**k): SIMS.append(k)

add(id='shukatsu-sougaku', cat=S, emoji='🕊️',
  title='終活 総費用シミュレーター｜終活、全部でいくら備える？｜シミュラボ',
  desc='お墓・葬儀・生前整理・遺言などの費用から、終活にかかる総額の目安を試算する無料シミュレーター。',
  ogtitle='終活 総費用シミュレーター｜全部でいくら？', ogdesc='お墓・葬儀・生前整理・遺言から終活の総額を試算。',
  h1='終活 総費用シミュレーター',
  lead='お墓に葬儀、生前整理、遺言…終活にはいくら備えればいい？項目ごとの費用から、総額の目安を出します。家族に負担を残さない準備の第一歩に。',
  inputs='''    <h2>🕊️ 費用を入れる</h2>
    <div class="row"><div class="field"><label>葬儀費用 <span class="hint">（万円）</span></label><input type="number" id="sougi" value="120" min="0" inputmode="numeric"></div>
    <div class="field"><label>お墓・納骨 <span class="hint">（万円）</span></label><input type="number" id="ohaka" value="100" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>生前整理・遺品 <span class="hint">（万円）</span></label><input type="number" id="seiri" value="30" min="0" inputmode="numeric"></div>
    <div class="field"><label>遺言・その他 <span class="hint">（万円）</span></label><input type="number" id="other" value="20" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">総額を見る</button>''',
  result='''      <div class="label">終活の総費用</div>
      <div class="big"><span id="big">0</span><span class="unit">万円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">月3万積立なら</div><div class="v accent" id="tsumi">—</div></div>
      <div class="stat"><div class="k">葬儀＋お墓</div><div class="v" id="big2">—</div></div>
      <div class="stat"><div class="k">内訳件数</div><div class="v" id="n">—</div></div></div>''',
  article='''    <h2>終活の費用の考え方</h2>
    <div class="note"><strong>計算式</strong><br>総額 ＝ 葬儀 ＋ お墓・納骨 ＋ 生前整理 ＋ 遺言・その他</div>
    <p>近年は家族葬や永代供養で費用を抑える選択も増えています。早めに備えておくと、家族の経済的・精神的な負担を大きく減らせます。エンディングノートで希望を整理するのもおすすめ。</p>
    <h2>よくある質問</h2>'''+faq([('相場はどれくらい？','葬儀100〜200万、お墓50〜200万が目安。形式で大きく変わります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const a=Math.max(0,+$('sougi').value||0),b=Math.max(0,+$('ohaka').value||0),c=Math.max(0,+$('seiri').value||0),d=Math.max(0,+$('other').value||0);const t=a+b+c+d;
    $('sub').textContent=`葬儀${a}＋お墓${b}＋整理${c}＋遺言${d}万`;$('tsumi').textContent=num(t/0.36)+'ヶ月';$('big2').textContent=num(a+b)+'万円';$('n').textContent='4項目';
    SHARE=`終活 総費用シミュ、備えの目安は約${num(t)}万円でした🕊️ 早めの準備が家族を守る。`;show();anim($('big'),0,t,800);}''')

add(id='ohaka-hiyou', cat=S, emoji='⛩️',
  title='お墓の費用比較シミュレーター｜墓石・永代供養・樹木葬どれが安い？｜シミュラボ',
  desc='墓石・永代供養・納骨堂・樹木葬・散骨など、供養の形ごとの費用の目安を比較できる無料シミュレーター。',
  ogtitle='お墓の費用比較｜どの供養が安い？', ogdesc='墓石・永代供養・樹木葬など供養の形別に費用を比較。',
  h1='お墓の費用比較シミュレーター',
  lead='お墓にもいろいろな形があります。墓石・永代供養・納骨堂・樹木葬・散骨の費用を比べて、家族に合った供養を考える参考に。',
  inputs='''    <h2>⛩️ 供養の形を選ぶ</h2>
    <div class="field"><label>供養の形</label><select id="type"><option value="180">一般墓（墓石）</option><option value="70" selected>永代供養墓</option><option value="90">納骨堂</option><option value="50">樹木葬</option><option value="15">散骨</option></select></div>
    <div class="field"><label>年間の管理費 <span class="hint">（円・かかる場合）</span></label><input type="number" id="kanri" value="10000" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">費用を見る</button>''',
  result='''      <div class="label">初期費用の目安</div>
      <div class="big"><span id="big">0</span><span class="unit">万円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">一般墓との差</div><div class="v accent" id="diff">—</div></div>
      <div class="stat"><div class="k">20年の管理費</div><div class="v" id="kanri2">—</div></div>
      <div class="stat"><div class="k">タイプ</div><div class="v" id="tv">—</div></div></div>''',
  article='''    <h2>供養の形と費用</h2>
    <div class="note"><strong>目安</strong><br>一般墓150〜250万／納骨堂50〜150万／永代供養50〜100万／樹木葬30〜70万／散骨5〜30万</div>
    <p>承継者がいない・子に負担をかけたくない場合は、管理不要の永代供養・樹木葬・散骨が選ばれています。費用だけでなく、お参りのしやすさや家族の気持ちも大切に選びましょう。</p>
    <h2>よくある質問</h2>'''+faq([('管理費は？','一般墓・納骨堂は年間管理費がかかることが多いです。永代供養は不要な場合も。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const t=+$('type').value||0,k=Math.max(0,+$('kanri').value||0);
    $('sub').textContent=`${sel('type').text}`;$('diff').textContent=(t-180)+'万円';$('kanri2').textContent=yen(k*20);$('tv').textContent=sel('type').text;
    SHARE=`お墓の費用比較シミュ、${sel('type').text}は初期費用 約${t}万円でした⛩️`;show();anim($('big'),0,t,800);}''')

add(id='sougi-hiyou', cat=S, emoji='🌸',
  title='葬儀費用シミュレーター｜家族葬・一般葬・直葬の費用は？｜シミュラボ',
  desc='葬儀の形式（直葬・家族葬・一般葬）と参列者数から、葬儀費用の目安と香典で戻る分を試算する無料シミュレーター。',
  ogtitle='葬儀費用シミュレーター｜形式別の費用は？', ogdesc='直葬・家族葬・一般葬と参列者数から葬儀費用を試算。',
  h1='葬儀費用シミュレーター',
  lead='葬儀の形式と参列者数から、費用の目安を試算します。香典でまかなえる分も計算するので、実際の自己負担が分かります。',
  inputs='''    <h2>🌸 条件を選ぶ</h2>
    <div class="field"><label>葬儀の形式</label><select id="type"><option value="20">直葬・火葬式</option><option value="100" selected>家族葬</option><option value="180">一般葬</option></select></div>
    <div class="row"><div class="field"><label>参列者数 <span class="hint">（人）</span></label><input type="number" id="n" value="30" min="0" inputmode="numeric"></div>
    <div class="field"><label>1人あたり香典 <span class="hint">（円）</span></label><input type="number" id="koden" value="7000" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">費用を見る</button>''',
  result='''      <div class="label">葬儀費用の目安</div>
      <div class="big"><span id="big">0</span><span class="unit">万円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">香典の合計</div><div class="v" id="kd">—</div></div>
      <div class="stat"><div class="k">実質の自己負担</div><div class="v accent" id="jiko">—</div></div>
      <div class="stat"><div class="k">飲食・返礼込み</div><div class="v" id="meal">—</div></div></div>''',
  article='''    <h2>葬儀費用の内訳</h2>
    <div class="note"><strong>計算の考え方</strong><br>総額 ＝ 基本費用（形式別）＋ 参列者数 × 飲食・返礼（1人約5千円）<br>自己負担 ＝ 総額 − 香典の合計</div>
    <p>近年は家族葬が主流に。参列者が多いと飲食・返礼が増えますが、香典も増えるため自己負担は形式で大きく変わります。見積もりは複数社の比較を。</p>
    <h2>よくある質問</h2>'''+faq([('香典返しは？','香典の3〜5割が目安。本ツールは飲食・返礼を1人5千円で概算しています。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const base=+$('type').value||0,n=Math.max(0,+$('n').value||0),k=Math.max(0,+$('koden').value||0);
    const meal=n*5000, total=base*10000+meal, koden=n*k, jiko=Math.max(0,total-koden);
    $('sub').textContent=`${sel('type').text}・参列${n}人`;$('kd').textContent=yen(koden);$('jiko').textContent=yen(jiko);$('meal').textContent=yen(meal);
    SHARE=`葬儀費用シミュ、${sel('type').text}の総額 約${num(total/10000)}万円・香典差引の自己負担は約${yen(jiko)}でした🌸`;show();anim($('big'),0,total/10000,800);}''')

add(id='kaigo-hiyou', cat=S, emoji='🧓',
  title='介護費用シミュレーター｜在宅 vs 施設、生涯でいくら？｜シミュラボ',
  desc='在宅介護と施設介護の月額費用と介護期間から、生涯の介護費用を比較する無料シミュレーター。',
  ogtitle='介護費用シミュレーター｜在宅vs施設の生涯費用', ogdesc='在宅と施設の月額と期間から生涯の介護費用を比較。',
  h1='介護費用シミュレーター',
  lead='介護は在宅か施設かで費用が大きく変わります。月額と介護期間から、生涯の介護費用を比較。早めに備えておくための目安に。',
  inputs='''    <h2>🧓 条件を入れる</h2>
    <div class="row"><div class="field"><label>在宅介護 <span class="hint">（円/月）</span></label><input type="number" id="zaitaku" value="50000" min="0" inputmode="numeric"></div>
    <div class="field"><label>施設介護 <span class="hint">（円/月）</span></label><input type="number" id="shisetsu" value="200000" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>介護期間 <span class="hint">（年・平均約5年）</span></label><input type="number" id="years" value="5" min="0" max="30" step="0.5" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">生涯費用を見る</button>''',
  result='''      <div class="label" id="lab">施設介護の生涯費用</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">在宅の生涯費用</div><div class="v" id="zv">—</div></div>
      <div class="stat"><div class="k">在宅と施設の差</div><div class="v accent" id="diff">—</div></div>
      <div class="stat"><div class="k">介護期間</div><div class="v" id="yv">—</div></div></div>''',
  article='''    <h2>介護費用の備え</h2>
    <div class="note"><strong>計算式</strong><br>生涯費用 ＝ 月額 × 12 × 介護期間（介護保険の自己負担後の目安）</div>
    <p>介護期間は平均約5年と言われますが、長くなることも。施設は費用が高い分、家族の負担は軽くなります。介護保険・高額介護サービス費の制度も活用を。一時金として別ツールの試算も参考に。</p>
    <h2>よくある質問</h2>'''+faq([('一時金は？','有料老人ホームは入居一時金が別途かかる場合があります。月額に加えて検討を。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const z=Math.max(0,+$('zaitaku').value||0),s=Math.max(0,+$('shisetsu').value||0),y=Math.max(0,+$('years').value||0);
    const zt=z*12*y, st=s*12*y;
    $('sub').textContent=`月 在宅${num(z)}／施設${num(s)}・${y}年`;$('zv').textContent=yen(zt);$('diff').textContent=yen(Math.abs(st-zt));$('yv').textContent=y+'年';
    SHARE=`介護費用シミュ、${y}年で在宅${yen(zt)}・施設${yen(st)}でした🧓 備えは早めに。`;show();anim($('big'),0,st,800);}''')

add(id='nenkin-kurisage', cat=S, emoji='📈',
  title='年金繰下げ受給シミュレーター｜何歳まで生きれば得？損益分岐｜シミュラボ',
  desc='年金の繰下げ受給による増額率と、繰下げない場合との損益分岐年齢を計算する無料シミュレーター。',
  ogtitle='年金繰下げ受給｜何歳まで生きれば得？', ogdesc='繰下げ受給の増額率と損益分岐年齢を計算。',
  h1='年金繰下げ受給シミュレーター',
  lead='年金を遅らせて受け取ると毎月の額が増えます（1ヶ月0.7%）。何歳まで生きれば「繰下げてよかった」になるか、損益分岐の年齢を計算します。',
  inputs='''    <h2>📈 条件を入れる</h2>
    <div class="row"><div class="field"><label>65歳開始の年金 <span class="hint">（円/月）</span></label><input type="number" id="m" value="150000" min="0" inputmode="numeric"></div>
    <div class="field"><label>繰下げる年齢 <span class="hint">（歳・66〜75）</span></label><input type="number" id="age" value="70" min="66" max="75" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">損益分岐を見る</button>''',
  result='''      <div class="label">損益分岐の年齢</div>
      <div class="big"><span id="big">0</span><span class="unit">歳</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">繰下げ後の月額</div><div class="v accent" id="newm">—</div></div>
      <div class="stat"><div class="k">増額率</div><div class="v" id="rate">—</div></div>
      <div class="stat"><div class="k">これより長生きで得</div><div class="v" id="note2">—</div></div></div>''',
  article='''    <h2>繰下げ受給のしくみ</h2>
    <div class="note"><strong>計算式</strong><br>増額率 ＝ 0.7% × 繰下げた月数（最大75歳で+84%）<br>損益分岐年齢 ＝ 受給開始年齢 ＋（受け取らなかった年数 ÷ 増額割合）</div>
    <p>繰下げると毎月の年金は増えますが、その分受け取り開始が遅れます。損益分岐の年齢より長生きすれば「繰下げて得」。健康状態やほかの収入とあわせて判断しましょう（税・社会保険料は考慮外の概算）。</p>
    <h2>よくある質問</h2>'''+faq([('繰上げ（早める）は？','60歳まで早められますが、1ヶ月0.4%減額されます（最大-24%）。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const m=Math.max(0,+$('m').value||0),age=Math.max(66,Math.min(75,+$('age').value||66));
    const months=(age-65)*12, rate=0.007*months, newm=m*(1+rate);
    const breakeven=age + (65*0+ ( (age-65)*m*12 ) / (newm*12 - m*12) );
    $('sub').textContent=`${age}歳まで繰下げ（${months}ヶ月）`;$('newm').textContent=yen(newm);$('rate').textContent='+'+(rate*100).toFixed(1)+'%';$('note2').textContent=breakeven.toFixed(0)+'歳〜';
    SHARE=`年金繰下げ受給シミュ、${age}歳まで繰下げると月額${yen(newm)}（+${(rate*100).toFixed(0)}%）、損益分岐は約${breakeven.toFixed(0)}歳でした📈`;show();anim($('big'),0,breakeven,800);}''')

add(id='seizen-zoyo', cat=S, emoji='🎁',
  title='生前贈与シミュレーター｜暦年贈与で無税で渡せる総額は？｜シミュラボ',
  desc='年間110万円の非課税枠を使った暦年贈与で、何年・何人に無税で渡せる総額と相続税の圧縮効果を試算する無料シミュレーター。',
  ogtitle='生前贈与シミュレーター｜無税で渡せる総額は？', ogdesc='暦年贈与で無税で渡せる総額と相続税圧縮を試算。',
  h1='生前贈与シミュレーター',
  lead='年間110万円までの贈与は非課税（暦年贈与）。計画的に贈ると、無税で財産を渡しつつ相続財産を減らせます。何年・何人で総額いくら渡せるかを計算します。',
  inputs='''    <h2>🎁 条件を入れる</h2>
    <div class="row"><div class="field"><label>1人に毎年贈る額 <span class="hint">（万円・110まで非課税）</span></label><input type="number" id="m" value="110" min="0" max="110" inputmode="numeric"></div>
    <div class="field"><label>贈る相手の人数 <span class="hint">（人）</span></label><input type="number" id="n" value="2" min="1" inputmode="numeric"></div></div>
    <div class="field"><label>続ける年数 <span class="hint">（年）</span></label><input type="number" id="years" value="10" min="1" max="30" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">無税で渡せる総額を見る</button>''',
  result='''      <div class="label">無税で渡せる総額</div>
      <div class="big"><span id="big">0</span><span class="unit">万円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1年あたり</div><div class="v" id="y1">—</div></div>
      <div class="stat"><div class="k">相続財産の圧縮</div><div class="v accent" id="atsu">—</div></div>
      <div class="stat"><div class="k">人数×年数</div><div class="v" id="ny">—</div></div></div>''',
  article='''    <h2>暦年贈与のしくみ</h2>
    <div class="note"><strong>計算式</strong><br>無税の総額 ＝ 1人110万円以内 × 人数 × 年数</div>
    <p>受け取る人ごとに年間110万円まで贈与税がかかりません。長期間・複数人に計画的に贈ると、相続財産を減らして相続税を抑えられます。※名義預金とみなされないよう、贈与契約・記録が大切。制度改正もあるため専門家に相談を。</p>
    <h2>よくある質問</h2>'''+faq([('110万を超えたら？','超えた分に贈与税がかかります（贈与税シミュで確認を）。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const m=Math.max(0,Math.min(110,+$('m').value||0)),n=Math.max(1,+$('n').value||1),y=Math.max(1,+$('years').value||1);
    const total=m*n*y;
    $('sub').textContent=`1人${m}万 × ${n}人 × ${y}年`;$('y1').textContent=num(m*n)+'万円';$('atsu').textContent=num(total)+'万円';$('ny').textContent=(n*y)+'回';
    SHARE=`生前贈与シミュ、${y}年で無税で約${num(total)}万円渡せる計算でした🎁 相続対策に。`;show();anim($('big'),0,total,800);}''')

add(id='kougaku-ryoyo', cat=S, emoji='🏥',
  title='高額療養費シミュレーター｜医療費の自己負担はいくらで止まる？｜シミュラボ',
  desc='1ヶ月の医療費と所得区分から、高額療養費制度による自己負担の上限額と払い戻しの目安を計算する無料シミュレーター。',
  ogtitle='高額療養費シミュレーター｜自己負担の上限は？', ogdesc='医療費と所得区分から高額療養費の自己負担上限を計算。',
  h1='高額療養費シミュレーター',
  lead='医療費が高額でも、「高額療養費制度」で自己負担には上限があります。1ヶ月の医療費と所得区分から、実際の自己負担額と戻ってくる目安を計算します。',
  inputs='''    <h2>🏥 条件を入れる</h2>
    <div class="field"><label>1ヶ月の医療費（総額・10割） <span class="hint">（円）</span></label><input type="number" id="hi" value="1000000" min="0" inputmode="numeric"></div>
    <div class="field"><label>所得区分（年収目安）</label><select id="kubun"><option value="low">〜約370万（一般・低）</option><option value="mid" selected>約370〜770万（一般）</option><option value="high">約770〜1160万</option></select></div>
    <button class="btn btn-primary" id="calcBtn">自己負担を見る</button>''',
  result='''      <div class="label">実際の自己負担（上限後）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">3割負担額</div><div class="v" id="san">—</div></div>
      <div class="stat"><div class="k">戻ってくる目安</div><div class="v accent" id="back">—</div></div>
      <div class="stat"><div class="k">区分</div><div class="v" id="kv">—</div></div></div>''',
  article='''    <h2>高額療養費制度</h2>
    <div class="note"><strong>自己負担の上限（70歳未満の目安）</strong><br>一般（年収〜370万）＝57,600円<br>一般（370〜770万）＝80,100円＋(医療費−267,000)×1%<br>770〜1160万＝167,400円＋(医療費−558,000)×1%</div>
    <p>窓口で3割払っても、上限を超えた分は後で払い戻されます（限度額適用認定証があれば窓口で上限まで）。高額な治療・入院でも、自己負担には歯止めがある安心な制度です。本ツールは目安です。</p>
    <h2>よくある質問</h2>'''+faq([('多数該当は？','直近12ヶ月で3回以上該当すると4回目から上限がさらに下がります（本ツールは初回の目安）。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const hi=Math.max(0,+$('hi').value||0),k=$('kubun').value;
    const san=hi*0.3; let cap;
    if(k==='low')cap=57600; else if(k==='mid')cap=80100+Math.max(0,(hi-267000))*0.01; else cap=167400+Math.max(0,(hi-558000))*0.01;
    const jiko=Math.min(san,cap), back=Math.max(0,san-jiko);
    $('sub').textContent=`医療費${num(hi)}円・${sel('kubun').text}`;$('san').textContent=yen(san);$('back').textContent=yen(back);$('kv').textContent=sel('kubun').text;
    SHARE=`高額療養費シミュ、3割なら${yen(san)}でも上限で自己負担は約${yen(jiko)}に🏥 知っておくと安心。`;show();anim($('big'),0,jiko,800);}''')

add(id='ending-do', cat=S, emoji='📒',
  title='終活準備度チェック｜あなたの終活、どこまで進んでる？｜シミュラボ',
  desc='エンディングノート・遺言・財産整理・お墓・延命などの準備状況から、終活の進み具合を診断し、次にやることを提案する無料チェック。',
  ogtitle='終活準備度チェック｜どこまで進んでる？', ogdesc='終活の準備状況を診断し、次にやることを提案。',
  h1='終活準備度チェック',
  lead='終活、何から手をつければいい？6つの項目で準備度をチェックし、次に取り組むべきことをお伝えします。家族のためにも、自分の安心のためにも一歩ずつ。',
  inputs='''    <h2>📒 準備状況を選ぶ</h2>
    <div class="field"><label>エンディングノート</label><select id="q1"><option value="2">書いてある</option><option value="1" selected>少し</option><option value="0">まだ</option></select></div>
    <div class="field"><label>財産・口座の整理</label><select id="q2"><option value="2">一覧化済み</option><option value="1" selected>把握はしている</option><option value="0">まだ</option></select></div>
    <div class="field"><label>遺言書</label><select id="q3"><option value="2">作成済み</option><option value="1" selected>検討中</option><option value="0">まだ</option></select></div>
    <div class="field"><label>お墓・葬儀の希望</label><select id="q4"><option value="2">決めて伝えてある</option><option value="1" selected>考えている</option><option value="0">まだ</option></select></div>
    <div class="field"><label>医療・延命の意思</label><select id="q5"><option value="2">家族に伝えてある</option><option value="1" selected>考えている</option><option value="0">まだ</option></select></div>
    <div class="field"><label>不要品・生前整理</label><select id="q6"><option value="2">進めている</option><option value="1" selected>少し</option><option value="0">まだ</option></select></div>
    <button class="btn btn-primary" id="calcBtn">準備度を診断する</button>''',
  result='''      <div class="label">終活の準備度</div>
      <div class="big"><span id="big">0</span><span class="unit">%</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:18px;">—</div>''',
  article='''    <h2>終活の進め方</h2>
    <p>終活は「エンディングノートを書く→財産を整理する→希望（医療・葬儀・お墓）を家族に伝える→遺言を整える」の順で進めるとスムーズです。一度に全部やろうとせず、できることから少しずつ。家族との会話のきっかけにもなります。</p>
    <div class="note">💡 まずはエンディングノートから。市販品や自治体の無料配布もあります。</div>
    <h2>よくある質問</h2>'''+faq([('何歳から始める？','決まりはありません。元気なうちに少しずつ始めるのが安心です。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  js='''  function calc(){let s=0;for(const id of ['q1','q2','q3','q4','q5','q6'])s+=(+$(id).value||0);const pct=Math.round(s/12*100);
    let a;if(pct>=80)a='しっかり準備が進んでいます。定期的な見直しを忘れずに📒';else if(pct>=45)a='良いペース。遺言や希望の共有など、残りの項目も少しずつ。';else a='これからですね。まずはエンディングノートと財産の把握から始めてみましょう。';
    $('sub').textContent='6項目のチェック結果';$('adv').textContent='📒 '+a;
    SHARE=`終活準備度チェック、私の準備度は${pct}%でした📒 できることから少しずつ。`;show();anim($('big'),0,pct,800);}''')

add(id='kenkou-jumyo', cat=S, emoji='🌿',
  title='健康寿命シミュレーター｜元気に過ごせる時間はあと何年？｜シミュラボ',
  desc='今の年齢から、平均寿命・健康寿命までの残り時間を計算し、元気に動ける期間を意識できるエンタメシミュレーター。',
  ogtitle='健康寿命シミュレーター｜元気な時間はあと何年？', ogdesc='年齢から平均寿命・健康寿命までの残り時間を計算。',
  h1='健康寿命シミュレーター',
  lead='「健康寿命」は、介護を必要とせず元気に過ごせる年齢のこと。今の年齢から、平均寿命までと健康寿命までの残り時間を出します。今を大切にするきっかけに。',
  inputs='''    <h2>🌿 条件を入れる</h2>
    <div class="row"><div class="field"><label>今の年齢 <span class="hint">（歳）</span></label><input type="number" id="age" value="60" min="0" max="110" inputmode="numeric"></div>
    <div class="field"><label>性別</label><select id="sex"><option value="m">男性</option><option value="f" selected>女性</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">残り時間を見る</button>''',
  result='''      <div class="label">健康寿命まで（元気な時間）</div>
      <div class="big"><span id="big">0</span><span class="unit">年</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">平均寿命まで</div><div class="v accent" id="life">—</div></div>
      <div class="stat"><div class="k">元気な日数</div><div class="v" id="days">—</div></div>
      <div class="stat"><div class="k">健康寿命の目安</div><div class="v" id="kj">—</div></div></div>''',
  article='''    <h2>健康寿命とは</h2>
    <div class="note"><strong>目安（日本の平均）</strong><br>平均寿命：男81歳・女87歳／健康寿命：男73歳・女75歳<br>残り＝目安の年齢 − 今の年齢</div>
    <p>平均寿命と健康寿命の差（男約9年・女約12年）は、何らかのサポートが必要な期間。運動・食事・社会とのつながりで健康寿命は延ばせると言われます。元気に動ける時間を大切に、やりたいことを今のうちに。</p>
    <h2>よくある質問</h2>'''+faq([('あくまで平均？','はい。個人差が大きい目安です。前向きに使ってください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const age=Math.max(0,+$('age').value||0),sex=$('sex').value;
    const life=sex==='m'?81:87, kj=sex==='m'?73:75;
    const toKj=Math.max(0,kj-age), toLife=Math.max(0,life-age);
    $('sub').textContent=`${age}歳・${sex==='m'?'男性':'女性'}`;$('life').textContent=toLife+'年';$('days').textContent=num(toKj*365)+'日';$('kj').textContent=kj+'歳';
    SHARE=`健康寿命シミュ、元気に過ごせる時間はあと約${toKj}年（${num(toKj*365)}日）でした🌿 今を大切に。`;show();anim($('big'),0,toKj,800);}''')

add(id='isan-bunkatsu', cat=S, emoji='⚖️',
  title='遺産分割シミュレーター｜法定相続分は誰がいくら？｜シミュラボ',
  desc='遺産の総額と家族構成（配偶者・子の人数など）から、民法で定められた法定相続分（誰がいくら相続するか）を計算する無料シミュレーター。',
  ogtitle='遺産分割シミュレーター｜法定相続分は誰がいくら？', ogdesc='遺産総額と家族構成から法定相続分を計算。',
  h1='遺産分割シミュレーター',
  lead='遺言がない場合、遺産は「法定相続分」で分けるのが基本です。遺産総額と家族構成から、配偶者・子それぞれの相続分の目安を計算します。',
  inputs='''    <h2>⚖️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>遺産の総額 <span class="hint">（万円）</span></label><input type="number" id="isan" value="6000" min="0" inputmode="numeric"></div>
    <div class="field"><label>配偶者</label><select id="hai"><option value="1" selected>いる</option><option value="0">いない</option></select></div></div>
    <div class="field"><label>子の人数 <span class="hint">（人）</span></label><input type="number" id="ko" value="2" min="0" max="10" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">相続分を見る</button>''',
  result='''      <div class="label">配偶者の相続分</div>
      <div class="big"><span id="big">0</span><span class="unit">万円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">子ども1人あたり</div><div class="v accent" id="ko1">—</div></div>
      <div class="stat"><div class="k">配偶者の割合</div><div class="v" id="hr">—</div></div>
      <div class="stat"><div class="k">子の合計</div><div class="v" id="kg">—</div></div></div>''',
  article='''    <h2>法定相続分の基本</h2>
    <div class="note"><strong>主なパターン</strong><br>配偶者＋子：配偶者1/2、子1/2を人数で均等分割<br>配偶者のみ：全額／子のみ：全額を人数で均等分割</div>
    <p>これは「法定相続分」で、遺言があればその内容が優先されます（遺留分に注意）。実際は相続人全員の話し合い（遺産分割協議）で自由に決められます。本ツールは配偶者と子のケースの目安です。詳しくは専門家へ。</p>
    <h2>よくある質問</h2>'''+faq([('親や兄弟が相続人の場合は？','子がいない場合は親・兄弟姉妹が相続人になり割合が変わります。本ツールは配偶者＋子向けです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const isan=Math.max(0,+$('isan').value||0),hai=+$('hai').value,ko=Math.max(0,+$('ko').value||0);
    let haibun=0,koTotal=0;
    if(hai&&ko>0){haibun=isan/2;koTotal=isan/2;}
    else if(hai&&ko===0){haibun=isan;koTotal=0;}
    else if(!hai&&ko>0){haibun=0;koTotal=isan;}
    const ko1=ko>0?koTotal/ko:0;
    $('sub').textContent=`遺産${num(isan)}万・配偶者${hai?'有':'無'}・子${ko}人`;
    $('ko1').textContent=num(ko1)+'万円';$('hr').textContent=hai?(ko>0?'1/2':'全部'):'なし';$('kg').textContent=num(koTotal)+'万円';
    SHARE=`遺産分割シミュ、法定相続分は配偶者${num(haibun)}万・子1人${num(ko1)}万でした⚖️`;show();anim($('big'),0,haibun,800);}''')

if __name__=='__main__':
    write_all(SIMS)
    print(f'senior done. {len(SIMS)} sims.')
