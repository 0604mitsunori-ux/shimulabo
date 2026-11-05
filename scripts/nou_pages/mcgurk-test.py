# -*- coding: utf-8 -*-
# 十人十脳 第25話「目で聞く音（マガーク効果）」と連動（2026-11-05 新規）。声は端末の読み上げ機能、口はこのページで作ったイラストのアニメ
PAGE = {
    "slug": "mcgurk-test",
    "title": "マガーク効果テスト｜口の動きで、聞こえる音が変わる？目で聞く音を体験｜シミュラボ",
    "desc": "同じ「ば」の声なのに、口の動きを見ると「だ」や「が」に聞こえる？目から入る情報で聞こえ方が変わる「マガーク効果」を、イラストの口のアニメで試すセルフテスト。日本語を話す人は効果が出にくいという研究や、雑音の中では強く出る話も解説。診断ではありません。",
    "og_title": "口の動きで、聞こえる音が変わる？｜マガーク効果テスト",
    "og_desc": "同じ「ば」の声なのに、口を見ると…？目で聞く音を体験。",
    "ld_name": "マガーク効果テスト（目で聞く音）",
    "h1": "マガーク効果テスト（口の動きで、聞こえる音が変わる？）",
    "lead": "私たちは、音を耳だけで聞いているわけではありません。話している人の口の動きも、知らないうちに「聞こえ方」に入りこんでいます。これを「マガーク効果」と呼びます。声と口の動きを見て、何と聞こえたかを答えてください。8問、約2分です。",
    "start_h2": "👄 何と聞こえた？",
    "start_text": "声が出ます（音量に気をつけてね）。イラストの顔が話すので、口をよく見ながら聞いて、聞こえた音を選んでください。後半は、ざあざあという雑音が入ります。",
    "tag": "マガーク効果",
    "card_label": "マガーク効果テストの結果",
    "card_footer": "口の動きで、聞こえる音が変わる？ → shimulabo.com",
    "stage_html": """
      <div class="syn-top"><span id="part">静かなとき</span><span id="count">1 / 8</span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div id="face" style="width:250px;height:270px;margin:6px auto 10px;"></div>
      <div class="syn-ask" id="q" style="font-size:17px;font-weight:700;color:#EEEAE3;min-height:1.8em;"></div>
      <div class="syn-btns" id="opts" style="grid-template-columns:repeat(4,1fr);"></div>
      <button type="button" class="syn-go" id="replay" style="margin-top:8px;padding:10px;font-size:14px;" hidden>🔁 もう一度見る</button>
      <p class="syn-note">※ 声は、お使いの端末の読み上げ機能で出しています。端末によって声がちがいます。</p>
    """,
    "js": r"""
  const $ = NOU.$;
  // 声はいつも「ば」。見せる口だけを変える（none＝口なし・ba＝口を閉じてから開く・ga＝口を閉じずに開く）
  const SEQ = [['none', 0], ['ga', 0], ['ba', 0], ['ga', 0], ['none', 1], ['ga', 1], ['ba', 1], ['ga', 1]];
  const FACE = `<svg viewBox="0 0 200 220" style="width:100%;height:100%;"><ellipse cx="100" cy="112" rx="78" ry="94" fill="#f1cfb2"/><path d="M24 96 Q20 18 100 16 Q180 18 176 96 Q156 54 100 50 Q44 54 24 96Z" fill="#3a2a22"/>`
    + `<circle cx="70" cy="104" r="8" fill="#222"/><circle cx="130" cy="104" r="8" fill="#222"/><path d="M98 118 L92 140 H104" stroke="#b07a5a" stroke-width="3" fill="none" stroke-linecap="round"/>`
    + `<g id="mo" style="transform-box:fill-box;transform-origin:50% 50%;transition:transform .11s ease-out;"><ellipse cx="100" cy="170" rx="34" ry="23" fill="#5a1f1f" stroke="#b5544f" stroke-width="5"/><ellipse cx="100" cy="180" rx="16" ry="7" fill="#d06a6a"/></g></svg>`;
  let k = 0, ans = [], ctx = null, voice = null, busy = false;
  const can = 'speechSynthesis' in window && 'SpeechSynthesisUtterance' in window;
  function pickVoice() { if (!can) return; const v = speechSynthesis.getVoices(); voice = v.find(x => /^ja/i.test(x.lang)) || null; }
  if (can) { pickVoice(); speechSynthesis.onvoiceschanged = pickVoice; }
  function mouth(s, anim) { const m = document.getElementById('mo'); if (!m) return; m.style.transition = anim ? 'transform .11s ease-out' : 'none'; m.style.transform = `scaleY(${s})`; }
  function noise(sec) { if (!ctx) return; const n = ctx.sampleRate * sec, buf = ctx.createBuffer(1, n, ctx.sampleRate), d = buf.getChannelData(0); for (let i = 0; i < n; i++) d[i] = Math.random() * 2 - 1;
    const src = ctx.createBufferSource(), lp = ctx.createBiquadFilter(), g = ctx.createGain(); lp.type = 'lowpass'; lp.frequency.value = 2500; g.gain.value = 0.12; src.buffer = buf; src.connect(lp).connect(g).connect(ctx.destination); src.start(); }
  function play() {
    const [c, nz] = SEQ[k]; busy = true; $('opts').querySelectorAll('button').forEach(b => b.disabled = true); $('replay').hidden = true;
    if (c === 'none') $('face').innerHTML = '<div style="height:100%;display:flex;align-items:center;justify-content:center;font-size:90px;">🔈</div>'; else { $('face').innerHTML = FACE; mouth(c === 'ba' ? 0.06 : 0.35, false); }
    $('q').textContent = c === 'none' ? '音だけを聞いてね' : '口をよく見ながら聞いてね';
    if (nz) noise(2.2);
    let fired = false;
    const go = () => { if (fired) return; fired = true;
      if (c !== 'none') { setTimeout(() => mouth(1, true), 30); setTimeout(() => mouth(0.25, true), 380); }
      setTimeout(() => { busy = false; $('q').textContent = '何と聞こえた？'; $('opts').querySelectorAll('button').forEach(b => b.disabled = false); $('replay').hidden = false; }, 900); };
    setTimeout(() => { const u = new SpeechSynthesisUtterance('ば'); u.lang = 'ja-JP'; u.rate = 0.8; if (voice) u.voice = voice; u.onstart = go;
      speechSynthesis.cancel(); speechSynthesis.speak(u); setTimeout(go, 1500); }, nz ? 500 : 300);
  }
  function show() { const [c, nz] = SEQ[k]; $('part').textContent = nz ? '雑音の中' : '静かなとき'; $('count').textContent = (k + 1) + ' / 8'; $('bar').style.width = (k / 8 * 100) + '%';
    $('opts').innerHTML = [['ば', 'ba'], ['だ', 'da'], ['が', 'ga'], ['ほか', 'x']].map(([s, v]) => `<button type="button" data-v="${v}" disabled>${s}</button>`).join(''); play(); }
  $('opts').addEventListener('click', e => { const b = e.target.closest('button'); if (!b || busy) return; ans.push(b.dataset.v); k++; if (k < 8) show(); else done(); });
  $('replay').addEventListener('click', () => { if (!busy) play(); });
  function done() {
    const gaQ = [1, 3].filter(i => ans[i] !== 'ba').length, gaN = [5, 7].filter(i => ans[i] !== 'ba').length, all = gaQ + gaN;
    const ctrl = [0, 2, 4, 6].filter(i => ans[i] === 'ba').length;
    const T = all >= 3 ? ['👀', '目で聞くタイプ', '口の動きに引っぱられて、「ば」の声がちがう音に聞こえやすいタイプです。']
            : all >= 1 ? ['👂👀', 'ときどき目で聞くタイプ', 'ときどき、口の動きに聞こえ方が引っぱられました。']
            : ['👂', '耳を信じるタイプ', '口の動きにまどわされず、声どおり「ば」と聞き取りました。日本語を話す人は、この効果が出にくいという研究もあります。'];
    const extra = (gaN > gaQ ? '<p style="font-size:14px;margin:6px 0;">雑音があるときのほうが、口の動きに引っぱられやすくなりました。研究でも、雑音の中ではこの効果が強く出やすいと報告されています。</p>' : '')
      + (ctrl < 3 ? '<p style="font-size:14px;margin:6px 0;">口が見えないときや「ば」の口のときも「ば」以外に聞こえることがあったので、端末の声が聞き取りにくかったのかもしれません。</p>' : '');
    NOU.finish({
      label: '「が」の口のとき、「ば」以外に聞こえた回数', big: all, unit: ' / 4 回', emoji: T[0], typeName: T[1], advice: T[2],
      extraHTML: extra + `<div class="syn-rows"><div><span class="k">静かなとき（「が」の口）</span><span class="v">${gaQ} / 2 回</span></div><div><span class="k">雑音の中（「が」の口）</span><span class="v">${gaN} / 2 回</span></div><div><span class="k">口なし・「ば」の口で「ば」と聞こえた</span><span class="v">${ctrl} / 4 回</span></div></div><p style="font-size:12px;color:var(--ink-3);">声は8回とも「ば」です。イラストの口なので、本物の人の顔より効果は弱く出やすいと考えられます。</p>`,
      share: `マガーク効果テストやってみた👄 同じ「ば」の声が、口の動きで${all}/4回ちがう音に聞こえて「${T[1]}」でした。あなたは目で聞いてる？`,
      cardTitle: 'わたしは目で聞いている？', cardLine: `「が」の口で、${all}/4回 ちがう音に聞こえた`,
      draw: (x, R) => {
        [['静かなとき', gaQ], ['雑音の中', gaN]].forEach(([lab, v], i) => { const y = R.y + 70 + i * 220;
          x.fillStyle = '#EEEAE3'; x.textAlign = 'left'; x.font = '800 40px ' + R.F; x.fillText(lab, R.x, y);
          for (let j = 0; j < 2; j++) { x.fillStyle = j < v ? '#F5BB5C' : '#2A3C43'; x.beginPath(); x.roundRect(R.x + j * (R.w / 2 + 10), y + 30, R.w / 2 - 10, 110, 24); x.fill();
            x.fillStyle = j < v ? '#0D1417' : '#8D9BA1'; x.textAlign = 'center'; x.font = '900 52px ' + R.F; x.fillText(j < v ? '👀 ちがう音' : '👂 「ば」', R.x + j * (R.w / 2 + 10) + (R.w / 2 - 10) / 2, y + 104); } });
      },
    });
  }
  function start() {
    if (!can) { NOU.startPanels(); $('q').textContent = 'この端末（ブラウザ）では声を出せないため、このテストはできません。別のブラウザで試してください。'; $('opts').innerHTML = ''; return; }
    try { if (!ctx) ctx = new (window.AudioContext || window.webkitAudioContext)(); if (ctx.state === 'suspended') ctx.resume(); } catch (e) { ctx = null; }
    pickVoice(); k = 0; ans = []; NOU.startPanels(); show();
  }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "端末の読み上げ機能で出す「ば」の声に合わせて、このページで作ったイラストの口を「口なし」「ば の口」「が の口」の3通りで動かし、何と聞こえたかを答えるセルフテストです。前半は静かなとき、後半は雑音の中で試します。",
    "article": """
    <h2>「ば」の声が「だ」に聞こえる</h2>
    <p>1976年、イギリスの研究者マガークとマクドナルドは、ある映像を作りました。「が」と言っている人の口の映像に、「ば」という声を重ねたのです。すると、見ている人の多くには、<b>「だ」と聞こえました</b>（McGurk・MacDonald 1976）。</p>
    <p>目を閉じると、ちゃんと「ば」と聞こえます。目を開けると、また「だ」に聞こえる。頭が、耳から入る音と、目から入る口の動きを、知らないうちに混ぜ合わせているのです。この現象は、2人の名前から<b>「マガーク効果」</b>と呼ばれています。</p>

    <h2>効果の出方は、人によって大きくちがう</h2>
    <p>アメリカの研究チームが多くの人を調べたところ、マガーク効果が出る割合は、<b>まったく出ない人（0%）から、いつも出る人（100%）まで</b>大きくちがいました。それでいて、同じ人を1年後に調べても、出やすさはあまり変わりませんでした（Basu Mallick ほか 2015）。</p>

    <h2>日本語を話す人は、効果が出にくい？</h2>
    <p>日本語を話す人に、日本語の音で試した研究があります。静かなところでは、<b>口の動きに引っぱられることは少なかった</b>のですが、<b>雑音を加えると、効果が強く、多くの人に出る</b>ようになりました（Sekiyama・Tohkura 1991）。その後の研究でも、日本語を話す人は英語を話す人より、静かなところではこの効果が出にくいと報告されています。</p>
    <p>このテストの後半で雑音を入れているのは、そのためです。静かなときと雑音の中で、結果をくらべてみてください。</p>

    <h2>このテストのしくみ</h2>
    <p>声は8回とも同じ「ば」です。変えているのは、イラストの口の動きだけです。「ば」の口は、くちびるを閉じてから開きます。「が」の口は、くちびるを閉じずに開きます。</p>
    <p>本物の人の顔ではなくイラストなので、研究の映像よりも効果は弱く出やすいと考えられます。「ば」にしか聞こえなくても、おかしいことではありません。</p>
""",
    "faq": [
        ("声が出ません。", "音量やマナーモードを確かめてください。端末やブラウザによっては、読み上げの声が出ないことがあります。その場合は、別のブラウザで試してください。"),
        ("ずっと「ば」にしか聞こえません。", "めずらしいことではありません。とくに日本語を話す人は、静かなところでは効果が出にくいと報告されています。"),
        ("このテストで耳や目の病気が分かりますか？", "いいえ。遊びのためのセルフテストで、検査や診断ではありません。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "McGurk H, MacDonald J (1976). Hearing lips and seeing voices. <i>Nature</i>, 264, 746–748.",
        "Basu Mallick D, Magnotti JF, Beauchamp MS (2015). Variability and stability in the McGurk effect: contributions of participants, stimuli, time, and response type. <i>Psychonomic Bulletin &amp; Review</i>, 22(5), 1299–1307.",
        "Sekiyama K, Tohkura Y (1991). McGurk effect in non-English listeners: Few visual effects for Japanese subjects hearing Japanese syllables of high auditory intelligibility. <i>Journal of the Acoustical Society of America</i>, 90(4), 1797–1805.",
    ],
    "related": [("mimi-nenrei", "👂", "耳年齢テスト（聞こえる高い音は？）"), ("onkan-test", "🎹", "音感テスト"), ("kyokankaku-test", "🔤", "共感覚テスト（文字に色が見える？）"), ("dress-iro", "👗", "ドレスの色テスト（白と金？青と黒？）")],
}
