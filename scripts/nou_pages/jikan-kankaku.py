# -*- coding: utf-8 -*-
# 十人十脳 第21話「時間の感じ方」と連動（2026-11-05 新規）
PAGE = {
    "slug": "jikan-kankaku",
    "title": "時間感覚テスト｜目を閉じて30秒、ぴったり数えられる？あなたの頭の中の時計を測る｜シミュラボ",
    "desc": "時計を見ずに10秒・30秒・60秒をはかって、実際の時間とくらべるセルフテスト。あなたの頭の中の時計は、速い？遅い？熱があると時間を速く数えるようになった、という1933年の有名な話や、長い時間ほどずれが大きくなる研究も解説。診断ではありません。",
    "og_title": "目を閉じて30秒、ぴったり数えられる？｜時間感覚テスト",
    "og_desc": "10秒・30秒・60秒を、時計を見ずにはかる。あなたの頭の中の時計は速い？遅い？",
    "ld_name": "時間感覚テスト（目を閉じて30秒）",
    "h1": "時間感覚テスト（目を閉じて30秒、ぴったり数えられる？）",
    "lead": "楽しい時間はあっという間で、退屈な時間は長く感じる。私たちの頭の中には、時計のようなしくみがあると考えられています。時計を見ずに、10秒・30秒・60秒をはかってみてください。約2分です。",
    "start_h2": "⏱️ 頭の中で時間をはかってね",
    "start_text": "ボタンを押したら、目を閉じて頭の中で時間をはかり、その時間がたったと思ったら、もう一度ボタンを押します。パソコンならスペースキーでもOKです。画面には時間は出ません。",
    "tag": "時間感覚",
    "card_label": "時間感覚テストの結果",
    "card_footer": "目を閉じて30秒、ぴったり？ → shimulabo.com",
    "stage_html": """
      <div class="syn-top"><span id="part">1回目</span><span id="count">1 / 3</span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div class="syn-big" id="em" style="font-size:72px;">⏱️</div>
      <div class="syn-ask" id="q" style="font-size:20px;font-weight:800;color:#EEEAE3;min-height:2.6em;line-height:1.6;"></div>
      <button type="button" class="syn-go" id="tap" style="padding:30px;font-size:20px;">スタート</button>
      <p class="syn-note">時計やスマホの時刻を見ないでね。頭の中で「いち、に、…」と数えてもOKです。</p>
    """,
    "js": r"""
  const $ = NOU.$;
  const TG = [10, 30, 60];
  let k = 0, t0 = 0, run = false, got = [];
  function show() { run = false; $('part').textContent = (k + 1) + '回目'; $('count').textContent = (k + 1) + ' / 3'; $('bar').style.width = (k / 3 * 100) + '%';
    $('em').textContent = '⏱️'; $('q').textContent = TG[k] + '秒 をはかってね'; $('tap').textContent = 'スタート'; }
  function press() {
    if (!run) { run = true; t0 = performance.now(); $('em').textContent = '🙈'; $('q').textContent = '目を閉じて…' + TG[k] + '秒たったと思ったら押してね'; $('tap').textContent = 'ストップ'; return; }
    if (performance.now() - t0 < 500) return;   // 押しまちがいの二度押しは数えない
    got.push((performance.now() - t0) / 1000); k++; if (k < 3) show(); else done();
  }
  $('tap').addEventListener('pointerdown', e => { e.preventDefault(); press(); });
  document.addEventListener('keydown', e => { if (e.code === 'Space' && !$('qPanel').hidden && k < 3) { e.preventDefault(); press(); } });
  function done() {
    const ratio = got.map((g, i) => g / TG[i]), avg = ratio.reduce((a, b) => a + b, 0) / 3, pct = Math.round((avg - 1) * 100);
    const T = avg < 0.9 ? ['🐇', 'せっかち時計タイプ', '実際より早くボタンを押しました。頭の中の時計が、少し速く進んでいるのかもしれません。']
            : avg > 1.1 ? ['🐢', 'のんびり時計タイプ', '実際よりおそくボタンを押しました。頭の中の時計が、少しゆっくり進んでいるのかもしれません。']
            : ['🎯', 'ぴったり時計タイプ', '実際の時間と、ほぼ同じでした。頭の中の時計が正確なタイプです。'];
    const f1 = v => (Math.round(v * 10) / 10).toFixed(1);
    const rows = TG.map((t, i) => `<div><span class="k">${t}秒のつもり</span><span class="v">${f1(got[i])} 秒（${got[i] >= t ? '+' : ''}${f1(got[i] - t)}）</span></div>`).join('');
    NOU.finish({
      label: '30秒のつもりで押した時間', big: f1(got[1]), unit: ' 秒', emoji: T[0], typeName: T[1], advice: T[2],
      extraHTML: `<div class="syn-rows">${rows}</div><p style="font-size:14px;margin:6px 0;">3回の平均で、実際の時間より<b>${Math.abs(pct)}% ${pct >= 0 ? '長く' : '短く'}</b>はかっていました。</p><p style="font-size:12px;color:var(--ink-3);">長い時間ほど、秒数のずれは大きくなりやすいことが知られています。</p>`,
      share: `時間感覚テストやってみた⏱️ 30秒のつもりが${f1(got[1])}秒で「${T[1]}」でした。あなたは目を閉じて30秒、ぴったり数えられる？`,
      cardTitle: 'わたしの頭の中の時計', cardLine: `30秒のつもりが ${f1(got[1])}秒`,
      draw: (x, R) => {
        const cw = (R.w - 2 * 40) / 3, base = R.y + 450, mx = Math.max(1.6, ...ratio);
        TG.forEach((t, i) => { const xx = R.x + i * (cw + 40), h = ratio[i] / mx * 340, h0 = 1 / mx * 340;
          x.fillStyle = '#2A3C43'; x.beginPath(); x.roundRect(xx, base - 360, cw, 360, 24); x.fill();
          x.fillStyle = '#4FC6B4'; x.beginPath(); x.roundRect(xx, base - h, cw, h, 24); x.fill();
          x.strokeStyle = '#F5BB5C'; x.lineWidth = 6; x.setLineDash([16, 10]); x.beginPath(); x.moveTo(xx - 6, base - h0); x.lineTo(xx + cw + 6, base - h0); x.stroke(); x.setLineDash([]);
          x.textAlign = 'center'; x.fillStyle = '#EEEAE3'; x.font = '900 42px ' + R.F; x.fillText(f1(got[i]) + '秒', xx + cw / 2, base - 380);
          x.font = '800 34px ' + R.F; x.fillText(t + '秒のつもり', xx + cw / 2, base + 50); });
      },
    });
  }
  function start() { k = 0; got = []; NOU.startPanels(); show(); }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "時計を見ずに、10秒・30秒・60秒がたったと思ったところでボタンを押し、実際にかかった時間とくらべるセルフテストです。",
    "article": """
    <h2>頭の中には「時計」がある？</h2>
    <p>私たちは時計を見なくても、「そろそろ1分くらいたったかな」と、だいたいの時間が分かります。研究者たちは、頭の中に時間をはかるしくみがあると考えてきました。</p>
    <p>有名な話があります。1930年代、アメリカの研究者ホーグランドは、熱を出した妻に「1分」を数えてもらいました。すると、<b>体温が高いときほど、60まで数え終わるのが早くなる</b>（頭の中の時計が速く進む）ことに気づきました（Hoagland 1933）。ホーグランドは、体の中の化学反応の速さが、時間の感じ方を決めているのではないかと考えました。</p>

    <h2>長い時間ほど、ずれも大きくなる</h2>
    <p>人が時間をはかる実験をたくさん集めると、ある共通点が見えてきます。それは、<b>はかる時間が長いほど、ずれの大きさもほぼ同じ割合で大きくなる</b>ということです。たとえば10秒で1秒ずれる人は、60秒では6秒くらいずれやすい、という考え方です。</p>
    <p>こうした性質は多くの研究で見られる一方、とても短い時間などでは当てはまらないこともあると報告されています（Wearden・Lejeune 2008）。</p>
    <p>このテストでは10秒・30秒・60秒の3つをはかり、ずれを「秒」と「割合」の両方で出しています。</p>

    <h2>時間の感じ方を変えるもの</h2>
    <ul>
      <li>体温や体の調子</li>
      <li>楽しい・退屈といった気持ち</li>
      <li>そのとき、どのくらい時間に注意を向けているか</li>
    </ul>
    <p>同じ人でも、朝と夜、元気なときと疲れたときで結果が変わることがあります。何回か試してみると、あなたの頭の中の時計のくせが見えてきます。</p>

    <h2>結果の3つのタイプ</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>3回の平均のずれ</th></tr>
    <tr><td>🐇 せっかち時計タイプ</td><td>実際より10%以上短い</td></tr>
    <tr><td>🎯 ぴったり時計タイプ</td><td>±10%未満</td></tr>
    <tr><td>🐢 のんびり時計タイプ</td><td>実際より10%以上長い</td></tr>
    </table>
    </div>
    <p>区切りは、このページで決めた目安です。</p>
""",
    "faq": [
        ("頭の中で数えてもいいですか？", "はい、数えてもかまいません。数えるかどうかで結果が変わるか、両方ためしてみるのもおもしろいです。"),
        ("毎回結果がちがいます。", "時間の感じ方は、そのときの体の調子や気持ちでも変わります。何回かの平均を見てください。"),
        ("このテストで何かの病気が分かりますか？", "いいえ。遊びのためのセルフテストで、検査や診断ではありません。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Hoagland H (1933). The physiological control of judgments of duration: Evidence for a chemical clock. <i>Journal of General Psychology</i>, 9, 267–287.",
        "Wearden JH, Lejeune H (2008). Scalar properties in human timing: Conformity and violations. <i>Quarterly Journal of Experimental Psychology</i>, 61(4), 569–587.",
    ],
    "related": [("rhythm-test", "🥁", "リズム感テスト"), ("chrono", "⏰", "朝型・夜型診断"), ("reaction-test", "⚡", "反応速度テスト"), ("kazu-shunkan", "🔢", "数の瞬間テスト（一瞬で数が分かる？）")],
}
