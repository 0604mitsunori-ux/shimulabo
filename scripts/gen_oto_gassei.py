# -*- coding: utf-8 -*-
"""音をつくる（倍音と音色）シミュレーター（2026-11-24）
   sims/oto-gassei/index.html を書き出す（冪等）。 使い方: python -X utf8 scripts/gen_oto_gassei.py"""
import html as H, io, json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://shimulabo.com"
SLUG = "oto-gassei"
NAME = "音をつくる（倍音と音色）シミュレーター"
CAT = "あそぶ・実験"
TITLE = "音をつくるシミュレーター｜倍音を足して波形と音色を変える（のこぎり波・四角い波・三角波）｜シミュラボ"
DESC = ("基本の音（サイン波）に、2倍・3倍…8倍の高さの音（倍音）を好きな強さで足していくと、波の形が変わり、音色が変わることを目と耳で確かめるシミュレーター。"
        "のこぎり波・四角い波・三角波・フルート風・クラリネット風のプリセットつき。音を鳴らさなくても、波形の動きだけで学べます。")
OG_T = "音をつくる 倍音と音色のシミュレーター"
OG_D = "サイン波に2倍〜8倍の倍音を足すと、波の形と音色が変わる。のこぎり波・四角い波・三角波も作れる。"
H1 = "音をつくる<br>倍音と音色のシミュレーター"
LEAD = ("同じ高さの「ド」でも、ピアノとフルートでは聞こえ方がちがいます。このちがいを音色（ねいろ）といいます。"
        "基本の音に、2倍・3倍…8倍の高さの音（倍音）を好きな強さで足して、波の形と音色がどう変わるかを確かめてみましょう。音は、ボタンを押したときだけ小さく鳴ります。")

FAQ = [
    ("倍音とは何ですか？", "基本の音の2倍、3倍、4倍…の振動数（1秒間にふるえる回数）をもつ音のことです。たとえば基本の音が262Hzなら、2倍の倍音は524Hz、3倍の倍音は786Hzです。楽器や声の音には、基本の音といっしょに、たくさんの倍音がまざっています。"),
    ("音が鳴りません。", "「🔊 音を鳴らす」を押したときだけ音が出ます。スマートフォンが消音（マナーモード）になっていると鳴らないことがあります。また、小さなスピーカーは低い音が出にくいので、基本の高さを上げるか、イヤホンでためしてみてください。音が出せない環境でも、波形の表示はそのまま使えます。"),
    ("波の形がちがっても、音の高さが同じに聞こえるのはなぜ？", "倍音を足しても、波がくり返す速さ（基本の振動数）は変わらないからです。音の高さは主に基本の振動数で決まり、倍音のまざり方は音色を決めます。"),
    ("四角い波なのに、角が丸かったり波打ったりしているのはなぜ？", "このシミュレーターでは8倍までの倍音しか足していないためです。もっと高い倍音まで足していくと、だんだん四角に近づきます。ただし、角の近くの小さなとび出しは、いくつ足しても残ることが知られています（ギブズ現象）。"),
    ("フルート風・クラリネット風は、本物の楽器の音ですか？", "いいえ。「フルートは基本の音が強く倍音が少なめ」「クラリネットは奇数倍の倍音が強い」と一般に言われる特ちょうをまねた、模式的な形です。本物の楽器を測った値ではありません。本物の音は、倍音がもっと多く、音の出はじめや消え方も音色に大きくかかわります。"),
]
REL = [("unari-teijouha", "〰️", "うなり・定常波シミュレーター"), ("chladni-zukei", "🎻", "クラドニ図形シミュレーター"), ("mosquito-on", "🦟", "モスキート音テスト")]

ARTICLE = """
<h2>このシミュレーターのしくみ</h2>
<p>音は、空気のふるえ（振動）が波として伝わるものです。音には3つの特ちょうがあります。</p>
<ul>
<li><b>音の高さ</b>：1秒間にふるえる回数（<b>振動数</b>、単位はHz＝ヘルツ）で決まります。振動数が大きいほど高い音です。</li>
<li><b>音の大きさ</b>：ふるえのはば（<b>振幅</b>）で決まります。振幅が大きいほど大きい音です。</li>
<li><b>音色（ねいろ）</b>：<b>波の形</b>のちがいです。波の形は、倍音のまざり方で決まります。</li>
</ul>
<p>このシミュレーターでは、基本の音（サイン波）と、その2倍〜8倍の振動数をもつ7つの倍音を、それぞれの強さでそのまま足し算しています。うすい線が1つ1つの音、太い黄色の線が足し合わせた波です。くり返す波は、サイン波の足し合わせで表せることが知られています（フーリエ級数）。</p>
<p>単純にしている点は次のとおりです。</p>
<ul>
<li>足せる倍音は<b>8倍まで</b>です。本物の音には、もっと高い倍音もふくまれます。</li>
<li>画面の波は、見やすいように<b>ゆっくり</b>流しています。本当は、262Hzの音なら1秒間に262回ふるえます。</li>
<li>聞こえる音の大きさは、耳にやさしいよう、波の高さにかかわらず<b>いつも同じくらいの小ささ</b>にそろえています。</li>
<li>三角波だけは、3倍と7倍の音を上下さかさまにして足しています（そうしないと三角の形になりません）。</li>
</ul>

<h2>ためしてみたいこと</h2>
<ul>
<li><b>サイン波から、2倍の音だけを少しずつ足す</b>：波の形がゆがんでいきます。音を鳴らしていると、音色が少し明るくなるのがわかります。</li>
<li><b>「のこぎり波」と「四角い波」をくらべる</b>：四角い波は、偶数倍（2・4・6・8倍）の音がありません。棒グラフのならび方と、音色のちがいをくらべてみましょう。</li>
<li><b>「四角い波」と「三角波」をくらべる</b>：どちらも奇数倍だけですが、三角波は高い倍音がとても弱く、サイン波に近いやわらかい音になります。</li>
<li><b>基本の音（1倍）を0にする</b>：倍音だけを残すと、波の形も音色も大きく変わります。</li>
<li><b>基本の高さを変える</b>：波の形（音色）はそのままで、音の高さだけが変わります。スペクトルの下の数字（Hz）がどう変わるかも見てみましょう。</li>
</ul>

<h2>本物では</h2>
<p>中学1年の理科「音の性質」では、音の大きさは振幅で、音の高さは振動数で決まることを学びます。オシロスコープやコンピュータで音の波形を見ると、同じ高さ・同じ大きさの音でも、楽器によって波の形がちがうことがわかります。これが音色のちがいです。</p>
<p>19世紀のドイツの科学者ヘルムホルツは、音色が倍音のまざり方に関係することをくわしく調べました。たとえばクラリネットは、管の形の性質から、低い音域では奇数倍の倍音が強くなりやすいと言われています。</p>
<p>ただし、本物の楽器の音色は、倍音の強さだけでは決まりません。音の出はじめの変化、時間とともに倍音が変わっていくようす、息や弓のこすれる音なども、その楽器らしさを作っています。このシミュレーターは、「倍音を足すと波の形と音色が変わる」という基本だけを取り出したものです。</p>
"""

REFS = [
    "文部科学省「中学校学習指導要領（平成29年告示）解説 理科編」（第1学年「光と音」音の性質）",
    "H. ヘルムホルツ『音感覚論』（1863年）",
    "J. フーリエ『熱の解析的理論』（1822年）（くり返す波をサイン波の足し合わせで表す考え方）",
    "W3C「Web Audio API」仕様（PeriodicWave：倍音の強さから波形を作るしくみ）",
]

STAGE = r"""
<style>
.ot-seg{display:flex;flex-wrap:wrap;gap:6px}
.ot-seg button{border:1.5px solid var(--line);background:#fff;border-radius:999px;padding:8px 13px;font:inherit;font-size:13.5px;font-weight:800;cursor:pointer;color:var(--ink)}
.ot-seg button.on{background:#4f46e5;border-color:#4f46e5;color:#fff}
#otWrap{position:relative;border-radius:14px;overflow:hidden;border:1px solid var(--line);background:#0b1220;margin-top:12px}
#otWave{display:block;width:100%;aspect-ratio:16/8}
.ot-legend{font-size:12px;color:var(--ink-2);display:flex;gap:14px;flex-wrap:wrap;margin-top:6px}
.ot-legend i{display:inline-block;width:20px;height:4px;vertical-align:3px;margin-right:4px;background:#eab308;border-radius:2px}
.ot-legend i.t{height:2px;background:#38bdf8}
.ot-legend i.d{height:0;border-top:2px dashed #94a3b8;background:none}
.ot-playrow{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-top:12px}
.ot-playrow .btn{width:auto;padding:12px 20px}
#otPlay.on{background:#dc2626;border-color:#dc2626}
.ot-anote{font-size:12.5px;color:var(--ink-2);margin:0}
.ot-sum{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:12px}
.ot-sum div{background:#eef2ff;border-radius:12px;padding:10px 4px;text-align:center}
.ot-sum b{display:block;font-size:20px;color:#4338ca;font-variant-numeric:tabular-nums}
.ot-sum b small{font-size:11.5px}
.ot-sum span{font-size:11.5px;color:var(--ink-2);font-weight:700}
.ot-note{font-size:13.5px;color:var(--ink);background:#eef2ff;border-radius:10px;padding:9px 12px;margin:10px 0 0;font-weight:700}
.ot-hint{font-size:13px;color:var(--ink-2);margin:0 0 6px}
#otBars{display:block;width:100%;height:180px;touch-action:none;cursor:ns-resize;border-radius:12px;background:#f8fafc;border:1px solid var(--line)}
.ot-lab{display:grid;grid-template-columns:repeat(8,1fr);text-align:center;margin-top:4px}
.ot-lab div{min-width:0}
.ot-lab b{display:block;font-size:12px}
.ot-lab span{display:block;font-size:11px;color:var(--ink-2);font-variant-numeric:tabular-nums}
#otSpec{display:block;width:100%;height:120px;margin-top:4px}
.ot-keys{display:grid;grid-template-columns:repeat(8,1fr);gap:4px}
.ot-keys button{min-width:0;border:1.5px solid var(--line);background:#fff;border-radius:0 0 8px 8px;padding:22px 0 8px;font:inherit;font-size:12.5px;font-weight:800;cursor:pointer;color:var(--ink)}
.ot-keys button.on{background:#4f46e5;border-color:#4f46e5;color:#fff}
.ot-cols{display:grid;grid-template-columns:1fr 1fr;gap:6px 22px}
.ot-msg{position:absolute;left:50%;bottom:10px;transform:translateX(-50%);background:rgba(255,255,255,.92);color:#0f172a;font-size:12.5px;font-weight:700;border-radius:12px;padding:6px 14px;max-width:92%;text-align:center;pointer-events:none;opacity:0;transition:opacity .3s}
.ot-msg.show{opacity:1}
@media (max-width:640px){#otWave{aspect-ratio:4/3}.ot-sum{grid-template-columns:repeat(2,1fr)}.ot-cols{grid-template-columns:1fr}.ot-seg button{padding:7px 11px;font-size:13px}#otBars{height:160px}}
</style>
"""

BODY = r"""
  <section class="panel" id="resultPanel">
    <h2 style="margin:0 0 8px;font-size:18px;">① 音色をえらぶ（プリセット）</h2>
    <div class="ot-seg" id="otPresets"></div>

    <div id="otWrap">
      <canvas id="otWave" aria-label="倍音を足し合わせた波形が右へ流れるアニメーション"></canvas>
      <div class="ot-msg" id="otMsg"></div>
    </div>
    <div class="ot-legend"><span><i></i>足し合わせた波</span><span><i class="t"></i>1つ1つの音（基本の音と倍音）</span><span><i class="d"></i>基本の音が100%のときの高さ</span></div>

    <div class="ot-playrow">
      <button class="btn btn-primary" id="otPlay" type="button" aria-pressed="false">🔊 音を鳴らす</button>
      <p class="ot-anote" id="otANote">押したときだけ、小さな音で鳴ります。もう一度押すと止まります。</p>
    </div>

    <div class="ot-sum">
      <div><b id="mF">262<small>Hz</small></b><span>基本の周波数</span></div>
      <div><b id="mTop">-</b><span>いちばん強い音</span></div>
      <div><b id="mCnt">0<small>こ</small></b><span>倍音の数（2倍〜8倍）</span></div>
      <div><b id="mPeak">0</b><span>波の高さの最大</span></div>
    </div>
    <p class="ot-note" id="otNote"></p>

    <h2 style="margin:20px 0 6px;font-size:18px;">② 倍音の強さ（指でなぞって変えられます）</h2>
    <p class="ot-hint">1倍が「基本の音」、2倍〜8倍が「倍音」です。棒を上下に動かすか、横になぞると、波の形がすぐ変わります。</p>
    <canvas id="otBars" role="img" aria-label="基本の音と2倍から8倍までの倍音の強さを変える8本の棒"></canvas>
    <div class="ot-lab" id="otLab"></div>

    <h2 style="margin:20px 0 6px;font-size:18px;">③ スペクトル（どの高さの音が、どれだけ入っているか）</h2>
    <p class="ot-hint">横は音の高さ（下の数字は周波数・Hz）、たては強さです。</p>
    <canvas id="otSpec" aria-label="倍音の強さのスペクトル"></canvas>

    <h2 style="margin:20px 0 10px;font-size:18px;">④ 基本の高さと、波の流れる速さ</h2>
    <div class="field"><label>鍵盤（ド〜上のド）</label><div class="ot-keys" id="otKeys"></div></div>
    <div class="ot-cols" style="margin-top:10px">
      <div class="field"><label>基本の周波数 <span class="hint">（<b id="vF"></b>）</span></label><input type="range" id="kF" min="110" max="880" step="1" value="262"></div>
      <div class="field"><label>波の流れる速さ <span class="hint">（<b id="vSp"></b>）</span></label><input type="range" id="kSp" min="0" max="2" step="0.05" value="0.5"></div>
    </div>
    <p class="ot-hint" id="otTime" style="margin-top:6px"></p>

    <div style="text-align:center;margin-top:16px;"><span id="shareCount" class="share-count" style="display:none"></span></div>
    <div class="share-row">
      <button class="btn btn-x" id="shareBtn">𝕏 で音色をシェア</button>
      <button class="btn btn-ghost" id="copyBtn">結果をコピー</button>
    </div>
  </section>
"""

JS = r"""
(() => {
  const $ = id => document.getElementById(id);
  const N = 8, TAU = Math.PI * 2;
  const cw = $('otWave'), cb = $('otBars'), cs = $('otSpec');
  const xw = cw.getContext('2d'), xb = cb.getContext('2d'), xs = cs.getContext('2d');
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const HUE = n => (200 + (n - 1) * 43) % 360;
  const COL = (n, a) => `hsla(${HUE(n)},78%,${a === undefined ? 46 : 62}%,${a === undefined ? 1 : a})`;

  // ---------- プリセット（倍音の強さ） ----------
  const PRESETS = [
    ['sine', 'サイン波', n => n === 1 ? 1 : 0, null, 'サイン波：倍音がまったくない、いちばん単純な音です。'],
    ['saw', 'のこぎり波', n => 1 / n, null, 'のこぎり波：すべての倍音が「1/n」の強さ（2倍は1/2、3倍は1/3…）で入っています。'],
    ['square', '四角い波', n => n % 2 ? 1 / n : 0, null, '四角い波：奇数倍（1・3・5・7倍）だけが「1/n」の強さで入っています。偶数倍はありません。'],
    ['tri', '三角波', n => n % 2 ? 1 / (n * n) : 0, n => n % 4 === 3 ? -1 : 1, '三角波：奇数倍だけが「1/n²」の強さで入っています（3倍と7倍は上下さかさまにして足しています）。'],
    ['flute', 'フルート風', n => [1, .45, .2, .1, .04, .02, 0, 0][n - 1], null, 'フルート風：基本の音が強く、倍音は少なめ、という模式的な形です（本物を測った値ではありません）。'],
    ['clar', 'クラリネット風', n => [1, .05, .6, .06, .4, .05, .25, .04][n - 1], null, 'クラリネット風：奇数倍の倍音が強い、と一般に言われる特ちょうをまねた模式的な形です（本物を測った値ではありません）。'],
  ];
  const NOTES = [['ド', 261.63], ['レ', 293.66], ['ミ', 329.63], ['ファ', 349.23], ['ソ', 392.0], ['ラ', 440.0], ['シ', 493.88], ['ド', 523.25]];

  const amp = new Array(N).fill(0), sgn = new Array(N).fill(1);
  let preset = 'saw', f = 261.63, speed = .5, phase = 0, sc = 1.2, peak = 0, dirty = true;

  function calcPeak() {
    let m = 0;
    for (let i = 0; i < 720; i++) { const x = i / 720 * TAU; let y = 0; for (let n = 1; n <= N; n++) y += sgn[n - 1] * amp[n - 1] * Math.sin(n * x); m = Math.max(m, Math.abs(y)); }
    return m;
  }
  const total = () => amp.reduce((a, b) => a + b, 0);
  function strongest() { let k = -1, m = .005; for (let i = 0; i < N; i++) if (amp[i] > m) { m = amp[i]; k = i; } return k + 1; }
  const count = () => amp.slice(1).filter(v => v > .005).length;

  // ---------- 音（押したときだけ・小さく） ----------
  const AC = window.AudioContext || window.webkitAudioContext;
  const VOL = .07;
  let audioOK = !!AC, ac = null, osc = null, gain = null, playing = false, apT = 0, apTm = 0;
  function mkWave() { const re = new Float32Array(N + 1), im = new Float32Array(N + 1); for (let n = 1; n <= N; n++) im[n] = sgn[n - 1] * amp[n - 1]; return ac.createPeriodicWave(re, im); }
  function applyAudio() {
    if (!playing || !osc) return;
    try {
      const t = ac.currentTime;
      if (total() < .005) gain.gain.setTargetAtTime(0, t, .02);
      else { osc.setPeriodicWave(mkWave()); gain.gain.setTargetAtTime(VOL, t, .03); }
      osc.frequency.setTargetAtTime(f, t, .02);
    } catch (e) {}
  }
  function touchAudio() { if (!playing) return; const now = performance.now(); clearTimeout(apTm); if (now - apT > 40) { apT = now; applyAudio(); } else apTm = setTimeout(applyAudio, 50); }
  function startAudio() {
    if (!audioOK) return;
    try {
      if (!ac) ac = new AC();
      if (ac.state === 'suspended') ac.resume();
      osc = ac.createOscillator(); gain = ac.createGain(); gain.gain.value = 0;
      osc.connect(gain); gain.connect(ac.destination); osc.frequency.value = f;
      if (total() >= .005) osc.setPeriodicWave(mkWave());
      osc.start(); playing = true; applyAudio();
    } catch (e) { audioOK = false; playing = false; osc = null; gain = null; }
    updPlay();
  }
  function stopAudio(fast) {
    if (!playing) return;
    playing = false; clearTimeout(apTm);
    try { const t = ac.currentTime; gain.gain.cancelScheduledValues(t); gain.gain.setTargetAtTime(0, t, fast ? .004 : .015); osc.stop(t + (fast ? .03 : .12)); } catch (e) {}
    osc = null; gain = null; updPlay();
  }
  function updPlay() {
    const b = $('otPlay');
    b.textContent = playing ? '⏹ 音を止める' : '🔊 音を鳴らす'; b.classList.toggle('on', playing); b.setAttribute('aria-pressed', playing ? 'true' : 'false');
    if (!audioOK) { b.disabled = true; b.style.opacity = .5; $('otANote').textContent = 'この環境では音を鳴らせません。波形の表示だけでお使いください。'; }
  }
  $('otPlay').addEventListener('click', () => { playing ? stopAudio(false) : startAudio(); });
  document.addEventListener('visibilitychange', () => { if (document.hidden) stopAudio(true); });
  window.addEventListener('pagehide', () => stopAudio(true));
  window.addEventListener('blur', () => { if (document.hidden) stopAudio(true); });

  // ---------- 描く ----------
  let dpr = 1;
  function fit(c) {
    const w = c.clientWidth || 600, h = c.clientHeight || 200;
    const W = Math.round(w * dpr), Hh = Math.round(h * dpr);
    if (c.width !== W || c.height !== Hh) { c.width = W; c.height = Hh; return true; }
    return false;
  }
  function drawWave() {
    const c = xw, W = cw.width, Hh = cw.height, y0 = Hh / 2, k = Hh * .45 / sc;
    c.setTransform(1, 0, 0, 1, 0, 0);
    c.fillStyle = '#0b1220'; c.fillRect(0, 0, W, Hh);
    c.strokeStyle = 'rgba(148,163,184,.13)'; c.lineWidth = 1 * dpr; c.beginPath();
    for (let i = 1; i < 8; i++) { const x = Math.round(W * i / 8) + .5; c.moveTo(x, 0); c.lineTo(x, Hh); }
    for (let i = 1; i < 6; i++) { const y = Math.round(Hh * i / 6) + .5; c.moveTo(0, y); c.lineTo(W, y); }
    c.stroke();
    c.strokeStyle = 'rgba(148,163,184,.45)'; c.beginPath(); c.moveTo(0, y0); c.lineTo(W, y0); c.stroke();
    c.setLineDash([6 * dpr, 6 * dpr]); c.strokeStyle = 'rgba(148,163,184,.4)'; c.beginPath();
    c.moveTo(0, y0 - k); c.lineTo(W, y0 - k); c.moveTo(0, y0 + k); c.lineTo(W, y0 + k); c.stroke(); c.setLineDash([]);
    const st = Math.max(1, dpr), kx = 2 * TAU / W;
    c.lineJoin = 'round'; c.lineCap = 'round';
    for (let n = 1; n <= N; n++) {
      const a = sgn[n - 1] * amp[n - 1]; if (amp[n - 1] < .005) continue;
      c.strokeStyle = COL(n, .6); c.lineWidth = 1.3 * dpr; c.beginPath();
      for (let x = 0; x <= W; x += st) { const y = y0 - a * Math.sin(n * (x * kx - phase)) * k; x ? c.lineTo(x, y) : c.moveTo(x, y); }
      c.stroke();
    }
    c.strokeStyle = '#fde047'; c.lineWidth = 3.4 * dpr; c.shadowColor = 'rgba(253,224,71,.55)'; c.shadowBlur = 8 * dpr; c.beginPath();
    for (let x = 0; x <= W; x += st) {
      const th = x * kx - phase; let y = 0;
      for (let n = 1; n <= N; n++) y += sgn[n - 1] * amp[n - 1] * Math.sin(n * th);
      const py = y0 - y * k; x ? c.lineTo(x, py) : c.moveTo(x, py);
    }
    c.stroke(); c.shadowBlur = 0;
  }
  const BP = { t: 12, b: 8 };
  function drawBars() {
    const c = xb, W = cb.width, Hh = cb.height, cwd = W / N, t = BP.t * dpr, b = BP.b * dpr, h = Hh - t - b;
    c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, W, Hh);
    c.strokeStyle = '#e2e8f0'; c.lineWidth = 1 * dpr; c.beginPath();
    [0, .5, 1].forEach(v => { const y = Math.round(t + h * (1 - v)) + .5; c.moveTo(0, y); c.lineTo(W, y); }); c.stroke();
    for (let n = 1; n <= N; n++) {
      const x = (n - 1) * cwd, bw = Math.min(cwd * .56, 46 * dpr), bx = x + (cwd - bw) / 2, v = amp[n - 1], y = t + h * (1 - v);
      c.fillStyle = '#e2e8f0'; c.fillRect(bx, t, bw, h);
      c.fillStyle = COL(n); c.fillRect(bx, y, bw, t + h - y);
      c.fillStyle = '#0f172a'; c.fillRect(bx - 4 * dpr, y - 2.5 * dpr, bw + 8 * dpr, 5 * dpr);
    }
  }
  function drawSpec() {
    const c = xs, W = cs.width, Hh = cs.height, cwd = W / N, t = 8 * dpr, base = Hh - 20 * dpr, h = base - t;
    c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, W, Hh);
    c.strokeStyle = '#94a3b8'; c.lineWidth = 1.2 * dpr; c.beginPath(); c.moveTo(0, base + .5); c.lineTo(W, base + .5); c.stroke();
    c.font = `${10.5 * dpr}px system-ui,sans-serif`; c.textAlign = 'center'; c.textBaseline = 'top';
    for (let n = 1; n <= N; n++) {
      const x = (n - .5) * cwd, v = amp[n - 1], y = base - h * v;
      c.fillStyle = '#64748b'; c.fillText(String(Math.round(n * f)), x, base + 5 * dpr);
      if (v < .005) { c.fillStyle = '#cbd5e1'; c.beginPath(); c.arc(x, base, 2.5 * dpr, 0, 7); c.fill(); continue; }
      c.strokeStyle = COL(n); c.lineWidth = 4 * dpr; c.lineCap = 'round'; c.beginPath(); c.moveTo(x, base); c.lineTo(x, y); c.stroke();
      c.fillStyle = COL(n); c.beginPath(); c.arc(x, y, 5 * dpr, 0, 7); c.fill();
    }
  }
  function draw() {
    dpr = Math.min(2, window.devicePixelRatio || 1);
    fit(cw); if (fit(cb)) dirty = true; if (fit(cs)) dirty = true;
    drawWave();
    if (dirty) { drawBars(); drawSpec(); dirty = false; }
  }

  // ---------- 数字とひとこと ----------
  function refresh() {
    peak = calcPeak(); dirty = true;
    const s = strongest();
    $('mF').innerHTML = Math.round(f) + '<small>Hz</small>';
    $('mTop').innerHTML = s === 0 ? 'なし' : s === 1 ? '基本<small>（1倍）</small>' : s + '<small>倍</small>';
    $('mCnt').innerHTML = count() + '<small>こ</small>';
    $('mPeak').textContent = peak.toFixed(2);
    for (let n = 1; n <= N; n++) $('otV' + n).textContent = Math.round(amp[n - 1] * 100) + '%';
    document.querySelectorAll('#otPresets button').forEach(b => b.classList.toggle('on', b.dataset.k === preset));
    const p = PRESETS.find(q => q[0] === preset);
    $('otNote').textContent = '🎹 ' + (p ? p[4] : total() < .005 ? 'すべての音が0です。棒を上げると波があらわれます。' : 'じぶんで作った音色です。倍音の強さを変えると、波の形（音色）が変わります。');
    $('vF').textContent = Math.round(f) + 'Hz';
    $('vSp').textContent = speed === 0 ? '止まっている' : '1秒に波' + speed.toFixed(2) + 'こ分';
    $('otTime').textContent = `画面には波2つ分が見えています。本当は1秒間に${Math.round(f)}回ふるえる速さ（1回のふるえは約${(1000 / f).toFixed(1)}ミリ秒）なので、ゆっくりにして見せています。`;
    document.querySelectorAll('#otKeys button').forEach(b => b.classList.toggle('on', Math.abs(+b.dataset.f - f) < .01));
  }

  // ---------- 操作 ----------
  function flash(s) { const el = $('otMsg'); el.textContent = s; el.classList.add('show'); clearTimeout(flash.t); flash.t = setTimeout(() => el.classList.remove('show'), 2200); }
  function setPreset(k) {
    const p = PRESETS.find(q => q[0] === k); if (!p) return;
    preset = k; for (let n = 1; n <= N; n++) { amp[n - 1] = p[2](n); sgn[n - 1] = p[3] ? p[3](n) : 1; }
    refresh(); touchAudio();
  }
  function setAmp(i, v) { v = clamp(v, 0, 1); if (v < .03) v = 0; if (v > .97) v = 1; if (amp[i] === v) return; amp[i] = v; preset = ''; refresh(); touchAudio(); }
  function setF(v) { f = clamp(v, 110, 880); $('kF').value = Math.round(f); refresh(); touchAudio(); }
  $('otPresets').innerHTML = PRESETS.map(p => `<button type="button" data-k="${p[0]}">${p[1]}</button>`).join('');
  $('otPresets').addEventListener('click', e => { const b = e.target.closest('button'); if (b) setPreset(b.dataset.k); });
  $('otLab').innerHTML = Array.from({ length: N }, (_, i) => `<div><b>${i + 1}倍</b><span id="otV${i + 1}">0%</span></div>`).join('');
  $('otKeys').innerHTML = NOTES.map(q => `<button type="button" data-f="${q[1]}">${q[0]}</button>`).join('');
  $('otKeys').addEventListener('click', e => { const b = e.target.closest('button'); if (b) setF(+b.dataset.f); });
  $('kF').addEventListener('input', e => { f = +e.target.value; refresh(); touchAudio(); });
  $('kSp').addEventListener('input', e => { speed = +e.target.value; refresh(); });
  let down = false;
  function barAt(e) {
    const r = cb.getBoundingClientRect(); if (!r.width || !r.height) return;
    const i = clamp(Math.floor((e.clientX - r.left) / r.width * N), 0, N - 1);
    const v = 1 - (e.clientY - r.top - BP.t) / (r.height - BP.t - BP.b);
    setAmp(i, v);
  }
  cb.addEventListener('pointerdown', e => { down = true; try { cb.setPointerCapture(e.pointerId); } catch (err) {} barAt(e); e.preventDefault(); });
  cb.addEventListener('pointermove', e => { if (down) { barAt(e); e.preventDefault(); } });
  const up = () => { down = false; };
  cb.addEventListener('pointerup', up); cb.addEventListener('pointercancel', up); cb.addEventListener('lostpointercapture', up);

  // ---------- シェア ----------
  function shareText() {
    const s = strongest(), p = PRESETS.find(q => q[0] === preset);
    return `倍音を足して音をつくりました🎹 ${p ? p[1] : 'じぶんの音色'}（基本の音${Math.round(f)}Hz・いちばん強い音は${s === 0 ? 'なし' : s === 1 ? '基本の音' : s + '倍の倍音'}・倍音${count()}こ・波の高さの最大${peak.toFixed(2)}）`;
  }
  $('shareBtn').addEventListener('click', () => { const u = location.origin + location.pathname; window.open('https://twitter.com/intent/tweet?text=' + encodeURIComponent(shareText() + '\n') + '&url=' + encodeURIComponent(u) + '&hashtags=' + encodeURIComponent('シミュラボ'), '_blank', 'noopener'); });
  $('copyBtn').addEventListener('click', async () => { try { await navigator.clipboard.writeText(shareText() + '\n' + location.origin + location.pathname); flash('コピーしました'); } catch (e) { flash('コピーできませんでした'); } });

  // ---------- 動かす ----------
  function advance(dt) {
    phase = (phase + TAU * speed * dt) % TAU;
    const target = Math.max(1.2, peak * 1.12);
    sc += (target - sc) * Math.min(1, dt * 8);
  }
  let tPrev = performance.now();
  function loop(now) {
    const dt = Math.min(.05, Math.max(0, (now - tPrev) / 1000)); tPrev = now;
    advance(dt); draw(); requestAnimationFrame(loop);
  }
  setPreset('saw'); $('kF').value = Math.round(f); updPlay();
  window.addEventListener('resize', () => { dirty = true; });
  requestAnimationFrame(loop);
  window.__t = {
    step(sec) { const n = Math.max(1, Math.round((sec || 0) * 60)); for (let i = 0; i < n; i++) advance(1 / 60); dirty = true; draw(); },
    get s() { return { amp: amp.slice(), sgn: sgn.slice(), f, speed, phase, preset, playing, audioOK, peak, scale: sc, strongest: strongest(), count: count() }; },
    setPreset, setAmp, setF,
  };
})();
"""


def esc(s): return H.escape(s, quote=True)


def build():
    url = f"{BASE}/sims/{SLUG}/"
    ld_app = {"@context": "https://schema.org", "@type": "WebApplication", "name": NAME, "url": url, "description": DESC,
              "applicationCategory": "EducationalApplication", "operatingSystem": "Any", "inLanguage": "ja", "isAccessibleForFree": True,
              "offers": {"@type": "Offer", "price": "0", "priceCurrency": "JPY"}}
    ld_bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "ホーム", "item": BASE + "/"}, {"@type": "ListItem", "position": 2, "name": NAME, "item": url}]}
    ld_faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    rel = "".join(f'<a class="related-card" href="../{s}/"><span class="e">{e}</span><span>{esc(t)}</span></a>' for s, e, t in REL)
    faq = "".join(f"<dt>{esc(q)}</dt><dd>{a}</dd>" for q, a in FAQ)
    refs = "".join(f"<li>{r}</li>" for r in REFS)
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- seo-head -->
    <link rel="icon" type="image/svg+xml" href="../../favicon.svg">
    <link rel="icon" type="image/png" sizes="32x32" href="../../favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="../../favicon-16x16.png">
    <link rel="apple-touch-icon" href="../../apple-touch-icon.png">
    <meta property="og:site_name" content="シミュラボ">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{BASE}/ogp/{SLUG}.png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="{BASE}/ogp/{SLUG}.png">
<title>{esc(TITLE)}</title>
<meta name="description" content="{esc(DESC)}">
<meta property="og:title" content="{esc(OG_T)}">
<meta property="og:description" content="{esc(OG_D)}">
<meta property="og:type" content="website">
<link rel="stylesheet" href="../../assets/style.css?v=4">
    <!-- seo-internal -->
    <link rel="canonical" href="{url}">
    <meta property="og:locale" content="ja_JP">
    <meta name="robots" content="index,follow">
    <script type="application/ld+json">{json.dumps(ld_app, ensure_ascii=False)}</script>
    <script type="application/ld+json">{json.dumps(ld_bc, ensure_ascii=False)}</script>
    <script type="application/ld+json">{json.dumps(ld_faq, ensure_ascii=False)}</script>
    <!-- ga4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-R72MT9H7PT"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","G-R72MT9H7PT");</script>
    <!-- adsense -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4521532459480990"
         crossorigin="anonymous"></script>
{STAGE}
</head>
<body>

<header class="site-header">
  <div class="inner">
    <a class="brand" href="../../">
      <span class="mark">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M9 3h6M10 3v5.2L5.4 16.4A2.4 2.4 0 0 0 7.5 20h9a2.4 2.4 0 0 0 2.1-3.6L14 8.2V3" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M7.7 14.5h8.6" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/>
          <circle cx="10.3" cy="16.7" r="1" fill="#fff"/>
          <circle cx="13.4" cy="17.4" r=".7" fill="#fff"/>
        </svg>
      </span>
      <span class="name">シミュ<b>ラボ</b></span>
    </a>
    <span class="spacer"></span>
    <a class="back" href="../../">← 一覧へ</a>
  </div>
</header>

<main class="wrap">

  <nav class="breadcrumb" aria-label="breadcrumb"><a href="../../">ホーム</a><span>›</span>{esc(CAT)}<span>›</span><span class="cur">{esc(NAME)}</span></nav>

  <div class="sim-head">
    <div class="cat">{esc(CAT)}</div>
    <h1>{H1}</h1>
    <p class="lead">{esc(LEAD)}</p>
  </div>
{BODY}
  <article class="article">
{ARTICLE}
    <h2>よくある質問</h2>
    <dl class="faq">{faq}</dl>
    <h2>参考にした資料</h2>
    <ul class="seo-refs">{refs}</ul>
  </article>

  <nav class="related" aria-label="related">
    <h2>関連するシミュレーター</h2>
    <div class="related-grid">{rel}</div>
  </nav>

  <section class="req-banner">
    <h2>💡 こんなシミュレーターも見てみたい？</h2>
    <p>あなたの「これシミュレーションしてみたい」を送ってください。面白い案から実際に作って、できたらお知らせします。</p>
    <a class="btn btn-primary" style="width:auto;display:inline-flex;padding:14px 30px;" href="../../request/">リクエストする →</a>
  </section>

</main>

<footer class="site-footer">
  <div class="inner">
    <p><a href="../../">← シミュラボ トップへ戻る</a></p>
    <p style="margin-top:8px;font-size:.85em"><!-- footer-links --><a href="../../about/">運営者情報</a>　<a href="../../privacy/">プライバシーポリシー</a>　<a href="../../terms/">利用規約</a>　<a href="../../contact/">お問い合わせ</a></p>
    <p style="margin-top:10px;opacity:.7">© 2026 シミュラボ</p>
  </div>
</footer>

<script>{JS}</script>
<script src="../../assets/share-counter.js?v=4"></script>
<script>ShareCounter.initSim({{ simId:'{SLUG}', badgeEl:document.getElementById('shareCount'), shareBtnIds:['shareBtn'] }});</script>
<script src="../../assets/lang-toggle.js?v=4"></script>
</body>
</html>
"""


if __name__ == "__main__":
    out = os.path.join(ROOT, "sims", SLUG, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    io.open(out, "w", encoding="utf-8", newline="\n").write(build())
    print("wrote", out)
