# -*- coding: utf-8 -*-
# 十人十脳 第13話「リズム感」と連動。既存の「リズム感テスト」を同じURLのまま作り直した（2026-11-05）
PAGE = {
    "slug": "rhythm-test",
    "title": "リズム感テスト｜拍にぴったり合わせられる？ずれ方で分かるあなたのリズムのくせ｜シミュラボ",
    "desc": "流れる拍に合わせて画面をタップ。何ミリ秒ずれたか、ずれ方がそろっているかで、あなたのリズムのくせが分かるリズム感テスト。人は拍より少し「先に」叩いてしまう、という研究も解説。診断ではありません。",
    "og_title": "拍にぴったり合わせられる？｜リズム感テスト",
    "og_desc": "人は拍より少し先に叩いてしまう。あなたのずれ方は？",
    "ld_name": "リズム感テスト（拍にぴったり合わせられる？）",
    "h1": "リズム感テスト（拍にぴったり合わせられる？）",
    "lead": "「カッ、カッ、カッ」と鳴る拍に合わせて、画面のボタンをタップしてください。前半16回は音に合わせて、後半8回は<b>音が消えたあとも同じ速さで</b>続けます。どれだけぴったりか、ずれ方がそろっているかを測ります。約1分です。",
    "start_h2": "🥁 音に合わせて、タップしてね",
    "start_text": "パソコンならスペースキーでもOK。ワイヤレスのイヤホンは音が遅れて届くことがあるので、できればスマホやパソコンのスピーカーで。",
    "tag": "リズム感テスト",
    "card_label": "リズム感テストの結果",
    "card_footer": "拍にぴったり合わせられる？ → shimulabo.com",
    "stage_html": """
      <div class="syn-top"><span id="part">音に合わせてタップ</span><span id="count"></span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div class="syn-big" id="beat" style="font-size:80px;transition:transform .08s;">🥁</div>
      <div class="syn-ask" id="ask">最初の4回は聞くだけ。5回目から合わせてね</div>
      <button type="button" class="syn-go" id="tap" style="padding:36px;font-size:22px;">ここをタップ</button>
    """,
    "js": r"""
  const $ = NOU.$;
  const IOI = 600, LEAD = 4, SYNC = 16, CONT = 8;      // 1拍0.6秒（1分に100拍）
  let ctx = null, t0 = 0, beats = [], taps = [], running = false, endTimer = 0;
  function click(at) { const o = ctx.createOscillator(), g = ctx.createGain(); o.frequency.value = 1600; g.gain.setValueAtTime(0.25, at); g.gain.exponentialRampToValueAtTime(0.001, at + 0.05); o.connect(g).connect(ctx.destination); o.start(at); o.stop(at + 0.06); }
  function begin() {
    if (!ctx) ctx = new (window.AudioContext || window.webkitAudioContext)(); if (ctx.state === 'suspended') ctx.resume();
    beats = []; taps = []; running = true;
    const s = ctx.currentTime + 0.5;
    const base = performance.now() + 500 + (ctx.outputLatency || 0) * 1000;   // 音がスピーカーから出るまでの遅れも足す
    for (let i = 0; i < LEAD + SYNC; i++) { click(s + i * IOI / 1000); beats.push(base + i * IOI); }
    for (let i = LEAD + SYNC; i < LEAD + SYNC + CONT; i++) beats.push(base + i * IOI);    // 音なしの拍（続けてタップ）
    const flash = i => setTimeout(() => { $('beat').style.transform = 'scale(1.18)'; setTimeout(() => $('beat').style.transform = 'scale(1)', 90);
      $('part').textContent = i < LEAD ? '聞くだけ' : i < LEAD + SYNC ? '音に合わせてタップ' : '音なしで、同じ速さで続けて！'; $('count').textContent = Math.min(LEAD + SYNC + CONT, i + 1) + ' / ' + (LEAD + SYNC + CONT);
      $('bar').style.width = (i / (LEAD + SYNC + CONT) * 100) + '%'; }, 500 + i * IOI);
    for (let i = 0; i < LEAD + SYNC; i++) flash(i);
    setTimeout(() => { $('part').textContent = '音なしで、同じ速さで続けて！'; $('ask').textContent = '音が消えても、同じ速さでタップを続けてね'; $('beat').textContent = '🔇'; }, 500 + (LEAD + SYNC) * IOI - 100);
    clearTimeout(endTimer); endTimer = setTimeout(done, 500 + (LEAD + SYNC + CONT) * IOI + 400);
  }
  function tap() { if (!running) return; taps.push(performance.now()); $('tap').style.background = '#F5BB5C'; setTimeout(() => $('tap').style.background = '#4FC6B4', 80); }
  $('tap').addEventListener('pointerdown', e => { e.preventDefault(); tap(); });
  document.addEventListener('keydown', e => { if (e.code === 'Space' && running) { e.preventDefault(); tap(); } });
  function match(from, to) {   // 拍ごとに、いちばん近いタップとのずれ（ミリ秒）
    const out = []; for (let i = from; i < to; i++) { const b = beats[i]; let best = null; for (const t of taps) if (Math.abs(t - b) < IOI / 2 && (best === null || Math.abs(t - b) < Math.abs(best))) best = t - b; if (best !== null) out.push(best); } return out;
  }
  const mean = a => a.reduce((s, v) => s + v, 0) / (a.length || 1), sd = a => Math.sqrt(mean(a.map(v => (v - mean(a)) ** 2)));
  function done() {
    running = false; $('beat').textContent = '🥁';
    const sync = match(LEAD, LEAD + SYNC), cont = match(LEAD + SYNC, LEAD + SYNC + CONT);
    if (sync.length < 6) { NOU.finish({ label: 'タップが少なくて測れませんでした', big: '—', unit: '', emoji: '❔', typeName: 'もう一度ためしてね', advice: '音に合わせて、ボタンを何回もタップしてください。', extraHTML: '', share: 'リズム感テストやってみた🥁', cardTitle: 'わたしのリズム', cardLine: 'もう一度ためす', draw: null }); return; }
    const m = Math.round(mean(sync)), s = Math.round(sd(sync)), cm = cont.length ? Math.round(mean(cont)) : null;
    const T = s <= 35 ? ['🎯', 'ぴったり合わせるタイプ', 'タップのずれがとてもそろっていました。拍を体でしっかりつかめています。']
            : s <= 70 ? ['🥁', 'ほぼ合わせるタイプ', '多少のゆれはあっても、拍についていけていました。多くの人はこのあたりです。']
            : ['🎶', '自分のノリで叩くタイプ', 'タップのずれが大きくゆれました。速さを決めて、体を少しゆらしながら叩くと合わせやすくなります。'];
    const lead = m < -10 ? `平均で<b>${-m}ミリ秒早く</b>叩いていました。人は拍より少し先に叩きやすいことが知られています。` : m > 10 ? `平均で<b>${m}ミリ秒遅れて</b>叩いていました。音を聞いてから叩くと遅れやすくなります。` : '平均すると、ほぼ拍ぴったりでした。';
    NOU.finish({
      label: 'ずれのばらつき（小さいほどそろっている）', big: s, unit: ' ミリ秒', emoji: T[0], typeName: T[1], advice: T[2],
      extraHTML: `<p style="font-size:14px;margin:6px 0;">${lead}</p><div class="syn-rows"><div><span class="k">音に合わせたとき（平均のずれ）</span><span class="v">${m > 0 ? '+' : ''}${m} ミリ秒</span></div><div><span class="k">音が消えたあと（平均のずれ）</span><span class="v">${cm === null ? '—' : (cm > 0 ? '+' : '') + cm + ' ミリ秒'}</span></div></div><p style="font-size:12px;color:var(--ink-3);">マイナス＝拍より早い・プラス＝拍より遅い。ワイヤレスのイヤホンや画面の反応の遅れでも、数十ミリ秒ずれることがあります。</p>`,
      share: `リズム感テストやってみた🥁 ずれのばらつき${s}ミリ秒・平均${m > 0 ? '+' : ''}${m}ミリ秒で「${T[1]}」でした。あなたは拍にぴったり合わせられる？`,
      cardTitle: 'わたしのリズムのずれ', cardLine: `ばらつき ${s}ミリ秒・平均 ${m > 0 ? '+' : ''}${m}ミリ秒`,
      draw: (x, R) => {
        const cx = R.x + R.w / 2, y = R.y + 280, sc = R.w / 2 / 300;
        x.strokeStyle = '#2A3C43'; x.lineWidth = 4; x.beginPath(); x.moveTo(R.x, y); x.lineTo(R.x + R.w, y); x.stroke();
        x.strokeStyle = '#F5BB5C'; x.lineWidth = 6; x.beginPath(); x.moveTo(cx, y - 160); x.lineTo(cx, y + 160); x.stroke();
        sync.forEach((v, i) => { x.fillStyle = '#4FC6B4'; x.beginPath(); x.arc(cx + Math.max(-300, Math.min(300, v)) * sc, y - 120 + i * 15, 12, 0, Math.PI * 2); x.fill(); });
        x.fillStyle = '#EEEAE3'; x.font = '800 32px ' + R.F; x.textAlign = 'left'; x.fillText('← 早い', R.x, y + 220); x.textAlign = 'right'; x.fillText('遅い →', R.x + R.w, y + 220); x.textAlign = 'center'; x.fillStyle = '#F5BB5C'; x.fillText('拍', cx, y + 220);
      },
    });
  }
  function start() { NOU.startPanels(); $('ask').textContent = '最初の4回は聞くだけ。5回目から合わせてね'; $('beat').textContent = '🥁'; begin(); }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "1分に100拍の音に合わせて16回タップし、音が消えたあとも8回続けて、拍とのずれ（ミリ秒）とばらつきを測るセルフテストです。",
    "article": """
    <h2>人は、拍より少し「先に」叩く</h2>
    <p>メトロノームの音に合わせて指でタップする実験は、たくさん行われてきました。その研究をまとめた論文によると、多くの人のタップは、<b>音が鳴るより数十ミリ秒（1秒の100分の数）早く</b>なりやすいことが知られています（Repp 2005）。音を聞いてから動くのではなく、次の拍を予想して先回りしているためと考えられています。</p>
    <p>このずれは「負の平均非同期」と呼ばれ、2006〜2012年の研究をまとめた続きの論文でも、多くの場合にマイナス（早め）になると書かれています（Repp・Su 2013）。ただし最近では、文化や音楽の経験によっては当てはまらない人もいるという報告もあります。</p>

    <h2>リズム感＝「ずれのそろい方」</h2>
    <p>このテストでは、2つのことを測っています。</p>
    <ul>
      <li><b>平均のずれ</b>：拍より早いか遅いか。少し早いのは、多くの人に見られるふつうのことです</li>
      <li><b>ばらつき</b>：毎回のずれが、どれだけそろっているか。小さいほど、拍を体でしっかりつかめています</li>
    </ul>
    <p>後半の「音が消えたあとも続ける」部分では、頭の中だけで拍を保てるかが分かります。速くなっていく人、遅くなっていく人など、ここにも人によるちがいが出ます。</p>

    <h2>結果が機械で変わる理由</h2>
    <p>ワイヤレスのイヤホンは、音が届くまでに時間がかかることがあります。画面がタップを受け取るまでにも、わずかな遅れがあります。平均のずれは機械でも変わるので、同じ機械で、家族や友だちとくらべてみてください。ばらつきのほうが、機械の影響を受けにくい目安です。</p>

    <h2>結果の3つのタイプ</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>ずれのばらつき</th></tr>
    <tr><td>🎯 ぴったり合わせるタイプ</td><td>35ミリ秒以下</td></tr>
    <tr><td>🥁 ほぼ合わせるタイプ</td><td>36〜70ミリ秒</td></tr>
    <tr><td>🎶 自分のノリで叩くタイプ</td><td>71ミリ秒以上</td></tr>
    </table>
    </div>
""",
    "faq": [
        ("このテストでリズム感が分かりますか？", "タップのずれ方の傾向は分かりますが、遊びのためのセルフテストで、音楽の才能を測るものではありません。"),
        ("ずっと早めに叩いてしまいます。", "多くの人に見られるふつうのことです。人は次の拍を予想して、少し先に動きやすいと考えられています（Repp 2005）。"),
        ("イヤホンで結果が変わりました。", "ワイヤレスのイヤホンは音が遅れて届くことがあります。できればスマホやパソコンのスピーカーで試してください。"),
        ("答えは送信されますか？", "いいえ。タップの記録はこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Repp BH (2005). Sensorimotor synchronization: A review of the tapping literature. <i>Psychonomic Bulletin &amp; Review</i>, 12(6), 969–992.",
        "Repp BH, Su YH (2013). Sensorimotor synchronization: A review of recent research (2006–2012). <i>Psychonomic Bulletin &amp; Review</i>, 20(3), 403–452.",
    ],
    "related": [("onkan-test", "🎹", "絶対音感・相対音感テスト"), ("jikan-kankaku", "⏱️", "時間の感じ方テスト（30秒ぴったり？）"), ("torihada-test", "🎵", "音楽で鳥肌が立つ人テスト"), ("reaction-test", "⚡", "反応速度テスト")],
}
