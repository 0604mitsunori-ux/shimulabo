# -*- coding: utf-8 -*-
# 十人十脳 第9話「錯視（どちら回りに見える？）」と連動（2026-11-05 新規）
PAGE = {
    "slug": "sakushi-kaiten",
    "title": "回転の錯視テスト｜この玉、どちら回りに見える？途中で向きが切りかわる不思議な錯覚｜シミュラボ",
    "desc": "画面の中で回る、点でできた玉。右回りに見えますか？左回りに見えますか？実はこの玉には、回る向きの手がかりがありません。見え方が途中で切りかわる「多義的な回転」の錯視を、30秒で試すセルフテスト。診断ではありません。",
    "og_title": "この玉、どちら回りに見える？｜回転の錯視テスト",
    "og_desc": "回る向きの手がかりがない玉。あなたの頭は、どちら回りに決める？",
    "ld_name": "回転の錯視テスト（どちら回りに見える？）",
    "h1": "回転の錯視テスト（この玉、どちら回りに見える？）",
    "lead": "点でできた玉が、くるくる回ります。手前の点が右へ動いて見えますか？左へ動いて見えますか？実はこの玉には、<b>どちら回りかを決める手がかりが入っていません</b>。決めているのは、あなたの頭のほうです。30秒間、見え方が変わるたびにボタンを押してください。",
    "start_h2": "🌀 30秒、玉を見ていてね",
    "start_text": "手前の点が「右へ動く」ように見えたら右のボタン、「左へ動く」ように見えたら左のボタンを押してください。途中で見え方が変わったら、そのたびに押し直します。",
    "tag": "錯視",
    "card_label": "回転の錯視テストの結果",
    "card_footer": "この玉、どちら回りに見える？ → shimulabo.com",
    "stage_html": """
      <div class="syn-top"><span id="now">見え方を押してね</span><span id="count">30 秒</span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <canvas id="ball" width="600" height="600" style="width:100%;max-width:340px;display:block;margin:6px auto 10px;"></canvas>
      <div class="syn-btns" id="opts"><button type="button" data-v="L">← 手前が左へ</button><button type="button" data-v="R">手前が右へ →</button></div>
      <p class="syn-note">見え方が変わったら、そのたびに押し直してね。どちらにも見えないときは押さなくてOK。</p>
    """,
    "js": r"""
  const $ = NOU.$;
  // 球の表面の点を「正面からまっすぐ」映す（遠近・明るさの差なし）＝回る向きの手がかりがない
  const P = Array.from({ length: 420 }, () => { const u = Math.random() * 2 - 1, th = Math.random() * Math.PI * 2; return [Math.sqrt(1 - u * u) * Math.cos(th), u, Math.sqrt(1 - u * u) * Math.sin(th)]; });
  let raf = 0, t0 = 0, log = [], cur = null, timer = 0;
  function draw(t) {
    const c = $('ball'), x = c.getContext('2d'), a = t / 1000 * 1.2;
    x.fillStyle = '#0D1417'; x.fillRect(0, 0, 600, 600); x.fillStyle = '#EEEAE3';
    for (const [px, py, pz] of P) { const X = px * Math.cos(a) + pz * Math.sin(a); x.beginPath(); x.arc(300 + X * 240, 300 - py * 240, 4, 0, Math.PI * 2); x.fill(); }
    raf = requestAnimationFrame(draw);
  }
  function tick() {
    const s = (performance.now() - t0) / 1000; $('count').textContent = Math.max(0, Math.ceil(30 - s)) + ' 秒'; $('bar').style.width = Math.min(100, s / 30 * 100) + '%';
    if (s >= 30) done();
  }
  $('opts').addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return; const v = b.dataset.v;
    if (v !== cur) { log.push([(performance.now() - t0) / 1000, v]); cur = v; }
    $('now').textContent = v === 'R' ? '手前が右へ動いて見えている' : '手前が左へ動いて見えている';
    [...$('opts').children].forEach(x => x.style.borderColor = x === b ? '#4FC6B4' : '#2A3C43');
  });
  function done() {
    cancelAnimationFrame(raf); clearInterval(timer);
    const sw = Math.max(0, log.length - 1), first = log[0] ? log[0][1] : null;
    const T = !first ? ['❔', 'どちらにも見えなかったタイプ', '回る向きが決まらないまま30秒がたちました。もう一度、玉の真ん中あたりをぼんやり見てみてください。']
            : sw === 0 ? ['🔒', 'ずっと同じ向きに見えるタイプ', '30秒のあいだ、最初に見えた向きのままでした。手がかりがなくても、頭が一度決めた向きを守っていたようです。']
            : sw <= 3 ? ['🔄', 'ときどき切りかわるタイプ', `30秒のあいだに${sw}回、回る向きが切りかわりました。`]
            : ['🌀', 'よく切りかわるタイプ', `30秒のあいだに${sw}回も、回る向きが切りかわりました。見え方の切りかわりやすさは、人によってかなりちがいます。`];
    // 時間ごとの向きの帯
    const seg = log.map((l, i) => [l[0], (log[i + 1] || [30])[0], l[1]]);
    const bar = seg.map(([a, b, v]) => `<span style="display:inline-block;height:14px;width:${(b - a) / 30 * 100}%;background:${v === 'R' ? 'var(--teal)' : '#f5bb5c'}"></span>`).join('');
    NOU.finish({
      label: '30秒のあいだに、向きが切りかわった回数', big: sw, unit: ' 回', emoji: T[0], typeName: T[1], advice: T[2],
      extraHTML: first ? `<p style="font-size:13px;margin:6px 0;">最初に見えた向き：<b>${first === 'R' ? '手前が右へ' : '手前が左へ'}</b></p><div style="display:flex;border-radius:7px;overflow:hidden;background:var(--line-2);">${bar}</div><p style="font-size:12px;color:var(--ink-3);margin-top:4px;">緑＝手前が右へ・黄＝手前が左へ（左から右へ30秒）</p>` : '',
      share: `回転の錯視テストやってみた🌀 最初は「${first === 'R' ? '手前が右へ' : first ? '手前が左へ' : 'どちらでもない'}」に見えて、30秒で${sw}回切りかわった「${T[1]}」でした。あなたにはどちら回りに見える？`,
      cardTitle: 'わたしの頭が決めた回る向き', cardLine: `30秒で ${sw}回 切りかわった`,
      draw: (x, R) => {
        const y = R.y + 200, h = 110;
        x.fillStyle = '#2A3C43'; x.beginPath(); x.roundRect(R.x, y, R.w, h, 20); x.fill();
        seg.forEach(([a, b, v]) => { x.fillStyle = v === 'R' ? '#4FC6B4' : '#F5BB5C'; x.fillRect(R.x + a / 30 * R.w, y, (b - a) / 30 * R.w, h); });
        x.fillStyle = '#EEEAE3'; x.textAlign = 'left'; x.font = '800 34px ' + R.F; x.fillText('0秒', R.x, y + h + 50); x.textAlign = 'right'; x.fillText('30秒', R.x + R.w, y + h + 50);
        x.textAlign = 'center'; x.font = '800 36px ' + R.F; x.fillStyle = '#4FC6B4'; x.fillText('■ 手前が右へ', R.x + R.w * .27, y - 50); x.fillStyle = '#F5BB5C'; x.fillText('■ 手前が左へ', R.x + R.w * .73, y - 50);
      },
    });
  }
  function start() { log = []; cur = null; NOU.startPanels(); [...$('opts').children].forEach(x => x.style.borderColor = '#2A3C43'); $('now').textContent = '見え方を押してね'; t0 = performance.now(); cancelAnimationFrame(raf); raf = requestAnimationFrame(draw); clearInterval(timer); timer = setInterval(tick, 200); }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "遠近や明るさの手がかりをなくした「点でできた回る玉」を30秒見て、回る向きがどう見えたか、何回切りかわったかを記録するセルフテストです。",
    "article": """
    <h2>回る向きを決めているのは、頭のほう</h2>
    <p>このページの玉は、球の表面に並べた点を、まっすぐ正面から映しています。遠くの点を小さく、手前の点を大きくするような手がかりは入れていません。だから画面の上では、点は左右に行ったり来たりしているだけで、<b>どちら回りかを決める情報はありません</b>。</p>
    <p>それでも、多くの人には玉が「回っている」ように見え、しかも向きまで決まって見えます。足りない手がかりを、頭が勝手におぎなって、立体の形と回る向きを決めているのです。</p>

    <h2>回るシルエットの錯視</h2>
    <p>同じしくみの錯視に、くるくる回る人のシルエットがあります。右回りにも左回りにも見えるのに、多くの人は<b>右回り（上から見て時計回り）</b>に見えやすいことが知られています。この見えやすさは、<b>ものを「上から見下ろしている」と思いこむくせ</b>で説明できると報告されています（Troje・McAdam 2010）。その後の研究では、このくせだけでは説明しきれない部分もあるとされています（2015年の研究）。</p>

    <h2>切りかわりやすさは、人によってちがう</h2>
    <p>このような「2通りに見える絵」は、見ているうちに見え方が入れかわることがあります。何回入れかわるかは、人によってかなりちがいます。発想の豊かさと、錯視の見え方の切りかわりの関係を調べた研究もあります（Blake・Palmisano 2021）。</p>

    <h2>結果の4つのタイプ</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>30秒で切りかわった回数</th></tr>
    <tr><td>🔒 ずっと同じ向きに見えるタイプ</td><td>0回</td></tr>
    <tr><td>🔄 ときどき切りかわるタイプ</td><td>1〜3回</td></tr>
    <tr><td>🌀 よく切りかわるタイプ</td><td>4回以上</td></tr>
    <tr><td>❔ どちらにも見えなかったタイプ</td><td>一度もボタンを押さなかった</td></tr>
    </table>
    </div>
    <p>見え方を切りかえたいときは、玉の端の点だけを目で追ったり、まばたきをしたりすると変わることがあります。</p>
""",
    "faq": [
        ("本当はどちら回りですか？", "このページの玉には、回る向きの手がかりを入れていません。どちら回りにも見えるのが正しい見え方です。"),
        ("ずっと同じ向きにしか見えません。", "そういう人も多くいます。玉の端の点を目で追うと、向きが入れかわって見えることがあります。"),
        ("この結果で性格が分かりますか？", "いいえ。遊びのためのセルフテストで、性格や頭の良さが分かるものではありません。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Troje NF, McAdam M (2010). The viewing-from-above bias and the silhouette illusion. <i>i-Perception</i>, 1(3), 143–148.",
        "Laterality effects in the spinning dancer illusion: The viewing-from-above bias is only part of the story (2015). PubMed 26666983.",
        "Blake A, Palmisano S (2021). Divergent Thinking Influences the Perception of Ambiguous Visual Illusions. <i>Perception</i>.",
    ],
    "related": [("hybrid-gazou", "👓", "近くと遠くで変わる絵テスト"), ("sakuchou-test", "🔊", "音の錯覚テスト（上がる？下がる？）"), ("shikikaku-test", "🎨", "色覚テスト（あなたの目は何色型？）"), ("stroop-test", "🧠", "ストループテスト")],
}
