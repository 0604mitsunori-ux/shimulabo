# -*- coding: utf-8 -*-
# 十人十脳 第30話「あくびがうつる人・うつらない人」と連動（2026-11-05 新規）。あくびの顔はこのページで作ったイラストのアニメ
PAGE = {
    "slug": "akubi-test",
    "title": "あくびがうつる？テスト｜あくびのアニメを見て、あくびが出るか試す｜シミュラボ",
    "desc": "人のあくびを見ると、自分もあくびが出てしまう。そんな「あくびがうつる」かどうかを、あくびをするイラストのアニメで試すセルフテスト。あくびを見るだけでなく、読んだり考えたりするだけでもあくびが出るという研究や、うつりやすさは年齢と関係していたという研究も解説。診断ではありません。",
    "og_title": "このアニメを見て、あくびが出たら…｜あくびがうつる？テスト",
    "og_desc": "あくびをするアニメを見て、あくびが出るか試す。この説明を読んでいるだけで、もう出そう？",
    "ld_name": "あくびがうつる？テスト",
    "h1": "あくびがうつる？テスト（あくびのアニメを見て、あくびが出る？）",
    "lead": "となりの人があくびをすると、つられて自分もあくびが出る。あくびは「うつる」ことで有名です。ところが、うつりやすさには大きな個人差があります。あくびをするイラストのアニメを、1分間見てください。あくびが出たら、ボタンを押してね。",
    "start_h2": "🥱 1分間、アニメを見てね",
    "start_text": "あくびをするイラストの顔が、くり返し出てきます。あくびが出たら「あくびが出た！」、出そうになったら「出そう…」を押してください。何回押してもOKです。",
    "tag": "あくび",
    "card_label": "あくびがうつる？テストの結果",
    "card_footer": "あくびがうつる人・うつらない人 → shimulabo.com",
    "stage_html": """
      <div class="syn-top"><span id="part">見ていてね</span><span id="count">のこり 60 秒</span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div id="face" style="width:230px;height:250px;margin:6px auto 10px;"></div>
      <div class="syn-btns" id="opts"></div>
      <p class="syn-note" id="tally">あくび 0 回・出そう 0 回</p>
    """,
    "js": r"""
  const $ = NOU.$;
  const SEC = 60;
  const FACE = `<svg viewBox="0 0 200 220" style="width:100%;height:100%;"><ellipse cx="100" cy="112" rx="78" ry="94" fill="#f1cfb2"/><path d="M24 96 Q20 18 100 16 Q180 18 176 96 Q156 54 100 50 Q44 54 24 96Z" fill="#5a3b26"/>`
    + `<g id="ey"><circle cx="70" cy="104" r="8" fill="#222"/><circle cx="130" cy="104" r="8" fill="#222"/></g><path id="lid" d="M58 104 Q70 112 82 104 M118 104 Q130 112 142 104" stroke="#222" stroke-width="4" fill="none" stroke-linecap="round" opacity="0"/>`
    + `<path d="M98 116 L92 136 H104" stroke="#b07a5a" stroke-width="3" fill="none" stroke-linecap="round"/>`
    + `<g id="mo" style="transform-box:fill-box;transform-origin:50% 30%;transition:transform 1.4s ease-in-out;transform:scaleY(.15)"><ellipse cx="100" cy="170" rx="26" ry="28" fill="#5a1f1f" stroke="#b5544f" stroke-width="5"/><ellipse cx="100" cy="186" rx="14" ry="8" fill="#d06a6a"/></g>`
    + `<g id="hand" style="transition:opacity .6s;opacity:0"><ellipse cx="150" cy="178" rx="22" ry="16" fill="#e8bf9c"/></g></svg>`;
  let left = SEC, yawn = [], almost = [], t0 = 0, iv = 0, cyc = 0;
  function yawnAnim() {   // 約6秒で1回のあくび：口を大きく開けて目を閉じ、手を口に当てて、ゆっくり戻る
    const m = document.getElementById('mo'), ey = document.getElementById('ey'), lid = document.getElementById('lid'), h = document.getElementById('hand'); if (!m) return;
    m.style.transform = 'scaleY(1.15)'; setTimeout(() => { ey.style.opacity = 0; lid.style.opacity = 1; h.style.opacity = 1; }, 700);
    setTimeout(() => { m.style.transform = 'scaleY(.15)'; h.style.opacity = 0; }, 2600); setTimeout(() => { ey.style.opacity = 1; lid.style.opacity = 0; }, 3400);
  }
  function tally() { $('tally').textContent = `あくび ${yawn.length} 回・出そう ${almost.length} 回`; }
  function startView() { $('face').innerHTML = FACE; left = SEC; yawn = []; almost = []; t0 = performance.now(); cyc = 0; tally();
    $('opts').innerHTML = '<button type="button" data-v="y">あくびが出た！</button><button type="button" data-v="a">出そう…</button>';
    setTimeout(yawnAnim, 500);
    clearInterval(iv); iv = setInterval(() => { left--; cyc++; $('count').textContent = 'のこり ' + Math.max(0, left) + ' 秒'; $('bar').style.width = ((SEC - left) / SEC * 100) + '%';
      if (cyc % 6 === 0) yawnAnim(); if (left <= 0) { clearInterval(iv); askAfter(); } }, 1000); }
  function askAfter() { $('part').textContent = 'さいごに'; $('face').innerHTML = '<div style="height:100%;display:flex;align-items:center;justify-content:center;font-size:90px;">🤔</div>';
    $('opts').className = 'syn-btns c1'; $('opts').innerHTML = [['ふだん、人のあくびがよくうつる', 3], ['ときどきうつる', 2], ['ほとんどうつらない', 1]].map(([t, v]) => `<button type="button" data-v="q${v}">${t}</button>`).join(''); }
  $('opts').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; const v = b.dataset.v, s = Math.round((performance.now() - t0) / 1000);
    if (v === 'y') { yawn.push(s); tally(); return; } if (v === 'a') { almost.push(s); tally(); return; }
    if (v[0] === 'q') done(+v.slice(1)); });
  function done(self) {
    const n = yawn.length, a = almost.length;
    const T = n >= 1 ? ['🥱', 'あくびがうつるタイプ', `アニメを見て、あくびが${n}回出ました。イラストの顔でも、あくびはうつることがあります。`]
            : a >= 1 ? ['😪', 'あくびがうつりかけたタイプ', 'あくびが出そうになりました。あと少しで、うつるところでした。']
            : ['😐', '今回はうつらなかったタイプ', 'あくびは出ませんでした。うつりやすさは人によって大きくちがい、うつらないのはめずらしいことではありません。'];
    const first = n ? `<p style="font-size:14px;margin:6px 0;">最初のあくびは、見はじめてから<b>${yawn[0]}秒後</b>でした。</p>` : '';
    NOU.finish({
      label: '1分間に出たあくび', big: n, unit: ' 回', emoji: T[0], typeName: T[1], advice: T[2],
      extraHTML: first + `<div class="syn-rows"><div><span class="k">あくびが出た</span><span class="v">${n} 回</span></div><div><span class="k">出そうになった</span><span class="v">${a} 回</span></div><div><span class="k">ふだんのうつりやすさ（自分の答え）</span><span class="v">${['', 'ほとんどうつらない', 'ときどき', 'よくうつる'][self]}</span></div></div><p style="font-size:12px;color:var(--ink-3);">あくびがうつるかどうかで、やさしさや共感する力が決まるわけではありません。</p>`,
      share: `あくびがうつる？テストやってみた🥱 1分間であくび${n}回・出そう${a}回で「${T[1]}」でした。この投稿を見て、あなたもあくびが出た？`,
      cardTitle: 'わたしのあくびは、うつる？', cardLine: `1分間で あくび ${n}回・出そう ${a}回`,
      draw: (x, R) => {
        const y = R.y + 250; x.strokeStyle = '#2A3C43'; x.lineWidth = 8; x.beginPath(); x.moveTo(R.x, y); x.lineTo(R.x + R.w, y); x.stroke();
        for (let s = 0; s <= 60; s += 10) { const xx = R.x + s / 60 * R.w; x.fillStyle = '#8D9BA1'; x.textAlign = 'center'; x.font = '700 28px ' + R.F; x.fillText(s + '秒', xx, y + 60); }
        yawn.forEach(s => { const xx = R.x + Math.min(60, s) / 60 * R.w; x.font = '400 64px ' + R.F; x.fillText('🥱', xx, y - 30); });
        almost.forEach(s => { const xx = R.x + Math.min(60, s) / 60 * R.w; x.font = '400 48px ' + R.F; x.fillText('😪', xx, y + 130); });
      },
    });
  }
  function start() { clearInterval(iv); $('opts').className = 'syn-btns'; $('part').textContent = '見ていてね'; $('bar').style.width = '0%'; NOU.startPanels(); startView(); }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "このページで作った、あくびをするイラストの顔のアニメを1分間見て、あくびが出た回数・出そうになった回数をボタンで記録し、最後にふだんのうつりやすさを答えるセルフテストです。",
    "article": """
    <h2>あくびは、見るだけでうつる</h2>
    <p>アメリカの心理学者プロヴァインは、あくびを研究した先がけの一人です。人があくびをする映像を見せると、見た人にもあくびが起きることを実験で確かめました（Provine 1986）。</p>
    <p>さらにおもしろいことに、あくびは<b>見なくても</b>、あくびについて<b>読んだり、考えたりするだけ</b>でも起きることが報告されています。このページをここまで読んで、もうあくびが出た人もいるかもしれません。</p>

    <h2>うつりやすさは、人によって大きくちがう</h2>
    <p>あくびがうつりやすいかどうかを、たくさんの人で調べた研究があります（Bartholomew・Cirulli 2014）。すると、うつりやすさには大きな個人差があり、しかも<b>同じ人ならくり返し調べてもあまり変わらない</b>ことが分かりました。</p>
    <p>よく「あくびがうつる人は共感する力が高い」と言われます。ところがこの研究では、年齢を考えに入れると、共感の質問票の点数とはっきりした関係は見られませんでした。うつりやすさと関係していたのは<b>年齢だけ</b>で、年を重ねるほどうつりにくい傾向がありました。</p>

    <h2>このテストのしくみ</h2>
    <p>このページでは、本物の人の映像ではなく、あくびをするイラストの顔のアニメを使っています。本物の映像より、うつりにくいかもしれません。あくびが出なかったとしても、おかしいことではありません。</p>
    <p>家族や友だちといっしょに見て、だれがいちばん先にあくびをするか、くらべてみるのもおもしろいですよ。</p>

    <h2>結果の3つのタイプ</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>1分間の結果</th></tr>
    <tr><td>🥱 あくびがうつるタイプ</td><td>あくびが1回以上出た</td></tr>
    <tr><td>😪 あくびがうつりかけたタイプ</td><td>出そうになった</td></tr>
    <tr><td>😐 今回はうつらなかったタイプ</td><td>どちらもなし</td></tr>
    </table>
    </div>
""",
    "faq": [
        ("あくびがうつらないのは、共感する力が低いからですか？", "いいえ。研究では、年齢を考えに入れると、共感の点数とはっきりした関係は見られませんでした。うつらないのは、めずらしいことではありません。"),
        ("あくびが止まらないくらい出ます。", "眠気が強い・疲れているときにも、あくびは出やすくなります。昼間の強い眠気が続くときは、医療機関に相談してください。"),
        ("このテストで何かの病気が分かりますか？", "いいえ。遊びのためのセルフテストで、検査や診断ではありません。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Provine RR (1986). Yawning as a stereotyped action pattern and releasing stimulus. <i>Ethology</i>, 72, 109–122.",
        "Bartholomew AJ, Cirulli ET (2014). Individual variation in contagious yawning susceptibility is highly stable and largely unexplained by empathy or other known factors. <i>PLoS ONE</i>, 9(3), e91773.",
    ],
    "related": [("hsp-shindan", "🌿", "HSP診断（繊細さん）"), ("mcgurk-test", "👄", "マガーク効果テスト（目で聞く音）"), ("yume-type", "💭", "夢タイプ診断"), ("shinpaku-kankaku", "💓", "心臓の音が分かる？テスト")],
}
