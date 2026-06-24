# -*- coding: utf-8 -*-
"""シミュラボ：結婚式・ブライダル診断6本（新カテゴリ slug=wedding）。
診断4（カテゴリ集計式タイプ診断）＋計算2。CTA（トキハナ）は patch_tokihana_cta.py で挿入。
gen_sims_tool の TPL/viz を流用（try無し）。

seo_internal.py / gen_images.py のauto-importに 'gen_sims_wedding' を追加して使う。
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq
from gen_sims_tool import TPL, viz
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CAT = '結婚式・ブライダル'
SIMS=[]
def add(**k):
    k.setdefault('visual','')
    SIMS.append(k)

QUIZ_INPUTS = '''    <h2>__QHEAD__</h2>
    <p style="color:var(--ink-2);font-size:13px;margin:-4px 0 6px;">直感で選んでOK。<span id="prog" style="font-weight:800;color:var(--teal-d);">0 / __QN__ 問</span></p>
    <div id="quiz" class="quiz"></div>
    <button class="btn btn-primary" id="calcBtn" style="margin-top:8px;">結果を見る</button>'''
QUIZ_RESULT = '''      <div class="label">__RLABEL__</div>
      <div id="emoji" style="font-size:66px;line-height:1.1;">💍</div>
      <div class="big" style="font-size:27px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="desc" style="text-align:left;margin-top:14px;">—</div>'''

def quiz_sim(id, emoji, title, desc, ogtitle, ogdesc, h1, lead, qhead, questions, results, rlabel, sharetpl, article):
    qn=len(questions)
    js = ('  const Q=' + json.dumps(questions, ensure_ascii=False) + ';\n'
          '  const RES=' + json.dumps(results, ensure_ascii=False) + ';\n'
          '  const RLABEL=' + json.dumps(rlabel, ensure_ascii=False) + ', SHARETPL=' + json.dumps(sharetpl, ensure_ascii=False) + ';\n'
          + r'''  const wrap=$('quiz');
  Q.forEach((qq,i)=>{const d=document.createElement('div');d.className='q';
    let h='<p class="qt"><b>Q'+(i+1)+'.</b> '+qq[0]+'</p><div class="opts" style="grid-template-columns:1fr;">';
    qq[1].forEach(o=>{h+='<button type="button" class="opt" data-q="'+i+'" data-k="'+o[1]+'">'+o[0]+'</button>';});
    d.innerHTML=h+'</div>';wrap.appendChild(d);});
  wrap.addEventListener('click',e=>{const b=e.target.closest('.opt');if(!b)return;const qi=b.dataset.q;
    wrap.querySelectorAll('.opt[data-q="'+qi+'"]').forEach(o=>o.classList.toggle('on',o===b));
    const p=$('prog');if(p)p.textContent=document.querySelectorAll('#quiz .opt.on').length+' / '+Q.length+' 問';});
  function calc(){const on=document.querySelectorAll('#quiz .opt.on');
    if(on.length<Q.length){alert('あと'+(Q.length-on.length)+'問！全部の質問に答えてね');
      const qs=document.querySelectorAll('#quiz .q');for(let j=0;j<qs.length;j++){if(!qs[j].querySelector('.opt.on')){qs[j].scrollIntoView({behavior:'smooth',block:'center'});break;}}return;}
    const tally={};on.forEach(b=>{tally[b.dataset.k]=(tally[b.dataset.k]||0)+1;});
    let best=Object.keys(RES)[0],bv=-1;for(const k in RES){const v=tally[k]||0;if(v>bv){bv=v;best=k;}}
    const r=RES[best];$('emoji').textContent=r[0];$('big').textContent=r[1];$('sub').textContent='あなたの結果';$('desc').textContent='✨ '+r[2];
    SHARE=SHARETPL.replace('{name}',r[1]);
    show();}
''')
    SIMS.append(dict(id=id, emoji=emoji, cat=CAT, title=title, desc=desc, ogtitle=ogtitle, ogdesc=ogdesc, h1=h1, lead=lead,
        inputs=QUIZ_INPUTS.replace('__QHEAD__',qhead).replace('__QN__',str(qn)),
        result=QUIZ_RESULT.replace('__RLABEL__',rlabel), visual='', article=article, js=js))

def w_article(intro, title, text, faqs):
    return ('    <div class="note"><strong>これは何？</strong>：'+intro+'<br><b>※エンタメ診断・目安です。実際の式場・費用は見学や相談で確認しましょう。</b></div>\n'
            '    <h2>'+title+'</h2>\n    <p>'+text+'</p>\n    <h2>よくある質問</h2>'+faq(faqs))

# ============================================================
# 1. 結婚式スタイル診断（結婚式 種類 800/KD0/TP7100 + 挙式スタイル）
# ============================================================
quiz_sim('wedding-style','💒',
  '結婚式スタイル診断｜ふたりに合う挙式スタイルは？教会式・神前式・人前式｜シミュラボ',
  '6つの質問で、ふたりに合う結婚式（挙式）のスタイルを診断する無料コンテンツ。教会式・神前式・人前式・フォト/少人数婚から、価値観にマッチするスタイルとおすすめ会場の方向性が分かります。',
  '結婚式スタイル診断｜ふたりに合う挙式は？','6問でふたりに合う挙式スタイル（教会式・神前式・人前式・少人数）を診断。',
  '結婚式スタイル診断',
  '教会式・神前式・人前式・フォト/少人数婚…結婚式（挙式）にはいろいろなスタイルがあります。6つの質問で、ふたりの価値観にマッチするスタイルと会場の方向性を診断します。',
  '💒 ふたりの希望に近いものを選んでね',
  [['ゲストの人数は？',[['たくさん招きたい','church'],['親族中心で少人数','shinto'],['親しい人だけ','jinzen'],['ふたり・ごく少人数','photo']]],
   ['式の雰囲気は？',[['ロマンチックで華やか','church'],['厳かで伝統的','shinto'],['自由でアットホーム','jinzen'],['気軽でカジュアル','photo']]],
   ['和と洋なら？',[['洋装でドレス','church'],['和装で白無垢','shinto'],['どちらも楽しみたい','jinzen'],['こだわらない','photo']]],
   ['大切にしたいのは？',[['映える写真と演出','church'],['ご先祖・両家のつながり','shinto'],['ゲストとの一体感','jinzen'],['費用を抑える','photo']]],
   ['誓いの形は？',[['神様の前で（チャペル）','church'],['神前で（神社・神殿）','shinto'],['ゲストの前で','jinzen'],['記録に残せれば十分','photo']]],
   ['予算感は？',[['しっかりかけたい','church'],['標準的に','shinto'],['メリハリつけたい','jinzen'],['なるべく抑えたい','photo']]]],
  {'church':['⛪','教会式（チャペル）タイプ','ドレスが映える華やかな挙式が似合うふたり。チャペルのあるホテルや専門式場、ゲストハウスがおすすめ。'],
   'shinto':['⛩️','神前式タイプ','伝統と両家のつながりを大切にするふたり。神社や神殿、和の会場が似合います。'],
   'jinzen':['💐','人前式タイプ','形式にとらわれず、ゲストと一緒に作る自由な式が似合うふたり。レストランやゲストハウスが好相性。'],
   'photo':['📸','フォト/少人数婚タイプ','費用を抑えて大切な人とゆっくり過ごしたいふたり。フォトウェディングや少人数会食がおすすめ。']},
  'あなたたちに合う挙式スタイルは',
  '結婚式スタイル診断、私たちは「{name}」でした💒 あなたたちは？',
  w_article('6つの質問から、ふたりに合う結婚式（挙式）のスタイルを診断します。','挙式スタイルの種類','結婚式のスタイルは大きく、教会式（チャペル）・神前式・人前式・フォト/少人数婚などに分かれます。それぞれ雰囲気・衣装・費用感・向いている会場が異なります。まずは方向性を知り、気になるスタイルが叶う式場を探すのがスムーズです。',
    [('スタイルは後から変えられる？','式場選びの前なら自由に検討できます。会場によって対応できるスタイルが異なるので、見学・相談で確認を。'),('費用はスタイルで変わる？','少人数・フォトは抑えやすく、大人数の挙式・披露宴は高くなりがちです。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]))

# ============================================================
# 2. 結婚式場タイプ診断（結婚式場 診断 + ゲストハウスウェディング）
# ============================================================
quiz_sim('venue-type','🏰',
  '結婚式場タイプ診断｜ホテル・専門式場・ゲストハウス・レストラン｜シミュラボ',
  '6つの質問で、ふたりに合う結婚式場のタイプ（ホテル・専門式場・ゲストハウス・レストラン）を診断する無料コンテンツ。重視するポイントから、向いている会場の方向性が分かります。',
  '結婚式場タイプ診断｜あなたに合う会場は？','6問でホテル・専門式場・ゲストハウス・レストランのどれが合うか診断。',
  '結婚式場タイプ診断',
  '結婚式場にもいろいろな種類があります。6つの質問で、ふたりに合う会場のタイプ（ホテル・専門式場・ゲストハウス・レストラン）を診断します。式場探しの軸づくりに。',
  '🏰 重視するポイントを選んでね',
  [['いちばん重視するのは？',[['格式・安心感','hotel'],['挙式・設備の充実','senmon'],['貸切でアットホーム','guest'],['料理・コスパ','rest']]],
   ['ゲストへのおもてなしは？',[['一流のサービス','hotel'],['専門スタッフの手厚さ','senmon'],['自宅に招くような距離感','guest'],['美味しい料理で','rest']]],
   ['遠方ゲストは？',[['多い（宿泊も安心な所）','hotel'],['それなりにいる','senmon'],['少なめ','guest'],['ほぼ近隣','rest']]],
   ['雰囲気の好みは？',[['上質でフォーマル','hotel'],['王道の結婚式らしさ','senmon'],['個性的でおしゃれ','guest'],['気取らずカジュアル','rest']]],
   ['人数規模は？',[['大人数もOK','hotel'],['標準的','senmon'],['中〜少人数','guest'],['少人数','rest']]],
   ['予算は？',[['しっかりめ','hotel'],['標準','senmon'],['メリハリ','guest'],['抑えめ','rest']]]],
  {'hotel':['🏨','ホテルウェディング タイプ','格式とおもてなし、遠方ゲストの安心感を重視するふたりに。宿泊や交通の便も◎。'],
   'senmon':['🏛️','専門式場 タイプ','挙式・披露宴の設備とスタッフの手厚さで、王道の結婚式を叶えたいふたりに。'],
   'guest':['🏡','ゲストハウス タイプ','一軒家を貸切で、自分たちらしい個性的な式をしたいふたりに。アットホームで自由度高め。'],
   'rest':['🍽️','レストラン タイプ','料理とコスパ、気取らない雰囲気を大切にするふたりに。少人数・会食婚にも好相性。']},
  'あなたたちに合う式場タイプは',
  '結婚式場タイプ診断、私たちは「{name}」でした🏰 あなたたちは？',
  w_article('6つの質問から、ふたりに合う結婚式場のタイプを診断します。','結婚式場の種類','結婚式場は主に、ホテル・専門式場・ゲストハウス・レストランに分かれます。格式・おもてなし・自由度・コスパなど、重視する点で向き不向きが変わります。タイプを絞ると、たくさんの式場から効率よく探せます。',
    [('1つに絞らないとダメ？','いいえ。気になるタイプを複数見学して比べるのがおすすめです。'),('費用はタイプで違う？','一般にホテル・専門式場は高め、レストラン・少人数は抑えやすい傾向です。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]))

# ============================================================
# 3. 結婚式の演出タイプ診断（結婚式 演出 1900/KD0/TP3600）
# ============================================================
quiz_sim('enshutsu-type','🎊',
  '結婚式の演出タイプ診断｜感動派？盛り上げ派？ふたりに合う演出は｜シミュラボ',
  '6つの質問で、ふたりに合う結婚式の演出タイプ（感動演出・盛り上げ・ナチュラル・王道フォーマル）を診断する無料コンテンツ。披露宴の演出選びのヒントに。',
  '結婚式の演出タイプ診断｜感動派？盛り上げ派？','6問でふたりに合う披露宴の演出タイプを診断。',
  '結婚式の演出タイプ診断',
  '披露宴の演出は、ふたりらしさが出るところ。6つの質問で、感動演出・盛り上げ・ナチュラル・王道フォーマルのどのタイプが合うかを診断します。',
  '🎊 ふたりの好みに近いものを選んでね',
  [['披露宴でゲストに何を届けたい？',[['感謝と感動','kandou'],['とにかく楽しい時間','moriage'],['心地よい時間','natural'],['きちんとした祝福','oudou']]],
   ['BGMや雰囲気は？',[['泣けるバラード','kandou'],['アップテンポで盛り上がる','moriage'],['おしゃれで穏やか','natural'],['上品でクラシック','oudou']]],
   ['手紙・サプライズは？',[['ぜひやりたい','kandou'],['ゲスト参加型で','moriage'],['さりげなく','natural'],['定番をきちんと','oudou']]],
   ['ゲストとの距離感は？',[['一人ひとりに感謝を','kandou'],['みんなでワイワイ','moriage'],['ゆったり歓談','natural'],['礼儀正しく','oudou']]],
   ['装花・装飾は？',[['ドラマチックに','kandou'],['カラフルで楽しく','moriage'],['ナチュラルグリーン','natural'],['格式高く','oudou']]],
   ['いちばん大切なのは？',[['泣ける瞬間','kandou'],['笑顔と歓声','moriage'],['ふたりらしさ','natural'],['きちんと感','oudou']]]],
  {'kandou':['😢','感動演出タイプ','手紙やサプライズで“泣ける”瞬間を大切にするふたり。映像演出や手紙が映えます。'],
   'moriage':['🎉','盛り上げタイプ','ゲスト参加型で会場を盛り上げたいふたり。余興やフォトラウンドで一体感を。'],
   'natural':['🌿','ナチュラルタイプ','気取らず心地よい時間を大切にするふたり。歓談中心・ナチュラル装花が◎。'],
   'oudou':['👑','王道フォーマルタイプ','格式と定番を大切にするふたり。きちんとした祝福の場が似合います。']},
  'あなたたちに合う演出タイプは',
  '結婚式の演出タイプ診断、私たちは「{name}」でした🎊 あなたたちは？',
  w_article('6つの質問から、ふたりに合う披露宴の演出タイプを診断します。','結婚式の演出の選び方','演出は「ふたりらしさ」と「ゲストへのおもてなし」のバランスで決めると失敗しにくいです。感動系・盛り上げ系・ナチュラル系・王道系など、方向性を決めてから具体的な演出を選ぶとまとまります。',
    [('演出はいくつやればいい？','詰め込みすぎは禁物。テーマに沿って3〜5個に絞ると間延びしません。'),('費用はかかる？','映像・装花・特殊演出は加算されます。優先順位をつけて選びましょう。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]))

# ============================================================
# 4. 結婚式テーマ診断（結婚式 テーマ 800/KD0）
# ============================================================
quiz_sim('wedding-theme','🎀',
  '結婚式テーマ診断｜ナチュラル？エレガント？ふたりのテーマカラー｜シミュラボ',
  '6つの質問で、ふたりに合う結婚式のテーマ（ナチュラル・エレガント/クラシック・モダン・カジュアル/ポップ）を診断する無料コンテンツ。会場装飾やドレス選びの軸づくりに。',
  '結婚式テーマ診断｜ふたりに合うテーマは？','6問で結婚式のテーマ（ナチュラル/エレガント/モダン/カジュアル）を診断。',
  '結婚式テーマ診断',
  '装花・ドレス・ペーパーアイテム…結婚式は「テーマ」を決めると一気にまとまります。6つの質問で、ふたりに合うテーマの方向性を診断します。',
  '🎀 好みに近いものを選んでね',
  [['好きな雰囲気は？',[['やわらかく自然体','natural'],['上品で洗練','elegant'],['シャープでおしゃれ','modern'],['明るく楽しい','casual']]],
   ['好きな色は？',[['グリーン・ベージュ','natural'],['白・くすみカラー','elegant'],['モノトーン・ネイビー','modern'],['ビビッド・カラフル','casual']]],
   ['会場装飾は？',[['草花・ドライフラワー','natural'],['シャンデリア・キャンドル','elegant'],['ミニマルでスタイリッシュ','modern'],['バルーン・ポップ','casual']]],
   ['ドレスの好みは？',[['ナチュラルなAライン','natural'],['クラシックなプリンセス','elegant'],['スレンダー・個性的','modern'],['カラードレスで遊ぶ','casual']]],
   ['理想の写真は？',[['ガーデン・自然光','natural'],['上質でドラマチック','elegant'],['都会的でアート','modern'],['笑顔でにぎやか','casual']]],
   ['大切にしたいのは？',[['心地よさ','natural'],['特別感','elegant'],['センス','modern'],['楽しさ','casual']]]],
  {'natural':['🌿','ナチュラルテーマ','草花や自然光が似合う、やわらかく自然体なふたり。ガーデンやレストランが好相性。'],
   'elegant':['🤍','エレガント／クラシックテーマ','上品で特別感のある世界観が似合うふたり。ホテルや専門式場で映えます。'],
   'modern':['🖤','モダン／スタイリッシュテーマ','洗練された都会的な雰囲気が似合うふたり。デザイン性の高い会場が◎。'],
   'casual':['🎈','カジュアル／ポップテーマ','明るく楽しい雰囲気が似合うふたり。ゲストハウスやレストランで自由に。']},
  'あなたたちに合う結婚式テーマは',
  '結婚式テーマ診断、私たちは「{name}」でした🎀 あなたたちは？',
  w_article('6つの質問から、ふたりに合う結婚式のテーマを診断します。','結婚式のテーマの決め方','テーマ（世界観）を最初に決めると、装花・ドレス・ペーパーアイテム・BGMまで一貫してまとまり、ちぐはぐになりません。色（テーマカラー）を1〜2色決めるだけでも、ぐっと統一感が出ます。',
    [('テーマは必要？','必須ではありませんが、決めると準備の判断がラクになり、満足度も上がりやすいです。'),('会場で実現できる？','会場の雰囲気と合うテーマだと再現しやすいです。見学時に相談を。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]))

# ============================================================
# 5. 結婚式の自己負担額シミュレーター（結婚式 費用 自己負担 250/KD0/TP1300）
# ============================================================
add(id='kekkon-jikofutan', emoji='💴', cat=CAT,
  title='結婚式の自己負担額シミュレーター｜ご祝儀を引いた持ち出しはいくら？｜シミュラボ',
  desc='招待人数・1人あたりの費用・ご祝儀・親の援助から、結婚式の自己負担額（実際の持ち出し）を計算する無料シミュレーター。総額だけでなく「最終的にいくら必要か」が分かります。',
  ogtitle='結婚式の自己負担額シミュレーター', ogdesc='総額からご祝儀・援助を引いた自己負担（持ち出し）を計算。無料。',
  h1='結婚式の自己負担額シミュレーター',
  lead='結婚式は「総額」だけでなく、ご祝儀や親の援助を引いた「自己負担（持ち出し）」が大事。招待人数・1人あたり費用・ご祝儀・援助を入れて、実際に必要な額を計算します。',
  inputs='''    <h2>💴 条件を入れる</h2>
    <div class="row"><div class="field"><label>招待人数 <span class="hint">（人）</span></label><input type="number" id="g" value="60" min="0" inputmode="numeric"></div>
    <div class="field"><label>1人あたりの費用 <span class="hint">（円・会場/料理/装花等）</span></label><input type="number" id="per" value="70000" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>1人あたりのご祝儀 <span class="hint">（円・平均）</span></label><input type="number" id="goshugi" value="32000" min="0" inputmode="numeric"></div>
    <div class="field"><label>親などの援助 <span class="hint">（円・任意）</span></label><input type="number" id="support" value="0" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">自己負担額を計算</button>''',
  result='''      <div class="label">ふたりの自己負担（持ち出し）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">総額</div><div class="v" id="total">—</div></div>
      <div class="stat"><div class="k">ご祝儀の合計</div><div class="v accent" id="gosum">—</div></div>
      <div class="stat"><div class="k">1人あたりの持ち出し</div><div class="v" id="perout">—</div></div></div>''',
  article='''    <div class="note"><strong>計算式</strong><br>総額 ＝ 招待人数 × 1人あたり費用／自己負担 ＝ 総額 − ご祝儀合計 − 援助</div>
    <h2>結婚式の自己負担の考え方</h2>
    <p>結婚式は総額の数字だけ見ると驚きますが、実際にはゲストからのご祝儀でかなりの部分がまかなえます。「総額 −（ご祝儀＋親の援助）＝ 自己負担」が、ふたりが本当に用意するお金。招待人数が増えると費用も増えますが、ご祝儀も増えるため、自己負担は意外と一定に近づくこともあります。<b>※見学時の見積もりは当日までに平均70〜100万円ほど上がることがあるため、最終見積もりで確認しましょう。</b></p>
    <h2>よくある質問</h2>'''+faq([
      ('ご祝儀の相場は？','友人3万円、上司・親族3〜5万円が目安。平均では1人あたり3万円前後で見積もる人が多いです。'),
      ('見積もりはなぜ上がる？','装花・衣装・料理のグレードアップやオプション追加で上がりがちです。当日想定の見積もりを出してもらうと安心です。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const g=Math.max(0,+$('g').value||0),per=Math.max(0,+$('per').value||0),go=Math.max(0,+$('goshugi').value||0),sup=Math.max(0,+$('support').value||0);
    const total=g*per,gosum=g*go,futan=Math.max(0,total-gosum-sup);
    $('sub').textContent=`${num(g)}人・1人${yen(per)}・ご祝儀${yen(go)}`;
    $('total').textContent=yen(total);$('gosum').textContent=yen(gosum);$('perout').textContent=yen(g>0?futan/g:0);
    SHARE=`結婚式の自己負担シミュ、${num(g)}人の式で自己負担は 約${yen(futan)}（総額${yen(total)}−ご祝儀${yen(gosum)}）でした💴`;
    show();anim(futan);}
  function anim(v){const el=$('big'),t0=performance.now();(function s(n){const p=Math.min(1,(n-t0)/800),e=1-Math.pow(1-p,3);el.textContent=Math.round(v*e).toLocaleString('ja-JP');if(p<1)requestAnimationFrame(s);})(performance.now());}''')

# ============================================================
# 6. 結婚式 準備スケジュール診断（結婚式 準備 いつから 100/KD0/TP1700）
# ============================================================
add(id='kekkon-junbi', emoji='📋', cat=CAT,
  title='結婚式 準備スケジュール診断｜いつから始める？間に合う？｜シミュラボ',
  desc='挙式の希望日を入れるだけで、今からの準備期間・式場決定や招待状などの目安時期・間に合うかの判定を表示する無料の結婚式準備スケジュール診断。',
  ogtitle='結婚式 準備スケジュール診断｜間に合う？', ogdesc='挙式希望日から準備期間と段取りの目安、間に合うかを診断。無料。',
  h1='結婚式 準備スケジュール診断',
  lead='「結婚式の準備っていつから？」挙式の希望日を入れると、今からの準備期間、式場決定・招待状などの目安時期、間に合うかどうかを表示します。',
  inputs='''    <h2>📋 挙式の希望日を入れる</h2>
    <div class="field"><label>挙式の希望日</label><input type="date" id="d" value="2027-06-01"></div>
    <button class="btn btn-primary" id="calcBtn">スケジュールを見る</button>''',
  result='''      <div class="label">挙式まで</div>
      <div class="big"><span id="big">0</span><span class="unit">日</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="judge" style="text-align:left;margin-top:14px;">—</div>
      <div class="statline"><div class="stat"><div class="k">準備期間</div><div class="v accent" id="months">—</div></div>
      <div class="stat"><div class="k">式場決定の目安</div><div class="v" id="venue">—</div></div>
      <div class="stat"><div class="k">招待状発送の目安</div><div class="v" id="invite">—</div></div></div>''',
  article='''    <div class="note"><strong>準備期間の目安</strong><br>式場決定：挙式の8〜12ヶ月前／招待状発送：2〜3ヶ月前／最終打合せ：1ヶ月前。一般に準備は半年〜1年が目安です。</div>
    <h2>結婚式の準備はいつから？</h2>
    <p>結婚式の準備は、式場探し・決定からスタートします。人気の式場・日取りは早く埋まるため、挙式の<b>8〜12ヶ月前</b >に式場を決めるのが安心。診断結果のスケジュールを目安に、まずは式場探し・見学から始めましょう。期間が短い場合でも、少人数婚やフォトなら短期間で実現できます。</p>
    <h2>よくある質問</h2>'''+faq([
      ('準備期間が短くても大丈夫？','可能です。少人数・フォト・持ち込み少なめなら数ヶ月でも実現できます。式場に相談を。'),
      ('まず何から始める？','式場探し・見学です。複数を比較して、見積もりと雰囲気を確認しましょう。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const v=$('d').value;if(!v){$('big').textContent='0';show();return;}
    const target=new Date(v+'T00:00:00'),today=new Date();today.setHours(0,0,0,0);
    const days=Math.round((target-today)/86400000),months=days/30.4;
    $('sub').textContent=`挙式希望日：${v}`;
    let j;if(months>=10)j='⏳ 余裕をもって準備できます。理想の式場・日取りを選べる好タイミング。';
    else if(months>=6)j='👍 標準的な準備期間。今から式場探しを始めれば安心です。';
    else if(months>=3)j='⚡ ややタイト。人気の式場は早く動きましょう。少人数婚も選択肢に。';
    else if(months>=0)j='🔥 かなりタイト。短期対応の式場やフォト/少人数婚がおすすめ。すぐ相談を。';
    else j='その日付は過去です。未来の日付を入れてください。';
    $('judge').textContent=j;
    $('months').textContent=days>=0?num(months)+'ヶ月':'—';
    function back(m){const d=new Date(target);d.setMonth(d.getMonth()-m);return `${d.getFullYear()}/${d.getMonth()+1}月ごろ`;}
    $('venue').textContent=days>=0?back(10):'—';$('invite').textContent=days>=0?back(2.5|0)+'〜':'—';
    SHARE=`結婚式 準備スケジュール診断、挙式まであと${num(days)}日（準備${num(months)}ヶ月）でした📋`;
    show();anim(days);}
  function anim(v){const el=$('big'),t0=performance.now();(function s(n){const p=Math.min(1,(n-t0)/800),e=1-Math.pow(1-p,3);el.textContent=Math.round(v*e).toLocaleString('ja-JP');if(p<1)requestAnimationFrame(s);})(performance.now());}''')

# ============================================================
def render():
    for s in SIMS:
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
    print(f'wedding done. {len(SIMS)} sims.')
