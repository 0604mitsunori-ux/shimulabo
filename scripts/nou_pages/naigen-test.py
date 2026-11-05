# -*- coding: utf-8 -*-
# 十人十脳 第4話「頭の中の声」と連動（2026-11-05 新規）
PAGE = {
    "slug": "naigen-test",
    "title": "頭の中の声テスト｜考えるとき、頭の中で声はしていますか？内言のタイプを試す｜シミュラボ",
    "desc": "考えごとをするとき、頭の中で声がしゃべっていますか？頭の中の声（内言）は、ずっとしゃべっている人から、まったくない人までいると報告されています。8つの質問と、声に出さずに答える8問で、あなたの頭の中の声のタイプを試すセルフテスト。診断ではありません。",
    "og_title": "頭の中で、声はしていますか？｜頭の中の声テスト",
    "og_desc": "頭の中の声は、ずっとしゃべっている人から、まったくない人まで。あなたは？",
    "ld_name": "頭の中の声テスト（内言のタイプ）",
    "h1": "頭の中の声テスト（考えるとき、頭の中で声はしていますか？）",
    "lead": "この文を読んでいるいま、頭の中で声が読み上げていますか？考えごとをするとき、言葉が頭の中で流れる人もいれば、まったく流れない人もいます。8つの質問と、声に出さずに答える8問で試してみましょう。約3分です。",
    "start_h2": "💬 頭の中の声について、答えてね",
    "start_text": "前半は、ふだんの頭の中について8つの質問（5段階）。後半は、2つの絵の名前の「最後の音」が同じかどうかを、声に出さずにできるだけ速く答える8問です。",
    "tag": "頭の中の声",
    "card_label": "頭の中の声テストの結果",
    "card_footer": "頭の中で、声はしていますか？ → shimulabo.com",
    "stage_html": """
      <div class="syn-top"><span id="part">前半：ふだんの頭の中</span><span id="count">1 / 16</span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div id="qa">
        <div class="syn-ask" id="qtext" style="font-size:18px;font-weight:700;color:#EEEAE3;min-height:3.4em;"></div>
        <div class="syn-btns c1" id="opts"></div>
      </div>
      <div id="rh" hidden>
        <div class="syn-ask" style="font-size:14px;">声に出さずに：2つの絵の名前の<b>最後の音</b>は同じ？</div>
        <div class="syn-big" id="pair" style="font-size:84px;letter-spacing:.2em;"></div>
        <div class="syn-btns" id="rhBtns"><button type="button" data-v="1">同じ</button><button type="button" data-v="0">ちがう</button></div>
        <p class="syn-note">絵の名前は、ふだん呼んでいる名前で（例：🐻＝くま）。</p>
      </div>
    """,
    "js": r"""
  const $ = NOU.$;
  // 前半の質問（研究の質問票の「頭の中の声の種類」の考え方をもとに、このページで作った文）
  const Q = [
    ['何かを考えるとき、頭の中で言葉がしゃべっている', 'amount'],
    ['文章を読むとき、頭の中で声に出して読んでいる', 'amount'],
    ['頭の中で、自分と会話するように考えることがある', 'dialog'],
    ['頭の中の言葉は、文にならず、短い言葉だけのことが多い', 'short'],
    ['頭の中で、家族や友だちの話し方を思い出しながら考えることがある', 'others'],
    ['頭の中の声で、自分をはげましたり落ち着かせたりする', 'positive'],
    ['頭の中の声で、自分を責めたり、きびしく言ったりする', 'critical'],
    ['頭の中は、言葉がなくて静かなことが多い', 'quiet'],
  ];
  const LV = [['とてもあてはまる', 5], ['ややあてはまる', 4], ['どちらとも言えない', 3], ['あまりあてはまらない', 2], ['まったくあてはまらない', 1]];
  // 後半：名前の最後の音（くま・うま＝同じ）
  const P = [['🐻', '🐴', 1], ['🐱', '🐙', 1], ['🍓', '🥚', 1], ['🍌', '🐟', 1], ['🐶', '☂️', 0], ['👟', '🐢', 0], ['🚗', '🍎', 0], ['👓', '❄️', 0]];
  let k = 0, A = {}, order = [], rh = [], t0 = 0;
  $('opts').innerHTML = LV.map(([t, v]) => `<button type="button" data-v="${v}">${t}</button>`).join('');
  function showQ() { $('qtext').textContent = Q[k][0]; $('count').textContent = (k + 1) + ' / 16'; $('bar').style.width = (k / 16 * 100) + '%'; }
  function showR() { const j = k - 8, p = order[j]; $('pair').textContent = p[0] + ' ' + p[1]; $('count').textContent = (k + 1) + ' / 16'; $('bar').style.width = (k / 16 * 100) + '%'; t0 = performance.now(); }
  $('opts').addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return; A[Q[k][1]] = (A[Q[k][1]] || 0) + (+b.dataset.v); k++;
    if (k < 8) showQ(); else { $('qa').hidden = true; $('rh').hidden = false; $('part').textContent = '後半：声に出さずに答える'; showR(); }
  });
  $('rhBtns').addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return; const p = order[k - 8];
    rh.push({ ok: +b.dataset.v === p[2], ms: performance.now() - t0 }); k++;
    if (k < 16) showR(); else done();
  });
  function done() {
    const amount = A.amount + A.dialog + (6 - A.quiet);          // 4〜20（「しゃべっている」「声に出して読む」「会話する」「静か（反対に数える）」の4問）
    const T = amount >= 16 ? ['📢', '頭の中がにぎやかなタイプ', '考えるときも読むときも、頭の中でよく声がしているようです。']
            : amount >= 10 ? ['💬', 'ときどき声がするタイプ', '頭の中の声は、場面によって出たり出なかったりするようです。多くの人はこのあたりです。']
            : ['🤫', '頭の中が静かなタイプ', '頭の中で言葉が流れることは少ないようです。研究で「頭の中の声がほとんどない」と答える人の答え方に近いかもしれません。'];
    const okN = rh.filter(r => r.ok).length, ms = rh.map(r => r.ms).sort((a, b) => a - b), med = (ms[3] + ms[4]) / 2 / 1000;
    const F = [['会話するように考える', A.dialog], ['短い言葉で考える', A.short], ['ほかの人の話し方で考える', A.others], ['自分をはげます声', A.positive], ['自分を責める声', A.critical]];
    const rows = F.map(([n, v]) => `<div><span class="k">${n}</span><span class="syn-meter"><i style="width:${v * 20}%"></i></span><span class="v">${v}</span></div>`).join('');
    NOU.finish({
      label: '頭の中の声の多さ（4〜20）', big: amount, unit: ' / 20', emoji: T[0], typeName: T[1], advice: T[2],
      extraHTML: `<div class="syn-rows">${rows}<div><span class="k">後半（最後の音が同じか）</span><span class="v">${okN} / 8 問・1問 ${med.toFixed(1)} 秒</span></div></div>
        <p style="font-size:12px;color:var(--ink-3);">頭の中の声が少ないと答えた人は、言葉の最後の音を比べる課題に時間がかかりやすい、という研究があります（下の解説）。ただし、この8問だけで何かが分かるものではありません。</p>`,
      share: `頭の中の声テストやってみた💬 声の多さ ${amount}/20で「${T[1]}」でした。あなたの頭の中では、声がしていますか？`,
      cardTitle: 'わたしの頭の中の声', cardLine: `声の多さ ${amount} / 20・後半 ${okN}/8 問`,
      draw: (x, r) => {
        F.forEach(([n, v], i) => {
          const y = r.y + 40 + i * 100;
          x.textAlign = 'left'; x.fillStyle = '#EEEAE3'; x.font = '800 36px ' + r.F; x.fillText(n, r.x, y);
          x.fillStyle = '#2A3C43'; x.beginPath(); x.roundRect(r.x, y + 20, r.w, 30, 15); x.fill();
          x.fillStyle = '#4FC6B4'; x.beginPath(); x.roundRect(r.x, y + 20, r.w * v / 5, 30, 15); x.fill();
        });
      },
    });
  }
  function start() {
    k = 0; A = {}; rh = []; order = P.slice().sort(() => Math.random() - 0.5);
    $('qa').hidden = false; $('rh').hidden = true; $('part').textContent = '前半：ふだんの頭の中'; NOU.startPanels(); showQ();
  }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "ふだんの頭の中の声について8つの質問に答え、後半で、2つの絵の名前の最後の音が同じかどうかを声に出さずに答えるセルフテストです。研究で使われる考え方をもとにしていますが、問題はこのページで作ったものです。",
    "article": """
    <h2>頭の中の声（内言）とは</h2>
    <p>考えごとをするとき、頭の中で言葉が流れる感じがすることがあります。これを「内言（ないげん）」と呼びます。誰にでもあると思われてきましたが、最近の研究では、<b>ほとんどずっとしゃべっている人から、まったくない人まで</b>いると報告されています（Nedergaard・Lupyan 2024）。</p>
    <p>頭の中の声がほとんどないことには、2024年に「アネンドファジア」という名前が提案されました（同じ研究）。</p>

    <h2>声が少ない人は、何かちがう？</h2>
    <p>この研究では、頭の中の声が少ないと答えた46人と、多いと答えた47人を比べました。声が少ない人たちは、</p>
    <ul>
      <li>言葉を覚えておく課題の成績が低め</li>
      <li>2つの絵の名前が<b>韻をふんでいるか</b>（最後の音が同じか）を決めるのに苦労しやすい</li>
    </ul>
    <p>という結果でした。一方で、作業を切りかえる課題や、ものを見分ける課題では、ちがいはありませんでした（Nedergaard・Lupyan 2024）。このページの後半の8問は、この「最後の音が同じか」の考え方をもとにしています。</p>

    <h2>頭の中の声にも、種類がある</h2>
    <p>頭の中の声を調べる質問票の研究では、声の種類が5つに分けられています（Alderson-Day ほか 2018）。</p>
    <ul>
      <li>自分と<b>会話する</b>ような声</li>
      <li>文にならず、<b>短く縮まった</b>声</li>
      <li><b>ほかの人</b>の話し方が出てくる声</li>
      <li>自分を<b>評価したり責めたり</b>する声</li>
      <li>自分を<b>はげましたり落ち着かせたり</b>する声</li>
    </ul>
    <p>このテストの結果にも、この5つを並べています。同じ「頭の中の声がある」人どうしでも、声の中身はかなりちがうはずです。</p>

    <h2>まだ議論が続いている</h2>
    <p>「頭の中の声がまったくない人」が本当にいるのかについては、研究者のあいだでも意見が分かれています。2026年の論文では、少なくとも「ほとんどない」人は、おそらくよくいるだろうと述べられています（Hurlburt 2026）。分かっていないことが多い、新しい研究のテーマです。</p>

    <h2>となりのテーマ：頭の中の映像</h2>
    <p>頭の中に映像が浮かばない「アファンタジア」も、人によるちがいとして調べられています。映像と声、両方で試すと、自分の頭の中の「使い方」が見えてきます。→ <a href="../aphantasia-test/">アファンタジア テスト</a></p>

    <h2>結果の3つのタイプ</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>声の多さ（4〜20）</th></tr>
    <tr><td>📢 頭の中がにぎやかなタイプ</td><td>16以上</td></tr>
    <tr><td>💬 ときどき声がするタイプ</td><td>10〜15</td></tr>
    <tr><td>🤫 頭の中が静かなタイプ</td><td>9以下</td></tr>
    </table>
    </div>
    <p>声の多さは、前半の「言葉がしゃべっている」「声に出して読んでいる」「自分と会話する」「静かなことが多い（反対に数える）」の4問から出しています。分け方はこのページの目安です。</p>
""",
    "faq": [
        ("頭の中の声がないのは、おかしいことですか？", "研究者は、人による「ちがい」の1つとして調べています。声がほとんどなくても、考えたり話したりはできます。"),
        ("このテストで何が分かりますか？", "ふだんの頭の中の声について、あなた自身の答え方の傾向が分かります。研究の考え方をもとにした遊びのためのセルフテストで、検査や診断ではありません。"),
        ("後半の問題は何のため？", "頭の中の声が少ない人は、言葉の最後の音を比べる課題に時間がかかりやすい、という研究があります（Nedergaard・Lupyan 2024）。その考え方をもとにした8問ですが、8問だけで何かが分かるものではありません。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Nedergaard JSK, Lupyan G (2024). Not Everybody Has an Inner Voice: Behavioral Consequences of Anendophasia. <i>Psychological Science</i>, 35(7), 780–797.",
        "Alderson-Day B, Mitrenga K, Wilkinson S, McCarthy-Jones S, Fernyhough C (2018). The varieties of inner speech questionnaire – Revised (VISQ-R). <i>Consciousness and Cognition</i>, 65, 48–58.",
        "Hurlburt RT (2026). Fidelity Versus Validity Using Anendophasia as an Example: Commentary on Nedergaard and Lupyan (2024) and Lind (2025). <i>Psychological Science</i>.",
    ],
    "related": [("aphantasia-test", "🍎", "アファンタジア テスト（頭の中の映像）"), ("kyokankaku-test", "🔤", "共感覚テスト（文字に色が見える？）"), ("mimi-nenrei", "👂", "耳年齢テスト（モスキート音）"), ("tango-kioku", "📝", "単語記憶テスト")],
}
