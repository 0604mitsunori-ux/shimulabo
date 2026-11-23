# -*- coding: utf-8 -*-
"""窓ガラスの雨つぶシミュレーター（2026-11-24）
   sims/mado-amatsubu/index.html を書き出す（冪等）。 使い方: python -X utf8 scripts/gen_mado_amatsubu.py"""
import html as H, io, json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://shimulabo.com"
SLUG = "mado-amatsubu"
NAME = "窓ガラスの雨つぶシミュレーター"
CAT = "ふしぎ・現象"
TITLE = "窓ガラスの雨つぶはなぜ流れる？｜雨つぶシミュレーター（重さと表面張力・撥水・風）｜シミュラボ"
DESC = ("窓ガラスについた小さな雨つぶが、となりとくっついて大きくなり、ある大きさをこえると流れ落ちるようすを見られるシミュレーター。"
        "雨の強さ・ガラスのはじきやすさ（撥水）・風を変えたり、指でなぞってつぶを集めたり、ワイパーでふいたりできます。")
OG_T = "窓ガラスの雨つぶはなぜ流れる？ 雨つぶシミュレーター"
OG_D = "小さいつぶは止まり、大きいつぶは流れる。重さと、ガラスにくっつく力のつり合いを、夜の窓でたしかめよう。"
H1 = "窓ガラスの雨つぶは、なぜ流れる？<br>雨つぶシミュレーター"
LEAD = ("夜の窓ガラスに、雨つぶがつきます。小さなつぶはその場に止まり、となりとくっついて大きくなると、すうっと流れ落ちます。"
        "雨の強さ、ガラスのはじきやすさ、風を変えて、つぶの動きをくらべてみましょう。指でなぞると、つぶを集めることもできます。")
NOTE = "☔ 画面の大きさは、たて6cm×よこ8cmくらいの窓ガラスを思いうかべて作っています。数字はめやすです。"

FAQ = [
    ("どうやって遊びますか？", "見ているだけで、雨つぶがついて、くっついて、流れ落ちます。下のスライダーで「雨の強さ」「ガラスのはじきやすさ」「風」を変えられます。画面を指（マウス）でなぞると、つぶを集めて大きなつぶを作れます。「🧽 ワイパー」をおすと、全部ふき取ります。"),
    ("小さいつぶは、なぜ落ちないのですか？", "水のつぶには、ガラスにくっつく力がはたらいています。この力は、つぶとガラスがふれている部分のふちの長さで決まります。つぶが小さいうちは、重さよりも、くっつく力のほうが大きいので、その場に止まります。"),
    ("大きくなると、なぜ流れるのですか？", "つぶの大きさが2倍になると、重さ（体積）はおよそ8倍になりますが、ガラスにくっつく力はおよそ2倍にしかなりません。そのため、ある大きさをこえると重さが勝って、流れはじめます。"),
    ("表示される直径は、本物と同じですか？", "いいえ。このシミュレーターの数字は、しくみを見やすくするためのめやすです。本物のつぶが流れ出す大きさは、ガラスのよごれ・かたむき・コーティングなどで大きく変わります。"),
]
REL = [("sekken-shabondama", "🫧", "セッケン・シャボン玉の膜のしくみ"), ("snowflake", "❄️", "雪の結晶ジェネレーター"), ("kaminari-houden", "⚡", "雷の通り道シミュレーター")]

ARTICLE = """
<h2>なぜ小さいつぶは止まり、大きいつぶは流れるのか</h2>
<p>窓ガラスについた雨つぶには、2つの力がはたらいています。</p>
<ul>
<li><b>下に引く力（重さ）</b>：つぶの体積で決まります。つぶの大きさが2倍になると、体積はおよそ8倍になります。</li>
<li><b>その場にとどめる力</b>：水の<b>表面張力</b>と、水がガラスにくっつく性質から生まれます。つぶとガラスがふれている部分のふちの長さで決まるので、つぶの大きさが2倍になっても、およそ2倍にしかなりません。</li>
</ul>
<p>小さいうちは、とどめる力のほうが大きいので、つぶは止まっています。くっついて大きくなると、重さのほうが早く大きくなるので、ある大きさで<b>重さが勝って流れはじめます</b>。</p>
<p>止まっているつぶをよく見ると、下側はふくらんで、上側はうすくなっています。つぶの下のふちと上のふちで、ガラスとの角度（接触角）がちがうためで、この角度の差が、つぶをささえる力になっています。</p>

<h2>流れはじめると、どうなるのか</h2>
<ul>
<li><b>とちゅうのつぶを集めて加速する</b>：流れる道すじにある小さなつぶを、次々に取りこみます。つぶが大きくなるほど重さが勝つので、だんだん速くなります。</li>
<li><b>あとに小さなつぶを残す</b>：通ったあとには、うすい水のすじが残ります。水は表面張力で丸くなろうとするので、すじはちぎれて、小さなつぶの列になります。</li>
<li><b>とちゅうで止まることもある</b>：水を残しながら流れるので、集める水が少ないと小さくなり、また止まります。</li>
</ul>

<h2>ためしてみたいこと</h2>
<ul>
<li><b>ガラスのはじきやすさを上げる</b>：水をはじくガラスでは、つぶがガラスにくっつく力が弱くなるので、小さいうちに流れ出します。車の窓の撥水（はっすい）コーティングは、この性質を使っています。</li>
<li><b>はじきやすさを下げる</b>：つぶはなかなか流れず、大きく育ってから、ゆっくり動きます。</li>
<li><b>風を強くする</b>：つぶは、重さと風の力を合わせた向きへ、ななめに流れます。</li>
<li><b>雨を止めて、指でなぞる</b>：自分でつぶを集めて、どのくらいの大きさで流れ出すかをたしかめられます。</li>
</ul>

<h2>このシミュレーターのきまり</h2>
<p>つぶがふれ合うと1つにまとまり、体積は足し算になります。つぶの半径が「流れ出す大きさ」をこえると動き出し、大きいほど速く流れます。本物の雨つぶの動きは、ガラスの小さなよごれや、すでにぬれている場所などにも左右されます。ここではそれらを省いた、単純なモデルです。</p>
"""

REFS = [
    "de Gennes, P.-G., Brochard-Wyart, F. & Quéré, D. (2004) Capillarity and Wetting Phenomena: Drops, Bubbles, Pearls, Waves. Springer.（表面張力・接触角・ぬれの教科書）",
    "Furmidge, C. G. L. (1962) Studies at phase interfaces. I. The sliding of liquid drops on solid surfaces and a theory for spray retention. Journal of Colloid Science 17, 309–324.（かたむいた面で水てきがすべり出す条件）",
]

STAGE = r"""
<style>
#maWrap{position:relative;border-radius:14px;overflow:hidden;border:1px solid var(--line);background:#0b1020;max-width:100%}
#maCv{display:block;width:100%;aspect-ratio:4/3;touch-action:none;cursor:crosshair}
.ma-play{position:absolute;left:10px;top:10px;display:flex;gap:6px;flex-wrap:wrap}
.ma-play button{border:0;border-radius:999px;background:rgba(255,255,255,.88);color:#0f172a;font:inherit;font-weight:800;font-size:12.5px;padding:7px 12px;cursor:pointer}
.ma-tip{position:absolute;left:50%;bottom:10px;transform:translateX(-50%);background:rgba(15,23,42,.72);color:#fff;font-size:12px;font-weight:700;border-radius:12px;padding:5px 12px;max-width:92%;text-align:center;pointer-events:none;transition:opacity .4s;white-space:nowrap}
.ma-tip.hide{opacity:0}
.ma-sum{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:12px}
.ma-sum div{background:#eff6ff;border-radius:12px;padding:10px 4px;text-align:center;min-width:0}
.ma-sum b{display:block;font-size:20px;color:#1d4ed8;font-variant-numeric:tabular-nums}
.ma-sum b small{font-size:11.5px}
.ma-sum span{font-size:11.5px;color:var(--ink-2);font-weight:700}
.ma-note{font-size:13.5px;color:var(--ink);background:#eff6ff;border-radius:10px;padding:9px 12px;margin:10px 0 0;font-weight:700}
.ma-cols{display:grid;grid-template-columns:1fr 1fr;gap:6px 22px}
.ma-cols input[type=range]{width:100%}
@media (max-width:640px){.ma-cols{grid-template-columns:1fr}.ma-play button{padding:6px 10px;font-size:12px}.ma-sum b{font-size:17px}}
</style>
"""

BODY = r"""
  <section class="panel" id="resultPanel">
    <div id="maWrap">
      <canvas id="maCv" aria-label="夜の街の明かりを背にした窓ガラスと、そこについた雨つぶの絵"></canvas>
      <div class="ma-play"><button type="button" id="maPlay">⏸ 止める</button><button type="button" id="maWipe">🧽 ワイパー</button></div>
      <div class="ma-tip" id="maTip">👆 なぞると、つぶを集められます</div>
    </div>
    <div class="ma-sum">
      <div><b id="maN">0</b><span>いまのつぶの数</span></div>
      <div><b id="maD">0</b><span>いちばん大きいつぶ</span></div>
      <div><b id="maF">0</b><span>流れ落ちた数</span></div>
    </div>
    <p class="ma-note" id="maNote">☔ 雨つぶがつきはじめました。</p>

    <h2 style="margin:20px 0 10px;font-size:18px;">雨とガラスを変える</h2>
    <div class="ma-cols">
      <div class="field"><label>☔ 雨の強さ <span class="hint">（<b id="maVRain"></b>）</span></label><input type="range" id="maRain" min="0" max="100" step="5" value="50"></div>
      <div class="field"><label>✨ ガラスのはじきやすさ <span class="hint">（<b id="maVRep"></b>）</span></label><input type="range" id="maRep" min="0" max="100" step="5" value="50"></div>
      <div class="field"><label>🍃 風 <span class="hint">（<b id="maVWind"></b>）</span></label><input type="range" id="maWind" min="-100" max="100" step="10" value="0"></div>
    </div>

    <div style="text-align:center;margin-top:16px;"><span id="shareCount" class="share-count" style="display:none"></span></div>
    <div class="share-row">
      <button class="btn btn-x" id="shareBtn">𝕏 でシェア</button>
      <button class="btn btn-ghost" id="copyBtn">結果をコピー</button>
    </div>
  </section>
"""

JS = r"""
(() => {
  const $ = id => document.getElementById(id);
  const cv = $('maCv'), ctx = cv.getContext('2d');
  const VW = 80, VH = 60, MAX = 650, HARD = 800;
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  function rng(s) { s = s >>> 0; return () => { s = (s + 0x6D2B79F5) >>> 0; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }

  // ---------- 状態（単位は mm。画面は よこ80mm × たて60mm） ----------
  let drops = [], streaks = [], t = 0, fallen = 0, spawnAcc = 0, playing = true, held = null, px = 0, py = 0, wipeX = null, touched = false;
  const P = { rain: 50, rep: 50, wind: 0 };
  const windX = () => P.wind / 100;
  const rcBase = () => 2.6 - 1.6 * P.rep / 100;                       // 流れ出す半径（風なし）
  const rcEff = () => rcBase() / Math.pow(1 + windX() * windX(), .25); // 風があると少し流れやすい
  function mk(x, y, r) { return { x, y, r, vx: 0, vy: 0, sliding: false, held: false, dirty: true, dead: false, born: t, wob: 0, tr: 0, next: 1.5, sx: x, sy: y }; }
  function absorb(d, o) {
    const a = d.r * d.r * d.r, b = o.r * o.r * o.r, v = a + b, wd = a / v;
    if (!d.held) { d.x = d.x * wd + o.x * (1 - wd); d.y = d.y * wd + o.y * (1 - wd); }
    if (d.sliding || o.sliding) { d.vx = d.vx * wd + o.vx * (1 - wd); d.vy = d.vy * wd + o.vy * (1 - wd); if (!d.held) d.sliding = true; }
    d.r = Math.cbrt(v); d.wob = 1; o.dead = true;
  }

  function step(dt) {
    t += dt;
    const rc = rcEff(), rs = rc * .6, wx = windX();
    // 雨がつく
    spawnAcc += P.rain * 1.2 * dt;
    while (spawnAcc >= 1) {
      spawnAcc -= 1;
      const x = Math.random() * VW, y = Math.random() * VH, r = .35 + Math.random() * .7;
      let hit = null, best = 1e9, near = null;
      for (let i = 0; i < drops.length; i++) {
        const o = drops[i], dx = o.x - x, dy = o.y - y, q = dx * dx + dy * dy, rr = (o.r + r) * .9;
        if (q < rr * rr) { hit = o; break; }
        if (q < best) { best = q; near = o; }
      }
      if (!hit && drops.length >= MAX) hit = near;
      if (hit) { hit.r = Math.cbrt(hit.r * hit.r * hit.r + r * r * r); hit.dirty = true; hit.wob = Math.max(hit.wob, .6); hit.born = t; }
      else drops.push(mk(x, y, r));
    }
    // 指でつかんでいるつぶ
    if (held) { held.x = px; held.y = py; held.sx = px; held.sy = py; held.dirty = true; }
    // 動く
    const damp = Math.exp(-5 * dt);
    for (let i = 0, n = drops.length; i < n; i++) {
      const d = drops[i]; if (d.dead) continue;
      d.wob *= damp;
      if (d.held) continue;
      if (!d.sliding) { if (d.r > rc) { d.sliding = true; d.vx = 0; d.vy = 0; d.tr = 0; d.sx = d.x; d.sy = d.y; } else continue; }
      const f = 1 - (rs / d.r) * (rs / d.r);
      if (f < .06) { d.sliding = false; d.vx = d.vy = 0; continue; }
      const a = 300 * f;
      d.vx += (wx * a - 3.5 * d.vx) * dt + (Math.random() - .5) * 70 * dt;
      d.vy += (a - 3.5 * d.vy) * dt;
      const mx = d.vx * dt, my = d.vy * dt, ds = Math.hypot(mx, my);
      d.x += mx; d.y += my; d.tr += ds;
      if (Math.hypot(d.x - d.sx, d.y - d.sy) > .9) {
        streaks.push({ x0: d.sx, y0: d.sy, x1: d.x, y1: d.y, w: d.r * .8, life: 1 }); d.sx = d.x; d.sy = d.y;
        if (streaks.length > 520) streaks.splice(0, streaks.length - 520);
      }
      if (d.tr > d.next && ds > 1e-6 && drops.length < HARD) {
        const rt = Math.min(.5, d.r * .28) * (.6 + Math.random() * .4), v = d.r * d.r * d.r - rt * rt * rt;
        if (v > .02) {
          d.r = Math.cbrt(v);
          const ux = mx / ds, uy = my / ds, back = d.r + rt + .25, j = (Math.random() - .5) * d.r * .7;
          const nd = mk(d.x - ux * back - uy * j, d.y - uy * back + ux * j, rt); nd.born = t - 9; nd.dirty = false; drops.push(nd);
        }
        d.tr = 0; d.next = 1.2 + Math.random() * 1.8;
      }
      if (d.y - d.r > VH || d.x + d.r < 0 || d.x - d.r > VW) { d.dead = true; fallen++; }
    }
    // くっつく（動いた・大きくなったつぶだけ調べる）
    for (let i = 0; i < drops.length; i++) {
      const d = drops[i]; if (d.dead || !(d.dirty || d.sliding || d.held)) continue;
      let merged = false;
      for (let j = 0; j < drops.length; j++) {
        const o = drops[j]; if (o === d || o.dead || o.held) continue;
        const dx = o.x - d.x, dy = o.y - d.y, rr = (d.r + o.r) * .85 + (d.held ? 1.2 : 0);
        if (dx * dx + dy * dy < rr * rr) {
          if (o.r > d.r && !d.held) { absorb(o, d); o.dirty = true; break; }
          absorb(d, o); merged = true;
        }
      }
      if (!d.dead) d.dirty = merged;
    }
    // ワイパー
    if (wipeX !== null) {
      wipeX += 170 * dt;
      for (const d of drops) if (!d.held && d.x - d.r < wipeX) d.dead = true;
      for (const s of streaks) if (s.x0 < wipeX) s.life = 0;
      if (wipeX > VW + 4) wipeX = null;
    }
    for (const s of streaks) s.life -= dt / 2.6;
    if (streaks.length && streaks[0].life <= 0) streaks = streaks.filter(s => s.life > 0);
    drops = drops.filter(d => !d.dead);
  }

  // ---------- 描く ----------
  let dpr = 1; const bg = document.createElement('canvas');
  function mkSprite(lens) {
    const n = 96, s = document.createElement('canvas'); s.width = s.height = n; const c = s.getContext('2d'), h = n / 2;
    const g = c.createRadialGradient(h, h * 1.05, h * .1, h, h, h);
    if (lens) { g.addColorStop(0, 'rgba(255,255,255,0)'); g.addColorStop(.6, 'rgba(10,16,36,.06)'); g.addColorStop(.88, 'rgba(6,10,26,.5)'); g.addColorStop(.97, 'rgba(4,8,20,.78)'); g.addColorStop(1, 'rgba(4,8,20,0)'); }
    else { g.addColorStop(0, 'rgba(215,230,255,.42)'); g.addColorStop(.55, 'rgba(150,180,230,.28)'); g.addColorStop(.86, 'rgba(20,30,60,.5)'); g.addColorStop(.96, 'rgba(6,10,26,.7)'); g.addColorStop(1, 'rgba(6,10,26,0)'); }
    c.fillStyle = g; c.beginPath(); c.arc(h, h, h, 0, 7); c.fill();
    c.strokeStyle = 'rgba(255,236,190,.55)'; c.lineWidth = n * .05; c.lineCap = 'round'; c.beginPath(); c.arc(h, h, h * .72, Math.PI * .22, Math.PI * .78); c.stroke();
    c.fillStyle = 'rgba(255,255,255,.9)'; c.beginPath(); c.ellipse(h * .68, h * .6, h * .17, h * .1, -.6, 0, 7); c.fill();
    return s;
  }
  const spS = mkSprite(false), spL = mkSprite(true);
  function mkBg(W, Hh) {
    bg.width = W; bg.height = Hh; const c = bg.getContext('2d'), R = rng(20261124);
    const g = c.createLinearGradient(0, 0, 0, Hh); g.addColorStop(0, '#070b1a'); g.addColorStop(.6, '#131a33'); g.addColorStop(1, '#1d1730'); c.fillStyle = g; c.fillRect(0, 0, W, Hh);
    const cols = ['255,196,92', '255,150,70', '255,90,90', '120,220,255', '255,240,210', '140,255,190', '255,120,200'];
    c.globalCompositeOperation = 'lighter';
    for (let i = 0; i < 56; i++) {
      const x = R() * W, y = Hh * (.1 + R() * .82), r = W * (.025 + R() * .06), col = cols[Math.floor(R() * cols.length)], a = .1 + R() * .3;
      const gr = c.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, `rgba(${col},${a.toFixed(3)})`); gr.addColorStop(.72, `rgba(${col},${(a * .8).toFixed(3)})`); gr.addColorStop(1, `rgba(${col},0)`);
      c.fillStyle = gr; c.beginPath(); c.arc(x, y, r, 0, 7); c.fill();
    }
    c.globalCompositeOperation = 'source-over';
  }
  function size() {
    const w = cv.clientWidth || 600; dpr = Math.min(2, window.devicePixelRatio || 1);
    const W = Math.round(w * dpr), Hh = Math.round(W * .75);
    if (cv.width !== W || cv.height !== Hh) { cv.width = W; cv.height = Hh; mkBg(W, Hh); }
  }
  function draw() {
    size();
    const c = ctx, W = cv.width, Hh = cv.height, S = W / VW, big = 5 * dpr;
    c.setTransform(1, 0, 0, 1, 0, 0); c.globalAlpha = 1;
    c.drawImage(bg, 0, 0);
    c.fillStyle = 'rgba(170,190,220,.07)'; c.fillRect(0, 0, W, Hh);
    c.lineCap = 'round';
    for (const s of streaks) { if (s.life <= 0) continue; c.strokeStyle = `rgba(190,215,255,${(.14 * s.life).toFixed(3)})`; c.lineWidth = Math.max(1, s.w * S * 1.6); c.beginPath(); c.moveTo(s.x0 * S, s.y0 * S); c.lineTo(s.x1 * S, s.y1 * S); c.stroke(); }
    for (const d of drops) {
      const R = d.r * S, x = d.x * S, y = d.y * S;
      if (R < big) c.drawImage(spS, x - R, y - R, 2 * R, 2 * R);
      else {
        const sp = d.sliding ? Math.hypot(d.vx, d.vy) : 0, k = 1 + Math.min(.3, sp / 160), wb = 1 + .1 * d.wob * Math.sin(t * 28 + d.x);
        c.save(); c.translate(x, y); if (sp > 1) c.rotate(Math.atan2(d.vy, d.vx) - Math.PI / 2); c.scale(wb / Math.sqrt(k), k / wb);
        c.beginPath(); c.arc(0, 0, R, 0, 7); c.clip();
        const sw = Math.min(W, R * 5), sh = Math.min(Hh, R * 5), sx0 = clamp(x - sw / 2, 0, W - sw), sy0 = clamp(y - sh / 2, 0, Hh - sh);
        c.rotate(Math.PI); c.drawImage(bg, sx0, sy0, sw, sh, -R, -R, 2 * R, 2 * R); c.rotate(-Math.PI);
        c.drawImage(spL, -R, -R, 2 * R, 2 * R);
        c.restore();
      }
      const age = t - d.born;
      if (age >= 0 && age < .35) { c.strokeStyle = `rgba(220,235,255,${(.5 * (1 - age / .35)).toFixed(3)})`; c.lineWidth = 1.2 * dpr; c.beginPath(); c.arc(x, y, R * (1 + 1.6 * age / .35) + 1, 0, 7); c.stroke(); }
    }
    if (held) { c.strokeStyle = 'rgba(255,255,255,.55)'; c.lineWidth = 1.5 * dpr; c.setLineDash([4 * dpr, 4 * dpr]); c.beginPath(); c.arc(held.x * S, held.y * S, (held.r + 1.6) * S, 0, 7); c.stroke(); c.setLineDash([]); }
    if (wipeX !== null) {
      const x = wipeX * S, g = c.createLinearGradient(x - 14 * S, 0, x, 0); g.addColorStop(0, 'rgba(200,220,255,0)'); g.addColorStop(1, 'rgba(200,220,255,.22)');
      c.fillStyle = g; c.fillRect(x - 14 * S, 0, 14 * S, Hh);
      c.fillStyle = 'rgba(8,10,18,.95)'; c.fillRect(x, 0, 1.3 * S, Hh); c.fillStyle = 'rgba(120,130,150,.9)'; c.fillRect(x + 1.3 * S, 0, .4 * S, Hh);
    }
    ui();
  }

  // ---------- 数字 ----------
  function summary() {
    let mx = 0, sl = 0, nan = false;
    for (const d of drops) { if (d.r > mx) mx = d.r; if (d.sliding) sl++; if (!(isFinite(d.x) && isFinite(d.y) && isFinite(d.r) && isFinite(d.vx) && isFinite(d.vy))) nan = true; }
    return { n: drops.length, maxD: +(mx * 2).toFixed(2), fallen, sliding: sl, streaks: streaks.length, startD: +(rcEff() * 2).toFixed(2), t: +t.toFixed(2), nan, wiping: wipeX !== null, rain: P.rain, rep: P.rep, wind: P.wind };
  }
  let lastUI = 0;
  function ui(force) {
    const now = performance.now(); if (!force && now - lastUI < 160) return; lastUI = now;
    const s = summary();
    $('maN').innerHTML = s.n + '<small>こ</small>';
    $('maD').innerHTML = '<small>直径 約</small>' + s.maxD.toFixed(1) + '<small>mm</small>';
    $('maF').innerHTML = s.fallen + '<small>こ</small>';
    $('maNote').textContent = !playing ? '⏸ 止めています。' : s.wiping ? '🧽 ワイパーでふいています。' : s.sliding > 0 ? `💧 大きくなったつぶが${s.sliding}こ、道すじのつぶを集めながら流れています。`
      : P.rain === 0 ? (s.n ? '🌙 雨は止んでいます。指でなぞって、つぶを集めてみましょう。' : '🌙 雨は止んでいます。') : `☔ つぶがくっついて大きくなっています。直径が約${s.startD.toFixed(1)}mmをこえると流れ出します。`;
  }

  // ---------- 操作 ----------
  const binds = [
    ['maRain', 'rain', v => v === 0 ? 'なし' : v < 35 ? '小雨' : v < 70 ? 'ふつう' : '大雨'],
    ['maRep', 'rep', v => (v < 35 ? 'はじきにくい' : v < 70 ? 'ふつう' : 'よくはじく') + '・直径 約' + (rcBase() * 2).toFixed(1) + 'mmで流れ出す'],
    ['maWind', 'wind', v => v === 0 ? 'なし' : (v < 0 ? '← 左へ ' : '右へ → ') + (Math.abs(v) < 50 ? '弱い' : '強い')],
  ];
  binds.forEach(([id, key, f]) => { const el = $(id), out = $('maV' + id.slice(2)); const up = () => { P[key] = +el.value; out.textContent = f(P[key]); ui(true); }; el.addEventListener('input', up); up(); });
  $('maPlay').addEventListener('click', () => { playing = !playing; $('maPlay').textContent = playing ? '⏸ 止める' : '▶ 動かす'; ui(true); });
  function wipe() { if (wipeX === null) wipeX = -2; }
  $('maWipe').addEventListener('click', wipe);
  function pos(e) { const r = cv.getBoundingClientRect(); px = clamp((e.clientX - r.left) / r.width * VW, 0, VW); py = clamp((e.clientY - r.top) / r.height * VH, 0, VH); }
  function grab(e) {
    pos(e); if (!touched) { touched = true; $('maTip').classList.add('hide'); }
    let pick = null;
    for (const d of drops) { const dx = d.x - px, dy = d.y - py, rr = d.r + 1; if (dx * dx + dy * dy < rr * rr && (!pick || d.r > pick.r)) pick = d; }
    if (!pick) { pick = mk(px, py, .3); pick.born = t - 9; drops.push(pick); }
    pick.held = true; pick.sliding = false; pick.vx = pick.vy = 0; held = pick;
  }
  function release() { if (held) { held.held = false; held.dirty = true; held.sx = held.x; held.sy = held.y; held = null; } }
  cv.addEventListener('pointerdown', e => { e.preventDefault(); try { cv.setPointerCapture(e.pointerId); } catch (_) {} release(); grab(e); });
  cv.addEventListener('pointermove', e => { if (held) pos(e); });
  ['pointerup', 'pointercancel', 'lostpointercapture'].forEach(n => cv.addEventListener(n, release));

  // ---------- シェア ----------
  function shareText() { const s = summary(); return `窓ガラスの雨つぶを観察しました。いまのつぶは${s.n}こ、いちばん大きいつぶは直径 約${s.maxD.toFixed(1)}mm、流れ落ちたつぶは${s.fallen}こでした☔`; }
  $('shareBtn').addEventListener('click', () => { const u = location.origin + location.pathname; window.open('https://twitter.com/intent/tweet?text=' + encodeURIComponent(shareText() + '\n') + '&url=' + encodeURIComponent(u) + '&hashtags=' + encodeURIComponent('シミュラボ'), '_blank', 'noopener'); });
  $('copyBtn').addEventListener('click', async () => { const b = $('copyBtn'); try { await navigator.clipboard.writeText(shareText() + '\n' + location.origin + location.pathname); b.textContent = 'コピーしました'; } catch (e) { b.textContent = 'コピーできませんでした'; } setTimeout(() => { b.textContent = '結果をコピー'; }, 1800); });

  // ---------- 動かす ----------
  function advance(sec) { const n = Math.max(1, Math.ceil(sec * 60)), dt = sec / n; for (let i = 0; i < n; i++) step(dt); }
  let tPrev = performance.now();
  function loop(now) {
    const dt = Math.min(.05, (now - tPrev) / 1000); tPrev = now;
    if (playing && dt > 0) advance(dt);
    draw(); requestAnimationFrame(loop);
  }
  advance(14);
  requestAnimationFrame(loop);
  window.__t = {
    step(sec) { advance(sec); draw(); ui(true); },
    get s() { return summary(); },
    set(o) { Object.assign(P, o); binds.forEach(([id, key]) => { $(id).value = P[key]; $(id).dispatchEvent(new Event('input')); }); },
    wipe, grabAt(x, y) { release(); px = x; py = y; grab({ clientX: cv.getBoundingClientRect().left + x / VW * cv.getBoundingClientRect().width, clientY: cv.getBoundingClientRect().top + y / VH * cv.getBoundingClientRect().height }); },
    moveTo(x, y) { px = x; py = y; }, release,
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
    <p class="ma-note" style="font-weight:400">{esc(NOTE)}</p>
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
