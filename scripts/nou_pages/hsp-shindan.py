# -*- coding: utf-8 -*-
# 十人十脳 第16話「繊細さん（HSP）」と連動。既存の「HSP診断（繊細さん）」を同じURLのまま作り直した（2026-11-05）
PAGE = {
    "slug": "hsp-shindan",
    "title": "HSP診断（繊細さん）｜音や光に疲れやすいのはなぜ？12問で繊細さの4つの面を試す｜シミュラボ",
    "desc": "音や光、人の多い場所で疲れやすい「繊細さん（HSP）」。12の質問で、深く考える・刺激で疲れやすい・気持ちが動きやすい・細かいことに気づく、の4つの面を試すセルフテスト。906人を調べて「繊細さは3つのグループに分かれる」とした研究も解説。病気の診断ではありません。",
    "og_title": "音や光に疲れやすいのはなぜ？｜HSP診断（繊細さん）",
    "og_desc": "12の質問で、あなたの繊細さの4つの面を。蘭・チューリップ・タンポポ、あなたはどれ？",
    "ld_name": "HSP診断（繊細さん）",
    "h1": "HSP診断（繊細さん）（音や光に疲れやすいのはなぜ？）",
    "lead": "にぎやかな場所から帰るとぐったりする。人のきげんの変化にすぐ気づく。そんな「繊細さ」は、研究では生まれ持った気質のひとつと考えられています。12の質問に答えると、あなたの繊細さを4つの面に分けて見られます。約2分です。",
    "start_h2": "🌿 12の質問に答えてね",
    "start_text": "ふだんの自分に、どのくらいあてはまるかを選んでください。正解はありません。",
    "tag": "繊細さん",
    "card_label": "HSP診断（繊細さん）の結果",
    "card_footer": "音や光に疲れやすいのはなぜ？ → shimulabo.com",
    "stage_html": """
      <div class="syn-top"><span id="part">ふだんの自分は？</span><span id="count">1 / 12</span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div class="syn-big" id="em" style="font-size:56px;"></div>
      <div class="syn-ask" id="q" style="font-size:18px;font-weight:700;color:#EEEAE3;min-height:3.4em;line-height:1.7;"></div>
      <div class="syn-btns c1" id="opts"></div>
    """,
    "js": r"""
  const $ = NOU.$;
  // 4つの面（研究で挙げられる繊細さの特徴）×3問。問題はこのページで作ったもの
  const AX = [['🤔', '深く考える'], ['🔋', '刺激で疲れやすい'], ['💧', '気持ちが動きやすい'], ['🔍', '細かいことに気づく']];
  const Q = [
    [0, '買い物では、いろいろくらべてから決めたい'], [1, '予定がつまった日の夜は、ひとりの時間がほしい'], [2, '悲しいニュースを見ると、しばらく気持ちが引きずられる'],
    [3, '部屋の物の位置が少し変わると、すぐに気づく'], [0, '寝る前に、その日の会話を思い返すことが多い'], [1, 'にぎやかなイベントのあとは、次の日まで疲れが残る'],
    [2, '友だちが落ちこんでいると、自分まで気持ちが重くなる'], [3, '相手の声の調子で、きげんが分かる'], [0, '「なぜだろう」と、ものごとの意味を考えこむほうだ'],
    [1, 'テレビとスマホの音が同時に鳴ると、頭がいっぱいになる'], [2, '好きな曲や本で、涙が出ることがある'], [3, '季節が変わるときの、空気のにおいのちがいに気づく'],
  ];
  const O = [['とてもあてはまる', 4], ['ややあてはまる', 3], ['あまりあてはまらない', 2], ['まったくあてはまらない', 1]];
  let k = 0, sc = [0, 0, 0, 0];
  function show() { const [a, q] = Q[k]; $('em').textContent = AX[a][0]; $('q').textContent = q; $('count').textContent = (k + 1) + ' / 12'; $('bar').style.width = (k / 12 * 100) + '%';
    $('opts').innerHTML = O.map(([t, v]) => `<button type="button" data-v="${v}">${t}</button>`).join(''); }
  $('opts').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; sc[Q[k][0]] += +b.dataset.v; k++; if (k < 12) show(); else done(); });
  function done() {
    const s = sc.reduce((a, b) => a + b, 0);   // 12〜48
    const T = s >= 37 ? ['🌷', '蘭（オーキッド）タイプ', 'まわりの刺激や人の気持ちを、とても深く受け取るタイプです。疲れたら、静かな場所で休む時間を先に予定に入れておくと楽になります。']
            : s >= 26 ? ['🌼', 'チューリップタイプ', '繊細さがまん中くらいのタイプです。研究でも、このまん中のグループがいちばん多い結果でした。']
            : ['🌻', 'タンポポタイプ', 'まわりの刺激に左右されにくいタイプです。にぎやかな場所でも、わりと平気でいられます。'];
    const top = sc.indexOf(Math.max(...sc));
    const rows = AX.map(([e, n], i) => `<div style="margin:6px 0;"><div style="display:flex;justify-content:space-between;font-size:13px;"><span>${e} ${n}</span><b>${sc[i]} / 12</b></div><div style="height:10px;border-radius:5px;background:var(--line,#e5e1da);"><i style="display:block;height:100%;width:${(sc[i] - 3) / 9 * 100}%;border-radius:5px;background:#4FC6B4;"></i></div></div>`).join('');
    NOU.finish({
      label: '繊細さの合計（12〜48点）', big: s, unit: ' / 48 点', emoji: T[0], typeName: T[1], advice: T[2],
      extraHTML: `<p style="font-size:14px;margin:6px 0;">4つの面のうち、いちばん強く出たのは「${AX[top][1]}」でした。</p>${rows}<p style="font-size:12px;color:var(--ink-3);">タイプの分け方（点の区切り）は、このページで決めた目安です。</p>`,
      share: `HSP診断（繊細さん）やってみた🌿 ${s}/48点で「${T[1]}」、いちばん強いのは「${AX[top][1]}」でした。あなたは蘭・チューリップ・タンポポのどれ？`,
      cardTitle: 'わたしの繊細さ 4つの面', cardLine: `合計 ${s} / 48 点・いちばん強いのは「${AX[top][1]}」`,
      draw: (x, R) => {
        AX.forEach(([e, n], i) => { const y = R.y + 60 + i * 120;
          x.fillStyle = '#EEEAE3'; x.textAlign = 'left'; x.font = '800 40px ' + R.F; x.fillText(e + ' ' + n, R.x, y);
          x.fillStyle = '#2A3C43'; x.beginPath(); x.roundRect(R.x, y + 22, R.w, 40, 20); x.fill();
          x.fillStyle = i === top ? '#F5BB5C' : '#4FC6B4'; x.beginPath(); x.roundRect(R.x, y + 22, Math.max(40, R.w * (sc[i] - 3) / 9), 40, 20); x.fill();
          x.fillStyle = '#EEEAE3'; x.textAlign = 'right'; x.font = '900 40px ' + R.F; x.fillText(sc[i] + ' / 12', R.x + R.w, y); });
      },
    });
  }
  function start() { k = 0; sc = [0, 0, 0, 0]; NOU.startPanels(); show(); }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "深く考える・刺激で疲れやすい・気持ちが動きやすい・細かいことに気づく、の4つの面について3問ずつ、合わせて12問に答えるセルフテストです。問題は、研究で挙げられる繊細さの特徴をもとに、このページで作っています。",
    "article": """
    <h2>HSP（繊細さん）とは</h2>
    <p>HSPは「Highly Sensitive Person（とても敏感な人）」の頭文字です。アメリカの心理学者アーロン夫妻が1997年に発表した研究で、まわりの刺激を深く受け取る気質を「感覚処理感受性」と名づけ、それを測る<b>27問の質問票</b>を作りました（Aron・Aron 1997）。</p>
    <p>この研究では、繊細さは「人見知り（内向的）」や「気持ちが不安定になりやすいこと」と重なるところはあるものの、<b>それだけでは説明できない別の性質</b>だとされました。</p>
    <p>大事なのは、HSPは<b>病気の名前でも、正式な診断名でもない</b>ということです。背が高い人・低い人がいるように、生まれ持った気質のちがいのひとつと考えられています。</p>

    <h2>繊細さの4つの面</h2>
    <p>繊細さの研究では、次のような特徴がよく挙げられます。このページの12問は、この4つに分けて作っています。</p>
    <ul>
      <li>🤔 <b>深く考える</b>：決める前にじっくり考える、あとから何度も思い返す</li>
      <li>🔋 <b>刺激で疲れやすい</b>：音・光・人ごみ・予定のつめこみで、ぐったりしやすい</li>
      <li>💧 <b>気持ちが動きやすい</b>：人の気持ちに引きずられやすい、芸術や音楽に強く心が動く</li>
      <li>🔍 <b>細かいことに気づく</b>：小さな変化や、においや音の細かいちがいに気づく</li>
    </ul>

    <h2>繊細さは「3つのグループ」に分かれる</h2>
    <p>ある研究チームは、906人の大人の答えを統計で分けました。すると、人は次の3つのグループに分かれました（Lionetti ほか 2018）。</p>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>グループ</th><th>繊細さ</th><th>割合</th></tr>
    <tr><td>🌷 蘭（オーキッド）</td><td>高い</td><td>31%</td></tr>
    <tr><td>🌼 チューリップ</td><td>まん中</td><td>40%</td></tr>
    <tr><td>🌻 タンポポ</td><td>低い</td><td>29%</td></tr>
    </table>
    </div>
    <p>蘭は、育て方しだいでとても美しく咲く一方、環境が合わないと弱りやすい花です。タンポポはどこでもたくましく育ちます。繊細な人は、<b>まわりの環境のよい面からも悪い面からも、強く影響を受けやすい</b>という考え方があり、それを花にたとえた名前です。</p>

    <h2>結果の3つのタイプ</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>このテストの点（12〜48）</th></tr>
    <tr><td>🌷 蘭（オーキッド）タイプ</td><td>37点以上</td></tr>
    <tr><td>🌼 チューリップタイプ</td><td>26〜36点</td></tr>
    <tr><td>🌻 タンポポタイプ</td><td>25点以下</td></tr>
    </table>
    </div>
    <p>点の区切りは、このページで決めた目安です。研究のグループ分けとは、計算のしかたがちがいます。</p>
""",
    "faq": [
        ("このテストでHSPかどうか分かりますか？", "いいえ。遊びのためのセルフテストで、診断ではありません。HSPは病気の名前でも正式な診断名でもありません。"),
        ("繊細さは悪いことですか？", "いいえ。研究では、繊細な人はまわりの環境のよい面からも強く影響を受けやすいと考えられています。"),
        ("つらくて生活に困っています。", "気分の落ちこみや不安が続き、生活に困っているときは、ひとりで抱えずに医療機関や相談窓口に相談してください。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Aron EN, Aron A (1997). Sensory-processing sensitivity and its relation to introversion and emotionality. <i>Journal of Personality and Social Psychology</i>, 73(2), 345–368.",
        "Lionetti F, Aron A, Aron EN, ほか (2018). Dandelions, tulips and orchids: evidence for the existence of low-sensitive, medium-sensitive and high-sensitive individuals. <i>Translational Psychiatry</i>, 8, 24.",
        "Greven CU, Lionetti F, Booth C, ほか (2019). Sensory Processing Sensitivity in the context of Environmental Sensitivity: A critical review and development of research agenda. <i>Neuroscience &amp; Biobehavioral Reviews</i>, 98, 287–305.",
    ],
    "related": [("mimi-nenrei", "👂", "耳年齢テスト（聞こえる高い音は？）"), ("akubi-test", "🥱", "あくびがうつる？テスト"), ("shinpaku-kankaku", "💓", "心臓の音が分かる？テスト"), ("torihada-test", "🎵", "音楽で鳥肌が立つ？テスト")],
}
