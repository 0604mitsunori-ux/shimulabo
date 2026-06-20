# -*- coding: utf-8 -*-
"""シミュラボ：マーケティング補充5本（SEO/AIO/店舗経営）。"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGO = '''<span class="mark">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M9 3h6M10 3v5.2L5.4 16.4A2.4 2.4 0 0 0 7.5 20h9a2.4 2.4 0 0 0 2.1-3.6L14 8.2V3" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M7.7 14.5h8.6" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/>
          <circle cx="10.3" cy="16.7" r="1" fill="#fff"/>
          <circle cx="13.4" cy="17.4" r=".7" fill="#fff"/>
        </svg>
      </span>'''

TPL = '''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<meta name="description" content="__DESC__">
<meta property="og:title" content="__OGTITLE__">
<meta property="og:description" content="__OGDESC__">
<meta property="og:type" content="website">
<link rel="stylesheet" href="../../assets/style.css">
</head>
<body>

<header class="site-header">
  <div class="inner">
    <a class="brand" href="../../index.html">
      ''' + LOGO + '''
      <span class="name">シミュ<b>ラボ</b></span>
    </a>
    <span class="spacer"></span>
    <a class="back" href="../../index.html">← 一覧へ</a>
  </div>
</header>

<main class="wrap">

  <div class="sim-head">
    <div class="cat">__CAT__</div>
    <h1>__H1__</h1>
    <p class="lead">__LEAD__</p>
  </div>

  <section class="panel">
__INPUTS__
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
__RESULT__
      <div style="text-align:center;"><span id="shareCount" class="share-count" style="display:none"></span></div>
      <div class="share-row">
        <button class="btn btn-x" id="shareBtn">𝕏 で結果をシェア</button>
        <button class="btn btn-ghost" id="copyBtn">結果をコピー</button>
      </div>
    </div>
  </section>

  <article class="article">
__ARTICLE__
  </article>

  <section class="req-banner">
    <h2>💡 こんなシミュも見てみたい？</h2>
    <p>あなたの「これ数字で見たい」を送ってください。投票で人気の案から実際に作ります。</p>
    <a class="btn btn-primary" style="width:auto;display:inline-flex;padding:14px 30px;" href="../../request/index.html">リクエストする →</a>
    <div style="margin-top:12px;"><a href="../../board/index.html" style="font-size:13px;font-weight:800;">🗳️ みんなのリクエストに投票する →</a></div>
  </section>

</main>

<footer class="site-footer">
  <div class="inner">
    <p><a href="../../index.html">← シミュラボ トップへ戻る</a></p>
    <p style="margin-top:10px;opacity:.7">© 2026 シミュラボ</p>
  </div>
</footer>

<script>
(() => {
  const $ = (id) => document.getElementById(id);
  const yen = (n) => '¥' + Math.round(n).toLocaleString('ja-JP');
  const num = (n) => Math.round(n).toLocaleString('ja-JP');
  const sel = (id) => { const e=$(id); return e.options[e.selectedIndex]; };
  let SHARE = '';
  function anim(el, from, to, dur, dec){ const t0=performance.now(); (function s(n){const p=Math.min(1,(n-t0)/dur);const e=1-Math.pow(1-p,3);const v=from+(to-from)*e;el.textContent=(dec!=null?v.toFixed(dec):Math.round(v).toLocaleString('ja-JP'));if(p<1)requestAnimationFrame(s);})(performance.now()); }
  function show(){ $('resultPanel').style.display=''; $('resultPanel').scrollIntoView({behavior:'smooth',block:'start'}); }
__JS__
  $('calcBtn').addEventListener('click', calc);
  $('shareBtn').addEventListener('click', () => window.open('https://twitter.com/intent/tweet?text='+encodeURIComponent(SHARE)+'&url='+encodeURIComponent(location.href)+'&hashtags='+encodeURIComponent('シミュラボ'),'_blank','noopener'));
  $('copyBtn').addEventListener('click', async () => { try{ await navigator.clipboard.writeText(SHARE+'\\n'+location.href); $('copyBtn').textContent='コピーしました ✓'; setTimeout(()=>$('copyBtn').textContent='結果をコピー',1600);}catch{alert(SHARE);} });
})();
</script>
<script src="../../assets/share-counter.js"></script>
<script>ShareCounter.initSim({ simId:'__ID__', badgeEl:document.getElementById('shareCount'), shareBtnIds:['shareBtn'] });</script>
</body>
</html>
'''

def faq(qa):
    return '<dl class="faq">' + ''.join(f'<dt>{q}</dt><dd>{a}</dd>' for q,a in qa) + '</dl>'

MKT='マーケティング'
SIMS=[]

# 1. 検索順位別クリック率シミュレーター（SEO）
SIMS.append(dict(id='seo-ctr', cat=MKT, emoji='🔍',
  title='検索順位別クリック率シミュレーター｜順位が上がると流入はどれだけ増える？｜シミュラボ',
  desc='月間検索ボリュームと検索順位から、想定クリック率（CTR）と月間クリック数を試算。現在順位から目標順位に上げると流入がどれだけ増えるかが分かる無料のSEOシミュレーター。',
  ogtitle='検索順位別クリック率シミュレーター｜順位で流入はどう変わる？', ogdesc='検索ボリュームと順位から、想定クリック数と順位アップの効果を試算。',
  h1='検索順位別クリック率シミュレーター',
  lead='検索で何位に入るかで、流入は大きく変わります。月間検索数と順位から、想定クリック数を試算。今の順位から上げたときの伸びも分かります。',
  inputs='''    <h2>🔍 条件を入れる</h2>
    <div class="field"><label>月間検索ボリューム <span class="hint">（そのキーワードが月に検索される回数）</span></label><input type="number" id="vol" value="10000" min="0" inputmode="numeric"></div>
    <div class="row"><div class="field"><label>現在の検索順位 <span class="hint">（位）</span></label><input type="number" id="cur" value="8" min="1" max="100" inputmode="numeric"></div>
    <div class="field"><label>目標の検索順位 <span class="hint">（位）</span></label><input type="number" id="goal" value="3" min="1" max="100" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">流入の変化を見る</button>''',
  result='''      <div class="label">目標順位での 月間クリック数</div>
      <div class="big"><span id="big">0</span><span class="unit">クリック</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">現在のクリック</div><div class="v" id="now">—</div></div>
      <div class="stat"><div class="k">増えるクリック</div><div class="v accent" id="up">—</div></div>
      <div class="stat"><div class="k">目標順位のCTR</div><div class="v" id="ctr">—</div></div></div>''',
  article='''    <h2>計算の考え方</h2>
    <div class="note"><strong>計算式</strong><br>月間クリック ＝ 月間検索ボリューム × 順位別CTR<br>順位別CTRは一般的な実測値（1位約28％／3位約11％／10位約2％…）にもとづく目安です。</div>
    <p>1位と10位ではクリック率に10倍以上の差。とくに1〜3位の「上位3枠」に入れるかどうかで流入が一変します。検索ボリュームの大きいキーワードほど、順位アップの効果は大きくなります。</p>
    <h2>よくある質問</h2>'''+faq([('CTRは固定値ですか？','業種・検索意図・リッチリザルトの有無で変わります。本ツールは一般的な平均カーブによる概算です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function ctr(p){
    const t={1:28,2:15,3:11,4:8,5:6,6:4.5,7:3.5,8:3,9:2.5,10:2.2};
    p=Math.max(1,Math.round(p));
    if(p<=10) return t[p];
    if(p<=20) return Math.max(0.4, 1.2-(p-10)*0.08);
    return 0.3;
  }
  function calc(){
    const vol=Math.max(0,+$('vol').value||0), cur=Math.max(1,+$('cur').value||1), goal=Math.max(1,+$('goal').value||1);
    const cc=vol*ctr(cur)/100, gc=vol*ctr(goal)/100, up=gc-cc;
    $('sub').textContent=`${cur}位（CTR${ctr(cur)}%）→ ${goal}位（CTR${ctr(goal)}%）`;
    $('now').textContent=num(cc)+'回'; $('up').textContent=(up>=0?'+':'')+num(up)+'回'; $('ctr').textContent=ctr(goal)+'%';
    SHARE=`検索${cur}位→${goal}位で、月間クリックが${num(cc)}→${num(gc)}回に🔍（月+${num(up)}回）\\n上位3枠の威力よ。👇`;
    show(); anim($('big'),0,gc,900);
  }'''))

# 2. 検索流入のお金換算メーター（SEO）
SIMS.append(dict(id='seo-kachi', cat=MKT, emoji='💰',
  title='検索流入のお金換算メーター｜あなたのSEO流入、広告で買うといくら？｜シミュラボ',
  desc='月間の自然検索クリック数とクリック単価（CPC）から、同じ流入を広告で買った場合の金額に換算。SEO・コンテンツが生む「資産価値」を可視化する無料シミュレーター。',
  ogtitle='検索流入のお金換算メーター｜SEO流入を広告費に換算', ogdesc='自然検索のクリック数を広告費に換算して、SEOの資産価値を可視化。',
  h1='検索流入のお金換算メーター',
  lead='自然検索からの流入は「無料」に見えて、実は広告で買えば大きな金額に。月間クリック数とクリック単価から、SEOが生んでいる価値をお金に換算します。',
  inputs='''    <h2>💰 条件を入れる</h2>
    <div class="field"><label>月間の自然検索クリック数 <span class="hint">（Search Consoleのクリック数など）</span></label><input type="number" id="clk" value="3000" min="0" inputmode="numeric"></div>
    <div class="field"><label>クリック単価（CPC） <span class="hint">（円・同じ流入を広告で買うときの1クリック単価）</span></label><input type="number" id="cpc" value="120" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">広告換算の価値を見る</button>''',
  result='''      <div class="label">この検索流入を 広告で買うと（月）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">年間の換算価値</div><div class="v accent" id="yr">—</div></div>
      <div class="stat"><div class="k">クリック単価</div><div class="v" id="cpcv">—</div></div>
      <div class="stat"><div class="k">月間クリック</div><div class="v" id="clkv">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>広告換算の価値 ＝ 月間クリック数 × クリック単価（CPC）<br>年間 ＝ 月額 × 12</div>
    <p>広告は出稿をやめれば流入はゼロになりますが、SEOで積み上げた検索順位は<strong>記事が残るかぎり流入を生み続けるストック資産</strong>です。「広告ならいくら払うはずだったか」で見ると、コンテンツの価値が分かりやすくなります。</p>
    <h2>よくある質問</h2>'''+faq([('CVや売上は含まれますか？','いいえ。本ツールは「流入を広告で買った場合の金額」換算です。実際の売上は別途CVR・客単価で見てください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const clk=Math.max(0,+$('clk').value||0), cpc=Math.max(0,+$('cpc').value||0);
    const m=clk*cpc, y=m*12;
    $('sub').textContent=`月${num(clk)}クリック × CPC${num(cpc)}円`;
    $('yr').textContent=yen(y); $('cpcv').textContent=num(cpc)+'円'; $('clkv').textContent=num(clk)+'回';
    SHARE=`うちの自然検索の流入、広告で買ったら月${yen(m)}・年${yen(y)}分の価値だった💰\\nSEOはストック資産。👇`;
    show(); anim($('big'),0,m,900);
  }'''))

# 3. ゼロクリック検索シミュレーター（AIO）
SIMS.append(dict(id='zero-click', cat=MKT, emoji='📉',
  title='ゼロクリック検索シミュレーター｜AI Overviewで検索流入はどれだけ減る？｜シミュラボ',
  desc='現在の月間検索流入・AI Overview（AIによる要約）の表示率・クリック減少率から、AI検索時代に失われるクリック数を試算する無料シミュレーター。',
  ogtitle='ゼロクリック検索シミュレーター｜AI Overviewで流入はどう減る？', ogdesc='AI Overviewの表示率から、検索流入がどれだけ失われるかを試算。',
  h1='ゼロクリック検索シミュレーター',
  lead='検索結果の上にAIの要約（AI Overview）が出ると、サイトをクリックせず解決＝「ゼロクリック」が増えます。あなたの流入がどれだけ影響を受けるかを試算します。',
  inputs='''    <h2>📉 条件を入れる</h2>
    <div class="field"><label>現在の月間検索流入 <span class="hint">（クリック数）</span></label><input type="number" id="clk" value="5000" min="0" inputmode="numeric"></div>
    <div class="row"><div class="field"><label>AI Overviewが出る割合 <span class="hint">（％・検索のうちAI要約が表示される率）</span></label><input type="number" id="aio" value="40" min="0" max="100" inputmode="numeric"></div>
    <div class="field"><label>そのうちクリックされなくなる率 <span class="hint">（％）</span></label><input type="number" id="red" value="35" min="0" max="100" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">失われる流入を見る</button>''',
  result='''      <div class="label">毎月 失われる可能性のあるクリック</div>
      <div class="big"><span id="big">0</span><span class="unit">クリック</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">残るクリック（月）</div><div class="v" id="rem">—</div></div>
      <div class="stat"><div class="k">年間で失う</div><div class="v accent" id="yr">—</div></div>
      <div class="stat"><div class="k">減少率</div><div class="v" id="rate">—</div></div></div>''',
  article='''    <h2>計算の考え方</h2>
    <div class="note"><strong>計算式</strong><br>失うクリック ＝ 月間流入 ×（AI Overview表示率 ÷100）×（クリック減少率 ÷100）</div>
    <p>AI検索時代は「検索→自社サイト」の一本道が崩れ、AIの要約内で完結する検索が増えます。だからこそ、<strong>AIに引用・参照される情報設計（LLMO）</strong>と、指名検索・他チャネルの強化が重要になります。数字はあくまで仮定にもとづく目安です。</p>
    <h2>よくある質問</h2>'''+faq([('この減少は確定ですか？','いいえ。業種・キーワード・AIの仕様で大きく変わる仮定値です。傾向をつかむための目安として使ってください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const clk=Math.max(0,+$('clk').value||0), aio=Math.max(0,Math.min(100,+$('aio').value||0)), red=Math.max(0,Math.min(100,+$('red').value||0));
    const lost=clk*aio/100*red/100, rem=clk-lost, rate=clk>0?lost/clk*100:0;
    $('sub').textContent=`AI要約表示${aio}% × クリック減${red}%`;
    $('rem').textContent=num(rem)+'回'; $('yr').textContent=num(lost*12)+'回'; $('rate').textContent=rate.toFixed(1)+'%';
    SHARE=`AI検索（ゼロクリック）で、月間流入の約${rate.toFixed(0)}%・${num(lost)}クリックが消えるかも📉\\nAIに引用される設計＝LLMOが効いてくる。👇`;
    show(); anim($('big'),0,lost,900);
  }'''))

# 4. AI被引用ポテンシャル診断（AIO/LLMO）
SIMS.append(dict(id='ai-inyou', cat=MKT, emoji='🤖',
  title='AI被引用ポテンシャル診断｜あなたのコンテンツ、AIに引用される？｜シミュラボ',
  desc='独自情報・専門性・構造化・結論の明快さ・出典の5項目から、ChatGPTやAI検索に引用されやすいか（LLMOポテンシャル）を点数化する無料診断シミュレーター。',
  ogtitle='AI被引用ポテンシャル診断｜あなたのコンテンツ、AIに引用される？', ogdesc='5項目チェックで、AIに引用されやすいか（LLMO）を点数化。',
  h1='AI被引用ポテンシャル診断',
  lead='ChatGPTやAI検索は、信頼できて分かりやすいページを「引用」します。あなたのコンテンツがAIに引用されやすいかを、5つの観点で診断します。',
  inputs='''    <h2>🤖 5つの観点でチェック</h2>
    <div class="field"><label>① 独自の情報・一次データはある？</label><select id="q1"><option value="20">独自調査・体験・データがある</option><option value="10" selected>一部ある</option><option value="0">一般論が中心</option></select></div>
    <div class="field"><label>② 著者・運営者の専門性は明示されている？</label><select id="q2"><option value="20">著者情報・実績が明確</option><option value="8" selected>少し触れている</option><option value="0">不明</option></select></div>
    <div class="field"><label>③ 見出し・箇条書き・表・FAQで構造化されている？</label><select id="q3"><option value="20">しっかり構造化</option><option value="10" selected>ある程度</option><option value="0">文章のかたまり</option></select></div>
    <div class="field"><label>④ 結論・答えが先に明快に書かれている？</label><select id="q4"><option value="20">冒頭で結論提示</option><option value="10" selected>まあまあ</option><option value="0">読まないと分からない</option></select></div>
    <div class="field"><label>⑤ 出典・更新日が明記されている？</label><select id="q5"><option value="20">出典・更新日あり</option><option value="8" selected>どちらか</option><option value="0">なし</option></select></div>
    <button class="btn btn-primary" id="calcBtn">ポテンシャルを診断する</button>''',
  result='''      <div class="label">AI被引用ポテンシャル</div>
      <div class="big"><span id="big">0</span><span class="unit">点</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:18px;">—</div>''',
  article='''    <h2>AIに引用される条件（LLMO）</h2>
    <p>生成AIは、①独自性・一次情報 ②発信者の信頼性（E-E-A-T）③構造化された分かりやすさ ④結論の明快さ ⑤出典の明示、がそろった情報を引用しやすいと言われます。これらを満たすと、検索だけでなくAIの回答内でも名前が出やすくなります。</p>
    <div class="note">💡 まずは「結論を冒頭に」「独自データや体験を足す」「FAQと出典を付ける」の3つから。AIにも人にも親切なページが、これからの正解です。</div>
    <h2>よくある質問</h2>'''+faq([('点数が高ければ必ず引用されますか？','いいえ。あくまで一般的な傾向にもとづく自己診断の目安です。'),('入力内容は送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    let s=0; for(const id of ['q1','q2','q3','q4','q5']) s+=(+$(id).value||0);
    s=Math.max(0,Math.min(100,s));
    let a; if(s>=80)a='AIに引用されやすい優良コンテンツ。独自性・構造・信頼性がそろっています。この型を横展開しましょう🔥';
    else if(s>=55)a='ベースは good。あと一歩、独自データ・出典・結論の先出しを足すと引用率がぐっと上がります。';
    else if(s>=30)a='伸びしろ大。まずは「結論を冒頭に」「FAQと出典を追加」「見出しで構造化」から着手を。';
    else a='今はAIに見つけてもらいにくい状態。独自情報・専門性の明示・構造化を一から整えるのがおすすめです。';
    $('sub').textContent=`独自性・専門性・構造・結論・出典の5観点／100点満点`;
    $('adv').textContent='🤖 '+a;
    SHARE=`AI被引用ポテンシャル診断、私のコンテンツは${s}点でした🤖\\nAI検索時代、引用される設計が勝ち筋。あなたは何点？👇`;
    show(); anim($('big'),0,s,900);
  }'''))

# 5. リピート率改善シミュレーター（店舗経営）
SIMS.append(dict(id='repeat-rieki', cat=MKT, emoji='🔁',
  title='リピート率改善シミュレーター｜常連が増えると売上はどれだけ伸びる？｜シミュラボ',
  desc='月間の新規客数・客単価・リピート率から、リピート率を改善したときに年間売上がどれだけ伸びるかを試算する無料の店舗経営シミュレーター。',
  ogtitle='リピート率改善シミュレーター｜常連が増えると売上はどう伸びる？', ogdesc='リピート率を数％上げると年間売上がどれだけ伸びるかを試算。',
  h1='リピート率改善シミュレーター',
  lead='新規集客もだいじ。でも「もう一度来てもらう」ほうが、ずっと効率的。リピート率を少し上げると年間売上がどれだけ伸びるかを試算します。',
  inputs='''    <h2>🔁 条件を入れる</h2>
    <div class="row"><div class="field"><label>月間の新規客数 <span class="hint">（人）</span></label><input type="number" id="n" value="100" min="0" inputmode="numeric"></div>
    <div class="field"><label>客単価 <span class="hint">（円）</span></label><input type="number" id="p" value="3000" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>今のリピート率 <span class="hint">（％・また来る人の割合）</span></label><input type="number" id="r1" value="30" min="0" max="95" inputmode="numeric"></div>
    <div class="field"><label>改善後のリピート率 <span class="hint">（％）</span></label><input type="number" id="r2" value="40" min="0" max="95" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">売上の伸びを見る</button>''',
  result='''      <div class="label">リピート率改善で 増える年間売上</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">改善前の年間売上</div><div class="v" id="b1">—</div></div>
      <div class="stat"><div class="k">改善後の年間売上</div><div class="v accent" id="b2">—</div></div>
      <div class="stat"><div class="k">1顧客の来店回数</div><div class="v" id="visits">—</div></div></div>''',
  article='''    <h2>計算の考え方</h2>
    <div class="note"><strong>計算式</strong><br>1顧客あたりの平均来店回数 ＝ 1 ÷（1 − リピート率）<br>年間売上 ＝ 年間の新規客数 × 客単価 × 平均来店回数</div>
    <p>リピート率が30%から40%に上がるだけで、1人あたりの来店回数は約1.4回→約1.7回に。<strong>新規を増やすより、リピート率を数％上げるほうが利益インパクトが大きい</strong>のはこのためです。クチコミ・MEO・LINEなどの再来店施策が効いてきます。</p>
    <h2>よくある質問</h2>'''+faq([('この数字どおりになりますか？','いいえ。来店回数を単純な継続モデルで近似した目安です。業態により実際の挙動は異なります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const n=Math.max(0,+$('n').value||0), p=Math.max(0,+$('p').value||0);
    const r1=Math.max(0,Math.min(95,+$('r1').value||0))/100, r2=Math.max(0,Math.min(95,+$('r2').value||0))/100;
    const v1=1/(1-r1), v2=1/(1-r2);
    const s1=n*12*p*v1, s2=n*12*p*v2, diff=s2-s1;
    $('sub').textContent=`リピート率 ${Math.round(r1*100)}% → ${Math.round(r2*100)}%（来店回数 ${v1.toFixed(2)}→${v2.toFixed(2)}回）`;
    $('b1').textContent=yen(s1); $('b2').textContent=yen(s2); $('visits').textContent=v1.toFixed(2)+'→'+v2.toFixed(2)+'回';
    SHARE=`リピート率を${Math.round(r1*100)}%→${Math.round(r2*100)}%にすると、年間売上が約${yen(diff)}増える計算だった🔁\\n新規より常連、効くなぁ。👇`;
    show(); anim($('big'),0,diff,900);
  }'''))

for s in SIMS:
    d=os.path.join(ROOT,'sims',s['id']); os.makedirs(d,exist_ok=True)
    html=(TPL.replace('__TITLE__',s['title']).replace('__DESC__',s['desc'])
          .replace('__OGTITLE__',s['ogtitle']).replace('__OGDESC__',s['ogdesc'])
          .replace('__CAT__',s['cat']).replace('__H1__',s['h1']).replace('__LEAD__',s['lead'])
          .replace('__INPUTS__',s['inputs']).replace('__RESULT__',s['result'])
          .replace('__ARTICLE__',s['article']).replace('__JS__',s['js']).replace('__ID__',s['id']))
    with open(os.path.join(d,'index.html'),'w',encoding='utf-8') as f: f.write(html)
    print('created sims/'+s['id'])
print(f'done. {len(SIMS)} sims.')
