# -*- coding: utf-8 -*-
# 十人十脳 第19話「頭の中で回す（メンタルローテーション）」と連動（2026-11-08 十人十脳の型で作り直し）
PAGE = {
    "slug": "mental-rotation",
    "title": "図形回転テスト（メンタルローテーション）｜この形、同じ？鏡？頭の中で回す力を12問で｜シミュラボ",
    "desc": "右の形は、左の形を回しただけ？それとも裏返した鏡？12問で頭の中で形を回す力（メンタルローテーション）を試すセルフテスト。最後に解き方から「くるっと型・目印型・からだ型」が分かります。1971年の実験、40万人を11年追った研究、練習で伸びるかの研究も解説。診断ではありません。",
    "og_title": "この形、同じ？鏡？｜図形回転テスト（メンタルローテーション）",
    "og_desc": "頭の中で形を回す力を12問で。あなたの解き方は、くるっと型？目印型？からだ型？",
    "ld_name": "図形回転テスト（メンタルローテーション）",
    "h1": "図形回転テスト（この形、同じ？鏡？）",
    "lead": "右の形は、左の形を<b>回しただけ</b>？それとも<b>裏返した鏡</b>？頭の中で形を回して、12問に答えてください。約2分です。最後に、あなたの解き方のタイプも分かります。",
    "start_h2": "🔄 同じ？鏡？ 12問に挑戦",
    "start_text": "2つの形が出ます。回しただけなら「同じ」、裏返しなら「鏡」を押してください。後半は少し難しくなります。答えるまでの時間も測ります。",
    "tag": "メンタルローテーション",
    "card_label": "図形回転テストの結果",
    "card_footer": "この形、同じ？鏡？ → shimulabo.com",
    "stage_html": """
      <div class="syn-top"><span id="part">同じ？鏡？</span><span id="count"></span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div id="shapes" style="display:flex;justify-content:space-around;align-items:center;min-height:190px;margin:10px 0;"></div>
      <div class="syn-ask" id="q">右の形は　回しただけ？　鏡？</div>
      <div class="syn-btns" id="opts"></div>
    """,
    "js": r"""
  const $ = NOU.$;
  const SH = [
    [[0,0],[0,1],[0,2],[0,3],[1,3],[2,3],[1,0]], [[1,0],[2,0],[0,1],[1,1],[1,2]], [[0,0],[1,0],[1,1],[2,1],[2,2],[3,2],[1,-1]],
    [[0,0],[1,0],[2,0],[2,1],[3,1],[1,-1]], [[0,0],[0,1],[1,1],[1,2],[2,2],[0,3]], [[0,0],[1,0],[2,0],[3,0],[3,1],[1,1],[1,2]],
  ];
  const ROT = [60, 90, 120, 150, 180, 210, 240, 270, 300];
  function svg(cells, rot, mir, col) {
    const xs = cells.map(c => c[0]), ys = cells.map(c => c[1]);
    const cx = (Math.min(...xs) + Math.max(...xs) + 1) / 2, cy = (Math.min(...ys) + Math.max(...ys) + 1) / 2;
    const r = Math.max(...cells.flatMap(([x, y]) => [[x, y], [x + 1, y], [x, y + 1], [x + 1, y + 1]].map(([a, b]) => Math.hypot(a - cx, b - cy))));
    const u = 160 * 0.46 / r;
    const body = cells.map(([x, y]) => `<rect x="${x}" y="${y}" width="1" height="1" fill="${col}" stroke="#0D1417" stroke-width="${(2 / u).toFixed(3)}"/>`).join('');
    return `<svg width="160" height="160" viewBox="0 0 160 160"><g transform="translate(80,80) rotate(${rot}) scale(${mir ? -1 : 1},1) scale(${u}) translate(${-cx},${-cy})">${body}</g></svg>`;
  }
  let Q = [], k = 0, ok = [], times = [], t0 = 0;
  function make() {
    Q = []; for (let i = 0; i < 12; i++) { const s = SH[i % SH.length]; Q.push({ s, rot: ROT[Math.floor(Math.random() * ROT.length)] * (i < 6 ? 0.5 : 1), mir: Math.random() < 0.5 }); }
  }
  function show() {
    const q = Q[k]; $('count').textContent = (k + 1) + ' / 12'; $('bar').style.width = (k / 12 * 100) + '%';
    $('part').textContent = k < 6 ? '同じ？鏡？' : '少し難しく';
    $('shapes').innerHTML = svg(q.s, 0, false, '#4FC6B4') + '<span style="font-size:28px;color:#8D9BA1">→</span>' + svg(q.s, q.rot, q.mir, '#4FC6B4');
    $('opts').innerHTML = '<button type="button" data-v="0">同じ<small>回しただけ</small></button><button type="button" data-v="1">鏡<small>裏返し</small></button>';
    t0 = performance.now();
  }
  function stepStyle() {
    $('part').textContent = 'さいごに'; $('count').textContent = ''; $('shapes').innerHTML = ''; $('bar').style.width = '100%';
    $('q').textContent = 'どうやって解きましたか？（いちばん近いもの）';
    $('opts').className = 'syn-btns c1';
    $('opts').innerHTML = [['🔄 形ごと、頭の中で回した', 0], ['📍 とがった所やはしの1マスなど、一部分の向きで比べた', 1], ['✋ 自分の手や体を動かすつもりで考えた', 2]].map(([t, v]) => `<button type="button" data-s="${v}">${t}</button>`).join('');
  }
  $('opts').addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    if (b.dataset.s !== undefined) return done(+b.dataset.s);
    const v = +b.dataset.v; times.push(performance.now() - t0); ok.push((v === 1) === Q[k].mir);
    k++; if (k < 12) show(); else stepStyle();
  });
  function done(st) {
    const n = ok.filter(Boolean).length, avg = times.reduce((a, b) => a + b, 0) / times.length / 1000;
    const T = [['🔄', 'くるっと型', '形ごと頭の中で回すタイプ。1971年の実験の人たちと同じ解き方で、大きく回す問題ほど時間がかかりやすいのが特ちょうです。'],
               ['📍', '目印型', '一部分の向きだけを比べるタイプ。全部を回さなくてすむので、積み木のような複雑な形でも迷いにくい解き方です。'],
               ['✋', 'からだ型', '自分の手や体を動かすつもりで考えるタイプ。頭の中で回すとき、体を動かす準備をする脳の場所が働くこともあります。']][st];
    NOU.finish({
      label: '正解数（12問中）', big: n, unit: ' 問', emoji: T[0], typeName: T[1], advice: T[2] + ' この力は練習で伸びることが、217の研究のまとめで分かっています。',
      extraHTML: `<div class="syn-rows"><div><span class="k">正解</span><span class="v">${n} / 12 問</span></div><div><span class="k">1問の平均</span><span class="v">${avg.toFixed(1)} 秒</span></div><div><span class="k">前半（やさしめ）</span><span class="v">${ok.slice(0, 6).filter(Boolean).length} / 6</span></div><div><span class="k">後半（大きく回す）</span><span class="v">${ok.slice(6).filter(Boolean).length} / 6</span></div></div>`,
      share: `図形回転テストやってみた🔄 12問中${n}問正解・1問${avg.toFixed(1)}秒で「${T[1]}」でした。この形、同じ？鏡？`,
      cardTitle: 'わたしの頭の中の回転', cardLine: `12問中 ${n}問正解 ・ 1問 ${avg.toFixed(1)}秒`,
      draw: (x, R) => {
        for (let i = 0; i < 12; i++) { const col = i % 6, row = Math.floor(i / 6), xx = R.x + 60 + col * 140, yy = R.y + 80 + row * 220;
          x.fillStyle = ok[i] ? '#4FC6B4' : '#2A3C43'; x.beginPath(); x.roundRect(xx, yy, 110, 160, 22); x.fill();
          x.fillStyle = ok[i] ? '#0D1417' : '#8D9BA1'; x.font = '900 56px ' + R.F; x.textAlign = 'center'; x.fillText(ok[i] ? '○' : '×', xx + 55, yy + 102); }
      },
    });
  }
  function start() { k = 0; ok = []; times = []; make(); $('opts').className = 'syn-btns'; $('q').textContent = '右の形は　回しただけ？　鏡？'; NOU.startPanels(); show(); }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "2つの形が「回しただけ（同じ）」か「裏返し（鏡）」かを答える、メンタルローテーション（心の中の回転）のセルフテストです。形はこのページで作ったもので、研究で使われた図の写しではありません。",
    "article": """
    <h2>メンタルローテーション（心の中の回転）とは</h2>
    <p>頭の中で、形を回して比べる力のことです。1971年、アメリカの心理学者シェパードとメッツラーは、積み木をつないだような立体の絵を2つ並べて「同じ立体か、鏡の立体か」を答えてもらいました。すると、<b>2つの向きの角度の差が大きいほど、答えるまでの時間が一直線に長くなりました</b>。絵の平面の中で回したときも、奥へ回したときも、かかる時間は変わりませんでした（Shepard・Metzler 1971）。まるで頭の中で、立体を本当に回しているかのようです。</p>

    <h2>形の力と、理系の進路</h2>
    <p>アメリカの高校生約40万人を11年追った研究では、理系（科学・技術・工学・数学）の博士になった人の<b>45%が、高校のとき形の力が上から4%</b>に入っていました。また、形の力が上から1%の人の70%は、数学や言葉のテストでは上から1%に入っていませんでした（Wai ほか 2009）。数学と言葉だけで選ぶと、見落とされてしまう力です。</p>

    <h2>練習で伸びる</h2>
    <p>形の力の練習を調べた217の研究をまとめると、練習した人ははっきり伸び、時間がたっても伸びは残り、練習していない別の形の課題にも広がりました（Uttal ほか 2013）。10時間のアクションゲームで、頭の中で回す力が伸びたという研究もあります（Feng ほか 2007）。子どものころのパズル遊びとのつながりも報告されています（Levine ほか 2012）。</p>

    <h2>解き方の3つのタイプ</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>解き方</th></tr>
    <tr><td>🔄 くるっと型</td><td>形ごと、頭の中で回した</td></tr>
    <tr><td>📍 目印型</td><td>とがった所やはしの1マスなど、一部分の向きで比べた</td></tr>
    <tr><td>✋ からだ型</td><td>自分の手や体を動かすつもりで考えた</td></tr>
    </table>
    </div>
    <p>タイプは、このページだけの遊びの区切りで、研究の基準ではありません。問題によって解き方が変わるのも自然なことです。</p>
""",
    "faq": [
        ("点数が低かったら、空間認識が苦手ということですか？", "いいえ。12問だけの遊びのセルフテストで、その日の調子や画面の大きさでも変わります。この力は練習で伸びることも分かっています（Uttal ほか 2013）。"),
        ("男女で差があるのですか？", "紙のテストの男女差は、時間を短く決めるほど大きく出ることが分かっています（Voyer 2011）。10時間のゲーム練習で差が小さくなったという研究もあり（Feng ほか 2007）、どちらが上と決まった力ではありません。"),
        ("コツはありますか？", "はしの1マスから順番にたどる、曲がり角を1つ選んで左右の向きを比べる、手を形と同じ向きにかまえて回してみる、などの方法があります。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Shepard RN, Metzler J (1971). Mental rotation of three-dimensional objects. <i>Science</i>, 171(3972), 701–703.",
        "Wai J, Lubinski D, Benbow CP (2009). Spatial ability for STEM domains: Aligning over 50 years of cumulative psychological knowledge solidifies its importance. <i>Journal of Educational Psychology</i>, 101(4), 817–835.",
        "Uttal DH, et al. (2013). The malleability of spatial skills: A meta-analysis of training studies. <i>Psychological Bulletin</i>, 139(2), 352–402.",
        "Feng J, Spence I, Pratt J (2007). Playing an action video game reduces gender differences in spatial cognition. <i>Psychological Science</i>, 18(10), 850–855.",
        "Voyer D (2011). Time limits and gender differences on paper-and-pencil tests of mental rotation: A meta-analysis. <i>Psychonomic Bulletin &amp; Review</i>, 18(2), 267–277.",
        "Levine SC, Ratliff KR, Huttenlocher J, Cannon J (2012). Early puzzle play: A predictor of preschoolers' spatial transformation skill. <i>Developmental Psychology</i>, 48(2), 530–542.",
    ],
    "related": [("zukei-housoku", "🔷", "図形の法則テスト"), ("iq-yottsu-chikara", "🧠", "IQ 4つの力テスト"), ("iq-test", "🧩", "IQテスト（しま模様）"), ("stroop-test", "🎨", "色の名前テスト（ストループ）")],
}
