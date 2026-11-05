# -*- coding: utf-8 -*-
# 十人十脳 第22話「数の感じ方」と連動（2026-11-05 新規）。shunkan-kioku（瞬間記憶）とは別のテーマ
PAGE = {
    "slug": "kazu-shunkan",
    "title": "数の瞬間テスト｜一瞬だけ出る点、いくつ見えた？パッと数が分かる上限を試す｜シミュラボ",
    "desc": "0.2秒だけ出る点の数を当てるセルフテスト。数えなくてもパッと分かるのは何個まで？4個くらいまでは一瞬で分かり、それより多いと急にまちがえやすくなる「サビタイジング」という頭のしくみを解説。診断ではありません。",
    "og_title": "一瞬だけ出る点、いくつ見えた？｜数の瞬間テスト",
    "og_desc": "0.2秒だけの点の数を当てる。あなたがパッと分かるのは何個まで？",
    "ld_name": "数の瞬間テスト（一瞬で数が分かる？）",
    "h1": "数の瞬間テスト（一瞬だけ出る点、いくつ見えた？）",
    "lead": "サイコロの目やお皿のおかしの数は、数えなくてもパッと分かります。でも、点が多くなると急に分からなくなります。0.2秒だけ出る点の数を当ててください。12問、約1分です。",
    "start_h2": "🔢 点はいくつ？",
    "start_text": "黒い画面に、白い点が一瞬だけ出ます。数えるひまはありません。パッと見て「いくつだったか」を選んでください。",
    "tag": "数の瞬間",
    "card_label": "数の瞬間テストの結果",
    "card_footer": "一瞬で数が分かるのは何個まで？ → shimulabo.com",
    "stage_html": """
      <div class="syn-top"><span id="part">点はいくつ？</span><span id="count">1 / 12</span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div id="box" style="position:relative;width:260px;height:260px;margin:10px auto 14px;border-radius:16px;background:#0D1417;"></div>
      <div class="syn-btns" id="opts" style="grid-template-columns:repeat(3,1fr);"></div>
    """,
    "js": r"""
  const $ = NOU.$;
  const SHOW = 200;   // 点を見せる時間（ミリ秒）
  let list = [], k = 0, ans = [];
  function dots(n) {   // 重ならないように、ばらばらの位置に置く
    const p = []; let g = 0; while (p.length < n && g++ < 5000) { const x = 30 + Math.random() * 200, y = 30 + Math.random() * 200; if (p.every(q => Math.hypot(q[0] - x, q[1] - y) > 40)) p.push([x, y]); }
    return p.map(([x, y]) => `<span style="position:absolute;left:${x - 11}px;top:${y - 11}px;width:22px;height:22px;border-radius:50%;background:#EEEAE3;"></span>`).join('');
  }
  const mask = '<div style="position:absolute;inset:0;border-radius:16px;background:repeating-linear-gradient(45deg,#2A3C43 0 6px,#0D1417 6px 12px);"></div>';
  function show() {
    $('count').textContent = (k + 1) + ' / 12'; $('bar').style.width = (k / 12 * 100) + '%'; $('opts').innerHTML = ''; $('part').textContent = 'よく見て…';
    $('box').innerHTML = '<div style="position:absolute;left:50%;top:50%;width:14px;height:14px;margin:-7px;border-radius:50%;background:#4FC6B4;"></div>';
    setTimeout(() => { $('box').innerHTML = dots(list[k]); setTimeout(() => { $('box').innerHTML = mask; $('part').textContent = '点はいくつ？';
      $('opts').innerHTML = Array.from({ length: 9 }, (_, i) => `<button type="button" data-v="${i + 1}">${i + 1}</button>`).join(''); }, SHOW); }, 700);
  }
  $('opts').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; ans.push(+b.dataset.v); k++; if (k < 12) show(); else done(); });
  function done() {
    const ok = n => list.map((v, i) => v === n ? ans[i] === v : null).filter(v => v !== null);
    let lim = 0; for (let n = 1; n <= 9; n++) { if (ok(n).every(Boolean)) lim = n; else break; }   // ここまでは全部正解、という数
    const right = list.filter((v, i) => ans[i] === v).length;
    const T = lim >= 5 ? ['🦉', 'パッと見で数が見えるタイプ', `${lim}個まで、一瞬で正しく分かりました。多くの人が一瞬で分かるのは4個くらいまでです。`]
            : lim >= 4 ? ['🙂', 'ふつうに見えるタイプ', '4個までは一瞬で分かりました。研究で言われる「パッと分かる数」とほぼ同じです。']
            : ['🔍', '数えて確かめるタイプ', `一瞬で分かったのは${lim}個まででした。0.2秒はとても短いので、まばたきなどでも結果が変わります。`];
    const rows = Array.from({ length: 9 }, (_, i) => { const r = ok(i + 1); return `<span style="display:inline-block;width:10.5%;margin:0 .5%;text-align:center;"><b style="display:block;height:30px;border-radius:6px;line-height:30px;background:${r.every(Boolean) ? '#4FC6B4' : '#F5BB5C'};color:#0D1417;">${r.every(Boolean) ? '○' : '×'}</b><small>${i + 1}個</small></span>`; }).join('');
    NOU.finish({
      label: '一瞬で正しく分かった数の上限', big: lim, unit: ' 個まで', emoji: T[0], typeName: T[1], advice: T[2],
      extraHTML: `<div style="margin:8px 0;">${rows}</div><p style="font-size:14px;margin:6px 0;">12問中 <b>${right}問</b> 正解でした。</p><p style="font-size:12px;color:var(--ink-3);">点の数は1〜9個で、4・6・8個は2回ずつ出ています。○は、その数がすべて正解だったしるしです。</p>`,
      share: `数の瞬間テストやってみた🔢 一瞬で分かったのは${lim}個までで「${T[1]}」でした。0.2秒だけの点、あなたは何個まで分かる？`,
      cardTitle: 'わたしがパッと分かる数', cardLine: `一瞬で分かるのは ${lim}個まで（12問中${right}問正解）`,
      draw: (x, R) => {
        const cw = (R.w - 8 * 16) / 9;
        for (let i = 0; i < 9; i++) { const r = ok(i + 1).every(Boolean), xx = R.x + i * (cw + 16), y = R.y + 120;
          x.fillStyle = r ? '#4FC6B4' : '#2A3C43'; x.beginPath(); x.roundRect(xx, y, cw, 260, 18); x.fill();
          x.fillStyle = r ? '#0D1417' : '#8D9BA1'; x.textAlign = 'center'; x.font = '900 56px ' + R.F; x.fillText(r ? '○' : '×', xx + cw / 2, y + 150);
          x.fillStyle = '#EEEAE3'; x.font = '800 32px ' + R.F; x.fillText((i + 1) + '個', xx + cw / 2, y + 320); }
      },
    });
  }
  function start() { list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 4, 6, 8].sort(() => Math.random() - .5); k = 0; ans = []; NOU.startPanels(); show(); }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "1〜9個の白い点を0.2秒だけ見せて、すぐにしまもようで隠し、点がいくつだったかを答えるセルフテストです。",
    "article": """
    <h2>数えなくても分かる数「サビタイジング」</h2>
    <p>点が2つや3つなら、私たちは数えなくても一瞬で「3つ」と分かります。このしくみは<b>「サビタイジング」</b>と呼ばれます。1949年の研究で名づけられた言葉で、ラテン語の「突然の」という言葉から来ています（Kaufman ほか 1949）。</p>

    <h2>パッと分かるのは、4個くらいまで</h2>
    <p>その後の研究で、ばらばらに置かれた点の場合、<b>1〜4個くらいまで</b>は、速く、ほとんどまちがえずに分かることが確かめられました（Trick・Pylyshyn 1994）。それより多くなると、1個ふえるごとに答えるまでの時間がのびていきます。つまり、5個をこえると、頭の中で「数える」作業が始まるのです。</p>
    <p>このテストでは、点を0.2秒しか見せないので、数えるひまがありません。そのため、パッと分かる範囲をこえると、急にまちがいがふえます。</p>

    <h2>サイコロの目は、なぜすぐ分かる？</h2>
    <p>サイコロの6の目は、点が6個あっても一瞬で分かります。これは、見慣れた形として覚えているからです。このテストでは、点の位置を毎回ばらばらにして、形で覚えられないようにしています。</p>

    <h2>結果の3つのタイプ</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>一瞬で正しく分かった上限</th></tr>
    <tr><td>🦉 パッと見で数が見えるタイプ</td><td>5個以上</td></tr>
    <tr><td>🙂 ふつうに見えるタイプ</td><td>4個</td></tr>
    <tr><td>🔍 数えて確かめるタイプ</td><td>3個以下</td></tr>
    </table>
    </div>
    <p>「上限」は、1個から順に見て、その数までの問題が全部正解だった数です。</p>
""",
    "faq": [
        ("点が見えないうちに消えました。", "0.2秒はとても短い時間です。画面の真ん中の緑の点を見ながら待つと、点が見やすくなります。"),
        ("何回もやると上達しますか？", "慣れると少し答えやすくなることはありますが、パッと分かる数の範囲そのものは、大きくは変わらないと考えられています。"),
        ("このテストで算数の得意・苦手が分かりますか？", "いいえ。遊びのためのセルフテストで、検査や診断ではありません。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Kaufman EL, Lord MW, Reese TW, Volkmann J (1949). The discrimination of visual number. <i>American Journal of Psychology</i>, 62(4), 498–525.",
        "Trick LM, Pylyshyn ZW (1994). Why are small and large numbers enumerated differently? A limited-capacity preattentive stage in vision. <i>Psychological Review</i>, 101(1), 80–102.",
    ],
    "related": [("shunkan-kioku", "⚡", "瞬間記憶テスト"), ("suuji-kioku", "🔢", "数字記憶テスト"), ("jikan-kankaku", "⏱️", "時間感覚テスト（目を閉じて30秒）"), ("yomu-hayasa", "📖", "読む速さテスト")],
}
