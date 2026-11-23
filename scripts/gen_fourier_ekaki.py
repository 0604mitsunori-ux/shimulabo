# -*- coding: utf-8 -*-
"""回る円で絵を描く（フーリエ級数のお絵かき）シミュレーター（2026-11-24）
   sims/fourier-ekaki/index.html を書き出す（冪等）。 使い方: python -X utf8 scripts/gen_fourier_ekaki.py"""
import html as H, io, json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://shimulabo.com"
SLUG = "fourier-ekaki"
NAME = "回る円で絵を描くフーリエお絵かきシミュレーター"
CAT = "あそぶ・実験"
TITLE = "回る円をつないで絵を描く｜フーリエ級数のお絵かきシミュレーター（エピサイクル）｜シミュラボ"
DESC = ("指やマウスで一筆書きの線を描くと、その線を「大きさと速さのちがう、たくさんの回る円」に分けて、円の先に円をつないだ腕が同じ絵をなぞって描きます。"
        "円の数を減らすと絵が丸く単純になり、増やすと元の絵に近づきます。ハート・星・音符などの見本つき。フーリエ級数の考え方を目で見て確かめられます。")
OG_T = "回る円をつないで絵を描く フーリエお絵かきシミュレーター"
OG_D = "描いた線を、たくさんの回る円に分けて、もう一度描きなおす。円の数を変えると絵がどう変わるかを見てみよう。"
H1 = "回る円をつないで絵を描く<br>フーリエお絵かきシミュレーター"
LEAD = ("ハートや星の形を、「回る円の先に、また回る円」をつないだ腕が描いていきます。画面に指やマウスで一筆書きをすると、その線も同じように円に分けて描きなおします。"
        "使う円の数を減らしたり増やしたりして、絵がどう変わるかを見てみましょう。")

FAQ = [
    ("どうやって遊びますか？", "開くと、ハートの形を回る円が描きはじめます。上のボタンで星・音符などの見本に変えられます。黒い画面を指やマウスでなぞると、自分の一筆書きを描けます。指をはなすと、その線を円に分けて、自動で描きなおしが始まります。"),
    ("円の数を減らすと、なぜ絵が丸くなるのですか？", "円は半径の大きい順に使っています。大きい円は絵のおおまかな形を、小さくて速く回る円は角やこまかい曲がりを受けもっています。小さい円をはぶくと、こまかい部分がなくなり、丸くてなめらかな形になります。"),
    ("「元の絵とのずれ」は何の数字ですか？", "元の線の上にとった200個の点と、円で描いた線の同じ順番の点との距離の平均です。絵のはば（たてと横の大きいほう）を100としたときの数字で、0に近いほど元の絵と同じです。円を全部（199こ）使うと、ほぼ0になります。"),
    ("どんな線でも描けますか？", "一筆書き（ペンをはなさずに描ける線）なら描けます。書きはじめと書きおわりがはなれているときは、同じ線を行って帰ってくる動きにして、線がつながるようにしています。ペンをはなして2本以上の線を描く絵は、このシミュレーターではあつかえません。"),
    ("フーリエ級数は、何の役に立っているのですか？", "音や画像を「いろいろな速さの波の足し合わせ」に分けて考える方法のもとになっています。音楽（MP3など）や写真（JPEGなど）のデータを小さくする技術では、この考え方のなかまの計算を使って、人が気づきにくいこまかい成分をはぶいています。"),
]
REL = [("spirograph", "🌀", "スピログラフ"), ("lissajous", "〰️", "リサージュ図形"), ("wave", "🌊", "波の干渉シミュレーター")]

ARTICLE = """
<h2>このシミュレーターのしくみ</h2>
<p>このシミュレーターは、次の順番で動いています。</p>
<ul>
<li><b>① 線を200個の点にする</b>：描かれた線の上に、同じ間かくで200個の点をとります。</li>
<li><b>② 回る円に分ける</b>：200個の点を「フーリエ変換（離散フーリエ変換）」という計算にかけます。すると、<b>半径・回る速さ・はじめの向き</b>がそれぞれちがう199この円が求まります。回る速さは「1周するあいだに何回まわるか」で、右回りと左回りの両方があります。</li>
<li><b>③ 大きい順につなぐ</b>：円を半径の大きい順にならべ、1つ目の円のふちに2つ目の円の中心を、そのふちに3つ目の中心を…とつないでいきます。全部の円を同時に回すと、いちばん先の点が元の絵をなぞります。</li>
</ul>
<p>「円の数」を変えると、大きい方から何こまでを使うかが変わります。数字の「元の絵とのずれ」「いちばん大きい円の半径」は、絵のはば（たてと横の大きいほう）を100としたときの大きさです。</p>
<p>単純にした点もあります。線は200個の点でしか見ていないので、それよりこまかいギザギザは再現できません。また、描いた線は画面のまん中に合うように、大きさと位置を自動でそろえています。</p>

<h2>ためしてみたいこと</h2>
<ul>
<li><b>円の数を1にする</b>：どの絵も、ただの円になります。2、3、4…と1つずつ増やして、形がどこで「それらしく」なるかを見てみましょう。</li>
<li><b>ハートと四角をくらべる</b>：なめらかなハートは、少ない円でも元の絵に近づきます。角のある四角や星は、円を増やしても角のまわりが少し波うちます。角を作るには、小さくて速い円がたくさん必要だからです。</li>
<li><b>「円を表示」を切る</b>：線だけを見ると、円の数による形のちがいが分かりやすくなります。</li>
<li><b>自分の名前の1文字を一筆書きで描く</b>：行って帰ってくる線になるので、同じところを2回なぞる動きになります。</li>
<li><b>回る速さを変える</b>：速さを変えても、描かれる形は変わりません。変わるのは1周にかかる時間だけです。</li>
</ul>

<h2>本物では</h2>
<p>この考え方のもとを作ったのは、19世紀はじめのフランスの数学者ジョゼフ・フーリエです。フーリエは熱の伝わり方を研究するなかで、「複雑な形の波も、単純な波（サインとコサイン）をたくさん足し合わせて表せる」という考えを使い、1822年に本にまとめました。回る円の先の点の動きは、サインとコサインの波を組にしたものなので、円をつなぐことは波を足し合わせることと同じです。</p>
<p>いまでは、音を高さごとの成分に分けて調べたり、音楽（MP3など）や写真（JPEGなど）のデータを小さくしたりする技術に、同じ考え方のなかまの計算が使われています。「円の数を減らしても絵のおおまかな形は残る」という性質は、データを小さくするときの考え方とよく似ています。</p>
<p>なお、実際の機器では「高速フーリエ変換（FFT）」という速い計算方法がよく使われます。このシミュレーターは点が200個と少ないので、定義どおりの単純な計算をしています。また、ここであつかっているのは1本につながった線だけで、写真のような面の画像をあつかう方法とはやり方がちがいます。</p>
"""

REFS = [
    "J. フーリエ (1822)『熱の解析的理論』（Fourier, J. Théorie analytique de la chaleur. Paris: Firmin Didot）",
    "Cooley, J. W. & Tukey, J. W. (1965) An algorithm for the machine calculation of complex Fourier series. Mathematics of Computation 19, 297–301.（高速フーリエ変換）",
    "ITU-T Recommendation T.81 (1992) Digital compression and coding of continuous-tone still images.（JPEGの規格）",
]

STAGE = r"""
<style>
.fe-seg{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.fe-seg button{border:1.5px solid var(--line);background:#fff;border-radius:999px;padding:8px 13px;font:inherit;font-size:13.5px;font-weight:800;cursor:pointer;color:var(--ink)}
.fe-seg button.on{background:#4338ca;border-color:#4338ca;color:#fff}
#feWrap{position:relative;border-radius:14px;overflow:hidden;border:1px solid var(--line);background:#0b1020;margin-top:12px}
#feCv{display:block;width:100%;aspect-ratio:3/2;touch-action:none;cursor:crosshair}
.fe-hint{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);color:#e2e8f0;font-size:15px;font-weight:800;text-align:center;pointer-events:none;width:86%;display:none;line-height:1.7}
.fe-hint.show{display:block}
.fe-msg{position:absolute;left:50%;bottom:10px;transform:translateX(-50%);background:rgba(255,255,255,.92);color:#0f172a;font-size:12.5px;font-weight:700;border-radius:12px;padding:6px 14px;max-width:92%;text-align:center;pointer-events:none;opacity:0;transition:opacity .3s}
.fe-msg.show{opacity:1}
.fe-tip{font-size:12.5px;color:var(--ink-2);margin:8px 0 0}
.fe-sum{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:12px}
.fe-sum div{background:#eef2ff;border-radius:12px;padding:10px 4px;text-align:center}
.fe-sum b{display:block;font-size:20px;color:#4338ca;font-variant-numeric:tabular-nums}
.fe-sum b small{font-size:11.5px}
.fe-sum span{font-size:11.5px;color:var(--ink-2);font-weight:700}
.fe-cols{display:grid;grid-template-columns:1fr 1fr;gap:6px 22px;margin-top:14px}
.fe-chk{display:flex;flex-wrap:wrap;gap:8px 18px;align-items:center;margin-top:8px}
.fe-chk label{display:inline-flex;align-items:center;gap:6px;font-size:14px;font-weight:700;cursor:pointer}
.fe-chk input{width:18px;height:18px}
@media (max-width:640px){#feCv{aspect-ratio:1/1}.fe-sum{grid-template-columns:repeat(2,1fr)}.fe-cols{grid-template-columns:1fr}}
</style>
"""

BODY = r"""
  <section class="panel" id="resultPanel">
    <h2 style="margin:0 0 8px;font-size:18px;">① 絵をえらぶ・自分で描く</h2>
    <div class="fe-seg" id="fePre"></div>

    <div id="feWrap">
      <canvas id="feCv" aria-label="回る円をつないだ腕が絵を描いていくアニメーション"></canvas>
      <div class="fe-hint" id="feHint">✏️ ここを指やマウスでなぞって、<br>一筆書きで描いてください</div>
      <div class="fe-msg" id="feMsg"></div>
    </div>
    <p class="fe-tip">黒い画面をなぞると、いつでも自分の線を描けます（描き終わると自動で再生）。うすい点線が元の絵、光る線が円で描いた絵です。</p>

    <div class="fe-sum">
      <div><b id="mN">0</b><span>使っている円の数</span></div>
      <div><b id="mR">0</b><span>いちばん大きい円の半径</span></div>
      <div><b id="mE">0</b><span>元の絵とのずれ（平均）</span></div>
      <div><b id="mT">0</b><span>1周にかかる時間</span></div>
    </div>
    <p class="fe-tip">半径とずれは、絵のはば（たてと横の大きいほう）を100としたときの数字です。</p>

    <h2 style="margin:18px 0 0;font-size:18px;">② 円の数と速さ</h2>
    <div class="fe-cols">
      <div class="field"><label>🌀 使う円の数 <span class="hint">（<b id="vN"></b>）</span></label><input type="range" id="kN" min="1" max="199" step="1" value="40"></div>
      <div class="field"><label>⏱ 回る速さ <span class="hint">（<b id="vS"></b>）</span></label><input type="range" id="kS" min="0.25" max="4" step="0.25" value="1"></div>
    </div>
    <div class="fe-chk">
      <label><input type="checkbox" id="cCircle" checked> 円を表示</label>
      <label><input type="checkbox" id="cOrig" checked> 元の絵を表示</label>
      <button class="btn btn-ghost" id="feAll" type="button" style="width:auto;padding:9px 14px;">円を全部使う</button>
      <button class="btn btn-ghost" id="feRestart" type="button" style="width:auto;padding:9px 14px;">↺ やり直し</button>
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
  const cv = $('feCv'), ctx = cv.getContext('2d');
  const N = 200, K = 600, TAU = Math.PI * 2, BASE_T = 12;

  // ---------- 見本の線（一筆書き） ----------
  function chaikin(p, it) {
    for (let k = 0; k < it; k++) {
      const q = [p[0]];
      for (let i = 0; i < p.length - 1; i++) { const a = p[i], b = p[i + 1]; q.push([a[0] * .75 + b[0] * .25, a[1] * .75 + b[1] * .25], [a[0] * .25 + b[0] * .75, a[1] * .25 + b[1] * .75]); }
      q.push(p[p.length - 1]); p = q;
    }
    return p;
  }
  const PRESETS = [
    ['♥ ハート', 'ハート', () => { const p = []; for (let i = 0; i < 160; i++) { const t = i / 160 * TAU, s = Math.sin(t); p.push([16 * s * s * s, -(13 * Math.cos(t) - 5 * Math.cos(2 * t) - 2 * Math.cos(3 * t) - Math.cos(4 * t))]); } return [p, true]; }],
    ['★ 星', '星', () => { const p = []; for (let i = 0; i < 10; i++) { const a = -Math.PI / 2 + i * Math.PI / 5, r = i % 2 ? .42 : 1; p.push([Math.cos(a) * r, Math.sin(a) * r]); } return [p, true]; }],
    ['♪ 音符', '音符', () => {
      const p = [], cx = -.2, cy = .58, rx = .3, ry = .2, rot = -.35;
      for (let i = 0; i <= 40; i++) { const a = i / 40 * TAU, x = Math.cos(a) * rx, y = Math.sin(a) * ry; p.push([cx + x * Math.cos(rot) - y * Math.sin(rot), cy + x * Math.sin(rot) + y * Math.cos(rot)]); }
      const sx = p[0][0], sy = p[0][1];
      const flag = chaikin([[sx, -.9], [sx + .1, -.62], [sx + .42, -.45], [sx + .46, -.08], [sx + .36, -.3], [sx + .16, -.46], [sx, -.52]], 2);
      return [p.concat(flag, [[sx, sy]]), true];
    }],
    ['あ', '「あ」', () => [chaikin([[-.55, -.5], [-.1, -.52], [.45, -.58], [.2, -.7], [-.08, -.88], [-.1, -.3], [-.08, .3], [-.02, .62], [.1, .3], [.3, -.12], [.05, .25], [-.3, .55], [-.55, .42], [-.5, .1], [-.1, -.14], [.35, -.1], [.62, .2], [.5, .58], [.15, .8]], 3), false]],
    ['■ 四角', '四角', () => [[[-1, -1], [1, -1], [1, 1], [-1, 1]], true]],
  ];

  // ---------- 線 → 同じ間かくのN点 ----------
  function resample(loop) {
    const n = loop.length, len = [0]; let L = 0;
    for (let i = 0; i < n; i++) { const a = loop[i], b = loop[(i + 1) % n]; L += Math.hypot(b[0] - a[0], b[1] - a[1]); len.push(L); }
    const out = []; let j = 0;
    for (let i = 0; i < N; i++) {
      const d = i * L / N; while (j < n - 1 && len[j + 1] < d) j++;
      const a = loop[j], b = loop[(j + 1) % n], sl = len[j + 1] - len[j], u = sl > 1e-9 ? (d - len[j]) / sl : 0;
      out.push([a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u]);
    }
    return out;
  }
  function normalize(p) {
    let x0 = 1e9, x1 = -1e9, y0 = 1e9, y1 = -1e9;
    p.forEach(q => { x0 = Math.min(x0, q[0]); x1 = Math.max(x1, q[0]); y0 = Math.min(y0, q[1]); y1 = Math.max(y1, q[1]); });
    const s = 2 / Math.max(x1 - x0, y1 - y0, 1e-6), mx = (x0 + x1) / 2, my = (y0 + y1) / 2;
    return p.map(q => [(q[0] - mx) * s, (q[1] - my) * s]);
  }

  // ---------- 離散フーリエ変換（複素数 x+iy） ----------
  function dft(P) {
    const out = [];
    for (let k = 0; k < N; k++) {
      let re = 0, im = 0;
      for (let n = 0; n < N; n++) { const a = -TAU * k * n / N, c = Math.cos(a), s = Math.sin(a); re += P[n][0] * c - P[n][1] * s; im += P[n][0] * s + P[n][1] * c; }
      re /= N; im /= N;
      out.push({ f: k <= N / 2 ? k : k - N, re, im, amp: Math.hypot(re, im), ph: Math.atan2(im, re) });
    }
    return out;
  }

  // ---------- 状態 ----------
  let P = [], dc = { re: 0, im: 0 }, terms = [], M = 40, speed = 1, t = 0, laps = 0, mode = 'play';
  let curve = new Float32Array(K * 2), err = 0, name = 'ハート', preset = 0, showC = true, showO = true, raw = [], saved = null;

  function setPath(pts, closed, nm) {
    const loop = closed ? pts : pts.concat(pts.slice(1, -1).reverse());
    P = resample(normalize(loop));
    const F = dft(P); dc = F[0]; terms = F.slice(1).sort((a, b) => b.amp - a.amp);
    name = nm; rebuild(); t = 0; laps = 0; mode = 'play'; $('feHint').classList.remove('show'); lastUI = 0;
  }
  function posAt(tt, m) { let x = dc.re, y = dc.im; for (let i = 0; i < m; i++) { const q = terms[i], a = TAU * q.f * tt + q.ph; x += q.amp * Math.cos(a); y += q.amp * Math.sin(a); } return [x, y]; }
  function rebuild() {
    for (let j = 0; j < K; j++) { const p = posAt(j / K, M); curve[j * 2] = p[0]; curve[j * 2 + 1] = p[1]; }
    let s = 0; const st = K / N;
    for (let n = 0; n < N; n++) s += Math.hypot(curve[n * st * 2] - P[n][0], curve[n * st * 2 + 1] - P[n][1]);
    err = s / N; lastUI = 0;
  }
  function advance(dt) { if (mode !== 'play') return; t += dt * speed / BASE_T; while (t >= 1) { t -= 1; laps++; } }

  // ---------- 描く ----------
  let dpr = 1, W = 0, Hh = 0, S = 1;
  function size() {
    const w = cv.clientWidth || 600, h = cv.clientHeight || 400; dpr = Math.min(2, window.devicePixelRatio || 1);
    const w2 = Math.round(w * dpr), h2 = Math.round(h * dpr); if (cv.width !== w2 || cv.height !== h2) { cv.width = w2; cv.height = h2; }
    W = cv.width; Hh = cv.height; S = Math.min(W, Hh) * .33;
  }
  function draw() {
    size();
    const c = ctx, cx = W / 2, cy = Hh / 2, X = x => cx + x * S, Y = y => cy + y * S;
    c.setTransform(1, 0, 0, 1, 0, 0);
    const bg = c.createRadialGradient(cx, cy, 0, cx, cy, Math.max(W, Hh) * .7); bg.addColorStop(0, '#172046'); bg.addColorStop(1, '#070a18');
    c.fillStyle = bg; c.fillRect(0, 0, W, Hh);
    c.lineCap = 'round'; c.lineJoin = 'round';
    if (mode === 'drawing') {
      if (raw.length > 1) {
        const path = () => { c.beginPath(); raw.forEach((q, i) => i ? c.lineTo(q[0] * dpr, q[1] * dpr) : c.moveTo(q[0] * dpr, q[1] * dpr)); c.stroke(); };
        c.strokeStyle = 'rgba(125,211,252,.25)'; c.lineWidth = 10 * dpr; path();
        c.strokeStyle = '#f8fafc'; c.lineWidth = 2.6 * dpr; path();
      }
      ui(); return;
    }
    if (mode !== 'play') { ui(); return; }
    // 元の絵（うすい点線）
    if (showO) {
      c.strokeStyle = 'rgba(203,213,225,.38)'; c.lineWidth = 1.3 * dpr; c.setLineDash([4 * dpr, 5 * dpr]);
      c.beginPath(); P.forEach((q, i) => i ? c.lineTo(X(q[0]), Y(q[1])) : c.moveTo(X(q[0]), Y(q[1]))); c.closePath(); c.stroke(); c.setLineDash([]);
    }
    // 腕の先の位置と円
    const tip = [dc.re, dc.im], joints = [[dc.re, dc.im]];
    for (let i = 0; i < M; i++) { const q = terms[i], a = TAU * q.f * t + q.ph; tip[0] += q.amp * Math.cos(a); tip[1] += q.amp * Math.sin(a); joints.push([tip[0], tip[1]]); }
    // 描かれた線（光る線）
    const end = laps > 0 ? K : Math.floor(t * K), cur = Math.floor(t * K);
    const seg = (a, b, close) => { c.beginPath(); for (let j = a; j <= b; j++) { const jj = ((j % K) + K) % K, x = X(curve[jj * 2]), y = Y(curve[jj * 2 + 1]); j === a ? c.moveTo(x, y) : c.lineTo(x, y); } if (close) c.lineTo(X(tip[0]), Y(tip[1])); c.stroke(); };
    if (end > 0 || laps > 0) {
      c.strokeStyle = 'rgba(56,189,248,.16)'; c.lineWidth = 11 * dpr; seg(0, laps > 0 ? K : end, laps === 0);
      c.strokeStyle = 'rgba(165,180,252,.22)'; c.lineWidth = 5.5 * dpr; seg(0, laps > 0 ? K : end, laps === 0);
      c.lineWidth = 2.4 * dpr; c.globalAlpha = laps > 0 ? .78 : 1;
      const last = laps > 0 ? K : end;
      for (let a = 0; a < last; a += 10) { c.strokeStyle = `hsl(${185 + 150 * a / K},95%,70%)`; seg(a, Math.min(a + 10, last), laps === 0 && a + 10 >= last); }
      c.globalAlpha = 1;
      // 先っぽの明るい尾
      const tail = Math.min(laps > 0 ? Math.round(K * .22) : cur, Math.round(K * .22));
      for (let k = 0; k < 6; k++) {
        const a = cur - Math.round(tail * (1 - k / 6)); if (a >= cur) continue;
        c.strokeStyle = `rgba(255,255,255,${.1 + k * .09})`; c.lineWidth = (2.2 + k * .35) * dpr; seg(a, cur, true);
      }
    }
    if (showC) {
      for (let i = 0; i < M; i++) {
        const r = terms[i].amp * S; if (r < .7 * dpr) continue;
        c.strokeStyle = `hsla(${(205 + i * 23) % 360},90%,${i < 12 ? 70 : 62}%,${i < 12 ? .55 : .3})`; c.lineWidth = (i < 4 ? 1.6 : 1) * dpr;
        c.beginPath(); c.arc(X(joints[i][0]), Y(joints[i][1]), r, 0, TAU); c.stroke();
      }
    }
    // 腕
    c.strokeStyle = showC ? 'rgba(255,255,255,.85)' : 'rgba(255,255,255,.35)'; c.lineWidth = 1.5 * dpr;
    c.beginPath(); joints.forEach((q, i) => i ? c.lineTo(X(q[0]), Y(q[1])) : c.moveTo(X(q[0]), Y(q[1]))); c.stroke();
    if (showC) { c.fillStyle = '#fde68a'; for (let i = 0; i < Math.min(M, 10); i++) { c.beginPath(); c.arc(X(joints[i][0]), Y(joints[i][1]), 2.2 * dpr, 0, TAU); c.fill(); } }
    // 先の点
    c.save(); c.shadowColor = '#fff7ae'; c.shadowBlur = 18 * dpr; c.fillStyle = '#fffbe6';
    c.beginPath(); c.arc(X(tip[0]), Y(tip[1]), 4.2 * dpr, 0, TAU); c.fill(); c.restore();
    ui();
  }

  // ---------- 数字 ----------
  let lastUI = 0;
  const u100 = v => v / 2 * 100;
  function ui() {
    const now = performance.now(); if (now - lastUI < 160) return; lastUI = now;
    const per = BASE_T / speed, e = u100(err);
    $('mN').innerHTML = M + '<small>こ／' + (N - 1) + '</small>';
    $('mR').innerHTML = (terms.length ? u100(terms[0].amp) : 0).toFixed(1);
    $('mE').innerHTML = e < .005 ? '0.00' : e.toFixed(2);
    $('mT').innerHTML = per.toFixed(1) + '<small>秒</small>';
    $('vN').textContent = M + 'こ' + (M === N - 1 ? '・全部' : '');
    $('vS').textContent = '×' + speed.toFixed(2).replace(/0$/, '').replace(/\.0$/, '');
  }

  // ---------- 操作 ----------
  function flash(s) { const el = $('feMsg'); el.textContent = s; el.classList.add('show'); clearTimeout(flash.t); flash.t = setTimeout(() => el.classList.remove('show'), 2400); }
  function markPreset() { document.querySelectorAll('#fePre button').forEach(b => b.classList.toggle('on', b.dataset.i === String(preset))); }
  function loadPreset(i) { preset = i; const [pts, closed] = PRESETS[i][2](); setPath(pts, closed, PRESETS[i][1]); markPreset(); }
  $('fePre').innerHTML = PRESETS.map((p, i) => `<button type="button" data-i="${i}">${p[0]}</button>`).join('') + '<button type="button" data-i="d">✏️ 自分で描く</button>';
  $('fePre').addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    if (b.dataset.i === 'd') { preset = 'd'; mode = 'wait'; raw = []; $('feHint').classList.add('show'); markPreset(); $('feWrap').scrollIntoView({ behavior: 'smooth', block: 'center' }); return; }
    loadPreset(+b.dataset.i);
  });
  $('kN').addEventListener('input', e => { M = Math.max(1, Math.min(N - 1, +e.target.value)); rebuild(); });
  $('kS').addEventListener('input', e => { speed = +e.target.value; lastUI = 0; });
  $('cCircle').addEventListener('change', e => { showC = e.target.checked; });
  $('cOrig').addEventListener('change', e => { showO = e.target.checked; });
  $('feAll').addEventListener('click', () => { M = N - 1; $('kN').value = M; rebuild(); flash('円を全部（' + M + 'こ）使います'); });
  $('feRestart').addEventListener('click', () => { if (mode !== 'play') { loadPreset(0); return; } t = 0; laps = 0; flash('はじめから描きなおします'); });

  // 自分で描く（マウス・タッチ共通）
  const pt = e => { const r = cv.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top]; };
  let pid = null;
  cv.addEventListener('pointerdown', e => {
    if (pid !== null) return; pid = e.pointerId; try { cv.setPointerCapture(pid); } catch (er) {}
    saved = mode; mode = 'drawing'; raw = [pt(e)]; $('feHint').classList.remove('show'); e.preventDefault();
  });
  cv.addEventListener('pointermove', e => {
    if (e.pointerId !== pid) return; const p = pt(e), q = raw[raw.length - 1];
    if (Math.hypot(p[0] - q[0], p[1] - q[1]) >= 2) raw.push(p); e.preventDefault();
  });
  function finish(e) {
    if (e.pointerId !== pid) return; pid = null;
    let L = 0; for (let i = 1; i < raw.length; i++) L += Math.hypot(raw[i][0] - raw[i - 1][0], raw[i][1] - raw[i - 1][1]);
    if (raw.length < 8 || L < 60) { mode = saved === 'drawing' ? 'play' : saved; if (mode === 'wait') $('feHint').classList.add('show'); raw = []; flash('もう少し長く、一筆書きで描いてみてください'); return; }
    let x0 = 1e9, x1 = -1e9, y0 = 1e9, y1 = -1e9; raw.forEach(q => { x0 = Math.min(x0, q[0]); x1 = Math.max(x1, q[0]); y0 = Math.min(y0, q[1]); y1 = Math.max(y1, q[1]); });
    const a = raw[0], b = raw[raw.length - 1], closed = Math.hypot(a[0] - b[0], a[1] - b[1]) < .15 * Math.max(x1 - x0, y1 - y0);
    preset = 'd'; markPreset(); setPath(raw.slice(), closed, '自分で描いた絵'); raw = [];
    flash(closed ? '線を' + (N - 1) + 'この円に分けました' : '線を円に分けました（行って帰る動きになります）');
  }
  cv.addEventListener('pointerup', finish); cv.addEventListener('pointercancel', finish);

  // ---------- シェア ----------
  function shareText() { return `回る円${M}こをつないで「${name}」を描きました。元の絵とのずれは${u100(err).toFixed(2)}（絵のはば＝100）🌀`; }
  $('shareBtn').addEventListener('click', () => { const u = location.origin + location.pathname; window.open('https://twitter.com/intent/tweet?text=' + encodeURIComponent(shareText() + '\n') + '&url=' + encodeURIComponent(u) + '&hashtags=' + encodeURIComponent('シミュラボ'), '_blank', 'noopener'); });
  $('copyBtn').addEventListener('click', async () => { try { await navigator.clipboard.writeText(shareText() + '\n' + location.origin + location.pathname); flash('コピーしました'); } catch (e) { flash('コピーできませんでした'); } });

  // ---------- 動かす ----------
  let tPrev = performance.now();
  function loop(now) { const dt = Math.min(.1, (now - tPrev) / 1000); tPrev = now; advance(dt); draw(); requestAnimationFrame(loop); }
  M = +$('kN').value; speed = +$('kS').value; loadPreset(0);
  requestAnimationFrame(loop);
  window.__t = {
    step(sec) { const n = Math.round(sec * 60); for (let i = 0; i < n; i++) advance(1 / 60); lastUI = 0; draw(); },
    get s() {
      const p = posAt(t, M); let nan = !isFinite(err) || !isFinite(p[0]) || !isFinite(p[1]) || !isFinite(t);
      for (let j = 0; j < K * 2; j++) if (!isFinite(curve[j])) { nan = true; break; }
      return { circles: M, total: N - 1, err: +u100(err).toFixed(4), maxR: +(terms.length ? u100(terms[0].amp) : 0).toFixed(3), t: +t.toFixed(4), laps, period: BASE_T / speed, speed, mode, name, tip: [+p[0].toFixed(3), +p[1].toFixed(3)], nan };
    },
    setN(n) { M = Math.max(1, Math.min(N - 1, n | 0)); $('kN').value = M; rebuild(); },
    setSpeed(v) { speed = v; $('kS').value = v; lastUI = 0; },
    preset(i) { loadPreset(i); },
    drawPath(pts) { preset = 'd'; markPreset(); const a = pts[0], b = pts[pts.length - 1]; setPath(pts, Math.hypot(a[0] - b[0], a[1] - b[1]) < 10, '自分で描いた絵'); },
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
