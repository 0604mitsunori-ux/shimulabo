"""2026-10-10 改善5か所（GA4・サチコ 8〜10月の実データから選定）。生成済みHTMLを直接書き換える。
何度実行しても同じ結果になる（各ページに <!-- improved-2026-10 --> を入れ、入っていればスキップ）。
生成元（gen_sims*.py）を再実行したページは、このスクリプトをもう一度実行すれば戻る。

  ① 海抜チェッカー … ハザードマップ・地理院地図へのボタン／海抜の目安／「海抜とは・標高との違い」
  ② チケット当選確率 … タイトルに「当落」、口数別の確率表、倍率の出し方（応募数÷座席数）
  ③ 歯車 … タイトルに「ギア比 計算」、回転数・速度伝達比の計算、回転カウンター・一時停止・全画面、授業で使える問い
  ④ 出席率・血のつながり・ml⇔g … Googleで9〜12位の検索の聞き方にタイトルと答えを合わせる
  ⑤ ライブ系30本 … 選んだ地域をブラウザに記憶し、次に開いたときはその地域ですぐ表示（assets/live-remember.js）
"""
import json, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
MARK = "<!-- improved-2026-10 -->"


def page(slug):
    return ROOT / "sims" / slug / "index.html"


def rep(h, old, new, count=1):
    n = h.count(old)
    if n != count:
        raise SystemExit(f"置換対象が {n} 件（期待 {count} 件）: {old[:80]!r}")
    return h.replace(old, new)


def set_title(h, title, desc, og=None):
    h = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", h, count=1)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', h, count=1)
    if og:
        h = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{og}">', h, count=1)
    return h


def add_faq(h, qas, first=False):
    """よくある質問（dl.faq）と FAQPage 構造化データの両方に Q&A を足す。answer の HTML タグは構造化データでは外す"""
    m = re.search(r'<script type="application/ld\+json">(\{"@context": "https://schema.org", "@type": "FAQPage".*?)</script>', h)
    data = json.loads(m.group(1))
    items = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in qas]
    data["mainEntity"] = items + data["mainEntity"] if first else data["mainEntity"] + items
    h = h.replace(m.group(1), json.dumps(data, ensure_ascii=False))
    dl = "".join(f"<dt>{q}</dt><dd>{a}</dd>" for q, a in qas)
    if first:
        h = rep(h, '<dl class="faq">', '<dl class="faq">' + dl)
    else:
        i = h.index('<dl class="faq">'); j = h.index("</dl>", i)
        h = h[:j] + dl + h[j:]
    return h


def done(h):
    return MARK in h


# ---------------------------------------------------------------- ① 海抜チェッカー
def kaibatsu():
    p = page("kaibatsu-check"); h = p.read_text(encoding="utf-8")
    if done(h): return "skip"
    h = set_title(h, "うちの海抜チェッカー｜住所で海抜（標高）を調べる・ハザードマップも｜シミュラボ",
                  "住所や駅名を入れるだけで、その場所の海抜（標高）を国土地理院の公式データから即計算。結果からその地点のハザードマップ（洪水・津波・高潮・土砂災害）をワンタップで開けます。海抜と標高の違い、海抜ゼロメートル地帯の解説つき。",
                  "うちの海抜チェッカー｜住所で海抜（標高）を調べる")
    # 結果の下：海抜の目安＋ハザードマップ・地理院地図へのボタン
    h = rep(h, '''      <div style="text-align:center;"><span id="shareCount" class="share-count" style="display:none"></span></div>
      <div class="share-row">
        <button class="btn btn-x" id="shareBtn">𝕏 で結果をシェア</button>''',
            '''      <div class="note" id="levelNote" style="margin-top:14px;text-align:left;"></div>
      <div class="share-row" style="margin-top:6px;">
        <a class="btn btn-primary" id="hazardBtn" href="https://disaportal.gsi.go.jp/" target="_blank" rel="noopener">🗺️ この場所のハザードマップを開く</a>
        <a class="btn btn-ghost" id="reliefBtn" href="https://maps.gsi.go.jp/" target="_blank" rel="noopener">⛰️ 地理院地図で周りの高さを見る</a>
      </div>
      <p class="hint" style="text-align:center;margin-top:4px;">国土地理院「重ねるハザードマップ」で、洪水・津波・高潮・土砂災害の想定をこの地点の地図で確認できます。</p>
      <div style="text-align:center;"><span id="shareCount" class="share-count" style="display:none"></span></div>
      <div class="share-row">
        <button class="btn btn-x" id="shareBtn">𝕏 で結果をシェア</button>''')
    h = rep(h, "      $('acc').textContent = j.hsrc || '—';",
            """      $('acc').textContent = j.hsrc || '—';
      const la = (+lat).toFixed(6), lo = (+lon).toFixed(6);
      $('hazardBtn').href = 'https://disaportal.gsi.go.jp/maps/?ll=' + la + ',' + lo + '&z=16&base=pale';
      $('reliefBtn').href = 'https://maps.gsi.go.jp/#16/' + la + '/' + lo + '/&base=std&ls=std%7Crelief&disp=11';
      let lv;
      if(ele < 0) lv = '<strong>海抜0m未満（海抜ゼロメートル地帯の可能性）</strong><br>まわりの海面より低い土地です。大雨や高潮のときに水が引きにくいため、ハザードマップで浸水の深さと避難先を必ず確認してください。';
      else if(ele < 5) lv = '<strong>海抜5m未満（低い土地）</strong><br>海や川に近い場合は、高潮・津波・洪水の想定区域に入っていることがあります。ハザードマップで浸水の深さを確認しましょう。';
      else if(ele < 20) lv = '<strong>海抜5〜20m</strong><br>海抜だけでは安全とも危険とも言えません。近くの川の氾濫や、低い場所へ水が集まる地形かどうかをハザードマップで確認しましょう。';
      else lv = '<strong>海抜20m以上</strong><br>津波・高潮の影響は受けにくい高さですが、がけ崩れ・土石流など土砂災害の警戒区域は高い場所に多くあります。ハザードマップの「土砂災害」も確認しましょう。';
      $('levelNote').innerHTML = lv;""")
    # 解説：海抜とは・標高との違い／海抜ゼロメートル地帯／調べたあとにやること
    h = rep(h, "    <h2>引用・転載について</h2>", MARK + '''
    <h2>海抜とは？標高との違い</h2>
    <p><b>海抜</b>は「海面からの高さ」、<b>標高</b>は「基準となる海面からの土地の高さ」のことで、日本ではどちらも<b>東京湾の平均海面（T.P.）を0m</b>として測った同じ高さを指します。地図や登山では「標高」、海辺の電柱や避難誘導の看板では「海抜」と書かれることが多い、という使い分けです。このツールが表示する数字も、国土地理院が東京湾平均海面を基準に測った標高です。</p>
    <div class="tbl-scroll"><table class="seo-table"><tr><th>言葉</th><th>意味</th><th>よく見る場所</th></tr>
    <tr><td>標高</td><td>東京湾平均海面を0mとした土地の高さ</td><td>地図・登山・国土地理院のデータ</td></tr>
    <tr><td>海抜</td><td>海面からの高さ（日本では標高と同じ値）</td><td>沿岸部の電柱・避難看板・防災マップ</td></tr>
    <tr><td>高さ（比高）</td><td>地面から建物などのてっぺんまで</td><td>ビルの高さ・タワーの高さ</td></tr></table></div>
    <h2>海抜ゼロメートル地帯とは</h2>
    <p>地面の高さが満潮時の海面より低い土地のことです。東京の江東区・墨田区・江戸川区の一部や、大阪湾・伊勢湾の沿岸などに広がっています。堤防で守られていますが、いったん浸水すると水が自然には引かないため、長い間水につかる想定になっている地域があります。</p>
    <h2>海抜を調べたあとにやること</h2>
    <ol>
    <li>結果の「この場所のハザードマップを開く」から、<b>洪水・高潮・津波・土砂災害</b>の想定を確認する</li>
    <li>浸水が想定されている場合は、その深さ（0.5m以上で床上浸水、3m以上で2階まで浸水 が目安）を確認する</li>
    <li>お住まいの自治体の指定緊急避難場所・避難所と、そこまでの道を確認する</li>
    <li>家族の人数分の水（1人1日3L）と食料を、最低3日分そなえる</li>
    </ol>
    <h2>引用・転載について</h2>''')
    h = add_faq(h, [
        ("海抜と標高の違いは？", "日本ではどちらも東京湾の平均海面を0mとして測った同じ高さです。地図や登山では「標高」、沿岸部の看板や防災の場面では「海抜」と書かれることが多いという違いです。"),
        ("海抜何メートルなら安全？", "海抜だけで安全かどうかは決まりません。津波・高潮は海抜が低い場所ほど影響を受けやすい一方、洪水は川との位置関係、土砂災害はむしろ高い場所の斜面で起きます。結果の「ハザードマップを開く」でその地点の想定を確認してください。"),
        ("海抜ゼロメートル地帯とは？", "地面の高さが満潮時の海面より低い土地のことです。堤防で守られていますが、浸水すると水が引きにくいのが特徴です。"),
    ])
    p.write_text(h, encoding="utf-8"); return "ok"


# ---------------------------------------------------------------- ② チケット当選確率
def ticket():
    p = page("ticket-tousen"); h = p.read_text(encoding="utf-8")
    if done(h): return "skip"
    h = set_title(h, "チケット当選確率・当落シミュレーター｜倍率と名義・公演数で何％当たる？｜シミュラボ",
                  "ライブ・イベントのチケット抽選の当落シミュレーター。倍率と応募口数（名義×公演数）から、少なくとも1枚当たる確率を計算。口数ごとの当選確率の早見表、倍率の出し方（応募数÷座席数）、会場の規模の目安つき。",
                  "チケット当選確率・当落シミュレーター｜何口で何％当たる？")
    h = rep(h, '''    <button class="btn btn-primary" id="calcBtn">当選確率を見る</button>
  </section>''', '''    <details style="margin:4px 0 12px;"><summary style="cursor:pointer;font-weight:800;font-size:14px;">倍率がわからないときは（座席数と応募数から計算）</summary>
      <div class="row" style="margin-top:10px;"><div class="field"><label>座席数（1公演） <span class="hint">（席）</span></label><input type="number" id="seats" value="15000" min="1" inputmode="numeric"></div>
      <div class="field"><label>応募数の見込み <span class="hint">（口）</span></label><input type="number" id="apps" value="150000" min="1" inputmode="numeric"></div></div>
      <button class="btn btn-ghost" id="rateBtn" type="button">この倍率を使う</button>
      <p class="hint" id="rateNote" style="margin-top:6px;">倍率 ＝ 応募数 ÷ 座席数（1口で2枚申し込む場合は、座席数を半分にして計算）</p>
    </details>
    <button class="btn btn-primary" id="calcBtn">当選確率を見る</button>
  </section>''')
    h = rep(h, '''      <div class="stat"><div class="k">判定</div><div class="v" id="judge">—</div></div></div>''',
            '''      <div class="stat"><div class="k">判定</div><div class="v" id="judge">—</div></div></div>
      <div class="tbl-scroll" style="margin-top:14px;"><table class="seo-table" id="byN"></table></div>''')
    h = rep(h, "    show(); anim($('big'),0,win*100,900,1);\n  }\n  $('calcBtn').addEventListener('click', calc);",
            """    const ns=[1,2,3,5,10,20,30]; if(!ns.includes(n)) ns.push(n); ns.sort((a,b)=>a-b);
    $('byN').innerHTML='<tr><th>応募口数</th><th>少なくとも1枚当たる確率</th></tr>'+ns.map(k=>'<tr'+(k===n?' style="font-weight:800"':'')+'><td>'+k+'口'+(k===n?'（いまの条件）':'')+'</td><td>'+((1-Math.pow(1-p,k))*100).toFixed(1)+'%</td></tr>').join('');
    show(); anim($('big'),0,win*100,900,1);
  }
  $('calcBtn').addEventListener('click', calc);
  $('rateBtn').addEventListener('click', () => { const s=+$('seats').value, a=+$('apps').value; if(!(s>0&&a>0)) return;
    const r=Math.max(1,Math.round(a/s*10)/10); $('rate').value=r; $('rateNote').textContent='倍率 '+r+'倍 を入れました（'+a.toLocaleString('ja-JP')+'口 ÷ '+s.toLocaleString('ja-JP')+'席）'; calc(); });""")
    h = rep(h, "    <h2>よくある質問</h2>", MARK + '''
    <h2>口数ごとの当選確率（早見表）</h2>
    <div class="tbl-scroll"><table class="seo-table"><tr><th>倍率</th><th>1口</th><th>3口</th><th>5口</th><th>10口</th><th>20口</th></tr>
    <tr><td>2倍</td><td>50.0%</td><td>87.5%</td><td>96.9%</td><td>99.9%</td><td>100.0%</td></tr>
    <tr><td>5倍</td><td>20.0%</td><td>48.8%</td><td>67.2%</td><td>89.3%</td><td>98.8%</td></tr>
    <tr><td>10倍</td><td>10.0%</td><td>27.1%</td><td>41.0%</td><td>65.1%</td><td>87.8%</td></tr>
    <tr><td>20倍</td><td>5.0%</td><td>14.3%</td><td>22.6%</td><td>40.1%</td><td>64.2%</td></tr>
    <tr><td>50倍</td><td>2.0%</td><td>5.9%</td><td>9.6%</td><td>18.3%</td><td>33.2%</td></tr></table></div>
    <p>倍率が10倍なら、1口では10%でも、10口申し込めば約65%。ただし20倍・50倍の公演では、口数を増やしても確率の伸びはゆるやかです。</p>
    <h2>倍率の出し方</h2>
    <p>倍率は「応募数 ÷ 座席数」です。座席数は会場の収容人数から、ステージの位置や機材席のぶんを引いた数になります。1回の申し込みで2枚まで申し込める公演では、当選の単位は「1申し込み」なので、座席数を半分にして計算すると実際に近くなります。</p>
    <div class="tbl-scroll"><table class="seo-table"><tr><th>会場の種類</th><th>収容人数の目安</th></tr>
    <tr><td>ドーム</td><td>約4万〜5.5万人</td></tr>
    <tr><td>スタジアム</td><td>約3万〜7万人</td></tr>
    <tr><td>アリーナ</td><td>約1万〜2万人（大型は3万人超も）</td></tr>
    <tr><td>ホール</td><td>約1,500〜5,000人</td></tr>
    <tr><td>ライブハウス</td><td>数百〜約2,500人</td></tr></table></div>
    <p class="hint">収容人数は会場や公演の組み方で大きく変わります。正確な数字は会場の公式サイトで確認してください。</p>
    <h2>よくある質問</h2>''')
    h = add_faq(h, [
        ("当落シミュレーターとは？", "抽選の倍率と応募口数から、少なくとも1枚当たる確率を計算するツールです。1口の当選率を1÷倍率とし、口数ぶん申し込んだときに全部外れる確率を1から引いて求めます。"),
        ("名義や公演を増やすと、どれくらい当たりやすくなる？", "倍率10倍なら、1口で10%、3口で約27%、10口で約65%です。結果の下に口数ごとの確率表が出ます。ただし名義の貸し借りや、同じ公演への重複申し込みを禁止している公演も多いので、必ず申し込みのルールを確認してください。"),
        ("FC先行と一般発売はどちらが当たりやすい？", "一般に、申し込める人が会員に限られるFC先行の方が倍率は低くなりやすいです。ただし配分される席数は公演ごとに異なり、公表されないことがほとんどです。"),
    ], first=True)
    p.write_text(h, encoding="utf-8"); return "ok"


# ---------------------------------------------------------------- ③ 歯車
def gears():
    p = page("gears"); h = p.read_text(encoding="utf-8")
    if done(h): return "skip"
    h = set_title(h, "歯車シミュレーター｜ギア比・回転数の計算（速度伝達比）｜シミュラボ",
                  "かみ合う歯車の歯数を変えると、ギア比と回転数がどう変わるかを目と数字で確かめられる無料シミュレーター。回転数（rpm）と速度伝達比の計算、回転カウンター、一時停止・全画面表示つきで、中学校の技術の授業にも使えます。",
                  "歯車シミュレーター｜ギア比・回転数の計算")
    h = rep(h, '''    <p style="text-align:center;color:var(--ink-2);font-size:13px;margin-top:14px;">歯数の比が、そのまま回転数の逆比に。歯数が半分の歯車は2倍速く回ります。</p>''',
            '''    <div class="row" style="max-width:560px;margin:12px auto 0;"><div class="field"><label>左（原動車）の回転数 <span class="hint">（rpm＝1分あたりの回転数）</span></label><input type="number" id="rpm" value="60" min="0" step="any" inputmode="decimal"></div></div>
    <div class="statline" style="max-width:560px;margin:0 auto;"><div class="stat"><div class="k">右（従動車）の回転数</div><div class="v accent" id="rpm2">—</div></div>
    <div class="stat"><div class="k">速度伝達比</div><div class="v" id="ratio">—</div></div>
    <div class="stat"><div class="k">回る向き</div><div class="v">左と反対</div></div></div>
    <div class="share-row" style="margin-top:4px;"><button class="btn btn-ghost" id="pauseBtn" type="button">⏸ 一時停止</button><button class="btn btn-ghost" id="resetBtn" type="button">↺ 回転数を0に</button><button class="btn btn-ghost" id="fsBtn" type="button">⛶ 全画面（電子黒板用）</button></div>
    <p style="text-align:center;color:var(--ink-2);font-size:13px;margin-top:14px;">歯数の比が、そのまま回転数の逆比に。歯数が半分の歯車は2倍速く回ります。</p>''')
    h = rep(h, "const cv=$('cv'),x=cv.getContext('2d');const W=cv.width,H=cv.height;let a=0;",
            "const cv=$('cv'),x=cv.getContext('2d');const W=cv.width,H=cv.height;let a=0,paused=false;")
    h = rep(h, """      a+=0.012; gear(cx1,cy,t1,a,'#5eead4'); gear(cx2,cy,t2,-a*t1/t2+Math.PI/t2,'#a78bfa');
      x.fillStyle='#fff';x.font='bold 15px sans-serif';x.textAlign='center';
      x.fillText('×'+(t1/t2).toFixed(2)+'倍速',W/2,H-14);""",
            """      if(!paused) a+=0.012; gear(cx1,cy,t1,a,'#5eead4'); gear(cx2,cy,t2,-a*t1/t2+Math.PI/t2,'#a78bfa');
      x.fillStyle='#fff';x.font='bold 15px sans-serif';x.textAlign='center';
      x.fillText('×'+(t1/t2).toFixed(2)+'倍速',W/2,H-14);
      const n1=a/(Math.PI*2), n2=n1*t1/t2; x.font='bold 14px sans-serif';
      x.fillStyle='#5eead4';x.textAlign='left';x.fillText('左 '+t1+'歯：'+n1.toFixed(1)+'回転',12,22);
      x.fillStyle='#a78bfa';x.textAlign='right';x.fillText('右 '+t2+'歯：'+n2.toFixed(1)+'回転',W-12,22);""")
    h = rep(h, "    } loop();\n",
            """    } loop();
    function calcRpm(){ const t1=+$('t1').value,t2=+$('t2').value,r=+$('rpm').value;
      $('rpm2').textContent=(isFinite(r)?(Math.round(r*t1/t2*100)/100):'—')+' rpm';
      $('ratio').textContent=(Math.round(t2/t1*100)/100)+'（'+t2+'÷'+t1+'）';
      SHARE='歯車シミュレーターで計算：左'+t1+'歯×'+r+'rpm → 右'+t2+'歯は'+(Math.round(r*t1/t2*100)/100)+'rpm（速度伝達比 '+(Math.round(t2/t1*100)/100)+'）⚙️'; }
    ['t1','t2','rpm'].forEach(id=>$(id).addEventListener('input',calcRpm)); calcRpm();
    $('pauseBtn').addEventListener('click',()=>{ paused=!paused; $('pauseBtn').textContent=paused?'▶ 再開':'⏸ 一時停止'; });
    $('resetBtn').addEventListener('click',()=>{ a=0; });
    $('fsBtn').addEventListener('click',()=>{ const el=cv; (el.requestFullscreen||el.webkitRequestFullscreen||function(){}).call(el); });
""")
    h = rep(h, "<!-- enriched-2026-09 -->", MARK + '''
<h2>回転数と速度伝達比の計算（中学校 技術）</h2>
<p>中学校の技術では、回す側の歯車を<b>原動車</b>、回される側を<b>従動車</b>と呼び、回転の速さがどれだけ変わるかを<b>速度伝達比</b>で表します。</p>
<div class="note"><strong>計算式</strong><br>速度伝達比 ＝ 原動車の回転数 ÷ 従動車の回転数 ＝ 従動車の歯数 ÷ 原動車の歯数<br>従動車の回転数 ＝ 原動車の回転数 × 原動車の歯数 ÷ 従動車の歯数</div>
<p>たとえば原動車24歯・従動車12歯なら、速度伝達比は 12÷24＝<b>0.5</b>。原動車が60rpmで回ると、従動車は 60×24÷12＝<b>120rpm</b> で回ります。速度伝達比が1より小さいと速く、1より大きいとゆっくり（そのぶん力が強く）回ります。上のシミュレーターに歯数と回転数を入れると、同じ計算がすぐに確かめられます。</p>
<h2>授業で使える問い</h2>
<details><summary>問1　原動車20歯・従動車40歯。原動車が1分間に60回転すると、従動車は何回転？</summary><p>60×20÷40＝<b>30回転</b>（速度伝達比は2）。</p></details>
<details><summary>問2　自転車の前のギア48歯・後ろのギア16歯。ペダルを1回こぐと、後輪は何回転？</summary><p>48÷16＝<b>3回転</b>。後ろのギアを大きくすると、こぐのは軽くなり、進む距離は短くなります。</p></details>
<details><summary>問3　歯車を3つ並べたとき、真ん中の歯車の歯数を変えると、右端の回転数は変わる？</summary><p><b>変わりません</b>。真ん中の歯車（アイドラー）は回る向きを変えるだけで、回転数の比は両端の歯数だけで決まります。</p></details>
<details><summary>問4　ゆっくり大きな力で回したいとき、速度伝達比は1より大きくする？小さくする？</summary><p><b>大きくします</b>。従動車の歯数を多くすると回転はゆっくりになり、回す力（トルク）は大きくなります。</p></details>
<p class="hint">先生向け：「全画面」で電子黒板に大きく映せます。「一時停止」で止めて歯の数を数えさせたり、「回転数を0に」で回転カウンターを戻して「左が2回転する間に右は何回転？」を数えさせたりできます。</p>
<!-- enriched-2026-09 -->''')
    h = add_faq(h, [
        ("ギア比の計算方法は？", "ギア比（速度伝達比）＝ 従動車の歯数 ÷ 原動車の歯数 です。従動車の回転数は「原動車の回転数 × 原動車の歯数 ÷ 従動車の歯数」で求められます。"),
        ("速度伝達比とは？", "中学校の技術で使う言葉で、原動車（回す側）の回転数 ÷ 従動車（回される側）の回転数のことです。歯車では「従動車の歯数 ÷ 原動車の歯数」と同じ値になります。"),
    ], first=True)
    p.write_text(h, encoding="utf-8"); return "ok"


# ---------------------------------------------------------------- ④ 検索の聞き方に合わせる3ページ
def tune3():
    out = []
    # 出席率：「出席率80 何回 休める」「3分の2以上の出席 計算」
    p = page("shusseki-ritsu"); h = p.read_text(encoding="utf-8")
    if not done(h):
        h = set_title(h, "出席率 計算｜出席率80%なら何回休める？3分の2の判定も｜シミュラボ",
                      "授業日数と欠席日数から出席率を計算する無料ツール。出席率80%・3分の2（約66.7%）・90%を保つには何回まで休めるかの早見表つき。大学の授業15回・30回、高校の年間授業日数にも対応。",
                      "出席率 計算｜出席率80%なら何回休める？")
        h = rep(h, "    <h2>学校段階別・出席率の考え方</h2>", MARK + '''
    <h2>出席率◯%を保つには何回まで休める？（早見表）</h2>
    <p>授業の回数ごとに、出席率を保てる欠席回数の上限です（欠席回数 ≦ 授業回数 ×（1 − 出席率）で、端数は切り捨て）。</p>
    <div class="tbl-scroll"><table class="seo-table"><tr><th>授業回数</th><th>90%以上</th><th>80%以上</th><th>75%以上</th><th>3分の2以上</th></tr>
    <tr><td>15回（大学の半期）</td><td>1回まで</td><td>3回まで</td><td>3回まで</td><td>5回まで</td></tr>
    <tr><td>30回（大学の通年）</td><td>3回まで</td><td>6回まで</td><td>7回まで</td><td>10回まで</td></tr>
    <tr><td>35回（高校の週1科目）</td><td>3回まで</td><td>7回まで</td><td>8回まで</td><td>11回まで</td></tr>
    <tr><td>200日（年間の授業日数）</td><td>20日まで</td><td>40日まで</td><td>50日まで</td><td>66日まで</td></tr></table></div>
    <p class="hint">遅刻・早退を欠席に数える学校や、「3分の1を超えて欠席すると不可」のように境目の扱いが違う学校もあります。最終的には在籍校の規定を確認してください。</p>
    <h2>学校段階別・出席率の考え方</h2>''')
        h = add_faq(h, [
            ("出席率80%だと何回休める？", "授業15回なら3回、30回なら6回、年間200日なら40日まで休めます（欠席回数 ≦ 授業回数 × 0.2）。"),
            ("3分の2以上の出席は何回？", "授業15回なら10回以上の出席（欠席5回まで）、30回なら20回以上の出席（欠席10回まで）が必要です。"),
        ], first=True)
        p.write_text(h, encoding="utf-8"); out.append("shusseki-ritsu")
    # 血のつながり：「いとこ 血の繋がり 割合」「いとこ 血の濃さ」
    p = page("ketsuen"); h = p.read_text(encoding="utf-8")
    if not done(h):
        h = set_title(h, "血のつながり 計算｜いとこの血の繋がりの割合は12.5%｜親子・はとこも｜シミュラボ",
                      "いとこの血の繋がりの割合（血縁度）は12.5%（8分の1）。親子・きょうだい50%、おじ・おば25%、はとこ3.125%など、続柄ごとの血の濃さを％で表示する無料ツール。いとこの子や二重いとこの割合も早見表で。",
                      "血のつながり 計算｜いとこの血の繋がりは12.5%")
        h = rep(h, '''    <tr><td>はとこ</td><td>3.125%</td><td>1/32</td></tr></table>''',
                '''    <tr><td>はとこ</td><td>3.125%</td><td>1/32</td></tr>
    <tr><td>異母・異父きょうだい</td><td>25%</td><td>1/4</td></tr>
    <tr><td>いとこの子（いとこ違い）</td><td>6.25%</td><td>1/16</td></tr>
    <tr><td>二重いとこ（父方・母方の両方がいとこ）</td><td>25%</td><td>1/4</td></tr></table>
    ''' + MARK + '''
    <h2>いとこの血の繋がりは、なぜ12.5%？</h2>
    <p>いとこ同士は、共通の祖父母（祖父と祖母の2人）を通じてつながっています。祖父から見ると、あなたまで2世代、いとこまで2世代の合計4回、遺伝子が1/2ずつ受け継がれるので (1/2)<sup>4</sup>＝1/16。祖母を通じた分も同じく1/16なので、合わせて <b>1/8（12.5%）</b>になります。はとこ（祖父母のきょうだいの孫）は、たどる世代が2つ増えるので1/32（約3.1%）まで薄まります。</p>''')
        h = add_faq(h, [
            ("いとこの血の繋がりの割合は？", "12.5%（8分の1）です。親子・きょうだいの50%の4分の1にあたります。"),
            ("はとこの血の繋がりの割合は？", "3.125%（32分の1）です。いとこの4分の1になります。"),
        ], first=True)
        p.write_text(h, encoding="utf-8"); out.append("ketsuen")
    # ml⇔g：「1mlは何g」
    p = page("ml-gram"); h = p.read_text(encoding="utf-8")
    if not done(h):
        h = set_title(h, "1mlは何g？ml⇔グラム換算｜水・牛乳・油・醤油・はちみつ｜シミュラボ",
                      "1mlは何グラム？水は1ml＝1g、牛乳は1.03g、サラダ油は0.92g、醤油は1.15g、はちみつは1.4g。食材を選んでmlとグラムを相互換算する無料ツール。100ml・200mlの早見表つき。",
                      "1mlは何g？ml⇔グラム換算")
        h = rep(h, '''    <tr><td>醤油</td><td>1.15g</td></tr><tr><td>はちみつ</td><td>1.4g</td></tr><tr><td>小麦粉</td><td>0.55g</td></tr></table>''',
                '''    <tr><td>醤油</td><td>1.15g</td></tr><tr><td>はちみつ</td><td>1.4g</td></tr><tr><td>小麦粉</td><td>0.55g</td></tr></table>
    ''' + MARK + '''
    <h2>100ml・180ml・200mlは何グラム？（早見表）</h2>
    <div class="tbl-scroll"><table class="seo-table"><tr><th>食材</th><th>100ml</th><th>180ml（1合）</th><th>200ml（1カップ）</th><th>500ml</th></tr>
    <tr><td>水</td><td>100g</td><td>180g</td><td>200g</td><td>500g</td></tr>
    <tr><td>牛乳</td><td>103g</td><td>185g</td><td>206g</td><td>515g</td></tr>
    <tr><td>サラダ油</td><td>92g</td><td>166g</td><td>184g</td><td>460g</td></tr>
    <tr><td>醤油</td><td>115g</td><td>207g</td><td>230g</td><td>575g</td></tr>
    <tr><td>はちみつ</td><td>140g</td><td>252g</td><td>280g</td><td>700g</td></tr>
    <tr><td>小麦粉</td><td>55g</td><td>99g</td><td>110g</td><td>275g</td></tr></table></div>
    <p class="hint">粉ものは、ふるい方や詰め方で同じ量でも重さが1〜2割変わります。お菓子づくりなど正確さが必要なときは、はかりで量ってください。</p>''')
        h = add_faq(h, [
            ("1mlは何g？", "水なら1ml＝1gです。食材によって違い、牛乳は約1.03g、サラダ油は約0.92g、醤油は約1.15g、はちみつは約1.4gです。"),
            ("mlとgの違いは？", "mlは体積（かさ）、gは重さの単位です。同じ1mlでも、ものの密度（比重）によって重さが変わります。"),
        ], first=True)
        p.write_text(h, encoding="utf-8"); out.append("ml-gram")
    return ",".join(out) or "skip"


# ---------------------------------------------------------------- ⑤ ライブ系：地域を記憶
LIVE_JS = r"""/* ライブ系：選んだ都道府県・地点をこのブラウザに記憶し、次に開いたときはその地域ですぐ表示する（2026-10）
   都道府県は全ページ共通（夕焼けで東京を選べば、星空・傘・洗濯も東京で開く）。地点（#spot）はページごと。
   保存先は localStorage のみ（サーバーには送らない）。 */
(function () {
  var NO_AUTO = ['umareta-hi-tenki'];          // 地域以外の入力（誕生日など）が主役のページは、自動では計算しない
  var path = location.pathname.replace(/index\.html$/, '');
  var slug = (path.match(/\/sims\/([^/]+)\//) || [])[1] || '';
  var base = function (t) { return (t || '').replace(/[（(].*$/, '').trim(); };
  function store(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function load(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  var sel = document.getElementById('pref'), key, val, idx = -1;
  if (sel) {
    key = 'shimulabo:pref';
    val = load(key);
    sel.addEventListener('change', function () { store(key, base(sel.options[sel.selectedIndex].text)); });
    if (val) idx = Array.prototype.findIndex.call(sel.options, function (o) { return base(o.text) === val; });
  } else {
    sel = document.getElementById('spot'); if (!sel) return;
    key = 'shimulabo:spot:' + slug;
    val = load(key);
    sel.addEventListener('change', function () { store(key, sel.value); });
    if (val) idx = Array.prototype.findIndex.call(sel.options, function (o) { return o.value === val; });
  }
  var btn = document.getElementById('calcBtn');
  if (btn) btn.addEventListener('click', function () { sel.dispatchEvent(new Event('change')); });
  if (idx < 0) return;
  sel.selectedIndex = idx;
  var note = document.createElement('p');
  note.className = 'hint';
  note.style.marginTop = '6px';
  note.textContent = '前回選んだ「' + base(sel.options[idx].text) + '」で表示しています（このブラウザに保存）';
  sel.parentNode.appendChild(note);
  if (NO_AUTO.indexOf(slug) >= 0) return;
  if (btn) {
    // 開いた直下で結果までスクロールしないよう、自動表示のあいだだけスクロールを止める（操作したら即解除）
    var orig = Element.prototype.scrollIntoView, restored = false;
    var restore = function () { if (!restored) { restored = true; Element.prototype.scrollIntoView = orig; } };
    Element.prototype.scrollIntoView = function () {};
    ['pointerdown', 'keydown', 'touchstart'].forEach(function (ev) { window.addEventListener(ev, restore, { once: true, capture: true }); });
    setTimeout(restore, 6000);
    btn.click();
  } else {
    sel.dispatchEvent(new Event('change'));
  }
})();
"""


def live():
    (ROOT / "assets" / "live-remember.js").write_text(LIVE_JS, encoding="utf-8")
    hub = (ROOT / "live" / "index.html").read_text(encoding="utf-8")
    slugs = sorted(set(re.findall(r'href="\.\./sims/([a-z0-9-]+)/"', hub)))
    tag = '<script src="../../assets/live-remember.js?v=1"></script>'
    n = 0
    for s in slugs:
        p = page(s); h = p.read_text(encoding="utf-8")
        if tag in h or not re.search(r'<select id="(pref|spot)"', h):
            continue
        h = rep(h, "</body>", tag + "\n</body>")
        p.write_text(h, encoding="utf-8"); n += 1
    return f"{n}ページに追加"


if __name__ == "__main__":
    for name, fn in [("①海抜チェッカー", kaibatsu), ("②チケット当選確率", ticket), ("③歯車", gears),
                     ("④検索の聞き方に合わせる3ページ", tune3), ("⑤ライブ系の地域記憶", live)]:
        print(name, fn())
