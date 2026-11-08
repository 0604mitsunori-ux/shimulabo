# -*- coding: utf-8 -*-
# 十人十脳 第20話「図形の法則（IQテストはなぜ図形なのか）」と連動（2026-11-08 新規）
PAGE = {
    "slug": "zukei-housoku",
    "title": "図形の法則テスト｜？に入る図形はどれ？IQテストによく出る行列の問題8問｜シミュラボ",
    "desc": "3×3に並んだ図形の「？」に入るものを選ぶ、行列の図形テスト8問。正解数と、解き方のタイプ（組み立て型・見比べ型・まざり型）が分かります。IQテストに図形が多い理由、14か国でIQが上がった研究、点の高い人の目の動きの研究も解説。問題はこのページで作ったもので、本物のIQテストではありません。診断ではありません。",
    "og_title": "？に入る図形はどれ？｜図形の法則テスト",
    "og_desc": "IQテストによく出る「図形の法則」を8問で。あなたは答えを組み立てる派？見比べる派？",
    "ld_name": "図形の法則テスト（行列の図形）",
    "h1": "図形の法則テスト（？に入る図形はどれ？）",
    "lead": "9つのマスに並んだ図形の、右下の<b>「？」に入るもの</b>をA〜Dから選んでください。横の並び・たての並びに、決まりがあります。全8問・約3分です。",
    "start_h2": "🔷 ？に入る図形を、8問",
    "start_text": "後半ほど、決まりが2つ重なって難しくなります。選択肢を見る前に、まず「？」の答えを想像してみるのがコツです。",
    "tag": "図形の法則テスト",
    "card_label": "図形の法則テストの結果",
    "card_footer": "？に入る図形はどれ？ → shimulabo.com",
    "stage_html": """
      <div class="syn-top"><span id="part">図形の法則</span><span id="count"></span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div id="mat" style="display:grid;grid-template-columns:repeat(3,76px);gap:6px;justify-content:center;margin:10px 0;"></div>
      <div class="syn-ask" id="q">？に入るのは？</div>
      <div class="syn-btns" id="opts" style="grid-template-columns:repeat(4,1fr);"></div>
    """,
    "js": r"""
  const $ = NOU.$;
  const T = '#4FC6B4', W = '#EEEAE3', G = '#F5BB5C', P = '#FF7AC6';
  function shp(k, cx = 50, cy = 50, r = 26, fill = T, stroke = '', sw = 5) {
    const s = `fill="${fill}"` + (stroke ? ` stroke="${stroke}" stroke-width="${sw}"` : '');
    if (k === 'c') return `<circle cx="${cx}" cy="${cy}" r="${r}" ${s}/>`;
    if (k === 's') return `<rect x="${cx - r * .9}" y="${cy - r * .9}" width="${r * 1.8}" height="${r * 1.8}" rx="2" ${s}/>`;
    if (k === 't') return `<polygon points="${cx},${cy - r * 1.05} ${cx + r * 1.05},${cy + r * .8} ${cx - r * 1.05},${cy + r * .8}" ${s}/>`;
    return `<polygon points="${cx},${cy - r * 1.15} ${cx + r},${cy} ${cx},${cy + r * 1.15} ${cx - r},${cy}" ${s}/>`;
  }
  const cnt = (k, n) => ({ 1: [50], 2: [32, 68], 3: [22, 50, 78], 4: [16, 39, 61, 84] })[n].map(x => shp(k, x, 50, n >= 3 ? 11 : 13)).join('');
  const arrow = d => `<g transform="rotate(${d} 50 50)"><line x1="50" y1="80" x2="50" y2="26" stroke="${T}" stroke-width="8" stroke-linecap="round"/><polyline points="32,42 50,22 68,42" fill="none" stroke="${T}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></g>`;
  const LN = { v: [50, 16, 50, 84], h: [16, 50, 84, 50], d1: [22, 22, 78, 78], d2: [78, 22, 22, 78] };
  const lines = ks => ks.map(k => `<line x1="${LN[k][0]}" y1="${LN[k][1]}" x2="${LN[k][2]}" y2="${LN[k][3]}" stroke="${T}" stroke-width="8" stroke-linecap="round"/>`).join('');
  const SD = { top: [22, 22, 78, 22], bottom: [22, 78, 78, 78], left: [22, 22, 22, 78], right: [78, 22, 78, 78] };
  const sides = ks => [[22, 22], [78, 22], [22, 78], [78, 78]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="3" fill="#3a3f44"/>`).join('') + ks.map(k => `<line x1="${SD[k][0]}" y1="${SD[k][1]}" x2="${SD[k][2]}" y2="${SD[k][3]}" stroke="${T}" stroke-width="8" stroke-linecap="round"/>`).join('');
  const nest = (o, i, f) => shp(o, 50, 52, 38, 'none', T, 5) + (f ? shp(i, 50, o === 't' ? 60 : 50, 11, T) : shp(i, 50, o === 't' ? 60 : 50, 11, 'none', T, 4));
  const ngon = n => `<polygon points="${Array.from({ length: n }, (_, k) => `${(50 + 36 * Math.sin(2 * Math.PI * k / n)).toFixed(1)},${(50 - 36 * Math.cos(2 * Math.PI * k / n)).toFixed(1)}`).join(' ')}" fill="none" stroke="${T}" stroke-width="6" stroke-linejoin="round"/>`;
  const Q = [
    [['c', 's', 't'].flatMap(k => [1, 2, 3].map(n => cnt(k, n))), [cnt('t', 2), cnt('t', 3), cnt('c', 3), cnt('t', 4)], 1],
    [[0, 90, 180].flatMap(r => [0, 1, 2].map(c => arrow(r + 90 * c))), [arrow(0), arrow(90), arrow(180), arrow(270)], 0],
    [['c', 's', 't', 's', 't', 'c', 't', 'c', 's'].map(k => shp(k)), [shp('c'), shp('s'), shp('t'), shp('d')], 1],
    [[['v'], ['h'], ['v', 'h'], ['d1'], ['d2'], ['d1', 'd2'], ['v'], ['d1'], ['v', 'd1']].map(lines), [lines(['v', 'd1']), lines(['v', 'h']), lines(['d1', 'd2']), lines(['v', 'd2'])], 0],
    [[['top', 'left'], ['top', 'right'], ['left', 'right'], ['bottom', 'left'], ['left', 'right'], ['bottom', 'right'], ['top', 'bottom'], ['bottom', 'right'], ['top', 'right']].map(sides),
     [sides(['top']), sides(['right']), sides(['top', 'bottom', 'right']), sides(['top', 'right'])], 3],
    [[['c', W], ['s', G], ['t', P], ['s', P], ['t', W], ['c', G], ['t', G], ['c', P], ['s', W]].map(([k, c]) => shp(k, 50, 50, 26, c)), [shp('s', 50, 50, 26, G), shp('s', 50, 50, 26, W), shp('t', 50, 50, 26, W), shp('c', 50, 50, 26, W)], 1],
    [['c', 's', 't'].flatMap(o => ['t', 's', 'c'].map(i => nest(o, i, i === 'c'))), [nest('t', 't'), nest('c', 'c', true), nest('t', 'c', true), nest('s', 'c', true)], 2],
    [[0, 1, 2].flatMap(r => [0, 1, 2].map(c => ngon(3 + r + c))), [ngon(6), ngon(8), ngon(7), ngon(5)], 2],
  ];
  const cell = (inner, sz, bd = '#2A3C43') => `<svg width="${sz}" height="${sz}" viewBox="0 0 100 100"><rect x="1.5" y="1.5" width="97" height="97" rx="10" fill="#111c20" stroke="${bd}" stroke-width="3"/>${inner}</svg>`;
  let k = 0, ok = [], t0 = 0, times = [];
  function show() {
    const [cells, opts] = Q[k]; $('count').textContent = (k + 1) + ' / 8'; $('bar').style.width = (k / 8 * 100) + '%';
    $('part').textContent = k < 3 ? 'やさしめ' : k < 5 ? 'ふつう' : '決まりが2つ';
    $('mat').innerHTML = cells.slice(0, 8).map(c => cell(c, 76)).join('') + cell(`<text x="50" y="70" text-anchor="middle" font-size="58" font-weight="900" fill="${G}">？</text>`, 76, G);
    $('q').textContent = '？に入るのは？';
    $('opts').innerHTML = opts.map((o, i) => `<button type="button" data-v="${i}" style="padding:6px 2px">${'ABCD'[i]}<br>${cell(o, 64)}</button>`).join('');
    t0 = performance.now();
  }
  function stepStyle() {
    $('mat').innerHTML = ''; $('part').textContent = 'さいごに'; $('count').textContent = ''; $('bar').style.width = '100%';
    $('q').textContent = 'どうやって選びましたか？（いちばん近いもの）'; $('opts').style.gridTemplateColumns = '1fr';
    $('opts').innerHTML = [['🧩 先に「？」の答えを頭の中で作ってから、選択肢を見た', 0], ['🔍 選択肢を1つずつ当てはめて、合わないものを消した', 1], ['🔀 問題によって、やり方が変わった', 2]].map(([t, v]) => `<button type="button" data-s="${v}">${t}</button>`).join('');
  }
  $('opts').addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    if (b.dataset.s !== undefined) return done(+b.dataset.s);
    times.push(performance.now() - t0); ok.push(+b.dataset.v === Q[k][2]); k++; if (k < 8) show(); else stepStyle();
  });
  function done(st) {
    const n = ok.filter(Boolean).length, sec = times.reduce((a, b) => a + b, 0) / 1000;
    const TY = [['🧩', '組み立て型', '先に答えを組み立ててから選ぶタイプ。研究で、点の高い人に多かった目の動きに近い解き方です（Laurence ほか 2018）。'],
                ['🔍', '見比べ型', '選択肢を当てはめて消していくタイプ。決まりが見えないときの、たよりになる方法です。次は、選択肢を見る前に「？」の答えを想像してみてください。'],
                ['🔀', 'まざり型', 'やさしい問題は組み立てて、難しい問題は見比べるタイプ。自然なやり方です。']][st];
    NOU.finish({
      label: '正解数（8問中）', big: n, unit: ' 問', emoji: TY[0], typeName: TY[1], advice: TY[2],
      extraHTML: `<div class="syn-rows"><div><span class="k">正解</span><span class="v">${n} / 8 問</span></div><div><span class="k">かかった時間</span><span class="v">${sec.toFixed(0)} 秒</span></div><div><span class="k">答え</span><span class="v">B・A・B・A・D・B・C・C</span></div></div>`,
      share: `図形の法則テストやってみた🔷 8問中${n}問正解で「${TY[1]}」でした。？に入る図形、分かる？`,
      cardTitle: 'わたしの図形の法則', cardLine: `8問中 ${n}問正解`,
      draw: (x, R) => {
        for (let i = 0; i < 8; i++) { const col = i % 4, row = Math.floor(i / 4), xx = R.x + 90 + col * 200, yy = R.y + 70 + row * 230;
          x.fillStyle = ok[i] ? '#4FC6B4' : '#2A3C43'; x.beginPath(); x.roundRect(xx, yy, 160, 170, 24); x.fill();
          x.fillStyle = ok[i] ? '#0D1417' : '#8D9BA1'; x.font = '900 64px ' + R.F; x.textAlign = 'center'; x.fillText(ok[i] ? '○' : '×', xx + 80, yy + 108); }
      },
    });
  }
  function start() { k = 0; ok = []; times = []; $('opts').style.gridTemplateColumns = 'repeat(4,1fr)'; NOU.startPanels(); show(); }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "3×3に並んだ図形の「？」に入るものを選ぶ、行列の図形テスト形式のセルフテストです。問題はこのページ（と十人十脳の動画）のために作ったもので、本物のIQテストの問題の写しではありません。",
    "article": """
    <h2>なぜIQテストに図形が多いのか</h2>
    <p>図形が並んだ「行列」のテストは、言葉を使わずに考える力を見るテストとして、広く使われてきました。国や文化、家の豊かさがちがう人たちや、時代による変化を比べるのにも使われています（Raven 2000）。</p>
    <p>1990年の分析では、点の高い人と低い人を分けていたのは、<b>目に見えない関係（決まり）を見つける力</b>と、<b>考えることをたくさん同時に頭の中で並べて管理する力</b>でした。どの人も、決まりを1つずつ見つけて、くり返し確かめていました（Carpenter ほか 1990）。</p>

    <h2>図形のテストの点は、時代で上がった</h2>
    <p>14か国のデータでは、ひと世代のあいだにIQが5〜25点上がり、いちばん大きく上がったのは、図形のような文化の影響を減らしたテストでした。オランダでは20点上がり、そのうち15点は、まだ分からない環境の力によるものでした（Flynn 1987）。</p>

    <h2>点の高い人の目の動き</h2>
    <p>34人の目の動きを測った研究では、図と選択肢のあいだを何度も行ったり来たりする人ほど点が低く、最初に選択肢を見るまでの時間が長い人ほど点が高い傾向がありました（Laurence ほか 2018）。先に答えを組み立ててから選ぶ「組み立て」と、選択肢を当てはめて消していく「見比べ（消去）」の2つの解き方があると考えられています。</p>

    <h2>練習で点は上がる？</h2>
    <p>同じ種類のテストを2回解くと点は上がりますが、その約3分の1は、目の動きに表れる「解き方のコツ」で説明できました（Hayes ほか 2015）。図形の点は、慣れやコツでも変わります。</p>

    <h2>解き方の3つのタイプ</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>解き方</th></tr>
    <tr><td>🧩 組み立て型</td><td>先に「？」の答えを頭の中で作ってから選ぶ</td></tr>
    <tr><td>🔍 見比べ型</td><td>選択肢を当てはめて、合わないものを消す</td></tr>
    <tr><td>🔀 まざり型</td><td>問題によって、やり方が変わる</td></tr>
    </table>
    </div>
    <p>タイプは、このページだけの遊びの区切りで、研究の基準ではありません。</p>
""",
    "faq": [
        ("これでIQが分かりますか？", "いいえ。8問だけの遊びのセルフテストで、IQの検査や診断ではありません。問題も本物のIQテストのものではありません。"),
        ("練習すると点は上がりますか？", "上がりますが、上がった分の一部は解き方のコツによるものと考えられています（Hayes ほか 2015）。点が上がること＝頭がよくなること、とは限りません。"),
        ("答えを教えてください", "結果の画面に、全問の答え（B・A・B・A・D・B・C・C）が出ます。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Carpenter PA, Just MA, Shell P (1990). What one intelligence test measures. <i>Psychological Review</i>, 97(3), 404–431.",
        "Raven J (2000). The Raven's Progressive Matrices: Change and stability over culture and time. <i>Cognitive Psychology</i>, 41(1), 1–48.",
        "Flynn JR (1987). Massive IQ gains in 14 nations: What IQ tests really measure. <i>Psychological Bulletin</i>, 101(2), 171–191.",
        "Laurence PG, et al. (2018). Eye movements and cognitive strategy in a fluid intelligence test: Item type analysis. <i>Frontiers in Psychology</i>, 9, 380.",
        "Hayes TR, Petrov AA, Sederberg PB (2015). Do we really become smarter when our fluid-intelligence test scores improve? <i>Intelligence</i>, 48, 1–14.",
    ],
    "related": [("mental-rotation", "🔄", "図形回転テスト"), ("iq-test", "🧩", "IQテスト（しま模様）"), ("matomekata-test", "🧠", "まとめ方テスト"), ("iq-yottsu-chikara", "💡", "IQ 4つの力テスト")],
}
