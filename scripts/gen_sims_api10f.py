# -*- coding: utf-8 -*-
"""API連携シリーズ第6弾 10本（1回限り）。sims生成→OGP→index→/live/→sitemap→share.js。
Ahrefs(jp) KD0の穴場KW狙い: 為替ドル円312k/時差クラスタ150k+/今日の服装78k/今日の月53k/18金相場1g今日122k
/祝日カレンダー64k+/アメリカ祝日10k/確定申告いつまで73k/お盆いつ64k/花粉今日119k(KD5)
API: Frankfurter(ECB為替) / gold-api.com(金・銀・プラチナ) / holidays-jp / Nager.Date / Open-Meteo / ブラウザIntl
"""
import os, io, re, json

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPTS)
TODAY = "2026-09-12"

_g10c = io.open(os.path.join(SCRIPTS, "gen_sims_api10c.py"), encoding="utf-8").read()
def _block(name):
    return re.search(name + r' = """(.*?)"""', _g10c, re.S).group(1)
SKELETON = _block("SKELETON")
SHARE_ROW = _block("SHARE_ROW")
JS_COMMON = _block("JS_COMMON")
PREF_ROWS = eval("[" + re.search(r'PREF_ROWS = \[(.*?)\]\n', _g10c, re.S).group(1) + "]")
PREFS_JS = "  const PREFS = [\n" + "\n".join("    ['%s',%s,%s]," % r for r in PREF_ROWS) + "\n  ];\n  $('pref').innerHTML = PREFS.map((p,i) => '<option value=\"' + i + '\"' + (i===12?' selected':'') + '>' + p[0] + '</option>').join('');"
WORLD = io.open(os.path.join(SCRIPTS, "_world_rings.json"), encoding="utf-8").read().strip()

# DPR対応canvasの共通ヘルパ（Retinaでボケない）
FIT_JS = r"""  function fitCanvas(cv, ratio){ const par=cv.parentElement, cs=getComputedStyle(par), pl=parseFloat(cs.paddingLeft)||0, pr=parseFloat(cs.paddingRight)||0;
    if(innerWidth<640 && pl>0){ cv.style.marginLeft=(-pl)+'px'; cv.style.marginRight=(-pr)+'px'; cv.style.width='calc(100% + '+(pl+pr)+'px)'; } else { cv.style.marginLeft=''; cv.style.marginRight=''; cv.style.width='100%'; }
    const W=cv.clientWidth || par.clientWidth; let H=Math.round(W*ratio); const dpr=Math.min(window.devicePixelRatio||1,2); cv.style.height=H+'px'; H=cv.clientHeight||H; cv.width=Math.floor(W*dpr); cv.height=Math.floor(H*dpr); const x=cv.getContext('2d'); x.setTransform(dpr,0,0,dpr,0,0); return {x,W,H}; }
  const pad2 = n => String(n).padStart(2,'0');
  const ymd = d => d.getFullYear()+'-'+pad2(d.getMonth()+1)+'-'+pad2(d.getDate());
  const jaDate = d => d.getFullYear()+'年'+(d.getMonth()+1)+'月'+d.getDate()+'日('+'日月火水木金土'[d.getDay()]+')';"""
# 現在地ボタン（都道府県selectと併用）
GEO_JS = r"""  function useGeo(cb){ if(!navigator.geolocation){ alert('この端末では現在地を取得できません'); return; }
    $('geoBtn').textContent='取得中…';
    navigator.geolocation.getCurrentPosition(p => { $('geoBtn').textContent='📍 現在地で表示中'; cb(p.coords.latitude, p.coords.longitude, '現在地'); },
      () => { $('geoBtn').textContent='📍 現在地を使う'; alert('位置情報が取得できませんでした。都道府県を選んでください。'); }, {timeout: 8000}); }"""

def faq_dl(faqs): return "".join("<dt>%s</dt><dd>%s</dd>" % (q, a) for q, a in faqs)
def faq_ld(faqs):
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in faqs]}, ensure_ascii=False)
def related(items):
    return "".join('<a class="related-card" href="../%s/"><span class="e">%s</span><span>%s</span></a>' % (s, e, t) for s, e, t in items)

# index.html の既存カードからカテゴリ別gradientを拾う（HTML上の一貫性のため）
_idx = io.open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
def grad_of(cat):
    m = re.search(r'data-cat="%s"[^>]*>\s*<div class="thumb" style="background:([^"]+)"' % cat, _idx)
    return m.group(1) if m else "linear-gradient(135deg,#eef2ff,#e0e7ff)"
CATJP = dict(money="お金・時間", travel="旅行・おでかけ", beauty="美容・ファッション", wonder="ふしぎ・現象",
             season="季節・行事", tax="税金・確定申告", health="健康・カラダ")

SIMS = []
def sim(**kw):
    kw["catjp"] = CATJP[kw["cat"]]; kw["grad"] = grad_of(kw["cat"]); SIMS.append(kw)

# ============================================================
# 1 ドル円 為替チャート（今日のレート＋推移）  KW: 為替 ドル円 312k/KD0
# ============================================================
sim(slug="dollar-yen-chart", cat="money", emoji="💱", score=68,
    title="ドル円 為替チャート（今日のレートと推移）",
    card_desc="今日のドル円は？欧州中央銀行の公表レートで最新値と30〜180日の推移チャートを表示。ユーロ・ポンドも。",
    title_tag="ドル円 為替チャート｜今日のレートと30〜180日の推移（ユーロ・ポンド・豪ドル対応）",
    meta_desc="今日のドル円レートはいくら？欧州中央銀行（ECB）公表の為替レートを取得し、最新値・前日比・30〜180日の推移チャートを表示する無料ツール。ユーロ・ポンド・豪ドル・元・ウォンにも対応。円換算の計算もできます。",
    og_title="ドル円 為替チャート｜今日のレートと推移", og_desc="ECB公表レートで今日のドル円と推移チャートをライブ表示。",
    lead="今日のドル円は、いくら？ 欧州中央銀行が毎営業日公表する為替レートを取得して、<b>最新値・前日比・推移チャート</b>を表示します。通貨を切り替えれば、ユーロや豪ドル、ウォンも見られます。",
    about_h2="このチャートについて",
    about="""<p>表示しているのは<b>欧州中央銀行（ECB）が毎営業日1回公表する参考為替レート</b>です。金融機関のリアルタイム相場（分単位で動く為替市場の気配値）ではなく、日次の基準値のため、「今日はだいたい1ドル何円か」「この3ヶ月でどれくらい円安・円高に動いたか」を把握する用途に向いています。土日・祝日は更新されません。</p>
    <h2>円安・円高は、どっちが得？</h2>
    <p>1ドル＝150円が160円になるのが<b>円安</b>（円の価値が下がる）、140円になるのが<b>円高</b>です。海外旅行・輸入品・海外サービスの支払いは円高のほうが安く済み、輸出企業の業績や海外資産の円換算額は円安で増えます。為替は日米の金利差、貿易収支、政府・日銀の介入観測などで日々動きます。</p>
    <div class="tbl-scroll"><table class="seo-table"><tr><th>ドル円が10円動くと…</th><th>影響の例</th></tr>
    <tr><td>1,000ドルの海外旅行費用</td><td>約1万円 変わる</td></tr>
    <tr><td>月3万円の米国株積立（ドル建て）</td><td>買える口数が約6〜7%変わる</td></tr>
    <tr><td>100万円の外貨預金（米ドル）</td><td>評価額が約6〜7万円 変わる</td></tr></table></div>
    <p>手元の外貨を円にしたい・円を外貨にしたい計算は、下の換算欄でどうぞ。海外で1万円が現地通貨でいくらになるかは<a href="../genchi-ikura/">1万円、現地でいくら？</a>、円安の体感は<a href="../enyasu-taikan/">円安体感メーター</a>もあわせて。</p>
    <div class="note">為替レートは投資判断の根拠にはしないでください。実際の両替・送金レートは金融機関ごとの手数料（TTS/TTBのスプレッド）で本レートと数円異なります。</div>""",
    faqs=[("レートはいつ更新される？", "欧州中央銀行の公表に合わせて、毎営業日1回（日本時間の夜）更新されます。土日祝は前営業日の値が表示されます。"),
          ("銀行の両替レートと違うのはなぜ？", "銀行や両替所は基準レートに手数料（TTS/TTB）を上乗せするため、片道で1〜3円程度の差が出るのが一般的です。"),
          ("リアルタイムのレートが知りたい", "分単位で動く為替市場の相場は証券会社・FX会社の取引画面をご確認ください。本ツールは日次の基準値です。"),
          ("入力データは送信される？", "換算に入れた金額はブラウザ内でのみ計算され、外部には送信されません。")],
    rel=[("genchi-ikura","💴","1万円、現地でいくら？"),("enyasu-taikan","📉","円安体感メーター"),("kin-souba","🥇","18金 相場 1g 今日"),("btc-tara","₿","もしビットコイン買ってたら")],
    body="""  <section class="panel" id="resultPanel">
    <div class="result">
      <div class="label">今日の <span id="curName">米ドル</span>／円</div>
      <div class="big"><span id="big">—</span><span class="unit" id="unitLbl">円</span></div>
      <div class="sub" id="sub">レートを取得中…</div>
      <div class="statline"><div class="stat"><div class="k">前日比</div><div class="v accent" id="diff">—</div></div>
      <div class="stat"><div class="k"><span id="periodHi">90</span>日の高値</div><div class="v" id="hi">—</div></div>
      <div class="stat"><div class="k"><span id="periodLo">90</span>日の安値</div><div class="v" id="lo">—</div></div></div>
      <canvas id="cv" style="width:100%;height:auto;display:block;margin-top:16px;background:#fff;border:1px solid var(--line);border-radius:8px;"></canvas>
      <div class="row" style="margin-top:14px;text-align:left;">
        <div class="field" style="margin-bottom:0;"><label>通貨</label><select id="cur"><option value="USD" selected>米ドル（USD）</option><option value="EUR">ユーロ（EUR）</option><option value="GBP">英ポンド（GBP）</option><option value="AUD">豪ドル（AUD）</option><option value="CNY">中国元（CNY）</option><option value="KRW">韓国ウォン（KRW）</option><option value="THB">タイバーツ（THB）</option><option value="CHF">スイスフラン（CHF）</option></select></div>
        <div class="field" style="margin-bottom:0;"><label>期間</label><div style="display:flex;gap:8px;"><button class="chip" data-days="30" type="button">30日</button><button class="chip is-on" data-days="90" type="button">90日</button><button class="chip" data-days="180" type="button">180日</button></div></div>
      </div>
      <div class="row" style="margin-top:12px;text-align:left;">
        <div class="field" style="margin-bottom:0;"><label><span id="amtLbl">米ドル</span> → 円</label><input type="number" id="amt" value="100" min="0" inputmode="decimal"></div>
        <div class="field" style="margin-bottom:0;"><label>円換算</label><div class="v" id="conv" style="font-size:22px;font-weight:700;padding:11px 0;font-variant-numeric:tabular-nums;">—</div></div>
      </div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js=r"""(() => {
@@JS_COMMON@@
@@FIT_JS@@
  const NAMES={USD:'米ドル',EUR:'ユーロ',GBP:'英ポンド',AUD:'豪ドル',CNY:'中国元',KRW:'韓国ウォン',THB:'タイバーツ',CHF:'スイスフラン'};
  let cur='USD', days=90, series=[];
  const per = () => cur==='KRW' ? 100 : 1;                      // ウォンは100単位で表示
  const fmt = v => (v*per()).toFixed(2)+'円';
  async function load(){
    $('sub').textContent='レートを取得中…';
    try{
      const end=new Date(), start=new Date(end.getTime()-(days+12)*86400000);
      const r=await fetch(`https://api.frankfurter.dev/v1/${ymd(start)}..${ymd(end)}?base=${cur}&symbols=JPY`);
      const j=await r.json();
      const keys=Object.keys(j.rates).sort().slice(-days);
      series=keys.map(k=>({d:k,v:j.rates[k].JPY}));
      if(series.length<2) throw new Error('short');
      const last=series[series.length-1], prev=series[series.length-2];
      const dv=(last.v-prev.v)*per();
      $('curName').textContent=NAMES[cur];
      $('big').textContent=(last.v*per()).toFixed(2);
      $('unitLbl').textContent= per()===100 ? '円/100ウォン' : '円';
      $('sub').textContent=last.d.replace(/-/g,'/')+' 公表（欧州中央銀行の参考レート・毎営業日更新）';
      $('diff').textContent=(dv>=0?'+':'')+dv.toFixed(2)+'円'+(dv>=0?'（円安）':'（円高）');
      $('diff').style.color= dv>=0 ? '#c4442b' : '#1b4a63';
      const vals=series.map(s=>s.v);
      $('hi').textContent=fmt(Math.max(...vals)); $('lo').textContent=fmt(Math.min(...vals));
      $('periodHi').textContent=days; $('periodLo').textContent=days;
      $('amtLbl').textContent=NAMES[cur];
      draw(); conv();
      SHARE=`今日の${NAMES[cur]}は ${(last.v*per()).toFixed(2)}円（前日比${dv>=0?'+':''}${dv.toFixed(2)}円）💱 ${days}日の推移チャートはこちら👇`;
    }catch(e){ $('sub').textContent='⚠️ レートを取得できませんでした。時間をおいて再度お試しください。'; }
  }
  function draw(){
    const cv=$('cv'); const {x,W,H}=fitCanvas(cv,0.5);
    x.fillStyle='#fff'; x.fillRect(0,0,W,H);
    if(!series.length) return;
    const L=54,R=14,T=18,B=30, w=W-L-R, h=H-T-B;
    const vals=series.map(s=>s.v*per()); let lo=Math.min(...vals), hi=Math.max(...vals);
    const span=Math.max(hi-lo, 0.5); lo-=span*0.08; hi+=span*0.08;
    const X=i=>L+i/(series.length-1)*w, Y=v=>T+(1-(v-lo)/(hi-lo))*h;
    // グリッド＋目盛
    x.strokeStyle='rgba(20,24,29,.08)'; x.lineWidth=1; x.font='11px system-ui,sans-serif'; x.fillStyle='#8b929c'; x.textAlign='right';
    for(let k=0;k<=4;k++){ const v=lo+(hi-lo)*k/4, y=Y(v); x.beginPath(); x.moveTo(L,y); x.lineTo(W-R,y); x.stroke(); x.fillText(v.toFixed(per()===100?2:1), L-6, y+4); }
    // 面のグラデ
    const g=x.createLinearGradient(0,T,0,T+h); g.addColorStop(0,'rgba(44,107,134,.22)'); g.addColorStop(1,'rgba(44,107,134,0)');
    x.beginPath(); x.moveTo(X(0),Y(vals[0])); vals.forEach((v,i)=>x.lineTo(X(i),Y(v))); x.lineTo(X(vals.length-1),T+h); x.lineTo(X(0),T+h); x.closePath(); x.fillStyle=g; x.fill();
    // 線
    x.beginPath(); vals.forEach((v,i)=> i?x.lineTo(X(i),Y(v)):x.moveTo(X(i),Y(v))); x.strokeStyle='#2c6b86'; x.lineWidth=2; x.lineJoin='round'; x.stroke();
    // 高値・安値マーカー
    const iH=vals.indexOf(Math.max(...vals)), iL=vals.indexOf(Math.min(...vals));
    x.textAlign='center'; x.font='600 11px system-ui,sans-serif';
    x.fillStyle='#c4442b'; x.beginPath(); x.arc(X(iH),Y(vals[iH]),3.5,0,6.283); x.fill(); x.fillText('高 '+vals[iH].toFixed(2), X(iH), Y(vals[iH])-9);
    x.fillStyle='#1b4a63'; x.beginPath(); x.arc(X(iL),Y(vals[iL]),3.5,0,6.283); x.fill(); x.fillText('安 '+vals[iL].toFixed(2), X(iL), Y(vals[iL])+17);
    // 最新点
    const n=vals.length-1; x.fillStyle='#c4442b'; x.beginPath(); x.arc(X(n),Y(vals[n]),5,0,6.283); x.fill(); x.fillStyle='#fff'; x.beginPath(); x.arc(X(n),Y(vals[n]),2.2,0,6.283); x.fill();
    // 日付ラベル
    x.fillStyle='#8b929c'; x.font='11px system-ui,sans-serif';
    [0, Math.floor(n/2), n].forEach((i,k)=>{ x.textAlign= k===0?'left':k===1?'center':'right'; x.fillText(series[i].d.slice(5).replace('-','/'), X(i), H-8); });
  }
  function conv(){ if(!series.length) return; const v=series[series.length-1].v, a=+$('amt').value||0; $('conv').textContent=Math.round(a*v).toLocaleString('ja-JP')+' 円'; }
  document.querySelectorAll('[data-days]').forEach(b=>b.addEventListener('click',()=>{ document.querySelectorAll('[data-days]').forEach(c=>c.classList.remove('is-on')); b.classList.add('is-on'); days=+b.dataset.days; load(); }));
  $('cur').addEventListener('change',()=>{ cur=$('cur').value; load(); });
  $('amt').addEventListener('input',conv);
  let rt; addEventListener('resize',()=>{ clearTimeout(rt); rt=setTimeout(draw,200); });
  load(); bindShare();
})();""")

# ============================================================
# 2 世界の時差・今何時（日照マップ）  KW: 国名 時差 のロングテール群 150k+/KD0-3
# ============================================================
_CITIES = [
 ("ニューヨーク（アメリカ東部）","America/New_York",40.7,-74.0),("ロサンゼルス（アメリカ西部）","America/Los_Angeles",34.1,-118.2),
 ("シカゴ（アメリカ中部）","America/Chicago",41.9,-87.6),("ホノルル（ハワイ）","Pacific/Honolulu",21.3,-157.9),
 ("バンクーバー（カナダ）","America/Vancouver",49.3,-123.1),("メキシコシティ","America/Mexico_City",19.4,-99.1),
 ("サンパウロ（ブラジル）","America/Sao_Paulo",-23.5,-46.6),("ロンドン（イギリス）","Europe/London",51.5,-0.1),
 ("パリ（フランス）","Europe/Paris",48.9,2.4),("ベルリン（ドイツ）","Europe/Berlin",52.5,13.4),
 ("ローマ・ミラノ（イタリア）","Europe/Rome",41.9,12.5),("マドリード（スペイン）","Europe/Madrid",40.4,-3.7),
 ("イスタンブール（トルコ）","Europe/Istanbul",41.0,29.0),("モスクワ（ロシア）","Europe/Moscow",55.8,37.6),
 ("カイロ（エジプト）","Africa/Cairo",30.0,31.2),("ドバイ（UAE）","Asia/Dubai",25.2,55.3),
 ("デリー（インド）","Asia/Kolkata",28.6,77.2),("バンコク（タイ）","Asia/Bangkok",13.8,100.5),
 ("ハノイ・ホーチミン（ベトナム）","Asia/Ho_Chi_Minh",10.8,106.7),("シンガポール","Asia/Singapore",1.3,103.8),
 ("クアラルンプール（マレーシア）","Asia/Kuala_Lumpur",3.1,101.7),("ジャカルタ（インドネシア）","Asia/Jakarta",-6.2,106.8),
 ("マニラ（フィリピン）","Asia/Manila",14.6,121.0),("香港","Asia/Hong_Kong",22.3,114.2),
 ("上海・北京（中国）","Asia/Shanghai",31.2,121.5),("台北（台湾）","Asia/Taipei",25.0,121.5),
 ("ソウル（韓国）","Asia/Seoul",37.6,127.0),("シドニー（オーストラリア）","Australia/Sydney",-33.9,151.2),
 ("オークランド（ニュージーランド）","Pacific/Auckland",-36.8,174.8),("ヨハネスブルグ（南アフリカ）","Africa/Johannesburg",-26.2,28.0),
]
_CITY_JS = json.dumps([[n,tz,la,lo] for n,tz,la,lo in _CITIES], ensure_ascii=False)
_JISA_TABLE = "".join("<tr><td>%s</td><td>%s</td></tr>" % (n, tz) for n,tz,la,lo in _CITIES)
sim(slug="sekai-jisa", cat="travel", emoji="🌐", score=67,
    title="世界の時差・いま何時？（日照マップ付き）",
    card_desc="シンガポール・アメリカ・韓国…30都市の現在時刻と日本との時差を、昼と夜が動く世界地図で。",
    title_tag="世界の時差・いま何時？｜シンガポール・アメリカ・韓国・ハワイ…30都市の時差計算と日照マップ",
    meta_desc="海外は今何時？シンガポール・アメリカ（ニューヨーク/ロサンゼルス）・韓国・台湾・タイ・ハワイ・イギリス・フランス・ドイツなど30都市の現在時刻と日本との時差を一覧表示する無料ツール。昼と夜の境目が動く世界地図つき。サマータイムも自動反映。",
    og_title="世界の時差・いま何時？", og_desc="30都市の現在時刻と日本との時差を日照マップで一目で。",
    lead="「あの国は、いま何時？」を一目で。都市を選ぶと現在時刻と日本との時差を表示し、<b>地球のどこが昼でどこが夜か</b>を世界地図に描きます。サマータイム中かどうかも自動で反映されます。",
    about_h2="時差の見かた",
    about="""<p>時差は、日本（UTC+9）との差で表しています。「−13時間」なら日本より13時間遅れ＝日本が朝9時のとき、現地は前日の夜8時です。海外へ電話やビデオ会議をするときは「相手の営業時間が日本の何時にあたるか」を先に確認しておくと失敗しません。</p>
    <h2>主な国・都市の時差 早見表（日本基準）</h2>
    <div class="tbl-scroll"><table class="seo-table"><tr><th>都市（国）</th><th>タイムゾーン</th></tr>@@JISA_TABLE@@</table></div>
    <p>※時差はサマータイム（夏時間）で1時間変わります。アメリカ・カナダは3月〜11月、ヨーロッパは3月末〜10月末、オーストラリア（シドニー）は10月〜4月が夏時間。本ツールはブラウザの世界時計機能で自動判定しているため、選んだ都市の「いまの時差」がそのまま出ます。日本・韓国・中国・東南アジア諸国にサマータイムはありません。</p>
    <h2>昼と夜が動く地図の仕組み</h2>
    <p>地図の暗い部分は、いまこの瞬間に夜になっている地域です。太陽が真上に来る地点（☀）は1時間に15度ずつ西へ移動し、季節によって北半球側・南半球側へ傾きます。夏至のころは北極周辺が一日中昼（白夜）、冬至のころは一日中夜（極夜）になる様子も、この地図で確認できます。</p>
    <p>時差ボケの回復日数は<a href="../jisa-boke/">時差ボケ回復シミュレーター</a>、旅先の祝日は<a href="../kaigai-shukujitsu/">海外の祝日カレンダー</a>でどうぞ。</p>""",
    faqs=[("時差はどう計算する？", "現地の標準時（UTCからの差）と日本（UTC+9）の差です。例えばニューヨークは標準時UTC−5なので日本より14時間遅れ、夏時間中はUTC−4で13時間遅れになります。"),
          ("サマータイムは自動で反映される？", "はい。ブラウザに内蔵された世界のタイムゾーン情報を使うため、現在夏時間かどうかを自動で判定します。"),
          ("アメリカの時差はひとつじゃない？", "アメリカ本土だけで東部・中部・山岳部・太平洋の4つ、ハワイ・アラスカを含めると6つの時間帯があります。都市で選んでください。"),
          ("入力データは送信される？", "このページは外部にデータを送信しません。時刻計算はすべてブラウザ内で行います。")],
    rel=[("jisa-boke","✈️","時差ボケ回復シミュレーター"),("kaigai-shukujitsu","📅","海外の祝日カレンダー"),("sekai-kion","🌡️","世界の気温いま"),("hiruma-nagasa","🌅","昼の長さメーター")],
    body="""  <section class="panel" id="resultPanel">
    <div class="result">
      <div class="label"><span id="cityName">ニューヨーク</span>は、いま</div>
      <div class="big" style="font-size:min(15vw,72px);"><span id="big">--:--</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">日本との時差</div><div class="v accent" id="jisa">—</div></div>
      <div class="stat"><div class="k">現地の日付</div><div class="v" id="ldate">—</div></div>
      <div class="stat"><div class="k">サマータイム</div><div class="v" id="dst">—</div></div></div>
      <canvas id="cv" style="width:100%;height:auto;display:block;margin-top:16px;background:#eef3f6;border:1px solid var(--line);border-radius:8px;"></canvas>
      <div class="field" style="margin:14px 0 0;text-align:left;"><label>都市を選ぶ</label><select id="city"></select></div>
      <div id="clocks" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px;margin-top:14px;text-align:left;"></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js=r"""(() => {
@@JS_COMMON@@
@@FIT_JS@@
  const CITIES = @@CITIES@@;
  const WORLD = @@WORLD@@;
  let sel = 0;
  $('city').innerHTML = CITIES.map((c,i)=>`<option value="${i}"${i===0?' selected':''}>${c[0]}</option>`).join('');
  function offsetMin(tz, date){ // タイムゾーンのUTCオフセット（分）
    const p = new Intl.DateTimeFormat('en-US',{timeZone:tz,hourCycle:'h23',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',second:'2-digit'}).formatToParts(date);
    const o={}; p.forEach(q=>o[q.type]=q.value);
    return Math.round((Date.UTC(+o.year, +o.month-1, +o.day, +o.hour, +o.minute, +o.second) - date.getTime())/60000);
  }
  function localParts(tz, date){
    const p = new Intl.DateTimeFormat('ja-JP',{timeZone:tz,hourCycle:'h23',weekday:'short',month:'numeric',day:'numeric',hour:'2-digit',minute:'2-digit'}).formatToParts(date);
    const o={}; p.forEach(q=>o[q.type]=q.value); return o;
  }
  function sun(date){ // NOAAの近似式：太陽直下点の緯度・経度
    const start=Date.UTC(date.getUTCFullYear(),0,1), doy=Math.floor((date-start)/86400000);
    const g=2*Math.PI/365*(doy + (date.getUTCHours()-12)/24);
    const eot=229.18*(0.000075+0.001868*Math.cos(g)-0.032077*Math.sin(g)-0.014615*Math.cos(2*g)-0.040849*Math.sin(2*g));
    const dec=0.006918-0.399912*Math.cos(g)+0.070257*Math.sin(g)-0.006758*Math.cos(2*g)+0.000907*Math.sin(2*g)-0.002697*Math.cos(3*g)+0.00148*Math.sin(3*g);
    const tmin=date.getUTCHours()*60+date.getUTCMinutes()+date.getUTCSeconds()/60;
    let lon=(720-tmin-eot)/4; lon=((lon+540)%360)-180;
    return {lat:dec*180/Math.PI, lon};
  }
  function draw(){
    const cv=$('cv'); const {x,W,H}=fitCanvas(cv,0.5);
    const px=lon=>(lon+180)/360*W, py=lat=>(90-lat)/180*H;
    x.fillStyle='#e6edf2'; x.fillRect(0,0,W,H);
    // 陸地
    x.fillStyle='#cdd5cc'; x.strokeStyle='rgba(20,24,29,.25)'; x.lineWidth=.6;
    for(const ring of WORLD){ x.beginPath(); ring.forEach((p,i)=> i?x.lineTo(px(p[0]),py(p[1])):x.moveTo(px(p[0]),py(p[1]))); x.closePath(); x.fill(); x.stroke(); }
    // 夜の影
    const s=sun(new Date()); const dec=s.lat*Math.PI/180;
    x.beginPath();
    for(let lon=-180;lon<=180;lon+=2){ const Hh=(lon-s.lon)*Math.PI/180; let lat=Math.atan(-Math.cos(Hh)/Math.tan(dec))*180/Math.PI; if(!isFinite(lat)) lat=0; lon===-180?x.moveTo(px(lon),py(lat)):x.lineTo(px(lon),py(lat)); }
    const poleY = dec>=0 ? H : 0;               // 北半球が夏なら夜は南極側へ
    x.lineTo(W,poleY); x.lineTo(0,poleY); x.closePath();
    x.fillStyle='rgba(16,22,52,.42)'; x.fill();
    // 太陽
    x.fillStyle='#f4c542'; x.beginPath(); x.arc(px(s.lon),py(s.lat),7,0,6.283); x.fill();
    x.strokeStyle='rgba(244,197,66,.6)'; x.lineWidth=2; x.beginPath(); x.arc(px(s.lon),py(s.lat),11,0,6.283); x.stroke();
    // 都市
    CITIES.forEach((c,i)=>{ const cx=px(c[3]), cy=py(c[2]); x.fillStyle= i===sel?'#c4442b':'rgba(27,74,99,.85)'; x.beginPath(); x.arc(cx,cy,i===sel?5:2.6,0,6.283); x.fill(); });
    // 東京
    const tx=px(139.7), ty=py(35.7); x.fillStyle='#14181d'; x.beginPath(); x.arc(tx,ty,3.5,0,6.283); x.fill();
    x.font='600 11px system-ui,sans-serif'; x.fillStyle='#14181d'; x.textAlign='left'; x.fillText('東京', tx+6, ty+4);
    const c=CITIES[sel]; x.fillStyle='#c4442b'; x.fillText(c[0].split('（')[0], px(c[3])+7, py(c[2])-6);
  }
  function tick(){
    const now=new Date(), c=CITIES[sel];
    const o=localParts(c[1], now);
    $('cityName').textContent=c[0].split('（')[0];
    $('big').textContent=o.hour+':'+o.minute;
    const off=offsetMin(c[1],now), jp=540, d=(off-jp)/60;
    $('jisa').textContent=(d>0?'+':'')+(Number.isInteger(d)?d:d.toFixed(1))+'時間';
    const jan=offsetMin(c[1], new Date(now.getFullYear(),0,15)), jul=offsetMin(c[1], new Date(now.getFullYear(),6,15));
    const hasDst = jan!==jul, inDst = hasDst && off===Math.max(jan,jul);
    $('dst').textContent= !hasDst ? 'なし' : (inDst ? '実施中（+1時間）' : '期間外');
    $('ldate').textContent=o.month+'/'+o.day+'（'+o.weekday+'）';
    const jpH=now.getHours();
    $('sub').textContent=`日本は ${pad2(jpH)}:${pad2(now.getMinutes())}。${c[0].split('（')[0]}は日本より${Math.abs(d)}時間${d>=0?'進んで':'遅れて'}います`;
    $('clocks').innerHTML=CITIES.map((cc,i)=>{ const p=localParts(cc[1],now); const dd=(offsetMin(cc[1],now)-jp)/60; return `<div style="padding:8px 10px;border:1px solid var(--line);border-radius:6px;background:${i===sel?'var(--teal-l)':'#fff'};cursor:pointer;" data-i="${i}"><div style="font-size:11px;color:var(--ink-3);">${cc[0].split('（')[0]}</div><div style="font-size:18px;font-weight:700;font-variant-numeric:tabular-nums;">${p.hour}:${p.minute} <span style="font-size:11px;color:var(--ink-2);font-weight:600;">${dd>=0?'+':''}${dd}h</span></div></div>`; }).join('');
    SHARE=`${c[0].split('（')[0]}はいま${o.hour}:${o.minute}（日本との時差${d>0?'+':''}${d}時間）🌐 昼と夜が動く世界地図で見る👇`;
    draw();
  }
  $('city').addEventListener('change',()=>{ sel=+$('city').value; tick(); });
  $('clocks').addEventListener('click',e=>{ const t=e.target.closest('[data-i]'); if(!t) return; sel=+t.dataset.i; $('city').value=sel; tick(); });
  let rt; addEventListener('resize',()=>{ clearTimeout(rt); rt=setTimeout(draw,200); });
  tick(); setInterval(tick, 15000); bindShare();
})();""")

# ============================================================
# 3 今日の服装指数  KW: 今日の服装 78k/KD0
# ============================================================
sim(slug="kyou-fukusou", cat="beauty", emoji="🧥", score=67,
    title="今日の服装指数（気温から何を着る？）",
    card_desc="今日・明日の予想気温から「半袖？上着？コート？」を判定。朝昼夜の寒暖差と雨・風も考慮。都道府県別。",
    title_tag="今日の服装指数｜気温から「何を着る？」を判定（都道府県別・明日の服装も）",
    meta_desc="今日は半袖？上着はいる？都道府県を選ぶと今日と明日の予想気温・風・降水確率から服装の目安（服装指数）を判定する無料ツール。朝昼夜の寒暖差、羽織りの要否、傘の要否まで。気温別の服装早見表つき。",
    og_title="今日の服装指数｜気温から何を着る？", og_desc="今日・明日の予想気温から服装を判定。朝昼夜の寒暖差も。",
    lead="今日、何を着ればいい？ お住まいの都道府県を選ぶと、今日と明日の予想気温・風・雨から<b>服装の目安</b>を判定します。朝と夜の寒暖差が大きい日は「羽織りを一枚」もお知らせ。",
    about_h2="気温別の服装 早見表",
    about="""<div class="tbl-scroll"><table class="seo-table"><tr><th>最高気温</th><th>服装の目安</th></tr>
    <tr><td>30℃以上</td><td>半袖・薄手。日差し対策と水分補給を</td></tr>
    <tr><td>25〜29℃</td><td>半袖。屋内の冷房用に薄い羽織りがあると安心</td></tr>
    <tr><td>20〜24℃</td><td>長袖シャツ・薄手カーディガン</td></tr>
    <tr><td>15〜19℃</td><td>薄手のジャケット・パーカー・ニット</td></tr>
    <tr><td>10〜14℃</td><td>ジャケット＋セーター、薄手コート</td></tr>
    <tr><td>5〜9℃</td><td>コート・マフラー</td></tr>
    <tr><td>5℃未満</td><td>厚手コート・ダウン・手袋</td></tr></table></div>
    <p>服装選びで最高気温と同じくらい大事なのが<b>朝晩との寒暖差</b>です。日中25℃でも朝が15℃なら、脱ぎ着できる羽織りが正解。また風速が強い日は体感温度が数℃下がり、雨の日は湿気で暑さ・寒さが増して感じられます。本ツールはそれらを加味して判定しています。</p>
    <h2>判定の仕組み</h2>
    <p>Open-Meteo（気象データAPI）の予報から、その日の最高・最低気温、朝（7時）・昼（13時）・夜（19時）の気温、最大風速、降水確率を取得し、最高気温で基本の服装レベルを決めたうえで「寒暖差8℃以上」「風速8m/s以上」「降水確率50%以上」で補正しています。予報は更新されるため、出かける直前に見直すのがおすすめです。</p>
    <p>暑さ・寒さの体感は<a href="../taikan-ondo/">体感温度 計算</a>、雨の判断は<a href="../kasa-iru/">今日、傘いる？</a>もどうぞ。</p>""",
    faqs=[("気温何度から上着がいる？", "目安は最高気温20℃を下回ったら長袖、15℃を下回ったら上着（ジャケット）です。ただし風が強い日・朝晩の冷え込みでは一段暖かめが正解です。"),
          ("子どもや高齢者は同じでいい？", "子どもは体温が高く動き回るため大人より一枚薄め、高齢者は体温調節が苦手なため一枚厚めが目安です。"),
          ("明日の服装も見られる？", "「明日」タブで翌日の予報に切り替わります。予報は日々更新されるので当日朝の再確認をおすすめします。"),
          ("入力データは送信される？", "都道府県の緯度経度が気象データAPIに送られるだけで、個人情報は送信しません。現在地を使う場合も位置情報は端末内で処理されます。")],
    rel=[("kasa-iru","☂️","今日、傘いる？"),("taikan-ondo","🌡️","体感温度 計算"),("kion-kandansa","🥶","寒暖差疲労チェッカー"),("sentaku-kawaku","👕","洗濯物 乾く時間メーター")],
    body="""  <section class="panel">
    <h2>🧥 場所と日を選ぶ</h2>
    <div class="row"><div class="field"><label>都道府県</label><select id="pref"></select></div>
    <div class="field"><label>いつ？</label><div style="display:flex;gap:8px;"><button class="chip is-on" data-day="0" type="button">今日</button><button class="chip" data-day="1" type="button">明日</button></div></div></div>
    <button class="btn btn-ghost" id="geoBtn" type="button" style="width:100%;">📍 現在地を使う</button>
    <div class="hint" id="state" style="margin-top:8px;"></div>
  </section>
  <section class="panel" id="resultPanel">
    <div class="result">
      <div class="label"><span id="whereLbl">東京都</span>・<span id="dayLbl">今日</span>の服装</div>
      <div class="big" style="font-size:min(9vw,38px);line-height:1.3;"><span id="big">—</span></div>
      <div class="sub" id="sub">予報を取得中…</div>
      <canvas id="cv" style="width:100%;height:auto;display:block;margin-top:14px;background:#fdfcf8;border:1px solid var(--line);border-radius:8px;"></canvas>
      <div class="statline"><div class="stat"><div class="k">最高／最低</div><div class="v" id="temps">—</div></div>
      <div class="stat"><div class="k">降水確率</div><div class="v accent" id="rain">—</div></div>
      <div class="stat"><div class="k">最大風速</div><div class="v" id="wind">—</div></div></div>
      <div class="alert good" id="advice" style="margin-top:14px;">—</div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js=r"""(() => {
@@JS_COMMON@@
@@FIT_JS@@
@@PREFS_JS@@
@@GEO_JS@@
  let day=0, data=null, where='東京都';
  const LV=[[30,'半袖・薄手'],[25,'半袖'],[20,'長袖シャツ・薄手カーディガン'],[15,'薄手のジャケット・パーカー'],[10,'ジャケット＋セーター'],[5,'コート・マフラー'],[-99,'厚手コート・ダウン・手袋']];
  function level(t){ for(let i=0;i<LV.length;i++) if(t>=LV[i][0]) return i; return LV.length-1; }
  async function load(lat,lon,name){
    where=name; $('whereLbl').textContent=name; $('sub').textContent='予報を取得中…';
    try{
      const r=await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max,weather_code&hourly=temperature_2m&timezone=Asia%2FTokyo&forecast_days=2`);
      data=await r.json(); render();
    }catch(e){ $('sub').textContent='⚠️ 予報を取得できませんでした。時間をおいて再度お試しください。'; }
  }
  function render(){
    if(!data) return;
    const d=data.daily, hi=d.temperature_2m_max[day], lo=d.temperature_2m_min[day], rain=d.precipitation_probability_max[day]??0, wind=d.wind_speed_10m_max[day];
    const h=data.hourly.temperature_2m, base=day*24;
    const t7=h[base+7], t13=h[base+13], t19=h[base+19];
    let lv=level(Math.round(hi)); const tips=[];
    if(wind>=8){ lv=Math.min(LV.length-1, lv+1); tips.push('風が強く体感は一段寒め'); }
    if(hi-lo>=8) tips.push('朝晩との寒暖差'+(hi-lo).toFixed(0)+'℃。脱ぎ着できる羽織りを一枚');
    if(rain>=50) tips.push('降水確率'+rain+'%。傘と濡れてもいい靴を');
    if(hi>=30) tips.push('日差し対策と水分補給を');
    $('big').textContent=LV[lv][1];
    $('dayLbl').textContent= day? '明日':'今日';
    $('sub').textContent=`朝${Math.round(t7)}℃ → 昼${Math.round(t13)}℃ → 夜${Math.round(t19)}℃（${d.time[day].replace(/-/g,'/')}の予報）`;
    $('temps').textContent=Math.round(hi)+'℃ / '+Math.round(lo)+'℃';
    $('rain').textContent=rain+'%'; $('wind').textContent=wind.toFixed(0)+' m/s';
    $('advice').textContent= tips.length ? '💡 '+tips.join('。')+'。' : '💡 一日を通して服装の切り替えは少なくてOK。';
    draw(lv, t7, t13, t19, rain>=50, hi>=30);
    SHARE=`${where}の${day?'明日':'今日'}の服装は「${LV[lv][1]}」🧥 朝${Math.round(t7)}℃/昼${Math.round(t13)}℃/夜${Math.round(t19)}℃。あなたの街は？👇`;
  }
  function draw(lv,t7,t13,t19,rain,hot){
    const cv=$('cv'); const {x,W,H}=fitCanvas(cv,0.5);
    x.fillStyle='#fdfcf8'; x.fillRect(0,0,W,H);
    // 朝昼夜の気温ストリップ（左）
    const cols=[['朝 7時',t7,'#9ec5d9'],['昼 13時',t13,'#f2c14e'],['夜 19時',t19,'#5d6d8a']];
    const sw=W*0.5, bx=24, bw=(sw-48)/3, base=H-34, maxT=Math.max(35,...cols.map(c=>c[1])), minT=Math.min(0,...cols.map(c=>c[1]));
    cols.forEach((c,i)=>{ const hgt=(c[1]-minT)/(maxT-minT)*(H-90); const X=bx+i*bw+bw*0.2;
      x.fillStyle=c[2]; x.fillRect(X, base-hgt, bw*0.6, hgt);
      x.fillStyle='#14181d'; x.font='700 15px system-ui,sans-serif'; x.textAlign='center'; x.fillText(Math.round(c[1])+'℃', X+bw*0.3, base-hgt-8);
      x.fillStyle='#59616c'; x.font='11px system-ui,sans-serif'; x.fillText(c[0], X+bw*0.3, base+18); });
    // 人物（右）
    const cx=W*0.75, top=22, scale=Math.min(1,(H-40)/240);
    x.save(); x.translate(cx, top); x.scale(scale,scale);
    const coat=lv>=4, longSleeve=lv>=2, scarf=lv>=5, gloves=lv>=6;
    const palette=['#e5735f','#e9a23b','#7fae6c','#4f8fc0','#3b5f8a','#4a3f70','#2d3140'][lv];
    // 頭
    x.fillStyle='#f1d3b8'; x.beginPath(); x.arc(0,30,22,0,6.283); x.fill();
    x.fillStyle='#3b2f2a'; x.beginPath(); x.arc(0,24,22,Math.PI,2*Math.PI); x.fill();
    // 胴体（服）
    const bodyW = coat? 78 : 62, bodyH = coat? 118 : 96;
    x.fillStyle=palette; roundRect(x,-bodyW/2,56,bodyW,bodyH,14); x.fill();
    // 袖
    const sl = longSleeve? 78 : 34;
    x.fillStyle=palette; roundRect(x,-bodyW/2-22,60,22,sl,10); x.fill(); roundRect(x,bodyW/2,60,22,sl,10); x.fill();
    if(!longSleeve){ x.fillStyle='#f1d3b8'; roundRect(x,-bodyW/2-20,94,18,44,9); x.fill(); roundRect(x,bodyW/2+2,94,18,44,9); x.fill(); }
    if(gloves){ x.fillStyle='#8a3b2f'; roundRect(x,-bodyW/2-22,132,22,18,8); x.fill(); roundRect(x,bodyW/2,132,22,18,8); x.fill(); }
    // コートのボタン列
    if(coat){ x.fillStyle='rgba(0,0,0,.25)'; for(let k=0;k<4;k++){ x.beginPath(); x.arc(0,80+k*22,3,0,6.283); x.fill(); } }
    // マフラー
    if(scarf){ x.fillStyle='#c4442b'; roundRect(x,-30,48,60,16,8); x.fill(); roundRect(x,8,58,14,46,6); x.fill(); }
    // 脚
    x.fillStyle= lv>=3? '#2f3a4a' : '#6b7d8f'; roundRect(x,-26,56+bodyH-6,22,58,8); x.fill(); roundRect(x,4,56+bodyH-6,22,58,8); x.fill();
    // 傘 / 太陽
    if(rain){ x.strokeStyle='#1b4a63'; x.lineWidth=3; x.beginPath(); x.moveTo(-72,130); x.lineTo(-72,60); x.stroke(); x.fillStyle='#2c6b86'; x.beginPath(); x.arc(-72,60,40,Math.PI,2*Math.PI); x.fill(); }
    if(hot&&!rain){ x.fillStyle='#f4c542'; x.beginPath(); x.arc(-84,26,18,0,6.283); x.fill(); x.strokeStyle='#f4c542'; x.lineWidth=3; for(let k=0;k<8;k++){ const a=k*Math.PI/4; x.beginPath(); x.moveTo(-84+Math.cos(a)*24,26+Math.sin(a)*24); x.lineTo(-84+Math.cos(a)*32,26+Math.sin(a)*32); x.stroke(); } }
    x.restore();
    function roundRect(c,X,Y,w,h,r){ c.beginPath(); c.moveTo(X+r,Y); c.arcTo(X+w,Y,X+w,Y+h,r); c.arcTo(X+w,Y+h,X,Y+h,r); c.arcTo(X,Y+h,X,Y,r); c.arcTo(X,Y,X+w,Y,r); c.closePath(); }
  }
  const go=()=>{ const p=PREFS[+$('pref').value]; load(p[1],p[2],p[0].replace(/\(.*\)/,'')); };
  $('pref').addEventListener('change',go);
  document.querySelectorAll('[data-day]').forEach(b=>b.addEventListener('click',()=>{ document.querySelectorAll('[data-day]').forEach(c=>c.classList.remove('is-on')); b.classList.add('is-on'); day=+b.dataset.day; render(); }));
  $('geoBtn').addEventListener('click',()=>useGeo(load));
  let rt; addEventListener('resize',()=>{ clearTimeout(rt); rt=setTimeout(render,200); });
  go(); bindShare();
})();""")

# ============================================================
# 4 今日の月（月齢・満ち欠け・次の満月）  KW: 今日の月 53k/KD0
# ============================================================
sim(slug="kyou-no-tsuki", cat="wonder", emoji="🌙", score=68,
    title="今日の月（月齢・満ち欠け・次の満月はいつ？）",
    card_desc="今夜の月はどんな形？月齢・輝面比・月の名前と、次の満月・新月の日付を計算。30日分の満ち欠けも。",
    title_tag="今日の月｜月齢・満ち欠け・月の名前と、次の満月・新月はいつ？（30日カレンダー）",
    meta_desc="今日の月齢は？今夜の月の形と輝面比、十三夜・十六夜などの月の名前、見えやすい時間帯、次の満月・新月の日付を計算する無料ツール。日付を変えれば過去・未来の月も。30日分の満ち欠けカレンダーつき。",
    og_title="今日の月｜月齢と次の満月はいつ？", og_desc="今夜の月の形・月齢・名前と、次の満月・新月を計算。",
    lead="今夜の月は、どんな形？ 今日の<b>月齢と満ち欠け</b>を描き、月の名前・見えやすい時間帯・<b>次の満月と新月の日付</b>を表示します。日付を変えれば、誕生日の月や旅行の日の月も分かります。",
    about_h2="月齢と月の名前",
    about="""<p><b>月齢</b>は新月からの経過日数で、約29.5日でひとまわりします。月齢0が新月、約7.4で上弦（右半分が光る半月）、約14.8で満月、約22.1で下弦（左半分が光る半月）。日本には満月前後の月にひとつずつ名前があり、「十三夜」「十五夜」「十六夜（いざよい）」「立待月」「居待月」「寝待月」…と、月の出が日ごとに遅くなる様子を待ちかたで表現した風流な呼び名です。</p>
    <div class="tbl-scroll"><table class="seo-table"><tr><th>月齢の目安</th><th>名前</th><th>見えやすい時間</th></tr>
    <tr><td>0</td><td>新月（朔）</td><td>見えない</td></tr>
    <tr><td>2〜3</td><td>三日月</td><td>夕方の西の空</td></tr>
    <tr><td>7〜8</td><td>上弦の月</td><td>夕方〜夜半（南の空）</td></tr>
    <tr><td>12〜13</td><td>十三夜</td><td>夕方〜深夜</td></tr>
    <tr><td>14〜15</td><td>満月（十五夜）</td><td>一晩中</td></tr>
    <tr><td>15〜16</td><td>十六夜（いざよい）</td><td>夜〜明け方</td></tr>
    <tr><td>16〜19</td><td>立待月・居待月・寝待月</td><td>夜遅く〜明け方</td></tr>
    <tr><td>22〜23</td><td>下弦の月</td><td>深夜〜午前中</td></tr>
    <tr><td>26〜27</td><td>二十六夜・有明月</td><td>明け方の東の空</td></tr></table></div>
    <h2>計算の仕組み</h2>
    <p>基準となる新月の時刻（2000年1月6日18時14分 UTC）からの経過時間を朔望月（29.530589日）で割った余りで月齢を求め、月齢から輝面比（光っている割合）を計算しています。実際の月の満ち欠けは楕円軌道の影響で±0.5日ほど前後するため、正確な満月の瞬間は国立天文台の暦をご確認ください。</p>
    <p>今夜の星の見えやすさは<a href="../hoshizora-shisu/">今夜の星空指数</a>、日の出・日の入りは<a href="../hiruma-nagasa/">昼の長さメーター</a>でどうぞ。</p>""",
    faqs=[("次の満月はいつ？", "今日の月齢から計算した「次の満月」を結果に表示しています。満月は約29.5日ごとに巡ってきます。"),
          ("月齢と輝面比の違いは？", "月齢は新月からの日数、輝面比は月の円盤のうち光っている割合（%）です。上弦・下弦で約50%、満月で100%です。"),
          ("南半球では形が逆？", "はい。南半球では月を逆さに見上げる形になるため、光っている側が左右逆に見えます。本ツールは日本（北半球）基準です。"),
          ("入力データは送信される？", "日付の計算はすべてブラウザ内で行い、外部には何も送信しません。")],
    rel=[("hoshizora-shisu","🌌","今夜の星空指数"),("hiruma-nagasa","🌅","昼の長さメーター"),("shio-live","🌊","今日の潮"),("galaxy-collision","🌌","銀河衝突シミュレーター")],
    body="""  <section class="panel" id="resultPanel">
    <div class="result">
      <div class="label"><span id="dLbl">今日</span>の月は</div>
      <canvas id="cv" style="width:100%;height:auto;display:block;background:#0a0f1e;border:1px solid var(--line);border-radius:8px;"></canvas>
      <div class="big" style="font-size:min(9vw,36px);margin-top:12px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">月齢</div><div class="v accent" id="age">—</div></div>
      <div class="stat"><div class="k">輝面比</div><div class="v" id="illum">—</div></div>
      <div class="stat"><div class="k">次の満月</div><div class="v" id="nextFull">—</div></div>
      <div class="stat"><div class="k">次の新月</div><div class="v" id="nextNew">—</div></div></div>
      <div class="field" style="margin:14px 0 0;text-align:left;"><label>日付を変える</label><input type="date" id="dt"></div>
      <canvas id="strip" style="width:100%;height:auto;display:block;margin-top:12px;background:#0a0f1e;border:1px solid var(--line);border-radius:8px;"></canvas>
      <p style="font-size:11.5px;color:var(--ink-3);margin:6px 0 0;">この日から30日分の満ち欠け（左が選んだ日）。</p>
@@SHARE_ROW@@
    </div>
  </section>""",
    js=r"""(() => {
@@JS_COMMON@@
@@FIT_JS@@
  const SYN=29.530588853, EPOCH=Date.UTC(2000,0,6,18,14);
  const age = d => { let a=((d.getTime()-EPOCH)/86400000)%SYN; if(a<0)a+=SYN; return a; };
  const illum = a => (1-Math.cos(2*Math.PI*a/SYN))/2;
  function name(a){ if(a<1||a>=28.8)return['新月','ほぼ見えません']; if(a<2)return['繊月（二日月）','日没直後の西の空に細く']; if(a<4)return['三日月','夕方の西の空']; if(a<6.5)return['上弦前の月','夕方〜夜'];
    if(a<8.5)return['上弦の月','夕方〜夜半、南の空']; if(a<12)return['十日夜ごろの月','夕方〜深夜']; if(a<13.5)return['十三夜','夕方〜深夜']; if(a<14.3)return['小望月（十四日月）','夕方〜明け方'];
    if(a<15.5)return['満月（十五夜）','一晩中']; if(a<16.5)return['十六夜（いざよい）','夜〜明け方']; if(a<17.5)return['立待月','夜〜明け方']; if(a<18.5)return['居待月','夜遅く〜明け方'];
    if(a<19.5)return['寝待月','深夜〜明け方']; if(a<21)return['更待月','深夜〜午前']; if(a<23.5)return['下弦の月','深夜〜午前中、南の空']; if(a<26)return['有明月','明け方〜午前'];
    return['二十六夜（明けの三日月）','明け方の東の空']; }
  function moon(x,cx,cy,R,a,detail){
    const p=a/SYN, s=Math.cos(2*Math.PI*p);
    x.save(); x.beginPath(); x.arc(cx,cy,R,0,6.283); x.clip();
    x.fillStyle='#1c2236'; x.fillRect(cx-R,cy-R,2*R,2*R);                      // 影の面
    const lit='#e9e4d2', dark='#1c2236';
    if(p<0.5){ x.fillStyle=lit; x.fillRect(cx,cy-R,R,2*R); x.fillStyle= s>0? dark: lit; }
    else     { x.fillStyle=lit; x.fillRect(cx-R,cy-R,R,2*R); x.fillStyle= s<0? lit: dark; }
    x.beginPath(); x.ellipse(cx,cy,Math.max(0.01,R*Math.abs(s)),R,0,0,6.283); x.fill();
    if(detail){ x.fillStyle='rgba(120,116,100,.28)';                              // クレーター
      [[-.35,-.25,.16],[.22,-.38,.1],[.35,.2,.2],[-.15,.42,.12],[-.5,.3,.09],[.05,.05,.07]].forEach(c=>{ x.beginPath(); x.arc(cx+c[0]*R,cy+c[1]*R,c[2]*R,0,6.283); x.fill(); }); }
    x.restore();
    if(detail){ x.strokeStyle='rgba(233,228,210,.25)'; x.lineWidth=1; x.beginPath(); x.arc(cx,cy,R+0.5,0,6.283); x.stroke(); }
  }
  function stars(x,W,H,n){ x.fillStyle='#fff'; for(let i=0;i<n;i++){ const sx=(i*97%W), sy=(i*53%H); x.globalAlpha=0.25+((i*31)%60)/100; x.fillRect(sx,sy,1.2,1.2); } x.globalAlpha=1; }
  let cur=new Date();
  function render(){
    const a=age(cur), k=illum(a), nm=name(a);
    const {x,W,H}=fitCanvas($('cv'),0.5); x.fillStyle='#0a0f1e'; x.fillRect(0,0,W,H); stars(x,W,H,90);
    const R=Math.min(H*0.38, 110), cx=W/2, cy=H/2;
    x.shadowColor='rgba(233,228,210,.45)'; x.shadowBlur=k*40; moon(x,cx,cy,R,a,true); x.shadowBlur=0;
    $('big').textContent=nm[0];
    $('dLbl').textContent= ymd(cur)===ymd(new Date()) ? '今日' : jaDate(cur);
    $('sub').textContent='見えやすい時間：'+nm[1]+(a<SYN/2?'　（満ちていく月）':'　（欠けていく月）');
    $('age').textContent=a.toFixed(1); $('illum').textContent=Math.round(k*100)+'%';
    const toFull = a<=SYN/2 ? SYN/2-a : SYN*1.5-a, toNew = SYN-a;
    const f=new Date(cur.getTime()+toFull*86400000), n=new Date(cur.getTime()+toNew*86400000);
    $('nextFull').innerHTML=(f.getMonth()+1)+'/'+f.getDate()+'<small style="font-size:12px;font-weight:600;color:var(--ink-3);margin-left:4px;">'+Math.ceil(toFull)+'日後</small>';
    $('nextNew').innerHTML=(n.getMonth()+1)+'/'+n.getDate()+'<small style="font-size:12px;font-weight:600;color:var(--ink-3);margin-left:4px;">'+Math.ceil(toNew)+'日後</small>';
    // 30日ストリップ
    const sc=$('strip'); const S=fitCanvas(sc,0.19); const sx=S.x; sx.fillStyle='#0a0f1e'; sx.fillRect(0,0,S.W,S.H);
    const cols=15, rows=2, cw=S.W/cols, rr=Math.min(cw*0.32, S.H/rows*0.3);
    for(let i=0;i<30;i++){ const d=new Date(cur.getTime()+i*86400000), aa=age(d); const ccx=(i%cols)*cw+cw/2, ccy=Math.floor(i/cols)*(S.H/rows)+S.H/rows*0.42;
      moon(sx,ccx,ccy,rr,aa,false); sx.fillStyle= (aa>=14&&aa<15.6)?'#f4c542':'rgba(233,228,210,.6)'; sx.font='10px system-ui,sans-serif'; sx.textAlign='center'; sx.fillText((d.getMonth()+1)+'/'+d.getDate(), ccx, ccy+rr+12); }
    SHARE=`今日の月は「${nm[0]}」🌙 月齢${a.toFixed(1)}・輝面比${Math.round(k*100)}%。次の満月は${f.getMonth()+1}/${f.getDate()}。今夜の月を見上げてみて👇`;
  }
  $('dt').value=ymd(cur);
  $('dt').addEventListener('change',()=>{ const v=$('dt').value; if(v){ cur=new Date(v+'T21:00:00'); render(); } });
  let rt; addEventListener('resize',()=>{ clearTimeout(rt); rt=setTimeout(render,200); });
  render(); bindShare();
})();""")

# ============================================================
# 5 18金 相場 1g 今日（金・銀・プラチナ）  KW: 18金 相場 1g 今日 122k+31k/KD0
# ============================================================
sim(slug="kin-souba", cat="money", emoji="🥇", score=68,
    title="18金 相場 1g 今日（金・プラチナ・銀の価格）",
    card_desc="今日の金1gはいくら？国際スポット価格と為替からK24・K22・K18・K14・プラチナ・銀の1g価格をライブ換算。手持ちの金の価値も。",
    title_tag="18金 相場 1g 今日｜金・プラチナ・銀の価格をライブ換算（K24・K22・K18・K14）",
    meta_desc="今日の18金（K18）は1gいくら？国際スポット価格（ドル/オンス）と為替レートから、K24・K22・K18・K14・K10とプラチナ・銀の1gあたり円価格をライブで換算する無料ツール。手持ちの金製品の重さから概算価値も計算。",
    og_title="18金 相場 1g 今日｜金・プラチナ・銀の価格", og_desc="国際スポット価格×為替で純度別の1g価格をライブ換算。",
    lead="今日、金は1gいくら？ 国際スポット価格（ドル建て/トロイオンス）と為替レートを取得して、<b>K24・K22・K18・K14と、プラチナ・銀の1gあたり円価格</b>を換算します。手持ちのアクセサリーの重さを入れれば、概算の価値も分かります。",
    about_h2="18金（K18）の価格はこう決まる",
    about="""<p>金の国際価格は「1トロイオンス（31.1035g）あたり何ドルか」で取引されます。これを<b>÷31.1035×ドル円レート</b>で1gあたりの円に直し、純度をかけたものが各カラットの目安です。K24は純度99.9%（≒1.0）、K22は91.7%、<b>K18は75%</b>、K14は58.5%、K10は41.7%。つまりK18の1g価格は、純金1g価格のおよそ4分の3です。</p>
    <div class="tbl-scroll"><table class="seo-table"><tr><th>刻印</th><th>金の含有率</th><th>主な用途</th></tr>
    <tr><td>K24（純金）</td><td>99.9%</td><td>インゴット・地金・コイン</td></tr>
    <tr><td>K22</td><td>91.7%</td><td>海外製ジュエリー・コイン</td></tr>
    <tr><td>K18</td><td>75.0%</td><td>指輪・ネックレスの主流</td></tr>
    <tr><td>K14</td><td>58.5%</td><td>硬めのジュエリー</td></tr>
    <tr><td>K10</td><td>41.7%</td><td>手頃な価格帯のジュエリー</td></tr>
    <tr><td>Pt1000／Pt900／Pt850</td><td>プラチナ 100／90／85%</td><td>結婚指輪など</td></tr></table></div>
    <h2>買取価格は「相場より数%低い」が普通</h2>
    <p>本ツールの価格は<b>国際市場の相場を円換算した理論値（税抜）</b>です。実際に貴金属店で売るときは、店舗の買取手数料・精錬コストが差し引かれ、相場の85〜95%程度になるのが一般的。逆に買うときは消費税と販売手数料が上乗せされます。石付きジュエリーは金属部分の重さだけが対象で、宝石は別査定です。複数店で見積もりを取ると数千円単位で差が出ることも珍しくありません。</p>
    <div class="note">価格は取得時点の国際スポット価格（gold-api.com）と欧州中央銀行公表の為替レートによる目安で、国内小売・買取価格そのものではありません。売買の判断は各社の当日公表価格でご確認ください。</div>
    <p>為替の推移は<a href="../dollar-yen-chart/">ドル円 為替チャート</a>、暗号資産は<a href="../crypto-zenbu/">暗号資産ぜんぶ</a>もどうぞ。</p>""",
    faqs=[("18金1gの相場はいくら？", "本ツールで表示している「K18 1g」が今日の目安です。純金（K24）1g価格の75%が計算上の基準になります。"),
          ("表示価格で売れる？", "いいえ。買取店は手数料を差し引くため、相場の85〜95%程度が一般的です。複数店で査定を比べるのがおすすめです。"),
          ("なぜ金の価格は上がっている？", "インフレや地政学リスクの高まりで「安全資産」として買われる局面が続いたためです。ただし相場は日々変動します。"),
          ("入力データは送信される？", "重さの入力はブラウザ内で計算され、外部には送信されません。価格APIと為替APIへの問い合わせだけを行います。")],
    rel=[("dollar-yen-chart","💱","ドル円 為替チャート"),("crypto-zenbu","🪙","暗号資産ぜんぶ"),("btc-tara","₿","もしビットコイン買ってたら"),("enyasu-taikan","📉","円安体感メーター")],
    body="""  <section class="panel" id="resultPanel">
    <div class="result">
      <div class="label">今日の <b>K18（18金）</b> 1gの目安</div>
      <div class="big"><span id="big">—</span><span class="unit">円/g</span></div>
      <div class="sub" id="sub">価格を取得中…</div>
      <canvas id="cv" style="width:100%;height:auto;display:block;margin-top:14px;background:#1a1712;border:1px solid var(--line);border-radius:8px;"></canvas>
      <div class="statline"><div class="stat"><div class="k">純金 K24</div><div class="v accent" id="k24">—</div></div>
      <div class="stat"><div class="k">プラチナ Pt1000</div><div class="v" id="pt">—</div></div>
      <div class="stat"><div class="k">銀</div><div class="v" id="ag">—</div></div>
      <div class="stat"><div class="k">ドル円</div><div class="v" id="fx">—</div></div></div>
      <div class="tbl-scroll" style="margin-top:14px;"><table class="seo-table" id="tbl"><tr><th>純度</th><th>1gの目安</th><th>買取目安（相場の90%）</th></tr></table></div>
      <div class="row" style="margin-top:14px;text-align:left;">
        <div class="field" style="margin-bottom:0;"><label>手持ちの金製品の重さ <span class="hint">（g）</span></label><input type="number" id="g" value="10" min="0" step="0.1" inputmode="decimal"></div>
        <div class="field" style="margin-bottom:0;"><label>純度</label><select id="pur"><option value="0.999">K24</option><option value="0.917">K22</option><option value="0.75" selected>K18</option><option value="0.585">K14</option><option value="0.417">K10</option><option value="pt">Pt900（プラチナ）</option></select></div>
      </div>
      <div class="alert good" id="worth" style="margin-top:12px;">—</div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js=r"""(() => {
@@JS_COMMON@@
@@FIT_JS@@
  const OZ=31.1035; let gJ=0, ptJ=0, agJ=0, fx=0;
  const PUR=[['K24',0.999],['K22',0.917],['K18',0.75],['K14',0.585],['K10',0.417]];
  async function load(){
    $('sub').textContent='価格を取得中…';
    try{
      const opt = u => fetch(u).then(r=>r.json()).catch(()=>({price:0}));   // 白金・銀は取れなくても金は出す
      const [xau,xpt,xag,f]=await Promise.all([
        fetch('https://api.gold-api.com/price/XAU').then(r=>r.json()),
        opt('https://api.gold-api.com/price/XPT'),
        opt('https://api.gold-api.com/price/XAG'),
        fetch('https://api.frankfurter.dev/v1/latest?base=USD&symbols=JPY').then(r=>r.json())]);
      fx=f.rates.JPY; gJ=xau.price/OZ*fx; ptJ=xpt.price/OZ*fx; agJ=xag.price/OZ*fx;
      $('big').textContent=Math.round(gJ*0.75).toLocaleString('ja-JP');
      const t=new Date(xau.updatedAt);
      $('sub').textContent=`金 ${Math.round(xau.price).toLocaleString('ja-JP')}ドル/oz × ドル円 ${fx.toFixed(2)}（${t.getMonth()+1}/${t.getDate()} ${pad2(t.getHours())}:${pad2(t.getMinutes())} 取得・税抜の理論値）`;
      $('k24').textContent=Math.round(gJ*0.999).toLocaleString('ja-JP')+'円'; $('pt').textContent=Math.round(ptJ).toLocaleString('ja-JP')+'円'; $('ag').textContent=agJ.toFixed(0)+'円'; $('fx').textContent=fx.toFixed(2)+'円';
      $('tbl').innerHTML='<tr><th>純度</th><th>1gの目安</th><th>買取目安（相場の90%）</th></tr>'+PUR.map(p=>`<tr><td>${p[0]}</td><td>${Math.round(gJ*p[1]).toLocaleString('ja-JP')}円</td><td>${Math.round(gJ*p[1]*0.9).toLocaleString('ja-JP')}円</td></tr>`).join('')+`<tr><td>Pt1000</td><td>${Math.round(ptJ).toLocaleString('ja-JP')}円</td><td>${Math.round(ptJ*0.9).toLocaleString('ja-JP')}円</td></tr><tr><td>Pt900</td><td>${Math.round(ptJ*0.9).toLocaleString('ja-JP')}円</td><td>${Math.round(ptJ*0.81).toLocaleString('ja-JP')}円</td></tr>`;
      draw(); worth();
      SHARE=`今日の18金（K18）相場は1g ${Math.round(gJ*0.75).toLocaleString('ja-JP')}円の目安🥇 純金は${Math.round(gJ*0.999).toLocaleString('ja-JP')}円/g。手持ちの金の価値もこちらで👇`;
    }catch(e){ $('sub').textContent='⚠️ 価格を取得できませんでした。時間をおいて再度お試しください。'; }
  }
  function worth(){ if(!gJ) return; const g=+$('g').value||0, v=$('pur').value; const per= v==='pt'? ptJ*0.9 : gJ*(+v); const val=g*per;
    $('worth').textContent=`🧾 ${g}g（${$('pur').options[$('pur').selectedIndex].text}）の相場価値は約 ${Math.round(val).toLocaleString('ja-JP')}円。買取なら約 ${Math.round(val*0.85).toLocaleString('ja-JP')}〜${Math.round(val*0.95).toLocaleString('ja-JP')}円が目安です。`; }
  function draw(){
    const cv=$('cv'); const {x,W,H}=fitCanvas(cv,0.42);
    x.fillStyle='#1a1712'; x.fillRect(0,0,W,H);
    // 純度ラダー（棒）
    const items=[...PUR.map(p=>[p[0],gJ*p[1],'#d4af37']),['Pt',ptJ,'#c9ced6'],['銀',agJ,'#b8bcc4']];
    const max=Math.max(...items.map(i=>i[1]))||1, bw=W/(items.length+1), base=H-30;
    items.forEach((it,i)=>{ const X=bw*(i+0.6), h=(it[1]/max)*(H-78);
      const g=x.createLinearGradient(X,base-h,X+bw*0.6,base); g.addColorStop(0,it[2]); g.addColorStop(0.5,'#fff1b0'); g.addColorStop(1,it[2]);
      if(it[0]==='Pt'||it[0]==='銀'){ g.addColorStop(0.5,'#f5f7fa'); }
      x.fillStyle=g; x.fillRect(X,base-h,bw*0.6,h);
      x.fillStyle='rgba(0,0,0,.25)'; x.fillRect(X,base-h,bw*0.6,3);
      x.fillStyle='#f3e7c3'; x.font='700 12px system-ui,sans-serif'; x.textAlign='center'; x.fillText(Math.round(it[1]).toLocaleString('ja-JP'), X+bw*0.3, base-h-8);
      x.fillStyle='rgba(243,231,195,.7)'; x.font='11px system-ui,sans-serif'; x.fillText(it[0], X+bw*0.3, base+16); });
    x.fillStyle='rgba(243,231,195,.55)'; x.font='11px system-ui,sans-serif'; x.textAlign='left'; x.fillText('1gあたりの目安（円）', 10, 16);
  }
  $('g').addEventListener('input',worth); $('pur').addEventListener('change',worth);
  let rt; addEventListener('resize',()=>{ clearTimeout(rt); rt=setTimeout(draw,200); });
  load(); bindShare();
})();""")

# ============================================================
# 6 祝日カレンダー（一覧・連休・あと何日）  KW: 祝日 64k / 2026年 祝日 19k / 祝日カレンダー 16k
# ============================================================
sim(slug="shukujitsu-calendar", cat="season", emoji="📅", score=67,
    title="祝日カレンダー（今年・来年の祝日一覧と連休）",
    card_desc="今年と来年の祝日を12ヶ月カレンダーと一覧で。3連休以上を自動で色分けし、次の祝日まであと何日かも。",
    title_tag="祝日カレンダー 2026・2027｜祝日一覧・3連休・次の祝日まであと何日（12ヶ月表示）",
    meta_desc="2026年・2027年の祝日をカレンダーと一覧で表示する無料ツール。土日とつながる3連休以上を自動で色分けし、次の祝日まで あと何日かをカウントダウン。振替休日も反映。11月・3月など月別の祝日もすぐ分かります。",
    og_title="祝日カレンダー｜祝日一覧と連休・次の祝日まで", og_desc="今年・来年の祝日を12ヶ月カレンダーで。3連休は色分け表示。",
    lead="今年の祝日、あと何回？ 内閣府の祝日データを取得して、<b>12ヶ月カレンダーと一覧</b>で表示します。土日とつながる<b>3連休以上は自動で色分け</b>。次の祝日までのカウントダウン付き。",
    about_h2="日本の祝日は年間16日",
    about="""<p>日本の国民の祝日は年間<b>16日</b>。祝日が日曜と重なると翌月曜が振替休日になり、祝日と祝日に挟まれた平日は「国民の休日」として休みになります。祝日が土曜と重なった場合は振替がないため、年によって「休みの日数」が変わります。</p>
    <div class="tbl-scroll"><table class="seo-table"><tr><th>月</th><th>祝日</th></tr>
    <tr><td>1月</td><td>元日（1日）・成人の日（第2月曜）</td></tr>
    <tr><td>2月</td><td>建国記念の日（11日）・天皇誕生日（23日）</td></tr>
    <tr><td>3月</td><td>春分の日（20日か21日）</td></tr>
    <tr><td>4〜5月</td><td>昭和の日（4/29）・憲法記念日（5/3）・みどりの日（5/4）・こどもの日（5/5）</td></tr>
    <tr><td>7月</td><td>海の日（第3月曜）</td></tr>
    <tr><td>8月</td><td>山の日（11日）</td></tr>
    <tr><td>9月</td><td>敬老の日（第3月曜）・秋分の日（22日か23日）</td></tr>
    <tr><td>10月</td><td>スポーツの日（第2月曜）</td></tr>
    <tr><td>11月</td><td>文化の日（3日）・勤労感謝の日（23日）</td></tr></table></div>
    <p>6月と12月には祝日がありません。「ハッピーマンデー」で月曜に固定された祝日（成人の日・海の日・敬老の日・スポーツの日）は毎年3連休になります。有休を1〜2日足して長い連休にするなら<a href="../renkyuu-maker/">9連休メーカー</a>、次の3連休までのカウントダウンは<a href="../tsugi-renkyuu/">次の3連休はいつ？</a>でどうぞ。</p>
    <div class="note">祝日データは holidays-jp（内閣府公表データを機械可読化したもの）から取得しています。来年分は公表後に反映されます。</div>""",
    faqs=[("今年の祝日は何日ある？", "国民の祝日は年16日です。振替休日が発生する年はその分だけ休みが増えます。カレンダー上部に今年の祝日数を表示しています。"),
          ("振替休日はどういうとき？", "祝日が日曜と重なったとき、その直後の平日が振替休日になります。土曜と重なった場合は振替はありません。"),
          ("来年の祝日はいつ分かる？", "春分の日・秋分の日は前年2月に官報で公示されます。それ以外は法律で日付が決まっているため先に分かります。"),
          ("入力データは送信される？", "このページは何も入力せずに使え、外部にデータは送信しません。")],
    rel=[("tsugi-renkyuu","🗓️","次の3連休はいつ？"),("renkyuu-maker","🏖️","9連休メーカー"),("obon-itsu","🏮","お盆はいつ？"),("kaigai-shukujitsu","🌏","海外の祝日カレンダー")],
    body="""  <section class="panel" id="resultPanel">
    <div class="result">
      <div class="label">次の祝日 <span id="nextName">—</span> まで</div>
      <div class="big"><span id="big">—</span><span class="unit">日</span></div>
      <div class="sub" id="sub">祝日データを取得中…</div>
      <div class="statline"><div class="stat"><div class="k"><span id="yLbl">今年</span>の祝日</div><div class="v accent" id="cnt">—</div></div>
      <div class="stat"><div class="k">3連休以上</div><div class="v" id="renkyu">—</div></div>
      <div class="stat"><div class="k">最長の連休</div><div class="v" id="longest">—</div></div></div>
      <div style="display:flex;gap:8px;justify-content:center;margin-top:14px;" id="years"></div>
      <div id="cal" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;margin-top:14px;text-align:left;"></div>
      <div class="tbl-scroll" style="margin-top:14px;"><table class="seo-table" id="list"><tr><th>日付</th><th>祝日</th><th>連休</th></tr></table></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js=r"""(() => {
@@JS_COMMON@@
@@FIT_JS@@
  let H={}, year=new Date().getFullYear();
  const isOff = (d) => d.getDay()===0||d.getDay()===6||!!H[ymd(d)];
  function runLen(d){ // その日を含む連続休みの長さ
    let a=new Date(d), b=new Date(d);
    while(true){ const p=new Date(a.getTime()-86400000); if(isOff(p)) a=p; else break; }
    while(true){ const n=new Date(b.getTime()+86400000); if(isOff(n)) b=n; else break; }
    return {len:Math.round((b-a)/86400000)+1, a, b};
  }
  async function load(){
    try{ const r=await fetch('https://holidays-jp.github.io/api/v1/date.json'); H=await r.json(); }
    catch(e){ $('sub').textContent='⚠️ 祝日データを取得できませんでした。'; return; }
    const ys=[...new Set(Object.keys(H).map(k=>+k.slice(0,4)))].filter(y=>y>=year-1&&y<=year+2).sort();
    $('years').innerHTML=ys.map(y=>`<button class="chip${y===year?' is-on':''}" data-y="${y}" type="button">${y}年</button>`).join('');
    document.querySelectorAll('[data-y]').forEach(b=>b.addEventListener('click',()=>{ year=+b.dataset.y; document.querySelectorAll('[data-y]').forEach(c=>c.classList.remove('is-on')); b.classList.add('is-on'); render(); }));
    render();
  }
  function render(){
    const today=new Date(); today.setHours(0,0,0,0);
    const list=Object.keys(H).filter(k=>k.startsWith(year+'-')).sort();
    const next=Object.keys(H).sort().find(k=>new Date(k+'T00:00:00')>=today);
    if(next){ const nd=new Date(next+'T00:00:00'); const dd=Math.round((nd-today)/86400000); $('big').textContent=dd; $('nextName').textContent='「'+H[next]+'」'+(nd.getMonth()+1)+'/'+nd.getDate();
      $('sub').textContent= dd===0 ? '今日は祝日です！' : `${jaDate(nd)}。${runLen(nd).len>=3? runLen(nd).len+'連休になります':'土日とはつながりません'}`; }
    $('yLbl').textContent=year+'年'; $('cnt').textContent=list.length+'日';
    // 連休（3日以上）を数える
    const seen=new Set(); let blocks=[];
    list.forEach(k=>{ const d=new Date(k+'T00:00:00'); const r=runLen(d); const key=ymd(r.a); if(r.len>=3&&!seen.has(key)){ seen.add(key); blocks.push(r); } });
    $('renkyu').textContent=blocks.length+'回'; const lg=blocks.reduce((m,b)=>Math.max(m,b.len),0); $('longest').textContent=lg? lg+'連休':'—';
    // 12ヶ月カレンダー
    let html='';
    for(let m=0;m<12;m++){ const first=new Date(year,m,1), days=new Date(year,m+1,0).getDate();
      html+=`<div style="border:1px solid var(--line);border-radius:8px;padding:8px 10px;background:#fff;"><div style="font-weight:700;font-size:13px;margin-bottom:6px;">${m+1}月</div><div style="display:grid;grid-template-columns:repeat(7,1fr);gap:2px;font-size:11px;text-align:center;">`;
      '日月火水木金土'.split('').forEach((w,i)=>html+=`<div style="color:${i===0?'#c4442b':i===6?'#1b4a63':'var(--ink-3)'};font-weight:600;">${w}</div>`);
      for(let i=0;i<first.getDay();i++) html+='<div></div>';
      for(let d=1;d<=days;d++){ const dt=new Date(year,m,d), key=ymd(dt), hol=H[key]; const r=isOff(dt)?runLen(dt):null; const inBlock=r&&r.len>=3;
        const bg= hol? '#c4442b' : inBlock? 'rgba(196,68,43,.16)' : (dt.getDay()===0? 'rgba(196,68,43,.06)': dt.getDay()===6? 'rgba(27,74,99,.07)':'transparent');
        const col= hol? '#fff' : dt.getDay()===0? '#c4442b' : dt.getDay()===6? '#1b4a63' : 'var(--ink)';
        const isT= ymd(dt)===ymd(today);
        html+=`<div title="${hol||''}" style="padding:3px 0;border-radius:4px;background:${bg};color:${col};${isT?'outline:2px solid #14181d;':''}font-variant-numeric:tabular-nums;">${d}</div>`; }
      html+='</div></div>'; }
    $('cal').innerHTML=html;
    $('list').innerHTML='<tr><th>日付</th><th>祝日</th><th>連休</th></tr>'+list.map(k=>{ const d=new Date(k+'T00:00:00'), r=runLen(d); return `<tr><td>${d.getMonth()+1}/${d.getDate()}（${'日月火水木金土'[d.getDay()]}）</td><td>${H[k]}</td><td>${r.len>=3? r.len+'連休（'+(r.a.getMonth()+1)+'/'+r.a.getDate()+'〜'+(r.b.getMonth()+1)+'/'+r.b.getDate()+'）':'—'}</td></tr>`; }).join('');
    SHARE=`${year}年の祝日は${list.length}日・3連休以上は${blocks.length}回📅 次の祝日「${next?H[next]:''}」まであと${$('big').textContent}日。祝日カレンダーはこちら👇`;
  }
  load(); bindShare();
})();""")

# ============================================================
# 7 海外の祝日カレンダー  KW: アメリカ 祝日 10k/KD0 ほか 韓国/中国/台湾…
# ============================================================
_CC = [("US","🇺🇸","アメリカ"),("KR","🇰🇷","韓国"),("CN","🇨🇳","中国"),("HK","🇭🇰","香港"),("VN","🇻🇳","ベトナム"),("SG","🇸🇬","シンガポール"),("PH","🇵🇭","フィリピン"),("ID","🇮🇩","インドネシア"),("AU","🇦🇺","オーストラリア"),("NZ","🇳🇿","ニュージーランド"),("GB","🇬🇧","イギリス"),("FR","🇫🇷","フランス"),("DE","🇩🇪","ドイツ"),("IT","🇮🇹","イタリア"),("ES","🇪🇸","スペイン"),("TR","🇹🇷","トルコ"),("CA","🇨🇦","カナダ"),("BR","🇧🇷","ブラジル"),("MX","🇲🇽","メキシコ"),("JP","🇯🇵","日本（比較用）")]
sim(slug="kaigai-shukujitsu", cat="travel", emoji="🌏", score=66,
    title="海外の祝日カレンダー（アメリカ・韓国・中国・香港…）",
    card_desc="アメリカ・韓国・中国・香港・ベトナム・イギリス…20カ国の今年の祝日一覧を1年タイムラインで。旅行・海外取引の日程確認に。",
    title_tag="海外の祝日カレンダー｜アメリカ・韓国・中国・香港・シンガポール・イギリスなど20カ国の祝日一覧（今年・来年）",
    meta_desc="アメリカ・韓国・中国・香港・ベトナム・シンガポール・フィリピン・オーストラリア・イギリス・フランス・ドイツ・イタリアなど20カ国の祝日一覧を国別に表示する無料ツール。1年タイムラインで連休の位置が一目で分かり、海外旅行や海外取引先とのやりとりの日程確認に。",
    og_title="海外の祝日カレンダー｜20カ国の祝日一覧", og_desc="アメリカ・韓国・中国・香港…各国の今年の祝日を1年タイムラインで。",
    lead="旅行先や取引先の国は、いつ休み？ 国を選ぶと<b>その国の今年・来年の祝日一覧</b>を取得し、1年のタイムラインに並べます。「今日は現地が祝日か」もひと目で。",
    about_h2="国が変われば、休みも変わる",
    about="""<p>祝日は国ごとにまったく違います。<b>アメリカ</b>は独立記念日（7/4）・感謝祭（11月第4木曜）・クリスマスが三大休暇で、正月休みは1/1のみ。<b>中国・香港・韓国・ベトナム</b>は旧正月（春節・テト）が最大の連休で、毎年日付が変わります。<b>インドネシア</b>や<b>トルコ</b>などイスラム圏は断食明け（イード）が大型連休。海外の取引先に連絡がつかない、旅行先の店が全部閉まっている——を避けるための基本情報です。</p>
    <div class="tbl-scroll"><table class="seo-table"><tr><th>国・地域</th><th>最大の連休</th><th>時期</th></tr>
    <tr><td>アメリカ</td><td>感謝祭〜クリスマス</td><td>11月下旬〜12月末</td></tr>
    <tr><td>中国</td><td>春節（旧正月）・国慶節</td><td>1〜2月・10月上旬</td></tr>
    <tr><td>韓国</td><td>ソルラル（旧正月）・秋夕</td><td>1〜2月・9〜10月</td></tr>
    <tr><td>香港</td><td>春節・イースター・国慶節</td><td>1〜2月・3〜4月・10月</td></tr>
    <tr><td>ベトナム</td><td>テト（旧正月）</td><td>1〜2月</td></tr>
    <tr><td>ヨーロッパ各国</td><td>イースター・クリスマス</td><td>3〜4月・12月末</td></tr></table></div>
    <p>旧正月など旧暦ベースの祝日は年ごとに日付が動くため、毎年の確認が必要です。渡航先の現在時刻は<a href="../sekai-jisa/">世界の時差・いま何時？</a>、日本の祝日は<a href="../shukujitsu-calendar/">祝日カレンダー</a>でどうぞ。</p>
    <div class="note">祝日データは Nager.Date（各国の公的祝日をまとめたオープンデータ）から取得しています。地域限定の祝日や臨時休日は含まれない場合があります。</div>""",
    faqs=[("アメリカの祝日は何日？", "連邦祝日は年11日（元日・キング牧師記念日・大統領の日・戦没将兵追悼記念日・ジューンティーンス・独立記念日・労働者の日・コロンブス記念日・退役軍人の日・感謝祭・クリスマス）です。"),
          ("旧正月は毎年いつ？", "旧暦の1月1日で、1月下旬〜2月中旬の間で毎年変わります。中国・台湾・韓国・ベトナムなどで最大の連休になります。"),
          ("データの出典は？", "Nager.Date（オープンな各国祝日API）です。国によっては地域限定の祝日が含まれないことがあります。"),
          ("入力データは送信される？", "国コードと年を祝日APIに問い合わせるだけで、個人情報は送信しません。")],
    rel=[("sekai-jisa","🌐","世界の時差・いま何時？"),("shukujitsu-calendar","📅","祝日カレンダー"),("sekai-yasumi","🎌","今日、世界のどこが祝日？"),("jisa-boke","✈️","時差ボケ回復シミュレーター")],
    body="""  <section class="panel" id="resultPanel">
    <div class="result">
      <div class="row" style="text-align:left;"><div class="field" style="margin-bottom:0;"><label>国・地域</label><select id="cc"></select></div>
      <div class="field" style="margin-bottom:0;"><label>年</label><div style="display:flex;gap:8px;" id="years"></div></div></div>
      <div class="label" style="margin-top:16px;"><span id="ccName">アメリカ</span>の祝日は</div>
      <div class="big"><span id="big">—</span><span class="unit">日</span></div>
      <div class="sub" id="sub">祝日データを取得中…</div>
      <canvas id="cv" style="width:100%;height:auto;display:block;margin-top:12px;background:#fff;border:1px solid var(--line);border-radius:8px;"></canvas>
      <div class="statline"><div class="stat"><div class="k">今日</div><div class="v accent" id="todayIs">—</div></div>
      <div class="stat"><div class="k">次の祝日</div><div class="v" id="next">—</div></div>
      <div class="stat"><div class="k">日本（同年）</div><div class="v" id="jp">16日</div></div></div>
      <div class="tbl-scroll" style="margin-top:14px;"><table class="seo-table" id="list"><tr><th>日付</th><th>祝日（現地名）</th><th>英語名</th></tr></table></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js=r"""(() => {
@@JS_COMMON@@
@@FIT_JS@@
  const CC=@@CC@@; let cc='US', year=new Date().getFullYear(), rows=[];
  $('cc').innerHTML=CC.map(c=>`<option value="${c[0]}">${c[1]} ${c[2]}</option>`).join('');
  $('years').innerHTML=[year,year+1].map(y=>`<button class="chip${y===year?' is-on':''}" data-y="${y}" type="button">${y}年</button>`).join('');
  async function load(){
    $('sub').textContent='祝日データを取得中…';
    try{ const r=await fetch(`https://date.nager.at/api/v3/PublicHolidays/${year}/${cc}`); if(!r.ok) throw 0; rows=await r.json(); }
    catch(e){ $('sub').textContent='⚠️ この国・年のデータを取得できませんでした。'; rows=[]; }
    render();
  }
  function render(){
    const c=CC.find(x=>x[0]===cc); $('ccName').textContent=c[2];
    const uniq=[]; const seen=new Set(); rows.forEach(r=>{ if(!seen.has(r.date)){ seen.add(r.date); uniq.push(r);} });
    $('big').textContent=uniq.length;
    const t=ymd(new Date()); const todayH=uniq.find(r=>r.date===t);
    $('todayIs').textContent= todayH? '祝日！' : '平日';
    const nx=uniq.find(r=>r.date>t); $('next').textContent= nx? nx.date.slice(5).replace('-','/')+' '+nx.localName.slice(0,10) : '—';
    $('sub').textContent= uniq.length? `${year}年・${c[2]}の公的祝日（Nager.Date）` : '';
    $('list').innerHTML='<tr><th>日付</th><th>祝日（現地名）</th><th>英語名</th></tr>'+uniq.map(r=>{ const d=new Date(r.date+'T00:00:00'); return `<tr><td>${d.getMonth()+1}/${d.getDate()}（${'日月火水木金土'[d.getDay()]}）</td><td>${r.localName}</td><td style="color:var(--ink-3);">${r.name}</td></tr>`; }).join('');
    draw(uniq);
    SHARE=`${year}年の${c[2]}の祝日は${uniq.length}日🌏 ${nx?'次は'+nx.date.slice(5).replace('-','/')+'「'+nx.localName+'」。':''}20カ国の祝日カレンダーはこちら👇`;
  }
  function draw(list){
    const cv=$('cv'); const {x,W,H}=fitCanvas(cv,0.3);
    x.fillStyle='#fff'; x.fillRect(0,0,W,H);
    const L=14,R=14,y0=H*0.55, w=W-L-R; const start=new Date(year,0,1), end=new Date(year,11,31);
    const X=d=>L+((d-start)/(end-start))*w;
    x.strokeStyle='rgba(20,24,29,.15)'; x.lineWidth=2; x.beginPath(); x.moveTo(L,y0); x.lineTo(W-R,y0); x.stroke();
    x.font='11px system-ui,sans-serif'; x.fillStyle='#8b929c'; x.textAlign='center';
    for(let m=0;m<12;m++){ const d=new Date(year,m,1); x.fillText((m+1)+'月', X(d)+w/24, y0+20); x.strokeStyle='rgba(20,24,29,.08)'; x.beginPath(); x.moveTo(X(d),y0-8); x.lineTo(X(d),y0+8); x.stroke(); }
    const today=new Date(); if(today.getFullYear()===year){ x.strokeStyle='#14181d'; x.setLineDash([3,3]); x.beginPath(); x.moveTo(X(today),y0-34); x.lineTo(X(today),y0+8); x.stroke(); x.setLineDash([]); x.fillStyle='#14181d'; x.fillText('今日', X(today), y0-38); }
    list.forEach((r,i)=>{ const d=new Date(r.date+'T00:00:00'), px=X(d); x.fillStyle='#c4442b'; x.beginPath(); x.arc(px,y0,5,0,6.283); x.fill();
      if(list.length<=16){ x.fillStyle='#14181d'; x.font='600 10px system-ui,sans-serif'; x.save(); x.translate(px, y0-12-(i%2)*11); x.textAlign='center'; x.fillText(r.localName.slice(0,7),0,0); x.restore(); } });
  }
  $('cc').addEventListener('change',()=>{ cc=$('cc').value; load(); });
  document.querySelectorAll('[data-y]').forEach(b=>b.addEventListener('click',()=>{ year=+b.dataset.y; document.querySelectorAll('[data-y]').forEach(c=>c.classList.remove('is-on')); b.classList.add('is-on'); load(); }));
  let rt; addEventListener('resize',()=>{ clearTimeout(rt); rt=setTimeout(render,200); });
  load(); bindShare();
})();""")

# ============================================================
# 8 確定申告いつまで？カウントダウン  KW: 確定申告いつまで 73k/KD0
# ============================================================
sim(slug="kakutei-shinkoku-itsu", cat="tax", emoji="🗓️", score=67,
    title="確定申告はいつまで？期限カウントダウン",
    card_desc="今年（令和8年分）の確定申告はいつからいつまで？受付開始・期限までのカウントダウンと、還付申告・消費税・贈与税の期限も。",
    title_tag="確定申告はいつまで？｜2027年（令和8年分）の期間・期限カウントダウン・還付申告は5年",
    meta_desc="確定申告はいつからいつまで？所得税の申告期間（2月16日〜3月15日・土日なら翌月曜）を自動計算し、受付開始・期限までの日数をカウントダウンする無料ツール。還付申告は5年間OK、消費税は3月31日、贈与税は2月1日〜3月15日など種類別の期限も一覧。",
    og_title="確定申告はいつまで？期限カウントダウン", og_desc="今年の申告期間と期限までの日数を自動計算。還付・消費税・贈与税の期限も。",
    lead="確定申告は、いつからいつまで？ 所得税の申告期間は<b>毎年2月16日〜3月15日</b>（土日祝なら翌平日）。今年の日程と<b>期限までの残り日数</b>を自動で計算します。還付申告・消費税・贈与税の期限もまとめて。",
    about_h2="確定申告の期間と期限",
    about="""<p>個人の所得税の確定申告は、<b>対象年の翌年2月16日から3月15日まで</b>が申告・納税の期間です。期限日が土曜・日曜・祝日にあたる年は、翌平日に繰り下がります。期限を過ぎると無申告加算税や延滞税がかかることがあるため、書類は早めに揃えておくのが安心です。</p>
    <div class="tbl-scroll"><table class="seo-table"><tr><th>種類</th><th>期間・期限</th></tr>
    <tr><td>所得税（申告納税）</td><td>2月16日〜3月15日</td></tr>
    <tr><td>還付申告（払いすぎの税金を取り戻す）</td><td>翌年1月1日から<b>5年間</b>いつでも</td></tr>
    <tr><td>消費税（個人事業主）</td><td>翌年3月31日まで</td></tr>
    <tr><td>贈与税</td><td>2月1日〜3月15日</td></tr>
    <tr><td>所得税の振替納税の引き落とし</td><td>4月中旬〜下旬</td></tr></table></div>
    <h2>期限を過ぎたらどうなる？</h2>
    <p>申告が必要なのに期限を過ぎると、本来の税額に<b>無申告加算税（原則5〜20%）</b>と<b>延滞税</b>が上乗せされます。ただし期限後1ヶ月以内の自主的な申告で一定条件を満たせば無申告加算税が免除される場合も。一方、医療費控除やふるさと納税（ワンストップ特例を使わなかった人）、年末調整で受けられなかった控除などの「還付申告」は2月16日を待つ必要がなく、<b>1月から受付・5年間有効</b>です。混み合う前の1月に済ませるのが賢い選択です。</p>
    <p>いくら戻るかは<a href="../iryouhi-koujo/">医療費控除の計算</a>や<a href="../fukugyo-zei/">副業の税金シミュレーター</a>、ふるさと納税の上限は<a href="../furusato/">ふるさと納税 上限額</a>でどうぞ。</p>
    <div class="note">期限は国税庁の公表に基づく一般的なルールで計算しています。災害等による期限延長や特例がある場合は国税庁の案内をご確認ください。</div>""",
    faqs=[("確定申告はいつからいつまで？", "所得税は翌年2月16日〜3月15日です。期限日が土日祝の場合は翌平日まで。本ツールが今年の実際の日付を表示します。"),
          ("還付申告も3月15日まで？", "いいえ。還付申告（払いすぎた税金を取り戻す申告）は翌年1月1日から5年間、いつでも提出できます。"),
          ("期限に間に合わなかったら？", "できるだけ早く申告してください。期限後申告には無申告加算税・延滞税がかかりますが、早いほど負担は軽くなります。"),
          ("入力データは送信される？", "このページは何も入力せず使え、外部にデータを送信しません。")],
    rel=[("iryouhi-koujo","🏥","医療費控除の計算"),("fukugyo-zei","💸","副業の税金・手取り"),("furusato","🎁","ふるさと納税 上限額"),("shukujitsu-calendar","📅","祝日カレンダー")],
    body="""  <section class="panel" id="resultPanel">
    <div class="result">
      <div class="label" id="lbl">確定申告の期限まで</div>
      <div class="big"><span id="big">—</span><span class="unit">日</span></div>
      <div class="sub" id="sub">—</div>
      <canvas id="cv" style="width:100%;height:auto;display:block;margin-top:14px;background:#fff;border:1px solid var(--line);border-radius:8px;"></canvas>
      <div class="statline"><div class="stat"><div class="k">受付開始</div><div class="v" id="st">—</div></div>
      <div class="stat"><div class="k">期限</div><div class="v accent" id="en">—</div></div>
      <div class="stat"><div class="k">対象</div><div class="v" id="tgt">—</div></div></div>
      <div class="field" style="margin:14px 0 0;text-align:left;"><label>申告の種類</label><select id="kind"><option value="income" selected>所得税（確定申告）</option><option value="refund">還付申告</option><option value="shohi">消費税（個人事業主）</option><option value="zoyo">贈与税</option></select></div>
      <div class="alert good" id="advice" style="margin-top:12px;">—</div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js=r"""(() => {
@@JS_COMMON@@
@@FIT_JS@@
  const nextWeekday = d => { while(d.getDay()===0||d.getDay()===6) d=new Date(d.getTime()+86400000); return d; };
  const wareki = y => '令和'+(y-2018)+'年';
  function period(kind, y){ // y=申告する年（対象は前年分）
    if(kind==='income') return {s:nextWeekday(new Date(y,1,16)), e:nextWeekday(new Date(y,2,15))};
    if(kind==='refund') return {s:new Date(y,0,1), e:nextWeekday(new Date(y+4,11,31))};
    if(kind==='shohi') return {s:new Date(y,0,1), e:nextWeekday(new Date(y,2,31))};
    return {s:nextWeekday(new Date(y,1,1)), e:nextWeekday(new Date(y,2,15))};
  }
  function render(){
    const kind=$('kind').value, today=new Date(); today.setHours(0,0,0,0);
    let y=today.getFullYear(); let p=period(kind,y); if(today>p.e) { y++; p=period(kind,y); }
    const toS=Math.round((p.s-today)/86400000), toE=Math.round((p.e-today)/86400000);
    const open = today>=p.s && today<=p.e;
    $('lbl').textContent= open ? '申告期限まで' : '受付開始まで';
    $('big').textContent= open ? toE : toS;
    $('sub').textContent= open ? `受付中です（期限 ${jaDate(p.e)}）` : `${jaDate(p.s)} から受付。期限は ${jaDate(p.e)}`;
    $('st').textContent=(p.s.getMonth()+1)+'/'+p.s.getDate(); $('en').textContent=(p.e.getMonth()+1)+'/'+p.e.getDate()+(p.e.getFullYear()!==y?'('+p.e.getFullYear()+')':'');
    $('tgt').textContent=wareki(y-1)+'分';
    const adv={income:'📌 給与以外の所得が20万円超、年収2,000万円超、個人事業主などは申告が必要です。e-Taxなら自宅から24時間提出できます。',
      refund:'📌 医療費控除・ふるさと納税・住宅ローン控除初年度などは還付申告。2月を待たず1月から提出でき、5年間さかのぼれます。',
      shohi:'📌 課税事業者（前々年の課税売上1,000万円超・インボイス登録者など）は消費税の申告も必要。期限は所得税より半月遅い3月31日です。',
      zoyo:'📌 年間110万円を超える贈与を受けた人が対象。所得税と別の申告書で、期間は2月1日〜3月15日です。'}[kind];
    $('advice').textContent=adv;
    draw(p, today, y);
    SHARE= open ? `確定申告の期限まであと${toE}日🗓️ 期限は${jaDate(p.e)}。まだの人は急いで👇` : `今年の確定申告は${jaDate(p.s)}から。受付開始まであと${toS}日🗓️`;
  }
  function draw(p, today, y){
    const cv=$('cv'); const {x,W,H}=fitCanvas(cv,0.28);
    x.fillStyle='#fff'; x.fillRect(0,0,W,H);
    const L=16,R=16,y0=H*0.5,w=W-L-R; const a=new Date(y-1,11,1), b=new Date(y,4,31);
    const X=d=>L+((d-a)/(b-a))*w;
    x.strokeStyle='rgba(20,24,29,.12)'; x.lineWidth=10; x.lineCap='round'; x.beginPath(); x.moveTo(L,y0); x.lineTo(W-R,y0); x.stroke();
    x.strokeStyle='#c4442b'; x.beginPath(); x.moveTo(X(p.s),y0); x.lineTo(X(Math.min(p.e,b)),y0); x.stroke();
    x.font='11px system-ui,sans-serif'; x.fillStyle='#8b929c'; x.textAlign='center';
    for(let d=new Date(a); d<=b; d.setMonth(d.getMonth()+1)){ x.fillText((d.getMonth()+1)+'月', X(d)+w/12, y0+24); }
    x.fillStyle='#c4442b'; x.font='600 12px system-ui,sans-serif'; x.fillText('申告期間', (X(p.s)+X(Math.min(p.e,b)))/2, y0-16);
    if(today>=a&&today<=b){ x.fillStyle='#14181d'; x.beginPath(); x.moveTo(X(today),y0-14); x.lineTo(X(today)-6,y0-24); x.lineTo(X(today)+6,y0-24); x.closePath(); x.fill(); x.font='600 11px system-ui,sans-serif'; x.fillText('今日', X(today), y0-28); }
  }
  $('kind').addEventListener('change',render);
  let rt; addEventListener('resize',()=>{ clearTimeout(rt); rt=setTimeout(render,200); });
  render(); bindShare();
})();""")

# ============================================================
# 9 お盆はいつ？（お盆休み・お彼岸）  KW: お盆 いつ 64k/KD3・お彼岸 いつ 32k/KD0
# ============================================================
sim(slug="obon-itsu", cat="season", emoji="🏮", score=67,
    title="お盆はいつ？お盆休み・お彼岸カウントダウン",
    card_desc="今年・来年のお盆（8月13〜16日）と、山の日・土日とつながるお盆休みの最長連休を自動計算。春・秋のお彼岸の日程も。",
    title_tag="お盆はいつ？2026・2027年のお盆休み期間と最長連休｜お彼岸の日程・カウントダウンつき",
    meta_desc="お盆はいつからいつまで？月遅れ盆（8月13〜16日）・新盆（7月）・旧盆の違いと、今年・来年のお盆休みが山の日・土日とつながって何連休になるかを自動計算する無料ツール。春分・秋分から春と秋のお彼岸の日程も表示。カウントダウンつき。",
    og_title="お盆はいつ？お盆休み・お彼岸カウントダウン", og_desc="今年のお盆休み期間と最長連休、お彼岸の日程を自動計算。",
    lead="お盆は、いつからいつまで？ 全国で最も一般的な<b>月遅れ盆（8月13日〜16日）</b>を基準に、山の日や土日とつながる<b>今年のお盆休みの最長連休</b>を自動計算します。春と秋の<b>お彼岸</b>の日程もあわせて。",
    about_h2="お盆は地域で3種類ある",
    about="""<div class="tbl-scroll"><table class="seo-table"><tr><th>呼び方</th><th>時期</th><th>主な地域</th></tr>
    <tr><td><b>月遅れ盆（8月盆）</b></td><td>8月13日〜16日</td><td>全国の大多数</td></tr>
    <tr><td>新盆（7月盆）</td><td>7月13日〜16日</td><td>東京都心部・神奈川の一部・金沢など</td></tr>
    <tr><td>旧盆</td><td>旧暦7月13〜15日（年により8〜9月）</td><td>沖縄・奄美</td></tr></table></div>
    <p>会社の「お盆休み」は法律で決まった祝日ではなく、多くの企業が8月13〜16日前後に夏季休暇を設定しています。2016年に<b>山の日（8月11日）</b>が祝日になったことで、土日と組み合わせて<b>9連休</b>になる年もあります。</p>
    <h2>お彼岸はいつ？</h2>
    <p>お彼岸は<b>春分の日・秋分の日を中日（ちゅうにち）として前後3日ずつ、計7日間</b>です。春分・秋分の日付は年によって1日ずれるため、本ツールでは天文計算の近似式で日付を求めています。初日を「彼岸の入り」、最終日を「彼岸明け」と呼び、お墓参りをする習慣があります。</p>
    <p>帰省の費用は<a href="../kisei-total/">帰省コスト内訳</a>、お盆の交通費比較は<a href="../shinkansen-car/">新幹線 vs 車</a>でどうぞ。連休の作り方は<a href="../renkyuu-maker/">9連休メーカー</a>。</p>
    <div class="note">祝日データは holidays-jp から取得。春分・秋分の日は近似計算のため、確定日は国立天文台の公表（前年2月）をご確認ください。</div>""",
    faqs=[("お盆は何日から何日まで？", "全国的には8月13日（迎え火）から16日（送り火）までの4日間です。東京都心部などは7月13〜16日の新盆、沖縄は旧暦で行います。"),
          ("お盆休みは祝日？", "いいえ。お盆自体は祝日ではなく、企業が夏季休暇として設定する休みです。8月11日の山の日だけが祝日です。"),
          ("お彼岸は何日間？", "春分の日・秋分の日を中心に前後3日、計7日間です。初日が彼岸の入り、最終日が彼岸明けです。"),
          ("入力データは送信される？", "このページは何も入力せず使え、外部にデータは送信しません。")],
    rel=[("kisei-total","🚗","帰省コスト内訳"),("shinkansen-car","🚄","新幹線 vs 車"),("renkyuu-maker","🏖️","9連休メーカー"),("shukujitsu-calendar","📅","祝日カレンダー")],
    body="""  <section class="panel" id="resultPanel">
    <div class="result">
      <div class="label"><span id="yLbl">今年</span>のお盆（8月13日）まで</div>
      <div class="big"><span id="big">—</span><span class="unit">日</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">お盆期間</div><div class="v" id="obon">8/13〜8/16</div></div>
      <div class="stat"><div class="k">最長のお盆休み</div><div class="v accent" id="longest">—</div></div>
      <div class="stat"><div class="k">山の日</div><div class="v" id="yama">—</div></div></div>
      <div id="cal" style="margin-top:14px;text-align:left;"></div>
      <div class="tbl-scroll" style="margin-top:14px;"><table class="seo-table" id="higan"><tr><th>お彼岸</th><th>期間</th><th>中日</th></tr></table></div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js=r"""(() => {
@@JS_COMMON@@
@@FIT_JS@@
  let H={};
  const isOff=d=>d.getDay()===0||d.getDay()===6||!!H[ymd(d)];
  const shunbun=y=>Math.floor(20.8431+0.242194*(y-1980)-Math.floor((y-1980)/4));
  const shubun=y=>Math.floor(23.2488+0.242194*(y-1980)-Math.floor((y-1980)/4));
  function longestRun(y){ // 8/8〜8/17 に重なる、休み＋お盆(13-16)の最長連続
    const off=d=> isOff(d) || (d.getMonth()===7 && d.getDate()>=13 && d.getDate()<=16);
    let best={len:0}; for(let d=new Date(y,7,6); d<=new Date(y,7,18); d=new Date(d.getTime()+86400000)){ if(!off(d)) continue; let a=new Date(d),b=new Date(d); while(off(new Date(a.getTime()-86400000))) a=new Date(a.getTime()-86400000); while(off(new Date(b.getTime()+86400000))) b=new Date(b.getTime()+86400000); const len=Math.round((b-a)/86400000)+1; if(len>best.len) best={len,a,b}; }
    return best;
  }
  async function load(){
    try{ const r=await fetch('https://holidays-jp.github.io/api/v1/date.json'); H=await r.json(); }catch(e){}
    render();
  }
  function render(){
    const today=new Date(); today.setHours(0,0,0,0);
    let y=today.getFullYear(); if(today>new Date(y,7,16)) y++;
    const obon=new Date(y,7,13), dd=Math.round((obon-today)/86400000);
    $('yLbl').textContent=y+'年'; $('big').textContent=Math.max(0,dd);
    $('sub').textContent= dd<0 ? `お盆期間中です（〜8/16）` : `${jaDate(obon)} が迎え火。送り火は8/16（${'日月火水木金土'[new Date(y,7,16).getDay()]}）`;
    const run=longestRun(y); $('longest').textContent= run.len? run.len+'連休（'+(run.a.getMonth()+1)+'/'+run.a.getDate()+'〜'+(run.b.getMonth()+1)+'/'+run.b.getDate()+'）':'—';
    const ym=new Date(y,7,11); $('yama').textContent='8/11（'+'日月火水木金土'[ym.getDay()]+'）';
    // 8月カレンダー
    let html=`<div style="font-weight:700;font-size:13px;margin-bottom:6px;">${y}年8月（朱＝お盆・祝日 / 薄朱＝休みがつながる期間）</div><div style="display:grid;grid-template-columns:repeat(7,1fr);gap:3px;font-size:12px;text-align:center;">`;
    '日月火水木金土'.split('').forEach((w,i)=>html+=`<div style="color:${i===0?'#c4442b':i===6?'#1b4a63':'var(--ink-3)'};font-weight:600;">${w}</div>`);
    const first=new Date(y,7,1); for(let i=0;i<first.getDay();i++) html+='<div></div>';
    for(let d=1;d<=31;d++){ const dt=new Date(y,7,d); const isObon=d>=13&&d<=16, hol=!!H[ymd(dt)], inRun= run.len&&dt>=run.a&&dt<=run.b;
      const bg= (isObon||hol)? '#c4442b' : inRun? 'rgba(196,68,43,.16)' : dt.getDay()===0?'rgba(196,68,43,.06)':dt.getDay()===6?'rgba(27,74,99,.07)':'transparent';
      const col=(isObon||hol)?'#fff':dt.getDay()===0?'#c4442b':dt.getDay()===6?'#1b4a63':'var(--ink)';
      html+=`<div style="padding:6px 0;border-radius:5px;background:${bg};color:${col};${ymd(dt)===ymd(today)?'outline:2px solid #14181d;':''}">${d}${hol?'<div style="font-size:9px;">山の日</div>':isObon?'<div style="font-size:9px;">お盆</div>':''}</div>`; }
    html+='</div>'; $('cal').innerHTML=html;
    // お彼岸（今年・来年）
    const rows=[]; [today.getFullYear(), today.getFullYear()+1].forEach(yy=>{ const sp=new Date(yy,2,shunbun(yy)), au=new Date(yy,8,shubun(yy));
      [[sp,'春のお彼岸'],[au,'秋のお彼岸']].forEach(([m,nm])=>{ const a=new Date(m.getTime()-3*86400000), b=new Date(m.getTime()+3*86400000); const days=Math.round((a-today)/86400000);
        rows.push(`<tr><td>${yy}年 ${nm}</td><td>${a.getMonth()+1}/${a.getDate()}（入り）〜${b.getMonth()+1}/${b.getDate()}（明け）${days>0?'　あと'+days+'日':(today<=b?'　期間中':'')}</td><td>${m.getMonth()+1}/${m.getDate()}</td></tr>`); }); });
    $('higan').innerHTML='<tr><th>お彼岸</th><th>期間</th><th>中日</th></tr>'+rows.join('');
    SHARE=`${y}年のお盆（8/13）まであと${Math.max(0,dd)}日🏮 お盆休みは最長${run.len}連休（${run.a?(run.a.getMonth()+1)+'/'+run.a.getDate()+'〜'+(run.b.getMonth()+1)+'/'+run.b.getDate():''}）。お彼岸の日程もこちら👇`;
  }
  load(); bindShare();
})();""")

# ============================================================
# 10 今日の花粉飛散 予測指数（気象条件から）  KW: 花粉 今日 119k/KD5
# ============================================================
sim(slug="kafun-yohou", cat="health", emoji="🌾", score=66,
    title="今日の花粉飛散 予測指数（気温・風・雨から判定）",
    card_desc="今日・明日・明後日の花粉の飛びやすさを、予想気温・風・雨・湿度と季節から5段階で予測。都道府県別。",
    title_tag="今日の花粉飛散 予測指数｜気温・風・雨から花粉の飛びやすさを5段階判定（都道府県別・3日間）",
    meta_desc="今日は花粉が多い？都道府県を選ぶと、予想気温・最大風速・降水・湿度と季節（スギ・ヒノキ・イネ科・ブタクサ）から花粉の飛びやすさを5段階で予測する無料ツール。今日・明日・明後日の3日分。花粉が飛びやすい気象条件の解説つき。",
    og_title="今日の花粉飛散 予測指数", og_desc="気温・風・雨・湿度と季節から花粉の飛びやすさを5段階予測。3日分。",
    lead="今日は花粉、飛びそう？ 花粉は<b>晴れて気温が高く、風が強く、雨上がりの翌日</b>にどっと飛びます。お住まいの都道府県の予報からこの条件を点数化し、今日・明日・明後日の<b>飛びやすさを5段階</b>で予測します。",
    about_h2="花粉が飛びやすい気象条件",
    about="""<div class="tbl-scroll"><table class="seo-table"><tr><th>条件</th><th>飛散への影響</th></tr>
    <tr><td>晴れて気温が高い</td><td>◎ 多い（スギは最高気温15℃前後から急増）</td></tr>
    <tr><td>風が強い（風速7m/s以上）</td><td>◎ 遠くから運ばれ多い</td></tr>
    <tr><td>湿度が低く乾燥</td><td>○ 多い</td></tr>
    <tr><td>雨の日</td><td>× 少ない（花粉が地面に落ちる）</td></tr>
    <tr><td>雨上がりの翌日</td><td>◎ 非常に多い（溜まった分がまとめて飛ぶ）</td></tr></table></div>
    <h2>季節ごとの花粉の種類</h2>
    <p>2〜4月が<b>スギ・ヒノキ</b>（患者数最多）、5〜6月は<b>イネ科</b>（カモガヤなど）、8〜10月は<b>ブタクサ・ヨモギ</b>（秋の花粉症）。11〜1月はほぼ飛散しません。本ツールはこの季節ごとの基礎レベルに、気象条件の点数をかけ合わせて指数を出しています。</p>
    <div class="note"><b>これは気象条件からの予測指数で、花粉の実測値ではありません。</b>実際の飛散量は環境省「はなこさん」の後継となる各機関の観測データや、気象会社の花粉情報をあわせてご確認ください。症状がつらいときは耳鼻科・アレルギー科にご相談を。</div>
    <p>年間の花粉症の出費は<a href="../kafun-cost/">花粉症の年間費用</a>、空気の状態は<a href="../kuuki-kirei/">空気きれいメーター</a>、洗濯物を外に干せるかは<a href="../sentaku-kawaku/">洗濯物 乾く時間メーター</a>でどうぞ。</p>""",
    faqs=[("これは実測の花粉情報？", "いいえ。予想気温・風・雨・湿度と季節から「飛びやすさ」を推定した予測指数です。実測値は各観測機関の情報をご確認ください。"),
          ("雨の翌日はなぜ多い？", "雨の日は花粉が落ちて飛散が減りますが、その分が翌日の晴れと風でまとめて舞い上がるためです。"),
          ("秋も花粉症になる？", "はい。8〜10月はブタクサ・ヨモギ・カナムグラの花粉が飛び、秋の花粉症の原因になります。背の低い草なので、河川敷や空き地の近くで症状が出やすいです。"),
          ("入力データは送信される？", "都道府県の緯度経度が気象APIに送られるだけで、個人情報は送信しません。")],
    rel=[("kafun-cost","💊","花粉症の年間費用"),("kuuki-kirei","🌫️","空気きれいメーター"),("sentaku-kawaku","👕","洗濯物 乾く時間メーター"),("kasa-iru","☂️","今日、傘いる？")],
    body="""  <section class="panel">
    <h2>🌾 場所を選ぶ</h2>
    <div class="field"><label>都道府県</label><select id="pref"></select></div>
    <button class="btn btn-ghost" id="geoBtn" type="button" style="width:100%;">📍 現在地を使う</button>
  </section>
  <section class="panel" id="resultPanel">
    <div class="result">
      <div class="label"><span id="whereLbl">東京都</span>・今日の花粉飛散 予測</div>
      <div class="big" style="font-size:min(11vw,44px);"><span id="big">—</span></div>
      <div class="sub" id="sub">予報を取得中…</div>
      <canvas id="cv" style="width:100%;height:auto;display:block;margin-top:12px;background:#fdfcf8;border:1px solid var(--line);border-radius:8px;"></canvas>
      <div class="statline" id="days3"></div>
      <div class="statline"><div class="stat"><div class="k">いまの主な花粉</div><div class="v" id="kind">—</div></div>
      <div class="stat"><div class="k">最高気温／風</div><div class="v" id="tw">—</div></div>
      <div class="stat"><div class="k">雨</div><div class="v accent" id="rn">—</div></div></div>
      <div class="alert good" id="advice" style="margin-top:12px;">—</div>
@@SHARE_ROW@@
    </div>
  </section>""",
    js=r"""(() => {
@@JS_COMMON@@
@@FIT_JS@@
@@PREFS_JS@@
@@GEO_JS@@
  const SEASON={1:.3,2:.9,3:1,4:.9,5:.55,6:.45,7:.2,8:.45,9:.6,10:.5,11:.2,12:.15};
  const KIND=m=> m>=2&&m<=4?'スギ・ヒノキ': m>=5&&m<=6?'イネ科（カモガヤ等）': m>=8&&m<=10?'ブタクサ・ヨモギ':'ほぼ飛散なし';
  const LV=[[20,'少ない','#8fbf9f'],[40,'やや多い','#c9c56a'],[60,'多い','#e8a14b'],[85,'非常に多い','#d9642f'],[999,'極めて多い','#b3261e']];
  const lvOf=s=>LV.find(l=>s<l[0]);
  let data=null, where='東京都', parts=[];
  function score(i){ const d=data.daily; const m=new Date(d.time[i]+'T00:00:00').getMonth()+1;
    const t=d.temperature_2m_max[i], w=d.wind_speed_10m_max[i], r=d.precipitation_sum[i], ry=i>0?d.precipitation_sum[i-1]:0;
    const hum=d.relative_humidity_2m_mean? d.relative_humidity_2m_mean[i] : 60;
    const fT= t<8?0.4: t<15?0.7: t<25?1.0: 0.9;
    const fR= r>=1?0.35: (ry>=1?1.3:1.0);
    const fW= w<3?0.7: w<7?1.0: 1.3;
    const fH= hum<40?1.2: hum<=70?1.0: 0.75;
    return {s:Math.min(100, SEASON[m]*fT*fR*fW*fH*100), t,w,r,m}; }
  async function load(lat,lon,name){
    where=name; $('whereLbl').textContent=name; $('sub').textContent='予報を取得中…';
    try{ const r=await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&daily=temperature_2m_max,precipitation_sum,wind_speed_10m_max,relative_humidity_2m_mean&timezone=Asia%2FTokyo&past_days=1&forecast_days=3`); data=await r.json(); render(); }
    catch(e){ $('sub').textContent='⚠️ 予報を取得できませんでした。時間をおいて再度お試しください。'; }
  }
  function render(){
    if(!data) return;
    const rs=[1,2,3].map(i=>score(i));           // index0は昨日（past_days=1）
    const t=rs[0], lv=lvOf(t.s);
    $('big').textContent=lv[1]; $('big').style.color=lv[2];
    $('sub').textContent=`予測指数 ${Math.round(t.s)}／100（${data.daily.time[1].replace(/-/g,'/')}・気象条件ベース）`;
    $('kind').textContent=KIND(t.m); $('tw').textContent=Math.round(t.t)+'℃ / '+t.w.toFixed(0)+'m/s'; $('rn').textContent= t.r>=1? '雨（飛散↓）': (data.daily.precipitation_sum[0]>=1? '昨日雨→今日↑':'なし');
    $('days3').innerHTML=['今日','明日','明後日'].map((n,i)=>{ const l=lvOf(rs[i].s); return `<div class="stat"><div class="k">${n}</div><div class="v" style="color:${l[2]}">${l[1]}</div></div>`; }).join('');
    const adv= t.s>=60? '😷 マスク・メガネ、帰宅時は玄関前で払い落とし、洗濯物は室内干しがおすすめ。' : t.s>=40? '🙂 敏感な人は対策を。外出後の洗顔・うがいで症状を軽く。' : t.s>=20? '🙂 飛散はやや多め。症状が出やすい人はマスクがあると安心。' : '😌 飛散は少なめの予測。それでも症状が出るなら他のアレルゲンも疑ってみて。';
    $('advice').textContent= (t.m>=11||t.m<=1)? '❄️ この時期は花粉はほぼ飛びません。鼻炎なら寒暖差やハウスダストが原因かも。' : adv;
    draw(rs.map(r=>r.s));
    SHARE=`${where}の今日の花粉飛散予測は「${lv[1]}」（指数${Math.round(t.s)}）🌾 明日は「${lvOf(rs[1].s)[1]}」。気象条件からの予測はこちら👇`;
  }
  let raf=0;
  function draw(sc){
    cancelAnimationFrame(raf);
    const cv=$('cv'); const {x,W,H}=fitCanvas(cv,0.38);
    const n=Math.round(sc[0]/100*160)+6; parts=[]; for(let i=0;i<n;i++) parts.push({x:Math.random()*W*0.62,y:Math.random()*H,vx:0.3+Math.random()*0.7,vy:(Math.random()-0.5)*0.4,r:1.5+Math.random()*2.2,ph:Math.random()*6.283});
    const bw=W*0.11, bx=W*0.66;
    function frame(){
      x.fillStyle='#fdfcf8'; x.fillRect(0,0,W,H);
      x.fillStyle='rgba(20,24,29,.06)'; x.fillRect(0,0,W*0.62,H);
      // 花粉の粒
      for(const p of parts){ p.x+=p.vx; p.y+=p.vy+Math.sin(p.ph+=0.05)*0.3; if(p.x>W*0.62) p.x=-4; if(p.y<0) p.y=H; if(p.y>H) p.y=0;
        x.fillStyle='rgba(232,161,75,.75)'; x.beginPath(); x.arc(p.x,p.y,p.r,0,6.283); x.fill(); }
      x.fillStyle='#59616c'; x.font='11px system-ui,sans-serif'; x.textAlign='left'; x.fillText('今日の飛びやすさイメージ', 10, 16);
      // 3日棒
      ['今日','明日','明後日'].forEach((nm,i)=>{ const l=lvOf(sc[i]); const h=(sc[i]/100)*(H-58), X=bx+i*bw;
        x.fillStyle=l[2]; x.fillRect(X,H-28-h,bw*0.7,h); x.fillStyle='#14181d'; x.font='700 12px system-ui,sans-serif'; x.textAlign='center'; x.fillText(Math.round(sc[i]), X+bw*0.35, H-32-h); x.fillStyle='#59616c'; x.font='11px system-ui,sans-serif'; x.fillText(nm, X+bw*0.35, H-10); });
      raf=requestAnimationFrame(frame);
    }
    frame();
  }
  const go=()=>{ const p=PREFS[+$('pref').value]; load(p[1],p[2],p[0].replace(/\(.*\)/,'')); };
  $('pref').addEventListener('change',go); $('geoBtn').addEventListener('click',()=>useGeo(load));
  let rt; addEventListener('resize',()=>{ clearTimeout(rt); rt=setTimeout(render,200); });
  go(); bindShare();
})();""")

# ============================================================
# ビルド
# ============================================================
IDX = os.path.join(ROOT, "index.html")
with io.open(IDX, encoding="utf-8") as f:
    html = f.read()
assert "sims/dollar-yen-chart/" not in html, "既に挿入済み（中止）"

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
    js = (s["js"].replace("@@JS_COMMON@@", JS_COMMON).replace("@@PREFS_JS@@", PREFS_JS).replace("@@FIT_JS@@", FIT_JS)
          .replace("@@GEO_JS@@", GEO_JS).replace("@@WORLD@@", WORLD).replace("@@CITIES@@", _CITY_JS).replace("@@CC@@", json.dumps(_CC, ensure_ascii=False)))
    body = s["body"].replace("@@SHARE_ROW@@", SHARE_ROW)
    about = s["about"].replace("@@JISA_TABLE@@", _JISA_TABLE)
    page = (SKELETON
        .replace("@@SLUG@@", s["slug"]).replace("@@TITLE_TAG@@", s["title_tag"])
        .replace("@@META_DESC@@", s["meta_desc"]).replace("@@OG_TITLE@@", s["og_title"]).replace("@@OG_DESC@@", s["og_desc"])
        .replace("@@LD_APP@@", ld_app).replace("@@LD_BREAD@@", ld_bread).replace("@@LD_FAQ@@", faq_ld(s["faqs"]))
        .replace("@@CATJP@@", s["catjp"]).replace("@@H1@@", s["title"]).replace("@@LEAD@@", s["lead"])
        .replace("@@BODY@@", body).replace("@@ABOUT_H2@@", s["about_h2"]).replace("@@ABOUT@@", about)
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
insert_after("inu-sanpo-ok", ["kyou-fukusou", "kafun-yohou"])
insert_after("nankyoku-ima", ["kyou-no-tsuki", "sekai-jisa"])
insert_after("solar-hatsuden", ["dollar-yen-chart", "kin-souba"])
insert_after("umareta-hi-tenki", ["shukujitsu-calendar", "kaigai-shukujitsu", "obon-itsu", "kakutei-shinkoku-itsu"])
for a, b in [("シミュレーター50選", "シミュレーター60選"), ("50本を一覧掲載", "60本を一覧掲載"), ("50本のコレクション", "60本のコレクション")]:
    lv = lv.replace(a, b)
lv = lv.replace("<tr><td>Wikipedia日本語版（CC BY-SA）</td>",
                "<tr><td>gold-api.com</td><td>金・銀・プラチナの国際スポット価格</td><td>18金 相場 1g 今日</td></tr>\n      <tr><td>Nager.Date</td><td>世界各国の公的祝日</td><td>海外の祝日カレンダー</td></tr>\n      <tr><td>Wikipedia日本語版（CC BY-SA）</td>")
with io.open(LIVE, "w", encoding="utf-8") as f:
    f.write(lv)
print("patched live/index.html: +10 cards, 50->60")

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

# api/share.js ALLOW
SH = os.path.join(ROOT, "api", "share.js")
with io.open(SH, encoding="utf-8") as f:
    sh = f.read()
ids = ", ".join("'%s'" % s["slug"] for s in SIMS)
sh = sh.replace("const ALLOW = new Set([", "const ALLOW = new Set([\n  " + ids + ",", 1)
with io.open(SH, "w", encoding="utf-8") as f:
    f.write(sh)
print("patched api/share.js: +%d ids" % len(SIMS))
print("ALL DONE")
