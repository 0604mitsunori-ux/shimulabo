# -*- coding: utf-8 -*-
"""4ストロークエンジンのしくみ（2026-11-24）
   sims/engine-4stroke/index.html を書き出す（冪等）。 使い方: python -X utf8 scripts/gen_engine_4stroke.py"""
import html as H, io, json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://shimulabo.com"
SLUG = "engine-4stroke"
NAME = "4ストロークエンジンのしくみシミュレーター"
CAT = "クルマ・乗り物"
TITLE = "4ストロークエンジンのしくみ｜吸気・圧縮・燃焼・排気を断面アニメで見る（1気筒／直列4気筒）｜シミュラボ"
DESC = ("ガソリンエンジン（4ストロークエンジン）のしくみを、断面のアニメーションで見るシミュレーター。吸気→圧縮→燃焼（膨張）→排気の4つの行程で、"
        "ピストン・コンロッド・クランク軸・吸気バルブと排気バルブ・点火プラグ・混合気の粒がどう動くかがわかります。"
        "クランク軸が2回転するあいだに4行程が1回。1気筒と直列4気筒（点火順序1-3-4-2）を切り替えられます。")
OG_T = "4ストロークエンジンのしくみ 断面アニメーション"
OG_D = "吸気→圧縮→燃焼→排気。クランク軸が2回転するあいだに4行程が1回。1気筒と直列4気筒（1-3-4-2）で見られます。"
H1 = "4ストロークエンジンのしくみ<br>吸気・圧縮・燃焼・排気を断面で見る"
LEAD = ("ガソリンで走るクルマのエンジンの中を、横から切った断面で見てみましょう。ピストンが上下するたびに「吸気 → 圧縮 → 燃焼 → 排気」と進み、"
        "クランク軸が2回転するあいだに、この4つの行程が1回おこなわれます。回転数を変えたり、1行程ずつコマ送りしたり、直列4気筒に切り替えたりできます。")

FAQ = [
    ("なぜ「4ストローク」というのですか？", "ピストンが上から下へ、または下から上へ1回動くことを「ストローク（行程）」といいます。吸気・圧縮・燃焼・排気の4回のストロークで1つのサイクルになるので、4ストロークエンジン（4サイクルエンジン）とよばれます。"),
    ("クランク軸が2回転するあいだに、燃焼は1回だけですか？", "はい。1つの気筒では、クランク軸が2回転（720°）するあいだに燃焼は1回だけです。力が出ない吸気・圧縮・排気の行程は、はずみ車（フライホイール）の勢いや、ほかの気筒の燃焼の力で回りつづけます。"),
    ("バルブはどうやって開いたり閉じたりするのですか？", "カム軸についた「カム山」というでっぱりが、回りながらバルブをおし下げて開きます。カム山が通りすぎると、ばねの力でバルブが閉じます。カム軸はベルトやチェーンでクランク軸とつながっていて、クランク軸の半分の速さで回ります。"),
    ("直列4気筒の点火順序は、なぜ1-3-4-2なのですか？", "直列4気筒では、ふつう1番と4番、2番と3番のピストンがそれぞれ同じ動きをします。同じ動きをする2つを1回転（360°）ずらして燃やすと、クランク軸が半回転（180°）するごとにどこかの気筒が燃える、等間隔の点火になります。この条件に合う順番が1-3-4-2と1-2-4-3で、1-3-4-2が広く使われています。"),
    ("表示されている回転数は、本物のエンジンと同じですか？", "いいえ。動きが目で追えるように、とてもゆっくりにした模式的な値です。本物のクルマのエンジンは、止まって待っているとき（アイドリング）でも1分間に数百回転以上で回っています。"),
]
REL = [("gears", "⚙️", "歯車シミュレーター"), ("nenpi-gas", "⛽", "年間ガソリン代シミュレーター"), ("kuruma-iji", "🚙", "車の維持費シミュレーター")]

ARTICLE = """
<h2>このシミュレーターのしくみ</h2>
<p>ガソリンエンジンは、シリンダー（筒）の中で燃料を燃やし、その力でピストンをおし下げます。ピストンの上下の動きは、<b>コンロッド</b>という棒を通して<b>クランク軸</b>に伝わり、回転の動きに変わります。自転車のペダルを足で上下にふむと、車輪が回るのと似ています。</p>
<p>4ストロークエンジンは、次の4つの行程をくり返します。</p>
<ul>
<li><b>① 吸気</b>：吸気バルブが開き、ピストンが下がります。空気とガソリンがまざった気体（混合気）がシリンダーに吸いこまれます。</li>
<li><b>② 圧縮</b>：バルブが2つとも閉じ、ピストンが上がって混合気をおしちぢめます。</li>
<li><b>③ 燃焼（膨張）</b>：点火プラグの火花で混合気に火がつきます。燃えて高温・高圧になったガスが、ピストンを強くおし下げます。力が出るのは、この行程だけです。</li>
<li><b>④ 排気</b>：排気バルブが開き、ピストンが上がって、燃えたあとのガスをおし出します。</li>
</ul>
<p>ピストンが1回下がって1回上がると、クランク軸は1回転します。4つの行程ではピストンが2往復するので、<b>クランク軸が2回転（720°）するあいだに、4行程が1回</b>です。バルブを動かすカム軸は、そのあいだに1回転だけします。</p>
<p>このシミュレーターでは、ピストンの位置を、クランク軸の角度とコンロッドの長さから図形の計算で求めています。そのため、ピストンは上のほうでは速く、下のほうではゆっくり向きを変えます。</p>
<p>わかりやすくするために、単純にしているところがあります。</p>
<ul>
<li>バルブは、ピストンがいちばん上（上死点）・いちばん下（下死点）に来たちょうどのところで開閉するようにしています。本物は少し早く開き、少しおそく閉じます。吸気バルブと排気バルブが両方とも開いている時間もあります。</li>
<li>点火は、ピストンがいちばん上に来たちょうどのところにしています。本物は、それより少し手前で点火します。</li>
<li>粒の数・色・動きは、気体のようすを表すイメージです。圧縮の強さ（圧縮比）も、見やすさを優先して本物より小さくしています。</li>
<li>4気筒の表示は、4つの気筒の断面を横に並べた図です。本物の直列4気筒は、1本のクランク軸に4つのピストンがつながっています。</li>
<li>回転数は、動きが見えるようにゆっくりにした模式的な値です。</li>
</ul>

<h2>ためしてみたいこと</h2>
<ul>
<li><b>回転数をいちばんゆっくりにする</b>：バルブが開くタイミングと、ピストンの向きが変わるタイミングを見くらべてみましょう。</li>
<li><b>「次の行程へ」で1つずつ進める</b>：行程が1つ進むたびに、クランク角が180°ずつふえます。4回おすと720°で、もとの吸気にもどります。</li>
<li><b>1気筒の表示で、右の輪を見る</b>：外側の針が1周するあいだに、内側の点（クランク軸の向き）は2周します。</li>
<li><b>カムを見る</b>：バルブの上で回っている、たまご形の部品がカムです。クランク軸の半分の速さで回り、でっぱりが下を向いたときだけバルブが開きます。</li>
<li><b>直列4気筒に切り替える</b>：オレンジ色に光る気筒が、1番 → 3番 → 4番 → 2番の順にうつっていきます。1番と4番、2番と3番のピストンが、いつも同じ高さにあることもたしかめてみましょう。</li>
<li><b>4気筒で回転数を上げる</b>：クランク軸が半回転するごとにどこかの気筒が燃えるので、1気筒よりも力がとぎれにくいことがわかります。</li>
</ul>

<h2>本物では</h2>
<p>本物のガソリンエンジンでは、圧縮比（いちばん広いときと、いちばんせまいときの体積の比）は、おおよそ10前後のものが多くなっています。回転数も、走っているときは1分間に数千回転になることがあります。その速さで、バルブの開閉と点火が正確なタイミングでくり返されています。</p>
<p>燃料の入れ方にも種類があります。吸気の通り道にガソリンを噴いて混合気にしてから吸いこむ方式のほか、空気だけを吸いこんで、シリンダーの中に直接ガソリンを噴く方式（直噴）もあります。</p>
<p>ディーゼルエンジンも同じ4つの行程で動きますが、点火プラグは使いません。空気だけを強く圧縮して高温にし、そこへ燃料を噴いて自然に火をつけます。</p>
<p>気筒の数や並べ方（直列・V型・水平対向など）は、クルマによってさまざまです。気筒が多いほど、燃焼の間かくが短くなり、回転がなめらかになります。</p>
"""

REFS = [
    "自動車技術会 編「自動車技術ハンドブック」",
    "JAF（日本自動車連盟）「クルマ何でも質問箱」",
    "文部科学省「中学校学習指導要領解説 技術・家庭編」（エネルギー変換の技術）",
]

STAGE = r"""
<style>
.en-tools{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-bottom:10px}
.en-seg{display:flex;flex-wrap:wrap;gap:6px}
.en-seg button,.en-tools button{border:1.5px solid var(--line);background:#fff;border-radius:999px;padding:8px 13px;font:inherit;font-size:13.5px;font-weight:800;cursor:pointer;color:var(--ink)}
.en-seg button.on{background:#0f172a;border-color:#0f172a;color:#fff}
#enPlay.on{background:#f59e0b;border-color:#f59e0b;color:#111}
.en-sp{flex:1 1 0;min-width:0}
.en-steps{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-bottom:10px}
.en-steps span{display:block;text-align:center;font-size:13px;font-weight:800;padding:7px 2px;border-radius:10px;background:#f1f5f9;color:#64748b;border:2px solid transparent;transition:background .15s,color .15s}
.en-steps span.on{color:#0f172a}
.en-steps span.on[data-i="0"]{background:#bae6fd;border-color:#38bdf8}
.en-steps span.on[data-i="1"]{background:#ddd6fe;border-color:#a78bfa}
.en-steps span.on[data-i="2"]{background:#fed7aa;border-color:#fb923c}
.en-steps span.on[data-i="3"]{background:#e2e8f0;border-color:#94a3b8}
#enWrap{position:relative;border-radius:14px;overflow:hidden;border:1px solid var(--line);background:#0f172a}
#enCv{display:block;width:100%;aspect-ratio:25/18}
.en-note{font-size:14px;color:var(--ink);background:#f1f5f9;border-radius:10px;padding:10px 12px;margin:10px 0 0;font-weight:700;min-height:4.6em;line-height:1.6}
.en-sum{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:12px}
.en-sum div{background:#f8fafc;border:1px solid var(--line);border-radius:12px;padding:10px 4px;text-align:center;min-width:0}
.en-sum b{display:block;font-size:20px;color:#0f172a;font-variant-numeric:tabular-nums;white-space:nowrap}
.en-sum b small{font-size:11.5px}
.en-sum span{font-size:11.5px;color:var(--ink-2);font-weight:700}
.en-order{margin-top:10px;font-size:13.5px;font-weight:700;color:var(--ink-2);display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.en-order[hidden]{display:none}
.en-order i{font-style:normal;display:inline-block;min-width:30px;text-align:center;padding:4px 8px;border-radius:999px;background:#f1f5f9;color:#475569;font-weight:800}
.en-order i.on{background:#fb923c;color:#111}
.en-hint{font-size:12.5px;color:var(--ink-2);margin:4px 0 0}
.en-legend{list-style:none;padding:0;margin:12px 0 0;display:flex;flex-wrap:wrap;gap:6px 14px;font-size:12.5px;color:var(--ink-2)}
.en-legend i{display:inline-block;width:11px;height:11px;border-radius:50%;vertical-align:-1px;margin-right:5px}
@media (max-width:640px){#enCv{aspect-ratio:50/49}.en-sum{grid-template-columns:repeat(2,1fr)}.en-steps span{font-size:12px}.en-note{min-height:6.2em}}
</style>
"""

BODY = r"""
  <section class="panel" id="resultPanel">
    <div class="en-tools">
      <div class="en-seg" id="enMode"><button type="button" data-m="1" class="on">1気筒（大きく）</button><button type="button" data-m="4">直列4気筒</button></div>
      <span class="en-sp"></span>
      <button type="button" id="enPlay">⏸ 一時停止</button>
      <button type="button" id="enStep">⏭ 次の行程へ</button>
    </div>
    <div class="en-steps" id="enSteps"><span data-i="0">① 吸気</span><span data-i="1">② 圧縮</span><span data-i="2">③ 燃焼</span><span data-i="3">④ 排気</span></div>
    <div id="enWrap"><canvas id="enCv" aria-label="4ストロークエンジンの断面。ピストン、クランク軸、バルブ、点火プラグが動くアニメーション"></canvas></div>
    <p class="en-note" id="enNote"></p>
    <div class="en-sum">
      <div><b id="enStroke">吸気</b><span id="enStrokeL">いまの行程</span></div>
      <div><b id="enAng">0<small>°</small></b><span id="enTurn">クランク角（1回転目）</span></div>
      <div><b id="enRpmB">20<small>rpm</small></b><span>回転数（模式的な値）</span></div>
      <div><b id="enBurn">0<small>回</small></b><span>燃焼した回数</span></div>
    </div>
    <div class="en-order" id="enOrder" hidden>点火順序 <i data-c="1">1</i>→<i data-c="3">3</i>→<i data-c="4">4</i>→<i data-c="2">2</i><span>（左から1番・2番・3番・4番の気筒）</span></div>

    <div class="field" style="margin-top:16px"><label>回転数 <span class="hint">（<b id="enRpmV"></b>）</span></label><input type="range" id="enRpm" min="0" max="100" step="1" value="34" aria-label="回転数">
      <p class="en-hint">左へ動かすとゆっくり、右へ動かすと速くなります。動きが見えるようにした模式的な値で、本物のエンジンはもっとずっと速く回ります。</p></div>
    <p class="en-hint" id="enDialHint">右の輪は1サイクル（クランク角0〜720°）を表します。外側の針が1周するあいだに、内側の点（クランク軸の向き）は2周します。</p>
    <ul class="en-legend">
      <li><i style="background:#7dd3fc"></i>混合気（空気＋ガソリン）</li>
      <li><i style="background:#fde047"></i>燃えているガス</li>
      <li><i style="background:#9ca3af"></i>燃えたあとのガス（排気）</li>
    </ul>

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
  const cv = $('enCv'), ctx = cv.getContext('2d');
  const TAU = Math.PI * 2, RAD = Math.PI / 180;
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const mod = (a, n) => ((a % n) + n) % n;
  const ease = t => { t = clamp(t, 0, 1); return t * t * (3 - 2 * t); };
  function rng(s) { s = s >>> 0; return () => { s = (s + 0x6D2B79F5) >>> 0; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }

  // ---------- 寸法（シリンダーの内径を1とした長さ） ----------
  const R = 0.42, L = 1.5, PIN = 0.3, PH = 0.55;      // クランク半径・コンロッド長・ピン〜ピストン上面・ピストンの高さ
  const HEAD = R + L + PIN + 0.16;                    // 燃焼室の天井
  const VX = 0.27, LIFT = 0.14, CAMY = 3.28, CAMB = 0.16, BTOP = 2.86;
  const NAMES = ['吸気', '圧縮', '燃焼', '排気'];
  const COLS = ['#38bdf8', '#a78bfa', '#fb923c', '#94a3b8'];
  const OFFS = { 1: [0], 4: [0, 540, 180, 360] };     // 気筒1〜4のずれ（点火順序 1-3-4-2）
  const NOTES = [
    '① 吸気：吸気バルブ（左）が開き、ピストンが下がります。シリンダーの中が広がるので、空気とガソリンがまざった気体（混合気）が吸いこまれます。',
    '② 圧縮：バルブが2つとも閉じ、ピストンが上がって混合気をぎゅっとおしちぢめます。粒がこみ合っていきます。',
    '③ 燃焼（膨張）：点火プラグの火花で混合気に火がつき、高温・高圧になったガスがピストンを強くおし下げます。力が出るのはこの行程だけです。',
    '④ 排気：排気バルブ（右）が開き、ピストンが上がって、燃えたあとのガスをおし出します。このあと、また吸気にもどります。',
  ];
  // ピストンピンの高さ（クランク中心から）：クランク角とコンロッドの長さから幾何学的に求める
  const pinY = th => R * Math.cos(th * RAD) + Math.sqrt(L * L - Math.pow(R * Math.sin(th * RAD), 2));
  const liftI = th => th > 0 && th < 180 ? Math.sin(th * RAD) : 0;            // 吸気バルブの開き 0〜1
  const liftE = th => th > 540 && th < 720 ? Math.sin((th - 540) * RAD) : 0;  // 排気バルブの開き 0〜1
  function cyl(c) { const py = pinY(c); return { c, si: Math.min(3, Math.floor(c / 180)), py, crown: py + PIN, li: liftI(c), le: liftE(c) }; }

  // ---------- 状態 ----------
  let A = 0, tm = 0, rpm = 20, playing = true, mode = 1, burns = 0, stepTarget = null, fired = [];
  function mk(n, seed) {
    const r = rng(seed), a = [];
    for (let i = 0; i < n; i++) { const v = r(); a.push({ u: (r() * 2 - 1) * .45, v, e: 6 + 150 * (i + r()) / n, x: 548 + 148 * (1 - v), side: r() < .5 ? -1 : 1, lane: (r() * 2 - 1) * .07, w1: 5 + r() * 9, w2: 5 + r() * 9, p1: r() * TAU, p2: r() * TAU }); }
    return a;
  }
  const P1 = mk(96, 11), P4 = mk(40, 23);

  function advance(dt, force) {
    const A0 = A;
    if (stepTarget != null) { A = Math.min(stepTarget, A + 300 * dt); if (A >= stepTarget) stepTarget = null; }
    else if (playing || force) A += rpm * 6 * dt;
    else return;
    tm += dt;
    OFFS[mode].forEach((off, i) => { if (Math.floor((A - off - 360) / 720) > Math.floor((A0 - off - 360) / 720)) { burns++; fired.push(i + 1); if (fired.length > 16) fired.shift(); } });
  }

  // ---------- 描く ----------
  let dpr = 1, W = 600, Hh = 432;
  function size() {
    W = cv.clientWidth || 600; Hh = cv.clientHeight || Math.round(W * .72); dpr = Math.min(2, window.devicePixelRatio || 1);
    const a = Math.round(W * dpr), b = Math.round(Hh * dpr); if (cv.width !== a || cv.height !== b) { cv.width = a; cv.height = b; }
  }
  const PX = () => ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  const UN = (ox, oy, S) => ctx.setTransform(S * dpr, 0, 0, -S * dpr, ox * dpr, oy * dpr);
  const PB = [[-1.05, 2.64], [-VX, 2.72], [-VX, 2.44]];
  function port(s, o, sx) {
    const a = 1 - s, x = a * a * PB[0][0] + 2 * a * s * PB[1][0] + s * s * PB[2][0], y = a * a * PB[0][1] + 2 * a * s * PB[1][1] + s * s * PB[2][1];
    const dx = 2 * a * (PB[1][0] - PB[0][0]) + 2 * s * (PB[2][0] - PB[1][0]), dy = 2 * a * (PB[1][1] - PB[0][1]) + 2 * s * (PB[2][1] - PB[1][1]), d = Math.hypot(dx, dy) || 1;
    return [sx * (x - dy / d * o), y + dx / d * o];
  }
  const RAMP = [[0, [255, 251, 214]], [22, [253, 224, 71]], [70, [251, 146, 60]], [150, [234, 110, 80]], [210, [156, 163, 175]]];
  function burnCol(age) {
    for (let i = 1; i < RAMP.length; i++) if (age <= RAMP[i][0]) { const t = (age - RAMP[i - 1][0]) / (RAMP[i][0] - RAMP[i - 1][0]), a = RAMP[i - 1][1], b = RAMP[i][1]; return `rgb(${a.map((v, k) => Math.round(v + (b[k] - v) * t))})`; }
    return 'rgb(156,163,175)';
  }
  function rr(x, y, w, h, r) { ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r); ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath(); }

  function drawGas(ox, oy, S, st, P, k) {
    PX();
    const c = st.c, hgt = HEAD - st.crown, f = (c % 180) / 180, rad = Math.max(1.5, S * .021);
    const amp = [.035, .03 + .03 * f, .1 - .05 * f, .04][st.si], ay = Math.min(amp, hgt * .3);
    const ci = c >= 540 ? c - 720 : c, ce = c < 180 ? c + 720 : c;
    const dot = (x, y, col, al, glow) => {
      const X = ox + x * S, Y = oy - y * S;
      if (glow) { ctx.globalAlpha = al * .22; ctx.fillStyle = col; ctx.beginPath(); ctx.arc(X, Y, rad * 2.4, 0, TAU); ctx.fill(); }
      ctx.globalAlpha = al; ctx.fillStyle = col; ctx.beginPath(); ctx.arc(X, Y, rad, 0, TAU); ctx.fill();
    };
    for (const p of P) {
      // 吸気ポートを流れてくる
      if (ci >= p.e - 55 && ci < p.e) { const s = (ci - (p.e - 55)) / 55, q = port(s, p.lane, 1); dot(q[0], q[1], '#7dd3fc', Math.min(1, s * 4)); }
      // 排気ポートを出ていく
      if (ce >= p.x && ce < p.x + 55) { const s = 1 - (ce - p.x) / 55, q = port(s, p.lane, -1); dot(q[0], q[1], '#9ca3af', Math.min(1, s * 3)); }
      // シリンダーの中
      if (c >= p.e && c < p.x) {
        let x = p.u + amp * Math.sin(tm * p.w1 + p.p1 + k), y = st.crown + .03 + p.v * (hgt - .06) + ay * Math.cos(tm * p.w2 + p.p2 + k);
        x = clamp(x, -.46, .46); y = clamp(y, st.crown + .025, HEAD - .025);
        if (c < p.e + 32) { const t = ease((c - p.e) / 32), sx = -VX + p.side * .2, sy = HEAD - st.li * LIFT * .6; x = sx + (x - sx) * t; y = sy + (y - sy) * t; }
        if (c > p.x - 26) { const t = ease((c - (p.x - 26)) / 26), ex = VX + p.side * .2, ey = HEAD - st.le * LIFT * .6; x += (ex - x) * t; y += (ey - y) * t; }
        let col = '#7dd3fc', glow = false;
        if (c >= 180 && c < 360) { const t = (c - 180) / 180; col = `rgb(${Math.round(125 + 99 * t)},${Math.round(211 + 31 * t)},${Math.round(252 + 2 * t)})`; }
        if (c >= 360) { const age = c - (360 + Math.hypot(x, HEAD - y) / .7 * 22); if (age >= 0) { col = burnCol(age); glow = age < 150; } else col = 'rgb(224,242,254)'; }
        dot(x, y, col, 1, glow);
      }
    }
    ctx.globalAlpha = 1;
  }

  function cam(x, phi) {
    ctx.beginPath();
    for (let d = -180; d < 180; d += 6) { const r = CAMB + (Math.abs(d) < 45 ? LIFT * Math.cos(2 * d * RAD) : 0), a = (phi + d) * RAD, X = x - Math.sin(a) * r, Y = CAMY - Math.cos(a) * r; d === -180 ? ctx.moveTo(X, Y) : ctx.lineTo(X, Y); }
    ctx.closePath(); ctx.fillStyle = '#cbd5e1'; ctx.fill(); ctx.lineWidth = .02; ctx.strokeStyle = '#475569'; ctx.stroke();
    ctx.fillStyle = '#475569'; ctx.beginPath(); ctx.arc(x, CAMY, .04, 0, TAU); ctx.fill();
  }
  function valve(x, lift, col) {
    const yb = HEAD - .035 - lift * LIFT, top = CAMY - CAMB - lift * LIFT;
    // ばね
    ctx.strokeStyle = '#94a3b8'; ctx.lineWidth = .022; ctx.beginPath(); const n = 6, y0 = BTOP, y1 = top - .07;
    for (let i = 0; i <= n; i++) { const X = x + (i % 2 ? .08 : -.08), Y = y0 + (y1 - y0) * i / n; i ? ctx.lineTo(X, Y) : ctx.moveTo(X, Y); } ctx.stroke();
    // 軸とかさ
    ctx.strokeStyle = '#e2e8f0'; ctx.lineWidth = .05; ctx.beginPath(); ctx.moveTo(x, yb + .05); ctx.lineTo(x, top); ctx.stroke();
    ctx.fillStyle = '#e2e8f0'; ctx.fillRect(x - .11, top - .07, .22, .04);
    ctx.fillStyle = lift > .02 ? col : '#e2e8f0'; ctx.beginPath(); ctx.moveTo(x - .18, yb); ctx.lineTo(x + .18, yb); ctx.lineTo(x + .1, yb + .075); ctx.lineTo(x - .1, yb + .075); ctx.closePath(); ctx.fill();
  }

  function drawCyl(ox, oy, S, c, k, single) {
    const st = cyl(c), th = c * RAD, cx = R * Math.sin(th), cy = R * Math.cos(th);
    UN(ox, oy, S);
    if (!single) { ctx.save(); ctx.beginPath(); ctx.rect(-.66, -.9, 1.32, 4.6); ctx.clip(); }
    // クランクケース・シリンダー
    ctx.fillStyle = '#334155'; ctx.beginPath(); ctx.arc(0, 0, .86, 0, TAU); ctx.fill();
    ctx.fillStyle = '#475569'; ctx.fillRect(-.64, .5, 1.28, HEAD - .5);
    ctx.fillStyle = '#0b1220'; ctx.beginPath(); ctx.arc(0, 0, .74, 0, TAU); ctx.fill(); ctx.fillRect(-.5, .3, 1, HEAD - .3);
    // 燃焼の光
    if (c >= 360 && c < 560) {
      const g = c < 372 ? (c - 360) / 12 : Math.max(0, 1 - (c - 372) / 188);
      const gr = ctx.createRadialGradient(0, HEAD, .02, 0, HEAD, Math.max(.5, (HEAD - st.crown) * 1.15));
      gr.addColorStop(0, `rgba(254,240,138,${.85 * g})`); gr.addColorStop(.45, `rgba(251,146,60,${.6 * g})`); gr.addColorStop(1, `rgba(239,68,68,${.22 * g})`);
      ctx.fillStyle = gr; ctx.fillRect(-.5, st.crown, 1, HEAD - st.crown);
    }
    // ヘッドと吸気・排気の通り道
    ctx.fillStyle = '#64748b'; ctx.fillRect(-.64, HEAD, 1.28, BTOP - HEAD);
    ctx.lineCap = 'butt';
    [[1, '#0c4a6e'], [-1, '#3f3f46']].forEach(([sx, col]) => {
      const path = () => { ctx.beginPath(); ctx.moveTo(sx * PB[0][0], PB[0][1]); ctx.quadraticCurveTo(sx * PB[1][0], PB[1][1], sx * PB[2][0], PB[2][1]); };
      ctx.strokeStyle = '#64748b'; ctx.lineWidth = .32; path(); ctx.stroke();
      ctx.strokeStyle = col; ctx.lineWidth = .22; path(); ctx.stroke();
      ctx.fillStyle = col; ctx.fillRect(sx * -VX - .13, HEAD, .26, .09);
    });
    drawGas(ox, oy, S, st, single ? P1 : P4, k * 1.7);
    UN(ox, oy, S);
    if (!single) { ctx.save(); ctx.beginPath(); ctx.rect(-.66, -.9, 1.32, 4.6); ctx.clip(); }
    // バルブ・カム
    valve(-VX, st.li, '#38bdf8'); valve(VX, st.le, '#fb923c');
    cam(-VX, (c - 90) / 2); cam(VX, (c - 630) / 2);
    // 点火プラグ
    ctx.fillStyle = '#94a3b8'; ctx.fillRect(-.03, HEAD - .04, .06, .1);
    ctx.fillStyle = '#f8fafc'; ctx.fillRect(-.05, HEAD + .06, .1, BTOP - HEAD + .2);
    ctx.fillStyle = '#94a3b8'; ctx.fillRect(-.085, BTOP - .02, .17, .1);
    if (c >= 354 && c < 376) {
      ctx.strokeStyle = '#fef9c3'; ctx.lineWidth = .025; ctx.lineCap = 'round'; ctx.beginPath();
      for (let i = 0; i < 9; i++) { const a = i / 9 * TAU + tm * 9, r = .07 + .08 * Math.abs(Math.sin(tm * 37 + i * 2.1)); ctx.moveTo(0, HEAD - .06); ctx.lineTo(Math.cos(a) * r, HEAD - .06 + Math.sin(a) * r * .7); }
      ctx.stroke(); ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(0, HEAD - .06, .035, 0, TAU); ctx.fill();
    }
    // クランク（つりあいおもり＋うで）
    ctx.fillStyle = '#64748b'; ctx.beginPath(); ctx.moveTo(0, 0);
    for (let d = -52; d <= 52; d += 8) { const a = th + Math.PI + d * RAD; ctx.lineTo(Math.sin(a) * .62, Math.cos(a) * .62); } ctx.closePath(); ctx.fill();
    ctx.strokeStyle = '#64748b'; ctx.lineWidth = .22; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(cx, cy); ctx.stroke();
    // コンロッド
    ctx.strokeStyle = '#94a3b8'; ctx.lineWidth = .15; ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(0, st.py); ctx.stroke();
    ctx.strokeStyle = '#cbd5e1'; ctx.lineWidth = .07; ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(0, st.py); ctx.stroke();
    // ピストン
    const gp = ctx.createLinearGradient(-.49, 0, .49, 0); gp.addColorStop(0, '#94a3b8'); gp.addColorStop(.3, '#e2e8f0'); gp.addColorStop(1, '#94a3b8');
    ctx.fillStyle = gp; ctx.fillRect(-.487, st.crown - PH, .974, PH);
    ctx.fillStyle = '#475569'; ctx.fillRect(-.487, st.crown - .1, .974, .025); ctx.fillRect(-.487, st.crown - .17, .974, .025);
    ctx.beginPath(); ctx.arc(0, st.py, .075, 0, TAU); ctx.fill();
    // ピストンの動く向き（燃焼のときはオレンジ）
    const down = st.si === 0 || st.si === 2, sp = Math.abs(Math.sin(th));
    if (sp > .12) {
      ctx.fillStyle = st.si === 2 ? '#f97316' : '#64748b'; ctx.globalAlpha = Math.min(1, sp * 1.6);
      [-.3, .3].forEach(x => { const y = st.crown - .33, d = down ? -1 : 1; ctx.beginPath(); ctx.moveTo(x - .07, y - d * .05); ctx.lineTo(x + .07, y - d * .05); ctx.lineTo(x, y + d * .08); ctx.closePath(); ctx.fill(); });
      ctx.globalAlpha = 1;
    }
    // クランク軸・クランクピン
    ctx.fillStyle = '#e2e8f0'; ctx.beginPath(); ctx.arc(0, 0, .15, 0, TAU); ctx.fill();
    ctx.fillStyle = '#475569'; ctx.beginPath(); ctx.arc(0, 0, .05, 0, TAU); ctx.fill();
    ctx.fillStyle = '#f1f5f9'; ctx.beginPath(); ctx.arc(cx, cy, .1, 0, TAU); ctx.fill();
    if (!single) { ctx.restore(); ctx.restore(); }
    return st;
  }

  function dial(dx, dy, r, c) {
    PX();
    const si = Math.min(3, Math.floor(c / 180));
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    for (let i = 0; i < 4; i++) {
      const a0 = -Math.PI / 2 + i * Math.PI / 2 + .035, a1 = a0 + Math.PI / 2 - .07, am = (a0 + a1) / 2, on = i === si;
      ctx.beginPath(); ctx.arc(dx, dy, r, a0, a1); ctx.arc(dx, dy, r * .64, a1, a0, true); ctx.closePath();
      ctx.globalAlpha = on ? 1 : .3; ctx.fillStyle = COLS[i]; ctx.fill(); ctx.globalAlpha = 1;
      ctx.fillStyle = on ? '#0f172a' : '#e2e8f0'; ctx.font = `800 ${Math.max(10, Math.round(r * .16))}px system-ui,sans-serif`;
      ctx.fillText(NAMES[i], dx + Math.cos(am) * r * .82, dy + Math.sin(am) * r * .82);
    }
    // 外側の針（720°で1周）
    const a = -Math.PI / 2 + c / 720 * TAU;
    ctx.strokeStyle = '#fff'; ctx.lineWidth = 3; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(dx + Math.cos(a) * r * .6, dy + Math.sin(a) * r * .6); ctx.lineTo(dx + Math.cos(a) * r * 1.07, dy + Math.sin(a) * r * 1.07); ctx.stroke();
    // 内側の点（クランク軸：360°で1周）
    const b = -Math.PI / 2 + c * RAD, ri = r * .44;
    ctx.strokeStyle = 'rgba(226,232,240,.35)'; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.arc(dx, dy, ri, 0, TAU); ctx.stroke();
    ctx.strokeStyle = 'rgba(226,232,240,.6)'; ctx.beginPath(); ctx.moveTo(dx, dy); ctx.lineTo(dx + Math.cos(b) * ri, dy + Math.sin(b) * ri); ctx.stroke();
    ctx.fillStyle = '#f8fafc'; ctx.beginPath(); ctx.arc(dx + Math.cos(b) * ri, dy + Math.sin(b) * ri, Math.max(3.5, r * .055), 0, TAU); ctx.fill();
    ctx.fillStyle = '#0f172a'; ctx.beginPath(); ctx.arc(dx, dy, r * .2, 0, TAU); ctx.fill();
    ctx.fillStyle = '#e2e8f0'; ctx.font = `800 ${Math.max(10, Math.round(r * .15))}px system-ui,sans-serif`; ctx.fillText((c < 360 ? '1' : '2') + '回転目', dx, dy);
  }

  function draw() {
    size(); PX();
    const bg = ctx.createLinearGradient(0, 0, 0, Hh); bg.addColorStop(0, '#111c33'); bg.addColorStop(1, '#0b1220');
    ctx.fillStyle = bg; ctx.fillRect(0, 0, W, Hh);
    const c1 = mod(A, 720);
    if (mode === 1) {
      const S = (Hh - 20) / 4.5, ox = Math.max(1.12 * S + 4, W * .31), oy = 10 + 3.6 * S;
      drawCyl(ox, oy, S, c1, 0, true);
      PX(); ctx.fillStyle = 'rgba(226,232,240,.85)'; ctx.font = `700 ${Math.max(10, Math.round(S * .12))}px system-ui,sans-serif`; ctx.textBaseline = 'top';
      ctx.textAlign = 'left'; ctx.fillText('混合気 →', ox - 1.08 * S, oy - 2.44 * S);
      ctx.textAlign = 'right'; ctx.fillText('→ 排気', ox + 1.08 * S, oy - 2.44 * S);
      const left = ox + 1.1 * S, r = Math.min((W - left - 14) / 2.14, Hh * .3);
      if (r > 34) dial(left + (W - left) / 2, Hh * .5, r, c1);
    } else {
      const S = Math.min((W - 8) / 5.36, (Hh - 46) / 4.5), oy = 8 + 3.6 * S, x0 = W / 2 - 1.95 * S;
      for (let i = 0; i < 4; i++) {
        const ox = x0 + i * 1.3 * S, st = drawCyl(ox, oy, S, mod(A - OFFS[4][i], 720), i, false);
        PX(); const pw = Math.min(1.2 * S, 78), ph = 22, py = oy + .9 * S + 6;
        rr(ox - pw / 2, py, pw, ph, 11); ctx.fillStyle = COLS[st.si]; ctx.fill();
        ctx.fillStyle = '#0f172a'; ctx.font = '800 12px system-ui,sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText((i + 1) + '番 ' + NAMES[st.si], ox, py + ph / 2 + .5);
      }
    }
    ui();
  }

  // ---------- 数字と説明 ----------
  const cache = {};
  function put(id, html) { if (cache[id] !== html) { cache[id] = html; $(id).innerHTML = html; } }
  function ui() {
    const c = mod(A, 720), si = Math.min(3, Math.floor(c / 180));
    put('enStroke', NAMES[si] + (si === 2 ? '<small>（膨張）</small>' : ''));
    put('enStrokeL', mode === 4 ? '1番の気筒の行程' : 'いまの行程');
    put('enAng', Math.floor(c + 1e-6) + '<small>°</small>');
    put('enTurn', (mode === 4 ? '1番の角度' : 'クランク角') + '（' + (c < 360 ? 1 : 2) + '回転目）');
    put('enRpmB', Math.round(rpm) + '<small>rpm</small>');
    put('enBurn', burns + '<small>回</small>');
    put('enNote', (mode === 4 ? '【1番の気筒】' : '') + NOTES[si]);
    if (cache.si !== si) { cache.si = si; document.querySelectorAll('#enSteps span').forEach(el => el.classList.toggle('on', +el.dataset.i === si)); }
    if (mode === 4) { let b = 0; OFFS[4].forEach((off, i) => { const q = mod(A - off, 720); if (q >= 360 && q < 540) b = i + 1; }); if (cache.b !== b) { cache.b = b; document.querySelectorAll('#enOrder i').forEach(el => el.classList.toggle('on', +el.dataset.c === b)); } }
  }

  // ---------- 操作 ----------
  function updPlay() { $('enPlay').textContent = playing ? '⏸ 一時停止' : '▶ 動かす'; $('enPlay').classList.toggle('on', !playing); }
  $('enPlay').addEventListener('click', () => { playing = !playing; stepTarget = null; updPlay(); });
  $('enStep').addEventListener('click', () => { playing = false; updPlay(); const base = stepTarget != null ? stepTarget : A; stepTarget = (Math.floor(base / 180 + 1e-6) + 1) * 180; });
  $('enMode').addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return; mode = +b.dataset.m; burns = 0; fired = []; cache.b = -1;
    document.querySelectorAll('#enMode button').forEach(x => x.classList.toggle('on', x === b));
    $('enOrder').hidden = mode !== 4; $('enDialHint').hidden = mode !== 1;
  });
  const rpmOf = v => 5 * Math.pow(60, v / 100);
  function updRpm() { rpm = rpmOf(+$('enRpm').value); $('enRpmV').textContent = '1分間に約' + Math.round(rpm) + '回転・模式的な値'; }
  $('enRpm').addEventListener('input', updRpm); updRpm();

  // ---------- シェア ----------
  function shareText() { return `4ストロークエンジンのしくみを断面アニメーションで見ました。吸気→圧縮→燃焼→排気の4行程は、クランク軸が2回転するあいだに1回。${mode === 4 ? '直列4気筒の点火順序は1-3-4-2。' : ''}${burns}回燃焼するところまで見ました🚗`; }
  $('shareBtn').addEventListener('click', () => { const u = location.origin + location.pathname; window.open('https://twitter.com/intent/tweet?text=' + encodeURIComponent(shareText() + '\n') + '&url=' + encodeURIComponent(u) + '&hashtags=' + encodeURIComponent('シミュラボ'), '_blank', 'noopener'); });
  $('copyBtn').addEventListener('click', async () => { const b = $('copyBtn'), t = b.textContent; try { await navigator.clipboard.writeText(shareText() + '\n' + location.origin + location.pathname); b.textContent = 'コピーしました'; } catch (e) { b.textContent = 'コピーできませんでした'; } setTimeout(() => { b.textContent = t; }, 1600); });

  // ---------- 動かす ----------
  let tPrev = performance.now();
  function loop(now) { const dt = Math.min(.05, Math.max(0, (now - tPrev) / 1000)); tPrev = now; advance(dt, false); draw(); requestAnimationFrame(loop); }
  updPlay(); draw();
  requestAnimationFrame(loop);

  // 確認用
  window.__t = {
    step(sec) { const n = Math.max(1, Math.round(sec * 60)); for (let i = 0; i < n; i++) advance(1 / 60, true); draw(); },
    setMode(m) { const b = document.querySelector('#enMode button[data-m="' + m + '"]'); if (b) b.click(); },
    setRpm(v) { rpm = v; },
    reset() { A = 0; tm = 0; burns = 0; fired = []; stepTarget = null; draw(); },
    get s() {
      const one = (off, i) => { const st = cyl(mod(A - off, 720)); return { no: i + 1, angle: +st.c.toFixed(2), stroke: NAMES[st.si], intakeOpen: st.li > .01, exhaustOpen: st.le > .01, intakeLift: +st.li.toFixed(3), exhaustLift: +st.le.toFixed(3), pistonTop: +st.crown.toFixed(4), spark: st.c >= 354 && st.c < 376 }; };
      const cs = OFFS[mode].map(one), a = cs[0];
      return { mode, total: +A.toFixed(2), angle: a.angle, turn: a.angle < 360 ? 1 : 2, stroke: a.stroke, intakeOpen: a.intakeOpen, exhaustOpen: a.exhaustOpen, pistonTop: a.pistonTop, spark: a.spark, rpm: +rpm.toFixed(1), burns, playing, stepping: stepTarget != null, fired: fired.slice(), cyls: cs };
    }
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
