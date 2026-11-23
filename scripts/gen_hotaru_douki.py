# -*- coding: utf-8 -*-
"""ホタルの光がそろうしくみ（同期）シミュレーター（2026-11-24）
   sims/hotaru-douki/index.html を書き出す（冪等）。 使い方: python -X utf8 scripts/gen_hotaru_douki.py"""
import html as H, io, json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://shimulabo.com"
SLUG = "hotaru-douki"
NAME = "ホタルの光がそろうシミュレーター"
CAT = "ふしぎ・現象"
TITLE = "ホタルの光がそろうしくみ｜同期のシミュレーター（リーダーなしでそろう理由）｜シミュラボ"
DESC = ("夜の川べりを飛ぶたくさんのホタルが、はじめはバラバラに光り、だんだんそろって光るようになるようすを見られるシミュレーター。"
        "ルールは「となりが光ったら、自分の光るタイミングを少し早める」だけ。ホタルの数・まわりを見るきょり・合わせる強さを変えて、そろい方のちがいをたしかめられます。")
OG_T = "ホタルの光がそろうしくみ 同期のシミュレーター"
OG_D = "リーダーはいないのに、だんだんそろって光る。ホタルの数・見るきょり・合わせる強さを変えてためせます。"
H1 = "ホタルの光がそろうしくみ<br>同期のシミュレーター"
LEAD = ("夜の川べりに、ホタルがたくさん飛んでいます。はじめはバラバラに光っていますが、「となりのホタルが光ったら、自分の光るタイミングを少し早める」というルールだけで、"
        "だんだん全体がそろって光るようになります。数やきょり、合わせる強さを変えて、そろい方をくらべてみましょう。")
NOTE = "💡 リーダーはいません。1ぴき1ぴきが、近くの光に少し合わせているだけです。"

FAQ = [
    ("どうやって遊びますか？", "開くと自動で始まります。しばらく見ていると、バラバラだった光がだんだんそろっていきます。「ホタルの数」「まわりを見るきょり」「合わせる強さ」を動かすと、そろう速さやそろい方が変わります。「バラバラにもどす」を押すと、光るタイミングをばらばらにして、もう一度はじめから見られます。"),
    ("「そろい具合」はどうやって計算していますか？", "1ぴきごとの「次に光るまでの進み具合」を時計の針の向きにおきかえて、全員の針の向きがどれくらいそろっているかを0〜100%で表しています。全員が同じ向きなら100%、ばらばらなら0%に近くなります。同期の研究でよく使われる計算のしかたです。"),
    ("合わせる強さを0にするとどうなりますか？", "ほかのホタルの光を見ても何もしないので、いつまでたってもそろいません。それぞれのホタルは光る間かくが少しずつちがうため、ぐうぜんそろって見えても、すぐにずれていきます。"),
    ("本物のホタルも同じルールで光っていますか？", "このシミュレーターは、そろうしくみの考え方を見るために、とても単純にしたものです。本物のホタルは種類によって光り方も合わせ方もちがい、そろって光る種類もあれば、そうでない種類もあります。"),
]
REL = [("boids", "🐦", "鳥の群れシミュレーター（ボイド）"), ("ari-pheromone", "🐜", "アリの行列はなぜできる？"), ("pendulum-wave", "🎐", "振り子の波")]

ARTICLE = """
<h2>このシミュレーターのしくみ</h2>
<p>ホタルは1ぴきずつ、自分の中に<b>「次に光るまでの時計」</b>を持っていると考えます。時計がいっぱいまで進むと光り、またゼロにもどります。ルールは1つだけです。</p>
<ul>
<li><b>近くのホタルが光るのを見たら、自分の時計を少しだけ進める。</b></li>
<li>進める量は、時計がいっぱいに近いホタルほど大きくなります。もうすぐ光るホタルは、となりの光につられてすぐに光ります。</li>
<li>進めた結果いっぱいになったホタルは、その場で光ります。一度いっしょに光ったホタルどうしは、そのあとも同じタイミングで光りつづけます。</li>
</ul>
<p>これをくり返すと、いっしょに光るなかまが少しずつ大きくなり、やがて全体が1つのリズムにまとまります。</p>

<h2>リーダーがいなくてもそろう理由</h2>
<p>だれかが「せーの」と合図を出しているわけではありません。1ぴき1ぴきが、まわりの光に少し合わせているだけです。それでも、近くどうしがそろい、そのかたまりどうしがまたそろい…と広がっていくので、全体がそろいます。</p>
<p>このように、同じリズムをもつものどうしが、おたがいに少しずつ合わせることでリズムがそろう現象を<b>「同期（どうき）」</b>といいます。数学者のミロロとストロガッツは1990年に、このような「光ったしゅんかんに相手を少し進める」しくみのなかまは、条件がそろえば、はじめのタイミングがどうであってもほぼ必ずそろうことを証明しました。</p>

<h2>ためしてみたいこと</h2>
<ul>
<li><b>まわりを見るきょりを「近くだけ」にする</b>：近くのなかまだけでそろうので、場所ごとに光るタイミングがずれて、光の波が広がるように見えることがあります。</li>
<li><b>「遠くまで」にする</b>：全体が一気にそろいやすくなります。</li>
<li><b>合わせる強さを弱くする／強くする</b>：弱いとゆっくり、強いと早くそろいます。0にするとそろいません。</li>
<li><b>ホタルの数を変える</b>：数が少ないと、近くにだれもいないホタルが取り残されることがあります。</li>
<li><b>そろったあとに「バラバラにもどす」を押す</b>：グラフで、そろい具合がもう一度上がっていくようすを見られます。</li>
</ul>

<h2>本物の世界では</h2>
<p>東南アジアの川ぞいでは、木いっぱいに集まったたくさんのホタルが、いっせいにそろって光ることが知られています。昔から旅行者や研究者をおどろかせてきた光景で、研究者のバック夫妻は1960年代に、ホタルがほかのホタルの光に合わせて自分の光るタイミングを調整していることを報告しました。</p>
<p>同じなかまの考え方は、ホタル以外にも使われています。</p>
<ul>
<li><b>心臓のペースメーカー細胞</b>：心臓には、拍動のリズムを作る細胞がたくさん集まった場所があります。1つ1つの細胞がおたがいに合わせることで、全体として1つのリズムになると考えられています。</li>
<li><b>拍手がそろう現象</b>：コンサートのあと、バラバラだった拍手が、いつのまにか手びょうしのようにそろうことがあります。これも、まわりの音に少しずつ合わせることで起きる同期として研究されています。</li>
</ul>
<p>このシミュレーターは、同期の考え方をつかむために、とても単純にしたものです。本物のホタルの光り方を正確に再現したものではありません。</p>
"""

REFS = [
    "Mirollo, R. E. &amp; Strogatz, S. H. (1990) Synchronization of pulse-coupled biological oscillators. SIAM Journal on Applied Mathematics 50(6), 1645–1662.",
    "Buck, J. &amp; Buck, E. (1968) Mechanism of rhythmic synchronous flashing of fireflies. Science 159, 1319–1327.",
    "Peskin, C. S. (1975) Mathematical Aspects of Heart Physiology. Courant Institute of Mathematical Sciences.（心臓のペースメーカー細胞のモデル）",
    "Néda, Z. et al. (2000) The sound of many hands clapping. Nature 403, 849–850.（拍手がそろう現象）",
]

STAGE = r"""
<style>
#htWrap{position:relative;border-radius:14px;overflow:hidden;border:1px solid var(--line);background:#050a1c}
#ht{display:block;width:100%;aspect-ratio:5/3}
.ht-play{position:absolute;left:10px;top:10px;display:flex;gap:6px;flex-wrap:wrap}
.ht-play button{border:0;border-radius:999px;background:rgba(255,255,255,.16);color:#fff;font:inherit;font-weight:800;font-size:12.5px;padding:7px 12px;cursor:pointer;backdrop-filter:blur(4px)}
.ht-play button.on{background:#d9f99d;color:#1a2e05}
.ht-sum{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:12px}
.ht-sum div{background:#f7fee7;border-radius:12px;padding:10px 4px;text-align:center}
.ht-sum b{display:block;font-size:22px;color:#4d7c0f;font-variant-numeric:tabular-nums}
.ht-sum b small{font-size:11.5px}
.ht-sum span{font-size:11.5px;color:var(--ink-2);font-weight:700}
.ht-note{font-size:13.5px;color:var(--ink);background:#f7fee7;border-radius:10px;padding:9px 12px;margin:10px 0 0;font-weight:700}
#htG{display:block;width:100%;height:90px;margin-top:10px}
.ht-glegend{font-size:12px;color:var(--ink-2)}
.ht-glegend i{display:inline-block;width:18px;height:3px;vertical-align:3px;margin-right:4px;background:#65a30d}
.ht-cols{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px 22px;margin-top:14px}
.ht-cols input[type=range]{width:100%}
.ht-btns{display:flex;gap:8px;flex-wrap:wrap;margin-top:8px}
@media (max-width:640px){#ht{aspect-ratio:4/3}.ht-cols{grid-template-columns:1fr}.ht-sum b{font-size:19px}.ht-play button{padding:6px 10px;font-size:12px}}
</style>
"""

BODY = r"""
  <section class="panel" id="resultPanel">
    <div id="htWrap">
      <canvas id="ht" aria-label="夜の川べりでホタルが光っている絵"></canvas>
      <div class="ht-play"><button type="button" id="htPlay">⏸ 止める</button><button type="button" id="htSlow">🐢 スロー</button></div>
    </div>
    <div class="ht-sum">
      <div><b id="mSync">0<small>%</small></b><span>そろい具合</span></div>
      <div><b id="mTog">0<small>ひき</small></b><span>いっしょに光った数</span></div>
      <div><b id="mTime">0<small>秒</small></b><span>経過時間</span></div>
    </div>
    <p class="ht-note" id="htNote">✨ はじめはバラバラに光っています。</p>
    <canvas id="htG" aria-label="そろい具合の変化のグラフ"></canvas>
    <div class="ht-glegend"><span><i></i>そろい具合（さいきん60秒）</span></div>

    <div class="ht-cols">
      <div class="field"><label>ホタルの数 <span class="hint">（<b id="vN"></b>）</span></label><input type="range" id="kN" min="20" max="300" step="10" value="120"></div>
      <div class="field"><label>まわりを見るきょり <span class="hint">（<b id="vR"></b>）</span></label><input type="range" id="kR" min="6" max="100" step="2" value="26"></div>
      <div class="field"><label>合わせる強さ <span class="hint">（<b id="vK"></b>）</span></label><input type="range" id="kK" min="0" max="100" step="5" value="40"></div>
    </div>
    <div class="ht-btns">
      <button class="btn btn-primary" id="htReset" type="button" style="width:auto;padding:10px 18px;">🔀 バラバラにもどす</button>
    </div>

    <div style="text-align:center;margin-top:16px;"><span id="shareCount" class="share-count" style="display:none"></span></div>
    <div class="share-row">
      <button class="btn btn-x" id="shareBtn">𝕏 で結果をシェア</button>
      <button class="btn btn-ghost" id="copyBtn">結果をコピー</button>
    </div>
  </section>
"""

JS = r"""
(() => {
  const $ = id => document.getElementById(id);
  const cv = $('ht'), ctx = cv.getContext('2d'), gc = $('htG'), gx = gc.getContext('2d');
  const MAXN = 300, DT = 1 / 60, YA = .1, YB = .78, RIV = .85;
  let range = .26, K = .024, slow = false, playing = true;
  let F = [], t = 0, binC = 0, binT = 0, bins = [], hist = [], histT = 0, sync = 0, asp = .6;

  // ---------- ホタル ----------
  function mk() { return { x: Math.random(), y: YA + Math.random() * (YB - YA), vx: (Math.random() - .5) * .03, vy: (Math.random() - .5) * .02, ph: Math.random(), T: 2 * (1 + (Math.random() - .5) * .04), lit: 9, w: Math.random() * 6.28 }; }
  function setN(n) { n = Math.max(2, Math.min(MAXN, n | 0)); while (F.length < n) F.push(mk()); F.length = n; }
  function calc() { let sx = 0, sy = 0; for (const f of F) { const a = f.ph * 6.283185307; sx += Math.cos(a); sy += Math.sin(a); } sync = F.length ? Math.hypot(sx, sy) / F.length : 0; return sync; }
  function scatter() { F.forEach(f => { f.ph = Math.random(); f.lit = 9; }); t = 0; bins = []; binC = 0; binT = 0; hist = []; histT = 0; calc(); }

  // ---------- 1コマ進める ----------
  const q = [];
  function tick() {
    const n = F.length, r2 = range * range;
    const ex = Math.max(12, Math.min(n, n * Math.PI * r2 / ((YB - YA) * asp)));
    const eps = K * 12 / ex;
    q.length = 0;
    for (let i = 0; i < n; i++) {
      const f = F[i];
      f.w += DT * .8;
      f.vx = (f.vx + Math.cos(f.w * 1.3 + i) * .0005) * .995; f.vy = (f.vy + Math.sin(f.w + i * 2) * .0004) * .995;
      f.x += f.vx * DT; f.y += f.vy * DT;
      if (f.x < .02) { f.x = .02; f.vx = Math.abs(f.vx); } else if (f.x > .98) { f.x = .98; f.vx = -Math.abs(f.vx); }
      if (f.y < YA) { f.y = YA; f.vy = Math.abs(f.vy); } else if (f.y > YB) { f.y = YB; f.vy = -Math.abs(f.vy); }
      f.lit += DT; f.ph += DT / f.T;
      if (f.ph >= 1) { f.ph = 1; q.push(i); }
    }
    for (let k = 0; k < q.length; k++) {
      const a = F[q[k]]; a.ph = 0; a.lit = 0;
      if (eps <= 0) continue;
      for (let j = 0; j < n; j++) {
        const b = F[j]; if (b.ph <= 0 || b.ph >= 1) continue;
        const dx = b.x - a.x, dy = (b.y - a.y) * asp;
        if (dx * dx + dy * dy > r2) continue;
        b.ph += eps * b.ph;
        if (b.ph >= 1) { b.ph = 1; q.push(j); }
      }
    }
    binC += q.length; binT += DT;
    if (binT >= .2) { bins.push(binC); if (bins.length > 12) bins.shift(); binC = 0; binT = 0; }
    t += DT; histT += DT;
    if (histT >= .25) { histT = 0; hist.push(calc()); if (hist.length > 240) hist.shift(); }
  }
  const together = () => Math.min(F.length, Math.max(0, ...bins));

  // ---------- 描く ----------
  let dpr = 1, bg = null, spr = null;
  function rng(s) { s = s >>> 0; return () => { s = (s + 0x6D2B79F5) >>> 0; let x = s; x = Math.imul(x ^ (x >>> 15), x | 1); x ^= x + Math.imul(x ^ (x >>> 7), x | 61); return ((x ^ (x >>> 14)) >>> 0) / 4294967296; }; }
  function mkSprite() {
    spr = document.createElement('canvas'); spr.width = spr.height = 64; const c = spr.getContext('2d');
    const g = c.createRadialGradient(32, 32, 0, 32, 32, 32);
    g.addColorStop(0, 'rgba(255,255,225,1)'); g.addColorStop(.16, 'rgba(215,255,120,.85)'); g.addColorStop(.48, 'rgba(150,230,60,.22)'); g.addColorStop(1, 'rgba(120,200,40,0)');
    c.fillStyle = g; c.fillRect(0, 0, 64, 64);
  }
  function mkBg(W, Hh) {
    bg = document.createElement('canvas'); bg.width = W; bg.height = Hh; const c = bg.getContext('2d'), R = rng(77);
    const sky = c.createLinearGradient(0, 0, 0, Hh); sky.addColorStop(0, '#040818'); sky.addColorStop(.6, '#0a1a33'); sky.addColorStop(1, '#0d2238');
    c.fillStyle = sky; c.fillRect(0, 0, W, Hh);
    for (let i = 0; i < 90; i++) { c.fillStyle = `rgba(255,255,255,${(.2 + R() * .6).toFixed(2)})`; c.beginPath(); c.arc(R() * W, R() * Hh * .5, (.4 + R() * .9) * dpr, 0, 7); c.fill(); }
    const mx = W * .82, my = Hh * .16, mr = Math.max(8, W * .022);
    const mg = c.createRadialGradient(mx, my, 0, mx, my, mr * 5); mg.addColorStop(0, 'rgba(226,232,240,.35)'); mg.addColorStop(1, 'rgba(226,232,240,0)'); c.fillStyle = mg; c.fillRect(mx - mr * 5, my - mr * 5, mr * 10, mr * 10);
    c.fillStyle = '#e8edf5'; c.beginPath(); c.arc(mx, my, mr, 0, 7); c.fill();
    // 遠くの山
    c.fillStyle = '#081425'; c.beginPath(); c.moveTo(0, Hh);
    for (let x = 0; x <= W; x += 8) c.lineTo(x, Hh * (.6 - .07 * Math.sin(x / W * 5.2 + 1) - .03 * Math.sin(x / W * 13)));
    c.lineTo(W, Hh); c.closePath(); c.fill();
    // 木
    c.fillStyle = '#050d19';
    for (let i = 0; i < 9; i++) { const tx = (i < 5 ? R() * .22 : .78 + R() * .22) * W, th = Hh * (.3 + R() * .25), tw = W * (.05 + R() * .05), by = Hh * .82;
      c.fillRect(tx - tw * .06, by - th * .5, tw * .12, th * .5);
      for (let k = 0; k < 5; k++) { c.beginPath(); c.ellipse(tx + (R() - .5) * tw, by - th * (.45 + R() * .5), tw * (.45 + R() * .3), th * (.18 + R() * .1), 0, 0, 7); c.fill(); } }
    // 岸と川
    c.fillStyle = '#06101c'; c.fillRect(0, Hh * .8, W, Hh * .2);
    const rv = c.createLinearGradient(0, Hh * RIV, 0, Hh); rv.addColorStop(0, '#0f2a44'); rv.addColorStop(1, '#07182a');
    c.fillStyle = rv; c.beginPath(); c.moveTo(0, Hh);
    for (let x = 0; x <= W; x += 8) c.lineTo(x, Hh * (RIV + .012 * Math.sin(x / W * 9)));
    c.lineTo(W, Hh); c.closePath(); c.fill();
    // 草
    c.strokeStyle = '#040b14'; c.lineWidth = 1.5 * dpr; c.lineCap = 'round';
    for (let i = 0; i < 140; i++) { const x = R() * W, y = Hh * (.8 + R() * .06), h = Hh * (.02 + R() * .05); c.beginPath(); c.moveTo(x, y); c.quadraticCurveTo(x + (R() - .5) * 8 * dpr, y - h * .6, x + (R() - .5) * 14 * dpr, y - h); c.stroke(); }
  }
  function size() {
    const w = cv.clientWidth || 600, h = cv.clientHeight || w * .6; dpr = Math.min(2, window.devicePixelRatio || 1);
    const W = Math.max(2, Math.round(w * dpr)), Hh = Math.max(2, Math.round(h * dpr));
    if (cv.width !== W || cv.height !== Hh || !bg) { cv.width = W; cv.height = Hh; asp = Hh / W; mkBg(W, Hh); }
    const GW = Math.max(2, Math.round((gc.clientWidth || 600) * dpr)), GH = Math.round(90 * dpr);
    if (gc.width !== GW || gc.height !== GH) { gc.width = GW; gc.height = GH; }
  }
  function draw() {
    size(); if (!spr) mkSprite();
    const c = ctx, W = cv.width, Hh = cv.height;
    c.setTransform(1, 0, 0, 1, 0, 0); c.globalCompositeOperation = 'source-over'; c.globalAlpha = 1; c.drawImage(bg, 0, 0);
    c.globalCompositeOperation = 'lighter';
    let tot = 0; const ry0 = Hh * RIV, k = W / 640;
    for (const f of F) {
      const b = Math.exp(-f.lit / .28); tot += b;
      const x = f.x * W, y = f.y * Hh, s = (5 + 20 * b) * k + 2 * dpr;
      c.globalAlpha = Math.min(1, .12 + b); c.drawImage(spr, x - s, y - s, s * 2, s * 2);
      if (b > .04) { const ry = ry0 + (ry0 - y) * .2 + 4 * dpr; c.globalAlpha = .4 * b; c.drawImage(spr, x - s * 1.3, ry - s * .35, s * 2.6, s * .7); }
    }
    const amb = Math.min(.16, tot / Math.max(1, F.length) * .2);
    if (amb > .004) { c.globalAlpha = amb; c.fillStyle = '#b4f05a'; c.fillRect(0, 0, W, Hh); }
    c.globalCompositeOperation = 'source-over'; c.globalAlpha = 1;
    ui(); drawGraph();
  }
  function drawGraph() {
    const c = gx, W = gc.width, Hh = gc.height, p = 34 * dpr, pr = 8 * dpr, pt = 8 * dpr, pb = 8 * dpr;
    c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, W, Hh);
    const Y = v => Hh - pb - v * (Hh - pt - pb), X = i => p + i / 239 * (W - p - pr);
    c.strokeStyle = '#e2e8f0'; c.lineWidth = 1 * dpr; c.fillStyle = '#64748b'; c.font = `${10 * dpr}px system-ui,sans-serif`; c.textAlign = 'right'; c.textBaseline = 'middle';
    [0, .5, 1].forEach(v => { const y = Y(v); c.beginPath(); c.moveTo(p, y); c.lineTo(W - pr, y); c.stroke(); c.fillText(Math.round(v * 100) + '%', p - 4 * dpr, y); });
    if (hist.length < 2) return;
    c.lineWidth = 2.2 * dpr; c.strokeStyle = '#65a30d'; c.lineJoin = 'round'; c.beginPath();
    hist.forEach((v, i) => i ? c.lineTo(X(i), Y(v)) : c.moveTo(X(i), Y(v))); c.stroke();
  }

  // ---------- 数字とひとこと ----------
  let lastUI = 0;
  function ui() {
    const now = performance.now(); if (now - lastUI < 150) return; lastUI = now;
    const s = Math.round(calc() * 100);
    $('mSync').innerHTML = s + '<small>%</small>';
    $('mTog').innerHTML = together() + '<small>ひき</small>';
    $('mTime').innerHTML = Math.floor(t) + '<small>秒</small>';
    $('htNote').textContent = K <= 0 ? '🌙 合わせる強さが0なので、いつまでたってもそろいません。'
      : s >= 90 ? '✨ ほぼ全体がそろって光っています。'
      : s >= 55 ? '✨ 大きなかたまりで、そろって光るようになってきました。'
      : s >= 25 ? '✨ 近くどうしで、少しずつそろいはじめています。'
      : '✨ まだバラバラに光っています。しばらく見ていてください。';
  }

  // ---------- 操作 ----------
  function bind(id, f) { const el = $(id); const up = () => f(+el.value); el.addEventListener('input', up); up(); }
  bind('kN', v => { setN(v); $('vN').textContent = F.length + 'ひき'; });
  bind('kR', v => { range = v / 100; $('vR').textContent = v < 20 ? '近くだけ' : v < 50 ? 'ふつう' : v < 80 ? '遠め' : '遠くまで'; });
  bind('kK', v => { K = v / 100 * .06; $('vK').textContent = v === 0 ? 'なし' : v < 30 ? '弱い' : v < 70 ? 'ふつう' : '強い'; });
  $('htReset').addEventListener('click', () => { scatter(); lastUI = 0; });
  $('htSlow').addEventListener('click', () => { slow = !slow; $('htSlow').classList.toggle('on', slow); });
  $('htPlay').addEventListener('click', () => { playing = !playing; $('htPlay').textContent = playing ? '⏸ 止める' : '▶ 動かす'; });

  // ---------- シェア ----------
  function shareText() { return `ホタル${F.length}ひきの光が、${Math.floor(t)}秒で${Math.round(calc() * 100)}%そろいました✨ リーダーなしでそろう「同期」のシミュレーター`; }
  $('shareBtn').addEventListener('click', () => { const u = location.origin + location.pathname; window.open('https://twitter.com/intent/tweet?text=' + encodeURIComponent(shareText() + '\n') + '&url=' + encodeURIComponent(u) + '&hashtags=' + encodeURIComponent('シミュラボ'), '_blank', 'noopener'); });
  $('copyBtn').addEventListener('click', async () => { const b = $('copyBtn'); try { await navigator.clipboard.writeText(shareText() + '\n' + location.origin + location.pathname); b.textContent = 'コピーしました'; } catch (e) { b.textContent = 'コピーできませんでした'; } setTimeout(() => { b.textContent = '結果をコピー'; }, 1800); });

  // ---------- 動かす ----------
  let tPrev = performance.now(), acc = 0;
  function loop(now) {
    const dt = Math.min(.1, (now - tPrev) / 1000); tPrev = now;
    if (playing) { acc += dt * (slow ? .25 : 1); let n = 0; while (acc >= DT && n < 12) { tick(); acc -= DT; n++; } if (n >= 12) acc = 0; }
    draw(); requestAnimationFrame(loop);
  }
  scatter();
  requestAnimationFrame(loop);
  window.__t = {
    step(sec) { const n = Math.max(0, Math.min(60000, Math.round(sec * 60))); for (let i = 0; i < n; i++) tick(); lastUI = 0; draw(); },
    scatter,
    get s() { return { n: F.length, t: +t.toFixed(2), sync: Math.round(calc() * 100), together: together(), range, K, slow, playing, hist: hist.length, nan: F.some(f => !isFinite(f.x + f.y + f.ph + f.lit)) }; }
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
    <p class="ht-note" style="font-weight:400">{esc(NOTE)}</p>
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
