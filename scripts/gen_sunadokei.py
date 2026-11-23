# -*- coding: utf-8 -*-
"""砂時計シミュレーター（2026-11-24） sims/sunadokei/index.html を書き出す（冪等）。
   使い方: python -X utf8 scripts/gen_sunadokei.py
   ※ページの外わく（build のHTML）は gen_jibun_shokubutsu.py の build() をそのまま使う。"""
import io, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_jibun_shokubutsu as base  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = "sunadokei"
NAME = "砂時計シミュレーター"
CAT = "ふしぎ・現象"
TITLE = "砂時計シミュレーター｜砂はなぜ同じ速さで落ちる？（くびれの太さ・砂の量を変えて確かめる）｜シミュラボ"
DESC = ("砂時計のくびれを通って砂のつぶが落ち、下に山ができていく様子を見られるシミュレーター。"
        "くびれの太さと砂の量を変えて、落ちる速さ（つぶ/秒）がどう変わるかをグラフで確かめられます。水とちがい、砂は上にどれだけ残っていても落ちる速さがほぼ変わりません。")
OG_T = "砂時計シミュレーター 砂はなぜ同じ速さで落ちる？"
OG_D = "くびれの太さと砂の量を変えて、砂の落ちる速さがほぼ一定になることをグラフで確かめよう。"
H1 = "砂時計シミュレーター<br>砂はなぜ同じ速さで落ちる？"
LEAD = ("砂時計の砂は、上にたくさん残っているときも、少ししか残っていないときも、ほぼ同じ速さで落ちます。だから時計として使えます。"
        "くびれの太さや砂の量を変えて、落ちる速さのグラフがほぼ平らになることを確かめてみましょう。")
NOTE = "📏 このページの数値（秒・つぶ/秒）は、画面の中のつぶモデルでの「めやす」です。本物の砂時計の時間とは一致しません。"

FAQ = [
    ("どうやって遊びますか？", "開くとすぐに砂が落ちはじめます。「くびれの太さ」と「砂の量」を変えると、最初からやり直します。ぜんぶ落ちたら「ひっくり返す」をおすと、もう一度落ちます。スロー・早送りで見やすい速さにできます。"),
    ("砂が少なくなっても、落ちる速さが変わらないのはなぜですか？", "砂のつぶは、となりのつぶやガラスのかべと押し合って、たがいに支え合っています。上の砂の重さの多くはかべの方へ逃げるので、くびれのところにかかる力は、上の砂の量にあまりよりません。そのため、落ちる速さもほぼ同じになります。"),
    ("くびれを太くすると、どうなりますか？", "一度に通れるつぶが増えるので、速く落ちます。このシミュレーターでは、くびれの太さにほぼ比例して速くなります。本物の砂では、太さを少し広げただけでも、落ちる量がもっと大きく増えることが知られています。"),
]
REL = [("sandpile", "⛰️", "砂山崩しシミュレーター"), ("galton", "🎯", "ガルトンボード"), ("domino-taoshi", "🧱", "ドミノ倒しシミュレーター")]

ARTICLE = """
<h2>水と砂のちがい</h2>
<p>バケツの底に穴をあけて水を入れると、水がたくさん入っているときは勢いよく出て、少なくなると弱くなります。水は深いほど底をおす力（水圧）が大きくなるからです。</p>
<p>砂はちがいます。砂のつぶは、となりのつぶやガラスのかべとこすれ合い、たがいに支え合っています。上の砂の重さの多くは、ななめにつたわってかべの方へ逃げます。そのため、くびれのところにかかる力は、上にどれだけ砂が残っているかにあまりよりません。この性質は、穀物をためるサイロの研究で古くから知られています。</p>
<p>だから砂時計は、砂が多いときも少ないときも、ほぼ同じ速さで砂を落とします。同じ量の砂を入れれば、毎回ほぼ同じ時間で落ちきるので、時計として使えます。</p>

<h2>ためしてみたいこと</h2>
<ul>
<li><b>グラフを見る</b>：「落ちる速さ」の線が、はじめから終わり近くまでほぼ平らになります（小さなゆれは、つぶがつかえたり通ったりするためです）。</li>
<li><b>砂の量を2倍にする</b>：落ちる速さはほぼ同じままで、落ちきる時間がほぼ2倍になります。</li>
<li><b>くびれを太くする</b>：落ちる速さが上がり、落ちきる時間が短くなります。</li>
<li><b>上と下の形を見る</b>：上の砂はまん中からへこんで「すりばち」の形に減り、下の砂はくずれながら「山」の形に積もります。</li>
</ul>

<h2>このシミュレーターのしくみ</h2>
<p>画面を小さなマス目に分け、砂のつぶを1マスに1つ置いています。つぶは、真下があいていれば真下へ、ふさがっていればななめ下へ動きます。くびれでは、つぶがときどきつかえるようにしてあります。とても単純にしたモデルなので、砂の山のかたむきや、くびれの太さと速さの関係は、本物の砂とは同じではありません。</p>
<p>本物の砂では、穴から落ちる量は、穴の直径の約2.5乗に比例することが実験で知られています（ベバルーの式）。穴がつぶの数個分より細いと、つぶがアーチのように組み合わさって、つまることもあります。</p>
"""

REFS = [
    "Janssen, H. A. (1895) Versuche über Getreidedruck in Silozellen. Zeitschrift des Vereines Deutscher Ingenieure 39, 1045–1049.（かべが粉や粒の重さを支えること）",
    "Beverloo, W. A., Leniger, H. A. &amp; van de Velde, J. (1961) The flow of granular solids through orifices. Chemical Engineering Science 15, 260–269.（穴から落ちる粒の量の式）",
]

STAGE = r"""
<style>
.sd-wrap{position:relative;border-radius:14px;border:1px solid var(--line);background:linear-gradient(#f8fafc,#eef2ff);overflow:hidden}
#sd{display:block;width:100%;max-width:400px;margin:0 auto;aspect-ratio:3/4}
.sd-play{position:absolute;left:8px;top:8px;display:flex;gap:5px;flex-wrap:wrap;max-width:calc(100% - 16px)}
.sd-play button{border:0;border-radius:999px;background:rgba(15,23,42,.8);color:#fff;font:inherit;font-weight:800;font-size:12px;padding:6px 10px;cursor:pointer}
.sd-play button.on{background:#f59e0b;color:#111}
.sd-sum{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:12px}
.sd-sum div{background:#fffbeb;border-radius:12px;padding:10px 4px;text-align:center;min-width:0}
.sd-sum b{display:block;font-size:20px;color:#b45309;font-variant-numeric:tabular-nums}
.sd-sum b small{font-size:11px}
.sd-sum span{font-size:11.5px;color:var(--ink-2);font-weight:700}
.sd-note{font-size:13.5px;color:var(--ink);background:#fffbeb;border-radius:10px;padding:9px 12px;margin:10px 0 0;font-weight:700}
#sdG{display:block;width:100%;height:120px;margin-top:10px}
.sd-legend{font-size:12px;color:var(--ink-2);display:flex;gap:14px;flex-wrap:wrap}
.sd-legend i{display:inline-block;width:18px;height:3px;vertical-align:3px;margin-right:4px;background:#d97706}
.sd-legend i.o{background:repeating-linear-gradient(90deg,#2563eb 0 5px,transparent 5px 8px)}
.sd-cols{display:grid;grid-template-columns:1fr 1fr;gap:6px 22px;margin-top:14px}
@media (max-width:640px){.sd-sum{grid-template-columns:repeat(2,1fr)}.sd-cols{grid-template-columns:1fr}}
</style>
"""

BODY = r"""
  <section class="panel" id="resultPanel">
    <div class="sd-wrap">
      <canvas id="sd" aria-label="砂時計の中で砂のつぶが落ちている絵"></canvas>
      <div class="sd-play"><button type="button" id="sdPlay">⏸ 止める</button><button type="button" data-sp="0.25">🐢 スロー</button><button type="button" data-sp="1" class="on">ふつう</button><button type="button" data-sp="4">⏩ 早送り</button></div>
    </div>
    <div class="sd-sum">
      <div><b id="sdT">0</b><span>経過時間</span></div>
      <div><b id="sdP">0</b><span>落ちた砂</span></div>
      <div><b id="sdR">0</b><span>いまの速さ</span></div>
      <div><b id="sdA">0</b><span>平均の速さ</span></div>
    </div>
    <p class="sd-note" id="sdNote">⏳ 砂が落ちています。</p>
    <canvas id="sdG" aria-label="落ちる速さの変化のグラフ"></canvas>
    <div class="sd-legend"><span><i></i>落ちる速さ（つぶ/秒）</span><span><i class="o"></i>ここまでの平均</span></div>

    <div class="sd-cols">
      <div class="field"><label>くびれの太さ <span class="hint">（<b id="vNeck"></b>）</span></label><input type="range" id="kNeck" min="1" max="4" step="1" value="2"></div>
      <div class="field"><label>砂の量 <span class="hint">（<b id="vAmt"></b>）</span></label><input type="range" id="kAmt" min="150" max="550" step="50" value="400"></div>
    </div>
    <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:10px">
      <button class="btn btn-primary" id="sdFlip" type="button" style="width:auto;padding:10px 18px;">🔄 ひっくり返す</button>
      <button class="btn btn-ghost" id="sdReset" type="button" style="width:auto;padding:10px 14px;">さいしょから</button>
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
  const cv = $('sd'), ctx = cv.getContext('2d'), gc = $('sdG'), gx = gc.getContext('2d');
  const C = 41, R = 61, MID = 30, CX = 20, FPS = 30, PASS = .35;
  const COL = ['#d97706', '#f59e0b', '#b45309'];
  let neck = 2, amt = 400, speed = 1, playing = true;
  let grid, LO, HI, total = 0, below = 0, steps = 0, t = 0, done = false, ring, hist, rate = 0, idle = 0, acc = 0, flips = 0;

  function shape() {
    LO = new Int16Array(R); HI = new Int16Array(R);
    for (let y = 0; y < R; y++) { const s = Math.min(17, Math.round(Math.abs(y - MID) * .9)); LO[y] = CX - Math.floor((neck - 1) / 2) - s; HI[y] = CX + Math.floor(neck / 2) + s; }
  }
  function clock() { below = 0; steps = 0; t = 0; done = total === 0; ring = new Uint8Array(FPS); hist = []; rate = 0; idle = 0; acc = 0; }
  function reset() {
    shape(); grid = new Uint8Array(C * R); let n = 0;
    for (let y = MID; y >= 0 && n < amt; y--) for (let x = LO[y]; x <= HI[y] && n < amt; x++) { grid[y * C + x] = 1 + ((x * 7 + y * 13) % 3); n++; }
    total = n; flips = 0; clock();
  }
  function flip() {
    const g2 = new Uint8Array(C * R); let n = 0;
    for (let y = 0; y < R; y++) for (let x = 0; x < C; x++) { const v = grid[(R - 1 - y) * C + x]; g2[y * C + x] = v; if (v && y <= MID) n++; }
    grid = g2; total = n; flips++; clock(); playing = true; updPlay();
  }
  function step() {
    let cross = 0;
    for (let y = R - 2; y >= 0; y--) {
      const ny = y + 1, l = LO[ny], h = HI[ny], a = LO[y], b = HI[y], ltr = (steps + y) & 1;
      for (let i = a; i <= b; i++) {
        const x = ltr ? i : a + b - i, v = grid[y * C + x]; if (!v) continue;
        if (y === MID && Math.random() > PASS) continue;
        let nx = -1;
        if (x >= l && x <= h && !grid[ny * C + x]) nx = x;
        else {
          const d = Math.random() < .5 ? -1 : 1;
          if (x + d >= l && x + d <= h && !grid[ny * C + x + d]) nx = x + d;
          else if (x - d >= l && x - d <= h && !grid[ny * C + x - d]) nx = x - d;
        }
        if (nx >= 0) { grid[y * C + x] = 0; grid[ny * C + nx] = v; if (y === MID) cross++; }
      }
    }
    below += cross; ring[steps % FPS] = cross; steps++; t = steps / FPS;
    rate = 0; for (let i = 0; i < FPS; i++) rate += ring[i];
    if (steps >= FPS && steps % 15 === 0) hist.push([t, rate]);
    idle = cross ? 0 : idle + 1;
    if (below >= total || idle > FPS * 3) done = true;
  }

  let dpr = 1;
  function size() {
    dpr = Math.min(2, window.devicePixelRatio || 1);
    const w = cv.clientWidth || 360, W = Math.round(w * dpr), Hh = Math.round(w * 4 / 3 * dpr);
    if (cv.width !== W || cv.height !== Hh) { cv.width = W; cv.height = Hh; }
    const gw = gc.clientWidth || 360, GW = Math.round(gw * dpr), GH = Math.round(120 * dpr);
    if (gc.width !== GW || gc.height !== GH) { gc.width = GW; gc.height = GH; }
  }
  function draw() {
    size();
    const c = ctx, W = cv.width, Hh = cv.height;
    c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, W, Hh);
    const cs = Math.min(W / (C + 2), Hh / (R + 7)), ox = (W - C * cs) / 2, oy = (Hh - R * cs) / 2 + cs * .8;
    // ガラス
    c.beginPath(); c.moveTo(ox + LO[0] * cs - cs * .4, oy);
    for (let y = 0; y < R; y++) c.lineTo(ox + LO[y] * cs - cs * .4, oy + (y + .5) * cs);
    c.lineTo(ox + LO[R - 1] * cs - cs * .4, oy + R * cs); c.lineTo(ox + (HI[R - 1] + 1) * cs + cs * .4, oy + R * cs);
    for (let y = R - 1; y >= 0; y--) c.lineTo(ox + (HI[y] + 1) * cs + cs * .4, oy + (y + .5) * cs);
    c.lineTo(ox + (HI[0] + 1) * cs + cs * .4, oy); c.closePath();
    c.fillStyle = 'rgba(186,230,253,.45)'; c.fill(); c.strokeStyle = '#7dd3fc'; c.lineWidth = 2 * dpr; c.lineJoin = 'round'; c.stroke();
    // 台
    c.fillStyle = '#92400e'; c.fillRect(ox + cs, oy - cs * 1.8, (C - 2) * cs, cs * 1.8); c.fillRect(ox + cs, oy + R * cs, (C - 2) * cs, cs * 1.8);
    // 砂
    for (let k = 1; k <= 3; k++) {
      c.fillStyle = COL[k - 1]; c.beginPath();
      for (let y = 0; y < R; y++) for (let x = LO[y]; x <= HI[y]; x++) if (grid[y * C + x] === k) { const px = ox + (x + .5) * cs, py = oy + (y + .5) * cs; c.moveTo(px + cs * .5, py); c.arc(px, py, cs * .5, 0, 6.3); }
      c.fill();
    }
    graph(); ui();
  }
  function graph() {
    const c = gx, W = gc.width, Hh = gc.height, p = 34 * dpr, r = 8 * dpr;
    c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, W, Hh);
    let mx = 20; for (const q of hist) if (q[1] > mx) mx = q[1];
    const maxR = Math.ceil(mx * 1.25 / 10) * 10, maxT = Math.max(20, Math.ceil(t / 10) * 10);
    const X = v => p + v / maxT * (W - p - r), Y = v => Hh - 18 * dpr - v / maxR * (Hh - 28 * dpr);
    c.strokeStyle = '#e2e8f0'; c.lineWidth = dpr; c.fillStyle = '#64748b'; c.font = `${10 * dpr}px system-ui,sans-serif`; c.textAlign = 'right'; c.textBaseline = 'middle';
    [0, .5, 1].forEach(f => { const y = Y(maxR * f); c.beginPath(); c.moveTo(p, y); c.lineTo(W - r, y); c.stroke(); c.fillText(Math.round(maxR * f), p - 4 * dpr, y); });
    c.textAlign = 'center'; c.textBaseline = 'top';
    for (let v = 0; v <= maxT; v += maxT > 60 ? 20 : 10) c.fillText(v + '秒', X(v), Hh - 14 * dpr);
    if (t > 1 && below > 0) { const av = below / t; c.strokeStyle = '#2563eb'; c.lineWidth = 1.4 * dpr; c.setLineDash([5 * dpr, 3 * dpr]); c.beginPath(); c.moveTo(X(0), Y(av)); c.lineTo(X(t), Y(av)); c.stroke(); c.setLineDash([]); }
    c.strokeStyle = '#d97706'; c.lineWidth = 2.2 * dpr; c.lineJoin = 'round'; c.beginPath();
    hist.forEach((q, i) => i ? c.lineTo(X(q[0]), Y(q[1])) : c.moveTo(X(q[0]), Y(q[1]))); c.stroke();
  }
  const pct = () => total ? below / total * 100 : 0, avg = () => t > 0 ? below / t : 0;
  let lastUI = 0;
  function ui(force) {
    const now = performance.now(); if (!force && now - lastUI < 150) return; lastUI = now;
    $('sdT').innerHTML = t.toFixed(1) + '<small>秒</small>';
    $('sdP').innerHTML = pct().toFixed(0) + '<small>%</small>';
    $('sdR').innerHTML = (done ? 0 : rate) + '<small>つぶ/秒</small>';
    $('sdA').innerHTML = avg().toFixed(1) + '<small>つぶ/秒</small>';
    $('sdNote').textContent = done ? (below >= total ? `⌛ ぜんぶ落ちました（${t.toFixed(1)}秒・平均 ${avg().toFixed(1)} つぶ/秒）。「ひっくり返す」でもう一度ためせます。` : '⌛ 砂が止まりました。「ひっくり返す」でもう一度ためせます。')
      : pct() > 50 ? '⏳ 上の砂が半分より少なくなっても、落ちる速さはほぼ同じままです。' : '⏳ 砂が落ちています。グラフの線がほぼ平らなことを見てみましょう。';
  }
  function updPlay() { $('sdPlay').textContent = playing ? '⏸ 止める' : '▶ 動かす'; document.querySelectorAll('.sd-play [data-sp]').forEach(b => b.classList.toggle('on', +b.dataset.sp === speed)); }
  function labels() { $('vNeck').textContent = ['ほそい', 'ふつう', 'ふとい', 'とてもふとい'][neck - 1] + '・' + neck + 'つぶ分'; $('vAmt').textContent = amt + 'つぶ'; }

  $('kNeck').addEventListener('input', e => { neck = +e.target.value; labels(); reset(); playing = true; updPlay(); });
  $('kAmt').addEventListener('input', e => { amt = +e.target.value; labels(); reset(); playing = true; updPlay(); });
  $('sdFlip').addEventListener('click', flip);
  $('sdReset').addEventListener('click', () => { reset(); playing = true; updPlay(); });
  $('sdPlay').addEventListener('click', () => { playing = !playing; updPlay(); });
  document.querySelectorAll('.sd-play [data-sp]').forEach(b => b.addEventListener('click', () => { speed = +b.dataset.sp; playing = true; updPlay(); }));
  const shareText = () => `砂時計シミュレーターで、${total}つぶの砂が${pct().toFixed(0)}%落ちるまで${t.toFixed(1)}秒。落ちる速さは平均 ${avg().toFixed(1)} つぶ/秒でほぼ一定でした⏳`;
  $('shareBtn').addEventListener('click', () => { const u = location.origin + location.pathname; window.open('https://twitter.com/intent/tweet?text=' + encodeURIComponent(shareText() + '\n') + '&url=' + encodeURIComponent(u) + '&hashtags=' + encodeURIComponent('シミュラボ'), '_blank', 'noopener'); });
  $('copyBtn').addEventListener('click', async () => { try { await navigator.clipboard.writeText(shareText() + '\n' + location.origin + location.pathname); $('copyBtn').textContent = 'コピーしました'; } catch (e) { $('copyBtn').textContent = 'コピーできませんでした'; } });

  let tPrev = performance.now();
  function loop(now) {
    const dt = Math.min(.1, (now - tPrev) / 1000); tPrev = now;
    if (playing && !done) { acc += dt * FPS * speed; let n = 0; while (acc >= 1 && n < 40 && !done) { step(); acc -= 1; n++; } if (acc > 1) acc = 0; }
    draw(); requestAnimationFrame(loop);
  }
  labels(); reset(); updPlay(); draw();
  requestAnimationFrame(loop);
  window.__t = {
    step(sec) { const n = Math.round(sec * FPS); for (let i = 0; i < n && !done; i++) step(); draw(); ui(true); },
    get s() { let g = 0, lowG = 0; for (let i = 0; i < grid.length; i++) if (grid[i]) { g++; if (i >= (MID + 1) * C) lowG++; } return { t, total, below, top: total - below, pct: pct(), rate, avg: avg(), done, neck, amt, speed, playing, flips, grains: g, lowGrains: lowG, hist: hist.length, histMin: hist.length ? Math.min(...hist.map(q => q[1])) : 0, histMax: hist.length ? Math.max(...hist.map(q => q[1])) : 0 }; },
    flip, reset
  };
})();
"""


def build():
    for k in ("SLUG", "NAME", "CAT", "TITLE", "DESC", "OG_T", "OG_D", "H1", "LEAD", "NOTE", "FAQ", "REL", "ARTICLE", "REFS", "STAGE", "BODY", "JS"):
        setattr(base, k, globals()[k])
    return base.build().replace('class="pl-note"', 'class="sd-note"')


if __name__ == "__main__":
    out = os.path.join(ROOT, "sims", SLUG, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    io.open(out, "w", encoding="utf-8", newline="\n").write(build())
    print("wrote", out)
