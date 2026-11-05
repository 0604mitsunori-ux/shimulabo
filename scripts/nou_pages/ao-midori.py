# -*- coding: utf-8 -*-
# 十人十脳 第14話「青と緑（色の分け方）」と連動（2026-11-05 新規）
PAGE = {
    "slug": "ao-midori",
    "title": "青と緑の境目テスト｜この色は青？緑？あなたの「青」はどこまで？信号が青と呼ばれる理由も｜シミュラボ",
    "desc": "青から緑へ少しずつ変わる12色。あなたはどこから「緑」と呼びますか？色の境目は人によってちがいます。信号の緑を「青」と呼ぶ日本語の不思議と、日本語の色の名前を57人で調べた研究も解説。診断ではありません。",
    "og_title": "この色は青？緑？｜青と緑の境目テスト",
    "og_desc": "青から緑へ少しずつ変わる色。あなたの「青」はどこまで？",
    "ld_name": "青と緑の境目テスト（あなたの青はどこまで？）",
    "h1": "青と緑の境目テスト（この色は、青？緑？）",
    "lead": "信号の「青」は、よく見ると緑色です。でも日本語では「青信号」と呼びます。青と緑の境目は、言葉によっても、人によってもちがいます。1色ずつ出る色を、「青」か「緑」かで答えてください。12問、約1分です。",
    "start_h2": "🟦🟩 この色は、青？緑？",
    "start_text": "色が1つずつ、順番をばらばらにして出ます。深く考えず、パッと見て「青」か「緑」かを選んでください。",
    "tag": "青と緑",
    "card_label": "青と緑の境目テストの結果",
    "card_footer": "あなたの「青」はどこまで？ → shimulabo.com",
    "stage_html": """
      <div class="syn-top"><span>この色は？</span><span id="count">1 / 12</span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div id="sw" style="height:180px;border-radius:16px;margin:10px auto 14px;max-width:360px;"></div>
      <div class="syn-btns" id="opts"><button type="button" data-v="ao">青</button><button type="button" data-v="mi">緑</button></div>
      <p class="syn-note">※ 画面の色の設定（夜の画面など）で見え方が変わります。</p>
    """,
    "js": r"""
  const $ = NOU.$;
  // 青（色相220°）から緑（色相140°）まで12段階。明るさとあざやかさはそろえる
  const H = Array.from({ length: 12 }, (_, i) => Math.round(220 - i * (80 / 11)));
  const col = h => `hsl(${h},62%,46%)`;
  let order = [], k = 0, ans = {};
  function show() { $('sw').style.background = col(H[order[k]]); $('count').textContent = (k + 1) + ' / 12'; $('bar').style.width = (k / 12 * 100) + '%'; }
  $('opts').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; ans[order[k]] = b.dataset.v; k++; if (k < 12) show(); else done(); });
  function done() {
    const nAo = Object.values(ans).filter(v => v === 'ao').length;       // 「青」と答えた数＝青の広さ
    const T = nAo >= 8 ? ['🟦', '青が広いタイプ', '緑に近い色まで「青」と呼びました。日本語の「青信号」の感覚に近いのかもしれません。']
            : nAo <= 4 ? ['🟩', '緑が広いタイプ', '青に近い色まで「緑」と呼びました。']
            : ['⚖️', 'まん中で分けるタイプ', '青と緑を、ほぼまん中で分けました。'];
    const row = H.map((h, i) => `<span style="display:inline-block;width:8.33%;height:36px;background:${col(h)};position:relative;"><b style="position:absolute;left:0;right:0;bottom:-20px;text-align:center;font-size:11px;color:var(--ink-2)">${ans[i] === 'ao' ? '青' : '緑'}</b></span>`).join('');
    NOU.finish({
      label: '12色のうち「青」と呼んだ数', big: nAo, unit: ' / 12 色', emoji: T[0], typeName: T[1], advice: T[2],
      extraHTML: `<div style="display:flex;border-radius:8px;overflow:visible;margin:8px 0 26px;">${row}</div><p style="font-size:12px;color:var(--ink-3);">左ほど青、右ほど緑に近い色です。あなたの答えを下に書いています。</p>`,
      share: `青と緑の境目テストやってみた🟦🟩 12色中${nAo}色を「青」と呼んで「${T[1]}」でした。あなたの「青」はどこまで？`,
      cardTitle: 'わたしの「青」と「緑」の境目', cardLine: `12色中 ${nAo}色 が「青」`,
      draw: (x, R) => {
        const cw = R.w / 12, y = R.y + 160;
        H.forEach((h, i) => { x.fillStyle = col(h); x.fillRect(R.x + i * cw, y, cw + 1, 220);
          x.fillStyle = '#EEEAE3'; x.textAlign = 'center'; x.font = '900 38px ' + R.F; x.fillText(ans[i] === 'ao' ? '青' : '緑', R.x + i * cw + cw / 2, y + 290); });
        x.font = '800 34px ' + R.F; x.fillStyle = '#EEEAE3'; x.textAlign = 'left'; x.fillText('← 青に近い', R.x, y - 40); x.textAlign = 'right'; x.fillText('緑に近い →', R.x + R.w, y - 40);
      },
    });
  }
  function start() { order = Array.from({ length: 12 }, (_, i) => i).sort(() => Math.random() - .5); k = 0; ans = {}; NOU.startPanels(); show(); }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "青から緑へ少しずつ変わる12色を、順番をばらばらにして1色ずつ見て、「青」か「緑」かを答えるセルフテストです。",
    "article": """
    <h2>信号の緑を、なぜ「青」と呼ぶ？</h2>
    <p>日本語の「青」は、昔は今よりも広い色をさしていて、緑っぽいものも「青」と呼ぶことがありました。その名残で、今でも<b>木の葉、信号、銅のさび</b>など、緑色のものを「青」と呼ぶことがあります（栗木ほかの研究グループの2016年の発表）。「青りんご」「青菜」もそうです。</p>

    <h2>今の日本語の「青」と「緑」</h2>
    <p>日本語を話す57人に、330枚の色見本に名前を付けてもらった研究があります（Kuriki ほか 2017）。</p>
    <ul>
      <li>日本語の色の名前は、統計で分けると<b>16のまとまり</b>になった</li>
      <li>「青」は、いまも一部の緑のものに使われる一方、ふつうは<b>青い色だけ</b>をさしていた</li>
      <li>「緑」は、いつも緑の色だけをさしていた</li>
      <li>「水色」は<b>98%の人</b>が使っていて、日本語の基本の色の名前に加わりそうだった</li>
    </ul>
    <p>つまり今の日本語は、英語と同じように「青」と「緑」を分けている言葉です。それでも、どこで分けるかの境目は、人によって少しずつちがいます。</p>

    <h2>このテストのしくみ</h2>
    <p>このページでは、青（色相220度）から緑（色相140度）までを12段階に分け、明るさとあざやかさはそろえています。順番をばらばらにして出すので、前の答えに引っぱられにくくしています。「青」と答えた数が多いほど、あなたの「青」の範囲が広いということです。</p>
    <p>画面の色の設定でも見え方は変わります。同じ画面で、家族や友だちとくらべると、境目のちがいが分かります。</p>

    <h2>結果の3つのタイプ</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>12色中「青」と呼んだ数</th></tr>
    <tr><td>🟦 青が広いタイプ</td><td>8色以上</td></tr>
    <tr><td>⚖️ まん中で分けるタイプ</td><td>5〜7色</td></tr>
    <tr><td>🟩 緑が広いタイプ</td><td>4色以下</td></tr>
    </table>
    </div>
""",
    "faq": [
        ("正解の境目はありますか？", "ありません。色の名前の境目は、言葉や人によってちがいます。このテストは、あなたの境目を知るためのものです。"),
        ("色覚の検査になりますか？", "いいえ。遊びのためのセルフテストで、検査や診断ではありません。色の見え方が気になる人は、眼科で検査を受けられます。"),
        ("画面によって結果が変わりますか？", "変わります。夜の画面の設定や、ブルーライトを減らす設定をオフにして試すのがおすすめです。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Kuriki I, Lange R, Muto Y, ほか (2017). The modern Japanese color lexicon. <i>Journal of Vision</i>, 17(3):1.",
        "Kuriki I, ほか (2016). Study of the Japanese color lexicon using cluster analysis. <i>Journal of Vision</i>（Vision Sciences Society 2016 発表要旨）.",
    ],
    "related": [("shikikaku-test", "🎨", "色覚テスト（あなたの目は何色型？）"), ("dress-iro", "👗", "ドレスの色テスト（白と金？青と黒？）"), ("kyokankaku-test", "🔤", "共感覚テスト（文字に色が見える？）"), ("color-test", "🌈", "色当てゲーム")],
}
