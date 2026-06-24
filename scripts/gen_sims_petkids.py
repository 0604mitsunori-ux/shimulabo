# -*- coding: utf-8 -*-
"""シミュラボ：ペット2本＋育児2本。犬/猫の年齢人間換算（cat=ペット）、子供の身長予測/子供の肥満度（cat=子ども・育児）。
gen_sims_tool TPL流用。seo_internal.py / gen_images.py のauto-importに 'gen_sims_petkids' を追加。
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq
from gen_sims_tool import TPL, viz
from sim_quiz import make_engines
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CAT = 'ペット'
SIMS = []
tally_quiz, num_quiz, band_quiz, add, q_article, render = make_engines(SIMS, CAT, TPL, viz)
ANIM = r'''  function anim(v){const el=$('big'),t0=performance.now();(function s(n){const p=Math.min(1,(n-t0)/700),e=1-Math.pow(1-p,3);el.textContent=(Math.round(v*e*10)/10).toLocaleString('ja-JP');if(p<1)requestAnimationFrame(s);else el.textContent=(Math.round(v*10)/10).toLocaleString('ja-JP');})(performance.now());}'''

# ============================================================
# 1. 犬の年齢 人間換算（犬 年齢 人間 4200/KD1/TP14000）★★
# ============================================================
add(id='inu-nenrei', emoji='🐶',
  title='犬の年齢 人間換算｜うちの子は人間で何歳？サイズ別に計算｜シミュラボ',
  desc='犬の年齢とサイズ（小型・中型・大型）を入れるだけで、人間に換算すると何歳かが分かる無料ツール。大型犬ほど歳をとるのが早い点も反映。愛犬の健康管理に。',
  ogtitle='犬の年齢 人間換算｜人間で何歳？', ogdesc='犬の年齢とサイズから人間年齢に換算。大型ほど早い。',
  h1='犬の年齢 人間換算',
  lead='うちの子、人間でいうと何歳?犬の年齢とサイズを入れると、人間年齢に換算します。大型犬ほど歳をとるのが早いことも反映。健康管理の目安に。',
  inputs='''    <h2>🐶 愛犬の情報を入れる</h2>
    <div class="field"><label>犬の年齢 <span class="hint">歳（0.5など小数もOK）</span></label><input type="number" id="age" value="3" min="0" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>サイズ</label><select id="size"><option value="s" selected>小型犬（〜10kg）</option><option value="m">中型犬（10〜25kg）</option><option value="l">大型犬（25kg〜）</option></select></div>
    <button class="btn btn-primary" id="calcBtn">人間年齢に換算</button>''',
  result='''      <div class="label">人間に換算すると</div>
      <div class="big"><span id="big">0</span><span class="unit">歳</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="stage" style="text-align:left;margin-top:12px;">—</div>''',
  article='''    <div class="note"><strong>換算の目安</strong><br>小型・中型犬：1歳＝人間15歳、2歳＝24歳、以降1年ごとに＋4歳<br>大型犬：1歳＝人間12歳、2歳＝22歳、以降1年ごとに＋7歳</div>
    <h2>犬の年齢の数え方</h2>
    <p>犬は人間よりずっと速く歳をとります。最初の1〜2年で一気に成長し、その後はサイズによってペースが変わります。小型・中型犬は比較的ゆっくり、大型犬は1年で人間の約7歳分と早く歳を重ねます。7歳ごろからシニア期に入るとされ、健康診断やフードの見直しが大切になります。あくまで一般的な目安です。</p>
    <h2>よくある質問</h2>'''+faq([
      ('なぜ大型犬は早い？','大型犬は成長も老化も早い傾向があり、平均寿命も小型犬より短めです。'),
      ('シニアは何歳から？','一般に7歳ごろから。健康診断の頻度を上げるとよいとされます。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const a=Math.max(0,+$('age').value||0),sz=$('size').value;let hy;
    const big=(sz==='l');
    if(a<=0)hy=0;
    else if(a<=1)hy=(big?12:15)*a;
    else if(a<=2)hy=(big?12:15)+(big?10:9)*(a-1);
    else hy=(big?22:24)+(big?7:4)*(a-2);
    hy=Math.round(hy*10)/10;
    const stg=hy<13?'こども〜思春期':hy<40?'おとな（成犬）':hy<60?'中年期':'シニア期';
    $('sub').textContent=sel('size').text.split('（')[0]+'・'+a+'歳';
    $('stage').textContent='🐾 人間でいうと「'+stg+'」くらい。'+(stg==='シニア期'?'定期的な健康チェックを大切に。':'元気に過ごせる時期です。');
    SHARE='犬の年齢 人間換算、'+sel('size').text.split('（')[0]+'の'+a+'歳は人間で約'+hy+'歳でした🐶';show();anim(hy);}
'''+ANIM)

# ============================================================
# 2. 猫の年齢 人間換算（猫 年齢 人間 2800/KD2/TP35000）★★
# ============================================================
add(id='neko-nenrei', emoji='🐱',
  title='猫の年齢 人間換算｜うちの猫は人間で何歳？すぐ計算｜シミュラボ',
  desc='猫の年齢を入れるだけで、人間に換算すると何歳かが分かる無料ツール。1歳で人間の18歳、2歳で24歳、以降は1年ごとに＋4歳。愛猫のライフステージ管理に。',
  ogtitle='猫の年齢 人間換算｜人間で何歳？', ogdesc='猫の年齢を人間年齢に換算。ライフステージも表示。',
  h1='猫の年齢 人間換算',
  lead='うちの猫、人間でいうと何歳?猫の年齢を入れると、人間年齢に換算します。ライフステージの目安もチェック。健康管理の参考に。',
  inputs='''    <h2>🐱 愛猫の年齢を入れる</h2>
    <div class="field"><label>猫の年齢 <span class="hint">歳（0.5など小数もOK）</span></label><input type="number" id="age" value="3" min="0" step="0.5" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">人間年齢に換算</button>''',
  result='''      <div class="label">人間に換算すると</div>
      <div class="big"><span id="big">0</span><span class="unit">歳</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="stage" style="text-align:left;margin-top:12px;">—</div>''',
  article='''    <div class="note"><strong>換算の目安</strong><br>1歳＝人間18歳、2歳＝24歳、以降1年ごとに＋4歳（猫は犬よりサイズ差が小さく、おおむね共通）</div>
    <h2>猫の年齢の数え方</h2>
    <p>猫は最初の1年で人間の18歳ほどまで一気に成長し、2年で24歳、その後は1年ごとに約4歳ずつ歳を重ねます。7歳ごろから中年期、11歳ごろからシニア期に入るとされます。年齢に応じてフードや運動量、健康診断の頻度を見直すと、長く元気に過ごしやすくなります。あくまで一般的な目安です。</p>
    <h2>よくある質問</h2>'''+faq([
      ('室内飼いと外で違う？','一般に室内飼いの猫のほうが長生きしやすい傾向があります。'),
      ('シニアは何歳から？','11歳ごろからシニア期とされます。健康チェックを大切に。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const a=Math.max(0,+$('age').value||0);let hy;
    if(a<=0)hy=0;else if(a<=1)hy=18*a;else if(a<=2)hy=18+6*(a-1);else hy=24+4*(a-2);
    hy=Math.round(hy*10)/10;
    const stg=hy<18?'こども〜青年期':hy<44?'おとな（成猫）':hy<60?'中年期':'シニア期';
    $('sub').textContent='猫の'+a+'歳';
    $('stage').textContent='🐾 人間でいうと「'+stg+'」くらい。'+(stg==='シニア期'?'定期的な健康チェックを大切に。':'元気に過ごせる時期です。');
    SHARE='猫の年齢 人間換算、'+a+'歳は人間で約'+hy+'歳でした🐱';show();anim(hy);}
'''+ANIM)

# ============================================================
# 3. 子供の身長予測（子供 身長 予測 250/KD0/TP4000）cat=子ども・育児
# ============================================================
add(id='kodomo-shincho', emoji='📏', cat='子ども・育児',
  title='子供の身長予測｜両親の身長から将来の身長を予測｜シミュラボ',
  desc='お父さん・お母さんの身長と子どもの性別から、将来の成人身長の目安を予測する無料ツール（ターゲット身長法）。あくまで遺伝からの目安として参考に。',
  ogtitle='子供の身長予測｜両親の身長から計算', ogdesc='両親の身長から子どもの将来の成人身長の目安を予測。',
  h1='子供の身長予測',
  lead='うちの子、将来どれくらい伸びる?お父さん・お母さんの身長から、成人身長の目安を予測します（ターゲット身長法）。遺伝からのおおよその目安に。',
  inputs='''    <h2>📏 両親の身長を入れる</h2>
    <div class="row"><div class="field"><label>お父さんの身長 <span class="hint">cm</span></label><input type="number" id="f" value="172" min="0" inputmode="decimal"></div>
    <div class="field"><label>お母さんの身長 <span class="hint">cm</span></label><input type="number" id="m" value="158" min="0" inputmode="decimal"></div></div>
    <div class="field"><label>お子さんの性別</label><select id="sex"><option value="boy" selected>男の子</option><option value="girl">女の子</option></select></div>
    <button class="btn btn-primary" id="calcBtn">将来の身長を予測</button>''',
  result='''      <div class="label">予測される成人身長</div>
      <div class="big"><span id="big">0</span><span class="unit">cm</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">目安の範囲（±9cm）</div><div class="v accent" id="range">—</div></div></div>''',
  article='''    <div class="note"><strong>計算式（ターゲット身長法）</strong><br>男の子 ＝（父の身長 ＋ 母の身長 ＋ 13）÷ 2<br>女の子 ＝（父の身長 ＋ 母の身長 − 13）÷ 2</div>
    <h2>子供の身長予測について</h2>
    <p>子どもの身長は遺伝の影響が大きいとされ、両親の身長から目安を予測できます。よく使われる「ターゲット身長法」では、男の子は両親の平均に＋6.5cm、女の子は−6.5cm（式では±13を2で割る）で計算します。ただし、実際の身長は栄養・睡眠・運動・生活習慣でも変わり、目安からおよそ±9cmの幅があります。あくまで参考としてお楽しみください。</p>
    <h2>よくある質問</h2>'''+faq([
      ('必ずこの身長になる？','いいえ。遺伝からの目安で、生活習慣などで±9cmほど変わります。'),
      ('身長を伸ばすには？','十分な睡眠・バランスの良い食事・適度な運動が大切とされます。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const f=Math.max(0,+$('f').value||0),m=Math.max(0,+$('m').value||0),boy=$('sex').value==='boy';
    const t=(f+m+(boy?13:-13))/2;const tr=Math.round(t*10)/10;
    $('sub').textContent=(boy?'男の子':'女の子')+'・父'+f+'/母'+m+'cm';
    $('range').textContent=(Math.round((t-9)*10)/10)+' 〜 '+(Math.round((t+9)*10)/10)+' cm';
    SHARE='子供の身長予測、'+(boy?'男の子':'女の子')+'の予測成人身長は約'+tr+'cmでした📏';show();anim(tr);}
'''+ANIM)

# ============================================================
# 4. 子供の肥満度（bmi 子供 250/KD2/TP14000）カウプ/ローレル cat=子ども・育児
# ============================================================
add(id='kodomo-himan', emoji='👶', cat='子ども・育児',
  title='子供の肥満度チェック｜カウプ指数・ローレル指数で判定｜シミュラボ',
  desc='お子さんの年齢・身長・体重から、肥満度の指数（乳幼児はカウプ指数、学童はローレル指数）を計算し、やせ〜肥満の判定を表示する無料ツール。成長の目安に。',
  ogtitle='子供の肥満度チェック｜カウプ・ローレル指数', ogdesc='年齢・身長・体重からカウプ/ローレル指数で肥満度を判定。',
  h1='子供の肥満度チェック',
  lead='うちの子の体型、標準?年齢・身長・体重から、子ども向けの肥満度指数（乳幼児＝カウプ指数、学童＝ローレル指数）を計算して判定します。成長の目安に。',
  inputs='''    <h2>👶 お子さんの情報を入れる</h2>
    <div class="field"><label>年齢区分</label><select id="kind"><option value="kaup" selected>乳幼児（3か月〜5歳）→カウプ指数</option><option value="rohrer">学童（6歳〜中学生）→ローレル指数</option></select></div>
    <div class="row"><div class="field"><label>身長 <span class="hint">cm</span></label><input type="number" id="h" value="100" min="0" inputmode="decimal"></div>
    <div class="field"><label>体重 <span class="hint">kg</span></label><input type="number" id="w" value="15" min="0" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">肥満度を判定</button>''',
  result='''      <div class="label">指数</div>
      <div class="big"><span id="big">0</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="judge" style="text-align:left;margin-top:12px;">—</div>''',
  article='''    <div class="note"><strong>計算式</strong><br>カウプ指数 ＝ 体重(g) ÷ 身長(cm)² × 10　（標準：15〜19）<br>ローレル指数 ＝ 体重(kg) ÷ 身長(m)³ × 10　（標準：115〜145）</div>
    <h2>子供の肥満度の指数</h2>
    <p>大人のBMIにあたる指標が、子どもでは年齢で使い分けられます。乳幼児は「カウプ指数」（標準15〜19）、学童期は「ローレル指数」（標準115〜145）です。子どもは成長期で体型が変わりやすいため、1回の数値だけでなく、母子手帳の成長曲線とあわせて見ることが大切です。気になる場合は、かかりつけ医や学校健診で相談しましょう。'''+'※あくまで目安です。成長には個人差があります。'+'''</p>
    <h2>よくある質問</h2>'''+faq([
      ('カウプとローレルの違いは？','対象年齢が違います。乳幼児はカウプ、学童はローレルを使います。'),
      ('数値が外れたら心配？','成長曲線とあわせて見ます。気になる場合は健診や受診で相談を。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const kind=$('kind').value,h=Math.max(1,+$('h').value||0),w=Math.max(0,+$('w').value||0);
    let idx,judge,cl='good';
    if(kind==='kaup'){idx=w*1000/(h*h)*10;idx=Math.round(idx*10)/10;
      judge=idx<13?'やせすぎ':idx<15?'やせぎみ':idx<19?'標準':idx<22?'太りぎみ':'太りすぎ';
      $('sub').textContent='カウプ指数（乳幼児・標準15〜19）';}
    else{const m=h/100;idx=w/(m*m*m)*10;idx=Math.round(idx*10)/10;
      judge=idx<100?'やせすぎ':idx<115?'やせぎみ':idx<=145?'標準':idx<=160?'太りぎみ':'太りすぎ';
      $('sub').textContent='ローレル指数（学童・標準115〜145）';}
    if(judge.indexOf('すぎ')>=0)cl='warn';$('judge').className='alert '+cl;
    $('judge').textContent=(cl==='warn'?'⚠️ ':'✅ ')+'判定：'+judge+'。子どもは成長で変わりやすいので、成長曲線とあわせて見ましょう。';
    SHARE='子供の肥満度チェック、指数'+idx+'（'+judge+'）でした👶';show();anim(idx);}
'''+ANIM)

if __name__=='__main__':
    render()
    print(f'petkids done. {len(SIMS)} sims.')
