# -*- coding: utf-8 -*-
"""API連携シリーズ第3弾 10本 + /live/ハブページ + 引用ブロック + トップ特集シェルフ（1回限り）。
   1) 新規10本生成（引用ブロック標準装備・og:image込み）
   2) 既存API連携15本に「引用・転載について」ブロックを追記
   3) /live/ ライブデータラボ（ハブページ）新設
   4) index.html: ⚡ライブデータ特集シェルフ + カード + ランキング + 本数(798→808)
   5) sitemap.xml: /live/ + 10URL
"""
import os, io, re, json

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPTS)
TODAY = "2026-08-20"

# ---------------------------------------------------------- 共通部品
SKELETON = """<!DOCTYPE html>
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
    <meta property="og:url" content="https://shimulabo.com/sims/@@SLUG@@/">
<title>@@TITLE_TAG@@｜シミュラボ</title>
<meta name="description" content="@@META_DESC@@">
<meta property="og:title" content="@@OG_TITLE@@">
<meta property="og:description" content="@@OG_DESC@@">
<meta property="og:type" content="website">
    <meta property="og:image" content="https://shimulabo.com/ogp/@@SLUG@@.png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="https://shimulabo.com/ogp/@@SLUG@@.png">
<link rel="stylesheet" href="../../assets/style.css?v=4">
    <!-- seo-internal -->
    <link rel="canonical" href="https://shimulabo.com/sims/@@SLUG@@/">
    <meta property="og:locale" content="ja_JP">
    <meta name="robots" content="index,follow">
    <script type="application/ld+json">@@LD_APP@@</script>
    <script type="application/ld+json">@@LD_BREAD@@</script>
    <script type="application/ld+json">@@LD_FAQ@@</script>
    <!-- ga4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-R72MT9H7PT"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-R72MT9H7PT");</script>
    <!-- adsense -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4521532459480990"
         crossorigin="anonymous"></script>
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
    <a class="back" href="../../live/">⚡ ライブデータ一覧</a>
  </div>
</header>

<main class="wrap">

  <nav class="breadcrumb" aria-label="breadcrumb"><a href="../../">ホーム</a><span>›</span><a href="../../live/">ライブデータラボ</a><span>›</span><span class="cur">@@H1@@</span></nav>

  <div class="sim-head">
    <div class="cat">@@CATJP@@</div>
    <h1>@@H1@@</h1>
    <p class="lead">@@LEAD@@</p>
  </div>

@@BODY@@

  <article class="article">
    <h2>@@ABOUT_H2@@</h2>
    @@ABOUT@@
    <h2>引用・転載について</h2>
    <p>本ページの計算結果・数値は、<b>出典を明記いただければ</b>ブログ・ニュース記事・SNS・社内資料への引用を歓迎します。事前連絡は不要です。</p>
    <div class="note">推奨クレジット表記：<code>出典：シミュラボ「@@H1@@」 https://shimulabo.com/sims/@@SLUG@@/</code><br>Webでご利用の際は上記URLへのリンク設置をお願いします。</div>
    <h2>よくある質問</h2><dl class="faq">@@FAQ_DL@@</dl>
  </article>

  <nav class="related" aria-label="related">
    <h2>ほかのシミュレーション</h2>
    <div class="related-grid">@@RELATED@@</div>
  </nav>

  <section class="req-banner">
    <h2>💡 こんなシミュも見てみたい？</h2>
    <p>あなたの「これ数字で見たい」を送ってください。投票で人気の案から実際に作ります。</p>
    <a class="btn btn-primary" style="width:auto;display:inline-flex;padding:14px 30px;" href="../../request/">リクエストする →</a>
    <div style="margin-top:12px;"><a href="../../board/" style="font-size:13px;font-weight:800;">🗳️ みんなのリクエストに投票する →</a></div>
  </section>

</main>

<footer class="site-footer">
  <div class="inner">
    <p><a href="../../">← シミュラボ トップへ戻る</a>　<a href="../../live/">⚡ ライブデータラボ</a></p>
    <p style="margin-top:10px;opacity:.7">© 2026 シミュラボ</p>
  </div>
</footer>

<script>
@@JS@@
</script>
<script src="../../assets/share-counter.js?v=4"></script>
<script>ShareCounter.initSim({ simId:'@@SLUG@@', badgeEl:document.getElementById('shareCount'), shareBtnIds:['shareBtn'] });</script>
<script src="../../assets/result-fx.js?v=4"></script>
<script src="../../assets/lang-toggle.js?v=4"></script>
</body>
</html>
"""

SHARE_ROW = """      <div style="text-align:center;"><span id="shareCount" class="share-count" style="display:none"></span></div>
      <div class="share-row">
        <button class="btn btn-x" id="shareBtn">𝕏 で結果をシェア</button>
        <button class="btn btn-ghost" id="copyBtn">結果をコピー</button>
      </div>"""

JS_COMMON = """  const $ = (id) => document.getElementById(id);
  let SHARE = '';
  function anim(el, from, to, dur, dec){ const t0=performance.now(); (function s(n){const p=Math.min(1,(n-t0)/dur);const e=1-Math.pow(1-p,3);const v=from+(to-from)*e;el.textContent=(dec!=null?v.toFixed(dec):Math.round(v).toLocaleString('ja-JP'));if(p<1)requestAnimationFrame(s);})(performance.now()); }
  function show(){ $('resultPanel').style.display=''; $('resultPanel').scrollIntoView({behavior:'smooth',block:'start'}); }
  function bindShare(){
    $('shareBtn').addEventListener('click', () => window.open('https://twitter.com/intent/tweet?text='+encodeURIComponent(SHARE)+'&url='+encodeURIComponent(location.href)+'&hashtags='+encodeURIComponent('シミュラボ'),'_blank','noopener'));
    $('copyBtn').addEventListener('click', async () => { try{ await navigator.clipboard.writeText(SHARE+'\\n'+location.href); $('copyBtn').textContent='コピーしました ✓'; setTimeout(()=>$('copyBtn').textContent='結果をコピー',1600);}catch{alert(SHARE);} });
  }"""

PREF_ROWS = [
    ('北海道(札幌)',43.06,141.35),('青森県',40.82,140.74),('岩手県',39.70,141.15),('宮城県(仙台)',38.27,140.87),
    ('秋田県',39.72,140.10),('山形県',38.24,140.36),('福島県',37.75,140.47),('茨城県',36.34,140.45),
    ('栃木県',36.57,139.88),('群馬県',36.39,139.06),('埼玉県',35.86,139.65),('千葉県',35.61,140.12),
    ('東京都',35.69,139.69),('神奈川県(横浜)',35.45,139.64),('新潟県',37.90,139.02),('富山県',36.70,137.21),
    ('石川県(金沢)',36.59,136.63),('福井県',36.07,136.22),('山梨県',35.66,138.57),('長野県',36.65,138.18),
    ('岐阜県',35.39,136.72),('静岡県',34.98,138.38),('愛知県(名古屋)',35.18,136.91),('三重県',34.73,136.51),
    ('滋賀県',35.00,135.87),('京都府',35.02,135.76),('大阪府',34.69,135.52),('兵庫県(神戸)',34.69,135.18),
    ('奈良県',34.69,135.83),('和歌山県',34.23,135.17),('鳥取県',35.50,134.24),('島根県(松江)',35.47,133.05),
    ('岡山県',34.66,133.93),('広島県',34.40,132.46),('山口県',34.19,131.47),('徳島県',34.07,134.56),
    ('香川県(高松)',34.34,134.04),('愛媛県(松山)',33.84,132.77),('高知県',33.56,133.53),('福岡県',33.61,130.42),
    ('佐賀県',33.25,130.30),('長崎県',32.74,129.87),('熊本県',32.79,130.74),('大分県',33.24,131.61),
    ('宮崎県',31.91,131.42),('鹿児島県',31.56,130.56),('沖縄県(那覇)',26.21,127.68),
]
PREFS_JS = "  const PREFS = [\n" + "\n".join(
    "    ['%s',%s,%s]," % r for r in PREF_ROWS) + "\n  ];\n  $('pref').innerHTML = PREFS.map((p,i) => '<option value=\"' + i + '\"' + (i===12?' selected':'') + '>' + p[0] + '</option>').join('');"

def faq_dl(faqs):
    return "".join("<dt>%s</dt><dd>%s</dd>" % (q, a) for q, a in faqs)

def faq_ld(faqs):
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in faqs
    ]}, ensure_ascii=False)

def related(items):
    return "".join('<a class="related-card" href="../%s/"><span class="e">%s</span><span>%s</span></a>' % (s, e, t) for s, e, t in items)

SIMS = []

# ============================================================ 1 傘いる？
SIMS.append(dict(
    slug="kasa-iru", cat="tool", catjp="便利ツール", grad="linear-gradient(135deg,#eff6ff,#e0f2fe)", emoji="☔",
    title="今日、傘いる？メーター", score=76,
    card_desc="出がけの3秒判定。今日の降水確率から「いらない/折りたたみ/ガチ傘」を即答。",
    title_tag="今日、傘いる？メーター｜降水確率から3秒で判定",
    meta_desc="今日の1時間ごとの降水確率をリアルタイム取得して「傘いらない・折りたたみでOK・ガチ傘必須」を3秒で判定する無料ツール。雨の時間帯と帰宅時間のリスクも表示。",
    og_title="今日、傘いる？メーター",
    og_desc="今日の降水確率から傘の要否を3秒判定。",
    lead="毎朝の「傘どうしよう」を3秒で終わらせます。今日の1時間ごとの降水確率から、傘の要否と危ない時間帯を判定します。",
    about_h2="この判定について",
    about="""<p>天気アプリは情報が多すぎて、結局知りたい「で、傘は？」に答えてくれません。このメーターは気象オープンデータAPI（Open-Meteo）から今日の1時間ごとの降水確率と降水量を取得し、外出時間帯（7時〜24時）の最大リスクで3段階判定します。判定の目安は、降水確率30%未満=いらない、30〜60%=折りたたみ、60%以上または強い雨予報=ガチ傘です。</p>
    <div class="note">にわか雨型の日は「合計では降らないが一瞬だけ降る」ことがあります。雨の時間帯表示もあわせて確認してください。</div>""",
    faqs=[("データの出典は？", "気象オープンデータAPI（Open-Meteo）から、選んだ地点の今日の降水確率・降水量を1時間単位で取得しています。"),
          ("判定の基準は？", "外出時間帯（7〜24時）の最大降水確率が30%未満で「いらない」、30〜60%で「折りたたみ」、60%以上または1mm/h以上の雨予報で「ガチ傘」としています。"),
          ("入力データは送信される？", "地域の選択のみを気象APIへの問い合わせに使います。個人情報は一切送信されません。")],
    rel=[("sentaku-kawaku","👕","洗濯物 乾く時間メーター"),("yuyake-yohou","🌇","今日の夕焼け予報"),("hiyake-timer","☀️","日焼けタイマー"),("kion-kandansa","🧣","寒暖差疲労チェッカー")],
    body="""  <section class="panel">
    <h2>☔ 条件</h2>
    <div class="field"><label>地域</label><select id="pref"></select></div>
    <button class="btn btn-primary" id="calcBtn">傘いる？を3秒判定</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label">今日の判定は</div>
      <div class="big" style="font-size:min(13vw,64px);"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">最大降水確率</div><div class="v" id="maxpop">—</div></div>
      <div class="stat"><div class="k">雨が降りそうな時間</div><div class="v" id="rainhours">—</div></div>
      <div class="stat"><div class="k">帰宅時間帯（18〜21時）</div><div class="v accent" id="evening">—</div></div></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
@@PREFS_JS@@
  async function calc(){
    const p = PREFS[+$('pref').value];
    $('state').textContent = '今日の降水予報を取得中…';
    try{
      const r = await fetch('https://api.open-meteo.com/v1/forecast?latitude=' + p[1] + '&longitude=' + p[2] + '&hourly=precipitation_probability,precipitation&forecast_days=1&timezone=Asia%2FTokyo');
      const j = await r.json();
      const PP = j.hourly.precipitation_probability, PR = j.hourly.precipitation;
      const H = new Date().getHours();
      const from = Math.max(7, H);
      let maxpop = 0, heavy = false;
      const rainH = [];
      for(let h = from; h <= 23; h++){
        if(PP[h] != null && PP[h] > maxpop) maxpop = PP[h];
        if((PP[h] ?? 0) >= 50) rainH.push(h);
        if((PR[h] ?? 0) >= 1) heavy = true;
      }
      const evening = Math.max(PP[18] ?? 0, PP[19] ?? 0, PP[20] ?? 0, PP[21] ?? 0);
      const verdict = (maxpop >= 60 || heavy) ? 'ガチ傘 ☂️' : maxpop >= 30 ? '折りたたみでOK 🌂' : 'いらない ☀️';
      $('state').textContent = '';
      $('big').textContent = verdict;
      $('sub').textContent = p[0] + '・いまから今日いっぱいの判定';
      $('maxpop').textContent = maxpop + '%';
      $('rainhours').textContent = rainH.length ? rainH.map(h => h + '時').join('・') : 'なし';
      $('evening').textContent = evening + '%' + (evening >= 50 ? '（置き傘推奨）' : '');
      SHARE = '今日の' + p[0] + '、傘は「' + verdict + '」☔（最大降水確率' + maxpop + '%）\\n毎朝3秒で判定できるやつ👇';
      show();
    }catch{ $('state').textContent = '⚠️ 予報の取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  bindShare();
})();"""
))

# ============================================================ 2 全国暑さランキング
SIMS.append(dict(
    slug="atsusa-ranking", cat="season", catjp="季節・行事", grad="linear-gradient(135deg,#fff7ed,#fce7f3)", emoji="🌡️",
    title="全国いま暑いランキング", score=75,
    card_desc="あなたの県はいま全国何位に暑い？47都道府県の現在気温をライブで一斉計測。",
    title_tag="全国いま暑いランキング｜47都道府県の現在気温をライブ順位表示",
    meta_desc="47都道府県の現在気温をリアルタイムに一斉取得して、あなたの県が全国何位に暑いかをランキング表示する無料ツール。暑さ自慢・涼しさ自慢のお供に。",
    og_title="全国いま暑いランキング｜あなたの県は何位？",
    og_desc="47都道府県の現在気温をライブで一斉計測。",
    lead="「うちの県が一番暑いって！」を数字で決着させます。47都道府県の現在気温を一斉取得して、いまこの瞬間の全国ランキングを作ります。",
    about_h2="このランキングについて",
    about="""<p>このランキングは気象オープンデータAPI（Open-Meteo）に47都道府県の県庁所在地の座標を一括で問い合わせ、現在気温を同時刻で取得して順位化しています。テレビの「今日の最高気温」と違い、<b>いまこの瞬間</b>の勝負なので、開くたびに順位が入れ替わります。夏は暑さ自慢、冬は寒さ自慢にどうぞ。</p>
    <div class="note">観測点は県庁所在地相当の1地点です。同じ県内でも内陸や盆地はもっと極端な数字が出ます。</div>""",
    faqs=[("気温データの出典は？", "気象オープンデータAPI（Open-Meteo）から、47都道府県の県庁所在地相当地点の現在気温を一括取得しています。"),
          ("アメダスの実測値と違う？", "数値予報モデルベースの推計のため、アメダス実測とは多少ズレることがあります。順位の目安としてお楽しみください。"),
          ("入力データは送信される？", "地域の選択のみを使います。個人情報は一切送信されません。")],
    rel=[("nettaiya-check","🌙","今夜、熱帯夜？チェック"),("kion-kandansa","🧣","寒暖差疲労チェッカー"),("sekai-kion","🌏","世界の都市、いま何度？"),("kasa-iru","☔","今日、傘いる？メーター")],
    body="""  <section class="panel">
    <h2>🌡️ あなたの県</h2>
    <div class="field"><label>地域</label><select id="pref"></select></div>
    <button class="btn btn-primary" id="calcBtn">いまの全国順位を見る</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label" id="topLabel">あなたの県はいま、全国で</div>
      <div class="big"><span id="big">0</span><span class="unit">位に暑い</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">いまの気温</div><div class="v" id="temp">—</div></div>
      <div class="stat"><div class="k">全国1位（暑い）</div><div class="v" id="hot1">—</div></div>
      <div class="stat"><div class="k">全国47位（涼しい）</div><div class="v accent" id="cool1">—</div></div></div>
      <div id="list" style="margin-top:14px;"></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
@@PREFS_JS@@
  async function calc(){
    const sel = +$('pref').value;
    $('state').textContent = '47都道府県の現在気温を一斉取得中…';
    try{
      const lats = PREFS.map(p => p[1]).join(',');
      const lons = PREFS.map(p => p[2]).join(',');
      const r = await fetch('https://api.open-meteo.com/v1/forecast?latitude=' + lats + '&longitude=' + lons + '&current=temperature_2m&timezone=Asia%2FTokyo');
      const j = await r.json();
      const rows = j.map((x, i) => ({ i, name: PREFS[i][0], t: x.current.temperature_2m })).sort((a,b) => b.t - a.t);
      const rank = rows.findIndex(x => x.i === sel) + 1;
      const me = rows[rank - 1];
      $('state').textContent = '';
      $('sub').textContent = new Date().toLocaleTimeString('ja-JP', {hour:'2-digit',minute:'2-digit'}) + ' 時点の現在気温で47都道府県を順位化';
      $('temp').textContent = me.t.toFixed(1) + '℃';
      $('hot1').textContent = rows[0].name + '（' + rows[0].t.toFixed(1) + '℃）';
      $('cool1').textContent = rows[46].name + '（' + rows[46].t.toFixed(1) + '℃）';
      $('list').innerHTML = '<div style="font-weight:800;font-size:13px;margin-bottom:8px;">🔥 いまのTOP5</div>' + rows.slice(0,5).map((x,k) =>
        '<div style="display:flex;gap:8px;justify-content:space-between;padding:7px 10px;margin-bottom:5px;background:rgba(127,127,127,.07);border-radius:8px;font-size:12.5px;text-align:left;' + (x.i === sel ? 'outline:2px solid rgba(255,120,0,.5);' : '') + '">'
        + '<span>' + (k+1) + '位　' + x.name + '</span><span>' + x.t.toFixed(1) + '℃</span></div>').join('');
      SHARE = 'いま' + PREFS[sel][0].split('(')[0] + 'は全国' + rank + '位に暑い🌡️（' + me.t.toFixed(1) + '℃）全国1位は' + rows[0].name.split('(')[0] + 'の' + rows[0].t.toFixed(1) + '℃！\\nあなたの県は何位？👇';
      show(); anim($('big'), 0, rank, 900);
    }catch{ $('state').textContent = '⚠️ 取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  bindShare();
})();"""
))

# ============================================================ 3 次の3連休
SIMS.append(dict(
    slug="tsugi-renkyuu", cat="season", catjp="季節・行事", grad="linear-gradient(135deg,#fff7ed,#fce7f3)", emoji="📅",
    title="次の3連休カウントダウン", score=74,
    card_desc="次の3連休、あと何日？最新の祝日データから連休カレンダーを自動生成。",
    title_tag="次の3連休はいつ？カウントダウン｜今年の連休カレンダー自動生成",
    meta_desc="次の3連休まであと何日かを最新の祝日データからリアルタイム計算する無料ツール。今年〜来年の3連休一覧と、有休1日で伸ばせる連休も表示。",
    og_title="次の3連休カウントダウン",
    og_desc="次の3連休まであと何日？祝日データから自動計算。",
    lead="がんばれるのは、次の連休が見えているときだけ。最新の祝日データから、次の3連休までのカウントダウンと今後の連休一覧を出します。",
    about_h2="このカウントダウンについて",
    about="""<p>このツールは世界の祝日オープンデータAPI（Nager.Date）から日本の「土日＋祝日で3日以上つながる週末」を取得し、次の3連休までの日数を数えます。橋渡しの平日に有休を1日置くと3連休になる「隠れ連休」も表示するので、<a href="../renkyuu-maker/">9連休メーカー</a>とあわせて休暇計画にどうぞ。</p>
    <div class="note">会社の夏季休暇・年末年始休暇は含みません。カレンダー通りに休める人向けの計算です。</div>""",
    faqs=[("祝日データの出典は？", "世界の祝日オープンデータAPI（Nager.Date）の日本の連休データを取得しています。祝日の発表・変更にも自動で追従します。"),
          ("「有休1日で3連休」とは？", "土日と祝日のあいだに平日が1日だけ挟まるケースです。その1日に有休を置くと連休がつながります。"),
          ("入力データは送信される？", "このページは何も入力せずに使えます。")],
    rel=[("renkyuu-maker","🏖️","9連休メーカー"),("sekai-yasumi","🌍","今日、世界のどこが祝日？"),("kyuryobi","📆","あと何回給料日"),("kotoshi-pct","📅","今年あと何％シミュレーター")],
    body="""  <section class="panel" id="resultPanel">
    <div class="result">
      <div class="label">次の3連休まで、あと</div>
      <div class="big"><span id="big">–</span><span class="unit">日</span></div>
      <div class="sub" id="sub">データを読み込み中…</div>
      <div class="statline"><div class="stat"><div class="k">期間</div><div class="v" id="period">—</div></div>
      <div class="stat"><div class="k">何連休？</div><div class="v" id="len">—</div></div>
      <div class="stat"><div class="k">今後1年の3連休以上</div><div class="v accent" id="count">—</div></div></div>
      <div id="list" style="margin-top:14px;"></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
  const WD = ['日','月','火','水','木','金','土'];
  const fmt = (s) => { const d = new Date(s + 'T00:00:00'); return (d.getMonth()+1) + '/' + d.getDate() + '(' + WD[d.getDay()] + ')'; };
  async function load(){
    try{
      const y = new Date().getFullYear();
      const [a, b] = await Promise.all([
        fetch('https://date.nager.at/api/v3/LongWeekend/' + y + '/JP').then(r => r.json()),
        fetch('https://date.nager.at/api/v3/LongWeekend/' + (y+1) + '/JP').then(r => r.json()),
      ]);
      const t = new Date(); t.setHours(0,0,0,0);
      const all = [...a, ...b].filter(x => new Date(x.startDate + 'T00:00:00') >= t);
      const solid = all.filter(x => !x.needBridgeDay);
      const nx = solid[0];
      if(!nx){ $('sub').textContent = 'この先1年の3連休データが見つかりませんでした。'; return; }
      const days = Math.round((new Date(nx.startDate + 'T00:00:00') - t) / 86400000);
      $('sub').textContent = days === 0 ? '🎉 今日から3連休です！' : '最新の祝日データから自動計算（土日+祝日ベース）';
      $('period').textContent = fmt(nx.startDate) + '〜' + fmt(nx.endDate);
      $('len').textContent = nx.dayCount + '連休';
      $('count').textContent = solid.length + '回';
      const bridge = all.filter(x => x.needBridgeDay).slice(0, 2);
      $('list').innerHTML = '<div style="font-weight:800;font-size:13px;margin-bottom:8px;">📋 この先の連休</div>'
        + solid.slice(0, 6).map(x => '<div style="display:flex;gap:8px;justify-content:space-between;padding:7px 10px;margin-bottom:5px;background:rgba(127,127,127,.07);border-radius:8px;font-size:12.5px;text-align:left;"><span>' + fmt(x.startDate) + '〜' + fmt(x.endDate) + '</span><span>' + x.dayCount + '連休</span></div>').join('')
        + (bridge.length ? '<div style="font-weight:800;font-size:13px;margin:10px 0 8px;">🎯 有休1日で作れる隠れ連休</div>' + bridge.map(x => '<div style="display:flex;gap:8px;justify-content:space-between;padding:7px 10px;margin-bottom:5px;background:rgba(255,170,0,.10);border-radius:8px;font-size:12.5px;text-align:left;"><span>' + fmt(x.startDate) + '〜' + fmt(x.endDate) + '</span><span>' + x.dayCount + '連休</span></div>').join('') : '');
      SHARE = '次の3連休（' + fmt(nx.startDate) + '〜）まで、あと' + days + '日📅 それまでがんばろう…\\nカウントダウンはこちら👇';
      anim($('big'), 0, days, 900);
    }catch{ $('sub').textContent = '⚠️ 祝日データの取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  load();
  bindShare();
})();"""
))

# ============================================================ 4 コンビニ密度
SIMS.append(dict(
    slug="conbini-mitsudo", cat="home", catjp="住まい・暮らし", grad="linear-gradient(135deg,#ecfdf5,#d1fae5)", emoji="🏪",
    title="コンビニ密度チェッカー", score=73,
    card_desc="あなたの街、徒歩圏にコンビニ何軒ある？地図データから500m圏をライブ集計。",
    title_tag="コンビニ密度チェッカー｜住所から徒歩圏のコンビニ数を集計",
    meta_desc="住所や駅名を入れると、半径500m・1kmのコンビニ数と最寄りまでの距離を世界最大の地図データベース（OpenStreetMap）からライブ集計する無料ツール。引っ越し先の利便性チェックに。",
    og_title="コンビニ密度チェッカー｜徒歩圏に何軒？",
    og_desc="500m圏のコンビニ数を地図データからライブ集計。",
    lead="「コンビニまで徒歩◯分」は、暮らしやすさの立派な指標。住所や駅名を入れるだけで、徒歩圏のコンビニ数と最寄り店舗を地図データから集計します。",
    about_h2="このチェッカーについて",
    about="""<p>このチェッカーは国土地理院の住所検索APIで場所を特定し、世界最大のオープン地図データベース「OpenStreetMap」（Overpass API）に登録されたコンビニエンスストアを半径1km圏で取得して、距離を計算しています。500m＝徒歩約6分、1km＝徒歩約12分が目安です。引っ越し候補の比較に使うと、物件サイトには載らない「生活の解像度」が上がります。</p>
    <div class="note">OpenStreetMapは有志が更新する地図のため、開店したばかりの店舗や小規模店が未登録のことがあります。実数はこれより多い可能性があります。</div>""",
    faqs=[("店舗データの出典は？", "世界最大のオープン地図データベースOpenStreetMap（Overpass API）と、国土地理院の住所検索APIを利用しています。"),
          ("数が実際より少ない気がする", "OpenStreetMapは有志更新のため、登録漏れがあり得ます。「最低でもこれだけある」という下限の目安としてご覧ください。"),
          ("入力した住所は保存される？", "いいえ。住所検索と店舗取得のAPI問い合わせだけに使い、保存はしません。")],
    rel=[("kaibatsu-check","⛰️","うちの海抜チェッカー"),("yachin-tekisei","🏠","適正家賃チェック"),("hikkoshi-hiyou","🚚","引っ越し費用"),("hitorigurashi","📦","ひとり暮らし初期費用")],
    body="""  <section class="panel">
    <h2>🏪 場所をえらぶ</h2>
    <div class="field"><label>住所・駅名・地名 <span class="hint">（例: 中野駅）</span></label><input type="text" id="q" placeholder="住所や駅名を入力" autocomplete="off"></div>
    <button class="btn btn-primary" id="searchBtn">コンビニ密度を調べる</button>
    <div id="candBox" style="margin-top:10px;"></div>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label" id="placeLabel">徒歩圏（半径500m）のコンビニは</div>
      <div class="big"><span id="big">0</span><span class="unit">軒</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">最寄り</div><div class="v" id="nearest">—</div></div>
      <div class="stat"><div class="k">半径1km圏</div><div class="v" id="km1">—</div></div>
      <div class="stat"><div class="k">密度判定</div><div class="v accent" id="judge">—</div></div></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
  const R = 6371000;
  function dist(la1, lo1, la2, lo2){
    const d = Math.PI / 180;
    const a = Math.sin((la2-la1)*d/2)**2 + Math.cos(la1*d)*Math.cos(la2*d)*Math.sin((lo2-lo1)*d/2)**2;
    return 2 * R * Math.asin(Math.sqrt(a));
  }
  async function count(lon, lat, placeName){
    $('state').textContent = '地図データからコンビニを集計中…（数秒かかります）';
    try{
      const q = '[out:json][timeout:20];node["shop"="convenience"](around:1000,' + lat + ',' + lon + ');out body;';
      const r = await fetch('https://overpass-api.de/api/interpreter?data=' + encodeURIComponent(q));
      const j = await r.json();
      const shops = (j.elements || []).map(e => ({ name: e.tags?.name || 'コンビニ', d: Math.round(dist(lat, lon, e.lat, e.lon)) })).sort((a,b) => a.d - b.d);
      const in500 = shops.filter(s => s.d <= 500);
      const judge = in500.length >= 10 ? '都会オブ都会🌃' : in500.length >= 5 ? 'かなり便利🏙️' : in500.length >= 2 ? '標準的🙂' : in500.length === 1 ? '1軒を大切に🏪' : 'コンビニ圏外…🌾';
      $('state').textContent = '';
      $('placeLabel').textContent = (placeName || 'この場所') + 'の徒歩圏（半径500m）のコンビニは';
      $('sub').textContent = 'OpenStreetMap登録店舗ベース｜500m=徒歩約6分';
      $('nearest').textContent = shops[0] ? shops[0].name + '（約' + shops[0].d + 'm）' : '1km圏内になし';
      $('km1').textContent = shops.length + '軒';
      $('judge').textContent = judge;
      SHARE = (placeName || 'うちの街') + '、徒歩圏のコンビニは' + in500.length + '軒だった🏪（判定: ' + judge + '）\\nあなたの街は何軒？👇';
      show(); anim($('big'), 0, in500.length, 900);
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
})();"""
))

# ============================================================ 5 ロケット
SIMS.append(dict(
    slug="rocket-uchiage", cat="wonder", catjp="ふしぎ・現象", grad="linear-gradient(135deg,#eef2ff,#e0e7ff)", emoji="🚀",
    title="次のロケット打ち上げまで", score=72,
    card_desc="人類の次の打ち上げは何時間後？世界のロケット打ち上げ予定をライブカウントダウン。",
    title_tag="次のロケット打ち上げカウントダウン｜世界の打ち上げ予定ライブ",
    meta_desc="世界の次のロケット打ち上げまでの残り時間を、宇宙開発データベースからリアルタイムでカウントダウンする無料ツール。ミッション名・ロケット・発射場も日本時間で表示。",
    og_title="次のロケット打ち上げまで",
    og_desc="人類の次の打ち上げをライブカウントダウン。",
    lead="いまこの瞬間も、世界のどこかで秒読みが進んでいます。人類の次のロケット打ち上げまでの時間を、宇宙開発データベースからライブ表示します。",
    about_h2="このカウントダウンについて",
    about="""<p>世界では年間200回を超えるロケットが打ち上がっており、もはや「打ち上げの無い週」はほぼありません。このカウントダウンは宇宙開発オープンデータベース（The Space Devs / Launch Library 2）から直近の打ち上げ予定を取得し、日本時間に変換して表示しています。打ち上げ時刻は天候や技術的な理由で直前に変わることがあります。</p>
    <div class="note">日本の種子島・内之浦からの打ち上げが入っている日は、射点近くの見学場所やライブ配信をチェックしてみてください。</div>""",
    faqs=[("データの出典は？", "宇宙開発のオープンデータベース「Launch Library 2」（The Space Devs）から直近の打ち上げ予定を取得しています。"),
          ("時刻は正確？", "表示は取得時点の予定時刻（日本時間換算）です。打ち上げは天候等で直前に延期されることが多いため、実際の視聴は公式配信の情報にあわせてください。"),
          ("入力データは送信される？", "このページは何も入力せずに使えます。")],
    rel=[("iss-doko","🛰️","ISSはいまどこ？"),("aurora-yohou","🌌","オーロラ予報メーター"),("hoshizora-shisu","🔭","今夜の星空指数"),("galaxy-collision","🌌","銀河衝突シミュレーター")],
    body="""  <section class="panel" id="resultPanel">
    <div class="result">
      <div class="label">人類の次のロケット打ち上げまで、あと</div>
      <div class="big" style="font-size:min(13vw,58px);"><span id="big">–</span></div>
      <div class="sub" id="sub">データを読み込み中…</div>
      <div class="statline"><div class="stat"><div class="k">ロケット / ミッション</div><div class="v" id="mission">—</div></div>
      <div class="stat"><div class="k">発射場</div><div class="v" id="pad">—</div></div>
      <div class="stat"><div class="k">今後の予定（直近10件中）</div><div class="v accent" id="upcoming">—</div></div></div>
      <div id="list" style="margin-top:14px;"></div>
      <button class="btn btn-ghost" id="reloadBtn" style="margin-top:10px;">🔄 最新に更新</button>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
  const fmtJST = (iso) => new Date(iso).toLocaleString('ja-JP', { month:'numeric', day:'numeric', hour:'2-digit', minute:'2-digit', timeZone:'Asia/Tokyo' });
  let TARGET = null, TIMER = null;
  function tick(){
    if(!TARGET) return;
    let s = Math.max(0, Math.floor((TARGET - Date.now()) / 1000));
    const d = Math.floor(s / 86400); s -= d * 86400;
    const h = Math.floor(s / 3600); s -= h * 3600;
    const m = Math.floor(s / 60); s -= m * 60;
    $('big').textContent = (d ? d + '日' : '') + String(h).padStart(2,'0') + ':' + String(m).padStart(2,'0') + ':' + String(s).padStart(2,'0');
  }
  async function load(){
    $('sub').textContent = 'データを読み込み中…';
    try{
      const r = await fetch('https://ll.thespacedevs.com/2.2.0/launch/upcoming/?limit=10&mode=list');
      const j = await r.json();
      const items = (j.results || []).filter(x => x.net && new Date(x.net) > new Date());
      const nx = items[0];
      if(!nx){ $('sub').textContent = '直近の打ち上げ予定が取得できませんでした。'; return; }
      TARGET = new Date(nx.net).getTime();
      if(TIMER) clearInterval(TIMER);
      TIMER = setInterval(tick, 1000); tick();
      $('sub').textContent = '🚀 ' + nx.name + '｜日本時間 ' + fmtJST(nx.net) + ' 予定';
      $('mission').textContent = nx.name.split('|')[0].trim();
      $('pad').textContent = (nx.location || '').split(',')[0] || '—';
      $('upcoming').textContent = items.length + '件';
      $('list').innerHTML = '<div style="font-weight:800;font-size:13px;margin-bottom:8px;">📋 この先の打ち上げ予定</div>' + items.slice(1, 6).map(x =>
        '<div style="display:flex;gap:8px;justify-content:space-between;padding:7px 10px;margin-bottom:5px;background:rgba(127,127,127,.07);border-radius:8px;font-size:12.5px;text-align:left;">'
        + '<span>' + x.name.split('|').map(t => t.trim()).join('｜') + '</span><span style="opacity:.7;white-space:nowrap;">' + fmtJST(x.net) + '</span></div>').join('');
      SHARE = '人類の次のロケット打ち上げは「' + nx.name.split('|')[0].trim() + '」🚀 日本時間' + fmtJST(nx.net) + '予定！\\nライブカウントダウンはこちら👇';
    }catch{ $('sub').textContent = '⚠️ データの取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  load();
  $('reloadBtn').addEventListener('click', load);
  bindShare();
})();"""
))

# ============================================================ 6 熱帯夜
SIMS.append(dict(
    slug="nettaiya-check", cat="health", catjp="健康・カラダ", grad="linear-gradient(135deg,#fef2f2,#fee2e2)", emoji="🌙",
    title="今夜、熱帯夜？チェック", score=71,
    card_desc="今夜の最低気温をライブ取得。熱帯夜ならエアコンつけっぱなし判定も。",
    title_tag="今夜、熱帯夜？チェック｜今夜の最低気温とエアコン判定",
    meta_desc="今夜〜明朝の最低気温を予報データからリアルタイム取得し、熱帯夜（25℃以上）・超熱帯夜（28℃以上）かどうかとエアコンつけっぱなし推奨かを判定する無料ツール。",
    og_title="今夜、熱帯夜？チェック",
    og_desc="今夜の最低気温からエアコンつけっぱなし判定。",
    lead="「夜は涼しくなるかな」に予報で答えます。今夜から明朝までの最低気温を取得して、熱帯夜判定とエアコンの使い方目安を出します。",
    about_h2="この判定について",
    about="""<p>夜間の最低気温が25℃を下回らない夜を「熱帯夜」と呼びます。熱中症は夜間の屋内でも多く発生しており、特に最低気温28℃前後の「超熱帯夜」はエアコンを我慢する危険度が上がります。このチェッカーは気象オープンデータAPI（Open-Meteo）から今夜21時〜明朝6時の気温予報を取得し、最低気温と発生時刻、エアコン運転の目安を表示します。</p>
    <div class="note">高齢の家族がいる場合は、数値にかかわらず「暑さを感じにくい」前提でエアコンの活用を。電気代の目安は<a href="../aircon-denki/">エアコン電気代シミュ</a>でどうぞ。</div>""",
    faqs=[("気温データの出典は？", "気象オープンデータAPI（Open-Meteo）から、選んだ地点の今夜〜明朝の気温予報を1時間単位で取得しています。"),
          ("エアコン判定の基準は？", "最低気温25℃以上で「つけて寝るのが無難」、28℃以上で「つけっぱなし推奨」としています。環境省の熱中症予防の考え方を参考にした目安です。"),
          ("入力データは送信される？", "地域の選択のみを使います。個人情報は一切送信されません。")],
    rel=[("atsusa-ranking","🌡️","全国いま暑いランキング"),("sleep-debt","😴","睡眠負債シミュレーター"),("kuuki-kirei","🍃","空気きれいメーター"),("nidone","🛌","二度寝損失メーター")],
    body="""  <section class="panel">
    <h2>🌙 条件</h2>
    <div class="field"><label>地域</label><select id="pref"></select></div>
    <button class="btn btn-primary" id="calcBtn">今夜の判定を見る</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label">今夜の最低気温は</div>
      <div class="big"><span id="big">0</span><span class="unit">℃</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">判定</div><div class="v" id="judge">—</div></div>
      <div class="stat"><div class="k">いちばん冷える時刻</div><div class="v" id="coolest">—</div></div>
      <div class="stat"><div class="k">エアコンの目安</div><div class="v accent" id="aircon">—</div></div></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
@@PREFS_JS@@
  async function calc(){
    const p = PREFS[+$('pref').value];
    $('state').textContent = '今夜の気温予報を取得中…';
    try{
      const r = await fetch('https://api.open-meteo.com/v1/forecast?latitude=' + p[1] + '&longitude=' + p[2] + '&hourly=temperature_2m&forecast_days=2&timezone=Asia%2FTokyo');
      const j = await r.json();
      const T = j.hourly.temperature_2m;
      let min = 99, minH = 21;
      for(let h = 21; h <= 30; h++){ if(T[h] != null && T[h] < min){ min = T[h]; minH = h; } }
      const judge = min >= 28 ? '🔥 超熱帯夜級' : min >= 25 ? '🥵 熱帯夜' : min >= 20 ? '😪 寝苦しさ残る夜' : '😴 わりと眠れる夜';
      const aircon = min >= 28 ? 'つけっぱなし推奨（我慢は危険）' : min >= 25 ? 'つけて寝るのが無難' : min >= 20 ? 'タイマー2〜3時間でOK' : 'なしでもいけそう';
      $('state').textContent = '';
      $('sub').textContent = p[0] + '・今夜21時〜明朝6時の予報｜' + judge;
      $('judge').textContent = judge.replace(/^[^ ]+ /, '');
      $('coolest').textContent = (minH >= 24 ? '明朝' + (minH - 24) : minH) + '時ごろ';
      $('aircon').textContent = aircon;
      SHARE = '今夜の' + p[0] + 'の最低気温は' + min.toFixed(1) + '℃（' + judge + '）🌙 エアコンは「' + aircon + '」\\nあなたの街の今夜は？👇';
      show(); anim($('big'), 0, Math.round(min * 10) / 10, 900, 1);
    }catch{ $('state').textContent = '⚠️ 予報の取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  bindShare();
})();"""
))

# ============================================================ 7 1万円現地でいくら
SIMS.append(dict(
    slug="genchi-ikura", cat="travel", catjp="旅行・おでかけ", grad="linear-gradient(135deg,#cffafe,#a5f3fc)", emoji="💴",
    title="1万円、現地でいくら？", score=70,
    card_desc="旅行先で1万円はいくらに化ける？最新レートで即換算、1年前との比較つき。",
    title_tag="1万円、現地でいくら？｜旅行先の通貨に最新レートで即換算",
    meta_desc="旅行先を選ぶと、1万円が現地通貨でいくらになるかを最新の為替レートで即換算する無料ツール。1年前のレートとの比較で「今行くと得か損か」も体感できる。",
    og_title="1万円、現地でいくら？",
    og_desc="旅行先の通貨に最新レートで即換算。1年前との比較つき。",
    lead="旅の予算感覚は「1万円が現地でいくらか」から始まります。行き先を選ぶだけで、最新レートと1年前との比較を表示します。",
    about_h2="この換算について",
    about="""<p>このツールは欧州中央銀行（ECB）の公表レートを配信するオープンAPI（Frankfurter）から最新の為替レートと1年前の実際のレートを取得し、1万円（金額は変更可）を現地通貨に換算します。1年前より増えていれば「円が強くなった＝今行くとお得」、減っていれば「現地物価が実質値上がり」です。</p>
    <div class="note">実際の両替では手数料（数%）がかかるため、手取りはこれより少し減ります。カード決済のほうがレートが良いことも多いです。</div>""",
    faqs=[("レートの出典は？", "欧州中央銀行（ECB）公表レートを配信するオープンAPI（Frankfurter）から、最新と1年前のレートを取得しています。"),
          ("手数料は含まれる？", "含まれません。空港両替は3〜5%、カード決済は1.6〜2.2%程度の上乗せが一般的です。"),
          ("入力データは送信される？", "行き先と金額の選択のみを使います。個人情報は一切送信されません。")],
    rel=[("enyasu-taikan","💱","円安体感メーター"),("ryohi","✈️","旅行費用 総額"),("sekai-kion","🌏","世界の都市、いま何度？"),("jisa-boke","🕐","時差ボケ回復")],
    body="""  <section class="panel">
    <h2>💴 条件</h2>
    <div class="field"><label>行き先</label>
      <select id="dest">
        <option value="USD,ドル,アメリカ・ハワイ" selected>アメリカ・ハワイ（ドル）</option>
        <option value="KRW,ウォン,韓国">韓国（ウォン）</option>
        <option value="THB,バーツ,タイ">タイ（バーツ）</option>
        <option value="EUR,ユーロ,ヨーロッパ">ヨーロッパ（ユーロ）</option>
        <option value="GBP,ポンド,イギリス">イギリス（ポンド）</option>
        <option value="AUD,豪ドル,オーストラリア">オーストラリア（豪ドル）</option>
        <option value="SGD,シンガポールドル,シンガポール">シンガポール（Sドル）</option>
        <option value="CNY,元,中国">中国（元）</option>
        <option value="PHP,ペソ,フィリピン">フィリピン（ペソ）</option>
        <option value="IDR,ルピア,インドネシア・バリ">インドネシア・バリ（ルピア）</option>
        <option value="CHF,フラン,スイス">スイス（フラン）</option>
        <option value="CAD,カナダドル,カナダ">カナダ（カナダドル）</option>
      </select>
    </div>
    <div class="field"><label>持っていく金額 <span class="hint">（円）</span></label><input type="number" id="yen" value="10000" min="100" step="1000" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">現地通貨に換算する</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label" id="topLabel">その金額、現地では</div>
      <div class="big"><span id="big">0</span><span class="unit" id="unit"></span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">いまのレート</div><div class="v" id="rate">—</div></div>
      <div class="stat"><div class="k">1年前なら</div><div class="v" id="old">—</div></div>
      <div class="stat"><div class="k">1年前とくらべて</div><div class="v accent" id="diff">—</div></div></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
  const num = (n) => Math.round(n).toLocaleString('ja-JP');
  async function calc(){
    const [cur, unit, place] = $('dest').value.split(',');
    const yen = Math.max(100, +$('yen').value || 10000);
    $('state').textContent = '最新レートを取得中…';
    try{
      const d = new Date(); d.setFullYear(d.getFullYear() - 1);
      const past = d.toISOString().slice(0, 10);
      const [nowR, oldR] = await Promise.all([
        fetch('https://api.frankfurter.dev/v1/latest?base=JPY&symbols=' + cur).then(r => r.json()),
        fetch('https://api.frankfurter.dev/v1/' + past + '?base=JPY&symbols=' + cur).then(r => r.json()),
      ]);
      const rate = nowR.rates[cur], rateOld = oldR.rates[cur];
      const val = yen * rate, valOld = yen * rateOld;
      const pct = (rate / rateOld - 1) * 100;
      $('state').textContent = '';
      $('sub').textContent = place + '｜' + num(yen) + '円を換算（' + nowR.date + '時点・手数料除く）';
      $('rate').textContent = '1円=' + rate.toFixed(4) + unit;
      $('old').textContent = num(valOld) + unit;
      $('diff').textContent = (pct >= 0 ? '+' : '') + pct.toFixed(1) + '%' + (pct >= 0 ? '（円が強くなった😊）' : '（実質値上がり😢）');
      SHARE = place + 'に' + num(yen) + '円持っていくと、いま' + num(val) + unit + '💴（1年前比' + (pct>=0?'+':'') + pct.toFixed(1) + '%）\\nあなたの行き先は？👇';
      show(); anim($('big'), 0, val, 1000);
      $('unit').textContent = unit;
    }catch{ $('state').textContent = '⚠️ レートの取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  bindShare();
})();"""
))

# ============================================================ 8 世界の都市いま何度
SIMS.append(dict(
    slug="sekai-kion", cat="travel", catjp="旅行・おでかけ", grad="linear-gradient(135deg,#cffafe,#a5f3fc)", emoji="🌏",
    title="世界の都市、いま何度？", score=69,
    card_desc="ホノルルは？パリは？世界13都市の現在気温をライブで一斉表示。東京との差も。",
    title_tag="世界の都市、いま何度？｜13都市の現在気温ライブ一覧",
    meta_desc="ホノルル・バンコク・パリ・ニューヨークなど世界13都市の現在気温をリアルタイムで一斉取得し、東京との差とあわせて表示する無料ツール。旅行の服装準備・海外との雑談に。",
    og_title="世界の都市、いま何度？",
    og_desc="世界13都市の現在気温をライブで一斉表示。",
    lead="東京が猛暑のいま、シドニーは冬。世界13都市の「いまの気温」を一斉取得して、地球の広さを1画面で体感します。",
    about_h2="この一覧について",
    about="""<p>この一覧は気象オープンデータAPI（Open-Meteo）に世界13都市の座標を一括で問い合わせ、現在気温を同時刻で取得しています。北半球と南半球で季節が逆転していることや、同じ緯度でも海流で気温が全く違うことが、ニュースの天気図より直感的に分かります。旅行前の服装準備にもどうぞ。</p>
    <div class="note">気温は現地の体感とは別物です。湿度が高いバンコクの30℃と、乾燥したロサンゼルスの30℃はまるで別の暑さです。</div>""",
    faqs=[("気温データの出典は？", "気象オープンデータAPI（Open-Meteo）から、世界13都市の現在気温を一括取得しています。"),
          ("都市は増やせる？", "リクエストがあれば追加を検討します。トップページの「リクエスト」からどうぞ。"),
          ("入力データは送信される？", "このページは何も入力せずに使えます。")],
    rel=[("genchi-ikura","💴","1万円、現地でいくら？"),("atsusa-ranking","🌡️","全国いま暑いランキング"),("jisa-boke","🕐","時差ボケ回復"),("kaigai-iju","🌏","海外移住の生活費")],
    body="""  <section class="panel" id="resultPanel">
    <div class="result">
      <div class="label">いま世界でいちばん暑いのは（13都市中）</div>
      <div class="big" style="font-size:min(11vw,52px);"><span id="big">–</span></div>
      <div class="sub" id="sub">データを読み込み中…</div>
      <div class="statline"><div class="stat"><div class="k">東京はいま</div><div class="v" id="tokyo">—</div></div>
      <div class="stat"><div class="k">いちばん寒い都市</div><div class="v" id="coldest">—</div></div>
      <div class="stat"><div class="k">最大気温差</div><div class="v accent" id="span">—</div></div></div>
      <div id="list" style="margin-top:14px;"></div>
      <button class="btn btn-ghost" id="reloadBtn" style="margin-top:10px;">🔄 最新に更新</button>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
  const CITIES = [
    ['東京','🇯🇵',35.69,139.69],['ホノルル','🇺🇸',21.31,-157.86],['バンコク','🇹🇭',13.76,100.50],['シンガポール','🇸🇬',1.35,103.82],
    ['ソウル','🇰🇷',37.57,126.98],['台北','🇹🇼',25.03,121.57],['ドバイ','🇦🇪',25.20,55.27],['パリ','🇫🇷',48.86,2.35],
    ['ロンドン','🇬🇧',51.51,-0.13],['ニューヨーク','🇺🇸',40.71,-74.01],['ロサンゼルス','🇺🇸',34.05,-118.24],['シドニー','🇦🇺',-33.87,151.21],['ヘルシンキ','🇫🇮',60.17,24.94]
  ];
  async function load(){
    $('sub').textContent = 'データを読み込み中…';
    try{
      const lats = CITIES.map(c => c[2]).join(',');
      const lons = CITIES.map(c => c[3]).join(',');
      const r = await fetch('https://api.open-meteo.com/v1/forecast?latitude=' + lats + '&longitude=' + lons + '&current=temperature_2m');
      const j = await r.json();
      const rows = j.map((x, i) => ({ name: CITIES[i][0], flag: CITIES[i][1], t: x.current.temperature_2m })).sort((a,b) => b.t - a.t);
      const tokyo = rows.find(x => x.name === '東京');
      $('sub').textContent = new Date().toLocaleTimeString('ja-JP', {hour:'2-digit',minute:'2-digit'}) + ' 時点（日本時間）の現在気温';
      $('big').textContent = rows[0].flag + rows[0].name + ' ' + rows[0].t.toFixed(1) + '℃';
      $('tokyo').textContent = tokyo.t.toFixed(1) + '℃';
      $('coldest').textContent = rows[rows.length-1].flag + rows[rows.length-1].name + '（' + rows[rows.length-1].t.toFixed(1) + '℃）';
      $('span').textContent = (rows[0].t - rows[rows.length-1].t).toFixed(1) + '℃';
      $('list').innerHTML = rows.map(x =>
        '<div style="display:flex;gap:8px;justify-content:space-between;padding:7px 10px;margin-bottom:5px;background:rgba(127,127,127,.07);border-radius:8px;font-size:12.5px;text-align:left;' + (x.name === '東京' ? 'outline:2px solid rgba(0,140,255,.4);' : '') + '">'
        + '<span>' + x.flag + ' ' + x.name + '</span><span>' + x.t.toFixed(1) + '℃（東京' + (x.t - tokyo.t >= 0 ? '+' : '') + (x.t - tokyo.t).toFixed(1) + '）</span></div>').join('');
      SHARE = 'いま世界でいちばん暑いのは' + rows[0].name + 'の' + rows[0].t.toFixed(1) + '℃🌏 東京は' + tokyo.t.toFixed(1) + '℃、いちばん寒い' + rows[rows.length-1].name + 'は' + rows[rows.length-1].t.toFixed(1) + '℃！\\n世界のいまの気温はこちら👇';
    }catch{ $('sub').textContent = '⚠️ 取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  load();
  $('reloadBtn').addEventListener('click', load);
  bindShare();
})();"""
))

# ============================================================ 9 寒暖差
SIMS.append(dict(
    slug="kion-kandansa", cat="health", catjp="健康・カラダ", grad="linear-gradient(135deg,#fef2f2,#fee2e2)", emoji="🧣",
    title="寒暖差疲労チェッカー", score=68,
    card_desc="今日の朝晩の気温差は何℃？7℃超えの「寒暖差疲労」リスクをライブ判定。",
    title_tag="寒暖差疲労チェッカー｜今日の朝晩の気温差をライブ判定",
    meta_desc="今日と明日の最高・最低気温をリアルタイム取得して、体調を崩しやすい「寒暖差7℃以上」かどうかを判定する無料ツール。服装アドバイスつき。",
    og_title="寒暖差疲労チェッカー",
    og_desc="今日の朝晩の気温差から体調リスクを判定。",
    lead="なんだか怠いのは、気温差のせいかもしれません。今日の最高・最低気温の差を取得して、寒暖差疲労のリスクと服装の目安を出します。",
    about_h2="このチェッカーについて",
    about="""<p>1日の気温差が7℃を超えると、体温調節を担う自律神経の負荷が増え、だるさ・頭痛・肩こりなどの「寒暖差疲労」が出やすくなると言われます。このチェッカーは気象オープンデータAPI（Open-Meteo）から今日と明日の最高・最低気温を取得し、気温差と対策の目安を表示します。季節の変わり目は特に要注意です。</p>
    <div class="note">症状がつらい場合は無理せず医療機関へ。このツールは環境要因の目安を示すもので、診断ではありません。</div>""",
    faqs=[("気温データの出典は？", "気象オープンデータAPI（Open-Meteo）から、選んだ地点の今日・明日の最高気温と最低気温を取得しています。"),
          ("7℃という基準は？", "寒暖差疲労の一般的な目安として使われている数字です。体感には個人差があります。"),
          ("入力データは送信される？", "地域の選択のみを使います。個人情報は一切送信されません。")],
    rel=[("nettaiya-check","🌙","今夜、熱帯夜？チェック"),("atsusa-ranking","🌡️","全国いま暑いランキング"),("sleep-debt","😴","睡眠負債シミュレーター"),("kasa-iru","☔","今日、傘いる？メーター")],
    body="""  <section class="panel">
    <h2>🧣 条件</h2>
    <div class="field"><label>地域</label><select id="pref"></select></div>
    <button class="btn btn-primary" id="calcBtn">今日の寒暖差を見る</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label">今日の寒暖差は</div>
      <div class="big"><span id="big">0</span><span class="unit">℃</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">今日の最高 / 最低</div><div class="v" id="hilo">—</div></div>
      <div class="stat"><div class="k">明日の寒暖差</div><div class="v" id="tomorrow">—</div></div>
      <div class="stat"><div class="k">服装の目安</div><div class="v accent" id="wear">—</div></div></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
@@PREFS_JS@@
  async function calc(){
    const p = PREFS[+$('pref').value];
    $('state').textContent = '今日の気温予報を取得中…';
    try{
      const r = await fetch('https://api.open-meteo.com/v1/forecast?latitude=' + p[1] + '&longitude=' + p[2] + '&daily=temperature_2m_max,temperature_2m_min&forecast_days=2&timezone=Asia%2FTokyo');
      const j = await r.json();
      const hi = j.daily.temperature_2m_max[0], lo = j.daily.temperature_2m_min[0];
      const hi2 = j.daily.temperature_2m_max[1], lo2 = j.daily.temperature_2m_min[1];
      const diff = hi - lo, diff2 = hi2 - lo2;
      const judge = diff >= 10 ? '⚠️ 大きい（自律神経に堪える日）' : diff >= 7 ? '🟡 やや大きい（寒暖差疲労ゾーン）' : '🟢 おだやか';
      const wear = diff >= 7 ? '脱ぎ着できる羽織りもの必須' : hi >= 28 ? '半袖+日よけで OK' : hi >= 20 ? '長袖1枚が快適' : hi >= 12 ? '軽めのアウターを' : 'しっかり防寒を';
      $('state').textContent = '';
      $('sub').textContent = p[0] + '・今日の予報｜' + judge;
      $('hilo').textContent = hi.toFixed(1) + '℃ / ' + lo.toFixed(1) + '℃';
      $('tomorrow').textContent = diff2.toFixed(1) + '℃' + (diff2 >= 7 ? '（明日も注意）' : '');
      $('wear').textContent = wear;
      SHARE = '今日の' + p[0] + 'の寒暖差は' + diff.toFixed(1) + '℃🧣（' + judge.replace(/^[^ ]+ /,'') + '）だるいのは気温のせいかも。\\nあなたの街は？👇';
      show(); anim($('big'), 0, Math.round(diff * 10) / 10, 900, 1);
    }catch{ $('state').textContent = '⚠️ 予報の取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  bindShare();
})();"""
))

# ============================================================ 10 ゲレンデ積雪
SIMS.append(dict(
    slug="gelande-yuki", cat="sports", catjp="スポーツ・運動", grad="linear-gradient(135deg,#ecfdf5,#d1fae5)", emoji="⛷️",
    title="ゲレンデ積雪ライブ", score=67,
    card_desc="ニセコ・白馬・苗場…主要スキー場のいまの積雪と直近の降雪をライブ表示。",
    title_tag="ゲレンデ積雪ライブ｜主要スキー場のいまの積雪・新雪をチェック",
    meta_desc="ニセコ・ルスツ・白馬・苗場・野沢温泉など主要スキー場の現在の積雪深と直近24時間・7日間の降雪量を気象データからライブ表示する無料ツール。遠征の判断に。",
    og_title="ゲレンデ積雪ライブ",
    og_desc="主要スキー場のいまの積雪・新雪をライブ表示。",
    lead="遠征の判断は雪の量がすべて。主要スキー場の現在の積雪深と、直近の降雪をライブ表示します。夏は「まだ雪ある？」の答え合わせに。",
    about_h2="このライブについて",
    about="""<p>このツールは気象オープンデータAPI（Open-Meteo）から、各スキー場エリアの積雪深（snow depth）と降雪量の推計値を取得しています。「昨晩どれだけ積もったか」はパウダー狙いの生命線、「7日間の降雪」はベースの底上げの目安です。オフシーズンは軒並み0cmになりますが、それもまた季節の観測です。</p>
    <div class="note">数値は気象モデルによる山域の推計で、ゲレンデ整備後の実測とは差があります。遠征前はスキー場公式の積雪情報とライブカメラを必ず確認してください。</div>""",
    faqs=[("積雪データの出典は？", "気象オープンデータAPI（Open-Meteo）の積雪深・降雪量の推計値を、各スキー場エリアの座標で取得しています。"),
          ("スキー場公式の発表と違う", "公式発表はコース上の実測、こちらは気象モデルの山域推計のため差が出ます。傾向（増えた/減った）の把握にお使いください。"),
          ("入力データは送信される？", "スキー場の選択のみを使います。個人情報は一切送信されません。")],
    rel=[("naminori-biyori","🏄","波乗り日和チェッカー"),("hoshizora-shisu","🔭","今夜の星空指数"),("onsen-seiha","♨️","全国制覇まで何年？"),("kisei-hiyou","🚄","帰省費用シミュレーター")],
    body="""  <section class="panel">
    <h2>⛷️ ゲレンデ</h2>
    <div class="field"><label>スキー場エリア</label>
      <select id="spot">
        <option value="42.86,140.70" selected>ニセコ（北海道）</option>
        <option value="42.75,140.90">ルスツ（北海道）</option>
        <option value="38.16,140.44">蔵王（山形）</option>
        <option value="36.92,138.44">野沢温泉（長野）</option>
        <option value="36.74,137.84">白馬八方尾根（長野）</option>
        <option value="36.70,138.50">志賀高原（長野）</option>
        <option value="36.85,138.79">苗場（新潟）</option>
        <option value="36.88,138.16">妙高（新潟）</option>
      </select>
    </div>
    <button class="btn btn-primary" id="calcBtn">いまの雪を見る</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label">いまの積雪は</div>
      <div class="big"><span id="big">0</span><span class="unit">cm</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">直近24時間の降雪</div><div class="v" id="new24">—</div></div>
      <div class="stat"><div class="k">直近7日間の降雪</div><div class="v" id="new7">—</div></div>
      <div class="stat"><div class="k">シーズン判定</div><div class="v accent" id="season">—</div></div></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
  async function calc(){
    const [lat, lon] = $('spot').value.split(',');
    const name = $('spot').selectedOptions[0].textContent;
    $('state').textContent = '雪のデータを取得中…';
    try{
      const r = await fetch('https://api.open-meteo.com/v1/forecast?latitude=' + lat + '&longitude=' + lon + '&hourly=snow_depth&daily=snowfall_sum&past_days=7&forecast_days=1&timezone=Asia%2FTokyo');
      const j = await r.json();
      const depths = j.hourly.snow_depth;
      const nowIdx = 7 * 24 + new Date().getHours();
      const depth = (depths[nowIdx] ?? depths.findLast(v => v != null) ?? 0) * 100;
      const sf = j.daily.snowfall_sum;
      const new24 = (sf[7] ?? 0);
      const new7 = sf.slice(0, 8).reduce((a,b) => a + (b || 0), 0);
      const season = depth >= 200 ? '❄️ 極上シーズン' : depth >= 80 ? '⛷️ 滑走OKレベル' : depth >= 20 ? '🌨️ シーズン序盤/終盤' : depth > 0 ? '🌿 うっすら残雪' : '🌿 雪なし（オフシーズン）';
      $('state').textContent = '';
      $('sub').textContent = name + ' エリアの気象モデル推計｜公式発表とあわせて確認を';
      $('new24').textContent = new24.toFixed(1) + 'cm';
      $('new7').textContent = new7.toFixed(0) + 'cm';
      $('season').textContent = season;
      SHARE = 'いまの' + name.split('（')[0] + '、積雪' + Math.round(depth) + 'cm⛷️（7日間降雪' + new7.toFixed(0) + 'cm・' + season.replace(/^[^ ]+ /,'') + '）\\n主要ゲレンデのライブ積雪はこちら👇';
      show(); anim($('big'), 0, Math.round(depth), 900);
    }catch{ $('state').textContent = '⚠️ データの取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  bindShare();
})();"""
))

# ============================================================ ここから投入処理
IDX = os.path.join(ROOT, "index.html")
with io.open(IDX, encoding="utf-8") as f:
    html = f.read()
assert "sims/kasa-iru/" not in html, "既に挿入済み（中止）"

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
    js = s["js"].replace("@@JS_COMMON@@", JS_COMMON).replace("@@PREFS_JS@@", PREFS_JS)
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

# ---------- 既存API連携15本に引用ブロックを追記 ----------
EXISTING = {
    "renkyuu-maker": "9連休メーカー", "kaibatsu-check": "うちの海抜チェッカー", "hiyake-timer": "日焼けタイマー",
    "enyasu-taikan": "円安体感メーター", "jishin-live": "日本はいまも揺れている",
    "hoshizora-shisu": "今夜の星空指数", "sentaku-kawaku": "洗濯物 乾く時間メーター", "kuuki-kirei": "空気きれいメーター",
    "iss-doko": "ISSはいまどこ？", "sekai-yasumi": "今日、世界のどこが祝日？", "btc-tara": "もしビットコイン買ってたら",
    "tanjobi-jiken": "あなたの誕生日、何が起きた日？", "aurora-yohou": "オーロラ予報メーター",
    "naminori-biyori": "波乗り日和チェッカー", "yuyake-yohou": "今日の夕焼け予報",
}
CITE_TPL = """<h2>引用・転載について</h2>
    <p>本ページの計算結果・数値は、<b>出典を明記いただければ</b>ブログ・ニュース記事・SNS・社内資料への引用を歓迎します。事前連絡は不要です。</p>
    <div class="note">推奨クレジット表記：<code>出典：シミュラボ「%s」 https://shimulabo.com/sims/%s/</code><br>Webでご利用の際は上記URLへのリンク設置をお願いします。</div>
    <h2>よくある質問</h2>"""
for slug, title in EXISTING.items():
    p = os.path.join(ROOT, "sims", slug, "index.html")
    with io.open(p, encoding="utf-8") as f:
        s = f.read()
    if "引用・転載について" in s:
        continue
    assert "<h2>よくある質問</h2>" in s, slug
    s = s.replace("<h2>よくある質問</h2>", CITE_TPL % (title, slug), 1)
    with io.open(p, "w", encoding="utf-8") as f:
        f.write(s)
    print("cite block added:", slug)

# ---------- OGP画像 ----------
gen_path = os.path.join(SCRIPTS, "gen_images.py")
gen_src = io.open(gen_path, encoding="utf-8").read()
defs_only = gen_src.split("\nSIMS = [")[0]
ns = {"__file__": gen_path}
exec(compile(defs_only, gen_path, "exec"), ns)
for s in SIMS:
    ns["make_ogp"](os.path.join(ROOT, "ogp", s["slug"] + ".png"), s["title"], s["catjp"])
ns["make_ogp"](os.path.join(ROOT, "ogp", "live.png"), "ライブデータラボ", "リアルタイムAPI搭載")

# ---------- index.html: 特集シェルフ + カード + ランキング + 本数 ----------
LIVE_FEATURED = [
    ("atsusa-ranking","🌡️","全国いま暑いランキング"), ("kasa-iru","☔","今日、傘いる？メーター"),
    ("jishin-live","🗾","日本はいまも揺れている"), ("iss-doko","🛰️","ISSはいまどこ？"),
    ("tsugi-renkyuu","📅","次の3連休カウントダウン"), ("btc-tara","🪙","もしビットコイン買ってたら"),
    ("hoshizora-shisu","🔭","今夜の星空指数"), ("rocket-uchiage","🚀","次のロケット打ち上げまで"),
]
shelf = """
  <section class="rank-wrap" id="liveShelf">
    <div class="rank-head">
      <h2>⚡ ライブデータ搭載シミュ</h2>
      <span class="note">いまの実データで動く</span>
    </div>
    <div class="related-grid">""" + "".join(
    '<a class="related-card" href="sims/%s/"><span class="e">%s</span><span>%s</span></a>' % (s, e, t) for s, e, t in LIVE_FEATURED
) + """</div>
    <div style="margin-top:10px;text-align:right;"><a href="live/" style="font-weight:800;font-size:13px;">🛰️ ライブデータ搭載を全部見る →</a></div>
  </section>
"""
rank_end = html.index('</section>', html.index('rank-wrap')) + len('</section>')
html = html[:rank_end] + shelf + html[rank_end:]

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
assert marker in html
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
print("patched index.html: shelf + %d cards, count=%d" % (len(SIMS), cnt + len(SIMS)))

# ---------- sitemap ----------
SM = os.path.join(ROOT, "sitemap.xml")
with io.open(SM, encoding="utf-8") as f:
    sm = f.read()
entries = "  <url><loc>https://shimulabo.com/live/</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>\n" % TODAY
entries += "".join(
    "  <url><loc>https://shimulabo.com/sims/%s/</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>\n" % (s["slug"], TODAY)
    for s in SIMS)
sm = sm.replace("</urlset>", entries + "</urlset>")
with io.open(SM, "w", encoding="utf-8") as f:
    f.write(sm)
print("patched sitemap.xml: +%d urls" % (len(SIMS) + 1))
print("ALL DONE (live/ hub is generated by gen_live_hub.py)")
