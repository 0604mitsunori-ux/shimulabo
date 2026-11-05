# -*- coding: utf-8 -*-
# 十人十脳 第24話「味覚（パクチー・スーパーテイスター）」と連動（2026-11-05 新規）
PAGE = {
    "slug": "mikaku-type",
    "title": "味覚タイプ診断｜パクチーが石けんの味？苦みに敏感なスーパーテイスター寄り？10問で試す｜シミュラボ",
    "desc": "パクチーが石けんの味に感じる人、コーヒーやゴーヤの苦みが人一倍つらい人。10の質問で、あなたの苦みの感じ方とパクチーへの反応を試すセルフテスト。2万人以上の遺伝子を調べたパクチーの研究や、苦みをとても強く感じる「スーパーテイスター」の研究も解説。診断ではありません。",
    "og_title": "パクチーが石けんの味になる人がいる｜味覚タイプ診断",
    "og_desc": "10の質問で、苦みの感じ方とパクチーへの反応を。あなたの舌はどのタイプ？",
    "ld_name": "味覚タイプ診断（パクチー・苦み）",
    "h1": "味覚タイプ診断（パクチーが石けんの味になる人がいる）",
    "lead": "同じ料理を食べても、「おいしい」と感じる人と「苦くて食べられない」と感じる人がいます。味の感じ方には、生まれつきのちがいもあることが分かってきました。10の質問に答えてください。約1分です。",
    "start_h2": "👅 10の質問に答えてね",
    "start_text": "ふだん食べたり飲んだりしたときの感じに、いちばん近いものを選んでください。食べたことがないものは「分からない」でOKです。",
    "tag": "味覚",
    "card_label": "味覚タイプ診断の結果",
    "card_footer": "パクチーが石けんの味？ → shimulabo.com",
    "stage_html": """
      <div class="syn-top"><span id="part">味の感じ方</span><span id="count">1 / 10</span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div class="syn-big" id="em" style="font-size:56px;"></div>
      <div class="syn-ask" id="q" style="font-size:18px;font-weight:700;color:#EEEAE3;min-height:3em;line-height:1.7;"></div>
      <div class="syn-btns c1" id="opts"></div>
    """,
    "js": r"""
  const $ = NOU.$;
  // b＝苦みの感じ方（8問）、p＝パクチー（2問）。問題はこのページで作ったもの
  const Q = [
    ['b', '☕', 'ブラックコーヒーの苦みは？'], ['b', '🥒', 'ゴーヤの苦みは？'], ['b', '🫑', 'ピーマンの苦みは？'], ['b', '🍊', 'グレープフルーツの苦みは？'],
    ['b', '🍵', '濃く入れた緑茶の苦みは？'], ['b', '🍫', 'カカオ分の多いチョコレートの苦みは？'], ['b', '🥬', '春菊やケールなど、苦みのある葉っぱの野菜は？'], ['b', '🌶️', '辛いものを食べたときの、舌の痛みは？'],
    ['p', '🌿', 'パクチー（コリアンダー）の味は？'], ['p', '🧼', 'パクチーを食べて、石けんやカメムシのような味・においを感じたことは？'],
  ];
  const OB = [['とても強く感じてつらい', 4], ['強く感じる', 3], ['少し感じる', 2], ['ほとんど感じない', 1], ['分からない', 0]];
  const OP = [[['大好き', 1], ['ふつう', 2], ['苦手', 3], ['食べられないほど苦手', 4], ['食べたことがない', 0]], [['よくある', 4], ['たまにある', 3], ['ない', 1], ['食べたことがない', 0]]];
  let k = 0, b = [], p = [];
  function show() { const [t, e, q] = Q[k]; $('em').textContent = e; $('q').textContent = q; $('part').textContent = t === 'b' ? '苦み・刺激の感じ方' : 'パクチー';
    $('count').textContent = (k + 1) + ' / 10'; $('bar').style.width = (k / 10 * 100) + '%';
    const o = t === 'b' ? OB : OP[k - 8]; $('opts').innerHTML = o.map(([s, v]) => `<button type="button" data-v="${v}">${s}</button>`).join(''); }
  $('opts').addEventListener('click', e => { const el = e.target.closest('button'); if (!el) return; (Q[k][0] === 'b' ? b : p).push(+el.dataset.v); k++; if (k < 10) show(); else done(); });
  function done() {
    const bs = b.filter(v => v > 0), avg = bs.length ? bs.reduce((s, v) => s + v, 0) / bs.length : 0, sc = Math.round(avg * 25);   // 25〜100
    const T = !bs.length ? ['❔', 'まだ分からないタイプ', '答えられた問題がありませんでした。'] : avg >= 3 ? ['👑', '苦みに敏感なタイプ（スーパーテイスター寄り）', '苦みや刺激を、人より強く感じやすいタイプかもしれません。苦い野菜は、ほかの味と合わせると食べやすくなります。']
            : avg >= 2 ? ['🙂', 'ふつうに感じるタイプ', '苦みを、ほどほどに感じるタイプです。']
            : ['🛡️', '苦みに強いタイプ', '苦みや刺激を、あまり感じにくいタイプです。'];
    const pk = p.filter(v => v > 0), soap = p[1] >= 3, pkHate = p[0] >= 3;
    const pkTxt = !pk.length ? 'パクチーは食べたことがないようです。' : soap ? 'パクチーに、石けんのような味やにおいを感じるタイプでした。パクチーの香りの感じ方には、においを感じる遺伝子のちがいも関係していると考えられています。' : pkHate ? 'パクチーは苦手なタイプでした。' : 'パクチーは平気なタイプでした。';
    NOU.finish({
      label: '苦み・刺激の感じやすさ（25〜100）', big: bs.length ? sc : '—', unit: bs.length ? ' / 100' : '', emoji: T[0], typeName: T[1], advice: T[2],
      extraHTML: `<p style="font-size:14px;margin:6px 0;">🌿 ${pkTxt}</p><div class="syn-rows">${Q.slice(0, 8).map((q, i) => `<div><span class="k">${q[1]} ${q[2].replace('は？', '')}</span><span class="v">${['分からない', 'ほとんど感じない', '少し', '強い', 'とても強い'][b[i]]}</span></div>`).join('')}</div><p style="font-size:12px;color:var(--ink-3);">スーパーテイスターかどうかは、研究では専用の苦い液や、舌の表面の観察で調べます。この結果は目安です。</p>`,
      share: `味覚タイプ診断やってみた👅 苦みの感じやすさ${bs.length ? sc : '—'}/100で「${T[1]}」でした。${soap ? 'パクチーは石けんの味がする派🧼' : ''}あなたの舌はどのタイプ？`,
      cardTitle: 'わたしの舌のタイプ', cardLine: `苦みの感じやすさ ${bs.length ? sc : '—'} / 100${soap ? '・パクチーは石けん味' : ''}`,
      draw: (x, R) => {
        const items = Q.slice(0, 8), cw = (R.w - 3 * 24) / 4;
        items.forEach((q, i) => { const xx = R.x + (i % 4) * (cw + 24), y = R.y + 30 + Math.floor(i / 4) * 260, v = b[i];
          x.fillStyle = '#2A3C43'; x.beginPath(); x.roundRect(xx, y, cw, 230, 22); x.fill();
          x.textAlign = 'center'; x.fillStyle = '#EEEAE3'; x.font = '400 80px ' + R.F; x.fillText(q[1], xx + cw / 2, y + 100);
          for (let d = 0; d < 4; d++) { x.fillStyle = v > d ? '#4FC6B4' : '#0D1417'; x.beginPath(); x.arc(xx + cw / 2 - 54 + d * 36, y + 175, 14, 0, Math.PI * 2); x.fill(); } });
      },
    });
  }
  function start() { k = 0; b = []; p = []; NOU.startPanels(); show(); }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "コーヒー・ゴーヤ・ピーマンなど8つの食べ物の苦みや刺激の感じ方と、パクチーについての2つの質問に答えるセルフテストです。問題はこのページで作っています。",
    "article": """
    <h2>パクチーが「石けんの味」になる人</h2>
    <p>パクチー（コリアンダー）を食べると、石けんのような味がすると言う人がいます。これは気のせいではないかもしれません。</p>
    <p>ヨーロッパ系の約1万4千人に「パクチーが石けんの味に感じるか」を聞き、遺伝子とくらべた研究があります（Eriksson ほか 2012）。すると、<b>においを感じるしくみの遺伝子が集まった場所</b>の近くに、関係のある遺伝子のちがいが1つ見つかりました。別の約1万2千人でも、パクチーの好き嫌いと関係していることが確かめられました。</p>
    <p>その近くには、パクチーの香りの成分によく反応する、においの受け取り役の遺伝子があります。ただし、この遺伝子のちがいで説明できる部分は小さく、好き嫌いは<b>食べ慣れているかどうか</b>などにも左右されると考えられています。</p>

    <h2>東アジアの人は、パクチー嫌いが多め？</h2>
    <p>カナダの20代の若者1,381人を調べた研究では、パクチーが嫌いな人の割合は、ルーツによって<b>3%〜21%</b>とちがいました（Mauer・El-Sohemy 2012）。いちばん多かったのは、日本や中国などの<b>東アジアにルーツを持つ人たち（21%）</b>、少なかったのは中東（3%）や中南米（4%）にルーツを持つ人たちでした。研究者は、料理でよく使う地域の人ほど嫌いな人が少ないのではないか、と考えています。</p>

    <h2>苦みをとても強く感じる「スーパーテイスター」</h2>
    <p>アメリカの研究室では、PROPという苦い物質をとかした液をなめてもらい、どのくらい苦く感じるかで人を分けました。とても強く苦く感じる人は<b>「スーパーテイスター」</b>と呼ばれ、舌の表面にある、味を感じる小さなつぶつぶが多い傾向がありました（Bartoshuk ほか 1994）。また、女性のほうがスーパーテイスターになりやすいと報告されています。</p>
    <p>このページの質問は、身近な食べ物の苦みで、その傾向をおおまかに試すものです。研究のように、専用の液で調べたものではありません。</p>

    <h2>結果の3つのタイプ</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>苦み・刺激の感じやすさ（25〜100）</th></tr>
    <tr><td>👑 苦みに敏感なタイプ（スーパーテイスター寄り）</td><td>75以上</td></tr>
    <tr><td>🙂 ふつうに感じるタイプ</td><td>50〜74</td></tr>
    <tr><td>🛡️ 苦みに強いタイプ</td><td>50未満</td></tr>
    </table>
    </div>
    <p>区切りは、このページで決めた目安です。「分からない」と答えた問題は、計算に入れていません。</p>
""",
    "faq": [
        ("このテストでスーパーテイスターか分かりますか？", "いいえ。遊びのためのセルフテストで、検査や診断ではありません。研究では、専用の苦い液や、舌の表面の観察で調べています。"),
        ("パクチー嫌いは直りますか？", "研究では、パクチーの好き嫌いに遺伝子が関係する部分は小さいとされています。食べ慣れることで、平気になる人もいます。"),
        ("急に味が分からなくなりました。", "味やにおいが急に分からなくなったときは、病気がかくれていることもあるので、医療機関に相談してください。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Eriksson N, Wu S, Do CB, ほか (2012). A genetic variant near olfactory receptor genes influences cilantro preference. <i>Flavour</i>, 1, 22.",
        "Mauer L, El-Sohemy A (2012). Prevalence of cilantro (Coriandrum sativum) disliking among different ethnocultural groups. <i>Flavour</i>, 1, 8.",
        "Bartoshuk LM, Duffy VB, Miller IJ (1994). PTC/PROP tasting: anatomy, psychophysics, and sex effects. <i>Physiology &amp; Behavior</i>, 56(6), 1165–1171.",
    ],
    "related": [("mimi-nenrei", "👂", "耳年齢テスト（聞こえる高い音は？）"), ("hsp-shindan", "🌿", "HSP診断（繊細さん）"), ("shikikaku-test", "🎨", "色覚テスト（あなたの目は何色型？）"), ("mcgurk-test", "👄", "マガーク効果テスト（目で聞く音）")],
}
