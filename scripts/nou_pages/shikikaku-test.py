# -*- coding: utf-8 -*-
# 十人十脳 第2話「4色型色覚」と連動。既存の「色の識別テスト」を同じURLのまま作り直した（2026-11-05）
PAGE = {
    "slug": "shikikaku-test",
    "title": "色覚テスト｜あなたの目は何色型？4色型・3色型と色の見分け方を試す｜シミュラボ",
    "desc": "あなたの目は何色型？16枚の色の中から1枚だけ違う色を探す、約3分の色覚セルフテスト。赤〜緑と青〜黄の2つの向きで、どこまで細かく見分けられるかが分かります。4色型の研究や、年齢で変わる見分け方も解説。診断ではありません。",
    "og_title": "あなたの目は、何色型？｜色覚テスト",
    "og_desc": "16枚の中から1枚だけ違う色を探す。赤〜緑・青〜黄、どこまで見分けられる？",
    "ld_name": "色覚テスト（あなたの目は何色型？）",
    "h1": "色覚テスト（あなたの目は何色型？）",
    "lead": "人の目には、ふつう色を感じる細胞が3種類あります。でも、その見分け方の細かさは人によってちがいます。16枚の中から1枚だけちがう色を探してください。だんだん差が小さくなります。全部で20問、約3分です。",
    "start_h2": "🎨 1枚だけちがう色を探してね",
    "start_text": "1問につき10秒。赤〜緑の向きと、青〜黄の向きのちがいが、交互に10問ずつ出ます。画面の明るさは、ふだん使っている明るさのままでどうぞ。",
    "start_extra": "",
    "tag": "色覚テスト",
    "card_label": "色覚テストの結果",
    "card_footer": "あなたの目は何色型？ → shimulabo.com 色覚テスト",
    "stage_html": """
      <div class="syn-top"><span id="axisLabel">赤〜緑</span><span id="count">1 / 20</span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div class="syn-bar" style="height:4px;margin-top:0;"><i id="timer" style="background:#F5BB5C;width:100%;transition:none;"></i></div>
      <div class="syn-ask">1枚だけちがう色を押してね</div>
      <div id="grid" style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;max-width:420px;margin:0 auto;"></div>
      <p class="syn-note">※ 画面の明るさ・色の設定（夜の画面・ブルーライトを減らす設定など）で結果が変わります。</p>
    """,
    "css": "#grid button{aspect-ratio:1/1;border:0;border-radius:10px;cursor:pointer;}",
    "js": r"""
  const $ = NOU.$;
  // OKLab → sRGB（色の差を「人の見え方に近い物差し」でそろえるため）
  function oklab(L, a, b) {
    const l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3, m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3, s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3;
    const r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s, g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s, bb = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s;
    const t = v => { v = Math.max(0, Math.min(1, v)); return Math.round(255 * (v <= 0.0031308 ? 12.92 * v : 1.055 * Math.pow(v, 1 / 2.4) - 0.055)); };
    return `rgb(${t(r)},${t(g)},${t(bb)})`;
  }
  const N = 20, STEPS = [0.06, 0.05, 0.04, 0.032, 0.026, 0.021, 0.017, 0.014, 0.011, 0.009];
  let k = 0, odd = -1, ok = { rg: [], by: [] }, timer = 0, t0 = 0, cur = null;
  function round() {
    const axis = k % 2 === 0 ? 'rg' : 'by', step = STEPS[Math.floor(k / 2)];
    const L = 0.62 + Math.random() * 0.14, a = (Math.random() - 0.5) * 0.12, b = (Math.random() - 0.5) * 0.12, sg = Math.random() < 0.5 ? 1 : -1;
    const base = oklab(L, a, b); let s = step, diff;
    do { diff = axis === 'rg' ? oklab(L, a + sg * s, b) : oklab(L, a, b + sg * s); s *= 1.15; } while (diff === base);   // 画面の色の段階で同じ色に丸まったら、少しだけ差を広げる
    odd = Math.floor(Math.random() * 16); cur = axis;
    $('grid').innerHTML = Array.from({ length: 16 }, (_, i) => `<button type="button" data-i="${i}" aria-label="色${i + 1}" style="background:${i === odd ? diff : base}"></button>`).join('');
    $('axisLabel').textContent = axis === 'rg' ? '赤〜緑のちがい' : '青〜黄のちがい';
    $('count').textContent = (k + 1) + ' / ' + N; $('bar').style.width = (k / N * 100) + '%';
    t0 = performance.now(); clearInterval(timer);
    timer = setInterval(() => { const p = 1 - (performance.now() - t0) / 10000; $('timer').style.width = Math.max(0, p * 100) + '%'; if (p <= 0) answer(-1); }, 100);
  }
  function answer(i) {
    clearInterval(timer); ok[cur].push(i === odd); k++;
    if (k < N) round(); else done();
  }
  function done() {
    const rg = ok.rg.filter(Boolean).length, by = ok.by.filter(Boolean).length, total = rg + by;
    const T = total >= 17 ? ['🦋', '細かい色まで見分けるタイプ', 'ほとんどの問題で、ごく小さな色の差まで見分けました。画面の性能の限界に近い差まで見えています。']
            : total >= 11 ? ['🌈', 'ふつうに見分けるタイプ', '大きな差はしっかり見分けて、小さな差で迷いました。多くの人はこのあたりです。']
            : ['🎨', 'ざっくり見分けるタイプ', '小さな差になると、見分けにくくなりました。画面の明るさや、見ている場所の光でも結果は変わります。'];
    let extra = '';
    if (Math.abs(rg - by) >= 4) extra = `<div class="alert" style="text-align:left;">🔍 ${rg < by ? '赤〜緑' : '青〜黄'}の向きのほうが、見分けにくかったようです。画面の設定でも変わるので、気になるときは別の画面でもう一度。色の見え方が気になる人は、眼科で検査を受けられます。</div>`;
    NOU.finish({
      label: '20問中、見分けられた数', big: total, unit: ' / 20 問', emoji: T[0], typeName: T[1], advice: T[2],
      extraHTML: extra + `<div class="syn-rows"><div><span class="k">赤〜緑のちがい</span><span class="syn-meter"><i style="width:${rg * 10}%"></i></span><span class="v">${rg} / 10</span></div><div><span class="k">青〜黄のちがい</span><span class="syn-meter"><i style="width:${by * 10}%"></i></span><span class="v">${by} / 10</span></div></div>`,
      share: `色覚テストやってみた🎨 赤〜緑 ${rg}/10・青〜黄 ${by}/10 で「${T[1]}」でした。あなたの目は何色型？`,
      cardTitle: 'わたしの色の見分け方', cardLine: `20問中 ${total}問 見分けられた`,
      draw: (x, r) => {
        [['赤〜緑', ok.rg, ['#E5484D', '#3DAA6A']], ['青〜黄', ok.by, ['#3B6FD8', '#F5D547']]].forEach(([name, arr, cols], row) => {
          const y = r.y + 70 + row * 250;
          x.textAlign = 'left'; x.fillStyle = '#EEEAE3'; x.font = '800 40px ' + r.F; x.fillText(name, r.x, y);
          x.textAlign = 'right'; x.fillText(arr.filter(Boolean).length + ' / 10', r.x + r.w, y);
          const cw = (r.w - 9 * 14) / 10;
          arr.forEach((v, i) => {
            x.fillStyle = v ? cols[i % 2] : '#2A3C43'; x.beginPath(); x.roundRect(r.x + i * (cw + 14), y + 30, cw, 120, 14); x.fill();
            x.fillStyle = v ? '#0D1417' : '#8D9BA1'; x.textAlign = 'center'; x.font = '900 40px ' + r.F; x.fillText(v ? '○' : '×', r.x + i * (cw + 14) + cw / 2, y + 106);
          });
        });
      },
    });
  }
  $('grid').addEventListener('click', e => { const b = e.target.closest('button'); if (b) answer(+b.dataset.i); });
  function start() { k = 0; ok = { rg: [], by: [] }; NOU.startPanels(); round(); }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "16枚の色の中から1枚だけちがう色を探して、色の差をどこまで細かく見分けられるかを試すセルフテストです。研究で使われる色の検査と同じように、赤〜緑と青〜黄の2つの向きに分けて数えます。",
    "article": """
    <h2>「何色型」とは</h2>
    <p>目の奥（網膜）には、色を感じる細胞が並んでいます。多くの人はこの細胞が3種類あり、その組み合わせで色を見分けています。これを「3色型」と呼びます。</p>
    <p>細胞の種類が少ない人は「2色型」、4種類ある人は「4色型」と呼ばれます。同じ景色を見ていても、頭の中に届く色の数は人によってちがうかもしれない、ということです。</p>

    <h2>4色型の人は本当にいる？</h2>
    <p>イギリスの研究では、<b>女性のおよそ12%</b>が、軽い色覚のちがいを生む遺伝子を持っていて、目の中に4種類の細胞があるはずだとされています（Jordan ほか 2010）。</p>
    <p>ところが、実際に見分け方を詳しく調べると、そのほとんどの人は4色の見分け方をしていませんでした。全部のテストで4色型らしい見分け方をしたのは、<b>24人中1人</b>だけでした。「細胞が4種類ある」ことと「4色で見える」ことは、同じではないようです。</p>

    <h2>このテストで4色型かどうかは分かりません</h2>
    <p>スマホやパソコンの画面は、赤・緑・青の3つの光を混ぜて色を作っています。3色型の目で見分けられない差は、画面ではそもそも出せません。だから、画面のテストで「あなたは4色型です」と言うことはできません。</p>
    <p>このページで試しているのは、<b>3色の画面の中で、どこまで小さな色の差を見分けられるか</b>です。</p>

    <h2>2つの向きに分けて数える理由</h2>
    <p>色の見分け方を調べる研究では、「赤〜緑の向き」と「青〜黄の向き」に分けて点数を出すことがあります（Kinnear・Sahraie 2002 など）。このテストでも、問題を2つの向きに分けて、それぞれ10問ずつ数えています。</p>

    <h2>見分ける力は、年齢で変わる</h2>
    <p>5歳から70代まで382人を調べた研究では、色を見分ける力は年齢によって変わり、<b>19歳ごろがいちばん細かく</b>、そこから先はゆるやかに下がっていくU字の形になりました（Kinnear・Sahraie 2002）。家族や友だちと結果を比べると、ちがいが出るかもしれません。</p>

    <h2>結果の3つのタイプ</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>どんな結果？</th></tr>
    <tr><td>🦋 細かい色まで見分けるタイプ</td><td>20問中17問以上。ごく小さな差まで見分けた</td></tr>
    <tr><td>🌈 ふつうに見分けるタイプ</td><td>11〜16問。大きな差は見分け、小さな差で迷った</td></tr>
    <tr><td>🎨 ざっくり見分けるタイプ</td><td>10問以下。小さな差になると見分けにくかった</td></tr>
    </table>
    </div>
    <p>画面の明るさ、夜の画面の設定、部屋の光でも結果は大きく変わります。点数そのものより、「赤〜緑」と「青〜黄」のどちらが見分けやすかったかを、ほかの人と比べてみてください。</p>
""",
    "faq": [
        ("このテストで4色型かどうか分かりますか？", "いいえ。画面は赤・緑・青の3つの光で色を作っているので、4色型の人だけが見分けられる差は、画面では出せません。このテストは、画面の中での色の見分け方の細かさを試すものです。"),
        ("色覚の検査になりますか？", "いいえ。遊びのためのセルフテストで、検査や診断ではありません。色の見え方が気になる人は、眼科で検査を受けられます。"),
        ("やるたびに結果が変わります。", "色の組み合わせは毎回ランダムで、画面の明るさや部屋の光でも変わります。何回か試して、だいたいの傾向を見るのがおすすめです。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Jordan G, Deeb SS, Bosten JM, Mollon JD (2010). The dimensionality of color vision in carriers of anomalous trichromacy. <i>Journal of Vision</i>, 10(8):12.",
        "Kinnear PR, Sahraie A (2002). New Farnsworth-Munsell 100 hue test norms of normal observers for each year of age 5–22 and for age decades 30–70. <i>British Journal of Ophthalmology</i>, 86(12), 1408–1411.",
    ],
    "related": [("kyokankaku-test", "🔤", "共感覚テスト（文字に色が見える？）"), ("aphantasia-test", "🍎", "頭の中の映像テスト（アファンタジア）"), ("color-test", "🌈", "色当てゲーム"), ("stroop-test", "🧠", "ストループテスト")],
}
