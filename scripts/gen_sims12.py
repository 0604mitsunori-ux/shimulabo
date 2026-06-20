# -*- coding: utf-8 -*-
"""シミュラボ：占い・診断カテゴリ 10本（gen_sims11のTPLを再利用）。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq, write_all

URANAI='占い・診断'
SIMS=[]

SIMS.append(dict(id='tanjyobi-uranai', cat=URANAI, emoji='🔢',
  title='誕生日でわかる運命数｜あなたの数秘術ナンバーは？｜シミュラボ',
  desc='生年月日の数字をすべて足して導く「運命数（ライフパスナンバー）」から、あなたの基本的な性質を占う無料の数秘術シミュレーター。',
  ogtitle='誕生日でわかる運命数｜あなたの数秘術ナンバーは？', ogdesc='生年月日から運命数（ライフパスナンバー）を計算して占う。',
  h1='誕生日でわかる運命数',
  lead='数秘術では、生年月日の数字をすべて足した「運命数」にあなたらしさが表れるとされます。誕生日を入れて、あなたのナンバーを占いましょう。',
  inputs='''    <h2>🔢 生年月日を入れる</h2>
    <div class="field"><label>生年月日</label><input type="date" id="d" value="1995-08-15"></div>
    <button class="btn btn-primary" id="calcBtn">運命数を占う</button>''',
  result='''      <div class="label">あなたの運命数は</div>
      <div class="big"><span id="big">0</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:18px;">—</div>''',
  article='''    <h2>運命数（ライフパスナンバー）とは</h2>
    <p>生年月日の数字をすべて足し、1桁になるまで足し続けて出す数字です（11・22・33はマスターナンバーとして残します）。数秘術ではこの数が「生まれ持った性質」を表すとされます。</p>
    <div class="note">💡 占いは自分を知るきっかけ。当たっている部分を活かし、苦手は工夫でカバーしていきましょう。</div>
    <h2>よくある質問</h2>'''+faq([('当たりますか？','エンタメ占いです。自己理解のヒントとしてお楽しみください。'),('入力した誕生日は送信されますか？','いいえ。占いはすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const v=$('d').value; if(!v){ alert('生年月日を選んでね'); return; }
    function lp(s){ let n=s.replace(/[^0-9]/g,'').split('').reduce((a,c)=>a+ +c,0); while(n>9&&n!==11&&n!==22&&n!==33){ n=n.toString().split('').reduce((a,c)=>a+ +c,0);} return n; }
    const N=lp(v);
    const M={1:['開拓者','自分で道を切り開くリーダー気質。行動力で周りを引っ張ります。'],2:['調和の人','人の気持ちに敏感で、サポートが得意。名脇役として輝きます。'],3:['表現者','明るくユニーク。クリエイティブな表現で人を楽しませます。'],4:['堅実家','コツコツ努力できる安定型。信頼を積み上げるタイプ。'],5:['自由人','好奇心旺盛で変化を楽しむ。フットワークの軽さが武器。'],6:['愛情家','面倒見が良く家庭的。人を支え育てることに喜びを感じます。'],7:['探究者','一人の時間を大切にする知的な分析家。深く突き詰める人。'],8:['実力者','野心と現実力を兼備。大きな目標を形にできるパワフルさ。'],9:['博愛者','視野が広く優しい理想家。みんなのために動ける人。'],11:['直感の人','鋭い直感とひらめき。人を導くカリスマ性を秘めます。'],22:['実現者','大きな夢を現実にする力。スケールの大きな実力者。'],33:['無償の愛','深い愛で人を包む稀有なナンバー。癒やしの存在。']};
    const t=M[N]||['自由人','あなたらしい個性を大切に。'];
    $('sub').textContent=`運命数 ${N}：${t[0]}`;
    $('adv').textContent='🔢 '+t[1];
    SHARE=`誕生日でわかる運命数、私は「${N}・${t[0]}」でした🔢\\n${t[1]}\\nあなたの運命数は？👇`;
    show(); anim($('big'),0,N,800);
  }'''))

SIMS.append(dict(id='zensei', cat=URANAI, emoji='🔮',
  title='前世診断｜あなたの前世は何者だった？｜シミュラボ',
  desc='生年月日と名前から、あなたの前世の姿と「前世の覚醒度」を占うエンタメ前世診断シミュレーター。',
  ogtitle='前世診断｜あなたの前世は何者だった？', ogdesc='生年月日と名前から、あなたの前世の姿を占う。',
  h1='前世診断',
  lead='あなたは前世で何者だったのか——。生年月日と名前から、前世の姿と「覚醒度」を占います。話のネタにどうぞ（エンタメ占い）。',
  inputs='''    <h2>🔮 あなたのことを教えて</h2>
    <div class="field"><label>生年月日</label><input type="date" id="d" value="1995-08-15"></div>
    <div class="field"><label>ニックネーム <span class="hint">（ひらがな/ローマ字でOK）</span></label><input type="text" id="nm" value="さくら" maxlength="20"></div>
    <button class="btn btn-primary" id="calcBtn">前世を占う</button>''',
  result='''      <div class="label">前世の覚醒度</div>
      <div class="big"><span id="big">0</span><span class="unit">%</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:18px;">—</div>''',
  article='''    <h2>この診断について</h2>
    <p>生年月日と名前から、あなたの前世像を導くエンタメ占いです。同じ入力なら結果は変わりません。出てきた前世の「強み」を、今のあなたに活かしてみては？</p>
    <div class="note">💡 前世が何であれ、大事なのは今世のあなた。結果はあくまで遊びとしてお楽しみください。</div>
    <h2>よくある質問</h2>'''+faq([('本当に前世が分かるの？','エンタメ占いです。真剣な前世鑑定ではありません。'),('入力内容は送信されますか？','いいえ。占いはすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const d=$('d').value, nm=($('nm').value||'').trim(); if(!d){ alert('生年月日を選んでね'); return; }
    const h=hash(d+'|'+nm);
    const T=[['旅する吟遊詩人','歌と物語で人々を癒やした自由な魂。表現力は今も健在。'],['名もなき名工','一つのことを極めた職人。あなたの粘り強さはここから。'],['辺境の薬師','薬草で人を助けた優しい治療者。世話好きはその名残。'],['星を読む占星術師','夜空から運命を読んだ賢者。直感の鋭さは前世ゆずり。'],['海を渡る商人','世界を股にかけた行動派。好奇心と交渉力が武器。'],['静かな修行僧','山にこもり真理を求めた探究者。内省的な深さがある。'],['誇り高き騎士','正義のために剣をとった勇者。芯の強さは折り紙つき。'],['宮廷の舞姫','人々を魅了したアーティスト。華やかさと愛され力。']];
    const t=T[h%8], pct=72+(h>>3)%28;
    $('sub').textContent=`あなたの前世は「${t[0]}」`;
    $('adv').textContent='🔮 '+t[1];
    SHARE=`前世診断、私の前世は「${t[0]}」でした🔮（覚醒度${pct}%）\\n${t[1]}\\nあなたの前世は？👇`;
    show(); anim($('big'),0,pct,900);
  }'''))

SIMS.append(dict(id='kotoshi-unsei', cat=URANAI, emoji='🎍',
  title='今年の運勢占い｜あなたの2026年の運気は？｜シミュラボ',
  desc='生年月日から、今年の総合運・金運・恋愛運・仕事運の運気スコアを占うエンタメ運勢シミュレーター。',
  ogtitle='今年の運勢占い｜あなたの今年の運気は？', ogdesc='生年月日から、今年の総合運・金運・恋愛運・仕事運を占う。',
  h1='今年の運勢占い',
  lead='今年のあなたの運気は？生年月日から、総合運・金運・恋愛運・仕事運をスコアで占います。1年の指針づくりに（エンタメ占い）。',
  inputs='''    <h2>🎍 生年月日を入れる</h2>
    <div class="field"><label>生年月日</label><input type="date" id="d" value="1995-08-15"></div>
    <button class="btn btn-primary" id="calcBtn">今年の運勢を占う</button>''',
  result='''      <div class="label">今年の総合運</div>
      <div class="big"><span id="big">0</span><span class="unit">点</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">金運</div><div class="v accent" id="kin">—</div></div>
      <div class="stat"><div class="k">恋愛運</div><div class="v" id="ren">—</div></div>
      <div class="stat"><div class="k">仕事運</div><div class="v" id="job">—</div></div></div>''',
  article='''    <h2>この占いについて</h2>
    <p>生年月日をもとに、今年の運気を4分野でスコア化するエンタメ占いです。良い運気は積極的に活かし、控えめな運気は無理せず備える——そんな使い方がおすすめです。</p>
    <div class="note">💡 運勢は「行動のヒント」。良い結果はお守りに、惜しい結果は注意のサインに。最後は自分の行動しだいです。</div>
    <h2>よくある質問</h2>'''+faq([('当たりますか？','エンタメ占いです。前向きな1年のきっかけにどうぞ。'),('入力内容は送信されますか？','いいえ。占いはすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const d=$('d').value; if(!d){ alert('生年月日を選んでね'); return; }
    const Y='2026';
    const sc=(salt)=>40+hash(d+'|'+Y+'|'+salt)%61;
    const total=sc('total'), kin=sc('kin'), ren=sc('ren'), job=sc('job');
    let cm; if(total>=80)cm='絶好調の最高な年！'; else if(total>=60)cm='追い風の良い年。'; else if(total>=45)cm='穏やかな安定の年。'; else cm='土台を整える充電の年。';
    $('sub').textContent=`${Y}年は…${cm}`;
    $('kin').textContent=kin+'点'; $('ren').textContent=ren+'点'; $('job').textContent=job+'点';
    SHARE=`今年の運勢を占ったら、総合運${total}点でした🎍（金運${kin}/恋愛${ren}/仕事${job}）\\n${cm}あなたは？👇`;
    show(); anim($('big'),0,total,900);
  }'''))

SIMS.append(dict(id='namae-uranai', cat=URANAI, emoji='📛',
  title='名前占い｜あなたの名前に秘められた運勢は？｜シミュラボ',
  desc='名前を入れるだけで、その名前に宿る総合運・性格・恋愛・仕事の傾向を占うエンタメ名前占いシミュレーター。',
  ogtitle='名前占い｜あなたの名前に秘められた運勢は？', ogdesc='名前から、総合運・性格・恋愛・仕事の傾向を占う。',
  h1='名前占い',
  lead='名前にはその人らしさが宿るといいます。あなたの名前を入れて、秘められた運勢と性格の傾向を占いましょう（エンタメ占い）。',
  inputs='''    <h2>📛 名前を入れる</h2>
    <div class="field"><label>名前 <span class="hint">（ニックネーム/ローマ字OK）</span></label><input type="text" id="nm" value="ゆうき" maxlength="20"></div>
    <button class="btn btn-primary" id="calcBtn">名前を占う</button>''',
  result='''      <div class="label">名前の総合運</div>
      <div class="big"><span id="big">0</span><span class="unit">点</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:18px;">—</div>''',
  article='''    <h2>この占いについて</h2>
    <p>名前の文字から運勢を導くエンタメ占いです。同じ名前なら結果は変わりません。占いの結果はあくまで遊び。あなたの名前は、あなただけの素敵な名前です。</p>
    <div class="note">💡 友だちや家族の名前も占って、結果を見せ合うと盛り上がります。</div>
    <h2>よくある質問</h2>'''+faq([('画数で占っていますか？','本ツールは名前の文字情報をもとにしたエンタメ占いで、正式な姓名判断（画数）とは異なります。'),('入力した名前は送信されますか？','いいえ。占いはすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const nm=($('nm').value||'').trim(); if(!nm){ alert('名前を入力してね'); return; }
    const h=hash(nm), total=50+h%51;
    const P=['情に厚く面倒見の良い','マイペースで芯の強い','好奇心旺盛で行動的な','穏やかで人に愛される','こだわり派の職人気質な','明るくムードメーカーな','努力家で堅実な','直感が冴える神秘的な'];
    const seikaku=P[(h>>4)%8];
    $('sub').textContent=`${seikaku}タイプ`;
    $('adv').textContent='📛 '+`「${nm}」さんは${seikaku}人。持ち味を信じて進めば運は開けます。`;
    SHARE=`名前占い、「${nm}」の総合運は${total}点でした📛\\n${seikaku}タイプだそう。あなたの名前は？👇`;
    show(); anim($('big'),0,total,900);
  }'''))

SIMS.append(dict(id='soul-color', cat=URANAI, emoji='🎨',
  title='ソウルカラー診断｜あなたの魂の色は何色？｜シミュラボ',
  desc='生年月日から、あなたの魂を表す「ソウルカラー」と、その色が示す性質を占うエンタメ診断シミュレーター。',
  ogtitle='ソウルカラー診断｜あなたの魂の色は何色？', ogdesc='生年月日から、あなたのソウルカラーとその意味を診断。',
  h1='ソウルカラー診断',
  lead='人にはそれぞれ、魂を象徴する色があるといいます。生年月日から、あなたの「ソウルカラー」を診断します（エンタメ診断）。',
  inputs='''    <h2>🎨 生年月日を入れる</h2>
    <div class="field"><label>生年月日</label><input type="date" id="d" value="1995-08-15"></div>
    <button class="btn btn-primary" id="calcBtn">ソウルカラーを診断する</button>''',
  result='''      <div class="label">あなたのソウルカラー濃度</div>
      <div class="big"><span id="big">0</span><span class="unit">%</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:18px;">—</div>''',
  article='''    <h2>この診断について</h2>
    <p>生年月日からソウルカラーを導くエンタメ診断です。あなたの色をラッキーカラーとして、小物やファッションに取り入れてみるのも楽しいですよ。</p>
    <div class="note">💡 出た色をその日のテーマカラーにすると、ちょっと気分が上がります。</div>
    <h2>よくある質問</h2>'''+faq([('当たりますか？','エンタメ診断です。自分を彩るヒントとしてどうぞ。'),('入力内容は送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const d=$('d').value; if(!d){ alert('生年月日を選んでね'); return; }
    const h=hash(d+'|soul');
    const C=[['レッド','情熱と行動力の人。エネルギッシュに前へ進む。'],['ブルー','冷静で誠実な人。信頼を集める安定感。'],['イエロー','明るく好奇心旺盛な人。場を照らすムードメーカー。'],['グリーン','穏やかで癒やしの人。人と自然を大切にする。'],['パープル','感性豊かで神秘的な人。直感とセンスが光る。'],['オレンジ','親しみやすく社交的な人。人を元気にする。'],['ピンク','愛情深くやさしい人。思いやりで包む。'],['ホワイト','純粋で芯のある人。まっすぐな信念を持つ。']];
    const t=C[h%8], pct=70+(h>>3)%31;
    $('sub').textContent=`あなたの色は「${t[0]}」`;
    $('adv').textContent='🎨 '+t[1];
    SHARE=`ソウルカラー診断、私の魂の色は「${t[0]}」でした🎨\\n${t[1]}\\nあなたは何色？👇`;
    show(); anim($('big'),0,pct,900);
  }'''))

SIMS.append(dict(id='doubutsu-uranai', cat=URANAI, emoji='🐾',
  title='誕生月の動物キャラ占い｜あなたはどんな動物タイプ？｜シミュラボ',
  desc='生まれた月から、あなたの性格を象徴する動物キャラと「らしさ度」を占うエンタメ動物タイプ占いシミュレーター。',
  ogtitle='誕生月の動物キャラ占い｜あなたは何タイプ？', ogdesc='生まれ月から、性格を象徴する動物キャラを占う。',
  h1='誕生月の動物キャラ占い',
  lead='あなたを動物にたとえると？生まれた月から、性格を象徴する動物タイプを占います。友だちと見せ合うと盛り上がります（エンタメ占い）。',
  inputs='''    <h2>🐾 生まれ月を選ぶ</h2>
    <div class="field"><label>生まれた月</label><select id="m"><option value="1">1月</option><option value="2">2月</option><option value="3">3月</option><option value="4">4月</option><option value="5">5月</option><option value="6">6月</option><option value="7">7月</option><option value="8" selected>8月</option><option value="9">9月</option><option value="10">10月</option><option value="11">11月</option><option value="12">12月</option></select></div>
    <div class="field"><label>名前 <span class="hint">（らしさ度の計算に使用）</span></label><input type="text" id="nm" value="さくら" maxlength="20"></div>
    <button class="btn btn-primary" id="calcBtn">動物タイプを占う</button>''',
  result='''      <div class="label">あなたの動物タイプ度</div>
      <div class="big"><span id="big">0</span><span class="unit">%</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:18px;">—</div>''',
  article='''    <h2>この占いについて</h2>
    <p>生まれ月ごとに動物キャラを当てはめたエンタメ占いです。動物の特徴を「あなたらしさ」として楽しんでください。</p>
    <div class="note">💡 家族や友だちの動物タイプも調べて、相性を語り合うと盛り上がります。</div>
    <h2>よくある質問</h2>'''+faq([('当たりますか？','エンタメ占いです。気軽にお楽しみください。'),('入力内容は送信されますか？','いいえ。占いはすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const m=+$('m').value||1, nm=($('nm').value||'').trim();
    const A=[['ライオン','堂々としたリーダー。頼れる存在感。'],['ネコ','自由気ままなマイペース。ツンデレな魅力。'],['イヌ','忠実で仲間思い。みんなに好かれる。'],['ウサギ','繊細でやさしい癒やし系。気配り上手。'],['イルカ','明るく社交的。場を盛り上げる人気者。'],['クマ','おだやかで包容力たっぷり。安心感の塊。'],['キツネ','頭の回転が速い策士。知的でクール。'],['ゾウ','穏やかで芯が強い。どっしり頼れる。'],['オオカミ','一匹狼の実力派。こだわりを貫く。'],['リス','こつこつ努力家。準備を怠らない堅実派。'],['ペンギン','仲間と群れる平和主義。協調性ばつぐん。'],['タカ','視野が広く先を読む。目標に一直線。']];
    const t=A[(m-1)%12], pct=70+hash(nm+'|'+m)%31;
    $('sub').textContent=`あなたは「${t[0]}」タイプ`;
    $('adv').textContent='🐾 '+t[1];
    SHARE=`誕生月の動物キャラ占い、私は「${t[0]}」タイプでした🐾\\n${t[1]}\\nあなたは何の動物？👇`;
    show(); anim($('big'),0,pct,900);
  }'''))

SIMS.append(dict(id='ketsueki-aishou', cat=URANAI, emoji='🩸',
  title='血液型相性占い｜あの人との血液型相性は？｜シミュラボ',
  desc='自分と相手の血液型から、相性の良さとつき合い方のヒントを占うエンタメ血液型相性シミュレーター。',
  ogtitle='血液型相性占い｜あの人との相性は？', ogdesc='自分と相手の血液型から、相性とつき合い方を占う。',
  h1='血液型相性占い',
  lead='定番の血液型相性。自分と相手の血液型を選ぶと、相性の良さとつき合い方のヒントを占います（楽しむための占いです）。',
  inputs='''    <h2>🩸 ふたりの血液型を選ぶ</h2>
    <div class="row"><div class="field"><label>あなた</label><select id="a"><option value="A">A型</option><option value="B">B型</option><option value="O">O型</option><option value="AB">AB型</option></select></div>
    <div class="field"><label>相手</label><select id="b"><option value="A">A型</option><option value="B" selected>B型</option><option value="O">O型</option><option value="AB">AB型</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">相性を占う</button>''',
  result='''      <div class="label">ふたりの相性</div>
      <div class="big"><span id="big">0</span><span class="unit">%</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:18px;">—</div>''',
  article='''    <h2>この占いについて</h2>
    <p>血液型による相性占いは、科学的根拠があるものではなく、あくまで会話を楽しむためのエンタメです。相性が何型でも、思いやりがあれば良い関係は築けます。</p>
    <div class="note">💡 血液型はきっかけの話題に。最後に大事なのは、お互いを尊重する気持ちです。</div>
    <h2>よくある質問</h2>'''+faq([('血液型で性格は決まるの？','科学的根拠はありません。エンタメとしてお楽しみください。'),('入力内容は送信されますか？','いいえ。占いはすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const a=$('a').value, b=$('b').value;
    const M={'AA':82,'BB':80,'OO':85,'ABAB':78,'AB':70,'BA':70,'AO':86,'OA':86,'AAB':75,'ABA':75,'BO':72,'OB':72,'BAB':74,'ABB':74,'OAB':80,'ABO':80};
    const sc=M[a+b]||75;
    let cm; if(sc>=84)cm='息ぴったりのベストコンビ。自然体でいられる関係です。'; else if(sc>=76)cm='良い相性。お互いの違いを認め合えば長続き。'; else cm='違いはあるけど学び合える二人。歩み寄りがカギ。';
    $('sub').textContent=`${a}型 × ${b}型`;
    $('adv').textContent='🩸 '+cm;
    SHARE=`血液型相性占い、${a}型×${b}型の相性は${sc}%でした🩸\\n${cm}\\nあなたたちは？👇`;
    show(); anim($('big'),0,sc,900);
  }'''))

SIMS.append(dict(id='lucky-today', cat=URANAI, emoji='🍀',
  title='今日の運勢＆ラッキーアイテム｜今日のあなたの運気は？｜シミュラボ',
  desc='生年月日を入れると、今日の運勢スコアとラッキーカラー・ラッキーナンバー・ラッキーアイテムを占う毎日使えるエンタメシミュレーター。',
  ogtitle='今日の運勢＆ラッキーアイテム｜今日の運気は？', ogdesc='生年月日から、今日の運勢とラッキーアイテムを占う。',
  h1='今日の運勢＆ラッキーアイテム',
  lead='今日のあなたはツイてる？生年月日を入れると、今日の運勢スコアとラッキーカラー・ナンバー・アイテムを占います。毎朝の習慣にどうぞ。',
  inputs='''    <h2>🍀 生年月日を入れる</h2>
    <div class="field"><label>生年月日</label><input type="date" id="d" value="1995-08-15"></div>
    <button class="btn btn-primary" id="calcBtn">今日の運勢を占う</button>''',
  result='''      <div class="label">今日のあなたの運勢</div>
      <div class="big"><span id="big">0</span><span class="unit">点</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">ラッキーカラー</div><div class="v accent" id="color">—</div></div>
      <div class="stat"><div class="k">ラッキーナンバー</div><div class="v" id="numb">—</div></div>
      <div class="stat"><div class="k">ラッキーアイテム</div><div class="v" id="item">—</div></div></div>''',
  article='''    <h2>この占いについて</h2>
    <p>生年月日と「その日の日付」から運勢を導くので、毎日結果が変わります。良いことがありそうな日は積極的に、控えめな日は無理せずマイペースに。</p>
    <div class="note">💡 ラッキーアイテムを身につけると、ちょっと気分が上がって良い1日になりやすいかも。</div>
    <h2>よくある質問</h2>'''+faq([('毎日変わりますか？','はい。日付が変わると結果も変わります。'),('入力内容は送信されますか？','いいえ。占いはすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const d=$('d').value; if(!d){ alert('生年月日を選んでね'); return; }
    const T=new Date(); const today=`${T.getFullYear()}-${T.getMonth()+1}-${T.getDate()}`;
    const h=hash(d+'|'+today), score=40+h%61;
    const colors=['レッド','ブルー','イエロー','グリーン','パープル','オレンジ','ピンク','ホワイト'];
    const items=['ハンカチ','腕時計','イヤホン','お気に入りのペン','リップ','マグカップ','観葉植物','スニーカー'];
    const color=colors[(h>>2)%8], numb=(h>>5)%9+1, item=items[(h>>8)%8];
    let cm; if(score>=80)cm='絶好調！チャンスを逃さないで。'; else if(score>=60)cm='good。前向きに動ける日。'; else if(score>=45)cm='まずまず。マイペースで。'; else cm='充電日。無理せずいこう。';
    $('sub').textContent=`今日(${T.getMonth()+1}/${T.getDate()})は…${cm}`;
    $('color').textContent=color; $('numb').textContent=numb; $('item').textContent=item;
    SHARE=`今日の運勢、${score}点でした🍀\\nラッキーカラーは${color}、アイテムは${item}！\\nあなたの今日は？👇`;
    show(); anim($('big'),0,score,900);
  }'''))

SIMS.append(dict(id='kyusei', cat=URANAI, emoji='⭐',
  title='九星気学 本命星占い｜あなたの本命星と今年の運気は？｜シミュラボ',
  desc='生まれ年から九星気学の「本命星」を割り出し、星の性質と今年の運気を占うエンタメ九星気学シミュレーター。',
  ogtitle='九星気学 本命星占い｜あなたの本命星は？', ogdesc='生まれ年から本命星を割り出し、性質と今年の運気を占う。',
  h1='九星気学 本命星占い',
  lead='東洋で親しまれてきた九星気学。生まれ年から「本命星」を割り出し、あなたの性質と今年の運気を占います（エンタメ占い）。',
  inputs='''    <h2>⭐ 生まれ年を入れる</h2>
    <div class="field"><label>生まれ年 <span class="hint">（西暦・例: 1995）</span></label><input type="number" id="y" value="1995" min="1920" max="2025" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">本命星を占う</button>''',
  result='''      <div class="label">今年の運気</div>
      <div class="big"><span id="big">0</span><span class="unit">点</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:18px;">—</div>''',
  article='''    <h2>九星気学とは</h2>
    <p>生まれ年をもとに「一白水星〜九紫火星」の9つの星に分け、性質や運気の流れを読む東洋の占術です。本ツールは簡易計算によるエンタメ版です。</p>
    <div class="note">💡 ※立春（2月4日ごろ）より前の生まれは前年の星になる流派もあります。本ツールは西暦の年で簡易判定しています。</div>
    <h2>よくある質問</h2>'''+faq([('正式な鑑定と同じ？','簡易計算のエンタメ版です。流派により異なる場合があります。'),('入力内容は送信されますか？','いいえ。占いはすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const y=Math.max(1,Math.round(+$('y').value||1));
    let s=y.toString().split('').reduce((a,c)=>a+ +c,0); while(s>9) s=s.toString().split('').reduce((a,c)=>a+ +c,0);
    let star=11-s; if(star>9)star-=9; if(star<1)star+=9;
    const N=['','一白水星','二黒土星','三碧木星','四緑木星','五黄土星','六白金星','七赤金星','八白土星','九紫火星'];
    const D=['','柔軟で人に寄り添う知性派','面倒見が良く努力家','行動的で勢いのある開拓者','穏やかで信頼される調整役','カリスマ性のある中心人物','正義感が強くリーダー気質','社交的で愛されるムードメーカー','粘り強く変革を起こす実力者','華やかで直感に優れた情熱家'];
    const score=45+hash(y+'|2026')%56;
    $('sub').textContent=`あなたの本命星は「${N[star]}」`;
    $('adv').textContent='⭐ '+`${D[star]}。今年は持ち味を信じて動くと吉。`;
    SHARE=`九星気学、私の本命星は「${N[star]}」でした⭐（今年の運気${score}点）\\n${D[star]}タイプだそう。あなたは？👇`;
    show(); anim($('big'),0,score,900);
  }'''))

SIMS.append(dict(id='tarot-today', cat=URANAI, emoji='🃏',
  title='今日の一枚タロット｜今日のあなたへのメッセージは？｜シミュラボ',
  desc='占いたいテーマを選んでカードを引くと、タロットの大アルカナ1枚と今日のメッセージを占えるエンタメタロットシミュレーター。',
  ogtitle='今日の一枚タロット｜今日のメッセージは？', ogdesc='テーマを選んでカードを1枚引き、今日のメッセージを占う。',
  h1='今日の一枚タロット',
  lead='今日のあなたへのメッセージを、タロット1枚に聞いてみましょう。占いたいテーマを選んでカードを引いてください（エンタメ占い）。',
  inputs='''    <h2>🃏 テーマを選んで引く</h2>
    <div class="field"><label>占いたいこと</label><select id="theme"><option value="total">今日の総合運</option><option value="love">恋愛</option><option value="work">仕事</option><option value="money">金運</option></select></div>
    <button class="btn btn-primary" id="calcBtn">カードを1枚引く</button>''',
  result='''      <div class="label">カードのエネルギー</div>
      <div class="big"><span id="big">0</span><span class="unit">%</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:18px;">—</div>''',
  article='''    <h2>この占いについて</h2>
    <p>大アルカナ22枚から、その日とテーマに応じて1枚を引くエンタメタロットです。正位置はそのまま、逆位置は「少し気をつけて」のサイン。メッセージを今日のヒントに。</p>
    <div class="note">💡 引いたカードの言葉を、今日の小さな指針にしてみてください。</div>
    <h2>よくある質問</h2>'''+faq([('毎日・テーマ別に変わりますか？','はい。日付とテーマで引かれるカードが変わります。'),('入力内容は送信されますか？','いいえ。占いはすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const theme=$('theme').value;
    const T=new Date(); const today=`${T.getFullYear()}-${T.getMonth()+1}-${T.getDate()}`;
    const h=hash(today+'|'+theme);
    const C=[['愚者','新しい一歩。思い切って踏み出して。'],['魔術師','準備は整った。あなたの実力を発揮する時。'],['女教皇','直感を信じて。静かに見極めを。'],['女帝','豊かさと愛情。受け取る心を大切に。'],['皇帝','主導権を握る時。堂々と進もう。'],['教皇','信頼できる人に相談を。学びの時。'],['恋人','心が動く出会い・選択。素直に。'],['戦車','勢いに乗って前進。突破口が開く。'],['力','焦らず粘り強く。やさしい強さで。'],['隠者','一人で考える時間が答えをくれる。'],['運命の輪','流れが変わる。チャンスを掴んで。'],['正義','公正な判断を。バランスが鍵。'],['吊された人','今は待ちの時。視点を変えて。'],['節制','ほどよく調和を。やりすぎ注意。'],['星','希望が見える。願いを大切に。'],['月','迷いやすい日。慎重に進もう。'],['太陽','最高の運気！自信を持って。'],['審判','再スタートの合図。過去を活かして。'],['世界','物事が完成へ。達成のとき。'],['力の杖','情熱を燃やして。やる気が結果に。'],['聖杯','心が満たされる。感謝を忘れずに。'],['星の硬貨','コツコツが実る。堅実にいこう。']];
    const idx=h%22, up=(h>>5)%10>2; const card=C[idx];
    const pct=up?(70+(h>>8)%31):(35+(h>>8)%30);
    $('sub').textContent=`引いたカード：${card[0]}（${up?'正位置':'逆位置'}）`;
    $('adv').textContent='🃏 '+(up?card[1]:card[1].replace(/。$/,'')+'…ただし少し慎重に。');
    SHARE=`今日の一枚タロット、引いたのは「${card[0]}」(${up?'正位置':'逆位置'})🃏\\n${card[1]}\\nあなたのカードは？👇`;
    show(); anim($('big'),0,pct,900);
  }'''))

if __name__=='__main__':
    write_all(SIMS)
    print(f'uranai done. {len(SIMS)} sims.')
