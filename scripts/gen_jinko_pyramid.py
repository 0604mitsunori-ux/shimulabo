# -*- coding: utf-8 -*-
"""日本の人口ピラミッド 動く年表（2026-11-18）— sims/jinko-pyramid/index.html を書き出す（冪等）。
   データ: scripts/data/jinko_pyramid.json（scripts/data/make_jinko_pyramid_json.py が公的統計の原表xlsxから作る）
     実績 1950〜2020年 = 総務省統計局 国勢調査（時系列データ 第2表）、推計 2025〜2070年 = 社人研 令和5年推計 出生中位(死亡中位)
   使い方: python scripts/data/make_jinko_pyramid_json.py → python scripts/gen_jinko_pyramid.py
   ※ フッターリンク（運営者情報ほか）もこのスクリプトが入れる。"""
import html as H, io, json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://shimulabo.com"
SLUG = "jinko-pyramid"
NAME = "日本の人口ピラミッド 動く年表"
TITLE = "日本の人口ピラミッド 動く年表｜1950年→2070年、富士山型・つりがね型・つぼ型に変わるのを再生で見る｜シミュラボ"
DESC = ("日本の人口ピラミッド（男女・5歳ごとの人口）を、1950年から2070年まで再生ボタンで動かして見られるシミュレーター。"
        "国勢調査の実績（1950〜2020年）と国立社会保障・人口問題研究所の将来推計（2025〜2070年）を使い、"
        "富士山型からつりがね型、つぼ型へ変わる様子と、総人口・65歳以上の割合・15歳未満の割合の変化が分かる。生まれ年を入れると自分の世代がどこにいるかも光る。")
OG_T = "日本の人口ピラミッド 動く年表｜1950→2070年を再生"
OG_D = "富士山型→つりがね型→つぼ型。生まれ年を入れると、自分の世代がピラミッドのどこにいるかが光る。"

DATA = json.load(io.open(os.path.join(ROOT, "scripts", "data", "jinko_pyramid.json"), encoding="utf-8"))

FAQ = [
    ("人口ピラミッドとは何ですか？", "国や地域の人口を、男女別・年齢別に横向きの棒グラフで表し、左右に男女を並べた図です。下が若い世代、上が高齢の世代です。子どもが多く高齢者が少ないと下が広い「富士山型（ピラミッド型）」、子どもと大人の数が近いと「つりがね型」、子どもが減って下がすぼまると「つぼ型」とよばれます。"),
    ("日本の人口ピラミッドはどう変わってきましたか？", "1950年は15歳未満が人口の約35%をしめる富士山型でした。その後、生まれる子どもの数が減り、つりがね型をへて、1990年代以降は下がすぼまったつぼ型になっています。65歳以上の割合は1950年の約5%から、2020年には約29%になりました。"),
    ("2070年の日本の人口はどうなると予測されていますか？", "国立社会保障・人口問題研究所の「日本の将来推計人口（令和5年推計）」の出生中位・死亡中位の仮定では、2070年の総人口は約8,700万人、65歳以上の割合は約39%と推計されています。出生や死亡、外国との出入りの仮定によって結果は変わります。"),
    ("ピラミッドに出っぱりがあるのはなぜですか？", "生まれた人数が特に多かった世代があるためです。1947〜1949年生まれの「団塊の世代」と、その子どもにあたる1971〜1974年生まれの「団塊ジュニア」の2つの山がはっきり見えます。年がたつと、この出っぱりが上へ移動していきます。"),
    ("このページの数字はどこから来ていますか？", "1950〜2020年は総務省統計局の国勢調査（時系列データ「年齢（5歳階級），男女別人口及び人口性比－全国」）、2025〜2070年は国立社会保障・人口問題研究所「日本の将来推計人口（令和5年推計）」の出生中位（死亡中位）推計の男女5歳階級別人口です。2015・2020年は年齢不詳をおぎなった値、それより前は年齢不詳を除いた値です。"),
]
REL = [("sedai-sakanobori", "🌳", "世代さかのぼりシミュレーター"), ("koreisha-itsu", "🎌", "高齢者は何歳から？ 判定ツール"), ("nenkin-kurisage", "📈", "年金繰下げ受給シミュレーター"),
       ("kenkou-jumyo", "🌿", "健康寿命シミュレーター"), ("jinsei-calendar", "🗓️", "人生カレンダーシミュレーター")]

ARTICLE = """
<h2>人口ピラミッドの3つの形</h2>
<div class="tbl-scroll"><table class="seo-table">
<tr><th>形</th><th>特徴</th><th>日本では（このページの分け方）</th></tr>
<tr><td>富士山型（ピラミッド型）</td><td>子どもが多く、上へ行くほど細い。生まれる人も亡くなる人も多い</td><td>1950〜1960年</td></tr>
<tr><td>つりがね型</td><td>子どもと働く世代の数が近く、上だけが細い</td><td>1965〜1985年</td></tr>
<tr><td>つぼ型</td><td>子どもが少なく、下がすぼまる。高齢者の割合が大きい</td><td>1990年以降</td></tr>
</table></div>
<p>このページでは、0〜14歳の棒の平均の長さを、15〜49歳の棒の平均の長さとくらべて、1.15倍以上なら富士山型、0.85倍未満ならつぼ型、そのあいだをつりがね型として表示しています（形の名前は目安で、決まった基準があるわけではありません）。</p>

<h2>2つの出っぱり ― 団塊の世代と団塊ジュニア</h2>
<p>第二次世界大戦のあと、1947〜1949年に生まれた人がとても多く、この世代を「団塊の世代」とよびます。その子どもにあたる1971〜1974年生まれの「団塊ジュニア」も人数が多い世代です。再生ボタンを押すと、この2つの出っぱりが年ごとに上へのぼっていくのが分かります。団塊の世代は2025年にすべての人が75歳以上になりました。</p>

<h2>数字の読み方</h2>
<ul>
<li><b>65歳以上の割合（高齢化率）</b>：7%をこえると「高齢化社会」、14%で「高齢社会」、21%で「超高齢社会」とよばれます。日本は1970年に7%、1995年に14%、2010年に21%をこえました（このページの国勢調査の値）。</li>
<li><b>15〜64歳</b>は「生産年齢人口」とよばれ、働く世代のめやすです。</li>
<li>2025年以降は<b>将来推計</b>（予測）で、点線のグラフで表しています。実際の人口は、生まれる子どもの数や外国との人の出入りによって変わります。</li>
</ul>
"""

REFS = [
    "総務省統計局「国勢調査」時系列データ 第2表「年齢（5歳階級），男女別人口及び人口性比－全国（大正9年～令和2年）」（e-Stat 統計表ID 000001085926）",
    "国立社会保障・人口問題研究所「日本の将来推計人口（令和5年推計）」表1-9A 男女年齢5歳階級別人口（総人口）：出生中位（死亡中位）推計",
    "国立社会保障・人口問題研究所「人口統計資料集」",
]

STAGE = r"""
<style>
.jp-wrap{display:grid;grid-template-columns:minmax(0,1fr) 250px;gap:16px;align-items:start;}
@media (max-width:760px){.jp-wrap{grid-template-columns:1fr;}}
#pyr{width:100%;height:520px;display:block;border-radius:12px;background:#fbfaf7;}
@media (max-width:760px){#pyr{height:440px;}}
.jp-year{font-size:52px;font-weight:900;line-height:1;letter-spacing:-.02em;color:var(--ink,#1f2937);}
.jp-tag{display:inline-block;font-size:12px;font-weight:800;border-radius:999px;padding:3px 10px;margin-left:6px;vertical-align:middle;}
.jp-tag.census{background:#e0f2fe;color:#075985;} .jp-tag.ipss{background:#fef3c7;color:#92400e;}
.jp-shape{margin:10px 0 4px;font-size:20px;font-weight:900;}
.jp-stats{display:grid;grid-template-columns:1fr auto;gap:6px 10px;font-size:14px;margin-top:8px;}
.jp-stats b{font-size:16px;text-align:right;}
.jp-ctl{display:flex;gap:10px;align-items:center;margin-top:14px;flex-wrap:wrap;}
.jp-ctl input[type=range]{flex:1;min-width:200px;}
.jp-play{border:none;background:var(--accent,#c2410c);color:#fff;font:inherit;font-weight:900;border-radius:999px;padding:10px 18px;cursor:pointer;min-width:110px;}
.jp-ticks{display:flex;justify-content:space-between;font-size:11px;color:#6b7280;margin-top:2px;padding:0 4px;}
.jp-opts{display:flex;gap:14px;flex-wrap:wrap;align-items:center;margin-top:12px;font-size:14px;}
.jp-opts input[type=number]{width:96px;padding:8px;border-radius:10px;border:1px solid #d6d3d1;font:inherit;}
.jp-opts select{padding:8px;border-radius:10px;border:1px solid #d6d3d1;font:inherit;}
#me{margin-top:10px;font-size:14px;font-weight:700;min-height:1.4em;}
#trend{width:100%;height:190px;display:block;margin-top:14px;border-radius:12px;background:#fbfaf7;cursor:pointer;}
</style>
"""

JS = r"""
(() => {
  const D = __DATA__;
  const $ = id => document.getElementById(id);
  const AG = D.ages, YRS = Object.keys(D.years).map(Number).sort((a, b) => a - b);
  const F = '"Hiragino Sans","Noto Sans JP","Yu Gothic",Meiryo,sans-serif';
  const CM = '#3b82f6', CF = '#ec4899', HL = '#f59e0b';
  const pc = $('pyr'), px = pc.getContext('2d'), tc = $('trend'), tx = tc.getContext('2d');
  let idx = 0, from = null, t0 = 0, playing = null, dpr = 1;
  const MAXV = Math.max(...YRS.flatMap(y => D.years[y].m.concat(D.years[y].f)));
  const sum = a => a.reduce((s, v) => s + v, 0);
  function stats(y) { const o = D.years[y], tot = sum(o.m) + sum(o.f), k = (a, b) => sum(o.m.slice(a, b)) + sum(o.f.slice(a, b));
    const yb = k(0, 3) / 6, mid = k(3, 10) / 14, r = yb / mid;
    return { total: o.total, p65: k(13, 18) / tot * 100, p14: k(0, 3) / tot * 100, p1564: k(3, 13) / tot * 100, shape: r >= 1.15 ? '富士山型（ピラミッド型）' : r >= .85 ? 'つりがね型' : 'つぼ型', r }; }
  function birth() { const v = parseInt($('by').value, 10); return v >= 1900 && v <= 2070 ? v : null; }
  function ageIdx(y, b) { const a = y - b; if (a < 0) return -1; return Math.min(17, Math.floor(a / 5)); }
  function size(c) { dpr = Math.min(2, window.devicePixelRatio || 1); const w = c.clientWidth, h = c.clientHeight; c.width = w * dpr; c.height = h * dpr; c.getContext('2d').setTransform(dpr, 0, 0, dpr, 0, 0); return [w, h]; }
  function cur() { // 補間中の棒の長さ（アニメーション用。数値表示はつねにデータのある年）
    const o = D.years[YRS[idx]]; if (!from) return o;
    const k = Math.min(1, (performance.now() - t0) / 450), e = k < .5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
    if (k >= 1) { from = null; return o; }
    return { m: o.m.map((v, i) => from.m[i] + (v - from.m[i]) * e), f: o.f.map((v, i) => from.f[i] + (v - from.f[i]) * e) };
  }
  function drawPyr() {
    const [W, Hh] = size(pc), y = YRS[idx], o = cur(), cmpY = +$('cmp').value, b = birth();
    px.clearRect(0, 0, W, Hh);
    const narrow = W < 520, top = 34, bot = narrow ? 42 : 30, labW = narrow ? 44 : 56, cx = W / 2, half = cx - labW / 2 - 10;
    const rowH = (Hh - top - bot) / 18, sc = half / (MAXV * 1.04);
    px.font = '800 ' + (narrow ? 13 : 15) + 'px ' + F; px.textAlign = 'center';
    px.fillStyle = CM; px.fillText('男', cx - labW / 2 - half / 2, 20); px.fillStyle = CF; px.fillText('女', cx + labW / 2 + half / 2, 20);
    // 目盛り（千人→万人）
    px.font = '600 10px ' + F; px.fillStyle = '#9ca3af'; px.strokeStyle = '#ece8df'; px.lineWidth = 1;
    const step = MAXV > 5000 ? 2000 : 1000;
    for (let v = 0; v <= MAXV; v += step) { [cx - labW / 2 - v * sc, cx + labW / 2 + v * sc].forEach(X => { px.beginPath(); px.moveTo(X, top); px.lineTo(X, Hh - bot); px.stroke(); px.fillText(v === 0 ? '0' : (v / 10) + '万', X, Hh - bot + 14); }); }
    const hi = b ? ageIdx(y, b) : -1, gens = [[1947, 1949, '団塊の世代'], [1971, 1974, '団塊ジュニア']];
    for (let i = 0; i < 18; i++) {
      const Y = Hh - bot - (i + 1) * rowH, h = rowH * .84, m = o.m[i] * sc, f = o.f[i] * sc, on = i === hi;
      px.fillStyle = on ? HL : CM; px.globalAlpha = on ? 1 : .82; px.fillRect(cx - labW / 2 - m, Y, m, h);
      px.fillStyle = on ? HL : CF; px.fillRect(cx + labW / 2, Y, f, h); px.globalAlpha = 1;
      px.fillStyle = '#4b5563'; px.font = '700 ' + (narrow ? 10 : 11) + 'px ' + F; px.textAlign = 'center';
      px.fillText(i === 17 ? '85〜' : (i * 5) + '〜' + (i * 5 + 4), cx, Y + h * .78);
      if (cmpY && D.years[cmpY]) { const c = D.years[cmpY]; px.strokeStyle = '#111827'; px.setLineDash([4, 3]); px.lineWidth = 1.4;
        px.strokeRect(cx - labW / 2 - c.m[i] * sc, Y, c.m[i] * sc, h); px.strokeRect(cx + labW / 2, Y, c.f[i] * sc, h); px.setLineDash([]); }
    }
    // 団塊の世代・団塊ジュニアの目じるし
    if ($('gen').checked) gens.forEach(([a, z, nm]) => { const i1 = ageIdx(y, z), i2 = ageIdx(y, a); if (i1 < 0 || y - z > 100) return; const i = Math.round((i1 + Math.max(i1, i2)) / 2); if (i > 17) return;
      const Y = Hh - bot - (i + 1) * rowH + rowH * .42, lab = narrow ? nm : nm + '（' + a + '〜' + String(z).slice(2) + '年生）';
      px.font = '800 ' + (narrow ? 10.5 : 12) + 'px ' + F; const tw = px.measureText(lab).width, X = Math.min(cx + labW / 2 + o.f[i] * sc + 6, W - tw - 22);
      px.fillStyle = 'rgba(255,255,255,.92)'; px.beginPath(); px.roundRect ? px.roundRect(X + 6, Y - 9, tw + 12, 18, 9) : px.rect(X + 6, Y - 9, tw + 12, 18); px.fill();
      px.fillStyle = '#7c3aed'; px.textAlign = 'left'; px.beginPath(); px.moveTo(X, Y); px.lineTo(X + 7, Y - 5); px.lineTo(X + 7, Y + 5); px.fill(); px.fillText(lab, X + 12, Y + 4); });
    if (cmpY && D.years[cmpY]) { px.textAlign = 'right'; px.fillStyle = '#111827'; px.font = '700 11px ' + F; px.fillText('点線＝' + cmpY + '年', W - 6, narrow ? Hh - 6 : 20); }
    if (from) requestAnimationFrame(drawPyr);
  }
  function drawTrend() {
    const [W, Hh] = size(tc), L = 44, R = 44, T = 22, B = 24; tx.clearRect(0, 0, W, Hh);
    const x = y => L + (y - 1950) / 120 * (W - L - R), yT = v => Hh - B - (v - 80000) / (130000 - 80000) * (Hh - T - B), yP = v => Hh - B - v / 45 * (Hh - T - B);
    tx.font = '600 10px ' + F; tx.fillStyle = '#9ca3af'; tx.strokeStyle = '#ece8df'; tx.textAlign = 'center';
    for (let y = 1950; y <= 2070; y += 20) { tx.beginPath(); tx.moveTo(x(y), T); tx.lineTo(x(y), Hh - B); tx.stroke(); tx.fillText(y, x(y), Hh - B + 14); }
    tx.textAlign = 'right'; [[80000, '8千万'], [100000, '1億'], [120000, '1.2億']].forEach(([v, t]) => tx.fillText(t, L - 4, yT(v) + 3));
    tx.textAlign = 'left'; [0, 20, 40].forEach(v => tx.fillText(v + '%', W - R + 4, yP(v) + 3));
    const line = (f, col) => { [['census', []], ['ipss', [5, 4]]].forEach(([src, dash]) => { tx.beginPath(); tx.setLineDash(dash); tx.strokeStyle = col; tx.lineWidth = 2.4; let st = false;
      YRS.forEach((y, i) => { const o = D.years[y]; if (o.src !== src && !(src === 'ipss' && y === 2020)) return; const X = x(y), Y = f(y); st ? tx.lineTo(X, Y) : tx.moveTo(X, Y); st = true; }); tx.stroke(); }); tx.setLineDash([]); };
    line(y => yT(D.years[y].total), '#0f766e'); line(y => yP(stats(y).p65), '#dc2626'); line(y => yP(stats(y).p14), '#2563eb');
    tx.font = '800 11px ' + F; tx.textAlign = 'left'; tx.fillStyle = '#0f766e'; tx.fillText('総人口', L + 4, T - 6); tx.fillStyle = '#dc2626'; tx.fillText('65歳以上の割合', L + 54, T - 6); tx.fillStyle = '#2563eb'; tx.fillText('15歳未満の割合', L + 150, T - 6);
    tx.fillStyle = '#6b7280'; tx.textAlign = 'right'; tx.fillText('点線＝推計', W - R, T - 6);
    const X = x(YRS[idx]); tx.strokeStyle = '#f59e0b'; tx.lineWidth = 2; tx.beginPath(); tx.moveTo(X, T); tx.lineTo(X, Hh - B); tx.stroke();
  }
  function fmtPop(k) { const man = k / 10; return man >= 10000 ? (man / 10000).toFixed(2).replace(/0$/, '') + '億人' : Math.round(man).toLocaleString() + '万人'; }
  function render() {
    const y = YRS[idx], o = D.years[y], s = stats(y), b = birth();
    $('yr').textContent = y; $('src').textContent = o.src === 'census' ? '国勢調査（実績）' : '将来推計（予測）'; $('src').className = 'jp-tag ' + o.src;
    $('shape').textContent = s.shape; $('sTot').textContent = fmtPop(o.total); $('s65').textContent = s.p65.toFixed(1) + '%'; $('s14').textContent = s.p14.toFixed(1) + '%'; $('s1564').textContent = s.p1564.toFixed(1) + '%';
    $('yrR').value = idx;
    let me = '';
    if (b) { const a = y - b, i = ageIdx(y, b);
      if (a < 0) me = `${b}年生まれの人は、${y}年にはまだ生まれていません。`;
      else { const n = D.years[y].m[i] + D.years[y].f[i]; me = `${b}年生まれの人は、${y}年に${a}歳前後。オレンジの段（${i === 17 ? '85歳以上' : (i * 5) + '〜' + (i * 5 + 4) + '歳'}）にいて、この段は約${Math.round(n / 10).toLocaleString()}万人。`; } }
    $('me').textContent = me;
    drawPyr(); drawTrend(); upd();
  }
  function go(i, anim) { i = Math.max(0, Math.min(YRS.length - 1, i)); if (anim !== false && i !== idx) { const o = cur(); from = { m: o.m.slice(), f: o.f.slice() }; t0 = performance.now(); } idx = i; render(); }
  function stop() { if (playing) { clearInterval(playing); playing = null; } $('play').textContent = '▶ 再生'; }
  $('play').addEventListener('click', () => { if (playing) return stop(); if (idx >= YRS.length - 1) go(0, false); $('play').textContent = '■ 止める';
    playing = setInterval(() => { if (idx >= YRS.length - 1) return stop(); go(idx + 1); }, 900); });
  $('yrR').max = YRS.length - 1; $('yrR').addEventListener('input', e => { stop(); go(+e.target.value); });
  ['by', 'cmp', 'gen'].forEach(id => $(id).addEventListener('input', render));
  tc.addEventListener('click', e => { const r = tc.getBoundingClientRect(), y = 1950 + (e.clientX - r.left - 44) / (r.width - 88) * 120; stop(); go(Math.round((y - 1950) / 5)); });
  $('cmp').innerHTML = '<option value="0">重ねない</option>' + YRS.map(y => `<option value="${y}"${y === 1950 ? ' selected' : ''}>${y}年</option>`).join('');
  window.addEventListener('resize', render);
  // シェア
  let SHARE = '';
  function upd() { const b = birth(), y = YRS[idx], s = stats(y);
    $('rBig').textContent = y + '年'; $('rSub').textContent = `${s.shape}・総人口${fmtPop(D.years[y].total)}・65歳以上${s.p65.toFixed(1)}%`;
    if (b && b <= 2070) { const a70 = 2070 - b, i = ageIdx(2070, b); SHARE = a70 >= 0 ? `${b}年生まれの私は、2070年に${a70}歳。そのとき日本の65歳以上は約${stats(2070).p65.toFixed(0)}%、同じ年代（${i === 17 ? '85歳以上' : (i * 5) + '〜' + (i * 5 + 4) + '歳'}）は約${Math.round((D.years[2070].m[i] + D.years[2070].f[i]) / 10).toLocaleString()}万人（社人研の推計）。` : ''; }
    if (!SHARE || !b) SHARE = `日本の人口ピラミッド、${y}年は${s.shape}。65歳以上が${s.p65.toFixed(1)}%（1950年は${stats(1950).p65.toFixed(1)}%）。1950→2070年を再生で見られる。`; }
  $('shareBtn').addEventListener('click', () => window.open('https://twitter.com/intent/tweet?text=' + encodeURIComponent(SHARE) + '&url=' + encodeURIComponent(location.href) + '&hashtags=' + encodeURIComponent('シミュラボ'), '_blank', 'noopener'));
  $('copyBtn').addEventListener('click', async () => { try { await navigator.clipboard.writeText(SHARE + '\n' + location.href); $('copyBtn').textContent = 'コピーしました ✓'; setTimeout(() => $('copyBtn').textContent = '結果をコピー', 1600); } catch { alert(SHARE); } });
  go(0, false);
  window.__jp = { go, stats, YRS, get idx() { return idx; } };
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
    js = JS.replace("__DATA__", json.dumps(DATA, ensure_ascii=False, separators=(",", ":")))
    ticks = "".join(f"<span>{y}</span>" for y in (1950, 1970, 1990, 2010, 2030, 2050, 2070))
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

  <nav class="breadcrumb" aria-label="breadcrumb"><a href="../../">ホーム</a><span>›</span>学生・勉強<span>›</span><span class="cur">{esc(NAME)}</span></nav>

  <div class="sim-head">
    <div class="cat">学生・勉強</div>
    <h1>日本の人口ピラミッド 動く年表（1950年→2070年）</h1>
    <p class="lead">再生ボタンを押すと、日本の人口ピラミッドが1950年から2070年まで5年ごとに動きます。子どもが多い富士山型から、つりがね型、つぼ型へ。生まれ年を入れると、自分の世代がどの段にいるかがオレンジ色で光ります。1950〜2020年は国勢調査の実績、2025年以降は国の研究所の将来推計です。</p>
  </div>

  <section class="panel">
    <div class="jp-wrap">
      <canvas id="pyr" aria-label="男女・年齢5歳ごとの人口ピラミッド"></canvas>
      <div>
        <div><span class="jp-year" id="yr">1950</span><span class="jp-tag census" id="src">国勢調査（実績）</span></div>
        <div class="jp-shape" id="shape">—</div>
        <div class="jp-stats">
          <span>総人口</span><b id="sTot">—</b>
          <span>65歳以上の割合</span><b id="s65">—</b>
          <span>15〜64歳の割合</span><b id="s1564">—</b>
          <span>15歳未満の割合</span><b id="s14">—</b>
        </div>
        <div id="me"></div>
      </div>
    </div>
    <div class="jp-ctl">
      <button type="button" class="jp-play" id="play">▶ 再生</button>
      <input type="range" id="yrR" min="0" max="24" step="1" value="0" aria-label="年">
    </div>
    <div class="jp-ticks">{ticks}</div>
    <div class="jp-opts">
      <label>生まれ年 <input type="number" id="by" min="1900" max="2070" placeholder="例 1990" inputmode="numeric"></label>
      <label>点線で重ねる <select id="cmp"></select></label>
      <label><input type="checkbox" id="gen" checked> 団塊の世代・団塊ジュニアの目じるし</label>
    </div>
    <canvas id="trend" aria-label="総人口と年齢の割合の移り変わり（クリックでその年へ）"></canvas>
    <p class="hint" style="margin:6px 0 0">下のグラフをクリックすると、その年へ移動します。棒の長さは千人単位のデータから描いています。</p>
  </section>

  <section class="panel">
    <div class="result">
      <div class="label">いま見ている年</div>
      <div class="big"><span id="rBig">1950年</span></div>
      <div class="sub" id="rSub">—</div>
      <div style="text-align:center;margin-top:12px;"><span id="shareCount" class="share-count" style="display:none"></span></div>
      <div class="share-row">
        <button class="btn btn-x" id="shareBtn">𝕏 でシェア</button>
        <button class="btn btn-ghost" id="copyBtn">結果をコピー</button>
      </div>
    </div>
  </section>

  <article class="article">
{ARTICLE}
    <h2>よくある質問</h2>
    <dl class="faq">{faq}</dl>
    <h2>参考にした資料（データの出典）</h2>
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

<script>{js}</script>
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
