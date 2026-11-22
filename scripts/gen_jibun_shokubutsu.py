# -*- coding: utf-8 -*-
"""自分だけの植物を育てるシミュレーター（2026-11-23・リクエスト 2e17b147c9「自分だけの植物を作る」）
   sims/jibun-shokubutsu/index.html を書き出す（冪等）。 使い方: python scripts/gen_jibun_shokubutsu.py"""
import html as H, io, json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://shimulabo.com"
SLUG = "jibun-shokubutsu"
NAME = "自分だけの植物を育てるシミュレーター"
CAT = "あそぶ・実験"
TITLE = "自分だけの植物を作って育てる｜植物の育て方シミュレーター（日当たり・水やり・肥料・かけ合わせ）｜シミュラボ"
DESC = ("背の高さ・枝分かれ・葉の形・花の色や花びらの数を決めた「自分だけのタネ」をまいて、日当たり・光の向き・水やり・肥料・気温を変えながら育てるシミュレーター。"
        "光が足りないとひょろひょろに、水が多すぎると根ぐされに。花が咲いたらタネをとって図鑑に保存し、2つをかけ合わせて子どもの植物も作れます。")
OG_T = "自分だけの植物を作って育てる 植物の育て方シミュレーター"
OG_D = "タネの形と、日当たり・水・肥料・気温で育ち方が変わる。花が咲いたらタネをとって、かけ合わせもできる。"
H1 = "自分だけの植物を作って育てる<br>植物の育て方シミュレーター"
LEAD = ("葉の形や花の色を決めた「自分だけのタネ」をまいて、育ててみましょう。日当たり・水やり・肥料・気温を変えると、伸び方や葉の色、花が咲くかどうかが変わります。"
        "花が咲いたらタネをとって図鑑に保存し、2つをかけ合わせると、親に似た（ときどき似ていない）子どもが生まれます。")
NOTE = "💌 このシミュレーターは、リクエスト「自分だけの植物を作る」から作りました。"

FAQ = [
    ("どうやって遊びますか？", "まず「タネをえらぶ」で好きなタネを選ぶか、「タネの形を決める」で背の高さ・葉の形・花の色などを決めます。次に「育てる環境」で日当たりや水やりを決めると、日にちが進んで植物が育ちます。花が咲いたら「🌰 タネをとる」で図鑑に保存できます。"),
    ("なかなか花が咲きません。", "このシミュレーターでは、ある程度大きく育ち、日当たりがよく（35以上）、気温が12℃以上で、元気（体調）が40%以上のときに花が咲きます。日かげのままだと、大きくなっても花は咲きません。"),
    ("ひょろひょろになってしまうのはなぜ？", "光が足りないと、植物は光を求めて茎を長く伸ばし、葉は小さく色がうすくなります。これを「徒長（とちょう）」といいます。日当たりを上げると、がっしりした育ち方になります。"),
    ("水をたくさんあげれば、よく育ちますか？", "いいえ。水が多すぎると土の中の空気が足りなくなり、根が息をできずに弱ってしまいます（根ぐされ）。少なすぎても、しおれてしまいます。このシミュレーターでは30〜70が「ちょうどよい」はんいです。"),
    ("かけ合わせると、どうなりますか？", "子どもの植物は、背の高さや枝分かれは2つの親のあいだくらいに、葉の形や葉のつき方は、どちらか片方の親と同じになります。10回に1回くらい「とつぜん変異」が起きて、親とはちがう特ちょうが出ることもあります。本物の遺伝をとても単純にしたものです。"),
    ("図鑑はどこに保存されますか？", "このブラウザの中（ローカルストレージ）だけに保存されます。サーバーには送られません。ブラウザの記録を消したり、別の端末で開いたりすると、図鑑は見えなくなります。"),
]
REL = [("kougousei", "🍃", "光合成と呼吸のシミュレーション"), ("mendel-iden", "🫛", "メンデルの法則・遺伝の規則性"), ("fractal-tree", "🌳", "フラクタルの木")]

ARTICLE = """
<h2>このシミュレーターのしくみ</h2>
<p>植物の形は、<b>タネ（遺伝子）</b>と<b>育つ環境</b>の両方で決まります。このシミュレーターでも、2つを分けてあつかっています。</p>
<ul>
<li><b>タネで決まること</b>：背の高さ（節の数と長さ）、枝分かれのしやすさと角度、葉の形・大きさ・つき方（互い違い／向かい合わせ）、花の色と花びらの数、光の方へ曲がる力。</li>
<li><b>環境で決まること</b>：育つ速さ、茎の長さと太さ、葉の色、しおれ方、花が咲くかどうか。</li>
</ul>
<p>育つ速さは「日当たり × 水 × 気温 × 肥料 × 元気」のかけ算で決まります。どれか1つでも足りないと、ほかがよくても育ちがおそくなります（いちばん足りないものが全体を決めてしまう考え方を「最少律（さいしょうりつ）」といいます）。</p>

<h2>ためしてみたいこと</h2>
<ul>
<li><b>日当たりを20にする</b>：茎がひょろひょろと長くなり、葉の色がうすくなります（徒長）。花も咲きません。</li>
<li><b>光の向きを「左から」にする</b>：茎が光の方へ曲がっていきます（光屈性）。タネの「光にむかう力」を強くすると、よく曲がります。</li>
<li><b>水やりを90にする</b>：よく育ちそうに見えて、根ぐされで元気がなくなります。</li>
<li><b>肥料を0にする</b>：葉が黄色っぽくなり、小さくしか育ちません。</li>
<li><b>同じタネを、ちがう環境で育てて図鑑に保存する</b>：同じ遺伝子でも、環境で見た目がこんなに変わることがわかります。</li>
<li><b>かけ合わせを何代も続ける</b>：好きな特ちょうをもつ子どもを選んで、またかけ合わせると、だんだん「理想の植物」に近づきます。人が作物や花の品種を作ってきた「品種改良」と同じ考え方です。</li>
</ul>

<h2>本物の植物では</h2>
<p>本物の植物も、光を受けて光合成をし、根から水と肥料（窒素・リン・カリウムなど）を吸って育ちます。茎が光の方へ曲がるのは、オーキシンという物質が光の当たらない側に多く集まり、そちら側がよく伸びるためです。</p>
<p>花がいつ咲くかは、実際には昼の長さ（日長）や気温、植物の種類によって大きくちがいます。このシミュレーターは、育ち方の「感じ」をつかむためにとても単純にしたもので、実際の植物の育て方を予測するものではありません。</p>
"""

REFS = [
    "文部科学省「中学校学習指導要領解説 理科編」（植物の体のつくりと働き、遺伝の規則性と遺伝子）",
    "Lindenmayer, A. (1968) Mathematical models for cellular interactions in development. Journal of Theoretical Biology 18, 280–315.（植物の枝分かれをえがくLシステム）",
    "Prusinkiewicz, P. & Lindenmayer, A. (1990) The Algorithmic Beauty of Plants. Springer.",
]

STAGE = r"""
<style>
.pl-tools{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-bottom:10px}
.pl-seg{display:flex;flex-wrap:wrap;gap:6px}
.pl-seg button,.pl-tools button{border:1.5px solid var(--line);background:#fff;border-radius:999px;padding:8px 13px;font:inherit;font-size:13.5px;font-weight:800;cursor:pointer;color:var(--ink)}
.pl-seg button.on{background:#15803d;border-color:#15803d;color:#fff}
#plWrap{position:relative;border-radius:14px;overflow:hidden;border:1px solid var(--line);background:#e0f2fe}
#pl{display:block;width:100%;aspect-ratio:5/4}
.pl-play{position:absolute;left:10px;top:10px;display:flex;gap:6px;flex-wrap:wrap}
.pl-play button{border:0;border-radius:999px;background:rgba(15,23,42,.8);color:#fff;font:inherit;font-weight:800;font-size:12.5px;padding:7px 12px;cursor:pointer}
.pl-play button.on{background:#f59e0b;color:#111}
.pl-msg{position:absolute;left:50%;bottom:10px;transform:translateX(-50%);background:rgba(15,23,42,.85);color:#fff;font-size:12.5px;font-weight:700;border-radius:12px;padding:6px 14px;max-width:92%;text-align:center;pointer-events:none;opacity:0;transition:opacity .3s}
.pl-msg.show{opacity:1}
.pl-sum{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-top:12px}
.pl-sum div{background:#f0fdf4;border-radius:12px;padding:10px 4px;text-align:center}
.pl-sum b{display:block;font-size:20px;color:#15803d;font-variant-numeric:tabular-nums}
.pl-sum b small{font-size:11.5px}
.pl-sum span{font-size:11.5px;color:var(--ink-2);font-weight:700}
.pl-sum div.warn{background:#fff7ed}.pl-sum div.warn b{color:#c2410c}
.pl-note{font-size:13.5px;color:var(--ink);background:#f0fdf4;border-radius:10px;padding:9px 12px;margin:10px 0 0;font-weight:700}
.pl-name{display:flex;gap:8px;align-items:center;margin-top:12px;flex-wrap:wrap}
.pl-name input{flex:1;min-width:180px;border:1.5px solid var(--line);border-radius:10px;padding:9px 12px;font:inherit;font-size:15px;font-weight:800}
.pl-name button:disabled,#plCross:disabled{opacity:.45;cursor:not-allowed}
#plG{display:block;width:100%;height:110px;margin-top:8px}
.pl-glegend{font-size:12px;color:var(--ink-2);display:flex;gap:14px}
.pl-glegend i{display:inline-block;width:18px;height:3px;vertical-align:3px;margin-right:4px;background:#16a34a}
.pl-glegend i.o{background:repeating-linear-gradient(90deg,#f97316 0 5px,transparent 5px 8px)}
.pl-cols{display:grid;grid-template-columns:1fr 1fr;gap:6px 22px}
#vHue{display:inline-block;width:16px;height:16px;border-radius:50%;vertical-align:-3px;border:1px solid rgba(0,0,0,.15)}
#kHue{background:linear-gradient(90deg,hsl(0,78%,63%),hsl(60,78%,63%),hsl(120,78%,63%),hsl(180,78%,63%),hsl(240,78%,63%),hsl(300,78%,63%),hsl(360,78%,63%));border-radius:999px;height:10px}
.pl-book{display:grid;grid-template-columns:repeat(auto-fill,minmax(132px,1fr));gap:10px;margin-top:8px}
.pl-card{border:1.5px solid var(--line);border-radius:12px;padding:6px;background:#fff;text-align:center}
.pl-card.on{border-color:#15803d;box-shadow:0 0 0 2px #bbf7d0}
.pl-card img{width:100%;height:auto;border-radius:8px;display:block}
.pl-card b{display:block;font-size:13.5px;margin-top:4px;word-break:break-all}
.pl-card span{display:block;font-size:11.5px;color:var(--ink-2)}
.pl-cbtn{display:flex;gap:4px;margin-top:6px}
.pl-cbtn button{flex:1;border:1px solid var(--line);background:#f8fafc;border-radius:8px;padding:6px 1px;font:inherit;font-size:11.5px;white-space:nowrap;font-weight:800;cursor:pointer}
.pl-cbtn button[data-a=del]{flex:0 0 28px}
.pl-hint{font-size:13px;color:var(--ink-2);margin:0 0 6px}
@media (max-width:640px){.pl-sum{grid-template-columns:repeat(3,1fr)}.pl-cols{grid-template-columns:1fr}.pl-play button{padding:6px 10px;font-size:12px}}
</style>
"""

BODY = r"""
  <section class="panel" id="resultPanel">
    <h2 style="margin:0 0 8px;font-size:18px;">① タネをえらぶ</h2>
    <div class="pl-seg" id="plSeeds"></div>

    <div id="plWrap" style="margin-top:12px">
      <canvas id="pl" aria-label="植木鉢で育っている植物の絵"></canvas>
      <div class="pl-play"><button type="button" id="plPlay">⏸ 止める</button><button type="button" data-sp="1" class="on">×1</button><button type="button" data-sp="4">×4</button><button type="button" id="plFast">⏩ 50日目まで</button></div>
      <div class="pl-msg" id="plMsg"></div>
    </div>
    <div class="pl-sum">
      <div><b id="mDay">0</b><span>育てた日数</span></div>
      <div><b id="mH">0</b><span>草たけ</span></div>
      <div><b id="mLeaf">0</b><span>葉</span></div>
      <div><b id="mFl">0</b><span>咲いた花</span></div>
      <div id="mHpBox"><b id="mHp">100</b><span>元気</span></div>
    </div>
    <p class="pl-note" id="plNote">🌱 タネをまきました。</p>
    <div class="pl-name">
      <input id="plName" type="text" maxlength="20" aria-label="植物の名前">
      <button class="btn btn-primary" id="plSeed" type="button" style="width:auto;padding:10px 16px;" disabled>🌰 タネをとる</button>
      <button class="btn btn-ghost" id="plRestart" type="button" style="width:auto;padding:10px 14px;">🌱 タネから育てなおす</button>
    </div>
    <canvas id="plG" aria-label="草たけと元気の変化のグラフ"></canvas>
    <div class="pl-glegend"><span><i></i>草たけ</span><span><i class="o"></i>元気</span></div>

    <h2 style="margin:20px 0 10px;font-size:18px;">② 育てる環境（いつでも変えられます）</h2>
    <div class="pl-cols">
      <div class="field"><label>☀️ 日当たり <span class="hint">（<b id="vLight"></b>）</span></label><input type="range" id="kLight" min="0" max="100" step="5" value="70"></div>
      <div class="field"><label>光のくる向き</label><div class="pl-seg" id="plDir"><button type="button" data-v="-1">← 左から</button><button type="button" data-v="0" class="on">↓ 真上から</button><button type="button" data-v="1">右から →</button></div></div>
      <div class="field"><label>💧 水やり <span class="hint">（<b id="vWater"></b>）</span></label><input type="range" id="kWater" min="0" max="100" step="5" value="50"></div>
      <div class="field"><label>🧪 肥料 <span class="hint">（<b id="vFert"></b>）</span></label><input type="range" id="kFert" min="0" max="100" step="5" value="40"></div>
      <div class="field"><label>🌡 気温 <span class="hint">（<b id="vTemp"></b>）</span></label><input type="range" id="kTemp" min="0" max="40" step="1" value="22"></div>
    </div>

    <h2 style="margin:18px 0 10px;font-size:18px;">③ タネの形を決める（遺伝子）</h2>
    <p class="pl-hint">育てている途中で変えると、いま育っている植物の形がそのまま変わります。</p>
    <div class="pl-cols">
      <div class="field"><label>背の高さ <span class="hint">（<b id="vH"></b>）</span></label><input type="range" id="kH" min="0" max="100" step="1"></div>
      <div class="field"><label>枝分かれ <span class="hint">（<b id="vBr"></b>）</span></label><input type="range" id="kBr" min="0" max="100" step="1"></div>
      <div class="field"><label>枝の角度 <span class="hint">（<b id="vAng"></b>）</span></label><input type="range" id="kAng" min="20" max="65" step="1"></div>
      <div class="field"><label>葉の大きさ <span class="hint">（<b id="vLs"></b>）</span></label><input type="range" id="kLs" min="0" max="100" step="1"></div>
      <div class="field"><label>葉の形</label><div class="pl-seg" id="plLeaf"></div></div>
      <div class="field"><label>葉のつき方</label><div class="pl-seg" id="plOpp"><button type="button" data-v="0">互い違い</button><button type="button" data-v="1">向かい合わせ</button></div></div>
      <div class="field"><label>花の色 <span id="vHue"></span></label><input type="range" id="kHue" min="0" max="359" step="1"></div>
      <div class="field"><label>花びらの数 <span class="hint">（<b id="vPet"></b>）</span></label><input type="range" id="kPet" min="3" max="12" step="1"></div>
      <div class="field"><label>光にむかう力 <span class="hint">（<b id="vPhoto"></b>）</span></label><input type="range" id="kPhoto" min="0" max="100" step="1"></div>
    </div>

    <h2 style="margin:18px 0 6px;font-size:18px;">④ 図鑑とかけ合わせ</h2>
    <p class="pl-hint">花が咲いたら「🌰 タネをとる」で保存（12まで・このブラウザの中だけ）。2つを「親にする」で選んで、かけ合わせてみましょう。</p>
    <p class="pl-hint" id="plBookEmpty">まだ何も保存されていません。</p>
    <div class="pl-book" id="plBook"></div>
    <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-top:10px">
      <button class="btn btn-primary" id="plCross" type="button" style="width:auto;padding:10px 18px;" disabled>🧬 かけ合わせる</button>
      <span class="pl-hint" id="plCrossNote" style="margin:0"></span>
    </div>

    <div style="text-align:center;margin-top:16px;"><span id="shareCount" class="share-count" style="display:none"></span></div>
    <div class="share-row">
      <button class="btn btn-x" id="shareBtn">𝕏 で植物をシェア</button>
      <button class="btn btn-ghost" id="copyBtn">結果をコピー</button>
    </div>
  </section>
"""

JS = r"""
(() => {
  const $ = id => document.getElementById(id);
  const cv = $('pl'), ctx = cv.getContext('2d'), gc = $('plG'), gx = gc.getContext('2d');
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const angDiff = (t, a) => { let d = t - a; while (d > Math.PI) d -= 2 * Math.PI; while (d < -Math.PI) d += 2 * Math.PI; return d; };
  function rng(s) { s = s >>> 0; return () => { s = (s + 0x6D2B79F5) >>> 0; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }

  // ---------- たね（遺伝子）と環境 ----------
  const LEAVES = [['round', 'まる'], ['narrow', 'ほそなが'], ['saw', 'ギザギザ'], ['heart', 'ハート']];
  const SEEDS = [
    ['🌻', '背高のっぽ', { h: .95, br: .12, ang: 30, leaf: 'heart', opp: 0, ls: .85, hue: 48, pet: 12, photo: .8 }],
    ['🌿', 'しげみ', { h: .3, br: .95, ang: 52, leaf: 'narrow', opp: 0, ls: .35, hue: 275, pet: 5, photo: .3 }],
    ['🌸', 'さくら色', { h: .55, br: .6, ang: 38, leaf: 'saw', opp: 0, ls: .5, hue: 338, pet: 5, photo: .5 }],
    ['🍀', 'まるまる', { h: .2, br: .7, ang: 45, leaf: 'round', opp: 1, ls: .6, hue: 205, pet: 4, photo: .4 }],
  ];
  let g = Object.assign({ seed: 1000 + 2 * 7919 }, SEEDS[2][2]);
  const env = { light: 70, dir: 0, water: 50, fert: 40, temp: 22 };
  let day = 0, G = 0, health = 1, etiol = .1, lightAvg = 70, dirAvg = 0, bloomed = false, playing = true, speed = 1, acc = 0, hist = [], ended = false;
  let topo = null, nameEdited = false;

  // ---------- 形（どこに枝・葉・花がつくか）はたねで決まる ----------
  const DT = .055;
  function buildTopo() {
    const R = rng(g.seed);
    function stem(depth, t0, n) {
      const s = { depth, t0, n, kids: [], wob: [] };
      for (let i = 0; i < n; i++) {
        s.wob.push((R() - .5) * .5);
        const p = g.br * (depth === 0 ? .6 : depth === 1 ? .38 : 0);
        const r1 = R(), r2 = R(), r3 = R();
        if (i >= 1 && i < n - 1 && r1 < p) {
          const kn = Math.max(2, Math.round((n - i) * (.45 + r2 * .35)));
          s.kids.push({ at: i, side: g.opp ? (r3 < .5 ? -1 : 1) : (i % 2 ? 1 : -1), stem: stem(depth + 1, t0 + (i + 1) * DT + .05, kn) });
        }
      }
      return s;
    }
    topo = stem(0, .02, 6 + Math.round(g.h * 9));
  }

  // ---------- 育ち方は環境で決まる ----------
  function factors() {
    const fL = Math.max(.04, Math.pow(env.light / 100, .7));
    const w = env.water, fW = w < 30 ? Math.max(.05, w / 30) : w > 70 ? Math.max(.12, 1 - (w - 70) / 30 * .88) : 1;
    const fT = Math.exp(-Math.pow((env.temp - 24) / 9, 2));
    const fN = .45 + .55 * Math.min(1, env.fert / 50);
    const burn = env.fert > 80 ? (env.fert - 80) / 20 * .65 : 0;
    return { fL, fW, fT, fN, burn };
  }
  function stepDay(dd) {
    const f = factors();
    const hT = Math.max(.05, Math.min(f.fW, Math.sqrt(f.fT), 1 - f.burn) * (env.light < 8 ? .75 : 1));
    health += (hT - health) * Math.min(1, .18 * dd);
    etiol += ((1 - env.light / 100) * (env.light < 50 ? 1 : .3) - etiol) * Math.min(1, .08 * dd);
    lightAvg += (env.light - lightAvg) * Math.min(1, .1 * dd);
    dirAvg += (env.dir - dirAvg) * Math.min(1, .12 * dd);
    G += .028 * f.fL * f.fW * f.fT * f.fN * health * dd;
    const d0 = Math.floor(day); day += dd;
    if (!bloomed && G > .5 && lightAvg >= 35 && env.temp >= 12 && health > .4) bloomed = true;
    if (bloomed && health < .25) bloomed = false;
    if (Math.floor(day) > d0) { const m = geom(); hist.push([Math.floor(day), m.h, health]); }
    if (day >= 120 && !ended) { ended = true; playing = false; updPlay(); flash('120日たちました。タネをとるか、育てなおしてみましょう'); }
  }

  // ---------- 形を計算（cm） ----------
  function geom() {
    const segs = [], leaves = [], flowers = [];
    const fN = Math.min(1, env.fert / 40);
    const Ln = (1.5 + g.h * 2.3) * (1 + etiol * .9) * (.75 + .25 * Math.min(1, env.fert / 50));
    const lightA = -Math.PI / 2 + dirAvg * .75;
    const droop = 1 - health;
    const hue = 112 - (1 - fN) * 50 - droop * 45, sat = 52 - droop * 22 + (1 - fN) * 8, lit = 34 + etiol * 22 + (1 - fN) * 10;
    const leafCol = `hsl(${hue.toFixed(0)},${clamp(sat, 15, 70).toFixed(0)}%,${clamp(lit, 25, 70).toFixed(0)}%)`;
    const stemCol = `hsl(${(hue + 5).toFixed(0)},${clamp(sat - 10, 12, 60).toFixed(0)}%,${clamp(lit - 4, 22, 62).toFixed(0)}%)`;
    let minX = 0, maxX = 0, minY = 0;
    function walk(s, x, y, a, w0) {
      for (let i = 0; i < s.n; i++) {
        const T = s.t0 + i * DT, age = G - T; if (age <= 0) return;
        const k = Math.min(1, age / .1);
        const len = Ln * k * (s.depth ? .82 : 1);
        a += s.wob[i] * (1 - g.photo * .6) * .5;
        a += angDiff(lightA, a) * (.04 + .22 * g.photo);
        if (s.depth) a += angDiff(Math.PI / 2, a) * droop * .07;
        const x2 = x + Math.cos(a) * len, y2 = y + Math.sin(a) * len;
        const wd = Math.max(.1, w0 * (1 - i / s.n * .55)) * (1 - etiol * .4);
        segs.push([x, y, x2, y2, wd]);
        minX = Math.min(minX, x2); maxX = Math.max(maxX, x2); minY = Math.min(minY, y2);
        const la = age - .03;
        if (la > 0) {
          const lk = Math.min(1, la / .15);
          const sz = (1.4 + g.ls * 3.2) * lk * (1 - etiol * .35) * (s.depth ? .85 : 1) * (.7 + .3 * fN) * (1 - droop * .15);
          const sides = g.opp ? [-1, 1] : [i % 2 ? 1 : -1];
          for (const sd of sides) {
            let a2 = a + sd * (1.05 - .3 * lk);
            a2 += angDiff(Math.PI / 2, a2) * droop * .65;
            leaves.push([x2, y2, a2, sz]);
            minX = Math.min(minX, x2 + Math.cos(a2) * sz); maxX = Math.max(maxX, x2 + Math.cos(a2) * sz); minY = Math.min(minY, y2 + Math.sin(a2) * sz);
          }
        }
        for (const kd of s.kids) if (kd.at === i) walk(kd.stem, x2, y2, a + kd.side * g.ang * Math.PI / 180, wd * .72);
        x = x2; y = y2;
      }
      const fa = G - (s.t0 + s.n * DT) - .05;
      if (fa > 0 && G > .45) {
        const fk = Math.min(1, fa / .12), open = bloomed ? fk : Math.min(fk, .3);
        const fr = (1.1 + g.ls * .6 + (s.depth ? 0 : .5)) * Math.max(.3, open);
        flowers.push([x, y, a, fr, open]);
        minY = Math.min(minY, y - fr); minX = Math.min(minX, x - fr); maxX = Math.max(maxX, x + fr);
      }
    }
    walk(topo, 0, 0, -Math.PI / 2, .5 + g.h * .3);
    const open = flowers.filter(q => q[4] > .4).length;
    return { segs, leaves, flowers, leafCol, stemCol, minX, maxX, minY, h: -minY, open };
  }

  // ---------- 描く ----------
  let dpr = 1, Sv = 0;
  function size() {
    const w = cv.clientWidth || 600; dpr = Math.min(2, window.devicePixelRatio || 1);
    const W = Math.round(w * dpr), Hh = Math.round(w * .8 * dpr); if (cv.width !== W || cv.height !== Hh) { cv.width = W; cv.height = Hh; }
    const gw = gc.clientWidth || 600; if (gc.width !== Math.round(gw * dpr)) { gc.width = Math.round(gw * dpr); gc.height = Math.round(110 * dpr); }
  }
  const mixc = (a, b, t) => a.map((v, i) => Math.round(v + (b[i] - v) * t));
  function leafPath(c, L, type) {
    c.beginPath();
    if (type === 'narrow') { L *= 1.3; const w = L * .16; c.moveTo(0, 0); c.bezierCurveTo(L * .3, -w * 1.4, L * .7, -w, L, 0); c.bezierCurveTo(L * .7, w, L * .3, w * 1.4, 0, 0); return L; }
    if (type === 'heart') { const w = L * .5; c.moveTo(L * .14, 0); c.bezierCurveTo(-L * .08, -w * 1.15, L * .62, -w * 1.1, L, 0); c.bezierCurveTo(L * .62, w * 1.1, -L * .08, w * 1.15, L * .14, 0); return L; }
    if (type === 'saw') {
      const w = L * .34, N = 9; c.moveTo(0, 0);
      for (let j = 1; j <= N; j++) { const t = j / N, e = Math.pow(Math.sin(Math.PI * t), .8) * w; c.lineTo(L * (t - .5 / N), -e * 1.18); c.lineTo(L * t, -e * .82); }
      for (let j = N; j >= 1; j--) { const t = j / N, e = Math.pow(Math.sin(Math.PI * t), .8) * w; c.lineTo(L * t, e * .82); c.lineTo(L * (t - .5 / N), e * 1.18); }
      c.closePath(); return L;
    }
    const w = L * .42; c.moveTo(0, 0); c.bezierCurveTo(L * .2, -w * 1.2, L * .8, -w * 1.1, L, 0); c.bezierCurveTo(L * .8, w * 1.1, L * .2, w * 1.2, 0, 0); return L;
  }
  let last = null;
  function draw() {
    size();
    const c = ctx, W = cv.width, Hh = cv.height;
    const m = geom(); last = m;
    // 空と日ざし
    c.setTransform(1, 0, 0, 1, 0, 0);
    const t = env.light / 100;
    const sky = c.createLinearGradient(0, 0, 0, Hh);
    sky.addColorStop(0, `rgb(${mixc([100, 116, 139], [125, 211, 252], t)})`); sky.addColorStop(1, `rgb(${mixc([203, 213, 225], [240, 249, 255], t)})`);
    c.fillStyle = sky; c.fillRect(0, 0, W, Hh);
    if (env.light > 3) {
      const sx = W * (.5 + env.dir * .38), sy = Hh * .2, sr = (10 + 16 * t) * dpr;
      c.fillStyle = `rgba(253,224,71,${.25 + .6 * t})`; c.beginPath(); c.arc(sx, sy, sr, 0, 7); c.fill();
      c.strokeStyle = `rgba(250,204,21,${.2 + .4 * t})`; c.lineWidth = 2 * dpr;
      for (let k = 0; k < 10; k++) { const a = k / 10 * Math.PI * 2; c.beginPath(); c.moveTo(sx + Math.cos(a) * sr * 1.3, sy + Math.sin(a) * sr * 1.3); c.lineTo(sx + Math.cos(a) * sr * 1.8, sy + Math.sin(a) * sr * 1.8); c.stroke(); }
    }
    // 大きさに合わせてズーム
    const groundY = Hh * .8, cx = W / 2;
    const spanH = Math.max(26, m.h + 4), spanW = Math.max(30, 2 * Math.max(-m.minX, m.maxX) + 6);
    const S = Math.min(groundY * .8 / spanH, W * .94 / spanW);
    Sv = Sv ? Sv + (S - Sv) * .12 : S;
    // 目もり
    c.fillStyle = 'rgba(15,23,42,.6)'; c.strokeStyle = 'rgba(15,23,42,.3)'; c.lineWidth = 1 * dpr; c.font = `${11 * dpr}px system-ui,sans-serif`; c.textAlign = 'left'; c.textBaseline = 'middle';
    const step = Sv * 10 < 26 * dpr ? 20 : 10;
    for (let k = step; groundY - k * Sv > 8 * dpr; k += step) { const y = groundY - k * Sv; c.beginPath(); c.moveTo(0, y); c.lineTo(10 * dpr, y); c.stroke(); c.fillText(k + 'cm', 13 * dpr, y); }
    // 鉢と土
    c.setTransform(Sv, 0, 0, Sv, cx, groundY);
    const wet = env.water / 100;
    c.fillStyle = '#c2410c'; c.beginPath(); c.moveTo(-8, -.6); c.lineTo(8, -.6); c.lineTo(6, 10); c.lineTo(-6, 10); c.closePath(); c.fill();
    c.fillStyle = '#9a3412'; c.fillRect(-8.6, -.9, 17.2, 2.2);
    c.fillStyle = `rgb(${mixc([196, 160, 118], [70, 48, 34], wet)})`; c.fillRect(-7.8, -.5, 15.6, 1.1);
    if (env.water > 85) { c.fillStyle = 'rgba(96,165,250,.7)'; c.fillRect(-7.8, -.55, 15.6, .45); }
    if (env.fert > 5) { c.fillStyle = '#f1f5f9'; const R = rng(7); for (let k = 0; k < Math.round(env.fert / 12); k++) { c.beginPath(); c.arc(-7 + R() * 14, -.2 + R() * .5, .22, 0, 7); c.fill(); } }
    // 茎
    c.lineCap = 'round'; c.strokeStyle = m.stemCol;
    m.segs.forEach(s => { c.lineWidth = s[4]; c.beginPath(); c.moveTo(s[0], s[1]); c.lineTo(s[2], s[3]); c.stroke(); });
    // 葉
    m.leaves.forEach(l => {
      c.save(); c.translate(l[0], l[1]); c.rotate(l[2]);
      c.strokeStyle = m.stemCol; c.lineWidth = .1; c.beginPath(); c.moveTo(0, 0); c.lineTo(l[3] * .14, 0); c.stroke();
      c.fillStyle = m.leafCol; const L = leafPath(c, l[3], g.leaf); c.fill();
      c.strokeStyle = 'rgba(255,255,255,.35)'; c.lineWidth = .07; c.beginPath(); c.moveTo(l[3] * .1, 0); c.lineTo(L * .85, 0); c.stroke();
      c.restore();
    });
    // 花（つぼみ → 開く）
    const wilt = health < .4;
    m.flowers.forEach(fl => {
      const [x, y, a, r, open] = fl;
      c.save(); c.translate(x, y);
      if (open < .35) {
        c.rotate(a + Math.PI / 2);
        c.fillStyle = `hsl(${g.hue},55%,${45 + open * 40}%)`; c.beginPath(); c.ellipse(0, -r * .5, r * .45, r * .8, 0, 0, 7); c.fill();
        c.fillStyle = m.stemCol; c.beginPath(); c.ellipse(0, -r * .1, r * .5, r * .35, 0, 0, 7); c.fill();
        c.restore(); return;
      }
      const n = g.pet, pr = r * (.55 + .45 * open);
      c.fillStyle = `hsl(${g.hue},${wilt ? 35 : 78}%,${wilt ? 55 : 63}%)`; c.strokeStyle = `hsla(${g.hue},70%,38%,.5)`; c.lineWidth = .06;
      for (let k = 0; k < n; k++) { const pa = k / n * Math.PI * 2 + a; c.save(); c.rotate(pa); c.beginPath(); c.ellipse(pr * .55, 0, pr * .55, pr * Math.min(.32, 1.6 / n + .08), 0, 0, 7); c.fill(); c.stroke(); c.restore(); }
      c.fillStyle = (g.hue > 35 && g.hue < 70) ? '#78350f' : '#facc15'; c.beginPath(); c.arc(0, 0, pr * .28, 0, 7); c.fill();
      c.restore();
    });
    ui(m);
    drawGraph();
  }
  function drawGraph() {
    const c = gx, W = gc.width, Hh = gc.height, p = 30 * dpr;
    c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, W, Hh);
    const maxD = Math.max(30, Math.ceil(day / 10) * 10), maxH = Math.max(20, Math.ceil(Math.max(0, ...hist.map(q => q[1])) / 10) * 10);
    const X = d => p + d / maxD * (W - p - 8 * dpr), Y = (v, mx) => Hh - 20 * dpr - v / mx * (Hh - 32 * dpr);
    c.strokeStyle = '#e2e8f0'; c.lineWidth = 1 * dpr; c.fillStyle = '#64748b'; c.font = `${10 * dpr}px system-ui,sans-serif`;
    c.textAlign = 'right'; c.textBaseline = 'middle';
    [0, .5, 1].forEach(f => { const y = Y(f, 1); c.beginPath(); c.moveTo(p, y); c.lineTo(W - 8 * dpr, y); c.stroke(); c.fillText(Math.round(maxH * f) + 'cm', p - 3 * dpr, y); });
    c.textAlign = 'center'; c.textBaseline = 'top';
    for (let d = 0; d <= maxD; d += maxD > 60 ? 20 : 10) c.fillText(d + '日', X(d), Hh - 15 * dpr);
    c.lineWidth = 2.2 * dpr; c.strokeStyle = '#16a34a'; c.beginPath(); hist.forEach((q, i) => i ? c.lineTo(X(q[0]), Y(q[1], maxH)) : c.moveTo(X(q[0]), Y(q[1], maxH))); c.stroke();
    c.lineWidth = 1.4 * dpr; c.strokeStyle = '#f97316'; c.setLineDash([4 * dpr, 3 * dpr]); c.beginPath(); hist.forEach((q, i) => i ? c.lineTo(X(q[0]), Y(q[2], 1)) : c.moveTo(X(q[0]), Y(q[2], 1))); c.stroke(); c.setLineDash([]);
  }

  // ---------- 数字とひとこと ----------
  function advice(m) {
    if (env.water < 20) return ['🥀', '土がカラカラです。葉がしおれてきました。水やりを増やしましょう。'];
    if (env.water > 80) return ['🫧', '水が多すぎて、根が息をできずに弱っています（根ぐされ）。水やりを減らしましょう。'];
    if (env.fert > 85) return ['🧂', '肥料が多すぎて、根がいたんでいます（肥料やけ）。'];
    if (env.temp < 10) return ['🥶', '寒すぎて、ほとんど育ちません。'];
    if (env.temp > 33) return ['🥵', '暑すぎて、ぐったりしています。'];
    if (env.light < 30 && G > .15) return ['🌑', '光が足りず、茎がひょろひょろ伸びて、葉の色もうすくなっています（徒長）。'];
    if (env.fert < 15 && G > .2) return ['🍂', '肥料が足りず、葉が黄色っぽくなっています。'];
    if (G > .5 && !bloomed && lightAvg < 35) return ['🌥', '大きくはなりましたが、光が足りなくて花が咲きません。'];
    if (bloomed && m.open > 0) return ['🌼', `花が${m.open}つ咲きました！「🌰 タネをとる」で図鑑に保存できます。`];
    if (env.dir !== 0 && G > .2 && g.photo > .3) return ['☀️', '光のくる方へ、茎が曲がって伸びています（光屈性）。'];
    if (G < .02) return ['🌱', 'タネをまきました。日にちが進むと芽が出ます。'];
    return ['🌱', 'すくすく育っています。'];
  }
  let lastUI = 0;
  function ui(m) {
    const now = performance.now(); if (now - lastUI < 200) return; lastUI = now;
    $('mDay').innerHTML = Math.floor(day) + '<small>日目</small>';
    $('mH').innerHTML = m.h.toFixed(1) + '<small>cm</small>';
    $('mLeaf').innerHTML = m.leaves.length + '<small>枚</small>';
    $('mFl').innerHTML = m.open + '<small>つ</small>';
    $('mHp').innerHTML = Math.round(health * 100) + '<small>%</small>';
    $('mHpBox').classList.toggle('warn', health < .6);
    const [e, s] = advice(m); $('plNote').textContent = e + ' ' + s;
    $('plSeed').disabled = !(bloomed && m.open > 0);
  }

  // ---------- 名前 ----------
  function autoName() {
    const h = g.hue, col = h < 15 || h >= 345 ? 'アカ' : h < 40 ? 'ダイダイ' : h < 70 ? 'キ' : h < 160 ? 'ミドリ' : h < 200 ? 'ミズイロ' : h < 250 ? 'アオ' : h < 300 ? 'ムラサキ' : 'モモイロ';
    const lf = { round: 'マルバ', narrow: 'ホソバ', saw: 'ギザバ', heart: 'ハートバ' }[g.leaf];
    return (g.h > .75 ? 'オオ' : g.h < .3 ? 'ヒメ' : '') + col + lf + (g.br > .75 ? 'ムラ' : '') + 'ソウ';
  }
  function setName() { if (!nameEdited) $('plName').value = autoName(); }

  // ---------- 操作 ----------
  function flash(s) { const el = $('plMsg'); el.textContent = s; el.classList.add('show'); clearTimeout(flash.t); flash.t = setTimeout(() => el.classList.remove('show'), 2400); }
  function restart(msg) { day = 0; G = 0; health = 1; etiol = .1; lightAvg = env.light; dirAvg = env.dir; bloomed = false; hist = [[0, 0, 1]]; ended = false; playing = true; acc = 0; Sv = 0; buildTopo(); updPlay(); if (msg) flash(msg); }
  function updPlay() { $('plPlay').textContent = playing ? '⏸ 止める' : '▶ 育てる'; document.querySelectorAll('[data-sp]').forEach(b => b.classList.toggle('on', +b.dataset.sp === speed)); }
  const lv3 = (v, a) => a[v < .34 ? 0 : v < .67 ? 1 : 2];
  function syncGenes() {
    const set = (id, v, txt) => { $(id).value = v; if (txt != null) $('v' + id.slice(1)).textContent = txt; };
    set('kH', Math.round(g.h * 100), lv3(g.h, ['ひくい', 'ふつう', 'たかい']));
    set('kBr', Math.round(g.br * 100), lv3(g.br, ['少ない', 'ふつう', '多い']));
    set('kAng', g.ang, g.ang + '°'); set('kLs', Math.round(g.ls * 100), lv3(g.ls, ['小さい', 'ふつう', '大きい']));
    set('kHue', g.hue, null); $('vHue').style.background = `hsl(${g.hue},78%,63%)`;
    set('kPet', g.pet, g.pet + '枚'); set('kPhoto', Math.round(g.photo * 100), lv3(g.photo, ['弱い', 'ふつう', '強い']));
    document.querySelectorAll('#plLeaf button').forEach(b => b.classList.toggle('on', b.dataset.v === g.leaf));
    document.querySelectorAll('#plOpp button').forEach(b => b.classList.toggle('on', +b.dataset.v === g.opp));
    setName();
  }
  function bindG(id, key, f) { $(id).addEventListener('input', e => { g[key] = f(+e.target.value); buildTopo(); syncGenes(); }); }
  bindG('kH', 'h', v => v / 100); bindG('kBr', 'br', v => v / 100); bindG('kAng', 'ang', v => v); bindG('kLs', 'ls', v => v / 100);
  bindG('kHue', 'hue', v => v); bindG('kPet', 'pet', v => v); bindG('kPhoto', 'photo', v => v / 100);
  $('plLeaf').innerHTML = LEAVES.map(([k, n]) => `<button type="button" data-v="${k}">${n}</button>`).join('');
  $('plLeaf').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; g.leaf = b.dataset.v; syncGenes(); });
  $('plOpp').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; g.opp = +b.dataset.v; buildTopo(); syncGenes(); });
  $('plSeeds').innerHTML = SEEDS.map(([e, n], i) => `<button type="button" data-i="${i}">${e} ${n}</button>`).join('') + '<button type="button" data-i="r">🎲 ランダム</button>';
  $('plSeeds').addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    g = b.dataset.i === 'r' ? randGenes() : Object.assign({ seed: 1000 + +b.dataset.i * 7919 }, SEEDS[+b.dataset.i][2]);
    nameEdited = false; syncGenes(); restart('新しいタネをまきました');
  });
  function randGenes() { const R = Math.random; return { h: R(), br: R(), ang: 20 + Math.round(R() * 45), leaf: LEAVES[Math.floor(R() * 4)][0], opp: R() < .3 ? 1 : 0, ls: R(), hue: Math.round(R() * 359), pet: 3 + Math.floor(R() * 10), photo: R(), seed: Math.floor(R() * 1e9) }; }
  const envB = [
    ['kLight', 'light', v => v + '（' + (v < 25 ? '日かげ' : v < 60 ? '明るい日かげ' : 'ひなた') + '）'],
    ['kWater', 'water', v => v < 20 ? '少なすぎ' : v < 30 ? '少なめ' : v <= 70 ? 'ちょうどよい' : v <= 80 ? '多め' : '多すぎ'],
    ['kFert', 'fert', v => v < 15 ? 'ほとんどなし' : v < 50 ? '少し' : v <= 80 ? 'たっぷり' : '多すぎ'],
    ['kTemp', 'temp', v => v + '℃'],
  ];
  envB.forEach(([id, key, f]) => { const el = $(id), out = $('v' + id.slice(1)); const up = () => { env[key] = +el.value; out.textContent = f(env[key]); }; el.addEventListener('input', up); up(); });
  $('plDir').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; env.dir = +b.dataset.v; document.querySelectorAll('#plDir button').forEach(x => x.classList.toggle('on', x === b)); });
  $('plPlay').addEventListener('click', () => { if (ended) { flash('120日たちました。「タネから育てなおす」で、もう一度育てられます'); return; } playing = !playing; updPlay(); });
  document.querySelectorAll('[data-sp]').forEach(b => b.addEventListener('click', () => { speed = +b.dataset.sp; if (!ended) playing = true; updPlay(); }));
  $('plRestart').addEventListener('click', () => restart('タネから育てなおします'));
  $('plFast').addEventListener('click', () => { if (day >= 50) { flash('もう50日をこえています'); return; } let n = 0; while (day < 50 && n < 400) { stepDay(.25); n++; } flash('50日目まで進めました'); });
  $('plName').addEventListener('input', () => { nameEdited = $('plName').value.trim() !== ''; if (!nameEdited) setName(); });

  // ---------- 図鑑とかけ合わせ ----------
  const KEY = 'shimulabo_plants_v1';
  const loadBook = () => { try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { return []; } };
  const saveBook = b => { try { localStorage.setItem(KEY, JSON.stringify(b)); return true; } catch (e) { flash('保存できませんでした（ブラウザの設定を確認してください）'); return false; } };
  let pick = [];
  function thumb() { const t = document.createElement('canvas'); t.width = 160; t.height = 128; t.getContext('2d').drawImage(cv, 0, 0, 160, 128); return t.toDataURL('image/jpeg', .7); }
  $('plSeed').addEventListener('click', () => {
    const b = loadBook(); if (b.length >= 12) { flash('図鑑はいっぱいです（12まで）。どれかを消してください'); return; }
    const m = last; b.unshift({ name: $('plName').value.trim() || autoName(), g: Object.assign({}, g), h: +m.h.toFixed(1), f: m.open, day: Math.floor(day), img: thumb() });
    pick = pick.map(i => i + 1);
    if (saveBook(b)) { renderBook(); flash('タネをとって図鑑に保存しました🌱'); }
  });
  function esc(s) { return String(s).replace(/[&<>"']/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch])); }
  function renderBook() {
    const b = loadBook(); pick = pick.filter(i => i < b.length);
    $('plBookEmpty').style.display = b.length ? 'none' : '';
    $('plBook').innerHTML = b.map((p, i) => `<div class="pl-card${pick.includes(i) ? ' on' : ''}" data-i="${i}"><img src="${p.img}" alt="${esc(p.name)}" width="160" height="128"><b>${esc(p.name)}</b><span>${p.h}cm・花${p.f}つ・${p.day}日</span><div class="pl-cbtn"><button type="button" data-a="grow">育てる</button><button type="button" data-a="pick">${pick.includes(i) ? '✔ 親' : '親にする'}</button><button type="button" data-a="del" aria-label="消す">🗑</button></div></div>`).join('');
    $('plCross').disabled = pick.length !== 2;
    $('plCrossNote').textContent = pick.length === 2 ? `「${b[pick[0]].name}」×「${b[pick[1]].name}」をかけ合わせます` : `図鑑から親を2つ選んでください（いま${pick.length}つ）`;
  }
  $('plBook').addEventListener('click', e => {
    const btn = e.target.closest('button'), card = e.target.closest('.pl-card'); if (!btn || !card) return;
    const i = +card.dataset.i, b = loadBook(), p = b[i]; if (!p) return;
    if (btn.dataset.a === 'grow') { g = Object.assign({}, p.g); $('plName').value = p.name; nameEdited = true; syncGenes(); restart(`「${p.name}」のタネをまきました`); $('plWrap').scrollIntoView({ behavior: 'smooth', block: 'center' }); }
    if (btn.dataset.a === 'pick') { pick = pick.includes(i) ? pick.filter(x => x !== i) : pick.concat(i).slice(-2); renderBook(); }
    if (btn.dataset.a === 'del') { if (!confirm(`「${p.name}」を図鑑から消しますか？`)) return; b.splice(i, 1); pick = []; saveBook(b); renderBook(); }
  });
  function cross(a, b) {
    const R = Math.random, one = (x, y) => R() < .5 ? x : y, mix = (x, y, lo, hi, j) => clamp((x + y) / 2 + (R() - .5) * j, lo, hi);
    const hd = ((b.hue - a.hue + 540) % 360) - 180;
    const c = { h: mix(a.h, b.h, 0, 1, .2), br: mix(a.br, b.br, 0, 1, .2), ang: Math.round(mix(a.ang, b.ang, 20, 65, 8)), leaf: one(a.leaf, b.leaf), opp: one(a.opp, b.opp), ls: mix(a.ls, b.ls, 0, 1, .2),
      hue: Math.round(((R() < .5 ? one(a.hue, b.hue) : a.hue + hd / 2) + (R() - .5) * 24 + 720) % 360), pet: Math.round(clamp(one(a.pet, b.pet) + (R() < .3 ? (R() < .5 ? -1 : 1) : 0), 3, 12)), photo: mix(a.photo, b.photo, 0, 1, .15), seed: Math.floor(R() * 1e9) };
    let mut = null;
    if (R() < .1) { const r = randGenes(), keys = ['hue', 'leaf', 'pet', 'h', 'br'], k = keys[Math.floor(R() * keys.length)]; c[k] = r[k]; mut = { hue: '花の色', leaf: '葉の形', pet: '花びらの数', h: '背の高さ', br: '枝分かれ' }[k]; }
    return [c, mut];
  }
  $('plCross').addEventListener('click', () => {
    const b = loadBook(); if (pick.length !== 2) return;
    const [c, mut] = cross(b[pick[0]].g, b[pick[1]].g);
    g = c; nameEdited = false; syncGenes(); restart(mut ? `とつぜん変異！「${mut}」が親とちがう子どもが生まれました` : 'かけ合わせた子どものタネをまきました');
    $('plWrap').scrollIntoView({ behavior: 'smooth', block: 'center' });
  });

  // ---------- シェア ----------
  function shareText() { const m = last || geom(); return `自分だけの植物「${$('plName').value.trim() || autoName()}」を${Math.floor(day)}日育てたら、草たけ${m.h.toFixed(0)}cm・葉${m.leaves.length}枚・花${m.open}つになりました🌱`; }
  $('shareBtn').addEventListener('click', () => { const u = location.origin + location.pathname; window.open('https://twitter.com/intent/tweet?text=' + encodeURIComponent(shareText() + '\n') + '&url=' + encodeURIComponent(u) + '&hashtags=' + encodeURIComponent('シミュラボ'), '_blank', 'noopener'); });
  $('copyBtn').addEventListener('click', async () => { try { await navigator.clipboard.writeText(shareText() + '\n' + location.origin + location.pathname); flash('コピーしました'); } catch (e) { flash('コピーできませんでした'); } });

  // ---------- 動かす ----------
  let tPrev = performance.now();
  function loop(now) {
    const dt = Math.min(.1, (now - tPrev) / 1000); tPrev = now;
    if (playing && !ended) { acc += dt * speed * 1.5; let n = 0; while (acc >= .25 && n < 60) { stepDay(.25); acc -= .25; n++; } }
    draw(); requestAnimationFrame(loop);
  }
  syncGenes(); restart(); renderBook();
  window.addEventListener('resize', () => { Sv = 0; });
  requestAnimationFrame(loop);
  window.__pl = { get g() { return g; }, env, get G() { return G; }, get day() { return day; }, get health() { return health; }, get bloomed() { return bloomed; }, geom, step(n) { for (let i = 0; i < n; i++) stepDay(.25); lastUI = 0; draw(); }, restart, cross, setG(o) { Object.assign(g, o); buildTopo(); syncGenes(); } };
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
    <p class="pl-note" style="font-weight:400">{esc(NOTE)}</p>
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
