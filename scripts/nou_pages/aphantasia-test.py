# -*- coding: utf-8 -*-
# 十人十脳 第3話「頭の中の映像（アファンタジア）」と連動（2026-11-05 新規）
PAGE = {
    "slug": "aphantasia-test",
    "title": "アファンタジア診断テスト｜目を閉じて、りんごは見える？頭の中の映像の濃さを試す｜シミュラボ",
    "desc": "目を閉じて、赤いりんごを思い浮かべてください。見えますか？頭の中に映像が浮かばない「アファンタジア」は、およそ25人に1人と報告されています。8つの場面を思い浮かべて、あなたの頭の中の映像の濃さを試すセルフテスト。診断ではありません。",
    "og_title": "目を閉じて、りんごは見える？｜アファンタジア テスト",
    "og_desc": "頭の中に映像が浮かばない人は、およそ25人に1人。あなたの頭の中の映像の濃さは？",
    "ld_name": "アファンタジア テスト（頭の中の映像の濃さ）",
    "h1": "アファンタジア テスト（目を閉じて、りんごは見える？）",
    "lead": "目を閉じて、赤いりんごを1つ思い浮かべてください。つやや形まで「見えて」いますか？それとも「りんごだと分かる」だけですか？頭の中に映像が浮かぶかどうかは、人によって大きくちがいます。8つの場面で試してみましょう。約2分です。",
    "start_h2": "🍎 8つの場面を、目を閉じて思い浮かべてね",
    "start_text": "場面が1つずつ出ます。読んだら目を閉じて思い浮かべ、どのくらいはっきり「見えた」かを5段階で選んでください。正解はありません。",
    "tag": "アファンタジア",
    "card_label": "アファンタジア テストの結果",
    "card_footer": "目を閉じて、りんごは見える？ → shimulabo.com",
    "stage_html": """
      <div class="syn-top"><span>目を閉じて、思い浮かべてね</span><span id="count">1 / 8</span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div class="syn-big" id="emoji" style="font-size:72px;"></div>
      <div class="syn-ask" id="scene" style="font-size:19px;font-weight:700;color:#EEEAE3;"></div>
      <div class="syn-ask" style="font-size:13px;">どのくらいはっきり「見えた」？</div>
      <div class="syn-btns c1" id="opts"></div>
    """,
    "js": r"""
  const $ = NOU.$;
  const SC = [['🍎', '赤いりんごが1つ、机の上にある'], ['👤', 'よく知っている人の顔（家族や友だち）'], ['🌅', '朝日が、海の向こうから昇ってくる'], ['🚪', '自分の部屋のドアを開けたときの景色'],
              ['☔', '雨の日の、人の多い交差点'], ['🐕', '走っている犬（毛の色と動き）'], ['🏪', 'よく行くお店の入口と看板'], ['🎆', '夜空に花火が上がって、ぱっと開く']];
  const LV = [['本物を見ているように、はっきり', 5], ['かなりはっきり', 4], ['ある程度はっきり', 3], ['ぼんやり、かすかに', 2], ['何も浮かばない（考えとして分かるだけ）', 1]];
  let k = 0, ans = [];
  $('opts').innerHTML = LV.map(([t, v]) => `<button type="button" data-v="${v}">${t}</button>`).join('');
  function show() { $('emoji').textContent = SC[k][0]; $('scene').textContent = SC[k][1]; $('count').textContent = (k + 1) + ' / 8'; $('bar').style.width = (k / 8 * 100) + '%'; }
  $('opts').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; ans.push(+b.dataset.v); k++; if (k < 8) show(); else done(); });
  function done() {
    const sum = ans.reduce((a, b) => a + b, 0), avg = sum / 8;
    const T = avg <= 1.5 ? ['🌑', '映像が浮かびにくいタイプ', 'ほとんどの場面で、映像は浮かびませんでした。研究で「アファンタジア」と呼ばれる人の答え方に近いかもしれません。映像がなくても、考えたり覚えたりはできます。']
            : avg <= 2.5 ? ['🌘', 'ぼんやり浮かぶタイプ', '映像は、かすかに・ぼんやり浮かびました。言葉や知識で思い出していることが多いのかもしれません。']
            : avg < 4 ? ['🌓', 'ふつうに浮かぶタイプ', 'ある程度はっきり浮かびました。多くの人はこのあたりです。']
            : avg < 4.6 ? ['🌕', 'はっきり浮かぶタイプ', 'かなりはっきり浮かびました。思い出す場面を、目で見るように使っているのかもしれません。']
            : ['✨', '本物のように浮かぶタイプ', 'ほとんどの場面が、本物を見ているようにはっきり浮かびました。研究で「ハイパーファンタジア」と呼ばれる人の答え方に近いかもしれません。'];
    const rows = SC.map((s, i) => `<div><span class="k">${s[0]} ${s[1]}</span><span class="syn-meter"><i style="width:${ans[i] * 20}%"></i></span><span class="v">${ans[i]}</span></div>`).join('');
    NOU.finish({
      label: '8つの場面の、映像の濃さ（8〜40点）', big: sum, unit: ' / 40 点', emoji: T[0], typeName: T[1], advice: T[2],
      extraHTML: `<div class="syn-rows">${rows}</div><p style="font-size:12px;color:var(--ink-3);">タイプの分け方はこのページの目安です。研究で使われる質問票（16問）とは問題も点数もちがいます。</p>`,
      share: `アファンタジア テストやってみた🍎 頭の中の映像の濃さは ${sum}/40点で「${T[1]}」でした。目を閉じて、りんごは見える？`,
      cardTitle: 'わたしの頭の中の映像', cardLine: `映像の濃さ ${sum} / 40 点`,
      draw: (x, r) => {
        SC.forEach((s, i) => {
          const y = r.y + 30 + i * 66, bw = r.w - 160;
          x.textAlign = 'left'; x.font = '400 40px ' + r.F; x.fillText(s[0], r.x, y + 40);
          x.fillStyle = '#2A3C43'; x.beginPath(); x.roundRect(r.x + 80, y + 10, bw, 40, 20); x.fill();
          const g = x.createLinearGradient(r.x + 80, 0, r.x + 80 + bw, 0); g.addColorStop(0, '#4FC6B4'); g.addColorStop(1, '#F5BB5C');
          x.fillStyle = g; x.globalAlpha = 0.25 + ans[i] * 0.15; x.beginPath(); x.roundRect(r.x + 80, y + 10, bw * ans[i] / 5, 40, 20); x.fill(); x.globalAlpha = 1;
          x.fillStyle = '#EEEAE3'; x.textAlign = 'right'; x.font = '900 36px ' + r.F; x.fillText(ans[i], r.x + r.w, y + 42);
        });
      },
    });
  }
  function start() { k = 0; ans = []; NOU.startPanels(); show(); }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "8つの場面を思い浮かべて、頭の中の映像がどのくらいはっきりしているかを5段階で答えるセルフテストです。研究で使われる「頭の中の映像の鮮明さ」の質問票の考え方をもとにしていますが、問題はこのページで作ったものです。",
    "article": """
    <h2>アファンタジアとは</h2>
    <p>目を閉じて何かを思い浮かべても、映像がまったく、またはほとんど浮かばないことを「アファンタジア」と呼びます。2015年にイギリスの研究者が名前をつけました（Zeman ほか 2015）。反対に、本物のようにはっきり浮かぶことは「ハイパーファンタジア」と呼ばれます（Zeman ほか 2020）。</p>

    <h2>どれくらいの人にある？</h2>
    <p>1,000人以上を調べた研究では、<b>3.9%</b>の人がアファンタジアにあてはまりました。<b>およそ25人に1人</b>です。男女の差はありませんでした（Dance ほか 2022）。この研究では、1973年に作られた「頭の中の映像の鮮明さ」の質問票（Marks 1973）が使われています。</p>

    <h2>体の反応でも、ちがいが分かる</h2>
    <p>明るいものを見ると、瞳（ひとみ）は小さくなります。実は、明るいものを<b>思い浮かべただけ</b>でも、瞳が小さくなる人がいます。オーストラリアの研究では、アファンタジアの人ではこの「思い浮かべたときの反応」が見られませんでした。実際に明るいものを見たときは、ほかの人と同じように反応しました（Kay ほか 2022）。頭の中の映像のちがいは、本人の感じ方だけでなく、体の反応にも出ていたのです。</p>

    <h2>浮かばない人・浮かぶ人の、それぞれの特徴</h2>
    <p>アファンタジアの2,000人と、ハイパーファンタジアの200人に質問した研究では、次のような傾向が報告されています（Zeman ほか 2020）。</p>
    <ul>
      <li>アファンタジアの人は、理科や数学に関わる仕事の人が多く、ハイパーファンタジアの人は、ものを作る仕事の人が多い</li>
      <li>アファンタジアの人は、人の顔を覚えることや、自分の思い出を思い出すことが苦手だと答える人が多め</li>
      <li>アファンタジアの人のおよそ半分は、音や味なども含めて、どの感覚でも思い浮かべられない</li>
      <li>それでも、多くの人は<b>夢の中では映像を見る</b></li>
      <li>家族の中で、たまたまより多く見られる</li>
      <li>ハイパーファンタジアの人には、<a href="../kyokankaku-test/">共感覚</a>（文字に色が見えるなど）の人が多め</li>
    </ul>

    <h2>結果の5つのタイプ</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>平均（1〜5）</th></tr>
    <tr><td>🌑 映像が浮かびにくいタイプ</td><td>1.5以下</td></tr>
    <tr><td>🌘 ぼんやり浮かぶタイプ</td><td>1.5〜2.5</td></tr>
    <tr><td>🌓 ふつうに浮かぶタイプ</td><td>2.5〜4.0</td></tr>
    <tr><td>🌕 はっきり浮かぶタイプ</td><td>4.0〜4.6</td></tr>
    <tr><td>✨ 本物のように浮かぶタイプ</td><td>4.6以上</td></tr>
    </table>
    </div>
    <p>どのタイプが良い・悪いということはありません。思い浮かべ方がちがうだけで、考えることも覚えることもできます。家族や友だちと答えを比べると、同じ「りんご」でも頭の中がまったくちがうことに驚くはずです。</p>
""",
    "faq": [
        ("このテストでアファンタジアかどうか分かりますか？", "いいえ。研究の質問票の考え方をもとにした遊びのためのセルフテストで、検査や診断ではありません。問題も点数の分け方もこのページで作ったものです。"),
        ("映像が浮かばないのは、おかしいことですか？", "研究者は、人による「ちがい」の1つとして調べています（Zeman ほか 2020）。浮かばなくても、考えたり、覚えたり、夢を見たりはできます。"),
        ("どれくらいの人が、映像が浮かばないのですか？", "1,000人以上を調べた研究では3.9%、およそ25人に1人でした（Dance ほか 2022）。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Zeman A, Dewar M, Della Sala S (2015). Lives without imagery – Congenital aphantasia. <i>Cortex</i>, 73, 378–380.",
        "Zeman A, Milton F, Della Sala S, ほか (2020). Phantasia – The psychological significance of lifelong visual imagery vividness extremes. <i>Cortex</i>, 130, 426–440.",
        "Dance CJ, Ipser A, Simner J (2022). The prevalence of aphantasia (imagery weakness) in the general population. <i>Consciousness and Cognition</i>, 97, 103243.",
        "Kay L, Keogh R, Andrillon T, Pearson J (2022). The pupillary light response as a physiological index of aphantasia, sensory and phenomenological imagery strength. <i>eLife</i>, 11, e72484.",
        "Marks DF (1973). Visual imagery differences in the recall of pictures. <i>British Journal of Psychology</i>, 64(1), 17–24.",
    ],
    "related": [("naigen-test", "💬", "頭の中の声テスト"), ("kyokankaku-test", "🔤", "共感覚テスト（文字に色が見える？）"), ("shikikaku-test", "🎨", "色覚テスト（あなたの目は何色型？）"), ("mimi-nenrei", "👂", "耳年齢テスト（モスキート音）")],
}
