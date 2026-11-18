# -*- coding: utf-8 -*-
"""ゲームセンターをやめたら貯まるお金（2026-11-18・リクエスト 7255424b65）— sims/gecen-chokin/index.html を書き出す（冪等）。
   使い方: python scripts/gen_gecen_chokin.py   ※フッターリンク込みで書き出す。"""
import html as H, io, json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://shimulabo.com"
SLUG = "gecen-chokin"
NAME = "ゲームセンターをやめたら貯まるお金シミュレーター"
TITLE = "ゲーセンをやめたらいくら貯まる？｜クレーンゲーム・メダル・音ゲーの1年・10年の節約額と時間をシミュレーション｜シミュラボ"
DESC = ("ゲームセンターに行く回数と、クレーンゲーム・メダルゲーム・音楽ゲームなどに使う金額を入れると、やめたとき・半分に減らしたときに"
        "1か月・1年・10年でいくら貯まるかを計算。貯金箱にコインがたまっていくアニメ、積み立てに回した場合、浮く時間、何に使えるかの換算つき。")
OG_T = "ゲーセンをやめたらいくら貯まる？ 1年・10年の節約額シミュレーター"
OG_D = "クレーンゲーム・メダル・音ゲーの金額と回数から、やめた・半分にしたときの貯金額と浮く時間を計算。"

FAQ = [
    ("ゲームセンターをやめると、1年でどれくらい貯まりますか？", "使い方によって大きく変わります。たとえば週1回・1回あたり2,000円（ゲーム代1,500円＋飲み物など500円）なら、1年（52週）で約10万4,000円です。このシミュレーターで、自分の回数と金額を入れて確かめてください。"),
    ("全部やめるのはむずかしいです。減らすだけでも意味はありますか？", "あります。「半分に減らす」「月に◯回までにする」を選ぶと、減らした分だけが貯まる計算になります。楽しみを全部なくすより、回数や1回の予算を決めるほうが続けやすいこともあります。"),
    ("積み立てに回した場合の金額は本当にそうなりますか？", "毎月同じ額を積み立て、年利が一定のまま毎月複利で増えると仮定した計算です。実際の運用では値上がりも値下がりもあり、元本を下回ることもあります。将来の金額を約束するものではありません。"),
    ("換算の金額（映画・ゲームソフトなど）は何の値段ですか？", "わかりやすくするための「例の金額」です。実際の値段はお店や時期によって変わります。"),
    ("入力した金額はどこかに送られますか？", "送られません。計算はすべてこのページの中（お使いの端末）で行っています。"),
]
REL = [("gacha-cost", "🎮", "ソシャゲ課金 生涯コスト計算機"), ("gacha", "🎴", "ガチャ天井シミュレーター")]

ARTICLE = """
<h2>計算のしかた</h2>
<p>1回に行ったときの出費（ゲーム代の合計＋交通費＋飲み物・軽食）に、1か月に行く回数をかけて、1か月の出費を出します。1か月は「1週間の回数×52週÷12か月」で計算しています。</p>
<ul>
<li><b>全部やめる</b>：1か月の出費がまるごと貯まる</li>
<li><b>半分に減らす</b>：行く回数を半分にした分が貯まる</li>
<li><b>月◯回までにする</b>：いまの回数から、その回数をひいた分が貯まる</li>
</ul>
<p>「積み立てに回したら」は、貯まる額を毎月積み立てて、選んだ年利で毎月複利で増えると仮定した金額です（年利0%なら、ただ貯めた額と同じ）。</p>

<h2>ゲームセンターでお金を使いすぎてしまうわけ</h2>
<p>クレーンゲームでは「あと少しで取れそう」と感じると、それまでに使ったお金がもったいなくなって、さらに続けてしまうことがあります。すでに使って取りもどせないお金にひっぱられて判断することを、経済学では<b>サンクコスト（埋没費用）</b>の効果とよびます。メダルゲームのように、お金がメダルやポイントに変わると、使った金額の感覚がうすれることもあります。</p>

<h2>やめる・減らすためのコツ</h2>
<ul>
<li><b>1回の予算を先に決める</b>：その日に使う分だけを持っていく。電子マネーなら上限を決めてチャージする。</li>
<li><b>行く日を決める</b>：「給料日のあとの1回だけ」など、回数を決めておく。</li>
<li><b>貯まったお金の使い道を決める</b>：このページの「何に使える？」で、ほしいものを目標にすると続けやすくなります。</li>
<li><b>かわりの楽しみを用意する</b>：家で遊べるゲームや、友だちと会う別の予定など。</li>
</ul>
"""

REFS = [
    "金融庁「資産運用シミュレーション」（毎月積み立て・複利の計算の考え方）",
    "消費者庁・金融広報中央委員会「知るぽると」家計管理・貯蓄の基礎",
]

STAGE = r"""
<style>
.gc-games{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;margin-bottom:16px;}
.gc-g{min-width:0;border:1.5px solid var(--line);border-radius:14px;padding:10px 10px 8px;background:#fff;cursor:pointer;transition:border-color .15s,background .15s,transform .15s;user-select:none;}
.gc-g.on{border-color:#e11d48;background:#fff1f2;}
.gc-g:hover{transform:translateY(-1px);}
.gc-g .t{display:flex;align-items:center;gap:6px;font-weight:800;font-size:13.5px;}
.gc-g .t .e{font-size:22px;}
.gc-g .t .ck{margin-left:auto;width:18px;height:18px;border-radius:6px;border:1.5px solid #cbd5e1;display:grid;place-items:center;font-size:12px;color:#fff;}
.gc-g.on .t .ck{background:#e11d48;border-color:#e11d48;}
.gc-g .y{display:flex;align-items:center;gap:4px;margin-top:8px;font-size:12px;color:var(--ink-2);}
.gc-g .y input{width:100%;min-width:0;padding:6px 8px;border:1px solid var(--line);border-radius:8px;font:inherit;font-weight:700;font-size:14px;text-align:right;}
.gc-g:not(.on) .y{opacity:.4;}
.gc-seg{display:flex;flex-wrap:wrap;gap:6px;}
.gc-seg button{border:1.5px solid var(--line);background:#fff;border-radius:999px;padding:8px 14px;font:inherit;font-size:13px;font-weight:700;cursor:pointer;}
.gc-seg button.on{background:#e11d48;border-color:#e11d48;color:#fff;}
#gcStageWrap{position:relative;border-radius:16px;overflow:hidden;background:linear-gradient(180deg,#1e1b4b,#312e81);}
#gc{display:block;width:100%;height:380px;}
.gc-play{position:absolute;right:12px;top:48px;border:0;border-radius:999px;background:#facc15;color:#422006;font:inherit;font-weight:900;font-size:14px;padding:11px 22px;cursor:pointer;box-shadow:0 6px 18px rgba(0,0,0,.25);}
.gc-sum{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:14px;}
.gc-sum div{background:#fff1f2;border-radius:12px;padding:10px 6px;text-align:center;}
.gc-sum b{display:block;font-size:20px;color:#be123c;font-variant-numeric:tabular-nums;}
.gc-sum span{font-size:11.5px;color:var(--ink-2);font-weight:700;}
@media (max-width:520px){.gc-sum{grid-template-columns:repeat(2,1fr);} #gc{height:320px;} .gc-games{grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;} .gc-g{padding:8px;} .gc-g .t{font-size:12px;} .gc-g .t .e{font-size:18px;}}
.gc-conv{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px;margin-top:10px;}
.gc-conv div{border:1px solid var(--line);border-radius:12px;padding:10px;text-align:center;background:#fff;}
.gc-conv .e{font-size:26px;}
.gc-conv b{display:block;font-size:18px;color:#0f172a;}
.gc-conv small{color:var(--ink-2);font-size:11px;}
.gc-note{font-size:12px;color:var(--ink-2);margin-top:8px;}
</style>
"""

BODY = r"""
  <section class="panel">
    <h2 style="margin:0 0 6px;font-size:18px;">① 1回行ったときに使う金額</h2>
    <p class="gc-note" style="margin:0 0 12px;">遊ぶものをタップして選び、1回に使う金額を入れてください（金額は例です）。</p>
    <div class="gc-games" id="gcGames"></div>
    <div class="row">
      <div class="field"><label>交通費（往復） <span class="hint">（円）</span></label><input type="number" id="gcTrain" value="0" min="0" step="10" inputmode="numeric"></div>
      <div class="field"><label>飲み物・軽食など <span class="hint">（円）</span></label><input type="number" id="gcFood" value="200" min="0" step="10" inputmode="numeric"></div>
    </div>
    <h2 style="margin:10px 0 10px;font-size:18px;">② 行く回数と、いる時間</h2>
    <div class="field"><div class="gc-seg" id="gcFreq"></div></div>
    <div class="field"><label>1回にいる時間 <span class="hint">（<b id="gcHourV">2</b> 時間）</span></label><input type="range" id="gcHour" min="0.5" max="6" step="0.5" value="2"></div>
    <h2 style="margin:10px 0 10px;font-size:18px;">③ どうする？</h2>
    <div class="field"><div class="gc-seg" id="gcMode"></div></div>
    <div class="field" id="gcCapF" style="display:none"><label>月に何回までにする？ <span class="hint">（<b id="gcCapV">1</b> 回）</span></label><input type="range" id="gcCap" min="0" max="8" step="1" value="1"></div>
    <div class="field"><label>貯まったお金を積み立てに回したら（年利） <span class="hint">（目安）</span></label><div class="gc-seg" id="gcRate"></div></div>
  </section>

  <section class="panel" id="resultPanel">
    <div id="gcStageWrap"><canvas id="gc" aria-label="貯金箱にコインがたまっていくアニメーション"></canvas><button class="gc-play" id="gcPlay" type="button">▶ 10年分ためてみる</button></div>
    <div class="gc-sum"><div><b id="s1">0</b><span>1か月</span></div><div><b id="s12">0</b><span>1年</span></div><div><b id="s60">0</b><span>5年</span></div><div><b id="s120">0</b><span>10年</span></div></div>
    <p class="gc-note" id="gcInv"></p>
    <div class="result" style="margin-top:14px;">
      <div class="label">1年で貯まるお金</div>
      <div class="big"><span id="rBig">0</span><small> 円</small></div>
      <div class="sub" id="rSub">—</div>
    </div>
    <h3 style="margin:18px 0 0;font-size:16px;">1年分で何に使える？ <small style="font-weight:600;color:var(--ink-2);font-size:12px;">（金額は例）</small></h3>
    <div class="gc-conv" id="gcConv"></div>
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
  const yen = n => Math.round(n).toLocaleString();
  const man = n => n >= 10000 ? (n / 10000).toFixed(n >= 1e6 ? 0 : 1).replace(/\.0$/, '') + '万' : yen(n);
  const GAMES = [['crane', '🧸', 'クレーンゲーム', 1000, 1], ['medal', '🪙', 'メダルゲーム', 1000, 0], ['ongei', '🥁', '音楽ゲーム', 500, 1],
                 ['video', '🕹️', '格闘・ビデオゲーム', 300, 0], ['purikura', '📸', 'プリントシール', 500, 0], ['other', '🎳', 'その他', 500, 0]];
  const FREQ = [['月1回', 12 / 52], ['月2回', 24 / 52], ['週1回', 1], ['週2回', 2], ['週3回', 3], ['ほぼ毎日（週5）', 5]];
  const MODES = [['all', '全部やめる'], ['half', '半分に減らす'], ['cap', '月◯回までにする']];
  const RATES = [0, 1, 3, 5];
  const CONV = [['🎬', '映画', 2000], ['🍜', 'ラーメン', 1000], ['🎮', 'ゲームソフト', 7000], ['👟', 'スニーカー', 12000], ['🚄', '国内1泊旅行', 30000]];
  const st = { on: {}, val: {}, freq: 2, mode: 'all', rate: 0 };
  GAMES.forEach(g => { st.on[g[0]] = !!g[4]; st.val[g[0]] = g[3]; });
  // UI
  $('gcGames').innerHTML = GAMES.map(g => `<div class="gc-g${g[4] ? ' on' : ''}" data-k="${g[0]}"><div class="t"><span class="e">${g[1]}</span>${g[2]}<span class="ck">✓</span></div><div class="y"><input type="number" min="0" step="100" value="${g[3]}" inputmode="numeric" aria-label="${g[2]}の金額">円</div></div>`).join('');
  $('gcGames').querySelectorAll('.gc-g').forEach(el => {
    const k = el.dataset.k, inp = el.querySelector('input');
    el.addEventListener('click', e => { if (e.target === inp) return; st.on[k] = !st.on[k]; el.classList.toggle('on', st.on[k]); calc(); });
    inp.addEventListener('focus', () => { if (!st.on[k]) { st.on[k] = true; el.classList.add('on'); } });
    inp.addEventListener('input', () => { st.val[k] = Math.max(0, +inp.value || 0); calc(); });
  });
  function seg(id, items, cur, cb) { const box = $(id); box.innerHTML = items.map((it, i) => `<button type="button" data-i="${i}" class="${i === cur ? 'on' : ''}">${it}</button>`).join('');
    box.querySelectorAll('button').forEach(b => b.addEventListener('click', () => { box.querySelectorAll('button').forEach(x => x.classList.remove('on')); b.classList.add('on'); cb(+b.dataset.i); calc(); })); }
  seg('gcFreq', FREQ.map(f => f[0]), st.freq, i => st.freq = i);
  seg('gcMode', MODES.map(m => m[1]), 0, i => { st.mode = MODES[i][0]; $('gcCapF').style.display = st.mode === 'cap' ? '' : 'none'; });
  seg('gcRate', RATES.map(r => r ? '年' + r + '%' : '積み立てない（0%）'), 0, i => st.rate = RATES[i]);
  ['gcTrain', 'gcFood', 'gcHour', 'gcCap'].forEach(id => $(id).addEventListener('input', calc));
  let R = null;
  function fv(m, months, r) { if (!r) return m * months; const i = r / 100 / 12; return m * ((Math.pow(1 + i, months) - 1) / i); }
  function calc() {
    const game = GAMES.reduce((a, g) => a + (st.on[g[0]] ? st.val[g[0]] : 0), 0);
    const per = game + Math.max(0, +$('gcTrain').value || 0) + Math.max(0, +$('gcFood').value || 0);
    const perWeek = FREQ[st.freq][1], visitsM = perWeek * 52 / 12, hour = +$('gcHour').value; $('gcHourV').textContent = hour;
    const cap = +$('gcCap').value; $('gcCapV').textContent = cap;
    const cut = st.mode === 'all' ? visitsM : st.mode === 'half' ? visitsM / 2 : Math.max(0, visitsM - cap);
    const save = per * cut, hoursY = hour * cut * 12;
    R = { per, game, visitsM, cut, save, hoursY, rate: st.rate };
    [1, 12, 60, 120].forEach(m => $('s' + m).textContent = man(fv(save, m, 0)) + '円');
    $('gcInv').innerHTML = st.rate ? `年${st.rate}%で積み立てに回すと、10年で <b>${yen(fv(save, 120, st.rate))}円</b>（うち増えた分 ${yen(fv(save, 120, st.rate) - save * 120)}円）。※一定の年利で毎月複利と仮定した目安で、実際の運用では元本を下回ることもあります。` : '「積み立てに回したら」を選ぶと、10年後の目安も出ます。';
    $('rBig').textContent = yen(save * 12);
    $('rSub').textContent = save > 0 ? `1回 ${yen(per)}円 × 月${cut.toFixed(cut < 10 ? 1 : 0).replace(/\.0$/, '')}回 減らす ＝ 月${yen(save)}円。浮く時間は1年で約${Math.round(hoursY)}時間（${(hoursY / 24).toFixed(1)}日分）` : (cut === 0 ? '減らす回数が0回です（いまの回数より多い上限になっています）' : '遊ぶものを選ぶか、金額を入れてください');
    $('gcConv').innerHTML = CONV.map(c => `<div><div class="e">${c[0]}</div><b>${Math.floor(save * 12 / c[2])}${c[1] === '国内1泊旅行' ? '回' : c[1] === '映画' ? '回' : c[1] === 'ラーメン' ? '杯' : c[1] === 'ゲームソフト' ? '本' : '足'}</b><small>${c[1]}（${yen(c[2])}円として）</small></div>`).join('');
    if (!playing) { month = 120; }
  }
  // アニメ：貯金箱にコインがたまる
  const cv = $('gc'), x = cv.getContext('2d'); let W = 0, Hh = 0, dpr = 1, month = 0, playing = false, t0 = 0, coins = [], last = 0, popups = [];
  const F = '"Hiragino Sans","Noto Sans JP","Yu Gothic",Meiryo,sans-serif';
  function size() { dpr = Math.min(2, window.devicePixelRatio || 1); W = cv.clientWidth; Hh = cv.clientHeight; cv.width = W * dpr; cv.height = Hh * dpr; x.setTransform(dpr, 0, 0, dpr, 0, 0); }
  function rr(X, Y, w, h, r) { x.beginPath(); x.roundRect ? x.roundRect(X, Y, w, h, r) : x.rect(X, Y, w, h); }
  function txt(s, X, Y, sz, c, al, w) { x.font = (w || 800) + ' ' + sz + 'px ' + F; x.fillStyle = c; x.textAlign = al || 'left'; x.fillText(s, X, Y); x.textAlign = 'left'; }
  function play() { if (!R || R.save <= 0) return; playing = true; month = 0; t0 = performance.now(); coins = []; popups = []; last = 0; $('gcPlay').textContent = '⏸ ためている…'; }
  $('gcPlay').addEventListener('click', () => { if (playing) { playing = false; $('gcPlay').textContent = '▶ もう一度ためる'; } else play(); });
  function frame(now) {
    const t = now / 1000;
    if (playing) { month = Math.min(120, (now - t0) / 1000 * 15); if (month >= 120) { playing = false; $('gcPlay').textContent = '▶ もう一度ためる'; }
      if (Math.floor(month) > last) { for (let k = last; k < Math.floor(month); k++) coins.push({ x: (Math.random() - .5) * 60, y: -20, vy: 0, r: 7 + Math.random() * 3 });
        const prev = fv(R.save, last, 0), cur = fv(R.save, Math.floor(month), 0); CONV.forEach(c => { if (prev < c[2] && cur >= c[2]) { popups = [{ s: c[0] + ' ' + c[1] + 'に届いた！', t: now }]; } });
        last = Math.floor(month); } }
    // 背景
    x.clearRect(0, 0, W, Hh);
    for (let i = 0; i < 40; i++) { const sx = (i * 97.3 % W), sy = (i * 53.7 % (Hh * .7)); x.fillStyle = `rgba(255,255,255,${.15 + .15 * Math.sin(t * 2 + i)})`; x.fillRect(sx, sy, 2, 2); }
    // ネオン看板
    const ng = .7 + .3 * Math.sin(t * 4); txt('GAME', 18, 34, 20, `rgba(244,114,182,${ng})`, 'left', 900); txt('→ ちょきん', 84, 34, 16, 'rgba(250,204,21,.9)', 'left', 900);
    const s = R ? R.save : 0, total = fv(s, month, 0), inv = R && R.rate ? fv(s, month, R.rate) : total, max = Math.max(1, R && R.rate ? fv(s, 120, R.rate) : fv(s, 120, 0));
    // 貯金箱（びん）
    const jw = Math.min(W * .42, 240), jh = Hh * .62, jx = W * .5 - jw / 2, jy = Hh * .2;
    rr(jx, jy, jw, jh, 22); x.fillStyle = 'rgba(255,255,255,.08)'; x.fill(); x.strokeStyle = 'rgba(255,255,255,.55)'; x.lineWidth = 2.5; x.stroke();
    rr(jx + jw * .3, jy - 12, jw * .4, 14, 6); x.fillStyle = 'rgba(255,255,255,.35)'; x.fill();
    // 中身の高さ
    const fh = (jh - 8) * Math.min(1, total / max), fh2 = (jh - 8) * Math.min(1, inv / max);
    if (fh2 > fh) { x.fillStyle = 'rgba(52,211,153,.35)'; rr(jx + 4, jy + jh - 4 - fh2, jw - 8, fh2, 16); x.fill(); }
    const gg = x.createLinearGradient(0, jy + jh - fh, 0, jy + jh); gg.addColorStop(0, '#fde047'); gg.addColorStop(1, '#ca8a04');
    x.save(); rr(jx + 4, jy + 4, jw - 8, jh - 8, 18); x.clip(); x.fillStyle = gg; x.fillRect(jx + 4, jy + jh - 4 - fh, jw - 8, fh);
    for (let i = 0; i < 30 && fh > 10; i++) { const cx = jx + 10 + (i * 37 % (jw - 20)), cy = jy + jh - 4 - fh + 6 + (i * 13 % Math.max(6, fh - 8)); x.fillStyle = 'rgba(254,240,138,.75)'; x.beginPath(); x.ellipse(cx, cy, 8, 3.5, 0, 0, 7); x.fill(); }
    x.restore();
    // 落ちてくるコイン
    coins.forEach(c => { c.vy += .5; c.y += c.vy; });
    coins = coins.filter(c => jy - 30 + c.y < jy + jh - fh - 6);
    coins.forEach(c => { const cx = W / 2 + c.x * jw / 120, cy = jy - 30 + c.y; x.fillStyle = '#facc15'; x.beginPath(); x.arc(cx, cy, c.r, 0, 7); x.fill(); x.strokeStyle = '#a16207'; x.lineWidth = 1.5; x.stroke(); txt('¥', cx, cy + 4, c.r * 1.2, '#a16207', 'center', 900); });
    // 数字
    const yrs = Math.floor(month / 12), mo = Math.floor(month % 12);
    txt(month >= 120 ? '10年' : (yrs ? yrs + '年' : '') + mo + 'か月', W - 16, 34, 16, '#e0e7ff', 'right', 800);
    txt(yen(total) + '円', W / 2, jy + jh + 30, Math.min(30, W / 14), '#fff', 'center', 900);
    if (R && R.rate && inv > total) txt('積み立てなら ' + yen(inv) + '円', W / 2, jy + jh + 52, 13, '#6ee7b7', 'center', 800);
    if (!R || s <= 0) txt('遊ぶものと金額を入れてください', W / 2, Hh / 2, 15, '#e0e7ff', 'center', 700);
    // 到達ポップ
    popups = popups.filter(p => now - p.t < 2200); popups.forEach((p, i) => { const a = 1 - (now - p.t) / 2200; x.globalAlpha = a; x.font = '800 12px ' + F; const pw = x.measureText(p.s).width + 24, py = jy + jh * .4; rr(W / 2 - pw / 2, py, pw, 24, 12); x.fillStyle = 'rgba(250,204,21,.95)'; x.fill(); txt(p.s, W / 2, py + 17, 12, '#422006', 'center', 800); x.globalAlpha = 1; });
    requestAnimationFrame(frame);
  }
  window.addEventListener('resize', size); size(); calc(); requestAnimationFrame(frame);
  function shareText() { return R && R.save > 0 ? `ゲーセンを${st.mode === 'all' ? 'やめたら' : st.mode === 'half' ? '半分にしたら' : '減らしたら'}、1年で${yen(R.save * 12)}円・10年で${man(R.save * 120)}円貯まる計算でした🪙 浮く時間は1年で約${Math.round(R.hoursY)}時間。` : 'ゲーセンをやめたらいくら貯まる？シミュレーター'; }
  $('shareBtn').addEventListener('click', () => window.open('https://twitter.com/intent/tweet?text=' + encodeURIComponent(shareText()) + '&url=' + encodeURIComponent(location.href) + '&hashtags=' + encodeURIComponent('シミュラボ'), '_blank', 'noopener'));
  $('copyBtn').addEventListener('click', async () => { try { await navigator.clipboard.writeText(shareText() + '\n' + location.href); $('copyBtn').textContent = 'コピーしました ✓'; setTimeout(() => $('copyBtn').textContent = '結果をコピー', 1600); } catch { alert(shareText()); } });
  window.__gc = { get R() { return R; }, play, fv };
})();
"""


def esc(s): return H.escape(s, quote=True)


def build():
    url = f"{BASE}/sims/{SLUG}/"
    ld_app = {"@context": "https://schema.org", "@type": "WebApplication", "name": NAME, "url": url, "description": DESC,
              "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "inLanguage": "ja", "isAccessibleForFree": True,
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

  <nav class="breadcrumb" aria-label="breadcrumb"><a href="../../">ホーム</a><span>›</span>お金・時間<span>›</span><span class="cur">{esc(NAME)}</span></nav>

  <div class="sim-head">
    <div class="cat">お金・時間</div>
    <h1>ゲーセンをやめたらいくら貯まる？シミュレーター</h1>
    <p class="lead">クレーンゲーム・メダルゲーム・音楽ゲームなど、ゲームセンターで1回に使う金額と、行く回数を入れてください。全部やめたとき・半分に減らしたときに、1か月・1年・10年でいくら貯まるか、どれだけ時間が浮くかを計算します。「▶ 10年分ためてみる」で、貯金箱にコインがたまっていく様子も見られます。</p>
    <p class="gc-note">💌 このシミュレーターは、そうめんさんのリクエストから作りました。</p>
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
