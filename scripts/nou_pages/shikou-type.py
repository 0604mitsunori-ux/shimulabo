# -*- coding: utf-8 -*-
# 十人十脳 第18話「絵で考える人・言葉で考える人」と連動（2026-11-05 新規）
PAGE = {
    "slug": "shikou-type",
    "title": "考え方のタイプ診断｜絵で考える人・図で考える人・言葉で考える人、あなたはどれ？｜シミュラボ",
    "desc": "頭の中で、あなたは「絵」で考える？「言葉」で考える？12の質問で、色や形を思い浮かべる「絵のタイプ」、しくみや位置で考える「図のタイプ」、言葉で考える「言葉のタイプ」の3つのうち、どれが強いかを試すセルフテスト。画家と科学者で考え方がちがうと分かった研究も解説。診断ではありません。",
    "og_title": "絵で考える？言葉で考える？｜考え方のタイプ診断",
    "og_desc": "12の質問で、あなたの頭の中の考え方のタイプを3つに分けて。",
    "ld_name": "考え方のタイプ診断（絵・図・言葉）",
    "h1": "考え方のタイプ診断（絵で考える人・言葉で考える人）",
    "lead": "道を説明するとき、頭の中に景色が浮かぶ人もいれば、「2つ目の角を右」と言葉で考える人もいます。研究では、頭の中の考え方には大きく3つのタイプがあると考えられています。12の質問に答えてください。約2分です。",
    "start_h2": "🧠 12の質問に答えてね",
    "start_text": "ふだんの自分に、どのくらいあてはまるかを選んでください。正解はありません。",
    "tag": "考え方",
    "card_label": "考え方のタイプ診断の結果",
    "card_footer": "絵で考える？言葉で考える？ → shimulabo.com",
    "stage_html": """
      <div class="syn-top"><span>ふだんの自分は？</span><span id="count">1 / 12</span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div class="syn-big" id="em" style="font-size:56px;"></div>
      <div class="syn-ask" id="q" style="font-size:18px;font-weight:700;color:#EEEAE3;min-height:3.4em;line-height:1.7;"></div>
      <div class="syn-btns c1" id="opts"></div>
    """,
    "js": r"""
  const $ = NOU.$;
  // 3つのタイプ×4問（研究で言われる3つの考え方のタイプをもとに、このページで作った問題）
  const TY = [['🎨', '絵のタイプ', '色・形・見た目をくわしく思い浮かべて考える'], ['📐', '図のタイプ', 'しくみ・位置・動きを図のように考える'], ['💬', '言葉のタイプ', '言葉や文で、順を追って考える']];
  const Q = [
    [0, '昔の思い出は、写真のように色まで思い浮かぶ'], [1, '家具の配置がえは、頭の中で動かしてから決める'], [2, '考えごとは、頭の中で文にして考えている'],
    [0, '人の服や髪型を、あとからくわしく思い出せる'], [1, '機械やしかけが、どう動いているのか気になる'], [2, '本を読むほうが、図を見るより分かりやすい'],
    [0, '絵をかいたり、写真をとったりするのが好き'], [1, '地図や図表を見ると、すぐに全体がつかめる'], [2, '人に説明するとき、ぴったりの言葉がすぐ出てくる'],
    [0, '料理の写真を見ると、味やにおいまで浮かぶ'], [1, '立体のパズルや組み立てが得意'], [2, '日記や文章を書くと、気持ちが整理できる'],
  ];
  const O = [['とてもあてはまる', 4], ['ややあてはまる', 3], ['あまりあてはまらない', 2], ['まったくあてはまらない', 1]];
  let k = 0, sc = [0, 0, 0];
  function show() { const [t, q] = Q[k]; $('em').textContent = TY[t][0]; $('q').textContent = q; $('count').textContent = (k + 1) + ' / 12'; $('bar').style.width = (k / 12 * 100) + '%';
    $('opts').innerHTML = O.map(([s, v]) => `<button type="button" data-v="${v}">${s}</button>`).join(''); }
  $('opts').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; sc[Q[k][0]] += +b.dataset.v; k++; if (k < 12) show(); else done(); });
  function done() {
    const mx = Math.max(...sc), tops = [0, 1, 2].filter(i => sc[i] === mx), t = tops[0];
    const ADV = ['色や形をくわしく思い浮かべるのが得意なタイプです。研究では、画家などの美術の仕事の人に多いタイプでした。', 'ものの位置やしくみを図のように考えるのが得意なタイプです。研究では、科学者や技術者に多いタイプでした。', '言葉で順を追って考えるのが得意なタイプです。考えを文にして、人に伝えるのが上手かもしれません。'];
    const name = tops.length > 1 ? tops.map(i => TY[i][1].replace('のタイプ', '')).join('と') + 'の両方タイプ' : TY[t][1];
    const rows = TY.map(([e, n, d], i) => `<div style="margin:6px 0;"><div style="display:flex;justify-content:space-between;font-size:13px;"><span>${e} ${n}<small style="color:var(--ink-3);">（${d}）</small></span><b>${sc[i]} / 16</b></div><div style="height:10px;border-radius:5px;background:var(--line,#e5e1da);"><i style="display:block;height:100%;width:${(sc[i] - 4) / 12 * 100}%;border-radius:5px;background:#4FC6B4;"></i></div></div>`).join('');
    NOU.finish({
      label: 'いちばん強い考え方', big: TY[t][0], unit: '', emoji: TY[t][0], typeName: name, advice: tops.length > 1 ? '2つ以上のタイプが同じくらい強く出ました。場面によって考え方を使い分けているのかもしれません。' : ADV[t],
      extraHTML: rows + `<p style="font-size:12px;color:var(--ink-3);">3つのタイプは、どれがよい・悪いではありません。多くの人は、3つを少しずつ持っています。</p>`,
      share: `考え方のタイプ診断やってみた🧠 「${name}」でした（絵${sc[0]}・図${sc[1]}・言葉${sc[2]}）。あなたは絵で考える？言葉で考える？`,
      cardTitle: 'わたしの頭の中の考え方', cardLine: `絵 ${sc[0]}・図 ${sc[1]}・言葉 ${sc[2]}（各16点）`,
      draw: (x, R) => {
        const cw = (R.w - 2 * 40) / 3;
        TY.forEach(([e, n], i) => { const xx = R.x + i * (cw + 40), hMax = 360, h = 30 + (sc[i] - 4) / 12 * (hMax - 30), base = R.y + 470;
          x.fillStyle = '#2A3C43'; x.beginPath(); x.roundRect(xx, base - hMax, cw, hMax, 24); x.fill();
          x.fillStyle = tops.includes(i) ? '#F5BB5C' : '#4FC6B4'; x.beginPath(); x.roundRect(xx, base - h, cw, h, 24); x.fill();
          x.textAlign = 'center'; x.fillStyle = '#EEEAE3'; x.font = '400 72px ' + R.F; x.fillText(e, xx + cw / 2, R.y + 70);
          x.font = '800 36px ' + R.F; x.fillText(n, xx + cw / 2, base + 50); });
      },
    });
  }
  function start() { k = 0; sc = [0, 0, 0]; NOU.startPanels(); show(); }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "色や形を思い浮かべる「絵のタイプ」、しくみや位置で考える「図のタイプ」、言葉で考える「言葉のタイプ」について4問ずつ、合わせて12問に答えるセルフテストです。問題は、研究で言われる3つのタイプの考え方をもとに、このページで作っています。",
    "article": """
    <h2>「絵で考える人」は2種類いる</h2>
    <p>昔は、人の考え方は「絵で考える人」と「言葉で考える人」の2つに分けられると考えられていました。ところが、絵で考える人を調べると、さらに<b>2つのタイプ</b>に分かれることが分かってきました（Kozhevnikov ほか 2005）。</p>
    <ul>
      <li>🎨 <b>絵のタイプ</b>：ものの色・形・見た目を、くわしく思い浮かべるのが得意</li>
      <li>📐 <b>図のタイプ</b>：ものの位置・しくみ・動きを、図のように考えるのが得意</li>
    </ul>
    <p>この研究では、<b>画家などの美術の人は「絵のタイプ」</b>の力が高く、<b>科学者や技術者は「図のタイプ」</b>の力が高いという結果でした。同じ「頭の中で見る」でも、見ているものがちがうのです。</p>

    <h2>3つの考え方のタイプ</h2>
    <p>その後、「絵」「図」「言葉」の3つのタイプを測る質問票が作られました（Blazhenkova・Kozhevnikov 2009）。この質問票は、いろいろな国の言葉に訳されて研究に使われています。</p>
    <p>このページの12問は、その3つのタイプの考え方をもとに作った簡単なものです。研究の質問票そのものではありません。</p>

    <h2>頭の中に絵が浮かばない人も</h2>
    <p>頭の中にまったく絵が浮かばない人もいて、「アファンタジア」と呼ばれています。そうした人でも、言葉や図の考え方で、ふつうに暮らしたり仕事をしたりしています。考え方のタイプは、どれがすぐれているというものではありません。</p>
    <p>頭の中にどのくらいはっきり絵が浮かぶかは、<a href="../aphantasia-test/">アファンタジア診断テスト</a>で試せます。</p>

    <h2>結果の見方</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>得意なこと</th></tr>
    <tr><td>🎨 絵のタイプ</td><td>色・形・見た目を思い浮かべる</td></tr>
    <tr><td>📐 図のタイプ</td><td>位置・しくみ・動きを考える</td></tr>
    <tr><td>💬 言葉のタイプ</td><td>言葉で順を追って考える</td></tr>
    </table>
    </div>
    <p>3つのうち、いちばん点が高かったものがあなたのタイプです。同じ点のときは「両方タイプ」と出ます。</p>
""",
    "faq": [
        ("どのタイプがいちばん頭がいいですか？", "どれがすぐれているということはありません。得意なことがちがうだけです。"),
        ("タイプは変わりますか？", "経験や仕事、練習によって変わることもあると考えられています。ときどき試してみるのもおすすめです。"),
        ("研究の質問票と同じですか？", "いいえ。このページの12問は、研究で言われる3つのタイプの考え方をもとに作った簡単なもので、研究の質問票そのものではありません。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Kozhevnikov M, Kosslyn S, Shephard J (2005). Spatial versus object visualizers: A new characterization of visual cognitive style. <i>Memory &amp; Cognition</i>, 33(4), 710–726.",
        "Blazhenkova O, Kozhevnikov M (2009). The new object-spatial-verbal cognitive style model: Theory and measurement. <i>Applied Cognitive Psychology</i>, 23(5), 638–663.",
    ],
    "related": [("aphantasia-test", "🌫️", "アファンタジア診断テスト"), ("naigen-test", "🗣️", "頭の中の声テスト（内言）"), ("houkou-kankaku", "🧭", "方向感覚テスト（頭の中で図形を回せる？）"), ("hidarikiki", "✋", "利き手・利き目・利き足チェック")],
}
