# -*- coding: utf-8 -*-
"""API連携シリーズ第5弾 15本（1回限り）。sims生成→OGP→index→/live/→sitemap。"""
import os, io, re, json

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPTS)
TODAY = "2026-08-20"

_g10c = io.open(os.path.join(SCRIPTS, "gen_sims_api10c.py"), encoding="utf-8").read()
def _block(name):
    return re.search(name + r' = """(.*?)"""', _g10c, re.S).group(1)
SKELETON = _block("SKELETON")
SHARE_ROW = _block("SHARE_ROW")
JS_COMMON = _block("JS_COMMON")
PREF_ROWS = eval("[" + re.search(r'PREF_ROWS = \[(.*?)\]\n', _g10c, re.S).group(1) + "]")
PREFS_JS = "  const PREFS = [\n" + "\n".join("    ['%s',%s,%s]," % r for r in PREF_ROWS) + "\n  ];\n  $('pref').innerHTML = PREFS.map((p,i) => '<option value=\"' + i + '\"' + (i===12?' selected':'') + '>' + p[0] + '</option>').join('');"

def faq_dl(faqs): return "".join("<dt>%s</dt><dd>%s</dd>" % (q, a) for q, a in faqs)
def faq_ld(faqs):
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in faqs]}, ensure_ascii=False)
def related(items):
    return "".join('<a class="related-card" href="../%s/"><span class="e">%s</span><span>%s</span></a>' % (s, e, t) for s, e, t in items)

G = dict(wonder="linear-gradient(135deg,#eef2ff,#e0e7ff)", play="linear-gradient(135deg,#fdf4ff,#fae8ff)",
         marketing="linear-gradient(135deg,#fff7ed,#ffedd5)", pet="linear-gradient(135deg,#fef9c3,#fde68a)",
         sports="linear-gradient(135deg,#ecfdf5,#d1fae5)", home="linear-gradient(135deg,#ecfdf5,#d1fae5)",
         season="linear-gradient(135deg,#fff7ed,#fce7f3)", tool="linear-gradient(135deg,#eff6ff,#e0f2fe)",
         money="linear-gradient(135deg,#fff1f2,#ffe4e6)", health="linear-gradient(135deg,#fef2f2,#fee2e2)")

SIMS = []
def sim(**kw): SIMS.append(kw)

WIKI_FILTER_JS = """  const NG = ['メインページ','特別:','Wikipedia:','ファイル:','Help:','Portal:','テンプレート:','ノート:','プロジェクト:','Category:'];
  const okTitle = (t) => t && !NG.some(n => t.startsWith(n));
  const dstr = (d) => d.getFullYear() + '/' + String(d.getMonth()+1).padStart(2,'0') + '/' + String(d.getDate()).padStart(2,'0');
  const dnum = (d) => d.getFullYear() + String(d.getMonth()+1).padStart(2,'0') + String(d.getDate()).padStart(2,'0');"""

# ---------- 1 きのう日本人が一番調べたもの ----------
sim(slug="kyou-no-kanshin", cat="wonder", catjp="ふしぎ・現象", grad=G["wonder"], emoji="📰",
    title="きのう、日本人が一番調べたもの", score=66,
    card_desc="昨日、日本中がWikipediaで一番調べた言葉は？閲覧数ランキングをライブ表示。",
    title_tag="きのう、日本人が一番調べたもの｜Wikipedia閲覧数ランキングをライブ表示",
    meta_desc="昨日日本中がWikipediaで最も調べた記事のランキングを、Wikimedia公式の閲覧統計からライブ表示する無料ツール。ニュースより正直な「世間の関心事」が分かる。",
    og_title="きのう、日本人が一番調べたもの", og_desc="Wikipedia閲覧数ランキングで世間の関心をライブ観測。",
    lead="テレビの「話題」はつくれますが、検索は正直です。昨日、日本中がWikipediaで一番読んだ記事のランキングを表示します。",
    about_h2="このランキングについて",
    about="""<p>Wikipediaを運営するWikimedia財団は、全記事の閲覧数統計を公式APIで公開しています。このツールは日本語版Wikipediaの日次閲覧ランキングを取得し、システムページを除いた「人々が本当に調べた記事」のトップを表示します。事件・訃報・ドラマの放送——世間の関心が数字でそのまま見えるため、「なぜこれが1位？」から昨日のニュースを逆引きする遊び方もできます。</p>
    <div class="note">集計は世界中からの日本語版アクセス合計です。統計の反映に1〜2日かかるため「昨日〜一昨日」のデータを表示しています。</div>""",
    faqs=[("データの出典は？", "Wikimedia財団公式の閲覧統計API（Pageviews API）から、日本語版Wikipediaの日次ランキングを取得しています。"),
          ("リアルタイムの検索ランキング？", "Wikipediaの閲覧数ベースなので、Google検索とは母数が異なりますが、傾向はよく一致します。反映まで1〜2日のタイムラグがあります。"),
          ("入力データは送信される？", "このページは何も入力せずに使えます。")],
    rel=[("docchi-yumei","🥊","どっちが有名？対決"),("kotoba-trend","📈","その言葉、まだ流行ってる？"),("tanjobi-jiken","🎂","あなたの誕生日、何が起きた日？"),("jishin-live","🗾","日本はいまも揺れている")],
    body="""  <section class="panel" id="resultPanel">
    <div class="result">
      <div class="label" id="topLabel">きのう、日本人が一番調べたのは</div>
      <div class="big" style="font-size:min(11vw,50px);"><span id="big">–</span></div>
      <div class="sub" id="sub">データを読み込み中…</div>
      <div class="statline"><div class="stat"><div class="k">1位の閲覧数</div><div class="v" id="v1">—</div></div>
      <div class="stat"><div class="k">2位</div><div class="v" id="v2">—</div></div>
      <div class="stat"><div class="k">3位</div><div class="v" id="v3">—</div></div></div>
      <div id="list" style="margin-top:14px;"></div>
      <button class="btn btn-ghost" id="reloadBtn" style="margin-top:10px;">🔄 最新に更新</button>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
@@WIKI_FILTER_JS@@
  async function load(){
    $('sub').textContent = 'データを読み込み中…';
    try{
      let items = null, used = null;
      for(let back = 2; back <= 4; back++){
        const d = new Date(Date.now() - back * 86400000);
        const r = await fetch('https://wikimedia.org/api/rest_v1/metrics/pageviews/top/ja.wikipedia/all-access/' + dstr(d));
        if(r.ok){ const j = await r.json(); items = j.items[0].articles; used = d; break; }
      }
      if(!items){ $('sub').textContent = '統計が取得できませんでした。'; return; }
      const arts = items.map(a => ({ t: a.article.replace(/_/g,' '), v: a.views })).filter(a => okTitle(a.t)).slice(0, 20);
      $('big').textContent = '「' + arts[0].t + '」';
      $('sub').textContent = (used.getMonth()+1) + '/' + used.getDate() + 'の日本語版Wikipedia閲覧数（Wikimedia公式統計）';
      $('v1').textContent = arts[0].v.toLocaleString('ja-JP') + '回';
      $('v2').textContent = arts[1].t;
      $('v3').textContent = arts[2].t;
      $('list').innerHTML = '<div style="font-weight:800;font-size:13px;margin-bottom:8px;">📋 TOP15</div>' + arts.slice(0,15).map((a,i) =>
        '<div style="display:flex;gap:8px;justify-content:space-between;padding:7px 10px;margin-bottom:5px;background:rgba(127,127,127,.07);border-radius:8px;font-size:12.5px;text-align:left;">'
        + '<span>' + (i+1) + '位　' + a.t + '</span><span style="opacity:.7;white-space:nowrap;">' + (a.v/10000).toFixed(1) + '万回</span></div>').join('');
      SHARE = 'きのう日本人がWikipediaで一番調べたのは「' + arts[0].t + '」（' + (arts[0].v/10000).toFixed(1) + '万回）📰 2位は' + arts[1].t + '。\\n世間の関心ランキングはこちら👇';
    }catch{ $('sub').textContent = '⚠️ 取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  load();
  $('reloadBtn').addEventListener('click', load);
  bindShare();
})();""")

# ---------- 2 どっちが有名？対決 ----------
sim(slug="docchi-yumei", cat="play", catjp="あそぶ・実験", grad=G["play"], emoji="🥊",
    title="どっちが有名？対決", score=65,
    card_desc="きのこの山vsたけのこの里、実際どっちが注目されてる？閲覧数データでガチ判定。",
    title_tag="どっちが有名？対決｜Wikipedia閲覧数で2つの言葉をガチ比較",
    meta_desc="2つの言葉・人物・作品を入力すると、直近60日のWikipedia閲覧数でどちらが注目されているかをガチ判定する無料ツール。推し対決・雑談の決着に。",
    og_title="どっちが有名？対決", og_desc="Wikipedia閲覧数データで2つの言葉をガチ比較。",
    lead="「どっちが有名か」論争に、データで決着をつけます。2つの言葉を入れると、直近60日のWikipedia閲覧数で勝敗を判定します。",
    about_h2="この対決について",
    about="""<p>知名度の議論は水掛け論になりがちですが、Wikipediaの閲覧数は「実際に調べた人の数」という動かぬ証拠です。このツールはWikimedia公式統計APIから両者の直近60日の閲覧数を合計して比較します。人物対決、作品対決、うどんvsそば——あらゆる論争にどうぞ。</p>
    <div class="note">Wikipediaの記事名と完全一致で検索します。ヒットしない場合は正式名称（例:「大谷翔平」「きのこの山」）でお試しください。</div>""",
    faqs=[("データの出典は？", "Wikimedia財団公式の閲覧統計API（Pageviews API）から、日本語版Wikipediaの記事別閲覧数を取得しています。"),
          ("記事が見つからないと言われる", "Wikipediaの記事名と完全一致している必要があります。正式名称・フルネームでお試しください。"),
          ("入力データは送信される？", "入力した言葉はWikipedia統計APIへの問い合わせにだけ使われます。")],
    rel=[("kyou-no-kanshin","📰","きのう、日本人が一番調べたもの"),("kotoba-trend","📈","その言葉、まだ流行ってる？"),("catchcopy","🎪","うさんくさいキャッチコピー製造機"),("aisho-name","💞","名前で相性占い")],
    body="""  <section class="panel">
    <h2>🥊 対戦カード</h2>
    <div class="field"><label>赤コーナー</label><input type="text" id="w1" placeholder="例: きのこの山" autocomplete="off"></div>
    <div class="field"><label>青コーナー</label><input type="text" id="w2" placeholder="例: たけのこの里" autocomplete="off"></div>
    <button class="btn btn-primary" id="calcBtn">ゴングを鳴らす</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label">直近60日の注目度、勝者は</div>
      <div class="big" style="font-size:min(11vw,50px);"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k" id="n1">赤</div><div class="v" id="s1">—</div></div>
      <div class="stat"><div class="k" id="n2">青</div><div class="v" id="s2">—</div></div>
      <div class="stat"><div class="k">差</div><div class="v accent" id="ratio">—</div></div></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
@@WIKI_FILTER_JS@@
  async function views(word){
    const end = new Date(Date.now() - 3 * 86400000), start = new Date(Date.now() - 63 * 86400000);
    const r = await fetch('https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/ja.wikipedia/all-access/all-agents/' + encodeURIComponent(word.replace(/ /g,'_')) + '/daily/' + dnum(start) + '/' + dnum(end));
    if(!r.ok) return null;
    const j = await r.json();
    return j.items.reduce((a,b) => a + b.views, 0);
  }
  async function calc(){
    const w1 = $('w1').value.trim(), w2 = $('w2').value.trim();
    if(!w1 || !w2){ $('state').textContent = '両方のコーナーに言葉を入れてください。'; return; }
    $('state').textContent = '閲覧数データを集計中…';
    try{
      const [v1, v2] = await Promise.all([views(w1), views(w2)]);
      if(v1 == null || v2 == null){
        $('state').textContent = '⚠️「' + (v1 == null ? w1 : w2) + '」のWikipedia記事が見つかりません。正式名称でお試しください。';
        return;
      }
      const win = v1 >= v2 ? w1 : w2;
      const ratio = Math.max(v1, v2) / Math.max(1, Math.min(v1, v2));
      $('state').textContent = '';
      $('big').textContent = '🏆 ' + win;
      $('sub').textContent = '直近60日の日本語版Wikipedia閲覧数（Wikimedia公式統計）';
      $('n1').textContent = w1; $('n2').textContent = w2;
      $('s1').textContent = (v1/10000).toFixed(1) + '万回';
      $('s2').textContent = (v2/10000).toFixed(1) + '万回';
      $('ratio').textContent = ratio < 1.15 ? 'ほぼ互角！' : ratio.toFixed(1) + '倍差';
      SHARE = '【どっちが有名？対決】' + w1 + ' vs ' + w2 + ' → 勝者「' + win + '」🥊（直近60日の閲覧数 ' + (v1/10000).toFixed(1) + '万 vs ' + (v2/10000).toFixed(1) + '万）\\nあなたの推し対決も👇';
      show();
    }catch{ $('state').textContent = '⚠️ 集計に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  bindShare();
})();""")

# ---------- 3 その言葉、まだ流行ってる？ ----------
sim(slug="kotoba-trend", cat="marketing", catjp="マーケティング", grad=G["marketing"], emoji="📈",
    title="その言葉、まだ流行ってる？", score=64,
    card_desc="話題のあの言葉、実は下火かも。半年分の閲覧数データでトレンドの生死を判定。",
    title_tag="その言葉、まだ流行ってる？｜半年の閲覧数データでトレンド判定",
    meta_desc="言葉・人物・作品名を入れると、直近半年のWikipedia閲覧数の推移から「上昇中か下火か」を判定する無料ツール。企画・ネタ選び・トレンド調査の一次データに。",
    og_title="その言葉、まだ流行ってる？", og_desc="半年の閲覧数推移でトレンドの生死を判定。",
    lead="「いま流行ってるらしい」の裏を取ります。言葉を入れると、半年分の閲覧数推移からトレンドが上昇中か下火かを判定します。",
    about_h2="この判定について",
    about="""<p>マーケティングでも雑談でも、「流行っている」の根拠は大抵ふわっとしています。このツールはWikimedia公式統計から対象記事の約半年分の日次閲覧数を取得し、直近30日と半年前の水準を比較してトレンドを判定します。企画書に「まだ伸びている」「もうピークは過ぎた」の一次データを添えたいときにも。</p>
    <div class="note">閲覧数はニュース露出で瞬間的に跳ねます。ピーク日が突出している場合は、一発ニュース型か定着型かをグラフの形で見分けてください。</div>""",
    faqs=[("データの出典は？", "Wikimedia財団公式の閲覧統計API（Pageviews API）から、日本語版Wikipediaの記事別日次閲覧数を取得しています。"),
          ("Googleトレンドとの違いは？", "母数は違いますが傾向は概ね一致します。こちらはAPIで即取得でき、具体的な閲覧回数で比較できるのが利点です。"),
          ("入力データは送信される？", "入力した言葉はWikipedia統計APIへの問い合わせにだけ使われます。")],
    rel=[("kyou-no-kanshin","📰","きのう、日本人が一番調べたもの"),("docchi-yumei","🥊","どっちが有名？対決"),("influencer-soroban","📱","インフルエンサー皮算用"),("kuchikomi-hakyu","📣","口コミ波及シミュレーター")],
    body="""  <section class="panel">
    <h2>📈 調べる言葉</h2>
    <div class="field"><label>言葉・人物・作品名 <span class="hint">（Wikipedia記事名と一致）</span></label><input type="text" id="w" placeholder="例: 生成的人工知能" autocomplete="off"></div>
    <button class="btn btn-primary" id="calcBtn">トレンドの生死を判定</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label" id="topLabel">判定</div>
      <div class="big" style="font-size:min(12vw,54px);"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">直近30日の平均/日</div><div class="v" id="recent">—</div></div>
      <div class="stat"><div class="k">半年前の平均/日</div><div class="v" id="old">—</div></div>
      <div class="stat"><div class="k">この半年のピーク</div><div class="v accent" id="peak">—</div></div></div>
      <div id="chart" style="margin-top:14px;display:flex;align-items:flex-end;gap:1px;height:70px;"></div>
      <div class="hint">▲ 直近180日の日次閲覧数</div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
@@WIKI_FILTER_JS@@
  async function calc(){
    const w = $('w').value.trim();
    if(!w){ $('w').focus(); return; }
    $('state').textContent = '半年分の閲覧数を取得中…';
    try{
      const end = new Date(Date.now() - 3 * 86400000), start = new Date(Date.now() - 183 * 86400000);
      const r = await fetch('https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/ja.wikipedia/all-access/all-agents/' + encodeURIComponent(w.replace(/ /g,'_')) + '/daily/' + dnum(start) + '/' + dnum(end));
      if(!r.ok){ $('state').textContent = '⚠️「' + w + '」のWikipedia記事が見つかりません。正式名称でお試しください。'; return; }
      const j = await r.json();
      const vs = j.items.map(x => x.views);
      const avg = (a) => a.reduce((x,y)=>x+y,0) / Math.max(1, a.length);
      const recent = avg(vs.slice(-30)), old = avg(vs.slice(0, 30));
      const chg = (recent / Math.max(1, old) - 1) * 100;
      let peakI = 0; vs.forEach((v,i) => { if(v > vs[peakI]) peakI = i; });
      const peakDate = j.items[peakI].timestamp;
      const verdict = chg >= 100 ? '🔥 爆伸び中' : chg >= 25 ? '📈 上昇トレンド' : chg >= -25 ? '➡️ 横ばい（定着期）' : chg >= -60 ? '📉 下火になりつつある' : '🧊 ブーム終了…';
      $('state').textContent = '';
      $('big').textContent = verdict;
      $('sub').textContent = '「' + w + '」半年前比 ' + (chg >= 0 ? '+' : '') + chg.toFixed(0) + '%（日本語版Wikipedia閲覧数）';
      $('recent').textContent = Math.round(recent).toLocaleString('ja-JP') + '回';
      $('old').textContent = Math.round(old).toLocaleString('ja-JP') + '回';
      $('peak').textContent = peakDate.slice(4,6).replace(/^0/,'') + '/' + peakDate.slice(6,8).replace(/^0/,'') + '（' + (vs[peakI]/10000).toFixed(1) + '万回）';
      const mx = Math.max(...vs);
      $('chart').innerHTML = vs.map(v => '<div style="flex:1;background:linear-gradient(180deg,#6366f1,#818cf8);border-radius:1px 1px 0 0;height:' + Math.max(2, v / mx * 100) + '%"></div>').join('');
      SHARE = '「' + w + '」のトレンド判定 → ' + verdict + '（半年前比' + (chg>=0?'+':'') + chg.toFixed(0) + '%）📈 Wikipedia閲覧数の一次データより\\nあなたの気になる言葉は？👇';
      show();
    }catch{ $('state').textContent = '⚠️ 集計に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  bindShare();
})();""")

# ---------- 4 温暖化体感 ----------
sim(slug="ondanka-taikan", cat="wonder", catjp="ふしぎ・現象", grad=G["wonder"], emoji="🥵",
    title="あなたの街、40年でこれだけ暑くなった", score=63,
    card_desc="1980年代の夏と、いまの夏。実測データ40年分で「体感してる温暖化」を数字に。",
    title_tag="あなたの街、40年でこれだけ暑くなった｜実測40年の夏を比較",
    meta_desc="1984〜88年と2020〜24年の夏の実測気象データ（ERA5）を比較して、あなたの街が40年でどれだけ暑くなったかを表示する無料ツール。真夏日の日数変化も。",
    og_title="あなたの街、40年でこれだけ暑くなった", og_desc="実測データ40年分で温暖化を体感する。",
    lead="「昔の夏はこんなに暑くなかった」——記憶ではなく、実測データで確かめます。1980年代の夏といまの夏を、同じ物差しで比較します。",
    about_h2="この比較について",
    about="""<p>この比較は、気象再解析データERA5（過去アーカイブAPI経由）から1984〜88年と2020〜24年の各5年分・7〜8月の日最高気温を取得し、平均気温と真夏日（30℃以上）日数を並べたものです。未来予測ではなく、すでに起きた変化の実測です。<a href="../natsu-2050/">2050年の夏</a>とあわせて見ると、この変化がまだ途中経過であることが分かります。</p>
    <div class="note">広域グリッドの平均のため都市の観測点より低めに出ますが、同一手法同士の比較なので「差」は意味を持ちます。都市化（ヒートアイランド）の影響も差に含まれます。</div>""",
    faqs=[("データの出典は？", "気象再解析データERA5（Open-Meteo Historical Weather API経由）の日最高気温を使用しています。"),
          ("温暖化だけの影響？", "いいえ。都市部では地球温暖化に都市化（ヒートアイランド）の影響が上乗せされています。表示する差はその合計です。"),
          ("入力データは送信される？", "地域の選択のみを使います。個人情報は一切送信されません。")],
    rel=[("natsu-2050","🔥","2050年の夏、何度になる？"),("atsusa-ranking","🌡️","全国いま暑いランキング"),("umareta-hi-tenki","👶","生まれた日の天気"),("nettaiya-check","🌙","今夜、熱帯夜？チェック")],
    body="""  <section class="panel">
    <h2>🥵 条件</h2>
    <div class="field"><label>地域</label><select id="pref"></select></div>
    <button class="btn btn-primary" id="calcBtn">40年の変化を見る</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label">あなたの街の夏は、40年で</div>
      <div class="big">+<span id="big">0</span><span class="unit">℃</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1980年代の夏</div><div class="v" id="old">—</div></div>
      <div class="stat"><div class="k">いまの夏（2020〜24）</div><div class="v" id="now">—</div></div>
      <div class="stat"><div class="k">真夏日（30℃以上）</div><div class="v accent" id="manatsu">—</div></div></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
@@PREFS_JS@@
  function summer(daily){
    const t = daily.time, v = daily.temperature_2m_max;
    let sum = 0, cnt = 0, hot = 0;
    for(let i = 0; i < t.length; i++){
      const mo = +t[i].slice(5,7);
      if((mo === 7 || mo === 8) && v[i] != null){ sum += v[i]; cnt++; if(v[i] >= 30) hot++; }
    }
    return { avg: sum / cnt, hot: hot / 5 };
  }
  async function calc(){
    const p = PREFS[+$('pref').value];
    $('state').textContent = '40年分の実測データを取得中…（数秒かかります）';
    try{
      const url = (a, b) => 'https://archive-api.open-meteo.com/v1/archive?latitude=' + p[1] + '&longitude=' + p[2] + '&start_date=' + a + '&end_date=' + b + '&daily=temperature_2m_max&timezone=Asia%2FTokyo';
      const [o, n] = await Promise.all([
        fetch(url('1984-01-01','1988-12-31')).then(r => r.json()),
        fetch(url('2020-01-01','2024-12-31')).then(r => r.json()),
      ]);
      const a = summer(o.daily), b = summer(n.daily);
      const diff = b.avg - a.avg;
      $('state').textContent = '';
      $('sub').textContent = p[0] + '｜1984〜88年 vs 2020〜24年の7〜8月・日最高気温の実測比較（ERA5）';
      $('old').textContent = a.avg.toFixed(1) + '℃';
      $('now').textContent = b.avg.toFixed(1) + '℃';
      $('manatsu').textContent = a.hot.toFixed(0) + '日/年 → ' + b.hot.toFixed(0) + '日/年';
      SHARE = '実測データによると、' + p[0].split('(')[0] + 'の夏は40年で+' + diff.toFixed(1) + '℃暑くなってた🥵 真夏日は年' + a.hot.toFixed(0) + '日→' + b.hot.toFixed(0) + '日に。記憶は正しかった。\\nあなたの街の40年は？👇';
      show(); anim($('big'), 0, Math.round(diff * 10) / 10, 1000, 1);
    }catch{ $('state').textContent = '⚠️ 取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  bindShare();
})();""")

# ---------- 5 犬の散歩OK？ ----------
sim(slug="inu-sanpo-ok", cat="pet", catjp="ペット", grad=G["pet"], emoji="🐕",
    title="いま、犬の散歩できる？", score=62,
    card_desc="夏のアスファルトは60℃になる。いまの推定路面温度から肉球やけどリスクを判定。",
    title_tag="いま、犬の散歩できる？｜推定路面温度で肉球やけどリスクを判定",
    meta_desc="いまの気温と日射量から夏のアスファルトの推定路面温度を計算し、犬の散歩をしていいか・肉球やけどのリスクを判定する無料ツール。おすすめの散歩時間帯も表示。",
    og_title="いま、犬の散歩できる？", og_desc="推定路面温度で肉球やけどリスクを判定。",
    lead="気温30℃の日、日なたのアスファルトは60℃近くになります。いまの気温と日差しから路面温度を推定して、散歩に出ていいかを判定します。",
    about_h2="この判定について",
    about="""<p>犬の肉球は路面に直接触れるため、真夏の散歩でやけどを負う事故が毎年起きています。アスファルトは日射を吸収して気温より20℃以上熱くなることがあり、このツールは気象オープンデータAPI（Open-Meteo）のいまの気温と日射量から路面温度を推定します。目安として路面55℃以上は数十秒でやけどの危険、45℃以上も要注意です。</p>
    <div class="note">出る前の最終確認は「手の甲を路面に5秒つけられるか」のアナログ最強テストで。5秒耐えられなければ、犬の散歩はまだ早いです。</div>""",
    faqs=[("路面温度はどう推定している？", "気象オープンデータAPI（Open-Meteo）の気温と日射量から、日なたのアスファルトの温度を推定式で概算しています（日射1kW/m²あたり約+22℃）。実測ではありません。"),
          ("何℃なら散歩していい？", "推定路面35℃未満が目安です。夏場は早朝5〜7時か、日没1時間後以降が安全圏になることが多いです。"),
          ("入力データは送信される？", "地域の選択のみを使います。個人情報は一切送信されません。")],
    rel=[("sanpo","🐾","犬の散歩 生涯距離シミュレーター"),("hiyake-timer","☀️","日焼けタイマー"),("nettaiya-check","🌙","今夜、熱帯夜？チェック"),("atsusa-ranking","🌡️","全国いま暑いランキング")],
    body="""  <section class="panel">
    <h2>🐕 条件</h2>
    <div class="field"><label>地域</label><select id="pref"></select></div>
    <button class="btn btn-primary" id="calcBtn">いまの路面を判定</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label">いまの推定路面温度は</div>
      <div class="big"><span id="big">0</span><span class="unit">℃</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">いまの気温</div><div class="v" id="temp">—</div></div>
      <div class="stat"><div class="k">判定</div><div class="v" id="judge">—</div></div>
      <div class="stat"><div class="k">今日のおすすめ散歩時間</div><div class="v accent" id="best">—</div></div></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
@@PREFS_JS@@
  const road = (t, r) => t + (r || 0) / 1000 * 22;
  async function calc(){
    const p = PREFS[+$('pref').value];
    $('state').textContent = '気温と日差しを取得中…';
    try{
      const r = await fetch('https://api.open-meteo.com/v1/forecast?latitude=' + p[1] + '&longitude=' + p[2] + '&hourly=temperature_2m,shortwave_radiation&forecast_days=1&timezone=Asia%2FTokyo');
      const j = await r.json();
      const T = j.hourly.temperature_2m, R = j.hourly.shortwave_radiation;
      const H = new Date().getHours();
      const rt = road(T[H], R[H]);
      const judge = rt >= 55 ? '🟥 肉球やけど危険。散歩NG' : rt >= 45 ? '🟧 危険。日陰でも短時間で' : rt >= 35 ? '🟨 注意。日陰ルート推奨' : '🟢 散歩OK！';
      const goodHours = [];
      for(let h = 4; h <= 23; h++){ if(road(T[h], R[h]) < 35) goodHours.push(h); }
      let bestTxt = '終日OK';
      if(goodHours.length === 0) bestTxt = '今日は室内推奨…';
      else if(goodHours.length < 20){
        const am = goodHours.filter(h => h < 12), pm = goodHours.filter(h => h >= 12);
        bestTxt = (am.length ? '朝' + am[0] + '〜' + (am[am.length-1]+1) + '時' : '') + (am.length && pm.length ? ' / ' : '') + (pm.length ? pm[0] + '時以降' : '');
      }
      $('state').textContent = '';
      $('sub').textContent = p[0] + '・' + H + '時（日なたのアスファルト推定）｜' + judge;
      $('temp').textContent = T[H].toFixed(1) + '℃';
      $('judge').textContent = judge.replace(/^[^ ]+ /, '');
      $('best').textContent = bestTxt;
      SHARE = 'いまの' + p[0].split('(')[0] + '、日なたの路面は推定' + Math.round(rt) + '℃🐕（' + judge.replace(/^[^ ]+ /,'') + '）今日の散歩どきは「' + bestTxt + '」\\n愛犬家はチェック👇';
      show(); anim($('big'), 0, Math.round(rt), 900);
    }catch{ $('state').textContent = '⚠️ 取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  bindShare();
})();""")

# ---------- 6 ランニング指数 ----------
sim(slug="running-shisu", cat="sports", catjp="スポーツ・運動", grad=G["sports"], emoji="🏃",
    title="いま走っていい？ランニング指数", score=61,
    card_desc="気温・湿度・紫外線・PM2.5をまとめて判定。今日のベストなラン時間帯も。",
    title_tag="いま走っていい？ランニング指数｜気温・湿度・UV・PM2.5を総合判定",
    meta_desc="いまの気温・湿度・紫外線・PM2.5をリアルタイムに総合して、ランニングに適しているかを0〜100で判定する無料ツール。今日のベストなラン時間帯も表示。",
    og_title="いま走っていい？ランニング指数", og_desc="気温・湿度・UV・PM2.5をまとめてラン判定。",
    lead="走れる空気かどうかは、気温だけでは決まりません。湿度・紫外線・PM2.5までまとめて取得して、いまのラン適性を採点します。",
    about_h2="この指数について",
    about="""<p>ランニングの快適さとリスクは「気温×湿度」（熱中症）、「紫外線」（日焼け）、「PM2.5」（呼吸器負荷）の掛け算で決まります。この指数は気象オープンデータAPI（Open-Meteo）の気象・大気質データを同時取得し、暑熱の負荷を中心に0〜100で採点します。夏は指数が高くなる早朝・夜間がおすすめになります。</p>
    <div class="note">心疾患・喘息などがある方は数値にかかわらず主治医の指導を優先してください。給水はどの指数でも必須です。</div>""",
    faqs=[("データの出典は？", "気象オープンデータAPI（Open-Meteo）の気温・湿度・UV指数と、同大気質API（CAMS）のPM2.5を使用しています。"),
          ("採点の考え方は？", "暑さ指数（気温と湿度の組み合わせ）を主軸に、紫外線とPM2.5で減点する方式です。医学的な安全保証ではありません。"),
          ("入力データは送信される？", "地域の選択のみを使います。個人情報は一切送信されません。")],
    rel=[("kuuki-kirei","🍃","空気きれいメーター"),("hiyake-timer","☀️","日焼けタイマー"),("nettaiya-check","🌙","今夜、熱帯夜？チェック"),("taiju","⚖️","半年後の体重シミュレーター")],
    body="""  <section class="panel">
    <h2>🏃 条件</h2>
    <div class="field"><label>地域</label><select id="pref"></select></div>
    <button class="btn btn-primary" id="calcBtn">いまのラン適性を採点</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label">いまのランニング指数は</div>
      <div class="big"><span id="big">0</span><span class="unit">/100</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">気温 / 湿度</div><div class="v" id="th">—</div></div>
      <div class="stat"><div class="k">UV / PM2.5</div><div class="v" id="up">—</div></div>
      <div class="stat"><div class="k">今日のベストラン時間</div><div class="v accent" id="best">—</div></div></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
@@PREFS_JS@@
  function scoreAt(t, h, uv, pm){
    let s = 100;
    const heat = t + (h - 50) * 0.1;
    if(heat > 18) s -= (heat - 18) * 4;
    if(t < 3) s -= (3 - t) * 4;
    if(uv >= 6) s -= (uv - 6) * 4;
    if(pm >= 35) s -= Math.min(30, (pm - 35));
    return Math.max(0, Math.round(s));
  }
  async function calc(){
    const p = PREFS[+$('pref').value];
    $('state').textContent = '気象と大気質を取得中…';
    try{
      const [w, a] = await Promise.all([
        fetch('https://api.open-meteo.com/v1/forecast?latitude=' + p[1] + '&longitude=' + p[2] + '&hourly=temperature_2m,relative_humidity_2m,uv_index&forecast_days=1&timezone=Asia%2FTokyo').then(r => r.json()),
        fetch('https://air-quality-api.open-meteo.com/v1/air-quality?latitude=' + p[1] + '&longitude=' + p[2] + '&hourly=pm2_5&forecast_days=1&timezone=Asia%2FTokyo').then(r => r.json()),
      ]);
      const H = new Date().getHours();
      const T = w.hourly.temperature_2m, RH = w.hourly.relative_humidity_2m, UV = w.hourly.uv_index, PM = a.hourly.pm2_5;
      const s = scoreAt(T[H], RH[H], UV[H], PM[H] ?? 0);
      let bestH = 5, bestS = -1;
      for(let h = 4; h <= 23; h++){ const x = scoreAt(T[h], RH[h], UV[h], PM[h] ?? 0); if(x > bestS){ bestS = x; bestH = h; } }
      const label = s >= 80 ? '快走日和！🏃' : s >= 60 ? 'ぼちぼち走れる' : s >= 40 ? '無理せず短めに' : '今は控えて別の時間に';
      $('state').textContent = '';
      $('sub').textContent = p[0] + '・' + H + '時｜' + label;
      $('th').textContent = T[H].toFixed(1) + '℃ / ' + Math.round(RH[H]) + '%';
      $('up').textContent = 'UV' + (UV[H] ?? 0).toFixed(1) + ' / ' + Math.round(PM[H] ?? 0) + 'μg';
      $('best').textContent = bestH + '時ごろ（指数' + bestS + '）';
      SHARE = 'いまの' + p[0].split('(')[0] + 'のランニング指数は' + s + '/100🏃（' + label + '）今日のベストは' + bestH + '時。\\nあなたの街は？👇';
      show(); anim($('big'), 0, s, 900);
    }catch{ $('state').textContent = '⚠️ 取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  bindShare();
})();""")

# ---------- 7 神社とお寺どっちが多い街 ----------
sim(slug="jinja-tera", cat="home", catjp="住まい・暮らし", grad=G["home"], emoji="⛩️",
    title="神社とお寺、どっちが多い街？", score=60,
    card_desc="あなたの街は神社派？お寺派？半径2kmの寺社を地図データからライブ集計。",
    title_tag="神社とお寺、どっちが多い街？｜半径2kmの寺社を地図データで集計",
    meta_desc="住所や地名を入れると、半径2km圏内の神社とお寺の数を世界最大の地図データベースからライブ集計して「神社の街かお寺の街か」を判定する無料ツール。散歩・御朱印巡りにも。",
    og_title="神社とお寺、どっちが多い街？", og_desc="半径2kmの寺社を地図データでライブ集計。",
    lead="日本には神社が約8万、お寺が約7万7千。ではあなたの街はどっち派？半径2kmの寺社を地図データから数えます。",
    about_h2="この集計について",
    about="""<p>全国の神社（約8万社）とお寺（約7万7千ヶ寺）は、コンビニ（約5万7千店）より多い——日本の風景の基本装備です。このツールは国土地理院の住所検索で場所を特定し、OpenStreetMapに登録された宗教施設を半径2kmで取得して、神道・仏教の内訳を数えます。城下町はお寺が、港町や旧街道は神社が多いなど、街の成り立ちが数字ににじみます。</p>
    <div class="note">OpenStreetMapは有志更新のため、小さな祠やお堂は未登録のことがあります。実数はこれより多いのが普通です。</div>""",
    faqs=[("データの出典は？", "OpenStreetMap（Overpass API）の宗教施設データと、国土地理院の住所検索APIを利用しています。"),
          ("数が少なく感じる", "地図データベース未登録の小さな祠・お堂は数えられません。「登録済みだけでこれだけある」とお考えください。"),
          ("入力した住所は保存される？", "いいえ。検索と集計のAPI問い合わせだけに使い、保存はしません。")],
    rel=[("conbini-mitsudo","🏪","コンビニ密度チェッカー"),("kaibatsu-check","⛰️","うちの海抜チェッカー"),("unmei","💘","運命の人に出会う確率"),("goshugi-souba","💐","ご祝儀・香典の相場シミュレーター")],
    body="""  <section class="panel">
    <h2>⛩️ 場所をえらぶ</h2>
    <div class="field"><label>住所・地名 <span class="hint">（例: 京都市東山区 ※市区町村から入れると正確）</span></label><input type="text" id="q" placeholder="住所を入力" autocomplete="off"></div>
    <button class="btn btn-primary" id="searchBtn">寺社を数える</button>
    <div id="candBox" style="margin-top:10px;"></div>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label" id="placeLabel">この街は</div>
      <div class="big" style="font-size:min(12vw,54px);"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">⛩️ 神社</div><div class="v" id="jinja">—</div></div>
      <div class="stat"><div class="k">🙏 お寺</div><div class="v" id="tera">—</div></div>
      <div class="stat"><div class="k">その他・不明</div><div class="v accent" id="other">—</div></div></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
  async function count(lon, lat, placeName){
    $('state').textContent = '地図データから寺社を集計中…（数秒かかります）';
    try{
      const q = '[out:json][timeout:20];nwr["amenity"="place_of_worship"](around:2000,' + lat + ',' + lon + ');out tags;';
      const r = await fetch('https://overpass-api.de/api/interpreter?data=' + encodeURIComponent(q));
      const j = await r.json();
      let jinja = 0, tera = 0, other = 0;
      (j.elements || []).forEach(e => {
        const rel = (e.tags && e.tags.religion) || '';
        if(rel === 'shinto') jinja++;
        else if(rel === 'buddhist') tera++;
        else other++;
      });
      const verdict = jinja > tera ? '⛩️ 神社の街' : tera > jinja ? '🙏 お寺の街' : '⚖️ 五分五分の街';
      $('state').textContent = '';
      $('placeLabel').textContent = (placeName || 'この街') + 'は';
      $('big').textContent = verdict;
      $('sub').textContent = '半径2km・OpenStreetMap登録の宗教施設より';
      $('jinja').textContent = jinja + '社';
      $('tera').textContent = tera + 'ヶ寺';
      $('other').textContent = other + '件';
      SHARE = (placeName || 'うちの街') + 'は「' + verdict.replace(/^[^ ]+ /,'') + '」だった⛩️（神社' + jinja + ' vs お寺' + tera + '・半径2km）\\nあなたの街はどっち派？👇';
      show();
    }catch{ $('state').textContent = '⚠️ 集計に失敗しました（地図サーバー混雑の可能性）。少し待って再度お試しください。'; }
  }
  async function search(){
    const q = $('q').value.trim();
    if(!q){ $('q').focus(); return; }
    $('state').textContent = '住所を検索中…';
    $('candBox').innerHTML = '';
    try{
      const r = await fetch('https://msearch.gsi.go.jp/address-search/AddressSearch?q=' + encodeURIComponent(q));
      const list = await r.json();
      if(!list.length){ $('state').textContent = '見つかりませんでした。表記を変えてお試しください。'; return; }
      if(list.length === 1){ const c = list[0].geometry.coordinates; count(c[0], c[1], list[0].properties.title); return; }
      $('state').textContent = '候補から場所を選んでください。';
      $('candBox').innerHTML = list.slice(0,6).map((f,i) => '<button class="btn btn-ghost" style="margin:3px 0;width:100%;text-align:left;" data-i="' + i + '">📍 ' + f.properties.title + '</button>').join('');
      [...$('candBox').querySelectorAll('button')].forEach(b => b.addEventListener('click', () => {
        const f = list[+b.dataset.i];
        $('candBox').innerHTML = '';
        count(f.geometry.coordinates[0], f.geometry.coordinates[1], f.properties.title);
      }));
    }catch{ $('state').textContent = '⚠️ 住所検索に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('searchBtn').addEventListener('click', search);
  $('q').addEventListener('keydown', e => { if(e.key === 'Enter') search(); });
  bindShare();
})();""")

# ---------- 8 平年よりナンボ暑い ----------
sim(slug="heinen-hikaku", cat="season", catjp="季節・行事", grad=G["season"], emoji="📊",
    title="今日、平年よりナンボ暑い？", score=59,
    card_desc="ニュースの「平年より高い」を自分の街で。過去30年の同日データと今日を比較。",
    title_tag="今日、平年よりナンボ暑い？｜過去30年の同日実測と比較",
    meta_desc="今日の予想最高気温を、過去30年（1991〜2020年）の同じ日の実測データと比較して「平年よりどれだけ暑いか・過去30年で何位か」を表示する無料ツール。",
    og_title="今日、平年よりナンボ暑い？", og_desc="過去30年の同日データと今日をライブ比較。",
    lead="天気予報の「平年より高い」を、自分の街の数字で。過去30年の今日と同じ日の実測と、今日の予想を比べます。",
    about_h2="この比較について",
    about="""<p>「平年値」は直近30年（1991〜2020年）の平均です。このツールは気象アーカイブ（ERA5）からあなたの街の過去30年分・今日と同じ日付（前後3日を含む）の最高気温を取得して平年値を計算し、今日の予想最高気温と比較します。さらに「過去30年の同日で何位の暑さか」も表示するので、「今日ヤバい」の程度が客観的に分かります。</p>
    <div class="note">平年値は地点・計算方法で公式発表と多少ずれます。気象庁の公式平年値とは別物の「同一データ内での比較」としてお楽しみください。</div>""",
    faqs=[("データの出典は？", "過去はERA5再解析（アーカイブAPI）、今日は同じ提供元の予報値を使用しています。"),
          ("気象庁の平年値と違う？", "計算地点と手法が異なるため多少ずれます。同一データソース内で past と today を比べているので、差や順位の目安として有効です。"),
          ("入力データは送信される？", "地域の選択のみを使います。個人情報は一切送信されません。")],
    rel=[("atsusa-ranking","🌡️","全国いま暑いランキング"),("ondanka-taikan","🥵","あなたの街、40年でこれだけ暑くなった"),("kion-kandansa","🧣","寒暖差疲労チェッカー"),("umareta-hi-tenki","👶","生まれた日の天気")],
    body="""  <section class="panel">
    <h2>📊 条件</h2>
    <div class="field"><label>地域</label><select id="pref"></select></div>
    <button class="btn btn-primary" id="calcBtn">平年と比べる</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label">今日はあなたの街の平年より</div>
      <div class="big" style="font-size:min(13vw,58px);"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">今日の予想最高</div><div class="v" id="today">—</div></div>
      <div class="stat"><div class="k">平年値（1991〜2020）</div><div class="v" id="normal">—</div></div>
      <div class="stat"><div class="k">過去30年の同日と比べて</div><div class="v accent" id="rank">—</div></div></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
@@PREFS_JS@@
  async function calc(){
    const p = PREFS[+$('pref').value];
    $('state').textContent = '過去30年分のデータを取得中…（少し時間がかかります）';
    try{
      const [hist, today] = await Promise.all([
        fetch('https://archive-api.open-meteo.com/v1/archive?latitude=' + p[1] + '&longitude=' + p[2] + '&start_date=1991-01-01&end_date=2020-12-31&daily=temperature_2m_max&timezone=Asia%2FTokyo').then(r => r.json()),
        fetch('https://api.open-meteo.com/v1/forecast?latitude=' + p[1] + '&longitude=' + p[2] + '&daily=temperature_2m_max&forecast_days=1&timezone=Asia%2FTokyo').then(r => r.json()),
      ]);
      const now = new Date();
      const doy = (d) => { const s = new Date(d.getFullYear(), 0, 0); return Math.floor((d - s) / 86400000); };
      const target = doy(now);
      const times = hist.daily.time, vals = hist.daily.temperature_2m_max;
      const sameWindow = [], sameDay = [];
      for(let i = 0; i < times.length; i++){
        if(vals[i] == null) continue;
        const d = new Date(times[i] + 'T00:00:00');
        const diff = Math.abs(doy(d) - target);
        if(Math.min(diff, 365 - diff) <= 3) sameWindow.push(vals[i]);
        if(Math.min(diff, 365 - diff) === 0) sameDay.push(vals[i]);
      }
      const normal = sameWindow.reduce((a,b)=>a+b,0) / sameWindow.length;
      const tv = today.daily.temperature_2m_max[0];
      const diff = tv - normal;
      const hotter = sameDay.filter(v => v > tv).length;
      const rank = hotter + 1;
      $('state').textContent = '';
      $('big').textContent = (diff >= 0 ? '+' : '') + diff.toFixed(1) + '℃' + (diff >= 3 ? '🔥' : diff <= -3 ? '🧊' : '');
      $('sub').textContent = p[0] + '・今日の予想最高気温 vs 平年値（同日±3日の30年平均）';
      $('today').textContent = tv.toFixed(1) + '℃';
      $('normal').textContent = normal.toFixed(1) + '℃';
      $('rank').textContent = rank <= 3 ? '30年で' + rank + '番目の暑さ級🔥' : rank >= 28 ? '30年で' + (31 - rank) + '番目の涼しさ級' : '30年中' + rank + '位の暑さ';
      SHARE = '今日の' + p[0].split('(')[0] + 'は平年より' + (diff>=0?'+':'') + diff.toFixed(1) + '℃📊（過去30年の同日で' + rank + '位の暑さ）\\nあなたの街の「今日ヤバい度」は？👇';
      show();
    }catch{ $('state').textContent = '⚠️ 取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  bindShare();
})();""")

# ---------- 9 いまの雨雲マップ ----------
sim(slug="amagumo-now", cat="tool", catjp="便利ツール", grad=G["tool"], emoji="🌧️",
    title="いまの雨雲マップ", score=58,
    card_desc="日本列島のいまの雨雲をレーダー合成画像でさっと確認。10分ごと更新。",
    title_tag="いまの雨雲マップ｜日本列島の雨雲レーダーをさっと確認",
    meta_desc="日本列島全体のいまの雨雲を、世界の気象レーダー合成データ（RainViewer）と国土地理院地図を重ねてさっと確認できる無料ツール。約10分ごとに更新。",
    og_title="いまの雨雲マップ", og_desc="日本列島のいまの雨雲を1画面でさっと確認。",
    lead="アプリを開くまでもなく、雨雲の「いま」をさっと。世界の気象レーダー合成データを地理院地図に重ねて、日本列島をひと目で見わたします。",
    about_h2="このマップについて",
    about="""<p>このマップは、世界中の気象レーダーを合成配信しているRainViewerの雨雲タイルを、国土地理院の淡色地図に重ねたものです。観測は約10分ごとに更新され、青→緑→黄→赤の順に雨が強くなります。全国を1枚で見わたす設計なので、「西からくる雨のかたまり」の把握に向いています。</p>
    <div class="note">詳細なズームや予測アニメーションは気象庁「雨雲の動き」やお手元の天気アプリが得意です。ここは「開いた瞬間に全国が見える」ことに全振りしています。</div>""",
    faqs=[("データの出典は？", "雨雲はRainViewer（世界の気象レーダー合成・約10分更新）、背景地図は国土地理院の淡色地図タイルです。"),
          ("色の意味は？", "青→緑→黄→赤の順に降水が強くなります。赤はゲリラ豪雨クラスです。"),
          ("入力データは送信される？", "このページは何も入力せずに使えます。")],
    rel=[("kasa-iru","☔","今日、傘いる？メーター"),("kaminari-alert","⚡","今日の雷ゴロゴロ度"),("kyou-kaze","💨","今日、風ヤバい？チェッカー"),("shuumatsu-hare","🌤️","今週末、晴れる？")],
    body="""  <section class="panel" id="resultPanel">
    <div class="result">
      <div class="label">日本列島のいまの雨雲</div>
      <div class="sub" id="sub">レーダーを読み込み中…</div>
      <div id="map" style="position:relative;width:100%;max-width:512px;margin:12px auto 4px;aspect-ratio:2/3;border-radius:12px;overflow:hidden;background:#dde;"></div>
      <div class="hint">🟦 弱い雨 → 🟩 → 🟨 → 🟥 強い雨｜約10分ごと更新</div>
      <div class="statline" style="margin-top:10px;"><div class="stat"><div class="k">観測時刻</div><div class="v" id="obsTime">—</div></div>
      <div class="stat"><div class="k">データ</div><div class="v">世界レーダー合成</div></div>
      <div class="stat"><div class="k">背景地図</div><div class="v accent">国土地理院</div></div></div>
      <button class="btn btn-ghost" id="reloadBtn" style="margin-top:10px;">🔄 最新に更新</button>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
  const TILES = [];
  for(let y = 11; y <= 13; y++){ for(let x = 27; x <= 28; x++){ TILES.push([x, y]); } }
  async function load(){
    $('sub').textContent = 'レーダーを読み込み中…';
    try{
      const r = await fetch('https://api.rainviewer.com/public/weather-maps.json');
      const j = await r.json();
      const frame = j.radar.past[j.radar.past.length - 1];
      const map = $('map');
      map.innerHTML = TILES.map(([x, y]) => {
        const left = (x - 27) * 50, top = (y - 11) * (100 / 3);
        const base = 'position:absolute;left:' + left + '%;top:' + top + '%;width:50%;height:' + (100/3) + '%;';
        return '<img style="' + base + '" src="https://cyberjapandata.gsi.go.jp/xyz/pale/5/' + x + '/' + y + '.png" alt="">'
             + '<img style="' + base + 'opacity:.65;" src="' + j.host + frame.path + '/256/5/' + x + '/' + y + '/2/1_1.png" alt="">';
      }).join('');
      const t = new Date(frame.time * 1000);
      $('sub').textContent = '雨雲観測 ' + t.toLocaleTimeString('ja-JP', {hour:'2-digit',minute:'2-digit'}) + ' 時点';
      $('obsTime').textContent = t.toLocaleTimeString('ja-JP', {hour:'2-digit',minute:'2-digit'});
      SHARE = 'いまの日本列島の雨雲マップ🌧️（' + t.toLocaleTimeString('ja-JP',{hour:'2-digit',minute:'2-digit'}) + '観測）ワンタップで全国が見えるやつ👇';
    }catch{ $('sub').textContent = '⚠️ レーダーの取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  load();
  $('reloadBtn').addEventListener('click', load);
  bindShare();
})();""")

# ---------- 10 今日の潮 ----------
sim(slug="shio-live", cat="sports", catjp="スポーツ・運動", grad=G["sports"], emoji="🌊",
    title="今日の潮、いつ満ちる？", score=57,
    card_desc="釣り・潮干狩りの基本情報。今日の満潮・干潮の時刻をエリア別にライブ表示。",
    title_tag="今日の潮、いつ満ちる？｜満潮・干潮の時刻をエリア別ライブ表示",
    meta_desc="今日の満潮・干潮の時刻と潮位変化を、海洋予報データからエリア別に表示する無料ツール。釣り・潮干狩り・磯遊びの計画に。",
    og_title="今日の潮、いつ満ちる？", og_desc="満潮・干潮の時刻をエリア別にライブ表示。",
    lead="釣りも潮干狩りも、すべては潮まわりから。今日の満潮・干潮の時刻を、海洋予報データからエリア別に表示します。",
    about_h2="この潮時表について",
    about="""<p>このツールは海洋予報オープンデータAPI（Open-Meteo Marine）の潮位（海面高）予測から、今日の極大・極小＝満潮・干潮の時刻を割り出しています。潮が動く時間帯（満潮・干潮の前後）は魚の活性が上がり、干潮前後は潮干狩り・磯遊びの時間です。</p>
    <div class="note">数値モデルの推定のため、公式の潮汐表と時刻が前後することがあります。航海・業務用途は海上保安庁の潮汐表を必ず使用してください。</div>""",
    faqs=[("データの出典は？", "海洋予報オープンデータAPI（Open-Meteo Marine）の潮位（海面高）予測値から満潮・干潮を算出しています。"),
          ("公式の潮汐表と違う", "モデル推定のため多少ずれます。レジャーの目安にはなりますが、航海用途は海上保安庁の潮汐表を使用してください。"),
          ("入力データは送信される？", "エリアの選択のみを使います。個人情報は一切送信されません。")],
    rel=[("naminori-biyori","🏄","波乗り日和チェッカー"),("umi-mizuon","🏖️","いま海、冷たい？"),("hoshizora-shisu","🔭","今夜の星空指数"),("gasolin-doko","🛻","満タンでどこまで")],
    body="""  <section class="panel">
    <h2>🌊 エリア</h2>
    <div class="field"><label>海のエリア</label>
      <select id="spot">
        <option value="35.55,139.90" selected>東京湾（船橋・木更津方面）</option>
        <option value="35.30,139.48">湘南・相模湾</option>
        <option value="34.60,135.30">大阪湾</option>
        <option value="34.35,132.40">広島湾</option>
        <option value="33.60,130.30">博多湾</option>
        <option value="32.95,130.40">有明海</option>
        <option value="38.30,141.10">仙台湾</option>
        <option value="26.30,127.85">沖縄本島（中部）</option>
      </select>
    </div>
    <button class="btn btn-primary" id="calcBtn">今日の潮を見る</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label">次の満潮は</div>
      <div class="big" style="font-size:min(13vw,58px);"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">今日の満潮</div><div class="v" id="high">—</div></div>
      <div class="stat"><div class="k">今日の干潮</div><div class="v" id="low">—</div></div>
      <div class="stat"><div class="k">干満差</div><div class="v accent" id="range">—</div></div></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
  async function calc(){
    const [lat, lon] = $('spot').value.split(',');
    const name = $('spot').selectedOptions[0].textContent;
    $('state').textContent = '潮位データを取得中…';
    try{
      const r = await fetch('https://marine-api.open-meteo.com/v1/marine?latitude=' + lat + '&longitude=' + lon + '&hourly=sea_level_height_msl&forecast_days=2&timezone=Asia%2FTokyo');
      const j = await r.json();
      const S = j.hourly.sea_level_height_msl;
      const highs = [], lows = [];
      for(let h = 1; h < 47; h++){
        if(S[h] == null) continue;
        if(S[h] >= S[h-1] && S[h] > S[h+1]) highs.push(h);
        if(S[h] <= S[h-1] && S[h] < S[h+1]) lows.push(h);
      }
      const H = new Date().getHours();
      const fmtH = (h) => (h >= 24 ? '明日' + (h - 24) : h) + '時ごろ';
      const nextHigh = highs.find(h => h >= H);
      const todayHigh = highs.filter(h => h < 24), todayLow = lows.filter(h => h < 24);
      const mx = Math.max(...S.slice(0, 24).filter(v => v != null));
      const mn = Math.min(...S.slice(0, 24).filter(v => v != null));
      $('state').textContent = '';
      $('big').textContent = nextHigh != null ? fmtH(nextHigh) : '—';
      $('sub').textContent = name + '沖の潮位モデル推定｜レジャー用の目安（公式は海保の潮汐表）';
      $('high').textContent = todayHigh.length ? todayHigh.map(fmtH).join(' / ') : '—';
      $('low').textContent = todayLow.length ? todayLow.map(fmtH).join(' / ') : '—';
      $('range').textContent = '約' + Math.round((mx - mn) * 100) + 'cm';
      SHARE = '今日の' + name.split('（')[0] + '、満潮は' + (todayHigh.map(fmtH).join('と') || '—') + '・干潮は' + (todayLow.map(fmtH).join('と') || '—') + '🌊\\n釣り・潮干狩り前にチェック👇';
      show();
    }catch{ $('state').textContent = '⚠️ 取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  bindShare();
})();""")

# ---------- 11 予報の信頼度 ----------
sim(slug="yohou-shinrai", cat="tool", catjp="便利ツール", grad=G["tool"], emoji="🔮",
    title="週間予報、どこまで信じる？", score=56,
    card_desc="気象庁は予報に「信頼度A/B/C」を付けている。今週の怪しい日をあぶり出す。",
    title_tag="週間予報、どこまで信じる？｜気象庁の信頼度A/B/Cを見える化",
    meta_desc="気象庁が週間予報に付けている「信頼度（A/B/C）」を地域別に見える化する無料ツール。旅行や洗車の計画前に、予報の怪しい日をあぶり出せる。",
    og_title="週間予報、どこまで信じる？", og_desc="気象庁の信頼度A/B/Cで怪しい日をあぶり出す。",
    lead="実は気象庁は、週間予報に自信度（信頼度A/B/C）を付けて発表しています。今週の「怪しい日」をあぶり出します。",
    about_h2="この見える化について",
    about="""<p>気象庁の週間予報には、降水の有無の予報がどれだけ確からしいかを示す「信頼度」がA（確度高い）/B/C（確度低い）の3段階で付いています。天気マークは同じ「くもり時々雨」でも、AとCでは意味がまるで違う——このツールは気象庁の公開データから信頼度を取得してカレンダー化します。Cの日の予定は前日にもう一度確認を。</p>
    <div class="note">信頼度は5日先以降の日に付与されます。直近の日に「—」が出るのは、確度が高く信頼度表示の対象外だからです。</div>""",
    faqs=[("データの出典は？", "気象庁が公開している週間天気予報データ（信頼度・降水確率・天気コード）をそのまま取得しています。"),
          ("信頼度A/B/Cの意味は？", "降水の有無の予報の確からしさで、Aは適中率が高く予報が変わりにくい、Cは適中率が低く予報が変わりやすいことを示します。"),
          ("入力データは送信される？", "地域の選択のみを使います。個人情報は一切送信されません。")],
    rel=[("shuumatsu-hare","🌤️","今週末、晴れる？"),("kasa-iru","☔","今日、傘いる？メーター"),("tsugi-renkyuu","📅","次の3連休カウントダウン"),("amagumo-now","🌧️","いまの雨雲マップ")],
    body="""  <section class="panel">
    <h2>🔮 条件</h2>
    <div class="field"><label>地域</label>
      <select id="area">
        <option value="016000">北海道（石狩）</option><option value="040000">宮城県</option><option value="150000">新潟県</option>
        <option value="130000" selected>東京都</option><option value="230000">愛知県</option><option value="170000">石川県</option>
        <option value="270000">大阪府</option><option value="340000">広島県</option><option value="390000">高知県</option>
        <option value="400000">福岡県</option><option value="471000">沖縄本島</option>
      </select>
    </div>
    <button class="btn btn-primary" id="calcBtn">今週の信頼度を見る</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label">今週、予報が「怪しい日」は</div>
      <div class="big"><span id="big">0</span><span class="unit">日</span></div>
      <div class="sub" id="sub">—</div>
      <div id="list" style="margin-top:14px;"></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
  const WD = ['日','月','火','水','木','金','土'];
  async function calc(){
    const code = $('area').value;
    const name = $('area').selectedOptions[0].textContent;
    $('state').textContent = '気象庁データを取得中…';
    try{
      const r = await fetch('https://www.jma.go.jp/bosai/forecast/data/forecast/' + code + '.json');
      const j = await r.json();
      const weekly = j[1];
      const ts = weekly.timeSeries[0];
      const area = ts.areas[0];
      const rows = ts.timeDefines.map((t, i) => ({
        d: new Date(t),
        rel: (area.reliabilities || [])[i] || '',
        pop: ((weekly.timeSeries[1] && weekly.timeSeries[1].areas[0].pops) || [])[i] || '',
      }));
      const shaky = rows.filter(x => x.rel === 'C').length;
      $('state').textContent = '';
      $('sub').textContent = name + '・気象庁週間予報の信頼度（A=確度高い / C=変わりやすい）';
      $('list').innerHTML = rows.map(x => {
        const badge = x.rel === 'A' ? '🟢 A' : x.rel === 'B' ? '🟡 B' : x.rel === 'C' ? '🔴 C' : '—';
        return '<div style="display:flex;gap:8px;justify-content:space-between;padding:7px 10px;margin-bottom:5px;background:rgba(127,127,127,.07);border-radius:8px;font-size:12.5px;text-align:left;">'
          + '<span>' + (x.d.getMonth()+1) + '/' + x.d.getDate() + '(' + WD[x.d.getDay()] + ')' + (x.pop !== '' ? '　降水確率' + x.pop + '%' : '') + '</span><span>信頼度 ' + badge + '</span></div>';
      }).join('');
      SHARE = '今週の' + name + 'の週間予報、確度が低い「信頼度C」の日は' + shaky + '日🔮 予定はその日だけ前日再確認が吉。\\n気象庁の自信度、見える化はこちら👇';
      show(); anim($('big'), 0, shaky, 800);
    }catch{ $('state').textContent = '⚠️ 取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  bindShare();
})();""")

# ---------- 12 BBQ指数 ----------
sim(slug="bbq-shisu", cat="season", catjp="季節・行事", grad=G["season"], emoji="🍖",
    title="BBQ・ピクニック指数", score=55,
    card_desc="風・雨・暑さ・紫外線をまとめて屋外ごはん判定。炭火がつけやすい風速かも。",
    title_tag="BBQ・ピクニック指数｜風・雨・暑さから屋外ごはん日和を判定",
    meta_desc="今日と明日の風速・降水確率・気温・紫外線をまとめて、BBQ・ピクニック・屋外ごはんに向いているかを0〜100で判定する無料ツール。",
    og_title="BBQ・ピクニック指数", og_desc="風・雨・暑さをまとめて屋外ごはん判定。",
    lead="BBQの敵は雨より風です。風・雨・暑さ・紫外線をまとめて取得して、今日と明日の「屋外ごはん日和度」を採点します。",
    about_h2="この指数について",
    about="""<p>屋外ごはんの快適さは、降水確率だけでは測れません。風速5m/sを超えると紙皿が飛び火の粉が舞い、炎天下では食材が危険になります。この指数は気象オープンデータAPI（Open-Meteo）から風・降水確率・気温・UVを取得し、屋外滞在の快適度として採点します。</p>
    <div class="note">炭火の目安：風3m/s以下=快適、5m/s=火の粉注意、8m/s以上=着火に苦労＆危険。強風日は無理せず屋内へ。</div>""",
    faqs=[("データの出典は？", "気象オープンデータAPI（Open-Meteo）の風速・降水確率・気温・UV指数の予報値を使用しています。"),
          ("採点の考え方は？", "降水確率と風速を大きく、暑さ・寒さと紫外線を補助的に減点する方式です。"),
          ("入力データは送信される？", "地域の選択のみを使います。個人情報は一切送信されません。")],
    rel=[("hanami-yosan","🌸","花見・BBQ予算シミュレーター"),("shuumatsu-hare","🌤️","今週末、晴れる？"),("kyou-kaze","💨","今日、風ヤバい？チェッカー"),("hiyake-timer","☀️","日焼けタイマー")],
    body="""  <section class="panel">
    <h2>🍖 条件</h2>
    <div class="field"><label>地域</label><select id="pref"></select></div>
    <button class="btn btn-primary" id="calcBtn">屋外ごはん日和を採点</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label">今日のBBQ・ピクニック指数は</div>
      <div class="big"><span id="big">0</span><span class="unit">/100</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">風（昼の最大）</div><div class="v" id="wind">—</div></div>
      <div class="stat"><div class="k">降水確率 / 最高気温</div><div class="v" id="pt">—</div></div>
      <div class="stat"><div class="k">明日の指数</div><div class="v accent" id="tomorrow">—</div></div></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
@@PREFS_JS@@
  function dayScore(pop, wind, tmax, uv){
    let s = 100 - (pop ?? 50) * 0.6;
    if(wind > 3) s -= (wind - 3) * 6;
    if(tmax > 30) s -= (tmax - 30) * 3;
    if(tmax < 10) s -= (10 - tmax) * 3;
    if(uv >= 8) s -= 5;
    return Math.max(0, Math.round(s));
  }
  async function calc(){
    const p = PREFS[+$('pref').value];
    $('state').textContent = '予報を取得中…';
    try{
      const r = await fetch('https://api.open-meteo.com/v1/forecast?latitude=' + p[1] + '&longitude=' + p[2] + '&daily=precipitation_probability_max,wind_speed_10m_max,temperature_2m_max,uv_index_max&forecast_days=2&timezone=Asia%2FTokyo');
      const j = await r.json();
      const d = j.daily;
      const sc = (i) => dayScore(d.precipitation_probability_max[i], d.wind_speed_10m_max[i] / 3.6, d.temperature_2m_max[i], d.uv_index_max[i]);
      const s0 = sc(0), s1 = sc(1);
      const label = s0 >= 75 ? '絶好の外めし日和🍖' : s0 >= 55 ? 'まずまずイケる' : s0 >= 35 ? '風・雨と相談' : '今日は屋内が正解…';
      $('state').textContent = '';
      $('sub').textContent = p[0] + '｜' + label;
      $('wind').textContent = (d.wind_speed_10m_max[0] / 3.6).toFixed(0) + 'm/s' + (d.wind_speed_10m_max[0] / 3.6 >= 5 ? '（火の粉注意）' : '');
      $('pt').textContent = d.precipitation_probability_max[0] + '% / ' + d.temperature_2m_max[0].toFixed(0) + '℃';
      $('tomorrow').textContent = s1 + '点' + (s1 > s0 + 10 ? '（明日のほうが良い）' : '');
      SHARE = '今日の' + p[0].split('(')[0] + 'のBBQ指数は' + s0 + '/100🍖（' + label + '）明日は' + s1 + '点。\\n外めし計画の前にチェック👇';
      show(); anim($('big'), 0, s0, 900);
    }catch{ $('state').textContent = '⚠️ 取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  bindShare();
})();""")

# ---------- 13 暗号資産ぜんぶでいくら ----------
sim(slug="crypto-zenbu", cat="money", catjp="お金・時間", grad=G["money"], emoji="🌍",
    title="暗号資産、ぜんぶでいくら？", score=54,
    card_desc="世界の暗号資産を全部売ったらいくら？時価総額を日本の国家予算と比べてみる。",
    title_tag="暗号資産、ぜんぶでいくら？｜世界の時価総額を国家予算と比較",
    meta_desc="世界の暗号資産すべての時価総額をリアルタイム取得して、日本の国家予算・GDPと比較する無料ツール。ビットコインの占有率や銘柄数も表示。投資助言ではありません。",
    og_title="暗号資産、ぜんぶでいくら？", og_desc="世界の時価総額をライブ取得して国家予算と比較。",
    lead="世界中の暗号資産を全部かき集めたら、いくらになるのか。時価総額をライブ取得して、日本の国家予算と並べてみます。",
    about_h2="このメーターについて",
    about="""<p>このメーターは公開の暗号資産データAPI（CoinGecko）から、世界の暗号資産すべての時価総額・ビットコインの占有率・登録銘柄数を取得しています。比較に使う日本の一般会計予算は約115兆円、名目GDPは約610兆円（いずれも2025年ごろの規模感）です。大きすぎる数字は、身近な物差しに換算してはじめて意味を持ちます。</p>
    <div class="note">⚠️ これは規模を体感する娯楽ツールで、投資助言ではありません。暗号資産の価格・時価総額は激しく変動します。</div>""",
    faqs=[("データの出典は？", "公開の暗号資産データAPI（CoinGecko /global）から時価総額・BTC占有率・銘柄数を取得しています。"),
          ("投資の参考になる？", "規模の体感用です。投資判断には使わず、必要なら専門家にご相談ください。"),
          ("入力データは送信される？", "このページは何も入力せずに使えます。")],
    rel=[("btc-tara","🪙","もしビットコイン買ってたら"),("enyasu-taikan","💱","円安体感メーター"),("infure","📉","物価2倍まで何年？"),("fire","🔥","FIRE達成シミュレーター")],
    body="""  <section class="panel" id="resultPanel">
    <div class="result">
      <div class="label">世界の暗号資産、ぜんぶで</div>
      <div class="big"><span id="big">–</span><span class="unit">兆円</span></div>
      <div class="sub" id="sub">データを読み込み中…</div>
      <div class="statline"><div class="stat"><div class="k">日本の国家予算（一般会計）なら</div><div class="v" id="budget">—</div></div>
      <div class="stat"><div class="k">ビットコインの占有率</div><div class="v" id="btc">—</div></div>
      <div class="stat"><div class="k">登録銘柄数</div><div class="v accent" id="coins">—</div></div></div>
      <button class="btn btn-ghost" id="reloadBtn" style="margin-top:10px;">🔄 最新に更新</button>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
  async function load(){
    $('sub').textContent = 'データを読み込み中…';
    try{
      const r = await fetch('https://api.coingecko.com/api/v3/global');
      const j = await r.json();
      const d = j.data;
      const cho = d.total_market_cap.jpy / 1e12;
      const chg = d.market_cap_change_percentage_24h_usd;
      $('sub').textContent = '時価総額ライブ｜24時間で' + (chg >= 0 ? '+' : '') + chg.toFixed(1) + '%（CoinGecko）';
      $('budget').textContent = '約' + (cho / 115).toFixed(1) + '年分';
      $('btc').textContent = d.market_cap_percentage.btc.toFixed(1) + '%';
      $('coins').textContent = d.active_cryptocurrencies.toLocaleString('ja-JP') + '銘柄';
      SHARE = 'いま世界の暗号資産を全部売ると約' + Math.round(cho).toLocaleString('ja-JP') + '兆円🌍（日本の国家予算' + (cho/115).toFixed(1) + '年分・' + d.active_cryptocurrencies.toLocaleString('ja-JP') + '銘柄）\\nライブの数字はこちら👇';
      anim($('big'), 0, Math.round(cho), 1000);
    }catch{ $('sub').textContent = '⚠️ 取得に失敗しました（混雑時は少し待つと通ります）。'; }
  }
  load();
  $('reloadBtn').addEventListener('click', load);
  bindShare();
})();""")

# ---------- 14 海の水温 ----------
sim(slug="umi-mizuon", cat="season", catjp="季節・行事", grad=G["season"], emoji="🏖️",
    title="いま海、冷たい？水温チェッカー", score=53,
    card_desc="見た目は夏でも水はまだ春かも。主要ビーチのいまの海水温をライブ判定。",
    title_tag="いま海、冷たい？水温チェッカー｜主要ビーチの海水温をライブ判定",
    meta_desc="湘南・伊豆・沖縄など主要ビーチのいまの海水温を海洋データからライブ取得し、海水浴できる水温かを判定する無料ツール。",
    og_title="いま海、冷たい？水温チェッカー", og_desc="主要ビーチのいまの海水温をライブ判定。",
    lead="気温は真夏でも、海の中はワンテンポ遅れています。主要ビーチのいまの海水温を取得して、泳げる水かを判定します。",
    about_h2="このチェッカーについて",
    about="""<p>海水温は気温より1〜2ヶ月遅れて変化します。7月頭の海がまだ冷たく、9月の海が意外と温かいのはこのためです。このチェッカーは海洋予報オープンデータAPI（Open-Meteo Marine）から各ビーチ沖の海面水温を取得します。目安は26℃以上=extended快適、23℃=快適、20℃前後=ひんやり、17℃以下=ウェットスーツ域です。</p>
    <div class="note">沖合モデルの推定値のため、浅瀬の実際の水温とは差があります。子どもは大人より体温を奪われやすいので、唇が紫になったら休憩を。</div>""",
    faqs=[("データの出典は？", "海洋予報オープンデータAPI（Open-Meteo Marine）の海面水温（SST）を各ビーチ沖の座標で取得しています。"),
          ("実際の水温と違う？", "沖合モデルの推定のため、浅瀬や湾奥の実測とは1〜3℃程度ずれることがあります。傾向の目安としてご利用ください。"),
          ("入力データは送信される？", "ビーチの選択のみを使います。個人情報は一切送信されません。")],
    rel=[("naminori-biyori","🏄","波乗り日和チェッカー"),("shio-live","🌊","今日の潮、いつ満ちる？"),("hiyake-timer","☀️","日焼けタイマー"),("atsusa-ranking","🌡️","全国いま暑いランキング")],
    body="""  <section class="panel">
    <h2>🏖️ ビーチ</h2>
    <div class="field"><label>ビーチ</label>
      <select id="spot">
        <option value="35.30,139.48" selected>湘南（片瀬・由比ヶ浜）</option>
        <option value="34.80,138.95">伊豆・白浜</option>
        <option value="35.28,140.40">千葉・九十九里</option>
        <option value="33.68,135.35">和歌山・白良浜</option>
        <option value="34.25,133.20">瀬戸内・しまなみ</option>
        <option value="33.90,130.60">福岡・芦屋</option>
        <option value="37.30,138.80">新潟・柏崎</option>
        <option value="26.44,127.79">沖縄・恩納村</option>
      </select>
    </div>
    <button class="btn btn-primary" id="calcBtn">いまの水温を見る</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label">いまの海水温は</div>
      <div class="big"><span id="big">0</span><span class="unit">℃</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">判定</div><div class="v" id="judge">—</div></div>
      <div class="stat"><div class="k">気温との差</div><div class="v" id="gap">—</div></div>
      <div class="stat"><div class="k">明日の水温</div><div class="v accent" id="tomorrow">—</div></div></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
  async function calc(){
    const [lat, lon] = $('spot').value.split(',');
    const name = $('spot').selectedOptions[0].textContent;
    $('state').textContent = '海水温を取得中…';
    try{
      const [m, w] = await Promise.all([
        fetch('https://marine-api.open-meteo.com/v1/marine?latitude=' + lat + '&longitude=' + lon + '&hourly=sea_surface_temperature&forecast_days=2&timezone=Asia%2FTokyo').then(r => r.json()),
        fetch('https://api.open-meteo.com/v1/forecast?latitude=' + lat + '&longitude=' + lon + '&current=temperature_2m').then(r => r.json()),
      ]);
      const H = new Date().getHours();
      const sst = m.hourly.sea_surface_temperature[H];
      const sstT = m.hourly.sea_surface_temperature[H + 24];
      const air = w.current.temperature_2m;
      const judge = sst >= 27 ? '🏖️ 極楽。ずっと入ってられる' : sst >= 24 ? '😊 快適に泳げる' : sst >= 21 ? '🥶 最初ヒヤッと。慣れれば' : sst >= 18 ? '🧊 ウェットスーツ推奨' : '⛔ 遊泳には冷たすぎ';
      $('state').textContent = '';
      $('sub').textContent = name + '沖の海面水温（モデル推定）｜' + judge;
      $('judge').textContent = judge.replace(/^[^ ]+ /, '');
      $('gap').textContent = '気温' + air.toFixed(0) + '℃より' + Math.abs(air - sst).toFixed(0) + '℃' + (air > sst ? '冷たい' : '温かい');
      $('tomorrow').textContent = sstT != null ? sstT.toFixed(1) + '℃' : '—';
      SHARE = 'いまの' + name.split('（')[0] + 'の海水温は' + sst.toFixed(1) + '℃🏖️（' + judge.replace(/^[^ ]+ /,'') + '）\\n海に行く前の答え合わせ👇';
      show(); anim($('big'), 0, Math.round(sst * 10) / 10, 900, 1);
    }catch{ $('state').textContent = '⚠️ 取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  bindShare();
})();""")

# ---------- 15 南極いま何度 ----------
sim(slug="nankyoku-ima", cat="wonder", catjp="ふしぎ・現象", grad=G["wonder"], emoji="🐧",
    title="南極、いま何度？", score=52,
    card_desc="日本が猛暑のいま、昭和基地は真冬。地球の裏側の「いま」をライブで見る。",
    title_tag="南極、いま何度？｜昭和基地・南極点の現在気温をライブ表示",
    meta_desc="南極の昭和基地と南極点、北極圏のいまの気温をリアルタイム取得して東京と比較する無料ツール。冷凍庫より寒いのか、ペンギンは何を思うのか。",
    og_title="南極、いま何度？", og_desc="昭和基地・南極点のいまの気温をライブ表示。",
    lead="あなたが暑い暑いと言っているいまこの瞬間、南極は極夜の真冬です。昭和基地と南極点の「いま」をライブで取得します。",
    about_h2="このメーターについて",
    about="""<p>南半球の季節は日本と真逆で、日本の夏は南極の冬。特に内陸の南極点は冬に−60℃前後まで下がり、家庭の冷凍庫（−18℃）が暖かく感じるレベルになります。このメーターは気象オープンデータAPI（Open-Meteo）から昭和基地（東オングル島）・南極点・北極圏（スバールバル）の現在気温を取得し、東京と並べます。</p>
    <div class="note">昭和基地には日本の南極地域観測隊が越冬しており、彼らは今日もこの気温の中で働いています。頭が下がります。</div>""",
    faqs=[("データの出典は？", "気象オープンデータAPI（Open-Meteo）から、昭和基地・南極点・スバールバル諸島の座標の現在気温を取得しています。"),
          ("観測隊の実測値？", "数値予報モデルの推定値です。実測は気象庁の昭和基地観測データで公開されています。"),
          ("入力データは送信される？", "このページは何も入力せずに使えます。")],
    rel=[("sekai-kion","🌏","世界の都市、いま何度？"),("aurora-yohou","🌌","オーロラ予報メーター"),("gelande-yuki","⛷️","ゲレンデ積雪ライブ"),("iss-doko","🛰️","ISSはいまどこ？")],
    body="""  <section class="panel" id="resultPanel">
    <div class="result">
      <div class="label">昭和基地（南極）は、いま</div>
      <div class="big"><span id="big">–</span><span class="unit">℃</span></div>
      <div class="sub" id="sub">データを読み込み中…</div>
      <div class="statline"><div class="stat"><div class="k">南極点</div><div class="v" id="pole">—</div></div>
      <div class="stat"><div class="k">北極圏（スバールバル）</div><div class="v" id="arctic">—</div></div>
      <div class="stat"><div class="k">東京との差</div><div class="v accent" id="tokyo">—</div></div></div>
      <button class="btn btn-ghost" id="reloadBtn" style="margin-top:10px;">🔄 最新に更新</button>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
  async function load(){
    $('sub').textContent = 'データを読み込み中…';
    try{
      const r = await fetch('https://api.open-meteo.com/v1/forecast?latitude=-69.00,-90.00,78.22,35.69&longitude=39.58,0.00,15.65,139.69&current=temperature_2m');
      const j = await r.json();
      const [showa, pole, sval, tokyo] = j.map(x => x.current.temperature_2m);
      const freezer = showa < -18 ? '家庭の冷凍庫（−18℃）より寒い❄️' : '意外にも冷凍庫より暖かい';
      $('sub').textContent = freezer + '｜モデル推定のライブ気温';
      $('pole').textContent = pole.toFixed(1) + '℃';
      $('arctic').textContent = sval.toFixed(1) + '℃';
      $('tokyo').textContent = '東京' + tokyo.toFixed(1) + '℃と' + Math.abs(tokyo - showa).toFixed(0) + '℃差';
      SHARE = 'いまの南極・昭和基地は' + showa.toFixed(1) + '℃、南極点は' + pole.toFixed(1) + '℃🐧 東京との差' + Math.abs(tokyo - showa).toFixed(0) + '℃。地球は広い。\\n地球の裏側のいまはこちら👇';
      anim($('big'), 0, Math.round(showa * 10) / 10, 1000, 1);
    }catch{ $('sub').textContent = '⚠️ 取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  load();
  $('reloadBtn').addEventListener('click', load);
  bindShare();
})();""")

# ============================================================ 投入処理
IDX = os.path.join(ROOT, "index.html")
with io.open(IDX, encoding="utf-8") as f:
    html = f.read()
assert "sims/kyou-no-kanshin/" not in html, "既に挿入済み（中止）"

for s in SIMS:
    dst = os.path.join(ROOT, "sims", s["slug"])
    assert not os.path.exists(dst), "slug衝突: " + s["slug"]
    os.makedirs(dst)
    ld_app = json.dumps({"@context": "https://schema.org", "@type": "WebApplication", "name": s["title"],
        "url": "https://shimulabo.com/sims/%s/" % s["slug"], "description": s["og_desc"],
        "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any", "inLanguage": "ja",
        "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "JPY"},
        "publisher": {"@type": "Organization", "name": "シミュラボ", "url": "https://shimulabo.com/"}}, ensure_ascii=False)
    ld_bread = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "ホーム", "item": "https://shimulabo.com/"},
        {"@type": "ListItem", "position": 2, "name": "ライブデータラボ", "item": "https://shimulabo.com/live/"},
        {"@type": "ListItem", "position": 3, "name": s["title"], "item": "https://shimulabo.com/sims/%s/" % s["slug"]}]}, ensure_ascii=False)
    js = s["js"].replace("@@JS_COMMON@@", JS_COMMON).replace("@@PREFS_JS@@", PREFS_JS).replace("@@WIKI_FILTER_JS@@", WIKI_FILTER_JS)
    body = s["body"].replace("@@SHARE_ROW@@", SHARE_ROW)
    page = (SKELETON
        .replace("@@SLUG@@", s["slug"]).replace("@@TITLE_TAG@@", s["title_tag"])
        .replace("@@META_DESC@@", s["meta_desc"]).replace("@@OG_TITLE@@", s["og_title"]).replace("@@OG_DESC@@", s["og_desc"])
        .replace("@@LD_APP@@", ld_app).replace("@@LD_BREAD@@", ld_bread).replace("@@LD_FAQ@@", faq_ld(s["faqs"]))
        .replace("@@CATJP@@", s["catjp"]).replace("@@H1@@", s["title"]).replace("@@LEAD@@", s["lead"])
        .replace("@@BODY@@", body).replace("@@ABOUT_H2@@", s["about_h2"]).replace("@@ABOUT@@", s["about"])
        .replace("@@FAQ_DL@@", faq_dl(s["faqs"])).replace("@@RELATED@@", related(s["rel"]))
        .replace("@@JS@@", js))
    with io.open(os.path.join(dst, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    print("generated:", s["slug"])

# OGP
gen_path = os.path.join(SCRIPTS, "gen_images.py")
gen_src = io.open(gen_path, encoding="utf-8").read()
ns = {"__file__": gen_path}
exec(compile(gen_src.split("\nSIMS = [")[0], gen_path, "exec"), ns)
for s in SIMS:
    ns["make_ogp"](os.path.join(ROOT, "ogp", s["slug"] + ".png"), s["title"], s["catjp"])

# index.html
cards, ranks = [], []
for s in SIMS:
    cards.append(
"""    <a class="sim-card" data-cat="%s" href="sims/%s/">
      <div class="thumb" style="background:%s"><span class="emoji">%s</span></div>
      <div class="body"><div class="cat">%s</div><h3>%s</h3><p>%s</p><span class="go">触ってみる →</span></div>
    </a>
""" % (s["cat"], s["slug"], s["grad"], s["emoji"], s["catjp"], s["title"], s["card_desc"]))
    ranks.append("    { href: 'sims/%s/', emoji: '%s', title: '%s', cat: '%s', score: %d }" % (s["slug"], s["emoji"], s["title"], s["catjp"], s["score"]))
marker = '    <a class="req-card" href="request/">'
html = html.replace(marker, "".join(cards) + marker, 1)
idx2 = html.index("\n  ];")
before = html[:idx2].rstrip()
if not before.endswith(","):
    before += ","
html = before + "\n" + ",\n".join(ranks) + html[idx2:]
m = re.search(r"<b>(\d+)</b>本 公開中", html)
cnt = int(m.group(1))
html = html.replace("<b>%d</b>本 公開中" % cnt, "<b>%d</b>本 公開中" % (cnt + len(SIMS)), 1)
with io.open(IDX, "w", encoding="utf-8") as f:
    f.write(html)
print("patched index.html: count=%d" % (cnt + len(SIMS)))

# /live/
LIVE = os.path.join(ROOT, "live", "index.html")
with io.open(LIVE, encoding="utf-8") as f:
    lv = f.read()
def live_card(s):
    return '\n    <a class="sim-card" href="../sims/%s/"><div class="thumb" style="background:%s"><span class="emoji">%s</span></div><div class="body"><div class="cat">%s</div><h3>%s</h3><p>%s</p><span class="go">触ってみる →</span></div></a>' % (
        s["slug"], s["grad"], s["emoji"], s["catjp"], s["title"], s["card_desc"])
by = {s["slug"]: s for s in SIMS}
def insert_after(anchor_slug, slugs):
    global lv
    a = lv.index(anchor_slug + "/")
    a = lv.index("</a>", a) + 4
    lv = lv[:a] + "".join(live_card(by[x]) for x in slugs) + lv[a:]

# 新グループ「世間のいま」を天気グループの前に追加
sec = """  <h2 class="live-h2">🧠 世間のいま</h2>
  <div class="live-grid">""" + "".join(live_card(by[x]) for x in ["kyou-no-kanshin", "docchi-yumei", "kotoba-trend", "crypto-zenbu"]) + """
  </div>

"""
anchor = lv.index('<h2 class="live-h2">☀️ 天気・気候のいま</h2>')
lv = lv[:anchor] + sec + lv[anchor:]
insert_after("hiruma-nagasa", ["heinen-hikaku", "amagumo-now", "yohou-shinrai", "bbq-shisu", "running-shisu", "inu-sanpo-ok"])
insert_after("natsu-2050", ["ondanka-taikan", "nankyoku-ima"])
insert_after("conbini-mitsudo", ["jinja-tera"])
insert_after("gelande-yuki", ["shio-live", "umi-mizuon"])
for a, b in [("シミュレーター35選", "シミュレーター50選"), ("35本を一覧掲載", "50本を一覧掲載"), ("35本のコレクション", "50本のコレクション")]:
    lv = lv.replace(a, b)
lv = lv.replace("<tr><td>米地質調査所（USGS）</td>",
                "<tr><td>Wikimedia財団（Wikipedia統計）</td><td>記事別・日別の閲覧数</td><td>きのうの関心事/どっちが有名/言葉トレンド/誕生日</td></tr>\n      <tr><td>RainViewer</td><td>世界の気象レーダー合成</td><td>いまの雨雲マップ</td></tr>\n      <tr><td>米地質調査所（USGS）</td>")
with io.open(LIVE, "w", encoding="utf-8") as f:
    f.write(lv)
print("patched live/index.html: +15 cards, 35->50")

# sitemap
SM = os.path.join(ROOT, "sitemap.xml")
with io.open(SM, encoding="utf-8") as f:
    sm = f.read()
entries = "".join(
    "  <url><loc>https://shimulabo.com/sims/%s/</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>\n" % (s["slug"], TODAY)
    for s in SIMS)
sm = sm.replace("</urlset>", entries + "</urlset>")
with io.open(SM, "w", encoding="utf-8") as f:
    f.write(sm)
print("patched sitemap.xml: +%d urls" % len(SIMS))
print("ALL DONE")
