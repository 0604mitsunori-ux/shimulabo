# -*- coding: utf-8 -*-
# 十人十脳 第29話「自分の心臓の音が分かる人」と連動（2026-11-05 新規）。shinpaku-zone（心拍ゾーン計算）とは別のテーマ
PAGE = {
    "slug": "shinpaku-kankaku",
    "title": "心臓の音が分かる？テスト｜脈にさわらずに、自分の心拍を数えられる？｜シミュラボ",
    "desc": "胸や手首にさわらずに、自分の心臓が何回打ったかを数えて、あとで測った脈とくらべるセルフテスト。体の内側の感覚「内受容感覚」の研究で40年以上使われてきた方法と、その方法への疑問も解説。結果は目安で、医療の検査ではありません。",
    "og_title": "脈にさわらずに、心臓の音を数えられる？｜心臓の音が分かる？テスト",
    "og_desc": "さわらずに数えた心拍と、実際の脈をくらべる。あなたは体の声が聞こえる？",
    "ld_name": "心臓の音が分かる？テスト（心拍を数える）",
    "h1": "心臓の音が分かる？テスト（脈にさわらずに、心拍を数えられる？）",
    "lead": "静かにしていると、自分の心臓がドクドクと打つのを感じることがあります。その感じ方には、人によって大きなちがいがあります。脈にさわらずに心拍を数えて、あとで測った脈とくらべてみましょう。約3分です。",
    "start_h2": "💓 心臓の音を数えてね",
    "start_text": "いすにすわって、楽にしてください。合図が出たら、胸や手首にさわらずに、心臓が打つのを感じた回数を心の中で数えます。これを3回くり返したあと、最後に手首で脈を測ります。",
    "tag": "心拍",
    "card_label": "心臓の音が分かる？テストの結果",
    "card_footer": "脈にさわらずに心拍を数えられる？ → shimulabo.com",
    "stage_html": """
      <div class="syn-top"><span id="part">1回目</span><span id="count">1 / 4</span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div class="syn-big" id="em" style="font-size:72px;">💓</div>
      <div class="syn-ask" id="q" style="font-size:18px;font-weight:700;color:#EEEAE3;min-height:3.2em;line-height:1.7;"></div>
      <div id="inp" style="display:flex;gap:8px;justify-content:center;margin:6px 0 10px;" hidden><input id="num" type="number" inputmode="numeric" min="0" max="300" style="width:120px;font-size:24px;padding:8px;border-radius:10px;border:0;text-align:center;"><span style="align-self:center;color:#EEEAE3;">回</span></div>
      <div class="syn-btns c1" id="opts"></div>
      <p class="syn-note">合図の音が出ます。目を閉じていてもOKです。</p>
    """,
    "js": r"""
  const $ = NOU.$;
  const LEN = [25, 35, 45], PULSE = 30;   // 数える秒数（研究でよく使われる長さ）・脈を測る秒数
  let order = [], k = 0, cnt = [], pulse = 0, ctx = null, tm = 0;
  function beep(f) { if (!ctx) return; const o = ctx.createOscillator(), g = ctx.createGain(), t = ctx.currentTime; o.frequency.value = f; g.gain.setValueAtTime(0.2, t); g.gain.exponentialRampToValueAtTime(0.001, t + 0.25); o.connect(g).connect(ctx.destination); o.start(t); o.stop(t + 0.3); }
  function ready() {
    const last = k === 3; $('part').textContent = last ? '脈を測る' : (k + 1) + '回目'; $('count').textContent = (k + 1) + ' / 4'; $('bar').style.width = (k / 4 * 100) + '%'; $('inp').hidden = true;
    $('em').textContent = last ? '🫳' : '💓';
    $('q').textContent = last ? `最後は、手首か首に指を当てて、${PULSE}秒間の脈を数えてね。` : '胸や手首にさわらずに、心臓が打つのを感じた回数を数えてね。';
    $('opts').innerHTML = '<button type="button" data-v="go">スタート</button>';
  }
  function run() {
    const sec = k === 3 ? PULSE : order[k]; $('opts').innerHTML = ''; $('em').textContent = '🔔'; $('q').textContent = '合図で数えはじめて…'; beep(880);
    setTimeout(() => { $('em').textContent = '🤫'; $('q').textContent = '数えています…（合図の音で終わり）'; tm = setTimeout(() => { beep(660); askNum(); }, sec * 1000); }, 300);
  }
  function askNum() { $('em').textContent = '✍️'; $('q').textContent = k === 3 ? '脈は何回でしたか？' : '心臓が打ったのは何回でしたか？'; $('inp').hidden = false; $('num').value = '';
    $('opts').innerHTML = '<button type="button" data-v="ok">決定</button>'; }
  $('opts').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return;
    if (b.dataset.v === 'go') { run(); return; }
    const n = Math.max(0, Math.min(300, Math.round(+$('num').value || 0)));
    if (k === 3) { if (n < 10) { $('q').textContent = '脈を数えた回数を入れてね（10回以上）'; return; } pulse = n; done(); return; }
    cnt.push(n); k++; ready(); });
  function done() {
    const hr = pulse / PULSE * 60;   // 1分あたりの心拍（目安）
    const acc = order.map((s, i) => { const real = hr * s / 60; return Math.max(0, 1 - Math.abs(real - cnt[i]) / real); });
    const sc = Math.round(acc.reduce((a, b) => a + b, 0) / 3 * 100);
    const T = sc >= 85 ? ['💓', '心臓の声がよく聞こえるタイプ', '脈にさわらなくても、心臓の動きをかなり正確に感じ取れていました。']
            : sc >= 60 ? ['🫀', 'ときどき聞こえるタイプ', '心臓の動きを、ある程度感じ取れていました。多くの人はこのあたりです。']
            : ['🌫️', '体の声は静かなタイプ', 'さわらずに心臓の動きを感じるのは、多くの人にとってむずかしいことです。'];
    const under = order.filter((s, i) => cnt[i] < hr * s / 60).length;
    const rows = order.map((s, i) => `<div><span class="k">${s}秒</span><span class="v">数えた ${cnt[i]} 回 ／ 脈からの目安 ${Math.round(hr * s / 60)} 回</span></div>`).join('');
    NOU.finish({
      label: '心拍の感じ取りの正確さ（目安）', big: sc, unit: ' / 100', emoji: T[0], typeName: T[1], advice: T[2],
      extraHTML: `<div class="syn-rows">${rows}<div><span class="k">脈（1分あたり）</span><span class="v">${Math.round(hr)} 回</span></div></div>${under >= 2 ? '<p style="font-size:14px;margin:6px 0;">実際より少なく数えることが多かったようです。研究でも、このテストでは少なめに数える人が多いと言われています。</p>' : ''}<p style="font-size:12px;color:var(--ink-3);">「脈からの目安」は、最後に測った脈から計算したものです。心拍は時間とともに変わるので、結果は目安です。</p>`,
      share: `心臓の音が分かる？テストやってみた💓 さわらずに数えた心拍の正確さ${sc}/100で「${T[1]}」でした。あなたは体の声が聞こえる？`,
      cardTitle: 'わたしは心臓の音が分かる？', cardLine: `心拍の感じ取り ${sc} / 100（目安）`,
      draw: (x, R) => {
        const cw = (R.w - 2 * 40) / 3, base = R.y + 460;
        order.forEach((s, i) => { const xx = R.x + i * (cw + 40), real = hr * s / 60, mx = Math.max(real, cnt[i]) * 1.15 || 1;
          x.fillStyle = '#2A3C43'; x.beginPath(); x.roundRect(xx, base - 360, cw, 360, 24); x.fill();
          x.fillStyle = '#4FC6B4'; const h = cnt[i] / mx * 340; x.beginPath(); x.roundRect(xx + 16, base - h, cw / 2 - 24, h, 16); x.fill();
          x.fillStyle = '#F5BB5C'; const h2 = real / mx * 340; x.beginPath(); x.roundRect(xx + cw / 2 + 8, base - h2, cw / 2 - 24, h2, 16); x.fill();
          x.textAlign = 'center'; x.fillStyle = '#EEEAE3'; x.font = '800 34px ' + R.F; x.fillText(s + '秒', xx + cw / 2, base + 50); });
        x.font = '700 28px ' + R.F; x.textAlign = 'left'; x.fillStyle = '#4FC6B4'; x.fillText('■ 数えた回数', R.x, R.y + 40); x.fillStyle = '#F5BB5C'; x.fillText('■ 脈からの目安', R.x + 300, R.y + 40);
      },
    });
  }
  function start() { clearTimeout(tm); try { if (!ctx) ctx = new (window.AudioContext || window.webkitAudioContext)(); if (ctx.state === 'suspended') ctx.resume(); } catch (e) { ctx = null; }
    order = [...LEN].sort(() => Math.random() - .5); k = 0; cnt = []; pulse = 0; NOU.startPanels(); ready(); }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "胸や手首にさわらずに、25秒・35秒・45秒（順番はばらばら）のあいだに感じた心拍の回数を数え、最後に30秒間測った脈とくらべるセルフテストです。",
    "article": """
    <h2>体の内側の感覚「内受容感覚」</h2>
    <p>おなかがすいた、のどがかわいた、心臓がドキドキする。こうした<b>体の内側の感覚</b>は「内受容感覚（ないじゅようかんかく）」と呼ばれます。この感覚の鋭さは人によってちがい、気持ちの感じ方との関係がさかんに研究されています。</p>

    <h2>心拍を数えるテストは、40年以上使われてきた</h2>
    <p>内受容感覚を測る方法として有名なのが、<b>脈にさわらずに、決まった時間のあいだに感じた心拍の数を数えてもらう</b>テストです。1981年に発表された「心臓の鼓動の感じ取りと、感情の体験」についての研究で広く知られるようになりました（Schandry 1981）。</p>
    <p>ふつうは25秒・35秒・45秒など長さのちがう時間で数えてもらい、実際の心拍とのずれから、正確さを0〜1の数字で出します。このページの計算も、その考え方にそっています。</p>

    <h2>このテストへの疑問</h2>
    <p>ただし、この方法には疑問も出されています。たとえば、<b>実際に心臓を感じているのではなく、「自分の心拍はだいたいこのくらい」という知識や、時間の感覚から数を見積もっている</b>人が多いのではないか、という指摘です（Desmedt ほか 2018）。また、多くの人が実際より少なく数える傾向があり、点数の多くはその「数えもれ」で決まってしまう、という研究もあります（Zamariola ほか 2018）。</p>
    <p>そのため、このテストの結果は「体の声がどのくらい聞こえるか」の、あくまで目安と考えてください。</p>

    <h2>結果の3つのタイプ</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>正確さ（目安・100点満点）</th></tr>
    <tr><td>💓 心臓の声がよく聞こえるタイプ</td><td>85点以上</td></tr>
    <tr><td>🫀 ときどき聞こえるタイプ</td><td>60〜84点</td></tr>
    <tr><td>🌫️ 体の声は静かなタイプ</td><td>60点未満</td></tr>
    </table>
    </div>
    <p>区切りは、このページで決めた目安です。</p>
""",
    "faq": [
        ("このテストで心臓の病気が分かりますか？", "いいえ。遊びのためのセルフテストで、医療の検査ではありません。胸の痛み・動悸・息苦しさなどがあるときは、すぐに医療機関に相談してください。"),
        ("脈がうまく測れません。", "手首の親指側に、人さし指と中指をそっと当てると見つけやすくなります。首の横に当てる方法もあります。"),
        ("心拍の数を予想して答えてもいいですか？", "このテストは「感じた回数」だけを数えてください。予想で答えると、研究で指摘されている「見積もり」のテストになってしまいます。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Schandry R (1981). Heart beat perception and emotional experience. <i>Psychophysiology</i>, 18(4), 483–488.",
        "Desmedt O, Luminet O, Corneille O (2018). The heartbeat counting task largely involves non-interoceptive processes: Evidence from both the original and an adapted counting task. <i>Biological Psychology</i>.",
        "Zamariola G, Maurage P, Luminet O, Corneille O (2018). Interoceptive accuracy scores from the heartbeat counting task are problematic: Evidence from simple bivariate correlations. <i>Biological Psychology</i>.",
    ],
    "related": [("hsp-shindan", "🌿", "HSP診断（繊細さん）"), ("jikan-kankaku", "⏱️", "時間感覚テスト（目を閉じて30秒）"), ("torihada-test", "🎵", "音楽で鳥肌が立つ？テスト"), ("shinpaku-zone", "❤️", "心拍ゾーン計算")],
}
