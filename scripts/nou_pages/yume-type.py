# -*- coding: utf-8 -*-
# 十人十脳 第26話「夢を見る人・見ない人」と連動（2026-11-05 新規）
PAGE = {
    "slug": "yume-type",
    "title": "夢タイプ診断｜毎晩夢を覚えている人と、まったく覚えていない人のちがい｜シミュラボ",
    "desc": "夢をよく覚えている人と、ほとんど覚えていない人。8つの質問で、あなたの「夢の覚え方」のタイプを試すセルフテスト。夢をよく覚える人は、眠っている間の脳の働き方や、夜中に目がさめる時間がちがっていたという研究も解説。診断ではありません。",
    "og_title": "夢をよく覚える人・覚えない人のちがい｜夢タイプ診断",
    "og_desc": "8つの質問で、あなたの夢の覚え方のタイプを。",
    "ld_name": "夢タイプ診断（夢をよく覚える人・覚えない人）",
    "h1": "夢タイプ診断（毎晩夢を覚えている人と、まったく覚えていない人）",
    "lead": "毎朝のように夢の話をする人もいれば、「夢なんてほとんど見ない」と言う人もいます。そのちがいは、夢を見るかどうかではなく、覚えているかどうかにあるのかもしれません。8つの質問に答えてください。約1分です。",
    "start_h2": "💭 8つの質問に答えてね",
    "start_text": "ここ1か月くらいの、ふだんの自分を思い浮かべて答えてください。",
    "tag": "夢",
    "card_label": "夢タイプ診断の結果",
    "card_footer": "夢をよく覚える人・覚えない人 → shimulabo.com",
    "stage_html": """
      <div class="syn-top"><span>ここ1か月の自分は？</span><span id="count">1 / 8</span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div class="syn-big" id="em" style="font-size:56px;"></div>
      <div class="syn-ask" id="q" style="font-size:18px;font-weight:700;color:#EEEAE3;min-height:3em;line-height:1.7;"></div>
      <div class="syn-btns c1" id="opts"></div>
    """,
    "js": r"""
  const $ = NOU.$;
  // r＝夢を覚えている回数、w＝夜中に目がさめる、h＝夢を覚えるくせ、e＝夢の中身。問題はこのページで作ったもの
  const Q = [
    ['r', '📅', '朝起きたとき、夢を覚えているのは1週間に何回くらい？', [['ほぼ毎日', 4], ['3〜5回', 3], ['1〜2回', 2], ['ほとんどない', 1]]],
    ['w', '🌙', '夜中に目がさめることは？', [['ほぼ毎晩', 4], ['週に何回か', 3], ['たまに', 2], ['ほとんどない', 1]]],
    ['h', '🧠', '起きてすぐ、どんな夢だったか思い出そうとする？', [['いつもする', 4], ['ときどきする', 3], ['あまりしない', 2], ['まったくしない', 1]]],
    ['h', '📝', '夢の内容を、人に話したりメモしたりする？', [['よくする', 4], ['ときどき', 3], ['あまりしない', 2], ['しない', 1]]],
    ['w', '⏰', '目ざましで、とつぜん起こされることが多い？', [['ほぼ毎日', 4], ['週に何回か', 3], ['たまに', 2], ['ほとんどない', 1]]],
    ['e', '🎨', '覚えている夢は、色や音までくわしい？', [['とてもくわしい', 4], ['わりとくわしい', 3], ['ぼんやり', 2], ['ほとんど覚えていない', 1]]],
    ['e', '😮', '夢の中で「これは夢だ」と気づいたことは？', [['よくある', 4], ['何回かある', 3], ['一度だけある', 2], ['ない', 1]]],
    ['h', '🎬', '起きたあとも、夢の気分が残ることがある？', [['よくある', 4], ['ときどき', 3], ['あまりない', 2], ['ない', 1]]],
  ];
  let k = 0, ans = [];
  function show() { const [, e, q, o] = Q[k]; $('em').textContent = e; $('q').textContent = q; $('count').textContent = (k + 1) + ' / 8'; $('bar').style.width = (k / 8 * 100) + '%';
    $('opts').innerHTML = o.map(([t, v]) => `<button type="button" data-v="${v}">${t}</button>`).join(''); }
  $('opts').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; ans.push(+b.dataset.v); k++; if (k < 8) show(); else done(); });
  function done() {
    const sum = t => Q.reduce((s, q, i) => s + (q[0] === t ? ans[i] : 0), 0), cnt = t => Q.filter(q => q[0] === t).length;
    const rec = ans[0], wk = sum('w') / cnt('w'), hb = sum('h') / cnt('h'), total = ans.reduce((a, b) => a + b, 0);   // 8〜32
    const T = rec >= 4 ? ['🌈', '夢をよく覚えるタイプ', 'ほぼ毎朝、夢を覚えているタイプです。']
            : rec >= 3 ? ['💭', 'わりと夢を覚えるタイプ', '週に何回か、夢を覚えているタイプです。']
            : rec >= 2 ? ['🌤️', 'ときどき夢を覚えるタイプ', 'たまに夢を覚えているタイプです。']
            : ['🌑', '夢をほとんど覚えないタイプ', '夢をほとんど覚えていないタイプです。夢を見ていないのではなく、覚えていないだけかもしれません。'];
    const hint = wk >= 3 ? '夜中に目がさめることが多いようです。研究では、夢をよく覚える人は、眠っている間に目がさめている時間が長かったと報告されています。' : hb <= 2 ? '起きてすぐに夢を思い出そうとすると、夢を覚えやすくなることがあります。まくらもとにメモを置いてみるのもおすすめです。' : '';
    const AX = [['📅 覚えている回数', rec], ['🌙 夜中・朝の目ざめ', wk], ['🧠 思い出すくせ', hb], ['🎨 夢のくわしさ', sum('e') / cnt('e')]];
    NOU.finish({
      label: '夢の覚えやすさ（8〜32点）', big: total, unit: ' / 32 点', emoji: T[0], typeName: T[1], advice: T[2],
      extraHTML: (hint ? `<p style="font-size:14px;margin:6px 0;">${hint}</p>` : '') + `<div class="syn-rows">${AX.map(([n, v]) => `<div><span class="k">${n}</span><span class="v">${'●'.repeat(Math.round(v))}${'○'.repeat(4 - Math.round(v))}</span></div>`).join('')}</div>`,
      share: `夢タイプ診断やってみた💭 「${T[1]}」でした（${total}/32点）。あなたは毎晩夢を覚えてる？`,
      cardTitle: 'わたしの夢の覚え方', cardLine: `夢の覚えやすさ ${total} / 32 点`,
      draw: (x, R) => {
        AX.forEach(([n, v], i) => { const y = R.y + 60 + i * 120;
          x.fillStyle = '#EEEAE3'; x.textAlign = 'left'; x.font = '800 40px ' + R.F; x.fillText(n, R.x, y);
          for (let d = 0; d < 4; d++) { x.fillStyle = d < Math.round(v) ? '#4FC6B4' : '#2A3C43'; x.beginPath(); x.arc(R.x + R.w - 270 + d * 80, y - 14, 28, 0, Math.PI * 2); x.fill(); } });
      },
    });
  }
  function start() { k = 0; ans = []; NOU.startPanels(); show(); }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "夢を覚えている回数・夜中や朝の目ざめ・夢を思い出すくせ・夢のくわしさについての8つの質問に答えるセルフテストです。問題はこのページで作っています。",
    "article": """
    <h2>夢を「よく覚える人」と「覚えない人」</h2>
    <p>夢を覚えている回数は、人によって大きくちがいます。フランスの研究チームは、夢を<b>1週間に平均5回ほど覚えている人</b>と、<b>平均0.5回ほどしか覚えていない人</b>をくらべました（Eichenlaub ほか 2014）。</p>
    <p>脳の働きを調べると、夢をよく覚える人は、眠っているときも起きているときも、<b>脳の「側頭頭頂接合部」や「内側前頭前野」と呼ばれる場所の働きが高い</b>という結果でした。研究チームは、これらの場所が、夢を見ることや、夢を記憶に残すことに関わっているのではないかと考えています。</p>

    <h2>夜中に目がさめる人ほど、夢を覚えている？</h2>
    <p>別の研究チームが眠っている人の脳波を調べた研究では、夢をよく覚える人は、<b>眠りの途中で目がさめる回数が多く、目がさめている時間も長い</b>ことが分かりました（van Wyk ほか 2019）。夢を見ている途中や直後に少し目がさめると、そのあいだに夢が記憶に残りやすいのかもしれません。</p>
    <p>つまり「夢を見ない」と思っている人も、夢を見ていないのではなく、<b>夢を記憶に残す前に、ぐっすり眠り続けている</b>だけなのかもしれません。</p>

    <h2>夢を覚えやすくするには</h2>
    <ul>
      <li>起きてすぐ、目を閉じたまま「どんな夢だったか」を思い出してみる</li>
      <li>まくらもとにメモを置いて、思い出したことをすぐ書く</li>
      <li>夢の話を人にしてみる</li>
    </ul>
    <p>夢を覚えていないことは、悪いことではありません。ぐっすり眠れているしるしかもしれません。</p>

    <h2>結果の4つのタイプ</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>夢を覚えている回数（1週間）</th></tr>
    <tr><td>🌈 夢をよく覚えるタイプ</td><td>ほぼ毎日</td></tr>
    <tr><td>💭 わりと夢を覚えるタイプ</td><td>3〜5回</td></tr>
    <tr><td>🌤️ ときどき夢を覚えるタイプ</td><td>1〜2回</td></tr>
    <tr><td>🌑 夢をほとんど覚えないタイプ</td><td>ほとんどない</td></tr>
    </table>
    </div>
""",
    "faq": [
        ("夢を覚えていないのは、眠りが浅くないからですか？", "そうとは限りませんが、研究では、夢をよく覚える人は眠っている間に目がさめている時間が長かったと報告されています。"),
        ("こわい夢ばかり見て、よく眠れません。", "悪い夢が続いて眠れない・昼間につらいときは、医療機関に相談してください。"),
        ("このテストで睡眠の病気が分かりますか？", "いいえ。遊びのためのセルフテストで、検査や診断ではありません。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Eichenlaub JB, Nicolas A, Daltrozzo J, Redouté J, Costes N, Ruby P (2014). Resting brain activity varies with dream recall frequency between subjects. <i>Neuropsychopharmacology</i>, 39(7), 1594–1602.",
        "van Wyk M, Solms M, Lipinska G (2019). Increased awakenings from non-rapid eye movement sleep explain differences in dream recall frequency in healthy individuals. <i>Frontiers in Human Neuroscience</i>, 13, 370.",
    ],
    "related": [("chrono", "⏰", "朝型・夜型診断"), ("aphantasia-test", "🌫️", "アファンタジア診断テスト"), ("jikan-kankaku", "⏱️", "時間感覚テスト（目を閉じて30秒）"), ("hsp-shindan", "🌿", "HSP診断（繊細さん）")],
}
