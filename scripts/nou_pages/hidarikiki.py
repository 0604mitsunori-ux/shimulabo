# -*- coding: utf-8 -*-
# 十人十脳 第17話「左利き」と連動（2026-11-05 新規）
PAGE = {
    "slug": "hidarikiki",
    "title": "利き手・利き目・利き足チェック｜あなたは本当に右利き？左利きは10人に1人｜シミュラボ",
    "desc": "字を書く手だけが利き手じゃない？投げる・はさみ・歯みがきなど8つの動作で利き手の度合いを数字で出し、利き足と利き目もチェック。約200万人分を調べた研究で分かった「左利きは10人に1人」の話も解説。診断ではありません。",
    "og_title": "あなたは本当に右利き？｜利き手・利き目・利き足チェック",
    "og_desc": "8つの動作で利き手の度合いを数字に。利き目と利き足も。",
    "ld_name": "利き手・利き目・利き足チェック",
    "h1": "利き手・利き目・利き足チェック（あなたは本当に右利き？）",
    "lead": "字は右手で書くけれど、ボールは左で投げる。そんな人は意外といます。利き手は「右か左か」の2つではなく、度合いで考えることができます。8つの動作と、利き足・利き目のチェックに答えてください。約2分です。",
    "start_h2": "✋ どっちの手を使う？",
    "start_text": "ふだん、その動作をするときに使う側を選んでください。分からないときは、実際にやるふりをしてみると分かりやすいです。",
    "tag": "利き手",
    "card_label": "利き手・利き目・利き足チェックの結果",
    "card_footer": "あなたは本当に右利き？ → shimulabo.com",
    "stage_html": """
      <div class="syn-top"><span id="part">利き手</span><span id="count">1 / 11</span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div class="syn-big" id="em" style="font-size:56px;"></div>
      <div class="syn-ask" id="q" style="font-size:18px;font-weight:700;color:#EEEAE3;min-height:3em;line-height:1.7;"></div>
      <div class="syn-btns" id="opts" style="grid-template-columns:repeat(3,1fr);"></div>
    """,
    "js": r"""
  const $ = NOU.$;
  // 利き手8問（研究でよく使われる利き手の質問票の考え方をもとに、このページで作った動作）＋利き足2問＋利き目1問
  const Q = [
    ['h', '✍️', '字を書く'], ['h', '🎨', '絵をかく'], ['h', '⚾', 'ボールを投げる'], ['h', '✂️', 'はさみを使う'],
    ['h', '🪥', '歯ブラシを持つ'], ['h', '🥄', 'スプーンを持つ'], ['h', '🔨', 'かなづちでくぎを打つ'], ['h', '🫙', 'びんのふたを回す手'],
    ['f', '⚽', 'ボールをける足'], ['f', '🪜', '階段の1段目にのせる足'],
    ['e', '👁️', '両手で小さな三角の窓を作り、遠くの物をその中に入れて、片目ずつ閉じてみて。物が窓の中に残ったのは、どっちの目を開けたとき？'],
  ];
  let k = 0, ans = [];
  function show() { const [t, e, q] = Q[k]; $('part').textContent = t === 'h' ? '利き手' : t === 'f' ? '利き足' : '利き目'; $('em').textContent = e; $('q').textContent = q;
    $('count').textContent = (k + 1) + ' / ' + Q.length; $('bar').style.width = (k / Q.length * 100) + '%';
    $('opts').innerHTML = [['左', 'L'], ['どちらも', 'B'], ['右', 'R']].map(([s, v]) => `<button type="button" data-v="${v}">${s}</button>`).join(''); }
  $('opts').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; ans.push(b.dataset.v); k++; if (k < Q.length) show(); else done(); });
  const side = v => v === 'R' ? '右' : v === 'L' ? '左' : 'どちらも';
  function done() {
    const h = ans.slice(0, 8), R = h.filter(v => v === 'R').length, L = h.filter(v => v === 'L').length;
    const LQ = Math.round((R - L) / 8 * 100);   // −100（左）〜 +100（右）
    const f = ans.slice(8, 10), fR = f.filter(v => v === 'R').length, fL = f.filter(v => v === 'L').length;
    const foot = fR > fL ? 'R' : fL > fR ? 'L' : 'B', eye = ans[10], hand = LQ >= 50 ? 'R' : LQ <= -50 ? 'L' : 'B';
    const T = hand === 'R' ? ['🫱', '右利き', '多くの動作を右手でしています。'] : hand === 'L' ? ['🫲', '左利き', '多くの動作を左手でしています。左利きは、およそ10人に1人です。'] : ['🙌', '両手を使い分けるタイプ', '動作によって右と左を使い分けています。'];
    const cross = hand !== 'B' && eye !== 'B' && hand !== eye ? `<p style="font-size:14px;margin:6px 0;">利き手と利き目が逆でした。これはめずらしいことではなく、たとえば右利きの人でも、3人に1人くらいは左目が利き目だと言われています。</p>` : '';
    NOU.finish({
      label: '利き手の度合い（−100＝左 … ＋100＝右）', big: (LQ > 0 ? '+' : '') + LQ, unit: '', emoji: T[0], typeName: T[1], advice: T[2],
      extraHTML: cross + `<div class="syn-rows"><div><span class="k">✋ 利き手</span><span class="v">${side(hand)}（右${R}・左${L}・どちらも${8 - R - L}）</span></div><div><span class="k">🦶 利き足</span><span class="v">${side(foot)}</span></div><div><span class="k">👁️ 利き目</span><span class="v">${side(eye)}</span></div></div><p style="font-size:12px;color:var(--ink-3);">度合いの計算と、右利き・左利きの区切り（±50）は、このページで決めた目安です。</p>`,
      share: `利き手・利き目・利き足チェックやってみた✋ 利き手の度合い${LQ > 0 ? '+' : ''}${LQ}で「${T[1]}」、利き足は${side(foot)}・利き目は${side(eye)}でした。あなたは本当に右利き？`,
      cardTitle: 'わたしの利き手・利き足・利き目', cardLine: `利き手の度合い ${LQ > 0 ? '+' : ''}${LQ}`,
      draw: (x, R2) => {
        const items = [['✋', '利き手', hand], ['🦶', '利き足', foot], ['👁️', '利き目', eye]], cw = (R2.w - 2 * 30) / 3;
        items.forEach(([e, n, v], i) => { const xx = R2.x + i * (cw + 30), y = R2.y + 40;
          x.fillStyle = '#2A3C43'; x.beginPath(); x.roundRect(xx, y, cw, 400, 28); x.fill();
          x.textAlign = 'center'; x.fillStyle = '#EEEAE3'; x.font = '400 110px ' + R2.F; x.fillText(e, xx + cw / 2, y + 150);
          x.font = '800 40px ' + R2.F; x.fillText(n, xx + cw / 2, y + 230);
          x.fillStyle = v === 'B' ? '#F5BB5C' : '#4FC6B4'; x.font = '900 72px ' + R2.F; x.fillText(side(v), xx + cw / 2, y + 340); });
      },
    });
  }
  function start() { k = 0; ans = []; NOU.startPanels(); show(); }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "字を書く・投げる・はさみなど8つの動作でどちらの手を使うかから利き手の度合いを出し、利き足2問と、両手で作る三角の窓を使った利き目のチェックを合わせたセルフテストです。",
    "article": """
    <h2>左利きは、およそ10人に1人</h2>
    <p>世界中の研究をまとめて、200万人をこえる人の利き手を調べた研究があります（Papadatou-Pastou ほか 2020）。左利きの割合は、どこまでを左利きと数えるかで変わり、<b>9.3%〜18.1%</b>。いちばん確かな見積もりは<b>10.6%</b>で、およそ10人に1人でした。</p>
    <p>数え方で割合が変わるのは、「字は右、投げるのは左」のように、<b>動作によって使う手が変わる人</b>がいるからです。きびしく「ほとんどの動作を左でする人」だけを数えると少なく、「右利きではない人」まで数えると多くなります。</p>

    <h2>利き手は「度合い」で測れる</h2>
    <p>利き手を調べる質問票として、1971年に作られた「エディンバラ利き手テスト」が今もよく使われています（Oldfield 1971）。いくつもの動作で使う手を答え、右と左の差から、利き手の度合いを数字で出すしくみです。</p>
    <p>このページの8つの動作も、その考え方をもとに作りました。右の動作が多いほど＋100に、左が多いほど−100に近づきます。</p>

    <h2>利き目と利き手は、同じとは限らない</h2>
    <p>目にも「利き目」があります。両手で作った窓の中に遠くの物を入れて片目ずつ閉じたとき、物が窓の中に残るほうの目が利き目です。</p>
    <p>利き手と利き目の関係を、54の研究・5万人あまりのデータでまとめた研究があります（Bourassa ほか 1996）。利き手と利き目は関係はあるものの、かならずしも同じではなく、<b>右利きの人でも3人に1人くらいは左目が利き目</b>だと報告されています。</p>

    <h2>「左利きは天才」は本当？</h2>
    <p>左利きについては、いろいろなうわさがあります。でも、利き手だけで頭のよさや性格が決まるわけではありません。このテストは、あなたの体の「使い分けのくせ」を知るためのものです。</p>
""",
    "faq": [
        ("両手利きはどのくらいいますか？", "どの動作も両方の手で同じようにできる人は、とても少ないと考えられています。このテストの「両手を使い分けるタイプ」は、動作によって使う手が変わる人のことです。"),
        ("左利きを右利きに直したほうがいいですか？", "このページでは、そうした考えはすすめていません。利き手は、生まれつきの面と育ち方の面の両方が関係していると考えられています。"),
        ("利き目の調べ方がよく分かりません。", "両手の親指と人さし指で小さな三角の窓を作り、腕をのばして遠くの物を窓の中に入れます。右目だけ・左目だけで見て、物が窓の中に残ったほうが利き目です。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Papadatou-Pastou M, Ntolka E, Schmitz J, ほか (2020). Human handedness: A meta-analysis. <i>Psychological Bulletin</i>, 146(6), 481–524.",
        "Oldfield RC (1971). The assessment and analysis of handedness: The Edinburgh inventory. <i>Neuropsychologia</i>, 9(1), 97–113.",
        "Bourassa DC, McManus IC, Bryden MP (1996). Handedness and eye-dominance: A meta-analysis of their relationship. <i>Laterality</i>, 1(1), 5–34.",
    ],
    "related": [("houkou-kankaku", "🧭", "方向感覚テスト（頭の中で図形を回せる？）"), ("shikou-type", "🧠", "絵で考える人・言葉で考える人テスト"), ("sakushi-kaiten", "💃", "回るダンサーの錯視テスト"), ("reaction-test", "⚡", "反応速度テスト")],
}
