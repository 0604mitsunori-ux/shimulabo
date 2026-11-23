# -*- coding: utf-8 -*-
"""たんぽぽの綿毛を飛ばすシミュレーター（2026-11-24）
   sims/tanpopo-watage/index.html を書き出す（冪等）。 使い方: python -X utf8 scripts/gen_tanpopo_watage.py"""
import html as H, io, json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://shimulabo.com"
SLUG = "tanpopo-watage"
NAME = "たんぽぽの綿毛を飛ばすシミュレーター"
CAT = "ふしぎ・現象"
TITLE = "たんぽぽの綿毛を飛ばすシミュレーター｜風の強さ・上昇気流でどこまで飛ぶ？｜シミュラボ"
DESC = ("野原のたんぽぽに「ふーっ」と息をふきかけて、綿毛を飛ばすシミュレーター。風の強さ・風のゆらぎ（上昇気流）・たんぽぽの高さを変えると、"
        "綿毛が飛ぶきょりや着地する場所の広がり方が変わります。綿毛がパラシュートのようにゆっくり落ちるしくみも、やさしく説明します。")
OG_T = "たんぽぽの綿毛を飛ばすシミュレーター"
OG_D = "ふーっとふくと綿毛がいっせいに飛ぶ。風の強さや上昇気流で、どこまで飛ぶかが変わる。"
H1 = "たんぽぽの綿毛を飛ばす<br>シミュレーター"
LEAD = ("野原のたんぽぽに「ふーっ」と息をふきかけてみましょう。綿毛がいっせいに飛び、風にのってふわふわ流れ、ゆっくり落ちて地面に着きます。"
        "風の強さや上昇気流、たんぽぽの高さを変えると、飛ぶきょりがどう変わるかをたしかめられます。")
NOTE = "📏 このシミュレーターのきょりは、しくみをつかむための「めやす」です。本物の綿毛が飛ぶきょりを表すものではありません。"

FAQ = [
    ("どうやって遊びますか？", "「ふーっとふく」ボタンをおすか、たんぽぽの白い綿毛をタップ（なぞる）と、綿毛が飛びます。風の強さ・風のゆらぎ・たんぽぽの高さを変えてから「もう一度さかせる」をおすと、何度でもためせます。"),
    ("綿毛は、なぜゆっくり落ちるのですか？", "綿毛（冠毛）の細い毛が空気の抵抗を大きく受けて、パラシュートのようにはたらくからです。落ちるのがおそいほど、空中にいる時間が長くなり、そのあいだに風に運ばれます。"),
    ("風が強いほど、遠くまで飛びますか？", "このシミュレーターでは、風が強いほど遠くまで運ばれます。また、上向きの風（上昇気流）にのった綿毛は空中にいる時間が長くなるので、とくに遠くまで飛びます。風のゆらぎを大きくすると、着地する場所のばらつきも大きくなります。"),
    ("シミュレーターのきょりは、本物と同じですか？", "いいえ、めやすです。本物の風はもっとふくざつで、地面のようすや天気によっても変わります。このシミュレーターは「落ちるのがおそいものほど、風に遠くまで運ばれる」というしくみをつかむために、とても単純にしてあります。"),
]
REL = [("jibun-shokubutsu", "🌱", "自分だけの植物を作って育てる"), ("snowflake", "❄️", "雪の結晶ジェネレーター"), ("boids", "🐦", "鳥の群れシミュレーター（ボイド）")]

ARTICLE = """
<h2>綿毛はパラシュート</h2>
<p>たんぽぽの白い綿毛は、<b>冠毛（かんもう）</b>といいます。細い毛がかさのように広がっていて、その下に細い柄（え）があり、先に小さな実がついています（「たね」に見える部分は、正しくは痩果（そうか）という実です）。</p>
<p>冠毛は空気の抵抗を大きく受けるので、綿毛は<b>パラシュートのようにゆっくり</b>落ちます。もし毛がなければ、実はすぐに真下へ落ちてしまいます。</p>

<h2>落ちるのがおそいほど、遠くへ運ばれる</h2>
<p>綿毛が横に動くのは、自分で進むからではなく、<b>風に運ばれる</b>からです。地面に着くまでの時間が長いほど、そのあいだに風が運んでくれるきょりは長くなります。</p>
<ul>
<li><b>風の強さを大きくする</b>：同じ時間でも、遠くまで運ばれます。</li>
<li><b>風のゆらぎ（上昇気流）を大きくする</b>：上向きの風にのった綿毛は、なかなか落ちずに遠くまで飛びます。下向きの風に当たった綿毛は、すぐ近くに落ちます。着地する場所が広くばらつきます。</li>
<li><b>たんぽぽの高さを高くする</b>：地面に着くまでの時間が長くなり、遠くまで飛びやすくなります。たんぽぽは、花がさいたあと茎をのばして、綿毛を高い位置にかかげることが知られています。</li>
</ul>
<p>下の棒グラフを見ると、多くの綿毛は近くに落ち、少しの綿毛だけが遠くまで飛ぶことがわかります。</p>

<h2>たねを遠くに運ぶと、なぜよいの？</h2>
<p>植物は自分で歩けません。たねが親のすぐ下にばかり落ちると、親やきょうだいどうしで、光・水・土の養分をとり合うことになります。たねを遠くへ運べば、<b>とり合いをさけられ</b>、まだ仲間が生えていない<b>新しい場所</b>で育つこともできます。また、あちこちにちらばっていれば、ある場所の環境が悪くなっても、ほかの場所で生きのこれます。</p>
<p>風でたねを運ぶ植物には、たんぽぽのほかに、カエデ（つばさのある実）、ススキ、ガガイモなどがあります。</p>

<h2>綿毛の上にできる「空気のうず」</h2>
<p>2018年に科学雑誌 Nature に発表された研究（Cummins ほか）では、落ちていく綿毛の<b>すぐ上に、輪の形をした空気のうず</b>ができることが報告されました。うずは綿毛にくっついているのではなく、少しはなれた位置に安定してとどまるため、「分離した渦輪（かりん）」とよばれています。</p>
<p>冠毛はすきまだらけですが、毛と毛のあいだを通りぬける空気の流れが、このうずを安定させています。このうずのおかげで、綿毛は少ない材料でも大きな抵抗を受けて、ゆっくり落ちることができると考えられています。</p>
<p>このシミュレーターでは、うずそのものは計算していません。「綿毛はゆっくり一定の速さで落ちる」として、風に運ばれるようすをえがいています。</p>
"""

REFS = [
    "Cummins, C., Seale, M., Macente, A., Certini, D., Mastropaolo, E., Viola, I. M. &amp; Nakayama, N. (2018) A separated vortex ring underlies the flight of the dandelion. Nature 562, 414–418.",
    "文部科学省「小学校学習指導要領解説 理科編」（植物の発芽・成長・結実）",
]

STAGE = r"""
<style>
#twWrap{position:relative;border-radius:14px;overflow:hidden;border:1px solid var(--line);background:#7dd3fc;touch-action:pan-y}
#tw{display:block;width:100%;aspect-ratio:16/10;cursor:pointer}
.tw-msg{position:absolute;left:50%;top:10px;transform:translateX(-50%);background:rgba(15,23,42,.8);color:#fff;font-size:12.5px;font-weight:700;border-radius:12px;padding:6px 14px;max-width:92%;text-align:center;pointer-events:none;opacity:0;transition:opacity .3s}
.tw-msg.show{opacity:1}
.tw-btns{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
.tw-btns button{border:1.5px solid var(--line);background:#fff;border-radius:999px;padding:10px 16px;font:inherit;font-size:14px;font-weight:800;cursor:pointer;color:var(--ink)}
.tw-btns button.tw-main{background:#0284c7;border-color:#0284c7;color:#fff}
.tw-btns button.on{background:#f59e0b;border-color:#f59e0b;color:#111}
.tw-sum{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:12px}
.tw-sum div{background:#f0f9ff;border-radius:12px;padding:10px 4px;text-align:center;min-width:0}
.tw-sum b{display:block;font-size:20px;color:#0369a1;font-variant-numeric:tabular-nums}
.tw-sum b small{font-size:11.5px}
.tw-sum span{font-size:11.5px;color:var(--ink-2);font-weight:700}
.tw-note{font-size:13.5px;color:var(--ink);background:#f0f9ff;border-radius:10px;padding:9px 12px;margin:10px 0 0}
.tw-cols{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px 22px;margin-top:14px}
#twH{display:block;width:100%;height:120px;margin-top:6px}
.tw-cap{font-size:12.5px;color:var(--ink-2);margin:12px 0 0;font-weight:700}
@media (max-width:640px){.tw-sum{grid-template-columns:repeat(2,1fr)}.tw-cols{grid-template-columns:1fr}.tw-btns button{padding:9px 13px;font-size:13px}}
</style>
"""

BODY = r"""
  <section class="panel" id="resultPanel">
    <div id="twWrap">
      <canvas id="tw" aria-label="野原のたんぽぽから綿毛が風にのって飛んでいく絵"></canvas>
      <div class="tw-msg" id="twMsg"></div>
    </div>
    <div class="tw-btns">
      <button type="button" class="tw-main" id="twBlow">🌬 ふーっとふく</button>
      <button type="button" id="twRegrow">🌼 もう一度さかせる</button>
      <button type="button" id="twSlow">🐢 スロー</button>
    </div>
    <div class="tw-sum">
      <div><b id="mFly">0</b><span>飛んでいる数</span></div>
      <div><b id="mLand">0</b><span>着地した数</span></div>
      <div><b id="mMax">–</b><span>いちばん遠く</span></div>
      <div><b id="mAvg">–</b><span>平均きょり</span></div>
    </div>
    <p class="tw-cap">着地した場所の分布（たんぽぽからのきょり・めやす）</p>
    <canvas id="twH" aria-label="綿毛が着地したきょりの分布の棒グラフ"></canvas>
    <div class="tw-cols">
      <div class="field"><label>🍃 風の強さ <span class="hint">（<b id="vWind"></b>）</span></label><input type="range" id="kWind" min="0" max="6" step="0.5" value="2"></div>
      <div class="field"><label>🌀 風のゆらぎ・上昇気流 <span class="hint">（<b id="vGust"></b>）</span></label><input type="range" id="kGust" min="0" max="100" step="5" value="50"></div>
      <div class="field"><label>🌼 たんぽぽの高さ <span class="hint">（<b id="vH"></b>）</span></label><input type="range" id="kH" min="10" max="60" step="5" value="30"></div>
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
  const cv = $('tw'), c = cv.getContext('2d'), hc = $('twH'), hx = hc.getContext('2d');
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const N = 90, X0 = -0.6, TAU = .12;
  const P = { wind: 2, gust: .5, h: .3, slow: false };
  let seeds = [], T = 0, touched = false, autoDone = false, dpr = 1, S = 100, vmx = 3, vmy = 1.2, lastUI = 0, doneMsg = false;
  let headPx = [0, 0, 20];

  function reset() {
    seeds = [];
    for (let i = 0; i < N; i++) {
      seeds.push({ st: 0, th: i / N * Math.PI * 2 + (Math.random() - .5) * .12, rr: .55 + Math.random() * .45, x: 0, y: 0, vx: 0, vy: 0,
        vt: .12 + Math.random() * .1, ph: Math.random() * 6.283, sp: (Math.random() < .5 ? -1 : 1) * (1.5 + Math.random() * 2.5), k: .6 + Math.random() * .8,
        age: 0, delay: 0, d: 0, lt: 0, rot: 0 });
    }
    doneMsg = false; vmx = 3; vmy = 1.2;
  }
  function release(s, delay) { if (s.st === 0) { s.st = 1; s.delay = delay; } }
  function blow() { seeds.forEach(s => release(s, Math.random() * .9)); flash('ふーっ！'); }
  function launch(s) {
    s.st = 2; s.age = 0;
    s.x = Math.cos(s.th) * .03; s.y = P.h - Math.sin(s.th) * .03;
    s.vx = 1.2 + Math.random() * 1.8; s.vy = (Math.random() - .35) * 1.2;
  }
  function air(s) {
    const g = P.gust, W = P.wind, x = s.x, y = s.y;
    const pr = .35 + .65 * Math.sqrt(clamp(y / .6, 0, 1));
    const u = W * pr * (1 + .3 * g * Math.sin(.8 * x - 1.1 * T + s.ph));
    let w = g * .8 * s.k * (.6 * Math.sin(1.1 * (x - .6 * W * T) + .5 + .35 * T) + .4 * Math.sin(.43 * x + .7 * T + s.ph) + .12) * clamp(y / .12, 0, 1);
    if (w > 0 && y > 2.2) w *= clamp(1 - (y - 2.2) / 1.2, 0, 1);
    if (s.age > 25) w *= clamp(1 - (s.age - 25) / 10, 0, 1);
    return [u, w];
  }
  function update(dt) {
    T += dt;
    if (!touched && !autoDone && T > 1.2) { autoDone = true; blow(); }
    let far = 0, top = 0, active = 0;
    const kk = Math.min(1, dt / TAU);
    for (const s of seeds) {
      if (s.st === 1) { s.delay -= dt; if (s.delay <= 0) launch(s); active++; }
      if (s.st === 2) {
        active++; s.age += dt;
        const a = air(s);
        s.vx += (a[0] - s.vx) * kk; s.vy += (a[1] - s.vt - s.vy) * kk;
        s.x += s.vx * dt; s.y += s.vy * dt;
        if (s.y <= 0) { s.y = 0; s.st = 3; s.d = Math.abs(s.x); s.lt = T; s.rot = (Math.random() < .5 ? -1 : 1) * (1 + Math.random() * .5); }
        else top = Math.max(top, s.y);
      }
      if (s.st >= 2) far = Math.max(far, s.x);
    }
    vmx += (Math.max(3, far * 1.12 + .6) - vmx) * Math.min(1, dt * 2.5);
    vmy += (Math.max(1.2, top + .4, P.h + .6) - vmy) * Math.min(1, dt * 2.5);
    if (!doneMsg && active === 0 && seeds.every(s => s.st === 3)) { doneMsg = true; flash('ぜんぶ着地しました。「もう一度さかせる」でためせます'); }
  }
  function stats() {
    let fly = 0, land = 0, mx = 0, sum = 0, att = 0, nan = false;
    for (const s of seeds) {
      if (!isFinite(s.x) || !isFinite(s.y)) nan = true;
      if (s.st === 0) att++; else if (s.st === 3) { land++; mx = Math.max(mx, s.d); sum += s.d; } else fly++;
    }
    return { attached: att, flying: fly, landed: land, max: +mx.toFixed(2), mean: land ? +(sum / land).toFixed(2) : 0, nan, wind: P.wind, gust: P.gust, h: P.h, t: +T.toFixed(2) };
  }

  // ---------- 描く ----------
  function size() {
    const w = cv.clientWidth || 600; dpr = Math.min(2, window.devicePixelRatio || 1);
    const W = Math.round(w * dpr), Hh = Math.round(w * .625 * dpr); if (cv.width !== W || cv.height !== Hh) { cv.width = W; cv.height = Hh; }
    const gw = hc.clientWidth || 600, GW = Math.round(gw * dpr), GH = Math.round(120 * dpr); if (hc.width !== GW || hc.height !== GH) { hc.width = GW; hc.height = GH; }
  }
  function drawSeed(x, y, r, rot, spin, al) {
    c.save(); c.translate(x, y); c.rotate(rot);
    c.strokeStyle = 'rgba(255,255,255,' + al + ')'; c.lineWidth = Math.max(1, r * .09); c.lineCap = 'round';
    c.beginPath();
    for (let k = 0; k < 11; k++) { const a = -Math.PI / 2 + (k - 5) * .3, L = r * (.76 + .24 * Math.cos(k * 1.7 + spin)); c.moveTo(0, 0); c.lineTo(Math.cos(a) * L, Math.sin(a) * L); }
    c.stroke();
    c.strokeStyle = 'rgba(214,211,209,' + al + ')'; c.beginPath(); c.moveTo(0, 0); c.lineTo(0, r * .9); c.stroke();
    c.fillStyle = '#78350f'; c.beginPath(); c.ellipse(0, r * 1.0, Math.max(1, r * .11), r * .24, 0, 0, 7); c.fill();
    c.restore();
  }
  function draw() {
    size();
    const W = cv.width, Hh = cv.height, gy = Hh * .82;
    S = Math.min(W / (vmx - X0), gy * .94 / vmy);
    const X = x => (x - X0) * S, Y = y => gy - y * S;
    c.setTransform(1, 0, 0, 1, 0, 0);
    const sky = c.createLinearGradient(0, 0, 0, gy); sky.addColorStop(0, '#0ea5e9'); sky.addColorStop(1, '#a5e3fb');
    c.fillStyle = sky; c.fillRect(0, 0, W, gy);
    // 太陽と雲
    c.fillStyle = 'rgba(254,240,138,.9)'; c.beginPath(); c.arc(W * .88, Hh * .14, 18 * dpr, 0, 7); c.fill();
    c.fillStyle = 'rgba(255,255,255,.75)';
    for (let i = 0; i < 4; i++) {
      const span = W + 240 * dpr, cx = ((i * 0.27 * span + T * (6 + P.wind * 9) * dpr * (.7 + i * .15)) % span) - 120 * dpr, cy = Hh * (.1 + i * .09), r = (16 + i * 5) * dpr;
      c.beginPath(); c.ellipse(cx, cy, r * 2.2, r * .7, 0, 0, 7); c.ellipse(cx - r, cy - r * .35, r, r * .7, 0, 0, 7); c.ellipse(cx + r * .8, cy - r * .3, r * 1.1, r * .75, 0, 0, 7); c.fill();
    }
    // 丘
    c.fillStyle = '#86efac'; c.beginPath(); c.moveTo(0, gy);
    for (let px = 0; px <= W; px += 12) c.lineTo(px, gy - (18 + 12 * Math.sin(px / W * 5 + 1) + 7 * Math.sin(px / W * 13)) * dpr);
    c.lineTo(W, gy); c.closePath(); c.fill();
    // 地面
    const gr = c.createLinearGradient(0, gy, 0, Hh); gr.addColorStop(0, '#4ade80'); gr.addColorStop(1, '#15803d');
    c.fillStyle = gr; c.fillRect(0, gy, W, Hh - gy);
    // きょりの目もり
    const steps = [.5, 1, 2, 5, 10, 20, 50, 100]; let st = steps.find(v => v * S >= 46 * dpr) || 200;
    c.fillStyle = 'rgba(255,255,255,.95)'; c.strokeStyle = 'rgba(255,255,255,.8)'; c.lineWidth = 1.5 * dpr; c.font = `700 ${11 * dpr}px system-ui,sans-serif`; c.textAlign = 'center'; c.textBaseline = 'top';
    for (let m = 0; X(m) < W - 6 * dpr; m += st) { c.beginPath(); c.moveTo(X(m), gy + 4 * dpr); c.lineTo(X(m), gy + 12 * dpr); c.stroke(); c.fillText(m + 'm', X(m), gy + 15 * dpr); }
    // 草
    c.strokeStyle = '#166534'; c.lineWidth = 1.6 * dpr; c.lineCap = 'round'; c.beginPath();
    const nb = Math.round(W / (9 * dpr));
    for (let i = 0; i < nb; i++) {
      const bx = (i + .5) / nb * W, bh = (7 + ((i * 37) % 9)) * dpr, sw = (Math.sin(T * (2 + (i % 5) * .3) + i) * .25 + .3) * P.wind * 1.6 * dpr + Math.sin(T * 1.3 + i) * 1.2 * dpr;
      c.moveTo(bx, gy + 2 * dpr); c.quadraticCurveTo(bx, gy - bh * .5, bx + sw, gy - bh);
    }
    c.stroke();
    // 着地した綿毛と芽
    const rs = clamp(.04 * S, 5 * dpr, 13 * dpr);
    let farS = null;
    for (const s of seeds) if (s.st === 3) {
      if (!farS || s.d > farS.d) farS = s;
      const px = X(s.x), g = clamp((T - s.lt) / 1.2, 0, 1), q = rs * .75 * g;
      drawSeed(px, gy - rs * .15, rs * .7, s.rot, s.ph, .75);
      c.strokeStyle = '#14532d'; c.lineWidth = Math.max(1.2, rs * .14); c.beginPath(); c.moveTo(px, gy + 2 * dpr); c.lineTo(px, gy - q); c.stroke();
      c.fillStyle = '#bef264';
      c.beginPath(); c.ellipse(px - q * .45, gy - q, q * .5, q * .24, -.5, 0, 7); c.ellipse(px + q * .45, gy - q, q * .5, q * .24, .5, 0, 7); c.fill();
    }
    if (farS) {
      const px = X(farS.x); c.strokeStyle = '#fff'; c.lineWidth = 1.5 * dpr; c.beginPath(); c.moveTo(px, gy); c.lineTo(px, gy - 30 * dpr); c.stroke();
      c.fillStyle = '#f97316'; c.beginPath(); c.moveTo(px, gy - 30 * dpr); c.lineTo(px - 13 * dpr, gy - 25 * dpr); c.lineTo(px, gy - 20 * dpr); c.closePath(); c.fill();
      c.fillStyle = '#fff'; c.font = `800 ${11 * dpr}px system-ui,sans-serif`; c.textAlign = px > W - 40 * dpr ? 'right' : 'center'; c.textBaseline = 'bottom'; c.fillText(farS.d.toFixed(1) + 'm', px, gy - 32 * dpr);
    }
    // たんぽぽ
    const bx = X(0), sway = Math.sin(T * 1.7) * .012 * P.wind * S, hx0 = bx + sway, hy0 = Y(P.h), hr = clamp(.055 * S, 10 * dpr, 26 * dpr);
    headPx = [hx0, hy0, hr];
    c.fillStyle = '#15803d';
    for (let i = 0; i < 5; i++) { c.save(); c.translate(bx, gy + 1 * dpr); c.rotate(-Math.PI / 2 + (i - 2) * .62); c.beginPath(); c.ellipse(hr * 1.1, 0, hr * 1.1, hr * .28, 0, 0, 7); c.fill(); c.restore(); }
    c.strokeStyle = '#65a30d'; c.lineWidth = Math.max(2 * dpr, hr * .16); c.beginPath(); c.moveTo(bx, gy); c.quadraticCurveTo(bx, (gy + hy0) / 2, hx0, hy0); c.stroke();
    c.fillStyle = '#a8a29e'; c.beginPath(); c.arc(hx0, hy0, hr * .22, 0, 7); c.fill();
    for (const s of seeds) if (s.st <= 1) {
      const jit = s.st === 1 ? Math.sin(T * 40 + s.ph) * .12 : Math.sin(T * 2 + s.ph) * .03, a = s.th + jit, r = hr * .62 * s.rr;
      drawSeed(hx0 + Math.cos(a) * r * 1.05, hy0 + Math.sin(a) * r * 1.05, r, a + Math.PI / 2, s.ph, .92);
    }
    // 飛んでいる綿毛
    for (const s of seeds) if (s.st === 2) {
      const rot = .32 * Math.sin(s.age * 2.2 + s.ph) + .14 * Math.sin(s.age * 5.1 + s.ph * 2) + clamp((s.vx - P.wind) * .12, -.5, .5);
      drawSeed(X(s.x), Y(s.y) - rs, rs, rot, s.age * s.sp + s.ph, .95);
    }
    drawHist(); ui();
  }
  function drawHist() {
    const W = hc.width, Hh = hc.height, pl = 26 * dpr, pb = 20 * dpr, pt = 8 * dpr;
    hx.setTransform(1, 0, 0, 1, 0, 0); hx.clearRect(0, 0, W, Hh);
    const ds = seeds.filter(s => s.st === 3).map(s => s.d), mx = Math.max(0, ...ds);
    const nice = [2, 4, 6, 8, 10, 15, 20, 30, 40, 60, 80, 100, 150, 200, 400], hm = nice.find(v => v >= mx) || Math.ceil(mx / 100) * 100, NB = 16;
    const bins = new Array(NB).fill(0); ds.forEach(d => bins[Math.min(NB - 1, Math.floor(d / hm * NB))]++);
    const bm = Math.max(5, ...bins), bw = (W - pl - 6 * dpr) / NB;
    hx.strokeStyle = '#e2e8f0'; hx.lineWidth = 1 * dpr; hx.beginPath(); hx.moveTo(pl, Hh - pb); hx.lineTo(W - 6 * dpr, Hh - pb); hx.stroke();
    hx.fillStyle = '#22c55e';
    bins.forEach((n, i) => { const bh = n / bm * (Hh - pb - pt); hx.fillRect(pl + i * bw + 1.5 * dpr, Hh - pb - bh, bw - 3 * dpr, bh); });
    hx.fillStyle = '#64748b'; hx.font = `${10 * dpr}px system-ui,sans-serif`; hx.textBaseline = 'top'; hx.textAlign = 'center';
    for (let k = 0; k <= 4; k++) { const v = hm * k / 4; hx.fillText((v % 1 ? v.toFixed(1) : v) + 'm', clamp(pl + k / 4 * NB * bw, pl + 8 * dpr, W - 16 * dpr), Hh - pb + 4 * dpr); }
    hx.textAlign = 'right'; hx.textBaseline = 'middle'; hx.fillText(bm + 'こ', pl - 3 * dpr, pt + 2 * dpr); hx.fillText('0', pl - 3 * dpr, Hh - pb);
  }
  function ui() {
    const now = performance.now(); if (now - lastUI < 150) return; lastUI = now;
    const s = stats();
    $('mFly').innerHTML = s.flying + '<small>こ</small>'; $('mLand').innerHTML = s.landed + '<small>こ</small>';
    $('mMax').innerHTML = s.landed ? s.max.toFixed(1) + '<small>m</small>' : '–'; $('mAvg').innerHTML = s.landed ? s.mean.toFixed(1) + '<small>m</small>' : '–';
  }
  function flash(t) { const el = $('twMsg'); el.textContent = t; el.classList.add('show'); clearTimeout(flash.t); flash.t = setTimeout(() => el.classList.remove('show'), 2200); }

  // ---------- 操作 ----------
  const binds = [
    ['kWind', v => { P.wind = v; return v === 0 ? '無風' : v.toFixed(1) + ' m/秒'; }],
    ['kGust', v => { P.gust = v / 100; return v < 20 ? 'ほとんどなし' : v < 55 ? 'ふつう' : v < 80 ? '強い' : 'とても強い'; }],
    ['kH', v => { P.h = v / 100; return v + ' cm'; }],
  ];
  binds.forEach(([id, f]) => { const el = $(id), out = $('v' + id.slice(1)); const up = () => { out.textContent = f(+el.value); }; el.addEventListener('input', () => { touched = true; up(); }); up(); });
  $('twBlow').addEventListener('click', () => { touched = true; if (!seeds.some(s => s.st === 0)) { flash('綿毛がもうありません。「もう一度さかせる」をおしてください'); return; } blow(); });
  $('twRegrow').addEventListener('click', () => { touched = true; reset(); lastUI = 0; flash('たんぽぽが、また綿毛になりました'); });
  $('twSlow').addEventListener('click', () => { P.slow = !P.slow; $('twSlow').classList.toggle('on', P.slow); });
  function poke(e) {
    const r = cv.getBoundingClientRect(), px = (e.clientX - r.left) * dpr, py = (e.clientY - r.top) * dpr;
    if (Math.hypot(px - headPx[0], py - headPx[1]) > headPx[2] * 2 + 24 * dpr) return;
    touched = true; let n = 0;
    for (const s of seeds) if (s.st === 0 && Math.random() < .5) { release(s, Math.random() * .15); if (++n >= 6) break; }
  }
  cv.addEventListener('pointerdown', poke);
  cv.addEventListener('pointermove', e => { if (e.buttons || e.pointerType === 'touch') poke(e); });

  // ---------- シェア ----------
  function shareText() { const s = stats(); return s.landed ? `たんぽぽの綿毛を飛ばしたら、${s.landed}この綿毛が着地。いちばん遠くて${s.max.toFixed(1)}m、平均${s.mean.toFixed(1)}mでした（めやす）🌼` : 'たんぽぽの綿毛を、ふーっと飛ばしてみよう🌼'; }
  $('shareBtn').addEventListener('click', () => { const u = location.origin + location.pathname; window.open('https://twitter.com/intent/tweet?text=' + encodeURIComponent(shareText() + '\n') + '&url=' + encodeURIComponent(u) + '&hashtags=' + encodeURIComponent('シミュラボ'), '_blank', 'noopener'); });
  $('copyBtn').addEventListener('click', async () => { try { await navigator.clipboard.writeText(shareText() + '\n' + location.origin + location.pathname); flash('コピーしました'); } catch (e) { flash('コピーできませんでした'); } });

  // ---------- 動かす ----------
  function advance(sec) { const n = Math.max(1, Math.ceil(sec * 60)); for (let i = 0; i < n; i++) update(sec / n); }
  let tPrev = performance.now();
  function loop(now) {
    const dt = Math.min(.05, (now - tPrev) / 1000); tPrev = now;
    advance(dt * (P.slow ? .3 : 1)); draw(); requestAnimationFrame(loop);
  }
  reset(); draw();
  requestAnimationFrame(loop);
  window.__t = { P, step(sec) { advance(sec); lastUI = 0; draw(); }, blow() { touched = true; blow(); }, reset() { touched = true; reset(); }, get s() { return stats(); } };
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
    <p class="tw-note" style="font-weight:400">{esc(NOTE)}</p>
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
