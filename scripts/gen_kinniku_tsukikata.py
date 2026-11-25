# -*- coding: utf-8 -*-
"""筋肉がつく仕組みシミュレーター（2026-11-25・リクエスト「筋肉のつきかた」）
   sims/kinniku-tsukikata/index.html を書き出す（冪等）。 使い方: python -X utf8 scripts/gen_kinniku_tsukikata.py"""
import html as H, io, json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://shimulabo.com"
SLUG = "kinniku-tsukikata"
NAME = "筋肉がつく仕組みシミュレーター"
CAT = "健康・カラダ"
TITLE = "筋肉がつく仕組みシミュレーター｜筋トレ・たんぱく質・すいみんで筋線維はどう太くなる？｜シミュラボ"
DESC = ("筋トレをすると筋肉が太くなる仕組みを、筋線維の絵とグラフで見るシミュレーター。トレーニングの回数・強さ・たんぱく質・すいみんを変えると、"
        "筋たんぱく質の「合成」と「分解」のバランス、疲労と回復、筋肉量の指数がどう変わるかが分かります。やりすぎや、やめたときの変化もためせます。")
OG_T = "筋肉がつく仕組みシミュレーター（筋トレ・栄養・休養でどう変わる？）"
OG_D = "筋線維が太くなる様子と、合成・分解のバランス、疲労と回復をアニメとグラフで。回数・強さ・たんぱく質・すいみんを変えてためせます。"
H1 = "筋肉がつく仕組みシミュレーター<br>筋トレ・栄養・休養でどう変わる？"
LEAD = ("筋トレをすると、筋肉を作っている細長い細胞（筋線維）の1本1本が、少しずつ太くなっていきます。"
        "トレーニングの回数・強さ・たんぱく質・すいみんを変えて、筋線維の絵とグラフがどう変わるかをためしてみましょう。")
NOTE = ("この数字は仕組みを見るための簡単なモデルです。伸び方は年齢・体質・経験で大きく変わります。"
        "成長期の人は無理な高重量を避け、指導者や保護者と相談を。持病やけがのある人は医師に相談を。")
REQ = "💌 このシミュレーターは、リクエスト「筋肉のつきかた」から作りました。"

FAQ = [
    ("筋トレをすると、筋線維の数が増えるのですか？",
     "筋肉が太くなるのは、おもに筋線維の1本1本が太くなるため（筋肥大）と考えられています。人の体で筋線維の数が増えるのかどうかは、はっきり分かっていません。このシミュレーターでは、数は19本のまま、太さだけが変わるようにえがいています。"),
    ("毎日きつくやれば、早く筋肉がつきますか？",
     "そうとは限りません。このシミュレーターでは、休みなしで毎日きつく行い、すいみんも短いと、疲れがたまって1回ごとのトレーニングの質が下がり、伸びが止まるようにしてあります。実際にどのくらいの回数がちょうどよいかは、人や種目によってちがいます。"),
    ("筋肉痛がないと、筋トレの効果はないのですか？",
     "筋肉痛がなくても筋肉は伸びます。筋肉痛の強さと筋肉の伸びは、かならずしも一致しないと考えられています。慣れてくると、同じトレーニングでも筋肉痛は出にくくなります。"),
    ("この指数は、実際の体の変化と同じですか？",
     "いいえ。開始のときを100とした「モデルの中の数字」で、実際の体重や筋肉の重さを表すものではありません。伸び方は年齢・体質・経験・種目などで大きく変わります。絵の太さの変化も、見やすいように大きめにえがいています。"),
]
REL = [("hone-kinniku", "🦴", "ほねときん肉のシミュレーター（うでの曲げのばし・関節）"),
       ("kintore-1rm", "🏋️", "1RM計算機（最大挙上重量）"),
       ("suimin-cycle", "😴", "快眠の起床時刻シミュレーター")]

ARTICLE = """
<h2>筋肉は何でできている？</h2>
<p>うでや足を動かす筋肉（骨格筋）は、<b>筋線維（きんせんい）</b>という細長い細胞がたくさん集まった束です。筋線維の中には、さらに細い<b>筋原線維（きんげんせんい）</b>がぎっしりならんでいて、これはアクチンやミオシンなどの<b>たんぱく質</b>でできています。</p>
<p>上の絵の「② 輪切りにしたところ」が筋線維の束、「③ 筋線維1本を横から」のしま模様が、筋原線維のならびを表しています。</p>

<h2>筋トレで太くなる仕組み</h2>
<p>筋肉のたんぱく質は、いつも少しずつ<b>作られ（合成）</b>、少しずつ<b>こわされて（分解）</b>います。ふだんは、この2つがほぼつり合っているので、筋肉の量は大きく変わりません。</p>
<ol>
<li><b>刺激</b>：筋トレで、筋線維にふだんより大きな力がかかります。</li>
<li><b>合成が高まる</b>：その刺激をきっかけに、筋たんぱく質の合成が高まります。筋トレのあと、合成が高まった状態は24〜48時間ほど続くという報告があります（続く長さは、人やトレーニングの内容によってちがいます）。</li>
<li><b>合成が分解を上回る</b>：合成が分解より多い時間が積み重なると、筋線維の中のたんぱく質が増え、1本1本が少しずつ太くなります。</li>
</ol>
<p>グラフ①の緑の線（合成）が、トレーニングのあとに山になるのがこの動きです。山と山のあいだでは分解のほうが少し多い時間もあり、差し引きでプラスの日が続くと、グラフ③の線がゆっくり上がっていきます。</p>
<p>絵では、トレーニングの直後に筋線維に小さな傷み（赤い点）が出て、休んでいる間に直っていく様子をえがいています。ただし、<b>傷みが大きいほどよく伸びる、というわけではありません</b>。太くなるきっかけとして大事なのは、筋線維にかかる力そのものだと考えられています。</p>

<h2>はじめは伸びやすく、だんだんゆるやかに</h2>
<p>このシミュレーターでは、筋肉が増えるほど、それを保つために必要な刺激も増えるようにしてあります。そのため、はじめは線がよく上がり、続けるほど上がり方がゆるやかになります。トレーニングをやめると合成の山がなくなり、時間をかけて元の太さにもどっていきます（プリセット「8週つづけて、やめる」でためせます）。</p>

<h2>休養とすいみんが大事な理由</h2>
<p>筋肉が太くなるのは、トレーニングをしている最中ではなく、そのあとの<b>休んでいる時間</b>です。合成が高まっている間に次のきついトレーニングを重ねすぎると、疲れがぬけないまま次の日をむかえることになります。</p>
<p>このシミュレーターでは、すいみんが短いと疲労のぬけ方がおそくなり、疲労がたまると1回のトレーニングで出せる力（刺激）が小さくなります。「毎日きつく・寝不足」のプリセットで、グラフ②の疲労が高いままになり、グラフ③の伸びが止まる様子を見てみましょう。これは「やりすぎ（オーバーワーク）」を単純にしたモデルです。</p>

<h2>たんぱく質の役割</h2>
<p>筋たんぱく質の材料は、食事でとったたんぱく質が分解されてできる<b>アミノ酸</b>です。材料が足りないと、刺激があっても合成が十分に高まりません。絵の中の青緑の小さなつぶが、血管から筋線維へ運ばれるアミノ酸を表しています。</p>
<p>では、とればとるほどよいのでしょうか。筋トレをしている人を対象にした研究をまとめた報告では、たんぱく質の量が体重1kgあたり1日およそ1.6gをこえると、筋肉を増やす効果はそれ以上あまり伸びなくなる、とされています。ただし、ちょうどよい量は年齢・体格・運動の量などによって人それぞれちがいます。腎臓などに持病のある人は、食事を変える前に医師に相談してください。</p>

<h2>「超回復」という考え方について</h2>
<p>「トレーニングで一度下がった力が、休むと元より少し高いところまで回復する。そのタイミングで次のトレーニングをするとよい」という<b>超回復</b>の説明を聞いたことがあるかもしれません。これは、休養の大切さをつかむための<b>分かりやすいモデル</b>です。</p>
<p>実際の体の中では、筋たんぱく質の合成と分解、エネルギーの回復、神経のはたらきの変化などが、それぞれちがう速さで進んでいて、1本の線で表せるほど単純ではありません。「何時間休めば必ず超回復する」と決まった数字があるわけではない点に注意してください。このシミュレーターも、同じように単純化したモデルの一つです。</p>

<h2>筋肉痛は成長のしるし？</h2>
<p>筋肉痛は、慣れない動きや強い運動のあとに出やすい痛みです。「筋肉痛がきたから効いている」と感じやすいのですが、<b>筋肉痛がなくても筋肉は伸びますし、痛みの強さと伸び方は一致しない</b>と考えられています。同じトレーニングを続けると、筋肉痛は出にくくなっていきます。強い痛みが長く続くときや、関節が痛むときは、無理をせず休みましょう。</p>

<h2>筋肉は骨にどうついている？</h2>
<p>筋肉の両はしは<b>けん（腱）</b>になって骨についていて、筋肉がちぢむと骨が引っぱられ、関節が曲がります。うでの曲げのばしで、どの筋肉がちぢんでいるのかは、<a href="../hone-kinniku/">ほねときん肉のシミュレーター</a>で動かして見ることができます。</p>

<h2>このシミュレーターのモデル</h2>
<ul>
<li>1日を20コマに分けて計算しています。トレーニングの日は、週の中でなるべく間があくように決めています。</li>
<li><b>合成</b>：トレーニングの刺激で上がり、1〜2日かけて下がります。たんぱく質とすいみんが少ないと、上がり方が小さくなります。</li>
<li><b>分解</b>：筋肉量が増えるほど少し大きくなり、疲労がたまりすぎたときも大きくなります。</li>
<li><b>疲労</b>：トレーニングのたびに増え（きついほど大きく）、すいみんが十分なほど早くぬけます。疲労が高いと、次のトレーニングの刺激が小さくなります。</li>
<li><b>筋肉量の指数</b>：「合成 − 分解」を足し合わせたものです。開始を100としています。</li>
</ul>
<p>式の中の数字は、動きを見やすくするために決めたもので、実際の人の体を測って決めたものではありません。</p>
"""

REFS = [
    "MacDougall, J. D. ほか (1995) The time course for elevated muscle protein synthesis following heavy resistance exercise. Canadian Journal of Applied Physiology.（筋トレ後に筋たんぱく質の合成が高まっている時間）",
    "Phillips, S. M. ほか (1997) Mixed muscle protein synthesis and breakdown after resistance exercise in humans. American Journal of Physiology.（筋トレ後の合成と分解）",
    "Morton, R. W. ほか (2018) A systematic review, meta-analysis and meta-regression of the effect of protein supplementation on resistance training-induced gains in muscle mass and strength in healthy adults. British Journal of Sports Medicine.（たんぱく質の量と効果の頭打ち）",
]

STAGE = r"""
<style>
.kt-seg{display:flex;flex-wrap:wrap;gap:6px}
.kt-seg button,.kt-tools button{border:1.5px solid var(--line);background:#fff;border-radius:999px;padding:8px 13px;font:inherit;font-size:13.5px;font-weight:800;cursor:pointer;color:var(--ink)}
.kt-seg button.on{background:#dc2626;border-color:#dc2626;color:#fff}
.kt-stage{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px}
.kt-cv{position:relative;border-radius:14px;overflow:hidden;border:1px solid var(--line);background:#fffaf5;min-width:0}
.kt-cv canvas{display:block;width:100%;aspect-ratio:100/105;touch-action:manipulation}
#ktA{cursor:pointer}
.kt-msg{position:absolute;left:50%;top:8px;transform:translateX(-50%);background:rgba(15,23,42,.86);color:#fff;font-size:12.5px;font-weight:700;border-radius:12px;padding:6px 14px;max-width:92%;text-align:center;pointer-events:none;opacity:0;transition:opacity .3s;white-space:nowrap}
.kt-msg.show{opacity:1}
.kt-tools{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-top:10px}
.kt-tools button.on{background:#0f172a;border-color:#0f172a;color:#fff}
.kt-tools button.kt-go{background:#dc2626;border-color:#dc2626;color:#fff}
.kt-sum{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:12px}
.kt-sum div{background:#fef2f2;border-radius:12px;padding:10px 4px;text-align:center}
.kt-sum b{display:block;font-size:22px;color:#b91c1c;font-variant-numeric:tabular-nums}
.kt-sum b small{font-size:11.5px}
.kt-sum span{font-size:11.5px;color:var(--ink-2);font-weight:700}
.kt-sum div.warn{background:#fff7ed}.kt-sum div.warn b{color:#c2410c}
.kt-say{font-size:13.5px;color:var(--ink);background:#fef2f2;border-radius:10px;padding:9px 12px;margin:10px 0 0;font-weight:700;min-height:2.9em}
.kt-note{font-size:13px;color:var(--ink-2);background:#f8fafc;border:1px solid var(--line);border-radius:10px;padding:9px 12px;margin:8px 0 0;line-height:1.7}
.kt-cols{display:grid;grid-template-columns:1fr 1fr;gap:6px 22px;margin-top:6px}
.kt-hint{font-size:13px;color:var(--ink-2);margin:6px 0 0}
@media (max-width:640px){.kt-stage{grid-template-columns:1fr}.kt-cols{grid-template-columns:1fr}.kt-seg button,.kt-tools button{padding:8px 11px;font-size:13px}.kt-sum b{font-size:19px}}
</style>
"""

BODY = r"""
  <section class="panel" id="resultPanel">
    <h2 style="margin:0 0 8px;font-size:18px;">① まずはこの4つをくらべてみよう</h2>
    <div class="kt-seg" id="ktPre">
      <button type="button" data-p="1">🙂 週3回・しっかり食べて寝る</button>
      <button type="button" data-p="2">🥵 毎日きつく・寝不足</button>
      <button type="button" data-p="3">🛋 何もしない</button>
      <button type="button" data-p="4">⏹ 8週つづけて、やめる</button>
    </div>

    <div class="kt-stage">
      <div class="kt-cv">
        <canvas id="ktA" aria-label="うでの筋肉を輪切りにした絵と、筋線維1本を横から見た絵。トレーニングのあとに小さな傷みが出て、休むと直り、少しずつ太くなる"></canvas>
        <div class="kt-msg" id="ktMsg"></div>
      </div>
      <div class="kt-cv">
        <canvas id="ktG" aria-label="合成と分解のバランス、疲労と回復、筋肉量の指数のグラフ"></canvas>
      </div>
    </div>
    <div class="kt-tools">
      <button type="button" id="ktPlay">⏸ 止める</button>
      <button type="button" data-sp="0.35">🐢 スロー</button>
      <button type="button" data-sp="2" class="on">ふつう</button>
      <button type="button" data-sp="10">⏩ 早送り</button>
      <button type="button" id="ktEnd">⏭ 最後まで</button>
      <button type="button" id="ktReset">↺ はじめから</button>
      <button type="button" id="ktNow" class="kt-go">💪 いま1回やる</button>
    </div>
    <div class="kt-sum">
      <div><b id="mDay">0</b><span>経過日数</span></div>
      <div><b id="mIdx">100.0</b><span>筋肉量の指数（開始＝100）</span></div>
      <div id="mFatBox"><b id="mFat">0</b><span>疲労</span></div>
    </div>
    <p class="kt-say" id="ktSay">　</p>

    <h2 style="margin:20px 0 4px;font-size:18px;">② 自分で変えてみる（とちゅうでも変えられます）</h2>
    <div class="kt-cols">
      <div class="field"><label>🏋️ トレーニングの回数 <span class="hint">（<b id="vFreq"></b>）</span></label><input type="range" id="kFreq" min="0" max="7" step="1" value="3"></div>
      <div class="field"><label>強さ</label><div class="kt-seg" id="ktLoad"><button type="button" data-v="0">軽い</button><button type="button" data-v="1">ふつう</button><button type="button" data-v="2">きつい</button></div></div>
      <div class="field"><label>🍗 たんぱく質</label><div class="kt-seg" id="ktProt"><button type="button" data-v="0">少ない</button><button type="button" data-v="1">ふつう</button><button type="button" data-v="2">十分</button></div></div>
      <div class="field"><label>😴 すいみん</label><div class="kt-seg" id="ktSleep"><button type="button" data-v="0">短い</button><button type="button" data-v="1">ふつう</button><button type="button" data-v="2">十分</button></div></div>
      <div class="field"><label>📅 期間</label><div class="kt-seg" id="ktWeeks"><button type="button" data-v="4">4週</button><button type="button" data-v="8">8週</button><button type="button" data-v="12">12週</button><button type="button" data-v="24">24週</button></div></div>
    </div>
    <p class="kt-hint">左の絵をタップ（クリック）しても、その場で1回トレーニングできます。続けてたくさん押すと、疲れて力が出なくなる様子が見られます。絵の中の小さな青緑の丸は、材料（アミノ酸）を運ぶ毛細血管です。グラフ③の灰色の点線は、1つ前にためした結果です。</p>

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
  const cA = $('ktA'), a = cA.getContext('2d'), cG = $('ktG'), g = cG.getContext('2d');
  const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
  const lerp = (p, q, f) => p + (q - p) * f;
  function rng(s) { s = s >>> 0; return () => { s = (s + 0x6D2B79F5) >>> 0; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
  const FONT = 'system-ui,-apple-system,"Hiragino Sans","Noto Sans JP",sans-serif';

  // ---------- モデル（仕組みを見るための簡単なもの） ----------
  const LOAD = [.55, .8, 1], PS = [.72, .92, 1], SS = [.8, .95, 1], RS = [.45, .8, 1], BP = [.04, 0, 0], BS = [.02, 0, 0];
  const DAYS = [[], [2], [1, 4], [0, 2, 4], [0, 1, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5, 6]];
  const WD = ['月', '火', '水', '木', '金', '土', '日'];
  const K = { fc: .55, fe: 2, qk: 1.15, q0: .2, qmin: .3, mix: .3, cap: 1.4, kC: .12, c0: .5, cw: .5, cp: .028, G: .5, tauC: 16, kS: .15 };
  const SPD = 20, DT = 1 / SPD, TRAIN_STEP = 8, WIN = 14;
  const st = { freq: 3, load: 1, protein: 2, sleep: 2, weeks: 12 };
  let n = 0, t = 0, M = 100, F = 0, C = 0, A = 0, S = 0, dmg = 0, syn = 1, brk = 1, lastQ = 1, lastTrainT = -9;
  let recent = [], mhist = [], trains = [], ghost = null, quitAt = null, maxM = 100;
  let playing = true, ended = false, speed = 2, acc = 0, quiet = false, curPreset = 1;

  function rates() {
    syn = 1 - BP[st.protein] - BS[st.sleep] + S * PS[st.protein] * SS[st.sleep];
    brk = 1 + K.cp * (M - 100) + K.kC * Math.tanh(Math.max(0, C - K.c0) / K.cw) + K.kS * S;
  }
  function train() {
    const L = LOAD[st.load], fe = K.mix * F + (1 - K.mix) * C;
    const q = clamp(1 - K.qk * Math.max(0, fe - K.q0), K.qmin, 1);
    A += Math.max(0, L * q * .9 * (1 - (S + A) / K.cap));
    F = Math.min(4, F + K.fc * Math.pow(L, K.fe));
    dmg = Math.min(1, dmg + .42 * L * (.5 + .5 * q));
    lastQ = q; lastTrainT = t; trains.push(t); if (trains.length > 60) trains.shift();
    if (!quiet) { fx.curl = 1.15; fx.pulse = .7; fx.word = q < .6 ? 1 : 0; }
    syncDots(true);
  }
  function stepSim() {
    if (quitAt != null && t >= quitAt) { quitAt = null; st.freq = 0; syncUI(); if (!quiet) flash('ここでトレーニングをやめました'); }
    const day = Math.floor(n / SPD);
    if (n % SPD === TRAIN_STEP && DAYS[st.freq].includes(day % 7)) train();
    const dA = A / .15 * DT; A -= dA; S += dA - S / 1.1 * DT;
    F += -F * .62 * RS[st.sleep] * DT; C += (F - C) / K.tauC * DT;
    dmg += -dmg * .8 * RS[st.sleep] * DT;
    rates();
    M += K.G * (syn - brk) * DT;
    n++; t = n / SPD; maxM = Math.max(maxM, M);
    recent.push([t, syn, brk, F, C]); if (recent.length > WIN * SPD + 1) recent.shift();
    if (n % SPD === 0) mhist.push([t, M]);
    syncDots(false);
  }
  function reset(keep) {
    if (keep && mhist.length > 7) ghost = mhist.slice();
    n = 0; t = 0; M = 100; F = 0; C = 0; A = 0; S = 0; dmg = 0; lastQ = 1; lastTrainT = -9; maxM = 100;
    recent = []; mhist = [[0, 100]]; trains = []; dots = []; glints = []; parts = []; Msm = 100; bal = 0;
    rates(); recent.push([0, syn, brk, 0, 0]);
    ended = false; playing = true; acc = 0; updPlay();
  }
  const isNaNState = () => ![M, F, C, A, S, dmg, syn, brk, t].every(Number.isFinite);

  // ---------- 絵のための準備 ----------
  const R1 = rng(77), FIB = [], CAPS = [];
  (function () {
    const pts = [[0, 0]];
    for (let k = 0; k < 6; k++) { const an = k * Math.PI / 3; pts.push([Math.cos(an), Math.sin(an)]); }
    for (let k = 0; k < 6; k++) { const an = k * Math.PI / 3, b = an + Math.PI / 6, q = Math.sqrt(3); pts.push([2 * Math.cos(an), 2 * Math.sin(an)]); pts.push([q * Math.cos(b), q * Math.sin(b)]); }
    pts.forEach(p => { const sh = []; for (let i = 0; i < 9; i++) sh.push(.93 + R1() * .13); FIB.push({ ux: p[0] + (R1() - .5) * .06, uy: p[1] + (R1() - .5) * .06, sh, rot: R1() * 6.28 }); });
    for (let k = 0; k < 6; k++) { const b = k * Math.PI / 3 + Math.PI / 6; CAPS.push([.58 * Math.cos(b), .58 * Math.sin(b)]); }
    for (let k = 0; k < 6; k++) for (const s of [-1, 1]) { const b = k * Math.PI / 3 + s * .19; CAPS.push([1.53 * Math.cos(b), 1.53 * Math.sin(b)]); }
    CAPS.forEach(c => { c.near = FIB.map((f, i) => [Math.hypot(f.ux - c[0], f.uy - c[1]), i]).sort((p, q) => p[0] - q[0]).slice(0, 3).map(p => p[1]); });
  })();
  let dots = [], glints = [], parts = [], Msm = 100, bal = 0;
  const fx = { curl: 0, pulse: 0, word: 0, time: 0 };
  function syncDots(isTrain) {
    const want = Math.round(dmg * 30);
    while (dots.length < want) dots.push({ fi: Math.floor(Math.random() * FIB.length), an: Math.random() * 6.28, rr: .15 + Math.random() * .7, sx: .04 + Math.random() * .92, sy: (Math.random() - .5) * 1.5, born: fx.time });
    while (dots.length > want) { const d = dots.shift(); if (!quiet && glints.length < 16) glints.push({ fi: d.fi, an: d.an, rr: d.rr, sx: d.sx, sy: d.sy, age: 0 }); }
  }
  function tickFx(dt) {
    fx.time += dt; fx.curl = Math.max(0, fx.curl - dt); fx.pulse = Math.max(0, fx.pulse - dt);
    Msm += (M - Msm) * Math.min(1, dt * 5); bal += ((syn - brk) - bal) * Math.min(1, dt * 7);
    glints.forEach(q => q.age += dt); glints = glints.filter(q => q.age < .75);
    const net = syn - brk, rate = Math.abs(net) < .015 ? 0 : Math.min(30, 5 + 34 * Math.abs(net));
    tickFx.acc = (tickFx.acc || 0) + rate * dt;
    while (tickFx.acc >= 1 && parts.length < 90) {
      tickFx.acc -= 1;
      const c = CAPS[Math.floor(Math.random() * CAPS.length)], f = FIB[c.near[Math.floor(Math.random() * 3)]], an = Math.random() * 6.28, r = Math.random() * .3;
      parts.push({ cx: c[0], cy: c[1], fx: f.ux + Math.cos(an) * r, fy: f.uy + Math.sin(an) * r, p: 0, inw: net > 0, v: 1 + Math.random() * .7 });
    }
    if (tickFx.acc > 3) tickFx.acc = 0;
    parts.forEach(q => q.p += dt * q.v); parts = parts.filter(q => q.p < 1);
  }

  // ---------- 絵：うで・輪切り・筋線維1本 ----------
  let dpr = 1;
  function size(cv) { const w = cv.clientWidth || 340; dpr = Math.min(2, window.devicePixelRatio || 1); const W = Math.round(w * dpr), Hh = Math.round(w * 1.05 * dpr); if (cv.width !== W || cv.height !== Hh) { cv.width = W; cv.height = Hh; } return w; }
  function rrect(c, x, y, w, h, r) { r = Math.min(r, w / 2, h / 2); c.beginPath(); c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r); c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath(); }
  function blob(c, x, y, r, sh, rot) {
    const m = sh.length, P = [];
    for (let i = 0; i < m; i++) { const an = rot + i / m * 6.2832; P.push([x + Math.cos(an) * r * sh[i], y + Math.sin(an) * r * sh[i]]); }
    c.beginPath(); const z = P[m - 1]; c.moveTo((z[0] + P[0][0]) / 2, (z[1] + P[0][1]) / 2);
    for (let i = 0; i < m; i++) { const p = P[i], q = P[(i + 1) % m]; c.quadraticCurveTo(p[0], p[1], (p[0] + q[0]) / 2, (p[1] + q[1]) / 2); }
    c.closePath();
  }
  function star(c, x, y, r) { c.beginPath(); for (let i = 0; i < 8; i++) { const an = i * Math.PI / 4, rr = i % 2 ? r * .32 : r; c.lineTo(x + Math.cos(an) * rr, y + Math.sin(an) * rr); } c.closePath(); }

  function drawA() {
    const W = size(cA), H = W * 1.05, c = a;
    c.setTransform(dpr, 0, 0, dpr, 0, 0); c.clearRect(0, 0, W, H);
    const bg = c.createLinearGradient(0, 0, 0, H); bg.addColorStop(0, '#fff7ed'); bg.addColorStop(1, '#fffdfa'); c.fillStyle = bg; c.fillRect(0, 0, W, H);
    const k = clamp(1 + (Msm - 100) / 100 * 3.2, .8, 1.42);
    const fs = Math.max(10, Math.min(12.5, W * .034));
    const day = Math.floor(t + 1e-9), dow = day % 7, plan = DAYS[st.freq];

    // 週の予定（月〜日）
    for (let i = 0; i < 7; i++) {
      const x = W * .055 + i * W * .056, y = W * .062, on = plan.includes(i), today = i === dow, r = W * (today ? .026 : .022);
      c.beginPath(); c.arc(x, y, r, 0, 7); c.fillStyle = on ? '#dc2626' : '#fff'; c.fill();
      c.lineWidth = today ? 2.4 : 1; c.strokeStyle = today ? '#0f172a' : on ? '#b91c1c' : '#cbd5e1'; c.stroke();
      c.fillStyle = on ? '#fff' : '#94a3b8'; c.font = `bold ${fs * .82}px ${FONT}`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(WD[i], x, y + .5);
    }
    c.fillStyle = '#334155'; c.font = `bold ${fs}px ${FONT}`; c.textAlign = 'left'; c.textBaseline = 'middle';
    c.fillText(`第${Math.floor(Math.max(0, t - 1e-6) / 7) + 1}週`, W * .44, W * .048);
    c.font = `${fs * .86}px ${FONT}`; c.fillStyle = '#64748b'; c.fillText(plan.includes(dow) ? 'トレーニングの日' : '休みの日', W * .44, W * .085);

    // うで
    const flexP = fx.curl > 0 ? 1 - fx.curl / 1.15 : 0, flex = fx.curl > 0 ? (1 - Math.cos(flexP * Math.PI * 4)) / 2 : 0;
    const sh = [-W * .06, W * .33], el = [W * .285, W * .372], th = lerp(-.9, -1.72, flex), fl = W * .165;
    const hand = [el[0] + Math.cos(th) * fl, el[1] + Math.sin(th) * fl];
    const ux = (el[0] - sh[0]), uy = (el[1] - sh[1]), ul = Math.hypot(ux, uy), nx = uy / ul, ny = -ux / ul; // n = 上向き
    const hb = W * .03 * (.75 + (k - 1) * 1.5) * (1 + .75 * flex);
    c.lineCap = 'round'; c.lineJoin = 'round';
    c.strokeStyle = '#e3ad86'; c.lineWidth = W * .094; c.beginPath(); c.moveTo(sh[0], sh[1]); c.lineTo(el[0], el[1]); c.stroke();
    c.lineWidth = W * .074; c.beginPath(); c.moveTo(el[0], el[1]); c.lineTo(hand[0], hand[1]); c.stroke();
    c.strokeStyle = '#f6cfae'; c.lineWidth = W * .084; c.beginPath(); c.moveTo(sh[0], sh[1]); c.lineTo(el[0], el[1]); c.stroke();
    c.lineWidth = W * .064; c.beginPath(); c.moveTo(el[0], el[1]); c.lineTo(hand[0], hand[1]); c.stroke();
    // 力こぶ（皮ふのふくらみ → 中の筋肉）
    const b0 = [sh[0] + ux * .3, sh[1] + uy * .3], b1 = [sh[0] + ux * .95, sh[1] + uy * .95], bm = [(b0[0] + b1[0]) / 2, (b0[1] + b1[1]) / 2];
    const spindle = (up, dn) => { c.beginPath(); c.moveTo(b0[0], b0[1]); c.quadraticCurveTo(bm[0] + nx * up, bm[1] + ny * up, b1[0], b1[1]); c.quadraticCurveTo(bm[0] - nx * dn, bm[1] - ny * dn, b0[0], b0[1]); c.closePath(); };
    spindle(hb * 2 + W * .05, W * .02); c.fillStyle = '#f6cfae'; c.fill(); c.strokeStyle = '#e3ad86'; c.lineWidth = 1; c.stroke();
    spindle(hb * 2 + W * .018, W * .012); const mg = c.createLinearGradient(0, bm[1] - hb * 1.6, 0, bm[1] + W * .02); mg.addColorStop(0, '#f08a7c'); mg.addColorStop(1, '#d9534a'); c.fillStyle = mg; c.fill(); c.strokeStyle = '#b4372f'; c.lineWidth = 1; c.stroke();
    c.strokeStyle = 'rgba(255,255,255,.45)'; c.lineWidth = 1.2; c.beginPath(); c.moveTo(b0[0] + ux * .08, b0[1] + uy * .08 + ny * hb * .5); c.quadraticCurveTo(bm[0] + nx * (hb * 1.25), bm[1] + ny * (hb * 1.25), b1[0] - ux * .08, b1[1] - uy * .08 + ny * hb * .4); c.stroke();
    // こぶし とダンベル
    c.fillStyle = '#f6cfae'; c.strokeStyle = '#e3ad86'; c.lineWidth = 1.2; c.beginPath(); c.arc(hand[0], hand[1], W * .04, 0, 7); c.fill(); c.stroke();
    const px = -Math.sin(th), py = Math.cos(th), dl = W * .062;
    c.strokeStyle = '#64748b'; c.lineWidth = W * .014; c.beginPath(); c.moveTo(hand[0] - px * dl, hand[1] - py * dl); c.lineTo(hand[0] + px * dl, hand[1] + py * dl); c.stroke();
    for (const s of [-1, 1]) { c.strokeStyle = '#1e293b'; c.lineWidth = W * (.03 + .012 * st.load); const hx = hand[0] + s * px * dl, hy = hand[1] + s * py * dl, tx = Math.cos(th) * W * (.022 + .008 * st.load), ty = Math.sin(th) * W * (.022 + .008 * st.load); c.lineCap = 'butt'; c.beginPath(); c.moveTo(hx - tx, hy - ty); c.lineTo(hx + tx, hy + ty); c.stroke(); c.lineCap = 'round'; }
    if (fx.curl > 0) {
      c.font = `bold ${fs * 1.05}px ${FONT}`; c.textAlign = 'left'; c.textBaseline = 'middle'; c.fillStyle = fx.word ? '#64748b' : '#dc2626';
      c.fillText(fx.word ? 'つかれて力が出ない…' : 'トレーニング！', W * .03, W * .135);
    }
    // 合成と分解のてんびん
    {
      const bx = W * .225, by = W * .642, bl = W * .15, ang = -clamp(bal * 1.3, -.3, .3);
      c.fillStyle = '#334155'; c.font = `bold ${fs * .84}px ${FONT}`; c.textAlign = 'left'; c.textBaseline = 'top'; c.fillText('合成と分解のてんびん', W * .03, W * .548);
      c.fillStyle = '#94a3b8'; c.beginPath(); c.moveTo(bx, by); c.lineTo(bx - W * .028, by + W * .042); c.lineTo(bx + W * .028, by + W * .042); c.closePath(); c.fill();
      c.save(); c.translate(bx, by); c.rotate(ang);
      c.strokeStyle = '#475569'; c.lineWidth = 3; c.beginPath(); c.moveTo(-bl, 0); c.lineTo(bl, 0); c.stroke();
      const box = (x, v, col, edge, txt) => { const bh = W * .034 * clamp(v, .6, 2.2), bw = W * .1; rrect(c, x - bw / 2, -bh - 1.5, bw, bh, 4); c.fillStyle = col; c.fill(); c.strokeStyle = edge; c.lineWidth = 1; c.stroke(); c.fillStyle = '#fff'; c.font = `bold ${fs * .8}px ${FONT}`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(txt, x, -bh / 2 - 1); };
      box(-bl + W * .045, syn, '#16a34a', '#15803d', '合成'); box(bl - W * .045, brk, '#ea580c', '#c2410c', '分解');
      c.restore();
      c.beginPath(); c.arc(bx, by, 3, 0, 7); c.fillStyle = '#1e293b'; c.fill();
    }
    // 輪切りの線と、拡大の案内線
    const cut0 = [bm[0] + nx * (hb * 1.05 + W * .035), bm[1] + ny * (hb * 1.05 + W * .035)], cut1 = [bm[0] - nx * W * .022, bm[1] - ny * W * .022];
    const cx = W * .705, cy = W * .40, Rb = W * .185, R = Rb * k * (1 + .035 * Math.sin(Math.min(1, fx.pulse / .7) * Math.PI) * (fx.pulse > 0 ? 1 : 0));
    c.strokeStyle = 'rgba(100,116,139,.5)'; c.lineWidth = 1; c.setLineDash([3, 3]);
    c.beginPath(); c.moveTo(cut0[0], cut0[1]); c.lineTo(cx - R * .5, cy - R * .87); c.moveTo(cut1[0], cut1[1]); c.lineTo(cx - R * .5, cy + R * .87); c.stroke(); c.setLineDash([]);
    c.strokeStyle = '#0f172a'; c.lineWidth = 1.6; c.setLineDash([4, 3]); c.beginPath(); c.moveTo(cut0[0], cut0[1]); c.lineTo(cut1[0], cut1[1]); c.stroke(); c.setLineDash([]);
    c.fillStyle = '#334155'; c.font = `bold ${fs * .92}px ${FONT}`; c.textAlign = 'left'; c.textBaseline = 'top'; c.fillText('① うで（力こぶ）', W * .03, W * .445);
    c.font = `${fs * .84}px ${FONT}`; c.fillStyle = '#64748b'; c.fillText('点線のところを輪切りに →', W * .03, W * .49);

    // 輪切り（筋線維の束）
    const d = R / 2.56, rf = d * .465;
    c.beginPath(); c.arc(cx, cy, R * 1.04, 0, 7); const og = c.createRadialGradient(cx, cy, R * .2, cx, cy, R * 1.04); og.addColorStop(0, '#fff1ec'); og.addColorStop(1, '#fbd9cf'); c.fillStyle = og; c.fill(); c.strokeStyle = '#c96a55'; c.lineWidth = 2.2; c.stroke();
    // 血管
    CAPS.forEach(q => { const x = cx + q[0] * d, y = cy + q[1] * d; c.beginPath(); c.arc(x, y, Math.max(1.6, d * .075), 0, 7); c.fillStyle = '#0f766e'; c.fill(); c.beginPath(); c.arc(x, y, Math.max(.7, d * .034), 0, 7); c.fillStyle = '#ccfbf1'; c.fill(); });
    // 筋線維
    const nMyo = clamp(Math.round(13 * k * k), 7, 30);
    FIB.forEach((f, i) => {
      const x = cx + f.ux * d, y = cy + f.uy * d;
      blob(c, x, y, rf, f.sh, f.rot);
      const fg = c.createRadialGradient(x - rf * .25, y - rf * .3, rf * .1, x, y, rf * 1.05); fg.addColorStop(0, '#fcc0b3'); fg.addColorStop(1, '#f08f80'); c.fillStyle = fg; c.fill();
      c.strokeStyle = '#b4443a'; c.lineWidth = 1.3; c.stroke();
      c.fillStyle = 'rgba(159,45,38,.42)';
      for (let j = 0; j < nMyo; j++) { const rr = Math.sqrt((j + .5) / nMyo) * rf * .74, an = j * 2.39996 + f.rot; c.beginPath(); c.arc(x + Math.cos(an) * rr, y + Math.sin(an) * rr, Math.max(.8, Rb / 2.56 * .034), 0, 7); c.fill(); }
    });
    // はじめの太さ（点線）
    c.strokeStyle = 'rgba(30,64,175,.55)'; c.lineWidth = 1.3; c.setLineDash([5, 4]); c.beginPath(); c.arc(cx, cy, Rb * 1.04, 0, 7); c.stroke(); c.setLineDash([]);
    // アミノ酸のつぶ（合成＝中へ・分解＝外へ）
    parts.forEach(q => {
      const e = q.inw ? q.p : 1 - q.p, es = e * e * (3 - 2 * e), x = cx + lerp(q.cx, q.fx, es) * d, y = cy + lerp(q.cy, q.fy, es) * d, al = Math.sin(q.p * Math.PI);
      c.beginPath(); c.arc(x, y, 2.3, 0, 7); c.fillStyle = q.inw ? `rgba(13,148,136,${.9 * al})` : `rgba(234,88,12,${.85 * al})`; c.fill();
      c.beginPath(); c.arc(x, y, 4.2, 0, 7); c.fillStyle = q.inw ? `rgba(45,212,191,${.25 * al})` : `rgba(251,146,60,${.22 * al})`; c.fill();
    });
    // 小さな傷み（赤い点）
    const pul = .75 + .25 * Math.sin(fx.time * 6);
    dots.forEach(q => {
      const f = FIB[q.fi], x = cx + f.ux * d + Math.cos(q.an) * q.rr * rf * .82, y = cy + f.uy * d + Math.sin(q.an) * q.rr * rf * .82, grow = Math.min(1, (fx.time - q.born) * 5 + .3);
      c.beginPath(); c.arc(x, y, 5.2 * pul * grow, 0, 7); c.fillStyle = 'rgba(220,38,38,.22)'; c.fill();
      c.beginPath(); c.arc(x, y, 2.5 * grow, 0, 7); c.fillStyle = '#dc2626'; c.fill(); c.strokeStyle = '#7f1d1d'; c.lineWidth = .8; c.stroke();
    });
    // 修復の光
    glints.forEach(q => {
      const f = FIB[q.fi], x = cx + f.ux * d + Math.cos(q.an) * q.rr * rf * .82, y = cy + f.uy * d + Math.sin(q.an) * q.rr * rf * .82, p = q.age / .75;
      c.beginPath(); c.arc(x, y, 3 + 9 * p, 0, 7); c.strokeStyle = `rgba(250,204,21,${.8 * (1 - p)})`; c.lineWidth = 1.6; c.stroke();
      star(c, x, y, 6.5 * Math.sin(Math.min(1, p * 1.6) * Math.PI) + 1); c.fillStyle = `rgba(255,251,235,${1 - p * .6})`; c.fill(); c.strokeStyle = `rgba(245,158,11,${1 - p})`; c.lineWidth = 1; c.stroke();
    });
    c.fillStyle = '#1e40af'; c.font = `${fs * .8}px ${FONT}`; c.textAlign = 'right'; c.textBaseline = 'bottom';
    if (Math.abs(k - 1) > .04) c.fillText('点線＝はじめの太さ', W * .985, W * .132);
    c.fillStyle = '#334155'; c.font = `bold ${fs * .92}px ${FONT}`; c.textAlign = 'center'; c.textBaseline = 'top';
    c.fillText('② 輪切りにしたところ（筋線維の束）', W * .5, W * .705);
    c.font = `${fs * .84}px ${FONT}`; c.fillStyle = '#64748b'; c.fillText('数は19本のまま。1本1本の太さが変わります', W * .5, W * .748);

    // 筋線維1本を横から
    const x0 = W * .05, x1 = W * .95, sy0 = W * .905, hh0 = W * .042, hh = hh0 * k;
    rrect(c, x0, sy0 - hh, x1 - x0, hh * 2, hh * .55);
    const sg = c.createLinearGradient(0, sy0 - hh, 0, sy0 + hh); sg.addColorStop(0, '#fbbcae'); sg.addColorStop(.5, '#f29484'); sg.addColorStop(1, '#e47565'); c.fillStyle = sg; c.fill();
    c.save(); c.clip();
    for (let x = x0 + 4, i = 0; x < x1; x += 5.5, i++) { c.strokeStyle = i % 2 ? 'rgba(127,29,29,.34)' : 'rgba(255,255,255,.28)'; c.lineWidth = i % 2 ? 1.5 : 1; c.beginPath(); c.moveTo(x, sy0 - hh); c.lineTo(x, sy0 + hh); c.stroke(); }
    const nL = Math.max(2, Math.round(hh * 2 / (W * .021)));
    c.strokeStyle = 'rgba(127,29,29,.3)'; c.lineWidth = 1;
    for (let i = 1; i < nL; i++) { const y = sy0 - hh + hh * 2 * i / nL; c.beginPath(); c.moveTo(x0, y); c.lineTo(x1, y); c.stroke(); }
    c.restore();
    rrect(c, x0, sy0 - hh, x1 - x0, hh * 2, hh * .55); c.strokeStyle = '#b4443a'; c.lineWidth = 1.5; c.stroke();
    c.fillStyle = '#6d28d9'; for (let i = 0; i < 5; i++) { const x = x0 + (x1 - x0) * (.12 + i * .19), y = sy0 + (i % 2 ? 1 : -1) * (hh - 2.5); c.beginPath(); c.ellipse(x, y, 6, 2.1, 0, 0, 7); c.globalAlpha = .7; c.fill(); c.globalAlpha = 1; }
    c.strokeStyle = 'rgba(30,64,175,.6)'; c.lineWidth = 1.2; c.setLineDash([5, 4]); rrect(c, x0, sy0 - hh0, x1 - x0, hh0 * 2, hh0 * .55); c.stroke(); c.setLineDash([]);
    dots.forEach(q => {
      const x = x0 + (x1 - x0) * q.sx, y = sy0 + q.sy * hh * .55, grow = Math.min(1, (fx.time - q.born) * 5 + .3);
      c.beginPath(); c.arc(x, y, 5.5 * pul * grow, 0, 7); c.fillStyle = 'rgba(220,38,38,.2)'; c.fill();
      c.strokeStyle = '#dc2626'; c.lineWidth = 2; c.beginPath(); c.moveTo(x - 3 * grow, y - 3.2 * grow); c.lineTo(x + 1.2 * grow, y - 1 * grow); c.lineTo(x - 1.2 * grow, y + 1 * grow); c.lineTo(x + 3 * grow, y + 3.2 * grow); c.stroke();
    });
    glints.forEach(q => {
      const x = x0 + (x1 - x0) * q.sx, y = sy0 + q.sy * hh * .55, p = q.age / .75;
      c.beginPath(); c.arc(x, y, 3 + 9 * p, 0, 7); c.strokeStyle = `rgba(250,204,21,${.8 * (1 - p)})`; c.lineWidth = 1.6; c.stroke();
      star(c, x, y, 6.5 * Math.sin(Math.min(1, p * 1.6) * Math.PI) + 1); c.fillStyle = `rgba(255,251,235,${1 - p * .6})`; c.fill(); c.strokeStyle = `rgba(245,158,11,${1 - p})`; c.lineWidth = 1; c.stroke();
    });
    c.fillStyle = '#334155'; c.font = `bold ${fs * .92}px ${FONT}`; c.textAlign = 'left'; c.textBaseline = 'top';
    c.fillText('③ 筋線維1本を横から', W * .05, W * .808);
    c.font = `${fs * .8}px ${FONT}`; c.fillStyle = '#64748b'; c.textAlign = 'right'; c.fillText('※太さの変化は大きめにえがいています', W * .95, W * .812);
    // 凡例
    const ly = W * 1.012; c.textBaseline = 'middle'; c.textAlign = 'left'; c.font = `${fs * .8}px ${FONT}`;
    let lx = W * .05;
    const leg = (col, txt, kind) => {
      if (kind === 's') { star(c, lx + 4, ly, 5); c.fillStyle = '#fde68a'; c.fill(); c.strokeStyle = '#f59e0b'; c.lineWidth = 1; c.stroke(); } else { c.beginPath(); c.arc(lx + 4, ly, 3, 0, 7); c.fillStyle = col; c.fill(); }
      c.fillStyle = '#475569'; c.fillText(txt, lx + 11, ly + .5); lx += 11 + c.measureText(txt).width + W * .03;
    };
    leg('#dc2626', '小さな傷み'); leg('', '修復', 's'); leg('#0d9488', '合成（材料が入る）'); leg('#ea580c', '分解');
  }

  // ---------- グラフ ----------
  function drawG() {
    const W = size(cG), H = W * 1.05, c = g;
    c.setTransform(dpr, 0, 0, dpr, 0, 0); c.clearRect(0, 0, W, H);
    c.fillStyle = '#f8fafc'; c.fillRect(0, 0, W, H);
    const fs = Math.max(9.5, Math.min(11.5, W * .032)), pad = 6, gap = 5;
    const hs = [.35, .25, .40], avail = H - pad * 2 - gap * 2;
    let y = pad;
    const boxes = hs.map(f => { const b = { x: pad, y, w: W - pad * 2, h: avail * f }; y += avail * f + gap; return b; });
    const head = (b, title, legs) => {
      rrect(c, b.x, b.y, b.w, b.h, 8); c.fillStyle = '#fff'; c.fill(); c.strokeStyle = '#e2e8f0'; c.lineWidth = 1; c.stroke();
      c.fillStyle = '#0f172a'; c.font = `bold ${fs}px ${FONT}`; c.textAlign = 'left'; c.textBaseline = 'middle'; c.fillText(title, b.x + 8, b.y + 12);
      let lx = b.x + b.w - 8; c.font = `${fs * .9}px ${FONT}`; c.textAlign = 'right';
      legs.slice().reverse().forEach(([col, txt, dash]) => { c.fillStyle = '#475569'; c.fillText(txt, lx, b.y + 12.5); lx -= c.measureText(txt).width + 4; c.strokeStyle = col; c.lineWidth = 2.4; c.setLineDash(dash || []); c.beginPath(); c.moveTo(lx - 13, b.y + 12); c.lineTo(lx, b.y + 12); c.stroke(); c.setLineDash([]); lx -= 21; });
      return { x: b.x + 30, y: b.y + 25, w: b.w - 38, h: b.h - 25 - 15 };
    };
    const t1 = Math.max(WIN, t), t0 = t1 - WIN;
    const dayTicks = (p) => {
      c.font = `${fs * .86}px ${FONT}`; c.textAlign = 'center'; c.textBaseline = 'top';
      for (let dd = Math.ceil(t0); dd <= t1; dd++) {
        const x = p.x + (dd - t0) / WIN * p.w; if (dd % 7 === 0) { c.strokeStyle = '#e2e8f0'; c.lineWidth = 1; c.beginPath(); c.moveTo(x, p.y); c.lineTo(x, p.y + p.h); c.stroke(); c.fillStyle = '#64748b'; c.fillText(dd === 0 ? '0日' : dd + '日', x, p.y + p.h + 2); }
      }
      c.fillStyle = '#dc2626';
      trains.forEach(tt => { if (tt < t0 || tt > t1) return; const x = p.x + (tt - t0) / WIN * p.w; c.beginPath(); c.moveTo(x - 3.2, p.y - 5); c.lineTo(x + 3.2, p.y - 5); c.lineTo(x, p.y); c.closePath(); c.fill(); });
    };
    const X = (p, tt) => p.x + (tt - t0) / WIN * p.w;

    // ① 合成と分解
    let p = head(boxes[0], '① 合成と分解', [['#16a34a', '合成'], ['#ea580c', '分解']]);
    const v0 = .8, v1 = 2.3, Y1 = v => p.y + p.h - (clamp(v, v0, v1 + .1) - v0) / (v1 - v0) * p.h;
    dayTicks(p);
    c.save(); c.beginPath(); c.rect(p.x, p.y - 1, p.w, p.h + 2); c.clip();
    for (let i = 1; i < recent.length; i++) {
      const q0 = recent[i - 1], q1 = recent[i], up = (q0[1] + q1[1]) > (q0[2] + q1[2]);
      c.fillStyle = up ? 'rgba(34,197,94,.3)' : 'rgba(249,115,22,.3)'; c.beginPath(); c.moveTo(X(p, q0[0]), Y1(q0[1])); c.lineTo(X(p, q1[0]), Y1(q1[1])); c.lineTo(X(p, q1[0]), Y1(q1[2])); c.lineTo(X(p, q0[0]), Y1(q0[2])); c.closePath(); c.fill();
    }
    c.strokeStyle = '#94a3b8'; c.lineWidth = 1; c.setLineDash([3, 3]); c.beginPath(); c.moveTo(p.x, Y1(1)); c.lineTo(p.x + p.w, Y1(1)); c.stroke(); c.setLineDash([]);
    [[2, '#ea580c'], [1, '#16a34a']].forEach(([ix, col]) => { c.strokeStyle = col; c.lineWidth = 2.2; c.lineJoin = 'round'; c.beginPath(); recent.forEach((q, i) => i ? c.lineTo(X(p, q[0]), Y1(q[ix])) : c.moveTo(X(p, q[0]), Y1(q[ix]))); c.stroke(); });
    c.restore();
    c.fillStyle = '#64748b'; c.font = `${fs * .86}px ${FONT}`; c.textAlign = 'right'; c.textBaseline = 'middle'; c.fillText('ふだん', p.x - 3, Y1(1)); c.fillText('高い', p.x - 3, p.y + 5);
    const net = syn - brk; c.textAlign = 'right'; c.textBaseline = 'top'; c.font = `bold ${fs * .9}px ${FONT}`;
    c.fillStyle = net > .015 ? '#15803d' : net < -.015 ? '#c2410c' : '#64748b';
    c.fillText(net > .015 ? '▲ いま：合成が多い（太くなる）' : net < -.015 ? '▼ いま：分解が多い' : '＝ いま：つり合っている', p.x + p.w - 2, p.y + 7);

    // ② 疲労と回復
    p = head(boxes[1], '② 疲労と回復', [['#fb923c', '疲労'], ['#7c2d12', 'たまった疲労']]);
    const fm = 3, Y2 = v => p.y + p.h - Math.sqrt(clamp(v, 0, fm) / fm) * p.h;
    dayTicks(p);
    c.save(); c.beginPath(); c.rect(p.x, p.y - 1, p.w, p.h + 2); c.clip();
    c.fillStyle = 'rgba(239,68,68,.09)'; c.fillRect(p.x, p.y, p.w, Y2(K.c0) - p.y);
    if (recent.length > 1) {
      c.fillStyle = 'rgba(251,146,60,.4)'; c.beginPath(); c.moveTo(X(p, recent[0][0]), Y2(0)); recent.forEach(q => c.lineTo(X(p, q[0]), Y2(q[3]))); c.lineTo(X(p, recent[recent.length - 1][0]), Y2(0)); c.closePath(); c.fill();
      c.strokeStyle = '#f97316'; c.lineWidth = 1.8; c.beginPath(); recent.forEach((q, i) => i ? c.lineTo(X(p, q[0]), Y2(q[3])) : c.moveTo(X(p, q[0]), Y2(q[3]))); c.stroke();
      c.strokeStyle = '#7c2d12'; c.lineWidth = 2.2; c.beginPath(); recent.forEach((q, i) => i ? c.lineTo(X(p, q[0]), Y2(q[4])) : c.moveTo(X(p, q[0]), Y2(q[4]))); c.stroke();
    }
    c.strokeStyle = '#ef4444'; c.lineWidth = 1; c.setLineDash([3, 3]); c.beginPath(); c.moveTo(p.x, Y2(K.c0)); c.lineTo(p.x + p.w, Y2(K.c0)); c.stroke(); c.setLineDash([]);
    c.restore();
    { const tx = '赤い点線より上が続くと、回復が追いつかない'; c.font = `${fs * .84}px ${FONT}`; const tw = c.measureText(tx).width; rrect(c, p.x + 4, p.y + 1, tw + 10, fs + 4, 5); c.fillStyle = 'rgba(255,255,255,.85)'; c.fill(); c.fillStyle = '#b91c1c'; c.textAlign = 'left'; c.textBaseline = 'middle'; c.fillText(tx, p.x + 9, p.y + 1 + (fs + 4) / 2 + .5); }
    c.fillStyle = '#64748b'; c.font = `${fs * .86}px ${FONT}`; c.textAlign = 'right'; c.textBaseline = 'middle'; c.fillText('0', p.x - 3, Y2(0)); c.fillText('高い', p.x - 3, p.y + 5);

    // ③ 筋肉量の指数
    p = head(boxes[2], '③ 筋肉量の指数', [['#dc2626', '今回'], ['#94a3b8', '前回', [4, 3]]]);
    const tEnd = Math.max(st.weeks * 7, Math.ceil(t / 7) * 7), all = mhist.concat(ghost ? ghost.filter(q => q[0] <= tEnd) : []);
    let lo = 98, hi = 104; all.forEach(q => { lo = Math.min(lo, q[1]); hi = Math.max(hi, q[1]); }); lo = Math.floor(lo - .6); hi = Math.ceil(Math.max(hi, M) + .8);
    const X3 = tt => p.x + tt / tEnd * p.w, Y3 = v => p.y + p.h - (v - lo) / (hi - lo) * p.h;
    const ys = hi - lo > 14 ? 4 : 2; c.font = `${fs * .86}px ${FONT}`; c.textAlign = 'right'; c.textBaseline = 'middle';
    for (let v = Math.ceil(lo / ys) * ys; v <= hi; v += ys) { c.strokeStyle = v === 100 ? '#94a3b8' : '#eef2f7'; c.lineWidth = 1; c.setLineDash(v === 100 ? [3, 3] : []); c.beginPath(); c.moveTo(p.x, Y3(v)); c.lineTo(p.x + p.w, Y3(v)); c.stroke(); c.setLineDash([]); c.fillStyle = '#64748b'; c.fillText(v, p.x - 3, Y3(v)); }
    const ws = tEnd / 7 > 12 ? 4 : tEnd / 7 > 6 ? 2 : 1; c.textAlign = 'center'; c.textBaseline = 'top';
    for (let w = 0; w <= tEnd / 7; w += ws) { const x = X3(w * 7); c.strokeStyle = '#eef2f7'; c.beginPath(); c.moveTo(x, p.y); c.lineTo(x, p.y + p.h); c.stroke(); c.fillStyle = '#64748b'; c.fillText(w + '週', x, p.y + p.h + 2); }
    if (ghost) { c.strokeStyle = '#94a3b8'; c.lineWidth = 1.6; c.setLineDash([4, 3]); c.beginPath(); ghost.forEach((q, i) => { if (q[0] > tEnd) return; i ? c.lineTo(X3(q[0]), Y3(q[1])) : c.moveTo(X3(q[0]), Y3(q[1])); }); c.stroke(); c.setLineDash([]); }
    c.strokeStyle = '#dc2626'; c.lineWidth = 2.6; c.lineJoin = 'round'; c.beginPath(); mhist.forEach((q, i) => i ? c.lineTo(X3(q[0]), Y3(q[1])) : c.moveTo(X3(q[0]), Y3(q[1]))); c.lineTo(X3(t), Y3(M)); c.stroke();
    const ex = X3(t), ey = Y3(M); c.beginPath(); c.arc(ex, ey, 4.2, 0, 7); c.fillStyle = '#dc2626'; c.fill(); c.strokeStyle = '#fff'; c.lineWidth = 1.5; c.stroke();
    c.font = `bold ${fs * 1.05}px ${FONT}`; c.fillStyle = '#b91c1c'; c.textBaseline = 'bottom'; c.textAlign = ex > p.x + p.w - 40 ? 'right' : 'left';
    if (ey < p.y + 16) { c.textBaseline = 'top'; c.fillText(M.toFixed(1), ex + (ex > p.x + p.w - 40 ? -7 : 7), ey + 6); } else c.fillText(M.toFixed(1), ex + (ex > p.x + p.w - 40 ? -7 : 7), ey - 4);
  }

  // ---------- 数字とひとこと ----------
  function status() {
    const wk = st.weeks;
    if (ended) return `⏹ ${wk}週たちました。指数は 100 → ${M.toFixed(1)}。「はじめから」でもう一度、または期間や回数を変えてくらべてみましょう。`;
    if (t - lastTrainT < .2 && lastTrainT >= 0) return lastQ < .6 ? '😵 トレーニングをしましたが、疲れがたまっていて十分な力が出せませんでした。刺激が小さくなっています。' : '💪 トレーニング！ 筋線維に大きな力がかかり、小さな傷み（赤い点）ができました。';
    if (C > K.c0 + .25) return '🥵 疲労がたまったままです。回復が追いつかず、合成の山が小さくなり、伸びが止まっています（やりすぎのモデル）。';
    if (st.freq === 0 && M > 100.4) return '📉 トレーニングの刺激がなくなり、合成の山が出ません。ゆっくり元の太さにもどっていきます。';
    if (st.freq === 0) return '🛋 トレーニングをしていないので、合成と分解はつり合ったまま。筋肉量はほとんど変わりません。';
    if (syn - brk > .05) return '🔧 合成が分解を上回っています。材料（アミノ酸）が筋線維に入り、少しずつ太くなる時間です。';
    if (st.protein === 0 && S > .1) return '🍽 刺激はあるのに、材料のたんぱく質が足りず、合成があまり高まりません。';
    return '😌 合成の山が落ちつき、次のトレーニングを待っています。山と山の間は、分解のほうが少し多くなります。';
  }
  let lastUI = 0;
  function ui(force) {
    const now = performance.now(); if (!force && now - lastUI < 180) return; lastUI = now;
    $('mDay').innerHTML = Math.floor(t + 1e-9) + '<small>日（第' + (Math.floor(Math.max(0, t - 1e-6) / 7) + 1) + '週）</small>';
    $('mIdx').textContent = M.toFixed(1);
    const fp = Math.round(clamp(F / 2, 0, 1) * 100); $('mFat').innerHTML = (C > K.c0 + .25 ? '高い' : fp >= 45 ? 'やや高い' : fp >= 12 ? '少し' : 'ほぼなし');
    $('mFatBox').classList.toggle('warn', C > K.c0 + .25);
    $('ktSay').textContent = status();
  }

  // ---------- 操作 ----------
  function flash(s) { const el = $('ktMsg'); el.textContent = s; el.classList.add('show'); clearTimeout(flash.t); flash.t = setTimeout(() => el.classList.remove('show'), 2200); }
  function updPlay() { $('ktPlay').textContent = playing && !ended ? '⏸ 止める' : '▶ 進める'; document.querySelectorAll('.kt-tools [data-sp]').forEach(b => b.classList.toggle('on', +b.dataset.sp === speed)); }
  function freqText() { const p = DAYS[st.freq]; return st.freq === 0 ? '週0回（しない）' : st.freq === 7 ? '週7回（毎日）' : `週${st.freq}回（${p.map(i => WD[i]).join('・')}）`; }
  function syncUI() {
    $('kFreq').value = st.freq; $('vFreq').textContent = freqText();
    [['ktLoad', 'load'], ['ktProt', 'protein'], ['ktSleep', 'sleep'], ['ktWeeks', 'weeks']].forEach(([id, key]) => document.querySelectorAll('#' + id + ' button').forEach(b => b.classList.toggle('on', +b.dataset.v === st[key])));
    document.querySelectorAll('#ktPre button').forEach(b => b.classList.toggle('on', +b.dataset.p === curPreset));
  }
  function changed() { curPreset = 0; quitAt = null; syncUI(); if (ended && t < st.weeks * 7) { ended = false; playing = true; updPlay(); } ui(true); }
  $('kFreq').addEventListener('input', e => { st.freq = +e.target.value; changed(); });
  [['ktLoad', 'load'], ['ktProt', 'protein'], ['ktSleep', 'sleep'], ['ktWeeks', 'weeks']].forEach(([id, key]) => $(id).addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; st[key] = +b.dataset.v; const cp = curPreset, qa = quitAt; changed(); if (key === 'weeks') { curPreset = cp; quitAt = qa; syncUI(); } }));
  const PRE = { 1: { freq: 3, load: 1, protein: 2, sleep: 2, weeks: 12 }, 2: { freq: 7, load: 2, protein: 1, sleep: 0, weeks: 12 }, 3: { freq: 0, load: 1, protein: 1, sleep: 1, weeks: 12 }, 4: { freq: 3, load: 1, protein: 2, sleep: 2, weeks: 24 } };
  function preset(i) { if (!PRE[i]) return; Object.assign(st, PRE[i]); curPreset = i; reset(true); quitAt = i === 4 ? 56 : null; syncUI(); ui(true); }
  $('ktPre').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; preset(+b.dataset.p); flash(b.textContent.trim() + ' ではじめます'); });
  $('ktPlay').addEventListener('click', () => { if (ended) { flash('期間が終わりました。「はじめから」か、期間をのばしてください'); return; } playing = !playing; updPlay(); });
  document.querySelectorAll('.kt-tools [data-sp]').forEach(b => b.addEventListener('click', () => { speed = +b.dataset.sp; if (!ended) playing = true; updPlay(); }));
  $('ktReset').addEventListener('click', () => { const cp = curPreset; reset(true); quitAt = cp === 4 ? 56 : null; if (cp === 4) { st.freq = 3; syncUI(); } ui(true); flash('はじめからやり直します'); });
  function toEnd() { quiet = true; let m = 0; while (t < st.weeks * 7 - 1e-9 && m < 5000) { stepSim(); m++; } quiet = false; finish(); }
  function finish() { if (!ended && t >= st.weeks * 7 - 1e-9) { ended = true; playing = false; updPlay(); ui(true); } }
  $('ktEnd').addEventListener('click', () => { if (ended) { flash('もう最後まで進んでいます'); return; } toEnd(); flash(st.weeks + '週目まで進めました'); });
  function trainNow() { if (ended) { flash('期間が終わりました。「はじめから」でもう一度'); return; } train(); rates(); ui(true); }
  $('ktNow').addEventListener('click', trainNow); cA.addEventListener('click', trainNow);

  // ---------- シェア ----------
  function shareText() { return `筋トレ${freqText().replace(/（.*/, '')}を${Math.max(1, Math.round(t / 7))}週つづけるモデルで、筋肉量の指数が100→${M.toFixed(1)}になりました💪（仕組みを見るための簡単なモデルです）`; }
  $('shareBtn').addEventListener('click', () => { const u = location.origin + location.pathname; window.open('https://twitter.com/intent/tweet?text=' + encodeURIComponent(shareText() + '\n') + '&url=' + encodeURIComponent(u) + '&hashtags=' + encodeURIComponent('シミュラボ'), '_blank', 'noopener'); });
  $('copyBtn').addEventListener('click', async () => { try { await navigator.clipboard.writeText(shareText() + '\n' + location.origin + location.pathname); flash('コピーしました'); } catch (e) { flash('コピーできませんでした'); } });

  // ---------- 動かす ----------
  function draw() { drawA(); drawG(); ui(false); }
  let tPrev = performance.now(), held = false;
  function loop(now) {
    const dt = Math.min(.1, (now - tPrev) / 1000); tPrev = now;
    if (playing && !ended && !held) { acc += dt * speed; let m = 0; while (acc >= DT && m < 40) { stepSim(); acc -= DT; m++; if (t >= st.weeks * 7 - 1e-9) { finish(); break; } } if (m >= 40) acc = 0; }
    if (!held) tickFx(dt); draw(); requestAnimationFrame(loop);
  }
  reset(false); syncUI(); ui(true);
  requestAnimationFrame(loop);
  // テスト用（裏のタブでは requestAnimationFrame が止まるため）
  window.__t = {
    step(days, loud) { quiet = !loud; const m = Math.round(days * SPD); for (let i = 0; i < m; i++) stepSim(); quiet = false; Msm = M; bal = syn - brk; tickFx(.016); draw(); ui(true); },
    set(o) { ['freq', 'load', 'protein', 'sleep', 'weeks'].forEach(k => { if (o && o[k] != null) st[k] = +o[k]; }); curPreset = 0; quitAt = null; syncUI(); rates(); draw(); ui(true); },
    preset(i) { preset(i); playing = false; updPlay(); draw(); },
    pause() { playing = false; updPlay(); }, play() { if (!ended) playing = true; updPlay(); },
    trainNow, st, fx, hold(v) { held = !!v; }, tick(sec) { for (let i = 0; i < Math.round(sec / .033); i++) tickFx(.033); draw(); },
    get s() { return { day: +t.toFixed(2), index: +M.toFixed(3), fatigue: +F.toFixed(3), chronic: +C.toFixed(3), synth: +syn.toFixed(3), breakdown: +brk.toFixed(3), damage: +dmg.toFixed(3), max: +maxM.toFixed(3), ended, nan: isNaNState() }; }
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
    <p class="kt-note">⚠️ {esc(NOTE)}</p>
    <p class="kt-note" style="border:0;background:#fef2f2">{esc(REQ)}</p>
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
