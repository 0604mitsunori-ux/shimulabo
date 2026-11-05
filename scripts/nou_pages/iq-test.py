# -*- coding: utf-8 -*-
# 十人十脳 第28話「頭の良さの見え方（IQ）」と連動。既存の「IQテスト（簡易版）」を同じURLのまま作り直した（2026-11-05）。IQの数字は出さない
PAGE = {
    "slug": "iq-test",
    "title": "IQテスト｜パターン問題8問と「見ない力」テスト。IQが高い人は何を見ていない？｜シミュラボ",
    "desc": "数や形の決まりを見つけるパターン問題8問と、一瞬だけ動くしま模様の向きを当てる「見ない力」テスト。IQテストの点が高い人ほど、大きな模様の動きを見分けにくかったという意外な研究や、IQテストの点が世代ごとに上がってきた話も解説。IQの数字は出しません。診断ではありません。",
    "og_title": "IQが高い人は、何を「見ていない」のか｜IQテスト",
    "og_desc": "パターン問題8問と、一瞬だけ動くしま模様のテスト。",
    "ld_name": "IQテスト（パターン問題と「見ない力」）",
    "h1": "IQテスト（IQが高い人は、何を「見ていない」のか）",
    "lead": "頭のよさというと、「たくさんのことに気づく力」を思い浮かべるかもしれません。ところが研究では、IQテストの点が高い人ほど、ある種のものを「見ない」ことが分かってきました。パターン問題8問と、しま模様の動きを当てる16問に答えてください。約4分です。",
    "start_h2": "🧩 2つのテストに答えてね",
    "start_text": "前半は、数や形の決まりを見つけるパターン問題8問です。後半は、一瞬だけ動くしま模様が「左」と「右」のどちらに動いたかを当てる16問です。後半はなるべく明るく、画面に近づきすぎずに見てください。",
    "tag": "IQテスト",
    "card_label": "IQテストの結果",
    "card_footer": "IQが高い人は何を見ていない？ → shimulabo.com",
    "stage_html": """
      <div class="syn-top"><span id="part">パターン問題</span><span id="count">1 / 8</span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div class="syn-ask" id="q" style="font-size:18px;font-weight:700;color:#EEEAE3;min-height:3.4em;line-height:1.7;"></div>
      <canvas id="mv" width="300" height="300" style="display:block;width:300px;max-width:100%;margin:6px auto 10px;border-radius:12px;background:#808080;" hidden></canvas>
      <div class="syn-btns" id="opts"></div>
    """,
    "js": r"""
  const $ = NOU.$;
  // 前半：パターン問題（このページで作った問題）
  const PQ = [
    ['3, 6, 11, 18, 27, ？', ['34', '36', '38', '40'], 2],
    ['2, 3, 5, 7, 11, ？', ['12', '13', '14', '15'], 1],
    ['7, 10, 8, 11, 9, 12, ？', ['10', '13', '14', '15'], 0],
    ['A, C, F, J, ？', ['M', 'N', 'O', 'P'], 2],
    ['△○□ ／ ○□△ ／ □△？　の「？」は？', ['△', '○', '□', '☆'], 1],
    ['AさんはBさんより年上。CさんはAさんより年上。DさんはBさんより年下。いちばん年下は？', ['Aさん', 'Bさん', 'Cさん', 'Dさん'], 3],
    ['1時に1回、2時に2回…と、時刻の数だけ鳴る時計。12時から3時まで（12時と3時もふくむ）に、全部で何回鳴る？', ['6回', '15回', '18回', '21回'], 2],
    ['1, 4, 9, 16, 25, ？', ['30', '35', '36', '49'], 2],
  ];
  // 後半：一瞬だけ動くしま模様（小さい・大きい）。研究で使われる課題の考え方をもとに、このページで作ったもの
  const PER = 24, SPD = 0.12, DUR = 90;   // しまの間隔(px)・速さ(px/ミリ秒)・見せる時間(ミリ秒)
  let mt = [], k = 0, pr = [], mr = [], img = null, busy = false;
  function grating(rad, dir, t) {
    const cv = $('mv'), x = cv.getContext('2d'), W = cv.width, c = W / 2; if (!img) img = x.createImageData(W, W); const d = img.data, edge = rad > 60 ? 24 : 8, ph = dir * SPD * t;
    for (let yy = 0; yy < W; yy++) for (let xx = 0; xx < W; xx++) { const r = Math.hypot(xx - c, yy - c), i = (yy * W + xx) * 4;
      let w = r > rad ? 0 : r > rad - edge ? 0.5 + 0.5 * Math.cos(Math.PI * (r - rad + edge) / edge) : 1;
      const v = 128 + 120 * w * Math.cos(2 * Math.PI * (xx - ph) / PER); d[i] = d[i + 1] = d[i + 2] = v; d[i + 3] = 255; }
    x.putImageData(img, 0, 0);
  }
  function gray(dot) { const x = $('mv').getContext('2d'); x.fillStyle = '#808080'; x.fillRect(0, 0, 300, 300); if (dot) { x.fillStyle = '#111'; x.beginPath(); x.arc(150, 150, 4, 0, Math.PI * 2); x.fill(); } }
  function showP() { const [q, o] = PQ[k]; $('part').textContent = 'パターン問題'; $('count').textContent = (k + 1) + ' / 8'; $('bar').style.width = (k / 24 * 100) + '%'; $('mv').hidden = true;
    $('q').textContent = q; $('opts').style.gridTemplateColumns = 'repeat(2,1fr)'; $('opts').innerHTML = o.map((t, i) => `<button type="button" data-v="${i}">${t}</button>`).join(''); }
  function showM() {
    const j = k - 8, t = mt[j]; busy = true; $('part').textContent = '左？右？'; $('count').textContent = (j + 1) + ' / 16'; $('bar').style.width = (k / 24 * 100) + '%'; $('mv').hidden = false;
    $('q').textContent = '真ん中の点を見ていてね'; $('opts').innerHTML = ''; gray(true);
    setTimeout(() => { let t0 = 0; const step = now => { if (!t0) t0 = now; const el = now - t0; if (el < DUR) { grating(t.big ? 140 : 32, t.dir, el); requestAnimationFrame(step); } else { gray(false); ask(); } }; requestAnimationFrame(step); }, 700);
  }
  function ask() { busy = false; $('q').textContent = 'しま模様は、どっちに動いた？'; $('opts').style.gridTemplateColumns = 'repeat(2,1fr)'; $('opts').innerHTML = '<button type="button" data-v="-1">← 左</button><button type="button" data-v="1">右 →</button>'; }
  $('opts').addEventListener('click', e => { const b = e.target.closest('button'); if (!b || busy) return; const v = +b.dataset.v;
    if (k < 8) pr.push(v === PQ[k][2]); else mr.push({ big: mt[k - 8].big, ok: v === mt[k - 8].dir });
    k++; if (k < 8) showP(); else if (k < 24) showM(); else done(); });
  function done() {
    const p = pr.filter(Boolean).length, sm = mr.filter(r => !r.big && r.ok).length, lg = mr.filter(r => r.big && r.ok).length;
    const T = p >= 7 ? ['🧠', 'パターン発見が得意なタイプ', '数や形の決まりを、すばやく見つけられるタイプです。'] : p >= 4 ? ['🙂', 'しっかり考えるタイプ', '多くの問題で決まりを見つけられました。'] : ['🐢', 'じっくり型タイプ', '今回はむずかしい問題が多かったようです。時間をかければ解ける問題もあるかもしれません。'];
    const mv = sm > lg ? `大きい模様のほうが、動きが分かりにくかったようです（小さい模様 ${sm}/8・大きい模様 ${lg}/8）。あなたの脳が、背景のような大きな動きを自動でおさえているしるしかもしれません。`
             : sm === lg ? `小さい模様と大きい模様で、正解の数が同じでした（どちらも ${sm}/8）。` : `大きい模様のほうが、動きが分かりやすかったようです（小さい模様 ${sm}/8・大きい模様 ${lg}/8）。画面の大きさや明るさでも結果は変わります。`;
    NOU.finish({
      label: 'パターン問題の正解', big: p, unit: ' / 8 問', emoji: T[0], typeName: T[1], advice: T[2],
      extraHTML: `<p style="font-size:14px;margin:6px 0;">🌀 ${mv}</p><div class="syn-rows"><div><span class="k">パターン問題</span><span class="v">${p} / 8 問</span></div><div><span class="k">小さいしま模様の向き</span><span class="v">${sm} / 8 問</span></div><div><span class="k">大きいしま模様の向き</span><span class="v">${lg} / 8 問</span></div></div><p style="font-size:12px;color:var(--ink-3);">このテストからIQの数字は出しません。本当のIQは、専門家が決まった手順で行う検査で測ります。</p>`,
      share: `IQテスト（パターン問題と「見ない力」）やってみた🧩 パターン問題${p}/8問、しま模様は小さい${sm}/8・大きい${lg}/8でした。IQが高い人は、何を見ていない？`,
      cardTitle: 'わたしのパターン力と「見ない力」', cardLine: `パターン ${p}/8・しま模様 小${sm}/8・大${lg}/8`,
      draw: (x, R) => {
        for (let i = 0; i < 8; i++) { x.fillStyle = i < p ? '#4FC6B4' : '#2A3C43'; x.beginPath(); x.arc(R.x + 58 + i * ((R.w - 116) / 7), R.y + 90, 44, 0, Math.PI * 2); x.fill(); }
        x.fillStyle = '#EEEAE3'; x.textAlign = 'left'; x.font = '800 36px ' + R.F; x.fillText('パターン問題', R.x, R.y + 20);
        [['小さいしま模様', sm], ['大きいしま模様', lg]].forEach(([n, v], i) => { const y = R.y + 230 + i * 150;
          x.fillStyle = '#EEEAE3'; x.textAlign = 'left'; x.font = '800 36px ' + R.F; x.fillText(n, R.x, y);
          x.fillStyle = '#2A3C43'; x.beginPath(); x.roundRect(R.x, y + 24, R.w, 56, 28); x.fill();
          x.fillStyle = i ? '#F5BB5C' : '#4FC6B4'; x.beginPath(); x.roundRect(R.x, y + 24, Math.max(56, R.w * v / 8), 56, 28); x.fill();
          x.fillStyle = '#EEEAE3'; x.textAlign = 'right'; x.font = '900 36px ' + R.F; x.fillText(v + ' / 8', R.x + R.w, y); });
      },
    });
  }
  function start() { mt = []; for (let i = 0; i < 16; i++) mt.push({ big: i % 2 === 1, dir: Math.random() < .5 ? -1 : 1 }); mt.sort(() => Math.random() - .5);
    k = 0; pr = []; mr = []; NOU.startPanels(); showP(); }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "数・文字・形の決まりを見つけるパターン問題8問と、小さい・大きいしま模様を約0.09秒だけ動かして、左右どちらに動いたかを答える16問のセルフテストです。問題はこのページで作っています。IQの数字は出しません。",
    "article": """
    <h2>IQが高い人は「見ない」のが上手？</h2>
    <p>アメリカの研究チームは、画面に一瞬だけ動くしま模様を出して、左右どちらに動いたかを答えてもらう実験をしました（Melnick ほか 2013）。しま模様には、小さいものと大きいものがありました。</p>
    <p>すると、IQテストの点が高い人ほど、<b>小さい模様の動きはすばやく見分けられる</b>一方で、<b>大きい模様の動きは見分けにくい</b>という、強い関係が見られました。</p>
    <p>大きく動く模様は、私たちのまわりでは「背景」のようなものです。研究チームは、頭のよさには、<b>大事なものをすばやくとらえる力</b>だけでなく、<b>背景のようなあまり大事でない情報をおさえる力</b>も関わっているのではないかと考えました。</p>

    <h2>このテストの後半のしくみ</h2>
    <p>後半では、小さいしま模様と大きいしま模様を、約0.09秒だけ動かしています。多くの人は、大きい模様のほうが動きの向きが分かりにくく感じます。研究と同じしくみを、画面で体験できるようにしたものです。</p>
    <p>ただし、画面の大きさ・明るさ・見る距離で結果は大きく変わります。このテストの結果から、あなたのIQは分かりません。</p>

    <h2>IQテストの点は、世代ごとに上がってきた</h2>
    <p>14の国のIQテストの記録を調べた研究では、<b>1世代のあいだに、テストの点が大きく上がっていた</b>ことが分かりました（Flynn 1987）。これは「フリン効果」と呼ばれています。</p>
    <p>そんなに短いあいだに、人の頭が生まれつき変わったとは考えにくいため、教育や暮らしの変化などが関わっていると考えられています。IQテストの点は、育った環境にも左右されるのです。</p>

    <h2>結果の見方</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>パターン問題の正解</th></tr>
    <tr><td>🧠 パターン発見が得意なタイプ</td><td>7問以上</td></tr>
    <tr><td>🙂 しっかり考えるタイプ</td><td>4〜6問</td></tr>
    <tr><td>🐢 じっくり型タイプ</td><td>3問以下</td></tr>
    </table>
    </div>
    <p>区切りは、このページで決めた目安です。点数で人のよしあしが決まるものではありません。</p>
""",
    "faq": [
        ("このテストでIQは分かりますか？", "いいえ。このテストからIQの数字は出しません。本当のIQは、専門家が決まった手順で行う検査で測ります。"),
        ("しま模様がよく見えませんでした。", "画面を明るくして、まわりを少し暗くすると見やすくなります。とても短い時間なので、まばたきにも気をつけてください。"),
        ("点が低かったのですが、大丈夫ですか？", "このテストは遊びのためのもので、頭のよさを決めるものではありません。その日の体調や集中でも結果は変わります。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Melnick MD, Harrison BR, Park S, Bennetto L, Tadin D (2013). A strong interactive link between sensory discriminations and intelligence. <i>Current Biology</i>, 23(11), 1013–1017.",
        "Flynn JR (1987). Massive IQ gains in 14 nations: What IQ tests really measure. <i>Psychological Bulletin</i>, 101(2), 171–191.",
    ],
    "related": [("dunning-kruger", "🤔", "ダニング＝クルーガー効果テスト"), ("houkou-kankaku", "🧭", "方向音痴テスト（頭の中で図形を回せる？）"), ("kazu-shunkan", "🔢", "数の瞬間テスト（一瞬で数が分かる？）"), ("shikou-type", "🧠", "考え方のタイプ診断")],
}
