# -*- coding: utf-8 -*-
"""犬なでシミュレーター（2026-11-24）: ラグの上の犬を、ただなでるだけの癒しページ。
   sims/inu-nadenade/index.html を書き出す（冪等）。 使い方: python -X utf8 scripts/gen_inu_nadenade.py
   絵はすべて canvas の自作（外部画像・外部ライブラリなし）。"""
import html as H, io, json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://shimulabo.com"
SLUG = "inu-nadenade"
NAME = "犬なでシミュレーター"
CAT = "あそぶ・実験"
TITLE = "犬なでシミュレーター｜ただ、犬をなでるだけの癒しページ（毛並み・しっぽ・へそ天）｜シミュラボ"
DESC = ("日の当たる部屋のラグの上にいる犬を、マウスや指でなでるだけのページです。なでた方向に毛並みがねて、頭・あご・背中・おなか・前足・しっぽで反応が変わります。"
        "おなかをなで続けるとへそ天に。犬のタイプ4種と毛色12種、体の大きさ・ふとさも変えられます。")
OG_T = "犬なでシミュレーター ただ、なでるだけ。"
OG_D = "ラグの上の犬を、マウスや指でなでるだけ。なでた所の毛並みが変わり、場所ごとに反応がちがいます。"
H1 = "犬なでシミュレーター<br>ただ、なでるだけ。"
LEAD = "日の当たる部屋で、犬がのんびりしています。マウスや指でなぞって、なでてあげてください。"
NOTE = "🐾 本物の犬は1ぴきずつ好みがちがいます。知らない犬は、かならず飼い主さんに聞いてからさわりましょう。"

FAQ = [
    ("どうやって遊びますか？", "犬の絵をマウスや指でなぞるだけです。なでる場所（頭・あご・背中・おなか・前足・しっぽ）によって、犬の反応が変わります。下のボタンで犬のタイプや毛色も変えられます。"),
    ("へそ天（おなかを見せるポーズ）にするには？", "体の下半分（おなか・わき腹）をなで続けると、ゴロンと横になっておなかを見せます。そのままおなかを速くかくと、後ろ足がカカカッと動きます。しばらくさわらないと、もとの「ふせ」にもどります。"),
    ("なでた回数や時間は、どこに保存されますか？", "このブラウザの中（ローカルストレージ）だけに保存されます。サーバーには送られません。ブラウザの記録を消したり、別の端末で開いたりすると、数字は0にもどります。"),
    ("本物の犬も、同じように反応しますか？", "犬によってちがいます。このページの反応は、よく知られているしぐさをもとに作ったもので、すべての犬に当てはまるわけではありません。本物の犬をなでるときは、その犬の様子をよく見て、いやがっていたらやめましょう。"),
]
REL = [("neko-nemuri", "🐱", "猫が寝てる時間シミュレーター"), ("pet-age", "🐶", "犬・猫の年齢 人間換算シミュレーター"), ("purupuru-jelly", "🍮", "ぷるぷるゼリー")]

ARTICLE = """
<h2>犬はどこをなでられるのが好き？</h2>
<p>好きな場所は、犬によってちがいます。<b>あごの下・胸・肩のあたり</b>をなでられるのを好む犬が多いと言われています。</p>
<p>反対に、頭の上からいきなり手を出すと、こわがる犬がいます。足先やしっぽは、さわられるのが苦手な犬も少なくありません。このページの犬が、前足をそっと引っこめたり、しっぽをさわるとふり返ったりするのは、そのためです。</p>
<p>このページの反応は、よく知られているしぐさをもとに作ったものです。すべての犬に当てはまるわけではありません。</p>

<h2>しっぽを振る＝うれしい、とはかぎらない</h2>
<p>しっぽを振るのは、気持ちが高ぶっているサインだと言われています。うれしいときだけでなく、きんちょうしているときや、けいかいしているときにも振ることがあります。</p>
<p>しっぽだけで決めつけず、<b>耳の向き・体のかたさ・口もと・目つきなど、体全体の様子とあわせて見る</b>ことが大切です。体がやわらかく、力がぬけているなら、リラックスしていることが多いと言われています。</p>

<h2>足が勝手に動くのはなぜ？</h2>
<p>おなかやわき腹をかかれると、後ろ足がカカカッと動く犬がいます。これは「引っかき反射」と呼ばれるもので、皮ふへの刺激に体が自動的に反応して、足が動くと言われています。犬が自分で動かそうとしているわけではありません。</p>
<p>足が動くからといって、かならず喜んでいるとはかぎりません。いやがる様子があれば、やめてあげましょう。</p>

<h2>はじめての犬へのあいさつの仕方</h2>
<ul>
<li><b>まず飼い主さんに聞く</b>：「さわってもいいですか」と聞いて、いいと言われてからにします。</li>
<li><b>いきなり近づかない</b>：走って近づいたり、大きな声を出したりしないで、犬のほうから近づいてくるのを待ちます。</li>
<li><b>手は低い位置から、ゆっくり</b>：頭の上からではなく、下のほうからゆっくり手を出して、においをかいでもらいます。</li>
<li><b>なでるのは、あごの下や胸、体の横から</b>：やさしく、ゆっくりなでます。</li>
<li><b>いやがったら、やめる</b>：体をかたくする、顔をそむける、はなれていく、などの様子が見えたら、さわるのをやめます。</li>
<li><b>食べているとき・寝ているときは、さわらない</b>：びっくりさせてしまうことがあります。</li>
</ul>

<h2>このページでためしてみたいこと</h2>
<ul>
<li><b>頭をなでる</b>：目を細めて、耳を後ろにねかせ、手に頭を押しつけてきます。</li>
<li><b>あごの下をなでる</b>：あごを上げて、うっとりします。</li>
<li><b>背中をなでる</b>：しっぽの振り方が速くなります。</li>
<li><b>おなか・わき腹をなで続ける</b>：ゴロンと横になります。速くかくと、後ろ足が動きます。</li>
<li><b>毛の流れと反対になでる</b>：毛が立って、なでたあとがしばらく残ります。</li>
<li><b>しばらく何もしない</b>：こちらを見たり、首をかしげたり、前足で「もっと」とさいそくしたりします。</li>
</ul>
"""

REFS = [
    "環境省「動物の愛護と適切な管理」（環境省のウェブサイト）",
]

STAGE = r"""
<style>
#inuWrap{position:relative;border-radius:16px;overflow:hidden;border:1px solid var(--line);background:#f7e6c4}
#inuCv{display:block;width:100%;aspect-ratio:3/2;touch-action:none;-webkit-user-select:none;user-select:none;-webkit-touch-callout:none}
#inuWrap.in-on #inuCv{cursor:none}
.in-mood{position:absolute;left:50%;bottom:10px;transform:translateX(-50%);background:rgba(255,255,255,.86);color:#5b4636;font-size:12.5px;font-weight:700;border-radius:999px;padding:5px 14px;max-width:92%;text-align:center;pointer-events:none;white-space:nowrap;box-shadow:0 1px 4px rgba(90,60,30,.12)}
.in-sum{display:grid;grid-template-columns:1fr 1fr 1.5fr;gap:8px;margin-top:12px}
.in-sum>div{background:#fff7ec;border-radius:12px;padding:10px 6px;text-align:center}
.in-sum b{display:block;font-size:20px;color:#b45f1f;font-variant-numeric:tabular-nums}
.in-sum span{font-size:11.5px;color:var(--ink-2);font-weight:700}
.in-sum span b{display:inline;font-size:13px}
.in-bar{height:14px;border-radius:999px;background:#f3e2cf;overflow:hidden;margin:6px 6px 7px}
.in-bar i{display:block;height:100%;width:0;border-radius:999px;background:linear-gradient(90deg,#ffb86b,#ff7f9c);transition:width .25s}
.in-h{margin:20px 0 10px;font-size:17px}
.in-row{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.in-seg{display:flex;flex-wrap:wrap;gap:6px}
.in-seg button,.in-rand{border:1.5px solid var(--line);background:#fff;border-radius:999px;padding:8px 13px;font:inherit;font-size:13.5px;font-weight:800;cursor:pointer;color:var(--ink)}
.in-seg button.on{background:#b45f1f;border-color:#b45f1f;color:#fff}
.in-rand{background:#fff7ec;border-color:#f0c99a}
.in-sw{display:flex;flex-wrap:wrap;gap:8px;margin-top:4px}
.in-sw button{width:38px;height:38px;border-radius:50%;border:2px solid #fff;box-shadow:0 0 0 1.5px var(--line);cursor:pointer;padding:0}
.in-sw button.on{box-shadow:0 0 0 3px #b45f1f}
.in-cols{display:grid;grid-template-columns:1fr 1fr;gap:6px 22px;margin-top:12px}
.in-note{font-size:13.5px;color:var(--ink);background:#fff7ec;border-radius:10px;padding:9px 12px;margin:10px 0 0}
@media (max-width:640px){#inuCv{aspect-ratio:4/5}.in-cols{grid-template-columns:1fr}.in-sum{grid-template-columns:1fr 1fr}.in-sum>div.in-happy{grid-column:1/3}.in-mood{font-size:11.5px}}
</style>
"""

BODY = r"""
  <section class="panel" id="resultPanel">
    <div id="inuWrap">
      <canvas id="inuCv" aria-label="日の当たる部屋のラグの上で、ふせをしている犬の絵。なぞると、なでることができます"></canvas>
      <div class="in-mood" id="inuMood" aria-live="polite">ゆっくり、しっぽを振っています</div>
    </div>
    <div class="in-sum">
      <div><b id="inuCnt">0</b><span>なでた回数</span></div>
      <div><b id="inuTime">0秒</b><span>なでた時間</span></div>
      <div class="in-happy"><div class="in-bar"><i id="inuBar"></i></div><span>うれしさ <b id="inuHappy">0</b></span></div>
    </div>

    <h2 class="in-h">犬をえらぶ</h2>
    <div class="in-row">
      <div class="in-seg" id="inuTypes"></div>
      <button type="button" class="in-rand" id="inuRand">🎲 おまかせ</button>
    </div>
    <div class="field" style="margin-top:12px"><label>毛色 <span class="hint">（<b id="inuCoatName"></b>）</span></label><div class="in-sw" id="inuCoats"></div></div>
    <div class="in-cols">
      <div class="field"><label>体の大きさ <span class="hint">（<b id="inuSizeV"></b>）</span></label><input type="range" id="inuSize" min="70" max="100" step="1" value="88"></div>
      <div class="field"><label>ふとさ <span class="hint">（<b id="inuFatV"></b>）</span></label><input type="range" id="inuFat" min="82" max="130" step="1" value="100"></div>
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
  'use strict';
  const $ = id => document.getElementById(id);
  const cv = $('inuCv'), ctx = cv.getContext('2d');
  const TAU = Math.PI * 2, clamp = (v, a, b) => Math.max(a, Math.min(b, v)), lerp = (a, b, t) => a + (b - a) * t;
  function rng(s) { s = s >>> 0; return () => { s = (s + 0x6D2B79F5) >>> 0; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
  const R01 = rng(20261124);

  // =====================================================================
  //  色・形の定義（ここを変えると見た目が変わる）
  // =====================================================================
  const KEY = 'shimulabo_inunade_v1';
  // 見た目のタイプ: ear=耳 / tail=しっぽ / hair=毛の長さ / len=胴の長さ / leg=足の長さ / head=頭の大きさ / snout=鼻先 / cheek=ほおの毛 / nb,nh=毛の本数（体・頭）
  const TYPES = {
    tachi: { name: '立ち耳・巻きしっぽ', ear: 'point', tail: 'curl', hair: 13, len: 1, leg: 1, head: 1, snout: 1, cheek: 1, nb: 840, nh: 360 },
    tare: { name: 'たれ耳', ear: 'drop', tail: 'long', hair: 12, len: 1.03, leg: 1.1, head: 1.02, snout: 1.16, cheek: 0, nb: 800, nh: 340 },
    fuwa: { name: 'ふわふわ長毛', ear: 'small', tail: 'plume', hair: 21, len: .9, leg: .8, head: 1.04, snout: .84, cheek: 1.5, nb: 980, nh: 460 },
    tansoku: { name: '短足・胴長', ear: 'big', tail: 'short', hair: 12, len: 1.15, leg: .55, head: .98, snout: 1.04, cheek: .5, nb: 880, nh: 350 },
  };
  const TYPE_IDS = Object.keys(TYPES);
  // しっぽ: n=節の数 / seg=節の長さ / a0=ふせの向き / a1=へそ天の向き / curl=巻き / r0,r1=太さ / lag=しなり / amp=振れ幅 / stiff=根もとのかたさ
  const TAILS = {
    curl: { n: 9, seg: 15, a0: -1.3, a1: -.55, curl: -.5, r0: 17, r1: 11, lag: .1, amp: .5, stiff: .9, fluff: 1 },
    long: { n: 9, seg: 19, a0: -.5, a1: .08, curl: -.07, r0: 13, r1: 6, lag: .42, amp: 1, stiff: .35 },
    plume: { n: 8, seg: 18, a0: -1.2, a1: -.35, curl: -.2, r0: 21, r1: 12, lag: .3, amp: .8, stiff: .5, plume: 1, fluff: 1 },
    short: { n: 4, seg: 14, a0: -.8, a1: -.1, curl: -.1, r0: 15, r1: 11, lag: .3, amp: 1.1, stiff: .6 },
  };
  // 毛色: base=地の色 / light=おなか・口もとの色 / patch=ぶちの色 / pat=もよう（solid=一色, ura=うら白, tan=茶のポイント, bi=2色, patch=ぶち）
  const COATS = [
    { id: 'akacha', name: '赤茶', base: '#dc9150', light: '#fdf1df', pat: 'ura' },
    { id: 'kurocha', name: '黒＋茶', base: '#342e2d', light: '#cf9257', pat: 'tan' },
    { id: 'shiro', name: '白', base: '#fbf7ef', light: '#ffffff', pat: 'solid' },
    { id: 'cream', name: 'クリーム', base: '#f0d9ae', light: '#fdf4e0', pat: 'ura' },
    { id: 'cha', name: '茶', base: '#a8703f', light: '#cfa272', pat: 'solid' },
    { id: 'kin', name: '金', base: '#e3b25a', light: '#f6dfae', pat: 'solid' },
    { id: 'gray', name: 'グレー', base: '#9b9ea5', light: '#d9dbe0', pat: 'solid' },
    { id: 'choco', name: 'チョコ', base: '#6d4631', light: '#946a4d', pat: 'solid' },
    { id: 'buchi', name: '白黒ぶち', base: '#fbf7ef', light: '#ffffff', patch: '#37312f', pat: 'patch' },
    { id: 'chashiro', name: '茶白', base: '#c88548', light: '#fdf8ef', pat: 'bi' },
    { id: 'goma', name: 'ごま', base: '#a88c6c', light: '#f3e6d1', pat: 'ura', fleck: 1 },
    { id: 'kuro', name: '黒', base: '#302b2c', light: '#5c5453', pat: 'solid' },
  ];
  // 部屋の色
  const SC = { wall1: '#fdf5e1', wall2: '#f8e6c3', floor1: '#dfae76', floor2: '#c78f56', rug: '#84b6ad', rug2: '#a6cec6', rugEdge: '#f7eedb', sky1: '#bfe3f7', sky2: '#eaf6fb', leaf: '#6fae7b', pot: '#d98b63' };
  // 顔の部品の色
  const FEAT = { dark: '#2b1d18', nose: '#231815', tongue: '#ff8fa6', mouth: '#7c2f39', heart: '#ff6f91' };
  // 体の形（胴のだ円を1としたときの、胴・むね・おしりのだ円 [中心u, 中心v, 半径u, 半径v]）
  const BODY_E = [[0, 0, 1, 1], [-.66, -.04, .46, 1.04], [.6, .1, .52, .94]];
  const PATCHES = [[-.12, -.6, .36, .44], [.66, -.05, .3, .5], [.12, .62, .22, .3]];
  const FACE0 = -8;   // 顔の向き（少し左向き）

  // ---------- 色の計算 ----------
  const hex = h => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
  const mix = (a, b, t) => { const A = hex(a), B = hex(b); return '#' + A.map((v, i) => Math.round(v + (B[i] - v) * t).toString(16).padStart(2, '0')).join(''); };
  const lum = h => { const c = hex(h); return (c[0] * .299 + c[1] * .587 + c[2] * .114) / 255; };
  const rgba = (h, a) => { const c = hex(h); return `rgba(${c[0]},${c[1]},${c[2]},${a})`; };

  // ---------- 行列 ----------
  const mat = (tx, ty, rot, sc) => { const c = Math.cos(rot) * sc, s = Math.sin(rot) * sc; return [c, s, -s, c, tx, ty]; };
  const mul = (m, n) => [m[0] * n[0] + m[2] * n[1], m[1] * n[0] + m[3] * n[1], m[0] * n[2] + m[2] * n[3], m[1] * n[2] + m[3] * n[3], m[0] * n[4] + m[2] * n[5] + m[4], m[1] * n[4] + m[3] * n[5] + m[5]];
  const app = (m, x, y) => [m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5]];
  const inv = m => { const d = m[0] * m[3] - m[1] * m[2]; return [m[3] / d, -m[1] / d, -m[2] / d, m[0] / d, (m[2] * m[5] - m[3] * m[4]) / d, (m[1] * m[4] - m[0] * m[5]) / d]; };
  let dpr = 1, W = 600, H = 480, portrait = false;
  const useM = m => ctx.setTransform(dpr * m[0], dpr * m[1], dpr * m[2], dpr * m[3], dpr * m[4], dpr * m[5]);

  // =====================================================================
  //  状態
  // =====================================================================
  const cfg = { type: 'tachi', coat: 'akacha', size: .88, fat: 1 };
  const st = { t: 0, happy: 15, count: 0, sec: 0, idle: 0, bellyT: 0, sleepyT: 0, breathPh: 0, wagPh: 0, wagHz: 1, kickPh: 0, kickHold: 0, nextBlink: 2, blinkT: 0, evt: null, evtN: 0, nextEvt: 0,
    reg: null, hover: null, petOn: false, petBody: false, hairFrac: 1, fps: 0, work: 0, mood: '', heartT: 0, sparkT: 0, zT: 0, dirty: false, saveT: 0 };
  const pet = { qx: 0, qy: 0, hx: 0, hy: 0, ux: 0, uy: 0, hux: 0, huy: 0 };
  const hand = { x: 0, y: 0, px: 0, py: 0, vx: 0, vy: 0, over: false, was: false, down: false, mouse: true, a: 0, rot: 0 };
  const stroke = { on: false, len: 0, dx: 0, dy: 0 };
  // バネ（x=今の値, t=めざす値, k=強さ, c=ねばり）
  const SP = {};
  const spr = (n, k, c, x) => { SP[n] = { x: x || 0, v: 0, t: x || 0, k, c }; };
  spr('eye', 260, 26); spr('smile', 120, 18); spr('ear', 130, 13); spr('perk', 120, 14); spr('headX', 150, 15); spr('headY', 150, 15); spr('headRot', 100, 12);
  spr('faceX', 140, 17, FACE0); spr('faceY', 140, 17); spr('chin', 100, 14); spr('mouth', 120, 15); spr('tongue', 80, 11); spr('yawn', 60, 12);
  spr('roll', 46, 12); spr('kick', 200, 20); spr('paw', 170, 17); spr('beg', 110, 13); spr('wagAmp', 60, 12, .25); spr('tuck', 100, 14);
  spr('squash', 220, 16); spr('sleepy', 14, 7.5); spr('earSw', 90, 8); spr('handP', 200, 20);
  function stepSprings(dt) { for (const n in SP) { const s = SP[n]; s.v += (s.k * (s.t - s.x) - s.c * s.v) * dt; s.x += s.v * dt; } }
  const coat = () => COATS.find(c => c.id === cfg.coat) || COATS[0];

  // ---------- 色の組（毛色が変わったら作り直す） ----------
  let C = {};
  function buildPalette() {
    const k = coat(), dk = lum(k.base) < .3, sh = dk ? '#000000' : (lum(k.base) > .85 ? '#a8957a' : '#5a3418');
    const under = k.pat === 'solid' ? mix(k.base, k.light, .6) : k.light;
    C = {
      base: k.base, under, patch: k.patch || k.base, dark: dk,
      line: dk ? mix(k.base, '#ffffff', .2) : mix(k.base, '#4a2c14', lum(k.base) > .85 ? .3 : .45),
      hi: mix(k.base, '#ffffff', dk ? .1 : .25), lo: mix(k.base, sh, dk ? .3 : .2), far: mix(k.base, sh, dk ? .28 : .17),
      ear: k.pat === 'patch' ? k.patch : mix(k.base, sh, dk ? .22 : .2), earIn: dk ? '#7a5a58' : '#f4bfb2',
      paw: k.pat === 'solid' ? mix(k.base, k.light, .4) : (k.pat === 'patch' ? k.base : k.light),
      belly: k.pat === 'solid' ? mix(k.base, '#ffffff', dk ? .18 : .32) : (k.pat === 'tan' ? mix(k.light, '#ffffff', .2) : k.light),
      muzzle: k.pat === 'solid' ? mix(k.base, k.light, .8) : k.light,
    };
    C.mline = lum(C.muzzle) < .35 ? '#120e0e' : FEAT.dark;
    C.mrim = mix(C.muzzle, lum(C.muzzle) < .35 ? '#000000' : '#6b4020', .22);
    // 毛の線の色: [地, うら, ぶち] × 明るさ5段
    C.lv = [k.base, under, C.patch].map(c => { const d = lum(c) < .3, s = d ? '#000000' : (lum(c) > .85 ? '#a8957a' : '#6b4020'); return [-1, -.5, 0, .5, 1].map(v => v < 0 ? mix(c, s, -v * (d ? .32 : .18)) : mix(c, '#ffffff', v * (d ? .17 : .24))); });
  }

  // =====================================================================
  //  毛（体と頭に生やす短い線。なでた向きを lx,ly に覚える）
  // =====================================================================
  let bodyHairs = [], headHairs = [];
  const inE = (u, v, e) => { const a = (u - e[0]) / e[2], b = (v - e[1]) / e[3]; return a * a + b * b < 1; };
  const inBody = (u, v) => inE(u, v, BODY_E[0]) || inE(u, v, BODY_E[1]) || inE(u, v, BODY_E[2]);
  function headInside(x, y, T) {
    if ((x / 104) ** 2 + (y / 94) ** 2 < 1) return true;
    if (T.cheek > 0) { const rr = 30 + 10 * T.cheek; for (const sd of [-1, 1]) if ((x - sd * 74) ** 2 + (y - 36) ** 2 < rr * rr) return true; }
    if (T.ear === 'small') { for (let i = 0; i < 14; i++) { const a = i / 14 * TAU + .22, cx = Math.cos(a) * 100, cy = Math.sin(a) * 88 + 6; if ((x - cx) ** 2 + (y - cy) ** 2 < 900) return true; } }
    return false;
  }
  function makeHairs() {
    const T = TYPES[cfg.type], R = rng(977 + TYPE_IDS.indexOf(cfg.type) * 131);
    bodyHairs = []; headHairs = [];
    let guard = 0;
    while (bodyHairs.length < T.nb && guard++ < 20000) {
      const u = (R() * 2 - 1) * 1.16, v = (R() * 2 - 1) * 1.1;
      if (!inBody(u * 1.1, v * 1.13)) continue;
      let a = .18 + .5 * v + (u < -.5 ? (-.5 - u) * 2.4 : 0) + (u > .75 ? (u - .75) * 1.5 : 0) + (R() - .5) * .5;
      bodyHairs.push({ u, v, rx: Math.cos(a), ry: Math.sin(a), len: T.hair * (.8 + R() * .5) * (u < -.5 ? 1.15 : 1) * (v > .72 ? .6 : 1), j: R() * 2 - 1, rnd: R(), lx: 0, ly: 0, s: 0, tone: 0, belly: false, patch: false, jj: 0 });
    }
    guard = 0;
    while (headHairs.length < T.nh && guard++ < 20000) {
      const x = (R() * 2 - 1) * 132, y = (R() * 2 - 1) * 122;
      if (!headInside(x * 1.11, y * 1.11, T)) continue;
      if (((x - FACE0 * 1.2) / (40 * T.snout)) ** 2 + ((y - 31) / (29 * T.snout)) ** 2 < 1) continue;   // 口もとには生やさない
      const d = Math.hypot(x / 104, y / 94);
      let a = Math.atan2(y - 6, x - FACE0) + (R() - .5) * .5; if (y < -20 && Math.abs(x) < 60) a = lerp(a, -Math.PI / 2, .35);
      headHairs.push({ x, y, rx: Math.cos(a), ry: Math.sin(a), len: T.hair * (.6 + R() * .4) * (d > .72 ? 1.15 : .9), j: R() * 2 - 1, rnd: R(), lx: 0, ly: 0, s: 0, tone: 0, jj: 0 });
    }
    assignTones();
  }
  function assignTones() {
    const k = coat();
    for (const h of bodyHairs) {
      h.patch = k.pat === 'patch' && PATCHES.some(q => inE(h.u, h.v, q));
      h.belly = inE(h.u, h.v, [.05, .1, .75, .62]);
      const tuft = k.pat !== 'solid' && k.pat !== 'patch' && inE(h.u, h.v, [-.8, .32, .3, .64]);
      h.tone = h.patch ? 2 : (h.v > .5 + h.j * .08 || tuft) ? 1 : 0;
      h.jj = h.j + (k.fleck && h.rnd < .32 && h.tone === 0 ? -1.5 : 0);
    }
    for (const h of headHairs) {
      const cheek = (k.pat === 'ura' || k.pat === 'bi' || k.pat === 'tan') && (((Math.abs(h.x - FACE0) - 64) / 46) ** 2 + ((h.y - 46) / 44) ** 2 < 1);
      const blaze = k.pat === 'bi' && h.y < 22 && Math.abs(h.x - FACE0) < 10 + (h.y + 100) * .13;
      const pt = k.pat === 'patch' && ((h.x - 52) / 46) ** 2 + ((h.y + 34) / 54) ** 2 < 1;
      h.tone = pt ? 2 : (cheek || blaze) ? 1 : 0;
      h.jj = h.j + (k.fleck && h.rnd < .32 && h.tone === 0 ? -1.5 : 0);
    }
  }
  function petHairs(list, isBody, hx, hy, ux, uy, speed, dt, g) {
    const n = Math.floor(list.length * st.hairFrac), R2 = 62 * 62, gain = clamp(speed / 280, .2, 1.2) * dt * 21, b = g.b;
    for (let i = 0; i < n; i++) {
      const h = list[i]; let x, y;
      if (isBody) { x = b.cx + b.cs * h.u * b.rx - b.sn * h.v * b.ry; y = b.cy + b.sn * h.u * b.rx + b.cs * h.v * b.ry; } else { x = h.x; y = h.y; }
      const dx = x - hx, dy = y - hy, d2 = dx * dx + dy * dy; if (d2 > R2) continue;
      const k = Math.min(1, gain * (1 - d2 / R2));
      h.lx += (ux * 1.2 - h.lx) * k; h.ly += (uy * 1.2 - h.ly) * k;
      h.s += ((ux * h.rx + uy * h.ry > 0 ? .95 : -.85) - h.s) * k;
    }
  }
  function relaxHairs(dt) {
    const f = Math.exp(-dt / 7);
    for (const h of bodyHairs) { h.lx *= f; h.ly *= f; h.s *= f; }
    for (const h of headHairs) { h.lx *= f; h.ly *= f; h.s *= f; }
  }

  // =====================================================================
  //  姿勢（部品の位置をまとめて計算）  r=0: ふせ / r=1: へそ天
  // =====================================================================
  let G = null;
  function geom() {
    const T = TYPES[cfg.type], F = cfg.fat, L = T.len * (1 + (F - 1) * .12), lg = T.leg;
    const r0 = clamp(SP.roll.x, 0, 1), r = r0 * r0 * (3 - 2 * r0), hop = Math.sin(r0 * Math.PI);
    const S = Math.min(W / (portrait ? 606 : 640), H / 470) * cfg.size;
    const br = Math.sin(st.breathPh * TAU), sq = SP.squash.x;
    const ry = lerp(100, 86, r) * F * (1 + .024 * br) * (1 - .05 * sq) * (1 + .06 * hop);
    const rx = lerp(195, 203, r) * L * (1 + .012 * sq);
    const rot = lerp(0, -.04, r) + Math.sin(st.wagPh) * SP.wagAmp.x * .014 * (1 - r);
    const cs = Math.cos(rot), sn = Math.sin(rot);
    const b = { cx: lerp(22, 34, r), cy: -ry - hop * 12, rx, ry, cs, sn, rot };
    const B = (u, v) => [b.cx + cs * u * rx - sn * v * ry, b.cy + sn * u * rx + cs * v * ry];
    const MD = [S, 0, 0, S, W * .5 + (10 + r * 16) * S, H * (portrait ? .8 : .85)];
    // 頭
    const hs = T.head * (1 + (.88 - cfg.size) * .45), sl = clamp(SP.sleepy.x, 0, 1);
    const hx = lerp(-172 * L, -186 * L, r) + SP.headX.x;
    const hy = lerp(-118 * F - 80 * hs, -90 * hs, r) + SP.headY.x + sl * 30 * (1 - r) - 2.4 * br * (1 - r) - SP.chin.x * 7 - hop * 16;
    const hrot = lerp(0, -1.95, r) + SP.headRot.x;
    const MH = mul(MD, mat(hx, hy, hrot, hs));
    // 足（s=つけ根, p=足先）
    const leg = (f, ro, w) => ({ sx: lerp(f[0], ro[0], r), sy: lerp(f[1], ro[1], r), px: lerp(f[2], ro[2], r), py: lerp(f[3], ro[3], r), w: w * (.88 + F * .12), bx: 0, by: 0, pa: 0 });
    const FN = leg([-112 * L, -30, -226 * L - 26 * lg, -17], [-110 * L, -128 * F, -150 * L, -150 * F - 80 * lg], 40);
    const FF = leg([-90 * L, -50, -192 * L - 26 * lg, -37], [-64 * L, -138 * F, -76 * L, -160 * F - 84 * lg], 36);
    const HN = leg([136 * L, -30, 52 * L + (1 - lg) * 36, -15], [128 * L, -118 * F, 184 * L, -140 * F - 76 * lg], 40);
    const HF = leg([150 * L, -62, 118 * L, -44], [96 * L, -130 * F, 112 * L, -152 * F - 82 * lg], 36);
    const pp = SP.paw.x; FN.px = lerp(FN.px, FN.sx, pp * .42); FN.py = lerp(FN.py, FN.sy, pp * .22) - pp * 5; FF.px = lerp(FF.px, FF.sx, pp * .16);
    const bg = SP.beg.x * (1 - r); FN.px += bg * (16 + Math.sin(st.t * 11) * 10); FN.py -= bg * (54 + Math.cos(st.t * 11) * 12);
    const kk = SP.kick.x, ks = Math.sin(st.kickPh);
    HN.px += kk * ks * 24 * (1 - r); HN.py -= kk * Math.abs(ks) * 10 * (1 - r);
    const swing = (l, a) => { const dx = l.px - l.sx, dy = l.py - l.sy, c = Math.cos(a), s = Math.sin(a); l.px = l.sx + dx * c - dy * s; l.py = l.sy + dx * s + dy * c; };
    swing(HN, kk * ks * .5 * r); swing(HF, kk * Math.sin(st.kickPh + 1.3) * .36 * r);
    const sway = Math.sin(st.t * 1.4) * .05 * r; swing(FN, sway); swing(FF, -sway * .8); swing(HN, sway * .6); swing(HF, -sway * .5);
    for (const l of [FN, FF, HN, HF]) l.pa = Math.atan2(l.py - l.sy, l.px - l.sx);
    FN.pa -= .95 * r; FF.pa -= .85 * r; HN.pa += .75 * r; HF.pa += .65 * r;
    FN.bx = -10 * r; FF.bx = -8 * r; HN.bx = 10 * r; HF.bx = 8 * r;
    // しっぽ
    const TT = TAILS[T.tail], tb = B(lerp(TT.fluff && !TT.plume ? .8 : .93, .97, r), lerp(TT.fluff && !TT.plume ? -.72 : -.36, .3, r)), amp = SP.wagAmp.x * TT.amp, tail = [];
    const N = TT.n * 3, a0 = lerp(TT.a0, TT.a1, r) + SP.tuck.x * .55;
    let x = tb[0], y = tb[1];
    for (let i = 0; i <= N; i++) {
      const k = i / N, ang = a0 + TT.curl * i / 3 + amp * Math.sin(st.wagPh - i / 3 * TT.lag) * (TT.stiff + (1 - TT.stiff) * k);
      const rad = (TT.plume ? TT.r0 * (.7 + .65 * Math.sin(Math.PI * Math.min(1, k * 1.15))) : lerp(TT.r0, TT.r1, k)) * (.88 + F * .12);
      tail.push({ x, y, r: rad, a: ang });
      x += Math.cos(ang) * TT.seg / 3; y += Math.sin(ang) * TT.seg / 3;
    }
    return { S, r, r0, b, B, MD, MDi: inv(MD), MH, MHi: inv(MH), hx, hy, hs, hrot, legs: { FN, FF, HN, HF }, tail, T, F, L };
  }

  // ---------- どこをさわっているか ----------
  function segDist(px, py, l, t0) {
    const dx = l.px - l.sx, dy = l.py - l.sy, d2 = dx * dx + dy * dy || 1;
    const t = clamp(((px - l.sx) * dx + (py - l.sy) * dy) / d2, t0, 1.12);
    return Math.hypot(px - (l.sx + dx * t), py - (l.sy + dy * t));
  }
  function hit(x, y) {
    const g = G, h = app(g.MHi, x, y);
    if (headInside(h[0], h[1], g.T) || (Math.abs(h[0]) < 100 && h[1] < 0 && h[1] > -150 && g.T.ear !== 'drop' && Math.abs(Math.abs(h[0]) - 62) < 40 + (h[1] + 150) * .2)) return h[1] > 40 ? 'chin' : 'head';
    if (g.T.ear === 'drop' && Math.abs(h[0]) < 130 && Math.abs(h[0]) > 60 && h[1] > -90 && h[1] < 72) return 'head';
    const q = app(g.MDi, x, y), L = g.legs;
    if (segDist(q[0], q[1], L.FN, .35) < L.FN.w * .5 + 9 || segDist(q[0], q[1], L.FF, .5) < L.FF.w * .5 + 7) return 'paw';
    for (let i = 3; i < g.tail.length; i += 2) { const n = g.tail[i]; if ((q[0] - n.x) ** 2 + (q[1] - n.y) ** 2 < (n.r + 9) ** 2) return 'tail'; }
    if (segDist(q[0], q[1], L.HN, .2) < L.HN.w * .5 + 8 || (g.r > .5 && segDist(q[0], q[1], L.HF, .2) < L.HF.w * .5 + 8)) return 'belly';
    const b = g.b, dx = q[0] - b.cx, dy = q[1] - b.cy, u = (dx * b.cs + dy * b.sn) / b.rx, v = (-dx * b.sn + dy * b.cs) / b.ry;
    if (!inBody(u, v)) return null;
    if (g.r > .5) return 'belly';
    if (u < -.5 && v < .4) return 'chin';
    return v < -.1 ? 'back' : 'belly';
  }
  function anchor(region) {
    const g = G; let p;
    if (region === 'head') return app(g.MH, 0, -42);
    if (region === 'chin') return app(g.MH, SP.faceX.x, 68);
    if (region === 'back') p = g.r > .5 ? g.B(.05, -.3) : g.B(.12, -.6);
    else if (region === 'belly') p = g.r > .5 ? g.B(.05, .05) : g.B(.12, .42);
    else if (region === 'paw') p = [lerp(g.legs.FN.sx, g.legs.FN.px, .9), lerp(g.legs.FN.sy, g.legs.FN.py, .9)];
    else { const n = g.tail[Math.floor(g.tail.length * .55)]; p = [n.x, n.y]; }
    return app(g.MD, p[0], p[1]);
  }

  // =====================================================================
  //  動き（1コマ分）
  // =====================================================================
  const parts = [];
  function emit(type, x, y) { if (parts.length > 26) return; parts.push({ type, x, y, vx: (R01() - .5) * 26, vy: -(26 + R01() * 26), life: 0, max: type === 'spark' ? .7 : 1.7, size: type === 'spark' ? 5 + R01() * 5 : 9 + R01() * 6, rot: (R01() - .5) * .6 }); }
  function handVel(dt) {
    if (hand.over) {
      if (!hand.was) { hand.px = hand.x; hand.py = hand.y; hand.vx = hand.vy = 0; }
      const S = G ? G.S : 1, k = Math.min(1, dt * 20);
      hand.vx += ((hand.x - hand.px) / dt / S - hand.vx) * k; hand.vy += ((hand.y - hand.py) / dt / S - hand.vy) * k;
      hand.px = hand.x; hand.py = hand.y;
    } else hand.vx = hand.vy = 0;
    hand.was = hand.over;
  }
  function update(dt) {
    st.t += dt;
    const g = G = geom(), rolled = SP.roll.t > .5;
    const speed = Math.hypot(hand.vx, hand.vy), ux = speed > 1 ? hand.vx / speed : 0, uy = speed > 1 ? hand.vy / speed : 0;
    const hov = hand.over ? hit(hand.x, hand.y) : null;
    const petting = !!hov && (speed > 22 || hand.down);
    const reg = petting ? hov : null;
    st.hover = hov; st.reg = reg; st.petOn = petting; st.petBody = petting && (reg === 'back' || reg === 'belly' || reg === 'chin');
    const q = app(g.MDi, hand.x, hand.y), hl = app(g.MHi, hand.x, hand.y);
    // --- 毛 ---
    relaxHairs(dt);
    if (petting) {
      const c = Math.cos(-g.hrot), s = Math.sin(-g.hrot);
      pet.qx = q[0]; pet.qy = q[1]; pet.hx = hl[0]; pet.hy = hl[1]; pet.ux = ux; pet.uy = uy; pet.hux = ux * c - uy * s; pet.huy = ux * s + uy * c;
      if (speed > 22) { petHairs(bodyHairs, true, q[0], q[1], ux, uy, speed, dt, g); petHairs(headHairs, false, hl[0], hl[1], pet.hux, pet.huy, speed, dt, g); }
    }
    // --- なでた回数・時間 ---
    if (petting) {
      if (!stroke.on) { stroke.on = true; stroke.len = 0; stroke.dx = ux; stroke.dy = uy; }
      stroke.len += speed * dt;
      const dot = ux * stroke.dx + uy * stroke.dy;
      if ((stroke.len > 26 && dot < -.25 && speed > 30) || stroke.len > 260) { st.count++; st.dirty = true; stroke.len = 0; stroke.dx = ux; stroke.dy = uy; }
      else if (speed > 30) { stroke.dx = lerp(stroke.dx, ux, Math.min(1, dt * 6)); stroke.dy = lerp(stroke.dy, uy, Math.min(1, dt * 6)); }
      if (speed > 22) { st.sec += dt; st.dirty = true; }
      st.idle = 0; st.evt = null; SP.beg.t = 0; SP.yawn.t = 0;
    } else {
      if (stroke.on) { if (stroke.len > 26) { st.count++; st.dirty = true; } stroke.on = false; }
      st.idle += dt;
    }
    // --- 場所ごとの反応（めざす値を決める） ---
    const hp = st.happy / 100;
    let tEye = 0, tSmile = 0, tEar = 0, tPerk = 0, tHX = 0, tHY = 0, tHR = 0, tFX = rolled ? 0 : FACE0, tFY = 0, tChin = 0, tPaw = 0, tTuck = 0, tSq = 0, gain = 0;
    let wagHz = .9 + hp * 3.3, wagA = .22 + hp * .55, fast = false;
    if (reg === 'head') {
      tEye = .74; tSmile = 1; tEar = 1; gain = 6.5;
      const dx = q[0] - g.hx, dy = q[1] - g.hy, d = Math.hypot(dx, dy) || 1; tHX = dx / d * 11; tHY = dy / d * 11 - 3; tHR = clamp(dx / 90, -1, 1) * .12 * (rolled ? 0 : 1);
    } else if (reg === 'chin') {
      tChin = 1; tEye = .9; tSmile = 1; tEar = .45; gain = 8; tHR = -.05;
    } else if (reg === 'back') {
      wagHz *= 1.75; wagA = wagA * 1.3 + .12; tEye = .3; tSmile = .7; tEar = .25; gain = 6; tSq = .6;
    } else if (reg === 'belly') {
      gain = rolled ? 8.5 : 6.5; tEye = rolled ? .85 : .35; tSmile = 1; tEar = .5; tSq = .8; wagHz *= 1.2;
      if (!rolled) st.bellyT += dt;
      if (speed > 430) st.kickHold = .28;
    } else if (reg === 'paw') {
      tPaw = 1; tPerk = 1; gain = 1.5; tFX = FACE0 - 16; tFY = 5; tHR = -.08; tHY = 6;
    } else if (reg === 'tail') {
      tTuck = 1; tPerk = 1; gain = 1; tFX = 28; tHX = 16; tHR = .13; wagA *= .3;
    }
    if (!reg) st.bellyT = Math.max(0, st.bellyT - dt * .4);
    if (!rolled && st.bellyT > 2.2) { SP.roll.t = 1; st.bellyT = 0; for (let i = 0; i < 3; i++) emit('heart', ...app(g.MH, (i - 1) * 50, -120)); }
    if (rolled && st.idle > 6.5) SP.roll.t = 0;
    st.kickHold = Math.max(0, st.kickHold - dt); fast = st.kickHold > 0;
    SP.kick.t = fast ? 1 : 0; st.kickPh += dt * 62;
    // うれしさ
    if (petting) st.happy = clamp(st.happy + gain * dt * (speed > 22 ? 1 : .35), 0, 100);
    else if (st.idle > 3) st.happy = Math.max(0, st.happy - 1.1 * dt);
    // とろん（うれしさが高いまま、ゆっくりなで続けると眠くなる）
    if (petting && st.happy > 88 && speed < 460 && gain >= 6) st.sleepyT += dt * .14;
    else if (petting && speed > 620) st.sleepyT -= dt * .35;
    else if (!petting) st.sleepyT -= dt * .06;
    st.sleepyT = clamp(st.sleepyT, 0, 1); SP.sleepy.t = st.sleepyT;
    const sl = clamp(SP.sleepy.x, 0, 1);
    // さわられていない時のしぐさ
    if (!petting && !rolled && st.idle > 7 && !st.evt && st.t > st.nextEvt && sl < .4) {
      const type = ['tilt', 'beg', 'tilt', 'yawn'][st.evtN++ % 4];
      st.evt = { type, t0: st.t, dur: type === 'yawn' ? 2.4 : type === 'beg' ? 2.8 : 2.5, side: R01() < .5 ? -1 : 1 };
    }
    let tBeg = 0, tYawn = 0;
    if (st.evt) {
      const p = (st.t - st.evt.t0) / st.evt.dur;
      if (p >= 1) { st.evt = null; st.nextEvt = st.t + 3 + R01() * 3; }
      else {
        const env = p < .2 ? p / .2 : p > .8 ? (1 - p) / .2 : 1;
        if (st.evt.type === 'tilt') { tHR = st.evt.side * .3 * env; tPerk = 1; tFX = 0; }
        else if (st.evt.type === 'beg') { tBeg = env > .3 ? 1 : 0; tPerk = 1; tFX = -4; tHR = -.06; }
        else { tYawn = Math.sin(Math.PI * p); tEye = tYawn > .3 ? 1 : 0; tHR = -.07 * tYawn; tHY = -6 * tYawn; }
      }
    }
    if (!petting && st.idle > 4 && !st.evt && sl < .4) { tPerk = Math.max(tPerk, .7); tFX = rolled ? 0 : FACE0 * .3; tHY -= 4; }
    // 目で手を追う
    if (hand.over && !reg && hov == null && hand.mouse) { tFX += clamp((q[0] - g.hx) / 60, -1, 1) * 7; tFY += clamp((q[1] - g.hy) / 60, -1, 1) * 4; }
    // まばたき
    if (st.t > st.nextBlink) { st.blinkT = .13; st.nextBlink = st.t + 2.2 + R01() * 3.5; }
    if (st.blinkT > 0) { st.blinkT -= dt; tEye = Math.max(tEye, 1); }
    // 眠い
    tEye = Math.max(tEye, sl * 1.02); if (sl > .55 && tEye >= .95) tSmile = Math.min(tSmile, .2);
    wagHz *= 1 - .6 * sl; wagA *= 1 - .45 * sl; tEar = Math.max(tEar, sl * .5);
    // 口と舌
    const pant = st.happy > 55 ? Math.sin(st.t * 7) * .07 : 0;
    SP.mouth.t = (st.happy > 35 ? clamp((st.happy - 35) / 30, 0, 1) * .62 + pant : 0) * (1 - sl * .9) + (reg === 'belly' && rolled ? .15 : 0);
    SP.tongue.t = (st.happy > 55 ? clamp((st.happy - 55) / 25, 0, 1) : 0) * (1 - sl * .75);
    // めざす値をバネへ
    SP.eye.t = tEye; SP.smile.t = tSmile; SP.ear.t = tEar - tPerk * .15; SP.perk.t = tPerk; SP.headX.t = tHX; SP.headY.t = tHY; SP.headRot.t = tHR;
    SP.faceX.t = tFX; SP.faceY.t = tFY; SP.chin.t = tChin; SP.paw.t = tPaw; SP.tuck.t = tTuck; SP.squash.t = tSq; SP.beg.t = tBeg; SP.yawn.t = tYawn;
    SP.wagAmp.t = wagA; SP.earSw.t = SP.headRot.x * 40 + SP.headX.v * .06; SP.handP.t = petting ? 1 : 0;
    st.wagHz += (wagHz - st.wagHz) * Math.min(1, dt * 4); st.wagPh += dt * st.wagHz * TAU;
    st.breathPh += dt * (sl > .5 ? .2 : st.happy > 60 && !sl ? .55 : .3);
    stepSprings(dt);
    // ハート・キラキラ・zzz
    if (petting && st.happy > 60 && sl < .6) { st.heartT -= dt; if (st.heartT <= 0) { st.heartT = 1.5 - hp * .7 + R01() * .5; emit('heart', ...app(g.MH, (R01() - .5) * 150, -100 - R01() * 30)); } }
    if (petting && speed > 160 && reg !== 'paw' && reg !== 'tail') { st.sparkT -= dt; if (st.sparkT <= 0) { st.sparkT = .28 + R01() * .3; emit('spark', hand.x + (R01() - .5) * 50 * g.S, hand.y + (R01() - .5) * 40 * g.S); } }
    if (sl > .75) { st.zT -= dt; if (st.zT <= 0) { st.zT = 1.5; emit('z', ...app(g.MH, 70, -70)); } }
    for (let i = parts.length - 1; i >= 0; i--) { const p = parts[i]; p.life += dt; p.x += p.vx * dt * g.S; p.y += p.vy * dt * g.S; p.vy *= 1 - dt * .6; if (p.life > p.max) parts.splice(i, 1); }
    // 手の向き
    hand.a += ((hand.over ? 1 : 0) - hand.a) * Math.min(1, dt * 12);
    hand.rot += (clamp(hand.vx / 900, -.5, .5) - hand.rot) * Math.min(1, dt * 8);
    st.mood = moodText(reg, rolled, sl, fast);
  }
  function moodText(reg, rolled, sl, fast) {
    if (sl > .65) return 'とろん… ねむくなってきました';
    if (rolled && fast) return '足が勝手に、カカカッ！';
    if (reg === 'head') return '目を細めて、手に頭を押しつけています';
    if (reg === 'chin') return 'あごを上げて、うっとりしています';
    if (reg === 'back') return 'しっぽをぶんぶん振っています';
    if (reg === 'belly') return rolled ? 'へそ天！ すっかり安心しています' : (fast ? '後ろ足がピクピク…' : 'わき腹、きもちいい… ゴロンしそう');
    if (reg === 'paw') return '前足は、ちょっとだけ引っこめます';
    if (reg === 'tail') return '「しっぽ？」と、ふり返りました';
    if (rolled) return 'おなかを見せて、待っています';
    if (st.evt) return st.evt.type === 'tilt' ? '首をかしげています' : st.evt.type === 'beg' ? '前足で「もっと」と、さいそく中' : 'ふわぁ… あくび';
    if (st.idle > 4) return 'こちらを見ています';
    return st.happy > 60 ? 'しっぽを大きく振っています' : 'ゆっくり、しっぽを振っています';
  }

  // =====================================================================
  //  絵
  // =====================================================================
  const bgc = document.createElement('canvas'); let bgOK = false;
  const rr = (c, x, y, w, h, r) => { c.beginPath(); c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r); c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath(); };
  function size() {
    const w = cv.clientWidth || 600, h = cv.clientHeight || Math.round(w * .8);
    dpr = Math.min(2, window.devicePixelRatio || 1);
    const pw = Math.round(w * dpr), ph = Math.round(h * dpr);
    if (cv.width !== pw || cv.height !== ph || !bgOK) { cv.width = pw; cv.height = ph; W = w; H = h; portrait = H > W; drawBg(); bgOK = true; }
  }
  function drawBg() {
    bgc.width = cv.width; bgc.height = cv.height;
    const b = bgc.getContext('2d'); b.setTransform(dpr, 0, 0, dpr, 0, 0);
    const fy = H * (portrait ? .5 : .47), S0 = Math.min(W / 640, H / 470), gy = H * (portrait ? .8 : .85);
    let g = b.createLinearGradient(0, 0, 0, fy); g.addColorStop(0, SC.wall1); g.addColorStop(1, SC.wall2); b.fillStyle = g; b.fillRect(0, 0, W, fy);
    // かべのもよう（うすい水玉）
    b.fillStyle = 'rgba(214,170,110,.10)'; for (let y = 14; y < fy - 12; y += 30) for (let x = ((y / 30) % 2) * 17 + 10; x < W; x += 34) { b.beginPath(); b.arc(x, y, 2.2, 0, TAU); b.fill(); }
    // まど
    const wx = W * (portrait ? .08 : .06), wy = H * .055, ww = W * (portrait ? .42 : .27), wh = fy * .68;
    b.fillStyle = 'rgba(160,110,60,.12)'; rr(b, wx - 6, wy - 4, ww + 16, wh + 16, 9); b.fill();
    b.fillStyle = '#fffdf8'; rr(b, wx - 8, wy - 8, ww + 16, wh + 16, 9); b.fill();
    b.save(); b.beginPath(); b.rect(wx, wy, ww, wh); b.clip();
    g = b.createLinearGradient(0, wy, 0, wy + wh); g.addColorStop(0, SC.sky1); g.addColorStop(1, SC.sky2); b.fillStyle = g; b.fillRect(wx, wy, ww, wh);
    b.fillStyle = 'rgba(255,255,255,.92)'; for (const c of [[.26, .3, .1], [.38, .25, .13], [.5, .31, .1], [.74, .52, .08], [.84, .5, .1]]) { b.beginPath(); b.arc(wx + ww * c[0], wy + wh * c[1], ww * c[2], 0, TAU); b.fill(); }
    b.fillStyle = '#b9dcae'; b.beginPath(); b.ellipse(wx + ww * .25, wy + wh * 1.08, ww * .5, wh * .3, 0, 0, TAU); b.fill();
    b.fillStyle = '#a3d19c'; b.beginPath(); b.ellipse(wx + ww * .82, wy + wh * 1.1, ww * .45, wh * .27, 0, 0, TAU); b.fill();
    g = b.createRadialGradient(wx + ww * .9, wy, 0, wx + ww * .9, wy, ww * .8); g.addColorStop(0, 'rgba(255,246,200,.95)'); g.addColorStop(1, 'rgba(255,246,200,0)'); b.fillStyle = g; b.fillRect(wx, wy, ww, wh);
    b.restore();
    b.fillStyle = '#fffdf8'; b.fillRect(wx + ww / 2 - 3, wy, 6, wh); b.fillRect(wx, wy + wh * .5 - 3, ww, 6);
    b.fillStyle = '#f3e4c8'; rr(b, wx - 15, wy + wh + 7, ww + 30, 9, 4); b.fill();
    // かべの絵（骨のマーク）
    const px = W * (portrait ? .68 : .56), py = H * .09, pw = W * (portrait ? .2 : .12), ph = pw * .8;
    b.fillStyle = 'rgba(160,110,60,.14)'; rr(b, px + 3, py + 4, pw, ph, 5); b.fill();
    b.fillStyle = '#c99a66'; rr(b, px, py, pw, ph, 5); b.fill(); b.fillStyle = '#fff9ec'; rr(b, px + 6, py + 6, pw - 12, ph - 12, 3); b.fill();
    b.save(); b.translate(px + pw / 2, py + ph / 2); b.rotate(-.35); const bl = pw * .2, br = pw * .075; b.fillStyle = '#e8c9a0';
    b.fillRect(-bl, -br * .7, bl * 2, br * 1.4); for (const sx of [-1, 1]) for (const sy of [-1, 1]) { b.beginPath(); b.arc(sx * bl, sy * br * .8, br, 0, TAU); b.fill(); } b.restore();
    // ゆか
    g = b.createLinearGradient(0, fy, 0, H); g.addColorStop(0, SC.floor1); g.addColorStop(1, SC.floor2); b.fillStyle = g; b.fillRect(0, fy, W, H - fy);
    b.strokeStyle = 'rgba(120,70,30,.17)'; b.lineWidth = 1;
    const rows = []; for (let i = 0; i <= 8; i++) rows.push(fy + (H - fy) * Math.pow(i / 8, 1.5));
    for (let i = 1; i < 8; i++) { b.beginPath(); b.moveTo(0, rows[i]); b.lineTo(W, rows[i]); b.stroke(); }
    const rb = rng(7); for (let i = 0; i < 8; i++) { const n = 2 + (i % 2); for (let k = 0; k < n; k++) { const x = (k + rb()) / n * W; b.beginPath(); b.moveTo(x, rows[i]); b.lineTo(x, rows[i + 1]); b.stroke(); } }
    b.fillStyle = '#fffaf0'; b.fillRect(0, fy - 10, W, 10); b.fillStyle = 'rgba(120,70,30,.16)'; b.fillRect(0, fy, W, 2);
    // 日だまり（まどの形）
    const sx0 = wx + ww * .35, sy0 = fy + (H - fy) * .1, sk = (H - sy0) * .62, sw = ww * 1.35;
    b.fillStyle = 'rgba(255,243,196,.42)'; b.beginPath(); b.moveTo(sx0, sy0); b.lineTo(sx0 + sw, sy0); b.lineTo(sx0 + sw + sk, H); b.lineTo(sx0 + sk, H); b.closePath(); b.fill();
    b.strokeStyle = 'rgba(190,130,70,.16)'; b.lineWidth = 5; b.beginPath(); b.moveTo(sx0 + sw / 2, sy0); b.lineTo(sx0 + sw / 2 + sk, H); b.moveTo(sx0 + sk * .45, sy0 + (H - sy0) * .45); b.lineTo(sx0 + sw + sk * .45, sy0 + (H - sy0) * .45); b.stroke();
    // はち植え
    const qx = W * (portrait ? .86 : .9), qy = fy + (H - fy) * .1, qs = S0 * (portrait ? 1.2 : 1);
    b.fillStyle = 'rgba(80,45,15,.16)'; b.beginPath(); b.ellipse(qx + 4 * qs, qy + 2 * qs, 30 * qs, 7 * qs, 0, 0, TAU); b.fill();
    for (const lf of [[-.9, 74, 15], [-.45, 96, 17], [0, 108, 18], [.45, 94, 17], [.95, 70, 15], [-.2, 60, 13], [.25, 62, 13]]) { b.save(); b.translate(qx, qy - 38 * qs); b.rotate(lf[0]); b.fillStyle = lf[1] > 90 ? SC.leaf : mix(SC.leaf, '#3f8456', .35); b.beginPath(); b.ellipse(0, -lf[1] * .5 * qs, lf[2] * qs, lf[1] * .5 * qs, 0, 0, TAU); b.fill(); b.strokeStyle = 'rgba(255,255,255,.3)'; b.lineWidth = 1.2; b.beginPath(); b.moveTo(0, -4 * qs); b.lineTo(0, -lf[1] * .9 * qs); b.stroke(); b.restore(); }
    b.fillStyle = SC.pot; b.beginPath(); b.moveTo(qx - 26 * qs, qy - 40 * qs); b.lineTo(qx + 26 * qs, qy - 40 * qs); b.lineTo(qx + 19 * qs, qy); b.lineTo(qx - 19 * qs, qy); b.closePath(); b.fill();
    b.fillStyle = mix(SC.pot, '#ffffff', .2); rr(b, qx - 29 * qs, qy - 46 * qs, 58 * qs, 11 * qs, 4 * qs); b.fill();
    // ラグ
    const rx = 306 * S0, ry = 66 * S0, cx = W * .5 + 8 * S0, cy = gy - 6 * S0;
    b.fillStyle = 'rgba(80,45,15,.16)'; b.beginPath(); b.ellipse(cx, cy + 5 * S0, rx + 3, ry + 3, 0, 0, TAU); b.fill();
    b.fillStyle = SC.rugEdge; b.beginPath(); b.ellipse(cx, cy, rx, ry, 0, 0, TAU); b.fill();
    b.fillStyle = SC.rug; b.beginPath(); b.ellipse(cx, cy, rx * .955, ry * .9, 0, 0, TAU); b.fill();
    b.strokeStyle = SC.rug2; b.lineWidth = 5 * S0; b.beginPath(); b.ellipse(cx, cy, rx * .84, ry * .76, 0, 0, TAU); b.stroke();
    b.lineWidth = 2 * S0; b.setLineDash([7 * S0, 7 * S0]); b.strokeStyle = SC.rugEdge; b.beginPath(); b.ellipse(cx, cy, rx * .66, ry * .56, 0, 0, TAU); b.stroke(); b.setLineDash([]);
    g = b.createLinearGradient(cx - rx, 0, cx + rx, 0); g.addColorStop(0, 'rgba(255,246,205,.30)'); g.addColorStop(.6, 'rgba(255,246,205,0)'); b.fillStyle = g; b.beginPath(); b.ellipse(cx, cy, rx * .955, ry * .9, 0, 0, TAU); b.fill();
    // ボール
    const ox = W * (portrait ? .13 : .1), oy = gy + 22 * S0, or = 17 * S0;
    b.fillStyle = 'rgba(80,45,15,.18)'; b.beginPath(); b.ellipse(ox + 3 * S0, oy + or * .9, or * 1.05, or * .3, 0, 0, TAU); b.fill();
    b.fillStyle = '#f6c945'; b.beginPath(); b.arc(ox, oy, or, 0, TAU); b.fill();
    b.save(); b.beginPath(); b.arc(ox, oy, or, 0, TAU); b.clip(); b.strokeStyle = '#ef7f6d'; b.lineWidth = or * .34; b.beginPath(); b.arc(ox - or * .9, oy - or * .9, or * 1.25, 0, TAU); b.stroke(); b.restore();
    b.fillStyle = 'rgba(255,255,255,.6)'; b.beginPath(); b.ellipse(ox - or * .35, oy - or * .45, or * .22, or * .13, -.6, 0, TAU); b.fill();
  }

  // ---------- 毛を描く ----------
  const BUF = []; for (let i = 0; i < 15; i++) BUF.push([]);
  function drawHairs(list, isBody, g) {
    const n = Math.floor(list.length * st.hairFrac), up = g.r > .5, b = g.b, p = st.petOn;
    for (const a of BUF) a.length = 0;
    const cx = isBody ? pet.qx : pet.hx, cy = isBody ? pet.qy : pet.hy, ux = isBody ? pet.ux : pet.hux, uy = isBody ? pet.uy : pet.huy;
    for (let i = 0; i < n; i++) {
      const h = list[i]; let x, y, tone;
      if (isBody) { x = b.cx + b.cs * h.u * b.rx - b.sn * h.v * b.ry; y = b.cy + b.sn * h.u * b.rx + b.cs * h.v * b.ry; tone = up ? (h.belly ? 1 : h.patch ? 2 : 0) : h.tone; }
      else { x = h.x; y = h.y; tone = h.tone; }
      let vx = h.rx + h.lx, vy = h.ry + h.ly; const m = Math.hypot(vx, vy); if (m > 1.25) { vx *= 1.25 / m; vy *= 1.25 / m; }
      if (p) { const dx = x - cx, dy = y - cy, d2 = dx * dx + dy * dy; if (d2 < 3844) { const w = 1 - d2 / 3844; x += ux * 7 * w; y += uy * 7 * w; } }
      const lv = clamp(Math.round((h.s * .65 + h.jj * .35) * 2 + 2), 0, 4);
      BUF[tone * 5 + lv].push(x, y, x + vx * h.len, y + vy * h.len);
    }
    ctx.lineCap = 'round'; ctx.lineWidth = 2.1;
    for (let k = 0; k < 15; k++) { const a = BUF[k]; if (!a.length) continue; ctx.strokeStyle = C.lv[(k / 5) | 0][k % 5]; ctx.beginPath(); for (let i = 0; i < a.length; i += 4) { ctx.moveTo(a[i], a[i + 1]); ctx.lineTo(a[i + 2], a[i + 3]); } ctx.stroke(); }
  }

  // ---------- 体 ----------
  function drawBody(g) {
    const b = g.b, k = coat(), r = g.r;
    const p = new Path2D();
    for (const e of BODY_E) { const c = g.B(e[0], e[1]), ex = e[2] * b.rx, ey = e[3] * b.ry; p.moveTo(c[0] + b.cs * ex, c[1] + b.sn * ex); p.ellipse(c[0], c[1], ex, ey, b.rot, 0, TAU); }
    ctx.lineJoin = 'round'; ctx.strokeStyle = C.line; ctx.lineWidth = 6; ctx.stroke(p);
    const gr = ctx.createLinearGradient(0, b.cy - b.ry, 0, b.cy + b.ry); gr.addColorStop(0, C.hi); gr.addColorStop(.5, C.base); gr.addColorStop(1, C.lo);
    ctx.fillStyle = gr; ctx.fill(p);
    ctx.save(); ctx.clip(p);
    ctx.save(); ctx.transform(b.cs * b.rx, b.sn * b.rx, -b.sn * b.ry, b.cs * b.ry, b.cx, b.cy);
    if (r < .98) {
      ctx.globalAlpha = 1 - r;
      const ug = ctx.createLinearGradient(0, .38, 0, .66); ug.addColorStop(0, rgba(C.under, 0)); ug.addColorStop(1, rgba(C.under, 1)); ctx.fillStyle = ug; ctx.fillRect(-2, .38, 4, 1.2);
      if (k.pat !== 'solid' && k.pat !== 'patch') { ctx.fillStyle = C.under; ctx.beginPath(); ctx.ellipse(-.8, .32, .3, .64, 0, 0, TAU); ctx.fill(); }
    }
    ctx.globalAlpha = 1;
    if (k.pat === 'patch') { ctx.fillStyle = C.patch; for (const q of PATCHES) { ctx.beginPath(); ctx.ellipse(q[0], q[1], q[2], q[3], 0, 0, TAU); ctx.fill(); } }
    if (r > .02) { ctx.globalAlpha = r; ctx.fillStyle = C.belly; ctx.beginPath(); ctx.ellipse(.05, .1, .75, .62, 0, 0, TAU); ctx.fill(); ctx.fillStyle = 'rgba(255,160,165,.20)'; ctx.beginPath(); ctx.ellipse(.14, .28, .3, .26, 0, 0, TAU); ctx.fill(); }
    ctx.restore();
    ctx.globalAlpha = 1;
    ctx.fillStyle = 'rgba(40,20,5,.13)'; ctx.beginPath(); ctx.ellipse(g.hx + 12, g.hy + 60 * g.hs, 88 * g.hs, 54 * g.hs, 0, 0, TAU); ctx.fill();
    if (st.petOn && st.petBody) { const a = SP.handP.x * .17, rg = ctx.createRadialGradient(pet.qx, pet.qy, 4, pet.qx, pet.qy, 64); rg.addColorStop(0, `rgba(30,15,5,${a})`); rg.addColorStop(1, 'rgba(30,15,5,0)'); ctx.fillStyle = rg; ctx.fillRect(pet.qx - 66, pet.qy - 66, 132, 132); }
    ctx.restore();
    if (r < .9) { const c = g.B(BODY_E[2][0], BODY_E[2][1]); ctx.globalAlpha = (1 - r) * .5; ctx.strokeStyle = C.line; ctx.lineWidth = 3.5; ctx.lineCap = 'round'; ctx.beginPath(); ctx.ellipse(c[0], c[1], BODY_E[2][2] * b.rx, BODY_E[2][3] * b.ry, b.rot, 2.15, 4.0); ctx.stroke(); ctx.globalAlpha = 1; }
  }
  function drawLeg(l, far) {
    const mx = (l.sx + l.px) / 2 + l.bx, my = (l.sy + l.py) / 2 + l.by;
    ctx.lineCap = 'round';
    ctx.beginPath(); ctx.moveTo(l.sx, l.sy); ctx.quadraticCurveTo(mx, my, l.px, l.py);
    // つけ根は「体の下側の色」から始めて足の色へなじませる（透明にぼかすと、にじんだ棒に見えるため）
    const fade = col => { const gd = ctx.createLinearGradient(l.sx, l.sy, l.px, l.py); gd.addColorStop(0, rgba(col, 0)); gd.addColorStop(.12, rgba(col, 0)); gd.addColorStop(.36, rgba(col, 1)); gd.addColorStop(1, rgba(col, 1)); return gd; };
    const legCol = far ? C.far : C.base, rootCol = far ? C.far : mix(C.under, C.base, G ? G.r : 0);
    const body = ctx.createLinearGradient(l.sx, l.sy, l.px, l.py); body.addColorStop(0, rootCol); body.addColorStop(.14, rootCol); body.addColorStop(.5, legCol); body.addColorStop(1, legCol);
    ctx.strokeStyle = fade(C.line); ctx.lineWidth = l.w + 6; ctx.stroke();
    ctx.strokeStyle = body; ctx.lineWidth = l.w; ctx.stroke();
    ctx.save(); ctx.translate(l.px, l.py); ctx.rotate(l.pa);
    ctx.beginPath(); ctx.ellipse(l.w * .2, 0, l.w * .76, l.w * .62, 0, 0, TAU);
    ctx.fillStyle = far ? mix(C.paw, C.far, .35) : C.paw; ctx.fill(); ctx.strokeStyle = C.line; ctx.lineWidth = 3; ctx.stroke();
    ctx.strokeStyle = rgba(lum(C.paw) < .3 ? '#000000' : '#6b4020', .45); ctx.lineWidth = 2.4;
    ctx.beginPath(); for (const o of [-.2, .2]) { ctx.moveTo(l.w * .62, l.w * o); ctx.lineTo(l.w * .93, l.w * o * 1.05); } ctx.stroke();
    ctx.restore();
  }
  function drawTail(g) {
    const t = g.tail, k = coat(), TT = TAILS[g.T.tail];
    ctx.fillStyle = C.line; ctx.beginPath(); for (const n of t) { ctx.moveTo(n.x + n.r + 3, n.y); ctx.arc(n.x, n.y, n.r + 3, 0, TAU); } ctx.fill();
    for (let i = t.length - 1; i >= 0; i--) {
      const n = t[i];
      ctx.fillStyle = (k.pat === 'bi' && i > t.length * .68) ? C.under : (k.pat === 'patch' && i < t.length * .45 ? C.patch : (k.pat === 'ura' && TT.fluff && i > t.length * .5 ? mix(C.base, C.under, .5) : C.base));
      ctx.beginPath(); ctx.arc(n.x, n.y, n.r, 0, TAU); ctx.fill();
    }
    if (TT.fluff) {
      ctx.strokeStyle = rgba(lum(C.base) < .3 ? '#ffffff' : '#fff8e8', lum(C.base) < .3 ? .12 : .3); ctx.lineWidth = 2.2; ctx.lineCap = 'round'; ctx.beginPath();
      for (let i = 2; i < t.length; i += 3) { const n = t[i], nx = -Math.sin(n.a), ny = Math.cos(n.a); for (const o of TT.plume ? [-.55, .1, .6] : [.45]) { const x = n.x + nx * n.r * o, y = n.y + ny * n.r * o; ctx.moveTo(x, y); ctx.lineTo(x + Math.cos(n.a + o * .8) * n.r * .55, y + Math.sin(n.a + o * .8) * n.r * .55); } }
      ctx.stroke();
    }
  }

  // ---------- 頭 ----------
  function earUp(kind, sd, e, pk) {
    const P = kind === 'point' ? [26, -80, 100, -36, 82, -152, 30, 42] : kind === 'small' ? [34, -84, 84, -58, 66, -134, 20, 26] : [18, -78, 106, -34, 96, -172, 30, 50];
    const ax = sd * P[0], ay = P[1], bx = sd * P[2], by = P[3], tx = sd * (P[4] + e * P[6]), ty = P[5] + e * P[7] - pk * 7;
    const path = s => { ctx.beginPath(); const cx = (ax + bx + tx) / 3, cy = (ay + by + ty) / 3, f = (x, c) => c + (x - c) * s;
      ctx.moveTo(f(ax, cx), f(ay, cy)); ctx.bezierCurveTo(f(ax + sd * 2, cx), f(ay - 42, cy), f(tx - sd * 16, cx), f(ty + 10, cy), f(tx, cx), f(ty, cy));
      ctx.bezierCurveTo(f(tx + sd * 16, cx), f(ty + 12, cy), f(bx + sd * 8, cx), f(by - 44, cy), f(bx, cx), f(by, cy)); ctx.closePath(); };
    path(1); ctx.strokeStyle = C.line; ctx.lineWidth = 6; ctx.stroke(); ctx.fillStyle = C.ear; ctx.fill();
    path(.58); ctx.fillStyle = C.earIn; ctx.fill();
  }
  function earDrop(sd, e) {
    const sw = SP.earSw.x * (sd > 0 ? 1 : 1) + sd * e * 9, dn = -e * 8;
    ctx.beginPath(); ctx.moveTo(sd * 48, -82);
    ctx.bezierCurveTo(sd * 96, -96, sd * 130 + sw * .6, -30, sd * 120 + sw, 34 + dn);
    ctx.bezierCurveTo(sd * 114 + sw * 1.2, 78 + dn, sd * 76 + sw * 1.2, 80 + dn, sd * 76 + sw * .8, 30 + dn);
    ctx.bezierCurveTo(sd * 74, 0, sd * 70, -40, sd * 48, -82); ctx.closePath();
    ctx.strokeStyle = C.line; ctx.lineWidth = 5; ctx.stroke(); ctx.fillStyle = C.ear; ctx.fill();
    ctx.strokeStyle = rgba(lum(C.ear) < .3 ? '#ffffff' : '#4a2c14', .16); ctx.lineWidth = 2.4; ctx.lineCap = 'round'; ctx.beginPath();
    for (const o of [0, 1, 2]) { ctx.moveTo(sd * (88 + o * 9) + sw * .5, -20 + o * 10); ctx.lineTo(sd * (92 + o * 8) + sw, 36 + dn + o * 6); } ctx.stroke();
  }
  function drawHead(g) {
    const T = g.T, k = coat();
    useM(g.MH);
    const e = clamp(SP.ear.x, -.25, 1.2), pk = SP.perk.x, fx = SP.faceX.x, fy = SP.faceY.x - SP.chin.x * 13, sn = T.snout, yw = clamp(SP.yawn.x, 0, 1);
    ctx.lineJoin = 'round';
    if (T.ear !== 'drop') for (const sd of [-1, 1]) earUp(T.ear, sd, e, pk);
    const p = new Path2D(); p.ellipse(0, 0, 104, 94, 0, 0, TAU);
    if (T.cheek > 0) { const rc = 30 + 10 * T.cheek; for (const sd of [-1, 1]) { p.moveTo(sd * 74 + rc, 36); p.arc(sd * 74, 36, rc, 0, TAU); } }
    if (T.ear === 'small') for (let i = 0; i < 14; i++) { const a = i / 14 * TAU + .22, x = Math.cos(a) * 100, y = Math.sin(a) * 88 + 6; p.moveTo(x + 30, y); p.arc(x, y, 30, 0, TAU); }
    ctx.strokeStyle = C.line; ctx.lineWidth = 6; ctx.stroke(p);
    const gr = ctx.createRadialGradient(-34, -50, 10, 0, 0, 140); gr.addColorStop(0, C.hi); gr.addColorStop(.55, C.base); gr.addColorStop(1, C.lo);
    ctx.fillStyle = gr; ctx.fill(p);
    ctx.save(); ctx.clip(p);
    if (k.pat === 'ura' || k.pat === 'bi' || k.pat === 'tan') { ctx.fillStyle = C.under; for (const sd of [-1, 1]) { ctx.beginPath(); ctx.ellipse(FACE0 + sd * 64, 46, 46, 44, 0, 0, TAU); ctx.fill(); } }
    if (k.pat === 'bi') { ctx.fillStyle = C.under; ctx.beginPath(); ctx.moveTo(FACE0 - 10, -100); ctx.quadraticCurveTo(FACE0 - 14, -30, FACE0 - 26, 24); ctx.lineTo(FACE0 + 26, 24); ctx.quadraticCurveTo(FACE0 + 14, -30, FACE0 + 10, -100); ctx.closePath(); ctx.fill(); }
    if (k.pat === 'patch') { ctx.fillStyle = C.patch; ctx.beginPath(); ctx.ellipse(52, -34, 46, 54, 0, 0, TAU); ctx.fill(); }
    ctx.restore();
    drawHairs(headHairs, false, g);
    if (T.ear === 'drop') for (const sd of [-1, 1]) earDrop(sd, e);
    // --- 顔 ---
    const mx = fx * 1.2, my = 31 + fy, nx = fx * 1.35, ny = 13 + fy;
    const mo = clamp(Math.max(SP.mouth.x, yw * 1.5), 0, 1.6), tg = clamp(SP.tongue.x, 0, 1.2) * (1 - yw * .5);
    // ほおの赤み
    const ba = .1 + st.happy * .0035; ctx.fillStyle = `rgba(255,120,140,${C.dark ? ba * .7 : ba})`;
    for (const sd of [-1, 1]) { ctx.beginPath(); ctx.ellipse(fx + sd * 66, 16 + fy * .5, 15, 9, 0, 0, TAU); ctx.fill(); }
    // 口もと
    ctx.fillStyle = C.muzzle; ctx.beginPath(); ctx.ellipse(mx, my, 44 * sn, 32 * sn * (1 + yw * .06), 0, 0, TAU); ctx.fill();
    ctx.strokeStyle = rgba(C.mrim, .5); ctx.lineWidth = 1.6; ctx.stroke();
    const cw = 19 * sn, top = ny + 21 * sn, dep = mo * 25 * sn, lift = SP.smile.x * 2.5 + mo * 2;
    if (mo > .04) {
      ctx.beginPath(); ctx.moveTo(nx - cw - 4, top - lift); ctx.bezierCurveTo(nx - cw - 6, top + dep * 1.25 + 11, nx + cw + 6, top + dep * 1.25 + 11, nx + cw + 4, top - lift); ctx.closePath();
      ctx.fillStyle = C.muzzle; ctx.fill(); ctx.strokeStyle = C.mrim; ctx.lineWidth = 2; ctx.stroke();
      ctx.beginPath(); ctx.moveTo(nx - cw, top - lift); ctx.bezierCurveTo(nx - cw, top + dep * 1.2 + 3, nx + cw, top + dep * 1.2 + 3, nx + cw, top - lift); ctx.closePath(); ctx.fillStyle = FEAT.mouth; ctx.fill();
      const ty = top + dep * .55 + tg * 8, th = Math.max(2, dep * .36 + tg * 9);
      ctx.fillStyle = FEAT.tongue; ctx.beginPath(); ctx.ellipse(nx, ty, 10.5 * sn, th, 0, 0, TAU); ctx.fill();
      ctx.strokeStyle = 'rgba(205,75,105,.5)'; ctx.lineWidth = 1.6; ctx.beginPath(); ctx.moveTo(nx, ty - th * .5); ctx.lineTo(nx, ty + th * .55); ctx.stroke();
    }
    // 口の線（ω）
    ctx.strokeStyle = C.mline; ctx.lineWidth = 3; ctx.lineCap = 'round'; ctx.beginPath();
    ctx.moveTo(nx, ny + 8); ctx.lineTo(nx, top - 2);
    ctx.moveTo(nx, top - 2); ctx.quadraticCurveTo(nx - cw * .45, top + 8, nx - cw - 1, top - lift);
    ctx.moveTo(nx, top - 2); ctx.quadraticCurveTo(nx + cw * .45, top + 8, nx + cw + 1, top - lift); ctx.stroke();
    // ひげの点
    ctx.fillStyle = rgba(C.mline, .32); for (const sd of [-1, 1]) for (const d of [[23, 4], [31, 10], [22, 14]]) { ctx.beginPath(); ctx.arc(mx + sd * d[0] * sn, my + d[1] - 4, 1.5, 0, TAU); ctx.fill(); }
    // 鼻
    ctx.fillStyle = FEAT.nose; ctx.beginPath(); ctx.moveTo(nx - 13 * sn, ny - 5); ctx.quadraticCurveTo(nx, ny - 11, nx + 13 * sn, ny - 5); ctx.quadraticCurveTo(nx + 13 * sn, ny + 4, nx, ny + 10); ctx.quadraticCurveTo(nx - 13 * sn, ny + 4, nx - 13 * sn, ny - 5); ctx.fill();
    ctx.fillStyle = 'rgba(255,255,255,.55)'; ctx.beginPath(); ctx.ellipse(nx - 4, ny - 4, 4.2, 2.1, -.2, 0, TAU); ctx.fill();
    // 茶のまゆ
    if (k.pat === 'tan') { ctx.fillStyle = C.under; for (const sd of [-1, 1]) { ctx.beginPath(); ctx.ellipse(fx + sd * 37, -40 + fy * .7 - pk * 2, 9, 6.5, sd * -.25, 0, TAU); ctx.fill(); } }
    // 目
    const c = clamp(SP.eye.x, 0, 1), sm = SP.smile.x;
    for (const sd of [-1, 1]) {
      const ex = fx + sd * 39, ey = -15 + fy * .8, onDark = lum(C.base) < .4 || (k.pat === 'patch' && sd === 1);
      if (c < .8) {
        const eh = 12.5 * (1 - c * .92);
        if (onDark) { ctx.strokeStyle = 'rgba(255,240,225,.38)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.ellipse(ex, ey, 11.5, eh + 1, 0, 0, TAU); ctx.stroke(); }
        ctx.fillStyle = FEAT.dark; ctx.beginPath(); ctx.ellipse(ex, ey, 10.5, eh, 0, 0, TAU); ctx.fill();
        if (c < .55) { const gx = clamp((fx - FACE0) * .08, -2, 2); ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(ex - 3.2 + gx, ey - 4.2 * (1 - c), 3.5 * (1 - c * .6), 0, TAU); ctx.fill(); ctx.beginPath(); ctx.arc(ex + 3.6 + gx, ey + 3.4 * (1 - c), 1.6, 0, TAU); ctx.fill(); }
      } else {
        ctx.strokeStyle = onDark ? '#f4e6d6' : FEAT.dark; ctx.lineWidth = 4; ctx.lineCap = 'round'; ctx.beginPath();
        const bend = lerp(6.5, -9, clamp(sm, 0, 1));   // 細めた目（⌒）〜 ねむい目（‿）
        ctx.moveTo(ex - 11, ey - bend * .3); ctx.quadraticCurveTo(ex, ey + bend, ex + 11, ey - bend * .3); ctx.stroke();
      }
    }
  }

  // ---------- 小さな飾り ----------
  function drawParts() {
    for (const p of parts) {
      const k = p.life / p.max, a = k < .15 ? k / .15 : 1 - (k - .15) / .85, s = p.size * (G.S / .9) * (.7 + k * .5);
      ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.rot); ctx.globalAlpha = clamp(a, 0, 1);
      if (p.type === 'heart') { ctx.fillStyle = FEAT.heart; ctx.beginPath(); ctx.moveTo(0, s * .7); ctx.bezierCurveTo(-s * 1.4, -s * .2, -s * .7, -s * 1.1, 0, -s * .35); ctx.bezierCurveTo(s * .7, -s * 1.1, s * 1.4, -s * .2, 0, s * .7); ctx.fill(); }
      else if (p.type === 'spark') { ctx.fillStyle = '#fff6c9'; ctx.beginPath(); for (let i = 0; i < 8; i++) { const r = i % 2 ? s * .32 : s, an = i * Math.PI / 4; ctx.lineTo(Math.cos(an) * r, Math.sin(an) * r); } ctx.closePath(); ctx.fill(); }
      else { ctx.fillStyle = '#7c8fb3'; ctx.font = `800 ${Math.round(s * 1.7)}px sans-serif`; ctx.textAlign = 'center'; ctx.fillText('z', 0, 0); }
      ctx.restore();
    }
    ctx.globalAlpha = 1;
  }
  // 手（1回だけ別のキャンバスに描いておく）
  const handCv = document.createElement('canvas'); handCv.width = handCv.height = 144;
  (() => { const h = handCv.getContext('2d'); h.translate(72, 80); h.scale(1.5, 1.5); h.lineCap = 'round'; h.strokeStyle = '#fff'; h.fillStyle = '#fff';
    h.beginPath(); h.ellipse(0, 7, 17, 15, 0, 0, TAU); h.fill(); h.lineWidth = 9;
    for (const f of [[-13, -4, -15, -20], [-4.5, -6, -5, -27], [4.5, -6, 5, -26], [13, -3, 15, -18]]) { h.beginPath(); h.moveTo(f[0], f[1]); h.lineTo(f[2], f[3]); h.stroke(); }
    h.beginPath(); h.moveTo(-14, 9); h.lineTo(-25, -1); h.stroke(); })();
  function drawHand() {
    if (hand.a < .02) return;
    const s = G.S / .9 * (1.12 - SP.handP.x * .14), pr = clamp(SP.handP.x, 0, 1);
    ctx.save(); ctx.translate(hand.x, hand.y); ctx.rotate(-.3 + hand.rot); ctx.scale(s, s);
    ctx.globalAlpha = hand.a * (.16 + pr * .1); ctx.filter = 'none';
    ctx.shadowColor = 'rgba(50,25,5,.9)'; ctx.shadowBlur = 10 * dpr; ctx.shadowOffsetY = (9 - pr * 6) * dpr; ctx.shadowOffsetX = (5 - pr * 3) * dpr;
    ctx.drawImage(handCv, -48, -53, 96, 96);
    ctx.shadowColor = 'transparent'; ctx.globalAlpha = hand.a * (.6 + pr * .12);
    ctx.drawImage(handCv, -48, -53, 96, 96);
    ctx.restore(); ctx.globalAlpha = 1;
  }

  function draw() {
    size();
    const g = G = geom(), L = g.legs, up = g.r >= .5;
    ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(bgc, 0, 0);
    useM(g.MD);
    // 影
    ctx.fillStyle = 'rgba(60,35,10,.20)'; ctx.beginPath(); ctx.ellipse(g.b.cx - 14, 2, g.b.rx * 1.16, 16, 0, 0, TAU); ctx.fill();
    if (g.r > .3) { ctx.globalAlpha = g.r; ctx.beginPath(); ctx.ellipse(g.hx, 4, 100 * g.hs, 14, 0, 0, TAU); ctx.fill(); ctx.globalAlpha = 1; }
    const tailTop = g.T.tail === 'curl' && !up;   // 巻きしっぽは背中の上にのせる
    if (!tailTop) drawTail(g);
    if (!up) { drawLeg(L.HF, true); drawLeg(L.FF, true); }
    drawBody(g); drawHairs(bodyHairs, true, g);
    if (tailTop) drawTail(g);
    if (up) { drawLeg(L.HF, true); drawLeg(L.FF, true); }
    drawLeg(L.HN, false); drawLeg(L.FN, false);
    drawHead(g);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    // 日の光
    const lg = ctx.createRadialGradient(W * .1, H * .05, 0, W * .1, H * .05, Math.max(W, H) * .95); lg.addColorStop(0, 'rgba(255,238,180,.20)'); lg.addColorStop(1, 'rgba(255,238,180,0)'); ctx.fillStyle = lg; ctx.fillRect(0, 0, W, H);
    for (let i = 0; i < 12; i++) { const ph = st.t * .05 + i * .083, x = W * (.12 + ((i * .137 + ph) % 1) * .6), y = H * (.12 + ((i * .31 + Math.sin(st.t * .2 + i) * .03 + ph * .6) % 1) * .6); ctx.fillStyle = `rgba(255,250,225,${.25 + .25 * Math.sin(st.t * .9 + i * 2)})`; ctx.beginPath(); ctx.arc(x, y, 1.3 + (i % 3) * .5, 0, TAU); ctx.fill(); }
    drawParts(); drawHand();
  }

  // =====================================================================
  //  画面の数字・ボタン
  // =====================================================================
  const fmtT = s => s < 60 ? Math.floor(s) + '秒' : Math.floor(s / 60) + '分' + Math.floor(s % 60) + '秒';
  let lastUI = 0, lastMood = '';
  function ui(force) {
    const now = performance.now(); if (!force && now - lastUI < 200) return; lastUI = now;
    $('inuCnt').textContent = st.count; $('inuTime').textContent = fmtT(st.sec);
    $('inuHappy').textContent = Math.round(st.happy); $('inuBar').style.width = st.happy.toFixed(0) + '%';
    if (st.mood !== lastMood) { lastMood = st.mood; $('inuMood').textContent = st.mood; }
    if (st.dirty && (force || now - st.saveT > 2000)) save();
  }
  function save() { st.dirty = false; st.saveT = performance.now(); try { localStorage.setItem(KEY, JSON.stringify({ count: st.count, sec: Math.round(st.sec * 10) / 10, type: cfg.type, coat: cfg.coat, size: cfg.size, fat: cfg.fat })); } catch (e) {} }
  function load() { try { const o = JSON.parse(localStorage.getItem(KEY) || 'null'); if (!o) return; st.count = Math.max(0, o.count | 0); st.sec = Math.max(0, +o.sec || 0); applyCfg(o, true); } catch (e) {} }
  function applyCfg(o, quiet) {
    const t0 = cfg.type;
    if (o.type && TYPES[o.type]) cfg.type = o.type;
    if (o.coat != null) { const c = typeof o.coat === 'number' ? COATS[o.coat] : COATS.find(v => v.id === o.coat); if (c) cfg.coat = c.id; }
    if (o.size != null && isFinite(+o.size)) cfg.size = clamp(+o.size, .7, 1);
    if (o.fat != null && isFinite(+o.fat)) cfg.fat = clamp(+o.fat, .82, 1.3);
    buildPalette(); if (cfg.type !== t0 || !bodyHairs.length) makeHairs(); else assignTones();
    syncUI(); if (!quiet) save();
  }
  function syncUI() {
    for (const b of $('inuTypes').children) b.classList.toggle('on', b.dataset.v === cfg.type);
    for (const b of $('inuCoats').children) b.classList.toggle('on', b.dataset.v === cfg.coat);
    $('inuCoatName').textContent = coat().name;
    $('inuSize').value = Math.round(cfg.size * 100); $('inuFat').value = Math.round(cfg.fat * 100);
    $('inuSizeV').textContent = cfg.size < .78 ? '小さめ' : cfg.size > .94 ? '大きめ' : 'ふつう';
    $('inuFatV').textContent = cfg.fat < .93 ? 'ほっそり' : cfg.fat > 1.14 ? 'ぽっちゃり' : 'ふつう';
  }
  for (const id of TYPE_IDS) { const b = document.createElement('button'); b.type = 'button'; b.dataset.v = id; b.textContent = TYPES[id].name; b.addEventListener('click', () => applyCfg({ type: id })); $('inuTypes').appendChild(b); }
  for (const c of COATS) {
    const b = document.createElement('button'); b.type = 'button'; b.dataset.v = c.id; b.title = c.name; b.setAttribute('aria-label', '毛色：' + c.name);
    const second = c.pat === 'patch' ? c.patch : c.pat === 'solid' ? null : c.light;
    b.style.background = second ? `linear-gradient(135deg, ${c.base} 0 58%, ${second} 58% 100%)` : c.base;
    b.addEventListener('click', () => applyCfg({ coat: c.id })); $('inuCoats').appendChild(b);
  }
  $('inuSize').addEventListener('input', e => applyCfg({ size: e.target.value / 100 }));
  $('inuFat').addEventListener('input', e => applyCfg({ fat: e.target.value / 100 }));
  $('inuRand').addEventListener('click', () => {
    let t = cfg.type, c = cfg.coat; while (t === cfg.type && c === cfg.coat) { t = TYPE_IDS[Math.floor(Math.random() * TYPE_IDS.length)]; c = COATS[Math.floor(Math.random() * COATS.length)].id; }
    applyCfg({ type: t, coat: c, size: .74 + Math.random() * .24, fat: .86 + Math.random() * .4 });
    SP.squash.v += 6; SP.headY.v -= 60;
  });

  // ---------- マウス・指 ----------
  function setHand(e) { const r = cv.getBoundingClientRect(); hand.x = (e.clientX - r.left) * (W / (r.width || W)); hand.y = (e.clientY - r.top) * (H / (r.height || H)); hand.mouse = e.pointerType === 'mouse'; hand.over = true; }
  cv.addEventListener('pointerdown', e => { try { cv.setPointerCapture(e.pointerId); } catch (_) {} hand.was = hand.over && hand.was; setHand(e); hand.down = true; e.preventDefault(); });
  cv.addEventListener('pointermove', e => { if (e.pointerType !== 'mouse' && !hand.down) return; setHand(e); });
  const up = e => { hand.down = false; if (e.pointerType !== 'mouse') hand.over = false; };
  cv.addEventListener('pointerup', up); cv.addEventListener('pointercancel', e => { hand.down = false; hand.over = false; });
  cv.addEventListener('pointerleave', e => { if (!hand.down) hand.over = false; });
  cv.addEventListener('contextmenu', e => e.preventDefault());
  $('inuWrap').classList.add('in-on');

  // ---------- シェア ----------
  const shareText = () => st.count > 0 ? `犬を${st.count}回なでました🐶（${fmtT(st.sec)}・うれしさ${Math.round(st.happy)}）ただ、なでるだけ。` : '犬を、ただなでるだけのページ🐶';
  const flash = m => { lastMood = m; $('inuMood').textContent = m; setTimeout(() => { lastMood = ''; }, 1600); };
  $('shareBtn').addEventListener('click', () => { const u = location.origin + location.pathname; window.open('https://twitter.com/intent/tweet?text=' + encodeURIComponent(shareText() + '\n') + '&url=' + encodeURIComponent(u) + '&hashtags=' + encodeURIComponent('シミュラボ'), '_blank', 'noopener'); });
  $('copyBtn').addEventListener('click', async () => { try { await navigator.clipboard.writeText(shareText() + '\n' + location.origin + location.pathname); flash('コピーしました'); } catch (e) { flash('コピーできませんでした'); } });

  // ---------- 動かす ----------
  function sim(dt) { handVel(dt); const n = Math.max(1, Math.ceil(dt / (1 / 50))); for (let i = 0; i < n; i++) update(dt / n); }
  let tPrev = performance.now(), fAcc = 0, fN = 0, wAcc = 0, wN = 0, slow = 0, paused = false;
  function loop(now) {
    const real = (now - tPrev) / 1000; tPrev = now;
    if (real < .5) { fAcc += real; fN++; }
    if (!paused) { const w0 = performance.now(); sim(clamp(real, .001, .05)); draw(); ui(false); wAcc += performance.now() - w0; wN++; }
    // 重い端末では毛を減らす（1コマにかかった計算時間で判断。裏のタブでコマが間引かれても減らさない）
    if (wN >= 60) {
      const work = wAcc / wN, fps = fAcc > 0 ? fN / fAcc : 0; st.fps = fps; st.work = work; wAcc = 0; wN = 0; fAcc = 0; fN = 0;
      if (work > 11 || (fps > 15 && fps < 42 && work > 4)) { if (++slow >= 2 && st.hairFrac > .4) { st.hairFrac = Math.max(.4, st.hairFrac - .2); slow = 0; } }
      else { slow = 0; if (work < 2.5 && fps > 50 && st.hairFrac < 1) st.hairFrac = Math.min(1, st.hairFrac + .2); }
    }
    requestAnimationFrame(loop);
  }
  buildPalette(); load(); if (!bodyHairs.length) { makeHairs(); syncUI(); }
  size(); G = geom(); draw(); ui(true);
  window.addEventListener('resize', () => { bgOK = false; });
  window.addEventListener('pagehide', () => { if (st.dirty) save(); });
  requestAnimationFrame(loop);

  // ---------- テスト用（裏のタブでは requestAnimationFrame が止まるため） ----------
  window.__t = {
    step(sec) { const n = Math.max(1, Math.round((sec || 0) * 60)); for (let i = 0; i < n; i++) sim(1 / 60); draw(); ui(true); return this.s; },
    pet(region, sec, speed) {
      sec = sec || 1; speed = speed || 260; const n = Math.max(1, Math.round(sec * 60)); let ph = 0;
      hand.over = false; hand.was = false;
      for (let i = 0; i < n; i++) {
        G = geom(); const a = anchor(region), A = (region === 'paw' || region === 'tail' ? 13 : region === 'head' || region === 'chin' ? 28 : 40) * G.S;
        ph += speed * G.S * (Math.PI / 2) / A / 60;
        hand.x = a[0] + Math.sin(ph) * A; hand.y = a[1] + Math.cos(ph * .5) * A * .12; hand.over = true; hand.down = true; hand.mouse = true;
        sim(1 / 60);
      }
      const out = this.s; draw(); ui(true); hand.down = false; hand.over = false; return out;
    },
    set(o) { applyCfg(o || {}); draw(); return this.s; },
    pause(v) { paused = v !== false; return paused; },
    reset() { st.count = 0; st.sec = 0; st.happy = 15; st.sleepyT = 0; SP.roll.t = 0; st.dirty = true; ui(true); },
    get s() {
      let nan = false; for (const n in SP) if (!isFinite(SP[n].x) || !isFinite(SP[n].v)) nan = true; if (!isFinite(st.happy) || !isFinite(st.wagPh)) nan = true;
      const f = v => Math.round(v * 100) / 100;
      return { happy: f(st.happy), pose: SP.roll.t > .5 ? 'hesoten' : 'fuse', roll: f(SP.roll.x), wag: { hz: f(st.wagHz), amp: f(SP.wagAmp.x) }, eye: f(SP.eye.x), ear: f(SP.ear.x), chin: f(SP.chin.x), headX: f(SP.headX.x), headY: f(SP.headY.x),
        faceX: f(SP.faceX.x), kick: f(SP.kick.x), paw: f(SP.paw.x), tuck: f(SP.tuck.x), mouth: f(SP.mouth.x), tongue: f(SP.tongue.x), sleepy: f(SP.sleepy.x), region: st.reg, mood: st.mood, idle: f(st.idle), evt: st.evt ? st.evt.type : null,
        counts: { pets: st.count, sec: f(st.sec) }, cfg: Object.assign({}, cfg), hairs: Math.floor(bodyHairs.length * st.hairFrac) + Math.floor(headHairs.length * st.hairFrac), hairFrac: st.hairFrac, fps: f(st.fps), work: f(st.work), W, H, dpr, particles: parts.length, nan };
    },
  };
})();
"""


def esc(s): return H.escape(s, quote=True)


def build():
    url = f"{BASE}/sims/{SLUG}/"
    ld_app = {"@context": "https://schema.org", "@type": "WebApplication", "name": NAME, "url": url, "description": DESC,
              "applicationCategory": "EntertainmentApplication", "operatingSystem": "Any", "inLanguage": "ja", "isAccessibleForFree": True,
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
    <p class="in-note">{esc(NOTE)}</p>
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
