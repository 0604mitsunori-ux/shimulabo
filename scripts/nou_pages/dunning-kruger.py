# -*- coding: utf-8 -*-
# 十人十脳 第12話「自信過剰（ダニング＝クルーガー効果）」と連動（2026-11-05 新規）
PAGE = {
    "slug": "dunning-kruger",
    "title": "ダニング＝クルーガー効果テスト｜自分の実力、正しく見積もれる？予想と結果のズレを試す｜シミュラボ",
    "desc": "解く前に「何問できそうか」を予想してから、10問のクイズに挑戦。予想と結果のズレで、あなたが自分を高く見積もるタイプか、低く見積もるタイプかが分かります。「できない人ほど自分はできると思う」ダニング＝クルーガー効果の研究と、その反論も解説。診断ではありません。",
    "og_title": "自分の実力、正しく見積もれる？｜ダニング＝クルーガー効果テスト",
    "og_desc": "解く前の予想と、実際の点数。そのズレが、あなたの見積もりぐせ。",
    "ld_name": "ダニング＝クルーガー効果テスト（予想と結果のズレ）",
    "h1": "ダニング＝クルーガー効果テスト（自分の実力、正しく見積もれる？）",
    "lead": "「わたしはできるほうだ」と思っている人ほど、実はできていない——そんな研究があります。でも、自分のことは分かりにくいもの。まず<b>10問中、何問できそうか</b>を予想してから、クイズに挑戦してください。約3分です。",
    "start_h2": "🤔 まず予想してから、10問に挑戦",
    "start_text": "最初に「10問中何問正解できそうか」と「同じテストを受けた人の中で、自分は上から何%くらいか」を答えます。そのあと、論理や数のクイズが10問出ます。",
    "tag": "ダニングクルーガー効果",
    "card_label": "ダニング＝クルーガー効果テストの結果",
    "card_footer": "自分の実力、正しく見積もれる？ → shimulabo.com",
    "stage_html": """
      <div class="syn-top"><span id="part">予想する</span><span id="count"></span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div class="syn-ask" id="q" style="font-size:18px;font-weight:700;color:#EEEAE3;min-height:3.4em;line-height:1.7;"></div>
      <div class="syn-btns" id="opts"></div>
    """,
    "js": r"""
  const $ = NOU.$;
  const QZ = [
    ['すべての犬は動物です。ポチは犬です。ポチは動物？', ['はい', 'いいえ', '分からない'], 0],
    ['2, 4, 8, 16, ? の「？」に入る数は？', ['24', '30', '32', '36'], 2],
    ['AはBより背が高く、CはAより背が高い。いちばん背が低いのは？', ['A', 'B', 'C', '分からない'], 1],
    ['バットとボールで合わせて1,100円。バットはボールより1,000円高い。ボールはいくら？', ['50円', '100円', '110円', '150円'], 0],
    ['1, 1, 2, 3, 5, 8, ? の「？」に入る数は？', ['11', '12', '13', '15'], 2],
    ['5台の機械で、5個作るのに5分かかる。100台で100個作るのは何分？', ['5分', '20分', '100分', '500分'], 0],
    ['池の水草が毎日2倍に増え、48日で池全体をおおった。池の半分をおおったのは何日目？', ['24日目', '36日目', '46日目', '47日目'], 3],
    ['ある月の1日が月曜日。その月の15日は何曜日？', ['日曜日', '月曜日', '火曜日', '水曜日'], 1],
    ['「雨が降ると道がぬれる」。道がぬれている。必ず雨が降った？', ['必ず降った', '必ずとは言えない', '降っていない'], 1],
    ['3人で3日に3個のパンを食べる。6人で6日に何個？', ['6個', '9個', '12個', '18個'], 2],
  ];
  let k = 0, predN = 0, predP = 0, right = [];
  function stepPred() {
    $('part').textContent = '予想する'; $('count').textContent = '';
    if (k === 0) { $('q').textContent = '10問中、何問正解できそう？'; $('opts').style.gridTemplateColumns = 'repeat(4,1fr)'; $('opts').innerHTML = Array.from({ length: 11 }, (_, i) => `<button type="button" data-v="${i}">${i}問</button>`).join(''); }
    else { $('q').textContent = '同じテストを受けた人の中で、自分は上から何%くらいだと思う？'; $('opts').style.gridTemplateColumns = '1fr'; $('opts').innerHTML = [['上位10%に入る', 90], ['上位30%くらい', 70], ['まん中くらい', 50], ['下から30%くらい', 30], ['下から10%くらい', 10]].map(([t, v]) => `<button type="button" data-v="${v}">${t}</button>`).join(''); }
  }
  function stepQ() {
    const j = k - 2, [q, o] = QZ[j]; $('part').textContent = 'クイズ'; $('count').textContent = (j + 1) + ' / 10'; $('bar').style.width = (j / 10 * 100) + '%';
    $('q').textContent = q; $('opts').style.gridTemplateColumns = o.length === 3 ? '1fr' : 'repeat(2,1fr)'; $('opts').innerHTML = o.map((t, i) => `<button type="button" data-v="${i}">${t}</button>`).join('');
  }
  $('opts').addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return; const v = +b.dataset.v;
    if (k === 0) predN = v; else if (k === 1) predP = v; else right.push(v === QZ[k - 2][2]);
    k++; if (k < 2) stepPred(); else if (k < 12) stepQ(); else done();
  });
  function done() {
    const n = right.filter(Boolean).length, d = predN - n;
    const T = d >= 3 ? ['🎈', '自分を高く見積もるタイプ', `予想（${predN}問）より、実際は${d}問少ない結果でした。研究でも、自分の点数を高めに見積もる人は多いことが分かっています。`]
            : d <= -3 ? ['🐢', '自分を低く見積もるタイプ', `予想（${predN}問）より、実際は${-d}問多い結果でした。自分の力を、ひかえめに見積もるくせがあるのかもしれません。`]
            : Math.abs(d) <= 1 ? ['🎯', 'ぴったり見積もるタイプ', `予想（${predN}問）と実際の点数が、ほとんど同じでした。自分の力を正確につかめています。`]
            : d > 0 ? ['🙂', '少し高めに見積もるタイプ', `予想より${d}問少ない結果でした。多くの人はこのあたりです。`]
            : ['🙂', '少し低めに見積もるタイプ', `予想より${-d}問多い結果でした。`];
    const wrongs = QZ.map((q, i) => right[i] ? '' : `<div><span class="k">${q[0]}</span><span class="v">答え：${q[1][q[2]]}</span></div>`).join('');
    NOU.finish({
      label: '予想とのズレ（予想 − 実際）', big: (d > 0 ? '+' : '') + d, unit: ' 問', emoji: T[0], typeName: T[1], advice: T[2],
      extraHTML: `<div class="syn-rows"><div><span class="k">予想</span><span class="v">${predN} / 10 問</span></div><div><span class="k">実際</span><span class="v">${n} / 10 問</span></div><div><span class="k">自分の位置の予想</span><span class="v">上から${100 - predP}%くらい</span></div></div>`
        + (wrongs ? `<details style="margin-top:8px;"><summary style="cursor:pointer;font-size:13px;">まちがえた問題の答え</summary><div class="syn-rows">${wrongs}</div></details>` : ''),
      share: `ダニング＝クルーガー効果テストやってみた🤔 予想${predN}問→実際${n}問で「${T[1]}」でした。あなたは自分の実力、正しく見積もれる？`,
      cardTitle: 'わたしの見積もりぐせ', cardLine: `予想 ${predN}問 → 実際 ${n}問`,
      draw: (x, R) => {
        [['予想', predN, '#F5BB5C'], ['実際', n, '#4FC6B4']].forEach(([lab, v, c], i) => {
          const bw = 260, xx = R.x + R.w / 2 - 300 + i * 340, h = 40 + v * 46;
          x.fillStyle = '#2A3C43'; x.beginPath(); x.roundRect(xx, R.y + 50, bw, 500, 24); x.fill();
          x.fillStyle = c; x.beginPath(); x.roundRect(xx, R.y + 550 - h, bw, h, 24); x.fill();
          x.fillStyle = '#EEEAE3'; x.textAlign = 'center'; x.font = '800 40px ' + R.F; x.fillText(lab, xx + bw / 2, R.y + 30);
          x.fillStyle = '#0D1417'; x.font = '900 60px ' + R.F; x.fillText(v + '問', xx + bw / 2, R.y + 525);
        });
      },
    });
  }
  function start() { k = 0; right = []; NOU.startPanels(); $('bar').style.width = '0%'; stepPred(); }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "解く前に自分の点数と順位を予想し、そのあと論理と数のクイズ10問を解いて、予想と結果のズレを見るセルフテストです。問題はこのページで作ったものです。",
    "article": """
    <h2>ダニング＝クルーガー効果とは</h2>
    <p>1999年、アメリカの心理学者ダニングとクルーガーは、学生に「ユーモア」「文法」「論理」のテストを受けてもらい、受ける前とあとに、自分の順位を予想してもらいました（Kruger・Dunning 1999）。</p>
    <p>すると、<b>点数が下から4分の1に入った人たち</b>は、実際には下から12%くらいの位置だったのに、自分では<b>上から4割くらい（62%の位置）</b>だと見積もっていました。できない人ほど、自分ができていないことに気づきにくい——これが「ダニング＝クルーガー効果」と呼ばれるようになりました。</p>
    <p>2人は理由を、「できているかどうかを見分ける力（メタ認知）」が足りないと、自分のまちがいにも気づけないからだと考えました。</p>

    <h2>反対の意見もある</h2>
    <p>その後の研究では、誰でも自分の順位の見積もりには「ずれ（ノイズ）」と「自分を良く思うくせ」があり、それだけでも同じような結果が出ると指摘されています（Burson ほか 2006）。また、上手な人は、逆に自分を低めに見積もることも報告されています。「できない人だけが勘ちがいしている」というより、<b>多くの人が自分の位置を正しくつかめていない</b>と考えたほうがよさそうです。</p>

    <h2>このテストの問題について</h2>
    <p>10問の中には、直感で答えるとまちがえやすい問題がいくつか入っています（たとえば、バットとボールの問題）。「かんたんだ」と思ったときほど、もう一度考え直すのがコツです。</p>

    <h2>結果の5つのタイプ</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>予想 − 実際</th></tr>
    <tr><td>🎈 自分を高く見積もるタイプ</td><td>＋3問以上</td></tr>
    <tr><td>🙂 少し高めに見積もるタイプ</td><td>＋2問</td></tr>
    <tr><td>🎯 ぴったり見積もるタイプ</td><td>−1〜＋1問</td></tr>
    <tr><td>🙂 少し低めに見積もるタイプ</td><td>−2問</td></tr>
    <tr><td>🐢 自分を低く見積もるタイプ</td><td>−3問以下</td></tr>
    </table>
    </div>
    <p>このページでは、ほかの人の点数を集めていないので、実際の順位は出していません。順位の予想は、自分の見積もりぐせをふり返るための参考です。</p>
""",
    "faq": [
        ("点数が低かったら、頭が悪いということですか？", "いいえ。遊びのためのセルフテストで、頭の良さを測るものではありません。見てほしいのは、点数より「予想とのズレ」です。"),
        ("ダニング＝クルーガー効果は本当にあるのですか？", "1999年の研究で報告されてから多くの研究がありますが、誰にでもある見積もりのずれで説明できるという反論もあります（Burson ほか 2006）。"),
        ("実際の順位は分かりますか？", "このページでは、ほかの人の答えを集めていないので、順位は出していません。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Kruger J, Dunning D (1999). Unskilled and unaware of it: How difficulties in recognizing one's own incompetence lead to inflated self-assessments. <i>Journal of Personality and Social Psychology</i>, 77(6), 1121–1134.",
        "Burson KA, Larrick RP, Klayman J (2006). Skilled or unskilled, but still unaware of it: How perceptions of difficulty drive miscalibration in relative comparisons. <i>Journal of Personality and Social Psychology</i>, 90(1), 60–77.",
    ],
    "related": [("iq-test", "🧩", "IQテスト（パターンの見え方）"), ("tango-kioku", "📝", "単語記憶テスト"), ("naigen-test", "💬", "頭の中の声テスト"), ("chrono", "⏰", "朝型・夜型診断")],
}
