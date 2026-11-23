# -*- coding: utf-8 -*-
"""紙飛行機を飛ばすシミュレーター（2026-11-24）
   sims/kami-hikouki/index.html を書き出す（冪等）。 使い方: python -X utf8 scripts/gen_kami_hikouki.py"""
import html as H, io, json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://shimulabo.com"
SLUG = "kami-hikouki"
NAME = "紙飛行機シミュレーター"
CAT = "あそぶ・実験"
TITLE = "紙飛行機を飛ばすシミュレーター｜揚力・抗力・重力と失速（投げ方と重心でとぶきょりが変わる）｜シミュラボ"
DESC = ("体育館で紙飛行機を投げるシミュレーター。投げる速さと角度、重心の位置、うしろの曲げ具合を変えると、すーっと滑空したり、"
        "急に上がって失速して落ちたり、波をうって飛んだりします。揚力・抗力・重力の矢印と、とんだきょり・時間・高さを見ながら、よく飛ぶ調整をさがせます。")
OG_T = "紙飛行機を飛ばすシミュレーター 揚力と失速"
OG_D = "投げる速さ・角度・重心・うしろの曲げ具合で、とび方ととぶきょりが変わる。失速のしくみも見える。"
H1 = "紙飛行機を飛ばす<br>揚力と失速のシミュレーター"
LEAD = ("体育館で紙飛行機を投げてみましょう。投げる速さと角度、重心の位置、うしろの曲げ具合を変えると、とび方が大きく変わります。"
        "前回の線がうすく残るので、調整する前とあとを比べられます。")
NOTE = "📝 数値は、飛び方の感じをつかむための「めやす」です。本物の紙飛行機は、折り方・紙の重さ・空気の流れで飛び方が変わります。"

FAQ = [
    ("どうやって遊びますか？", "投げる速さ・投げる角度・重心の位置・うしろの曲げ具合を決めて「投げる」をおします。とんだきょり・とんでいた時間・いちばん高いところが出ます。前回の線がうすく残るので、1つだけ変えて比べると、ちがいがよくわかります。"),
    ("失速（しっそく）とは何ですか？", "つばさが空気に当たる角度（迎え角）が大きくなりすぎて、つばさの上の空気の流れがはがれ、揚力が急に小さくなることです。紙飛行機が急に上を向いたあと、ストンと落ちるのは失速したためです。"),
    ("強く投げれば、遠くまで飛びますか？", "そうとはかぎりません。速すぎると揚力が大きくなりすぎて急に上がり、速さを失って失速することがあります。機体がつり合う速さに近い速さで、少し上向きか水平に投げると、なめらかに滑空しやすくなります。"),
]
REL = [("mizukiri-ishi", "🪨", "水切りシミュレーター"), ("coaster-energy", "🎢", "ジェットコースターで学ぶエネルギー"), ("tanpopo-watage", "🌼", "たんぽぽの綿毛を飛ばす")]

ARTICLE = """
<h2>紙飛行機にはたらく力</h2>
<p>飛行機には、ふつう<b>重力・揚力（ようりょく）・抗力（こうりょく）・推力（すいりょく）</b>の4つの力がはたらきます。紙飛行機にはエンジンがないので、手をはなれたあとは推力がありません。滑空しているあいだにはたらくのは、次の3つです。</p>
<ul>
<li><b>重力</b>：地球が下に引く力です。いつも真下を向いています。</li>
<li><b>揚力</b>：つばさが空気から受ける力のうち、進む向きに対して直角の力です。機体をささえます。</li>
<li><b>抗力</b>：進む向きと逆向きにはたらく、空気のていこうです。</li>
</ul>
<p>揚力と抗力は、どちらも<b>速さの2乗</b>に比例します。速さが2倍になると、力は4倍になります。紙飛行機は、少しずつ下りながら重力で速さをたもち、その速さで生まれる揚力で体をささえています。これが滑空です。</p>

<h2>失速とは</h2>
<p>つばさが、進む向きに対してどれだけ上を向いているかを<b>迎え角（むかえかく）</b>といいます。迎え角を大きくすると揚力は大きくなりますが、大きくなりすぎると、つばさの上の空気の流れがはがれて、揚力が急に小さくなります。これが<b>失速</b>です。失速すると、抗力も大きくなり、機体は落ちはじめます。</p>
<p>強く上向きに投げると、紙飛行機は上がりながら速さを失います。おそくなると揚力が足りなくなり、迎え角が大きくなって失速します。上がっては落ち、また速くなって上がる、という波のような飛び方も、同じしくみで起こります。</p>

<h2>重心の位置で飛び方が変わる理由</h2>
<p>紙飛行機は、重心（重さの中心）を軸にして、頭を上げたり下げたりします。</p>
<ul>
<li><b>先が重い（重心が前）</b>：頭が下がりやすくなります。迎え角が小さくなって揚力が足りず、まっすぐ床に向かって落ちやすくなります。</li>
<li><b>うしろが重い（重心がうしろ）</b>：頭が上がりやすくなります。迎え角が大きくなりすぎて、失速しやすくなります。向きも安定しにくくなります。</li>
</ul>
<p>重心が少し前よりにあると、向きがずれても元にもどろうとするので、安定して飛びます。</p>

<h2>うしろを少し上に曲げるとよく飛ぶ理由</h2>
<p>つばさのうしろを少し上に曲げると、そこに当たった空気が、うしろの部分を下におします。すると、重心を軸にして頭が上がります。重心が前よりの紙飛行機は頭が下がりやすいので、この「頭を上げる力」とつり合って、ちょうどよい迎え角で滑空できるようになります。</p>
<p>曲げすぎると、頭が上がりすぎて失速します。少しずつ曲げて、ためしてみるのがこつです。</p>

<h2>ためしてみたいこと</h2>
<ul>
<li><b>うしろの曲げ具合を0にする</b>：ほかはそのままにして、飛び方がどう変わるか見てみましょう。</li>
<li><b>重心をうしろよりにする</b>：頭が上がり、失速しやすくなるようすを見てみましょう。</li>
<li><b>投げる速さだけを変える</b>：ゆっくり投げたときと、強く投げたときの線を比べてみましょう。</li>
<li><b>スローにする</b>：揚力・抗力の矢印が、速さや迎え角でのびちぢみするようすが見えます。</li>
</ul>

<h2>このシミュレーターのモデル</h2>
<p>横から見た2次元で、機体を「1つの点」と「機体の向き」で表しています。揚力と抗力は速さの2乗に比例し、迎え角で変わります。迎え角が約12°をこえると失速して、揚力が急に小さくなります。重心の位置とうしろの曲げ具合で、つり合う迎え角が変わります。風はなく、左右へのかたむきや回転は考えていません。</p>
"""

REFS = [
    "文部科学省「中学校学習指導要領解説 理科編」（力のつり合いと合成・分解、運動の規則性）",
    "NASA Glenn Research Center, Beginner's Guide to Aeronautics（Forces on a Glider／The Lift Equation／The Drag Equation）",
]

STAGE = r"""
<style>
#khWrap{position:relative;border-radius:14px;overflow:hidden;border:1px solid var(--line);background:#fef3c7}
#kh{display:block;width:100%;aspect-ratio:100/42}
.kh-play{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:10px}
.kh-play button{border:1.5px solid var(--line);background:#fff;border-radius:999px;padding:9px 15px;font:inherit;font-size:14px;font-weight:800;cursor:pointer;color:var(--ink)}
.kh-play button.kh-go{background:#2563eb;border-color:#2563eb;color:#fff;padding:11px 24px;font-size:16px}
.kh-play button.on{background:#f59e0b;border-color:#f59e0b;color:#111}
.kh-sum{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:12px}
.kh-sum div{background:#eff6ff;border-radius:12px;padding:10px 4px;text-align:center}
.kh-sum b{display:block;font-size:20px;color:#1d4ed8;font-variant-numeric:tabular-nums}
.kh-sum b small{font-size:11.5px}
.kh-sum span{font-size:11.5px;color:var(--ink-2);font-weight:700}
.kh-note{font-size:13.5px;color:var(--ink);background:#eff6ff;border-radius:10px;padding:9px 12px;margin:10px 0 0;font-weight:700}
.kh-cols{display:grid;grid-template-columns:1fr 1fr;gap:6px 22px;margin-top:6px}
.kh-legend{font-size:12px;color:var(--ink-2);display:flex;gap:12px;flex-wrap:wrap;margin-top:8px}
.kh-legend i{display:inline-block;width:16px;height:4px;vertical-align:3px;margin-right:4px;border-radius:2px}
@media (max-width:640px){.kh-sum{grid-template-columns:repeat(2,1fr)}.kh-cols{grid-template-columns:1fr}.kh-play button{padding:8px 12px;font-size:13px}.kh-play button.kh-go{padding:10px 18px;font-size:15px}}
</style>
"""

BODY = r"""
  <section class="panel" id="resultPanel">
    <div id="khWrap">
      <canvas id="kh" aria-label="体育館を横から見た絵。紙飛行機が飛んでいく"></canvas>
    </div>
    <div class="kh-play">
      <button type="button" class="kh-go" id="khThrow">✈️ 投げる</button>
      <button type="button" id="khSlow">🐢 スロー</button>
      <button type="button" id="khArr" class="on">力の矢印</button>
    </div>
    <div class="kh-legend"><span><i style="background:#2563eb"></i>揚力</span><span><i style="background:#dc2626"></i>抗力</span><span><i style="background:#475569"></i>重力</span><span><i style="background:repeating-linear-gradient(90deg,#2563eb 0 4px,transparent 4px 7px)"></i>今回の線</span><span><i style="background:repeating-linear-gradient(90deg,#94a3b8 0 4px,transparent 4px 7px)"></i>前回の線</span></div>
    <div class="kh-sum">
      <div><b id="mDist">0</b><span>とんだきょり</span></div>
      <div><b id="mTime">0</b><span>とんでいた時間</span></div>
      <div><b id="mH">0</b><span>いちばん高いところ</span></div>
      <div><b id="mBest">0</b><span>今回のベスト</span></div>
    </div>
    <p class="kh-note" id="khNote">✈️ 投げました。</p>

    <h2 style="margin:20px 0 6px;font-size:18px;">投げ方</h2>
    <div class="kh-cols">
      <div class="field"><label>投げる速さ <span class="hint">（<b id="vV"></b>）</span></label><input type="range" id="kV" min="3" max="12" step="0.5" value="6"></div>
      <div class="field"><label>投げる角度 <span class="hint">（<b id="vA"></b>）</span></label><input type="range" id="kA" min="-10" max="45" step="1" value="10"></div>
    </div>
    <h2 style="margin:16px 0 6px;font-size:18px;">機体の調整</h2>
    <div class="kh-cols">
      <div class="field"><label>重心の位置 <span class="hint">（<b id="vCg"></b>）</span></label><input type="range" id="kCg" min="0" max="100" step="5" value="60"></div>
      <div class="field"><label>うしろの曲げ具合 <span class="hint">（<b id="vEl"></b>）</span></label><input type="range" id="kEl" min="0" max="100" step="5" value="35"></div>
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
  const cv = $('kh'), c = cv.getContext('2d');
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const G = 9.8, K = 0.97, GW = 26, CEIL = 9, X0 = 1.2, Y0 = 1.5, DT = 1 / 240, AS = 0.21;
  const P = { v: 6, ang: 10, cg: 60, el: 35 };
  let s = null, trail = [], prev = [], best = 0, slow = false, arrows = true, acc = 0, tTrail = 0;

  // ---------- 空気の力（迎え角 al で変わる。AS をこえると失速） ----------
  function aero(al) {
    const a = Math.abs(al), sg = al < 0 ? -1 : 1;
    const lin = 4 * Math.min(a, AS), post = 0.55 * Math.sin(2 * a);
    const t = clamp((a - AS) / 0.06, 0, 1);
    const CL = sg * (lin * (1 - t) + post * t);
    const sn = Math.sin(a), CD = 0.07 + 1.5 * sn * sn;
    return [CL, CD, a > AS + 0.03];
  }
  function trimAngle() { return (3 + 12 * P.el / 100 - 7 * (P.cg / 50 - 1)) * Math.PI / 180; }

  function launch() {
    if (s && trail.length > 1) prev = trail;
    const a = P.ang * Math.PI / 180;
    s = { x: X0, y: Y0, vx: P.v * Math.cos(a), vy: P.v * Math.sin(a), th: a, om: 0, t: 0, fly: true, maxH: Y0, dist: 0, stall: false, stalls: 0, al: 0, CL: 0, CD: 0, end: '' };
    trail = [[X0, Y0]]; tTrail = 0; acc = 0;
    $('khNote').textContent = '✈️ 投げました。';
  }
  function finish(why) {
    s.fly = false; s.end = why; s.dist = Math.max(0, s.x - X0); best = Math.max(best, s.dist);
    trail.push([s.x, s.y]);
    let m;
    if (why === 'wall') m = '🎉 向こうのかべまでとどきました！';
    else if (s.stalls > 0 && s.dist < 8) m = '🌀 上を向きすぎて失速しました。重心を前よりにするか、うしろの曲げを少なくしてみましょう。';
    else if (s.stalls > 0) m = '〰️ とちゅうで失速して、波をうつように飛びました。';
    else if (s.t < 1.6 && s.maxH < Y0 + 0.6) m = '⬇️ 頭が下がって、すぐに床に落ちました。うしろを少し上に曲げるか、重心を少しうしろにしてみましょう。';
    else m = '✨ 失速せずに滑空しました。';
    $('khNote').textContent = m + '（' + s.dist.toFixed(1) + 'm）';
  }
  function step1() {
    const v = Math.hypot(s.vx, s.vy) || 1e-6, gam = Math.atan2(s.vy, s.vx);
    let al = s.th - gam; while (al > Math.PI) al -= 2 * Math.PI; while (al < -Math.PI) al += 2 * Math.PI;
    const [CL, CD, st] = aero(al);
    if (st && !s.stall && s.t > 0.05) s.stalls++;
    s.stall = st; s.al = al; s.CL = CL; s.CD = CD;
    const ax = K * v * (-CL * s.vy - CD * s.vx), ay = K * v * (CL * s.vx - CD * s.vy) - G;
    s.vx += ax * DT; s.vy += ay * DT; s.x += s.vx * DT; s.y += s.vy * DT;
    const kq = 0.6 + 1.6 * P.cg / 100;
    s.om += (-kq * v * v * clamp(al - trimAngle(), -0.6, 0.6) - 1.2 * v * s.om) * DT;
    s.om = clamp(s.om, -12, 12); s.th += s.om * DT;
    s.t += DT; tTrail += DT;
    if (s.y > CEIL - 0.1) { s.y = CEIL - 0.1; s.vy = -Math.abs(s.vy) * 0.2; s.vx *= 0.6; }
    if (s.x < 0.15) { s.x = 0.15; s.vx = Math.abs(s.vx) * 0.2; }
    if (s.y > s.maxH) s.maxH = s.y;
    if (tTrail >= 0.06) { tTrail = 0; trail.push([s.x, s.y]); }
    if (s.x >= GW - 0.15) { s.x = GW - 0.15; finish('wall'); }
    else if (s.y <= 0.04) { s.y = 0.04; finish('floor'); }
    else if (s.t > 30) finish('time');
  }
  function adv(sec) { acc += sec; let n = 0; while (acc >= DT && n < 20000) { if (s.fly) step1(); acc -= DT; n++; } }

  // ---------- 描く ----------
  let dpr = 1, S = 1, W = 0, Hh = 0, gy = 0;
  function size() {
    const w = cv.clientWidth || 600; dpr = Math.min(2, window.devicePixelRatio || 1);
    const Wp = Math.round(w * dpr), Hp = Math.round(w * 0.42 * dpr);
    if (cv.width !== Wp || cv.height !== Hp) { cv.width = Wp; cv.height = Hp; }
    W = cv.width; Hh = cv.height; S = W / (GW + 1.2); gy = Hh - 0.9 * S;
  }
  const X = x => (x + 0.6) * S, Y = y => gy - y * S;
  function arrow(x, y, dx, dy, col, label) {
    const L = Math.hypot(dx, dy); if (L < 3 * dpr) return;
    const ux = dx / L, uy = dy / L, h = Math.min(7 * dpr, L * 0.5);
    c.strokeStyle = col; c.fillStyle = col; c.lineWidth = 2.4 * dpr; c.lineCap = 'round';
    c.beginPath(); c.moveTo(x, y); c.lineTo(x + dx - ux * h * 0.6, y + dy - uy * h * 0.6); c.stroke();
    c.beginPath(); c.moveTo(x + dx, y + dy); c.lineTo(x + dx - ux * h - uy * h * 0.55, y + dy - uy * h + ux * h * 0.55); c.lineTo(x + dx - ux * h + uy * h * 0.55, y + dy - uy * h - ux * h * 0.55); c.closePath(); c.fill();
    if (label && W > 520 * dpr) { c.font = `bold ${10.5 * dpr}px system-ui,sans-serif`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(label, x + dx + ux * 12 * dpr, y + dy + uy * 9 * dpr); }
  }
  function path(pts, col, w) {
    if (pts.length < 2) return;
    c.strokeStyle = col; c.lineWidth = w * dpr; c.setLineDash([4 * dpr, 4 * dpr]); c.lineCap = 'butt';
    c.beginPath(); pts.forEach((p, i) => i ? c.lineTo(X(p[0]), Y(p[1])) : c.moveTo(X(p[0]), Y(p[1]))); c.stroke(); c.setLineDash([]);
  }
  function draw() {
    size();
    c.setTransform(1, 0, 0, 1, 0, 0);
    // かべ・天井
    const wg = c.createLinearGradient(0, 0, 0, gy); wg.addColorStop(0, '#fde9b8'); wg.addColorStop(1, '#fff7e0');
    c.fillStyle = wg; c.fillRect(0, 0, W, gy);
    c.fillStyle = '#7c4a21'; c.fillRect(0, 0, W, Y(CEIL));
    c.fillStyle = '#5b3516'; for (let x = 1; x < GW; x += 3.2) c.fillRect(X(x), 0, 0.18 * S, Y(CEIL) + 0.25 * S);
    // まど
    for (let x = 2.2; x < GW - 2; x += 3.2) {
      c.fillStyle = '#bfe3ff'; c.fillRect(X(x), Y(7.6), 2 * S, 2.1 * S);
      c.strokeStyle = '#fff'; c.lineWidth = 2 * dpr; c.strokeRect(X(x), Y(7.6), 2 * S, 2.1 * S);
      c.beginPath(); c.moveTo(X(x + 1), Y(7.6)); c.lineTo(X(x + 1), Y(5.5)); c.stroke();
    }
    // こしかべ
    c.fillStyle = '#e7c98f'; c.fillRect(0, Y(1.1), W, 1.1 * S);
    // ゴール
    c.fillStyle = '#fff'; c.fillRect(X(GW - 0.25), Y(3.9), 0.12 * S, 1.1 * S); c.strokeStyle = '#ea580c'; c.lineWidth = 2 * dpr;
    c.beginPath(); c.moveTo(X(GW - 0.25), Y(3.05)); c.lineTo(X(GW - 0.75), Y(3.05)); c.stroke();
    // ゆか
    c.fillStyle = '#d9a35c'; c.fillRect(0, gy, W, Hh - gy);
    c.fillStyle = 'rgba(255,255,255,.25)'; c.fillRect(0, gy, W, 2 * dpr);
    // きょりの目もり
    c.font = `${10.5 * dpr}px system-ui,sans-serif`; c.textAlign = 'center'; c.textBaseline = 'top';
    for (let d = 0; d <= GW - X0; d += 5) {
      const x = X(X0 + d); c.strokeStyle = 'rgba(120,53,15,.55)'; c.lineWidth = 1.5 * dpr;
      c.beginPath(); c.moveTo(x, gy); c.lineTo(x, gy + 0.3 * S); c.stroke();
      c.fillStyle = '#5b3516'; c.fillText(d + 'm', x, gy + 0.33 * S);
    }
    // 投げる人
    const px = X(X0 - 0.45), hy = Y(1.38), hr = 0.17 * S;
    c.strokeStyle = '#334155'; c.lineWidth = Math.max(2 * dpr, 0.09 * S); c.lineCap = 'round';
    c.beginPath(); c.moveTo(px, hy + hr); c.lineTo(px, Y(0.6)); c.lineTo(px - 0.18 * S, Y(0)); c.moveTo(px, Y(0.6)); c.lineTo(px + 0.2 * S, Y(0));
    c.moveTo(px, Y(1.1)); c.lineTo(X(X0 - 0.05), Y(Y0 - 0.05)); c.stroke();
    c.fillStyle = '#fcd9b6'; c.beginPath(); c.arc(px, hy, hr, 0, 7); c.fill(); c.stroke();
    // 線
    path(prev, 'rgba(100,116,139,.45)', 1.6);
    path(trail.concat(s.fly ? [[s.x, s.y]] : []), '#2563eb', 2);
    // かげ
    const sh = clamp(1 - s.y / 8, 0.15, 1);
    c.fillStyle = `rgba(60,30,10,${0.28 * sh})`; c.beginPath(); c.ellipse(X(s.x), gy + 0.12 * S, 0.45 * S * (0.6 + 0.4 * sh), 0.07 * S, 0, 0, 7); c.fill();
    // 力の矢印
    const cx = X(s.x), cy = Y(s.y);
    if (arrows && s.fly) {
      const v = Math.hypot(s.vx, s.vy) || 1e-6, u = Math.max(1.5 * S, 30 * dpr) / G;
      const Lf = K * v * s.CL, Df = K * v * s.CD;
      arrow(cx, cy, 0, G * u, '#475569', '重力');
      arrow(cx, cy, clamp(-Lf * s.vy, -25, 25) * u, -clamp(Lf * s.vx, -25, 25) * u, '#2563eb', '揚力');
      arrow(cx, cy, clamp(-Df * s.vx, -25, 25) * u, -clamp(-Df * s.vy, -25, 25) * u, '#dc2626', '抗力');
    }
    // 紙飛行機
    const L = Math.max(0.95 * S, 22 * dpr);
    c.save(); c.translate(cx, cy); c.rotate(-s.th);
    c.lineJoin = 'round'; c.lineWidth = 1.3 * dpr; c.strokeStyle = '#334155';
    c.fillStyle = '#cbd5e1'; c.beginPath(); c.moveTo(L * 0.5, 0); c.lineTo(-L * 0.42, 0); c.lineTo(-L * 0.3, L * 0.13); c.closePath(); c.fill(); c.stroke();
    c.fillStyle = '#fff'; c.beginPath(); c.moveTo(L * 0.5, 0); c.lineTo(-L * 0.36, 0); c.lineTo(-L * 0.5, -L * 0.12); c.closePath(); c.fill(); c.stroke();
    const ea = P.el / 100 * 0.9; c.strokeStyle = '#f97316'; c.lineWidth = 2.2 * dpr;
    c.beginPath(); c.moveTo(-L * 0.36, 0); c.lineTo(-L * 0.36 - Math.cos(ea) * L * 0.16, -Math.sin(ea) * L * 0.16); c.stroke();
    c.fillStyle = '#dc2626'; c.beginPath(); c.arc(L * (P.cg / 100 - 0.5) * 0.6, L * 0.03, Math.max(1.8 * dpr, L * 0.045), 0, 7); c.fill();
    c.restore();
    if (s.fly && s.stall) { c.font = `bold ${13 * dpr}px system-ui,sans-serif`; c.textAlign = 'center'; c.textBaseline = 'bottom'; c.fillStyle = '#dc2626'; c.fillText('失速！', clamp(cx, 30 * dpr, W - 30 * dpr), Math.max(16 * dpr, cy - L * 0.5)); }
    ui();
  }
  function ui() {
    const d = s.fly ? Math.max(0, s.x - X0) : s.dist;
    $('mDist').innerHTML = d.toFixed(1) + '<small>m</small>';
    $('mTime').innerHTML = s.t.toFixed(1) + '<small>秒</small>';
    $('mH').innerHTML = s.maxH.toFixed(1) + '<small>m</small>';
    $('mBest').innerHTML = best.toFixed(1) + '<small>m</small>';
  }

  // ---------- 操作 ----------
  const binds = [
    ['kV', 'v', v => v.toFixed(1) + ' m/秒（' + (v < 5 ? 'そっと' : v < 8 ? 'ふつう' : '強く') + '）'],
    ['kA', 'ang', v => v === 0 ? '水平' : v > 0 ? '上に' + v + '°' : '下に' + (-v) + '°'],
    ['kCg', 'cg', v => v < 30 ? 'うしろより' : v < 50 ? '少しうしろ' : v === 50 ? 'まん中' : v <= 70 ? '少し前より' : '前より（先が重い）'],
    ['kEl', 'el', v => v === 0 ? '曲げない' : v < 40 ? '少し上に曲げる' : v < 70 ? '上に曲げる' : '大きく上に曲げる'],
  ];
  binds.forEach(([id, key, f]) => { const el = $(id), out = $('v' + id.slice(1)); const up = () => { P[key] = +el.value; out.textContent = f(P[key]); }; el.addEventListener('input', up); up(); });
  $('khThrow').addEventListener('click', launch);
  $('khSlow').addEventListener('click', () => { slow = !slow; $('khSlow').classList.toggle('on', slow); });
  $('khArr').addEventListener('click', () => { arrows = !arrows; $('khArr').classList.toggle('on', arrows); });

  // ---------- シェア ----------
  function shareText() { return `紙飛行機を投げたら、${s.dist.toFixed(1)}mとびました（${s.t.toFixed(1)}秒・高さ${s.maxH.toFixed(1)}m）。今回のベストは${best.toFixed(1)}m✈️`; }
  $('shareBtn').addEventListener('click', () => { const u = location.origin + location.pathname; window.open('https://twitter.com/intent/tweet?text=' + encodeURIComponent(shareText() + '\n') + '&url=' + encodeURIComponent(u) + '&hashtags=' + encodeURIComponent('シミュラボ'), '_blank', 'noopener'); });
  $('copyBtn').addEventListener('click', async () => { try { await navigator.clipboard.writeText(shareText() + '\n' + location.origin + location.pathname); $('khNote').textContent = 'コピーしました。'; } catch (e) { $('khNote').textContent = 'コピーできませんでした。'; } });

  // ---------- 動かす ----------
  let tp = performance.now();
  function loop(now) { const dt = Math.min(0.05, (now - tp) / 1000); tp = now; adv(dt * (slow ? 0.25 : 1)); draw(); requestAnimationFrame(loop); }
  launch(); draw();
  requestAnimationFrame(loop);
  window.__t = {
    step(sec) { adv(sec); draw(); },
    throw() { launch(); },
    set(o) { Object.assign(P, o); binds.forEach(([id, key, f]) => { $(id).value = P[key]; $('v' + id.slice(1)).textContent = f(P[key]); }); },
    get s() { return { x: +s.x.toFixed(3), y: +s.y.toFixed(3), vx: +s.vx.toFixed(3), vy: +s.vy.toFixed(3), th: +s.th.toFixed(3), t: +s.t.toFixed(2), flying: s.fly, dist: +s.dist.toFixed(2), maxH: +s.maxH.toFixed(2), best: +best.toFixed(2), stalls: s.stalls, end: s.end, trail: trail.length, prev: prev.length, nan: [s.x, s.y, s.vx, s.vy, s.th, s.om].some(v => !isFinite(v)), P: Object.assign({}, P) }; }
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
    <p class="kh-note" style="font-weight:400">{esc(NOTE)}</p>
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
