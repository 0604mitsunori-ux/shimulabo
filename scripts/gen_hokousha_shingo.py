# -*- coding: utf-8 -*-
"""歩行者と信号のシミュレーター（2026-11-23・リクエスト b735df04cd「人の動きシュミレーター」／df97e908db「信号を好きなところに置いて人を歩かせるシュミレーター」）
   sims/hokousha-shingo/index.html を書き出す（冪等）。 使い方: python scripts/gen_hokousha_shingo.py"""
import html as H, io, json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://shimulabo.com"
SLUG = "hokousha-shingo"
NAME = "歩行者と信号のシミュレーター"
TITLE = "信号を好きな場所に置いて人を歩かせる｜歩行者と信号のシミュレーター（横断歩道・押しボタン信号・人の流れ）｜シミュラボ"
DESC = ("大通りが2本ある町で、信号や横断歩道を好きな場所に置くと、駅・学校・お店へ向かう人たちがどう歩くか、車がどれだけ止まるかを動かして確かめるシミュレーター。"
        "人の数・車の量・青の長さ・押しボタン式・信号を守らない人の割合を変えて、1人あたりの移動時間・待ち時間・車の速さ・ヒヤリハットを比べられます。")
OG_T = "信号を好きな場所に置いて人を歩かせる 歩行者と信号のシミュレーター"
OG_D = "信号や横断歩道を置く場所で、人の移動時間・待ち時間・車の速さ・ヒヤリハットがどう変わるかを動かして比べる。"

FAQ = [
    ("信号はどこに置けますか？", "灰色の道路の上なら、どこでもタップ（クリック）して置けます。上の「🚦 信号」「🦓 横断歩道」「🧹 消す」で、置くものを切り替えてください。横断歩道どうしは5m以上はなして置きます。"),
    ("信号のない横断歩道では、車はどう動きますか？", "道路交通法では、横断歩道を渡ろうとしている人がいるとき、車は手前で止まって道をゆずることになっています。このシミュレーターの車も、渡っている人や渡ろうとして待っている人がいれば止まります。人が多いと車が止まり続けるので、車の流れがどう変わるかも見てください。"),
    ("「押しボタン式」とは何ですか？", "ふだんは車の信号が青のままで、人がボタンを押したときだけ歩行者の青になる信号です。このシミュレーターでは、信号の前で待っている人がいると、ボタンが押されたことにしています。人が少ない場所では、車を止める時間を減らせます。"),
    ("「ヒヤリハット」は何を数えていますか？", "車が、人のために急ブレーキ（強いブレーキ）をかけた回数を、1時間あたりにならして数えています。信号を守らない人の割合を上げたり、見通しの悪い場所に横断歩道を置いたりすると増えます。実際の事故の起こりやすさを表すものではありません。"),
    ("横断歩道がないと、どうなりますか？", "道路の向こう側には行けません。行き先に行けない人は、行ける場所に目的地を変えます。その人数は「行けなかった人」に数えます。"),
    ("人の動きはどうやって決めていますか？", "1人ずつが、行き先までのいちばん近い道（地面を1m四方のマスに分けて計算）を選び、まわりの人とぶつからないように少しずつよけながら歩きます。歩く速さは秒速1.0〜1.6mの間でばらつかせています。"),
]
REL = [("jutai", "🚗", "渋滞は勝手に生まれる"), ("hinan-crowd", "🚪", "群衆避難シミュレーター")]

ARTICLE = """
<h2>このシミュレーターのしくみ</h2>
<p>町には東西にのびる大通りが2本あり、北には駅と会社、まん中にはコンビニとスーパー、南には学校・公園・住宅があります。人は建物から建物へ、行き先を決めて歩きます。道路をわたれるのは、信号か横断歩道を置いた場所だけです。</p>
<ul>
<li><b>人</b>：地面を1m四方のマスに分け、行き先までのいちばん近い道を選んで歩きます。まわりの人とぶつからないように、少しずつよけます（人の流れの研究で使われる「ソーシャルフォース（社会力）モデル」を、とても簡単にしたものです）。</li>
<li><b>車</b>：前の車との間をあけながら、時速40kmまで加速します（車の流れの研究で使われる「IDM（知的運転者モデル）」という考え方です）。赤信号や、横断歩道に人がいるときは止まります。</li>
<li><b>信号</b>：車の青 → 黄色（3秒）→ 全部赤（1秒）→ 歩行者の青（最後の4秒は点滅）→ 全部赤（2秒）をくり返します。押しボタン式では、人が待っているときだけ歩行者の青になります。</li>
</ul>

<h2>ためしてみたいこと</h2>
<ul>
<li><b>信号を駅の近くに寄せる</b>：駅に向かう人は近道できますが、ほかの行き先の人は遠回りになるかもしれません。</li>
<li><b>信号のない横断歩道を増やす</b>：人は近道できますが、人が多いと車がなかなか進めません（このシミュレーターでは、車が3秒以上待つと、人が少しのあいだ待って車を先に通します）。車の量を増やすと、どうなるでしょう。</li>
<li><b>押しボタン式にする</b>：人が少ないときは、車の速さがどれだけ上がるでしょう。</li>
<li><b>歩行者の青を短くする</b>：信号待ちの人がたまって、1回の青でわたりきれなくなることがあります。</li>
<li><b>信号を守らない人を増やす</b>：待ち時間は少し減りますが、車が急ブレーキで止まることが増え（ヒヤリハット）、車の流れも遅くなります。</li>
</ul>
<p>「📋 この配置の結果を記録」を押すと、置き方ごとの結果を表で比べられます。</p>

<h2>本物の信号と横断歩道では</h2>
<p>横断歩道を渡ろうとしている人がいるとき、車は手前で止まらなければなりません（道路交通法 第38条）。信号を置くかどうかは、人や車の量、子どもや高齢の人が多いか、近くに別の信号があるかなどを見て、警察（公安委員会）が決めます。歩行者の青の長さは、ゆっくり歩く人でもわたりきれるように決められています。</p>
<p>このシミュレーターは、とても単純にした町と決まりで動かしています。実際の交差点の安全や渋滞を予測するものではありません。</p>
"""

REFS = [
    "道路交通法 第38条（横断歩道等における歩行者等の優先）",
    "警察庁「信号機設置の指針」",
    "Helbing, D. & Molnár, P. (1995) Social force model for pedestrian dynamics. Physical Review E 51, 4282.",
    "Treiber, M., Hennecke, A. & Helbing, D. (2000) Congested traffic states in empirical observations and microscopic simulations. Physical Review E 62, 1805.（IDM）",
]

STAGE = r"""
<style>
.hs-tools{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px;align-items:center}
.hs-tools button,.hs-seg button{border:1.5px solid var(--line);background:#fff;border-radius:999px;padding:8px 14px;font:inherit;font-size:13.5px;font-weight:800;cursor:pointer;color:var(--ink)}
.hs-tools button.on,.hs-seg button.on{background:#0f766e;border-color:#0f766e;color:#fff}
.hs-tools .sp{flex:1}
.hs-tools .hint{font-size:12px;color:var(--ink-3);font-weight:700}
.hs-seg{display:flex;flex-wrap:wrap;gap:6px}
#hsWrap{position:relative;border-radius:14px;overflow:hidden;background:#dfe9d3;border:1px solid var(--line);touch-action:manipulation}
#hs{display:block;width:100%;aspect-ratio:96/60;cursor:crosshair}
.hs-play{position:absolute;left:10px;top:10px;display:flex;gap:6px}
.hs-play button{border:0;border-radius:999px;background:rgba(15,23,42,.82);color:#fff;font:inherit;font-weight:800;font-size:12.5px;padding:7px 12px;cursor:pointer}
.hs-play button.on{background:#f59e0b;color:#111}
.hs-msg{position:absolute;left:50%;bottom:10px;transform:translateX(-50%);background:rgba(15,23,42,.85);color:#fff;font-size:12.5px;font-weight:700;border-radius:999px;padding:6px 14px;white-space:nowrap;pointer-events:none;opacity:0;transition:opacity .3s}
.hs-msg.show{opacity:1}
.hs-sum{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:12px}
.hs-sum div{background:#f0fdfa;border-radius:12px;padding:10px 6px;text-align:center}
.hs-sum b{display:block;font-size:21px;color:#0f766e;font-variant-numeric:tabular-nums}
.hs-sum b small{font-size:12px}
.hs-sum span{font-size:11.5px;color:var(--ink-2);font-weight:700;line-height:1.4;display:block}
.hs-sum div.warn{background:#fff7ed}.hs-sum div.warn b{color:#c2410c}
.hs-sub{display:flex;flex-wrap:wrap;gap:6px 14px;margin-top:8px;font-size:12.5px;color:var(--ink-2)}
.hs-sub b{color:var(--ink)}
.hs-legend{display:flex;flex-wrap:wrap;gap:6px 12px;margin-top:8px;font-size:12px;color:var(--ink-2)}
.hs-legend i{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:4px;vertical-align:-1px}
.hs-tbl{width:100%;border-collapse:collapse;font-size:13px;margin-top:8px}
.hs-tbl th,.hs-tbl td{border-bottom:1px solid var(--line);padding:7px 6px;text-align:right;white-space:nowrap}
.hs-tbl th:first-child,.hs-tbl td:first-child{text-align:left;white-space:normal}
.hs-tbl th{font-size:11.5px;color:var(--ink-2)}
.hs-tblw{overflow-x:auto}
.hs-note{font-size:13px;color:var(--ink-2);background:#f0fdfa;border-radius:10px;padding:8px 12px;margin:10px 0 0}
@media (max-width:560px){.hs-sum{grid-template-columns:repeat(2,1fr)}.hs-tools button{padding:7px 11px;font-size:12.5px}.hs-tools .hint{width:100%}}
</style>
"""

BODY = r"""
  <section class="panel" id="resultPanel">
    <div class="hs-tools" role="toolbar" aria-label="置くもの">
      <button type="button" data-tool="sig" class="on">🚦 信号</button>
      <button type="button" data-tool="zeb">🦓 横断歩道</button>
      <button type="button" data-tool="del">🧹 消す</button>
      <span class="sp"></span>
      <span class="hint">灰色の道路をタップして置く</span>
    </div>
    <div id="hsWrap">
      <canvas id="hs" aria-label="町の地図。道路をタップすると信号や横断歩道を置けます"></canvas>
      <div class="hs-play"><button type="button" id="hsPause">⏸ 止める</button><button type="button" data-sp="1">×1</button><button type="button" data-sp="3" class="on">×3</button><button type="button" data-sp="8">×8</button></div>
      <div class="hs-msg" id="hsMsg"></div>
    </div>
    <div class="hs-legend" id="hsLegend"></div>
    <div class="hs-sum">
      <div><b id="mTrip">–</b><span>1人の移動時間<br>（平均）</span></div>
      <div><b id="mWait">–</b><span>そのうち<br>信号・車待ち</span></div>
      <div><b id="mCar">–</b><span>車の平均の速さ</span></div>
      <div class="warn"><b id="mNear">–</b><span>ヒヤリハット<br>（1時間あたり）</span></div>
    </div>
    <div class="hs-sub"><span>いま待っている人 <b id="mWaitNow">0</b>人</span><span>止まっている車 <b id="mCarStop">0</b>台</span><span>着いた人 <b id="mDone">0</b>人</span><span>行けなかった人 <b id="mNo">0</b>人</span><span>経過 <b id="mTime">0:00</b></span></div>
    <p class="hs-note" id="hsNote">まずはそのまま眺めてみてください。人は色ごとに行き先がちがいます。</p>

    <h2 style="margin:20px 0 10px;font-size:18px;">置き方を選ぶ</h2>
    <div class="field"><div class="hs-seg" id="hsPreset"></div></div>

    <h2 style="margin:16px 0 10px;font-size:18px;">条件を変える</h2>
    <div class="field"><label>人の数 <span class="hint">（<b id="vPeople">120</b> 人）</span></label><input type="range" id="kPeople" min="20" max="300" step="10" value="120"></div>
    <div class="field"><label>車の量 <span class="hint">（1車線あたり 1分に <b id="vCars">14</b> 台）</span></label><input type="range" id="kCars" min="0" max="30" step="1" value="14"></div>
    <div class="field"><label>信号のタイプ</label><div class="hs-seg" id="hsType"><button type="button" data-v="timer" class="on">⏱ 時間で切りかえ</button><button type="button" data-v="push">👆 押しボタン式</button></div></div>
    <div class="field"><label>歩行者の青の長さ <span class="hint">（<b id="vPed">15</b> 秒）</span></label><input type="range" id="kPed" min="8" max="40" step="1" value="15"></div>
    <div class="field"><label>車の青の長さ <span class="hint">（<b id="vCarG">40</b> 秒。押しボタン式では「最低でもこれだけは青」）</span></label><input type="range" id="kCarG" min="10" max="90" step="5" value="40"></div>
    <div class="field"><label>信号を守らない人 <span class="hint">（<b id="vBad">0</b> %）</span></label><input type="range" id="kBad" min="0" max="30" step="5" value="0"></div>

    <h2 style="margin:18px 0 6px;font-size:18px;">置き方ごとに比べる</h2>
    <p style="font-size:13px;color:var(--ink-2);margin:0 0 6px;">2〜3分（×3なら1分ほど）動かしてから記録すると、数字が落ち着きます。</p>
    <button class="btn btn-ghost" id="hsRec" type="button" style="width:auto;padding:10px 18px;">📋 この配置の結果を記録</button>
    <div class="hs-tblw"><table class="hs-tbl" id="hsTbl" style="display:none"><thead><tr><th>置き方</th><th>移動</th><th>待ち</th><th>車</th><th>ヒヤリ</th></tr></thead><tbody></tbody></table></div>

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
  const W = 96, H = 60;                         // 1マス=1m
  const ROADS = [{ y0: 15, y1: 21 }, { y0: 39, y1: 45 }];
  const LANES = [{ r: 0, y: 16.5, d: 1 }, { r: 0, y: 19.5, d: -1 }, { r: 1, y: 40.5, d: 1 }, { r: 1, y: 43.5, d: -1 }];   // 左側通行
  // 建物（x0,y0,x1,y1, 入口）
  const B = [
    { k: 'eki', e: '🚉', n: '駅', c: '#2563eb', r: [38, 2, 58, 10], door: [48, 11], w: 3 },
    { k: 'kaisha', e: '🏢', n: '会社', c: '#7c3aed', r: [4, 2, 17, 10], door: [11, 11], w: 1.5 },
    { k: 'ie1', e: '🏠', n: '住宅', c: '#db2777', r: [76, 2, 92, 10], door: [84, 11], w: 1 },
    { k: 'conbi', e: '🏪', n: 'コンビニ', c: '#16a34a', r: [6, 26, 18, 34], door: [12, 25], w: 1 },
    { k: 'super', e: '🛒', n: 'スーパー', c: '#ea580c', r: [68, 26, 88, 34], door: [78, 35], w: 1.5 },
    { k: 'gakko', e: '🏫', n: '学校', c: '#ca8a04', r: [6, 50, 26, 58], door: [16, 49], w: 2 },
    { k: 'koen', e: '🌳', n: '公園', c: '#0d9488', r: [42, 50, 62, 58], door: [52, 49], w: 1 },
    { k: 'ie2', e: '🏠', n: '住宅', c: '#be185d', r: [74, 50, 92, 58], door: [83, 49], w: 1.5 },
  ];
  const cv = $('hs'), ctx = cv.getContext('2d');
  const isRoad = (x, y) => ROADS.findIndex(r => y >= r.y0 && y < r.y1);
  const inB = (x, y) => B.findIndex(b => x >= b.r[0] && x < b.r[2] && y >= b.r[1] && y < b.r[3]);

  // ---------- 状態 ----------
  const st = { tool: 'sig', speed: 3, paused: false, people: 120, cars: 14, type: 'timer', pedG: 15, carG: 40, bad: 0 };
  let X = [];          // 横断歩道 {r, x, sig, ph, t, req}
  let P = [], C = [], T = 0, near = [], trips = [], doneN = 0, noN = 0, carSp = 11, records = [];
  let dist = null, crossCell = null;

  function walkGrid() {
    const g = new Uint8Array(W * H);           // 0=歩けない 1=歩ける
    crossCell = new Int16Array(W * H).fill(-1);
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
      let ok = isRoad(x, y) < 0 && inB(x, y) < 0;
      g[y * W + x] = ok ? 1 : 0;
    }
    B.forEach(b => { g[b.door[1] * W + b.door[0]] = 1; });
    X.forEach((c, i) => { const R = ROADS[c.r]; for (let y = R.y0; y < R.y1; y++) for (let x = c.x - 2; x < c.x + 2; x++) if (x >= 0 && x < W) { g[y * W + x] = 1; crossCell[y * W + x] = i; } });
    return g;
  }
  function buildDist() {
    const g = walkGrid();
    dist = B.map(b => {
      const d = new Float64Array(W * H).fill(Infinity);
      const s = b.door[1] * W + b.door[0]; d[s] = 0;
      // 小さな二分ヒープの Dijkstra（8方向）
      const hp = [[0, s]];
      const push = (v) => { hp.push(v); let i = hp.length - 1; while (i > 0) { const p = (i - 1) >> 1; if (hp[p][0] <= hp[i][0]) break; [hp[p], hp[i]] = [hp[i], hp[p]]; i = p; } };
      const pop = () => { const top = hp[0], last = hp.pop(); if (hp.length) { hp[0] = last; let i = 0; for (;;) { const l = 2 * i + 1, r = l + 1; let m = i; if (l < hp.length && hp[l][0] < hp[m][0]) m = l; if (r < hp.length && hp[r][0] < hp[m][0]) m = r; if (m === i) break; [hp[m], hp[i]] = [hp[i], hp[m]]; i = m; } } return top; };
      while (hp.length) {
        const [dc, i] = pop(); if (dc > d[i]) continue;
        const x = i % W, y = (i / W) | 0;
        for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) {
          if (!dx && !dy) continue;
          const nx = x + dx, ny = y + dy; if (nx < 0 || ny < 0 || nx >= W || ny >= H) continue;
          const j = ny * W + nx; if (!g[j]) continue;
          if (dx && dy && (!g[y * W + nx] || !g[ny * W + x])) continue;   // 角を斜めにすり抜けない
          const nd = dc + (dx && dy ? 1.414 : 1);
          if (nd < d[j]) { d[j] = nd; push([nd, j]); }
        }
      }
      return d;
    });
  }

  // ---------- 人 ----------
  const pickDest = (not) => { let tot = 0; B.forEach((b, i) => { if (i !== not) tot += b.w; }); let r = Math.random() * tot; for (let i = 0; i < B.length; i++) { if (i === not) continue; r -= B[i].w; if (r <= 0) return i; } return (not + 1) % B.length; };
  function newTrip(p, from) {
    let to = pickDest(from), tries = 0;
    const cell = Math.floor(p.y) * W + Math.floor(p.x);
    while (!(dist[to][cell] < Infinity) && tries++ < 12) to = pickDest(from);
    p.idle = false;
    if (!(dist[to][cell] < Infinity)) { to = from; p.idle = true; }
    if (tries > 0) noN++;
    p.to = to; p.t0 = T; p.wait = 0; p.hide = 0;
  }
  function spawnPerson(i) {
    const from = Math.floor(Math.random() * B.length), b = B[from];
    const p = { x: b.door[0] + .5 + (Math.random() - .5) * .6, y: b.door[1] + .5 + (Math.random() - .5) * .6, vx: 0, vy: 0, sp: 1 + Math.random() * .6, bad: Math.random() * 100 < st.bad, waiting: false, onX: -1 };
    newTrip(p, from);
    p.hide = Math.random() * 20;            // 少しずつ出てくる
    return p;
  }
  function fitPeople() { while (P.length < st.people) P.push(spawnPerson()); if (P.length > st.people) P.length = st.people; P.forEach(p => { p.bad = Math.random() * 100 < st.bad; }); }

  // ---------- 信号 ----------
  // ph: 'G'(車青) 'Y' 'R1' 'P'(歩青) 'F'(歩点滅) 'R2'
  const carGo = c => !c.sig || c.ph === 'G';
  const pedGo = c => !c.sig || c.ph === 'P';
  function stepSig(c, dt) {
    if (!c.sig) return;
    c.t += dt;
    const dur = { G: st.carG, Y: 3, R1: 1, P: Math.max(2, st.pedG - 4), F: 4, R2: 2 };
    if (c.ph === 'G') {
      if (st.type === 'push') { if (c.req && c.t >= st.carG) { c.ph = 'Y'; c.t = 0; } }
      else if (c.t >= dur.G) { c.ph = 'Y'; c.t = 0; }
      return;
    }
    if (c.t >= dur[c.ph]) { c.t = 0; c.ph = { Y: 'R1', R1: 'P', P: 'F', F: 'R2', R2: 'G' }[c.ph]; if (c.ph === 'P') c.req = false; }
  }

  // ---------- 人の1歩 ----------
  let grid = new Map();
  function hashPeople() { grid.clear(); P.forEach((p, i) => { if (p.hide > 0) return; const k = ((p.x / 2) | 0) + ',' + ((p.y / 2) | 0); let a = grid.get(k); if (!a) grid.set(k, a = []); a.push(i); }); }
  let WG = null;
  const isWalkCell = (cx, cy) => WG[cy * W + cx] === 1;
  function stepPeople(dt) {
    hashPeople();
    X.forEach(c => { c.waitN = 0; c.onN = [0, 0]; });
    for (let i = 0; i < P.length; i++) {
      const p = P[i];
      if (p.hide > 0) { p.hide -= dt; if (p.hide <= 0) p.t0 = T; continue; }
      const d = dist[p.to];
      const cx = Math.floor(p.x), cy = Math.floor(p.y), ci = cy * W + cx;
      // 着いた
      const door = B[p.to].door;
      if (Math.abs(p.x - door[0] - .5) < .9 && Math.abs(p.y - door[1] - .5) < .9) {
        if (!p.idle) { trips.push({ t: T - p.t0, w: p.wait, at: T }); doneN++; }
        const from = p.to; p.x = door[0] + .5; p.y = door[1] + .5; newTrip(p, from); p.hide = 3 + Math.random() * 8; continue;
      }
      if (!(d[ci] < Infinity)) { newTrip(p, p.to); continue; }
      // いちばん近い道（次のマス）
      let best = ci, bd = d[ci];
      for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) {
        const nx = cx + dx, ny = cy + dy; if (nx < 0 || ny < 0 || nx >= W || ny >= H) continue;
        const j = ny * W + nx; if (d[j] < bd - 1e-6) { bd = d[j]; best = j; }
      }
      let tx = best % W + .5, ty = ((best / W) | 0) + .5;
      // 2マス先も見て、なめらかに
      if (best !== ci) {
        const bx = best % W, by = (best / W) | 0; let b2 = best, bd2 = bd;
        for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) { const nx = bx + dx, ny = by + dy; if (nx < 0 || ny < 0 || nx >= W || ny >= H) continue; const j = ny * W + nx; if (d[j] < bd2 - 1e-6) { bd2 = d[j]; b2 = j; } }
        tx = (tx + (b2 % W + .5)) / 2; ty = (ty + (((b2 / W) | 0) + .5)) / 2;
      }
      // 横断歩道に入ってよいか（信号・車）。入るマスごとに1回だけ判定する
      const xi = crossCell[ci], nxi = crossCell[best];
      const memo = {};
      const canEnter = (k) => {
        if (k in memo) return memo[k];
        const c = X[k]; let ok;
        if (c.sig) { if (pedGo(c)) ok = true; else if (p.bad) ok = p.wait > 3 && !carComing(c, 0, .9); else { ok = false; c.req = true; } }
        else ok = !carComing(c, 0) && !(c.carTurn > 0);   // 車が長く待っていたら、しばらく車を先に通す
        return (memo[k] = ok);
      };
      p.waiting = false; p.onX = xi; let wx = -1;
      if (xi < 0 && nxi >= 0 && !canEnter(nxi)) { p.waiting = true; wx = nxi; }
      if (xi >= 0) X[xi].onN[p.y < (ROADS[X[xi].r].y0 + ROADS[X[xi].r].y1) / 2 ? 0 : 1]++;
      let ax = 0, ay = 0;
      if (!p.waiting) { const dx = tx - p.x, dy = ty - p.y, L = Math.hypot(dx, dy) || 1; const v = p.sp * (xi >= 0 ? 1.15 : 1); ax = dx / L * v; ay = dy / L * v; }
      // まわりの人をよける
      const gx = (p.x / 2) | 0, gy = (p.y / 2) | 0;
      for (let oy = -1; oy <= 1; oy++) for (let ox = -1; ox <= 1; ox++) {
        const a = grid.get((gx + ox) + ',' + (gy + oy)); if (!a) continue;
        for (const j of a) { if (j === i) continue; const q = P[j]; const dx = p.x - q.x, dy = p.y - q.y, r2 = dx * dx + dy * dy; if (r2 > .64 || r2 < 1e-6) continue; const r = Math.sqrt(r2), f = (.8 - r) / .8 * 1.6; ax += dx / r * f; ay += dy / r * f; }
      }
      p.vx += (ax - p.vx) * Math.min(1, dt * 5); p.vy += (ay - p.vy) * Math.min(1, dt * 5);
      const vmax = p.sp * 1.3, vv = Math.hypot(p.vx, p.vy); if (vv > vmax) { p.vx *= vmax / vv; p.vy *= vmax / vv; }
      // 壁（歩けないマス）にはぶつかって止まる・すべる
      let nx = p.x + p.vx * dt, ny = p.y + p.vy * dt;
      const okc = (x, y) => { const a = Math.floor(x), b = Math.floor(y); if (a < 0 || b < 0 || a >= W || b >= H) return false; const j = b * W + a; if (!WG[j]) return false;
        if (crossCell[j] >= 0 && crossCell[ci] < 0 && !canEnter(crossCell[j])) { p.waiting = true; wx = crossCell[j]; return false; } return true; };
      if (okc(nx, ny)) { p.x = nx; p.y = ny; } else if (okc(nx, p.y)) p.x = nx; else if (okc(p.x, ny)) p.y = ny;
      if (p.waiting && wx >= 0) { X[wx].waitN++; p.wait += dt; }
    }
  }

  // ---------- 車 ----------
  const L = 4.5, V0 = 11.1, A = 1.6, Bc = 2.5, S0 = 2, TG = 1.3;
  function carComing(c, side, horizon) {    // この横断歩道に、すぐ車が来るか（人が渡り始めてよいか）
    const hz = horizon || 2.2;
    return C.some(k => { const ln = LANES[k.l]; if (ln.r !== c.r) return false; if (side && ((side < 0) !== (ln.y < (ROADS[c.r].y0 + ROADS[c.r].y1) / 2)) && false) return false;
      const front = k.x, gap = ln.d > 0 ? (c.x - 2) - front : front - (c.x + 2);
      return gap > -L && gap < Math.max(4, k.v * hz) && k.v > 1.5; });
  }
  function mustStop(c, k) {
    if (c.sig) {
      if (c.ph === 'G') return c.onN[0] + c.onN[1] > 0;
      if (c.ph === 'Y') { const ln = LANES[k.l], gap = ln.d > 0 ? (c.x - 2) - k.x : k.x - (c.x + 2); return gap > k.v * k.v / (2 * 4) + .5; }
      return true;
    }
    if (c.onN[0] + c.onN[1] > 0) return true;
    if (c.waitN > 0 && !(c.carTurn > 0)) { const ln = LANES[k.l], gap = ln.d > 0 ? (c.x - 2.6) - k.x : k.x - (c.x + 2.6); return gap > k.v * k.v / (2 * 3) - .5; }   // 待っている人には、無理なく止まれるときに止まる
    return false;
  }
  function stepCars(dt) {
    X.forEach(c => { c.cw2 = 0; });
    // 出てくる
    LANES.forEach((ln, li) => {
      if (Math.random() < st.cars / 60 * dt) {
        const x0 = ln.d > 0 ? -30 : W + 30;
        const last = C.filter(k => k.l === li).reduce((m, k) => (ln.d > 0 ? Math.min(m, k.x - L) : Math.max(m, k.x + L)), ln.d > 0 ? 1e9 : -1e9);
        if ((ln.d > 0 ? last - x0 : x0 - last) > 10) C.push({ l: li, x: x0, v: 9, c: ['#ef4444', '#3b82f6', '#f8fafc', '#facc15', '#111827', '#94a3b8', '#22c55e'][Math.floor(Math.random() * 7)], brk: false, nm: {} });
      }
    });
    LANES.forEach((ln, li) => {
      const cs = C.filter(k => k.l === li).sort((a, b) => ln.d > 0 ? b.x - a.x : a.x - b.x);
      cs.forEach((k, idx) => {
        let gap = 1e9, dv = 0;
        if (idx > 0) { const f = cs[idx - 1]; gap = ln.d > 0 ? (f.x - L) - k.x : k.x - (f.x + L); dv = k.v - f.v; }
        // 横断歩道
        X.forEach((c, ci) => {
          if (c.r !== ln.r) return;
          const g = ln.d > 0 ? (c.x - 2.6) - k.x : k.x - (c.x + 2.6);
          if (g < -0.3 || g > 70) return;
          if (mustStop(c, k)) {
            if (g < gap) { gap = Math.max(0.05, g); dv = k.v; }
            if (g < 4 && k.v < .5) { k.wt = (k.wt || 0) + dt; c.cw2 = Math.max(c.cw2, k.wt); }
            const need = k.v * k.v / (2 * Math.max(.3, g));
            if (need > 4.5 && k.v > 3 && k.x > 0 && k.x < W && c.onN[0] + c.onN[1] > 0 && !k.nm[ci]) { k.nm[ci] = 1; near.push(T); }
          } else { if (g > 8) k.nm[ci] = 0; if (g < 4 && k.v < .5 && !c.sig) { k.wt = (k.wt || 0) + dt; c.cw2 = Math.max(c.cw2, k.wt); } }
        });
        const ss = S0 + Math.max(0, k.v * TG + k.v * dv / (2 * Math.sqrt(A * Bc)));
        let a = A * (1 - Math.pow(k.v / V0, 4) - Math.pow(ss / Math.max(gap, .1), 2));
        a = Math.max(-8, a);
        k.brk = a < -1;
        k.v = Math.max(0, k.v + a * dt); if (k.v > 2) k.wt = 0;
        k.x += ln.d * k.v * dt;
      });
    });
    X.forEach(c => { c.cw = c.cw2; if (c.carTurn > 0) c.carTurn -= dt; else if (!c.sig && c.cw > 3) c.carTurn = 8; });
    C = C.filter(k => k.x > -32 && k.x < W + 32);
    if (C.length) { const m = C.reduce((s, k) => s + k.v, 0) / C.length; carSp += (m - carSp) * Math.min(1, dt * .2); } else carSp += (V0 - carSp) * Math.min(1, dt * .2);
  }

  // ---------- 置く・消す ----------
  function hasNear(r, x, d) { return X.findIndex(c => c.r === r && Math.abs(c.x - x) < d); }
  function place(mx, my) {
    const r = isRoad(mx, my);
    if (r < 0) { flash('道路（灰色のところ）をタップしてください'); return; }
    const x = Math.max(6, Math.min(W - 6, Math.round(mx)));
    if (st.tool === 'del') { const i = hasNear(r, x, 4); if (i >= 0) { X.splice(i, 1); changed(); } else flash('ここには何もありません'); return; }
    const i = hasNear(r, x, 5);
    if (i >= 0) { const c = X[i]; const sig = st.tool === 'sig'; if (c.sig !== sig) { c.sig = sig; c.ph = 'G'; c.t = 0; changed(); } else flash('近すぎます（5m以上はなしてください）'); return; }
    if (X.length >= 14) { flash('置けるのは14か所までです'); return; }
    X.push({ r, x, sig: st.tool === 'sig', ph: 'G', t: 0, req: false, waitN: 0, onN: [0, 0], cw: 0 });
    changed();
  }
  function changed() { X.sort((a, b) => a.r - b.r || a.x - b.x); buildDist(); WG = walkGrid(); resetStats(); updPreset(); }
  function resetStats() { trips = []; near = []; doneN = 0; noN = 0; T0 = T; }
  let T0 = 0;
  let msgT = null;
  function flash(s) { const m = $('hsMsg'); m.textContent = s; m.classList.add('show'); clearTimeout(msgT); msgT = setTimeout(() => m.classList.remove('show'), 1800); }

  const PRESETS = [
    ['few', '🚦 信号を2つ', () => [{ r: 0, x: 48, sig: 1 }, { r: 1, x: 48, sig: 1 }]],
    ['zebra', '🦓 横断歩道だけ', () => [{ r: 0, x: 14, sig: 0 }, { r: 0, x: 48, sig: 0 }, { r: 0, x: 82, sig: 0 }, { r: 1, x: 14, sig: 0 }, { r: 1, x: 52, sig: 0 }, { r: 1, x: 82, sig: 0 }]],
    ['many', '🚦 信号をたくさん', () => [14, 34, 54, 74].flatMap(x => [{ r: 0, x, sig: 1 }, { r: 1, x, sig: 1 }])],
    ['edge', '↔ 町のはしにだけ', () => [{ r: 0, x: 6, sig: 1 }, { r: 1, x: 90, sig: 1 }]],
    ['none', '🧹 何もなし', () => []],
  ];
  let presetK = 'few';
  function setPreset(k) { presetK = k; X = PRESETS.find(p => p[0] === k)[2]().map(c => ({ r: c.r, x: c.x, sig: !!c.sig, ph: 'G', t: 0, req: false, waitN: 0, onN: [0, 0] })); buildDist(); WG = walkGrid(); P = []; C = []; fitPeople(); resetStats(); updPreset(); }
  function updPreset() {
    const sig = JSON.stringify(X.map(c => [c.r, c.x, +c.sig]));
    const m = PRESETS.find(p => JSON.stringify(p[2]().map(c => [c.r, c.x, +!!c.sig])) === sig);
    presetK = m ? m[0] : 'custom';
    document.querySelectorAll('#hsPreset button').forEach(b => b.classList.toggle('on', b.dataset.k === presetK));
  }
  function layoutName() { const ns = X.filter(c => c.sig).length, nz = X.length - ns; const m = PRESETS.find(p => p[0] === presetK); return (m ? m[1].replace(/^\S+\s/, '') + '：' : '自分で置いた：') + `信号${ns}・横断歩道${nz}`; }

  // ---------- 描く ----------
  let S = 6, dpr = 1;
  function size() { const w = cv.clientWidth || 600; dpr = Math.min(2, window.devicePixelRatio || 1); cv.width = Math.round(w * dpr); cv.height = Math.round(w * 60 / 96 * dpr); S = cv.width / W; }
  const lit = (on, col) => on ? col : 'rgba(255,255,255,.25)';
  function draw() {
    const c = ctx; c.setTransform(1, 0, 0, 1, 0, 0);
    c.fillStyle = '#dfe9d3'; c.fillRect(0, 0, cv.width, cv.height);
    c.setTransform(S, 0, 0, S, 0, 0);
    // 歩道
    c.fillStyle = '#eceae4'; ROADS.forEach(r => { c.fillRect(0, r.y0 - 2.2, W, 2.2); c.fillRect(0, r.y1, W, 2.2); });
    // 道路
    ROADS.forEach(r => { c.fillStyle = '#4b5563'; c.fillRect(0, r.y0, W, r.y1 - r.y0); c.strokeStyle = '#fde68a'; c.lineWidth = .18; c.setLineDash([2, 1.5]); c.beginPath(); c.moveTo(0, (r.y0 + r.y1) / 2); c.lineTo(W, (r.y0 + r.y1) / 2); c.stroke(); c.setLineDash([]); });
    // 建物
    c.textAlign = 'center'; c.textBaseline = 'middle';
    B.forEach(b => {
      const [x0, y0, x1, y1] = b.r; c.fillStyle = b.c + '22'; c.strokeStyle = b.c; c.lineWidth = .25;
      c.beginPath(); c.roundRect ? c.roundRect(x0, y0, x1 - x0, y1 - y0, 1) : c.rect(x0, y0, x1 - x0, y1 - y0); c.fill(); c.stroke();
      c.fillStyle = '#000'; c.font = `${3.2}px system-ui, sans-serif`; c.fillText(b.e, (x0 + x1) / 2 - (x1 - x0 > 14 ? 3.2 : 0), (y0 + y1) / 2 - (x1 - x0 > 14 ? 0 : 1.2));
      c.fillStyle = b.c; c.font = `bold ${2}px system-ui, sans-serif`; c.fillText(b.n, (x0 + x1) / 2 + (x1 - x0 > 14 ? 3.4 : 0), (y0 + y1) / 2 + (x1 - x0 > 14 ? 0 : 2.2));
      c.fillStyle = b.c; c.fillRect(b.door[0] + .1, b.door[1] + .1, .8, .8);
    });
    // 横断歩道と信号
    X.forEach(x => {
      const R = ROADS[x.r];
      c.fillStyle = '#f8fafc';
      for (let y = R.y0 + .3; y < R.y1 - .2; y += 1) c.fillRect(x.x - 2, y, 4, .55);
      if (x.sig) {
        const pg = x.ph === 'P' || (x.ph === 'F' && (T * 2.5 % 1) < .5), pr = !(x.ph === 'P' || x.ph === 'F');
        [[x.x - 3.2, R.y0 - 1.4], [x.x + 3.2, R.y1 + 1.4]].forEach(([sx, sy]) => {
          c.fillStyle = '#111827'; c.fillRect(sx - .9, sy - 1.4, 1.8, 2.8);
          c.fillStyle = lit(pr, '#ef4444'); c.beginPath(); c.arc(sx, sy - .7, .55, 0, 7); c.fill();
          c.fillStyle = lit(pg, '#22c55e'); c.beginPath(); c.arc(sx, sy + .7, .55, 0, 7); c.fill();
        });
        // 車の信号（道路の中に小さく）
        const cc = x.ph === 'G' ? '#22c55e' : x.ph === 'Y' ? '#f59e0b' : '#ef4444';
        c.fillStyle = cc; c.beginPath(); c.arc(x.x - 2.8, R.y0 + .7, .45, 0, 7); c.fill(); c.beginPath(); c.arc(x.x + 2.8, R.y1 - .7, .45, 0, 7); c.fill();
        if (st.type === 'push' && x.req && x.ph === 'G') { c.fillStyle = '#f59e0b'; c.font = `bold ${1.8}px system-ui`; c.fillText('👆', x.x, R.y0 - 3.4); }
      }
    });
    // 車
    C.forEach(k => {
      const ln = LANES[k.l], x0 = ln.d > 0 ? k.x - L : k.x;
      c.fillStyle = k.c; c.strokeStyle = 'rgba(0,0,0,.35)'; c.lineWidth = .12;
      c.beginPath(); c.roundRect ? c.roundRect(x0, ln.y - .9, L, 1.8, .5) : c.rect(x0, ln.y - .9, L, 1.8); c.fill(); c.stroke();
      c.fillStyle = 'rgba(15,23,42,.55)'; c.fillRect(ln.d > 0 ? x0 + L - 1.6 : x0 + .6, ln.y - .7, 1, 1.4);
      if (k.brk) { c.fillStyle = '#ff2d2d'; const bx = ln.d > 0 ? x0 + .05 : x0 + L - .35; c.fillRect(bx, ln.y - .85, .3, .45); c.fillRect(bx, ln.y + .4, .3, .45); }
    });
    // 人
    const rr = Math.max(.42, 2.2 / S);
    P.forEach(p => {
      if (p.hide > 0) return;
      c.fillStyle = B[p.to].c; c.beginPath(); c.arc(p.x, p.y, rr, 0, 7); c.fill();
      if (p.waiting) { c.strokeStyle = '#111827'; c.lineWidth = .14; c.stroke(); }
      if (p.bad) { c.strokeStyle = '#ef4444'; c.lineWidth = .18; c.stroke(); }
    });
    // 置く場所の目印
    if (hover && !touch) { const r = isRoad(hover.x, hover.y); if (r >= 0) { const R = ROADS[r], x = Math.round(hover.x); c.strokeStyle = st.tool === 'del' ? '#ef4444' : '#fff'; c.lineWidth = .25; c.setLineDash([.8, .6]); c.strokeRect(x - 2, R.y0, 4, R.y1 - R.y0); c.setLineDash([]); } }
  }

  // ---------- 数字 ----------
  const mmss = s => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, '0')}`;
  function stats() {
    const win = trips.filter(t => t.at > T - 240);
    const n = win.length;
    const trip = n ? win.reduce((s, t) => s + t.t, 0) / n : NaN, wait = n ? win.reduce((s, t) => s + t.w, 0) / n : NaN;
    const span = Math.min(T - T0, 600); near = near.filter(t => t > T - 600);
    const nearH = span > 20 ? near.filter(t => t > T - span).length * 3600 / span : NaN;
    return { trip, wait, car: carSp * 3.6, nearH, n };
  }
  let lastUI = 0;
  function ui() {
    const s = stats();
    $('mTrip').innerHTML = isNaN(s.trip) ? '–' : Math.round(s.trip) + '<small>秒</small>';
    $('mWait').innerHTML = isNaN(s.wait) ? '–' : Math.round(s.wait) + '<small>秒</small>';
    $('mCar').innerHTML = st.cars ? Math.round(s.car) + '<small>km/h</small>' : '–';
    $('mNear').innerHTML = isNaN(s.nearH) ? '–' : Math.round(s.nearH) + '<small>回</small>';
    $('mWaitNow').textContent = P.filter(p => p.waiting && p.hide <= 0).length;
    $('mCarStop').textContent = C.filter(k => k.v < .5).length;
    $('mDone').textContent = doneN; $('mNo').textContent = noN; $('mTime').textContent = mmss(T - T0);
    const ns = X.filter(c => c.sig).length, nz = X.length - ns;
    let note;
    if (!X.length) note = '道路をわたれる場所がありません。人は同じ側の行き先にしか行けません。道路をタップして信号や横断歩道を置いてみましょう。';
    else if (!X.some(c => c.r === 0) || !X.some(c => c.r === 1)) note = '片方の大通りには、わたれる場所がありません。そちら側の行き先には行けない人が出ます。';
    else if (nz && s.car < 18 && st.cars >= 10) note = '信号のない横断歩道に人が多く、車が何度も止まっています。信号にすると、どう変わるでしょう。';
    else if (st.bad > 0 && s.nearH > 30) note = '信号を守らない人がいるので、車の急ブレーキ（ヒヤリハット）が増えています。';
    else if (ns && s.wait > s.trip * .35) note = '移動時間のうち、待っている時間が長めです。信号の場所や青の長さを変えてみましょう。';
    else note = `いまの置き方：信号${ns}か所・横断歩道${nz}か所。置く場所を変えて、数字を比べてみましょう。`;
    $('hsNote').textContent = note;
  }

  // ---------- ループ ----------
  let lastT = performance.now(), acc = 0, visible = true;
  function frame(now) {
    const rdt = Math.min(.1, (now - lastT) / 1000); lastT = now;
    if (!st.paused && visible) {
      acc += rdt * st.speed;
      let n = 0;
      while (acc > .05 && n++ < 60) { const dt = .05; T += dt; X.forEach(c => stepSig(c, dt)); stepPeople(dt); stepCars(dt); acc -= dt; }
      if (acc > .5) acc = 0;
    }
    draw();
    if (now - lastUI > 400) { ui(); lastUI = now; }
    requestAnimationFrame(frame);
  }

  // ---------- 操作 ----------
  let hover = null, touch = false;
  const toWorld = e => { const r = cv.getBoundingClientRect(); return { x: (e.clientX - r.left) / r.width * W, y: (e.clientY - r.top) / r.height * H }; };
  cv.addEventListener('pointermove', e => { touch = e.pointerType === 'touch'; hover = toWorld(e); });
  cv.addEventListener('pointerleave', () => { hover = null; });
  cv.addEventListener('pointerdown', e => { touch = e.pointerType === 'touch'; const w = toWorld(e); place(w.x, w.y); try { gtag('event', 'sim_interact', { sim: 'hokousha-shingo', act: st.tool }); } catch (er) {} });
  document.querySelectorAll('.hs-tools [data-tool]').forEach(b => b.onclick = () => { st.tool = b.dataset.tool; document.querySelectorAll('.hs-tools [data-tool]').forEach(x => x.classList.toggle('on', x === b)); });
  document.querySelectorAll('.hs-play [data-sp]').forEach(b => b.onclick = () => { st.speed = +b.dataset.sp; document.querySelectorAll('.hs-play [data-sp]').forEach(x => x.classList.toggle('on', x === b)); });
  $('hsPause').onclick = () => { st.paused = !st.paused; $('hsPause').textContent = st.paused ? '▶ 動かす' : '⏸ 止める'; $('hsPause').classList.toggle('on', st.paused); };
  $('hsPreset').innerHTML = PRESETS.map(p => `<button type="button" data-k="${p[0]}">${p[1]}</button>`).join('');
  document.querySelectorAll('#hsPreset button').forEach(b => b.onclick = () => setPreset(b.dataset.k));
  document.querySelectorAll('#hsType button').forEach(b => b.onclick = () => { st.type = b.dataset.v; document.querySelectorAll('#hsType button').forEach(x => x.classList.toggle('on', x === b)); X.forEach(c => { c.ph = 'G'; c.t = 0; c.req = false; }); resetStats(); });
  const bind = (id, vid, key, f) => { const el = $(id); el.addEventListener('input', () => { st[key] = +el.value; $(vid).textContent = el.value; f && f(); }); };
  bind('kPeople', 'vPeople', 'people', () => { fitPeople(); });
  bind('kCars', 'vCars', 'cars', resetStats);
  bind('kPed', 'vPed', 'pedG', resetStats);
  bind('kCarG', 'vCarG', 'carG', resetStats);
  bind('kBad', 'vBad', 'bad', () => { P.forEach(p => { p.bad = Math.random() * 100 < st.bad; }); resetStats(); });
  $('hsLegend').innerHTML = B.filter((b, i) => B.findIndex(x => x.n === b.n) === i).map(b => `<span><i style="background:${b.c}"></i>${b.e}${b.n}へ</span>`).join('') + '<span>○の黒わく＝待っている人</span>' + '<span style="color:#ef4444">○の赤わく＝信号を守らない人</span>';
  $('hsRec').onclick = () => {
    const s = stats(); if (!s.n) { flash('もう少し動かしてから記録してください'); return; }
    records.unshift({ name: layoutName() + (st.type === 'push' ? '（押しボタン）' : ''), ...s }); records = records.slice(0, 6);
    $('hsTbl').style.display = ''; $('hsTbl').querySelector('tbody').innerHTML = records.map(r => `<tr><td>${r.name}</td><td>${Math.round(r.trip)}秒</td><td>${Math.round(r.wait)}秒</td><td>${st.cars ? Math.round(r.car) + 'km/h' : '–'}</td><td>${isNaN(r.nearH) ? '–' : Math.round(r.nearH) + '回'}</td></tr>`).join('');
    try { gtag('event', 'sim_record', { sim: 'hokousha-shingo' }); } catch (er) {}
  };
  if ('IntersectionObserver' in window) new IntersectionObserver(es => { visible = es[0].isIntersecting; }).observe(cv);
  window.addEventListener('resize', size);
  size(); setPreset('few'); requestAnimationFrame(frame);

  function shareText() { const s = stats(), ns = X.filter(c => c.sig).length, nz = X.length - ns; return isNaN(s.trip) ? '信号を好きな場所に置いて人を歩かせるシミュレーター🚦' : `信号${ns}個・横断歩道${nz}本の町で、1人の移動は平均${Math.round(s.trip)}秒（待ち${Math.round(s.wait)}秒）、車は平均${Math.round(s.car)}km/hでした🚦`; }
  $('shareBtn').addEventListener('click', () => window.open('https://twitter.com/intent/tweet?text=' + encodeURIComponent(shareText()) + '&url=' + encodeURIComponent(location.href) + '&hashtags=' + encodeURIComponent('シミュラボ'), '_blank', 'noopener'));
  $('copyBtn').addEventListener('click', async () => { try { await navigator.clipboard.writeText(shareText() + '\n' + location.href); $('copyBtn').textContent = 'コピーしました ✓'; setTimeout(() => $('copyBtn').textContent = '結果をコピー', 1600); } catch { alert(shareText()); } });
  window.__hs = { get dist() { return dist; }, get WG() { return WG; }, get X() { return X; }, get P() { return P; }, get C() { return C; }, stats, setPreset, place, get T() { return T; }, st,
    step(n) { for (let i = 0; i < n; i++) { const dt = .05; T += dt; X.forEach(c => stepSig(c, dt)); stepPeople(dt); stepCars(dt); } ui(); } };
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

  <nav class="breadcrumb" aria-label="breadcrumb"><a href="../../">ホーム</a><span>›</span>ふしぎ・現象<span>›</span><span class="cur">{esc(NAME)}</span></nav>

  <div class="sim-head">
    <div class="cat">ふしぎ・現象</div>
    <h1>信号を好きな場所に置いて、人を歩かせる<br>歩行者と信号のシミュレーター</h1>
    <p class="lead">大通りが2本ある町で、駅・学校・お店へ向かう人たちが歩いています。灰色の道路をタップすると、信号や横断歩道を好きな場所に置けます。置く場所や青の長さを変えると、人が着くまでの時間、信号待ち、車の速さ、急ブレーキ（ヒヤリハット）がどう変わるか、動かして確かめてください。</p>
    <p class="hs-note">💌 このシミュレーターは、リクエスト「人の動きシュミレーター」「信号を好きなところに置いて人を歩かせるシュミレーター」から作りました。</p>
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
