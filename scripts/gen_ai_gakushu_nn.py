# -*- coding: utf-8 -*-
"""AI（ニューラルネットワーク）の学習を見るシミュレーター（2026-11-24）
   sims/ai-gakushu-nn/index.html を書き出す（冪等）。 使い方: python -X utf8 scripts/gen_ai_gakushu_nn.py"""
import html as H, io, json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://shimulabo.com"
SLUG = "ai-gakushu-nn"
NAME = "AIの学習（ニューラルネットワーク）シミュレーター"
CAT = "ふしぎ・現象"
TITLE = "AIが学習するようすを見る｜ニューラルネットワークの学習シミュレーター（逆伝播・境界線の変化）｜シミュラボ"
DESC = ("小さなニューラルネットワークが、2色の点を分ける境界線を学習していくようすをリアルタイムで見るシミュレーター。"
        "データの形（2つのかたまり・円の内と外・XOR・うずまき）、ニューロンの数、層の数、学習の速さを変えられます。"
        "ニューロン1個では円やXORを分けられず、増やすと分けられることを体験できます。")
OG_T = "AIが学習するようすを見る ニューラルネットワーク シミュレーター"
OG_D = "2色の点を分ける境界線が、学習でぐにゃりと曲がっていく。ニューロンの数や層の数を変えて、AIの学習をためせます。"
H1 = "AIが学習するようすを見る<br>ニューラルネットワーク シミュレーター"
LEAD = ("オレンジと青の点を、AI（小さなニューラルネットワーク）が色分けしようとしています。背景の色は「いまのAIの判定」です。"
        "学習が進むと、境界線が少しずつ動いて点を分けていきます。データの形やニューロンの数を変えたり、画面をタップして点を足したりして、ためしてみましょう。")

FAQ = [
    ("どうやって遊びますか？", "開くとすぐに学習がはじまります。上のボタンで「データの形」をえらび、下のスライダーで中間層のニューロンの数・層の数・学習の速さを変えます。左の図をタップ（クリック）すると、えらんでいる色の点を足せます。「🔄 リセット」で、重みを最初からやりなおします。"),
    ("ニューロン1個だと、円やXORを分けられないのはなぜ？", "ニューロン1個は、平面を1本のまっすぐな線で2つに分けることしかできないからです。円の内と外や、XOR（ななめ向かいが同じ色）は、まっすぐな線1本では分けられません。ニューロンを増やすと、何本かの線を組み合わせて、曲がった境界を作れるようになります。"),
    ("学習の速さを上げると、どうなりますか？", "1回の学習で重みを動かす大きさ（学習率）が大きくなり、早く進みます。ただし大きすぎると、行きすぎてはもどることをくり返し、誤差のグラフがガタガタして落ち着かないことがあります。小さすぎると、安定しますが時間がかかります。"),
    ("リセットするたびに結果が少しちがうのはなぜ？", "学習をはじめる前の重みを、毎回ちがう乱数（でたらめな数）で決めているからです。出発点がちがうと、たどりつく境界の形や、かかる回数も変わります。ニューロンが少ないときは、出発点によってうまく分けられないこともあります。"),
    ("ChatGPTのようなAIも、同じしくみですか？", "「数に重みをかけて足し合わせる」「誤差が小さくなるように重みを少しずつ直す」という基本の考え方は同じです。ただし、実際のAIは重みの数が数十億個以上あり、ネットワークの形（トランスフォーマーなど）もデータの量も、このシミュレーターとはけた違いです。"),
]
REL = [("maze-ai", "🤖", "迷路をAIが解く 探索アルゴリズム対決"), ("sort-visualizer", "📊", "ソートアルゴリズム可視化"), ("markov-bunsho", "📝", "AIはこうやって文章を作る マルコフ連鎖シミュレーター")]

ARTICLE = """
<h2>このシミュレーターのしくみ</h2>
<p>ニューラルネットワークは、<b>ニューロン</b>という小さな計算の部品を、線でつないだものです。ここでは「入力2つ（点の横の位置 x と、たての位置 y）→ 中間層 → 出力1つ」という小さなネットワークを使っています。</p>
<ul>
<li><b>ニューロンの計算</b>：入ってきた数に、それぞれ<b>重み</b>をかけて足し合わせ、さらに「バイアス」という数を足します。その結果を tanh（ハイパボリックタンジェント）という関数に通して、−1〜1の数にします。</li>
<li><b>出力</b>：最後のニューロンは、シグモイド関数で0〜1の数を出します。0.5より大きければ「青」、小さければ「オレンジ」と判定します。背景の色は、この数を場所ごとに計算してぬったものです。</li>
<li><b>誤差</b>：判定と正解がどれだけずれているかを、交差エントロピーという式で1つの数にします。全部の点を自信をもって当てるほど、0に近づきます。</li>
<li><b>学習</b>：誤差を小さくするには、それぞれの重みを「どちら向きに、どれくらい」動かせばよいかを、出力側から入力側へさかのぼって計算します（<b>誤差逆伝播法</b>）。そのとおりに重みを少しだけ動かすことを、何百回もくり返します。</li>
</ul>
<p>右の図では、線の<b>太さ</b>が重みの大きさ、<b>色</b>が重みの正（青）と負（オレンジ）を表します。丸の中の模様は、そのニューロンが平面のどこで強く反応しているかを表しています。</p>
<p>このシミュレーターでは、1回の学習で全部の点を使い、重みの直し方には Adam という方法を使っています。計算はすべて、いま見ているブラウザの中で行っています。</p>

<h2>ためしてみたいこと</h2>
<ul>
<li><b>「円の内と外」でニューロンを1個にする</b>：境界はまっすぐな線1本にしかならず、正解率は上がりきりません。2個、3個と増やすと、線が組み合わさって、まん中の青い点を囲めるようになります。</li>
<li><b>「XOR（市松）」でニューロンを1個 → 4個にする</b>：1個では分けられません。増やすと、ななめ向かいの同じ色どうしをまとめる境界ができます。</li>
<li><b>「うずまき」で層を2、ニューロンを8にする</b>：いちばんむずかしい形です。層1・ニューロン少なめでは分けきれませんが、増やすと、時間をかけて境界がうずを巻いていきます。</li>
<li><b>学習の速さを「とてもはやい」にする</b>：誤差のグラフがガタガタすることがあります。「ゆっくり」にすると、なめらかに下がります。</li>
<li><b>点を足す</b>：青いかたまりの中にオレンジの点を1つ置くと、AIがその点に合わせようとして境界をゆがめます。ニューロンが多いほど、無理に合わせることができます。</li>
<li><b>同じ設定で何回かリセットする</b>：出発点の重みがちがうので、境界の形や学習にかかる回数が毎回変わります。</li>
</ul>

<h2>本物では</h2>
<p>1個のニューロン（単純パーセプトロン）では XOR のような問題を解けないことは、1969年にミンスキーとパパートがくわしく論じました。中間層をもつネットワークを誤差逆伝播法で学習させる方法は、1986年のラメルハート、ヒントン、ウィリアムズの論文で広く知られるようになり、いまのAIの学習でも基本になっています。</p>
<p>また、中間層のニューロンを十分に増やせば、連続な関数にいくらでも近づけられることが数学的に示されています（ただし、学習でその重みを見つけられるかどうかは別の問題です）。</p>
<p>このシミュレーターは、しくみをつかむためにとても単純にしたものです。実際のAIは、入力が2つではなく画像や文章で、重みの数は数十億個以上になることがあります。活性化関数には tanh ではなく ReLU などがよく使われ、データも一度に全部ではなく小分けにして学習します。また、練習用のデータに合わせすぎて新しいデータで外れてしまう「過学習」を防ぐくふうも必要です。ここでの正解率は、学習に使った点だけで数えたものです。</p>
"""

REFS = [
    "Rumelhart, D. E., Hinton, G. E. & Williams, R. J. (1986) Learning representations by back-propagating errors. Nature 323, 533–536.",
    "Minsky, M. & Papert, S. (1969) Perceptrons: An Introduction to Computational Geometry. MIT Press.",
    "Cybenko, G. (1989) Approximation by superpositions of a sigmoidal function. Mathematics of Control, Signals, and Systems 2, 303–314.",
    "Kingma, D. P. & Ba, J. (2015) Adam: A Method for Stochastic Optimization. ICLR 2015.",
]

STAGE = r"""
<style>
.nn-seg{display:flex;flex-wrap:wrap;gap:6px}
.nn-seg button,.nn-tools button{border:1.5px solid var(--line);background:#fff;border-radius:999px;padding:8px 13px;font:inherit;font-size:13.5px;font-weight:800;cursor:pointer;color:var(--ink)}
.nn-seg button.on{background:#4338ca;border-color:#4338ca;color:#fff}
.nn-seg button[data-c="0"].on{background:#ea580c;border-color:#ea580c}
.nn-seg button[data-c="1"].on{background:#2563eb;border-color:#2563eb}
.nn-stage{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px}
.nn-stage>div{min-width:0}
.nn-box{position:relative;border-radius:14px;overflow:hidden;border:1px solid var(--line);background:#fff}
#nnField{display:block;width:100%;aspect-ratio:1/1;cursor:crosshair;touch-action:manipulation}
#nnNet{display:block;width:100%;aspect-ratio:1/1}
.nn-cap{font-size:12px;color:var(--ink-2);margin:5px 2px 0;font-weight:700;line-height:1.5}
.nn-cap i{display:inline-block;width:18px;height:4px;border-radius:2px;vertical-align:3px;margin:0 3px 0 6px}
.nn-msg{position:absolute;left:50%;bottom:10px;transform:translateX(-50%);background:rgba(15,23,42,.85);color:#fff;font-size:12.5px;font-weight:700;border-radius:12px;padding:6px 14px;max-width:92%;text-align:center;pointer-events:none;opacity:0;transition:opacity .3s}
.nn-msg.show{opacity:1}
.nn-tools{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-top:12px}
.nn-tools button.go{background:#0f172a;border-color:#0f172a;color:#fff}
.nn-tools .sp{flex:1 1 8px}
.nn-sum{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:12px}
.nn-sum div{background:#eef2ff;border-radius:12px;padding:10px 4px;text-align:center}
.nn-sum b{display:block;font-size:21px;color:#3730a3;font-variant-numeric:tabular-nums}
.nn-sum b small{font-size:11.5px}
.nn-sum span{font-size:11.5px;color:var(--ink-2);font-weight:700}
.nn-note{font-size:13.5px;color:var(--ink);background:#eef2ff;border-radius:10px;padding:9px 12px;margin:10px 0 0;font-weight:700}
#nnG{display:block;width:100%;height:90px;margin-top:10px}
.nn-glegend{font-size:12px;color:var(--ink-2);display:flex;gap:14px;flex-wrap:wrap}
.nn-glegend i{display:inline-block;width:18px;height:3px;vertical-align:3px;margin-right:4px;background:#ea580c}
.nn-glegend i.b{background:repeating-linear-gradient(90deg,#2563eb 0 5px,transparent 5px 8px)}
.nn-cols{display:grid;grid-template-columns:1fr 1fr;gap:6px 22px}
@media (max-width:640px){.nn-stage{grid-template-columns:1fr}#nnNet{aspect-ratio:4/3}.nn-cols{grid-template-columns:1fr}.nn-seg button,.nn-tools button{padding:8px 11px;font-size:13px}}
</style>
"""

BODY = r"""
  <section class="panel" id="resultPanel">
    <h2 style="margin:0 0 8px;font-size:18px;">① データの形をえらぶ</h2>
    <div class="nn-seg" id="nnData">
      <button type="button" data-v="blobs">2つのかたまり</button>
      <button type="button" data-v="circle" class="on">円の内と外</button>
      <button type="button" data-v="xor">XOR（市松）</button>
      <button type="button" data-v="spiral">うずまき</button>
    </div>

    <div class="nn-stage">
      <div>
        <div class="nn-box">
          <canvas id="nnField" aria-label="オレンジと青の点と、AIのいまの判定を色でぬった図"></canvas>
          <div class="nn-msg" id="nnMsg"></div>
        </div>
        <p class="nn-cap">背景の色＝いまのAIの判定。黒い線が境界です。タップすると点を足せます。</p>
      </div>
      <div>
        <div class="nn-box"><canvas id="nnNet" aria-label="ニューラルネットワークの図。線の太さと色が重みを表す"></canvas></div>
        <p class="nn-cap">左から 入力（x・y）→ 中間層 → 出力。線の太さ＝重みの大きさ<i style="background:#2563eb"></i>正の重み<i style="background:#ea580c"></i>負の重み</p>
      </div>
    </div>

    <div class="nn-tools">
      <button type="button" id="nnPlay" class="go">⏸ 一時停止</button>
      <button type="button" id="nnReset">🔄 リセット</button>
      <span class="sp"></span>
      <div class="nn-seg" id="nnPen"><button type="button" data-c="0">🟠 オレンジを足す</button><button type="button" data-c="1" class="on">🔵 青を足す</button></div>
      <button type="button" id="nnUndo">点をもとにもどす</button>
      <button type="button" id="nnClear">点をぜんぶ消す</button>
    </div>

    <div class="nn-sum">
      <div><b id="mStep">0</b><span>学習した回数</span></div>
      <div><b id="mAcc">0</b><span>正解率</span></div>
      <div><b id="mLoss">0</b><span>誤差</span></div>
    </div>
    <p class="nn-note" id="nnNote">🧠 学習をはじめました。</p>
    <canvas id="nnG" aria-label="誤差と正解率の変化のグラフ"></canvas>
    <div class="nn-glegend"><span><i></i>誤差（下がるほどよい）</span><span><i class="b"></i>正解率（上がるほどよい）</span></div>

    <h2 style="margin:20px 0 10px;font-size:18px;">② ネットワークの形と学習の速さ</h2>
    <div class="nn-cols">
      <div class="field"><label>中間層のニューロンの数 <span class="hint">（<b id="vH"></b>）</span></label><input type="range" id="kH" min="1" max="8" step="1" value="4"></div>
      <div class="field"><label>層の数（中間層）</label><div class="nn-seg" id="nnLayers"><button type="button" data-v="1" class="on">1層</button><button type="button" data-v="2">2層</button></div></div>
      <div class="field"><label>学習の速さ（学習率） <span class="hint">（<b id="vLr"></b>）</span></label><input type="range" id="kLr" min="0" max="4" step="1" value="2"></div>
    </div>
    <p class="nn-cap">ニューロンの数や層の数を変えると、重みを最初からやりなおします。</p>

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
  const cv = $('nnField'), ctx = cv.getContext('2d'), nc = $('nnNet'), nx = nc.getContext('2d'), gc = $('nnG'), gx = gc.getContext('2d');
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  function rng(s) { s = s >>> 0; return () => { s = (s + 0x6D2B79F5) >>> 0; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }

  const DNAME = { blobs: '2つのかたまり', circle: '円の内と外', xor: 'XOR（市松）', spiral: 'うずまき' };
  const LRS = [0.003, 0.01, 0.03, 0.1, 0.3], LRN = ['とてもゆっくり', 'ゆっくり', 'ふつう', 'はやい', 'とてもはやい'];
  const SPF = 1;                 // 1コマ（1/60秒）あたりの学習回数
  const OR = [234, 88, 12], BL = [37, 99, 235];
  let dataKey = 'circle', Hn = 4, NL = 1, lrIdx = 2, playing = true, steps = 0, loss = 0, acc = 0, seed = 3, pen = 1;
  let pts = [], hist = [];
  let sizes, W, B, mW, vW, mB, vB, gW, gB, A, D, tAdam = 0, thumbs = [];

  // ---------- データ（x, y は -1〜1。ラベル 0=オレンジ, 1=青） ----------
  function makeData(key) {
    const R = rng(4242 + key.length * 131 + key.charCodeAt(0)), out = [], n = 60;
    const gauss = () => { let u = 0; for (let i = 0; i < 6; i++) u += R(); return (u - 3) / .7071; };
    if (key === 'blobs') {
      for (let i = 0; i < n; i++) { out.push([-.45 + gauss() * .2, -.4 + gauss() * .2, 0]); out.push([.45 + gauss() * .2, .4 + gauss() * .2, 1]); }
    } else if (key === 'circle') {
      for (let i = 0; i < n; i++) {
        let a = R() * Math.PI * 2, r = Math.sqrt(R()) * .34; out.push([Math.cos(a) * r, Math.sin(a) * r, 1]);
        a = R() * Math.PI * 2; r = .62 + R() * .28; out.push([Math.cos(a) * r, Math.sin(a) * r, 0]);
      }
    } else if (key === 'xor') {
      for (let i = 0; i < n * 2; i++) { const x = (R() < .5 ? -1 : 1) * (.1 + R() * .8), y = (R() < .5 ? -1 : 1) * (.1 + R() * .8); out.push([x, y, x * y > 0 ? 1 : 0]); }
    } else {
      for (let i = 0; i < n; i++) {
        const t = i / (n - 1), r = .12 + .8 * t, th = t * 3 * Math.PI;
        const x = Math.cos(th) * r + gauss() * .02, y = Math.sin(th) * r + gauss() * .02;
        out.push([x, y, 0]); out.push([-x, -y, 1]);
      }
    }
    out.forEach(p => { p[0] = clamp(p[0], -.97, .97); p[1] = clamp(p[1], -.97, .97); });
    return out;
  }

  // ---------- ネットワーク（入力2 → tanh の中間層 → sigmoid の出力1） ----------
  const TN = 14;
  function initNet() {
    sizes = [2]; for (let i = 0; i < NL; i++) sizes.push(Hn); sizes.push(1);
    const R = rng(seed * 7919 + 13);
    W = []; B = []; mW = []; vW = []; mB = []; vB = []; gW = []; gB = [];
    for (let l = 0; l < sizes.length - 1; l++) {
      const nin = sizes[l], nout = sizes[l + 1], w = new Float64Array(nin * nout), b = new Float64Array(nout), s = Math.sqrt(6 / (nin + nout)) * (l === 0 ? 1.4 : 1);
      for (let i = 0; i < w.length; i++) w[i] = (R() * 2 - 1) * s;
      for (let i = 0; i < nout; i++) b[i] = (R() * 2 - 1) * .2;
      W.push(w); B.push(b);
      mW.push(new Float64Array(w.length)); vW.push(new Float64Array(w.length)); gW.push(new Float64Array(w.length));
      mB.push(new Float64Array(nout)); vB.push(new Float64Array(nout)); gB.push(new Float64Array(nout));
    }
    A = sizes.map(n => new Float64Array(n)); D = sizes.map(n => new Float64Array(n));
    thumbs = sizes.map(n => Array.from({ length: n }, () => { const c = document.createElement('canvas'); c.width = c.height = TN; const x = c.getContext('2d'); return { c, x, img: x.createImageData(TN, TN) }; }));
    steps = 0; tAdam = 0; hist = []; evalStats(); hist.push([0, loss, acc]);
  }
  // 順伝播
  function forward(x, y) {
    A[0][0] = x; A[0][1] = y; const Ln = W.length;
    for (let l = 0; l < Ln; l++) {
      const nin = sizes[l], nout = sizes[l + 1], w = W[l], b = B[l], a = A[l], o = A[l + 1];
      for (let j = 0; j < nout; j++) {
        let z = b[j]; const k = j * nin;
        for (let i = 0; i < nin; i++) z += w[k + i] * a[i];
        o[j] = l === Ln - 1 ? 1 / (1 + Math.exp(-z)) : Math.tanh(z);
      }
    }
    return A[Ln][0];
  }
  function adam(w, g, m, v, lr, c1, c2, n) {
    for (let i = 0; i < w.length; i++) {
      const gi = g[i] / n; m[i] = .9 * m[i] + .1 * gi; v[i] = .999 * v[i] + .001 * gi * gi;
      let x = w[i] - lr * (m[i] / c1) / (Math.sqrt(v[i] / c2) + 1e-8);
      w[i] = x > 40 ? 40 : x < -40 ? -40 : x;
    }
  }
  // 逆伝播で勾配を出して、重みを1回直す（全部の点を使う）
  function trainStep() {
    const Ln = W.length, n = pts.length; if (!n) return;
    for (let l = 0; l < Ln; l++) { gW[l].fill(0); gB[l].fill(0); }
    for (let q = 0; q < n; q++) {
      const p = pts[q], out = forward(p[0], p[1]);
      D[Ln][0] = out - p[2];                       // 交差エントロピー × sigmoid の勾配
      for (let l = Ln - 1; l >= 0; l--) {
        const nin = sizes[l], nout = sizes[l + 1], w = W[l], a = A[l], d = D[l + 1], dp = D[l], gw = gW[l], gb = gB[l];
        if (l > 0) dp.fill(0);
        for (let j = 0; j < nout; j++) {
          const dj = d[j], k = j * nin; gb[j] += dj;
          for (let i = 0; i < nin; i++) { gw[k + i] += dj * a[i]; if (l > 0) dp[i] += w[k + i] * dj; }
        }
        if (l > 0) for (let i = 0; i < nin; i++) dp[i] *= 1 - a[i] * a[i];   // tanh の微分
      }
    }
    tAdam++; const lr = LRS[lrIdx], c1 = 1 - Math.pow(.9, tAdam), c2 = 1 - Math.pow(.999, tAdam);
    for (let l = 0; l < Ln; l++) { adam(W[l], gW[l], mW[l], vW[l], lr, c1, c2, n); adam(B[l], gB[l], mB[l], vB[l], lr, c1, c2, n); }
    steps++;
  }
  function evalStats() {
    let L = 0, ok = 0; const n = pts.length;
    for (let q = 0; q < n; q++) { const p = pts[q], o = clamp(forward(p[0], p[1]), 1e-7, 1 - 1e-7); L += p[2] ? -Math.log(o) : -Math.log(1 - o); if ((o >= .5) === (p[2] === 1)) ok++; }
    loss = n ? L / n : 0; acc = n ? ok / n : 0;
  }
  function frameTrain() {
    if (!pts.length) return;
    for (let k = 0; k < SPF; k++) trainStep();
    evalStats();
    if (!isFinite(loss)) { seed++; initNet(); return; }
    hist.push([steps, loss, acc]);
    if (hist.length > 480) hist = hist.filter((q, i) => i % 2 === 0 || i === hist.length - 1);
  }

  // ---------- 描く ----------
  const GN = 56, off = document.createElement('canvas'); off.width = off.height = GN;
  const octx = off.getContext('2d'), img = octx.createImageData(GN, GN), val = new Float32Array(GN * GN);
  let dpr = 1;
  function size() {
    dpr = Math.min(2, window.devicePixelRatio || 1);
    [cv, nc, gc].forEach(el => { const w = Math.round((el.clientWidth || 320) * dpr), h = Math.round((el.clientHeight || 200) * dpr); if (el.width !== w || el.height !== h) { el.width = w; el.height = h; } });
  }
  function put(d, o, t, k) { const c = t < 0 ? OR : BL, s = Math.min(1, Math.abs(t)) * k; d[o] = 255 + (c[0] - 255) * s; d[o + 1] = 255 + (c[1] - 255) * s; d[o + 2] = 255 + (c[2] - 255) * s; d[o + 3] = 255; }
  function draw() {
    size();
    const Ln = W.length, d = img.data;
    // いまの判定を、あらい格子（56×56）で計算
    for (let gy = 0; gy < GN; gy++) {
      const y = 1 - (gy + .5) / GN * 2;
      for (let gi = 0; gi < GN; gi++) {
        const x = (gi + .5) / GN * 2 - 1, p = forward(x, y);
        val[gy * GN + gi] = p; put(d, (gy * GN + gi) * 4, p * 2 - 1, .62);
        if ((gy & 3) === 1 && (gi & 3) === 1) {
          const o = ((gy >> 2) * TN + (gi >> 2)) * 4;
          for (let l = 0; l <= Ln; l++) { const a = A[l], th = thumbs[l]; for (let j = 0; j < a.length; j++) put(th[j].img.data, o, l === Ln ? a[j] * 2 - 1 : a[j], .9); }
        }
      }
    }
    octx.putImageData(img, 0, 0);
    const c = ctx, Wd = cv.width, Hh = cv.height;
    c.setTransform(1, 0, 0, 1, 0, 0); c.imageSmoothingEnabled = true; c.imageSmoothingQuality = 'high';
    c.drawImage(off, 0, 0, Wd, Hh);
    // 境界線（判定がちょうど半々のところ）
    const sx = Wd / GN, sy = Hh / GN;
    c.beginPath();
    for (let j = 0; j < GN - 1; j++) for (let i = 0; i < GN - 1; i++) {
      const a = val[j * GN + i] - .5, b = val[j * GN + i + 1] - .5, e = val[(j + 1) * GN + i] - .5, f = val[(j + 1) * GN + i + 1] - .5;
      const sa = a > 0, sb = b > 0, se = e > 0, sf = f > 0; if (sa === sb && sb === se && se === sf) continue;
      const P = [];
      if (sa !== sb) P.push(i + a / (a - b), j);
      if (sb !== sf) P.push(i + 1, j + b / (b - f));
      if (se !== sf) P.push(i + e / (e - f), j + 1);
      if (sa !== se) P.push(i, j + a / (a - e));
      for (let k = 0; k + 3 < P.length; k += 4) { c.moveTo((P[k] + .5) * sx, (P[k + 1] + .5) * sy); c.lineTo((P[k + 2] + .5) * sx, (P[k + 3] + .5) * sy); }
    }
    c.lineCap = 'round'; c.strokeStyle = 'rgba(255,255,255,.85)'; c.lineWidth = 4.5 * dpr; c.stroke();
    c.strokeStyle = 'rgba(15,23,42,.85)'; c.lineWidth = 2 * dpr; c.stroke();
    // 点
    const pr = Math.max(3.2, Math.min(5, cv.clientWidth / 80)) * dpr;
    c.lineWidth = 1.3 * dpr; c.strokeStyle = '#fff';
    for (let q = 0; q < pts.length; q++) { const p = pts[q]; c.fillStyle = p[2] ? '#2563eb' : '#ea580c'; c.beginPath(); c.arc((p[0] + 1) / 2 * Wd, (1 - p[1]) / 2 * Hh, pr, 0, 7); c.fill(); c.stroke(); }
    drawNet(); drawGraph(); ui();
  }
  function drawNet() {
    const c = nx, Wd = nc.width, Hh = nc.height, nl = sizes.length;
    c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, Wd, Hh);
    const r = Math.min(Hh / 20, Wd / 14), padX = r * 2;
    const pos = (l, j) => { const n = sizes[l], gap = n > 1 ? Math.min((Hh - 2 * r - 10 * dpr) / (n - 1), r * 3.4) : 0; return [padX + (Wd - 2 * padX) * l / (nl - 1), Hh / 2 + (j - (n - 1) / 2) * gap]; };
    c.lineCap = 'round';
    for (let l = 0; l < nl - 1; l++) {
      const nin = sizes[l], nout = sizes[l + 1];
      for (let j = 0; j < nout; j++) for (let i = 0; i < nin; i++) {
        const w = W[l][j * nin + i], m = Math.abs(w), p0 = pos(l, i), p1 = pos(l + 1, j);
        c.strokeStyle = (w > 0 ? 'rgba(37,99,235,' : 'rgba(234,88,12,') + clamp(.2 + m * .3, .2, .95).toFixed(2) + ')';
        c.lineWidth = clamp(1.3 * Math.pow(m, .75), .5, 9) * dpr * (r / (20 * dpr) * .6 + .4);
        c.beginPath(); c.moveTo(p0[0], p0[1]); c.lineTo(p1[0], p1[1]); c.stroke();
      }
    }
    c.imageSmoothingEnabled = true; c.imageSmoothingQuality = 'high';
    for (let l = 0; l < nl; l++) for (let j = 0; j < sizes[l]; j++) {
      const p = pos(l, j), th = thumbs[l][j]; th.x.putImageData(th.img, 0, 0);
      c.save(); c.beginPath(); c.arc(p[0], p[1], r, 0, 7); c.clip(); c.fillStyle = '#fff'; c.fillRect(p[0] - r, p[1] - r, 2 * r, 2 * r); c.drawImage(th.c, p[0] - r, p[1] - r, 2 * r, 2 * r); c.restore();
      c.strokeStyle = '#334155'; c.lineWidth = (l === nl - 1 ? 2.6 : 1.8) * dpr; c.beginPath(); c.arc(p[0], p[1], r, 0, 7); c.stroke();
      if (l === 0) { c.font = `800 ${Math.round(r * .95)}px system-ui,sans-serif`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.lineWidth = 3 * dpr; c.strokeStyle = 'rgba(255,255,255,.9)'; c.strokeText(j ? 'y' : 'x', p[0], p[1]); c.fillStyle = '#0f172a'; c.fillText(j ? 'y' : 'x', p[0], p[1]); }
    }
  }
  function drawGraph() {
    const c = gx, Wd = gc.width, Hh = gc.height, p = 6 * dpr;
    c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, Wd, Hh);
    c.strokeStyle = '#e2e8f0'; c.lineWidth = 1 * dpr;
    [0, .5, 1].forEach(f => { const y = Hh - p - f * (Hh - 2 * p); c.beginPath(); c.moveTo(p, y); c.lineTo(Wd - p, y); c.stroke(); });
    if (hist.length < 2) return;
    const s1 = Math.max(hist[hist.length - 1][0], 120); let mx = .7; for (const q of hist) if (q[1] > mx) mx = q[1];
    const X = s => p + s / s1 * (Wd - 2 * p), Y = (v, m) => Hh - p - clamp(v / m, 0, 1) * (Hh - 2 * p);
    c.lineJoin = 'round';
    c.lineWidth = 1.5 * dpr; c.strokeStyle = '#2563eb'; c.setLineDash([4 * dpr, 3 * dpr]); c.beginPath(); hist.forEach((q, i) => i ? c.lineTo(X(q[0]), Y(q[2], 1)) : c.moveTo(X(q[0]), Y(q[2], 1))); c.stroke(); c.setLineDash([]);
    c.lineWidth = 2.2 * dpr; c.strokeStyle = '#ea580c'; c.beginPath(); hist.forEach((q, i) => i ? c.lineTo(X(q[0]), Y(q[1], mx)) : c.moveTo(X(q[0]), Y(q[1], mx))); c.stroke();
  }

  // ---------- 数字とひとこと ----------
  function advice() {
    if (!pts.length) return '✏️ 点がありません。左の図をタップして点を足すか、「点をもとにもどす」を押してください。';
    const one = pts.every(p => p[2] === pts[0][2]);
    if (one) return '✏️ いまは1色だけです。もう1つの色の点も足してみましょう。';
    if (acc >= .985) return `🎉 ほぼ全部の点を分けられました（${steps.toLocaleString()}回の学習）。ニューロンを減らしたり、点を足したりしてみましょう。`;
    if (steps > 500 && acc < .92 && (Hn === 1)) return '📏 ニューロン1個では、まっすぐな線1本でしか分けられません。ニューロンの数を増やしてみましょう。';
    if (steps > 1500 && acc < .92 && dataKey === 'spiral' && (NL === 1 || Hn < 6)) return '🌀 うずまきはむずかしい形です。層を2、ニューロンを8にしてみましょう。';
    if (steps > 2500 && acc < .9) return '🤔 なかなか分けきれません。ニューロンや層を増やすか、「リセット」で出発点を変えてみましょう。';
    if (!playing) return '⏸ 一時停止中です。「▶ スタート」で学習を続けます。';
    if (steps < 60) return '🧠 学習をはじめました。最初の重みはでたらめなので、判定もでたらめです。';
    return '🧠 学習中です。誤差が小さくなる向きに、重みを少しずつ動かしています。';
  }
  let lastUI = 0;
  function ui() {
    const now = performance.now(); if (now - lastUI < 150) return; lastUI = now;
    $('mStep').innerHTML = steps.toLocaleString() + '<small>回</small>';
    $('mAcc').innerHTML = pts.length ? (acc * 100).toFixed(acc >= .9995 ? 0 : 1) + '<small>%</small>' : '—';
    $('mLoss').textContent = pts.length ? loss.toFixed(3) : '—';
    $('nnNote').textContent = advice();
  }

  // ---------- 操作 ----------
  function flash(s) { const el = $('nnMsg'); el.textContent = s; el.classList.add('show'); clearTimeout(flash.t); flash.t = setTimeout(() => el.classList.remove('show'), 2200); }
  function updPlay() { $('nnPlay').textContent = playing ? '⏸ 一時停止' : '▶ スタート'; }
  function syncUI() {
    document.querySelectorAll('#nnData button').forEach(b => b.classList.toggle('on', b.dataset.v === dataKey));
    document.querySelectorAll('#nnLayers button').forEach(b => b.classList.toggle('on', +b.dataset.v === NL));
    document.querySelectorAll('#nnPen button').forEach(b => b.classList.toggle('on', +b.dataset.c === pen));
    $('kH').value = Hn; $('vH').textContent = Hn + '個'; $('kLr').value = lrIdx; $('vLr').textContent = LRN[lrIdx] + '・' + LRS[lrIdx];
    updPlay();
  }
  function reset(msg) { seed++; initNet(); playing = true; lastUI = 0; syncUI(); if (msg) flash(msg); }
  $('nnData').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; dataKey = b.dataset.v; pts = makeData(dataKey); reset('データを「' + DNAME[dataKey] + '」にしました'); });
  $('nnLayers').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; NL = +b.dataset.v; reset('中間層を' + NL + '層にしました'); });
  $('nnPen').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; pen = +b.dataset.c; syncUI(); });
  $('kH').addEventListener('input', e => { Hn = +e.target.value; reset(); });
  $('kLr').addEventListener('input', e => { lrIdx = +e.target.value; syncUI(); });
  $('nnPlay').addEventListener('click', () => { playing = !playing; lastUI = 0; updPlay(); });
  $('nnReset').addEventListener('click', () => reset('重みを最初からやりなおします'));
  $('nnUndo').addEventListener('click', () => { pts = makeData(dataKey); evalStats(); lastUI = 0; flash('点をもとにもどしました'); });
  $('nnClear').addEventListener('click', () => { pts = []; reset('点を消しました。タップして点を足してください'); });
  // タップで点を足す（指で画面を動かしたときは足さない）
  let dn = null;
  cv.addEventListener('pointerdown', e => { dn = [e.clientX, e.clientY]; });
  cv.addEventListener('pointercancel', () => { dn = null; });
  cv.addEventListener('pointerup', e => {
    if (!dn) return; const moved = Math.hypot(e.clientX - dn[0], e.clientY - dn[1]); dn = null; if (moved > 10) return;
    if (pts.length >= 400) { flash('点は400個までです'); return; }
    const r = cv.getBoundingClientRect();
    pts.push([clamp((e.clientX - r.left) / r.width * 2 - 1, -.98, .98), clamp(1 - (e.clientY - r.top) / r.height * 2, -.98, .98), pen]);
    evalStats(); lastUI = 0;
  });

  // ---------- シェア ----------
  function shareText() { return `AIの学習シミュレーターで「${DNAME[dataKey]}」を、ニューロン${Hn}個×${NL}層のネットワークに${steps.toLocaleString()}回学習させたら、正解率${(acc * 100).toFixed(0)}%になりました🧠`; }
  $('shareBtn').addEventListener('click', () => { const u = location.origin + location.pathname; window.open('https://twitter.com/intent/tweet?text=' + encodeURIComponent(shareText() + '\n') + '&url=' + encodeURIComponent(u) + '&hashtags=' + encodeURIComponent('シミュラボ'), '_blank', 'noopener'); });
  $('copyBtn').addEventListener('click', async () => { try { await navigator.clipboard.writeText(shareText() + '\n' + location.origin + location.pathname); flash('コピーしました'); } catch (e) { flash('コピーできませんでした'); } });

  // ---------- 動かす ----------
  let tPrev = performance.now(), accT = 0;
  function loop(now) {
    const dt = Math.min(.1, (now - tPrev) / 1000); tPrev = now;
    if (playing) { accT += dt * 60; let n = 0; while (accT >= 1 && n < 4) { frameTrain(); accT -= 1; n++; } if (accT > 4) accT = 0; }
    draw(); requestAnimationFrame(loop);
  }
  pts = makeData(dataKey); initNet(); syncUI();
  requestAnimationFrame(loop);
  window.__t = {
    step(sec) { const n = Math.round(sec * 60); for (let i = 0; i < n; i++) frameTrain(); lastUI = 0; draw(); },
    get s() { let bad = !isFinite(loss) || !isFinite(acc); for (const w of W) for (let i = 0; i < w.length; i++) if (!isFinite(w[i])) bad = true; return { steps, acc: +acc.toFixed(4), loss: +loss.toFixed(5), data: dataKey, hidden: Hn, layers: NL, lr: LRS[lrIdx], points: pts.length, playing, nan: bad, sizes: sizes.slice() }; },
    set(o) { if (o.data) { dataKey = o.data; pts = makeData(dataKey); } if (o.hidden) Hn = o.hidden; if (o.layers) NL = o.layers; if (o.lr != null) lrIdx = o.lr; if (o.seed != null) seed = o.seed - 1; reset(); if (o.playing != null) { playing = o.playing; updPlay(); } lastUI = 0; draw(); },
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
