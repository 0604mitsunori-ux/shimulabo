"""/kyouiku/（学校・教材会社の方へ）を作る（2026-11-19）。何度実行しても同じ結果。
- 先生（無料で使う）と、教材会社・塾・EdTech（制作・使用許諾・授業パック＝有料）の2つの入口
- 数字は GA4（2026/9/1〜11/17）。更新するときは STATS を書き換える
- 頭・フッター・メールフォームの JS は contact/index.html を流用（build_seisaku.py と同じ作り）
- 画像は kyouiku/img/*.jpg（理科ページの実画面）
使い方: python scripts/build_kyouiku.py
"""
import html as H
import io, json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://shimulabo.com"
rd = lambda p: io.open(os.path.join(ROOT, p), encoding="utf-8").read()
def wr(p, s): io.open(os.path.join(ROOT, p), "w", encoding="utf-8", newline="").write(s)

idx = rd("index.html")
total = int(re.search(r"<b>(\d+)</b>本 公開中", idx).group(1))
U = json.load(io.open(os.path.join(ROOT, "scripts", "rika", "units.json"), encoding="utf-8"))
rika = len({it["id"] for s in U["sections"] for g in s["groups"] for it in g["items"]})

STATS = [("59%", "平日8〜16時（授業の時間帯）の利用"), ("5分23秒", "学校のChromebookでの1回の平均利用時間"),
         (f"{rika}本", "理科の授業向け（小学校〜高校・単元別）")]
STATS_SRC = "数字はシミュラボのアクセス解析（Googleアナリティクス、2026年9月1日〜11月17日）。"

EXAMPLES = [  # (slug, 画像, 単元, 説明)
    ("tsuki-michikake", "小4・小6・中3 月と太陽", "宇宙から見た図と、日本から見た空が連動して動きます。"),
    ("denryu-jikai", "小5 電磁石／中2 電流と磁界", "電流の向きを変えると、磁界と方位磁針が反転します。"),
    ("hone-kinniku", "小4 人の体のつくりと運動", "うでを曲げると、縮む筋肉とゆるむ筋肉が入れ替わります。"),
    ("daniel-denchi", "中3 化学変化と電池", "イオンと電子の動きを、反応式と一緒に追えます。"),
    ("kamu-pulley", "中学 技術 動力伝達の機構", "直径を変えると、回転数と速度伝達比を計算して表示します。"),
    ("maku-yuso", "高校 生物 細胞と分子", "先生からのリクエストで作りました。受動輸送と能動輸送を比べられます。"),
]
MENUS = [
    ("新しく作る", "制作受託", "5万円〜", "／1本", ["御社の単元・教科書・指導案に合わせて新しく作る", "3D・複数場面のものは 30万円〜", "触れる試作をお見せしてから本制作", "納品後1か月の修正を含む"]),
    ("いまあるものを使う", "使用許諾・埋め込み", "年3万円〜", "／1本", [f"公開中の理科{rika}本から選べる", "理科をまとめて：年30万円〜", "御社のロゴ・配色への変更も可", "iframe埋め込み、またはファイル提供"]),
    ("一緒に作る", "授業パック共同開発", "ご相談", "", ["シミュ＋ワークシート＋指導の流れを1セットに", "先生向けの配布・販売を想定", "制作費と売上の分け方はご相談", "まず1単元の試作から"]),
]
FAQS = [
    ("先生個人が授業で使うのに料金はかかりますか？", "かかりません。公開中のページは、授業・家庭学習でそのまま無料でお使いいただけます。URLを配るだけで、児童・生徒のタブレットでそれぞれ操作できます。"),
    ("学校や自治体でまとめて使うときに手続きは必要ですか？", "公開ページを授業で使うだけなら手続きは不要です。校内のポータルや学習サイトに組み込みたい、名前や配色を変えたいといった場合は、下のフォームからご相談ください。"),
    ("教材会社の自社サービスに組み込めますか？", "はい。使用許諾（埋め込み・ファイル提供）か、御社向けの制作でご提供します。1つのHTMLファイルで外部のライブラリやサーバーを使わないため、LMSや学習アプリにも組み込みやすい作りです。"),
    ("児童・生徒の個人情報は扱いますか？", "扱いません。ログインは不要で、入力した内容はサーバーに送らず端末の中だけで計算します。"),
    ("料金はどう決まりますか？", "上の金額はめやす（税別）です。教科・本数・納品の形をうかがってからお見積りします。触れる試作を先にお見せして、方向性を確かめてから本制作に進みます。"),
    ("どの端末で動きますか？", "Chromebook・iPad・Windows・電子黒板のブラウザで動き、指でもマウスでも操作できます。"),
]

TITLE = "学校・教材会社の方へ｜授業で使われている理科シミュレーションの制作・使用許諾｜シミュラボ"
DESC = (f"シミュラボの理科シミュレーション（小学校〜高校・{rika}本）は、先生は授業で無料で使えます。"
        "教材会社・学習塾・EdTech企業向けに、シミュレーションの制作受託・使用許諾（埋め込み）・授業パックの共同開発を承ります。")

c = rd("contact/index.html")
head = c[:c.index("</head>")]
head = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", head, flags=re.S)
head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{DESC}">', head)
head = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="学校・教材会社の方へ｜シミュラボ">', head)
head = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="授業で使われている理科シミュレーションを、御社の教材に。制作・使用許諾・授業パックの共同開発。">', head)
head = head.replace(f"{BASE}/contact/", f"{BASE}/kyouiku/").replace("/ogp/contact.png", "/ogp/kyouiku.png")
head = head.replace('"name": "広告掲載・タイアップ"', '"name": "学校・教材会社の方へ"')
ld_service = {"@context": "https://schema.org", "@type": "Service", "name": "教材用シミュレーションの制作・使用許諾",
              "serviceType": "理科シミュレーション教材の制作受託・使用許諾・授業パック共同開発",
              "audience": {"@type": "EducationalAudience", "educationalRole": "teacher"},
              "provider": {"@type": "Organization", "name": "シミュラボ", "url": BASE + "/"},
              "areaServed": "JP", "url": BASE + "/kyouiku/", "description": DESC}
ld_faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]}
head += ('    <style>\n'
 '.ky-hero{display:grid;grid-template-columns:1.1fr .9fr;gap:22px;align-items:center;margin:6px 0 8px}\n'
 '.ky-hero img{width:100%;height:auto;border-radius:14px;border:1px solid var(--line);display:block}\n'
 '.ky-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:16px 0 4px}\n'
 '.ky-stat{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 14px 12px}\n'
 '.ky-stat b{display:block;font-size:28px;line-height:1.15;color:var(--accent);font-variant-numeric:tabular-nums}\n'
 '.ky-stat span{font-size:12.5px;color:var(--ink-2);line-height:1.5;display:block;margin-top:4px}\n'
 '.ky-src{font-size:11.5px;color:var(--ink-3);margin:6px 0 0}\n'
 '.ky-two{display:grid;grid-template-columns:1fr 1fr;gap:14px}\n'
 '.ky-door{display:block;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px 18px 16px;text-decoration:none;color:inherit;transition:transform .2s,box-shadow .2s}\n'
 '.ky-door:hover{transform:translateY(-3px);box-shadow:0 10px 24px rgba(20,24,29,.08)}\n'
 '.ky-door .k{font-size:12px;font-weight:800;color:var(--accent);letter-spacing:.06em}\n'
 '.ky-door h3{margin:4px 0 6px;font-size:19px}.ky-door p{margin:0;font-size:13.5px;color:var(--ink-2);line-height:1.7}\n'
 '.ky-door .go{display:inline-block;margin-top:10px;font-weight:800;font-size:13.5px;color:var(--teal-d)}\n'
 '.ky-ex{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,290px),1fr));gap:14px}\n'
 '.ky-ex a{display:block;background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;text-decoration:none;color:inherit;transition:transform .2s,box-shadow .2s}\n'
 '.ky-ex a:hover{transform:translateY(-3px);box-shadow:0 10px 24px rgba(20,24,29,.08)}\n'
 '.ky-ex img{width:100%;height:auto;aspect-ratio:940/560;object-fit:cover;display:block;border-bottom:1px solid var(--line)}\n'
 '.ky-ex .t{padding:11px 13px 13px}.ky-ex .u{font-size:11.5px;font-weight:800;color:var(--teal-d)}\n'
 '.ky-ex h3{margin:3px 0 4px;font-size:15px;line-height:1.45}.ky-ex p{margin:0;font-size:12.5px;color:var(--ink-2);line-height:1.6}\n'
 '.ky-menu{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}\n'
 '.ky-plan{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px 16px 14px}\n'
 '.ky-plan.hi{border:2px solid var(--accent)}\n'
 '.ky-plan .k{font-size:12px;font-weight:800;color:var(--ink-3)}.ky-plan h3{margin:2px 0 6px;font-size:18px}\n'
 '.ky-plan .p{font-size:26px;font-weight:800;color:var(--teal-d);font-variant-numeric:tabular-nums}.ky-plan.hi .p{color:var(--accent)}\n'
 '.ky-plan .p small{font-size:13px;color:var(--ink-3);font-weight:700}\n'
 '.ky-plan ul{margin:10px 0 0;padding-left:1.1em;font-size:13px;line-height:1.75;color:var(--ink)}\n'
 '.ky-note{font-size:12px;color:var(--ink-3);margin:10px 0 0}\n'
 '.ky-steps{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;counter-reset:s}\n'
 '.ky-steps div{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:13px 13px 12px;counter-increment:s}\n'
 '.ky-steps div::before{content:counter(s);display:inline-flex;width:24px;height:24px;border-radius:50%;background:var(--accent);color:#fff;font-weight:800;font-size:13px;align-items:center;justify-content:center;margin-bottom:6px}\n'
 '.ky-steps b{display:block;font-size:15px}.ky-steps i{font-style:normal;font-size:12px;font-weight:800;color:var(--teal-d)}.ky-steps p{margin:4px 0 0;font-size:12.5px;color:var(--ink-2);line-height:1.6}\n'
 '.ky-case{display:grid;grid-template-columns:.9fr 1.1fr;gap:18px;align-items:center}.ky-case img{width:100%;height:auto;border-radius:12px;border:1px solid var(--line)}\n'
 '@media(max-width:760px){.ky-hero,.ky-two,.ky-case{grid-template-columns:1fr}.ky-menu{grid-template-columns:1fr}.ky-steps{grid-template-columns:1fr 1fr}.ky-stats{grid-template-columns:repeat(3,1fr);gap:6px}.ky-stat{padding:10px 8px 9px;border-radius:12px}.ky-stat b{font-size:19px}.ky-stat span{font-size:10.5px;line-height:1.45}.ky-hero img{max-height:260px;object-fit:cover;object-position:top}.ky-case img{max-height:300px;object-fit:cover;object-position:top}}\n'
 '    </style>\n'
 '    <script type="application/ld+json">' + json.dumps(ld_service, ensure_ascii=False) + "</script>\n"
 '    <script type="application/ld+json">' + json.dumps(ld_faq, ensure_ascii=False) + "</script>\n")
header = c[c.index("</head>"):c.index('<main class="wrap">')]

def h1(slug):
    m = re.search(r"<h1>(.*?)</h1>", rd(f"sims/{slug}/index.html"), re.S)
    return re.sub(r"<[^>]+>", "", m.group(1)).strip()

stats = "".join(f'<div class="ky-stat"><b>{v}</b><span>{k}</span></div>' for v, k in STATS)
ex = "".join(f'''<a href="../sims/{s}/"><img src="img/{s}.jpg" alt="{H.escape(h1(s))}の画面" loading="lazy" width="800" height="477"><div class="t"><div class="u">{u}</div><h3>{H.escape(h1(s))}</h3><p>{d}</p></div></a>''' for s, u, d in EXAMPLES)
menu = "".join(f'''<div class="ky-plan{' hi' if i == 0 else ''}"><div class="k">{k}</div><h3>{t}</h3><div class="p">{p}<small>{u}</small></div><ul>{''.join(f'<li>{b}</li>' for b in bl)}</ul></div>''' for i, (k, t, p, u, bl) in enumerate(MENUS))
faq_dl = "".join(f"<dt>{q}</dt><dd>{a}</dd>" for q, a in FAQS)
opts = "".join(f'<option value="{v}">{v}</option>' for v in ["制作受託（新しく作る）", "使用許諾・埋め込み（いまあるものを使う）", "授業パックの共同開発", "先生として授業での使い方を相談したい", "まだ決まっていない・相談したい"])

main = f'''<main class="wrap">
  <nav class="breadcrumb" aria-label="breadcrumb"><a href="../">ホーム</a><span>›</span><span class="cur">学校・教材会社の方へ</span></nav>

  <div class="ky-hero">
    <div class="sim-head" style="margin:0">
      <div class="cat">FOR SCHOOLS &amp; PUBLISHERS</div>
      <h1>授業で、いま使われている<br>理科シミュレーションを。</h1>
      <p class="lead">シミュラボの理科ページ（小学校〜高校・{rika}本）は、先生はそのまま無料で授業に使えます。教材会社・学習塾・EdTech企業の方には、御社の教材に組み込める形での制作・使用許諾をご提供します。</p>
      <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:14px">
        <a class="btn btn-primary" style="width:auto;display:inline-flex;padding:12px 22px" href="#form">相談する（無料）→</a>
        <a class="btn" style="width:auto;display:inline-flex;padding:12px 22px" href="#menu">料金のめやすを見る</a>
      </div>
    </div>
    <img src="img/tsuki-michikake.jpg" alt="月の満ち欠けシミュレーターの画面" width="800" height="477">
  </div>

  <div class="ky-stats">{stats}</div>
  <p class="ky-src">{STATS_SRC}</p>

  <section class="panel">
    <h2>👋 どちらの方ですか？</h2>
    <div class="ky-two">
      <a class="ky-door" href="#teacher"><div class="k">先生の方</div><h3>授業でそのまま使う（無料）</h3><p>URLを配るだけで、児童・生徒のタブレットで操作できます。ログインもアプリも不要です。ほしい単元はリクエストで作ります。</p><span class="go">使い方を見る →</span></a>
      <a class="ky-door" href="#menu"><div class="k">教材会社・学習塾・EdTechの方</div><h3>御社の教材に組み込む</h3><p>新しく作る・いまあるものを使う・授業パックを一緒に作る、の3つの形でご提供します。</p><span class="go">メニューと料金を見る →</span></a>
    </div>
  </section>

  <section class="panel">
    <h2>🔬 授業で使われているシミュレーション（実際の画面）</h2>
    <div class="ky-ex">{ex}</div>
    <p style="margin:12px 0 0;text-align:right"><a href="../rika/" style="font-weight:800;font-size:13.5px">学年・単元別に{rika}本を見る →</a></p>
  </section>

  <article class="article" id="teacher">
    <h2>先生の方へ：授業での使い方</h2>
    <ul>
      <li><b>電子黒板・プロジェクターで見せる</b>：条件を変えると、その場で図と数値が変わります。全画面表示（F11キー）が見やすいです。</li>
      <li><b>一人ひとりのタブレットで試す</b>：URLを配るだけ。Google Classroom などに貼れば、それぞれが条件を変えて確かめられます。</li>
      <li><b>家庭学習・ふり返りに</b>：授業で見たページを、家でもう一度動かせます。</li>
    </ul>
    <p>料金はかかりません。「この単元のこの現象を見せたい」というご要望は、<a href="../request/">リクエスト</a>からお送りください。いただいたリクエストは<a href="../board/">リクエストボード</a>で進み具合が見られます。</p>
  </article>

  <section class="panel">
    <h2>📮 事例：高校の先生のリクエストから2本作りました</h2>
    <div class="ky-case">
      <img src="img/maku-yuso.jpg" alt="膜輸送のシミュレーターの画面" loading="lazy" width="800" height="477">
      <div>
        <p style="margin:0 0 8px;font-size:14px;line-height:1.8">「授業で膜輸送を動かして見せたい」「リン脂質が水中でどう集まるかを見せたい」というリクエストをいただき、高校「生物」の単元に合わせて2本作りました。公開後に「3Dで見る」機能も足しています。</p>
        <p style="margin:0"><a href="../sims/maku-yuso/" style="font-weight:800">膜輸送のシミュレーター →</a>　<a href="../sims/rinshishitsu-maku/" style="font-weight:800">リン脂質と細胞膜のでき方 →</a></p>
      </div>
    </div>
  </section>

  <section class="panel" id="menu">
    <h2>🏫 教材会社・学習塾・EdTechの方へ：3つのメニュー</h2>
    <div class="ky-menu">{menu}</div>
    <p class="ky-note">※ 金額はめやす（税別）です。教科・本数・納品の形によって変わります。先生個人の授業での利用は無料です。</p>
  </section>

  <section class="panel">
    <h2>⏱️ 進め方（1本あたり3〜5週間がめやす）</h2>
    <div class="ky-steps">
      <div><b>ご相談</b><i>無料</i><p>単元・使う場面・置き場所をうかがいます。</p></div>
      <div><b>試作</b><i>約1週間</i><p>動きと見せ方を決める、触れる試作をお見せします。</p></div>
      <div><b>制作・確認</b><i>2〜3週間</i><p>数値の照合と、学校の端末での表示確認をして仕上げます。</p></div>
      <div><b>公開・改良</b><i>公開後</i><p>設置のお手伝いと、使われ方を見ての改良まで。</p></div>
    </div>
  </section>

  <section class="panel" id="form">
    <h2>✉️ ご相談・お見積り</h2>
    <div class="field">
      <label>会社名・学校名・団体名 <span class="hint">（任意）</span></label>
      <input type="text" id="company" placeholder="例：株式会社○○／○○中学校">
    </div>
    <div class="row">
      <div class="field">
        <label>お名前 <span class="hint">（必須）</span></label>
        <input type="text" id="person" placeholder="例：山田 太郎">
      </div>
      <div class="field">
        <label>メールアドレス <span class="hint">（必須）</span></label>
        <input type="email" id="email" placeholder="例：you@example.com">
      </div>
    </div>
    <div class="field">
      <label>ご相談の種類 <span class="hint">（必須）</span></label>
      <select id="type">{opts}</select>
    </div>
    <div class="field">
      <label>ご相談内容 <span class="hint">（必須）</span></label>
      <textarea id="message" placeholder="教科・単元、使う場面（授業・教材・アプリなど）、本数、ご希望の時期などをご記入いただけるとスムーズです。"></textarea>
    </div>
    <button class="btn btn-primary" id="sendBtn">この内容で相談する</button>
    <p id="formNote" style="font-size:13px;color:var(--ink-2);margin:14px 0 0;text-align:center;">送信ボタンを押すと、メールソフトが起動します。</p>
    <p style="font-size:13px;color:var(--ink-2);margin:10px 0 0;text-align:center;">企業向けの計算ツール・診断コンテンツの制作は<a href="../seisaku/">こちら</a></p>
  </section>

  <article class="article">
    <h2>よくあるご質問</h2>
    <dl class="faq">{faq_dl}</dl>
  </article>
</main>
'''

footer = c[c.index('<footer class="site-footer">'):c.index("<script>\n(() => {")]
js = c[c.index("<script>\n(() => {"):]
js = js.replace("const subject = `【シミュラボ】広告掲載・タイアップのお問い合わせ（${$('type').value}）`;",
                "const subject = `【シミュラボ】学校・教材のご相談（${$('type').value}）`;")
js = js.replace("■会社名・媒体名：", "■会社名・学校名：")
assert "学校・教材のご相談" in js
os.makedirs(os.path.join(ROOT, "kyouiku"), exist_ok=True)
wr("kyouiku/index.html", head + header + main + "\n" + footer + js)
print(f"kyouiku/index.html（理科{rika}本）")

p = os.path.join(ROOT, "ogp", "kyouiku.png")
if not os.path.exists(p):
    gen = os.path.join(ROOT, "scripts", "gen_images.py"); ns = {"__file__": gen}
    exec(compile(rd("scripts/gen_images.py").split("\nSIMS = [")[0], gen, "exec"), ns)
    ns["make_ogp"](p, "授業で使われている\n理科シミュレーション", "FOR SCHOOLS", underline="理科")
    print("OGP:", p)
