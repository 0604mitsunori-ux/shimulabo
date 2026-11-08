# -*- coding: utf-8 -*-
# 十人十脳 第21話「待てる人・待てない人（マシュマロの実験）」と連動（2026-11-08 新規）
PAGE = {
    "slug": "matsu-chikara",
    "title": "待つ力テスト｜今もらう？あとで多く？マシュマロの実験と同じ選び方を10問で｜シミュラボ",
    "desc": "今すぐ1万円？それとも1年後に2万円？「今か、あとか」の10問に直感で答えると、あなたの選び方のタイプ（じっくり型・その時しだい型・いま大事型）が分かります。有名なマシュマロの実験、やり直し研究、約束を守る大人のもとで子どもが4倍待った研究、日本の子が食べ物を長く待てた研究も解説。診断ではありません。",
    "og_title": "今もらう？あとで多く？｜待つ力テスト",
    "og_desc": "マシュマロの実験と同じ「今か、あとか」の選び方を10問で。正解はありません。",
    "ld_name": "待つ力テスト（今か、あとか）",
    "h1": "待つ力テスト（今もらう？あとで多く？）",
    "lead": "今すぐもらうか、少し待って多くもらうか。<b>正解はありません</b>。直感で10問に答えてください。約1分です。お金の質問は遊びで、損得のアドバイスではありません。",
    "start_h2": "⏳ 今か、あとか。直感で10問",
    "start_text": "「今すぐ」と「あとで多く」のどちらがいいかを選びます。考えこまずに、ぱっと選んでください。",
    "tag": "マシュマロテスト",
    "card_label": "待つ力テストの結果",
    "card_footer": "今もらう？あとで多く？ → shimulabo.com",
    "stage_html": """
      <div class="syn-top"><span id="part">今か、あとか</span><span id="count"></span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div class="syn-ask" id="q" style="font-size:16px;">どちらがいい？</div>
      <div class="syn-btns" id="opts"></div>
      <p class="syn-note">※ 正解のない、好みの質問です。</p>
    """,
    "js": r"""
  const $ = NOU.$;
  const QZ = [
    ['💴 1万円', '1週間後に 1万500円'], ['🍰 ケーキ 1個', '1時間後に ケーキ 2個'], ['💴 1万円', '1年後に 2万円'], ['💴 1万円', '1日後に 1万100円'],
    ['🪙 100円', '1年後に 200円'], ['💴 5,000円', '3か月後に 6,000円'], ['💴 1万円', '1か月後に 1万2,000円'], ['💴 1万円', '10年後に 10万円'],
    ['🍫 チョコ 1枚', '明日 チョコ 3枚'], ['🎮 今日 30分遊ぶ', '週末に 2時間遊ぶ'],
  ];
  let k = 0, later = [];
  function show() {
    const [now, aft] = QZ[k]; $('count').textContent = (k + 1) + ' / 10'; $('bar').style.width = (k / 10 * 100) + '%';
    $('opts').innerHTML = `<button type="button" data-v="0">${now}<small>今すぐ</small></button><button type="button" data-v="1">${aft}<small>あとで</small></button>`;
  }
  $('opts').addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return; later.push(+b.dataset.v === 1); k++; if (k < 10) show(); else done();
  });
  function done() {
    const n = later.filter(Boolean).length;
    const T = n >= 8 ? ['🌱', 'じっくり型', '先の大きなものを選びやすいタイプ。待てば本当にもらえると信じられる環境にいるのかもしれません。']
            : n >= 4 ? ['⚖️', 'その時しだい型', '金額や待つ長さを見て、選び分けるタイプ。多くの人はこのあたりです。']
            : ['✋', 'いま大事型', '確かに手に入る「今」を選ぶタイプ。約束が守られない世界なら、それはかしこい選び方です（Kidd ほか 2013）。'];
    NOU.finish({
      label: '「あとで」を選んだ数（10問中）', big: n, unit: ' 問', emoji: T[0], typeName: T[1], advice: T[2],
      extraHTML: `<div class="syn-rows">${QZ.map((q, i) => `<div><span class="k">${q[0]} ／ ${q[1]}</span><span class="v">${later[i] ? 'あとで' : '今すぐ'}</span></div>`).join('')}</div>`,
      share: `待つ力テストやってみた⏳ 10問中「あとで」が${n}問で「${T[1]}」でした。今もらう？あとで多く？`,
      cardTitle: 'わたしの待つ力', cardLine: `「あとで」を選んだのは 10問中 ${n}問`,
      draw: (x, R) => {
        for (let i = 0; i < 10; i++) { const col = i % 5, row = Math.floor(i / 5), xx = R.x + 50 + col * 175, yy = R.y + 70 + row * 230;
          x.fillStyle = later[i] ? '#4FC6B4' : '#F5BB5C'; x.beginPath(); x.roundRect(xx, yy, 140, 170, 24); x.fill();
          x.fillStyle = '#0D1417'; x.font = '900 40px ' + R.F; x.textAlign = 'center'; x.fillText(later[i] ? 'あと' : '今', xx + 70, yy + 102); }
      },
    });
  }
  function start() { k = 0; later = []; NOU.startPanels(); show(); }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "「今すぐ」か「あとで多く」かを選ぶ、好みのセルフテストです（正解はありません）。質問はこのページで作ったものです。",
    "article": """
    <h2>マシュマロの実験</h2>
    <p>子どもの前にお菓子を1つ置き、「今食べてもいいけれど、大人がもどるまで待てたら2つ」と伝える。待てた時間を測る有名な実験です。1989年の報告では、4歳で長く待てた子は、10代で学校の成績が高く、ストレスにもうまく対処していました（Mischel ほか 1989）。</p>

    <h2>やり直してみると</h2>
    <p>2018年のやり直し研究では、4歳で待った時間と15歳の学力のつながりは、元の研究の<b>半分の大きさ</b>で、家の環境や幼いころの考える力などをそろえると、さらに3分の2ほど小さくなりました。学力の差のほとんどは「少なくとも20秒待てたか」から来ていました（Watts ほか 2018）。</p>

    <h2>待つのは、信じられるから</h2>
    <p>4歳半の子ども28人で、大人が「新しい画材を持ってくるね」という約束を守った子は平均12分、守らなかった子は平均3分でマシュマロを食べました（Kidd ほか 2013）。待つかどうかは、自分を抑える力だけでなく、<b>まわりを信じられるか</b>でも変わります。</p>
    <p>日本の子どもは、プレゼントより食べ物を長く待て、アメリカの子どもは逆でした。「いただきます」まで待つ習慣が、待つ力を支えているのかもしれません（Yanaoka ほか 2022）。</p>

    <h2>頭のよさとのつながり</h2>
    <p>24の研究をまとめると、頭のよさのテストの点が高い人ほど、あとの大きいものを選びやすい傾向がありましたが、つながりは弱めから中くらいでした（Shamosh・Gray 2008）。</p>

    <h2>結果の3つのタイプ</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>「あとで」の数</th></tr>
    <tr><td>🌱 じっくり型</td><td>8〜10問</td></tr>
    <tr><td>⚖️ その時しだい型</td><td>4〜7問</td></tr>
    <tr><td>✋ いま大事型</td><td>0〜3問</td></tr>
    </table>
    </div>
    <p>タイプは、このページだけの遊びの区切りで、研究の基準ではありません。どのタイプが正しい、ということもありません。</p>
""",
    "faq": [
        ("「今すぐ」が多いと、頭が悪いということですか？", "いいえ。やり直し研究では、待つ時間と学力のつながりは小さく、家の環境などでも説明できました。約束が守られない環境なら、今を選ぶのはかしこい選び方です。"),
        ("今の子どもは、昔より待てなくなったのですか？", "1960年代・80年代・2000年代の3〜5歳840人の記録を比べると、2000年代の子は1960年代の子より平均2分長く待てていました（Carlson ほか 2018）。"),
        ("お金の選び方の参考になりますか？", "このページは遊びのセルフテストで、損得のアドバイスではありません。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Mischel W, Shoda Y, Rodriguez MI (1989). Delay of gratification in children. <i>Science</i>, 244(4907), 933–938.",
        "Watts TW, Duncan GJ, Quan H (2018). Revisiting the marshmallow test. <i>Psychological Science</i>, 29(7), 1159–1177.",
        "Kidd C, Palmeri H, Aslin RN (2013). Rational snacking. <i>Cognition</i>, 126(1), 109–114.",
        "Yanaoka K, et al. (2022). Cultures crossing: The power of habit in delaying gratification. <i>Psychological Science</i>, 33(7), 1172–1181.",
        "Shamosh NA, Gray JR (2008). Delay discounting and intelligence: A meta-analysis. <i>Intelligence</i>, 36(4), 289–305.",
        "Carlson SM, et al. (2018). Cohort effects in children's delay of gratification. <i>Developmental Psychology</i>, 54(8), 1395–1407.",
    ],
    "related": [("dunning-kruger", "🤔", "ダニング＝クルーガー効果テスト"), ("tsukaimichi-test", "📎", "使い道テスト（発想）"), ("stroop-test", "🎨", "ストループテスト"), ("chrono", "⏰", "朝型・夜型診断")],
}
