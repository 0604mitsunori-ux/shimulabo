# -*- coding: utf-8 -*-
"""API連携シリーズ第2弾 10本を生成して一括投入（1回限り）。
   sims/生成（og:image込み）→ OGP画像 → index.html（カード/ランキング/本数）→ sitemap.xml
"""
import os, io, re, json

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPTS)
TODAY = "2026-08-20"

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
    <a class="back" href="../../">← 一覧へ</a>
  </div>
</header>

<main class="wrap">

  <nav class="breadcrumb" aria-label="breadcrumb"><a href="../../">ホーム</a><span>›</span>@@CATJP@@<span>›</span><span class="cur">@@H1@@</span></nav>

  <div class="sim-head">
    <div class="cat">@@CATJP@@</div>
    <h1>@@H1@@</h1>
    <p class="lead">@@LEAD@@</p>
  </div>

@@BODY@@

  <article class="article">
    <h2>@@ABOUT_H2@@</h2>
    @@ABOUT@@
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
    <p><a href="../../">← シミュラボ トップへ戻る</a></p>
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

PREFS_JS = """  const PREFS = [
    ['北海道(札幌)',43.06,141.35],['青森県',40.82,140.74],['岩手県',39.70,141.15],['宮城県(仙台)',38.27,140.87],
    ['秋田県',39.72,140.10],['山形県',38.24,140.36],['福島県',37.75,140.47],['茨城県',36.34,140.45],
    ['栃木県',36.57,139.88],['群馬県',36.39,139.06],['埼玉県',35.86,139.65],['千葉県',35.61,140.12],
    ['東京都',35.69,139.69],['神奈川県(横浜)',35.45,139.64],['新潟県',37.90,139.02],['富山県',36.70,137.21],
    ['石川県(金沢)',36.59,136.63],['福井県',36.07,136.22],['山梨県',35.66,138.57],['長野県',36.65,138.18],
    ['岐阜県',35.39,136.72],['静岡県',34.98,138.38],['愛知県(名古屋)',35.18,136.91],['三重県',34.73,136.51],
    ['滋賀県',35.00,135.87],['京都府',35.02,135.76],['大阪府',34.69,135.52],['兵庫県(神戸)',34.69,135.18],
    ['奈良県',34.69,135.83],['和歌山県',34.23,135.17],['鳥取県',35.50,134.24],['島根県(松江)',35.47,133.05],
    ['岡山県',34.66,133.93],['広島県',34.40,132.46],['山口県',34.19,131.47],['徳島県',34.07,134.56],
    ['香川県(高松)',34.34,134.04],['愛媛県(松山)',33.84,132.77],['高知県',33.56,133.53],['福岡県',33.61,130.42],
    ['佐賀県',33.25,130.30],['長崎県',32.74,129.87],['熊本県',32.79,130.74],['大分県',33.24,131.61],
    ['宮崎県',31.91,131.42],['鹿児島県',31.56,130.56],['沖縄県(那覇)',26.21,127.68]
  ];
  $('pref').innerHTML = PREFS.map((p,i) => '<option value="' + i + '"' + (i===12?' selected':'') + '>' + p[0] + '</option>').join('');"""

def faq_dl(faqs):
    return "".join("<dt>%s</dt><dd>%s</dd>" % (q, a) for q, a in faqs)

def faq_ld(faqs):
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in faqs
    ]}, ensure_ascii=False)

def related(items):
    return "".join('<a class="related-card" href="../%s/"><span class="e">%s</span><span>%s</span></a>' % (s, e, t) for s, e, t in items)

SIMS = []

# ============================================================ 1
SIMS.append(dict(
    slug="hoshizora-shisu", cat="travel", catjp="旅行・おでかけ", grad="linear-gradient(135deg,#cffafe,#a5f3fc)", emoji="🔭",
    title="今夜の星空指数", score=66,
    card_desc="今夜、星は見える？雲量予報×月の明るさから星空指数を計算。ベスト時間帯も。",
    title_tag="今夜の星空指数｜雲量×月齢から「星が見えるか」を計算",
    meta_desc="今夜のリアルタイム雲量予報と月の満ち欠けから、星空がどれだけ見えるかを0〜100の指数で計算する無料シミュレーター。都道府県を選ぶだけ。天体観測・キャンプのお供に。",
    og_title="今夜の星空指数｜今夜、星は見える？",
    og_desc="雲量予報×月の明るさで星空指数を計算。",
    lead="今夜、星は見えるのか。選んだ地域の今夜の雲量予報をリアルタイム取得し、月の明るさも計算に入れて「星空指数」を出します。",
    about_h2="この指数について",
    about="""<p>星が見えるかどうかは「雲」と「月」でほぼ決まります。この指数は、気象オープンデータAPI（Open-Meteo）から今夜21時〜翌1時の雲量予報を取得し、さらに月齢から計算した月の明るさで補正して0〜100点にしたものです。満月の夜は空が明るく、天の川クラスの淡い星は見えにくくなります。</p>
    <div class="note">街灯りの影響（光害）は場所によって大きく異なるため含めていません。同じ指数でも、山や海辺に行くほど見える星は増えます。</div>""",
    faqs=[("雲量データはどこから？", "気象オープンデータAPI（Open-Meteo）から、選んだ地点の今夜の雲量予報を1時間単位で取得しています。"),
          ("月の明るさはどう計算？", "月齢周期（約29.53日）から満ち欠けを計算し、満月に近いほど指数が下がる補正をかけています。"),
          ("入力データは送信される？", "地域の選択のみを気象APIへの問い合わせに使います。個人情報は一切送信されません。")],
    rel=[("iss-doko","🛰️","ISSはいまどこ？"),("yuyake-yohou","🌇","今日の夕焼け予報"),("onsen-seiha","♨️","全国制覇まで何年？"),("ryohi","✈️","旅行費用 総額")],
    body="""  <section class="panel">
    <h2>🔭 条件</h2>
    <div class="field"><label>地域</label><select id="pref"></select></div>
    <button class="btn btn-primary" id="calcBtn">今夜の星空指数を見る</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label">今夜の星空指数は</div>
      <div class="big"><span id="big">0</span><span class="unit">点</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">今夜の雲量</div><div class="v" id="cloud">—</div></div>
      <div class="stat"><div class="k">月齢</div><div class="v" id="moon">—</div></div>
      <div class="stat"><div class="k">ベスト時間帯</div><div class="v accent" id="best">—</div></div></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
@@PREFS_JS@@
  const moonAge = () => ((Date.now() - 947182440000) / 86400000) % 29.530588853;
  const moonName = (a) => a < 1.85 ? '新月' : a < 5.5 ? '三日月ごろ' : a < 9.2 ? '上弦ごろ' : a < 12.9 ? '十三夜ごろ' : a < 16.6 ? '満月ごろ' : a < 20.3 ? '寝待月ごろ' : a < 24 ? '下弦ごろ' : a < 27.7 ? '有明月ごろ' : '新月';
  async function calc(){
    const p = PREFS[+$('pref').value];
    $('state').textContent = '今夜の雲量予報を取得中…';
    try{
      const r = await fetch('https://api.open-meteo.com/v1/forecast?latitude=' + p[1] + '&longitude=' + p[2] + '&hourly=cloud_cover&forecast_days=2&timezone=Asia%2FTokyo');
      const j = await r.json();
      const cc = j.hourly.cloud_cover;
      const hours = [20,21,22,23,24];
      const vals = hours.map(h => cc[h]).filter(v => v != null);
      const avg = vals.reduce((a,b)=>a+b,0) / vals.length;
      let bestH = 20, bestC = 101;
      hours.forEach(h => { if(cc[h] != null && cc[h] < bestC){ bestC = cc[h]; bestH = h; } });
      const age = moonAge();
      const illum = (1 - Math.cos(2 * Math.PI * age / 29.530588853)) / 2;
      const score = Math.max(0, Math.round((100 - avg) * (1 - 0.55 * illum)));
      const label = score >= 80 ? '満天チャンス✨' : score >= 60 ? 'よく見えそう' : score >= 40 ? '明るい星なら見える' : score >= 20 ? '今夜は厳しめ' : '今夜は絶望的…';
      $('state').textContent = '';
      $('sub').textContent = p[0] + '・今夜21時〜翌1時の予報｜判定: ' + label;
      $('cloud').textContent = Math.round(avg) + '%';
      $('moon').textContent = age.toFixed(1) + '（' + moonName(age) + '）';
      $('best').textContent = (bestH >= 24 ? (bestH-24) : bestH) + '時ごろ（雲量' + Math.round(bestC) + '%）';
      SHARE = '今夜の' + p[0] + 'の星空指数は' + score + '点（' + label + '）🔭 雲量' + Math.round(avg) + '%・' + moonName(age) + '。あなたの街の空は？👇';
      show(); anim($('big'), 0, score, 900);
    }catch{ $('state').textContent = '⚠️ 予報の取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  bindShare();
})();"""
))

# ============================================================ 2
SIMS.append(dict(
    slug="sentaku-kawaku", cat="home", catjp="住まい・暮らし", grad="linear-gradient(135deg,#ecfdf5,#d1fae5)", emoji="👕",
    title="洗濯物 乾く時間メーター", score=65,
    card_desc="今日干すと何時間で乾く？湿度・気温・風の予報から乾燥時間と「干しどき」を計算。",
    title_tag="洗濯物 乾く時間メーター｜今日の湿度・風から乾燥時間を計算",
    meta_desc="今日の湿度・気温・風速の予報から「外干しで何時間で乾くか」と一番乾く干し始め時刻を計算する無料シミュレーター。雨リスクの警告つき。都道府県を選ぶだけ。",
    og_title="洗濯物 乾く時間メーター｜今日は何時間で乾く？",
    og_desc="湿度・気温・風の予報から乾燥時間と干しどきを計算。",
    lead="「今日って外干しで乾く日？」を数字で。今日の湿度・気温・風速の予報から、乾くまでの時間と一番得する干し始め時刻を計算します。",
    about_h2="この計算について",
    about="""<p>洗濯物の乾きやすさは、湿度が低いほど・気温が高いほど・風が強いほど上がります。このメーターは気象オープンデータAPI（Open-Meteo）から今日の1時間ごとの湿度・気温・風速・降水確率を取得し、時間ごとの「乾燥パワー」を積み上げて、乾くまでの時間を試算します。干し始めの時刻を変えながら、今日いちばん早く乾くスタート時刻も探します。</p>
    <div class="note">日当たりや干し方（ピンチ間隔・裏返し）でも実際の時間は変わります。数値は外干し・日なた想定の目安です。</div>""",
    faqs=[("気象データはどこから？", "気象オープンデータAPI（Open-Meteo）から、選んだ地点の今日の湿度・気温・風速・降水確率を1時間単位で取得しています。"),
          ("部屋干しには使える？", "この計算は外干し想定です。部屋干しは風がほぼゼロになるため、表示より大幅に長くかかります（除湿機・扇風機併用がおすすめ）。"),
          ("入力データは送信される？", "地域の選択のみを気象APIへの問い合わせに使います。個人情報は一切送信されません。")],
    rel=[("kaji-jikan","🧹","家事の生涯時間"),("denki-setsuyaku","💡","電気代 節約"),("kounetsu","🧾","光熱費の平均"),("hiyake-timer","☀️","日焼けタイマー")],
    body="""  <section class="panel">
    <h2>👕 条件</h2>
    <div class="field"><label>地域</label><select id="pref"></select></div>
    <div class="field"><label>洗濯物の厚さ</label>
      <select id="thick"><option value="4.5" selected>ふつう（Tシャツ・タオル中心）</option><option value="7.5">厚手あり（パーカー・ジーンズ・バスタオル）</option></select>
    </div>
    <button class="btn btn-primary" id="calcBtn">今日の乾き時間を計算</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label" id="topLabel">いちばん良い時間に干すと、乾くまで</div>
      <div class="big"><span id="big">0</span><span class="unit" id="unit">時間</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">ベストの干し始め</div><div class="v" id="best">—</div></div>
      <div class="stat"><div class="k">日中の平均湿度</div><div class="v" id="hum">—</div></div>
      <div class="stat"><div class="k">雨リスク</div><div class="v accent" id="rain">—</div></div></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
@@PREFS_JS@@
  async function calc(){
    const p = PREFS[+$('pref').value];
    const need = +$('thick').value;
    $('state').textContent = '今日の予報を取得中…';
    try{
      const r = await fetch('https://api.open-meteo.com/v1/forecast?latitude=' + p[1] + '&longitude=' + p[2] + '&hourly=relative_humidity_2m,temperature_2m,wind_speed_10m,precipitation_probability&forecast_days=1&timezone=Asia%2FTokyo');
      const j = await r.json();
      const RH = j.hourly.relative_humidity_2m, T = j.hourly.temperature_2m, W = j.hourly.wind_speed_10m, PP = j.hourly.precipitation_probability;
      const power = (h) => Math.max(0.15, (100 - RH[h]) / 40) * (1 + 0.10 * (W[h] || 0)) * Math.max(0.4, 1 + (T[h] - 15) / 25);
      // 8〜14時の各スタートで乾き終わり時刻を試算（20時まで）
      let best = null;
      for(let s = 8; s <= 14; s++){
        let acc = 0, end = null;
        for(let h = s; h <= 20; h++){
          acc += power(h);
          if(acc >= need){ end = h + 1 - (acc - need) / power(h); break; }
        }
        if(end != null && (!best || end - s < best.dur)){ best = { s, dur: end - s, end }; }
      }
      const maxPP = Math.max(...PP.slice(8, 19).filter(v => v != null));
      const avgRH = Math.round(RH.slice(9, 17).reduce((a,b)=>a+b,0) / 8);
      $('state').textContent = '';
      if(!best){
        $('topLabel').textContent = '今日は…';
        $('big').textContent = '乾き切らない';
        $('unit').textContent = '';
        $('sub').textContent = p[0] + '・今日は外干しでは夜までに乾かない予報です（部屋干し＋除湿がおすすめ）';
        $('best').textContent = '—';
      }else{
        const hh = Math.floor(best.dur), mm = Math.round((best.dur - hh) * 60);
        $('topLabel').textContent = 'いちばん良い時間に干すと、乾くまで';
        $('unit').textContent = '時間';
        $('big').textContent = '0';
        $('sub').textContent = p[0] + '・' + best.s + '時に干すと ' + hh + '時間' + (mm ? mm + '分' : '') + ' で乾く計算（' + Math.round(best.end) + '時ごろ取り込み）';
        $('best').textContent = best.s + '時スタート';
        show(); anim($('big'), 0, Math.round(best.dur * 10) / 10, 900, 1);
      }
      $('hum').textContent = avgRH + '%';
      $('rain').textContent = maxPP >= 50 ? '⚠️ 高い（' + maxPP + '%）取り込み注意' : maxPP >= 30 ? 'やや注意（' + maxPP + '%）' : '低い（' + maxPP + '%）';
      SHARE = best
        ? '今日の' + p[0] + '、洗濯物は' + best.s + '時に干すと約' + (Math.round(best.dur*10)/10) + '時間で乾くらしい👕 あなたの街の干しどきは？👇'
        : '今日の' + p[0] + '、外干しでは乾き切らない予報…👕 あなたの街は？👇';
      if(!best){ show(); }
    }catch{ $('state').textContent = '⚠️ 予報の取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  bindShare();
})();"""
))

# ============================================================ 3
SIMS.append(dict(
    slug="kuuki-kirei", cat="health", catjp="健康・カラダ", grad="linear-gradient(135deg,#fef2f2,#fee2e2)", emoji="🍃",
    title="空気きれいメーター", score=64,
    card_desc="いまの空気、吸って大丈夫？PM2.5・黄砂をリアルタイム取得して判定。",
    title_tag="空気きれいメーター｜いまのPM2.5・黄砂をリアルタイム判定",
    meta_desc="いまいる地域のPM2.5・PM10・黄砂の濃度をリアルタイムの大気質データから取得し、窓開け・外干し・運動していいかを判定する無料ツール。都道府県を選ぶだけ。",
    og_title="空気きれいメーター｜いまの空気、吸って大丈夫？",
    og_desc="PM2.5・黄砂をリアルタイム取得してきれい度を判定。",
    lead="いまの空気、どれくらいきれい？ PM2.5・PM10・黄砂の濃度をリアルタイムの大気質予測データから取得して、今日の空気を判定します。",
    about_h2="このメーターについて",
    about="""<p>PM2.5は髪の毛の太さの30分の1ほどの微粒子で、濃度が高い日は呼吸器への負担が増えるとされています。このメーターは大気質オープンデータAPI（Open-Meteo Air Quality・CAMSモデル）から、選んだ地点のPM2.5・PM10・黄砂の濃度を1時間単位で取得しています。日本の環境基準は「1日平均35μg/m³以下」です。</p>
    <div class="note">表示は数値モデルによる推計値で、最寄りの実測局の値とはズレることがあります。健康不安がある場合は自治体の実測データ（そらまめくん等）もあわせて確認してください。</div>""",
    faqs=[("データの出典は？", "大気質オープンデータAPI（Open-Meteo Air Quality、欧州CAMSモデル）から、選んだ地点の推計濃度を取得しています。"),
          ("PM2.5はどこからが「多い」？", "日本の環境基準は1日平均35μg/m³以下です。このメーターでは35を超えると「やや多い」、70を超えると「多い」と表示します。"),
          ("入力データは送信される？", "地域の選択のみを大気質APIへの問い合わせに使います。個人情報は一切送信されません。")],
    rel=[("sleep-debt","😴","睡眠負債シミュレーター"),("caffeine","☕","カフェイン残量メーター"),("hiyake-timer","☀️","日焼けタイマー"),("sentaku-kawaku","👕","洗濯物 乾く時間メーター")],
    body="""  <section class="panel">
    <h2>🍃 条件</h2>
    <div class="field"><label>地域</label><select id="pref"></select></div>
    <button class="btn btn-primary" id="calcBtn">いまの空気を判定</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label">いまのPM2.5は</div>
      <div class="big"><span id="big">0</span><span class="unit">μg/m³</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">PM10</div><div class="v" id="pm10">—</div></div>
      <div class="stat"><div class="k">黄砂</div><div class="v" id="dust">—</div></div>
      <div class="stat"><div class="k">今日のピーク</div><div class="v accent" id="peak">—</div></div></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
@@PREFS_JS@@
  async function calc(){
    const p = PREFS[+$('pref').value];
    $('state').textContent = '大気質データを取得中…';
    try{
      const r = await fetch('https://air-quality-api.open-meteo.com/v1/air-quality?latitude=' + p[1] + '&longitude=' + p[2] + '&hourly=pm2_5,pm10,dust&forecast_days=1&timezone=Asia%2FTokyo');
      const j = await r.json();
      const h = new Date().getHours();
      const pm25 = j.hourly.pm2_5[h] ?? 0, pm10 = j.hourly.pm10[h] ?? 0, dust = j.hourly.dust[h] ?? 0;
      let peak = 0, peakH = 0;
      j.hourly.pm2_5.forEach((v,i) => { if(v != null && v > peak){ peak = v; peakH = i; } });
      const label = pm25 <= 15 ? 'とてもきれい🟢 窓開け・外干し・運動ぜんぶOK' : pm25 <= 35 ? 'ふつう🙂 環境基準の範囲内です' : pm25 <= 70 ? 'やや多い😷 敏感な人は長時間の屋外運動を控えめに' : '多い⚠️ 窓開け・外干しは控えるのが無難';
      $('state').textContent = '';
      $('sub').textContent = p[0] + '・' + h + '時の推計｜' + label;
      $('pm10').textContent = Math.round(pm10) + 'μg/m³';
      $('dust').textContent = dust >= 50 ? '⚠️ 飛来中（' + Math.round(dust) + '）' : dust >= 10 ? 'うっすら（' + Math.round(dust) + '）' : 'なし';
      $('peak').textContent = Math.round(peak) + '（' + peakH + '時ごろ）';
      SHARE = 'いまの' + p[0] + 'のPM2.5は' + Math.round(pm25) + 'μg/m³🍃 ' + label.split(' ')[0] + ' あなたの街の空気は？👇';
      show(); anim($('big'), 0, Math.round(pm25), 900);
    }catch{ $('state').textContent = '⚠️ 大気質データの取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  bindShare();
})();"""
))

# ============================================================ 4
SIMS.append(dict(
    slug="iss-doko", cat="wonder", catjp="ふしぎ・現象", grad="linear-gradient(135deg,#eef2ff,#e0e7ff)", emoji="🛰️",
    title="ISSはいまどこ？", score=63,
    card_desc="国際宇宙ステーションは、いまあなたから何km？時速2.8万kmで動く位置をライブ表示。",
    title_tag="ISSはいまどこ？｜国際宇宙ステーションとの距離をライブ計算",
    meta_desc="国際宇宙ステーション（ISS）のいまの位置をリアルタイム取得して、あなたの街からの距離・高度・速度をライブ表示する無料ツール。90分で地球を1周する速さを体感。",
    og_title="ISSはいまどこ？｜あなたから何km？",
    og_desc="ISSの現在位置をライブ取得して距離を計算。",
    lead="頭の上400kmを、時速約2万8千kmで飛んでいる国際宇宙ステーション。いまどこにいて、あなたから何km離れているのかをライブで計算します。",
    about_h2="このメーターについて",
    about="""<p>ISS（国際宇宙ステーション）は高度約400kmを秒速約7.7kmで飛行し、およそ90分で地球を1周しています。このメーターは公開の衛星位置API（wheretheiss.at）からISSの現在位置を取得し、あなたの選んだ地点との距離を球面距離で計算しています。「更新」を押すたびに位置が変わる＝それだけ速く動いている、ということです。</p>
    <div class="note">距離が1,000km前後まで近づいた夜の時間帯は、条件がよければ「動く明るい星」として肉眼でも見えます（JAXAの目視予報「きぼうを見よう」が便利です）。</div>""",
    faqs=[("位置データの出典は？", "公開の衛星位置API（wheretheiss.at）から、ISSの現在の緯度・経度・高度・速度を取得しています。"),
          ("ISSは肉眼で見える？", "見えます。日の出前・日没後の空が暗い時間に上空を通過すると、飛行機より速く動く明るい光点として数分間見えます。"),
          ("入力データは送信される？", "地域の選択は距離計算だけに使い、外部には送信されません。")],
    rel=[("hoshizora-shisu","🔭","今夜の星空指数"),("jishin-live","🗾","日本はいまも揺れている"),("galaxy-collision","🌌","銀河衝突シミュレーター"),("black-hole","🕳️","ブラックホール 光の曲がり")],
    body="""  <section class="panel">
    <h2>🛰️ 条件</h2>
    <div class="field"><label>あなたの地域</label><select id="pref"></select></div>
    <button class="btn btn-primary" id="calcBtn">ISSの現在地を見る</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label">ISSはいま、あなたから</div>
      <div class="big"><span id="big">0</span><span class="unit">km</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">高度</div><div class="v" id="alt">—</div></div>
      <div class="stat"><div class="k">速度</div><div class="v" id="vel">—</div></div>
      <div class="stat"><div class="k">現在位置（緯度・経度）</div><div class="v accent" id="pos">—</div></div></div>
      <button class="btn btn-ghost" id="reloadBtn" style="margin-top:10px;">🔄 いまの位置に更新</button>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
@@PREFS_JS@@
  const R = 6371;
  function hav(la1, lo1, la2, lo2){
    const d = Math.PI / 180;
    const a = Math.sin((la2-la1)*d/2)**2 + Math.cos(la1*d)*Math.cos(la2*d)*Math.sin((lo2-lo1)*d/2)**2;
    return 2 * R * Math.asin(Math.sqrt(a));
  }
  async function calc(){
    const p = PREFS[+$('pref').value];
    $('state').textContent = 'ISSの現在位置を取得中…';
    try{
      const r = await fetch('https://api.wheretheiss.at/v1/satellites/25544');
      const j = await r.json();
      const ground = hav(p[1], p[2], j.latitude, j.longitude);
      const dist = Math.round(Math.sqrt(ground*ground + j.altitude*j.altitude));
      $('state').textContent = '';
      const tokyoOsaka = (dist / 400).toFixed(1);
      $('sub').textContent = p[0] + 'から直線距離｜東京-大阪間の約' + tokyoOsaka + '倍' + (ground < 1200 ? '｜🌟いまあなたの空のすぐ近く！' : '');
      $('alt').textContent = Math.round(j.altitude) + 'km 上空';
      $('vel').textContent = '時速' + Math.round(j.velocity).toLocaleString('ja-JP') + 'km';
      $('pos').textContent = j.latitude.toFixed(1) + ', ' + j.longitude.toFixed(1);
      SHARE = 'ISS（国際宇宙ステーション）はいま、私から' + dist.toLocaleString('ja-JP') + 'km先を時速' + Math.round(j.velocity).toLocaleString('ja-JP') + 'kmで飛行中🛰️ いまの位置はこちら👇';
      show(); anim($('big'), 0, dist, 900);
    }catch{ $('state').textContent = '⚠️ 位置の取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  $('reloadBtn').addEventListener('click', calc);
  bindShare();
})();"""
))

# ============================================================ 5
SIMS.append(dict(
    slug="sekai-yasumi", cat="work", catjp="仕事・働き方", grad="linear-gradient(135deg,#eff6ff,#dbeafe)", emoji="🌍",
    title="今日、世界のどこが祝日？", score=62,
    card_desc="あなたが働いている今日、世界のどこかは休んでいる。祝日データをライブ取得。",
    title_tag="今日、世界のどこが祝日？｜世界の祝日ライブカウンター",
    meta_desc="今日、世界のどの国が祝日で休んでいるかを公開祝日データからリアルタイム表示する無料ツール。海外取引先の「返信が来ない理由」も分かる。日本の次の祝日も表示。",
    og_title="今日、世界のどこが祝日？",
    og_desc="世界の祝日データをライブ取得。今日休んでいる国がわかる。",
    lead="あなたが働いている今日この瞬間、世界のどこかの国は祝日で休んでいます。公開祝日データベースから「今日休みの国」をライブで数えます。",
    about_h2="このカウンターについて",
    about="""<p>世界には190以上の国があり、それぞれ独自の祝日カレンダーで動いています。このカウンターは世界の祝日オープンデータAPI（Nager.Date）から直近の祝日リストを取得し、今日が祝日の国を抽出しています。海外の取引先から返信が来ない日は、だいたいこれが理由です。</p>
    <div class="note">主要国の法定祝日ベースのため、地域限定の祝日や宗教暦の休日はカバーし切れていません。「意外と毎日どこかが休んでる」ことを楽しむメーターです。</div>""",
    faqs=[("祝日データの出典は？", "世界の祝日オープンデータAPI（Nager.Date）から、直近の世界の祝日リストを取得しています。"),
          ("日本の次の祝日も分かる？", "はい。同じAPIから日本の祝日リストも取得して、次の祝日までの日数を表示します。"),
          ("入力データは送信される？", "このページは何も入力せずに使えます。個人情報は一切送信されません。")],
    rel=[("renkyuu-maker","🏖️","9連休メーカー"),("yukyu","🏖️","有給消化シミュ"),("kyuryobi","📆","あと何回給料日"),("jisa-boke","🕐","時差ボケ回復")],
    body="""  <section class="panel" id="resultPanel">
    <div class="result">
      <div class="label">今日、祝日で休んでいる国は</div>
      <div class="big"><span id="big">–</span><span class="unit">カ国</span></div>
      <div class="sub" id="sub">データを読み込み中…</div>
      <div class="statline"><div class="stat"><div class="k">直近1週間の世界の祝日</div><div class="v" id="week">—</div></div>
      <div class="stat"><div class="k">次に休む国</div><div class="v" id="next">—</div></div>
      <div class="stat"><div class="k">日本の次の祝日</div><div class="v accent" id="jp">—</div></div></div>
      <div id="list" style="margin-top:14px;"></div>
      <button class="btn btn-ghost" id="reloadBtn" style="margin-top:10px;">🔄 最新に更新</button>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
  const JA = {US:'アメリカ',GB:'イギリス',DE:'ドイツ',FR:'フランス',IT:'イタリア',ES:'スペイン',PT:'ポルトガル',NL:'オランダ',BE:'ベルギー',CH:'スイス',AT:'オーストリア',SE:'スウェーデン',NO:'ノルウェー',DK:'デンマーク',FI:'フィンランド',IS:'アイスランド',IE:'アイルランド',PL:'ポーランド',CZ:'チェコ',SK:'スロバキア',HU:'ハンガリー',RO:'ルーマニア',BG:'ブルガリア',GR:'ギリシャ',HR:'クロアチア',SI:'スロベニア',RS:'セルビア',UA:'ウクライナ',EE:'エストニア',LV:'ラトビア',LT:'リトアニア',RU:'ロシア',TR:'トルコ',CN:'中国',KR:'韓国',JP:'日本',TW:'台湾',HK:'香港',SG:'シンガポール',TH:'タイ',VN:'ベトナム',ID:'インドネシア',MY:'マレーシア',PH:'フィリピン',IN:'インド',AU:'オーストラリア',NZ:'ニュージーランド',CA:'カナダ',MX:'メキシコ',BR:'ブラジル',AR:'アルゼンチン',CL:'チリ',CO:'コロンビア',PE:'ペルー',ZA:'南アフリカ',EG:'エジプト',NG:'ナイジェリア',KE:'ケニア',MA:'モロッコ',BO:'ボリビア',PY:'パラグアイ',UY:'ウルグアイ',VE:'ベネズエラ',CR:'コスタリカ',PA:'パナマ',DO:'ドミニカ共和国',GT:'グアテマラ',HN:'ホンジュラス',NI:'ニカラグア',SV:'エルサルバドル',CU:'キューバ',JM:'ジャマイカ',LU:'ルクセンブルク',MT:'マルタ',CY:'キプロス',AL:'アルバニア',MK:'北マケドニア',BA:'ボスニア',ME:'モンテネグロ',MD:'モルドバ',BY:'ベラルーシ',GE:'ジョージア',AM:'アルメニア',AZ:'アゼルバイジャン',KZ:'カザフスタン',UZ:'ウズベキスタン',MN:'モンゴル',PG:'パプアニューギニア'};
  const flag = (cc) => String.fromCodePoint(...[...cc].map(c => 0x1F1E6 + c.charCodeAt(0) - 65));
  const cname = (cc) => JA[cc] || cc;
  const today = () => { const d = new Date(); return d.getFullYear() + '-' + String(d.getMonth()+1).padStart(2,'0') + '-' + String(d.getDate()).padStart(2,'0'); };
  async function load(){
    $('sub').textContent = 'データを読み込み中…';
    try{
      const [world, jp] = await Promise.all([
        fetch('https://date.nager.at/api/v3/NextPublicHolidaysWorldwide').then(r => r.json()),
        fetch('https://date.nager.at/api/v3/NextPublicHolidays/JP').then(r => r.json()),
      ]);
      const t = today();
      const todays = world.filter(x => x.date === t);
      const codes = [...new Set(todays.map(x => x.countryCode))];
      const week = new Set(world.map(x => x.countryCode)).size;
      $('sub').textContent = t + ' 時点｜あなたが働いている今日、' + (codes.length ? 'この国々は休みです' : '主要国はだいたい働いています');
      $('week').textContent = world.length + '件';
      const nx = world.find(x => x.date > t);
      $('next').textContent = nx ? flag(nx.countryCode) + cname(nx.countryCode) + '（' + nx.date.slice(5).replace('-','/') + '）' : '—';
      if(jp && jp[0]){
        const days = Math.ceil((new Date(jp[0].date) - new Date(t)) / 86400000);
        $('jp').textContent = jp[0].date.slice(5).replace('-','/') + ' ' + jp[0].localName + '（あと' + days + '日）';
      }
      $('list').innerHTML = codes.length
        ? '<div style="font-weight:800;font-size:13px;margin-bottom:8px;">🎉 今日休んでいる国</div>' + todays.slice(0,12).map(x =>
          '<div style="display:flex;gap:8px;justify-content:space-between;padding:7px 10px;margin-bottom:5px;background:rgba(127,127,127,.07);border-radius:8px;font-size:12.5px;text-align:left;">'
          + '<span>' + flag(x.countryCode) + ' ' + cname(x.countryCode) + '</span><span style="opacity:.75;">' + x.localName + '</span></div>').join('')
        : '';
      SHARE = codes.length
        ? '私が働いてる今日、世界では' + codes.length + 'カ国が祝日で休んでた🌍 ' + codes.slice(0,3).map(c => flag(c) + cname(c)).join('・') + '…今日はどこが休み？👇'
        : '今日は世界の主要国がだいたい働いてる日らしい🌍 次に休む国はどこ？👇';
      anim($('big'), 0, codes.length, 800);
    }catch{ $('sub').textContent = '⚠️ 祝日データの取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  load();
  $('reloadBtn').addEventListener('click', load);
  bindShare();
})();"""
))

# ============================================================ 6
SIMS.append(dict(
    slug="btc-tara", cat="money", catjp="お金・時間", grad="linear-gradient(135deg,#fff1f2,#ffe4e6)", emoji="🪙",
    title="もしビットコイン買ってたら", score=61,
    card_desc="1年前にビットコインを買ってたら、いまいくら？実際の価格データでタラレバを清算。",
    title_tag="もしビットコイン買ってたらメーター｜実際の価格データでタラレバ計算",
    meta_desc="「あの時ビットコインを買ってたら」を実際の過去1年の価格データで計算する娯楽シミュレーター。金額と時期を選ぶだけで、いまの価値と損益をリアルタイム表示。投資助言ではありません。",
    og_title="もしビットコイン買ってたらメーター",
    og_desc="実際の価格データでタラレバを清算。増えたか減ったかは時期しだい。",
    lead="「あの時買ってれば…」を、実際の価格データで清算します。金額と時期を選ぶだけ。増えているか減っているかは、選んだ時期しだいです。",
    about_h2="このメーターについて",
    about="""<p>暗号資産の価格ニュースは「上がった」「下がった」の切り取りばかりで、自分ごとの金額に直してくれません。このメーターは公開の価格データAPI（CoinGecko）から過去1年分のビットコイン円建て価格を取得し、「その時◯円分買っていたら今いくらか」を機械的に計算します。夢が見られる日もあれば、現実を突きつけられる日もあります。</p>
    <div class="note">⚠️ これは娯楽用の計算ツールであり、投資助言ではありません。暗号資産は価格変動が非常に大きく、過去の値動きは将来を保証しません。取引には手数料・税金もかかります。</div>""",
    faqs=[("価格データの出典は？", "公開の暗号資産価格API（CoinGecko）から、過去1年分のビットコイン円建て日次価格を取得しています。"),
          ("投資の参考にしていい？", "いいえ。これは「タラレバ」を数字にして遊ぶ娯楽ツールで、投資助言ではありません。投資判断はご自身の責任で、必要なら専門家にご相談ください。"),
          ("なぜ1年前まで？", "無料APIで取得できる履歴が直近365日分のためです。")],
    rel=[("takarakuji","🎰","宝くじ買い続けたら"),("fire","🔥","FIRE達成シミュレーター"),("infure","📉","物価2倍まで何年？"),("enyasu-taikan","💱","円安体感メーター")],
    body="""  <section class="panel">
    <h2>🪙 条件</h2>
    <div class="field"><label>いくら分買っていた？</label>
      <select id="amount"><option value="10000">1万円</option><option value="100000" selected>10万円</option><option value="1000000">100万円</option><option value="custom">自分で入力</option></select>
    </div>
    <div class="field" id="customField" style="display:none"><label>金額 <span class="hint">（円）</span></label><input type="number" id="customYen" value="50000" min="100" inputmode="numeric"></div>
    <div class="field"><label>いつ買っていた？</label>
      <select id="when"><option value="365" selected>1年前</option><option value="180">半年前</option><option value="90">3ヶ月前</option><option value="30">1ヶ月前</option><option value="7">先週</option></select>
    </div>
    <button class="btn btn-primary" id="calcBtn">タラレバを清算する</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label" id="topLabel">その買い物、いまの価値は</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">損益</div><div class="v" id="pl">—</div></div>
      <div class="stat"><div class="k">変化率</div><div class="v" id="pct">—</div></div>
      <div class="stat"><div class="k">期間中の最高値で売れてたら</div><div class="v accent" id="best">—</div></div></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
  const num = (n) => Math.round(n).toLocaleString('ja-JP');
  const WHEN_LABEL = {365:'1年前', 180:'半年前', 90:'3ヶ月前', 30:'1ヶ月前', 7:'先週'};
  let PRICES = null;
  $('amount').addEventListener('change', () => { $('customField').style.display = $('amount').value === 'custom' ? '' : 'none'; });
  async function calc(){
    const yen = $('amount').value === 'custom' ? Math.max(100, +$('customYen').value || 0) : +$('amount').value;
    const days = +$('when').value;
    $('state').textContent = '価格データを取得中…';
    try{
      if(!PRICES){
        const r = await fetch('https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=jpy&days=365&interval=daily');
        const j = await r.json();
        if(!j.prices) throw new Error('rate');
        PRICES = j.prices;
      }
      const nowP = PRICES[PRICES.length - 1][1];
      const idx = Math.max(0, PRICES.length - 1 - days);
      const pastP = PRICES[idx][1];
      const val = yen * nowP / pastP;
      const window_ = PRICES.slice(idx);
      const maxP = Math.max(...window_.map(x => x[1]));
      const bestVal = yen * maxP / pastP;
      const pl = val - yen;
      $('state').textContent = '';
      $('sub').textContent = WHEN_LABEL[days] + 'に' + num(yen) + '円分購入した想定｜当時1BTC=' + num(pastP) + '円 → いま' + num(nowP) + '円';
      $('pl').textContent = (pl >= 0 ? '+' : '') + num(pl) + '円';
      $('pct').textContent = (pl >= 0 ? '+' : '') + ((nowP / pastP - 1) * 100).toFixed(1) + '%';
      $('best').textContent = '約' + num(bestVal) + '円';
      SHARE = WHEN_LABEL[days] + 'にビットコインを' + num(yen) + '円分買ってたら、いま' + num(val) + '円' + (pl >= 0 ? 'になってた🪙' : '…実際は減ってた🫠') + '（' + (pl>=0?'+':'') + ((nowP/pastP-1)*100).toFixed(1) + '%）\\nあなたのタラレバも清算する？👇';
      show(); anim($('big'), 0, val, 1000);
    }catch{ $('state').textContent = '⚠️ 価格データの取得に失敗しました（混雑時は少し待つと通ります）。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  bindShare();
})();"""
))

# ============================================================ 7
SIMS.append(dict(
    slug="tanjobi-jiken", cat="life", catjp="人生・自分ごと", grad="linear-gradient(135deg,#fefce8,#fef9c3)", emoji="🎂",
    title="あなたの誕生日、何が起きた日？", score=60,
    card_desc="誕生日を入れると、その日に歴史が何回動いたかをWikipediaから集計。",
    title_tag="あなたの誕生日、何が起きた日？｜歴史イベントカウンター",
    meta_desc="誕生日（月日）を選ぶと、その日に起きた歴史上のできごと・生まれた有名人・記念日の数をWikipediaのデータからリアルタイム集計する無料ツール。話のネタ・自己紹介に。",
    og_title="あなたの誕生日、何が起きた日？",
    og_desc="その日に歴史が動いた回数をWikipediaから集計。",
    lead="あなたの誕生日は、歴史が何回動いた日でしょうか。Wikipediaの「その日」のページから、できごと・誕生した有名人・記念日をその場で数えます。",
    about_h2="このカウンターについて",
    about="""<p>Wikipediaには366日ぶんの「日付ページ」があり、その日に起きたできごと・生まれた人・記念日が編集者たちの手で積み上げられています。このカウンターはWikipedia APIから選んだ日付のページを取得し、各セクションの項目数をその場で数えて、ランダムに数件を紹介します。同じ誕生日でも、開くたびに違うできごとに出会えます。</p>
    <div class="note">出典: <a href="https://ja.wikipedia.org/" target="_blank" rel="noopener">Wikipedia日本語版</a>（CC BY-SA）。項目数は編集状況により変動します。</div>""",
    faqs=[("データの出典は？", "Wikipedia日本語版の日付ページ（例:「8月20日」）をAPI経由で取得し、ブラウザ内で集計しています（CC BY-SAライセンス）。"),
          ("誕生日は送信される？", "選んだ月日はWikipediaのページ取得だけに使われます。生年や個人情報は一切入力不要・送信されません。")],
    rel=[("sakura-kaisu","🌸","桜をあと何回見られるか"),("mental-age","🧠","精神年齢診断"),("isekai","🗡️","異世界転生チート度診断"),("kotoshi-pct","📅","今年あと何％シミュレーター")],
    body="""  <section class="panel">
    <h2>🎂 あなたの誕生日</h2>
    <div class="field"><label>月</label><select id="month"></select></div>
    <div class="field"><label>日</label><select id="day"></select></div>
    <button class="btn btn-primary" id="calcBtn">この日の歴史を数える</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label" id="topLabel">あなたの誕生日、歴史が動いたのは</div>
      <div class="big"><span id="big">0</span><span class="unit">回</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">この日生まれの有名人</div><div class="v" id="born">—</div></div>
      <div class="stat"><div class="k">記念日・年中行事</div><div class="v" id="kinen">—</div></div>
      <div class="stat"><div class="k">この日亡くなった人</div><div class="v accent" id="died">—</div></div></div>
      <div id="list" style="margin-top:14px;"></div>
      <button class="btn btn-ghost" id="moreBtn" style="margin-top:10px;display:none;">🎲 別のできごとを見る</button>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
  $('month').innerHTML = Array.from({length:12}, (_,i) => '<option value="' + (i+1) + '">' + (i+1) + '月</option>').join('');
  $('day').innerHTML = Array.from({length:31}, (_,i) => '<option value="' + (i+1) + '">' + (i+1) + '日</option>').join('');
  let EVENTS = [], PAGE = '';
  function clean(s){
    return s.replace(/<ref[^>]*\\/>/g, '').replace(/<ref[\\s\\S]*?<\\/ref>/g, '')
      .replace(/\\{\\{仮リンク\\|([^|}]+)[^}]*\\}\\}/g, '$1').replace(/\\{\\{[^{}]*\\}\\}/g, '')
      .replace(/\\[\\[[^\\]|]*\\|([^\\]]+)\\]\\]/g, '$1').replace(/\\[\\[([^\\]]+)\\]\\]/g, '$1')
      .replace(/'''?/g, '').replace(/<[^>]+>/g, '').trim();
  }
  function section(text, name){
    const m = text.match(new RegExp('\\\\n==\\\\s*' + name + '\\\\s*==\\\\n([\\\\s\\\\S]*?)(?=\\\\n==[^=]|$)'));
    if(!m) return [];
    return m[1].split('\\n').filter(l => l.startsWith('* ') || (l.startsWith('*') && !l.startsWith('**'))).map(l => clean(l.replace(/^\\*+\\s*/, ''))).filter(l => l.length > 3);
  }
  function showEvents(){
    const picks = [...EVENTS].sort(() => Math.random() - .5).slice(0, 3);
    $('list').innerHTML = '<div style="font-weight:800;font-size:13px;margin-bottom:8px;">📜 たとえばこんな日</div>' + picks.map(e =>
      '<div style="padding:9px 12px;margin-bottom:6px;background:rgba(127,127,127,.07);border-radius:10px;font-size:12.5px;text-align:left;line-height:1.6;">' + (e.length > 110 ? e.slice(0, 110) + '…' : e) + '</div>').join('');
  }
  async function calc(){
    const mo = +$('month').value, da = +$('day').value;
    PAGE = mo + '月' + da + '日';
    $('state').textContent = 'Wikipediaから「' + PAGE + '」を取得中…';
    try{
      const r = await fetch('https://ja.wikipedia.org/w/api.php?action=parse&page=' + encodeURIComponent(PAGE) + '&prop=wikitext&format=json&origin=*');
      const j = await r.json();
      if(!j.parse){ $('state').textContent = 'その日付のページが見つかりませんでした。'; return; }
      const wt = j.parse.wikitext['*'];
      EVENTS = section(wt, 'できごと');
      const born = section(wt, '誕生日').length;
      const died = section(wt, '忌日').length;
      const kinen = section(wt, '記念日・年中行事').length;
      $('state').textContent = '';
      $('sub').textContent = PAGE + '｜Wikipedia日本語版の記録より（開くたびに違うできごとを紹介）';
      $('born').textContent = born + '人';
      $('died').textContent = died + '人';
      $('kinen').textContent = kinen + '件';
      showEvents();
      $('moreBtn').style.display = '';
      SHARE = '私の誕生日' + PAGE + 'は、歴史が' + EVENTS.length + '回動いた日だった🎂（有名人' + born + '人誕生・記念日' + kinen + '件）\\nあなたの誕生日は？👇';
      show(); anim($('big'), 0, EVENTS.length, 900);
    }catch{ $('state').textContent = '⚠️ 取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  $('moreBtn').addEventListener('click', showEvents);
  bindShare();
})();"""
))

# ============================================================ 8
SIMS.append(dict(
    slug="aurora-yohou", cat="wonder", catjp="ふしぎ・現象", grad="linear-gradient(135deg,#eef2ff,#e0e7ff)", emoji="🌌",
    title="オーロラ予報メーター", score=59,
    card_desc="いま地球の磁気はどれだけ荒れてる？NASA系の宇宙天気データで日本オーロラの可能性を判定。",
    title_tag="オーロラ予報メーター｜いまのKp指数と日本で見える可能性",
    meta_desc="米海洋大気庁（NOAA）の宇宙天気データからいまの地磁気活動（Kp指数）をリアルタイム取得し、北海道で低緯度オーロラが見える可能性を判定する無料メーター。",
    og_title="オーロラ予報メーター｜いま地磁気はどれだけ荒れてる？",
    og_desc="NOAAの宇宙天気データでKp指数をライブ表示。",
    lead="オーロラは太陽の爆発が地球の磁気を揺らした夜に現れます。米NOAAの宇宙天気データから、いまの地磁気の荒れ具合（Kp指数）をライブ表示します。",
    about_h2="このメーターについて",
    about="""<p>Kp指数は地磁気の乱れを0〜9で表す国際指標で、数字が大きいほどオーロラが低緯度まで降りてきます。ふだんの日本では無縁ですが、Kp8〜9級の巨大磁気嵐が起きると、北海道でも地平線が赤く染まる「低緯度オーロラ」が観測されることがあります。実際に2024年5月の巨大磁気嵐では、北海道各地で赤いオーロラが撮影されました。このメーターは米海洋大気庁（NOAA）の公開データをそのまま表示しています。</p>
    <div class="note">Kpが高い夜に狙うなら、北の空が開けた暗い場所で「地平線近くの赤い光」を探すのがコツです。肉眼より先にスマホの夜景モードに写ることが多いです。</div>""",
    faqs=[("データの出典は？", "米海洋大気庁（NOAA）宇宙天気予報センターの公開データ（惑星間Kp指数）をそのまま取得・表示しています。"),
          ("日本でオーロラが見えるのはどんな時？", "目安としてKp8以上の巨大磁気嵐の夜、北海道など北日本の暗い場所で、北の地平線が赤く見えることがあります（低緯度オーロラ）。"),
          ("入力データは送信される？", "このページは何も入力せずに使えます。")],
    rel=[("hoshizora-shisu","🔭","今夜の星空指数"),("iss-doko","🛰️","ISSはいまどこ？"),("jishin-live","🗾","日本はいまも揺れている"),("galaxy-collision","🌌","銀河衝突シミュレーター")],
    body="""  <section class="panel" id="resultPanel">
    <div class="result">
      <div class="label">いまの地磁気活動（Kp指数）は</div>
      <div class="big"><span id="big">–</span><span class="unit">/ 9</span></div>
      <div class="sub" id="sub">データを読み込み中…</div>
      <div class="statline"><div class="stat"><div class="k">直近24時間の最大</div><div class="v" id="max24">—</div></div>
      <div class="stat"><div class="k">状態</div><div class="v" id="status">—</div></div>
      <div class="stat"><div class="k">北海道オーロラの目安</div><div class="v accent" id="line">Kp 8以上</div></div></div>
      <button class="btn btn-ghost" id="reloadBtn" style="margin-top:10px;">🔄 最新に更新</button>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
  async function load(){
    $('sub').textContent = 'データを読み込み中…';
    try{
      const r = await fetch('https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json');
      const j = await r.json();
      const rows = Array.isArray(j[0]) ? j.slice(1).map(x => ({t: x[0], kp: +x[1]})) : j.map(x => ({t: x.time_tag, kp: +x.Kp}));
      const last = rows[rows.length - 1];
      const max24 = Math.max(...rows.slice(-8).map(x => x.kp));
      const kp = last.kp;
      const judge = kp >= 8 ? '🔴 巨大磁気嵐！北海道で低緯度オーロラのチャンス' : kp >= 6 ? '🟠 磁気嵐発生中（北欧・カナダは大チャンス）' : kp >= 4 ? '🟡 やや活発（極地のオーロラが元気）' : '🟢 静穏（オーロラは極地の定位置のみ）';
      $('sub').textContent = '観測時刻 ' + last.t.replace('T',' ').slice(0,16) + ' UTC｜' + judge;
      $('max24').textContent = max24.toFixed(1);
      $('status').textContent = kp >= 6 ? '磁気嵐' : kp >= 4 ? '活発' : '静穏';
      SHARE = 'いまの地磁気活動はKp' + kp.toFixed(1) + '/9🌌 ' + judge.replace(/^[🔴🟠🟡🟢] /,'') + '\\n宇宙天気のライブはこちら👇';
      anim($('big'), 0, Math.round(kp * 10) / 10, 800, 1);
    }catch{ $('sub').textContent = '⚠️ 宇宙天気データの取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  load();
  $('reloadBtn').addEventListener('click', load);
  bindShare();
})();"""
))

# ============================================================ 9
SIMS.append(dict(
    slug="naminori-biyori", cat="sports", catjp="スポーツ・運動", grad="linear-gradient(135deg,#ecfdf5,#d1fae5)", emoji="🏄",
    title="波乗り日和チェッカー", score=58,
    card_desc="明日の朝イチ、波ある？主要サーフポイントの波高・周期を予報データから判定。",
    title_tag="波乗り日和チェッカー｜明日朝の波高・周期をポイント別に判定",
    meta_desc="湘南・千葉・大洗など主要サーフポイントの明日朝の波高・周期を海洋予報データから取得し、サイズ感（ヒザ〜アタマ）を判定する無料チェッカー。",
    og_title="波乗り日和チェッカー｜明日の朝イチ、波ある？",
    og_desc="主要ポイントの波高・周期を予報データから判定。",
    lead="明日の朝イチ、入る価値ある？主要サーフポイントの波高と周期を海洋予報データから取得して、サイズ感を判定します。",
    about_h2="このチェッカーについて",
    about="""<p>波のコンディションは「波高（大きさ）」と「周期（うねりの質）」でだいたい決まります。周期が8秒を超えるうねりは整った波になりやすく、逆に短い周期は風波でまとまりがちです。このチェッカーは海洋予報オープンデータAPI（Open-Meteo Marine）から選んだポイント沖の予報を取得し、日本のサーファーが使う「ヒザ・コシ・ムネ・アタマ」のサイズ感に翻訳します。</p>
    <div class="note">沖合モデルの予報値のため、地形・風向き・潮位による実際のブレイクとの差があります。最終判断はポイントのライブカメラや現地情報で。</div>""",
    faqs=[("波データの出典は？", "海洋予報オープンデータAPI（Open-Meteo Marine）から、選んだポイント沖の波高・周期の予報を取得しています。"),
          ("サイズ表記の目安は？", "波高おおよそ0.3m未満=フラット、〜0.6m=ヒザ〜モモ、〜0.9m=コシ〜ハラ、〜1.2m=ムネ、〜1.6m=カタ〜アタマ、それ以上=アタマオーバーとしています。"),
          ("入力データは送信される？", "ポイントの選択のみをAPIへの問い合わせに使います。個人情報は一切送信されません。")],
    rel=[("hiyake-timer","☀️","日焼けタイマー"),("onsen-seiha","♨️","全国制覇まで何年？"),("gasolin-doko","🛻","満タンでどこまで"),("ryohi","✈️","旅行費用 総額")],
    body="""  <section class="panel">
    <h2>🏄 ポイント</h2>
    <div class="field"><label>サーフポイント</label>
      <select id="spot">
        <option value="35.31,139.47" selected>湘南・鵠沼（神奈川）</option>
        <option value="35.35,140.40">一宮・志田下（千葉）</option>
        <option value="35.09,140.14">鴨川マルキ（千葉）</option>
        <option value="36.31,140.58">大洗（茨城）</option>
        <option value="34.60,138.22">御前崎（静岡）</option>
        <option value="33.53,135.90">磯ノ浦（和歌山）</option>
        <option value="33.65,130.20">糸島（福岡）</option>
        <option value="31.86,131.45">木崎浜（宮崎）</option>
      </select>
    </div>
    <button class="btn btn-primary" id="calcBtn">明日の朝イチをチェック</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label">明日の朝6時、予想波高は</div>
      <div class="big"><span id="big">0</span><span class="unit">m</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">サイズ感</div><div class="v" id="size">—</div></div>
      <div class="stat"><div class="k">周期</div><div class="v" id="period">—</div></div>
      <div class="stat"><div class="k">今朝はどうだった？</div><div class="v accent" id="today">—</div></div></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
  const sizeLabel = (h) => h < 0.3 ? 'フラット…' : h < 0.6 ? 'ヒザ〜モモ' : h < 0.9 ? 'コシ〜ハラ' : h < 1.2 ? 'ムネ' : h < 1.6 ? 'カタ〜アタマ' : 'アタマオーバー⚠️';
  async function calc(){
    const [lat, lon] = $('spot').value.split(',');
    const name = $('spot').selectedOptions[0].textContent;
    $('state').textContent = '海洋予報を取得中…';
    try{
      const r = await fetch('https://marine-api.open-meteo.com/v1/marine?latitude=' + lat + '&longitude=' + lon + '&hourly=wave_height,wave_period&forecast_days=2&timezone=Asia%2FTokyo');
      const j = await r.json();
      const H = j.hourly.wave_height, P = j.hourly.wave_period;
      const h6 = H[30], p6 = P[30];       // 明日6時
      const t6 = H[6];                     // 今朝6時
      const quality = p6 >= 10 ? '長周期のうねり（質良し）' : p6 >= 8 ? '整ったうねり' : p6 >= 6 ? 'ふつう' : '風波っぽい（まとまり欠く）';
      $('state').textContent = '';
      $('sub').textContent = name + ' 沖の予報｜' + quality;
      $('size').textContent = sizeLabel(h6);
      $('period').textContent = p6.toFixed(1) + '秒';
      $('today').textContent = t6 != null ? t6.toFixed(1) + 'm（' + sizeLabel(t6) + '）' : '—';
      SHARE = '明日朝の' + name.split('（')[0] + '、予想波高' + h6.toFixed(1) + 'm・' + sizeLabel(h6) + '🏄（周期' + p6.toFixed(1) + '秒）\\nあなたのホームは？👇';
      show(); anim($('big'), 0, Math.round(h6 * 10) / 10, 900, 1);
    }catch{ $('state').textContent = '⚠️ 予報の取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  bindShare();
})();"""
))

# ============================================================ 10
SIMS.append(dict(
    slug="yuyake-yohou", cat="wonder", catjp="ふしぎ・現象", grad="linear-gradient(135deg,#eef2ff,#e0e7ff)", emoji="🌇",
    title="今日の夕焼け予報", score=57,
    card_desc="今日の空、焼ける？日没時刻の雲量から「夕焼けの当たり日」を予報。",
    title_tag="今日の夕焼け予報｜日没の雲量から「焼ける空」を予測",
    meta_desc="今日の日没時刻とそのときの雲量予報から、夕焼けがきれいに焼けるかを0〜100点で予報する無料ツール。ベストな観賞タイミングも表示。写真好き・散歩好きに。",
    og_title="今日の夕焼け予報｜今日の空、焼ける？",
    og_desc="日没時刻の雲量から夕焼けの当たり日を予測。",
    lead="夕焼けの「当たり日」は、実は雲がゼロの日ではありません。今日の日没時刻とそのときの雲量から、空が焼ける可能性を予報します。",
    about_h2="この予報について",
    about="""<p>意外なことに、快晴の夕焼けは平凡です。空が燃えるように焼けるのは、上空に適度な雲（目安2〜6割）があって、沈んだ太陽の光を下から照らすとき。逆に雲が厚すぎると光が届かず、ただ暗くなります。この予報は気象オープンデータAPI（Open-Meteo）から今日の日没時刻とその時間帯の雲量を取得し、「焼け度」を0〜100点で表します。</p>
    <div class="note">いちばん焼けるのは日没の5〜20分後、いわゆるマジックアワーです。太陽が沈んだからと帰るのは、いちばんおいしいところを捨てています。</div>""",
    faqs=[("データの出典は？", "気象オープンデータAPI（Open-Meteo）から、選んだ地点の今日の日没時刻と雲量予報を取得しています。"),
          ("なぜ雲があるほうが焼けるの？", "沈んだ直後の太陽光は地平線の下から雲の底を赤く照らします。雲がないと光を受け止めるスクリーンがなく、グラデーションだけで終わります。"),
          ("入力データは送信される？", "地域の選択のみを気象APIへの問い合わせに使います。個人情報は一切送信されません。")],
    rel=[("hoshizora-shisu","🔭","今夜の星空指数"),("iss-doko","🛰️","ISSはいまどこ？"),("sakura-kaisu","🌸","桜をあと何回見られるか"),("machi-jikan","⏳","人生の「待ち時間」")],
    body="""  <section class="panel">
    <h2>🌇 条件</h2>
    <div class="field"><label>地域</label><select id="pref"></select></div>
    <button class="btn btn-primary" id="calcBtn">今日の焼け度を予報する</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label">今日の夕焼け、焼け度は</div>
      <div class="big"><span id="big">0</span><span class="unit">点</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">今日の日の入り</div><div class="v" id="sunset">—</div></div>
      <div class="stat"><div class="k">日没時の雲量</div><div class="v" id="cloud">—</div></div>
      <div class="stat"><div class="k">ベスト観賞タイム</div><div class="v accent" id="best">—</div></div></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
@@PREFS_JS@@
  async function calc(){
    const p = PREFS[+$('pref').value];
    $('state').textContent = '日没と雲の予報を取得中…';
    try{
      const r = await fetch('https://api.open-meteo.com/v1/forecast?latitude=' + p[1] + '&longitude=' + p[2] + '&daily=sunset&hourly=cloud_cover&forecast_days=1&timezone=Asia%2FTokyo');
      const j = await r.json();
      const sunset = j.daily.sunset[0];                  // "2026-08-20T18:23"
      const hh = +sunset.slice(11,13), mm = +sunset.slice(14,16);
      const cloud = j.hourly.cloud_cover[Math.min(23, hh + (mm >= 30 ? 1 : 0))] ?? j.hourly.cloud_cover[hh];
      let score, label;
      if(cloud <= 5){ score = 55; label = '快晴。焼けるけど、ちょっと平凡かも'; }
      else if(cloud <= 15){ score = 70; label = 'きれいなグラデーション日和'; }
      else if(cloud <= 40){ score = 88; label = '🔥燃える空の予感！カメラの準備を'; }
      else if(cloud <= 65){ score = 74; label = '雲の切れ間しだいで大当たりも'; }
      else if(cloud <= 85){ score = 40; label = '雲多め。ドラマチック狙いならワンチャン'; }
      else { score = 15; label = '今日は厚い雲の向こう…'; }
      const bestFrom = mm + 5, bestTo = mm + 20;
      const fmtT = (h, m) => (h + Math.floor(m / 60)) + ':' + String(m % 60).padStart(2, '0');
      $('state').textContent = '';
      $('sub').textContent = p[0] + '｜' + label;
      $('sunset').textContent = hh + ':' + String(mm).padStart(2,'0');
      $('cloud').textContent = Math.round(cloud) + '%';
      $('best').textContent = fmtT(hh, bestFrom) + '〜' + fmtT(hh, bestTo) + '（日没後のマジックアワー）';
      SHARE = '今日の' + p[0] + 'の夕焼け予報、焼け度' + score + '点🌇 ' + label + '（日の入り' + hh + ':' + String(mm).padStart(2,'0') + '）\\nあなたの街の空は？👇';
      show(); anim($('big'), 0, score, 900);
    }catch{ $('state').textContent = '⚠️ 予報の取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  bindShare();
})();"""
))

# ============================================================ 生成
IDX = os.path.join(ROOT, "index.html")
with io.open(IDX, encoding="utf-8") as f:
    html = f.read()
assert "sims/hoshizora-shisu/" not in html, "既に挿入済み（中止）"

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
        {"@type": "ListItem", "position": 2, "name": s["title"], "item": "https://shimulabo.com/sims/%s/" % s["slug"]}]}, ensure_ascii=False)
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

# OGP画像
gen_path = os.path.join(SCRIPTS, "gen_images.py")
gen_src = io.open(gen_path, encoding="utf-8").read()
defs_only = gen_src.split("\nSIMS = [")[0]
ns = {"__file__": gen_path}
exec(compile(defs_only, gen_path, "exec"), ns)
for s in SIMS:
    ns["make_ogp"](os.path.join(ROOT, "ogp", s["slug"] + ".png"), s["title"], s["catjp"])

# index.html: カード＋ランキング＋本数
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
print("patched index.html: count=%d" % (cnt + len(SIMS)))

# sitemap.xml
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
