# -*- coding: utf-8 -*-
# 十人十脳 第7話「忘れる人・覚える人（記憶）」と連動。既存の「単語記憶テスト」を同じURLのまま作り直した（2026-11-05）
PAGE = {
    "slug": "tango-kioku",
    "title": "単語記憶テスト｜すぐ忘れる人と、覚えている人は何がちがう？すぐあと・少しあとの記憶を試す｜シミュラボ",
    "desc": "12個の言葉を覚えて、すぐあとと、別のことをしたあとで、どれだけ思い出せるかを試す記憶のセルフテスト。忘れ方のカーブを140年前に調べた研究と、「思い出す練習」で記憶が残りやすくなる研究も解説。診断ではありません。",
    "og_title": "すぐ忘れる人、覚えている人｜単語記憶テスト",
    "og_desc": "12個の言葉、すぐあとと少しあとで、どれだけ残る？",
    "ld_name": "単語記憶テスト（すぐあと・少しあと）",
    "h1": "単語記憶テスト（すぐ忘れる人と、覚えている人は何がちがう？）",
    "lead": "同じものを見ても、すぐ忘れてしまう人と、ずっと覚えている人がいます。12個の言葉が1つずつ出るので、覚えてください。すぐあとに半分、別のことを30秒したあとに残りの半分を思い出します。約2分です。",
    "start_h2": "📝 12個の言葉を覚えてね",
    "start_text": "言葉が1.5秒ずつ、12個出ます。声に出しても、頭の中でくり返してもOK。そのあと「出てきた言葉」を選ぶ問題になります。",
    "tag": "記憶力テスト",
    "card_label": "単語記憶テストの結果",
    "card_footer": "すぐ忘れる？覚えている？ → shimulabo.com 単語記憶テスト",
    "stage_html": """
      <div class="syn-top"><span id="part">覚える</span><span id="count"></span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div id="show" class="syn-big" style="font-size:60px;min-height:1.5em;"></div>
      <div id="ask" class="syn-ask"></div>
      <div id="pick" class="syn-btns" style="grid-template-columns:repeat(3,1fr);" hidden></div>
      <button type="button" class="syn-go" id="okBtn" hidden>これで答える</button>
      <div id="dist" class="syn-btns" hidden><button type="button" data-v="1">10より大きい</button><button type="button" data-v="0">10以下</button></div>
    """,
    "js": r"""
  const $ = NOU.$;
  const POOL = ['りんご', 'でんしゃ', 'うみ', 'とけい', 'ねこ', 'ほん', 'ほし', 'かさ', 'えんぴつ', 'はな', 'やま', 'くつ', 'とり', 'パン', 'はし', 'ゆき', 'つくえ', 'かぎ', 'ふね', 'もり', 'くも', 'まど', 'はた', 'かい', 'いす', 'たいこ', 'みかん', 'てがみ', 'ぼうし', 'かがみ', 'たまご', 'いぬ', 'ふうせん', 'ろうそく', 'はさみ', 'ラジオ'];
  let words = [], A = [], B = [], lureA = [], lureB = [], sel = new Set(), phase = '', res = {}, timer = 0, dk = 0;
  const shuffle = a => a.slice().sort(() => Math.random() - .5);
  function study() {
    phase = 'study'; let i = 0; $('part').textContent = '覚える'; $('ask').textContent = ''; $('pick').hidden = $('okBtn').hidden = $('dist').hidden = true;
    const step = () => { if (i >= 12) { $('show').textContent = ''; return recall('A'); } $('show').textContent = words[i]; $('count').textContent = (i + 1) + ' / 12'; $('bar').style.width = (i / 12 * 100) + '%'; i++; timer = setTimeout(step, 1500); };
    step();
  }
  function recall(which) {
    phase = which; sel = new Set(); $('show').textContent = '';
    const list = shuffle(which === 'A' ? A.concat(lureA) : B.concat(lureB));
    $('part').textContent = which === 'A' ? 'すぐあとに思い出す' : '少しあとに思い出す'; $('count').textContent = '';
    $('ask').innerHTML = 'さっき<b>出てきた言葉</b>を、ぜんぶ選んでね（このなかに6個あります）';
    $('pick').hidden = false; $('okBtn').hidden = false; $('dist').hidden = true;
    $('pick').innerHTML = list.map(w => `<button type="button" data-w="${w}">${w}</button>`).join('');
  }
  $('pick').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; const w = b.dataset.w; if (sel.has(w)) { sel.delete(w); b.style.borderColor = '#2A3C43'; b.style.background = '#111c20'; } else { sel.add(w); b.style.borderColor = '#4FC6B4'; b.style.background = '#1d3d49'; } });
  $('okBtn').addEventListener('click', () => {
    const old = phase === 'A' ? A : B, hit = old.filter(w => sel.has(w)).length, fa = [...sel].filter(w => !old.includes(w)).length;
    res[phase] = { hit, fa, score: Math.max(0, hit - fa) };
    if (phase === 'A') distract(); else done();
  });
  function distract() {             // 30秒、別のこと（足し算）をして、覚えたことから頭をはなす
    phase = 'dist'; $('pick').hidden = $('okBtn').hidden = true; $('dist').hidden = false; $('part').textContent = '30秒、別のことをする';
    const t0 = performance.now(); dk = 0;
    const q = () => { const a = 1 + Math.floor(Math.random() * 9), b = 1 + Math.floor(Math.random() * 9); $('show').textContent = a + ' ＋ ' + b; $('show').dataset.s = a + b; $('ask').textContent = '答えは10より大きい？'; };
    q(); clearInterval(timer);
    timer = setInterval(() => { const s = (performance.now() - t0) / 1000; $('count').textContent = Math.max(0, Math.ceil(30 - s)) + ' 秒'; $('bar').style.width = Math.min(100, s / 30 * 100) + '%'; if (s >= 30) { clearInterval(timer); recall('B'); } }, 200);
    $('dist').onclick = e => { if (e.target.closest('button')) { dk++; q(); } };
  }
  function done() {
    const a = res.A.score, b = res.B.score, drop = a - b;
    const T = b >= 5 && drop <= 1 ? ['🧱', 'しっかり残るタイプ', '別のことをはさんでも、覚えた言葉がほとんど残っていました。']
            : drop >= 3 ? ['🍃', 'すぐ入れかわるタイプ', 'すぐあとはよく思い出せましたが、別のことをはさむと、ぐっと減りました。新しいことが入ると、前のことが押し出されやすいのかもしれません。']
            : ['🌗', '少しずつ薄れるタイプ', '別のことをはさむと、少しだけ減りました。多くの人はこのあたりです。'];
    NOU.finish({
      label: '少しあと（30秒の別のことのあと）に思い出せた数', big: b, unit: ' / 6 個', emoji: T[0], typeName: T[1], advice: T[2],
      extraHTML: `<div class="syn-rows"><div><span class="k">すぐあと</span><span class="syn-meter"><i style="width:${a / 6 * 100}%"></i></span><span class="v">${a} / 6</span></div><div><span class="k">30秒の別のことのあと</span><span class="syn-meter"><i style="width:${b / 6 * 100}%"></i></span><span class="v">${b} / 6</span></div></div>
        <p style="font-size:12px;color:var(--ink-3);">点数は「当たった数 − まちがえて選んだ数」です（0より下は0）。</p>`,
      share: `単語記憶テストやってみた📝 すぐあと ${a}/6・少しあと ${b}/6 で「${T[1]}」でした。あなたは、すぐ忘れる？覚えている？`,
      cardTitle: 'わたしの記憶の残り方', cardLine: `すぐあと ${a}/6 → 少しあと ${b}/6`,
      draw: (x, R) => {
        [['すぐあと', a, '#4FC6B4'], ['少しあと', b, '#F5BB5C']].forEach(([n, v, c], i) => {
          const bw = 260, xx = R.x + R.w / 2 - 300 + i * 340, h = 80 + v * 70, y = R.y + 520 - h;
          x.fillStyle = '#2A3C43'; x.beginPath(); x.roundRect(xx, R.y + 100, bw, 420, 24); x.fill();
          x.fillStyle = c; x.beginPath(); x.roundRect(xx, y, bw, h, 24); x.fill();
          x.fillStyle = '#EEEAE3'; x.textAlign = 'center'; x.font = '800 40px ' + R.F; x.fillText(n, xx + bw / 2, R.y + 70);
          x.fillStyle = '#0D1417'; x.font = '900 64px ' + R.F; x.fillText(v + ' / 6', xx + bw / 2, R.y + 490);
        });
      },
    });
  }
  function start() {
    clearTimeout(timer); clearInterval(timer);
    const p = shuffle(POOL); words = p.slice(0, 12); const w2 = shuffle(words); A = w2.slice(0, 6); B = w2.slice(6); lureA = p.slice(12, 18); lureB = p.slice(18, 24); res = {};
    NOU.startPanels(); study();
  }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "12個の言葉を覚えて、すぐあとに半分、30秒の別の作業（足し算）のあとに残りの半分を、まぎらわしい言葉の中から選ぶセルフテストです。",
    "article": """
    <h2>人は、どのくらいの速さで忘れる？</h2>
    <p>1880年代、ドイツのエビングハウスという研究者が、意味のない文字の並びを自分で覚えては、どれだけ忘れるかを調べました。これが有名な「忘れ方のカーブ（忘却曲線）」です。</p>
    <p>2015年、オランダの研究者が<b>同じやり方で調べ直しました</b>。1人が70時間かけて言葉のリストを覚え、20分後・1時間後・9時間後・1日後・2日後・31日後に覚え直して、どれだけ楽になるかを測ったのです。結果は、140年前のエビングハウスのものとよく似ていました。そして、<b>1日（24時間）たったところで、カーブが少しだけ持ち直す</b>ことも分かりました（Murre・Dros 2015）。</p>

    <h2>「もう一度読む」より「思い出す」</h2>
    <p>アメリカの研究では、学生に文章を読ませたあと、半分の人には<b>もう一度読ませ</b>、残りの人には<b>何も見ずに思い出して書かせ</b>ました（Roediger・Karpicke 2006）。</p>
    <ul>
      <li>5分後のテストでは、もう一度読んだ人のほうがよく覚えていた</li>
      <li>ところが、<b>2日後・1週間後</b>のテストでは、思い出す練習をした人のほうがよく覚えていた</li>
      <li>もう一度読んだ人は、「覚えた」という自信だけは高かった</li>
    </ul>
    <p>すぐ忘れる人と覚えている人のちがいは、生まれつきの記憶力だけではなく、<b>覚え方</b>にもあるのかもしれません。</p>

    <h2>このテストで分かること</h2>
    <p>このテストは、すぐあとと、30秒の別のこと（足し算）のあとをくらべています。30秒でも、別のことが頭に入ると、覚えたことは押し出されやすくなります。ただし、1日・1週間あとの「長く残る記憶」とは別のものです。長く覚えたいことは、何度も思い出す練習をしてみてください。</p>

    <h2>結果の3つのタイプ</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>どんな結果？</th></tr>
    <tr><td>🧱 しっかり残るタイプ</td><td>少しあとも6個中5個以上で、すぐあととの差が1個以内</td></tr>
    <tr><td>🌗 少しずつ薄れるタイプ</td><td>少しあとに、少しだけ減った</td></tr>
    <tr><td>🍃 すぐ入れかわるタイプ</td><td>少しあとに、3個以上減った</td></tr>
    </table>
    </div>
    <p>点数は「当たった数 − まちがえて選んだ数」で出しています。全部選んでしまうと、点数は上がりません。</p>
""",
    "faq": [
        ("このテストで記憶力が分かりますか？", "いいえ。遊びのためのセルフテストで、検査ではありません。その日の体調や集中でも大きく変わります。"),
        ("すぐあとは覚えていたのに、少しあとに忘れました。", "多くの人に起きることです。別のことをすると、覚えたばかりのことは押し出されやすくなります。"),
        ("覚えたことを長く残すには？", "もう一度読むより、何も見ずに思い出す練習をしたほうが、2日後・1週間後によく残っていたという研究があります（Roediger・Karpicke 2006）。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Murre JMJ, Dros J (2015). Replication and Analysis of Ebbinghaus' Forgetting Curve. <i>PLoS ONE</i>, 10(7), e0120644.",
        "Roediger HL, Karpicke JD (2006). Test-Enhanced Learning: Taking Memory Tests Improves Long-Term Retention. <i>Psychological Science</i>, 17(3), 249–255.",
    ],
    "related": [("naigen-test", "💬", "頭の中の声テスト"), ("suuji-kioku", "🔢", "数字記憶テスト"), ("shunkan-kioku", "⚡", "瞬間記憶テスト"), ("aphantasia-test", "🍎", "アファンタジア テスト（頭の中の映像）")],
}
