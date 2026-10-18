"""2026-10-18 改善（GA4・サチコ 10/3〜10/17 の実データから選定）。生成済みHTMLを直接書き換える。
何度実行しても同じ結果になる（各ページにマーカーを入れ、入っていればスキップ。②は毎回作り直す）。
生成元（gen_sims*.py）を再実行したページは、このスクリプトをもう一度実行すれば戻る。

  ① 地震ライブ（jishin-live）… 10/16 の地震の日に Bing から約100人が来て平均10秒で離脱。
     「いま起きた地震」の震源・M・深さ・最大震度・津波・各地の震度を先頭に出す。関連リンクを地震の仲間に。
  ② 理科の単元表（/rika/）に載っている「理科の授業向け」以外のシミュ（歯車・磁力線・太陽系など）に、
     その単元名・使いどころ・同じ単元の理科シミュ・/rika/ へのリンクを入れる（units.json から毎回作り直す）。
"""
import html as H
import io, json, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from improve_2026_10 import page, rep, set_title, add_faq  # noqa: E402

MARK_Q = "<!-- improved-2026-10b -->"


# ---------------------------------------------------------------- ① 地震ライブ
QUAKE_CSS = '''<style id="quake-now-style">
.quake-now{border:1px solid var(--line,#e3ded3);border-radius:12px;padding:16px 16px 12px;margin:0 0 18px;text-align:left;background:rgba(196,68,43,.04)}
.quake-now .qn-k{font-size:12.5px;font-weight:700;letter-spacing:.04em;opacity:.75}
.quake-now .qn-main{font-size:20px;font-weight:700;line-height:1.45;margin:4px 0 10px}
.quake-now .qn-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}
.quake-now .qn-grid div{background:rgba(127,127,127,.07);border-radius:8px;padding:7px 9px}
.quake-now .qn-grid b{display:block;font-size:11.5px;font-weight:600;opacity:.7}
.quake-now .qn-grid span{font-size:15px;font-weight:700}
.quake-now .qn-tsunami{margin-top:10px;padding:8px 10px;border-radius:8px;font-size:14px;font-weight:700;background:rgba(44,107,134,.08)}
.quake-now .qn-tsunami.warn{background:#c4442b;color:#fff}
.quake-now details{margin-top:10px;font-size:13px}
.quake-now summary{cursor:pointer;font-weight:700}
.quake-now .qn-pt{padding:4px 0;border-bottom:1px dashed rgba(127,127,127,.25)}
.quake-now .qn-links{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
.quake-now .qn-links a{font-size:13px}
@media (max-width:520px){.quake-now .qn-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.quake-now .qn-main{font-size:17px}}
</style>
'''

QUAKE_HTML = '''      <div class="quake-now" id="quakeNow">
        <div class="qn-k">最新の地震（気象庁発表）</div>
        <div class="qn-main" id="qnMain">データを読み込み中…</div>
        <div class="qn-grid">
          <div><b>発生時刻</b><span id="qnTime">—</span></div>
          <div><b>最大震度</b><span id="qnScale">—</span></div>
          <div><b>マグニチュード</b><span id="qnMag">—</span></div>
          <div><b>震源</b><span id="qnPlace">—</span></div>
          <div><b>深さ</b><span id="qnDepth">—</span></div>
          <div><b>発生から</b><span id="qnAgo">—</span></div>
        </div>
        <div class="qn-tsunami" id="qnTsunami">津波の情報：—</div>
        <details id="qnPoints"><summary id="qnPointsSum">各地の震度</summary><div id="qnPointsList"></div></details>
        <div class="qn-links">
          <a class="btn btn-ghost" href="https://www.jma.go.jp/bosai/map.html#contents=earthquake_map" target="_blank" rel="noopener">気象庁の地震情報を開く</a>
          <a class="btn btn-ghost" href="../kaibatsu-check/">自分の地域の海抜・ハザードマップ</a>
        </div>
      </div>
'''

QUAKE_JS = '''<script>
(() => {
  const $ = (id) => document.getElementById(id);
  const SCALE = {10:'震度1',20:'震度2',30:'震度3',40:'震度4',45:'震度5弱',50:'震度5強',55:'震度6弱',60:'震度6強',70:'震度7'};
  const TSUNAMI = {
    None: ['この地震による津波の心配はありません。', false],
    NonEffective: ['若干の海面変動があるかもしれませんが、被害の心配はありません。', false],
    Checking: ['津波の有無を調査中です。海岸からは離れて続報を待ってください。', true],
    Watch: ['津波注意報が発表されています。海岸から離れてください。', true],
    Warning: ['津波警報が発表されています。すぐに高い所へ避難してください。', true],
    Unknown: ['津波の情報はまだ発表されていません。', false]
  };
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const ago = (ms) => { const m = Math.floor(ms/60000); if(m < 60) return m + '分前'; const h = Math.floor(m/60); if(h < 24) return h + '時間前'; return Math.floor(h/24) + '日前'; };
  async function loadLatest(){
    try{
      const r = await fetch('https://api.p2pquake.net/v2/history?codes=551&limit=20');
      const j = await r.json();
      if(!j.length) return;
      // 同じ地震は「震度速報→震源→各地の震度」と複数回届く（新しい順）。最新の地震のレコードをまとめる
      const key = j[0].earthquake.time;
      const recs = j.filter((x) => x.earthquake.time === key);
      const q = { place: '', mag: null, depth: null, scale: -1, tsunami: 'Unknown', points: [] };
      for(const x of recs){
        const e = x.earthquake, hc = e.hypocenter || {};
        if(!q.place && hc.name) q.place = hc.name;
        if(q.mag == null && hc.magnitude != null && hc.magnitude >= 0) q.mag = hc.magnitude;
        if(q.depth == null && hc.depth != null && hc.depth >= 0) q.depth = hc.depth;
        if((e.maxScale ?? -1) > q.scale) q.scale = e.maxScale;
        if(q.tsunami === 'Unknown' && e.domesticTsunami && e.domesticTsunami !== 'Unknown') q.tsunami = e.domesticTsunami;
        if((x.points || []).length > q.points.length) q.points = x.points;
      }
      const t = new Date(key.replace(/\\//g,'-').replace(' ','T') + '+09:00');
      const when = (t.getMonth()+1) + '月' + t.getDate() + '日 ' + t.getHours() + '時' + String(t.getMinutes()).padStart(2,'0') + '分ごろ';
      const sc = SCALE[q.scale] || '調査中';
      $('qnMain').textContent = when + '、' + (q.place || '震源は調査中') + 'で最大' + sc + 'の地震';
      $('qnTime').textContent = when;
      $('qnScale').textContent = sc;
      $('qnMag').textContent = q.mag != null ? 'M' + q.mag.toFixed(1) : '調査中';
      $('qnPlace').textContent = q.place || '調査中';
      $('qnDepth').textContent = q.depth == null ? '調査中' : (q.depth === 0 ? 'ごく浅い' : '約' + q.depth + 'km');
      $('qnAgo').textContent = ago(Date.now() - t.getTime());
      const ts = TSUNAMI[q.tsunami] || TSUNAMI.Unknown;
      $('qnTsunami').textContent = '津波の情報：' + ts[0];
      $('qnTsunami').classList.toggle('warn', ts[1]);
      // 各地の震度（震度の大きい順・震度ごとに都道府県でまとめる）
      const by = new Map();
      for(const p of q.points){ const k = p.scale; if(!by.has(k)) by.set(k, []); by.get(k).push(p); }
      const rows = [...by.keys()].sort((a,b) => b - a).map((k) => {
        const pts = by.get(k); const pref = new Map();
        for(const p of pts){ if(!pref.has(p.pref)) pref.set(p.pref, []); pref.get(p.pref).push(p.addr); }
        return '<div class="qn-pt"><b>' + (SCALE[k] || '震度—') + '</b>　' + [...pref].map(([pf, a]) => esc(pf) + '：' + a.slice(0, 12).map(esc).join('、') + (a.length > 12 ? ' ほか' + (a.length - 12) + '地点' : '')).join('／') + '</div>';
      });
      $('qnPointsSum').textContent = '各地の震度（' + q.points.length + '地点）';
      $('qnPointsList').innerHTML = rows.join('') || '<div class="qn-pt">各地の震度はまだ発表されていません。</div>';
      $('qnPoints').open = q.points.length > 0 && q.points.length <= 12;
    }catch{
      $('qnMain').textContent = '最新の地震データを取得できませんでした。時間をおいて「最新に更新」を押してください。';
    }
  }
  loadLatest();
  $('reloadBtn').addEventListener('click', loadLatest);
})();
</script>
'''

QUAKE_ARTICLE = MARK_Q + '''
    <h2>震度とマグニチュードの違い</h2>
    <p><b>震度</b>は、その場所がどれだけ揺れたかを表す数字で、気象庁は震度0〜7の10段階（5と6は弱・強に分かれる）で発表します。<b>マグニチュード（M）</b>は、地震そのものの規模（放出されたエネルギーの大きさ）を表す数字です。1つの地震でマグニチュードは1つですが、震度は場所ごとに違います。マグニチュードが1大きくなると、エネルギーは約32倍、2大きくなると約1000倍になります。</p>
    <table>
      <tr><th></th><th>震度</th><th>マグニチュード</th></tr>
      <tr><td>表すもの</td><td>その場所の揺れの強さ</td><td>地震そのものの規模</td></tr>
      <tr><td>1つの地震で</td><td>場所ごとに違う</td><td>1つ</td></tr>
      <tr><td>段階</td><td>0・1・2・3・4・5弱・5強・6弱・6強・7（10段階）</td><td>M1増えるとエネルギー約32倍</td></tr>
    </table>
    <h2>地震の情報が出る順番</h2>
    <p>大きな揺れを観測すると、気象庁はおよそ次の順に情報を発表します。①<b>震度速報</b>（震度3以上の地域）→ ②<b>震源に関する情報</b>（震源・マグニチュード・津波の心配の有無）→ ③<b>震源・震度に関する情報</b>（各地の震度）。このページの「最新の地震」は、届いた情報をまとめて表示しているため、発生直後は震源やマグニチュードが「調査中」になり、数分後に埋まっていきます。</p>
    <div class="note">揺れを感じたら、まず身の安全を確保してください。津波の心配があるときは、このページを見るより先に、海岸や川から離れて高い所へ移動してください。</div>
    <h2>地震のしくみを学ぶ</h2>
    <p>なぜ最初に小さくカタカタ揺れ、あとから大きくユサユサ揺れるのか（P波とS波）は<a href="../jishin-ha/">地震の伝わり方シミュレーター</a>で、ビルの高さで揺れ方が変わる理由は<a href="../building-quake/">共振シミュレーター</a>で、津波が岸で高くなる理由は<a href="../tsunami-kishi/">津波シミュレーター</a>で確かめられます。中学1年理科「火山と地震」の授業向けのまとめは<a href="../../rika/#chu">理科の授業向けシミュ</a>にあります。</p>
'''

QUAKE_FAQ = [
    ("いま起きた地震の震源と震度は？", "このページの先頭「最新の地震」に、気象庁が発表した最新の地震の発生時刻・震源・マグニチュード・深さ・最大震度・津波の情報・各地の震度を表示しています。「最新に更新」で読み直せます。"),
    ("震度とマグニチュードの違いは？", "震度はその場所の揺れの強さ（震度0〜7の10段階）、マグニチュードは地震そのものの規模です。1つの地震でマグニチュードは1つですが、震度は場所ごとに違います。"),
    ("この地震で津波の心配はありますか？", "「最新の地震」の津波の情報に、気象庁の発表（津波の心配なし／若干の海面変動／調査中／津波注意報・警報）を表示しています。注意報・警報が出ているときは、ページを見るより先に海岸から離れて高い所へ避難してください。"),
]

QUAKE_RELATED = '''<div class="related-grid"><a class="related-card" href="../jishin-ha/"><span class="e">📳</span><span>地震の伝わり方（P波・S波）</span></a><a class="related-card" href="../chikyu-yure/"><span class="e">🌐</span><span>地球まるごと地震カウンター</span></a><a class="related-card" href="../building-quake/"><span class="e">🏢</span><span>地震でビルはどう揺れる？</span></a><a class="related-card" href="../tsunami-kishi/"><span class="e">🌊</span><span>津波はなぜ岸で高くなる？</span></a><a class="related-card" href="../kaibatsu-check/"><span class="e">⛰️</span><span>うちの海抜チェッカー</span></a></div>'''


def jishin_live():
    p = page("jishin-live"); h = p.read_text(encoding="utf-8")
    if MARK_Q in h: return "skip"
    h = set_title(h, "今日の地震・最新の地震情報ライブ｜震源・震度・津波と24時間の回数｜シミュラボ",
                  "いま起きた地震の震源・マグニチュード・深さ・最大震度・津波の有無と各地の震度を、気象庁発表の公開データからその場で表示。直近24時間・7日間の地震回数と最新10件も一目でわかります。",
                  "今日の地震・最新の地震情報ライブ｜日本はいまも揺れている")
    h = rep(h, "</head>", QUAKE_CSS + "</head>")
    h = rep(h, '<p class="lead">あなたが気づいていないだけで、日本のどこかは今日も揺れています。直近24時間に発表された地震を、公開データからその場で数えます。</p>',
            '<p class="lead">いま起きた地震の震源・震度・津波の情報と、直近24時間に日本で発表された地震の回数を、気象庁発表の公開データからその場で表示します。あなたが気づいていないだけで、日本のどこかは今日も揺れています。</p>')
    h = rep(h, '''    <div class="result">
      <div class="label">直近24時間、日本で発表された地震は</div>''', '''    <div class="result">
''' + QUAKE_HTML + '''      <div class="label">直近24時間、日本で発表された地震は</div>''')
    h = rep(h, "    <h2>引用・転載について</h2>", QUAKE_ARTICLE + "    <h2>引用・転載について</h2>")
    h = add_faq(h, QUAKE_FAQ, first=True)
    h = re.sub(r'<div class="related-grid">.*?</div>(?=\s*</nav>)', QUAKE_RELATED, h, count=1, flags=re.S)
    h = rep(h, '<script src="../../assets/result-fx.js', QUAKE_JS + '<script src="../../assets/result-fx.js')
    p.write_text(h, encoding="utf-8")
    return "ok"


# ---------------------------------------------------------------- ② 理科の授業向けへの逆リンク
RIKA_START, RIKA_END = "<!-- rika-links:start -->", "<!-- rika-links:end -->"
SEC_LABEL = {"sho": "小学校", "chu": "中学校", "ko": "高校"}


def h1_of(slug, cache={}):
    if slug not in cache:
        t = page(slug).read_text(encoding="utf-8")
        m = re.search(r"<h1>(.*?)</h1>", t, re.S)
        cache[slug] = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else slug
    return cache[slug]


def is_rika(slug):
    return 'href="../../rika/"' in page(slug).read_text(encoding="utf-8")


def core(unit):
    return re.sub(r"（.*?）", "", unit).strip()


def rika_links():
    U = json.load(io.open(ROOT / "scripts" / "rika" / "units.json", encoding="utf-8"))
    rows = {}   # slug -> [(sec, group, unit, use)]
    for s in U["sections"]:
        for g in s["groups"]:
            for it in g["items"]:
                rows.setdefault(it["id"], []).append((s["id"], g, it["unit"], it["use"]))
    total = len(rows)
    n = 0
    for slug, ent in rows.items():
        if not page(slug).exists() or is_rika(slug):
            continue
        lis, sibs, secs = [], [], []
        for sec, g, unit, use in ent:
            lis.append(f"<li><b>{H.escape(unit)}</b>　{H.escape(use)}</li>")
            secs.append(sec)
            same = [it["id"] for it in g["items"] if it["id"] != slug and core(it["unit"]) == core(unit)]
            rest = [it["id"] for it in g["items"] if it["id"] != slug and it["id"] not in same]
            for x in same + rest:
                if x not in sibs and page(x).exists() and is_rika(x):
                    sibs.append(x)
        sibs = sibs[:4]
        sec = secs[0]
        links = "".join(f'<a class="related-card" href="../{x}/"><span class="e">🔬</span><span>{H.escape(h1_of(x))}</span></a>' for x in sibs)
        box = f'''{RIKA_START}
  <section class="rika-box" aria-label="理科の授業で使うとき" style="margin:28px 0;padding:18px 18px 14px;border:1px solid var(--line,#e3ded3);border-radius:12px;">
    <h2 style="margin-top:0;">🔬 理科の授業で使うとき</h2>
    <ul style="margin:0 0 12px;padding-left:1.2em;line-height:1.7;">{"".join(lis)}</ul>
    {f'<p style="font-size:13.5px;font-weight:700;margin:0 0 8px;">同じ単元の授業向けシミュ</p><div class="related-grid">{links}</div>' if links else ''}
    <p style="margin:12px 0 0;"><a href="../../rika/#{sec}">{SEC_LABEL[sec]}の単元から授業向けシミュを探す（小学校〜高校・{total}本）→</a></p>
  </section>
{RIKA_END}
'''
        p = page(slug); h = p.read_text(encoding="utf-8")
        h = re.sub(re.escape(RIKA_START) + r".*?" + re.escape(RIKA_END) + r"\n", "", h, flags=re.S)
        anchor = '  <nav class="related"'
        if anchor not in h:
            anchor = '  <section class="req-banner">'
        assert h.count(anchor) == 1, (slug, anchor)
        h = h.replace(anchor, box + anchor)
        p.write_text(h, encoding="utf-8")
        n += 1
    return f"{n}本"


if __name__ == "__main__":
    print("① 地震ライブ:", jishin_live())
    print("② 理科への逆リンク:", rika_links())
