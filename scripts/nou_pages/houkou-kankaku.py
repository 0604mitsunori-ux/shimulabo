# -*- coding: utf-8 -*-
# 十人十脳 第20話「方向音痴（頭の中の地図）」と連動（2026-11-05 新規）
PAGE = {
    "slug": "houkou-kankaku",
    "title": "方向音痴テスト｜頭の中で図形を回せる？図形の回転問題と方向感覚の質問で試す｜シミュラボ",
    "desc": "地図をくるくる回さないと読めない？10問の「図形を頭の中で回す問題」と、5つの方向感覚の質問で、あなたの頭の中の地図を試すセルフテスト。回す角度が大きいほど答えるのに時間がかかる、という1971年の有名な研究も解説。診断ではありません。",
    "og_title": "頭の中で図形を回せる？｜方向音痴テスト",
    "og_desc": "図形を回す10問と、方向感覚の5つの質問。あなたの頭の中の地図は？",
    "ld_name": "方向音痴テスト（頭の中で図形を回す）",
    "h1": "方向音痴テスト（頭の中で図形を回せる？）",
    "lead": "地図アプリを見ても、自分がどっちを向いているのか分からない。そんな「方向音痴」の悩みには、頭の中で物の向きを変える力も関わっていると考えられています。図形を頭の中で回す10問と、方向感覚の5つの質問に答えてください。約3分です。",
    "start_h2": "🧭 図形を頭の中で回してね",
    "start_text": "左と右に、同じ形の図形が出ます。右の図形は、左の図形を「回しただけ」？それとも「鏡にうつした形」？なるべく速く、正確に答えてください。",
    "tag": "方向感覚",
    "card_label": "方向音痴テストの結果",
    "card_footer": "頭の中で図形を回せる？ → shimulabo.com",
    "stage_html": """
      <div class="syn-top"><span id="part">回しただけ？鏡うつし？</span><span id="count">1 / 10</span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div id="pair" style="display:flex;justify-content:center;gap:18px;margin:10px auto 14px;"></div>
      <div class="syn-ask" id="q" style="font-size:17px;font-weight:700;color:#EEEAE3;min-height:1.6em;line-height:1.7;"></div>
      <div class="syn-btns" id="opts"></div>
    """,
    "js": r"""
  const $ = NOU.$;
  // 鏡にうつすと回しても重ならない形（5つのマスの形）
  const SH = [[[1,0],[2,0],[0,1],[1,1],[1,2]], [[0,0],[0,1],[0,2],[0,3],[1,3]], [[0,0],[0,1],[1,1],[1,2],[1,3]], [[0,0],[1,0],[0,1],[1,1],[0,2]], [[1,0],[0,1],[1,1],[1,2],[1,3]]];
  const ANG = [0, 45, 90, 135, 180];
  function fig(cells, rot, mirror, color) {
    const xs = cells.map(c => c[0]), ys = cells.map(c => c[1]), cx = (Math.min(...xs) + Math.max(...xs) + 1) / 2 * 24, cy = (Math.min(...ys) + Math.max(...ys) + 1) / 2 * 24;
    const sq = cells.map(([a, b]) => `<rect x="${a * 24}" y="${b * 24}" width="24" height="24" fill="${color}" stroke="#0D1417" stroke-width="2"/>`).join('');
    return `<svg viewBox="-60 -60 120 120" style="width:140px;height:140px;background:#2A3C43;border-radius:14px;"><g transform="rotate(${rot}) scale(${mirror ? -1 : 1},1) translate(${-cx},${-cy})">${sq}</g></svg>`;
  }
  const SQ = [['🗺️', '地図を見るとき、進む向きに地図を回したくなる', true], ['🏙️', '初めての町でも、来た道を戻れる', false], ['🧭', '今いる場所で、だいたいの東西南北が分かる', false],
    ['🚇', '地下鉄の駅から地上に出たとき、どっちを向いているか分かる', false], ['🗣️', '人に道を説明するのが得意だ', false]];
  const O = [['とてもあてはまる', 4], ['ややあてはまる', 3], ['あまりあてはまらない', 2], ['まったくあてはまらない', 1]];
  let trials = [], k = 0, rec = [], sres = [], t0 = 0, phase = 'rot';
  function makeTrials() { trials = []; ANG.forEach(a => [false, true].forEach(m => trials.push({ s: Math.floor(Math.random() * SH.length), base: Math.floor(Math.random() * 8) * 45, a: a * (Math.random() < .5 ? 1 : -1), m }))); trials.sort(() => Math.random() - .5); }
  function showT() { const t = trials[k]; phase = 'rot';
    $('pair').innerHTML = fig(SH[t.s], t.base, false, '#4FC6B4') + fig(SH[t.s], t.base + t.a, t.m, '#4FC6B4');
    $('part').textContent = '回しただけ？鏡うつし？'; $('q').textContent = '右の図形は、左の図形を…'; $('count').textContent = (k + 1) + ' / 10'; $('bar').style.width = (k / 15 * 100) + '%';
    $('opts').className = 'syn-btns'; $('opts').innerHTML = '<button type="button" data-v="0">回しただけ</button><button type="button" data-v="1">鏡にうつした形</button>'; t0 = performance.now(); }
  function showS() { const j = k - 10, [e, q] = SQ[j]; phase = 'self'; $('pair').innerHTML = `<div style="font-size:64px;">${e}</div>`;
    $('part').textContent = '方向感覚の質問'; $('q').textContent = q; $('count').textContent = (j + 1) + ' / 5'; $('bar').style.width = (k / 15 * 100) + '%';
    $('opts').className = 'syn-btns c1'; $('opts').innerHTML = O.map(([s, v]) => `<button type="button" data-v="${v}">${s}</button>`).join(''); }
  $('opts').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; const v = +b.dataset.v;
    if (phase === 'rot') { const t = trials[k]; rec.push({ a: Math.abs(t.a), ok: (v === 1) === t.m, ms: performance.now() - t0 }); }
    else { const rev = SQ[k - 10][2]; sres.push(rev ? 5 - v : v); }
    k++; if (k < 10) showT(); else if (k < 15) showS(); else done(); });
  function done() {
    const r = rec.filter(x => x.ok).length, d = sres.reduce((a, b) => a + b, 0);   // 図形0〜10・方向感覚5〜20
    const g = [[0, 45], [90, 135], [180]].map(as => { const v = rec.filter(x => x.ok && as.includes(x.a)).map(x => x.ms); return v.length ? Math.round(v.reduce((a, b) => a + b, 0) / v.length / 100) / 10 : null; });
    const R8 = r >= 8, D = d >= 14;
    const T = R8 && D ? ['🗺️', '頭の中に地図があるタイプ', '図形を回すのも、道を覚えるのも自信があるタイプです。']
            : R8 ? ['🧩', '図形は得意・道はちょっと苦手タイプ', '図形を頭の中で回すのは得意でした。町の中で道を覚える力は、図形を回す力とまったく同じではないと考えられています。']
            : D ? ['🚶', '図形は苦手・道は得意タイプ', '図形の問題はむずかしく感じても、町の中では目印などを使って道を覚えているのかもしれません。']
            : ['📱', '地図アプリと仲よしタイプ', '図形を回す問題も、道を覚えることも苦手に感じやすいタイプです。目印を声に出して覚えると、道を覚えやすくなります。'];
    const tl = ['小さい回転（0〜45度）', '中くらい（90〜135度）', '大きい回転（180度）'];
    NOU.finish({
      label: '図形を回す問題の正解（10問中）', big: r, unit: ' / 10 問', emoji: T[0], typeName: T[1], advice: T[2],
      extraHTML: `<div class="syn-rows">${g.map((v, i) => `<div><span class="k">${tl[i]}で答えるまでの時間</span><span class="v">${v === null ? '—' : v + ' 秒'}</span></div>`).join('')}<div><span class="k">方向感覚の自己評価</span><span class="v">${d} / 20 点</span></div></div><p style="font-size:12px;color:var(--ink-3);">時間は、正しく答えた問題だけの平均です。多くの人は、回す角度が大きいほど時間がかかります。</p>`,
      share: `方向音痴テストやってみた🧭 図形を回す問題${r}/10問・方向感覚${d}/20点で「${T[1]}」でした。あなたは頭の中で図形を回せる？`,
      cardTitle: 'わたしの頭の中の地図', cardLine: `図形 ${r}/10問・方向感覚 ${d}/20点`,
      draw: (x, R) => {
        const vals = g.map(v => v || 0), mx = Math.max(3, ...vals), cw = (R.w - 2 * 40) / 3, base = R.y + 440;
        ['0〜45°', '90〜135°', '180°'].forEach((lab, i) => { const xx = R.x + i * (cw + 40), h = vals[i] ? 40 + vals[i] / mx * 320 : 0;
          x.fillStyle = '#2A3C43'; x.beginPath(); x.roundRect(xx, base - 360, cw, 360, 24); x.fill();
          if (h) { x.fillStyle = '#4FC6B4'; x.beginPath(); x.roundRect(xx, base - h, cw, h, 24); x.fill(); }
          x.textAlign = 'center'; x.fillStyle = '#EEEAE3'; x.font = '900 44px ' + R.F; x.fillText(g[i] === null ? '—' : g[i] + '秒', xx + cw / 2, base - 380);
          x.font = '800 36px ' + R.F; x.fillText(lab, xx + cw / 2, base + 50); });
      },
    });
  }
  function start() { makeTrials(); k = 0; rec = []; sres = []; NOU.startPanels(); showT(); }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "同じ形の図形2つを見て、右が左を「回しただけ」か「鏡にうつした形」かを答える10問（回す角度は0〜180度）と、方向感覚についての5つの質問に答えるセルフテストです。",
    "article": """
    <h2>頭の中で図形を回すと、時間がかかる</h2>
    <p>1971年、アメリカの研究者シェパードとメッツラーは、向きのちがう2つの立体の絵を見せて、「同じ形か、鏡にうつした形か」を答えてもらう実験をしました。すると、<b>2つの絵の向きのちがいが大きいほど、答えるまでの時間がまっすぐ長くなる</b>ことが分かりました（Shepard・Metzler 1971）。</p>
    <p>まるで、頭の中で図形を少しずつ回しているかのような結果です。これは「心的回転（メンタル・ローテーション）」と呼ばれ、今もいろいろな研究で使われています。</p>
    <p>このテストの結果にも、回す角度ごとに答えるまでの時間を出しています。角度が大きいほど時間が長くなっていたら、あなたの頭の中でも図形が回っていたのかもしれません。</p>

    <h2>「方向感覚」は、自分の答えでも測れる</h2>
    <p>アメリカの研究チームは2002年、方向感覚を自分で答える<b>15問の質問票</b>を作りました（Hegarty ほか 2002）。この質問票の点数は、実際の建物や町の中で道を覚えたり、見えない場所の方角を指さしたりする課題の成績と関係していたと報告されています。</p>
    <p>つまり「自分は方向音痴だ」という感覚は、ある程度は当たっているということです。このページの5つの質問は、その考え方をもとに作った簡単なものです。</p>

    <h2>図形の力と、道を覚える力は同じ？</h2>
    <p>紙や画面の上で図形を回す力と、町の中で道を覚える力は、関係はあっても<b>まったく同じではない</b>と考えられています。町の中では、目印・歩いた距離・曲がった向きなど、いろいろな手がかりを使っているからです。</p>
    <p>そのためこのテストでは、図形の問題と方向感覚の質問を分けて出し、2つを組み合わせて4つのタイプにしています。</p>

    <h2>結果の4つのタイプ</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>図形の問題</th><th>方向感覚の質問</th></tr>
    <tr><td>🗺️ 頭の中に地図があるタイプ</td><td>8問以上</td><td>14点以上</td></tr>
    <tr><td>🧩 図形は得意・道はちょっと苦手タイプ</td><td>8問以上</td><td>13点以下</td></tr>
    <tr><td>🚶 図形は苦手・道は得意タイプ</td><td>7問以下</td><td>14点以上</td></tr>
    <tr><td>📱 地図アプリと仲よしタイプ</td><td>7問以下</td><td>13点以下</td></tr>
    </table>
    </div>
""",
    "faq": [
        ("方向音痴は直りますか？", "目印を意識して歩く、来た道をふり返って見ておく、などの工夫で道を覚えやすくなることがあります。"),
        ("スマホと大きな画面で結果は変わりますか？", "図形の大きさで答えやすさが変わることがあります。くらべるときは、同じ画面で試してください。"),
        ("研究の質問票と同じですか？", "いいえ。このページの問題と質問は、研究の考え方をもとに作った簡単なもので、研究で使われるテストそのものではありません。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Shepard RN, Metzler J (1971). Mental rotation of three-dimensional objects. <i>Science</i>, 171(3972), 701–703.",
        "Hegarty M, Richardson AE, Montello DR, Lovelace K, Subbiah I (2002). Development of a self-report measure of environmental spatial ability. <i>Intelligence</i>, 30(5), 425–447.",
    ],
    "related": [("shikou-type", "🧠", "絵で考える人・言葉で考える人テスト"), ("hidarikiki", "✋", "利き手・利き目・利き足チェック"), ("sakushi-kaiten", "💃", "回るダンサーの錯視テスト"), ("iq-test", "🧩", "IQテスト")],
}
