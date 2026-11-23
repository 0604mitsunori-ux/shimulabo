# -*- coding: utf-8 -*-
"""クラドニ図形（音で砂が模様になる）シミュレーター（2026-11-24）
   sims/chladni-zukei/index.html を書き出す（冪等）。 使い方: python -X utf8 scripts/gen_chladni_zukei.py"""
import html as H, io, json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://shimulabo.com"
SLUG = "chladni-zukei"
NAME = "クラドニ図形シミュレーター"
CAT = "あそぶ・実験"
TITLE = "クラドニ図形シミュレーター｜音のふるえで砂が模様になる（m・nを変えて節の線を見る）｜シミュラボ"
DESC = ("ふるえる四角い板にまいた砂が、ふるえない場所（節）に集まって模様をつくる「クラドニ図形」のシミュレーター。"
        "m と n のスライダーを動かすと、数千つぶの砂がサーッと流れて別の模様に変わります。＋／−の型の切り替え、ふるえの強さ、音を鳴らすボタンつき。")
OG_T = "クラドニ図形シミュレーター 音で砂が模様になる"
OG_D = "ふるえる板の上で、砂がふるえない場所（節）に集まって模様になる。m と n を変えると砂が流れて別の模様に。"
H1 = "クラドニ図形シミュレーター<br>音で砂が模様になる"
LEAD = ("黒い板の上に、砂を数千つぶまきました。板がふるえると、砂はふるえの大きい所ではねて、ふるえない場所（節）に集まり、線の模様をつくります。"
        "m と n を変えると、砂がサーッと動いて別の模様に変わります。")

FAQ = [
    ("クラドニ図形とは何ですか？", "ふるえている板の上に砂などの粉をまいたときにできる模様のことです。板には、大きくふるえる場所と、ほとんどふるえない場所（節）があります。砂は節に集まるので、節の形が線の模様として見えます。ドイツの物理学者エルンスト・クラドニが18世紀の終わりにくわしく調べて発表したので、この名前がついています。"),
    ("なぜ砂は線の上に集まるのですか？", "ふるえの大きい所にある砂は、板にはじかれてあちこちにはねます。はねた先がふるえの小さい所だと、そこではあまりはねなくなります。これをくり返すうちに、砂はふるえない場所（節）にたまっていきます。節は点ではなく線になってつながっているので、砂の線ができます。"),
    ("m と n は何を表していますか？", "このシミュレーターの式の中で、板の横方向と縦方向に波がいくつ入るかを決める数です。大きくするほど節の線がふえて、模様が細かくなります。m と n を入れかえても、できる模様は同じです。"),
    ("「−の型」と「＋の型」は何がちがいますか？", "2つのふるえ方を引き算で重ねるか、足し算で重ねるかのちがいです。同じ m と n でも、型を変えると模様が変わります。−の型では、板の対角線（左上から右下）がかならず節になります。また、−の型で m と n を同じにすると板全体がふるえなくなるので、このシミュレーターでは自動で1つずらしています。"),
    ("鳴る音は、本物の板の音と同じですか？", "いいえ、同じではありません。このシミュレーターの音の高さは「m×m＋n×n に比例する」とした模式的な値で、模様が細かいほど音が高くなることを感じてもらうためのものです。本物の板の音の高さは、板の材料・厚さ・大きさ・支え方で決まります。"),
]
REL = [("unari-teijouha", "🎸", "うなり・定常波（定在波）シミュレーター"), ("wave", "🌊", "波の干渉シミュレーター"), ("lissajous", "➰", "リサージュ図形")]

ARTICLE = """
<h2>このシミュレーターのしくみ</h2>
<p>板のふるえ方は、正方形の板でよく使われる次の近似式で決めています（x・y は板の上の位置で、どちらも 0〜1）。</p>
<p class="ch-formula">ふるえの大きさ ＝ cos(nπx)·cos(mπy) <b>−</b> cos(mπx)·cos(nπy)</p>
<p>まん中の符号を <b>＋</b> にしたものが「＋の型」です。この値が 0 になる場所が<b>節（ふし）</b>で、板がふるえていてもそこだけは動きません。</p>
<p>砂は、次のかんたんな規則で動かしています。</p>
<ul>
<li>砂つぶは1つぶずつ、1秒間に60回、でたらめな向きにはねます。</li>
<li>はねる大きさは、その場所の<b>ふるえの大きさに比例</b>します。ふるえが大きい所ほど、遠くまではねます。</li>
<li>ふるえがとても小さい所（節のすぐ近く）に入った砂は、もう動きません。止まる場所は砂つぶごとに少しずつちがうので、線に太さが出ます。</li>
</ul>
<p>なお、模様が細かいとき（m・n が大きいとき）は、見やすいように全体のはね方を少し小さくしています。</p>
<p>「節のほうへ進め」という命令は入れていません。それでも、よくはねる所からは砂が出ていき、はねない所には砂がたまるので、しぜんに節の線がうかび上がります。「節に集まった砂」の数字は、ふるえの大きさがいちばん大きい所の10%より小さい場所にある砂の割合です。</p>

<h2>ためしてみたいこと</h2>
<ul>
<li><b>m か n を1つだけ変える</b>：できあがった模様がくずれ、砂が流れて新しい模様にまとまります。節の場所が変わると、今までの場所が「ふるえる所」になるからです。</li>
<li><b>m と n を大きくする</b>：節の線がふえて、模様が細かくなります。音を鳴らしていると、音も高くなります。</li>
<li><b>＋と−を切りかえる</b>：同じ m・n でも模様が変わります。−の型では、対角線（左上から右下）にかならず砂の線ができます。</li>
<li><b>ふるえの強さを変える</b>：強くすると砂が速く動き、線は細くなります。弱くすると、砂は節の少し手前で止まるので、線が太くなります。</li>
<li><b>板をタップして砂をまく</b>：ふるえの大きい所にまくと、すぐにちっていきます。節の上にまくと、そのまま動きません。</li>
<li><b>「ふるえの大きさを色で見る」をおす</b>：青く光っている所が、よくふるえている所です。砂の線が、青くない所を通っていることをたしかめられます。</li>
</ul>

<h2>本物では</h2>
<p>ドイツの物理学者エルンスト・クラドニ（1756〜1827）は、金属の板に砂をまき、板のふちをバイオリンの弓でこすって鳴らすと、音の高さによってちがう模様ができることを調べ、1787年に本にまとめて発表しました。目に見えない音のふるえを、目で見えるようにした実験として知られています。</p>
<p>クラドニは1808年ごろにパリでこの実験をひろうし、それを見たナポレオンは、模様を数学で説明した人に賞を出すことにしました。この問題に取り組んだのがフランスの数学者ソフィ・ジェルマンで、1816年に賞を受けています。</p>
<p>今では弓のかわりに、スピーカーや振動を出す機械を板の中心に取りつけて実験することが多くなっています。弦楽器の板のふるえ方を調べるのにも、同じ方法が使われてきました。</p>
<p><b>単純にしているところ：</b>このシミュレーターの式は近似です。ふちが自由に動ける本物の板のふるえ方はもっと複雑で、かんたんな式では書けません（20世紀のはじめにリッツが近似の計算方法を示しました）。そのため、本物の模様は線が曲がっていたり、ここで見える模様と少しちがっていたりします。砂の動かし方も、本物の砂が板の上ではねるようすをとても単純にしたものです。また、とても細かい粉は、砂とは反対に、ふるえの大きい所に集まることがあります。</p>
"""

REFS = [
    "E. F. F. Chladni (1787) Entdeckungen über die Theorie des Klanges. Leipzig.（クラドニ図形を最初にまとめた本）",
    "Lord Rayleigh (1877) The Theory of Sound. Macmillan.（板の振動と節の線の説明）",
    "W. Ritz (1909) Theorie der Transversalschwingungen einer quadratischen Platte mit freien Rändern. Annalen der Physik 28, 737–786.（ふちが自由な正方形の板の近似計算）",
]

STAGE = r"""
<style>
#chWrap{position:relative;max-width:560px;margin:0 auto;border-radius:14px;overflow:hidden;background:#06060a;border:1px solid #2b2716;box-shadow:0 10px 30px rgba(20,16,4,.25)}
#ch{display:block;width:100%;aspect-ratio:1/1;touch-action:pan-y;cursor:crosshair}
.ch-msg{position:absolute;left:50%;bottom:10px;transform:translateX(-50%);background:rgba(250,245,225,.92);color:#1c1917;font-size:12.5px;font-weight:700;border-radius:12px;padding:6px 14px;max-width:92%;text-align:center;pointer-events:none;opacity:0;transition:opacity .3s}
.ch-msg.show{opacity:1}
.ch-hint{font-size:13px;color:var(--ink-2);margin:8px 0 0;text-align:center}
.ch-sum{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:12px}
.ch-sum div{background:#fbf6e6;border-radius:12px;padding:10px 4px;text-align:center;min-width:0}
.ch-sum b{display:block;font-size:20px;color:#92400e;font-variant-numeric:tabular-nums}
.ch-sum b small{font-size:11.5px}
.ch-sum span{font-size:11.5px;color:var(--ink-2);font-weight:700}
.ch-note{font-size:13.5px;color:var(--ink);background:#fbf6e6;border-radius:10px;padding:9px 12px;margin:10px 0 0;font-weight:700}
.ch-cols{display:grid;grid-template-columns:1fr 1fr;gap:6px 22px;margin-top:14px}
.ch-seg{display:flex;flex-wrap:wrap;gap:6px}
.ch-seg button{border:1.5px solid var(--line);background:#fff;border-radius:999px;padding:8px 13px;font:inherit;font-size:13.5px;font-weight:800;cursor:pointer;color:var(--ink)}
.ch-seg button.on{background:#92400e;border-color:#92400e;color:#fff}
.ch-seg button.snd.on{background:#b91c1c;border-color:#b91c1c}
.ch-sub{font-size:12.5px;color:var(--ink-2);margin:6px 0 0}
.article p.ch-formula{background:#14110a;color:#fde9a8;border-radius:10px;padding:10px 12px;font-size:14px;overflow-wrap:anywhere;text-align:center}
.article p.ch-formula b{color:#fff}
@media (max-width:640px){.ch-sum{grid-template-columns:repeat(2,1fr)}.ch-cols{grid-template-columns:1fr}}
</style>
"""

BODY = r"""
  <section class="panel" id="resultPanel">
    <div id="chWrap">
      <canvas id="ch" aria-label="黒い板の上で、砂が節の線に集まってできるクラドニ図形"></canvas>
      <div class="ch-msg" id="chMsg"></div>
    </div>
    <p class="ch-hint">板をタップ（クリック）すると、そこに砂をまけます。</p>
    <div class="ch-sum">
      <div><b id="mM">3</b><span>m</span></div>
      <div><b id="mN">5</b><span>n</span></div>
      <div><b id="mNode">0<small>%</small></b><span>節に集まった砂</span></div>
      <div><b id="mHz">0<small>Hz</small></b><span>音の高さの目安（模式的）</span></div>
    </div>
    <p class="ch-note" id="chNote">砂が動いています。</p>

    <div class="ch-cols">
      <div class="field"><label>m <span class="hint">（<b id="vM">3</b>）</span></label><input type="range" id="kM" min="1" max="8" step="1" value="3"></div>
      <div class="field"><label>n <span class="hint">（<b id="vN">5</b>）</span></label><input type="range" id="kN" min="1" max="8" step="1" value="5"></div>
      <div class="field"><label>型（式のまん中の符号）</label><div class="ch-seg" id="chSign"><button type="button" data-v="-1" class="on">− の型</button><button type="button" data-v="1">＋ の型</button></div></div>
      <div class="field"><label>ふるえの強さ <span class="hint">（<b id="vP">ふつう</b>）</span></label><input type="range" id="kP" min="0.4" max="2" step="0.1" value="1"></div>
    </div>

    <div class="ch-seg" style="margin-top:12px">
      <button type="button" id="chScatter">🌾 砂をまき直す</button>
      <button type="button" id="chPlay">⏸ ふるえを止める</button>
      <button type="button" id="chSound" class="snd" aria-pressed="false">🔊 音を鳴らす</button>
      <button type="button" id="chField" aria-pressed="false">🎨 ふるえの大きさを色で見る</button>
    </div>
    <p class="ch-sub">音は、ボタンをおしたときだけ小さめに鳴ります。もう一度おすと止まり、15秒たつと自動で止まります。音の高さは模式的な値です。</p>

    <div class="field" style="margin-top:14px"><label>模様をえらぶ</label><div class="ch-seg" id="chPre"></div></div>

    <div style="text-align:center;margin-top:16px;"><span id="shareCount" class="share-count" style="display:none"></span></div>
    <div class="share-row">
      <button class="btn btn-x" id="shareBtn">𝕏 で模様をシェア</button>
      <button class="btn btn-ghost" id="copyBtn">結果をコピー</button>
    </div>
  </section>
"""

JS = r"""
(() => {
  const $ = id => document.getElementById(id);
  const cv = $('ch'), ctx = cv.getContext('2d');
  const PI = Math.PI, N = 6000, NODE = 0.1, DT = 1 / 60;
  const px = new Float32Array(N), py = new Float32Array(N);
  const COL = ['#fff8dc', '#ffe7a3', '#f6c761', '#ffffff', '#e9b949'];
  let m = 3, n = 5, sign = -1, power = 1, running = true, showField = false;
  let t = 0, nodeFrac = 0, moving = 1, cur = 0, settledAt = -1;

  // でたらめな数（xorshift）
  let rs = 2463534242;
  function rnd() { rs ^= rs << 13; rs ^= rs >>> 17; rs ^= rs << 5; return (rs >>> 0) / 4294967296; }

  // ---------- 板のふるえ方（−1〜1） ----------
  function U(x, y) { return (Math.cos(n * PI * x) * Math.cos(m * PI * y) + sign * Math.cos(m * PI * x) * Math.cos(n * PI * y)) / 2; }
  const freq = () => 30 * (m * m + n * n);

  // ---------- 砂 ----------
  function scatter() { for (let i = 0; i < N; i++) { px[i] = rnd(); py[i] = rnd(); } settledAt = -1; }
  function addSand(x, y) {
    for (let k = 0; k < 220; k++) {
      const a = rnd() * PI * 2, r = Math.sqrt(rnd()) * 0.045;
      px[cur] = Math.min(1, Math.max(0, x + Math.cos(a) * r)); py[cur] = Math.min(1, Math.max(0, y + Math.sin(a) * r));
      cur = (cur + 1) % N;
    }
    settledAt = -1;
  }
  // 1コマ（1/60秒）進める。move=false のときは数えるだけ
  function tick(move) {
    // 模様が細かいほど、全体のはね方を少し小さくする（見やすさのため）
    const thr = 0.045 / power / 16, k = 0.05 * power * Math.max(.6, Math.min(2, 6 / (m + n)));
    let cnt = 0, mv = 0;
    for (let i = 0; i < N; i++) {
      let x = px[i], y = py[i];
      const a = Math.abs(U(x, y));
      if (a < NODE) cnt++;
      // 止まる深さは砂つぶごとに少しずつちがう（線に太さが出る）
      if (move && a > thr * ((i & 15) + 1)) {
        const s = k * a * 2;
        x += (rnd() - .5) * s; y += (rnd() - .5) * s;
        if (x < 0) x = -x; else if (x > 1) x = 2 - x;
        if (y < 0) y = -y; else if (y > 1) y = 2 - y;
        px[i] = x; py[i] = y; mv++;
      }
    }
    nodeFrac = cnt / N; moving = mv / N;
    if (move) { t += DT; if (settledAt < 0 && nodeFrac > .9) settledAt = t; }
  }

  // ---------- ふるえの大きさの色 ----------
  let fieldCv = null;
  function buildField() {
    const S = 128; if (!fieldCv) { fieldCv = document.createElement('canvas'); fieldCv.width = S; fieldCv.height = S; }
    const fx = fieldCv.getContext('2d'), im = fx.createImageData(S, S), d = im.data;
    for (let j = 0; j < S; j++) for (let i = 0; i < S; i++) {
      const a = Math.abs(U((i + .5) / S, (j + .5) / S)), o = (j * S + i) * 4;
      d[o] = 20 + 50 * a * a; d[o + 1] = 30 * a + 60 * a * a; d[o + 2] = 235 * Math.pow(a, .8); d[o + 3] = 255;
    }
    fx.putImageData(im, 0, 0);
  }

  // ---------- 描く ----------
  let dpr = 1;
  function size() {
    const w = cv.clientWidth || 560; dpr = Math.min(2, window.devicePixelRatio || 1);
    const W = Math.round(w * dpr); if (cv.width !== W || cv.height !== W) { cv.width = W; cv.height = W; return true; }
    return false;
  }
  function draw(full) {
    if (size()) full = true;
    const W = cv.width;
    ctx.fillStyle = full ? '#06060a' : 'rgba(6,6,10,.5)'; ctx.fillRect(0, 0, W, W);
    if (showField && fieldCv) { ctx.globalAlpha = full ? .6 : .35; ctx.imageSmoothingEnabled = true; ctx.drawImage(fieldCv, 0, 0, W, W); ctx.globalAlpha = 1; }
    const s = Math.max(1, (W / dpr < 420 ? 1.3 : 1.6) * dpr), h = s / 2;
    for (let c = 0; c < 5; c++) {
      ctx.fillStyle = COL[c];
      for (let i = c; i < N; i += 5) ctx.fillRect(px[i] * W - h, py[i] * W - h, s, s);
    }
    ui();
  }

  // ---------- 数字とひとこと ----------
  let lastUI = 0;
  function ui() {
    const now = performance.now(); if (now - lastUI < 150) return; lastUI = now;
    $('mM').textContent = m; $('mN').textContent = n; $('vM').textContent = m; $('vN').textContent = n;
    $('mNode').innerHTML = Math.round(nodeFrac * 100) + '<small>%</small>';
    $('mHz').innerHTML = '約' + freq().toLocaleString('ja-JP') + '<small>Hz</small>';
    let s;
    if (!running) s = '⏸ ふるえを止めています。砂は動きません。';
    else if (moving > .25) s = '砂がはねて、ふるえない場所（節）へ流れています。';
    else if (nodeFrac > .9) s = '✨ 砂の ' + Math.round(nodeFrac * 100) + '% が節に集まり、模様ができました。m や n を変えてみましょう。';
    else s = '砂が少しずつ節に集まっています。';
    $('chNote').textContent = s;
  }
  function flash(s) { const el = $('chMsg'); el.textContent = s; el.classList.add('show'); clearTimeout(flash.t); flash.t = setTimeout(() => el.classList.remove('show'), 2600); }

  // ---------- 音（おしたときだけ・小さく） ----------
  let ac = null, osc = null, gain = null, sounding = false, sndTimer = 0;
  const vol = () => 0.05 * Math.min(1, Math.sqrt(500 / freq()));
  function soundOn() {
    try {
      const AC = window.AudioContext || window.webkitAudioContext; if (!AC) { flash('このブラウザでは音を出せません'); return; }
      ac = ac || new AC(); if (ac.state === 'suspended') ac.resume();
      osc = ac.createOscillator(); gain = ac.createGain(); osc.type = 'sine'; osc.frequency.value = freq();
      const t0 = ac.currentTime; gain.gain.setValueAtTime(0, t0); gain.gain.linearRampToValueAtTime(vol(), t0 + .08);
      osc.connect(gain); gain.connect(ac.destination); osc.start();
      sounding = true; clearTimeout(sndTimer); sndTimer = setTimeout(() => { if (sounding) { soundOff(); flash('15秒たったので音を止めました'); } }, 15000);
    } catch (e) { sounding = false; osc = null; flash('音を出せませんでした'); }
    updSound();
  }
  function soundOff() {
    clearTimeout(sndTimer);
    if (osc && ac) { try { const t0 = ac.currentTime; gain.gain.cancelScheduledValues(t0); gain.gain.setValueAtTime(gain.gain.value, t0); gain.gain.linearRampToValueAtTime(0, t0 + .05); osc.stop(t0 + .08); } catch (e) {} }
    osc = null; sounding = false; updSound();
  }
  function retune() { if (sounding && osc && ac) { try { const t0 = ac.currentTime; osc.frequency.setTargetAtTime(freq(), t0, .04); gain.gain.setTargetAtTime(vol(), t0, .04); } catch (e) {} } }
  function updSound() { const b = $('chSound'); b.classList.toggle('on', sounding); b.setAttribute('aria-pressed', sounding ? 'true' : 'false'); b.textContent = sounding ? '🔇 音を止める' : '🔊 音を鳴らす'; }
  $('chSound').addEventListener('click', () => { sounding ? soundOff() : soundOn(); });
  document.addEventListener('visibilitychange', () => { if (document.hidden && sounding) soundOff(); });
  window.addEventListener('pagehide', () => { if (sounding) soundOff(); });

  // ---------- 操作 ----------
  const PRE = [[1, 2, -1], [1, 3, 1], [2, 4, -1], [3, 5, -1], [3, 5, 1], [4, 7, -1], [5, 8, 1], [6, 7, -1]];
  function apply(o, from) {
    if (o.m != null) m = Math.max(1, Math.min(8, Math.round(o.m)));
    if (o.n != null) n = Math.max(1, Math.min(8, Math.round(o.n)));
    if (o.sign != null) sign = o.sign < 0 ? -1 : 1;
    if (o.power != null) power = Math.max(.4, Math.min(2, +o.power));
    if (sign < 0 && m === n) {
      if (from === 'n') m = m < 8 ? m + 1 : m - 1; else n = n < 8 ? n + 1 : n - 1;
      flash('−の型では m と n を同じにできないので、1つずらしました');
    }
    $('kM').value = m; $('kN').value = n; $('kP').value = power;
    $('vP').textContent = power < .75 ? '弱い' : power <= 1.3 ? 'ふつう' : '強い';
    document.querySelectorAll('#chSign button').forEach(b => b.classList.toggle('on', +b.dataset.v === sign));
    document.querySelectorAll('#chPre button[data-i]').forEach(b => { const p = PRE[+b.dataset.i]; b.classList.toggle('on', !!p && p[0] === m && p[1] === n && p[2] === sign); });
    settledAt = -1; buildField(); retune(); tick(false); lastUI = 0;
  }
  $('kM').addEventListener('input', e => apply({ m: +e.target.value }, 'm'));
  $('kN').addEventListener('input', e => apply({ n: +e.target.value }, 'n'));
  $('kP').addEventListener('input', e => apply({ power: +e.target.value }));
  $('chSign').addEventListener('click', e => { const b = e.target.closest('button'); if (b) apply({ sign: +b.dataset.v }); });
  $('chPre').innerHTML = PRE.map((p, i) => `<button type="button" data-i="${i}">m${p[0]}・n${p[1]} ${p[2] < 0 ? '−' : '＋'}</button>`).join('') + '<button type="button" data-r="1">🎲 おまかせ</button>';
  $('chPre').addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    if (b.dataset.r) { let a, c, sg; do { a = 1 + Math.floor(Math.random() * 8); c = 1 + Math.floor(Math.random() * 8); sg = Math.random() < .5 ? -1 : 1; } while (a === c || (a === m && c === n && sg === sign)); apply({ m: a, n: c, sign: sg }); }
    else { const p = PRE[+b.dataset.i]; apply({ m: p[0], n: p[1], sign: p[2] }); }
    if (!running) { running = true; updPlay(); }
  });
  $('chScatter').addEventListener('click', () => { scatter(); tick(false); lastUI = 0; if (!running) { running = true; updPlay(); } flash('砂をまき直しました'); });
  function updPlay() { $('chPlay').textContent = running ? '⏸ ふるえを止める' : '▶ ふるわせる'; lastUI = 0; }
  $('chPlay').addEventListener('click', () => { running = !running; updPlay(); });
  $('chField').addEventListener('click', () => { showField = !showField; const b = $('chField'); b.classList.toggle('on', showField); b.setAttribute('aria-pressed', showField ? 'true' : 'false'); draw(true); });

  // 板をタップ／ドラッグ → そこに砂をまく
  let down = false;
  function ptr(e) { const r = cv.getBoundingClientRect(); if (!r.width) return; addSand((e.clientX - r.left) / r.width, (e.clientY - r.top) / r.height); tick(false); lastUI = 0; }
  cv.addEventListener('pointerdown', e => { down = true; ptr(e); });
  cv.addEventListener('pointermove', e => { if (down) ptr(e); });
  ['pointerup', 'pointercancel', 'pointerleave'].forEach(ev => cv.addEventListener(ev, () => { down = false; }));

  // ---------- シェア ----------
  function shareText() { return `クラドニ図形（m=${m}・n=${n}・${sign < 0 ? '−' : '＋'}の型）で、砂の${Math.round(nodeFrac * 100)}%が節に集まって模様になりました🎻`; }
  $('shareBtn').addEventListener('click', () => { const u = location.origin + location.pathname; window.open('https://twitter.com/intent/tweet?text=' + encodeURIComponent(shareText() + '\n') + '&url=' + encodeURIComponent(u) + '&hashtags=' + encodeURIComponent('シミュラボ'), '_blank', 'noopener'); });
  $('copyBtn').addEventListener('click', async () => { try { await navigator.clipboard.writeText(shareText() + '\n' + location.origin + location.pathname); flash('コピーしました'); } catch (e) { flash('コピーできませんでした'); } });

  // ---------- 動かす ----------
  let tPrev = performance.now(), acc = 0;
  function loop(now) {
    const dt = Math.min(.1, (now - tPrev) / 1000); tPrev = now;
    if (running) { acc += dt; let k = 0; while (acc >= DT && k < 4) { tick(true); acc -= DT; k++; } if (k === 4) acc = 0; }
    draw(false); requestAnimationFrame(loop);
  }
  scatter(); apply({}); draw(true);
  window.addEventListener('resize', () => draw(true));
  requestAnimationFrame(loop);

  // 確認用
  window.__t = {
    step(sec) { const k = Math.max(1, Math.round(sec * 60)); for (let i = 0; i < k; i++) tick(true); lastUI = 0; draw(true); },
    get s() { return { m, n, sign, power, node: +(nodeFrac * 100).toFixed(1), moving: +(moving * 100).toFixed(1), hz: freq(), t: +t.toFixed(2), settledAt: +settledAt.toFixed(2), running, sounding, showField, N }; },
    set(o) { apply(o); }, scatter() { scatter(); tick(false); }, add(x, y) { addSand(x, y); tick(false); }
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
