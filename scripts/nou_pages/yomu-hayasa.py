# -*- coding: utf-8 -*-
# 十人十脳 第23話「読むのが速い人」と連動（2026-11-05 新規）。文章はこのページのために書いた作り話
PAGE = {
    "slug": "yomu-hayasa",
    "title": "読む速さテスト｜1分間に何文字読める？読む速さと内容の理解を同時に測る｜シミュラボ",
    "desc": "約580字の短いお話を読んで、1分間に何文字読めるかを測るセルフテスト。読んだあとに3つの問題で、内容がちゃんと頭に入ったかも確かめます。190の研究をまとめた読む速さの研究や、「速読」についての研究も解説。診断ではありません。",
    "og_title": "1分間に何文字読める？｜読む速さテスト",
    "og_desc": "短いお話を読んで、読む速さと理解を同時に測る。",
    "ld_name": "読む速さテスト（1分間に何文字？）",
    "h1": "読む速さテスト（1分間に何文字読める？）",
    "lead": "同じ本を、ほかの人の半分の時間で読み終える人がいます。読む速さは、人によってかなりちがいます。短いお話をふだんどおりに読んで、読む速さと、内容がどのくらい頭に入ったかを測ってみましょう。約2分です。",
    "start_h2": "📖 ふだんどおりに読んでね",
    "start_text": "「読みはじめる」を押すとお話が出て、時間を測りはじめます。声に出さず、ふだん本を読むときと同じように読んでください。読み終わったらボタンを押すと、内容についての問題が3つ出ます。",
    "tag": "読む速さ",
    "card_label": "読む速さテストの結果",
    "card_footer": "1分間に何文字読める？ → shimulabo.com",
    "stage_html": """
      <div class="syn-top"><span id="part">読む</span><span id="count"></span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div id="txt" style="text-align:left;font-size:16px;line-height:1.95;color:#EEEAE3;background:#16242a;border-radius:14px;padding:16px 18px;margin:8px 0 12px;" hidden></div>
      <div class="syn-ask" id="q" style="font-size:18px;font-weight:700;color:#EEEAE3;min-height:2.4em;line-height:1.7;"></div>
      <div class="syn-btns c1" id="opts"></div>
    """,
    "js": r"""
  const $ = NOU.$;
  const TXT = [
    '駅前の小さなパン屋には、毎朝六時になると決まって一匹の三毛猫がやって来る。店主の春子さんは、その猫を「ジャム」と呼んでいた。初めて来た日に、いちごジャムのびんの横で丸くなって眠っていたからだ。',
    'ジャムは、パンをねだるわけではない。店の前の青いベンチに座り、焼き上がったパンが棚に並ぶのを、じっとながめているだけだった。客が来ると、しっぽを一度だけゆらして、また前を向く。常連の人たちは、その様子を見るのを毎朝の楽しみにしていた。',
    'ある冬の朝、ジャムが来なかった。次の日も、その次の日も、青いベンチは空いたままだった。春子さんは心配になって、近所の人にたずねて回った。すると、駅の向こうの花屋の店主が、「三日前から、うちの店先で寝ていますよ」と教えてくれた。花屋の入り口には、小さなストーブが置いてあったのだ。',
    '花屋の店主によると、ジャムは店のバケツの水を飲み、ストーブの前で気持ちよさそうに目を細めていたという。春子さんは花屋にお礼を言い、焼きたてのくるみパンを一つ置いて帰った。',
    '春子さんは少し笑って、次の朝、青いベンチの上に古い毛布を一枚しいておいた。その日の六時、ジャムはいつものようにやって来て、毛布の上で丸くなった。それからというもの、春子さんの店の前には、毛布のしかれた青いベンチが一年中置かれている。冬が来るたびに、毛布は少しずつ厚くなっていった。',
  ];
  const NCH = TXT.join('').length;
  const Q = [
    ['猫が「ジャム」と呼ばれたのは、なぜ？', ['ジャムのびんの横で眠っていたから', 'ジャムが大好物だったから', '毛の色がジャムに似ていたから', '春子さんがジャム作りが得意だったから'], 0],
    ['ジャムが来なくなったとき、どこにいた？', ['近所の公園', '駅の向こうの花屋', '春子さんの家の中', '駅のホーム'], 1],
    ['次の朝、春子さんがベンチにしたことは？', ['ストーブを置いた', '焼きたてのパンを置いた', '古い毛布をしいた', 'ベンチを新しくした'], 2],
  ];
  let t0 = 0, sec = 0, k = -1, right = 0;
  function intro() { k = -1; right = 0; $('part').textContent = '読む'; $('count').textContent = ''; $('bar').style.width = '0%'; $('txt').hidden = true;
    $('q').textContent = '準備ができたら、読みはじめてね'; $('opts').innerHTML = '<button type="button" data-v="read">読みはじめる</button>'; }
  function read() { $('txt').innerHTML = TXT.map(p => `<p style="margin:0 0 .7em;text-indent:1em;">${p}</p>`).join(''); $('txt').hidden = false; $('q').textContent = '';
    $('opts').innerHTML = '<button type="button" data-v="end">読み終わった</button>'; t0 = performance.now(); }
  function showQ() { const [q, o] = Q[k]; $('part').textContent = '内容の問題'; $('count').textContent = (k + 1) + ' / 3'; $('bar').style.width = ((k + 1) / 4 * 100) + '%';
    $('q').textContent = q; $('opts').innerHTML = o.map((t, i) => `<button type="button" data-v="${i}">${t}</button>`).join(''); }
  $('opts').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; const v = b.dataset.v;
    if (v === 'read') { read(); return; }
    if (v === 'end') { sec = (performance.now() - t0) / 1000; $('txt').hidden = true; $('txt').innerHTML = ''; k = 0; showQ(); return; }
    if (+v === Q[k][2]) right++; k++; if (k < 3) showQ(); else done(); });
  function done() {
    const cpm = Math.round(NCH / sec * 60);
    const T = cpm >= 2500 ? ['⚡', 'ななめ読みタイプ', 'ふつうに読むにはとても速いペースでした。ななめ読みをしたのかもしれません。'] : cpm >= 1000 ? ['🚀', '速く読むタイプ', 'とても速いペースで読みました。'] : cpm >= 500 ? ['📖', 'ふつうのペースで読むタイプ', 'ほどよいペースで読みました。'] : ['🐢', 'じっくり読むタイプ', 'ゆっくり、ていねいに読むタイプです。'];
    const cmt = right === 3 ? '内容もしっかり頭に入っていました。' : right === 2 ? '内容も、だいたい頭に入っていました。' : '内容の問題は少しむずかしかったようです。速く読むほど、内容が頭に残りにくくなることがあります。';
    NOU.finish({
      label: '1分間に読んだ文字数', big: cpm.toLocaleString(), unit: ' 字 / 分', emoji: T[0], typeName: T[1], advice: T[2] + cmt,
      extraHTML: `<div class="syn-rows"><div><span class="k">読んだ文字数</span><span class="v">${NCH} 字</span></div><div><span class="k">かかった時間</span><span class="v">${sec.toFixed(1)} 秒</span></div><div><span class="k">内容の問題</span><span class="v">${right} / 3 問 正解</span></div></div><p style="font-size:12px;color:var(--ink-3);">文字数は、句読点やかっこも1字として数えています。タイプの区切りは、このページで決めた目安です。</p>`,
      share: `読む速さテストやってみた📖 1分間に${cpm}字・内容の問題${right}/3問で「${T[1]}」でした。あなたは1分間に何文字読める？`,
      cardTitle: 'わたしの読む速さ', cardLine: `1分間に ${cpm.toLocaleString()}字・内容 ${right}/3問`,
      draw: (x, R) => {
        const y = R.y + 220, mx = 1500, w = Math.min(1, cpm / mx) * R.w;
        x.fillStyle = '#2A3C43'; x.beginPath(); x.roundRect(R.x, y, R.w, 80, 40); x.fill();
        x.fillStyle = '#4FC6B4'; x.beginPath(); x.roundRect(R.x, y, Math.max(80, w), 80, 40); x.fill();
        x.fillStyle = '#EEEAE3'; x.textAlign = 'center'; x.font = '900 120px ' + R.F; x.fillText(cpm.toLocaleString(), R.x + R.w / 2, y - 60);
        x.font = '800 34px ' + R.F; x.textAlign = 'left'; x.fillText('0', R.x, y + 130); x.textAlign = 'right'; x.fillText('1,500字/分', R.x + R.w, y + 130);
        for (let i = 0; i < 3; i++) { x.fillStyle = i < right ? '#F5BB5C' : '#2A3C43'; x.beginPath(); x.arc(R.x + R.w / 2 - 110 + i * 110, y + 230, 40, 0, Math.PI * 2); x.fill(); }
      },
    });
  }
  function start() { NOU.startPanels(); intro(); }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "このページのために書いた約580字の短いお話を読み、かかった時間から1分間に読んだ文字数を出し、内容についての3つの問題で理解を確かめるセルフテストです。",
    "article": """
    <h2>人は1分間に、どのくらい読める？</h2>
    <p>英語の読む速さについて、190の研究・1万8千人あまりのデータをまとめた研究があります（Brysbaert 2019）。大人が声に出さずに読む速さの平均は、<b>説明文で1分間に238語、物語で260語</b>でした。</p>
    <p>よく「1分間に300語」と言われることがありますが、この研究では、それは多くの人にとって高すぎる目標だとしています。</p>
    <p>日本語の読む速さは、文章のむずかしさや、文字の大きさ、測り方によって大きく変わります。このページのタイプの区切りは、目安として決めたものです。</p>

    <h2>目は、止まっては跳んでいる</h2>
    <p>文章を読むとき、目はすべるように動いているように感じます。でも実際には、<b>文字の上で一瞬止まっては、次の場所へ跳ぶ</b>ことをくり返しています（Rayner ほか 2016）。読むのが速い人は、止まる回数が少なかったり、止まる時間が短かったりします。</p>

    <h2>「速読」で、速く読めるようになる？</h2>
    <p>読む速さを何倍にもできる、とうたう「速読」の方法があります。読む研究をまとめた2016年の研究では、<b>速く読むほど内容の理解は落ちやすく、速さと理解の両方を大きく上げる近道は見つかっていない</b>とされました（Rayner ほか 2016）。</p>
    <p>そこでこのテストでは、読む速さだけでなく、読んだあとに内容の問題も出しています。速くても、内容が頭に入っていなければ意味がないからです。</p>

    <h2>結果の3つのタイプ</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>1分間の文字数</th></tr>
    <tr><td>⚡ ななめ読みタイプ</td><td>2,500字以上</td></tr>
    <tr><td>🚀 速く読むタイプ</td><td>1,000〜2,499字</td></tr>
    <tr><td>📖 ふつうのペースで読むタイプ</td><td>500〜999字</td></tr>
    <tr><td>🐢 じっくり読むタイプ</td><td>500字未満</td></tr>
    </table>
    </div>
""",
    "faq": [
        ("速く読むほうがいいのですか？", "いいえ。読む目的によって、ちょうどよい速さはちがいます。じっくり読むほうが、内容がよく頭に残ることもあります。"),
        ("スマホと紙で結果は変わりますか？", "文字の大きさや画面の明るさで、読みやすさが変わることがあります。くらべるときは、同じ画面で試してください。"),
        ("このテストで読む力の障害が分かりますか？", "いいえ。遊びのためのセルフテストで、検査や診断ではありません。読むことで困っているときは、専門の機関に相談できます。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Brysbaert M (2019). How many words do we read per minute? A review and meta-analysis of reading rate. <i>Journal of Memory and Language</i>, 109, 104047.",
        "Rayner K, Schotter ER, Masson MEJ, Potter MC, Treiman R (2016). So much to read, so little time: How do we read, and can speed reading help? <i>Psychological Science in the Public Interest</i>, 17(1), 4–34.",
    ],
    "related": [("naigen-test", "🗣️", "頭の中の声テスト（内言）"), ("kazu-shunkan", "🔢", "数の瞬間テスト（一瞬で数が分かる？）"), ("tango-kioku", "📝", "単語記憶テスト"), ("shikou-type", "🧠", "絵で考える人・言葉で考える人テスト")],
}
