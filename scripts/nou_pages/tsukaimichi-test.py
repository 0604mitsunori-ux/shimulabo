# -*- coding: utf-8 -*-
# 十人十脳 第22話「発想の数（IQと発想）」と連動（2026-11-08 新規）
PAGE = {
    "slug": "tsukaimichi-test",
    "title": "使い道テスト（発想力テスト）｜クリップの使い道、30秒でいくつ？｜シミュラボ",
    "desc": "クリップや新聞紙の使い道を、30秒でいくつ書けるかを試す発想力のセルフテスト。書いた数と「めずらしい使い道」の数から、たくさん型・ひねり型・あとから型が分かります。IQと発想のつながりは小さいという研究、IQ120の境目の研究、歩くと発想が増える研究も解説。診断ではありません。",
    "og_title": "クリップの使い道、30秒でいくつ？｜使い道テスト",
    "og_desc": "答えは1つじゃない。30秒で、ちがう方向にたくさん考える発想力テスト。",
    "ld_name": "使い道テスト（発想力テスト）",
    "h1": "使い道テスト（クリップの使い道、30秒でいくつ？）",
    "lead": "ある物の使い道を、<b>30秒で、できるだけたくさん</b>書いてください。ふつうの使い方でなくてもかまいません。正解はありません。2回くり返して、最後に「めずらしい」と思うものに印をつけます。約2分です。",
    "start_h2": "💡 使い道を、30秒でいくつ？",
    "start_text": "お題が出たら、1行に1つずつ使い道を書きます。30秒たつと次へ進みます（早めに終わってもOK）。",
    "tag": "発想力テスト",
    "card_label": "使い道テストの結果",
    "card_footer": "使い道、30秒でいくつ？ → shimulabo.com",
    "stage_html": """
      <div class="syn-top"><span id="part">お題</span><span id="count"></span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div class="syn-ask" id="q" style="font-size:22px;font-weight:800;color:#EEEAE3;"></div>
      <textarea id="ta" rows="7" style="width:100%;box-sizing:border-box;border-radius:10px;border:1px solid #2A3C43;background:#111c20;color:#EEEAE3;font:inherit;font-size:16px;padding:10px;" placeholder="1行に1つずつ書く"></textarea>
      <div id="checks" class="syn-rows" hidden></div>
      <button class="syn-go" id="goBtn" type="button">次へ</button>
    """,
    "js": r"""
  const $ = NOU.$;
  const ITEMS = [['📎', 'クリップ'], ['📰', '新聞紙'], ['🥫', '空き缶'], ['🧱', 'レンガ'], ['🥄', 'スプーン'], ['🧦', 'くつ下']];
  let round = 0, picks = [], answers = [], timer = null, left = 30, phase = 'write';
  function pickItems() { const a = ITEMS.slice().sort(() => Math.random() - 0.5); picks = a.slice(0, 2); }
  function startRound() {
    phase = 'write'; left = 30; $('checks').hidden = true; $('ta').hidden = false; $('ta').value = '';
    $('part').textContent = 'お題 ' + (round + 1) + ' / 2'; $('q').textContent = picks[round][0] + ' ' + picks[round][1] + ' の使い道は？';
    $('goBtn').textContent = '書けた（次へ）'; $('count').textContent = '残り 30 秒'; $('bar').style.width = '0%'; $('ta').focus();
    clearInterval(timer); timer = setInterval(() => { left--; $('count').textContent = '残り ' + left + ' 秒'; $('bar').style.width = ((30 - left) / 30 * 100) + '%'; if (left <= 0) next(); }, 1000);
  }
  function lines() { return $('ta').value.split(/\n/).map(s => s.trim()).filter(Boolean).slice(0, 30); }
  function next() {
    if (phase !== 'write') return;
    clearInterval(timer); answers[round] = lines(); round++;
    if (round < 2) startRound(); else showChecks();
  }
  function showChecks() {
    phase = 'check'; $('ta').hidden = true; $('part').textContent = 'さいごに'; $('count').textContent = ''; $('bar').style.width = '100%';
    $('q').textContent = 'ほかの人は思いつかなさそうな使い道に、チェック';
    const all = answers.flatMap((a, r) => a.map(t => [r, t]));
    $('checks').innerHTML = all.length ? all.map(([r, t], i) => `<div><label style="display:flex;gap:10px;align-items:center;width:100%;cursor:pointer"><input type="checkbox" data-i="${i}"> <span class="k">${picks[r][1]}：${t.replace(/[<>&]/g, '')}</span></label></div>`).join('') : '<div>（書いた使い道がありません）</div>';
    $('checks').hidden = false; $('goBtn').textContent = '結果を見る';
  }
  $('goBtn').addEventListener('click', () => { if (phase === 'write') next(); else done(); });
  function done() {
    phase = 'done';
    const n1 = answers[0].length, n2 = answers[1].length, rare = document.querySelectorAll('#checks input:checked').length;
    const T = Math.max(n1, n2) >= 6 && rare >= 2 ? ['🌟', 'たくさん＆ひねり型', '数も多く、めずらしい使い道も出せました。']
            : Math.max(n1, n2) >= 6 ? ['🌊', 'たくさん型', '数の勢いが強いタイプ。アイデアの数は、最初の1分がいちばん多いことが分かっています（Beaty・Silvia 2012）。']
            : rare >= 2 ? ['🌀', 'ひねり型', '数は少なくても、めずらしい使い道を出せるタイプ。IQ120あたりの境目が見えたのは、めずらしいアイデアのほうでした（Jauk ほか 2013）。']
            : n2 > n1 ? ['🌱', 'あとから型', '2回目のほうが多く書けました。おもしろいアイデアは、時間がたつほど出てきます。']
            : ['🌱', 'じっくり型', '30秒は短すぎたかもしれません。少し歩いたり、ぼんやりしたりすると、発想が増えるという研究があります（Oppezzo・Schwartz 2014）。'];
    NOU.finish({
      label: '30秒で書けた使い道（2回の合計）', big: n1 + n2, unit: ' 個', emoji: T[0], typeName: T[1], advice: T[2],
      extraHTML: `<div class="syn-rows"><div><span class="k">${picks[0][0]} ${picks[0][1]}</span><span class="v">${n1} 個</span></div><div><span class="k">${picks[1][0]} ${picks[1][1]}</span><span class="v">${n2} 個</span></div><div><span class="k">めずらしい使い道</span><span class="v">${rare} 個</span></div></div>`,
      share: `使い道テストやってみた💡 30秒×2回で${n1 + n2}個・めずらしいのは${rare}個で「${T[1]}」でした。クリップの使い道、いくつ思いつく？`,
      cardTitle: 'わたしの発想', cardLine: `${picks[0][1]} ${n1}個 ・ ${picks[1][1]} ${n2}個 ・ めずらしい ${rare}個`,
      draw: (x, R) => {
        const mx = Math.max(8, n1, n2);
        [[picks[0][1], n1, '#4FC6B4'], [picks[1][1], n2, '#F5BB5C']].forEach(([lab, v, c], i) => {
          const bw = 260, xx = R.x + R.w / 2 - 300 + i * 340, h = 40 + v / mx * 420;
          x.fillStyle = '#2A3C43'; x.beginPath(); x.roundRect(xx, R.y + 50, bw, 500, 24); x.fill();
          x.fillStyle = c; x.beginPath(); x.roundRect(xx, R.y + 550 - h, bw, h, 24); x.fill();
          x.fillStyle = '#EEEAE3'; x.textAlign = 'center'; x.font = '800 40px ' + R.F; x.fillText(lab, xx + bw / 2, R.y + 30);
          x.fillStyle = '#0D1417'; x.font = '900 60px ' + R.F; x.fillText(v + '個', xx + bw / 2, R.y + 525);
        });
      },
    });
  }
  function start() { round = 0; answers = []; pickItems(); NOU.startPanels(); startRound(); }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "ある物の使い道を30秒で書き出す「使い道テスト」形式のセルフテストです。書いた内容は、この画面の中だけで数えます。",
    "article": """
    <h2>使い道テストとは</h2>
    <p>レンガやクリップのような身近な物の使い道を、できるだけたくさん考えるテストです。答えが1つに決まる問題ではなく、<b>ちがう方向にたくさん考える力（発想の力）</b>を見るのに、よく使われてきました。</p>

    <h2>IQと発想のつながりは小さい</h2>
    <p>21の研究・45,880人をまとめると、発想のテストの点とIQのつながりは小さいものでした（Kim 2005）。一方、297人で調べた研究では、アイデアの数ならIQ85あたり、めずらしいアイデアを2つならIQ100あたり、めずらしいアイデアをたくさんならIQ120あたりに「境目」があり、それより上では性格のほうが発想とつながっていました（Jauk ほか 2013）。</p>

    <h2>アイデアは、あとからおもしろくなる</h2>
    <p>10分間の使い道テストでは、アイデアの数は最初の1分がいちばん多く、おもしろさは時間がたつほど上がりました（Beaty・Silvia 2012）。はじめは知っている使い方が出て、それが出つくしたあとに、新しい使い道が出てくるのです。</p>

    <h2>発想を増やすには</h2>
    <p>歩きながら使い道テストをすると、81%の人で点が上がりました（Oppezzo・Schwartz 2014）。一度考えたあと、頭を使わないかんたんな作業をはさむと、もう一度考えたときに大きく伸びたという研究もあります（Baird ほか 2012）。</p>

    <h2>結果のタイプ</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>目安</th></tr>
    <tr><td>🌊 たくさん型</td><td>どちらかの回で6個以上</td></tr>
    <tr><td>🌀 ひねり型</td><td>めずらしい使い道が2個以上</td></tr>
    <tr><td>🌱 あとから型</td><td>2回目のほうが多い</td></tr>
    </table>
    </div>
    <p>タイプは、このページだけの遊びの区切りで、研究の基準ではありません。数が少なくても、発想がないということではありません。</p>
""",
    "faq": [
        ("書いた使い道は、だれかに見られますか？", "いいえ。書いた内容はこの画面の中だけで数え、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
        ("頭がいい人ほど発想が多いのですか？", "4万5千人以上をまとめた研究では、IQと発想のテストのつながりは小さいものでした（Kim 2005）。IQは上がっているのに、発想のテストの点は1990年から下がっていたという報告もあります（Kim 2011）。"),
        ("「めずらしい」はどうやって決めるのですか？", "このページでは、自分で「ほかの人は思いつかなさそう」と思うものに印をつけます。研究では、複数の人が採点します。"),
        ("30秒では短すぎませんか？", "研究では1分〜10分のことが多いです。このページは手軽に試せるよう30秒にしています。もう一度試すと、数が増えることもあります。"),
    ],
    "refs": [
        "Kim KH (2005). Can only intelligent people be creative? A meta-analysis. <i>Journal of Secondary Gifted Education</i>, 16(2–3), 57–66.",
        "Jauk E, Benedek M, Dunst B, Neubauer AC (2013). The relationship between intelligence and creativity: New support for the threshold hypothesis by means of empirical breakpoint detection. <i>Intelligence</i>, 41(4), 212–221.",
        "Beaty RE, Silvia PJ (2012). Why do ideas get more creative across time? <i>Psychology of Aesthetics, Creativity, and the Arts</i>, 6(4), 309–319.",
        "Oppezzo M, Schwartz DL (2014). Give your ideas some legs: The positive effect of walking on creative thinking. <i>Journal of Experimental Psychology: Learning, Memory, and Cognition</i>, 40(4), 1142–1152.",
        "Baird B, et al. (2012). Inspired by distraction: Mind wandering facilitates creative incubation. <i>Psychological Science</i>, 23(10), 1117–1122.",
        "Kim KH (2011). The creativity crisis: The decrease in creative thinking scores on the Torrance Tests of Creative Thinking. <i>Creativity Research Journal</i>, 23(4), 285–295.",
    ],
    "related": [("zukei-housoku", "🔷", "図形の法則テスト"), ("matsu-chikara", "⏳", "待つ力テスト"), ("shikou-type", "💭", "絵で考える？言葉で考える？"), ("iq-yottsu-chikara", "🧠", "IQ 4つの力テスト")],
}
