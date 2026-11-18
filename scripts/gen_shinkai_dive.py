# -*- coding: utf-8 -*-
"""深海へもぐるスクロール（2026-11-18）— sims/shinkai-dive/index.html を書き出す（冪等）。
   スクロールすると水深0m→マリアナ海溝の底（約10,920m）までもぐり、光・水圧・水温・生き物・高さ比べが出る。
   使い方: python scripts/gen_shinkai_dive.py
   ※ 書き出し後のフッターリンク（運営者情報ほか）はこのスクリプトが自分で入れる（add_footer_links.py 不要）。"""
import html as H, io, json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://shimulabo.com"
SLUG = "shinkai-dive"
NAME = "深海へもぐるシミュレーター"
TITLE = "深海へもぐるシミュレーター｜スクロールで水深0mからマリアナ海溝1万mへ。光・水圧・水温と深海の生き物｜シミュラボ"
DESC = ("画面をスクロールすると、海の表面から世界一深いマリアナ海溝の底（約10,920m）まで、もぐっていけるシミュレーター。"
        "深さごとに光の量・水圧・水温が変わり、ダイオウイカやチョウチンアンコウ、8,336mで撮影された魚まで、深海の生き物が現れる。"
        "スカイツリー・富士山・エベレストを沈めた高さ比べつき。")
OG_T = "深海へもぐるシミュレーター｜スクロールでマリアナ海溝の底まで"
OG_D = "スクロールするほど暗く、重くなる海。200mで光は1%、1万mで指先に約1トン。そこにも生き物がいる。"

FAQ = [
    ("海の深さは平均どれくらいですか？", "海の平均の深さは約3,700mです。いちばん深いのは太平洋のマリアナ海溝にあるチャレンジャー海淵で、約10,920mあります（測り方によって数十mの差があります）。富士山（3,776m）を沈めると平均の深さとほぼ同じ、エベレスト（8,849m）を沈めても、てっぺんの上にまだ2,000m以上の水があります。"),
    ("太陽の光はどこまで届きますか？", "きれいな海でも、水深200mで水面の約1%まで弱くなります。ここまでを「有光層」とよび、植物プランクトンが光合成できるのはおおよそこの深さまでです。水深1,000mより深いところには、太陽の光はほとんど届きません。"),
    ("深海の水圧はどれくらいですか？", "水深が10m深くなるごとに、約1気圧ずつ増えます。水面の大気圧1気圧を合わせると、水深1,000mで約101気圧、マリアナ海溝の底では約1,100気圧になり、指先（1cm²）に約1.1トンの重さがかかるのと同じです。"),
    ("いちばん深いところにすむ魚は？", "2022年、伊豆・小笠原海溝の水深8,336mで、シンカイクサウオのなかまが撮影されました。これまでに撮影された中で最も深いところにいた魚の記録です。8,200mより深いところでは、体のつくりの限界から魚はすめないと考えられています。それより深い海の底には、ヨコエビのなかまなどがすんでいます。"),
    ("人はどこまでもぐれますか？", "空気のボンベを使うスキューバダイビングの世界記録は332m（2014年）、息を止めてもぐる素潜りの記録は214m（2007年）です。それより深くは、潜水艇に乗って行きます。日本の「しんかい6500」は6,500mまで、1960年には潜水艇トリエステ号がマリアナ海溝の底に到達しました。"),
]
REL = [("shinkai-suiatsu-3d", "🌌", "深海の水圧 3Dシミュレーター"), ("takasa-kurabe-3d", "🗼", "高さ比べ 3D"), ("suiatsu-fuyuu", "💧", "水圧と浮力のシミュレーター"),
       ("kaibatsu-check", "⛰️", "うちの海抜チェッカー"), ("tsunami-kishi", "🌊", "津波はなぜ岸で高くなる？")]

ARTICLE = """
<h2>深くなるほど、何が変わる？</h2>
<p>海は、深さによって<b>光・水圧・水温</b>が大きく変わります。このシミュレーターでは、画面をスクロールするたびに数メートルずつもぐり、そのときの値を左上に表示しています。</p>
<div class="tbl-scroll"><table class="seo-table">
<tr><th>層（深さ）</th><th>光</th><th>水圧（目安）</th><th>水温（太平洋の例）</th><th>主な生き物</th></tr>
<tr><td>表層（0〜200m）</td><td>水面の100%→約1%</td><td>1〜21気圧</td><td>25℃前後→15℃ほど</td><td>植物プランクトン・ウミガメ・サンゴ礁の魚</td></tr>
<tr><td>中深層（200〜1,000m）</td><td>うす暗い→ほぼ届かない</td><td>21〜101気圧</td><td>15℃→4〜5℃</td><td>リュウグウノツカイ・メンダコ・ダイオウイカ</td></tr>
<tr><td>漸深層（1,000〜4,000m）</td><td>まっ暗</td><td>101〜401気圧</td><td>4℃→2℃ほど</td><td>チョウチンアンコウ・ホウライエソ・マッコウクジラ（狩り）</td></tr>
<tr><td>深海層（4,000〜6,000m）</td><td>まっ暗</td><td>401〜601気圧</td><td>1〜2℃</td><td>オニキンメ・ナマコのなかま</td></tr>
<tr><td>超深海層（6,000m〜）</td><td>まっ暗</td><td>601〜約1,100気圧</td><td>1〜2℃台</td><td>シンカイクサウオのなかま・ヨコエビのなかま</td></tr>
</table></div>
<p>深海の生き物の多くは、自分で光を出す<b>生物発光</b>のしくみをもっています。光の届かない世界で、えさをおびき寄せたり、仲間を見つけたり、敵から身を隠したりするために使われています。</p>

<h2>水圧は「10mで1気圧」</h2>
<p>水の重さによる圧力（水圧）は、深さに比例して大きくなり、海水では10m深くなるごとに約1気圧ずつ増えます。左上の「指先にかかる重さ」は、指先の面積を1cm²として、そこにかかる力を重さ（kg）で表したものです。左上の風船は、中の空気が水圧で押し縮められる大きさ（体積が気圧に反比例する＝ボイルの法則）を表しています。深海の生き物は、体の中に空気のすき間がほとんどなく、まわりと同じ圧力で体の中も押しているため、つぶれずにくらせます。</p>

<h2>このシミュレーターの数値について</h2>
<p>水圧は「1気圧（水面の大気圧）＋深さ÷10」、光は水面を100%として水深200mで約1%になるように減らした目安、水温は熱帯〜温帯の太平洋の例です。海域や季節によって大きく変わります。生き物の深さは、すんでいる深さのはんいの中の一例で、図の生き物の大きさは実際の比率ではありません。</p>
"""

REFS = [
    "国立研究開発法人 海洋研究開発機構（JAMSTEC）「深海とは」「しんかい6500」",
    "Jamieson AJ ほか（2023年発表）伊豆・小笠原海溝 水深8,336mでのシンカイクサウオ類の撮影（西オーストラリア大学・東京海洋大学）",
    "Quick NJ ほか (2020). Extreme diving in mammals: first estimates of behavioural aerobic dive limits in Cuvier's beaked whales. <i>Journal of Experimental Biology</i>.",
    "国立科学博物館 窪寺恒己ほか：ダイオウイカの深海での撮影（小笠原諸島沖）",
    "NOAA Ocean Exploration「How deep is the ocean?」",
]

STAGE = r"""
<style>
.dv-intro{text-align:center;}
.dv-intro .btns{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:12px;}
#dive{position:relative;margin:18px 0 0;border-radius:16px;}
#dvStage{position:sticky;top:0;height:100vh;height:100svh;border-radius:16px;overflow:hidden;background:#38bdf8;}
#dv{width:100%;height:100%;display:block;}
.dv-ctl{position:absolute;right:12px;bottom:12px;display:flex;gap:8px;z-index:2;}
.dv-ctl button{border:1px solid rgba(255,255,255,.35);background:rgba(15,23,42,.55);color:#fff;border-radius:999px;padding:9px 14px;font:inherit;font-size:13px;font-weight:800;cursor:pointer;backdrop-filter:blur(4px);}
.dv-ctl button:hover{background:rgba(15,23,42,.8);}
.dv-end{margin-top:18px;}
</style>
"""

JS = r"""
(() => {
  const $ = id => document.getElementById(id);
  const cv = $('dv'), stage = $('dvStage'), dive = $('dive');
  const x = cv.getContext('2d');
  const F = '"Hiragino Sans","Noto Sans JP","Yu Gothic",Meiryo,sans-serif';
  const MAXD = 10920;
  // スクロールの進み(0〜1) ↔ 深さ（浅いところほどゆっくり）
  const KP = [[0, 0], [0.16, 200], [0.38, 1000], [0.6, 4000], [0.74, 6000], [1, MAXD]];
  function p2d(p) { for (let i = 1; i < KP.length; i++) if (p <= KP[i][0]) { const [p0, d0] = KP[i - 1], [p1, d1] = KP[i]; return d0 + (d1 - d0) * (p - p0) / (p1 - p0); } return MAXD; }
  function d2p(d) { for (let i = 1; i < KP.length; i++) if (d <= KP[i][1]) { const [p0, d0] = KP[i - 1], [p1, d1] = KP[i]; return p0 + (p1 - p0) * (d - d0) / (d1 - d0); } return 1; }
  const lerp = (a, b, t) => a + (b - a) * t, clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  function interp(tab, d) { for (let i = 1; i < tab.length; i++) if (d <= tab[i][0]) { const t = (d - tab[i - 1][0]) / (tab[i][0] - tab[i - 1][0]); return lerp(tab[i - 1][1], tab[i][1], t); } return tab[tab.length - 1][1]; }
  const TEMP = [[0, 25], [100, 22], [200, 15], [500, 8], [1000, 4.5], [2000, 2.5], [4000, 1.5], [6000, 1.4], [8000, 1.8], [MAXD, 2.4]];
  const COL = [[0, [56, 189, 248]], [60, [14, 165, 233]], [200, [3, 105, 161]], [500, [8, 47, 92]], [1000, [8, 22, 48]], [3000, [3, 9, 22]], [MAXD, [1, 3, 8]]];
  function colAt(d) { for (let i = 1; i < COL.length; i++) if (d <= COL[i][0]) { const t = (d - COL[i - 1][0]) / (COL[i][0] - COL[i - 1][0]); return COL[i - 1][1].map((v, k) => Math.round(lerp(v, COL[i][1][k], t))); } return COL[COL.length - 1][1]; }
  const ZONES = [[0, 200, '表層（有光層）'], [200, 1000, '中深層（トワイライトゾーン）'], [1000, 4000, '漸深層'], [4000, 6000, '深海層'], [6000, MAXD + 1, '超深海層']];
  // 生き物： [深さ, 絵文字, 名前, ひとこと, 光る？]
  const LIFE = [
    [6, '🐢', 'ウミガメ', '光がたっぷり届く明るい海', 0], [18, '🐠', 'サンゴ礁の魚', 'サンゴは光合成をする藻と共生している', 0],
    [90, '🐬', 'ハンドウイルカ', '300mほどまでもぐることがある', 0], [250, '🦀', 'タカアシガニ', '日本近海の水深200〜300mほどの海底', 0],
    [380, '🐟', 'リュウグウノツカイ', '200〜1,000mの中層をただよう長い魚', 0], [520, '🐙', 'メンダコ', '日本近海の200〜1,000mの海底近く', 0],
    [650, '🦑', 'ダイオウイカ', '小笠原沖の水深600〜900mで撮影された記録がある', 0], [760, '🦑', 'コウモリダコ', '酸素の少ない600〜900mにすむ', 1],
    [850, '🦈', 'ラブカ', '500〜1,000m。「生きた化石」とよばれるサメ', 0], [950, '🦐', 'ダイオウグソクムシ', '200〜2,000mの海底で死がいなどを食べる', 0],
    [1150, '🐡', 'チョウチンアンコウのなかま', '光る「ちょうちん」でえさをおびき寄せる', 1], [1600, '🐟', 'ホウライエソ', '体の光る点で仲間や獲物を見分ける', 1],
    [2000, '🐋', 'マッコウクジラ', '1,000〜2,000mほどまでもぐってイカを食べる', 0], [2500, '🪸', 'チューブワーム', '熱水が噴き出す場所のまわりに群れる', 0],
    [2992, '🐋', 'アカボウクジラ', '哺乳類の潜水記録 2,992m（2020年報告）', 0], [4600, '🐟', 'オニキンメ', '大きな牙をもつ。5,000mほどまですむ', 1],
    [5200, '🥒', 'ナマコのなかま', '深海の海底でいちばん多い動物の一つ', 1], [8336, '🐟', 'シンカイクサウオのなかま', '2022年、伊豆・小笠原海溝で撮影。最も深い魚の記録', 0],
    [10300, '🦐', 'ヨコエビのなかま', '1万mをこえる海の底にもすんでいる', 0],
  ];
  // 目じるし： [深さ, ラベル, 種類]
  const MARK = [
    [40, 'レジャーのスキューバダイビングの目安（約40m）', 'h'], [200, 'ここで光は水面の約1%（有光層の終わり）', 'z'], [214, '素潜りの世界記録 214m（2007年）', 'h'],
    [332, 'スキューバダイビングの世界記録 332m（2014年）', 'h'], [634, '東京スカイツリー（634m）を沈めると、てっぺんはここ', 'm'],
    [1000, '太陽の光は、ここより下にはほとんど届かない', 'z'], [3700, '海の平均の深さ（約3,700m）', 'z'], [3776, '富士山（3,776m）を沈めると、山頂はここ', 'm'],
    [3800, 'タイタニック号がしずんでいる深さ（約3,800m）', 'h'], [6500, '「しんかい6500」がもぐれる深さ（6,500m）', 'h'],
    [8849, 'エベレスト（8,849m）を沈めても、山頂の上にまだ2,000m以上の海', 'm'],
  ];
  let HT = 0, W = 0, Hh = 0, dpr = 1, SH = 0, depth = 0, maxDepth = 0, auto = null, t0 = performance.now();
  const SNOW = Array.from({ length: 140 }, () => ({ x: Math.random(), y: Math.random(), r: .6 + Math.random() * 1.8, s: .2 + Math.random() * .8 }));
  const BUB = Array.from({ length: 26 }, () => ({ x: Math.random(), y: Math.random(), r: 2 + Math.random() * 5, s: .3 + Math.random() }));
  function size() {
    const hd = document.querySelector('.site-header'), hh = hd ? hd.offsetHeight : 0;
    stage.style.top = hh + 'px'; stage.style.height = (window.innerHeight - hh) + 'px';
    dpr = Math.min(2, window.devicePixelRatio || 1); W = stage.clientWidth; Hh = stage.clientHeight; HT = hh;
    cv.width = W * dpr; cv.height = Hh * dpr; x.setTransform(dpr, 0, 0, dpr, 0, 0);
    SH = Math.round(Math.max(9000, Hh * 13)); dive.style.height = SH + 'px';
  }
  function prog() { const r = dive.getBoundingClientRect(); return clamp((HT - r.top) / (SH - Hh), 0, 1); }
  function yOf(d) { return Hh * .5 + (d2p(d) - d2p(depth)) * (SH - Hh); }
  function txt(s, X, Y, size, c, al, w) { x.font = (w || 800) + ' ' + size + 'px ' + F; x.fillStyle = c; x.textAlign = al || 'left'; x.fillText(s, X, Y); x.textAlign = 'left'; }
  function wrap(s, mw, size, w) { x.font = (w || 800) + ' ' + size + 'px ' + F; const out = []; let cur = '';
    for (const ch of s) { if (x.measureText(cur + ch).width > mw && cur) { out.push(cur); cur = ch; } else cur += ch; } if (cur) out.push(cur); return out; }
  function rr(X, Y, w, h, r) { x.beginPath(); x.roundRect ? x.roundRect(X, Y, w, h, r) : x.rect(X, Y, w, h); }
  function fmt(n) { return Math.round(n).toLocaleString(); }
  function frame(now) {
    const t = (now - t0) / 1000;
    depth = p2d(prog()); if (depth > maxDepth) maxDepth = depth;
    const c = colAt(depth), light = depth >= 1000 ? 0 : 100 * Math.exp(-depth / 43.4);
    // 背景（上下で少しずつ色を変える）
    const g = x.createLinearGradient(0, 0, 0, Hh); const ct = colAt(Math.max(0, depth - 120)), cb = colAt(depth + 160);
    g.addColorStop(0, `rgb(${ct})`); g.addColorStop(1, `rgb(${cb})`); x.fillStyle = g; x.fillRect(0, 0, W, Hh);
    // 水面と光の帯
    const sy = yOf(0);
    if (sy > -10) { x.fillStyle = '#e0f2fe'; x.fillRect(0, 0, W, Math.max(0, sy)); txt('☀️ 海面', 18, Math.max(26, sy - 12), 16, '#0c4a6e'); x.fillStyle = 'rgba(255,255,255,.7)'; x.fillRect(0, sy, W, 3); }
    const ra = clamp(1 - depth / 220, 0, 1);
    if (ra > 0) { for (let k = 0; k < 6; k++) { const bx = (k / 6 + .08 * Math.sin(t * .3 + k)) * W; const gr = x.createLinearGradient(0, sy, 0, Hh); gr.addColorStop(0, `rgba(255,255,255,${.22 * ra})`); gr.addColorStop(1, 'rgba(255,255,255,0)');
      x.fillStyle = gr; x.beginPath(); x.moveTo(bx, Math.max(0, sy)); x.lineTo(bx + 40, Math.max(0, sy)); x.lineTo(bx + 140 + k * 10, Hh); x.lineTo(bx + 60, Hh); x.closePath(); x.fill(); } }
    // 泡（浅いところ）とマリンスノー（深いところ）— スクロールと一緒に流れる
    const scrollPx = d2p(depth) * (SH - Hh);
    if (depth < 60) BUB.forEach(b => { const y = ((b.y * Hh - t * 40 * b.s + scrollPx * .5) % Hh + Hh) % Hh; x.strokeStyle = `rgba(255,255,255,${.5 * (1 - depth / 60)})`; x.lineWidth = 1.2; x.beginPath(); x.arc(b.x * W + Math.sin(t + b.y * 9) * 6, y, b.r, 0, 7); x.stroke(); });
    const sa = clamp((depth - 60) / 400, 0, 1) * .8;
    if (sa > 0) SNOW.forEach(s => { const y = ((s.y * Hh - scrollPx * s.s * .6 + t * 6 * s.s) % Hh + Hh) % Hh; x.fillStyle = `rgba(226,232,240,${sa * (.35 + s.s * .4)})`; x.beginPath(); x.arc(s.x * W + Math.sin(t * .5 + s.y * 20) * 4, y, s.r, 0, 7); x.fill(); });
    // 目じるしの線
    const L = W < 560 ? 12 : 22, wide = W >= 560;
    MARK.forEach(([d, lab, k]) => { const y = yOf(d); if (y < -30 || y > Hh + 30) return;
      x.save(); x.setLineDash(k === 'm' ? [10, 6] : [4, 6]); x.strokeStyle = k === 'm' ? 'rgba(251,191,36,.85)' : k === 'z' ? 'rgba(186,230,253,.7)' : 'rgba(255,255,255,.6)'; x.lineWidth = k === 'm' ? 2 : 1.4; x.beginPath(); x.moveTo(0, y); x.lineTo(W - (wide ? 70 : 46), y); x.stroke(); x.restore();
      const icon = k === 'm' ? '⛰️ ' : k === 'z' ? '' : '📍 '; const lx = y < (wide ? 236 : 196) ? (wide ? 330 : 222) : L; if (lx > L && W - lx < 260) return; const fs = wide ? 14 : 12, ls = wrap(icon + lab, W - lx - (wide ? 80 : 54), fs, 700); ls.forEach((t2, i) => txt(t2, lx, y - 8 - (ls.length - 1 - i) * (fs + 4), fs, k === 'm' ? '#fde68a' : '#e0f2fe', 'left', 700)); });
    // 生き物
    LIFE.forEach(([d, em, nm, note, glow], k) => { const y = yOf(d) + Math.sin(t * 1.2 + k) * 5; if (y < -80 || y > Hh + 80) return;
      const es = wide ? 46 : 34, sx = (wide ? (k % 2 ? .3 : .52) * W : (k % 2 ? 34 : 58)) + Math.sin(t * .4 + k * 2) * (wide ? 12 : 6);
      if (glow && depth > 200) { const a = .35 + .25 * Math.sin(t * 3 + k); const gg = x.createRadialGradient(sx, y - es * .35, 2, sx, y - es * .35, es * 1.4); gg.addColorStop(0, `rgba(103,232,249,${a})`); gg.addColorStop(1, 'rgba(103,232,249,0)'); x.fillStyle = gg; x.beginPath(); x.arc(sx, y - es * .35, es * 1.4, 0, 7); x.fill(); }
      x.save(); x.font = es + 'px ' + F; x.textAlign = 'center'; x.fillText(em, sx, y); x.restore();
      const bx = sx + es * .7, lw = wide ? Math.min(340, W - bx - 80) : W - bx - 50, fs2 = wide ? 12 : 10.5, nl = wrap(note, lw - 20, fs2, 600), bh = 26 + nl.length * (fs2 + 5), by = y - es * .9;
      rr(bx, by, lw, bh, 10); x.fillStyle = 'rgba(15,23,42,.62)'; x.fill();
      txt(nm + '　' + fmt(d) + 'm', bx + 10, by + 18, wide ? 14 : 12, '#fff'); nl.forEach((t2, i) => txt(t2, bx + 10, by + 18 + (i + 1) * (fs2 + 5) + 1, fs2, '#bae6fd', 'left', 600)); });
    // 海の底
    const fy = yOf(MAXD);
    if (fy < Hh + 20) { x.fillStyle = '#1c1917'; x.beginPath(); x.moveTo(0, fy + 30); for (let i = 0; i <= 20; i++) x.lineTo(i / 20 * W, fy + 6 + Math.sin(i * 1.7) * 8); x.lineTo(W, Hh + 400); x.lineTo(0, Hh + 400); x.closePath(); x.fill();
      txt('🏁 マリアナ海溝 チャレンジャー海淵（約10,920m）', W / 2, fy + 60, wide ? 18 : 14, '#fde68a', 'center'); txt('1960年、潜水艇トリエステ号が人類で初めてここまでもぐった', W / 2, fy + 84, wide ? 13 : 11, '#e7e5e4', 'center', 600); }
    // 右の深さものさし
    const RX = W - (wide ? 44 : 30), RT = 70, RB = Hh - 70;
    x.strokeStyle = 'rgba(255,255,255,.35)'; x.lineWidth = 2; x.beginPath(); x.moveTo(RX, RT); x.lineTo(RX, RB); x.stroke();
    ZONES.forEach(([a, b], k) => { const y1 = RT + d2p(a) * (RB - RT), y2 = RT + d2p(Math.min(b, MAXD)) * (RB - RT); x.fillStyle = `rgba(186,230,253,${.35 - k * .06})`; x.fillRect(RX - 4, y1, 8, y2 - y1); });
    [0, 200, 1000, 2000, 4000, 6000, 8000, 10920].forEach(d => { const y = RT + d2p(d) * (RB - RT); x.fillStyle = 'rgba(255,255,255,.7)'; x.fillRect(RX - 7, y, 14, 1.5); txt(d >= 1000 ? (d / 1000).toFixed(d === 10920 ? 1 : 0) + 'k' : String(d), RX - 10, y + 4, 10, 'rgba(255,255,255,.75)', 'right', 700); });
    const py = RT + d2p(depth) * (RB - RT); x.fillStyle = '#facc15'; x.beginPath(); x.moveTo(RX + 6, py); x.lineTo(RX + 16, py - 7); x.lineTo(RX + 16, py + 7); x.closePath(); x.fill();
    // 左上の計器
    const atm = 1 + depth / 10, kg = atm * 1.033, temp = interp(TEMP, depth), zone = ZONES.find(z => depth < z[1])[2];
    const pw = wide ? 270 : 200, ph = wide ? 196 : 162; rr(12, 12, pw, ph, 14); x.fillStyle = 'rgba(2,6,23,.82)'; x.fill();
    txt('水深', 26, 40, wide ? 13 : 11, '#bae6fd'); txt(fmt(depth), 26, wide ? 82 : 70, wide ? 44 : 34, '#fff', 'left', 900); x.font = '900 ' + (wide ? 44 : 34) + 'px ' + F; const nw = x.measureText(fmt(depth)).width; txt('m', 32 + nw, wide ? 82 : 70, wide ? 18 : 15, '#fff');
    txt(zone, 26, wide ? 104 : 90, wide ? 13 : 11, '#fde68a');
    const rows = [['光', light >= 1 ? light.toFixed(light >= 10 ? 0 : 1) + '%' : light > 0.01 ? light.toFixed(2) + '%' : '届かない'], ['水圧', (atm < 100 ? atm.toFixed(1) : fmt(atm)) + ' 気圧'], ['指先にかかる重さ', kg >= 1000 ? '約' + (kg / 1000).toFixed(2) + 'トン' : '約' + (kg < 100 ? kg.toFixed(1) : fmt(kg)) + 'kg'], ['水温（目安）', temp.toFixed(1) + '℃']];
    rows.forEach(([k, v], i) => { const yy = (wide ? 128 : 110) + i * (wide ? 18 : 15); txt(k, 26, yy, wide ? 12 : 10.5, '#94a3b8', 'left', 700); txt(v, 12 + pw - 14, yy, wide ? 13 : 11, '#fff', 'right', 800); });
    // 風船（空気が押し縮められる）
    const bs = Math.cbrt(1 / atm), br = (wide ? 22 : 16) * Math.max(bs, .08), bxp = 12 + pw + (wide ? 34 : 24), byp = wide ? 50 : 42;
    if (W > 420) { x.fillStyle = '#f43f5e'; x.beginPath(); x.ellipse(bxp, byp, br, br * 1.15, 0, 0, 7); x.fill(); x.strokeStyle = 'rgba(255,255,255,.6)'; x.lineWidth = 1; x.beginPath(); x.moveTo(bxp, byp + br * 1.15); x.lineTo(bxp, byp + 34); x.stroke();
      txt('風船 ' + (1 / atm >= .1 ? Math.round(100 / atm) + '%' : (atm).toFixed(0) + '分の1'), bxp, byp + 50, 10.5, '#fecdd3', 'center', 700); }
    if (depth < 3 && !auto) { const a = .6 + .4 * Math.sin(t * 3); txt('▼ スクロールしてもぐる', W / 2, Hh - 40, wide ? 18 : 15, `rgba(12,74,110,${a})`, 'center'); }
    $('dvAuto').textContent = auto ? '■ 止める' : (depth >= MAXD - 1 ? '↑ 海面へ' : '▼ 自動でもぐる');
    requestAnimationFrame(frame);
  }
  function stopAuto() { if (auto) { cancelAnimationFrame(auto.raf); auto = null; } }
  function goTo(d, ms) { stopAuto(); const start = window.scrollY, top = dive.getBoundingClientRect().top + window.scrollY - HT, end = top + d2p(d) * (SH - Hh), T0 = performance.now();
    const step = now => { const k = clamp((now - T0) / ms, 0, 1); window.scrollTo({ behavior: 'instant', top: start + (end - start) * (ms > 4000 ? k : (k < .5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2)) }); if (k < 1 && auto) auto.raf = requestAnimationFrame(step); else auto = null; };
    auto = { raf: requestAnimationFrame(step) }; }
  $('dvAuto').addEventListener('click', () => { if (auto) return stopAuto(); if (depth >= MAXD - 1) return goTo(0, 2500); goTo(MAXD, Math.max(8000, (MAXD - depth) / MAXD * 75000)); });
  $('dvStart').addEventListener('click', () => { const top = dive.getBoundingClientRect().top + window.scrollY - HT; window.scrollTo({ top, behavior: 'smooth' }); setTimeout(() => goTo(MAXD, 75000), 700); });
  $('dvJump').addEventListener('change', e => { const v = +e.target.value; if (v >= 0) goTo(v, 1800); e.target.value = '-1'; });
  ['wheel', 'touchstart', 'keydown'].forEach(ev => window.addEventListener(ev, () => { if (auto) stopAuto(); }, { passive: true }));
  window.addEventListener('resize', size); size(); requestAnimationFrame(frame);
  // シェア・結果（どこまでもぐったか）
  let SHARE = '';
  function upd() { const d = Math.round(maxDepth), atm = 1 + d / 10; const near = LIFE.filter(l => l[0] <= d).pop();
    $('rBig').textContent = fmt(d); $('rSub').textContent = '水圧 ' + (atm < 100 ? atm.toFixed(1) : fmt(atm)) + '気圧' + (near ? '・出会った生き物 ' + LIFE.filter(l => l[0] <= d).length + '種（最後は' + near[2] + '）' : '');
    SHARE = d >= MAXD - 5 ? '深海シミュレーターで、マリアナ海溝の底（約10,920m）までもぐった🌊 水圧は約1,100気圧、指先に約1.1トン。そこにも生き物がいた。' : `深海シミュレーターで水深${fmt(d)}mまでもぐった🌊 水圧は${atm < 100 ? atm.toFixed(1) : fmt(atm)}気圧。${near ? near[2] + 'に出会った。' : ''}`; }
  setInterval(upd, 500); upd();
  $('shareBtn').addEventListener('click', () => window.open('https://twitter.com/intent/tweet?text=' + encodeURIComponent(SHARE) + '&url=' + encodeURIComponent(location.href) + '&hashtags=' + encodeURIComponent('シミュラボ'), '_blank', 'noopener'));
  $('copyBtn').addEventListener('click', async () => { try { await navigator.clipboard.writeText(SHARE + '\n' + location.href); $('copyBtn').textContent = 'コピーしました ✓'; setTimeout(() => $('copyBtn').textContent = '結果をコピー', 1600); } catch { alert(SHARE); } });
  window.__dv = { p2d, d2p, get depth() { return depth; }, goTo, LIFE, MARK };
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
    jumps = "".join(f'<option value="{d}">{t}</option>' for d, t in [(-1, "深さを選んでジャンプ"), (0, "海面"), (200, "200m 光が1%"), (634, "634m スカイツリー"), (1000, "1,000m 光が届かない"),
                                                                       (3776, "3,776m 富士山"), (6500, "6,500m しんかい6500"), (8336, "8,336m 最も深い魚"), (10920, "10,920m 海溝の底")])
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
    <h1>深海へもぐるシミュレーター（海面からマリアナ海溝の底まで）</h1>
    <p class="lead">画面を下へスクロールすると、海の表面から、世界一深いマリアナ海溝の底（約10,920m）まで、もぐっていけます。もぐるほど光は弱く、水圧は重く、水は冷たくなっていきます。とちゅうで出会う深海の生き物や、スカイツリー・富士山・エベレストを海に沈めた高さ比べも見てください。</p>
  </div>

  <section class="panel dv-intro">
    <p style="margin:0;font-weight:800;">🌊 下へスクロールして、自分のペースでもぐる。または…</p>
    <div class="btns">
      <button class="btn btn-primary" id="dvStart" style="width:auto;padding:12px 26px;">▼ 自動で海の底までもぐる（約75秒）</button>
      <select id="dvJump" style="padding:10px;border-radius:10px;font:inherit;">{jumps}</select>
    </div>
  </section>

  <section id="dive" aria-label="深海へもぐるアニメーション">
    <div id="dvStage">
      <canvas id="dv" aria-label="水深と、その深さの光・水圧・水温・生き物"></canvas>
      <div class="dv-ctl"><button type="button" id="dvAuto">▼ 自動でもぐる</button></div>
    </div>
  </section>

  <section class="panel dv-end">
    <div class="result">
      <div class="label">あなたがもぐった深さ</div>
      <div class="big"><span id="rBig">0</span><small> m</small></div>
      <div class="sub" id="rSub">—</div>
      <div style="text-align:center;margin-top:12px;"><span id="shareCount" class="share-count" style="display:none"></span></div>
      <div class="share-row">
        <button class="btn btn-x" id="shareBtn">𝕏 で結果をシェア</button>
        <button class="btn btn-ghost" id="copyBtn">結果をコピー</button>
      </div>
    </div>
  </section>

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
