# -*- coding: utf-8 -*-
# 十人十脳 第19話「顔の覚え方」と連動（2026-11-05 新規）。顔はこのページで作ったイラストだけを使い、実在の人の写真は使わない
PAGE = {
    "slug": "kao-kioku",
    "title": "顔の記憶力テスト｜人の顔を一度で覚えられる？8人の顔を覚えて当てる｜シミュラボ",
    "desc": "人の顔をすぐ覚える人と、何度会っても覚えられない人。8人の顔のイラストを20秒で覚えて、あとで出る16人の中から「見た顔」を当てるセルフテスト。顔を一度見たら忘れない「スーパー・レコグナイザー」の研究と、顔を覚えにくい人が約2.5%いるという研究も解説。診断ではありません。",
    "og_title": "人の顔を一度で覚えられる？｜顔の記憶力テスト",
    "og_desc": "8人の顔を20秒で覚えて、16人の中から当てる。あなたの顔の記憶力は？",
    "ld_name": "顔の記憶力テスト（8人の顔を覚えて当てる）",
    "h1": "顔の記憶力テスト（人の顔を一度で覚えられる？）",
    "lead": "一度会っただけの人の顔をずっと覚えている人もいれば、何度会っても「はじめまして」と言ってしまう人もいます。顔を覚える力は、人によってかなりちがうことが分かっています。8人の顔を覚えて、あとで当ててください。約2分です。",
    "start_h2": "🙂 8人の顔を覚えてね",
    "start_text": "8人の顔が20秒間出ます。そのあと16人の顔が1人ずつ出るので、さっき見た顔かどうかを答えてください。顔はこのページで作ったイラストです。",
    "tag": "顔の記憶",
    "card_label": "顔の記憶力テストの結果",
    "card_footer": "人の顔を一度で覚えられる？ → shimulabo.com",
    "stage_html": """
      <div class="syn-top"><span id="part">顔を覚えてね</span><span id="count"></span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div id="grid" style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;max-width:440px;margin:10px auto;"></div>
      <div id="one" style="width:190px;margin:10px auto;" hidden></div>
      <div class="syn-btns" id="opts"></div>
    """,
    "js": r"""
  const $ = NOU.$;
  const SK = ['#f3d3b8', '#e8bf9c', '#d6a47e'], HC = ['#2b211c', '#5a3b26', '#8f6d4b'];
  const N = { sk: 3, sh: 3, hr: 6, hc: 3, br: 3, ey: 4, no: 3, mo: 4 }, KEYS = Object.keys(N);
  const rnd = n => Math.floor(Math.random() * n);
  function face(f) {
    const sk = SK[f.sk], hc = HC[f.hc];
    const back = f.hr === 2 ? `<path d="M12 112 Q8 20 60 16 Q112 20 108 112 L94 112 Q98 52 60 42 Q22 52 26 112Z" fill="${hc}"/>` : f.hr === 3 ? `<path d="M10 140 Q4 18 60 14 Q116 18 110 140 L92 140 Q98 54 60 44 Q22 54 28 140Z" fill="${hc}"/>` : '';
    const head = f.sh === 0 ? `<ellipse cx="60" cy="76" rx="42" ry="50" fill="${sk}"/>` : f.sh === 1 ? `<ellipse cx="60" cy="78" rx="37" ry="55" fill="${sk}"/>` : `<rect x="19" y="28" width="82" height="98" rx="30" fill="${sk}"/>`;
    const ears = `<ellipse cx="${f.sh === 1 ? 22 : 18}" cy="82" rx="7" ry="11" fill="${sk}"/><ellipse cx="${f.sh === 1 ? 98 : 102}" cy="82" rx="7" ry="11" fill="${sk}"/>`;
    const HR = [
      `<path d="M18 64 Q20 20 60 20 Q100 20 102 64 Q90 40 60 38 Q30 40 18 64Z" fill="${hc}"/>`,
      `<path d="M16 72 Q14 16 62 16 Q104 18 104 68 Q96 42 72 36 Q50 48 24 52Z" fill="${hc}"/>`,
      `<path d="M18 62 Q22 18 60 18 Q98 18 102 62 Q84 44 60 44 Q36 44 18 62Z" fill="${hc}"/>`,
      `<path d="M18 62 Q22 18 60 18 Q98 18 102 62 Q84 40 60 40 Q36 40 18 62Z" fill="${hc}"/>`,
      `<circle cx="60" cy="14" r="13" fill="${hc}"/><path d="M18 64 Q20 22 60 22 Q100 22 102 64 Q90 42 60 40 Q30 42 18 64Z" fill="${hc}"/>`,
      `<path d="M18 62 L22 30 L32 38 L38 16 L50 30 L60 10 L70 30 L82 16 L88 38 L98 30 L102 62 Q90 42 60 40 Q30 42 18 62Z" fill="${hc}"/>`,
    ];
    const BR = [
      `<path d="M36 62 H52 M68 62 H84" stroke="${hc}" stroke-width="3" stroke-linecap="round"/>`,
      `<path d="M36 64 Q44 56 52 62 M68 62 Q76 56 84 64" stroke="${hc}" stroke-width="3" fill="none" stroke-linecap="round"/>`,
      `<path d="M35 60 L53 63 M67 63 L85 60" stroke="${hc}" stroke-width="6" stroke-linecap="round"/>`,
    ];
    const EY = [
      `<circle cx="44" cy="76" r="3.5" fill="#222"/><circle cx="76" cy="76" r="3.5" fill="#222"/>`,
      `<ellipse cx="44" cy="76" rx="7" ry="4.5" fill="#fff"/><ellipse cx="76" cy="76" rx="7" ry="4.5" fill="#fff"/><circle cx="44" cy="76" r="3" fill="#222"/><circle cx="76" cy="76" r="3" fill="#222"/>`,
      `<path d="M37 77 Q44 72 51 77 M69 77 Q76 72 83 77" stroke="#222" stroke-width="2.5" fill="none" stroke-linecap="round"/>`,
      `<circle cx="44" cy="76" r="7" fill="#fff" stroke="#222" stroke-width="1.5"/><circle cx="76" cy="76" r="7" fill="#fff" stroke="#222" stroke-width="1.5"/><circle cx="45" cy="77" r="4" fill="#222"/><circle cx="77" cy="77" r="4" fill="#222"/><circle cx="46.5" cy="75" r="1.3" fill="#fff"/><circle cx="78.5" cy="75" r="1.3" fill="#fff"/>`,
    ];
    const NO = [
      `<path d="M60 84 V94" stroke="#b07a5a" stroke-width="2.5" stroke-linecap="round"/>`,
      `<path d="M62 82 L56 96 H64" stroke="#b07a5a" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`,
      `<ellipse cx="60" cy="93" rx="7" ry="5" fill="#c98f6c"/>`,
    ];
    const MO = [
      `<path d="M48 106 Q60 116 72 106" stroke="#8a3b3b" stroke-width="3" fill="none" stroke-linecap="round"/>`,
      `<path d="M50 108 H70" stroke="#8a3b3b" stroke-width="3" stroke-linecap="round"/>`,
      `<ellipse cx="60" cy="108" rx="5" ry="6" fill="#8a3b3b"/>`,
      `<path d="M44 104 Q60 122 76 104Z" fill="#8a3b3b"/><path d="M47 105 H73 L71 109 H49Z" fill="#fff"/>`,
    ];
    return `<svg viewBox="0 0 120 140" style="display:block;width:100%;background:#2A3C43;border-radius:12px;">${back}${ears}${head}${HR[f.hr]}${BR[f.br]}${EY[f.ey]}${NO[f.no]}${MO[f.mo]}</svg>`;
  }
  const diff = (a, b) => KEYS.filter(k => a[k] !== b[k]).length;
  let olds = [], test = [], k = 0, res = [], timer = 0, left = 0;
  function make() {
    olds = []; while (olds.length < 8) { const f = {}; KEYS.forEach(k => f[k] = rnd(N[k])); if (olds.every(o => diff(o, f) >= 3)) olds.push(f); }
    const lures = []; olds.forEach(o => { for (let t = 0; t < 200; t++) {    // 見た顔の3か所だけを変えた「よく似た顔」
      const f = { ...o }; [...KEYS].sort(() => Math.random() - .5).slice(0, 3).forEach(k => { let v; do v = rnd(N[k]); while (v === o[k]); f[k] = v; });
      if (olds.every(x => diff(x, f) >= 2) && lures.every(x => diff(x, f) >= 2)) { lures.push(f); break; } } });
    if (lures.length < 8) return make();
    test = [...olds.map(f => ({ f, old: true })), ...lures.map(f => ({ f, old: false }))].sort(() => Math.random() - .5);
  }
  function study() {
    $('part').textContent = '顔を覚えてね'; $('grid').hidden = false; $('one').hidden = true;
    $('grid').innerHTML = olds.map(face).join(''); $('opts').className = 'syn-btns c1'; $('opts').innerHTML = '<button type="button" data-v="go">覚えた！</button>';
    left = 20; $('count').textContent = 'のこり ' + left + ' 秒'; $('bar').style.width = '0%';
    clearInterval(timer); timer = setInterval(() => { left--; $('count').textContent = 'のこり ' + left + ' 秒'; $('bar').style.width = ((20 - left) / 20 * 100) + '%'; if (left <= 0) quiz(); }, 1000);
  }
  function quiz() { clearInterval(timer); k = 0; res = []; $('grid').hidden = true; $('grid').innerHTML = ''; $('one').hidden = false; $('part').textContent = 'さっき見た顔？'; $('opts').className = 'syn-btns'; showQ(); }
  function showQ() { $('one').innerHTML = face(test[k].f); $('count').textContent = (k + 1) + ' / 16'; $('bar').style.width = (k / 16 * 100) + '%';
    $('opts').innerHTML = '<button type="button" data-v="y">見た</button><button type="button" data-v="n">見ていない</button>'; }
  $('opts').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return;
    if (b.dataset.v === 'go') { quiz(); return; }
    res.push((b.dataset.v === 'y') === test[k].old); k++; if (k < 16) showQ(); else done(); });
  function done() {
    const n = res.filter(Boolean).length, hit = test.filter((t, i) => t.old && res[i]).length, cr = test.filter((t, i) => !t.old && res[i]).length;
    const T = n >= 15 ? ['🦅', '顔をよく覚えるタイプ', 'よく似た顔の中から、見た顔をしっかり見分けられました。']
            : n >= 11 ? ['🙂', 'ふつうに覚えるタイプ', '多くの顔を覚えられていました。よく似た顔に、少しまよったかもしれません。']
            : ['🌀', '顔より別のことで覚えるタイプ', '今回は、よく似た顔を見分けるのがむずかしかったようです。人を声や服、話した内容で覚えている人もいます。'];
    NOU.finish({
      label: '16人中、正しく答えた人数', big: n, unit: ' / 16 人', emoji: T[0], typeName: T[1], advice: T[2],
      extraHTML: `<div class="syn-rows"><div><span class="k">見た顔を「見た」と答えた</span><span class="v">${hit} / 8 人</span></div><div><span class="k">初めての顔を「見ていない」と答えた</span><span class="v">${cr} / 8 人</span></div></div><p style="font-size:12px;color:var(--ink-3);">初めての顔は、見た顔の3か所だけを変えた「よく似た顔」です。イラストの顔なので、実際の人の顔を覚える力とは同じではありません。</p>`,
      share: `顔の記憶力テストやってみた🙂 16人中${n}人正解で「${T[1]}」でした。あなたは人の顔を一度で覚えられる？`,
      cardTitle: 'わたしの顔の記憶力', cardLine: `16人中 ${n}人 正解`,
      draw: (x, R) => {
        [['見た顔', test.map((t, i) => t.old ? res[i] : null).filter(v => v !== null)], ['初めての顔', test.map((t, i) => t.old ? null : res[i]).filter(v => v !== null)]].forEach(([lab, arr], row) => {
          const y = R.y + 90 + row * 240; x.fillStyle = '#EEEAE3'; x.textAlign = 'left'; x.font = '800 38px ' + R.F; x.fillText(lab, R.x, y);
          arr.forEach((ok, i) => { const cx = R.x + 58 + i * ((R.w - 116) / 7); x.fillStyle = ok ? '#4FC6B4' : '#2A3C43'; x.beginPath(); x.arc(cx, y + 90, 46, 0, Math.PI * 2); x.fill();
            x.fillStyle = ok ? '#0D1417' : '#8D9BA1'; x.textAlign = 'center'; x.font = '900 48px ' + R.F; x.fillText(ok ? '○' : '×', cx, y + 106); }); });
      },
    });
  }
  function start() { make(); NOU.startPanels(); study(); }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "このページで作った8人の顔のイラストを20秒で覚え、見た8人と、見た顔の3か所だけを変えたよく似た8人を合わせた16人について、見た顔かどうかを答えるセルフテストです。実在の人の顔は使っていません。",
    "article": """
    <h2>顔を一度見たら忘れない人がいる</h2>
    <p>2009年、アメリカの研究チームは、「自分は人の顔を覚えるのがとても得意だ」と言う4人を調べました。すると4人とも、2種類のまったくちがう顔のテストで、<b>くらべた人たちの範囲をこえる高い成績</b>を出しました（Russell ほか 2009）。</p>
    <p>研究チームはこうした人たちを<b>「スーパー・レコグナイザー（顔をとても見分けられる人）」</b>と呼びました。そして、顔を覚える力は「できる・できない」の2つではなく、<b>とても苦手な人からとても得意な人まで、なだらかに並んでいる</b>と考えました。</p>

    <h2>顔を覚えにくい人は、約2.5%</h2>
    <p>反対に、生まれつき顔を見分けるのがとても苦手な人もいます。ドイツの研究では、生徒・学生689人を調べて17人、<b>約2.5%</b>が、生まれつき顔を覚えにくい「相貌失認（そうぼうしつにん）」にあたると報告されました（Kennerknecht ほか 2006）。家族の中で続いて見られることがある、とも報告されています。</p>
    <p>こうした人は、顔のかわりに<b>声・髪型・歩き方・服</b>などで人を見分けていることがあります。目が悪いわけでも、人に興味がないわけでもありません。</p>

    <h2>このテストのしくみ</h2>
    <p>このページでは、顔の形・髪・まゆ・目・鼻・口などを組み合わせたイラストの顔を作っています。最後に出る「初めての顔」は、<b>見た顔の3か所だけを変えた、よく似た顔</b>です。そのため、髪型だけで覚えていると、まちがえやすくなっています。</p>
    <p>イラストの顔は、本物の人の顔とは見え方がちがいます。この結果は、実際に人の顔を覚える力とは同じではありません。</p>

    <h2>結果の3つのタイプ</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>16人中の正解</th></tr>
    <tr><td>🦅 顔をよく覚えるタイプ</td><td>15人以上</td></tr>
    <tr><td>🙂 ふつうに覚えるタイプ</td><td>11〜14人</td></tr>
    <tr><td>🌀 顔より別のことで覚えるタイプ</td><td>10人以下</td></tr>
    </table>
    </div>
""",
    "faq": [
        ("このテストでスーパー・レコグナイザーや相貌失認か分かりますか？", "いいえ。遊びのためのセルフテストで、検査や診断ではありません。研究では、本物の顔の写真を使った専用のテストで調べています。"),
        ("毎回結果が変わります。", "顔はその場で作っているので、毎回ちがう顔が出ます。何回か試して、だいたいの傾向を見てください。"),
        ("人の顔が覚えられなくて困っています。", "生活に困るほどのときは、医療機関に相談すると、くわしく調べてもらえることがあります。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Russell R, Duchaine B, Nakayama K (2009). Super-recognizers: People with extraordinary face recognition ability. <i>Psychonomic Bulletin &amp; Review</i>, 16(2), 252–257.",
        "Kennerknecht I, Grueter T, Welling B, ほか (2006). First report of prevalence of non-syndromic hereditary prosopagnosia (HPA). <i>American Journal of Medical Genetics Part A</i>, 140A(15), 1617–1622.",
    ],
    "related": [("tango-kioku", "📝", "単語の記憶テスト"), ("shunkan-kioku", "⚡", "瞬間記憶テスト"), ("kaotype-shindan", "🪞", "顔タイプ診断"), ("shikou-type", "🧠", "絵で考える人・言葉で考える人テスト")],
}
