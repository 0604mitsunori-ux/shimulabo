# -*- coding: utf-8 -*-
# 十人十脳 第23話「色の名前（ストループ効果）」と連動（2026-11-08 十人十脳の型で作り直し）
PAGE = {
    "slug": "stroop-test",
    "title": "ストループテスト｜字の色、すぐ答えられる？頭のブレーキを時間で測る｜シミュラボ",
    "desc": "「赤」という字が青で書いてあったら？字の意味ではなく、インクの色をボタンで答えるストループテスト。字と色が同じ10問・ちがう10問の時間とまちがいを比べて、頭のブレーキのタイプ（ブレーキ強め型・ふつう型・つられ型）が分かります。1935年の実験と、ブレーキの力とIQの関係も解説。診断ではありません。",
    "og_title": "字の色、すぐ答えられる？｜ストループテスト",
    "og_desc": "字の意味にひっぱられずに、インクの色を答えられる？頭のブレーキを時間で測る。",
    "ld_name": "ストループテスト（色の名前テスト）",
    "h1": "ストループテスト（字の色、すぐ答えられる？）",
    "lead": "画面の字の<b>意味ではなく、インクの色</b>をボタンで答えてください。字と色が同じ10問と、ちがう10問の時間を比べます。約1分です。",
    "start_h2": "🎨 インクの色を、すばやく答える",
    "start_text": "前半10問は字と色が同じ、後半10問は字と色がちがいます。できるだけ速く、正しく押してください。色の区別がつきにくい人は、無理をしないでください。",
    "tag": "ストループ効果",
    "card_label": "ストループテストの結果",
    "card_footer": "字の色、すぐ答えられる？ → shimulabo.com",
    "stage_html": """
      <div class="syn-top"><span id="part">字と色が同じ</span><span id="count"></span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div class="syn-ask">インクの色は？</div>
      <div class="syn-big" id="word" style="min-height:1.2em;"></div>
      <div class="syn-btns" id="opts" style="grid-template-columns:repeat(4,1fr);"></div>
    """,
    "js": r"""
  const $ = NOU.$;
  const C = [['赤', '#FF4D4F'], ['青', '#3B82F6'], ['緑', '#22C55E'], ['黄', '#FACC15']];
  $('opts').innerHTML = C.map(([n, c], i) => `<button type="button" data-v="${i}" style="font-weight:800;font-size:17px;border-color:${c}">${n}</button>`).join('');
  let k = 0, items = [], tSame = 0, tDiff = 0, errS = 0, errD = 0, t0 = 0, tStart = 0;
  function make() {
    items = [];
    for (let i = 0; i < 10; i++) { const w = Math.floor(Math.random() * 4); items.push([w, w]); }
    for (let i = 0; i < 10; i++) { const w = Math.floor(Math.random() * 4); let c = Math.floor(Math.random() * 3); if (c >= w) c++; items.push([w, c]); }
  }
  function show() {
    const [w, c] = items[k]; $('word').textContent = C[w][0]; $('word').style.color = C[c][1];
    $('part').textContent = k < 10 ? '字と色が同じ' : '字と色がちがう'; $('count').textContent = (k % 10 + 1) + ' / 10'; $('bar').style.width = (k / 20 * 100) + '%';
    if (k === 0 || k === 10) tStart = performance.now();
  }
  $('opts').addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b || !items.length) return;
    const v = +b.dataset.v, ok = v === items[k][1];
    if (k < 10) { if (!ok) errS++; } else { if (!ok) errD++; }
    k++;
    if (k === 10) { tSame = (performance.now() - tStart) / 1000; }
    if (k === 20) { tDiff = (performance.now() - tStart) / 1000; return done(); }
    show();
  });
  function done() {
    items = [];
    const pct = Math.round((tDiff / tSame - 1) * 100), slow = tDiff - tSame;
    const T = pct <= 15 && errD <= 1 ? ['🛑', 'ブレーキ強め型', '字を読むくせを、しっかり止められました。字と色がちがっても、あまり遅れませんでした。']
            : pct <= 60 && errD <= 3 ? ['⚖️', 'ふつう型', '字と色がちがうと、少しずつ遅れました。1935年の実験の大学生たちと同じように、だれにでも起きることです。']
            : ['📖', 'つられ型', '字を読むくせが強いタイプ。たくさん字を読んできた証拠でもあります。練習すると、このじゃまは小さくなります。'];
    NOU.finish({
      label: '字と色がちがうと、どれだけ遅くなった？', big: (pct >= 0 ? '+' : '') + pct, unit: ' %', emoji: T[0], typeName: T[1], advice: T[2],
      extraHTML: `<div class="syn-rows"><div><span class="k">字と色が同じ（10問）</span><span class="v">${tSame.toFixed(1)} 秒・まちがい ${errS}</span></div><div><span class="k">字と色がちがう（10問）</span><span class="v">${tDiff.toFixed(1)} 秒・まちがい ${errD}</span></div><div><span class="k">遅くなった時間</span><span class="v">${slow.toFixed(1)} 秒</span></div></div>`,
      share: `ストループテストやってみた🎨 字と色がちがうと${pct}%遅くなって「${T[1]}」でした。字の色、すぐ答えられる？`,
      cardTitle: 'わたしの頭のブレーキ', cardLine: `同じ ${tSame.toFixed(1)}秒 → ちがう ${tDiff.toFixed(1)}秒（${pct >= 0 ? '+' : ''}${pct}%）`,
      draw: (x, R) => {
        const mx = Math.max(tSame, tDiff) * 1.15;
        [['字と色が同じ', tSame, '#4FC6B4'], ['字と色がちがう', tDiff, '#F5BB5C']].forEach(([lab, v, c], i) => {
          const yy = R.y + 110 + i * 200, bw = (R.w - 80) * v / mx;
          x.fillStyle = '#EEEAE3'; x.textAlign = 'left'; x.font = '800 38px ' + R.F; x.fillText(lab, R.x + 40, yy - 18);
          x.fillStyle = '#2A3C43'; x.beginPath(); x.roundRect(R.x + 40, yy, R.w - 80, 90, 20); x.fill();
          x.fillStyle = c; x.beginPath(); x.roundRect(R.x + 40, yy, bw, 90, 20); x.fill();
          x.fillStyle = '#0D1417'; x.font = '900 48px ' + R.F; x.fillText(v.toFixed(1) + '秒', R.x + 64, yy + 62);
        });
      },
    });
  }
  function start() { k = 0; errS = errD = 0; make(); NOU.startPanels(); show(); }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "字の意味ではなくインクの色を答える、ストループ効果のセルフテストです。前半（字と色が同じ）と後半（字と色がちがう）の時間とまちがいを比べます。",
    "article": """
    <h2>ストループ効果とは</h2>
    <p>字の意味と色がちがうと、色の名前を言うのが遅くなる現象です。1935年、アメリカのストループは、赤・青・緑・茶・紫の名前を、わざとちがう色のインクで印刷しました。大学生にインクの色を100個言ってもらうと、色の四角なら平均63.3秒だったのが、字と色がちがうと110.3秒、<b>74%も長く</b>なりました。一方、字を読むだけなら、色がちがっても2.3秒（5.6%）しか長くなりませんでした（Stroop 1935）。</p>
    <p>ストループは、字を読むことのほうが、色の名前を言うことより、ずっとたくさん練習してきたからだと考えました。8日間、1日200回の練習で、このじゃまは小さくなりましたが、なくなりはしませんでした。</p>

    <h2>脳のブレーキ役と見張り役</h2>
    <p>色を言う準備をするときは、脳の前のほうの横（背外側前頭前野）が働き、字と色がちがう問題に答えるときは、前のほうの内側（前帯状皮質）が働くことが分かっています（MacDonald ほか 2000）。読むくせにブレーキをかける役と、まちがいそうなときに知らせる見張り役です。</p>

    <h2>ブレーキの力とIQ</h2>
    <p>頭をコントロールする力を「ブレーキ（つい出る反応を止める）」「切りかえ」「更新（覚えたものを入れかえる）」に分けると、IQと強くつながっていたのは「更新」で、ブレーキと切りかえは、ほかの力の分をそろえるとつながりが小さくなりました（Friedman ほか 2006）。頭のブレーキは、IQとは別の力なのです。</p>

    <h2>結果の3つのタイプ</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>目安</th></tr>
    <tr><td>🛑 ブレーキ強め型</td><td>遅れ15%以下・まちがい1つ以下</td></tr>
    <tr><td>⚖️ ふつう型</td><td>遅れ60%以下・まちがい3つ以下</td></tr>
    <tr><td>📖 つられ型</td><td>それより大きい</td></tr>
    </table>
    </div>
    <p>タイプは、このページだけの遊びの区切りで、研究の基準ではありません。ボタンの位置に慣れると速くなるので、何回か試してみてください。</p>
""",
    "faq": [
        ("2か国語を話す人はブレーキが強いのですか？", "そういう説がありますが、大人で比べた152の研究をまとめると、出版のかたよりを直したあとは、たしかな利点は残りませんでした（Lehtonen ほか 2018）。"),
        ("練習すると速くなりますか？", "1935年の実験では、8日間の練習でじゃまは小さくなりましたが、なくなりはしませんでした。このページでも、何回か試すと速くなるはずです。"),
        ("色の区別がつきにくいのですが", "このテストは色の区別が前提なので、無理をしないでください。動画では、数字の個数を答える「数のテスト」も紹介しています。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Stroop JR (1935). Studies of interference in serial verbal reactions. <i>Journal of Experimental Psychology</i>, 18(6), 643–662.",
        "MacDonald AW, Cohen JD, Stenger VA, Carter CS (2000). Dissociating the role of the dorsolateral prefrontal and anterior cingulate cortex in cognitive control. <i>Science</i>, 288(5472), 1835–1838.",
        "Friedman NP, et al. (2006). Not all executive functions are related to intelligence. <i>Psychological Science</i>, 17(2), 172–179.",
        "Lehtonen M, et al. (2018). Is bilingualism associated with enhanced executive functioning in adults? A meta-analytic review. <i>Psychological Bulletin</i>, 144(4), 394–425.",
    ],
    "related": [("mental-rotation", "🔄", "図形回転テスト"), ("zukei-housoku", "🔷", "図形の法則テスト"), ("matsu-chikara", "⏳", "待つ力テスト"), ("iq-yottsu-chikara", "🧠", "IQ 4つの力テスト")],
}
