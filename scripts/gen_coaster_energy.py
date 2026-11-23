# -*- coding: utf-8 -*-
"""ジェットコースターで学ぶエネルギー（2026-11-24・中学3年「力学的エネルギーの保存」）
   sims/coaster-energy/index.html を書き出す（冪等）。 使い方: python -X utf8 scripts/gen_coaster_energy.py"""
import html as H, io, json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://shimulabo.com"
SLUG = "coaster-energy"
NAME = "ジェットコースターで学ぶエネルギー"
CAT = "あそぶ・実験"
TITLE = "ジェットコースターで学ぶエネルギー｜力学的エネルギーの保存シミュレーター（位置エネルギー・運動エネルギー・まさつ）｜シミュラボ"
DESC = ("線路の点を動かしたり、指でなぞって線路を描いたりして、ジェットコースターを走らせるシミュレーター。"
        "位置エネルギー・運動エネルギー・まさつで熱になったエネルギーを、棒グラフと時間のグラフでリアルタイムに表示。"
        "まさつ0ならスタートと同じ高さまで上がれることや、スタートより高い山は越えられないことを体験できます（中学3年 理科）。")
OG_T = "ジェットコースターで学ぶエネルギー（力学的エネルギーの保存）"
OG_D = "線路の形を自由に変えて車両を走らせよう。位置エネルギーと運動エネルギーが入れかわるようすが、グラフでわかる。"
H1 = "ジェットコースターで学ぶエネルギー<br>力学的エネルギーの保存シミュレーター"
LEAD = ("線路の上の白い点を動かして、山や谷の形を変えてみましょう。車両が下ると速くなり、上るとおそくなります。"
        "このとき「位置エネルギー」と「運動エネルギー」が入れかわっていて、まさつがなければ、その合計はずっと同じです。")

FAQ = [
    ("どうやって遊びますか？", "最初から車両が走っています。線路の上の白い点をドラッグ（スマホでは指でおさえて動かす）すると、山や谷の形が変わります。「✏️ なぞって描く」をえらぶと、指やマウスでなぞった形がそのまま線路になります。「まさつ」と「スタートの高さ」のスライダー、プリセット（山2つ・宙返り・なだらか）も試してみてください。"),
    ("力学的エネルギーの保存とは何ですか？", "高いところにある物体がもつ「位置エネルギー」と、動いている物体がもつ「運動エネルギー」の合計を「力学的エネルギー」といいます。まさつや空気の抵抗がなければ、この合計は変わりません。これを力学的エネルギーの保存といいます。下り坂では位置エネルギーが運動エネルギーに変わり、上り坂ではその逆が起こります。"),
    ("どうして、スタートより高い山は越えられないのですか？", "車両はスタートしたときの位置エネルギーしかもっていません。途中でエネルギーが増えることはないので、スタートより高い場所まで上るにはエネルギーが足りません。画面の点線は「いまのエネルギーで上がれる高さ」を表していて、車両はこの線より上には行けません。"),
    ("まさつを大きくすると、エネルギーはなくなるのですか？", "なくなるのではなく、熱などの別のエネルギーに変わります。グラフのオレンジ色が、まさつで熱に変わった分です。位置エネルギー・運動エネルギー・熱の3つを合わせた合計は変わりません。ただし、熱になった分は車両を動かすのには使えないので、上がれる高さはだんだん低くなります。"),
    ("「体にかかる力（G）」とは何ですか？", "座席が体をおす力が、止まっているときの何倍かを表した数です。平らな場所で止まっていると1Gです。谷の底を速く通るときは1Gより大きくなり（体が重く感じる）、山のてっぺんを通るときは1Gより小さくなります（体がうく感じ）。このシミュレーターでは、線路に垂直な向きの力だけを計算しています。マイナスの数は、座席から体がはなれる向きの力を表します。"),
]
REL = [("furiko-jikken", "🪀", "ふりこの実験"), ("newtons-cradle", "⚪", "ニュートンのゆりかご"), ("double-pendulum", "🌀", "二重ふりこ")]

ARTICLE = """
<h2>このシミュレーターのしくみ</h2>
<p>車両は、モーターなどで自分から進む力をもっていません。高いところからスタートし、重力だけで走ります。このシミュレーターでは、次の3つのエネルギーを計算しています。</p>
<ul>
<li><b>位置エネルギー（青）</b>：高いところにあるほど大きいエネルギーです。「質量 × 重力加速度 × 高さ」で求めます。</li>
<li><b>運動エネルギー（赤）</b>：速く動いているほど大きいエネルギーです。「1/2 × 質量 × 速さ × 速さ」で求めます。</li>
<li><b>熱になったエネルギー（オレンジ）</b>：まさつによって、熱などに変わった分です。</li>
</ul>
<p>まさつが0のとき、位置エネルギーと運動エネルギーの合計（力学的エネルギー）は一定に保たれます。これが「力学的エネルギーの保存」です。中学校ではエネルギーが入れかわることを学び、上の2つの式は高校の物理でくわしく学びます。</p>
<p>計算を簡単にするため、次のように単純化しています。</p>
<ul>
<li>3両の車両を、まん中の1つの点（質量500kg）とみなしています。車両の長さや、車輪の回転は考えていません。</li>
<li>車両は線路からはなれないものとしています（宙返りの途中でエネルギーが足りなくなっても、落ちずに線路にそって戻ります）。</li>
<li>まさつの力は、線路が車両をおす力に比例するものとしています。空気の抵抗は、べつには計算していません。</li>
<li>線路の両はしには、はね返るストッパーがあるものとしています。</li>
<li>画面におさめるため、本物よりずっと短いコースにしています。谷や山の曲がり方が本物より急なので、「体にかかる力（G）」は本物のジェットコースターより大きな数字になることがあります。</li>
</ul>

<h2>ためしてみたいこと</h2>
<ul>
<li><b>まさつを0にする</b>：反対側の坂で、スタートと同じ高さ（点線の高さ）まで上がって戻ってきます。合計のグラフは、ずっと同じ高さのままです。</li>
<li><b>スタートの高さを20mにする（プリセット「山2つ」）</b>：1つ目の山（約25m）を越えられずに、戻ってきます。</li>
<li><b>山の点をドラッグして、点線より高くする</b>：その山は越えられなくなります。点線より少しでも低ければ、ゆっくりですが越えられます。</li>
<li><b>まさつを大きくする</b>：オレンジ色（熱）が少しずつ増え、点線が下がっていきます。最後は谷の底で止まります。</li>
<li><b>プリセット「宙返り」で、スタートの高さを下げていく</b>：輪のてっぺんより低いところからスタートすると、輪を回りきれません。</li>
<li><b>谷の底と山のてっぺんで、Gの数字をくらべる</b>：速さが同じでも、線路の曲がり方で体にかかる力が変わります。</li>
<li><b>「✏️ なぞって描く」で、自分だけのコースを作る</b>：最後まで走りきれるコースを考えてみましょう。</li>
</ul>

<h2>本物では</h2>
<p>本物のジェットコースターの多くも、走っているあいだは車両に動力がありません。最初にチェーンなどで高いところまで引き上げ、そのときにたくわえた位置エネルギーを使って最後まで走ります（スタートのときに機械で一気に加速させる方式のものもあります）。</p>
<p>本物ではまさつや空気の抵抗があるため、力学的エネルギーは少しずつ熱などに変わっていきます。そのため、引き上げたあとの山は、あとになるほど低く作られているのがふつうです。</p>
<p>宙返りの輪は、本物ではまん丸ではなく、上がせまく下が広い、しずくのような形に作られています。まん丸にすると、輪の入り口で体にかかる力がとても大きくなってしまうためです。また、車両には線路を上下からはさむ車輪がついていて、さかさまになっても線路からはなれないようになっています。</p>
<p>このシミュレーターは、エネルギーの移り変わりをつかむために単純にしたものです。実際のコースの設計では、車両の長さ、空気の抵抗、乗る人の体への負担などを細かく計算しています。</p>
"""

REFS = [
    "文部科学省「中学校学習指導要領（平成29年告示）解説 理科編」（運動とエネルギー：力学的エネルギーの保存）",
    "文部科学省「高等学校学習指導要領（平成30年告示）解説 理科編 理数編」（物理基礎：運動エネルギーと位置エネルギー、力学的エネルギーの保存）",
    "Halliday, D., Resnick, R. & Walker, J. Fundamentals of Physics. Wiley.（力学的エネルギーの保存、円運動）",
]

STAGE = r"""
<style>
.ce-tools{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;margin-bottom:10px}
.ce-seg{display:flex;flex-wrap:wrap;gap:6px}
.ce-seg button{border:1.5px solid var(--line);background:#fff;border-radius:999px;padding:8px 13px;font:inherit;font-size:13.5px;font-weight:800;cursor:pointer;color:var(--ink)}
.ce-seg button.on{background:#2563eb;border-color:#2563eb;color:#fff}
#ceWrap{position:relative;border-radius:14px;overflow:hidden;border:1px solid var(--line);background:#e0f2fe}
#ce{display:block;width:100%;aspect-ratio:8/5;touch-action:none;cursor:grab;-webkit-user-select:none;user-select:none}
.ce-play{position:absolute;left:50%;top:8px;transform:translateX(-50%);display:flex;gap:6px;white-space:nowrap}
.ce-play button{border:0;border-radius:999px;background:rgba(15,23,42,.8);color:#fff;font:inherit;font-weight:800;font-size:12.5px;padding:7px 12px;cursor:pointer}
.ce-play button.on{background:#f59e0b;color:#111}
.ce-msg{position:absolute;left:50%;bottom:8px;transform:translateX(-50%);background:rgba(15,23,42,.85);color:#fff;font-size:12.5px;font-weight:700;border-radius:12px;padding:6px 14px;max-width:92%;text-align:center;pointer-events:none;opacity:0;transition:opacity .3s}
.ce-msg.show{opacity:1}
.ce-sum{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-top:12px}
.ce-sum div{background:#eff6ff;border-radius:12px;padding:10px 4px;text-align:center;min-width:0}
.ce-sum b{display:block;font-size:20px;color:#1d4ed8;font-variant-numeric:tabular-nums}
.ce-sum b small{font-size:11.5px}
.ce-sum span{font-size:11.5px;color:var(--ink-2);font-weight:700}
.ce-note{font-size:13.5px;color:var(--ink);background:#eff6ff;border-radius:10px;padding:9px 12px;margin:10px 0 0;font-weight:700}
#ceG{display:block;width:100%;height:150px;margin-top:12px}
.ce-legend{font-size:12.5px;color:var(--ink-2);display:flex;flex-wrap:wrap;gap:4px 14px;margin-top:4px}
.ce-legend i{display:inline-block;width:12px;height:12px;border-radius:3px;vertical-align:-1px;margin-right:4px}
.ce-legend b{font-variant-numeric:tabular-nums;color:var(--ink)}
.ce-legend i.d{width:18px;height:0;border-top:2px dashed #475569;border-radius:0;vertical-align:3px}
.ce-cols{display:grid;grid-template-columns:1fr 1fr;gap:6px 22px;margin-top:14px}
.ce-hint{font-size:13px;color:var(--ink-2);margin:8px 0 0}
@media (max-width:640px){.ce-sum{grid-template-columns:repeat(3,1fr)}.ce-cols{grid-template-columns:1fr}.ce-play button{padding:6px 10px;font-size:12px}.ce-seg button{padding:7px 11px;font-size:13px}}
</style>
"""

BODY = r"""
  <section class="panel" id="resultPanel">
    <div class="ce-tools">
      <div class="ce-seg" id="cePre"><button type="button" data-p="hills" class="on">⛰ 山2つ</button><button type="button" data-p="loop">🔄 宙返り</button><button type="button" data-p="gentle">〰 なだらか</button></div>
      <div class="ce-seg" id="ceMode"><button type="button" data-m="drag" class="on">✋ 点を動かす</button><button type="button" data-m="draw">✏️ なぞって描く</button></div>
    </div>
    <div id="ceWrap">
      <canvas id="ce" aria-label="ジェットコースターの線路と、その上を走る車両の絵"></canvas>
      <div class="ce-play"><button type="button" id="cePlay">⏸ 止める</button><button type="button" id="ceReset">↺ リセット</button><button type="button" id="ceSlow">🐢 スロー</button></div>
      <div class="ce-msg" id="ceMsg"></div>
    </div>
    <div class="ce-sum">
      <div><b id="ceV">0</b><span>速さ</span></div>
      <div><b id="ceH">0</b><span>高さ</span></div>
      <div><b id="ceGf">1.0</b><span>体にかかる力</span></div>
      <div><b id="ceMax">0</b><span>最高の速さ</span></div>
      <div><b id="ceHeat">0</b><span>熱になった割合</span></div>
    </div>
    <p class="ce-note" id="ceNote">🎢 スタートしました。</p>

    <canvas id="ceG" aria-label="位置エネルギー・運動エネルギー・熱の棒グラフと、時間による変化のグラフ"></canvas>
    <div class="ce-legend">
      <span><i style="background:#2563eb"></i>位置エネルギー <b id="cePE">0</b>kJ</span>
      <span><i style="background:#ef4444"></i>運動エネルギー <b id="ceKE">0</b>kJ</span>
      <span><i style="background:#f59e0b"></i>まさつで熱になった分 <b id="ceQ">0</b>kJ</span>
      <span>合計 <b id="ceTot">0</b>kJ</span>
      <span><i class="d"></i>点線＝いまのエネルギーで上がれる高さ／はじめの合計</span>
    </div>

    <div class="ce-cols">
      <div class="field"><label>まさつの大きさ <span class="hint">（<b id="ceMuV"></b>）</span></label><input type="range" id="ceMu" min="0" max="10" step="1" value="0"></div>
      <div class="field"><label>スタートの高さ <span class="hint">（<b id="ceH0V"></b>）</span></label><input type="range" id="ceH0" min="8" max="40" step="1" value="30"></div>
    </div>
    <p class="ce-hint">線路の白い点は、上下左右に動かせます。スタート地点は、最初の下り坂の上で「スタートの高さ」になる場所です（旗のところ）。</p>

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
  const cv = $('ce'), ctx = cv.getContext('2d'), gc = $('ceG'), gx = gc.getContext('2d');
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const g = 9.8, M = 500;
  const PRE = {
    hills: [[2, 44], [13, 22], [23, 6], [33, 5], [43, 20], [50, 25], [57, 21], [65, 9], [73, 5], [81, 9], [87, 17], [91, 21], [95, 31], [98, 44]],
    loop: [[2, 44], [13, 22], [25, 7], [40, 3], [54, 7], [58, 16], [50, 24], [42, 16], [46, 7], [60, 3], [73, 5], [85, 15], [92, 27], [98, 44]],
    gentle: [[2, 44], [12, 30], [26, 16], [40, 10], [54, 13], [68, 9], [82, 14], [92, 28], [98, 44]],
  };
  let pts = PRE.hills.map(p => p.slice());
  let X, Y, TX, TY, K, N = 0, L = 0, hS = .25;
  let s = 0, v = 0, Em = 0, Q = 0, E0 = 1, t = 0, vmax = 0, s0 = 0, lastHist = -1, hist = [];
  let mu = 0, h0 = 30, running = true, slow = false, mode = 'drag', drag = null, stroke = null, anim = 0, stopped = false, vpk = 0, latch = false;

  // ---------- 線路（点をなめらかにつないで、等間隔の点の列にする） ----------
  function cr(p0, p1, p2, p3, out) {
    const d = (a, b) => Math.sqrt(Math.hypot(b[0] - a[0], b[1] - a[1])) || 1e-3;
    const t0 = 0, t1 = t0 + d(p0, p1), t2 = t1 + d(p1, p2), t3 = t2 + d(p2, p3);
    for (let k = 0; k < 24; k++) {
      const tt = t1 + (t2 - t1) * k / 24;
      const l = (a, b, ta, tb) => { const f = (tt - ta) / (tb - ta); return [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f]; };
      const A1 = l(p0, p1, t0, t1), A2 = l(p1, p2, t1, t2), A3 = l(p2, p3, t2, t3), B1 = l(A1, A2, t0, t2), B2 = l(A2, A3, t1, t3);
      out.push(l(B1, B2, t1, t2));
    }
  }
  function resamp(P, step) {
    const cum = [0]; for (let i = 1; i < P.length; i++) cum.push(cum[i - 1] + Math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]));
    const Lx = cum[cum.length - 1], n = Math.max(8, Math.round(Lx / step)), hs = Lx / n, out = []; let j = 0;
    for (let i = 0; i <= n; i++) { const ss = Math.min(Lx, i * hs); while (j < P.length - 2 && cum[j + 1] < ss) j++; const f = (ss - cum[j]) / ((cum[j + 1] - cum[j]) || 1); out.push([P[j][0] + (P[j + 1][0] - P[j][0]) * f, P[j][1] + (P[j + 1][1] - P[j][1]) * f]); }
    return { out, L: Lx, n, hs };
  }
  function build() {
    const n = pts.length, P = [];
    const ext = [[2 * pts[0][0] - pts[1][0], 2 * pts[0][1] - pts[1][1]], ...pts, [2 * pts[n - 1][0] - pts[n - 2][0], 2 * pts[n - 1][1] - pts[n - 2][1]]];
    for (let i = 0; i < n - 1; i++) cr(ext[i], ext[i + 1], ext[i + 2], ext[i + 3], P);
    P.push(pts[n - 1].slice());
    P.forEach(p => { if (p[1] < .6) p[1] = .6; });
    // いったん等間隔にしてから、急すぎる角を少し丸め、もう一度等間隔にする
    let R = resamp(P, .25), A = R.out;
    for (let pass = 0; pass < 2; pass++) A = A.map((p, i) => { const w = Math.min(10, i, A.length - 1 - i); if (!w) return p; let sx = 0, sy = 0; for (let q = -w; q <= w; q++) { sx += A[i + q][0]; sy += A[i + q][1]; } return [sx / (2 * w + 1), sy / (2 * w + 1)]; });
    R = resamp(A, .25); L = R.L; N = R.n; hS = R.hs;
    X = new Float64Array(N + 1); Y = new Float64Array(N + 1); TX = new Float64Array(N + 1); TY = new Float64Array(N + 1); K = new Float64Array(N + 1);
    for (let i = 0; i <= N; i++) { X[i] = R.out[i][0]; Y[i] = R.out[i][1]; }
    const th = new Float64Array(N + 1);
    for (let i = 0; i <= N; i++) { const a = Math.max(0, i - 1), b = Math.min(N, i + 1), dx = X[b] - X[a], dy = Y[b] - Y[a], d = Math.hypot(dx, dy) || 1; TX[i] = dx / d; TY[i] = dy / d; th[i] = Math.atan2(dy, dx); }
    for (let i = 0; i <= N; i++) { const a = Math.max(0, i - 1), b = Math.min(N, i + 1); let d = th[b] - th[a]; while (d > Math.PI) d -= 2 * Math.PI; while (d < -Math.PI) d += 2 * Math.PI; K[i] = d / ((b - a) * hS); }
    for (let pass = 0; pass < 5; pass++) { const k2 = K.slice(); for (let i = 0; i <= N; i++) { let sum = 0, c = 0; for (let q = -3; q <= 3; q++) { const u = i + q; if (u >= 0 && u <= N) { sum += k2[u]; c++; } } K[i] = sum / c; } }
  }
  function at(ss) {
    const u = clamp(ss / hS, 0, N - 1e-9), i = Math.floor(u), f = u - i;
    return { x: X[i] + (X[i + 1] - X[i]) * f, y: Y[i] + (Y[i + 1] - Y[i]) * f, tx: TX[i] + (TX[i + 1] - TX[i]) * f, ty: TY[i] + (TY[i + 1] - TY[i]) * f, k: K[i] + (K[i + 1] - K[i]) * f, slope: (Y[i + 1] - Y[i]) / hS };
  }
  function startS() {
    let i = 0; while (i < N - 1 && Y[i] > h0 && Y[i + 1] <= Y[i]) i++;
    if (i > 0 && Y[i] <= h0 && Y[i - 1] > h0) { const f = (Y[i - 1] - h0) / ((Y[i - 1] - Y[i]) || 1); return (i - 1 + f) * hS; }
    return i * hS;
  }

  // ---------- 運動（線路にそった1次元の運動） ----------
  function note(sx) { $('ceNote').textContent = sx; }
  function restart(msg) {
    s0 = startS(); s = s0; v = 0; const p = at(s); Em = g * p.y; Q = 0; E0 = Math.max(1, Em); t = 0; vmax = 0; hist = []; lastHist = -1; running = true; stopped = false; latch = false; vpk = 0;
    updPlay(); note('🎢 高さ ' + p.y.toFixed(1) + 'm からスタートしました。'); if (msg) flash(msg);
  }
  function phys(dt) {
    const n = Math.max(1, Math.ceil(dt * 480 - 1e-9)), h = dt / n;
    for (let q = 0; q < n; q++) {
      const p = at(s), Nn = g * p.tx + v * v * p.k, fr = mu * Math.abs(Nn);
      let a = -g * p.slope;
      if (latch || (Math.abs(v) < .03 && Math.abs(a) <= fr)) {
        if (!stopped && fr > 0) { stopped = true; note(t < .5 ? '🛑 まさつが大きくて、動き出せません。坂を急にするか、まさつを小さくしてみましょう。' : '🛑 まさつで止まりました。位置エネルギーの一部が、熱に変わりました。'); }
        { const rest = Em - g * p.y; if (rest > 0) { Q += rest; Em -= rest; } v = 0; }
        t += h; continue;
      }
      stopped = false;
      const vOld = v;
      a -= (v !== 0 ? Math.sign(v) : Math.sign(a)) * fr;
      v += a * h;
      if (vOld * v < 0 && Math.abs(g * p.slope) <= fr) v = 0;
      const ds = v * h; s += ds; t += h;
      const dQ = fr * Math.abs(ds); Q += dQ; Em -= dQ;
      if (s < 0) { s = -s; v = Math.abs(v); } else if (s > L) { s = 2 * L - s; v = -Math.abs(v); }
      const y = at(s).y, tg = Em - g * y;
      if (tg > .5 && v !== 0) v = Math.sign(v) * Math.sqrt(2 * tg);
      if (vOld * v < 0 && vpk > 1.5) note('↩️ 高さ ' + y.toFixed(1) + 'm でいったん止まって、戻りはじめました（スタートの高さは ' + at(s0).y.toFixed(1) + 'm）。');
      if (vOld * v < 0 && vpk < .12 && fr > 0) { latch = true; v = 0; }
      if (vOld * v < 0) vpk = 0; if (Math.abs(v) > vpk) vpk = Math.abs(v);
      if (Math.abs(v) > vmax) vmax = Math.abs(v);
    }
    if (t - lastHist >= .1) { const e = energies(); hist.push([t, e.pe, e.ke, e.q]); lastHist = t; if (hist.length > 260) hist.shift(); }
  }
  function energies() { const p = at(s); const pe = g * p.y * M / 1000, ke = .5 * v * v * M / 1000, q = Q * M / 1000; return { pe, ke, q, total: pe + ke + q, p }; }

  // ---------- 描く ----------
  let dpr = 1, W = 0, Hh = 0, sc = 1;
  function size() {
    const w = cv.clientWidth || 600; dpr = Math.min(2, window.devicePixelRatio || 1);
    const a = Math.round(w * dpr), b = Math.round(w * .625 * dpr); if (cv.width !== a || cv.height !== b) { cv.width = a; cv.height = b; }
    W = a; Hh = b; sc = W / 102;
    const gw = Math.round((gc.clientWidth || 600) * dpr), gh = Math.round((gc.clientHeight || 150) * dpr); if (gc.width !== gw || gc.height !== gh) { gc.width = gw; gc.height = gh; }
  }
  function rr(c, x, y, w, h, r) { c.beginPath(); if (c.roundRect) c.roundRect(x, y, w, h, r); else c.rect(x, y, w, h); }
  function draw() {
    size(); const c = ctx;
    c.setTransform(1, 0, 0, 1, 0, 0);
    const sky = c.createLinearGradient(0, 0, 0, Hh); sky.addColorStop(0, '#7dd3fc'); sky.addColorStop(1, '#e0f2fe'); c.fillStyle = sky; c.fillRect(0, 0, W, Hh);
    c.setTransform(sc, 0, 0, -sc, sc, Hh - 6 * sc);
    c.lineCap = 'round'; c.lineJoin = 'round';
    // 太陽・雲
    c.fillStyle = 'rgba(253,224,71,.95)'; c.beginPath(); c.arc(70, 52.5, 3, 0, 7); c.fill();
    c.fillStyle = 'rgba(255,255,255,.85)';
    [[10, 53, 1], [48, 55, .8], [80, 50, 1.1]].forEach(([x0, y, k], i) => { const x = ((x0 + anim * (.6 + i * .25)) % 124) - 12; [[0, 0, 5, 1.5], [2.4, .9, 3, 1.6], [-2.4, .6, 2.6, 1.3]].forEach(e => { c.beginPath(); c.ellipse(x + e[0] * k, y + e[1] * k, e[2] * k, e[3] * k, 0, 0, 7); c.fill(); }); });
    // 遠くの山
    c.fillStyle = '#b7e4c0'; c.beginPath(); c.moveTo(-1, 0); for (let x = -1; x <= 101; x += 2) c.lineTo(x, 8 + 4 * Math.sin(x * .07) + 2 * Math.sin(x * .19 + 1)); c.lineTo(101, 0); c.fill();
    // 観覧車
    c.strokeStyle = 'rgba(100,116,139,.4)'; c.lineWidth = .3; c.beginPath(); c.moveTo(66, 14); c.lineTo(62.5, 0); c.moveTo(66, 14); c.lineTo(69.5, 0); c.stroke();
    c.beginPath(); c.arc(66, 14, 9, 0, 7); c.stroke();
    for (let k = 0; k < 8; k++) { const a = anim * .25 + k * Math.PI / 4, x = 66 + Math.cos(a) * 9, y = 14 + Math.sin(a) * 9; c.beginPath(); c.moveTo(66, 14); c.lineTo(x, y); c.stroke(); c.fillStyle = ['rgba(248,113,113,.7)', 'rgba(250,204,21,.7)', 'rgba(96,165,250,.7)', 'rgba(74,222,128,.7)'][k % 4]; c.beginPath(); c.arc(x, y - .9, 1, 0, 7); c.fill(); }
    // 地面・木
    c.fillStyle = '#86c96a'; c.fillRect(-1, -6, 102, 6); c.fillStyle = '#65a30d'; c.fillRect(-1, -.45, 102, .45);
    [9, 33, 47, 60, 94].forEach((x, i) => { c.fillStyle = '#92400e'; c.fillRect(x - .3, 0, .6, 2.2); c.fillStyle = i % 2 ? '#16a34a' : '#15803d'; c.beginPath(); c.arc(x, 3.6, 1.9, 0, 7); c.fill(); });
    // 支柱
    c.strokeStyle = '#94a3b8'; c.lineWidth = .28; c.beginPath();
    const st = Math.max(1, Math.round(4 / hS)); for (let i = st; i < N; i += st) if (TX[i] > .3) { c.moveTo(X[i], Y[i]); c.lineTo(X[i], 0); } c.stroke();
    // いまのエネルギーで上がれる高さ（点線）
    c.setLineDash([1.3, 1.1]); c.strokeStyle = 'rgba(30,41,59,.6)'; c.lineWidth = .22; c.beginPath(); c.moveTo(-1, Em / g); c.lineTo(101, Em / g); c.stroke(); c.setLineDash([]);
    // レール
    c.beginPath(); c.moveTo(X[0], Y[0]); for (let i = 1; i <= N; i++) c.lineTo(X[i], Y[i]);
    c.strokeStyle = '#334155'; c.lineWidth = .95; c.stroke(); c.strokeStyle = '#e2e8f0'; c.lineWidth = .3; c.stroke();
    c.fillStyle = '#ef4444'; [0, N].forEach(i => { c.beginPath(); c.arc(X[i], Y[i], .9, 0, 7); c.fill(); });
    // スタートの旗
    const f0 = at(s0); c.strokeStyle = '#475569'; c.lineWidth = .22; c.beginPath(); c.moveTo(f0.x, f0.y); c.lineTo(f0.x, f0.y + 5); c.stroke();
    c.fillStyle = '#f97316'; c.beginPath(); c.moveTo(f0.x, f0.y + 5); c.lineTo(f0.x + 2.6, f0.y + 4.1); c.lineTo(f0.x, f0.y + 3.2); c.fill();
    // 車両（3両。計算はまん中の1点）
    const cols = ['#3b82f6', '#ef4444', '#facc15'], fast = Math.abs(v) > 9;
    [-4.1, 0, 4.1].forEach((off, ci) => {
      const p = at(clamp(s + off, 0, L)); c.save(); c.translate(p.x, p.y); c.rotate(Math.atan2(p.ty, p.tx)); c.scale(1.5, 1.5);
      c.fillStyle = '#1e293b'; [-.72, .72].forEach(wx => { c.beginPath(); c.arc(wx, .5, .38, 0, 7); c.fill(); });
      c.fillStyle = cols[ci]; rr(c, -1.22, .55, 2.44, 1.2, .38); c.fill();
      c.fillStyle = 'rgba(255,255,255,.35)'; rr(c, -1.0, 1.35, 2.0, .22, .1); c.fill();
      [-.52, .52].forEach(hx => {
        if (fast) { c.strokeStyle = '#fcd9a8'; c.lineWidth = .17; c.beginPath(); c.moveTo(hx - .25, 2.2); c.lineTo(hx - .5, 3.05); c.moveTo(hx + .25, 2.2); c.lineTo(hx + .5, 3.05); c.stroke(); }
        c.fillStyle = '#fcd9a8'; c.beginPath(); c.arc(hx, 2.15, .43, 0, 7); c.fill();
        c.fillStyle = ci === 1 ? '#1e293b' : '#7c2d12'; c.beginPath(); c.arc(hx, 2.28, .43, .1, Math.PI - .1); c.fill();
      });
      c.restore();
    });
    // 動かせる点 / なぞった線
    if (mode === 'drag') {
      const r = Math.max(1.05, 7 * dpr / sc);
      pts.forEach((p, i) => { c.beginPath(); c.arc(p[0], p[1], r, 0, 7); c.fillStyle = drag && drag.i === i ? '#fde047' : '#fff'; c.fill(); c.strokeStyle = '#2563eb'; c.lineWidth = r * .32; c.stroke(); });
    } else if (stroke && stroke.length > 1) {
      c.strokeStyle = '#f97316'; c.lineWidth = .6; c.setLineDash([1, 1]); c.beginPath(); stroke.forEach((p, i) => i ? c.lineTo(p[0], p[1]) : c.moveTo(p[0], p[1])); c.stroke(); c.setLineDash([]);
    }
    // 高さの目もり
    c.setTransform(1, 0, 0, 1, 0, 0); c.fillStyle = 'rgba(15,23,42,.55)'; c.strokeStyle = 'rgba(15,23,42,.3)'; c.lineWidth = dpr; c.font = `${10 * dpr}px system-ui,sans-serif`; c.textAlign = 'left'; c.textBaseline = 'middle';
    [10, 20, 30, 40].forEach(hh => { const y = Hh - (hh + 6) * sc; c.beginPath(); c.moveTo(0, y); c.lineTo(5 * dpr, y); c.stroke(); c.fillText(hh + 'm', 7 * dpr, y); });
    drawG(); ui();
  }
  function drawG() {
    const c = gx, w = gc.width, h = gc.height; c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, w, h);
    const e = energies(), e0 = E0 * M / 1000, mx = Math.max(1, e0 * 1.12, e.total * 1.05);
    const top = 6 * dpr, bot = h - 18 * dpr, Yv = val => bot - (val / mx) * (bot - top);
    const bw = Math.min(34 * dpr, w * .062), gap = bw * .4, x0 = 4 * dpr;
    const bars = [[e.pe, '#2563eb', '位置'], [e.ke, '#ef4444', '運動'], [e.q, '#f59e0b', '熱']];
    c.font = `${10 * dpr}px system-ui,sans-serif`; c.textAlign = 'center'; c.textBaseline = 'top';
    bars.forEach((b, i) => { const x = x0 + i * (bw + gap); c.fillStyle = '#f1f5f9'; c.fillRect(x, top, bw, bot - top); c.fillStyle = b[1]; c.fillRect(x, Yv(b[0]), bw, bot - Yv(b[0])); c.fillStyle = '#475569'; c.fillText(b[2], x + bw / 2, bot + 4 * dpr); });
    const xt = x0 + 3 * (bw + gap); let acc = 0; c.fillStyle = '#f1f5f9'; c.fillRect(xt, top, bw, bot - top);
    bars.forEach(b => { c.fillStyle = b[1]; c.fillRect(xt, Yv(acc + b[0]), bw, Yv(acc) - Yv(acc + b[0])); acc += b[0]; });
    c.fillStyle = '#475569'; c.fillText('合計', xt + bw / 2, bot + 4 * dpr);
    const gx0 = xt + bw + 12 * dpr, gx1 = w - 4 * dpr, SP = 20;
    c.fillStyle = '#f8fafc'; c.fillRect(gx0, top, gx1 - gx0, bot - top);
    if (hist.length > 1) {
      const t1 = hist[hist.length - 1][0], tA = Math.max(0, t1 - SP), Xt = tt => gx0 + clamp((tt - tA) / SP, 0, 1) * (gx1 - gx0);
      const hs = hist.filter(q => q[0] >= tA - .2);
      [[q => q[1] + q[2] + q[3], '#f59e0b'], [q => q[1] + q[2], '#ef4444'], [q => q[1], '#2563eb']].forEach(([f, col]) => {
        c.fillStyle = col; c.beginPath(); c.moveTo(Xt(hs[0][0]), bot); hs.forEach(q => c.lineTo(Xt(q[0]), Yv(f(q)))); c.lineTo(Xt(hs[hs.length - 1][0]), bot); c.closePath(); c.fill();
      });
    }
    c.strokeStyle = 'rgba(15,23,42,.6)'; c.lineWidth = 1.2 * dpr; c.setLineDash([4 * dpr, 3 * dpr]); c.beginPath(); c.moveTo(x0, Yv(e0)); c.lineTo(gx1, Yv(e0)); c.stroke(); c.setLineDash([]);
    c.fillStyle = '#64748b'; c.textAlign = 'right'; c.fillText('時間 →', gx1, bot + 4 * dpr);
  }
  let lastUI = 0;
  function ui() {
    const now = performance.now(); if (now - lastUI < 100) return; lastUI = now;
    const e = energies(), p = e.p, G = (g * p.tx + v * v * p.k) / g;
    $('ceV').innerHTML = (Math.abs(v) * 3.6).toFixed(0) + '<small>km/h</small>';
    $('ceH').innerHTML = p.y.toFixed(1) + '<small>m</small>';
    $('ceGf').innerHTML = G.toFixed(1) + '<small>G</small>';
    $('ceMax').innerHTML = (vmax * 3.6).toFixed(0) + '<small>km/h</small>';
    $('ceHeat').innerHTML = (Q / E0 * 100).toFixed(0) + '<small>%</small>';
    $('cePE').textContent = e.pe.toFixed(0); $('ceKE').textContent = e.ke.toFixed(0); $('ceQ').textContent = e.q.toFixed(0); $('ceTot').textContent = e.total.toFixed(0);
  }

  // ---------- 操作 ----------
  function flash(sx) { const el = $('ceMsg'); el.textContent = sx; el.classList.add('show'); clearTimeout(flash.t); flash.t = setTimeout(() => el.classList.remove('show'), 2400); }
  function updPlay() { $('cePlay').textContent = running ? '⏸ 止める' : '▶ スタート'; $('ceSlow').classList.toggle('on', slow); }
  $('cePlay').addEventListener('click', () => { running = !running; updPlay(); });
  $('ceReset').addEventListener('click', () => restart('スタート地点に戻しました'));
  $('ceSlow').addEventListener('click', () => { slow = !slow; updPlay(); });
  $('cePre').addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    pts = PRE[b.dataset.p].map(p => p.slice()); document.querySelectorAll('#cePre button').forEach(x => x.classList.toggle('on', x === b));
    build(); restart();
  });
  $('ceMode').addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return; mode = b.dataset.m; stroke = null;
    document.querySelectorAll('#ceMode button').forEach(x => x.classList.toggle('on', x === b)); cv.style.cursor = mode === 'draw' ? 'crosshair' : 'grab';
    if (mode === 'draw') flash('左から右へ、線路の形をなぞってください');
  });
  const muTxt = n => n === 0 ? 'なし' : n <= 3 ? '小さい' : n <= 6 ? 'ふつう' : '大きい';
  function upMu() { const n = +$('ceMu').value; mu = n * .008; latch = false; $('ceMuV').textContent = n + '・' + muTxt(n); }
  $('ceMu').addEventListener('input', upMu); upMu();
  function upH0() { h0 = +$('ceH0').value; $('ceH0V').textContent = h0 + 'm'; }
  $('ceH0').addEventListener('input', () => { upH0(); restart(); }); upH0();

  function wpos(e) { const r = cv.getBoundingClientRect(), k = r.width / 102; return [(e.clientX - r.left) / k - 1, (r.height - (e.clientY - r.top)) / k - 6, k]; }
  function hold() { s0 = startS(); s = s0; v = 0; Em = g * at(s).y; Q = 0; E0 = Math.max(1, Em); vmax = 0; hist = []; lastHist = -1; t = 0; }
  cv.addEventListener('pointerdown', e => {
    const [x, y, k] = wpos(e);
    if (mode === 'draw') { stroke = [[x, y]]; drag = { draw: 1 }; }
    else {
      let bi = -1, bd = 1e9; pts.forEach((p, i) => { const d = Math.hypot(p[0] - x, p[1] - y); if (d < bd) { bd = d; bi = i; } });
      if (bd * k > (e.pointerType === 'mouse' ? 18 : 30)) return;
      drag = { i: bi }; cv.style.cursor = 'grabbing';
    }
    try { cv.setPointerCapture(e.pointerId); } catch (err) {}
    e.preventDefault();
  });
  cv.addEventListener('pointermove', e => {
    if (!drag) return; const [x, y] = wpos(e);
    if (drag.draw) { const q = stroke[stroke.length - 1]; if (Math.hypot(x - q[0], y - q[1]) > .8) stroke.push([clamp(x, 0, 100), clamp(y, 1.5, 52)]); }
    else { pts[drag.i] = [clamp(x, 0, 100), clamp(y, 1.5, 52)]; build(); hold(); }
    e.preventDefault();
  });
  function endDrag() {
    if (!drag) return;
    if (drag.draw) {
      const cum = [0]; for (let i = 1; i < stroke.length; i++) cum.push(cum[i - 1] + Math.hypot(stroke[i][0] - stroke[i - 1][0], stroke[i][1] - stroke[i - 1][1]));
      const tot = cum[cum.length - 1];
      if (tot < 20) flash('もう少し長く、なぞってください');
      else {
        const m = clamp(Math.round(tot / 11), 5, 16), np = []; let j = 0;
        for (let i = 0; i < m; i++) { const ss = tot * i / (m - 1); while (j < stroke.length - 2 && cum[j + 1] < ss) j++; const f = (ss - cum[j]) / ((cum[j + 1] - cum[j]) || 1); np.push([stroke[j][0] + (stroke[j + 1][0] - stroke[j][0]) * f, stroke[j][1] + (stroke[j + 1][1] - stroke[j][1]) * f]); }
        pts = np; document.querySelectorAll('#cePre button').forEach(x => x.classList.remove('on')); build(); flash('なぞった形の線路ができました');
      }
      stroke = null;
    }
    drag = null; cv.style.cursor = mode === 'draw' ? 'crosshair' : 'grab'; restart();
  }
  cv.addEventListener('pointerup', endDrag); cv.addEventListener('pointercancel', endDrag);

  // ---------- シェア ----------
  function shareText() { return `ジェットコースターを高さ${at(s0).y.toFixed(0)}mから走らせたら、最高の速さは時速${(vmax * 3.6).toFixed(0)}kmでした🎢 位置エネルギーと運動エネルギーが入れかわるようすがグラフでわかる`; }
  $('shareBtn').addEventListener('click', () => { const u = location.origin + location.pathname; window.open('https://twitter.com/intent/tweet?text=' + encodeURIComponent(shareText() + '\n') + '&url=' + encodeURIComponent(u) + '&hashtags=' + encodeURIComponent('シミュラボ'), '_blank', 'noopener'); });
  $('copyBtn').addEventListener('click', async () => { try { await navigator.clipboard.writeText(shareText() + '\n' + location.origin + location.pathname); flash('コピーしました'); } catch (e) { flash('コピーできませんでした'); } });

  // ---------- 動かす ----------
  let tPrev = performance.now();
  function loop(now) {
    const dt = Math.min(.05, Math.max(0, (now - tPrev) / 1000)); tPrev = now; anim += dt;
    if (running && !drag) phys(dt * (slow ? .25 : 1));
    draw(); requestAnimationFrame(loop);
  }
  build(); restart();
  requestAnimationFrame(loop);
  window.__t = {
    step(sec) { const n = Math.max(1, Math.round(sec * 60)); for (let i = 0; i < n; i++) phys(1 / 60); anim += sec; lastUI = 0; draw(); },
    get s() { const e = energies(), p = e.p; return { t, s, L, x: p.x, y: p.y, v, kmh: Math.abs(v) * 3.6, pe: e.pe, ke: e.ke, heat: e.q, total: e.total, e0: E0 * M / 1000, G: (g * p.tx + v * v * p.k) / g, mu, h0, vmax, running, stopped }; },
    set(o) { if (o.mu != null) { $('ceMu').value = o.mu; upMu(); } if (o.h0 != null) { $('ceH0').value = o.h0; upH0(); } if (o.preset) { pts = PRE[o.preset].map(p => p.slice()); build(); } if (o.pts) { pts = o.pts.map(p => p.slice()); build(); } restart(); },
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
