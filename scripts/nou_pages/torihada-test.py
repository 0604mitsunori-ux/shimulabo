# -*- coding: utf-8 -*-
# 十人十脳 第27話「音楽で鳥肌が立つ人」と連動（2026-11-05 新規）。曲は使わず、ふだんの体験の質問で試す（自作曲を足すときは別途）
PAGE = {
    "slug": "torihada-test",
    "title": "音楽で鳥肌が立つ？テスト｜同じ曲で鳥肌が立つ人と立たない人のちがい｜シミュラボ",
    "desc": "好きな曲のサビで、背中がゾクッとする。そんな「音楽の鳥肌」が立ちやすいかを、8つの質問で試すセルフテスト。鳥肌が立つ直前と瞬間に、脳で「快感の物質」が出ていた研究や、鳥肌が立ちやすい人は耳と感情の場所をつなぐ脳の配線が多かった研究も解説。診断ではありません。",
    "og_title": "同じ曲で、鳥肌が立つ人と立たない人｜音楽で鳥肌が立つ？テスト",
    "og_desc": "8つの質問で、あなたの「音楽の鳥肌」の立ちやすさを。鳥肌タイプ？涙タイプ？",
    "ld_name": "音楽で鳥肌が立つ？テスト",
    "h1": "音楽で鳥肌が立つ？テスト（同じ曲で、鳥肌が立つ人と立たない人）",
    "lead": "同じ曲を聞いても、サビで鳥肌が立つ人もいれば、何も感じない人もいます。音楽で体が反応するしくみは、脳の研究でも少しずつ分かってきました。8つの質問に答えてください。約1分です。",
    "start_h2": "🎵 8つの質問に答えてね",
    "start_text": "ふだん音楽を聞いたり、映画を見たりしたときのことを思い浮かべて答えてください。",
    "tag": "音楽の鳥肌",
    "card_label": "音楽で鳥肌が立つ？テストの結果",
    "card_footer": "同じ曲で、鳥肌が立つ人と立たない人 → shimulabo.com",
    "stage_html": """
      <div class="syn-top"><span>ふだんの自分は？</span><span id="count">1 / 8</span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div class="syn-big" id="em" style="font-size:56px;"></div>
      <div class="syn-ask" id="q" style="font-size:18px;font-weight:700;color:#EEEAE3;min-height:3em;line-height:1.7;"></div>
      <div class="syn-btns c1" id="opts"></div>
    """,
    "js": r"""
  const $ = NOU.$;
  // c＝鳥肌、t＝涙、m＝音楽へののめりこみ。問題はこのページで作ったもの
  const Q = [
    ['c', '🎵', '音楽を聞いて、鳥肌が立つことは？'], ['c', '🎤', '曲がいちばん盛り上がる瞬間に、背中がゾクッとする？'], ['t', '😢', '音楽を聞いて、涙が出ることは？'],
    ['c', '🎬', '映画やドラマの名場面で、鳥肌が立つ？'], ['m', '🔁', '好きな曲の同じところを、何度も聞き返す？'], ['t', '🎻', 'しずかで切ない曲を聞くと、胸がぎゅっとなる？'],
    ['m', '🎧', '音楽を聞くと、まわりの音が聞こえなくなるくらい入りこむ？'], ['c', '🗣️', 'スピーチや歌声の「声」だけで、ゾクッとすることがある？'],
  ];
  const O = [['よくある', 4], ['ときどきある', 3], ['あまりない', 2], ['まったくない', 1]];
  let k = 0, ans = [];
  function show() { const [, e, q] = Q[k]; $('em').textContent = e; $('q').textContent = q; $('count').textContent = (k + 1) + ' / 8'; $('bar').style.width = (k / 8 * 100) + '%';
    $('opts').innerHTML = O.map(([t, v]) => `<button type="button" data-v="${v}">${t}</button>`).join(''); }
  $('opts').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; ans.push(+b.dataset.v); k++; if (k < 8) show(); else done(); });
  function done() {
    const avg = t => { const v = Q.map((q, i) => q[0] === t ? ans[i] : null).filter(x => x !== null); return v.reduce((a, b) => a + b, 0) / v.length; };
    const c = avg('c'), t = avg('t'), m = avg('m'), sc = Math.round(c * 25);   // 鳥肌 25〜100
    const T = c >= 3 && t >= 3 ? ['🎆', '鳥肌も涙も出るタイプ', '音楽で、体も心も大きく動くタイプです。']
            : c >= 3 ? ['⚡', '鳥肌タイプ', '曲の盛り上がりで、体がゾクッと反応しやすいタイプです。']
            : t >= 3 ? ['💧', '涙タイプ', '鳥肌よりも、しみじみと涙が出やすいタイプです。研究では、鳥肌と涙は体の反応がちがうと報告されています。']
            : ['🌊', '静かに味わうタイプ', '体が大きく反応するより、静かに音楽を味わうタイプです。鳥肌が立つ曲は人それぞれなので、まだ出会っていないだけかもしれません。'];
    const AX = [['⚡ 鳥肌', c], ['💧 涙', t], ['🎧 のめりこみ', m]];
    NOU.finish({
      label: '音楽の鳥肌の立ちやすさ（25〜100）', big: sc, unit: ' / 100', emoji: T[0], typeName: T[1], advice: T[2],
      extraHTML: `<div class="syn-rows">${AX.map(([n, v]) => `<div><span class="k">${n}</span><span class="v">${'●'.repeat(Math.round(v))}${'○'.repeat(4 - Math.round(v))}</span></div>`).join('')}</div><p style="font-size:14px;margin:6px 0;">試してみよう：自分が鳥肌が立つ曲を流して、ゾクッとする直前の「来るぞ」という感じにも注目してみてください。</p>`,
      share: `音楽で鳥肌が立つ？テストやってみた🎵 鳥肌の立ちやすさ${sc}/100で「${T[1]}」でした。あなたは同じ曲で鳥肌が立つ？`,
      cardTitle: 'わたしの「音楽の鳥肌」', cardLine: `鳥肌の立ちやすさ ${sc} / 100`,
      draw: (x, R) => {
        const cw = (R.w - 2 * 40) / 3, base = R.y + 460;
        AX.forEach(([n, v], i) => { const xx = R.x + i * (cw + 40), h = 40 + (v - 1) / 3 * 320;
          x.fillStyle = '#2A3C43'; x.beginPath(); x.roundRect(xx, base - 360, cw, 360, 24); x.fill();
          x.fillStyle = i === 0 ? '#F5BB5C' : '#4FC6B4'; x.beginPath(); x.roundRect(xx, base - h, cw, h, 24); x.fill();
          x.textAlign = 'center'; x.fillStyle = '#EEEAE3'; x.font = '800 38px ' + R.F; x.fillText(n, xx + cw / 2, base + 52); });
      },
    });
  }
  function start() { k = 0; ans = []; NOU.startPanels(); show(); }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "音楽や映画で鳥肌が立つか・涙が出るか・音楽にのめりこむかについての8つの質問に答えるセルフテストです。問題はこのページで作っています。",
    "article": """
    <h2>音楽の鳥肌は、脳の「ごほうび」</h2>
    <p>カナダの研究チームは、参加者に<b>自分で選んだ「鳥肌が立つ曲」</b>を聞いてもらい、脳の中で何が起きているかを調べました（Salimpoor ほか 2011）。</p>
    <p>すると、曲が盛り上がる<b>直前</b>には脳の「尾状核」という場所で、鳥肌が立つ<b>その瞬間</b>には「側坐核」という場所で、快感に関わる物質<b>ドーパミン</b>が出ていました。おいしいものを食べたときなどに関わる、脳の「ごほうび」のしくみが、音楽でも働いていたのです。</p>
    <p>「来るぞ、来るぞ」という期待の時間と、来た瞬間の気持ちよさ。その両方に、脳がちゃんと反応していたことになります。</p>

    <h2>鳥肌が立ちやすい人は、脳の配線がちがう？</h2>
    <p>アメリカの研究チームは、音楽で鳥肌が立つ人10人と、立たない人10人の脳の配線（神経の通り道）をくらべました（Sachs ほか 2016）。すると、鳥肌が立ちやすい人ほど、<b>音を聞く場所と、感情や体の感覚に関わる場所をつなぐ配線</b>が多い傾向がありました。</p>
    <p>ただし、調べた人数が少ないため、これから確かめていく必要がある結果です。</p>

    <h2>鳥肌と涙は、別の反応</h2>
    <p>音楽で鳥肌が立つときと、涙が出るときをくらべた研究もあります（Mori・Iwanaga 2017）。体の反応を測ると、鳥肌のときは<b>皮膚の汗の反応（体の高ぶり）が強まり</b>、涙のときは<b>弱まって</b>いて、2つはちがう反応だと考えられています。</p>
    <p>このテストで「鳥肌」と「涙」を分けて出しているのは、そのためです。</p>

    <h2>結果の4つのタイプ</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>めやす</th></tr>
    <tr><td>🎆 鳥肌も涙も出るタイプ</td><td>鳥肌も涙も「ときどき」以上</td></tr>
    <tr><td>⚡ 鳥肌タイプ</td><td>鳥肌が「ときどき」以上</td></tr>
    <tr><td>💧 涙タイプ</td><td>涙が「ときどき」以上</td></tr>
    <tr><td>🌊 静かに味わうタイプ</td><td>どちらも「あまりない」くらい</td></tr>
    </table>
    </div>
""",
    "faq": [
        ("鳥肌が立たないのは、感受性が低いからですか？", "いいえ。鳥肌が立つかどうかは、曲との相性や、そのときの気分でも変わります。静かに深く味わう楽しみ方もあります。"),
        ("どんな曲で鳥肌が立ちやすいですか？", "人によってちがいます。研究でも、参加者が自分で選んだ「鳥肌が立つ曲」を使って調べています。"),
        ("このテストで何かの病気が分かりますか？", "いいえ。遊びのためのセルフテストで、検査や診断ではありません。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Salimpoor VN, Benovoy M, Larcher K, Dagher A, Zatorre RJ (2011). Anatomically distinct dopamine release during anticipation and experience of peak emotion to music. <i>Nature Neuroscience</i>, 14(2), 257–262.",
        "Sachs ME, Ellis RJ, Schlaug G, Loui P (2016). Brain connectivity reflects human aesthetic responses to music. <i>Social Cognitive and Affective Neuroscience</i>, 11(6), 884–891.",
        "Mori K, Iwanaga M (2017). Two types of peak emotional responses to music: The psychophysiology of chills and tears. <i>Scientific Reports</i>, 7, 46063.",
    ],
    "related": [("onkan-test", "🎹", "絶対音感テスト・相対音感テスト"), ("rhythm-test", "🥁", "リズム感テスト"), ("hsp-shindan", "🌿", "HSP診断（繊細さん）"), ("shinpaku-kankaku", "💓", "心臓の音が分かる？テスト")],
}
