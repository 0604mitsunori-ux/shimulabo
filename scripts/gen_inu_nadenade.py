# -*- coding: utf-8 -*-
"""犬なでシミュレーター（2026-11-24）: 犬用ベッドの上の犬を、ただなでるだけの癒しページ。
   sims/inu-nadenade/index.html を書き出す（冪等）。 使い方: python -X utf8 scripts/gen_inu_nadenade.py
   絵はすべて WebGL のシェーダで計算（外部画像・外部ライブラリなし）。イラスト版は gen_inu_nadenade_illust_backup.py に残してある。"""
import html as H, io, json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://shimulabo.com"
SLUG = "inu-nadenade"
NAME = "犬なでシミュレーター"
CAT = "あそぶ・実験"
TITLE = "犬なでシミュレーター｜ただ、犬をなでるだけの癒しページ（毛並み・しっぽ・へそ天）｜シミュラボ"
DESC = ("日の当たる部屋で、犬用ベッドの上で休んでいる犬を、マウスや指でなでるだけのページです。なでた方向に毛並みがねて、頭・首・背中・おなか・前足・しっぽで反応が変わります。"
        "わき腹をなで続けるとへそ天に。犬のタイプ4種と毛色12種、体の大きさ・ふとさも変えられます。")
OG_T = "犬なでシミュレーター ただ、なでるだけ。"
OG_D = "ベッドの上の犬を、マウスや指でなでるだけ。なでた所の毛並みが変わり、場所ごとに反応がちがいます。"
H1 = "犬なでシミュレーター<br>ただ、なでるだけ。"
LEAD = "日の当たる部屋で、犬がのんびりしています。マウスや指でなぞって、なでてあげてください。"
NOTE = "🐾 本物の犬は1ぴきずつ好みがちがいます。知らない犬は、かならず飼い主さんに聞いてからさわりましょう。"

FAQ = [
    ("どうやって遊びますか？", "犬の絵をマウスや指でなぞるだけです。なでる場所（頭・首・背中・おなか・前足・しっぽ）によって、犬の反応が変わります。下のボタンで犬のタイプや毛色も変えられます。"),
    ("へそ天（おなかを見せるポーズ）にするには？", "体の横（わき腹）をなで続けると、ゴロンとあお向けになっておなかを見せます。そのままおなかを速くかくと、後ろ足がカカカッと動きます。しばらくさわらないと、もとの「ふせ」にもどります。"),
    ("なでた回数や時間は、どこに保存されますか？", "このブラウザの中（ローカルストレージ）だけに保存されます。サーバーには送られません。ブラウザの記録を消したり、別の端末で開いたりすると、数字は0にもどります。"),
    ("本物の犬も、同じように反応しますか？", "犬によってちがいます。このページの反応は、よく知られているしぐさをもとに作ったもので、すべての犬に当てはまるわけではありません。本物の犬をなでるときは、その犬の様子をよく見て、いやがっていたらやめましょう。"),
]
REL = [("neko-nemuri", "🐱", "猫が寝てる時間シミュレーター"), ("pet-age", "🐶", "犬・猫の年齢 人間換算シミュレーター"), ("purupuru-jelly", "🍮", "ぷるぷるゼリー")]

ARTICLE = """
<h2>犬はどこをなでられるのが好き？</h2>
<p>好きな場所は、犬によってちがいます。<b>あごの下・胸・肩のあたり</b>をなでられるのを好む犬が多いと言われています。</p>
<p>反対に、頭の上からいきなり手を出すと、こわがる犬がいます。足先やしっぽは、さわられるのが苦手な犬も少なくありません。このページの犬が、前足をそっと引っこめたり、しっぽをさわると体のほうへ巻いたりするのは、そのためです。</p>
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
<li><b>頭をなでる</b>：目を細めて、耳を後ろにねかせ、手に頭を寄せてきます。</li>
<li><b>首やほおの横をなでる</b>：頭をかたむけて、うっとりします。</li>
<li><b>背中をなでる</b>：しっぽの振り方が速くなります。</li>
<li><b>わき腹をなで続ける</b>：ゴロンとあお向けになります。速くかくと、後ろ足が動きます。</li>
<li><b>毛の流れと反対になでる</b>：毛が立って、なでたあとがしばらく残ります。</li>
<li><b>しばらく何もしない</b>：頭をこちらに向けたり、前足でトントンしたり、あくびをしたりします。</li>
</ul>
"""

REFS = [
    "環境省「動物の愛護と適切な管理」（環境省のウェブサイト）",
]

STAGE = r"""
<style>
#inuWrap{position:relative;border-radius:16px;overflow:hidden;border:1px solid var(--line);background:#8a6a48}
#inuCv{display:block;width:100%;aspect-ratio:3/2;touch-action:none;-webkit-user-select:none;user-select:none;-webkit-touch-callout:none}
#inuWrap.in-on #inuCv{cursor:grab}
.in-nogl{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;text-align:center;padding:20px;color:#fff;font-size:14px;font-weight:700;line-height:1.8}
.in-nogl[hidden]{display:none}
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
      <canvas id="inuCv" aria-label="日の当たる部屋の犬用ベッドの上で、ふせをしている犬を上から見た絵。なぞると、なでることができます"></canvas>
      <div class="in-nogl" id="inuNoGl" hidden>申し訳ありません。この端末では表示できません。<br>別のブラウザや端末でお試しください。</div>
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
  const cv = $('inuCv');
  const TAU = Math.PI * 2, clamp = (v, a, b) => Math.max(a, Math.min(b, v)), lerp = (a, b, t) => a + (b - a) * t;
  function rng(s) { s = s >>> 0; return () => { s = (s + 0x6D2B79F5) >>> 0; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
  const R01 = rng(20261124);

  // =====================================================================
  //  色・形の定義（ここを変えると見た目が変わる）
  // =====================================================================
  const KEY = 'shimulabo_inunade_v1';
  const NP = 24;                      // 体の部品（カプセル）の数。シェーダと同じ数にする
  const FW = 96, FH = 64;             // なでた向きを覚えるテクスチャの大きさ
  const FR = { x0: -300, y0: -200, w: 620, h: 400 };   // そのテクスチャが体のどこを覆うか（犬の座標）
  // 見た目のタイプ: ear=耳 / tail=しっぽ / hair=毛の長さ / len=胴の長さ / leg=足の長さ / head=頭の大きさ / snout=鼻先 / fluff=毛のふくらみ / cheek=ほおの幅
  const TYPES = {
    tachi: { name: '立ち耳・巻きしっぽ', ear: 'point', tail: 'curl', hair: 1, len: .96, leg: 1, head: 1.04, snout: .86, fluff: 0, cheek: 17 },
    tare: { name: 'たれ耳', ear: 'drop', tail: 'long', hair: .85, len: 1.04, leg: 1.04, head: 1.03, snout: 1.2, fluff: 0, cheek: 4 },
    fuwa: { name: 'ふわふわ長毛', ear: 'small', tail: 'plume', hair: 2.6, len: .9, leg: .8, head: 1.0, snout: .76, fluff: 7, cheek: 13 },
    tansoku: { name: '短足・胴長', ear: 'big', tail: 'short', hair: 1.1, len: 1.22, leg: .56, head: .98, snout: 1.05, fluff: 1, cheek: 7 },
  };
  const TYPE_IDS = Object.keys(TYPES);
  // 耳: b=つけ根 / t=先 / tb=後ろにねた時の先 / tr=あお向けの時の先 / rb,rt=太さ / hb,ht,htb=高さ / inner=内側が見える度合い
  const EARS = {
    point: { b: [-15, 27], t: [-1, 60], tb: [-38, 50], tr: [-20, 68], rb: 17, rt: 3, hb: 54, ht: 74, htb: 54, hm: .6, inner: 1 },
    drop: { b: [-10, 30], t: [22, 45], tb: [8, 52], tr: [-10, 70], rb: 15, rt: 8.5, hb: 46, ht: 20, htb: 16, hm: .9, inner: 0 },
    small: { b: [-14, 25], t: [-6, 52], tb: [-30, 44], tr: [-18, 56], rb: 15, rt: 3.5, hb: 56, ht: 72, htb: 54, hm: 1.1, inner: .7 },
    big: { b: [-12, 27], t: [0, 60], tb: [-32, 52], tr: [-20, 72], rb: 18, rt: 4.5, hb: 50, ht: 74, htb: 54, hm: .6, inner: 1 },
  };
  // しっぽ: n=節の数 / seg=節の長さ / a0=ふせの向き / a1=あお向けの向き / curl=巻き / rad=太さ / h=高さ / lag=しなり / amp=振れ幅 / stiff=根もとのかたさ / tuck=体へ巻く量
  const TAILS = {
    curl: { n: 6, seg: 17, a0: 2.2, a1: Math.PI + .5, curl: .75, uncurl: .75, root: .45, rad: k => 15 - 4 * k, h: k => 46 + 10 * Math.sin(Math.PI * k), lag: .15, amp: .16, stiff: .8, tuck: .25, hm: 1.3 },
    long: { n: 6, seg: 23, a0: Math.PI + .7, a1: Math.PI + .2, curl: -.26, uncurl: 0, root: .8, rad: k => 13.5 - 7 * k, h: k => 18 - 9 * k, lag: .5, amp: .5, stiff: .25, tuck: -.9, hm: .7 },
    plume: { n: 6, seg: 19, a0: 2.3, a1: Math.PI + .4, curl: .6, uncurl: .7, root: .45, rad: k => 15 + 9 * Math.sin(Math.PI * Math.min(1, k * 1.1)), h: k => 46 + 12 * Math.sin(Math.PI * k), lag: .2, amp: .2, stiff: .7, tuck: .3, hm: 2.2 },
    short: { n: 3, seg: 13, a0: Math.PI + .15, a1: Math.PI, curl: -.1, uncurl: 0, root: .8, rad: k => 12 - 4 * k, h: k => 22 - 8 * k, lag: .4, amp: .7, stiff: .5, tuck: -.6, hm: .8 },
  };
  // 毛色: base=地の色 / light=うらの色 / patch=ぶちの色 / pat=もよう（0=一色, 1=うら白, 2=茶のポイント, 3=茶白, 4=ぶち）/ collar=首輪の色
  const COATS = [
    { id: 'akacha', name: '赤茶', base: '#b9712f', light: '#eadcc4', pat: 1, collar: '#2f5d8a' },
    { id: 'kurocha', name: '黒＋茶', base: '#1c1817', light: '#b57a3c', pat: 2, collar: '#b8342c' },
    { id: 'shiro', name: '白', base: '#efe8dc', light: '#fbf7ef', pat: 0, collar: '#b8342c' },
    { id: 'cream', name: 'クリーム', base: '#dfc396', light: '#f5ead3', pat: 1, collar: '#3f7a5a' },
    { id: 'cha', name: '茶', base: '#8c5a30', light: '#b98a58', pat: 0, collar: '#2f5d8a' },
    { id: 'kin', name: '金', base: '#cf9a48', light: '#ecd3a0', pat: 0, collar: '#3a4f8c' },
    { id: 'gray', name: 'グレー', base: '#8b8a8c', light: '#c9c9cc', pat: 0, collar: '#b8342c' },
    { id: 'choco', name: 'チョコ', base: '#4a2c1c', light: '#76503a', pat: 0, collar: '#c9a23a' },
    { id: 'buchi', name: '白黒ぶち', base: '#efe9df', light: '#fbf7ef', patch: '#1c1918', pat: 4, collar: '#b8342c' },
    { id: 'chashiro', name: '茶白', base: '#a8642c', light: '#f6efe2', pat: 3, collar: '#2f6f6a' },
    { id: 'goma', name: 'ごま', base: '#9a7b55', light: '#efe2c9', pat: 1, fleck: 1, collar: '#b8342c' },
    { id: 'kuro', name: '黒', base: '#181516', light: '#3a3433', pat: 0, collar: '#c23b30' },
  ];
  const BED = { rx: 288, ry: 226, bw: 54, h: 30 };   // 犬用ベッド（だ円・ふちの太さ・ふちの高さ）
  const LIGHT = (() => { const v = [-.52, -.56, .65], n = Math.hypot(v[0], v[1], v[2]); return v.map(x => x / n); })();   // 光の向き（左上の窓から）
  const RES = [1, .8, .64, .5, .4, .3, .22];   // 重い端末で下げていく描画解像度

  // =====================================================================
  //  シェーダ（絵はすべてここで計算する）
  // =====================================================================
  const VS = 'attribute vec2 a;void main(){gl_Position=vec4(a,0.,1.);}';
  const FS = `
precision highp float;
#define NP 24
uniform vec2 uRes, uView;
uniform vec4 uA[NP], uB[NP], uC[NP], uD[NP];
uniform vec4 uDog, uDogS, uHead, uFace, uFace2, uCol, uCol2, uBed, uBedR, uHand, uHand2, uHandL, uFlowRect, uPat, uHair, uSun, uMisc, uBound;
uniform vec3 uBase, uUnder, uPatch, uCollarC, uL;
uniform sampler2D uNoise, uFlow;

float gH, gS; vec2 gFlow, gDisp, gZ, gW3; vec4 gW1, gW2; vec3 gQ;

vec2 rot(vec2 v,float a){float c=cos(a),s=sin(a);return vec2(c*v.x-s*v.y,s*v.x+c*v.y);}
float vn(vec2 p){return texture2D(uNoise,p/256.).a;}
float fbm(vec2 p){return vn(p)*.5+vn(p*2.07+vec2(17.3,5.1))*.25+vn(p*4.13+vec2(3.7,41.))*.125+vn(p*8.3+vec2(71.,13.))*.0625;}
float hash(vec2 c){return texture2D(uNoise,(floor(c)+.5)/256.).g;}
float smx(float a,float b,float k){float h=clamp(.5+.5*(b-a)/k,0.,1.);return mix(a,b,h)+k*h*(1.-h);}
float sdSeg(vec2 p,vec2 a,vec2 b,float r){vec2 ab=b-a,pa=p-a;float t=clamp(dot(pa,ab)/dot(ab,ab),0.,1.);return length(pa-ab*t)-r;}

// 体の高さ（かんたん版）: x=高さ, y=輪かくまでの距離（内側が正）
vec2 dogL(vec2 p){
  float h=-1e3,s=-1e3;
  for(int i=0;i<NP;i++){
    vec4 A=uA[i],B=uB[i];
    vec2 ab=A.zw-A.xy,pa=p-A.xy;
    float t=clamp(dot(pa,ab)/max(dot(ab,ab),1e-3),0.,1.);
    float d=length(pa-ab*t),r=mix(B.x,B.y,t),x=1.-d/r,H=mix(B.z,B.w,t);
    float v=x>0.?H*sqrt(x*(2.-x)):H*1.6*x;
    float k=uC[i].w;
    h=smx(h,v,k);s=smx(s,r-d,k*.5);
  }
  vec2 q=p-uHandL.xy;h-=uHandL.z*exp(-dot(q,q)/1500.);
  return vec2(h,s);
}
// 体の高さ（くわしい版）: 毛の流れ・部位・もよう用の座標もいっしょに求める
void dogF(vec2 p){
  float h=-1e3,s=-1e3;vec2 fl=vec2(-1.,0.),dsp=vec2(0.),Z=vec2(0.,1.),w3=vec2(0.);vec4 w1=vec4(0.),w2=vec4(0.);vec3 Q=vec3(0.);
  for(int i=0;i<NP;i++){
    vec4 A=uA[i],B=uB[i],C=uC[i],D=uD[i];
    vec2 ab=A.zw-A.xy,pa=p-A.xy;
    float t=clamp(dot(pa,ab)/max(dot(ab,ab),1e-3),0.,1.);
    vec2 pc=pa-ab*t;
    float d=length(pc),r=mix(B.x,B.y,t),x=1.-d/r,H=mix(B.z,B.w,t);
    float v=x>0.?H*sqrt(x*(2.-x)):H*1.6*x;
    float k=C.w;
    float m=clamp(.5+.5*(v-h)/k,0.,1.);
    h=mix(h,v,m)+k*m*(1.-m);
    s=smx(s,r-d,k*.5);
    float part=C.z;
    fl=mix(fl,C.xy,m);dsp=mix(dsp,D.xy,m);Z=mix(Z,D.zw,m);
    w1=mix(w1,max(vec4(0.),1.-abs(part-vec4(0.,1.,2.,3.))),m);
    w2=mix(w2,max(vec4(0.),1.-abs(part-vec4(4.,5.,6.,7.))),m);
    w3=mix(w3,max(vec2(0.),1.-abs(part-vec2(8.,9.))),m);
    Q=mix(Q,vec3((C.x*pc.y-C.y*pc.x)/r,dot(C.xy,pc)/r,t),m);
  }
  vec2 q=p-uHandL.xy;h-=uHandL.z*exp(-dot(q,q)/1500.);
  gH=h;gS=s;gFlow=fl;gDisp=dsp;gZ=Z;gW1=w1;gW2=w2;gW3=w3;gQ=Q;
}
// 毛のすじ: 流れにそってノイズを平均する
float lic(vec2 p,vec2 d,float tex,float sp,vec4 ch){
  float a=0.,ws=0.;
  for(int i=-6;i<=6;i++){float fi=float(i);float w=1.-abs(fi)/7.;a+=w*dot(texture2D(uNoise,(p+d*fi*tex*sp)/(tex*256.)),ch);ws+=w;}
  return a/ws;
}
float lic5(vec2 p,vec2 d,float tex,float sp,vec4 ch){
  float a=0.,ws=0.;
  for(int i=-3;i<=3;i++){float fi=float(i);float w=1.-abs(fi)/4.;a+=w*dot(texture2D(uNoise,(p+d*fi*tex*sp)/(tex*256.)),ch);ws+=w;}
  return a/ws;
}
// 体が落とす影
float shDog(vec2 pl,float z0,vec3 Ll){
  vec2 dir=normalize(Ll.xy);float slope=Ll.z/length(Ll.xy);float sh=1.;
  for(int i=0;i<4;i++){
    float fi=float(i);float t=5.+6.5*fi+2.6*fi*fi;
    float hz=dogL(pl+dir*t).x-(z0+t*slope);
    sh=min(sh,1.-clamp(hz/(1.5+t*.22),0.,1.));
  }
  return sh;
}
// ベッドの高さ（ふちが盛り上がった丸いクッション）
float bedH(vec2 q){
  float rr=length(q/uBedR.xy),R=(uBedR.x+uBedR.y)*.5,d=(rr-1.)*R,bw=uBedR.z;
  float x=1.-abs((d+bw*.5)/(bw*.5));
  float lump=1.+.09*(vn(q*.045)-.5)+.035*sin(atan(q.y,q.x)*9.);
  float hb=x>0.?uBedR.w*lump*sqrt(x*(2.-x)):0.;
  float ri=1.-bw/R*.86;
  float xc=clamp(rr/ri,0.,1.);
  float hc=rr<ri?7.+7.*sqrt(1.-xc*xc*xc*xc)+2.4*(vn(q*.03)-.5):0.;
  return max(hb,hc);
}
// 窓からの日だまり（窓わくの影つき）
float sunAt(vec2 p){
  vec2 q=p-uSun.xy;
  vec2 ax=vec2(.95,.31),ay=vec2(-.45,.89);
  float det=ax.x*ay.y-ax.y*ay.x;
  float u=(q.x*ay.y-q.y*ay.x)/det/uSun.z,v=(ax.x*q.y-ax.y*q.x)/det/uSun.w;
  float e=.09;
  float m=smoothstep(1.+e,1.-e,abs(u))*smoothstep(1.+e,1.-e,abs(v));
  float bar=smoothstep(.02,.07,abs(u))*smoothstep(.02,.065,abs(abs(v)-.34));
  m*=mix(.3,1.,bar);
  m*=.82+.18*smoothstep(.35,.6,vn(p*.022+vec2(uMisc.x*.35,uMisc.x*.2)));
  return m;
}
// 木の床
vec3 floorAlb(vec2 p,out float gap,out float glossy){
  vec2 q=rot(p,.07);
  float pw=58.;
  float row=floor(q.y/pw),fy=fract(q.y/pw);
  float off=hash(vec2(row,3.))*520.,pl=300.+hash(vec2(row,9.))*160.;
  float xi=(q.x+off)/pl;float ci=floor(xi),fx=fract(xi);
  float id=hash(vec2(row*7.+ci*13.,row*3.+ci));
  float gy=min(fy,1.-fy)*pw,gx=min(fx,1.-fx)*pl;
  gap=smoothstep(.15,1.3,gy)*smoothstep(.15,1.2,gx);
  float gr=fbm(vec2(q.x*.05+id*190.,q.y*.9+id*77.));
  float ring=sin(q.y*.55+fbm(vec2(q.x*.012+id*31.,q.y*.07))*26.+id*40.);
  vec3 a=vec3(.50,.32,.165),b=vec3(.33,.195,.092);
  vec3 c=mix(b,a,clamp(id*.7+.22+(gr-.47)*.9,0.,1.));
  c*=1.-.12*smoothstep(.5,1.,ring)*(.5+gr);
  c*=.93+.14*vn(q*vec2(.9,6.));
  glossy=.4+gr*.6;
  return c;
}

void main(){
  vec2 uv=gl_FragCoord.xy/uRes;
  vec2 p=(uv-.5)*vec2(uView.x,-uView.y);
  vec3 L=uL;
  vec3 V=normalize(vec3(0.,.16,1.));
  vec3 Hv=normalize(L+V);
  vec3 Lc=vec3(1.,.90,.74)*2.3,Sk=vec3(.60,.68,.82)*.62;
  float S=uDogS.x;
  vec2 pr=p-uDog.xy;
  vec2 pl=vec2(uDog.z*pr.x+uDog.w*pr.y,-uDog.w*pr.x+uDog.z*pr.y)/S;
  vec3 Ll=vec3(uDog.z*L.x+uDog.w*L.y,-uDog.w*L.x+uDog.z*L.y,L.z);
  vec3 Hl=vec3(uDog.z*Hv.x+uDog.w*Hv.y,-uDog.w*Hv.x+uDog.z*Hv.y,Hv.z);
  // ---- ベッドの形
  vec2 bp=p-uBed.xy;
  vec2 bq=vec2(uBed.z*bp.x+uBed.w*bp.y,-uBed.w*bp.x+uBed.z*bp.y);
  vec3 Lb=vec3(uBed.z*L.x+uBed.w*L.y,-uBed.w*L.x+uBed.z*L.y,L.z);
  float bh=bedH(bq);
  float brr=length(bq/uBedR.xy),bR=(uBedR.x+uBedR.y)*.5,bd=(brr-1.)*bR;

  // ---- 犬
  vec3 fur=vec3(0.);float cov=0.,dsh=1.,dao=1.,tongueM=0.;
  vec2 bb=pl-uBound.xy;
  if(dot(bb,bb)<uBound.z*uBound.z){
    dogF(pl);
    float h0=gH,s0=gS;
    vec2 hv=pl-uHead.xy;
    vec2 hq=vec2(dot(hv,uHead.zw),uHead.z*hv.y-uHead.w*hv.x)/uFace.x;
    float ahy=abs(hq.y);
    float roll=uFace2.x;
    if(s0>-uHair.w*2.2-4.){
      float E=1.3;
      vec2 a1=dogL(pl+vec2(E,0.)),a2=dogL(pl+vec2(0.,E));
      vec2 gh=(vec2(a1.x,a2.x)-h0)/E,gs=(vec2(a1.y,a2.y)-s0)/E;
      float ghl=length(gh);if(ghl>3.2)gh*=3.2/ghl;
      vec3 N=normalize(vec3(-gh,1.));
      vec2 dn=-gh;float sl=length(dn)+1e-4;
      vec2 d=normalize(gFlow+dn/sl*min(sl,1.5)*.5+vec2(1e-4,0.));
      // なでた向き
      vec4 ft=texture2D(uFlow,(pl-uFlowRect.xy)*uFlowRect.zw);
      vec2 sv=(ft.rg-.50196)*2.;float sm=length(sv);float stg=smoothstep(.02,.75,sm);vec2 sdn=sv/max(sm,1e-3);
      float agn=dot(d,sdn);
      float ruf=stg*smoothstep(.15,-.55,agn),sleek=stg*smoothstep(.2,.85,agn);
      d=normalize(mix(d,sdn,stg*.78)+vec2(-d.y,d.x)*ruf*.25+vec2(1e-4,0.));
      vec2 pn=pl-gDisp;
      float hm=gZ.y;
      d=rot(d,(vn(pn/24.)-.5)*uHair.z*hm);
      float tex=uHair.x,sp=uHair.y*hm/(13.*tex);
      tex*=max(1.,sp/1.35);sp=clamp(sp,.7,1.35);
      float f1=lic(pn,d,tex,sp,vec4(1.,0.,0.,0.));
      float f2=lic(pn+vec2(71.3,23.9),d,tex*2.2,sp,vec4(0.,1.,0.,0.));
      float f3=lic5(pn+vec2(13.7,57.1),d,tex*5.5,1.4,vec4(0.,0.,1.,0.));
      f1=clamp(.5+(f1-.5)*3.8,0.,1.);f2=clamp(.5+(f2-.5)*3.4,0.,1.);f3=clamp(.5+(f3-.5)*3.,0.,1.);
      float raw=texture2D(uNoise,pn/(tex*256.)*1.3).b;
      float strand=mix(f1*.55+f2*.45,clamp(.5+(raw-.5)*1.9,0.,1.),ruf*.6);
      // 輪かく（毛先がはみ出す）
      float gsl=length(gs)+1e-4;float outw=max(0.,dot(d,-gs/gsl));
      float fr=uHair.w*hm*(strand*1.5-.5)*(.3+.7*outw);
      float px=uDogS.y;
      float tgv=min(abs(gQ.x),min(abs(gQ.x-.46),abs(gQ.x+.46)));
      float toeZ=smoothstep(.2,.7,gQ.z+gQ.y*.8)*(1.-roll)*(gW3.x+gW3.y);
      float toe=smoothstep(.16,0.,tgv)*toeZ;
      cov=smoothstep(-px,px,s0+fr-toe*smoothstep(.3,1.,gQ.y)*5.);
      // ---- 毛色・もよう
      float wT=gW1.x,wSk=gW1.y,wMz=gW1.z,wEar=gW1.w,wFl=gW2.x,wHl=gW2.y,wTl=gW2.z,wNk=gW2.w,wFp=gW3.x,wHp=gW3.y;
      float al=abs(gQ.x),lon=gQ.y,tt=gQ.z,jit=(strand-.5)*.28,pat=uPat.x;
      float U=wT*smoothstep(.9,1.08,al+jit)+wSk*smoothstep(.5,.85,al+jit)*smoothstep(.4,-.3,lon)
        +wMz*max(smoothstep(.6,.95,al+jit),smoothstep(.2,.04,tt+jit))
        +(wFl+wHl)*smoothstep(.55,.9,tt+jit)+wTl*smoothstep(.1,.6,gQ.x*uPat.w+jit)+wNk*smoothstep(.72,1.,al+jit)+wFp+wHp;
      U=max(U,gZ.x);
      float belly=(wT+wNk)*smoothstep(.85,.5,al+jit)+(wMz+wSk)*smoothstep(.9,.55,al+jit)+(wFl+wHl)*.6;
      U=max(U,roll*belly);
      float isSolid=step(pat,.5),isTan=step(1.5,pat)*step(pat,2.5),isBi=step(2.5,pat)*step(pat,3.5),isPatch=step(3.5,pat);
      float blaze=wSk*smoothstep(.26,.1,al+jit*.6)+wMz+wNk*smoothstep(.95,.5,tt+jit);
      U=max(U,isBi*clamp(blaze,0.,1.));
      float brow=smoothstep(5.2,3.4,length(vec2(hq.x-15.,ahy-15.5)))*min(1.,wSk+wMz)*(1.-roll);
      U=max(U,isTan*brow);
      U=clamp(U,0.,1.)*(1.-isPatch)*mix(1.,.6,isSolid);
      vec3 base=mix(uBase,uUnder,U);
      float pm=smoothstep(.5,.56,vn(pn*.014+vec2(40.,90.))*.75+vn(pn*.035)*.35-.06+jit*.25);
      pm=max(pm,wEar);
      pm=max(pm,smoothstep(25.,19.,length(hq-vec2(6.,17.)))*min(1.,wSk+wMz*.4));
      base=mix(base,uPatch,isPatch*clamp(pm,0.,1.)*(1.-roll*clamp(belly,0.,1.)*.8));
      float flk=uPat.y*smoothstep(.5,.8,f2)*(1.-U)*min(1.,wT+wSk+wNk+wTl+wEar*.5);
      float depth=mix(.70,1.12,strand)*mix(.84,1.06,f3);
      depth*=mix(1.,.6+.5*f3,ruf);
      vec3 alb=base*depth;
      alb=mix(alb,alb*.22,flk*.8);
      alb=mix(alb,alb*1.12+.03,strand*strand*.35);
      // 耳の内側
      float einn=uFace2.y*wEar*smoothstep(0.,.45,gQ.x*sign(hq.y)*uFace2.z)*smoothstep(1.,.55,tt);
      alb=mix(alb,mix(vec3(.42,.27,.22),uUnder*.8,smoothstep(.25,.7,abs(gQ.x)))*(.8+.2*strand),einn*.8);
      // 指の分かれ目・肉球
      float wP=wFp+wHp;
      alb*=1.-.8*toe;
      alb*=1.+.18*toeZ*smoothstep(.08,.23,tgv);
      vec2 pd=vec2(lon-(1.-tt)*1.3,gQ.x);
      float pads=smoothstep(1.,.8,length((pd-vec2(-.2,0.))/vec2(.4,.5)));
      pads=max(pads,smoothstep(.2,.14,length(vec2(pd.x-.5,abs(pd.y)-.22))));
      pads=max(pads,smoothstep(.2,.14,length(vec2(pd.x-.32,abs(pd.y)-.62))));
      pads*=wP*roll;
      alb=mix(alb,vec3(.035,.025,.025),pads*.9);
      // あお向けの時の口の線
      float jaw=roll*wMz*smoothstep(.09,.03,abs(al-.55))*smoothstep(.15,.4,tt);
      alb*=1.-.6*jaw;
      // ---- 光
      vec3 d3=vec3(d,0.);vec3 T=normalize(d3-N*dot(d3,N));
      float lift=mix(.28,1.05,ruf)-sleek*.1;
      T=normalize(T*cos(lift)+N*sin(lift));
      float ndl=dot(N,Ll),wrap=clamp((ndl+.25)/1.25,0.,1.);wrap*=wrap*(3.-2.*wrap)*.4+.6;
      float form=mix(.55,1.,pow(clamp(N.z,0.,1.),1.4));form=mix(form,1.,smoothstep(-.1,.5,ndl)*.85);
      float tl=dot(T,Ll);float kd=sqrt(max(0.,1.-tl*tl));
      float diff=wrap*mix(.7,1.,kd);
      vec3 T1=normalize(T+N*(-.10+(strand-.5)*.30)),T2=normalize(T+N*(.22+(f2-.5)*.4));
      float th1=dot(T1,Hl),th2=dot(T2,Hl);
      float s1=pow(sqrt(max(0.,1.-th1*th1)),80.),s2=pow(sqrt(max(0.,1.-th2*th2)),18.);
      float darkK=smoothstep(.07,.01,dot(base,vec3(.3,.6,.1)));
      float smask=mix(smoothstep(.3,.75,strand),.35+.3*strand,darkK)*(1.-ruf*.85)*(1.+sleek*.7)*wrap;
      float eao=mix(.5,1.,smoothstep(-3.,16.,s0))*mix(.8,1.,smoothstep(0.,26.,h0));
      float sun=sunAt(p-L.xy/L.z*max(h0,0.)*S);
      float sh=cov>.01?shDog(pl,max(h0,0.)+2.,Ll):1.;
      vec3 dir=Lc*(.30+.70*sun)*sh;
      fur=alb*(Sk*eao*form+dir*diff*mix(.8,1.,form))+dir*smask*(s1*.10*vec3(1.,.97,.9)+s2*.22*(base*1.5+.06));
      // ---- 首輪・名札
      vec2 cvv=pl-uCol.xy;vec2 cq=vec2(dot(cvv,uCol.zw),uCol.z*cvv.y-uCol.w*cvv.x);
      float cw=uCol2.x;
      float onb=smoothstep(.4,.62,wT+wNk)*smoothstep(1.,4.,s0);
      float band=smoothstep(cw+.7,cw-.5,abs(cq.x)+(strand-.5)*uCol2.y)*onb;
      fur*=mix(1.,.62,onb*smoothstep(cw+4.,cw,abs(cq.x))*(1.-band));
      vec3 Nc=normalize(N+vec3(uCol.zw*(cq.x/cw)*.7,0.));
      float cweave=.86+.14*sin(cq.y*3.3)*sin(cq.x*2.6+1.)+.1*(vn(vec2(cq.y*2.,cq.x*.6))-.5);
      float cedge=smoothstep(cw,cw-1.6,abs(cq.x));
      vec3 calb=uCollarC*cweave*mix(.55,1.,cedge);
      float stitch=smoothstep(.5,.15,abs(abs(cq.x)-cw*.62))*step(.5,fract(cq.y*.45));
      calb=mix(calb,calb*1.6+.05,stitch*.5);
      vec3 ccol=calb*(Sk*eao+dir*clamp((dot(Nc,Ll)+.3)/1.3,0.,1.))+dir*pow(max(dot(Nc,Hl),0.),24.)*.05;
      fur=mix(fur,ccol,band);
      vec2 perpC=vec2(-uCol.w,uCol.z);
      vec2 tq=cq-vec2(-cw-5.5,uCol2.z);
      vec2 so=-normalize(Ll.xy)*2.6;
      float tsh=smoothstep(8.,4.5,length(tq-vec2(dot(so,uCol.zw),dot(so,perpC))))*onb;
      fur*=1.-.45*tsh*(1.-band);
      float tr=length(tq);
      float tagm=smoothstep(5.7,5.1,tr)*onb;
      vec3 Nt=normalize(N*.7+vec3((uCol.zw*tq.x+perpC*tq.y)*.035,.5));
      float tsp=pow(max(dot(Nt,Hl),0.),38.);
      vec3 tcol=vec3(.83,.58,.22)*(Sk*.9+dir*(.25+.5*max(dot(Nt,Ll),0.)))*(.85+.15*sin(tr*5.))+dir*tsp*vec3(1.,.9,.7)*1.4;
      tcol*=1.-.3*smoothstep(.8,.3,abs(tr-4.3));
      fur=mix(fur,tcol,tagm);
      float ringm=smoothstep(.9,.4,abs(length(cq-vec2(-cw-.3,uCol2.z))-2.4))*onb;
      fur=mix(fur,vec3(.6,.6,.62)*(Sk+dir*.8),ringm*.9);
      vec2 bk=abs(cq-vec2(0.,-uCol2.z*1.7))-vec2(cw+1.3,4.2);
      float bsd=max(bk.x,bk.y);
      float buckle=smoothstep(.5,-.3,bsd)*smoothstep(-2.8,-1.9,bsd)*onb;
      fur=mix(fur,vec3(.62,.62,.66)*(Sk+dir*(.5+1.2*pow(max(dot(N,Hl),0.),20.))),buckle);
      // ---- 目
      vec2 eq=vec2(hq.x-24.,ahy-18.5);
      vec2 er=vec2(dot(eq,vec2(-.5,.866)),dot(eq,vec2(-.866,-.5)));
      float eo=uFace.z;
      float eyeV=(1.-roll)*min(1.,wSk+wMz);
      float rim=smoothstep(1.9,1.,length(er/vec2(6.2,1.4+2.2*eo)))*eyeV;
      fur*=1.-.5*rim;
      float eye=smoothstep(1.,.7,length(er/vec2(5.2,.5+2.*eo)))*eyeV;
      vec3 ecol=vec3(.02,.012,.008)*(Sk+dir*.6)+dir*smoothstep(1.1,.5,length(er-vec2(-1.6,-.7)))*eo*.35;
      fur=mix(fur,ecol,eye);
      // ---- 鼻（ぬれたつや）
      vec2 ne=(hq-vec2(uFace.y-5.,0.))/vec2(8.2,9.4);
      float nl=length(ne);
      float nose=smoothstep(1.,.86,nl);
      vec2 perpH=vec2(-uHead.w,uHead.z);
      vec3 Nn=normalize(vec3(uHead.zw*ne.x+perpH*ne.y,sqrt(max(0.,1.-nl*nl))+.3));
      float nb=vn(hq*2.3);
      float nsp=pow(max(dot(Nn,Hl),0.),70.)*(.6+.8*nb)*2.2+pow(max(dot(Nn,Hl),0.),7.)*.12;
      float nost=smoothstep(.3,.16,length(vec2(ne.x-.38,abs(ne.y)-.42)));
      vec3 ncol=vec3(.016,.013,.013)*(1.-.7*nost)*(Sk+dir*clamp(dot(Nn,Ll)+.3,0.,1.))+dir*nsp*(1.-nost)*vec3(.9,.95,1.)*.35;
      fur=mix(fur,ncol,nose);
      cov=max(cov,nose);
    }
    // 舌
    float tgu=uFace.w;
    if(tgu>.03){
      float bx=uFace.y+2.+13.*tgu,ax=uFace.y-9.;
      float t2=clamp((hq.x-ax)/(bx-ax),0.,1.);
      float dd=length(hq-vec2(mix(ax,bx,t2),0.));
      tongueM=smoothstep(6.3,5.3,dd)*smoothstep(.03,.2,tgu);
    }
    float z0=max(0.,(bh-14.)/S);
    dsh=cov<.99?shDog(pl,z0,Ll):1.;
    dao=1.-.42*exp(min(s0,0.)/15.);
  }

  // ---- 床とベッド
  float E2=1.6;
  vec2 bgd=vec2(bedH(bq+vec2(E2,0.))-bh,bedH(bq+vec2(0.,E2))-bh)/E2;
  float bgl=length(bgd);if(bgl>2.5)bgd*=2.5/bgl;
  bgd+=vec2(cos(bq.x*2.4)*sin(bq.y*2.4),sin(bq.x*2.4)*cos(bq.y*2.4))*.05;
  vec3 Nb=normalize(vec3(-bgd,1.));
  float onBed=smoothstep(1.2,-1.2,bd);
  float isBol=smoothstep(-uBedR.z*.9,-uBedR.z*.78,bd);
  float thr=vn(vec2(bq.x*1.7,bq.y*.22))*.5+vn(vec2(bq.x*.22,bq.y*1.7))*.5;
  vec3 balb=mix(vec3(.20,.29,.32),vec3(.115,.185,.215),isBol)*(.82+.54*(thr-.5)+.07*sin(bq.x*2.4)*sin(bq.y*2.4))*(.88+.24*fbm(bq*.08));
  float seam=smoothstep(2.4,.6,abs(bd+uBedR.z*.84));
  balb*=1.-.4*seam;
  float bsh=1.;vec2 bdir=normalize(Lb.xy);float bsl=Lb.z/length(Lb.xy);
  for(int i=0;i<3;i++){float t=5.+float(i)*11.;float hz=bedH(bq+bdir*t)-(bh+1.+t*bsl);bsh=min(bsh,1.-clamp(hz/(1.5+t*.2),0.,1.));}
  float sunB=sunAt(p-L.xy/L.z*bh);
  vec3 dirB=Lc*(.30+.70*sunB)*bsh*dsh;
  float aoC=1.-.4*exp(-abs(bd+uBedR.z*.84)/7.);
  vec3 bedC=balb*(Sk*aoC*dao+dirB*max(dot(Nb,Lb),0.));
  float gap,glossy;
  vec3 falb=floorAlb(p,gap,glossy);
  falb*=mix(.28,1.,gap);
  float fao=1.-.5*exp(-max(bd,0.)/9.);
  float refl=pow(max(0.,1.-length(p-vec2(-uView.x*.3,-uView.y*.45))/(uView.x*.9)),2.)*.10*glossy*gap;
  vec3 flC=falb*(Sk*fao*dao+dirB*L.z)+dirB*refl;
  vec3 col=mix(flC,bedC,onBed);
  // 舌
  if(tongueM>0.){
    vec2 hv2=pl-uHead.xy;float hy2=(uHead.z*hv2.y-uHead.w*hv2.x)/uFace.x;
    vec3 talb=vec3(.60,.15,.17)*(1.-.3*smoothstep(1.4,.2,abs(hy2)));
    vec3 tc=talb*(Sk*.9+Lc*(.30+.70*sunB)*dsh*.7)+Lc*dsh*.05;
    col=mix(col,tc,tongueM);
  }
  col=mix(col,fur,cov);
  // ---- 手の影
  if(uHand.z>.01){
    vec2 hp=p-uHand.xy-vec2(7.,10.);
    vec2 hh=vec2(uHand2.x*hp.x+uHand2.y*hp.y,-uHand2.y*hp.x+uHand2.x*hp.y)/uHand2.z;
    float sd=length(hh-vec2(0.,22.))-27.;
    sd=min(sd,sdSeg(hh,vec2(-21.,2.),vec2(-27.,-44.),7.2));
    sd=min(sd,sdSeg(hh,vec2(-7.,-2.),vec2(-9.,-58.),7.6));
    sd=min(sd,sdSeg(hh,vec2(7.,-2.),vec2(9.,-55.),7.4));
    sd=min(sd,sdSeg(hh,vec2(20.,3.),vec2(26.,-40.),6.6));
    sd=min(sd,sdSeg(hh,vec2(-22.,26.),vec2(-45.,2.),8.4));
    col*=1.-.62*smoothstep(10.,-7.,sd)*uHand.z;
  }
  // ---- 仕上げ
  vec2 vc=uv-.5;
  col*=1.-.42*pow(dot(vc,vc)*2.,1.3);
  col=1.-exp(-col*1.25);
  col=pow(col,vec3(1./2.2));
  col=mix(col,col*col*(3.-2.*col),.3);
  col+=(texture2D(uNoise,gl_FragCoord.xy/256.+uMisc.yz).r-.5)*.03;
  gl_FragColor=vec4(col,1.);
}`;

  // =====================================================================
  //  WebGL の準備
  // =====================================================================
  let gl = null, prog = null, glErr = '';
  const U = {};
  function noGL(msg) { glErr = msg || 'no webgl'; const n = $('inuNoGl'); if (n) n.hidden = false; cv.style.visibility = 'hidden'; $('inuMood').style.display = 'none'; }
  function initGL() {
    const opt = { antialias: false, alpha: false, depth: false, stencil: false, preserveDrawingBuffer: true, powerPreference: 'high-performance' };
    try { gl = cv.getContext('webgl', opt) || cv.getContext('experimental-webgl', opt); } catch (e) { gl = null; }
    if (!gl) { noGL('webgl なし'); return false; }
    const hp = gl.getShaderPrecisionFormat(gl.FRAGMENT_SHADER, gl.HIGH_FLOAT);
    if (!hp || hp.precision < 20 || gl.getParameter(gl.MAX_FRAGMENT_UNIFORM_VECTORS) < 128) { noGL('性能が足りない'); return false; }
    const mk = (type, src) => { const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) { const log = gl.getShaderInfoLog(s); console.error('[inu] shader compile error\n' + log); glErr = log || 'compile'; return null; } return s; };
    const vs = mk(gl.VERTEX_SHADER, VS), fs = mk(gl.FRAGMENT_SHADER, FS);
    if (!vs || !fs) { noGL(glErr); return false; }
    prog = gl.createProgram(); gl.attachShader(prog, vs); gl.attachShader(prog, fs); gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) { const log = gl.getProgramInfoLog(prog); console.error('[inu] program link error\n' + log); noGL(log || 'link'); return false; }
    gl.useProgram(prog);
    const buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    const loc = gl.getAttribLocation(prog, 'a'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    for (const n of ['uRes', 'uView', 'uDog', 'uDogS', 'uHead', 'uFace', 'uFace2', 'uCol', 'uCol2', 'uBed', 'uBedR', 'uHand', 'uHand2', 'uHandL', 'uFlowRect', 'uPat', 'uHair', 'uSun', 'uMisc', 'uBound', 'uBase', 'uUnder', 'uPatch', 'uCollarC', 'uL', 'uNoise', 'uFlow']) U[n] = gl.getUniformLocation(prog, n);
    for (const n of ['uA', 'uB', 'uC', 'uD']) U[n] = gl.getUniformLocation(prog, n + '[0]');
    // ノイズ（毛のすじ・木目・布目に使う。コードで作る）
    const R = rng(4242), nz = new Uint8Array(256 * 256 * 4); for (let i = 0; i < nz.length; i++) nz[i] = Math.floor(R() * 256);
    const t0 = gl.createTexture(); gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, t0);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 256, 256, 0, gl.RGBA, gl.UNSIGNED_BYTE, nz);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.REPEAT); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.REPEAT);
    // なでた向き
    const t1 = gl.createTexture(); gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, t1);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, FW, FH, 0, gl.RGBA, gl.UNSIGNED_BYTE, flowBuf);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    gl.uniform1i(U.uNoise, 0); gl.uniform1i(U.uFlow, 1);
    cv.addEventListener('webglcontextlost', e => { e.preventDefault(); noGL('context lost'); });
    return true;
  }

  // =====================================================================
  //  状態
  // =====================================================================
  const cfg = { type: 'tachi', coat: 'akacha', size: .88, fat: 1 };
  const st = { t: 0, happy: 15, count: 0, sec: 0, idle: 0, bellyT: 0, sleepyT: 0, breathPh: 0, wagPh: 0, wagHz: 1, kickPh: 0, kickHold: 0, kickSide: 1, nextBlink: 2, blinkT: 0, evt: null, evtN: 0, nextEvt: 0,
    nextTw: 3, nextSigh: 9, sighT: 0, wagBoost: 0, lastReg: null, reg: null, hover: null, petOn: false, fps: 0, ms: 0, level: 0, mood: '', dirty: false, saveT: 0 };
  const hand = { x: 0, y: 0, px: 0, py: 0, vx: 0, vy: 0, over: false, was: false, down: false, mouse: true, a: 0, rot: 0, sx: 0, sy: 0 };
  const stroke = { on: false, len: 0, dx: 0, dy: 0 };
  // バネ（x=今の値, t=めざす値, k=強さ, c=ねばり）
  const SP = {};
  const spr = (n, k, c, x) => { SP[n] = { x: x || 0, v: 0, t: x || 0, k, c }; };
  spr('eye', 200, 24); spr('ear', 130, 14); spr('earTw', 260, 14); spr('headX', 120, 15); spr('headY', 120, 15); spr('headRot', 80, 12); spr('look', 60, 11);
  spr('tongue', 70, 12); spr('roll', 34, 10); spr('kick', 200, 20); spr('paw', 150, 17); spr('tap', 160, 15); spr('wagAmp', 60, 12, .3); spr('tuck', 90, 13);
  spr('sleepy', 14, 7.5); spr('handP', 160, 20);
  function stepSprings(dt) { for (const n in SP) { const s = SP[n]; s.v += (s.k * (s.t - s.x) - s.c * s.v) * dt; s.x += s.v * dt; } }
  const coat = () => COATS.find(c => c.id === cfg.coat) || COATS[0];
  let W = 600, H = 400, dpr = 1, portrait = false, VW = 780, VH = 520;

  // ---------- 座標（画面 → 部屋 → 犬） ----------
  function xform() {
    const S = cfg.size, th = portrait ? -Math.PI / 2 + .13 : Math.PI - .1;
    const c = Math.cos(th), s = Math.sin(th), bx = 0, by = portrait ? 4 : 6, lx = 20 * S;
    return { S, th, c, s, bx, by, ox: bx - c * lx, oy: by - s * lx };
  }
  const toScene = (x, y) => [(x / W - .5) * VW, (y / H - .5) * VH];
  const toLocal = (X, sx, sy) => { const x = sx - X.ox, y = sy - X.oy; return [(X.c * x + X.s * y) / X.S, (-X.s * x + X.c * y) / X.S]; };
  const fromLocal = (X, lx, ly) => { const sx = X.ox + (X.c * lx - X.s * ly) * X.S, sy = X.oy + (X.s * lx + X.c * ly) * X.S; return [(sx / VW + .5) * W, (sy / VH + .5) * H]; };

  // =====================================================================
  //  姿勢（体の部品の位置をまとめて計算）  r=0: ふせ / r=1: あお向け
  // =====================================================================
  function poseQ(rest) {
    if (rest) return { r: 0, br: 0, kick: 0, kickPh: 0, kickSide: 1, paw: 0, tap: 0, tapPh: 0, look: 0, hrot: 0, hx: 0, hy: 0, ear: 0, earTw: 0, tuck: 0, wag: 0, wagPh: 0, sway: 0 };
    const r0 = clamp(SP.roll.x, 0, 1);
    const sg = st.sighT > 0 ? Math.sin(Math.PI * (1 - st.sighT / 1.8)) * 1.5 : 0;
    return { r: r0 * r0 * (3 - 2 * r0), br: Math.sin(st.breathPh * TAU) + sg, kick: SP.kick.x, kickPh: st.kickPh, kickSide: st.kickSide, paw: clamp(SP.paw.x, 0, 1.1), tap: clamp(SP.tap.x, 0, 1.2), tapPh: st.t * 12,
      look: SP.look.x, hrot: SP.headRot.x, hx: SP.headX.x, hy: SP.headY.x, ear: SP.ear.x, earTw: SP.earTw.x, tuck: SP.tuck.x, wag: SP.wagAmp.x + st.wagBoost, wagPh: st.wagPh, sway: Math.sin(st.t * 1.4) * .06 * r0 };
  }
  function pose(q) {
    const T = TYPES[cfg.type], F = cfg.fat, Lb = T.len, lg = T.leg, fl = T.fluff, r = q.r, Fw = .4 + .6 * F, lgk = .45 + .55 * lg;
    const P = [];
    const add = (part, ax, ay, bx, by, ra, rb, ha, hb, fx, fy, k, z, hm) => { const n = Math.hypot(fx, fy) || 1; P.push({ part, ax, ay, bx, by, ra, rb, ha, hb, fx: fx / n, fy: fy / n, k, z: z || 0, hm: hm == null ? 1 : hm }); };
    const side = r * 12, br = q.br;
    // 胴
    const xc = 70 * Lb, xh = -85 * Lb;
    const rc = (58 * Fw + fl) * (1 + .024 * br) * lerp(1, 1.05, r), rh = (54 * Fw + fl) * (1 + .014 * br) * lerp(1, 1.07, r);
    const hipY = -9 * (1 - r);   // 腰を少しひねる
    add(0, xc, side, xh, side + hipY, rc, rh, 50 * (1 + .03 * br), 46 * (1 + .02 * br), -1, 0, 14, 0, 1);
    // 肩
    for (const sg of [-1, 1]) { const x = lerp(60, 62, r) * Lb, y = side + sg * lerp(30, 24, r) * Fw, h = lerp(48, 40, r); add(0, x, y, x, y, 34 + fl, 34 + fl, h, h, -1, sg * .4, 16, 0, 1); }
    // もも
    for (const sg of [-1, 1]) { const x = lerp(sg > 0 ? -74 : -66, -70, r) * Lb, y = side + hipY + sg * lerp(sg > 0 ? 50 : 30, 48, r) * Fw, rr = lerp(sg > 0 ? 40 : 30, 33, r) + fl, h = lerp(sg > 0 ? 44 : 40, 44, r); add(5, x, y, x, y, rr, rr, h, h, -.8, sg * .6, 12, 0, 1); }
    // 後ろ足
    const kph = Math.sin(q.kickPh), kk = q.kick;
    for (const sg of [-1, 1]) {
      // ふせ: 後ろ足は2本とも同じ側（+y）へ出す
      let ax = (sg > 0 ? -92 : -46) * Lb, ay = side + hipY + (sg > 0 ? 64 : 52) * Fw + fl, bx = ax + (sg > 0 ? 54 : 46) * lgk, by = side + hipY + (sg > 0 ? 92 : 80) * Fw + fl;
      if (sg === q.kickSide) { bx += kk * kph * 10 * (1 - r); by += kk * Math.abs(kph) * 5 * (1 - r); }
      const an = .8 + kk * Math.sin(q.kickPh + sg) * .45 * r + q.sway * sg, ln = 62 * lgk;
      const ax1 = -90 * Lb, ay1 = side + sg * 52 * Fw, bx1 = ax1 - Math.cos(an) * ln, by1 = ay1 + sg * Math.sin(an) * ln;
      ax = lerp(ax, ax1, r); ay = lerp(ay, ay1, r); bx = lerp(bx, bx1, r); by = lerp(by, by1, r);
      const dl = Math.hypot(bx - ax, by - ay) || 1, dx = (bx - ax) / dl, dy = (by - ay) / dl;
      add(5, ax, ay, bx, by, 14 + fl * .4, 12 + fl * .3, lerp(16, 34, r), lerp(13, 26, r), dx, dy, 6, 0, .7);
      add(9, bx, by, bx + dx * 13, by + dy * 13, 13.5 + fl * .3, 13 + fl * .3, lerp(13, 26, r), lerp(13, 24, r), dx, dy, 5, 1, .55);
    }
    // 前足
    for (const sg of [-1, 1]) {
      const tap = sg === 1 ? q.tap : 0, lift = tap * (.5 + .5 * Math.sin(q.tapPh));
      let ax = 64 * Lb, ay = side + sg * 46 * Fw, bx = ax + (sg > 0 ? 142 : 152) * lg * (1 - .2 * q.paw) - tap * 8, by = side + sg * ((sg > 0 ? 44 : 39) + q.paw * 17);
      const an = .95 + q.sway * sg, ln = 70 * lgk;
      const ax1 = 60 * Lb, ay1 = side + sg * 34 * Fw, bx1 = ax1 + Math.cos(an) * ln, by1 = ay1 + sg * Math.sin(an) * ln;
      ax = lerp(ax, ax1, r); ay = lerp(ay, ay1, r); bx = lerp(bx, bx1, r); by = lerp(by, by1, r);
      const dl = Math.hypot(bx - ax, by - ay) || 1, dx = (bx - ax) / dl, dy = (by - ay) / dl;
      add(4, ax, ay, bx, by, 21 + fl * .5, 15 + fl * .3 + lift * 1.5, lerp(26, 40, r), lerp(17, 30, r) + lift * 9, dx, dy, 7, 0, .75);
      const ph = lerp(17, 30, r) + lift * 9;
      add(8, bx, by, bx + dx * 14, by + dy * 14, 16.5 + fl * .3 + lift * 1.5, 15.5 + fl * .3 + lift * 1.5, ph, ph, dx, dy, 5, 1, .5);
    }
    // 頭
    const hs = T.head * 1.13 * (1 + q.look * .05), sn = T.snout;
    const xf = xc + rc * .55, pvx = xf - 10, pvy = side, hrot = q.hrot + r * .5 + (1 - r) * .2;
    const h0x = xf + 66 * hs - r * 8 + q.hx, h0y = side + q.hy, ch = Math.cos(hrot), sh = Math.sin(hrot);
    const hcx = pvx + (h0x - pvx) * ch - (h0y - pvy) * sh, hcy = pvy + (h0x - pvx) * sh + (h0y - pvy) * ch;
    const HP = (x, y) => [hcx + (x * ch - y * sh) * hs, hcy + (x * sh + y * ch) * hs];
    // 首
    const na = HP(-24, 0), nbx = xf - 14, nby = side;
    add(7, na[0], na[1], nbx, nby, (31 + fl) * (.8 + .2 * Fw), (43 + fl * .6) * Fw, 42, 49, nbx - na[0], nby - na[1], 11, 0, 1.15);
    // しっぽ
    const TT = TAILS[T.tail];
    { let x = xh - rh * TT.root, y = side + hipY; const a0 = lerp(TT.a0, TT.a1, r) + q.tuck * TT.tuck;
      for (let i = 0; i < TT.n; i++) {
        const k0 = i / TT.n, k1 = (i + 1) / TT.n;
        const ang = a0 + TT.curl * (1 - r * TT.uncurl) * (i + .5) + q.wag * TT.amp * Math.sin(q.wagPh - i * TT.lag) * (TT.stiff + (1 - TT.stiff) * k1);
        const nx = x + Math.cos(ang) * TT.seg, ny = y + Math.sin(ang) * TT.seg;
        add(6, x, y, nx, ny, TT.rad(k0) + fl * .5, TT.rad(k1) + fl * .5, lerp(TT.h(k0), 12, r), lerp(TT.h(k1), 10, r), nx - x, ny - y, 5, 0, TT.hm);
        x = nx; y = ny;
      } }
    // 頭の骨・マズル・耳
    const ck = T.cheek, s1 = HP(-2, -ck), s2 = HP(-2, ck), skH = lerp(55, 42, r);
    add(1, s1[0], s1[1], s2[0], s2[1], (39 + fl) * hs, (39 + fl) * hs, skH, skH, -ch, -sh, 6, 0, .8);
    const tip = 86 * sn, m1 = HP(tip - 14.5, 0), m2 = HP(20, 0);
    add(2, m1[0], m1[1], m2[0], m2[1], 14.5 * hs, (21.5 + fl * .4) * hs, lerp(30, 30, r), lerp(41, 34, r), -ch, -sh, 7, 0, .45);
    const E = EARS[T.ear], eb = clamp(q.ear, -.3, 1.2);
    for (const sg of [-1, 1]) {
      let tx = lerp(E.t[0], E.tb[0], eb), ty = lerp(E.t[1], E.tb[1], eb);
      if (sg === 1) { tx += q.earTw * 5; ty += q.earTw * 3; }
      tx = lerp(tx, E.tr[0], r); ty = lerp(ty, E.tr[1], r);
      const a = HP(E.b[0], sg * E.b[1]), b = HP(tx, sg * ty);
      add(3, a[0], a[1], b[0], b[1], E.rb * hs, E.rt * hs, lerp(E.hb, 30, r), lerp(lerp(E.ht, E.htb, clamp(eb, 0, 1)), 14, r), b[0] - a[0], b[1] - a[1], 3.5, 0, E.hm);
    }
    const cl = Math.hypot(na[0] - nbx, na[1] - nby) || 1;
    return { P, r, head: { x: hcx, y: hcy, fx: ch, fy: sh, hs, tip }, collar: { x: lerp(na[0], nbx, .52), y: lerp(na[1], nby, .52), ax: (na[0] - nbx) / cl, ay: (na[1] - nby) / cl },
      torso: { xc, xh, rc, rh, side }, T };
  }
  let G = null, restA = [];
  function makeRest() { restA = pose(poseQ(true)).P.map(p => [p.ax, p.ay]); }

  // ---------- どこをさわっているか ----------
  function hitLocal(x, y) {
    const g = G; let best = null, bh = 0;
    for (const p of g.P) {
      const abx = p.bx - p.ax, aby = p.by - p.ay, d2 = abx * abx + aby * aby;
      const t = d2 > 1e-3 ? clamp(((x - p.ax) * abx + (y - p.ay) * aby) / d2, 0, 1) : 0;
      const d = Math.hypot(x - p.ax - abx * t, y - p.ay - aby * t), rr = lerp(p.ra, p.rb, t) + 3, xx = 1 - d / rr;
      if (xx <= 0) continue;
      const v = lerp(p.ha, p.hb, t) * Math.sqrt(xx * (2 - xx));
      if (v > bh) { bh = v; best = p; }
    }
    if (!best) return null;
    const pt = best.part;
    if (pt === 1 || pt === 3) { const h = g.head, lat = Math.abs(-(x - h.x) * h.fy + (y - h.y) * h.fx) / h.hs; return pt === 1 && lat > 30 ? 'chin' : 'head'; }
    if (pt === 2) return 'head';
    if (pt === 7) return 'chin';
    if (pt === 4 || pt === 8) return 'paw';
    if (pt === 6) return 'tail';
    if (pt === 5 || pt === 9) return 'belly';
    if (g.r > .5) return 'belly';
    return Math.abs(y - g.torso.side) / g.torso.rc < .5 ? 'back' : 'belly';
  }
  function anchorLocal(region) {
    const g = G, h = g.head, t = g.torso;
    if (region === 'head') return [h.x - h.fx * 4, h.y - h.fy * 4];
    if (region === 'chin') return [g.collar.x - 4, g.collar.y + 10];
    if (region === 'back') return [-8, t.side + (g.r > .5 ? 0 : 4)];
    if (region === 'belly') return g.r > .5 ? [-8, t.side] : [-8, t.side + t.rc * .76];
    if (region === 'paw') { const p = g.P.find(v => v.part === 8); return [p.ax + p.fx * 4, p.ay + p.fy * 4]; }
    const tl = g.P.filter(v => v.part === 6), n = tl[Math.floor(tl.length * .55)]; return [n.bx, n.by];
  }

  // =====================================================================
  //  なでた向き（体に固定した小さなテクスチャに覚える）
  // =====================================================================
  const flowX = new Float32Array(FW * FH), flowY = new Float32Array(FW * FH), flowBuf = new Uint8Array(FW * FH * 4);
  for (let i = 0; i < FW * FH; i++) { flowBuf[i * 4] = 128; flowBuf[i * 4 + 1] = 128; flowBuf[i * 4 + 3] = 255; }
  let flowE = 0, flowDirty = false;
  function paint(lx, ly, ux, uy, speed, dt) {
    const R = 40, gain = clamp(speed / 260, .25, 1.3) * dt * 17;
    const i0 = Math.max(0, Math.floor((lx - R - FR.x0) / FR.w * FW)), i1 = Math.min(FW - 1, Math.ceil((lx + R - FR.x0) / FR.w * FW));
    const j0 = Math.max(0, Math.floor((ly - R - FR.y0) / FR.h * FH)), j1 = Math.min(FH - 1, Math.ceil((ly + R - FR.y0) / FR.h * FH));
    for (let j = j0; j <= j1; j++) for (let i = i0; i <= i1; i++) {
      const dx = (i + .5) / FW * FR.w + FR.x0 - lx, dy = (j + .5) / FH * FR.h + FR.y0 - ly, d2 = dx * dx + dy * dy; if (d2 > R * R) continue;
      const k = Math.min(1, gain * (1 - d2 / (R * R))), n = j * FW + i;
      flowX[n] += (ux - flowX[n]) * k; flowY[n] += (uy - flowY[n]) * k;
    }
    flowDirty = true;
  }
  function relaxFlow(dt, tau) {
    if (flowE < 1e-4 && !flowDirty) return;
    const f = Math.exp(-dt / tau); let e = 0;
    for (let n = 0; n < FW * FH; n++) { const x = flowX[n] *= f, y = flowY[n] *= f; e += x * x + y * y; }
    flowE = e; flowDirty = true;
  }
  function uploadFlow() {
    if (!flowDirty) return; flowDirty = false;
    for (let n = 0; n < FW * FH; n++) { flowBuf[n * 4] = clamp(Math.round(128 + flowX[n] * 127), 0, 255); flowBuf[n * 4 + 1] = clamp(Math.round(128 + flowY[n] * 127), 0, 255); }
    gl.activeTexture(gl.TEXTURE1); gl.texSubImage2D(gl.TEXTURE_2D, 0, 0, 0, FW, FH, gl.RGBA, gl.UNSIGNED_BYTE, flowBuf);
  }

  // =====================================================================
  //  動き（1コマ分）
  // =====================================================================
  function handVel(dt) {
    if (hand.over) {
      const s = toScene(hand.x, hand.y);
      if (!hand.was) { hand.px = s[0]; hand.py = s[1]; hand.vx = hand.vy = 0; }
      const k = Math.min(1, dt * 20);
      hand.vx += ((s[0] - hand.px) / dt - hand.vx) * k; hand.vy += ((s[1] - hand.py) / dt - hand.vy) * k;
      hand.px = s[0]; hand.py = s[1]; hand.sx = s[0]; hand.sy = s[1];
    } else hand.vx = hand.vy = 0;
    hand.was = hand.over;
  }
  function update(dt) {
    st.t += dt;
    const X = xform(), g = G = pose(poseQ()), rolled = SP.roll.t > .5;
    const sv = Math.hypot(hand.vx, hand.vy), speed = sv / X.S;
    const ux = sv > 1 ? hand.vx / sv : 0, uy = sv > 1 ? hand.vy / sv : 0;
    const ulx = X.c * ux + X.s * uy, uly = -X.s * ux + X.c * uy;
    const hl = toLocal(X, hand.sx, hand.sy);
    const hov = hand.over ? hitLocal(hl[0], hl[1]) : null;
    const petting = !!hov && (speed > 22 || hand.down);
    const reg = petting ? hov : null;
    st.hover = hov; st.reg = reg; st.petOn = petting;
    // --- 毛 ---
    relaxFlow(dt, Math.abs(SP.roll.v) > .25 ? .25 : 9);
    if (petting && speed > 22) paint(hl[0], hl[1], ulx, uly, speed, dt);
    // --- なでた回数・時間 ---
    if (petting) {
      if (!stroke.on) { stroke.on = true; stroke.len = 0; stroke.dx = ux; stroke.dy = uy; }
      stroke.len += speed * dt;
      const dot = ux * stroke.dx + uy * stroke.dy;
      if ((stroke.len > 26 && dot < -.25 && speed > 30) || stroke.len > 260) { st.count++; st.dirty = true; stroke.len = 0; stroke.dx = ux; stroke.dy = uy; }
      else if (speed > 30) { stroke.dx = lerp(stroke.dx, ux, Math.min(1, dt * 6)); stroke.dy = lerp(stroke.dy, uy, Math.min(1, dt * 6)); }
      if (speed > 22) { st.sec += dt; st.dirty = true; }
      st.idle = 0; st.evt = null;
    } else {
      if (stroke.on) { if (stroke.len > 26) { st.count++; st.dirty = true; } stroke.on = false; }
      st.idle += dt;
    }
    // --- 場所ごとの反応（めざす値を決める） ---
    const hp = st.happy / 100;
    let tEye = 0, tEar = 0, tHX = 0, tHY = 0, tHR = 0, tLook = 0, tPaw = 0, tTap = 0, tTuck = 0, tTongue = 0, gain = 0;
    let wagHz = .8 + hp * 3.2, wagA = .3 + hp * .7;
    if (reg === 'head') {
      tEye = 1; tEar = 1; gain = 6.5;
      const dx = hl[0] - g.head.x, dy = hl[1] - g.head.y, d = Math.hypot(dx, dy) || 1; tHX = dx / d * 6; tHY = dy / d * 7;
    } else if (reg === 'chin') {
      tEye = .8; tEar = .4; gain = 8; tHR = (hl[1] - g.head.y > 0 ? 1 : -1) * .2 * (rolled ? .4 : 1);
    } else if (reg === 'back') {
      wagHz *= 1.8; wagA = wagA * 1.4 + .25; tEye = .35; tEar = .25; gain = 6;
    } else if (reg === 'belly') {
      gain = rolled ? 8.5 : 6.5; tEye = rolled ? .9 : .4; tEar = .5; wagHz *= 1.2;
      if (!rolled) st.bellyT += dt;
      if (speed > 430) { st.kickHold = .28; st.kickSide = hl[1] > g.torso.side ? 1 : -1; }
    } else if (reg === 'paw') {
      tPaw = 1; gain = 1.5; tHR = (hl[1] > g.torso.side ? 1 : -1) * .07;
    } else if (reg === 'tail') {
      tTuck = 1; gain = 1; wagA *= .4;
      if (st.lastReg !== 'tail') st.wagBoost = 1.6;
    }
    st.lastReg = reg;
    st.wagBoost *= Math.exp(-dt / .45);
    if (!reg) st.bellyT = Math.max(0, st.bellyT - dt * .4);
    if (!rolled && st.bellyT > 2.2) { SP.roll.t = 1; st.bellyT = 0; }
    if (rolled && st.idle > 8) SP.roll.t = 0;
    st.kickHold = Math.max(0, st.kickHold - dt); const fast = st.kickHold > 0;
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
      const type = ['look', 'tap', 'look', 'yawn'][st.evtN++ % 4];
      st.evt = { type, t0: st.t, dur: type === 'yawn' ? 2.4 : type === 'tap' ? 1.5 : 2.6, side: R01() < .5 ? -1 : 1 };
    }
    if (st.evt) {
      const p = (st.t - st.evt.t0) / st.evt.dur;
      if (p >= 1) { st.evt = null; st.nextEvt = st.t + 3 + R01() * 3; }
      else {
        const env = p < .2 ? p / .2 : p > .8 ? (1 - p) / .2 : 1;
        if (st.evt.type === 'look') { tHR = st.evt.side * .2 * env; tLook = env; }
        else if (st.evt.type === 'tap') { tTap = env > .3 ? 1 : 0; tLook = .4 * env; }
        else { const y = Math.sin(Math.PI * p); tTongue = y; tEye = y > .3 ? 1 : 0; tLook = y; tEar = .5 * y; }
      }
    }
    if (!petting && st.idle > 4 && !st.evt && sl < .4 && !rolled) tLook = Math.max(tLook, .35);
    // まばたき・耳のぴくっ・ため息
    if (st.t > st.nextBlink) { st.blinkT = .13; st.nextBlink = st.t + 2.2 + R01() * 3.5; }
    if (st.blinkT > 0) { st.blinkT -= dt; tEye = 1; }
    if (st.t > st.nextTw) { SP.earTw.v += (R01() < .5 ? -1 : 1) * 9; st.nextTw = st.t + 3.5 + R01() * 5; }
    if (st.t > st.nextSigh && !petting) { st.sighT = 1.8; st.nextSigh = st.t + 11 + R01() * 8; }
    st.sighT = Math.max(0, st.sighT - dt);
    // 眠い
    tEye = Math.max(tEye, sl * 1.05); if (st.happy > 92) tEye = Math.max(tEye, .9);
    wagHz *= 1 - .6 * sl; wagA *= 1 - .45 * sl; tEar = Math.max(tEar, sl * .5);
    // 舌
    tTongue = Math.max(tTongue, (st.happy > 55 ? clamp((st.happy - 55) / 25, 0, 1) * .7 : 0) * (1 - sl * .8));
    // めざす値をバネへ
    SP.eye.t = tEye; SP.ear.t = tEar; SP.headX.t = tHX; SP.headY.t = tHY; SP.headRot.t = tHR; SP.look.t = tLook; SP.paw.t = tPaw; SP.tap.t = tTap; SP.tuck.t = tTuck; SP.tongue.t = tTongue;
    SP.wagAmp.t = wagA; SP.handP.t = petting ? 1 : 0;
    st.wagHz += (wagHz - st.wagHz) * Math.min(1, dt * 4); st.wagPh += dt * st.wagHz * TAU;
    st.breathPh += dt * (sl > .5 ? .2 : st.happy > 60 ? .5 : .3);
    stepSprings(dt);
    hand.a += ((hand.over ? 1 : 0) - hand.a) * Math.min(1, dt * 12);
    hand.rot += (clamp(hand.vx / 900, -.4, .4) - hand.rot) * Math.min(1, dt * 8);
    st.mood = moodText(reg, rolled, sl, fast);
  }
  function moodText(reg, rolled, sl, fast) {
    if (sl > .65) return 'とろん… ねむくなってきました';
    if (rolled && fast) return '足が勝手に、カカカッ！';
    if (reg === 'head') return '目を細めて、手に頭を寄せています';
    if (reg === 'chin') return '頭をかたむけて、うっとりしています';
    if (reg === 'back') return 'しっぽをぶんぶん振っています';
    if (reg === 'belly') return rolled ? 'へそ天！ すっかり安心しています' : (fast ? '後ろ足がピクピク…' : 'わき腹、きもちいい… ゴロンしそう');
    if (reg === 'paw') return '前足は、ちょっとだけ引っこめます';
    if (reg === 'tail') return 'しっぽを、体のほうへくるん';
    if (rolled) return 'おなかを見せて、待っています';
    if (st.evt) return st.evt.type === 'look' ? '頭をこちらに向けました' : st.evt.type === 'tap' ? '前足で、トントン' : 'ふわぁ… あくび';
    if (st.idle > 4) return 'こちらを気にしています';
    return st.happy > 60 ? 'しっぽを大きく振っています' : 'ゆっくり、しっぽを振っています';
  }

  // =====================================================================
  //  絵（シェーダへ値をわたして1枚かく）
  // =====================================================================
  const lin = h => [1, 3, 5].map(i => Math.pow(parseInt(h.slice(i, i + 2), 16) / 255, 2.2));
  const mixc = (a, b, t) => a.map((v, i) => v + (b[i] - v) * t);
  const arrA = new Float32Array(NP * 4), arrB = new Float32Array(NP * 4), arrC = new Float32Array(NP * 4), arrD = new Float32Array(NP * 4);
  let needSize = true;
  function size() {
    const w = cv.clientWidth || 600, h = cv.clientHeight || Math.round(w * 2 / 3);
    dpr = Math.min(w < 520 ? 1.5 : 2, window.devicePixelRatio || 1);
    const sc = RES[st.level], pw = Math.max(2, Math.round(w * dpr * sc)), ph = Math.max(2, Math.round(h * dpr * sc));
    if (cv.width !== pw || cv.height !== ph || needSize) { cv.width = pw; cv.height = ph; W = w; H = h; portrait = H > W; needSize = false; }
    { const T0 = TYPES[cfg.type], vk = (1 + (T0.len - 1) * .75 + Math.max(0, T0.snout - 1) * .22) * (.45 + .55 * cfg.size / .88);   // 胴長・大きい犬でも顔が切れないように引く
      if (portrait) { VW = 372 * vk; VH = VW * H / W; } else { VH = 332 * vk; VW = VH * W / H; } }
  }
  function render() {
    if (!gl || glErr) return;
    size();
    const X = xform(), g = G = pose(poseQ()), T = g.T, k = coat();
    for (let i = 0; i < NP; i++) {
      const p = g.P[i], o = i * 4;
      if (!p) { arrA[o] = arrA[o + 2] = 9000; arrA[o + 1] = arrA[o + 3] = 9000; arrB[o] = arrB[o + 1] = 1; arrB[o + 2] = arrB[o + 3] = 1; arrC[o] = -1; arrC[o + 1] = 0; arrC[o + 2] = 20; arrC[o + 3] = 5; arrD[o] = arrD[o + 1] = arrD[o + 2] = 0; arrD[o + 3] = 1; continue; }
      arrA[o] = p.ax; arrA[o + 1] = p.ay; arrA[o + 2] = p.bx; arrA[o + 3] = p.by;
      arrB[o] = p.ra; arrB[o + 1] = p.rb; arrB[o + 2] = p.ha; arrB[o + 3] = p.hb;
      arrC[o] = p.fx; arrC[o + 1] = p.fy; arrC[o + 2] = p.part; arrC[o + 3] = p.k;
      const ra = restA[i] || [p.ax, p.ay];
      arrD[o] = p.ax - ra[0]; arrD[o + 1] = p.ay - ra[1]; arrD[o + 2] = p.z; arrD[o + 3] = p.hm;
    }
    gl.viewport(0, 0, cv.width, cv.height);
    gl.uniform2f(U.uRes, cv.width, cv.height); gl.uniform2f(U.uView, VW, VH);
    gl.uniform4fv(U.uA, arrA); gl.uniform4fv(U.uB, arrB); gl.uniform4fv(U.uC, arrC); gl.uniform4fv(U.uD, arrD);
    const upp = VW / cv.width / X.S;
    gl.uniform4f(U.uDog, X.ox, X.oy, X.c, X.s); gl.uniform4f(U.uDogS, X.S, upp, 0, 0);
    gl.uniform4f(U.uHead, g.head.x, g.head.y, g.head.fx, g.head.fy);
    gl.uniform4f(U.uFace, g.head.hs, g.head.tip, 1 - clamp(SP.eye.x, 0, 1), clamp(SP.tongue.x, 0, 1));
    gl.uniform4f(U.uFace2, g.r, EARS[T.ear].inner, -1, 0);
    gl.uniform4f(U.uCol, g.collar.x, g.collar.y, g.collar.ax, g.collar.ay); gl.uniform4f(U.uCol2, 6, T.hair > 2 ? 5 : 1.6, 9, 0);
    gl.uniform4f(U.uBed, X.bx, X.by, X.c, X.s); gl.uniform4f(U.uBedR, BED.rx, BED.ry, BED.bw, BED.h);
    const hl = toLocal(X, hand.sx, hand.sy), hr = hand.rot;
    gl.uniform4f(U.uHand, hand.sx, hand.sy, hand.a, 0); gl.uniform4f(U.uHand2, Math.cos(hr), Math.sin(hr), 1.2, 0);
    gl.uniform4f(U.uHandL, hl[0], hl[1], clamp(SP.handP.x, 0, 1.2) * 5 * hand.a, 0);
    gl.uniform4f(U.uFlowRect, FR.x0, FR.y0, 1 / FR.w, 1 / FR.h);
    gl.uniform4f(U.uPat, k.pat, k.fleck ? 1 : 0, 0, 1);
    const hairLen = 9.5 * T.hair;
    gl.uniform4f(U.uHair, clamp(1.25 * upp, .45, 2.2), hairLen, T.hair > 2 ? .55 : .28, Math.min(hairLen * .2, 6));
    if (portrait) gl.uniform4f(U.uSun, -70, -150, 190, 215); else gl.uniform4f(U.uSun, -150, -90, 250, 185);
    gl.uniform4f(U.uMisc, st.t, (st.t * 7.13) % 1, (st.t * 3.71) % 1, 0);
    gl.uniform4f(U.uBound, 36, 0, 345 + T.fluff * 2, 0);
    const base = lin(k.base), light = lin(k.light);
    gl.uniform3fv(U.uBase, base); gl.uniform3fv(U.uUnder, k.pat === 0 ? mixc(base, light, .7) : light); gl.uniform3fv(U.uPatch, lin(k.patch || k.base));
    gl.uniform3fv(U.uCollarC, lin(k.collar)); gl.uniform3fv(U.uL, LIGHT);
    uploadFlow();
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  }
  const px1 = new Uint8Array(4);
  function timedRender() { const t0 = performance.now(); render(); if (gl && !glErr) gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px1); return performance.now() - t0; }

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
    if (o.type && TYPES[o.type]) cfg.type = o.type;
    if (o.coat != null) { const c = typeof o.coat === 'number' ? COATS[o.coat] : COATS.find(v => v.id === o.coat); if (c) cfg.coat = c.id; }
    if (o.size != null && isFinite(+o.size)) cfg.size = clamp(+o.size, .7, 1);
    if (o.fat != null && isFinite(+o.fat)) cfg.fat = clamp(+o.fat, .82, 1.3);
    makeRest(); syncUI(); if (!quiet) save();
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
    const second = c.pat === 4 ? c.patch : c.pat === 0 ? null : c.light;
    b.style.background = second ? `linear-gradient(135deg, ${c.base} 0 58%, ${second} 58% 100%)` : c.base;
    b.addEventListener('click', () => applyCfg({ coat: c.id })); $('inuCoats').appendChild(b);
  }
  $('inuSize').addEventListener('input', e => applyCfg({ size: e.target.value / 100 }));
  $('inuFat').addEventListener('input', e => applyCfg({ fat: e.target.value / 100 }));
  $('inuRand').addEventListener('click', () => {
    let t = cfg.type, c = cfg.coat; while (t === cfg.type && c === cfg.coat) { t = TYPE_IDS[Math.floor(Math.random() * TYPE_IDS.length)]; c = COATS[Math.floor(Math.random() * COATS.length)].id; }
    applyCfg({ type: t, coat: c, size: .74 + Math.random() * .24, fat: .86 + Math.random() * .4 });
    SP.earTw.v += 8; SP.look.v += 3;
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
  let tPrev = performance.now(), fAcc = 0, fN = 0, frame = 0, slow = 0, quick = 0, paused = false, lastDown = -1e9;
  // 重い端末では描画解像度を段階的に下げる（1コマの描画時間で判断）
  function adapt(ms) {
    st.ms = ms;
    if (ms > 21) { quick = 0; if (++slow >= 2 && st.level < RES.length - 1) { let l = st.level; while (l < RES.length - 1 && ms * Math.pow(RES[l] / RES[st.level], 2) > 19) l++; st.level = l; slow = 0; needSize = true; lastDown = performance.now(); } }
    else { slow = 0; if (ms < 6 && st.level > 0 && performance.now() - lastDown > 15000) { if (++quick >= 5) { st.level--; quick = 0; needSize = true; } } else quick = 0; }
  }
  function loop(now) {
    const real = (now - tPrev) / 1000; tPrev = now;
    if (real < .5) { fAcc += real; fN++; }
    if (!paused && gl && !glErr) {
      sim(clamp(real, .001, .05));
      if (++frame % 30 === 0 || frame < 4 || st.ms > 45) adapt(timedRender()); else render();
      ui(false);
    }
    if (fN >= 60) { st.fps = fAcc > 0 ? fN / fAcc : 0; fAcc = 0; fN = 0; }
    requestAnimationFrame(loop);
  }
  const okGL = initGL();
  load(); makeRest(); syncUI();
  if (okGL) { size(); G = pose(poseQ()); render(); }
  ui(true);
  window.addEventListener('resize', () => { needSize = true; });
  window.addEventListener('pagehide', () => { if (st.dirty) save(); });
  requestAnimationFrame(loop);

  // ---------- テスト用（裏のタブでは requestAnimationFrame が止まるため） ----------
  window.__t = {
    step(sec) { const n = Math.max(1, Math.round((sec || 0) * 60)); for (let i = 0; i < n; i++) sim(1 / 60); st.ms = timedRender(); ui(true); return this.s; },
    // region: 'head'|'chin'|'back'|'belly'|'paw'|'tail' / dir: 0=行ったり来たり, 1=頭→しっぽの向きだけ, -1=しっぽ→頭の向きだけ（逆なで）
    pet(region, sec, speed, dir) {
      sec = sec || 1; speed = speed || 260; dir = dir || 0; const n = Math.max(1, Math.round(sec * 60)); let ph = 0;
      hand.over = false; hand.was = false;
      for (let i = 0; i < n; i++) {
        const X = xform(); G = pose(poseQ());
        const a = anchorLocal(region), A = region === 'paw' || region === 'tail' ? 10 : region === 'head' || region === 'chin' ? 18 : 44;
        let off, on = true;
        if (dir) { ph += speed / (2 * A) / 60; const f = ph % 1.25; on = f < 1; off = -dir * (Math.min(f, 1) * 2 - 1) * A; }
        else { ph += speed * (Math.PI / 2) / A / 60; off = Math.sin(ph) * A; }
        const c = fromLocal(X, a[0] + off, a[1] + Math.cos(ph * .5) * 1.5);
        hand.x = c[0]; hand.y = c[1]; hand.over = on; hand.down = on; hand.mouse = true;
        sim(1 / 60);
      }
      const out = this.s; st.ms = timedRender(); ui(true); hand.down = false; hand.over = false; return out;
    },
    set(o) { applyCfg(o || {}); render(); return this.s; },
    pause(v) { paused = v !== false; return paused; },
    level(v) { st.level = clamp(v | 0, 0, RES.length - 1); needSize = true; return timedRender(); },
    reset() { st.count = 0; st.sec = 0; st.happy = 15; st.sleepyT = 0; SP.roll.t = 0; flowX.fill(0); flowY.fill(0); flowDirty = true; st.dirty = true; ui(true); },
    get s() {
      let nan = false; for (const n in SP) if (!isFinite(SP[n].x) || !isFinite(SP[n].v)) nan = true; if (!isFinite(st.happy) || !isFinite(st.wagPh) || !isFinite(flowE)) nan = true;
      if (G) for (const p of G.P) if (!isFinite(p.ax + p.ay + p.bx + p.by + p.ra + p.rb + p.ha + p.hb + p.fx + p.fy)) nan = true;
      const f = v => Math.round(v * 100) / 100;
      return { happy: f(st.happy), pose: SP.roll.t > .5 ? 'hesoten' : 'fuse', roll: f(SP.roll.x), wag: { hz: f(st.wagHz), amp: f(SP.wagAmp.x + st.wagBoost) }, eye: f(SP.eye.x), ear: f(SP.ear.x), headRot: f(SP.headRot.x), headX: f(SP.headX.x), headY: f(SP.headY.x),
        look: f(SP.look.x), kick: f(SP.kick.x), paw: f(SP.paw.x), tap: f(SP.tap.x), tuck: f(SP.tuck.x), tongue: f(SP.tongue.x), sleepy: f(SP.sleepy.x), region: st.reg, mood: st.mood, idle: f(st.idle), evt: st.evt ? st.evt.type : null,
        counts: { pets: st.count, sec: f(st.sec) }, cfg: Object.assign({}, cfg), prims: G ? G.P.length : 0, flow: f(flowE), fps: f(st.fps), ms: f(st.ms), scale: RES[st.level], level: st.level, W, H, dpr, cw: cv.width, chh: cv.height, glErr, nan };
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
