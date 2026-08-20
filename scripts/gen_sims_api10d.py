# -*- coding: utf-8 -*-
"""API連携シリーズ第4弾 10本（1回限り）。sims生成→OGP→index→/live/→sitemap。"""
import os, io, re, json

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPTS)
TODAY = "2026-08-20"

_g10c = io.open(os.path.join(SCRIPTS, "gen_sims_api10c.py"), encoding="utf-8").read()
def _block(name):
    m = re.search(name + r' = """(.*?)"""', _g10c, re.S)
    return m.group(1)
SKELETON = _block("SKELETON")
SHARE_ROW = _block("SHARE_ROW")
JS_COMMON = _block("JS_COMMON")
PREF_ROWS_SRC = re.search(r'PREF_ROWS = \[(.*?)\]\n', _g10c, re.S).group(1)
PREF_ROWS = eval("[" + PREF_ROWS_SRC + "]")
PREFS_JS = "  const PREFS = [\n" + "\n".join("    ['%s',%s,%s]," % r for r in PREF_ROWS) + "\n  ];\n  $('pref').innerHTML = PREFS.map((p,i) => '<option value=\"' + i + '\"' + (i===12?' selected':'') + '>' + p[0] + '</option>').join('');"

def faq_dl(faqs):
    return "".join("<dt>%s</dt><dd>%s</dd>" % (q, a) for q, a in faqs)

def faq_ld(faqs):
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in faqs
    ]}, ensure_ascii=False)

def related(items):
    return "".join('<a class="related-card" href="../%s/"><span class="e">%s</span><span>%s</span></a>' % (s, e, t) for s, e, t in items)

WMO_JS = """  const WMO = {0:'快晴',1:'晴れ',2:'晴れ時々くもり',3:'くもり',45:'霧',48:'霧氷',51:'霧雨',53:'霧雨',55:'強い霧雨',61:'弱い雨',63:'雨',65:'強い雨',66:'着氷性の雨',67:'着氷性の雨',71:'弱い雪',73:'雪',75:'大雪',77:'霧雪',80:'にわか雨',81:'にわか雨',82:'激しいにわか雨',85:'にわか雪',86:'にわか雪',95:'雷雨',96:'雷雨(ひょう)',99:'激しい雷雨'};
  const wmoEmoji = (c) => c<=1?'☀️':c<=2?'🌤️':c<=3?'☁️':c<=48?'🌫️':c<=57?'🌦️':c<=67?'🌧️':c<=77?'🌨️':c<=82?'🌦️':c<=86?'🌨️':'⛈️';"""

SIMS = []

# ============================================================ 1 生まれた日の天気
SIMS.append(dict(
    slug="umareta-hi-tenki", cat="life", catjp="人生・自分ごと", grad="linear-gradient(135deg,#fefce8,#fef9c3)", emoji="👶",
    title="生まれた日の天気", score=66,
    card_desc="あなたが生まれた日、空はどうだった？1940年からの気象アーカイブで答え合わせ。",
    title_tag="生まれた日の天気｜誕生日の気温・天気を気象アーカイブで再現",
    meta_desc="生年月日と場所を入れると、あなたが生まれた日の天気・最高気温・降水を1940年からの気象アーカイブデータで表示する無料ツール。記念日・家族の思い出調べにも。",
    og_title="生まれた日の天気｜あなたが生まれた日、空はどうだった？",
    og_desc="1940年からの気象アーカイブで誕生日の空を再現。",
    lead="あなたが生まれた日、外は晴れていたでしょうか。1940年まで遡れる気象アーカイブから、その日の天気と気温を呼び出します。",
    about_h2="このツールについて",
    about="""<p>このツールは気象オープンデータの過去アーカイブAPI（Open-Meteo Historical Weather・ERA5再解析データ）から、指定した日付・地点の天気を取得しています。1940年以降の全世界の気象が再現されており、ご自身はもちろん、親や祖父母が生まれた日・結婚した日など、家族の記念日の「あの日の空」も調べられます。</p>
    <div class="note">再解析データは観測とモデルを組み合わせた推計値のため、当時の新聞の天気欄と細部が異なることがあります。</div>""",
    faqs=[("データの出典は？", "気象オープンデータの過去アーカイブAPI（Open-Meteo Historical Weather、ERA5再解析）から取得しています。1940年以降に対応しています。"),
          ("生年月日は保存される？", "いいえ。入力した日付は気象APIへの問い合わせにだけ使われ、当サイトが保存することはありません。"),
          ("海外生まれでも使える？", "現在は日本の都道府県のみ対応です。リクエストが多ければ海外都市も追加します。")],
    rel=[("tanjobi-jiken","🎂","あなたの誕生日、何が起きた日？"),("sakura-kaisu","🌸","桜をあと何回見られるか"),("hoshizora-shisu","🔭","今夜の星空指数"),("kotoshi-pct","📅","今年あと何％シミュレーター")],
    body="""  <section class="panel">
    <h2>👶 生まれた日</h2>
    <div class="field"><label>年 <span class="hint">（1940〜）</span></label><input type="number" id="year" value="1990" min="1940" max="2026" inputmode="numeric"></div>
    <div class="field"><label>月</label><select id="month"></select></div>
    <div class="field"><label>日</label><select id="day"></select></div>
    <div class="field"><label>生まれた場所</label><select id="pref"></select></div>
    <button class="btn btn-primary" id="calcBtn">その日の空を見る</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label" id="topLabel">その日の天気は</div>
      <div class="big" style="font-size:min(13vw,58px);"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">最高気温</div><div class="v" id="hi">—</div></div>
      <div class="stat"><div class="k">最低気温</div><div class="v" id="lo">—</div></div>
      <div class="stat"><div class="k">降水量</div><div class="v accent" id="rain">—</div></div></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
@@PREFS_JS@@
@@WMO_JS@@
  $('month').innerHTML = Array.from({length:12}, (_,i) => '<option value="' + (i+1) + '">' + (i+1) + '月</option>').join('');
  $('day').innerHTML = Array.from({length:31}, (_,i) => '<option value="' + (i+1) + '">' + (i+1) + '日</option>').join('');
  async function calc(){
    const y = Math.max(1940, Math.min(2026, +$('year').value || 1990));
    const mo = +$('month').value, da = +$('day').value;
    const p = PREFS[+$('pref').value];
    const date = y + '-' + String(mo).padStart(2,'0') + '-' + String(da).padStart(2,'0');
    if(new Date(date) > new Date(Date.now() - 6 * 86400000)){ $('state').textContent = '直近すぎる日付はアーカイブ未反映です。少し前の日付でお試しください。'; return; }
    $('state').textContent = '気象アーカイブを検索中…';
    try{
      const r = await fetch('https://archive-api.open-meteo.com/v1/archive?latitude=' + p[1] + '&longitude=' + p[2] + '&start_date=' + date + '&end_date=' + date + '&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,snowfall_sum,weather_code&timezone=Asia%2FTokyo');
      const j = await r.json();
      const d = j.daily;
      if(!d || d.temperature_2m_max[0] == null){ $('state').textContent = 'その日付のデータが見つかりませんでした。'; return; }
      const code = d.weather_code[0] ?? 0;
      const wx = WMO[code] || 'くもり';
      const snow = d.snowfall_sum[0] || 0;
      $('state').textContent = '';
      $('big').textContent = wmoEmoji(code) + ' ' + wx;
      $('sub').textContent = y + '年' + mo + '月' + da + '日・' + p[0] + '（ERA5気象アーカイブ）';
      $('hi').textContent = d.temperature_2m_max[0].toFixed(1) + '℃';
      $('lo').textContent = d.temperature_2m_min[0].toFixed(1) + '℃';
      $('rain').textContent = snow > 1 ? '雪 ' + snow.toFixed(0) + 'cm' : (d.precipitation_sum[0] || 0).toFixed(1) + 'mm';
      SHARE = '私が生まれた' + y + '年' + mo + '月' + da + '日の' + p[0].split('(')[0] + 'は「' + wx + '」・最高' + d.temperature_2m_max[0].toFixed(1) + '℃だった' + wmoEmoji(code) + '\\nあなたが生まれた日の空は？👇';
      show();
    }catch{ $('state').textContent = '⚠️ アーカイブの取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  bindShare();
})();"""
))

# ============================================================ 2 2050年の夏
SIMS.append(dict(
    slug="natsu-2050", cat="wonder", catjp="ふしぎ・現象", grad="linear-gradient(135deg,#eef2ff,#e0e7ff)", emoji="🔥",
    title="2050年の夏、何度になる？", score=65,
    card_desc="いまの猛暑はまだ序の口かも。気候モデルCMIP6であなたの街の2050年の夏を見る。",
    title_tag="2050年の夏、何度になる？｜気候モデルであなたの街の未来の夏を予測",
    meta_desc="国際的な気候予測モデル（CMIP6）のデータから、あなたの街の2050年夏の平均最高気温と猛暑日数を表示する無料ツール。いまの夏との差を数字で体感。",
    og_title="2050年の夏、何度になる？",
    og_desc="気候モデルCMIP6で2050年のあなたの街の夏を予測。",
    lead="「今年の夏は異常」と毎年言っていますが、気候モデルが描く2050年はさらにその先です。あなたの街の未来の夏を、国際的な気候予測データで見てみます。",
    about_h2="この予測について",
    about="""<p>この予測は、IPCC評価報告書にも使われる国際気候モデル群CMIP6の1モデル（EC-Earth3P-HR）のダウンスケーリングデータを、気候オープンデータAPI（Open-Meteo Climate）から取得しています。2050年7〜8月の日別最高気温から平均と猛暑日（35℃以上）日数を計算し、直近の実測（2024年の同期間・ERA5）と並べます。</p>
    <div class="note">気候モデルは「その年の天気の予言」ではなく、温室効果ガスシナリオに基づく長期傾向の推計です。モデルや シナリオによって数値は変わります。研究・報道用途では原典（CMIP6/IPCC）をご参照ください。</div>""",
    faqs=[("データの出典は？", "気候オープンデータAPI（Open-Meteo Climate API）経由のCMIP6気候モデル（EC-Earth3P-HR）と、比較用にERA5再解析（2024年実測相当）を使用しています。"),
          ("2050年の天気が本当に分かるの？", "特定の日の天気は分かりません。表示するのは気候モデルが示す「2050年ごろの夏の平均的な姿」で、長期傾向の目安です。"),
          ("入力データは送信される？", "地域の選択のみを使います。個人情報は一切送信されません。")],
    rel=[("atsusa-ranking","🌡️","全国いま暑いランキング"),("nettaiya-check","🌙","今夜、熱帯夜？チェック"),("infure","📉","物価2倍まで何年？"),("chikyu-yure","🌐","地球まるごと地震カウンター")],
    body="""  <section class="panel">
    <h2>🔥 条件</h2>
    <div class="field"><label>地域</label><select id="pref"></select></div>
    <button class="btn btn-primary" id="calcBtn">2050年の夏を見る</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label">2050年の夏（7〜8月）、日中の平均は</div>
      <div class="big"><span id="big">0</span><span class="unit">℃</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">いまの夏（2024年実測）</div><div class="v" id="now">—</div></div>
      <div class="stat"><div class="k">上昇幅</div><div class="v" id="diff">—</div></div>
      <div class="stat"><div class="k">猛暑日（35℃以上）予測</div><div class="v accent" id="mosho">—</div></div></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
@@PREFS_JS@@
  const stats = (arr) => {
    const v = arr.filter(x => x != null);
    return { avg: v.reduce((a,b)=>a+b,0) / v.length, mosho: v.filter(x => x >= 35).length };
  };
  async function calc(){
    const p = PREFS[+$('pref').value];
    $('state').textContent = '気候モデルの計算結果を取得中…（数秒かかります）';
    try{
      const [fut, cur] = await Promise.all([
        fetch('https://climate-api.open-meteo.com/v1/climate?latitude=' + p[1] + '&longitude=' + p[2] + '&start_date=2050-07-01&end_date=2050-08-31&models=EC_Earth3P_HR&daily=temperature_2m_max').then(r => r.json()),
        fetch('https://archive-api.open-meteo.com/v1/archive?latitude=' + p[1] + '&longitude=' + p[2] + '&start_date=2024-07-01&end_date=2024-08-31&daily=temperature_2m_max&timezone=Asia%2FTokyo').then(r => r.json()),
      ]);
      const f = stats(fut.daily.temperature_2m_max);
      const c = stats(cur.daily.temperature_2m_max);
      const diff = f.avg - c.avg;
      $('state').textContent = '';
      $('sub').textContent = p[0] + '｜気候モデルCMIP6（EC-Earth3P-HR）の2050年7〜8月推計';
      $('now').textContent = c.avg.toFixed(1) + '℃（猛暑日' + c.mosho + '日）';
      $('diff').textContent = (diff >= 0 ? '+' : '') + diff.toFixed(1) + '℃';
      $('mosho').textContent = f.mosho + '日 / 62日';
      SHARE = '気候モデルによると、2050年の' + p[0].split('(')[0] + 'の夏は日中平均' + f.avg.toFixed(1) + '℃・猛暑日' + f.mosho + '日🔥（2024年比' + (diff>=0?'+':'') + diff.toFixed(1) + '℃）\\nあなたの街の2050年は？👇';
      show(); anim($('big'), 0, Math.round(f.avg * 10) / 10, 1000, 1);
    }catch{ $('state').textContent = '⚠️ 取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  bindShare();
})();"""
))

# ============================================================ 3 富士山見える？
SIMS.append(dict(
    slug="fujisan-mieru", cat="travel", catjp="旅行・おでかけ", grad="linear-gradient(135deg,#cffafe,#a5f3fc)", emoji="🗻",
    title="今日、富士山見える？", score=64,
    card_desc="視程と富士山周辺の雲から「今日見えるか」を主要スポット別に判定。",
    title_tag="今日、富士山見える？チェッカー｜視程×雲量でスポット別に判定",
    meta_desc="河口湖・江の島・東京都心など主要スポットから今日富士山が見えるかを、大気の視程と富士山周辺の雲量からリアルタイム判定する無料ツール。",
    og_title="今日、富士山見える？チェッカー",
    og_desc="視程×雲量で富士山が見えるかをスポット別に判定。",
    lead="富士山が見えるかどうかは「空気の澄み具合」と「山頂の雲」で決まります。いまの視程と雲量から、スポット別の「見える度」を判定します。",
    about_h2="この判定について",
    about="""<p>遠くの山が見えるかは、大気中の水蒸気やチリで決まる「視程」（どこまで見通せるか）に大きく左右されます。このチェッカーは気象オープンデータAPI（Open-Meteo）から、選んだスポットの現在の視程と、富士山周辺の雲量を取得し、スポットから富士山までの距離と突き合わせて「見える度」を計算します。冬の朝がいちばんよく見えるのは、空気が乾いて視程が伸びるからです。</p>
    <div class="note">局地的な靄（もや）やビルの遮蔽までは反映できません。「見える度が高い日に外に出たら本物を確認」くらいの気持ちでどうぞ。</div>""",
    faqs=[("データの出典は？", "気象オープンデータAPI（Open-Meteo）の視程（visibility）と雲量の予報値を利用しています。"),
          ("見える度100でも見えないことは？", "あります。ビル・地形の遮蔽や局地的な靄は考慮できないため、あくまで大気条件の目安です。逆に低くても山頂だけ覗くこともあります。"),
          ("入力データは送信される？", "スポットの選択のみを使います。個人情報は一切送信されません。")],
    rel=[("hoshizora-shisu","🔭","今夜の星空指数"),("yuyake-yohou","🌇","今日の夕焼け予報"),("kaibatsu-check","⛰️","うちの海抜チェッカー"),("shuumatsu-hare","🌤️","今週末、晴れる？")],
    body="""  <section class="panel">
    <h2>🗻 どこから見る？</h2>
    <div class="field"><label>スポット</label>
      <select id="spot">
        <option value="35.50,138.76,16">河口湖（山梨・約16km）</option>
        <option value="35.42,138.87,14">山中湖（山梨・約14km）</option>
        <option value="35.31,138.93,19">御殿場（静岡・約19km）</option>
        <option value="35.12,138.92,32">三島・沼津（静岡・約32km）</option>
        <option value="34.99,138.52,45">三保松原（静岡・約45km）</option>
        <option value="35.30,139.48,69">江の島（神奈川・約69km）</option>
        <option value="35.45,139.64,83">横浜（約83km）</option>
        <option value="35.69,139.69,95" selected>東京都心（約95km）</option>
      </select>
    </div>
    <button class="btn btn-primary" id="calcBtn">いまの「見える度」を判定</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label">いまの富士山「見える度」は</div>
      <div class="big"><span id="big">0</span><span class="unit">%</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">いまの視程</div><div class="v" id="vis">—</div></div>
      <div class="stat"><div class="k">富士山周辺の雲</div><div class="v" id="cloud">—</div></div>
      <div class="stat"><div class="k">今日のベスト時間帯</div><div class="v accent" id="best">—</div></div></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
  const FUJI = [35.36, 138.73];
  async function calc(){
    const [lat, lon, dist] = $('spot').value.split(',').map(Number);
    const name = $('spot').selectedOptions[0].textContent.split('（')[0];
    $('state').textContent = '視程と雲量を取得中…';
    try{
      const [vp, fj] = await Promise.all([
        fetch('https://api.open-meteo.com/v1/forecast?latitude=' + lat + '&longitude=' + lon + '&hourly=visibility&forecast_days=1&timezone=Asia%2FTokyo').then(r => r.json()),
        fetch('https://api.open-meteo.com/v1/forecast?latitude=' + FUJI[0] + '&longitude=' + FUJI[1] + '&hourly=cloud_cover&forecast_days=1&timezone=Asia%2FTokyo').then(r => r.json()),
      ]);
      const h = new Date().getHours();
      const visArr = vp.hourly.visibility, cloudArr = fj.hourly.cloud_cover;
      const vis = visArr[h] ?? 0;
      const cloud = cloudArr[h] ?? 100;
      const scoreAt = (hh) => Math.round(Math.min(1, (visArr[hh] ?? 0) / (dist * 1000)) * (100 - (cloudArr[hh] ?? 100)));
      const score = scoreAt(h);
      let bestH = 6, bestS = -1;
      for(let x = 6; x <= 18; x++){ const s = scoreAt(x); if(s > bestS){ bestS = s; bestH = x; } }
      const label = score >= 70 ? 'くっきり見えるはず🗻' : score >= 40 ? 'うっすら見えるかも' : score >= 15 ? 'かなり厳しい' : '今はほぼ無理…';
      $('state').textContent = '';
      $('sub').textContent = name + 'から（距離約' + dist + 'km）｜' + label;
      $('vis').textContent = (vis / 1000).toFixed(0) + 'km';
      $('cloud').textContent = Math.round(cloud) + '%';
      $('best').textContent = bestH + '時ごろ（見える度' + bestS + '%）';
      SHARE = 'いま' + name + 'から富士山が見える度は' + score + '%🗻（' + label + '）視程' + (vis/1000).toFixed(0) + 'km・山頂の雲' + Math.round(cloud) + '%\\nあなたの場所からは？👇';
      show(); anim($('big'), 0, score, 900);
    }catch{ $('state').textContent = '⚠️ 取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  bindShare();
})();"""
))

# ============================================================ 4 風ヤバい？
SIMS.append(dict(
    slug="kyou-kaze", cat="tool", catjp="便利ツール", grad="linear-gradient(135deg,#eff6ff,#e0f2fe)", emoji="💨",
    title="今日、風ヤバい？チェッカー", score=63,
    card_desc="ビニール傘は生き残れるか。今日の最大瞬間風速から自転車・傘・洗濯物リスクを判定。",
    title_tag="今日、風ヤバい？チェッカー｜最大瞬間風速から傘・自転車リスクを判定",
    meta_desc="今日の風速・最大瞬間風速の予報をリアルタイム取得して、傘が壊れる・自転車がつらい・洗濯物が飛ぶリスクを時間帯つきで判定する無料ツール。",
    og_title="今日、風ヤバい？チェッカー",
    og_desc="最大瞬間風速から傘・自転車・洗濯物のリスクを判定。",
    lead="天気予報の「風やや強く」では何も分かりません。今日の最大瞬間風速を取得して、ビニール傘・自転車・洗濯物への実害レベルで判定します。",
    about_h2="この判定について",
    about="""<p>風の実害は平均風速より「突風（最大瞬間風速）」で決まります。ビニール傘はおよそ10m/sの突風で反り返り始め、15m/sで寿命を迎えます。このチェッカーは気象オープンデータAPI（Open-Meteo）から今日の風速と突風の予報を1時間単位で取得し、生活ダメージに翻訳します。</p>
    <div class="note">目安：突風5m/s=そよ風、10m/s=傘が反る・自転車ふらつく、15m/s=ビニール傘全滅、20m/s=看板注意・外出考慮、25m/s以上=不要不急の外出は控える領域です。</div>""",
    faqs=[("データの出典は？", "気象オープンデータAPI（Open-Meteo）から、選んだ地点の風速・突風（最大瞬間風速相当）の予報を取得しています。"),
          ("警報の代わりになる？", "なりません。強風・暴風警報は気象庁の公式発表を必ず確認してください。これは生活の目安ツールです。"),
          ("入力データは送信される？", "地域の選択のみを使います。個人情報は一切送信されません。")],
    rel=[("kasa-iru","☔","今日、傘いる？メーター"),("sentaku-kawaku","👕","洗濯物 乾く時間メーター"),("naminori-biyori","🏄","波乗り日和チェッカー"),("kion-kandansa","🧣","寒暖差疲労チェッカー")],
    body="""  <section class="panel">
    <h2>💨 条件</h2>
    <div class="field"><label>地域</label><select id="pref"></select></div>
    <button class="btn btn-primary" id="calcBtn">今日の風を判定</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label">今日の最大瞬間風速は</div>
      <div class="big"><span id="big">0</span><span class="unit">m/s</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">風のピーク時間</div><div class="v" id="peak">—</div></div>
      <div class="stat"><div class="k">ビニール傘</div><div class="v" id="kasa">—</div></div>
      <div class="stat"><div class="k">自転車・洗濯物</div><div class="v accent" id="jitensha">—</div></div></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
@@PREFS_JS@@
  async function calc(){
    const p = PREFS[+$('pref').value];
    $('state').textContent = '今日の風予報を取得中…';
    try{
      const r = await fetch('https://api.open-meteo.com/v1/forecast?latitude=' + p[1] + '&longitude=' + p[2] + '&hourly=wind_speed_10m,wind_gusts_10m&forecast_days=1&timezone=Asia%2FTokyo');
      const j = await r.json();
      const G = j.hourly.wind_gusts_10m, W = j.hourly.wind_speed_10m;
      const H = new Date().getHours();
      let maxG = 0, peakH = H;
      for(let h = H; h <= 23; h++){ const g = (G[h] ?? 0) / 3.6; if(g > maxG){ maxG = g; peakH = h; } }
      const label = maxG >= 25 ? '🟥 外出注意レベル' : maxG >= 20 ? '🟧 看板・飛来物に注意' : maxG >= 15 ? '🟨 かなり強い' : maxG >= 10 ? '💨 風強め' : maxG >= 5 ? '🍃 そよ風〜ふつう' : '😌 穏やか';
      $('state').textContent = '';
      $('sub').textContent = p[0] + '・いまから今日いっぱいの予報｜' + label;
      $('peak').textContent = peakH + '時ごろ';
      $('kasa').textContent = maxG >= 15 ? '全滅リスク☂️💀' : maxG >= 10 ? '反り返り注意' : '生き残れる';
      $('jitensha').textContent = maxG >= 15 ? '自転車つらい・洗濯物は飛ぶ' : maxG >= 10 ? 'ふらつき注意・洗濯バサミ2倍' : '問題なし';
      SHARE = '今日の' + p[0] + '、最大瞬間風速' + maxG.toFixed(0) + 'm/s💨（' + label.replace(/^[^ ]+ /,'') + '・ピーク' + peakH + '時）ビニール傘は「' + (maxG >= 15 ? '全滅リスク' : maxG >= 10 ? '反り返り注意' : '生き残れる') + '」\\nあなたの街の風は？👇';
      show(); anim($('big'), 0, Math.round(maxG), 900);
    }catch{ $('state').textContent = '⚠️ 予報の取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  bindShare();
})();"""
))

# ============================================================ 5 雷ゴロゴロ度
SIMS.append(dict(
    slug="kaminari-alert", cat="tool", catjp="便利ツール", grad="linear-gradient(135deg,#eff6ff,#e0f2fe)", emoji="⚡",
    title="今日の雷ゴロゴロ度", score=62,
    card_desc="夕立の前に知る。大気の不安定エネルギー（CAPE）から今日の雷リスクを判定。",
    title_tag="今日の雷ゴロゴロ度｜大気の不安定エネルギーから雷リスクを判定",
    meta_desc="気象学で使われる大気の不安定エネルギー指標（CAPE）をリアルタイム取得して、今日の雷・夕立・ゲリラ豪雨のリスクと危ない時間帯を判定する無料ツール。",
    og_title="今日の雷ゴロゴロ度",
    og_desc="大気の不安定エネルギー（CAPE）から雷リスクを判定。",
    lead="夕立や雷は「大気の不安定さ」から生まれます。気象学で実際に使われる指標CAPEを取得して、今日の雷ゴロゴロ度と危ない時間帯を出します。",
    about_h2="この判定について",
    about="""<p>CAPE（対流有効位置エネルギー）は、上昇気流がどれだけ発達できるかを表す気象学の指標で、雷雨予測の基本材料です。目安として1,000 J/kgを超えると雷雨の可能性が意識され、2,500を超えると激しい雷雨・ひょうの可能性も出てきます。このツールは気象オープンデータAPI（Open-Meteo）から今日のCAPEと降水確率を取得し、0〜100の「ゴロゴロ度」に翻訳しています。</p>
    <div class="note">ゴロゴロ度が高い日の屋外イベント・ゴルフ・河川敷は、空の急変（急な冷たい風・真っ黒な雲）に注意。雷注意報は気象庁の公式発表を確認してください。</div>""",
    faqs=[("CAPEって何？", "対流有効位置エネルギー（Convective Available Potential Energy）。大気がどれだけ「入道雲を育てる燃料」を持っているかを表す指標で、値が大きいほど雷雨のポテンシャルが高くなります。"),
          ("データの出典は？", "気象オープンデータAPI（Open-Meteo）のCAPE・降水確率の予報値を取得しています。"),
          ("入力データは送信される？", "地域の選択のみを使います。個人情報は一切送信されません。")],
    rel=[("kasa-iru","☔","今日、傘いる？メーター"),("kyou-kaze","💨","今日、風ヤバい？チェッカー"),("jishin-live","🗾","日本はいまも揺れている"),("yuyake-yohou","🌇","今日の夕焼け予報")],
    body="""  <section class="panel">
    <h2>⚡ 条件</h2>
    <div class="field"><label>地域</label><select id="pref"></select></div>
    <button class="btn btn-primary" id="calcBtn">今日のゴロゴロ度を見る</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label">今日の雷ゴロゴロ度は</div>
      <div class="big"><span id="big">0</span><span class="unit">/100</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">危ない時間帯</div><div class="v" id="peak">—</div></div>
      <div class="stat"><div class="k">大気の燃料（CAPE）</div><div class="v" id="cape">—</div></div>
      <div class="stat"><div class="k">にわか雨の確率</div><div class="v accent" id="pop">—</div></div></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
@@PREFS_JS@@
  async function calc(){
    const p = PREFS[+$('pref').value];
    $('state').textContent = '大気の不安定度を取得中…';
    try{
      const r = await fetch('https://api.open-meteo.com/v1/forecast?latitude=' + p[1] + '&longitude=' + p[2] + '&hourly=cape,precipitation_probability&forecast_days=1&timezone=Asia%2FTokyo');
      const j = await r.json();
      const C = j.hourly.cape, PP = j.hourly.precipitation_probability;
      let maxC = 0, peakH = 12, maxPop = 0;
      for(let h = 6; h <= 23; h++){
        if((C[h] ?? 0) > maxC){ maxC = C[h]; peakH = h; }
        if((PP[h] ?? 0) > maxPop) maxPop = PP[h];
      }
      const score = Math.min(100, Math.round(maxC / 30));
      const label = score >= 80 ? '⛈️ 激しい雷雨・ひょうの可能性も' : score >= 40 ? '🌩️ 雷雨ポテンシャルあり（夕立注意）' : score >= 15 ? '🌥️ 局地的にゴロつくかも' : '😌 今日は静かな空';
      $('state').textContent = '';
      $('sub').textContent = p[0] + '・今日の予報｜' + label;
      $('peak').textContent = peakH + '時ごろ';
      $('cape').textContent = Math.round(maxC) + ' J/kg';
      $('pop').textContent = maxPop + '%';
      SHARE = '今日の' + p[0] + 'の雷ゴロゴロ度は' + score + '/100⚡（' + label.replace(/^[^ ]+ /,'') + '・ピーク' + peakH + '時）\\nあなたの街の空は？👇';
      show(); anim($('big'), 0, score, 900);
    }catch{ $('state').textContent = '⚠️ 取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  bindShare();
})();"""
))

# ============================================================ 6 昼の長さ
SIMS.append(dict(
    slug="hiruma-nagasa", cat="season", catjp="季節・行事", grad="linear-gradient(135deg,#fff7ed,#fce7f3)", emoji="🌅",
    title="昼の長さメーター", score=61,
    card_desc="今日の昼は何時間何分？昨日との差を秒単位で表示。季節が動く音が聞こえる。",
    title_tag="昼の長さメーター｜今日の昼は何時間？昨日との差を秒単位で表示",
    meta_desc="今日の日の出から日の入りまでの「昼の長さ」と、昨日・明日との差を秒単位で表示する無料ツール。夏至・冬至に向かって毎日どれだけ変わっているかを体感できる。",
    og_title="昼の長さメーター｜季節が動く音が聞こえる",
    og_desc="今日の昼の長さと昨日との差を秒単位で表示。",
    lead="気づかないうちに、昼は毎日1〜2分ずつ伸び縮みしています。今日の昼の長さと「昨日との差」を秒単位で表示して、季節が動く速度を体感します。",
    about_h2="このメーターについて",
    about="""<p>昼の長さ（日の出から日の入りまで）は夏至と冬至で5時間近く違い、その間を毎日少しずつ移動しています。変化がいちばん速いのは春分・秋分のころで、1日に2分以上変わることも。このメーターは気象オープンデータAPI（Open-Meteo）から日照時間・日の出・日の入りの天文計算値を取得しています。</p>
    <div class="note">「最近日が短くなったな」と感じたら、それは気のせいではなく毎日約1〜2分ずつ確実に短くなっています。夕方の散歩の時刻を数字で調整するのにもどうぞ。</div>""",
    faqs=[("データの出典は？", "気象オープンデータAPI（Open-Meteo）の天文計算値（日の出・日の入り・日照可能時間）を取得しています。"),
          ("場所で変わるの？", "変わります。緯度が高いほど夏の昼は長く、冬の昼は短くなります。北海道と沖縄では夏至の昼の長さが1時間以上違います。"),
          ("入力データは送信される？", "地域の選択のみを使います。個人情報は一切送信されません。")],
    rel=[("yuyake-yohou","🌇","今日の夕焼け予報"),("hoshizora-shisu","🔭","今夜の星空指数"),("kotoshi-pct","📅","今年あと何％シミュレーター"),("tsugi-renkyuu","📅","次の3連休カウントダウン")],
    body="""  <section class="panel">
    <h2>🌅 条件</h2>
    <div class="field"><label>地域</label><select id="pref"></select></div>
    <button class="btn btn-primary" id="calcBtn">今日の昼の長さを見る</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label">今日の昼の長さは</div>
      <div class="big" style="font-size:min(13vw,58px);"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">日の出 / 日の入り</div><div class="v" id="sun">—</div></div>
      <div class="stat"><div class="k">昨日との差</div><div class="v" id="diff">—</div></div>
      <div class="stat"><div class="k">明日はさらに</div><div class="v accent" id="tomorrow">—</div></div></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
@@PREFS_JS@@
  const fmtDur = (s) => Math.floor(s / 3600) + '時間' + Math.round(s % 3600 / 60) + '分';
  const fmtDiff = (s) => {
    const a = Math.abs(Math.round(s)), m = Math.floor(a / 60), ss = a % 60;
    return (s >= 0 ? '+' : '−') + (m ? m + '分' : '') + ss + '秒';
  };
  async function calc(){
    const p = PREFS[+$('pref').value];
    $('state').textContent = '天文データを取得中…';
    try{
      const r = await fetch('https://api.open-meteo.com/v1/forecast?latitude=' + p[1] + '&longitude=' + p[2] + '&daily=sunrise,sunset,daylight_duration&past_days=1&forecast_days=2&timezone=Asia%2FTokyo');
      const j = await r.json();
      const D = j.daily.daylight_duration;
      const today = D[1], dy = today - D[0], dt = D[2] - today;
      const sr = j.daily.sunrise[1].slice(11), ss = j.daily.sunset[1].slice(11);
      $('state').textContent = '';
      $('big').textContent = fmtDur(today);
      $('sub').textContent = p[0] + '・今日（' + (dy >= 0 ? '昼が伸びていく季節🌱' : '昼が縮んでいく季節🍂') + '）';
      $('sun').textContent = sr + ' / ' + ss;
      $('diff').textContent = fmtDiff(dy);
      $('tomorrow').textContent = fmtDiff(dt);
      SHARE = '今日の' + p[0].split('(')[0] + 'の昼は' + fmtDur(today) + '🌅 昨日より' + fmtDiff(dy) + '。季節は毎日これだけ動いてる。\\nあなたの街の昼は？👇';
      show();
    }catch{ $('state').textContent = '⚠️ 取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  bindShare();
})();"""
))

# ============================================================ 7 ソーラー発電
SIMS.append(dict(
    slug="solar-hatsuden", cat="hikari", catjp="光熱費・節約", grad="linear-gradient(135deg,#fffbeb,#fef3c7)", emoji="🔋",
    title="今日のソーラー発電シミュ", score=60,
    card_desc="今日の日射量だと、ソーラーパネルはいくら分発電する？電気代換算つき。",
    title_tag="今日のソーラー発電シミュ｜日射量予報から発電量と電気代換算",
    meta_desc="今日・明日の日射量予報から、ベランダソーラーや屋根の太陽光パネルの発電量と電気代換算額を計算する無料シミュレーター。導入検討の体感にも。",
    og_title="今日のソーラー発電シミュ",
    og_desc="今日の日射量からパネルの発電量と電気代換算を計算。",
    lead="今日みたいな空だと、ソーラーパネルはどれだけ稼ぐのか。今日の日射量予報から、発電量と電気代換算をその場で計算します。",
    about_h2="この計算について",
    about="""<p>太陽光発電の発電量は「日射量 × パネル容量 × 損失係数」でおおよそ決まります。このシミュレーターは気象オープンデータAPI（Open-Meteo）から今日と明日の日射量（水平面全天日射量）を取得し、損失係数0.8（パネル温度・変換ロス等）で発電量を計算、電気代単価31円/kWhで金額換算しています。最近増えているベランダソーラー（0.4kW級）から戸建ての屋根（5kW級）まで対応。</p>
    <div class="note">パネルの向き・角度・影で実際の発電量は変わります。南向き最適傾斜だと表示よりやや多く、壁掛けベランダ設置だと2〜3割少なくなる傾向です。</div>""",
    faqs=[("データの出典は？", "気象オープンデータAPI（Open-Meteo）の日射量（shortwave radiation）予報値を使用しています。"),
          ("計算式は？", "日射量(kWh/m²) × パネル容量(kW) × 損失係数0.8 で概算し、電気代は31円/kWh（全国目安）で換算しています。"),
          ("入力データは送信される？", "地域とパネル容量の選択のみを使います。個人情報は一切送信されません。")],
    rel=[("denki-setsuyaku","💡","電気代 節約"),("kounetsu","🧾","光熱費の平均"),("nettaiya-check","🌙","今夜、熱帯夜？チェック"),("hiyake-timer","☀️","日焼けタイマー")],
    body="""  <section class="panel">
    <h2>🔋 条件</h2>
    <div class="field"><label>地域</label><select id="pref"></select></div>
    <div class="field"><label>パネル容量</label>
      <select id="panel">
        <option value="0.4">ベランダソーラー（0.4kW）</option>
        <option value="1">小型セット（1kW）</option>
        <option value="4" selected>戸建て屋根（4kW）</option>
        <option value="6">戸建て大きめ（6kW）</option>
      </select>
    </div>
    <button class="btn btn-primary" id="calcBtn">今日の発電量を計算</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label">今日の予想発電量は</div>
      <div class="big"><span id="big">0</span><span class="unit">kWh</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">電気代に換算</div><div class="v" id="yen">—</div></div>
      <div class="stat"><div class="k">スマホ充電なら</div><div class="v" id="phone">—</div></div>
      <div class="stat"><div class="k">明日の予想</div><div class="v accent" id="tomorrow">—</div></div></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
@@PREFS_JS@@
  async function calc(){
    const p = PREFS[+$('pref').value];
    const kw = +$('panel').value;
    $('state').textContent = '日射量予報を取得中…';
    try{
      const r = await fetch('https://api.open-meteo.com/v1/forecast?latitude=' + p[1] + '&longitude=' + p[2] + '&daily=shortwave_radiation_sum&forecast_days=2&timezone=Asia%2FTokyo');
      const j = await r.json();
      const S = j.daily.shortwave_radiation_sum;         // MJ/m2
      const gen = (mj) => mj / 3.6 * kw * 0.8;           // kWh
      const today = gen(S[0]), tmr = gen(S[1]);
      $('state').textContent = '';
      $('sub').textContent = p[0] + '・' + kw + 'kWパネル想定（日射量' + (S[0]/3.6).toFixed(1) + 'kWh/m²・損失係数0.8）';
      $('yen').textContent = '約' + Math.round(today * 31) + '円分';
      $('phone').textContent = '約' + Math.round(today * 1000 / 15) + '回分';
      $('tomorrow').textContent = tmr.toFixed(1) + 'kWh（約' + Math.round(tmr * 31) + '円）';
      SHARE = '今日の' + p[0].split('(')[0] + '、' + kw + 'kWのソーラーなら約' + today.toFixed(1) + 'kWh＝電気代' + Math.round(today * 31) + '円分発電🔋 スマホ' + Math.round(today * 1000 / 15) + '回充電できる☀️\\nあなたの街は？👇';
      show(); anim($('big'), 0, Math.round(today * 10) / 10, 900, 1);
    }catch{ $('state').textContent = '⚠️ 取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  bindShare();
})();"""
))

# ============================================================ 8 気圧ジェットコースター
SIMS.append(dict(
    slug="kiatsu-jet", cat="health", catjp="健康・カラダ", grad="linear-gradient(135deg,#fef2f2,#fee2e2)", emoji="🎢",
    title="気圧ジェットコースター指数", score=59,
    card_desc="今日、気圧はどれだけ乱高下する？この先24時間の変化幅をライブ表示。",
    title_tag="気圧ジェットコースター指数｜この先24時間の気圧変化幅をライブ表示",
    meta_desc="この先24時間の気圧の変化幅と最低気圧の時刻をリアルタイム予報から表示する無料ツール。気圧変化が気になる日の予定調整の目安に。",
    og_title="気圧ジェットコースター指数",
    og_desc="この先24時間の気圧の乱高下をライブ表示。",
    lead="頭が重い日は、空の気圧がジェットコースターしていることがあります。この先24時間の気圧の変化幅と「底」の時刻を表示します。",
    about_h2="この指数について",
    about="""<p>天気の変わり目には気圧が数時間で数hPa単位で動きます。この指数は気象オープンデータAPI（Open-Meteo）から気圧（海面更正気圧）の推移を取得し、この先24時間の変化幅を表示するものです。変化幅が大きい日は、体調と相談しながら予定を組む目安にどうぞ。</p>
    <div class="note">気圧と体調の関係は個人差が大きく、このツールは医学的な診断・予測ではありません。つらい症状が続く場合は医療機関へ。</div>""",
    faqs=[("データの出典は？", "気象オープンデータAPI（Open-Meteo）の海面更正気圧の予報値を1時間単位で取得しています。"),
          ("どれくらいの変化が「大きい」？", "このツールでは24時間で3hPa未満を「安定」、6hPa以上を「変化大きめ」、10hPa以上を「ジェットコースター級」と表示しています（台風接近時は20hPa以上動くこともあります）。"),
          ("体調不良の予測になる？", "なりません。気圧感受性は個人差が大きいため、あくまで環境データの表示です。診断・治療は医療機関にご相談ください。")],
    rel=[("kion-kandansa","🧣","寒暖差疲労チェッカー"),("sleep-debt","😴","睡眠負債シミュレーター"),("caffeine","☕","カフェイン残量メーター"),("kasa-iru","☔","今日、傘いる？メーター")],
    body="""  <section class="panel">
    <h2>🎢 条件</h2>
    <div class="field"><label>地域</label><select id="pref"></select></div>
    <button class="btn btn-primary" id="calcBtn">この先24時間の気圧を見る</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label">この先24時間の気圧変化幅は</div>
      <div class="big"><span id="big">0</span><span class="unit">hPa</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">いまの気圧</div><div class="v" id="now">—</div></div>
      <div class="stat"><div class="k">この先6時間</div><div class="v" id="trend">—</div></div>
      <div class="stat"><div class="k">気圧の底</div><div class="v accent" id="bottom">—</div></div></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
@@PREFS_JS@@
  async function calc(){
    const p = PREFS[+$('pref').value];
    $('state').textContent = '気圧の予報を取得中…';
    try{
      const r = await fetch('https://api.open-meteo.com/v1/forecast?latitude=' + p[1] + '&longitude=' + p[2] + '&hourly=pressure_msl&forecast_days=2&timezone=Asia%2FTokyo');
      const j = await r.json();
      const P = j.hourly.pressure_msl;
      const H = new Date().getHours();
      const win = P.slice(H, H + 25).filter(v => v != null);
      const max = Math.max(...win), min = Math.min(...win);
      const range = max - min;
      let bottomIdx = H;
      for(let h = H; h <= H + 24 && h < P.length; h++){ if(P[h] === min){ bottomIdx = h; break; } }
      const trend = (P[Math.min(H + 6, P.length - 1)] ?? P[H]) - P[H];
      const label = range >= 10 ? '🎢 ジェットコースター級' : range >= 6 ? '🟧 変化大きめ' : range >= 3 ? '🟨 ゆるやかに変化' : '🟢 安定';
      $('state').textContent = '';
      $('sub').textContent = p[0] + '｜' + label;
      $('now').textContent = P[H].toFixed(1) + 'hPa';
      $('trend').textContent = (trend >= 0 ? '上昇 +' : '下降 ') + trend.toFixed(1) + 'hPa';
      $('bottom').textContent = (bottomIdx >= 24 ? '明日' + (bottomIdx - 24) : bottomIdx) + '時ごろ（' + min.toFixed(0) + 'hPa）';
      SHARE = 'この先24時間の' + p[0].split('(')[0] + 'の気圧変化幅は' + range.toFixed(1) + 'hPa🎢（' + label.replace(/^[^ ]+ /,'') + '・底は' + (bottomIdx >= 24 ? '明日' + (bottomIdx-24) : bottomIdx) + '時）\\nあなたの街の空模様は？👇';
      show(); anim($('big'), 0, Math.round(range * 10) / 10, 900, 1);
    }catch{ $('state').textContent = '⚠️ 取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  bindShare();
})();"""
))

# ============================================================ 9 今週末晴れる？
SIMS.append(dict(
    slug="shuumatsu-hare", cat="travel", catjp="旅行・おでかけ", grad="linear-gradient(135deg,#cffafe,#a5f3fc)", emoji="🌤️",
    title="今週末、晴れる？", score=58,
    card_desc="土日の天気・降水確率・気温をまとめて即答。おでかけ判定つき。",
    title_tag="今週末、晴れる？｜土日の天気と降水確率をまとめて即答",
    meta_desc="次の土曜・日曜の天気・降水確率・最高気温を週間予報からまとめて表示し、おでかけ日和かを判定する無料ツール。週末の予定づくりの最初の1タップに。",
    og_title="今週末、晴れる？",
    og_desc="土日の天気をまとめて即答。おでかけ判定つき。",
    lead="週末の予定は天気から。次の土曜・日曜の天気と降水確率をまとめて取得して、「おでかけ日和度」を即答します。",
    about_h2="この判定について",
    about="""<p>このツールは気象オープンデータAPI（Open-Meteo）の週間予報から、次の土曜・日曜の天気・降水確率・最高気温を取り出して1画面にまとめます。おでかけ日和度は降水確率と天気から計算しており、どちらの日に予定を入れるべきかがひと目で分かります。</p>
    <div class="note">週間予報は先になるほど精度が下がります。週の前半に見た週末予報は、前日にもう一度確認するのが確実です。</div>""",
    faqs=[("データの出典は？", "気象オープンデータAPI（Open-Meteo）の週間予報（天気・降水確率・最高気温）を取得しています。"),
          ("どっちの日がおすすめかも分かる？", "はい。土日それぞれのおでかけ日和度を計算して、良い方の日を表示します。"),
          ("入力データは送信される？", "地域の選択のみを使います。個人情報は一切送信されません。")],
    rel=[("kasa-iru","☔","今日、傘いる？メーター"),("fujisan-mieru","🗻","今日、富士山見える？"),("tsugi-renkyuu","📅","次の3連休カウントダウン"),("hanami-yosan","🌸","花見・BBQ予算シミュレーター")],
    body="""  <section class="panel">
    <h2>🌤️ 条件</h2>
    <div class="field"><label>地域</label><select id="pref"></select></div>
    <button class="btn btn-primary" id="calcBtn">今週末の天気を見る</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
      <div class="label">今週末のおでかけ日和度は</div>
      <div class="big"><span id="big">0</span><span class="unit">点</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">土曜日</div><div class="v" id="sat">—</div></div>
      <div class="stat"><div class="k">日曜日</div><div class="v" id="sun">—</div></div>
      <div class="stat"><div class="k">おすすめ</div><div class="v accent" id="reco">—</div></div></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
@@PREFS_JS@@
@@WMO_JS@@
  async function calc(){
    const p = PREFS[+$('pref').value];
    $('state').textContent = '週間予報を取得中…';
    try{
      const r = await fetch('https://api.open-meteo.com/v1/forecast?latitude=' + p[1] + '&longitude=' + p[2] + '&daily=weather_code,precipitation_probability_max,temperature_2m_max&forecast_days=8&timezone=Asia%2FTokyo');
      const j = await r.json();
      const T = j.daily.time, C = j.daily.weather_code, PP = j.daily.precipitation_probability_max, TX = j.daily.temperature_2m_max;
      let sat = -1, sun = -1;
      T.forEach((t, i) => {
        const wd = new Date(t + 'T00:00:00').getDay();
        if(wd === 6 && sat < 0) sat = i;
        if(wd === 0 && i > 0 && sun < 0 && (sat < 0 || i > sat)) sun = i;
      });
      if(sat < 0 || sun < 0){ $('state').textContent = '週末が予報範囲に見つかりませんでした。'; return; }
      const dayScore = (i) => Math.max(0, Math.round((100 - (PP[i] ?? 50)) * (C[i] <= 3 ? 1 : C[i] <= 48 ? 0.8 : 0.45)));
      const sSat = dayScore(sat), sSun = dayScore(sun);
      const score = Math.max(sSat, sSun);
      const fmtDay = (i) => wmoEmoji(C[i]) + (WMO[C[i]] || '') + '・' + (PP[i] ?? '—') + '%・' + TX[i].toFixed(0) + '℃';
      const label = score >= 75 ? 'おでかけ日和！' : score >= 50 ? 'まずまず' : score >= 30 ? '傘と相談' : 'インドア推奨…';
      $('state').textContent = '';
      $('sub').textContent = p[0] + '・' + T[sat].slice(5).replace('-','/') + '(土)〜' + T[sun].slice(5).replace('-','/') + '(日)｜' + label;
      $('sat').textContent = fmtDay(sat);
      $('sun').textContent = fmtDay(sun);
      $('reco').textContent = sSat === sSun ? 'どちらも同じくらい' : (sSat > sSun ? '土曜日がおすすめ' : '日曜日がおすすめ');
      SHARE = '今週末の' + p[0].split('(')[0] + '、土曜は' + (WMO[C[sat]]||'') + '・日曜は' + (WMO[C[sun]]||'') + '🌤️ おでかけ日和度' + score + '点（' + label + '）\\nあなたの街の週末は？👇';
      show(); anim($('big'), 0, score, 900);
    }catch{ $('state').textContent = '⚠️ 予報の取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  $('calcBtn').addEventListener('click', calc);
  bindShare();
})();"""
))

# ============================================================ 10 地球まるごと地震
SIMS.append(dict(
    slug="chikyu-yure", cat="wonder", catjp="ふしぎ・現象", grad="linear-gradient(135deg,#eef2ff,#e0e7ff)", emoji="🌐",
    title="地球まるごと地震カウンター", score=57,
    card_desc="日本だけじゃない。直近24時間に地球全体で起きたM4.5以上の地震をライブ集計。",
    title_tag="地球まるごと地震カウンター｜世界のM4.5以上を24時間ライブ集計",
    meta_desc="米地質調査所（USGS）の地震データから、直近24時間に地球全体で起きたM4.5以上の地震回数・最大地震・日本周辺の回数をライブ表示する無料ツール。",
    og_title="地球まるごと地震カウンター",
    og_desc="直近24時間の世界の地震をライブ集計。",
    lead="日本が揺れていない日も、地球はどこかで揺れています。米地質調査所（USGS）のデータから、直近24時間の地球全体の地震を数えます。",
    about_h2="このカウンターについて",
    about="""<p>地球全体では、M4.5以上の地震だけで年間およそ1万回—つまり1日平均30回近く起きています。このカウンターは米地質調査所（USGS）のリアルタイム地震フィードから直近24時間のM4.5以上を取得し、最大の地震と日本周辺の回数もあわせて表示します。<a href="../jishin-live/">日本版カウンター</a>と見比べると、環太平洋の「火の輪」の上に住んでいることを実感できます。</p>
    <div class="note">USGSのマグニチュードは気象庁マグニチュードと算出方法が異なるため、同じ地震でも数値が少し違うことがあります。</div>""",
    faqs=[("データの出典は？", "米地質調査所（USGS）のリアルタイム地震フィード（GeoJSON）から直近24時間のデータを取得しています。"),
          ("日本の地震情報と数値が違う", "USGSと気象庁ではマグニチュードの算出方法が異なるため、同じ地震でも値がずれることがあります。日本の詳細は気象庁の発表をご覧ください。"),
          ("入力データは送信される？", "このページは何も入力せずに使えます。")],
    rel=[("jishin-live","🗾","日本はいまも揺れている"),("natsu-2050","🔥","2050年の夏、何度になる？"),("iss-doko","🛰️","ISSはいまどこ？"),("sandpile","⛰️","砂山崩しシミュレーター")],
    body="""  <section class="panel" id="resultPanel">
    <div class="result">
      <div class="label">直近24時間、地球で起きたM4.5以上の地震は</div>
      <div class="big"><span id="big">–</span><span class="unit">回</span></div>
      <div class="sub" id="sub">データを読み込み中…</div>
      <div class="statline"><div class="stat"><div class="k">最大の地震</div><div class="v" id="biggest">—</div></div>
      <div class="stat"><div class="k">日本周辺</div><div class="v" id="japan">—</div></div>
      <div class="stat"><div class="k">M6以上</div><div class="v accent" id="m6">—</div></div></div>
      <div id="list" style="margin-top:14px;"></div>
      <button class="btn btn-ghost" id="reloadBtn" style="margin-top:10px;">🔄 最新に更新</button>
@@SHARE_ROW@@
    </div>
  </section>""",
    js="""(() => {
@@JS_COMMON@@
  const ago = (ms) => { const m = Math.floor(ms / 60000); if(m < 60) return m + '分前'; const h = Math.floor(m / 60); if(h < 24) return h + '時間前'; return Math.floor(h / 24) + '日前'; };
  async function load(){
    $('sub').textContent = 'データを読み込み中…';
    try{
      const r = await fetch('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson');
      const j = await r.json();
      const now = Date.now();
      const qs = (j.features || []).map(f => ({
        mag: f.properties.mag, place: f.properties.place || '', t: f.properties.time,
        lat: f.geometry.coordinates[1], lon: f.geometry.coordinates[0],
      })).sort((a,b) => b.mag - a.mag);
      const jp = qs.filter(q => q.lat >= 24 && q.lat <= 46 && q.lon >= 122 && q.lon <= 148);
      const m6 = qs.filter(q => q.mag >= 6);
      $('sub').textContent = new Date().toLocaleString('ja-JP') + ' 時点（USGSリアルタイムフィード）';
      $('biggest').textContent = qs[0] ? 'M' + qs[0].mag.toFixed(1) + '・' + qs[0].place : '—';
      $('japan').textContent = jp.length + '回';
      $('m6').textContent = m6.length + '回';
      $('list').innerHTML = '<div style="font-weight:800;font-size:13px;margin-bottom:8px;">📋 直近24時間の大きい順TOP5</div>' + qs.slice(0, 5).map(q =>
        '<div style="display:flex;gap:8px;justify-content:space-between;padding:7px 10px;margin-bottom:5px;background:rgba(127,127,127,.07);border-radius:8px;font-size:12.5px;text-align:left;">'
        + '<span>M' + q.mag.toFixed(1) + '　' + q.place + '</span><span style="opacity:.7;white-space:nowrap;">' + ago(now - q.t) + '</span></div>').join('');
      SHARE = '直近24時間、地球ではM4.5以上の地震が' + qs.length + '回起きてた🌐 最大はM' + (qs[0] ? qs[0].mag.toFixed(1) : '—') + '。日本周辺は' + jp.length + '回。\\n地球のいまの揺れはこちら👇';
      anim($('big'), 0, qs.length, 900);
    }catch{ $('sub').textContent = '⚠️ データの取得に失敗しました。時間をおいて再度お試しください。'; }
  }
  load();
  $('reloadBtn').addEventListener('click', load);
  bindShare();
})();"""
))

# ============================================================ 投入処理
IDX = os.path.join(ROOT, "index.html")
with io.open(IDX, encoding="utf-8") as f:
    html = f.read()
assert "sims/umareta-hi-tenki/" not in html, "既に挿入済み（中止）"

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
    js = s["js"].replace("@@JS_COMMON@@", JS_COMMON).replace("@@PREFS_JS@@", PREFS_JS).replace("@@WMO_JS@@", WMO_JS)
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

# index.html: カード + ランキング + 本数
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

# /live/: カード追加 + 25→35表記更新
LIVE = os.path.join(ROOT, "live", "index.html")
with io.open(LIVE, encoding="utf-8") as f:
    lv = f.read()
def live_card(s):
    return '\n    <a class="sim-card" href="../sims/%s/"><div class="thumb" style="background:%s"><span class="emoji">%s</span></div><div class="body"><div class="cat">%s</div><h3>%s</h3><p>%s</p><span class="go">触ってみる →</span></div></a>' % (
        s["slug"], s["grad"], s["emoji"], s["catjp"], s["title"], s["card_desc"])
by = {s["slug"]: s for s in SIMS}
# 天気・気候グループの末尾(yuyake-yohouカード直後)に6本
anchor = lv.index('yuyake-yohou/')
anchor = lv.index('</a>', anchor) + 4
weather = "".join(live_card(by[k]) for k in ["kasa_iru" if False else "shuumatsu-hare", "kyou-kaze", "kaminari-alert", "kiatsu-jet", "fujisan-mieru", "hiruma-nagasa"])
lv = lv[:anchor] + weather + lv[anchor:]
# 地球・宇宙(kuuki-kireiカード直後)に2本
anchor = lv.index('kuuki-kirei/')
anchor = lv.index('</a>', anchor) + 4
lv = lv[:anchor] + live_card(by["chikyu-yure"]) + live_card(by["natsu-2050"]) + lv[anchor:]
# お金(genchi-ikura直後)に1本
anchor = lv.index('genchi-ikura/')
anchor = lv.index('</a>', anchor) + 4
lv = lv[:anchor] + live_card(by["solar-hatsuden"]) + lv[anchor:]
# 暮らし(tanjobi-jiken直後)に1本
anchor = lv.index('tanjobi-jiken/')
anchor = lv.index('</a>', anchor) + 4
lv = lv[:anchor] + live_card(by["umareta-hi-tenki"]) + lv[anchor:]
# 表記 25→35
lv = lv.replace("シミュレーター25選", "シミュレーター35選").replace("25本を一覧掲載", "35本を一覧掲載").replace("25本のコレクション", "35本のコレクション").replace("ライブシミュレーター集", "ライブシミュレーター集")
# 出典テーブルの利用シミュレーター列を軽く更新
lv = lv.replace("傘いる？/洗濯/日焼け/夕焼け/星空/熱帯夜/寒暖差/暑さランキング/世界気温/波乗り/ゲレンデ積雪",
                "傘いる？/洗濯/日焼け/夕焼け/星空/熱帯夜/寒暖差/暑さランキング/世界気温/波乗り/ゲレンデ積雪/風/雷/気圧/週末天気/富士山/昼の長さ/ソーラー/生まれた日の天気(過去)/2050年の夏(気候)")
lv = lv.replace("<tr><td>米海洋大気庁（NOAA SWPC）</td>",
                "<tr><td>米地質調査所（USGS）</td><td>世界の地震（リアルタイム）</td><td>地球まるごと地震カウンター</td></tr>\n      <tr><td>米海洋大気庁（NOAA SWPC）</td>")
with io.open(LIVE, "w", encoding="utf-8") as f:
    f.write(lv)
print("patched live/index.html: +10 cards, 25->35")

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
