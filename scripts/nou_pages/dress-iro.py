# -*- coding: utf-8 -*-
# 十人十脳 第15話「同じ写真が違う色に（ドレス）」と連動（2026-11-05 新規）。元の写真は使わず、色と光の思いこみを試す絵をこのページで作った
PAGE = {
    "slug": "dress-iro",
    "title": "ドレスの色テスト｜白と金？青と黒？同じ色が人によってちがって見える理由を試す｜シミュラボ",
    "desc": "2015年に世界中で話題になった「青と黒？白と金？」のドレス。同じ写真なのに、人によって見える色が割れました。その理由は「光の思いこみ」にあると考えられています。同じ色の布を、ちがう光の中で見比べるセルフテスト。診断ではありません。",
    "og_title": "白と金？青と黒？｜ドレスの色テスト",
    "og_desc": "同じ色の布なのに、光しだいで見え方が変わる。あなたの頭の「光の思いこみ」は？",
    "ld_name": "ドレスの色テスト（白と金？青と黒？）",
    "h1": "ドレスの色テスト（白と金？青と黒？）",
    "lead": "2015年、1枚のドレスの写真が世界中で話題になりました。「青と黒」に見える人と「白と金」に見える人が、まっぷたつに割れたのです。このページでは元の写真は使わず、<b>まったく同じ色の布</b>を、ちがう光の部屋に置いて見てもらいます。5問、約1分です。",
    "start_h2": "👗 布は何色に見える？",
    "start_text": "最初に、ドレスの絵が出ます。そのあと、同じ布の切れはしが、ちがう光の部屋に置かれて4回出ます。見えたとおりに答えてください。",
    "tag": "ドレスの色",
    "card_label": "ドレスの色テストの結果",
    "card_footer": "白と金？青と黒？ → shimulabo.com ドレスの色テスト",
    "stage_html": """
      <div class="syn-top"><span id="part">ドレスは何色と何色？</span><span id="count">1 / 5</span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div id="scene" style="position:relative;height:300px;border-radius:16px;overflow:hidden;margin:8px auto 12px;max-width:360px;"></div>
      <div class="syn-btns c1" id="opts"></div>
    """,
    "js": r"""
  const $ = NOU.$;
  // 布の色はどの問題でもまったく同じ（あいまいな青むらさきと、くすんだ茶色のしま）
  const C1 = '#8f97bd', C2 = '#6e5a34';
  const stripes = `repeating-linear-gradient(180deg, ${C1} 0 34px, ${C2} 34px 50px)`;
  const dress = `<svg viewBox="0 0 200 300" style="position:absolute;left:50%;top:12px;height:276px;transform:translateX(-50%)"><defs><pattern id="dst" width="200" height="34" patternUnits="userSpaceOnUse"><rect width="200" height="24" fill="${C1}"/><rect y="24" width="200" height="10" fill="${C2}"/></pattern></defs>`
    + `<path d="M72 8 L78 8 L85 32 Q100 38 115 32 L122 8 L128 8 L136 96 Q100 104 64 96 Z" fill="url(#dst)"/>`
    + `<path d="M64 96 Q100 104 136 96 L184 292 Q100 302 16 292 Z" fill="url(#dst)"/><path d="M63 88 Q100 96 137 88 L138 100 Q100 108 62 100 Z" fill="${C2}"/></svg>`;
  const swatch = `<div style="position:absolute;left:50%;top:50%;width:150px;height:150px;transform:translate(-50%,-50%);border-radius:10px;background:${stripes};box-shadow:0 4px 20px rgba(0,0,0,.25)"></div>`;
  const SC = [
    ['ドレスは何色と何色？', `<div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 30%,#fffbe8,#f3e6b8 60%,#c9b27a)"></div>` + dress,
      [['白と金', 'wg'], ['青と黒', 'bk'], ['青と茶色', 'bb'], ['そのほか', 'x']]],
    ['電球のオレンジの光の部屋。布の明るいしまは何色？', `<div style="position:absolute;inset:0;background:radial-gradient(circle at 30% 20%,#ffcf7a,#c5762a 70%,#6b3a12)"></div>` + swatch, [['青っぽい', 'b'], ['白っぽい', 'w']]],
    ['青い日かげの部屋。布の明るいしまは何色？', `<div style="position:absolute;inset:0;background:radial-gradient(circle at 70% 20%,#a9c3ff,#5571b8 70%,#22325e)"></div>` + swatch, [['青っぽい', 'b'], ['白っぽい', 'w']]],
    ['まぶしい窓の前（逆光）。布の明るいしまは何色？', `<div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 40%,#ffffff,#fff3cf 55%,#d8c28a)"></div>` + swatch, [['青っぽい', 'b'], ['白っぽい', 'w']]],
    ['うす暗い夜の部屋。布の明るいしまは何色？', `<div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 30%,#3a3f4f,#1b1e27 70%,#0b0c10)"></div>` + swatch, [['青っぽい', 'b'], ['白っぽい', 'w']]],
  ];
  let k = 0, ans = [];
  function show() { const [q, html, o] = SC[k]; $('part').textContent = q; $('scene').innerHTML = html; $('count').textContent = (k + 1) + ' / 5'; $('bar').style.width = (k / 5 * 100) + '%';
    $('opts').className = 'syn-btns ' + (o.length > 2 ? 'c1' : ''); $('opts').innerHTML = o.map(([t, v]) => `<button type="button" data-v="${v}">${t}</button>`).join(''); }
  $('opts').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; ans.push(b.dataset.v); k++; if (k < 5) show(); else done(); });
  function done() {
    const d = ans[0], swaps = ans.slice(1), nBlue = swaps.filter(v => v === 'b').length;
    const name = { wg: '白と金', bk: '青と黒', bb: '青と茶色', x: 'そのほか' }[d];
    const T = d === 'wg' ? ['🤍', '「青い影」を差し引くタイプ', 'ドレスが白と金に見えました。研究では、ドレスが青っぽい日かげにあると頭が思いこむと、青みを差し引いて白と金に見えやすいと考えられています。']
            : d === 'bk' ? ['💙', '「黄色い光」を差し引くタイプ', 'ドレスが青と黒に見えました。研究では、黄色っぽい電球の光の中にあると頭が思いこむと、黄みを差し引いて青と黒に見えやすいと考えられています。']
            : ['🔀', 'その中間タイプ', `ドレスが「${name}」に見えました。白と金・青と黒以外に見える人も、研究では1割ほどいました。`];
    const swing = nBlue > 0 && nBlue < 4 ? `<p style="font-size:14px;margin:6px 0;">同じ布なのに、部屋の光によって「青っぽい」と「白っぽい」が入れかわりました（4問中${nBlue}問が青っぽい）。頭が光の色を差し引いて、布の色を決めているからだと考えられます。</p>` : `<p style="font-size:14px;margin:6px 0;">4つの部屋で、布はいつも「${nBlue ? '青っぽい' : '白っぽい'}」に見えました。光の影響を受けにくい見え方です。</p>`;
    const rows = SC.slice(1).map((s, i) => `<div><span class="k">${s[0].split('。')[0]}</span><span class="v">${swaps[i] === 'b' ? '青っぽい' : '白っぽい'}</span></div>`).join('');
    NOU.finish({
      label: 'ドレスの絵は何色に見えた？', big: name, unit: '', emoji: T[0], typeName: T[1], advice: T[2],
      extraHTML: swing + `<div class="syn-rows">${rows}</div><p style="font-size:12px;color:var(--ink-3);">布の色は、5問とも画面の上ではまったく同じです。</p>`,
      share: `ドレスの色テストやってみた👗 ドレスは「${name}」に見えて「${T[1]}」でした。同じ色の布なのに、光で見え方が変わった！あなたは白と金？青と黒？`,
      cardTitle: 'わたしの頭の「光の思いこみ」', cardLine: `ドレスは「${name}」に見えた`,
      draw: (x, R) => {
        const bg = [['#ffcf7a', '電球'], ['#5571b8', '日かげ'], ['#fff3cf', '逆光'], ['#1b1e27', '夜']], cw = (R.w - 3 * 24) / 4;
        bg.forEach(([c, n], i) => { const xx = R.x + i * (cw + 24), y = R.y + 120;
          x.fillStyle = c; x.beginPath(); x.roundRect(xx, y, cw, 300, 20); x.fill();
          for (let s = 0; s < 6; s++) { x.fillStyle = s % 2 ? C2 : C1; x.fillRect(xx + cw * .2, y + 70 + s * 26, cw * .6, s % 2 ? 12 : 26); }
          x.fillStyle = '#EEEAE3'; x.textAlign = 'center'; x.font = '800 32px ' + R.F; x.fillText(n, xx + cw / 2, y - 24);
          x.font = '900 36px ' + R.F; x.fillText(swaps[i] === 'b' ? '青っぽい' : '白っぽい', xx + cw / 2, y + 360); });
      },
    });
  }
  function start() { k = 0; ans = []; NOU.startPanels(); show(); }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "このページで作ったドレスの絵と、まったく同じ色の布を4つのちがう光の部屋に置いた絵を見て、何色に見えたかを答えるセルフテストです。2015年に話題になった元の写真は使っていません。",
    "article": """
    <h2>2015年の「ドレス」騒動</h2>
    <p>2015年、1枚のドレスの写真がインターネットで世界中に広まりました。同じ写真なのに、「青と黒」に見える人と「白と金」に見える人がいて、どちらも「どう見てもこっちだ」とゆずらなかったのです。</p>
    <p>アメリカの研究チームが1,400人あまりに聞いたところ、<b>青と黒が57%、白と金が30%、青と茶色が11%</b>、そのほかが2%でした（Lafer-Sousa ほか 2015）。別の研究者がインターネットで多くの人に聞いた調査では、白と金と答えた人のほうが多く（59%）、割合は調べ方によって変わります（Wallisch 2017）。どちらにしても、<b>同じ写真で答えが大きく割れた</b>ことは同じです。</p>

    <h2>見え方を分けたのは「光の思いこみ」</h2>
    <p>私たちの頭は、ものの色を見るとき、<b>そのものを照らしている光の色</b>を自動で差し引いています。白い紙が、電球の下でも日かげでも「白」に見えるのはそのためです。</p>
    <p>ところがドレスの写真は、光がどんな色なのかがはっきりしない写り方をしていました。そのため、</p>
    <ul>
      <li>「青っぽい日かげにある」と頭が思いこむと、青みを差し引いて<b>白と金</b>に見える</li>
      <li>「黄色っぽい電球の光の中にある」と思いこむと、黄みを差し引いて<b>青と黒</b>に見える</li>
    </ul>
    <p>と考えられています（Lafer-Sousa ほか 2015、Wallisch 2017）。どんな光を思いこむかは、それまでに見てきた光の経験で変わると考えられていて、朝型の人と夜型の人で見え方が分かれるという説も出されています。</p>

    <h2>このテストのしくみ</h2>
    <p>このページの絵の布は、5問とも<b>画面の上ではまったく同じ色</b>です。変えているのは、まわりの部屋の光だけです。答えが部屋によって入れかわったら、あなたの頭が光の色を差し引いて、布の色を決めているからだと考えられます。</p>
    <p>ドレスの絵は、元の写真の雰囲気をまねて作ったもので、元の写真ほど見え方は割れないかもしれません。</p>

    <h2>結果の3つのタイプ</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>ドレスの絵の見え方</th></tr>
    <tr><td>🤍 「青い影」を差し引くタイプ</td><td>白と金</td></tr>
    <tr><td>💙 「黄色い光」を差し引くタイプ</td><td>青と黒</td></tr>
    <tr><td>🔀 その中間タイプ</td><td>青と茶色・そのほか</td></tr>
    </table>
    </div>
""",
    "faq": [
        ("本当のドレスは何色ですか？", "実物は青と黒のドレスだったと報じられています。ただ、写真の見え方として白と金に見える人がいるのは、目や頭がおかしいからではありません。"),
        ("元の写真は使っていないのですか？", "使っていません。写真には撮った人の権利があるため、このページでは色と光の関係を試す絵を作って使っています。"),
        ("色覚の検査になりますか？", "いいえ。遊びのためのセルフテストで、検査や診断ではありません。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Lafer-Sousa R, Hermann KL, Conway BR (2015). Striking individual differences in color perception uncovered by 'the dress' photograph. <i>Current Biology</i>, 25(13), R545–R546.",
        "Wallisch P (2017). Illumination assumptions account for individual differences in the perceptual interpretation of a profoundly ambiguous stimulus in the color domain: \"The dress\". <i>Journal of Vision</i>, 17(4):5.",
    ],
    "related": [("ao-midori", "🟦", "青と緑の境目テスト"), ("shikikaku-test", "🎨", "色覚テスト（あなたの目は何色型？）"), ("chrono", "⏰", "朝型・夜型診断"), ("hybrid-gazou", "👓", "近くと遠くで変わる数字テスト")],
}
